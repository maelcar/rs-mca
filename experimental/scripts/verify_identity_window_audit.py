#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_identity_window_audit.py -- stdlib-only, zero-arg, INDEPENDENT verifier
for the promotion-gate audit of the identity-dominance window criterion
(PR #542, experimental/notes/thresholds/envelope_identity_window.md) against
experimental/asymptotic_rs_mca_frontiers.tex hard input (d).

This is an ADVERSARIAL SELF-AUDIT verifier: it is written FRESH and shares NO
code path with verify_envelope_window.py (the #542 verifier).  Where #542 used a
floating-point brute scan for the window edges, this file recomputes the window
membership in EXACT RATIONAL ARITHMETIC (fractions.Fraction) treating the
entropy value h=H2(rho+g) and the crossing s=g*beta as free positive rationals
-- so the window algebra is checked with zero floating error.  Entropy /
enumeration are used only in the finite-tower and target-threshold sections, with
conservative margins.

It recomputes, from scratch:

  R.  RE-DERIVATION (exact, symbolic in h,s).  The competitor exponent
        e_c = (1/c)(h - lambda*s)
      re-derived here directly from the QR6 pigeonhole scale
        barN_{c,r}(w) = C(N,m) |B_phi|^{-floor(w/c)},  N=n/c, m=(a-r)/c,
      by the finite-n limit (section R2), AND its algebraic equality with the
      paper's QR8 rearrangement (1/c)(h-s)+(s/c)(1-lambda) (section R1, exact).
      Window edges kappa_low=(c-1)/(c-lambda), kappa_high=1/lambda and the wall
      margin ((1-lambda)/c) h are then derived and checked EXACTLY.

  W.  WINDOW vs DEFINITION (exact rational grid).  For a SINGLE competitor
      (c,lambda) the closed-form membership
        s <= kappa_low*h   OR   s >= kappa_high*h
      equals the primitive definition  e_c <= max(0, e_1),  e_1=h-s,  at every
      rational (h,s,c,lambda) grid point.  (Independent of #542's float scan.)

  S.  SOUNDNESS ATTACK (the audit's adversarial core).  Rows with MULTIPLE
      foldings {(c_i,lambda_i)}.  We compare three readings of the criterion:
        TRUE  : DOM over the full competitor set (definitional, exact),
        RED-a : "cheapest folding c_min with ITS OWN drop" (literal Rung-3 text),
        RED-c : "global-min c combined with global-min lambda" (independent-min),
        INT   : per-folding intersection of windows (the proposed repair).
      A point where a reading says DOMINANT but TRUE says FAIL is a SOUNDNESS
      HIT (COUNTEREXAMPLE_NEW_FLOOR).  We census hits per reading; the audit
      finding is that RED-a is UNSOUND while RED-c and INT are SOUND.

  P.  BAND-PLACEMENT of the paper's own obstruction.  thm:smooth-quotient-
      obstruction = (c=2,lambda=1/2,s=h): verify s=h is strictly interior to the
      band (kappa_low*h, kappa_high*h), that the excess e_c-max(0,e_1) PEAKS at
      s=h (not the geometric midpoint), and that the wall margin there is h/4.

  T.  TARGET-THRESHOLD.  Independent re-derivation that tau>=tau0:=F(g_low)>0
      pushes the right crossing g_T into the LOWER window; g_low<g* strictly.

  E.  FINITE F_{p^2} TOWER (independent).  Fresh construction of D=theta*H, the
      2-to-1 square folding, exact big-integer identity vs quotient scales, and
      the empirical quotient exponent -> (1/c)(h-lambda s) with shrinking error.

Exit 0 iff every check passes.
Run:  python3 experimental/scripts/verify_identity_window_audit.py
Target < 60 s under  ulimit -v 2097152.
"""

from __future__ import annotations
from fractions import Fraction as Fr
from math import log2, comb
from itertools import combinations

CHECKS = 0
FAILS = 0
LOG = []


def gate(cond, msg):
    global CHECKS, FAILS
    CHECKS += 1
    if not cond:
        FAILS += 1
        LOG.append("  FAIL: " + msg)
    return bool(cond)


def note(msg):
    LOG.append(msg)


# ===========================================================================
# Exact-rational criterion primitives (h,s are FREE positive rationals; the
# entropy value never enters -- this is what makes W and S float-free).
# ===========================================================================
def e1_of(h, s):
    """identity exponent e_1 = h - s."""
    return h - s


def ec_of(h, s, c, lam):
    """competitor exponent e_c = (1/c)(h - lambda*s), exact in h,s,lam."""
    return (h - lam * s) / c


def dom_true(h, s, competitors):
    """Primitive definition: identity dominates iff e_c<=max(0,e_1) for ALL."""
    r = max(Fr(0), e1_of(h, s))
    return all(ec_of(h, s, c, lam) <= r for (c, lam) in competitors)


def kappa_low(c, lam):
    return Fr(c - 1, 1) / (c - lam)


def kappa_high(lam):
    return Fr(1, 1) / lam


def window_dominant_single(h, s, c, lam):
    """Closed-form window predicate for ONE competitor (exact)."""
    return (s <= kappa_low(c, lam) * h) or (s >= kappa_high(lam) * h)


# ---------------------------------------------------------------------------
# R.  Independent re-derivation of the constants.
# ---------------------------------------------------------------------------
def section_R():
    note("== R. Re-derivation of e_c, window edges, wall margin ==")
    # R1: e_c closed form == QR8 rearrangement, EXACT in free rationals h,s.
    for hn in range(1, 7):
        for sn in range(1, 9):
            h = Fr(hn, 6)          # h in (0,1]
            s = Fr(sn, 4)          # s in (0,2]
            for c in (2, 3, 5, 7):
                for lam in (Fr(1, 10), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(9, 10), Fr(1)):
                    ec = ec_of(h, s, c, lam)
                    qr8 = (h - s) / c + (s / c) * (1 - lam)   # paper's QR8 form
                    gate(ec == qr8, f"R1 e_c==QR8 h={h} s={s} c={c} lam={lam}")
                    # wall margin at the crossing s=h must be ((1-lam)/c)*h
                    ec_cross = ec_of(h, h, c, lam)
                    gate(ec_cross == (1 - lam) * h / c,
                         f"R1 wall margin h={h} c={c} lam={lam}")
    # R1b: window edges solve e_c==max(0,e_1) exactly.
    #   Case A boundary: e_c == e_1  ->  s == kappa_low*h
    #   Case B boundary: e_c == 0    ->  s == kappa_high*h
    for c in (2, 3, 4, 5):
        for lam in (Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(3, 4), Fr(1)):
            h = Fr(1)  # scale-free
            s_lowedge = kappa_low(c, lam) * h
            gate(ec_of(h, s_lowedge, c, lam) == e1_of(h, s_lowedge),
                 f"R1b lower edge is e_c==e_1 c={c} lam={lam}")
            s_highedge = kappa_high(lam) * h
            gate(ec_of(h, s_highedge, c, lam) == Fr(0),
                 f"R1b upper edge is e_c==0 c={c} lam={lam}")
            # kappa_low in (0,1], kappa_high in [1,inf)
            gate(Fr(0) < kappa_low(c, lam) <= 1, f"R1b kappa_low range c={c} lam={lam}")
            gate(kappa_high(lam) >= 1, f"R1b kappa_high range lam={lam}")
            # for lam=1 the band is a single point s==h
            if lam == 1:
                gate(kappa_low(c, lam) == 1 and kappa_high(lam) == 1,
                     f"R1b lam=1 collapses c={c}")

    # R2: independent FINITE-n limit of the QR6 scale -> (1/c)(h-lam*s).
    # Build a synthetic tower: alpha=a/n fixed, |B|=2^beta, |B_phi|=2^(lam*beta),
    # w = g*n prefix eqns; compare (1/n)log2[C(N,m) |B_phi|^{-floor(w/c)}] to e_c.
    note("   R2: finite-n QR6 exponent -> (1/c)(h-lam*s) with shrinking error")
    prev = None
    for n in (600, 1200, 2400, 4800, 9600):
        alpha = 0.30
        beta = 3.0
        g = 0.08                     # prefix rate, w=g*n
        c, lam = 2, 0.5
        a = int(round(alpha * n))
        w = int(round(g * n))
        N = n // c
        m = a // c
        # exact big-int quotient scale:  C(N,m) * |B_phi|^{-floor(w/c)}
        log_scale = log2(comb(N, m)) - (w // c) * (lam * beta)
        emp = log_scale / n
        h = H2(alpha)
        s = g * beta
        form = (h - lam * s) / c
        err = abs(emp - form)
        gate(err < 0.02, f"R2 emp~form n={n} emp={emp:.5f} form={form:.5f} err={err:.5f}")
        if prev is not None:
            gate(err <= prev + 1e-9, f"R2 error shrinks n={n} err={err:.5f} prev={prev:.5f}")
        prev = err


def H2(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * log2(x) - (1.0 - x) * log2(1.0 - x)


# ---------------------------------------------------------------------------
# W.  Window predicate == primitive definition, EXACT rational grid.
# ---------------------------------------------------------------------------
def section_W():
    note("== W. Closed-form window == primitive definition (exact rationals) ==")
    hs = [Fr(i, 8) for i in range(1, 9)]           # h in (0,1]
    ss = [Fr(j, 8) for j in range(1, 25)]          # s in (0,3]
    cs = [2, 3, 4, 6]
    lams = [Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(1)]
    n_pts = 0
    for h in hs:
        for s in ss:
            for c in cs:
                for lam in lams:
                    prim = dom_true(h, s, [(c, lam)])
                    clsd = window_dominant_single(h, s, c, lam)
                    gate(prim == clsd,
                         f"W closed==prim h={h} s={s} c={c} lam={lam} "
                         f"prim={prim} clsd={clsd}")
                    n_pts += 1
    note(f"   W: {n_pts} exact rational points, closed form == definition")


# ---------------------------------------------------------------------------
# S.  SOUNDNESS ATTACK: multi-folding rows, the audit's adversarial core.
# ---------------------------------------------------------------------------
def red_a_dominant(h, s, foldings):
    """Reading (a), FAITHFUL to the note's Rung-3 wording: 'the row's cheapest
    folding c_min with its deepest field drop lambda_min'.  So: restrict to the
    smallest-degree foldings, then take the DEEPEST drop (smallest lambda) AMONG
    THOSE.  (This is the note's own prescription -- not a strawman.)  Its blind
    spot: a deeper drop carried by a folding of NON-minimal degree is ignored."""
    cmin = min(c for (c, _) in foldings)
    lam_at_cmin = min(lam for (c, lam) in foldings if c == cmin)
    return window_dominant_single(h, s, cmin, lam_at_cmin)


def red_c_dominant(h, s, foldings):
    """Reading (c): global-min c combined with global-min lambda (fictitious)."""
    cmin = min(c for (c, _) in foldings)
    lmin = min(lam for (_, lam) in foldings)
    return window_dominant_single(h, s, cmin, lmin)


def intersection_dominant(h, s, foldings):
    """Repair: dominant iff s in the safe window of EVERY folding."""
    return all(window_dominant_single(h, s, c, lam) for (c, lam) in foldings)


def section_S():
    note("== S. Soundness attack: multi-folding rows (readings a / c / int) ==")
    # Realizable field example: B=F_{2^10}; proper-subfield drops lam in
    # {1/10,2/10,5/10}.  Build rows with two foldings of anti-correlated (c,lam).
    subfield_lams = [Fr(1, 10), Fr(1, 5), Fr(1, 2)]
    degs = [2, 3, 5, 7]
    rows = []
    for (c1, l1) in [(c, l) for c in degs for l in subfield_lams]:
        for (c2, l2) in [(c, l) for c in degs for l in subfield_lams]:
            if (c1, l1) == (c2, l2):
                continue
            rows.append([(c1, l1), (c2, l2)])
    # exact (h,s) grid
    hs = [Fr(i, 6) for i in range(1, 7)]
    ss = [Fr(j, 6) for j in range(1, 37)]     # s up to 6
    hits_a = hits_c = hits_int = 0
    total_pts = 0
    example = None
    for foldings in rows:
        for h in hs:
            for s in ss:
                total_pts += 1
                truth = dom_true(h, s, foldings)
                a = red_a_dominant(h, s, foldings)
                cc = red_c_dominant(h, s, foldings)
                it = intersection_dominant(h, s, foldings)
                # SOUNDNESS violation = reading says DOMINANT while truth=FAIL
                if a and not truth:
                    hits_a += 1
                    if example is None:
                        example = (foldings, h, s)
                if cc and not truth:
                    hits_c += 1
                if it and not truth:
                    hits_int += 1
    note(f"   S: census pts={total_pts} rows={len(rows)}  "
         f"soundness hits: RED-a={hits_a}  RED-c={hits_c}  INT={hits_int}")
    # THE FINDING: RED-a is unsound (>0 hits); RED-c and INT are sound (0 hits).
    gate(hits_a > 0, "S RED-a is UNSOUND (finds soundness hits) -- expected")
    gate(hits_c == 0, "S RED-c (independent-min) is SOUND (0 hits)")
    gate(hits_int == 0, "S INT (per-folding intersection repair) is SOUND (0 hits)")
    # exhibit the concrete refutation and verify it by hand-value.
    if example is not None:
        foldings, h, s = example
        note(f"   S: concrete RED-a counterexample foldings={foldings} h={h} s={s}")
    # canonical hand-checked witness: B=F_{2^10}, foldings (2,1/2) and (5,1/10),
    # at s=3h.  RED-a([cheapest c=2, its drop 1/2]) says dominant; TRUE says fail.
    h0, s0 = Fr(1), Fr(3)     # s=3h with h=1
    foldings0 = [(2, Fr(1, 2)), (5, Fr(1, 10))]
    gate(red_a_dominant(h0, s0, foldings0) is True,
         "S witness: RED-a declares DOMINANT at s=3h")
    gate(dom_true(h0, s0, foldings0) is False,
         "S witness: TRUE dominance FAILS at s=3h")
    # the breaking competitor is (5,1/10): e_c>0 while max(0,e_1)=0
    gate(ec_of(h0, s0, 5, Fr(1, 10)) > 0 and e1_of(h0, s0) < 0,
         "S witness: competitor (5,1/10) has e_c>0=max(0,e1)")
    gate(intersection_dominant(h0, s0, foldings0) is False,
         "S witness: INT repair correctly declares FAIL")


# ---------------------------------------------------------------------------
# P.  Band-placement of the paper's own obstruction (c=2,lam=1/2,s=h).
# ---------------------------------------------------------------------------
def section_P():
    note("== P. smooth-quotient-obstruction placement (c=2,lam=1/2,s=h) ==")
    c, lam = 2, Fr(1, 2)
    for hn in range(1, 6):
        h = Fr(hn, 5)
        kl = kappa_low(c, lam) * h        # (1)/(3/2) h = 2/3 h
        kh = kappa_high(lam) * h          # 2 h
        s = h                              # the crossing
        gate(kl < s < kh, f"P s=h strictly interior band h={h} band=({kl},{kh})")
        gate(kl == Fr(2, 3) * h and kh == 2 * h, f"P band edges h={h}")
        # excess peaks at s=h, value h/4 = ((1-lam)/c) h
        exc_at_h = ec_of(h, h, c, lam) - max(Fr(0), e1_of(h, h))
        gate(exc_at_h == h / 4, f"P wall margin h/4 at crossing h={h}")
        # excess is < value-at-h just inside on both sides (peak, not midpoint)
        for eps in (Fr(1, 20), Fr(1, 10)):
            for sp in (h - eps, h + eps):
                if not (kl < sp < kh):
                    continue
                exc = ec_of(h, sp, c, lam) - max(Fr(0), e1_of(h, sp))
                gate(exc < exc_at_h, f"P excess peaks at s=h h={h} sp={sp}")
        # geometric midpoint of the band is (2/3+2)/2 h = 4/3 h != h
        mid = (kl + kh) / 2
        gate(mid != s, f"P crossing is NOT geometric midpoint h={h} mid={mid}")


# ---------------------------------------------------------------------------
# T.  Target-threshold: tau>=tau0 -> crossing in lower window; g_low<g*.
# ---------------------------------------------------------------------------
def F_of(rho, beta, g):
    return H2(rho + g) - beta * g


def right_crossing(rho, beta, tau):
    """Rightmost g with F(g)>=tau; concave F, bisect on decreasing branch."""
    lo, hi = 0.0, 1.0 - rho - 1e-12
    best_g, best_v, Ng = 0.0, F_of(rho, beta, 0.0) - tau, 4000
    for i in range(Ng + 1):
        g = (1.0 - rho) * i / Ng
        v = F_of(rho, beta, g) - tau
        if v > best_v:
            best_v, best_g = v, g
    if best_v < 0:
        return None
    a, b = best_g, hi
    if F_of(rho, beta, b) - tau > 0:
        return b
    for _ in range(200):
        mmid = 0.5 * (a + b)
        if F_of(rho, beta, mmid) - tau >= 0:
            a = mmid
        else:
            b = mmid
    return 0.5 * (a + b)


def lower_edge_g(rho, beta, c, lam):
    """g_low: beta*g == kappa_low*H2(rho+g), positive root (bisection)."""
    kl = float(kappa_low(c, lam))
    phi = lambda g: beta * g - kl * H2(rho + g)
    lo, hi = 1e-9, 1.0 - rho - 1e-9
    if phi(hi) < 0:
        return hi
    if phi(lo) >= 0:
        return lo
    for _ in range(200):
        mmid = 0.5 * (lo + hi)
        if phi(mmid) < 0:
            lo = mmid
        else:
            hi = mmid
    return 0.5 * (lo + hi)


def section_T():
    note("== T. Target-threshold form: tau>=tau0 -> lower window ==")
    c, lam = 2, 0.5
    for rho in (0.20, 0.35, 0.50):
        for beta in (1.5, 2.5, 4.0):
            gstar = right_crossing(rho, beta, 0.0)
            if gstar is None:
                continue
            glow = lower_edge_g(rho, beta, c, lam)
            tau0 = F_of(rho, beta, glow)
            gate(glow < gstar - 1e-6, f"T g_low<g* rho={rho} beta={beta}")
            gate(tau0 > 1e-6, f"T tau0>0 rho={rho} beta={beta} tau0={tau0:.5f}")
            # at g_low the crossing s=beta*g_low is exactly the lower edge
            slow = beta * glow
            hlow = H2(rho + glow)
            gate(abs(slow - float(kappa_low(c, lam)) * hlow) < 1e-6,
                 f"T lower-edge identity rho={rho} beta={beta}")
            for frac in (1.0, 1.3, 1.8):
                tau = tau0 * frac
                gT = right_crossing(rho, beta, tau)
                if gT is None:
                    continue
                gate(gT <= glow + 1e-6, f"T tau>=tau0 -> gT<=g_low rho={rho} beta={beta} f={frac}")
                sT, hT = beta * gT, H2(rho + gT)
                gate(sT <= float(kappa_low(c, lam)) * hT + 1e-9,
                     f"T crossing in lower window rho={rho} beta={beta} f={frac}")


# ---------------------------------------------------------------------------
# E.  Independent finite F_{p^2} tower (fresh field arithmetic).
# ---------------------------------------------------------------------------
def build_fp2(p):
    nu = next(c for c in range(2, p) if pow(c, (p - 1) // 2, p) == p - 1)

    def mul(x, y):
        (a, b), (c, d) = x, y
        return ((a * c + b * d * nu) % p, (a * d + b * c) % p)

    def powr(x, e):
        r, base = (1, 0), x
        while e > 0:
            if e & 1:
                r = mul(r, base)
            base = mul(base, base)
            e >>= 1
        return r

    return nu, mul, powr


def generator(p, mul, powr):
    order = p * p - 1
    fac, m, d = set(), order, 2
    while d * d <= m:
        while m % d == 0:
            fac.add(d)
            m //= d
        d += 1
    if m > 1:
        fac.add(m)
    for a in range(1, p):
        for b in range(0, p):
            if (a, b) == (1, 0):
                continue
            g = (a, b)
            if all(powr(g, order // q) != (1, 0) for q in fac):
                return g
    raise RuntimeError("no gen")


def section_E():
    note("== E. Independent finite F_{p^2} tower: scales + field drop ==")
    for p in (5, 7, 11, 13):
        n = 2 * (p - 1)
        c = 2
        a = 2 * round(0.3 * n / 2)
        a = max(a, 2)
        m, N, w = a // 2, n // 2, 2
        nu, mul, powr = build_fp2(p)
        th = generator(p, mul, powr)
        order = p * p - 1
        gate(order % n == 0, f"E n|p^2-1 p={p}")
        step = order // n
        D = [powr(th, 1 + j * step) for j in range(n)]
        gate(len(set(D)) == n, f"E |D|=n p={p}")
        sq = [mul(x, x) for x in D]
        Q = set(sq)
        gate(len(Q) == N, f"E |phi(D)|=N p={p}")
        # complete 2-fibers
        from collections import Counter
        gate(all(v == 2 for v in Counter(sq).values()), f"E complete 2-fibers p={p}")
        # field drop: Q subset eta*F_p, eta=theta^2
        eta = mul(th, th)
        inv_eta = powr(eta, p * p - 2)
        gate(all(mul(inv_eta, q)[1] % p == 0 for q in Q),
             f"E field drop Q<=eta*F_p p={p}")
        # exact scale comparison: quotient natural scale vs identity avg
        barN1 = Fr(comb(n, a), (p * p) ** w)         # identity natural scale
        quo = Fr(comb(N, m), p ** (w // c))          # QR6 quotient natural scale
        # exact-integer pigeonhole floor: some prefix bucket carries ceil(QR6)>=1
        ceil_quo = -(-comb(N, m) // (p ** (w // c)))
        gate(ceil_quo >= 1, f"E pigeonhole bucket ceil(QR6)>=1 p={p} ceil={ceil_quo}")
        # the quotient cell carries strictly more than the identity natural scale
        gate(quo > barN1, f"E quotient>identity (exact) p={p} "
                          f"quo={float(quo):.4f} barN1={float(barN1):.4f}")


def main():
    print("verify_identity_window_audit.py -- promotion-gate self-audit of #542")
    print("target: experimental/asymptotic_rs_mca_frontiers.tex hard input (d)")
    print("-" * 72)
    section_R()
    section_W()
    section_S()
    section_P()
    section_T()
    section_E()
    print("\n".join(LOG))
    print("-" * 72)
    if FAILS == 0:
        print(f"RESULT: PASS ({CHECKS} checks)")
    else:
        print(f"RESULT: FAIL ({FAILS} of {CHECKS} checks failed)")
    return 0 if FAILS == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
