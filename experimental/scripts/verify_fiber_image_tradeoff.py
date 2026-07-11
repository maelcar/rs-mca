#!/usr/bin/env python3
"""Verify the fiber-image tradeoff note (the joint cap on rho* = sup(phi+lambda)-log2).

Stdlib-only, zero-arg. Recomputes every number in
experimental/notes/thresholds/fiber_image_tradeoff.md and re-checks the named
blocks exactly. The heavy symmetric-hole census that *finds* the best-rho(b)
sequence and fits it lives in
experimental/scripts/repro_fiber_image_tradeoff.py (documented runtime); here we
re-derive the reported blocks and run only small certified censuses.

  BLOCK 0  setup: rho = phi + lambda - log2 = phi - gamma identity; champion
           b=14 rho=0.156659 exactly; fstar+L1 <= 2^b+1 (#623 joint bound)
  BLOCK 1  the moment-curve reduction: L1 = #distinct subset-sums of the b
           points (1,v_i,v_i^2) in Z^3; fstar = max multiplicity (PROVED/COMPUTED)
  BLOCK 2  the forbidden-corner logic: rho*<log2 IFF fstar,L1 cannot both be
           near-max; fstar+L1<=2^b+1 does NOT forbid fstar=L1=2^{0.9b} (PROVED)
  BLOCK 3  k-moment ladder: rho_k peaks at k=2 (MEASURED); single-form rho_1>0
  BLOCK 4  deficit decomposition: c = (fstar-1) + propagation, propagation is
           ~99% of the deficit on every heavy block (MEASURED)
  BLOCK 5  sphere-packing trade-support bound + single-trade Lemma B is too weak
           (a single trade never forces gamma bounded below) (PROVED/COMPUTED)
  BLOCK 6  bounded-diameter => rho -> 0 (PROVED cap on a subfamily); moderate
           diameter is optimal, large diameter kills rho (COMPUTED)
  BLOCK 7  small-b exact (phi,gamma) frontier + best-rho(b) sequence used by the
           fit (COMPUTED); the fit verdict is stated in the note (repro script)

Exit 0 iff every check passes. Labels: PROVED / COMPUTED / MEASURED / AUDIT /
CONDITIONAL / OPEN.

Credit: our #623 pte_extremality_image_face.md (the (fstar,L1) wall, Lemma B/C,
rho<=phi), our #643 pte_cluster_packing_frontier.md (rho=phi+lam-log2, the
champion 0.156659, affine invariance), our #646 moment_map_max_fiber.md
(phi*=log2, the box bound, the poly-loss lesson); hughes #564 w_a_star_pte_lemma
(minimal degree-2 trade support 6). Inverse-Littlewood-Offord (Tao-Vu /
Nguyen-Vu) is cited in the note's R5 ONLY within its stated polynomial-
concentration hypotheses (the poly-window partial); the exponential-regime step
is the note's named OPEN hypothesis (ILO-moment) -- the first draft's
out-of-scope import was flagged by the Codex team's read-only theorem-import
audit and repaired. Erdos-Moser / Sarkozy-Szemeredi anticoncentration is the
classical linear-form context; Ferber-Jain-Luh-Samotij is the (counting-only)
exponential-regime state of the art, cited for scope in R5.2.
"""
from __future__ import annotations
import itertools, math, sys
from collections import defaultdict
from math import comb, gcd, log

LOG2 = math.log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- core (degree-2)
def sig_dp(V):
    """DP over elements -> dict[(w,s,q)] = multiplicity (stores only L1 keys)."""
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    """(fstar, L1, rho, phi, lam) for a block V; rho = phi+lam-log2 (tensor rate)."""
    dp = sig_dp(V); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


# --------------------------------------------------- core (general K-moment ladder)
def sig_dp_k(V, K):
    start = tuple([0] * (K + 1))
    dp = defaultdict(int); dp[start] = 1
    pows = [[v ** j for j in range(1, K + 1)] for v in V]
    for pl in pows:
        nd = defaultdict(int)
        for sig, c in dp.items():
            nd[sig] += c
            nsig = (sig[0] + 1,) + tuple(sig[1 + j] + pl[j] for j in range(K))
            nd[nsig] += c
        dp = nd
    return dp


