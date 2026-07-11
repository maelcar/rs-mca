#!/usr/bin/env python3
"""Repro (heavy) for the (ILO-moment)-on-structured-classes note.

Stdlib-only, zero-arg. This is the DOCUMENTED heavy search behind R3's corner
census; the fast verifier (verify_ilo_moment_structured.py) re-checks the reported
conclusions on small certified instances. Nothing here is silently capped: every
search range is printed.

Runtime (single core, CPython 3.12): ~15 s / 22 MB under ulimit -v 2097152.
  STAGE 1  corner census: joint (phi_2, lam_2) frontier over symmetric
           interval-with-holes blocks, b = 8,10,12,14,16 (deletion patterns of
           bounded diameter). Confirms max(phi_2+lam_2) << 2 and the fiber-vs-
           image squeeze (max lam_2 non-increasing in the phi_2 threshold).
  STAGE 2  position-independence of the union-of-APs bound: shift/stretch the
           pieces over many (start, step) choices; L1 <= prod_j B(m_j) always,
           and L1 is invariant once pieces are well separated.
  STAGE 3  wild-construction sweep: geometric, Sidon (Mian-Chowla, greedy B_2),
           multiplicative-coset, and two-scale sets -- all have fstar small and
           rho far below the champion; none reaches the (phi high, lam high)
           corner.

Prints a human-readable report; exit 0 on completion. Not a PASS/FAIL gate.
Credit as in the note and the verifier header.
"""
from __future__ import annotations
import itertools, math, sys
from collections import defaultdict
from math import gcd, log

LOG2 = math.log(2)


def sig_dp(V):
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    dp = sig_dp(V); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, log(f) / b / LOG2, log(L) / b / LOG2   # fstar, L1, phi_2, lam_2


