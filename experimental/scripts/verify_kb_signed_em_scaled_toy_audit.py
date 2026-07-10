#!/usr/bin/env python3
"""Zero-argument, stdlib-only verifier for a scaled KB signed-e_m toy.

The row p=193, n=64, m=30, w=2 has the same w/n=1/32 scale and nearly
the same m/n density as the deployed KB-MCA row. Unlike the w>=2 rows in the
integrated participation-ratio packet, its average prefix-fiber size is much
larger than one. We compute the prefix fibers exactly and the signed-e_m
spectrum independently, compressed by the exact mu_n dilation action.
It is density/prefix-depth scaled, not geometry-faithful: its subgroup index is
3, while the deployed KB index is 1016.

Run under the repository's overnight cap:
  ulimit -v 2097152; python3 experimental/scripts/verify_kb_signed_em_scaled_toy_audit.py
"""

from array import array
from fractions import Fraction
import cmath
import json
import math
import os
import resource
import sys
import time


CAP_GB = float(os.environ.get("KB_SIGNED_EM_AS_CAP_GB", "2.0"))
CAP_BYTES = min(int(CAP_GB * 1024**3), 2 * 1024**3)
_soft, _hard = resource.getrlimit(resource.RLIMIT_AS)
if _hard != resource.RLIM_INFINITY:
    CAP_BYTES = min(CAP_BYTES, _hard)
resource.setrlimit(resource.RLIMIT_AS, (CAP_BYTES, CAP_BYTES))


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")
DATA_DIR = os.environ.get("KB_SIGNED_EM_DATA_DIR", DEFAULT_DATA_DIR)
JSON_PATH = os.path.join(DATA_DIR, "cap25_v13_kb_signed_em_scaled_toy_audit.json")
with open(JSON_PATH, "r", encoding="utf-8") as handle:
    DATA = json.load(handle)

CHECKS = []


def check(name, cond, detail=""):
    ok = bool(cond)
    CHECKS.append((name, ok, detail))
    suffix = f"  ({detail})" if detail else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def prime_factors(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p):
    factors = prime_factors(p - 1)
    return next(
        g for g in range(2, p)
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors)
    )


def subgroup(p, n):
    assert (p - 1) % n == 0
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    values = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = x * h % p
    assert x == 1 and len(set(values)) == n
    return g, h, tuple(values)


def exact_prefix_fibers(p, domain, m):
    """Return exact N(z1,z2) for m-subsets using uint64 slice DP."""
    size = p * p
    zero = array("Q", [0]) * size
    dp = [array("Q", zero) for _ in range(m + 1)]
    dp[0][0] = 1
    for used, x in enumerate(domain):
        x2 = x * x % p
        perm = array("I", [0]) * size
        pos = 0
        for z1 in range(p):
            base = ((z1 + x) % p) * p
            for z2 in range(p):
                perm[pos] = base + ((z2 + x2) % p)
                pos += 1
        for j in range(min(m, used + 1), 0, -1):
            src = dp[j - 1]
            dst = dp[j]
            for idx, value in enumerate(src):
                if value:
                    target = perm[idx]
                    dst[target] += value
    return dp[m]


def mode_orbits(p, h, n):
    """Orbits of (t1,t2)->(h*t1,h^2*t2) on F_p^2 minus zero."""
    size = p * p
    seen = bytearray(size)
    seen[0] = 1
    h2 = h * h % p
    orbits = []
    for code in range(1, size):
        if seen[code]:
            continue
        t1, t2 = divmod(code, p)
        orbit = []
        u1, u2 = t1, t2
        while True:
            here = u1 * p + u2
            if seen[here]:
                break
            seen[here] = 1
            orbit.append(here)
            u1 = u1 * h % p
            u2 = u2 * h2 % p
        assert u1 == t1 and u2 == t2
        orbits.append((t1, t2, len(orbit)))
    assert all(seen)
    assert 1 + sum(mult for _, _, mult in orbits) == size
    return orbits


