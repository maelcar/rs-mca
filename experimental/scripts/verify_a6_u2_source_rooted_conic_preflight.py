#!/usr/bin/env python3
"""Deterministic verifier for the experimental source-rooted conic preflight."""

from __future__ import annotations

import argparse
import ast
import hashlib
import itertools
import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence


P = 101
U = tuple(range(10))
SELF = Path(__file__).resolve()
ROOT = SELF.parents[2]
NOTE = ROOT / "experimental/notes/thresholds/a6_u2_source_rooted_conic_preflight.md"
TAMPERS = (
    "sign",
    "source",
    "divisor",
    "operator",
    "base",
    "probe",
    "denominator",
    "stress",
    "note_marker",
)


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def inv(value: int) -> int:
    value %= P
    require(value != 0, "inverse of zero")
    return pow(value, -1, P)


def trim(poly: Sequence[int]) -> list[int]:
    result = [value % P for value in poly] or [0]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def zero(poly: Sequence[int]) -> bool:
    return all(value % P == 0 for value in poly)


def deg(poly: Sequence[int]) -> int:
    clean = trim(poly)
    return -1 if zero(clean) else len(clean) - 1


def add(left: Sequence[int], right: Sequence[int]) -> list[int]:
    size = max(len(left), len(right))
    return trim(
        [
            ((left[i] if i < len(left) else 0)
             + (right[i] if i < len(right) else 0))
            % P
            for i in range(size)
        ]
    )


def scale(poly: Sequence[int], scalar: int) -> list[int]:
    return trim([scalar * value % P for value in poly])


def neg(poly: Sequence[int]) -> list[int]:
    return scale(poly, -1)


def sub(left: Sequence[int], right: Sequence[int]) -> list[int]:
    return add(left, neg(right))


def mul(left: Sequence[int], right: Sequence[int]) -> list[int]:
    if zero(left) or zero(right):
        return [0]
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % P
    return trim(result)


def evaluate(poly: Sequence[int], point: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * point + coefficient) % P
    return value


def divmod_poly(
    numerator: Sequence[int], denominator: Sequence[int]
) -> tuple[list[int], list[int]]:
    num = trim(numerator)
    den = trim(denominator)
    require(not zero(den), "division by zero polynomial")
    if deg(num) < deg(den):
        return [0], num
    quotient = [0] * (deg(num) - deg(den) + 1)
    inverse_lead = inv(den[-1])
    while not zero(num) and deg(num) >= deg(den):
        shift = deg(num) - deg(den)
        coefficient = num[-1] * inverse_lead % P
        quotient[shift] = coefficient
        num = sub(num, [0] * shift + scale(den, coefficient))
    return trim(quotient), trim(num)


def exact_div(
    numerator: Sequence[int], denominator: Sequence[int]
) -> list[int]:
    quotient, remainder = divmod_poly(numerator, denominator)
    require(zero(remainder), "claimed divisor leaves a remainder")
    return quotient


def monic(poly: Sequence[int]) -> list[int]:
    clean = trim(poly)
    return [0] if zero(clean) else scale(clean, inv(clean[-1]))


def gcd_poly(left: Sequence[int], right: Sequence[int]) -> list[int]:
    a, b = trim(left), trim(right)
    while not zero(b):
        _, remainder = divmod_poly(a, b)
        a, b = b, remainder
    return monic(a)


def gcd_all(polynomials: Iterable[Sequence[int]]) -> list[int]:
    iterator = iter(polynomials)
    try:
        result = trim(next(iterator))
    except StopIteration:
        return [0]
    for polynomial in iterator:
        result = gcd_poly(result, polynomial)
    return monic(result)


def from_roots(roots: Iterable[int]) -> list[int]:
    result = [1]
    for root in roots:
        result = mul(result, [(-root) % P, 1])
    return result


