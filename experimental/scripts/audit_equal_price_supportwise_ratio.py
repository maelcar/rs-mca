#!/usr/bin/env python3
"""Independent dynamic-programming audit of the equal-price ratio."""

from __future__ import annotations

import json
import math
from fractions import Fraction


WEIGHTS = [3432, 1716, 1716, 792, 792, 330, 330, 120, 120, 36, 36, 8, 8, 1, 1]


def independent_minimum(points: int, blocks: int, full_fibers: int) -> int:
    infinity = 10**9
    dp = {(0, 0): 0}
    for _ in range(blocks):
        nxt = {}
        for (used_points, used_full), value in dp.items():
            for local_full in range(5):
                for residual in range(7 * (4 - local_full) + 1):
                    local_points = 8 * local_full + residual
                    if local_points == 0:
                        continue
                    key = (used_points + local_points, used_full + local_full)
                    if key[0] <= points and key[1] <= full_fibers:
                        local_cost = math.comb(local_points, 2) - 28 * local_full
                        nxt[key] = min(nxt.get(key, infinity), value + local_cost)
        dp = nxt
    return dp[(points, full_fibers)]


def main() -> None:
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
    maximum = Fraction(0)
    owner = None
    table = {}
    for offset, h in enumerate(range(3, 18)):
        row = []
        for c in range(5):
            value = independent_minimum(64, h, c)
            row.append(value)
            ratio = Fraction(WEIGHTS[offset], value)
            if ratio > maximum:
                maximum = ratio
                owner = (h, c)
        table[h] = row

    assert table == expected_rows
    assert maximum == Fraction(858, 133)
    assert owner == (5, 4)
    payload = {
        "verdict": "PASS_INDEPENDENT_EQUAL_PRICE_SUPPORTWISE_RATIO",
        "sharp_ratio": "858/133",
        "sharp_profile": [5, 4],
        "relaxed_minimum_table": {str(h): row for h, row in table.items()},
        "scope_guard": (
            "Supportwise occupancy ratio only; global pair resources and "
            "codegrees are separate inputs."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
