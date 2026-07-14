#!/usr/bin/env python3
"""Exact audit for the weighted [2K,K,K+1] MDS coset-packing bound.

The deployed checks use only Python's standard library and exact integers.
The toy check exhausts all errors through the tested radius in every syndrome
of a small weighted GRS code. No assert statements are used, so ``python -O``
performs the same checks.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations, product
from math import comb, isqrt
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def is_prime_trial_division(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    limit = isqrt(value)
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def weighted_grs_parity_columns(
    points: tuple[int, ...],
    multipliers: tuple[int, ...],
    dimension: int,
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    """Return standard weighted-GRS parity-check columns."""
    require(len(points) == 2 * dimension, "toy length is not 2K")
    require(len(multipliers) == len(points), "multiplier length mismatch")
    columns = []
    for index, point in enumerate(points):
        derivative = 1
        for other_index, other in enumerate(points):
            if other_index != index:
                derivative = derivative * (point - other) % prime
        denominator = multipliers[index] * derivative % prime
        require(denominator != 0, "zero weighted-GRS parity denominator")
        eta = pow(denominator, prime - 2, prime)
        columns.append(
            tuple(
                eta * pow(point, degree, prime) % prime
                for degree in range(dimension)
            )
        )
    return tuple(columns)


def syndrome_of_sparse_error(
    support: tuple[int, ...],
    values: tuple[int, ...],
    columns: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[int, ...]:
    dimension = len(columns[0])
    return tuple(
        sum(
            values[position] * columns[coordinate][row]
            for position, coordinate in enumerate(support)
        )
        % prime
        for row in range(dimension)
    )


def audit_toy_weighted_grs_cosets() -> tuple[int, int, int]:
    prime = 11
    dimension = 4
    length = 2 * dimension
    sigma = 1
    radius = dimension - sigma
    points = tuple(range(length))
    multipliers = tuple(range(1, length + 1))
    columns = weighted_grs_parity_columns(points, multipliers, dimension, prime)

    minimum_weight = length + 1
    for coefficients in product(range(prime), repeat=dimension):
        codeword = tuple(
            multipliers[index]
            * sum(coefficients[degree] * pow(point, degree, prime) for degree in range(dimension))
            % prime
            for index, point in enumerate(points)
        )
        syndrome = tuple(
            sum(
                codeword[index] * columns[index][row]
                for index in range(length)
            )
            % prime
            for row in range(dimension)
        )
        require(syndrome == (0,) * dimension, "toy GRS word has nonzero syndrome")
        if any(codeword):
            minimum_weight = min(minimum_weight, sum(value != 0 for value in codeword))
    require(minimum_weight == dimension + 1, "toy weighted GRS code is not MDS")

    list_counts: defaultdict[tuple[int, ...], int] = defaultdict(int)
    low_counts: defaultdict[tuple[int, ...], int] = defaultdict(int)
    high_supports: defaultdict[
        tuple[int, ...], list[tuple[int, ...]]
    ] = defaultdict(list)

    for weight in range(radius + 1):
        for support in combinations(range(length), weight):
            for values in product(range(1, prime), repeat=weight):
                syndrome = syndrome_of_sparse_error(support, values, columns, prime)
                list_counts[syndrome] += 1
                if weight <= dimension // 2:
                    low_counts[syndrome] += 1
                else:
                    high_supports[syndrome].append(support)

    require(max(low_counts.values()) <= 1, "toy low branch exceeds one")
    packing_numerator = comb(length, dimension - 2 * sigma)
    packing_denominator = comb(dimension - sigma, dimension - 2 * sigma)
    shell_integer_upper = packing_numerator // packing_denominator

    max_high_shell = 0
    for syndrome, supports in high_supports.items():
        require(
            len(supports) == len(set(supports)),
            f"duplicate support at syndrome {syndrome}",
        )
        for left_index, left in enumerate(supports):
            left_set = set(left)
            for right in supports[left_index + 1 :]:
                require(
                    len(left_set.intersection(right))
                    <= dimension - 2 * sigma - 1,
                    f"toy support packing failed at syndrome {syndrome}",
                )
        require(
            len(supports) <= shell_integer_upper,
            "toy high shell exceeds packing bound",
        )
        max_high_shell = max(max_high_shell, len(supports))

    full_integer_upper = (
        packing_denominator + packing_numerator
    ) // packing_denominator
    max_list = max(list_counts.values())
    require(max_list <= full_integer_upper, "toy coset exceeds full packing bound")
    return minimum_weight, max_high_shell, max_list


def deployed_arithmetic() -> None:
    prime = 2_130_706_433
    length = 2_097_152
    dimension = 1_048_576
    sigma = 67_471
    agreement = dimension + sigma
    radius = dimension - sigma

    require(is_prime_trial_division(prime), "deployed p is not prime")
    require(length == 2 * dimension, "deployed n is not 2K")
    require(agreement == 1_116_047, "wrong deployed agreement")
    require(radius == 981_105, "wrong deployed radius")
    require(
        prime > length,
        "deployed field is not larger than the evaluation set",
    )
    require(
        (prime - 1) % length == 0,
        "deployed cyclic domain does not divide p-1",
    )
    require((prime - 1) // length == 1_016, "wrong deployed subgroup index")

    challenge_budget = prime**6 // 2**128
    target = (
        (challenge_budget + 1) * (prime - length + agreement) - 1
    ) // prime
    require(
        challenge_budget == 274_980_728_111_395_087,
        "wrong challenge budget",
    )
    require(target == 274_854_110_496_187_592, "wrong one-row target")

    max_numerator = -1
    max_denominator = 1
    max_delta = None
    ratio_checks = 0
    for delta in range(sigma, dimension // 2 - 1):
        numerator = (delta + 1) * (dimension - delta)
        denominator = (dimension + 2 * delta + 1) * (
            dimension + 2 * delta + 2
        )
        require(
            11 * numerator < denominator,
            f"ratio bound failed at delta={delta}",
        )
        ratio_checks += 1
        if numerator * max_denominator > max_numerator * denominator:
            max_numerator = numerator
            max_denominator = denominator
            max_delta = delta

    high_shell_terms = dimension // 2 - sigma
    require(
        ratio_checks == high_shell_terms - 1,
        "ratio loop does not cover every adjacent high-shell pair",
    )
    require(max_delta == 262_143, "wrong deployed maximum-ratio location")

    packing_depth = dimension - 2 * sigma
    require(packing_depth == 913_634, "wrong first packing depth")
    first_numerator = comb(length, packing_depth)
    first_denominator = comb(radius, packing_depth)
    require(
        first_denominator == comb(radius, sigma),
        "binomial symmetry check failed",
    )

    u_high = (11 * first_numerator - 1) // (10 * first_denominator)
    u_list = u_high + 1
    require(
        10 * first_denominator * u_high < 11 * first_numerator,
        "U_high is too large",
    )
    require(
        10 * first_denominator * u_list >= 11 * first_numerator,
        "U_list is not the corrected ceiling",
    )
    require(
        u_list > target,
        "unexpectedly the packing route meets the deployed target",
    )

    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(1_000_000)
    u_high_text = str(u_high)
    u_list_text = str(u_list)
    quotient_text = str(u_list // target)

    require(len(u_high_text) == 517_030, "U_high digit count changed")
    require(len(u_list_text) == 517_030, "U_list digit count changed")
    require(
        u_high_text.startswith("904729988050617145947819275983"),
        "U_high leading digits changed",
    )
    require(
        u_high_text.endswith("447267321596643140059698004080"),
        "U_high trailing digits changed",
    )
    require(
        u_list_text.endswith("447267321596643140059698004081"),
        "U_list trailing digits changed",
    )
    require(
        len(quotient_text) == 517_013,
        "comparison quotient digit count changed",
    )
    require(
        quotient_text.startswith("329167348604439498924431336018"),
        "comparison quotient leading digits changed",
    )

    minimum_weight, max_high_shell, max_list = audit_toy_weighted_grs_cosets()

    print("status=PROVED")
    print("theorem=weighted_2K_K_Kplus1_MDS_coset_packing")
    print("scope=weighted_GRS_or_linear_MDS_with_n_equals_2K")
    print(
        "toy_weighted_grs_cosets=PASS "
        f"p=11 K=4 sigma=1 minimum_weight={minimum_weight} "
        f"max_high_shell={max_high_shell} max_list={max_list}"
    )
    print(f"p={prime}")
    print(f"n={length}")
    print(f"K={dimension}")
    print(f"sigma={sigma}")
    print(f"agreement={agreement}")
    print(f"radius={radius}")
    print(f"challenge_budget={challenge_budget}")
    print(f"target={target}")
    print(f"high_shell_terms={high_shell_terms}")
    print(
        f"ratio_bound=PASS checks={ratio_checks} max_delta={max_delta} "
        f"max_ratio={max_numerator}/{max_denominator}"
    )
    print(f"packing_depth={packing_depth}")
    print(f"first_numerator_bits={first_numerator.bit_length()}")
    print(f"first_denominator_bits={first_denominator.bit_length()}")
    print(f"U_high_bits={u_high.bit_length()}")
    print(f"U_high_digits={len(u_high_text)}")
    print(f"U_high_leading30={u_high_text[:30]}")
    print(f"U_high_trailing30={u_high_text[-30:]}")
    print(f"U_list_bits={u_list.bit_length()}")
    print(f"U_list_digits={len(u_list_text)}")
    print(f"U_list_leading30={u_list_text[:30]}")
    print(f"U_list_trailing30={u_list_text[-30:]}")
    print(f"floor_U_list_over_target_digits={len(quotient_text)}")
    print(f"floor_U_list_over_target_leading30={quotient_text[:30]}")
    print("comparison=FAILS_TARGET")
    print("nonclaim=no_deployed_closure_no_score_movement")


def main() -> None:
    deployed_arithmetic()


if __name__ == "__main__":
    main()