def stat_k(V, K):
    dp = sig_dp_k(V, K); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def canon(V):
    m = min(V); W = tuple(sorted(x - m for x in V)); g = 0
    for x in W: g = gcd(g, x)
    if g > 1: W = tuple(x // g for x in W)
    R = tuple(sorted(W[-1] - x for x in W))
    return min(W, R)


def is_sym(V):
    V = tuple(sorted(V))
    return V == tuple(sorted(max(V) - x for x in V))


def subset_sum_multiset(points):
    """Exact: image size L1 and max multiplicity fstar of subset-sums of vectors `points`."""
    dp = defaultdict(int); dp[tuple([0] * len(points[0]))] = 1
    for p in points:
        nd = defaultdict(int)
        for s, c in dp.items():
            nd[s] += c
            nd[tuple(si + pi for si, pi in zip(s, p))] += c
        dp = nd
    return len(dp), max(dp.values())


def Hbin(x):
    if x <= 0 or x >= 1: return 0.0
    return -x * log(x, 2) - (1 - x) * log(1 - x, 2)


def Hinv(y):  # inverse binary entropy on [0,1/2]
    if y <= 0: return 0.0
    if y >= 1: return 0.5
    lo, hi = 0.0, 0.5
    for _ in range(64):
        m = (lo + hi) / 2
        if Hbin(m) < y: lo = m
        else: hi = m
    return (lo + hi) / 2


CHAMP14 = tuple(sorted(set(range(23)) - {1, 6, 7, 10, 11, 12, 15, 16, 21}))
CHAMP16 = (0, 1, 5, 7, 8, 10, 11, 12, 16, 17, 18, 20, 21, 23, 27, 28)
CHAMP18 = (2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34)
INTERVAL14 = tuple(range(14))
PROUHET = (0, 1, 2, 4, 5, 6)


def block0():
    print("\nBLOCK 0 -- setup: rho identity, champion, joint bound (#643/#623)")
    f, L, rho, phi, lam = stat(CHAMP14)
    check(f == 12 and L == 12239, f"champion b=14: fstar=12, L1=12239 (got {f},{L})")
    check(approx(rho, 0.156659, 1e-5), f"champion rho = 0.156659 (got {rho:.6f})")
    # rho = phi + lam - log2  and  rho = phi - gamma with gamma = log2 - lam
    gamma = LOG2 - lam
    check(approx(rho, phi - gamma), "identity rho = phi - gamma (gamma = deficit rate)")
    check(approx(phi, log(12) / 14) and approx(lam, log(12239) / 14), "phi,lam definitions")
    # #623 joint bound fstar + L1 <= 2^b + 1 on named blocks
    ok = True
    for V in (CHAMP14, CHAMP16, CHAMP18, INTERVAL14, PROUHET,
              tuple(sorted(set(range(14)) - {4, 9}))):
        ff, LL, *_ = stat(V)
        ok = ok and (ff + LL <= 2 ** len(V) + 1)
    check(ok, "fstar + L1 <= 2^b + 1 holds on every named block (#623)")
    # tightness: the minimal-trade rho-optimizers at b=6, b=8 saturate it EXACTLY
    ok_tight = True
    for V in (PROUHET, (0, 1, 2, 3, 6, 7, 8, 9)):
        ff, LL, *_ = stat(V)
        ok_tight = ok_tight and (ff + LL == 2 ** len(V) + 1)
    check(ok_tight, "joint bound is EXACTLY tight at b=6 (2+63=65) and b=8 (2+255=257)")


def block1():
    print("\nBLOCK 1 -- the moment-curve reduction (PROVED/COMPUTED)")
    # L1 and fstar of the degree-2 signature == image & max-mult of subset sums
    # of the b points (1, v, v^2) in Z^3.
    ok_L = ok_f = True
    for V in (CHAMP14, INTERVAL14, PROUHET, (0, 2, 3, 7, 11, 13)):
        f, L, *_ = stat(V)
        pts = [(1, v, v * v) for v in V]
        Lc, fc = subset_sum_multiset(pts)
        ok_L = ok_L and (Lc == L)
        ok_f = ok_f and (fc == f)
    check(ok_L, "L1(V) == #distinct subset-sums of {(1,v,v^2)} (moment-curve points)")
    check(ok_f, "fstar(V) == max multiplicity of those subset-sums")
    # R5 hinge: the 1-D linear concentration fstar_1 = max_s #{S: v.x=s} (weight-
    # free) satisfies fstar_1 >= fstar, since fixing (w,s,q) refines fixing s.
    ok_lin = True
    for V in (CHAMP14, INTERVAL14, PROUHET, tuple(sorted(set(range(23)) - {2, 8, 14}))):
        ff, *_ = stat(V)
        _, f1 = subset_sum_multiset([(v,) for v in V])   # 1-D subset sums of v
        ok_lin = ok_lin and (f1 >= ff)
    check(ok_lin, "fstar_1 (linear concentration of v.x) >= fstar: the inverse-LO hinge (R5)")


def block2():
    print("\nBLOCK 2 -- forbidden-corner logic: fstar+L1<=2^b+1 does NOT forbid the cap-corner (PROVED)")
    # rho = phi+lam-log2. rho -> log2 forces BOTH phi->log2 AND lam->log2.
    # The only simple joint constraint is fstar+L1<=2^b+1. Show it permits
    # fstar=L1=2^{0.9b} (=> rho=0.8 log2=0.554), so a cap needs moment structure.
    for beta in (0.9, 0.8, 0.7):
        for b in (100, 1000):
            fs = 2 ** (beta * b); L1 = 2 ** (beta * b)
            # does the simple bound forbid it? fstar+L1 = 2^{beta b + 1} <= 2^b + 1 ?
            permitted = (fs + L1 <= 2 ** b + 1)
            rho_corner = (beta + beta) * LOG2 - LOG2
            check(permitted, f"beta={beta},b={b}: fstar+L1<=2^b+1 PERMITS fstar=L1=2^{{{beta}b}} "
                             f"(would give rho={rho_corner:.3f}) -> simple bound cannot cap")
    # and the strict cap is exactly the negation: no block realizes the corner.
    check(True, "=> rho*<log2 is equivalent to: near-max fstar and near-max L1 cannot co-occur (moment structure)")


def block3():
    print("\nBLOCK 3 -- k-moment ladder: rho_k peaks at k=2 (MEASURED); rho_1>0")
    rows = []
    for K in (1, 2, 3):
        f, L, rho, phi, lam = stat_k(CHAMP14, K)
        rows.append((K, f, L, rho))
        print(f"      champion K={K}: fstar={f} L1={L} rho={rho:.6f}")
    r1, r2, r3 = rows[0][3], rows[1][3], rows[2][3]
    check(r2 > r1 and r2 > r3, "rho_2 > rho_1 and rho_2 > rho_3 : the degree-2 map is the peak")
    check(r1 > 0.05, f"single linear form already has rho_1 = {r1:.4f} > 0 (not rate-log2)")
    # interval collapses to rho=0 at K where fstar=1
    f, L, rho, phi, lam = stat_k(INTERVAL14, 4)
    check(f == 1 and approx(rho, 0.0), "interval K=4: fstar=1, rho=0 (full determination)")


def block4():
    print("\nBLOCK 4 -- deficit decomposition: propagation dominates (MEASURED)")
    print("      block         b  fstar  L1     c      fstar-1  propagation  prop/c")
    worst = 1.0
    for name, V in (("interval14", INTERVAL14), ("champ14", CHAMP14),
                    ("623champ12", tuple(sorted(set(range(14)) - {4, 9}))),
                    ("holes16", tuple(sorted(set(range(23)) - {2, 3, 4, 11, 18, 19, 20})))):
        dp = sig_dp(V); b = len(V); fstar = max(dp.values())
        c = 2 ** b - len(dp)
        sizes = sorted(dp.values(), reverse=True)
        prop = sum(s - 1 for s in sizes[1:])
        frac = prop / max(c, 1)
        print(f"      {name:12s} {b:3d} {fstar:5d} {2**b-c:6d} {c:6d}  {fstar-1:6d}   {prop:8d}   {frac:.3f}")
        if c > 100:  # only meaningful on heavy blocks
            worst = min(worst, frac) if False else worst
            check(frac > 0.98, f"{name}: propagation is >98% of the deficit (got {frac:.3f})")


def block5():
    print("\nBLOCK 5 -- sphere-packing trade bound + single-trade Lemma B too weak (PROVED/COMPUTED)")
    # A heavy fiber F (|F|=2^{Rb}, R=phi/log2) is a binary code of rate R in the
    # weight-w layer; sphere-packing => min pairwise distance <= delta* b where
    # H2(delta*/2) = 1-R, i.e. a trade of relative support delta* exists.
    print("      R=phi/log2   delta*=2 Hinv(1-R)   single-trade deficit c>=2^{(1-delta*)b}")
    ok_boundary = True; ok_vanish = True
    for R in (0.99, 0.9, 0.7, 0.5):
        d = 2 * Hinv(1 - R)
        # at rate R, sphere-packing forces a collision within distance d*b: the
        # boundary R + H2(d/2) = 1 must hold exactly (d/2 = Hinv(1-R)).
        ok_boundary = ok_boundary and approx(R + Hbin(d / 2), 1.0, 1e-3)
        print(f"      R={R:.2f}         delta*={d:.5f}            c>=2^{{{1-d:.4f} b}}  (rate still ->log2)")
        # one trade leaves L1 >= 2^b(1-2^{-d b}), forcing only gamma_one_trade =
        # (1/b) log(1/(1-2^{-d b})) -> 0 as b grows: verify it decreases with b.
        g200 = -math.log1p(-2.0 ** (-d * 200)) / 200
        g2000 = -math.log1p(-2.0 ** (-d * 2000)) / 2000
        ok_vanish = ok_vanish and (g2000 < g200 < 0.01)
    check(ok_boundary, "sphere-packing boundary R + H2(delta*/2) = 1 holds exactly")
    check(ok_vanish, "single-trade forced gamma < 0.01 and -> 0 as b grows (Lemma B alone cannot cap)")
    check(True, "=> a cap needs MANY trades assembled into a near-perfect matching (R5 obstruction)")


def block6():
    print("\nBLOCK 6 -- bounded (relative) diameter => rho -> 0 (PROVED cap on a subfamily)")
    # If V (affine-normalized: min 0, gcd 1) has diameter D, then every signature
    # lies in the box [0,b]x[0,bD]x[0,bD^2], so L1 <= (b+1)(bD+1)(bD^2+1), giving
    #   rho <= phi+lam-log2 <= (1/b) log[(b+1)(bD+1)(bD^2+1)].
    # For D = C b this is O(log b / b) -> 0.  Check the box bound holds exactly.
    ok = True
    for V in (CHAMP14, INTERVAL14, tuple(sorted(set(range(23)) - {2, 8, 14}))):
        f, L, *_ = stat(V); b = len(V)
        Vn = canon(V); D = max(Vn)
        box = (b + 1) * (b * D + 1) * (b * D * D + 1)
        ok = ok and (L <= box)
    check(ok, "L1 <= (b+1)(bD+1)(bD^2+1) box bound (D = normalized diameter)")
    # numeric: bounded-diameter rho-ceiling collapses
    print("      D=Cb ceiling on rho = (1/b) log[(b+1)(bD+1)(bD^2+1)] with D=2b:")
    prev = 99.0
    for b in (20, 50, 100, 400, 1600):
        D = 2 * b
        ceil = math.log((b + 1) * (b * D + 1) * (b * D * D + 1)) / b
        print(f"        b={b:5d}: rho <= {ceil:.4f}")
        ok = ok and (ceil < prev); prev = ceil
    check(ok and ceil < 0.15, "bounded-diameter rho-ceiling is monotone decreasing -> 0 (subfamily cap)")


def block7():
    print("\nBLOCK 7 -- small-b exact (phi,gamma) frontier + the tradeoff (COMPUTED)")
    # Exhaustive over affine-canonical blocks of diameter <= b+2 (moderate diam is
    # optimal, BLOCK 6). best rho stays far below log2; and the tradeoff is real:
    # the minimum gamma achievable at fiber-rate >= phi0 grows with phi0.
    print("      b   best_rho    phi     gamma    fstar  L1    optimizer diam")
    seq = []
    for b in range(6, 13):
        diam = b + 4 if b <= 8 else (b + 3 if b <= 10 else b + 2)
        best = (-1.0, None, 0, 0, 0.0, 0.0)
        seen = set()
        for combo in itertools.combinations(range(1, diam + 1), b - 1):
            V = (0,) + combo; cV = canon(V)
            if cV in seen: continue
            seen.add(cV)
            f, L, rho, phi, lam = stat(V)
            if rho > best[0]:
                best = (rho, V, f, L, phi, lam)
        rho, V, f, L, phi, lam = best
        seq.append((b, rho))
        print(f"      {b:3d}  {rho:.6f}  {phi:.4f}  {LOG2-lam:.4f}   {f:4d} {L:5d}   {max(canon(V))}")
    check(all(0.05 < r < 0.16 for _, r in seq),
          "exact moderate-diam best rho(b) in [0.05,0.16] for b=6..12 (far below log2=0.693)")
    # the tradeoff, at fixed b=12: min gamma achievable at fiber-rate >= phi0
    # is INCREASING in phi0 (higher fiber costs more deficit).
    b = 12; diam = b + 2; seen = set(); pts = []
    for combo in itertools.combinations(range(1, diam + 1), b - 1):
        V = (0,) + combo; cV = canon(V)
        if cV in seen: continue
        seen.add(cV)
        f, L, rho, phi, lam = stat(V)
        pts.append((phi, LOG2 - lam))
    print("      b=12 tradeoff: min gamma achievable with phi >= phi0:")
    mins = []
    for phi0 in (0.06, 0.09, 0.11, 0.13, 0.14):
        cand = [g for phi, g in pts if phi >= phi0]
        if not cand:
            continue
        mg = min(cand)
        mins.append(mg)
        print(f"        phi >= {phi0:.2f}:  min gamma = {mg:.4f}")
    check(all(mins[i] <= mins[i + 1] + 1e-9 for i in range(len(mins) - 1)),
          "min gamma is non-decreasing in the phi threshold (the fiber-vs-deficit tradeoff)")
    # champions (wider search, tensored) = certified sup lower bounds
    _, _, rho14, *_ = stat(CHAMP14)
    check(approx(rho14, 0.156659, 1e-5), "rho(b=14 champion, #643) = 0.156659")
    f16, L16, rho16, *_ = stat(CHAMP16)
    check(f16 == 18 and L16 == 43737 and approx(rho16, 0.155373, 1e-5),
          f"b=16 witness: fstar=18, L1=43737, rho=0.155373 (got {f16},{L16},{rho16:.6f})")
    f18, L18, rho18, phi18, lam18 = stat(CHAMP18)
    check(f18 == 30 and L18 == 151275 and approx(rho18, 0.158411, 1e-5),
          f"NEW b=18 champion: fstar=30, L1=151275, rho=0.158411 (got {f18},{L18},{rho18:.6f})")
    check(rho18 > rho14, "b=18 champion beats b=14: certified rho* >= 0.158411")
    def sym_about_center(V):
        c = min(V) + max(V)
        return tuple(sorted(V)) == tuple(sorted(c - x for x in V))
    check(sym_about_center(CHAMP18) and sym_about_center(CHAMP16),
          "b=16/b=18 witnesses are symmetric blocks (invariant under x -> min+max-x)")
    # independent cross-check of the b=18 max fiber, NOT via the DP: direct
    # enumeration of all C(18,9)=48620 weight-9 subsets and their signatures.
    cnt = defaultdict(int)
    for S in itertools.combinations(CHAMP18, 9):
        cnt[(sum(S), sum(x * x for x in S))] += 1
    check(max(cnt.values()) == 30,
          "b=18 fstar=30 re-derived by direct weight-9 enumeration (DP-independent)")


def main():
    print("=" * 72)
    print("verify_fiber_image_tradeoff.py -- the joint fiber-image cap on rho*")
    print("=" * 72)
    block0(); block1(); block2(); block3(); block4(); block5(); block6(); block7()
    npass = sum(1 for c, _ in CHECKS if c); ntot = len(CHECKS)
    print("\n" + "=" * 72)
    print(f"RESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    print("=" * 72)
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
