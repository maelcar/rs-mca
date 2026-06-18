#!/usr/bin/env python3
"""Forced-Ra finite scan for Cycle 15.

Status: EXPERIMENTAL / AUDIT, not a proof.

Cycle 14 reduced the remaining t=2, j=3 wall to the slope image on resonance
surfaces.  One resonance type is

    Ra: Delta(tau) in F^* * B[tau],

meaning the F-valued quadratic Delta has all its coefficients on one B-line in
F = B + alpha B.  This script forces that condition by linear algebra.

For fixed E and Bnum, Delta is F-linear in W.  For each projective B-line
direction v=(v0,v1) in F, the conditions

    v0 * coeff_alpha(Delta_m) - v1 * coeff_base(Delta_m) = 0

for the ten degree <=2 monomials are homogeneous B-linear equations in the
2n base coordinates of W.  We compute the nullspace, sample source-valid W
from it, and tabulate C2 on distinct D-split cubics.

This is designed to find finite counterpackets or useful evidence.  It does
not certify asymptotics and does not touch q_chal or protocol ledgers.
"""

from itertools import combinations, product
import importlib.util
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
PREV = ROOT / "20260618_cycle12_base_component_rank_scan.py"
spec = importlib.util.spec_from_file_location("cycle12_rank", PREV)
c12r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c12r)
c12 = c12r.c12
c11 = c12r.c11


def rref_nullspace(matrix, p):
    """Return a B=F_p basis for the nullspace of matrix."""
    if not matrix:
        return []
    mat = [row[:] for row in matrix]
    m = len(mat)
    n = len(mat[0])
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
                mat[i] = [(mat[i][j] - factor * mat[r][j]) % p for j in range(n)]
        pivots.append(col)
        r += 1
        if r == m:
            break

    pivot_set = set(pivots)
    free_cols = [c for c in range(n) if c not in pivot_set]
    basis = []
    for free in free_cols:
        vec = [0] * n
        vec[free] = 1
        for row, col in enumerate(pivots):
            vec[col] = (-mat[row][free]) % p
        basis.append(vec)
    return basis


def random_from_basis(basis, p, rng):
    vec = [0] * len(basis[0])
    used = False
    for bvec in basis:
        coeff = rng.randrange(p)
        if coeff:
            used = True
        for i, v in enumerate(bvec):
            vec[i] = (vec[i] + coeff * v) % p
    if not used:
        bvec = rng.choice(basis)
        vec = bvec[:]
    return vec


def vec_to_W(vec):
    n = len(vec) // 2
    return c11.trim([(vec[2 * i] % c11.P, vec[2 * i + 1] % c11.P) for i in range(n)])


def coeff_pairs_for_W(W, E, bnum, D):
    p = c11.P
    n = len(D)
    LD = c11.locator(D)
    D1 = c12.sum_points(D)
    D2 = c12.elem2(D)
    Wres = c11.residue2(W, E)
    LDres = c11.residue2(LD, E)
    Bres = c11.residue2(bnum, E)

    rows = []
    rhs0 = []
    rhs1 = []
    for x, y, z in product(range(p), repeat=3):
        rows.append([c12r.monomial_value(exp, x, y, z, p) for exp in c12r.MONOMIALS_DEG_LE_2])
        val = c12r.delta_for_tau(
            Wres, LDres, Bres, E, W, D1, D2, n, c11.b(x), c11.b(y), c11.b(z)
        )
        rhs0.append(val[0])
        rhs1.append(val[1])
    coeff0 = c12r.solve_mod_p(rows, rhs0, p)
    coeff1 = c12r.solve_mod_p(rows, rhs1, p)
    return list(zip(coeff0, coeff1))


def forced_line_nullspace(p, nr, E, bnum, direction):
    c11.set_field(p, nr)
    D = [c11.b(x) for x in range(p)]
    n = len(D)
    v0, v1 = direction
    columns = []
    for i in range(n):
        for basis_coeff in (c11.one, c11.alpha):
            W = [c11.zero] * n
            W[i] = basis_coeff
            pairs = coeff_pairs_for_W(c11.trim(W), E, bnum, D)
            columns.append([(v0 * a1 - v1 * a0) % p for a0, a1 in pairs])
    matrix = []
    for row_idx in range(len(c12r.MONOMIALS_DEG_LE_2)):
        matrix.append([columns[col][row_idx] for col in range(2 * n)])
    return rref_nullspace(matrix, p)


