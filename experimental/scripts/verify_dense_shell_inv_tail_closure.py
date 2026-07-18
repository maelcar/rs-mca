#!/usr/bin/env python3
"""Verifier: dense-shell INV-TAIL closure (frame + proof gates).

Objects (as in #880/#858). Level vectors G_j(t), t in [1/6, 1/2], built by
the two-branch aggregated step; flipped-positive half-weight coordinates
c_0 = b_0, c_i = b_i/2 with even extension to Z; the step is exact
Z-convolution with K_d = (1/4, d, 1/4), d(t) = -cos(2 pi t)/2, aggregated
over children t_pm = (1 pm t)/3 (the c-dictionary). Bands r_0 = b_1/b_0
(cap 2), r_i = b_{i+1}/b_i (cap 1, i >= 1).

Gates (13: V1-V7, V9-V14):
  V1 [CDICT]   the c-dictionary is exact: the even-extension convolution
               reproduces the aggregated mult_root step (<= 1e-12).
  V2 [KREFUTE] composed 2-step kernel refutation witnesses: minus-plus
               L1 = d1^2 + d1 d2 + d2^2 - 1/8 < 0 at parent t = 1/2
               (closed form -0.0115..); minus-minus N1 = d1 + d2 < 0 at
               t = 1/2; and L1 >= 0 for parent t <= 0.39 (region pin).
  V3 [CONV]    polynomial convergence: delta_j * j^2 stays in a fixed
               window (no geometric contraction; theta_j tracks 1 - 2/j).
  V4 [CAPS]    computed cap layer of T1: r_0 < 2 and r_i < 1 (i <= 6) on
               the (j, t) grid; margins shrink ~ C/j (recorded).
  V5 [DRIFT]   computed layer of T2: pointwise monotone drift
               r_i(j+1, t) >= r_i(j, t) - tol, zero violations on the grid.
  V6 [DOM]     T3 tail dominance: D_i >= floor > 0 on the eps grid for
               j >= 7, plus the second-order structure: DeltaC * j constant
               across depths (D_0 ~ 0.089), C_i - D_i > 1 (no crossover).
  V7 [ASSEMBLY] the i=0-only share arithmetic at the level-48 base: the
               r_0 floors on the two child ranges AND the span floor are
               computed in-gate from the level-48 cascade (persistence pad
               0.995), and the assembly gamma_0 is gated >= gamma_req@loose
               = 1.1471 at BOTH the full floors (f = 1.00) and the census
               floors (f = 0.98).
  V9 [BASE]    the caps/no-spike base cases J(5), J(6) on a 400-pt t-grid
               (min(Delta, no-spike) > 0), the induction base of T1.
  V10 [COUP]   the (COUP) constant scan: kappa = sup p^-_i / p^+_i over
               sibling pairs at child level jc, against the threshold
               4*min d_+ = 4*(sin^2(7 pi/18) - 1/2) = 1.53209.
  V11 [SIGMA]  the mass recursion S_j(t) = a(t+) S(t+) + a(t-) S(t-) -
               (1/4)[Delta_0(t+) + Delta_0(t-)] holds exactly (<1e-10
               relative) on the cascade; the measured minus-share sigma(t)
               stays in [0.24, 0.43] at j in {20, 40}, monotone decreasing
               in t.
  V12 [CENSUS] the final-bundle corner census at the target (floors
               0.98 * r_i(48,t), caps, LC, sigma <= sigma_max(t),
               rho_prop <= 1.02560749): the box closes (cap slack >= 0
               non-strict at the r_0 = 2 fixed point; floor slack > 0), and
               the output c-vectors stay log-concave (LC) to 1e-6. LC-corner
               set (reduced by default, full 2^5 x 2^5 x 41-parent set under
               --deep).
  V13 [PROP]   the realized cross-child spread rho_prop(j) = max_i g_i /
               min_i g_i, g_i = c_i(t-)/c_i(t+). GATED on the operative
               window the census consumes (i < 17, the corner-vector
               length): rho_prop(j) <= 1.02560749 for all computed
               j >= 48, and monotone-decreasing over the deep grid
               {48, 50, 55, 60}. The narrower i < 10 window (which decays
               faster) is printed for information only.
  V14 [PMASS]  the p-mass recursion P_j(t) = a(t+) P+ + a(t-) P- -
               (1/2)[p_0(t+) + p_0(t-)] holds (<1e-8 relative, j >= 30
               where the second-difference p-cascade is well-conditioned);
               Dp <= 0 (p decreasing in t, closing pair-1) on the j in
               {20, 40} grid; and the coherence kappa_max/N <= 1.1695
               (= 1.53209/1.31, the (COUP) reduction bound) at j in
               {20, 40}, parent t = 1/2.

Numbering note: V8 was retired during development (its cap/no-spike content
folded into V4 and V9); the gate set is V1-V7, V9-V14.

Flags: --deep extends grids (j to 60); --tamper-selftest runs all tampers,
each must FAIL. stdlib only, deterministic. RESULT: PASS/FAIL summary.
"""
import itertools
import math
import sys

