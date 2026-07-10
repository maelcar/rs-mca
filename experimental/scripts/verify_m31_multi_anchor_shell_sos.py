#!/usr/bin/env python3
"""Exact verifier for the M31 multi-anchor shell-pair SOS wall."""

from hashlib import sha256
from itertools import combinations, product
from math import comb


N = 2**21
M = 981_129
W = 67_447
L = 2**24
R = M * (N - M)
ONE_SHELL_CAP = N - W
E1_MIN = W + 1
E1_MAX = R // N
E2_MAX = M


def exchange(a, b):
    return len(set(a) - set(b))


def wall(e1, e2):
    return 8 * N * e2 * e2 > R * (16 * e2 - 7 * e1)


def first_bad(e1):
    lo, hi = e1 + 1, E2_MAX
    if not wall(e1, hi):
        return None
    while lo < hi:
        mid = (lo + hi) // 2
        if wall(e1, mid):
            hi = mid
        else:
            lo = mid + 1
    assert wall(e1, lo)
    assert lo == e1 + 1 or not wall(e1, lo - 1)
    return lo


def exact_sos_tests():
    family = list(combinations(range(6), 3))
    checks = 0
    for anchor in family:
        shells = {}
        for row in family:
            if row != anchor:
                shells.setdefault(exchange(anchor, row), []).append(row)
        distances = sorted(shells)
        assert distances == [1, 2, 3]
        for coeffs in product(range(-2, 3), repeat=3):
            coordinate_sum = [0] * 6
            q = 0
            for distance, coeff in zip(distances, coeffs):
                for row in shells[distance]:
                    q += coeff * distance
                    for i in range(6):
                        coordinate_sum[i] += coeff * (
                            int(i in row) - int(i in anchor)
                        )
            lhs = 3 * 3 * sum(x * x for x in coordinate_sum) - 6 * q * q

            delete_loads = [-coordinate_sum[i] for i in anchor]
            add_loads = [coordinate_sum[i] for i in range(6) if i not in anchor]
            rhs = 3 * sum(
                (delete_loads[i] - delete_loads[j]) ** 2
                for i in range(3) for j in range(i + 1, 3)
            ) + 3 * sum(
                (add_loads[i] - add_loads[j]) ** 2
                for i in range(3) for j in range(i + 1, 3)
            )
            assert lhs == rhs >= 0
            checks += 1
    return checks


def ceil_div(a, b):
    return -((-a) // b)


def main():
    sos_checks = exact_sos_tests()
    assert sos_checks == 2_500

    universe = sum(E2_MAX - e1 for e1 in range(E1_MIN, E1_MAX + 1))
    rows = []
    cut_count = 0
    for e1 in range(E1_MIN, E1_MAX + 1):
        start = first_bad(e1)
        if start is None:
            continue
        count = E2_MAX - start + 1
        rows.append((e1, start, E2_MAX, count))
        cut_count += count

    payload = "".join(
        f"{e1},{start},{end},{count}\n"
        for e1, start, end, count in rows
    )
    interval_hash = sha256(payload.encode("ascii")).hexdigest()

    integral_grid = 0
    integral_overlap = 0
    for kappa in range(2, 775):
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            integral_grid += 1
            if wall((kappa - 1) * t, kappa * t):
                integral_overlap += 1

    q, rem = divmod(L, ONE_SHELL_CAP)
    complement_edges = rem * comb(q + 1, 2) + (ONE_SHELL_CAP - rem) * comb(q, 2)
    ordered_nonminimum = 2 * complement_edges
    high_degree_anchors = L - 8 * ONE_SHELL_CAP
    high_degree_incidences = ordered_nonminimum - 56 * ONE_SHELL_CAP

    strict_e1 = 522_118
    strict_shells = list(range(981_122, 981_130))
    strict_margin = (
        N * sum(strict_shells) ** 2
        - R * (16 * sum(strict_shells) - 7 * strict_e1 * 8)
    )

    assert universe == 312_061_622_166
    assert len(rows) == 386_588
    assert cut_count == 45_504_039_302
    assert universe - cut_count == 266_557_582_864
    assert rows[0] == (135_531, 981_129, 981_129, 1)
    assert rows[-1] == (522_118, 706_717, 981_129, 274_413)
    assert interval_hash == "d130fa35b9c5b8d473e3929d53d2627f598439b26e67fb689ec9936c11ee465f"
    assert integral_grid == 3_254_885
    assert integral_overlap == 97_162
    assert complement_edges == 61_148_348
    assert ordered_nonminimum == 122_296_696
    assert high_degree_anchors == 539_576
    assert high_degree_incidences == 8_633_216
    assert strict_margin == 23_704_293_362_569_658_480

    print("RESULT: PASS")
    print(f"weighted_sos_checks={sos_checks}")
    print(f"first_two_cells_total={universe}")
    print(f"first_two_cells_cut={cut_count}")
    print(f"first_two_cells_survive={universe-cut_count}")
    print(f"cut_interval_rows={len(rows)}")
    print(f"cut_interval_sha256={interval_hash}")
    print(f"integral_ratio_overlap={integral_overlap}")
    print(f"high_degree_anchors={high_degree_anchors}")
    print(f"high_degree_incidences={high_degree_incidences}")
    print(f"strict_cross_shell_gain_margin={strict_margin}")


if __name__ == "__main__":
    main()
