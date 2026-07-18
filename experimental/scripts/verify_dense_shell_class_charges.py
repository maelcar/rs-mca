#!/usr/bin/env python3
"""Verifier: dense-shell class-charge arithmetic (computational core).

Objects. Level-B chart, c = 3^B. Dense shell = the 2^B residues xi whose
balanced digits are all nonzero. Weight hatf(xi) = [z^B] prod_{i<B}
(1 + 2cos(2 pi xi 3^i / c) z + z^2) (#842/#827; sign law #858:
sign(hatf) = (-1)^B on the shell). Inverse side h(sigma) = (1/c)
sum_{xi dense} hatf(xi) e(-xi sigma / c). Support classes: for
U subseteq {0..B-1}, class(U) = {sigma : balanced digits supported
EXACTLY on U}; |class(U)| = 2^{|U|}.

Claims verified here (computational layer of the packet):
  G1 [DEF]     the i-indexed product equals the scan-state product
               (reordering identity; scan u_k = (d_{k-1}+u_{k-1})/3).
  G2 [KERNEL]  class-sum(U) = (1/c) sum_xi hatf(xi) prod_{i in U}
               2cos(2 pi xi 3^i / c): sigma-side brute == kernel form
               == scan-coordinate insertion table with K = {B-i : i in U}.
  G3 [LAW]     sign(class-sum(U)) = (-1)^{B-|U|} for EVERY U, B <= 10
               (exhaustive; margins recorded).
  G4 [LEAK]    B = 10 pointwise leak table: wrong-sign |h|-mass share by
               |U|: 0 for |U| <= 3; pinned values for 4..10 (the leak
               correction of the charge arithmetic omega_U = W_U +
               1_{s_U=+1}|Sigma_U|, equivalently (M_U+Sigma_U)/2).
  G5 [DP]      u-state-collapsed transfer DP (function-valued in u via
               Chebyshev nodes, z-polynomial payload) reproduces the
               subset charge table; certified additive tail bar in the
               #858-D6 constants, insertion levels carrying one extra
               2cosh factor; observed <= certified at the instances.

Proof-layer gates P1-P15 (P2/P3 reserved, unused): the ATOM and coupling
identity, A-purity, the exact-derivative envelope machinery (DG identity,
L4 one-step bound, L5 cancellation), the sharp secant caps on the two
MASTER-consumed COUPLED child curves (P7) plus an informational
whole-support census (P14), the KEY scalar as a conditional check at the
certified caps and (separately) at hypothesis loose caps, Master base
cases + direct check, the child-share floor, the R4 tree identity with
the prefix-cone scan, the general-K decorated-charge census with the
anchored-case floor, the exhaustive parity-correct charge-identity census
(P13), and certificate-JSON source/script binding (P15).

Repair note (audit #914, COUNTEREXAMPLE verdict on the integrated
a575019/#880 packet, repaired here): the old universal charge identity
"omega_U = Sigma_U + W_U always" and the old broad-domain P7 pair-2 cap
1.61 were FALSE as shipped (both had explicit numeric counterexamples).
Both are corrected; P13 and P14 are the resulting permanent regression
gates pinning the two counterexamples so they cannot silently regress.

Flags: default run ~10s; --deep extends the envelope/share/coupled-curve
horizons to q = j-1 <= 47 (~90s); --tamper-selftest runs all tampers,
each must FAIL; --emit-cert [--deep] writes the certificate JSON (with
source/script/commit binding) next to the data directory.

stdlib only, deterministic. RESULT: PASS/FAIL summary.
"""
import cmath
import hashlib
import json
import math
import os
import sys
from itertools import product as iproduct, combinations

PI = math.pi

# ------------------------------------------------------- source binding
# Pins this packet's base commit and gives the paths + hashing helper the
# CERT-BIND gate (P15) uses to attest the shipped certificate JSON was
# generated from these exact source bytes (audit #914 SHOULD item: the
# JSON carried no commit/source/script binding and was never re-loaded).
COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
_HERE = os.path.dirname(__file__) or "."
NOTE_PATH = os.path.join(_HERE, "..", "notes", "thresholds",
                         "dense_shell_class_charges.md")
CERT_DIR = os.path.join(_HERE, "..", "data", "certificates",
                        "dense-shell-class-charges")
CERT_PATH = os.path.join(CERT_DIR, "dense_shell_class_charges.json")

def file_sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# ---------------------------------------------------------------- basics

def balanced_digits(x, B):
    y = x % (3 ** B); out = []
    for _ in range(B):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        out.append(d)
    return out

def hatf_by_angles(xi, B):
    """[z^B] prod_i (1 + 2cos(2 pi xi 3^i/c) z + z^2), i-indexed angles."""
    c = 3 ** B
    poly = [1.0]
    for i in range(B):
        t = 2.0 * math.cos(2 * PI * ((xi * (3 ** i)) % c) / c)
        new = [0.0] * (len(poly) + 2)
        for k, cf in enumerate(poly):
            new[k] += cf; new[k + 1] += cf * t; new[k + 2] += cf
        poly = new
    return poly[B]

def scan_states(word):
    u = 0.0; out = []
    for d in word:
        u = (d + u) / 3.0
        out.append(u)
    return out

def hatf_by_scan(word):
    """Same middle coefficient from the scan-state angle multiset."""
    poly = [1.0]
    for u in scan_states(word):
        t = 2.0 * math.cos(2 * PI * u)
        new = [0.0] * (len(poly) + 2)
        for k, cf in enumerate(poly):
            new[k] += cf; new[k + 1] += cf * t; new[k + 2] += cf
        poly = new
    return poly[len(word)]

def dense_words(B):
    return list(iproduct((-1, 1), repeat=B))

def word_to_xi(word, B):
    return sum(d * 3 ** i for i, d in enumerate(word)) % (3 ** B)

# ------------------------------------------------- subset charge table

def subset_table(B):
    """T[S] = sum_words hatf * prod_{k in S} 2cos(2 pi u_k), S over scan
    positions {1..B} (bit k-1). O(4^B)."""
    T = [0.0] * (1 << B)
    for word in dense_words(B):
        h = hatf_by_scan(word)
        ins = [2.0 * math.cos(2 * PI * u) for u in scan_states(word)]
        vec = [h]
        for f in ins:
            vec = vec + [x * f for x in vec]
        for S, val in enumerate(vec):
            T[S] += val
    return T

# ------------------------------------------------------- radix-3 FFT

def fft3(vals, sign):
    """X[k] = sum_j vals[j] * exp(sign * 2 pi i j k / n), n = 3^m."""
    n = len(vals)
    if n == 1:
        return vals[:]
    third = n // 3
    A = [fft3(vals[r::3], sign) for r in range(3)]
    X = [0j] * n
    for k in range(third):
        for j in range(3):
            kk = k + j * third
            wkk = cmath.exp(sign * 2j * PI * kk / n)
            X[kk] = A[0][k] + wkk * A[1][k] + wkk * wkk * A[2][k]
    return X

# ---------------------------------------------------------------- gates

def gate_def(report, Bs=(4, 6, 8)):
    worst = 0.0
    for B in Bs:
        for word in dense_words(B):
            xi = word_to_xi(word, B)
            worst = max(worst, abs(hatf_by_angles(xi, B) - hatf_by_scan(word)))
    ok = worst < 1e-9
    report.append(("G1 DEF reordering identity (B<=%d), worst dev" % max(Bs),
                   "%.2e" % worst, ok))
    return ok

