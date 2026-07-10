#!/usr/bin/env python3
"""Exact small-field checks for the direction-distance ray compiler."""

from collections import defaultdict
from itertools import combinations, product


def add(a, b, q):
    return tuple((x + y) % q for x, y in zip(a, b))


def scale(c, a, q):
    return tuple(c * x % q for x in a)


def weight(a):
    return sum(x != 0 for x in a)


def parity_columns(q, n, redundancy):
    points = list(range(n))
    return [tuple(pow(x, j, q) for j in range(redundancy)) for x in points]


def syndrome(word, columns, q):
    return tuple(
        sum(word[i] * columns[i][j] for i in range(len(word))) % q
        for j in range(len(columns[0]))
    )


def normalize_projective(v, q):
    first = next(x for x in v if x)
    inv = pow(first, -1, q)
    return tuple(inv * x % q for x in v)


def errors(q, n, radius):
    yield (0,) * n
    for size in range(1, radius + 1):
        for support in combinations(range(n), size):
            for values in product(range(1, q), repeat=size):
                row = [0] * n
                for i, value in zip(support, values):
                    row[i] = value
                yield tuple(row)


def extension_code(kernel, lift, q):
    return {
        add(z, scale(gamma, lift, q), q)
        for gamma in range(q)
        for z in kernel
    }


def maximum_ball_list(code, q, radius):
    counts = defaultdict(int)
    errs = list(errors(q, len(next(iter(code))), radius))
    for word in code:
        for err in errs:
            counts[add(word, err, q)] += 1
    return max(counts.values()), len(counts), len(errs)


def compiler_bound(n, t, distance):
    mu = n - distance
    denominator = (n - t) ** 2 - n * mu
    assert denominator > 0
    return n * (distance - t) // denominator


def exhaustive_projective_chart(q, n, redundancy, t):
    columns = parity_columns(q, n, redundancy)
    words = list(product(range(q), repeat=n))
    fibers = defaultdict(list)
    for word in words:
        fibers[syndrome(word, columns, q)].append(word)
    zero = (0,) * redundancy
    kernel = set(fibers[zero])
    kappa = n - redundancy

    assert len(kernel) == q**kappa
    assert min(weight(z) for z in kernel if any(z)) == redundancy + 1

    directions = {}
    for y, lifts in fibers.items():
        if y == zero:
            continue
        key = normalize_projective(y, q)
        directions.setdefault(key, lifts[0])

    paid = 0
    mds = 0
    min_slack = None
    for y, lift in directions.items():
        coset = [add(lift, z, q) for z in kernel]
        distance = min(map(weight, coset))
        mu = n - distance
        if (n - t) ** 2 <= n * mu:
            continue
        paid += 1
        if distance == redundancy:
            mds += 1
        code = extension_code(kernel, lift, q)
        observed, _, _ = maximum_ball_list(code, q, t)
        bound = compiler_bound(n, t, distance)
        assert observed <= bound <= n * n
        slack = bound - observed
        min_slack = slack if min_slack is None else min(min_slack, slack)

    return {
        "q": q,
        "n": n,
        "redundancy": redundancy,
        "kappa": kappa,
        "t": t,
        "projective_directions": len(directions),
        "paid_directions": paid,
        "direction_mds": mds,
        "minimum_bound_slack": min_slack,
    }


def explicit_mds_chart(q, n, redundancy, t):
    columns = parity_columns(q, n, redundancy)
    kappa = n - redundancy
    points = list(range(n))

    # K_U = {(omega_u p(u)) : deg p < kappa}.
    omega = []
    for u in points:
        derivative = 1
        for v in points:
            if u != v:
                derivative = derivative * (u - v) % q
        omega.append(pow(derivative, -1, q))

    kernel = set()
    for coeffs in product(range(q), repeat=kappa):
        row = []
        for u, w in zip(points, omega):
            value = sum(coeffs[j] * pow(u, j, q) for j in range(kappa)) % q
            row.append(w * value % q)
        kernel.add(tuple(row))

    lift = tuple(w * pow(u, kappa, q) % q for u, w in zip(points, omega))
    direction = syndrome(lift, columns, q)
    assert any(direction)
    assert all(syndrome(z, columns, q) == (0,) * redundancy for z in kernel)

    distance = min(weight(add(lift, z, q)) for z in kernel)
    assert distance == redundancy
    code = extension_code(kernel, lift, q)
    observed, centers, error_count = maximum_ball_list(code, q, t)
    bound = compiler_bound(n, t, distance)
    assert observed <= bound <= n * n
    return {
        "q": q,
        "n": n,
        "redundancy": redundancy,
        "kappa": kappa,
        "t": t,
        "distance": distance,
        "bound": bound,
        "observed_max": observed,
        "centers_reached": centers,
        "errors_per_codeword": error_count,
    }


def main():
    rows = [
        explicit_mds_chart(5, 5, 4, 2),
        explicit_mds_chart(7, 6, 4, 2),
        exhaustive_projective_chart(5, 5, 4, 2),
        exhaustive_projective_chart(5, 5, 3, 1),
        exhaustive_projective_chart(5, 5, 2, 1),
    ]

    assert rows[0] == {
        "q": 5, "n": 5, "redundancy": 4, "kappa": 1, "t": 2,
        "distance": 4, "bound": 2, "observed_max": 2,
        "centers_reached": 3025, "errors_per_codeword": 181,
    }
    assert rows[1] == {
        "q": 7, "n": 6, "redundancy": 4, "kappa": 2, "t": 2,
        "distance": 4, "bound": 3, "observed_max": 3,
        "centers_reached": 113533, "errors_per_codeword": 577,
    }
    assert rows[2]["projective_directions"] == 156
    assert rows[2]["paid_directions"] == 6
    assert rows[2]["direction_mds"] == 6
    assert rows[2]["minimum_bound_slack"] == 0
    assert rows[3]["projective_directions"] == 31
    assert rows[3]["paid_directions"] == 26
    assert rows[3]["direction_mds"] == 1
    assert rows[3]["minimum_bound_slack"] == 0
    assert rows[4]["projective_directions"] == 6
    assert rows[4]["paid_directions"] == 1
    assert rows[4]["direction_mds"] == 1
    assert rows[4]["minimum_bound_slack"] == 0

    for row in rows:
        print(row)
    print("RESULT: PASS")


if __name__ == "__main__":
    main()
