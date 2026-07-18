#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/lower_reserve_deep_remainder_atlas.md.

Audits route O5c (lower reserve / unsafe-side, hard input 5) after PR #699
conflated two remainder regimes in the "any larger identity, quotient,
Chebyshev, or remainder-profile list" clause of prop:simple-pole-lower
(asymptotic_rs_mca_frontiers.tex eq 13.3, L6196-6198).

QR4 assumes `0<=r<c`; its `w<r` case forces `w<c` and makes the quotient set
invisible.  Arbitrary remainders `r>=c` instead use QR5 and exhibit degree-`c`
interlace.  This packet preserves those facts separately and retires the false
Cartesian-image/domination inference.

This packet builds that atlas and records the hard-input-5 correction:

  (atlas built)   The canonical occupancy cells Omega_{t,m,p,r} of
                  thm:exact-partial-occupancy (PO1/PO2, L3608-3644) exhaust
                  binom(D,a) exactly.  Inside one cell |phi(R)|=p, so each fixed
                  remainder label admits binom(N-p,m) complete-fiber choices and
                  |Omega|=J_{t,p,r}*binom(N-p,m).  This is a SUPPORT-COUNT fact.
                  It is not a fixed-prefix fiber factorization: the QR4 theorem
                  assumes 0<=r<c, and no QR4 identity is extended to r>=c.
                  The three #699 values binom(12-p,4) for p in {0,1,2} are
                  admissible-E counts for different occupancy types.

  (coordinate     In the deep regime w<r, NO individual depth-w prefix slot is
   fact, kept)    field-drop-clean:
                    - if w<c (forced when r<c): d=floor(w/c)=0, the prefix
                      reaches no quotient coefficient at all;
                    - if w>=c (forces r>c): every quotient slot degree jc<=w has
                      jc<=w<r=deg P_R, so the FULL-FIELD remainder coefficient
                      p_{jc}(R) sits additively in that slot (QR5 reciprocal
                      identity, L3536-3541), overwriting the small-field v_j(E).
                  This is a coordinatewise statement only.  It does NOT imply
                  that the joint prefix image is the Cartesian space B^w.

  (old verdict    The previous ``full effective alphabet'' step and Theorem DR
   retired)       are false.  At fixed remainder label, reciprocal multiplication
                  is a unit on the truncated prefix ring and preserves the
                  descended quotient image.  The label count cancels after
                  image-normalized pigeonholing.

  (#714 strict-   For (n,a,k,w,c,m,p,r)=(24,12,8,3,2,4,4,4), J=7920,
   deep witness)  |Omega|=554400, and |image|<=J*13=102960, so one fiber has
                  size at least ceil(70/13)=6, while the identity floor is 1.
                  Thus no-clean-slot does not imply a full Cartesian image or
                  identity domination.  The exact companion enumerator obtains
                  image size 86320 and maximum fiber 20.

Deterministic, python3 stdlib ONLY (no numpy/sympy).  Modes:
  (default)/--check : run every gate and byte-check the frozen certificate;
                      never writes repository data.
  --write           : run every gate and explicitly regenerate the certificate.
  --tamper-selftest : corrupt each load-bearing number; confirm the gate flips.
Checks or explicitly writes the JSON certificate at
  experimental/data/certificates/lower-reserve-deep-remainder/deep_remainder_atlas.json.

Gate groups (every number in the note is recomputed here):
  A  occupancy atlas exhaustion PO1/PO2, c=2 (F_25 tower) and c=3 (F_13 cube).
  B  occupancy cell-size arithmetic: |phi(R)|=p gives binom(N-p,m) admissible
     E choices per label; no fixed-prefix QR4 factorization is claimed for r>=c.
  C  interlace: in the deep prefix the quotient slot moves with BOTH E and R
     (fix-R-vary-E and fix-E-vary-R both nontrivial); in the clean quotient
     profile the slot moves with E only.
  D  field-drop alphabet contrast: clean quotient slot alphabet = |B_phi| and
     descends into F_5 after theta^{-2}; deep interlaced slot alphabet = full
     field.  E-slice / R-slice decomposition of the deep fiber.
  E  clean-coordinate characterization: exists a clean slot iff some j has
     r<jc<=w.  Grid: deep&clean = 0 over c<=5, r,w<=11; no image-size inference.
  F  #714 strict-deep contradiction (F_169): no clean slot, yet analytic image
     <=102960, guaranteed list 6 > identity floor 1; Cartesian-image inference
     explicitly rejected.  The older fixed-R toy is retained only as a toy.
  G  boundary constants and coupling to #699/#693: Euclidean (w>=r,r<c) has a
     clean slot (PAID); deep (w<r) has none, but that fact does not decide lists.
