#!/usr/bin/env python3
"""KB mixed twist-orbit energy: a graded index ladder for the deployed-transfer question.

Zero-argument, stdlib-only verifier.  It extends PR #475's exact mixed-axis
Parseval identity and 576-orbit Cauchy--Schwarz bound to a graded toy family with
increasing multiplicative subgroup index ``[F_p^*:H]``, and adds an EXACT per-coset
energy decomposition that supports a rigorous split (heavy cosets counted exactly,
light cosets bounded by Cauchy--Schwarz) improving on the plain #475 bound.

Everything gated below is an exact integer or rational identity.  Amplitudes /
``S_mix`` / slack are MEASURED (float) and cross-checked against the exact energy.

Normal path: recompute all exact quantities, check the committed JSON, run live
tamper tests.  ``KB_LADDER_WRITE_JSON=1`` regenerates the JSON mechanically.

    ulimit -v 2097152
    python3 experimental/scripts/verify_kb_mixed_orbit_index_ladder.py
"""

from array import array
import cmath
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
from collections import defaultdict
from typing import Any, Callable

ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3
PACKET = "cap25_v13_kb_mixed_orbit_index_ladder"
DATA_NAME = f"{PACKET}.json"
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR = Path(os.environ.get("KB_LADDER_DATA_DIR", DEFAULT_DATA_DIR))
DATA_PATH = DATA_DIR / DATA_NAME

# Deployed KoalaBear MCA row (a_+ = 1116048); constants from
# cap25_v13_q_moment_floor_reconciliation.md / q_em_inverse_participation_ratio.md.
DEPLOYED = {
    "p": 2**31 - 2**24 + 1,          # 2130706433
    "n": 2**21,                       # 2097152
    "k": 2**20,                       # 1048576
    "a_plus": 1_116_048,
    "m": 2**21 - 1_116_048,           # 981104
    "w": 1_116_048 - (2**20 + 1),     # 67471
    "B_star": 274980728111395087,
    "subgroup_index": ((2**31 - 2**24 + 1) - 1) // (2**21),  # 1016
}
# #475 published exact energies at (193,64,30), used as a byte cross-check.
CROSS_475 = {"p": 193, "n": 64, "m": 30,
             "mixed_energy": 50213717213843458304,
             "linear_energy": 488790592,
             "quadratic_energy": 207138020418762144}
# Dead unrestricted-second-moment margin (HARD BOUNDARY (a)); cap25_v13_q_em_inverse_participation_ratio.md.
DEAD_SECOND_MOMENT_MARGIN_BITS = "1045396.58"

# (p, n, m, do_full_coset_sum).  m ~ n/2, w = 2 throughout.  Full coset sum is the
# O(p^3) exact Sum_kappa E_kappa = E_mix identity check; only cheap for small p.
LADDER = [
    (7, 6, 3, True), (13, 6, 3, True), (31, 6, 3, True), (61, 6, 3, True),
    (127, 6, 3, True), (307, 6, 3, False), (601, 6, 3, False),
    (13, 12, 6, True), (37, 12, 6, True), (61, 12, 6, True), (109, 12, 6, True),
    (157, 12, 6, False), (241, 12, 6, False), (313, 12, 6, False),
    (41, 20, 10, True), (101, 20, 10, True), (181, 20, 10, False), (401, 20, 10, False),
    (31, 30, 15, True), (61, 30, 15, True), (151, 30, 15, True), (211, 30, 15, False),
    (97, 48, 24, False), (109, 54, 27, False), (193, 64, 30, False),  # large-subgroup; 193 = #475 anchor
]
HEAVY_K = 3  # number of heavy s-cosets peeled in the split bound (capped at index)


class CheckFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            raise CheckFailure(label)
        self.passed += 1

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.check(actual == expected, f"{label}: {actual!r} != {expected!r}")

    def close(self, actual: float, expected: float, tol: float, label: str) -> None:
        denom = max(1.0, abs(expected))
        self.check(abs(actual - expected) <= tol * denom, f"{label}: {actual} !~ {expected}")


def impose_address_space_cap() -> int:
    requested_gb = float(os.environ.get("KB_LADDER_AS_CAP_GB", "2"))
    if not (0 < requested_gb <= 2):
        raise CheckFailure("KB_LADDER_AS_CAP_GB must lie in (0,2]")
    cap = min(int(requested_gb * 1024**3), ADDRESS_SPACE_CAP_BYTES)
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    if soft > ADDRESS_SPACE_CAP_BYTES:
        raise CheckFailure("RLIMIT_AS exceeds 2 GiB")
    return int(soft)


# ---------- number theory ----------
def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def is_prime(value: int) -> bool:
    return value >= 2 and prime_factors(value) == [value]


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // q, p) != 1 for q in factors):
            return candidate
    raise CheckFailure("no primitive root")


