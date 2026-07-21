#!/usr/bin/env python3
"""Exact two-price occupancy compiler for the M31 transfer-cap tail."""

from __future__ import annotations

import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


WEIGHTS = {
    3: 3432, 4: 1716, 5: 1716, 6: 792, 7: 792,
    8: 330, 9: 330, 10: 120, 11: 120, 12: 36,
    13: 36, 14: 8, 15: 8, 16: 1, 17: 1,
}
BASE_RESOURCES = 12_285
PARTIAL_RESOURCES = 3_556
TAIL_BUDGET = 1_761_515


def choose2(n: int) -> int:
    return n * (n - 1) // 2


def pareto(points: set[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    """Retain points not coordinatewise dominated by a cheaper point."""
    kept: list[tuple[int, int]] = []
    best_partial = math.inf
    for base, partial in sorted(points):
        if partial < best_partial:
            kept.append((base, partial))
            best_partial = partial
    return tuple(kept)


def local_patterns(punctured: bool) -> tuple[tuple[int, int, int, int], ...]:
    """Return (points, complete blocks, base pairs, partial pairs)."""
    patterns: set[tuple[int, int, int, int]] = set()
    cap0 = 7 if punctured else 8
    for t0 in range(cap0 + 1):
        for t1 in range(9):
            for t2 in range(9):
                for t3 in range(9):
                    occ = (t0, t1, t2, t3)
                    points = sum(occ)
                    if points == 0:
                        continue
                    complete = sum(t == 8 for t in occ)
                    internal = sum(choose2(t) for t in occ)
                    inter = choose2(points) - internal
                    if punctured:
                        base = inter + choose2(t0)
                        partial = sum(choose2(t) for t in occ[1:] if t < 8)
                    else:
                        base = inter
                        partial = sum(choose2(t) for t in occ if t < 8)
                    patterns.add((points, complete, base, partial))
    return tuple(sorted(patterns))


def occupancy_frontiers() -> dict[tuple[int, int], tuple[tuple[int, int], ...]]:
    full = local_patterns(False)
    punctured = ((0, 0, 0, 0),) + local_patterns(True)

    # Up to 17 occupied full outer fibers. There are 31 available, so no
    # finite-supply restriction is active.
    states: dict[tuple[int, int, int], tuple[tuple[int, int], ...]] = {
        (0, 0, 0): ((0, 0),)
    }
    for _ in range(17):
        candidates: dict[tuple[int, int, int], set[tuple[int, int]]] = defaultdict(set)
        for key, frontier in states.items():
            candidates[key].update(frontier)
        for (blocks, points, complete), frontier in states.items():
            for lp, lc, lb, lq in full:
                key = (blocks + 1, points + lp, complete + lc)
                if key[0] > 17 or key[1] > 64 or key[2] > 4:
                    continue
                for base, partial in frontier:
                    candidates[key].add((base + lb, partial + lq))
        states = {key: pareto(values) for key, values in candidates.items()}

    combined: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for (blocks, points, complete), frontier in states.items():
        for lp, lc, lb, lq in punctured:
            h = blocks + (1 if lp else 0)
            if points + lp != 64 or complete + lc > 4 or h not in WEIGHTS:
                continue
            key = (h, complete + lc)
            for base, partial in frontier:
                combined[key].add((base + lb, partial + lq))

    expected = {(h, c) for h in WEIGHTS for c in range(5)}
    assert set(combined) == expected
    return {key: pareto(values) for key, values in combined.items()}


def normalized_constraints(
    frontiers: dict[tuple[int, int], tuple[tuple[int, int], ...]],
) -> list[tuple[Fraction, Fraction, int, int, int, int]]:
    raw: list[tuple[Fraction, Fraction, int, int, int, int]] = []
    for (h, c), points in frontiers.items():
        weight = WEIGHTS[h]
        for base, partial in points:
            raw.append((Fraction(base, weight), Fraction(partial, weight), h, c, base, partial))

    # A constraint alpha*u+beta*v>=1 is redundant if another has no larger
    # u and no larger v.
    raw.sort(key=lambda row: (row[0], row[1]))
    kept: list[tuple[Fraction, Fraction, int, int, int, int]] = []
    best_v: Fraction | None = None
    for row in raw:
        if best_v is None or row[1] < best_v:
            kept.append(row)
            best_v = row[1]
    return kept


def feasible(alpha: Fraction, beta: Fraction, constraints: list[tuple]) -> bool:
    return alpha >= 0 and beta >= 0 and all(
        alpha * row[0] + beta * row[1] >= 1 for row in constraints
    )


def optimize(constraints: list[tuple], delta_base: int, delta_partial: int) -> dict:
    cb = BASE_RESOURCES * delta_base
    cp = PARTIAL_RESOURCES * delta_partial
    candidates: list[tuple[Fraction, Fraction, tuple[int, int] | str]] = []

    if all(row[0] > 0 for row in constraints):
        alpha = max(1 / row[0] for row in constraints)
        candidates.append((alpha, Fraction(0), "beta_zero"))
    if all(row[1] > 0 for row in constraints):
        beta = max(1 / row[1] for row in constraints)
        candidates.append((Fraction(0), beta, "alpha_zero"))

    for i, left in enumerate(constraints):
        u1, v1 = left[0], left[1]
        for j in range(i + 1, len(constraints)):
            u2, v2 = constraints[j][0], constraints[j][1]
            det = u1 * v2 - u2 * v1
            if det == 0:
                continue
            alpha = (v2 - v1) / det
            beta = (u1 - u2) / det
            if feasible(alpha, beta, constraints):
                candidates.append((alpha, beta, (i, j)))

    assert candidates
    alpha, beta, source = min(candidates, key=lambda row: cb * row[0] + cp * row[1])
    objective = cb * alpha + cp * beta
    tight = [
        {
            "h": row[2], "c": row[3], "base": row[4], "partial": row[5],
            "normalized_base": str(row[0]), "normalized_partial": str(row[1]),
        }
        for row in constraints if alpha * row[0] + beta * row[1] == 1
    ]
    return {
        "delta_base": delta_base,
        "delta_partial": delta_partial,
        "alpha": str(alpha),
        "beta": str(beta),
        "exact_objective": str(objective),
        "floor_upper": objective.numerator // objective.denominator,
        "slack": TAIL_BUDGET - objective.numerator // objective.denominator,
        "source": source,
        "tight_profiles": tight,
    }


def main() -> None:
    frontiers = occupancy_frontiers()
    constraints = normalized_constraints(frontiers)

    results = {
        f"{db}_{dp}": optimize(constraints, db, dp)
        for db, dp in ((21, 1), (21, 2), (21, 3), (21, 4), (21, 5),
                       (21, 10), (21, 16),
                       (21, 21), (20, 5), (19, 8), (16, 16), (25, 25))
    }

    closing_dp_at_21 = 0
    frontier_at_21 = []
    for dp in range(1, 65):
        result = optimize(constraints, 21, dp)
        frontier_at_21.append((dp, result["floor_upper"], result["slack"]))
        if result["floor_upper"] <= TAIL_BUDGET:
            closing_dp_at_21 = dp

    payload = {
        "status": "PASS_EXACT_OPTIMAL_TWO_PRICE_OCCUPANCY_COMPILER",
        "full_outer_local_patterns": len(local_patterns(False)),
        "punctured_outer_local_patterns": len(local_patterns(True)),
        "frontier_profile_count": sum(len(value) for value in frontiers.values()),
        "nonredundant_normalized_constraints": len(constraints),
        "resource_counts": {"base": BASE_RESOURCES, "partial": PARTIAL_RESOURCES},
        "tail_budget": TAIL_BUDGET,
        "selected_codegree_results": results,
        "largest_closing_delta_partial_at_delta_base_21": closing_dp_at_21,
        "delta_base_21_frontier": frontier_at_21,
        "scope_guard": (
            "This proves an optimal linear two-price compiler over exact block occupancies. "
            "It does not prove any pair codegree bound or locator realizability beyond the "
            "occupancy caps used by the existing external quotient weight table."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
