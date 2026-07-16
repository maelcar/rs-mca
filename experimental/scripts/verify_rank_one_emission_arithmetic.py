#!/usr/bin/env python3
"""Verifier: emission arithmetic on the rank-one family (the admission input).

Claims checked (see experimental/notes/thresholds/rank_one_emission_arithmetic.md):

  R   (reality/parity) G_{k,r} is REAL for every (k,r) (a <-> -a digit
                       pairing), so chat_v(D) in i^|D| R on every single
                       coset; symmetric pieces have the fully explicit form
                         h(sigma_eps) = 2 G(s_low) cos(2 pi r tau(eps)/3^k),
                         chat_v(D)   = (-1)^{|D|/2} 2 G(s_low) prod trig
                       with odd-|D| vanishing (= band-uniform T2's symmetry).
  E1  (budget)         per-class cube ell^1 budgets in closed form; on a
                       single coset |h(sigma)| == |G(s_low)| identically.
  E2  (schedule)       T3's one-pattern-per-class rule with the argmax
                       pattern is the optimal sound schedule; its payment
                       is closed-form.
  E3  (overdraw wall)  paying ALL patterns overdraws the cube ell^1 budget:
                       ratio > 1 on twisted pieces, attaining EXACTLY 2 at
                       the extremal classes -- the quantified reason T3
                       restricts to one pattern per class.
  E4  (flat collapse)  flat-cube emission (the #791 primitive) collects
                       |cos|/|sin| = 1/sqrt(3) of the optimum on every
                       twisted k=1 class-piece, and as little as ~1% at
                       (k,r) = (3,7): the primitive must widen to rank-one
                       emission.  The maximal band (full r-union) recovers
                       flat exactness (T3's boundary case).
  E5  (resonant pin)   the transverse-charge mandatory instance
                       j* = (c-1)/2 is the all-ones digit word: maximally
                       twisted (r_k = (3^k-1)/2) at EVERY depth, s3 = B,
                       |hatf(j*)| >= 0.70 M.

stdlib only, deterministic; floats under exact Parseval guards.

Usage:
  python3 verify_rank_one_emission_arithmetic.py
  python3 verify_rank_one_emission_arithmetic.py --tamper-selftest
  python3 verify_rank_one_emission_arithmetic.py --emit-certificate PATH
"""
import json
import sys
from cmath import exp as cexp
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


TAMPER = {"pairing": False, "tau_weight": False, "parity_sign": False,
          "budget": False, "overdraw_cap": False, "flat_share": False,
          "argmax_parity": False}

B = 6
c = 3 ** B
P = [3 ** i for i in range(B)]


def s3(y, ndig):
    y %= 3 ** ndig
    s = 0
    for _ in range(ndig):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        s += d != 0
    return s


def wtil(s):
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


HF = [factors_poly([2 * pi * ((j * 3 ** i) % c) / c for i in range(B)])[B]
      for j in range(c)]
EXP = [cexp(-2j * pi * t / c) for t in range(c)]
M = comb(2 * B, B)


def G_complex(k, r):
    ck = 3 ** k
    return [sum(cexp(-2j * pi * a * r / ck) * wtil(s3(a, k) + l)
                for a in range(ck)) / ck for l in range(B + 1)]


