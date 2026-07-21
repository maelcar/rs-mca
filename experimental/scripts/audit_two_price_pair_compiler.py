#!/usr/bin/env python3
"""Independent scalar-DP audit of the two-price occupancy compiler."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


WEIGHTS = {
    3: 3432, 4: 1716, 5: 1716, 6: 792, 7: 792,
    8: 330, 9: 330, 10: 120, 11: 120, 12: 36,
    13: 36, 14: 8, 15: 8, 16: 1, 17: 1,
}
A_NUM = 2244
P_NUM = 45342
DEN = 599


def c2(n: int) -> int:
    return n * (n - 1) // 2


def cheapest_local(punctured: bool) -> dict[tuple[int, int], tuple[int, int, int, tuple[int, ...]]]:
    """Minimize A_NUM*base+P_NUM*partial for each (points, complete)."""
    caps = (7, 8, 8, 8) if punctured else (8, 8, 8, 8)
    result: dict[tuple[int, int], tuple[int, int, int, tuple[int, ...]]] = {}
    for occ in itertools.product(*(range(cap + 1) for cap in caps)):
        points = sum(occ)
        if points == 0:
            continue
        complete = sum(t == 8 for t in occ)
        internal = sum(c2(t) for t in occ)
        inter = c2(points) - internal
        if punctured:
            base = inter + c2(occ[0])
            partial = sum(c2(t) for t in occ[1:] if t < 8)
        else:
            base = inter
            partial = sum(c2(t) for t in occ if t < 8)
        cost = A_NUM * base + P_NUM * partial
        key = (points, complete)
        old = result.get(key)
        candidate = (cost, base, partial, occ)
        if old is None or candidate < old:
            result[key] = candidate
    return result


def main() -> None:
    full = cheapest_local(False)
    punctured = cheapest_local(True)

    # State value is (scaled cost, base, partial, tuple of local occupancies).
    states: dict[tuple[int, int, int], tuple[int, int, int, tuple]] = {
        (0, 0, 0): (0, 0, 0, ())
    }
    for _ in range(17):
        updated = dict(states)
        for (blocks, points, complete), value in states.items():
            for (lp, lc), local in full.items():
                key = (blocks + 1, points + lp, complete + lc)
                if key[0] > 17 or key[1] > 64 or key[2] > 4:
                    continue
                candidate = (
                    value[0] + local[0], value[1] + local[1],
                    value[2] + local[2], value[3] + (local[3],),
                )
                if key not in updated or candidate[0] < updated[key][0]:
                    updated[key] = candidate
        states = updated

    punctured_options = {(0, 0): (0, 0, 0, ())} | punctured
    minima: dict[tuple[int, int], tuple[int, int, int, tuple]] = {}
    for (blocks, points, complete), value in states.items():
        for (lp, lc), local in punctured_options.items():
            h = blocks + (1 if lp else 0)
            if points + lp != 64 or complete + lc > 4 or h not in WEIGHTS:
                continue
            key = (h, complete + lc)
            candidate = (
                value[0] + local[0], value[1] + local[1],
                value[2] + local[2], value[3] + (("P", local[3]),),
            )
            if key not in minima or candidate[0] < minima[key][0]:
                minima[key] = candidate

    assert set(minima) == {(h, c) for h in WEIGHTS for c in range(5)}
    violations = {
        f"{h}_{c}": {"cost_numerator": value[0], "required": DEN * WEIGHTS[h]}
        for (h, c), value in minima.items() if value[0] < DEN * WEIGHTS[h]
    }
    assert not violations

    tight = []
    for (h, c), value in sorted(minima.items()):
        if value[0] == DEN * WEIGHTS[h]:
            tight.append({
                "h": h, "c": c, "base": value[1], "partial": value[2],
                "occupancy_witness": value[3],
            })
    assert [(row["h"], row["c"], row["base"], row["partial"]) for row in tight] == [
        (5, 4, 256, 10),
        (7, 4, 171, 2),
    ]

    base_resource = (31 * 6 * 8 * 8 + 3 * 8 * 8 + 3 * 8 * 7) + c2(7)
    partial_resource = 127 * c2(8)
    assert (base_resource, partial_resource) == (12_285, 3_556)

    upper = Fraction(A_NUM, DEN) * base_resource * 21 + Fraction(P_NUM, DEN) * partial_resource * 2
    assert upper == Fraction(901_390_644, 599)
    assert upper.numerator // upper.denominator == 1_504_825
    assert 1_761_515 - upper.numerator // upper.denominator == 256_690

    # The two tight profiles give an exact dual certificate of optimality for
    # the objective (12285*21)*alpha+(3556*2)*beta.
    lam1 = Fraction(350_091, 599)
    lam2 = Fraction(379_589, 599)
    assert 256 * lam1 + 171 * lam2 == 12_285 * 21
    assert 10 * lam1 + 2 * lam2 == 3_556 * 2
    assert 1716 * lam1 + 792 * lam2 == upper

    payload = {
        "status": "PASS_INDEPENDENT_TWO_PRICE_COMPILER_AUDIT",
        "prices": {"alpha": "2244/599", "beta": "45342/599"},
        "profile_count": len(minima),
        "tight_profiles": tight,
        "resource_counts": {"base": base_resource, "partial": partial_resource},
        "typed_codegrees": {"base": 21, "partial": 2},
        "exact_upper": str(upper),
        "floor_upper": upper.numerator // upper.denominator,
        "slack": 1_761_515 - upper.numerator // upper.denominator,
        "optimality_dual": {"lambda_h5c4": str(lam1), "lambda_h7c4": str(lam2)},
        "scope_guard": "Occupancy compiler only; pair codegrees 21 and 2 remain hypotheses.",
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
