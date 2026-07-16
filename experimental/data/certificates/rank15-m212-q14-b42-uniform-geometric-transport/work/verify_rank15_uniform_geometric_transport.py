#!/usr/bin/env python3
"""Exact standard-library replay for the rank-15 D=66..68 and D=146 cut.

The companion JSON stores sparse integer Farkas certificates.  This checker
reconstructs every source-derived moment profile, the exact disjoint-group
packing gate, every admissible line type, all pair-capacity rows, the residual
incidence gates, the two-15-point affine-stabilizer obstruction, the D=68
Kneser obstruction, and the D=146 incidence contradiction.

No solver, floating-point arithmetic, third-party package, or assert statement
is used by this verifier.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from functools import lru_cache
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "rank15_uniform_geometric_transport_certificates.json"
P_FIELD = 2_130_706_433


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def profile_text(profile: tuple[int, ...]) -> str:
    return ",".join(f"{i + 4}^{count}" for i, count in enumerate(profile) if count)


def moment_profiles(double_count: int) -> list[tuple[int, ...]]:
    """All exact nonnegative c_w profiles for w=1,...,12."""
    target_linear = double_count - 3
    target_square = 471 - double_count
    maximum_high_points = 211 - double_count
    current = [0] * 13
    rows: list[tuple[int, ...]] = []

    def visit(weight: int, linear: int, square: int, high_points: int) -> None:
        if weight == 0:
            if (
                linear == target_linear
                and square == target_square
                and high_points <= maximum_high_points
            ):
                rows.append(tuple(current[1:13]))
            return
        remaining_linear = target_linear - linear
        remaining_square = target_square - square
        remaining_points = maximum_high_points - high_points
        if remaining_linear < 0 or remaining_square < 0 or remaining_points < 0:
            return
        maximum = min(
            remaining_linear // weight,
            remaining_square // (weight * weight),
            remaining_points,
        )
        for count in range(maximum + 1):
            current[weight] = count
            visit(
                weight - 1,
                linear + count * weight,
                square + count * weight * weight,
                high_points + count,
            )
        current[weight] = 0

    visit(12, 0, 0, 0)
    return rows


def minimal_groups(threshold: int) -> tuple[tuple[int, ...], ...]:
    """Inclusion-minimal weight-1,...,10 groups meeting a threshold."""
    rows: list[tuple[int, ...]] = []
    current = [0] * 10

    def visit(weight: int, total: int) -> None:
        if weight == 11:
            used = [w for w in range(1, 11) if current[w - 1]]
            if used and total >= threshold and total - min(used) < threshold:
                rows.append(tuple(current))
            return
        maximum = (threshold + 9 - total) // weight
        if maximum >= 0:
            for count in range(maximum + 1):
                current[weight - 1] = count
                visit(weight + 1, total + count * weight)
        current[weight - 1] = 0

    visit(1, 0)
    return tuple(rows)


MINIMAL_GROUPS = {threshold: minimal_groups(threshold) for threshold in range(1, 11)}


@lru_cache(maxsize=None)
def max_disjoint_groups(state: tuple[int, ...], threshold: int) -> int:
    best = 0
    for group in MINIMAL_GROUPS[threshold]:
        if all(group[i] <= state[i] for i in range(10)):
            remainder = tuple(state[i] - group[i] for i in range(10))
            best = max(best, 1 + max_disjoint_groups(remainder, threshold))
    return best


def passes_disjoint_group_gate(profile: tuple[int, ...]) -> bool:
    big_points = profile[10] + profile[11]
    for i, count in enumerate(profile[:10]):
        if count:
            other_small = list(profile[:10])
            other_small[i] -= 1
            required_lines = i + 4
            threshold = 10 - i
            if required_lines > big_points + max_disjoint_groups(
                tuple(other_small), threshold
            ):
                return False
    return True


def line_types() -> list[tuple[int, ...]]:
    """All per-line high-point types satisfying S>=11 and S+s<=26."""
    rows: list[tuple[int, ...]] = []
    current = [0] * 12

    def visit(index: int, support_cost: int, weight_sum: int) -> None:
        if index == 12:
            if weight_sum >= 11:
                rows.append(tuple(current))
            return
        weight = index + 1
        for count in range((26 - support_cost) // (weight + 1) + 1):
            current[index] = count
            visit(
                index + 1,
                support_cost + count * (weight + 1),
                weight_sum + count * weight,
            )
        current[index] = 0

    visit(0, 0, 0)
    return rows


LINE_TYPES = line_types()
PAIRS = [(i, j) for i in range(12) for j in range(i, 12)]
PAIR_ROWS = [
    tuple(comb(t[i], 2) if i == j else t[i] * t[j] for i, j in PAIRS)
    for t in LINE_TYPES
]
FULL_ROWS = [(1,) + t + pair_row for t, pair_row in zip(LINE_TYPES, PAIR_ROWS)]


def global_rhs(profile: tuple[int, ...]) -> tuple[int, ...]:
    equalities = (42,) + tuple((i + 4) * profile[i] for i in range(12))
    capacities = tuple(
        comb(profile[i], 2) if i == j else profile[i] * profile[j]
        for i, j in PAIRS
    )
    return equalities + capacities


def is_admissible(line_type: tuple[int, ...], profile: tuple[int, ...]) -> bool:
    return all(line_type[i] <= profile[i] for i in range(12))


def coefficient(
    sparse: tuple[tuple[int, int], ...],
    line_type: tuple[int, ...],
    pair_row: tuple[int, ...],
) -> int:
    total = 0
    for index, value in sparse:
        if index == 0:
            entry = 1
        elif index < 13:
            entry = line_type[index - 1]
        else:
            entry = pair_row[index - 13]
        total += value * entry
    return total


def verify_certificate_syntax(
    sparse_rows: list[list[int]],
) -> tuple[tuple[int, int], ...]:
    seen: set[int] = set()
    normalized: list[tuple[int, int]] = []
    for row in sparse_rows:
        check(isinstance(row, list) and len(row) == 2, "bad sparse certificate row")
        index, value = row
        check(isinstance(index, int) and isinstance(value, int), "noninteger certificate")
        check(0 <= index < 91, "certificate index out of range")
        check(index not in seen, "duplicate certificate index")
        check(value != 0, "zero stored coefficient")
        if index >= 13:
            check(value > 0, "pair-capacity multiplier is not positive")
        seen.add(index)
        normalized.append((index, value))
    check(normalized == sorted(normalized), "certificate indices are not canonical")
    return tuple(normalized)


def negative_type_indices(
    sparse: tuple[tuple[int, int], ...]
) -> tuple[int, ...]:
    negative: list[int] = []
    for row_index, row in enumerate(FULL_ROWS):
        total = 0
        for index, value in sparse:
            total += value * row[index]
        if total < 0:
            negative.append(row_index)
    return tuple(negative)


def verify_farkas_rhs_and_admissibility(
    profile: tuple[int, ...],
    sparse: tuple[tuple[int, int], ...],
    negative_types: tuple[int, ...],
) -> None:
    rhs = global_rhs(profile)
    rhs_value = sum(value * rhs[index] for index, value in sparse)
    check(rhs_value < 0, f"nonnegative Farkas RHS for {profile_text(profile)}")
    for row_index in negative_types:
        check(
            not is_admissible(LINE_TYPES[row_index], profile),
            f"negative admissible line coefficient for {profile_text(profile)}",
        )


def expanded_multiplicities(profile: tuple[int, ...]) -> list[int]:
    values: list[int] = []
    for i, count in enumerate(profile):
        values.extend([i + 4] * count)
    values.sort(reverse=True)
    return values


def strongest_distinguished_pair_row(profile: tuple[int, ...]) -> tuple[int, ...]:
    values = expanded_multiplicities(profile)
    best: tuple[int, ...] | None = None
    for selected in range(1, len(values) + 1):
        incidence = sum(values[:selected])
        avoiding_upper = 42 + comb(selected, 2) - incidence
        demand = sum(
            comb(max(0, multiplicity - selected), 2)
            for multiplicity in values[selected:]
        )
        capacity = comb(avoiding_upper, 2) if avoiding_upper >= 0 else -1
        row = (
            capacity - demand,
            selected,
            incidence,
            avoiding_upper,
            demand,
            capacity,
        )
        if best is None or row < best:
            best = row
    check(best is not None, "empty high-point profile")
    return best


def two_fifteen_field_gate() -> None:
    """Check the only stabilizer orders permitted by a 14-point affine set."""
    possible: list[tuple[int, int, int]] = []
    for order in range(13, 15):
        for fixed in (0, 1):
            remainder = 14 - fixed
            if remainder > 0 and remainder % order == 0 and (P_FIELD - 1) % order == 0:
                possible.append((order, fixed, remainder // order))
    check(not possible, "two-15-point affine stabilizer survives the field gate")
    check((P_FIELD - 1) % 13 == 10, "mod-13 field remainder")
    check((P_FIELD - 1) % 14 == 8, "mod-14 field remainder")


def d68_no_heavy_pair_gate() -> None:
    """Replay the missing no-heavy-line concurrency lemma for D=68.

    A small point off the three heavy sides uses at least k-3 of the three
    no-heavy lines; a point on a heavy side uses at least k-2.  Two distinct
    points cannot use the same pair of no-heavy lines.  This finite replay
    checks the only two terminal profiles after the preceding incidence cuts.
    """
    lines = frozenset(range(3))
    pairs = frozenset({frozenset((0, 1)), frozenset((0, 2)), frozenset((1, 2))})

    def pair_set(subset: frozenset[int]) -> frozenset[frozenset[int]]:
        return frozenset(pair for pair in pairs if pair <= subset)

    choices = [
        frozenset(i for i in lines if mask & (1 << i))
        for mask in range(1 << 3)
        if mask.bit_count() >= 2
    ]

    allocations: list[tuple[frozenset[int], ...]] = []
    for first in choices:
        for second in choices:
            for third in choices:
                used = (pair_set(first), pair_set(second), pair_set(third))
                if all(used[i].isdisjoint(used[j]) for i in range(3) for j in range(i)):
                    allocations.append((first, second, third))

    check(len(allocations) == 6, "D=68 three-fivefold no-heavy allocations")
    for allocation in allocations:
        check(all(len(subset) == 2 for subset in allocation), "D=68 fivefold side case")
        check(
            frozenset().union(*(pair_set(subset) for subset in allocation)) == pairs,
            "D=68 fivefold pair exhaustion",
        )

    sixfold_choices = [subset for subset in choices if len(subset) >= 3]
    check(sixfold_choices == [lines], "D=68 sixfold no-heavy allocation")
    check(pair_set(sixfold_choices[0]) == pairs, "D=68 sixfold pair exhaustion")


def verify_d68_kneser(profiles: list[tuple[int, ...]]) -> None:
    expected = {
        (26, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
        (29, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1),
    }
    check(set(profiles) == expected, "unexpected D=68 terminal profile set")
    d68_no_heavy_pair_gate()

    for profile in profiles:
        small_count = sum(profile[:9])
        small_weight = sum((i + 1) * profile[i] for i in range(9))
        small_cost = sum((i + 2) * profile[i] for i in range(9))
        check(small_weight == 32, "D=68 small-weight total")
        if profile[1] == 3:
            check((small_count, small_cost) == (29, 61), "D=68 profile A totals")
        else:
            check((small_count, small_cost) == (30, 62), "D=68 profile B totals")

    # Heavy multiplicities 13,14,15 give exactly three sides and three
    # no-heavy lines.  The side-corrected triple/grid count is 131 in either
    # profile; its algebra is checked for every possible side-small pattern.
    for profile in profiles:
        small_points = sum(profile[:9])
        small_cost = sum((i + 2) * profile[i] for i in range(9))
        small_weight = sum((i + 1) * profile[i] for i in range(9))
        for side_n4_ab in (0, 1):
            for side_n4_ac in (0, 1):
                for side_n5_ab in (0, 1):
                    # AB contains at most one side-small point; AC can contain
                    # only a fourfold point; no small point lies on BC.
                    if side_n4_ab + side_n5_ab > 1:
                        continue
                    if side_n5_ab and profile[1] == 0:
                        continue
                    if side_n4_ab + side_n4_ac > profile[0]:
                        continue
                    side_count = side_n4_ab + side_n4_ac + side_n5_ab
                    side_weight = side_n4_ab + side_n4_ac + 2 * side_n5_ab
                    side_cost = 2 * (side_n4_ab + side_n4_ac) + 3 * side_n5_ab
                    total_triples = 11 * 15 - (small_cost - side_cost)
                    nongrid_upper = 2 + side_weight
                    correlation_floor = (
                        small_points - side_count + total_triples - nongrid_upper
                    )
                    check(correlation_floor == 131, "D=68 side correction")

    check(9 * 12 + 2 * 11 == 130 < 131, "D=68 full-correlation count")
    full_correlations = 10
    possible_orders = [h for h in range(1, 14) if (P_FIELD - 1) % h == 0]
    check(possible_orders == [1, 2, 4, 8], "D=68 stabilizer orders")
    lower_bounds = {
        h: h * ((full_correlations + h - 1) // h)
        + h * ((12 + h - 1) // h)
        - h
        for h in possible_orders
    }
    check(lower_bounds == {1: 21, 2: 20, 4: 20, 8: 24}, "D=68 Kneser rows")
    check(min(lower_bounds.values()) > 13, "D=68 Kneser contradiction")


def verify_d146() -> tuple[int, str, tuple[tuple[int, int], ...]]:
    profiles = moment_profiles(146)
    forced = (0, 52, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    check(profiles == [forced], "D=146 moment profile")
    local_solutions = tuple(
        (fivefold, sixfold)
        for fivefold in range(15)
        for sixfold in range(15)
        if 3 * fivefold + 4 * sixfold == 26
    )
    check(local_solutions == ((2, 5), (6, 2)), "D=146 line solutions")
    actual_sixfold_incidence = 13 * 6
    required_sixfold_incidence = 42 * min(b for _, b in local_solutions)
    check(
        actual_sixfold_incidence == 78 < required_sixfold_incidence == 84,
        "D=146 sixfold incidence",
    )
    return len(profiles), profile_text(forced), local_solutions


def verify_d145_relaxation_survivor() -> str:
    """Exact abstract line-type survivor of the moment+pair-capacity relaxation."""
    profile = (0, 50, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    double_count = 145
    triple_count = 211 - double_count - sum(profile)
    check(triple_count == 2, "D=145 triple count")
    check(sum((i + 1) * profile[i] for i in range(12)) == double_count - 3, "D=145 linear moment")
    check(sum((i + 1) ** 2 * profile[i] for i in range(12)) == 471 - double_count, "D=145 square moment")
    check(passes_disjoint_group_gate(profile), "D=145 packing gate")
    distinguished = strongest_distinguished_pair_row(profile)
    check(distinguished == (200, 1, 6, 36, 430, 630), "D=145 distinguished-pair row")

    # One line of type A and 41 lines of type B.  Entries are
    # (multiplicity, d, t, n5, n6).
    line_rows = ((1, 3, 6, 4, 2), (41, 7, 0, 6, 2))
    check(sum(multiplicity for multiplicity, *_ in line_rows) == 42, "D=145 line count")
    for _, doubles, triples, fivefold, sixfold in line_rows:
        support = doubles + triples + fivefold + sixfold
        other_lines = doubles + 2 * triples + 4 * fivefold + 5 * sixfold
        check((support, other_lines) == (15, 41), "D=145 local line equation")
    incidences = {
        2: sum(m * d for m, d, _, _, _ in line_rows),
        3: sum(m * t for m, _, t, _, _ in line_rows),
        5: sum(m * a for m, _, _, a, _ in line_rows),
        6: sum(m * b for m, _, _, _, b in line_rows),
    }
    check(incidences == {2: 290, 3: 6, 5: 250, 6: 84}, "D=145 incidences")
    pair_usage = {
        "5-5": sum(m * comb(a, 2) for m, _, _, a, _ in line_rows),
        "5-6": sum(m * a * b for m, _, _, a, b in line_rows),
        "6-6": sum(m * comb(b, 2) for m, _, _, _, b in line_rows),
    }
    pair_caps = {"5-5": comb(50, 2), "5-6": 50 * 14, "6-6": comb(14, 2)}
    check(pair_usage == {"5-5": 621, "5-6": 500, "6-6": 42}, "D=145 pair usage")
    check(pair_caps == {"5-5": 1225, "5-6": 700, "6-6": 91}, "D=145 pair caps")
    check(all(pair_usage[key] <= pair_caps[key] for key in pair_usage), "D=145 pair capacities")
    return (
        "D=145_relaxation profile=5^50,6^14 n3=2 "
        "line_types=1*(d3,t6,5^4,6^2)+41*(d7,t0,5^6,6^2) "
        "pair_usage=5-5:621/1225,5-6:500/700,6-6:42/91 "
        "distinguished_pair_margin=200"
    )


def main() -> None:
    raw = DATA_PATH.read_bytes()
    payload = json.loads(raw)
    check(payload.get("schema") == "rank15-uniform-geometric-transport-farkas-v1", "schema")
    check(payload.get("line_type_count") == len(LINE_TYPES) == 2025, "line type count")
    check(payload.get("pair_row_count") == len(PAIRS) == 78, "pair row count")
    check(payload.get("covered_D") == [66, 67, 68], "covered D list")
    check(payload.get("certificate_count") == 4387, "certificate count declaration")

    expected_counts = {
        66: (3586, 378, 373, 5, 2, 3, 0),
        67: (4128, 1174, 1168, 6, 4, 2, 0),
        68: (4849, 2858, 2846, 12, 7, 3, 2),
    }
    expected_survivors = {
        66: [
            (3, 14, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1),
            (0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 2),
            (9, 11, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2),
            (24, 3, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2),
            (27, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 2),
        ],
        67: [
            (4, 14, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
            (6, 13, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1),
            (0, 2, 12, 0, 0, 0, 0, 0, 0, 0, 0, 2),
            (2, 14, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2),
            (12, 10, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2),
            (27, 2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2),
        ],
        68: [
            (5, 14, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0),
            (7, 13, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1),
            (9, 12, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1),
            (26, 3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1),
            (29, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1),
            (0, 4, 11, 0, 0, 0, 0, 0, 0, 0, 0, 2),
            (3, 1, 12, 0, 0, 0, 0, 0, 0, 0, 0, 2),
            (2, 16, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2),
            (5, 13, 1, 0, 0, 0, 1, 0, 0, 0, 0, 2),
            (8, 10, 2, 0, 0, 0, 1, 0, 0, 0, 0, 2),
            (15, 9, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2),
            (30, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2),
        ],
    }

    unique_certificate_keys: set[tuple[tuple[int, int], ...]] = set()
    negative_type_cache: dict[tuple[tuple[int, int], ...], tuple[int, ...]] = {}
    total_certificates = 0
    output_rows: list[str] = []
    d68_terminal: list[tuple[int, ...]] = []

    for double_count in (66, 67, 68):
        block = payload["data"][str(double_count)]
        profiles = moment_profiles(double_count)
        packing = [p for p in profiles if passes_disjoint_group_gate(p)]
        expected = expected_counts[double_count]
        check(len(profiles) == block["moment_count"] == expected[0], "moment count")
        check(len(packing) == block["packing_count"] == expected[1], "packing count")

        certificate_map: dict[tuple[int, ...], tuple[tuple[int, int], ...]] = {}
        for row in block["certificates"]:
            profile = tuple(row["profile"])
            check(profile not in certificate_map, "duplicate certified profile")
            sparse = verify_certificate_syntax(row["certificate"])
            certificate_map[profile] = sparse
            unique_certificate_keys.add(sparse)
            if sparse not in negative_type_cache:
                negative_type_cache[sparse] = negative_type_indices(sparse)
            verify_farkas_rhs_and_admissibility(
                profile, sparse, negative_type_cache[sparse]
            )
        total_certificates += len(certificate_map)
        check(len(certificate_map) == expected[2], "Farkas count")

        packing_set = set(packing)
        check(set(certificate_map).issubset(packing_set), "certificate outside packing set")
        survivors = [p for p in packing if p not in certificate_map]
        stored_survivors = [tuple(p) for p in block["line_type_survivors"]]
        check(survivors == stored_survivors, "stored survivor list")
        check(survivors == expected_survivors[double_count], "expected survivor list")
        check(len(survivors) == expected[3], "survivor count")

        heavy_rejected: list[tuple[int, ...]] = []
        after_heavy: list[tuple[int, ...]] = []
        for profile in survivors:
            if strongest_distinguished_pair_row(profile)[0] < 0:
                heavy_rejected.append(profile)
            else:
                after_heavy.append(profile)
        check(len(heavy_rejected) == expected[4], "distinguished-pair count")

        two_fifteen_rejected = [p for p in after_heavy if p[11] >= 2]
        after_two_fifteen = [p for p in after_heavy if p[11] < 2]
        check(len(two_fifteen_rejected) == expected[5], "two-15 count")
        check(len(after_two_fifteen) == expected[6], "terminal count")
        if double_count == 68:
            d68_terminal = after_two_fifteen
        else:
            check(not after_two_fifteen, "unexpected non-D68 terminal profile")

        output_rows.append(
            f"D={double_count} moment={len(profiles)} packing={len(packing)} "
            f"farkas={len(certificate_map)} line_type_survivors={len(survivors)} "
            f"distinguished_pair_rejected={len(heavy_rejected)} "
            f"two15_rejected={len(two_fifteen_rejected)} "
            f"kneser_rejected={len(after_two_fifteen) if double_count == 68 else 0} remaining=0"
        )
        output_rows.append(
            "  line_type_profiles=" + ";".join(profile_text(p) for p in survivors)
        )

    check(total_certificates == payload["certificate_count"] == 4387, "total certificate count")
    two_fifteen_field_gate()
    verify_d68_kneser(d68_terminal)
    d146_count, d146_profile, local_solutions = verify_d146()
    d145_route_cut = verify_d145_relaxation_survivor()

    check(P_FIELD - 1 == (2**24) * 127, "field factorization")
    print("RANK15_UNIFORM_GEOMETRIC_TRANSPORT: PASS")
    print(f"certificate_sha256={hashlib.sha256(raw).hexdigest()}")
    print(
        f"line_types={len(LINE_TYPES)} pair_rows={len(PAIRS)} "
        f"certificates={total_certificates} unique_certificates={len(unique_certificate_keys)}"
    )
    for row in output_rows:
        print(row)
    print(d145_route_cut)
    print(
        f"D=146 moment={d146_count} profile={d146_profile} "
        f"local_solutions={local_solutions} sixfold_incidence=78 "
        f"required_minimum=84 remaining=0"
    )
    print(
        f"field={P_FIELD} field_minus_one=2^24*127 "
        f"mod13={(P_FIELD - 1) % 13} mod14={(P_FIELD - 1) % 14}"
    )
    print("SCOPE conditional_arrangement_interface_only")
    print("NOVEL excluded_D=66,67,68,146 conditional_post_804_residual_D=69..145")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RANK15_UNIFORM_GEOMETRIC_TRANSPORT: FAIL: {exc}", file=sys.stderr)
        raise
