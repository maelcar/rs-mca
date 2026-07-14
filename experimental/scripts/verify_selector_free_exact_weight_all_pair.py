#!/usr/bin/env python3
"""Verify the selector-free exact-weight all-pair compiler.

The checker is deterministic, standard-library only, and fail-closed under
``python -O``.  It reuses the repository's pinned prime-field RS model.

Usage:
  python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --summary-only
  python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --check
  python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --tamper-selftest
"""

import argparse
import copy
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from math import comb
from pathlib import Path

import verify_selector_free_direction_distance_all_pair as rs


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/selector-free-exact-weight-all-pair"
    / "selector_free_exact_weight_all_pair.json"
)
BASE_SHA = "9262f63cf093a7510a2df435f220390f59e2bcd5"
SCHEMA = "selector-free-exact-weight-all-pair/v1"

FORMULAS = {
    "height": "h_j=max(1,d+j-t)",
    "Xi": "Xi_j=d(M-j)^2+M h_j^2-dM^2",
    "Xi_strict": "0<j<M and Xi_j>0 => |P_j|<=N-1",
    "Xi_equality": "0<j<M and Xi_j=0 => |P_j|<=2(N-2)",
    "Xi_endpoints": "|P_0|<=floor(d/h_0); Xi_M>=0 => |P_M|<=2d-1",
    "separation": "D_j=min(M,max(Delta,d+2j-2t))",
    "Q": "Q_j=M D_j-2 M j+j^2",
    "Q_words": "Q_j>0 => |W_j|<=floor(M(D_j-j)/Q_j)",
    "Q_pairs": "Q_j>0 => |P_j|<=floor(d/h_j) floor(M(D_j-j)/Q_j)",
}

HYPOTHESES = {
    "chart": "weighted Reed-Solomon parity columns at N distinct locators",
    "parameters": "N=R+kappa, kappa>=1, 0<=t<R",
    "direction": "y1!=0 and v is a minimum-weight y1 lift",
    "pairs": "finite distinct transverse (gamma,e) with He=y0+gamma y1 and wt(e)<=t",
    "kernel": "ker(H) is [N,kappa,R+1] MDS; Delta=R+1-d after puncturing supp(v)",
    "full_endpoint": "the j=M zero center uses R+1>t, not minimum-lift distance d alone",
}

SOURCES = {
    "base": BASE_SHA,
    "completed_zero_mask": {
        "path": "experimental/notes/thresholds/completed_zero_mask_two_block.md",
        "pin": "ea4eb0784417ca5ab503a3c31a7eef6464ad100a",
    },
    "exact_weight_predecessor": {
        "path": "experimental/notes/thresholds/low_direction_hybrid_exact_weight.md",
        "pin": "5c9aab794e6575d815541e0a5dd8534d03d400aa",
    },
    "all_pair_predecessor": {
        "path": "experimental/notes/thresholds/selector_free_direction_distance_all_pair.md",
        "pin": BASE_SHA,
    },
    "affine_core_predecessor": {
        "path": "experimental/notes/thresholds/all_lineray_affine_core_set_pair.md",
        "pin": BASE_SHA,
    },
}

NONCLAIMS = [
    "no positive-Q payment when Q_j<=0",
    "no interior completed-mask payment when Xi_j<0",
    "no theorem for arbitrary linear charts lacking kernel distance above t",
    "no hosted-chart extraction or witness-exhaustive atlas",
    "no complete profile-envelope or lower-reserve comparison",
    "no deployed finite-row or Grand MCA/List theorem",
]

EXPECTED_SWEEP = {
    "parameter_rows": 414_250,
    "nonempty_complete_families": 209_846,
    "exact_weight_strata": 310_632,
    "positive_Q_strata": 222_106,
}


