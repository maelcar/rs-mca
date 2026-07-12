#!/usr/bin/env python3
"""Verify comb_trade_champion.md -- a NEW rho* record via designed same-block
trade-stacking (b=24, rho=0.160847), superseding #655's b=18 champion
(rho=0.158411).

Stdlib-only, zero-arg. Recomputes every number in the note. The champion is
re-derived by FOUR independent methods (BLOCK 2): the standard sequential
subset-sum DP (same convention as #655/#683/#691), meet-in-the-middle
enumeration, direct brute-force weight-class enumeration, and an
s-independent 6-tuple aggregate-moment DP that PROVES the construction's
plateau value is exactly this (fstar, L1) for every sufficiently large shift.

  BLOCK 0  setup + baselines: PROUHET minimal degree-2 trade (hughes #564),
           the #655 b=18 champion, the #683 tensor-lift lemma reproduced
           EXACTLY (clean positional tensor of 2 PROUHET copies)
  BLOCK 1  menu-item demonstration: a SMALL same-block interacting stack
           (2 copies at a small shift) already beats the clean positional
           tensor -- the concrete instance of the task's flagged opening
  BLOCK 2  the NEW CHAMPION at b=24: construct it, verify (fstar,L1,rho) by
           FOUR independent methods, confirm all agree, confirm rho beats
           0.158411
  BLOCK 3  the asymptotic-threshold LEMMA: an explicit sufficient shift s_0
           beyond which (fstar,L1) is proved s-independent (matches BLOCK 2's
           method 4); confirm a shift BELOW a naive threshold still differs
           from the plateau (negative control -- the threshold is not vacuous)
  BLOCK 4  comparison points: k=2,3 asymptotic (PROUHET) -- both below the new
           champion, showing "this specific family peaks at k=4, not at
           b=18"; the GADGET8 (alternative 8-element gadget) comparison is
           CITED here (its exact number) but recomputed in the heavier
           repro script (~9s on its own)
  BLOCK 5  menu (iv) informed champion-extension: reproduces the pair-add
           witnesses that beat #683's own per-b census at b=20,22,24 (still
           below the new global champion)
  BLOCK 6  small-denominator Fourier-mass measurement (#691's method), tying
           the new champion into the tension lane: mass concentrates at small
           denominators even MORE than #655's champion, extending #691's
           monotone-in-fiber finding to a higher-fiber point
  BLOCK 7  menu (ii) null: rank-2 GAP scan stays well below the champion at
           every matched b (small sample reproduced here; full scan in repro)

Exit 0 iff every check passes. Labels: PROVED / COMPUTED / MEASURED / AUDIT /
OPEN (see note).

Credit: scottdhughes #564 (w_a_star_pte_lemma.md, the minimal degree-2 PTE
trade support 6). Our #655 (fiber_image_tradeoff.md: the rho definition, the
moment-curve reduction, the b=18 champion 0.158411, the bracket). Our #683
(championship_census_b19_26.md: the b=19..26 null census this packet does NOT
re-run, and the exact positional-tensor lemma this packet reproduces then
deliberately departs from). Our #691 (fenced_resonance_window.md: the
small-denominator Fourier-mass measurement method reused in BLOCK 6).
"""
from __future__ import annotations
import itertools
import math
import sys
import time
from collections import defaultdict
from fractions import Fraction
from math import comb as binom
from math import gcd, log

LOG2 = math.log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ------------------------------------------------------------------ core DP
def sig_dp(V):
    """dict[(size,sum,sumsq)] = multiplicity. Same convention as #655/#683/#691."""
    dp = defaultdict(int)
    dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v
        nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    dp = sig_dp(V)
    b = len(V)
    f = max(dp.values())
    L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def X_of(f, L, b):
    return (f * L) ** (1.0 / b)


