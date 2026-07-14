#!/usr/bin/env python3
"""Exact certificate: complete two-sector vacancy for ell=11,13.

Let ell be 11 or 13, let tau>=5 and tau<m<ell, and work over F_p with
ell | p-1.  A full-petal word with exactly two active nonzero DFT sectors
has, on every live core coset, a restriction with three exponent slots.
After the AGL(1,ell) action on exponents its support is {0,1,e}.

Three distinct roots may similarly be written {1,zeta,zeta^w}, where zeta
is primitive of order ell.  The corresponding Fourier minor is

    D_{e,w}(X)
      = (X-1)(X^(e*w)-1) - (X^e-1)(X^w-1).

Its Vandermonde factor is

    V_w(X)=(X-1)(X^w-1)(X^w-X).

The script divides D by V exactly over Z[X] and computes every cyclotomic
resultant Res(Phi_ell,D/V) by a Sylvester matrix and fraction-free Bareiss
elimination.  The complete orbit tables are

    ell=11: [[1,1],   ell=13: [[1, 1,   1],
             [1,23]]           [1,53,  27],
                                [1,27, 729]].

The only prime factors congruent to one modulo ell are 23 (ell=11) and 53
(ell=13).  Their multiplicative groups contain only 2 and 4 mu_ell-cosets.
Every cell tau>=5, tau<m needs at least tau+m>=11 distinct cosets, so those
bad characteristics are geometrically unavailable.  Thus every realizable
cell has a two-root cap on every live coset.

With D=m-tau-1, at most D core cosets are sector-dead.  Hence

    retained <= D*ell + 2*(tau+1) < (D+2)*ell,

because tau<m<ell.  This rules out listing in the exact-two-sector stratum.

Finite-field exhaustions at p=331 (ell=11) and p=313 (ell=13) are auxiliary
smoke tests; both fields realize even the largest cell.  Exhaustions at the
two unavailable bad primes confirm that the geometric guard is load-bearing.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
UPSTREAM_RESIDUAL_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_MULTISECTOR_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_prime_ell_pv_refutation.md"
)
ARTIFACT = DATA / "ell11_13_two_sector_vacancy.json"


ELLS = (11, 13)
TAU_MIN = 5
SMOKE_FIELDS = {11: 331, 13: 313}
EXCEPTIONAL_FIELDS = {11: 23, 13: 53}
EXPECTED_ORBIT_SIZES = {
    11: {(0, 1, 2): 55, (0, 1, 3): 110},
    13: {(0, 1, 2): 78, (0, 1, 3): 156, (0, 1, 4): 52},
}
EXPECTED_RATIO_CLASSES = {
    11: {
        (0, 1, 2): [2, 6, 10],
        (0, 1, 3): [3, 4, 5, 7, 8, 9],
    },
    13: {
        (0, 1, 2): [2, 7, 12],
        (0, 1, 3): [3, 5, 6, 8, 9, 11],
        (0, 1, 4): [4, 10],
    },
}
EXPECTED_QUOTIENT_RESULTANTS = {
    11: {
        (2, 2): 1,
        (2, 3): 1,
        (3, 2): 1,
        (3, 3): 23,
    },
    13: {
        (2, 2): 1,
        (2, 3): 1,
        (2, 4): 1,
        (3, 2): 1,
        (3, 3): 53,
        (3, 4): 27,
        (4, 2): 1,
        (4, 3): 27,
        (4, 4): 729,
    },
}


def trim(polynomial: list[int]) -> list[int]:
    """Trim an ascending coefficient vector, retaining one zero."""

    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def monomial(exponent: int) -> list[int]:
    return [0] * exponent + [1]


def poly_add(first: list[int], second: list[int]) -> list[int]:
    out = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        out[index] += value
    for index, value in enumerate(second):
        out[index] += value
    return trim(out)


def poly_sub(first: list[int], second: list[int]) -> list[int]:
    return poly_add(first, [-value for value in second])


def poly_mul(first: list[int], second: list[int]) -> list[int]:
    out = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            out[first_index + second_index] += first_value * second_value
    return trim(out)


def exact_poly_division(dividend: list[int], divisor: list[int]) -> list[int]:
    """Exact Z[X] division for ascending coefficient vectors."""

    work = trim(dividend[:])
    divisor = trim(divisor[:])
    assert divisor != [0]
    if len(work) < len(divisor):
        raise AssertionError("nonzero remainder in exact polynomial division")
    quotient = [0] * (len(work) - len(divisor) + 1)
    while work != [0] and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient, remainder = divmod(work[-1], divisor[-1])
        assert remainder == 0, "nonintegral polynomial quotient"
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[index + shift] -= coefficient * value
        trim(work)
    assert work == [0], "nonzero remainder in exact polynomial division"
    return trim(quotient)


def fourier_minor_polynomial(exponent_ratio: int, root_ratio: int) -> list[int]:
    """D_{e,w}, in ascending order, from the symbolic 3x3 determinant."""

    first = poly_mul(
        poly_sub(monomial(1), [1]),
        poly_sub(monomial(exponent_ratio * root_ratio), [1]),
    )
    second = poly_mul(
        poly_sub(monomial(exponent_ratio), [1]),
        poly_sub(monomial(root_ratio), [1]),
    )
    return poly_sub(first, second)


def vandermonde_polynomial(root_ratio: int) -> list[int]:
    return poly_mul(
        poly_mul(
            poly_sub(monomial(1), [1]),
            poly_sub(monomial(root_ratio), [1]),
        ),
        poly_sub(monomial(root_ratio), monomial(1)),
    )


def sylvester_matrix(first: list[int], second: list[int]) -> list[list[int]]:
    """Sylvester matrix from descending coefficient vectors."""

    first_degree = len(first) - 1
    second_degree = len(second) - 1
    size = first_degree + second_degree
    assert size > 0
    rows = []
    for shift in range(second_degree):
        rows.append([0] * shift + first + [0] * (second_degree - 1 - shift))
    for shift in range(first_degree):
        rows.append([0] * shift + second + [0] * (first_degree - 1 - shift))
    assert len(rows) == size and all(len(row) == size for row in rows)
    return rows


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Exact fraction-free determinant with integral divisions asserted."""

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
                numerator = (
                    work[row][col] * pivot
                    - work[row][column] * work[column][col]
                )
                quotient, remainder = divmod(numerator, previous_pivot)
                assert remainder == 0, "Bareiss division lost exactness"
                work[row][col] = quotient
        for row in range(column + 1, size):
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def resultant(first_ascending: list[int], second_ascending: list[int]) -> int:
    return bareiss_determinant(
        sylvester_matrix(
            list(reversed(trim(first_ascending[:]))),
            list(reversed(trim(second_ascending[:]))),
        )
    )


