#!/usr/bin/env python3
"""Finite-field stress checks for agreement_weighted_transverse_secant.md."""

from itertools import combinations, product
from math import comb
from random import Random


def rank(rows, q):
    a = [list(row) for row in rows if any(x % q for x in row)]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c] % q), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c] % q, -1, q)
        a[r] = [(inv * x) % q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c] % q:
                f = a[i][c] % q
                a[i] = [(x - f * y) % q for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def in_column_space(G, b, indices, q):
    rows = [G[i] for i in indices]
    augmented = [G[i] + (b[i],) for i in indices]
    return rank(rows, q) == rank(augmented, q)


def stress(q, n, kappa, t, trials):
    assert n <= q
    G = [tuple(pow(x, j, q) for j in range(kappa)) for x in range(n)]
    assert all(rank([G[i] for i in I], q) == kappa
               for I in combinations(range(n), kappa))
    rng = Random(1000 * q + 100 * n + kappa)
    checked = 0

    for _ in range(trials):
        b0 = tuple(rng.randrange(q) for _ in range(n))
        b1 = tuple(rng.randrange(q) for _ in range(n))
        selected = {}
        trans_cache = {}

        for gamma in range(q):
            best = None
            for c in product(range(q), repeat=kappa):
                e = tuple(
                    (b0[x] + gamma * b1[x] +
                     sum(G[x][j] * c[j] for j in range(kappa))) % q
                    for x in range(n)
                )
                zeros = tuple(i for i, value in enumerate(e) if value == 0)
                if n - len(zeros) > t:
                    continue
                if zeros not in trans_cache:
                    trans_cache[zeros] = not (
                        in_column_space(G, b0, zeros, q) and
                        in_column_space(G, b1, zeros, q)
                    )
                if not trans_cache[zeros]:
                    continue
                score = comb(len(zeros) - 1, kappa) if len(zeros) > kappa else 0
                if best is None or score > best:
                    best = score
            if best is not None:
                selected[gamma] = best

        lhs = sum(selected.values())
        rhs = comb(n, kappa + 1)
        assert lhs <= rhs
        minimum = comb(n - t - 1, kappa)
        if minimum:
            assert len(selected) <= rhs // minimum
        checked += 1
    return checked


def main():
    rows = 0
    rows += stress(q=7, n=6, kappa=2, t=3, trials=60)
    rows += stress(q=11, n=7, kappa=3, t=3, trials=30)
    print(f"RESULT: PASS ({rows} deterministic full-spark chart stresses)")


if __name__ == "__main__":
    main()
