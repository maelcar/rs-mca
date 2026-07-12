#!/usr/bin/env python3
"""Verify championship_census_b19_26.md (rho-census for b=19..26, and the two
open ends of rho* in [0.158411, 0.405465]).

Stdlib-only, zero-arg, deterministic, re-derives every reported number.
`RESULT: PASS (75/75)`, ~42s / ~1.7GB peak (fits under `ulimit -v 2097152`) --
heavier than #655/#678's own verifiers since witnesses here run to b=26 with
L1 up to 6.2M (vs their b<=18, L1<~151K).

  BLOCK 0  setup: rho = phi+lambda-log2, X = (fstar*L1)^{1/b} = 2 e^rho;
           re-derive the #655 b=18 champion exactly (baseline for R1/R3)
  BLOCK 1  R1 championship search results: every b=19..26 witness re-derived
           by the exact subset-sum DP (fstar, L1, rho); every one < 0.158411;
           the b=19..22 exhaustive-within-class sweep re-derives the b=18
           champion as its own class-optimum (method sanity check)
  BLOCK 2  the two-block positional tensor lemma: f_combined=f1*f2,
           L_combined=L1*L2 exactly, checked on 3 explicit instances (a
           dissociated pair, a real-trade block x a dissociated block, and a
           real-trade block tensored with itself)
  BLOCK 3  small-b (1..17) plain-interval rho, exhaustive brute force,
           confirms none exceeds 0.158411 (feeds the tensor corollary)
  BLOCK 4  R2(a) calibration: X=(fL)^{1/b} for the new census stays under
           #678's off-corridor ceiling 2^{4/3}=2.5198 and far under 3
  BLOCK 5  R2(b) arithmetic: composing #678 Theorem A with X=2e^rho gives
           rho <= (1/3)log2 = 0.230... < log(3/2) on the off-corridor slice
  BLOCK 6  R3 Codex team F_13 calibration point: X=2.1600 -> rho=0.076961
           (arithmetic re-derivation only; the modular construction itself is
           external and not re-derived here)
  BLOCK 7  DP-independent cross-check of the smallest new champion (b=19) by
           direct brute-force enumeration at its own argmax weight

Exit 0 iff every check passes. Labels: PROVED / COMPUTED / MEASURED / AUDIT /
CONDITIONAL / OPEN (see note).

Credit: #655 fiber_image_tradeoff.md (the bracket, moment-curve reduction,
b=18 champion, affine invariance); DannyExperiments #668
canonical_transversal_vc_compression.md (f<=2^(b-d), L<=SS(d), fL<=3^b); #673
ilo_moment_closed_consumer.md (both-ends-unconditional reconciliation); #678
curve_restricted_product.md (dissociation-dimension envelope, Theorem A
off-corridor ceiling, itself crediting Codex team route cuts). The F_13 calibration point in BLOCK 6 is Codex team calibration, 2026-07-12. scottdhughes #564 w_a_star_pte_lemma.md (minimal degree-2
trade support 6).
"""
from __future__ import annotations
import itertools
import sys
from collections import defaultdict
from math import comb, log

LOG2 = log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ------------------------------------------------------------------ core DP
def sig_dp(V):
    """DP over elements -> dict[(w,s,q)] = multiplicity. Exact, no sampling."""
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
    """(fstar, L1, rho, phi, lam) for a block V; rho = phi+lam-log2."""
    dp = sig_dp(V)
    b = len(V)
    f = max(dp.values())
    L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def sym_set(offsets, center=False):
    V = []
    for o in offsets:
        V += [-o, o]
    if center:
        V.append(0)
    return V


def X_of(f, L, b):
    return (f * L) ** (1.0 / b)


CHAMP18 = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]


# ---------------------------------------------------------------- BLOCK 0
def block0():
    print("\n[BLOCK 0] setup + b=18 baseline")
    f, L, rho, phi, lam = stat(CHAMP18)
    check(f == 30 and L == 151275 and approx(rho, 0.158411, 1e-5),
          f"#655 b=18 champion re-derived: fstar=30, L1=151275, rho=0.158411 (got {f},{L},{rho:.6f})")
    X = X_of(f, L, 18)
    check(approx(X, 2.3432959, 1e-5), f"X(b=18) = 2^1.228539 = 2.343296 (got {X:.6f})")
    check(approx(log(1.5), 0.4054651081, 1e-9), "log(3/2) = 0.405465108...")


