#!/usr/bin/env python3
"""
Verifier for experimental/notes/thresholds/curve_restricted_product.md

Curve-restricted refinement of DannyExperiments #668's compression bound
f * L <= 3^b, specialized to the distinct-integer degree-2 moment curve
weights a_i = (1, v_i, v_i^2).  Recomputes EVERY number in the note:

  BLOCK 0  the d-envelope h(alpha) and its peak = log2(3) at alpha = 1/3;
           X = 2 e^rho identity; max_d 2^{b-d} min(2^b,SS(d)) = 3^b (#668).
  BLOCK 1  #668 chain on named witnesses: f <= 2^{b-d}, L <= SS(d), fL <= 3^b,
           and the champion f=30, L=151275 (cross-checks #655).
  BLOCK 2  LEMMA 1: every 5-subset dissociated, a non-dissociated 6-subset
           exists (minimal trade support 6, hughes #564) -> d >= 5.
  BLOCK 3  LEMMA 2 (Pajor refinement): L <= #shattered <= N_dis(d) <= SS(d),
           strict (N_dis < SS) whenever a trade of support <= d exists.
  BLOCK 3b LEMMA 2b (signed-span, Codex team route cut): outside columns are signed
           {-1,0,1}-combinations of a max dissociated set, so L <= (2m+2)^d.
  BLOCK 4  LEMMA 3 (dissociation box bound): 2^d <= (d+1)(dD+1)(dD^2+1); the
           interval d-growth table (d/b descends, X stays flat ~2.27).
  BLOCK 5  THEOREM A (corridor localization): X <= 2^{h(d/b)} on every witness;
           d >= 2b/3 => X <= 2^{4/3} = 2.5198; d >= b/2 => X <= 2.8284.
  BLOCK 6  THEOREM B (corner localization) + the S2 overdetermination lemma
           b - d <= Con(I) (each outside element forced: x AND x^2 determined).
  BLOCK 7  MEASURED frontier: max X per d/b bin over a curated block sample;
           champion X = 2.3433 re-derived; corridor interior empty of blocks.
  BLOCK 8  amplification (Codex cut): positional Q-power tensor f_k=f^k, L_k=L^k,
           exponent preserved => X* >= 2.3433; exact counterguard exponents.

stdlib only; zero-arg; ulimit -v 2097152; ~<3 min.  Nonzero exit on any FAIL.
"""
import sys, math
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

# ---------------------------------------------------------------- primitives
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
    """all 2^|S| subset sums of {(1,v,v^2)} distinct; early-exit."""
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

def max_dissoc(V, callcap=6_000_000):
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

def max_dissoc_set(V):
    """one maximum dissociated set (the surviving elements)."""
    b = len(V)
    for k in range(0, b + 1):
        for D in combinations(range(b), k):
            Ds = set(D)
            S = [V[i] for i in range(b) if i not in Ds]
            if is_dissoc(S):
                return S
    return []

def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)

def SS(b, d):
    return sum(math.comb(b, j) for j in range(0, min(d, b) + 1))

def henv(alpha):
    """envelope exponent: (1-alpha) + H2(min(alpha,1/2))  (base 2)."""
    return (1 - alpha) + H2(min(alpha, 0.5))

def Xbound_from_d(b, d):
    return 2 ** (((b - d) + math.log2(min(2 ** b, SS(b, d)))) / b)

def N_dis(V, d):
    n = 0
    for k in range(0, d + 1):
        for C in combinations(V, k):
            if is_dissoc(list(C)):
                n += 1
    return n

def min_cost_reps(V):
    b = len(V)
    best = {}
    for mask in range(1 << b):
        w = s = q = 0
        for i in range(b):
            if mask >> i & 1:
                w += 1; s += V[i]; q += V[i] * V[i]
        key = (w, s, q)
        if key not in best or mask < best[key]:
            best[key] = mask
    return list(best.values())

