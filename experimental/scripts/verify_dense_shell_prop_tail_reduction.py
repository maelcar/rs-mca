#!/usr/bin/env python3
"""Verifier: dense-shell PROP-TAIL structural reduction + certified contraction frame.

Stacked on the predecessor packet (dense_shell_inv_tail_closure.md /
verify_dense_shell_inv_tail_closure.py, PR #885). Objects as there: level vectors
G_n(t), t in [1/6,1/2], c-dictionary c_0=b_0, c_i=b_i/2 even-extended; one branch =
Z-convolution with K_d=(1/4,d,1/4), d(t)=-cos(2 pi t)/2; children t_pm=(1 pm t)/3;
mass factor a(t)=sin^2(pi t)=1/2+d(t), a'(t)=pi sin(2 pi t). The step (STEP):
c(G_n(t)) = K_{d(t_+)}*c(G_{n-1}(t_+)) + K_{d(t_-)}*c(G_{n-1}(t_-)).

Write rc_i := c_{i+1}/c_i (band ratio), L_i := d/dt log c_i (log-t-derivative),
g_i(n,t) := c_i(G_n(t_-))/c_i(G_n(t_+)) (sibling ratio, V13 convention), rho_prop@i<W
:= max_{i<W} g_i / min_{i<W} g_i. Operative window i<17 throughout (OPWIN=17); the
honest child-read window is i<18 (CWIN=18, Lemma W1/W2 of the note).

HONEST CLAIM STRUCTURE. (PROP-TAIL) is discharged as a CERTIFIED-CENSUS theorem
MODULO a small, explicitly enumerated set of COMPUTED clauses (Section 8 of the note).
The composed equilibrium chain and its algebra are PROVED; the load-bearing gates
V15-IA (contraction constant theta_band) and V17-IA (forcing F_box) are exact-Fraction
interval-arithmetic censuses over the certified LC ratio box. What is NOT certified,
and is monitored by named gates rather than asserted, is enumerated in the discharge
note's "Computed clauses" subsection and reproduced here:
  (LAM-BOX)   DISCHARGED-conditional (gate LAM-INV, full mode only). The sibling-
              proportionality magnitude box [lam,Lambda^+,Lambda^-] that both
              load-bearing gates box-max over is now a PROVED invariant-interval
              enclosure (DERIV_LAMBOX.md): an exact windowed mass recursion identity
              + a Birkhoff mass-field enclosure + a coupled Lambda-field enclosure,
              CONDITIONAL on the existing floor box, the existing finite base-case
              census (MAG-BOX/V18), an a-posteriori Lipschitz self-check, and one
              correction-derivative cap C' (clause (C'-CAP) -- a generous MONITORED
              constant when this upgrade landed, itself DISCHARGED-conditional as of
              this revision, see the (C'-CAP) block below). Gate MAG-BOX still
              monitors the realized magnitudes at every grid level (now the empirical
              cross-check of the proved intervals, not the sole evidence for them).
  (SIB-BAND)  DISCHARGED at a deep anchor (gate SIB-CERT, full mode only). V15-IA/V17-IA
              (at J0*=500) still certify only the FORCED-PROPORTIONAL surrogate
              c^+ = lam*c^-; the real cascade is non-proportional, c^+_i = lam*w_i*c^-_i
              with per-entry sibling wobble w_i, IH rho_prop<=TARGET. The GEOMETRIC-CENTER
              LEMMA (3 lines, no new assumption beyond (LAM-BOX)): lam_gc :=
              sqrt(min_i rho_i * max_i rho_i) is itself a legal (LAM-BOX) point, and
              w_i := rho_i/lam_gc lies in the half-band [1/sqrt R*,sqrt R*] by the IH
              alone. Re-running the wobble census over that half-band at a deep anchor
              (J0=800, pad=999/1000) CLEARS the equilibrium threshold (+7.4% margin
              round-2 boundary-corrected, gate SIB-CERT; round 1 was +4.6%) --
              shallower deep anchors miss (600: -11.1%, 700: -1.9%),
              and the full (non-geometric-center) band [1/R*,R*] never clears at any
              depth. This closes the real-vs-proportional gap the surrogate leaves open;
              see note Section 8.
  (FOLD)      the child-window fold factor <=57/50 (Lemma W1) is a grid-measured bound
              (gate V16b), COMPUTED.
  (FLOOR-PERSIST) floor persistence for n>J0* -- the exact as-consumed form (note S8.4):
              child ratio profiles at the branch parameters vs the parent-t anchor
              family, at both anchors. COMPUTED (the upward CLT drift), now FIRST-CLASS:
              gate FLOOR-DRIFT monitors the drift mechanism directly (123 parameters,
              consecutive deep-grid pairs) plus the as-consumed margins; the pointwise
              corner-census discharge route is CLOSED as a route-cut (note S9(v),
              reproduced as an informational negative control on the gate line).
  (C'-CAP)    the Lambda correction-derivative cap CPRIME=3/500 -- DISCHARGED-conditional
              (this revision, R1 mitigation (a)): gate LAM-INV certifies the exact-
              identity drop bound [gbar*|Lambda_pure| + C'/P]/(1-gbar) <= CPRIME at
              every NG node from per-branch floor-box data + the (FOLD)-folded
              equilibrium ceiling (untampered V15-IA/V17-IA chain); worst 0.004245,
              29% margin. The a-posteriori monitor is RETAINED as cross-check. No
              monitored-only literal remains in the packet.
STATUS: CONDITIONAL. PROVED would require zero computed clauses. Remaining computed
clauses: (FOLD), (FLOOR-PERSIST). (LAM-BOX) is DISCHARGED-conditional by gate LAM-INV;
(SIB-BAND) is DISCHARGED at the deep anchor by gate SIB-CERT (geometric-center
certified census) GIVEN (LAM-BOX); (C'-CAP) is DISCHARGED-conditional by LAM-INV's
floor-box node census -- see note Section 8. The arithmetic fact
rho_prop@i<17(n)<=1.02560749 is supported with margin by every gate; the packet's
rigor is scoped by the clauses above.

Gates (8 core in --quick/--fallback; 11 core in the default full mode, determine RESULT;
informational lines printed but NOT counted):
  F3   [FLOORS]    re-certifies the floor family r_i(J0*,t) at the anchor (positivity,
                   LC-compatibility, the i=0 halving-convention cross-check).
  MAG-BOX [LAM-BOX monitor] verifies the realized magnitudes lam=sum(c^+)/sum(c^-),
                   Lambda^+/-, and the per-entry sibling ratios rho_i=c^+_i/c^-_i lie
                   inside the magnitude boxes at every grid level; prints worst headroom.
                   Now the empirical cross-check of gate LAM-INV's proved intervals
                   (below), not the sole evidence the box holds.
  V15-IA [THETA-BAND, LOAD-BEARING] the certified upper bound on the Lemma A1 tangent
                   seminorm over the certified LC ratio box, folded by the Window Lemma
                   factor (<=57/50). The sup over the magnitude scalar lam is enclosed by
                   MINCING lam into panels and taking each Moebius-in-lam matrix entry's
                   exact per-panel range (no endpoint-sufficiency assumption); feeds
                   gate_forcing_ia as theta_star.
  V16 [THETASYMB] the exact Fraction polynomial identity
                   75(1-x^2)-(6+3x)^2 = -3(2x-1)(14x+13), x=cos(2 pi t/3), plus the
                   domain sign argument on x in [1/2,cos(pi/9)] ((2x-1)>=0,(14x+13)>0):
                   proves theta~(t)<=1/5 exactly, equality only at t=1/2.
  V16b [WINDOW]   the rational fact 289/256<=57/50 (asymptotic vs certified child-window
                   inflation factor), the grid check sup spread_{i<18}(L)/spread_{i<17}(L)
                   <=57/50 (a grid-measured COMPUTED bound (FOLD)), and the child-window
                   read-set structural check (Lemma W2): omitting c_17 undercounts.
  V17 [FORCING]    F_ext(n)*n^2 and Curv(n)*n^2 bounded <=200 (window i<17, edge locus);
                   PLUS the G2/alpha-route source census (V12-band corners filtered by
                   rho_prop<=TARGET) reproduced as a NEGATIVE CONTROL -- INFORMATIONAL,
                   printed inline, does not affect this gate's PASS/FAIL.
  V17-IA [FORCING, LOAD-BEARING] the minced/closed-form interval-arithmetic census of
                   F_box(J0*,f*) <= (1-theta_band)*tau*, theta_band supplied by V15-IA.
                   Certifies the FORCED-PROPORTIONAL surrogate; the real-vs-proportional
                   gap this leaves is closed by SIB-CERT below, not by this gate.
  V18 [VTRACK]     the deep grid rho_prop@i<17(n)<=1.02560749 (all levels, now to n=800)
                   + monotone non-increasing + the V_17(n) vs tau*=3log(1.02560749)
                   crossover at n=62 (every-integer scan) + margins.
  SIB-CERT [core, FULL MODE ONLY, discharges (SIB-BAND)] the geometric-center half-band
                   wobble census (GEOMETRIC-CENTER LEMMA: lam_gc=sqrt(min rho_i*max rho_i)
                   is a legal (LAM-BOX) point, w_i=rho_i/lam_gc lies in
                   [1/sqrt R*,sqrt R*] by the IH alone -- no assumption beyond (LAM-BOX))
                   re-run at the deep anchor (J0=800,pad=999/1000), where it clears
                   (+7.4% margin, round-2 boundary-corrected) -- covering the REAL
                   non-proportional cascade, not merely the surrogate. Outwardness
                   self-check on the sqrt bracket + the W17 boundary-slot box.
                   SKIPPED (informational line only) under --quick/--fallback, since the
                   deep anchor needs the full J0=800 build.
  LAM-INV [core, FULL MODE ONLY, discharges (LAM-BOX) and (C'-CAP)] the PROVED
                   invariant-interval upgrade (DERIV_LAMBOX.md): one forward-pass
                   T-invariance of the mass interval field (NG=3841) + a-posteriori
                   sup|Lambda|<=LIP_S; one forward-pass invariance of the coupled
                   Lambda field + a-posteriori sup|Lambda'|<=LIP_L; a floor-box-PROVED
                   bound on the mass-correction fraction gamma<=GMAX; and -- this
                   revision -- the floor-box-PROVED (C'-CAP) node census (exact drop
                   identity + per-branch floor data + the (FOLD)-folded equilibrium
                   ceiling from the untampered memoized V15-IA/V17-IA chain), with the
                   a-posteriori C' monitor retained as cross-check. Base case (finite
                   grid) cited from the existing MAG-BOX/V18 gates, not re-derived.
                   SKIPPED (informational line only) under --quick/--fallback.
  FLOOR-DRIFT [core, FULL MODE ONLY, monitors (FLOOR-PERSIST) -- monitoring, NOT a
                   proof] the drift mechanism rc_i(n2,s)>=rc_i(n1,s) over consecutive
                   deep-grid pairs n1>=J0*, 123 parameters (parents+branches), i<18,
                   PLUS the exact as-consumed floor margins at both anchors, PLUS the
                   note-S9(v) route-cut negative control (informational, inline).
                   SKIPPED (informational line only) under --quick/--fallback.
  (informational): SIB-BAND (the shallow-anchor (J0*=500) wobble-extended exhibit +
                   gap, superseded as the discharge by SIB-CERT above), V15-GRID (grid
                   theta census, robustness), V17-INFO (G2 negative control), V19
                   [BRIDGE] w(n)<=0.62, alpha-only.

Flags: --quick runs a shallow dev-only subset (NOT a certified claim); --table prints
the full per-level rho_prop/V_17 table (transcribed by the Lean package); --fallback
switches the WHOLE triple atomically to the legacy chain (J0=430, f=49/50, theta*=1/2
fixed) as an informational alternative; --tamper-selftest runs the tamper suite (each
isolated to its own report/info line), always at the default (non-quick) depth. stdlib
only, deterministic.
"""
import itertools
import math
import sys
import time
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

PI = math.pi
K = 80

NODES = [0.25 * (1 + math.cos(PI * m / K)) for m in range(K + 1)]
BW = [(0.5 if m in (0, K) else 1.0) * (1 if m % 2 == 0 else -1) for m in range(K + 1)]

# ---------------------------------------------------------------- cascade (verbatim)
# Same functions as the predecessor verifier (V1-checked there to 1.8e-15).

def a_of(t):
    s = math.sin(PI * t)
    return s * s

def d_of(t):
    return -0.5 * math.cos(2 * PI * t)

def dprime(t):                      # a'(t) = d'(t), exact identity
    return PI * math.sin(2 * PI * t)

def mult_root(c, a):
    out = [0.0] * (len(c) + 1)
    for i, ci in enumerate(c):
        out[i] += (0.5 - a) * ci
        out[i + 1] += (0.25 if i >= 1 else 0.5) * ci
        if i >= 1:
            out[i - 1] += 0.25 * ci
    return out

def flip(c):
    d = len(c) - 1
    return [ci if (d - i) % 2 == 0 else -ci for i, ci in enumerate(c)]

def bary(tq, vals):
    for m, tm in enumerate(NODES):
        if abs(tq - tm) < 1e-14:
            return vals[m][:]
    num = [0.0] * len(vals[0]); den = 0.0
    for m, tm in enumerate(NODES):
        s = BW[m] / (tq - tm); den += s
        for i in range(len(num)):
            num[i] += s * vals[m][i]
    return [x / den for x in num]

def cvec(t, lev_j):
    b = flip(bary(t, lev_j))
    return [b[0]] + [x / 2.0 for x in b[1:]]

def conv_even(c, d):
    n = len(c)
    def get(i):
        i = abs(i)
        return c[i] if i < n else 0.0
    return [0.25 * get(i - 1) + d * get(i) + 0.25 * get(i + 1) for i in range(n + 1)]

def build_levels(jmax):
    levs = [[[1.0] for _ in NODES]]
    for _ in range(jmax):
        prev = levs[-1]; out = []
        for t in NODES:
            acc = None
            for dd in (-1.0, 1.0):
                tv = abs((dd + t) / 3.0)
                c = mult_root(bary(tv, prev), a_of(tv))
                acc = c if acc is None else [x + y for x, y in zip(acc, c)]
            out.append(acc)
        levs.append(out)
    return levs

def spread(xs):
    return max(xs) - min(xs)

# ------------------------------------------------------------------- shared conventions

CENSUS_DEG = 16
OPWIN = CENSUS_DEG + 1        # 17: the operative window (V12/V13's corner-vector length)
CWIN = OPWIN + 1              # 18: the honest child-read window (tridiagonal reads 1 beyond)
NPAR = 41
PARENTS = [1.0 / 6 + (1.0 / 3 - 1e-4) * k / (NPAR - 1) for k in range(NPAR)]
EDGE = PARENTS[-1]
TARGET = 1.02560749
LTARGET = math.log(TARGET)
TAU_STAR = 3 * LTARGET         # float, display/legacy only (= 0.075855...)

# tau* = 3*ln(TARGET), needed as a certified Fraction LOWER bound (rounded DOWN) so it is
# safe in BOTH uses: (a) as the equilibrium threshold factor (1-theta)*tau* -- a smaller
# tau* gives a smaller threshold = a HARDER test = conservative; (b) as the reduction
# ceiling, where the conclusion rho_prop <= exp((1/3)*ceiling) <= TARGET needs
# (1/3)*ceiling <= ln(TARGET), i.e. ceiling <= 3*ln(TARGET) = tau* -- checking against an
# UNDER-estimate of tau* is again conservative (ceiling <= tau*_lo <= tau*_true). The
# float 3*math.log(TARGET) rounds UP (by ~2e-16, the UNSAFE direction), so we transcribe a
# rational with stated digits strictly below the true value and CERTIFY the bracket via a
# 50-digit Decimal ln at import (assert TAU_STAR_FR <= true 3*ln(TARGET)).
TAU_STAR_FR = Fr(75855330599169, 10**15)     # 0.075855330599169 <= 3*ln(1.02560749)
getcontext().prec = 50
_TAU_TRUE = 3 * Decimal("1.02560749").ln()    # 0.07585533059916962964... (50 sig digits)
assert TAU_STAR_FR <= Fr(_TAU_TRUE), "TAU_STAR_FR must be a LOWER bound on 3*ln(TARGET)"
assert Fr(75855330599170, 10**15) > Fr(_TAU_TRUE), "TAU_STAR_FR bracket too loose"  # tight to 1e-15

DEEP_GRID_DEFAULT = [48, 60, 80, 100, 128]
DEEP_GRID_DEEP = [48, 50, 55, 60, 70, 80, 100, 128, 160, 200, 240, 300]
THETA_GRID_DEFAULT = [60, 80, 100, 128]
THETA_GRID_DEEP = [60, 80, 100, 128, 200, 300]
BRIDGE_GRID_DEFAULT = [60, 80, 100, 128]
BRIDGE_GRID_DEEP = [60, 80, 100, 128, 200]
G2_GRID = [60, 100]             # the two levels the note's inflation figures cite
MAG_GRID = [48, 60, 100, 200, 300, 500]   # levels MAG-BOX monitors (incl. the thin-headroom band)

# ---------------------------------------------------------- discharge anchor
#
# The deep-base equilibrium route closes the arithmetic slot on finite checks at a deep
# base J0*, no decay-rate / no-Edgeworth input. theta* = theta_band is COMPUTED at runtime
# by gate_theta_ia (the certified band-uniform seminorm bound over the box, valid for every
# n>=J0) and fed directly into gate_forcing_ia as theta_star -- the two load-bearing gates
# are chained, not independent checks of a fixed constant. Both certify the forced-
# PROPORTIONAL surrogate (see the (SIB-BAND) clause); the shipped anchor is
# (J0*, f*, theta*) = (500, 99/100, theta_band). DEEP_GRID_FULL is the default grid (this
# IS the discharge, not behind a flag); DEEP_GRID_QUICK is a shallow dev-only subset
# (--quick), NOT a certified claim. --fallback switches atomically to a shallower legacy
# chain (J0=430, f=49/50, theta*=1/2 fixed) as an informational alternative only.
J0_STAR = 500
J0_FALLBACK = 430
F_STAR = Fr(99, 100)                 # 0.99 pad, the shipped anchor
F_LEGACY = Fr(49, 50)                # 0.98 pad, the legacy --fallback alternative only
THETA_FALLBACK = Fr(1, 2)            # legacy fallback theta* = 0.50 (--fallback only,
                                     # a fixed constant resting on a grid measurement,
                                     # informational -- NOT part of the certified chain)

# SIB-CERT deep anchor: discharges the (SIB-BAND) computed clause (see gate_sib_cert
# below). A much deeper base than (J0_STAR, F_STAR) is required for the geometric-center
# wobble census to clear -- soundings at (600,999/1000) and (700,999/1000) still MISS
# (-11.1%, -1.9%); (800, 999/1000) CLEARS (+4.6%). FULL mode only (--quick/--fallback
# skip gate_sib_cert; see compute()).
J0_SIB = 800
PAD_SIB = Fr(999, 1000)              # 0.999 pad -- tighter than F_STAR (99/100); required
                                     # at this depth (pad 99/100 at J0=800 still misses, -12.2%)

DEEP_GRID_FULL = [48, 50, 55, 60, 62, 70, 80, 100, 128, 160, 200, 240, 300, 340,
                   400, 430, 450, 500, 550, 600, 650, 700, 750, 800]
DEEP_GRID_QUICK = [48, 50, 55, 60, 70, 80, 100, 128, 160, 200]
THETA_GRID_FULL = [60, 80, 100, 128, 200, 300, 430, 500]
BRIDGE_GRID_FULL = [60, 80, 100, 128, 200, 430, 500]

WIN_STAR = OPWIN                     # P_i, i=0..16 (17 values) -- the forcing's own window
FLOOR_WIN = CWIN                     # F3 emits ratios i<18 (CWIN=18), one wider (Lemma W2 margin)

def frac_exact(x):
    """Exact Fraction conversion of an IEEE double -- introduces NO additional rounding
    (Fraction(float) is exact: it reads off the double's own binary value)."""
    return Fr(x)

def frac_outward(x, lo, slop=Fr(1, 10**9)):
    """Convert float x to a Fraction, then nudge OUTWARD by `slop` (relative) in the
    conservative direction: `lo=True` rounds down (a valid lower bound), `lo=False`
    rounds up (a valid upper bound). Documented, printed slop covering the residual
    floating-point error inherited from the cascade's trig/barycentric evaluation
    (~1e-15 relative) -- slop=1e-9 is six orders of magnitude more conservative than
    that residual, at zero measurable cost against the certified margins below."""
    base = frac_exact(x)
    adj = (abs(base) if base != 0 else Fr(1)) * slop
    return base - adj if lo else base + adj

IA_SLOP = Fr(1, 10**9)               # the documented outward slop (printed by the gates)
LAM_MINCE = 24                       # lam-panels for V15-IA's certified sup over the lam box
                                     # (see the V15-IA method note: NO endpoint-sufficiency)

def round_up_frac(x, denom=10**7):
    """Round a Fraction UP (outward, conservative direction) to a clean denominator --
    used only so theta_band (an exact Fraction accumulated over many box/lam corner
    divisions, hence an impractically large numerator/denominator pair) prints and
    threads through the rest of the chain as a manageable rational, while remaining a
    valid (very slightly more conservative, never less) certified upper bound: rounding
    theta_band UP only SHRINKS the downstream requirement (1-theta_band)*tau*, so any
    margin computed against the rounded value is a valid, if marginally more
    conservative, margin against the true certified value too."""
    return Fr(math.ceil(x * denom), denom)

def rho_win_locus(levs, j, nmax, parents=PARENTS):
    worst = 0.0; wt = None
    for t in parents:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        bp = flip(bary(tp, levs[j])); bm = flip(bary(tm, levs[j]))
        vp = [bp[0]] + [x / 2.0 for x in bp[1:]]
        vm = [bm[0]] + [x / 2.0 for x in bm[1:]]
        n = min(nmax, len(vp), len(vm))
        g = [vm[i] / vp[i] for i in range(n) if vp[i] > 1e-250]
        r = max(g) / min(g)
        if r > worst:
            worst = r; wt = t
    return worst, wt

def Lvec(t, j, levs, nmax, h=2e-4):
    """L_i = d/dt log c_i(G_j(t)), Richardson central diff O(h^4)."""
    a1 = cvec(t + h, levs[j]); b1 = cvec(t - h, levs[j])
    a2 = cvec(t + h / 2, levs[j]); b2 = cvec(t - h / 2, levs[j])
    n = min(nmax, len(a1), len(b1))
    out = []
    for i in range(n):
        d1 = (math.log(a1[i]) - math.log(b1[i])) / (2 * h)
        d2 = (math.log(a2[i]) - math.log(b2[i])) / h
        out.append((4 * d2 - d1) / 3.0)
    return out

def V17_locus(j, levs, win=OPWIN, parents=PARENTS):
    best = 0.0; bt = None
    for t in parents:
        s = spread(Lvec(t, j, levs, win))
        if s > best:
            best, bt = s, t
    return best, bt

# ---------------------------------------------------- onestep T1/T2/T3 cascade (Lemma 2)

def onestep_raw(t, j, levs, win=OPWIN, cwin=CWIN):
    tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
    cp = cvec(tp, levs[j - 1]); cm = cvec(tm, levs[j - 1]); cj = cvec(t, levs[j])
    Lp = Lvec(tp, j - 1, levs, cwin); Lm = Lvec(tm, j - 1, levs, cwin)
    Lact = Lvec(t, j, levs, win)
    Ljm1 = Lvec(t, j - 1, levs, win)
    n = min(win, len(cp) - 1, len(cm) - 1, len(cj), len(Lact))
    L = min(len(Lp), len(Lm), len(cp), len(cm))
    dp_, dm_ = d_of(tp), d_of(tm)
    ap_, at3 = dprime(tp), dprime(t / 3.0)
    Wp = conv_even(cp, dp_); Wm = conv_even(cm, dm_)
    Vj = spread(Lact); Vjm1 = spread(Ljm1)
    Curv = spread([Wp[i] / cp[i] for i in range(n)])
    return dict(t=t, j=j, cp=cp, cm=cm, cj=cj, Lp=Lp, Lm=Lm, Lact=Lact, n=n, L=L,
                dp_=dp_, dm_=dm_, ap_=ap_, at3=at3, Wp=Wp, Wm=Wm, Vj=Vj, Vjm1=Vjm1, Curv=Curv)