def G_paired(k, r):
    """Real form via the a <-> -a digit pairing."""
    ck = 3 ** k
    out = []
    for l in range(B + 1):
        x = wtil(l)
        for a in range(1, ck // 2 + 1):
            w = wtil(s3(a, k) + l)
            if TAMPER["pairing"]:
                x += w * cos(2 * pi * a * r / ck)
            else:
                x += 2 * w * cos(2 * pi * a * r / ck)
        out.append(x / ck)
    return out


def classes():
    return [tuple((n >> i) & 1 for i in range(B)) for n in range(2 ** B)
            if bin(n).count("1") % 2 == B % 2 and bin(n).count("1") >= 2]


CLS = classes()


def coset(k, r):
    return [(r + 3 ** k * m) % c for m in range(3 ** (B - k))]


def brute_h(Ab, sig):
    return sum(HF[xi] * EXP[(xi * sig) % c] for xi in Ab) / c


def v_R_E1_E2_E3_E4(cert):
    worst_h, worst_cube, worst_odd = 0.0, 0.0, 0.0
    worst_unimod = 0.0
    overdraw_max = 0.0
    worst_sched = 0.0
    k1_flat_exact = 0.0
    flat_share_min = {1: 2.0, 2: 2.0, 3: 2.0}
    for k in (1, 2, 3):
        ck = 3 ** k
        # single-coset unimodularity |h| == |G(s_low)| (E1b)
        r0 = 1
        Gr = G_paired(k, r0)
        Ab0 = coset(k, r0)
        for v in CLS[:8]:
            s = sum(v)
            U = [i for i in range(B) if v[i]]
            top = [t for t in range(s) if U[t] >= B - k]
            slow = s - len(top)
            for bits in (0, 1, 2 ** s - 1):
                sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                          for t in range(s)) % c
                gv = abs(Gr[slow]) * (2 if TAMPER["budget"] else 1)
                worst_unimod = max(worst_unimod,
                                   abs(abs(brute_h(Ab0, sig)) - gv))
        # symmetric pieces {r, ck - r}
        for r in range(1, (ck + 1) // 2):
            if (ck - r) % ck == r:
                continue
            Ab = sorted(set(coset(k, r)) | set(coset(k, ck - r)))
            Gr = G_paired(k, r)
            for v in CLS:
                s = sum(v)
                U = [i for i in range(B) if v[i]]
                top = [t for t in range(s) if U[t] >= B - k]
                slow = s - len(top)
                cube, budget = {}, 0.0
                for bits in range(2 ** s):
                    sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                              for t in range(s)) % c
                    hv = brute_h(Ab, sig)
                    tau = sum((1 if not (bits >> t) & 1 else -1)
                              * (1 if TAMPER["tau_weight"]
                                 else 3 ** (U[t] - (B - k))) for t in top)
                    pred = 2 * Gr[slow] * cos(2 * pi * r * tau / ck)
                    worst_h = max(worst_h, abs(hv - pred))
                    cube[bits] = hv
                    budget += abs(hv)
                pays, pays_pred = [], []
                for dbits in range(2 ** s):
                    br = sum(((-1) ** bin(bits & dbits).count("1")) * x
                             for bits, x in cube.items()) / 2 ** s
                    nd = bin(dbits).count("1")
                    if any((dbits >> t) & 1 and t not in top
                           for t in range(s)) or nd % 2:
                        pred = 0.0
                        if nd % 2:
                            worst_odd = max(worst_odd, abs(br))
                    else:
                        pred = 2 * Gr[slow]
                        for t in top:
                            beta = 2 * pi * r * 3 ** (U[t] - (B - k)) / ck
                            pred *= -sin(beta) if (dbits >> t) & 1 \
                                else cos(beta)
                        pred *= 1 if TAMPER["parity_sign"] \
                            else (-1) ** (nd // 2)
                    worst_cube = max(worst_cube, abs(br - pred))
                    pays.append(2 ** s * abs(br))
                    pays_pred.append(2 ** s * abs(pred))
                if budget > 1e-9:
                    overdraw_max = max(overdraw_max, sum(pays) / budget)
                    worst_sched = max(worst_sched,
                                      abs(max(pays) - max(pays_pred)))
                    best = max(pays)
                    if top and best > 1e-9 and abs(Gr[slow]) > 1e-12:
                        share = pays[0] / best
                        if TAMPER["flat_share"]:
                            share = best / max(pays[0], 1e-30)
                        flat_share_min[k] = min(flat_share_min[k], share)
                        if k == 1:
                            k1_flat_exact = max(
                                k1_flat_exact,
                                max(abs(share - 1.0),
                                    abs(pays[0] - budget) / budget))
    check(f"R: symmetric h == 2 G(s_low) cos(2 pi r tau/3^k), ALL (k, r-pairs, classes, eps) (worst {worst_h:.1e})",
          worst_h <= 1e-11)
    check(f"R: cube closed form with i^|D| parity signs (worst {worst_cube:.1e})",
          worst_cube <= 1e-11)
    check(f"R: odd-|D| coefficients vanish (T2 consistency) (worst {worst_odd:.1e})",
          worst_odd <= 1e-11)
    check(f"E1: single-coset |h(sigma)| == |G(s_low)| (unimodular budget) (worst {worst_unimod:.1e})",
          worst_unimod <= 1e-11)
    check(f"E2: optimal one-pattern schedule closed form == brute argmax payment (worst {worst_sched:.1e})",
          worst_sched <= 1e-10)
    cap = 1.0 if TAMPER["overdraw_cap"] else 2.0
    check(f"E3: overdraw wall -- max over pieces/classes of sum_D pay / budget == 2 exactly (got {overdraw_max:.6f})",
          overdraw_max <= cap + 1e-9 and abs(overdraw_max - 2.0) <= 1e-6)
    check(f"E4: symmetric depth-1 pieces are FLAT-EXACT -- flat pattern optimal AND pays the full budget (worst dev {k1_flat_exact:.1e})",
          k1_flat_exact <= 1e-9)
    check(f"E4: flat-cube under-collection at depth 2 -- min share < 0.75 (got {flat_share_min[2]:.4f})",
          flat_share_min[2] < 0.75)
    check(f"E4: flat-cube collapse at k=3 -- min share <= 0.02 (got {flat_share_min[3]:.4f})",
          flat_share_min[3] <= 0.02)
    # single-coset k=1 arithmetic: |chat({top})| / |chat(empty)| == tan(2 pi r/3)
    Ab1 = coset(1, 1)
    Gr1 = G_paired(1, 1)
    v = next(vv for vv in CLS if vv[B - 1] == 1 and sum(vv) == 2)
    U = [i for i in range(B) if v[i]]
    cube = {}
    for bits in range(4):
        sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                  for t in range(2)) % c
        cube[bits] = brute_h(Ab1, sig)
    c0 = sum(cube.values()) / 4
    c1 = sum(((-1) ** ((bits >> 1) & 1)) * x for bits, x in cube.items()) / 4
    check(f"E4: single-coset k=1 ratio |chat(top)|/|chat(empty)| == sqrt(3) == |tan(2 pi/3)| (got {abs(c1)/abs(c0):.6f})",
          abs(abs(c1) / abs(c0) - sqrt(3)) <= 1e-9)
    if cert is not None:
        cert["overdraw_max"] = round(overdraw_max, 9)
        cert["k1_flat_exact_dev"] = f"{k1_flat_exact:.2e}"
        cert["flat_share_min_k2"] = round(flat_share_min[2], 6)
        cert["flat_share_min_k3"] = round(flat_share_min[3], 6)


