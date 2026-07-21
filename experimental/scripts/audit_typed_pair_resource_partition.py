#!/usr/bin/env python3
"""Independent arithmetic and occupancy audit of the pair-resource repair."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction
from pathlib import Path


def choose2(n: int) -> int:
    return n * (n - 1) // 2


def bound(dc: int, di: int) -> int:
    value = Fraction(858, 133) * (12_285 * dc + 3_556 * di)
    return value.numerator // value.denominator


def main() -> None:
    full_outer = 31 * 496 + 465
    inter = 31 * (6 * 64) + 3 * 64 + 3 * 56
    punctured_internal = choose2(7)
    base = inter + punctured_internal
    partial_complete = 127 * 28
    assert (full_outer, inter, punctured_internal) == (15_841, 12_264, 21)
    assert (base, partial_complete) == (12_285, 3_556)
    assert base + partial_complete == full_outer

    blocks = [(8, 0, 0, 0)] + [(7, 0, 0, 0)] * 8
    total = sum(itertools.chain.from_iterable(blocks))
    complete = sum(x == 8 for x in itertools.chain.from_iterable(blocks))
    printed = sum(choose2(sum(row)) for row in blocks) - 28 * complete
    cross_count = sum(
        sum(row[i] * row[j] for i in range(4) for j in range(i + 1, 4))
        for row in blocks
    )
    partial_count = sum(
        sum(choose2(x) for x in row if x != 8)
        for row in blocks
    )
    assert (total, complete, printed, cross_count, partial_count) == (64, 1, 168, 0, 168)

    uniform = {
        d: (Fraction(858, 133) * d * full_outer).__floor__()
        for d in (16, 17, 18, 21)
    }
    assert uniform == {
        16: 1_635_077, 17: 1_737_269, 18: 1_839_461, 21: 2_146_038
    }
    typed = {(21, d): bound(21, d) for d in (1, 2, 4, 5)}
    assert typed == {
        (21, 1): 1_687_234, (21, 2): 1_710_174,
        (21, 4): 1_756_055, (21, 5): 1_778_995,
    }

    payload = {
        "status": "PASS_INDEPENDENT_TYPED_PAIR_RESOURCE_PARTITION",
        "all_pairs": full_outer,
        "inter_T8_pairs": inter,
        "punctured_T8_internal_pairs": punctured_internal,
        "base_ordinary_pairs": base,
        "partial_complete_T8_pairs": partial_complete,
        "counterprofile_rho": [printed, cross_count, partial_count],
        "uniform_bounds": {str(k): v for k, v in uniform.items()},
        "typed_21_1": typed[(21, 1)],
        "typed_21_2": typed[(21, 2)],
        "typed_21_4": typed[(21, 4)],
        "typed_21_5": typed[(21, 5)],
        "slack_21_4": 1_761_515 - typed[(21, 4)],
        "excess_21_5": typed[(21, 5)] - 1_761_515,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
