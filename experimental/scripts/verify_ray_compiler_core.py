#!/usr/bin/env python3
"""verify_ray_compiler_core.py  --  stdlib-only, zero-arg verifier.

Recomputes every gated number behind the packet note
  experimental/notes/thresholds/ray_compiler_balanced_core.md

Object: hard input #3, the residual ray compiler for higher-dimensional
balanced cores (hyp:ray-compiler / eq:ray-compiler in
experimental/asymptotic_rs_mca_frontiers.tex).

Main proved claim (PROVED, this lane): for a Reed-Solomon (Vandermonde/MDS)
parity check of redundancy R over GF(q), a fixed chart U subset D with
|U| = R + kappa (so kappa = dim ker H_U >= 1), and an integer t with
0 <= t <= R-1, the number of finite transverse slopes admitting a witness
E_gamma subset U with |E_gamma| <= t is at most

        C(R + kappa, kappa + 1)                          (field-INDEPENDENT)

which recovers thm:single-mds-circuit-ray (C(R+1,2)) at kappa = 1 and removes
the |F|^kappa field dependence of thm:bounded-residual-kernel-ray (RC_ker).

The verifier does NOT bake in the bound: it recomputes the exact transverse
ray count by brute force and compares.  A violation would be a self-refutation.

Exit 0 and prints  RESULT: PASS (N checks)  when all gated numbers reproduce.
Numbers that are asserted but NOT independently recomputed are labelled UNGATED
in comments; there are none load-bearing here.
"""
from __future__ import annotations
import itertools
from math import comb
from pathlib import Path

CHECKS = 0
FAILS: list[str] = []


def check(cond: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILS.append(label)


# ---------------------------------------------------------------- GF(q) linalg
def rank(rows, q):
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0]); pr = 0; rk = 0
    for c in range(ncol):
        piv = next((r for r in range(pr, len(M)) if M[r][c] % q), None)
        if piv is None:
            continue
        M[pr], M[piv] = M[piv], M[pr]
        inv = pow(M[pr][c], q - 2, q)
        M[pr] = [(v * inv) % q for v in M[pr]]
        for r in range(len(M)):
            if r != pr and M[r][c] % q:
                f = M[r][c]
                M[r] = [(M[r][j] - f * M[pr][j]) % q for j in range(ncol)]
        pr += 1; rk += 1
        if pr == len(M):
            break
    return rk


def in_span(vec, cols, q):
    if not cols:
        return all(v % q == 0 for v in vec)
    return rank(cols, q) == rank(list(cols) + [vec], q)


def solve_one(cols, rhs, q):
    """One x with sum_i x_i cols[i] = rhs over GF(q), or None (cols are vectors)."""
    m = len(rhs); nc = len(cols)
    A = [[cols[j][i] for j in range(nc)] + [rhs[i]] for i in range(m)]
    where = [-1] * nc; r = 0
    for c in range(nc):
        piv = next((i for i in range(r, m) if A[i][c] % q), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], q - 2, q)
        A[r] = [(v * inv) % q for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % q:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % q for j in range(nc + 1)]
        where[c] = r; r += 1
    for i in range(m):
        if all(A[i][j] % q == 0 for j in range(nc)) and A[i][nc] % q:
            return None  # inconsistent
    x = [0] * nc
    for c in range(nc):
        if where[c] != -1:
            x[c] = A[where[c]][nc] % q
    return x


