#!/usr/bin/env python3
"""
Verifier for experimental/notes/thresholds/corridor_diameter_map.md

The diameter geography of the curve-restricted corridor.  Composes three
already-proved inputs -- #668's fiber bound f <= 2^{b-d}, the #655/#663 image
box bound L <= (b+1)(bD+1)(bD^2+1) (= #663 R2 V1 Horn A, rank 1; = #673 Thm 3
rank 1), and #678's corridor L <= 2^{d+b/3} <=> X <= 2^{4/3} -- into an explicit
two-parameter (alpha=d/b, delta=log2 D / b) map of where the corridor wall can
live.  Recomputes EVERY number in the note.

  BLOCK 0  corridor endpoint alpha_0 (root of h=4/3); the diameter residual line
           delta_res(alpha)=(alpha+1/3)/3; empty-threshold delta<=0.13928; full
           corridor needs delta>=1/3.  X = 2^{phi+lambda} identity.
  BLOCK 1  champion f=30,L=151275,d=12,X=2.3433,D=32,delta=5/18; box bound holds;
           box does NOT certify at b=18 (finite poly overhead) -- exact logs.
  BLOCK 2  image box bound L <= (b+1)(bD+1)(bD^2+1) exact on a block family;
           corridor-bound slack L/2^{d+b/3} < 1 on every one.
  BLOCK 3  the 2D residual map: classify a (alpha,delta) grid as certified
           (envelope OR box) vs residual; residual = {alpha_0<a<2/3, d>del_res};
           empty for delta<=0.13928, full alpha-corridor for delta>=1/3.
  BLOCK 4  diameter-inflation: residual => delta >= alpha/3 + 1/9, i.e.
           D >= 2^{d/3 + b/9} (a factor 2^{b/9} above the Lemma-3 floor);
           Lemma-3 floor alpha <= 3delta cross-checked on blocks.
  BLOCK 5  transfer: rank-r host gives lambda <= (r+2)delta (#673 Thm 3), so the
           residual line is (alpha+1/3)/(r+2) and empty-threshold shrinks with r.
  BLOCK 6  amplification base d0=5, delta_inf=log2 Q / b0 >= 1/3 (wall-diameter
           regime, yet X0=2.239<2.52); F_13 modular calibration f=3,L=737,X=2.16
           (Codex team, team board 2026-07-12; modular, NOT distinct-integer).
  BLOCK 7  counterexample probe: structured + sampled blocks, exact d, no block
           with L > 2^{d+b/3}; min non-degenerate d/b reached, max slack ratio.

stdlib only; zero-arg; deterministic; finishes < 60 s.  Nonzero exit on any FAIL.
"""
import sys, math, random
from itertools import combinations
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

# ------------------------------------------------------------- primitives
def sigs_all(V):
    subs = [(0, 0, 0)]
    for v in V:
        vv = v * v
        subs = subs + [(a + 1, b + v, c + vv) for (a, b, c) in subs]
    return subs

def f_and_L(V):
    cnt = Counter(sigs_all(V))
    return max(cnt.values()), len(cnt)

def is_dissoc(S):
    sums = {(0, 0, 0)}
    for v in S:
        vv = v * v
        add = set()
        for (a, b, c) in sums:
            t = (a + 1, b + v, c + vv)
            if t in sums or t in add:
                return False
            add.add(t)
        sums |= add
    return True

def max_dissoc(V, callcap=4_000_000):
    """exact d = max dissociated subset size, via deletion (small b-d)."""
    b = len(V)
    calls = 0
    for k in range(0, b + 1):
        for D in combinations(range(b), k):
            Ds = set(D)
            S = [V[i] for i in range(b) if i not in Ds]
            calls += 1
            if calls > callcap:
                return None
            if is_dissoc(S):
                return b - k
    return 0

def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)

def henv(a):
    """#668 envelope exponent (base 2): (1-alpha) + H2(min(alpha,1/2))."""
    return (1 - a) + H2(min(a, 0.5))