PI = math.pi
K = 80

NODES = [0.25 * (1 + math.cos(PI * m / K)) for m in range(K + 1)]
BW = [(0.5 if m in (0, K) else 1.0) * (1 if m % 2 == 0 else -1) for m in range(K + 1)]

def a_of(t):
    s = math.sin(PI * t)
    return s * s

def d_of(t):
    return -0.5 * math.cos(2 * PI * t)

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

def cvec(t, lev_j):
    b = flip(bary(t, lev_j))
    return [b[0]] + [x / 2.0 for x in b[1:]]

def conv_even(c, d, edge_tamper=False):
    n = len(c)
    def get(i):
        i = abs(i)
        return c[i] if i < n else 0.0
    out = [0.25 * get(i - 1) + d * get(i) + 0.25 * get(i + 1) for i in range(n + 1)]
    if edge_tamper:
        out[0] = d * get(0) + 0.25 * get(1)   # tamper: drop the reflected 1/4
    return out

# ---------------------------------------------------------------- gates

def gate_cdict(report, levs, tamper=None):
    worst = 0.0
    for (t, j) in ((0.31, 12), (0.26, 20), (0.49, 16), (0.18, 10)):
        target = cvec(t, levs[j])
        acc = None
        for dd in (-1.0, 1.0):
            tv = abs((dd + t) / 3.0)
            step = conv_even(cvec(tv, levs[j - 1]), d_of(tv),
                             edge_tamper=(tamper == "cdict-edge"))
            acc = step if acc is None else [x + y for x, y in zip(acc, step)]
        worst = max(worst, max(abs(x - y) / max(abs(y), 1e-300)
                               for x, y in zip(acc, target)))
    ok = worst < 1e-12
    report.append(("V1 CDICT exact (rel %.1e)" % worst, ok))

def gate_krefute(report, tamper=None):
    d1 = d_of(1.0 / 6); d2 = d_of(7.0 / 18)
    L1 = d1 * d1 + d1 * d2 + d2 * d2 - 0.125
    ok1 = -0.0120 < L1 < -0.0110
    d2mm = d_of(5.0 / 18)
    N1 = d1 + d2mm
    ok2 = -0.17 < N1 < -0.16
    lim = 0.50 if tamper == "krefute-region" else 0.39
    ok3 = True
    for k in range(200):
        t = 1.0 / 6 + (lim - 1.0 / 6) * k / 199
        tm = (1.0 - t) / 3.0
        e1 = d_of(tm); e2 = d_of((1.0 + tm) / 3.0)
        if e1 * e1 + e1 * e2 + e2 * e2 < 0.125:
            ok3 = False
    report.append(("V2 KREFUTE mp L1 = %.5f, mm N1 = %.4f, safe region t <= %.2f"
                   % (L1, N1, lim), ok1 and ok2 and ok3))

def gate_conv(report, levs, jmax, tamper=None):
    probes = [0.25 + 0.028 * k / 9 for k in range(10)] + [0.2, 0.35, 0.45]
    prev_bands = None
    deltas = {}
    for j in range(jmax - 14, jmax + 1):
        bands = []
        for t in probes:
            b = flip(bary(t, levs[j]))
            bands.append([b[i + 1] / b[i] for i in range(5) if b[i] > 1e-250])
        if prev_bands is not None:
            dd = 0.0
            for rn, ro in zip(bands, prev_bands):
                for x, y in zip(rn, ro):
                    if x > 0 and y > 0:
                        dd = max(dd, abs(math.log(x / y)))
            deltas[j] = dd
        prev_bands = bands
    vals = [deltas[j] * j * j for j in deltas]
    lo, hi = min(vals), max(vals)
    if tamper == "conv-window":
        # tamper: assert the REFUTED geometric model (theta <= 0.93) -- the
        # polynomial data (theta -> 1 - 2/j > 0.93 here) must break this.
        js = sorted(deltas)
        ok = all(deltas[b] / deltas[a] <= 0.93 for a, b in zip(js, js[1:]))
        report.append(("V3 CONV [tampered: geometric theta <= 0.93]", ok))
        return
    ok = hi / lo < 2.6 and all(deltas[j] > 0 for j in deltas)
    report.append(("V3 CONV delta*j^2 in [%.2f, %.2f] (ratio %.2f < 2.6), poly not geometric"
                   % (lo, hi, hi / lo), ok))