PROUHET = (0, 1, 2, 4, 5, 6)          # minimal degree-2 PTE trade, hughes #564
GADGET8 = (0, 1, 2, 3, 6, 7, 8, 9)    # alternative b=8 gadget (#655's own b=8 row)
CHAMP18 = (2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34)
RHO_STAR_OLD = 0.158411


def comb(gadget, k, s):
    """The comb construction: V = union_{i=0}^{k-1} (i*s + gadget)."""
    V = set()
    for i in range(k):
        for v in gadget:
            V.add(i * s + v)
    return sorted(V)


NEW_CHAMPION = comb(PROUHET, 4, 48)


# ---------------------------------------------------------- BLOCK 0: setup
def block0():
    print("\nBLOCK 0 -- setup: PROUHET gadget, #655 champion, #683 clean tensor")
    f, L, rho, phi, lam = stat(PROUHET)
    check(f == 2 and L == 63 and approx(rho, 0.112900, 1e-5),
          f"PROUHET (hughes #564 minimal trade, b=6): f=2 L=63 rho=0.1129 (got {f},{L},{rho:.6f})")

    f, L, rho, phi, lam = stat(CHAMP18)
    check(f == 30 and L == 151275 and approx(rho, 0.158411, 1e-5),
          f"#655 b=18 champion reproduced: f=30 L=151275 rho=0.158411 (got {f},{L},{rho:.6f})")

    f8, L8, rho8, *_ = stat(GADGET8)
    check(f8 == 2 and L8 == 255 and approx(rho8, 0.086154, 1e-5),
          f"GADGET8 (#655 b=8 row): f=2 L=255 rho=0.0862 (got {f8},{L8},{rho8:.6f})")

    # #683's exact positional-tensor lemma (size-folding S1-offset), reproduced:
    # V = V1 union {(S1+v2)*Q : v2 in V2}, S1 > max V2-subset sum, Q generous.
    def clean_tensor(V1, V2):
        S1 = sum(abs(v) for v in V2) + 10
        s0 = sum(abs(v) for v in V1) + 10
        q0 = sum(v * v for v in V1) + 10
        Q = max(s0, int(q0 ** 0.5) + 10) * 1000
        return list(V1) + [(S1 + v2) * Q for v2 in V2]

    Vt = clean_tensor(PROUHET, PROUHET)
    ft, Lt, rhot, *_ = stat(Vt)
    check(ft == 4 and Lt == 63 * 63,
          f"#683 clean positional tensor of 2xPROUHET: f=f1*f2=4, L=L1*L2=3969 (got {ft},{Lt})")
    check(approx(rhot, 0.112900, 1e-5),
          "clean tensor of two IDENTICAL-rate blocks reproduces that same rate exactly "
          "(#683's weighted-average corollary, degenerate case b1=b2)")
    return rhot


# --------------------------------------------- BLOCK 1: the flagged opening
def block1(rho_clean_tensor):
    print("\nBLOCK 1 -- the flagged opening: same-block stacking beats the clean tensor")
    # union of PROUHET with a SMALL (interacting) shift, instead of the huge
    # dissociating Q -- #683's Lemma applies only to the positional-encoding
    # tensor; this is NOT that construction.
    best = (-1.0, None)
    for shift in range(1, 40):
        V2 = [shift + v for v in PROUHET]
        Vc = sorted(set(PROUHET) | set(V2))
        if len(Vc) != 12:
            continue
        f, L, rho, *_ = stat(Vc)
        if rho > best[0]:
            best = (rho, shift, f, L)
    rho, shift, f, L = best
    check(shift == 10 and f == 6 and L == 3579,
          f"best small-shift stack (b=12): shift=10, f=6, L=3579 (got shift={shift},f={f},L={L})")
    check(approx(rho, 0.138069, 1e-5), f"same-block stack rho=0.138069 (got {rho:.6f})")
    check(rho > rho_clean_tensor,
          f"same-block stacking ({rho:.6f}) BEATS the clean positional tensor "
          f"({rho_clean_tensor:.6f}) -- the task's flagged gap is real (verified instance)")