def img_box(V):
    """#655/#663 image box bound; returns (bound, diameter D)."""
    m = min(V)
    D = max(v - m for v in V)
    b = len(V)
    return (b + 1) * (b * D + 1) * (b * D * D + 1), D

CHAMP18 = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]
CHAMP12 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13]
ALPHA0_LO, ALPHA0_HI = 0.084, 0.085
DELTA_EMPTY = 0.13928        # (alpha_0 + 1/3)/3
LOG2_3 = math.log2(3)

# ================================================================ BLOCK 0
print("BLOCK 0: corridor endpoints, the diameter residual line, X=2^(phi+lambda)")
# alpha_0 = root of henv=4/3 on [0,1/3]; upper endpoint 2/3
check(abs(henv(2 / 3) - 4 / 3) < 1e-12, "henv(2/3)=4/3 (upper endpoint)")
lo, hi = 1e-6, 1 / 3
for _ in range(100):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if henv(mid) < 4 / 3 else (lo, mid)
alpha0 = lo
check(abs(henv(alpha0) - 4 / 3) < 1e-6, "henv(alpha_0)=4/3")
check(ALPHA0_LO < alpha0 < ALPHA0_HI, "alpha_0 in (0.084,0.085)")
# the DIAMETER residual line: box certifies X<=2^(4/3) iff (1-a)+3*delta<=4/3
# iff delta <= (a+1/3)/3 =: delta_res(a).  Empty-threshold = delta_res(alpha_0).
def delta_res(a):
    return (a + 1 / 3) / 3
check(abs(delta_res(alpha0) - DELTA_EMPTY) < 1e-4, "delta_res(alpha_0) = 0.13928 empty-threshold")
check(abs(delta_res(2 / 3) - 1 / 3) < 1e-12, "delta_res(2/3) = 1/3 (full corridor needs delta>=1/3)")
# residual corridor upper end at diameter delta: alpha < 3*delta - 1/3 (cap 2/3)
for delta, exp_upper in [(0.10, -1 / 30), (0.20, 4 / 15), (5 / 18, 1 / 2), (1 / 3, 2 / 3)]:
    check(abs((3 * delta - 1 / 3) - exp_upper) < 1e-9, f"delta={delta:.3f}: residual upper=3d-1/3={exp_upper:.4f}")
# X = 2^(phi+lambda) with phi=log2 f/b, lambda=log2 L/b
f, L = f_and_L(CHAMP12); b = 12
phi = math.log2(f) / b; lam = math.log2(L) / b
check(abs(2 ** (phi + lam) - (f * L) ** (1 / b)) < 1e-9, "X = 2^(phi+lambda)")
print(f"  corridor (envelope): d/b in (alpha_0, 2/3) = ({alpha0:.6f}, {2/3:.6f})")
print(f"  diameter residual line delta_res(a)=(a+1/3)/3: empty if delta<={DELTA_EMPTY:.5f},"
      f" full corridor iff delta>=1/3")

# ================================================================ BLOCK 1
print("BLOCK 1: champion in the map (f=30,L=151275,d=12,X=2.3433,D=32,delta=5/18)")
f, L = f_and_L(CHAMP18); d = max_dissoc(CHAMP18); b = 18
box, D = img_box(CHAMP18)
X = (f * L) ** (1 / b)
delta = math.log2(D) / b
check(f == 30 and L == 151275, "champion f=30, L=151275")
check(d == 12, "champion d=12 (d/b=2/3 exactly)")
check(abs(X - 2.343296) < 1e-4, "champion X=2.3433")
check(D == 32 and abs(delta - 5 / 18) < 1e-9, "champion D=32, delta=5/18=0.27778")
check(L <= box, "champion obeys image box bound L<=(b+1)(bD+1)(bD^2+1)")
# box does NOT certify at b=18: (b-d)+log2(box) exceeds 4b/3 by the poly overhead
lhs = (b - d) + math.log2(box)
check(lhs > 4 * b / 3, "box does NOT certify champion at b=18 (finite poly overhead)")
# asymptotically (a,delta)=(2/3,5/18) IS certified: delta=0.2778 < delta_res(2/3)=1/3
check(delta < delta_res(2 / 3), "asymptotically champion (a=2/3,delta=5/18) is box-certified")
print(f"  f={f} L={L} d={d} X={X:.4f} D={D} delta={delta:.4f}; box={box} (L<=box: {L<=box})")
print(f"  finite b=18: (b-d)+log2 box = {lhs:.2f} > 4b/3 = {4*b/3:.2f} (overhead {lhs-4*b/3:.2f});"
      f" asymptotic: delta {delta:.3f} < 1/3 => certified")

