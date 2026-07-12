#!/usr/bin/env python3
r"""Verify exchange-excess simple-pole separation over small prime fields.

For an m-subset S write Q_S for its locator and fix a depth-w locator
prefix, where the target line code has dimension k=m-w-1.  If S,T share
that prefix and t=d_J(S,T), then

    Q_S-Q_T = Q_(S intersect T) (Q_(S\T)-Q_(T\S)),
    deg(Q_(S\T)-Q_(T\S)) <= t-(w+1).

Consequently the pair collides at at most its exchange excess
e=t-(w+1) off-domain simple poles.  This script checks the factorization,
root bound, weighted pole average, Cauchy distinct-value compiler, and the
resulting source-line MCA witnesses by independent exact finite-field routes.
It is stdlib-only, deterministic, and writes no files.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from math import comb


CHECKS: list[tuple[str, bool]] = []
ROWS = 0
FIBERS = 0
PAIRS = 0
MINIMUM_PAIRS = 0
SHARP_POSITIVE_PAIRS = 0
SEPARATOR_GAIN_FIBERS = 0
SOURCE_LINES = 0


def require(name: str, condition: bool) -> None:
    CHECKS.append((name, bool(condition)))
    if not condition:
        print(f"FAIL: {name}")


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def trim(poly: tuple[int, ...], prime: int) -> tuple[int, ...]:
    values = list(poly)
    while len(values) > 1 and values[-1] % prime == 0:
        values.pop()
    return tuple(value % prime for value in values)


def add(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return trim(
        tuple(
            ((left[index] if index < len(left) else 0)
             + (right[index] if index < len(right) else 0))
            % prime
            for index in range(size)
        ),
        prime,
    )


def subtract(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    return add(left, tuple(-value for value in right), prime)


def multiply(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    product = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            product[left_index + right_index] += left_value * right_value
    return trim(tuple(value % prime for value in product), prime)


def evaluate(poly: tuple[int, ...], point: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * point + coefficient) % prime
    return value


def degree(poly: tuple[int, ...], prime: int) -> int:
    reduced = trim(poly, prime)
    return -1 if reduced == (0,) else len(reduced) - 1


def locator(points: tuple[int, ...], prime: int) -> tuple[int, ...]:
    result = (1,)
    for point in points:
        result = multiply(result, ((-point) % prime, 1), prime)
    return result


def prefix(locator_poly: tuple[int, ...], depth: int) -> tuple[int, ...]:
    support_size = len(locator_poly) - 1
    return tuple(locator_poly[support_size - index] for index in range(1, depth + 1))


def synthetic_divide_linear(
    poly: tuple[int, ...], root: int, prime: int
) -> tuple[tuple[int, ...], int]:
    """Return quotient and remainder for poly/(X-root)."""
    high = list(reversed(poly))
    quotient_high = [high[0]]
    for coefficient in high[1:-1]:
        quotient_high.append((coefficient + root * quotient_high[-1]) % prime)
    remainder = (high[-1] + root * quotient_high[-1]) % prime
    return trim(tuple(reversed(quotient_high)), prime), remainder


def interpolate(
    points: tuple[int, ...], values: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    """Lagrange interpolation through distinct points."""
    result = (0,)
    for index, point in enumerate(points):
        basis = (1,)
        denominator = 1
        for other_index, other in enumerate(points):
            if other_index == index:
                continue
            basis = multiply(basis, ((-other) % prime, 1), prime)
            denominator = denominator * (point - other) % prime
        scale = values[index] * pow(denominator, -1, prime) % prime
        result = add(result, tuple(scale * coefficient for coefficient in basis), prime)
    return trim(result, prime)


def build_u(
    support_size: int, fiber_prefix: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    result = [0] * (support_size + 1)
    result[support_size] = 1
    for index, coefficient in enumerate(fiber_prefix, start=1):
        result[support_size - index] = coefficient % prime
    return tuple(result)


def collision_count(values: list[int]) -> int:
    return sum(comb(multiplicity, 2) for multiplicity in Counter(values).values())


def verify_challenge_shear(
    label: str,
    slopes: list[int],
    certified_distinct: int,
    prime: int,
) -> None:
    bad_slopes = set(slopes)
    require(
        f"{label}: certified distinct slopes",
        len(bad_slopes) >= certified_distinct,
    )
    for challenge_size in sorted({1, max(1, prime // 2), prime}):
        challenge = set(range(challenge_size))
        best_translate = max(
            sum((slope + shift) % prime in challenge for slope in bad_slopes)
            for shift in range(prime)
        )
        nested_bound = ceil_div(challenge_size * certified_distinct, prime)
        require(
            f"{label}: challenge shear size {challenge_size}",
            best_translate >= nested_bound,
        )


def analyze_source_line(
    label: str,
    prime: int,
    domain: tuple[int, ...],
    support_size: int,
    dimension: int,
    fiber_prefix: tuple[int, ...],
    supports: tuple[tuple[int, ...], ...],
    pole: int,
    certified_distinct: int,
) -> None:
    global SOURCE_LINES
    SOURCE_LINES += 1
    u_poly = build_u(support_size, fiber_prefix, prime)
    slopes: list[int] = []

    for support_index, support in enumerate(supports):
        q_poly = locator(support, prime)
        listed_poly = subtract(u_poly, q_poly, prime)
        slope = evaluate(listed_poly, pole, prime)
        slopes.append(slope)
        centered = subtract(listed_poly, (slope,), prime)
        explanation, remainder = synthetic_divide_linear(centered, pole, prime)

        require(
            f"{label}: support {support_index} list degree",
            degree(listed_poly, prime) <= dimension,
        )
        require(
            f"{label}: support {support_index} exact division",
            remainder == 0 and degree(explanation, prime) < dimension,
        )

        for point in support:
            denominator_inverse = pow((point - pole) % prime, -1, prime)
            received_zero = evaluate(u_poly, point, prime) * denominator_inverse % prime
            received_one = -denominator_inverse % prime
            require(
                f"{label}: support {support_index} witness at {point}",
                (received_zero + slope * received_one) % prime
                == evaluate(explanation, point, prime),
            )

        interpolation_points = support[:dimension]
        received_one_values = tuple(
            -pow((point - pole) % prime, -1, prime) % prime
            for point in interpolation_points
        )
        candidate = interpolate(interpolation_points, received_one_values, prime)
        require(
            f"{label}: support {support_index} is support-wise nontrivial",
            any(
                evaluate(candidate, point, prime)
                != -pow((point - pole) % prime, -1, prime) % prime
                for point in support[dimension:]
            ),
        )

    multiplicities = Counter(slopes)
    require(
        f"{label}: slope collision second-moment identity",
        sum(value * value for value in multiplicities.values())
        == len(supports) + 2 * collision_count(slopes),
    )
    verify_challenge_shear(label, slopes, certified_distinct, prime)


def analyze_row(
    prime: int, domain: tuple[int, ...], support_size: int, dimension: int
) -> None:
    global ROWS, FIBERS, PAIRS, MINIMUM_PAIRS, SHARP_POSITIVE_PAIRS
    global SEPARATOR_GAIN_FIBERS
    ROWS += 1
    label = f"fp{prime}-n{len(domain)}-m{support_size}-k{dimension}"
    depth = support_size - dimension - 1
    outside = tuple(point for point in range(prime) if point not in set(domain))
    require(f"{label}: valid parameters", depth >= 0 and outside)

    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in combinations(domain, support_size):
        q_poly = locator(support, prime)
        fibers[prefix(q_poly, depth)].append(support)

    row_has_minimum = False
    row_has_strict_budget_gain = False
    source_lines_before = SOURCE_LINES

    for fiber_prefix, support_list in sorted(fibers.items()):
        if len(support_list) < 2:
            continue
        FIBERS += 1
        pair_excess: dict[tuple[int, int], int] = {}
        pair_roots: dict[tuple[int, int], tuple[int, ...]] = {}

        for left_index, right_index in combinations(range(len(support_list)), 2):
            PAIRS += 1
            left = support_list[left_index]
            right = support_list[right_index]
            left_set = set(left)
            right_set = set(right)
            common = tuple(sorted(left_set & right_set))
            left_exchange = tuple(sorted(left_set - right_set))
            right_exchange = tuple(sorted(right_set - left_set))
            exchange = len(left_exchange)
            excess = exchange - (depth + 1)
            pair_excess[(left_index, right_index)] = excess

            full_gap = subtract(locator(left, prime), locator(right, prime), prime)
            reduced_gap = subtract(
                locator(left_exchange, prime),
                locator(right_exchange, prime),
                prime,
            )
            factor_route = multiply(locator(common, prime), reduced_gap, prime)
            full_roots = tuple(point for point in outside if evaluate(full_gap, point, prime) == 0)
            reduced_roots = tuple(
                point for point in outside if evaluate(reduced_gap, point, prime) == 0
            )
            pair_roots[(left_index, right_index)] = reduced_roots

            require(f"{label}: pair exchange sizes agree", len(right_exchange) == exchange)
            require(f"{label}: pair rigidity", excess >= 0)
            require(f"{label}: pair common-core factorization", full_gap == factor_route)
            require(
                f"{label}: pair reduced-gap degree",
                degree(reduced_gap, prime) <= excess,
            )
            require(
                f"{label}: pair off-domain root route",
                full_roots == reduced_roots and len(reduced_roots) <= excess,
            )

            if excess == 0:
                MINIMUM_PAIRS += 1
                row_has_minimum = True
                require(f"{label}: minimum pair is pole-separated", not reduced_roots)
            if excess > 0 and len(reduced_roots) == excess:
                SHARP_POSITIVE_PAIRS += 1

        size = len(support_list)
        total_excess = sum(pair_excess.values())
        coordinate_loads = {
            point: sum(point in support for support in support_list)
            for point in domain
        }
        load_numerator = sum(
            load * (size - load) for load in coordinate_loads.values()
        )
        require(
            f"{label}: coordinate-load exchange identity",
            load_numerator % 2 == 0
            and total_excess
            == load_numerator // 2 - (depth + 1) * comb(size, 2),
        )
        old_budget = dimension * comb(size, 2)
        require(f"{label}: exchange budget never exceeds old k-budget", total_excess <= old_budget)
        if total_excess < old_budget:
            row_has_strict_budget_gain = True

        direct_collisions: dict[int, int] = {}
        direct_distinct: dict[int, int] = {}
        for pole in outside:
            values = [evaluate(locator(support, prime), pole, prime) for support in support_list]
            direct_collisions[pole] = collision_count(values)
            direct_distinct[pole] = len(set(values))
            pair_route = sum(pole in roots for roots in pair_roots.values())
            require(f"{label}: pole {pole} pair collision route", direct_collisions[pole] == pair_route)

        require(
            f"{label}: weighted collision sum",
            sum(direct_collisions.values()) <= total_excess,
        )
        best_pole = max(outside, key=lambda pole: direct_distinct[pole])
        minimum_collision = min(direct_collisions.values())
        require(
            f"{label}: averaging collision floor",
            minimum_collision <= total_excess // len(outside),
        )
        exact_cauchy = ceil_div(size * size, size + 2 * (total_excess // len(outside)))
        rational_cauchy = ceil_div(
            size * size * len(outside),
            size * len(outside) + 2 * total_excess,
        )
        maximum_excess = max(pair_excess.values(), default=0)
        geometric_excess = min(
            dimension,
            len(domain) - 2 * support_size + dimension,
        )
        require(
            f"{label}: automatic geometric excess cap",
            geometric_excess >= 0 and maximum_excess <= geometric_excess,
        )
        uniform_bound = ceil_div(
            size * len(outside),
            len(outside) + maximum_excess * (size - 1),
        )
        geometric_bound = ceil_div(
            size * len(outside),
            len(outside) + geometric_excess * (size - 1),
        )
        require(
            f"{label}: exact Cauchy distinct-value compiler",
            direct_distinct[best_pole] >= exact_cauchy >= rational_cauchy,
        )
        require(
            f"{label}: uniform-excess distinct-value compiler",
            direct_distinct[best_pole] >= uniform_bound >= geometric_bound,
        )

        if len(outside) > total_excess:
            SEPARATOR_GAIN_FIBERS += int(len(outside) <= old_budget)
            require(
                f"{label}: weighted separator criterion",
                minimum_collision == 0,
            )

        analyze_source_line(
            f"{label}-prefix{fiber_prefix}",
            prime,
            domain,
            support_size,
            dimension,
            fiber_prefix,
            tuple(support_list),
            best_pole,
            exact_cauchy,
        )

    largest_fiber = max(fibers.values(), key=len)
    prefix_floor = ceil_div(comb(len(domain), support_size), prime**depth)
    require(
        f"{label}: identity-prefix pigeonhole floor",
        len(largest_fiber) >= prefix_floor,
    )
    selected_supports = tuple(largest_fiber[:prefix_floor])
    geometric_excess = max(
        0,
        min(dimension, len(domain) - 2 * support_size + dimension),
    )
    identity_floor = ceil_div(
        prefix_floor * len(outside),
        len(outside) + geometric_excess * (prefix_floor - 1),
    )
    selected_prefix = prefix(locator(selected_supports[0], prime), depth)
    selected_u = build_u(support_size, selected_prefix, prime)
    selected_slopes_by_pole = {
        pole: [
            evaluate(
                subtract(selected_u, locator(support, prime), prime),
                pole,
                prime,
            )
            for support in selected_supports
        ]
        for pole in outside
    }
    identity_pole = max(
        outside,
        key=lambda pole: len(set(selected_slopes_by_pole[pole])),
    )
    verify_challenge_shear(
        f"{label}: identity-prefix compiler",
        selected_slopes_by_pole[identity_pole],
        identity_floor,
        prime,
    )

    require(
        f"{label}: row contains a nonsingleton prefix fiber",
        SOURCE_LINES > source_lines_before,
    )
    require(f"{label}: row exercises a minimum-exchange pair", row_has_minimum)
    require(f"{label}: row exchange budget strictly improves k-budget", row_has_strict_budget_gain)


def main() -> int:
    # Depth zero: the unique prefix fiber consists of every support.
    analyze_row(11, tuple(range(1, 7)), 3, 2)
    analyze_row(13, tuple(range(1, 9)), 4, 2)
    # Here m=(n+k)/2, so every nonsingleton prefix pair has zero excess.
    analyze_row(13, tuple(range(1, 12)), 7, 3)
    analyze_row(17, tuple(range(1, 11)), 5, 2)
    analyze_row(19, tuple(range(1, 11)), 5, 3)

    require("positive-excess root bound is attained", SHARP_POSITIVE_PAIRS > 0)
    require("new separator succeeds where old k-budget does not", SEPARATOR_GAIN_FIBERS > 0)

    failed = [name for name, passed in CHECKS if not passed]
    print(f"rows={ROWS}")
    print(f"fibers={FIBERS}")
    print(f"pairs={PAIRS}")
    print(f"minimum_exchange_pairs={MINIMUM_PAIRS}")
    print(f"sharp_positive_excess_pairs={SHARP_POSITIVE_PAIRS}")
    print(f"separator_gain_fibers={SEPARATOR_GAIN_FIBERS}")
    print(f"source_lines={SOURCE_LINES}")
    if failed:
        print(f"RESULT: FAIL ({len(failed)}/{len(CHECKS)} checks failed)")
        return 1
    print(f"RESULT: PASS ({len(CHECKS)} checks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
