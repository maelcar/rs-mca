#!/usr/bin/env python3
"""Exact replay for the A6 full-support and zero-boundary theorem."""

from itertools import combinations, product
from math import comb


def rank(matrix, modulus):
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [value * inverse % modulus for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % modulus
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def nullspace(matrix, modulus):
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivots = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, modulus)
        work[pivot_row] = [value * inverse % modulus for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (value - factor * pivot_value) % modulus
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_columns = [column for column in range(column_count) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * column_count
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -work[row][free] % modulus
        basis.append(tuple(vector))
    return basis


def weighted_rs_parity(modulus, points, redundancy, weights):
    assert len(points) == len(set(points))
    assert all(0 <= point < modulus for point in points)
    assert all(weight % modulus for weight in weights)
    return [
        tuple(
            weights[column] * pow(points[column], degree, modulus) % modulus
            for column in range(len(points))
        )
        for degree in range(redundancy)
    ]


def syndrome(word, parity, modulus):
    return tuple(
        sum(row[column] * word[column] for column in range(len(word))) % modulus
        for row in parity
    )


def minimum_lift(target, parity, modulus):
    length = len(parity[0])
    for size in range(1, length + 1):
        for selected in combinations(range(length), size):
            for values in product(range(1, modulus), repeat=size):
                word = [0] * length
                for column, value in zip(selected, values):
                    word[column] = value
                if syndrome(word, parity, modulus) == target:
                    return tuple(word)
    raise AssertionError("nonzero target has no lift")


def shortened_dimension(generator, support_set, modulus):
    complement = [
        column for column in range(len(generator[0])) if column not in support_set
    ]
    restricted = [tuple(row[column] for column in complement) for row in generator]
    return len(generator) - rank(restricted, modulus)


def generalized_weights(generator, modulus):
    dimension = len(generator)
    length = len(generator[0])
    result = [None] * dimension
    coordinates = range(length)
    for size in range(length + 1):
        for selected in combinations(coordinates, size):
            shortened = shortened_dimension(generator, set(selected), modulus)
            for subdimension in range(1, shortened + 1):
                if result[subdimension - 1] is None:
                    result[subdimension - 1] = size
        if all(value is not None for value in result):
            break
    return result


def check_generalized_weight_case(modulus, length, redundancy, weights, seed):
    points = list(range(length))
    parity = weighted_rs_parity(modulus, points, redundancy, weights)
    assert rank(parity, modulus) == redundancy
    kernel = nullspace(parity, modulus)
    kappa = length - redundancy
    assert len(kernel) == kappa
    assert generalized_weights(kernel, modulus) == [
        redundancy + index for index in range(1, kappa + 1)
    ]

    target = syndrome(seed, parity, modulus)
    assert any(target)
    lift = minimum_lift(target, parity, modulus)
    distance = sum(value != 0 for value in lift)
    assert distance <= redundancy

    extension = kernel + [lift]
    assert rank(extension, modulus) == kappa + 1
    actual = generalized_weights(extension, modulus)
    expected = [distance] + [
        redundancy + subdimension - 1
        for subdimension in range(2, kappa + 2)
    ]
    assert actual == expected, (actual, expected)

    mask_checks = 0
    for radius in range(redundancy):
        for support_size in range(radius + 1):
            for supported in combinations(range(length), support_size):
                assert shortened_dimension(extension, set(supported), modulus) <= 1
                mask_checks += 1
    return distance, actual, mask_checks


def parameter_record(length, redundancy, radius, distance, exact_weight):
    kappa = length - redundancy
    punctured_length = length - distance
    punctured_distance = redundancy + 1 - distance
    q_value = distance + 2 * exact_weight - 2 * radius
    effective_distance = min(
        punctured_length, max(punctured_distance, q_value)
    )
    denominator = (
        punctured_length * effective_distance
        - 2 * punctured_length * exact_weight
        + exact_weight * exact_weight
    )
    if q_value <= punctured_distance:
        branch = "W1"
    elif q_value < punctured_length:
        branch = "W2"
    else:
        branch = "W3"
    return {
        "N": length,
        "R": redundancy,
        "kappa": kappa,
        "t": radius,
        "d": distance,
        "M": punctured_length,
        "Delta": punctured_distance,
        "e": exact_weight,
        "q": q_value,
        "D": effective_distance,
        "J": denominator,
        "branch": branch,
    }


def check_parameter_record(record, claimed_d=None, claimed_j=None):
    n = record["N"]
    r = record["R"]
    kappa = record["kappa"]
    radius = record["t"]
    distance = record["d"]
    m = record["M"]
    delta = record["Delta"]
    exact_weight = record["e"]
    q_value = record["q"]
    effective_distance = record["D"]
    denominator = record["J"]

    assert n == r + kappa
    assert 1 <= kappa and 0 <= radius < r
    assert 1 <= distance <= r
    assert m == n - distance and delta == r + 1 - distance
    assert delta == m - kappa + 1
    assert 0 <= exact_weight <= min(radius, m)
    assert effective_distance == min(m, max(delta, q_value))
    assert denominator == m * effective_distance - 2 * m * exact_weight + exact_weight**2
    if claimed_d is not None:
        assert effective_distance == claimed_d
    if claimed_j is not None:
        assert denominator == claimed_j

    if record["branch"] == "W1":
        assert q_value <= delta
        formula = exact_weight**2 - 2 * m * exact_weight + m * delta
    elif record["branch"] == "W2":
        assert delta < q_value < m
        formula = exact_weight**2 - m * (2 * radius - distance)
    else:
        assert q_value >= m
        formula = (m - exact_weight) ** 2
        assert denominator >= 0
    assert denominator == formula

    strict_wall = (
        record["branch"] == "W1" and formula < 0
    ) or (
        record["branch"] == "W2" and formula < 0
    )
    assert (denominator < 0) == strict_wall

    if denominator == 0 and exact_weight == m and q_value < m:
        assert delta == m and kappa == 1
    if record["branch"] == "W3" and exact_weight < m:
        assert denominator == (m - exact_weight) ** 2 > 0
        h_value = max(1, distance + exact_weight - radius)
        direct_bound = (distance // h_value) * (m // (m - exact_weight))
        assert direct_bound <= n**2
    if record["branch"] == "W3" and exact_weight == m:
        assert q_value - m == n - 2 * radius
        assert n >= 2 * radius
        if n > 2 * radius or radius == m:
            endpoint_bound = 1
        else:
            assert n == 2 * radius and radius > m
            endpoint_bound = distance // (radius - m)
        assert endpoint_bound <= n
    if denominator == 0 and exact_weight < m:
        h_value = max(1, distance + exact_weight - radius)
        equality_bound = 2 * (m - 1) * (distance // h_value)
        assert equality_bound <= 2 * n**2


def exhaustive_parameters(maximum_length=18):
    count = 0
    equality_samples = {"W1": None, "W2": None, "W3": None, "K1": None}
    strict_samples = {"W1": None, "W2": None}
    for length in range(3, maximum_length + 1):
        for redundancy in range(1, length):
            for radius in range(redundancy):
                for distance in range(1, redundancy + 1):
                    punctured_length = length - distance
                    for exact_weight in range(min(radius, punctured_length) + 1):
                        record = parameter_record(
                            length, redundancy, radius, distance, exact_weight
                        )
                        check_parameter_record(record)
                        count += 1
                        branch = record["branch"]
                        if record["J"] < 0 and strict_samples[branch] is None:
                            strict_samples[branch] = record
                        if record["J"] == 0:
                            if exact_weight < punctured_length:
                                equality_samples[branch] = equality_samples[branch] or record
                            elif branch == "W3":
                                equality_samples["W3"] = equality_samples["W3"] or record
                            elif record["q"] < punctured_length:
                                equality_samples["K1"] = equality_samples["K1"] or record

    assert all(equality_samples.values()), equality_samples
    assert all(strict_samples.values()), strict_samples
    return count, equality_samples, strict_samples


def right_angle_family(vectors):
    dimension = len(vectors[0])
    assert all(any(vector) and len(vector) == dimension for vector in vectors)
    for first, second in combinations(vectors, 2):
        assert sum(x * y for x, y in zip(first, second)) <= 0
    assert len(vectors) <= 2 * dimension


def expect_failure(action):
    try:
        action()
    except AssertionError:
        return
    raise AssertionError("tampered claim was accepted")


def tamper_checks(equality_samples):
    sample = equality_samples["W1"]
    expect_failure(
        lambda: check_parameter_record(sample, claimed_d=sample["D"] + 1)
    )
    expect_failure(
        lambda: check_parameter_record(sample, claimed_j=sample["J"] + 1)
    )

    actual_weights = [2, 4, 5]
    expect_failure(lambda: assert_equal(actual_weights, [2, 3, 5]))

    dimension = 4
    basis = [tuple(int(i == j) for j in range(dimension)) for i in range(dimension)]
    sharp_family = basis + [tuple(-value for value in vector) for vector in basis]
    right_angle_family(sharp_family)
    expect_failure(lambda: right_angle_family(sharp_family + [basis[0]]))

    assert comb(6, 2) == 15
    return 4


def assert_equal(actual, expected):
    assert actual == expected


def main():
    parameter_count, equality_samples, strict_samples = exhaustive_parameters()

    code_cases = [
        (5, 4, 3, [1, 2, 3, 4], (1, 1, 0, 0)),
        (5, 5, 3, [1, 2, 4, 3, 1], (1, 0, 1, 1, 0)),
        (7, 6, 4, [1, 2, 3, 4, 5, 6], (1, 1, 0, 1, 0, 0)),
    ]
    code_results = [check_generalized_weight_case(*case) for case in code_cases]
    tamper_count = tamper_checks(equality_samples)

    print("A6 full-support/zero-boundary verification: PASS")
    print(f"  admissible parameter records: {parameter_count}")
    print(
        "  equality witnesses: "
        + ", ".join(
            f"{name}=(N={record['N']},R={record['R']},t={record['t']},"
            f"d={record['d']},e={record['e']})"
            for name, record in equality_samples.items()
        )
    )
    print(
        "  strict-wall falsifiers: "
        + ", ".join(
            f"{name}=(N={record['N']},R={record['R']},t={record['t']},"
            f"d={record['d']},e={record['e']},J={record['J']})"
            for name, record in strict_samples.items()
        )
    )
    print(
        "  generalized-weight cases: "
        + ", ".join(
            f"d={distance}, weights={weights}, masks={masks}"
            for distance, weights, masks in code_results
        )
    )
    print(f"  deliberate tamper checks rejected: {tamper_count}")


if __name__ == "__main__":
    main()