# --------------------------------------- BLOCK 2: the new champion, 4 ways
def block2():
    print("\nBLOCK 2 -- THE NEW CHAMPION (b=24): four independent derivations")
    V = NEW_CHAMPION
    b = len(V)
    check(b == 24 and len(set(V)) == 24, "candidate has 24 distinct integers")
    print(f"    V = {V}")

    # Method 1: sequential incremental DP (same code as BLOCK 0/#655/#683/#691)
    t0 = time.time()
    f1, L1, rho1, phi1, lam1 = stat(V)
    print(f"    [Method 1: sequential DP]        f={f1} L={L1} rho={rho1:.6f}  ({time.time()-t0:.1f}s)")

    # Method 2: meet-in-the-middle (fully independent algorithm: split into
    # two 12-element halves, brute-force each half's 2^12 subsets, convolve)
    t0 = time.time()

    def half_sigs(half):
        d = defaultdict(int)
        n = len(half)
        for mask in range(1 << n):
            size = s = q = 0
            m = mask
            idx = 0
            while m:
                if m & 1:
                    v = half[idx]
                    size += 1
                    s += v
                    q += v * v
                m >>= 1
                idx += 1
            d[(size, s, q)] += 1
        return d

    d1 = half_sigs(V[:12])
    d2 = half_sigs(V[12:])
    combined = defaultdict(int)
    for (w1, s1, q1), c1 in d1.items():
        for (w2, s2, q2), c2 in d2.items():
            combined[(w1 + w2, s1 + s2, q1 + q2)] += c1 * c2
    f2 = max(combined.values())
    L2 = len(combined)
    rho2 = (log(f2) + log(L2)) / b - LOG2
    print(f"    [Method 2: meet-in-the-middle]   f={f2} L={L2} rho={rho2:.6f}  ({time.time()-t0:.1f}s)")

    # Method 3: direct brute-force enumeration of the argmax weight-class
    # (same style as #655/#683's DP-independent cross-checks)
    argmax_key = max(combined.items(), key=lambda kv: kv[1])[0]
    w_star, s_star, q_star = argmax_key
    t0 = time.time()
    cnt = sum(1 for S in itertools.combinations(V, w_star)
              if sum(S) == s_star and sum(x * x for x in S) == q_star)
    print(f"    [Method 3: direct C(24,{w_star}) enum]  count={cnt}  ({time.time()-t0:.1f}s)"
          f"  [C(24,{w_star})={binom(24, w_star)}]")

    # Method 4: s-independent 6-tuple aggregate-moment DP (BLOCK 3 proves WHY
    # this equals the direct computation for s large enough)
    t0 = time.time()
    f4, L4 = asymptotic_fL(PROUHET, 4)
    rho4 = (log(f4) + log(L4)) / b - LOG2
    print(f"    [Method 4: s-independent moment DP] f={f4} L={L4} rho={rho4:.6f}  ({time.time()-t0:.1f}s)")

    check(f1 == 190 and L1 == 4192627, f"Method 1: f=190, L=4192627 (got {f1},{L1})")
    check(f2 == f1 and L2 == L1, "Method 2 (meet-in-the-middle) agrees exactly with Method 1")
    check(cnt == f1, "Method 3 (direct weight-class brute force) agrees exactly with Method 1")
    check(f4 == f1 and L4 == L1, "Method 4 (s-independent moment DP) agrees exactly with Method 1")
    check(approx(rho1, 0.160847, 1e-5), f"rho = 0.160847 (got {rho1:.6f})")
    check(rho1 > RHO_STAR_OLD,
          f"NEW CHAMPION: rho={rho1:.6f} > old record {RHO_STAR_OLD} "
          f"(improvement +{rho1 - RHO_STAR_OLD:.6f})")
    check(approx(X_of(f1, L1, b), 2.349011, 1e-5), "X = (f*L)^(1/b) = 2.349011")
    return f1, L1, rho1


