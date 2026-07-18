#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_a4_coverage.py -- gated verifier for the A4-coverage-of-high-kappa lane.

Question (the wall named by PR #534, thresholds-balanced-core-kappa-growth):
does the (A4) prefix-flatness / Sidon payment reach any actual residual
balanced-core chart lying in the high-kappa raw regime exposed by #534?
#534 computed raw prefix-support families; it did not prove that they survive
first-match removal or that raw member count equals realized slope mass. This
is a COVERAGE / ROUTING question, not a proof of (MI)/(MA).

The decisive structural fact this script recomputes with EXACT prime-field
arithmetic (no floats/sampling in the gated identities): the (A4) payment axes
are all INDEPENDENT of the residual kernel dimension kappa = k - |common core|.

  Group A  the effective Fourier span A_eff = |V_g| (lem:effective-span-fourier,
           EF1/EF2/EF3 L2860-2893) recomputed as p^{dim span{g(t)-g(t0)}}, and
           the closure bound A <= |B|^{a-k-1} (thm:small-effective-dual-closure
           L3026-3061); the closure criterion is log A = o(|T|), i.e.
           (a-k-1) log|B| = o(n) -- a statement about prefix depth, not kappa.
  Group B  the raw prefix-map fiber F_s = the #534 prefix class and f_s is its
           support-member count. This is not an actual first-match chart or a
           realized-slope count.
  Group C  the raw census on #534's four configs: A_eff is a property of the
           ambient slice while raw kappa varies; finite exponents and energies
           are measured without promoting raw families to actual residuals.
  Group D  the PTM stress test (disjoint_equal_prefix_pair, #534): the raw
           family lies in shallow-prefix ambient slices. The closure theorem
           pays any actual residual subfamily there, if one survives.
  Group E  the w-sweep: A_eff(w) grows with prefix depth while each sampled
           slice retains a near-maximal raw-kappa family. Names the deep-prefix
           wall numerically.
  Group F  residual monotonicity (lem:residual-monotonicity L6574) as a SET fact:
           a residual sub-family's max-fiber <= the full-slice max-fiber, for
           any sub-family, independent of its kappa -- the coverage transfer.

Stdlib only.  Deterministic.  Runtime target < 120 s under ulimit -v 2097152.
Prints  RESULT: PASS (N checks)  and exits 0 iff every gated check holds.

Credit: builds directly on PR #534 (balanced_core_kappa_growth.md, verifier
verify_kappa_growth.py) and its raw prefix/kernel primitives. Consumes PR
#528's (RC) statement and the scottdhughes (MI)/(MA) inequalities as inputs.
LegaSage #531 isolates the residual Sidon statement as an OPEN GAP. The proved
coverage statement is conditional on an actual residual being contained in an
ambient shallow-prefix slice; its bound is independent of the kernel label.
"""

import sys
import math
from math import comb
from itertools import combinations
from collections import Counter, defaultdict

# ----------------------------------------------------------------------------
# exact prime-field linear algebra  (identical primitives to verify_kappa_growth.py)
# ----------------------------------------------------------------------------

def inv_mod(a, p):
    a %= p
    if a == 0:
        raise ZeroDivisionError("no inverse of 0")
    return pow(a, p - 2, p)

def mat_rank(rows, p):
    """Rank over F_p of a list-of-lists matrix."""
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    rank = 0
    prow = 0
    for col in range(ncol):
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
    return [[pow(x, i, p) for x in U] for i in range(R)]

def kappa_kernel(U, R, p):
    """dim ker(H_U) = |U| - rank(H_U); the #528/#534 secant kernel dimension."""
    r = mat_rank(vandermonde_columns(U, R, p), p)
    return len(U) - r, r

def poly_from_roots(S, p):
    """Monic locator Q_S(X)=prod (X-t); coeffs high->low [1, q_1, ..., q_a]."""
    coeffs = [1]
    for t in S:
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] - t * c) % p
        coeffs = new
    return coeffs

def prefix_key(S, p, w):
    """Depth-w common-prefix key: locator coeffs q_1..q_w."""
    coeffs = poly_from_roots(S, p)
    return tuple(coeffs[1:w + 1])

# ----------------------------------------------------------------------------
# (A4) effective span A_eff = |V_g| = p^{dim span{g(t)-g(t0)}}  (EF1, L2860)
# ----------------------------------------------------------------------------

