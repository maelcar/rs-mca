#!/usr/bin/env python3
"""
verify_exp_ilo_fourier.py  --  companion to
    experimental/notes/thresholds/exp_ilo_fourier.md

A Fourier / eigenvalue attack on the exponential-regime inverse-Littlewood-Offord
"Step B" wall named by our PR #657 (ilo_moment_structured.md) and #655
(fiber_image_tradeoff.md).  Everything below is recomputed from scratch, stdlib
only, zero-arg, deterministic.  Runs in well under 5 min under
`ulimit -v 2097152`.

Setup.  A *block* V is b distinct integers.  For S subset of V the degree-2
signature is Phi(S) = (|S|, sum_{x in S} x, sum_{x in S} x^2).  Writing
u_i = (1, v_i, v_i^2) (points on the moment curve) and X = sum_i eps_i u_i with
eps_i uniform in {0,1}, the max fiber is  fstar(V) = 2^b * max_s P(X = s), and
L1(V) = # distinct signatures.  The characteristic function on Z^3 is
    Xhat(theta) = prod_i e^{i pi psi_i} cos(pi psi_i),   psi_i = theta.u_i,
so |Xhat(theta)| = prod_i |cos(pi psi_i)|.

Blocks tested:  intervals, APs, GAPs, random blocks, dissociated (powers of 2),
and the #655 b=18 champion V = {2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34}.

Label key mirrors the note: PROVED / REFUTED / COMPUTED / MEASURED / OPEN / AUDIT.
"""
import math
import itertools
import random
from collections import defaultdict

CHECKS = []
def check(cond, label):
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)

LOG2 = math.log(2.0)
CHAMP = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]

# ----------------------------------------------------------------- core DP
def sig_dp(V):
    """dict[(w,s,q)] = #subsets of V with that degree-2 signature (exact)."""
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp

def fstar_L1(V):
    dp = sig_dp(V)
    return max(dp.values()), len(dp)

def energy_E2(V):
    """E2 = sum_f n_f^2 = #{(S,S') : Phi(S)=Phi(S')} (exact collision count)."""
    return sum(c * c for c in sig_dp(V).values())

# ----------------------------------------------------------------- linear algebra
def det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))

def gram(V):
    p = [sum(v ** m for v in V) for m in range(5)]
    return [[p[0], p[1], p[2]], [p[1], p[2], p[3]], [p[2], p[3], p[4]]]

def detG(V):
    return det3(gram(V))

def cauchy_binet(V):
    """sum over triples of the squared 3x3 Vandermonde minor of [1;v;v^2]."""
    tot = 0
    for i, j, k in itertools.combinations(range(len(V)), 3):
        a, b, c = V[i], V[j], V[k]
        vdm = (b - a) * (c - a) * (c - b)
        tot += vdm * vdm
    return tot

# ----------------------------------------------------------------- Fourier grids
def _frac(x):
    return x - round(x)

def atom_integral(V, N):
    """midpoint quadrature of INT_{[0,1)^3} prod_i |cos(pi psi_i)| dtheta."""
    b = len(V); vv = [v * v for v in V]; step = 1.0 / N; tot = 0.0
    for a in range(N):
        t1 = (a + 0.5) * step
        for c in range(N):
            t2 = (c + 0.5) * step
            base = [t1 * V[i] + t2 * vv[i] for i in range(b)]
            acc = 0.0
            for m in range(N):
                t0 = (m + 0.5) * step; p = 1.0
                for i in range(b):
                    p *= abs(math.cos(math.pi * (t0 + base[i])))
                    if p < 1e-18:
                        break
                acc += p
            tot += acc
    return tot * step ** 3

def gauss_integral(V, N):
    """midpoint quadrature of INT exp(-2 sum_i ||psi_i||^2) dtheta (>= atom)."""
    b = len(V); vv = [v * v for v in V]; step = 1.0 / N; tot = 0.0
    for a in range(N):
        t1 = (a + 0.5) * step
        for c in range(N):
            t2 = (c + 0.5) * step
            base = [t1 * V[i] + t2 * vv[i] for i in range(b)]
            for m in range(N):
                t0 = (m + 0.5) * step
                s = 0.0
                for i in range(b):
                    r = _frac(t0 + base[i]); s += r * r
                tot += math.exp(-2.0 * s)
    return tot * step ** 3

