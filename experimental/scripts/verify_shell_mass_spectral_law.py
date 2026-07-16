#!/usr/bin/env python3
"""Verifier: the shell-mass spectral law and the dense-shell failing band.

Claims checked (see experimental/notes/thresholds/shell_mass_spectral_law.md):

  I   (identity)   the digit-shell generating identity
                      sum_xi x^{s3(xi)} e_c(xi z) = prod_i (1 + 2x cos(theta_i(z)))
                   (balanced-digit independence, Lemma 0), and its
                   consequence: exact shell masses
                      sum_{s3(xi)=t} hatf(xi)^2
                        = [x^t] sum_{y,y'} N(y) N(y') prod_i (1 + 2x cos(theta_i(y-y'))).
  R   (the table)  exact shell failure ratios R_t = shell mass / (c M^2/L)
                   at B in {6,8} inline (B in {10,12} behind --deep):
                   the profile is BIMODAL, the middle shells are
                   subordinate at every computed B, and the DENSE shell
                   s3 = B crosses R = 1 at exactly B = 12 (R = 1.0457):
                   the first SINGLE shell to fail alone (B=11 stays below);
                   proper failing shell-unions exist from B = 6.
  D   (structure)  the dense shell {s3(xi) = B} IS the full-signature set
                   (the level-B class syndrome cube, 2^B points); it
                   contains the resonant point j* = (c-1)/2 (#776); it is
                   NOT hierarchy-measurable at any bounded depth; its
                   band transform has the closed form
                      sum_{s3(xi)=B} e_c(xi w) = prod_i 2 cos(theta_i(w));
                   and w-weighted digit sums of PRODUCT profiles factor
                   digit-wise (the tractability seed beyond bounded depth).

stdlib only, deterministic; floats under exact Parseval + Lemma-N guards.

Usage:
  python3 verify_shell_mass_spectral_law.py [--deep]
  python3 verify_shell_mass_spectral_law.py --tamper-selftest
  python3 verify_shell_mass_spectral_law.py --emit-certificate PATH [--deep]
"""
import json
import sys
from cmath import exp as cexp
from itertools import combinations
from math import comb, cos, pi

FAILED = []
PASSED = [0]


def check(name, ok):
    if ok:
        PASSED[0] += 1
    else:
        FAILED.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")


TAMPER = {"gen_identity": False, "r_pin": False, "shell_set": False,
          "depth_lemma": False, "factorization": False}


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


def shell_R(B, hf=None):
    c = 3 ** B
    M = comb(2 * B, B)
    L = (c + 1) // 2
    if hf is None:
        hf = hatf_scan(B)
    mass = [0.0] * (B + 1)
    for xi in range(1, c):
        mass[s3(xi, B)] += hf[xi] ** 2
    thr = c * M * M / L
    return [m / thr for m in mass]


def digit_gen_poly(z, B, x_deg=None):
    """prod_i (1 + 2x cos(theta_i(z))) as x-coefficient list."""
    c = 3 ** B
    poly = [1.0]
    for i in range(B):
        t = 2 * cos(2 * pi * ((z * 3 ** i) % c) / c)
        if TAMPER["gen_identity"]:
            t = 2 * cos(2 * pi * ((z * 3 ** i) % c) / c) ** 2
        new = [0.0] * (len(poly) + 1)
        for d, a in enumerate(poly):
            new[d] += a
            new[d + 1] += a * t
        poly = new
    return poly