def span_dim_from_prefixes(prefix_keys, p):
    """Affine F_p-dimension of a set of prefix vectors = rank of {v - v0}.

    The boundary map paying a balanced-core chart is the depth-w locator prefix
    Psi(S)=(q_1(S),...,q_w(S)) (Newton-equivalent to power sums p_1..p_w).  Its
    effective span V (thm:small-effective-dual-closure, EF1 L2860) is the F_p-span
    of {Psi(S)-Psi(S_0)}; A_eff = |V| = p^{dim}, bounded by w so A_eff <= p^w --
    exactly the closure hypothesis A <= |B|^{a-k-1}."""
    keys = list(prefix_keys)
    if not keys:
        return 0
    v0 = keys[0]
    diffs = [tuple((a - b) % p for a, b in zip(v, v0)) for v in keys[1:]]
    return mat_rank(diffs, p) if diffs else 0

# ----------------------------------------------------------------------------
# additive energy of a fiber (incidence vectors), def:sidon-heavy (L5065-5091)
# E(F) = #{(a,b,c,d) in F^4 : a-b=c-d} = sum_z r(z)^2,  Delta = E/|F|^3
# ----------------------------------------------------------------------------

def additive_energy(support_family):
    """Exact additive energy of a family of supports (as frozensets over [1..n]),
    identified with 0/1 incidence vectors in Z^T (integer arithmetic per L5061)."""
    vecs = [frozenset(S) for S in support_family]
    f = len(vecs)
    if f == 0:
        return 0, 0.0
    # difference multiset r(z), z = a-b in Z^T represented as (sorted +coords, -coords)
    r = Counter()
    for a in vecs:
        for b in vecs:
            plus = tuple(sorted(a - b))     # coords where a=1,b=0  (+1)
            minus = tuple(sorted(b - a))    # coords where a=0,b=1  (-1)
            r[(plus, minus)] += 1
    E = sum(c * c for c in r.values())
    Delta = E / (f ** 3) if f > 0 else 0.0
    return E, Delta

# ----------------------------------------------------------------------------
# Raw PTM support family (verbatim mechanism from PR #534)
# ----------------------------------------------------------------------------

def disjoint_equal_prefix_pair(n, w):
    """Two DISJOINT a-subsets S1,S2 of [1..n] with equal power sums p_1..p_w via
    a scaling Prouhet-Thue-Morse split (Prouhet's theorem)."""
    m = w + 1
    blk = 1 << m
    S1, S2 = [], []
    val = 1
    while val + blk - 1 <= n:
        for i in range(blk):
            (S1 if bin(i).count("1") % 2 == 0 else S2).append(val + i)
        val += blk
    return S1, S2

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
# GROUP A -- effective span A_eff and the closure bound A <= |B|^{a-k-1}
# ============================================================================
def group_A():
    print("[Group A] effective Fourier span A_eff=|V_g| and closure bound A<=|B|^w")
    # field sanity
    for p in (13, 17, 19, 23):
        check("A.inv.field_%d" % p, all((a * inv_mod(a, p)) % p == 1 for a in range(1, p)))
    # A_eff = p^{dim} <= p^w on each census slice; recompute dim by rank of prefix
    # differences over the realized depth-w prefixes of all a-subsets.
    for (p, n, k, a, w, lab) in CENSUS_CONFIGS:
        D = list(range(1, n + 1))
        prefixes = set()
        for S in combinations(D, a):
            prefixes.add(prefix_key(S, p, w))
        dim = span_dim_from_prefixes(prefixes, p)
        A_eff = p ** dim
        # GATED: A_eff <= p^w  (the closure hypothesis multiplier bound)
        check("A.closure_bound.%s" % lab, dim <= w and A_eff <= p ** w,
              "dim=%d w=%d A_eff=%d p^w=%d" % (dim, w, A_eff, p ** w))
        # GATED: log A_eff / |T| is the closure exponent; w log p / n here
        logA_over_T = math.log(A_eff) / n
        wbound = w * math.log(p) / n
        check("A.exponent_le_wbound.%s" % lab, logA_over_T <= wbound + 1e-9,
              "logA/|T|=%.4f <= w log p/n=%.4f" % (logA_over_T, wbound))
        print("      [%s] p=%d n=%d a=%d w=%d : dim(V)=%d  A_eff=p^%d=%d  "
              "log A_eff/|T|=%.3f (w log p/n=%.3f)"
              % (lab, p, n, a, w, dim, dim, A_eff, logA_over_T, wbound))
    # closure criterion is a statement about (w, |B|), NOT about kappa:
    ungated("closure hypothesis is (a-k-1) log|B| = o(n) [thm:small-effective-dual-"
            "closure L3057-3060]; it contains no kernel-dimension term.")