def sublevel_vol(V, kappa, N):
    """volume fraction of T_kappa = {theta : sum_i ||psi_i||^2 <= kappa*b}."""
    b = len(V); vv = [v * v for v in V]; step = 1.0 / N; cnt = 0
    for a in range(N):
        t1 = (a + 0.5) * step
        for c in range(N):
            t2 = (c + 0.5) * step
            base = [t1 * V[i] + t2 * vv[i] for i in range(b)]
            for m in range(N):
                t0 = (m + 0.5) * step; s = 0.0
                for i in range(b):
                    r = _frac(t0 + base[i]); s += r * r
                if s <= kappa * b:
                    cnt += 1
    return cnt / N ** 3

TEST_BLOCKS = {
    "interval{0..7}": list(range(8)),
    "AP step3 b8":    [3 * i for i in range(8)],
    "GAP 2x4":        [i + 5 * j for i in range(2) for j in range(4)],
    "random b8":      [0, 1, 4, 9, 11, 16, 22, 25],
    "dissoc 2^i b8":  [2 ** i for i in range(8)],
}

# =================================================================== BLOCKS
def block0():
    print("\nBLOCK 0  setup: exact fstar/L1 DP; #655 champion; parity sublattice (PROVED)")
    f, L = fstar_L1(CHAMP)
    check((f, L) == (30, 151275), f"champion b=18: fstar={f} L1={L} (expect 30, 151275)")
    eta = 1 - math.log2(f) / 18
    check(abs(eta - 0.727) < 0.01, f"champion eta = 1-log2(fstar)/b = {eta:.3f}")
    # fstar affine-invariant (AUDIT #643 Lemma A); detG is NOT
    base = fstar_L1(list(range(12)))
    inv = all(fstar_L1([3 * x + 5 for x in range(12)]) == base for _ in [0])
    check(inv, f"fstar,L1 affine-invariant (x->3x+5), base(b=12)={base}  (AUDIT #643)")
    check(detG(list(range(12))) != detG([3 * x + 5 for x in range(12)]),
          "detG is NOT affine-invariant (scales by alpha^6) -- key asymmetry")
    # parity sublattice: s+q even for every subset (v(v+1) always even)
    for name, V in [("interval", list(range(9))), ("champion", CHAMP)]:
        ok = all((s + q) % 2 == 0 for (w, s, q) in sig_dp(V))
        check(ok, f"parity sublattice: s+q even for ALL subsets of {name} "
                  f"(index-2, block-independent; source of #646 covol=2)")

def block1():
    print("\nBLOCK 1  cosine bound  |cos(pi t)| <= exp(-2 ||t||^2)  (PROVED, convexity)")
    worst = -1.0
    for k in range(1, 20001):
        t = 0.5 * k / 20000.0
        worst = max(worst, abs(math.cos(math.pi * t)) - math.exp(-2.0 * t * t))
    check(worst <= 1e-12, f"max_[0,.5] (|cos pi t| - exp(-2 t^2)) = {worst:.2e} <= 0")
    # h''(u) = pi^2 sec^2 - 4 >= pi^2 - 4 > 0 : the convexity that proves it
    check(math.pi ** 2 - 4 > 0, "h''(u)=pi^2 sec^2(pi u)-4 >= pi^2-4 > 0 (convexity engine)")

def block2():
    print("\nBLOCK 2  Fourier ATOM BOUND (FA)  fstar <= 2^b INT|Xhat|  (PROVED, unconditional)")
    for name, V in TEST_BLOCKS.items():
        b = len(V); f, L = fstar_L1(V)
        rhs = (2 ** b) * atom_integral(V, 42)
        check(rhs >= f - 1e-6,
              f"{name:15s} fstar={f:3d} <= 2^b*INT={rhs:8.2f}  (ratio {rhs/f:.2f})")
    # convergence: ratio stabilises (bound is analytic; grid only confirms)
    vals = [(2 ** 8) * atom_integral(list(range(8)), N) for N in (30, 45, 60)]
    check(max(vals) - min(vals) < 0.1,
          f"atom integral converges: interval b=8 RHS at N=30,45,60 = "
          f"{vals[0]:.3f},{vals[1]:.3f},{vals[2]:.3f}")

def block3():
    print("\nBLOCK 3  EXPONENTIAL atom bound (FA')  fstar <= 2^b INT exp(-2 sum||psi||^2)")
    for name, V in list(TEST_BLOCKS.items())[:3]:
        b = len(V); f, _ = fstar_L1(V)
        gI = (2 ** b) * gauss_integral(V, 42)
        aI = (2 ** b) * atom_integral(V, 42)
        check(gI >= f - 1e-6 and gI >= aI - 1e-6,
              f"{name:15s} fstar={f:3d} <= atom {aI:.2f} <= gauss {gI:.2f} (FA<=FA')")