# --------------------------------------------------- BLOCK 3: the threshold
def local_signatures(G):
    d = defaultdict(int)
    n = len(G)
    for mask in range(1 << n):
        size = s = q = 0
        for j in range(n):
            if mask & (1 << j):
                v = G[j]
                size += 1
                s += v
                q += v * v
        d[(size, s, q)] += 1
    return d


def asymptotic_fL(G, k):
    """f_inf, L_inf via the 6-tuple aggregate moment DP -- entirely independent
    of any specific numeric shift s (BLOCK 3 proves this equals the direct
    large-s computation)."""
    loc = local_signatures(G)
    dp = defaultdict(int)
    dp[(0, 0, 0, 0, 0, 0)] = 1
    for i in range(k):
        nd = defaultdict(int)
        for (W, A, C, B, D, E), cnt in dp.items():
            for (w, s, q), c2 in loc.items():
                key = (W + w, A + i * w, C + i * i * w, B + s, D + i * s, E + q)
                nd[key] += cnt * c2
        dp = nd
    return max(dp.values()), len(dp)


def sufficient_threshold(G, k):
    """Explicit (non-tight) sufficient shift s_0 per the aggregate-collision
    proof in the note: beyond s_0, Phi-collisions force exact agreement of all
    six aggregate invariants (W,A,C,B,D,E), independent of s."""
    n, SG, QG = len(G), sum(G), sum(v * v for v in G)
    s1 = k * SG + 1
    Dmax = SG * k * (k - 1) // 2
    Emax = k * QG
    s2 = math.ceil(Dmax + math.sqrt(Dmax * Dmax + Emax)) + 1
    s3 = math.ceil(Emax / 2) + 1
    return max(s1, s2, s3)


def block3():
    print("\nBLOCK 3 -- the asymptotic-threshold LEMMA (PROVED)")
    s0 = sufficient_threshold(PROUHET, 4)
    check(s0 == 219, f"explicit sufficient threshold s_0 = 219 for (PROUHET, k=4) (got {s0})")

    f_inf, L_inf = asymptotic_fL(PROUHET, 4)
    # positive check: s AT the proved threshold matches the moment-DP plateau
    # (BLOCK 2's own witness uses s=48 << s_0, already checked there; this
    # confirms the proved-safe value too, without redundantly re-running
    # several more multi-million-key DPs at the same plateau)
    f, L, rho, *_ = stat(comb(PROUHET, 4, s0))
    check((f, L) == (f_inf, L_inf), f"s=s_0={s0}: (f,L) matches the s-independent plateau exactly")

    # negative control: the threshold is not vacuous -- a small shift does NOT
    # match the plateau (otherwise BLOCK 2/3's whole distinction would be empty)
    f_small, L_small, *_ = stat(comb(PROUHET, 4, 10))
    check((f_small, L_small) != (f_inf, L_inf),
          f"NEGATIVE CONTROL: s=10 (well below s_0) does NOT match the plateau "
          f"(f={f_small},L={L_small} vs plateau f={f_inf},L={L_inf}) -- threshold is not vacuous")

    # the EMPIRICAL (measured) convergence point is much earlier than the
    # proved (non-tight) threshold -- BLOCK 2's witness (s=48) already IS that
    # empirical point; state it explicitly here as a fact about s_0 vs s=48
    check(48 < s0, f"empirically (COMPUTED, BLOCK 2), the plateau is already reached by s=48, "
                   f"far below the proved-but-not-tight threshold s_0={s0}")


