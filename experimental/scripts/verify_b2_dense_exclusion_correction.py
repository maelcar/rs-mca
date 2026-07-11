#!/usr/bin/env python3
"""Replay the dense exclusion identities with exact integer arithmetic."""

from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb


def subset_census(points, size, modulus, phi):
    out = Counter()
    for subset in combinations(points, size):
        out[sum(phi[x] for x in subset) % modulus] += 1
    return out


def check_subset_identity():
    points = tuple(range(7))
    modulus = 11
    size = 4
    phi = [(x * x + 3 * x + 1) % modulus for x in points]

    previous = subset_census(points, size - 1, modulus, phi)
    current = subset_census(points, size, modulus, phi)
    point_measure = Counter(phi)

    convolution = Counter()
    for first, first_count in previous.items():
        for second, second_count in point_measure.items():
            convolution[(first + second) % modulus] += first_count * second_count

    correction = Counter()
    for point in points:
        remainder = [x for x in points if x != point]
        for subset in combinations(remainder, size - 2):
            target = (sum(phi[x] for x in subset) + 2 * phi[point]) % modulus
            correction[target] += 1

    assert all(
        convolution[target] == size * current[target] + correction[target]
        for target in range(modulus)
    )
    assert sum(correction.values()) == (size - 1) * comb(len(points), size - 1)


def syndrome(subset, phi, modulus):
    return sum(phi[x] for x in subset) % modulus


def disjoint_census(points, positive_size, negative_size, modulus, phi):
    out = Counter()
    for negative_tuple in combinations(points, negative_size):
        negative = set(negative_tuple)
        available = [x for x in points if x not in negative]
        for positive_tuple in combinations(available, positive_size):
            target = (
                syndrome(positive_tuple, phi, modulus)
                - syndrome(negative_tuple, phi, modulus)
            ) % modulus
            out[target] += 1
    return out


def check_disjoint_identity():
    points = tuple(range(8))
    modulus = 13
    size = 3
    phi = [(x * x + 2 * x + 3) % modulus for x in points]

    previous = disjoint_census(points, size - 1, size, modulus, phi)
    current = disjoint_census(points, size, size, modulus, phi)
    lower = disjoint_census(points, size - 1, size - 1, modulus, phi)
    point_measure = Counter(phi)

    convolution = Counter()
    for first, first_count in previous.items():
        for second, second_count in point_measure.items():
            convolution[(first + second) % modulus] += first_count * second_count

    correction = Counter()
    for point in points:
        without_point = [x for x in points if x != point]
        for negative_tuple in combinations(without_point, size):
            negative = set(negative_tuple)
            available = [x for x in without_point if x not in negative]
            for positive_tuple in combinations(available, size - 2):
                target = (
                    syndrome(positive_tuple, phi, modulus)
                    + 2 * phi[point]
                    - syndrome(negative_tuple, phi, modulus)
                ) % modulus
                correction[target] += 1

    assert all(
        convolution[target]
        == size * current[target]
        + correction[target]
        + (len(points) - 2 * size + 2) * lower[target]
        for target in range(modulus)
    )


def print_source_ratios():
    n = 1 << 21
    r = n // 3
    ratios = [
        ("single_omitted_over_convolution", Fraction(r - 1, n)),
        ("single_error_over_true", Fraction(r - 1, n - r + 1)),
        ("single_proxy_mass_over_true", Fraction(n, n - r + 1)),
        ("single_random_energy_floor", Fraction(n * n, (n - r + 1) ** 2)),
        ("disjoint_omitted_over_convolution", Fraction(2 * r - 1, n)),
        ("disjoint_error_over_true", Fraction(2 * r - 1, n - 2 * r + 1)),
        ("disjoint_proxy_mass_over_true", Fraction(n, n - 2 * r + 1)),
        ("disjoint_random_energy_floor", Fraction(n * n, (n - 2 * r + 1) ** 2)),
    ]

    print(f"parameters: n={n} r={r}")
    print("object: fixed-weight add-one and disjoint-pair exclusion corrections")
    for name, value in ratios:
        print(f"{name}: {value} = {float(value):.12f}")


def main():
    check_subset_identity()
    check_disjoint_identity()
    print("pointwise identities: PASS")
    print_source_ratios()
    print("theorem: b2_dense_exclusion_correction")
    print("status: PROVED exact identities; asymptotic proxy route cut")


if __name__ == "__main__":
    main()
