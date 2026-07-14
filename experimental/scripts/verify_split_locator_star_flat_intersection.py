#!/usr/bin/env python3
"""Audit the sharp split-locator star-configuration flat bound.

The proof is the deletion/restriction induction in the companion Markdown
note.  This stdlib-only verifier checks its arithmetic recurrences, exact
boundaries, fixed-root sharpness formula, and exhaustive small prime-field
coordinate instances.  It deliberately uses explicit checks instead of
``assert`` so normal and ``python -O`` runs execute identical logic.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from itertools import combinations, product
from math import comb
from typing import Iterator, Sequence


BASE_COMMIT = "9262f63cf093a7510a2df435f220390f59e2bcd5"
THEOREM_ID = "split-locator-star-flat-intersection-v1"


def fail(message: str) -> None:
    raise RuntimeError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def intersection_bound(n_points: int, degree: int, flat_dim: int) -> int:
    check(n_points >= 0, "N must be nonnegative")
    check(0 <= degree <= n_points, "require 0 <= k <= N")
    check(0 <= flat_dim <= degree, "require 0 <= d <= k")
    return comb(n_points - degree + flat_dim, flat_dim)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def matrix_rank_mod(rows: Sequence[Sequence[int]], prime: int) -> int:
    """Return row rank over F_prime by reduced Gaussian elimination."""
    check(is_prime(prime), f"modulus {prime} is not prime")
    if not rows:
        return 0
    width = len(rows[0])
    check(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [[entry % prime for entry in row] for row in rows]
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column] != 0),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(entry * inverse) % prime for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def polynomial_product_mod(
    left: Sequence[int], right: Sequence[int], prime: int
) -> tuple[int, ...]:
    """Multiply low-to-high coefficient vectors over F_prime."""
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index] + left_value * right_value
            ) % prime
    return tuple(result)


def locator_vector(roots: Sequence[int], prime: int) -> tuple[int, ...]:
    coefficients: tuple[int, ...] = (1,)
    for root in roots:
        coefficients = polynomial_product_mod(
            coefficients, ((-root) % prime, 1), prime
        )
    return coefficients


def locator_configuration(
    field_points: Sequence[int], degree: int, prime: int
) -> tuple[tuple[int, ...], ...]:
    locators = tuple(
        locator_vector(root_set, prime)
        for root_set in combinations(field_points, degree)
    )
    check(
        len(set(locators)) == comb(len(field_points), degree),
        "distinct root sets did not give distinct monic locators",
    )
    check(all(locator[-1] == 1 for locator in locators), "locator is not monic")
    return locators


def gaussian_binomial(ambient_dim: int, subspace_dim: int, prime: int) -> int:
    check(0 <= subspace_dim <= ambient_dim, "invalid Gaussian-binomial inputs")
    reduced_dim = min(subspace_dim, ambient_dim - subspace_dim)
    numerator = 1
    denominator = 1
    for index in range(reduced_dim):
        numerator *= prime ** (ambient_dim - index) - 1
        denominator *= prime ** (reduced_dim - index) - 1
    check(numerator % denominator == 0, "Gaussian binomial was not integral")
    return numerator // denominator


def rref_subspaces(
    prime: int, ambient_dim: int, subspace_dim: int
) -> Iterator[tuple[tuple[int, ...], ...]]:
    """Yield each vector subspace once via its unique RREF row basis."""
    check(is_prime(prime), f"modulus {prime} is not prime")
    check(0 <= subspace_dim <= ambient_dim, "invalid subspace dimension")
    for pivots in combinations(range(ambient_dim), subspace_dim):
        pivot_set = set(pivots)
        nonpivots = [column for column in range(ambient_dim) if column not in pivot_set]
        free_positions = [
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in nonpivots
            if column > pivot
        ]
        for values in product(range(prime), repeat=len(free_positions)):
            rows = [[0] * ambient_dim for _ in range(subspace_dim)]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, column), value in zip(free_positions, values):
                rows[row][column] = value
            yield tuple(tuple(row) for row in rows)


def vector_in_row_span(
    vector: Sequence[int], basis: Sequence[Sequence[int]], prime: int
) -> bool:
    basis_rank = len(basis)
    check(matrix_rank_mod(basis, prime) == basis_rank, "basis is dependent")
    return matrix_rank_mod((*basis, tuple(vector)), prime) == basis_rank


def fixed_root_flat_basis(
    field_points: Sequence[int], degree: int, flat_dim: int, prime: int
) -> tuple[tuple[int, ...], ...]:
    fixed_roots = tuple(field_points[: degree - flat_dim])
    fixed_locator = locator_vector(fixed_roots, prime)
    basis = []
    for shift in range(flat_dim + 1):
        row = (
            (0,) * shift
            + fixed_locator
            + (0,) * (flat_dim - shift)
        )
        check(len(row) == degree + 1, "fixed-root basis has wrong width")
        basis.append(row)
    result = tuple(basis)
    check(
        matrix_rank_mod(result, prime) == flat_dim + 1,
        "fixed-root multiplication basis is dependent",
    )
    return result


@dataclass(frozen=True)
class CoordinateCase:
    prime: int
    points: tuple[int, ...]
    degree: int
    flat_dim: int


COORDINATE_CASES = (
    CoordinateCase(3, (0, 1, 2), 0, 0),
    CoordinateCase(3, (0, 1, 2), 2, 0),
    CoordinateCase(3, (0, 1, 2), 2, 1),
    CoordinateCase(3, (0, 1, 2), 2, 2),
    CoordinateCase(5, (0, 1, 2), 3, 2),
    CoordinateCase(5, (0, 1, 2, 3, 4), 2, 1),
    CoordinateCase(5, (0, 1, 2, 3, 4), 3, 1),
    CoordinateCase(5, (0, 1, 2, 3, 4), 3, 2),
    CoordinateCase(7, (0, 1, 2, 3, 4, 5), 3, 1),
    CoordinateCase(7, (0, 1, 2, 3, 4, 5), 3, 2),
)


def check_symbolic_identities() -> dict[str, object]:
    boundary_counts = {"d=0": 0, "k=0": 0, "N=k": 0, "d=k": 0}
    sharpness_cases = 0
    for n_points in range(13):
        for degree in range(n_points + 1):
            for flat_dim in range(degree + 1):
                bound = intersection_bound(n_points, degree, flat_dim)
                if flat_dim == 0:
                    check(bound == 1, "d=0 boundary failed")
                    boundary_counts["d=0"] += 1
                if degree == 0:
                    check(flat_dim == 0 and bound == 1, "k=0 boundary failed")
                    boundary_counts["k=0"] += 1
                if n_points == degree:
                    check(bound == 1, "N=k boundary failed")
                    boundary_counts["N=k"] += 1
                if flat_dim == degree:
                    check(bound == comb(n_points, degree), "d=k boundary failed")
                    boundary_counts["d=k"] += 1

                fixed_root_count = comb(n_points - (degree - flat_dim), flat_dim)
                check(fixed_root_count == bound, "fixed-root sharp count failed")
                sharpness_cases += 1

    transverse_cases = 0
    contained_cases = 0
    for n_points in range(2, 13):
        for degree in range(1, n_points):
            for flat_dim in range(1, degree + 1):
                parent = intersection_bound(n_points, degree, flat_dim)
                avoiding = intersection_bound(n_points - 1, degree, flat_dim)
                containing = intersection_bound(
                    n_points - 1, degree - 1, flat_dim - 1
                )
                check(
                    parent == avoiding + containing,
                    "transverse Pascal recurrence failed",
                )
                transverse_cases += 1
            for flat_dim in range(degree):
                parent = intersection_bound(n_points, degree, flat_dim)
                restricted = intersection_bound(
                    n_points - 1, degree - 1, flat_dim
                )
                check(parent == restricted, "contained-flat recurrence failed")
                contained_cases += 1

    return {
        "boundary_counts": boundary_counts,
        "contained_recurrence_cases": contained_cases,
        "sharpness_cases": sharpness_cases,
        "transverse_recurrence_cases": transverse_cases,
    }


def check_coordinate_case(case: CoordinateCase) -> dict[str, object]:
    prime = case.prime
    points = tuple(point % prime for point in case.points)
    n_points = len(points)
    degree = case.degree
    flat_dim = case.flat_dim
    check(is_prime(prime), f"F_{prime} is not a prime field")
    check(len(set(points)) == n_points, "field points are not distinct")
    check(0 <= degree <= n_points, "coordinate case has invalid degree")
    check(0 <= flat_dim <= degree, "coordinate case has invalid flat dimension")

    locators = locator_configuration(points, degree, prime)
    expected_locators = comb(n_points, degree)
    check(len(locators) == expected_locators, "locator count mismatch")

    ambient_dim = degree + 1
    subspace_dim = flat_dim + 1
    expected_flat_count = gaussian_binomial(ambient_dim, subspace_dim, prime)
    flat_count = 0
    maximum = -1
    maximizing_flats = 0
    for basis in rref_subspaces(prime, ambient_dim, subspace_dim):
        flat_count += 1
        incidence = sum(
            vector_in_row_span(locator, basis, prime) for locator in locators
        )
        if incidence > maximum:
            maximum = incidence
            maximizing_flats = 1
        elif incidence == maximum:
            maximizing_flats += 1
    check(flat_count == expected_flat_count, "projective-flat census mismatch")

    bound = intersection_bound(n_points, degree, flat_dim)
    check(maximum <= bound, "coordinate instance violates theorem bound")

    sharp_basis = fixed_root_flat_basis(points, degree, flat_dim, prime)
    sharp_incidence = sum(
        vector_in_row_span(locator, sharp_basis, prime) for locator in locators
    )
    check(sharp_incidence == bound, "fixed-root coordinate flat is not sharp")
    check(maximum == bound, "coordinate maximum does not attain sharp bound")

    return {
        "bound": bound,
        "degree": degree,
        "field": prime,
        "flat_dim": flat_dim,
        "flats": flat_count,
        "locators": len(locators),
        "max_incidence": maximum,
        "maximizing_flats": maximizing_flats,
        "n_points": n_points,
        "sharp_incidence": sharp_incidence,
    }


def main() -> None:
    symbolic = check_symbolic_identities()
    coordinate_rows = [check_coordinate_case(case) for case in COORDINATE_CASES]
    certificate = {
        "base_commit": BASE_COMMIT,
        "coordinate_rows": coordinate_rows,
        "scope": {
            "common_star_attainment_28": False,
            "average_johnson_degree_le_60": False,
            "deployed_or_prize_claim": False,
            "rs_source_bridge": False,
        },
        "symbolic": symbolic,
        "theorem_id": THEOREM_ID,
    }
    canonical = json.dumps(
        certificate, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    digest = hashlib.sha256(canonical).hexdigest()

    boundaries = symbolic["boundary_counts"]
    check(isinstance(boundaries, dict), "boundary count record has wrong type")
    print("SPLIT_LOCATOR_STAR_FLAT_INTERSECTION")
    print(f"BASE_COMMIT={BASE_COMMIT}")
    print(f"THEOREM_ID={THEOREM_ID}")
    print(
        "RECURRENCE: "
        f"transverse={symbolic['transverse_recurrence_cases']} "
        f"contained={symbolic['contained_recurrence_cases']} PASS"
    )
    print(
        "BOUNDARIES: "
        f"d0={boundaries['d=0']} k0={boundaries['k=0']} "
        f"N_eq_k={boundaries['N=k']} d_eq_k={boundaries['d=k']} PASS"
    )
    print(f"SHARPNESS: parameter_cases={symbolic['sharpness_cases']} PASS")
    for row in coordinate_rows:
        print(
            "COORDINATE: "
            f"F_{row['field']} N={row['n_points']} k={row['degree']} "
            f"d={row['flat_dim']} flats={row['flats']} "
            f"locators={row['locators']} max={row['max_incidence']} "
            f"bound={row['bound']} sharp={row['sharp_incidence']} "
            f"maximizers={row['maximizing_flats']} PASS"
        )
    print(f"certificate_sha256={digest}")
    print(
        "SCOPE: abstract locator configuration only; no RS source bridge; "
        "no common-star attainment 28; no average Johnson degree <=60; "
        "no deployed or prize claim"
    )
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