def v_identity(cert):
    import random
    random.seed(20260716)
    # primitive form: sum_xi x^{s3} e_c(xi z) == prod_i (1 + 2x cos theta_i(z))
    worst = 0.0
    for B in (6, 8):
        c = 3 ** B
        for _ in range(6):
            z = random.randrange(1, c)
            lhs = [0j] * (B + 1)
            for xi in range(c):
                lhs[s3(xi, B)] += cexp(2j * pi * xi * z / c)
            rhs = digit_gen_poly(z, B)
            worst = max(worst, max(abs(lhs[t] - rhs[t])
                                   for t in range(B + 1)))
    check(f"I: digit-shell generating identity, random z, B in {{6,8}} (worst {worst:.1e})",
          worst <= 1e-6)
    # shell-mass consequence at B = 6 via the correlation-product route
    B = 6
    c = 3 ** B
    hf = hatf_scan(B)
    N = [wtil(B, s3(y, B)) for y in range(c)]
    mass = [0.0] * (B + 1)
    for xi in range(c):
        mass[s3(xi, B)] += hf[xi] ** 2
    rhs = [0.0] * (B + 1)
    supp = [y for y in range(c) if N[y]]
    for y in supp:
        for yp in supp:
            poly = digit_gen_poly((y - yp) % c, B)
            for t in range(B + 1):
                rhs[t] += N[y] * N[yp] * poly[t]
    worst2 = max(abs(mass[t] - rhs[t]) / max(mass[t], 1.0)
                 for t in range(B + 1))
    check(f"I: exact shell masses == correlation-product coefficients (B=6, worst rel {worst2:.1e})",
          worst2 <= 1e-9)
    if cert is not None:
        cert["identity_worst"] = f"{worst:.2e}"


def v_table(cert, deep):
    pins = {6: {"total": 1.0315, "mid": 0.0271, "dense2": 0.7648},
            8: {"total": 1.4301, "mid": 0.0763, "dense2": 0.9581}}
    got = {}
    for B in (6, 8):
        R = shell_R(B)
        got[B] = R
        mid = sum(R[3:B - 1])
        d2 = R[B - 1] + R[B]
        p = pins[B]
        tol = 5e-4 if not TAMPER["r_pin"] else 1e-6
        exp_mid = p["mid"] if not TAMPER["r_pin"] else p["mid"] * 2
        check(f"R: B={B} pins -- total {sum(R):.4f}=={p['total']}, mid {mid:.4f}=={exp_mid if TAMPER['r_pin'] else p['mid']}, dense2 {d2:.4f}=={p['dense2']}",
              abs(sum(R) - p["total"]) <= tol and abs(mid - exp_mid) <= tol
              and abs(d2 - p["dense2"]) <= tol)
    check("R: middle subordinate & bimodal ordering at B in {6,8}: R_mid < R_sparse < R_dense2",
          all(sum(got[B][3:B - 1]) < got[B][1] + got[B][2]
              < got[B][B - 1] + got[B][B] for B in (6, 8)))
    u6 = got[6][1] + got[6][2] + got[6][5] + got[6][6]
    check(f"R: proper failing UNIONS exist from B=6 -- sparse+dense-pair {u6:.4f} == 1.0044 > 1",
          abs(u6 - 1.0044) <= 5e-4 and u6 > 1)
    if deep:
        for B, dense_pin, cross in ((10, 0.9100, False), (11, 0.9757, False),
                                    (12, 1.0457, True)):
            R = shell_R(B)
            got[B] = R
            check(f"R(--deep): B={B} dense-shell R_B {R[B]:.4f} == {dense_pin}; crosses 1: {R[B] > 1} (expect {cross})",
                  abs(R[B] - dense_pin) <= 5e-4 and (R[B] > 1) == cross)
        pair10 = got[10][9] + got[10][10]
        check(f"R(--deep): dense PAIR {{B-1,B}} self-suffices from B=10 ({pair10:.4f} == 1.1976 > 1)",
              abs(pair10 - 1.1976) <= 5e-4 and pair10 > 1)
    if cert is not None:
        cert["R_tables"] = {str(B): [round(x, 6) for x in R]
                            for B, R in got.items()}