# ---------------------------------------------------------------- BLOCK 1
# R1 championship-search witnesses: the best-found block for each b=19..26,
# combining the exhaustive-within-class sweep (b=19..22) and the general
# incrementally-seeded hill-climb (b=19..26); every (offsets, center, f, L,
# rho) is exactly as reported in the note's Section 1.3 table.
NEW_CENSUS: dict[int, tuple] = {
    19: ([1, 2, 3, 4, 5, 12, 14, 15, 16], True, 35, 231262, 0.14404516719845673),
    20: ([1, 2, 4, 5, 12, 14, 15, 16, 21, 22], False, 36, 508381, 0.1429780886354185),
    21: ([1, 2, 3, 4, 5, 14, 15, 16, 22, 23], True, 46, 736714, 0.13250026861359876),
    22: ([1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 21], False, 96, 1056451, 0.14479708884348141),
    23: ([2, 3, 6, 9, 10, 14, 15, 21, 25, 26, 31], True, 66, 2405852, 0.12785583695165192),
    24: ([2, 6, 9, 10, 15, 21, 23, 24, 25, 26, 29, 31], False, 104, 3727586, 0.13083874845089527),
    25: ([2, 6, 9, 10, 15, 21, 23, 24, 25, 26, 29, 31], True, 133, 4997920, 0.11944807992277962),
    26: ([2, 6, 7, 9, 10, 15, 21, 23, 24, 25, 26, 29, 31], False, 266, 6181859, 0.12303073874940429),
}


def block1():
    print("\n[BLOCK 1] R1 championship search witnesses (b=19..26)")
    for b, (offsets, center, expect_f, expect_L, expect_rho) in NEW_CENSUS.items():
        V = sym_set(offsets, center)
        check(len(V) == b, f"b={b}: witness has exactly {b} elements")
        f, L, rho, phi, lam = stat(V)
        check(f == expect_f and L == expect_L and approx(rho, expect_rho, 1e-5),
              f"b={b}: fstar={expect_f}, L1={expect_L}, rho={expect_rho:.6f} (got {f},{L},{rho:.6f})")
        check(rho < 0.158411,
              f"b={b}: rho={rho:.6f} < 0.158411 (b=18 champion not beaten)")

    # method sanity: re-running the SAME exhaustive-within-class sweep used to
    # search b=19..22 at b=18 reproduces the #655 champion exactly (n=5 near
    # cluster, far window [12,16], h=1 hole) -- validates the search class.
    n, f0, w, h = 5, 12, 5, 1
    far_full = list(range(f0, f0 + w))
    best = (-99.0, None)
    for holes in itertools.combinations(range(w), h):
        hole_vals = {far_full[i] for i in holes}
        far = [x for x in far_full if x not in hole_vals]
        offs = list(range(1, n + 1)) + far
        if len(offs) != 9:
            continue
        f, L, rho, *_ = stat(sym_set(offs, False))
        if rho > best[0]:
            best = (rho, tuple(offs))
    check(approx(best[0], 0.158411, 1e-5) and best[1] == (1, 2, 3, 4, 5, 12, 14, 15, 16),
          f"sweep-class sanity: re-running the b=19..22 search class at b=18 "
          f"reproduces the #655 champion exactly (got rho={best[0]:.6f}, offsets={best[1]})")


# ---------------------------------------------------------------- BLOCK 2
def combine(V1, V2):
    """Positional (S+v)*Q^j tensor of two DIFFERENT blocks into one block of
    size len(V1)+len(V2) with f_combined=f1*f2, L_combined=L1*L2 exactly."""
    S0 = sum(abs(x) for x in V1) + 1
    S1 = sum(abs(x) for x in V2) + 1
    b1 = len(V1)
    Q = 4 * (S0 ** 2) * (b1 + 1) + 10 * S0 + 10
    return list(V1) + [(S1 + v) * Q for v in V2]


def block2():
    print("\n[BLOCK 2] two-block positional tensor lemma (f_combined=f1*f2, L_combined=L1*L2)")
    # (a) two dissociated blocks
    V1 = [1, 2, 3, 4, 5, 12, 14, 15, 16]
    V2 = [0, 1, 3, 7]
    f1, L1v, _, _, _ = stat(V1)
    f2, L2v, _, _, _ = stat(V2)
    Vc = combine(V1, V2)
    fc, Lc, _, _, _ = stat(Vc)
    check(fc == f1 * f2 and Lc == L1v * L2v,
          f"dissociated x dissociated: f_c={fc} (={f1}*{f2}), L_c={Lc} (={L1v}*{L2v})")

    # (b) a block with a genuine degree-2 PTE trade ({1,5,6} vs {2,3,7},
    # sum=12, sumsq=62 both -- minimal support-6 trade, hughes #564) x a
    # dissociated block
    V0 = [1, 2, 3, 5, 6, 7]
    f0, L0, _, _, _ = stat(V0)
    check(f0 == 2 and L0 == 63, f"real-trade block V0: fstar=2, L1=63 (got {f0},{L0})")
    Vc2 = combine(V0, V1)
    fc2, Lc2, _, _, _ = stat(Vc2)
    check(fc2 == f0 * f1 and Lc2 == L0 * L1v,
          f"real-trade x dissociated: f_c={fc2} (={f0}*{f1}), L_c={Lc2} (={L0}*{L1v})")

    # (c) the real-trade block tensored with ITSELF as two independent slots
    Vc3 = combine(V0, V0)
    fc3, Lc3, _, _, _ = stat(Vc3)
    check(fc3 == f0 * f0 and Lc3 == L0 * L0,
          f"real-trade x itself: f_c={fc3} (={f0}^2), L_c={Lc3} (={L0}^2)")