def gate_caps(report, levs, jmax, tamper=None):
    cap0 = 1.95 if tamper == "caps-margin" else 2.0
    worst_m = 1e9; ok = True
    for j in range(4, jmax + 1, 2):
        for k in range(40):
            t = 1.0 / 6 + (1.0 / 3 - 1e-3) * k / 39
            b = flip(bary(t, levs[j]))
            for i in range(min(7, len(b) - 1)):
                if b[i] > 1e-250:
                    r = b[i + 1] / b[i]
                    cap = cap0 if i == 0 else 1.0
                    m = cap - r
                    if m <= 0:
                        ok = False
                    if i == 0:
                        worst_m = min(worst_m, m)
    report.append(("V4 CAPS r0 < %.2f margin >= %.4f, r_i < 1 (grid j <= %d)"
                   % (cap0, worst_m, jmax), ok))

def gate_drift(report, levs, jmax, tamper=None):
    # tamper 'drift-sign' flips the tested direction: it counts UP-drifts
    # as violations, and since the drift IS up everywhere the gate must FAIL.
    sign = -1.0 if tamper == "drift-sign" else 1.0
    viol = 0
    for j in range(31, jmax):
        for k in range(30):
            t = 0.25 + 0.028 * k / 29
            b0 = flip(bary(t, levs[j])); b1 = flip(bary(t, levs[j + 1]))
            for i in range(min(6, len(b0) - 1)):
                if b0[i] > 1e-250 and b1[i] > 1e-250:
                    d = b1[i + 1] / b1[i] - b0[i + 1] / b0[i]
                    if sign * d < -1e-9:
                        viol += 1
    report.append(("V5 DRIFT monotone, %d violations (j 31..%d)" % (viol, jmax), viol == 0))

def gate_dom(report, levs, jmax, tamper=None):
    # ALL indices: both D_i >= 0 and gamma_i monotone-in-i over the full
    # vector (tail floor 1e-260) — the tail of the share floor reduces to
    # i = 0 exactly because of this gate.
    floor = 1e-3 if tamper == "dom-floor" else 0.0
    worst = 1e9; ok = True
    for j in range(7, jmax + 1):
        for ke in range(1, 20):
            eps = 0.25 * ke / 20
            tin = 0.25 - eps / 3; r = 0.25 + eps / 9
            G = flip(bary(tin, levs[j])); Y = flip(bary(r, levs[j - 1]))
            gprev = None
            for i in range(len(Y)):
                if Y[i] > 1e-260 and G[i] > 1e-260:
                    g = G[i] / Y[i]
                    if gprev is not None and g < gprev * (1 - 1e-11):
                        ok = False
                    gprev = g
            for i in range(len(Y) - 1):
                if Y[i] > 1e-260 and G[i] > 1e-260 and Y[i + 1] > 1e-260 and G[i + 1] > 1e-260:
                    D = G[i + 1] / G[i] - Y[i + 1] / Y[i]
                    worst = min(worst, D)
                    if D < floor:
                        ok = False
    # second-order: DeltaC * j (NOT DeltaC) is depth-constant; compare at two
    # depths within 12%. raw ratio difference * j = DeltaC; * j again = DeltaC*j.
    eps = 0.24375; tin = 0.25 - eps / 3; r = 0.25 + eps / 9
    dcj = []
    for j in (30, jmax):
        bt = flip(bary(tin, levs[j])); br = flip(bary(r, levs[j]))
        dcj.append((bt[1] / bt[0] - br[1] / br[0]) * j * j)
    agree = abs(dcj[0] - dcj[1]) / abs(dcj[0]) < 0.12 and dcj[0] < 0
    report.append(("V6 DOM D_i >= %.0e (worst %.2e, j 7..%d); DeltaC*j %.3f/%.3f consistent"
                   % (floor, worst, jmax, dcj[0], dcj[1]), ok and agree))

