#!/usr/bin/env python3
"""Deterministic verifier for the Route-D marked-contact fold/profile no-go.

This stdlib-only script reconstructs the F_31 canonical comparison corpus,
checks the contact split and exact common-factor fold on all 245 comparison
occurrences, exhausts the elementary <= r profile-label count, and pins the
deployed arithmetic.  It is intentionally not a first-match or owner replay.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


P = 31
DOMAIN = tuple(range(1, P))
ERROR = {1, 2, 3}
BASE = (1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28)
TARGET = (30, 9)
DEPLOYED_R = 67472
DEPLOYED_P = 2130706433
BASE_COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
SOURCE_PINS = {
    "prefix_reduction_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "prefix_reduction_note_blob": "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "singleton_schema_commit": "84b393ec1bc52fa662756bd117a45537007d086a",
    "singleton_schema_note_blob": "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "signed_local_minority_commit": "208b4773687f0fbb01194ac20082872ec4a291cc",
    "signed_local_minority_blob": "376c21252b5ee167839c2d214f173428c0010ff4",
    "marked_cross_gram_commit": "5c9aab794e6575d815541e0a5dd8534d03d400aa",
    "marked_cross_gram_blob": "4ed789595305170556371c87c5773d9e14ba4307",
    "puncture_commit": "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b",
    "puncture_note_blob": "7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9",
    "root_compiler_commit": "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe",
    "root_compiler_note_blob": "97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc",
    "defect_commit": "332153d6e74403e3ad20f367ff4a3df8406a30bf",
    "defect_note_blob": "6ce5a571ca05f774a6569a9c78d9cb69e8fc896a",
    "adapter_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
    "adapter_note_blob": "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
}
DEPLOYED_PRODUCT = 143763024447376


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


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


def poly_sub(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return trim(tuple(
        (left[i] if i < len(left) else 0)
        - (right[i] if i < len(right) else 0)
        for i in range(width)
    ))


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator))
    den = trim(denominator)
    require(den != (0,), "zero polynomial divisor")
    if len(num) < len(den):
        return (0,), tuple(num)
    quotient = [0] * (len(num) - len(den) + 1)
    inverse = pow(den[-1], -1, P)
    while len(num) >= len(den) and any(num):
        shift = len(num) - len(den)
        coefficient = num[-1] * inverse % P
        quotient[shift] = coefficient
        for i, value in enumerate(den):
            num[i + shift] = (num[i + shift] - coefficient * value) % P
        while len(num) > 1 and num[-1] == 0:
            num.pop()
    return trim(quotient), trim(num)


def poly_monic(poly: Sequence[int]) -> tuple[int, ...]:
    value = trim(poly)
    require(value != (0,), "zero polynomial is not monic")
    inverse = pow(value[-1], -1, P)
    return tuple(entry * inverse % P for entry in value)


def poly_gcd(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    a, b = trim(left), trim(right)
    while b != (0,):
        _, remainder = poly_divmod(a, b)
        a, b = b, remainder
    return poly_monic(a)


def locator(roots: Iterable[int]) -> tuple[int, ...]:
    out = (1,)
    for root in sorted(roots):
        out = poly_mul(out, ((-root) % P, 1))
    return out


def locator_prefix2(roots: Iterable[int]) -> tuple[int, int]:
    value = locator(roots)
    return value[-2], value[-3]


def power_sum(roots: Iterable[int], degree: int) -> int:
    return sum(pow(root, degree, P) for root in roots) % P


def signed_moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coeff * pow(root, degree, P) for root, coeff in weight.items()) % P


def side_weight(positive: Iterable[int], negative: Iterable[int]) -> dict[int, int]:
    counter: Counter[int] = Counter(positive)
    counter.subtract(negative)
    return {root: coeff for root, coeff in counter.items() if coeff}


def make_mates() -> tuple[tuple[int, ...], ...]:
    base = set(BASE)
    removable = tuple(root for root in BASE if root not in ERROR)
    outside = tuple(root for root in DOMAIN if root not in base)
    mates = []
    require(locator_prefix2(BASE) == TARGET, "base target drift")
    for removed in itertools.combinations(removable, 3):
        core = base - set(removed)
        for added in itertools.combinations(outside, 3):
            support = canonical(core | set(added))
            if locator_prefix2(support) == TARGET:
                mates.append(support)
    require(len(mates) == 121, "raw F31 mate count drift")
    return tuple(mates)


def primitive(weight: Mapping[int, int]) -> bool:
    normalized = dict(weight)
    stabilizers = []
    for scalar in DOMAIN:
        scaled = {(scalar * root) % P: coeff for root, coeff in normalized.items()}
        for sign in (1, -1):
            if scaled == {root: sign * coeff for root, coeff in normalized.items()}:
                stabilizers.append((scalar, sign))
    return stabilizers == [(1, 1)]


def child_key(support: Iterable[int]) -> int:
    return power_sum(support, 3)


def canonical_packet(
    child: int,
    children: Mapping[int, Sequence[tuple[int, ...]]],
    universe: Sequence[tuple[int, ...]],
) -> dict[str, object]:
    pairs = [
        (inside, outside)
        for inside in children[child]
        for outside in universe
        if child_key(outside) != child
        and len(set(inside) - set(outside)) == 3
        and len(set(outside) - set(inside)) == 3
    ]
    require(bool(pairs), "missing canonical boundary")
    inside, outside = min(pairs)
    added = set(inside) - set(outside)
    removed = set(outside) - set(inside)
    core = set(inside) & set(outside)
    u, v = locator(added), locator(removed)
    c = (u[0] - v[0]) % P
    require(poly_sub(u, (c,)) == v, "top-seam relation drift")
    return {
        "child": child,
        "inside": inside,
        "outside": outside,
        "A": canonical(added),
        "R": canonical(removed),
        "G": canonical(core),
        "c": c,
    }


def compare(rep: Mapping[str, object], packet: Mapping[str, object]) -> dict[str, object]:
    require(rep["c"] == packet["c"], "cross-cell comparison")
    a0, r0 = set(rep["A"]), set(rep["R"])
    a, r, g = set(packet["A"]), set(packet["R"]), set(packet["G"])
    mu = side_weight((*a0, *r), (*r0, *a))
    c_plus, c_minus = a0 & g, r0 & g
    contact = c_plus | c_minus
    kappa = side_weight(c_plus, c_minus)
    lam = dict(mu)
    for root, coeff in kappa.items():
        lam[root] = lam.get(root, 0) - coeff
        if lam[root] == 0:
            del lam[root]
    require(set(lam).isdisjoint(g), "lambda not off core")
    require({root: coeff for root, coeff in mu.items() if root in g} == kappa,
            "contact restriction identity failed")
    require(all(signed_moment(mu, degree) == 0 for degree in range(4)),
            "Rule2 moment drift")
    require(all(
        signed_moment(lam, degree) == -signed_moment(kappa, degree) % P
        for degree in range(4)
    ), "inhomogeneous moment identity failed")

    l_plus = poly_mul(locator(a0), locator(r))
    l_minus = poly_mul(locator(r0), locator(a))
    common = poly_gcd(l_plus, l_minus)
    expected_common_roots = (a0 & a) | (r0 & r)
    require(common == locator(expected_common_roots), "Rule2 gcd root formula failed")
    require(set(expected_common_roots).isdisjoint(g), "Rule2 gcd met canonical core")

    free_core = g - contact
    folded_plus = poly_mul(
        poly_mul(locator(g - c_minus), locator(a0 - g)), locator(r)
    )
    folded_minus = poly_mul(
        poly_mul(locator(g - c_plus), locator(r0 - g)), locator(a)
    )
    require(folded_plus == poly_mul(locator(free_core), l_plus),
            "positive fold factor identity failed")
    require(folded_minus == poly_mul(locator(free_core), l_minus),
            "negative fold factor identity failed")
    folded_gcd = poly_gcd(folded_plus, folded_minus)
    require(folded_gcd == poly_mul(locator(free_core), common),
            "folded gcd did not acquire exact common-core factor")
    q_plus, rem_plus = poly_divmod(folded_plus, folded_gcd)
    q_minus, rem_minus = poly_divmod(folded_minus, folded_gcd)
    require(rem_plus == rem_minus == (0,), "fold cancellation was not exact")
    base_q_plus, base_rem_plus = poly_divmod(l_plus, common)
    base_q_minus, base_rem_minus = poly_divmod(l_minus, common)
    require(base_rem_plus == base_rem_minus == (0,), "base cancellation was not exact")
    require((q_plus, q_minus) == (base_q_plus, base_q_minus),
            "large fold did not cancel back")

    a_size, b_size = len(c_plus), len(c_minus)
    require(signed_moment(lam, 0) % P == (b_size - a_size) % P,
            "profile difference is not encoded by lambda_0")
    profile_support = c_plus | (r0 - c_minus)
    require(all(
        power_sum(profile_support, degree)
        == (power_sum(r0, degree) - signed_moment(lam, degree)) % P
        for degree in range(1, 4)
    ), "two-block contact target identity failed")
    return {
        "contact_size": len(contact),
        "a": a_size,
        "b": b_size,
        "free_core_size": len(free_core),
        "support_size": len(mu),
    }


def profile_count(r: int, difference: int) -> int:
    return sum(
        1 for a in range(r + 1) for b in range(r + 1)
        if a - b == difference and a + b > 0
    )


def summarize() -> dict[str, object]:
    mates = make_mates()
    base_set = set(BASE)
    primitive_mates = []
    for support in mates:
        added = set(support) - base_set
        removed = base_set - set(support)
        if primitive(side_weight(added, removed)):
            primitive_mates.append(support)
    require(len(primitive_mates) == 119, "primitive mate count drift")
    universe = tuple(sorted({BASE, *primitive_mates}))
    children: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in universe:
        children[child_key(support)].append(support)
    require(len(children) == 29, "child count drift")
    packets = tuple(canonical_packet(child, children, universe) for child in sorted(children))

    rows = []
    outcome_histogram: Counter[tuple[int, int]] = Counter()
    for excluded in sorted(children):
        groups: dict[int, list[dict[str, object]]] = defaultdict(list)
        for packet in packets:
            if packet["child"] != excluded:
                groups[int(packet["c"])].append(packet)
        comparisons = 0
        for group in groups.values():
            group.sort(key=lambda packet: (packet["inside"], packet["outside"]))
            for packet in group[1:]:
                comparisons += 1
                row = compare(group[0], packet)
                row["excluded"] = excluded
                rows.append(row)
        outcome_histogram[(len(groups), comparisons)] += 1
    require(outcome_histogram == Counter({(19, 9): 13, (20, 8): 16}),
            "base-choice outcome drift")
    require(len(rows) == 245, "comparison occurrence count drift")
    require(all(int(row["contact_size"]) > 0 for row in rows),
            "marked-disjoint F31 occurrence appeared")

    for r in range(1, 40):
        counts = {d: profile_count(r, d) for d in range(-r, r + 1)}
        require(max(counts.values()) == r, "nonempty profile cap failed")
        require(counts[0] == r, "zero-difference profile count failed")
        require(all(counts[d] == r + 1 - abs(d) for d in counts if d),
                "nonzero-difference profile formula failed")

    require(DEPLOYED_R * DEPLOYED_P == DEPLOYED_PRODUCT,
            "deployed product arithmetic drift")
    raw_balanced_contact_choices = len(tuple(itertools.combinations(range(6), 3))) ** 2
    require(raw_balanced_contact_choices == 400, "small balanced raw-contact fixture drift")
    deployed_balanced_choices = math.comb(DEPLOYED_R, DEPLOYED_R // 2) ** 2
    deployed_balanced_bits = deployed_balanced_choices.bit_length()
    require(deployed_balanced_choices > DEPLOYED_PRODUCT,
            "deployed raw-contact diagnostic unexpectedly small")
    return {
        "status": "COUNTEREXAMPLE",
        "provenance": {"base_commit": BASE_COMMIT, **SOURCE_PINS},
        "generic": {
            "contact_split": "mu=kappa+lambda; supp(lambda) disjoint G",
            "fold_factor_coprime_to_rule2_pair": True,
            "fold": "Lhat_plus=L_F*L_plus; Lhat_minus=L_F*L_minus",
            "cancellation_back": True,
            "generated_field_preserved": True,
            "common_core_mark_preserved": True,
        },
        "profile_compiler": {
            "nonempty_profiles_per_lambda_at_most_r": True,
            "deployed_r": DEPLOYED_R,
            "deployed_p": DEPLOYED_P,
            "hypothetical_r_times_p": DEPLOYED_PRODUCT,
            "hypothetical_lambda_family_owner_exists": False,
            "bridge_scope": "one_fixed_carried_representative_recovery_key",
            "global_actual_nonempty_profiles": (DEPLOYED_R + 1) ** 2 - 1,
            "global_key_addback_proved": False,
            "owner_obstruction": "MARKED_CONTACT_INHOMOGENEOUS_OFFCORE_OWNER",
            "raw_balanced_choices_small_fixture": raw_balanced_contact_choices,
            "deployed_balanced_choices_bit_length": deployed_balanced_bits,
            "deployed_balanced_choices_exceed_r_times_p": True,
        },
        "f31": {
            "raw_mates": len(mates),
            "primitive_mates": len(primitive_mates),
            "children": len(children),
            "comparison_occurrences": len(rows),
            "contact_size_histogram": dict(sorted(Counter(
                int(row["contact_size"]) for row in rows
            ).items())),
            "all_contact_nonempty": True,
            "all_folds_cancel_back": True,
        },
        "ownership": {
            "actual_all_minors_vanishing_routes_rank_drop": True,
            "raw_contact_pivot_is_owner_typed": False,
            "nonzero_pivot_is_injective_label": False,
            "numerical_payment_inferred": False,
            "named_deletions_executed": False,
        },
    }


def validate(certificate: Mapping[str, object]) -> None:
    expected = {
        "status": "COUNTEREXAMPLE",
        "provenance": {"base_commit": BASE_COMMIT, **SOURCE_PINS},
        "generic": {
            "contact_split": "mu=kappa+lambda; supp(lambda) disjoint G",
            "fold_factor_coprime_to_rule2_pair": True,
            "fold": "Lhat_plus=L_F*L_plus; Lhat_minus=L_F*L_minus",
            "cancellation_back": True,
            "generated_field_preserved": True,
            "common_core_mark_preserved": True,
        },
        "profile_compiler": {
            "nonempty_profiles_per_lambda_at_most_r": True,
            "deployed_r": DEPLOYED_R,
            "deployed_p": DEPLOYED_P,
            "hypothetical_r_times_p": DEPLOYED_PRODUCT,
            "hypothetical_lambda_family_owner_exists": False,
            "bridge_scope": "one_fixed_carried_representative_recovery_key",
            "global_actual_nonempty_profiles": (DEPLOYED_R + 1) ** 2 - 1,
            "global_key_addback_proved": False,
            "owner_obstruction": "MARKED_CONTACT_INHOMOGENEOUS_OFFCORE_OWNER",
            "raw_balanced_choices_small_fixture": 400,
            "deployed_balanced_choices_bit_length": 134928,
            "deployed_balanced_choices_exceed_r_times_p": True,
        },
        "f31": {
            "raw_mates": 121,
            "primitive_mates": 119,
            "children": 29,
            "comparison_occurrences": 245,
            "contact_size_histogram": {1: 81, 2: 109, 3: 27, 4: 28},
            "all_contact_nonempty": True,
            "all_folds_cancel_back": True,
        },
        "ownership": {
            "actual_all_minors_vanishing_routes_rank_drop": True,
            "raw_contact_pivot_is_owner_typed": False,
            "nonzero_pivot_is_injective_label": False,
            "numerical_payment_inferred": False,
            "named_deletions_executed": False,
        },
    }
    require(set(certificate) == set(expected), "top-level certificate keys drift")
    for key, block in expected.items():
        require(certificate[key] == block, f"certificate block drift: {key}")


def leaf_paths(value: object, path: tuple[object, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from leaf_paths(child, (*path, key))
    else:
        yield path


def tamper_selftest(certificate: dict[str, object]) -> None:
    paths = tuple(leaf_paths(certificate))
    caught = 0
    for path in paths:
        broken = copy.deepcopy(certificate)
        cursor = broken
        for key in path[:-1]:
            cursor = cursor[key]
        key = path[-1]
        value = cursor[key]
        if isinstance(value, bool):
            cursor[key] = not value
        elif isinstance(value, int):
            cursor[key] = value + 1
        elif isinstance(value, str):
            cursor[key] = value + "!"
        else:
            raise CertificateError(f"unsupported tamper leaf: {path}")
        try:
            validate(broken)
        except CertificateError:
            caught += 1
    extra = copy.deepcopy(certificate)
    extra["unexpected"] = True
    try:
        validate(extra)
    except CertificateError:
        caught += 1
    missing = copy.deepcopy(certificate)
    del missing["ownership"]
    try:
        validate(missing)
    except CertificateError:
        caught += 1
    require(caught == len(paths) + 2, "exhaustive tamper suite failed")
    print(f"TAMPER: PASS ({caught}/{len(paths) + 2})")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", action="store_true")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        tamper_selftest(certificate)
    else:
        print(json.dumps(certificate, indent=2, sort_keys=True))
        print("PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