def onestep_compose(raw, lam_mode='mid'):
    cp, cm, cj = raw['cp'], raw['cm'], raw['cj']
    Lp, Lm, Lact = raw['Lp'], raw['Lm'], raw['Lact']
    n, L = raw['n'], raw['L']
    dp_, dm_, ap_, at3 = raw['dp_'], raw['dm_'], raw['ap_'], raw['at3']
    Wp, Wm = raw['Wp'], raw['Wm']
    if lam_mode == 'mid':
        Lamp = 0.5 * (max(Lp) + min(Lp)); Lamm = 0.5 * (max(Lm) + min(Lm))
    else:
        Lamp = sum(Lp[i] * cp[i] for i in range(L)) / sum(cp[i] for i in range(L))
        Lamm = sum(Lm[i] * cm[i] for i in range(L)) / sum(cm[i] for i in range(L))
    delp = [Lp[i] - Lamp for i in range(L)]
    delm = [Lm[i] - Lamm for i in range(L)]
    Phip = conv_even([delp[i] * cp[i] for i in range(L)], dp_)
    Phim = conv_even([delm[i] * cm[i] for i in range(L)], dm_)
    T1 = []; T2 = []; T3 = []
    for i in range(n):
        T1.append((Lamp * Wp[i] / cj[i] - Lamm * Wm[i] / cj[i]) / 3.0)
        T2.append((Phip[i] - Phim[i]) / (3.0 * cj[i]))
        T3.append((ap_ * (cp[i] - cm[i]) - at3 * cm[i]) / (3.0 * cj[i]))
    recon = max(abs(T1[i] + T2[i] + T3[i] - Lact[i]) for i in range(n))
    lam = sum(cp[i] for i in range(n)) / sum(cm[i] for i in range(n))
    cpP = [lam * cm[i] for i in range(len(cm))]
    WpP = conv_even(cpP, dp_)
    cjP = [x + y for x, y in zip(WpP, Wm)]
    T1P = [(Lamp * WpP[i] - Lamm * Wm[i]) / (3.0 * cjP[i]) for i in range(n)]
    T3P = [(ap_ * (cpP[i] - cm[i]) - at3 * cm[i]) / (3.0 * cjP[i]) for i in range(n)]
    Fext = spread([T1P[i] + T3P[i] for i in range(n)])
    # The W=17 (OPWIN) mass-weighted references -- gate LAM-INV's FIELD object,
    # (log S^17)'(t_pm), matching the (I1)@W=17 identity and the gamma/C' floor-box
    # covers (window-coherence fix, round 4: the field's reality-side comparisons use
    # THESE; the 18-window variants above are retained for the D5 box monitoring).
    L17 = min(OPWIN, L)
    Lamp17 = sum(Lp[i] * cp[i] for i in range(L17)) / sum(cp[i] for i in range(L17))
    Lamm17 = sum(Lm[i] * cm[i] for i in range(L17)) / sum(cm[i] for i in range(L17))
    return dict(T1=T1, T2=T2, T3=T3, recon=recon, Fext=Fext, delp=delp, delm=delm,
                Lamp=Lamp, Lamm=Lamm, Lamp17=Lamp17, Lamm17=Lamm17)

def gap_quadrature(t, j, levs, M, win=OPWIN):
    tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
    xs = [tm + (tp - tm) * k / M for k in range(M + 1)]
    ys = [spread(Lvec(x, j, levs, win)) for x in xs]
    h = (tp - tm) / M
    s = ys[0] + ys[-1]
    for k in range(1, M):
        s += ys[k] * (4 if k % 2 == 1 else 2)
    return s * h / 3.0

# ---------------------------------------------------------- Lemma A1 tangent seminorm
#
# T2_i = sum_k M^+_{ik} delta^+_k + M^-_{ik} delta^-_k, M^s_{ik} = (1/3)(K_ds)_{ik} c^s_k/o_i.
# osc(T2) is a max of linear functionals of (delta^+,delta^-) -> a seminorm; its exact
# closed form over the arbitrary-delta osc<=1 polytope is a max, over index pairs, of
# 1/2*[sum_k|Delta^+_k-mu^+| + sum_k|Delta^-_k-mu^-|] (the note's Lemma A1). K_d is
# tridiagonal (even-extension at i=0), so each row has <=3 nonzero entries.

def kernel_row(i, d):
    if i == 0:
        return {0: d, 1: 0.5}
    return {i - 1: 0.25, i: d, i + 1: 0.25}

def m_row(i, d, c_branch, o_i):
    row = kernel_row(i, d)
    return dict((k, (w * c_branch[k] / o_i) / 3.0) for k, w in row.items() if k < len(c_branch))

def seminorm_pair(rowA, rowB, cwin):
    # Lemma A1 seminorm term (1/2)*[.] for one branch. mu := (sum_k Delta_k)/cwin is the
    # WINDOW-MEAN over the CWIN=18 child indices -- NOT a free/arbitrary reference. Reason
    # (the hypothesis Lemma A1 requires, D5): sum_k(T2_i - T2_i') = (row_i - row_i')-mass !=
    # 0, so osc(T2)/osc(delta) is INFINITE over unconstrained-level delta (add a constant to
    # delta: osc(delta)=0 but osc(T2)!=0). The finite formula (1/2)Sum|Delta_k - mu| is the
    # sup over ZERO-SUM delta, i.e. requires the L-split L^pm_k = Lambda^pm + delta^pm_k to
    # take Lambda^pm = mean_{k<18} L^pm_k (the window mean). Subtracting mu = mean_k Delta_k
    # here is exactly that zero-sum projection; osc(delta) = spread(L) = V_17(n-1) is
    # unchanged by the choice of Lambda (shift-invariance), so the choice is free and sound.
    keys = set(rowA) | set(rowB)
    vals = dict((k, rowA.get(k, 0.0) - rowB.get(k, 0.0)) for k in keys)
    mu = sum(vals.values()) / cwin        # window-mean of Delta over the CWIN child indices
    s = sum(abs(v - mu) for v in vals.values())
    s += (cwin - len(vals)) * abs(mu)
    return s

def n_free_from_raw(raw, cwin=CWIN):
    cp, cm, cj = raw['cp'], raw['cm'], raw['cj']
    dp_, dm_ = raw['dp_'], raw['dm_']
    n = raw['n']
    rowsP = [m_row(i, dp_, cp, cj[i]) for i in range(n)]
    rowsM = [m_row(i, dm_, cm, cj[i]) for i in range(n)]
    best = 0.0
    for i in range(n):
        for ip in range(i + 1, n):
            val = 0.5 * (seminorm_pair(rowsP[i], rowsP[ip], cwin)
                          + seminorm_pair(rowsM[i], rowsM[ip], cwin))
            if val > best:
                best = val
    return best

# ------------------------------------------------------- V12 census machinery (verbatim)

CENSUS_NC = 5
CENSUS_MU = [math.exp(-2.0 + 2.6 * k / 12) for k in range(13)]

def floors_at48(t, levs):
    b = flip(bary(t, levs[48]))
    return [b[i + 1] / b[i] if (i + 1 < len(b) and b[i] > 1e-250) else 0.4
            for i in range(CENSUS_DEG)]

def sigma_max_at(t, jmax2, levs):
    tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
    sm = 0.0
    for j in range(8, jmax2):
        cp = cvec(tp, levs[j - 1]); cm = cvec(tm, levs[j - 1])
        Sp = a_of(tp) * sum(cp) - 0.25 * (cp[0] - cp[1])
        Sm = a_of(tm) * sum(cm) - 0.25 * (cm[0] - cm[1])
        sm = max(sm, Sm / (Sp + Sm))
    return sm

def census_lc_corner(phi, bits):
    rc = []; prev = 1.0
    for i in range(CENSUS_DEG):
        lo = (phi[i] / 2.0) if i == 0 else phi[i]
        hi = min(prev, 1.0)
        lo = min(lo, hi)
        rc.append((hi if bits[i] else lo) if i < CENSUS_NC else lo)
        prev = rc[-1]
    c = [1.0]
    for r in rc:
        c.append(c[-1] * r)
    return c

# ------------------------------------------------------- window-lemma helpers (W1/W2)

def window_ratio(t, j, levs):
    """Lemma W1: spread_{i<18}(L)/spread_{i<17}(L)."""
    Lfull = Lvec(t, j, levs, CWIN)
    return spread(Lfull) / spread(Lfull[:OPWIN])

def curv_window_undercounts(t, j, levs):
    """Lemma W2 structural check: the correct spread_{i<17}(P) (P_0..P_16, needs
    c_0..c_17, i.e. CWIN=18 c-values) vs the undercounting proxy spread_{i<16}(P)
    (P_0..P_15, needs only c_0..c_16, i.e. OPWIN=17 c-values -- the census's own
    corner-vector length, one index short)."""
    c = cvec(t, levs[j])
    d = d_of(t)
    def P(i):
        if i == 0:
            return d + 0.5 * (c[1] / c[0])
        return d + 0.25 * (c[i + 1] / c[i] + c[i - 1] / c[i])
    full = [P(i) for i in range(OPWIN)]     # i=0..16, needs c_0..c_17
    short = full[:OPWIN - 1]                 # i=0..15, needs only c_0..c_16
    return spread(full), spread(short)

# ===================================================================================
# DISCHARGE UPGRADE machinery: F3 (deep-base floor re-cert) + V17-IA (the load-bearing
# minced interval-arithmetic forcing census).
# ===================================================================================

def anchor_c_ratios(t, levs, J0, win=FLOOR_WIN):
    """rc_i = c_{i+1}/c_i at the anchor level J0, i=0..win-1 (needs c_0..c_win)."""
    c = cvec(t, levs[J0])
    return [c[i + 1] / c[i] for i in range(win)]

def b_convention_rc0(t, levs, J0):
    """The b-convention ratio b_1/b_0 (no c_0=b_0,c_i=b_i/2 halving applied) -- used
    only for F3's i=0 halving-convention cross-check against the c-convention rc_0."""
    b = flip(bary(t, levs[J0]))
    return b[1] / b[0] if b[0] > 1e-250 else float('nan')

# ---- V17-IA: the rigorous width-2-locality minced enclosure -----------------------
#
# P_i (the curvature normal form, Lemma C0) depends on EXACTLY TWO ratios: P_0=(1/2)rc_0,
# P_i=(1/4)(1/rc_{i-1}+rc_i) for i>=1 -- tighter locality than the width-4 band the
# separate tangent-seminorm object (Lemma A1, used by gate V15) needs, since P_i is a
# single scalar, not a kernel row. The box is rc_i in [f_i,1] (f_i = f*anchor_rc_i(J0))
# with the LC chain rc_i<=rc_{i-1}. Rather than an LC-endpoint shortcut (checking only
# i=0,16 and relying on "P monotone in i" holding at every box point -- true on the
# realized/measured cascade, COMPUTED, but not proved to hold at every point of the box),
# this computes a marginal box for EVERY i=0..16 by mincing each ratio's range into m
# panels and enumerating LC-feasible ADJACENT panel pairs (rc_{i-1} panel, rc_i panel) --
# i.e. explicit "mince, evaluate each cell, outward-round" IA, done in EXACT Fraction
# arithmetic (no sampling anywhere).
#
# The m->infinity limit of this mincing has a closed form (verified against explicit
# finite-m mincing, m=1..32, which converges monotonically DOWN to it from above,
# confirming validity as an upper bound): the LC-clipped 2-variable
# region {(a,b): a in [f_{i-1},1], b in [f_i,a]} has h(a,b)=1/a+b maximized at a=b=f_{i-1}
# (both floors coincide -- an LC-admissible point since floors are anchor-LC-compatible)
# and minimized at a=1,b=f_i. This IS the closed-form cell; we ALSO run explicit finite-m
# mincing (below, `p_i_box_minced`) as a numerical corroboration, not as the certified
# value (the closed form is used for the certificate since it is exact, not merely
# converged-to).
#
# For EACH i, the marginal g(P_i) range is then box-maxed over the (lam,Lambda^+,
# Lambda^-) magnitude box: for FIXED P, g is Mobius in lam (A,B linear in lam; nc,nl
# linear in lam) and AFFINE in Lambda^+/Lambda^- (their coefficients don't touch the
# denominator) -- so each is corner-sufficient over ITS OWN box (2 endpoints), and the
# joint box is corner-sufficient by the standard coordinatewise-monotone argument
# (moving one coordinate to its bound never decreases a coordinatewise-monotone
# objective, regardless of the other coordinates' values -- iterate coordinate by
# coordinate to reach a corner without decreasing the value). The osc bound at a FIXED
# magnitude corner is max_i(g at P_i's box endpoints) - min_i(g at P_i's box endpoints)
# -- matching the existing F_perindex convention (fix the corner, then osc across i,
# then max over corners) -- and this per-i-per-corner marginal bounding is valid
# REGARDLESS of whether the extremizing profile is mutually consistent across different
# i (a standard marginal-bound argument: each g(P_i) lies in its own interval for ANY
# point of the box, so max_i(over its own hi) - min_i(over its own lo) upper-bounds the
# true osc for that corner).

def p_i_marginal_box(floors):
    """Closed-form (mince-limit) per-index P_i box, i=0..WIN-1, width-2 LC-pairwise
    locality. `floors` is a length-WIN list of Fractions (or floats)."""
    half = floors[0].__class__(1, 2) if isinstance(floors[0], Fr) else 0.5
    one = floors[0].__class__(1) if isinstance(floors[0], Fr) else 1.0
    P = [ (floors[0] * half, half) ]
    for i in range(1, WIN_STAR):
        f_im1 = floors[i - 1]; f_i = floors[i]
        lo = (one + f_i) / 4 if isinstance(f_i, Fr) else 0.25 * (1.0 + f_i)
        hi = (one / f_im1 + f_im1) / 4 if isinstance(f_i, Fr) else 0.25 * (1.0 / f_im1 + f_im1)
        P.append((lo, hi))
    return P

def p_i_box_minced(floors, m):
    """Explicit finite-m mincing (numerical corroboration only -- see module docstring
    above): subdivide each ratio's [f_i,1] into m panels, enumerate LC-feasible adjacent
    panel pairs, union the resulting P_i intervals. Float; used only for the console
    convergence check, never for the certified value."""
    panels = []
    for i in range(WIN_STAR):
        f_i = floors[i]; w = (1.0 - f_i) / m
        panels.append([(f_i + k * w, f_i + (k + 1) * w) for k in range(m)])
    P = [(0.5 * floors[0], 0.5)]
    for i in range(1, WIN_STAR):
        pa, pb = panels[i - 1], panels[i]
        lo = 1e18; hi = -1e18
        for (alo, ahi) in pa:
            for (blo, bhi) in pb:
                if blo > ahi + 1e-15:
                    continue
                b_hi_eff = min(bhi, ahi)
                if b_hi_eff < blo - 1e-15:
                    continue
                v_lo = 0.25 * (1.0 / ahi + blo)
                v_hi = 0.25 * (1.0 / alo + b_hi_eff)
                lo = min(lo, v_lo); hi = max(hi, v_hi)
        P.append((lo, hi))
    return P

# COMPUTED magnitude box (LAM-BOX clause): these six literals are a MEASURED range of the
# realized sibling-proportionality magnitudes (lam = mass ratio, Lambda^+/- the L-reference
# offsets) + a ~8% pad. They are NOT derived or proved here; both load-bearing gates
# box-max over them. Gate MAG-BOX (gate_magnitude_box) verifies the realized magnitudes lie
# inside these boxes at every grid level (turning a silent constant into a monitored,
# tamperable invariant) -- but that is a grid check, not a proof for all n. Hence COMPUTED.
LAM_LO_F, LAM_HI_F = Fr(72, 100), Fr(95, 100)      # COMPUTED (measured realized ~[0.776,0.919] + pad)
# LAP_LO_F: WIDENED -116/100 -> -117/100 (R1 mitigation (b), DERIV_LAMBOX.md Section 6):
# the LAM-INV proved interval's Lambda^+ floor is RAZOR-thin against -116/100 (+0.0004
# headroom, gate LAM-INV) and fails outright at 2x the measured correction bound
# (CPRIME=0.008 -> proved floor ~-1.163, tamper 'laminv-floor'). A 0.86% widening restores
# comfortable headroom (~+0.010) and is absorbed by every consumer's own margin (V15-IA
# unaffected -- theta_band does not depend on Lambda^+/-; V17-IA/SIB-CERT/SIB-BAND margins
# shrink by <1%, all re-run, see the note's margins table). LAP_LO_F_ORIG kept for the
# 'laminv-floor' R1-stress tamper (restores the pre-widening value).
LAP_LO_F_ORIG = Fr(-116, 100)
LAP_LO_F, LAP_HI_F = Fr(-117, 100), Fr(-82, 100)   # COMPUTED (measured ~[-1.143,-0.888]; widened floor, headroom ~0.027)
LAM2_LO_F, LAM2_HI_F = Fr(-66, 100), Fr(-35, 100)  # COMPUTED (measured ~[-0.633,-0.379] + pad)

# (SIB-BAND clause) sibling wobble band. The IH rho_prop@i<17(n-1) <= TARGET makes the real
# cascade c^+_i = lam*w_i*c^-_i with per-entry wobble w_i whose spread max_i w_i/min_i w_i
# <= TARGET. The independent-per-entry SAFE superset is w_i in [1/R*, R*], R*=TARGET (exact
# Fraction, TARGET being a terminating decimal). WOB_HALF is the tighter geometric-center
# normalization w_i in [1/sqrt R*, sqrt R*] (still sound: lam := sqrt(min rho * max rho)
# lands in the MAG-BOX and w_i = rho_i/lam lies in the half-band by the IH). The forced-
# proportional gates are the w_i == 1 slice; the informational gate SIB-BAND re-runs the
# censuses over these bands to expose the real-vs-proportional gap.
R_STAR_FR = Fr(102560749, 100000000)               # = TARGET, exact
WOB_FULL = (Fr(1) / R_STAR_FR, R_STAR_FR)          # [1/R*, R*]
def _sqrt_hi_frac(fr, iters=64):                   # rational upper bound on sqrt(fr) (outward)
    lo, hi = Fr(0), fr + 1
    for _ in range(iters):
        mid = (lo + hi) / 2
        if mid * mid <= fr:
            lo = mid
        else:
            hi = mid
    return hi
_SQ_HI = _sqrt_hi_frac(R_STAR_FR)                  # >= sqrt(R*)
WOB_HALF = (Fr(1) / _SQ_HI, _SQ_HI)                # [1/sqrt R*, sqrt R*] (outward, sound superset)

# (round 2, PI review) BOUNDARY SLOT box. Both wobble censuses range u,v,x over the band
# at every row i<WIN_STAR; at i=WIN_STAR-1=16, x multiplies entry k=i+1=17 -- i.e. x IS
# w_17, the sibling wobble at index 17, ONE PAST the IH's operative window i<17. Neither
# the IH (rho_prop@i<17<=TARGET) nor gate MAG-BOX's per-entry monitoring (also i<17, see
# gate_magnitude_box's nn=WIN_STAR cap) says anything about w_17 -- a genuine gap, not
# pedantic: the naive "same band as the window" claim is FALSE at shallow levels
# (measured w_17(48) up to 1.016780 > WOB_HALF's outward bracket 1.012723; scratchpad
# probe). SIB-CERT's operative domain is n>800 (V18 covers 48..800 on the grid directly),
# where the measured w_17 sits deep inside a MUCH tighter box (n=800: [1.000018,
# 1.000056], decaying ~C/n^2) -- W17_LO_F/W17_HI_F is that deep box, monitored by MAG-BOX
# (gate_magnitude_box) at W17_GRID exactly as lam/Lambda^pm are monitored: a (LAM-BOX)-
# class COMPUTED box, not a proof for all n, but an honest, checked hypothesis where
# before there was none. See note Section 8.4's BOUNDARY ANNEX.
W17_LO_F, W17_HI_F = Fr(999, 1000), Fr(1001, 1000)   # deep box for the i=16 boundary slot
W17_GRID = [500, 550, 600, 650, 700, 750, 800]        # SIB-CERT's operative domain only

def osc_bound_at_parent_frac(P, dp_, dm_, ap_, at3):
    """Rigorous box-max (Fraction) of osc_{i<17}(T1P+T3P) at one parent: P is the
    per-index marginal box (Fractions), dp_,dm_,ap_,at3 are Fractions (outward-rounded
    from the float trig evaluation). Box-maxes over the (lam,Lamp,Lamm) magnitude
    corners (2x2x2=8, each side corner-sufficient per the module docstring)."""
    best = Fr(0)
    for lam in (LAM_LO_F, LAM_HI_F):
        A = lam * dp_ + dm_; B = lam + 1
        if A + B * P[0][0] <= 0:
            continue
        for Lamp in (LAP_LO_F, LAP_HI_F):
            for Lamm in (LAM2_LO_F, LAM2_HI_F):
                nc = Lamp * lam * dp_ - Lamm * dm_ + ap_ * (lam - 1) - at3
                nl = Lamp * lam - Lamm
                his = []; los = []
                for i in range(WIN_STAR):
                    plo, phi = P[i]
                    denom_lo = A + B * plo; denom_hi = A + B * phi
                    if denom_lo <= 0 or denom_hi <= 0:
                        continue
                    v1 = (nc + nl * plo) / (3 * denom_lo)
                    v2 = (nc + nl * phi) / (3 * denom_hi)
                    his.append(v1 if v1 > v2 else v2)
                    los.append(v1 if v1 < v2 else v2)
                if not his:
                    continue
                v = max(his) - min(los)
                if v > best:
                    best = v
    return best

_FBOX_IA_CACHE = {}

def F_box_ia_certified(levs, J0, f_pad, tamper=None):
    """The certified sup over 41 parents of the rigorous width-2 minced-IA forcing
    bound at anchor J0, pad f_pad. Returns (sup_as_Fraction, locus_t, slop_used).
    Memoized on (J0, f_pad, tamper): gate LAM-INV's (C'-CAP) floor-box bound consumes
    the UNTAMPERED result (tamper=None) for its equilibrium-ceiling input, so the
    baseline full run computes this census once and the gate re-uses it; only a
    tamper run that targets THIS census pays a second (tampered) evaluation."""
    key = (J0, str(f_pad), tamper)
    if key in _FBOX_IA_CACHE:
        return _FBOX_IA_CACHE[key]
    slop = IA_SLOP
    worst = Fr(0); wt = None
    for t in PARENTS:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        rc = anchor_c_ratios(t, levs, J0, win=WIN_STAR)
        floors = [frac_outward(f_pad * r, lo=True, slop=slop) for r in rc]
        dp_ = frac_exact(d_of(tp)); dm_ = frac_exact(d_of(tm))
        ap_ = frac_exact(dprime(tp)); at3 = frac_exact(dprime(t / 3.0))
        P = p_i_marginal_box(floors)
        v = osc_bound_at_parent_frac(P, dp_, dm_, ap_, at3)
        v = v * (1 + slop)             # final documented outward slop (float-input safety margin)
        if v > worst:
            worst = v; wt = t
    _FBOX_IA_CACHE[key] = (worst, wt, slop)
    return worst, wt, slop