def em_for_mode(p, domain, m, omega, t1, t2, reverse=False):
    coeff = [0j] * (m + 1)
    coeff[0] = 1.0 + 0.0j
    xs = reversed(domain) if reverse else domain
    used = 0
    for x in xs:
        phase = (t1 * x + t2 * x * x) % p
        v = omega[phase]
        used += 1
        for j in range(min(m, used), 0, -1):
            coeff[j] += v * coeff[j - 1]
    return coeff[m]


def spectrum(p, domain, m, orbits):
    omega = tuple(cmath.exp(2j * math.pi * s / p) for s in range(p))
    C = math.comb(len(domain), m)
    L1 = 0.0
    L2 = 0.0
    L1_reverse = 0.0
    L2_reverse = 0.0
    L1_prim = 0.0
    L2_prim = 0.0
    L1_quot = 0.0
    L2_quot = 0.0
    by_category = {
        "linear": [0.0, 0.0],
        "mixed": [0.0, 0.0],
        "quadratic_quotient": [0.0, 0.0],
    }
    orbit_rows = []
    worst_reverse_rel = 0.0
    for t1, t2, mult in orbits:
        em = em_for_mode(p, domain, m, omega, t1, t2)
        em_reverse = em_for_mode(p, domain, m, omega, t1, t2, reverse=True)
        mag = abs(em)
        mag_reverse = abs(em_reverse)
        scale = max(1.0, mag, mag_reverse)
        worst_reverse_rel = max(worst_reverse_rel, abs(mag - mag_reverse) / scale)
        mass1 = mult * mag
        mass2 = mult * mag * mag
        mass1_reverse = mult * mag_reverse
        mass2_reverse = mult * mag_reverse * mag_reverse
        L1 += mass1
        L2 += mass2
        L1_reverse += mass1_reverse
        L2_reverse += mass2_reverse
        primitive = t1 != 0
        if primitive:
            L1_prim += mass1
            L2_prim += mass2
        else:
            L1_quot += mass1
            L2_quot += mass2
        if t1 != 0 and t2 == 0:
            category = "linear"
        elif t1 != 0 and t2 != 0:
            category = "mixed"
        else:
            category = "quadratic_quotient"
        by_category[category][0] += mass1
        by_category[category][1] += mass2
        orbit_rows.append(
            (mass1, mass2, t1, t2, mult, mag / C, primitive, category)
        )
    return {
        "L1": L1,
        "L2": L2,
        "L1_reverse": L1_reverse,
        "L2_reverse": L2_reverse,
        "L1_prim": L1_prim,
        "L2_prim": L2_prim,
        "L1_quot": L1_quot,
        "L2_quot": L2_quot,
        "by_category": by_category,
        "orbits": orbit_rows,
        "worst_reverse_rel": worst_reverse_rel,
    }


def fraction_float(fr):
    return fr.numerator / fr.denominator


def concentration_count(rows, which, fraction):
    idx = 0 if which == "L1" else 1
    ordered = sorted(rows, key=lambda row: row[idx], reverse=True)
    total = sum(row[idx] for row in ordered)
    target = fraction * total
    acc = 0.0
    count_modes = 0
    count_orbits = 0
    for row in ordered:
        acc += row[idx]
        count_modes += row[4]
        count_orbits += 1
        if acc >= target:
            return count_orbits, count_modes
    return count_orbits, count_modes


def parameter_gate(p, n, m, w, C):
    return (
        prime_factors(p) == [p]
        and (p - 1) % n == 0
        and 0 < m < n
        and 0 < w < p
        and C == math.comb(n, m)
        and C < 2**64
    )


def fiber_gate(total, C, nonempty, space, minimum, maximum):
    return (
        total == C
        and nonempty == space
        and 0 < minimum <= maximum
        and maximum * space >= C
    )