def det_poly(matrix: Sequence[Sequence[Sequence[int]]]) -> list[int]:
    size = len(matrix)
    require(size > 0, "empty determinant")
    require(all(len(row) == size for row in matrix), "nonsquare matrix")
    result = [0]
    for permutation in itertools.permutations(range(size)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = [1]
        for row, column in enumerate(permutation):
            term = mul(term, matrix[row][column])
        result = add(result, term if inversions % 2 == 0 else neg(term))
    return result


def rank_mod(matrix: Sequence[Sequence[int]]) -> int:
    if not matrix:
        return 0
    work = [[value % P for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        work[rank] = [
            value * inv(work[rank][column]) % P
            for value in work[rank]
        ]
        for row in range(len(work)):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % P
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def dot(left: Sequence[int], right: Sequence[int]) -> int:
    return sum(a * b for a, b in zip(left, right)) % P


def lagrange(
    slopes: Sequence[int], polynomials: Sequence[Sequence[int]]
) -> list[list[int]]:
    require(len(slopes) == len(polynomials) == 5, "five inputs required")
    output = [[0] for _ in range(5)]
    for i, slope in enumerate(slopes):
        basis, denominator = [1], 1
        for j, other in enumerate(slopes):
            if i == j:
                continue
            basis = mul(basis, [(-other) % P, 1])
            denominator = denominator * (slope - other) % P
        basis = scale(basis, inv(denominator))
        for y_degree, coefficient in enumerate(basis):
            output[y_degree] = add(
                output[y_degree], scale(polynomials[i], coefficient)
            )
    return [trim(poly) for poly in output]


def delta_of(
    slopes: Sequence[int], polynomials: Sequence[Sequence[int]]
) -> list[int]:
    coefficients = lagrange(slopes, polynomials)
    g2, g3, g4 = coefficients[2], coefficients[3], coefficients[4]
    s1 = sum(slopes) % P
    s2 = sum(a * b for a, b in itertools.combinations(slopes, 2)) % P
    result = sub(mul(g2, g4), mul(g3, g3))
    result = sub(result, scale(mul(g3, g4), s1))
    return sub(result, scale(mul(g4, g4), s2))


def conic_rhs(
    slopes: Sequence[int], locators: Sequence[Sequence[int]]
) -> list[int]:
    row_vandermondes = [
        math.prod(
            (slopes[i] - slopes[j]) % P
            for j in range(5)
            if i != j
        )
        % P
        for i in range(5)
    ]
    result = [0]
    for i, j in itertools.combinations(range(5), 2):
        coefficient = (
            (slopes[i] - slopes[j]) ** 2
            * inv(row_vandermondes[i])
            * inv(row_vandermondes[j])
        ) % P
        result = add(result, scale(mul(locators[i], locators[j]), coefficient))
    return result


def graph_det(
    slopes: Sequence[int], polynomials: Sequence[Sequence[int]]
) -> list[int]:
    rows = []
    for slope, polynomial in zip(slopes, polynomials):
        rows.append(
            [
                [1],
                [slope],
                [slope * slope % P],
                trim(polynomial),
                scale(polynomial, slope),
            ]
        )
    return det_poly(rows)


def vandermonde(slopes: Sequence[int]) -> int:
    result = 1
    for i, j in itertools.combinations(range(len(slopes)), 2):
        result = result * (slopes[j] - slopes[i]) % P
    return result


def relation_rows(
    slopes: Sequence[int], masks: Sequence[set[int]]
) -> tuple[list[list[int]], int]:
    rows: list[list[int]] = []
    predicted = 0
    for point in U:
        incidence = [i for i, mask in enumerate(masks) if point in mask]
        predicted += max(len(incidence) - 2, 0)
        if len(incidence) < 3:
            continue
        first, second = incidence[:2]
        for third in incidence[2:]:
            relation = [0] * 5
            relation[first] = slopes[second] - slopes[third]
            relation[second] = slopes[third] - slopes[first]
            relation[third] = slopes[first] - slopes[second]
            relation = [value % P for value in relation]
            require(sum(relation) % P == 0, "bad relation constant moment")
            require(
                sum(a * b for a, b in zip(relation, slopes)) % P == 0,
                "bad relation slope moment",
            )
            powers = [pow(point, exponent, P) for exponent in range(5)]
            rows.append(
                [
                    coefficient * power % P
                    for coefficient in relation
                    for power in powers
                ]
            )
    require(len(rows) == predicted, "operator row count mismatch")
    return rows, predicted


def build_seed() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for support_tuple in itertools.combinations(U, 3):
        if sum(support_tuple) != 14:
            continue
        support = set(support_tuple)
        mask = set(U) - support
        locator = from_roots(sorted(mask))
        require(deg(locator) == 7 and locator[7] == 1, "bad locator degree")
        require(locator[6] == (-31) % P, "bad fixed first prefix")
        slope = locator[5]
        approximation = trim(locator[:5])
        source = [0, 0, 0, 0, 0, slope, (-31) % P, 1]
        require(locator == add(source, approximation), "bad source decomposition")
        items.append(
            {
                "slope": slope,
                "support": support,
                "mask": mask,
                "locator": locator,
                "f": approximation,
            }
        )
    expected = {
        88: (0, 5, 9),
        85: (0, 6, 8),
        84: (1, 4, 9),
        80: (1, 5, 8),
        78: (1, 6, 7),
        82: (2, 3, 9),
        77: (2, 4, 8),
        74: (2, 5, 7),
        72: (3, 4, 7),
        70: (3, 5, 6),
    }
    require(len(items) == 10, "wrong fixed-sum family size")
    require(
        {int(item["slope"]): tuple(sorted(item["support"])) for item in items}
        == expected,
        "support/slope table changed",
    )
    prefix = []
    for mask_tuple in itertools.combinations(U, 7):
        locator = from_roots(mask_tuple)
        if locator[6] == (-31) % P:
            prefix.append((mask_tuple, locator[5]))
    require(len(prefix) == 10, "prefix fiber is not exhaustive")
    require(len({slope for _, slope in prefix}) == 10, "colors are not singleton")
    direction_witness = from_roots(range(5))
    require(deg(direction_witness) == 5, "direction witness degree changed")
    direction_roots = {
        point for point in U if evaluate(direction_witness, point) == 0
    }
    require(direction_roots == set(range(5)), "direction witness roots changed")
    require(
        len(U) - len(direction_roots) == 5,
        "direction witness does not attain weight five",
    )
    return items


def verify_five_cases(
    items: Sequence[dict[str, object]], tamper: str | None
) -> dict[str, object]:
    degree_counts: Counter[int] = Counter()
    root_counts: Counter[int] = Counter()
    operator_ranks: Counter[int] = Counter()
    operator_rows: Counter[int] = Counter()
    exact_two_counts: Counter[int] = Counter()
    count = 0
    for index, chosen in enumerate(itertools.combinations(items, 5)):
        slopes = [int(item["slope"]) for item in chosen]
        values = [list(item["f"]) for item in chosen]
        locators = [list(item["locator"]) for item in chosen]
        supports = [set(item["support"]) for item in chosen]
        masks = [set(item["mask"]) for item in chosen]
        delta = delta_of(slopes, values)
        if tamper == "sign" and index == 0:
            delta = add(delta, [1])
        rhs_locators = [poly[:] for poly in locators]
        if tamper == "source" and index == 0:
            rhs_locators[0] = add(rhs_locators[0], [1])
        require(delta == conic_rhs(slopes, rhs_locators), "conic identity failed")
        require(
            graph_det(slopes, values) == scale(delta, -vandermonde(slopes)),
            "determinant identity failed",
        )
        require(not zero(delta), "unexpected zero Delta")

        multiplicities = [
            sum(point in support for support in supports) for point in U
        ]
        roots_zero = [
            point for point, multiplicity in zip(U, multiplicities)
            if multiplicity == 0
        ]
        roots_one = [
            point for point, multiplicity in zip(U, multiplicities)
            if multiplicity == 1
        ]
        divisor = mul(
            mul(from_roots(roots_zero), from_roots(roots_zero)),
            from_roots(roots_one),
        )
        if tamper == "divisor" and index == 0:
            extra = next(
                point for point, multiplicity in zip(U, multiplicities)
                if multiplicity == 2
            )
            divisor = mul(divisor, [(-extra) % P, 1])
        exact_div(delta, divisor)
        require(
            2 * len(roots_zero) + len(roots_one)
            >= 2 * len(U) - sum(len(support) for support in supports),
            "divisor lower bound failed",
        )
        for point, multiplicity in zip(U, multiplicities):
            value = evaluate(delta, point)
            if multiplicity == 2:
                require(value != 0, "Delta vanishes at exact-two support")
            if value != 0:
                require(multiplicity >= 2, "Delta leaves collision support")
        roots = sum(evaluate(delta, point) == 0 for point in U)
        require(len(U) - roots >= len(U) - deg(delta), "RS distance failed")
        degree_counts[deg(delta)] += 1
        root_counts[roots] += 1
        exact_two_counts[multiplicities.count(2)] += 1

        rows, row_count = relation_rows(slopes, masks)
        vector = [
            coefficient
            for polynomial in values
            for coefficient in polynomial + [0] * (5 - len(polynomial))
        ]
        if tamper == "operator" and index == 0:
            rows[0][0] = (rows[0][0] + 1) % P
        require(
            all(dot(row, vector) == 0 for row in rows),
            "actual tuple left the U_(2,5) kernel",
        )
        rank = rank_mod(rows)
        require(rank < 15, "operator unexpectedly full rank")
        operator_ranks[rank] += 1
        operator_rows[row_count] += 1
        count += 1

    require(count == 252, "five-subset census changed")
    require(degree_counts == Counter({8: 245, 7: 7}), "degree census changed")
    require(
        root_counts == Counter({3: 7, 4: 58, 5: 112, 6: 66, 7: 9}),
        "root census changed",
    )
    require(
        operator_ranks == Counter({13: 1, 14: 251}),
        "operator rank census changed",
    )
    require(
        operator_rows == Counter({15: 246, 16: 6}),
        "operator row census changed",
    )
    require(
        exact_two_counts
        == Counter({1: 6, 2: 30, 3: 44, 4: 85, 5: 51, 6: 29, 7: 7}),
        "exact-two census changed",
    )
    return {
        "five_subsets": count,
        "delta_degrees": dict(sorted(degree_counts.items())),
        "delta_roots": dict(sorted(root_counts.items())),
        "operator_ranks": dict(sorted(operator_ranks.items())),
        "operator_rows": dict(sorted(operator_rows.items())),
    }


def cofactors_four(
    slopes: Sequence[int], values: Sequence[Sequence[int]]
) -> list[list[int]]:
    rows = [
        [
            [1],
            [slope],
            [slope * slope % P],
            trim(polynomial),
            scale(polynomial, slope),
        ]
        for slope, polynomial in zip(slopes, values)
    ]
    output = []
    for omitted in range(5):
        minor = [
            [entry for column, entry in enumerate(row) if column != omitted]
            for row in rows
        ]
        value = det_poly(minor)
        output.append(value if omitted % 2 == 0 else neg(value))
    for row in rows:
        relation = [0]
        for coefficient, entry in zip(output, row):
            relation = add(relation, mul(coefficient, entry))
        require(zero(relation), "cofactor misses base row")
    return output


def verify_fixed_base(
    items: Sequence[dict[str, object]], tamper: str | None
) -> dict[str, object]:
    by_slope = {int(item["slope"]): item for item in items}
    base_slopes = [88, 85, 80, 78]
    moving_slopes = [84, 82, 77, 74, 72, 70]
    base = [by_slope[slope] for slope in base_slopes]
    raw = cofactors_four(base_slopes, [list(item["f"]) for item in base])
    require(
        tuple(deg(poly) for poly in raw) == (8, 8, 8, 4, 4),
        "raw cofactor degrees changed",
    )
    common_zeros = set.intersection(*(set(item["mask"]) for item in base))
    if tamper == "base":
        common_zeros.add(0)
    require(common_zeros == {2, 3, 4}, "base divisor changed")
    base_divisor = from_roots(sorted(common_zeros))
    for polynomial in raw:
        exact_div(polynomial, base_divisor)
    full_gcd = gcd_poly(raw[3], raw[4])
    require(full_gcd == monic(base_divisor), "full cofactor gcd changed")
    for polynomial in raw:
        exact_div(polynomial, full_gcd)
    primitive = [exact_div(poly, full_gcd) for poly in raw]
    require(
        tuple(deg(poly) for poly in primitive) == (5, 5, 5, 1, 1),
        "primitive cofactor degrees changed",
    )
    require(deg(gcd_all(primitive)) == 0, "cofactor vector not primitive")
    if tamper == "denominator":
        primitive[3] = add(primitive[3], [1])

    support_multiplicity = {
        point: sum(point in set(item["support"]) for item in base)
        for point in U
    }
    probe = {
        point for point, multiplicity in support_multiplicity.items()
        if multiplicity == 1
    }
    if tamper == "probe":
        probe.add(0)
    require(probe == {7, 9}, "probe changed")
    probe_owner = {
        point: next(
            int(item["slope"])
            for item in base
            if point in set(item["support"])
        )
        for point in probe
    }
    require(
        all(evaluate(full_gcd, point) != 0 for point in probe),
        "cofactor gcd meets probe",
    )

    multiplier_roots: dict[int, tuple[int, ...]] = {}
    probe_scalars: dict[tuple[int, int], int] = {}
    support_hits: dict[int, tuple[int, ...]] = {}
    for slope in moving_slopes:
        item = by_slope[slope]
        row = [
            [1],
            [slope],
            [slope * slope % P],
            list(item["f"]),
            scale(list(item["f"]), slope),
        ]
        raw_e, primitive_e = [0], [0]
        for raw_cofactor, primitive_cofactor, entry in zip(raw, primitive, row):
            raw_e = add(raw_e, mul(raw_cofactor, entry))
            primitive_e = add(
                primitive_e, mul(primitive_cofactor, entry)
            )
        require(not zero(raw_e), "moving determinant vanished")
        require(raw_e == mul(full_gcd, primitive_e), "gcd division changed E")
        require(
            raw_e
            == graph_det(
                base_slopes + [slope],
                [list(base_item["f"]) for base_item in base] + [list(item["f"])],
            ),
            "fixed-base cofactor expansion changed",
        )
        multiplier = add(primitive[3], scale(primitive[4], slope))
        multiplier_roots[slope] = tuple(
            point for point in U if evaluate(multiplier, point) == 0
        )
        for point in probe:
            owner_slope = probe_owner[point]
            owner = by_slope[owner_slope]
            left = evaluate(primitive_e, point)
            moving_value = evaluate(list(item["locator"]), point)
            owner_value = evaluate(list(owner["locator"]), point)
            require(
                (left == 0) == (moving_value == 0),
                "probe misses actual moving zero pattern",
            )
            if moving_value != 0:
                denominator = (
                    (owner_slope - slope) * owner_value * moving_value
                ) % P
                ratio = left * inv(denominator) % P
                key = (owner_slope, point)
                if key in probe_scalars:
                    require(
                        probe_scalars[key] == ratio,
                        "probe scalar depends on moving slope",
                    )
                probe_scalars[key] = ratio
        hit = tuple(sorted(set(item["support"]) & common_zeros))
        support_hits[slope] = hit
        require(bool(hit), "moving support misses base divisor")
        require(
            not common_zeros <= set(item["mask"]),
            "moving locator contains full base divisor",
        )

    require(
        multiplier_roots
        == {84: (), 82: (3,), 77: (), 74: (), 72: (), 70: ()},
        "multiplier-root census changed",
    )
    require(
        support_hits
        == {
            84: (4,),
            82: (2, 3),
            77: (2, 4),
            74: (2,),
            72: (3, 4),
            70: (3,),
        },
        "moving support/base-divisor incidence changed",
    )
    augmented = [
        [1, int(item["slope"])]
        + list(reversed(list(item["f"])))
        for item in items
    ]
    augmented_rank = rank_mod(augmented)
    require(augmented_rank == 7, "selector augmented rank changed")
    return {
        "base_divisor": sorted(common_zeros),
        "probe": sorted(probe),
        "raw_degrees": [deg(poly) for poly in raw],
        "primitive_degrees": [deg(poly) for poly in primitive],
        "multiplier_roots": {
            str(slope): list(roots)
            for slope, roots in multiplier_roots.items()
        },
        "core_rank": augmented_rank - 2,
    }


def verify_stress(tamper: str | None) -> dict[str, object]:
    report = []
    for u in (1, 2, 7, 19):
        n, r, kappa, t, d = 500 * u, 275 * u, 225 * u, 150 * u, 250 * u
        require(n == r + kappa, "stress dimension split changed")
        require(2 * kappa - 1 <= n, "collision RS distance is unavailable")
        distance = n - 2 * kappa + 2
        expected = 50 * u + 2
        if tamper == "stress" and u == 1:
            expected += 1
        require(distance == expected, "stress collision distance changed")
        divisor_lower = 2 * n - 5 * t
        require(divisor_lower == 250 * u, "stress divisor lower bound changed")
        require(
            2 * kappa - 2 - divisor_lower == 200 * u - 2,
            "stress residual factor degree changed",
        )
        require(
            math.ceil(divisor_lower / 5) == 50 * u,
            "four-locator gcd lower bound changed",
        )
        for g in (0, 1, 50 * u, kappa - 1):
            length = n - g
            dimension = 2 * kappa - 1 - g
            require(
                length - dimension + 1 == distance,
                "shortening changed designed distance",
            )
        for g in range(50 * u, kappa):
            a_max = n - g
            d0 = 2 * kappa - 2 - g
            left = 11 * (d0 * a_max - (a_max - t) ** 2)
            right = (1850 * u - 22) * a_max
            require(left >= right, "residual Johnson gap bound changed")
        for probe_size in range(t, n + 1):
            require(
                (probe_size - t) ** 2 - (n - d) * probe_size <= 0,
                "pairwise probe Johnson denominator became positive",
            )
        require(
            n * (n - d) - (n - t) ** 2 == 2500 * u * u,
            "full-mask five-u miss changed",
        )
        report.append(
            {
                "u": u,
                "distance": distance,
                "divisor_lower": divisor_lower,
                "pairwise_gap_square": 2500 * u * u,
            }
        )
    return {"stress": report}


def verify_note(tamper: str | None) -> dict[str, object]:
    require(NOTE.is_file(), "companion note missing")
    text = NOTE.read_text(encoding="utf-8")
    markers = [
        "The symmetric direct-quartic invariant",
        "source-rooted conic identity",
        "Hereditary conic vanishing is polynomially paid",
        "The exact four-block probe",
        "counterguard",
        "No literature novelty is asserted",
        "2kappa-1<=N",
    ]
    if tamper == "note_marker":
        markers.append("THIS MARKER MUST NOT EXIST")
    for marker in markers:
        require(marker in text, f"note marker missing: {marker}")
    require(text.count("```") % 2 == 0, "unbalanced note fences")
    require("\t" not in text, "note contains tabs")
    require(
        all(line == line.rstrip() for line in text.splitlines()),
        "note has trailing whitespace",
    )
    forbidden_terms = (
        "clau" + "de.ai",
        "anth" + "ropic",
        "ses" + "sion",
        "scratch" + "pad",
        "/" + "tmp/clau" + "de",
        "Co-" + "Authored",
        "Generated" + " with",
    )
    folded = text.casefold()
    require(
        all(term.casefold() not in folded for term in forbidden_terms),
        "note contains forbidden provenance leak",
    )
    return {
        "note_lines": len(text.splitlines()),
        "note_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


def verify_source() -> dict[str, object]:
    source = SELF.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert_nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    require(not assert_nodes, "assert used as a semantic gate")
    require("\t" not in source, "source contains tabs")
    require(
        all(line == line.rstrip() for line in source.splitlines()),
        "source has trailing whitespace",
    )
    return {
        "source_lines": len(source.splitlines()),
        "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
        "assert_nodes": len(assert_nodes),
    }


def run_checks(tamper: str | None) -> dict[str, object]:
    source = verify_source()
    note = verify_note(tamper)
    items = build_seed()
    five = verify_five_cases(items, tamper)
    base = verify_fixed_base(items, tamper)
    stress = verify_stress(tamper)
    return {**source, **note, **five, **base, **stress}


def tamper_selftest() -> dict[str, object]:
    rejected = []
    for tamper in TAMPERS:
        process = subprocess.run(
            [sys.executable, str(SELF), "--check", "--tamper", tamper],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
        )
        require(process.returncode != 0, f"tamper survived: {tamper}")
        require("RESULT: FAIL" in process.stdout, f"tamper missed gates: {tamper}")
        rejected.append(tamper)
    optimized = subprocess.run(
        [sys.executable, "-O", str(SELF), "--check"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    require(optimized.returncode == 0, "optimized replay failed")
    require("RESULT: PASS" in optimized.stdout, "optimized replay did not pass")
    return {"tamper_rejections": rejected, "optimized": "PASS"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper", choices=TAMPERS)
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.check and not args.tamper_selftest:
        print("choose --check or --tamper-selftest", file=sys.stderr)
        return 2
    try:
        report: dict[str, object] = {}
        if args.check:
            report.update(run_checks(args.tamper))
        if args.tamper_selftest:
            report.update(tamper_selftest())
    except VerificationError as error:
        print(f"RESULT: FAIL: {error}")
        return 1
    print("RESULT: PASS")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