# ---------------------------------------------------------------- BLOCK 3
def block3():
    print("\n[BLOCK 3] small-b (1..17) plain-interval rho: exhaustive, none exceeds 0.158411")
    worst_over = None
    for b in range(1, 18):
        V = list(range(b))
        f, L, rho, _, _ = stat(V)
        if rho >= 0.158411:
            worst_over = (b, rho)
        check(rho < 0.158411, f"interval b={b}: rho={rho:.6f} < 0.158411")
    check(worst_over is None, "no plain-interval b in 1..17 reaches the b=18 champion rate")


# ---------------------------------------------------------------- BLOCK 4
def block4():
    print("\n[BLOCK 4] R2(a): new census X stays under #678's off-corridor ceiling 2^{4/3}")
    ceiling = 2 ** (4.0 / 3.0)
    check(approx(ceiling, 2.5198421, 1e-6), f"2^(4/3) = 2.519842 (got {ceiling:.6f})")
    for b, (offsets, center, f, L, rho) in NEW_CENSUS.items():
        X = X_of(f, L, b)
        check(X < ceiling, f"b={b}: X={X:.4f} < 2.5198 (off-corridor ceiling)")
        check(X < 3.0, f"b={b}: X={X:.4f} < 3 (universal #668 ceiling)")


# ---------------------------------------------------------------- BLOCK 5
def block5():
    print("\n[BLOCK 5] R2(b): off-corridor envelope o compression arithmetic")
    val = log(2 ** (4.0 / 3.0) / 2.0)
    check(approx(val, (1.0 / 3.0) * LOG2, 1e-12),
          f"log(2^(4/3)/2) = (1/3)log2 exactly (got {val:.9f} vs {(1.0/3.0)*LOG2:.9f})")
    check(val < log(1.5), f"(1/3)log2={val:.6f} < log(3/2)={log(1.5):.6f}")
    # #678 Theorem A closed-form endpoints
    def h(alpha):
        a = min(alpha, 0.5)
        H2 = 0.0 if a in (0.0, 1.0) else -a * (log(a) / LOG2) - (1 - a) * (log(1 - a) / LOG2)
        return (1 - alpha) + H2
    check(approx(h(2.0 / 3.0), 4.0 / 3.0, 1e-9), f"h(2/3) = 4/3 (got {h(2/3):.9f})")
    check(approx(2 ** h(2.0 / 3.0), ceiling_val := 2 ** (4.0 / 3.0), 1e-9),
          "2^h(2/3) = 2^(4/3) (Theorem A large-d endpoint)")


# ---------------------------------------------------------------- BLOCK 6
def block6():
    print("\n[BLOCK 6] R3: Codex team F_13 calibration point (arithmetic only)")
    X = 2.1600
    rho = log(X / 2.0)
    check(approx(rho, 0.0769610411, 1e-6),
          f"X=2.1600 (b=10, modular F_13, Codex team calibration) -> rho=0.076961 (got {rho:.6f})")
    check(rho < 0.158411, "F_13 calibration point sits below the b=18 champion")
    check(X < 2.3432959, "F_13 calibration point sits below the b=18 champion's X")


# ---------------------------------------------------------------- BLOCK 7
def block7():
    print("\n[BLOCK 7] DP-independent cross-check of the b=19 witness by direct enumeration")
    offsets, center, f_exp, L_exp, rho_exp = NEW_CENSUS[19]
    V = sym_set(offsets, center)
    b = len(V)
    dp = sig_dp(V)
    f_dp = max(dp.values())
    argmax_w = max(dp.items(), key=lambda kv: kv[1])[0][0]
    cnt = defaultdict(int)
    for S in itertools.combinations(V, argmax_w):
        cnt[(sum(S), sum(x * x for x in S))] += 1
    f_direct = max(cnt.values())
    check(f_direct == f_dp == f_exp,
          f"b=19 fstar={f_exp} re-derived by direct weight-{argmax_w} enumeration "
          f"(C({b},{argmax_w})={comb(b, argmax_w)} subsets), DP-independent (got {f_direct})")


def main():
    print("=" * 72)
    print("verify_championship_census_b19_26.py -- rho-census b=19..26")
    print("=" * 72)
    block0()
    block1()
    block2()
    block3()
    block4()
    block5()
    block6()
    block7()
    npass = sum(1 for c, _ in CHECKS if c)
    ntot = len(CHECKS)
    print("\n" + "=" * 72)
    print(f"RESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    print("=" * 72)
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
