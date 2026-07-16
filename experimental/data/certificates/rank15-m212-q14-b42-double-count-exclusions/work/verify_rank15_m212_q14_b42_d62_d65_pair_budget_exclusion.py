#!/usr/bin/env python3
"""Exact replay for the rank-15 D=62..65 pair-budget exclusions."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from math import comb

B = 42
POINTS = 211
PAIR_TOTAL = comb(B, 2)  # 861
INCIDENCE_TOTAL = B * 15  # 630


def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def profiles_at_d(double_count: int) -> list[tuple[int, ...]]:
    """Return c=(c_1,...,c_12), where c_w counts multiplicity w+3 points."""
    target_sum = double_count - 3
    target_square = 471 - double_count
    max_high = POINTS - double_count
    counts = [0] * 13
    rows: list[tuple[int, ...]] = []

    def visit(weight: int, total: int, square: int, number: int) -> None:
        if weight == 0:
            if total == target_sum and square == target_square and number <= max_high:
                rows.append(tuple(counts[1:13]))
            return
        maximum = min(
            (target_sum - total) // weight,
            (target_square - square) // (weight * weight),
            max_high - number,
        )
        for multiplicity in range(maximum + 1):
            counts[weight] = multiplicity
            visit(
                weight - 1,
                total + multiplicity * weight,
                square + multiplicity * weight * weight,
                number + multiplicity,
            )
        counts[weight] = 0

    visit(12, 0, 0, 0)
    return rows


def minimal_group_patterns(threshold: int) -> tuple[tuple[int, ...], ...]:
    """Minimal multisets of weights 1..10 having sum at least threshold."""
    patterns: list[tuple[int, ...]] = []
    counts = [0] * 10

    def visit(weight: int, total: int, minimum: int) -> None:
        if weight == 0:
            if total >= threshold and total - minimum < threshold:
                patterns.append(tuple(counts))
            return
        maximum = (threshold + 9 - total) // weight
        if maximum >= 0:
            for multiplicity in range(maximum + 1):
                counts[weight - 1] = multiplicity
                new_minimum = min(minimum, weight) if multiplicity else minimum
                visit(weight - 1, total + multiplicity * weight, new_minimum)
        counts[weight - 1] = 0

    visit(10, 0, 99)
    return tuple(patterns)


PATTERNS = {threshold: minimal_group_patterns(threshold) for threshold in range(1, 11)}


@lru_cache(maxsize=None)
def maximum_groups(counts: tuple[int, ...], threshold: int) -> int:
    best = 0
    for pattern in PATTERNS[threshold]:
        if all(pattern[i] <= counts[i] for i in range(10)):
            remainder = tuple(counts[i] - pattern[i] for i in range(10))
            best = max(best, 1 + maximum_groups(remainder, threshold))
    return best


def survives_exact_packing(profile: tuple[int, ...]) -> bool:
    """Necessary disjoint-group condition at every multiplicity 4..13 point."""
    small = profile[:10]
    big_count = profile[10] + profile[11]  # multiplicities 14 and 15
    for index, multiplicity in enumerate(small):
        if multiplicity == 0:
            continue
        weight = index + 1
        other = list(small)
        other[index] -= 1
        line_cap = big_count + maximum_groups(tuple(other), 11 - weight)
        if weight + 3 > line_cap:
            return False
    return True


def expanded(profile: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        multiplicity
        for weight, count in enumerate(profile, start=1)
        for multiplicity in [weight + 3] * count
    )


def profile_text(values: tuple[int, ...]) -> str:
    parts: list[str] = []
    for value in sorted(set(values)):
        count = values.count(value)
        parts.append(str(value) if count == 1 else f"{value}^{count}")
    return "{" + ",".join(parts) + "}"


def survives_heavy_noheavy_pair_gate(values: tuple[int, ...]) -> tuple[bool, tuple[int, ...]]:
    """Use heavy multiplicity >=11 and pairs of no-heavy arrangement lines."""
    heavy = tuple(k for k in values if k >= 11)
    light = tuple(k for k in values if k <= 10)
    h = len(heavy)
    incidence = sum(heavy)
    if incidence > B + comb(h, 2):
        return False, (h, incidence, -1, -1, -1)
    z_max = B + comb(h, 2) - incidence
    demand = sum(comb(max(0, k - h), 2) for k in light)
    capacity = comb(z_max, 2)
    return demand <= capacity, (h, incidence, z_max, demand, capacity)


def phi_42(incidence: int) -> int:
    q, r = divmod(incidence, B)
    return (B - r) * comb(q, 2) + r * comb(q + 1, 2)


def first_prefix_violation(values: tuple[int, ...]) -> tuple[tuple[int, ...], int, int, int]:
    chosen: list[int] = []
    incidence = 0
    for value in sorted(values, reverse=True):
        chosen.append(value)
        incidence += value
        demand = phi_42(incidence)
        capacity = comb(len(chosen), 2)
        if demand > capacity:
            return tuple(sorted(chosen)), incidence, demand, capacity
    raise RuntimeError("terminal subset-pair violation not found")


EXPECTED = (
    (4,4,5,5,6,7,7,7,7,7,7,10,14,14),
    (4,4,4,5,8,8,8,9,9,9,9,9,15),
    (4,4,5,6,6,6,7,7,7,7,7,10,13,15),
    (4,4,4,4,5,6,7,7,7,7,7,7,10,13,15),
    (6,6,6,6,6,7,7,7,7,7,7,14,15),
    (4,4,4,4,4,4,6,6,6,6,6,6,7,7,10,14,15),
    (4,4,5,5,5,5,5,5,6,6,7,7,7,10,14,15),
    (4,4,4,4,4,5,5,5,6,6,6,7,7,7,10,14,15),
    (4,4,4,4,4,4,4,4,6,6,6,6,7,7,7,10,14,15),
    (4,4,4,4,5,5,5,5,5,5,7,7,7,7,10,14,15),
    (4,4,4,4,4,4,4,5,5,5,6,7,7,7,7,10,14,15),
    (4,4,4,4,4,4,4,4,4,4,6,6,7,7,7,7,10,14,15),
    (4,4,4,4,4,4,4,4,4,4,4,4,7,7,7,7,7,10,14,15),
)


def main() -> None:
    check(PAIR_TOTAL == 861 and INCIDENCE_TOTAL == 630, "base arithmetic")
    expected_counts = {
        62: (1825, 26, 10, 16, 4),
        63: (2172, 41, 12, 29, 3),
        64: (2573, 51, 17, 34, 2),
    }
    print("RANK15_D62_D65_PAIR_BUDGET_EXCLUSION: PASS")
    print("D moment_profiles packing_survivors negative_zmax pair_rejects min_positive_gap survivors")
    for double_count, expected in expected_counts.items():
        moment_profiles = profiles_at_d(double_count)
        packing = [p for p in moment_profiles if survives_exact_packing(p)]
        negative_zmax = 0
        pair_rejects = 0
        gaps: list[int] = []
        survivors: list[tuple[int, ...]] = []
        for profile in packing:
            values = expanded(profile)
            survives, data = survives_heavy_noheavy_pair_gate(values)
            if survives:
                survivors.append(values)
            elif data[2] < 0:
                negative_zmax += 1
            else:
                pair_rejects += 1
                gaps.append(data[3] - data[4])
        actual = (
            len(moment_profiles),
            len(packing),
            negative_zmax,
            pair_rejects,
            min(gaps),
        )
        check(actual == expected, f"D={double_count} finite ledger")
        check(not survivors, f"D={double_count} survivors")
        print(
            f"{double_count} {actual[0]} {actual[1]} {actual[2]} "
            f"{actual[3]} {actual[4]} {len(survivors)}"
        )

    double_count = 65
    moment_profiles = profiles_at_d(double_count)
    packing = [p for p in moment_profiles if survives_exact_packing(p)]
    post_gate: list[tuple[int, ...]] = []
    gate_data: dict[tuple[int, ...], tuple[int, ...]] = {}
    negative_zmax = 0
    pair_rejects = 0
    for profile in packing:
        values = expanded(profile)
        survives, data = survives_heavy_noheavy_pair_gate(values)
        if survives:
            post_gate.append(values)
            gate_data[values] = data
        elif data[2] < 0:
            negative_zmax += 1
        else:
            pair_rejects += 1

    check(len(moment_profiles) == 3103, "moment profile count")
    check(len(packing) == 138, "packing survivor count")
    check((negative_zmax, pair_rejects) == (49, 76), "D=65 first-gate ledger")
    check(set(post_gate) == set(EXPECTED), "thirteen-profile set")
    check(len(post_gate) == 13, "post-gate survivor count")

    print("65 3103 138 49 76 1 13")
    print("D=65 terminal subset-pair ledger")
    print("id profile h n3 heavy I_H zmax gate_pair/cap terminal_subset J phi/cap")
    ledger_lines: list[str] = []
    for index, values in enumerate(EXPECTED, start=1):
        h_total = len(values)
        n3 = POINTS - double_count - h_total
        h, incidence, z_max, gate_demand, gate_capacity = gate_data[values]
        subset, selected_incidence, terminal_demand, terminal_capacity = first_prefix_violation(values)
        line = (
            f"{index:02d} {profile_text(values)} h={h_total} n3={n3} "
            f"H={h} I_H={incidence} zmax={z_max} "
            f"gate={gate_demand}/{gate_capacity} "
            f"X={profile_text(subset)} J={selected_incidence} "
            f"terminal={terminal_demand}/{terminal_capacity}"
        )
        ledger_lines.append(line)
        print(line)

    # Reproduce the diagnostic 67>66 inequality independently.
    special = EXPECTED[1]
    light = tuple(k for k in special if k < 11)
    noheavy_lines = B - 15
    light_incidences = sum(k - 1 for k in light)
    q, r = divmod(light_incidences, noheavy_lines)
    special_pair_demand = (noheavy_lines - r) * comb(q, 2) + r * comb(q + 1, 2)
    special_pair_capacity = comb(len(light), 2)
    check((noheavy_lines, light_incidences, special_pair_demand, special_pair_capacity) == (27, 74, 67, 66), "special 67>66 ledger")
    print("special_4^3_5_8^3_9^5_15 noheavy=27 incidences=74 pair_demand=67 capacity=66")

    # Reproduce the corrected near-PBD row and its vertex-equation failure.
    corrected = EXPECTED[4]
    survives, data = survives_heavy_noheavy_pair_gate(corrected)
    check(survives and data == (2, 29, 14, 90, 91), "corrected near-PBD gate")
    deg12_solutions = [(a, b) for a in range(8) for b in range(8) if 4*a + 3*b == 12]
    deg13_solutions = [(a, b) for a in range(8) for b in range(8) if 4*a + 3*b == 13]
    check(deg12_solutions == [(0, 4), (3, 0)], "degree-12 vertex solutions")
    check(deg13_solutions == [(1, 3)], "degree-13 vertex solutions")
    check(12 * 3 > 5 * 4, "near-PBD K4 membership contradiction")
    print("corrected_6^5_7^6_14_15 blocks=6xK5+5xK4 edges=90/91 vertex_equations=impossible")

    digest = sha256(("\n".join(ledger_lines) + "\n").encode()).hexdigest()
    print(f"ledger_sha256={digest}")
    print("payment=D62,D63,D64,D65")
    print("next=D66")


if __name__ == "__main__":
    main()