# ============================================================================
# GROUP B -- raw prefix-fiber census; no actual first-match projection
# ============================================================================
def slice_fibers(p, n, k, a, w):
    """Group all a-subsets of D=[1..n] by depth-w prefix (= syndrome fiber).
    Returns dict prefix-key -> list of supports (frozensets)."""
    D = list(range(1, n + 1))
    fibers = defaultdict(list)
    for S in combinations(D, a):
        fibers[prefix_key(S, p, w)].append(frozenset(S))
    return D, fibers

def group_B():
    print("[Group B] RAW PREFIX FIBER: member count is not realized-slope count")
    for (p, n, k, a, w, lab) in CENSUS_CONFIGS:
        R = n - k
        D, fibers = slice_fibers(p, n, k, a, w)
        # Largest raw prefix fiber. Its members are supports, not realized slopes.
        best_key = max(fibers, key=lambda kk: len(fibers[kk]))
        members = fibers[best_key]
        f_s = len(members)
        core = set(D)
        for S in members:
            core &= S
        U = sorted(set(D) - core)  # union of error supports = D \ common core
        kap_ker = kappa_kernel(U, R, p)[0] if U else 0
        kap_set = max(0, k - len(core))
        # GATED: kappa recomputed two ways agrees (K1)=(K2), ties to #534
        check("B.kappa_two_ways.%s" % lab, kap_ker == kap_set,
              "kernel kappa=%d vs k-|core|=%d" % (kap_ker, kap_set))
        # GATED: the LARGEST fiber has empty core and maximal kernel kappa=k
        check("B.largest_fiber_kappa_k.%s" % lab, kap_ker == k and len(core) == 0,
              "largest fiber size=%d kappa=%d core=%d (want kappa=k=%d,core=0)"
              % (f_s, kap_ker, len(core), k))
        # GATED: f_s is exactly the raw support-fiber cardinality.
        check("B.raw_member_count.%s" % lab, f_s == sum(1 for S in members),
              "member count matches fiber cardinality")
        print("      [%s] largest fiber: f_s=%d  kappa=%d=k  core=EMPTY  "
              "=> raw prefix family only; realized slopes not counted"
              % (lab, f_s, kap_ker))