def num_shattered(reps, b, dcap):
    cnt = 0
    for J in range(1 << b):
        pc = bin(J).count('1')
        if pc > dcap:
            continue
        traces = set()
        for R in reps:
            traces.add(R & J)
        if len(traces) == (1 << pc):
            cnt += 1
    return cnt

def Con(V, I):
    r"""S2 overdetermination for a dissociated set I inside V:
    #{ (A',B): A',B subseteq I disjoint, |B|=|A'|+1, (sumB-sumA')^2 = sumsqB-sumsqA' }.
    Each such tuple forces a UNIQUE candidate x = sumB - sumA' (both x and x^2 are
    determined -> overdetermined), so the number of DISTINCT forced x lying in V\I
    upper-bounds b - |I| when I is maximal.  Exhaustive over all r for |I| small."""
    Iset = list(I)
    con = 0
    forced_valid = set()
    outside = set(V) - set(I)
    m = len(Iset)
    for r in range(1, m // 2 + 2):           # |A'|=r-1, |B|=r, need 2r-1 <= m
        if 2 * r - 1 > m:
            break
        for A in combinations(Iset, r - 1):
            As = set(A); sA = sum(A); qA = sum(x * x for x in A)
            for B in combinations([x for x in Iset if x not in As], r):
                sB = sum(B); qB = sum(x * x for x in B)
                x = sB - sA
                if x * x == qB - qA:
                    con += 1
                    if x in outside:
                        forced_valid.add(x)
    return con, forced_valid

# named witnesses
CHAMP18 = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]
CHAMP12 = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13]
MIANCHOWLA = [1, 2, 4, 8, 13, 21, 31, 45, 66, 81, 97, 123, 148, 182]

# ================================================================ BLOCK 0
print("BLOCK 0: the d-envelope and #668 identities")
log2_3 = math.log2(3)
# peak of henv is at alpha=1/3, value log2(3)
check(abs(henv(1/3) - log2_3) < 1e-12, "henv(1/3)=log2 3")
for a in [0.0, 1/6, 0.25, 0.4, 0.5, 0.6, 0.75, 1.0]:
    check(henv(a) <= log2_3 + 1e-12, f"henv({a})<=log2 3")
    check(henv(a) < log2_3 - 1e-9 if abs(a - 1/3) > 1e-9 else True, f"henv({a})<log2 3 off-peak")
# X = 2 e^rho identity: rho = log(X/2)
for X in [2.0, 2.3433, 2.8284, 3.0]:
    rho = math.log(X / 2)
    check(abs(2 * math.exp(rho) - X) < 1e-9, f"X=2e^rho at X={X}")
# #668: max_d 2^{b-d} min(2^b,SS(b,d)) has exponent -> log2 3 (envelope), and the
# closed bound 2^{b-d} SS(d) <= 3^b holds for every d (their (3/2)^b step).
for b in [12, 18, 30]:
    worst = max(((b - d) + math.log2(min(2 ** b, SS(b, d)))) / b for d in range(0, b + 1))
    check(worst <= log2_3 + 1e-9, f"b={b}: max-d envelope <= log2 3")
    # #668's own inequality 2^{b-d} SS(d) <= 3^b for all d
    for d in range(0, b + 1):
        check((b - d) + math.log2(SS(b, d)) <= b * log2_3 + 1e-9,
              f"b={b} d={d}: 2^(b-d)SS(d)<=3^b")
print(f"  henv peak = log2(3) = {log2_3:.6f} at alpha=1/3 (X=3); henv<log2 3 elsewhere")
print(f"  henv(1/2)={henv(0.5):.4f} (X={2**henv(0.5):.4f}); henv(1/6)={henv(1/6):.4f} (X={2**henv(1/6):.4f})")
# corridor endpoints: henv(alpha)=4/3 at alpha=2/3 and at a lower root alpha_0
check(abs(henv(2 / 3) - 4 / 3) < 1e-12, "henv(2/3)=4/3")
lo, hi = 1e-6, 1 / 3
for _ in range(80):
    mid = (lo + hi) / 2
    (lo, hi) = (mid, hi) if henv(mid) < 4 / 3 else (lo, mid)