def orbit_gate(orbits, p, n):
    total = 0
    for t1, t2, mult in orbits:
        active = []
        if t1:
            active.append(1)
        if t2:
            active.append(2)
        if not active:
            return False
        stabilizer = n
        for degree in active:
            stabilizer = math.gcd(stabilizer, degree)
        if mult != n // stabilizer:
            return False
        total += mult
    return total == p * p - 1


def scope_gate(status, space, deploy_nu_ref):
    return status == "AUDIT/MEASURED" and space - 1 < deploy_nu_ref


print("== KB signed-e_m scaled-toy audit ==")
print("OBJECT: raw KB signed-e_m primitive orbit amplitudes; #431 O414 -> A397")
print("STATUS: PROVED reduction / AUDIT / MEASURED; deployed inverse OPEN")
print("REPRODUCIBILITY: deterministic exact DP and full orbit replay; no seed")
P = 193
N = 64
M = 30
W = 2
DEPLOY_N = 2**21
DEPLOY_P = 2**31 - 2**24 + 1
DEPLOY_K = 2**20
DEPLOY_A = 1116048
DEPLOY_M = 981104
DEPLOY_W = 67471
DEPLOY_BSTAR = 274980728111395087
DEPLOY_TP = 143763024447376
DEPLOY_BREM = DEPLOY_BSTAR - DEPLOY_TP
DEPLOY_KREM = 4805007
DEPLOY_NU_REF = (DEPLOY_KREM - 1) ** 2
STATUS = "AUDIT/MEASURED"