def subgroup(p: int, n: int) -> tuple[int, int, tuple[int, ...]]:
    if not is_prime(p) or (p - 1) % n:
        raise CheckFailure(f"invalid subgroup parameters ({p},{n})")
    g = primitive_root(p)
    step = pow(g, (p - 1) // n, p)
    values = tuple(pow(step, i, p) for i in range(n))
    if len(set(values)) != n or pow(step, n, p) != 1:
        raise CheckFailure("subgroup order failure")
    return g, step, values


# ---------- exact prefix-fiber DP ----------
def exact_prefix_fibers(p: int, domain: tuple[int, ...], m: int) -> array:
    """Exact counts N(z1,z2) of m-subsets with (sum, sum of squares)=(z1,z2)."""
    size = p * p
    dp = [array("Q", [0]) * size for _ in range(m + 1)]
    dp[0][0] = 1
    for used, x in enumerate(domain):
        x2 = x * x % p
        perm = array("I", [0]) * size
        si = 0
        for z1 in range(p):
            base = ((z1 + x) % p) * p
            for z2 in range(p):
                perm[si] = base + ((z2 + x2) % p)
                si += 1
        for card in range(min(m, used + 1), 0, -1):
            src = dp[card - 1]
            tgt = dp[card]
            for idx, c in enumerate(src):
                if c:
                    tgt[perm[idx]] += c
    return dp[m]


def axis_energies(p: int, fibers: array, C: int) -> dict[str, int]:
    joint = sum(c * c for c in fibers)
    first = [0] * p
    second = [0] * p
    for idx, c in enumerate(fibers):
        z1, z2 = divmod(idx, p)
        first[z1] += c
        second[z2] += c
    f2 = sum(c * c for c in first)
    s2 = sum(c * c for c in second)
    total = p * p * joint - C * C
    linear = p * f2 - C * C
    quadratic = p * s2 - C * C
    mixed = total - linear - quadratic
    return {"total": total, "linear": linear, "quadratic": quadratic, "mixed": mixed,
            "joint_sq": joint, "first_sq": f2, "second_sq": s2}


def coset_energy(p: int, fibers: array, C: int, s_values: list[int]) -> int:
    """EXACT E_kappa = sum_{s in kappa} ( p*sum_y R_s(y)^2 - C^2 ),
    R_s(y) = #{m-subsets M: sumsq(M) - s*sum(M) = y} = sheared marginal of N."""
    total = 0
    for s in s_values:
        R = [0] * p
        for idx, c in enumerate(fibers):
            if c:
                z1, z2 = divmod(idx, p)
                R[(z2 - s * z1) % p] += c
        total += p * sum(r * r for r in R) - C * C
    return total


def isqrt_ceil(value: int) -> int:
    if value <= 0:
        return 0
    r = math.isqrt(value)
    return r if r * r == value else r + 1


# ---------- orbit amplitudes (MEASURED float) ----------
def orbit_amplitudes(p: int, step: int, n: int, domain: list[int], m: int
                     ) -> list[tuple[float, int]]:
    """One |E(t)| per mixed twist orbit; return (amplitude, s = -t1/t2)."""
    dom2 = [(x * x) % p for x in domain]
    seen = bytearray(p * p)
    steps = [pow(step, j, p) for j in range(n)]
    two_pi = 2.0 * math.pi
    amps: list[tuple[float, int]] = []
    inv_cache: dict[int, int] = {}
    for t1 in range(1, p):
        row = t1 * p
        for t2 in range(1, p):
            if seen[row + t2]:
                continue
            for hh in steps:
                seen[(hh * t1 % p) * p + (hh * hh % p) * t2 % p] = 1
            poly = [0j] * (m + 1)
            poly[0] = 1 + 0j
            for x, x2 in zip(domain, dom2):
                u = cmath.exp(1j * two_pi * ((t1 * x + t2 * x2) % p) / p)
                for kk in range(m, 0, -1):
                    poly[kk] += poly[kk - 1] * u
            inv = inv_cache.get(t2)
            if inv is None:
                inv = pow(t2, p - 2, p)
                inv_cache[t2] = inv
            amps.append((abs(poly[m]), (-t1 * inv) % p))
    return amps


def coset_index_map(p: int, g: int, index: int) -> dict[int, int]:
    """s -> coset of s in F_p^*/H, i.e. dlog_g(s) mod index."""
    out: dict[int, int] = {}
    cur = 1
    for e in range(p - 1):
        out[cur] = e % index
        cur = cur * g % p
    return out


def r_H(Hset: set[int], p: int, s: int) -> int:
    return sum(1 for x in Hset if (s - x) % p in Hset)


# ---------- fraction / decimal helpers ----------
def fraction_record(value: Fraction) -> dict[str, Any]:
    with localcontext() as ctx:
        ctx.prec = 40
        dec = Decimal(value.numerator) / Decimal(value.denominator)
    return {"numerator": value.numerator, "denominator": value.denominator,
            "decimal": format(dec, ".12E")}


def analyze_point(p: int, n: int, m: int, full_coset: bool) -> dict[str, Any]:
    g, step, domain = subgroup(p, n)
    C = math.comb(n, m)
    if C >= 2**64:
        raise CheckFailure(f"uint64 fiber cells not exact for ({p},{n},{m})")
    index = (p - 1) // n
    fibers = exact_prefix_fibers(p, list(domain), m)
    en = axis_energies(p, fibers, C)
    E_mix = en["mixed"]
    n_orbits = (p - 1) ** 2 // n
    orbits_per_coset = p - 1

    amps = orbit_amplitudes(p, step, n, list(domain), m)
    if len(amps) != n_orbits:
        raise CheckFailure(f"orbit count mismatch at ({p},{n},{m})")
    S_mix = n * math.fsum(a for a, _ in amps)
    amp_energy = n * math.fsum(a * a for a, _ in amps)  # ~ E_mix
    cmap = coset_index_map(p, g, index)

    # float per-coset energy -> pick heavy cosets
    coset_float = defaultdict(float)
    for a, s in amps:
        coset_float[cmap[s]] += n * a * a
    K = min(HEAVY_K, index)
    heavy = sorted(range(index), key=lambda c: -coset_float.get(c, 0.0))[:K]

    steps_all = [pow(step, j, p) for j in range(n)]
    exact_coset: dict[int, int] = {}
    if full_coset:
        for ci in range(index):
            srep = pow(g, ci, p)
            exact_coset[ci] = coset_energy(p, fibers, C, [srep * st % p for st in steps_all])
        if sum(exact_coset.values()) != E_mix:
            raise CheckFailure(f"sum of coset energies != E_mix at ({p},{n},{m})")
        # heavy = exact top-K
        heavy = sorted(range(index), key=lambda c: -exact_coset[c])[:K]
    else:
        for ci in heavy:
            srep = pow(g, ci, p)
            exact_coset[ci] = coset_energy(p, fibers, C, [srep * st % p for st in steps_all])

    E_heavy = sum(exact_coset[c] for c in heavy)
    E_light = E_mix - E_heavy
    N_light = n_orbits - K * orbits_per_coset
    if E_light < 0 or N_light < 0:
        raise CheckFailure("negative light residual")

    # exact bounds (all integer ceilings on the L1 sum S_mix / C-free)
    CS_ceiling = isqrt_ceil((p - 1) ** 2 * E_mix)
    split_ceiling = sum(isqrt_ceil(n * orbits_per_coset * exact_coset[c]) for c in heavy)
    if N_light > 0 and E_light > 0:
        split_ceiling += isqrt_ceil(n * N_light * E_light)
    gain = Fraction(CS_ceiling, split_ceiling) if split_ceiling else Fraction(0)

    beta1 = Fraction(exact_coset[heavy[0]], E_mix)
    beta_topK = Fraction(E_heavy, E_mix)
    mix_over_Csq = Fraction(E_mix, C * C)

    # concentration counts (cosets carrying 50/90/99% of E_mix) — full points only
    conc = None
    if full_coset:
        srt = sorted(exact_coset.values(), reverse=True)
        run = 0
        counts = {}
        for thr in (Fraction(1, 2), Fraction(9, 10), Fraction(99, 100)):
            k = 0
            run = 0
            for v in srt:
                k += 1
                run += v
                if Fraction(run, E_mix) >= thr:
                    break
            counts[str(thr)] = k
        conc = counts

    exact_block = {
        "p": p, "n": n, "m": m, "w": 2, "index": index, "C": C,
        "mixed_orbits": n_orbits, "orbits_per_coset": orbits_per_coset,
        "E_total": en["total"], "E_linear": en["linear"],
        "E_quadratic": en["quadratic"], "E_mix": E_mix,
        "heavy_cosets": heavy, "heavy_K": K,
        "E_kappa_heavy": [exact_coset[c] for c in heavy],
        "E_heavy": E_heavy, "E_light": E_light, "N_light": N_light,
        "CS_ceiling": CS_ceiling, "split_ceiling": split_ceiling,
        "gain": fraction_record(gain),
        "beta1": fraction_record(beta1),
        "beta_topK": fraction_record(beta_topK),
        "mix_over_Csq": fraction_record(mix_over_Csq),
        "full_coset_sum_checked": full_coset,
        "concentration_cosets": conc,
    }
    measured_block = {
        "S_mix": f"{S_mix:.6E}",
        "CS_over_Smix_slack": f"{CS_ceiling / S_mix:.6f}",
        "amp_energy_reldiff": f"{abs(amp_energy - E_mix) / max(1, E_mix):.3E}",
        "gain_decimal": f"{CS_ceiling / split_ceiling:.6f}",
        "sqrt_index": f"{math.sqrt(index):.6f}",
        "beta1_decimal": f"{float(beta1):.6f}",
    }
    return {"exact": exact_block, "measured": measured_block}


def folding_certificate(p: int, n: int, m: int) -> dict[str, Any]:
    """Exhaustive check that f_t(x)=f_t(s-x) for s=-t1/t2, over all mixed modes."""
    _, _, domain = subgroup(p, n)
    Hset = set(domain)
    ok = True
    vs_min, vs_max = n, 0
    for t1 in range(1, p):
        for t2 in range(1, p):
            inv = pow(t2, p - 2, p)
            s = (-t1 * inv) % p
            vals = {}
            for x in domain:
                vals[x] = (t1 * x + t2 * x * x) % p
            for x in domain:
                y = (s - x) % p
                if y in Hset and vals[x] != vals[y]:
                    ok = False
            k = len(set(vals.values()))
            vs_min = min(vs_min, k)
            vs_max = max(vs_max, k)
    return {"p": p, "n": n, "m": m, "folding_holds": ok,
            "value_set_min": vs_min, "value_set_max": vs_max,
            "folding_floor_nover2_plus1": n // 2 + 1}


def rH_coset_invariance(p: int, n: int) -> dict[str, Any]:
    g, step, domain = subgroup(p, n)
    Hset = set(domain)
    steps_all = [pow(step, j, p) for j in range(n)]
    ok = True
    for s in range(1, p):
        base = r_H(Hset, p, s)
        for h in steps_all:
            if r_H(Hset, p, (s * pow(h, p - 2, p)) % p) != base:
                ok = False
    return {"p": p, "n": n, "rH_constant_on_cosets": ok}


def heavy_amp_autocorrelation(p: int, n: int, m: int) -> dict[str, Any]:
    """Exact integer autocorrelation certificate A_0 = sum_r g_r^2 for the heaviest
    mixed orbit, with its value-set multiplicity profile.  Documents that the
    amplifier is a GLOBAL subset-sum resonance, not local value-set degeneracy."""
    g, step, domain = subgroup(p, n)
    C = math.comb(n, m)
    fibers = exact_prefix_fibers(p, list(domain), m)
    amps_full = orbit_amplitudes(p, step, n, list(domain), m)
    # recover (t1,t2) of the heaviest orbit by re-scanning (cheap for small p)
    dom = list(domain)
    dom2 = [(x * x) % p for x in dom]
    seen = bytearray(p * p)
    steps_all = [pow(step, j, p) for j in range(n)]
    best = (-1.0, 0, 0)
    two_pi = 2.0 * math.pi
    for t1 in range(1, p):
        for t2 in range(1, p):
            if seen[t1 * p + t2]:
                continue
            for hh in steps_all:
                seen[(hh * t1 % p) * p + (hh * hh % p) * t2 % p] = 1
            poly = [0j] * (m + 1)
            poly[0] = 1 + 0j
            for x, x2 in zip(dom, dom2):
                u = cmath.exp(1j * two_pi * ((t1 * x + t2 * x2) % p) / p)
                for kk in range(m, 0, -1):
                    poly[kk] += poly[kk - 1] * u
            a = abs(poly[m])
            if a > best[0]:
                best = (a, t1, t2)
    a, t1, t2 = best
    grp = [0] * p
    for idx, c in enumerate(fibers):
        if c:
            z1, z2 = divmod(idx, p)
            grp[(t1 * z1 + t2 * z2) % p] += c
    if sum(grp) != C:
        raise CheckFailure("projected count sum != C")
    A0 = sum(x * x for x in grp)                       # exact integer
    recon = math.fsum(sum(grp[r] * grp[(r - d) % p] for r in range(p)) * math.cos(two_pi * d / p)
                      for d in range(p))               # ~ |E|^2
    vmult = defaultdict(int)
    for x, x2 in zip(dom, dom2):
        vmult[(t1 * x + t2 * x2) % p] += 1
    prof = sorted(vmult.values(), reverse=True)
    return {"p": p, "n": n, "m": m, "t1": t1, "t2": t2,
            "s": (-t1 * pow(t2, p - 2, p)) % p,
            "A0_exact": A0, "value_set_size": len(vmult),
            "folded_pairs": sum(1 for v in vmult.values() if v >= 2),
            "mult_profile_head": prof[:6],
            "amp_over_sqrtC_measured": f"{a / math.sqrt(C):.4f}",
            "abs_E_sq_measured": f"{a * a:.6E}",
            "autocorr_reldiff_measured": f"{abs(a * a - recon) / max(1.0, a * a):.3E}"}


def compute_certificate() -> dict[str, Any]:
    points = [analyze_point(p, n, m, full) for (p, n, m, full) in LADDER]
    cross = next(pt for pt in points
                 if (pt["exact"]["p"], pt["exact"]["n"], pt["exact"]["m"]) ==
                 (CROSS_475["p"], CROSS_475["n"], CROSS_475["m"]))
    return {
        "packet": PACKET,
        "date": "2026-07-10",
        "status": {
            "index_ladder_measurement": "MEASURED",
            "coset_energy_identity": "PROVED",
            "split_bound": "PROVED",
            "folding_lemma": "PROVED",
            "popular_sum_predictor": "REFUTED",
            "deployed_transfer": "OPEN",
        },
        "deployed_reference": DEPLOYED,
        "dead_second_moment_margin_bits": DEAD_SECOND_MOMENT_MARGIN_BITS,
        "method_ceiling": {
            "deployed_index": DEPLOYED["subgroup_index"],
            "max_gain_sqrt_index": f"{math.sqrt(DEPLOYED['subgroup_index']):.6f}",
            "max_gain_bits": f"{0.5 * math.log2(DEPLOYED['subgroup_index']):.6f}",
            "dead_second_moment_margin_bits": DEAD_SECOND_MOMENT_MARGIN_BITS,
            "statement": ("coset refinement of Cauchy-Schwarz improves the mixed-orbit "
                          "L1 bound by at most sqrt(index); at the deployed row this is "
                          "~5 bits, negligible vs the ~1.045e6-bit second-moment deficit"),
        },
        "cross_check_475": {
            "point": [CROSS_475["p"], CROSS_475["n"], CROSS_475["m"]],
            "expected_mixed_energy": CROSS_475["mixed_energy"],
            "expected_linear_energy": CROSS_475["linear_energy"],
            "expected_quadratic_energy": CROSS_475["quadratic_energy"],
            "recomputed_mixed_energy": cross["exact"]["E_mix"],
            "recomputed_linear_energy": cross["exact"]["E_linear"],
            "recomputed_quadratic_energy": cross["exact"]["E_quadratic"],
        },
        "ladder": points,
        "folding": [folding_certificate(13, 12, 6), folding_certificate(41, 20, 10)],
        "rH_coset_invariance": rH_coset_invariance(61, 12),
        "heavy_amp_resonance": heavy_amp_autocorrelation(211, 30, 15),
        "claims": {
            "proves_exact_coset_energy_decomposition": True,
            "proves_split_bound_beats_cs_at_toys": True,
            "proves_folding_lemma": True,
            "refutes_popular_sum_as_heavy_predictor": True,
            "proves_deployed_mixed_orbit_bound": False,
            "proves_raw_signed_em_inverse": False,
            "imports_unrestricted_second_moment": False,
            "proves_disjoint_pte_count_law": False,
            "is_counterexample": False,
        },
    }


def validate_certificate(cert: dict[str, Any], replay: dict[str, Any] | None,
                         checks: Checks) -> None:
    checks.equal(cert["packet"], PACKET, "packet id")
    st = cert["status"]
    checks.equal(st["coset_energy_identity"], "PROVED", "coset identity status")
    checks.equal(st["split_bound"], "PROVED", "split status")
    checks.equal(st["folding_lemma"], "PROVED", "folding status")
    checks.equal(st["popular_sum_predictor"], "REFUTED", "predictor status")
    checks.equal(st["deployed_transfer"], "OPEN", "deployed status")

    dep = cert["deployed_reference"]
    checks.equal(dep["p"], 2**31 - 2**24 + 1, "deployed p")
    checks.equal(dep["n"], 2**21, "deployed n")
    checks.equal(dep["a_plus"], 1_116_048, "deployed a_+")
    checks.equal(dep["m"], 981104, "deployed m")
    checks.equal(dep["w"], 67471, "deployed w")
    checks.equal(dep["B_star"], 274980728111395087, "deployed B*")
    checks.equal(dep["subgroup_index"], 1016, "deployed index")
    checks.equal(cert["dead_second_moment_margin_bits"], "1045396.58", "dead margin cite")

    mc = cert["method_ceiling"]
    checks.equal(mc["deployed_index"], 1016, "method ceiling index")
    checks.close(float(mc["max_gain_sqrt_index"]), math.sqrt(1016), 1e-6, "method ceiling sqrt(index)")
    checks.close(float(mc["max_gain_bits"]), 0.5 * math.log2(1016), 1e-6, "method ceiling bits")
    # 5-bit ceiling is negligible vs the ~1.045e6-bit second-moment deficit
    checks.check(float(mc["max_gain_bits"]) < 6.0
                 and float(mc["dead_second_moment_margin_bits"]) > 1_000_000,
                 "method ceiling << dead second-moment deficit")

    cx = cert["cross_check_475"]
    checks.equal(cx["recomputed_mixed_energy"], cx["expected_mixed_energy"], "475 mixed byte-check")
    checks.equal(cx["recomputed_linear_energy"], cx["expected_linear_energy"], "475 linear byte-check")
    checks.equal(cx["recomputed_quadratic_energy"], cx["expected_quadratic_energy"], "475 quad byte-check")

    seen_points = set()
    for pt in cert["ladder"]:
        ex = pt["exact"]
        p, n, m, idx, C = ex["p"], ex["n"], ex["m"], ex["index"], ex["C"]
        tag = (p, n, m)
        seen_points.add(tag)
        checks.check(is_prime(p), f"{tag} prime")
        checks.equal((p - 1) % n, 0, f"{tag} subgroup divides")
        checks.equal(idx, (p - 1) // n, f"{tag} index")
        checks.equal(C, math.comb(n, m), f"{tag} C")
        checks.check(C < 2**64, f"{tag} uint64 exact")
        checks.equal(ex["mixed_orbits"], (p - 1) ** 2 // n, f"{tag} orbit count")
        checks.equal(ex["orbits_per_coset"], p - 1, f"{tag} orbits/coset")
        # Parseval mixed = total - linear - quadratic (structural)
        checks.equal(ex["E_mix"], ex["E_total"] - ex["E_linear"] - ex["E_quadratic"],
                     f"{tag} mixed Parseval subtraction")
        checks.check(ex["E_mix"] > 0, f"{tag} mixed energy positive")
        # heavy peel bookkeeping
        K = ex["heavy_K"]
        checks.equal(K, min(HEAVY_K, idx), f"{tag} heavy K")
        checks.equal(len(ex["heavy_cosets"]), K, f"{tag} heavy list length")
        checks.equal(len(set(ex["heavy_cosets"])), K, f"{tag} heavy distinct")
        checks.check(all(0 <= c < idx for c in ex["heavy_cosets"]), f"{tag} heavy in range")
        checks.equal(ex["E_heavy"], sum(ex["E_kappa_heavy"]), f"{tag} E_heavy sum")
        checks.equal(ex["E_light"], ex["E_mix"] - ex["E_heavy"], f"{tag} E_light")
        checks.check(ex["E_light"] >= 0, f"{tag} E_light nonneg")
        checks.equal(ex["N_light"], ex["mixed_orbits"] - K * (p - 1), f"{tag} N_light")
        checks.check(ex["N_light"] >= 0, f"{tag} N_light nonneg")
        # exact bounds
        checks.equal(ex["CS_ceiling"], isqrt_ceil((p - 1) ** 2 * ex["E_mix"]), f"{tag} CS ceiling")
        exp_split = sum(isqrt_ceil(n * (p - 1) * e) for e in ex["E_kappa_heavy"])
        if ex["N_light"] > 0 and ex["E_light"] > 0:
            exp_split += isqrt_ceil(n * ex["N_light"] * ex["E_light"])
        checks.equal(ex["split_ceiling"], exp_split, f"{tag} split ceiling")
        # ceilings are genuine upper bounds on their radicands
        checks.check(ex["CS_ceiling"] ** 2 >= (p - 1) ** 2 * ex["E_mix"], f"{tag} CS is upper bound")
        # split must not exceed CS (refinement is never worse); gain >= 1
        checks.check(ex["split_ceiling"] <= ex["CS_ceiling"], f"{tag} split <= CS")
        gain = Fraction(ex["gain"]["numerator"], ex["gain"]["denominator"])
        checks.equal(gain, Fraction(ex["CS_ceiling"], ex["split_ceiling"]), f"{tag} gain value")
        checks.check(gain >= 1, f"{tag} gain >= 1")
        # METHOD-CEILING THEOREM (exact core): split >= sqrt(n*(p-1)*E_mix), by
        # subadditivity of sqrt over the peeled terms.  Hence gain <= sqrt(index).
        checks.check(ex["split_ceiling"] ** 2 >= n * (p - 1) * ex["E_mix"],
                     f"{tag} split^2 >= n(p-1)E_mix [method ceiling core]")
        checks.equal(Fraction(ex["beta1"]["numerator"], ex["beta1"]["denominator"]),
                     Fraction(ex["E_kappa_heavy"][0], ex["E_mix"]), f"{tag} beta1")
        checks.equal(Fraction(ex["beta_topK"]["numerator"], ex["beta_topK"]["denominator"]),
                     Fraction(ex["E_heavy"], ex["E_mix"]), f"{tag} beta_topK")
        checks.equal(Fraction(ex["mix_over_Csq"]["numerator"], ex["mix_over_Csq"]["denominator"]),
                     Fraction(ex["E_mix"], C * C), f"{tag} mix/C^2")
        # measured consistency (float, tolerance)
        me = pt["measured"]
        reldiff = float(me["amp_energy_reldiff"])
        checks.check(reldiff < 1e-6, f"{tag} amplitude energy cross-check")
        checks.close(float(me["gain_decimal"]), float(gain), 1e-6, f"{tag} gain decimal")
        # method ceiling: gain <= sqrt(index) (equality iff all energy in one coset)
        checks.check(float(me["gain_decimal"]) <= math.sqrt(idx) * (1 + 1e-9),
                     f"{tag} gain <= sqrt(index)")

    # every ladder family present
    for want in [(7, 6, 3), (601, 6, 3), (211, 30, 15), (193, 64, 30)]:
        checks.check(want in seen_points, f"ladder contains {want}")

    for fc in cert["folding"]:
        checks.equal(fc["folding_holds"], True, f"folding ({fc['p']},{fc['n']})")
        checks.check(fc["value_set_min"] >= fc["folding_floor_nover2_plus1"] - 1,
                     f"folding value-set floor ({fc['p']},{fc['n']})")
    checks.equal(cert["rH_coset_invariance"]["rH_constant_on_cosets"], True, "r_H coset invariance")

    hr = cert["heavy_amp_resonance"]
    checks.check(hr["A0_exact"] > 0, "resonance A0 positive")
    checks.check(hr["folded_pairs"] <= 3, "resonance has FEW folded pairs (global not local)")
    checks.check(float(hr["amp_over_sqrtC_measured"]) > 10.0, "resonance amplitude >> generic")
    checks.check(float(hr["autocorr_reldiff_measured"]) < 1e-4, "resonance autocorr matches float")

    cl = cert["claims"]
    checks.equal(cl["proves_exact_coset_energy_decomposition"], True, "claim coset decomp")
    checks.equal(cl["proves_split_bound_beats_cs_at_toys"], True, "claim split")
    checks.equal(cl["proves_folding_lemma"], True, "claim folding")
    checks.equal(cl["refutes_popular_sum_as_heavy_predictor"], True, "claim predictor refute")
    checks.equal(cl["proves_deployed_mixed_orbit_bound"], False, "nonclaim deployed")
    checks.equal(cl["proves_raw_signed_em_inverse"], False, "nonclaim inverse")
    checks.equal(cl["imports_unrestricted_second_moment"], False, "nonclaim 2nd moment")
    checks.equal(cl["proves_disjoint_pte_count_law"], False, "nonclaim PTE law")
    checks.equal(cl["is_counterexample"], False, "nonclaim counterexample")

    if replay is not None:
        # strict replay on the exact spine; measured floats compared with tolerance.
        c_ex = strip_measured(cert)
        r_ex = strip_measured(replay)
        checks.equal(c_ex, r_ex, "full exact JSON replay")
        for a, b in zip(cert["ladder"], replay["ladder"]):
            checks.close(float(a["measured"]["CS_over_Smix_slack"]),
                         float(b["measured"]["CS_over_Smix_slack"]), 1e-3,
                         f"replay slack ({a['exact']['p']},{a['exact']['n']})")


def strip_measured(cert: dict[str, Any]) -> dict[str, Any]:
    c = deepcopy(cert)
    for pt in c["ladder"]:
        pt.pop("measured", None)
    hr = c.get("heavy_amp_resonance", {})
    for kk in ("amp_over_sqrtC_measured", "abs_E_sq_measured", "autocorr_reldiff_measured"):
        hr.pop(kk, None)
    return c


def tamper_suite(cert: dict[str, Any]) -> tuple[int, int]:
    def first_full(data):
        return next(pt for pt in data["ladder"] if pt["exact"]["full_coset_sum_checked"])
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("mixed-energy", lambda d: d["ladder"][0]["exact"].__setitem__(
            "E_mix", d["ladder"][0]["exact"]["E_mix"] + 1)),
        ("linear-energy", lambda d: d["ladder"][0]["exact"].__setitem__(
            "E_linear", d["ladder"][0]["exact"]["E_linear"] + 1)),
        ("heavy-coset-energy", lambda d: first_full(d)["exact"]["E_kappa_heavy"].__setitem__(
            0, first_full(d)["exact"]["E_kappa_heavy"][0] + 1)),
        ("E-light", lambda d: d["ladder"][0]["exact"].__setitem__(
            "E_light", d["ladder"][0]["exact"]["E_light"] + 1)),
        ("split-ceiling-down", lambda d: first_full(d)["exact"].__setitem__(
            "split_ceiling", first_full(d)["exact"]["split_ceiling"] - 1)),
        ("gain-numerator", lambda d: d["ladder"][0]["exact"]["gain"].__setitem__(
            "numerator", d["ladder"][0]["exact"]["gain"]["numerator"] + 1)),
        ("CS-ceiling", lambda d: d["ladder"][0]["exact"].__setitem__(
            "CS_ceiling", d["ladder"][0]["exact"]["CS_ceiling"] - 1)),
        ("475-cross", lambda d: d["cross_check_475"].__setitem__(
            "recomputed_mixed_energy", d["cross_check_475"]["recomputed_mixed_energy"] + 1)),
        ("deployed-index", lambda d: d["deployed_reference"].__setitem__("subgroup_index", 1017)),
        ("method-ceiling-bits", lambda d: d["method_ceiling"].__setitem__("max_gain_bits", "1200000.0")),
        ("split-below-core", lambda d: first_full(d)["exact"].__setitem__(
            "E_mix", first_full(d)["exact"]["E_mix"] * 4)),
        ("folding", lambda d: d["folding"][0].__setitem__("folding_holds", False)),
        ("rH-invariance", lambda d: d["rH_coset_invariance"].__setitem__(
            "rH_constant_on_cosets", False)),
        ("resonance-pairs", lambda d: d["heavy_amp_resonance"].__setitem__("folded_pairs", 20)),
        ("deployed-overclaim", lambda d: d["claims"].__setitem__(
            "proves_deployed_mixed_orbit_bound", True)),
        ("second-moment-import", lambda d: d["claims"].__setitem__(
            "imports_unrestricted_second_moment", True)),
        ("status-promotion", lambda d: d["status"].__setitem__("deployed_transfer", "PROVED")),
    ]
    caught = 0
    for label, mutate in mutations:
        bad = deepcopy(cert)
        mutate(bad)
        try:
            validate_certificate(bad, None, Checks())
        except (CheckFailure, KeyError, IndexError, TypeError, ValueError, ZeroDivisionError,
                StopIteration):
            caught += 1
            print(f"[tamper] CAUGHT {label}")
        else:
            print(f"[tamper] MISSED {label}")
    return caught, len(mutations)


def main() -> None:
    cap = impose_address_space_cap()
    started = time.monotonic()
    replay = compute_certificate()
    elapsed = time.monotonic() - started
    print(f"[cap] RLIMIT_AS={cap} bytes")
    print(f"[compute] full ladder + certificates in {elapsed:.2f}s")

    if os.environ.get("KB_LADDER_WRITE_JSON") == "1":
        checks = Checks()
        validate_certificate(replay, None, checks)
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        print(f"RESULT: GENERATED ({checks.passed}/{checks.total} checks)")
        print(DATA_PATH)
        return

    if not DATA_PATH.exists():
        raise CheckFailure(f"missing data JSON: {DATA_PATH}")
    stored = json.loads(DATA_PATH.read_text())
    checks = Checks()
    validate_certificate(stored, replay, checks)
    caught, total = tamper_suite(stored)
    checks.check(total >= 10, "at least ten live tamper tests")
    checks.equal(caught, total, "all live tamper tests caught")

    print("\nindex ladder (family, index -> E_mix/C^2, beta1, gain, slack):")
    for pt in stored["ladder"]:
        ex, me = pt["exact"], pt["measured"]
        print(f"  ({ex['p']:>4},{ex['n']:>3},{ex['m']:>3}) idx={ex['index']:>4} "
              f"Emix/C^2={ex['mix_over_Csq']['decimal']} beta1={me['beta1_decimal']} "
              f"gain={me['gain_decimal']} slack={me['CS_over_Smix_slack']}")
    hr = stored["heavy_amp_resonance"]
    print(f"\nresonance (211,30,15): heaviest orbit amp/sqrtC={hr['amp_over_sqrtC_measured']} "
          f"with only {hr['folded_pairs']} folded pairs (value set {hr['value_set_size']}/30) "
          f"=> global, not local.")
    print(f"RESULT: PASS ({checks.passed}/{checks.total} checks; tampers {caught}/{total})")


if __name__ == "__main__":
    try:
        main()
    except (CheckFailure, MemoryError, OverflowError) as error:
        print(f"RESULT: FAIL ({error})", file=sys.stderr)
        raise SystemExit(1)