def gate_kernel(report, Bs=(4, 6), flip_tamper=False):
    worst = 0.0
    for B in Bs:
        c = 3 ** B
        words = dense_words(B)
        xis = [word_to_xi(w, B) for w in words]
        hs = [hatf_by_scan(w) for w in words]
        # sigma-side brute class sums
        brute = {}
        for sigma in range(c):
            h = sum(hv * math.cos(2 * PI * ((xi * sigma) % c) / c)
                    for xi, hv in zip(xis, hs)) / c
            v = tuple(1 if d != 0 else 0 for d in balanced_digits(sigma, B))
            brute[v] = brute.get(v, 0.0) + h
        # kernel form + insertion table
        T = subset_table(B)
        for v, s in brute.items():
            U = [i for i, b in enumerate(v) if b]
            kern = sum(hv * math.prod(
                2.0 * math.cos(2 * PI * ((xi * (3 ** i)) % c) / c) for i in U)
                for xi, hv in zip(xis, hs)) / c
            if flip_tamper:
                S2 = sum(1 << i for i in U)          # tamper: flip dropped
            else:
                S2 = sum(1 << (B - 1 - i) for i in U)
            worst = max(worst, abs(kern - s), abs(T[S2] / c - s))
    ok = worst < 1e-9
    report.append(("G2 KERNEL class-sum == kernel form == insertion table "
                   "(B in %s), worst dev" % (Bs,), "%.2e" % worst, ok))
    return ok

def gate_law(report, Bs=(4, 6, 8, 10), parity_tamper=False):
    ok = True
    margins = {}
    shift = 1 if parity_tamper else 0
    for B in Bs:
        T = subset_table(B)
        c = 3 ** B
        minmag = float("inf")
        for S in range(1 << B):
            want = 1 if (B - bin(S).count("1") + shift) % 2 == 0 else -1
            val = T[S] / c
            if (val > 0) != (want > 0):
                ok = False
            minmag = min(minmag, abs(val))
        margins["B%d" % B] = minmag
        floor = {4: 2.6, 6: 6.5, 8: 17.7, 10: 49.2}.get(B, 0.0)
        report.append(("G3 LAW sign(class-sum)=(-1)^(B-|U|) exhaustive B=%d, "
                       "min |class-sum| (floor %.1f)" % (B, floor),
                       "%.3e" % minmag, minmag >= floor))
        if minmag < floor:
            ok = False
    report.append(("G3 LAW all signs correct", str(ok), ok))
    return ok, margins

LEAK_PINS = {4: 9.3e-06, 5: 1.30e-03, 6: 7.8e-03, 7: 2.72e-02,
             8: 6.63e-02, 9: 1.21e-01, 10: 1.86e-01}

def gate_leak(report, B=10):
    c = 3 ** B
    F = [0j] * c
    for word in dense_words(B):
        F[word_to_xi(word, B)] = hatf_by_scan(word)
    H = fft3(F, -1)          # h(sigma) * c
    wrong = [0.0] * (B + 1); total = [0.0] * (B + 1)
    for sigma in range(c):
        h = H[sigma].real / c
        m = sum(1 for d in balanced_digits(sigma, B) if d != 0)
        want = 1 if (B - m) % 2 == 0 else -1
        total[m] += abs(h)
        if h * want < 0:
            wrong[m] += abs(h)
    ok = True
    table = {}
    for m in range(B + 1):
        share = wrong[m] / total[m] if total[m] > 0 else 0.0
        table[m] = share
        if m <= 3 and share > 1e-12:
            ok = False
        if m in LEAK_PINS:
            if abs(share - LEAK_PINS[m]) > 0.05 * max(LEAK_PINS[m], 1e-9) + 1e-7:
                ok = False
    report.append(("G4 LEAK B=10 pure through |U|<=3; pins 4..10 match",
                   " ".join("%d:%.3g" % (m, table[m]) for m in range(4, B + 1)),
                   ok))
    return ok, table

# ------------------------------------------- P13: charge-identity gate

def gate_c6_parity(report, Bs=tuple(range(1, 9)), tamper=None):
    """P13 C6-PARITY (audit #914 MUST-repair, now a permanent regression
    gate): exhaustively checks the parity-correct charge identity

        omega_U = W_U + 1_{s_U=+1} |Sigma_U|          (sign-law form)
        omega_U = (M_U + Sigma_U) / 2                 (always-valid form)

    for EVERY support class U at EVERY B <= max(Bs), both parities
    s_U = (-1)^(B-|U|). omega_U = h_+ (sum of the positive class values,
    definitional); Sigma_U the signed class sum; W_U the wrong-sign mass
    (sign(h) != s_U); M_U = sum |h| the total variation. The old
    'omega_U = Sigma_U + W_U always' claim is correct only at s_U = +1;
    the audit's B=4, U={0} witness (s_U=-1) is printed explicitly:
    Sigma_U=-3.599182825207051, W_U=omega_U=0, so the old formula would
    give Sigma_U+W_U=-3.599... != 0. Tamper 'ident-universal' reinstates
    the false always-form so this gate (only) catches it."""
    worst_sign = 0.0
    worst_general = 0.0
    witness = None
    for B in Bs:
        c = 3 ** B
        F = [0j] * c
        for word in dense_words(B):
            F[word_to_xi(word, B)] = hatf_by_scan(word)
        H = fft3(F, -1)
        Sigma = {}; W = {}; Omega = {}; M = {}
        for sigma in range(c):
            h = H[sigma].real / c
            digits = balanced_digits(sigma, B)
            U = tuple(i for i, d in enumerate(digits) if d != 0)
            s_U = 1 if (B - len(U)) % 2 == 0 else -1
            Sigma[U] = Sigma.get(U, 0.0) + h
            M[U] = M.get(U, 0.0) + abs(h)
            Omega[U] = Omega.get(U, 0.0) + max(h, 0.0)
            wrong = W.get(U, 0.0)
            if h * s_U < 0:
                wrong += abs(h)
            W[U] = wrong
        for U, sigma_u in Sigma.items():
            s_U = 1 if (B - len(U)) % 2 == 0 else -1
            w_u = W[U]; m_u = M[U]; om_u = Omega[U]
            if tamper == "ident-universal":
                pred_sign = sigma_u + w_u             # the FALSE always-form
            else:
                pred_sign = w_u + (abs(sigma_u) if s_U > 0 else 0.0)
            pred_general = (m_u + sigma_u) / 2.0
            worst_sign = max(worst_sign, abs(om_u - pred_sign))
            worst_general = max(worst_general, abs(om_u - pred_general))
            if B == 4 and U == (0,):
                witness = (sigma_u, w_u, om_u, s_U)
    ok = (worst_sign < 1e-9) and (worst_general < 1e-9)
    wsig, wwit, owit, swit = witness
    report.append((
        "P13 C6-PARITY omega_U=W_U+1[s_U=+1]|Sigma_U| (also "
        "(M_U+Sigma_U)/2), ALL U every B<=%d both parities; audit "
        "witness B=4 U={0}: Sigma_U=%.9f W_U=%.9f omega_U=%.9f s_U=%+d"
        % (max(Bs), wsig, wwit, owit, swit),
        "max|dev| sign-law=%.2e general=%.2e" % (worst_sign, worst_general),
        ok))
    return ok

# ------------------------------------ G5: transfer DP + certified tail