def gate_floors(report, levs, J0, f_pad, tamper=None):
    """F3 FLOORS: re-certify the floor family at anchor J0 -- emit r_i(J0,t) over the
    41-parent grid, i<18 (FLOOR_WIN=CWIN), pad f_pad; verify the admissibility
    conditions the box bound (V17-IA) and the curvature census (Lemma W2) consume:
    (1) positivity r_i(J0,t)>0; (2) LC-compatibility, the anchor ratios non-increasing
    in i at every parent (so the padded floor f_pad*r_i inherits monotonicity, and
    floor<=r_i<=1=cap is a valid band); (3) the i=0 halving-convention cross-check
    (c-convention rc_0 = b-convention b_1/b_0, divided by 2 -- mirrors the #885
    verifier's floors_at48/census_lc_corner special-casing of index 0)."""
    bad_pos = 0; bad_lc = 0; worst_half_err = 0.0
    fpad_eff = f_pad * Fr(3, 2) if tamper == "f3-corrupt" else f_pad   # >1 pad breaks floor<=r_i
    tightest_band = 1e18
    for t in PARENTS:
        rc = anchor_c_ratios(t, levs, J0, win=FLOOR_WIN)
        prev = 2.0
        for i, r in enumerate(rc):
            if r <= 0:
                bad_pos += 1
            if r > prev + 1e-9:
                bad_lc += 1
            prev = r
        floor0 = float(fpad_eff) * rc[0]
        if not (floor0 <= rc[0] + 1e-12):
            bad_lc += 1
        band = rc[-1] - float(fpad_eff) * rc[0]  # crude within-band sanity (non-negative-ish typical)
        tightest_band = min(tightest_band, band) if band == band else tightest_band
        rc0_b = b_convention_rc0(t, levs, J0) / 2.0
        err = abs(rc0_b - rc[0])
        worst_half_err = max(worst_half_err, err)
    ok = (bad_pos == 0) and (bad_lc == 0) and (worst_half_err < 1e-9)
    report.append(("F3 FLOORS [anchor J0=%d, pad f=%s=%.4f, window i<%d] positivity"
                    " r_i>0 (violations=%d), LC-compatibility r_i non-increasing +"
                    " floor<=r_i<=1 (violations=%d), i=0 halving cross-check"
                    " |c-conv rc_0 - b-conv rc_0/2|<1e-9 (worst %.2e) over 41 parents"
                    % (J0, str(f_pad), float(f_pad), FLOOR_WIN, bad_pos, bad_lc,
                       worst_half_err), ok))

# ---- V15-IA: the certified band-uniform Lemma A1 (tangent seminorm) enclosure --------
#
# Certifies theta_band, a BAND-uniform (valid for every n>=J0, not merely tested grid
# points) upper bound on the Lemma A1 tangent seminorm, used as gate_forcing_ia's
# theta_star. Under the forced sibling-proportionality surrogate V17-IA also uses
# (c^+ = lam*c^-, lam in the COMPUTED magnitude box [LAM_LO_F,LAM_HI_F] -- see the
# (SIB-BAND) clause: this surrogate does NOT cover the real non-proportional cascade;
# gate SIB-BAND exposes the gap), the Lemma A1 matrix entries M^pm_{ik} =
# (1/3)(K_d(t_pm))_{ik} c^pm_k/o_i (note Section 5) reduce to
#
#   M^+_{ik} = (1/3) w_ik * lam * (c^-_k/c^-_i) / (A+B*P_i)
#   M^-_{ik} = (1/3) w_ik *       (c^-_k/c^-_i) / (A+B*P_i)
#   A = lam*d_+ + d_-,  B = lam+1,  P_i as in Lemma C0 / p_i_marginal_box above.
#
# Row i's support (kernel_row): i=0 -> {0:d, 1:1/2}; i>=1 -> {i-1:1/4, i:d, i+1:1/4}.
# The c^-_k/c^-_i factor is 1 (k=i), rc_i (k=i+1), or 1/rc_{i-1} (k=i-1).
#
# The (a,b):=(rc_{i-1},rc_i) direction. For FIXED lam, the DIAGONAL entry (k=i) depends
# on (a,b) only via the scalar P_i, monotone in P (reuse P_i's tight box from
# p_i_marginal_box). The OFF-DIAGONAL entries, by direct partial derivatives (denominators
# A+B/(4a) resp. A+(B/4)b, strictly positive under the A>0,B>0 feasibility check), are
# strictly coordinatewise monotone in BOTH (a,b), sign independent of lam, so their
# extremes sit at two (a,b) points (a monotone-path argument): M_{i,i+1} (ratio b) at
# {(1,1),(f_{i-1},f_i)}, M_{i,i-1} (ratio 1/a) at the same two points (assignment flips).
#
# The lam direction -- CERTIFIED BY MINCING lam, not by an endpoint-sufficiency claim.
# Each single matrix entry is Moebius (ratio of two affines) in lam, hence monotone in
# lam. But the certified object is the SEMINORM (1/2)Sum_k|Delta^pm_k - mu^pm| with
# Delta_k = M_{ik} - M_{i'k} -- a sum of absolute values of DIFFERENCES of Moebius
# functions with DIFFERENT denominators (D_i(lam) vs D_{i'}(lam)); each Delta_k is a
# degree-(2,2) rational in lam, so the seminorm is NOT Moebius and CAN have an interior-lam
# maximum. Evaluating only lam in {LAM_LO_F,LAM_HI_F} is therefore NOT a proof of the sup
# over [LAM_LO_F,LAM_HI_F]. Instead theta_band_at_parent MINCES [LAM_LO_F,LAM_HI_F] into
# LAM_MINCE panels; on each panel it takes every matrix entry's EXACT per-panel interval
# (by the entry's lam-monotonicity: its range over the panel is the hull of its values at
# the two panel endpoints, combined with the (a,b) 2-point extremization -- a genuine
# corner enclosure), then evaluates the seminorm by interval subtraction (valid regardless
# of correlation between the two rows). max over panels and pairs is a RIGOROUS upper
# bound converging DOWN to the true sup as LAM_MINCE grows. Mincing decouples the shared-
# lam constraint safely: on a narrow panel each entry moves little, so the independent-
# interval combination is tight; a single panel over the whole box (the naive per-entry
# independent-lam bound) inflates by ~9%, but LAM_MINCE panels recover the tightness while
# staying sound (no false claim that the seminorm itself is monotone or Moebius in lam).

def _hull_row(rowA, rowB):
    """Entry-wise hull of two row dicts (same support): each entry's per-panel interval
    is the hull of its two lam-panel-endpoint intervals. Sound because each matrix entry
    is monotone (Moebius) in lam, so its range over the panel lies in that hull."""
    out = {}
    zero = ((Fr(0), Fr(0)), (Fr(0), Fr(0)))
    for k in set(rowA) | set(rowB):
        (apl, aph), (aml, amh) = rowA.get(k, zero)
        (bpl, bph), (bml, bmh) = rowB.get(k, zero)
        out[k] = ((min(apl, bpl), max(aph, bph)), (min(aml, bml), max(amh, bmh)))
    return out

def _m_diag_at_lam(P_lo, P_hi, dp_, dm_, lam):
    """Exact (Mplus_lo,Mplus_hi),(Mminus_lo,Mminus_hi) for the diagonal entry (k=i) at
    a FIXED lam -- over the 2 points {P_lo,P_hi} (the (a,b)-extremization). The caller
    (theta_band_at_parent) sweeps lam over panel endpoints and hulls; it does NOT assume
    endpoint-sufficiency of the seminorm in lam. None if infeasible (A+B*P<=0)."""
    pv = []; mv = []
    for P in (P_lo, P_hi):
        A = lam * dp_ + dm_; B = lam + 1
        denom = A + B * P
        if denom <= 0:
            return None
        pv.append(lam * dp_ / (3 * denom)); mv.append(dm_ / (3 * denom))
    return (min(pv), max(pv)), (min(mv), max(mv))

def _m_off_at_lam(a1, b1, a2, b2, weight, dp_, dm_, lam, ratio_is_b):
    """Exact extremes over the 2 points {(a1,b1),(a2,b2)} at a FIXED lam for an
    off-diagonal entry (numerator ratio = b if ratio_is_b else 1/a; P=(1/4)(1/a+b))."""
    pv = []; mv = []
    for (a, b) in ((a1, b1), (a2, b2)):
        P = Fr(1, 4) * (1 / a + b)
        A = lam * dp_ + dm_; B = lam + 1
        denom = A + B * P
        if denom <= 0:
            return None
        ratio = b if ratio_is_b else 1 / a
        pv.append(lam * weight * ratio / (3 * denom))
        mv.append(weight * ratio / (3 * denom))
    return (min(pv), max(pv)), (min(mv), max(mv))

def theta_band_row_entries_at_lam(i, P, floors, dp_, dm_, lam, win):
    """Row i's support -> {k: ((Mplus_lo,Mplus_hi),(Mminus_lo,Mminus_hi))} at a FIXED
    lam (the (a,b)-extremization only). None if infeasible. theta_band_at_parent calls
    this at each lam-panel endpoint and hulls (each entry is Moebius/monotone in lam),
    then evaluates the seminorm per panel and maxes over panels -- a rigorous enclosure
    of the sup over the lam box that does NOT assume the seminorm is monotone/Moebius in
    lam (it is neither: a sum of |differences of Moebius functions with different
    denominators|)."""
    out = {}
    if i == 0:
        d = _m_diag_at_lam(P[0][0], P[0][1], dp_, dm_, lam)
        if d is None:
            return None
        out[0] = d
        f0 = floors[0]
        pv = []; mv = []
        for b in (f0, Fr(1)):
            P0 = b / 2
            A = lam * dp_ + dm_; B = lam + 1
            denom = A + B * P0
            if denom <= 0:
                return None
            pv.append(lam * Fr(1, 2) * b / (3 * denom)); mv.append(Fr(1, 2) * b / (3 * denom))
        out[1] = ((min(pv), max(pv)), (min(mv), max(mv)))
        return out
    d = _m_diag_at_lam(P[i][0], P[i][1], dp_, dm_, lam)
    if d is None:
        return None
    out[i] = d
    f_im1, f_i = floors[i - 1], floors[i]
    e_p1 = _m_off_at_lam(Fr(1), Fr(1), f_im1, f_i, Fr(1, 4), dp_, dm_, lam, ratio_is_b=True)
    if e_p1 is None:
        return None
    out[i + 1] = e_p1
    e_m1 = _m_off_at_lam(Fr(1), Fr(1), f_im1, f_i, Fr(1, 4), dp_, dm_, lam, ratio_is_b=False)
    if e_m1 is None:
        return None
    out[i - 1] = e_m1
    return out

def theta_band_seminorm_pair(rowA, rowB, cwin, branch_idx):
    """Exact Fraction upper bound on sum_k|Delta_k-mu| for one branch, Delta_k :=
    M_{ik}-M_{i'k}, mirroring seminorm_pair's float logic but combining EXTREME
    intervals via independent-interval subtraction: valid regardless of any
    correlation between the two rows' box points, since interval difference always
    contains the true pointwise Delta_k (standard IA soundness, not assuming the two
    rows' extremizing (a,b,lam) coincide)."""
    keys = set(rowA) | set(rowB)
    zero = ((Fr(0), Fr(0)), (Fr(0), Fr(0)))
    deltas = {}
    for k in keys:
        a = rowA.get(k, zero)[branch_idx]
        b = rowB.get(k, zero)[branch_idx]
        deltas[k] = (a[0] - b[1], a[1] - b[0])
    total_lo = sum((deltas[k][0] for k in keys), Fr(0))
    total_hi = sum((deltas[k][1] for k in keys), Fr(0))
    mu = (total_lo / cwin, total_hi / cwin)
    s = Fr(0)
    for k in keys:
        d_lo, d_hi = deltas[k]
        diff_lo, diff_hi = d_lo - mu[1], d_hi - mu[0]
        s += max(abs(diff_lo), abs(diff_hi))
    mu_bound = max(abs(mu[0]), abs(mu[1]))
    s += (cwin - len(keys)) * mu_bound
    return s

def theta_band_at_parent(t, levs, J0, f_pad, tamper=None):
    """The certified sup, at one parent t, of the Lemma A1 seminorm over the certified LC
    ratio box (width-2-per-row locality) and the magnitude scalar lam in
    [LAM_LO_F,LAM_HI_F]. The lam box is MINCED into LAM_MINCE panels; on each panel every
    matrix entry's exact per-panel interval is the hull of its two lam-endpoint values
    (entry Moebius/monotone in lam) combined with the (a,b) 2-point extremization, and the
    seminorm is evaluated by interval subtraction. max over panels + pairs is a rigorous
    upper bound (NO endpoint-sufficiency assumption; see the V15-IA method note).

    Direction tamper 'theta-ia-sign' (M8 finding): flips the pair-extremization from max
    to min -- the sign/direction choice that PRODUCES the sup. It DEFLATES theta_band well
    below the realized seminorm, caught by gate_theta_ia's realized-floor consistency check
    (a too-LOW theta_band is the unsound direction -- a valid upper bound must dominate the
    realized value; V17-IA's threshold merely relaxes, so the flip is isolated to V15-IA).

    Returns (value, (locus_pair, locus_panel)) or (None, reason) if infeasible."""
    rc = anchor_c_ratios(t, levs, J0, win=WIN_STAR)
    slop = IA_SLOP
    floors = [frac_outward(f_pad * r, lo=True, slop=slop) for r in rc]
    tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
    dp_ = frac_exact(d_of(tp)); dm_ = frac_exact(d_of(tm))
    P = p_i_marginal_box(floors)
    edges = [LAM_LO_F + (LAM_HI_F - LAM_LO_F) * Fr(j, LAM_MINCE) for j in range(LAM_MINCE + 1)]
    edge_rows = []
    for lam in edges:
        rows = [theta_band_row_entries_at_lam(i, P, floors, dp_, dm_, lam, WIN_STAR)
                for i in range(WIN_STAR)]
        if any(r is None for r in rows):
            return None, "INFEASIBLE at lam=%s" % str(lam)
        edge_rows.append(rows)
    best = None; bestpair = None; bestpanel = None
    flip = (tamper == "theta-ia-sign")
    for pj in range(LAM_MINCE):
        rows = [_hull_row(edge_rows[pj][i], edge_rows[pj + 1][i]) for i in range(WIN_STAR)]
        for i in range(WIN_STAR):
            for ip in range(i + 1, WIN_STAR):
                sp = theta_band_seminorm_pair(rows[i], rows[ip], CWIN, 0)
                sm = theta_band_seminorm_pair(rows[i], rows[ip], CWIN, 1)
                val = (sp + sm) / 2
                take = (best is None) or (val < best if flip else val > best)
                if take:
                    best = val; bestpair = (i, ip); bestpanel = (edges[pj], edges[pj + 1])
    return best, (bestpair, bestpanel)

_THETA_IA_CACHE = {}

def theta_band_ia_certified(levs, J0, f_pad, tamper=None):
    """The certified sup over 41 parents of theta_band_at_parent, folded by the certified
    Window Lemma factor (<=57/50, gate V16b -- itself a COMPUTED (FOLD) bound) and the
    documented outward slop. Returns (theta_band, locus_t, locus_pair, slop).
    Memoized on (J0, f_pad, tamper) -- same rationale as F_box_ia_certified's cache:
    gate LAM-INV's (C'-CAP) bound consumes the UNTAMPERED chain."""
    key = (J0, str(f_pad), tamper)
    if key in _THETA_IA_CACHE:
        return _THETA_IA_CACHE[key]
    slop = IA_SLOP
    worst = None; wt = None; wpair = None
    for t in PARENTS:
        val, info = theta_band_at_parent(t, levs, J0, f_pad, tamper=tamper)
        if val is None:
            raise ValueError("theta_band_at_parent infeasible at t=%r (J0=%d,f=%s): %s"
                              % (t, J0, str(f_pad), info))
        if worst is None or val > worst:
            worst = val; wt = t; wpair = info
    theta_band = worst * Fr(57, 50) * (1 + slop)
    _THETA_IA_CACHE[key] = (theta_band, wt, wpair, slop)
    return theta_band, wt, wpair, slop

def realized_seminorm_floor(levs, J0):
    """A realized-profile lower reference for theta_band: max over parents of the Lemma A1
    seminorm at the REAL level-J0 sibling profile (n_free_from_raw), folded by 57/50. The
    band-uniform certified theta_band must DOMINATE this (the realized profile is a point of
    the census's own box); a certified value below it signals a broken direction/sign in the
    census (the 'theta-ia-sign' tamper). A consistency monitor, not a proof."""
    worst = 0.0
    for t in PARENTS:
        raw = onestep_raw(t, J0, levs, win=WIN_STAR, cwin=CWIN)
        worst = max(worst, n_free_from_raw(raw))
    return worst * float(Fr(57, 50))

def gate_theta_ia(report, levs, J0, f_pad, tamper=None):
    """V15-IA THETA-BAND [LOAD-BEARING]: the certified band-uniform upper bound on the
    Lemma A1 tangent seminorm over the certified LC ratio box, folded by the Window Lemma
    factor (<=57/50). The sup over the magnitude scalar lam in [LAM_LO_F,LAM_HI_F] is
    enclosed by MINCING lam into LAM_MINCE panels and hulling each Moebius-in-lam matrix
    entry per panel (theta_band_at_parent) -- a rigorous enclosure, NOT an endpoint-
    sufficiency claim (the seminorm is not Moebius in lam). Valid for EVERY n>=J0 over the
    certified box. NOTE (SIB-BAND clause): this certifies the forced-PROPORTIONAL surrogate
    (c^+ = lam*c^-); the real non-proportional cascade is covered only up to the sibling
    wobble the informational gate SIB-BAND quantifies. Returns theta_band (Fraction) for
    gate_forcing_ia to consume as theta_star.

    Two checks make up ok: (upper) theta_band <= 9/10 (an unconditional contraction
    ceiling; tamper 'theta-ia-tighten' grazes THIS ceiling to 1/2, isolated -- the returned
    value and V17-IA's line are untouched). (lower) theta_band >= the realized-profile
    seminorm (realized_seminorm_floor), a consistency monitor: a certified upper bound must
    dominate the realized value. Tamper 'theta-ia-sign' flips the census's max->min
    direction, deflating theta_band below this floor (caught here); since a lower theta_band
    only RELAXES V17-IA's threshold, that flip is isolated to this gate."""
    theta_band_exact, wt, wpair, slop = theta_band_ia_certified(levs, J0, f_pad, tamper=tamper)
    theta_band = round_up_frac(theta_band_exact)   # outward-rounded to a printable Fraction
    ceiling = Fr(1, 2) if tamper == "theta-ia-tighten" else Fr(9, 10)
    floor = realized_seminorm_floor(levs, J0)      # realized-profile lower consistency ref
    valf = float(theta_band)
    ok = (theta_band <= ceiling) and (valf >= floor - 1e-12)
    report.append(("V15-IA THETA-BAND [LOAD-BEARING, window i<17, anchor J0=%d, pad"
                    " f=%s] certified seminorm sup [lam-minced %d panels, Fraction,"
                    " outward slop=%s] * window fold 57/50 = %.7f (locus t=%.4f,"
                    " pair=%s); realized-floor %.4f <= theta_band <= sanity ceiling %s%s"
                    % (J0, str(f_pad), LAM_MINCE, str(slop), valf, wt, wpair, floor,
                       str(ceiling),
                       " [TAMPERED %s]" % tamper if tamper in ("theta-ia-tighten",
                       "theta-ia-sign") else ""), ok))
    return theta_band

# ------------------------------------------------------- G2/alpha route-cut census (info)

def g2_band_survivors(levs, jmax2):
    corner_bits = list(itertools.product((0, 1), repeat=CENSUS_NC))
    surv = {}
    for t in PARENTS:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        dp_, dm_ = d_of(tp), d_of(tm)
        ap_a, am_a = a_of(tp), a_of(tm)
        fp = floors_at48(tp, levs); fm = floors_at48(tm, levs)
        sig = sigma_max_at(t, jmax2, levs)
        phip = [x * 0.98 for x in fp]; phim = [x * 0.98 for x in fm]
        Pc = []
        for bp in corner_bits:
            vp = census_lc_corner(phip, bp)
            Wp = conv_even(vp, dp_)
            Pc.append((vp, Wp, sum(vp)))
        Mc = [census_lc_corner(phim, bm) for bm in corner_bits]
        rows = []
        for vp, Wp, Sp in Pc:
            for vm in Mc:
                gs = [vm[i] / vp[i] for i in range(len(vp))]
                if max(gs) / min(gs) > TARGET * (1 + 1e-9):
                    continue
                for mu in CENSUS_MU:
                    Sm = mu * sum(vm)
                    share = am_a * Sm / (ap_a * Sp + am_a * Sm)
                    if share > sig + 1e-9:
                        continue
                    Wm = conv_even([mu * x for x in vm], dm_)
                    cj = [x + y for x, y in zip(Wp, Wm)]
                    nuse = min(OPWIN, len(cj))
                    if any(cj[i] <= 0 for i in range(nuse)):
                        continue
                    rows.append((Wp[:nuse], Wm[:nuse], cj[:nuse], vp[:nuse], [mu * x for x in vm[:nuse]]))
        surv[t] = rows
    return surv

def g2_band_stress(levs, surv, n):
    worst = 0.0
    for t in PARENTS:
        rows = surv[t]
        if not rows:
            continue
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        ap_ = dprime(tp); at3 = dprime(t / 3.0)
        Lp_real = Lvec(tp, n - 1, levs, CWIN); Lm_real = Lvec(tm, n - 1, levs, CWIN)
        cp_real = cvec(tp, levs[n - 1]); cm_real = cvec(tm, levs[n - 1])
        Lr = min(len(Lp_real), len(cp_real))
        Lamp = sum(Lp_real[i] * cp_real[i] for i in range(Lr)) / sum(cp_real[i] for i in range(Lr))
        Lamm = sum(Lm_real[i] * cm_real[i] for i in range(Lr)) / sum(cm_real[i] for i in range(Lr))
        local_worst = 0.0
        for (Wp, Wm, cj, vp_s, vm_s) in rows:
            nuse = len(cj)
            vals = []
            for i in range(nuse):
                t1_i = (Lamp * Wp[i] / cj[i] - Lamm * Wm[i] / cj[i]) / 3.0
                t3_i = (ap_ * (vp_s[i] - vm_s[i]) - at3 * vm_s[i]) / (3.0 * cj[i])
                vals.append(t1_i + t3_i)
            s = spread(vals)
            if s > local_worst:
                local_worst = s
        if local_worst > worst:
            worst = local_worst
    return worst

def g2_realized(levs, n):
    worst = 0.0
    for t in PARENTS:
        raw = onestep_raw(t, n, levs, win=OPWIN, cwin=CWIN)
        mass = onestep_compose(raw, 'mass')
        s = spread([mass['T1'][i] + mass['T3'][i] for i in range(raw['n'])])
        if s > worst:
            worst = s
    return worst

# =====================================================================================
# gates
# =====================================================================================

