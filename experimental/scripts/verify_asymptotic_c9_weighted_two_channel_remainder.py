#!/usr/bin/env python3
"""Finite scans for the weighted two-channel remainder compiler."""

from __future__ import annotations

import itertools
import json
from collections import defaultdict


LISTS = ((0,), (0, 1), (0, -1))


def check(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def order_power_of_two_root(p: int, n: int) -> int:
    for value in range(2, p):
        if pow(value, n, p) == 1 and pow(value, n // 2, p) != 1:
            return value
    raise AssertionError((p, n))


def evaluate(word: tuple[int, ...], root: int, p: int) -> int:
    return sum(value * pow(root, index, p) for index, value in enumerate(word)) % p


def inherited_sets(interval: tuple[int, ...], h: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    odd = tuple(sorted(((index - 1) // 2) % h for index in interval if index % 2))
    even = tuple(sorted((index // 2) % h for index in interval if index % 2 == 0))
    return odd, even


def pure_window_max(h: int, p: int, eta: int, even: tuple[int, ...]) -> int:
    maximum = 0
    roots = tuple(pow(eta, exponent, p) for exponent in even)
    for mask in itertools.product(range(3), repeat=h):
        count = 0
        for word in itertools.product(*(LISTS[state] for state in mask)):
            if all(evaluate(word, root, p) == 0 for root in roots):
                count += 1
        maximum = max(maximum, count)
    return maximum


def po_at_least_integer(p: int, q: int, h: int, threshold: int) -> bool:
    """Decide p^(2q/h) >= threshold without floating arithmetic."""
    if threshold <= 0:
        return True
    return p ** (2 * q) >= threshold**h


def lambda_at_least_width(p: int, q: int, e: int, h: int, width: int) -> bool:
    if 2 * (q + e + 1) >= width:
        return True

    # min{A_o+e+1,4A_o} >= width iff both terms clear width, where
    # A_o=max{p^(2q/h),q+1}.
    first_threshold = width - e - 1
    first = q + 1 >= first_threshold or po_at_least_integer(
        p, q, h, first_threshold
    )
    second = 4 * (q + 1) >= width or (
        (4**h) * (p ** (2 * q)) >= width**h
    )
    return first and second


def check_family(
    mask: tuple[int, ...],
    interval: tuple[int, ...],
    p: int,
    zeta: int,
    t_cache: dict[tuple[int, ...], int],
) -> tuple[int, int]:
    n = len(mask)
    h = n // 2
    eta = pow(zeta, 2, p)
    odd, even = inherited_sets(interval, h)
    q, e = len(odd), len(even)
    check(q + e == len(interval) <= h, ("inherited-size", interval, odd, even))
    check(abs(q - e) <= 1, ("inherited-balance", interval, odd, even))

    roots = tuple(pow(zeta, exponent, p) for exponent in interval)
    family: list[tuple[int, ...]] = []
    words_seen = 0
    for word in itertools.product(*(LISTS[state] for state in mask)):
        words_seen += 1
        if not all(evaluate(word, root, p) == 0 for root in roots):
            continue
        if word[:h] == word[h:]:
            continue
        family.append(word)

    groups: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for word in family:
        remainder = tuple(word[i] - word[i + h] for i in range(h))
        groups[remainder].append(word)

    if even not in t_cache:
        t_cache[even] = pure_window_max(h, p, eta, even)
    child_bound = t_cache[even]
    check(
        all(len(group) <= child_bound for group in groups.values()),
        ("same-remainder-bound", mask, interval, child_bound),
    )

    representatives = [group[0] for group in groups.values()]
    remainders = {
        word: tuple(word[i] - word[i + h] for i in range(h)) for word in family
    }

    pair_checks = 0
    for left, right in itertools.combinations(family, 2):
        if remainders[left] == remainders[right]:
            continue
        delta_a = tuple(left[i] - right[i] for i in range(h))
        delta_b = tuple(left[i + h] - right[i + h] for i in range(h))
        delta = tuple(a - b for a, b in zip(delta_a, delta_b))
        tau = tuple(a + b for a, b in zip(delta_a, delta_b))
        check(any(delta), ("distinct-remainders", mask, interval))

        for exponent in odd:
            check(
                evaluate(delta, (zeta * pow(eta, exponent, p)) % p, p) == 0,
                ("odd-root", mask, interval, exponent, delta),
            )
        for exponent in even:
            check(
                evaluate(tau, pow(eta, exponent, p), p) == 0,
                ("even-root", mask, interval, exponent, tau),
            )

        energy = sum(value * value for value in delta) + sum(
            value * value for value in tau
        )
        distance = sum(a != b for a, b in zip(left, right))
        check(energy == 2 * distance, ("energy-identity", energy, distance))
        check(distance >= q + e + 1, ("full-window-distance", distance, q, e))

        if any(tau):
            delta_energy = sum(value * value for value in delta)
            tau_energy = sum(value * value for value in tau)
            check(
                delta_energy**h >= p ** (2 * q),
                ("odd-resultant", mask, interval, delta_energy, p, q, h),
            )
            check(delta_energy >= q + 1, ("odd-mds", delta_energy, q))
            check(tau_energy >= e + 1, ("even-mds", tau_energy, e))
        else:
            check(all(value % 2 == 0 for value in delta), ("tau-zero", delta))
            r_energy = sum((value // 2) ** 2 for value in delta)
            check(
                r_energy**h >= p ** (2 * q),
                ("tau-zero-resultant", mask, interval, r_energy, p, q, h),
            )
            check(r_energy >= q + 1, ("tau-zero-mds", r_energy, q))
        pair_checks += 1

    width = sum(state != 0 for state in mask)
    if lambda_at_least_width(p, q, e, h, width):
        representative_bound = max(1, 2 * width)
        check(
            len(representatives) <= representative_bound,
            ("representative-bound", mask, interval, len(representatives)),
        )
        check(
            len(family) <= representative_bound * child_bound,
            ("weighted-bound", mask, interval, len(family), child_bound),
        )

    return words_seen, pair_checks


def selected_length_eight_masks() -> tuple[tuple[int, ...], ...]:
    return (
        (1,) * 8,
        (2,) * 8,
        (1, 2) * 4,
        (1, 0, 2, 1, 0, 2, 1, 0),
        (0, 0, 1, 1, 2, 2, 1, 2),
        (1, 1, 1, 1, 0, 0, 0, 0),
    )


def run_scan(n: int, p: int, masks: tuple[tuple[int, ...], ...]) -> dict[str, int]:
    check(n & (n - 1) == 0, ("length-not-power-two", n))
    check((p - 1) % n == 0, ("nonsplit-fixture", n, p))
    h = n // 2
    zeta = order_power_of_two_root(p, n)
    t_cache: dict[tuple[int, ...], int] = {}
    families = words = pairs = 0
    for length in range(1, h + 1):
        for start in range(n):
            interval = tuple((start + offset) % n for offset in range(length))
            for mask in masks:
                checked_words, checked_pairs = check_family(
                    mask, interval, p, zeta, t_cache
                )
                families += 1
                words += checked_words
                pairs += checked_pairs
    return {"families": families, "words": words, "pairs": pairs}


def main() -> None:
    exhaustive_four = tuple(itertools.product(range(3), repeat=4))
    four = run_scan(4, 5, exhaustive_four)
    eight = run_scan(8, 17, selected_length_eight_masks())
    result = {
        "status": "PASS",
        "length4": four,
        "length8": eight,
    }
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
