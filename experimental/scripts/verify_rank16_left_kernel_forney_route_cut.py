#!/usr/bin/env python3
"""Replay the rank-16 left-kernel / shortened-dual / Forney certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from math import comb
from pathlib import Path
from typing import Any, Callable


REPO = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "rank16-left-kernel-forney"
    / "f31_fixture.json"
)
EXPECTED_FIXTURE_SHA256 = "673bd22b58aba1f30c37b0ceff310a61dc325b7fd3a9640a4361460d68a5d716"


class VerificationError(RuntimeError):
    """A deterministic certificate check failed."""


def fail(message: str) -> None:
    raise VerificationError(message)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_int(value: Any, label: str) -> int:
    check(type(value) is int, f"{label} must be an integer")
    return value


def require_list(value: Any, label: str) -> list[Any]:
    check(type(value) is list, f"{label} must be a list")
    return value


def require_dict(value: Any, label: str) -> dict[str, Any]:
    check(type(value) is dict, f"{label} must be an object")
    check(all(type(key) is str for key in value), f"{label} has a non-string key")
    return value


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_fixture_digest(raw: bytes) -> None:
    actual = sha256_bytes(raw)
    check(
        actual == EXPECTED_FIXTURE_SHA256,
        f"fixture SHA-256 mismatch: expected {EXPECTED_FIXTURE_SHA256}, got {actual}",
    )


def poly_trim(poly: list[int]) -> list[int]:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % prime
    return poly_trim(result)


def poly_eval(poly: list[int], x: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % prime
    return value


def locator(points: tuple[int, ...], prime: int) -> list[int]:
    result = [1]
    for point in points:
        result = poly_mul(result, [(-point) % prime, 1], prime)
    return result


def listed_polynomial(
    support: tuple[int, ...], prime: int, received_word_exponent: int
) -> list[int]:
    support_locator = locator(support, prime)
    result = [(-coefficient) % prime for coefficient in support_locator]
    if len(result) <= received_word_exponent:
        result.extend([0] * (received_word_exponent + 1 - len(result)))
    result[received_word_exponent] = (result[received_word_exponent] + 1) % prime
    return poly_trim(result)


def matrix_shape(matrix: list[list[int]]) -> tuple[int, int]:
    if not matrix:
        return 0, 0
    width = len(matrix[0])
    check(all(len(row) == width for row in matrix), "matrix is not rectangular")
    return len(matrix), width


def field_rank(matrix: list[list[int]], prime: int) -> int:
    row_count, column_count = matrix_shape(matrix)
    if row_count == 0 or column_count == 0:
        return 0
    work = [[entry % prime for entry in row] for row in matrix]
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
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for row in range(row_count):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def field_determinant(matrix: list[list[int]], prime: int) -> int:
    row_count, column_count = matrix_shape(matrix)
    check(row_count == column_count, "determinant matrix is not square")
    check(row_count > 0, "determinant matrix is empty")
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    for column in range(column_count):
        pivot = next(
            (row for row in range(column, row_count) if work[row][column] != 0),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = (-determinant) % prime
        pivot_value = work[column][column]
        determinant = (determinant * pivot_value) % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, row_count):
            if work[row][column] == 0:
                continue
            factor = work[row][column] * inverse % prime
            for entry_column in range(column, column_count):
                work[row][entry_column] = (
                    work[row][entry_column]
                    - factor * work[column][entry_column]
                ) % prime
    return determinant


def lagrange_weights(evaluation_set: tuple[int, ...], prime: int) -> dict[int, int]:
    weights: dict[int, int] = {}
    for x in evaluation_set:
        derivative_value = 1
        for y in evaluation_set:
            if x != y:
                derivative_value = derivative_value * (x - y) % prime
        check(derivative_value != 0, f"zero locator derivative at {x}")
        weights[x] = pow(derivative_value, -1, prime)
    return weights


def build_difference_matrix(
    supports: tuple[tuple[int, ...], ...],
    evaluation_set: tuple[int, ...],
    dimension: int,
    prime: int,
) -> list[list[int]]:
    block_count = len(supports) - 1
    support_sets = [set(support) for support in supports]
    matrix: list[list[int]] = []
    for x in evaluation_set:
        incident = [index for index, support in enumerate(support_sets) if x in support]
        check(incident, f"coordinate {x} is absent from the support union")
        root = incident[0]
        powers = [pow(x, degree, prime) for degree in range(dimension)]
        for other in incident[1:]:
            row = [0] * (block_count * dimension)
            if root != 0:
                offset = (root - 1) * dimension
                for degree, value in enumerate(powers):
                    row[offset + degree] = value
            if other != 0:
                offset = (other - 1) * dimension
                for degree, value in enumerate(powers):
                    row[offset + degree] = (-value) % prime
            matrix.append(row)
    return matrix


def matrix_vector_product(
    matrix: list[list[int]], vector: list[int], prime: int
) -> list[int]:
    _, column_count = matrix_shape(matrix)
    check(len(vector) == column_count, "matrix-vector dimension mismatch")
    return [sum(a * b for a, b in zip(row, vector)) % prime for row in matrix]


def build_macaulay_matrix(
    complement_locators: list[list[int]], degree_bound: int, prime: int
) -> list[list[int]]:
    check(degree_bound >= 1, "Macaulay degree bound must be positive")
    locator_degrees = {len(poly_trim(poly)) - 1 for poly in complement_locators}
    check(len(locator_degrees) == 1, "complement locators have unequal degrees")
    locator_degree = next(iter(locator_degrees))
    output = [
        [0] * (len(complement_locators) * degree_bound)
        for _ in range(locator_degree + degree_bound)
    ]
    for index, poly in enumerate(complement_locators):
        for shift in range(degree_bound):
            column = index * degree_bound + shift
            for degree, coefficient in enumerate(poly):
                output[degree + shift][column] = coefficient % prime
    return output


def infer_forney_profile(nullities: dict[str, int], index_count: int) -> list[int]:
    kernel_dimensions = [0] + [nullities[str(degree)] for degree in range(1, 4)]
    previous_cumulative = 0
    profile: list[int] = []
    for degree_bound in range(1, 4):
        cumulative = (
            kernel_dimensions[degree_bound] - kernel_dimensions[degree_bound - 1]
        )
        exact_count = cumulative - previous_cumulative
        check(exact_count >= 0, "negative Forney-index multiplicity")
        profile.extend([degree_bound - 1] * exact_count)
        previous_cumulative = cumulative
    check(previous_cumulative == index_count, "Macaulay table misses a Forney index")
    check(len(profile) == index_count, "Forney profile has the wrong length")
    return profile


def validate_fixture_shape(data: dict[str, Any]) -> None:
    expected_top_keys = {
        "schema",
        "field",
        "evaluation_set",
        "dimension",
        "agreement",
        "received_word_exponent",
        "supports",
        "expected",
    }
    check(set(data) == expected_top_keys, "fixture top-level keys changed")
    check(data["schema"] == "rank16-left-kernel-forney-f31-v1", "fixture schema")
    require_int(data["field"], "field")
    require_int(data["dimension"], "dimension")
    require_int(data["agreement"], "agreement")
    require_int(data["received_word_exponent"], "received_word_exponent")
    require_list(data["evaluation_set"], "evaluation_set")
    require_list(data["supports"], "supports")
    require_dict(data["expected"], "expected")


def compute_fixture_result(data: dict[str, Any]) -> dict[str, Any]:
    validate_fixture_shape(data)
    prime = require_int(data["field"], "field")
    dimension = require_int(data["dimension"], "dimension")
    agreement = require_int(data["agreement"], "agreement")
    received_word_exponent = require_int(
        data["received_word_exponent"], "received_word_exponent"
    )

    check(prime == 31, "fixture field is not 31")
    check(all(prime % divisor for divisor in range(2, 6)), "fixture field is not prime")
    check(dimension == 15, "fixture dimension is not 15")
    check(agreement == 16, "fixture agreement is not 16")
    check(received_word_exponent == 16, "received word is not x^16")

    evaluation_values = require_list(data["evaluation_set"], "evaluation_set")
    check(
        all(type(value) is int for value in evaluation_values),
        "evaluation_set has a non-integer",
    )
    evaluation_set = tuple(evaluation_values)
    check(evaluation_set == tuple(range(1, prime)), "evaluation set is not F_31^*")

    support_rows = require_list(data["supports"], "supports")
    supports: list[tuple[int, ...]] = []
    for index, raw_support in enumerate(support_rows):
        row = require_list(raw_support, f"supports[{index}]")
        check(all(type(value) is int for value in row), f"support {index} is non-integral")
        support = tuple(row)
        check(len(support) == agreement, f"support {index} has the wrong size")
        check(tuple(sorted(set(support))) == support, f"support {index} is not sorted/unique")
        check(set(support) <= set(evaluation_set), f"support {index} leaves H")
        supports.append(support)
    supports_tuple = tuple(supports)
    check(len(supports_tuple) == 16, "fixture does not contain 16 supports")
    check(len(set(supports_tuple)) == len(supports_tuple), "supports are not distinct")

    zero_sum_count = sum(sum(support) % prime == 0 for support in supports_tuple)
    check(zero_sum_count == len(supports_tuple), "a support is not zero-sum")
    support_union = set().union(*(set(support) for support in supports_tuple))
    check(support_union == set(evaluation_set), "supports do not cover F_31^*")

    binomial_value = comb(len(evaluation_set), agreement)
    check(binomial_value == 145_422_675, "binomial(30,16) mismatch")
    list_count_numerator = binomial_value + (prime - 1)
    check(list_count_numerator % prime == 0, "character-filter numerator is not divisible")
    full_list_size = list_count_numerator // prime
    check(full_list_size == 4_691_055, "full zero-sum list size mismatch")

    listed_polynomials: list[list[int]] = []
    exact_agreement_count = 0
    for index, support in enumerate(supports_tuple):
        support_locator = locator(support, prime)
        check(len(support_locator) == 17, f"support locator {index} degree")
        check(support_locator[16] == 1, f"support locator {index} is not monic")
        check(support_locator[15] == 0, f"support locator {index} has x^15 term")
        polynomial = listed_polynomial(support, prime, received_word_exponent)
        check(len(polynomial) <= dimension, f"listed polynomial {index} has degree >=15")
        agreements = tuple(
            x
            for x in evaluation_set
            if poly_eval(polynomial, x, prime)
            == pow(x, received_word_exponent, prime)
        )
        check(agreements == support, f"listed polynomial {index} agreement set mismatch")
        exact_agreement_count += 1
        listed_polynomials.append(polynomial + [0] * (dimension - len(polynomial)))

    affine_differences = [
        [
            (listed_polynomials[index][degree] - listed_polynomials[0][degree])
            % prime
            for degree in range(dimension)
        ]
        for index in range(1, len(listed_polynomials))
    ]
    affine_rank = field_rank(affine_differences, prime)
    affine_determinant = field_determinant(affine_differences, prime)
    check(affine_rank == 15, "listed polynomials are not affinely independent")
    check(affine_determinant == 2, "affine determinant is not 2 mod 31")

    complement_locators = [
        locator(tuple(x for x in evaluation_set if x not in support), prime)
        for support in supports_tuple
    ]
    check(
        all(len(poly) == 15 and poly[-1] == 1 for poly in complement_locators),
        "a complement locator is not monic of degree 14",
    )
    complement_locator_span = field_rank(complement_locators, prime)
    dual_dimension = len(support_union) - dimension
    h = dual_dimension - complement_locator_span
    check(dual_dimension == 15, "shortened dual dimension mismatch")
    check(complement_locator_span == 14, "complement-locator span mismatch")
    check(h == 1, "shortened-dual codimension is not one")

    weights = lagrange_weights(evaluation_set, prime)
    syndrome = [
        sum(
            pow(x, received_word_exponent, prime)
            * weights[x]
            * pow(x, degree, prime)
            for x in evaluation_set
        )
        % prime
        for degree in range(dual_dimension)
    ]
    syndrome_nonzero = [degree for degree, value in enumerate(syndrome) if value]
    check(syndrome_nonzero == [13], "common syndrome has the wrong support")
    check(syndrome[13] == 1, "common syndrome has the wrong value")

    for index, (support, complement_locator) in enumerate(
        zip(supports_tuple, complement_locators)
    ):
        support_set = set(support)
        shortened_word = [
            weights[x] * poly_eval(complement_locator, x, prime) % prime
            for x in evaluation_set
        ]
        actual_support = {
            x for x, value in zip(evaluation_set, shortened_word) if value != 0
        }
        check(actual_support == support_set, f"shortened word {index} support mismatch")
        for degree in range(dimension):
            moment = sum(
                value * pow(x, degree, prime)
                for x, value in zip(evaluation_set, shortened_word)
            ) % prime
            check(moment == 0, f"shortened word {index} fails dual moment {degree}")
        syndrome_value = sum(
            pow(x, received_word_exponent, prime) * value
            for x, value in zip(evaluation_set, shortened_word)
        ) % prime
        check(syndrome_value == 0, f"common syndrome misses W_{index}")

    macaulay_ranks: dict[str, int] = {}
    macaulay_nullities: dict[str, int] = {}
    for degree_bound in range(1, 4):
        macaulay = build_macaulay_matrix(complement_locators, degree_bound, prime)
        macaulay_rank = field_rank(macaulay, prime)
        macaulay_ranks[str(degree_bound)] = macaulay_rank
        macaulay_nullities[str(degree_bound)] = (
            len(complement_locators) * degree_bound - macaulay_rank
        )
    forney_profile = infer_forney_profile(
        macaulay_nullities, len(complement_locators) - 1
    )
    sigma = agreement - dimension
    excess = sum(max(0, index - sigma) for index in forney_profile)
    bounded_syzygy_dimension = sum(
        max(0, sigma - index) for index in forney_profile
    )
    check(sum(forney_profile) == len(support_union) - agreement, "Forney sum is not e")
    check(excess == h, "Forney excess does not equal h")

    difference_matrix = build_difference_matrix(
        supports_tuple, evaluation_set, dimension, prime
    )
    matrix_rows, matrix_columns = matrix_shape(difference_matrix)
    matrix_rank = field_rank(difference_matrix, prime)
    right_nullity = matrix_columns - matrix_rank
    left_nullity = matrix_rows - matrix_rank
    check(matrix_rows == len(supports_tuple) * agreement - len(support_union), "row count")
    check(matrix_columns == (len(supports_tuple) - 1) * dimension, "column count")
    check(matrix_rank == matrix_columns - h, "rank/h identity")
    check(right_nullity == h, "right nullity/h identity")
    check(
        left_nullity
        == (len(supports_tuple) - 1) * sigma
        - (len(support_union) - agreement)
        + h,
        "left-nullity formula",
    )
    check(left_nullity == bounded_syzygy_dimension, "left nullity/Forney formula")

    kernel_witness: list[int] = []
    for index in range(1, len(listed_polynomials)):
        kernel_witness.extend(
            (
                listed_polynomials[index][degree] - listed_polynomials[0][degree]
            )
            % prime
            for degree in range(dimension)
        )
    check(any(kernel_witness), "affine kernel witness is zero")
    check(
        all(value == 0 for value in matrix_vector_product(difference_matrix, kernel_witness, prime)),
        "affine differences do not lie in the right kernel",
    )

    return {
        "full_list_size": full_list_size,
        "support_count": len(supports_tuple),
        "zero_sum_supports": zero_sum_count,
        "union_size": len(support_union),
        "exact_agreement_supports": exact_agreement_count,
        "affine_rank": affine_rank,
        "affine_determinant_mod_field": affine_determinant,
        "common_syndrome_nonzero_degree": syndrome_nonzero[0],
        "common_syndrome_value": syndrome[syndrome_nonzero[0]],
        "complement_locator_span": complement_locator_span,
        "h": h,
        "macaulay_ranks": macaulay_ranks,
        "macaulay_nullities": macaulay_nullities,
        "forney_profile": forney_profile,
        "matrix_rows": matrix_rows,
        "matrix_columns": matrix_columns,
        "matrix_rank": matrix_rank,
        "right_nullity": right_nullity,
        "left_nullity": left_nullity,
    }


def verify_expected(data: dict[str, Any], actual: dict[str, Any]) -> None:
    expected = require_dict(data["expected"], "expected")
    check(
        actual == expected,
        "fixture result mismatch\nexpected="
        + json.dumps(expected, sort_keys=True, separators=(",", ":"))
        + "\nactual="
        + json.dumps(actual, sort_keys=True, separators=(",", ":")),
    )


def compute_deployed_result() -> dict[str, int]:
    n = 2_097_152
    dimension = 1_048_576
    agreement = 1_116_047
    support_count = 16
    sigma = agreement - dimension
    radius = n - agreement
    rows_at_full_union = support_count * agreement - n
    columns = (support_count - 1) * dimension
    rank_if_h1 = columns - 1
    row_surplus = rows_at_full_union - columns
    forced_left_nullity = (support_count - 1) * sigma - radius + 1
    forced_mu_max_at_least = sigma + 1
    check(sigma == 67_471, "deployed sigma mismatch")
    check(radius == 981_105, "deployed radius mismatch")
    check(rows_at_full_union == 15_759_600, "deployed row count mismatch")
    check(columns == 15_728_640, "deployed column count mismatch")
    check(rank_if_h1 == 15_728_639, "deployed h=1 rank mismatch")
    check(row_surplus == 30_960, "deployed row surplus mismatch")
    check(forced_left_nullity == 30_961, "deployed forced left nullity mismatch")
    check(forced_mu_max_at_least == 67_472, "deployed Forney floor mismatch")
    return {
        "sigma": sigma,
        "radius": radius,
        "rows_at_full_union": rows_at_full_union,
        "columns": columns,
        "rank_if_h1": rank_if_h1,
        "row_surplus": row_surplus,
        "forced_left_nullity": forced_left_nullity,
        "forced_mu_max_at_least": forced_mu_max_at_least,
    }


def expect_rejection(label: str, action: Callable[[], None]) -> None:
    try:
        action()
    except VerificationError:
        return
    fail(f"tamper check {label} was accepted")


def run_tamper_checks(raw: bytes, data: dict[str, Any]) -> int:
    changed_raw = raw.replace(b'"field": 31', b'"field": 30', 1)
    check(changed_raw != raw, "digest tamper mutation did not change the fixture")
    expect_rejection("digest", lambda: verify_fixture_digest(changed_raw))

    changed_support = copy.deepcopy(data)
    changed_support["supports"][0][0] = 2
    expect_rejection("support", lambda: compute_fixture_result(changed_support))

    changed_expected = copy.deepcopy(data)
    changed_expected["expected"]["matrix_rank"] = 223

    def reject_changed_expected() -> None:
        actual = compute_fixture_result(changed_expected)
        verify_expected(changed_expected, actual)

    expect_rejection("claimed-rank", reject_changed_expected)
    return 3


def format_profile(profile: list[int]) -> str:
    check(profile == [0, 0] + [1] * 12 + [2], "unexpected profile formatting input")
    return "0x2,1x12,2x1"


def certificate_digest(fixture_result: dict[str, Any], deployed: dict[str, int]) -> str:
    canonical = json.dumps(
        {"deployed": deployed, "fixture": fixture_result},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("ascii")
    return sha256_bytes(canonical)


def print_transcript(
    fixture_result: dict[str, Any], deployed: dict[str, int], tamper_count: int
) -> None:
    print("RANK16_LEFT_KERNEL_FORNEY_ROUTE_CUT")
    print(f"fixture_sha256={EXPECTED_FIXTURE_SHA256}")
    print("field=31 domain=30 K=15 m=16 sigma=1 t=16")
    print(f"full_list_size={fixture_result['full_list_size']}")
    print(
        "supports="
        f"{fixture_result['support_count']} union={fixture_result['union_size']} "
        f"zero_sum={fixture_result['zero_sum_supports']} "
        f"exact_agreement={fixture_result['exact_agreement_supports']}"
    )
    print(
        f"affine_rank={fixture_result['affine_rank']} "
        "affine_determinant_mod_31="
        f"{fixture_result['affine_determinant_mod_field']}"
    )
    print(
        "common_syndrome_nonzero_degree="
        f"{fixture_result['common_syndrome_nonzero_degree']} "
        f"common_syndrome_value={fixture_result['common_syndrome_value']}"
    )
    print(
        f"complement_locator_span={fixture_result['complement_locator_span']} "
        f"h={fixture_result['h']}"
    )
    for degree_bound in range(1, 4):
        key = str(degree_bound)
        print(
            f"macaulay_D{degree_bound}=rank{fixture_result['macaulay_ranks'][key]},"
            f"nullity{fixture_result['macaulay_nullities'][key]}"
        )
    print(
        f"matrix_rows={fixture_result['matrix_rows']} "
        f"matrix_columns={fixture_result['matrix_columns']} "
        f"matrix_rank={fixture_result['matrix_rank']}"
    )
    print(
        f"right_nullity={fixture_result['right_nullity']} "
        f"left_nullity={fixture_result['left_nullity']}"
    )
    print(f"forney_profile={format_profile(fixture_result['forney_profile'])}")
    print(
        f"deployed_sigma={deployed['sigma']} "
        f"deployed_radius={deployed['radius']}"
    )
    print(
        f"deployed_rows_at_full_union={deployed['rows_at_full_union']} "
        f"deployed_columns={deployed['columns']}"
    )
    print(f"deployed_rank_if_h1={deployed['rank_if_h1']}")
    print(
        f"deployed_row_surplus={deployed['row_surplus']} "
        f"deployed_forced_left_nullity={deployed['forced_left_nullity']}"
    )
    print(f"deployed_forced_mu_max_at_least={deployed['forced_mu_max_at_least']}")
    print(f"tamper_checks={tamper_count}/3_rejected")
    print(f"certificate_sha256={certificate_digest(fixture_result, deployed)}")
    print("official_score=0/2")
    print("RESULT: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fixture",
        type=Path,
        default=DEFAULT_FIXTURE,
        help="path to the byte-pinned F31 fixture",
    )
    args = parser.parse_args()
    try:
        raw = args.fixture.read_bytes()
        verify_fixture_digest(raw)
        decoded = json.loads(raw.decode("ascii"))
        data = require_dict(decoded, "fixture")
        fixture_result = compute_fixture_result(data)
        verify_expected(data, fixture_result)
        deployed = compute_deployed_result()
        tamper_count = run_tamper_checks(raw, data)
        print_transcript(fixture_result, deployed, tamper_count)
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, VerificationError) as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