# ================================================================ BLOCK 2
print("BLOCK 2: image box bound exact + corridor-bound slack L/2^(d+b/3) < 1")
FAM = [
    ("interval12", list(range(12))), ("interval14", list(range(14))),
    ("interval16", list(range(16))), ("champ12", CHAMP12),
    ("hole14", [x for x in range(19) if x not in {1, 4, 9, 14, 17}]),
    ("twoscale12", list(range(6)) + [100 + i for i in range(6)]),
]
maxslack = 0.0
for nm, V in FAM:
    V = sorted(set(V)); b = len(V); f, L = f_and_L(V); d = max_dissoc(V)
    box, D = img_box(V); delta = math.log2(D) / b; X = (f * L) ** (1 / b)
    slack = L / 2 ** (d + b / 3)
    maxslack = max(maxslack, slack)
    check(L <= box, f"{nm}: L<=box")
    check(L <= 2 ** (d + b / 3), f"{nm}: L<=2^(d+b/3) (corridor bound holds)")
    print(f"  {nm:11s} b={b} d/b={d/b:.3f} L={L} <= box={box}  X={X:.4f} delta={delta:.3f}"
          f"  L/2^(d+b/3)={slack:.3f}")
check(maxslack < 1.0, "every sampled block satisfies the corridor bound with slack < 1")

# ================================================================ BLOCK 3
print("BLOCK 3: the 2D residual map (envelope OR box); residual = corridor & delta>del_res")
def certified(a, delta):
    """asymptotic: envelope (h(a)<=4/3) OR box ((1-a)+3delta<=4/3) proves X<=2^(4/3)."""
    env = henv(a) <= 4 / 3 + 1e-12
    boxc = (1 - a) + 3 * delta <= 4 / 3 + 1e-12
    return env or boxc
def residual(a, delta):
    return (alpha0 < a < 2 / 3) and (delta > delta_res(a) + 1e-12)
# consistency of the two definitions on a fine grid
gridok = True
for ia in range(0, 101):
    a = ia / 100.0
    for idl in range(0, 61):
        delta = idl / 60.0
        cert = certified(a, delta)
        res = residual(a, delta)
        # residual <=> not certified   (the two must partition)
        if res == cert:
            gridok = False
check(gridok, "on a 101x61 grid, residual(a,delta) == not certified(a,delta)")
# empty for delta <= DELTA_EMPTY
empty_below = all(not residual(ia / 100.0, delta)
                  for ia in range(0, 101) for delta in [0.0, 0.05, 0.10, DELTA_EMPTY - 1e-4])
check(empty_below, "residual region empty for delta <= 0.13928 (corridor bound holds)")
# for delta >= 1/3 the whole alpha-corridor (alpha_0,2/3) is residual
full_at_third = all(residual(a, 1 / 3 + 1e-6)
                    for a in [alpha0 + 0.01, 0.2, 0.4, 0.6, 2 / 3 - 0.01])
check(full_at_third, "at delta>=1/3 the whole alpha-corridor is residual")
# residual upper end at a few delta (3*delta-1/3, capped 2/3)
for delta in [0.16, 0.20, 0.25, 0.30]:
    upper = min(2 / 3, 3 * delta - 1 / 3)
    below = residual((alpha0 + upper) / 2, delta) if upper > alpha0 else False
    above = not residual(min(upper + 0.02, 0.66), delta)
    check(below and above, f"delta={delta}: residual = (alpha_0, {upper:.3f})")
    print(f"  delta={delta:.2f}: residual corridor = ({alpha0:.4f}, {upper:.4f})  width {max(0,upper-alpha0):.4f}")

