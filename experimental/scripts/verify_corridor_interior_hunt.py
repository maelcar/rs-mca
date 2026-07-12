#!/usr/bin/env python3
"""
Verifier for experimental/notes/thresholds/corridor_interior_hunt.md

A targeted search for a corridor-interior wall witness (a block V with
X(V) = (f(V) L(V))^{1/b} > 2^{4/3} = 2.51984...), per #678's curve-restricted
product corridor (curve_restricted_product.md) and #682's diameter map
(corridor_diameter_map.md). Recomputes EVERY number reported in the note:

  BLOCK 0   definitions + the one-sided certificate arithmetic (PROVED): for
            ANY block, f<=2^(b-d) (DannyExperiments #668) plus X>2^(4/3) forces
            L>2^(d+b/3), regardless of the value of d -- a self-contained
            corridor-interior-forcing argument that needs no computation of d.
  BLOCK 1   Lemma 1 sufficiency (AUDIT of #678 Lemma 1): ceil(alpha_0*b)<=5 for
            every b in the searched range, so ANY 5 elements of ANY b>=5 block
            serve as a free, trivially-verified S0 certificate (no lacunary
            construction needed); spot-checked dissociation on two witnesses.
  BLOCK 2   champion reproduction (#655): b=18, f=30, L=151275, X=2.343296 --
            the bar every family below is measured against (NOTHING beats it).
  BLOCK 3   family (i): lacunary core + dense cluster, far and same-scale --
            NULL, monotonically declining as core size grows.
  BLOCK 4   family (ii): two-scale same-block grids V={a+M*c}, plain-interval
            and trade-bearing bases, several M -- NULL, interaction (small M)
            measurably HURTS relative to the large-M (near-tensor) limit.
  BLOCK 5   family (iii): CRT/modular lift of the Codex team's F_13 seed,
            full 2^10 wrap-choice search; own larger modular seeds (mod
            23/29/31) -- NULL, worse than the F_13 seed itself.
  BLOCK 6   family (iv): direct anneal witness + the diameter-stretch
            invariance check (affine dilation leaves f,L,X EXACTLY fixed,
            proved from the homogeneity of Phi under scaling).
  BLOCK 7   overall NULL summary: every computed X across every family and
            every witness is below 2^(4/3), and below the known champion.

stdlib only; zero-arg; deterministic (every witness is an explicit hardcoded
list, no RNG dependency); ~20-30s. Nonzero exit on any FAIL.

Two witnesses (a b=36 trade-bearing grid, two M values) are COMPUTED exactly
and reported in the note but are NOT in this fast gate (each takes ~50s);
they use the identical grid()+f_and_L_dp() code exercised on the b=18/24
cases in BLOCK 4, just at larger scale, and are reproducible by calling
grid([0,1,2,4,5,6],[0,1,2,4,5,6],M) for M in {7,8} through f_and_L_dp.
"""
import sys, math, time
from collections import Counter

PASS = 0
FAIL = 0
def check(cond, msg):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        print("  FAIL:", msg)
    return cond

TARGET = 2 ** (4/3)   # 2.5198420997897464
CHAMP18 = [2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34]

# ---------------------------------------------------------------- primitives
def f_and_L_dp(V, cap=25_000_000, max_seconds=90.0):
    """Exact f, L via incremental dict DP over (size,sum,sumsq) -> count.
    O(b*L) time, O(L) memory. Returns None if capped/timed out (safety valve;
    every USE of this function below either succeeds within the stated
    budget or is explicitly labeled as skipped)."""
    t0 = time.time()
    state = {(0, 0, 0): 1}
    for v in V:
        if len(state) > cap or (time.time() - t0) > max_seconds:
            return None
        vv = v * v
        new_state = dict(state)
        for (a, s, q), c in state.items():
            k = (a + 1, s + v, q + vv)
            new_state[k] = new_state.get(k, 0) + c
        state = new_state
    if len(state) > cap:
        return None
    return max(state.values()), len(state)

def f_and_L_bruteforce(V):
    """Cross-check via literal 2^b subset enumeration (small b only)."""
    subs = [(0, 0, 0)]
    for v in V:
        vv = v * v
        subs = subs + [(a + 1, s + v, q + vv) for (a, s, q) in subs]
    cnt = Counter(subs)
    return max(cnt.values()), len(cnt)

def is_dissoc(S):
    """Exact: all 2^|S| signatures Phi(subset) pairwise distinct."""
    sums = {(0, 0, 0)}
    for v in S:
        vv = v * v
        add = set()
        for (a, s, q) in sums:
            t = (a + 1, s + v, q + vv)
            if t in sums or t in add:
                return False
            add.add(t)
        sums |= add
    return True

def X_of(f, L, b):
    return (f * L) ** (1.0 / b)

def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)