def cyclotomic_prime_polynomial(ell: int) -> list[int]:
    return [1] * ell


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def prime_factorization(value: int) -> list[list[int]]:
    value = abs(value)
    factors: list[list[int]] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            multiplicity = 0
            while value % divisor == 0:
                value //= divisor
                multiplicity += 1
            factors.append([divisor, multiplicity])
        divisor += 1
    if value > 1:
        factors.append([value, 1])
    return factors


def affine_canonical(ell: int, support: tuple[int, int, int]) -> tuple[int, int, int]:
    return min(
        tuple(sorted((unit * exponent + shift) % ell for exponent in support))
        for unit in range(1, ell)
        for shift in range(ell)
    )


def orbit_data(ell: int) -> dict[str, object]:
    orbit_members: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}
    for support in itertools.combinations(range(ell), 3):
        canonical = affine_canonical(ell, support)
        orbit_members.setdefault(canonical, []).append(support)

    ratio_classes: dict[tuple[int, int, int], list[int]] = {}
    for ratio in range(2, ell):
        canonical = affine_canonical(ell, (0, 1, ratio))
        ratio_classes.setdefault(canonical, []).append(ratio)

    return {
        "orbit_count": len(orbit_members),
        "orbits": [
            {
                "canonical": list(canonical),
                "size": len(members),
                "normalized_ratios": ratio_classes[canonical],
                "representative_ratio": min(ratio_classes[canonical]),
            }
            for canonical, members in sorted(orbit_members.items())
        ],
        "ratio_class_map": {
            str(ratio): list(affine_canonical(ell, (0, 1, ratio)))
            for ratio in range(2, ell)
        },
    }