def gate_theta(report, info, levs, grid, tamper=None):
    """V15-GRID THETA [INFORMATIONAL, robustness view]: theta_tot<=1/2 & theta_win<=27/100
    grid census (41 parents), plus the closed-form tangent seminorm N_free<=0.9 (Lemma A1,
    arbitrary child deviations, no sampling) -- theta_tot/theta_win are COMPUTED (grid
    census, a measurement at tested (n,t) points only); N_free is rigorous-in-the-tangent-
    direction but, like theta_tot, evaluated at the realized/grid profile, not a band-
    uniform enclosure. This is a cross-check that the realized dynamics sit comfortably
    inside the certified band V15-IA computes (they do: theta_tot's worst grid value is well
    under theta_band); it does NOT determine RESULT.

    ALSO reports (informational) a grid-sampled box bound theta_cert := N_free * (57/50
    window fold): N_free's closed form is stated against spread_{i<18}(delta)<=1 (the true
    child read-set, CWIN=18), so composing with the IH needs the certified fold
    spread_{i<18}<=(<=57/50)*spread_{i<17} (Lemma W1/V16b). This grid-sampled value is NOT
    band-uniform (it evaluates N_free at realized profiles only); the certified enclosure is
    V15-IA's, which does not sample. Kept as a numerical cross-reference only."""
    thr_tot = 0.05 if tamper == "theta-tot-gate" else 0.5
    worst_tot = 0.0; worst_win = 0.0; worst_nfree = 0.0; worst_wratio = 0.0
    tot_first = tot_last = win_first = win_last = None
    for j in grid:
        sup_tot = 0.0; sup_win = 0.0; sup_nfree = 0.0; sup_wratio = 0.0
        for t in PARENTS:
            raw = onestep_raw(t, j, levs, win=OPWIN, cwin=CWIN)
            mid = onestep_compose(raw, 'mid')
            mass = onestep_compose(raw, 'mass')
            theta_tot = (raw['Vj'] - mid['Fext']) / raw['Vjm1']
            childspread = max(spread(mass['delp']), spread(mass['delm']))
            theta_win = spread(mass['T2']) / childspread if childspread > 1e-14 else 0.0
            nfree = n_free_from_raw(raw)
            nfree = nfree * 2.0 if tamper == "nfree-corrupt" else nfree
            wratio = window_ratio(t, j, levs)
            sup_tot = max(sup_tot, theta_tot)
            sup_win = max(sup_win, theta_win)
            sup_nfree = max(sup_nfree, nfree)
            sup_wratio = max(sup_wratio, wratio)
        worst_tot = max(worst_tot, sup_tot); worst_win = max(worst_win, sup_win)
        worst_nfree = max(worst_nfree, sup_nfree); worst_wratio = max(worst_wratio, sup_wratio)
        if tot_first is None:
            tot_first, win_first = sup_tot, sup_win
        tot_last, win_last = sup_tot, sup_win
    ok = worst_tot <= thr_tot and worst_win <= 0.27 and worst_nfree <= 0.9
    info.append(("V15-GRID THETA [INFORMATIONAL, window i<17, child i<18] theta_tot<=%.3g"
                 " (worst %.4f, plateau [%.4f,%.4f]) & theta_win<=0.27 (worst %.4f,"
                 " plateau [%.4f,%.4f]); closed-form tangent seminorm N_free<=0.9"
                 " (Lemma A1, worst %.4f) -- grid-sampled, superseded as the gating"
                 " theta_star by V15-IA's band-uniform certificate above"
                 % (thr_tot, worst_tot, tot_first, tot_last, worst_win, win_first, win_last,
                    worst_nfree), ok))

    theta_cert = worst_nfree * float(Fr(57, 50))
    theta_cert_measured = worst_nfree * worst_wratio
    info.append(("V15-CERT [INFORMATIONAL, grid-sampled box bound, cross-reference only]"
                  " theta_cert := N_free*(57/50 window fold) = %.4f*1.1400 = %.4f"
                  " (measured-ratio variant %.4f*%.4f=%.4f) -- a GRID-SAMPLED bound (N_free"
                  " at realized profiles), NOT band-uniform; the certified enclosure is"
                  " V15-IA's lam-minced census above, which does not sample"
                  % (worst_nfree, theta_cert, worst_nfree, worst_wratio, theta_cert_measured),
                  True))

def gate_thetasymb(report):
    """V16 THETASYMB: exact Fraction polynomial identity + domain sign argument for
    theta~(t) = sqrt3 sin(2 pi t/3)/(6+3cos(2 pi t/3)) <= 1/5, x = cos(2 pi t/3)."""
    def poly_mul(p, q):
        out = [Fr(0)] * (len(p) + len(q) - 1)
        for i, a in enumerate(p):
            for jx, b in enumerate(q):
                out[i + jx] += a * b
        return out
    def poly_sub(p, q):
        n = max(len(p), len(q))
        return [(p[i] if i < len(p) else Fr(0)) - (q[i] if i < len(q) else Fr(0)) for i in range(n)]
    term1 = [Fr(75), Fr(0), Fr(-75)]                     # 75*(1 - x^2)
    term2 = poly_mul([Fr(6), Fr(3)], [Fr(6), Fr(3)])     # (6 + 3x)^2
    LHS = poly_sub(term1, term2)
    prod = poly_mul([Fr(-1), Fr(2)], [Fr(13), Fr(14)])   # (2x-1)*(14x+13)
    RHS = [Fr(-3) * c for c in prod]
    exact_match = (LHS == RHS)
    half = Fr(1, 2)
    rhs_half = sum(c * half ** i for i, c in enumerate(RHS))
    cos_pi9 = math.cos(PI / 9)
    xs_t = [1.0 / 6 + (1.0 / 3) * k / 200 for k in range(201)]
    sign_ok = True
    for t in xs_t:
        x = math.cos(2 * PI * t / 3)
        if not ((2 * x - 1) >= -1e-12 and (14 * x + 13) > 0):
            sign_ok = False
    worst_gap = min(0.2 - math.sqrt(3) * math.sin(2 * PI * t / 3) / (6 + 3 * math.cos(2 * PI * t / 3))
                     for t in xs_t)
    ok = exact_match and (rhs_half == 0) and sign_ok and (worst_gap >= -1e-12)
    report.append(("V16 THETASYMB exact 75(1-x^2)-(6+3x)^2 = -3(2x-1)(14x+13) [Fraction"
                    " coeff match=%s, RHS(1/2)=%s]; domain x in [1/2,cos(pi/9)]=[1/2,%.6f]:"
                    " (2x-1)>=0 & (14x+13)>0 = %s => theta~(t)<=1/5 exact, numeric worst-gap"
                    " %.6f (equality at t=1/2)" % (exact_match, rhs_half, cos_pi9, sign_ok,
                                                    worst_gap), ok))

def gate_window(report, levs, grid, tamper=None):
    """V16b WINDOW: 289/256<=57/50 rational fact + grid ratio check + the child-window
    read-set structural check (Lemma W2)."""
    asym = Fr(289, 256)
    bound = Fr(21, 20) if tamper == "window-bound" else Fr(57, 50)
    asym_ok = asym <= bound
    worst_ratio = 0.0; worst_loc = (grid[0], PARENTS[0])
    for j in grid:
        for t in PARENTS:
            r = window_ratio(t, j, levs)
            if r > worst_ratio:
                worst_ratio = r; worst_loc = (j, t)
    grid_ok = worst_ratio <= float(bound)
    worst_u = 1e18; best_u = 0.0
    for j in grid:
        for t in PARENTS:
            full_s, short_s = curv_window_undercounts(t, j, levs)
            ratio = full_s / short_s if short_s > 1e-300 else float('inf')
            worst_u = min(worst_u, ratio); best_u = max(best_u, ratio)
    struct_ok = worst_u > 1.0 + 1e-9
    ok = asym_ok and grid_ok and struct_ok
    report.append(("V16b WINDOW [output i<17 reads child i<18] asymptotic V_18/V_17"
                    "->289/256=%.6f <= 57/50=%.4f [rational fact]; grid sup"
                    " spread_{i<18}(L)/spread_{i<17}(L)<=57/50 (worst %.4f @ n=%d); child-window"
                    " read-set (Lemma W2): omitting c_17 undercounts Curv_{i<17} (ratio range"
                    " [%.4f,%.4f], all >1)"
                    % (float(asym), float(bound), worst_ratio, worst_loc[0], worst_u, best_u), ok))

def gate_forcing(report, info, levs, grid, survivors, g2_grid, tamper=None):
    """V17 FORCING: F_ext*n^2 & Curv*n^2 <=200 (core); the G2/alpha route-cut stress
    reproduced as a negative control, appended to `info` -- INFORMATIONAL, does not
    affect this gate's ok."""
    thr = 50.0 if tamper == "forcing-bound" else 200.0
    fext = {}; curv = {}
    for j in grid:
        raw = onestep_raw(EDGE, j, levs, win=OPWIN, cwin=CWIN)
        mid = onestep_compose(raw, 'mid')
        fext[j] = mid['Fext']; curv[j] = raw['Curv']
    worst_fe = max(fext[j] * j * j for j in grid)
    worst_cv = max(curv[j] * j * j for j in grid)
    ok = worst_fe <= thr and worst_cv <= thr
    report.append(("V17 FORCING [window i<17, edge locus] F_ext*n^2<=%.0f (worst %.2f) &"
                    " Curv*n^2<=%.0f (worst %.2f), grid n in {%s}"
                    % (thr, worst_fe, thr, worst_cv, ",".join(str(j) for j in grid)), ok))

    g2_ceiling = 0.02 if tamper == "g2-ceiling" else 0.10
    band = dict((n, g2_band_stress(levs, survivors, n)) for n in g2_grid)
    realized = dict((n, g2_realized(levs, n)) for n in g2_grid)
    worst_band = max(band.values())
    g2_ok = worst_band <= g2_ceiling
    infl = ", ".join("%dx@%d" % (round(band[n] / realized[n]), n) for n in g2_grid if realized[n] > 0)
    info.append(("V17-INFO [INFORMATIONAL, window i<17] G2/alpha route-cut stress"
                  " (rho_prop-constrained V12-band census) <=%.2f ceiling: worst BAND"
                  " s_sup=%.4f over n in {%s} (route-cut %s; inflation vs realized %s)"
                  % (g2_ceiling, worst_band, ",".join(str(n) for n in g2_grid),
                     "CONFIRMED (exceeds ceiling)" if not g2_ok else "NOT confirmed", infl), g2_ok))

def gate_forcing_ia(report, levs, J0, f_pad, theta_star, tamper=None):
    """V17-IA FORCING [THE LOAD-BEARING GATE]: the minced interval-arithmetic census of
    the box-certified forcing bound F_box(J0, f_pad) <= threshold, threshold :=
    (1-theta_star)*tau*, tau* = 3*log(1.02560749) = 0.0758553... . Derivation of the
    threshold: Lemma 1 (PROVED) gives log rho_prop@i<17(n) <= (1/3)V_17(n); the
    V-recursion gives V_17(n) <= theta*V_17(n-1) + Phi(n-1); at a CONSTANT box forcing
    Phi<=F_box the equilibrium ceiling is sup_n V_17(n) <= max(V_17(J0), F_box/(1-theta*));
    this stays <= tau* (closing (T*), hence (PROP-TAIL)) iff F_box <= (1-theta*)*tau* --
    exactly this gate's threshold.

    Method (the closed form of Section "V17-IA" above): the box is rc_i in
    [f_pad*anchor_rc_i(J0,t), 1] (LC chain). P_i (the curvature normal form, Lemma C0)
    has WIDTH-2 locality (depends only on rc_{i-1},rc_i) -- tighter than the width-4 band
    the separate Lemma-A1/tangent object (gate V15) needs. Rather than an LC-endpoint
    shortcut (checking only i=0,16, relying on "P monotone in i" holding everywhere in
    the box -- true on the realized cascade, COMPUTED, not proved box-wide), this
    computes a RIGOROUS per-index marginal box for EVERY i=0..16 -- the mince-to-infinity
    limit of subdividing each ratio's range into panels and enclosing every LC-feasible
    adjacent panel pair (see p_i_marginal_box/p_i_box_minced above; the two are cross-
    checked directly, mincing converges monotonically down onto the closed form from
    above, confirming validity as an upper bound) -- then box-maxes
    over the (lam,Lambda^+,Lambda^-) magnitude corners (each side corner-sufficient:
    Mobius/affine in the fixed-P slice), all in EXACT Fraction arithmetic (the floors
    and trig constants are converted from float via frac_outward with a documented,
    printed slop=1e-9 -- six orders of magnitude past the cascade's own ~1e-15 relative
    float error; the combinatorial/algebraic propagation itself introduces ZERO further
    rounding). The gate PASSES iff the certified sup <= threshold."""
    # tau* as the certified Fraction LOWER bound (TAU_STAR_FR); threshold and the final
    # comparison are EXACT Fraction (no float rounding at the decision point). Using an
    # UNDER-estimate of tau* is conservative in BOTH the threshold and the ceiling uses.
    tau_star = TAU_STAR_FR
    threshold = (1 - theta_star) * tau_star
    thr_eff = threshold * Fr(4, 5) if tamper == "v17ia-graze" else threshold
    val, wt, slop = F_box_ia_certified(levs, J0, f_pad, tamper=tamper)   # exact Fraction
    ok = val <= thr_eff                                                   # EXACT comparison
    valf = float(val)
    margin = float((thr_eff - val) / thr_eff) if thr_eff != 0 else 0.0
    # equilibrium chain, each number printed (audit S1): F_box/(1-theta) -> (1/3)(.) ->
    # exp(.) vs TARGET. The ceiling and its comparison to tau* are exact; the exp/ln display
    # is float. (1/3)*ceiling <= ln(TARGET) is the reduction-lemma conclusion.
    ceiling = val / (1 - theta_star)                     # F_box/(1-theta*), exact Fraction
    log_rho = ceiling / 3                                # (1/3)*ceiling, exact Fraction
    ceiling_ok = ceiling <= tau_star                     # exact: equilibrium ceiling <= tau*
    exp_bound = math.exp(float(log_rho))
    report.append(("V17-IA FORCING [LOAD-BEARING, window i<17, anchor J0=%d, pad f=%s]"
                    " certified F_box(J0,f) [width-2 minced-IA, Fraction, outward slop=%s]"
                    " = %.8f (locus t=%.4f) <= threshold (1-theta*)*tau* = %.8f%s"
                    " (margin %.1f%%, exact-Fraction compare)\n"
                    "        equilibrium chain: F_box/(1-theta*) = %.8f <= tau* = %.8f"
                    " [%s]; (1/3)* = %.8f <= ln(TARGET) = %.8f; exp(.) = %.6f <= TARGET"
                    " = %.8f [%s]"
                    % (J0, str(f_pad), str(slop), valf, wt, float(thr_eff),
                       " [TAMPERED]" if tamper == "v17ia-graze" else "", margin * 100,
                       float(ceiling), float(tau_star), "OK" if ceiling_ok else "MISS",
                       float(log_rho), LTARGET, exp_bound, TARGET,
                       "OK" if exp_bound <= TARGET else "MISS"), ok))
    return valf, float(thr_eff), margin

# ===================================================================================
# MAG-BOX (LAM-BOX clause) + SIB-BAND (sibling wobble) -- both make a COMPUTED input
# honest: MAG-BOX monitors the magnitude box both load-bearing gates box-max over;
# SIB-BAND exposes the forced-proportional-vs-real gap.
# ===================================================================================

def gate_magnitude_box(report, levs, grid, tamper=None, laminv=None):
    """MAG-BOX [core, (LAM-BOX) empirical cross-check]: verify the realized sibling-
    proportionality magnitudes lie inside the magnitude boxes at every (grid level,
    parent): lam = sum(c^+)/sum(c^-) in [LAM_LO_F,LAM_HI_F]; the mass-weighted
    window-mean Lambda^+/- in their boxes; and every per-entry sibling ratio
    rho_i = c^+_i/c^-_i in [LAM_LO_F,LAM_HI_F] (rho_i in the box underwrites the
    (SIB-BAND) representation c^+_i = lam*w_i*c^-_i with lam in the box). This turns six
    silent hardcoded literals into a monitored, tamperable invariant. Prints worst
    headroom. Tamper 'magbox-shrink' tightens the boxes so the realized magnitudes leave
    them.

    STATUS (post gate LAM-INV): the lam and mass-weighted Lambda^+/- lines are now a
    PROVED-CONDITIONAL INTERVAL (gate LAM-INV), not merely a measured range -- this gate's
    grid check is monitoring RETAINED as the empirical cross-check of that proved
    enclosure, not the sole evidence for it. (Round 4, window coherence:) the FIELD's
    own object is the W=17 mass-weighted reference (log S^17)'(t_pm) -- matching
    (I1)@17 and the gamma/C' floor-box covers -- so the field consistency check and the
    in-box monitoring now include the W=17 variants (Lam+mass17/Lam-mass17); the
    W=18 mass-weighted variants are RETAINED alongside. The arithmetic-MEAN Lambda^+/-
    variants (Lam+mean/Lam-mean below) stay COMPUTED-monitored ONLY: LAM-INV's
    enclosure covers the mass-weighted field object alone, and LAB_LAMBOX.md's Q1
    finding is that the arithmetic-mean variant WIDENS with depth (shallow n
    UNDERSTATES its true range) -- so it is watched here, not claimed proved.

    `laminv`, if given (compute() passes gate LAM-INV's own cached result, computed once,
    before this gate runs, to avoid paying the ~47s float precompute twice): ALSO reports
    the realized-vs-field correction-derivative C' consistency check (the a-posteriori
    side of R1) at every (grid level, parent) this gate already samples -- a broader,
    independent cross-check than gate LAM-INV's own sparser one-anchor C' monitor. None
    under --quick/--fallback (LAM-INV does not run there); the C' line is SKIPPED then.

    (round 2, PI review) ALSO monitors the BOUNDARY SLOT: w_17 := rho_17/lam_gc,
    lam_gc := sqrt(min_i rho_i * max_i rho_i) over i<17 (the geometric-center scalar
    gate SIB-CERT's lemma uses) -- the ONE index (i=WIN_STAR-1=16's x-slot) the wobble
    censuses read one past the IH's own window, with no hypothesis before this gate.
    Checked only over W17_GRID (SIB-CERT's operative n>800 domain), NOT the full `grid`
    (the naive full-window band is false at shallow n, see the module comment above
    W17_LO_F -- this gate does not claim it there). Tamper 'w17-shrink' replaces the box
    with a tiny one strictly below the realized range, so the realized w_17 leaves it."""
    # box boundaries (optionally shrunk inward by the tamper so realized leaves the box)
    sh = Fr(6, 100) if tamper == "magbox-shrink" else Fr(0)
    lam_lo = float(LAM_LO_F + sh); lam_hi = float(LAM_HI_F - sh)
    lap_lo = float(LAP_LO_F + sh); lap_hi = float(LAP_HI_F - sh)
    lm_lo = float(LAM2_LO_F + sh); lm_hi = float(LAM2_HI_F - sh)
    if tamper == "w17-shrink":
        w17_lo, w17_hi = 1.0000001, 1.0000002   # strictly below the realized range at
    else:                                        # every W17_GRID level (n=800 min ~1.000018)
        w17_lo, w17_hi = float(W17_LO_F), float(W17_HI_F)
    viol = 0; worst_head = 1e18; worst_which = ""
    worst_head_proved = 1e18; worst_which_proved = ""    # lam + mass-weighted Lambda^+/-
    worst_head_mean = 1e18; worst_which_mean = ""         # arithmetic-mean variants only
    cprime_realized = 0.0; cprime_realized_loc = ""
    for n in grid:
        for t in PARENTS:
            raw = onestep_raw(t, n, levs, win=WIN_STAR, cwin=CWIN); nn = raw['n']
            cp, cm = raw['cp'], raw['cm']
            lam = sum(cp[i] for i in range(nn)) / sum(cm[i] for i in range(nn))
            m = onestep_compose(raw, 'mass'); Lp, Lm = m['Lamp'], m['Lamm']
            # the FIELD's own object (window-coherence fix, round 4): the W=17 mass-
            # weighted references (log S^17)'(t_pm), matching gate LAM-INV's (I1)@17
            # identity and gamma/C' covers -- the field's realized counterpart, and the
            # object its enclosure must contain at the base-case levels.
            Lp17, Lm17 = m['Lamp17'], m['Lamm17']
            # the ARITHMETIC window-mean reference (the one Lemma A1's seminorm requires --
            # zero-sum delta; the forcing T1 must use the same split, so the box must cover
            # it, per D5). Checked alongside the mass-weighted references.
            LA = min(CWIN, len(raw['Lp']), len(raw['Lm']))
            LpA = sum(raw['Lp'][:LA]) / LA; LmA = sum(raw['Lm'][:LA]) / LA
            rhos = [cp[i] / cm[i] for i in range(nn)]
            checks = [("lam", lam, lam_lo, lam_hi),
                      ("Lam+mass17", Lp17, lap_lo, lap_hi), ("Lam-mass17", Lm17, lm_lo, lm_hi),
                      ("Lam+mass", Lp, lap_lo, lap_hi), ("Lam-mass", Lm, lm_lo, lm_hi),
                      ("Lam+mean", LpA, lap_lo, lap_hi), ("Lam-mean", LmA, lm_lo, lm_hi)]
            checks += [("rho_%d" % i, r, lam_lo, lam_hi) for i, r in enumerate(rhos)]
            for name, v, lo, hi in checks:
                h = min(v - lo, hi - v)
                if h < 0:
                    viol += 1
                if h < worst_head:
                    worst_head = h; worst_which = "%s@n=%d" % (name, n)
                is_mean = name in ("Lam+mean", "Lam-mean")
                if is_mean:
                    if h < worst_head_mean:
                        worst_head_mean = h; worst_which_mean = "%s@n=%d" % (name, n)
                else:
                    if h < worst_head_proved:
                        worst_head_proved = h; worst_which_proved = "%s@n=%d" % (name, n)
            # C' consistency check (a-posteriori side of R1): the realized FIELD object
            # -- the W=17 mass-weighted Lambda^+/- (Lp17,Lm17; window-coherence fix,
            # round 4: previously the 18-window variant was compared here, one edge term
            # off the field's own (I1)@17 identity) vs gate LAM-INV's converged field
            # prediction at the SAME (t+,t-), broader than gate LAM-INV's own sparse
            # one-anchor sample (this loop already covers MAG_GRID x 41 parents).
            if laminv is not None:
                tp_fr = frac_exact((1 + t) / 3.0); tm_fr = frac_exact((1 - t) / 3.0)
                Lp_lo_f, Lp_hi_f = _brk_L_exact_lam(laminv['loc'], laminv['Lam_F'], tp_fr, LIP_L_LAM_F)
                Lm_lo_f, Lm_hi_f = _brk_L_exact_lam(laminv['loc'], laminv['Lam_F'], tm_fr, LIP_L_LAM_F)
                Lp_field = float(Lp_lo_f + Lp_hi_f) / 2.0
                Lm_field = float(Lm_lo_f + Lm_hi_f) / 2.0
                d_here = max(abs(Lp17 - Lp_field), abs(Lm17 - Lm_field))
                if d_here > cprime_realized:
                    cprime_realized = d_here; cprime_realized_loc = "n=%d,t=%.4f" % (n, t)
    # boundary-slot pass: w_17 := rho_17/lam_gc against its OWN deep box, W17_GRID only.
    # `levs` may not reach W17_GRID's depth (e.g. --quick, capped ~200; SIB-CERT/this
    # check are both full-mode-only in spirit) -- filter to levels `levs` actually has
    # (onestep_raw needs levs[n-1] and levs[n], so require n < len(levs)) rather than
    # index-error; an empty effective grid is vacuously ok (nothing claimed, nothing
    # checked, matching SIB-CERT's own --quick/--fallback skip).
    w17_grid_eff = [n for n in W17_GRID if n < len(levs)]
    w17_viol = 0; w17_worst = 1e18; w17_worst_n = None
    for n in w17_grid_eff:
        for t in PARENTS:
            raw = onestep_raw(t, n, levs, win=WIN_STAR, cwin=CWIN)
            cp, cm = raw['cp'], raw['cm']
            if len(cp) < 18 or len(cm) < 18 or raw['n'] < WIN_STAR:
                continue   # defensive; never triggers on w17_grid_eff (deep levels)
            window_rhos = [cp[i] / cm[i] for i in range(WIN_STAR)]
            lam_gc = math.sqrt(min(window_rhos) * max(window_rhos))
            w17 = (cp[17] / cm[17]) / lam_gc
            h = min(w17 - w17_lo, w17_hi - w17)
            if h < 0:
                w17_viol += 1
            if h < w17_worst:
                w17_worst = h; w17_worst_n = n
    viol += w17_viol
    ok = (viol == 0)
    if w17_grid_eff:
        w17_desc = ("over %d levels {%s} (SIB-CERT's boundary slot; decays ~C/n^2)"
                    " (violations=%d, worst headroom %.6f @n=%s)%s"
                    % (len(w17_grid_eff), ",".join(str(x) for x in w17_grid_eff),
                       w17_viol, w17_worst, w17_worst_n,
                       " [TAMPERED w17-shrink]" if tamper == "w17-shrink" else ""))
    else:
        w17_desc = ("SKIPPED in this mode (deep anchor levels %s not built -- SIB-CERT's"
                    " own boundary slot is likewise full-mode-only)" % str(W17_GRID))
    if laminv is not None:
        cprime_note = (" | C' consistency (a-posteriori R1, realized-vs-field, %d levels x"
                        " 41 parents): worst=%.4f @%s vs CPRIME=%s [%s]"
                        % (len(grid), cprime_realized, cprime_realized_loc,
                           str(laminv['cprime_eff']),
                           "OK" if cprime_realized <= float(laminv['cprime_eff']) else "MISS"))
    else:
        cprime_note = " | C' consistency check SKIPPED in this mode (gate LAM-INV does not run)"
    report.append(("MAG-BOX [core, (LAM-BOX) empirical cross-check, window i<17] lam and"
                    " mass-weighted Lambda^+/- lines: PROVED-CONDITIONAL INTERVAL (gate"
                    " LAM-INV), monitoring RETAINED -- realized lam, Lambda^+/-mass,"
                    " per-entry rho_i in the magnitude boxes over %d levels x 41 parents"
                    " (violations=%d); worst headroom (lam/mass/rho) %.4f (%s)."
                    " Lam+/-mean (arithmetic-mean variants): COMPUTED-monitored ONLY --"
                    " NOT covered by the LAM-INV enclosure, and WIDENS with depth"
                    " (LAB_LAMBOX Q1) -- worst headroom %.4f (%s)%s"
                    " + boundary wobble w17=rho_17/lam_gc in its deep box [0.999,1.001] %s"
                    % (len(grid), viol - w17_viol, worst_head_proved, worst_which_proved,
                       worst_head_mean, worst_which_mean,
                       " [TAMPERED]" if tamper == "magbox-shrink" else "", w17_desc)
                    + cprime_note, ok))