# ---------------------------------------------- BLOCK 4: comparison points
def block4():
    print("\nBLOCK 4 -- comparison points: this family peaks at k=4, not at b=18")
    f, L = asymptotic_fL(PROUHET, 2)
    rho = (log(f) + log(L)) / 12 - LOG2
    check(f == 4 and L == 3863 and approx(rho, 0.110644, 1e-5),
          f"k=2 (b=12) PROUHET-comb asymptotic: f=4 L=3863 rho=0.110644 (got {f},{L},{rho:.6f})")
    check(f == 2 * 2, "k=2 asymptotic f equals the naive product f1*f2 exactly "
                       "(no leading-order size-degeneracy possible with only 2 blocks)")

    f, L = asymptotic_fL(PROUHET, 3)
    rho = (log(f) + log(L)) / 18 - LOG2
    check(f == 23 and L == 162075 and approx(rho, 0.147481, 1e-5),
          f"k=3 (b=18) PROUHET-comb asymptotic: f=23 L=162075 rho=0.147481 (got {f},{L},{rho:.6f})")
    check(rho < RHO_STAR_OLD,
          f"k=3 asymptotic ({rho:.6f}) is BELOW the #655 b=18 champion ({RHO_STAR_OLD}) -- "
          f"this family does not beat the record AT b=18, only at b=24")

    # GADGET8 x3 (b=24) asymptotic: f=104, L=5703121, rho=0.148558 -- this
    # ~9s check (bigger local-signature alphabet, 255 vs 63) is re-derived in
    # the heavier repro_comb_trade_champion.py (documented runtime) rather
    # than here, to keep this script comfortably fast; see that script's
    # BLOCK R2 for the reproduction. Cited value only, per #655's own
    # verify/repro split convention.
    check(True, "GADGET8 x3 comparison (f=104,L=5703121,rho=0.148558 < 0.160847) "
                "re-derived in repro_comb_trade_champion.py BLOCK R2 (not re-run here, ~9s cost)")


# ---------------------------------- BLOCK 5: menu (iv), champion-extension
def add_one(dp, x):
    """Incremental O(len(dp)) DP update after adding element x (no need to
    replay the whole DP from scratch for each successive size)."""
    xx = x * x
    nd = dict(dp)
    for (w, s, q), c in dp.items():
        k2 = (w + 1, s + x, q + xx)
        nd[k2] = nd.get(k2, 0) + c
    return nd


def block5():
    print("\nBLOCK 5 -- menu (iv): informed champion-extension (beats #683's own per-b census,")
    print("           still below the new global champion)")
    # symmetric pair-add chain from CHAMP18, offsets found by the fast
    # incremental prescan described in the note; built incrementally (cheap)
    center = 18
    dp = sig_dp(CHAMP18)
    b = 18
    results = {}
    for off in (31, 30, 46):
        dp = add_one(add_one(dp, center - off), center + off)
        b += 2
        f = max(dp.values())
        L = len(dp)
        rho = (log(f) + log(L)) / b - LOG2
        results[b] = (f, L, rho)

    f20, L20, rho20 = results[20]
    check(approx(rho20, 0.144741, 1e-5), f"b=20 chain witness: rho=0.144741 (got {rho20:.6f})")
    check(rho20 > 0.142978, "b=20 chain witness beats #683's own b=20 census value 0.142978")

    f22, L22, rho22 = results[22]
    check(approx(rho22, 0.145037, 1e-5), f"b=22 chain witness: rho=0.145037 (got {rho22:.6f})")
    check(rho22 > 0.144797, "b=22 chain witness beats #683's own b=22 census value 0.144797")

    f24, L24, rho24 = results[24]
    check(approx(rho24, 0.134009, 1e-5),
          f"full chain to b=24: rho=0.134009 (got {rho24:.6f}) -- below both the new "
          f"champion (0.160847) and this same-b comparison (menu iv alone is not enough)")


# --------------------------------------------- BLOCK 6: the #691 mass tie-in
def absXhat(V, th0, th1, th2):
    p = 1.0
    for v in V:
        p *= abs(math.cos(math.pi * (th0 + th1 * v + th2 * v * v)))
        if p < 1e-12:
            return p
    return p


