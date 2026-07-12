#!/usr/bin/env python3
"""Hardened preflight for the A6 actual-witness core-rank argument.

This standard-library-only checker separates exact finite verification from
the two analytic inputs.  Finite-field ranks, zero masks, reconstruction,
binomial charges, and hypergeometric convolutions are exact.  Decimal
probability and entropy rows are supporting numerical checks only; the
Hoeffding and binary-entropy asymptotics require their stated analytic proofs.

Usage:
  python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py [--check]
  python3 experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py --tamper KIND

There are 14 semantic tamper kinds; see the usage emitted for a bad argument.
"""

import ast
import hashlib
import math
import random
import sys
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path


PR_PINS = {
    670: "08198f1b7c116710f3b0ba80d4bc00427ed0fe7a",
    676: "fe8b6ef7ac57a31228a347d38f6e8d2fbb7323dd",
    671: "b0ce6c57049fbafe749d1af1e3a6eef0f9de06e5",
}
EXPECTED_PR_PINS = {
    670: "08198f1b7c116710f3b0ba80d4bc00427ed0fe7a",
    676: "fe8b6ef7ac57a31228a347d38f6e8d2fbb7323dd",
    671: "b0ce6c57049fbafe749d1af1e3a6eef0f9de06e5",
}
RANDOM_SEED = 20260712

# Filled only after the deterministic census is stable.  Deliberately kept in
# one fail-closed table so a changed selector or lost coverage cannot pass.
EXPECTED_COUNTS = {
    "charts": 9,
    "vandermonde_minors": 124,
    "low_weight_vectors": 15078,
    "families": 156,
    "multiwitness_families": 147,
    "selector_rank_variations": 26,
    "safe_deletions": 131,
    "base_pairs": 1301,
    "nonminimum_base_pairs": 1006,
    "core_masks": 671,
    "h_subfamilies_positive": 3041,
    "h_subfamilies_rank_zero": 1386,
    "rank_zero_formula_failures": 10,
    "gh_rows": 18,
    "hypergeom_convolutions": 6,
    "general_linear_families": 2,
    "kappa_subsets": 8658,
    "k0_row_flats": 4599,
    "d_row_flats": 136821,
    "multiplicity_masks": 1205,
    "k0_bases": 3329,
    "d_bases": 1594,
    "extension_pairs": 3915,
    "multiplicity_bounds": 348,
    "integer_mds_bounds": 348,
    "integer_rounding_gains": 0,
    "old_ratio_crosschecks": 1205,
    "exact_e_subfamilies": 329,
    "exact_e_support_ceilings": 329,
    "minimum_affine_direction_differences": 139,
    "ell_tight_masks": 1094,
    "bollobas_families": 156,
    "bollobas_ordered_crossings": 2602,
    "bollobas_beats_mds": 102,
    "mds_beats_bollobas": 2,
    "bollobas_mds_ties": 49,
    "loose_budget_regressions": 1,
    "endpoint_e0_cases": 28,
    "endpoint_eM_cases": 35,
    "endpoint_zero_vectors": 35,
    "endpoint_compilations": 8000,
    "overlap_670_families": 156,
    "overlap_670_exact_certificates": 797,
    "overlap_670_equal": 48,
    "overlap_670_stronger": 1,
    "core_overlap_stronger": 1,
    "nonuniform_core_sums": 348,
    "nonuniform_core_mu_total": 1317,
    "nonuniform_670_equal": 37,
    "nonuniform_670_stronger": 6,
    "nonuniform_core_stronger": 7,
}
EXPECTED_RANK_HISTOGRAM = {0: 29, 1: 42, 2: 49, 3: 36}

ALLOWED_IMPORT_ROOTS = {
    "ast",
    "hashlib",
    "math",
    "random",
    "sys",
    "collections",
    "decimal",
    "fractions",
    "itertools",
    "pathlib",
}


class VerificationError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def add_vectors(first, second, modulus):
    return tuple((x + y) % modulus for x, y in zip(first, second))


def subtract_vectors(first, second, modulus):
    return tuple((x - y) % modulus for x, y in zip(first, second))


def scale_vector(scalar, vector, modulus):
    return tuple((scalar * x) % modulus for x in vector)


def linear_combination(coefficients, vectors, modulus, length=None):
    if vectors:
        result = [0] * len(vectors[0])
    else:
        require(length is not None, "empty combination needs ambient length")
        result = [0] * length
    for coefficient, vector in zip(coefficients, vectors):
        for index, value in enumerate(vector):
            result[index] = (result[index] + coefficient * value) % modulus
    return tuple(result)


def vector_weight(vector):
    return sum(value != 0 for value in vector)


def matrix_rank(matrix, modulus):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    require(all(len(row) == column_count for row in work), "ragged matrix")
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column] % modulus),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column] % modulus, -1, modulus)
        work[rank] = [(inverse * value) % modulus for value in work[rank]]
        for row in range(row_count):
            if row == rank:
                continue
            factor = work[row][column] % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == row_count:
            break
    return rank


def rref(matrix, modulus):
    if not matrix:
        return [], []
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivots = []
    active = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(active, row_count) if work[row][column] % modulus),
            None,
        )
        if pivot is None:
            continue
        work[active], work[pivot] = work[pivot], work[active]
        inverse = pow(work[active][column] % modulus, -1, modulus)
        work[active] = [(inverse * value) % modulus for value in work[active]]
        for row in range(row_count):
            if row == active:
                continue
            factor = work[row][column] % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[active])
                ]
        pivots.append(column)
        active += 1
        if active == row_count:
            break
    return work, pivots


def nullspace_basis(matrix, modulus, column_count=None):
    if not matrix:
        require(column_count is not None, "empty nullspace needs column count")
        return [
            tuple(1 if index == free else 0 for index in range(column_count))
            for free in range(column_count)
        ]
    reduced, pivots = rref(matrix, modulus)
    width = len(matrix[0])
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free]) % modulus
        basis.append(tuple(vector))
    return basis


def determinant(matrix, modulus):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "determinant not square")
    work = [list(row) for row in matrix]
    value = 1
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if work[row][column] % modulus),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            value = -value
        pivot_value = work[column][column] % modulus
        value = value * pivot_value % modulus
        inverse = pow(pivot_value, -1, modulus)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % modulus
            for later in range(column, size):
                work[row][later] = (
                    work[row][later] - factor * work[column][later]
                ) % modulus
    return value % modulus


def solve_square(matrix, right_hand_side, modulus):
    size = len(matrix)
    require(size == len(right_hand_side), "solve dimension mismatch")
    require(determinant(matrix, modulus) != 0, "solve matrix singular")
    work = [
        [value % modulus for value in row] + [rhs % modulus]
        for row, rhs in zip(matrix, right_hand_side)
    ]
    for column in range(size):
        pivot = next(
            row for row in range(column, size) if work[row][column] % modulus
        )
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, modulus)
        work[column] = [(inverse * value) % modulus for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column] % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[column])
                ]
    return tuple(work[index][-1] for index in range(size))


def column_basis(vectors, modulus):
    basis = []
    old_rank = 0
    for vector in vectors:
        new_rank = matrix_rank(basis + [vector], modulus)
        if new_rank > old_rank:
            basis.append(tuple(vector))
            old_rank = new_rank
    return basis


def same_span(first, second, modulus):
    first_basis = column_basis(first, modulus)
    second_basis = column_basis(second, modulus)
    combined = column_basis(first_basis + second_basis, modulus)
    return len(first_basis) == len(second_basis) == len(combined)


def mat_vec(matrix, vector, modulus):
    return tuple(
        sum(value * coefficient for value, coefficient in zip(row, vector))
        % modulus
        for row in matrix
    )


def vandermonde_matrix(modulus, points, redundancy, weights):
    require(len(points) == len(weights), "point/weight length mismatch")
    require(len(set(points)) == len(points), "evaluation points not distinct")
    require(all(weight % modulus for weight in weights), "zero parity weight")
    return tuple(
        tuple(
            weights[column] * pow(points[column], row, modulus) % modulus
            for column in range(len(points))
        )
        for row in range(redundancy)
    )


def matrix_columns(matrix):
    if not matrix:
        return ()
    return tuple(tuple(row[index] for row in matrix) for index in range(len(matrix[0])))


def span_contains(columns, vector, modulus):
    return matrix_rank(list(columns), modulus) == matrix_rank(
        list(columns) + [tuple(vector)], modulus
    )


def is_transverse(chart, y_zero, y_one, witness):
    support = [index for index, value in enumerate(witness) if value]
    columns = [chart["columns"][index] for index in support]
    return not (
        span_contains(columns, y_zero, chart["p"])
        and span_contains(columns, y_one, chart["p"])
    )


def enumerate_low_weight(length, radius, modulus):
    zero = (0,) * length
    yield zero
    nonzero = tuple(range(1, modulus))
    for weight in range(1, radius + 1):
        for support in combinations(range(length), weight):
            for values in product(nonzero, repeat=weight):
                vector = [0] * length
                for index, value in zip(support, values):
                    vector[index] = value
                yield tuple(vector)


def build_chart(modulus, length, redundancy, radius, weights):
    require(radius < redundancy, "the completed witness chart needs t<R")
    require(length <= modulus, "not enough prime-field evaluation points")
    points = tuple(range(length))
    matrix = vandermonde_matrix(modulus, points, redundancy, weights)
    columns = matrix_columns(matrix)
    kernel = nullspace_basis(matrix, modulus)
    require(len(kernel) == length - redundancy, "kernel dimension mismatch")
    low_vectors = list(enumerate_low_weight(length, radius, modulus))
    expected_low = sum(
        math.comb(length, weight) * (modulus - 1) ** weight
        for weight in range(radius + 1)
    )
    require(len(low_vectors) == expected_low, "low-weight census count changed")
    buckets = defaultdict(list)
    for vector in low_vectors:
        buckets[mat_vec(matrix, vector, modulus)].append(vector)
    for syndrome in buckets:
        buckets[syndrome].sort()
    return {
        "p": modulus,
        "N": length,
        "R": redundancy,
        "kappa": length - redundancy,
        "t": radius,
        "points": points,
        "weights": tuple(weights),
        "H": matrix,
        "columns": columns,
        "kernel": tuple(kernel),
        "low_vectors": tuple(low_vectors),
        "buckets": buckets,
        "name": (
            f"F{modulus}-N{length}-R{redundancy}-t{radius}-"
            + ("unweighted" if len(set(weights)) == 1 else "weighted")
        ),
    }

