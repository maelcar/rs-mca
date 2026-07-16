#!/usr/bin/env python3
"""Verifier: the complete twisted-coset cube spectrum on the base-3 chart.

Claims checked (see experimental/notes/thresholds/twisted_coset_cube_spectrum.md):

  N   (counting)     N(y) = w_{s3(y)} [s3(y) == B mod 2], exact integers.
  A   (localization) cube coefficients vanish EXACTLY unless D is inside the
                     class's top-k block -- for every depth-k coset and, by
                     linearity, every hierarchy-measurable band.
  B   (product law)  on the coset {xi == r mod 3^k} the class-v cube function
                     is the character omega^{-r tau(eps_top)} times the class
                     constant G_{k,r}(s_low); its cube transform is the
                     rank-one product
                        chat_v(D) = G_{k,r}(s_low)
                                    * prod_{t in top} (-i sin(beta_t r)  if t in D
                                                       else cos(beta_t r)),
                        beta_t = 2 pi 3^{U_t-(B-k)} / 3^k,
                        G_{k,r}(l) = 3^{-k} sum_a e(-ar/3^k) wtil(s3(a)+l).
  C   (consequences) r=0 recovers subgroup flatness in one line; the k=1
                     nonflat spectrum is PURELY IMAGINARY (the cosine-blind
                     anatomy of the withdrawn extrapolation); per-class cube
                     energy equals |G(s_low)|^2; the #805 regression constants
                     are derived, not scanned.

Float scans sit under exact Parseval guards; the counting layer is exact
integer arithmetic.  stdlib only, deterministic.

Usage:
  python3 verify_twisted_coset_cube_spectrum.py
  python3 verify_twisted_coset_cube_spectrum.py --tamper-selftest
  python3 verify_twisted_coset_cube_spectrum.py --emit-certificate PATH
"""
import json
import sys
from cmath import exp as cexp
from collections import defaultdict
from itertools import combinations
from math import comb, cos, pi, sin, sqrt

FAILED = []
PASSED = [0]


def check(name, ok):
    if ok:
        PASSED[0] += 1
    else:
        FAILED.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")


# --------------------------------------------------------------- chart data

TAMPER = {"parity": False, "phase": False, "cosine_only": False,
          "beta": False, "digits": False, "energy": False}


def s3(y, ndig):
    """Nonzero canonical balanced-ternary digits of y mod 3^ndig."""
    y %= 3 ** ndig
    s = 0
    for _ in range(ndig):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        s += d != 0
    return s


def s3_tampered(y, ndig):
    y %= 3 ** ndig
    s = 0
    for _ in range(ndig):
        d = y % 3
        y = (y - (d if d < 2 else -1)) // 3 if d != 2 else (y + 1) // 3
        s += d == 1  # WRONG: counts only +1 digits
    return s


def wtil(B, s):
    """w_s = C(B-s,(B-s)/2) on the realized parity, else 0."""
    if s < 0 or s > B:
        return 0
    if TAMPER["parity"]:
        good = True
    else:
        good = (s % 2 == B % 2)
    return comb(B - s, (B - s) // 2) if good else 0


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


def brute_N(B):
    c = 3 ** B
    P = [3 ** i for i in range(B)]
    T = P + [c - p for p in P]
    N = [0] * c
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    return N


def classes(B):
    """Realized parity vectors (all v with |v| == B mod 2)."""
    return [v for v in
            (tuple((n >> i) & 1 for i in range(B)) for n in range(2 ** B))
            if sum(v) % 2 == B % 2]


def G_table(B, k, r):
    ck = 3 ** k
    dig = s3_tampered if TAMPER["digits"] else s3
    return [sum(cexp(-2j * pi * a * r / ck) * wtil(B, dig(a, k) + l)
                for a in range(ck)) / ck for l in range(B + 1)]


def model_coeff(B, k, r, U, dbits, Gk):
    """Theorem B product formula; 0 when D leaves the top block."""
    s = len(U)
    top = [t for t in range(s) if U[t] >= B - k]
    if any((dbits >> t) & 1 and t not in top for t in range(s)):
        return 0j
    x = Gk[s - len(top)]
    ck = 3 ** k
    sin_unit = 1.0 if TAMPER["phase"] else -1j
    for t in top:
        e = U[t] - (B - k) + (1 if TAMPER["beta"] else 0)
        beta = 2 * pi * (3 ** e) * r / ck
        x *= (sin_unit * sin(beta)) if (dbits >> t) & 1 else cos(beta)
    return x


def brute_cube(B, hf, Ab, cls, exptab):
    """{v: {dbits: coefficient}} by literal complex Fourier inversion."""
    c = 3 ** B
    P = [3 ** i for i in range(B)]
    hv = {}
    out = {}
    for v in cls:
        s = sum(v)
        if s < 2:
            continue
        U = [i for i in range(B) if v[i]]
        sigs = {}
        for bits in range(2 ** s):
            sigs[bits] = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                             for t in range(s)) % c
        for sig in sigs.values():
            if sig not in hv:
                z = sum(hf[xi] * exptab[(xi * sig) % c] for xi in Ab) / c
                hv[sig] = z.real if TAMPER["cosine_only"] else z
        cube = {bits: hv[sigs[bits]] for bits in sigs}
        out[v] = {dbits: sum(((-1) ** bin(bits & dbits).count("1")) * x
                             for bits, x in cube.items()) / 2 ** s
                  for dbits in range(2 ** s)}
    return out


