#!/usr/bin/env python3
"""Verify the Route-D pivot and marked-incidence obstruction exactly.

The checks expose an obstruction to the proposed routing closure. They do not
refute the deployed KoalaBear numerical support inequality.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from pathlib import Path


P, J, W, R = 17, 8, 2, 3
TARGET = (1, 9)
BASE = (1, 3, 5, 9, 10, 11, 13, 15)
LEFT = (1, 3, 4, 5, 6, 7, 9, 15)
RIGHT = (1, 2, 5, 8, 9, 13, 14, 15)
EXPECTED_MU = ((2, -1), (3, 1), (4, 1), (6, 1), (7, 1), (8, -1), (13, -1), (14, -1))
NAMED_DELETIONS = (
    "generated_field",
    "quotient_planted",
    "sparse_pade_hankel",
    "m1_window_shadow",
    "rank_drop_pivot",
    "bc_chart",
    "sp_shift_pair",
    "extension_slope",
)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    ensure(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def locator_prefix(support: tuple[int, ...], depth: int) -> tuple[int, ...]:
    elementary = [0] * (depth + 1)
    elementary[0] = 1
    used = 0
    for x in support:
        used = min(depth, used + 1)
        for degree in range(used, 0, -1):
            elementary[degree] = (elementary[degree] + x * elementary[degree - 1]) % P
    return tuple(((-elementary[d]) if d % 2 else elementary[d]) % P for d in range(1, depth + 1))


def monic_locator(support: tuple[int, ...]) -> tuple[int, ...]:
    coeffs = [1]
    for x in support:
        nxt = [0] * (len(coeffs) + 1)
        for degree, coeff in enumerate(coeffs):
            nxt[degree] = (nxt[degree] - coeff * x) % P
            nxt[degree + 1] = (nxt[degree + 1] + coeff) % P
        coeffs = nxt
    return tuple(coeffs)


def side_data(support: tuple[int, ...]) -> dict:
    support_set, base_set = set(support), set(BASE)
    plus = tuple(sorted(support_set - base_set))
    minus = tuple(sorted(base_set - support_set))
    core = tuple(sorted(support_set & base_set))
    delta = tuple((a - b) % P for a, b in zip(monic_locator(plus), monic_locator(minus)))
    return {"plus": plus, "minus": minus, "core": core, "delta": delta, "cell": delta[0]}


def folding_defect(support: tuple[int, ...]) -> int:
    values = set(support)
    return sum((x in values) != ((-x) % P in values) for x in range(1, 9))


def stabilizer(mu: dict[int, int]) -> tuple[int, ...]:
    return tuple(
        scalar
        for scalar in range(1, P)
        if all(mu.get(scalar * x % P, 0) == weight for x, weight in mu.items())
    )


def moments(mu: dict[int, int], through: int) -> tuple[int, ...]:
    return tuple(sum(weight * pow(x, degree, P) for x, weight in mu.items()) % P for degree in range(through + 1))


def vandermonde(points: tuple[int, ...]) -> int:
    product = 1
    for i, left in enumerate(points):
        for right in points[i + 1 :]:
            product = product * (right - left) % P
    return product


def target_stabilizer() -> tuple[int, ...]:
    return tuple(
        scalar
        for scalar in range(1, P)
        if tuple(value * pow(scalar, degree, P) % P for degree, value in enumerate(TARGET, 1)) == TARGET
    )


def fiber_size() -> int:
    return sum(1 for support in itertools.combinations(range(1, P), J) if locator_prefix(support, W) == TARGET)


def rim_products() -> tuple[int, ...]:
    matrix = (
        (1, 1, 1, 0, 0, 0),
        (1, 2, 4, 0, 0, 0),
        (0, 0, 0, 1, 4, 16),
        (0, 0, 0, 1, 13, 16),
        (1, 8, 13, -1, -8, -13),
        (1, 16, 1, -1, -16, -1),
    )
    kernel = (2, 14, 1, 3, 0, 3)
    return tuple(sum(a * b for a, b in zip(row, kernel)) % P for row in matrix)


def build_result() -> dict:
    root = Path(__file__).resolve().parents[2]
    singleton = load_json(root / "experimental/data/certificates/rowsharp-q-singleton-topseam-v1/rowsharp_q_singleton_topseam_v1.json")
    owner = load_json(root / "experimental/data/certificates/m1-kb-branch2-rank-deep-owner-v1/m1_kb_branch2_rank_deep_owner_v1.json")
    reduction = load_json(root / "experimental/data/certificates/rowsharp-q-prefix-atom-reductions-v1/rowsharp_q_prefix_atom_reductions_v1.json")

    left, right = side_data(LEFT), side_data(RIGHT)
    positive = (set(left["plus"]) | set(right["minus"])) - (set(left["minus"]) | set(right["plus"]))
    negative = (set(left["minus"]) | set(right["plus"])) - (set(left["plus"]) | set(right["minus"]))
    mu = {x: 1 for x in positive} | {x: -1 for x in negative}
    pivot_points = tuple(sorted(mu)[: R + 1])
    policy, scope = owner["rank_drop_policy"], owner["deep_mca_owner"]
    weighted = singleton["step_4_cross_pair_branch_matching"]["weighted_sp_pade_dichotomy"]
    return {
        "status": "COUNTEREXAMPLE",
        "deployed_product": 67_472 * 2_130_706_433,
        "deployed_bound_refuted": False,
        "target_stabilizer": target_stabilizer(),
        "fiber_size": fiber_size(),
        "prefixes": tuple(locator_prefix(support, W + 1) for support in (BASE, LEFT, RIGHT)),
        "folding_defects": tuple(folding_defect(support) for support in (BASE, LEFT, RIGHT)),
        "left": left,
        "right": right,
        "mu": tuple(sorted(mu.items())),
        "mu_support_size": len(mu),
        "moments": moments(mu, R + 1),
        "pivot_points": pivot_points,
        "pivot": vandermonde(pivot_points),
        "mu_stabilizer": stabilizer(mu),
        "rim_products": rim_products(),
        "named_deletion_aggregate": singleton["first_match_order"][0],
        "owner_contract": {
            "requires_actual_bad_incidence": policy["requires_actual_bad_incidence"],
            "raw_algebraic_rank_drop_paid": policy["raw_algebraic_rank_drop_paid"],
            "theorem_object": scope["theorem_object"],
            "scope": scope["scope"],
            "per_support_charge": scope["per_support_charge"],
            "per_pivot_charge": scope["per_pivot_charge"],
        },
        "weighted_status": weighted["status"],
        "weighted_key": weighted["full_rank_chart"]["injective_chart_key"],
        "weighted_remaining_count": weighted["full_rank_chart"]["remaining_count"],
        "reduction_status": reduction["status"],
    }


def validate(result: dict) -> int:
    checks = 0

    def check(condition: bool, message: str) -> None:
        nonlocal checks
        ensure(condition, message)
        checks += 1

    check(result["status"] == "COUNTEREXAMPLE", "status changed")
    check(result["deployed_product"] == 143_763_024_447_376, "deployed product changed")
    check(result["deployed_bound_refuted"] is False, "deployed bound overclaim")
    check(result["target_stabilizer"] == (1,), "target is not primitive")
    check(result["fiber_size"] == 49, "toy fiber changed")
    check(result["prefixes"] == ((1, 9, 10), (1, 9, 14), (1, 9, 14)), "prefixes changed")
    check(result["folding_defects"] == (8, 8, 4), "folding defects changed")
    check(result["left"]["delta"] == (4, 0, 0, 0), "left cell changed")
    check(result["right"]["delta"] == (4, 0, 0, 0), "right cell changed")
    check(result["left"]["core"] != result["right"]["core"], "common-core marks collapsed")
    check(result["mu"] == EXPECTED_MU, "signed defect changed")
    check(result["mu_support_size"] == 8 and result["mu_support_size"] >= R + 3, "not large WSP")
    check(result["moments"] == (0, 0, 0, 0, 10), "moments changed")
    check(result["pivot_points"] == (2, 3, 4, 6) and result["pivot"] == 14, "pivot changed")
    check(result["mu_stabilizer"] == (1,), "signed defect is quotient-periodic")
    check(result["rim_products"] == (0, 0, 0, 0, 0, 0), "RIM witness is nonsingular")

    aggregate = result["named_deletion_aggregate"]
    check(tuple(aggregate["examples"]) == NAMED_DELETIONS, "named deletion list changed")
    check(aggregate["name"] == "earlier_global_first_match_branches" and aggregate["priority"] == 0, "aggregate changed")
    check(set(aggregate) == {"examples", "name", "priority"}, "aggregate unexpectedly defines predicates")

    contract = result["owner_contract"]
    check(contract["requires_actual_bad_incidence"] is True, "owner incidence requirement changed")
    check(contract["raw_algebraic_rank_drop_paid"] is False, "owner unexpectedly pays raw pivots")
    check(contract["per_support_charge"] is False and contract["per_pivot_charge"] is False, "owner unit changed")
    check(contract["scope"] == "FIRST_MATCH_GLOBAL_ONCE", "owner scope changed")
    check(contract["theorem_object"] == "distinct finite MCA-bad slopes of one received pair", "owner object changed")
    check(result["weighted_status"] == "WEIGHTED_SP_PADE_DICHOTOMY_PROVED_FULL_RANK_PRIMITIVE_COUNT_REQUIRED", "WSP status changed")
    check("G" in result["weighted_key"], "marked core missing from key")
    check(result["weighted_remaining_count"] == "N_WSP_full(z)", "WSP remaining count changed")
    check(result["reduction_status"] == "REDUCED_NOT_PROVED", "source reduction status changed")
    return checks


def mutation_test(result: dict) -> int:
    mutations = (
        ("deployed_bound_refuted", True),
        ("fiber_size", 48),
        ("mu_support_size", 5),
        ("pivot", 0),
        ("mu_stabilizer", (1, 16)),
        ("weighted_key", "(r,c,U0,H,D,P,mu_F)"),
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
    deployed = result["deployed_product"]
    refuted = result["deployed_bound_refuted"]
    fiber = result["fiber_size"]
    pivot = result["pivot"]
    rim = result["rim_products"]
    print("STATUS COUNTEREXAMPLE")
    print(f"deployed_bound={deployed} refuted={refuted}")
    print(f"primitive_fiber={fiber} marked_cell=4 pivot={pivot}")
    print(f"rim_kernel_zero={rim} owner_raw_pivot_paid=False")
    print(f"checks={checks} mutations_caught={caught}")
    print("deployed_primitive_support_certificate=OPEN")


if __name__ == "__main__":
    main()