alpha0 = lo
check(abs(henv(alpha0) - 4 / 3) < 1e-6, "alpha_0 root of henv=4/3")
check(0.084 < alpha0 < 0.085, "alpha_0 ~ 0.0845")
print(f"  X <= 2^(4/3) = {2**(4/3):.4f} outside the corridor d/b in ({alpha0:.4f}, {2/3:.4f})")

# ================================================================ BLOCK 1
print("BLOCK 1: #668 chain on witnesses (f<=2^(b-d), L<=SS(d), fL<=3^b)")
for nm, V in [("interval12", list(range(12))), ("champ12", CHAMP12), ("champ18", CHAMP18)]:
    b = len(V); f, L = f_and_L(V); d = max_dissoc(V)
    check(d is not None, f"{nm}: d computed")
    check(f <= 2 ** (b - d), f"{nm}: f<=2^(b-d)")
    check(L <= SS(b, d), f"{nm}: L<=SS(d)")
    check(f * L <= 3 ** b, f"{nm}: fL<=3^b")
    print(f"  {nm:10s} b={b} f={f} L={L} d={d}  fL^(1/b)=X={ (f*L)**(1/b):.4f}")
# champion values cross-check #655
fc, Lc = f_and_L(CHAMP18)
check(fc == 30 and Lc == 151275, "champion f=30,L=151275 (matches #655)")
check(abs((fc * Lc) ** (1 / 18) - 2.3433) < 1e-3, "champion X=2.3433")

# ================================================================ BLOCK 2
print("BLOCK 2: LEMMA 1 (d>=5): every 5-subset dissociated; non-dissoc 6-subset")
for nm, V in [("interval12", list(range(12))), ("champ18", CHAMP18)]:
    all5 = all(is_dissoc(list(C)) for C in combinations(V, 5))
    has6 = any(not is_dissoc(list(C)) for C in combinations(V, 6))
    check(all5, f"{nm}: all 5-subsets dissociated")
    check(has6, f"{nm}: some 6-subset non-dissociated (trade support 6)")
    d = max_dissoc(V)
    check(d >= 5, f"{nm}: d>=5")
print("  every 5-subset dissociated (min trade support 6, hughes #564) => d>=5")

# ================================================================ BLOCK 3
print("BLOCK 3: LEMMA 2 (Pajor): L <= #shattered <= N_dis(d) <= SS(d)")
for nm, V in [("interval8", list(range(8))), ("interval10", list(range(10))),
              ("champ_ish10", [0, 1, 2, 3, 5, 6, 7, 8, 10, 11])]:
    b = len(V); f, L = f_and_L(V); d = max_dissoc(V)
    ss = SS(b, d); nd = N_dis(V, d)
    reps = min_cost_reps(V); ns = num_shattered(reps, b, d)
    check(L <= ns <= nd <= ss, f"{nm}: L<=#shat<=N_dis<=SS")
    check(nd < ss, f"{nm}: N_dis < SS (Pajor refinement has bite)")
    print(f"  {nm:12s} L={L} <= #shat={ns} <= N_dis={nd} <= SS={ss}")
for nm, V in [("interval12", list(range(12))), ("champ12", CHAMP12)]:
    b = len(V); f, L = f_and_L(V); d = max_dissoc(V)
    ss = SS(b, d); nd = N_dis(V, d)
    check(L <= nd <= ss and nd < ss, f"{nm}: L<=N_dis<SS")
    print(f"  {nm:12s} L={L} <= N_dis={nd} < SS={ss}  (N_dis/SS={nd/ss:.3f})")

