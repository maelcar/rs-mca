#!/usr/bin/env python3
"""Verify the support-dependent ordinary-pair resource repair."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path


PUNCTURED_T32_PAIRS = 31 * math.comb(32, 2) + math.comb(31, 2)
INTER_T8_PAIRS = 31 * 6 * 8 * 8 + (3 * 8 * 8 + 3 * 8 * 7)
PUNCTURED_T8_INTERNAL_PAIRS = math.comb(7, 2)
BASE_ORDINARY_PAIRS = INTER_T8_PAIRS + PUNCTURED_T8_INTERNAL_PAIRS
PARTIAL_COMPLETE_T8_PAIRS = 127 * math.comb(8, 2)
RATIO = Fraction(858, 133)
TAIL_RESIDUAL = 1_761_515


def floor_bound(delta_cross: int, delta_partial: int) -> int:
    value = RATIO * (
        delta_cross * BASE_ORDINARY_PAIRS
        + delta_partial * PARTIAL_COMPLETE_T8_PAIRS
    )
    return value.numerator // value.denominator


def main() -> None:
    assert PUNCTURED_T32_PAIRS == 15_841
    assert INTER_T8_PAIRS == 12_264
    assert PUNCTURED_T8_INTERNAL_PAIRS == 21
    assert BASE_ORDINARY_PAIRS == 12_285
    assert PARTIAL_COMPLETE_T8_PAIRS == 3_556
    assert BASE_ORDINARY_PAIRS + PARTIAL_COMPLETE_T8_PAIRS == PUNCTURED_T32_PAIRS

    # One complete T8 block and eight seven-point partial T8 blocks in nine
    # distinct T32 fibers. Every selected pair lies inside one T8 block.
    occupancy = [[8, 0, 0, 0]] + [[7, 0, 0, 0] for _ in range(8)]
    points = sum(sum(block) for block in occupancy)
    complete_t8 = sum(value == 8 for block in occupancy for value in block)
    rho_printed = sum(math.comb(sum(block), 2) for block in occupancy) - 28 * complete_t8
    rho_cross = sum(
        sum(block[i] * block[j] for i in range(4) for j in range(i + 1, 4))
        for block in occupancy
    )
    rho_partial = sum(
        sum(math.comb(value, 2) for value in block if value < 8)
        for block in occupancy
    )
    assert (points, complete_t8, rho_printed, rho_cross, rho_partial) == (64, 1, 168, 0, 168)

    uniform_all_pair_bounds = {}
    for delta in (16, 17, 18, 21):
        value = RATIO * delta * PUNCTURED_T32_PAIRS
        uniform_all_pair_bounds[str(delta)] = value.numerator // value.denominator
    assert uniform_all_pair_bounds == {
        "16": 1_635_077,
        "17": 1_737_269,
        "18": 1_839_461,
        "21": 2_146_038,
    }

    typed_bounds = {
        "21_1": floor_bound(21, 1),
        "21_2": floor_bound(21, 2),
        "21_4": floor_bound(21, 4),
        "21_5": floor_bound(21, 5),
        "20_5": floor_bound(20, 5),
        "19_8": floor_bound(19, 8),
        "16_16": floor_bound(16, 16),
    }
    assert typed_bounds == {
        "21_1": 1_687_234,
        "21_2": 1_710_174,
        "21_4": 1_756_055,
        "21_5": 1_778_995,
        "20_5": 1_699_743,
        "19_8": 1_689_311,
        "16_16": 1_635_077,
    }

    payload = {
        "status": "PASS_TYPED_PAIR_RESOURCE_PARTITION",
        "resource_counts": {
            "all_same_T32_pairs": PUNCTURED_T32_PAIRS,
            "inter_T8_pairs": INTER_T8_PAIRS,
            "punctured_T8_internal_pairs": PUNCTURED_T8_INTERNAL_PAIRS,
            "base_ordinary_pairs": BASE_ORDINARY_PAIRS,
            "partial_complete_T8_pairs": PARTIAL_COMPLETE_T8_PAIRS,
        },
        "typing_counterprofile": {
            "outer_occupancy": occupancy,
            "points": points,
            "complete_T8_blocks": complete_t8,
            "rho_printed": rho_printed,
            "rho_cross": rho_cross,
            "rho_partial": rho_partial,
            "weight_cap_B9": 330,
        },
        "uniform_all_pair_repair": {
            "sharp_ratio": "858/133",
            "bounds": uniform_all_pair_bounds,
            "largest_closing_integer_codegree": 17,
            "first_failing_integer_codegree": 18,
            "slack_at_17": TAIL_RESIDUAL - uniform_all_pair_bounds["17"],
        },
        "typed_two_resource_repair": {
            "formula": "floor((858/133)*(12285*Delta_base+3556*Delta_partial))",
            "bounds": typed_bounds,
            "closing_21_4_slack": TAIL_RESIDUAL - typed_bounds["21_4"],
            "failing_21_5_excess": typed_bounds["21_5"] - TAIL_RESIDUAL,
        },
        "scope_guard": (
            "This repairs the compiler. It does not prove either typed codegree bound. "
            "The former 12285-resource Delta=21 implication is unsupported with rho(S) "
            "defined by subtracting only complete-T8 internal pairs."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