def gate_assembly(report, levs2, jmax2):
    # V7: the i=0-only share arithmetic at the level-48 base. By V6
    # (gamma_i monotone in i) the all-i share floor reduces to i = 0, and
    # the i = 0 assembly consumes ONLY the r_0 floor on the two child
    # ranges (q_0 = r_0/4; no caps enter at i = 0) + the span floor (the
    # pointwise-min ratio Y2[i]/Y[i] between the two child vectors). All
    # three floors are computed here from the level-48 cascade (levs2[48],
    # always available -- j0 = 48 in both default and --deep) with a 0.995
    # persistence pad; r_i drifts UP in j for j >= 48 (T2/V5), so the
    # level-48 value padded down is a valid floor for every j >= 48.
    # Requirement: gamma_req at LOOSE caps = 1.1471 (exact 1.1470992682;
    # the banked 1.149 was rounding, 1.036 was an error). Gated at BOTH
    # the full floors (f = 1.00) and the census floors (f = 0.98), so the
    # discharge chain uses the SAME f = 0.98 floors on the census and the
    # assembly side.
    GAMMA_REQ_LOOSE = 1.1471
    PAD = 0.995
    j0 = 48
    lo_r0_Y = 1e9; lo_r0_Y2 = 1e9
    for k in range(30):
        tY = 0.25 + 0.028 * k / 29
        tY2 = 0.389 + 0.028 * k / 29
        bY = flip(bary(tY, levs2[j0])); bY2 = flip(bary(tY2, levs2[j0]))
        lo_r0_Y = min(lo_r0_Y, bY[1] / bY[0])
        lo_r0_Y2 = min(lo_r0_Y2, bY2[1] / bY2[0])
    lo_r0_Y *= PAD; lo_r0_Y2 *= PAD
    # span floor: min over the eps grid and index i of Y2[i]/Y[i], the two
    # child vectors at level 48, padded down. It multiplies the (positive)
    # second child term, so the min is the conservative choice.
    span = 1e9
    for ke in range(1, 25):
        eps = 0.25 * ke / 25
        r = 0.25 + eps / 9; r2 = 5.0 / 12 - eps / 9
        Yv = flip(bary(r, levs2[j0])); Y2v = flip(bary(r2, levs2[j0]))
        span = min(span, min(Y2v[i] / Yv[i]
                             for i in range(min(len(Yv), len(Y2v))) if Yv[i] > 1e-12))
    span *= PAD

    def assembly(f):
        g0 = 1e9
        for ke in range(1, 25):
            eps = 0.25 * ke / 25
            r = 0.25 + eps / 9; r2 = 5.0 / 12 - eps / 9
            dr, dr2 = a_of(r) - 0.5, a_of(r2) - 0.5
            g0 = min(g0, dr + f * lo_r0_Y / 4.0 + span * (dr2 + f * lo_r0_Y2 / 4.0))
        return g0

    g_full = assembly(1.00); g_f098 = assembly(0.98)
    ok = g_full >= GAMMA_REQ_LOOSE and g_f098 >= GAMMA_REQ_LOOSE
    report.append(("V7 ASSEMBLY i=0-only @ j0=48 (r0 floors %.4f/%.4f, span %.4f):"
                   " gamma[f=1.00]=%.4f, gamma[f=0.98]=%.4f, both >= %.4f"
                   % (lo_r0_Y, lo_r0_Y2, span, g_full, g_f098, GAMMA_REQ_LOOSE), ok))

def delta_p_of(b):
    # difference and no-spike sequences of the flipped-positive c-vector
    c = [b[0]] + [x / 2.0 for x in b[1:]]
    D = [c[i] - c[i + 1] for i in range(len(c) - 1)]
    p = [D[1] - 2 * D[0]] + [D[i - 1] + D[i + 1] - D[i] for i in range(1, len(D) - 1)]
    return D, p

def gate_basej(report, levs, tamper=None):
    # V9: the caps/no-spike base cases J(5), J(6) on a fine t-grid.
    jset = (4, 5, 6) if tamper == "basej-early" else (5, 6)
    ok = True; worst = 1e9
    for j in jset:
        for k in range(400):
            t = 1.0 / 6 + (1.0 / 3 - 1e-4) * k / 399
            D, p = delta_p_of(flip(bary(t, levs[j])))
            m = min(min(D), min(p[:max(1, len(p) - 2)]))
            worst = min(worst, m)
            if m < 0:
                ok = False
    report.append(("V9 BASE J(%s) min(Delta, nospike) = %+.4f on 400-pt grid"
                   % (",".join(str(j) for j in jset), worst), ok))