def slope_stats_for_W(p, E, bnum, W):
    D = [c11.b(x) for x in range(p)]
    n = len(D)
    LD = c11.locator(D)
    D1 = c12.sum_points(D)
    D2 = c12.elem2(D)
    Wres = c11.residue2(W, E)
    LDres = c11.residue2(LD, E)
    Bres = c11.residue2(bnum, E)

    coeff_pairs = coeff_pairs_for_W(W, E, bnum, D)
    coeff_rank = c12r.coefficient_line_rank(coeff_pairs, p)
    r0 = c11.wedge(Wres, Bres)

    slopes = {}
    split_landings = 0
    for idxs in combinations(range(n), 3):
        T = [D[i] for i in idxs]
        tau1 = c12.sum_points(T)
        tau2 = c12.elem2(T)
        tau3 = c12.elem3(T)
        if c12r.delta_for_tau(Wres, LDres, Bres, E, W, D1, D2, n, tau1, tau2, tau3) != c11.zero:
            continue
        split_landings += 1
        LT = c11.locator(T)
        Ls, rem = c11.pdivmod(LD, LT)
        if rem != [c11.zero]:
            raise AssertionError("L_T did not divide L_D")
        _, Is = c11.pdivmod(W, Ls)
        z = c11.line_scalar(c11.residue2(Is, E), Bres)
        if z is None:
            raise AssertionError("Delta zero but direct slope test failed")
        slopes[z] = slopes.get(z, 0) + 1

    return {
        "coeff_rank": coeff_rank,
        "off_R0": r0 != c11.zero,
        "split_landings": split_landings,
        "C2": len(slopes),
        "max_slope_fiber": max(slopes.values()) if slopes else 0,
    }


def scan_case(p, nr, seed, samples_per_direction):
    c11.set_field(p, nr)
    rng = random.Random(seed)
    D = [c11.b(x) for x in range(p)]
    E = c11.random_separated_quadratic(rng)
    bnum = c11.random_bnum(rng)
    if c11.residue2(bnum, E) == [c11.zero]:
        raise AssertionError("zero bnum residue")

    directions = [(1, s) for s in range(p)] + [(0, 1)]
    best = None
    checked = 0
    forced_dims = []
    for direction in directions:
        basis = forced_line_nullspace(p, nr, E, bnum, direction)
        forced_dims.append((direction, len(basis)))
        if not basis:
            continue
        for _ in range(samples_per_direction):
            W = vec_to_W(random_from_basis(basis, p, rng))
            if W == [c11.zero]:
                continue
            stats = slope_stats_for_W(p, E, bnum, W)
            checked += 1
            row = {
                "p": p,
                "q_gen": p,
                "q_line": p * p,
                "seed": seed,
                "direction": direction,
                "kernel_dim": len(basis),
                **stats,
            }
            if best is None or (row["C2"], row["split_landings"], row["off_R0"]) > (
                best["C2"],
                best["split_landings"],
                best["off_R0"],
            ):
                best = row
    return best, checked, forced_dims


def main():
    # Keep the default run intentionally small.  The p=11 extension is useful
    # but slower because each forced line requires repeated quadratic
    # interpolation over B^3.  This smoke pass is meant for commit-time
    # evidence while the main Fable run is pending.
    cases = [
        (7, 3, 12, 8),
    ]
    global_best = None
    for p, nr, seeds, samples_per_direction in cases:
        for seed in range(seeds):
            best, checked, dims = scan_case(p, nr, seed, samples_per_direction)
            if best is None:
                print(f"p={p} seed={seed} no forced-Ra samples")
                continue
            if global_best is None or best["C2"] > global_best["C2"]:
                global_best = best
            max_dim = max(dim for _, dim in dims)
            print(
                "p={p} seed={seed} q_gen={q_gen} q_line={q_line} "
                "checked={checked} max_kernel_dim={max_dim} "
                "best_direction={direction} kernel_dim={kernel_dim} "
                "coeff_rank={coeff_rank} off_R0={off_R0} "
                "split_landings={split_landings} C2={C2} "
                "max_slope_fiber={max_slope_fiber}".format(
                    checked=checked,
                    max_dim=max_dim,
                    **best,
                )
            )
    if global_best is not None:
        print(
            "forced_ra_slope_scan: BEST "
            "p={p} q_gen={q_gen} q_line={q_line} seed={seed} "
            "C2={C2} split_landings={split_landings} off_R0={off_R0} "
            "direction={direction} kernel_dim={kernel_dim}".format(**global_best)
        )


if __name__ == "__main__":
    main()
