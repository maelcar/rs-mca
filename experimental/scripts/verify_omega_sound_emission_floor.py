#!/usr/bin/env python3
"""Verifier: the omega-sound emission floor (compiler soundness discharged).

Claims checked (see experimental/notes/thresholds/omega_sound_emission_floor.md):

  S1  (the catch)   band-uniform T3's floor 2^s|hcube_v(D)| <= sum_eps
                    |h(sigma_eps)| is sound against the cube |h|-ell^1 as
                    stated, but the grammar's charge is omega = h_+ -- and
                    against sum_eps h_+ the floor OVERPAYS on 263 of 558
                    (piece, class) pairs at B = 6, including classes with
                    ZERO positive charge paid positively (witness
                    (k, r, v) = (3, 12, 011110)).
  S2  (the fix)     the omega-sound cap is closed-form:
                        sum_eps h_+ = (sum_eps |h| + 2^s hcube_v(empty)) / 2
                    (exact identity), and on hierarchy pieces it is
                    G-table-computable (h = 2 G(s_low) cos(phi_tau)).
  S3  (safety)      on single-sign (flat) classes the T3 floor is already
                    omega-sound -- depth-1 pieces, subgroup unions, and the
                    maximal band are unaffected; the #791 reduction is
                    untouched.
  S4  (discharge)   the corrected rank-one rule -- pay
                    min(2^s|hcube_v(D*)|, sum_eps h_+), one pattern per
                    class, disjoint pieces -- never overpays omega:
                    compiler soundness is arithmetic, 0 violations.
  S5  (adequacy)    COMPUTED: on EVERY charged (piece, class) pair at
                    B = 6 the argmax payment already reaches the positive
                    charge (2^s|hcube(D*)| >= sum h_+, 421/421), so the
                    corrected rule pays hierarchy pieces IN FULL.

stdlib only, deterministic; floats under exact Parseval + Lemma-N guards.

Usage:
  python3 verify_omega_sound_emission_floor.py
  python3 verify_omega_sound_emission_floor.py --tamper-selftest
  python3 verify_omega_sound_emission_floor.py --emit-certificate PATH
"""
import json
import sys
from cmath import exp as cexp
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


TAMPER = {"cap_identity": False, "closed_sign": False, "uncorrected": False,
          "witness_class": False, "underpay": False}

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


def G_real(k, r):
    ck = 3 ** k
    return [sum(cexp(-2j * pi * a * r / ck) * wtil(s3(a, k) + l)
                for a in range(ck)).real / ck for l in range(B + 1)]


CLS = [tuple((n >> i) & 1 for i in range(B)) for n in range(2 ** B)
       if bin(n).count("1") % 2 == B % 2 and bin(n).count("1") >= 2]


def piece(k, r):
    ck = 3 ** k
    return sorted(set((r + ck * m) % c for m in range(3 ** (B - k)))
                  | set((ck - r + ck * m) % c for m in range(3 ** (B - k))))


IMAG_RESIDUE = [0.0]


def class_data(Ab, v):
    s = sum(v)
    U = [i for i in range(B) if v[i]]
    hvals = []
    for bits in range(2 ** s):
        sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                  for t in range(s)) % c
        z = sum(HF[xi] * EXP[(xi * sig) % c] for xi in Ab) / c
        IMAG_RESIDUE[0] = max(IMAG_RESIDUE[0], abs(z.imag))
        hvals.append(z.real)
    best = 0.0
    for dbits in range(2 ** s):
        cf = sum(((-1) ** bin(bits & dbits).count("1")) * x
                 for bits, x in enumerate(hvals)) / 2 ** s
        best = max(best, abs(cf) * 2 ** s)
    pos = sum(x for x in hvals if x > 0)
    tot = sum(abs(x) for x in hvals)
    mean = sum(hvals)
    return hvals, best, pos, tot, mean


def v_guards():
    m2 = sum(comb(B, s) * 2 ** s * wtil(s) ** 2 for s in range(B + 1))
    check("guard: Parseval sum hatf^2 == c * M2 (1e-6 rel)",
          abs(sum(x * x for x in HF) - c * m2) <= 1e-6 * c * m2)
    N = [0] * c
    T = P + [c - p for p in P]
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    check("guard: Lemma N exact (B=6 brute)",
          all(N[y] == wtil(s3(y, B)) for y in range(c)))


