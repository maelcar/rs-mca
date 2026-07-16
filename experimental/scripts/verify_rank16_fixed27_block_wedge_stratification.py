#!/usr/bin/env python3
"""Arithmetic replay for the fixed-27-core block-wedge theorem."""

def main() -> None:
    p = 2_130_706_433
    n = 2_097_152
    K = 1_048_576
    m = 1_116_047
    t = n - m
    sigma = m - K
    a = sigma + 1
    B = 32_768
    fixed_core = 27
    D = t - fixed_core * B
    w = D - a
    residual = D - B

    assert p - 1 == 127 * 2**24
    assert n == 2**21
    assert n // B == 64
    assert (t, sigma, a) == (981_105, 67_471, 67_472)
    assert (D, w, residual) == (96_369, 28_897, 63_601)
    assert w < B and 2 * B < a < D < 3 * B

    transverse = {r: 2 * r - 5 for r in range(3, 7)}
    assert transverse == {3: 1, 4: 3, 5: 5, 6: 7}
    assert 2 * (2 + 1) < 7

    cubic_k = 3 * B - a
    quartic_k = 4 * B - a
    assert cubic_k == 30_832
    assert quartic_k == 63_600
    assert cubic_k + residual == 94_433
    assert quartic_k + residual == 127_201
    assert 2 * B + w == 94_433
    assert 3 * B + w == 127_201

    target = 274_854_110_496_187_592
    cap6 = 271_769_678_181_377_208
    cap7 = 300_964_056_749_491_576
    assert target - cap6 == 3_084_432_314_810_384
    assert cap7 - target == 26_109_946_253_303_984

    # Fail closed under the two errors caught in hostile audit.
    assert cubic_k + residual != residual
    assert quartic_k + residual != residual
    sample_a0, sample_aj = 7, 0
    sample_c = sample_aj / sample_a0
    assert sample_c == 0

    print("RANK16_FIXED27_BLOCK_WEDGE: PASS")
    print(f"field=p={p} p_minus_1=127*2^24 H_order={n} q64_block={B}")
    print(f"degrees: a={a} D={D} w={w} residual={residual}")
    print(f"transverse={transverse}")
    print(
        "rank2: "
        f"cubic_K={cubic_k} cubic_product={cubic_k + residual} "
        f"quartic_K={quartic_k} quartic_product={quartic_k + residual}"
    )
    print(
        "conditional_ledger: "
        f"cap6_margin={target - cap6} cap7_excess={cap7 - target}"
    )
    print("finite_payment=0 official_score=0/2")


if __name__ == "__main__":
    main()
