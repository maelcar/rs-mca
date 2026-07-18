#!/usr/bin/env python3
"""Deterministic verifier for the Route-D F31 all-depth tree no-go.

The script reconstructs the restricted finite corpus, its full power-sum
prefix tree, canonical marked boundary packets, Rule-1 keys, Rule-2 reductions,
and the all-base-child cell-mask dynamic program from definitions.  It uses only the Python standard library.

Usage:
  python3 experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py
  python3 experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py --tamper
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
PREFIX_COMMIT = "e83962ae5ad7bacb391b691ffd37f0abef977b83"
SINGLETON_COMMIT = "84b393ec1bc52fa662756bd117a45537007d086a"
PUNCTURE_COMMIT = "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b"
ADAPTER_COMMIT = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
SOURCE_BLOBS = {
    "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
    "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
    "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
        "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "experimental/scripts/verify_rowsharp_q_prefix_atom_reductions_v1.py":
        "a2da1c0657600d7497512bfa80138e60f6c89c01",
    "experimental/data/certificates/rowsharp-q-prefix-atom-reductions-v1/"
    "rowsharp_q_prefix_atom_reductions_v1.json":
        "908ee64976b46b9d8b5bd6015dd8c031dc17df6f",
    "experimental/notes/thresholds/cap25_v13_lq_top_seam_marked_incidence.md":
        "a7f2bf4f1338d0b31d999c86a29859317033113f",
    "experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md":
        "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py":
        "dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1",
    "experimental/data/certificates/rowsharp-q-singleton-topseam-v1/"
    "rowsharp_q_singleton_topseam_v1.json":
        "6a8aa0c61eeebfa93b97e157b3bc72f8c3dce892",
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
PREFLIGHT_COMMIT = "36d560d7421dace47bf48b3fecc9389adaf0977b"
PREFLIGHT_BLOBS = {
    "experimental/notes/thresholds/route_d_rule2_wsp_algebraic_preflight_v1.md":
        "b11def86906c467fc5a1b07caf14a07108b430f6",
    "experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py":
        "a00d900f5af63babf847ebbaf4efdc2dba4babc7",
    "experimental/lean/route_d_rule2_wsp_algebraic_preflight_v1/"
    "RouteDRule2WspAlgebraicPreflightV1.lean":
        "cfbc2e4ce825247fe638e14464b085226fa403e3",
}
ROOT_COMPILER_COMMIT = "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe"
ROOT_COMPILER_BLOBS = {
    "experimental/notes/thresholds/route_d_f31_root_compiler_no_go_v1.md":
        "97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc",
    "experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py":
        "c6c78f88def94ec460fe33ac4aeb673533ad3a11",
    "experimental/lean/route_d_f31_root_compiler_no_go_v1/"
    "RouteDF31RootCompilerNoGoV1.lean":
        "86bca88e3d37c786bc0b4531c1ae96643d8ac5dd",
    "experimental/agents-log.md":
        "d45f9f0bbc5e423dba6bc70f5749996f97a91db9",
}


EXPECTED_PROVENANCE = {
    "source_commit": SOURCE_COMMIT,
    "prefix_commit": PREFIX_COMMIT,
    "singleton_commit": SINGLETON_COMMIT,
    "puncture_commit": PUNCTURE_COMMIT,
    "adapter_commit": ADAPTER_COMMIT,
    "preflight_commit": PREFLIGHT_COMMIT,
    "root_compiler_commit": ROOT_COMPILER_COMMIT,
    "source_blobs": SOURCE_BLOBS,
    "puncture_blobs": PUNCTURE_BLOBS,
    "adapter_blobs": ADAPTER_BLOBS,
    "preflight_blobs": PREFLIGHT_BLOBS,
    "root_compiler_blobs": ROOT_COMPILER_BLOBS,
}
EXPECTED_RESTRICTED_TREE = {
    "supports": 120,
    "leaves_minus_one": 119,
    "branch_buckets_by_row": {3: 1, 4: 27, 5: 9, 6: 2},
    "non_singleton_buckets_by_row": {3: 1, 4: 27, 5: 10, 6: 2},
    "outdegree_histograms": {
        3: {29: 1},
        4: {2: 6, 3: 6, 4: 6, 5: 6, 6: 2, 9: 1},
        5: {1: 1, 2: 7, 3: 2},
        6: {2: 2},
    },
    "child_size_histograms": {
        3: {1: 2, 2: 4, 3: 5, 4: 8, 5: 3, 6: 4, 7: 1, 8: 1, 9: 1},
        4: {1: 95, 2: 7, 3: 3},
        5: {1: 19, 2: 2},
        6: {1: 4},
    },
    "excess_units_by_row": {3: 28, 4: 78, 5: 11, 6: 2},
}
EXPECTED_LEX_REPLAY = {
    "boundary": 107,
    "strict": 12,
    "strict_distance_histogram": ((4, 5, 10), (4, 6, 2)),
    "primitive_boundary": 106,
    "nonprimitive_boundary": 1,
    "nonprimitive_fixture": {
        "row": 3,
        "c": 4,
        "inside": (1, 2, 3, 4, 5, 6, 7, 10, 18, 19, 20, 21, 22, 23, 26),
        "outside": (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 18, 21, 22, 26),
        "added": (19, 20, 23),
        "removed": (8, 11, 12),
        "stabilizer": ((1, 1), (30, -1)),
    },
    "rule1_duplicates": 0,
    "cell_size_histogram": {1: 26, 2: 16, 3: 9, 4: 4, 5: 1},
    "row_cell_comparisons": {
        3: {"packets": 27, "cells": 19, "comparisons": 8},
        4: {"packets": 66, "cells": 27, "comparisons": 39},
        5: {"packets": 11, "cells": 8, "comparisons": 3},
        6: {"packets": 2, "cells": 2, "comparisons": 0},
    },
    "rule2_comparisons": 50,
    "extensions": 4,
    "nonextensions": 46,
    "support_size_histogram": {8: 1, 9: 4, 10: 13, 11: 4, 12: 6, 13: 10, 14: 5, 15: 5, 16: 2},
    "ordered_comparisons": 154,
    "ordered_extensions": 10,
    "representative_choice_extensions_min": 2,
    "representative_choice_extensions_max": 5,
    "representative_choice_nonextensions_min": 45,
    "representative_choice_nonextensions_max": 48,
    "common_core_marks_preserved": True,
}
EXPECTED_ALL_BASE_CHILD_DP = {
    "primitive": {
        3: {"states": 13, "maximum_collision_surplus": 9, "witness_packets": 28, "witness_cells": 19},
        4: {"states": 6896, "maximum_collision_surplus": 45, "witness_packets": 70, "witness_cells": 25},
        5: {"states": 153, "maximum_collision_surplus": 6, "witness_packets": 11, "witness_cells": 5},
        6: {"states": 4, "maximum_collision_surplus": 0, "witness_packets": 2, "witness_cells": 2},
    },
    "all_boundary_ceiling_by_row": {3: 9, 4: 45, 5: 6, 6: 0},
    "rule2_comparison_ceiling": 60,
    "prior_fixed_base_floor": 81,
    "ceiling_strictly_below_prior_floor": True,
}
EXPECTED_ROW_BUDGET = {
    "toy_t": 3,
    "charged_rows": (3, 4, 5, 6),
    "charged_row_count": 4,
    "fits_toy_budget": False,
    "first_three_rows_excess": 117,
    "row6_excess": 2,
}
EXPECTED_OWNERSHIP = {
    "restricted_toy_called_actual_post_first_match": False,
    "named_deletions_executed": False,
    "strict_classification_called_payment": False,
    "rule2_algebraic_comparison_called_payment": False,
    "official_N_WSP_full_claimed": False,
    "deployed_bound_proved_or_refuted": False,
    "common_core_mark_preserved": True,
    "forbidden_shortcut_used": False,
}
EXPECTED_TOP_LEVEL_KEYS = {
    "schema", "status", "provenance", "restricted_tree", "lex_replay",
    "all_base_child_dp", "row_budget", "ownership",
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


def prefix_key(support: Sequence[int], depth: int) -> tuple[int, ...]:
    return tuple(power_sum(support, degree) for degree in range(1, depth + 1))


def distance(left: Sequence[int], right: Sequence[int]) -> int:
    return len(set(left) - set(right))


def canonical_child_packet(
    child: Sequence[tuple[int, ...]],
    children: Sequence[Sequence[tuple[int, ...]]],
    row: int,
    beta: tuple[int, ...],
) -> dict[str, object]:
    outside = tuple(sorted(support for other in children if other != child for support in other))
    candidates = [
        (distance(inside, other), inside, other)
        for inside in child
        for other in outside
    ]
    require(bool(candidates), "child complement is empty")
    minimum_distance = min(item[0] for item in candidates)
    inside, other = min((inside, other) for d, inside, other in candidates if d == minimum_distance)
    require(minimum_distance >= row, "prefix-distance lower bound failed")
    packet: dict[str, object] = {
        "row": row,
        "minimum_distance": minimum_distance,
        "inside": inside,
        "outside": other,
        "beta": beta,
        "boundary": minimum_distance == row,
    }
    if minimum_distance != row:
        return packet
    added = canonical(set(inside) - set(other))
    removed = canonical(set(other) - set(inside))
    core = canonical(set(inside) & set(other))
    require(len(added) == len(removed) == row, "boundary side size changed")
    u = locator(added)
    v = locator(removed)
    delta = poly_sub(u, v)
    require(len(delta) == 1 and delta[0] != 0, "boundary locator difference changed")
    c = delta[0]
    require(poly_sub(u, (c,)) == v, "U-c != V")
    require(canonical((*core, *added)) == inside, "inside common-core reconstruction failed")
    require(canonical((*core, *removed)) == other, "outside common-core reconstruction failed")
    nu = side_weight(added, removed)
    packet.update({
        "core": core,
        "added": added,
        "removed": removed,
        "U": u,
        "V": v,
        "c": c,
        "primitive": projective_signed_stabilizer(nu) == ((1, 1),),
        "stabilizer": projective_signed_stabilizer(nu),
    })
    return packet


def build_tree(universe: Sequence[tuple[int, ...]]) -> dict[str, object]:
    current = [tuple(sorted(universe))]
    depth = 2
    branch_buckets: list[dict[str, object]] = []
    all_buckets: list[dict[str, object]] = []
    while current:
        following: list[tuple[tuple[int, ...], ...]] = []
        for bucket in current:
            if len(bucket) <= 1:
                continue
            grouped: dict[int, list[tuple[int, ...]]] = defaultdict(list)
            for support in bucket:
                grouped[power_sum(support, depth + 1)].append(support)
            children = tuple(sorted(
                (tuple(sorted(group)) for group in grouped.values()),
                key=lambda group: group[0],
            ))
            row = depth + 1
            record: dict[str, object] = {
                "depth": depth,
                "row": row,
                "bucket": bucket,
                "children": children,
                "outdegree": len(children),
            }
            all_buckets.append(record)
            following.extend(child for child in children if len(child) > 1)
            if len(children) > 1:
                beta = prefix_key(bucket[0], depth)
                require(all(prefix_key(support, depth) == beta for support in bucket),
                        "bucket prefix drift")
                packets = tuple(canonical_child_packet(child, children, row, beta) for child in children)
                record["packets"] = packets
                branch_buckets.append(record)
        current = following
        depth += 1
        require(depth <= 16, "prefix tree did not terminate")
    return {"all_buckets": tuple(all_buckets), "branch_buckets": tuple(branch_buckets)}


def rule2_certificate(
    representative: Mapping[str, object], packet: Mapping[str, object]
) -> dict[str, object]:
    row = int(packet["row"])
    require(representative["row"] == row and representative["c"] == packet["c"],
            "cross-cell Rule-2 comparison")
    u0, v0 = representative["U"], representative["V"]
    u, v = packet["U"], packet["V"]
    require(all(isinstance(poly, tuple) for poly in (u0, v0, u, v)), "malformed locator")
    require(u0 != u, "Rule-2 comparison reused U")
    c = int(packet["c"])
    require(poly_sub(u0, (c,)) == v0 and poly_sub(u, (c,)) == v,
            "Rule-2 source orientation changed")
    l_plus = poly_mul(u0, v)
    l_minus = poly_mul(v0, u)
    h = poly_gcd(l_plus, l_minus)
    m_plus = poly_exact_div(l_plus, h)
    m_minus = poly_exact_div(l_minus, h)
    require(m_plus != m_minus and poly_gcd(m_plus, m_minus) == (1,),
            "Rule-2 reduction failed")
    require(len(m_plus) == len(m_minus), "Rule-2 reduced degrees differ")
    require(len(poly_sub(m_plus, m_minus)) - 1 <= len(m_plus) - 2 - row,
            "Rule-2 degree bound failed")

    a0, r0 = representative["added"], representative["removed"]
    added, removed = packet["added"], packet["removed"]
    require(all(isinstance(side, tuple) for side in (a0, r0, added, removed)),
            "malformed marked sides")
    counter: Counter[int] = Counter(a0)
    counter.update(removed)
    counter.subtract(r0)
    counter.subtract(added)
    mu = {root: coefficient for root, coefficient in counter.items() if coefficient}
    positive = tuple(sorted(root for root, coefficient in mu.items() for _ in range(coefficient)))
    negative = tuple(sorted(root for root, coefficient in mu.items() for _ in range(-coefficient)))
    require(locator(positive) == m_plus and locator(negative) == m_minus,
            "reduced signed-weight factorization failed")
    require(poly_exact_div(poly_mul(h, m_minus), v0) == u, "packet recovery failed")

    core, inside, outside = packet["core"], packet["inside"], packet["outside"]
    require(all(isinstance(item, tuple) for item in (core, inside, outside)), "mark malformed")
    require(canonical((*core, *added)) == inside, "carried G lost inside endpoint")
    require(canonical((*core, *removed)) == outside, "carried G lost outside endpoint")
    moments = tuple(signed_moment(mu, degree) for degree in range(row + 2))
    require(all(value == 0 for value in moments[:row + 1]), "Rule-2 vanishing moments changed")
    support = tuple(sorted(mu))
    vandermonde = tuple(tuple(pow(root, degree, P) for root in support) for degree in range(row + 1))
    require(len(support) >= row + 1, "reduced support too small for pivot")
    pivot_matrix = tuple(tuple(line[column] for column in range(row + 1)) for line in vandermonde)
    pivot = det_mod(pivot_matrix)
    rank = rank_mod(vandermonde)
    require(pivot != 0 and rank == row + 1, "WSP pivot lost full row rank")
    require(len(support) > row + 2, "support-collapse or BC chart appeared")
    require(projective_signed_stabilizer(mu) == ((1, 1),),
            "reduced weight is not projectively primitive")
    return {
        "row": row,
        "c": c,
        "support_size": len(support),
        "extension": moments[row + 1] == 0,
        "pivot": pivot,
        "rank": rank,
        "packet_core": core,
    }


def cell_mask(packets: Sequence[Mapping[str, object]]) -> int:
    mask = 0
    for packet in packets:
        c = int(packet["c"])
        require(1 <= c < P, "cell label left F31 nonzero range")
        mask |= 1 << (c - 1)
    return mask


def row_dp(
    buckets: Sequence[Mapping[str, object]], primitive_only: bool
) -> dict[str, int]:
    states = {0: 0}
    for bucket in buckets:
        packets = bucket["packets"]
        require(isinstance(packets, tuple), "bucket packets malformed")
        options = []
        for omitted in range(len(packets)):
            selected = tuple(
                packet for index, packet in enumerate(packets)
                if index != omitted and bool(packet["boundary"])
                and (not primitive_only or bool(packet["primitive"]))
            )
            options.append((cell_mask(selected), len(selected)))
        following: dict[int, int] = {}
        for option_mask, option_count in options:
            for old_mask, old_count in states.items():
                merged = old_mask | option_mask
                count = old_count + option_count
                if count > following.get(merged, -1):
                    following[merged] = count
        states = following
    surplus, packets, mask = max(
        (count - occupied.bit_count(), count, occupied)
        for occupied, count in states.items()
    )
    return {
        "states": len(states),
        "maximum_collision_surplus": surplus,
        "witness_packets": packets,
        "witness_cells": mask.bit_count(),
    }


def summarize() -> dict[str, object]:
    raw = make_mates()
    primitive_mate_records = primitive_mates(raw)
    universe = tuple(sorted({BASE, *(record["support"] for record in primitive_mate_records)}))
    require(len(universe) == 120, "restricted support count changed")
    tree = build_tree(universe)
    all_buckets = tree["all_buckets"]
    branch_buckets = tree["branch_buckets"]
    require(isinstance(all_buckets, tuple) and isinstance(branch_buckets, tuple), "tree malformed")

    branch_by_row: dict[int, list[dict[str, object]]] = defaultdict(list)
    all_by_row: dict[int, list[dict[str, object]]] = defaultdict(list)
    for bucket in all_buckets:
        all_by_row[int(bucket["row"])].append(bucket)
    for bucket in branch_buckets:
        branch_by_row[int(bucket["row"])].append(bucket)
    require({row: len(items) for row, items in branch_by_row.items()} == {3: 1, 4: 27, 5: 9, 6: 2},
            "branch-bucket row distribution changed")
    require({row: len(items) for row, items in all_by_row.items()} == {3: 1, 4: 27, 5: 10, 6: 2},
            "non-singleton bucket row distribution changed")
    outdegree_histograms = {
        row: dict(sorted(Counter(int(bucket["outdegree"]) for bucket in items).items()))
        for row, items in all_by_row.items()
    }
    require(outdegree_histograms == {
        3: {29: 1},
        4: {2: 6, 3: 6, 4: 6, 5: 6, 6: 2, 9: 1},
        5: {1: 1, 2: 7, 3: 2},
        6: {2: 2},
    }, "outdegree histograms changed")
    child_size_histograms = {
        row: dict(sorted(Counter(
            len(child) for bucket in items for child in bucket["children"]
        ).items()))
        for row, items in all_by_row.items()
    }
    require(child_size_histograms == {
        3: {1: 2, 2: 4, 3: 5, 4: 8, 5: 3, 6: 4, 7: 1, 8: 1, 9: 1},
        4: {1: 95, 2: 7, 3: 3},
        5: {1: 19, 2: 2},
        6: {1: 4},
    }, "child-size histograms changed")
    excess_by_row = {
        row: sum(int(bucket["outdegree"]) - 1 for bucket in items)
        for row, items in branch_by_row.items()
    }
    require(excess_by_row == {3: 28, 4: 78, 5: 11, 6: 2}, "tree excess changed")
    require(sum(excess_by_row.values()) == len(universe) - 1 == 119,
            "tree leaf/excess identity changed")

    lex_units = []
    for bucket in branch_buckets:
        packets = bucket["packets"]
        require(isinstance(packets, tuple), "lex bucket packets malformed")
        lex_units.extend(packets[1:])
    require(len(lex_units) == 119, "lex unit count changed")
    boundary = [packet for packet in lex_units if bool(packet["boundary"])]
    strict = [packet for packet in lex_units if not bool(packet["boundary"])]
    primitive_boundary = [packet for packet in boundary if bool(packet["primitive"])]
    nonprimitive = [packet for packet in boundary if not bool(packet["primitive"])]
    require((len(boundary), len(strict), len(primitive_boundary), len(nonprimitive)) == (107, 12, 106, 1),
            "lex boundary classification changed")
    strict_distance_hist = Counter((int(packet["row"]), int(packet["minimum_distance"])) for packet in strict)
    require(strict_distance_hist == Counter({(4, 5): 10, (4, 6): 2}),
            "strict-distance histogram changed")
    nonprimitive_fixture = nonprimitive[0]
    require(
        (nonprimitive_fixture["row"], nonprimitive_fixture["c"],
         nonprimitive_fixture["inside"], nonprimitive_fixture["outside"],
         nonprimitive_fixture["added"], nonprimitive_fixture["removed"],
         nonprimitive_fixture["stabilizer"])
        == (3, 4,
            (1, 2, 3, 4, 5, 6, 7, 10, 18, 19, 20, 21, 22, 23, 26),
            (1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 18, 21, 22, 26),
            (19, 20, 23), (8, 11, 12), ((1, 1), (30, -1))),
        "nonprimitive fixture changed",
    )

    rule1_keys = [
        (int(packet["row"]), int(packet["c"]), packet["U"], packet["beta"])
        for packet in boundary
    ]
    require(len(rule1_keys) == len(set(rule1_keys)) == 107, "Rule-1 duplicate appeared")
    cells: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    for packet in primitive_boundary:
        cells[(int(packet["row"]), int(packet["c"]))].append(packet)
    cell_size_histogram = dict(sorted(Counter(len(group) for group in cells.values()).items()))
    require(cell_size_histogram == {1: 26, 2: 16, 3: 9, 4: 4, 5: 1},
            "primitive cell-size histogram changed")
    row_cell_comparisons = {
        row: {
            "packets": sum(len(group) for (r, _), group in cells.items() if r == row),
            "cells": sum(1 for r, _ in cells if r == row),
            "comparisons": sum(len(group) - 1 for (r, _), group in cells.items() if r == row),
        }
        for row in (3, 4, 5, 6)
    }
    require(row_cell_comparisons == {
        3: {"packets": 27, "cells": 19, "comparisons": 8},
        4: {"packets": 66, "cells": 27, "comparisons": 39},
        5: {"packets": 11, "cells": 8, "comparisons": 3},
        6: {"packets": 2, "cells": 2, "comparisons": 0},
    }, "row cell census changed")

    lex_certificates = []
    ordered_certificates = []
    extension_ranges: dict[tuple[int, int], tuple[int, int]] = {}
    for key, group in cells.items():
        group.sort(key=lambda packet: (packet["inside"], packet["outside"]))
        lex_certificates.extend(rule2_certificate(group[0], packet) for packet in group[1:])
        per_representative = []
        for representative in group:
            certificates = [rule2_certificate(representative, packet) for packet in group if packet is not representative]
            ordered_certificates.extend(certificates)
            per_representative.append(sum(bool(certificate["extension"]) for certificate in certificates))
        extension_ranges[key] = (min(per_representative), max(per_representative))
    require(len(lex_certificates) == 50 and len(ordered_certificates) == 154,
            "Rule-2 certificate census changed")
    extensions = [certificate for certificate in lex_certificates if bool(certificate["extension"])]
    nonextensions = [certificate for certificate in lex_certificates if not bool(certificate["extension"])]
    require((len(extensions), len(nonextensions)) == (4, 46), "lex extension split changed")
    require(Counter((int(certificate["row"]), int(certificate["c"]), int(certificate["support_size"])) for certificate in extensions)
            == Counter({(4, 1, 14): 1, (4, 3, 11): 1, (4, 15, 14): 1, (4, 29, 12): 1}),
            "extension fixtures changed")
    support_histogram = dict(sorted(Counter(int(certificate["support_size"]) for certificate in lex_certificates).items()))
    require(support_histogram == {8: 1, 9: 4, 10: 13, 11: 4, 12: 6, 13: 10, 14: 5, 15: 5, 16: 2},
            "Rule-2 support histogram changed")
    minimum_extensions = sum(low for low, _ in extension_ranges.values())
    maximum_extensions = sum(high for _, high in extension_ranges.values())
    require((minimum_extensions, maximum_extensions) == (2, 5),
            "representative-choice extension range changed")
    require(sum(bool(certificate["extension"]) for certificate in ordered_certificates) == 10,
            "ordered extension count changed")

    primitive_dp = {row: row_dp(items, True) for row, items in branch_by_row.items()}
    all_boundary_dp = {row: row_dp(items, False) for row, items in branch_by_row.items()}
    require(primitive_dp == {
        3: {"states": 13, "maximum_collision_surplus": 9, "witness_packets": 28, "witness_cells": 19},
        4: {"states": 6896, "maximum_collision_surplus": 45, "witness_packets": 70, "witness_cells": 25},
        5: {"states": 153, "maximum_collision_surplus": 6, "witness_packets": 11, "witness_cells": 5},
        6: {"states": 4, "maximum_collision_surplus": 0, "witness_packets": 2, "witness_cells": 2},
    }, "primitive DP changed")
    require({row: data["maximum_collision_surplus"] for row, data in all_boundary_dp.items()}
            == {3: 9, 4: 45, 5: 6, 6: 0}, "all-boundary DP ceiling changed")
    ceiling = sum(data["maximum_collision_surplus"] for data in primitive_dp.values())
    require(ceiling == 60 and ceiling < 81, "60 < 81 no-go arithmetic changed")

    row_set = tuple(sorted(row_cell_comparisons))
    require(row_set == (3, 4, 5, 6) and len(row_set) == 4 > 3,
            "toy row-budget obstruction changed")
    require(sum(excess_by_row[row] for row in (3, 4, 5)) == 117 and excess_by_row[6] == 2,
            "first-three-row coverage changed")
    require(12 + 1 + 4 + 46 + 56 == 119, "lex partition identity changed")

    return {
        "schema": "route-d-f31-all-depth-tree-no-go-v1",
        "status": "COUNTEREXAMPLE",
        "provenance": {
            "source_commit": SOURCE_COMMIT,
            "prefix_commit": PREFIX_COMMIT,
            "singleton_commit": SINGLETON_COMMIT,
            "puncture_commit": PUNCTURE_COMMIT,
            "adapter_commit": ADAPTER_COMMIT,
            "preflight_commit": PREFLIGHT_COMMIT,
            "root_compiler_commit": ROOT_COMPILER_COMMIT,
            "source_blobs": SOURCE_BLOBS,
            "puncture_blobs": PUNCTURE_BLOBS,
            "adapter_blobs": ADAPTER_BLOBS,
            "preflight_blobs": PREFLIGHT_BLOBS,
            "root_compiler_blobs": ROOT_COMPILER_BLOBS,
        },
        "restricted_tree": {
            "supports": len(universe),
            "leaves_minus_one": 119,
            "branch_buckets_by_row": {row: len(items) for row, items in branch_by_row.items()},
            "non_singleton_buckets_by_row": {row: len(items) for row, items in all_by_row.items()},
            "outdegree_histograms": outdegree_histograms,
            "child_size_histograms": child_size_histograms,
            "excess_units_by_row": excess_by_row,
        },
        "lex_replay": {
            "boundary": len(boundary),
            "strict": len(strict),
            "strict_distance_histogram": tuple(sorted((*key, count) for key, count in strict_distance_hist.items())),
            "primitive_boundary": len(primitive_boundary),
            "nonprimitive_boundary": len(nonprimitive),
            "nonprimitive_fixture": {
                "row": nonprimitive_fixture["row"], "c": nonprimitive_fixture["c"],
                "inside": nonprimitive_fixture["inside"], "outside": nonprimitive_fixture["outside"],
                "added": nonprimitive_fixture["added"], "removed": nonprimitive_fixture["removed"],
                "stabilizer": nonprimitive_fixture["stabilizer"],
            },
            "rule1_duplicates": 0,
            "cell_size_histogram": cell_size_histogram,
            "row_cell_comparisons": row_cell_comparisons,
            "rule2_comparisons": len(lex_certificates),
            "extensions": len(extensions),
            "nonextensions": len(nonextensions),
            "support_size_histogram": support_histogram,
            "ordered_comparisons": len(ordered_certificates),
            "ordered_extensions": 10,
            "representative_choice_extensions_min": minimum_extensions,
            "representative_choice_extensions_max": maximum_extensions,
            "representative_choice_nonextensions_min": 50 - maximum_extensions,
            "representative_choice_nonextensions_max": 50 - minimum_extensions,
            "common_core_marks_preserved": True,
        },
        "all_base_child_dp": {
            "primitive": primitive_dp,
            "all_boundary_ceiling_by_row": {
                row: data["maximum_collision_surplus"] for row, data in all_boundary_dp.items()
            },
            "rule2_comparison_ceiling": ceiling,
            "prior_fixed_base_floor": 81,
            "ceiling_strictly_below_prior_floor": True,
        },
        "row_budget": {
            "toy_t": 3,
            "charged_rows": row_set,
            "charged_row_count": len(row_set),
            "fits_toy_budget": False,
            "first_three_rows_excess": 117,
            "row6_excess": 2,
        },
        "ownership": {
            "restricted_toy_called_actual_post_first_match": False,
            "named_deletions_executed": False,
            "strict_classification_called_payment": False,
            "rule2_algebraic_comparison_called_payment": False,
            "official_N_WSP_full_claimed": False,
            "deployed_bound_proved_or_refuted": False,
            "common_core_mark_preserved": True,
            "forbidden_shortcut_used": False,
        },
    }


def validate(certificate: dict[str, object]) -> None:
    require(set(certificate) == EXPECTED_TOP_LEVEL_KEYS, "top-level result block drift")
    require(certificate["schema"] == "route-d-f31-all-depth-tree-no-go-v1", "schema drift")
    require(certificate["status"] == "COUNTEREXAMPLE", "status drift")

    provenance = certificate["provenance"]
    ownership = certificate["ownership"]
    require(isinstance(provenance, dict), "provenance block missing")
    require(provenance == EXPECTED_PROVENANCE, "provenance block drift")
    require(isinstance(ownership, dict), "ownership block missing")
    require(ownership == EXPECTED_OWNERSHIP, "ownership block drift")

    for name, expected in (
        ("restricted_tree", EXPECTED_RESTRICTED_TREE),
        ("lex_replay", EXPECTED_LEX_REPLAY),
        ("all_base_child_dp", EXPECTED_ALL_BASE_CHILD_DP),
        ("row_budget", EXPECTED_ROW_BUDGET),
    ):
        block = certificate[name]
        require(isinstance(block, dict), f"{name} block missing")
        require(block == expected, f"{name} block drift")


def tamper_selftest(certificate: dict[str, object]) -> int:
    mutations = (
        (("restricted_tree", "supports"), 119),
        (("restricted_tree", "excess_units_by_row", 4), 77),
        (("restricted_tree", "branch_buckets_by_row", 5), 8),
        (("restricted_tree", "child_size_histograms", 4, 1), 94),
        (("lex_replay", "strict"), 11),
        (("lex_replay", "nonprimitive_boundary"), 0),
        (("lex_replay", "rule1_duplicates"), 1),
        (("lex_replay", "rule2_comparisons"), 49),
        (("lex_replay", "extensions"), 3),
        (("lex_replay", "ordered_comparisons"), 153),
        (("lex_replay", "ordered_extensions"), 9),
        (("lex_replay", "representative_choice_nonextensions_min"), 44),
        (("all_base_child_dp", "rule2_comparison_ceiling"), 61),
        (("all_base_child_dp", "ceiling_strictly_below_prior_floor"), False),
        (("all_base_child_dp", "all_boundary_ceiling_by_row", 4), 44),
        (("all_base_child_dp", "primitive", 4, "states"), 6895),
        (("row_budget", "charged_rows"), (3, 4, 5)),
        (("row_budget", "fits_toy_budget"), True),
        (("row_budget", "first_three_rows_excess"), 116),
        (("ownership", "named_deletions_executed"), True),
        (("ownership", "common_core_mark_preserved"), False),
        (("provenance", "preflight_commit"), "0" * 40),
        (("provenance", "root_compiler_blobs", "experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py"), "0" * 40),
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
    return len(mutations)


def exhaustive_leaf_tamper_selftest(certificate: dict[str, object]) -> int:
    leaves: list[tuple[tuple[object, ...], object]] = []

    def collect(value: object, path: tuple[object, ...] = ()) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                collect(item, (*path, key))
        else:
            leaves.append((path, value))

    collect(certificate)
    for path, value in leaves:
        candidate = copy.deepcopy(certificate)
        cursor: object = candidate
        for key in path[:-1]:
            require(isinstance(cursor, dict), "bad exhaustive tamper path")
            cursor = cursor[key]
        require(isinstance(cursor, dict), "bad exhaustive tamper leaf")
        if isinstance(value, bool):
            changed: object = not value
        elif isinstance(value, int):
            changed = value + 1
        elif isinstance(value, str):
            changed = value + "-tamper"
        elif isinstance(value, tuple):
            changed = (*value, "tamper")
        elif value is None:
            changed = "tamper"
        else:
            changed = ("tamper", repr(value))
        cursor[path[-1]] = changed
        try:
            validate(candidate)
        except CertificateError:
            continue
        raise CertificateError(f"exhaustive leaf tamper was not rejected: {path}")
    return len(leaves)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamper", action="store_true", help="run fail-closed mutation tests")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        targeted = tamper_selftest(certificate)
        exhaustive = exhaustive_leaf_tamper_selftest(certificate)
        total = targeted + exhaustive
        require((targeted, exhaustive, total) == (23, 157, 180), "tamper census changed")
        print(f"TAMPER: PASS ({total}/{total}; targeted={targeted}, exhaustive={exhaustive})")
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