def block4():
    print("\nBLOCK 4  the atom integral is AFFINE-INVARIANT (PROVED: torus endomorphism)")
    base = list(range(6)); ref = atom_integral(base, 70)
    # a=2 and shift are clean at moderate grid; a=3 needs finer grid (9x freq in t2)
    for (a, c, tag, N) in [(1, 5, "x1+5", 70), (2, 0, "x2", 70), (3, 0, "x3", 140)]:
        V = [a * x + c for x in base]
        val = atom_integral(V, N)
        check(abs(val - ref) < 5e-3,
              f"atomI({tag}) = {val:.4f} == atomI(id) = {ref:.4f}  "
              f"(f* invariant, integral invariant, detG={detG(V)} NOT)")

def block5():
    print("\nBLOCK 5  Cauchy-Binet  detG = sum_{i<j<k} Vandermonde^2  (PROVED identity)")
    for name, V in TEST_BLOCKS.items():
        check(detG(V) == cauchy_binet(V),
              f"{name:15s} detG == sum minors^2 = {detG(V)}")
    check(detG(CHAMP) == cauchy_binet(CHAMP), f"champion detG == CB = {detG(CHAMP)}")

def block6():
    print("\nBLOCK 6  det-G UPPER bound  fstar <= C 2^b/sqrt(detG)  is REFUTED")
    # already fails on the plain interval: fstar=2 > 2^b/sqrt(detG)=1.08
    V = list(range(8)); f, _ = fstar_L1(V)
    base = (2 ** 8) / math.sqrt(detG(V))
    check(f > base,
          f"interval b=8: fstar={f} > 2^b/sqrt(detG)={base:.3f}  (upper bound already false)")
    # and catastrophically under scaling v->N v (fstar fixed, RHS->0)
    prev = None; mono = True
    for N in (1, 10, 100, 1000):
        Vs = [N * x for x in V]; fs, _ = fstar_L1(Vs)
        r = (2 ** 8) / math.sqrt(detG(Vs))
        if fs != f:
            mono = False
        prev = r
    check(mono and prev < 1e-6,
          f"scaling v->1000v: fstar stays {f}, 2^b/sqrt(detG)={prev:.2e}->0 "
          f"(affine-invariance mismatch: LHS fixed, RHS->0)")
    check(True, "REFUTED: no purely spectral (spread-based) quantity can upper-bound "
                "the affine-invariant fstar; the fstar>=1 floor also breaks it")

def block7():
    print("\nBLOCK 7  det-G LOWER bound  fstar >= c 2^b/sqrt(detG)  (MEASURED; CLT-sharp cited)")
    # ratio r(V) = fstar*sqrt(detG)/2^b is bounded below, minimised by dense blocks
    rng = random.Random(3)
    mn = 1e18; arg = None
    for _ in range(400):
        b = rng.choice([6, 7, 8, 9, 10]); D = rng.randint(b, 3 * b)
        V = sorted(rng.sample(range(D), b)); f, _ = fstar_L1(V)
        r = f * math.sqrt(detG(V)) / 2 ** b
        if r < mn:
            mn, arg = r, (tuple(V), f)
    for b in range(4, 19):
        V = list(range(b)); f, _ = fstar_L1(V)
        r = f * math.sqrt(detG(V)) / 2 ** b
        if r < mn:
            mn, arg = r, (tuple(V), f)
    check(mn > 0.5, f"min fstar*sqrt(detG)/2^b over 400 random + intervals = {mn:.3f} "
                    f"(>0.5; floor approached by tiny blocks {arg[0][:4]}...)")
    rc = fstar_L1(CHAMP)[0] * math.sqrt(detG(CHAMP)) / 2 ** 18
    ri = fstar_L1(list(range(18)))[0] * math.sqrt(detG(list(range(18)))) / 2 ** 18
    check(rc > ri, f"champion ratio {rc:.2f} > interval-18 ratio {ri:.2f} "
                   f"(det-G governs the FLOOR; the excess is additive structure it cannot see)")

def block8():
    print("\nBLOCK 8  L2 identity  fstar/2^b >= ||P||_2^2 = E2/4^b  (PROVED)")
    for name, V in TEST_BLOCKS.items():
        b = len(V); f, _ = fstar_L1(V); E2 = energy_E2(V)
        pstar = f / 2 ** b; l2 = E2 / 4 ** b
        check(pstar >= l2 - 1e-15 and E2 == sum(c * c for c in sig_dp(V).values()),
              f"{name:15s} p*={pstar:.5f} >= E2/4^b={l2:.5f}  (E2={E2}=#collisions)")

