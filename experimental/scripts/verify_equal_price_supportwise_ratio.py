#!/usr/bin/env python3
"""Verify the sharp equal-price supportwise occupancy ratio."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


WEIGHTS = {
    3: 3432, 4: 1716, 5: 1716, 6: 792, 7: 792,
    8: 330, 9: 330, 10: 120, 11: 120, 12: 36,
    13: 36, 14: 8, 15: 8, 16: 1, 17: 1,
}


def minimum_ordinary_pairs() -> dict[tuple[int, int], int]:
    """Minimize in a relaxation with four size-eight subblocks per block."""
    local_states: list[tuple[int, int, int]] = []
    for full_subblocks in range(5):
        for mixed_points in range(7 * (4 - full_subblocks) + 1):
            points = 8 * full_subblocks + mixed_points
            if 1 <= points <= 31:
                cost = math.comb(points, 2) - 28 * full_subblocks
                local_states.append((points, full_subblocks, cost))

    infinity = 10**9
    states: dict[tuple[int, int, int], int] = {(0, 0, 0): 0}
    for _ in range(17):
        updated = dict(states)
        for (blocks, points, complete_t8), value in states.items():
            for local_points, local_t8, local_cost in local_states:
                key = (blocks + 1, points + local_points, complete_t8 + local_t8)
                if key[0] <= 17 and key[1] <= 64 and key[2] <= 4:
                    updated[key] = min(updated.get(key, infinity), value + local_cost)
        states = updated

    return {
        (h, c): states[(h, 64, c)]
        for h in WEIGHTS
        for c in range(5)
    }


def main() -> None:
    minima = minimum_ordinary_pairs()
    expected_rows = {
        3: [651, 623, 595, 567, 539],
        4: [480, 452, 424, 396, 368],
        5: [378, 350, 322, 294, 266],
        6: [310, 282, 254, 226, 198],
        7: [261, 233, 205, 177, 149],
        8: [224, 196, 168, 140, 112],
        9: [196, 168, 141, 114, 87],
        10: [174, 147, 120, 95, 70],
        11: [155, 130, 105, 80, 58],
        12: [140, 115, 92, 70, 48],
        13: [126, 104, 82, 60, 42],
        14: [116, 94, 72, 54, 36],
        15: [106, 84, 66, 48, 31],
        16: [96, 78, 60, 42, 28],
        17: [90, 72, 54, 38, 25],
    }
    actual_rows = {h: [minima[(h, c)] for c in range(5)] for h in WEIGHTS}
    assert actual_rows == expected_rows

    ratios = {(h, c): Fraction(WEIGHTS[h], minima[(h, c)]) for h in WEIGHTS for c in range(5)}
    worst_profile = max(ratios, key=ratios.get)
    sharp_ratio = ratios[worst_profile]
    assert worst_profile == (5, 4)
    assert sharp_ratio == Fraction(858, 133)

    payload = {
        "verdict": "PASS_EQUAL_PRICE_SUPPORTWISE_OCCUPANCY_RATIO",
        "relaxed_minimum_table": {str(h): actual_rows[h] for h in actual_rows},
        "sharp_pointwise_ratio": {
            "numerator": sharp_ratio.numerator,
            "denominator": sharp_ratio.denominator,
            "attained_at_h_completeT8": list(worst_profile),
        },
        "scope_guard": (
            "This proves q_z(S)/rho(S)<=858/133 in the stated occupancy "
            "relaxation. The global resource partition is checked separately."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
