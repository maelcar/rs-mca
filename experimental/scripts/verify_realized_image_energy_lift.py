#!/usr/bin/env python3
"""Verify the realized-image Boolean-slice energy lift (stdlib only)."""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
from math import comb, isclose, log, log2


def layer_count(n: int, total: int, cap: int) -> int:
    row = [0] * (total + 1)
    row[0] = 1
    for _ in range(n):
        nxt = [0] * (total + 1)
        for s, value in enumerate(row):
            if not value:
                continue
            for digit in range(cap + 1):
                if s + digit <= total:
                    nxt[s + digit] += value
        row = nxt
    return row[total]


def h2(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * log2(p) - (1.0 - p) * log2(1.0 - p)


def entropy(probs: tuple[float, ...]) -> float:
    return -sum(p * log2(p) for p in probs if p)


def g(p: float) -> float:
    return entropy(
        (
            (1.0 - p) ** 2 / 2.0,
            (1.0 - p * p) / 2.0,
            p * (2.0 - p) / 2.0,
            p * p / 2.0,
        )
    )


def masks_of_weight(n: int, m: int) -> list[int]:
    return [x for x in range(1 << n) if x.bit_count() == m]


def syndrome(mask: int, coeffs: tuple[int, ...], modulus: int) -> int:
    return sum(coeffs[i] for i in range(len(coeffs)) if mask >> i & 1) % modulus


def sum_code(a: int, b: int, n: int) -> int:
    code = 0
    scale = 1
    for i in range(n):
        code += (((a >> i) & 1) + ((b >> i) & 1)) * scale
        scale *= 3
    return code


def energy(points: tuple[int, ...], n: int) -> int:
    counts = Counter(sum_code(a, b, n) for a in points for b in points)
    return sum(value * value for value in counts.values())


def subsets(points: list[int], exhaustive: bool) -> list[tuple[int, ...]]:
    if exhaustive:
        return [
            tuple(points[i] for i in range(len(points)) if bits >> i & 1)
            for bits in range(1, 1 << len(points))
        ]
    ans = [(point,) for point in points]
    ans.append(tuple(points))
    if len(points) > 2:
        ans.append(tuple(points[::2]))
        ans.append(tuple(points[1::2]))
    return [item for item in ans if item]


def check_map(n: int, modulus: int, coeffs: tuple[int, ...], exhaustive: bool) -> tuple[int, bool]:
    checked = 0
    tamper_rejected = False
    all_image = set()
    by_weight: dict[int, dict[int, list[int]]] = {}
    for m in range(n + 1):
        fibers: dict[int, list[int]] = defaultdict(list)
        for mask in masks_of_weight(n, m):
            s = syndrome(mask, coeffs, modulus)
            fibers[s].append(mask)
            all_image.add((m, s))
        by_weight[m] = fibers

    l_all = len(all_image)
    for m, fibers in by_weight.items():
        theta = m / n
        l_slice = len(fibers)
        a_count = layer_count(n, 2 * m, 2)
        b_count = layer_count(n, 3 * m, 3)
        a_entropy = 1.0 + h2(theta) / 2.0
        g_entropy = g(theta)
        for points in fibers.values():
            for chosen in subsets(points, exhaustive and len(points) <= 9):
                f = len(chosen)
                e = energy(chosen, n)
                assert f * l_slice <= a_count
                assert f * l_slice * f**3 <= b_count * e
                assert f * l_slice <= 2.0 ** (n * a_entropy) + 1e-9
                assert f * l_slice * f**3 <= 2.0 ** (n * g_entropy) * e + 1e-7
                assert f * l_all <= 2.0 ** (n * a_entropy) + 1e-9
                assert f * l_all * f**3 <= 2.0 ** (n * g_entropy) * e + 1e-7
                # The false strengthening fL <= B Delta^2 must not pass all tests.
                if f * l_slice * f**6 > b_count * e * e:
                    tamper_rejected = True
                checked += 6
    return checked, tamper_rejected


def main() -> None:
    checks = 0
    tamper_rejected = False

    # Exhaust every cyclic syndrome map through N=4.
    for n in range(1, 5):
        for modulus in range(2, 5):
            for coeffs in product(range(modulus), repeat=n):
                count, rejected = check_map(n, modulus, coeffs, True)
                checks += count
                tamper_rejected |= rejected

    # Deterministic N=5 stress maps, including repeated and full-rank-looking rows.
    for modulus in range(2, 8):
        candidates = {
            tuple(0 for _ in range(5)),
            tuple(1 for _ in range(5)),
            tuple(i % modulus for i in range(5)),
            tuple((i * i + 1) % modulus for i in range(5)),
        }
        for coeffs in candidates:
            count, rejected = check_map(5, modulus, coeffs, True)
            checks += count
            tamper_rejected |= rejected

    theta0 = 0.173952331409395
    assert isclose(h2(theta0), 2.0 / 3.0, rel_tol=0.0, abs_tol=2e-15)
    g_half = g(0.5)
    gamma0 = g_half - 4.0 / 3.0
    assert isclose(g_half, 3.0 - 0.75 * log2(3.0), abs_tol=1e-15)
    assert isclose(gamma0, 0.477944791125799, abs_tol=2e-15)
    assert isclose(gamma0 * log(2.0), 0.331286084432160, abs_tol=2e-15)
    assert isclose(log(2.0) / log(4.0 / 3.0), 2.409420839653, abs_tol=5e-13)
    assert layer_count(5, 4, 2) == 45
    assert layer_count(5, 6, 3) == 135
    checks += 7

    assert tamper_rejected, "extra-Delta tamper was not rejected"
    print(f"PASS: {checks:,} theorem checks")
    print("PASS: constants and coefficient recurrences")
    print("PASS: strengthened extra-Delta tamper rejected")


if __name__ == "__main__":
    main()
