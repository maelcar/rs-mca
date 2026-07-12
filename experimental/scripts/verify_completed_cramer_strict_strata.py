#!/usr/bin/env python3
"""Exact arithmetic checks for completed_cramer_strict_strata.md."""

from math import comb


def C(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def cramer_bound(N, R, t, d, e):
    kappa = N - R
    M = N - d
    Delta = R + 1 - d
    h = max(1, d + e - t)
    if e <= Delta - 1:
        den = h * C(M - e, kappa)
        assert den > 0
        return d * C(M, kappa) // den, 1
    return C(M, e) * C(d, e - Delta + 2), 2


def main():
    checked = 0
    strict_w1 = 0
    strict_w2 = 0
    for N in range(4, 70):
        for R in range(2, N):
            for t in range(1, R):
                for d in range(1, R + 1):
                    M = N - d
                    kappa = N - R
                    Delta = R + 1 - d
                    assert Delta == M - kappa + 1
                    for e in range(min(t, M) + 1):
                        B, case = cramer_bound(N, R, t, d, e)
                        if case == 1:
                            assert B <= N ** (e + 1)
                        else:
                            assert B <= N ** (2 * e + 2)

                        q_e = d + 2 * e - 2 * t
                        J_e = e * e - 2 * M * e + M * q_e
                        if q_e <= Delta and J_e < 0:
                            strict_w1 += 1
                        if Delta < q_e < M and e * e < M * (2 * t - d):
                            strict_w2 += 1
                        checked += 1

    for m in range(4, 34, 2):
        N, R, d, e = 2 * m, m + 1, m, 2
        M, Delta = N - d, R + 1 - d

        t = m // 2 + 1
        q_e = d + 2 * e - 2 * t
        J_e = e * e - 2 * M * e + M * q_e
        assert q_e <= Delta and J_e < 0
        assert cramer_bound(N, R, t, d, e)[0] <= N ** (e + 1)

    for m in range(5, 34, 2):
        N, R, d, e = 2 * m, m + 1, m, 2
        M, Delta = N - d, R + 1 - d
        t = (m + 1) // 2
        q_e = d + 2 * e - 2 * t
        assert Delta < q_e < M and e * e < M * (2 * t - d)
        assert cramer_bound(N, R, t, d, e)[0] <= N ** (2 * e + 2)

    assert strict_w1 and strict_w2
    print(
        "RESULT: PASS "
        f"({checked} parameter rows; strict W1-={strict_w1}, W2-={strict_w2})"
    )


if __name__ == "__main__":
    main()