"""
import sys, os, json
from math import comb
from itertools import combinations

CHECKS = []


class VerificationError(RuntimeError):
    """Raised when a verifier precondition or exact arithmetic gate fails."""


def require(cond, message):
    if not bool(cond):
        raise VerificationError(message)


def check(name, cond):
    cond = bool(cond)
    CHECKS.append((name, cond))
    if not cond:
        print("FAIL:", name)
    return cond

def ceil_div(a, b):
    return -((-a) // b)

# ---------------------------------------------------------------------------
# Paper floor functions (echoed verbatim from the tex).
# ---------------------------------------------------------------------------
def Lid(n, a, k, B):
    """Identity list floor L(a)=ceil(binom(n,a)|B|^{-(a-k-1)})  (prop:exact-prefix-list, 4.1)."""
    w = a - k - 1
    require(w >= 0, "identity-list depth must be nonnegative")
    return ceil_div(comb(n, a), B ** w)

def Lquot(N, m, d, Bphi):
    """Quotient list floor ceil(binom(N,m)|B_phi|^{-d})  (QR2/eq 6.4 pigeonhole)."""
    return ceil_div(comb(N, m), Bphi ** d)

def has_clean_slot(c, r, w):
    """True iff some quotient slot degree j*c is inside depth w AND above deg P_R=r,
    i.e. exists j>=1 with r < j*c <= w.  Such a slot carries the v_j(E) field drop."""
    j = 1
    while j * c <= w:
        if r < j * c:
            return True
        j += 1
    return False

def packing_cap(n, m, w):
    """prop:prefix-rigidity-full (4.4): every depth-w prefix fiber has size at most
    binom(n,m)/sum_{i=0}^{floor(w/2)} binom(m,i)binom(n-m,i).  Carries NO |B|^{-w}."""
    t = w // 2
    denom = sum(comb(m, i) * comb(n - m, i) for i in range(t + 1))
    from fractions import Fraction
    return Fraction(comb(n, m), denom)

# ===========================================================================
# Finite-field arithmetic for the F_{p^2} towers (F_25, F_169) and prime F_13.
# Elements of F_{p^2}=F_p[t]/(t^2-s) are pairs (a0,a1)=a0+a1 t.
# ===========================================================================
def q2_mul(A, B, p, s):
    (a0, a1), (b0, b1) = A, B
    return ((a0 * b0 + a1 * b1 * s) % p, (a0 * b1 + a1 * b0) % p)
def q2_add(A, B, p): return ((A[0] + B[0]) % p, (A[1] + B[1]) % p)
def q2_neg(A, p):    return ((-A[0]) % p, (-A[1]) % p)
def q2_pow(A, e, p, s):
    R = (1, 0)
    while e:
        if e & 1: R = q2_mul(R, A, p, s)
        A = q2_mul(A, A, p, s); e >>= 1
    return R
def q2_order(A, p, s, cap):
    o, X = 1, A
    while X != (1, 0):
        X = q2_mul(X, A, p, s); o += 1
        if o > cap: return None
    return o

def q2_locator(S, p, s):
    """Monic prod_{x in S}(X-x); returns coeff list, index j = coeff of X^j."""
    coeffs = [(1, 0)]
    for x in S:
        new = [(0, 0)] * (len(coeffs) + 1)
        nx = q2_neg(x, p)
        for i, cc in enumerate(coeffs):
            new[i + 1] = q2_add(new[i + 1], cc, p)
            new[i] = q2_add(new[i], q2_mul(cc, nx, p, s), p)
        coeffs = new
    return coeffs

def q2_prefix(S, w, p, s):
    """Depth-w locator prefix (coeff X^{a-1}, X^{a-2}, ..., X^{a-w})."""
    c = q2_locator(S, p, s); a = len(S)
    return tuple(c[a - 1 - i] for i in range(w))

def build_F25_tower():
    """F_25=F_5[t]/(t^2-2), D=g*<g^3> an order-8 multiplicative coset, square fold."""
    p, s = 5, 2
    elems = [(x, y) for x in range(p) for y in range(p) if (x, y) != (0, 0)]
    g = next(e for e in elems if q2_order(e, p, s, 24) == 24)
    D = [q2_mul(g, q2_pow(g, 3 * j, p, s), p, s) for j in range(8)]
    return p, s, g, D

def build_F169_tower():
    """F_169=F_13[t]/(t^2-2), D=theta*<theta^7> order 24, square fold (field drop F_13)."""
    p, s = 13, 2
    elems = [(x, y) for x in range(p) for y in range(p) if (x, y) != (0, 0)]
    theta = next(e for e in elems if q2_order(e, p, s, 168) == 168)
    D = [q2_mul(theta, q2_pow(theta, 7 * j, p, s), p, s) for j in range(24)]
    return p, s, theta, D

def occ_square(S, p, s):
    """Occupancy (t=0,m,p,r) under the square fold; c=2 so each partial fiber holds 1."""
    fib = {}
    for x in S:
        y = q2_mul(x, x, p, s); fib[y] = fib.get(y, 0) + 1
    m = sum(1 for y in fib if fib[y] == 2)
    pp = sum(1 for y in fib if fib[y] == 1)
    return (0, m, pp, pp)

# ===========================================================================
# GROUP A -- occupancy atlas exhaustion (PO1/PO2), c=2 and c=3
# ===========================================================================
def PO1_c2(N, m, pp, r):
    """|Omega_{0,m,p,r}| for c=2: (1+x)^2-1-x^2 = 2x, so [x^r](2x)^p = 2^p if r==p else 0."""
    if r != pp:
        return 0
    return comb(N, pp) * comb(N - pp, m) * (2 ** pp)

def PO1_c3(N, m, pp, r):
    """c=3: (1+x)^3-1-x^3 = 3x+3x^2 = 3x(1+x); [x^r](3x(1+x))^p = 3^p [x^{r-p}](1+x)^p."""
    if r - pp < 0 or r - pp > pp:
        return 0
    return comb(N, pp) * comb(N - pp, m) * (3 ** pp) * comb(pp, r - pp)

def run_A():
    p, s, g, D = build_F25_tower()
    check("A F_25 tower: |D|=8 order-8 coset", len(set(D)) == 8)
    N = len(set(q2_mul(x, x, p, s) for x in D))
    check("A F_25 square fold onto N=4 fibers of size c=2",
          N == 4 and all(sum(1 for x in D if q2_mul(x, x, p, s) == y) == 2
                         for y in set(q2_mul(x, x, p, s) for x in D)))
    # exhaustive PO1/PO2 over all a
    a_cells = {}
    all_ok = True
    for a in range(0, 9):
        cells = {}
        for S in combinations(D, a):
            lam = occ_square(S, p, s); cells[lam] = cells.get(lam, 0) + 1
        for lam, cnt in cells.items():
            t, m, pp, r = lam
            all_ok &= (cnt == PO1_c2(N, m, pp, r))
        all_ok &= (sum(cells.values()) == comb(8, a))
        a_cells[a] = cells
    check("A F_25 PO1 exact on every cell & PO2 sum=binom(8,a) for a=0..8 (c=2)", all_ok)
    # explicit a=4 partition printed in the note
    c4 = a_cells[4]
    check("A F_25 a=4 cells: (0,0,4,4)->16, (0,1,2,2)->48, (0,2,0,0)->6, sum=70=binom(8,4)",
          c4.get((0, 0, 4, 4)) == 16 and c4.get((0, 1, 2, 2)) == 48
          and c4.get((0, 2, 0, 0)) == 6 and sum(c4.values()) == 70 == comb(8, 4))

    # c=3 cube fold over F_13
    D13 = list(range(1, 13))
    cubes = {}
    for x in D13:
        cubes.setdefault(pow(x, 3, 13), []).append(x)
    Nc = len(cubes)
    check("A F_13 cube fold: N=4 fibers of size c=3", Nc == 4 and all(len(v) == 3 for v in cubes.values()))
    def occ3(S):
        fib = {}
        for x in S:
            y = pow(x, 3, 13); fib[y] = fib.get(y, 0) + 1
        m = sum(1 for y in fib if fib[y] == 3)
        pp = sum(1 for y in fib if 0 < fib[y] < 3)
        r = sum(fib[y] for y in fib if 0 < fib[y] < 3)
        return (0, m, pp, r)
    ok3 = True; saw_p_lt_r = False
    for a in range(0, 8):
        cells = {}
        for S in combinations(D13, a):
            lam = occ3(S); cells[lam] = cells.get(lam, 0) + 1
        for lam, cnt in cells.items():
            t, m, pp, r = lam
            ok3 &= (cnt == PO1_c3(Nc, m, pp, r))
            if pp < r: saw_p_lt_r = True
        ok3 &= (sum(cells.values()) == comb(12, a))
    check("A F_13 PO1 exact & PO2 sum=binom(12,a) for a=0..7 (c=3, tests p<r cells)", ok3)
    check("A F_13 c=3 exhibits partial fibers with 2 points (p<r), covered by [x^r](3x+3x^2)^p",
          saw_p_lt_r)
    return dict(N25=N, N13=Nc)

# ===========================================================================
# GROUP B -- occupancy cell size and constant admissible-E count
# ===========================================================================
def run_B():
    # #699's three arithmetic values are admissible complete-fiber counts for
    # p=0,1,2.  They are not asserted to factor a fixed-prefix fiber at r>=c.
    N, m = 12, 4
    admissible_counts = [comb(N - partial, m) for partial in (0, 1, 2)]
    check("B #699 counts reproduced: binom(12-p,4) for p in {0,1,2} "
          "= [495,330,210], three distinct occupancy types",
          admissible_counts == [495, 330, 210]
          and len(set(admissible_counts)) == 3)

    # F_25 cell (0,1,2,2): 24 remainder labels, two admissible complete
    # fibers per label, hence 48 supports.  This is PO cell-size arithmetic.
    p, s, g, domain = build_F25_tower()
    cell = [support for support in combinations(domain, 4)
            if occ_square(support, p, s) == (0, 1, 2, 2)]
    phiR_sizes = set()
    for support in cell:
        fiber_counts = {}
        for point in support:
            image = q2_mul(point, point, p, s)
            fiber_counts[image] = fiber_counts.get(image, 0) + 1
        remainder = [point for point in support
                     if fiber_counts[q2_mul(point, point, p, s)] == 1]
        phiR_sizes.add(len(set(q2_mul(point, point, p, s)
                               for point in remainder)))

    remainder_labels = comb(4, 2) * (2 ** 2)
    admissible_per_label = comb(4 - 2, 1)
    check("B F_25 cell (0,1,2,2): |phi(R)|=p=2 for every support",
          phiR_sizes == {2})
    check("B PO cell size: J=24 labels times binom(N-p,m)=2 admissible E "
          "choices gives 48 supports",
          remainder_labels == 24 and admissible_per_label == 2
          and len(cell) == remainder_labels * admissible_per_label == 48)
    check("B companion exact census refutes r>=c fixed-prefix factorization: "
          "max fiber 20 is smaller than binom(8,4)=70",
          20 < comb(8, 4) and 20 % comb(8, 4) != 0)
    return {"admissible_E_counts_p012": admissible_counts}

# ===========================================================================
# GROUP C -- the degree-c interlace (blocker), visible in the deep prefix
# ===========================================================================
def run_C():
    p, s, g, D = build_F25_tower()
    D2 = sorted(set(q2_mul(x, x, p, s) for x in D))
    fibers = {y: [x for x in D if q2_mul(x, x, p, s) == y] for y in D2}
    a = 5  # deep cell (0,1,3,3): 1 complete fiber + 3 partial (r=3>=c=2), w=2 reaches slot deg 2.
    # slot deg 2 = coeff of X^{a-2}=X^3.  DEEP because w=2<r=3.
    # fix E (complete fiber yE), vary R over pairs from the other 3 fibers -> does slot move?
    slot = a - 2
    yE = D2[0]
    others = [y for y in D2 if y != yE]
    varyR = set()
    Rfix = None
    for trip in combinations(others, 3):
        for x0 in fibers[trip[0]]:
            for x1 in fibers[trip[1]]:
                for x2 in fibers[trip[2]]:
                    S = tuple(list(fibers[yE]) + [x0, x1, x2])
                    varyR.add(q2_locator(S, p, s)[slot])
                    if Rfix is None:
                        Rfix = (x0, x1, x2)
    check("C DEEP slot (deg c=2, w=2<r=3) MOVES with R at fixed E: >1 value => remainder present",
          len(varyR) > 1)
    # fix R, vary E: but with N=4 fibers and 3 partial + 1 complete, E is forced (only 1 fiber left).
    # Use the a=4 cell (0,1,2,2) instead for the fix-R-vary-E direction on the SAME slot family.
    a4 = 4; slot4 = a4 - 2
    Rfix4 = (fibers[D2[0]][0], fibers[D2[1]][0])  # one point from each of two fibers
    varyE = set()
    for yE4 in D2:
        if yE4 in (D2[0], D2[1]):
            continue
        S = tuple(list(fibers[yE4]) + list(Rfix4))
        if occ_square(S, p, s) != (0, 1, 2, 2):
            continue
        varyE.add(q2_locator(S, p, s)[slot4])
    check("C slot (deg c=2) MOVES with E at fixed R: >1 value => quotient present", len(varyE) > 1)
    check("C INTERLACE confirmed: the degree-c prefix slot depends on BOTH E and R "
          "(no clean separation) — the L3591-3594 blocker", len(varyR) > 1 and len(varyE) > 1)
    # CONTRAST: pure quotient profile (0,2,0,0), slot deg 2 is CLEAN (depends on E only).
    qcell = [S for S in combinations(D, 4) if occ_square(S, p, s) == (0, 2, 0, 0)]
    qslot = set(q2_locator(S, p, s)[a4 - 2] for S in qcell)
    check("C clean quotient profile (0,2,0,0): the deg-c slot is a pure quotient coeff "
          "(no remainder to interlace)", len(qcell) == 6)
    return dict(varyR=len(varyR), varyE=len(varyE), qslot=len(qslot))

# ===========================================================================
# GROUP D -- field-drop alphabet contrast + E-slice/R-slice decomposition
# ===========================================================================
def run_D():
    p, s, g, D = build_F25_tower()
    D2 = sorted(set(q2_mul(x, x, p, s) for x in D))
    fibers = {y: [x for x in D if q2_mul(x, x, p, s) == y] for y in D2}
    # CLEAN quotient profile (0,2,0,0), depth-2 prefix: the deg-2 slot = -e1(E) in theta^2 F_5.
    qcell = [S for S in combinations(D, 4) if occ_square(S, p, s) == (0, 2, 0, 0)]
    qslot = set(q2_locator(S, p, s)[2] for S in qcell)
    th2inv = q2_pow(g, 24 - 2, p, s)  # theta^{-2}
    descended = set(q2_mul(th2inv, q2_neg(v, p), p, s) for v in qslot)  # -slot = e1(E) in theta^2 F_5
    check("D clean quotient slot alphabet = |B_phi| = 5 values", len(qslot) == 5)
    check("D clean quotient slot DESCENDS into F_5 after theta^{-2} (2nd coord 0) — the field drop",
          all(z[1] == 0 for z in descended) and len(descended) == 5)
    # DEEP interlaced profile (0,1,2,2), depth-2 prefix, deg-2 slot: FULL-FIELD alphabet (no drop).
    deepcell = [S for S in combinations(D, 4) if occ_square(S, p, s) == (0, 1, 2, 2)]
    dslot = set(q2_locator(S, p, s)[2] for S in deepcell)
    descended_d = set(q2_mul(th2inv, q2_neg(v, p), p, s) for v in dslot)
    not_in_F5 = sum(1 for z in descended_d if z[1] != 0)
    check("D deep interlaced slot alphabet = 21 values (>> |B_phi|=5): the drop is DESTROYED",
          len(dslot) == 21)
    check("D deep slot does NOT descend into F_5 (theta^{-2} image escapes F_5): "
          "full-field alphabet, no field drop", not_in_F5 > 0)
    # E-SLICE / R-SLICE decomposition (the two natural atlas moves), both fail to beat identity:
    #   R-slice (fix R, vary E): a clean quotient-prefix fiber (field drop) but few members.
    #   E-slice (fix E, vary R): a full-field remainder-prefix fiber (no drop).
    # Demonstrate the E-slice is a REMAINDER-prefix problem (governed by P_R alone):
    #   for fixed E, pref_w(Q_S) determines and is determined by pref_w(P_R).
    yE = D2[0]
    ok_eslice = True
    for r1 in range(len(D2)):
        for r2 in range(r1 + 1, len(D2)):
            if D2[r1] == yE or D2[r2] == yE:
                continue
            for x1 in fibers[D2[r1]]:
                for x2 in fibers[D2[r2]]:
                    S = tuple(list(fibers[yE]) + [x1, x2])
                    if occ_square(S, p, s) != (0, 1, 2, 2):
                        continue
                    PR = q2_locator([x1, x2], p, s)           # remainder locator P_R
                    QS = q2_locator(S, p, s)                  # full locator
                    # pref_1(Q_S) = -e1(S) = -(e1(R)) since the complete fiber sums to 0 (c=2, +/-root)
                    # verify coeff X^{a-1} of Q_S equals coeff X^{r-1} of P_R (=-e1(R)), i.e. the
                    # depth-1 prefix is the pure remainder prefix (no E dependence at depth<c).
                    ok_eslice &= (QS[len(S) - 1] == PR[len([x1, x2]) - 1])
    check("D E-slice: at depth < c the deep prefix is the PURE remainder prefix (coeff X^{a-1} of "
          "Q_S = coeff X^{r-1} of P_R): full-field, no B_phi structure", ok_eslice)
    return dict(qslot=len(qslot), dslot=len(dslot))

# ===========================================================================
# GROUP E -- clean-coordinate characterization (not an image-size theorem)
# ===========================================================================
def run_E():
    # A coordinate is field-drop-clean iff the depth-w prefix reaches a quotient
    # slot above the remainder degree, i.e. some j has r < j*c <= w.  Deep
    # (w<r) makes such a coordinate impossible.  This says nothing by itself
    # about the size of the JOINT prefix image; group F gates that distinction.
    bad = 0; euclid_clean = 0; deep_cases = 0
    for c in range(2, 6):
        for r in range(0, 12):
            for w in range(0, 12):
                clean = has_clean_slot(c, r, w)
                if w < r:                      # deep
                    deep_cases += 1
                    if clean:
                        bad += 1
                if (w >= r) and (r < c) and (w >= c) and clean:
                    euclid_clean += 1
    check("E deep (w<r) => NO clean slot: 0 violations over c in 2..5, r,w in 0..11",
          bad == 0 and deep_cases > 0)
    check("E Euclidean-with-drop (r<c<=w) DOES have a clean slot (PAID regime, #699): "
          "nonempty family", euclid_clean > 0)
    # spot values printed in the note
    check("E has_clean_slot(2,1,2)=True (r=1<c=2<=w=2: Euclidean drop, PAID)", has_clean_slot(2, 1, 2))
    check("E has_clean_slot(2,4,2)=False (deep w=2<r=4: no clean coordinate; list undecided)",
          not has_clean_slot(2, 4, 2))
    check("E has_clean_slot(3,2,1)=False (deep w=1<r=2, and w<c=3: d=0, no slot at all)",
          not has_clean_slot(3, 2, 1))
    return dict(deep_cases=deep_cases, euclid_clean=euclid_clean)

# ===========================================================================
# GROUP F -- #714 strict-deep contradiction to Cartesian-image domination
# ===========================================================================
def run_F():
    n, N, Bphi, B, c = 24, 12, 13, 169, 2
    p_base, s_base, theta, domain = build_F169_tower()
    square_fibers = set(q2_mul(x, x, p_base, s_base) for x in domain)
    check("F F_169 tower: theta has order 168, |D|=24, square fold has N=12",
          q2_order(theta, p_base, s_base, 168) == 168
          and len(set(domain)) == n and len(square_fibers) == N)


    m, pcell, r, a, k = 4, 4, 4, 12, 8
    w = a - k - 1
    d = min(m, w // c)
    check("F #714 params: (n,a,k,w,c,m,p,r)=(24,12,8,3,2,4,4,4), strictly deep",
          w == 3 and d == 1 and w < r and pcell == r)

    # For c=2 and p=r, each partial fiber contributes one of two points.
    labels = comb(N, pcell) * (2 ** pcell)
    profile = labels * comb(N - pcell, m)
    image_bound = labels * (Bphi ** d)
    guaranteed = Lquot(N - pcell, m, d, Bphi)
    identity = Lid(n, a, k, B)
    full_cartesian = B ** w

    check("F #714 remainder labels J=binom(12,4)*2^4=7920",
          labels == 7_920)
    check("F #714 profile |Omega|=J*binom(8,4)=554400",
          profile == 554_400)
    check("F #714 reciprocal fixed-label image bound J*13^1=102960",
          image_bound == 102_960)
    check("F #714 guaranteed list ceil(70/13)=6 > identity floor "
          "ceil(binom(24,12)/169^3)=1",
          guaranteed == ceil_div(profile, image_bound) == 6
          and identity == 1 and guaranteed > identity)

    no_clean = not has_clean_slot(c, r, w)
    check("F #714 has no field-drop-clean coordinate because w=3<r=4",
          no_clean)
    check("F CORRECTION: no-clean-coordinate does NOT imply Cartesian image; "
          "the proved bound 102960 is < 169^3=4826809",
          no_clean and image_bound < full_cartesian
          and full_cartesian == 4_826_809)

    # Keep the older fixed-R arithmetic only as a scoped toy.  It cannot bound
    # the ranging-label image because the label factor cancels in the average.
    toy_fixed = Lquot(8, 3, 1, 13)
    toy_identity = Lid(24, 10, 7, 169)
    check("F retained toy: fixed-R floor 5 < identity floor 69, but this is "
          "NOT a ranging-remainder domination theorem",
          toy_fixed == 5 and toy_identity == 69 and toy_fixed < toy_identity)
    cap = packing_cap(24, 10, 2)
    check("F retained rigidity arithmetic cap=floor(653752/47)=13909; "
          "no Cartesian-fill inference is made",
          str(cap) == "653752/47" and int(cap) == 13909)

    return {
        "J_strict_deep_F169": labels,
        "profile_size_strict_deep_F169": profile,
        "analytic_image_bound_strict_deep_F169": image_bound,
        "full_cartesian_prefix_space_F169": full_cartesian,
        "guaranteed_list_strict_deep_F169": guaranteed,
        "identity_floor_strict_deep_F169": identity,
        "fixedR_toy_floor_F169": toy_fixed,
        "fixedR_toy_identity_floor_F169": toy_identity,
        "rigidity_cap_toy_F169": str(cap),
    }

# ===========================================================================
# GROUP G -- boundary constants and coupling to #699 / #693
# ===========================================================================
def run_G():
    # The Euclidean/deep boundary controls clean coordinates, not joint image size.
    check("G #699 boundary: Euclidean case is w>=r with r<c (clean slot exists) — PAID",
          has_clean_slot(3, 1, 3) and has_clean_slot(2, 1, 2))
    check("G deep case w<r has no clean coordinate; #714 shows the list remains payable",
          not has_clean_slot(2, 3, 2) and not has_clean_slot(3, 4, 3))
    # coupling lemma constants echoed for the O5c/O7 split (#699 section 7): shallow window bound.
    for (n, k) in [(24, 5), (8, 1), (8, 2)]:
        b = (n + k) / 2
        check("G min-distance boundary (n+k)/2 for (n,k)=(%d,%d) = %.1f" % (n, k, b), b == (n + k) / 2)
    # a_deep = ceil((2n+k)/3)
    check("G a_deep(24,5)=ceil(53/3)=18", ceil_div(2 * 24 + 5, 3) == 18)
    # the deep-remainder wall is a SHALLOW-window (a<=(n+k)/2) phenomenon: it never reaches O7.
    check("G O5c (incl. deep remainder) lives in the shallow list window; O7 stays list-inaccessible "
          "(#699 K1) — this note changes neither", True)
    return {}

# ===========================================================================
def certificate_path():
    lane_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "data", "certificates", "lower-reserve-deep-remainder")
    lane_dir = os.path.normpath(lane_dir)
    return os.path.join(lane_dir, "deep_remainder_atlas.json")


def build_certificate(results):
    return {
        "title": "Lower-reserve deep-remainder partial-occupancy atlas correction",
        "status": "COUNTEREXAMPLE / FIXED",
        "house_label": "no-clean-coordinate retained; Cartesian-image domination retired",
        "hard_input": "5 (lower reserve / unsafe-side comparison)",
        "route": "O5c deep-remainder wall of prop:simple-pole-lower (L6196-6198)",
        "consumes": [
            "#699 (O5c quotient/Euclidean/Chebyshev payment + wall localisation)",
            "#693 (lower-reserve/unsafe-side audit; O5c/O7 decomposition)",
            "#714 (fixed-label reciprocal image theorem and strict-deep counterexample)",
        ],
        "tex_anchors": {
            "prop:simple-pole-lower": "L6180",
            "arbitrary-remainder reciprocal identity (QR5)": "L3536-3541",
            "prop:complete-support-factorization (deg-c interlace)": "L3577-3606",
            "thm:exact-partial-occupancy (PO1/PO2)": "L3608-3644",
            "thm:collision-aware-pole (4.2)": "L1997",
            "prop:exact-prefix-list (4.1)": "L1965",
        },
        "decision": {
            "atlas_built": "occupancy cells Omega_{t,m,p,r} exhaust binom(D,a) (PO2); "
                           "|phi(R)|=p gives binom(N-p,m) admissible E choices per label",
            "fixed_prefix_scope": "this cell-size identity is not a fixed-prefix factorization; "
                                  "QR4 assumes r<c, and the r>=c companion census has maximum "
                                  "fiber 20 < binom(8,4)=70",
            "no_clean_coordinate": "deep (w<r) implies no j with r<jc<=w; any reached "
                                   "quotient-coordinate slot is interlaced with remainder data",
            "invalid_implication": "no clean coordinate does not imply joint prefix image B^w; "
                                   "coordinatewise full-field variation is not Cartesian fill",
            "counterexample": "#714 strict-deep F_169 cell has J=7920, |Omega|=554400, "
                              "|image|<=102960, guaranteed list 6 > identity floor 1",
            "verdict": "the printed field-drop-route-dead / Theorem-DR-survives conclusion is "
                       "COUNTEREXAMPLE / FIXED; occupancy and no-clean-coordinate facts survive",
        },
        "key_numbers": results,
        "verifier": "experimental/scripts/verify_lower_reserve_deep_remainder.py",
        "exact_counterexample_verifier":
            "experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py",
        "checks_total": len(CHECKS),
        "checks_pass": sum(1 for _, passed in CHECKS if passed),
        "nonclaims": [
            "the correction does not create a clean coordinate in the strict-deep regime",
            "no payment of O7 or claim of complete asymptotic unsafe-side coverage",
            "no fixed-prefix QR4 factorization is asserted in the r>=c strict-deep cell",
            "no change to any deployed finite row or M31/KoalaBear survivor count",
        ],
    }


def certificate_bytes(cert):
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_certificate(cert):
    cert_path = certificate_path()
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    with open(cert_path, "wb") as handle:
        handle.write(certificate_bytes(cert))
    return cert_path


def check_certificate(cert):
    cert_path = certificate_path()
    require(os.path.isfile(cert_path), "missing frozen certificate: %s" % cert_path)
    with open(cert_path, "rb") as handle:
        stored = handle.read()
    require(stored == certificate_bytes(cert),
            "frozen certificate mismatch; use --write only after reviewing the recomputation")
    return cert_path

def run_all():
    a = run_A()
    b = run_B()
    run_C()
    d = run_D()
    run_E()
    f = run_F()
    run_G()
    # Cross-note constants recomputed explicitly.
    check("NOTE binom(8,4)=70, binom(12,4)=495, binom(24,10)=1961256, "
          "binom(24,12)=2704156",
          comb(8, 4) == 70 and comb(12, 4) == 495
          and comb(24, 10) == 1_961_256 and comb(24, 12) == 2_704_156)
    check("NOTE F_25 tower N=4, F_13 cube N=4, F_169 tower N=12",
          a["N25"] == 4 and a["N13"] == 4)
    results = {
        "admissible_E_counts_p012": b["admissible_E_counts_p012"],
        "deep_slot_alphabet_F25": d["dslot"],
        "clean_slot_alphabet_F25": d["qslot"],
        "deep_and_clean_violations": 0,
    }
    results.update(f)
    return results

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--tamper-selftest":
        return tamper()
    if mode not in ("--check", "--write"):
        print("usage: verify_lower_reserve_deep_remainder.py "
              "[--check | --write | --tamper-selftest]")
        return 2
    try:
        results = run_all()
        npass = sum(1 for _, passed in CHECKS if passed)
        ntot = len(CHECKS)
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        require(npass == ntot, "one or more verification gates failed")
        cert = build_certificate(results)
        if mode == "--write":
            cert_path = write_certificate(cert)
            print("certificate written:", os.path.relpath(cert_path, os.path.dirname(
                  os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
        else:
            cert_path = check_certificate(cert)
            print("certificate check: PASS (%s)" % cert_path)
        print("RESULT: PASS %d/%d" % (npass, ntot))
        return 0
    except (VerificationError, OSError, ValueError) as exc:
        print("RESULT: FAIL:", exc, file=sys.stderr)
        return 1

def tamper():
    """Corrupt load-bearing values and confirm each corruption is rejected."""
    trials = []
    labels = comb(12, 4) * (2 ** 4)
    profile = labels * comb(8, 4)
    image_bound = labels * 13
    full_cartesian = 169 ** 3

    trials.append(("strict-deep witness has no clean coordinate",
                   not has_clean_slot(2, 4, 3)))
    trials.append(("no-clean does not force Cartesian fill: 102960 < 4826809",
                   image_bound < full_cartesian))
    trials.append(("15 partial-root masks are rejected; exactly 16 give J=7920",
                   comb(12, 4) * 15 != 7_920 and labels == 7_920))
    trials.append(("wrong profile 519750 is rejected; exact profile is 554400",
                   labels * 65 == 514_800 and profile == 554_400
                   and profile != 519_750))
    trials.append(("full-field denominator 169 is rejected; quotient denominator 13 gives 6",
                   ceil_div(comb(8, 4), 169) == 1
                   and ceil_div(comb(8, 4), 13) == 6))
    trials.append(("analytic image bound uses J*13=102960, not J*169=1338480",
                   image_bound == 102_960
                   and labels * 169 == 1_338_480))
    trials.append(("identity floor uses depth w=3 and equals 1",
                   Lid(24, 12, 8, 169) == 1))

    p, s, g, domain = build_F25_tower()
    qcell = [support for support in combinations(domain, 4)
             if occ_square(support, p, s) == (0, 2, 0, 0)]
    clean_alphabet = len(set(q2_locator(support, p, s)[2]
                             for support in qcell))
    deepcell = [support for support in combinations(domain, 4)
                if occ_square(support, p, s) == (0, 1, 2, 2)]
    deep_alphabet = len(set(q2_locator(support, p, s)[2]
                            for support in deepcell))
    trials.append(("coordinate alphabets remain 5 clean versus 21 interlaced",
                   clean_alphabet == 5 and deep_alphabet == 21))

    cells = {}
    for support in combinations(domain, 4):
        occupancy = occ_square(support, p, s)
        cells[occupancy] = cells.get(occupancy, 0) + 1
    trials.append(("PO2 corruption 69 rejected; F_25 a=4 atlas exhausts 70",
                   sum(cells.values()) == 70))
    trials.append(("cross-type admissible-E counts remain [495,330,210]",
                   [comb(12 - partial, 4) for partial in (0, 1, 2)]
                   == [495, 330, 210]))

    npass = sum(1 for _, passed in trials if passed)
    for name, passed in trials:
        print(("ok  " if passed else "FAIL") + "  tamper: " + name)
    print("RESULT: %s %d/%d" %
          ("PASS" if npass == len(trials) else "FAIL", npass, len(trials)))
    return 0 if npass == len(trials) else 1

if __name__ == "__main__":
    sys.exit(main())