class VerificationError(RuntimeError):
    """A fail-closed verification condition failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def height(d, j, t):
    return max(1, d + j - t)


def separation(M, Delta, d, t, j):
    return min(M, max(Delta, d + 2 * j - 2 * t))


def denominator(M, D, j):
    return M * D - 2 * M * j + j * j


def xi_value(d, M, t, j):
    h = height(d, j, t)
    return d * (M - j) ** 2 + M * h * h - d * M * M


def zero_set(vector, indices):
    return frozenset(index for index in indices if vector[index] == 0)


def direct_complete_family(q, N, R, y0, y1, t):
    matrix = rs.parity_matrix(q, N, R)
    errors = tuple(rs.low_weight_vectors(q, N, t))
    by_syndrome = defaultdict(list)
    for error in errors:
        by_syndrome[rs.mat_vec(matrix, error, q)].append(error)
    pairs = []
    for gamma in range(q):
        target = rs.add(y0, rs.scale(gamma, y1, q), q)
        for error in by_syndrome.get(target, ()):
            if rs.transverse(matrix, y0, y1, error, q):
                pairs.append((gamma, error))
    return matrix, tuple(pairs)


def check_minimum_lift(q, N, matrix, y1, v, label):
    d = rs.weight(v)
    require(rs.mat_vec(matrix, v, q) == y1, label + ": bad lift syndrome")
    for candidate in rs.low_weight_vectors(q, N, d - 1):
        require(
            rs.mat_vec(matrix, candidate, q) != y1,
            label + ": displayed lift is not minimum",
        )


def check_stratum(q, N, R, matrix, y0, y1, v, t, pairs, j, label):
    d = rs.weight(v)
    J = tuple(rs.support(v))
    I = tuple(index for index in range(N) if index not in set(J))
    M = len(I)
    Delta = R + 1 - d
    h = height(d, j, t)
    Xi = xi_value(d, M, t, j)
    D = separation(M, Delta, d, t, j)
    Q = denominator(M, D, j)

    Pj = tuple(
        pair for pair in pairs if rs.weight(rs.restrict(pair[1], I)) == j
    )
    require(Pj, label + ": empty stratum")
    clusters = defaultdict(list)
    lifts = {}
    masks = []

    for gamma, error in Pj:
        require(rs.weight(error) <= t, label + ": error exceeds t")
        require(
            rs.mat_vec(matrix, error, q)
            == rs.add(y0, rs.scale(gamma, y1, q), q),
            label + ": wrong syndrome",
        )
        require(
            rs.transverse(matrix, y0, y1, error, q),
            label + ": nontransverse pair",
        )
        affine = rs.subtract(error, rs.scale(gamma, v, q), q)
        word = rs.restrict(affine, I)
        require(word == rs.restrict(error, I), label + ": puncture identity failed")
        require(rs.mat_vec(matrix, affine, q) == y0, label + ": bad affine lift")
        if word in lifts:
            require(lifts[word] == affine, label + ": puncture lost injectivity")
        else:
            lifts[word] = affine
        clusters[word].append((gamma, error))
        X = zero_set(error, I)
        Y = zero_set(error, J)
        require(len(X) == M - j, label + ": wrong I-zero count")
        require(len(Y) >= h, label + ": J-zero demand failed")
        masks.append((gamma, error, X, Y))

    pair_checks = 0
    same_slope_checks = 0
    for first, second in combinations(masks, 2):
        gamma_a, error_a, X_a, Y_a = first
        gamma_b, error_b, X_b, Y_b = second
        difference = rs.subtract(error_a, error_b, q)
        require(any(difference), label + ": distinct pairs share an error")
        if gamma_a == gamma_b:
            same_slope_checks += 1
            require(
                rs.mat_vec(matrix, difference, q) == (0,) * R,
                label + ": same-slope difference left kernel",
            )
            require(rs.weight(difference) >= R + 1, label + ": MDS distance failed")
        else:
            quotient = rs.scale(pow((gamma_a - gamma_b) % q, -1, q), difference, q)
            require(rs.mat_vec(matrix, quotient, q) == y1, label + ": bad lift quotient")
            require(rs.weight(quotient) >= d, label + ": minimum-lift distance failed")
        common = len(X_a & X_b) + len(Y_a & Y_b)
        require(common <= M, label + ": all-pair common-zero cap failed")
        gram = M * d * common - d * (M - j) ** 2 - M * len(Y_a) * len(Y_b)
        require(gram <= -Xi, label + ": centered Gram inequality failed")
        pair_checks += 1

    maximum_cluster = 0
    for word, rows in clusters.items():
        require(rs.weight(word) == j, label + ": wrong realized weight")
        require(len({gamma for gamma, _ in rows}) == len(rows), label + ": cluster repeats slope")
        zero_masks = [zero_set(error, J) for _, error in rows]
        for first, second in combinations(zero_masks, 2):
            require(not (first & second), label + ": cluster zero masks overlap")
        require(len(rows) * h <= d, label + ": cluster floor failed")
        maximum_cluster = max(maximum_cluster, len(rows))

    words = tuple(sorted(clusters))
    representatives = [clusters[word][0] for word in words]
    for (word_a, pair_a), (word_b, pair_b) in combinations(
        tuple(zip(words, representatives)), 2
    ):
        actual = rs.weight(rs.subtract(word_a, word_b, q))
        require(actual >= Delta, label + ": punctured kernel distance failed")
        require(actual >= D, label + ": exact separation failed")
        X_a = zero_set(pair_a[1], I)
        X_b = zero_set(pair_b[1], I)
        require(len(X_a & X_b) <= M - D, label + ": support incidence failed")

    word_bound = None
    pair_bound = None
    if Q > 0:
        numerator = M * (D - j)
        require(D > j, label + ": positive Q did not force D>j")
        require(len(words) * Q <= numerator, label + ": incidence inequality failed")
        word_bound = numerator // Q
        pair_bound = (d // h) * word_bound
        require(len(words) <= word_bound, label + ": word floor failed")
        require(len(Pj) <= pair_bound, label + ": all-pair Q floor failed")

    xi_bound = None
    if j == 0:
        xi_bound = d // h
        require(len(Pj) <= xi_bound, label + ": zero endpoint failed")
    elif j == M:
        require(Q <= 0, label + ": Q must be nonpositive at j=M")
        if Xi >= 0:
            xi_bound = 2 * d - 1
            zero_centers = sum(len(Y) == d for _, _, _, Y in masks)
            require(zero_centers <= 1, label + ": repeated endpoint zero center")
            require(len(Pj) <= xi_bound, label + ": full endpoint failed")
    elif Xi > 0:
        xi_bound = N - 1
        require(len(Pj) <= xi_bound, label + ": strict Xi bound failed")
    elif Xi == 0:
        xi_bound = 2 * (N - 2)
        require(len(Pj) <= xi_bound, label + ": equality Xi bound failed")

    slopes = Counter(gamma for gamma, _ in Pj)
    return {
        "j": j,
        "pairs": len(Pj),
        "slopes": len(slopes),
        "same_slope_excess": sum(value - 1 for value in slopes.values()),
        "realized_words": len(words),
        "maximum_cluster": maximum_cluster,
        "h": h,
        "D": D,
        "Q": Q,
        "word_bound": word_bound,
        "pair_bound": pair_bound,
        "Xi": Xi,
        "Xi_bound": xi_bound,
        "pair_checks": pair_checks,
        "same_slope_checks": same_slope_checks,
    }


def check_family(q, N, R, matrix, y0, y1, v, t, pairs, label, check_lift=True):
    require(pairs, label + ": empty family")
    require(len(set(pairs)) == len(pairs), label + ": duplicate pair")
    if check_lift:
        check_minimum_lift(q, N, matrix, y1, v, label)
    J = tuple(rs.support(v))
    I = tuple(index for index in range(N) if index not in set(J))
    weights = sorted({rs.weight(rs.restrict(error, I)) for _, error in pairs})
    rows = tuple(
        check_stratum(q, N, R, matrix, y0, y1, v, t, pairs, j, label + f"/j={j}")
        for j in weights
    )
    if all(row["Xi"] >= 0 for row in rows):
        require(len(pairs) < 2 * N * N, label + ": global Xi compilation failed")
    return rows


def exhaustive_sweep():
    totals = Counter()
    for q in (2, 3, 5):
        for N in range(2, q + 1):
            for R in range(1, N):
                context = rs.SmallContext(q, N, R)
                for t in range(R):
                    for y1 in context.directions:
                        direction = context.direction_records[y1]
                        for y0 in context.target_vectors:
                            totals["parameter_rows"] += 1
                            pairs = rs.complete_pair_family(context, y0, y1, t)
                            if not pairs:
                                continue
                            totals["nonempty_complete_families"] += 1
                            rows = check_family(
                                q, N, R, context.matrix, y0, y1,
                                direction["v"], t, pairs,
                                f"sweep-F{q}-N{N}-R{R}-t{t}",
                                check_lift=False,
                            )
                            totals["exact_weight_strata"] += len(rows)
                            totals["positive_Q_strata"] += sum(row["Q"] > 0 for row in rows)
    for key, expected in EXPECTED_SWEEP.items():
        require(totals[key] == expected, f"sweep {key} changed: {totals[key]} != {expected}")
    return {
        "fields": [2, 3, 5],
        "scope": "all 2<=N<=q, 1<=R<N, 0<=t<R, normalized y1!=0, every y0",
        **EXPECTED_SWEEP,
        "violations": 0,
    }


def fixture_summary():
    f5_y0 = (1, 0, 1)
    f5_y1 = (0, 1, 3)
    f5_v = (0, 4, 1, 0)
    f5_expected = {
        (1, (0, 0, 2, 4)),
        (2, (4, 2, 0, 0)),
        (4, (4, 0, 2, 0)),
        (4, (0, 2, 0, 4)),
    }
    matrix5, pairs5 = direct_complete_family(5, 4, 3, f5_y0, f5_y1, 2)
    require(set(pairs5) == f5_expected, "F5 complete family changed")
    rows5 = check_family(5, 4, 3, matrix5, f5_y0, f5_y1, f5_v, 2, pairs5, "F5")
    require(len(rows5) == 1, "F5 gained another stratum")
    f5 = rows5[0]
    require(
        (f5["j"], f5["pairs"], f5["slopes"], f5["realized_words"], f5["Q"], f5["Xi"])
        == (1, 4, 3, 2, 1, -4),
        "F5 sharp metrics changed",
    )

    f7_y0 = (0, 1, 0)
    f7_y1 = (0, 0, 1)
    f7_v = (0, 0, 0, 0, 4, 6, 4)
    f7_expected = {
        (1, (6, 1, 0, 0, 0, 0, 0)),
        (2, (3, 0, 4, 0, 0, 0, 0)),
        (3, (2, 0, 0, 5, 0, 0, 0)),
        (3, (0, 6, 1, 0, 0, 0, 0)),
        (4, (0, 3, 0, 4, 0, 0, 0)),
        (5, (0, 0, 6, 1, 0, 0, 0)),
    }
    matrix7, pairs7 = direct_complete_family(7, 7, 3, f7_y0, f7_y1, 2)
    rows7 = check_family(7, 7, 3, matrix7, f7_y0, f7_y1, f7_v, 2, pairs7, "F7")
    J7 = set(rs.support(f7_v))
    I7 = tuple(index for index in range(7) if index not in J7)
    stratum7 = {
        pair for pair in pairs7 if rs.weight(rs.restrict(pair[1], I7)) == 2
    }
    require(stratum7 == f7_expected, "F7 equality stratum changed")
    f7 = next(row for row in rows7 if row["j"] == 2)
    require(
        (f7["pairs"], f7["slopes"], f7["Xi"], f7["Xi_bound"])
        == (6, 5, 0, 10),
        "F7 equality metrics changed",
    )

    q = 37
    matrix = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 1))
    y0 = (0, 0, 0)
    y1 = (1, 1, 0)
    v = (1, 1, 0, 0)
    bad_pairs = tuple((0, (0, 0, a, (-a) % q)) for a in range(1, q))
    check_minimum_lift(q, 4, matrix, y1, v, "F37-boundary")
    for _, error in bad_pairs:
        require(rs.mat_vec(matrix, error, q) == y0, "F37 syndrome changed")
        require(rs.transverse(matrix, y0, y1, error, q), "F37 lost transversality")
    require(xi_value(2, 2, 2, 2) == 0, "F37 Xi changed")
    require(len(bad_pairs) == 36 > 3, "F37 no longer falsifies weakened endpoint")

    return {
        "F5_positive_Q_sharp": {
            "q": 5, "N": 4, "R": 3, "t": 2, "d": 2, "M": 2,
            "j": 1, "pairs": 4, "slopes": 3, "realized_words": 2,
            "maximum_cluster": 2, "h": 1, "D": 2, "Q": 1,
            "word_bound": 2, "pair_bound": 4, "Xi": -4,
        },
        "F7_Xi_equality_all_pair": {
            "q": 7, "N": 7, "R": 3, "t": 2, "d": 3, "M": 4,
            "j": 2, "pairs": 6, "slopes": 5, "Xi": 0, "Xi_bound": 10,
        },
        "F37_endpoint_boundary": {
            "q": 37, "N": 4, "t": 2, "d": 2, "M": 2, "j": 2,
            "Xi": 0, "same_slope_pairs": 36, "weakened_bound": 3,
            "kernel_distance": 2, "required_distance": 3,
        },
    }


def route_cut_fixture(q, t, kappa):
    N = t + kappa + 1
    R = t + 1
    require(N <= q, "route-cut fixture has colliding locators")
    matrix = rs.parity_matrix(q, N, R)
    y0 = tuple(int(index == t - 1) for index in range(R))
    y1 = tuple(int(index == t) for index in range(R))
    constructed = []
    for support in combinations(range(N), t):
        error = [0] * N
        for point in support:
            derivative = 1
            for other in support:
                if other != point:
                    derivative = derivative * (point - other) % q
            error[point] = pow(derivative, -1, q)
        error = tuple(error)
        gamma = sum(support) % q
        expected = rs.add(y0, rs.scale(gamma, y1, q), q)
        require(rs.mat_vec(matrix, error, q) == expected, "route-cut moment identity failed")
        require(rs.transverse(matrix, y0, y1, error, q), "route-cut transversality failed")
        constructed.append((gamma, error))

    require(len(constructed) == comb(N, t), "route-cut binomial family size failed")
    _, complete = direct_complete_family(q, N, R, y0, y1, t)
    require(set(complete) == set(constructed), "route-cut complete family changed")
    for candidate in rs.low_weight_vectors(q, N, t):
        require(rs.mat_vec(matrix, candidate, q) != y1, "route direction gained a short lift")
    first_basis = rs.matrix_columns(matrix, tuple(range(R)))
    require(rs.matrix_rank(first_basis, q) == R, "route direction lost an R-support lift")
    return {
        "q": q,
        "N": N,
        "R": R,
        "t": t,
        "kappa": kappa,
        "pairs": len(constructed),
        "expected_pairs": comb(N, t),
        "complete": True,
    }


def arithmetic_summary():
    for r in range(1, 501):
        N, R, t, d, M, Delta, j = 20*r, 11*r, 6*r, 10*r, 10*r, r+1, 5*r
        h, D = height(d, j, t), separation(M, Delta, d, t, j)
        Q = denominator(M, D, j)
        DH = (N - t) ** 2 - N * (N - d)
        DJ = M * Delta - 2 * M * t + t * t
        require((h, D, Q, DH, DJ) == (9*r, 8*r, 5*r*r, -4*r*r, -74*r*r+10*r), "20r identity failed")
        require(M * (D - j) // Q == 6 and d // h == 1, "20r floor changed")

    sums = {}
    for m in range(1, 501):
        N, R, t, d, M, Delta = 90*m, 86*m, 31*m, 50*m, 40*m, 36*m+1
        DH = (N - t) ** 2 - N * (N - d)
        DJ = M * Delta - 2 * M * t + t * t
        require(DH == -119*m*m and DJ == m*(40-79*m), "90m denominator failed")
        total = 0
        minimum = None
        for j in range(0, t + 1):
            D = separation(M, Delta, d, t, j)
            Q = denominator(M, D, j)
            require(Q > 0, "90m has nonpositive exact Q")
            minimum = Q if minimum is None else min(minimum, Q)
            total += (d // height(d, j, t)) * (M * (D - j) // Q)
        require(minimum == 81*m*m and total <= 112*m+2, "90m exact sum failed")
        if m in (1, 2, 5, 10, 200):
            sums[str(m)] = total

    samples = {}
    for r in range(1, 501):
        N, t, d, M = 500*r, 150*r, 250*r, 250*r
        for j in (15*r, 50*r, 75*r, 100*r, 111*r):
            require(xi_value(d, M, t, j) == 500*r*(j-50*r)*(j-100*r), "500r factorization failed")
        strict = 46*r
        equality = 2
        total = strict*(N-1) + equality*2*(N-2)
        require(total == 23000*r*r+1954*r-8, "500r total failed")
        if r in (1, 500):
            samples[str(r)] = total

    for t in range(2, 101):
        for kappa in range(1, 101):
            rho = min(t, kappa)
            require(1-kappa*(t-1) <= 0, "route-cut DH became positive")
            require(kappa*(1-2*rho)+rho*rho <= 0, "route-cut DJ became positive")
        if t % 2 == 0:
            j = t // 2
            require(t - 3*t*t//4 < 0, "route-cut Q became nonnegative")
            require(-t**3//2 + t*t//4 + t < 0, "route-cut Xi became nonnegative")

    route_fixtures = [
        route_cut_fixture(5, 2, 2),
        route_cut_fixture(7, 3, 3),
    ]

    return {
        "multiplicity_20r": {
            "parameters": "(20r,11r,9r,6r,10r,10r,r+1,5r)",
            "h": "9r", "D": "8r", "Q": "5r^2", "pair_bound": 6,
            "D_H": "-4r^2", "D_J": "-74r^2+10r", "r_sweep": [1, 500],
        },
        "selector_complete_90m": {
            "parameters": "(90m,86m,4m,31m,50m,40m,36m+1)",
            "minimum_Q": "81m^2", "summed_bound": "<=112m+2",
            "D_H": "-119m^2", "D_J": "m(40-79m)",
            "m_sweep": [1, 500], "sum_samples": sums,
        },
        "central_500r": {
            "parameters": "(500r,275r,225r,150r,250r,250r,25r+1)",
            "Xi": "500r(j-50r)(j-100r)",
            "paid_windows": ["15r<=j<=50r", "100r<=j<=111r"],
            "summed_bound": "23000r^2+1954r-8", "r_sweep": [1, 500],
            "bound_samples": samples,
        },
        "route_cut": {
            "parameters": "N=t+kappa+1,R=t+1,d=t+1,M=kappa,Delta=1",
            "family_size": "binom(N,t)", "D_H": "1-kappa(t-1)",
            "D_J": "kappa(1-2rho)+rho^2, rho=min(t,kappa)",
            "symmetric_Q": "t-3t^2/4<0", "symmetric_Xi": "-t^3/2+t^2/4+t<0",
            "grid": "2<=t<=100,1<=kappa<=100",
            "finite_fixtures": route_fixtures,
        },
    }


def compute_summary():
    return {
        "theorem": "selector-free exact-weight two-block all-pair compiler",
        "exhaustive_small_fields": exhaustive_sweep(),
        "fixtures": fixture_summary(),
        "arithmetic": arithmetic_summary(),
    }


def expected_certificate(summary):
    return {
        "schema": SCHEMA,
        "status": "PROVED",
        "lean_status": "UNPROVED STATEMENT TARGET",
        "hard_input": 3,
        "theorem": summary["theorem"],
        "formulas": FORMULAS,
        "hypotheses": HYPOTHESES,
        "sources": SOURCES,
        "computed_summary": summary,
        "nonclaims": NONCLAIMS,
    }


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise VerificationError("nonstandard JSON constant: " + value)


def load_certificate():
    require(CERTIFICATE.is_file(), "certificate is missing")
    try:
        return json.loads(
            CERTIFICATE.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_constant,
        )
    except (OSError, json.JSONDecodeError) as error:
        raise VerificationError("cannot parse certificate: " + str(error)) from error


def strict_equal(first, second):
    if type(first) is not type(second):
        return False
    if isinstance(first, dict):
        return first.keys() == second.keys() and all(strict_equal(first[key], second[key]) for key in first)
    if isinstance(first, list):
        return len(first) == len(second) and all(strict_equal(a, b) for a, b in zip(first, second))
    return first == second


def validate_certificate(payload, summary):
    expected = expected_certificate(summary)
    require(type(payload) is dict, "certificate root is not an object")
    require(payload.keys() == expected.keys(), "certificate top-level keys changed")
    require(strict_equal(payload, expected), "certificate differs from recomputed evidence")


def tamper_selftest(summary):
    pristine = load_certificate()
    validate_certificate(pristine, summary)
    mutations = []
    for path, value in (
        (("status",), "CONDITIONAL"),
        (("hard_input",), True),
        (("formulas", "Xi_strict"), "tampered"),
        (("hypotheses", "full_endpoint"), "distance d is enough"),
        (("sources", "base"), "0" * 40),
        (("computed_summary", "fixtures", "F5_positive_Q_sharp", "pairs"), 5),
        (("computed_summary", "exhaustive_small_fields", "positive_Q_strata"), 0),
    ):
        changed = copy.deepcopy(pristine)
        cursor = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutations.append(changed)
    changed = copy.deepcopy(pristine)
    changed["unexpected"] = 1
    mutations.append(changed)
    rejected = 0
    for payload in mutations:
        try:
            validate_certificate(payload, summary)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "a certificate tamper was accepted")
    for text in ('{"x":1,"x":1}', '{"x":NaN}'):
        try:
            json.loads(text, object_pairs_hook=reject_duplicate_keys, parse_constant=reject_constant)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations) + 2, "a parser tamper was accepted")
    return {"tamper_cases": len(mutations) + 2, "rejected": rejected}


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--summary-only", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        summary = compute_summary()
        if args.summary_only:
            output = summary
        elif args.check:
            validate_certificate(load_certificate(), summary)
            output = {"status": "ok", "summary": summary}
        else:
            output = {"status": "ok", **tamper_selftest(summary)}
        print(json.dumps(output, indent=2, sort_keys=True))
        return 0
    except (VerificationError, ValueError) as error:
        print("verification failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
