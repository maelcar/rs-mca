#!/usr/bin/env python3
"""Replay the integer ledger for the rank-16 quotient-line obstruction."""

from __future__ import annotations

import argparse


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def replay(*, block: int = 32_768, degree_shift: int = 0, width_shift: int = 0) -> list[str]:
    p = 2_130_706_433
    n = 2_097_152
    k = 1_048_576
    m = 1_116_047
    core_size = 27
    target = 274_854_110_496_187_592

    require(is_prime(p), "deployed field modulus is not prime")
    require(p - 1 == 127 * (2**24), "field factorization mismatch")
    require(n == 2**21 and n % block == 0, "subgroup/block mismatch")
    require(n // block == 64, "q64 image-size mismatch")

    t = n - m
    sigma = m - k
    generator_degree = sigma + 1
    degree = t - core_size * block + degree_shift
    residual_degree = degree - block
    width = degree - generator_degree + width_shift

    require((t, sigma, generator_degree) == (981_105, 67_471, 67_472), "base degrees mismatch")
    require(degree == 96_369, "post-core locator degree mismatch")
    require(residual_degree == 63_601, "residual locator degree mismatch")
    require(width == 28_897, "Pade quotient degree mismatch")

    root_count = 6 * block
    cross_degree = 2 * degree
    require(root_count > cross_degree, "six-fiber root count does not force the cross polynomial to vanish")

    lower = degree - width
    upper = degree
    multiples = [j * block for j in range(upper // block + 2) if lower <= j * block <= upper]
    require(not multiples, "a block multiple survives the final degree interval")
    require(2 * block < lower and upper < 3 * block, "degree interval is not strictly between 2B and 3B")

    cap8_total = 272_133_314_965_102_416
    cap9_total = 301_327_693_533_216_784
    cap8_margin = target - cap8_total
    cap9_excess = cap9_total - target
    require(cap8_margin == 2_720_795_531_085_176, "cap-eight margin mismatch")
    require(cap9_excess == 26_473_583_037_029_192, "cap-nine excess mismatch")

    return [
        "RANK16_FIXED_CORE_QUOTIENT_LINE_OBSTRUCTION: PASS",
        f"p={p} prime=true p_minus_1={p - 1}=127*2^24 subgroup={n} block={block} image={n // block}",
        f"t={t} sigma={sigma} a={generator_degree} D={degree} residual={residual_degree} w={width}",
        f"cross_roots={root_count} cross_degree_cap={cross_degree} gap={root_count - cross_degree}",
        f"degree_interval=[{lower},{upper}] twoB={2 * block} threeB={3 * block} multiples={multiples}",
        f"conditional_cap8_total={cap8_total} target_margin={cap8_margin}",
        f"cap9_total={cap9_total} target_excess={cap9_excess}",
        "RESULT: PASS",
    ]


def tamper_selftest() -> None:
    mutations = (
        {"block": 32_767},
        {"degree_shift": 2_000},
        {"width_shift": 2_000},
    )
    for mutation in mutations:
        try:
            replay(**mutation)
        except RuntimeError:
            continue
        raise RuntimeError(f"tamper mutation was not rejected: {mutation}")
    print("TAMPER_SELFTEST: PASS (3/3 rejected)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        tamper_selftest()
        return
    print("\n".join(replay()))


if __name__ == "__main__":
    main()