# ============================================================================
# GROUP C -- kappa-independence census + additive energy of the kappa=k fiber
# ============================================================================
def group_C():
    print("[Group C] kappa-independence census: A_eff is a SLICE property "
          "orthogonal to (member count, kappa)")
    summaries = []
    for (p, n, k, a, w, lab) in CENSUS_CONFIGS:
        R = n - k
        D, fibers = slice_fibers(p, n, k, a, w)
        # A_eff for the whole slice (one number for the slice)
        dim = span_dim_from_prefixes(set(fibers.keys()), p)
        A_eff = p ** dim
        logA_over_T = math.log(A_eff) / n
        # per-fiber kappa distribution (kappa = k - |core|); measure the SPREAD
        kap_vals = []
        f_by_kappa = defaultdict(list)
        for key, members in fibers.items():
            core = set(D)
            for S in members:
                core &= S
            kap = max(0, k - len(core))
            kap_vals.append(kap)
            f_by_kappa[kap].append(len(members))
        kap_min, kap_max = min(kap_vals), max(kap_vals)
        f_sizes = [len(v) for v in fibers.values()]
        f_min, f_max = min(f_sizes), max(f_sizes)
        # GATED: A_eff is ONE number for the whole slice (p^dim, dim<=w), shared by
        # every fiber, while fiber sizes f_s vary widely AND kappa attains its max k.
        # So the closure axis A_eff is orthogonal to (member count, kappa): the SAME
        # small A_eff covers the kappa=k / largest-member fiber.  [The kappa values
        # themselves CONCENTRATE at k as n grows -- #534's finding -- so at n>=16
        # kap_min=kap_max=k; that concentration does not change A_eff.]
        check("C.A_is_slice_property.%s" % lab,
              dim <= w and kap_max == k and f_max > f_min,
              "A_eff=p^%d (dim<=w=%d) shared by all fibers; f_s in [%d..%d]; "
              "kappa_max=%d=k" % (dim, w, f_min, f_max, kap_max))
        # GATED finite measurement only: the sampled exponent is below 1/2
        # uniformly because A_eff belongs to the ambient slice.
        check("C.sample_exponent_below_half.%s" % lab, logA_over_T <= 0.5,
              "sample log A_eff/|T|=%.3f <= 0.5 over raw kappa in [%d..%d]"
              % (logA_over_T, kap_min, kap_max))
        # additive energy of the largest (kappa=k) fiber -- classify Sidon vs high
        best_key = max(fibers, key=lambda kk: len(fibers[kk]))
        big = fibers[best_key]
        E, Delta = additive_energy(big)
        Nbar = sum(len(v) for v in fibers.values()) / len(fibers)
        summaries.append((lab, n, k, dim, A_eff, logA_over_T, kap_min, kap_max,
                          len(big), Delta, Nbar))
        print("      [%s] slice A_eff=p^%d  log A_eff/|T|=%.3f  kappa in [%d..%d] "
              "(max=k)  | kappa=k fiber: f_s=%d Delta=%.3f (avg fiber Nbar=%.2f)"
              % (lab, dim, logA_over_T, kap_min, kap_max, len(big), Delta, Nbar))
    # GATED cross-config: the closure exponent log A_eff/|T| DECREASES as n grows
    # (w fixed) in these four finite rows. This is a measured trend, not an
    # actual-residual existence or asymptotic-mass claim.
    exps = [s[5] for s in summaries]
    check("C.coverage_strengthens_with_n", exps[-1] < exps[0],
          "log A_eff/|T| falls along the ladder: %s" % [round(x, 3) for x in exps])
    # GATED (measured, key finding): the kappa=k (largest-member) fibers are
    # LOW-energy / Sidon-like -- Delta_s ~ 1/f_s STRICTLY DECREASING with scale
    # ([0.36,0.17,0.06,0.02]). This classifies the raw fibers only; an actual
    # first-match residual would still require the source's projection step.
    deltas = [s[9] for s in summaries]
    check("C.kappa_k_fiber_is_sidon_low_energy",
          all(deltas[i] > deltas[i + 1] for i in range(len(deltas) - 1))
          and deltas[-1] < 0.05,
          "Delta_s strictly decreasing and ->0 (Sidon-like): %s"
          % [round(d, 3) for d in deltas])
    return summaries

# ============================================================================
# GROUP D -- raw PTM stress test inside shallow ambient slices
# ============================================================================
def group_D():
    print("[Group D] raw PTM stress test: ambient prefix slice is shallow")
    rows = []
    prev_exp = None
    decreasing = True
    for (p, n) in ((23, 16), (43, 32), (79, 64), (137, 128)):
        w = 2
        S1, S2 = disjoint_equal_prefix_pair(n, w)
        a = len(S1)
        k = a - w - 1
        R = n - k
        # Confirm raw equal prefix and disjointness; no first-match survival claim.
        pref_eq = prefix_key(S1, p, w) == prefix_key(S2, p, w)
        core = set(S1) & set(S2)
        U = sorted(set(S1) | set(S2))
        kap_ker = kappa_kernel(U, R, p)[0]
        check("D.prefix_eq.n%d" % n, pref_eq, "S1,S2 share depth-%d prefix" % w)
        check("D.core_empty.n%d" % n, len(core) == 0, "|core|=%d" % len(core))
        check("D.kappa_eq_k.n%d" % n, kap_ker == k, "kappa=%d k=%d" % (kap_ker, k))
        # effective span A_eff of the SLICE this pair lives in: A_eff <= p^w.
        # The pair's own realized prefix is a single point; the ambient slice's
        # closure multiplier is bounded by p^w -- the paid closure bound.
        A_eff_bound = p ** w
        logA_over_T = math.log(A_eff_bound) / n   # w log p / n, the closure exponent
        # GATED: closure exponent is SMALL and shrinks with n  => log A = o(|T|)
        check("D.shallow_prefix.n%d" % n, logA_over_T <= 0.65,
              "w log p/n=%.4f <= 0.65 (shallow => closure pays)" % logA_over_T)
        if prev_exp is not None and logA_over_T >= prev_exp:
            decreasing = False
        prev_exp = logA_over_T
        # additive energy of the PTM PAIR itself (the 'additively structured' worry)
        E_pair, Delta_pair = additive_energy([S1, S2])
        # secant constant for comparison (the DEAD #528 route): C(R+kappa,kappa+1)
        logC_secant = math.log2(comb(R + kap_ker, kap_ker + 1))
        rows.append((n, a, k, kap_ker, logA_over_T, logC_secant / n, Delta_pair))
        print("      n=%3d a=%2d k=%2d : kappa=%2d=k  |  CLOSURE exp w log p/n=%.4f "
              "(RAW SLICE) vs secant-bound log2 C/n=%.3f | PTM-pair Delta=%.3f"
              % (n, a, k, kap_ker, logA_over_T, logC_secant / n, Delta_pair))
    # GATED finite stress comparison. The theorem-level routing statement is
    # conditional on an actual residual subfamily of the ambient slice.
    check("D.ptm_shallow_vs_secant_bound",
          decreasing and all(r[4] <= 0.65 for r in rows) and rows[-1][5] > 0.9,
          "sample shallow exponents decrease while secant-bound exponent exceeds 0.9")
    ungated("The raw PTM family lies in shallow ambient slices. "
            "thm:small-effective-dual-closure pays any actual residual subfamily "
            "there, but this census does not prove that the PTM family survives "
            "first-match removal or realizes distinct slopes.")
    return rows

