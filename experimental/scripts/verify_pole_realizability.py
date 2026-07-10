#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/simple_pole_realizability.md.

Settles the realizability of prop:simple-pole-lower's witness construction on
the window where SB2 of thm:unconditional-support-envelope-bracket invokes it
(asymptotic_rs_mca_frontiers.tex).  This is the definitive resolution of #524's
ledger entry L-3 ("bracket lower-leg realizability").

Zero-argument, stdlib-only (no numpy/sympy).  Recomputes EVERY gated number:

  A. deep-regime  a >= a_deep = ceil((2n+k)/3)  is contained *strictly* in the
     list-<=1 zone  a > (n+k)/2  (holds exactly because n>k; margin (n-k)/6).
  B. min-distance rigidity forces the identity list floor L(a)=1 throughout the
     list-<=1 zone: binom(n,a) <= |B|^{a-k-1} for a>(n+k)/2 (|B|>=n).  Hence on
     the whole deep regime L(a)=1, M(L(a))=1, P(a)=1 -- the pole floor collapses
     to the trivial floor and cannot overshoot.
  C. collision-aware M(L) properties: 1<=M<=L, M(1)=1, monotone when q-n>=k,
     and M(L) <= q-n (so P <= |Gamma|).
  D. realizability as a valid floor: P(a) <= U(a) (exact support upper) for ALL
     a in [k+1,n]; and P(a) <= E(a) (exact deep numerator) on the deep regime --
     P never exceeds the true numerator.  Zone census: P>E only in the shallow
     non-deep band a<=(n+k)/2.
  E. faithful RS-MCA brute force (support-wise noncommon MCA-bad, per L187-201):
     deep k=1/F5 (reproduce #524) gives B^MCA=r+1=E, P=1; shallow k=1/F11 gives
     B^MCA=P=U>E (P realizable AND strictly tighter); a sampled k=2/F7 non-
     constant row confirms P<=B^MCA<=U.

Exit 0 and print `RESULT: PASS (N checks)` iff all gates hold; else exit 1.
Runs from anywhere.
"""
import sys, random
from math import comb, ceil
from itertools import product, combinations

CHECKS = []
def check(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL:", name)
    return bool(cond)

# ----------------------------------------------------------------------
# Paper functions (SB1 of thm:unconditional-support-envelope-bracket, L6216)
# ----------------------------------------------------------------------
def Lid(n, a, k, B):
    """Identity list floor L(a)=ceil(binom(n,a) |B|^{-(a-k-1)}) (prop:exact-prefix-list)."""
    w = a - k - 1
    assert w >= 0
    return -((-comb(n, a)) // (B ** w))            # exact integer ceil

def Mpole(L, q, n, k):
    """Collision-aware bad-slope count M(L)=ceil(L(q-n)/(q-n+k(L-1))) (thm:collision-aware-pole, 4.2)."""
    num = L * (q - n)
    den = (q - n) + k * (L - 1)
    return -((-num) // den)                         # exact integer ceil

def Pval(n, a, k, B, q, G):
    """Pole lower reserve P(a)=ceil((|Gamma|/q) M(L(a))) (SB1)."""
    M = Mpole(Lid(n, a, k, B), q, n, k)
    return -((-G * M) // q)                          # ceil(G*M/q)

def Uval(n, a, G):
    """Exact support-atlas upper U(a)=min{|Gamma|, binom(n,a)} (prop:exact-support-upper, 2.2)."""
    return min(G, comb(n, a))

def Eval(n, a, G):
    """Universal tangent floor / exact deep numerator E(a)=min{|Gamma|, n-a+1}
       (prop:universal-tangent-floor 3.6 = lower bound everywhere;
        cor:exact-deep-numerator = equality on the deep regime)."""
    return min(G, n - a + 1)

def a_deep(n, k):
    """First deep agreement: 3(n-a)<=n-k  <=>  a >= ceil((2n+k)/3)."""
    return -((-(2 * n + k)) // 3)

# ======================================================================
# GROUP A -- deep regime is strictly inside the list-<=1 zone
# ======================================================================
# The true list (max # of dim-(k+1) codewords agreeing with one word on >=a
# coords) is <=1 once a>(n+k)/2, because two such codewords overlap in <=k
# coords (their degree-<=k difference has <=k roots), forcing union 2a-k<=n.
# Deep boundary a_deep>(n+k)/2 iff (2n+k)/3>(n+k)/2 iff n>k -- always true.
A_contain_fail = 0
A_margin_ok = True
for n in range(3, 220):
    for k in range(1, n):
        ad = a_deep(n, k)
        # smallest deep agreement is strictly above (n+k)/2:  2*a_deep - k > n
        if not (2 * ad - k > n):
            A_contain_fail += 1
        # algebraic margin (2n+k)/3-(n+k)/2 = (n-k)/6 > 0, i.e.
        # 2(2n+k)-3(n+k) = n-k over the common denominator 6.
        if not (2 * (2 * n + k) - 3 * (n + k) == (n - k) and n - k > 0):
            A_margin_ok = False
check("A1 deep-regime strictly inside list<=1 zone (a_deep>(n+k)/2), all n>k", A_contain_fail == 0)
check("A2 containment margin equals (n-k)/6 > 0", A_margin_ok)

# ======================================================================
# GROUP B -- rigidity forces L(a)=1 on the list-<=1 zone (=> no overshoot)
# ======================================================================
# If prop:exact-prefix-list's pigeonhole floor exceeded the true list, it would
# contradict the C^+ minimum distance.  Consistency REQUIRES, for a>(n+k)/2:
#     binom(n,a) <= |B|^{a-k-1}     (|B|>=n, worst case |B|=n).
# We gate this identity; a failure would be a genuine paper bug (report it).
B_star_fail = 0
B_star_tested = 0
for n in range(3, 70):
    for k in range(1, n):
        for a in range(k + 1, n + 1):
            if 2 * a - k > n:                        # a > (n+k)/2  (strict)
                for B in (n, n + 1, 2 * n):          # |B|>=n
                    B_star_tested += 1
                    if comb(n, a) > B ** (a - k - 1):
                        B_star_fail += 1
check("B1 rigidity bound binom(n,a)<=|B|^{a-k-1} for a>(n+k)/2 (all tested)", B_star_fail == 0)

# Consequently L(a)=1, M=1, P=1 throughout the deep regime, for every field size.
B_deepP_fail = 0
B_deepP_tested = 0
for n in range(3, 55):
    for k in range(1, n):
        for a in range(a_deep(n, k), n + 1):         # deep regime
            for q in (n + 1, n + 2, 2 * n, 5 * n):
                for B in (n, q):
                    for G in (1, 2, max(1, q // 2), q):
                        B_deepP_tested += 1
                        L = Lid(n, a, k, B)
                        if L != 1:
                            B_deepP_fail += 1
                        elif Pval(n, a, k, B, q, G) != 1:
                            B_deepP_fail += 1
check("B2 deep regime => L(a)=1 and P(a)=1 (pole floor collapses to trivial)", B_deepP_fail == 0)

# Direct empirical confirmation of the list-<=1 bound (star): brute force over
# tiny RS(D,k+1) rows -- no received word has >=2 codewords agreeing on >=a
# coords once a>(n+k)/2.
def list_size_max(q, n, k, a):
    """max over received words u of #{deg<=k polys agreeing with u on >=a of the
       first n field elements}.  Enumerated via which a-subset each codeword hits;
       equivalently: max # pairwise 'a-far-agreeing' codewords -> we test the
       structural claim that any two distinct deg<=k polys agree on <=k points."""
    # For the (star) claim it suffices to confirm any two distinct deg<=k
    # polynomials coincide on at most k of the n points (=> overlap<=k =>
    # union>=2a-k), which is the degree bound; gate it over all coeff tuples.
    pts = list(range(n))
    worst = 0
    for c1 in product(range(q), repeat=k + 1):
        p1 = [sum(c1[j] * (x ** j) for j in range(k + 1)) % q for x in pts]
        for c2 in product(range(q), repeat=k + 1):
            if c2 <= c1:
                continue
            p2 = [sum(c2[j] * (x ** j) for j in range(k + 1)) % q for x in pts]
            agree = sum(1 for i in range(n) if p1[i] == p2[i])
            if agree > worst:
                worst = agree
    return worst
# any two distinct dim-(k+1) codewords agree on <= k of n points
ov = list_size_max(5, 4, 1, 3)      # k=1 over F5, n=4
check("B3 distinct dim-(k+1) codewords agree on <=k points (F5,n=4,k=1): %d<=1" % ov, ov <= 1)
ov2 = list_size_max(5, 4, 2, 4)     # k=2 over F5, n=4
check("B3b distinct dim-(k+1) codewords agree on <=k points (F5,n=4,k=2): %d<=2" % ov2, ov2 <= 2)

# ======================================================================
# GROUP C -- collision-aware M(L) properties
# ======================================================================
C_fail = 0
for q in range(6, 60):
    for n in range(3, q):
        for k in range(1, n):
            for L in range(1, 40):
                M = Mpole(L, q, n, k)
                if not (1 <= M <= L):
                    C_fail += 1
                if L == 1 and M != 1:
                    C_fail += 1
                if M > q - n:                        # => P <= |Gamma|
                    C_fail += 1
                if q - n >= k and L >= 2 and Mpole(L - 1, q, n, k) > M:
                    C_fail += 1                      # monotone nondecreasing
check("C M(L): 1<=M<=L, M(1)=1, M<=q-n, monotone when q-n>=k", C_fail == 0)

# ======================================================================
# GROUP D -- P is a valid (realizable) floor: never exceeds U, nor E in deep
# ======================================================================
PU_fail = 0
PE_deep_fail = 0
maxPE_U_fail = 0
zone_useful = zone_eq = zone_trivial = 0
zone_useful_nondeep_shallow = 0
D_tested = 0
for n in range(3, 40):
    for k in range(1, n):
        for q in (n + 1, n + 2, n + 3, 2 * n, 3 * n, 5 * n):
            for B in (n, q):
                if B > q:
                    continue
                for G in (1, 2, max(1, q // 4), max(1, q // 2), q - 1, q):
                    if G < 1:
                        continue
                    for a in range(k + 1, n + 1):
                        D_tested += 1
                        L = Lid(n, a, k, B)
                        p = Pval(n, a, k, B, q, G)
                        u = Uval(n, a, G)
                        e = Eval(n, a, G)
                        if p > u:
                            PU_fail += 1
                        if max(p, e) > u:
                            maxPE_U_fail += 1
                        if 3 * (n - a) <= n - k:      # deep
                            if p > e:
                                PE_deep_fail += 1
                        if p > e:
                            zone_useful += 1
                            if (3 * (n - a) > n - k) and (2 * a - k <= n):
                                zone_useful_nondeep_shallow += 1
                        elif p == e:
                            zone_eq += 1
                        else:
                            zone_trivial += 1
check("D1 P(a)<=U(a) for ALL a in [k+1,n] (P never exceeds exact upper)", PU_fail == 0)
check("D2 P(a)<=E(a) on the deep regime (P never overshoots true numerator)", PE_deep_fail == 0)
check("D3 max{P,E}<=U everywhere (combined lower leg is consistent)", maxPE_U_fail == 0)
check("D4 P>E occurs ONLY in the shallow non-deep band a<=(n+k)/2",
      zone_useful > 0 and zone_useful == zone_useful_nondeep_shallow)

# ======================================================================
# GROUP E -- faithful RS-MCA brute force (support-wise noncommon MCA-bad)
# ======================================================================
def _explained(w, S, k, q, pts):
    """True iff some deg<k poly matches w on every index in S (RS explanation)."""
    m = len(S)
    if m <= k:
        return True                                  # k coeffs fit any k points
    xs = [pts[i] for i in S]
    ys = [w[i] for i in S]
    base = range(k)                                  # interpolate through first k
    for idx in range(k, m):
        atx = xs[idx]
        total = 0
        for j in base:
            num = 1
            den = 1
            xj = xs[j]
            for l in base:
                if l == j:
                    continue
                num = (num * (atx - xs[l])) % q
                den = (den * (xj - xs[l])) % q
            total = (total + ys[j] * num * pow(den, q - 2, q)) % q
        if total % q != ys[idx] % q:
            return False
    return True

def mca_bad_count(u0, u1, q, n, k, a, pts, Gamma, subsets):
    """# distinct slopes g in Gamma that are support-wise MCA-bad at agreement a:
       some S,|S|>=a explains (u0+g u1) but NOT the pair (<=> u1 unexplained on S)."""
    cnt = 0
    for g in Gamma:
        gw = [(u0[i] + g * u1[i]) % q for i in range(n)]
        for S in subsets:
            if _explained(gw, S, k, q, pts) and not _explained(u1, S, k, q, pts):
                cnt += 1
                break
    return cnt

def brute_max(q, n, k, a, G=None, exhaustive=True, samples=0, seed=0):
    pts = list(range(n))
    Gamma = list(range(q if G is None else G))
    subsets = [S for s in range(a, n + 1) for S in combinations(range(n), s)]
    best = 0
    if exhaustive:
        for u0 in product(range(q), repeat=n):
            for u1 in product(range(q), repeat=n):
                b = mca_bad_count(u0, u1, q, n, k, a, pts, Gamma, subsets)
                if b > best:
                    best = b
    else:
        rnd = random.Random(seed)
        for _ in range(samples):
            u0 = tuple(rnd.randrange(q) for _ in range(n))
            u1 = tuple(rnd.randrange(q) for _ in range(n))
            b = mca_bad_count(u0, u1, q, n, k, a, pts, Gamma, subsets)
            if b > best:
                best = b
    return best

# E1 -- DEEP, exhaustive, k=1 constants over F5, n=4, a=3, r=1 (reproduces #524).
#       cor:exact-deep-numerator: B^MCA = min{|Gamma|,n-a+1}=min{5,2}=2=r+1; P=1.
q, n, k, a = 5, 4, 1, 3
be = brute_max(q, n, k, a, exhaustive=True)
p1, u1v, e1 = Pval(n, a, k, n, q, q), Uval(n, a, q), Eval(n, a, q)
check("E1 deep F5,n=4,k=1,a=3: B^MCA=%d = E=%d = r+1 (exhaustive)" % (be, e1), be == e1 == 2)
check("E1b deep pole floor P=%d = 1 (collapsed, <= B^MCA=%d)" % (p1, be), p1 == 1 and p1 <= be)

# E2 -- SHALLOW, exhaustive, k=1 over F11, n=3, a=2: the SB2-invoked window.
#       P=U=3 (realizable & tight), strictly above tangent floor E=2.
q, n, k, a = 11, 3, 1, 2
bs = brute_max(q, n, k, a, exhaustive=True)
pS, uS, eS = Pval(n, a, k, n, q, q), Uval(n, a, q), Eval(n, a, q)
check("E2 shallow F11,n=3,k=1,a=2: B^MCA=%d (exhaustive)" % bs, bs == 3)
check("E2b P=%d <= B^MCA=%d <= U=%d  (pole floor realizable, tight to U)" % (pS, bs, uS),
      pS <= bs <= uS and pS == 3 and uS == 3)
check("E2c B^MCA=%d > tangent floor E=%d  (pole floor strictly tightens the reserve)" % (bs, eS),
      bs > eS and eS == 2)
check("E2d a=2 is shallow (a<a_deep=%d) and in list>=2 band (2a-k<=n)" % a_deep(n, k),
      a < a_deep(n, k) and 2 * a - k <= n)

# E3 -- non-constant row, sampled, k=2 over F7, n=4, a=3: confirm P<=B^MCA<=U.
q, n, k, a = 7, 4, 2, 3
b3 = brute_max(q, n, k, a, exhaustive=False, samples=25000, seed=7)
p3, u3, e3 = Pval(n, a, k, n, q, q), Uval(n, a, q), Eval(n, a, q)
check("E3 k=2 F7,n=4,a=3 sampled: P=%d <= B^MCA(sample)=%d <= U=%d" % (p3, b3, u3),
      p3 <= b3 <= u3)

# ----------------------------------------------------------------------
n_pass = sum(1 for _, c in CHECKS if c)
n_fail = len(CHECKS) - n_pass
print()
print("gated grids: A(containment) deep-subset all n<=219;  "
      "B1 rigidity %d cases;  B2 deep-P %d cases;  D %d cases" %
      (B_star_tested, B_deepP_tested, D_tested))
print("zone census (grid D): P>E useful=%d (all shallow non-deep), P==E=%d, P<E redundant=%d" %
      (zone_useful, zone_eq, zone_trivial))
if n_fail:
    print("RESULT: FAIL (%d/%d checks failed)" % (n_fail, len(CHECKS)))
    sys.exit(1)
print("RESULT: PASS (%d checks)" % len(CHECKS))
sys.exit(0)
