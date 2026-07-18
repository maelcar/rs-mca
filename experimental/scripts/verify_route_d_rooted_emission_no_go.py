#!/usr/bin/env python3
"""Verify exact no-go examples for an unrooted Route-D owner adapter."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from collections import Counter
from pathlib import Path


P = 17
DOMAIN = tuple(range(1, P))
N = 16
K = 5
AGREEMENT = 8
J = 8
R = 3
T_RANK = AGREEMENT - K
TARGET = (1, 9)
BASE = (1, 8, 10, 11, 12, 13, 14, 15)
TOGGLE_SUPPORT = (1, 3, 5, 9, 10, 11, 13, 15)
E_SMALL = (1, 3)
E_FULL = (1, 3, 5)
PUNCTURE_ERROR = (16,)
PADDING_TARGET = (0, 9)
EXPECTED_CELLS = {1: 2, 2: 1, 3: 2, 4: 1, 5: 1, 6: 2, 7: 2, 11: 2, 14: 2, 15: 2, 16: 2}
EXPECTED_PUNCTURED_CELLS = {7: 2, 11: 1, 14: 1, 15: 1, 16: 2}


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def locator_prefix(support: tuple[int, ...], depth: int = 2) -> tuple[int, ...]:
    elementary = [0] * (depth + 1)
    elementary[0] = 1
    used = 0
    for x in support:
        used = min(depth, used + 1)
        for degree in range(used, 0, -1):
            elementary[degree] = (elementary[degree] + x * elementary[degree - 1]) % P
    return tuple(((-elementary[d]) if d % 2 else elementary[d]) % P for d in range(1, depth + 1))


def locator(support: set[int]) -> tuple[int, ...]:
    coefficients = [1]
    for x in sorted(support):
        nxt = [0] * (len(coefficients) + 1)
        for degree, coefficient in enumerate(coefficients):
            nxt[degree] = (nxt[degree] - coefficient * x) % P
            nxt[degree + 1] = (nxt[degree + 1] + coefficient) % P
        coefficients = nxt
    return tuple(coefficients)


def top_seam_packet(support: tuple[int, ...]) -> dict:
    base = set(BASE)
    row = set(support)
    plus = row - base
    minus = base - row
    plus_locator = locator(plus)
    minus_locator = locator(minus)
    delta = tuple((left - right) % P for left, right in zip(plus_locator, minus_locator))
    return {
        "support": support,
        "core": tuple(sorted(row & base)),
        "plus": tuple(sorted(plus)),
        "minus": tuple(sorted(minus)),
        "delta": delta,
        "cell": delta[0],
    }


def matrix_rank_mod_p(matrix: list[list[int]]) -> int:
    rows = [[entry % P for entry in row] for row in matrix]
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((index for index in range(rank, len(rows)) if rows[index][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, P)
        rows[rank] = [(entry * inverse) % P for entry in rows[rank]]
        for index in range(len(rows)):
            if index == rank:
                continue
            factor = rows[index][column]
            rows[index] = [(left - factor * right) % P for left, right in zip(rows[index], rows[rank])]
        rank += 1
    return rank


def poly_mul(left: list[int], right: list[int]) -> list[int]:
    product = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product[i + j] = (product[i + j] + a * b) % P
    return product


def interpolate_values_on(nodes: tuple[int, ...], value_at) -> tuple[int, ...]:
    coefficients = [0] * K
    for i, xi in enumerate(nodes):
        basis = [1]
        denominator = 1
        for j, xj in enumerate(nodes):
            if i == j:
                continue
            basis = poly_mul(basis, [(-xj) % P, 1])
            denominator = denominator * (xi - xj) % P
        scale = value_at(xi) * pow(denominator, -1, P) % P
        for degree, value in enumerate(basis):
            coefficients[degree] = (coefficients[degree] + scale * value) % P
    return tuple(coefficients)


def interpolate_x5_on(nodes: tuple[int, ...], slope: int) -> tuple[int, ...]:
    return interpolate_values_on(nodes, lambda x: slope * pow(x, K, P) % P)


def eval_poly(coefficients: tuple[int, ...], x: int) -> int:
    return sum(value * pow(x, degree, P) for degree, value in enumerate(coefficients)) % P


def max_agreement_for_slope(slope: int) -> int:
    return max_agreement_for_value(
        lambda x: slope * pow(x, K, P) % P
    )


def max_agreement_for_value(value_at) -> int:
    maximum = 0
    seen: set[tuple[int, ...]] = set()
    for nodes in itertools.combinations(DOMAIN, K):
        coefficients = interpolate_values_on(nodes, value_at)
        if coefficients in seen:
            continue
        seen.add(coefficients)
        agreement = sum(
            eval_poly(coefficients, x) == value_at(x)
            for x in DOMAIN
        )
        maximum = max(maximum, agreement)
    return maximum


def hankel(error_support: tuple[int, ...]) -> list[list[int]]:
    return [
        [(-sum(pow(x, row + column + 1, P) for x in error_support)) % P for column in range(J + 1)]
        for row in range(T_RANK)
    ]


def prefix_target_stabilizer(target: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        scalar
        for scalar in DOMAIN
        if tuple(value * pow(scalar, degree, P) % P for degree, value in enumerate(target, 1)) == target
    )


def set_stabilizer(points: tuple[int, ...]) -> tuple[int, ...]:
    point_set = set(points)
    return tuple(
        scalar
        for scalar in DOMAIN
        if {scalar * point % P for point in point_set} == point_set
    )


def deconvolve_prefix(
    target: tuple[int, int], fixed_prefix: tuple[int, int]
) -> tuple[int, int]:
    padding_first = (target[0] - fixed_prefix[0]) % P
    padding_second = (
        target[1] - fixed_prefix[1] - fixed_prefix[0] * padding_first
    ) % P
    return padding_first, padding_second


def build_result() -> dict:
    root = Path(__file__).resolve().parents[2]
    owner_path = root / "experimental/data/certificates/m1-kb-branch2-rank-deep-owner-v1/m1_kb_branch2_rank_deep_owner_v1.json"
    with owner_path.open(encoding="utf-8") as handle:
        owner = json.load(handle)

    fiber = [
        support
        for support in itertools.combinations(DOMAIN, J)
        if locator_prefix(support) == TARGET
    ]
    base = set(BASE)
    mates = [
        top_seam_packet(support)
        for support in fiber
        if len(set(support) ^ base) == 2 * R
    ]
    toggle = top_seam_packet(TOGGLE_SUPPORT)
    small_matrix = hankel(E_SMALL)
    full_matrix = hankel(E_FULL)
    policy = owner["rank_drop_policy"]
    scope = owner["deep_mca_owner"]
    max_agreements = tuple(max_agreement_for_slope(slope) for slope in range(P))
    bad_slopes = tuple(slope for slope, maximum in enumerate(max_agreements) if maximum >= AGREEMENT)

    puncture_error_set = set(PUNCTURE_ERROR)
    punctured_domain = tuple(x for x in DOMAIN if x not in puncture_error_set)
    puncture_error_prefix = locator_prefix(PUNCTURE_ERROR)
    padding_target = deconvolve_prefix(TARGET, puncture_error_prefix)
    padding_choices = [
        padding
        for padding in itertools.combinations(
            punctured_domain, J - len(PUNCTURE_ERROR)
        )
        if locator_prefix(padding) == padding_target
    ]
    reconstructed_padding_supports = [
        tuple(sorted(puncture_error_set | set(padding)))
        for padding in padding_choices
    ]
    padding_fiber = [
        support for support in fiber if puncture_error_set <= set(support)
    ]
    punctured_mates = [
        top_seam_packet(support)
        for support in padding_fiber
        if len(set(support) ^ base) == 2 * R
    ]
    punctured_max_agreements = tuple(
        max_agreement_for_value(
            lambda x, slope=slope: (
                (1 if x in puncture_error_set else 0)
                + slope * pow(x, K, P)
            )
            % P
        )
        for slope in range(P)
    )
    punctured_bad_slopes = tuple(
        slope
        for slope, maximum in enumerate(punctured_max_agreements)
        if maximum >= AGREEMENT
    )
    punctured_matrix = hankel(PUNCTURE_ERROR)

    complements_force_noncontainment = all(
        len({x for x in DOMAIN if x not in set(packet["support"])}) > K
        for packet in mates
    )

    return {
        "status": "COUNTEREXAMPLE",
        "field_prime": P,
        "code_dimension": K,
        "agreement": AGREEMENT,
        "co_support_size": J,
        "rank_threshold": T_RANK,
        "owner_matrix_shape": (T_RANK, J + 1),
        "dual_weight_formula": "lambda_x=-x on F17^*",
        "deep_gate_lhs": 3 * (T_RANK - 1),
        "deep_gate_rhs": N - K,
        "deep_gate_holds": 3 * (T_RANK - 1) <= N - K,
        "fixed_direction": "g(x)=x^5",
        "fixed_codeword": "c(x)=0",
        "target": TARGET,
        "target_stabilizer": prefix_target_stabilizer(TARGET),
        "fiber_size": len(fiber),
        "top_seam_mate_count": len(mates),
        "distinct_common_core_marks": len({packet["core"] for packet in mates}),
        "cell_histogram": dict(sorted(Counter(packet["cell"] for packet in mates).items())),
        "all_top_seam_deltas_constant_nonzero": all(
            packet["cell"] != 0 and packet["delta"][1:] == (0, 0, 0)
            for packet in mates
        ),
        "root_bound_noncontained_on_every_complement": complements_force_noncontainment,
        "max_agreement_by_slope": max_agreements,
        "bad_slope_set": bad_slopes,
        "bad_slope_set_root_bound": "gamma*x^5-h has degree 5 and cannot vanish on 8 points for gamma!=0",
        "common_rank_drop_slope": 0,
        "common_rank_at_zero": 0,
        "support_witness_count": len(mates),
        "slope_times_base_field_capacity": P,
        "multiplicity_exceeds_capacity": len(mates) > P,
        "puncture_error_support": PUNCTURE_ERROR,
        "puncture_error_prefix": puncture_error_prefix,
        "padding_target": padding_target,
        "padding_target_algebraic_stabilizer": prefix_target_stabilizer(
            padding_target
        ),
        "punctured_domain": punctured_domain,
        "punctured_domain_stabilizer": set_stabilizer(punctured_domain),
        "padding_fiber_size": len(padding_fiber),
        "padding_fiber_exceeds_capacity": len(padding_fiber) > P,
        "padding_factorization_exact": sorted(padding_fiber)
        == sorted(reconstructed_padding_supports),
        "padding_choices_have_deconvolved_target": all(
            locator_prefix(padding) == padding_target
            for padding in padding_choices
        ),
        "reconstructed_supports_have_full_target": all(
            locator_prefix(support) == TARGET
            for support in reconstructed_padding_supports
        ),
        "punctured_owner_matrix": punctured_matrix,
        "punctured_actual_rank": matrix_rank_mod_p(punctured_matrix),
        "punctured_max_agreement_by_slope": punctured_max_agreements,
        "punctured_bad_slope_set": punctured_bad_slopes,
        "punctured_top_seam_mate_count": len(punctured_mates),
        "punctured_distinct_common_core_marks": len(
            {packet["core"] for packet in punctured_mates}
        ),
        "punctured_cell_histogram": dict(
            sorted(Counter(packet["cell"] for packet in punctured_mates).items())
        ),
        "punctured_top_seam_deltas_constant_nonzero": all(
            packet["cell"] != 0 and packet["delta"][1:] == (0, 0, 0)
            for packet in punctured_mates
        ),
        "toggle_packet": toggle,
        "toggle_same_displayed_support_datum": (
            TARGET,
            BASE,
            toggle["support"],
            toggle["core"],
            toggle["cell"],
        ),
        "small_error_support": E_SMALL,
        "full_error_support": E_FULL,
        "small_hankel": small_matrix,
        "full_hankel": full_matrix,
        "small_hankel_rank": matrix_rank_mod_p(small_matrix),
        "full_hankel_rank": matrix_rank_mod_p(full_matrix),
        "both_errors_inside_same_chosen_cosupport": set(E_FULL) <= set(TOGGLE_SUPPORT),
        "toggle_exact_agreement_support": tuple(x for x in DOMAIN if x not in set(TOGGLE_SUPPORT)),
        "toggle_actual_errors_equal_E2_E3": True,
        "same_line_direction_noncontained_on_toggle_complement": len(
            {x for x in DOMAIN if x not in set(TOGGLE_SUPPORT)}
        ) > K,
        "owner_contract": {
            "requires_actual_bad_incidence": policy["requires_actual_bad_incidence"],
            "raw_algebraic_rank_drop_paid": policy["raw_algebraic_rank_drop_paid"],
            "slope_set_is_support_independent": policy["slope_set_is_support_independent"],
            "theorem_object": scope["theorem_object"],
            "scope": scope["scope"],
            "per_support_charge": scope["per_support_charge"],
            "per_pivot_charge": scope["per_pivot_charge"],
        },
        "deployed_bound_refuted": False,
        "post_first_match_adapter_refuted": False,
    }


def validate(result: dict) -> int:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        ensure(condition, message)
        checks += 1

    check(result["status"] == "COUNTEREXAMPLE", "status changed")
    check(result["code_dimension"] == 5 and result["agreement"] == 8, "toy RS parameters changed")
    check(result["co_support_size"] == 8 and result["rank_threshold"] == 3, "toy owner dimensions changed")
    check(result["owner_matrix_shape"] == (3, 9), "owner matrix shape changed")
    check(result["dual_weight_formula"] == "lambda_x=-x on F17^*", "dual weights changed")
    check(result["deep_gate_lhs"] == 6 and result["deep_gate_rhs"] == 11, "deep gate arithmetic changed")
    check(result["deep_gate_holds"], "toy is outside the deep-owner gate")
    check(result["fixed_direction"] == "g(x)=x^5", "fixed line direction changed")
    check(result["fixed_codeword"] == "c(x)=0", "explaining codeword changed")
    check(result["target_stabilizer"] == (1,), "target is not primitive")
    check(result["fiber_size"] == 49, "primitive fiber size changed")
    check(result["top_seam_mate_count"] == 19, "top-seam mate count changed")
    check(result["distinct_common_core_marks"] == 19, "common-core marks collapsed")
    check(result["cell_histogram"] == EXPECTED_CELLS, "cell histogram changed")
    check(result["all_top_seam_deltas_constant_nonzero"], "a mate is not top-seam")
    check(result["root_bound_noncontained_on_every_complement"], "line became contained")
    check(result["bad_slope_set"] == (0,), "bad-slope set changed")
    check(result["max_agreement_by_slope"] == (16,) + (5,) * 16, "exact slope census changed")
    check("degree 5" in result["bad_slope_set_root_bound"], "bad-slope root bound disappeared")
    check(result["common_rank_drop_slope"] == 0 and result["common_rank_at_zero"] == 0, "common slope changed")
    check(result["support_witness_count"] == 19, "witness count changed")
    check(result["slope_times_base_field_capacity"] == 17, "capacity changed")
    check(result["multiplicity_exceeds_capacity"], "multiplicity no longer exceeds p")

    check(result["puncture_error_support"] == (16,), "puncture error changed")
    check(result["puncture_error_prefix"] == (1, 0), "puncture locator prefix changed")
    check(result["padding_target"] == PADDING_TARGET, "deconvolved padding target changed")
    check(
        result["padding_target_algebraic_stabilizer"] == (1, 16),
        "padding target algebraic stabilizer changed",
    )
    check(
        len(result["punctured_domain"]) == 15
        and 16 not in result["punctured_domain"],
        "punctured domain changed",
    )
    check(
        result["punctured_domain_stabilizer"] == (1,),
        "punctured-domain stabilizer changed",
    )
    check(result["padding_fiber_size"] == 24, "padding fiber size changed")
    check(result["padding_fiber_exceeds_capacity"], "padding fiber no longer exceeds p")
    check(result["padding_factorization_exact"], "padding round trip failed")
    check(
        result["padding_choices_have_deconvolved_target"],
        "a padding choice escaped the deconvolved target",
    )
    check(
        result["reconstructed_supports_have_full_target"],
        "a reconstructed support escaped the full target",
    )
    check(
        len(result["punctured_owner_matrix"]) == 3
        and all(len(row) == 9 for row in result["punctured_owner_matrix"]),
        "punctured owner matrix shape changed",
    )
    check(result["punctured_actual_rank"] == 1, "punctured actual rank changed")
    check(result["punctured_bad_slope_set"] == (0,), "punctured bad-slope set changed")
    check(
        result["punctured_max_agreement_by_slope"][0] == 15
        and max(result["punctured_max_agreement_by_slope"][1:]) < AGREEMENT,
        "punctured exact agreement census changed",
    )
    check(
        result["punctured_top_seam_mate_count"] == 7,
        "punctured top-seam mate count changed",
    )
    check(
        result["punctured_distinct_common_core_marks"] == 7,
        "punctured common-core marks collapsed",
    )
    check(
        result["punctured_cell_histogram"] == EXPECTED_PUNCTURED_CELLS,
        "punctured cell histogram changed",
    )
    check(
        result["punctured_top_seam_deltas_constant_nonzero"],
        "a punctured mate is not top-seam",
    )

    packet = result["toggle_packet"]
    check(packet["support"] == TOGGLE_SUPPORT, "toggle support changed")
    check(packet["core"] == (1, 10, 11, 13, 15), "toggle common core changed")
    check(packet["delta"] == (2, 0, 0, 0), "toggle top-seam cell changed")
    check(result["both_errors_inside_same_chosen_cosupport"], "error escaped chosen co-support")
    check(len(result["toggle_exact_agreement_support"]) == 8, "toggle agreement support changed")
    check(result["toggle_actual_errors_equal_E2_E3"], "toggle actual errors changed")
    check(result["same_line_direction_noncontained_on_toggle_complement"], "toggle line became contained")
    check(len(result["small_hankel"]) == 3 and all(len(row) == 9 for row in result["small_hankel"]), "small owner matrix shape changed")
    check(len(result["full_hankel"]) == 3 and all(len(row) == 9 for row in result["full_hankel"]), "full owner matrix shape changed")
    check([row[:4] for row in result["small_hankel"]] == [[13, 7, 6, 3], [7, 6, 3, 11], [6, 3, 11, 1]], "small leading block changed")
    check([row[:4] for row in result["full_hankel"]] == [[8, 16, 0, 7], [16, 0, 7, 14], [0, 7, 14, 16]], "full leading block changed")
    check(result["small_hankel_rank"] == 2, "small error is not rank-drop")
    check(result["full_hankel_rank"] == 3, "full error is not full rank")

    contract = result["owner_contract"]
    check(contract["requires_actual_bad_incidence"] is True, "owner incidence requirement changed")
    check(contract["raw_algebraic_rank_drop_paid"] is False, "owner raw pivot policy changed")
    check(contract["slope_set_is_support_independent"] is True, "owner slope scope changed")
    check(contract["theorem_object"] == "distinct finite MCA-bad slopes of one received pair", "owner object changed")
    check(contract["scope"] == "FIRST_MATCH_GLOBAL_ONCE", "owner first-match scope changed")
    check(contract["per_support_charge"] is False and contract["per_pivot_charge"] is False, "owner unit changed")
    check(result["deployed_bound_refuted"] is False, "deployed bound overclaim")
    check(result["post_first_match_adapter_refuted"] is False, "post-filter adapter overclaim")
    return checks


def mutation_test(result: dict) -> int:
    mutations = (
        ("target_stabilizer", (1, 16)),
        ("fiber_size", 48),
        ("top_seam_mate_count", 17),
        ("distinct_common_core_marks", 1),
        ("multiplicity_exceeds_capacity", False),
        ("deep_gate_holds", False),
        ("bad_slope_set", (0, 1)),
        ("padding_target", (1, 9)),
        ("padding_target_algebraic_stabilizer", (1,)),
        ("punctured_domain_stabilizer", (1, 16)),
        ("padding_fiber_size", 17),
        ("padding_fiber_exceeds_capacity", False),
        ("padding_factorization_exact", False),
        ("punctured_actual_rank", 2),
        ("punctured_bad_slope_set", (0, 1)),
        ("punctured_top_seam_mate_count", 6),
        ("punctured_distinct_common_core_marks", 1),
        ("punctured_cell_histogram", {7: 7}),
        ("small_hankel_rank", 3),
        ("full_hankel_rank", 2),
        ("deployed_bound_refuted", True),
        ("post_first_match_adapter_refuted", True),
    )
    caught = 0
    for key, value in mutations:
        bad = copy.deepcopy(result)
        bad[key] = value
        try:
            validate(bad)
        except AssertionError:
            caught += 1
    ensure(caught == len(mutations), "mutation suite did not fail closed")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    result = build_result()
    checks = validate(result)
    caught = mutation_test(result) if args.self_test else 0
    print("STATUS COUNTEREXAMPLE")
    fiber = result["fiber_size"]
    mates = result["top_seam_mate_count"]
    witnesses = result["support_witness_count"]
    capacity = result["slope_times_base_field_capacity"]
    small_rank = result["small_hankel_rank"]
    full_rank = result["full_hankel_rank"]
    print(f"primitive_fiber={fiber} top_seam_mates={mates}")
    print(f"one_slope_marked_witnesses={witnesses} capacity={capacity}")
    padding_size = result["padding_fiber_size"]
    padding_stabilizer = result["padding_target_algebraic_stabilizer"]
    punctured_stabilizer = result["punctured_domain_stabilizer"]
    print(
        f"punctured_padding={padding_size} algebraic_stabilizer={padding_stabilizer} "
        f"domain_stabilizer={punctured_stabilizer}"
    )
    print(f"same_datum_ranks={small_rank},{full_rank}")
    print(f"checks={checks} mutations_caught={caught}")
    print("minimal_repair=FIXED_LINE_MARKED_INJECTION_AFTER_EXACT_FIRST_MATCH")


if __name__ == "__main__":
    main()
