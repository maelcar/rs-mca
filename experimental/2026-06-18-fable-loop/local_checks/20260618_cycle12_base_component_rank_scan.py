#!/usr/bin/env python3
"""Base-component scan for the Cycle 12 t=2, j=3 incidence wall.

Status: EXPERIMENTAL / AUDIT.

Cycle 12 records the bad-line landing condition as one F-valued quadric

    Delta(tau1,tau2,tau3)=0

with tau_i in B=F_p and F=F_{p^2}.  This script checks the alternative lens
that matters over the generated/base field: an F-valued equation on B-variables
is normally two B-valued quadratic equations.  If the two components have no
common surface factor, the landing set should be curve-sized, O(p), before any
slope-fiber argument is needed.

The script is not a proof.  It records finite evidence for the coefficient-rank
and landing-count form of the wall.
"""

from itertools import combinations, product
import importlib.util
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
PREV = ROOT / "20260618_cycle12_t2_j3_line_incidence_scan.py"
spec = importlib.util.spec_from_file_location("cycle12", PREV)
c12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c12)
c11 = c12.c11


MONOMIALS_DEG_LE_2 = [
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (2, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (0, 2, 0),
    (0, 1, 1),
    (0, 0, 2),
]


def monomial_value(exp, x, y, z, p):
    a, b, c = exp
    return (pow(x, a, p) * pow(y, b, p) * pow(z, c, p)) % p


def solve_mod_p(rows, rhs, p):
    """Solve an overdetermined full-rank linear system over F_p."""
    mat = [list(row) + [val % p] for row, val in zip(rows, rhs)]
    m = len(mat)
    n = len(rows[0])
    pivots = []
    r = 0
    for col in range(n):
        pivot = None
        for i in range(r, m):
            if mat[i][col] % p:
                pivot = i
                break
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        inv = pow(mat[r][col] % p, p - 2, p)
        mat[r] = [(v * inv) % p for v in mat[r]]
        for i in range(m):
            if i != r and mat[i][col] % p:
                factor = mat[i][col] % p
                mat[i] = [(mat[i][j] - factor * mat[r][j]) % p for j in range(n + 1)]
        pivots.append(col)
        r += 1
        if r == n:
            break

    for row in mat:
        if all(v % p == 0 for v in row[:n]) and row[n] % p:
            raise AssertionError("inconsistent interpolation system")

    sol = [0] * n
    for i, col in enumerate(pivots):
        sol[col] = mat[i][n] % p
    return sol


def coefficient_line_rank(coeff_pairs, p):
    """Rank over B of the coefficient vectors in F=B+alpha B."""
    first = None
    for u, v in coeff_pairs:
        if u % p or v % p:
            first = (u % p, v % p)
            break
    if first is None:
        return 0
    for u, v in coeff_pairs:
        if (first[0] * (v % p) - first[1] * (u % p)) % p:
            return 2
    return 1


def delta_for_tau(Wres, LDres, Bres, E, W, D1, D2, n, tau1, tau2, tau3):
    LT = c11.trim([c11.fneg(tau3), tau2, c11.fneg(tau1), c11.one])
    Q = c12.q_formula_j3(W, n, D1, D2, tau1, tau2)
    LTres = c11.residue2(LT, E)
    Qres = c11.residue2(Q, E)
    Pres = c11.rsub(c11.rmul(Wres, LTres, E), c11.rmul(LDres, Qres, E))
    Bpp = c11.rmul(Bres, LTres, E)
    return c11.wedge(Pres, Bpp)


def run_trial(p, nr, seed):
    c11.set_field(p, nr)
    rng = random.Random(seed)
    D = [c11.b(x) for x in range(p)]
    n = len(D)

    E = c11.random_separated_quadratic(rng)
    bnum = c11.random_bnum(rng)
    bnum_res = c11.residue2(bnum, E)

    w0 = [c11.b(rng.randrange(p)) for _ in D]
    w1 = [c11.b(rng.randrange(p)) for _ in D]
    w = [c11.fadd(w0[i], c11.fmul(c11.alpha, w1[i])) for i in range(n)]
    W = c11.interp(D, w)
    LD = c11.locator(D)
    D1 = c12.sum_points(D)
    D2 = c12.elem2(D)
    Wres = c11.residue2(W, E)
    LDres = c11.residue2(LD, E)
    Bres = c11.residue2(bnum, E)

    rows = []
    rhs0 = []
    rhs1 = []
    zeros_all = 0
    for x, y, z in product(range(p), repeat=3):
        rows.append([monomial_value(exp, x, y, z, p) for exp in MONOMIALS_DEG_LE_2])
        val = delta_for_tau(Wres, LDres, Bres, E, W, D1, D2, n, c11.b(x), c11.b(y), c11.b(z))
        rhs0.append(val[0])
        rhs1.append(val[1])
        if val == c11.zero:
            zeros_all += 1

    coeff0 = solve_mod_p(rows, rhs0, p)
    coeff1 = solve_mod_p(rows, rhs1, p)
    coeff_rank = coefficient_line_rank(list(zip(coeff0, coeff1)), p)

    slopes = {}
    zeros_split = 0
    for idxs in combinations(range(n), 3):
        T = [D[i] for i in idxs]
        tau1 = c12.sum_points(T)
        tau2 = c12.elem2(T)
        tau3 = c12.elem3(T)
        if delta_for_tau(Wres, LDres, Bres, E, W, D1, D2, n, tau1, tau2, tau3) != c11.zero:
            continue
        zeros_split += 1
        LT = c11.locator(T)
        Ls, rem = c11.pdivmod(LD, LT)
        if rem != [c11.zero]:
            raise AssertionError("L_T did not divide L_D")
        _, Is = c11.pdivmod(W, Ls)
        z = c11.line_scalar(c11.residue2(Is, E), bnum_res)
        if z is None:
            raise AssertionError("Delta zero but direct slope test failed")
        slopes[z] = slopes.get(z, 0) + 1

    return {
        "p": p,
        "q_gen": p,
        "q_line": p * p,
        "seed": seed,
        "zeros_all_B3": zeros_all,
        "zeros_split": zeros_split,
        "C2": len(slopes),
        "max_slope_fiber": max(slopes.values()) if slopes else 0,
        "coeff_component_rank": coeff_rank,
    }


def main():
    cases = [(7, 3, 8), (11, 2, 8), (17, 3, 5)]
    for p, nr, trials in cases:
        for seed in range(trials):
            r = run_trial(p, nr, seed)
            print(
                "p={p} seed={seed} q_gen={q_gen} q_line={q_line} "
                "zeros_all_B3={zeros_all_B3} zeros_split={zeros_split} "
                "C2={C2} max_slope_fiber={max_slope_fiber} "
                "coeff_component_rank={coeff_component_rank}".format(**r)
            )


if __name__ == "__main__":
    main()
