#!/usr/bin/env python3
"""Deterministic verifier for the Route-D marked-defect transfer no-go.

The script reconstructs the exact F_31 root-comparison corpus, checks the
canonical-core contact identity, audits all base-child choices, verifies that
common-core intersection cancels back to the unique degree-three boundary
decomposition, and exhausts every weighted-Vandermonde maximal minor.

It uses only the Python standard library.
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

BASE_COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
ROOT_COMPILER_COMMIT = "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe"
PUNCTURE_COMMIT = "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b"
ADAPTER_COMMIT = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
ROOT_COMPILER_BLOBS = {
    "experimental/notes/thresholds/route_d_f31_root_compiler_no_go_v1.md":
        "97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc",
    "experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py":
        "c6c78f88def94ec460fe33ac4aeb673533ad3a11",
    "experimental/lean/route_d_f31_root_compiler_no_go_v1/"
    "RouteDF31RootCompilerNoGoV1.lean":
        "86bca88e3d37c786bc0b4531c1ae96643d8ac5dd",
}
SOURCE_BLOBS = {
    "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
        "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md":
        "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "experimental/notes/thresholds/signed_local_minority_fixed_composition.md":
        "376c21252b5ee167839c2d214f173428c0010ff4",
    "experimental/notes/roadmaps/marked_exclusion_cross_gram.md":
        "4ed789595305170556371c87c5773d9e14ba4307",
    "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
    "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
}
PUNCTURE_BLOBS = {
    "experimental/notes/thresholds/route_d_marked_puncture_contact_recursion_v1.md":
        "7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9",
    "experimental/scripts/verify_route_d_marked_puncture_contact_recursion_v1.py":
        "d6bb3cb7e8177d3c52eb245e4f7e142ea3250734",
    "experimental/lean/route_d_marked_puncture_contact_recursion_v1/"
    "RouteDMarkedPunctureContactRecursionV1.lean":
        "81d736e0e398210d552ecf307a1abc36702bc520",
}
ADAPTER_BLOBS = {
    "experimental/notes/thresholds/route_d_marked_rim_all_minors_adapter_v1.md":
        "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
    "experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py":
        "ace3e859b917ae87eeffb8c0e7c37155520e311e",
    "experimental/lean/route_d_marked_rim_all_minors_adapter_v1/"
    "RouteDMarkedRimAllMinorsAdapterV1.lean":
        "78e46c6ab97d97191c567041f81a6ca05e76cf41",
}


class CertificateError(RuntimeError):
    """Fail-closed verification error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def trim(poly: Sequence[int]) -> tuple[int, ...]:
    values = [value % P for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return trim(result)


def poly_sub(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0)
        - (right[i] if i < len(right) else 0)
        for i in range(width)
    ])


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator))
    den = trim(denominator)
    require(den != (0,), "division by zero polynomial")
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