# ================================================================ BLOCK 3b
print("BLOCK 3b: LEMMA 2b (signed-span): outside cols = signed D-combos; L<=(2m+2)^d")
def signed_combo(x, D):
    """find disjoint A',B subseteq D with a_x = sum_B a - sum_A' a (both coords)."""
    Dl = list(D)
    for r in range(1, len(Dl) // 2 + 2):
        for B in combinations(Dl, r):
            sB = sum(B); qB = sum(t * t for t in B)
            for A in combinations([t for t in Dl if t not in B], r - 1):
                if x == sB - sum(A) and x * x == qB - sum(t * t for t in A):
                    return True
    return False
for nm, V in [("interval12", list(range(12))), ("champ12", CHAMP12)]:
    V = sorted(V); b = len(V); f, L = f_and_L(V)
    D = max_dissoc_set(V); d = len(D); m = b - d
    outside = [x for x in V if x not in set(D)]
    # maximality <=> each outside x is a signed {-1,0,1}-combo of D (Lemma 2b proof)
    allcombo = all(signed_combo(x, D) for x in outside)
    check(allcombo, f"{nm}: every outside col is a signed D-combination")
    span = (2 * m + 2) ** d
    check(L <= span, f"{nm}: L <= (2m+2)^d")
    check(SS(b, d) < span, f"{nm}: (2m+2)^d dominated by SS(d) (structural, not tighter)")
    print(f"  {nm:12s} d={d} m={m}: L={L} <= (2m+2)^d={span}  (SS(d)={SS(b,d)} < span)")

# ================================================================ BLOCK 4
print("BLOCK 4: LEMMA 3 (dissociation box bound) + interval d-growth")
for nm, V in [("interval12", list(range(12))), ("champ18", CHAMP18),
              ("sidon10", MIANCHOWLA[:10])]:
    m = min(V); D = max(v - m for v in V); d = max_dissoc(V)
    box = (d + 1) * (d * D + 1) * (d * D * D + 1)
    check(2 ** d <= box, f"{nm}: 2^d <= (d+1)(dD+1)(dD^2+1)")
    # every dissociated set (of any size) obeys the per-size box: 2^k<=(k+1)(kD+1)(kD^2+1)
    print(f"  {nm:10s} d={d} D={D}: 2^d={2**d} <= box={box}  (d <= log2 box = {math.log2(box):.1f})")
print("  interval d-growth (d/b descends, X flat ~2.27 -> interval never nears X=3):")
prevX = []
for b in range(10, 19):
    V = list(range(b)); f, L = f_and_L(V); d = max_dissoc(V); X = (f * L) ** (1 / b)
    prevX.append((b, d / b, X))
    print(f"    b={b:2d} f={f:3d} L={L:6d} d={d:2d} d/b={d/b:.3f} X={X:.4f}")
check(max(x for _, _, x in prevX) < 2.30, "interval X stays < 2.30 across b=10..18")
check(min(a for _, a, _ in prevX) < 0.63, "interval d/b descends below 0.63 by b=18")

# ================================================================ BLOCK 5
print("BLOCK 5: THEOREM A (corridor): X<=2^h(d/b); d>=2b/3 => X<=2.5198; d>=b/2 => X<=2.8284")
c283 = 2 ** 1.5
c252 = 2 ** (4 / 3)
for nm, V in [("interval14", list(range(14))), ("champ12", CHAMP12), ("champ18", CHAMP18),
              ("sidon14", MIANCHOWLA)]:
    b = len(V); f, L = f_and_L(V); d = max_dissoc(V); X = (f * L) ** (1 / b)
    check(X <= Xbound_from_d(b, d) + 1e-9, f"{nm}: X<=2^h(d/b)")
    if 2 * d >= b:   # d >= b/2  ->  X <= 2^{2-d/b} <= 2.8284
        check(f * L <= 2 ** (2 * b - d), f"{nm}: d>=b/2 => fL<=2^(2b-d)")
        check(X <= c283 + 1e-9, f"{nm}: d>=b/2 => X<=2.8284")
    reg = ""
    if 3 * d >= 2 * b:   # d >= 2b/3  ->  f<=2^{b/3}, L<=2^b, fL<=2^{4b/3}
        check(f <= 2 ** (b - d) and f <= 2 ** (b / 3 + 1e-9), f"{nm}: d>=2b/3 => f<=2^(b/3)")
        check(f * L <= 2 ** (4 * b / 3) + 1e-6, f"{nm}: d>=2b/3 => fL<=2^(4b/3)")
        check(X <= c252 + 1e-9, f"{nm}: d>=2b/3 => X<=2.5198")
        reg = "  [d>=2b/3 => X<=2.5198]"
    print(f"  {nm:10s} d/b={d/b:.3f} X={X:.4f} <= 2^h(d/b)={Xbound_from_d(b,d):.4f}{reg}")
check(abs(c283 - 2.8284) < 1e-3 and abs(c252 - 2.5198) < 1e-3, "2^(3/2)=2.8284, 2^(4/3)=2.5198")

# ================================================================ BLOCK 6
print("BLOCK 6: THEOREM B (corner localization) + S2 overdetermination")
# X >= 3-delta => f,L >= ((3-delta)/2)^b => d/b <= 1 - log2((3-delta)/2)
for delta in [0.5, 0.3, 0.1, 0.0]:
    X = 3 - delta
    r = math.log2(X / 2)             # f,L >= 2^{r b}
    dub = 1 - r                      # d/b <= dub
    # sanity: at the envelope-optimal point d/b=1/3, f=2^{2b/3}>=2^{rb}, L=SS(b/3)>=2^{rb}
    check(2 / 3 >= r - 1e-9, f"delta={delta}: 2/3 >= r (f can reach)")
    check(H2(1 / 3) >= r - 1e-9, f"delta={delta}: H2(1/3) >= r (L can reach)")
    print(f"  X>=3-{delta:.2f}: f,L >= 2^({r:.4f} b), d/b <= {dub:.4f}")
check(abs(math.log2(1.5) - 0.585) < 1e-2, "log2(1.5)=0.585 (rate of the corner)")
# S2 overdetermination: for a MAXIMAL dissociated I, each outside x is forced
# (x and x^2 both determined by a witnessing (A',B)); verify b-|I| <= #forced_valid.
for nm, V in [("champ12", CHAMP12), ("interval12", list(range(12)))]:
    b = len(V); d = max_dissoc(V)
    # get one maximal dissociated set of size d by greedy deletion
    I = None
    for k in range(0, b + 1):
        for Dd in combinations(range(b), k):
            Ds = set(Dd); S = [V[i] for i in range(b) if i not in Ds]
            if is_dissoc(S):
                I = S; break
        if I is not None:
            break
    con, fv = Con(V, I)
    check(b - len(I) <= len(fv), f"{nm}: b-d <= #forced-x [S2 overdetermination]")
    print(f"  {nm:10s} b-d={b-len(I)} <= #forced-valid-x={len(fv)}  (Con={con} consistent"
          f" tuples; each forces a UNIQUE x since x and x^2 are both fixed)")

# ================================================================ BLOCK 7
print("BLOCK 7: MEASURED frontier -- max X per d/b bin; danger band [1/3,1/2] empty")
sample = [
    ("interval10", list(range(10))), ("interval12", list(range(12))),
    ("interval14", list(range(14))), ("interval16", list(range(16))),
    ("champ12", CHAMP12), ("champ18", CHAMP18),
    ("sidon14", MIANCHOWLA), ("geom12", [2 ** i for i in range(12)]),
    ("hole14", [x for x in range(19) if x not in {1, 4, 9, 14, 17}]),
    ("twoscale12", list(range(6)) + [100 + i for i in range(6)]),
    ("rand14", [0, 2, 5, 6, 9, 11, 12, 14, 17, 19, 21, 24, 25, 27]),
]
bins = {}
maxX = 0.0
mind_over_b = 1.0
for nm, V in sample:
    V = sorted(set(V)); b = len(V); f, L = f_and_L(V); d = max_dissoc(V); X = (f * L) ** (1 / b)
    key = round(d / b, 1)
    if key not in bins or X > bins[key][0]:
        bins[key] = (X, nm, b, d)
    maxX = max(maxX, X)
    if f > 1:
        mind_over_b = min(mind_over_b, d / b)   # ignore degenerate f=1 (Sidon/geom, X=2)
for k in sorted(bins):
    X, nm, b, d = bins[k]
    print(f"  d/b~{k:.1f}: maxX={X:.4f} ({nm}, b={b}, d={d})")
# no non-degenerate block has d/b in the danger band [0.34, 0.49]
danger = [nm for nm, V in sample
          if (lambda VV: (lambda b, f, d: f > 1 and 0.34 <= d / b <= 0.49)
              (len(VV), f_and_L(VV)[0], max_dissoc(VV)))(sorted(set(V)))]
check(len(danger) == 0, f"no non-degenerate block in danger band d/b in [1/3,1/2]: {danger}")
check(maxX <= 2.3433 + 1e-3, "max sampled X = champion 2.3433")
check(mind_over_b >= 0.5 - 1e-9, f"all non-degenerate sampled blocks have d/b>=0.5 (min={mind_over_b:.3f})")
print(f"  max sampled X = {maxX:.4f} (champion); min non-degenerate d/b = {mind_over_b:.3f}")

# ================================================================ BLOCK 8
print("BLOCK 8: amplification lower guard (Codex cut) + exact counterguard numbers")
# champion exponent and the 1.5-delta guard
fC, LC = f_and_L(CHAMP18)
eC = math.log2(fC * LC) / 18
check(abs(eC - 1.2285391474842977) < 1e-12, "champion exponent = 1.2285391474842977")
check(abs((1.5 - eC) - 0.2714608525157023) < 1e-12, "delta(1.5-exp) = 0.2714608525157023")
check(2 ** eC > 2.3432 and 2 ** eC < 2.3434, "X* >= 2^exp = 2.3433")
fI, LI = f_and_L(list(range(16)))
check(abs(math.log2(fI * LI) / 16 - 1.1867543039302069) < 1e-12,
      "interval16 exponent = 1.1867543039302069")
# positional-encoding amplification on the moment curve: f_k=f^k, L_k=L^k, exp preserved
Vamp = [0, 1, 2, 4, 5, 6]
b0 = len(Vamp); f0, L0 = f_and_L(Vamp)
Samp = sum(Vamp) + 1
Qamp = b0 * Samp * Samp + sum(Vamp) + 1        # no-carry Q^j spacing
heights = [(Samp + v) * (Qamp ** j) for j in range(2) for v in Vamp]
check(len(set(heights)) == 2 * b0, "amplified heights are distinct integers on the curve")
fk, Lk = f_and_L(sorted(heights))
check(fk == f0 * f0, f"amplify k=2: f_k = f^2 ({fk}={f0*f0})")
check(Lk == L0 * L0, f"amplify k=2: L_k = L^2 ({Lk}={L0*L0})")
check(abs(math.log2(fk * Lk) / (2 * b0) - math.log2(f0 * L0) / b0) < 1e-12,
      "amplify: exponent preserved (curve sup)")
print(f"  champion exponent {eC:.12f} -> X* >= {2**eC:.7f}; 1.5-delta guard delta<={1.5-eC:.12f}")
print(f"  amplify k=2 on {{0,1,2,4,5,6}}: f_k={fk}=f^2, L_k={Lk}=L^2, exp={math.log2(fk*Lk)/(2*b0):.6f} preserved")

# ================================================================ summary
print()
total = PASS + FAIL
print(f"RESULT: {'PASS' if FAIL == 0 else 'FAIL'} ({PASS}/{total})")
sys.exit(0 if FAIL == 0 else 1)