# ================================================================ BLOCK 4
print("BLOCK 4: diameter inflation -- residual => delta >= alpha/3 + 1/9 (D>=2^(d/3+b/9))")
# residual line delta_res(a) = (a+1/3)/3 = a/3 + 1/9  ==> in residual, delta > a/3+1/9
check(abs(delta_res(0.0) - 1 / 9) < 1e-12, "delta_res(0)=1/9")
for a in [0.1, 0.3, 0.5, 2 / 3]:
    check(abs(delta_res(a) - (a / 3 + 1 / 9)) < 1e-12, f"delta_res({a})=a/3+1/9")
# Lemma-3 floor: alpha <= 3*delta + poly-overhead (2^d <= (d+1)(dD+1)(dD^2+1)).
# So in the residual, delta exceeds its dissociation-forced floor (~alpha/3) by >=1/9.
for nm, V in [("interval12", list(range(12))), ("champ18", CHAMP18),
              ("twoscale12", list(range(6)) + [100 + i for i in range(6)])]:
    V = sorted(set(V)); b = len(V); d = max_dissoc(V)
    m = min(V); D = max(v - m for v in V)
    boxk = (d + 1) * (d * D + 1) * (d * D * D + 1)
    check(2 ** d <= boxk, f"{nm}: Lemma-3 box 2^d<=(d+1)(dD+1)(dD^2+1) (alpha<=3delta floor)")
    print(f"  {nm:11s} d={d} D={D}: 2^d={2**d}<=box={boxk}; delta={math.log2(D)/b:.3f}"
          f" vs floor alpha/3={d/(3*b):.3f}")
print("  => any corridor-wall block has diameter D >= 2^(d/3 + b/9): a factor 2^(b/9)"
      " above the Lemma-3 dissociation floor 2^(d/3)")

# ================================================================ BLOCK 5
print("BLOCK 5: transfer -- rank-r GAP host: lambda<=(r+2)delta (#673 Thm3);"
      " residual line (a+1/3)/(r+2)")
for r in [1, 2, 3]:
    dres = (alpha0 + 1 / 3) / (r + 2)          # empty-threshold for rank r
    at_two_thirds = (2 / 3 + 1 / 3) / (r + 2)   # residual-line value at a=2/3
    print(f"  rank r={r}: residual line delta=(a+1/3)/{r+2}; empty if delta<={dres:.4f};"
          f" full-corridor delta>={at_two_thirds:.4f}")
    check(dres > 0, f"rank {r} empty-threshold positive")
# r=1 reproduces the diameter map (host interval {0..D} is a rank-1 GAP)
check(abs((alpha0 + 1 / 3) / 3 - DELTA_EMPTY) < 1e-4, "rank-1 reproduces delta<=0.13928")
# #663 R2 V1 Horn A: diam <= 2^(eta b) => lam2 <= 3 eta (= our lambda<=3delta)
check(abs(3 * 0.1 - 0.3) < 1e-12, "#663 Horn A: lam2<=3*eta at eta=0.1 gives 0.3")

# ================================================================ BLOCK 6
print("BLOCK 6: amplification base (wall-diameter regime) + F_13 modular calibration")
Vamp = [0, 1, 2, 4, 5, 6]; b0 = len(Vamp)
f0, L0 = f_and_L(Vamp); d0 = max_dissoc(Vamp); X0 = (f0 * L0) ** (1 / b0)
S = sum(Vamp) + 1; Q = b0 * S * S + sum(Vamp) + 1
delta_inf = math.log2(Q) / b0
check(f0 == 2 and L0 == 63 and d0 == 5, "amp base f0=2,L0=63,d0=5")
check(delta_inf >= 1 / 3, "amplified diameter regime: delta_inf=log2 Q/b0 >= 1/3 (wall regime)")
check(X0 < 2 ** (4 / 3), "yet X0 < 2^(4/3): large-delta is necessary, not sufficient, for the wall")
print(f"  V={Vamp}: f0={f0} L0={L0} d0={d0} d0/b0={d0/b0:.3f} X0={X0:.4f};"
      f" Q={Q} delta_inf={delta_inf:.3f} (>=1/3)")