def v_dense_structure(cert):
    B = 6
    c = 3 ** B
    P = [3 ** i for i in range(B)]
    # dense shell == full-signature set
    shell = {xi for xi in range(c) if s3(xi, B) == B}
    sigs = set()
    for bits in range(2 ** B):
        sigs.add(sum((1 if not (bits >> t) & 1 else -1) * P[t]
                     for t in range(B)) % c)
    if TAMPER["shell_set"]:
        sigs.add(0)
    check(f"D: dense shell {{s3 = B}} == level-B signature set (|shell| {len(shell)} == 2^B == {2 ** B})",
          shell == sigs and len(shell) == 2 ** B)
    check("D: the resonant point j* = (c-1)/2 lies in the dense shell",
          s3((c - 1) // 2, B) == B)
    # not hierarchy-measurable at any bounded depth k < B
    ok = True
    for k in range(1, B):
        found = False
        for r in range(3 ** k):
            ins = outs = False
            for hi in range(3 ** (B - k)):
                xi = r + 3 ** k * hi
                if xi == 0:
                    continue
                if s3(xi, B) == B:
                    ins = True
                else:
                    outs = True
                if ins and outs:
                    found = True
                    break
            if found:
                break
        if not found:
            ok = False
    if TAMPER["depth_lemma"]:
        ok = not ok
    check("D: NOT hierarchy-measurable at any depth k < B (every depth has a split coset; B=6)",
          ok)
    # band-transform closed form: sum_{shell} e_c(xi w) == prod_i 2 cos(theta_i(w))
    import random
    random.seed(7)
    worst = 0.0
    for _ in range(8):
        w = random.randrange(1, c)
        lhs = sum(cexp(2j * pi * xi * w / c) for xi in shell)
        rhs = 1.0
        for i in range(B):
            rhs *= 2 * cos(2 * pi * ((w * 3 ** i) % c) / c)
        worst = max(worst, abs(lhs - rhs))
    check(f"D: dense-band transform == prod_i 2 cos(theta_i(w)) (8 random w, worst {worst:.1e})",
          worst <= 1e-9)
    # product-profile digit-sum factorization (exact integers)
    ok = True
    random.seed(11)
    for k in (2, 3, 4, 5):
        lam = [[random.randrange(0, 3) for _ in range(3)] for _ in range(k)]
        # LHS: sum over a in Z_3^k of prod_j lam_j(balanced digit) * x^{s3(a)}
        lhs = [0] * (k + 1)
        for a in range(3 ** k):
            aa, prod, t = a, 1, 0
            for j in range(k):
                d = aa % 3
                if d == 2:
                    d = -1
                aa = (aa - d) // 3
                prod *= lam[j][d]  # index -1 = last = digit -1
                t += d != 0
            lhs[t] += prod
        # RHS: prod_j (lam_j(0) + x (lam_j(1) + lam_j(-1)))
        rhs = [1]
        for j in range(k):
            z0, pl = lam[j][0], lam[j][1] + lam[j][-1]
            if TAMPER["factorization"]:
                pl = lam[j][1]
            new = [0] * (len(rhs) + 1)
            for d, aco in enumerate(rhs):
                new[d] += aco * z0
                new[d + 1] += aco * pl
            rhs = new
        rhs += [0] * (k + 1 - len(rhs))
        if lhs != rhs[:k + 1]:
            ok = False
    check("D: product-profile digit sums factor digit-wise (exact integers, k <= 5, random profiles)",
          ok)


def v_guards():
    B = 6
    c = 3 ** B
    hf = hatf_scan(B)
    m2 = sum(comb(B, s) * 2 ** s * wtil(B, s) ** 2 for s in range(B + 1))
    check("guard: Parseval sum hatf^2 == c * M2 (1e-6 rel)",
          abs(sum(x * x for x in hf) - c * m2) <= 1e-6 * c * m2)
    P = [3 ** i for i in range(B)]
    T = P + [c - p for p in P]
    N = [0] * c
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    check("guard: Lemma N exact (B=6 brute)",
          all(N[y] == wtil(B, s3(y, B)) for y in range(c)))


def run_all(cert=None, deep=False):
    v_guards()
    v_identity(cert)
    v_table(cert, deep)
    v_dense_structure(cert)
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
        ok = "RESULT: FAIL" in rr.stdout
        caught += ok
        print(f"tamper {key}: {'caught' if ok else 'MISSED'}")
    print(f"tamper-selftest: caught {caught}/{len(keys)}")
    return caught == len(keys)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--tamper-selftest":
        sys.exit(0 if tamper_selftest() else 1)
    deep = "--deep" in args
    for a in args:
        if a.startswith("--tamper="):
            TAMPER[a.split("=", 1)[1]] = True
    cert = None
    path = None
    if args and args[0] == "--emit-certificate":
        path = args[1]
        cert = {"packet": "shell-mass-spectral-law", "chart": "base-3",
                "claims": ["I", "R", "D"]}
    ok = run_all(cert, deep)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