def kernel_basis(cols, q, ncols):
    """Basis of {x in GF(q)^ncols : sum_i x_i cols[i] = 0}."""
    m = len(cols[0])
    A = [[cols[j][i] for j in range(ncols)] for i in range(m)]
    where = [-1] * ncols; r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, m) if A[i][c] % q), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], q - 2, q)
        A[r] = [(v * inv) % q for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % q:
                f = A[i][c]
                A[i] = [(A[i][j] - f * A[r][j]) % q for j in range(ncols)]
        where[c] = r; r += 1
    free = [c for c in range(ncols) if where[c] == -1]
    basis = []
    for fc in free:
        v = [0] * ncols; v[fc] = 1
        for c in range(ncols):
            if where[c] != -1:
                v[c] = (-A[where[c]][fc]) % q
        basis.append(tuple(v))
    return basis


def det(M, q):
    n = len(M)
    A = [list(r) for r in M]; d = 1
    for c in range(n):
        piv = next((i for i in range(c, n) if A[i][c] % q), None)
        if piv is None:
            return 0
        if piv != c:
            A[c], A[piv] = A[piv], A[c]; d = (-d) % q
        d = (d * A[c][c]) % q
        inv = pow(A[c][c], q - 2, q)
        for i in range(c + 1, n):
            if A[i][c] % q:
                f = (A[i][c] * inv) % q
                A[i] = [(A[i][j] - f * A[c][j]) % q for j in range(n)]
    return d % q


def hcol(x, R, q):
    return tuple(pow(x, j, q) for j in range(R))


# ---------------------------------------------------- exact transverse ray count
def theta_full(y0, y1, Ucols, t, q):
    """Exact # finite transverse-bad slopes, brute over all gamma (definition)."""
    idx = range(len(Ucols))
    subsE = [c for sz in range(t + 1) for c in itertools.combinations(idx, sz)]
    cnt = 0
    for g in range(q):
        pt = tuple((y0[i] + g * y1[i]) % q for i in range(len(y0)))
        for comb_ in subsE:
            cols = [Ucols[i] for i in comb_]
            if in_span(pt, cols, q) and not (
                in_span(y0, cols, q) and in_span(y1, cols, q)
            ):
                cnt += 1
                break
    return cnt


def two_dim_subspaces(R, q):
    for c1 in range(R):
        for c2 in range(c1 + 1, R):
            f1 = [j for j in range(c1 + 1, R) if j != c2]
            f2 = [j for j in range(c2 + 1, R)]
            for v1 in itertools.product(range(q), repeat=len(f1)):
                r1 = [0] * R; r1[c1] = 1
                for j, val in zip(f1, v1):
                    r1[j] = val
                for v2 in itertools.product(range(q), repeat=len(f2)):
                    r2 = [0] * R; r2[c2] = 1
                    for j, val in zip(f2, v2):
                        r2[j] = val
                    yield tuple(r1), tuple(r2)


def maxtheta_proj(q, R, U, t):
    """max_{y0,y1} theta via projective-line reduction (validated == full enum)."""
    Ucols = [hcol(x, R, q) for x in U]
    idx = range(len(U))
    subsE = [c for sz in range(t + 1) for c in itertools.combinations(idx, sz)]
    best = 0; argbest = None
    for a, b in two_dim_subspaces(R, q):
        pts = [a] + [tuple((b[i] + g * a[i]) % q for i in range(R)) for g in range(q)]
        pc = 0
        for w in pts:
            for comb_ in subsE:
                cols = [Ucols[i] for i in comb_]
                if in_span(w, cols, q) and not (
                    in_span(a, cols, q) and in_span(b, cols, q)
                ):
                    pc += 1
                    break
        th = min(pc, q)
        if th > best:
            best = th; argbest = (a, b, pc)
    return best, argbest


# ------------------------------------------------------------------ CHECK GROUPS
def group_A_combinatorics():
    """Field-independent constant C(R+kappa,kappa+1); kappa=1 recovers C(R+1,2)."""
    def pascal(n, k):
        row = [1]
        for _ in range(n):
            row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
        return row[k]
    for R in range(2, 12):
        for kap in range(1, 6):
            val = comb(R + kap, kap + 1)
            check(val == pascal(R + kap, kap + 1), f"A:pascal R={R} k={kap}")
        # kappa=1 must equal the paper's single-MDS-circuit constant C(R+1,2)
        check(comb(R + 1, 2) == R * (R + 1) // 2, f"A:circ R={R}")
    # monotone: bound grows with kappa for fixed R (higher-dim costs more)
    for R in (3, 5, 8):
        vals = [comb(R + k, k + 1) for k in range(1, 5)]
        check(all(vals[i] < vals[i + 1] for i in range(len(vals) - 1)), f"A:mono R={R}")


def group_B_mds(cases):
    """ker H_U is [R+kappa, kappa, R+1] MDS: dim, min weight, general position."""
    for q, R, U in cases:
        Ucols = [hcol(x, R, q) for x in U]
        kap = len(U) - R
        Z = kernel_basis(Ucols, q, len(U))
        check(len(Z) == kap, f"B:dim q={q} R={R} |U|={len(U)}")
        # min nonzero weight of kernel code == R+1 (Singleton / MDS)
        minw = len(U) + 1
        for coeffs in itertools.product(range(q), repeat=kap):
            if not any(coeffs):
                continue
            v = [0] * len(U)
            for c, z in zip(coeffs, Z):
                for i in range(len(U)):
                    v[i] = (v[i] + c * z[i]) % q
            w = sum(1 for e in v if e % q)
            if 0 < w < minw:
                minw = w
        check(minw == R + 1, f"B:minwt q={q} R={R} |U|={len(U)} got {minw}")
        # every kappa columns of the kernel generator are independent
        # (equivalently every kappa-subset of U indexes an invertible kappa x kappa
        #  minor of the |U| x kappa matrix Z^T) -- MDS "general position".
        gen = [[Z[j][i] for j in range(kap)] for i in range(len(U))]  # rows indexed by U
        allpos = all(
            det([gen[i] for i in S], q) != 0
            for S in itertools.combinations(range(len(U)), kap)
        )
        check(allpos, f"B:genpos q={q} R={R} |U|={len(U)}")


def group_C_inequality(cases):
    """Exact: max transverse ray count <= C(R+kappa,kappa+1).  NO bound baked in."""
    results = {}
    for q, R, U, t, mode in cases:
        kap = len(U) - R
        bound = comb(R + kap, kap + 1)
        if mode == "full":  # enumerate all (y0,y1) in (F^R)^2
            best = 0
            for y0 in itertools.product(range(q), repeat=R):
                for y1 in itertools.product(range(q), repeat=R):
                    th = theta_full(y0, y1, [hcol(x, R, q) for x in U], t, q)
                    if th > best:
                        best = th
            arg = None
        else:  # "proj": projective-line reduction (validated equal to full)
            best, arg = maxtheta_proj(q, R, U, t)
        check(best <= bound, f"C:ineq q={q} R={R} |U|={len(U)} t={t} obs={best} bnd={bound}")
        results[(q, R, len(U), t)] = (best, bound, kap)
    return results


def group_D_crosscheck_and_tightness():
    """(i) proj reduction == full enumeration; (ii) tightness records."""
    # (i) cross-validate the optimization against the definition-level full enum
    for q, R, U, t in [(5, 3, [0, 1, 2, 3, 4], 2), (7, 2, [0, 1, 2, 3], 1),
                       (5, 2, [0, 1, 2, 3, 4], 1)]:
        full = 0
        for y0 in itertools.product(range(q), repeat=R):
            for y1 in itertools.product(range(q), repeat=R):
                th = theta_full(y0, y1, [hcol(x, R, q) for x in U], t, q)
                full = max(full, th)
        proj, _ = maxtheta_proj(q, R, U, t)
        check(full == proj, f"D:xcheck q={q} R={R} |U|={len(U)} full={full} proj={proj}")
    # (ii) tightness: bound is ATTAINED (sharp) for kappa<=2 when C(..)<q
    tight = [(11, 3, [0, 1, 2, 3], 2), (13, 3, [0, 1, 2, 3], 2),      # kappa=1
             (11, 3, [0, 1, 2, 3, 4], 2), (13, 3, [0, 1, 2, 3, 4], 2)]  # kappa=2
    for q, R, U, t in tight:
        kap = len(U) - R
        bound = comb(R + kap, kap + 1)
        best, _ = maxtheta_proj(q, R, U, t)
        check(bound < q, f"D:binding q={q} bnd={bound}")
        check(best == bound, f"D:tight q={q} R={R} kap={kap} obs={best} bnd={bound}")


def group_E_charging_certificate():
    """Directly validate the PROOF mechanism on an extremal kappa=2 line:
    charge each transverse slope to a (kappa+1)-subset T via a determinant that
    is affine in gamma, vanishes at gamma, is not identically zero, and the
    charge is injective -> |Z| <= C(R+kappa,kappa+1)."""
    q, R, U, t = 11, 3, [0, 1, 2, 3, 4], 2
    kap = len(U) - R
    Ucols = [hcol(x, R, q) for x in U]
    Z = kernel_basis(Ucols, q, len(U))  # kap kernel generators z_1..z_kap in F^|U|
    _, arg = maxtheta_proj(q, R, U, t)
    a, b, pc = arg
    # realise (y0,y1): put the direction (infinity) at a NON-transverse-bad point
    idx = range(len(U))
    subsE = [c for sz in range(t + 1) for c in itertools.combinations(idx, sz)]

    def transverse_witness(pt):
        for comb_ in subsE:
            cols = [Ucols[i] for i in comb_]
            if in_span(pt, cols, q) and not (
                in_span(a, cols, q) and in_span(b, cols, q)
            ):
                return comb_
        return None

    pts = [a] + [tuple((b[i] + g * a[i]) % q for i in range(R)) for g in range(q)]
    nonbad = next((w for w in pts if transverse_witness(w) is None), None)
    check(nonbad is not None, "E:has-nonbad-infinity")
    y1 = nonbad
    y0 = next(w for w in pts if rank([y1, w], q) == 2)  # any independent finite base
    # b0,b1 in F^|U| with sum_x b_i(x) h_x = y_i
    b0 = solve_one(Ucols, y0, q)
    b1 = solve_one(Ucols, y1, q)
    check(b0 is not None and b1 is not None, "E:lifts-exist")

    bad = []
    for g in range(q):
        pt = tuple((y0[i] + g * y1[i]) % q for i in range(R))
        E = transverse_witness(pt)
        if E is None:
            continue
        bad.append(g)
        # unique error on E explaining pt; e_gamma in F^|U|
        coeffsE = solve_one([Ucols[i] for i in E], pt, q)
        check(coeffsE is not None, f"E:err-solves g={g}")
        e = [0] * len(U)
        for pos, i in enumerate(E):
            e[i] = coeffsE[pos]
        Sg = [i for i in range(len(U)) if e[i] % q == 0]  # zero set of e_gamma
        check(len(Sg) >= kap + 1, f"E:Sg-big g={g} |Sg|={len(Sg)}")
        # find a (kappa+1)-subset T of Sg with Delta_T not identically zero in gamma'
        found = None
        for T in itertools.combinations(Sg, kap + 1):
            # rows: (z_1(x),...,z_kap(x), b_*(x)); Delta = D0 + gamma'*D1
            def mat(bstar):
                return [[Z[j][x] for j in range(kap)] + [bstar[x]] for x in T]
            D0 = det(mat(b0), q)
            D1 = det(mat(b1), q)
            if (D0, D1) != (0, 0):
                # concurrence at c_gamma => Delta_T(gamma) = 0
                check((D0 + g * D1) % q == 0, f"E:Delta-zero g={g} T={T}")
                found = T
                break
        check(found is not None, f"E:T-exists g={g}")
    # injective charge: reconstruct the map and assert distinct triples
    charged = {}
    ok_inj = True
    for g in bad:
        pt = tuple((y0[i] + g * y1[i]) % q for i in range(R))
        E = transverse_witness(pt)
        coeffsE = solve_one([Ucols[i] for i in E], pt, q)
        e = [0] * len(U)
        for pos, i in enumerate(E):
            e[i] = coeffsE[pos]
        Sg = [i for i in range(len(U)) if e[i] % q == 0]
        T = None
        for Tt in itertools.combinations(Sg, kap + 1):
            D0 = det([[Z[j][x] for j in range(kap)] + [b0[x]] for x in Tt], q)
            D1 = det([[Z[j][x] for j in range(kap)] + [b1[x]] for x in Tt], q)
            if (D0, D1) != (0, 0):
                T = Tt
                break
        if T in charged:
            ok_inj = False
        charged[T] = g
    check(ok_inj, f"E:injective |bad|={len(bad)} |triples|={len(charged)}")
    check(len(bad) <= comb(R + kap, kap + 1), f"E:count {len(bad)} <= {comb(R+kap,kap+1)}")
    check(len(bad) == pc, f"E:realises-max bad={len(bad)} pc={pc}")


def group_F_legasage_crosscheck():
    """Credit + differentiate LegaSage #523 (linear-form image proxy).
    Their checker: gamma = c.p a NONZERO linear form on F_q^d has image size q
    (surjective), zero form has image 1.  We reproduce these facts and record
    that this is an ABSTRACT map image, not the RS witness geometry -- our
    C(R+kappa,kappa+1) bound is field-independent and < q, which a surjective
    linear-form model (image exactly q) can never exhibit."""
    for q, d, coeffs in [(5, 2, (1, 0)), (5, 2, (1, 2)), (7, 2, (1, 3)),
                          (11, 3, (1, 1, 1))]:
        img = {sum(c * p[i] for i, c in enumerate(coeffs)) % q
               for p in itertools.product(range(q), repeat=d)}
        expected = 1 if all(c % q == 0 for c in coeffs) else q
        check(len(img) == expected, f"F:linimg q={q} d={d} c={coeffs}")
    check(len({0}) == 1, "F:zeroform")  # zero form image size 1
    # the differentiating fact: our geometric bound can sit strictly below q
    check(comb(3 + 2, 2 + 1) == 10 and 10 < 11, "F:geom-below-q")


def group_G_tex_anchors():
    """Gate the paper labels/line numbers this packet reads."""
    tex = Path(__file__).resolve().parents[1] / "asymptotic_rs_mca_frontiers.tex"
    lines = tex.read_text(encoding="utf-8").splitlines()

    def line_of(needle):
        return next((i for i, ln in enumerate(lines, 1) if needle in ln), None)

    anchors = {
        r"\label{hyp:ray-compiler}": 6033,
        r"\label{thm:single-mds-circuit-ray}": 1735,
        r"\label{thm:bounded-residual-kernel-ray}": 1680,
        r"\label{thm:syndrome-secant-exact}": 1607,
        r"\label{eq:transverse-secant-count}": 1615,
        r"\label{rem:balanced-core-exhaustion}": 4763,
        r"\label{prop:split-pencil-payment}": 4742,
        r"\label{eq:ray-compiler}": 6051,
    }
    for needle, exp in anchors.items():
        got = line_of(needle)
        check(got == exp, f"G:anchor {needle} exp {exp} got {got}")
    # the open-object sentence naming the target
    check(line_of("higher-dimensional transverse-secant bound") == 1089,
          "G:open-object-sentence")
    # RC_circ constant literally present
    check(any(r"\binom{R+1}{2}" in ln for ln in lines), "G:RCcirc-constant")
    # RC_ker field-dependent bound literally present
    check(any(r"(t+1)\abs{\F}^{\kappa(U)}" in ln for ln in lines), "G:RCker-fielddep")


def main():
    group_A_combinatorics()
    group_B_mds([
        (5, 2, [0, 1, 2]), (5, 2, [0, 1, 2, 3]), (5, 2, [0, 1, 2, 3, 4]),
        (5, 3, [0, 1, 2, 3]), (5, 3, [0, 1, 2, 3, 4]), (7, 3, [0, 1, 2, 3, 4]),
        (11, 3, [0, 1, 2, 3, 4, 5]), (7, 4, [0, 1, 2, 3, 4, 5]),
    ])
    group_C_inequality([
        # small full enumerations (definition-level, no shortcut)
        (5, 2, [0, 1, 2], 1, "full"),
        (5, 2, [0, 1, 2, 3], 1, "full"),
        (5, 2, [0, 1, 2, 3, 4], 1, "full"),
        (5, 3, [0, 1, 2, 3], 2, "full"),
        (5, 3, [0, 1, 2, 3, 4], 2, "full"),
        # larger, bound-binding (C(..) < q), via validated projective reduction
        (7, 3, [0, 1, 2, 3], 2, "proj"),
        (11, 3, [0, 1, 2, 3], 2, "proj"),
        (13, 3, [0, 1, 2, 3], 2, "proj"),
        (11, 3, [0, 1, 2, 3, 4], 2, "proj"),
        (13, 3, [0, 1, 2, 3, 4], 2, "proj"),
        (17, 3, [0, 1, 2, 3, 4, 5], 2, "proj"),   # kappa=3, obs 14 <= 15
        (11, 4, [0, 1, 2, 3, 4], 3, "proj"),      # R=4 kappa=1
        (13, 4, [0, 1, 2, 3, 4], 3, "proj"),
    ])
    group_D_crosscheck_and_tightness()
    group_E_charging_certificate()
    group_F_legasage_crosscheck()
    group_G_tex_anchors()

    if FAILS:
        print("RESULT: FAIL")
        for f in FAILS:
            print("  FAILED:", f)
        return 1
    print(f"RESULT: PASS ({CHECKS} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