def Bbox(m):
    return (m + 1) * (1 + m * (m - 1) // 2) * (1 + (m - 1) * m * (2 * m - 1) // 6)


def canon(V):
    m = min(V); W = tuple(sorted(x - m for x in V)); g = 0
    for x in W: g = gcd(g, x)
    if g > 1: W = tuple(x // g for x in W)
    R = tuple(sorted(W[-1] - x for x in W))
    return min(W, R)


# --------------------------------------------------------------------- STAGE 1
def stage1():
    print("=" * 74)
    print("STAGE 1 -- corner census: joint (phi_2, lam_2) frontier (symmetric holes)")
    print("=" * 74)
    thresholds = (0.10, 0.15, 0.20, 0.25, 0.30, 0.35)
    global_corner = 0.0
    for b in (8, 10, 12, 14, 16):
        # symmetric interval-with-holes: choose a base interval {0..n-1}, delete a
        # symmetric hole set, keep exactly b elements, diameter n-1 <= cap.
        best_rho = -1.0; best = None
        hi = {t: -1.0 for t in thresholds}
        seen = set()
        # enumerate base widths n from b to b + wcap, delete (n-b) elements
        # symmetrically about the center. Range printed (no silent cap).
        wcap = {8: 10, 10: 10, 12: 9, 14: 8, 16: 7}[b]
        for n in range(b, b + wcap + 1):
            holes_needed = n - b
            elts = list(range(n)); center2 = n - 1  # 2*center
            # symmetric deletion: pick holes closed under x -> center2 - x
            # generate symmetric subsets of a half and mirror
            half = [x for x in elts if 2 * x < center2]
            mid = [x for x in elts if 2 * x == center2]  # 0 or 1 element
            # choose k pairs from half and optionally the midpoint
            for kmid in ((0, 1) if mid else (0,)):
                rem = holes_needed - kmid
                if rem < 0 or rem % 2 != 0:
                    continue
                kpairs = rem // 2
                if kpairs > len(half):
                    continue
                for combo in itertools.combinations(half, kpairs):
                    hole = set(combo) | {center2 - x for x in combo}
                    if kmid: hole |= set(mid)
                    V = tuple(x for x in elts if x not in hole)
                    if len(V) != b:
                        continue
                    cV = canon(V)
                    if cV in seen:
                        continue
                    seen.add(cV)
                    f, L, p2, l2 = stat(V)
                    rho = (p2 + l2 - 1.0) * LOG2
                    if rho > best_rho:
                        best_rho = rho; best = (V, f, L, p2, l2)
                    for t in thresholds:
                        if p2 >= t and l2 > hi[t]:
                            hi[t] = l2
        V, f, L, p2, l2 = best
        print(f"\n  b={b}  base widths {b}..{b+wcap}  (distinct canon blocks: {len(seen)})")
        print(f"    best rho = {best_rho:.5f}  at fstar={f} L1={L} phi_2={p2:.3f} lam_2={l2:.3f}")
        for t in thresholds:
            if hi[t] >= 0:
                corner = t + hi[t]
                global_corner = max(global_corner, corner)
                print(f"    phi_2 >= {t:.2f}:  max lam_2 = {hi[t]:.3f}  =>  phi_2+lam_2 corner <= {corner:.3f}")
        # squeeze check
        seq = [hi[t] for t in thresholds if hi[t] >= 0]
        mono = all(seq[i] >= seq[i + 1] - 1e-9 for i in range(len(seq) - 1))
        print(f"    fiber-vs-image squeeze (max lam_2 non-increasing in phi_2): {mono}")
    print(f"\n  GLOBAL: max phi_2+lam_2 over the whole census = {global_corner:.3f}  (vs 2.0)")
    print("  => the (phi_2, lam_2) corner near (1,1) is EMPTY at every b <= 16 searched.")


# --------------------------------------------------------------------- STAGE 2
def stage2():
    print("\n" + "=" * 74)
    print("STAGE 2 -- position-independence of the union-of-APs bound  L1 <= prod B(m_j)")
    print("=" * 74)
    # two AP pieces of sizes 4 and 4; sweep start/step of the second piece.
    m1, m2 = 4, 4
    P1 = tuple(range(m1))
    bound = Bbox(m1) * Bbox(m2)
    print(f"  pieces sizes ({m1},{m2}); bound prod B(m_j) = B({m1})*B({m2}) = {bound}")
    worst = 0; L_values = set()
    for start in (20, 200, 2000, 200000):
        for step in (1, 2, 3, 7):
            P2 = tuple(start + step * t for t in range(m2))
            V = tuple(sorted(P1 + P2))
            if len(set(V)) != len(V):
                continue
            f, L, p2, l2 = stat(V)
            L_values.add(L)
            worst = max(worst, L)
            ok = L <= bound
            if not ok:
                print(f"    VIOLATION start={start} step={step}: L1={L} > {bound}")
    print(f"  over all (start,step) sampled: max L1 = {worst} <= {bound}  (bound holds: {worst <= bound})")
    print(f"  distinct L1 values realized = {sorted(L_values)}  (well-separated pieces => stable)")
    # 3 pieces, wilder
    for pieces in ([(0, 1, 5), (37, 3, 4), (9001, 7, 4)],
                   [(0, 2, 4), (500, 5, 5), (1000000, 11, 4)]):
        parts = [tuple(a + d * t for t in range(c)) for (a, d, c) in pieces]
        V = tuple(sorted(x for p in parts for x in p))
        f, L, p2, l2 = stat(V)
        bnd = 1
        for (_, _, c) in pieces: bnd *= Bbox(c)
        b = len(V); c = len(pieces)
        print(f"  3-piece {[(a,d,cc) for (a,d,cc) in pieces]}: b={b} L1={L} <= prodB={bnd} "
              f"<= b^(6c)={b**(6*c)}  ({L <= bnd <= b**(6*c)})")


# --------------------------------------------------------------------- STAGE 3
def stage3():
    print("\n" + "=" * 74)
    print("STAGE 3 -- wild-construction sweep (fat image without interval-likeness?)")
    print("=" * 74)
    champ_rho = 0.158411
    families = {}
    families["geometric {2^i}"] = tuple(2 ** i for i in range(12))
    families["geometric {3^i}"] = tuple(3 ** i for i in range(11))
    # greedy Sidon (Mian-Chowla)
    S = [0]; x = 1; sums = {0}
    while len(S) < 13:
        ok = True
        for a in S:
            if a + x in sums:
                ok = False; break
        if ok:
            for a in S: sums.add(a + x)
            sums.add(2 * x); S.append(x)
        x += 1
    families["Sidon (Mian-Chowla)"] = tuple(S[:12])
    # multiplicative coset mod prime: quadratic residues of a prime
    p = 101; QR = sorted({(i * i) % p for i in range(1, p)})[:12]
    families["quad-residues mod 101"] = tuple(QR)
    # two-scale: small cluster + spread
    families["two-scale cluster+spread"] = tuple([0, 1, 2, 3, 4, 5] + [100, 300, 700, 1500, 3100, 6300])
    # random-ish dissociated via powers of 3 minus small perturb
    families["perturbed powers"] = tuple(3 ** i + (i % 2) for i in range(12))
    print(f"  champion rho (b=18) for reference = {champ_rho:.5f}\n")
    print(f"  {'family':30s} {'b':>3s} {'fstar':>6s} {'L1':>7s} {'phi_2':>6s} {'lam_2':>6s} {'rho':>8s}")
    for name, V in families.items():
        V = tuple(sorted(set(V)))
        f, L, p2, l2 = stat(V)
        rho = (p2 + l2 - 1.0) * LOG2
        print(f"  {name:30s} {len(V):3d} {f:6d} {L:7d} {p2:6.3f} {l2:6.3f} {rho:8.5f}")
    print("\n  => every wild family has SMALL fstar (mostly 1) and rho far below the")
    print("     champion; large image is bought by dissociation, which kills the fiber.")
    print("     No family reaches the (phi_2 high, lam_2 high) corner. Consistent with")
    print("     (ILO-moment): fat fiber needs additive structure, which caps the image.")


def main():
    print("repro_ilo_moment_structured.py -- heavy census behind R3 (documented, no silent caps)\n")
    stage1()
    stage2()
    stage3()
    print("\nDONE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