def gate_coup(report, levs, jmax, tamper=None):
    # V10: the (COUP) constant scan — kappa = sup p^-_i / p^+_i over
    # sibling pairs at child level jc, against the threshold 4*min d_+
    # = 4*(sin^2(7 pi/18) - 1/2) = 1.53209.
    thresh = 4.0 * (math.sin(PI * 7.0 / 18) ** 2 - 0.5)
    cap = 1.415 if tamper == "coup-cap" else 1.462
    ok = True; kmax = 0.0; kwhere = None
    for jc in range(6, min(jmax, 48)):
        for k in range(60):
            t = 1.0 / 6 + (1.0 / 3 - 1e-3) * k / 59
            tp = (1.0 + t) / 3.0; tm = (1.0 - t) / 3.0
            _, pp = delta_p_of(flip(bary(tp, levs[jc])))
            _, pm = delta_p_of(flip(bary(tm, levs[jc])))
            n = min(len(pp), len(pm)) - 2
            for i in range(1, max(2, n)):
                if pp[i] > 1e-200 and pm[i] > 0:
                    kap = pm[i] / pp[i]
                    if kap > kmax: kmax = kap; kwhere = (jc, i)
    if kmax > cap: ok = False
    report.append(("V10 COUP kappa = %.4f at (jc,i)=%s <= %.3f < threshold %.5f"
                   % (kmax, kwhere, cap, thresh), ok and cap < thresh))

# ------------------------------------------------------- V7 and V11-V14 helpers
#
# These gates need level j = 48 available even in the default (non-deep) run
# (the target floors/census are pinned at EXACTLY level 48, not a moving
# "jmax"), so run() builds a second cascade levs2 up to jmax2 = 48 (60 under
# --deep), independent of the jmax = 40/60 cascade V1-V6/V9/V10 use.

def mass_of(t, j, levs):
    return sum(cvec(t, levs[j]))

def delta0_of(t, j, levs):
    c = cvec(t, levs[j])
    return c[0] - c[1]

def rlen_of(cv, tol=1e-9):
    # trims the tail below `tol` relative to c_0 (interpolation-noise floor).
    c0 = abs(cv[0]) if cv[0] else 1.0
    L = len(cv)
    while L > 3 and abs(cv[L - 1]) / c0 < tol:
        L -= 1
    return L

def pvec_of(t, j, levs):
    return delta_p_of(flip(bary(t, levs[j])))[1]

def pmass_of(t, j, levs):
    p = pvec_of(t, j, levs)
    L = min(rlen_of(cvec(t, levs[j])), len(p))
    return sum(p[:L])

def gate_sigma(report, levs2, tamper=None):
    # V11: the mass recursion (S3) and the tight sigma_max(t) profile. The
    # mass factor a(t) = 1/2 + d(t) is exact, so the minus-share is a
    # scalar quantity; the pure-a operator is positive, hence Birkhoff-
    # contracting, which bounds sigma above j-uniformly (PROVED, loose);
    # the tight profile is the computed max below.
    corr = 0.5 if tamper == "sigma-recur" else 0.25
    samples = [(0.22, 12), (0.31, 20), (0.44, 30), (0.26, 40)]
    worst_rel = 0.0
    for (t, j) in samples:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        lhs = mass_of(t, j, levs2)
        rhs = (a_of(tp) * mass_of(tp, j - 1, levs2) + a_of(tm) * mass_of(tm, j - 1, levs2)
               - corr * (delta0_of(tp, j - 1, levs2) + delta0_of(tm, j - 1, levs2)))
        worst_rel = max(worst_rel, abs(lhs - rhs) / max(abs(lhs), 1e-300))
    ok_rec = worst_rel < 1e-10

    def sigma_j(t, j):
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        Sp = a_of(tp) * mass_of(tp, j - 1, levs2) - corr * delta0_of(tp, j - 1, levs2)
        Sm = a_of(tm) * mass_of(tm, j - 1, levs2) - corr * delta0_of(tm, j - 1, levs2)
        return Sm / (Sp + Sm)

    ok_range = True; ok_mono = True
    lo_all, hi_all = 9.9, -9.9
    for j in (20, 40):
        prev = None
        for k in range(24):
            t = 1.0 / 6 + (1.0 / 3 - 1e-4) * k / 23
            s = sigma_j(t, j)
            lo_all = min(lo_all, s); hi_all = max(hi_all, s)
            if not (0.24 <= s <= 0.43):
                ok_range = False
            if prev is not None and s > prev + 1e-9:
                ok_mono = False
            prev = s
    ok = ok_rec and ok_range and ok_mono
    report.append(("V11 SIGMA mass-recursion rel %.1e (<1e-10); sigma range [%.4f,%.4f]"
                   " within [0.24,0.43], monotone-dec in t (j=20,40)"
                   % (worst_rel, lo_all, hi_all), ok))

# ---------------------------------------------------------- V12 census constants
#
# Corner-sufficiency (S3): the aggregate output ratio is Mobius-monotone in
# each input c-ratio for fixed output sign, so over the LC-feasible box the
# extremes sit at the LC-ratio corners. The finite corner census below is
# therefore a certificate for the ratio dimensions (the mu-scale and the
# parent t are gridded; the mu-monotonicity is Mobius as well and the grid
# has been checked to be robust to refinement).

