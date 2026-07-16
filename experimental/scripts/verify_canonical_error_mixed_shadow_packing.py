#!/usr/bin/env python3
"""Exact arithmetic for canonical-error mixed complete-fiber shadows."""

from __future__ import annotations

import argparse
from math import comb


P = 2_130_706_433
N_DEPLOYED = 2_097_152
K = 1_048_576
M = 1_116_047
T = N_DEPLOYED - M
DELTA = N_DEPLOYED - 2 * M + K - 1
TARGET = 274_854_110_496_187_592


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def compute(delta: int = DELTA, q64_blocks: int = 64) -> dict[str, int]:
    b64 = 2**15
    s64 = delta // b64
    shadow64 = comb(q64_blocks, s64 + 1)
    f29_cap = shadow64 // comb(29, s64 + 1)

    b32 = 2**16
    n32 = 32
    s32 = delta // b32
    paired = comb(n32, s32 + 1)
    joint = paired + (shadow64 - paired) // 29
    nonpaired = shadow64 - paired

    return {
        "delta": delta,
        "s64": s64,
        "shadow64": shadow64,
        "f29_cap": f29_cap,
        "f29_margin": TARGET - f29_cap,
        "s32": s32,
        "paired": paired,
        "joint": joint,
        "joint_margin": TARGET - joint,
        "nonpaired": nonpaired,
        "nonpaired_excess": nonpaired - TARGET,
    }


def verify(values: dict[str, int]) -> None:
    require(P - 1 == 1016 * N_DEPLOYED, "deployed subgroup divisibility")
    require(T == 981_105, "canonical error-complement size")
    require(DELTA == 913_633, "canonical complement intersection bound")
    require(T == 29 * 2**15 + 30_833, "q64 complement decomposition")
    require(T == 14 * 2**16 + 63_601, "q32 complement decomposition")
    require(27 * 2**15 <= DELTA < 28 * 2**15, "q64 shadow threshold")
    require(13 * 2**16 <= DELTA < 14 * 2**16, "q32 shadow threshold")

    require(values["delta"] == 913_633, "delta")
    require(values["s64"] == 27, "q64 s")
    require(values["shadow64"] == 1_118_770_292_985_239_888, "q64 shadow count")
    require(values["f29_cap"] == 38_578_285_965_008_272, "q64 f29 cap")
    require(values["f29_margin"] == 236_275_824_531_179_320, "q64 f29 margin")
    require(values["s32"] == 13, "q32 s")
    require(values["paired"] == 471_435_600, "paired q32 shadows")
    require(values["joint"] == 38_578_286_420_187_472, "joint cap")
    require(values["joint_margin"] == 236_275_824_076_000_120, "joint margin")
    require(values["nonpaired"] == 1_118_770_292_513_804_288, "nonpaired ceiling")
    require(values["nonpaired_excess"] == 843_916_182_017_616_696, "nonpaired excess")
    require(values["f29_cap"] < TARGET, "f29 cap is below the full target")
    require(values["joint"] < TARGET, "joint cap is below the full target")
    require(values["nonpaired"] > TARGET, "nonpaired f28 remains open")


def tamper_selftest() -> None:
    caught = 0
    for kwargs in ({"delta": DELTA + 1}, {"q64_blocks": 63}):
        try:
            verify(compute(**kwargs))
        except RuntimeError:
            caught += 1
    require(caught == 2, "tamper self-test")
    print("tamper_selftest=PASS caught=2/2")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        tamper_selftest()
        return

    values = compute()
    verify(values)
    print("CANONICAL_ERROR_MIXED_SHADOW_PACKING: PASS")
    for key in (
        "delta",
        "s64",
        "shadow64",
        "f29_cap",
        "f29_margin",
        "s32",
        "paired",
        "joint",
        "joint_margin",
        "nonpaired",
        "nonpaired_excess",
    ):
        print(f"{key}={values[key]}")
    print("scope=one arbitrary received word; global across its rays and generators")
    print("nonclaim=cap is not a complete disjoint-ledger or official-score payment")


if __name__ == "__main__":
    main()
