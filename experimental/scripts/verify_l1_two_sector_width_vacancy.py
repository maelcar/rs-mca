#!/usr/bin/env python3
"""Exact certificate for the two-active-sector width vacancy theorem.

For prime ell, normalize two nonzero DFT sectors r,s to exponents 1,e on
mu_ell.  The zero set of A+B h+C h^e is unchanged by affine transformations
of the exponent triple {0,1,e}.  Its minimal cyclic span delta_ell(e) is an
exact degree bound for every live core coset.

If a full-petal word has tau petals, m core cosets, and exactly two active
nonzero sectors, at most D=m-tau-1 core cosets are dead.  Hence

    retained <= D*ell + (tau+1)*delta,

while listing requires (D+2)*ell retained points.  Thus

    (tau+1)*delta < 2*ell

forces vacancy.  The script verifies the exponent compression, exact root
counts on finite fields, and the retention arithmetic.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
UPSTREAM_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
ARTIFACT = DATA / "two_sector_width_vacancy.json"


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def cyclic_span_three(first: int, second: int, ell: int) -> int:
    points = sorted((0, first % ell, second % ell))
    gaps = (
        points[1] - points[0],
        points[2] - points[1],
        ell - points[2] + points[0],
    )
    return ell - max(gaps)


def sector_delta(ell: int, ratio: int) -> tuple[int, int]:
    rows = [
        (cyclic_span_three(multiplier, multiplier * ratio, ell), multiplier)
        for multiplier in range(1, ell)
    ]
    return min(rows)


def ceil_sqrt(value: int) -> int:
    root = math.isqrt(value)
    return root if root * root == value else root + 1


def dirichlet_bound(ell: int) -> int:
    q = ceil_sqrt(ell)
    return q + ell // (q + 1)


def primitive_root(prime: int) -> int:
    value = prime - 1
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root not found")


def exhaustive_root_row(prime: int, ell: int) -> dict[str, object]:
    generator = primitive_root(prime)
    zeta = pow(generator, (prime - 1) // ell, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    ratio_rows = []
    total_polynomials = 0
    single_active_polynomials = 0
    violations = 0
    single_active_violations = 0
    for ratio in range(2, ell):
        delta, multiplier = sector_delta(ell, ratio)
        max_roots = 0
        witness = None
        powers = [pow(point, ratio, prime) for point in subgroup]
        # Normalize B=1 when both active coefficients are live. Scaling a
        # nonzero polynomial does not change its zero set.
        for constant in range(prime):
            for coefficient in range(1, prime):
                roots = sum(
                    1
                    for point, point_power in zip(subgroup, powers)
                    if (constant + point + coefficient * point_power) % prime == 0
                )
                total_polynomials += 1
                if roots > max_roots:
                    max_roots = roots
                    witness = (constant, coefficient)
                if roots > delta:
                    violations += 1
        # Boundary live cosets with only one of B,C nonzero.  Because every
        # nonzero exponent is a unit modulo prime ell, both monomial maps
        # permute mu_ell and every such binomial has at most one root.
        for constant in range(prime):
            for coefficient in range(1, prime):
                roots_b_only = sum(
                    1 for point in subgroup if (constant + coefficient * point) % prime == 0
                )
                roots_c_only = sum(
                    1
                    for point_power in powers
                    if (constant + coefficient * point_power) % prime == 0
                )
                single_active_polynomials += 2
                if roots_b_only > 1 or roots_c_only > 1:
                    single_active_violations += 1
        ratio_rows.append(
            {
                "ratio": ratio,
                "delta": delta,
                "minimizing_multiplier": multiplier,
                "max_roots_exhaustive": max_roots,
                "max_root_witness": witness,
                "within_delta": max_roots <= delta,
            }
        )
    return {
        "p": prime,
        "ell": ell,
        "generator": generator,
        "p_is_prime": is_prime(prime),
        "ell_divides_p_minus_one": (prime - 1) % ell == 0,
        "subgroup_size": len(set(subgroup)),
        "total_normalized_trinomials": total_polynomials,
        "single_active_binomials": single_active_polynomials,
        "violations": violations,
        "single_active_violations": single_active_violations,
        "max_roots_seen": max(int(row["max_roots_exhaustive"]) for row in ratio_rows),
        "max_delta": max(int(row["delta"]) for row in ratio_rows),
        "ratio_rows": ratio_rows,
        "pass": violations == 0
        and single_active_violations == 0
        and is_prime(prime)
        and (prime - 1) % ell == 0
        and len(set(subgroup)) == ell,
    }


def compression_row(ell: int) -> dict[str, object]:
    ratios = []
    for ratio in range(2, ell):
        delta, multiplier = sector_delta(ell, ratio)
        ratios.append(
            {
                "ratio": ratio,
                "delta": delta,
                "minimizing_multiplier": multiplier,
            }
        )
    max_delta = max(int(row["delta"]) for row in ratios)
    bound = dirichlet_bound(ell)
    tau_max = (2 * ell - 1) // max_delta - 1
    arithmetic_rows = []
    for tau in range(2, max(2, tau_max) + 1):
        for core_cosets in range(tau + 1, ell):
            dead_cap = core_cosets - tau - 1
            retained_bound = dead_cap * ell + (tau + 1) * max_delta
            listing_threshold = (dead_cap + 2) * ell
            arithmetic_rows.append(retained_bound < listing_threshold)
    return {
        "ell": ell,
        "prime": is_prime(ell),
        "ratio_rows": ratios,
        "max_delta": max_delta,
        "dirichlet_bound": bound,
        "delta_below_dirichlet_bound": max_delta <= bound,
        "universal_tau_max": tau_max,
        "covers_t_ge_5": tau_max >= 5,
        "all_retention_rows_strict": all(arithmetic_rows),
        "retention_rows": len(arithmetic_rows),
    }


def run() -> dict[str, object]:
    note = UPSTREAM_NOTE.read_text(encoding="utf-8")
    ell_values = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 83, 97, 127, 151, 181, 211, 251]
    compression = [compression_row(ell) for ell in ell_values]
    root_rows = [
        exhaustive_root_row(31, 5),
        exhaustive_root_row(71, 7),
        exhaustive_root_row(23, 11),
        exhaustive_root_row(53, 13),
        exhaustive_root_row(103, 17),
    ]

    checks = {
        "upstream_single_sector_theorem_present": (
            "Theorem B (single active sector" in note
            or "Theorem B (single active sector, all `ell`)" in note
        ),
        "upstream_leaves_multi_sector_residual": "|S| >= 2" in note,
        "all_ell_values_are_prime": all(row["prime"] for row in compression),
        "all_exact_deltas_meet_dirichlet_bound": all(
            row["delta_below_dirichlet_bound"] for row in compression
        ),
        "all_retention_arithmetic_is_strict": all(
            row["all_retention_rows_strict"] for row in compression
        ),
        "root_exhaustions_have_no_violation": all(row["pass"] for row in root_rows),
        "root_exhaustions_include_modular_three_root_case": any(
            int(row["max_roots_seen"]) >= 3 for row in root_rows
        ),
        "nontrivial_t_ge_5_coverage_exists": any(
            row["covers_t_ge_5"] for row in compression
        ),
    }

    return {
        "title": "Two-active-sector exponent-width vacancy theorem",
        "status": "PROVED_LOCAL",
        "verdict": "PASS_WITH_TWO_SECTOR_WIDTH_VACANCY_THEOREM",
        "theorem": (
            "Let ell be prime and a background-free coset sunflower have tau petals, "
            "m core cosets, and a full-petal codeword with exactly two nonzero active "
            "DFT sectors r,s. Let delta_ell(r,s) be the minimum cyclic span of the "
            "affine exponent triple u*{0,r,s}+v. If (tau+1)delta_ell(r,s)<2ell, "
            "the codeword is not listed. Consequently no primitive mixed minimal "
            "kernel set occurs in this two-sector width regime."
        ),
        "proof_steps": [
            "Exactly two active nonzero sectors force m>=tau+1 in the full-petal chart, so D=m-tau-1>=0.",
            "Full-petal agreement gives P_a(Y)=phi(Y)g_a(Y) for every active nonzero sector and deg g_a<=D=m-tau-1.",
            "The two nonzero g_r,g_s have at most D common core-label roots, so at most D core cosets are sector-dead. Assigning ell retained points to each is a deliberately pessimistic upper bound.",
            "On a live core coset the retained points are zeros on mu_ell of A+B h^r+C h^s with (B,C) not both zero.",
            "Substitution by a unit power and multiplication by a nonvanishing monomial turn this into a nonzero polynomial of degree at most delta_ell(r,s), hence at most delta_ell(r,s) roots.",
            "Thus retained<=D ell+(tau+1)delta, whereas listing requires (D+2)ell. The strict width inequality rules listing out.",
            "For Q=ceil(sqrt(ell)), order the Q+1 residues 0,e,...,Qe on the circle. Two consecutive residues have circular gap at most floor(ell/(Q+1)); their index difference u has 1<=|u|<=Q and is a unit because ell is prime. Hence delta<=Q+floor(ell/(Q+1)).",
        ],
        "compression_rows": compression,
        "root_exhaustion_rows": root_rows,
        "scope": (
            "Pays the exact two-active-sector chart only when the exponent-width "
            "inequality holds. Large tau or wide sector pairs remain open; no claim "
            "is made for three or more active sectors or for composite ell. The "
            "reported tau_max values are exact for the listed ell grid, not a claim "
            "that those same integers are uniform in all primes ell."
        ),
        "upstream": {
            "source": UPSTREAM_NOTE.relative_to(ROOT).as_posix(),
            "collision": "No two-active-sector width theorem found; the source leaves |S|>=2 open.",
        },
        "next_obligation": (
            "Attack the complementary wide-pair/large-tau two-sector chart using "
            "coupled trinomial incidences across cosets, or find an exact primitive listed witness."
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> int:
    out = run()
    ARTIFACT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    covered = [
        (row["ell"], row["max_delta"], row["universal_tau_max"])
        for row in out["compression_rows"]
        if row["covers_t_ge_5"]
    ]
    total_root_tests = sum(
        int(row["total_normalized_trinomials"]) + int(row["single_active_binomials"])
        for row in out["root_exhaustion_rows"]
    )
    print(out["title"])
    print(
        f"ell_rows={len(out['compression_rows'])} root_tests={total_root_tests} "
        f"root_violations={sum(int(row['violations']) + int(row['single_active_violations']) for row in out['root_exhaustion_rows'])}"
    )
    print(f"t_ge_5_covered_rows={len(covered)} last={covered[-1] if covered else None}")
    if not out["all_checks_pass"]:
        print("FAIL")
        for key, value in out["checks"].items():
            if not value:
                print("  -", key)
        return 1
    print(out["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