def coset(B, k, r):
    c = 3 ** B
    return [(r + 3 ** k * m) % c for m in range(3 ** (B - k))]


# ------------------------------------------------------------------ checks

def vN(cert):
    for B in (4, 6, 8):
        N = brute_N(B)
        ok = all(N[y] == wtil(B, s3(y, B)) for y in range(3 ** B))
        check(f"N: N(y) == wtil(s3(y)) for ALL y in Z_3^{B} (exact, B={B})", ok)
    ok = all(sum(1 for a in range(3 ** k) if s3(a, k) == j) ==
             comb(k, j) * 2 ** j for k in range(1, 7) for j in range(k + 1))
    check("N: #{a in Z_3^k : s3(a)=j} == C(k,j) 2^j, k <= 6 (exact)", ok)
    if cert is not None:
        cert["N_exact_B"] = [4, 6, 8]


def vAB(cert):
    B = 6
    c = 3 ** B
    hf = hatf_scan(B)
    check("Parseval guard sum hatf^2 == c * sum C(B,s) 2^s wtil(s)^2 to 1e-6 rel (B=6)",
          abs(sum(x * x for x in hf) - c * closed_M2(B))
          <= 1e-6 * c * closed_M2(B))
    cls = classes(B)
    exptab = [cexp(-2j * pi * t / c) for t in range(c)]
    worst_loc, worst_prod, n_coeff = 0.0, 0.0, 0
    im_worst = 0.0
    energy_worst = 0.0
    nonflat_min = float("inf")
    for k in (1, 2, 3):
        for r in range(1, 3 ** k):
            Ab = coset(B, k, r)
            data = brute_cube(B, hf, Ab, cls, exptab)
            Gk = G_table(B, k, r)
            nonempty_max = 0.0
            for v, coeffs in data.items():
                s = sum(v)
                U = [i for i in range(B) if v[i]]
                top = [t for t in range(s) if U[t] >= B - k]
                cube_energy = sum(abs(x) ** 2 for x in coeffs.values())
                gval = abs(Gk[s - len(top)]) ** 2
                energy_worst = max(energy_worst,
                                   abs(cube_energy - gval * (2 if TAMPER["energy"] else 1)))
                for dbits, x in coeffs.items():
                    n_coeff += 1
                    if any((dbits >> t) & 1 and t not in top
                           for t in range(s)):
                        worst_loc = max(worst_loc, abs(x))
                    else:
                        worst_prod = max(
                            worst_prod,
                            abs(x - model_coeff(B, k, r, U, dbits, Gk)))
                    if dbits:
                        nonempty_max = max(nonempty_max, abs(x))
                    if k == 1 and dbits:
                        im_worst = max(im_worst, abs(x.real))
            nonflat_min = min(nonflat_min, nonempty_max)
    check(f"A: localization -- D outside the top block vanishes, ALL (k,r), B=6 ({n_coeff} coefficients, worst {worst_loc:.1e})",
          worst_loc <= 1e-12)
    check(f"C4: EVERY twisted coset is nonflat, all (k,r), B=6 (min of per-coset max nonempty {nonflat_min:.3f})",
          nonflat_min > 1e-10)
    check(f"B: product law matches brute on ALL coefficients, ALL (k,r), B=6 (worst {worst_prod:.1e})",
          worst_prod <= 1e-12)
    check(f"C: k=1 nonempty spectrum PURELY IMAGINARY, all r (worst |Re| {im_worst:.1e})",
          im_worst <= 1e-12)
    check(f"C: per-class cube energy == |G(s_low)|^2 (worst {energy_worst:.1e})",
          energy_worst <= 1e-9)
    if cert is not None:
        cert["B6_coefficients"] = n_coeff
        cert["localization_worst"] = f"{worst_loc:.2e}"
        cert["product_law_worst"] = f"{worst_prod:.2e}"
        cert["k1_pure_imag_worst_re"] = f"{im_worst:.2e}"