DEPLOY_C = math.comb(DEPLOY_N, DEPLOY_M)
DEPLOY_PW = DEPLOY_P**DEPLOY_W
DEPLOY_AVG_FLOOR = DEPLOY_C // DEPLOY_PW
DEPLOY_AVG_CEIL = -((-DEPLOY_C) // DEPLOY_PW)
DEPLOY_TARGET_FLOOR = (DEPLOY_KREM * DEPLOY_C) // DEPLOY_PW
DEPLOY_KRAW = (DEPLOY_BSTAR * DEPLOY_PW) // DEPLOY_C

g, h, D = subgroup(P, N)
C = math.comb(N, M)
space = P**W
avg = Fraction(C, space)

print("\n== Section 1 parameters and scaling ==")
check("self RLIMIT_AS cap is at most 2 GiB", CAP_BYTES <= 2 * 1024**3,
      f"cap={CAP_BYTES} bytes")
check("deployed row dimensions derive exactly",
      DEPLOY_M == DEPLOY_N - DEPLOY_A
      and DEPLOY_W == DEPLOY_A - (DEPLOY_K + 1))
check("deployed avg floor/ceil reproduce #414",
      DEPLOY_AVG_FLOOR == 57198030365
      and DEPLOY_AVG_CEIL == 57198030366,
      f"floor={DEPLOY_AVG_FLOOR}, ceil={DEPLOY_AVG_CEIL}")
check("deployed first-match remaining budget derives exactly",
      DEPLOY_BREM == 274836965086947711
      and (DEPLOY_BREM * DEPLOY_PW) // DEPLOY_C == DEPLOY_KREM,
      f"Brem={DEPLOY_BREM}, Krem={DEPLOY_KREM}")
check("deployed target floor reproduces #414",
      DEPLOY_TARGET_FLOOR == 274836936291722953,
      str(DEPLOY_TARGET_FLOOR))
check("deployed raw quotient and reservation derive exactly",
      DEPLOY_KRAW == 4807520 and DEPLOY_KRAW - DEPLOY_KREM == 2513,
      f"Kraw={DEPLOY_KRAW}, loss={DEPLOY_KRAW - DEPLOY_KREM}")
check("deployed reference participation numerator is exact",
      DEPLOY_NU_REF == 23088082660036,
      str(DEPLOY_NU_REF))
check("parameter gate accepts the shipped row", parameter_gate(P, N, M, W, C))
check("p=193 is prime (trial-factor certificate)", prime_factors(P) == [P])
check("D=mu_64 and index (p-1)/n=3", len(set(D)) == N and (P - 1) // N == 3)
check("w/n matches deployment within 3.0%",
      abs(W / N - DEPLOY_W / DEPLOY_N) / (DEPLOY_W / DEPLOY_N) < 0.03,
      f"toy={W / N:.8f}, deploy={DEPLOY_W / DEPLOY_N:.8f}")
check("m/n matches deployment within 0.3%",
      abs(M / N - DEPLOY_M / DEPLOY_N) / (DEPLOY_M / DEPLOY_N) < 0.003,
      f"toy={M / N:.8f}, deploy={DEPLOY_M / DEPLOY_N:.8f}")
check("scaled-toy average is much larger than one", avg > 2**40,
      f"avg={fraction_float(avg):.6e}=2^{math.log2(fraction_float(avg)):.3f}")
check("toy respects characteristic > w and n | p-1", P > W and (P - 1) % N == 0)
check("toy is not geometry-faithful to deployed subgroup index",
      (P - 1) // N != (DEPLOY_P - 1) // DEPLOY_N,
      f"toy index={(P - 1) // N}, deploy index={(DEPLOY_P - 1) // DEPLOY_N}")

print("\n== Section 2 exact prefix-fiber DP ==")
t0 = time.monotonic()
fibers = exact_prefix_fibers(P, D, M)
fiber_seconds = time.monotonic() - t0
sumN = sum(fibers)
sumN2 = sum(value * value for value in fibers)
maxN = max(fibers)
minN = min(fibers)
nonempty = sum(value != 0 for value in fibers)
Gamma2 = Fraction(space * sumN2, C * C)
Rmax = Fraction(space * maxN, C)
check("exact fiber gate accepts the recomputed distribution",
      fiber_gate(sumN, C, nonempty, space, minN, maxN))
check("all p^2 target fibers are nonempty", nonempty == space, f"{nonempty}/{space}")
check("exact max fiber is above exact average", maxN * space >= C,
      f"min={minN}, max={maxN}")
check("exact Gamma2 >= 1", Gamma2 >= 1,
      f"Gamma2-1={fraction_float(Gamma2 - 1):.9g}")
check("exact row-sharp ratio is finite", Rmax > 1,
      f"Rmax={fraction_float(Rmax):.9f}")

print("\n== Section 3 dilation-orbit compressed signed-e_m spectrum ==")
orbits = mode_orbits(P, h, N)
check("dual twist-orbit gate accepts the full nonzero mode partition", orbit_gate(orbits, P, N))
primitive_orbits = sum(t1 != 0 for t1, _, _ in orbits)
quotient_orbits = len(orbits) - primitive_orbits
check("primitive mode orbits have size n",
      all(mult == N for t1, _, mult in orbits if t1 != 0))
check("pure quadratic quotient orbits have size n/2",
      all(mult == N // 2 for t1, _, mult in orbits if t1 == 0))
check("orbit count is exact", len(orbits) == 585,
      f"total={len(orbits)}, primitive={primitive_orbits}, quotient={quotient_orbits}")
t1 = time.monotonic()
spec = spectrum(P, D, M, orbits)
spectrum_seconds = time.monotonic() - t1
D_offset = tuple(g * x % P for x in D)
spec_offset = spectrum(P, D_offset, M, orbits)
L1 = spec["L1"]
L2 = spec["L2"]
PR = L1 * L1 / L2
PR_prim = spec["L1_prim"] ** 2 / spec["L2_prim"]
primitive_amplitudes = [row[5] for row in spec["orbits"] if row[6]]
PR_primitive_orbits = (
    sum(primitive_amplitudes) ** 2
    / sum(value * value for value in primitive_amplitudes)
)
DEPLOY_PRIMITIVE_ORBIT_BUDGET = Fraction(DEPLOY_NU_REF, DEPLOY_N)
Gamma2_minus_1 = fraction_float(Gamma2 - 1)
parseval_rhs = C * C * Gamma2_minus_1
parseval_rel = abs(L2 - parseval_rhs) / parseval_rhs
fourier_upper = (C + L1) / space
triangle_factor = fourier_upper / maxN
primitive_share = spec["L1_prim"] / L1
mixed_L1_share = spec["by_category"]["mixed"][0] / L1
mixed_L2_share = spec["by_category"]["mixed"][1] / L2
top_two = sorted(spec["orbits"], key=lambda row: row[1], reverse=True)[:2]
top_two_L2_share = sum(row[1] for row in top_two) / L2
top_two_are_mixed = all(row[7] == "mixed" for row in top_two)
reverse_L1_rel = abs(L1 - spec["L1_reverse"]) / L1
reverse_L2_rel = abs(L2 - spec["L2_reverse"]) / L2
offset_L1_rel = abs(L1 - spec_offset["L1"]) / L1
offset_L2_rel = abs(L2 - spec_offset["L2"]) / L2
check("direct spectral DP has bounded per-orbit order drift",
      spec["worst_reverse_rel"] < 1e-8,
      f"worst relative magnitude drift={spec['worst_reverse_rel']:.3e}")
check("aggregate L1/L2 are order-robust",
      reverse_L1_rel < 2e-11 and reverse_L2_rel < 2e-11,
      f"L1={reverse_L1_rel:.3e}, L2={reverse_L2_rel:.3e}")
check("coset-offset spectrum is invariant after mode reparametrization",
      offset_L1_rel < 2e-11 and offset_L2_rel < 2e-11,
      f"L1={offset_L1_rel:.3e}, L2={offset_L2_rel:.3e}")
check("spectral L2 matches exact-fiber Parseval",
      parseval_rel < 2e-11,
      f"relative error={parseval_rel:.3e}")
check("Fourier triangle bound dominates the exact max fiber",
      fourier_upper >= maxN * (1 - 2e-12),
      f"triangle/max={triangle_factor:.6f}")
check("participation ratio lies in [1,p^w-1]", 1 <= PR <= space - 1,
      f"PR={PR:.6f}/{space - 1}")
check("primitive modes carry a strict majority of L1 mass", primitive_share > 0.5,
      f"primitive share={primitive_share:.6f}")
check("linear/mixed/quadratic classification partitions L1/L2",
      abs(sum(v[0] for v in spec["by_category"].values()) - L1) / L1 < 2e-14
      and abs(sum(v[1] for v in spec["by_category"].values()) - L2) / L2 < 2e-14)
check("mixed primitive modes carry the measured L1 share",
      abs(mixed_L1_share - 0.961946994846) < 5e-12,
      f"mixed L1 share={mixed_L1_share:.12f}")
check("mixed primitive modes carry the measured L2 share",
      abs(mixed_L2_share - 0.995891818575) < 5e-12,
      f"mixed L2 share={mixed_L2_share:.12f}")
check("two mixed twist orbits carry the measured L2 mass",
      top_two_are_mixed and abs(top_two_L2_share - 0.993360184) < 5e-9,
      f"top-two L2 share={top_two_L2_share:.12f}")
check("primitive participation factors exactly by full dual twist orbits",
      abs(PR_prim / N - PR_primitive_orbits) < 2e-11,
      f"PR_prim={PR_prim:.6f}=n*{PR_primitive_orbits:.6f}")
check("deployed primitive reference target becomes an orbit budget",
      DEPLOY_PRIMITIVE_ORBIT_BUDGET == Fraction(5772020665009, 524288),
      f"{float(DEPLOY_PRIMITIVE_ORBIT_BUDGET):.6f}=2^{math.log2(float(DEPLOY_PRIMITIVE_ORBIT_BUDGET)):.6f}")

print("\n== Section 4 scaled-toy measurements and falsification guards ==")
nu_true_toy = (DEPLOY_KREM - 1) ** 2 / Gamma2_minus_1
check("automatic finite-space sanity: raw STAR with deployed Krem",
      L1 / C <= DEPLOY_KREM - 1,
      f"L1/C={L1 / C:.9f} vs {DEPLOY_KREM - 1}")
check("automatic finite-space sanity: equivalent PR inequality",
      PR <= nu_true_toy,
      f"PR={PR:.6f}, nu*={nu_true_toy:.6e}")
check("toy PR does not itself prove the deployed inverse",
      space - 1 < DEPLOY_NU_REF,
      f"all {space - 1} toy modes < deploy nu_ref={DEPLOY_NU_REF}")
check("scope gate keeps the packet at AUDIT/MEASURED",
      scope_gate(STATUS, space, DEPLOY_NU_REF))
check("the triangle certificate is audited against the true fiber, not assumed exact",
      triangle_factor >= 1.0,
      f"triangle/max={triangle_factor:.6f}")
check("the w>=2 density/prefix-depth row is not an avg<<1 artifact", avg > 1 and W >= 2)
concentrations = []
for frac in (0.5, 0.9, 0.99):
    o1, q1 = concentration_count(spec["orbits"], "L1", frac)
    o2, q2 = concentration_count(spec["orbits"], "L2", frac)
    concentrations.append((frac, o1, q1, o2, q2))
    print(f"  MASS {frac:.0%}: L1 {o1} orbits/{q1} modes; L2 {o2} orbits/{q2} modes")
print("  TOP ORBITS (L1 contribution):")
for mass1, mass2, t1_mode, t2_mode, mult, mag_over_C, primitive, category in sorted(
        spec["orbits"], reverse=True)[:10]:
    print(
        f"    t=({t1_mode},{t2_mode}) mult={mult} {category} "
        f"mag/C={mag_over_C:.12g} L1share={mass1 / L1:.9f} L2share={mass2 / L2:.9f}"
    )

print("\n== Section 5 exact outputs ==")
print(f"  p={P} n={N} m={M} w={W} index={(P - 1) // N}")
print(f"  C={C} space={space} avg={fraction_float(avg):.12f} log2avg={math.log2(fraction_float(avg)):.9f}")
print(f"  fiber min={minN} max={maxN} Rmax={fraction_float(Rmax):.12f}")
print(f"  Gamma2-1={Gamma2_minus_1:.12g}")
print(f"  L1/C={L1 / C:.12f} L2/C^2={L2 / (C * C):.12g}")
print(f"  PR={PR:.12f} normalized_PR={PR / (space - 1):.12f}")
print(f"  primitive_PR={PR_prim:.12f} primitive_orbit_PR={PR_primitive_orbits:.12f}")
print(f"  primitive_L1_share={primitive_share:.12f}")
for category, (cat_L1, cat_L2) in spec["by_category"].items():
    print(f"  {category}: L1share={cat_L1 / L1:.12f} L2share={cat_L2 / L2:.12f}")
print(f"  triangle/max={triangle_factor:.12f}")
print(f"  runtime fiber={fiber_seconds:.3f}s spectrum={spectrum_seconds:.3f}s")

print("\n== Section 6 live-gate tamper guards ==")


def rejected(name, gate_result):
    check("tamper::" + name, not gate_result)


rejected("wrong_C", parameter_gate(P, N, M, W, C - 1))
rejected("wrong_fiber_total", fiber_gate(sumN - 1, C, nonempty, space, minN, maxN))
rejected("wrong_fiber_occupancy", fiber_gate(sumN, C, nonempty - 1, space, minN, maxN))
bad_orbits = list(orbits)
bad_t1, bad_t2, bad_mult = bad_orbits[0]
bad_orbits[0] = (bad_t1, bad_t2, bad_mult - 1)
rejected("wrong_orbit_size", orbit_gate(bad_orbits, P, N))
rejected("claim_deployed_proof", scope_gate("PROVED_DEPLOYED", space, DEPLOY_NU_REF))
rejected("hide_finite_space_triviality", scope_gate(STATUS, DEPLOY_NU_REF + 2, DEPLOY_NU_REF))

passed = sum(ok for _, ok, _ in CHECKS)
total = len(CHECKS)
print(f"\nRESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total} checks)")
sys.exit(0 if passed == total else 1)
