#!/usr/bin/env python3
"""Verify the Route-D F17 global marked-contact pivot no-go v1.

The verifier exhausts the fixed-beta, all-cell F_17 algebraic packet universe,
executes the explicitly defined Rule-1 and defect filters, preserves literal
cores, and checks exact contact/profile/pivot multiplicities.  It does not
simulate undefined named first-match projectors or an actual RIM matrix.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


P = 17
D = tuple(range(1, P))
R = 2
T = 2
BETA = 16
ANALOG_TARGET = T * P
SOURCE_PINS = {
    "base_commit": "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e",
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "singleton_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "marked_key_commit": "b23f997474f7a7aec9a889d933c774acc4980050",
    "marked_key_note_blob": "5ae8c3f628b8246f9d2c02201854256e56f3ee27",
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


def trim(poly: Sequence[int]) -> tuple[int, ...]:
    out = [value % P for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return trim(out)


def locator(roots: Iterable[int]) -> tuple[int, ...]:
    out = (1,)
    for root in sorted(roots):
        out = poly_mul(out, ((-root) % P, 1))
    return out


def roots_nonzero(poly: Sequence[int]) -> tuple[int, ...]:
    return tuple(
        x for x in D
        if sum(value * pow(x, degree, P)
               for degree, value in enumerate(poly)) % P == 0
    )


def signed_weight(
    positive: Iterable[int], negative: Iterable[int]
) -> dict[int, int]:
    values: Counter[int] = Counter(positive)
    values.subtract(negative)
    return {root: coefficient for root, coefficient in values.items() if coefficient}


def moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(
        coefficient * pow(root, degree, P)
        for root, coefficient in weight.items()
    ) % P


def projectively_primitive(weight: Mapping[int, int]) -> bool:
    target = dict(weight)
    stabilizers = []
    for scalar in D:
        pushed = {(scalar * root) % P: coefficient for root, coefficient in target.items()}
        for sign in (1, -1):
            if pushed == {root: sign * coefficient for root, coefficient in target.items()}:
                stabilizers.append((scalar, sign))
    return stabilizers == [(1, 1)]


def det3(columns: Sequence[Sequence[int]]) -> int:
    matrix = [[columns[column][row] % P for column in range(3)] for row in range(3)]
    return (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % P


def lex_pivot(weight: Mapping[int, int]) -> int:
    support = sorted(weight)
    require(len(support) >= 3, "support too small for pivot")
    columns = [
        (
            weight[root] % P,
            weight[root] * root % P,
            weight[root] * root * root % P,
        )
        for root in support[:3]
    ]
    return det3(columns)


def enumerate_cells() -> dict[int, tuple[tuple[object, ...], ...]]:
    cells: dict[int, tuple[tuple[object, ...], ...]] = {}
    for c in D:
        packets = []
        for a_roots in itertools.combinations(D, R):
            u = locator(a_roots)
            v = ((u[0] - c) % P, *u[1:])
            r_roots = roots_nonzero(v)
            if len(r_roots) != R:
                continue
            g = (BETA - sum(a_roots)) % P
            if g == 0 or g in a_roots or g in r_roots:
                continue
            core = (g,)
            support = tuple(sorted((*core, *a_roots)))
            target = tuple(sorted((*core, *r_roots)))
            packets.append((support, target, u, core, a_roots, r_roots, v))
        packets.sort(key=lambda packet: (packet[0], packet[1], packet[2], packet[3]))

        deduped = []
        seen = set()
        for packet in packets:
            key = (R, c, packet[2], BETA)
            if key not in seen:
                seen.add(key)
                deduped.append(packet)
        require(len(deduped) == len(packets), "Rule1 key unexpectedly repeated")
        if deduped:
            cells[c] = tuple(deduped)
    require(tuple(sorted(cells)) == D, "not every nonzero cell was occupied")
    return cells


def summarize() -> dict[str, object]:
    cells = enumerate_cells()
    packet_histogram = Counter(len(packets) for packets in cells.values())
    raw_packet_count = sum(len(packets) for packets in cells.values())
    require(raw_packet_count == 516, "raw packet count drift")

    filters: Counter[str] = Counter({
        "nonprimitive": 0, "extension": 0, "support_collapse": 0,
        "bc_size": 0, "toy_pivot_vanishing": 0, "retained": 0,
    })
    retained = []
    per_cell: Counter[int] = Counter()
    support_histogram: Counter[int] = Counter()
    for c, packets in sorted(cells.items()):
        representative = packets[0]
        a0 = representative[4]
        r0 = representative[5]
        for packet in packets[1:]:
            core, a_roots, r_roots = packet[3], packet[4], packet[5]
            mu = signed_weight((*a0, *r_roots), (*r0, *a_roots))
            require(all(moment(mu, degree) == 0 for degree in range(3)),
                    "homogeneous moment drift")
            if not projectively_primitive(mu):
                filters["nonprimitive"] += 1
                continue
            if moment(mu, 3) == 0:
                filters["extension"] += 1
                continue
            if len(mu) <= R + 1:
                filters["support_collapse"] += 1
                continue
            if len(mu) == R + 2:
                filters["bc_size"] += 1
                continue
            pivot = lex_pivot(mu)
            if pivot == 0:
                filters["toy_pivot_vanishing"] += 1
                continue
            filters["retained"] += 1
            per_cell[c] += 1
            support_histogram[len(mu)] += 1

            c_plus = set(a0) & set(core)
            c_minus = set(r0) & set(core)
            kappa = signed_weight(c_plus, c_minus)
            lam = dict(mu)
            for root, coefficient in kappa.items():
                lam[root] = lam.get(root, 0) - coefficient
                if lam[root] == 0:
                    del lam[root]
            require(set(lam).isdisjoint(core), "off-core weight met literal core")
            require(all(
                moment(lam, degree) == (-moment(kappa, degree)) % P
                for degree in range(3)
            ), "inhomogeneous target drift")
            require(projectively_primitive(lam), "off-core primitive orbit drift")
            lambda_pivot = lex_pivot(lam)
            require(lambda_pivot != 0, "contact lambda pivot vanished")
            retained.append({
                "cell": c,
                "packet": packet,
                "mu": mu,
                "kappa": kappa,
                "lambda": lam,
                "profile": (len(c_plus), len(c_minus)),
                "pivot": lambda_pivot,
            })

    require(sum(filters.values()) == raw_packet_count - len(cells),
            "comparison filter partition drift")
    require(filters["retained"] == len(retained) == 463, "retained count drift")

    contact = [row for row in retained if row["kappa"]]
    zero_contact = [row for row in retained if not row["kappa"]]
    require(len(contact) == 115 and len(zero_contact) == 348,
            "contact split drift")
    profile_histogram = Counter(row["profile"] for row in contact)
    label_histogram = Counter((row["profile"], row["pivot"]) for row in contact)
    keyed_lambda = {
        (row["cell"], tuple(sorted(row["lambda"].items()))) for row in contact
    }
    unkeyed_lambda = {
        tuple(sorted(row["lambda"].items())) for row in contact
    }
    retained_mu = {
        tuple(sorted(row["mu"].items())) for row in retained
    }
    support_rows: dict[tuple[tuple[int, int], ...], tuple[tuple[int, int], int]] = {}
    for row in contact:
        key = tuple(sorted(row["lambda"].items()))
        value = (row["profile"], row["pivot"])
        if key in support_rows:
            require(support_rows[key] == value,
                    "one lambda acquired inconsistent profile/pivot labels")
        support_rows[key] = value
    support_profile_histogram = Counter(
        profile for profile, _ in support_rows.values()
    )
    support_label_histogram = Counter(support_rows.values())
    return {
        "source_pins": dict(SOURCE_PINS),
        "parameters": {
            "p": P,
            "r": R,
            "t": T,
            "beta1": BETA,
            "analog_target": ANALOG_TARGET,
        },
        "occupied_cells": len(cells),
        "contact_support_profile_histogram": {
            str(profile): count for profile, count in sorted(support_profile_histogram.items())
        },
        "packet_count": raw_packet_count,
        "packet_count_histogram": dict(sorted(packet_histogram.items())),
        "representative_count": len(cells),
        "comparison_count": raw_packet_count - len(cells),
        "contact_support_count": len(support_rows),
        "contact_support_exceeds_target": len(support_rows) > ANALOG_TARGET,
        "filters": dict(filters),
        "per_cell_retained": dict(sorted(per_cell.items())),
        "retained_support_histogram": dict(sorted(support_histogram.items())),
        "representative_plus_retained": len(cells) + len(retained),
        "representative_plus_retained_exceeds_target":
            len(cells) + len(retained) > ANALOG_TARGET,
        "distinct_retained_mu": len(retained_mu),
        "retained_mu_exceeds_target": len(retained_mu) > ANALOG_TARGET,
        "zero_contact_count": len(zero_contact),
        "contact_count": len(contact),
        "contact_profile_histogram": {
            str(profile): count for profile, count in sorted(profile_histogram.items())
        },
        "contact_lambda_primitive_count": sum(
            projectively_primitive(row["lambda"]) for row in contact
        ),
        "contact_nonzero_pivot_count": sum(row["pivot"] != 0 for row in contact),
        "distinct_profile_pivot_labels": len(support_label_histogram),
        "max_profile_pivot_multiplicity": max(support_label_histogram.values()),
        "distinct_unkeyed_lambda": len(unkeyed_lambda),
        "distinct_cell_keyed_lambda": len(keyed_lambda),
        "contact_exceeds_target": len(contact) > ANALOG_TARGET,
    }


EXPECTED = {
    "parameters": {
        "p": 17,
        "r": 2,
        "t": 2,
        "beta1": 16,
        "analog_target": 34,
    },
    "occupied_cells": 16,
    "packet_count": 516,
    "packet_count_histogram": {26: 2, 27: 2, 28: 2, 29: 2, 35: 2, 37: 2, 38: 4},
    "representative_count": 16,
    "comparison_count": 500,
    "filters": {
        "nonprimitive": 13,
        "extension": 20,
        "support_collapse": 0,
        "bc_size": 4,
        "toy_pivot_vanishing": 0,
        "retained": 463,
    },
    "per_cell_retained": {
        1: 21, 2: 25, 3: 34, 4: 24,
        5: 33, 6: 34, 7: 32, 8: 24,
        9: 26, 10: 31, 11: 36, 12: 34,
        13: 25, 14: 34, 15: 27, 16: 23,
    },
    "retained_support_histogram": {5: 63, 6: 174, 7: 108, 8: 118},
    "representative_plus_retained": 479,
    "representative_plus_retained_exceeds_target": True,
    "distinct_retained_mu": 407,
    "retained_mu_exceeds_target": True,
    "zero_contact_count": 348,
    "contact_count": 115,
    "contact_profile_histogram": {"(0, 1)": 68, "(1, 0)": 47},
    "contact_support_profile_histogram": {"(0, 1)": 57, "(1, 0)": 46},
    "contact_lambda_primitive_count": 115,
    "contact_nonzero_pivot_count": 115,
    "distinct_profile_pivot_labels": 30,
    "max_profile_pivot_multiplicity": 9,
    "distinct_unkeyed_lambda": 103,
    "contact_support_count": 103,
    "contact_support_exceeds_target": True,
    "distinct_cell_keyed_lambda": 115,
    "contact_exceeds_target": True,
}


def verify(summary: Mapping[str, object]) -> None:
    require(summary["source_pins"] == SOURCE_PINS, "source pin drift")
    for key, value in EXPECTED.items():
        require(summary[key] == value, f"{key} drift")


def tamper_suite(summary: Mapping[str, object]) -> int:
    trials = [
        ("packet_count", 515),
        ("representative_count", 15),
        ("comparison_count", 499),
        ("representative_plus_retained", 478),
        ("representative_plus_retained_exceeds_target", False),
        ("distinct_retained_mu", 406),
        ("retained_mu_exceeds_target", False),
        ("zero_contact_count", 347),
        ("contact_count", 114),
        ("contact_lambda_primitive_count", 114),
        ("contact_nonzero_pivot_count", 114),
        ("distinct_profile_pivot_labels", 31),
        ("max_profile_pivot_multiplicity", 8),
        ("distinct_unkeyed_lambda", 102),
        ("contact_support_count", 102),
        ("contact_support_exceeds_target", False),
        ("distinct_cell_keyed_lambda", 114),
        ("contact_exceeds_target", False),
    ]
    detected = 0
    for key, replacement in trials:
        forged = copy.deepcopy(summary)
        forged[key] = replacement
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
        print("PASS: Route-D F17 global marked-contact pivot no-go v1")
        print(f"representatives plus retained: {summary['representative_plus_retained']}")
        print(f"nonempty contact: {summary['contact_count']}")
        print(f"analogue target: {summary['parameters']['analog_target']}")
        print(f"profile/pivot labels: {summary['distinct_profile_pivot_labels']}")
        if args.self_test:
            print(f"tamper trials: {summary['tamper_trials']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
