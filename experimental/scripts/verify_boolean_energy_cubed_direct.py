#!/usr/bin/env python3
from collections import Counter
from itertools import product
from random import Random


def poly_add(a, b, scale=1):
    out = dict(a)
    for mon, coeff in b.items():
        out[mon] = out.get(mon, 0) + scale * coeff
        if out[mon] == 0:
            del out[mon]
    return out


def poly_mul(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, ell), y in b.items():
            mon = (i + k, j + ell)
            out[mon] = out.get(mon, 0) + x * y
    return {mon: coeff for mon, coeff in out.items() if coeff}


def poly_pow(a, exponent):
    out = {(0, 0): 1}
    base = a
    while exponent:
        if exponent & 1:
            out = poly_mul(out, base)
        base = poly_mul(base, base)
        exponent //= 2
    return out


def monomial(coeff, i, j):
    return {} if coeff == 0 else {(i, j): coeff}


def verify_polynomial_certificate():
    u3_v3 = {(3, 0): 1, (0, 3): 1}
    mixed = {(8, 0): 1, (0, 8): 1, (4, 4): 4}
    lhs = poly_add(poly_pow(u3_v3, 8), poly_pow(mixed, 3), scale=-1)

    coeffs = (8, 112, 464, 976, 1169, 814, 304, 56, 4)
    u_minus_v = {(1, 0): 1, (0, 1): -1}
    total = {}
    for index, coeff in enumerate(coeffs):
        term = poly_mul(
            monomial(coeff, 11 - index, 11 - index),
            poly_pow(u_minus_v, 2 * index),
        )
        total = poly_add(total, term)
    factor = {(2, 0): 2, (1, 1): 1, (0, 2): 2}
    assert lhs == poly_mul(factor, total)

    tampered = list(coeffs)
    tampered[4] += 1
    bad_total = {}
    for index, coeff in enumerate(tampered):
        bad_total = poly_add(
            bad_total,
            poly_mul(
                monomial(coeff, 11 - index, 11 - index),
                poly_pow(u_minus_v, 2 * index),
            ),
        )
    assert lhs != poly_mul(factor, bad_total)


def energy(family):
    if not family:
        return 0
    reps = Counter(
        tuple(x - y for x, y in zip(a, b))
        for a in family
        for b in family
    )
    return sum(value * value for value in reps.values())


def verify_all_small_families():
    checked = 0
    equality = 0
    for dimension in range(5):
        cube = list(product((0, 1), repeat=dimension))
        for mask in range(1 << len(cube)):
            family = [cube[i] for i in range(len(cube)) if mask & (1 << i)]
            value = energy(family)
            size = len(family)
            assert value ** 3 <= size ** 8
            checked += 1
            equality += value ** 3 == size ** 8
    return checked, equality


def verify_random_dimension_five():
    rng = Random(20260711)
    cube = list(product((0, 1), repeat=5))
    for _ in range(2000):
        family = [point for point in cube if rng.randrange(2)]
        value = energy(family)
        size = len(family)
        assert value ** 3 <= size ** 8


def main():
    verify_polynomial_certificate()
    checked, equality = verify_all_small_families()
    verify_random_dimension_five()
    print("RESULT: PASS")
    print(f"exhaustive_families={checked}")
    print(f"equality_cases={equality}")
    print("random_dimension_five=2000")
    print("polynomial_certificate=PASS")
    print("tamper_check=PASS")


if __name__ == "__main__":
    main()
