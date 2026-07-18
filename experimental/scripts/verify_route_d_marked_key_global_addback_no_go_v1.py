#!/usr/bin/env python3
"""Deterministic verifier for Route-D marked-key global add-back no-go v1.

This stdlib-only verifier exhausts two finite-field fixtures.  It checks the
printed-key F_17 counterexample, the independent F_101 beta-omission stress
test, marked common-core preservation, projective primitivity, extension
deletion, full Vandermonde rank, and deployed arithmetic.  It intentionally
does not simulate undefined named first-match projectors or an actual RIM
incidence matrix.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
from collections import Counter
from typing import Iterable, Mapping, Sequence


DEPLOYED_R = 67472
DEPLOYED_P = 2130706433
DEPLOYED_PRODUCT = 143763024447376
SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "singleton_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "marked_contact_commit": "3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835",
    "marked_contact_note_blob": "13479a4b8de5f495508375a16366b62efe39acab",
    "priority_zero_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "priority_zero_note_blob": "fdeabf0708cb8806feefae9322ed9002339332cf",
    "rank_adapter_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "rank_adapter_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def trim(poly: Sequence[int], p: int) -> tuple[int, ...]:
    out = [value % p for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % p
    return trim(out, p)


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator, p))
    den = trim(denominator, p)
    require(den != (0,), "zero polynomial divisor")
    quotient = [0] * max(1, len(num) - len(den) + 1)
    inverse = pow(den[-1], -1, p)
    while len(num) >= len(den) and any(num):
        shift = len(num) - len(den)
        coefficient = num[-1] * inverse % p
        quotient[shift] = coefficient
        for i, value in enumerate(den):
            num[i + shift] = (num[i + shift] - coefficient * value) % p
        while len(num) > 1 and num[-1] == 0:
            num.pop()
    return trim(quotient, p), trim(num, p)


def poly_gcd(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    a, b = trim(left, p), trim(right, p)
    while b != (0,):
        _, remainder = poly_divmod(a, b, p)
        a, b = b, remainder
    inverse = pow(a[-1], -1, p)
    return tuple(value * inverse % p for value in a)


def locator(roots: Iterable[int], p: int) -> tuple[int, ...]:
    out = (1,)
    for root in sorted(roots):
        out = poly_mul(out, ((-root) % p, 1), p)
    return out


def roots_in_nonzero_domain(poly: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(
        x for x in range(1, p)
        if sum(value * pow(x, degree, p) for degree, value in enumerate(poly)) % p == 0
    )


def signed_weight(
    positive: Iterable[int], negative: Iterable[int]
) -> dict[int, int]:
    values: Counter[int] = Counter(positive)
    values.subtract(negative)
    return {root: coefficient for root, coefficient in values.items() if coefficient}


def signed_moment(weight: Mapping[int, int], degree: int, p: int) -> int:
    return sum(
        coefficient * pow(root, degree, p)
        for root, coefficient in weight.items()
    ) % p


def projectively_primitive(weight: Mapping[int, int], p: int) -> bool:
    target = dict(weight)
    stabilizers = []
    for scalar in range(1, p):
        pushed = {(scalar * root) % p: coefficient for root, coefficient in target.items()}
        for sign in (1, -1):
            if pushed == {root: sign * coefficient for root, coefficient in target.items()}:
                stabilizers.append((scalar, sign))
    return stabilizers == [(1, 1)]


def det3(columns: Sequence[Sequence[int]], p: int) -> int:
    require(len(columns) == 3 and all(len(column) == 3 for column in columns),
            "det3 shape")
    matrix = [[columns[column][row] % p for column in range(3)] for row in range(3)]
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % p


def lex_marked_pivot(weight: Mapping[int, int], p: int) -> int:
    support = sorted(weight)
    require(len(support) >= 3, "support too small for marked pivot")
    columns = [
        (
            weight[root] % p,
            weight[root] * root % p,
            weight[root] * root * root % p,
        )
        for root in support[:3]
    ]
    return det3(columns, p)


def f17_fixture() -> dict[str, object]:
    p = 17
    domain = tuple(range(1, p))
    beta = 16
    c = 11
    packets = []
    for a_roots in itertools.combinations(domain, 2):
        u = locator(a_roots, p)
        v = ((u[0] - c) % p, *u[1:])
        r_roots = roots_in_nonzero_domain(v, p)
        if len(r_roots) != 2:
            continue
        for g in domain:
            if g in a_roots or g in r_roots:
                continue
            if (g + sum(a_roots)) % p != beta:
                continue
            core = (g,)
            support = tuple(sorted((*core, *a_roots)))
            target = tuple(sorted((*core, *r_roots)))
            packets.append((support, target, u, core, a_roots, r_roots, v))

    packets.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    require(len(packets) == 38, "F17 packet bucket drift")

    deduped = []
    seen = set()
    for packet in packets:
        key = (2, c, packet[2], beta)
        if key not in seen:
            seen.add(key)
            deduped.append(packet)
    require(len(deduped) == 38, "F17 Rule1 dedup drift")

    representative = deduped[0]
    u0 = representative[2]
    v0 = representative[6]
    a0 = representative[4]
    r0 = representative[5]
    require(
        representative[:6]
        == ((1, 2, 13), (2, 15, 16), (13, 3, 1), (2,), (1, 13), (15, 16)),
        "F17 canonical representative drift",
    )

    gcd_histogram: Counter[str] = Counter()
    rows = []
    for packet in deduped[1:]:
        u, core, a_roots, r_roots, v = (
            packet[2], packet[3], packet[4], packet[5], packet[6]
        )
        h = poly_gcd(poly_mul(u0, v, p), poly_mul(v0, u, p), p)
        gcd_histogram[str(h)] += 1
        if h != (1,):
            continue
        mu = signed_weight((*a0, *r_roots), (*r0, *a_roots))
        c_plus = set(a0) & set(core)
        c_minus = set(r0) & set(core)
        kappa = signed_weight(c_plus, c_minus)
        lam = dict(mu)
        for root, coefficient in kappa.items():
            lam[root] = lam.get(root, 0) - coefficient
            if lam[root] == 0:
                del lam[root]
        require(all(signed_moment(mu, degree, p) == 0 for degree in range(3)),
                "F17 homogeneous moments drift")
        require(all(
            signed_moment(lam, degree, p)
            == (-signed_moment(kappa, degree, p)) % p
            for degree in range(3)
        ), "F17 inhomogeneous moments drift")
        require(set(lam).isdisjoint(core), "F17 lambda met marked core")
        require(projectively_primitive(lam, p), "F17 lambda primitive orbit drift")
        pivot = lex_marked_pivot(lam, p)
        require(pivot != 0, "F17 full-rank pivot vanished")
        rows.append({
            "packet": packet,
            "mu": mu,
            "kappa": kappa,
            "lambda": lam,
            "mu_primitive": projectively_primitive(mu, p),
            "extension": signed_moment(mu, 3, p) == 0,
            "pivot": pivot,
        })

    require(len(rows) == 25, "F17 H=1 key count drift")
    require(not any(row["extension"] for row in rows), "F17 extension count drift")
    require(len({row["packet"][2] for row in rows}) == 25, "F17 U collision")
    require(len({
        tuple((value - base) % p for value, base in itertools.zip_longest(
            row["packet"][2], u0, fillvalue=0
        ))
        for row in rows
    }) == 25, "F17 affine-shift collision")
    require(len({
        tuple(sorted(row["lambda"].items())) for row in rows
    }) == 25, "F17 lambda collision")
    require(len({
        tuple(sorted(row["mu"].items())) for row in rows
    }) == 25, "F17 mu collision")
    core_histogram = Counter(row["packet"][3][0] for row in rows)
    return {
        "p": p,
        "packets": len(packets),
        "rule1_deduped": len(deduped),
        "representative": {
            "G0": list(representative[3]),
            "A0": list(a0),
            "R0": list(r0),
            "U0": list(u0),
            "V0": list(v0),
        },
        "gcd_histogram": dict(sorted(gcd_histogram.items())),
        "printed_key_count": len(rows),
        "mu_primitive_count": sum(row["mu_primitive"] for row in rows),
        "lambda_primitive_count": len(rows),
        "nonempty_contact_count": sum(bool(row["kappa"]) for row in rows),
        "extension_count": sum(row["extension"] for row in rows),
        "nonextension_count": sum(not row["extension"] for row in rows),
        "lambda_support_histogram": dict(sorted(Counter(
            len(row["lambda"]) for row in rows
        ).items())),
        "nonzero_pivots": sum(row["pivot"] != 0 for row in rows),
        "distinct_pivot_labels": len({row["pivot"] for row in rows}),
        "literal_core_fibers": len(core_histogram),
        "max_core_fiber": max(core_histogram.values()),
        "mu_primitive_exceeds_field": sum(row["mu_primitive"] for row in rows) > p,
        "contact_lambda_exceeds_field": sum(bool(row["kappa"]) for row in rows) > p,
    }


def f101_fixture() -> dict[str, object]:
    p = 101
    u0 = (2, -3, 1)
    a0 = (1, 2)
    r0 = (24, 80)
    rows = []
    for a in range(p):
        for b in range(p):
            if a == 0 and b == 0:
                continue
            u = ((2 + b) % p, (-3 + a) % p, 1)
            v = ((1 + b) % p, (-3 + a) % p, 1)
            a_roots = roots_in_nonzero_domain(u, p)
            r_roots = roots_in_nonzero_domain(v, p)
            if len(a_roots) != 2 or len(r_roots) != 2:
                continue
            if set(a_roots) & {1, 2}:
                continue
            if set(r_roots) & {1, 24, 80}:
                continue
            mu = signed_weight((*a0, *r_roots), (*r0, *a_roots))
            lam = dict(mu)
            lam[1] = lam.get(1, 0) - 1
            if lam.get(1) == 0:
                del lam[1]
            require(all(signed_moment(mu, degree, p) == 0 for degree in range(3)),
                    "F101 homogeneous moments drift")
            require(all(signed_moment(lam, degree, p) == p - 1 for degree in range(3)),
                    "F101 inhomogeneous moments drift")
            require(1 not in lam, "F101 lambda met marked core")
            require(projectively_primitive(lam, p), "F101 primitive orbit drift")
            pivot = lex_marked_pivot(lam, p)
            require(pivot != 0, "F101 full-rank pivot vanished")
            rows.append({
                "a": a,
                "b": b,
                "u": u,
                "lambda": lam,
                "extension": signed_moment(mu, 3, p) == 0,
                "pivot": pivot,
                "beta": (4 - a) % p,
            })

    require(len(rows) == 2098, "F101 raw count drift")
    require(len({tuple(sorted(row["lambda"].items())) for row in rows}) == 2098,
            "F101 lambda collision")
    require(all(projectively_primitive(row["lambda"], p) for row in rows),
            "F101 primitive replay drift")
    nonextension = [row for row in rows if not row["extension"]]
    beta_histogram = Counter(row["beta"] for row in rows)
    pivot_histogram = Counter(row["pivot"] for row in rows)
    nonextension_pivots = Counter(row["pivot"] for row in nonextension)
    return {
        "p": p,
        "raw_count": len(rows),
        "primitive_count": len(rows),
        "extension_count": sum(row["extension"] for row in rows),
        "nonextension_count": len(nonextension),
        "support_histogram": dict(sorted(Counter(
            len(row["lambda"]) for row in rows
        ).items())),
        "nonzero_pivots": sum(row["pivot"] != 0 for row in rows),
        "distinct_pivot_labels": len(pivot_histogram),
        "max_pivot_multiplicity": max(pivot_histogram.values()),
        "nonextension_distinct_pivot_labels": len(nonextension_pivots),
        "nonextension_max_pivot_multiplicity": max(nonextension_pivots.values()),
        "beta_fibers": len(beta_histogram),
        "max_fixed_beta_fiber": max(beta_histogram.values()),
        "nonextension_exceeds_field": len(nonextension) > p,
    }


EXPECTED = {
    "deployed_product": DEPLOYED_PRODUCT,
    "f17": {
        "p": 17,
        "packets": 38,
        "rule1_deduped": 38,
        "representative": {
            "G0": [2],
            "A0": [1, 13],
            "R0": [15, 16],
            "U0": [13, 3, 1],
            "V0": [2, 3, 1],
        },
        "gcd_histogram": {
            "(1,)": 25,
            "(1, 1)": 3,
            "(16, 1)": 2,
            "(2, 1)": 3,
            "(4, 1)": 4,
        },
        "printed_key_count": 25,
        "mu_primitive_count": 24,
        "lambda_primitive_count": 25,
        "nonempty_contact_count": 9,
        "extension_count": 0,
        "nonextension_count": 25,
        "lambda_support_histogram": {5: 1, 6: 5, 7: 13, 8: 6},
        "nonzero_pivots": 25,
        "distinct_pivot_labels": 13,
        "literal_core_fibers": 13,
        "max_core_fiber": 4,
        "mu_primitive_exceeds_field": True,
        "contact_lambda_exceeds_field": False,
    },
    "f101": {
        "p": 101,
        "raw_count": 2098,
        "primitive_count": 2098,
        "extension_count": 21,
        "nonextension_count": 2077,
        "support_histogram": {5: 2, 6: 129, 7: 1967},
        "nonzero_pivots": 2098,
        "distinct_pivot_labels": 100,
        "max_pivot_multiplicity": 67,
        "nonextension_distinct_pivot_labels": 100,
        "nonextension_max_pivot_multiplicity": 66,
        "beta_fibers": 101,
        "max_fixed_beta_fiber": 23,
        "nonextension_exceeds_field": True,
    },
}


def summarize() -> dict[str, object]:
    return {
        "source_pins": dict(SOURCE_PINS),
        "deployed_r": DEPLOYED_R,
        "deployed_p": DEPLOYED_P,
        "deployed_product": DEPLOYED_R * DEPLOYED_P,
        "f17": f17_fixture(),
        "f101": f101_fixture(),
    }


def verify(summary: Mapping[str, object]) -> None:
    require(summary["source_pins"] == SOURCE_PINS, "source pins drift")
    require(summary["deployed_r"] == DEPLOYED_R, "deployed r drift")
    require(summary["deployed_p"] == DEPLOYED_P, "deployed p drift")
    require(summary["deployed_product"] == EXPECTED["deployed_product"],
            "deployed product drift")
    require(summary["f17"] == EXPECTED["f17"], "F17 certificate drift")
    require(summary["f101"] == EXPECTED["f101"], "F101 certificate drift")


def tamper_suite(summary: Mapping[str, object]) -> int:
    trials = [
        ("deployed_product", 1),
        ("f17.printed_key_count", 17),
        ("f17.mu_primitive_count", 23),
        ("f17.lambda_primitive_count", 24),
        ("f17.nonempty_contact_count", 10),
        ("f17.extension_count", 1),
        ("f17.nonzero_pivots", 24),
        ("f17.max_core_fiber", 5),
        ("f17.mu_primitive_exceeds_field", False),
        ("f101.raw_count", 2097),
        ("f101.primitive_count", 2097),
        ("f101.extension_count", 20),
        ("f101.nonextension_count", 2076),
        ("f101.nonzero_pivots", 2097),
        ("f101.max_fixed_beta_fiber", 101),
        ("f101.nonextension_exceeds_field", False),
    ]
    detected = 0
    for path, replacement in trials:
        forged = copy.deepcopy(summary)
        target = forged
        keys = path.split(".")
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = replacement
        try:
            verify(forged)
        except CertificateError:
            detected += 1
    require(detected == len(trials), "tamper suite failed open")
    return detected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        summary = summarize()
        verify(summary)
        if args.self_test:
            summary["tamper_trials"] = tamper_suite(summary)
    except CertificateError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("PASS: Route-D marked-key global add-back no-go v1")
        print(f"F17 printed-key full-mu primitive count: "
              f"{summary['f17']['mu_primitive_count']}")
        print(f"F17 field size: {summary['f17']['p']}")
        print(f"F101 nonextension count: {summary['f101']['nonextension_count']}")
        print(f"deployed product: {summary['deployed_product']}")
        if args.self_test:
            print(f"tamper trials: {summary['tamper_trials']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