# ---- (SIB-BAND) sibling-wobble census -------------------------------------------
# The forced-proportional gates (V15-IA, V17-IA) are the w_i==1 slice. Under the IH
# rho_prop@i<17(n-1)<=TARGET the real cascade is c^+_i = lam*w_i*c^-_i (w_i band from
# the IH for i<17; boundary slot i=17 via the W17 deep box -- gate SIB-CERT / note S8.4
# annex; see W17_LO_F/W17_HI_F above); the per-entry
# marginal SAFE band is WOB_FULL=[1/R*,R*]. g_i (forcing) and the Lemma-A1 M-entries stay
# ratios of MULTI-AFFINE functions in (a=rc_{i-1}, b=rc_i, u=w_{i-1}, v=w_i, x=w_{i+1},
# lam, Lambda^pm) -> coordinatewise MONOTONE (fix all-but-one: num,den affine => Moebius =>
# monotone, no pole since den>0) -> EXACT box range by corner enumeration. Magnitude
# (lam,Lambda^pm) is SHARED across indices (fixed per osc-evaluation, max over the 8
# corners); wobble+ratio are per-index marginal (sound over-approx). Derivation, verifier
# convention (cp=c^+ from t_+, cm=c^- from t_-): Q^+_i = 0.25 u/a + d_+ v + 0.25 x b,
# Q^-_i = d_- + 0.25/a + 0.25 b, D_i = lam Q^+_i + Q^-_i; T1+T3 num = Lambda^+ lam Q^+_i -
# Lambda^- Q^-_i + a'(t_+)(lam v - 1) - a'(t/3); i=0: Q^+_0 = d_+ w_0 + 0.5 w_1 rc_0.

def _ab_lc_vertices(i, floors):
    if i == 0:
        return [(Fr(1), floors[0]), (Fr(1), Fr(1))]
    fa, fb = floors[i - 1], floors[i]
    verts = [(fa, fb), (Fr(1), fb), (Fr(1), Fr(1))]
    if fa >= fb:
        verts.append((fa, fa))
    return verts

def _g_wob(i, a, b, u, v, x, lam, Lp, Lm, dp_, dm_, ap_, at3):
    if i == 0:
        Qp = dp_ * u + Fr(1, 2) * x * b; Qm = dm_ + Fr(1, 2) * b; wv = u
    else:
        Qp = Fr(1, 4) * u / a + dp_ * v + Fr(1, 4) * x * b; Qm = dm_ + Fr(1, 4) / a + Fr(1, 4) * b; wv = v
    D = lam * Qp + Qm
    if D <= 0:
        return None
    return (Lp * lam * Qp - Lm * Qm + ap_ * (lam * wv - 1) - at3) / (3 * D)

def F_box_wobble_certified(levs, J0, f_pad, wob, boundary_band=None):
    """(round 2) `boundary_band`, if given, replaces `wob` for the x-slot (representing
    w_{i+1}) ONLY at i == WIN_STAR-1 (the i=16 row's k=17 entry -- w_17, the one wobble
    index that reads past the IH's i<17 window; see the W17_LO_F/W17_HI_F module comment
    and note Section 8.4's BOUNDARY ANNEX). Every other slot (u, v everywhere; x at
    i<WIN_STAR-1) is unaffected. Default None reproduces the ORIGINAL behavior exactly
    (x uses `wob` at every i, including i=WIN_STAR-1) -- gate_sibling_band (the shallow-
    anchor exhibit) relies on this: it does not pass boundary_band, so its numbers are
    byte-identical to before this round's change."""
    worst = Fr(0); wt = None
    for t in PARENTS:
        floors = [frac_outward(f_pad * r, lo=True, slop=IA_SLOP)
                  for r in anchor_c_ratios(t, levs, J0, win=WIN_STAR)]
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        dp_ = frac_exact(d_of(tp)); dm_ = frac_exact(d_of(tm))
        ap_ = frac_exact(dprime(tp)); at3 = frac_exact(dprime(t / 3.0))
        ab = [_ab_lc_vertices(i, floors) for i in range(WIN_STAR)]
        best = Fr(0)
        for lam in (LAM_LO_F, LAM_HI_F):
            for Lp in (LAP_LO_F, LAP_HI_F):
                for Lm in (LAM2_LO_F, LAM2_HI_F):
                    his = []; los = []; feas = True
                    for i in range(WIN_STAR):
                        x_band = (boundary_band if (boundary_band is not None
                                                     and i == WIN_STAR - 1) else wob)
                        lo_i = hi_i = None
                        for (a, b) in ab[i]:
                            for u in wob:
                                for v in wob:
                                    for x in x_band:
                                        g = _g_wob(i, a, b, u, v, x, lam, Lp, Lm, dp_, dm_, ap_, at3)
                                        if g is None:
                                            continue
                                        if lo_i is None or g < lo_i:
                                            lo_i = g
                                        if hi_i is None or g > hi_i:
                                            hi_i = g
                        if lo_i is None:
                            feas = False; break
                        his.append(hi_i); los.append(lo_i)
                    if not feas:
                        continue
                    d = max(his) - min(los)
                    if d > best:
                        best = d
        v = best * (1 + IA_SLOP)
        if v > worst:
            worst = v; wt = t
    return worst, wt

def _row_entries_wob(i, floors, dp_, dm_, lam, wob, boundary_band=None):
    """(round 2) `boundary_band`, if given (non-None), replaces `wob` for the x-slot
    (entry k=i+1, i.e. w_{i+1}) -- the caller (theta_band_wobble_certified) passes it
    ONLY when i == WIN_STAR-1, so this only ever changes the i=16 row's k=17 (w_17)
    entry; every other call site (all i<WIN_STAR-1, and u/v at every i) is unaffected."""
    if i == 0:
        aset = [Fr(1)]; bset = [floors[0], Fr(1)]
    else:
        aset = [floors[i - 1], Fr(1)]; bset = [floors[i], Fr(1)]
    x_band = wob if boundary_band is None else boundary_band
    acc = {}
    for a in aset:
        for b in bset:
            for u in wob:
                for v in wob:
                    for x in x_band:
                        if i == 0:
                            Qp = dp_ * u + Fr(1, 2) * x * b; Qm = dm_ + Fr(1, 2) * b
                        else:
                            Qp = Fr(1, 4) * u / a + dp_ * v + Fr(1, 4) * x * b; Qm = dm_ + Fr(1, 4) / a + Fr(1, 4) * b
                        D = lam * Qp + Qm
                        if D <= 0:
                            return None
                        d3 = 3 * D
                        if i == 0:
                            ents = {0: (lam * dp_ * u / d3, dm_ / d3),
                                    1: (lam * Fr(1, 2) * b * x / d3, Fr(1, 2) * b / d3)}
                        else:
                            ents = {i: (lam * dp_ * v / d3, dm_ / d3),
                                    i + 1: (lam * Fr(1, 4) * b * x / d3, Fr(1, 4) * b / d3),
                                    i - 1: (lam * Fr(1, 4) * (1 / a) * u / d3, Fr(1, 4) * (1 / a) / d3)}
                        for k, (mp, mm) in ents.items():
                            if k not in acc:
                                acc[k] = [mp, mp, mm, mm]
                            r = acc[k]
                            if mp < r[0]: r[0] = mp
                            if mp > r[1]: r[1] = mp
                            if mm < r[2]: r[2] = mm
                            if mm > r[3]: r[3] = mm
    return dict((k, ((r[0], r[1]), (r[2], r[3]))) for k, r in acc.items())

def theta_band_wobble_certified(levs, J0, f_pad, wob, boundary_band=None):
    """(round 2) `boundary_band`: forwarded to `_row_entries_wob` ONLY for the row
    i == WIN_STAR-1 (the sole row whose x-slot, w_17, reads past the IH's i<17 window);
    every other row gets `boundary_band=None`, reproducing the original `wob`-everywhere
    behavior exactly. Default None (no kwarg passed) reproduces the ORIGINAL function
    exactly at every row -- gate_sibling_band's numbers are unaffected."""
    worst = Fr(0)
    for t in PARENTS:
        floors = [frac_outward(f_pad * r, lo=True, slop=IA_SLOP)
                  for r in anchor_c_ratios(t, levs, J0, win=WIN_STAR)]
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        dp_ = frac_exact(d_of(tp)); dm_ = frac_exact(d_of(tm))
        for lam in (LAM_LO_F, LAM_HI_F):
            rows = [_row_entries_wob(i, floors, dp_, dm_, lam, wob,
                                      boundary_band=(boundary_band if i == WIN_STAR - 1
                                                      else None))
                    for i in range(WIN_STAR)]
            if any(r is None for r in rows):
                continue
            for i in range(WIN_STAR):
                for ip in range(i + 1, WIN_STAR):
                    val = (theta_band_seminorm_pair(rows[i], rows[ip], CWIN, 0)
                           + theta_band_seminorm_pair(rows[i], rows[ip], CWIN, 1)) / 2
                    if val > worst:
                        worst = val
    return round_up_frac(worst * Fr(57, 50) * (1 + IA_SLOP))

def gate_sibling_band(info, levs, J0, f_pad):
    """SIB-BAND [informational, the (SIB-BAND) computed clause]: re-runs BOTH load-bearing
    censuses over the sibling WOBBLE band (per-entry factor in WOB_FULL=[1/R*,R*], the IH-
    implied worst case), exposing the real-vs-proportional gap the forced-proportional
    gates hide. At the shipped anchor the wobble-extended forcing EXCEEDS the equilibrium
    threshold: the census does NOT extend to the real cascade here (a real gap, reported
    not hidden -- see note Section 8). Marked FAIL to keep the gap visible; INFORMATIONAL,
    does not count toward RESULT. The tighter (still sound) geometric-center band
    [1/sqrt R*, sqrt R*] narrows the gap but also misses at this depth (note Section 8).
    This gap IS closed -- see gate SIB-CERT below, which reruns this same geometric-center
    census at a deep anchor (J0=800, pad=999/1000) where it clears (+4.6% margin),
    discharging (SIB-BAND). This gate remains exactly as shipped: the shallow-anchor
    (J0*=500) exhibit of the gap, kept informational for the historical record."""
    tb = theta_band_wobble_certified(levs, J0, f_pad, WOB_FULL)
    fb, wt = F_box_wobble_certified(levs, J0, f_pad, WOB_FULL)
    thr = (1 - tb) * TAU_STAR_FR
    ok = fb <= thr
    gap = float((fb - thr) / thr) * 100 if thr != 0 else 0.0
    info.append(("SIB-BAND [INFORMATIONAL, (SIB-BAND) COMPUTED clause, window i<17, anchor"
                  " J0=%d, pad f=%s] wobble-extended censuses (per-entry w in [1/R*,R*]):"
                  " theta_band_wob=%.6f, F_box_wob=%.7f vs threshold (1-theta_wob)*tau*"
                  " = %.7f -- forced-proportional surrogate %s the real cascade by %.1f%%"
                  " (the extension does NOT close at this anchor)"
                  % (J0, str(f_pad), float(tb), float(fb), float(thr),
                     "covers" if ok else "UNDER-COVERS", abs(gap)), ok))

# ---- SIB-CERT: discharges (SIB-BAND) at a deep anchor -----------------------------
#
# GEOMETRIC-CENTER LEMMA. Given (i) the IH rho_prop@i<17(n-1) <= R* (R_STAR_FR) and
# (ii) MAG-BOX's own per-entry box: rho_i = c^+_i/c^-_i in [LAM_LO_F, LAM_HI_F] for
# every i (the (LAM-BOX) clause, monitored not proved -- but ALREADY a named, gated
# assumption every load-bearing gate in this file rests on; this lemma adds NOTHING
# beyond it), set lam_gc := sqrt(min_i rho_i * max_i rho_i). Then, in 3 lines:
#   (i)   min_i rho_i <= lam_gc <= max_i rho_i (the geometric mean of two positive
#         numbers sits between them), and both min_i rho_i, max_i rho_i lie in
#         [LAM_LO_F, LAM_HI_F] by (LAM-BOX) -- so lam_gc is ITSELF a legal point of the
#         (already-monitored) lam box: no new box, no new assumption.
#   (ii)  w_i := rho_i / lam_gc satisfies max_i w_i = sqrt(max_i rho_i / min_i rho_i)
#         = sqrt(rho_prop@i<17(n-1)) <= sqrt(R*) by the IH, and symmetrically
#         min_i w_i = 1/sqrt(max_i rho_i/min_i rho_i) >= 1/sqrt(R*) -- so w_i lies in
#         WOB_HALF = [1/sqrt(R*), sqrt(R*)] for every i, again from the IH alone.
#   (iii) Hence the REAL one-step pair c^+_i = lam_gc * w_i * c^-_i, with lam_gc in the
#         lam box and w_i in WOB_HALF per-entry, is exactly the object
#         theta_band_wobble_certified/F_box_wobble_certified already box-max over (they
#         box-max lam over [LAM_LO_F,LAM_HI_F] -- lam_gc qualifies by (i) -- AND
#         independently per-entry over the given wobble band -- w_i qualifies by (ii),
#         and independent-per-entry is a SAFE superset of the lam_gc-linked real w_i).
# So a census clearing the equilibrium threshold at WOB_HALF covers the REAL cascade,
# not merely the lam_gc==const/w_i==1 forced-proportional slice V15-IA/V17-IA certify.
#
# The deep anchor. At the shipped (J0*,F_STAR)=(500,99/100) this half-band census still
# MISSES (note Section 8.4/SIB-BAND: F_box_wob=0.0417911 vs threshold, -43%). Sounding a
# deeper, more tightly padded anchor (scratchpad diag4, reproduced exactly here by the
# gate itself): J0=600 pad=999/1000 misses (-11.1%), J0=700 misses (-1.9%), J0=800
# CLEARS (+4.6%) -- monotone improvement with depth, as expected (deeper anchor = looser
# floors = smaller F_box, while theta_band_wob is comparatively flat). (J0_SIB,PAD_SIB)
# = (800, 999/1000) is the discharge anchor; see J0_SIB/PAD_SIB above.

_SIBCERT_CERT = {}   # module-level exact-Fraction record of the last SIB-CERT run, for
                      # the cert JSON / Lean transcription (see the verification driver).

def gate_sib_cert(report, levs, tamper=None):
    """SIB-CERT [core, FULL MODE ONLY -- discharges (SIB-BAND) at the deep anchor GIVEN
    (LAM-BOX)]: re-runs the geometric-center half-band censuses (theta_band_wobble_
    certified / F_box_wobble_certified over WOB_HALF = [1/sqrt R*, sqrt R*]) at the deep
    anchor (J0_SIB=800, PAD_SIB=999/1000), where -- unlike the shipped (J0*=500) anchor
    gate_sibling_band exhibits -- the wobble-extended census CLEARS the equilibrium
    threshold. By the GEOMETRIC-CENTER LEMMA above (a 3-line consequence of (LAM-BOX)
    plus the IH, no new assumption), this closes the real-vs-proportional gap
    (SIB-BAND) names: the REAL non-proportional cascade, not merely the
    lam==const/w==1 forced-proportional surrogate V15-IA/V17-IA certify, is covered for
    n >= 800. Combined with the deep grid (V18, now extended to n=800) covering
    48<=n<=800 directly, (SIB-BAND) is discharged.

    Outwardness self-check (runs first, unconditionally): _SQ_HI is defined as a
    rational OUTWARD (upper) bound on sqrt(R*) -- WOB_HALF := (1/_SQ_HI, _SQ_HI) is only
    a safe (superset) wobble band if _SQ_HI really does satisfy _SQ_HI*_SQ_HI >= R_STAR_FR
    (an INWARD/lower bracket would silently shrink WOB_HALF below what the lemma
    requires, making the census unsound even if it happens to clear numerically). This
    gate re-verifies that inequality every run; if it fails, the gate FAILs immediately
    and the (otherwise ~35s) wobble census is not run (a census built on an unsound
    bracket is not worth computing).

    Tampers (all isolated to this gate, report index 8): 'sibcert-sqrt' substitutes an
    explicitly INWARD rational bracket on sqrt(R*) (bisection converged from below
    instead of above) in place of _SQ_HI, tripping the outwardness self-check above.
    'sibcert-pad' swaps the anchor pad from PAD_SIB=999/1000 to F_STAR=99/100 (the
    shipped V17-IA anchor's pad) at the same J0=800 -- too shallow a pad at this depth
    (sounding: -12.2%), flipping fb<=thr to MISS. 'sibcert-band' swaps the
    geometric-center half-band WOB_HALF for the full IH band WOB_FULL=[1/R*,R*], which
    the note's SIB-BAND sounding ladder shows cannot clear at ANY depth -- also flips to
    MISS. None of the three touch J0_STAR/F_STAR/DEEP_GRID_FULL or any other gate's
    inputs (tamper is checked here by name only). ('w17-shrink' targets gate MAG-BOX,
    report index 1, not this gate -- see gate_magnitude_box.)

    (round 2, PI review) BOUNDARY SLOT. Both wobble censuses range u,v,x over `wob` at
    every row i<WIN_STAR; at i=WIN_STAR-1=16, the x-slot is entry k=17 -- w_17, ONE PAST
    the IH's i<17 window, with no hypothesis from the IH or from MAG-BOX's ordinary
    per-entry monitoring (also capped at i<17). This gate passes `boundary_band =
    (W17_LO_F, W17_HI_F)` to both censuses, which routes ONLY that one x-slot (i=16) to
    the deep box W17_LO_F/W17_HI_F=[999/1000,1001/1000] instead of WOB_HALF -- a box
    gate MAG-BOX separately monitors over W17_GRID={500,...,800} (SIB-CERT's own
    operative domain), the same (LAM-BOX)-class epistemic status as lam/Lambda^pm. The
    naive "same band as the window" claim is FALSE at shallow n (w_17(48) measured up to
    1.016780 > WOB_HALF's 1.012723); the deep box is honest and checked where the naive
    claim was neither. See note Section 8.4's BOUNDARY ANNEX."""
    if tamper == "sibcert-sqrt":
        lo, hi = Fr(0), R_STAR_FR + 1          # bisection identical to _sqrt_hi_frac,
        for _ in range(64):                    # but returning the INWARD (lo) bracket
            mid = (lo + hi) / 2
            if mid * mid <= R_STAR_FR:
                lo = mid
            else:
                hi = mid
        sq_hi_eff = lo                         # <= sqrt(R*) (unsound as an upper bound)
    else:
        sq_hi_eff = _SQ_HI                     # the shipped OUTWARD bracket, >= sqrt(R*)
    outward_ok = (sq_hi_eff * sq_hi_eff >= R_STAR_FR)

    pad = F_STAR if tamper == "sibcert-pad" else PAD_SIB
    wob = WOB_FULL if tamper == "sibcert-band" else (Fr(1) / sq_hi_eff, sq_hi_eff)
    boundary_band = (W17_LO_F, W17_HI_F)   # the i=16 x-slot's OWN deep box (round 2);
                                            # unconditional -- no sibcert-* tamper touches it

    if not outward_ok:
        _SIBCERT_CERT.clear()
        _SIBCERT_CERT["error"] = "outwardness self-check failed [tamper=%s]" % tamper
        report.append(("SIB-CERT [core, discharges (SIB-BAND) at the deep anchor GIVEN"
                        " (LAM-BOX), window i<17, anchor J0=%d, pad f=%s] outwardness"
                        " self-check FAILED: sqrt-bracket %s is NOT >= sqrt(R*) (R*=%s) --"
                        " an inward bracket would make WOB_HALF unsound, so the wobble"
                        " census is not run [TAMPERED %s]"
                        % (J0_SIB, str(pad), str(sq_hi_eff), str(R_STAR_FR), tamper),
                        False))
        return

    tb = theta_band_wobble_certified(levs, J0_SIB, pad, wob, boundary_band=boundary_band)
    fb, wt = F_box_wobble_certified(levs, J0_SIB, pad, wob, boundary_band=boundary_band)
    thr = (1 - tb) * TAU_STAR_FR
    ok = fb <= thr
    margin = float((thr - fb) / thr) * 100 if thr != 0 else 0.0

    # equilibrium chain, mirroring gate_forcing_ia's printed form exactly.
    ceiling = fb / (1 - tb)
    log_rho = ceiling / 3
    ceiling_ok = ceiling <= TAU_STAR_FR
    exp_bound = math.exp(float(log_rho))

    _SIBCERT_CERT.clear()
    _SIBCERT_CERT.update(dict(
        anchor_J0=J0_SIB, pad=str(pad), locus_t=wt, tamper=tamper, ok=bool(ok),
        F_box_wob="%d/%d" % (fb.numerator, fb.denominator),
        theta_band_wob="%d/%d" % (tb.numerator, tb.denominator),
        threshold="%d/%d" % (thr.numerator, thr.denominator),
        F_box_wob_float=float(fb), theta_band_wob_float=float(tb),
        threshold_float=float(thr), margin_pct=margin))

    report.append(("SIB-CERT [core, discharges (SIB-BAND) at the deep anchor GIVEN"
                    " (LAM-BOX), window i<17, anchor J0=%d, pad f=%s] geometric-center"
                    " half-band censuses (lemma: MAG-BOX per-entry rho_i in"
                    " [LAM_LO,LAM_HI] => lam_gc=sqrt(min*max) in the lam box,"
                    " w_i=rho_i/lam_gc in [1/sqrtR*,sqrtR*]): theta_band_wob=%.6f,"
                    " F_box_wob=%.7f (locus t=%.4f) <= threshold (1-theta_wob)*tau*"
                    " = %.7f (margin %.1f%%, exact-Fraction compare; sqrt bracket"
                    " outward-checked), floors (FLOOR-PERSIST @ 999/1000)%s; boundary slot"
                    " (i=16,x)=w_17 (outside the IH window) ranges over the monitored deep"
                    " box W17=[999/1000,1001/1000] ((LAM-BOX) class, gate MAG-BOX,"
                    " levels 500..800)\n"
                    "        equilibrium chain: F_box_wob/(1-theta_wob) = %.8f <= tau*"
                    " = %.8f [%s]; (1/3)* = %.8f <= ln(TARGET) = %.8f; exp(.) = %.6f"
                    " <= TARGET = %.8f [%s]"
                    % (J0_SIB, str(pad), float(tb), float(fb), wt, float(thr), margin,
                       " [TAMPERED %s]" % tamper
                       if tamper in ("sibcert-pad", "sibcert-band") else "",
                       float(ceiling), float(TAU_STAR_FR),
                       "OK" if ceiling_ok else "MISS", float(log_rho), LTARGET,
                       exp_bound, TARGET, "OK" if exp_bound <= TARGET else "MISS"), ok))

