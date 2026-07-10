#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_kappa_growth.py  --  gated verifier for the balanced-core kappa-growth lane.

Question (residual (1) of PR #528, thresholds-ray-compiler-balanced-core):
for admissible RESIDUAL balanced-core charts, is the chart kernel dimension
kappa = |U| - R forced to be o(n/log n), or can it be Theta(n)?

This script recomputes, with EXACT prime-field arithmetic (no floats, no
sampling in the gated identities), every number the note
experimental/notes/thresholds/balanced_core_kappa_growth.md gates:

  Group A  combinatorics of the per-chart secant constant C(R+kappa,kappa+1)
           (re-derives the PR #528 sharp table values).
  Group B  the MDS chart identity  kappa(U) = |U|-R  via a direct kernel/rank
           computation of the Vandermonde parity block H_U over F_q.
  Group C  the SET-THEORETIC IDENTITY  kappa = k - |common agreement core|,
           and an exact census of balanced-core charts (prefix classes) on
           small RS codes: the joint (proj-dim, kappa, size) distribution.
  Group D  explicit residual balanced cores at growing scale n, exhibiting
           kappa = k = Theta(n) with a superpolynomial secant constant.
  Group E  a small direct check that the transverse-secant count really is
           <= C(R+kappa,kappa+1) (grounds the secant picture; sampled lines).

Stdlib only.  Deterministic.  Runtime target < 120 s.
Prints  RESULT: PASS (N checks)  and exits 0 iff every gated check holds.
"""

import sys
from math import comb
from itertools import combinations

# ----------------------------------------------------------------------------
# exact prime-field linear algebra
# ----------------------------------------------------------------------------

def inv_mod(a, p):
    a %= p
    if a == 0:
        raise ZeroDivisionError("no inverse of 0")
    return pow(a, p - 2, p)  # Fermat, p prime

def mat_rank(rows, p):
    """Rank over F_p of a list-of-lists matrix (rows may vary; we copy)."""
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    rank = 0
    prow = 0
    for col in range(ncol):
        # find pivot at or below prow in this column
        piv = None
        for r in range(prow, len(M)):
            if M[r][col] % p != 0:
                piv = r
                break
        if piv is None:
            continue
        M[prow], M[piv] = M[piv], M[prow]
        invp = inv_mod(M[prow][col], p)
        M[prow] = [(x * invp) % p for x in M[prow]]
        for r in range(len(M)):
            if r != prow and M[r][col] % p != 0:
                f = M[r][col] % p
                M[r] = [(M[r][j] - f * M[prow][j]) % p for j in range(ncol)]
        prow += 1
        rank += 1
        if prow == len(M):
            break
    return rank

def vandermonde_columns(U, R, p):
    """Parity columns h_x = (1,x,...,x^{R-1}) for x in U, returned as R rows."""
    rows = []
    for i in range(R):
        rows.append([pow(x, i, p) for x in U])
    return rows

def kappa_kernel(U, R, p):
    """dim ker(H_U : F_p^U -> F_p^R) = |U| - rank(H_U)."""
    r = mat_rank(vandermonde_columns(U, R, p), p)
    return len(U) - r, r

def poly_from_roots(S, p):
    """Monic locator Q_S(X)=prod_{t in S}(X-t), coeffs high->low: [1, q_1, ..., q_a]."""
    coeffs = [1]
    for t in S:
        # multiply by (X - t)
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] + c) % p              # X * c
            new[i + 1] = (new[i + 1] - t * c) % p   # (-t) * c
        coeffs = new
    return coeffs  # length |S|+1

# ----------------------------------------------------------------------------
# check bookkeeping
# ----------------------------------------------------------------------------

CHECKS = []
def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))
    if not ok:
        print("  FAIL: %s   %s" % (name, detail))

def ungated(msg):
    print("  UNGATED: %s" % msg)

# ============================================================================
# GROUP A -- the per-chart secant constant C(R+kappa, kappa+1)
# ============================================================================
def group_A():
    print("[Group A] per-chart secant constant C(R+kappa,kappa+1)")
    # field arithmetic sanity
    for p in (7, 11, 13, 17):
        ok = all((a * inv_mod(a, p)) % p == 1 for a in range(1, p))
        check("A.inv.field_%d" % p, ok)
    # PR #528 sharp table (re-derived): the bound recovers single-circuit at
    # kappa=1 and matches the attained maxima reported sharp for kappa<=2.
    check("A.circ.R2", comb(2 + 1, 2) == 3)     # C(R+1,2), R=2
    check("A.circ.R3", comb(3 + 1, 2) == 6)     # C(R+1,2)=6 at R=3 (PR #528)
    check("A.circ.R4", comb(4 + 1, 2) == 10)    # C(5,2)=10 at R=4 (PR #528)
    check("A.k2.R3",  comb(3 + 2, 3) == 10)     # C(5,3)=10, kappa=2 (PR #528)
    check("A.k3.R3",  comb(3 + 3, 4) == 15)     # C(6,4)=15, kappa=3 (PR #528)
    # monotonic explosion in kappa at fixed rate: with R = n-k, kappa up to k,
    # the constant C(R+kappa,kappa+1) is superpolynomial once kappa = Theta(n).
    # exhibit: log2 C(R+kappa,kappa+1) grows ~ linearly in n along kappa=k, R=k.
    prev = -1.0
    growth_ok = True
    lg = []
    for k in (4, 8, 16, 32, 64):
        R = k                    # rate 1/2 model: R = n-k = k, n = 2k
        kap = k                  # empty-core residual chart: kappa = k (Group C/D)
        val = comb(R + kap, kap + 1)
        import math
        L = math.log2(val)
        lg.append((2 * k, kap, L))
        if L <= prev:
            growth_ok = False
        prev = L
    check("A.growth.monotone", growth_ok, "log2 C(R+k,k+1) strictly increasing in n")
    # linear-in-n: the ratio log2(C)/n stays bounded below by a positive constant
    ratio_ok = all(L / n >= 0.5 for (n, kap, L) in lg)
    check("A.growth.linear_in_n", ratio_ok,
          "log2 C(R+k,k+1)/n >= 0.5  (superpolynomial => secant bound vacuous)")
    print("    kappa=k table (n, kappa, log2 C(R+k,k+1)):")
    for (n, kap, L) in lg:
        print("      n=%3d  kappa=%3d  log2C=%.1f  (=%.3f n)" % (n, kap, L, L / n))

# ============================================================================
# GROUP B -- kappa(U) = |U| - R via direct MDS kernel/rank computation
# ============================================================================
def group_B():
    print("[Group B] MDS chart identity  kappa(U) = |U| - R  (direct kernel)")
    # For an RS parity check any R columns are independent (MDS), so
    # rank(H_U) = min(|U|,R) and kappa = max(0,|U|-R).  Recompute directly.
    for (p, R) in ((11, 4), (13, 6), (17, 5)):
        D = list(range(1, p))            # F_p^* as evaluation domain
        for size in range(1, min(len(D), R + 4) + 1):
            U = D[:size]
            kap, rnk = kappa_kernel(U, R, p)
            check("B.rank.p%d.R%d.sz%d" % (p, R, size), rnk == min(size, R),
                  "rank(H_U)=%d expected min(|U|,R)=%d" % (rnk, min(size, R)))
            check("B.kappa.p%d.R%d.sz%d" % (p, R, size), kap == max(0, size - R),
                  "kappa=%d expected max(0,|U|-R)=%d" % (kap, max(0, size - R)))

# ============================================================================
# GROUP C -- census of balanced-core charts (prefix classes) on small RS
# ============================================================================
def prefix_key(S, p, w):
    """Depth-w common-prefix key: first w nonleading locator coeffs (q_1..q_w)."""
    coeffs = poly_from_roots(S, p)  # [1, q_1, ..., q_a]
    return tuple(coeffs[1:w + 1])

def deep_vec(S, p, w, a):
    """Moving coefficients (q_{w+1},...,q_a) of the locator."""
    coeffs = poly_from_roots(S, p)  # length a+1
    return tuple(coeffs[w + 1:a + 1])

def proj_dim(vectors, p):
    """Projective dimension of a finite point set: rank of homogenized
    coordinates (1, v) minus 1.  Single point -> 0, pencil/line -> 1, ..."""
    if not vectors:
        return -1
    hom = [(1,) + tuple(v) for v in vectors]
    return mat_rank(hom, p) - 1

def census_config(p, n, k, a, w, label, verbose=True):
    """Enumerate a-subsets of D=F_p^* (size n), group by depth-w prefix, and
    measure (proj-dim, kappa, class-size) for each balanced-core-candidate class.
    Returns summary dict incl. recs and a witness.  Gated identity checked inside."""
    R = n - k
    assert w == a - k - 1, "prefix depth convention w=a-k-1"
    D = list(range(1, n + 1))            # n distinct nonzero points; need p>n
    assert p > n, "need distinct evaluation points"
    classes = {}
    for S in combinations(D, a):
        classes.setdefault(prefix_key(S, p, w), []).append(S)

    n_classes = 0
    id_ok = True
    recs = []            # (size, proj_dim, kappa, |core|)
    wit = None           # witness: members of the largest balanced core
    for key, members in classes.items():
        n_classes += 1
        Sset = [set(m) for m in members]
        core = set(D)
        for s in Sset:
            core &= s
        U = sorted(set(D) - core)        # union of error supports = D \ core
        kap_ker = kappa_kernel(U, R, p)[0] if U else 0
        kap_set = max(0, k - len(core))  # set-theoretic identity
        if kap_ker != kap_set:
            id_ok = False
        pdim = proj_dim([deep_vec(m, p, w, a) for m in members], p)
        recs.append((len(members), pdim, kap_ker, len(core)))
        if pdim >= 2 and (wit is None or len(members) > len(wit[1])):
            wit = (key, members, pdim, kap_ker, len(core))

    # GATED: the two kappa computations agree for EVERY class in this config
    # (the MDS identity kappa = |U|-R = max(0, k - |common core|)).
    check("C.identity.%s" % label, id_ok,
          "kappa(|U|-R) == max(0,k-|core|) over all %d classes" % n_classes)

    bc = [r for r in recs if r[1] >= 2]           # balanced cores: proj-dim >= 2
    kappa_max_bc = max((r[2] for r in bc), default=-1)
    largest = max(bc, key=lambda r: r[0]) if bc else (0, -1, -1, -1)
    frac_full = (sum(1 for r in bc if r[2] == k) / len(bc)) if bc else float("nan")

    if bc:
        # GATED: some balanced core attains the maximal kernel kappa = k
        check("C.kappa_max.%s" % label, kappa_max_bc == k,
              "max kappa over proj>=2 charts=%d, k=%d" % (kappa_max_bc, k))
        # GATED: the LARGEST balanced core (most members ~ most rays) has kappa=k
        #        (empty common core) -- the per-chart secant bound is vacuous
        #        exactly on the charts that could carry the most slopes.
        check("C.largest_bc_kappa.%s" % label, largest[2] == k and largest[3] == 0,
              "largest proj>=2 chart: size=%d kappa=%d core=%d (want kappa=k=%d,core=0)"
              % (largest[0], largest[2], largest[3], k))

    if verbose:
        from collections import Counter
        kap_hist = Counter(r[2] for r in bc)
        size_by_kappa = {}
        for r in bc:
            size_by_kappa.setdefault(r[2], []).append(r[0])
        import math
        print("    [%s] p=%d n=%d k=%d R=%d a=%d w=%d : %d prefix classes, %d balanced (proj>=2)"
              % (label, p, n, k, R, a, w, n_classes, len(bc)))
        print("      kappa histogram over balanced cores (kappa: #charts, max class size):")
        for kap in sorted(kap_hist):
            print("        kappa=%d : %4d charts, max_class_size=%d"
                  % (kap, kap_hist[kap], max(size_by_kappa[kap])))
        print("      largest balanced core: size=%d proj_dim=%d kappa=%d core=%d"
              % (largest[0], largest[1], largest[2], largest[3]))
        print("      frac of ALL balanced cores with kappa=k (empty core): %.2f" % frac_full)
        if largest[2] >= 0:
            print("      => secant constant on largest chart: C(%d,%d), log2=%.1f"
                  % (R + largest[2], largest[2] + 1,
                     math.log2(max(1, comb(R + largest[2], largest[2] + 1)))))
        if wit is not None:
            print("      witness (largest balanced core) members: %s ; common core=%s"
                  % ([tuple(m) for m in wit[1][:4]], "EMPTY" if wit[4] == 0 else wit[4]))
    return {"n": n, "k": k, "R": R, "n_classes": n_classes, "n_bc": len(bc),
            "largest": largest, "kappa_max_bc": kappa_max_bc,
            "frac_full": frac_full, "recs": recs, "witness": wit}

def group_C():
    print("[Group C] exact census of balanced-core charts on small RS codes")
    summaries = []
    # (p, n, k, a, w=a-k-1) -- ladder where balanced cores (proj-dim>=2) occur
    configs = [
        (13, 12, 5, 8, 2, "q13_n12_k5"),
        (17, 14, 6, 9, 2, "q17_n14_k6"),
        (17, 16, 7, 10, 2, "q17_n16_k7"),
        (19, 18, 8, 11, 2, "q19_n18_k8"),
    ]
    for (p, n, k, a, w, lab) in configs:
        summaries.append(census_config(p, n, k, a, w, lab))
    # GATED cross-config: max balanced-core kappa = k in every config, and it
    # increases along the ladder => kappa_max = Theta(n) empirically.
    ks = [(s["n"], s["kappa_max_bc"], s["k"]) for s in summaries]
    check("C.kappa_grows_with_n",
          all(s["kappa_max_bc"] == s["k"] for s in summaries) and ks[-1][1] > ks[0][1],
          "kappa_max=k in every config and increases with n: %s" % ks)
    # GATED: fraction of balanced cores at maximal kappa=k INCREASES with n
    #        (mass concentrates at kappa=k -- residual => empty core => kappa=k).
    fr = [s["frac_full"] for s in summaries]
    check("C.mass_concentrates_at_kappa_k", fr[-1] > fr[0],
          "frac(kappa=k) rises along ladder: %s" % [round(x, 2) for x in fr])
    # GATED: proj-dim and kappa are INDEPENDENT parameters -- exhibit a balanced
    #        core with proj_dim < kappa AND one with proj_dim > kappa across the
    #        census (so kappa is NOT a function of the moving-space dimension).
    all_bc = [r for s in summaries for r in s["recs"] if r[1] >= 2]
    has_lt = any(r[1] < r[2] for r in all_bc)   # proj_dim < kappa
    has_gt = any(r[1] > r[2] for r in all_bc)   # proj_dim > kappa
    check("C.projdim_kappa_independent", has_lt and has_gt,
          "found proj<kappa (%s) and proj>kappa (%s) balanced cores" % (has_lt, has_gt))
    return summaries

# ============================================================================
# GROUP D -- residual charts force kappa=k=Theta(n): explicit + census-tied
# ============================================================================
def disjoint_equal_prefix_pair(n, w):
    """Two DISJOINT a-subsets S1,S2 of D=[1..n] with equal power sums
    p_1,...,p_w (hence equal depth-w locator prefix by Newton), built by a
    scaling Prouhet-Thue-Morse split: index i in [0,2^m) goes to S1 if the
    binary digit sum of i is even, else S2.  Such a bipartition equalises
    p_1,...,p_{m-1}.  We take m = w+1 blocks and tile them across [1..n]."""
    m = w + 1                     # PTM on 2^m indices equalises p_1..p_{m-1}=p_1..p_w
    blk = 1 << m
    S1, S2 = [], []
    val = 1
    while val + blk - 1 <= n:
        for i in range(blk):
            (S1 if bin(i).count("1") % 2 == 0 else S2).append(val + i)
        val += blk
    return S1, S2

def group_D():
    print("[Group D] residual => kappa=k=Theta(n): explicit PTM pairs + census tie")
    import math
    # (D1) explicit, scalable, EXACT residual charts (disjoint equal-prefix pairs).
    #      Disjoint => empty common core => U=D => kappa=|U|-R=k.  A shift PAIR
    #      is proj-dim 1, so it is a residual SHIFT-PAIR chart (A6 still needs
    #      it paid); it certifies kappa=k is attained by exact residual charts
    #      at every scale.  (proj-dim>=2 balanced cores are exhibited by Group C.)
    rows = []
    prev = -1.0
    mono = True
    for (p, n) in ((23, 16), (43, 32), (79, 64), (137, 128)):
        w = 2
        S1, S2 = disjoint_equal_prefix_pair(n, w)
        a = len(S1)
        assert len(S2) == a, "PTM halves must match"
        k = a - w - 1
        R = n - k
        # verify equal depth-w prefix (residual shift pair) exactly over F_p
        pref_ok = prefix_key(S1, p, w) == prefix_key(S2, p, w)
        core = set(S1) & set(S2)
        U = sorted(set(range(1, n + 1)) & (set(S1) | set(S2)))
        kap_ker, rnk = kappa_kernel(U, R, p)
        check("D1.prefix_eq.n%d" % n, pref_ok, "S1,S2 share depth-%d prefix" % w)
        check("D1.core_empty.n%d" % n, len(core) == 0, "|core|=%d" % len(core))
        check("D1.kappa_eq_k.n%d" % n, kap_ker == k == max(0, k - len(core)),
              "kappa=%d k=%d" % (kap_ker, k))
        logc = math.log2(comb(R + kap_ker, kap_ker + 1))
        if logc <= prev:
            mono = False
        prev = logc
        rows.append((n, k, kap_ker, logc))
        print("      n=%3d a=%2d k=%2d R=%2d : kappa=%2d  log2 C(R+kappa,kappa+1)=%.1f (=%.3f n)"
              % (n, a, k, R, kap_ker, logc, logc / n))
    check("D1.kappa_theta_n", mono and rows[-1][2] > rows[0][2] and rows[-1][3] / rows[-1][0] >= 0.5,
          "kappa=k grows with n and secant constant is superpolynomial (>=0.5 n)")
    return rows

# ============================================================================
# GROUP E -- direct transverse-secant count <= C(R+kappa, kappa+1) (grounding)
# ============================================================================
def in_span(cols, y, R, p):
    """Is vector y in F_p^R in the span of the given columns (each len R)?"""
    if not cols:
        return all(v % p == 0 for v in y)
    aug = [list(row) for row in zip(*cols)]   # R rows x |cols|
    # append y as extra column, compare ranks
    base_rank = mat_rank(aug, p)
    aug2 = [aug[i] + [y[i]] for i in range(R)]
    return mat_rank(aug2, p) == base_rank

def theta_U(U, R, t, y0, y1, p):
    """#{gamma in F_p : exists E subset U, |E|<=t, y0+gamma y1 in V_E,
       {y0,y1} not both in V_E}."""
    Ucols = [tuple(pow(x, i, p) for i in range(R)) for x in U]
    subsets = []
    for sz in range(0, t + 1):
        for idx in combinations(range(len(U)), sz):
            subsets.append(idx)
    bad = set()
    for gamma in range(p):
        yg = tuple((y0[i] + gamma * y1[i]) % p for i in range(R))
        for idx in subsets:
            cols = [Ucols[j] for j in idx]
            if in_span(cols, yg, R, p):
                # transversality: not both y0,y1 in V_E
                if not (in_span(cols, y0, R, p) and in_span(cols, y1, R, p)):
                    bad.add(gamma)
                    break
    return len(bad)

def group_E():
    print("[Group E] direct check: transverse count <= C(R+kappa,kappa+1) (sampled lines)")
    p, R, t = 7, 3, 2
    D = list(range(1, p))              # 6 points
    # deterministic line sample via a fixed LCG
    def lcg(seed):
        x = seed
        while True:
            x = (1103515245 * x + 12345) % (2 ** 31)
            yield x
    for kappa in (1, 2):
        U = D[:R + kappa]              # |U| = R+kappa
        bound = comb(R + kappa, kappa + 1)
        gen = lcg(2718281 + kappa)
        worst = 0
        nlines = 400
        ok = True
        for _ in range(nlines):
            y0 = tuple(next(gen) % p for _ in range(R))
            y1 = tuple(next(gen) % p for _ in range(R))
            if all(v == 0 for v in y1):
                continue
            th = theta_U(U, R, t, y0, y1, p)
            worst = max(worst, th)
            if th > bound:
                ok = False
        check("E.secant_bound.kappa%d" % kappa, ok,
              "max Theta_U=%d over %d lines, bound C(%d,%d)=%d"
              % (worst, nlines, R + kappa, kappa + 1, bound))
        print("      kappa=%d |U|=%d : max Theta_U(sampled)=%d <= C(%d,%d)=%d"
              % (kappa, len(U), worst, R + kappa, kappa + 1, bound))
    ungated("Group E samples lines (not exhaustive); it grounds the secant "
            "DIRECTION only. Sharpness of C(R+kappa,kappa+1) is PR #528's job.")

# ============================================================================
def main():
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = sum(1 for _, ok, _ in CHECKS if not ok)
    print("-" * 68)
    if nfail == 0:
        print("RESULT: PASS (%d checks)" % npass)
        return 0
    else:
        print("RESULT: FAIL (%d passed, %d failed)" % (npass, nfail))
        return 1

if __name__ == "__main__":
    sys.exit(main())