def henv(alpha):
    return (1 - alpha) + H2(min(alpha, 0.5))

def grid(A, C, M):
    return sorted(set(a + M * c for a in A for c in C))

def mod_f_and_L(U, p):
    state = {(0, 0, 0): 1}
    for u in U:
        uu = (u * u) % p
        new_state = dict(state)
        for (a, s, q), c in state.items():
            k = (a + 1, (s + u) % p, (q + uu) % p)
            new_state[k] = new_state.get(k, 0) + c
        state = new_state
    return max(state.values()), len(state)

# ================================================================ BLOCK 0
print("BLOCK 0: definitions + the one-sided corridor-interior forcing argument")
check(abs(TARGET - 2.5198420997897464) < 1e-9, "TARGET = 2^(4/3) = 2.5198420997897464")
# alpha_0: root of henv(alpha) = 4/3 on [0, 1/3] (#678 Theorem A)
lo, hi = 1e-6, 1/3
for _ in range(100):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if henv(mid) < 4/3 else (lo, mid)
alpha0 = lo
check(abs(alpha0 - 0.084497) < 1e-5, "alpha_0 = 0.084497 (#678/#682 root of h=4/3)")
check(abs(henv(2/3) - 4/3) < 1e-12, "henv(2/3) = 4/3 (#678 Theorem A upper endpoint)")
# The one-sided forcing argument (PROVED, self-contained, no d computed):
#   f <= 2^(b-d)  (DannyExperiments #668, unconditional)
#   X > 2^(4/3)  =>  fL > 2^(4b/3)
#   =>  L > 2^(4b/3) / f  >=  2^(4b/3) / 2^(b-d)  =  2^(d + b/3)
# i.e. L > 2^(d+b/3) for whatever d=d(V) actually is -- a refutation of the
# OPEN corridor bound (#678 Section 8), fired the instant X(V) > 2^(4/3) is
# verified, without ever computing d exactly.
for b, d in [(20, 8), (24, 15), (30, 6), (36, 30), (18, 12)]:
    lhs = (4 * b / 3) - (b - d)     # exponent of the forced L-lower-bound
    rhs = d + b / 3
    check(abs(lhs - rhs) < 1e-9, f"b={b} d={d}: 4b/3-(b-d) == d+b/3 (forcing algebra)")
print(f"  alpha_0 = {alpha0:.6f}; forcing algebra 4b/3-(b-d)=d+b/3 verified on 5 (b,d) samples")
print("  Theorem A contrapositive (AUDIT, #678): X>2^(4/3) => alpha_0 < d/b < 2/3")
print("  one-sided certificate: f<=2^(b-d) (#668) + X>2^(4/3) => L>2^(d+b/3), any d, no d computed")

# ================================================================ BLOCK 1
print("BLOCK 1: Lemma 1 sufficiency -- d0=5 is a free S0 certificate throughout the search range")
for b in range(20, 41):
    need = math.ceil(alpha0 * b)
    check(5 >= need, f"b={b}: ceil(alpha_0*b)={need} <= 5 (Lemma 1's d>=5 suffices)")
check(math.ceil(alpha0 * 59) <= 5 and math.ceil(alpha0 * 60) > 5,
      "d0=5 stops sufficing only past b~59 (5/alpha_0=59.17), well outside 20..40")
# spot-check: first 5 elements of two witnesses are dissociated (Lemma 1's claim)
for nm, V in [("champ18", CHAMP18),
              ("anneal20", [-28,-23,-19,-16,-13,-12,-10,-8,-4,-1,1,4,8,10,12,13,16,19,23,28])]:
    S0 = sorted(V)[:5]
    check(is_dissoc(S0), f"{nm}: first-5 S0={S0} is dissociated (free Lemma-1 certificate)")
print("  ceil(alpha_0*b)<=5 for all b in 20..40; ANY 5 elements of ANY witness certify d/b>alpha_0")

# ================================================================ BLOCK 2
print("BLOCK 2: champion reproduction (#655) -- the bar for every family below")
fc, Lc = f_and_L_bruteforce(CHAMP18)
check(fc == 30 and Lc == 151275, "champ18: f=30, L=151275 (#655)")
Xc = X_of(fc, Lc, 18)
check(abs(Xc - 2.343296) < 1e-5, "champ18: X=2.343296")
print(f"  champ18 b=18 f={fc} L={Lc} X={Xc:.6f}  <-- NOTHING below beats this")