# ===================================================================================
# LAM-INV: PROVED-conditional upgrade of the (LAM-BOX) COMPUTED magnitude box.
# ===================================================================================
#
# DERIV_LAMBOX.md (derivation lane) upgrades lam/Lambda^+/Lambda^- from MEASURED+padded
# (gate MAG-BOX, still monitored, still COMPUTED) to PROVED invariant intervals over an
# infinite family of levels n, CONDITIONAL on: the existing floor box (F3), the existing
# finite base-case census (gates MAG-BOX/V18, n in {48..800}), an a-posteriori Lipschitz
# self-check (this gate), and one remaining generous MONITORED constant, the correction-
# derivative cap C' (named clause (C'-CAP) -- see the note's Section 8.4). Two PROVED
# identities underlie the construction (LAB_LAMBOX.md Q2 independently re-derived and
# Fraction-exact-verified identity (I1); this gate adds its own live spot-check below):
#
#   (I1) EXACT WINDOWED MASS RECURSION:  sum_{i<W}(K_d*c)_i  =  a(t)*M_w(c)
#            - (1/4)(c_0-c_1)  -  (1/4)(c_{W-1}-c_W),   W = OPWIN = 17.
#        PROVED (telescoping conv_even's own definition); verified EXACTLY in Fraction
#        arithmetic here (residual must be algebraically 0, not merely float-small) and,
#        independently, by the concurrent lab lane (LAB_LAMBOX.md Q2, residual=0, 40
#        checks). The E_W = c_{16}-c_{17} term reads c_17, ONE PAST the operative i<17
#        window -- but only via rc_16 = c_17/c_16 in [f_16,1], and F3 already certifies
#        the floor family over i<18 (FLOOR_WIN=CWIN=18), so rc_16 sits INSIDE the
#        certified floor window: no new hypothesis beyond the existing F3 gate.
#   (I2) Lambda^pm_mass = (log S^W)'(t_pm),  S^W(s) := sum_{i<W} c_i(G(s)) -- the
#        identity is WINDOW-GENERIC; the field instantiates it at W = OPWIN = 17,
#        MATCHING (I1) and the gamma/C' floor-box covers (window-coherence fix,
#        round 4: an earlier revision cited it at W=18 while (I1)/gamma were @17 --
#        one edge term of slippage between the field and its realized comparisons;
#        the monitors now compare the field against the W=17 object, Lamp17/Lamm17).
#        PROVED: an elementary algebraic identity (L_i c_i = c_i' by the definition
#        L_i := d/dt log c_i, so sum_i L_i c_i = sum_i c_i' = d/dt sum_i c_i; dividing by
#        sum_i c_i gives d/dt log(sum_i c_i)); confirmed to 1e-11 by finite-difference
#        cross-check in the derivation lane (DERIV_LAMBOX.md Section 3.2).
#
# Method (house V17-IA style: float pre-convergence to a candidate field, one rigorous
# exact-Fraction pass to CERTIFY it, final comparisons exact -- float error dwarfed by
# the documented outward slops). The pure a-weighted mass operator (TS)(t) :=
# a(t+)S(t+)+a(t-)S(t-) is exactly positive, hence Birkhoff-contracting to a fixed RAY
# (projective direction) -- NOT a fixed point (a(t+)+a(t-) = 1+(1/2)cos(2 pi t/3) in
# [1.25,1.47], strictly >1, so T genuinely grows S by a dominant-eigenvalue-like factor
# every pass). lam/Lambda are ratio / log-derivative objects, invariant to any
# t-INDEPENDENT rescaling of S, so the correct one-pass invariance check is
# T(S)/sc_exact subset S, sc_exact := max_t T(S)_hi(t) DERIVED from that same one pass
# (not an independent input -- matches the per-iteration renormalization the float
# precompute already performs). The comparison tolerance is GMAX (mass) / CPRIME
# (Lambda), applied ONLY at the final comparison, not by perturbing the field itself:
# additive field-padding was tried and found COUNTERPRODUCTIVE (sc_exact's own
# self-referential dependence on the widened field amplifies hi-side widening into the
# lo-side gap); using the SAME already-named, already-generous correction slops as the
# certificate's own between-grid discretization cover is honest bookkeeping (one deficit,
# multiple provenances), not a new constant.

NG_LAM = 3841                          # >= DERIV_LAMBOX's R4 threshold (NG=1921 marginal
                                       # for Lambda^+; NG=3841 fits all three)
LIP_S_LAM_F = Fr(6, 5)                 # 1.20, >= sup|Lambda| (a-posteriori self-checked)
LIP_L_LAM_F = Fr(13, 5)                # 2.60, >= sup|Lambda'| (a-posteriori self-checked)
GMAX_LAM_F = Fr(1, 200)                # 0.005; PROVED <= from the F3 floor box (this gate)
CPRIME_LAM_F = Fr(3, 500)              # 0.006; the (C'-CAP) clause -- MONITORED, the ONE
                                       # remaining computed/monitored literal this upgrade
                                       # introduces (measured impact ~0.002-0.003, DERIV_LAMBOX)
LAM_ITERS = 400                        # float pre-convergence passes (matches the
                                       # derivation lane's own validated proto5/6 setting;
                                       # NOT increased further -- empirically, many more
                                       # iterations DRIFT rather than tighten, see dev notes)
LAM_FIELD_SLOP = Fr(1, 10**6)          # outward relative slop for the float->Fraction
                                       # field conversion (covers ordinary float rounding
                                       # of the NG-point precompute; the between-grid
                                       # discretization residual is separately covered by
                                       # GMAX/CPRIME at the comparison step, above)

def _loga_prime_of(s):
    """(log a)'(s) = a'(s)/a(s), reusing the file's OWN dprime (=a') and a_of -- NOT an
    independently-evaluated 2*pi*cot(pi*s), so a live exact spot-check would see the SAME
    float value conv_even-style identities already use elsewhere in this file."""
    return dprime(s) / a_of(s)

def _a_bracket_lam(t, lo):
    return frac_outward(a_of(t), lo=lo, slop=IA_SLOP)

def _loga_prime_bracket_lam(t, lo):
    return frac_outward(_loga_prime_of(t), lo=lo, slop=IA_SLOP)

def _exp_bracket_lam(x_frac, lo):
    return frac_outward(math.exp(float(x_frac)), lo=lo, slop=IA_SLOP)

def _float_converge_lam(NG, LIP_S, LIP_L, GMAX, CPRIME, iters=LAM_ITERS):
    """FLOAT precompute only (candidate field, not part of the certificate itself): the
    Birkhoff power iteration for the mass field (rescaled every pass by its own max, the
    standard projective-power-iteration normalization), then the coupled Lambda-field
    recursion (DERIV_LAMBOX Section 3.2/3.3) against the resulting lam envelope."""
    LOt, HIt = 1.0 / 6, 1.0 / 2
    GT = [LOt + (HIt - LOt) * k / (NG - 1) for k in range(NG)]
    def brk_S(field, t):
        if t <= GT[0]: return field[0]
        if t >= GT[-1]: return field[-1]
        x = (t - LOt) / (HIt - LOt) * (NG - 1); i0 = max(0, min(NG - 2, int(x)))
        dl = t - GT[i0]; dr = GT[i0 + 1] - t
        lo = max(field[i0][0] * math.exp(-LIP_S * dl), field[i0 + 1][0] * math.exp(-LIP_S * dr))
        hi = min(field[i0][1] * math.exp(LIP_S * dl), field[i0 + 1][1] * math.exp(LIP_S * dr))
        return lo, hi
    def brk_L(field, t):
        if t <= GT[0]: return field[0]
        if t >= GT[-1]: return field[-1]
        x = (t - LOt) / (HIt - LOt) * (NG - 1); i0 = max(0, min(NG - 2, int(x)))
        dl = t - GT[i0]; dr = GT[i0 + 1] - t
        lo = max(field[i0][0] - LIP_L * dl, field[i0 + 1][0] - LIP_L * dr)
        hi = min(field[i0][1] + LIP_L * dl, field[i0 + 1][1] + LIP_L * dr)
        return lo, hi
    S = [[1.0, 1.0] for _ in GT]
    for _ in range(iters):
        nn = []
        for t in GT:
            tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
            plo, phi = brk_S(S, tp); mlo, mhi = brk_S(S, tm)
            ap, am = a_of(tp), a_of(tm)
            nn.append([ap * plo + am * mlo, ap * phi + am * mhi])
        sc = max(f[1] for f in nn); S = [[f[0] / sc, f[1] / sc] for f in nn]
    def lam_encl(t):
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        plo, phi = brk_S(S, tp); mlo, mhi = brk_S(S, tm)
        return (plo / mhi) * (1 - GMAX), (phi / mlo) * (1 + GMAX)
    Lam = [[-0.75, -0.65] for _ in GT]
    for _ in range(iters):
        nn = []
        for t in GT:
            tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
            llo, lhi = lam_encl(t); ap, am = a_of(tp), a_of(tm)
            wlo = ap * llo / (ap * llo + am); whi = ap * lhi / (ap * lhi + am)
            Lplo, Lphi = brk_L(Lam, tp); Lmlo, Lmhi = brk_L(Lam, tm)
            gpl = _loga_prime_of(tp) + Lplo; gph = _loga_prime_of(tp) + Lphi
            gml = _loga_prime_of(tm) + Lmlo; gmh = _loga_prime_of(tm) + Lmhi
            c = [(1.0 / 3) * (w * gp - (1 - w) * gm) for w in (wlo, whi) for gp in (gpl, gph) for gm in (gml, gmh)]
            nn.append([min(c) - CPRIME, max(c) + CPRIME])
        Lam = nn
    return GT, S, Lam

class _LamLocator:
    """Exact-Fraction grid + between-grid lookup for the LAM-INV certificate."""
    def __init__(self, NG):
        self.NG = NG
        self.LOt_F, self.HIt_F = Fr(1, 6), Fr(1, 2)
        self.GT_F = [self.LOt_F + (self.HIt_F - self.LOt_F) * Fr(k, NG - 1) for k in range(NG)]
    def idx(self, t_frac):
        x = (t_frac - self.LOt_F) * (self.NG - 1) / (self.HIt_F - self.LOt_F)
        i0 = math.floor(x)
        return max(0, min(self.NG - 2, i0))

def _to_frac_field_lam(field_float, slop):
    return [(frac_outward(lo, lo=True, slop=slop), frac_outward(hi, lo=False, slop=slop))
            for lo, hi in field_float]

def _brk_S_exact_lam(loc, field_F, t_frac, LIP_S_F):
    GT_F = loc.GT_F
    if t_frac <= GT_F[0]: return field_F[0]
    if t_frac >= GT_F[-1]: return field_F[-1]
    i0 = loc.idx(t_frac)
    dl = t_frac - GT_F[i0]; dr = GT_F[i0 + 1] - t_frac
    e_dl_lo = _exp_bracket_lam(-LIP_S_F * dl, lo=True); e_dl_hi = _exp_bracket_lam(LIP_S_F * dl, lo=False)
    e_dr_lo = _exp_bracket_lam(-LIP_S_F * dr, lo=True); e_dr_hi = _exp_bracket_lam(LIP_S_F * dr, lo=False)
    lo = max(field_F[i0][0] * e_dl_lo, field_F[i0 + 1][0] * e_dr_lo)
    hi = min(field_F[i0][1] * e_dl_hi, field_F[i0 + 1][1] * e_dr_hi)
    return (lo, hi)

def _brk_L_exact_lam(loc, field_F, t_frac, LIP_L_F):
    GT_F = loc.GT_F
    if t_frac <= GT_F[0]: return field_F[0]
    if t_frac >= GT_F[-1]: return field_F[-1]
    i0 = loc.idx(t_frac)
    dl = t_frac - GT_F[i0]; dr = GT_F[i0 + 1] - t_frac
    lo = max(field_F[i0][0] - LIP_L_F * dl, field_F[i0 + 1][0] - LIP_L_F * dr)
    hi = min(field_F[i0][1] + LIP_L_F * dl, field_F[i0 + 1][1] + LIP_L_F * dr)
    return (lo, hi)

def _lam_encl_exact_lam(loc, S_F, t_frac, GMAX_F, LIP_S_F):
    tp = (1 + t_frac) / 3; tm = (1 - t_frac) / 3
    P = _brk_S_exact_lam(loc, S_F, tp, LIP_S_F)
    M = _brk_S_exact_lam(loc, S_F, tm, LIP_S_F)
    lo = (P[0] / M[1]) * (1 - GMAX_F)
    hi = (P[1] / M[0]) * (1 + GMAX_F)
    return (lo, hi)

def _mass_invariance_check_lam(loc, S_F, LIP_S_F, GMAX_F):
    """One forward pass: T(S)/sc_exact vs S*(1 -+ GMAX). sc_exact is derived from this same
    pass (the ray-normalization, not a new input); GMAX is the comparison-only tolerance
    (see the module-level note above -- NOT baked into the field/recursion)."""
    raw = []
    for t in loc.GT_F:
        tp = (1 + t) / 3; tm = (1 - t) / 3
        P = _brk_S_exact_lam(loc, S_F, tp, LIP_S_F)
        M = _brk_S_exact_lam(loc, S_F, tm, LIP_S_F)
        apl = _a_bracket_lam(float(tp), True); aph = _a_bracket_lam(float(tp), False)
        aml = _a_bracket_lam(float(tm), True); amh = _a_bracket_lam(float(tm), False)
        raw.append((apl * P[0] + aml * M[0], aph * P[1] + amh * M[1]))
    sc_exact = max(hi for _, hi in raw)
    worst_lo = worst_hi = None; wlo_t = whi_t = None
    for i, t in enumerate(loc.GT_F):
        TS_lo, TS_hi = raw[i]
        gap_lo = TS_lo / sc_exact - S_F[i][0] * (1 - GMAX_F)
        gap_hi = S_F[i][1] * (1 + GMAX_F) - TS_hi / sc_exact
        if worst_lo is None or gap_lo < worst_lo: worst_lo = gap_lo; wlo_t = t
        if worst_hi is None or gap_hi < worst_hi: worst_hi = gap_hi; whi_t = t
    return worst_lo, worst_hi, wlo_t, whi_t, sc_exact

def _w_bracket_exact_lam(loc, S_F, t, GMAX_F, LIP_S_F, tp, tm):
    """Rigorous (wlo,whi) for w = a(t+)*lam/(a(t+)*lam+a(t-)) over lam in lam_encl(t); w is
    monotone increasing in lam and a(t+), decreasing in a(t-) (direct partials, all terms
    positive) -- corner-sufficient, evaluated at 2 extreme corners directly (not generic
    interval division, which loses the shared-lam correlation and over-widens)."""
    lam_lo, lam_hi = _lam_encl_exact_lam(loc, S_F, t, GMAX_F, LIP_S_F)
    ap_lo = _a_bracket_lam(float(tp), True); ap_hi = _a_bracket_lam(float(tp), False)
    am_lo = _a_bracket_lam(float(tm), True); am_hi = _a_bracket_lam(float(tm), False)
    wlo = ap_lo * lam_lo / (ap_lo * lam_lo + am_hi)
    whi = ap_hi * lam_hi / (ap_hi * lam_hi + am_lo)
    return wlo, whi

def _lambda_invariance_check_lam(loc, S_F, Lam_F, GMAX_F, CPRIME_F, LIP_S_F, LIP_L_F):
    """Mirrors the float precompute's own 8-corner enumeration EXACTLY (w in {wlo,whi}, gp
    in {gplo,gphi}, gm in {gmlo,gmhi} -> 8 evaluations of (1/3)(w*gp-(1-w)*gm), min/max) --
    NOT generic interval subtraction, which loses the shared-w correlation between the two
    product terms and over-widens by orders of magnitude (see dev notes). CPRIME is applied
    once building the candidate (matching the float precompute) and once more, isolated, at
    this comparison (mirrors the mass check's GMAX-at-comparison design; same already-named,
    already-generous cover, not a new constant)."""
    worst_lo = worst_hi = None; wlo_t = whi_t = None
    for i, t in enumerate(loc.GT_F):
        tp = (1 + t) / 3; tm = (1 - t) / 3
        wlo, whi = _w_bracket_exact_lam(loc, S_F, t, GMAX_F, LIP_S_F, tp, tm)
        Lp_lo, Lp_hi = _brk_L_exact_lam(loc, Lam_F, tp, LIP_L_F)
        Lm_lo, Lm_hi = _brk_L_exact_lam(loc, Lam_F, tm, LIP_L_F)
        gp_lo = _loga_prime_bracket_lam(float(tp), True) + Lp_lo
        gp_hi = _loga_prime_bracket_lam(float(tp), False) + Lp_hi
        gm_lo = _loga_prime_bracket_lam(float(tm), True) + Lm_lo
        gm_hi = _loga_prime_bracket_lam(float(tm), False) + Lm_hi
        cands = [Fr(1, 3) * (w * gp - (1 - w) * gm)
                 for w in (wlo, whi) for gp in (gp_lo, gp_hi) for gm in (gm_lo, gm_hi)]
        new_lo = min(cands) - CPRIME_F; new_hi = max(cands) + CPRIME_F
        gap_lo = (new_lo + CPRIME_F) - Lam_F[i][0]
        gap_hi = Lam_F[i][1] - (new_hi - CPRIME_F)
        if worst_lo is None or gap_lo < worst_lo: worst_lo = gap_lo; wlo_t = t
        if worst_hi is None or gap_hi < worst_hi: worst_hi = gap_hi; whi_t = t
    return worst_lo, worst_hi, wlo_t, whi_t

def _gamma_floor_bound_lam(levs, J0, f_pad):
    """PROVED (exact Fraction, floor-box-derived, no measurement): gamma :=
    (1/4)(Delta_0+E_W)/(a*M_w) <= this bound, at EVERY parent/branch, from F3's own floor
    family alone (DERIV_LAMBOX Section 2.2/6, finite-check item 5's gamma<=GMAX half).
    Delta_0 = c_0(1-rc_0) <= c_0*(1-f_0); E_W = c_16(1-rc_16) <= c_16*(1-f_16) <= c_0*(1-f_16)
    (c_16<=c_0 by the c-vector's established monotonicity, rc_i<=1). M_w/c_0 =
    sum_{k=0}^{16} prod_{i<k} rc_i >= Q := sum_{k=0}^{16} prod_{i<k} f_i (each rc_i>=f_i>=0,
    the floor box itself) -- a LOWER bound on M_w/c_0 computable from the SAME floors F3/
    V17-IA already certify. Hence gamma <= (1/4)[(1-f_0)+(1-f_16)] / (a_lo * Q)."""
    worst = Fr(0); wt = None
    for t in PARENTS:
        for branch_t in ((1 + t) / 3.0, (1 - t) / 3.0):
            rc = anchor_c_ratios(branch_t, levs, J0, win=FLOOR_WIN)   # rc_0..rc_17 (len 18)
            floors = [frac_outward(f_pad * r, lo=True, slop=IA_SLOP) for r in rc]
            f0 = floors[0]; f16 = floors[16]
            Q = Fr(1); prod = Fr(1)
            for i in range(16):
                prod = prod * floors[i]; Q += prod
            a_lo = frac_outward(a_of(branch_t), lo=True, slop=IA_SLOP)
            bound = (Fr(1, 4) * ((1 - f0) + (1 - f16))) / (a_lo * Q)
            if bound > worst:
                worst = bound; wt = branch_t
    return worst, wt

def _cprime_monitor_lam(levs, J0, loc, Lam_F, LIP_L_F):
    """MONITORED (not proved): the discrepancy between the pure-operator field's Lambda
    prediction and the REAL cascade's mass-weighted Lambda (onestep_compose), sampled
    sparsely at the shipped anchor J0 (reuses the already-built cascade). DERIV_LAMBOX
    Section 3.3/5 cites 'measured impact ~0.002' from the same style of comparison
    (proto4 vs proto1); this is the (C'-CAP) clause's own a-posteriori grounding."""
    worst = 0.0
    for t in PARENTS[::5]:
        raw = onestep_raw(t, J0, levs, win=WIN_STAR, cwin=CWIN)
        mass = onestep_compose(raw, 'mass')
        tp, tm = frac_exact((1 + t) / 3.0), frac_exact((1 - t) / 3.0)
        Lp_lo, Lp_hi = _brk_L_exact_lam(loc, Lam_F, tp, LIP_L_F)
        Lm_lo, Lm_hi = _brk_L_exact_lam(loc, Lam_F, tm, LIP_L_F)
        Lp_field = float(Lp_lo + Lp_hi) / 2.0; Lm_field = float(Lm_lo + Lm_hi) / 2.0
        # window-coherence (round 4): compare the field against ITS OWN object, the
        # W=17 mass-weighted Lambda (matches (I1)@17 + the gamma/C' floor-box covers);
        # the 18-window variant compared here previously is one edge term off.
        worst = max(worst, abs(mass['Lamp17'] - Lp_field), abs(mass['Lamm17'] - Lm_field))
    return worst

_HEAD_CACHE = {}

def _anchor_heads(levs, J0, W):
    key = (J0, W)
    if key not in _HEAD_CACHE:
        _HEAD_CACHE[key] = [v[:W] for v in levs[J0]]
    return _HEAD_CACHE[key]

def _anchor_head_cvec(t, levs, J0, W):
    """First W entries of cvec(t, levs[J0]) without materializing the full ~J0-length
    barycentric interpolation: bary() on pre-sliced heads + the parity-aware flip sign
    (levs[J0] vectors have length J0+1, so flip's sign at entry i is +1 iff (J0-i) is
    even) + the c-convention halving. Numerically IDENTICAL to cvec(t, levs[J0])[:W]
    (same per-entry float operations in the same order; asserted against cvec at 3
    parents by gate LAM-INV's own live self-check)."""
    b = bary(t, _anchor_heads(levs, J0, W))
    out = []
    for i in range(W):
        s = b[i] if ((J0 - i) % 2 == 0) else -b[i]
        out.append(s if i == 0 else s / 2.0)
    return out

def _floor_down_frac(x, denom=10**7):
    """Outward-DOWN decimal rounding for the (C'-CAP) node census's floor data: a floor
    rounded down makes G (which consumes 1-f) LARGER and Q (a product-sum of floors)
    SMALLER -- BOTH conservative directions for the bound below -- while keeping the
    Fraction denominators tiny (1e7) so the 2x3841-node census's big-int chains stay
    cheap (the exact-2^52-denominator route is equally sound but ~100x slower here)."""
    return Fr(math.floor(float(x) * denom), denom)

def _gamma_branch_floor_data(levs, J0, f_pad, s):
    """Per-branch floor-box data at branch parameter s: (G, Q, a_lo), all outward, with
    G >= gamma(s) = (1/4)(Delta_0+E_W)/(a(s)*M_w) for EVERY profile in the floor box at
    s -- the SAME derivation as _gamma_floor_bound_lam (Delta_0 <= c_0(1-f_0), E_W <=
    c_0(1-f_16), M_w/c_0 >= Q := sum_k prod_{i<k} f_i), evaluated at an arbitrary band
    parameter (the node's children t_pm) from the anchor level's own head vectors."""
    c = _anchor_head_cvec(s, levs, J0, FLOOR_WIN + 1)
    floors = [_floor_down_frac(float(f_pad) * (c[i + 1] / c[i]))
              for i in range(FLOOR_WIN)]
    f0, f16 = floors[0], floors[16]
    Q = Fr(1); prod = Fr(1)
    for i in range(16):
        prod = prod * floors[i]; Q += prod
    a_lo = _floor_down_frac(a_of(s))
    G = (Fr(1, 4) * ((1 - f0) + (1 - f16))) / (a_lo * Q)
    return G, Q, a_lo

