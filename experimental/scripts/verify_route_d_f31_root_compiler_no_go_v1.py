#!/usr/bin/env python3
"""Deterministic verifier for the Route-D F31 root-compiler no-go.

The script reconstructs the finite corpus, depth-three children, canonical
boundary packets, Rule-1 keys, Rule-2 reductions, and overlap diagnostics from
definitions.  It uses only the Python standard library.

Usage:
  python3 experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py
  python3 experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py --tamper
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


P = 31
DOMAIN = tuple(range(1, P))
ERROR = {1, 2, 3}
BASE = (1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28)
TARGET = (30, 9)

SOURCE_COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
PUNCTURE_COMMIT = "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b"
ADAPTER_COMMIT = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
SOURCE_BLOBS = {
    "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
    "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
    "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
        "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md":
        "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py":
        "dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1",
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


def poly_sub(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0) - (right[i] if i < len(right) else 0)
        for i in range(width)
    ])


def poly_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return trim(result)


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator))
    den = trim(denominator)
    require(den != (0,), "polynomial division by zero")
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
    loc = locator(support)
    return loc[-2], loc[-3]


def power_sum(support: Iterable[int], degree: int) -> int:
    return sum(pow(root, degree, P) for root in support) % P


def signed_moment(weight: Mapping[int, int], degree: int) -> int:
    return sum(coeff * pow(root, degree, P) for root, coeff in weight.items()) % P


def det_mod(matrix: Sequence[Sequence[int]]) -> int:
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant input is not square")
    work = [[entry % P for entry in row] for row in matrix]
    result = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result % P
        value = work[column][column]
        result = result * value % P
        inverse = pow(value, -1, P)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % P
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[column])
                ]
    return result


def rank_mod(matrix: Sequence[Sequence[int]]) -> int:
    if not matrix:
        return 0
    work = [[entry % P for entry in row] for row in matrix]
    width = len(work[0])
    rank = 0
    for column in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, P)
        work[rank] = [value * inverse % P for value in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def projective_signed_stabilizer(
    weight: Mapping[int, int]
) -> tuple[tuple[int, int], ...]:
    normalized = {root: coeff for root, coeff in weight.items() if coeff}
    answers: list[tuple[int, int]] = []
    for scalar in range(1, P):
        scaled = {(scalar * root) % P: coeff for root, coeff in normalized.items()}
        for sign in (1, -1):
            signed = {root: sign * coeff for root, coeff in normalized.items()}
            if scaled == signed:
                answers.append((scalar, sign))
    return tuple(answers)


def side_weight(positive: Sequence[int], negative: Sequence[int]) -> dict[int, int]:
    result: Counter[int] = Counter(positive)
    result.subtract(negative)
    return {root: coeff for root, coeff in result.items() if coeff}


def make_mates() -> tuple[dict[str, object], ...]:
    base_set = set(BASE)
    removable = tuple(root for root in BASE if root not in ERROR)
    outside = tuple(root for root in DOMAIN if root not in base_set)
    records: list[dict[str, object]] = []
    require(locator_prefix2(BASE) == TARGET, "base target changed")
    for removed in itertools.combinations(removable, 3):
        core = tuple(root for root in BASE if root not in removed)
        for added in itertools.combinations(outside, 3):
            support = canonical((*core, *added))
            if locator_prefix2(support) != TARGET:
                continue
            nu = side_weight(added, removed)
            nu3 = signed_moment(nu, 3)
            c = (locator(added)[0] - locator(removed)[0]) % P
            require(c != 0, "zero top-seam label appeared")
            require(c == -nu3 * pow(3, -1, P) % P, "Newton orientation changed")
            require(poly_sub(locator(added), (c,)) == locator(removed), "U-c != V")
            records.append({
                "support": support,
                "core": core,
                "added": canonical(added),
                "removed": canonical(removed),
                "nu": nu,
            })
    require(len(records) == 121, "mate count changed")
    return tuple(records)


def primitive_mates(records: Sequence[dict[str, object]]) -> tuple[dict[str, object], ...]:
    primitive = []
    for record in records:
        nu = record["nu"]
        require(isinstance(nu, dict), "bad raw packet weight")
        if projective_signed_stabilizer(nu) == ((1, 1),):
            primitive.append(record)
    require(len(primitive) == 119, "primitive mate count changed")
    return tuple(primitive)


def child_key(support: Sequence[int]) -> int:
    """Depth-three child key P_3; Phi_2 is already fixed."""
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
    require(bool(pairs), f"child {child} has no distance-three boundary packet")
    inside, outside = min(pairs)
    added = canonical(set(inside) - set(outside))
    removed = canonical(set(outside) - set(inside))
    core = canonical(set(inside) & set(outside))
    u = locator(added)
    v = locator(removed)
    c = (u[0] - v[0]) % P
    require(len(added) == len(removed) == 3, "boundary side size changed")
    require(poly_sub(u, (c,)) == v, "canonical packet is not top seam")
    require((child_key(inside) - child_key(outside)) % P == -3 * c % P,
            "Newton child/cell relation changed")
    require(canonical((*core, *added)) == inside, "inside common-core reconstruction failed")
    require(canonical((*core, *removed)) == outside, "outside common-core reconstruction failed")
    return {
        "child": child,
        "inside": inside,
        "outside": outside,
        "core": core,
        "added": added,
        "removed": removed,
        "c": c,
    }


def rule2_certificate(
    representative: Mapping[str, object], packet: Mapping[str, object]
) -> dict[str, object]:
    require(representative["c"] == packet["c"], "cross-cell Rule-2 comparison")
    a0 = representative["added"]
    r0 = representative["removed"]
    added = packet["added"]
    removed = packet["removed"]
    require(all(isinstance(side, tuple) for side in (a0, r0, added, removed)),
            "malformed packet side")
    u0 = locator(a0)
    v0 = locator(r0)
    u = locator(added)
    v = locator(removed)
    c = int(packet["c"])
    require(poly_sub(u0, (c,)) == v0 and poly_sub(u, (c,)) == v,
            "Rule-2 source orientation changed")
    l_plus = poly_mul(u0, v)
    l_minus = poly_mul(v0, u)
    h = poly_gcd(l_plus, l_minus)
    m_plus = poly_exact_div(l_plus, h)
    m_minus = poly_exact_div(l_minus, h)
    require(m_plus != m_minus, "reduced Rule-2 sides became identical")
    require(poly_gcd(m_plus, m_minus) == (1,), "reduced sides are not coprime")
    require(len(m_plus) == len(m_minus), "reduced sides have unequal degree")
    require(len(poly_sub(m_plus, m_minus)) - 1 <= len(m_plus) - 5,
            "Rule-2 degree bound failed")

    mu_counter: Counter[int] = Counter(a0)
    mu_counter.update(removed)
    mu_counter.subtract(r0)
    mu_counter.subtract(added)
    mu = {root: coeff for root, coeff in mu_counter.items() if coeff}
    positive = tuple(sorted(root for root, coeff in mu.items() for _ in range(coeff)))
    negative = tuple(sorted(root for root, coeff in mu.items() for _ in range(-coeff)))
    require(locator(positive) == m_plus, "positive reduced weight factorization failed")
    require(locator(negative) == m_minus, "negative reduced weight factorization failed")
    require(poly_exact_div(poly_mul(h, m_minus), v0) == u, "packet recovery failed")

    core = packet["core"]
    inside = packet["inside"]
    outside = packet["outside"]
    require(isinstance(core, tuple) and isinstance(inside, tuple) and isinstance(outside, tuple),
            "common-core mark malformed")
    require(canonical((*core, *added)) == inside, "carried G lost the inside endpoint")
    require(canonical((*core, *removed)) == outside, "carried G lost the outside endpoint")

    moments = tuple(signed_moment(mu, degree) for degree in range(5))
    require(moments[:4] == (0, 0, 0, 0), "Rule-2 moments mu_0..mu_3 changed")
    support = tuple(sorted(mu))
    vandermonde = tuple(
        tuple(pow(root, degree, P) for root in support)
        for degree in range(4)
    )
    pivot_matrix = tuple(tuple(row[column] for column in range(4)) for row in vandermonde)
    pivot = det_mod(pivot_matrix)
    require(pivot != 0 and rank_mod(vandermonde) == 4, "WSP pivot lost full row rank")
    require(projective_signed_stabilizer(mu) == ((1, 1),),
            "reduced weight is not projectively primitive")
    return {
        "cell": (3, c),
        "representative_child": representative["child"],
        "packet_child": packet["child"],
        "packet_core": core,
        "support_size": len(support),
        "moments_0_through_4": moments,
        "extension": moments[4] == 0,
        "pivot": pivot,
        "rank": 4,
        "representative_anchor_intersection_with_packet_core": canonical((set(a0) | set(r0)) & set(core)),
    }


def grouped_replay(
    packets: Sequence[dict[str, object]], excluded_child: int
) -> dict[str, object]:
    selected = [packet for packet in packets if packet["child"] != excluded_child]
    require(len(selected) == 28, "root packet count changed")
    rule1_keys = [
        (3, packet["c"], locator(packet["added"]), TARGET)
        for packet in selected
    ]
    require(len(rule1_keys) == len(set(rule1_keys)), "Rule-1 key duplicate appeared")
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for packet in selected:
        groups[int(packet["c"])].append(packet)
    certificates: list[dict[str, object]] = []
    for group in groups.values():
        group.sort(key=lambda packet: (packet["inside"], packet["outside"]))
        certificates.extend(rule2_certificate(group[0], packet) for packet in group[1:])
    require(len(certificates) == 28 - len(groups), "Rule-2 comparison identity failed")
    require(all(not bool(certificate["extension"]) for certificate in certificates),
            "extension comparison appeared")
    return {
        "excluded_child": excluded_child,
        "conditional_toy_canonical_packets": len(selected),
        "rule1_key_duplicates": 0,
        "cells": len(groups),
        "cell_size_histogram": dict(sorted(Counter(len(group) for group in groups.values()).items())),
        "algebraic_same_cell_comparisons": len(certificates),
        "extensions": 0,
        "nonextension_projectively_primitive": len(certificates),
        "support_size_histogram": dict(sorted(Counter(
            int(certificate["support_size"]) for certificate in certificates
        ).items())),
        "moment4_multiset": tuple(sorted(
            int(certificate["moments_0_through_4"][4]) for certificate in certificates
        )),
        "pivot_multiset": tuple(sorted(int(certificate["pivot"]) for certificate in certificates)),
        "common_core_marks_preserved": all(bool(certificate["packet_core"]) for certificate in certificates),
        "anchor_core_intersection_sizes": tuple(sorted(len(certificate["representative_anchor_intersection_with_packet_core"]) for certificate in certificates)),
    }


def summarize() -> dict[str, object]:
    raw = make_mates()
    primitive = primitive_mates(raw)
    universe = tuple(sorted({BASE, *(record["support"] for record in primitive)}))
    require(len(universe) == 120, "restricted parent support count changed")
    children: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in universe:
        children[child_key(support)].append(support)
    require(len(children) == 29, "depth-three child count changed")
    require(child_key(BASE) == 17 and children[17] == [BASE], "base-support child changed")
    require(len({child_key(record["support"]) for record in primitive}) == 28,
            "primitive mate child count changed")

    packets = tuple(
        canonical_boundary_packet(child, children, universe)
        for child in sorted(children)
    )
    deterministic_base_child = child_key(universe[0])
    require(deterministic_base_child == 2, "support-lex toy base child changed")
    toy = grouped_replay(packets, deterministic_base_child)
    require(toy["cells"] == 20 and toy["algebraic_same_cell_comparisons"] == 8,
            "support-lex root replay changed")
    require(toy["cell_size_histogram"] == {1: 13, 2: 6, 3: 1},
            "support-lex cell histogram changed")
    require(toy["support_size_histogram"] == {9: 1, 10: 5, 11: 2},
            "support-lex reduced-support histogram changed")
    require(toy["moment4_multiset"] == (9, 10, 11, 18, 21, 25, 25, 28),
            "support-lex fourth moments changed")
    require(toy["pivot_multiset"] == (3, 11, 14, 17, 17, 23, 27, 28),
            "support-lex pivots changed")
    require(toy["anchor_core_intersection_sizes"] == (1, 2, 2, 2, 2, 3, 4, 4),
            "support-lex anchor/core intersections changed")

    all_base_replays = tuple(grouped_replay(packets, child) for child in sorted(children))
    outcome_histogram = Counter((int(replay["cells"]), int(replay["algebraic_same_cell_comparisons"])) for replay in all_base_replays)
    require(outcome_histogram == Counter({(19, 9): 13, (20, 8): 16}),
            "all-base outcome histogram changed")
    require({int(replay["cells"]) for replay in all_base_replays} == {19, 20},
            "all-base cell range changed")
    require({int(replay["algebraic_same_cell_comparisons"]) for replay in all_base_replays} == {8, 9},
            "all-base Rule-2 range changed")
    require(all(replay["extensions"] == 0 for replay in all_base_replays),
            "all-base extension range changed")

    mate_children: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for record in primitive:
        mate_children[child_key(record["support"])].append(record["support"])
    require(17 not in mate_children and len(mate_children) == 28,
            "forced-B mate children changed")
    forced_packets = []
    for child in sorted(mate_children):
        inside = min(mate_children[child])
        added = canonical(set(inside) - set(BASE))
        removed = canonical(set(BASE) - set(inside))
        require(len(added) == len(removed) == 3, "forced-B side size changed")
        c = (locator(added)[0] - locator(removed)[0]) % P
        forced_packets.append((child, c, inside, BASE))
    require(len({packet[1] for packet in forced_packets}) == 28,
            "forced-B cells ceased to be injective")
    require(all(packet[3] == BASE for packet in forced_packets),
            "forced-B outside anchor changed")

    truncation_packets = tuple(
        sum(min(len(supports), level) for supports in mate_children.values())
        for level in range(1, 7)
    )
    require(truncation_packets == (28, 55, 78, 96, 106, 113),
            "overlap truncation sums changed")
    truncation_comparisons = tuple(total - 28 for total in truncation_packets)
    require(truncation_comparisons == (0, 27, 50, 68, 78, 85),
            "overlap comparison diagnostics changed")
    require(28 + 81 == 109 and truncation_packets[4] < 109 <= truncation_packets[5],
            "six-layer threshold arithmetic changed")

    return {
        "schema": "route-d-f31-root-compiler-no-go-v1",
        "status": "COUNTEREXAMPLE",
        "provenance": {
            "source_commit": SOURCE_COMMIT,
            "puncture_commit": PUNCTURE_COMMIT,
            "adapter_commit": ADAPTER_COMMIT,
            "source_blobs": SOURCE_BLOBS,
            "puncture_blobs": PUNCTURE_BLOBS,
            "adapter_blobs": ADAPTER_BLOBS,
        },
        "restricted_parent": {
            "raw_mates": len(raw),
            "primitive_mates": len(primitive),
            "supports_with_base": len(universe),
            "primitive_mate_children": len(mate_children),
            "children_with_base": len(children),
            "base_support_child": child_key(BASE),
            "root_units_for_any_base_child": 28,
        },
        "support_lex_toy_replay": toy,
        "all_base_child_replays": {
            "choices": len(all_base_replays),
            "outcome_histogram": ((19, 9, 13), (20, 8, 16)),
            "cells_min": min(int(replay["cells"]) for replay in all_base_replays),
            "cells_max": max(int(replay["cells"]) for replay in all_base_replays),
            "comparisons_min": min(int(replay["algebraic_same_cell_comparisons"]) for replay in all_base_replays),
            "comparisons_max": max(int(replay["algebraic_same_cell_comparisons"]) for replay in all_base_replays),
            "extensions_min": 0,
            "extensions_max": 0,
            "all_reduced_weights_projectively_primitive": True,
        },
        "forced_base_anchor_diagnostic": {
            "packets": len(forced_packets),
            "distinct_cells": len({packet[1] for packet in forced_packets}),
            "algebraic_same_cell_comparisons": 0,
            "common_outside_endpoint": BASE,
        },
        "unit_multiplicity_diagnostic": {
            "root_units_in_one_29_child_parent": 28,
            "cells_for_forced_base_anchor": 28,
            "comparisons_sought": 81,
            "packets_needed_at_fixed_28_cells": 109,
            "one_child_partition_can_supply_109_distinct_units": False,
            "overlap_truncation_packets_L1_through_L6": truncation_packets,
            "overlap_truncation_comparisons_L1_through_L6": truncation_comparisons,
            "first_level_reaching_81": 6,
        },
        "ownership": {
            "all_119_raw_marked_packets_are_distinct_branch_excess_units": False,
            "named_map_supplies_packet_multiplicity": False,
            "conditional_toy_replay_called_actual_residual": False,
            "priority0_survival_claimed": False,
            "named_deletions_executed_in_predecessor": False,
            "common_core_mark_preserved": True,
            "generated_field_changed": False,
            "deployed_bound_refuted": False,
        },
    }


def validate(certificate: dict[str, object]) -> None:
    require(certificate["schema"] == "route-d-f31-root-compiler-no-go-v1", "schema drift")
    require(certificate["status"] == "COUNTEREXAMPLE", "status drift")
    provenance = certificate["provenance"]
    require(isinstance(provenance, dict), "provenance missing")
    require(provenance["source_commit"] == SOURCE_COMMIT, "source commit drift")
    require(provenance["puncture_commit"] == PUNCTURE_COMMIT, "puncture commit drift")
    require(provenance["adapter_commit"] == ADAPTER_COMMIT, "adapter commit drift")
    require(provenance["source_blobs"] == SOURCE_BLOBS, "source blobs drift")
    require(provenance["puncture_blobs"] == PUNCTURE_BLOBS, "puncture blobs drift")
    require(provenance["adapter_blobs"] == ADAPTER_BLOBS, "adapter blobs drift")
    parent = certificate["restricted_parent"]
    toy = certificate["support_lex_toy_replay"]
    ranges = certificate["all_base_child_replays"]
    forced = certificate["forced_base_anchor_diagnostic"]
    anchor = certificate["unit_multiplicity_diagnostic"]
    ownership = certificate["ownership"]
    require(isinstance(parent, dict) and parent["primitive_mates"] == 119, "parent census drift")
    require(parent["primitive_mate_children"] == 28 and parent["children_with_base"] == 29,
            "child census drift")
    require(parent["root_units_for_any_base_child"] == 28, "root-unit identity drift")
    require(isinstance(toy, dict) and toy["excluded_child"] == 2, "toy order drift")
    require(toy["cells"] == 20 and toy["algebraic_same_cell_comparisons"] == 8,
            "toy Rule-2 census drift")
    require(toy["extensions"] == 0 and toy["nonextension_projectively_primitive"] == 8,
            "toy classification drift")
    require(toy["anchor_core_intersection_sizes"] == (1, 2, 2, 2, 2, 3, 4, 4),
            "anchor/core intersection drift")
    require(isinstance(ranges, dict) and ranges["choices"] == 29, "base-choice range missing")
    require(ranges["outcome_histogram"] == ((19, 9, 13), (20, 8, 16)),
            "base-choice outcome histogram drift")
    require((ranges["cells_min"], ranges["cells_max"]) == (19, 20), "cell range drift")
    require((ranges["comparisons_min"], ranges["comparisons_max"]) == (8, 9),
            "comparison range drift")
    require((ranges["extensions_min"], ranges["extensions_max"]) == (0, 0),
            "extension range drift")
    require(ranges["all_reduced_weights_projectively_primitive"] is True,
            "primitivity range drift")
    require(isinstance(forced, dict) and forced["packets"] == 28, "forced anchor drift")
    require(forced["distinct_cells"] == 28 and forced["algebraic_same_cell_comparisons"] == 0,
            "forced anchor cell drift")
    require(isinstance(anchor, dict) and anchor["packets_needed_at_fixed_28_cells"] == 109,
            "anchor lower bound drift")
    require(anchor["overlap_truncation_packets_L1_through_L6"] == (28, 55, 78, 96, 106, 113),
            "truncation packet drift")
    require(anchor["first_level_reaching_81"] == 6, "truncation threshold drift")
    require(anchor["one_child_partition_can_supply_109_distinct_units"] is False,
            "false one-parent multiplicity claim")
    require(isinstance(ownership, dict), "ownership block missing")
    require(all(ownership[key] is False for key in (
        "all_119_raw_marked_packets_are_distinct_branch_excess_units",
        "named_map_supplies_packet_multiplicity",
        "conditional_toy_replay_called_actual_residual",
        "priority0_survival_claimed",
        "named_deletions_executed_in_predecessor",
        "generated_field_changed",
        "deployed_bound_refuted",
    )), "false ownership or promotion claim")
    require(ownership["common_core_mark_preserved"] is True, "common-core mark lost")


def tamper_selftest(certificate: dict[str, object]) -> None:
    mutations = (
        (("restricted_parent", "children_with_base"), 28),
        (("support_lex_toy_replay", "algebraic_same_cell_comparisons"), 9),
        (("support_lex_toy_replay", "extensions"), 1),
        (("support_lex_toy_replay", "anchor_core_intersection_sizes"), (0, 2, 2, 2, 2, 3, 4, 4)),
        (("all_base_child_replays", "comparisons_min"), 7),
        (("all_base_child_replays", "outcome_histogram"), ((19, 9, 12), (20, 8, 17))),
        (("unit_multiplicity_diagnostic", "packets_needed_at_fixed_28_cells"), 108),
        (("unit_multiplicity_diagnostic", "first_level_reaching_81"), 5),
        (("ownership", "named_deletions_executed_in_predecessor"), True),
        (("ownership", "common_core_mark_preserved"), False),
        (("provenance", "adapter_commit"), "0" * 40),
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
    parser.add_argument("--tamper", action="store_true", help="run fail-closed mutation tests")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        tamper_selftest(certificate)
        print("TAMPER: PASS")
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