def dp_subset_charge(B, S_scan, K_nodes, noins=False):
    """T[S]/1 via backward function-valued DP: H_m(z; u) over Chebyshev
    nodes u in [-1/2, 1/2]; H_m = sum_d (1 + t(u_d) z + z^2) *
    (t(u_d) if inserted) * H_{m-1}(u_d); answer [z^B] H_B(0).
    Level m consumes scan position m (1-indexed from the deepest); the
    scan runs forward k = 1..B, so level m corresponds to scan position
    k = m counted from the START at u: H builds suffixes from state u;
    at u = 0 the full word product is recovered with u_1 = d_1/3 ...
    i.e. inserted scan positions k map to DP level (B - k + 1)."""
    nodes = [0.5 * math.cos(PI * m / K_nodes) for m in range(K_nodes + 1)]
    bw = [(0.5 if m in (0, K_nodes) else 1.0) * (1 if m % 2 == 0 else -1)
          for m in range(K_nodes + 1)]

    def bary(x, vals):
        for m, xm in enumerate(nodes):
            if abs(x - xm) < 1e-15:
                return vals[m][:]
        num = [0.0] * len(vals[0]); den = 0.0
        for m, xm in enumerate(nodes):
            s = bw[m] / (x - xm); den += s
            vm = vals[m]
            for i in range(len(num)):
                num[i] += s * vm[i]
        return [v / den for v in num]

    H = [[1.0] for _ in nodes]
    for lev in range(1, B + 1):
        k_scan = B - lev + 1
        ins = (k_scan in S_scan) and not noins
        out = []
        for u in nodes:
            acc = None
            for d in (-1.0, 1.0):
                ud = (d + u) / 3.0
                t = 2.0 * math.cos(2 * PI * ud)
                g = bary(ud, H)
                new = [0.0] * (len(g) + 2)
                for i, cf in enumerate(g):
                    new[i] += cf; new[i + 1] += cf * t; new[i + 2] += cf
                if ins:
                    new = [t * x for x in new]
                acc = new if acc is None else [x + y for x, y in zip(acc, new)]
            out.append(acc)
        H = out
    final = bary(0.0, H)
    return final[B]

def gate_dp(report, B=6, K=24, noins_tamper=False):
    T = subset_table(B)
    cases = [(), (3,), (2, 5), (1, 6), (4,)]
    rho = 5.0
    lam = 2 * 2 * math.cosh(2 * PI * (rho - 1 / rho) / 12)      # 24.85
    fac = 2 * math.cosh(2 * PI * (rho - 1 / rho) / 12)          # 12.42
    worst = 0.0; ok = True
    for S in cases:
        got = dp_subset_charge(B, set(S), K, noins=noins_tamper)
        Sbits = sum(1 << (k - 1) for k in S)
        ref = T[Sbits]
        bar = 4 * (lam ** B) * (fac ** len(S)) * (rho ** -K) / (rho - 1)
        err = abs(got - ref)
        worst = max(worst, err)
        if err > bar:
            ok = False
    report.append(("G5 DP subset charges (B=%d,K=%d) vs table, worst obs err "
                   "(certified bars hold)" % (B, K), "%.2e" % worst, ok))
    return ok

# -------------------------------------------- proof-layer gates (P*)

def need_eps(eps):
    return math.sin(2 * PI * eps / 3) / math.sin(2 * PI * (1.0 / 6 + eps / 3))

def a_of(t):
    s = math.sin(PI * t)
    return s * s

def gate_atom(report, tamper=None):
    """P1: the ATOM. f(phi) = sin(7pi/18) cos(phi) - sin(pi/18) cos(phi/2)
    on [2pi/9, 4pi/9]: f' < 0 throughout and f(4pi/9) = sin^2(pi/18)."""
    s7, s1 = math.sin(7 * PI / 18), math.sin(PI / 18)
    if tamper == "atom-endpoint":
        s1 *= 1.0 + 1e-6
    end = s7 * math.cos(4 * PI / 9) - s1 * math.cos(2 * PI / 9)
    ok_end = abs(end - math.sin(PI / 18) ** 2) < (1e-15 if tamper != "atom-endpoint" else 0.0)
    ok_mono = True; ok_pos = True
    N = 20000
    for k in range(N + 1):
        phi = 2 * PI / 9 + (2 * PI / 9) * k / N
        f = s7 * math.cos(phi) - s1 * math.cos(phi / 2)
        fp = -s7 * math.sin(phi) + 0.5 * s1 * math.sin(phi / 2)
        if f <= 0:
            ok_pos = False
        if fp >= 0:
            ok_mono = False
    # equivalence with the j=1 master statement on an eps grid
    ok_eq = True
    for k in range(1, 1000):
        eps = 0.25 * k / 1000
        lhs = 0.5 - a_of((5.0 / 12 + eps / 3) / 3)
        rhs = need_eps(eps) * (0.5 - a_of((0.25 - eps / 3) / 3))
        if lhs <= rhs:
            ok_eq = False
    # the coupling identity drift(t_out)*need(eps) = |drift(t_in)| EXACTLY:
    # need is critical, not adjustable (tamper 'coupling-off' scales it)
    scale = 1.02 if tamper == "coupling-off" else 1.0
    wcpl = 0.0
    for k in range(1, 2000):
        eps = 0.25 * k / 2000
        d_out = 0.5 * math.sin(2 * PI * (1.0 / 6 + eps / 3))
        d_in = 0.5 * math.sin(2 * PI * eps / 3)
        wcpl = max(wcpl, abs(d_out * scale * need_eps(eps) - d_in))
    ok_cpl = wcpl < 1e-15
    ok = ok_end and ok_mono and ok_pos and ok_eq and ok_cpl
    report.append(("P1 ATOM: endpoint = sin^2(pi/18), monotone, positive; "
                   "== (M_1); coupling identity exact",
                   "end dev %.1e cpl dev %.1e" % (abs(end - math.sin(PI / 18) ** 2), wcpl), ok))
    return ok

def _cascade_G(jmax, Kn=64):
    nodes = [0.25 * (1 + math.cos(PI * m / Kn)) for m in range(Kn + 1)]
    bw = [(0.5 if m in (0, Kn) else 1.0) * (1 if m % 2 == 0 else -1)
          for m in range(Kn + 1)]

    def bary(x, vals):
        for m, xm in enumerate(nodes):
            if abs(x - xm) < 1e-15:
                return vals[m][:]
        num = [0.0] * len(vals[0]); den = 0.0
        for m, xm in enumerate(nodes):
            s = bw[m] / (x - xm); den += s
            vm = vals[m]
            for i in range(len(num)):
                num[i] += s * vm[i]
        return [v / den for v in num]

    def mult_root(c, a):
        out = [0.0] * (len(c) + 1)
        for i, ci in enumerate(c):
            out[i] += (0.5 - a) * ci
            out[i + 1] += (0.25 if i >= 1 else 0.5) * ci
            if i >= 1:
                out[i - 1] += 0.25 * ci
        return out

    lev = [[[1.0] for _ in nodes]]
    for j in range(1, jmax + 1):
        prev = lev[-1]; out = []
        for t in nodes:
            acc = None
            for d in (-1.0, 1.0):
                tv = abs((d + t) / 3.0)
                cvec = mult_root(bary(tv, prev), a_of(tv))
                acc = cvec if acc is None else [x + y for x, y in zip(acc, cvec)]
            out.append(acc)
        lev.append(out)
    return nodes, bw, bary, mult_root, lev