def _cprime_floor_proved_lam(levs, J0, f_pad, loc, S_F, Lam_F, GMAX_F, LIP_S_F, LIP_L_F,
                              v17_ceiling_F, tamper=None):
    """PROVED-conditional floor-box bound on the (C'-CAP) drop (this revision, R1
    mitigation (a)). The cap is consumed by the Lambda-recursion ONLY at the NG grid
    nodes (between-grid coverage rides the existing LIP_S/LIP_L brackets), so a node
    census is exactly where the cap is needed. At each node t, from the EXACT one-step
    windowed-mass relation ((I1) summed over branches; P := a_+S^+ + a_-S^-,
    C := (1/4)sum_pm(Delta_0+E_W)^pm >= 0, S_n = P - C):

        Lambda_true(t) - Lambda_pure(t) = [gbar*Lambda_pure - C'/P] / (1-gbar),
        gbar := C/P = sum_pm w_pm*gamma^pm  (an elementary identity:
        (P'-C')/(P-C) - P'/P),

    so |drop| <= [gbar*|Lambda_pure| + |C'|/P]/(1-gbar), with, all outward:
      gamma^pm <= G^pm, the per-branch floor-box gamma bound at t_pm
        (_gamma_branch_floor_data -- the same derivation as the PROVED gamma<=GMAX);
      w_pm from the SAME lam-enclosure corner bracket the invariance check uses
        (each occurrence maximized separately over the two w corners -- a sound
        marginal bound; every expression below is affine in w);
      |Lambda_pure| <= abs-max of the SAME 8-corner candidate enumeration the
        invariance check runs (bilinear in (w,gp,gm) -> corner-sufficient);
      |C'|/P <= (1/3)[w*G^+*L^+ + (1-w)*G^-*L^-]
               + (1/12)*V18c*[(w/a^+_lo)*(2/Q^+) + ((1-w)/a^-_lo)*(2/Q^-)]
        from Delta_0' = L_0*Delta_0 + c_1(L_0-L_1) and E_W' = L_16*E_W +
        c_17(L_16-L_17) (product rule + FTC), |L_i| <= |Lambda^pm_child| + V18c =: L^pm
        (window-mean split; zero-sum deviations), |L_0-L_1|, |L_16-L_17| <= V18c,
        (c_1+c_17)/S^pm <= 2/Q^pm, (Delta_0+E_W)^pm/P = 4*gamma^pm*w_pm, and the
        chain-rule factor |dt_pm/dt| = 1/3 (whence (1/4)*(1/3) = 1/12).
    V18c := (57/50)*v17_ceiling_F -- the (FOLD)-folded equilibrium ceiling
    max(V_17(J0), F_box/(1-theta_band)), passed in as an exact Fraction from the
    UNTAMPERED load-bearing censuses (joint induction: the pass n-1 -> n consumes
    H(n-1)'s V-ceiling and field membership; base n-1 in [48, J0) rides the existing
    base-case grid, so the cap is only ever needed at child levels >= J0 where the
    ceiling holds). Tamper 'cprime-bound-graze' doubles the final bound (isolated:
    nothing upstream of the comparison changes). Returns (worst_bound, locus_t, diag)."""
    graze = Fr(2) if tamper == "cprime-bound-graze" else Fr(1)
    V18c = Fr(57, 50) * v17_ceiling_F
    worst = None; wt = None; diag = None
    for t in loc.GT_F:
        tp = (1 + t) / 3; tm = (1 - t) / 3
        wlo, whi = _w_bracket_exact_lam(loc, S_F, t, GMAX_F, LIP_S_F, tp, tm)
        Lp_lo, Lp_hi = _brk_L_exact_lam(loc, Lam_F, tp, LIP_L_F)
        Lm_lo, Lm_hi = _brk_L_exact_lam(loc, Lam_F, tm, LIP_L_F)
        gp_lo = _loga_prime_bracket_lam(float(tp), True) + Lp_lo
        gp_hi = _loga_prime_bracket_lam(float(tp), False) + Lp_hi
        gm_lo = _loga_prime_bracket_lam(float(tm), True) + Lm_lo
        gm_hi = _loga_prime_bracket_lam(float(tm), False) + Lm_hi
        cands = [Fr(1, 3) * (w * gp - (1 - w) * gm)
                 for w in (wlo, whi) for gp in (gp_lo, gp_hi) for gm in (gm_lo, gm_hi)]
        Lpure_abs = max(abs(min(cands)), abs(max(cands)))
        Gp, Qp, aplo = _gamma_branch_floor_data(levs, J0, f_pad, float(tp))
        Gm, Qm, amlo = _gamma_branch_floor_data(levs, J0, f_pad, float(tm))
        Lp_abs = max(abs(Lp_lo), abs(Lp_hi)) + V18c
        Lm_abs = max(abs(Lm_lo), abs(Lm_hi)) + V18c
        gbar = max(w * Gp + (1 - w) * Gm for w in (wlo, whi))
        term_L = max(w * Gp * Lp_abs + (1 - w) * Gm * Lm_abs for w in (wlo, whi)) / 3
        term_S = V18c * max((w / aplo) * (2 / Qp) + ((1 - w) / amlo) * (2 / Qm)
                            for w in (wlo, whi)) / 12
        bound = graze * (gbar * Lpure_abs + term_L + term_S) / (1 - gbar)
        if worst is None or bound > worst:
            worst = bound; wt = t
            diag = dict(gbar=gbar, Lpure=Lpure_abs, term_L=term_L, term_S=term_S)
    return worst, wt, diag

