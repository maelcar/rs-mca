#!/usr/bin/env python3
"""Verifier: the transfer certificate for product-profile bands.

Claims checked (see experimental/notes/thresholds/product_profile_transfer_certificate.md):

  C1 (IFS cocycle, PROVED)   scanning balanced digits d_0.. upward with
                             state u <- (d + u)/3 and factor 2cos(2 pi u),
                             prod_{i<B} 2cos(theta_i(w)) equals the scan
                             product -- the dense-band indicator transform
                             is an iterated-function-system cocycle.
  C2 (carry DP, PROVED)      the dense-band class function h_v(sigma) is
                             computed EXACTLY by a digit DP over sigma's
                             balanced word with registers (carry in
                             {-1,0,1}, level count, IFS tail u) and
                             terminal weights wtil(count); every final
                             carry is accepted (balanced uniqueness mod
                             3^B).  The carry step (v = e - g + ci,
                             d = ((v+1) mod 3) - 1, co = (v-d)/3) is
                             closed on {-1,0,1}.
  C3 (spectral evaluation)   the adjoint function-valued DP on K Chebyshev
                             nodes evaluates h_v(sigma) in O(B^2 K^2) work
                             with GEOMETRIC K-convergence (pins at B=8:
                             worst err 7.0e-5 / 6.1e-10 / <2e-14 at
                             K = 8/12/16) -- COMPUTED convergence, rigor
                             bound open.
  C4 (generality, PROVED)    for ANY symmetric product profile
                             (lambda_j(1) = lambda_j(-1)) the band
                             indicator transform factors with affine
                             factors a_j + b_j 2cos(theta_j(w)) -- same
                             machinery; verified against brute indicator
                             transforms on random profiles.
  C5 (positivity pin)        hatf > 0 on the ENTIRE dense shell at
                             B in {6,8} (min hatf/M = 0.0177 / 0.0045) --
                             COMPUTED; proof open.

stdlib only, deterministic; floats under exact Parseval + Lemma-N guards.

Usage:
  python3 verify_product_profile_transfer.py
  python3 verify_product_profile_transfer.py --tamper-selftest
  python3 verify_product_profile_transfer.py --emit-certificate PATH
"""
import json
import sys
from cmath import exp as cexp
from collections import defaultdict
from itertools import combinations
from math import comb, cos, pi, sin

FAILED = []
PASSED = [0]


def check(name, ok):
    if ok:
        PASSED[0] += 1
    else:
        FAILED.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")


TAMPER = {"scan_state": False, "carry_step": False, "final_carry": False,
          "cheb_pin": False, "profile_factor": False}


def s3(y, B):
    y %= 3 ** B
    s = 0
    for _ in range(B):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        s += d != 0
    return s


def wtil(B, s):
    if s < 0 or s > B:
        return 0
    return comb(B - s, (B - s) // 2) if s % 2 == B % 2 else 0


def factors_poly(angles):
    poly = [1.0]
    for th in angles:
        t = 2 * cos(th)
        new = [0.0] * (len(poly) + 2)
        for i, a in enumerate(poly):
            new[i] += a
            new[i + 1] += a * t
            new[i + 2] += a
        poly = new
    return poly


def hatf_scan(B):
    c = 3 ** B
    return [factors_poly([2 * pi * ((j * 3 ** i) % c) / c
                          for i in range(B)])[B] for j in range(c)]


def digits(x, B):
    y = x % 3 ** B
    out = []
    for _ in range(B):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        out.append(d)
    return out


def v_c1(cert):
    import random
    random.seed(1)
    worst = 0.0
    for B in (6, 8):
        c = 3 ** B
        for _ in range(400):
            w = random.randrange(1, c)
            direct = 1.0
            for i in range(B):
                direct *= 2 * cos(2 * pi * ((w * 3 ** i) % c) / c)
            u = 0.0
            scan = 1.0
            div = 3 if not TAMPER["scan_state"] else 2
            for d in digits(w, B):
                u = (d + u) / div
                scan *= 2 * cos(2 * pi * u)
            worst = max(worst, abs(direct - scan))
    check(f"C1: IFS cocycle == direct product, 800 random w, B in {{6,8}} (worst {worst:.1e})",
          worst <= 1e-11)
    if cert is not None:
        cert["c1_worst"] = f"{worst:.2e}"


def carry_step(e, g, ci):
    v = e - g + ci
    d = ((v + 1) % 3) - 1
    if TAMPER["carry_step"]:
        d = ((v + 2) % 3) - 1
    return d, (v - d) // 3


def dp_exact(B, sig):
    c = 3 ** B
    gd = digits(sig, B)
    states = {(0, 0.0, 0): 1.0}
    for j in range(B):
        new = defaultdict(float)
        for (carry, u, cnt), amp in states.items():
            for e in (-1, 0, 1):
                d, co = carry_step(e, gd[j], carry)
                u2 = (d + u) / 3
                new[(co, u2, cnt + (e != 0))] += amp * 2 * cos(2 * pi * u2)
        states = new
    tot = 0.0
    for (carry, u, cnt), amp in states.items():
        if TAMPER["final_carry"] and carry != 0:
            continue
        tot += wtil(B, cnt) * amp
    return tot / c


def v_c2(cert):
    ok_carry = all(carry_step(e, g, ci)[0] in (-1, 0, 1)
                   and carry_step(e, g, ci)[1] in (-1, 0, 1)
                   and e - g + ci == carry_step(e, g, ci)[0]
                   + 3 * carry_step(e, g, ci)[1]
                   for e in (-1, 0, 1) for g in (-1, 0, 1)
                   for ci in (-1, 0, 1))
    check("C2: carry step closed on {-1,0,1}^3 with v == d + 3co (27 cases, exact)",
          ok_carry)
    worst = 0.0
    n = 0
    for B, vv in ((6, (0, 1, 1, 0, 1, 1)), (6, (1, 1, 1, 1, 1, 1)),
                  (8, (0, 1, 1, 0, 1, 1, 0, 1))):
        c = 3 ** B
        P = [3 ** i for i in range(B)]
        hf = hatf_scan(B)
        Ab = [xi for xi in range(c) if s3(xi, B) == B]
        exptab = [cexp(-2j * pi * t / c) for t in range(c)]
        U = [i for i in range(B) if vv[i]]
        s = sum(vv)
        for bits in range(min(2 ** s, 32)):
            sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                      for t in range(s)) % c
            brute = sum(hf[xi] * exptab[(xi * sig) % c] for xi in Ab).real / c
            worst = max(worst, abs(brute - dp_exact(B, sig)))
            n += 1
    check(f"C2: carry DP == brute dense-band class values ({n} signatures, B in {{6,8}}; worst {worst:.1e})",
          worst <= 1e-11)
    if cert is not None:
        cert["c2_worst"] = f"{worst:.2e}"


