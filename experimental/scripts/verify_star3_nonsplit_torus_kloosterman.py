#!/usr/bin/env python3
"""Finite checks for the star3 nonsplit-torus Kloosterman reduction."""

from __future__ import annotations

import cmath
import itertools
import json
import math
from collections import Counter


ROWS = ((17, 16, 9, 2), (23, 22, 12, 9), (257, 64, 36, 58))


def check(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


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


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for value in range(2, p):
        if all(pow(value, (p - 1) // factor, p) != 1 for factor in factors):
            return value
    raise AssertionError(p)


def arc(p: int, n: int, t: int) -> tuple[list[int], int]:
    check((p - 1) % n == 0, ("bad-arc", p, n))
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values = [pow(omega, index, p) for index in range(t)]
    return values[:-1], values[-1]


def high_pair(x: int, y: int, zeta: int, p: int) -> tuple[int, int]:
    return ((x + y + zeta) % p, (x * y + zeta * (x + y)) % p)


def high_triple(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    return ((a + b + c) % p, (a * b + a * c + b * c) % p)


def direct_incidence(p: int, values: list[int], zeta: int) -> int:
    pairs = Counter(
        high_pair(x, y, zeta, p) for x, y in itertools.combinations(values, 2)
    )
    triples = Counter(
        high_triple(a, b, c, p)
        for a, b, c in itertools.combinations(values, 3)
    )
    return sum(count * triples[high] for high, count in pairs.items())


def rational_orbit_count(p: int, values: list[int], zeta: int) -> int:
    members = set(values)
    total = 0
    for x in values:
        for y in values:
            if x == y:
                continue
            for u in range(p):
                denominator = (u * u + u + 1) % p
                check(denominator != 0, ("split-denominator", p, u))
                inverse = pow(denominator, -1, p)
                alpha = u * (u + 1) * inverse % p
                beta = (u + 1) * inverse % p
                gamma = -u * inverse % p
                a = (alpha * x + beta * y + gamma * zeta) % p
                b = (gamma * x + alpha * y + beta * zeta) % p
                c = (beta * x + gamma * y + alpha * zeta) % p
                if a in members and b in members and c in members and len({a, b, c}) == 3:
                    total += 1
    return total


def extension_norm(a: int, b: int, p: int) -> int:
    # rho^2+rho+1=0, so N(a+b rho)=a^2-ab+b^2.
    return (a * a - a * b + b * b) % p


def extension_trace(a: int, b: int, p: int) -> int:
    return (2 * a - b) % p


def verify_histograms(p: int) -> int:
    checks = 0
    for c in range(1, p):
        norm_trace = Counter()
        for a in range(p):
            for b in range(p):
                if extension_norm(a, b, p) == c:
                    norm_trace[extension_trace(a, b, p)] += 1
        split = Counter((w + c * pow(w, -1, p)) % p for w in range(1, p))
        for s in range(p):
            check(
                norm_trace[s] + split[s] == 2,
                ("norm-trace-histogram", p, c, s, norm_trace[s], split[s]),
            )
            checks += 1
    return checks


def fourier_reconstruction(p: int, values: list[int], zeta: int, incidence: int) -> None:
    psi = [cmath.exp(2j * math.pi * index / p) for index in range(p)]
    ga = [sum(psi[(-h * a) % p] for a in values) for h in range(p)]

    def fhat(l0: int, l1: int, l2: int) -> complex:
        return (
            ga[l0] * ga[l1] * ga[l2]
            - ga[(l0 + l1) % p] * ga[l2]
            - ga[(l0 + l2) % p] * ga[l1]
            - ga[(l1 + l2) % p] * ga[l0]
            + 2 * ga[(l0 + l1 + l2) % p]
        )

    triple_sum_counts = Counter(
        (a + b + c) % p
        for a in values
        for b in values
        for c in values
        if len({a, b, c}) == 3
    )
    c_diag = (p + 1) / (p * p) * sum(
        triple_sum_counts[(x + y + zeta) % p]
        for x in values
        for y in values
        if x != y
    )

    kl = {}
    for c in range(1, p):
        kl[c] = sum(
            psi[(w + c * pow(w, -1, p)) % p] for w in range(1, p)
        )

    inv3 = pow(3, -1, p)
    inv9 = pow(9, -1, p)
    accumulator = 0j
    modes = 0
    for x in values:
        for y in values:
            if x == y:
                continue
            s = (x + y + zeta) % p
            q_xy = (
                x * x
                + y * y
                + zeta * zeta
                - x * y
                - x * zeta
                - y * zeta
            ) % p
            check(q_xy != 0, ("zero-q", p, x, y, zeta))
            for l0 in range(p):
                for l1 in range(p):
                    for l2 in range(p):
                        if l0 == l1 == l2:
                            continue
                        # kappa=(l0-l1)+rho(l2-l1).
                        ka = (l0 - l1) % p
                        kb = (l2 - l1) % p
                        norm_kappa = extension_norm(ka, kb, p)
                        check(
                            norm_kappa != 0,
                            ("off-diagonal-zero-kappa", p, l0, l1, l2),
                        )
                        parameter = norm_kappa * q_xy * inv9 % p
                        phase = psi[((l0 + l1 + l2) * s * inv3) % p]
                        accumulator += fhat(l0, l1, l2) * phase * kl[parameter]
                        modes += 1

    c_kl = -accumulator / (p**3)
    reconstructed = c_diag + c_kl
    check(abs(reconstructed.imag) < 1e-6, ("imaginary-residue", p, reconstructed))
    check(
        abs(reconstructed.real - 12 * incidence) < 1e-5,
        (p, reconstructed, 12 * incidence),
    )
    check(
        modes == len(values) * (len(values) - 1) * (p**3 - p),
        ("mode-count", p, modes),
    )


def verify_deployed() -> None:
    p = 2_130_706_433
    n = 2**21
    omega = 1_213_133_211
    e = 67_472
    m = 1_183_519
    h2 = e * p // 1_860
    d2 = m * (m - 1)
    d3 = m * (m - 1) * (m - 2)
    p2 = p * p
    budget_numerator = 12 * h2 * p2 - d2 * d3
    check(h2 == 77_291_948_627, ("H2", h2))
    check((p - 1) % n == 0, ("domain-divisibility", p, n))
    check(pow(omega, n, p) == 1, ("omega-upper-order", omega, n, p))
    check(
        pow(omega, n // 2, p) != 1,
        ("omega-exact-order", omega, n, p),
    )
    check(m == n // 2 + 2 * e - 1, ("prefix-length", m, n, e))
    check(e * p % 1_860 == 1_156, ("H2-remainder", e * p % 1_860))
    check(d2 == 1_400_716_039_842, ("D2", d2))
    check(d3 == 1_657_771_245_325_684_314, ("D3", d3))
    check(p2 == 4_539_909_903_627_583_489, ("p2", p2))
    check(
        budget_numerator == 1_888_715_022_792_167_261_828_558_596_848,
        ("budget", budget_numerator),
    )
    check(2 * math.sqrt(p) < 92_320, ("weil-constant", 2 * math.sqrt(p)))
    check(
        (p + 1) / (2 * math.sqrt(p)) > 23_079,
        ("modewise-gain", (p + 1) / (2 * math.sqrt(p))),
    )


def main() -> None:
    row_results = []
    for p, n, t, expected in ROWS:
        values, zeta = arc(p, n, t)
        incidence = direct_incidence(p, values, zeta)
        orbit_count = rational_orbit_count(p, values, zeta)
        check(incidence == expected, ("incidence", p, incidence, expected))
        check(orbit_count == 12 * incidence, ("orbit-count", p, orbit_count))
        row_results.append((p, incidence, orbit_count))

    histogram_checks = sum(verify_histograms(p) for p in (5, 11, 17))
    for p, n, t, expected in ROWS[:2]:
        values, zeta = arc(p, n, t)
        fourier_reconstruction(p, values, zeta, expected)
    verify_deployed()

    print(
        json.dumps(
            {
                "status": "PASS",
                "rows": row_results,
                "histogram_checks": histogram_checks,
                "fourier_reconstructions": 2,
                "deployed_arithmetic": "PASS",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
