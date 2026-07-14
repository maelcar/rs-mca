#!/usr/bin/env python3
"""Exact certificate for the ell=7 two-sector vacancy cell.

The cell is (tau,m,ell)=(5,6,7), hence D=m-tau-1=0.  For a
full-petal codeword with exactly two active nonzero DFT sectors, every core
coset is live.  The affine group AGL(1,7) has two orbits on three-element
exponent supports:

    narrow: {0,1,2}, cyclic width 2;
    wide:   {0,1,3}, cyclic width 3.

The width theorem already makes the narrow orbit contribute at most two retained points
per core coset.  For the wide orbit, three roots of A+B X+C X^3 on mu_7
would have sum zero.  After normalizing one root, this would give

    1 + zeta^u + zeta^v = 0,  1 <= u < v <= 6.

The script computes, over the integers, every resultant

    Res(Phi_7, 1+X^u+X^v)

as a Sylvester determinant evaluated by fraction-free Bareiss elimination.
They are all 1 or 8.  A prime p congruent to 1 modulo 7 is odd, so none
vanishes modulo p.  Consequently the wide orbit also has at most two roots.
The retained core is therefore at most 6*2=12 points, below the exact list
requirement 2*7=14.

Finite-field exhaustions are auxiliary smoke tests; the integer-resultant
argument, not the tested prime list, supplies the uniform theorem.
"""

from __future__ import annotations

import itertools
import json
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
ARTIFACT = DATA / "ell7_two_sector_vacancy.json"


ELL = 7
TAU = 5
CORE_COSETS = 6
EXPECTED_RESULTANTS = {
    (1, 2): 1,
    (1, 3): 8,
    (1, 4): 1,
    (1, 5): 8,
    (1, 6): 1,
    (2, 3): 8,
    (2, 4): 1,
    (2, 5): 1,
    (2, 6): 8,
    (3, 4): 1,
    (3, 5): 1,
    (3, 6): 1,
    (4, 5): 8,
    (4, 6): 8,
    (5, 6): 1,
}


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def prime_factors(value: int) -> list[int]:
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
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root not found")


def polynomial_descending(exponents: set[int]) -> list[int]:
    """Return a monic/0-1 polynomial's coefficients in descending order."""

    degree = max(exponents)
    return [int(power in exponents) for power in range(degree, -1, -1)]