def gate_A_purity(report, tamper=None, jmax=12):
    """P4: A_j(t) = sum_d drift(t_d) N G_{j-1}(t_d) cone-pure on
    [1/6, 1/2); the a-parity-flip tamper corrupts the cone convention
    and must break this scan."""
    nodes, bw, bary, mult_root, lev = _cascade_G(jmax)

    def flip(c):
        d = len(c) - 1
        return [ci if (d - i) % 2 == 0 else -ci for i, ci in enumerate(c)]

    def flipT(c):
        # tampered parity flip (off by one) -- must break the scan
        d = len(c) - 1
        return [ci if (d - i + 1) % 2 == 0 else -ci for i, ci in enumerate(c)]

    FL = flipT if tamper == "a-parity-flip" else flip
    worstA = float("inf")
    for j in (4, 8, jmax):
        for k in range(500):
            t = 1.0 / 6 + k * (1.0 / 3 - 1e-4) / 499
            acc = None
            for d in (-1.0, 1.0):
                td = abs((d + t) / 3.0); ad = a_of(td)
                v = mult_root(bary(td, lev[j - 1]), ad)
                v = [(ad - 0.5) * x for x in v]
                acc = v if acc is None else [x + y for x, y in zip(acc, v)]
            b = FL(acc)
            mn = min(x / (sum(abs(y) for y in b)) for x in b)
            worstA = min(worstA, mn)
    ok = worstA > 0
    report.append(("P4 A-purity scan (drift-aggregated cone, j<=%d)"
                   % jmax, "min %.3e" % worstA, ok))
    return ok

# -------------------------------------------- P5-P11: proof-layer gates
# Proof-layer gates: the differential envelope, the Master step's scalar
# spine, base cases, the R4 tree identity, and the general-K census; the Master
# envelope (E) + induction-step (KEY) + general-K (T_pi) proof chain for
# the |K|=1 (and conjecturally general-K) class-charge sign law. Same
# flipped shifted-Chebyshev conventions as P1/P4 above: b_i=(-1)^{deg-i}
# coeff_i, cone == b>=0 entrywise, N_a = "multiply by (x-a)" (mult_root
# below); a(t)=sin^2(pi t) (a_of, already defined); children of t:
# t_+=(1+t)/3, t_-=(1-t)/3. stdlib only, deterministic; no cross-file
# imports (all lab machinery re-derived below).

def mult_root(c, a):
    """(x - a) * P in raw shifted-Chebyshev coords (tridiagonal step)."""
    n = len(c); out = [0.0] * (n + 1)
    for i, ci in enumerate(c):
        out[i] += (0.5 - a) * ci
        out[i + 1] += (0.25 if i >= 1 else 0.5) * ci
        if i >= 1:
            out[i - 1] += 0.25 * ci
    return out

def flip(c):
    d = len(c) - 1
    return [ci if (d - i) % 2 == 0 else -ci for i, ci in enumerate(c)]

def da_of(t):
    return PI * math.sin(2.0 * PI * t)

def vadd(x, y):
    n = max(len(x), len(y)); r = [0.0] * n
    for i in range(len(x)): r[i] += x[i]
    for i in range(len(y)): r[i] += y[i]
    return r

def vsub(x, y):
    n = max(len(x), len(y)); r = [0.0] * n
    for i in range(len(x)): r[i] += x[i]
    for i in range(len(y)): r[i] -= y[i]
    return r

def vscale(s, x):
    return [s * v for v in x]

def GD_direct(j, u):
    """Exact (no-interpolation) joint (G_j, DG_j) tree recursion -- Lemma
    L0's exact-derivative identity, chain rule through t_+=(1+u)/3,
    t_-=(1-u)/3."""
    if j == 0:
        return [1.0], [0.0]
    tp = (1.0 + u) / 3.0; tm = (1.0 - u) / 3.0
    Gp, Dp = GD_direct(j - 1, tp); Gm, Dm = GD_direct(j - 1, tm)
    ap = a_of(tp); am = a_of(tm)
    g = vadd(mult_root(Gp, ap), mult_root(Gm, am))
    php = vsub(mult_root(Dp, ap), vscale(da_of(tp), Gp))
    phm = vsub(mult_root(Dm, am), vscale(da_of(tm), Gm))
    d = vscale(1.0 / 3.0, vsub(php, phm))
    return g, d

K_GD = 96
NODES_GD = [0.25 * (1.0 + math.cos(PI * m / K_GD)) for m in range(K_GD + 1)]
BW_GD = [(0.5 if m in (0, K_GD) else 1.0) * (1.0 if m % 2 == 0 else -1.0)
         for m in range(K_GD + 1)]
GD_FLOOR = 1e-13

def bary_gd(tq, vals):
    for m, tm in enumerate(NODES_GD):
        if abs(tq - tm) < 1e-15:
            return vals[m][:]
    num = None; den = 0.0
    for m, tm in enumerate(NODES_GD):
        s = BW_GD[m] / (tq - tm); den += s; vm = vals[m]
        if num is None: num = [0.0] * len(vm)
        for i in range(len(vm)): num[i] += s * vm[i]
    return [x / den for x in num]

def build_gd_cascade(jmax):
    """Interpolated (G_j, DG_j) cascade on Chebyshev-Lobatto nodes over
    [0,1/2] (barycentric interpolation; shared by P6/P7/P9)."""
    G = [[[1.0] for _ in NODES_GD]]; D = [[[0.0] for _ in NODES_GD]]
    for j in range(1, jmax + 1):
        Gp = G[-1]; Dp = D[-1]; gout = []; dout = []
        for t in NODES_GD:
            tp = (1.0 + t) / 3.0; tm = (1.0 - t) / 3.0
            ap = a_of(tp); am = a_of(tm)
            Gtp = bary_gd(tp, Gp); Gtm = bary_gd(tm, Gp)
            Dtp = bary_gd(tp, Dp); Dtm = bary_gd(tm, Dp)
            g = vadd(mult_root(Gtp, ap), mult_root(Gtm, am))
            php = vsub(mult_root(Dtp, ap), vscale(da_of(tp), Gtp))
            phm = vsub(mult_root(Dtm, am), vscale(da_of(tm), Gtm))
            d = vscale(1.0 / 3.0, vsub(php, phm))
            gout.append(g); dout.append(d)
        G.append(gout); D.append(dout)
    return G, D

def G_at(lev, j, t):
    return bary_gd(t, lev[j])

def D_at(lev, j, t):
    return bary_gd(t, lev[j])

def eps_grid(n):
    g = [0.25 * k / n for k in range(1, n)]
    g += [0.24, 0.245, 0.249, 0.2499, 0.24999, 0.249999]
    return sorted(set(x for x in g if 0.0 < x < 0.25))

def gate_dg(report):
    """P5: DG exact-derivative identity (L0 recursion) matches central
    finite differences of the exact tree, j in {4,6}; plus the
    top-defect-exactly-zero structural fact (Lemma L1: top(G_j)=2^{1-j}
    is t-independent so DG_j's top entry is 0)."""
    h = 1e-6; wfd = 0.0; wtop = 0.0
    for j in (4, 6):
        for t in (0.18, 0.25, 0.33, 0.41, 0.47):
            gph, _ = GD_direct(j, t + h)
            gmh, _ = GD_direct(j, t - h)
            fd = vscale(1.0 / (2 * h), vsub(gph, gmh))
            g_t, d_t = GD_direct(j, t)
            n = min(len(fd), len(d_t))
            wfd = max(wfd, max(abs(fd[i] - d_t[i]) for i in range(n)))
            wtop = max(wtop, abs(d_t[j]))
    # L5 trace-derivative cancellation: a'(t_+) - a'(t_-) = -a'(t/3)
    wl5 = 0.0
    for k in range(1, 400):
        t = 0.5 * k / 400
        lhs = PI * math.sin(2 * PI * (1 + t) / 3) - PI * math.sin(2 * PI * (1 - t) / 3)
        wl5 = max(wl5, abs(lhs + PI * math.sin(2 * PI * t / 3)))
    ok = (wfd < 1e-6) and (wtop < 1e-12) and (wl5 < 1e-12)
    report.append(("P5 DG exact-derivative identity (j in {4,6}) vs "
                   "central FD; top-defect; L5 cancellation",
                   "dev=%.2e top=%.2e L5=%.2e" % (wfd, wtop, wl5), ok))
    return ok

