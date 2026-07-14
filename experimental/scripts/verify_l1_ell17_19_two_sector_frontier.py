#!/usr/bin/env python3
"""Exact certificate for the ell=17,19 two-sector frontier.

The certificate continues the smaller-prime vacancy theorems in the prime-field, background-free
setting.  For each prime ell in {17,19}, it

* classifies three-exponent and three-root supports under AGL(1,ell);
* divides the Fourier 3x3 minor by its distinct-root Vandermonde factor;
* computes the normalized cyclotomic-resultant table over Z with Bareiss;
* filters its prime factors by p == 1 (mod ell) and exact coset availability;
* exhausts ranks of every 3x3 and 4x3 evaluation submatrix over every
  exceptional prime, without enumerating coefficient pairs; and
* combines those caps with the cyclic-width inequality and the exact
  sector-dead/listing budget.

The output is deliberately a frontier theorem, not a complete vacancy
theorem.  The only unresolved exact-two-sector families are

    ell=17, p=1361, tau>=11, e in {4,5,7,11,13,14};
    ell=19, p=2699, tau>=12, e in {4,5,6,14,15,16},

with tau<m<ell.  Rank exhaustion proves only that their live-coset root cap
is exactly three (never four); it does not construct a listed codeword.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
ARTIFACT = DATA / "ell17_19_two_sector_exceptional_frontier.json"

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
UPSTREAM_DAG = (
    ROOT
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)
UPSTREAM_ELL17_SPECTRUM_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_prime_ell_frontier_corrected.md"
)
UPSTREAM_ELL19_ATTAINMENT_NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_ell19_attainment.md"
)

TAU_MIN = 5
EXPECTED = {
    17: {
        "resultant_values": {1, 103, 239, 1361},
        "external_primes": [103, 239, 1361],
        "frontier_prime": 1361,
        "frontier_tau_min": 11,
        "frontier_ratios": [4, 5, 7, 11, 13, 14],
        "transition_prime": 239,
        "transition_width": 3,
    },
    19: {
        "resultant_values": {1, 191, 343, 457, 1331, 2699, 117649},
        "external_primes": [191, 457, 2699],
        "frontier_prime": 2699,
        "frontier_tau_min": 12,
        "frontier_ratios": [4, 5, 6, 14, 15, 16],
        "transition_prime": 457,
        "transition_width": 3,
    },
}


def trim(polynomial: list[int]) -> list[int]:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def monomial(exponent: int) -> list[int]:
    return [0] * exponent + [1]


def poly_add(first: list[int], second: list[int]) -> list[int]:
    output = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        output[index] += value
    for index, value in enumerate(second):
        output[index] += value
    return trim(output)


def poly_sub(first: list[int], second: list[int]) -> list[int]:
    return poly_add(first, [-value for value in second])


def poly_mul(first: list[int], second: list[int]) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] += first_value * second_value
    return trim(output)


def exact_poly_division(dividend: list[int], divisor: list[int]) -> list[int]:
    work = trim(dividend[:])
    divisor = trim(divisor[:])
    assert divisor != [0]
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    while work != [0] and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient, remainder = divmod(work[-1], divisor[-1])
        assert remainder == 0, "nonintegral quotient"
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[index + shift] -= coefficient * value
        trim(work)
    assert work == [0], "nonzero polynomial remainder"
    return trim(quotient)


def fourier_minor_polynomial(exponent_ratio: int, root_ratio: int) -> list[int]:
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
    first_degree = len(first) - 1
    second_degree = len(second) - 1
    size = first_degree + second_degree
    rows = []
    for shift in range(second_degree):
        rows.append([0] * shift + first + [0] * (second_degree - 1 - shift))
    for shift in range(first_degree):
        rows.append([0] * shift + second + [0] * (first_degree - 1 - shift))
    assert size > 0 and len(rows) == size
    assert all(len(row) == size for row in rows)
    return rows


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    assert size > 0 and all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous_pivot = 1
    for column in range(size - 1):
        if work[column][column] == 0:
            swap = next(
                (
                    row
                    for row in range(column + 1, size)
                    if work[row][column] != 0
                ),
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


def prime_factorization(value: int) -> list[list[int]]:
    value = abs(value)
    factors = []
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


def affine_canonical(ell: int, support: tuple[int, int, int]) -> tuple[int, int, int]:
    return min(
        tuple(sorted((unit * exponent + shift) % ell for exponent in support))
        for unit in range(1, ell)
        for shift in range(ell)
    )


def orbit_data(ell: int) -> dict[str, object]:
    support_orbits: dict[tuple[int, int, int], int] = {}
    for support in itertools.combinations(range(ell), 3):
        canonical = affine_canonical(ell, support)
        support_orbits[canonical] = support_orbits.get(canonical, 0) + 1

    ratio_classes: dict[tuple[int, int, int], list[int]] = {}
    for ratio in range(2, ell):
        canonical = affine_canonical(ell, (0, 1, ratio))
        ratio_classes.setdefault(canonical, []).append(ratio)

    assert set(support_orbits) == set(ratio_classes)
    rows = []
    for canonical in sorted(support_orbits):
        ratios = ratio_classes[canonical]
        rows.append(
            {
                "canonical": list(canonical),
                "support_orbit_size": support_orbits[canonical],
                "normalized_ratios": ratios,
                "representative_ratio": min(ratios),
            }
        )
    assert sum(row["support_orbit_size"] for row in rows) == (
        ell * (ell - 1) * (ell - 2) // 6
    )
    assert sorted(ratio for row in rows for ratio in row["normalized_ratios"]) == list(
        range(2, ell)
    )
    return {"orbit_count": len(rows), "orbits": rows}


def cyclic_span_width(ell: int, exponent_ratio: int) -> int:
    """The width invariant delta_ell for normalized support {0,1,e}."""

    best = ell
    for unit in range(1, ell):
        points = sorted((0, unit, (unit * exponent_ratio) % ell))
        gaps = [
            points[1] - points[0],
            points[2] - points[1],
            ell + points[0] - points[2],
        ]
        best = min(best, ell - max(gaps))
    return best


def resultant_sieve(ell: int, orbits: dict[str, object]) -> dict[str, object]:
    phi = cyclotomic_prime_polynomial(ell)
    table = []
    values = set()
    for exponent_orbit in orbits["orbits"]:
        exponent_ratio = int(exponent_orbit["representative_ratio"])
        for root_orbit in orbits["orbits"]:
            root_ratio = int(root_orbit["representative_ratio"])
            determinant = fourier_minor_polynomial(exponent_ratio, root_ratio)
            vandermonde = vandermonde_polynomial(root_ratio)
            quotient = exact_poly_division(determinant, vandermonde)
            quotient_resultant = abs(resultant(phi, quotient))
            vandermonde_resultant = abs(resultant(phi, vandermonde))
            raw_resultant = abs(resultant(phi, determinant))
            assert vandermonde_resultant == ell**3
            assert raw_resultant == vandermonde_resultant * quotient_resultant
            values.add(quotient_resultant)
            table.append(
                {
                    "exponent_class": exponent_orbit["canonical"],
                    "exponent_representative": exponent_ratio,
                    "root_class": root_orbit["canonical"],
                    "root_representative": root_ratio,
                    "quotient_resultant": quotient_resultant,
                    "factorization": prime_factorization(quotient_resultant),
                    "determinant_degree": len(determinant) - 1,
                    "vandermonde_degree": len(vandermonde) - 1,
                    "quotient_degree": len(quotient) - 1,
                    "raw_factorization_check": raw_resultant
                    == ell**3 * quotient_resultant,
                }
            )

    assert values == EXPECTED[ell]["resultant_values"]
    external_primes = sorted(
        {
            prime
            for value in values
            for prime, _multiplicity in prime_factorization(value)
            if prime % ell == 1
        }
    )
    assert external_primes == EXPECTED[ell]["external_primes"]
    return {
        "orbit_table": table,
        "normalized_resultant_values": sorted(values),
        "external_admissible_prime_factors": external_primes,
        "vandermonde_resultant": ell**3,
        "orbit_normalization_reason": (
            "AGL unit powers and translations act by row/column permutations, "
            "cyclotomic Galois automorphisms, and nonzero monomial factors; "
            "therefore the absolute quotient resultant is constant on each "
            "ordered pair of exponent/root orbits."
        ),
    }


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(value * inverse) % prime for value in work[rank]]
        for row in range(row_count):
            if row != rank and work[row][column] != 0:
                factor = work[row][column]
                work[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def null_vector_three_by_three(matrix: list[list[int]], prime: int) -> list[int]:
    for first_index, second_index in itertools.combinations(range(3), 2):
        first = matrix[first_index]
        second = matrix[second_index]
        vector = [
            first[1] * second[2] - first[2] * second[1],
            first[2] * second[0] - first[0] * second[2],
            first[0] * second[1] - first[1] * second[0],
        ]
        vector = [value % prime for value in vector]
        if any(vector):
            assert all(
                sum(entry * coefficient for entry, coefficient in zip(row, vector))
                % prime
                == 0
                for row in matrix
            )
            return vector
    raise AssertionError("rank-two matrix had no cross-product null vector")


def rank_exhaustion(ell: int, prime: int) -> dict[str, object]:
    assert is_prime(prime) and (prime - 1) % ell == 0
    generator = primitive_root(prime)
    zeta = pow(generator, (prime - 1) // ell, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    assert len(set(subgroup)) == ell and pow(zeta, ell, prime) == 1

    rows = []
    total_three_tests = 0
    total_four_tests = 0
    for exponent_ratio in range(2, ell):
        evaluation_rows = [
            [1, point, pow(point, exponent_ratio, prime)] for point in subgroup
        ]
        singular_three = 0
        singular_four = 0
        witness = None
        minimum_singular_three_rank = 3
        for indices in itertools.combinations(range(ell), 3):
            matrix = [evaluation_rows[index] for index in indices]
            rank = matrix_rank_mod(matrix, prime)
            total_three_tests += 1
            if rank < 3:
                singular_three += 1
                minimum_singular_three_rank = min(minimum_singular_three_rank, rank)
                if witness is None:
                    coefficients = null_vector_three_by_three(matrix, prime)
                    assert all(coefficients), "three roots cannot come from a binomial"
                    witness = {
                        "root_indices": list(indices),
                        "root_values": [subgroup[index] for index in indices],
                        "coefficients_A_B_C": coefficients,
                    }
        for indices in itertools.combinations(range(ell), 4):
            matrix = [evaluation_rows[index] for index in indices]
            rank = matrix_rank_mod(matrix, prime)
            total_four_tests += 1
            if rank < 3:
                singular_four += 1

        assert singular_four == 0
        if singular_three:
            assert minimum_singular_three_rank == 2
            exact_max_roots = 3
        else:
            exact_max_roots = 2
        rows.append(
            {
                "exponent_ratio": exponent_ratio,
                "cyclic_span_width": cyclic_span_width(ell, exponent_ratio),
                "singular_three_subsets": singular_three,
                "singular_four_subsets": singular_four,
                "exact_max_roots": exact_max_roots,
                "three_root_witness": witness,
            }
        )

    return {
        "ell": ell,
        "p": prime,
        "generator": generator,
        "zeta": zeta,
        "quotient_cosets": (prime - 1) // ell,
        "three_subset_rank_tests": total_three_tests,
        "four_subset_rank_tests": total_four_tests,
        "all_four_by_three_matrices_full_column_rank": all(
            row["singular_four_subsets"] == 0 for row in rows
        ),
        "ratios_with_exactly_three_roots": [
            row["exponent_ratio"]
            for row in rows
            if row["exact_max_roots"] == 3
        ],
        "ratio_rows": rows,
    }


def cell_pairs(ell: int) -> list[tuple[int, int]]:
    return [
        (tau, core_cosets)
        for tau in range(TAU_MIN, ell - 1)
        for core_cosets in range(tau + 1, ell)
    ]


def cap_gap(ell: int, tau: int, cap: int) -> int:
    """Listing requirement minus the sector-dead cap."""

    return 2 * ell - cap * (tau + 1)


def classify_cells(
    ell: int, rank_by_prime: dict[int, dict[str, object]]
) -> dict[str, object]:
    external_primes = EXPECTED[ell]["external_primes"]
    rank_lookup = {
        prime: {
            int(row["exponent_ratio"]): int(row["exact_max_roots"])
            for row in rank_by_prime[prime]["ratio_rows"]
        }
        for prime in external_primes
    }

    # Every nonexceptional prime has cap two by the integer resultant sieve.
    generic_rows = []
    for tau, core_cosets in cell_pairs(ell):
        D = core_cosets - tau - 1
        gap = cap_gap(ell, tau, 2)
        assert gap == 2 * (ell - tau - 1) > 0
        generic_rows.append(
            {
                "tau": tau,
                "m": core_cosets,
                "D": D,
                "retained_bound_cap_2": D * ell + 2 * (tau + 1),
                "listing_requirement": (D + 2) * ell,
                "strict_gap": gap,
            }
        )

    exceptional_rows = []
    residual_rows = []
    route_counts: dict[str, int] = {}
    for prime in external_primes:
        quotient_cosets = (prime - 1) // ell
        for exponent_ratio in range(2, ell):
            width = cyclic_span_width(ell, exponent_ratio)
            exact_cap = rank_lookup[prime][exponent_ratio]
            for tau, core_cosets in cell_pairs(ell):
                required_cosets = tau + core_cosets
                if cap_gap(ell, tau, width) > 0:
                    route = "cyclic_width_vacancy"
                elif quotient_cosets < required_cosets:
                    route = "prime_field_coset_unavailable"
                elif exact_cap == 2:
                    assert cap_gap(ell, tau, 2) > 0
                    route = "Fourier_resultant_two_root_cap"
                elif cap_gap(ell, tau, 3) > 0:
                    route = "four_by_three_rank_three_root_cap"
                else:
                    route = "EXPLICIT_UNRESOLVED_FRONTIER"
                route_counts[route] = route_counts.get(route, 0) + 1
                row = {
                    "p": prime,
                    "exponent_ratio": exponent_ratio,
                    "cyclic_span_width": width,
                    "tau": tau,
                    "m": core_cosets,
                    "required_cosets": required_cosets,
                    "available_cosets": quotient_cosets,
                    "exact_live_coset_root_cap": exact_cap,
                    "route": route,
                }
                exceptional_rows.append(row)
                if route == "EXPLICIT_UNRESOLVED_FRONTIER":
                    residual_rows.append(row)

    expected = EXPECTED[ell]
    assert {row["p"] for row in residual_rows} == {expected["frontier_prime"]}
    assert sorted({row["exponent_ratio"] for row in residual_rows}) == expected[
        "frontier_ratios"
    ]
    assert min(row["tau"] for row in residual_rows) == expected["frontier_tau_min"]
    assert max(row["tau"] for row in residual_rows) == ell - 2
    assert all(row["exact_live_coset_root_cap"] == 3 for row in residual_rows)

    transition_prime = int(expected["transition_prime"])
    transition_width = int(expected["transition_width"])
    first_unpaid_tau = min(
        tau
        for tau in range(TAU_MIN, ell - 1)
        if cap_gap(ell, tau, transition_width) <= 0
    )
    assert first_unpaid_tau == expected["frontier_tau_min"]
    minimum_required_at_transition = 2 * first_unpaid_tau + 1
    transition_cosets = (transition_prime - 1) // ell
    assert transition_cosets < minimum_required_at_transition

    frontier_cell_pairs = sorted({(row["tau"], row["m"]) for row in residual_rows})
    return {
        "generic_nonexceptional_characteristics": {
            "root_cap": 2,
            "cell_rows": generic_rows,
            "all_cells_vacant": True,
        },
        "exceptional_route_counts": route_counts,
        "exceptional_classification_row_count": len(exceptional_rows),
        "frontier": {
            "p": expected["frontier_prime"],
            "tau_min": expected["frontier_tau_min"],
            "tau_max": ell - 2,
            "m_condition": "tau < m < ell",
            "exponent_ratios": expected["frontier_ratios"],
            "parameter_pairs": [list(pair) for pair in frontier_cell_pairs],
            "parameter_pair_count": len(frontier_cell_pairs),
            "ratio_parameter_cell_count": len(residual_rows),
            "proven_live_coset_root_cap": 3,
            "four_root_event": False,
            "status": "UNRESOLVED_NOT_A_COUNTEREXAMPLE",
        },
        "width_three_transition": {
            "p": transition_prime,
            "quotient_cosets": transition_cosets,
            "last_tau_paid_by_cyclic_width": first_unpaid_tau - 1,
            "first_tau_not_paid_by_width": first_unpaid_tau,
            "minimum_required_cosets_at_first_unpaid_tau": minimum_required_at_transition,
            "unavailable_from_first_unpaid_tau_onward": True,
        },
    }


def run() -> dict[str, object]:
    residual_text = UPSTREAM_RESIDUAL_NOTE.read_text(encoding="utf-8")
    multisector_text = UPSTREAM_MULTISECTOR_NOTE.read_text(encoding="utf-8")
    dag_text = UPSTREAM_DAG.read_text(encoding="utf-8")
    ell17_spectrum_text = UPSTREAM_ELL17_SPECTRUM_NOTE.read_text(encoding="utf-8")
    ell19_attainment_text = UPSTREAM_ELL19_ATTAINMENT_NOTE.read_text(encoding="utf-8")
    assert "The residual danger is `|S| >= 2`" in residual_text
    assert "pma_wide_residual" in multisector_text
    assert '"id": "pma_wide_residual"' in dag_text
    assert "`p = 239` (`n = 14`)" in ell17_spectrum_text
    assert "remaining 17 (2699..5701)" in ell19_attainment_text
    assert "no random search at all" in ell19_attainment_text

    ell_rows = []
    total_three_tests = 0
    total_four_tests = 0
    for ell in sorted(EXPECTED):
        orbits = orbit_data(ell)
        sieve = resultant_sieve(ell, orbits)
        rank_by_prime = {}
        for prime in EXPECTED[ell]["external_primes"]:
            rank = rank_exhaustion(ell, prime)
            rank_by_prime[prime] = rank
            total_three_tests += int(rank["three_subset_rank_tests"])
            total_four_tests += int(rank["four_subset_rank_tests"])

        frontier_prime = int(EXPECTED[ell]["frontier_prime"])
        assert rank_by_prime[frontier_prime]["ratios_with_exactly_three_roots"] == EXPECTED[
            ell
        ]["frontier_ratios"]
        assert rank_by_prime[frontier_prime][
            "all_four_by_three_matrices_full_column_rank"
        ]
        classification = classify_cells(ell, rank_by_prime)
        ell_rows.append(
            {
                "ell": ell,
                "affine_orbits": orbits,
                "cyclic_span_widths": [
                    {
                        "exponent_ratio": ratio,
                        "delta": cyclic_span_width(ell, ratio),
                    }
                    for ratio in range(2, ell)
                ],
                "resultant_sieve": sieve,
                "exceptional_prime_rank_exhaustions": [
                    rank_by_prime[prime]
                    for prime in EXPECTED[ell]["external_primes"]
                ],
                "cell_classification": classification,
            }
        )

    result = {
        "title": "ell=17,19 exact-two-sector exceptional frontier",
        "status": "PROVED_LOCAL_FRONTIER_REDUCTION",
        "verdict": "PASS_WITH_ELL17_19_TWO_SECTOR_EXCEPTIONAL_FRONTIER",
        "theorem": (
            "Let ell be 17 or 19, p be prime with ell|(p-1), tau>=5, and "
            "tau<m<ell in the background-free full-petal setting.  Every "
            "geometrically realizable exactly-two-active-nonzero-sector "
            "stratum is vacant except possibly: ell=17,p=1361,tau>=11, "
            "e in {4,5,7,11,13,14}; or ell=19,p=2699,tau>=12, "
            "e in {4,5,6,14,15,16}.  In both families tau<m<ell."
        ),
        "frontier_meaning": (
            "The two displayed families are unresolved cells, not witnesses. "
            "Exact rank exhaustion proves that a live trinomial can have three "
            "roots but never four in those characteristics.  It does not prove "
            "a listed codeword, a minimal kernel set, or whole-cell nonvacancy."
        ),
        "proof_steps": [
            "Write D=m-tau-1.  At most D core cosets are sector-dead; with live-coset cap c, retained<=D*ell+c*(tau+1), while listing requires (D+2)*ell.",
            "Normalize exponent and root triples under AGL(1,ell).  A three-root trinomial makes the 3x3 Fourier minor D_e,w singular; divide its nonzero distinct-root Vandermonde factor.",
            "Exact Bareiss resultants give value sets {1,103,239,1361} for ell=17 and {1,191,343,457,1331,2699,117649} for ell=19.",
            "Only p congruent to 1 modulo ell can contain mu_ell: the external primes are {103,239,1361} and {191,457,2699} respectively.",
            "Every 3x3 and 4x3 evaluation subset is ranked over each external prime.  No singular 4x3 matrix occurs; the exact live-coset cap is therefore two or three, never four.",
            "The width theorem pays each cell satisfying (tau+1)*delta<2ell.  The rank cap three extends payment to tau<=10 at ell=17 and tau<=11 at ell=19.",
            "The width-three primes p=239 and p=457 are unavailable at the first following tau: 14<23 and 24<25 quotient-coset requirements.  The small primes p=103 and p=191 cannot realize even the smallest cell.",
            "At p=1361 and p=2699 the only ratios admitting three roots are the displayed frontier ratios; cap three stops paying exactly at tau=11 and tau=12.  All other rows have a proved vacancy route.",
        ],
        "scope": (
            "Prime fields only; background-free sunflowers; exactly two active "
            "nonzero DFT sectors.  This is not an extension-field theorem, not "
            "vacancy of any whole parameter cell, and not a global "
            "counterexample.  Three-or-more-sector upstream witnesses remain "
            "outside the statement."
        ),
        "upstream": {
            "residual_source": UPSTREAM_RESIDUAL_NOTE.relative_to(ROOT).as_posix(),
            "multisector_source": UPSTREAM_MULTISECTOR_NOTE.relative_to(ROOT).as_posix(),
            "dag_source": UPSTREAM_DAG.relative_to(ROOT).as_posix(),
            "ell17_p239_spectrum_source": UPSTREAM_ELL17_SPECTRUM_NOTE.relative_to(ROOT).as_posix(),
            "ell19_p2699_coverage_source": UPSTREAM_ELL19_ATTAINMENT_NOTE.relative_to(ROOT).as_posix(),
            "collision": (
                "No ell=17,19 exact-two-sector orbit-resultant/exceptional-rank "
                "frontier theorem was found.  Upstream keeps |S|>=2 and "
                "pma_wide_residual open.  Its p=239 entry is spectrum-side and "
                "explicitly availability-limited; p=2699 occurs only in an "
                "unsearched concentrated-floor coverage interval.  Neither is "
                "this exact-two-sector frontier theorem."
            ),
        },
        "ell_rows": ell_rows,
        "operation_counts": {
            "three_by_three_rank_tests": total_three_tests,
            "four_by_three_rank_tests": total_four_tests,
            "coefficient_pair_enumerations": 0,
        },
        "next_obligation": (
            "Resolve or refute the two explicit p=1361 and p=2699 frontier "
            "families using cross-coset coefficient coupling/minimality; do not "
            "infer a listed word from a local three-root witness."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    certificate = run()
    frontiers = [
        row["cell_classification"]["frontier"] for row in certificate["ell_rows"]
    ]
    print("ell=17,19 exact-two-sector exceptional frontier")
    print(
        "resultant_values="
        + str(
            [
                row["resultant_sieve"]["normalized_resultant_values"]
                for row in certificate["ell_rows"]
            ]
        )
    )
    print(
        "external_primes="
        + str(
            [
                row["resultant_sieve"]["external_admissible_prime_factors"]
                for row in certificate["ell_rows"]
            ]
        )
    )
    print(
        "frontiers="
        + str(
            [
                (row["p"], row["tau_min"], row["exponent_ratios"])
                for row in frontiers
            ]
        )
    )
    print(
        f"rank_tests_3={certificate['operation_counts']['three_by_three_rank_tests']} "
        f"rank_tests_4={certificate['operation_counts']['four_by_three_rank_tests']}"
    )
    print(certificate["verdict"])