def cheb_nodes(K):
    return [0.5 * cos(pi * (2 * i + 1) / (2 * K)) for i in range(K)]


def bary_w(K):
    return [(-1) ** i * sin(pi * (2 * i + 1) / (2 * K)) for i in range(K)]


def interp(nodes, w, vals, x):
    num = den = 0.0
    for xi, wi, vi in zip(nodes, w, vals):
        dx = x - xi
        if abs(dx) < 1e-14:
            return vi
        t = wi / dx
        num += t * vi
        den += t
    return num / den


def dp_cheb(B, sig, K):
    c = 3 ** B
    gd = digits(sig, B)
    nodes = cheb_nodes(K)
    w = bary_w(K)
    F = {}
    for carry in (-1, 0, 1):
        for cnt in range(B + 1):
            F[(carry, cnt)] = [float(wtil(B, cnt))] * K
    for j in range(B - 1, -1, -1):
        Fn = {}
        for ci in (-1, 0, 1):
            for cnt in range(B + 1):
                vals = []
                for u in nodes:
                    acc = 0.0
                    for e in (-1, 0, 1):
                        cnt2 = cnt + (e != 0)
                        if cnt2 > B:
                            continue
                        d, co = carry_step(e, gd[j], ci)
                        u2 = (d + u) / 3
                        acc += 2 * cos(2 * pi * u2) * interp(
                            nodes, w, F[(co, cnt2)], u2)
                    vals.append(acc)
                Fn[(ci, cnt)] = vals
        F = Fn
    return interp(nodes, w, F[(0, 0)], 0.0) / c


def v_c3(cert):
    B = 8
    c = 3 ** B
    P = [3 ** i for i in range(B)]
    hf = hatf_scan(B)
    Ab = [xi for xi in range(c) if s3(xi, B) == B]
    exptab = [cexp(-2j * pi * t / c) for t in range(c)]
    vv = (0, 1, 1, 0, 1, 1, 0, 1)
    U = [i for i in range(B) if vv[i]]
    sigs = [sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                for t in range(sum(vv))) % c for bits in range(16)]
    ref = {sig: sum(hf[xi] * exptab[(xi * sig) % c] for xi in Ab).real / c
           for sig in sigs}
    pins = {8: 7.0e-5, 12: 6.2e-10, 16: 2e-14}
    if TAMPER["cheb_pin"]:
        pins = {8: 1e-7, 12: 6.2e-10, 16: 2e-14}
    ok = True
    got = {}
    for K, bound in pins.items():
        try:
            worst = max(abs(dp_cheb(B, sig, K) - ref[sig]) for sig in sigs)
        except Exception:
            worst = float("inf")
        got[K] = worst
        if worst > bound * 1.5:
            ok = False
    check(f"C3: Chebyshev DP geometric convergence at B=8 -- worst {got[8]:.1e}/{got[12]:.1e}/{got[16]:.1e} at K=8/12/16 (bounds 7e-5/6.2e-10/2e-14)",
          ok and got[16] < got[12] < got[8])
    if cert is not None:
        cert["c3_convergence"] = {str(K): f"{v:.2e}" for K, v in got.items()}


