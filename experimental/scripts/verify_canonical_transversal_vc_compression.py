#!/usr/bin/env python3
"""Exact small-instance checks for canonical_transversal_vc_compression.md."""

from collections import Counter
from itertools import combinations, product


def subset_sums(values, modulus=None):
    sums = [0]
    for value in values:
        sums += [x + value for x in sums]
    if modulus is not None:
        sums = [x % modulus for x in sums]
    return sums


def dissociation_dimension(values, modulus=None):
    b = len(values)
    for d in range(b, -1, -1):
        for indices in combinations(range(b), d):
            sums = subset_sums([values[i] for i in indices], modulus)
            if len(set(sums)) == 1 << d:
                return d
    raise AssertionError("unreachable")


def binomial_prefix(b, d):
    total = 0
    term = 1
    for j in range(d + 1):
        if j:
            term = term * (b - j + 1) // j
        total += term
    return total


def minimum_cost_transversal(values, modulus=None):
    b = len(values)
    best = {}
    for mask in range(1 << b):
        value = sum(values[i] for i in range(b) if mask >> i & 1)
        if modulus is not None:
            value %= modulus
        best.setdefault(value, mask)  # numeric mask is the binary cost
    return set(best.values())


def vc_dimension(family, b):
    for d in range(b, -1, -1):
        for indices in combinations(range(b), d):
            traces = {
                tuple((mask >> i) & 1 for i in indices) for mask in family
            }
            if len(traces) == 1 << d:
                return d
    raise AssertionError("unreachable")


def audit(values, modulus=None):
    b = len(values)
    counts = Counter(subset_sums(values, modulus))
    f = max(counts.values())
    image = len(counts)
    d = dissociation_dimension(values, modulus)
    family = minimum_cost_transversal(values, modulus)
    vcdim = vc_dimension(family, b)
    assert f <= 1 << (b - d)
    assert image == len(family)
    assert vcdim <= d
    assert image <= binomial_prefix(b, d)
    assert f * image <= 3**b
    return 5


def main():
    checks = 0
    instances = 0

    # Exhaust every indexed sequence of length at most four in small cyclic
    # groups. Repetitions are allowed; the theorem does not require distinct
    # group elements.
    for modulus in range(2, 8):
        for b in range(1, 5):
            for values in product(range(modulus), repeat=b):
                checks += audit(values, modulus)
                instances += 1

    # Targeted larger cyclic instances.
    for modulus, values in (
        (11, (0, 1, 3, 4, 7)),
        (13, (0, 1, 2, 5, 8, 12)),
        (17, (0, 2, 3, 7, 8, 11, 15)),
    ):
        checks += audit(values, modulus)
        instances += 1

    # Integer moment-curve blocks used by the RS-MCA consumer. Keep these at
    # size eight so the exact VC-dimension regression remains quick.
    for values in (
        tuple(range(8)),
        (0, 1, 4, 9, 11, 16, 22, 25),
        tuple(1 << i for i in range(8)),
    ):
        columns = [(1, v, v * v) for v in values]
        # Encode the finite list of integer triples injectively for this check.
        bound = 1 + sum(v * v for v in values)
        encoded = [a + bound * (s + bound * q) for a, s, q in columns]
        checks += audit(encoded)
        instances += 1

    print(f"RESULT: PASS ({checks} assertions, {instances} exact instances)")


if __name__ == "__main__":
    main()
