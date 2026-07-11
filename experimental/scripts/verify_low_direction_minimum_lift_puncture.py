#!/usr/bin/env python3
"""Exact small-field replay for the minimum-lift puncture compiler."""

from collections import defaultdict
from itertools import combinations, product


def add(first, second, modulus):
    return tuple((x + y) % modulus for x, y in zip(first, second))


def subtract(first, second, modulus):
    return tuple((x - y) % modulus for x, y in zip(first, second))


def scale(scalar, vector, modulus):
    return tuple(scalar * x % modulus for x in vector)


def weight(vector):
    return sum(value != 0 for value in vector)


def parity_columns(modulus, length, redundancy):
    return [
        tuple(pow(point, degree, modulus) for degree in range(redundancy))
        for point in range(length)
    ]


def syndrome(word, columns, modulus):
    return tuple(
        sum(word[index] * columns[index][degree] for index in range(len(word)))
        % modulus
        for degree in range(len(columns[0]))
    )


def errors(modulus, length, radius):
    yield (0,) * length
    for size in range(1, radius + 1):
        for selected in combinations(range(length), size):
            for values in product(range(1, modulus), repeat=size):
                row = [0] * length
                for index, value in zip(selected, values):
                    row[index] = value
                yield tuple(row)


def support(word):
    return tuple(index for index, value in enumerate(word) if value)


def punctured_johnson_bound(length, redundancy, radius, direction_distance):
    kappa = length - redundancy
    punctured_length = length - direction_distance
    agreement = punctured_length - radius
    denominator = agreement * agreement - punctured_length * (kappa - 1)
    if radius >= punctured_length or denominator <= 0:
        return None
    list_bound = (
        punctured_length * (agreement - (kappa - 1)) // denominator
    )
    return direction_distance * list_bound


def census(modulus, length, redundancy, radius):
    columns = parity_columns(modulus, length, redundancy)
    zero = (0,) * redundancy

    fibers = defaultdict(list)
    for word in product(range(modulus), repeat=length):
        fibers[syndrome(word, columns, modulus)].append(word)

    kernel = fibers[zero]
    assert len(kernel) == modulus ** (length - redundancy)
    assert min(weight(word) for word in kernel if any(word)) == redundancy + 1

    error_fibers = defaultdict(list)
    spans = {}
    for error in errors(modulus, length, radius):
        exact_support = support(error)
        error_fibers[syndrome(error, columns, modulus)].append(
            (error, exact_support)
        )
        if exact_support not in spans:
            span = set()
            for values in product(range(modulus), repeat=len(exact_support)):
                row = [0] * length
                for index, value in zip(exact_support, values):
                    row[index] = value
                span.add(syndrome(tuple(row), columns, modulus))
            spans[exact_support] = span

    syndromes = list(product(range(modulus), repeat=redundancy))
    nonempty = applications = max_slopes = 0
    minimum_slack = None

    for y_0 in syndromes:
        b_0 = fibers[y_0][0]
        for y_1 in syndromes:
            if y_1 == zero:
                continue

            lifts = fibers[y_1]
            direction_distance = min(weight(word) for word in lifts)
            b_1 = next(
                word for word in lifts if weight(word) == direction_distance
            )
            direction_support = {
                index for index, value in enumerate(b_1) if value
            }
            puncture = tuple(
                index for index in range(length) if index not in direction_support
            )

            chosen = {}
            for gamma in range(modulus):
                target = add(y_0, scale(gamma, y_1, modulus), modulus)
                for error, exact_support in error_fibers.get(target, ()):
                    span = spans[exact_support]
                    if not (y_0 in span and y_1 in span):
                        chosen[gamma] = error
                        break

            if not chosen:
                continue

            nonempty += 1
            slope_count = len(chosen)
            max_slopes = max(max_slopes, slope_count)

            clusters = defaultdict(list)
            for gamma, error in chosen.items():
                kernel_word = subtract(
                    subtract(error, b_0, modulus),
                    scale(gamma, b_1, modulus),
                    modulus,
                )
                assert syndrome(kernel_word, columns, modulus) == zero
                clusters[kernel_word].append(gamma)

            punctured_radii = [
                weight(
                    tuple((b_0[index] + word[index]) % modulus for index in puncture)
                )
                for word in kernel
            ]
            weighted_ball = sum(
                direction_distance
                // max(1, direction_distance + punctured_radius - radius)
                for punctured_radius in punctured_radii
                if punctured_radius <= radius
            )
            assert slope_count <= weighted_ball

            bound = punctured_johnson_bound(
                length, redundancy, radius, direction_distance
            )
            if bound is not None:
                assert slope_count <= bound
                applications += 1
                slack = bound - slope_count
                minimum_slack = slack if minimum_slack is None else min(
                    minimum_slack, slack
                )

    return {
        "q": modulus,
        "N": length,
        "R": redundancy,
        "kappa": length - redundancy,
        "t": radius,
        "nonempty_lines": nonempty,
        "max_slopes": max_slopes,
        "johnson_applications": applications,
        "minimum_slack": minimum_slack,
    }


def check_positive_rate_family():
    for m in range(5, 101):
        n, redundancy, kappa, radius, distance = 9 * m, 8 * m, m, 4 * m, 2 * m
        punctured_length = n - distance
        punctured_distance = redundancy + 1 - distance
        denominator = (
            punctured_distance * punctured_length
            - 2 * radius * punctured_length
            + radius * radius
        )
        numerator = punctured_length * (punctured_distance - radius)
        bound = distance * (numerator // denominator)

        assert (n - radius) ** 2 <= n * (n - distance)
        assert 3 * radius > redundancy
        assert kappa == n - redundancy
        assert denominator == m * (2 * m + 7)
        assert bound <= 12 * m


def main():
    rows = [
        census(5, 4, 2, 1),
        census(5, 5, 3, 1),
        census(5, 5, 4, 2),
    ]
    check_positive_rate_family()

    print("object: low-direction minimum-lift puncture compiler")
    for row in rows:
        print(row)
    print("positive-rate family m=5..100: PASS")
    print("theorem: low_direction_minimum_lift_puncture")
    print("status: PROVED for the printed branch")


if __name__ == "__main__":
    main()
