#!/usr/bin/env python3
"""Exact finite replay for the affine-prefix line fibre bifurcation."""

from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import comb, exp, log


Q = [1, 4, 4, 4, 1]
P = [1, 4, 5, 4, 1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def power(poly: list[int], exponent: int) -> list[int]:
    out = [1]
    base = poly[:]
    while exponent:
        if exponent & 1:
            out = multiply(out, base)
        base = multiply(base, base)
        exponent //= 2
    return out


def coefficient(poly: list[int], degree: int) -> int:
    return poly[degree] if 0 <= degree < len(poly) else 0


def local_signature_census() -> Counter[tuple[int, int, int]]:
    points = [(0, 0), (1, 0), (0, 1), (1, 1)]
    census: Counter[tuple[int, int, int]] = Counter()
    for mask in range(1 << 4):
        chosen = [points[i] for i in range(4) if mask & (1 << i)]
        census[(len(chosen), sum(x for x, _ in chosen) % 5,
                sum(y for _, y in chosen) % 5)] += 1
    return census


def b2_histogram() -> Counter[int]:
    points = []
    for block in range(2):
        for eps, eta in ((0, 0), (1, 0), (0, 1), (1, 1)):
            vector = [0] * 6
            vector[3 * block] = 1
            vector[3 * block + 1] = eps
            vector[3 * block + 2] = eta
            points.append(tuple(vector))

    fibres: Counter[tuple[int, ...]] = Counter()
    for indices in combinations(range(8), 4):
        syndrome = tuple(sum(points[i][j] for i in indices) % 5
                         for j in range(6))
        fibres[syndrome] += 1
    return Counter(fibres.values())


def l_value(blocks: int, ambiguous: int) -> int:
    remaining = blocks - ambiguous
    return comb(blocks, ambiguous) * coefficient(
        power(Q, remaining), 2 * remaining
    )


def main() -> None:
    local = local_signature_census()
    require(len(local) == 15, "wrong local signature count")
    require(Counter(local.values()) == Counter({1: 14, 2: 1}),
            "wrong local ambiguity pattern")

    histogram = b2_histogram()
    require(histogram == Counter({1: 50, 2: 8, 4: 1}),
            f"wrong B=2 histogram: {histogram}")

    for blocks in range(1, 11):
        values = [l_value(blocks, j) for j in range(blocks + 1)]
        require(sum(values) == coefficient(power(P, blocks), 2 * blocks),
                f"syndrome identity failed at B={blocks}")
        require(sum((2**j) * values[j] for j in range(blocks + 1))
                == comb(4 * blocks, 2 * blocks),
                f"support identity failed at B={blocks}")

    for j in range(13):
        distribution = {2**ell: comb(j, ell) * 2 ** (j - ell)
                        for ell in range(j + 1)}
        require(sum(distribution.values()) == 3**j,
                f"representation support failed at j={j}")
        for tau in range(5):
            moment = sum(count * multiplicity**tau
                         for multiplicity, count in distribution.items())
            require(moment == (2 + 2**tau) ** j,
                    f"moment failed at j={j}, tau={tau}")

    for blocks in range(2, 101):
        field_size = 5 ** (3 * blocks)
        separator_cost = 4 * blocks + (2 * blocks - 2) * comb(2**blocks, 2)
        require(field_size > separator_cost,
                f"separator inequality failed at B={blocks}")

    eta = log((9**9 * 2**9) / (14 * 10**10)) / 10
    require(abs(eta - 0.0348437561509767) < 1e-15, "wrong eta")
    for blocks in range(2, 101):
        for j in range(blocks + 1):
            if 10 * j < 9 * blocks:
                continue
            value = l_value(blocks, j)
            if value:
                require(log(value) <= j * log(2) - eta * blocks + 1e-12,
                        f"high-switch envelope failed at B={blocks}, j={j}")

    mutations = {
        "all_local_signatures_unique": max(local.values()) == 1,
        "wrong_b2_top_fibre": histogram[4] != 1,
        "nonpositive_reserve": eta <= 0,
    }
    require(not any(mutations.values()), f"tamper survived: {mutations}")

    print("AFFINE_PREFIX_LINE_FIBRE_BIFURCATION: PASS")
    print("local_signatures=15 ambiguity_pattern=14x1+1x2")
    print("B2_histogram=size1:50,size2:8,size4:1 supports=70")
    print("generating_function_checks=B1..B10")
    print("representation_moments=j0..j12,tau0..tau4")
    print("separator_checks=B2..B100")
    print(f"eta={eta:.17f} high_switch_checks=B2..B100")
    print("tamper_checks=3/3")


if __name__ == "__main__":
    main()