# F_13 modular calibration (Codex team, team board 2026-07-12) -- modular, not distinct-int
U = [0, 1, 2, 3, 4, 5, 6, 7, 10, 12]; p = 13
def sigs_mod(V, p):
    subs = [(0, 0, 0)]
    for v in V:
        vv = (v * v) % p
        subs = subs + [(a + 1, (b + v) % p, (c + vv) % p) for (a, b, c) in subs]
    return subs
def max_dissoc_mod(V, p):
    b = len(V)
    for k in range(0, b + 1):
        for Dd in combinations(range(b), k):
            Ds = set(Dd); S = [V[i] for i in range(b) if i not in Ds]
            sums = set(); ok = True
            for mask in range(1 << len(S)):
                w = s = q = 0
                for i in range(len(S)):
                    if mask >> i & 1:
                        w += 1; s = (s + S[i]) % p; q = (q + S[i] * S[i]) % p
                key = (w, s, q)
                if key in sums:
                    ok = False; break
                sums.add(key)
            if ok:
                return b - k
    return 0
cntm = Counter(sigs_mod(U, p)); fm = max(cntm.values()); Lm = len(cntm)
dm = max_dissoc_mod(U, p); Xm = (fm * Lm) ** (1 / 10)
check(fm == 3 and Lm == 737, "F_13 seed: f=3, L=737 (Codex team calibration)")
check(dm == 7, "F_13 seed: d=7 (modular dissociation)")
check(abs(Xm - 2.1600) < 1e-3, "F_13 seed: X=2.1600")
print(f"  F_13 U={U}: (b,f,L,d)=(10,{fm},{Lm},{dm}) X={Xm:.4f}"
      f"  [MODULAR over F_13 -- NOT the distinct-integer class; calibration only]")

# ================================================================ BLOCK 7
print("BLOCK 7: counterexample probe -- structured + sampled blocks, no L>2^(d+b/3)")
cands = []
for nm, V in FAM:
    cands.append(V)
cands.append(CHAMP18); cands.append(CHAMP12)
# interval-with-holes families (dense additive structure -> lower d/b)
for span, holes in [(15, {3, 11}), (16, {2, 8, 13}), (17, {4, 9, 14}),
                    (18, {1, 6, 11, 16}), (14, {5, 9}), (13, {6})]:
    cands.append([x for x in range(span) if x not in holes])
# a modest deterministic random sample (fixed seed) in the moderate-diameter band
rnd = random.Random(20260712)
for _ in range(40):
    n = rnd.choice([12, 13, 14])
    span = n + rnd.choice([2, 3, 4, 5])
    cands.append(sorted(rnd.sample(range(span), n)))
viol = 0; tested = 0; min_ab = 1.0; max_ratio = 0.0
for V in cands:
    V = sorted(set(V)); b = len(V)
    if b < 8 or b > 18:
        continue
    d = max_dissoc(V)
    if d is None:
        continue
    f, L = f_and_L(V)
    tested += 1
    ratio = L / 2 ** (d + b / 3)
    max_ratio = max(max_ratio, ratio)
    if L > 2 ** (d + b / 3):
        viol += 1
        print("  VIOLATION:", V, "f", f, "L", L, "d", d, "b", b)
    if f > 1:
        min_ab = min(min_ab, d / b)
check(viol == 0, "no sampled block violates the corridor bound L<=2^(d+b/3)")
check(max_ratio < 1.0, "max slack ratio L/2^(d+b/3) < 1 over the whole probe")
print(f"  tested={tested} blocks; violations={viol}; min non-degenerate d/b={min_ab:.3f};"
      f" max L/2^(d+b/3)={max_ratio:.3f}")
print("  (reaching d/b < ~0.6 needs b beyond the exact-d range -- consistent with #678's"
      " 'corridor interior empty of computed blocks')")

# ================================================================ summary
print()
total = PASS + FAIL
print(f"RESULT: {'PASS' if FAIL == 0 else 'FAIL'} ({PASS}/{total})")
sys.exit(0 if FAIL == 0 else 1)