def v_G_reality(cert):
    worst = 0.0
    for k in (1, 2, 3):
        for r in range(3 ** k):
            gc = G_complex(k, r)
            gp = G_paired(k, r)
            worst = max(worst,
                        max(abs(a - b) for a, b in zip(gc, gp)))
    check(f"R: G_(k,r) real -- complex def == a<->-a paired cosine form, ALL (k,r) (worst {worst:.1e})",
          worst <= 1e-12)
    if cert is not None:
        cert["G_reality_worst"] = f"{worst:.2e}"


def v_single_coset_overdraw(cert):
    """E3's PROVED half: on a single coset, sum_D pays == budget *
    prod_top(|sin|+|cos|), with the factor > 1 on twisted-top classes."""
    worst = 0.0
    min_factor = float("inf")
    for k in (1, 2, 3):
        ck = 3 ** k
        r = 1
        Ab = coset(k, r)
        Gr = G_paired(k, r)
        for v in CLS[:12]:
            s = sum(v)
            U = [i for i in range(B) if v[i]]
            top = [t for t in range(s) if U[t] >= B - k]
            if not top:
                continue
            slow = s - len(top)
            if abs(Gr[slow]) < 1e-12:
                continue
            cube = {}
            for bits in range(2 ** s):
                sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                          for t in range(s)) % c
                cube[bits] = brute_h(Ab, sig)
            budget = sum(abs(x) for x in cube.values())
            tot = sum(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                              for bits, x in cube.items()) / 2 ** s) * 2 ** s
                      for dbits in range(2 ** s))
            factor = 1.0
            for t in top:
                beta = 2 * pi * r * 3 ** (U[t] - (B - k)) / ck
                factor *= abs(sin(beta)) + abs(cos(beta))
            worst = max(worst, abs(tot - budget * factor))
            min_factor = min(min_factor, factor)
    check(f"E3: single-coset identity sum_D pays == budget * prod(|sin|+|cos|) (worst {worst:.1e})",
          worst <= 1e-9)
    check(f"E3: single-coset overdraw factor > 1 on twisted-top classes (min {min_factor:.6f})",
          min_factor > 1 + 1e-9)
    if cert is not None:
        cert["single_coset_min_factor"] = round(min_factor, 9)


