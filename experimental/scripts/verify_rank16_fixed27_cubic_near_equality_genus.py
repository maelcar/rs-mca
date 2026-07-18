#!/usr/bin/env python3
"""Replay the finite arithmetic in the fixed-27 cubic genus exclusion."""

from __future__ import annotations

from math import comb, gcd


ORIGIN_MAIN = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
PR892_HEAD = "d4a33c87ac3e3e1a5078b88fddf085cb6536b75e"

P = 2_130_706_433
H_ORDER = 2**21
B = 32_768
A = 67_472
D = 63_601
W = 28_897
COMMON_FLOOR = 230_415

LAYERS = {
    18_619: {"slack": 2, "pr_floor": 176_056},
    18_618: {"slack": 5, "pr_floor": 176_059},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def partitions3(total: int) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (x, y, total - x - y)
        for x in range(total, -1, -1)
        for y in range(min(x, total - x), -1, -1)
        if y >= total - x - y >= 0
    )


def typed_atlas(total: int) -> dict[str, tuple[tuple[int, ...], ...]]:
    split = partitions3(total)
    linear_quadratic = tuple(
        (total - 2 * quadratic, quadratic)
        for quadratic in range(total // 2 + 1)
    )
    double_simple = tuple(
        (first, second, total - first - second)
        for first in range(total, -1, -1)
        for second in range(min(first, total - first), -1, -1)
        if total - first - second >= 0
    )
    return {
        "split": split,
        "linear_quadratic": linear_quadratic,
        "double_simple": double_simple,
        "triple": split,
    }


def occurrence_slacks(kind: str, pattern: tuple[int, ...]) -> tuple[int, int, int]:
    if kind == "linear_quadratic":
        linear, quadratic = pattern
        return linear, quadratic, quadratic
    return pattern  # split, double+simple, and triple each have three layers


def root_charge(c: int, k: int) -> tuple[int, tuple[int, int, int], str]:
    base_degree = B - (W - c)
    candidates = []
    for kind, patterns in typed_atlas(LAYERS[c]["slack"]).items():
        for pattern in patterns:
            degrees = tuple(base_degree + x for x in occurrence_slacks(kind, pattern))
            branch_counts = tuple((degree + k - 1) // k for degree in degrees)
            charge = sum(comb(count, 2) for count in branch_counts)
            candidates.append((charge, tuple(sorted(degrees)), kind))
    return min(candidates)


def balanced_pair_charge(total_branches: int, pair_points: int = 21) -> int:
    q, s = divmod(total_branches, pair_points)
    return pair_points * comb(q, 2) + s * q


def allowed_map_degrees(c: int) -> tuple[int, ...]:
    r = D - c
    common = gcd(B, r)
    return tuple(k for k in range(1, common + 1) if common % k == 0)


def genus_row(
    c: int,
    k: int,
    union_size: int,
    *,
    pair_points: int = 21,
    root_adjustment: int = 0,
) -> dict[str, int]:
    r = D - c
    require(r % k == 0, "map degree must divide the residual degree")
    image_degree = r // k
    pair_mass = 7 * D - 6 * c - union_size
    require(pair_mass % k == 0, "pair mass must be divisible by the map degree")
    pair_branches = pair_mass // k
    d_pair = balanced_pair_charge(pair_branches, pair_points)
    d_root = root_charge(c, k)[0] + root_adjustment
    arithmetic_genus = comb(image_degree - 1, 2)
    return {
        "c": c,
        "k": k,
        "union": union_size,
        "E": pair_mass,
        "N": pair_branches,
        "D_pair": d_pair,
        "D_root": d_root,
        "p_a": arithmetic_genus,
        "excess": d_pair + d_root - arithmetic_genus,
    }


def largest_admissible_below(c: int, k: int, floor: int) -> int:
    for union_size in range(floor - 1, LAYERS[c]["pr_floor"] - 1, -1):
        if (7 * D - 6 * c - union_size) % k == 0:
            return union_size
    raise AssertionError("no admissible row")


def proves_floor(
    floor: int,
    *,
    pair_points: int = 21,
    root_adjustment: int = 0,
) -> bool:
    for c in LAYERS:
        for k in allowed_map_degrees(c):
            union_size = largest_admissible_below(c, k, floor)
            row = genus_row(
                c,
                k,
                union_size,
                pair_points=pair_points,
                root_adjustment=root_adjustment,
            )
            if row["excess"] <= 0:
                return False
    return True


def first_unresolved(c: int, k: int) -> dict[str, int]:
    for union_size in range(COMMON_FLOOR, COMMON_FLOOR + 100):
        if (7 * D - 6 * c - union_size) % k:
            continue
        row = genus_row(c, k, union_size)
        if row["excess"] <= 0:
            return row
    raise AssertionError("unresolved row not found")


def endpoint_occupancy(c: int) -> tuple[int, int, int, int]:
    r = D - c
    union_size = LAYERS[c]["pr_floor"]
    outside_union = union_size - c
    incidences = 7 * r
    singletons = 2 * outside_union - incidences
    doubletons = incidences - outside_union
    return r, incidences, singletons, doubletons


def main() -> None:
    require(P - 1 == 2_130_706_432, "wrong deployed field")
    require(H_ORDER == 2_097_152, "wrong deployed subgroup")
    require(3 * B - A == 30_832, "wrong cubic degree identity")
    require(3 * W - (3 * B - A) == 55_859, "wrong resultant budget")
    require(55_859 // 3 == 18_619, "wrong Base cap")
    require(55_859 - 3 * 18_619 == 2, "wrong top-layer slack")
    require(55_859 - 3 * 18_618 == 5, "wrong adjacent-layer slack")

    require(allowed_map_degrees(18_619) == (1, 2), "wrong top map degrees")
    require(allowed_map_degrees(18_618) == (1,), "wrong adjacent map degree")

    expected_occupancy = {
        18_619: (44_982, 314_874, 0, 157_437),
        18_618: (44_983, 314_881, 1, 157_440),
    }
    for c, expected in expected_occupancy.items():
        require(endpoint_occupancy(c) == expected, f"wrong endpoint occupancy at c={c}")
        r, _, singletons, _ = expected
        pair_degree = r - (1 if singletons else 0)
        require(4 * (W - c) < pair_degree, f"five-edge gate failed at c={c}")

    atlas2 = typed_atlas(2)
    atlas5 = typed_atlas(5)
    require(tuple(map(len, atlas2.values())) == (2, 2, 4, 2), "slack-two atlas")
    require(tuple(map(len, atlas5.values())) == (5, 3, 12, 5), "slack-five atlas")

    expected_roots = {
        (18_619, 1): (758_711_395, (22_490, 22_491, 22_491)),
        (18_619, 2): (189_669_415, (22_490, 22_490, 22_492)),
        (18_618, 1): (758_711_395, (22_490, 22_491, 22_491)),
    }
    for key, (charge, degrees) in expected_roots.items():
        got_charge, got_degrees, _ = root_charge(*key)
        require(
            (got_charge, got_degrees) == (charge, degrees),
            f"wrong root-charge minimum at {key}",
        )

    require(proves_floor(COMMON_FLOOR), "common union floor is not certified")

    decisive = [
        genus_row(18_619, 1, 230_414),
        genus_row(18_619, 2, 230_413),
        genus_row(18_618, 1, 230_414),
    ]
    require(
        [row["excess"] for row in decisive] == [20_031, 1_785, 4_498],
        "wrong decisive genus excesses",
    )

    unresolved = [
        first_unresolved(18_619, 1),
        first_unresolved(18_619, 2),
        first_unresolved(18_618, 1),
    ]
    require(
        [(row["union"], -row["excess"]) for row in unresolved]
        == [(230_419, 4_509), (230_415, 669), (230_415, 410)],
        "wrong first unresolved rows",
    )

    mutations = [
        not proves_floor(230_420),
        not proves_floor(COMMON_FLOOR, pair_points=22),
        not proves_floor(COMMON_FLOOR, root_adjustment=-1_786),
    ]
    require(all(mutations), "one or more semantic mutations survived")

    print("rank16 fixed27 cubic near-equality genus verifier")
    print(f"origin_main={ORIGIN_MAIN}")
    print(f"pr892_head={PR892_HEAD}")
    print("atlas_counts slack2=2,2,4,2 slack5=5,3,12,5")
    for row in decisive:
        print(
            "decisive"
            f" c={row['c']} k={row['k']} U={row['union']}"
            f" E={row['E']} N={row['N']}"
            f" D_pair={row['D_pair']} D_root={row['D_root']}"
            f" p_a={row['p_a']} excess={row['excess']}"
        )
    for row in unresolved:
        print(
            "first_unresolved"
            f" c={row['c']} k={row['k']} U={row['union']}"
            f" shortfall={-row['excess']}"
        )
    print("common_union_floor=230415")
    print("mutations=3/3")
    print("PASS")


if __name__ == "__main__":
    main()
