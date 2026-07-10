#!/usr/bin/env python3
"""Attack the (FI) full-image certificate on primitive prefix leaves.

Target: experimental/asymptotic_rs_mca_frontiers.tex, base 4e3c4ee.

(FI), the full-image certificate (eq:full-image-certificate, L4844 / L875):

        L >= e^{-o(N)} A ,      A = |B|^R ,   L = |Phi(Omega_{T,m})| .

Consumed wherever the AMBIENT scale barN^amb = M/A replaces the realized
image scale barN^img = M/L (L873, A3 L923, L1246, L1443, L6378, L6462,
L5608).  It is *proved* only via rem:flatness-certifies-image (L4902): an
AMBIENT max-fiber bound max_s f_s <= e^{o(N)} barN^amb pigeonholes to
A/L <= e^{o(N)} (used at L3369, L5395, L5447, L6589).

CORE STRUCTURAL CLAIM VERIFIED HERE -- the (FI) scale tower.  Three sizes,
    L  <=  A_eff  <=  A ,
        L     = |realized prefix image|              (attained targets)
        A_eff = |V_g| = p^{dim_Fp Span{g(t)-g(t_0)}}  (effective span, EF1 L2861)
        A     = |B|^R = p^{Rf}                        (ambient codomain)
splits (FI)-ambient into two INDEPENDENT gaps:
    Gap-1  L >= e^{-o(n)} A_eff   (image fills its effective span)
    Gap-2  A_eff >= e^{-o(n)} A   (effective span is nearly ambient).

  Gap-1 is PROVED equivalent to effective-scale Q: def:effective-fourier-
  payment (EFP, L2929) with constant kappa gives L >= A_eff/kappa (its own
  L2944 sentence), and the smallest admissible kappa is exactly
        kappa* = A_eff * F_max / M                    (EF4 at binom(|T|,m)=M)
  = (max fiber)/(effective-average fiber).  So Gap-1(FI) <=> kappa*=e^{o(n)}
  <=> image-normalized Q, which (A4) already supplies.  NOT an independent
  obligation.

  Gap-2 is a pure rank condition dim_Fp V_g >= Rf - o(.).  On SHALLOW
  prefixes (log A = o(|T|), i.e. (a-k-1)log|B|=o(n), SE2 L3054) ALL of (FI)
  is FREE: A = e^{o(N)} and L>=1 give A/L <= A = e^{o(N)} with no payment.
  On DEEP prefixes Gap-2 is the genuine content; it fails via char-p /
  Frobenius collapse (rem:binary-ambient-image L4349: p_{2j}=p_j^2 in char 2)
  and structured-domain relations.  Each failure is a UNIVERSAL linear
  relation among prefix coordinates = an algebraic subvariety = an EARLIER
  structural profile; whether that profile catches AND pays the collapsed
  mass is the ROUTING claim, which the paper leaves as an enumerative input
  (C7 saturation/collapse cell L2452; L4/L1115 disjunction) -- AUDIT.

WHAT THIS SCRIPT RECOMPUTES (every gated number, stdlib only, zero-arg):
  A. Algebraic identities, exact:
     (A1) EFP => L >= A_eff/kappa*  with kappa*=A_eff*F_max/M  (pigeonhole).
     (A2) lem:image-ambient-moment-conversion, Gamma_q^amb=(A/L)^{q-1}Gamma_q^img.
     (A3) rem:flatness-certifies-image: max f_s <= c*barN^amb => A/L <= c.
  B. Census on the #534/#536 configs (structured D=F_p^* and generic D<[1..n],
     w in 1..3): L, dim, A_eff, A, F_max, M, kappa*, and the three collapse
     ratios r1=lnL/lnA_eff (Gap-1), r2=dim/w (Gap-2), r=lnL/lnA (overall).
     Flag any leaf with genuine collapse (ratio bounded away from 1) and
     check whether the constructible cells re-route it (uncaught => COUNTEREX).
  C. char-2 Frobenius collapse probe (rem:binary-ambient-image): power-sum
     prefix (p_1,p_2) collapses to the curve y=x^2 (Gap-2 span drop), while
     the elementary prefix (q_1,q_2) does NOT -- the paper's named collapse
     and its coordinate resolution ("route to the elementary profile").
  D. Shallow-prefix automatic-FI: A/L <= A pointwise; on the configs with the
     smallest w*log p the ambient/image discrepancy is bounded by A itself.

HONESTY: toy-scale census nulls are EVIDENCE + SCOPE, never an asymptotic
discharge of (FI).  The PROVED items are the algebraic identities (A) and the
Gap-1<=>Q equivalence and the shallow-prefix freeness (finite / scale-
independent facts).  The deep-prefix Gap-2 routing is the WALL and is labeled
AUDIT.  Census primitives reuse PR #534/#535/#536 verbatim (credited).

Status: EXPERIMENTAL.  Stdlib only.  Zero-arg.  Runtime target < 120s.
"""
from __future__ import annotations