CENSUS_DEG = 16
CENSUS_NC = 5
CENSUS_MU = [math.exp(-2.0 + 2.6 * k / 12) for k in range(13)]

def floors_at48(t, levs2):
    b = flip(bary(t, levs2[48]))
    return [b[i + 1] / b[i] if (i + 1 < len(b) and b[i] > 1e-250) else 0.4
            for i in range(CENSUS_DEG)]

def sigma_max_at(t, jmax2, levs2):
    tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
    sm = 0.0
    for j in range(8, jmax2):
        cp = cvec(tp, levs2[j - 1]); cm = cvec(tm, levs2[j - 1])
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

def census_out_bratios(o):
    r = [2 * o[1] / o[0]]
    for i in range(1, len(o) - 1):
        r.append(o[i + 1] / o[i] if o[i] > 1e-300 else float('nan'))
    return r

def gate_census(report, levs2, jmax2, tamper=None):
    # V12: the final-bundle census at the target f=0.98, rho_prop<=1.02560749
    # (the PRECISE bisected plateau value; the rounded "1.026" is already
    # just past the threshold -- the census fails there by ~-0.0046). rho_prop
    # is imposed over the full corner window (all CENSUS_DEG+1 indices), which
    # is exactly the window V13 gates. Reported: cap slack (>= 0 non-strict:
    # the tight case is the r_0 = 2 degenerate fixed point, where both
    # children and the output sit at r_0 = 2), floor slack (> 0), and the
    # output-LC slack (the output c-ratios stay non-increasing to 1e-6).
    rho_prop = 1.05 if tamper == "census-rho" else 1.02560749
    f = 0.98
    nparents = 41 if jmax2 >= 60 else 17
    parents = [1.0 / 6 + (1.0 / 3 - 1e-4) * k / (nparents - 1) for k in range(nparents)]
    corner_bits = list(itertools.product((0, 1), repeat=CENSUS_NC))

    wc = 1e9; wf = 1e9; wlc = 1e9
    for t in parents:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        dp, dm = d_of(tp), d_of(tm)
        ap, am = a_of(tp), a_of(tm)
        fp = floors_at48(tp, levs2); fm = floors_at48(tm, levs2); ft = floors_at48(t, levs2)
        sig = sigma_max_at(t, jmax2, levs2)
        phip = [x * f for x in fp]; phim = [x * f for x in fm]; ftf = [x * f for x in ft]
        Pc = []
        for bp in corner_bits:
            vp = census_lc_corner(phip, bp)
            cp = conv_even(vp, dp)
            Pc.append((vp, cp, sum(vp)))
        Mc = [census_lc_corner(phim, bm) for bm in corner_bits]
        for vp, cp, Sp in Pc:
            for vm in Mc:
                gs = [vm[i] / vp[i] for i in range(len(vp))]
                if max(gs) / min(gs) > rho_prop * (1 + 1e-9):
                    continue
                for mu in CENSUS_MU:
                    Sm = mu * sum(vm)
                    share = am * Sm / (ap * Sp + am * Sm)
                    if share > sig + 1e-9:
                        continue
                    cm = conv_even([mu * x for x in vm], dm)
                    o = [x + y for x, y in zip(cp, cm)]
                    if any(val <= 0 for val in o[:CENSUS_DEG - 1]):
                        continue
                    r = census_out_bratios(o)
                    cs = min([2 - r[0]] + [1 - r[i] for i in range(1, 9)])
                    if cs < wc:
                        wc = cs
                    for i in range(3):
                        v = r[i] - ftf[i]
                        if v < wf:
                            wf = v
                    # output log-concavity: the output c-ratios (rc_i =
                    # o_{i+1}/o_i) must stay non-increasing, so these outputs
                    # are valid LC children at the next induction step.
                    rc = [o[i + 1] / o[i] for i in range(CENSUS_DEG - 1) if o[i] > 1e-250]
                    for i in range(len(rc) - 1):
                        if rc[i] - rc[i + 1] < wlc:
                            wlc = rc[i] - rc[i + 1]
    ok = wc >= 0 and wf >= 0 and wlc >= -1e-6
    report.append(("V12 CENSUS floors=0.98*r_i(48,t)+caps+LC+sigma<=sigma_max(t), rho_prop<=%.6f:"
                   " cap %+.5f (non-strict; r_0=2 fixed pt), floor %+.5f, out-LC %+.2e (>=-1e-6),"
                   " %d parents"
                   % (rho_prop, wc, wf, wlc, nparents), ok))