def v_c4(cert):
    import random
    random.seed(9)
    worst = 0.0
    B = 6
    c = 3 ** B
    for _ in range(5):
        prof = [[random.randrange(0, 3) for _ in range(2)] for _ in range(B)]
        # lambda_j(0) = prof[j][0]; lambda_j(+-1) = prof[j][1] (symmetric)
        for _ in range(6):
            w = random.randrange(1, c)
            brute = 0j
            for xi in range(c):
                dd = digits(xi, B)
                pr = 1
                for j in range(B):
                    pr *= prof[j][0] if dd[j] == 0 else prof[j][1]
                if pr:
                    brute += pr * cexp(2j * pi * xi * w / c)
            fact = 1.0
            for j in range(B):
                b2 = prof[j][1] * (2 if not TAMPER["profile_factor"] else 1)
                fact *= prof[j][0] + b2 * cos(2 * pi * ((w * 3 ** j) % c) / c)
            worst = max(worst, abs(brute - fact))
    check(f"C4: symmetric product-profile indicator transform factors (random profiles, worst {worst:.1e})",
          worst <= 1e-7)
    # position-varying profile through the SCAN: factors enter REVERSED
    # (scan step j produces profile position B-1-j)
    prof = [[1, 1], [0, 1], [2, 1], [1, 2], [1, 0], [2, 2]]
    worst_rev = 0.0
    for w in (5, 100, 400):
        direct = 1.0
        for jj in range(B):
            direct *= prof[jj][0] + 2 * prof[jj][1] * cos(
                2 * pi * ((w * 3 ** jj) % c) / c)
        u = 0.0
        scan = 1.0
        for step, d in enumerate(digits(w, B)):
            u = (d + u) / 3
            pj = B - 1 - step if not TAMPER["profile_factor"] else step
            scan *= prof[pj][0] + 2 * prof[pj][1] * cos(2 * pi * u)
        worst_rev = max(worst_rev, abs(direct - scan))
    check(f"C4: position-varying affine factors enter the scan REVERSED (worst {worst_rev:.1e})",
          worst_rev <= 1e-9)
    if cert is not None:
        cert["c4_worst"] = f"{worst:.2e}"


def v_c5_and_guards(cert):
    for B in (6, 8):
        c = 3 ** B
        hf = hatf_scan(B)
        m2 = sum(comb(B, s) * 2 ** s * wtil(B, s) ** 2 for s in range(B + 1))
        check(f"guard: Parseval (B={B})",
              abs(sum(x * x for x in hf) - c * m2) <= 1e-6 * c * m2)
        shell = [xi for xi in range(c) if s3(xi, B) == B]
        mn = min(hf[xi] for xi in shell) / comb(2 * B, B)
        pin = {6: 0.0177, 8: 0.0045}[B]
        check(f"C5: hatf > 0 on the ENTIRE dense shell (B={B}; min hatf/M {mn:.4f} == {pin})",
              mn > 0 and abs(mn - pin) <= 5e-4)
    B = 6
    c = 3 ** B
    P = [3 ** i for i in range(B)]
    T = P + [c - p for p in P]
    N = [0] * c
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    check("guard: Lemma N exact (B=6 brute)",
          all(N[y] == wtil(B, s3(y, B)) for y in range(c)))


def run_all(cert=None):
    v_c5_and_guards(cert)
    v_c1(cert)
    v_c2(cert)
    v_c3(cert)
    v_c4(cert)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} "
          f"({PASSED[0]}/{PASSED[0] + len(FAILED)})")
    return not FAILED


def tamper_selftest():
    import subprocess
    caught = 0
    keys = list(TAMPER)
    for key in keys:
        rr = subprocess.run([sys.executable, __file__, f"--tamper={key}"],
                            capture_output=True, text=True)
        ok = "RESULT: FAIL" in rr.stdout or rr.returncode != 0
        caught += ok
        print(f"tamper {key}: {'caught' if ok else 'MISSED'}")
    print(f"tamper-selftest: caught {caught}/{len(keys)}")
    return caught == len(keys)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--tamper-selftest":
        sys.exit(0 if tamper_selftest() else 1)
    for a in args:
        if a.startswith("--tamper="):
            TAMPER[a.split("=", 1)[1]] = True
    cert = None
    path = None
    if args and args[0] == "--emit-certificate":
        path = args[1]
        cert = {"packet": "product-profile-transfer", "chart": "base-3",
                "claims": ["C1", "C2", "C3", "C4", "C5"]}
    ok = run_all(cert)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
