#!/usr/bin/env python3
"""Replay the exact hypothesis repair for the depth-one twin-pair theorem."""

from itertools import combinations, product
from math import comb


def distinct_subset_sums(values):
    seen = set()
    for size in range(len(values) + 1):
        for subset in combinations(values, size):
            total = sum(subset)
            if total in seen:
                return False
            seen.add(total)
    return True


def two_dissociated(values):
    seen = set()
    for coefficients in product((-1, 0, 1), repeat=len(values)):
        total = sum(c * value for c, value in zip(coefficients, values))
        if total in seen:
            return False
        seen.add(total)
    return True


def domain(values, center):
    return tuple(sorted(set(values) | {center - x for x in values}))


def central_fiber_integer(values, center):
    points = domain(values, center)
    target = (len(values) // 2) * center
    return points, {
        tuple(support)
        for support in combinations(points, len(values))
        if sum(support) == target
    }


def central_fiber_mod(values, center):
    points = domain(values, center)
    target = ((len(values) // 2) * center) % center
    return points, {
        tuple(support)
        for support in combinations(points, len(values))
        if sum(support) % center == target
    }


def image_mod(values, center):
    points = domain(values, center)
    return {
        sum(support) % center
        for support in combinations(points, len(values))
    }


def twin_unions(values, center):
    pairs = tuple((x, center - x) for x in values)
    return {
        tuple(sorted(item for index in choice for item in pairs[index]))
        for choice in combinations(range(len(values)), len(values) // 2)
    }


def require(condition, label):
    if not condition:
        raise AssertionError(label)
    print(f"PASS: {label}")


def check_exact_fiber(values, center, label):
    integer_domain, integer_fiber = central_fiber_integer(values, center)
    modular_domain, modular_fiber = central_fiber_mod(values, center)
    twins = twin_unions(values, center)
    require(integer_domain == modular_domain, f"{label}: integer/modular domains agree")
    require(len(integer_domain) == 2 * len(values), f"{label}: 2B distinct coordinates")
    require(integer_fiber == twins, f"{label}: integer central fiber is exact")
    require(modular_fiber == twins, f"{label}: modular central fiber is exact")
    require(
        len(twins) == comb(len(values), len(values) // 2),
        f"{label}: exact twin-fiber size",
    )


def main():
    print("HEAVY-FIBER PLANTED-EMISSION HYPOTHESIS REPAIR")

    old_values = (3, 5, 6, 7)
    old_center = 15
    old_domain, old_integer_fiber = central_fiber_integer(old_values, old_center)
    _, old_modular_fiber = central_fiber_mod(old_values, old_center)
    old_twins = twin_unions(old_values, old_center)
    expected_extras = {(3, 8, 9, 10), (5, 6, 7, 12)}

    require(distinct_subset_sums(old_values), "P={3,5,6,7} is dissociated")
    require(old_center > 2 * max(old_values), "old condition c > 2 max(P) holds")
    require(len(old_domain) == 2 * len(old_values), "old example has 2B coordinates")
    require(len(old_integer_fiber) == 8, "old integer central fiber has eight supports")
    require(old_modular_fiber == old_integer_fiber, "old modular fiber has the same eight supports")
    require(len(old_twins) == comb(4, 2), "only six complete-pair unions exist")
    require(old_integer_fiber - old_twins == expected_extras, "the two extra supports are exact")

    structural_cases = (
        ((3, 5, 6, 7), 22),
        ((1, 2, 4, 8), 17),
        ((11, 17, 20, 22, 23, 24), 118),
    )
    for values, center in structural_cases:
        label = f"structural B={len(values)}, c={center}"
        require(distinct_subset_sums(values), f"{label}: P is dissociated")
        require(center > max(sum(values), 2 * max(values)), f"{label}: structural condition")
        check_exact_fiber(values, center, label)

    weak_values = (1, 2, 4, 8)
    weak_center = 17
    weak_image = image_mod(weak_values, weak_center)
    weak_w = comb(len(weak_values), len(weak_values) // 2)
    weak_m = comb(2 * len(weak_values), len(weak_values))
    require(
        weak_w * len(weak_image) < 2 * weak_m,
        "structural condition alone does not imply the finite heavy proxy",
    )
    print(
        "INFO: structural-only witness W*L/M = "
        f"{weak_w * len(weak_image)}/{weak_m}"
    )

    binary_values = tuple(2 ** index for index in range(8))
    binary_center = 2 * sum(binary_values) + 1
    require(distinct_subset_sums(binary_values), "binary family is dissociated")
    require(not two_dissociated(binary_values), "binary family is not 2-dissociated")
    binary_w = comb(len(binary_values), len(binary_values) // 2)
    binary_m = comb(2 * len(binary_values), len(binary_values))
    binary_upper_numerator = binary_w * binary_center
    require(
        binary_upper_numerator < 3 * binary_m,
        "B=8 binary strong-center instance has ratio below 3",
    )
    print(
        "INFO: B=8 binary instance L<=c gives W*L/M <= "
        f"{binary_upper_numerator}/{binary_m}"
    )

    wrapped_values = (1, 3)
    wrapped_center = 8
    require(two_dissociated(wrapped_values), "P={1,3} is 2-dissociated")
    require(
        wrapped_center > max(sum(wrapped_values), 2 * max(wrapped_values)),
        "P={1,3}, c=8 satisfies the structural center bound",
    )
    check_exact_fiber(wrapped_values, wrapped_center, "wrapped B=2, c=8")
    wrapped_image_size = len(image_mod(wrapped_values, wrapped_center))
    require(wrapped_image_size == 4, "wrapped B=2 image has size four")
    require(
        wrapped_image_size != (3 ** len(wrapped_values) + 1) // 2,
        "without c>2 sum(P), the exact image formula fails",
    )

    heavy_cases = tuple(
        tuple(5 ** index for index in range(size))
        for size in (2, 4, 6, 8)
    )
    for values in heavy_cases:
        center = 2 * sum(values) + 1
        label = f"heavy B={len(values)}, c={center}"
        require(distinct_subset_sums(values), f"{label}: P is dissociated")
        require(two_dissociated(values), f"{label}: P is 2-dissociated")
        require(center > 2 * sum(values), f"{label}: heavy-center condition")
        check_exact_fiber(values, center, label)
        image_size = len(image_mod(values, center))
        expected_image = (3 ** len(values) + 1) // 2
        require(image_size == expected_image, f"{label}: L=(3^B+1)/2")
        w = comb(len(values), len(values) // 2)
        m = comb(2 * len(values), len(values))
        print(f"INFO: {label}: W={w}, L={image_size}, M={m}, W*L/M={w * image_size}/{m}")

    print("OLD INTEGER/MODULAR CENTRAL FIBER:")
    for support in sorted(old_integer_fiber):
        print(" ", support)
    print("RESULT: PASS (old hypothesis refuted; structural and heavy repairs replayed)")


if __name__ == "__main__":
    main()