def exact_resultant_data(ell: int, orbits: dict[str, object]) -> dict[str, object]:
    phi = cyclotomic_prime_polynomial(ell)
    orbit_rows = list(orbits["orbits"])
    representative_by_class = {
        tuple(row["canonical"]): int(row["representative_ratio"])
        for row in orbit_rows
    }

    all_rows = []
    values_by_class_pair: dict[
        tuple[tuple[int, int, int], tuple[int, int, int]], set[int]
    ] = {}
    for exponent_ratio in range(2, ell):
        exponent_class = affine_canonical(ell, (0, 1, exponent_ratio))
        for root_ratio in range(2, ell):
            root_class = affine_canonical(ell, (0, 1, root_ratio))
            determinant = fourier_minor_polynomial(exponent_ratio, root_ratio)
            vandermonde = vandermonde_polynomial(root_ratio)
            quotient = exact_poly_division(determinant, vandermonde)
            raw_resultant = abs(resultant(phi, determinant))
            vandermonde_resultant = abs(resultant(phi, vandermonde))
            quotient_resultant = abs(resultant(phi, quotient))
            assert raw_resultant == vandermonde_resultant * quotient_resultant
            values_by_class_pair.setdefault((exponent_class, root_class), set()).add(
                quotient_resultant
            )
            all_rows.append(
                {
                    "exponent_ratio": exponent_ratio,
                    "root_ratio": root_ratio,
                    "exponent_class": list(exponent_class),
                    "root_class": list(root_class),
                    "determinant_degree": len(determinant) - 1,
                    "vandermonde_degree": len(vandermonde) - 1,
                    "quotient_degree": len(quotient) - 1,
                    "raw_resultant": raw_resultant,
                    "vandermonde_resultant": vandermonde_resultant,
                    "quotient_resultant": quotient_resultant,
                    "quotient_factorization": prime_factorization(quotient_resultant),
                }
            )

    table_rows = []
    for exponent_row in orbit_rows:
        exponent_class = tuple(exponent_row["canonical"])
        exponent_representative = representative_by_class[exponent_class]
        for root_row in orbit_rows:
            root_class = tuple(root_row["canonical"])
            root_representative = representative_by_class[root_class]
            values = values_by_class_pair[(exponent_class, root_class)]
            assert len(values) == 1
            value = next(iter(values))
            expected = EXPECTED_QUOTIENT_RESULTANTS[ell][
                (exponent_representative, root_representative)
            ]
            table_rows.append(
                {
                    "exponent_class": list(exponent_class),
                    "exponent_representative": exponent_representative,
                    "root_class": list(root_class),
                    "root_representative": root_representative,
                    "quotient_resultant": value,
                    "factorization": prime_factorization(value),
                    "all_normalized_pairs_in_class_agree": True,
                    "matches_expected": value == expected,
                }
            )

    external_prime_factors = sorted(
        {
            prime
            for row in table_rows
            for prime, _multiplicity in row["factorization"]
            if prime % ell == 1
        }
    )
    return {
        "all_normalized_pair_rows": all_rows,
        "orbit_resultant_table": table_rows,
        "external_admissible_prime_factors": external_prime_factors,
        "vandermonde_resultant_value": ell**3,
    }


def prime_factors(value: int) -> list[int]:
    return [prime for prime, _multiplicity in prime_factorization(value)]


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def projective_live_coefficients(prime: int):
    """One representative of every [A:B:C] with (B,C)!=(0,0)."""

    for linear in range(prime):
        for high in range(prime):
            if linear != 0 or high != 0:
                yield (1, linear, high)
    for high in range(prime):
        yield (0, 1, high)
    yield (0, 0, 1)