L4_REGIONS = [("[1/6,.22]", 1.0 / 6, 0.22), ("[.22,.30]", 0.22, 0.30),
              ("[.30,.38]", 0.30, 0.38), ("[.38,.44]", 0.38, 0.44),
              ("[.44,.50]", 0.44, 0.49995)]
L4_CAP = {"[1/6,.22]": 0.62, "[.22,.30]": 0.87, "[.30,.38]": 1.05,
          "[.38,.44]": 1.22, "[.44,.50]": 1.32}         # sup(j>=2), rounded up
PAIR1 = ("pair-1 [1/6,0.2778]", 1.0 / 6, 0.27778)
PAIR2 = ("pair-2 [.3889,.50]", 0.38889, 0.49995)

def grid(lo, hi, n):
    return [lo + k * (hi - lo) / n for k in range(n + 1)]

def region_of(s):
    for (nm, a, b) in L4_REGIONS:
        if a - 1e-9 <= s <= b + 1e-9:
            return nm
    return "[.44,.50]"

def gate_l4(report, Glev, Dlev, jmax=12):
    """P6: one-step differential bound RHS(L4) - |DG_j| >= 0 on a
    moderate grid, j<=jmax, both pair supports."""
    minslack = float("inf")
    for (nm, lo, hi) in (PAIR1, PAIR2):
        ms = float("inf")
        for j in range(2, jmax + 1):
            for t in grid(lo, hi, 60):
                tp = (1.0 + t) / 3.0; tm = (1.0 - t) / 3.0
                ap = a_of(tp); am = a_of(tm)
                Gp = G_at(Glev, j - 1, tp); Gm = G_at(Glev, j - 1, tm)
                Dp = D_at(Dlev, j - 1, tp); Dm = D_at(Dlev, j - 1, tm)
                Vp = mult_root(Gp, ap); Vm = mult_root(Gm, am)
                Gj = vadd(Vp, Vm); DGj = D_at(Dlev, j, t)
                Lp = L4_CAP[region_of(tp)]; Lm = L4_CAP[region_of(tm)]
                sminus = max(0.0, 0.5 - am)
                dap = da_of(tp); dam = da_of(tm)
                for i in range(len(Gj)):
                    if abs(Gj[i]) <= GD_FLOOR:
                        continue
                    vp_i = Vp[i] if i < len(Vp) else 0.0
                    vm_i = Vm[i] if i < len(Vm) else 0.0
                    gmm = Gm[i] if i < len(Gm) else 0.0
                    gpp = Gp[i] if i < len(Gp) else 0.0
                    term_p = Lp * abs(vp_i)
                    term_m = Lm * (abs(vm_i) + 2 * sminus * abs(gmm))
                    t2i = abs(dap * gpp - dam * gmm)
                    rhs = (term_p + term_m + t2i) / 3.0
                    lhs = abs(DGj[i]) if i < len(DGj) else 0.0
                    ms = min(ms, rhs - lhs)
        minslack = min(minslack, ms)
    ok = minslack >= 0.0
    report.append(("P6 L4 one-step differential bound (j<=%d, both pair "
                   "supports), min slack" % jmax, "%+.3e" % minslack, ok))
    return ok

def secant_of_pair(Glev, j, x, y):
    """Secant exponent of flip(G_j) between two argument points x, y."""
    gx = flip(G_at(Glev, j, x)); gy = flip(G_at(Glev, j, y))
    r = 1e9
    for i in range(min(len(gx), len(gy))):
        if gx[i] > GD_FLOOR and gy[i] > GD_FLOOR:
            r = min(r, gx[i] / gy[i], gy[i] / gx[i])
    g = abs(y - x)
    return -math.log(max(r, 1e-15)) / g

def secant_env(Glev, j, lo, hi, gmin, gmax, n=110, pts=None):
    ts = pts if pts is not None else grid(lo, hi, n)
    w = 0.0
    for x in range(len(ts)):
        for y in range(x + 1, len(ts)):
            g = ts[y] - ts[x]
            if g > gmax + 1e-12 or g < max(gmin, 1e-6) - 1e-12:
                continue
            Lv = secant_of_pair(Glev, j, ts[x], ts[y])
            if Lv > w:
                w = Lv
    return w

def forced_grid(lo, hi, n):
    """Uniform (n+1)-point grid over [lo,hi] with the exact
    boundary-adjacent points at gap 1/18 and 1/9 from each end forced
    in. Audit #914's P7 counterexample sits exactly at hi - 1/18 with
    y = hi; a plain uniform grid can straddle both and hide the true
    supremum, which is how the shipped gate silently missed it."""
    base = [lo + k * (hi - lo) / n for k in range(n + 1)]
    forced = [lo, hi, lo + 1.0 / 18, lo + 1.0 / 9, hi - 1.0 / 18, hi - 1.0 / 9]
    pts = base + [p for p in forced if lo - 1e-12 <= p <= hi + 1e-12]
    return sorted(set(round(p, 15) for p in pts))

def _pair1_curve(eps):
    """t_out's inner child s and t_in's plus child r (s + r = 4/9
    exactly, the pair-1 analog of pair-2's r2+s2=8/9)."""
    return 7.0 / 36 - eps / 9.0, 1.0 / 4 + eps / 9.0

def _pair2_curve(eps):
    """t_in's minus child r2 and t_out's outer child s2 (r2+s2=8/9
    exactly -- the coupled relation Step B of 3.2 actually uses)."""
    return 5.0 / 12 - eps / 9.0, 17.0 / 36 + eps / 9.0

def _coupled_eps_grid(n, tamper=None):
    """n+1 eps-nodes over [0,1/4], BOTH endpoints included exactly.
    Tamper 'p7-domain' silently re-shrinks the top endpoint (the
    original audited bug: hi=0.49995 instead of the stated 0.50) so
    the endpoint-inclusion check below (only) catches it."""
    hi = 0.24999 if tamper == "p7-domain" else 0.25
    return [hi * k / n for k in range(n + 1)]

