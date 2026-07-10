#!/usr/bin/env python3
"""Exact checks for the Parseval-sharp split-prime descent note."""

from __future__ import annotations

import argparse
import cmath
import random
from collections import defaultdict
from itertools import product
from math import comb, pi


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
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
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if work[row][pivot_index] != 0
                ),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                assert numerator % previous == 0
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def reduce_mod_cyclotomic(coefficients: tuple[int, ...]) -> list[int]:
    n = len(coefficients)
    half = n // 2
    return [coefficients[i] - coefficients[i + half] for i in range(half)]


def cyclotomic_resultant(coefficients: tuple[int, ...]) -> int:
    """Return Res(X^(n/2)+1,f) via multiplication by f in the quotient."""
    reduced = reduce_mod_cyclotomic(coefficients)
    half = len(reduced)
    matrix = [[0] * half for _ in range(half)]
    for column in range(half):
        for exponent, coefficient in enumerate(reduced):
            target = exponent + column
            if target >= half:
                target -= half
                coefficient = -coefficient
            matrix[target][column] += coefficient
    return bareiss_determinant(matrix)


def evaluate_mod(coefficients: tuple[int, ...], value: int, prime: int) -> int:
    out = 0
    for coefficient in reversed(coefficients):
        out = (out * value + coefficient) % prime
    return out


def verify_resultant_lemma() -> int:
    checks = 0
    rng = random.Random(20260710)
    rows: list[tuple[int, int, list[tuple[int, ...]]]] = []
    for n, prime in ((4, 13), (8, 17)):
        rows.append((n, prime, list(product((-1, 0, 1), repeat=n))))
    samples = [
        tuple(rng.choice((-1, 0, 1)) for _ in range(16))
        for _ in range(4000)
    ]
    rows.append((16, 97, samples))

    for n, prime, words in rows:
        zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
        omega = cmath.exp(2j * pi / n)
        for coefficients in words:
            resultant = cyclotomic_resultant(coefficients)
            modular_zeros = sum(
                evaluate_mod(coefficients, pow(zeta, k, prime), prime) == 0
                for k in range(1, n, 2)
            )
            if resultant:
                assert resultant % (prime**modular_zeros) == 0
                assert abs(resultant) ** 4 <= (2 * n) ** n
            else:
                assert all(value == 0 for value in reduce_mod_cyclotomic(coefficients))

            lhs = sum(
                abs(
                    sum(
                        coefficient * omega ** (k * i)
                        for i, coefficient in enumerate(coefficients)
                    )
                )
                ** 2
                for k in range(1, n, 2)
            )
            rhs = (n / 2) * sum(
                value * value for value in reduce_mod_cyclotomic(coefficients)
            )
            assert abs(lhs - rhs) < 1e-7 * max(1, rhs)
            checks += 1
    return checks


def syndrome(
    bits: int,
    n: int,
    prime: int,
    zeta: int,
    shift: int,
    depth: int,
    lifts: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        sum(
            (lifts[i] % prime) * pow(zeta, ((shift + j) * i) % n, prime)
            for i in range(n)
            if bits >> i & 1
        )
        % prime
        for j in range(depth)
    )


def verified_descent_depth(n: int, prime: int, depth: int, bound: int) -> int:
    j = 0
    scale = n
    while scale >= 2 and j < n.bit_length() - 1:
        exponent = depth // (1 << (j + 1))
        if exponent == 0 or prime**exponent <= (2 * bound * bound * scale) ** (
            scale // 4
        ):
            break
        j += 1
        scale //= 2
    return j


def verify_periodicity() -> tuple[int, int]:
    cases = 0
    pair_checks = 0
    configurations = (
        (8, 65537, 3, 2, (1, 2, -1, -2, 1, 2, -1, -2)),
        (16, 65537, 8, 5, (1,) * 16),
    )
    for n, prime, depth, shift, lifts in configurations:
        zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
        bound = max(map(abs, lifts))
        levels = verified_descent_depth(n, prime, depth, bound)
        modulus = n // (1 << levels)
        assert levels > 0
        fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
        for bits in range(1 << n):
            fibers[
                syndrome(bits, n, prime, zeta, shift, depth, lifts)
            ].append(bits)
        for family in fibers.values():
            base = family[0]
            for bits in family[1:]:
                word = [
                    lifts[i] * (((bits >> i) & 1) - ((base >> i) & 1))
                    for i in range(n)
                ]
                for i in range(n - modulus):
                    assert word[i] == word[i + modulus]
                pair_checks += 1
            assert len(family) <= 2**modulus
        cases += 1
    return cases, pair_checks


def verify_endpoint_fibers() -> tuple[int, int]:
    cases = 0
    fibers_checked = 0
    for n, prime, shifts in ((4, 13, range(4)), (8, 17, range(8)), (16, 97, (0, 1, 5))):
        zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
        depth = n // 2
        for shift in shifts:
            fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
            for bits in range(1 << n):
                key = syndrome(bits, n, prime, zeta, shift, depth, (1,) * n)
                fibers[key].append(bits)
            assert max(map(len, fibers.values())) <= 4
            fibers_checked += len(fibers)

            for weight in range(n + 1):
                maximum = max(
                    (
                        sum(bits.bit_count() == weight for bits in family)
                        for family in fibers.values()
                    ),
                    default=0,
                )
                assert maximum <= 2
            cases += 1
    return cases, fibers_checked


def verify_scale_arithmetic() -> int:
    checks = 0
    for n in (8, 16, 32, 64, 128, 256, 512):
        for bound in (1, 2, 3):
            prime_floor = 2 * bound * bound * n + 1
            depth = n // 2
            scale = n
            for j in range(n.bit_length() - 2):
                exponent = depth // (1 << (j + 1))
                assert exponent == scale // 4
                assert prime_floor**exponent > (
                    2 * bound * bound * scale
                ) ** (scale // 4)
                scale //= 2
                checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")

    resultant_checks = verify_resultant_lemma()
    periodicity_cases, periodicity_pairs = verify_periodicity()
    endpoint_cases, endpoint_fibers = verify_endpoint_fibers()
    scale_checks = verify_scale_arithmetic()
    total = (
        resultant_checks
        + periodicity_cases
        + periodicity_pairs
        + endpoint_cases
        + endpoint_fibers
        + scale_checks
    )
    print(f"resultant_parseval_checks={resultant_checks}")
    print(f"periodicity_cases={periodicity_cases}")
    print(f"periodicity_pair_checks={periodicity_pairs}")
    print(f"endpoint_cases={endpoint_cases}")
    print(f"endpoint_fibers={endpoint_fibers}")
    print(f"scale_checks={scale_checks}")
    print(f"RESULT: PASS ({total}/{total} checks)")


if __name__ == "__main__":
    main()
