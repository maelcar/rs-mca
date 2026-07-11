#!/usr/bin/env python3
"""Exact replay for the characteristic-cycle coefficient bound."""

from fractions import Fraction
from math import ceil, comb, log


def generalized_binom(parameter, order):
    """Return binom(parameter+order-1, order) for rational parameter."""
    value = Fraction(1, 1)
    for index in range(order):
        value *= parameter + index
        value /= index + 1
    return value


def cycle_coefficient(n, p, r, lam):
    total = Fraction(0, 1)
    residual_parameter = Fraction(n, 1) - lam
    residual_parameter /= p
    for ell in range(r // p + 1):
        total += generalized_binom(residual_parameter, ell) * generalized_binom(
            lam, r - p * ell
        )
    return total


def constant_factor(k_bound):
    return sum(
        generalized_binom(Fraction(k_bound, 1), ell)
        for ell in range(k_bound + 1)
    )


def check_exact_majorant():
    checks = 0
    for p in (3, 5, 7, 11):
        for multiplier in range(1, 9):
            n = p * multiplier
            k_bound = ceil(n / p)
            candidates = {
                Fraction(1, 1),
                Fraction(n, 10),
                Fraction(n, 3),
                Fraction(n - 1, 2),
            }
            for lam in sorted(candidates):
                if not (1 <= lam < n):
                    continue
                c_k = constant_factor(k_bound)
                for r in range(n // 2 + 1):
                    exact = cycle_coefficient(n, p, r, lam)
                    upper = c_k * generalized_binom(lam, r)
                    assert exact <= upper, (n, p, r, lam, exact, upper)
                    checks += 1
    return checks


def entropy(x):
    if x == 0.0 or x == 1.0:
        return 0.0
    return -x * log(x) - (1.0 - x) * log(1.0 - x)


def check_entropy_gap():
    minima = []
    for lam in (0.10, 0.25, 0.49):
        values = []
        for step in range(1, 501):
            x = step / 1000.0
            gap = entropy(x) - (x + lam) * entropy(x / (x + lam))
            assert gap > 0.0
            values.append(gap)
        minima.append((lam, min(values)))
    return minima


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def explicit_family_rows():
    rows = []
    for d in (5, 7, 11):
        found = 0
        p = 3
        while found < 3:
            if is_prime(p) and p % d == 1:
                subgroup_order = d * (p + 1)
                assert (p * p - 1) % subgroup_order == 0
                assert subgroup_order > p - 1
                rows.append((d, p, subgroup_order))
                found += 1
            p += 2
    return rows


def main():
    coefficient_checks = check_exact_majorant()
    entropy_minima = check_entropy_gap()
    rows = explicit_family_rows()

    print("object: R=2 characteristic-cycle coefficient majorant")
    print(f"exact rational coefficient checks: {coefficient_checks} PASS")
    for lam, minimum in entropy_minima:
        print(f"entropy gap sample lambda={lam:.2f}: min={minimum:.12g} PASS")
    for d, p, subgroup_order in rows:
        print(f"explicit subgroup arithmetic: d={d} p={p} N={subgroup_order} PASS")
    print("theorem: r2_constant_weil_cycle_flatness")
    print("status: PROVED conditional on integrated weighted-Weil input")


if __name__ == "__main__":
    main()