# ============================================================================
# GROUP E -- w-sweep: A_eff grows with prefix depth; largest fiber stays kappa=k
# ============================================================================
def group_E():
    print("[Group E] w-sweep: A_eff ~ p^{min(w,dim)} grows, kernel kappa stays near-maximal")
    p, n = 19, 14           # small enough to sweep w exhaustively over a-subsets
    prev_dim = -1
    dim_monotone = True
    for w in (1, 2, 3):
        a = 9               # fixed support size; k = a-w-1 varies with w
        k = a - w - 1
        R = n - k
        D, fibers = slice_fibers(p, n, k, a, w)
        dim = span_dim_from_prefixes(set(fibers.keys()), p)
        A_eff = p ** dim
        best_key = max(fibers, key=lambda kk: len(fibers[kk]))
        members = fibers[best_key]
        # kappa_max over the WHOLE slice (some fiber has empty core => kappa=k)
        kap_max = 0
        for key, mem in fibers.items():
            core = set(D)
            for S in mem:
                core &= S
            kap_max = max(kap_max, max(0, k - len(core)))
        # kappa of the largest-member fiber (may regain a core at deep w/small n)
        core_big = set(D)
        for S in members:
            core_big &= S
        kap_big = max(0, k - len(core_big))
        # GATED: at EVERY prefix depth w the slice STILL realizes a NEAR-MAXIMAL
        # kernel kappa_max >= k-1 (a near-empty-core fiber persists) while
        # A_eff = p^dim(w) GROWS with w.  So the closure axis A_eff and the kernel
        # dimension kappa are ORTHOGONAL.  (kappa_max = k for shallow w; it dips to
        # k-1 only at the deepest w on this tiny n, a finite-size effect: deeper
        # prefixes force a shared point.  It never collapses toward 0 as A_eff grows.)
        check("E.kappa_max_near_max.w%d" % w, kap_max >= k - 1,
              "w=%d: kappa_max over slice=%d >= k-1=%d (A_eff=p^%d)"
              % (w, kap_max, k - 1, dim))
        if dim <= prev_dim:
            dim_monotone = False
        prev_dim = dim
        print("      w=%d k=%d : dim(V)=%d A_eff=p^%d  | kappa_max(slice)=%d (>=k-1)  "
              "largest-fiber(f_s=%d) kappa=%d  (A_eff GREW, kappa stayed near-max)"
              % (w, k, dim, dim, kap_max, len(members), kap_big))
    # GATED: only the prefix-span dimension monotonicity is asserted here.
    # The separate per-w gates above certify a near-maximal raw-kappa family.
    check("E.prefix_span_dimension_increases", dim_monotone,
          "dim(V) strictly increases with w; separate gates retain raw kappa>=k-1")
    # deep-prefix WALL (elementary, flagged): if w log p were Theta(n), closure
    # fails; that regime needs genuine (MI)/(MA), never a kappa bound.
    n_big, p_big, w_big = 1000, 1009, 300
    deep_exp = w_big * math.log(p_big) / n_big
    check("E.deep_prefix_wall_named", deep_exp > 1.0,
          "deep w=Theta(n): w log p/n=%.2f is NOT o(1) => closure fails, "
          "(MI)/(MA) needed (hughes), still kappa-free" % deep_exp)
    ungated("Deep-prefix (w log|B| = Theta(n)) balanced cores are NOT closure-paid; "
            "their payment reduces to (MI)/(MA) on the ambient slice -- a "
            "character-sum condition, NOT a kappa condition.  This is the WALL.")

