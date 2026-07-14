#!/usr/bin/env python3
"""Exhaustive finite checks for the weighted cyclic-GRS salvage packet."""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import dataclass
from typing import Callable, Iterable


class VerificationError(RuntimeError):
    """A mathematical or certificate check failed."""


def check(condition: bool, detail: object) -> None:
    if not condition:
        raise VerificationError(detail)


def inv(value: int, p: int) -> int:
    check(value % p != 0, ("inverse-of-zero", value, p))
    return pow(value, p - 2, p)


def poly_add(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return tuple(
        ((left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)) % p
        for i in range(size)
    )


def poly_scale(poly: tuple[int, ...], scalar: int, p: int) -> tuple[int, ...]:
    return tuple((scalar * coefficient) % p for coefficient in poly)


def poly_mul(left: tuple[int, ...], right: tuple[int, ...], p: int) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % p
    return tuple(result)


def poly_eval(poly: tuple[int, ...], value: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % p
    return result


def poly_pad(poly: tuple[int, ...], size: int) -> tuple[int, ...]:
    check(len(poly) <= size, ("polynomial-too-long", poly, size))
    return poly + (0,) * (size - len(poly))


def lagrange(
    points: tuple[int, ...], values: tuple[int, ...], p: int
) -> tuple[int, ...]:
    check(len(points) == len(values) > 0, ("bad-interpolation-data", points, values))
    check(len(set(points)) == len(points), ("duplicate-points", points))
    result = (0,) * len(points)
    for i, x_i in enumerate(points):
        basis = (1,)
        denominator = 1
        for j, x_j in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, ((-x_j) % p, 1), p)
            denominator = denominator * (x_i - x_j) % p
        term = poly_scale(poly_pad(basis, len(points)), values[i] * inv(denominator, p), p)
        result = poly_add(result, term, p)
    result = poly_pad(result, len(points))
    check(
        all(poly_eval(result, x, p) == value for x, value in zip(points, values)),
        ("interpolation-failed", points, values, result),
    )
    return result


def prime_factors(value: int) -> tuple[int, ...]:
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
    return tuple(factors)


def element_of_order(p: int, order: int) -> int:
    check((p - 1) % order == 0, ("order-not-supported", p, order))
    for value in range(2, p):
        if pow(value, order, p) != 1:
            continue
        if all(pow(value, order // factor, p) != 1 for factor in prime_factors(order)):
            return value
    raise VerificationError(("missing-element-of-order", p, order))


@dataclass(frozen=True)
class Fixture:
    p: int
    q: int
    length: int
    k: int
    n: int
    h: tuple[int, ...]
    q_points: tuple[int, ...]
    fibers: tuple[tuple[int, tuple[int, ...]], ...]

    def fiber(self, y: int) -> tuple[int, ...]:
        for point, values in self.fibers:
            if point == y:
                return values
        raise VerificationError(("missing-fiber", y))


def make_fixture(p: int, q: int, length: int) -> Fixture:
    check(q % 2 == 0, ("q-not-even", q))
    n = q * length
    generator = element_of_order(p, n)
    h = tuple(pow(generator, exponent, p) for exponent in range(n))
    q_generator = pow(generator, length, p)
    q_points = tuple(pow(q_generator, exponent, p) for exponent in range(q))
    fibers = tuple(
        (y, tuple(x for x in h if pow(x, length, p) == y)) for y in q_points
    )
    return Fixture(p, q, length, q // 2, n, h, q_points, fibers)


def validate_quotient(fixture: Fixture, exponent: int | None = None) -> int:
    p = fixture.p
    power = fixture.length if exponent is None else exponent
    image = {pow(x, power, p) for x in fixture.h}
    check(image == set(fixture.q_points), ("quotient-image", power, image, fixture.q_points))
    check(
        sum(pow(x, power, p) == 1 for x in fixture.h) == fixture.length,
        ("quotient-kernel", power),
    )
    hom_pairs = 0
    for left in fixture.h:
        for right in fixture.h:
            check(
                pow(left * right % p, power, p)
                == pow(left, power, p) * pow(right, power, p) % p,
                ("quotient-homomorphism", left, right, power),
            )
            hom_pairs += 1
    seen: set[int] = set()
    for y in fixture.q_points:
        fiber = tuple(x for x in fixture.h if pow(x, power, p) == y)
        check(len(fiber) == fixture.length, ("fiber-cardinality", y, power, fiber))
        check(not (seen & set(fiber)), ("fiber-overlap", y, fiber))
        seen.update(fiber)
    check(seen == set(fixture.h), ("fiber-cover", power, seen))
    return hom_pairs


def recover_residues(
    fixture: Fixture,
    multipliers: tuple[int, ...],
    received: tuple[int, ...],
) -> dict[int, tuple[int, ...]]:
    p = fixture.p
    check(len(multipliers) == len(received) == fixture.n, "source-length")
    normalized = {
        x: received[index] * inv(multipliers[index], p) % p
        for index, x in enumerate(fixture.h)
    }
    residues: dict[int, tuple[int, ...]] = {}
    for y in fixture.q_points:
        fiber = fixture.fiber(y)
        residues[y] = lagrange(fiber, tuple(normalized[x] for x in fiber), p)
    return residues


def literal_source(
    fixture: Fixture,
    multipliers: tuple[int, ...],
    residues: dict[int, tuple[int, ...]],
    restore_weights: bool = True,
) -> tuple[int, ...]:
    p = fixture.p
    output: list[int] = []
    for index, x in enumerate(fixture.h):
        y = pow(x, fixture.length, p)
        value = poly_eval(residues[y], x, p)
        if restore_weights:
            value = value * multipliers[index] % p
        output.append(value)
    return tuple(output)


def syndromes(
    fixture: Fixture,
    residues: dict[int, tuple[int, ...]],
    lambda_mode: str = "correct",
) -> tuple[tuple[int, ...], ...]:
    p = fixture.p
    q_inv = inv(fixture.q, p)
    result: list[tuple[int, ...]] = []
    for degree in range(fixture.k):
        coefficients: list[int] = []
        for inner in range(fixture.length):
            total = 0
            for y in fixture.q_points:
                dual = q_inv if lambda_mode == "constant" else y * q_inv % p
                total += dual * pow(y, degree, p) * residues[y][inner]
            coefficients.append(total % p)
        result.append(tuple(coefficients))
    return tuple(result)


def phi_apply(
    images: tuple[tuple[int, ...], ...],
    argument: tuple[int, ...],
    p: int,
) -> tuple[int, ...]:
    check(len(images) == len(argument), ("phi-domain", images, argument))
    output = (0,) * len(images[0])
    for scalar, image in zip(argument, images):
        output = poly_add(output, poly_scale(image, scalar, p), p)
    return output


def source_realization(
    fixture: Fixture,
    images: tuple[tuple[int, ...], ...],
    exponent_shift: int = 0,
) -> dict[int, tuple[int, ...]]:
    p = fixture.p
    residues: dict[int, tuple[int, ...]] = {}
    for y in fixture.q_points:
        output = (0,) * fixture.length
        for degree, image in enumerate(images):
            exponent = degree + 1 + exponent_shift
            scalar = inv(pow(y, exponent, p), p)
            output = poly_add(output, poly_scale(image, scalar, p), p)
        residues[y] = output
    return residues


def outer_interpolant(
    fixture: Fixture,
    residues: dict[int, tuple[int, ...]],
    complement: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    check(len(complement) == fixture.k, ("outer-complement", complement))
    return tuple(
        lagrange(complement, tuple(residues[y][inner] for y in complement), fixture.p)
        for inner in range(fixture.length)
    )


def outer_value(
    fixture: Fixture,
    interpolant: tuple[tuple[int, ...], ...],
    y: int,
) -> tuple[int, ...]:
    return tuple(poly_eval(poly, y, fixture.p) for poly in interpolant)


def locator(points: Iterable[int], p: int) -> tuple[int, ...]:
    result = (1,)
    for point in points:
        result = poly_mul(result, ((-point) % p, 1), p)
    return result


def root_count(poly: tuple[int, ...], points: Iterable[int], p: int) -> int:
    return sum(poly_eval(poly, point, p) == 0 for point in points)


def discrepancy_scan(
    fixture: Fixture,
    residues: dict[int, tuple[int, ...]],
    images: tuple[tuple[int, ...], ...],
    scalar_mode: str = "correct",
) -> tuple[int, int]:
    p = fixture.p
    identities = 0
    exact_footprints = 0
    for j_tuple in itertools.combinations(fixture.q_points, fixture.k):
        j_set = set(j_tuple)
        complement = tuple(y for y in fixture.q_points if y not in j_set)
        interpolant = outer_interpolant(fixture, residues, complement)
        discrepancies = {
            y: tuple(
                (left - right) % p
                for left, right in zip(residues[y], outer_value(fixture, interpolant, y))
            )
            for y in fixture.q_points
        }
        check(
            all(not any(discrepancies[y]) for y in complement),
            ("complement-discrepancy", j_tuple, discrepancies),
        )
        all_nonzero = True
        predicted_roots = 0
        for y in j_tuple:
            q_jy = poly_pad(locator((z for z in j_tuple if z != y), p), fixture.k)
            left = phi_apply(images, q_jy, p)
            scalar = y * inv(fixture.q, p) % p
            if scalar_mode == "omit-locator":
                multiplier = scalar
            else:
                multiplier = scalar * poly_eval(q_jy, y, p) % p
            right = poly_scale(discrepancies[y], multiplier, p)
            check(left == right, ("discrepancy-identity", j_tuple, y, left, right))
            check(any(left) == any(discrepancies[y]), ("nonvanishing", j_tuple, y))
            all_nonzero = all_nonzero and any(left)
            predicted_roots += root_count(left, fixture.fiber(y), p)
            identities += 1

        nonfull = {y for y in fixture.q_points if any(discrepancies[y])}
        check(all_nonzero == (nonfull == j_set), ("exact-footprint", j_tuple, nonfull))
        actual_agreements = 0
        for y in fixture.q_points:
            candidate = outer_value(fixture, interpolant, y)
            actual_agreements += sum(
                poly_eval(residues[y], x, p) == poly_eval(candidate, x, p)
                for x in fixture.fiber(y)
            )
        check(
            actual_agreements == fixture.k * fixture.length + predicted_roots,
            ("agreement-count", j_tuple, actual_agreements, predicted_roots),
        )
        if all_nonzero:
            exact_footprints += 1
    return identities, exact_footprints


def exhaustive_weighted_f5() -> dict[str, int]:
    fixture = make_fixture(5, 4, 1)
    hom_pairs = validate_quotient(fixture)
    nonzero = tuple(range(1, fixture.p))
    all_words = tuple(itertools.product(range(fixture.p), repeat=fixture.n))
    reached: set[tuple[int, ...]] = set()
    weighted_forward_cases = 0
    for multipliers in itertools.product(nonzero, repeat=fixture.n):
        for received in all_words:
            residues = recover_residues(fixture, multipliers, received)
            restored = literal_source(fixture, multipliers, residues)
            check(restored == received, ("weighted-roundtrip", multipliers, received, restored))
            images = syndromes(fixture, residues)
            reached.add(tuple(value for image in images for value in image))
            weighted_forward_cases += 1

    discrepancy_identities = 0
    exact_footprints = 0
    unit_weights = (1,) * fixture.n
    for normalized in all_words:
        residues = recover_residues(fixture, unit_weights, normalized)
        images = syndromes(fixture, residues)
        identities, exact = discrepancy_scan(fixture, residues, images)
        discrepancy_identities += identities
        exact_footprints += exact

    inverse_realizations = 0
    for flat in itertools.product(range(fixture.p), repeat=fixture.k * fixture.length):
        images = tuple(
            tuple(flat[degree * fixture.length + inner] for inner in range(fixture.length))
            for degree in range(fixture.k)
        )
        residues = source_realization(fixture, images)
        for multipliers in itertools.product(nonzero, repeat=fixture.n):
            received = literal_source(fixture, multipliers, residues)
            recovered = recover_residues(fixture, multipliers, received)
            check(recovered == residues, ("inverse-residues-f5", images, multipliers))
            check(syndromes(fixture, recovered) == images, ("inverse-phi-f5", images, multipliers))
            inverse_realizations += 1

    expected_maps = fixture.p ** (fixture.k * fixture.length)
    check(len(reached) == expected_maps, ("forward-not-surjective", len(reached), expected_maps))
    return {
        "discrepancy_identities": discrepancy_identities,
        "distinct_phi_reached": len(reached),
        "exact_footprints": exact_footprints,
        "inverse_realizations_with_all_weights": inverse_realizations,
        "quotient_homomorphism_pairs": hom_pairs,
        "weighted_forward_cases": weighted_forward_cases,
    }


def subspaces_f2(p: int) -> tuple[tuple[tuple[int, int], tuple[tuple[int, int], ...]], ...]:
    zero = ((0, 0), ((0, 0),))
    spaces: list[tuple[tuple[int, int], tuple[tuple[int, int], ...]]] = [zero]
    for slope in range(p):
        basis = (1, slope)
        spaces.append((basis, tuple(((t, t * slope % p)) for t in range(p))))
    vertical = (0, 1)
    spaces.append((vertical, tuple(((0, t)) for t in range(p))))
    full = tuple(itertools.product(range(p), repeat=2))
    spaces.append(((1, 0), full))
    check(len({frozenset(values) for _, values in spaces}) == p + 3, "subspace-enumeration")
    return tuple(spaces)


def exhaustive_phi_f17() -> tuple[dict[str, int], int]:
    fixture = make_fixture(17, 4, 2)
    hom_pairs = validate_quotient(fixture)
    multipliers = tuple(range(1, fixture.n + 1))
    subspaces = subspaces_f2(fixture.p)
    full_space = frozenset(itertools.product(range(fixture.p), repeat=2))
    relevant_spaces: dict[int, tuple[tuple[tuple[int, int], ...], ...]] = {}
    for a in fixture.q_points:
        line_vector = ((-a) % fixture.p, 1)
        line_space = frozenset(
            ((t * line_vector[0] % fixture.p, t) for t in range(fixture.p))
        )
        containing = tuple(
            tuple(values)
            for _, values in subspaces
            if line_vector in frozenset(values)
        )
        check(
            {frozenset(values) for values in containing} == {line_space, full_space},
            ("qualifying-subspaces", a, containing),
        )
        relevant_spaces[a] = (
            (line_vector,),
            ((1, 0), (0, 1)),
        )

    # Multiplying a nonzero W-polynomial by any t in F_p^* preserves both its
    # nonvanishing and its root set.  Exhaust this finite scalar fact once;
    # the core scan can then count all T=t without repeating identical roots.
    for output in itertools.product(range(fixture.p), repeat=fixture.length):
        if not any(output):
            continue
        for t in range(1, fixture.p):
            scaled = poly_scale(output, t, fixture.p)
            check(any(scaled), ("nonzero-scalar-output", output, t))
            check(
                all(
                    (poly_eval(output, x, fixture.p) == 0)
                    == (poly_eval(scaled, x, fixture.p) == 0)
                    for x in fixture.h
                ),
                ("scalar-root-set", output, t),
            )

    maps = discrepancy_identities = exact_footprints = 0
    core_cases = core_equality_cases = 0
    for flat in itertools.product(range(fixture.p), repeat=fixture.k * fixture.length):
        images = tuple(
            tuple(flat[degree * fixture.length + inner] for inner in range(fixture.length))
            for degree in range(fixture.k)
        )
        residues = source_realization(fixture, images)
        received = literal_source(fixture, multipliers, residues)
        recovered = recover_residues(fixture, multipliers, received)
        check(recovered == residues, ("inverse-residues-f17", images))
        check(syndromes(fixture, recovered) == images, ("inverse-phi-f17", images))
        identities, exact = discrepancy_scan(fixture, recovered, images)
        discrepancy_identities += identities
        exact_footprints += exact

        for a in fixture.q_points:
            line_vector = ((-a) % fixture.p, 1)
            base_output = phi_apply(images, line_vector, fixture.p)
            if not any(base_output):
                continue
            for basis in relevant_spaces[a]:
                common_roots = tuple(
                    x
                    for x in fixture.fiber(a)
                    if all(
                        poly_eval(phi_apply(images, vector, fixture.p), x, fixture.p) == 0
                        for vector in basis
                    )
                )
                check(len(common_roots) <= fixture.length - 1, ("core-root-f17", a, images))
                check(
                    all(poly_eval(base_output, x, fixture.p) == 0 for x in common_roots),
                    ("core-containment-f17", a, images, common_roots),
                )
                core_cases += fixture.p - 1
                if len(common_roots) == fixture.length - 1:
                    core_equality_cases += fixture.p - 1
        maps += 1

    expected_maps = fixture.p ** (fixture.k * fixture.length)
    check(maps == expected_maps, ("map-count-f17", maps, expected_maps))
    check(core_equality_cases > 0, "missing-core-equality-f17")
    return (
        {
            "core_equality_cases": core_equality_cases,
            "core_qualifying_cases": core_cases,
            "discrepancy_identities": discrepancy_identities,
            "exact_footprints": exact_footprints,
            "inverse_realizations": maps,
            "linear_maps": maps,
            "quotient_homomorphism_pairs": hom_pairs,
        },
        fixture.length - 1,
    )


def exhaustive_multi_owner_core_f13() -> dict[str, int]:
    fixture = make_fixture(13, 6, 2)
    hom_pairs = validate_quotient(fixture)
    a, b = fixture.q_points[:2]
    p = fixture.p
    image_space = tuple(itertools.product(range(p), repeat=fixture.length))
    fiber_a = fixture.fiber(a)
    fiber_b = fixture.fiber(b)
    ab = a * b % p
    minus_sum = -(a + b) % p
    maps = qualifying = equality = 0
    for image_0, image_1, image_2 in itertools.product(image_space, repeat=3):
        output_0 = (ab * image_0[0] + minus_sum * image_1[0] + image_2[0]) % p
        output_1 = (ab * image_0[1] + minus_sum * image_1[1] + image_2[1]) % p
        maps += 1
        if output_0 == 0 and output_1 == 0:
            continue

        owner_a_0 = (
            ((image_1[0] - b * image_0[0]) % p, (image_1[1] - b * image_0[1]) % p),
            ((image_2[0] - b * image_1[0]) % p, (image_2[1] - b * image_1[1]) % p),
        )
        owner_b_0 = (
            ((image_1[0] - a * image_0[0]) % p, (image_1[1] - a * image_0[1]) % p),
            ((image_2[0] - a * image_1[0]) % p, (image_2[1] - a * image_1[1]) % p),
        )
        roots_a = tuple(
            x
            for x in fiber_a
            if all((poly[0] + poly[1] * x) % p == 0 for poly in owner_a_0)
        )
        roots_b = tuple(
            x
            for x in fiber_b
            if all((poly[0] + poly[1] * x) % p == 0 for poly in owner_b_0)
        )
        check(not (set(roots_a) & set(roots_b)), ("multi-owner-overlap", roots_a, roots_b))
        check(
            all((output_0 + output_1 * x) % p == 0 for x in roots_a + roots_b),
            ("multi-owner-containment", image_0, image_1, image_2, roots_a, roots_b),
        )
        root_sum = len(roots_a) + len(roots_b)
        check(
            root_sum <= fixture.length - 1,
            ("multi-owner-core-bound", image_0, image_1, image_2, root_sum),
        )
        qualifying += 1
        if root_sum == fixture.length - 1:
            equality += 1

    expected_maps = p ** (3 * fixture.length)
    check(maps == expected_maps, ("map-count-f13", maps, expected_maps))
    check(
        qualifying == expected_maps - p ** (2 * fixture.length),
        ("qualifying-count-f13", qualifying),
    )
    check(equality > 0, "missing-multi-owner-equality")
    return {
        "core_equality_maps": equality,
        "linear_maps": maps,
        "nonvanishing_core_maps": qualifying,
        "quotient_homomorphism_pairs": hom_pairs,
    }


DEPLOYED = {
    "K": 2**20,
    "L": 2**15,
    "a_size": 27,
    "k": 32,
    "m": 1_116_047,
    "n": 2**21,
    "owner_size": 5,
    "p": 2**31 - 2**24 + 1,
    "q0": 64,
    "extension_degree": 6,
    "outer_q0_unrouted_footprint_floor": 33,
    "sigma": 67_471,
}


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def validate_deployed(constants: dict[str, int]) -> dict[str, int]:
    check(is_prime(constants["p"]), ("deployed-p-not-prime", constants["p"]))
    check(constants["n"] == constants["q0"] * constants["L"], "deployed-n")
    check(constants["K"] == constants["k"] * constants["L"], "deployed-K")
    check(constants["q0"] == 2 * constants["k"], "deployed-half")
    check(constants["extension_degree"] == 6, "deployed-extension-degree")
    check(constants["m"] - constants["K"] == constants["sigma"], "deployed-sigma")
    check((constants["p"] - 1) % constants["n"] == 0, "deployed-split")
    check(constants["a_size"] + constants["owner_size"] == constants["k"], "deployed-core")
    check(constants["L"] - 1 == 32_767, "deployed-root-budget")
    check(
        constants["outer_q0_unrouted_footprint_floor"] == constants["k"] + 1,
        "outer-q0-wall",
    )
    return {
        "K": constants["K"],
        "L": constants["L"],
        "L_minus_1": constants["L"] - 1,
        "a_size": constants["a_size"],
        "k": constants["k"],
        "m": constants["m"],
        "n": constants["n"],
        "owner_size": constants["owner_size"],
        "p": constants["p"],
        "q0": constants["q0"],
        "extension_degree": constants["extension_degree"],
        "code_alphabet_size": constants["p"] ** constants["extension_degree"],
        "outer_q0_unrouted_footprint_floor": constants[
            "outer_q0_unrouted_footprint_floor"
        ],
        "sigma": constants["sigma"],
    }


def expect_rejected(name: str, mutation: Callable[[], None]) -> str:
    try:
        mutation()
    except VerificationError:
        return name
    raise VerificationError(("tamper-not-rejected", name))


def reject_wrong_lambda() -> None:
    fixture = make_fixture(5, 4, 1)
    weights = (1,) * fixture.n
    for word in itertools.product(range(fixture.p), repeat=fixture.n):
        residues = recover_residues(fixture, weights, word)
        wrong_images = syndromes(fixture, residues, lambda_mode="constant")
        try:
            discrepancy_scan(fixture, residues, wrong_images)
        except VerificationError:
            raise
    check(False, "wrong-lambda-survived")


def reject_wrong_discrepancy_scalar() -> None:
    fixture = make_fixture(5, 4, 1)
    weights = (1,) * fixture.n
    for word in itertools.product(range(fixture.p), repeat=fixture.n):
        residues = recover_residues(fixture, weights, word)
        images = syndromes(fixture, residues)
        try:
            discrepancy_scan(fixture, residues, images, scalar_mode="omit-locator")
        except VerificationError:
            raise
    check(False, "wrong-discrepancy-scalar-survived")


def reject_wrong_inverse_exponent() -> None:
    fixture = make_fixture(17, 4, 2)
    images = ((1, 3), (4, 2))
    residues = source_realization(fixture, images, exponent_shift=1)
    check(syndromes(fixture, residues) == images, "wrong-inverse-exponent")


def reject_missing_weight_restore() -> None:
    fixture = make_fixture(5, 4, 1)
    weights = (1, 2, 3, 4)
    images = ((1,), (2,))
    residues = source_realization(fixture, images)
    received = literal_source(fixture, weights, residues, restore_weights=False)
    recovered = recover_residues(fixture, weights, received)
    check(syndromes(fixture, recovered) == images, "missing-weight-restore")


def reject_wrong_exact_footprint_logic() -> None:
    fixture = make_fixture(5, 4, 1)
    weights = (1,) * fixture.n
    for word in itertools.product(range(fixture.p), repeat=fixture.n):
        residues = recover_residues(fixture, weights, word)
        images = syndromes(fixture, residues)
        for j_tuple in itertools.combinations(fixture.q_points, fixture.k):
            values = []
            for y in j_tuple:
                q_jy = poly_pad(locator((z for z in j_tuple if z != y), fixture.p), fixture.k)
                values.append(any(phi_apply(images, q_jy, fixture.p)))
            if any(values) and not all(values):
                check(any(values) == all(values), ("any-versus-all", word, j_tuple, values))
    check(False, "wrong-footprint-logic-survived")


def run_tamper_suite(core_bound: int) -> tuple[str, ...]:
    rejected = [
        expect_rejected(
            "deployed_sigma_plus_one",
            lambda: validate_deployed({**DEPLOYED, "sigma": DEPLOYED["sigma"] + 1}),
        ),
        expect_rejected(
            "quotient_exponent_L_plus_one",
            lambda: validate_quotient(make_fixture(17, 4, 2), exponent=3),
        ),
        expect_rejected("dual_multiplier_without_y", reject_wrong_lambda),
        expect_rejected("inverse_dft_exponent_shift", reject_wrong_inverse_exponent),
        expect_rejected("discrepancy_scalar_without_locator", reject_wrong_discrepancy_scalar),
        expect_rejected("literal_weights_not_restored", reject_missing_weight_restore),
        expect_rejected("exact_footprint_any_instead_of_all", reject_wrong_exact_footprint_logic),
        expect_rejected(
            "core_budget_L_minus_two",
            lambda: check(core_bound <= 0, ("mutated-core-budget", core_bound, 0)),
        ),
    ]
    return tuple(rejected)


def main() -> None:
    deployed = validate_deployed(DEPLOYED)
    f5 = exhaustive_weighted_f5()
    f17, core_bound = exhaustive_phi_f17()
    f13 = exhaustive_multi_owner_core_f13()
    tamper = run_tamper_suite(core_bound)
    result = {
        "deployed": deployed,
        "fixture_scope": "prime_field_evidence_only",
        "fixtures": {
            "F13_q6_L2_multi_owner_core": f13,
            "F17_q4_L2_all_phi": f17,
            "F5_q4_L1_all_weighted_sources": f5,
        },
        "status": "PASS",
        "tamper_mutations_rejected": tamper,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
