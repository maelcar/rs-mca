#!/usr/bin/env python3
"""Exact verifier for the M31 rank-inertia anchored two-shell cut."""

from hashlib import sha256
from math import comb


N = 2**21
M = 981_129
W = 67_447
L = 2**24
R = M * (N - M)
Q = 7 * N


def ceil_div(a, b):
    return -((-a) // b)


def falling(x, length):
    out = 1
    for i in range(length):
        out *= x - i
    return out


def eberlein_num(distance, level):
    return sum(
        (-1) ** j
        * comb(level, j)
        * falling(distance, j) ** 2
        * falling(M - distance, level - j)
        * falling(N - M - distance, level - j)
        for j in range(level + 1)
    )


def eberlein_den(level):
    return falling(M, level) * falling(N - M, level)


def pr495_infeasible(e1, e2):
    low_num, low_den = 0, 1
    high_num, high_den = L - 1, 1
    for level in range(1, 7):
        den = eberlein_den(level)
        n1 = eberlein_num(e1, level)
        n2 = eberlein_num(e2, level)
        coeff = n1 - n2
        rhs = -den - (L - 1) * n2
        if coeff > 0 and rhs * low_den > low_num * coeff:
            low_num, low_den = rhs, coeff
        elif coeff < 0:
            num, denom = -rhs, -coeff
            if num * high_den < high_num * denom:
                high_num, high_den = num, denom
        elif coeff == 0 and rhs > 0:
            return True
        if low_num * high_den > high_num * low_den:
            return True
    return False


def p_value(kappa, x):
    lam = kappa - 1
    return x * x + (14 * lam - 8 * (N - 1)) * x + 7 * lam * lam * (8 * N - 1)


def t_value(kappa, x):
    lam = kappa - 1
    return (N - 1) ** 2 * (Q * lam**3 + x**3) - (Q * lam + x) ** 3


def first_true(lo, hi, predicate):
    assert lo <= hi and predicate(hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def anchor_threshold(kappa):
    lam = kappa - 1
    vertex = 4 * (N - 1) - 7 * lam
    h2 = first_true(0, vertex, lambda h: p_value(kappa, h) <= 0)
    lower = ceil_div(Q * lam, N - 2)
    h3 = first_true(lower, L - 1, lambda h: t_value(kappa, h) >= 0)
    return max(h2, h3), h2, h3


def rank_inertia_cut(kappa, t, h):
    lam = kappa - 1
    z = (h * (kappa + 1) + lam) * R - h * N * kappa * kappa * t
    if h <= N:
        return z < 0
    d = h - N
    if d * lam <= N:
        return d * lam * lam * R > N * z
    b = 2 * d * lam - h * (N - 1)
    c = d * lam * lam * (h - 1)
    return (
        2 * N * z < -b * R
        and N * z * z + b * z * R + c * R * R > 0
    )


def centroid_cut(kappa, t):
    lam = kappa - 1
    un = L * R - lam * (L - 1) * N * t
    ud = N * t
    return (
        2 * un < (8 * (N - 1) - 14 * lam) * ud
        and un * un
        + (14 * lam - 8 * (N - 1)) * un * ud
        + 7 * lam * lam * (8 * N - 1) * ud * ud
        > 0
    )


def pr529_cut(kappa, t):
    return 8 * N * kappa * kappa * t > (9 * kappa + 7) * R


def spectral_cubic_cut(kappa, t):
    """Independent Role 02 predicate, used only for containment audit."""
    lam = kappa - 1
    c0 = N * kappa * kappa * t - R * (kappa + 1)
    if c0 <= 0:
        return False
    u = R * lam // c0
    q0 = u * u - 7 * u * lam - 16 * u + 14 * lam * lam
    p0 = (
        u * u
        - 7 * u * lam * lam
        - 7 * u * lam
        - 8 * u
        + 7 * lam**3
        + 14 * lam * lam
    )
    g0 = u**3 - 21 * lam * u * u + 28 * lam**3
    return (q0 > 0 and p0 < 0) or (q0 <= 0 and g0 < 0)


def row_hash(rows):
    payload = ";".join(",".join(map(str, row)) for row in sorted(rows))
    return sha256(payload.encode("ascii")).hexdigest()


def intervals(rows):
    out = {}
    for kappa in sorted({row[0] for row in rows}):
        ts = [row[1] for row in rows if row[0] == kappa]
        out[str(kappa)] = [min(ts), max(ts), len(ts)]
    return out


def main():
    thresholds = {k: anchor_threshold(k) for k in range(2, 775)}
    assert thresholds[2][0] == 890
    assert thresholds[3][0] == 1_780
    assert thresholds[128][0] == 113_686
    assert thresholds[400][0] == 1_200_745
    assert thresholds[600][0] == 3_077_757
    assert thresholds[774][0] == 8_060_986

    grid = []
    ri = []
    centroid = []
    old = []
    cubic = []
    for kappa in range(2, 775):
        h = thresholds[kappa][0]
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            row = (kappa, t, (kappa - 1) * t, kappa * t)
            grid.append(row)
            if rank_inertia_cut(kappa, t, h):
                ri.append(row)
            if centroid_cut(kappa, t):
                centroid.append(row)
            if pr529_cut(kappa, t) or pr495_infeasible(row[2], row[3]):
                old.append(row)
            if spectral_cubic_cut(kappa, t):
                cubic.append(row)

    ri_set = set(ri)
    centroid_set = set(centroid)
    union = sorted(ri_set | centroid_set)
    old_set = set(old)
    cubic_set = set(cubic)

    assert len(grid) == 3_254_885
    assert len(ri) == 153_483
    assert len(centroid) == 187
    assert len(ri_set & centroid_set) == 65
    assert len(union) == 153_605
    assert len(grid) - len(union) == 3_101_280
    assert len(old_set) == 97_546
    assert old_set <= set(union)
    assert len(set(union) - old_set) == 56_059
    assert len(cubic_set) == 108_582
    assert cubic_set <= set(union)

    assert row_hash(ri) == "f50806d868f320ce8239ea92d466a516253a50089991d862f18f51123e80ebaf"
    assert row_hash(centroid) == "358fc8532b53afbdc5cfbdf7b1baa7768cf8cf68f1859147c38cdc0ea2af6564"
    assert row_hash(ri_set & centroid_set) == "5a49088a6121f3ce4756b02a5e8156e0c5c234c772281f88ebc9d33c4b924095"
    assert row_hash(union) == "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da"
    assert row_hash(set(union) - old_set) == "b207f4a216f3dbe770f2a099e55a3380f8b20acad8a74beaa45b030c027c541c"

    union_intervals = intervals(union)
    assert union_intervals["2"] == [391_736, 490_564, 98_829]
    assert union_intervals["3"] == [232_118, 261_059, 28_942]
    assert union_intervals["4"] == [163_199, 174_039, 10_841]
    assert union_intervals["5"] == [125_332, 130_529, 5_198]

    # Boundary and bisection checks are independent of the row hashes.
    for kappa, (h, h2, h3) in thresholds.items():
        assert p_value(kappa, h2) <= 0
        assert h2 == 0 or p_value(kappa, h2 - 1) > 0
        assert t_value(kappa, h3) >= 0
        lower = ceil_div(Q * (kappa - 1), N - 2)
        assert h3 == lower or t_value(kappa, h3 - 1) < 0
        assert h == max(h2, h3)

    print("RESULT: PASS")
    print(f"grid={len(grid)} ri={len(ri)} centroid={len(centroid)} union={len(union)}")
    print(f"old_union={len(old_set)} new_rows={len(set(union) - old_set)} survivors={len(grid)-len(union)}")
    print(f"role02_cubic={len(cubic_set)} contained_in_rank_inertia={cubic_set <= set(union)}")
    print(f"union_sha256={row_hash(union)}")
    print(f"new_sha256={row_hash(set(union)-old_set)}")


if __name__ == "__main__":
    main()