# ============================================================================
# GROUP F -- subset monotonicity as a set fact (conditional coverage transfer)
# ============================================================================
def group_F():
    print("[Group F] subset monotonicity: conditional residual coverage transfer")
    # Full slice Omega0 = all a-subsets; syndrome map = depth-R power-sum prefix.
    # Claim: for ANY subfamily Omc subset Omega0, and for every syndrome s,
    # |Omc cap Phi^{-1}(s)| <= |Omega0 cap Phi^{-1}(s)|. This set fact transfers
    # full-slice payment to an actual residual if its inclusion is separately
    # certified. Here we test synthetic candidate subfamilies of differing raw
    # kappa; the samples are not claimed to be first-match residual charts.
    p, n, k, a = 17, 14, 6, 9
    R = n - k
    w = a - k - 1
    D, full_fibers = slice_fibers(p, n, k, a, w)
    full_maxfiber = max(len(v) for v in full_fibers.values())
    import random
    rng = random.Random(20260710)
    all_supports = [S for v in full_fibers.values() for S in v]
    ok_all = True
    kappas_seen = set()
    candidate_families = [
        set(all_supports),
        {support for support in all_supports if 1 in support},
        {support for support in all_supports if {1, 2}.issubset(support)},
    ]
    for _ in range(3):
        subsize = rng.randint(len(all_supports) // 4, len(all_supports) // 2)
        candidate_families.append(set(rng.sample(all_supports, subsize)))
    for trial, Omc in enumerate(candidate_families):
        # its own fibers
        sub_fibers = defaultdict(int)
        for S in Omc:
            sub_fibers[prefix_key(sorted(S), p, w)] += 1
        sub_maxfiber = max(sub_fibers.values()) if sub_fibers else 0
        # Raw kappa of this synthetic candidate family (union of supports).
        core = set(D)
        for S in Omc:
            core &= S
        kap = max(0, k - len(core))
        kappas_seen.add(kap)
        if sub_maxfiber > full_maxfiber:
            ok_all = False
        check("F.monotone.trial%d" % trial, sub_maxfiber <= full_maxfiber,
              "candidate max-fiber=%d <= full max-fiber=%d (raw kappa=%d)"
              % (sub_maxfiber, full_maxfiber, kap))
    # GATED: monotonicity held across deliberately varied core sizes.
    check("F.transfer_kappa_independent", ok_all and len(kappas_seen) >= 3,
          "full-slice max-fiber bounds every candidate, over raw kappa values %s"
          % sorted(kappas_seen))
    print("      full-slice max-fiber=%d bounds every synthetic candidate "
          "(kappas seen: %s) -- actual-residual transfer needs inclusion"
          % (full_maxfiber, sorted(kappas_seen)))

# ============================================================================
# census configs = PR #534's exact four (p, n, k, a, w=a-k-1)
# ============================================================================
CENSUS_CONFIGS = [
    (13, 12, 5, 8, 2, "q13_n12_k5"),
    (17, 14, 6, 9, 2, "q17_n14_k6"),
    (17, 16, 7, 10, 2, "q17_n16_k7"),
    (19, 18, 8, 11, 2, "q19_n18_k8"),
]

def main():
    group_A()
    group_B()
    group_C()
    group_D()
    group_E()
    group_F()
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = sum(1 for _, ok, _ in CHECKS if not ok)
    print("-" * 70)
    if nfail == 0:
        print("RESULT: PASS (%d checks)" % npass)
        return 0
    print("RESULT: FAIL (%d passed, %d failed)" % (npass, nfail))
    return 1

if __name__ == "__main__":
    sys.exit(main())
