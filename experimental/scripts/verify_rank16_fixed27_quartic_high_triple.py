#!/usr/bin/env python3
"""Independent finite replay for the fixed-27 quartic high-triple theorem."""

B = 32_768
D = 63_601
W = 28_897
BASE_CAP = 12_997
LAMBDA_MIN = W - BASE_CAP
LAMBDA_MAX = W


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def balanced_pair_sum(total: int, cells: int = 6) -> int:
    q, rem = divmod(total, cells)
    return rem * (q + 1) * q + (cells - rem) * q * (q - 1)


def main() -> None:
    rows = []
    block = 4
    checked_pairs = 0
    while block <= B:
        orbit = B // block
        best = None
        for lam in range(LAMBDA_MIN, LAMBDA_MAX + 1):
            checked_pairs += 1
            local_degree = lam // orbit
            required_total = (5 * lam) // orbit + 1
            if required_total > 6 * local_degree:
                continue
            quadratic_min = balanced_pair_sum(required_total)
            comparison_cap = (block - 1) * (2 * local_degree - 1)
            gap = quadratic_min - comparison_cap
            candidate = (
                gap,
                lam,
                local_degree,
                required_total,
                quadratic_min,
                comparison_cap,
            )
            if best is None or candidate < best:
                best = candidate

        require(best is not None, f"no feasible row for block={block}")
        require(best[0] > 0, f"descent inequality fails for block={block}: {best}")
        rows.append((block, orbit, *best))
        block *= 2

    expected = [
        (4, 8192, 1, 16384, 2, 11, 10, 9),
        (8, 4096, 5, 16384, 4, 21, 54, 49),
        (16, 2048, 15, 16384, 8, 41, 240, 225),
        (32, 1024, 37, 15900, 15, 78, 936, 899),
        (64, 512, 57, 15900, 31, 156, 3900, 3843),
        (128, 256, 189, 15900, 62, 311, 15810, 15621),
        (256, 128, 875, 15900, 124, 622, 63860, 62985),
        (512, 64, 3321, 15900, 248, 1243, 256266, 252945),
        (1024, 32, 11709, 15904, 497, 2486, 1027548, 1015839),
        (2048, 16, 46115, 15904, 994, 4971, 4113504, 4067389),
        (4096, 8, 181269, 15900, 1987, 9938, 16450704, 16269435),
        (8192, 4, 712429, 15900, 3975, 19876, 65822688, 65110259),
        (16384, 2, 2843933, 15900, 7950, 39751, 263317250, 260473317),
        (32768, 1, 11364167, 15900, 15900, 79501, 1053322000, 1041957833),
    ]
    require(rows == expected, "finite convexity table mismatch")
    require(checked_pairs == 181_972, "wrong exhaustive pair count")

    reduced_min = D - BASE_CAP
    reduced_max = D
    terminal_orbit = B // 2
    require(
        3 * terminal_orbit < reduced_min <= reduced_max < 4 * terminal_orbit,
        "terminal reduced-degree interval contains an orbit multiple",
    )

    numerator = 7 * D - 5 * W
    union_floor = (numerator + 1) // 2
    require((numerator, union_floor) == (300_722, 150_361), "union floor mismatch")

    mutations = {
        "allows_zero_gap": min(row[2] for row in rows) <= 0,
        "weakened_terminal_orbit_has_no_multiple": not any(
            x % 8192 == 0 for x in range(reduced_min, reduced_max + 1)
        ),
        "old_union_floor": union_floor == 141_686,
    }
    require(not any(mutations.values()), f"tamper survived: {mutations}")

    print("R30_FIXED27_QUARTIC_HIGH_TRIPLE: PASS")
    print(
        f"B={B} d={D} w={W} Base_cap={BASE_CAP} "
        f"lambda_range={LAMBDA_MIN}..{LAMBDA_MAX} checked_pairs={checked_pairs}"
    )
    for block, orbit, gap, lam, degree, total, qmin, cap in rows:
        print(
            f"block={block:5d} orbit={orbit:5d} min_gap={gap:8d} "
            f"at_lambda={lam} L={degree} S={total} Q={qmin} cap={cap}"
        )
    print(
        f"terminal_orbit={terminal_orbit} residual_range={reduced_min}..{reduced_max} "
        f"bracket={3*terminal_orbit}<{reduced_min}<={reduced_max}<{4*terminal_orbit}"
    )
    print(f"union_floor={union_floor}")
    print("tamper_checks=3/3")


if __name__ == "__main__":
    main()