def gate_env(report, Glev, tamper=None, jmax=16):
    """P7 (repaired per audit #914): sharp envelope secant constants
    restricted to the two MASTER-consumed COUPLED child curves --
    pair-1 (s+r=4/9), pair-2 (r2+s2=8/9), see 3.2 Step B -- at levels
    q = j-1 in [5, min(jmax,47)] (the general step needs j>=6, and the
    B<=49 leg needs j<=48), eps in [0,1/4] with BOTH boundary
    endpoints, n=440 (4x the former n=110 whole-support grid). This
    THEOREM-supporting gate supersedes the old whole-support pairwise
    census (now P14 ENV-BROAD, informational): audit #914's
    counterexample (j=3, x=4/9, y=1/2) is off both curves
    (x+y=17/18 != 8/9) and below q=5, so it is out of scope by
    construction here, not by a silently shrunk domain -- the
    endpoints_ok flag below is the check that the domain itself is not
    quietly re-shrunk the way the original gate was."""
    cap1 = 0.55 if tamper == "env-tightcap" else 0.85
    cap2 = 1.61
    n = 440
    eps_nodes = _coupled_eps_grid(n, tamper=tamper)
    endpoints_ok = (abs(eps_nodes[0] - 0.0) < 1e-15
                    and abs(eps_nodes[-1] - 0.25) < 1e-15)
    qmax = min(jmax, 47)
    sup1 = 0.0; sup2 = 0.0; arg1 = None; arg2 = None
    for q in range(5, qmax + 1):
        for eps in eps_nodes:
            x1, y1 = _pair1_curve(eps)
            L1 = secant_of_pair(Glev, q, x1, y1)
            if L1 > sup1:
                sup1 = L1; arg1 = (q, eps)
            x2, y2 = _pair2_curve(eps)
            L2 = secant_of_pair(Glev, q, x2, y2)
            if L2 > sup2:
                sup2 = L2; arg2 = (q, eps)
    ok = (sup1 <= cap1) and (sup2 <= cap2) and endpoints_ok
    report.append((
        "P7 ENV coupled-curve secants (pair-1 s+r=4/9, pair-2 "
        "r2+s2=8/9), q=j-1 in [5,%d], eps-grid n=%d incl. both "
        "endpoints: pair-1<=%.2f pair-2<=%.2f" % (qmax, n, cap1, cap2),
        "sup1=%.4f@%s sup2=%.4f@%s endpoints_ok=%s"
        % (sup1, arg1, sup2, arg2, endpoints_ok), ok))
    return ok, {"pair1": sup1, "pair2": sup2}

def gate_env_broad(report, Glev, tamper=None, jmax=16):
    """P14 ENV-BROAD (audit #914 honesty exhibit; COMPUTED,
    informational -- NOT MASTER-consumed, NOT a THEOREM ingredient):
    the old whole-support pairwise secant census, on the TRUE stated
    domain (pair-2 to its exact endpoint 0.50, not the silently
    shrunk 0.49995) with boundary-adjacent points forced into the
    grid so the true supremum cannot be hidden between nodes.
    Reproduces audit #914's pair-2 counterexample honestly (sup ~
    1.6101 > the old false cap 1.61) while showing pair-1 in fact
    holds even on this broader domain/level range. The cap is
    corrected (1.62), not the falsified 1.61; tamper 'p7-cap' restores
    1.61 so this gate (only) catches a reinstated false claim."""
    cap1 = 0.85
    cap2 = 1.61 if tamper == "p7-cap" else 1.62
    n = 110
    lo1, hi1 = PAIR1[1], PAIR1[2]
    lo2, hi2 = PAIR2[1], 0.5             # true endpoint, not .49995
    ts1 = forced_grid(lo1, hi1, n)
    ts2 = forced_grid(lo2, hi2, n)
    sup1 = 0.0; sup2 = 0.0
    for q in range(2, min(jmax, 48) + 1):
        sup1 = max(sup1, secant_env(Glev, q, lo1, hi1, 1.0 / 18, 1.0 / 9,
                                     pts=ts1))
        sup2 = max(sup2, secant_env(Glev, q, lo2, hi2, 1.0 / 18, 1.0 / 9,
                                     pts=ts2))
    ok = (sup1 <= cap1) and (sup2 <= cap2)
    report.append((
        "P14 ENV-BROAD informational whole-support census (NOT "
        "MASTER-consumed; COMPUTED honesty exhibit), true domain incl. "
        "endpoint 0.50, 2<=q<=%d: pair-1<=%.2f pair-2<=%.2f (corrected "
        "cap)" % (min(jmax, 48), cap1, cap2),
        "sup1=%.4f sup2=%.4f" % (sup1, sup2), ok))
    return ok, {"pair1": sup1, "pair2": sup2}

def gate_key(report, tamper=None):
    """P8: the (KEY) scalar inequality tying envelope+share constants
    together, 4000-pt eps grid, monotone decreasing, endpoint margin.
    Two instantiations, DIFFERENT epistemic status (audit #914 MUST
    item -- do not conflate them): the sharp-cap check carries no
    external hypothesis on the B<=49 leg (its inputs are gate
    P7/P12-certified); the
    loose-cap check is a CONDITIONAL IMPLICATION only -- 'IF the all-j
    envelope/share hypotheses (1.086, 1.663, 1.20) hold, THEN (KEY)
    holds with margin >= 0.015' -- since no gate in this file produces
    those hypotheses. A producer now exists outside this packet: PR
    #905 (head 0000964) proves the 1.086/1.663 envelopes and a 7/6
    share floor via a positive two-state cone, modulo #905's own
    finite Arb continuum certificate (independently audited in #911,
    head 8d47b40: symbolic half verified, Arb half not replayed)."""
    L1S, L2S = 0.85, 1.61          # the P7-certified envelope caps
    L1L, L2L = 1.086, 1.663        # HYPOTHESIS loose caps (producer: #905)
    GAMMA = 1.0 if tamper == "key-noshare" else 1.20
    s49 = math.sin(4 * PI / 9)

    def Fgen(eps, L1, L2):
        g = 1.0 / 18 + 2.0 * eps / 9.0
        rho1 = math.exp(-L1 * g); rho2 = math.exp(-L2 * g)
        nd = need_eps(eps)
        D1 = s49 * math.sin(PI * g)
        return (min(rho1, rho2) - nd) * GAMMA * rho1 - D1

    def F(eps):
        return Fgen(eps, L1S, L2S)

    worst = float("inf"); prevF = None; mono = True
    for eps in eps_grid(4000):
        Fv = F(eps)
        worst = min(worst, Fv)
        if prevF is not None and Fv > prevF + 1e-12:
            mono = False
        prevF = Fv
    Fend = F(0.25 - 1e-9)
    worstL = min(Fgen(eps, L1L, L2L) for eps in eps_grid(4000))
    ok = (worst > 0.0) and mono and (Fend >= 0.030 - 1e-3) and (worstL >= 0.015 - 1e-3)
    report.append(("P8 KEY scalar: no external hypothesis at sharp caps "
                   "(0.85,1.61,1.20); CONDITIONAL IMPLICATION only at "
                   "HYPOTHESIS loose caps (1.086,1.663,1.20) -- producer "
                   "PR #905 head 0000964, audited #911 head 8d47b40",
                   "minF=%.4f mono=%s Fend=%.4f minF_loose(hyp)=%.4f"
                   % (worst, mono, Fend, worstL), ok))
    return ok, Fend

def gate_base(report, Glev):
    """P9: Master base cases. (a) j=2..5 Lipschitz-certified grid floors,
    2000-pt eps grid. (b) direct Master check Delta>=0
    entrywise, j<=16 (trimmed), strict entries 0,1."""
    grid_a = eps_grid(2000); h = 0.25 / 2000
    floors = {}; ok_a = True
    for j in (2, 3, 4, 5):
        dmins = []
        for eps in grid_a:
            tin = 0.25 - eps / 3.0; tout = 5.0 / 12 + eps / 3.0
            gi = flip(GD_direct(j, tin)[0]); go = flip(GD_direct(j, tout)[0])
            nd = need_eps(eps)
            dmins.append(min(go[i] - nd * gi[i] for i in range(len(go))))
        worst_abs = min(dmins)
        maxslope = 0.0
        for k in range(1, len(dmins)):
            maxslope = max(maxslope, abs(dmins[k] - dmins[k - 1]) / h)
        cert = worst_abs - maxslope * h / 2
        floors[j] = cert
        if cert <= 0.0:
            ok_a = False

    Bj_list = (1, 2, 3, 4, 6, 8, 10, 12, 14, 16)
    grid_b = eps_grid(400)
    ok_b = True; worst_delta = float("inf")
    for j in Bj_list:
        for eps in grid_b:
            tin = 0.25 - eps / 3.0; tout = 5.0 / 12 + eps / 3.0
            gi = flip(G_at(Glev, j, tin)); go = flip(G_at(Glev, j, tout))
            nd = need_eps(eps)
            D = [go[i] - nd * gi[i] for i in range(len(go))]
            dm = min(D)
            worst_delta = min(worst_delta, dm)
            if dm < 0.0 or D[0] <= 0.0 or (len(D) > 1 and D[1] <= 0.0):
                ok_b = False
    ok = ok_a and ok_b
    report.append(("P9 BASE Lipschitz floors j=2..5 + direct Master j<=16 "
                   "strict entries 0,1", "floors[" +
                   " ".join("j%d:%.4f" % (j, floors[j]) for j in (2, 3, 4, 5)) +
                   "] worst_delta=%.3e" % worst_delta, ok))
    return ok, floors