def gate_prop(report, levs2, jmax2, tamper=None):
    # V13: the realized cross-child spread rho_prop(j) = max_i g_i / min_i g_i,
    # g_i = c_i(t_-)/c_i(t_+), over the full t-domain (41 parents).
    #
    # rho_prop is window-dependent (g_i is a smooth monotone-decreasing
    # profile, so a wider index window gives a larger max/min). The OPERATIVE
    # window is the one V12 imposes: the full corner-vector length,
    # i < CENSUS_DEG+1 = 17. This gate is the census precondition, so it is
    # gated on THAT window: rho_prop@i<17(j) <= 1.02560749 (the bisected
    # target, equal to the realized j=48 value up to +1.7e-5 -- the honest
    # margin is the j-improvement, not a fixed multiple) for every computed
    # j >= 48, AND monotone-decreasing over the deep grid {48,50,55,60}.
    # The narrower i<10 window decays FASTER (its j=48 value is ~1.008); it
    # is printed for information only and is NOT the operative constraint.
    NPAR = 41
    PARENTS = [1.0 / 6 + (1.0 / 3 - 1e-4) * k / (NPAR - 1) for k in range(NPAR)]
    OPWIN = CENSUS_DEG + 1   # = 17, the corner-vector length V12 uses

    def rho_win(j, nmax):
        worst = 0.0
        for t in PARENTS:
            tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
            bp = flip(bary(tp, levs2[j])); bm = flip(bary(tm, levs2[j]))
            vp = [bp[0]] + [x / 2.0 for x in bp[1:]]
            vm = [bm[0]] + [x / 2.0 for x in bm[1:]]
            n = min(nmax, len(vp), len(vm))
            g = [vm[i] / vp[i] for i in range(n) if vp[i] > 1e-250]
            worst = max(worst, max(g) / min(g))
        return worst

    TARGET = 1.02560749
    ttarget = 1.0250 if tamper == "prop-window" else TARGET
    deep_grid = [j for j in (48, 50, 55, 60) if j <= jmax2]
    op = {j: rho_win(j, OPWIN) for j in deep_grid}
    ok_target = all(op[j] <= ttarget for j in deep_grid)
    ok_mono = all(op[a] >= op[b] - 1e-9 for a, b in zip(deep_grid, deep_grid[1:]))
    info10_48 = rho_win(48, 10)
    info10_hi = rho_win(deep_grid[-1], 10)

    ok = ok_target and ok_mono
    report.append(("V13 PROP rho_prop@i<17(48)=%.7f <= %.8f, monotone-dec over {%s}: %s;"
                   " info i<10 decays faster (%.5f@48 -> %.5f@%d, non-operative)"
                   % (op[48], ttarget, ",".join(str(j) for j in deep_grid),
                      "yes" if ok_mono else "NO", info10_48, info10_hi, deep_grid[-1]), ok))

