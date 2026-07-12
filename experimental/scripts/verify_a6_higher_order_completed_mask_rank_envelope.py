#!/usr/bin/env python3
"""Checks for the higher-order completed-mask A6 rank envelope."""
from __future__ import annotations

from itertools import combinations, product


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def weight(vec: tuple[int, ...]) -> int:
    return sum(x != 0 for x in vec)


def mat_vec(H: list[list[int]], v: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple(sum(row[j] * v[j] for j in range(len(v))) % p for row in H)


def rank_mod(rows: list[list[int]], p: int) -> int:
    A = [[x % p for x in row] for row in rows]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if A[i][col]), None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(A[rank][col], -1, p)
        A[rank] = [(x * inv) % p for x in A[rank]]
        for i in range(m):
            if i != rank and A[i][col]:
                factor = A[i][col]
                A[i] = [
                    (A[i][j] - factor * A[rank][j]) % p for j in range(n)
                ]
        rank += 1
        if rank == m:
            break
    return rank


def in_column_span(
    H: list[list[int]], columns: tuple[int, ...], y: tuple[int, ...], p: int
) -> bool:
    base = [[H[i][j] for j in columns] for i in range(len(H))]
    augmented = [base[i] + [y[i]] for i in range(len(H))]
    return rank_mod(base, p) == rank_mod(augmented, p)


def null_vector_full_rank(matrix: list[list[int]], p: int) -> tuple[int, ...]:
    """Return a nonzero null vector for an m x (m+1) full-row-rank matrix."""
    m, n = len(matrix), len(matrix[0])
    require(n == m + 1 and rank_mod(matrix, p) == m, "nullspace shape/rank")
    # Solve the first m variables with the last variable fixed to 1.
    A = [[matrix[i][j] % p for j in range(m)] + [(-matrix[i][m]) % p] for i in range(m)]
    row = 0
    pivots: list[int] = []
    for col in range(m):
        pivot = next(i for i in range(row, m) if A[i][col])
        A[row], A[pivot] = A[pivot], A[row]
        inv = pow(A[row][col], -1, p)
        A[row] = [(x * inv) % p for x in A[row]]
        for i in range(m):
            if i != row and A[i][col]:
                factor = A[i][col]
                A[i] = [(A[i][j] - factor * A[row][j]) % p for j in range(m + 1)]
        pivots.append(col)
        row += 1
    sol = [0] * m
    for i, col in enumerate(pivots):
        sol[col] = A[i][m]
    result = tuple(sol + [1])
    require(
        all(sum(matrix[i][j] * result[j] for j in range(n)) % p == 0 for i in range(m)),
        "null vector",
    )
    return result


def check_explicit_family(max_r: int = 1000) -> dict[str, int]:
    """Exhaust every physical exact weight for r <= max_r.

    Family:
      (N,R,kappa,t,d)=(15r,9r,6r,3r,5r), M=10r, Delta=4r+1.
    """
    rows = negative_rows = strict_rows = w1_rows = w2_rows = 0
    for r in range(1, max_r + 1):
        N, R, kappa, t, d = 15 * r, 9 * r, 6 * r, 3 * r, 5 * r
        M = N - d
        Delta = R + 1 - d
        for e in range(t + 1):  # e <= wt(c_gamma) <= t
            rows += 1
            h = max(1, d + e - t)
            Xi = d * (M - e) ** 2 + M * h**2 - d * M**2
            require(Xi == 5 * r * (3 * e**2 - 12 * e * r + 8 * r**2), "Xi formula")
            q = d + 2 * e - 2 * t
            D = min(M, max(Delta, q))
            J = e**2 - 2 * M * e + M * D
            W1 = q <= Delta and J < 0
            W2 = Delta < q < M and e**2 < M * (2 * t - d)
            C3 = max(0, M - 3 * e) + max(0, 3 * h - 2 * d)
            strict = W1 or W2
            expected_strict = (10 * r - e) ** 2 < 10 * r * (6 * r - 1)
            require(strict == expected_strict, "strict dispatcher interval")
            require(C3 >= 6 * r > kappa - 1, "three-mask rank collapse")
            if Xi < 0:
                negative_rows += 1
                require(e > 0, "negative Xi endpoint")
            if strict:
                strict_rows += 1
                require(Xi < 0, "strict branch must have negative Xi")
                require(W1 ^ W2, "strict W1/W2 disjointness")
                if W1:
                    w1_rows += 1
                else:
                    w2_rows += 1
    return {
        "r_values": max_r,
        "physical_exact_weight_rows": rows,
        "Xi_negative_rows": negative_rows,
        "strict_W1_or_W2_negative_rows": strict_rows,
        "strict_W1_negative_rows": w1_rows,
        "strict_W2_negative_rows": w2_rows,
    }


