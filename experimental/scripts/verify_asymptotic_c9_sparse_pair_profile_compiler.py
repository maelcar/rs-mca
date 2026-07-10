#!/usr/bin/env python3
"""Finite checks for the sparse-pair actual-syndrome compiler."""

from __future__ import annotations

import itertools
import json
from collections import defaultdict


FIXTURES = (
    (16, 2, 17, 2),
    (32, 4, 97, 2),
    (64, 8, 193, 3),
    (64, 4, 193, 4),
)


def check(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def order_power_of_two_root(p: int, n: int) -> int:
    for value in range(2, p):
        if pow(value, n, p) == 1 and pow(value, n // 2, p) != 1:
            return value
    raise AssertionError((p, n))


def johnson_distance(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    check(sum(left) == sum(right), ("unequal-weights", left, right))
    return sum(a == 1 and b == 0 for a, b in zip(left, right))


def run_fixture(n: int, b: int, p: int, d: int) -> int:
    check(n & (n - 1) == 0, ("length-not-power-two", n))
    check(b & (b - 1) == 0, ("spacing-not-power-two", b))
    check((p - 1) % n == 0, ("nonsplit-fixture", n, p))
    m = n // b
    check(2 <= d <= m, ("bad-distance", d, m))

    zeta = order_power_of_two_root(p, n)
    xi = pow(zeta, b, p)
    check(pow(xi, m, p) == 1, ("xi-upper-order", xi, m, p))
    check(pow(xi, m // 2, p) != 1, ("xi-exact-order", xi, m, p))

    alpha = 2 % p
    c = 3 % p
    short_fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    long_fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)

    evaluations = 0
    for u in itertools.product((0, 1), repeat=m):
        x = [0] * n
        for j, bit in enumerate(u):
            x[b * j] = bit
            x[b * j + 1] = 1 - bit

        short = tuple(
            sum(u[j] * pow(xi, k * j, p) for j in range(m)) % p
            for k in range(1, d)
        )
        long = tuple(
            c
            * pow(alpha, k - 1, p)
            * sum(x[i] * pow(zeta, k * i, p) for i in range(n))
            % p
            for k in range(1, d)
        )
        predicted = tuple(
            c
            * pow(alpha, k - 1, p)
            * (1 - pow(zeta, k, p))
            * short[k - 1]
            % p
            for k in range(1, d)
        )
        check(long == predicted, (n, b, p, d, u, long, predicted))

        positive_zero = tuple(
            c
            * pow(alpha, k, p)
            * sum(x[i] * pow(zeta, k * i, p) for i in range(n))
            % p
            for k in range(d)
        )
        predicted_zero = (c * m % p,) + tuple(
            c
            * pow(alpha, k, p)
            * (1 - pow(zeta, k, p))
            * short[k - 1]
            % p
            for k in range(1, d)
        )
        check(
            positive_zero == predicted_zero,
            ("positive-a0", n, b, p, d, u, positive_zero, predicted_zero),
        )

        reversed_x = tuple(x[(-i) % n] for i in range(n))
        negative_one = tuple(
            c
            * pow(alpha, k - 1, p)
            * sum(reversed_x[i] * pow(zeta, -k * i, p) for i in range(n))
            % p
            for k in range(1, d)
        )
        negative_zero = tuple(
            c
            * pow(alpha, k, p)
            * sum(reversed_x[i] * pow(zeta, -k * i, p) for i in range(n))
            % p
            for k in range(d)
        )
        check(
            negative_one == predicted,
            ("negative-a1", n, b, p, d, u, negative_one, predicted),
        )
        check(
            negative_zero == predicted_zero,
            ("negative-a0", n, b, p, d, u, negative_zero, predicted_zero),
        )
        short_fibers[short].append(u)
        long_fibers[long].append(u)
        evaluations += 1

    check(
        sorted(map(len, short_fibers.values()))
        == sorted(map(len, long_fibers.values())),
        ("fiber-multisets", n, b, p, d),
    )

    for fiber in short_fibers.values():
        by_weight: dict[int, list[tuple[int, ...]]] = defaultdict(list)
        for word in fiber:
            by_weight[sum(word)].append(word)
        for weight, words in by_weight.items():
            for left, right in itertools.combinations(words, 2):
                check(
                    johnson_distance(left, right) >= d,
                    ("johnson-separation", n, b, d, weight, left, right),
                )

            size = len(words)
            q_num = weight * (m - weight)
            gap_num = d * m - q_num
            if gap_num > 0:
                check(
                    size * gap_num <= d * m,
                    ("strict-plotkin", n, b, d, weight, size),
                )
            elif gap_num == 0:
                check(
                    size <= 2 * (m - 1),
                    ("equality-plotkin", n, b, d, weight, size),
                )

    maximum = max(map(len, short_fibers.values()))
    if 4 * d > m:
        check(
            maximum * (4 * d - m) <= (m + 1) * 4 * d,
            ("full-strict-bound", n, b, d, maximum),
        )
    elif 4 * d == m:
        check(
            maximum <= m * m + 2 * m - 2,
            ("full-equality-bound", n, b, d, maximum),
        )

    return evaluations


def main() -> None:
    evaluations = sum(run_fixture(*fixture) for fixture in FIXTURES)
    check(evaluations == 66304, ("evaluation-count", evaluations))
    print(
        json.dumps(
            {
                "status": "PASS",
                "fixtures": len(FIXTURES),
                "evaluations": evaluations,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