def check_vandermonde_and_generalized_weights(chart, expected_shift=0):
    modulus = chart["p"]
    length = chart["N"]
    redundancy = chart["R"]
    kappa = chart["kappa"]
    minor_count = 0
    for selected in combinations(range(length), redundancy):
        square = [
            [chart["H"][row][column] for column in selected]
            for row in range(redundancy)
        ]
        require(determinant(square, modulus) != 0, "Vandermonde MDS minor vanished")
        minor_count += 1

    generalized = []
    kernel = chart["kernel"]
    for dimension in range(1, kappa + 1):
        minimum_support = None
        for support_size in range(length + 1):
            found = False
            for support in combinations(range(length), support_size):
                support_set = set(support)
                outside_rows = [
                    tuple(kernel[column][coordinate] for column in range(kappa))
                    for coordinate in range(length)
                    if coordinate not in support_set
                ]
                shortened_dimension = kappa - matrix_rank(outside_rows, modulus)
                if shortened_dimension >= dimension:
                    minimum_support = support_size
                    found = True
                    break
            if found:
                break
        expected = redundancy + dimension + (
            expected_shift if dimension == 1 else 0
        )
        require(
            minimum_support == expected,
            (
                f"generalized-Hamming mismatch in {chart['name']}: "
                f"d_{dimension}={minimum_support}, expected {expected}"
            ),
        )
        generalized.append(minimum_support)
    return minor_count, generalized


def intrinsic_core(slopes, witnesses, modulus, ambient_length):
    size = len(slopes)
    differences = tuple(
        subtract_vectors(witness, witnesses[0], modulus)
        for witness in witnesses[1:]
    ) if witnesses else ()
    affine_span = tuple(column_basis(differences, modulus))
    if size <= 1:
        return {
            "E": (),
            "theta_images": (),
            "W": (),
            "r": 0,
            "D": affine_span,
            "s": len(affine_span),
        }
    coefficient_constraints = [
        tuple(1 for _ in slopes),
        tuple(slopes),
    ]
    e_basis = nullspace_basis(coefficient_constraints, modulus)
    require(len(e_basis) == size - 2, "affine-relation dimension mismatch")
    theta_images = tuple(
        linear_combination(coefficients, witnesses, modulus, ambient_length)
        for coefficients in e_basis
    )
    w_basis = tuple(column_basis(theta_images, modulus))
    return {
        "E": tuple(e_basis),
        "theta_images": theta_images,
        "W": w_basis,
        "r": len(w_basis),
        "D": affine_span,
        "s": len(affine_span),
    }


def interpolate_base(slopes, witnesses, first_index, second_index, modulus):
    alpha = slopes[first_index]
    beta = slopes[second_index]
    denominator = (beta - alpha) % modulus
    require(denominator != 0, "base slopes collided")
    inverse = pow(denominator, -1, modulus)
    direction = scale_vector(
        inverse,
        subtract_vectors(witnesses[second_index], witnesses[first_index], modulus),
        modulus,
    )
    intercept = subtract_vectors(
        witnesses[first_index], scale_vector(alpha, direction, modulus), modulus
    )
    residuals = tuple(
        subtract_vectors(
            subtract_vectors(witness, intercept, modulus),
            scale_vector(slope, direction, modulus),
            modulus,
        )
        for slope, witness in zip(slopes, witnesses)
    )
    return intercept, direction, residuals


def minimum_coset_weight(direction, kernel_basis, modulus):
    minimum = len(direction) + 1
    for coefficients in product(range(modulus), repeat=len(kernel_basis)):
        kernel_word = linear_combination(
            coefficients, kernel_basis, modulus, len(direction)
        )
        candidate = add_vectors(direction, kernel_word, modulus)
        minimum = min(minimum, vector_weight(candidate))
    return minimum


def zero_mask(witness):
    return tuple(index for index, value in enumerate(witness) if value == 0)


def restriction_rows(basis, coordinates):
    return [
        tuple(vector[coordinate] for vector in basis)
        for coordinate in coordinates
    ]


def lex_nonzero_minor(basis, coordinates, modulus):
    size = len(basis)
    for selected in combinations(coordinates, size):
        square = restriction_rows(basis, selected)
        if determinant(square, modulus):
            return tuple(selected), square
    raise VerificationError("full-rank zero mask had no nonzero core minor")


def syndrome_line_candidates(chart, first, second):
    modulus = chart["p"]
    y_zero = mat_vec(chart["H"], first, modulus)
    y_at_one = mat_vec(chart["H"], second, modulus)
    y_one = subtract_vectors(y_at_one, y_zero, modulus)
    if not any(y_one):
        return None
    slopes = []
    candidates = []
    for gamma in range(modulus):
        target = add_vectors(y_zero, scale_vector(gamma, y_one, modulus), modulus)
        transverse = tuple(
            witness
            for witness in chart["buckets"].get(target, ())
            if is_transverse(chart, y_zero, y_one, witness)
        )
        if transverse:
            slopes.append(gamma)
            candidates.append(transverse)
    if len(slopes) < 2:
        return None
    return {
        "chart": chart,
        "y0": y_zero,
        "y1": y_one,
        "slopes": tuple(slopes),
        "candidates": tuple(candidates),
    }


def select_line_family(line, mode):
    selected = []
    multi = False
    for slope, candidates in zip(line["slopes"], line["candidates"]):
        multi = multi or len(candidates) > 1
        if mode == 0:
            index = 0
        elif mode == 1:
            index = len(candidates) - 1
        elif mode == 2:
            index = len(candidates) // 2
        else:
            index = (3 * slope + mode) % len(candidates)
        selected.append(candidates[index])
    return {
        "chart": line["chart"],
        "y0": line["y0"],
        "y1": line["y1"],
        "slopes": line["slopes"],
        "witnesses": tuple(selected),
        "multi_available": multi,
        "selector_mode": mode,
        "global_slopes": line["slopes"],
        "global_witnesses": tuple(selected),
        "deleted": False,
    }


def restrict_family(family, indices, deletion=True):
    return {
        "chart": family["chart"],
        "y0": family["y0"],
        "y1": family["y1"],
        "slopes": tuple(family["slopes"][index] for index in indices),
        "witnesses": tuple(family["witnesses"][index] for index in indices),
        "multi_available": family["multi_available"],
        "selector_mode": family["selector_mode"],
        "global_slopes": family.get("global_slopes", family["slopes"]),
        "global_witnesses": family.get("global_witnesses", family["witnesses"]),
        "deleted": deletion,
    }


def lightweight_rank(family):
    chart = family["chart"]
    return intrinsic_core(
        family["slopes"], family["witnesses"], chart["p"], chart["N"]
    )["r"]