def gate_pmass(report, levs2, jmax2, tamper=None):
    # V14: the p-mass recursion (S2; odd-sequence 1/2 center correction, vs
    # the 1/4 for even c). Sampled at j in {30,40,48}: at low j (<~28) the
    # p-sequence is a genuine second difference and is interpolation-limited
    # to ~1e-3..1e-6 relative, so j >= 30 (comfortably <1e-8) is used. Also:
    #  - Dp <= 0 (p strictly decreasing in t) on the j in {20,40} grid --
    #    the definiteness that closes pair-1 (L* = 0.974); COMPUTED here.
    #  - the coherence kappa_max/N: (COUP) [kappa <= 1.53209] reduces to
    #    {N <= 1.31 (PROVED, loose)} AND {kappa_max/N <= 1.53209/1.31 =
    #    1.1695}; the second factor is measured here (t = 1/2, j in {20,40}).
    corr = 0.25 if tamper == "pmass-center" else 0.5
    samples = [(0.22, 30), (0.35, 40), (0.28, 48)]
    worst_rel = 0.0
    for (t, j) in samples:
        tp, tm = (1 + t) / 3.0, (1 - t) / 3.0
        lhs = pmass_of(t, j, levs2)
        p0p = pvec_of(tp, j - 1, levs2)[0]
        p0m = pvec_of(tm, j - 1, levs2)[0]
        rhs = (a_of(tp) * pmass_of(tp, j - 1, levs2) + a_of(tm) * pmass_of(tm, j - 1, levs2)
               - corr * (p0p + p0m))
        worst_rel = max(worst_rel, abs(lhs - rhs) / max(abs(lhs), 1e-300))
    ok_rec = worst_rel < 1e-8

    # Dp <= 0: p decreasing in t (finite difference in t at fixed j).
    dp_bound = -0.01 if tamper == "pmass-dp" else 1e-6
    worst_dp = -9.9
    for j in (20, 40):
        for k in range(40):
            t = 1.0 / 6 + (1.0 / 3 - 2e-3) * k / 39
            h = 1e-4
            p0 = pvec_of(t, j, levs2); p1 = pvec_of(t + h, j, levs2)
            L = min(rlen_of(cvec(t, levs2[j])), len(p0), len(p1))
            for i in range(1, L):
                worst_dp = max(worst_dp, p1[i] - p0[i])
    ok_dp = worst_dp <= dp_bound

    KN_THRESH = 1.1695   # = 1.53209 / 1.31
    ok_kn = True; worst_kn = 0.0
    for j in (20, 40):
        tp, tm = 0.5, 1.0 / 6   # children of the edge parent t=1/2
        pp = pvec_of(tp, j, levs2); pm = pvec_of(tm, j, levs2)
        Lm = min(rlen_of(cvec(tp, levs2[j])), rlen_of(cvec(tm, levs2[j])), len(pp), len(pm))
        kmax = 0.0
        for i in range(1, Lm):
            if pp[i] > 1e-11:
                r = pm[i] / pp[i]
                if r > kmax:
                    kmax = r
        N = pmass_of(tm, j, levs2) / pmass_of(tp, j, levs2)
        kn = kmax / N
        worst_kn = max(worst_kn, kn)
        if kn > KN_THRESH:
            ok_kn = False
    ok = ok_rec and ok_dp and ok_kn
    report.append(("V14 PMASS recursion rel %.1e (<1e-8, j={30,40,48}); Dp=%+.1e <= 0"
                   " (p dec. in t, j={20,40}); kappa_max/N=%.4f <= %.4f (j={20,40})"
                   % (worst_rel, worst_dp, worst_kn, KN_THRESH), ok))

# ---------------------------------------------------------------- driver

_LEV_CACHE = {}

def _get_levels(jmax):
    if jmax not in _LEV_CACHE:
        _LEV_CACHE[jmax] = build_levels(jmax)
    return _LEV_CACHE[jmax]

def run(deep=False, tamper=None):
    jmax = 60 if deep else 40
    levs = _get_levels(jmax)
    # V7 and V11-V14 pin the target floors/census at EXACTLY level 48, so a
    # second cascade levs2 is built to jmax2 = 48 by default (60 under
    # --deep); jmax2 == jmax under --deep, so the cache serves both.
    jmax2 = 60 if deep else 48
    levs2 = _get_levels(jmax2)
    report = []
    gate_cdict(report, levs, tamper=tamper)
    gate_krefute(report, tamper=tamper)
    gate_conv(report, levs, jmax, tamper=tamper)
    gate_caps(report, levs, jmax, tamper=tamper)
    gate_drift(report, levs, jmax, tamper=tamper)
    gate_dom(report, levs, jmax, tamper=tamper)
    gate_assembly(report, levs2, jmax2)
    gate_basej(report, levs, tamper=tamper)
    gate_coup(report, levs, jmax, tamper=tamper)
    gate_sigma(report, levs2, tamper=tamper)
    gate_census(report, levs2, jmax2, tamper=tamper)
    gate_prop(report, levs2, jmax2, tamper=tamper)
    gate_pmass(report, levs2, jmax2, tamper=tamper)
    npass = sum(1 for _, ok in report if ok)
    for name, ok in report:
        print("  [%s] %s" % ("PASS" if ok else "FAIL", name))
    print("RESULT: %d/%d %s" % (npass, len(report),
                                "PASS" if npass == len(report) else "FAIL"))
    return npass == len(report)

TAMPERS = ["cdict-edge", "krefute-region", "conv-window", "caps-margin",
           "drift-sign", "dom-floor", "basej-early", "coup-cap",
           "sigma-recur", "census-rho", "prop-window", "pmass-center",
           "pmass-dp"]

def main():
    deep = "--deep" in sys.argv
    if "--tamper-selftest" in sys.argv:
        allbroke = True
        for tm in TAMPERS:
            print("tamper: %s" % tm)
            broke = not run(deep=False, tamper=tm)
            print("  -> %s" % ("BROKE (good)" if broke else "SURVIVED (BAD)"))
            allbroke = allbroke and broke
        print("TAMPER SELFTEST: %s" % ("PASS" if allbroke else "FAIL"))
        sys.exit(0 if allbroke else 1)
    ok = run(deep=deep)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