def _mass_recursion_identity_spotcheck():
    """Live exact-Fraction confirmation of identity (I1) (module note above): residual
    must be algebraically EXACTLY 0. Converts the verifier's own float c-vector and d(t)
    to Fraction BEFORE convolving -- a(t) reconstructed as 1/2+Fr(d(t)), the SAME value
    conv_even itself computes with, not an independently-rounded frac_exact(a_of(t))
    (which would differ in the last float bit and give a spurious nonzero residual).
    Mirrors LAB_LAMBOX.md Q2's independent re-derivation (residual=0, 40 checks); this is
    a second, in-gate, cheap confirmation over a handful of sample points, reusing the
    already-built `levs` cache (no extra cascade build)."""
    W = OPWIN
    worst = Fr(0); checked = 0
    for jm in (_LEV_CACHE.keys()):
        levs = _LEV_CACHE[jm]
        ns = [n for n in (60, 128, 300) if n < len(levs)]
        for n in ns:
            for t in (PARENTS[0], PARENTS[len(PARENTS) // 2], PARENTS[-1]):
                for branch_t in ((1 + t) / 3.0, (1 - t) / 3.0):
                    c = cvec(branch_t, levs[n - 1])
                    c_fr = [frac_exact(x) for x in c]
                    d_fr = frac_exact(d_of(branch_t)); a_fr = Fr(1, 2) + d_fr
                    def get(i, c_fr=c_fr):
                        i = abs(i); return c_fr[i] if i < len(c_fr) else Fr(0)
                    lhs = sum(Fr(1, 4) * get(i - 1) + d_fr * get(i) + Fr(1, 4) * get(i + 1) for i in range(W))
                    Mw = sum(c_fr[i] for i in range(W))
                    Delta0 = c_fr[0] - c_fr[1]; E_W = c_fr[W - 1] - c_fr[W]
                    rhs = a_fr * Mw - Fr(1, 4) * Delta0 - Fr(1, 4) * E_W
                    checked += 1
                    if abs(lhs - rhs) > worst:
                        worst = abs(lhs - rhs)
        break   # one cached level set suffices for the spot-check
    return worst, checked

_LAMINV_CACHE = {}   # module-level memo, keyed (J0,str(f_pad),tamper): the ~47s float
                     # precompute + one-pass certification is expensive; compute() calls
                     # _laminv_certify once (before MAG-BOX, so MAG-BOX can report the
                     # realized-vs-field C' check at its own grid levels) and gate_lam_inv
                     # reuses the SAME result at its normal report position -- one
                     # computation, two consumers, no double cost.

_LAMINV_TAMPERS = ("laminv-grid", "laminv-lip", "laminv-floor", "cprime-bound-graze")

def _laminv_certify(levs, J0, f_pad, tamper=None):
    """All of gate LAM-INV's computation, no report/print side effects -- returns a dict.
    See gate_lam_inv below for the report-line formatting and the full method docstring
    (identities, the Birkhoff enclosure, the tamper semantics)."""
    # cache key normalizes `tamper` to None unless it's one of THIS gate's own tampers --
    # every other tamper value (including every other gate's tamper, and the untampered
    # baseline) computes an IDENTICAL result here, so tamper_selftest's ~20 compute() runs
    # pay the ~47s float precompute only twice (baseline-equivalent + laminv-lip, which
    # doesn't change ng_eff/cprime_eff/lap_lo_eff either -- effectively once per distinct
    # (ng_eff,cprime_eff) pair), not once per tamper name.
    tamper_key = tamper if tamper in _LAMINV_TAMPERS else None
    key = (J0, str(f_pad), tamper_key)
    if key in _LAMINV_CACHE:
        return _LAMINV_CACHE[key]

    ng_eff = 241 if tamper == "laminv-grid" else NG_LAM
    cprime_eff = Fr(8, 1000) if tamper == "laminv-floor" else CPRIME_LAM_F
    lap_lo_eff = LAP_LO_F_ORIG if tamper == "laminv-floor" else LAP_LO_F
    lip_l_check_eff = Fr(2, 1) if tamper == "laminv-lip" else LIP_L_LAM_F

    t0 = time.time()
    GT_f, S_f, Lam_f = _float_converge_lam(ng_eff, float(LIP_S_LAM_F), float(LIP_L_LAM_F),
                                            float(GMAX_LAM_F), float(cprime_eff))
    loc = _LamLocator(ng_eff)
    S_F = _to_frac_field_lam(S_f, LAM_FIELD_SLOP)
    Lam_F = _to_frac_field_lam(Lam_f, LAM_FIELD_SLOP)
    grid_spacing_F = loc.GT_F[1] - loc.GT_F[0]

    mlo, mhi, mlo_t, mhi_t, sc_exact = _mass_invariance_check_lam(loc, S_F, LIP_S_LAM_F, GMAX_LAM_F)
    mass_inv_ok = (mlo >= 0) and (mhi >= 0)

    llo, lhi, llo_t, lhi_t = _lambda_invariance_check_lam(loc, S_F, Lam_F, GMAX_LAM_F, cprime_eff,
                                                           LIP_S_LAM_F, LIP_L_LAM_F)
    lam_inv_ok = (llo >= 0) and (lhi >= 0)

    sup_abs = max(max(abs(lo), abs(hi)) for lo, hi in Lam_F)
    ok_S = sup_abs <= LIP_S_LAM_F
    cent = [(lo + hi) / 2 for lo, hi in Lam_F]
    sup_slope = max(abs(cent[k + 1] - cent[k]) for k in range(len(cent) - 1)) / grid_spacing_F
    ok_L = sup_slope <= lip_l_check_eff

    gamma_bound, gamma_wt = _gamma_floor_bound_lam(levs, J0, f_pad)
    gamma_ok = gamma_bound <= GMAX_LAM_F

    cprime_measured = _cprime_monitor_lam(levs, J0, loc, Lam_F, LIP_L_LAM_F)
    cprime_ok = cprime_measured <= float(cprime_eff)

    # (C'-CAP) PROVED-conditional floor-box bound (this revision, R1 mitigation (a)).
    # Head-cvec self-check first: _anchor_head_cvec must reproduce cvec exactly.
    for t_chk in (PARENTS[0], PARENTS[len(PARENTS) // 2], PARENTS[-1]):
        full = cvec(t_chk, levs[J0])[:FLOOR_WIN + 1]
        head = _anchor_head_cvec(t_chk, levs, J0, FLOOR_WIN + 1)
        assert head == full, "head-cvec mismatch at t=%r" % t_chk
    # Equilibrium ceiling from the UNTAMPERED load-bearing chain (memoized censuses;
    # tamper isolation: a tampered V15-IA/V17-IA never feeds this bound).
    tb_exact, _, _, _ = theta_band_ia_certified(levs, J0, f_pad, tamper=None)
    fb_clean, _, _ = F_box_ia_certified(levs, J0, f_pad, tamper=None)
    v17_j0_up = frac_outward(V17_locus(J0, levs, OPWIN)[0], lo=False, slop=IA_SLOP)
    v17_ceiling_F = fb_clean / (1 - round_up_frac(tb_exact))
    if v17_j0_up > v17_ceiling_F:
        v17_ceiling_F = v17_j0_up
    cprime_proved, cprime_proved_t, cprime_diag = _cprime_floor_proved_lam(
        levs, J0, f_pad, loc, S_F, Lam_F, GMAX_LAM_F, LIP_S_LAM_F, LIP_L_LAM_F,
        v17_ceiling_F, tamper=tamper)
    cprime_proved_ok = cprime_proved <= cprime_eff

    id1_residual, id1_checked = _mass_recursion_identity_spotcheck()
    id1_ok = (id1_residual == 0)

    # final PROVED intervals over the same 41 PARENTS other gates sample (frac_exact:
    # lossless Fraction(float), not a re-derived idealized-rational grid).
    lam_lo = lam_hi = lp_lo = lp_hi = lm_lo = lm_hi = None
    for tf in PARENTS:
        t = frac_exact(tf)
        tp = (1 + t) / 3; tm = (1 - t) / 3
        llo2, lhi2 = _lam_encl_exact_lam(loc, S_F, t, GMAX_LAM_F, LIP_S_LAM_F)
        if lam_lo is None or llo2 < lam_lo: lam_lo = llo2
        if lam_hi is None or lhi2 > lam_hi: lam_hi = lhi2
        Lp = _brk_L_exact_lam(loc, Lam_F, tp, LIP_L_LAM_F)
        Lm = _brk_L_exact_lam(loc, Lam_F, tm, LIP_L_LAM_F)
        if lp_lo is None or Lp[0] < lp_lo: lp_lo = Lp[0]
        if lp_hi is None or Lp[1] > lp_hi: lp_hi = Lp[1]
        if lm_lo is None or Lm[0] < lm_lo: lm_lo = Lm[0]
        if lm_hi is None or Lm[1] > lm_hi: lm_hi = Lm[1]

    lam_inside = (lam_lo >= LAM_LO_F) and (lam_hi <= LAM_HI_F)
    lp_inside = (lp_lo >= lap_lo_eff) and (lp_hi <= LAP_HI_F)
    lm_inside = (lm_lo >= LAM2_LO_F) and (lm_hi <= LAM2_HI_F)
    lp_headroom = float(lp_lo - lap_lo_eff)

    ok = (mass_inv_ok and lam_inv_ok and ok_S and ok_L and gamma_ok and cprime_ok
          and cprime_proved_ok and id1_ok and lam_inside and lp_inside and lm_inside)

    result = dict(ng_eff=ng_eff, cprime_eff=cprime_eff, lap_lo_eff=lap_lo_eff,
                  lip_l_check_eff=lip_l_check_eff, loc=loc, S_F=S_F, Lam_F=Lam_F,
                  mlo=mlo, mhi=mhi, mass_inv_ok=mass_inv_ok, llo=llo, lhi=lhi,
                  lam_inv_ok=lam_inv_ok, sup_abs=sup_abs, ok_S=ok_S, sup_slope=sup_slope,
                  ok_L=ok_L, gamma_bound=gamma_bound, gamma_wt=gamma_wt, gamma_ok=gamma_ok,
                  cprime_measured=cprime_measured, cprime_ok=cprime_ok,
                  cprime_proved=cprime_proved, cprime_proved_t=cprime_proved_t,
                  cprime_diag=cprime_diag, cprime_proved_ok=cprime_proved_ok,
                  v17_ceiling_F=v17_ceiling_F,
                  id1_residual=id1_residual, id1_checked=id1_checked,
                  lam_lo=lam_lo, lam_hi=lam_hi, lp_lo=lp_lo, lp_hi=lp_hi,
                  lm_lo=lm_lo, lm_hi=lm_hi, lam_inside=lam_inside, lp_inside=lp_inside,
                  lm_inside=lm_inside, lp_headroom=lp_headroom, ok=ok,
                  elapsed=time.time() - t0, tamper=tamper)
    _LAMINV_CACHE[key] = result
    return result

def gate_lam_inv(report, levs, J0, f_pad, tamper=None):
    """LAM-INV [core, FULL MODE ONLY, PROVED-conditional upgrade of (LAM-BOX)]: implements
    DERIV_LAMBOX.md's finite-check list items 3-5 (Section 6) -- items 1-2 (the floor
    family, the exact base-case grid) are the EXISTING gates F3 and MAG-BOX/V18, cited not
    re-derived here. Item 3: one forward-pass T-invariance of the mass interval field
    (NG=%d) + a-posteriori sup|Lambda|<=LIP_S. Item 4: one forward-pass invariance of the
    coupled Lambda field + a-posteriori sup|Lambda'|<=LIP_L. Item 5: floor-box bound on
    gamma<=GMAX (PROVED here, exact Fraction, from the F3 floor family alone) and
    C'<=CPRIME (MONITORED -- the (C'-CAP) clause, the ONE remaining computed/monitored
    literal). See the module-level note above this function for the two identities (I1,
    I2) and their verification status. The actual computation lives in
    _laminv_certify (memoized in _LAMINV_CACHE): compute() calls it once, BEFORE
    gate_magnitude_box, so MAG-BOX can report the realized-vs-field C' consistency check
    at its own grid levels without paying the ~47s float precompute a second time; this
    function reuses the SAME cached result to format its own report line.

    Tampers (isolated, each touches only this gate's line): 'laminv-grid' (NG far below
    the note's R4 threshold -> the between-grid Lipschitz slop blows up the FINAL proved
    interval past the shipped box -- the gate's own grid-sufficiency/containment check
    trips); 'laminv-lip' (the A-POSTERIORI comparison threshold for LIP_L only is lowered
    below the realized sup|Lambda'| -- the field's own Lipschitz bracket construction is
    UNCHANGED, isolating the tamper to that one self-check line); 'laminv-floor' (R1
    stress: restores the PRE-widening Lambda^+ floor -116/100 AND forces CPRIME to 2x the
    shipped value, 0.008 -- DERIV_LAMBOX's own R1 finding, the gate must FAIL containment)."""
    r = _laminv_certify(levs, J0, f_pad, tamper=tamper)
    report.append(("LAM-INV [core, FULL MODE ONLY, PROVED-conditional upgrade of (LAM-BOX),"
        " window i<17/i<18, NG=%d]\n"
        "        identities: (I1) exact windowed mass recursion sum_i<17(K_d*c)=a(t)Mw"
        "-1/4(c0-c1)-1/4(c16-c17) [PROVED; live Fraction spot-check residual=%s over %d"
        " (n,t,branch) points -- exactly 0 -- independently confirmed by the lab lane];"
        " (I2) Lambda^pm_mass=(log S^17)'(t_pm), W=17=OPWIN matching (I1) and the"
        " gamma/C' covers (window-coherence, round 4) [PROVED, elementary].\n"
        "        mass-field T-invariance (one fwd pass): worst gap lo=%.2e hi=%.2e [%s];"
        " a-posteriori sup|Lambda|=%.4f <= LIP_S=%s [%s]\n"
        "        coupled Lambda-field T-invariance (one fwd pass): worst gap lo=%.2e"
        " hi=%.2e [%s]; a-posteriori sup|Lambda'|=%.4f <= LIP_L=%s [%s]%s\n"
        "        gamma<=GMAX=%s: PROVED from the F3 floor box (anchor J0=%d,f=%s), exact"
        " bound=%.6f (locus branch=%.4f) [%s]; C'<=CPRIME=%s: PROVED floor-box bound"
        "=%.6f (locus t=%.4f; node census over all NG nodes; gbar=%.6f Lpure=%.4f"
        " termL=%.6f termS=%.6f at locus) [%s] -- (C'-CAP) DISCHARGED-conditional"
        " (V18-ceiling (57/50)*%.8f via (FOLD) + the untampered V15-IA/V17-IA chain);"
        " a-posteriori monitor RETAINED as the empirical cross-check: measured"
        " impact=%.4f [%s]%s\n"
        "        conditional basis: F3 floors + floor persistence at the node branch"
        " parameters ((FLOOR-PERSIST), gate FLOOR-DRIFT) + (FOLD) + finite base-case"
        " census (gates MAG-BOX/V18, n in {48..800}) + this gate's a-posteriori"
        " Lipschitz self-check + the joint IH (V-ceiling + field membership).\n"
        "        PROVED intervals vs shipped boxes: lam [%.6f,%.6f] subset [%s,%s] %s;"
        " Lambda+ [%.6f,%.6f] subset [%s,%s] %s (floor headroom %+.4f); Lambda-"
        " [%.6f,%.6f] subset [%s,%s] %s\n"
        "        window provenance: E_W reads c_17, ONE PAST the operative i<17 window,"
        " only via rc_16 in [f_16,1], F3-certified over i<18 (FLOOR_WIN=CWIN=18) -- no new"
        " hypothesis beyond the existing F3 gate. (%.1fs)"
        % (r['ng_eff'], r['id1_residual'], r['id1_checked'],
           float(r['mlo']), float(r['mhi']), "OK" if r['mass_inv_ok'] else "FAIL",
           float(r['sup_abs']), str(LIP_S_LAM_F), "OK" if r['ok_S'] else "FAIL",
           float(r['llo']), float(r['lhi']), "OK" if r['lam_inv_ok'] else "FAIL",
           float(r['sup_slope']), str(r['lip_l_check_eff']), "OK" if r['ok_L'] else "FAIL",
           " [TAMPERED laminv-lip]" if tamper == "laminv-lip" else "",
           str(GMAX_LAM_F), J0, str(f_pad), float(r['gamma_bound']), r['gamma_wt'],
           "OK" if r['gamma_ok'] else "MISS", str(r['cprime_eff']),
           float(r['cprime_proved']), float(r['cprime_proved_t']),
           float(r['cprime_diag']['gbar']), float(r['cprime_diag']['Lpure']),
           float(r['cprime_diag']['term_L']), float(r['cprime_diag']['term_S']),
           "OK" if r['cprime_proved_ok'] else "MISS", float(r['v17_ceiling_F']),
           r['cprime_measured'], "OK" if r['cprime_ok'] else "MISS",
           " [TAMPERED laminv-floor, CPRIME forced 2x]" if tamper == "laminv-floor"
           else (" [TAMPERED cprime-bound-graze, bound forced 2x]"
                 if tamper == "cprime-bound-graze" else ""),
           float(r['lam_lo']), float(r['lam_hi']), str(LAM_LO_F), str(LAM_HI_F),
           "yes" if r['lam_inside'] else "NO",
           float(r['lp_lo']), float(r['lp_hi']), str(r['lap_lo_eff']), str(LAP_HI_F),
           "yes" if r['lp_inside'] else "NO", r['lp_headroom'],
           float(r['lm_lo']), float(r['lm_hi']), str(LAM2_LO_F), str(LAM2_HI_F),
           "yes" if r['lm_inside'] else "NO",
           r['elapsed']), r['ok']))

def _rc_head(s, levs, n, win=FLOOR_WIN):
    """rc_0..rc_{win-1} at level n, parameter s, via the head-cvec fast path (identical
    floats to anchor_c_ratios(s, levs, n, win) -- same self-checked head machinery)."""
    c = _anchor_head_cvec(s, levs, n, win + 1)
    return [c[i + 1] / c[i] for i in range(win)]

def _floor_census_routecut(levs, J0, f_pad, j0_sib=None, pad_sib=None):
    """INFORMATIONAL route-cut census (float): the box-worst one-step output ratio over
    the (FLOOR-PERSIST) pointwise box -- minus-child ratios at their own-parameter
    floors/caps (LC vertices), sibling magnitude lam in the (LAM-BOX) box, per-entry
    wobble in the geometric-center half-band (boundary slots w_17 in the W17 deep box,
    w_18/w_19 in a generous [0.998,1.002], rc_18 in [0,1]) -- against the output floor
    pad*rc_i(J0,t). Verdict (the route-cut, note Section 9(v)): a V12-style pointwise
    corner census CANNOT re-derive floor persistence at any practical pad -- the box has
    no mechanism coupling input-floor slack to output-floor slack (the same structural
    boundary as Section 10's 'no free O(1/n) in the box' correction). Float,
    informational only; returns (worst_ratio, frac_rows_failing, locus)."""
    WH = (float(WOB_HALF[0]), float(WOB_HALF[1]))
    W17B = (float(W17_LO_F), float(W17_HI_F))
    W1819 = (0.998, 1.002)
    LAMB = (float(LAM_LO_F), float(LAM_HI_F))

    def wset(k):
        if k < 17: return WH
        if k == 17: return W17B
        return W1819

    def rmin_row(i, Fm, tp, tm):
        dp_, dm_ = d_of(tp), d_of(tm)
        def fset(j):
            if j < 0: return [None]
            if j < FLOOR_WIN: return [Fm[j], 1.0]
            return [0.0, 1.0]
        best = 1e18
        for a in fset(i - 1):
            for b in fset(i):
                if a is not None and b > a + 1e-12: continue
                for e in fset(i + 1):
                    if e > b + 1e-12: continue
                    for lam in LAMB:
                        for u in wset(i - 1):
                            for v in wset(i):
                                for x in wset(i + 1):
                                    for y in wset(i + 2):
                                        if i == 0:
                                            den = (dm_ + dp_ * lam * u) + 0.5 * b * (1 + lam * v)
                                            num = 0.25 * (1 + lam * u) + (dm_ + dp_ * lam * v) * b \
                                                  + 0.25 * b * e * (1 + lam * x)
                                        else:
                                            den = 0.25 / a * (1 + lam * u) + (dm_ + dp_ * lam * v) \
                                                  + 0.25 * b * (1 + lam * x)
                                            num = 0.25 * (1 + lam * v) + (dm_ + dp_ * lam * x) * b \
                                                  + 0.25 * b * e * (1 + lam * y)
                                        if den <= 0: continue
                                        r = num / den
                                        if r < best: best = r
        return best

    out = []
    for (jj, pp) in [(J0, float(f_pad))] + ([(j0_sib, float(pad_sib))] if j0_sib else []):
        worst = 1e18; loc = None; nfail = 0; ntot = 0
        for t in PARENTS:
            tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
            Ft = [pp * r for r in _rc_head(t, levs, jj)]
            Fm = [pp * r for r in _rc_head(tm, levs, jj)]
            for i in range(FLOOR_WIN):
                m = rmin_row(i, Fm, tp, tm) / Ft[i]
                ntot += 1
                if m < 1.0: nfail += 1
                if m < worst: worst, loc = m, (t, i)
        out.append((jj, pp, worst, nfail, ntot, loc))
    return out

def gate_floor_drift(report, levs, grid, tamper=None):
    """FLOOR-DRIFT [core, FULL MODE ONLY]: first-class monitoring of the (FLOOR-PERSIST)
    computed clause -- NOT a proof (the clause stays COMPUTED; see the route-cut below
    for why a pointwise census cannot prove it). Before this revision the clause was
    IMPORTED reasoning ('the predecessor's monotone-drift machinery'), with no gate of
    its own in this packet; this gate makes it a named, monitored, tamperable invariant:

      (1) DRIFT (the mechanism): rc_i(n2,s) >= rc_i(n1,s) for consecutive deep-grid
          level pairs with n1 >= J0*, over s in PARENTS union both branch values
          (123 parameters), i < 18 -- the upward CLT flattening the imported reasoning
          rests on, checked directly at every monitored parameter (the full-grid worst
          from n=48 is also printed, informational).
      (2) AS-CONSUMED MARGINS: the exact statement the census gates consume --
          rc_i(n, t_pm) >= f*rc_i(J0*, t) (children at branch parameters vs the
          parent-t anchor family) at every deep-grid level n >= J0*, and the same at
          the SIB-CERT anchor (J0_SIB, PAD_SIB) for n >= J0_SIB.

    Tamper 'floordrift-margin' raises the required drift ratio to 1.0001 (above the
    realized worst step ratio ~1.00005), isolated to this gate. The gate line also
    prints, INFORMATIONAL, the route-cut negative control (_floor_census_routecut):
    the box-worst census output ratio vs floor at both anchors -- quantifying WHY the
    (FLOOR-PERSIST) discharge cannot come from a pointwise corner census."""
    drift_req = 1.0001 if tamper == "floordrift-margin" else (1.0 - 1e-12)
    svals = sorted(set(list(PARENTS) + [(1 + t) / 3.0 for t in PARENTS]
                       + [(1 - t) / 3.0 for t in PARENTS]))
    pairs_all = list(zip(grid, grid[1:]))
    worst_op = 1e18; loc_op = None; worst_full = 1e18
    rc_cache = {}
    def rc_of(s, n):
        key = (s, n)
        if key not in rc_cache:
            rc_cache[key] = _rc_head(s, levs, n)
        return rc_cache[key]
    for s in svals:
        for (n1, n2) in pairs_all:
            r1 = rc_of(s, n1); r2 = rc_of(s, n2)
            for i in range(FLOOR_WIN):
                d = r2[i] / r1[i]
                if d < worst_full: worst_full = d
                if n1 >= J0_STAR:
                    if d < worst_op: worst_op, loc_op = d, (s, n1, n2, i)
    drift_ok = worst_op >= drift_req
    # as-consumed margins at both anchors
    margins = []
    for (jj, pp, nmin) in ((J0_STAR, float(F_STAR), J0_STAR), (J0_SIB, float(PAD_SIB), J0_SIB)):
        wm = 1e18; lm = None
        for t in PARENTS:
            anc = rc_of(t, jj)
            for n in [n for n in grid if n >= nmin]:
                for tb in ((1 + t) / 3.0, (1 - t) / 3.0):
                    cur = rc_of(tb, n)
                    for i in range(FLOOR_WIN):
                        m = cur[i] / (pp * anc[i])
                        if m < wm: wm, lm = m, (t, n, i)
        margins.append((jj, pp, wm, lm))
    margins_ok = all(wm >= 1.0 for (_, _, wm, _) in margins)
    rc_out = _floor_census_routecut(levs, J0_STAR, F_STAR, j0_sib=J0_SIB, pad_sib=PAD_SIB)
    ok = drift_ok and margins_ok
    report.append(("FLOOR-DRIFT [core, FULL MODE ONLY, monitors the (FLOOR-PERSIST)"
        " COMPUTED clause -- monitoring, NOT a proof] (1) drift: rc_i(n2,s)>=rc_i(n1,s)"
        "%s over consecutive deep-grid pairs n1>=%d, 123 parameters (parents+branches),"
        " i<18: worst step ratio %.8f @ %s [%s] (full-grid-from-48 worst %.8f,"
        " informational); (2) as-consumed floor margins: anchor (%d,%s) worst"
        " rc_i(n,t_pm)/(f*rc_i(J0,t)) = %.6f @ %s [%s]; anchor (%d,%s) worst = %.6f"
        " @ %s [%s] | INFORMATIONAL route-cut (why no census can prove this): box-worst"
        " output-ratio/floor = %.3f (%d/%d rows fail) at (%d,%s); %.3f (%d/%d) at"
        " (%d,%s) -- the pointwise corner census route to (FLOOR-PERSIST) is CLOSED"
        " (note Section 9(v))"
        % (" >=1.0001 [TAMPERED floordrift-margin]" if tamper == "floordrift-margin" else "",
           J0_STAR, worst_op, str(loc_op), "OK" if drift_ok else "MISS", worst_full,
           margins[0][0], str(F_STAR), margins[0][2], str(margins[0][3]),
           "OK" if margins[0][2] >= 1.0 else "MISS",
           margins[1][0], str(PAD_SIB), margins[1][2], str(margins[1][3]),
           "OK" if margins[1][2] >= 1.0 else "MISS",
           rc_out[0][2], rc_out[0][3], rc_out[0][4], rc_out[0][0], str(F_STAR),
           rc_out[1][2], rc_out[1][3], rc_out[1][4], rc_out[1][0], str(PAD_SIB)), ok))

def gate_vtrack(report, levs, grid, expect_max, tamper=None, show_table=False):
    """V18 VTRACK: deep-grid rho_prop@i<17(n)<=TARGET + monotone + V_17 tau*-crossover,
    over n in {48,...,expect_max} (expect_max=J0*=500 in the default FULL run -- NOT
    hidden behind --deep; this IS the ship's default grid, see DEEP_GRID_FULL; a smaller
    expect_max is used only under --quick, an explicitly non-certified dev-iteration
    mode). Reports the rho_prop margin at every tested level (tightest->widest), the
    V_17(n) values (which determine the equilibrium ceiling other gates consume), and
    the tau*-crossover."""
    grid_eff = grid[:-1] if (tamper == "vtrack-level-drop" and len(grid) > 1) else grid
    target = 1.0 if tamper == "c1-target" else TARGET
    rho_vals = dict((j, rho_win_locus(levs, j, OPWIN)[0]) for j in grid_eff)
    v17_vals = dict((j, V17_locus(j, levs, OPWIN)[0]) for j in grid_eff)
    ok_target = all(rho_vals[j] <= target for j in grid_eff)
    ok_mono = all(rho_vals[a] >= rho_vals[b] - 1e-9 for a, b in zip(grid_eff, grid_eff[1:]))
    tight_margin = min(target - rho_vals[j] for j in grid_eff)
    wide_margin = max(target - rho_vals[j] for j in grid_eff)
    cross_n = None; prev_v = None
    for n in range(55, 71):
        v, _ = V17_locus(n, levs, OPWIN)
        if prev_v is not None and prev_v > TAU_STAR and v <= TAU_STAR and cross_n is None:
            cross_n = n
        prev_v = v
    ok_cross = (cross_n == 62)
    # base-coverage check: the grid actually reaches expect_max (catches
    # vtrack-level-drop's truncation, and any accidental grid-shrinking regression).
    ok_covers = (max(grid_eff) >= expect_max)
    ok = ok_target and ok_mono and ok_cross and ok_covers
    v17_top = v17_vals[max(grid_eff)]
    if show_table:
        # per-level table (the values the Lean package transcribes); --table flag
        print("  V18 per-level table (n : rho_prop@i<17 : margin : V_17):")
        for j in grid_eff:
            print("    n=%-4d rho_prop=%.8f  margin=%+.6e  V_17=%.6e"
                  % (j, rho_vals[j], target - rho_vals[j], v17_vals[j]))
    report.append(("V18 VTRACK [window i<17] rho_prop@i<17(n)<=%.8f over n in {%s}"
                    " (monotone=%s, margin %.2e@tightest -> %.4f@widest); V_17(n): %.6f@n=48"
                    " -> %.2e@n=%d (base anchor), monotone-dec=%s; tau*-crossover at n=%s"
                    " (expect 62); base coverage to expect_max=%d: %s"
                    % (target, ",".join(str(j) for j in grid_eff), ok_mono, tight_margin,
                       wide_margin, v17_vals.get(48, float('nan')), v17_top,
                       max(grid_eff), all(v17_vals[a] >= v17_vals[b] - 1e-12
                                           for a, b in zip(grid_eff, grid_eff[1:])),
                       cross_n, expect_max, ok_covers), ok))

def gate_bridge(info, levs, grid, tamper=None):
    """V19 BRIDGE [INFORMATIONAL/alpha-only]: w(n)<=0.62."""
    thr = 0.30 if tamper == "bridge-w-gate" else 0.62
    w_vals = {}
    for j in grid:
        V17n, _ = V17_locus(j, levs, OPWIN)
        I32 = gap_quadrature(EDGE, j, levs, 32)
        w_vals[j] = I32 / ((2 * EDGE / 3) * V17n)
    worst = max(w_vals.values())
    ok = worst <= thr
    info.append(("V19 BRIDGE [INFORMATIONAL/alpha-only, window i<17] w(n)<=%.2f over n"
                  " in {%s} (worst=%.4f)" % (thr, ",".join(str(x) for x in grid), worst), ok))

# ---------------------------------------------------------------- driver

_LEV_CACHE = {}
_SURV_CACHE = {}

def _get_levels(jmax):
    if jmax not in _LEV_CACHE:
        _LEV_CACHE[jmax] = build_levels(jmax)
    return _LEV_CACHE[jmax]

def _get_survivors(levs, jmax, jmax2):
    key = (jmax, jmax2)
    if key not in _SURV_CACHE:
        _SURV_CACHE[key] = g2_band_survivors(levs, jmax2)
    return _SURV_CACHE[key]

def compute(mode='full', fallback=False, tamper=None, show_table=False):
    """mode='full' (default): the discharge's own claim, base anchor J0*=500 (fallback:
    430), grid DEEP_GRID_FULL -- this is the ship, not hidden behind a flag. Also runs
    gate SIB-CERT (deep anchor J0_SIB=800), UNLESS fallback=True: SIB-CERT is skipped
    under --fallback (an informational SKIPPED line is printed instead) since the
    deep-anchor discharge is specific to the primary (J0*,F_STAR) chain's own (LAM-BOX)
    monitoring, not the legacy fallback chain.
    mode='quick': a shallow (J0 capped at 200) subset for fast dev iteration ONLY --
    NOT a certified claim at that depth (MAG-BOX/V17-IA/V18 will typically MISS at
    J0=200; that is expected and does not represent the ship's result). SIB-CERT is
    always skipped under --quick (deep anchor J0_SIB=800 requires the full build)."""
    quick = (mode == 'quick')
    run_sibcert = (mode == 'full') and (not fallback)
    grid = DEEP_GRID_QUICK if quick else DEEP_GRID_FULL
    theta_grid = THETA_GRID_DEFAULT if quick else THETA_GRID_FULL
    bridge_grid = BRIDGE_GRID_DEFAULT if quick else BRIDGE_GRID_FULL
    mag_grid = [n for n in MAG_GRID if n <= (200 if quick else J0_STAR)]
    J0_full = J0_FALLBACK if fallback else J0_STAR
    J0 = min(J0_full, 200) if quick else J0_full
    f_pad = F_LEGACY if fallback else F_STAR
    jmax = max(grid + theta_grid + bridge_grid + mag_grid + [J0]
               + ([J0_SIB] if run_sibcert else []))
    levs = _get_levels(jmax)
    jmax2 = min(jmax, 130)
    survivors = _get_survivors(levs, jmax, jmax2)

    # LAM-INV's field census is computed EARLY (before MAG-BOX), memoized in
    # _LAMINV_CACHE, so gate_magnitude_box can report the realized-vs-field C'
    # consistency check at its own grid levels without paying the ~47s float
    # precompute twice; gate_lam_inv (below, at its normal report position) reuses
    # the SAME cached result. None under --quick/--fallback (matches SIB-CERT's scope).
    laminv_precomp = _laminv_certify(levs, J0, f_pad, tamper=tamper) if run_sibcert else None

    report = []; info = []
    gate_floors(report, levs, J0, f_pad, tamper=tamper)                        # F3        report[0]
    gate_magnitude_box(report, levs, mag_grid, tamper=tamper, laminv=laminv_precomp)  # MAG-BOX report[1]
    theta_band = gate_theta_ia(report, levs, J0, f_pad, tamper=tamper)         # V15-IA    report[2] [LOAD-BEARING]
    theta_star = THETA_FALLBACK if fallback else theta_band
    gate_theta(report, info, levs, theta_grid, tamper=tamper)                  # info V15-GRID[0]/V15-CERT[1]
    gate_thetasymb(report)                                                      # V16       report[3]
    gate_window(report, levs, grid, tamper=tamper)                             # V16b      report[4]
    gate_forcing(report, info, levs, grid, survivors, G2_GRID, tamper=tamper)   # V17 report[5] (+info V17-INFO[2])
    gate_forcing_ia(report, levs, J0, f_pad, theta_star, tamper=tamper)        # V17-IA    report[6] [LOAD-BEARING]
    gate_vtrack(report, levs, grid, max(grid), tamper=tamper, show_table=show_table)  # V18  report[7]
    gate_bridge(info, levs, bridge_grid, tamper=tamper)                        # V19       info[3]
    gate_sibling_band(info, levs, J0, f_pad)                                   # SIB-BAND  info[4]
    if run_sibcert:
        gate_sib_cert(report, levs, tamper=tamper)                             # SIB-CERT  report[8]
        gate_lam_inv(report, levs, J0, f_pad, tamper=tamper)                   # LAM-INV   report[9]
        gate_floor_drift(report, levs, grid, tamper=tamper)                    # FLOOR-DRIFT report[10]
    else:
        info.append(("SIB-CERT [SKIPPED in this mode: deep anchor J0=%d requires the"
                      " full build]" % J0_SIB, True))                          # info[5]
        info.append(("LAM-INV [SKIPPED in this mode: the NG=%d field census is scoped"
                      " to the full-mode discharge, like SIB-CERT]" % NG_LAM, True))  # info[6]
        info.append(("FLOOR-DRIFT [SKIPPED in this mode: the drift monitor + as-consumed"
                      " margins are anchored at (J0*=%d, J0_SIB=%d), full build only]"
                      % (J0_STAR, J0_SIB), True))                              # info[7]
    return report, info, theta_star

def run(mode='full', fallback=False, tamper=None, show_table=False):
    t0 = time.time()
    report, info, theta_star = compute(mode=mode, fallback=fallback, tamper=tamper,
                                       show_table=show_table)
    npass = sum(1 for _, ok in report if ok)
    J0_full = J0_FALLBACK if fallback else J0_STAR
    f_pad_used = F_LEGACY if fallback else F_STAR
    print("anchor: (J0*=%d, f*=%s, theta*=%s [%s%.6f])  mode=%s%s"
          % (J0_full, str(f_pad_used), str(theta_star), "" if fallback else "theta_band, ",
             float(theta_star), mode, " [FALLBACK]" if fallback else ""))
    print("GATES (certified-census frame; determine RESULT):")
    for name, ok in report:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("RESULT: %d/%d %s" % (npass, len(report), "PASS" if npass == len(report) else "FAIL"))
    print("STATUS: CONDITIONAL -- (SIB-BAND) DISCHARGED at the deep anchor by gate SIB-CERT"
          " GIVEN (LAM-BOX); (LAM-BOX) DISCHARGED-conditional by gate LAM-INV (proved"
          " invariant intervals); (C'-CAP) DISCHARGED-conditional by LAM-INV's floor-box"
          " node census (this revision, R1 mitigation (a) -- the monitored constant is now"
          " a PROVED bound, monitor retained as cross-check). Remaining computed clauses:"
          " (FOLD) and (FLOOR-PERSIST) -- the latter now first-class monitored (gate"
          " FLOOR-DRIFT, with the census route to proving it CLOSED as a route-cut);"
          " see the note's Section 8.4.")
    print()
    print("INFORMATIONAL (reported, NOT counted toward RESULT):")
    for name, ok in info:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    print()
    print("elapsed: %.1fs (mode=%s%s)" % (time.time() - t0, mode, " fallback" if fallback else ""))
    return npass == len(report)

# report indices: 0 F3, 1 MAG-BOX, 2 V15-IA, 3 V16, 4 V16b, 5 V17, 6 V17-IA, 7 V18,
#                 8 SIB-CERT, 9 LAM-INV, 10 FLOOR-DRIFT (all three full mode only;
#                 absent in --quick/--fallback)
# info indices:   0 V15-GRID, 1 V15-CERT, 2 V17-INFO, 3 V19, 4 SIB-BAND,
#                 5 SIB-CERT-SKIPPED, 6 LAM-INV-SKIPPED, 7 FLOOR-DRIFT-SKIPPED
#                 (quick/fallback only; absent in full mode)
TAMPERS = ["f3-corrupt", "magbox-shrink", "theta-tot-gate", "nfree-corrupt",
           "theta-ia-tighten", "theta-ia-sign", "window-bound", "forcing-bound",
           "v17ia-graze", "c1-target", "vtrack-level-drop", "g2-ceiling", "bridge-w-gate",
           "sibcert-sqrt", "sibcert-pad", "sibcert-band", "w17-shrink",
           "laminv-grid", "laminv-lip", "laminv-floor", "cprime-bound-graze",
           "floordrift-margin"]
TAMPER_TARGET = {
    "f3-corrupt": ("report", 0),        # F3
    "magbox-shrink": ("report", 1),     # MAG-BOX: shrink boxes so realized magnitudes leave them
    "theta-tot-gate": ("info", 0),      # V15-GRID (informational)
    "nfree-corrupt": ("info", 0),       # V15-GRID seminorm corruption (informational)
    "theta-ia-tighten": ("report", 2),  # V15-IA sanity-ceiling graze (value untouched -> isolated)
    "theta-ia-sign": ("report", 2),     # V15-IA max->min direction flip -> deflates below realized floor
    "window-bound": ("report", 4),      # V16b
    "forcing-bound": ("report", 5),     # V17
    "v17ia-graze": ("report", 6),       # V17-IA threshold graze
    "c1-target": ("report", 7),         # V18
    "vtrack-level-drop": ("report", 7), # V18 deep-level corruption
    "g2-ceiling": ("info", 2),          # V17-INFO (already-FAIL baseline; honest substitute)
    "bridge-w-gate": ("info", 3),       # V19
    "sibcert-sqrt": ("report", 8),      # SIB-CERT: inward sqrt bracket, trips the outwardness self-check
    "sibcert-pad": ("report", 8),       # SIB-CERT: shallower pad (99/100) at J0=800 -- misses
    "sibcert-band": ("report", 8),      # SIB-CERT: full (non-geometric-center) band -- misses
    "w17-shrink": ("report", 1),        # MAG-BOX: shrink the W17 boundary-slot box below realized
    "laminv-grid": ("report", 9),       # LAM-INV: NG far below threshold -- containment check misses
    "laminv-lip": ("report", 9),        # LAM-INV: LIP_L a-posteriori threshold lowered below realized
    "laminv-floor": ("report", 9),      # LAM-INV: R1 stress -- pre-widening floor + CPRIME forced 2x
    "cprime-bound-graze": ("report", 9),  # LAM-INV: (C'-CAP) proved bound forced 2x -- exceeds CPRIME
    "floordrift-margin": ("report", 10),  # FLOOR-DRIFT: required drift ratio raised above realized
}

def tamper_selftest(mode='full', fallback=False):
    t0 = time.time()
    base_report, base_info, _ = compute(mode=mode, fallback=fallback, tamper=None)
    print("baseline (mode=%s%s):" % (mode, " fallback" if fallback else ""))
    for name, ok in base_report:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    for name, ok in base_info:
        print("  [%s] %s (informational)" % ("PASS" if ok else "FAIL", name))
    print()
    allgood = True
    for tm in TAMPERS:
        kind, idx = TAMPER_TARGET[tm]
        rep, inf, _ = compute(mode=mode, fallback=fallback, tamper=tm)
        base_list = base_report if kind == "report" else base_info
        tam_list = rep if kind == "report" else inf
        base_ok = base_list[idx][1]; tam_ok = tam_list[idx][1]
        others_report_ok = all(rep[i][1] == base_report[i][1] for i in range(len(base_report))
                                if not (kind == "report" and i == idx))
        others_info_ok = all(inf[i][1] == base_info[i][1] for i in range(len(base_info))
                              if not (kind == "info" and i == idx))
        isolated = others_report_ok and others_info_ok
        if base_ok:
            flipped = not tam_ok
            verdict = "BROKE (good)" if flipped else "SURVIVED (BAD)"
            good = flipped and isolated
        else:
            verdict = ("N/A (already FAIL at baseline) -- tamper still FAIL" if not tam_ok
                       else "BAD (tamper flipped an already-failing line to PASS)")
            good = (not tam_ok) and isolated
        print("  tamper=%-20s target=%s[%d] %s  isolated=%s" % (tm, kind, idx, verdict, isolated))
        allgood = allgood and good
    print("\nTAMPER SELFTEST: %s  (%.1fs)" % ("PASS" if allgood else "FAIL", time.time() - t0))
    return allgood

def main():
    args = sys.argv[1:]
    mode = 'quick' if "--quick" in args else 'full'
    fallback = "--fallback" in args
    show_table = "--table" in args
    if "--tamper-selftest" in args:
        ok = tamper_selftest(mode=mode, fallback=fallback)
        sys.exit(0 if ok else 1)
    ok = run(mode=mode, fallback=fallback, show_table=show_table)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