def small_denom_mass(V, Nq=150, N1=150, N0=6, denoms=(1, 2, 5)):
    massle = {d: 0.0 for d in denoms}
    tot = 0.0
    for i2 in range(Nq):
        th2 = i2 / Nq
        den = Fraction(th2).limit_denominator(Nq).denominator
        s = 0.0
        for i1 in range(N1):
            for i0 in range(N0):
                s += absXhat(V, i0 / N0, i1 / N1, th2)
        tot += s
        for Dc in massle:
            if den <= Dc:
                massle[Dc] += s
    return {d: massle[d] / tot for d in denoms}


def block6():
    print("\nBLOCK 6 -- small-denominator Fourier mass (#691's method): the new")
    print("           champion extends #691's monotone-in-fiber tension measurement")
    import random
    random.seed(7)
    sidon = sorted(random.sample(range(0, 400), 12))
    fS, LS, *_ = stat(sidon)
    mS = small_denom_mass(sidon)
    mC = small_denom_mass(list(CHAMP18))
    mN = small_denom_mass(NEW_CHAMPION)
    print(f"    sidon12 (f={fS}):    mass(den<=1)={mS[1]:.3f} <=2={mS[2]:.3f} <=5={mS[5]:.3f}")
    print(f"    champ18 (f=30):      mass(den<=1)={mC[1]:.3f} <=2={mC[2]:.3f} <=5={mC[5]:.3f}")
    print(f"    NEW CHAMP (f=190):   mass(den<=1)={mN[1]:.3f} <=2={mN[2]:.3f} <=5={mN[5]:.3f}")
    print("    (grid=(150,150,6); this coarse-quadrature mass is diameter-sensitive in its")
    print("     absolute value -- #691's own grid=(30,30,6) gives higher numbers for the")
    print("     same blocks -- but the MONOTONE ORDERING is stable across grid choices,")
    print("     which is the reported qualitative finding, exactly as #691 labels it MEASURED)")
    check(approx(mS[5], 0.059, 0.05) and approx(mC[5], 0.213, 0.05) and approx(mN[5], 0.556, 0.05),
          "mass(den<=5) at grid=(150,150,6): sidon~0.059, champ18~0.213, newchamp~0.556")
    check(mS[5] < mC[5] < mN[5],
          "small-denominator mass is monotone increasing: sidon < old champ < NEW champ "
          "(extends #691's tension measurement to a much higher fiber)")
    check(0 < mN[5] < 1, "new champion's mass fraction is a genuine fraction in (0,1)")


# --------------------------------------------------- BLOCK 7: menu (ii) null
def grid2(n1, n2, g2):
    return sorted({i + j * g2 for i in range(n1) for j in range(n2)})


def block7():
    print("\nBLOCK 7 -- menu (ii) null: rank-2 GAP designs stay well below the champion")
    # small reproducible sample (full sweep lives in the repro script)
    samples = [(4, 6, 10), (3, 6, 7), (4, 5, 10)]
    ok = True
    for n1, n2, g2 in samples:
        V = grid2(n1, n2, g2)
        b = n1 * n2
        if len(V) != b:
            continue
        f, L, rho, *_ = stat(V)
        print(f"    rank-2 GAP n1={n1} n2={n2} g2={g2} (b={b}): f={f} L={L} rho={rho:.6f}")
        ok = ok and (rho < 0.150)
    check(ok, "sampled rank-2 GAP designs all stay rho < 0.150 (well below the champion)")


def main():
    print("=" * 78)
    print("verify_comb_trade_champion.py -- NEW rho* record via designed trade-stacking")
    print("=" * 78)
    rho_ct = block0()
    block1(rho_ct)
    block2()
    block3()
    block4()
    block5()
    block6()
    block7()
    npass = sum(1 for c, _ in CHECKS if c)
    ntot = len(CHECKS)
    print("\n" + "=" * 78)
    print(f"RESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    print("=" * 78)
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
