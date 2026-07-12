#!/usr/bin/env python3
"""Exact finite checks for syndrome_secant_challenge_lower.md."""

from itertools import combinations, product
from math import comb, ceil


def add(u, v, q):
    return tuple((x + y) % q for x, y in zip(u, v))


def scale(a, u, q):
    return tuple(a * x % q for x in u)


def span(columns, q, R):
    out = {(0,) * R}
    for column in columns:
        out = {add(x, scale(a, column, q), q) for x in out for a in range(q)}
    return out


def s_value(q, n, k, a):
    R = n - k
    t = n - a
    return sum(
        comb(t, j) * comb(n - t, t - j) * q ** max(j, 2 * t - R)
        for j in range(t + 1)
        if 0 <= t - j <= n - t
    )


def lower_bound(q, n, k, a, G):
    R = n - k
    t = n - a
    N = comb(n, t)
    numerator = G * N * q ** (2 * t) * (q**R - q**t)
    denominator = q ** (2 * R) * s_value(q, n, k, a)
    return (numerator + denominator - 1) // denominator


def brute_max(q, n, k, a, gamma):
    R = n - k
    t = n - a
    columns = [tuple(pow(x, j, q) for j in range(R)) for x in range(n)]
    spaces = [span([columns[i] for i in E], q, R) for E in combinations(range(n), t)]
    vectors = list(product(range(q), repeat=R))
    membership = {}
    for y in vectors:
        mask = 0
        for i, space in enumerate(spaces):
            if y in space:
                mask |= 1 << i
        membership[y] = mask

    best = 0
    for y0 in vectors:
        for y1 in vectors:
            bad = 0
            for g in gamma:
                y = add(y0, scale(g, y1, q), q)
                if membership[y] & ~membership[y1]:
                    bad += 1
            best = max(best, bad)
    return best


def run_case(q, n, k, a):
    R = n - k
    t = n - a
    N = comb(n, t)
    S = s_value(q, n, k, a)

    # Independently rebuild the exact second moment from subspace intersections.
    direct = 0
    tsets = list(combinations(range(n), t))
    for E in tsets:
        for F in tsets:
            j = len(set(E) & set(F))
            direct += q ** max(j, 2 * t - R)
    assert direct == N * S

    gamma = tuple(range(q))
    bound = lower_bound(q, n, k, a, len(gamma))
    exact = brute_max(q, n, k, a, gamma)
    assert exact >= bound

    if a == k + 1:
        adjacent = ceil(len(gamma) * (q - 1) * comb(n, k + 1) /
                        (q * (comb(n, k + 1) + q - 1)))
        assert bound == adjacent
    return S, bound, exact


def main():
    rows = [
        (5, 4, 1, 2),
        (7, 5, 2, 3),
    ]
    results = [run_case(*row) for row in rows]
    assert results == [(50, 3, 5), (112, 4, 7)]
    print(f"RESULT: PASS ({len(rows)} exhaustive rows; {results})")


if __name__ == "__main__":
    main()