def discover_chart_families(chart, desired_lines=2):
    seed = RANDOM_SEED + chart["p"] * 1000 + chart["N"] * 100 + chart["R"]
    rng = random.Random(seed)
    vectors = chart["low_vectors"]
    lines = []
    seen_lines = set()
    attempts = 0
    while len(lines) < desired_lines and attempts < 30000:
        attempts += 1
        first = vectors[rng.randrange(len(vectors))]
        second = vectors[rng.randrange(len(vectors))]
        if first == second:
            continue
        line = syndrome_line_candidates(chart, first, second)
        if line is None or len(line["slopes"]) < min(5, chart["p"]):
            continue
        line_key = (line["y0"], line["y1"], line["slopes"])
        if line_key in seen_lines:
            continue
        trial = [select_line_family(line, mode) for mode in range(4)]
        ranks = {
            lightweight_rank(
                restrict_family(family, tuple(range(min(5, len(family["slopes"])))))
            )
            for family in trial
        }
        if not ranks.intersection({1, 2, 3}):
            continue
        lines.append(line)
        seen_lines.add(line_key)
    require(
        len(lines) == desired_lines,
        f"could not discover enough rich actual lines in {chart['name']}",
    )

    families = []
    signatures = set()
    for line in lines:
        selected_modes = [select_line_family(line, mode) for mode in range(4)]
        for family in selected_modes:
            size = len(family["slopes"])
            index_sets = [tuple(range(size))]
            for prefix in range(2, min(size, 6) + 1):
                index_sets.append(tuple(range(prefix)))
            if size >= 4:
                index_sets.extend(
                    [
                        tuple(range(1, size)),
                        tuple(index for index in range(size) if index % 2 == 0),
                        tuple(index for index in range(size) if index != size // 2),
                    ]
                )
            for indices in index_sets:
                if len(indices) < 2:
                    continue
                candidate = restrict_family(
                    family, indices, deletion=(len(indices) != size)
                )
                signature = (
                    candidate["slopes"],
                    candidate["witnesses"],
                    candidate["y0"],
                    candidate["y1"],
                )
                if signature not in signatures:
                    signatures.add(signature)
                    families.append(candidate)
    require(families, f"no selected families in {chart['name']}")
    return families


def vector_in_span(vector, basis, modulus):
    return matrix_rank(list(basis), modulus) == matrix_rank(
        list(basis) + [tuple(vector)], modulus
    )


def kernel_intersection_with_span(span_basis, matrix, modulus):
    if not span_basis:
        return ()
    image_columns = [mat_vec(matrix, vector, modulus) for vector in span_basis]
    coefficient_kernel = nullspace_basis(
        [tuple(column[row] for column in image_columns) for row in range(len(matrix))],
        modulus,
    )
    vectors = [
        linear_combination(coefficients, span_basis, modulus, len(span_basis[0]))
        for coefficients in coefficient_kernel
    ]
    return tuple(column_basis(vectors, modulus))



SUBSPACE_CACHE = {}


def minimum_lift_vector(chart, syndrome):
    modulus = chart["p"]
    key = tuple(syndrome)
    cache = chart.setdefault("minimum_lift_vectors", {})
    if key in cache:
        return cache[key]
    redundancy = chart["R"]
    length = chart["N"]
    square = [
        [chart["H"][row][column] for column in range(redundancy)]
        for row in range(redundancy)
    ]
    coefficients = solve_square(square, syndrome, modulus)
    particular = tuple(coefficients) + (0,) * (length - redundancy)
    best = None
    for kernel_coefficients in product(
        range(modulus), repeat=len(chart["kernel"])
    ):
        kernel_word = linear_combination(
            kernel_coefficients, chart["kernel"], modulus, length
        )
        candidate = add_vectors(particular, kernel_word, modulus)
        candidate_key = (vector_weight(candidate), candidate)
        if best is None or candidate_key < best:
            best = candidate_key
    require(best is not None, "minimum-lift coset was empty")
    require(
        mat_vec(chart["H"], best[1], modulus) == key,
        "minimum lift has wrong syndrome",
    )
    cache[key] = best[1]
    return best[1]


def all_rref_subspaces(modulus, ambient_dimension, dimension):
    key = (modulus, ambient_dimension, dimension)
    if key in SUBSPACE_CACHE:
        return SUBSPACE_CACHE[key]
    require(0 <= dimension <= ambient_dimension, "subspace dimension out of range")
    spaces = []
    for pivots in combinations(range(ambient_dimension), dimension):
        variable_positions = [
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in range(pivot + 1, ambient_dimension)
            if column not in pivots
        ]
        for values in product(range(modulus), repeat=len(variable_positions)):
            matrix = [
                [0] * ambient_dimension for _ in range(dimension)
            ]
            for row, pivot in enumerate(pivots):
                matrix[row][pivot] = 1
            for (row, column), value in zip(variable_positions, values):
                matrix[row][column] = value
            space = tuple(tuple(row) for row in matrix)
            require(matrix_rank(space, modulus) == dimension, "RREF rank changed")
            spaces.append(space)
    expected = 1
    if dimension:
        numerator = math.prod(
            modulus ** (ambient_dimension - index) - 1
            for index in range(dimension)
        )
        denominator = math.prod(
            modulus ** (dimension - index) - 1
            for index in range(dimension)
        )
        require(numerator % denominator == 0, "Gaussian binomial not integral")
        expected = numerator // denominator
    require(len(spaces) == expected, "RREF subspace census changed")
    SUBSPACE_CACHE[key] = tuple(spaces)
    return SUBSPACE_CACHE[key]


def support_size_of_space(space_basis):
    if not space_basis:
        return 0
    return sum(
        any(vector[coordinate] for vector in space_basis)
        for coordinate in range(len(space_basis[0]))
    )


def coordinate_row(space_basis, coordinate):
    return tuple(vector[coordinate] for vector in space_basis)


def coordinate_basis_sets(space_basis, coordinates, modulus):
    dimension = len(space_basis)
    if dimension == 0:
        return ((),)
    result = []
    for selected in combinations(coordinates, dimension):
        square = [
            coordinate_row(space_basis, coordinate)
            for coordinate in selected
        ]
        if determinant(square, modulus):
            result.append(tuple(selected))
    return tuple(result)


def subcode_annihilating_flat(code_basis, flat, modulus):
    dimension = len(code_basis)
    annihilator = nullspace_basis(
        list(flat), modulus, column_count=dimension
    )
    words = [
        linear_combination(
            coefficients,
            code_basis,
            modulus,
            len(code_basis[0]) if code_basis else 0,
        )
        for coefficients in annihilator
    ]
    return tuple(column_basis(words, modulus))


def audit_row_flat_caps(chart, core, minimum_weight, stats, cap_shift=0):
    modulus = chart["p"]
    length = chart["N"]
    redundancy = chart["R"]
    kappa = chart["kappa"]
    r_value = core["r"]
    s_value = core["s"]

    for flat_dimension in range(r_value):
        cap = kappa - r_value + flat_dimension + cap_shift
        for flat in all_rref_subspaces(modulus, r_value, flat_dimension):
            rows_in_flat = sum(
                vector_in_span(
                    coordinate_row(core["W"], coordinate), flat, modulus
                )
                for coordinate in range(length)
            )
            require(rows_in_flat <= cap, "K0 row-flat MDS cap failed")
            subcode = subcode_annihilating_flat(
                core["W"], flat, modulus
            )
            require(
                len(subcode) == r_value - flat_dimension,
                "K0 flat annihilator dimension changed",
            )
            require(
                support_size_of_space(subcode)
                >= redundancy + r_value - flat_dimension,
                "K0 generalized-weight support failed",
            )
            stats["k0_row_flats"] += 1

    for flat_dimension in range(r_value + 1):
        if flat_dimension < r_value:
            cap = kappa - r_value + flat_dimension + cap_shift
            support_floor = redundancy + r_value - flat_dimension
        else:
            cap = length - minimum_weight + cap_shift
            support_floor = minimum_weight
        for flat in all_rref_subspaces(modulus, s_value, flat_dimension):
            rows_in_flat = sum(
                vector_in_span(
                    coordinate_row(core["D"], coordinate), flat, modulus
                )
                for coordinate in range(length)
            )
            require(rows_in_flat <= cap, "D relative row-flat cap failed")
            subcode = subcode_annihilating_flat(
                core["D"], flat, modulus
            )
            require(
                len(subcode) == s_value - flat_dimension,
                "D flat annihilator dimension changed",
            )
            require(
                support_size_of_space(subcode) >= support_floor,
                "D relative generalized-weight support failed",
            )
            stats["d_row_flats"] += 1


def validate_bollobas_pairs(
    family,
    core,
    stats=None,
    claimed_support_sizes=None,
    require_all_crossings=True,
):
    chart = family["chart"]
    modulus = chart["p"]
    length = chart["N"]
    s_value = core["s"]
    witnesses = family["witnesses"]
    slopes = family["slopes"]
    basis_labels = []
    supports = []
    actual_sizes = []
    for witness in witnesses:
        mask = zero_mask(witness)
        label, _ = lex_nonzero_minor(core["D"], mask, modulus)
        support = tuple(
            coordinate for coordinate, value in enumerate(witness) if value
        )
        require(not set(label) & set(support), "Bollobas diagonal disjointness")
        basis_labels.append(label)
        supports.append(support)
        actual_sizes.append(len(support))

    if claimed_support_sizes is not None:
        require(
            tuple(claimed_support_sizes) == tuple(actual_sizes),
            "punctured weight substituted for total witness support",
        )

    crossing_count = 0
    for first in range(len(slopes)):
        for second in range(len(slopes)):
            if first == second:
                continue
            intersects = bool(set(basis_labels[first]) & set(supports[second]))
            if require_all_crossings:
                require(intersects, "ordered Bollobas cross-intersection failed")
            crossing_count += intersects

    reciprocal_sum = sum(
        (
            Fraction(1, math.comb(s_value + support_size, s_value))
            for support_size in actual_sizes
        ),
        Fraction(0, 1),
    )
    require(reciprocal_sum <= 1, "nonuniform Bollobas inequality failed")
    maximum_support = max(actual_sizes, default=0)
    require(
        s_value <= length - maximum_support,
        "max-support mask cannot detect D",
    )
    actual_bound = math.comb(s_value + maximum_support, s_value)
    coarse_bound = math.comb(s_value + chart["t"], s_value)
    require(len(slopes) <= actual_bound, "actual-support Bollobas bound failed")
    require(actual_bound <= math.comb(length, s_value), "Bollobas/direct order")
    require(len(slopes) <= coarse_bound, "coarse support-budget bound failed")

    if stats is not None:
        stats["bollobas_families"] += 1
        stats["bollobas_ordered_crossings"] += crossing_count
    return {
        "labels": tuple(basis_labels),
        "supports": tuple(supports),
        "sum": reciprocal_sum,
        "actual_bound": actual_bound,
        "coarse_bound": coarse_bound,
        "maximum_support": maximum_support,
    }


def audit_basis_multiplicity(
    family,
    core,
    minimum_lift,
    q_certificates,
    stats,
    check_flats=True,
):
    chart = family["chart"]
    modulus = chart["p"]
    length = chart["N"]
    kappa = chart["kappa"]
    r_value = core["r"]
    s_value = core["s"]
    size = len(family["slopes"])
    if size <= 1:
        require(s_value == r_value == 0, "singleton multiplicity edge changed")
        require(size <= math.comb(length, 0), "singleton direct bound failed")
        return ()

    require(s_value == r_value + 1, "multiplicity requires s=r+1")
    minimum_weight = vector_weight(minimum_lift)
    require(minimum_weight <= chart["R"], "minimum y1 lift exceeds R")
    if check_flats:
        audit_row_flat_caps(chart, core, minimum_weight, stats)

    all_coordinates = tuple(range(length))
    for selected in combinations(all_coordinates, kappa):
        bases = coordinate_basis_sets(core["W"], selected, modulus)
        require(bases, "a kappa-subset contains no K0 row basis")
        stats["kappa_subsets"] += 1

    masks = tuple(zero_mask(witness) for witness in family["witnesses"])
    actual_q = min(len(mask) for mask in masks)
    certificates = sorted(set(q_certificates) | {actual_q, length - chart["t"]})
    for q_value in certificates:
        require(q_value <= actual_q, "uncertified zero-mask lower bound q")
        require(
            q_value >= kappa + 1,
            "q must be at least kappa+1 for the MDS basis count",
        )

    seen_d_bases = {}
    nonuniform_mu_sum = 0
    for slope, mask in zip(family["slopes"], masks):
        mask_size = len(mask)
        k_bases = coordinate_basis_sets(core["W"], mask, modulus)
        d_bases = coordinate_basis_sets(core["D"], mask, modulus)
        require(k_bases and d_bases, "mask lost a required row basis")
        stats["multiplicity_masks"] += 1
        stats["k0_bases"] += len(k_bases)
        stats["d_bases"] += len(d_bases)

        strong_denominator = math.comb(
            mask_size - kappa + r_value, r_value
        )
        require(
            len(k_bases) >= strong_denominator,
            "greedy K0 basis multiplicity failed",
        )
        require(
            len(k_bases) * math.comb(kappa, r_value)
            >= math.comb(mask_size, r_value),
            "older kappa-subset double count failed",
        )
        require(
            strong_denominator * math.comb(kappa, r_value)
            >= math.comb(mask_size, r_value),
            "strong K0 count did not dominate old ratio",
        )
        stats["old_ratio_crosschecks"] += 1

        d_basis_set = set(d_bases)
        pair_multiplicity = defaultdict(int)
        extension_total = 0
        ell_mask = max(1, minimum_weight + mask_size - length)
        mask_mu = (
            ell_mask * strong_denominator + s_value - 1
        ) // s_value
        nonuniform_mu_sum += mask_mu
        minimum_extensions = None
        for k_basis in k_bases:
            extension_count = 0
            k_set = set(k_basis)
            for coordinate in mask:
                if coordinate in k_set:
                    continue
                d_basis = tuple(sorted(k_basis + (coordinate,)))
                if d_basis in d_basis_set:
                    extension_count += 1
                    extension_total += 1
                    pair_multiplicity[d_basis] += 1
            require(
                extension_count >= ell_mask,
                "a K0 basis has too few D-basis extensions",
            )
            minimum_extensions = (
                extension_count
                if minimum_extensions is None
                else min(minimum_extensions, extension_count)
            )
        require(
            extension_total >= ell_mask * len(k_bases),
            "extension-pair lower count failed",
        )
        require(
            all(count <= s_value for count in pair_multiplicity.values()),
            "a D basis was counted by more than s extension pairs",
        )
        require(
            len(d_bases) * s_value
            >= ell_mask * strong_denominator,
            "direct greedy D-basis count failed",
        )
        stats["extension_pairs"] += extension_total
        stats["ell_tight_masks"] += minimum_extensions == ell_mask

        for d_basis in d_bases:
            if d_basis in seen_d_bases:
                require(
                    seen_d_bases[d_basis] == slope,
                    "D-basis label reused across distinct slopes",
                )
            seen_d_bases[d_basis] = slope

    require(
        nonuniform_mu_sum <= math.comb(length, s_value),
        "exact nonuniform actual-core multiplicity sum failed",
    )
    stats["nonuniform_core_sums"] += 1
    stats["nonuniform_core_mu_total"] += nonuniform_mu_sum

    bounds = []
    for q_value in certificates:
        ell_q = max(1, minimum_weight + q_value - length)
        strong_denominator = math.comb(
            q_value - kappa + r_value, r_value
        )
        require(
            strong_denominator * math.comb(kappa, r_value)
            >= math.comb(q_value, r_value),
            "strong denominator did not dominate old ratio at q",
        )
        require(
            size * ell_q * strong_denominator
            <= s_value * math.comb(length, s_value),
            "strong MDS multiplicity slope bound failed",
        )
        require(
            size * ell_q * math.comb(q_value, r_value)
            <= (
                s_value
                * math.comb(length, s_value)
                * math.comb(kappa, r_value)
            ),
            "old MDS multiplicity slope bound failed",
        )
        ambient_basis_count = math.comb(length, s_value)
        bound = Fraction(
            s_value * ambient_basis_count,
            ell_q * strong_denominator,
        )
        mu_value = (
            ell_q * strong_denominator + s_value - 1
        ) // s_value
        integer_bound = ambient_basis_count // mu_value
        require(
            size <= integer_bound,
            "exact integer MDS multiplicity bound failed",
        )
        require(
            integer_bound <= bound.numerator // bound.denominator,
            "integer MDS bound did not refine rational floor",
        )
        bounds.append((q_value, ell_q, bound, mu_value, integer_bound))
        stats["multiplicity_bounds"] += 1
        stats["integer_mds_bounds"] += 1
        stats["integer_rounding_gains"] += (
            integer_bound < bound.numerator // bound.denominator
        )
    require(
        size <= math.comb(length, s_value),
        "direct affine-minor bound changed",
    )
    return tuple(bounds)


def audit_exact_e_multiplicity(family, minimum_lift, stats):
    chart = family["chart"]
    length = chart["N"]
    d_value = vector_weight(minimum_lift)
    support_j = {
        coordinate for coordinate, value in enumerate(minimum_lift) if value
    }
    outside = tuple(
        coordinate for coordinate in range(length) if coordinate not in support_j
    )
    m_length = length - d_value
    groups = defaultdict(list)
    for index, witness in enumerate(family["witnesses"]):
        exact_weight = sum(witness[coordinate] != 0 for coordinate in outside)
        groups[exact_weight].append(index)
    for exact_weight, indices in groups.items():
        subfamily = restrict_family(family, tuple(indices), deletion=True)
        h_value = max(1, d_value + exact_weight - chart["t"])
        q_exact = m_length - exact_weight + h_value
        require(
            all(len(zero_mask(witness)) >= q_exact
                for witness in subfamily["witnesses"]),
            "exact-e zero-mask certificate failed",
        )
        stats["exact_e_subfamilies"] += 1
        core = intrinsic_core(
            subfamily["slopes"],
            subfamily["witnesses"],
            chart["p"],
            length,
        )
        weight_ceiling = exact_weight + d_value - h_value
        require(
            weight_ceiling == length - q_exact,
            "exact-e support ceiling is not N-q_e",
        )
        require(
            all(vector_weight(witness) <= weight_ceiling
                for witness in subfamily["witnesses"]),
            "actual witness exceeded exact-e support ceiling",
        )
        pair_bound = validate_bollobas_pairs(subfamily, core)
        require(
            pair_bound["actual_bound"]
            <= math.comb(core["s"] + weight_ceiling, core["s"]),
            "exact-e Bollobas ceiling failed",
        )
        stats["exact_e_support_ceilings"] += 1
        if len(indices) >= 2:
            bounds = audit_basis_multiplicity(
                subfamily,
                core,
                minimum_lift,
                (q_exact,),
                stats,
                check_flats=False,
            )
            expected_ell = max(1, d_value - chart["t"])
            q_entry = next(row for row in bounds if row[0] == q_exact)
            require(
                q_entry[1] == expected_ell,
                "ell_e simplification max(1,h_e-e) failed",
            )


def build_binary_mds_chart():
    modulus = 2
    matrix = (
        (1, 0, 1),
        (0, 1, 1),
    )
    kernel = tuple(nullspace_basis(matrix, modulus))
    low_vectors = tuple(enumerate_low_weight(3, 1, modulus))
    buckets = defaultdict(list)
    for vector in low_vectors:
        buckets[mat_vec(matrix, vector, modulus)].append(vector)
    return {
        "p": 2,
        "N": 3,
        "R": 2,
        "kappa": 1,
        "t": 1,
        "points": (),
        "weights": (),
        "H": matrix,
        "columns": matrix_columns(matrix),
        "kernel": kernel,
        "low_vectors": low_vectors,
        "buckets": buckets,
        "name": "F2-N3-R2-t1-extended-MDS",
    }


def binary_mds_families():
    chart = build_binary_mds_chart()
    c_zero = unit_vector(3, 0)
    c_one = unit_vector(3, 1)
    y_zero = mat_vec(chart["H"], c_zero, 2)
    y_one = mat_vec(chart["H"], subtract_vectors(c_one, c_zero, 2), 2)
    pair = {
        "chart": chart,
        "y0": y_zero,
        "y1": y_one,
        "slopes": (0, 1),
        "witnesses": (c_zero, c_one),
        "multi_available": False,
        "selector_mode": 0,
        "global_slopes": (0, 1),
        "global_witnesses": (c_zero, c_one),
        "deleted": False,
    }
    empty = (0, 0, 0)
    empty_singleton = {
        "chart": chart,
        "y0": (0, 0),
        "y1": chart["columns"][0],
        "slopes": (0,),
        "witnesses": (empty,),
        "multi_available": False,
        "selector_mode": 0,
        "global_slopes": (0,),
        "global_witnesses": (empty,),
        "deleted": False,
    }
    return chart, (pair, empty_singleton)



def mds_beats_bollobas_fixture():
    chart = build_chart(7, 5, 4, 2, (1, 1, 1, 1, 1))
    for first_values in product(range(1, 7), repeat=2):
        first = (first_values[0], first_values[1], 0, 0, 0)
        for second_values in product(range(1, 7), repeat=2):
            second = (0, 0, second_values[0], second_values[1], 0)
            y_zero = mat_vec(chart["H"], first, 7)
            y_one = mat_vec(
                chart["H"], subtract_vectors(second, first, 7), 7
            )
            if not any(y_one):
                continue
            family = {
                "chart": chart,
                "y0": y_zero,
                "y1": y_one,
                "slopes": (0, 1),
                "witnesses": (first, second),
                "multi_available": False,
                "selector_mode": 0,
                "global_slopes": (0, 1),
                "global_witnesses": (first, second),
                "deleted": False,
            }
            if not all(
                is_transverse(chart, y_zero, y_one, witness)
                for witness in family["witnesses"]
            ):
                continue
            minimum_lift = minimum_lift_vector(chart, y_one)
            if vector_weight(minimum_lift) != 4:
                continue
            core = intrinsic_core(
                family["slopes"], family["witnesses"], 7, 5
            )
            require(core["r"] == 0 and core["s"] == 1, "comparison rank")
            q_value = 3
            ell_value = 2
            mds_bound = Fraction(5, 2)
            bollobas_bound = math.comb(3, 1)
            require(
                Fraction(
                    core["s"] * math.comb(5, core["s"]),
                    ell_value
                    * math.comb(
                        q_value - chart["kappa"] + core["r"], core["r"]
                    ),
                )
                == mds_bound,
                "comparison MDS arithmetic changed",
            )
            require(mds_bound < bollobas_bound, "comparison order changed")
            return chart, family
    raise VerificationError("could not build MDS-beats-Bollobas fixture")




def overlap_670_fixtures():
    weaker_chart = build_chart(7, 6, 4, 2, (1, 1, 1, 1, 1, 1))
    weaker = {
        "chart": weaker_chart,
        "y0": (4, 4, 3, 5),
        "y1": (6, 1, 1, 1),
        "slopes": (0, 1, 2, 3, 4),
        "witnesses": (
            (0, 0, 1, 3, 0, 0),
            (2, 0, 0, 0, 0, 1),
            (0, 1, 0, 0, 0, 1),
            (0, 0, 2, 0, 6, 0),
            (0, 0, 0, 6, 1, 0),
        ),
        "multi_available": False,
        "selector_mode": 0,
        "deleted": False,
    }
    stronger_chart = build_chart(7, 6, 5, 3, (1, 1, 1, 1, 1, 1))
    stronger = {
        "chart": stronger_chart,
        "y0": (5, 0, 5, 2, 0),
        "y1": (1, 5, 4, 6, 3),
        "slopes": (0, 1, 3),
        "witnesses": (
            (3, 0, 4, 0, 5, 0),
            (6, 4, 0, 0, 0, 3),
            (0, 2, 5, 1, 0, 0),
        ),
        "multi_available": False,
        "selector_mode": 0,
        "deleted": False,
    }
    for family in (weaker, stronger):
        family["global_slopes"] = family["slopes"]
        family["global_witnesses"] = family["witnesses"]
    return (
        (weaker_chart, weaker, "overlap_670_stronger"),
        (stronger_chart, stronger, "core_overlap_stronger"),
    )


def audit_670_overlap(family, core, minimum_lift, mds_bounds, stats):
    chart = family["chart"]
    length = chart["N"]
    kappa = chart["kappa"]
    masks = tuple(zero_mask(witness) for witness in family["witnesses"])
    exact_certificates = sum(
        math.comb(len(mask) - 1, kappa) for mask in masks
    )
    ambient_certificates = math.comb(length, kappa + 1)
    require(
        exact_certificates <= ambient_certificates,
        "pinned #670 exact agreement-weighted inequality failed",
    )
    q_uniform = length - chart["t"]
    mu_670 = math.comb(q_uniform - 1, kappa)
    require(
        len(family["slopes"]) * mu_670 <= ambient_certificates,
        "pinned #670 uniform agreement bound failed",
    )
    stats["overlap_670_families"] += 1
    stats["overlap_670_exact_certificates"] += exact_certificates

    if len(family["slopes"]) >= 2:
        minimum_weight = vector_weight(minimum_lift)
        exact_core_sum = sum(
            (
                max(1, minimum_weight + len(mask) - length)
                * math.comb(
                    len(mask) - kappa + core["r"], core["r"]
                )
                + core["s"]
                - 1
            )
            // core["s"]
            for mask in masks
        )
        require(
            exact_core_sum <= math.comb(length, core["s"]),
            "exact nonuniform core sum failed in #670 overlap audit",
        )
    if len(family["slopes"]) >= 2 and core["r"] == kappa:
        require(core["s"] == kappa + 1, "ambient-rank overlap has wrong s")
        if exact_core_sum == exact_certificates:
            stats["nonuniform_670_equal"] += 1
        elif exact_certificates > exact_core_sum:
            stats["nonuniform_670_stronger"] += 1
        else:
            stats["nonuniform_core_stronger"] += 1
        for q_value, ell_q, _, mu_core, _ in mds_bounds:
            comparison_mu_670 = math.comb(q_value - 1, kappa)
            require(
                ell_q * math.comb(q_value, kappa) * (q_value - kappa)
                == ell_q * q_value * comparison_mu_670,
                "#670/core pre-ceil binomial ratio identity failed",
            )
            if q_value == core["s"] and ell_q == 1:
                require(
                    mu_core == comparison_mu_670 == 1,
                    "minimal-q #670/core equality failed",
                )
            if mu_core == comparison_mu_670:
                stats["overlap_670_equal"] += 1
            elif comparison_mu_670 > mu_core:
                stats["overlap_670_stronger"] += 1
            else:
                stats["core_overlap_stronger"] += 1


def maximum_clique_size(adjacency):
    best = 0

    def color_sort(candidates):
        order = []
        colors = []
        color = 0
        remaining = candidates
        while remaining:
            color += 1
            available = remaining
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                remaining &= ~bit
                available &= ~bit
                available &= ~adjacency[vertex]
                order.append(vertex)
                colors.append(color)
        return order, colors

    def expand(candidates, size):
        nonlocal best
        if not candidates:
            best = max(best, size)
            return
        order, colors = color_sort(candidates)
        for index in range(len(order) - 1, -1, -1):
            if size + colors[index] <= best:
                return
            vertex = order[index]
            bit = 1 << vertex
            expand(candidates & adjacency[vertex], size + 1)
            candidates &= ~bit

    expand((1 << len(adjacency)) - 1, 0)
    return best


def subset_masks_at_least(length, minimum_size):
    return tuple(
        mask
        for mask in range(1 << length)
        if mask.bit_count() >= minimum_size
    )


def clique_for_intersection_cap(candidates, cap):
    adjacency = [0] * len(candidates)
    for first in range(len(candidates)):
        for second in range(first):
            if (candidates[first] & candidates[second]).bit_count() <= cap:
                adjacency[first] |= 1 << second
                adjacency[second] |= 1 << first
    return maximum_clique_size(adjacency)


def endpoint_regressions(stats):
    for direction_weight in range(1, 8):
        for h_zero in range(1, direction_weight + 1):
            candidates = subset_masks_at_least(direction_weight, h_zero)
            observed = clique_for_intersection_cap(candidates, 0)
            require(
                observed == direction_weight // h_zero,
                "e=0 disjoint-Y endpoint bound failed",
            )
            stats["endpoint_e0_cases"] += 1

    for direction_weight in range(2, 7):
        for m_length in range(1, 7):
            for h_value in range(2, direction_weight + 1):
                radius = direction_weight + m_length - h_value
                length = direction_weight + m_length
                if radius < m_length or radius > length - 2:
                    continue
                xi_value = m_length * (
                    h_value * h_value - direction_weight * m_length
                )
                if xi_value < 0:
                    continue
                candidates = subset_masks_at_least(direction_weight, h_value)
                observed = clique_for_intersection_cap(candidates, m_length)
                nonzero = tuple(
                    mask for mask in candidates
                    if mask != (1 << direction_weight) - 1
                )
                nonzero_observed = clique_for_intersection_cap(nonzero, m_length)
                zero_vectors = int(
                    (1 << direction_weight) - 1 in candidates
                )
                require(
                    nonzero_observed <= 2 * (direction_weight - 1),
                    "e=M nonzero centered right-angle bound failed",
                )
                require(zero_vectors <= 1, "multiple centered zero vectors")
                require(
                    observed <= 2 * direction_weight - 1,
                    "e=M endpoint bound failed",
                )
                stats["endpoint_eM_cases"] += 1
                stats["endpoint_zero_vectors"] += zero_vectors

    for direction_weight in range(1, 21):
        for m_length in range(1, 21):
            length = direction_weight + m_length
            for radius in range(length - 1):
                if max(direction_weight, radius + 1) > length - 1:
                    continue
                h_zero = max(1, direction_weight - radius)
                total = direction_weight // h_zero
                for exact_weight in range(1, min(radius, m_length - 1) + 1):
                    h_value = max(
                        1, direction_weight + exact_weight - radius
                    )
                    xi_value = (
                        direction_weight * (m_length - exact_weight) ** 2
                        + m_length * h_value * h_value
                        - direction_weight * m_length * m_length
                    )
                    if xi_value > 0:
                        total += length - 1
                    elif xi_value == 0:
                        total += 2 * (length - 2)
                if radius >= m_length:
                    h_value = direction_weight + m_length - radius
                    xi_value = m_length * (
                        h_value * h_value - direction_weight * m_length
                    )
                    if xi_value >= 0:
                        total += 2 * direction_weight - 1
                require(total < 2 * length * length, "endpoint compilation budget")
                stats["endpoint_compilations"] += 1


def loose_budget_bollobas_regression(stats):
    chart = build_chart(7, 6, 3, 2, (1, 2, 3, 4, 5, 6))
    families = discover_chart_families(chart, desired_lines=2)
    candidate = next(
        family for family in families
        if lightweight_rank(family) == 3
    )
    loose_chart = dict(chart)
    loose_chart["t"] = 3
    loose_family = dict(candidate)
    loose_family["chart"] = loose_chart
    core = intrinsic_core(
        loose_family["slopes"],
        loose_family["witnesses"],
        7,
        6,
    )
    result = validate_bollobas_pairs(loose_family, core)
    require(
        result["coarse_bound"] > math.comb(6, core["s"]),
        "loose support budget did not lose to direct bound",
    )
    require(
        result["actual_bound"] <= math.comb(6, core["s"]),
        "actual-support Bollobas bound lost its guarantee",
    )
    stats["loose_budget_regressions"] += 1


def find_positive_rank_family():
    chart = build_chart(5, 5, 3, 2, (1, 1, 1, 1, 1))
    return next(
        family for family in discover_chart_families(chart, desired_lines=2)
        if lightweight_rank(family) > 0
    )


def validate_zero_vector_claim(claimed_count):
    direction_weight = 2
    full_mask = (1 << direction_weight) - 1
    candidates = subset_masks_at_least(direction_weight, direction_weight)
    actual = sum(mask == full_mask for mask in candidates)
    require(actual == claimed_count, "centered zero-vector count was weakened")


def validate_one_ordered_crossing_only():
    labels = ((0,), (1,))
    supports = ((1,), (2,))
    require(not set(labels[0]) & set(supports[0]), "tamper diagonal zero")
    require(not set(labels[1]) & set(supports[1]), "tamper diagonal one")
    require(
        bool(set(labels[1]) & set(supports[0])),
        "tamper retained ordered crossing missing",
    )
    require(
        bool(set(labels[0]) & set(supports[1])),
        "the omitted reverse ordered crossing is false",
    )


def validate_core_rank(family, claimed_rank):
    chart = family["chart"]
    core = intrinsic_core(
        family["slopes"], family["witnesses"], chart["p"], chart["N"]
    )
    require(core["r"] == claimed_rank, "claimed intrinsic core rank is wrong")


def audit_family(family, stats):
    chart = family["chart"]
    modulus = chart["p"]
    length = chart["N"]
    slopes = family["slopes"]
    witnesses = family["witnesses"]
    require(len(slopes) == len(witnesses) and len(slopes) >= 1, "empty family")
    require(len(set(slopes)) == len(slopes), "selected slopes not distinct")
    require(any(family["y1"]), "zero syndrome direction")
    for slope, witness in zip(slopes, witnesses):
        target = add_vectors(
            family["y0"], scale_vector(slope, family["y1"], modulus), modulus
        )
        require(mat_vec(chart["H"], witness, modulus) == target, "wrong bucket")
        require(vector_weight(witness) <= chart["t"], "witness exceeds radius")
        require(
            is_transverse(chart, family["y0"], family["y1"], witness),
            "selected witness is not transverse",
        )

    core = intrinsic_core(slopes, witnesses, modulus, length)
    for coefficients, image in zip(core["E"], core["theta_images"]):
        require(sum(coefficients) % modulus == 0, "E lost constant equation")
        require(
            sum(a * gamma for a, gamma in zip(coefficients, slopes)) % modulus == 0,
            "E lost slope equation",
        )
        require(
            image
            == linear_combination(coefficients, witnesses, modulus, length),
            "theta coefficient map changed",
        )
    for vector in core["W"]:
        require(
            mat_vec(chart["H"], vector, modulus) == (0,) * chart["R"],
            "W is not contained in kernel H",
        )
        require(vector_in_span(vector, core["D"], modulus), "W not contained in D")

    intersection = kernel_intersection_with_span(
        core["D"], chart["H"], modulus
    )
    require(
        same_span(intersection, core["W"], modulus),
        "D intersect ker(H) is not the intrinsic theta image",
    )
    if len(slopes) >= 2:
        require(core["s"] == core["r"] + 1, "affine span dimension is not r+1")
    else:
        require(core["r"] == core["s"] == 0, "singleton core is not rank zero")

    stats["families"] += 1
    stats["safe_deletions"] += family["deleted"]
    stats["multiwitness_families"] += family["multi_available"]
    stats["rank_hist"][core["r"]] += 1

    bollobas = validate_bollobas_pairs(family, core, stats)
    minimum_lift = minimum_lift_vector(chart, family["y1"])
    mds_bounds = audit_basis_multiplicity(
        family,
        core,
        minimum_lift,
        (length - chart["t"],),
        stats,
    )
    audit_exact_e_multiplicity(family, minimum_lift, stats)
    audit_670_overlap(family, core, minimum_lift, mds_bounds, stats)
    if mds_bounds:
        best_mds = min(
            Fraction(integer_bound, 1)
            for _, _, _, _, integer_bound in mds_bounds
        )
        bollobas_bound = Fraction(bollobas["actual_bound"], 1)
        if bollobas_bound < best_mds:
            stats["bollobas_beats_mds"] += 1
        elif best_mds < bollobas_bound:
            stats["mds_beats_bollobas"] += 1
        else:
            stats["bollobas_mds_ties"] += 1

    if family["deleted"]:
        parent_core = intrinsic_core(
            family["global_slopes"],
            family["global_witnesses"],
            modulus,
            length,
        )
        require(
            all(vector_in_span(vector, parent_core["W"], modulus)
                for vector in core["W"]),
            "fixed-selector deletion lost K_0 inclusion",
        )
        require(
            core["r"] <= parent_core["r"],
            "fixed-selector deletion increased intrinsic rank",
        )

    if len(slopes) >= 2:
        _, affine_direction, _ = interpolate_base(
            slopes, witnesses, 0, 1, modulus
        )
        stats["minimum_affine_direction_differences"] += (
            affine_direction != minimum_lift
        )
        cached = chart.setdefault("minimum_lifts", {})
        y_one_key = tuple(family["y1"])
        if y_one_key not in cached:
            _, sample_direction, _ = interpolate_base(
                slopes, witnesses, 0, 1, modulus
            )
            cached[y_one_key] = minimum_coset_weight(
                sample_direction, chart["kernel"], modulus
            )
        minimum_weight = cached[y_one_key]
        canonical_u, canonical_v, canonical_residuals = interpolate_base(
            slopes, witnesses, 0, 1, modulus
        )
        for first_index, second_index in combinations(range(len(slopes)), 2):
            intercept, direction, residuals = interpolate_base(
                slopes, witnesses, first_index, second_index, modulus
            )
            stats["base_pairs"] += 1
            stats["nonminimum_base_pairs"] += vector_weight(direction) > minimum_weight
            require(
                mat_vec(chart["H"], intercept, modulus) == family["y0"],
                "intercept is not a y0 lift",
            )
            require(
                mat_vec(chart["H"], direction, modulus) == family["y1"],
                "interpolating direction is not a y1 lift",
            )
            require(
                same_span(residuals, core["W"], modulus),
                "base-pair residual span depends on the base",
            )
            require(
                same_span(core["W"] + (direction,), core["D"], modulus),
                "<v>+W is not the affine witness span D",
            )
            require(
                vector_in_span(
                    subtract_vectors(intercept, canonical_u, modulus),
                    core["W"],
                    modulus,
                ),
                "base intercept changed outside W",
            )
            require(
                vector_in_span(
                    subtract_vectors(direction, canonical_v, modulus),
                    core["W"],
                    modulus,
                ),
                "base direction changed outside W",
            )
        require(
            same_span(canonical_residuals, core["W"], modulus),
            "canonical curvature span mismatch",
        )

    charges = {}
    affine_base = witnesses[0]
    for slope, witness in zip(slopes, witnesses):
        mask = zero_mask(witness)
        require(
            len(mask) >= length - chart["t"],
            "zero mask is not the complete low-weight complement",
        )
        restricted_rank = matrix_rank(restriction_rows(core["D"], mask), modulus)
        require(restricted_rank == core["s"], "D restriction lost intrinsic rank")
        selected, square = lex_nonzero_minor(core["D"], mask, modulus)
        solution = solve_square(
            square, tuple((-affine_base[index]) % modulus for index in selected),
            modulus,
        )
        reconstructed = add_vectors(
            affine_base,
            linear_combination(solution, core["D"], modulus, length),
            modulus,
        )
        require(reconstructed == witness, "direct lex-minor recovery failed")
        require(
            mat_vec(chart["H"], reconstructed, modulus)
            == add_vectors(
                family["y0"],
                scale_vector(slope, family["y1"], modulus),
                modulus,
            ),
            "recovered witness lost its slope",
        )
        if selected in charges:
            require(charges[selected] == slope, "lex charge is not injective")
        charges[selected] = slope
        stats["core_masks"] += 1

        if len(slopes) >= 2:
            curvature_basis = core["W"]
            curvature_space = tuple(curvature_basis) + (canonical_v,)
            curvature_rank = matrix_rank(
                restriction_rows(curvature_space, mask), modulus
            )
            require(
                curvature_rank == core["r"] + 1,
                "<v>+W restriction lost rank",
            )
            curvature_minor, curvature_square = lex_nonzero_minor(
                curvature_space, mask, modulus
            )
            recovery = solve_square(
                curvature_square,
                tuple((-canonical_u[index]) % modulus for index in curvature_minor),
                modulus,
            )
            require(recovery[-1] == slope, "curvature recovery lost gamma")
            recovered_witness = add_vectors(
                canonical_u,
                linear_combination(recovery, curvature_space, modulus, length),
                modulus,
            )
            require(
                recovered_witness == witness,
                "unique (gamma, coefficient) recovery failed",
            )

    require(
        len(slopes) <= math.comb(length, core["s"]),
        "intrinsic binomial charge bound failed",
    )
    if len(slopes) >= 2:
        require(
            math.comb(length, core["s"]) == math.comb(length, core["r"] + 1),
            "D and curvature binomial charges disagree",
        )
    else:
        require(
            math.comb(length, core["s"]) == 1,
            "singleton did not charge to C(N,0)=1",
        )
    return core


def audit_h_subfamilies(family, stats):
    chart = family["chart"]
    modulus = chart["p"]
    length = chart["N"]
    size = len(family["slopes"])
    for subset_size in range(2, size + 1):
        for selected in combinations(range(size), subset_size):
            subfamily = restrict_family(family, selected)
            core = intrinsic_core(
                subfamily["slopes"],
                subfamily["witnesses"],
                modulus,
                length,
            )
            common_zero_count = sum(
                all(subfamily["witnesses"][index][coordinate] == 0
                    for index in range(subset_size))
                for coordinate in range(length)
            )
            if core["r"] > 0:
                stats["h_subfamilies_positive"] += 1
                support_size = sum(
                    any(vector[coordinate] for vector in core["W"])
                    for coordinate in range(length)
                )
                require(
                    support_size >= chart["R"] + core["r"],
                    "positive-rank W violated generalized Hamming support",
                )
                require(
                    common_zero_count <= chart["kappa"] - core["r"],
                    "positive-rank common-zero cap failed",
                )
            else:
                stats["h_subfamilies_rank_zero"] += 1
                if common_zero_count > chart["kappa"]:
                    stats["rank_zero_formula_failures"] += 1


def unit_vector(length, index):
    return tuple(1 if coordinate == index else 0 for coordinate in range(length))


def explicit_rank_zero_families():
    rows = []
    specifications = [
        (7, 5, 3, (1, 1, 1, 1, 1)),
        (11, 6, 3, (1, 2, 3, 4, 5, 6)),
    ]
    for modulus, length, redundancy, weights in specifications:
        chart = build_chart(modulus, length, redundancy, 1, weights)
        c_zero = unit_vector(length, 0)
        c_one = unit_vector(length, 1)
        y_zero = mat_vec(chart["H"], c_zero, modulus)
        y_one = mat_vec(
            chart["H"], subtract_vectors(c_one, c_zero, modulus), modulus
        )
        family = {
            "chart": chart,
            "y0": y_zero,
            "y1": y_one,
            "slopes": (0, 1),
            "witnesses": (c_zero, c_one),
            "multi_available": False,
            "selector_mode": 0,
            "deleted": False,
        }
        singleton = restrict_family(family, (0,), deletion=True)
        rows.append((family, singleton))
    return rows


def exact_hypergeometric_bad_numerator(scale):
    population = 250 * scale
    selected = 175 * scale
    lower = max(0, 2 * selected - population)
    counts = {
        overlap: math.comb(selected, overlap)
        * math.comb(population - selected, selected - overlap)
        for overlap in range(lower, selected + 1)
    }
    denominator = math.comb(population, selected)
    require(sum(counts.values()) == denominator, "hypergeometric mass changed")
    overlaps = sorted(counts)
    suffix = {}
    running = 0
    for overlap in reversed(overlaps):
        running += counts[overlap]
        suffix[overlap] = running
    bad_numerator = 0
    for first, count in counts.items():
        threshold = population - first + 1
        if threshold <= overlaps[-1]:
            key = max(lower, threshold)
            bad_numerator += count * suffix[key]
    require(0 < bad_numerator < denominator * denominator, "bad tail degenerate")
    single_threshold = 125 * scale + 1
    single_bad_numerator = sum(
        count for overlap, count in counts.items()
        if overlap >= single_threshold
    )
    require(0 < single_bad_numerator < denominator, "single-block tail degenerate")
    return (
        bad_numerator,
        denominator * denominator,
        single_bad_numerator,
        denominator,
    )


def stress_arithmetic(xi_constant=-312500, exact_convolution_limit=6):
    exact_rows = []
    with localcontext() as context:
        context.prec = 90
        for scale in range(1, 201):
            length = 500 * scale
            direction_weight = 250 * scale
            outside_length = 250 * scale
            radius = 150 * scale
            exact_weight = 75 * scale
            height = max(1, direction_weight + exact_weight - radius)
            xi = (
                direction_weight * (outside_length - exact_weight) ** 2
                + outside_length * height**2
                - direction_weight * outside_length**2
            )
            require(
                xi == xi_constant * scale**3,
                "central PR676 Xi arithmetic changed",
            )
            require(length == 2 * outside_length, "stress block split changed")
            mask_size = outside_length - exact_weight
            require(mask_size == height == 175 * scale, "stress mask size changed")
            mean_overlap_sum = (
                Decimal(2 * mask_size * mask_size) / Decimal(outside_length)
            )
            require(mean_overlap_sum == Decimal(245 * scale), "stress mean changed")
            deviation = Decimal(outside_length) - mean_overlap_sum
            exponent = (
                Decimal(2) * deviation * deviation / Decimal(2 * mask_size)
            )
            require(exponent == Decimal(scale) / Decimal(7), "Hoeffding exponent")
            family_size = int((Decimal(scale) / Decimal(14)).exp())
            union_bound = (
                Decimal(math.comb(family_size, 2))
                * (-(Decimal(scale) / Decimal(7))).exp()
            )
            require(union_bound < 1, "combined Hoeffding union bound no longer pays")

            one_block_deviation = Decimal(5 * scale) / Decimal(2)
            one_block_exponent = (
                Decimal(2) * one_block_deviation * one_block_deviation
                / Decimal(mask_size)
            )
            require(
                one_block_exponent == Decimal(scale) / Decimal(14),
                "one-block Hoeffding exponent",
            )
            note_family_size = int((Decimal(scale) / Decimal(40)).exp())
            note_union_bound = (
                Decimal(math.comb(note_family_size, 2))
                * Decimal(2)
                * (-(Decimal(scale) / Decimal(14))).exp()
            )
            require(note_union_bound < 1, "companion-note union bound no longer pays")

        for scale in range(1, exact_convolution_limit + 1):
            (
                numerator,
                denominator,
                single_numerator,
                single_denominator,
            ) = exact_hypergeometric_bad_numerator(scale)
            probability = Decimal(numerator) / Decimal(denominator)
            single_probability = Decimal(single_numerator) / Decimal(single_denominator)
            hoeffding = (-(Decimal(scale) / Decimal(7))).exp()
            one_block_hoeffding = (-(Decimal(scale) / Decimal(14))).exp()
            require(
                probability <= hoeffding,
                "exact convolution exceeded the combined Hoeffding value",
            )
            require(
                single_probability <= one_block_hoeffding,
                "exact one-block tail exceeded the companion-note Hoeffding value",
            )
            family_size = int((Decimal(scale) / Decimal(14)).exp())
            require(
                math.comb(family_size, 2) * numerator < denominator,
                "exact combined hypergeometric union bound failed",
            )
            note_family_size = int((Decimal(scale) / Decimal(40)).exp())
            require(
                math.comb(note_family_size, 2) * 2 * single_numerator
                < single_denominator,
                "exact companion-note hypergeometric union bound failed",
            )
            exact_rows.append(
                (
                    scale,
                    numerator.bit_length(),
                    denominator.bit_length(),
                    f"{probability:.12E}",
                    f"{single_probability:.12E}",
                )
            )
    return {
        "Xi_rows": 200,
        "hypergeom_convolutions": len(exact_rows),
        "exact_rows": tuple(exact_rows),
    }


def log_integer(value):
    require(value > 0, "log_integer domain")
    bits = value.bit_length()
    shift = max(0, bits - 53)
    return math.log(value >> shift) + shift * math.log(2.0)


def binary_entropy(probability):
    if probability <= 0.0 or probability >= 1.0:
        return 0.0
    return (
        -probability * math.log(probability)
        - (1.0 - probability) * math.log(1.0 - probability)
    )


def entropy_support_rows():
    rows = []
    prior = {"n/log(n)": None, "n/sqrt(log(n))": None}
    for length in (1_000, 10_000, 100_000):
        choices = {
            "n/log(n)": max(1, int(length / math.log(length))),
            "n/sqrt(log(n))": max(1, int(length / math.sqrt(math.log(length)))),
        }
        for label, rank in choices.items():
            exact_binomial = math.comb(length, rank + 1)
            exact_log_rate = log_integer(exact_binomial) / length
            probability = (rank + 1) / length
            entropy_bound = binary_entropy(probability)
            require(
                exact_log_rate <= entropy_bound + 1e-12,
                "exact binomial exceeded entropy bound",
            )
            if prior[label] is not None:
                require(
                    exact_log_rate < prior[label],
                    "sublinear-rank example did not decrease",
                )
            prior[label] = exact_log_rate
            rows.append((length, rank, label, exact_log_rate, entropy_bound))
    linear_rank = 10_000
    linear_rate = log_integer(math.comb(100_000, linear_rank)) / 100_000
    require(linear_rate > 0.3, "linear-rank negative control lost positive rate")
    return rows, linear_rate


def validate_pins(pins):
    require(pins == EXPECTED_PR_PINS, "source PR pin mismatch")
    require(set(pins) == {670, 671, 676}, "source pin set changed")
    require(all(len(value) == 40 for value in pins.values()), "non-SHA pin")


def source_self_check():
    source_path = Path(__file__)
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    require(
        not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
        "optimized-mode-unsafe assert statement present",
    )
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    require(imported <= ALLOWED_IMPORT_ROOTS, "non-standard or unsafe import")
    for forbidden in ("subprocess", "socket", "urllib", "requests"):
        require(forbidden not in imported, f"forbidden import {forbidden}")
    require("PR_PINS" in source and "EXPECTED_PR_PINS" in source, "pins absent")
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def chart_configurations():
    return [
        (5, 5, 3, 2, (1, 1, 1, 1, 1)),
        (7, 6, 3, 2, (1, 2, 3, 4, 5, 6)),
        (7, 7, 4, 3, (1, 1, 1, 1, 1, 1, 1)),
    ]


def finite_census():
    stats = defaultdict(int)
    stats["rank_hist"] = defaultdict(int)
    charts = []
    generalized_rows = []
    for specification in chart_configurations():
        chart = build_chart(*specification)
        charts.append(chart)
        stats["charts"] += 1
        stats["low_weight_vectors"] += len(chart["low_vectors"])
        minors, generalized = check_vandermonde_and_generalized_weights(chart)
        stats["vandermonde_minors"] += minors
        stats["gh_rows"] += len(generalized)
        generalized_rows.append((chart["name"], tuple(generalized)))

    families = []
    for chart in charts:
        families.extend(discover_chart_families(chart, desired_lines=2))

    falsifier_rows = explicit_rank_zero_families()
    for family, singleton in falsifier_rows:
        stats["charts"] += 1
        stats["low_weight_vectors"] += len(family["chart"]["low_vectors"])
        minors, generalized = check_vandermonde_and_generalized_weights(
            family["chart"]
        )
        stats["vandermonde_minors"] += minors
        stats["gh_rows"] += len(generalized)
        generalized_rows.append((family["chart"]["name"], tuple(generalized)))
        families.extend((family, singleton))

    binary_chart, binary_families = binary_mds_families()
    stats["charts"] += 1
    stats["general_linear_families"] += len(binary_families)
    stats["low_weight_vectors"] += len(binary_chart["low_vectors"])
    binary_minors, binary_generalized = (
        check_vandermonde_and_generalized_weights(binary_chart)
    )
    stats["vandermonde_minors"] += binary_minors
    stats["gh_rows"] += len(binary_generalized)
    generalized_rows.append(
        (binary_chart["name"], tuple(binary_generalized))
    )
    families.extend(binary_families)

    comparison_chart, comparison_family = mds_beats_bollobas_fixture()
    stats["charts"] += 1
    stats["low_weight_vectors"] += len(comparison_chart["low_vectors"])
    comparison_minors, comparison_generalized = (
        check_vandermonde_and_generalized_weights(comparison_chart)
    )
    stats["vandermonde_minors"] += comparison_minors
    stats["gh_rows"] += len(comparison_generalized)
    generalized_rows.append(
        (comparison_chart["name"], tuple(comparison_generalized))
    )
    families.append(comparison_family)

    for overlap_chart, overlap_family, expected_winner in overlap_670_fixtures():
        stats["charts"] += 1
        stats["low_weight_vectors"] += len(overlap_chart["low_vectors"])
        overlap_minors, overlap_generalized = (
            check_vandermonde_and_generalized_weights(overlap_chart)
        )
        stats["vandermonde_minors"] += overlap_minors
        stats["gh_rows"] += len(overlap_generalized)
        generalized_rows.append(
            (overlap_chart["name"], tuple(overlap_generalized))
        )
        families.append(overlap_family)

    signatures = set()
    unique_families = []
    for family in families:
        signature = (
            family["chart"]["name"],
            family["slopes"],
            family["witnesses"],
            family["y0"],
            family["y1"],
        )
        if signature not in signatures:
            signatures.add(signature)
            unique_families.append(family)

    for family in unique_families:
        audit_family(family, stats)
        audit_h_subfamilies(family, stats)

    selector_groups = defaultdict(set)
    for family in unique_families:
        key = (
            family["chart"]["name"],
            family["y0"],
            family["y1"],
            family["slopes"],
        )
        selector_groups[key].add(lightweight_rank(family))
    stats["selector_rank_variations"] = sum(
        len(ranks) > 1 for ranks in selector_groups.values()
    )

    required_ranks = {0, 1, 2, 3}
    require(
        required_ranks <= set(stats["rank_hist"]),
        f"missing intrinsic ranks {required_ranks - set(stats['rank_hist'])}",
    )
    rank_three_kappa = any(
        lightweight_rank(family) == 3 and family["chart"]["kappa"] >= 3
        for family in unique_families
    )
    require(rank_three_kappa, "no r=3 family with kappa>=3")
    require(stats["nonminimum_base_pairs"] > 0, "no nonminimum interpolating v")
    require(stats["multiwitness_families"] > 0, "no multi-witness selections")
    require(
        stats["selector_rank_variations"] > 0,
        "arbitrary selectors produced no audited rank variation",
    )
    require(stats["safe_deletions"] > 0, "no deletion/recompute coverage")
    require(
        stats["rank_zero_formula_failures"] >= 2,
        "rank-zero generalized-Hamming formula was not explicitly falsified",
    )

    endpoint_regressions(stats)
    loose_budget_bollobas_regression(stats)
    require(stats["bollobas_beats_mds"] > 0, "Bollobas never beat MDS")
    require(stats["mds_beats_bollobas"] > 0, "MDS never beat Bollobas")
    require(stats["overlap_670_equal"] > 0, "no #670/core equality case")
    require(stats["overlap_670_stronger"] > 0, "no #670-stronger case")
    require(stats["core_overlap_stronger"] > 0, "no core-stronger case")
    require(stats["nonuniform_670_equal"] > 0, "no nonuniform overlap equality")
    require(stats["nonuniform_670_stronger"] > 0, "no nonuniform #670 win")
    require(stats["nonuniform_core_stronger"] > 0, "no nonuniform core win")

    f7_family = falsifier_rows[0][0]
    f7_core = intrinsic_core(
        f7_family["slopes"],
        f7_family["witnesses"],
        f7_family["chart"]["p"],
        f7_family["chart"]["N"],
    )
    f7_common = len(
        set(zero_mask(f7_family["witnesses"][0]))
        & set(zero_mask(f7_family["witnesses"][1]))
    )
    require(f7_core["r"] == 0, "mandated F7 falsifier is not rank zero")
    require(f7_common == 3 > f7_family["chart"]["kappa"], "F7 N5 falsifier lost")

    plain_stats = {
        key: value
        for key, value in stats.items()
        if key != "rank_hist"
    }
    plain_stats["rank_hist"] = dict(sorted(stats["rank_hist"].items()))
    return plain_stats, tuple(generalized_rows)


def validate_counts(stats, expected_counts=EXPECTED_COUNTS):
    if any(value < 0 for value in expected_counts.values()):
        return False
    for key, expected in expected_counts.items():
        actual = stats.get(key)
        require(actual == expected, f"coverage count {key}: {actual} != {expected}")
    require(
        stats["rank_hist"] == EXPECTED_RANK_HISTOGRAM,
        "intrinsic rank histogram changed",
    )
    return True


def expect_rejection(label, action):
    try:
        action()
    except VerificationError:
        print(f"tamper {label}: REJECTED")
        return
    raise VerificationError(f"tamper {label} was accepted")


def run_tamper(kind):
    source_self_check()
    if kind == "pins":
        changed = dict(PR_PINS)
        changed[676] = "0" + changed[676][1:]
        expect_rejection(kind, lambda: validate_pins(changed))
    elif kind == "core":
        rows = explicit_rank_zero_families()
        family = rows[0][0]
        expect_rejection(kind, lambda: validate_core_rank(family, 1))
    elif kind == "counts":
        require(
            all(value >= 0 for value in EXPECTED_COUNTS.values()),
            "counts are not hardened yet",
        )
        fake = dict(EXPECTED_COUNTS)
        fake["core_masks"] += 1
        fake["rank_hist"] = dict(EXPECTED_RANK_HISTOGRAM)
        expect_rejection(kind, lambda: validate_counts(fake))
    elif kind == "gh":
        chart = build_chart(7, 5, 3, 1, (1, 1, 1, 1, 1))
        expect_rejection(
            kind,
            lambda: check_vandermonde_and_generalized_weights(
                chart, expected_shift=1
            ),
        )
    elif kind == "stress":
        expect_rejection(
            kind,
            lambda: stress_arithmetic(
                xi_constant=-312499, exact_convolution_limit=0
            ),
        )
    elif kind == "q":
        family = explicit_rank_zero_families()[0][0]
        actual_q = min(len(zero_mask(witness)) for witness in family["witnesses"])
        expect_rejection(
            kind,
            lambda: require(
                all(len(zero_mask(witness)) >= actual_q + 1
                    for witness in family["witnesses"]),
                "uncertified q+1 rejected",
            ),
        )
        kappa = family["chart"]["kappa"]
        expect_rejection(
            "q-boundary",
            lambda: require(
                kappa >= kappa + 1,
                "q=kappa boundary rejected",
            ),
        )
    elif kind == "ell":
        family = explicit_rank_zero_families()[0][0]
        core = intrinsic_core(family["slopes"], family["witnesses"], 7, 5)
        minimum_lift = minimum_lift_vector(family["chart"], family["y1"])
        mask = zero_mask(family["witnesses"][0])
        k_bases = coordinate_basis_sets(core["W"], mask, 7)
        d_bases = set(coordinate_basis_sets(core["D"], mask, 7))
        actual_minimum = min(
            sum(
                tuple(sorted(k_basis + (coordinate,))) in d_bases
                for coordinate in mask
                if coordinate not in k_basis
            )
            for k_basis in k_bases
        )
        expect_rejection(
            kind,
            lambda: require(
                actual_minimum >= actual_minimum + 1,
                "off-by-one ell rejected",
            ),
        )
    elif kind == "mds":
        family = find_positive_rank_family()
        core = intrinsic_core(
            family["slopes"],
            family["witnesses"],
            family["chart"]["p"],
            family["chart"]["N"],
        )
        minimum_lift = minimum_lift_vector(
            family["chart"], family["y1"]
        )
        expect_rejection(
            kind,
            lambda: audit_row_flat_caps(
                family["chart"],
                core,
                vector_weight(minimum_lift),
                defaultdict(int),
                cap_shift=-1,
            ),
        )
    elif kind == "zero-vector":
        expect_rejection(kind, lambda: validate_zero_vector_claim(0))
    elif kind == "one-crossing":
        expect_rejection(kind, validate_one_ordered_crossing_only)
    elif kind == "punctured-e":
        family = explicit_rank_zero_families()[0][0]
        core = intrinsic_core(family["slopes"], family["witnesses"], 7, 5)
        minimum_lift = minimum_lift_vector(family["chart"], family["y1"])
        support_j = {
            index for index, value in enumerate(minimum_lift) if value
        }
        punctured = tuple(
            sum(
                value != 0 and index not in support_j
                for index, value in enumerate(witness)
            )
            for witness in family["witnesses"]
        )
        require(
            punctured != tuple(map(vector_weight, family["witnesses"])),
            "punctured-e tamper fixture did not differ",
        )
        expect_rejection(
            kind,
            lambda: validate_bollobas_pairs(
                family, core, claimed_support_sizes=punctured
            ),
        )
    elif kind == "loose-budget":
        expect_rejection(
            kind,
            lambda: require(
                math.comb(7, 4) <= math.comb(6, 4),
                "loose t bound falsely claimed to sharpen direct count",
            ),
        )
    elif kind == "overlap":
        expect_rejection(
            kind,
            lambda: require(
                math.comb(4 - 1, 2) == math.comb(4, 2),
                "mutated #670 agreement multiplicity rejected",
            ),
        )
    elif kind == "nonuniform":
        exact_mu = (
            (2 * math.comb(3, 1) + 1) // 2
            + (3 * math.comb(4, 1) + 1) // 2
        )
        uniform_mu = 2 * ((2 * math.comb(3, 1) + 1) // 2)
        expect_rejection(
            kind,
            lambda: require(
                exact_mu == uniform_mu,
                "uniform q substituted for exact nonuniform mask sizes",
            ),
        )
    else:
        raise VerificationError("unknown tamper kind")
    print("TAMPER RESULT: PASS")
    return 0


def run_check():
    validate_pins(PR_PINS)
    source_hash = source_self_check()
    finite_stats, generalized = finite_census()
    stress = stress_arithmetic()
    entropy_rows, linear_rate = entropy_support_rows()
    finite_stats["hypergeom_convolutions"] = stress["hypergeom_convolutions"]
    hardened = validate_counts(finite_stats)

    print(f"source pins: PASS {PR_PINS}")
    print(
        "credit gate: #670 agreement weighting is prior work; "
        "actual-core row-flat multiplicity is a complementary refinement"
    )
    print(f"source/AST optimized-mode gate: PASS sha256={source_hash}")
    print(f"finite core-rank census: PASS {finite_stats}")
    print(f"weighted/unweighted generalized weights: PASS {generalized}")
    print(
        "central abstract-mask stress: PASS "
        f"Xi_rows={stress['Xi_rows']} exact={stress['exact_rows']}"
    )
    print("entropy support (exact binomials; numerical logs only):")
    for length, rank, label, exact_rate, entropy_bound in entropy_rows:
        print(
            f"  N={length} r={rank} ({label}) "
            f"log(C(N,r+1))/N={exact_rate:.9f} h={entropy_bound:.9f}"
        )
    print(f"  linear-rank negative-control rate={linear_rate:.9f}")
    print(
        "analytic scope: r=o(N) is paid by the binary-entropy proof; "
        "the finite rows do not prove that limit."
    )
    if not hardened:
        print(f"HARDENING CANDIDATE COUNTS: {finite_stats}")
        print("HARDENING CANDIDATE RANKS:", finite_stats["rank_hist"])
        print("RESULT: UNHARDENED")
        return 3
    print("RESULT: PASS")
    return 0


def main(arguments):
    if arguments in ([], ["--check"]):
        return run_check()
    if len(arguments) == 2 and arguments[0] == "--tamper":
        return run_tamper(arguments[1].lower())
    print(
        "usage: verify_a6_actual_witness_core_rank_preflight.py "
        "[--check|--tamper {pins,core,counts,gh,stress,q,ell,mds,"
        "zero-vector,one-crossing,punctured-e,loose-budget,overlap,nonuniform}]",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