def closed_M2(B):
    # sum_y N(y)^2 = sum_s (#level-s signatures) w_s^2 = sum_s C(B,s)2^s w_s^2
    return sum(comb(B, s) * 2 ** s * wtil(B, s) ** 2 for s in range(B + 1))


def v_regressions(cert):
    B = 6
    # #805 pin 1: k=1, r=1 max nonempty magnitude sqrt(3), now DERIVED:
    Gk = G_table(B, 1, 1)
    derived = max(abs(Gk[s - 1] * sin(2 * pi / 3)) for s in (2, 4, 6))
    check("#805 pin: max nonempty magnitude at k=1,r=1 == sqrt(3) (derived)",
          abs(derived - sqrt(3)) <= 1e-12)
    # #805 pin 2: symmetric depth-two union, v=(0,0,0,0,1,1), D=both:
    tot = 0j
    for r in (1, 8):
        G2 = G_table(B, 2, r)
        tot += model_coeff(B, 2, r, [4, 5], 3, G2)
    literal = -1.336932620625273
    check("#805 pin: symmetric depth-two coefficient == -1.336932620625273... (derived)",
          abs(tot - literal) <= 1e-12)
    # closed form of the same pin:
    closed = -(2 / 9) * sin(2 * pi / 9) * sin(2 * pi / 3) * (
        comb(6, 3) + 2 * comb(4, 2) * (cos(4 * pi / 9) + cos(8 * pi / 9)))
    check("#805 pin: derived value == the published closed form",
          abs(tot - closed) <= 1e-12)
    # subgroup one-liner: r=0 makes every sine vanish
    ok = True
    for k in (1, 2, 3):
        G0 = G_table(B, k, 0)
        for U in ([4, 5], [0, 5], [2, 3, 4, 5]):
            for dbits in range(1, 2 ** len(U)):
                if abs(model_coeff(B, k, 0, U, dbits, G0)) > 1e-15:
                    ok = False
    check("C: r=0 product law is flat (subgroup flatness re-derived)", ok)
    # exact vanishing criterion: sin(beta_t r)=0 iff 3^{k-j} | r
    ok = True
    for k in (2, 3):
        ck = 3 ** k
        for r in range(1, ck):
            for j in range(k):
                zero = abs(sin(2 * pi * 3 ** j * r / ck)) <= 1e-12
                if zero != (r % 3 ** (k - j) == 0):
                    ok = False
    check("C: sin(beta r) == 0 iff 3^{k-j} | r (exact criterion)", ok)
    if cert is not None:
        cert["pin_k1_r1_max"] = round(derived, 15)
        cert["pin_symmetric_depth2"] = round(tot.real, 15)


def v_profiles(cert):
    """Linearity: random hierarchy-measurable unions obey the summed law."""
    import random
    random.seed(20260716)
    B = 6
    c = 3 ** B
    hf = hatf_scan(B)
    cls = classes(B)
    exptab = [cexp(-2j * pi * t / c) for t in range(c)]
    worst = 0.0
    for k in (2, 3):
        for _ in range(3):
            R = random.sample(range(3 ** k), random.randrange(2, 5))
            Ab = sorted(set().union(*[coset(B, k, r) for r in R]))
            data = brute_cube(B, hf, Ab, cls, exptab)
            Gs = {r: G_table(B, k, r) for r in R}
            for v, coeffs in data.items():
                U = [i for i in range(B) if v[i]]
                for dbits, x in coeffs.items():
                    m = sum(model_coeff(B, k, r, U, dbits, Gs[r]) for r in R)
                    worst = max(worst, abs(x - m))
    check(f"A+B: random depth-k unions obey the summed product law (worst {worst:.1e})",
          worst <= 1e-11)
    if cert is not None:
        cert["union_worst"] = f"{worst:.2e}"


def embed_low(u, m, B):
    """Canonical balanced lift of u mod 3^m into Z_3^B."""
    return u if 2 * u + 1 <= 3 ** m else 3 ** B + u - 3 ** m