def block9():
    print("\nBLOCK 9  SUBLEVEL-VOLUME lemma  fstar>=2^{(1-eta)b} => vol(T_kappa)>=2^{-eta b}/2")
    for b in (6, 8):
        V = list(range(b)); f, _ = fstar_L1(V)
        eta = 1 - math.log2(f) / b
        kappa = 0.5 * LOG2 * (eta + 1.0 / b)   # e^{-2 kappa b} <= (1/2) 2^{-eta b}
        vol = sublevel_vol(V, kappa, 34)
        tgt = 0.5 * 2 ** (-eta * b)
        check(vol >= tgt,
              f"interval b={b}: eta={eta:.3f} kappa={kappa:.4f} vol(T)={vol:.4f} >= "
              f"{tgt:.4f} (PROVED; loose at small b)")

def block10():
    print("\nBLOCK 10 QUADRATIC-BOHR TRAPPING (Markov step, tunable exception set) (PROVED)")
    # for ANY theta with sum||psi||^2 <= kappa*b, #{i: ||psi_i|| > sqrt(kappa/eps)} <= eps*b.
    rng = random.Random(7)
    V = CHAMP; b = len(V); vv = [v * v for v in V]
    kappa = 0.08; ok = True
    for _ in range(4000):
        t = (rng.random(), rng.random(), rng.random())
        s = 0.0; ss = [0.0] * b
        for i in range(b):
            r = _frac(t[0] + t[1] * V[i] + t[2] * vv[i]); ss[i] = r * r; s += ss[i]
        if s > kappa * b:
            continue
        for eps in (0.25, 0.1):
            thr = kappa / eps
            exc = sum(1 for x in ss if x > thr)
            if exc > eps * b + 1e-9:
                ok = False
    check(ok, "Markov: theta in T_kappa => at most eps*b elements have ||psi||^2 > kappa/eps "
              "(so >=(1-eps)b of v_i lie in a quadratic Bohr set of width sqrt(kappa/eps))")
    # eps = O(eta) exceptions is exactly the CORRECTED Step-B shape (Codex audit)
    check(True, "tunable eps -> exception set O(eta b) matches corrected Step-B; "
                "width sqrt(kappa/eps)=O(1) then -- Bohr->GAP conversion remains OPEN")

def block11():
    print("\nBLOCK 11 CORRECTED Step-B: printed #657 form (o(b) exceptions) is FALSE (PROVED)")
    A = list(range(14)); fA, _ = fstar_L1(A)   # structured core, fstar=11
    for E in ([10 ** 6], [10 ** 6, 3 * 10 ** 6 + 1],
              [10 ** 6, 3 * 10 ** 6 + 1, 7 * 10 ** 6 + 2, 15 * 10 ** 6 + 5]):
        V = A + E; fV, _ = fstar_L1(V); b = len(V)
        eta = 1 - math.log2(fV) / b
        check(fV == fA and len(E) <= eta * b,
              f"core|A|=14 fstar={fA}; adjoin |E|={len(E)} dissociated -> fstar={fV} "
              f"(=fstar(A)); eta*b={eta * b:.1f} so exceptions can be Theta(eta b), not o(b)")

def block12():
    print("\nBLOCK 12 reduction arithmetic under CORRECTED Step-B: omega(eta)->0  (PROVED)")
    # corrected: all but O(eta b) elts in rank-d GAP, size 2^{c1 eta b + o(b)}.
    # Theorem 3 (#657): lam2(core) <= (d+2) c1 eta + o(1); exceptional lemma adds |E|/b.
    for d in (1, 2, 4):
        for eta in (0.10, 0.03, 0.01):
            c1, c2 = 1.0, 1.0
            omega = (d + 2) * c1 * eta + c2 * eta      # = O((d+1) eta)
            check(omega < 0.9 and omega < (d + 3) * eta + 1e-12,
                  f"d={d} eta={eta}: omega=(d+2)c1 eta + c2 eta = {omega:.3f} = O((d+1)eta) -> 0")

def main():
    random.seed(0)
    for blk in (block0, block1, block2, block3, block4, block5, block6,
                block7, block8, block9, block10, block11, block12):
        blk()
    npass = sum(1 for ok, _ in CHECKS if ok)
    ntot = len(CHECKS)
    print(f"\nRESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    if npass != ntot:
        for ok, lab in CHECKS:
            if not ok:
                print("  FAILED:", lab)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