def v_flip_weakest(cert):
    """E2 on symmetric pieces: the even-restricted argmax is the
    flip-weakest rule, checked against brute even-maxima on every
    (k, r, top) configuration."""
    worst = 0.0
    cases = odd_cases = 0
    for k in (1, 2, 3):
        ck = 3 ** k
        for r in range(1, ck):
            for topmask in range(1, 2 ** k):
                js = [j for j in range(k) if (topmask >> j) & 1]
                S = [abs(sin(2 * pi * r * 3 ** j / ck)) for j in js]
                C = [abs(cos(2 * pi * r * 3 ** j / ck)) for j in js]
                t = len(js)
                best = 0.0
                for m in range(2 ** t):
                    if bin(m).count("1") % 2:
                        continue
                    p = 1.0
                    for i in range(t):
                        p *= S[i] if (m >> i) & 1 else C[i]
                    best = max(best, p)
                m0 = sum(1 << i for i in range(t) if S[i] > C[i])
                p0 = 1.0
                for i in range(t):
                    p0 *= max(S[i], C[i])
                if bin(m0).count("1") % 2:
                    odd_cases += 1
                    if not TAMPER["argmax_parity"]:
                        p0 *= max(min(S[i], C[i]) / max(S[i], C[i])
                                  for i in range(t))
                cases += 1
                worst = max(worst, abs(best - p0))
    check(f"E2: flip-weakest rule == brute even-restricted maxima, ALL {cases} (k,r,top) configs ({odd_cases} odd-argmax; worst {worst:.1e})",
          worst <= 1e-12 and odd_cases == 122)
    if cert is not None:
        cert["flip_weakest_odd_cases"] = odd_cases


def v_maximal_flat(cert):
    """Full r-union at each depth k == the flat maximal band: D=empty floor
    EQUALS the full cube ell^1 (T3's boundary case), via profile summation."""
    ok = True
    for k in (1, 2, 3):
        ck = 3 ** k
        # sum of all rank-one characters over r in Z_ck collapses to a = 0:
        # closed form h(sigma_eps) = wtil(s3(sigma)) - M/c, class-constant.
        for v in CLS[:6]:
            s = sum(v)
            U = [i for i in range(B) if v[i]]
            for bits in (0, 3 % 2 ** s):
                sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                          for t in range(s)) % c
                hv = brute_h([xi for xi in range(1, c)], sig)
                if abs(hv - (wtil(s) - M / c)) > 1e-9 * M:
                    ok = False
    check("E4: maximal band (full union) recovers class-constant h == wtil(s) - M/c (flat boundary case)",
          ok)


def v_resonant(cert):
    jstar = (c - 1) // 2
    check("E5: j* = (c-1)/2 is the all-ones digit word (s3 == B)",
          s3(jstar, B) == B)
    check("E5: j* is maximally twisted at EVERY depth: j* mod 3^k == (3^k-1)/2, k <= B",
          all(jstar % 3 ** k == (3 ** k - 1) // 2 for k in range(1, B + 1)))
    check(f"E5: |hatf(j*)| >= 0.70 M (transverse-charge pin; got {HF[jstar]/M:.4f})",
          abs(HF[jstar]) >= 0.70 * M)
    if cert is not None:
        cert["resonant_ratio"] = round(HF[jstar] / M, 6)
        # per-depth emission data for the resonant residue
        table = {}
        for k in (1, 2, 3):
            rk = (3 ** k - 1) // 2
            table[f"k{k}"] = {"r": rk,
                              "G": [round(x, 9) for x in G_paired(k, rk)]}
        cert["resonant_G_tables"] = table


def v_guards(cert):
    ps = sum(x * x for x in HF)
    m2 = sum(comb(B, s) * 2 ** s * wtil(s) ** 2 for s in range(B + 1))
    check("guard: Parseval sum hatf^2 == c * M2 (1e-6 rel)",
          abs(ps - c * m2) <= 1e-6 * c * m2)
    N = [0] * c
    T = P + [c - p for p in P]
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    check("guard: Lemma N exact (B=6 brute)",
          all(N[y] == wtil(s3(y, B)) for y in range(c)))


def run_all(cert=None):
    v_guards(cert)
    v_G_reality(cert)
    v_R_E1_E2_E3_E4(cert)
    v_single_coset_overdraw(cert)
    v_flip_weakest(cert)
    v_maximal_flat(cert)
    v_resonant(cert)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} "
          f"({PASSED[0]}/{PASSED[0] + len(FAILED)})")
    return not FAILED


def tamper_selftest():
    import subprocess
    keys = list(TAMPER)
    caught = 0
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
        sys.exit(0 if tamper_selftest() else 1)
    for a in args:
        if a.startswith("--tamper="):
            TAMPER[a.split("=", 1)[1]] = True
    cert = None
    path = None
    if args and args[0] == "--emit-certificate":
        path = args[1]
        cert = {"packet": "rank-one-emission-arithmetic", "B": 6,
                "chart": "base-3",
                "claims": ["R", "E1", "E2", "E3", "E4", "E5"]}
    ok = run_all(cert)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