def finite_field_exhaustion(ell: int, prime: int, orbit_rows: list[dict[str, object]]) -> dict[str, object]:
    assert is_prime(prime) and (prime - 1) % ell == 0
    generator = primitive_root(prime)
    zeta = pow(generator, (prime - 1) // ell, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    rows = []
    total_polynomials = 0
    total_point_evaluations = 0
    for orbit in orbit_rows:
        exponent = int(orbit["representative_ratio"])
        high_powers = [pow(point, exponent, prime) for point in subgroup]
        max_roots = -1
        max_witness = None
        max_root_set = None
        boundary_max = {"A_zero": 0, "B_zero": 0, "C_zero": 0}
        polynomial_count = 0
        for constant, linear, high in projective_live_coefficients(prime):
            roots = [
                point
                for point, point_power in zip(subgroup, high_powers)
                if (constant + linear * point + high * point_power) % prime == 0
            ]
            root_count = len(roots)
            polynomial_count += 1
            if root_count > max_roots:
                max_roots = root_count
                max_witness = [constant, linear, high]
                max_root_set = roots
            if constant == 0:
                boundary_max["A_zero"] = max(boundary_max["A_zero"], root_count)
            if linear == 0:
                boundary_max["B_zero"] = max(boundary_max["B_zero"], root_count)
            if high == 0:
                boundary_max["C_zero"] = max(boundary_max["C_zero"], root_count)
        total_polynomials += polynomial_count
        total_point_evaluations += polynomial_count * ell
        rows.append(
            {
                "support_class": orbit["canonical"],
                "representative_exponent": exponent,
                "projective_live_polynomials": polynomial_count,
                "max_roots": max_roots,
                "max_root_witness": max_witness,
                "max_root_set": max_root_set,
                "binomial_boundary_maxima": boundary_max,
                "all_binomial_boundaries_have_at_most_one_root": max(boundary_max.values()) <= 1,
            }
        )

    quotient_cosets = (prime - 1) // ell
    maximum_cell_cosets = 2 * ell - 3
    return {
        "ell": ell,
        "p": prime,
        "generator": generator,
        "subgroup_size": len(set(subgroup)),
        "quotient_cosets": quotient_cosets,
        "minimum_cell_cosets": 11,
        "maximum_cell_cosets": maximum_cell_cosets,
        "realizes_at_least_one_tau_ge_5_cell": quotient_cosets >= 11,
        "realizes_every_tau_ge_5_cell": quotient_cosets >= maximum_cell_cosets,
        "orbit_rows": rows,
        "total_projective_polynomials": total_polynomials,
        "total_point_evaluations": total_point_evaluations,
        "max_roots": max(int(row["max_roots"]) for row in rows),
        "all_binomial_boundaries_have_at_most_one_root": all(
            bool(row["all_binomial_boundaries_have_at_most_one_root"])
            for row in rows
        ),
    }


def cell_rows(ell: int) -> list[dict[str, object]]:
    rows = []
    for tau in range(TAU_MIN, ell - 1):
        for core_cosets in range(tau + 1, ell):
            dead_degree = core_cosets - tau - 1
            retained_bound = dead_degree * ell + 2 * (tau + 1)
            listing_requirement = (dead_degree + 2) * ell
            rows.append(
                {
                    "ell": ell,
                    "tau": tau,
                    "m": core_cosets,
                    "D": dead_degree,
                    "distinct_cosets_required": tau + core_cosets,
                    "retained_upper_bound": retained_bound,
                    "listing_core_requirement": listing_requirement,
                    "strict_gap": listing_requirement - retained_bound,
                    "expected_gap": 2 * (ell - tau - 1),
                    "vacant_under_two_root_cap": retained_bound < listing_requirement,
                }
            )
    return rows


def run() -> dict[str, object]:
    residual_text = UPSTREAM_RESIDUAL_NOTE.read_text(encoding="utf-8")
    multisector_text = UPSTREAM_MULTISECTOR_NOTE.read_text(encoding="utf-8")
    ell_rows = []
    for ell in ELLS:
        orbits = orbit_data(ell)
        exact = exact_resultant_data(ell, orbits)
        cells = cell_rows(ell)
        smoke = finite_field_exhaustion(
            ell, SMOKE_FIELDS[ell], list(orbits["orbits"])
        )
        exceptional = finite_field_exhaustion(
            ell, EXCEPTIONAL_FIELDS[ell], list(orbits["orbits"])
        )
        exceptional_prime = EXCEPTIONAL_FIELDS[ell]
        ell_rows.append(
            {
                "ell": ell,
                "affine_orbits": orbits,
                "exact_resultants": exact,
                "cells": cells,
                "cell_count": len(cells),
                "minimum_required_cosets": min(
                    int(row["distinct_cosets_required"]) for row in cells
                ),
                "maximum_required_cosets": max(
                    int(row["distinct_cosets_required"]) for row in cells
                ),
                "exceptional_prime": exceptional_prime,
                "exceptional_prime_quotient_cosets": (exceptional_prime - 1) // ell,
                "exceptional_prime_is_geometrically_unavailable_for_every_cell": all(
                    (exceptional_prime - 1) // ell
                    < int(row["distinct_cosets_required"])
                    for row in cells
                ),
                "available_smoke": smoke,
                "unavailable_exceptional_smoke": exceptional,
            }
        )

    checks = {
        "upstream_current_snapshot_leaves_two_or_more_sectors_open": "The residual danger is `|S| >= 2`" in residual_text,
        "upstream_current_snapshot_has_full_support_multisector_witnesses": "all `ell-1` DFT sectors active" in multisector_text,
        "orbit_counts_are_2_and_3": [
            int(row["affine_orbits"]["orbit_count"]) for row in ell_rows
        ] == [2, 3],
        "orbit_sizes_match_exact_tables": all(
            {
                tuple(orbit["canonical"]): int(orbit["size"])
                for orbit in row["affine_orbits"]["orbits"]
            }
            == EXPECTED_ORBIT_SIZES[int(row["ell"])]
            for row in ell_rows
        ),
        "normalized_ratio_classes_match_exact_tables": all(
            {
                tuple(orbit["canonical"]): list(orbit["normalized_ratios"])
                for orbit in row["affine_orbits"]["orbits"]
            }
            == EXPECTED_RATIO_CLASSES[int(row["ell"])]
            for row in ell_rows
        ),
        "all_orbit_resultants_match_expected": all(
            all(
                bool(table_row["matches_expected"])
                for table_row in row["exact_resultants"]["orbit_resultant_table"]
            )
            for row in ell_rows
        ),
        "all_normalized_resultants_are_orbit_invariant": all(
            all(
                bool(table_row["all_normalized_pairs_in_class_agree"])
                for table_row in row["exact_resultants"]["orbit_resultant_table"]
            )
            for row in ell_rows
        ),
        "vandermonde_resultants_are_ell_cubed": all(
            all(
                int(pair_row["vandermonde_resultant"]) == int(row["ell"]) ** 3
                for pair_row in row["exact_resultants"]["all_normalized_pair_rows"]
            )
            for row in ell_rows
        ),
        "unique_admissible_external_primes_are_23_and_53": [
            row["exact_resultants"]["external_admissible_prime_factors"]
            for row in ell_rows
        ] == [[23], [53]],
        "exceptional_primes_are_unavailable_for_every_cell": all(
            bool(row["exceptional_prime_is_geometrically_unavailable_for_every_cell"])
            for row in ell_rows
        ),
        "all_43_cells_have_strict_retained_gap": sum(
            int(row["cell_count"]) for row in ell_rows
        ) == 43
        and all(
            all(
                bool(cell["vacant_under_two_root_cap"])
                and int(cell["strict_gap"]) == int(cell["expected_gap"]) > 0
                for cell in row["cells"]
            )
            for row in ell_rows
        ),
        "available_smokes_realize_every_cell_and_have_root_cap_two": all(
            bool(row["available_smoke"]["realizes_every_tau_ge_5_cell"])
            and int(row["available_smoke"]["max_roots"]) <= 2
            for row in ell_rows
        ),
        "exceptional_smokes_are_unavailable_and_exhibit_three_roots": all(
            not bool(row["unavailable_exceptional_smoke"]["realizes_at_least_one_tau_ge_5_cell"])
            and int(row["unavailable_exceptional_smoke"]["max_roots"]) == 3
            for row in ell_rows
        ),
        "all_smoke_binomial_boundaries_have_at_most_one_root": all(
            bool(row[key]["all_binomial_boundaries_have_at_most_one_root"])
            for row in ell_rows
            for key in ("available_smoke", "unavailable_exceptional_smoke")
        ),
    }

    return {
        "title": "Complete exact-two-sector vacancy for ell=11 and ell=13",
        "status": "PROVED_LOCAL",
        "verdict": "PASS_WITH_ELL11_13_TWO_SECTOR_COMPLETE_VACANCY",
        "theorem": (
            "Let ell be 11 or 13, p prime with ell|(p-1), tau>=5, and "
            "tau<m<ell. If F_p^* contains the tau+m distinct mu_ell-cosets "
            "needed by the background-free sunflower, no listed full-petal "
            "codeword has exactly two active nonzero DFT sectors. Hence this "
            "exact-two-sector stratum contributes no mixed minimal kernel set, "
            "primitive or otherwise."
        ),
        "proof_steps": [
            "Write D=m-tau-1>=0. Full-petal agreement gives P_r=phi*g_r and P_s=phi*g_s with nonzero g_r,g_s of degree at most D.",
            "The common zero set of g_r,g_s contains at most D core labels. Calling these sector-dead and granting them all ell retained points is a pessimistic upper bound.",
            "On every other core coset the restriction is A+B*h^r+C*h^s with (B,C)!=(0,0). A coefficient-zero boundary is a nonzero binomial and has at most one root on mu_ell because ell is prime.",
            "Normalize the exponent support to {0,1,e} under AGL(1,ell), and any three distinct roots to {1,zeta,zeta^w}. The 3x3 evaluation matrix is singular exactly when a nonzero supported polynomial vanishes on those roots; the binomial bound forces all three coefficients to be nonzero.",
            "The evaluation determinant is D_e,w=(X-1)(X^(ew)-1)-(X^e-1)(X^w-1). Divide its nonvanishing distinct-root Vandermonde factor V_w=(X-1)(X^w-1)(X^w-X).",
            "Exact Sylvester/Bareiss resultants of Phi_ell with D_e,w/V_w are orbit-invariant. Their tables are [[1,1],[1,23]] at ell=11 and [[1,1,1],[1,53,27],[1,27,729]] at ell=13.",
            "Among prime factors of those tables, the only primes congruent to one modulo ell are 23 and 53. They contain only 2 and 4 mu_ell-cosets, but every tau>=5,tau<m cell needs at least tau+m>=11, so a realizable cell avoids every bad characteristic.",
            "Every live coset therefore retains at most two points. If z<=D is the actual number of sector-dead cosets, retained<=z*ell+2*(m-z)<=D*ell+2*(tau+1), while listing requires (D+2)*ell. Their difference is 2*(ell-tau-1)>0 because tau<m<ell.",
        ],
        "ell_rows": ell_rows,
        "uniformity": (
            "The load-bearing proof is the complete integer orbit-resultant "
            "table plus the geometric coset-count exclusion. Finite-field "
            "enumerations are regression tests only."
        ),
        "singularity_equivalence": (
            "For fixed distinct support and root triples, determinant zero is "
            "equivalent to a nonzero coefficient vector in the evaluation "
            "kernel. A monomial has no roots and a binomial has at most one "
            "mu_ell-root, so a kernel vector for three distinct roots has all "
            "three entries nonzero; it is exactly a trinomial three-root event."
        ),
        "scope": (
            "Prime-field background-free setting only: no extension-field "
            "claim is made. Closes exactly two active nonzero sectors for "
            "ell in {11,13} and tau>=5,tau<m<ell, conditional only on "
            "geometric realizability. "
            "It is not whole-cell vacancy. Current upstream contains compatible "
            "multispectral/full-support witnesses (and numeric ell=11,13 spectrum "
            "witnesses); every stratum with three or more active sectors remains "
            "outside this theorem."
        ),
        "upstream": {
            "residual_source": UPSTREAM_RESIDUAL_NOTE.relative_to(ROOT).as_posix(),
            "multisector_source": UPSTREAM_MULTISECTOR_NOTE.relative_to(ROOT).as_posix(),
            "collision": (
                "No exact-two-sector ell=11/13 orbit-resultant closure found in "
                "the inspected upstream sources. Upstream's multispectral "
                "witnesses prevent any whole-cell vacancy restatement."
            ),
        },
        "next_obligation": (
            "Extend the orbit-resultant sieve to further prime ell, or attack "
            "the first three-active-sector strata without contradicting the "
            "known multispectral witness band."
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> int:
    out = run()
    ARTIFACT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    table_shapes = [
        len(row["exact_resultants"]["orbit_resultant_table"])
        for row in out["ell_rows"]
    ]
    field_polynomials = sum(
        int(row[key]["total_projective_polynomials"])
        for row in out["ell_rows"]
        for key in ("available_smoke", "unavailable_exceptional_smoke")
    )
    print(out["title"])
    print(
        f"orbit_table_cells={table_shapes} theorem_cells="
        f"{sum(int(row['cell_count']) for row in out['ell_rows'])}"
    )
    print(
        "external_admissible_primes="
        f"{[row['exact_resultants']['external_admissible_prime_factors'] for row in out['ell_rows']]} "
        f"field_projective_polynomials={field_polynomials}"
    )
    print(
        "available_smoke_max_roots="
        f"{[row['available_smoke']['max_roots'] for row in out['ell_rows']]} "
        "exceptional_smoke_max_roots="
        f"{[row['unavailable_exceptional_smoke']['max_roots'] for row in out['ell_rows']]}"
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