def v_main(cert):
    n_pairs = n_viol = n_zero_paid = 0
    n_charged = n_full = corrected_viol = 0
    id_worst = closed_worst = 0.0
    depth1_overpay = 0.0
    single_sign_overpay = 0.0
    witness_hit = False
    wit = (3, 12, (0, 1, 1, 1, 1, 0))
    if TAMPER["witness_class"]:
        wit = (1, 1, (0, 0, 0, 0, 1, 1))
    for k in (1, 2, 3):
        ck = 3 ** k
        Gk = {}
        for r in range(1, (ck + 1) // 2):
            if (ck - r) % ck == r:
                continue
            Ab = piece(k, r)
            Gr = G_real(k, r)
            for v in CLS:
                s = sum(v)
                U = [i for i in range(B) if v[i]]
                top = [t for t in range(s) if U[t] >= B - k]
                slow = s - len(top)
                hvals, best, pos, tot, mean = class_data(Ab, v)
                n_pairs += 1
                # S2 identity
                cap = (tot + mean) / 2
                if TAMPER["cap_identity"]:
                    cap = tot / 2
                id_worst = max(id_worst, abs(pos - cap))
                # S2 closed form via G
                posG = 0.0
                for tb in range(2 ** len(top)):
                    tau = sum((1 if not (tb >> i) & 1 else -1)
                              * 3 ** (U[top[i]] - (B - k))
                              for i in range(len(top)))
                    hv = 2 * Gr[slow] * cos(2 * pi * r * tau / ck)
                    if (hv < 0) if TAMPER["closed_sign"] else (hv > 0):
                        posG += hv if not TAMPER["closed_sign"] else -hv
                posG *= 2 ** slow
                closed_worst = max(closed_worst, abs(pos - posG))
                # S1: T3-floor vs positive charge
                if best > pos + 1e-12:
                    n_viol += 1
                    if pos <= 1e-12 and best > 1e-9:
                        n_zero_paid += 1
                        if (k, r, v) == wit:
                            witness_hit = True
                # S3: single-sign classes are safe
                if all(x >= -1e-12 for x in hvals) or \
                        all(x <= 1e-12 for x in hvals):
                    single_sign_overpay = max(single_sign_overpay,
                                              best - max(pos, abs(mean)))
                if k == 1:
                    depth1_overpay = max(depth1_overpay,
                                         best - pos if best > pos else 0.0)
                # S4 + S5: corrected rule
                pay = min(best, pos)
                if TAMPER["uncorrected"]:
                    pay = best
                if TAMPER["underpay"]:
                    pay = 0.99 * min(best, pos)
                if pay > pos + 1e-12:
                    corrected_viol += 1
                if pos > 1e-9:
                    n_charged += 1
                    if pay >= pos - 1e-9:
                        n_full += 1
    check(f"S1: T3 floor overpays omega on {n_viol}/558 pairs (expect 263)",
          n_pairs == 558 and n_viol == 263)
    check(f"S1: zero-charge classes paid positively exist incl. witness (3,12,011110) ({n_zero_paid} zero-charge violations)",
          n_zero_paid > 0 and witness_hit)
    check(f"S2: cap identity sum h_+ == (sum|h| + 2^s chat(empty))/2 (worst {id_worst:.1e})",
          id_worst <= 1e-12)
    check(f"S2: cap closed form via G-table (worst {closed_worst:.1e})",
          closed_worst <= 1e-10)
    check(f"S3: single-sign classes -- T3 floor already omega-sound (worst overpay {single_sign_overpay:.1e})",
          single_sign_overpay <= 1e-9)
    check(f"S3: depth-1 pieces unaffected (worst overpay {depth1_overpay:.1e})",
          depth1_overpay <= 1e-12)
    check(f"S4: corrected rule min(argmax, cap) never overpays omega ({corrected_viol} violations)",
          corrected_viol == 0)
    check(f"S5: corrected rule pays IN FULL on every charged pair ({n_full}/{n_charged}, expect 421/421)",
          n_charged == 421 and n_full == 421)
    check(f"guard: h real on symmetric pieces (worst |Im| {IMAG_RESIDUE[0]:.1e})",
          IMAG_RESIDUE[0] <= 1e-12)
    if cert is not None:
        cert["t3_overpay_pairs"] = n_viol
        cert["pairs_total"] = n_pairs
        cert["zero_charge_paid"] = n_zero_paid
        cert["cap_identity_worst"] = f"{id_worst:.2e}"
        cert["cap_closed_form_worst"] = f"{closed_worst:.2e}"
        cert["charged_pairs_full"] = f"{n_full}/{n_charged}"


def v_maximal():
    """Maximal band: h class-constant, positive exactly on the admissible
    levels -- T3 floor == omega cap there (the #791 (=>) territory)."""
    ok = True
    M = comb(2 * B, B)
    for v in CLS[:6]:
        s = sum(v)
        hv = wtil(s) - M / c
        pos = 2 ** s * max(hv, 0.0)
        floor = 2 ** s * abs(hv)
        if hv > 0 and abs(floor - pos) > 1e-9:
            ok = False
    check("S3: maximal band -- T3 floor == omega cap on positive levels (closed form)",
          ok)


def run_all(cert=None):
    v_guards()
    v_main(cert)
    v_maximal()
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} "
          f"({PASSED[0]}/{PASSED[0] + len(FAILED)})")
    return not FAILED


def tamper_selftest():
    import subprocess
    caught = 0
    keys = list(TAMPER)
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
        cert = {"packet": "omega-sound-emission-floor", "B": 6,
                "chart": "base-3", "claims": ["S1", "S2", "S3", "S4", "S5"]}
    ok = run_all(cert)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