# ================================================================ BLOCK 3
print("BLOCK 3: family (i) -- lacunary core + dense cluster (NULL)")
fam1 = []
tests1 = [
    ("far k=2 (b=20)",         CHAMP18 + [3000, 9000],  20, 30, 605100),
    ("same-scale k=2 (b=19)",  CHAMP18 + [1, 3],        19, 32, 250614),
    ("same-scale k=3 (b=20)",  CHAMP18 + [1, 3, 9],     20, 38, 372969),
    ("same-scale k=4 (b=21)",  CHAMP18 + [1, 3, 9, 27], 21, 49, 511034),
]
for nm, V, b_exp, f_exp, L_exp in tests1:
    V = sorted(set(V))
    check(len(V) == b_exp, f"{nm}: b={b_exp}")
    f, L = f_and_L_dp(V)
    check(f == f_exp and L == L_exp, f"{nm}: f={f_exp} L={L_exp} (got f={f} L={L})")
    X = X_of(f, L, len(V))
    check(X < TARGET, f"{nm}: X={X:.6f} < TARGET")
    check(X < Xc, f"{nm}: X={X:.6f} < champion {Xc:.6f}")
    fam1.append(X)
    print(f"  {nm:26s} b={b_exp} f={f} L={L} X={X:.6f}")
check(fam1[1] > fam1[2] > fam1[3], "family(i): X strictly DECLINES as same-scale core grows (k=2>3>4)")
print(f"  family(i) best X = {max(fam1):.6f} (declining trend as core size grows)")

# ================================================================ BLOCK 4
print("BLOCK 4: family (ii) -- two-scale same-block grids V={a+M*c} (NULL)")
fam2 = []
grid_tests = [
    ("plain p4q5 M=40", range(4), range(5), 40, 20, 40, 474533),
    ("plain p4q5 M=20", range(4), range(5), 20, 20, 40, 473763),
    ("plain p4q5 M=4",  range(4), range(5), 4,  20, 98, 110627),
    ("trade  A6C3 M=7", [0,1,2,4,5,6], [0,1,2], 7, 18, 34, 75413),
    ("trade  A6C4 M=7", [0,1,2,4,5,6], [0,1,2,3], 7, 24, 442, 561409),
]
for nm, A, C, M, b_exp, f_exp, L_exp in grid_tests:
    V = grid(A, C, M)
    check(len(V) == b_exp, f"{nm}: b={b_exp} (got {len(V)})")
    f, L = f_and_L_dp(V)
    check(f == f_exp and L == L_exp, f"{nm}: f={f_exp} L={L_exp} (got f={f} L={L})")
    X = X_of(f, L, b_exp)
    check(X < TARGET, f"{nm}: X={X:.6f} < TARGET")
    check(X < Xc, f"{nm}: X={X:.6f} < champion")
    fam2.append(X)
    print(f"  {nm:26s} b={b_exp} f={f} L={L} X={X:.6f}")
check(fam2[0] > fam2[1] > fam2[2], "family(ii): plain-interval grid X DECLINES as M shrinks (interaction hurts)")
print(f"  family(ii) best X = {max(fam2):.6f} (large-M / near-tensor limit wins; interaction hurts)")
print("  [NOTE: a b=36 trade-grid (A=C={0,1,2,4,5,6}) gives X=2.185435 (M=7) and")
print("   X=2.217223 (M=8), f/L in the 10^5-10^7 range -- COMPUTED once (~50s/case,")
print("   identical method), reported in the note, not in this fast gate; still < champion]")

# ================================================================ BLOCK 5
print("BLOCK 5: family (iii) -- CRT/modular lift of the Codex team's F_13 seed (NULL)")
U13 = [0,1,2,3,4,5,6,7,10,12]; P13 = 13
fm, Lm = mod_f_and_L(U13, P13)
check((fm, Lm) == (3, 737), "F13 seed (modular): f=3, L=737")
Xm = X_of(fm, Lm, len(U13))
check(abs(Xm - 2.160025) < 1e-5, "F13 seed (modular): X=2.160025")
print(f"  F13 seed (mod 13, Codex team calibration)  b=10 f={fm} L={Lm} X={Xm:.6f}")

# full 2^10 wrap-choice search x_u = u + 13*k_u, k_u in {0,1} -- re-derive "best"
best = (0.0, None)
for mask in range(2 ** len(U13)):
    ks = [(mask >> i) & 1 for i in range(len(U13))]
    V = sorted(u + P13 * k for u, k in zip(U13, ks))
    if len(set(V)) != len(U13):
        continue
    f, L = f_and_L_bruteforce(V)
    X = X_of(f, L, len(V))
    if X > best[0]:
        best = (X, (ks[:], f, L, V))
bX, (bks, bf, bL, bV) = best
check(bks == [1,1,0,1,0,0,0,0,0,0], "full 2^10 search: best ks reproduced exactly")
check((bf, bL) == (3, 980), "F13 lift best: f=3, L=980")
check(abs(bX - 2.222464) < 1e-5, "F13 lift best: X=2.222464")
check(bX > Xm, "lift beats the raw modular value (careful wrap choice recovers some rate)")
check(bX < Xc, "F13 lift best still < champion")
print(f"  F13 best lift (full 2^10 search)  b=10 f={bf} L={bL} X={bX:.6f}  ks={bks}")