def sylvester_matrix(first: list[int], second: list[int]) -> list[list[int]]:
    """Build the Sylvester matrix for descending coefficient vectors."""

    first_degree = len(first) - 1
    second_degree = len(second) - 1
    size = first_degree + second_degree
    rows: list[list[int]] = []
    for shift in range(second_degree):
        rows.append([0] * shift + first + [0] * (second_degree - 1 - shift))
    for shift in range(first_degree):
        rows.append([0] * shift + second + [0] * (first_degree - 1 - shift))
    assert len(rows) == size and all(len(row) == size for row in rows)
    return rows


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Exact fraction-free determinant, with integral divisions asserted."""

    size = len(matrix)
    assert size > 0 and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous_pivot = 1
    for column in range(size - 1):
        if work[column][column] == 0:
            swap = next(
                (row for row in range(column + 1, size) if work[row][column] != 0),
                None,
            )
            if swap is None:
                return 0
            work[column], work[swap] = work[swap], work[column]
            sign *= -1
        pivot = work[column][column]
        for row in range(column + 1, size):
            for col in range(column + 1, size):
                numerator = work[row][col] * pivot - work[row][column] * work[column][col]
                quotient, remainder = divmod(numerator, previous_pivot)
                assert remainder == 0, "Bareiss division lost exactness"
                work[row][col] = quotient
        for row in range(column + 1, size):
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def resultant(first: list[int], second: list[int]) -> int:
    return bareiss_determinant(sylvester_matrix(first, second))


def affine_canonical(support: tuple[int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int]]:
    rows = []
    for unit in range(1, ELL):
        for shift in range(ELL):
            image = tuple(sorted((unit * exponent + shift) % ELL for exponent in support))
            rows.append((image, (unit, shift)))
    return min(rows)


def cyclic_span(support: tuple[int, int, int]) -> int:
    points = sorted(support)
    gaps = [
        points[1] - points[0],
        points[2] - points[1],
        ELL - points[2] + points[0],
    ]
    return ELL - max(gaps)


def affine_orbit_rows() -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    all_supports = list(itertools.combinations(range(ELL), 3))
    orbit_members: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}
    for support in all_supports:
        canonical, _ = affine_canonical(support)
        orbit_members.setdefault(canonical, []).append(support)

    orbit_summary = {
        "orbit_count": len(orbit_members),
        "orbits": [
            {
                "canonical": canonical,
                "size": len(members),
                "minimum_cyclic_span": min(cyclic_span(member) for member in members),
            }
            for canonical, members in sorted(orbit_members.items())
        ],
    }

    pair_rows = []
    for first, second in itertools.combinations(range(1, ELL), 2):
        canonical, witness = affine_canonical((0, first, second))
        pair_rows.append(
            {
                "sectors": [first, second],
                "canonical_support": canonical,
                "class": "narrow" if canonical == (0, 1, 2) else "wide",
                "affine_witness_unit_shift": witness,
            }
        )

    ratio_rows = []
    for ratio in range(2, ELL):
        canonical, witness = affine_canonical((0, 1, ratio))
        ratio_rows.append(
            {
                "ratio": ratio,
                "canonical_support": canonical,
                "class": "narrow" if canonical == (0, 1, 2) else "wide",
                "affine_witness_unit_shift": witness,
            }
        )
    return pair_rows, ratio_rows, orbit_summary


def resultant_rows() -> list[dict[str, object]]:
    phi7 = polynomial_descending(set(range(ELL)))
    rows = []
    for first, second in itertools.combinations(range(1, ELL), 2):
        trinomial = polynomial_descending({0, first, second})
        value = resultant(phi7, trinomial)
        rows.append(
            {
                "u": first,
                "v": second,
                "sylvester_size": (ELL - 1) + second,
                "resultant": value,
                "absolute_resultant": abs(value),
                "expected": EXPECTED_RESULTANTS[(first, second)],
                "matches_expected": value == EXPECTED_RESULTANTS[(first, second)],
            }
        )
    return rows


def projective_live_coefficients(prime: int):
    """One representative of every [A:B:C] with (B,C)!=(0,0)."""

    for second in range(prime):
        for third in range(prime):
            if second != 0 or third != 0:
                yield (1, second, third)
    for third in range(prime):
        yield (0, 1, third)
    yield (0, 0, 1)


def finite_field_row(prime: int) -> dict[str, object]:
    assert is_prime(prime) and (prime - 1) % ELL == 0
    generator = primitive_root(prime)
    zeta = pow(generator, (prime - 1) // ELL, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ELL)]
    coefficient_rows = list(projective_live_coefficients(prime))
    ratio_rows = []
    total_tests = 0
    violations = 0
    for ratio in range(2, ELL):
        powers = [pow(point, ratio, prime) for point in subgroup]
        max_roots = -1
        max_witness = None
        bound = 2
        for constant, linear, high in coefficient_rows:
            roots = sum(
                1
                for point, point_power in zip(subgroup, powers)
                if (constant + linear * point + high * point_power) % prime == 0
            )
            total_tests += 1
            if roots > max_roots:
                max_roots = roots
                max_witness = [constant, linear, high]
            if roots > bound:
                violations += 1
        canonical, _ = affine_canonical((0, 1, ratio))
        ratio_rows.append(
            {
                "ratio": ratio,
                "class": "narrow" if canonical == (0, 1, 2) else "wide",
                "projective_live_polynomials": len(coefficient_rows),
                "max_roots": max_roots,
                "max_root_witness": max_witness,
                "within_two_root_bound": max_roots <= bound,
            }
        )

    quotient_cosets = (prime - 1) // ELL
    required_cosets = TAU + CORE_COSETS
    return {
        "p": prime,
        "p_is_prime": is_prime(prime),
        "p_mod_7": prime % ELL,
        "generator": generator,
        "subgroup_size": len(set(subgroup)),
        "quotient_cosets": quotient_cosets,
        "required_distinct_petal_plus_core_cosets": required_cosets,
        "cell_available_in_Fp_star": quotient_cosets >= required_cosets,
        "ratio_rows": ratio_rows,
        "total_projective_root_tests": total_tests,
        "violations": violations,
        "pass": len(set(subgroup)) == ELL and violations == 0,
    }


def run() -> dict[str, object]:
    upstream = UPSTREAM_NOTE.read_text(encoding="utf-8")
    pair_rows, ratio_rows, orbit_summary = affine_orbit_rows()
    exact_resultants = resultant_rows()
    # The first three fields test the algebra in geometrically unavailable
    # small ambient groups; the last three actually contain 5+6 distinct
    # mu_7-cosets and therefore realize the whole sunflower cell.
    field_rows = [finite_field_row(prime) for prime in (29, 43, 71, 113, 127, 197)]

    dead_coset_degree = CORE_COSETS - TAU - 1
    live_core_cosets = CORE_COSETS - dead_coset_degree
    retained_bound = live_core_cosets * 2
    listing_core_requirement = (dead_coset_degree + 2) * ELL
    narrow_pairs = sum(row["class"] == "narrow" for row in pair_rows)
    wide_pairs = sum(row["class"] == "wide" for row in pair_rows)
    available_fields = [row["p"] for row in field_rows if row["cell_available_in_Fp_star"]]

    checks = {
        "upstream_explicitly_leaves_two_or_more_sectors_open": "The residual danger is `|S| >= 2`" in upstream,
        "agl_has_exactly_two_three_support_orbits": orbit_summary["orbit_count"] == 2,
        "agl_orbit_sizes_are_21_and_14": sorted(row["size"] for row in orbit_summary["orbits"]) == [14, 21],
        "all_15_nonzero_sector_pairs_classified": len(pair_rows) == 15 and narrow_pairs + wide_pairs == 15,
        "sector_pair_split_is_9_narrow_6_wide": (narrow_pairs, wide_pairs) == (9, 6),
        "normalized_narrow_ratios_are_2_4_6": [row["ratio"] for row in ratio_rows if row["class"] == "narrow"] == [2, 4, 6],
        "normalized_wide_ratios_are_3_5": [row["ratio"] for row in ratio_rows if row["class"] == "wide"] == [3, 5],
        "all_15_bareiss_resultants_match_exact_table": all(row["matches_expected"] for row in exact_resultants),
        "all_resultants_are_units_or_powers_of_two": {row["absolute_resultant"] for row in exact_resultants} == {1, 8},
        "no_tested_admissible_prime_divides_a_resultant": all(
            all(int(resultant_row["resultant"]) % int(field_row["p"]) != 0 for resultant_row in exact_resultants)
            for field_row in field_rows
        ),
        "D_is_zero_so_every_core_coset_is_live": dead_coset_degree == 0 and live_core_cosets == CORE_COSETS,
        "retained_bound_is_strictly_below_list_requirement": retained_bound == 12 and listing_core_requirement == 14 and retained_bound < listing_core_requirement,
        "finite_field_exhaustions_have_no_root_violation": all(row["pass"] for row in field_rows),
        "finite_field_suite_contains_three_available_cells": len(available_fields) >= 3,
    }

    return {
        "title": "Complete exact-two-sector vacancy at (tau,m,ell)=(5,6,7)",
        "status": "PROVED_LOCAL",
        "verdict": "PASS_WITH_ELL7_TWO_SECTOR_COMPLETE_VACANCY",
        "theorem": (
            "Let p be prime with p congruent to 1 modulo 7. In a background-free "
            "mu_7-coset sunflower with tau=5 petals and m=6 core cosets, no listed "
            "full-petal codeword has exactly two active nonzero DFT sectors. Thus the "
            "exact-two-sector stratum contributes no mixed minimal kernel set, primitive "
            "or otherwise. The statement is vacuous when F_p^* has fewer "
            "than 11 distinct mu_7-cosets."
        ),
        "proof_steps": [
            "Here D=m-tau-1=0. Each active sector quotient g_r=P_r/phi is a nonzero constant, so all six core cosets are live.",
            "AGL(1,7) has exactly two orbits on three-exponent supports: narrow {0,1,2} and wide {0,1,3}. The 15 pairs of nonzero sectors split as 9 narrow and 6 wide pairs.",
            "The narrow orbit has cyclic width two, so the monomial-rotation argument gives at most two retained mu_7-points per live core coset.",
            "For the wide orbit, after a unit-power substitution and a nonvanishing monomial rotation, the restriction has support {0,1,3}. Binomial boundary cases have at most one root.",
            "If A+B X+C X^3 with ABC nonzero had three distinct roots x,y,z in mu_7, its missing X^2 coefficient would force x+y+z=0. Dividing by x gives 1+zeta^u+zeta^v=0 for distinct 1<=u<v<=6.",
            "Exact Sylvester/Bareiss determinants give Res(Phi_7,1+X^u+X^v) in {1,8} for all 15 pairs. Since p congruent to 1 modulo 7 is odd, p divides none of them, so the three-root relation is impossible in every admissible characteristic.",
            "Every one of the six core cosets therefore retains at most two points: retained<=12. Listing requires retained>=(D+2)ell=14, a contradiction.",
        ],
        "parameters": {
            "tau": TAU,
            "m": CORE_COSETS,
            "ell": ELL,
            "D": dead_coset_degree,
            "live_core_cosets": live_core_cosets,
            "retained_upper_bound": retained_bound,
            "listing_core_requirement": listing_core_requirement,
        },
        "affine_orbits": orbit_summary,
        "sector_pair_rows": pair_rows,
        "normalized_ratio_rows": ratio_rows,
        "resultant_rows": exact_resultants,
        "finite_field_rows": field_rows,
        "available_test_fields": available_fields,
        "uniformity": (
            "The theorem is uniform over every prime p congruent to 1 modulo 7: "
            "the load-bearing certificate is the integer resultant set {1,8}. "
            "Finite-field enumeration is only a regression and normalization check."
        ),
        "availability": (
            "The background-free cell needs tau+m=11 distinct mu_7-cosets. "
            "Inside F_p^* this requires (p-1)/7>=11. Small tested primes may be "
            "algebraically admissible but geometrically unavailable; p=113,127,197 "
            "are tested available examples."
        ),
        "scope": (
            "Closes the exact-two-active-sector stratum only at (tau,m,ell)=(5,6,7). "
            "It is not a vacancy theorem for the whole parameter cell and does not "
            "exclude any witness with three or more active sectors (including a "
            "six-sector witness), other ell, or the large-tau/wide-pair residual in general."
        ),
        "upstream": {
            "source": UPSTREAM_NOTE.relative_to(ROOT).as_posix(),
            "collision": "No ell=7 wide-pair resultant closure found; upstream leaves |S|>=2 open.",
        },
        "next_obligation": (
            "Generalize the arithmetic root cap nu_{p,ell}(r,s) with a resultant/Fourier-minor "
            "sieve, or attack the first three-active-sector cell at ell=7."
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> int:
    out = run()
    ARTIFACT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    resultants = sorted({int(row["absolute_resultant"]) for row in out["resultant_rows"]})
    tests = sum(int(row["total_projective_root_tests"]) for row in out["finite_field_rows"])
    violations = sum(int(row["violations"]) for row in out["finite_field_rows"])
    parameters = out["parameters"]
    print(out["title"])
    print(
        f"agl_orbits={out['affine_orbits']['orbit_count']} sector_pairs={len(out['sector_pair_rows'])} "
        f"resultants={resultants}"
    )
    print(
        f"field_projective_tests={tests} root_violations={violations} "
        f"available_test_fields={out['available_test_fields']}"
    )
    print(
        f"retained_bound={parameters['retained_upper_bound']} "
        f"listing_requirement={parameters['listing_core_requirement']}"
    )
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