def check_actual_weighted_rs_sharp_example() -> dict[str, object]:
    """Construct an actual F_17 weighted-RS r=1 target stratum with two slopes."""
    p, N, R = 17, 15, 9
    points = tuple(range(N))
    H = [[pow(x, i, p) for x in points] for i in range(R)]
    W = tuple(range(10))
    H_W = [[H[i][j] for j in W] for i in range(R)]
    k_W = null_vector_full_rank(H_W, p)
    require(all(k_W), "minimum GRS kernel word has full ten-point support")
    k = tuple(k_W[j] if j < 10 else 0 for j in range(N))
    require(mat_vec(H, k, p) == (0,) * R and weight(k) == 10, "GRS kernel word")

    J = tuple(range(5))
    Z = tuple(range(5, 10))
    v = tuple((-k[j]) % p if j in J else 0 for j in range(N))
    z = tuple(k[j] if j in Z else 0 for j in range(N))
    y1 = mat_vec(H, v, p)
    require(y1 == mat_vec(H, z, p) and weight(v) == weight(z) == 5, "equal syndrome lifts")

    # No lift on <=4 columns: hence the minimum lift weight is exactly d=5.
    for size in range(5):
        for cols in combinations(range(N), size):
            require(not in_column_span(H, cols, y1, p), "minimum lift weight")

    pivot, A, B = Z[0], Z[1:3], Z[3:5]
    c0 = [0] * N
    c1 = [0] * N
    for j in A:
        c0[j] = (-z[j]) % p
    for j in B:
        c1[j] = z[j]
    a = 1
    while (a + z[pivot]) % p == 0:
        a += 1
    c0[pivot] = a % p
    c1[pivot] = (a + z[pivot]) % p
    c0_t, c1_t = tuple(c0), tuple(c1)
    require(tuple((c1_t[j] - c0_t[j]) % p for j in range(N)) == z, "pencil difference")
    require(weight(c0_t) == weight(c1_t) == 3, "witness weights")
    require(sum(c0_t[j] != 0 for j in range(N) if j not in J) == 3, "first punctured weight")
    require(sum(c1_t[j] != 0 for j in range(N) if j not in J) == 3, "second punctured weight")
    y0 = mat_vec(H, c0_t, p)
    require(
        mat_vec(H, c1_t, p) == tuple((y0[i] + y1[i]) % p for i in range(R)),
        "syndrome line",
    )

    # Transversality follows because y1 is not spanned by any 3 support columns.
    for c in (c0_t, c1_t):
        supp = tuple(i for i, value in enumerate(c) if value)
        require(not in_column_span(H, supp, y1, p), "transversality")

    pencil_weights = {
        gamma: weight(tuple((c0_t[j] + gamma * z[j]) % p for j in range(N)))
        for gamma in range(p)
    }
    require(
        tuple(gamma for gamma, value in pencil_weights.items() if value <= 3) == (0, 1),
        "exact low-weight slopes",
    )

    Xi = 5 * (3 * 3**2 - 12 * 3 + 8)
    require(Xi == -5, "sharp-example Xi")
    return {
        "field": "F_17",
        "parameters": (N, R, N - R, 3, 5),
        "punctured_weight": 3,
        "Xi": Xi,
        "slopes": (0, 1),
        "witness_weights": (weight(c0_t), weight(c1_t)),
        "exact_low_weight_slopes": (0, 1),
        "result": "actual target stratum; bound 2 attained",
    }


def check_canonical_stress_hcm(max_r: int = 200) -> dict[str, int]:
    """Check the exact all-order HCM slack on the canonical central band."""
    rows = 0
    for r in range(1, max_r + 1):
        kappa = 225 * r
        for e in range(50 * r + 1, 100 * r):
            rows += 1

            def c(j: int) -> int:
                return max(0, 250 * r - (j + 1) * e) + max(
                    0, 100 * r - 150 * j * r + (j + 1) * e
                )

            require(c(2) <= 100 * r < kappa - 1, "canonical C2 slack")
            require(c(3) <= 50 * r < kappa - 2, "canonical C3 slack")
            require(c(4) == 0, "canonical C4 vanishing")
            # For j>=4, both affine terms decrease in j on this band.
            require(c(kappa + 1) == 0, "canonical terminal HCM vanishing")
    return {"r_values": max_r, "central_band_rows": rows}


def check_no_collinear_shortcut_tamper() -> dict[str, object]:
    """Falsify the tempting shortcut 2d>=3t => no three collinear witnesses."""
    p, R = 5, 3
    points = (0, 1, 2, 3)
    H = [[pow(x, i, p) for x in points] for i in range(R)]
    v = (1, 1, 1, 0)
    c0 = (0, 4, 3, 0)
    witnesses = (
        c0,
        tuple((c0[j] + v[j]) % p for j in range(4)),
        tuple((c0[j] + 2 * v[j]) % p for j in range(4)),
    )
    y1 = mat_vec(H, v, p)
    minimum = 5
    for w in product(range(p), repeat=4):
        if mat_vec(H, w, p) == y1:
            minimum = min(minimum, weight(w))
    require(minimum == 3, "tamper minimum lift")
    require(tuple(weight(c) for c in witnesses) == (2, 2, 2), "tamper witness weights")
    require(2 * minimum == 3 * 2, "tamper equality surface")
    return {
        "field": "F_5",
        "N": 4,
        "R": 3,
        "t": 2,
        "d": minimum,
        "witness_weights": tuple(weight(c) for c in witnesses),
        "slopes": (0, 1, 2),
        "result": "tamper rejected; collinear branch must be handled",
    }


def main() -> None:
    guard_rejected = False
    try:
        require(False, "guard self-test")
    except VerificationError:
        guard_rejected = True
    require(guard_rejected, "always-active guard")
    print(f"always-active guard ({'normal' if __debug__ else 'optimized'} mode): PASS")
    print("three-mask explicit family: PASS", check_explicit_family())
    print("actual weighted-RS sharp example: PASS", check_actual_weighted_rs_sharp_example())
    print("canonical all-order HCM stress: PASS", check_canonical_stress_hcm())
    print("no-collinear shortcut tamper: PASS", check_no_collinear_shortcut_tamper())
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