def poly_exact_div(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[int, ...]:
    quotient, remainder = poly_divmod(numerator, denominator)
    require(remainder == (0,), "non-exact polynomial division")
    return quotient


def poly_monic(poly: Sequence[int]) -> tuple[int, ...]:
    value = trim(poly)
    require(value != (0,), "zero polynomial has no monic normalization")
    inverse = pow(value[-1], -1, P)
    return tuple(entry * inverse % P for entry in value)


def poly_gcd(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    a = trim(left)
    b = trim(right)
    while b != (0,):
        _, remainder = poly_divmod(a, b)
        a, b = b, remainder
    return poly_monic(a)


def locator(support: Sequence[int]) -> tuple[int, ...]:
    result = (1,)
    for root in support:
        result = poly_mul(result, ((-root) % P, 1))
    return result


def locator_prefix2(support: Sequence[int]) -> tuple[int, int]:
    value = locator(support)
    return value[-2], value[-3]


def power_sum(support: Iterable[int], degree: int) -> int:
    return sum(pow(root, degree, P) for root in support) % P


def signed_moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coeff * pow(root, degree, P) for root, coeff in weight.items()) % P


def det_mod(matrix: Sequence[Sequence[int]]) -> int:
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant input not square")
    work = [[entry % P for entry in row] for row in matrix]
    answer = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer % P
        value = work[column][column]
        answer = answer * value % P
        inverse = pow(value, -1, P)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % P
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return answer


def side_weight(positive: Sequence[int], negative: Sequence[int]) -> dict[int, int]:
    result: Counter[int] = Counter(positive)
    result.subtract(negative)
    return {root: coeff for root, coeff in result.items() if coeff}


def projective_signed_stabilizer(
    weight: Mapping[int, int]
) -> tuple[tuple[int, int], ...]:
    normalized = {root: coeff for root, coeff in weight.items() if coeff}
    answers = []
    for scalar in range(1, P):
        scaled = {(scalar * root) % P: coeff for root, coeff in normalized.items()}
        for sign in (1, -1):
            signed = {root: sign * coeff for root, coeff in normalized.items()}
            if scaled == signed:
                answers.append((scalar, sign))
    return tuple(answers)


def fixed_subgroup(prefix: tuple[int, int]) -> tuple[int, ...]:
    a1, a2 = prefix
    return tuple(
        scalar for scalar in range(1, P)
        if scalar * a1 % P == a1 and scalar * scalar * a2 % P == a2
    )


def make_mates() -> tuple[dict[str, object], ...]:
    base_set = set(BASE)
    removable = tuple(root for root in BASE if root not in ERROR)
    outside = tuple(root for root in DOMAIN if root not in base_set)
    records = []
    require(locator_prefix2(BASE) == TARGET, "base target changed")
    for removed in itertools.combinations(removable, 3):
        core = tuple(root for root in BASE if root not in removed)
        for added in itertools.combinations(outside, 3):
            support = canonical((*core, *added))
            if locator_prefix2(support) != TARGET:
                continue
            weight = side_weight(added, removed)
            c = (locator(added)[0] - locator(removed)[0]) % P
            require(c != 0, "zero top-seam cell appeared")
            require(poly_sub(locator(added), (c,)) == locator(removed), "U-c != V")
            records.append({
                "support": support,
                "core": core,
                "added": canonical(added),
                "removed": canonical(removed),
                "weight": weight,
            })
    require(len(records) == 121, "raw mate count changed")
    return tuple(records)


def primitive_mates(records: Sequence[dict[str, object]]) -> tuple[dict[str, object], ...]:
    primitive = []
    for record in records:
        weight = record["weight"]
        require(isinstance(weight, dict), "malformed raw weight")
        if projective_signed_stabilizer(weight) == ((1, 1),):
            primitive.append(record)
    require(len(primitive) == 119, "primitive mate count changed")
    return tuple(primitive)


def child_key(support: Sequence[int]) -> int:
    return power_sum(support, 3)


def canonical_boundary_packet(
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
    require(bool(pairs), f"child {child} has no boundary packet")
    inside, outside = min(pairs)
    added = canonical(set(inside) - set(outside))
    removed = canonical(set(outside) - set(inside))
    core = canonical(set(inside) & set(outside))
    u = locator(added)
    v = locator(removed)
    c = (u[0] - v[0]) % P
    require(poly_sub(u, (c,)) == v, "canonical top-seam relation changed")
    require(canonical((*core, *added)) == inside, "inside reconstruction failed")
    require(canonical((*core, *removed)) == outside, "outside reconstruction failed")
    return {
        "child": child,
        "inside": inside,
        "outside": outside,
        "core": core,
        "added": added,
        "removed": removed,
        "c": c,
    }


def comparison_data(
    representative: Mapping[str, object], packet: Mapping[str, object]
) -> dict[str, object]:
    require(representative["c"] == packet["c"], "cross-cell comparison")
    a0 = representative["added"]
    r0 = representative["removed"]
    added = packet["added"]
    removed = packet["removed"]
    require(all(isinstance(side, tuple) for side in (a0, r0, added, removed)),
            "malformed packet side")
    counter: Counter[int] = Counter(a0)
    counter.update(removed)
    counter.subtract(r0)
    counter.subtract(added)
    mu = {root: coeff for root, coeff in counter.items() if coeff}
    require(tuple(signed_moment(mu, degree) for degree in range(4)) == (0, 0, 0, 0),
            "Rule-2 moments changed")
    require(signed_moment(mu, 4) != 0, "extension comparison appeared")
    require(projective_signed_stabilizer(mu) == ((1, 1),),
            "reduced weight lost projective primitivity")
    return {
        "mu": mu,
        "support": tuple(sorted(mu)),
        "moment4": signed_moment(mu, 4),
    }


def maximal_minor_census(mu: Mapping[int, int]) -> tuple[int, int]:
    support = tuple(sorted(mu))
    total = 0
    nonzero = 0
    for columns in itertools.combinations(support, 4):
        matrix = tuple(
            tuple(mu[root] * pow(root, degree, P) % P for root in columns)
            for degree in range(4)
        )
        total += 1
        nonzero += det_mod(matrix) != 0
    return total, nonzero


def actual_incidence_hankel_census() -> dict[str, object]:
    error = set(ERROR)
    syndrome_values = tuple(
        sum(((-root) % P) * pow(root, degree, P) * int(root in error)
            for root in DOMAIN) % P
        for degree in range(18)
    )
    matrix = tuple(
        tuple(syndrome_values[row + column] for column in range(16))
        for row in range(3)
    )
    minors = tuple(
        det_mod(tuple(tuple(matrix[row][column] for column in columns)
                      for row in range(3)))
        for columns in itertools.combinations(range(16), 3)
    )
    nonzero = sum(value != 0 for value in minors)
    rank = 3 if nonzero else 0
    require(len(minors) == 560 and nonzero == 541 and rank == 3,
            "actual-incidence Hankel census changed")
    return {
        "actual_incidence_hankel_rank": rank,
        "actual_incidence_hankel_maximal_minors": len(minors),
        "actual_incidence_hankel_nonzero_maximal_minors": nonzero,
        "actual_incidence_hankel_all_minors_vanish": all(value == 0 for value in minors),
    }


def summarize() -> dict[str, object]:
    raw = make_mates()
    primitive = primitive_mates(raw)
    universe = tuple(sorted({BASE, *(record["support"] for record in primitive)}))
    require(len(universe) == 120, "restricted support universe changed")
    children: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in universe:
        children[child_key(support)].append(support)
    require(len(children) == 29, "child count changed")
    packets = tuple(
        canonical_boundary_packet(child, children, universe)
        for child in sorted(children)
    )
    packet_by_child = {int(packet["child"]): packet for packet in packets}

    subgroup_rows = []
    for packet in packets:
        added = packet["added"]
        require(isinstance(added, tuple), "malformed side for subgroup")
        subgroup_rows.append((
            int(packet["child"]), int(packet["c"]), fixed_subgroup(locator_prefix2(added))
        ))
    require(Counter(len(row[2]) for row in subgroup_rows) == Counter({1: 28, 2: 1}),
            "canonical side fixed-subgroup census changed")
    require([row for row in subgroup_rows if len(row[2]) > 1] == [(21, 4, (1, 30))],
            "unique nontrivial side subgroup changed")
    require(Counter(int(packet["c"]) for packet in packets)[4] == 1,
            "nontrivial c=4 side cell is no longer singleton")

    occurrences = []
    outcome_histogram: Counter[tuple[int, int]] = Counter()
    for excluded_child in sorted(children):
        selected = [packet for packet in packets if packet["child"] != excluded_child]
        groups: dict[int, list[dict[str, object]]] = defaultdict(list)
        for packet in selected:
            groups[int(packet["c"])].append(packet)
        comparisons = 0
        for c, group in sorted(groups.items()):
            group.sort(key=lambda packet: (packet["inside"], packet["outside"]))
            representative = group[0]
            for packet in group[1:]:
                comparisons += 1
                data = comparison_data(representative, packet)
                mu = data["mu"]
                require(isinstance(mu, dict), "malformed comparison weight")
                g0 = set(representative["core"])
                core = set(packet["core"])
                a0 = set(representative["added"])
                r0 = set(representative["removed"])
                added = set(packet["added"])
                removed = set(packet["removed"])

                require(not (added & core) and not (removed & core),
                        "packet side meets its canonical core")
                restricted = {root: mu[root] for root in core if root in mu}
                expected = {root: 1 for root in a0 & core}
                expected.update({root: -1 for root in r0 & core})
                require(restricted == expected, "generic restriction identity failed")
                contact = (a0 | r0) & core
                require((set(mu) & core) == contact, "marked-disjointness iff failed")
                require(bool(contact), "marked-disjoint canonical comparison appeared")

                common = g0 & core
                require(not (set(mu) & common), "common-core intersection meets defect")
                packet_inside = set(packet["inside"])
                packet_outside = set(packet["outside"])
                require(core == packet_inside & packet_outside, "canonical core not unique")
                require(added == packet_inside - packet_outside, "canonical added side not unique")
                require(removed == packet_outside - packet_inside, "canonical removed side not unique")

                leftover = canonical(core - common)
                inside_residual = canonical(packet_inside - common)
                outside_residual = canonical(packet_outside - common)
                require(poly_gcd(locator(inside_residual), locator(outside_residual)) == locator(leftover),
                        "intersection re-marking common factor changed")
                require(poly_exact_div(locator(inside_residual), locator(leftover)) == locator(tuple(sorted(added))),
                        "intersection re-marking did not cancel to A")
                require(poly_exact_div(locator(outside_residual), locator(leftover)) == locator(tuple(sorted(removed))),
                        "intersection re-marking did not cancel to R")
                residual_difference = poly_sub(
                    locator(inside_residual), locator(outside_residual)
                )
                expected_difference = poly_mul((int(packet["c"]),), locator(leftover))
                require(residual_difference == expected_difference,
                        "intersection re-marking shift factor changed")
                require(len(leftover) > 0 and len(residual_difference) - 1 == len(leftover),
                        "intersection re-marking unexpectedly stayed constant-shift")

                side_prefix = locator_prefix2(tuple(sorted(added)))
                side_group = fixed_subgroup(side_prefix)
                require(side_group == (1,), "compared packet has nontrivial side subgroup")
                representative_added = representative["added"]
                require(isinstance(representative_added, tuple),
                        "malformed representative side for subgroup")
                representative_group = fixed_subgroup(locator_prefix2(representative_added))
                require(representative_group == (1,),
                        "comparison representative has nontrivial side subgroup")
                require(int(representative["child"]) != 21 and int(packet["child"]) != 21,
                        "unique nontrivial side packet entered a comparison role")
                require(c != 4, "singleton nontrivial side cell entered a comparison")
                require(not set(mu).isdisjoint(core), "defect unexpectedly legal as padding off G")

                occurrences.append({
                    "excluded_child": excluded_child,
                    "c": c,
                    "representative_child": int(representative["child"]),
                    "packet_child": int(packet["child"]),
                    "a0_core": canonical(a0 & core),
                    "r0_core": canonical(r0 & core),
                    "contact_size": len(contact),
                    "common_core_size": len(common),
                    "support_size": len(data["support"]),
                    "moment4": int(data["moment4"]),
                    "mu": tuple(sorted(mu.items())),
                })
        require(comparisons == 28 - len(groups), "comparison/cell identity changed")
        outcome_histogram[(len(groups), comparisons)] += 1

    require(outcome_histogram == Counter({(19, 9): 13, (20, 8): 16}),
            "all-base outcome histogram changed")
    require(len(occurrences) == 245, "all-base comparison occurrence count changed")
    unique = {
        (row["c"], row["representative_child"], row["packet_child"]): row
        for row in occurrences
    }
    require(len(unique) == 11, "distinct comparison count changed")

    base_rows = [row for row in occurrences if row["excluded_child"] == 2]
    require(len(base_rows) == 8, "support-lex comparison count changed")
    base_fixtures = tuple(
        (
            row["c"], row["representative_child"], row["packet_child"],
            row["a0_core"], row["r0_core"], row["contact_size"]
        )
        for row in base_rows
    )
    expected_fixtures = (
        (3, 22, 25, (12, 18), (11, 28), 4),
        (6, 14, 16, (7,), (19,), 2),
        (14, 23, 19, (21,), (7, 11, 18), 4),
        (21, 1, 12, (19, 20), (7,), 3),
        (22, 30, 29, (21,), (12,), 2),
        (22, 30, 15, (21, 29), (), 2),
        (28, 11, 8, (28,), (21,), 2),
        (30, 5, 6, (), (11,), 1),
    )
    require(base_fixtures == expected_fixtures, "exact eight fixtures changed")

    minor_cache = {}
    for key, row in unique.items():
        mu = dict(row["mu"])
        total, nonzero = maximal_minor_census(mu)
        require(total == nonzero, f"vanishing maximal minor appeared at {key}")
        require(total == math.comb(int(row["support_size"]), 4), "minor count changed")
        minor_cache[key] = total
    base_minor_total = sum(
        minor_cache[(row["c"], row["representative_child"], row["packet_child"])]
        for row in base_rows
    )
    occurrence_minor_total = sum(
        minor_cache[(row["c"], row["representative_child"], row["packet_child"])]
        for row in occurrences
    )
    unique_minor_total = sum(minor_cache.values())
    require((base_minor_total, occurrence_minor_total, unique_minor_total) ==
            (1836, 59022, 2706), "maximal-minor totals changed")

    actual_hankel = actual_incidence_hankel_census()

    parent_group = fixed_subgroup(TARGET)
    punctured_group = fixed_subgroup((0, 9))
    require(parent_group == (1,), "primitive parent fixed subgroup changed")
    require(punctured_group == (1, 30), "punctured child fixed subgroup changed")
    require(all(int(row["c"]) != 0 and (-int(row["c"])) % P != int(row["c"])
                for row in occurrences), "minus-one unexpectedly preserves a comparison cell")

    return {
        "schema": "route-d-marked-defect-transfer-no-go-v1",
        "status": "COUNTEREXAMPLE",
        "provenance": {
            "base_commit": BASE_COMMIT,
            "root_compiler_commit": ROOT_COMPILER_COMMIT,
            "puncture_commit": PUNCTURE_COMMIT,
            "adapter_commit": ADAPTER_COMMIT,
            "root_compiler_blobs": ROOT_COMPILER_BLOBS,
            "source_blobs": SOURCE_BLOBS,
            "puncture_blobs": PUNCTURE_BLOBS,
            "adapter_blobs": ADAPTER_BLOBS,
        },
        "restricted_parent": {
            "raw_mates": len(raw),
            "primitive_mates": len(primitive),
            "supports_with_base": len(universe),
            "children_with_base": len(children),
        },
        "generic_transfer": {
            "restriction_identity": "mu|G=1_(A0_inter_G)-1_(R0_inter_G)",
            "marked_disjoint_iff_anchor_disjoint": True,
            "endpoint_disjoint_decomposition_unique": True,
            "canonical_common_core_mark_preserved": True,
        },
        "support_lex_base_child_2": {
            "comparisons": len(base_rows),
            "fixtures": base_fixtures,
            "contact_size_multiset": tuple(sorted(row["contact_size"] for row in base_rows)),
            "support_size_histogram": dict(sorted(Counter(
                row["support_size"] for row in base_rows
            ).items())),
            "marked_disjoint": 0,
        },
        "all_base_choices": {
            "choices": len(children),
            "outcome_histogram": ((19, 9, 13), (20, 8, 16)),
            "comparison_occurrences": len(occurrences),
            "distinct_comparisons": len(unique),
            "contact_size_histogram": dict(sorted(Counter(
                row["contact_size"] for row in occurrences
            ).items())),
            "marked_disjoint_occurrences": 0,
            "common_core_intersection_size_histogram": dict(sorted(Counter(
                row["common_core_size"] for row in occurrences
            ).items())),
            "support_size_histogram": dict(sorted(Counter(
                row["support_size"] for row in occurrences
            ).items())),
        },
        "intersection_remarking": {
            "common_intersection_is_defect_disjoint": True,
            "common_intersection_is_canonical_packet_mark": False,
            "residual_common_factor_cancels_back": True,
            "residual_difference_is_c_times_leftover_locator": True,
            "residual_difference_is_nonconstant": True,
            "preserves_degree_three_top_seam_after_remarking": False,
        },
        "puncture_and_fixed_subgroup": {
            "parent_target_stabilizer": parent_group,
            "punctured_child_stabilizer": punctured_group,
            "canonical_side_subgroup_size_histogram": {1: 28, 2: 1},
            "unique_nontrivial_side_packet": (21, 4, (1, 30)),
            "compared_side_stabilizers_trivial": True,
            "puncture_boundary_for_compared_side_targets_empty": True,
            "minus_one_preserves_parent_target_and_cell": False,
        },
        "maximal_minors": {
            "support_lex_total": base_minor_total,
            "support_lex_nonzero": base_minor_total,
            "all_occurrences_total": occurrence_minor_total,
            "all_occurrences_nonzero": occurrence_minor_total,
            "distinct_comparisons_total": unique_minor_total,
            "distinct_comparisons_nonzero": unique_minor_total,
            "vanishing_maximal_minor_families": 0,
            "routed_to_existing_rank_drop_owner": 0,
            "matrix_is_existing_actual_incidence_hankel": False,
            "raw_vanishing_family_owner_eligible_without_adapter": False,
            **actual_hankel,
        },
        "ownership": {
            "conditional_toy_packets_only": True,
            "named_deletions_executed": False,
            "post_deletion_residual_claimed": False,
            "deployed_bound_refuted": False,
            "generated_field_changed": False,
            "new_owner_or_charge_created": False,
        },
    }


def validate(certificate: dict[str, object]) -> None:
    require(certificate["schema"] == "route-d-marked-defect-transfer-no-go-v1",
            "schema drift")
    require(certificate["status"] == "COUNTEREXAMPLE", "status drift")
    provenance = certificate["provenance"]
    require(isinstance(provenance, dict), "provenance missing")
    require(provenance["base_commit"] == BASE_COMMIT, "base commit drift")
    require(provenance["root_compiler_commit"] == ROOT_COMPILER_COMMIT,
            "root compiler commit drift")
    require(provenance["root_compiler_blobs"] == ROOT_COMPILER_BLOBS,
            "root compiler blobs drift")
    parent = certificate["restricted_parent"]
    generic = certificate["generic_transfer"]
    base = certificate["support_lex_base_child_2"]
    all_base = certificate["all_base_choices"]
    remarking = certificate["intersection_remarking"]
    subgroup = certificate["puncture_and_fixed_subgroup"]
    minors = certificate["maximal_minors"]
    ownership = certificate["ownership"]
    require(isinstance(parent, dict) and
            (parent["raw_mates"], parent["primitive_mates"],
             parent["supports_with_base"], parent["children_with_base"]) ==
            (121, 119, 120, 29), "restricted parent drift")
    require(isinstance(generic, dict) and
            generic["marked_disjoint_iff_anchor_disjoint"] is True and
            generic["endpoint_disjoint_decomposition_unique"] is True and
            generic["canonical_common_core_mark_preserved"] is True,
            "generic transfer theorem drift")
    require(isinstance(base, dict) and base["comparisons"] == 8 and
            base["contact_size_multiset"] == (1, 2, 2, 2, 2, 3, 4, 4) and
            base["support_size_histogram"] == {9: 1, 10: 5, 11: 2} and
            base["marked_disjoint"] == 0, "support-lex fixture drift")
    require(isinstance(all_base, dict) and all_base["choices"] == 29 and
            all_base["comparison_occurrences"] == 245 and
            all_base["distinct_comparisons"] == 11 and
            all_base["contact_size_histogram"] == {1: 81, 2: 109, 3: 27, 4: 28} and
            all_base["marked_disjoint_occurrences"] == 0 and
            all_base["common_core_intersection_size_histogram"] == {7: 55, 8: 55, 9: 135} and
            all_base["support_size_histogram"] == {9: 27, 10: 136, 11: 82},
            "all-base contact census drift")
    require(isinstance(remarking, dict) and
            remarking["common_intersection_is_defect_disjoint"] is True and
            remarking["common_intersection_is_canonical_packet_mark"] is False and
            remarking["residual_common_factor_cancels_back"] is True and
            remarking["residual_difference_is_c_times_leftover_locator"] is True and
            remarking["residual_difference_is_nonconstant"] is True and
            remarking["preserves_degree_three_top_seam_after_remarking"] is False,
            "intersection re-marking classification drift")
    require(isinstance(subgroup, dict) and subgroup["parent_target_stabilizer"] == (1,) and
            subgroup["punctured_child_stabilizer"] == (1, 30) and
            subgroup["compared_side_stabilizers_trivial"] is True and
            subgroup["minus_one_preserves_parent_target_and_cell"] is False,
            "fixed-subgroup classification drift")
    require(isinstance(minors, dict) and
            (minors["support_lex_total"], minors["support_lex_nonzero"]) == (1836, 1836) and
            (minors["all_occurrences_total"], minors["all_occurrences_nonzero"]) ==
            (59022, 59022) and
            (minors["distinct_comparisons_total"], minors["distinct_comparisons_nonzero"]) ==
            (2706, 2706) and minors["vanishing_maximal_minor_families"] == 0 and
            minors["routed_to_existing_rank_drop_owner"] == 0 and
            minors["matrix_is_existing_actual_incidence_hankel"] is False and
            minors["raw_vanishing_family_owner_eligible_without_adapter"] is False and
            minors["actual_incidence_hankel_rank"] == 3 and
            minors["actual_incidence_hankel_maximal_minors"] == 560 and
            minors["actual_incidence_hankel_nonzero_maximal_minors"] == 541 and
            minors["actual_incidence_hankel_all_minors_vanish"] is False,
            "maximal-minor census drift")
    require(isinstance(ownership, dict) and ownership["conditional_toy_packets_only"] is True,
            "toy scope lost")
    require(all(ownership[key] is False for key in (
        "named_deletions_executed", "post_deletion_residual_claimed",
        "deployed_bound_refuted", "generated_field_changed", "new_owner_or_charge_created",
    )), "false promotion or ownership claim")


def tamper_selftest(certificate: dict[str, object]) -> None:
    mutations = (
        (("restricted_parent", "primitive_mates"), 118),
        (("generic_transfer", "marked_disjoint_iff_anchor_disjoint"), False),
        (("support_lex_base_child_2", "comparisons"), 9),
        (("support_lex_base_child_2", "marked_disjoint"), 1),
        (("all_base_choices", "comparison_occurrences"), 244),
        (("all_base_choices", "distinct_comparisons"), 12),
        (("all_base_choices", "contact_size_histogram"), {0: 1, 1: 80, 2: 109, 3: 27, 4: 28}),
        (("intersection_remarking", "common_intersection_is_canonical_packet_mark"), True),
        (("intersection_remarking", "residual_difference_is_nonconstant"), False),
        (("puncture_and_fixed_subgroup", "parent_target_stabilizer"), (1, 30)),
        (("maximal_minors", "all_occurrences_nonzero"), 59021),
        (("maximal_minors", "routed_to_existing_rank_drop_owner"), 1),
        (("maximal_minors", "matrix_is_existing_actual_incidence_hankel"), True),
        (("maximal_minors", "actual_incidence_hankel_rank"), 2),
        (("maximal_minors", "actual_incidence_hankel_nonzero_maximal_minors"), 0),
        (("maximal_minors", "actual_incidence_hankel_all_minors_vanish"), True),
        (("ownership", "named_deletions_executed"), True),
        (("ownership", "generated_field_changed"), True),
        (("provenance", "root_compiler_commit"), "0" * 40),
    )
    for path, value in mutations:
        candidate = copy.deepcopy(certificate)
        cursor: object = candidate
        for key in path[:-1]:
            require(isinstance(cursor, dict), "bad tamper path")
            cursor = cursor[key]
        require(isinstance(cursor, dict), "bad tamper leaf")
        cursor[path[-1]] = value
        try:
            validate(candidate)
        except CertificateError:
            continue
        raise CertificateError(f"tamper was not rejected: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamper", action="store_true", help="run fail-closed mutations")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        tamper_selftest(certificate)
        print("TAMPER: PASS (19/19)")
    else:
        print(json.dumps(certificate, sort_keys=True, separators=(",", ":")))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