def gpoly(avals):
    c = [1.0]
    for a in avals:
        c = mult_root(c, a)
    return c

def word_info(word):
    """a-values along the scan, |hatf| = (-1)^B 4^B coeff_0(g_B)."""
    B = len(word)
    av = [a_of(u) for u in scan_states(word)]
    c0 = gpoly(av)[0]
    habs = ((-1) ** B) * (4 ** B) * c0
    return av, habs

def emu_pair(p, q):
    n = min(len(p), len(q)); s = 0.0
    for i in range(n):
        s += (1.0 if i == 0 else 0.5) * p[i] * q[i]
    return s

def gate_r4(report, tamper=None):
    """P10: R4 tree-decomposition identity A_k = (-1)^B 4^B sum_pi
    E_mu[g^pi A^pi] vs brute, every k, B in {4,5,6} (odd B=5 included so
    the 'r4-signflip' tamper -- dropping the (-1)^B factor -- is
    observable: that drop is a numerical no-op at the even B in {4,6}
    the claim is pinned at, since (-1)^even=1); prefix-cone scan, B<=6."""
    drop_sign = (tamper == "r4-signflip")
    Bs = (4, 5, 6)
    worst_recon = 0.0; min_Ak = float("inf")
    for B in Bs:
        words = dense_words(B)
        infos = {w: word_info(w) for w in words}
        for k in range(1, B + 1):
            brute = 0.0
            for w in words:
                av, habs = infos[w]
                brute += habs * (av[k - 1] - 0.5)
            groups = {}
            for w in words:
                groups.setdefault(w[:k - 1], []).append(w)
            recon = 0.0
            for pref, ws in groups.items():
                av0 = infos[ws[0]][0]
                gpi = gpoly(av0[:k - 1])
                Api = None
                for w in ws:
                    av = infos[w][0]
                    suff = gpoly(av[k - 1:])
                    contrib = [(av[k - 1] - 0.5) * x for x in suff]
                    Api = contrib if Api is None else [x + y for x, y in zip(Api, contrib)]
                e1 = emu_pair(gpi, Api)
                recon += (4 ** B) * e1 if drop_sign else ((-1) ** B) * (4 ** B) * e1
            worst_recon = max(worst_recon, abs(recon - brute))
            min_Ak = min(min_Ak, brute)
    cone_min = float("inf"); n_pref = 0
    for B in (4, 6, 8):
        for w in dense_words(B):
            av = [a_of(u) for u in scan_states(w)]
            g = [1.0]
            for m in range(B + 1):
                if m >= 1:
                    g = mult_root(g, av[m - 1])
                b = flip(g); n1 = sum(abs(x) for x in b)
                if n1 > 0:
                    cone_min = min(cone_min, min(b) / n1)
                    n_pref += 1
    ok = (worst_recon < 1e-9) and (min_Ak > 0) and (cone_min >= -1e-9)
    report.append(("P10 R4 exact identity (B in %s), A_k recon vs brute "
                   "max dev; prefix-cone scan (B<=8, %d prefixes) min b/||b||"
                   % (Bs, n_pref),
                   "dev=%.2e min_Ak=%.2f cone_min=%+.3e"
                   % (worst_recon, min_Ak, cone_min), ok))
    return ok

def per_prefix_terms(K, B, infos, words, W):
    """Return (E_w[prod_K], [T_pi per prefix]); T_pi = (-1)^B
    E_mu[g^pi_{k1-1} G^S(t_pi)] (decorated subtree charge)."""
    k1 = K[0]
    brute = 0.0
    for w in words:
        av = infos[w][0]
        pr = 1.0
        for kk in K:
            pr *= (av[kk - 1] - 0.5)
        brute += infos[w][1] * pr
    groups = {}
    for w in words:
        groups.setdefault(w[:k1 - 1], []).append(w)
    terms = []
    for pref, ws in groups.items():
        av0 = infos[ws[0]][0]
        gpi = gpoly(av0[:k1 - 1])
        GS = None
        for w in ws:
            av = infos[w][0]
            suff = gpoly(av[k1 - 1:])
            dec = 1.0
            for kk in K:
                dec *= (av[kk - 1] - 0.5)
            contrib = [dec * x for x in suff]
            GS = contrib if GS is None else [x + y for x, y in zip(GS, contrib)]
        terms.append(((-1) ** B) * emu_pair(gpi, GS))
    return brute / W, terms

def gate_tpi(report):
    """P11: general-K decorated-charge census -- reduction identity
    E_w[prod_K] == (4^B/W) sum_pi T_pi and ALL T_pi > 0, every K, every
    prefix, B in {6,8}. B in {6,8} together cost well under 1s, so B=8 runs by default."""
    worst_id = 0.0; neg_K = 0; total_K = 0; min_term_norm = float("inf")
    for B in (6, 8):
        words = dense_words(B)
        infos = {w: word_info(w) for w in words}
        W = sum(infos[w][1] for w in words)
        for r in range(1, B + 1):
            for K in combinations(range(1, B + 1), r):
                total_K += 1
                Ew, terms = per_prefix_terms(K, B, infos, words, W)
                recon = (4 ** B) / W * sum(terms)
                worst_id = max(worst_id, abs(recon - Ew))
                tn = sum(abs(x) for x in terms)
                if tn > 0:
                    min_term_norm = min(min_term_norm, min(terms) / tn)
                if any(t < -1e-9 for t in terms):
                    neg_K += 1
    # anchored case: b_0(G^S(0)) normalized mean positivity for every
    # decoration pattern S at B = 8 (the k_1 = 1 sub-case of the law)
    def dec_vec(S, j, u):
        if j == 0:
            return [1.0]
        acc = None
        lev = 9 - j          # levels count 1..8 from the top at u=0 root
        for d in (-1.0, 1.0):
            v = (d + u) / 3.0; av = a_of(abs(v))
            sub = dec_vec(S, j - 1, v)
            c = mult_root(sub, av)
            if lev in S:
                dr = av - 0.5
                c = [dr * x for x in c]
            acc = c if acc is None else [x + y for x, y in zip(acc, c)]
        return acc
    anch_min = float("inf")
    for r in range(1, 9):
        for S in combinations(range(1, 9), r):
            v = dec_vec(set(S), 8, 0.0)
            b = flip(v)
            n1 = sum(abs(x) for x in b)
            anch_min = min(anch_min, b[0] / n1)
    ok = (worst_id < 1e-9) and (neg_K == 0) and (anch_min >= 0.15)
    report.append(("P11 TPI general-K decorated-charge census (B in (6,8), "
                   "all K & prefixes); anchored b0(G^S(0)) floor 0.15",
                   "id_dev=%.2e neg_K=%d/%d min_term/||terms||=%+.3e "
                   "anch_min=%.4f"
                   % (worst_id, neg_K, total_K, min_term_norm, anch_min), ok))
    return ok, min_term_norm