modseeds = [
    ("modseed p23 b16", [0,1,3,4,6,7,8,9,10,11,12,18,19,20,21,22], 23, 37, 5811),
    ("modseed p29 b20", [1,2,6,8,9,11,12,13,14,15,16,17,19,20,22,23,25,26,27,28], 29, 253, 12719),
    ("modseed p31 b22", [0,1,2,3,4,6,8,12,13,15,16,17,18,19,21,22,23,24,25,26,28,30], 31, 776, 16647),
]
for nm, U, p, f_exp, L_exp in modseeds:
    f, L = mod_f_and_L(U, p)
    check((f, L) == (f_exp, L_exp), f"{nm}: f={f_exp} L={L_exp} (got f={f} L={L})")
    X = X_of(f, L, len(U))
    check(X < Xm, f"{nm}: X={X:.6f} < F13 seed's own X (bigger own-search seeds are WORSE)")
    print(f"  {nm:26s} b={len(U)} f={f} L={L} X={X:.6f}  (mod {p})")
print(f"  family(iii) best X = {bX:.6f} (small b=10; scaling our own modular search up made things worse)")

# ================================================================ BLOCK 6
print("BLOCK 6: family (iv) -- direct anneal + diameter-stretch invariance")
Vanneal20 = [-28,-23,-19,-16,-13,-12,-10,-8,-4,-1,1,4,8,10,12,13,16,19,23,28]
check(len(Vanneal20) == 20, "anneal20: b=20")
fa, La = f_and_L_dp(Vanneal20)
check((fa, La) == (30, 573373), f"anneal20: f=30 L=573373 (got f={fa} L={La})")
Xa = X_of(fa, La, 20)
check(abs(Xa - 2.300265) < 1e-5, "anneal20: X=2.300265")
check(Xa < Xc, "anneal20: X < champion")
print(f"  anneal best (b=20)  f={fa} L={La} X={Xa:.6f}")

# affine dilation invariance (PROVED): Phi_{sV}(sS) = (|S|, s*sum_S, s^2*sumsq_S)
# is an injective reparametrization of Phi_V(S) for any s != 0, so f, L, X are
# EXACTLY unchanged under uniform dilation. Special case of #643 Lemma A.
def to_symmetric_offsets(V):
    c = sum(V) / len(V)
    return sorted(v - round(c) for v in V)
off = to_symmetric_offsets(CHAMP18)
check(off == [-16,-15,-14,-12,-5,-4,-3,-2,-1,1,2,3,4,5,12,14,15,16],
      "champion centered offsets reproduced exactly")
for s in [1, 3, 21]:
    V = sorted(o * s for o in off)
    f, L = f_and_L_dp(V)
    check((f, L) == (30, 151275), f"dilation s={s}: f,L EXACTLY unchanged (got f={f} L={L})")
    X = X_of(f, L, len(V))
    check(abs(X - Xc) < 1e-9, f"dilation s={s}: X EXACTLY unchanged (D={max(V)-min(V)})")
    print(f"  champion * s={s:2d}: D={max(V)-min(V):4d}  f={f} L={L} X={X:.6f}  (unchanged)")
# generality check: dilation invariance on a second, unrelated block
V2 = [0, 1, 2, 4, 5, 6]
f2a, L2a = f_and_L_dp(V2)
f2b, L2b = f_and_L_dp([v * 5 for v in V2])
check((f2a, L2a) == (f2b, L2b), "dilation invariance also holds on a second block {0,1,2,4,5,6}*5")
print("  dilation invariance (PROVED, special case of #643 Lemma A) confirmed on 2 blocks")

# ================================================================ BLOCK 7
print("BLOCK 7: overall NULL summary")
all_X = fam1 + fam2 + [bX, Xm] + [X_of(f,L,len(U)) for _,U,p,f,L in modseeds] + [Xa]
check(all(x < TARGET for x in all_X), "every computed X across every family < TARGET = 2^(4/3)")
check(all(x <= Xc + 1e-9 for x in all_X), "every computed X across every family <= known champion")
print(f"  {len(all_X)} witnesses checked; max X found = {max(all_X):.6f} "
      f"(vs champion {Xc:.6f}, vs TARGET {TARGET:.6f})")
print("  NULL: no family in this hunt found a corridor-interior witness; the champion")
print("  (#655, outside the corridor at d/b=2/3 exactly) remains the record.")

# ================================================================ summary
print()
total = PASS + FAIL
print(f"RESULT: {'PASS' if FAIL == 0 else 'FAIL'} ({PASS}/{total})")
sys.exit(0 if FAIL == 0 else 1)