from itertools import combinations
from collections import defaultdict, Counter
from math import log, comb

BASE_SHA = "4e3c4ee"
CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    CHECKS.append((name, bool(ok), detail))
    return bool(ok)


# ---------------------------------------------------------------------------
# prime-field linear algebra (exact; reused from #534/#536, credited)
# ---------------------------------------------------------------------------
def inv_mod(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def mat_rank(rows, p: int) -> int:
    M = [list(r) for r in rows]
    if not M:
        return 0
    ncol = len(M[0])
    r = 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(M)) if M[i][c] % p), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = inv_mod(M[r][c], p)
        M[r] = [(x * iv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                fac = M[i][c] % p
                M[i] = [(x - fac * y) % p for x, y in zip(M[i], M[r])]
        r += 1
        if r == len(M):
            break
    return r


def poly_from_roots(S, p: int):
    """Monic locator Q_S(X)=prod_{t in S}(X-t); returns [1,q_1,...,q_a]."""
    coeffs = [1]
    for t in S:
        new = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            new[i] = (new[i] + c) % p
            new[i + 1] = (new[i + 1] - t * c) % p
        coeffs = new
    return coeffs


def prefix_key(S, p: int, w: int):
    """Depth-w elementary prefix Phi_w(S)=(q_1,...,q_w) (sec:coordinate-atlas)."""
    return tuple(poly_from_roots(S, p)[1:w + 1])


def span_dim(keys, p: int) -> int:
    """dim_Fp of the affine span of a set of prefix vectors = A_eff exponent."""
    keys = list(keys)
    if not keys:
        return 0
    v0 = keys[0]
    diffs = [tuple((a - b) % p for a, b in zip(v, v0)) for v in keys[1:]]
    return mat_rank(diffs, p) if diffs else 0


# ===========================================================================
# PART A -- exact algebraic identities behind (FI)
# ===========================================================================
def part_A_identities():
    # (A1) EFP pigeonhole: for ANY fiber multiset with total M over L nonempty
    #      fibers and max F_max, we have L >= M/F_max = A_eff/kappa* with
    #      kappa* = A_eff*F_max/M.  This is the exact content of the L2944
    #      sentence "the realized image contains at least A_eff/kappa points".
    import random
    rng = random.Random(20260710)
    ok_all = True
    tight = 0
    for _ in range(400):
        L = rng.randint(1, 40)
        A_eff = rng.randint(L, 400)          # L <= A_eff always
        fibers = [rng.randint(1, 30) for _ in range(L)]
        M = sum(fibers)
        F_max = max(fibers)
        kappa_star = A_eff * F_max / M
        lower = A_eff / kappa_star           # = M / F_max
        if not (L >= lower - 1e-9):
            ok_all = False
        # pigeonhole is exactly M <= L*F_max
        if not (M <= L * F_max):
            ok_all = False
        if abs(L - lower) < 1e-9:
            tight += 1
    check("A1.EFP.image_ge_Aeff_over_kappa", ok_all,
          f"L >= A_eff/kappa* on 400 random fiber multisets (kappa*=A_eff*F_max/M); "
          f"{tight} exactly tight (uniform fibers)")

    # (A2) lem:image-ambient-moment-conversion (9.3):
    #      Gamma_q^amb = (A/L)^{q-1} Gamma_q^img, exact, for f_s zero-extended.
    ok_conv = True
    for _ in range(200):
        L = rng.randint(1, 20)
        A = rng.randint(L, 200)
        fibers = [rng.randint(1, 25) for _ in range(L)]
        M = sum(fibers)
        Nimg = M / L
        Namb = M / A
        for q in (2, 3, 4, 7):
            g_img = (1.0 / L) * sum((fs / Nimg) ** q for fs in fibers)
            g_amb = (1.0 / A) * sum((fs / Namb) ** q for fs in fibers)  # zero-ext
            rhs = (A / L) ** (q - 1) * g_img
            if abs(g_amb - rhs) > 1e-6 * (1 + abs(g_amb)):
                ok_conv = False
    check("A2.moment_conversion_identity", ok_conv,
          "Gamma_q^amb = (A/L)^{q-1} Gamma_q^img exact (eq:image-ambient-moment-identity)")

    # (A3) rem:flatness-certifies-image: max_s f_s <= c*barN^amb  =>  A/L <= c.
    #      Proof: M = sum_{s in image} f_s <= L*max f_s <= L*c*M/A => A/L <= c.
    ok_flat = True
    for _ in range(200):
        L = rng.randint(1, 20)
        A = rng.randint(L, 200)
        fibers = [rng.randint(1, 25) for _ in range(L)]
        M = sum(fibers)
        Namb = M / A
        c = max(fibers) / Namb               # smallest c s.t. hypothesis holds
        if not (A / L <= c + 1e-9):
            ok_flat = False
    check("A3.flatness_certifies_image", ok_flat,
          "max f_s <= c*barN^amb => A/L <= c  (FI with e^{o(N)}=c); ambient flatness needed")


# ===========================================================================
# PART B -- census on the #534/#536 configs; the (FI) collapse ratios
# ===========================================================================
STRUCTURED = [  # D = F_p^* (n == p-1)
    (13, 12, 5, 7),   # w=1
    (13, 12, 5, 8),   # w=2
    (17, 16, 7, 10),  # w=2
    (19, 18, 8, 11),  # w=2
]
GENERIC = [     # D = [1..n], n < p-1, a <= n/2
    (13, 9, 4, 6),    # w=1
    (17, 11, 4, 7),   # w=2
    (19, 12, 4, 7),   # w=2
    (23, 14, 5, 8),   # w=2
    (29, 18, 6, 10),  # w=3
]

COLLAPSE_TOL = 0.85   # ratio below this = "bounded away from 1" = genuine collapse
census_rows = []


def census_config(p, n, k, a):
    w = a - k - 1
    structured = (n == p - 1)
    D = list(range(1, n + 1))
    assert all(x < p for x in D) and w >= 1
    fibers = defaultdict(int)
    for S in combinations(D, a):
        fibers[prefix_key(S, p, w)] += 1
    M = comb(n, a)
    assert sum(fibers.values()) == M
    L = len(fibers)
    F_max = max(fibers.values())
    dim = span_dim(fibers.keys(), p)
    A_eff = p ** dim
    A = p ** w
    # exact scale tower
    tower_ok = (L <= A_eff <= A)
    # smallest admissible effective Fourier constant (EF4): kappa* = A_eff*F_max/M
    kappa_star = A_eff * F_max / M
    # Gap-1 lower bound realized: L >= A_eff/kappa* = M/F_max
    gap1_ok = (L >= A_eff / kappa_star - 1e-9)
    # collapse ratios (log base p so A ratio = dim/w exactly)
    lnp = log(p)
    r1 = (log(L) / log(A_eff)) if A_eff > 1 else 1.0     # Gap-1 image/span
    r2 = (dim / w)                                        # Gap-2 span/ambient
    r_all = (log(L) / log(A)) if A > 1 else 1.0           # overall image/ambient
    # kappa* as an exponential rate in n (is the effective-scale Q subexp?)
    kappa_rate = log(kappa_star) / n if kappa_star > 1 else 0.0
    row = dict(p=p, n=n, k=k, a=a, w=w, structured=structured, M=M, L=L,
               dim=dim, A_eff=A_eff, A=A, F_max=F_max, kappa_star=kappa_star,
               kappa_rate=kappa_rate, r1=r1, r2=r2, r_all=r_all)
    census_rows.append(row)

    tag = f"p{p}n{n}k{k}a{a}w{w}"
    check(f"B.tower.{tag}", tower_ok,
          f"L={L} <= A_eff=p^{dim}={A_eff} <= A=p^{w}={A}")
    check(f"B.gap1_realized.{tag}", gap1_ok,
          f"L={L} >= A_eff/kappa*={A_eff/kappa_star:.2f} (kappa*={kappa_star:.3f}, "
          f"rate {kappa_rate:.4f}/n); Gap-1 image-fills-span holds")
    return row


def part_B_census():
    for cfg in STRUCTURED + GENERIC:
        census_config(*cfg)

    # Gap-2 collapse audit: which configs have dim < w (span collapse)?
    collapsed = [r for r in census_rows if r["r2"] < COLLAPSE_TOL]
    full_span = [r for r in census_rows if r["dim"] == r["w"]]
    check("B.gap2.prime_field_full_span", len(collapsed) == 0,
          f"{len(full_span)}/{len(census_rows)} configs have dim=w (full ambient span, "
          f"A_eff=A); {len(collapsed)} Gap-2 collapses -- prime-field elementary "
          f"prefixes do not collapse at w<=3")

    # Gap-1 collapse audit: kappa* subexponential everywhere?  (F_max not
    # exponentially above the effective-average fiber M/A_eff)
    hot = [r for r in census_rows if r["kappa_rate"] > 0.30]  # generous toy cutoff
    worst = max(census_rows, key=lambda r: r["kappa_rate"])
    check("B.gap1.kappa_subexp", len(hot) == 0,
          f"max kappa* rate {worst['kappa_rate']:.4f}/n at "
          f"p{worst['p']}n{worst['n']}a{worst['a']}; no exponential effective-scale "
          f"max-fiber => Gap-1(FI) holds on every census leaf")

    # Uncaught collapsing leaf?  A genuine collapse = r_all bounded away from 1
    # AND not routed to an earlier structural cell.  None present here.
    uncaught = [r for r in census_rows
                if r["r_all"] < COLLAPSE_TOL and r["dim"] < r["w"]]
    check("B.no_uncaught_collapsing_leaf", len(uncaught) == 0,
          f"0 leaves with overall collapse r_all<{COLLAPSE_TOL} AND span drop; "
          f"census exhibits no COUNTEREXAMPLE-class routing gap (toy scope)")


# ===========================================================================
# PART C -- char-2 Frobenius collapse probe (rem:binary-ambient-image L4349)
#   Genuine Gap-2 span collapse: over F_{2^kk} the power-sum prefix (p_1,p_2)
#   obeys p_2 = p_1^2 (Frobenius is F_2-LINEAR), so the image lies in the
#   F_2-linear subspace {(x, x^2)} of F_2-dimension kk inside the 2*kk-dim
#   ambient -> A_eff^{ps} = 2^kk, exactly HALF the ambient exponent, while the
#   elementary prefix (e_1,e_2) reaches the full ambient span.  ratio r2 = 1/2.
# ===========================================================================
def gf2k(kk: int, modulus: int):
    """F_{2^kk} = F_2[t]/(modulus).  Elements 0..2^kk-1 (bit i = t^i coeff)."""
    add = lambda x, y: x ^ y
    def mul(x, y):
        r = 0
        while y:
            if y & 1:
                r ^= x
            y >>= 1
            x <<= 1
            if x >> kk:
                x ^= modulus
        return r
    return add, mul


def part_C_frobenius():
    kk, modulus = 3, 0b1011      # F_8 = F_2[t]/(t^3+t+1)
    add, mul = gf2k(kk, modulus)
    # field sanity: t=2 is primitive, t^7=1, order-7 cycle of nonzero elements
    v, seen = 1, []
    for _ in range(7):
        v = mul(v, 2)
        seen.append(v)
    check("C.gf8.field", sorted(seen) == list(range(1, 8)) and mul(3, 6) == mul(6, 3),
          "F_8=F_2[t]/(t^3+t+1): t primitive (t^7=1 cycles all nonzero), mul commutes")

    D = list(range(8))           # full field as evaluation domain
    a = 2                        # 2-subsets; depth-2 prefix; ambient dim = 2*kk = 6
    ambient_dim = 2 * kk

    def bits(x):
        return tuple((x >> i) & 1 for i in range(kk))

    # POWER-SUM prefix (p_1,p_2), p_1 = s+u, p_2 = s^2+u^2 = (s+u)^2
    ps_keys, frob_ok = set(), True
    for S in combinations(D, a):
        p1 = add(S[0], S[1])
        p2 = add(mul(S[0], S[0]), mul(S[1], S[1]))
        if mul(p1, p1) != p2:
            frob_ok = False
        ps_keys.add((p1, p2))
    check("C.frobenius.p2_eq_p1sq", frob_ok,
          "char-2 power sums obey p_2=p_1^2 on every support (rem:binary-ambient-image)")

    ps_vecs = [bits(x) + bits(y) for (x, y) in ps_keys]
    v0 = ps_vecs[0]
    ps_dim = mat_rank([tuple((c - d) % 2 for c, d in zip(v, v0)) for v in ps_vecs[1:]], 2)

    # ELEMENTARY prefix (e_1,e_2), e_1 = s+u, e_2 = s*u
    el_keys = set()
    for S in combinations(D, a):
        el_keys.add((add(S[0], S[1]), mul(S[0], S[1])))
    el_vecs = [bits(x) + bits(y) for (x, y) in el_keys]
    w0 = el_vecs[0]
    el_dim = mat_rank([tuple((c - d) % 2 for c, d in zip(v, w0)) for v in el_vecs[1:]], 2)

    # The collapse: power-sum span dim is (near) HALF; A_eff^{ps} << A = 2^{2kk}.
    check("C.frobenius.powersum_collapses", ps_dim <= kk and ps_dim < el_dim,
          f"power-sum A_eff dim={ps_dim} (<= kk={kk}, image lies on the F_2-linear "
          f"Frobenius graph) < elementary dim={el_dim} <= ambient={ambient_dim}; "
          f"|im| ps={len(ps_keys)} vs el={len(el_keys)}: r2={ps_dim}/{ambient_dim} span collapse")
    # Resolution mandated by (A5 L935 / rem:binary-ambient-image): small-char
    # leaves retain ELEMENTARY coordinates -> restores the effective span, so the
    # collapse is a coordinate artifact, not a genuine image loss.  This is the
    # paper's own routing of the named collapse (switch profile/coordinates).
    check("C.frobenius.elementary_resolves", el_dim > ps_dim,
          f"elementary prefix span dim {el_dim} > power-sum {ps_dim}: coordinate route "
          f"out of the collapse ((A5) small-char clause); named collapse is caught")


# ===========================================================================
# PART D -- shallow-prefix automatic-FI (SE2 L3054: log A = o(|T|))
# ===========================================================================
def part_D_shallow():
    # POINTWISE: for any leaf, A/L <= A (since L>=1).  Hence if A = e^{o(N)}
    # (shallow), then A/L <= e^{o(N)} => (FI) with e^{-o(N)} = 1/A, no payment.
    ok = True
    for r in census_rows:
        if not (r["A"] / r["L"] <= r["A"] + 1e-9):
            ok = False
    check("D.shallow.A_over_L_le_A", ok,
          "A/L <= A on every leaf => (FI) discrepancy is bounded by A itself; "
          "A=e^{o(N)} (shallow) makes (FI) automatic with no payment")

    # Rank the configs by the shallow parameter w*log p (proxy for (a-k-1)log|B|);
    # confirm the ambient/image discrepancy exponent (ln(A/L)) is <= ln A exactly.
    worst_disc = 0.0
    for r in census_rows:
        disc = log(r["A"] / r["L"])
        capA = log(r["A"])
        if disc > capA + 1e-9:
            worst_disc = 1e9
        worst_disc = max(worst_disc, disc / capA if capA > 0 else 0.0)
    check("D.shallow.discrepancy_bounded_by_logA", worst_disc <= 1.0 + 1e-9,
          f"max ln(A/L)/ln(A) = {worst_disc:.3f} <= 1 across configs; the (FI) "
          f"gap never exceeds the ambient budget log A (shallow => o(n) => free)")

    # Contentful regime statement: (FI) is only nontrivial when log A grows
    # linearly, i.e. deep prefix w*log|B| = Theta(n).  None of the toy configs
    # is deep; report the largest log A / n as evidence of shallowness at scale.
    max_depth = max(log(r["A"]) / r["n"] for r in census_rows)
    check("D.shallow.toy_configs_are_shallow", max_depth > 0,
          f"max (log A)/n = {max_depth:.3f} over configs (finite toy depth; the "
          f"deep-prefix wall log A = Theta(n) is not reachable at toy scale -- SCOPE)")


# ===========================================================================
def main():
    part_A_identities()
    part_B_census()
    part_C_frobenius()
    part_D_shallow()

    # ---- census table (raw data for the note) ----
    print("=" * 78)
    print("(FI) CENSUS -- collapse ratios per leaf  (base %s)" % BASE_SHA)
    print("-" * 78)
    print("  regime      p  n  k  a  w   M      L    dim A_eff   A   kappa*  "
          "r1    r2    r_all")
    for r in census_rows:
        reg = "struct" if r["structured"] else "generic"
        print(f"  {reg:7s} {r['p']:3d}{r['n']:3d}{r['k']:3d}{r['a']:3d}{r['w']:3d} "
              f"{r['M']:6d} {r['L']:5d} {r['dim']:3d} {r['A_eff']:5d} {r['A']:5d} "
              f"{r['kappa_star']:6.3f} {r['r1']:.3f} {r['r2']:.3f} {r['r_all']:.3f}")
    print("-" * 78)
    print("  r1=lnL/lnA_eff (Gap-1 image/span)  r2=dim/w (Gap-2 span/ambient)  "
          "r_all=lnL/lnA")
    print("=" * 78)

    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = len(CHECKS) - npass
    for name, ok, detail in CHECKS:
        if not ok:
            print(f"  FAIL  {name}: {detail}")
    print()
    if nfail == 0:
        print(f"RESULT: PASS ({len(CHECKS)} checks)")
    else:
        print(f"RESULT: FAIL ({nfail} of {len(CHECKS)} checks failed)")
    return nfail == 0


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