# ---------------------------------------------------------------- main

def gate_share(report, Glev, jmax):
    """P12: the child-share floor the Master step consumes (H-S):
    G_j(t_in) >= 1.20 * G_{j-1}(r) entrywise on shared indices, for the
    sibling parent t_in = 1/4 - eps/3 and its minus-child r = 1/4 + eps/9,
    every level 6 <= j <= jmax; per-level minima printed."""
    floor = float("inf"); arg = None
    for j in range(6, jmax + 1):
        for k in range(1, 200):
            eps = 0.25 * k / 200
            tin = 0.25 - eps / 3
            r = 0.25 + eps / 9
            gj = flip(bary_gd(tin, Glev[j]))
            gr = flip(bary_gd(r, Glev[j - 1]))
            for i in range(len(gr)):
                if gr[i] > 1e-13:
                    q = gj[i] / gr[i]
                    if q < floor:
                        floor = q; arg = (j, eps, i)
    ok = floor >= 1.20
    report.append(("P12 SHARE child-share floor G_j(t_in)>=1.20*G_{j-1}(r) "
                   "(6<=j<=%d)" % jmax, "min=%.4f @(j=%d,eps=%.3f,i=%d)"
                   % (floor, arg[0], arg[1], arg[2]), ok))
    return ok, floor

# --------------------------------------------- P15: certificate binding

def gate_cert_binding(report, tamper=None):
    """P15 CERT-BIND (audit #914 SHOULD item, now a permanent gate):
    the shipped certificate JSON must be bound to the exact source
    note + verifier bytes it certifies. Loads the on-disk JSON and
    attests commit/source_sha256/script_sha256 against the current
    files, and requires command/deep/jmax/horizon to be present --
    exactly the fields the audit found missing (the old cert carried
    none of them and was never re-loaded by the verifier). After
    --emit-cert regenerates the file, a plain rerun must show this
    gate PASS; any later edit to the note or this script without
    re-emitting will correctly FAIL it. Tamper 'cert-unbound' strips
    the metadata (the pre-repair shape) to confirm this is caught."""
    required = {"commit", "source_sha256", "script_sha256", "command",
                "deep", "jmax", "horizon"}
    try:
        with open(CERT_PATH, encoding="utf-8") as f:
            cert = json.load(f)
    except (OSError, ValueError):
        cert = {}
    if tamper == "cert-unbound":
        cert = {k: v for k, v in cert.items() if k not in required}
    missing = required - set(cert)
    hashes_ok = (
        not missing
        and cert.get("commit") == COMMIT
        and cert.get("source_sha256") == file_sha256(NOTE_PATH)
        and cert.get("script_sha256") == file_sha256(__file__)
    )
    ok = hashes_ok and not missing
    report.append((
        "P15 CERT-BIND certificate JSON bound to source/script bytes + "
        "commit/command/deep/jmax/horizon metadata",
        "missing=%s hashes_ok=%s" % (sorted(missing), hashes_ok), ok))
    return ok

TAMPERS = ["atom-endpoint", "a-parity-flip", "kernel-flip", "law-parity",
           "dp-noins", "key-noshare", "r4-signflip", "env-tightcap",
           "coupling-off", "ident-universal", "p7-domain", "p7-cap",
           "cert-unbound"]

def run(tamper=None, deep=False):
    report = []
    oks = []
    oks.append(gate_def(report))
    oks.append(gate_kernel(report, flip_tamper=(tamper == "kernel-flip")))
    ok3, margins = gate_law(report, parity_tamper=(tamper == "law-parity"))
    oks.append(ok3)
    ok4, leak = gate_leak(report)
    oks.append(ok4)
    oks.append(gate_c6_parity(report, tamper=tamper))
    oks.append(gate_dp(report, noins_tamper=(tamper == "dp-noins")))
    oks.append(gate_atom(report, tamper=tamper))
    oks.append(gate_A_purity(report, tamper=tamper))

    oks.append(gate_dg(report))
    jmax_gd = 48 if deep else 16
    Glev, Dlev = build_gd_cascade(jmax_gd)
    oks.append(gate_l4(report, Glev, Dlev, jmax=12))
    ok7, env_sups = gate_env(report, Glev, tamper=tamper, jmax=jmax_gd)
    oks.append(ok7)
    ok14, env_sups_broad = gate_env_broad(report, Glev, tamper=tamper,
                                           jmax=jmax_gd)
    oks.append(ok14)
    ok8, key_margin = gate_key(report, tamper=tamper)
    oks.append(ok8)
    ok9, base_floors = gate_base(report, Glev)
    oks.append(ok9)
    ok12, share_floor = gate_share(report, Glev, jmax=jmax_gd)
    oks.append(ok12)
    oks.append(gate_r4(report, tamper=tamper))
    ok11, tpi_min = gate_tpi(report)
    oks.append(ok11)
    oks.append(gate_cert_binding(report, tamper=tamper))

    allok = all(oks)
    for name, val, ok in report:
        print("  [%s] %s : %s" % ("PASS" if ok else "FAIL", name, val))
    n = len(report)
    npass = sum(1 for _, _, ok in report if ok)
    print("RESULT: %s (%d/%d)" % ("PASS" if allok else "FAIL", npass, n))
    extra = {"share_floor": share_floor,
             "envelope_sups": env_sups,
             "envelope_sups_broad": env_sups_broad,
             "key_endpoint_margin": key_margin,
             "base_case_floors": {str(j): v for j, v in base_floors.items()},
             "tpi_census_min": tpi_min,
             "jmax": jmax_gd,
             "deep": deep}
    return allok, margins, leak, extra

if __name__ == "__main__":
    if "--tamper-selftest" in sys.argv:
        caught = 0
        for tm in TAMPERS:
            print("--- tamper:", tm)
            allok, _, _, _ = run(tamper=tm)
            if not allok:
                caught += 1
        print("TAMPER SELFTEST: %d/%d caught" % (caught, len(TAMPERS)))
    elif "--emit-cert" in sys.argv:
        deep_flag = "--deep" in sys.argv
        allok, margins, leak, extra = run(deep=deep_flag)
        command = "python3 " + " ".join(
            [os.path.basename(__file__)] + sys.argv[1:])
        jmax_used = extra["jmax"]
        cert = {"claims": "dense-shell class-charge computational core "
                          "+ proof-layer gates",
                "law_margins": margins,
                "leak_table_B10": {str(k): v for k, v in leak.items()},
                "envelope_sups": extra["envelope_sups"],
                "envelope_sups_broad": extra["envelope_sups_broad"],
                "key_endpoint_margin": extra["key_endpoint_margin"],
                "base_case_floors": extra["base_case_floors"],
                "tpi_census_min": extra["tpi_census_min"],
                "share_floor": extra["share_floor"],
                "pass": bool(allok),
                "commit": COMMIT,
                "source_sha256": file_sha256(NOTE_PATH),
                "script_sha256": file_sha256(__file__),
                "command": command,
                "deep": deep_flag,
                "jmax": jmax_used,
                "horizon": ("coupled q=j-1 in [5,%d]; broad j in [2,%d]"
                            % (min(jmax_used, 47), min(jmax_used, 48)))}
        os.makedirs(CERT_DIR, exist_ok=True)
        with open(CERT_PATH, "w") as f:
            json.dump(cert, f, indent=1, sort_keys=True)
        print("cert written:", CERT_PATH)
    elif "--deep" in sys.argv:
        run(deep=True)
    else:
        run()