def v_digit_block(cert):
    """Theorem A's load-bearing digit lemma, exact and exhaustive:
    s3(a 3^{B-k} + embed(u)) == s3(a) + s3(u), all (a,u), k in {1,2,3}."""
    ok = True
    for B in (6, 8):
        for k in (1, 2, 3):
            for a in range(3 ** k):
                for u in range(3 ** (B - k)):
                    if s3((a * 3 ** (B - k) + embed_low(u, B - k, B)) % 3 ** B,
                          B) != s3(a, k) + s3(u, B - k):
                        ok = False
    check("A: digit-block additivity s3(a 3^{B-k} + embed(u)) == s3(a)+s3(u), ALL (a,u), k in {1,2,3}, B in {6,8} (exact)",
          ok)


def v_coset_energy(cert):
    """Full-sigma Parseval through the digit split:
    sum_{xi in K_{k,r}} hatf(xi)^2 == c 3^k sum_l C(B-k,l) 2^l |G_{k,r}(l)|^2."""
    B = 6
    c = 3 ** B
    hf = hatf_scan(B)
    worst = 0.0
    for k in (1, 2, 3):
        for r in range(3 ** k):
            lhs = sum(hf[xi] ** 2 for xi in coset(B, k, r))
            Gk = G_table(B, k, r)
            rhs = c * 3 ** k * sum(comb(B - k, l) * 2 ** l * abs(Gk[l]) ** 2
                                   for l in range(B - k + 1))
            worst = max(worst, abs(lhs - rhs) / rhs if rhs else abs(lhs))
    check(f"C: coset energy == c 3^k sum C(B-k,l) 2^l |G(l)|^2, ALL (k,r) (worst rel {worst:.1e})",
          worst <= 1e-9)
    if cert is not None:
        cert["coset_energy_worst_rel"] = f"{worst:.2e}"


def v_B8_spot(cert):
    B = 8
    c = 3 ** B
    hf = hatf_scan(B)
    exptab = [cexp(-2j * pi * t / c) for t in range(c)]
    # spot classes: two twisted cosets, a handful of classes
    spot_classes = [tuple(int(i in U) for i in range(B))
                    for U in ([6, 7], [0, 7], [1, 3, 5, 7], [0, 1, 6, 7],
                              [2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7])]
    worst = 0.0
    for k, r in ((1, 1), (2, 5)):
        Ab = coset(B, k, r)
        data = brute_cube(B, hf, Ab, spot_classes, exptab)
        Gk = G_table(B, k, r)
        for v, coeffs in data.items():
            U = [i for i in range(B) if v[i]]
            for dbits, x in coeffs.items():
                worst = max(worst,
                            abs(x - model_coeff(B, k, r, U, dbits, Gk)))
    check(f"B: product law spot check at B=8 (k,r) in ((1,1),(2,5)) (worst {worst:.1e})",
          worst <= 1e-11)
    if cert is not None:
        cert["B8_spot_worst"] = f"{worst:.2e}"


def run_all(cert=None):
    vN(cert)
    v_digit_block(cert)
    vAB(cert)
    v_regressions(cert)
    v_profiles(cert)
    v_coset_energy(cert)
    v_B8_spot(cert)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} "
          f"({PASSED[0]}/{PASSED[0] + len(FAILED)})")
    return not FAILED


def tamper_selftest():
    import subprocess
    caught = 0
    keys = ["parity", "phase", "cosine_only", "beta", "digits", "energy"]
    for key in keys:
        r = subprocess.run([sys.executable, __file__, f"--tamper={key}"],
                           capture_output=True, text=True)
        ok = "RESULT: FAIL" in r.stdout
        caught += ok
        print(f"tamper {key}: {'caught' if ok else 'MISSED'}")
    print(f"tamper-selftest: caught {caught}/{len(keys)}")
    return caught == len(keys)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--tamper-selftest":
        ok = tamper_selftest()
        sys.exit(0 if ok else 1)
    for a in args:
        if a.startswith("--tamper="):
            TAMPER[a.split("=", 1)[1]] = True
    cert = None
    path = None
    if args and args[0] == "--emit-certificate":
        path = args[1]
        cert = {"packet": "twisted-coset-cube-spectrum", "B": 6,
                "chart": "base-3", "claims": ["N", "A", "B", "C"]}
    ok = run_all(cert)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
