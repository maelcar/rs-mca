#!/usr/bin/env python3
"""Exact checks for the endpoint shortened-Plotkin C9 note."""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import ceil, comb


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


def endpoint_fibers(
    n: int, prime: int, weight: int, depth: int, shift: int
) -> dict[tuple[int, ...], list[int]]:
    zeta = pow(primitive_root(prime), (prime - 1) // n, prime)
    points = [pow(zeta, i, prime) for i in range(n)]
    exponents = [(shift + j) % n for j in range(depth)]
    columns = [
        tuple(pow(point, exponent, prime) for exponent in exponents)
        for point in points
    ]
    fibers: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for support in combinations(range(n), weight):
        mask = sum(1 << i for i in support)
        syndrome = tuple(
            sum(columns[i][j] for i in support) % prime
            for j in range(depth)
        )
        fibers[syndrome].append(mask)
    return fibers


def verify_endpoint_rows() -> tuple[int, int, int]:
    cases = 0
    fibers_checked = 0
    pair_checks = 0
    for n, prime in ((4, 5), (8, 17), (8, 41)):
        for weight in range(1, n):
            for depth in range(1, n // 2 + 1):
                endpoints = (
                    (0, depth),
                    (1, depth + 1),
                    ((1 - depth) % n, depth),
                    ((-depth) % n, depth + 1),
                )
                for shift, side_distance in endpoints:
                    fibers = endpoint_fibers(
                        n, prime, weight, depth, shift
                    )
                    max_fiber = max(map(len, fibers.values()))
                    for family in fibers.values():
                        for right in range(len(family)):
                            for left in range(right):
                                side = (family[right] & ~family[left]).bit_count()
                                assert side >= side_distance
                                pair_checks += 1

                    distance = 2 * side_distance
                    threshold = Fraction(2 * weight * (n - weight), n)
                    if distance > threshold:
                        bound = Fraction(distance, 1) / (distance - threshold)
                        assert max_fiber <= bound
                    elif distance == threshold:
                        assert max_fiber <= 2 * (n - 1)
                    cases += 1
                    fibers_checked += len(fibers)
    return cases, fibers_checked, pair_checks


def verify_shortening_arithmetic(max_n: int) -> int:
    checks = 0
    for n in range(4, max_n + 1):
        for q in range(1, n // 2 + 1):
            threshold = Fraction(2 * q * (n - q), n)
            max_u = min(n // 4, n - q)
            if n <= 64:
                shortening_depths = range(max_u + 1)
            else:
                shortening_depths = sorted(
                    {0, 1, max_u // 4, max_u // 2, 3 * max_u // 4, max_u}
                )
            for u in shortening_depths:
                shortened = Fraction(2 * q * (n - u - q), n - u)
                drop = threshold - shortened
                assert drop == Fraction(2 * q * q * u, n * (n - u))
                ratio = Fraction(comb(n, q), comb(n - u, q))
                assert ratio <= 4**u
                checks += 1

            alpha = Fraction(q, n)
            for distance in range(1, n + 3):
                deficit = max(Fraction(0), threshold - distance)
                target = (deficit + 1) / (2 * alpha * alpha)
                u = ceil(target)
                if u > min(n // 4, n - q):
                    continue
                shortened = Fraction(2 * q * (n - u - q), n - u)
                assert distance - shortened >= 1
                exact = Fraction(comb(n, q), comb(n - u, q)) * Fraction(
                    distance, 1
                ) / (distance - shortened)
                assert exact <= (n + 2) * 4**u
                checks += 1
    return checks


def verify_half_density_examples() -> int:
    checks = 0
    for n, prime in ((8, 17), (16, 17), (16, 97)):
        weight = n // 2
        rows = (
            (n // 4, 0, 2 * (n - 1)),
            (n // 4 - 1, 1, 2 * (n - 1)),
            (n // 4, 1, n // 4 + 1),
        )
        for depth, shift, bound in rows:
            if depth < 1:
                continue
            fibers = endpoint_fibers(n, prime, weight, depth, shift)
            assert max(map(len, fibers.values())) <= bound
            checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="run exact checks")
    parser.add_argument(
        "--max-n",
        type=int,
        default=192,
        help="check shortening arithmetic through this length (default: 192)",
    )
    args = parser.parse_args()
    if not args.check:
        parser.error("pass --check")
    if not 16 <= args.max_n <= 512:
        parser.error("--max-n must lie between 16 and 512")

    cases, fibers, pairs = verify_endpoint_rows()
    arithmetic = verify_shortening_arithmetic(args.max_n)
    half_density = verify_half_density_examples()
    total = cases + fibers + pairs + arithmetic + half_density
    print(f"endpoint_cases={cases}")
    print(f"endpoint_fibers={fibers}")
    print(f"within_fiber_pair_checks={pairs}")
    print(f"shortening_arithmetic_checks={arithmetic}")
    print(f"half_density_checks={half_density}")
    print(f"RESULT: PASS ({total}/{total} checks)")


if __name__ == "__main__":
    main()
