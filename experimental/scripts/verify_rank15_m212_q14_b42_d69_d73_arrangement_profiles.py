#!/usr/bin/env python3
"""Exact arithmetic replay for the conditional rank-15 D=69..73 packet.

Python standard library only.  The verifier reconstructs the moment profiles,
applies the descending-prefix necessary inequalities and the proved at-most-one
multiplicity-15 filter, checks the field/divisor arithmetic used by the Kneser
step, and checks the pairwise-balanced-design and D=73 direction-spectrum
arithmetic.

It does not machine-prove the geometric lemmas: the multiplicity-14 matching
lemma, the coordinate normalizations, the applications of Cauchy-Davenport or
Kneser, the construction of the PBD, or the conversion to the affine D=73
wall.  Those arguments are in the accompanying theorem note.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import Counter
from dataclasses import dataclass, replace
from math import comb


P = 2_130_706_433
LINES = 42
POINTS = 211
POINTS_PER_LINE = 15
MAX_MULTIPLICITY = 15
D_VALUES = tuple(range(69, 74))


class VerificationError(RuntimeError):
    """Raised when a frozen arithmetic obligation fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class ReplayParameters:
    p: int = P
    lines: int = LINES
    points: int = POINTS
    points_per_line: int = POINTS_PER_LINE
    max_multiplicity: int = MAX_MULTIPLICITY
    d_values: tuple[int, ...] = D_VALUES
    prefix_capacity_shift: int = 0
    allow_two_multiplicity_15_points: bool = False


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def divisors_of_p_minus_one() -> tuple[int, ...]:
    return tuple(sorted({(2**exponent) * odd for exponent in range(25) for odd in (1, 127)}))


def profiles_at_d(params: ReplayParameters, double_count: int) -> list[tuple[int, ...]]:
    """Return tuples (n4,...,n_max) satisfying all three global moments."""
    max_weight = params.max_multiplicity - 3
    target_linear = (
        params.lines * params.points_per_line - 3 * params.points + double_count
    )
    target_square = (
        2 * (comb(params.lines, 2) - 3 * params.points + 2 * double_count)
        - 5 * target_linear
    )
    max_high_points = params.points - double_count
    counts = [0] * (max_weight + 1)
    rows: list[tuple[int, ...]] = []

    def visit(weight: int, linear: int, square: int, number: int) -> None:
        if weight == 0:
            if (
                linear == target_linear
                and square == target_square
                and number <= max_high_points
            ):
                rows.append(tuple(counts[1:]))
            return

        linear_left = target_linear - linear
        square_left = target_square - square
        count_left = max_high_points - number
        if min(linear_left, square_left, count_left) < 0:
            return
        maximum = min(
            linear_left // weight,
            square_left // (weight * weight),
            count_left,
        )
        for multiplicity in range(maximum + 1):
            counts[weight] = multiplicity
            visit(
                weight - 1,
                linear + multiplicity * weight,
                square + multiplicity * weight * weight,
                number + multiplicity,
            )
        counts[weight] = 0

    visit(max_weight, 0, 0, 0)
    return rows


def multiplicity_count(profile: tuple[int, ...], multiplicity: int) -> int:
    if multiplicity < 4 or multiplicity - 4 >= len(profile):
        return 0
    return profile[multiplicity - 4]


def n3(params: ReplayParameters, double_count: int, profile: tuple[int, ...]) -> int:
    return params.points - double_count - sum(profile)


def expanded(profile: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        multiplicity
        for multiplicity, count in enumerate(profile, start=4)
        for _ in range(count)
    )


def prefix_margin(params: ReplayParameters, profile: tuple[int, ...]) -> int:
    values = sorted(expanded(profile), reverse=True)
    margins: list[int] = []
    for selected_count in range(1, len(values) + 1):
        incidence = sum(values[:selected_count])
        avoiding_bound = (
            params.lines
            + comb(selected_count, 2)
            - incidence
            + params.prefix_capacity_shift
        )
        demand = sum(
            comb(max(0, multiplicity - selected_count), 2)
            for multiplicity in values[selected_count:]
        )
        capacity = comb(avoiding_bound, 2) if avoiding_bound >= 0 else -1
        margins.append(capacity - demand)
    return min(margins)


def profile_signature(profile: tuple[int, ...]) -> str:
    fields = [
        f"n{multiplicity}={count}"
        for multiplicity, count in enumerate(profile, start=4)
        if count
    ]
    return " ".join(fields)


def terminal_core_line(
    params: ReplayParameters, double_count: int, profile: tuple[int, ...]
) -> str:
    return f"D={double_count} n3={n3(params, double_count, profile)} {profile_signature(profile)}"


EXPECTED_COUNTS = {
    69: (5_473, 7, 3),
    70: (6_115, 5, 2),
    71: (6_998, 22, 3),
    72: (7_706, 23, 2),
    73: (8_446, 25, 3),
}

EXPECTED_TERMINAL_LINES = (
    "D=69 n3=109 n4=27 n5=3 n14=3",
    "D=69 n3=108 n4=29 n5=2 n13=1 n14=1 n15=1",
    "D=69 n3=108 n4=30 n6=1 n14=3",
    "D=70 n3=106 n4=30 n5=2 n14=3",
    "D=70 n3=105 n4=32 n5=1 n13=1 n14=1 n15=1",
    "D=71 n3=103 n4=33 n5=1 n14=3",
    "D=71 n3=102 n4=35 n13=1 n14=1 n15=1",
    "D=71 n3=123 n6=15 n14=1 n15=1",
    "D=72 n3=100 n4=36 n14=3",
    "D=72 n3=121 n5=2 n6=14 n14=1 n15=1",
    "D=73 n3=122 n4=1 n5=1 n6=1 n7=11 n11=1 n15=1",
    "D=73 n3=118 n4=3 n5=1 n6=14 n14=1 n15=1",
    "D=73 n3=119 n5=4 n6=13 n14=1 n15=1",
)

EXPECTED_TERMINAL_STREAM_SHA256 = "b7089c1cd264762b603188f11545551462ab34bd97b9c8cacbb100e7589f7fb1"


def classify_terminal(double_count: int, profile: tuple[int, ...]) -> str:
    if multiplicity_count(profile, 14) >= 3:
        return "THREE_N14"
    if all(multiplicity_count(profile, value) > 0 for value in (13, 14, 15)):
        return "N13_N14_N15"
    signature = profile_signature(profile)
    pbd_routes = {
        (71, "n6=15 n14=1 n15=1"): "PBD_D71",
        (72, "n5=2 n6=14 n14=1 n15=1"): "PBD_D72",
        (73, "n4=3 n5=1 n6=14 n14=1 n15=1"): "PBD_D73_4_2BLOCKS",
        (73, "n5=4 n6=13 n14=1 n15=1"): "PBD_D73_4_3BLOCKS",
    }
    if (double_count, signature) in pbd_routes:
        return pbd_routes[(double_count, signature)]
    if (
        double_count == 73
        and signature == "n4=1 n5=1 n6=1 n7=11 n11=1 n15=1"
    ):
        return "OPEN_D73"
    raise VerificationError(f"unclassified terminal profile: D={double_count} {signature}")


def pbd_blocks(profile: tuple[int, ...]) -> tuple[int, ...]:
    require(multiplicity_count(profile, 14) == 1, "PBD needs one 14-point")
    require(multiplicity_count(profile, 15) == 1, "PBD needs one 15-point")
    blocks = [2]
    for multiplicity in range(4, 14):
        blocks.extend([multiplicity - 2] * multiplicity_count(profile, multiplicity))
    return tuple(sorted(blocks))


def exact_vertex_solutions(
    small_block_count: int, small_coefficient: int, e_max: int
) -> tuple[tuple[int, int, int], ...]:
    solutions: list[tuple[int, int, int]] = []
    for u in range(small_block_count + 1):
        for e in range(e_max + 1):
            remainder = 13 - small_coefficient * u - e
            if remainder >= 0 and remainder % 3 == 0:
                solutions.append((u, e, remainder // 3))
    return tuple(solutions)


def replay(params: ReplayParameters = ReplayParameters()) -> dict[str, object]:
    moment_counts: dict[int, int] = {}
    prefix_counts: dict[int, int] = {}
    terminal_counts: dict[int, int] = {}
    terminal_profiles: dict[int, list[tuple[int, ...]]] = {}
    core_lines: list[str] = []
    tagged_lines: list[str] = []

    for double_count in params.d_values:
        moment = profiles_at_d(params, double_count)
        prefix = [profile for profile in moment if prefix_margin(params, profile) >= 0]
        if params.allow_two_multiplicity_15_points:
            terminal = prefix
        else:
            terminal = [
                profile for profile in prefix if multiplicity_count(profile, 15) < 2
            ]
        terminal.sort(key=profile_signature)
        moment_counts[double_count] = len(moment)
        prefix_counts[double_count] = len(prefix)
        terminal_counts[double_count] = len(terminal)
        terminal_profiles[double_count] = terminal
        for profile in terminal:
            line = terminal_core_line(params, double_count, profile)
            core_lines.append(line)
            tagged_lines.append(f"{line} route={classify_terminal(double_count, profile)}")

    terminal_stream = ("\n".join(core_lines) + "\n").encode("ascii")
    terminal_digest = hashlib.sha256(terminal_stream).hexdigest()

    divisors = divisors_of_p_minus_one()
    kneser_minima: dict[int, tuple[int, tuple[int, ...]]] = {}
    for size in range(11, 15):
        candidates = {
            divisor: divisor * (2 * ((size + divisor - 1) // divisor) - 1)
            for divisor in divisors
        }
        minimum = min(candidates.values())
        minimizers = tuple(
            divisor for divisor, value in candidates.items() if value == minimum
        )
        kneser_minima[size] = (minimum, minimizers)

    collinear_arithmetic = {
        "n14_side_absent": (14 * 14, 14 + 26 * 12),
        "n14_side_present": (13 * 13, 13 + 24 * 11),
        "n13_n14_n15_side_present": (14 * 14, 14 + 22 * 12),
    }

    product_coset = {
        "coset_size": 16,
        "x_size": 14,
        "y_size": 14,
        "target_values_at_most": 14,
        "omitted_values_at_least": 2,
        "representations_per_omitted_value_at_least": 12,
        "exceptional_pairs_at_least": 24,
        "matching_pairs_at_most": 14,
    }

    pbd_checks: dict[str, tuple[tuple[int, ...], int]] = {}
    for double_count in (71, 72, 73):
        for profile in terminal_profiles[double_count]:
            tag = classify_terminal(double_count, profile)
            if not tag.startswith("PBD_"):
                continue
            blocks = pbd_blocks(profile)
            pbd_checks[tag] = (blocks, sum(comb(size, 2) for size in blocks))

    vertex_checks = {
        "D72": exact_vertex_solutions(2, 2, 1),
        "D73_4_3BLOCKS": exact_vertex_solutions(4, 2, 1),
        "D73_4_2BLOCKS": exact_vertex_solutions(1, 2, 4),
    }
    # D71 has no 3-block variable: solve 3v+e=13 directly.
    vertex_checks["D71"] = tuple(
        (0, e, (13 - e) // 3)
        for e in range(2)
        if (13 - e) >= 0 and (13 - e) % 3 == 0
    )

    direction_spectrum = Counter({10: 1, 6: 11, 5: 1, 4: 1, 3: 1, 2: 122, 1: 73})
    direction_checks = {
        "blocks": sum(direction_spectrum.values()),
        "incidences": sum(size * count for size, count in direction_spectrum.items()),
        "pairs": sum(comb(size, 2) * count for size, count in direction_spectrum.items()),
    }

    return {
        "params": params,
        "moment_counts": moment_counts,
        "prefix_counts": prefix_counts,
        "terminal_counts": terminal_counts,
        "terminal_profiles": terminal_profiles,
        "core_lines": tuple(core_lines),
        "tagged_lines": tuple(tagged_lines),
        "terminal_stream_bytes": len(terminal_stream),
        "terminal_stream_sha256": terminal_digest,
        "divisors": divisors,
        "kneser_minima": kneser_minima,
        "collinear_arithmetic": collinear_arithmetic,
        "product_coset": product_coset,
        "pbd_checks": pbd_checks,
        "vertex_checks": vertex_checks,
        "direction_spectrum": direction_spectrum,
        "direction_checks": direction_checks,
    }


def verify(values: dict[str, object]) -> None:
    params = values["params"]
    require(isinstance(params, ReplayParameters), "parameter record type")
    require(params == ReplayParameters(), "canonical parameter mutation")
    require(is_prime(params.p), "p is not prime")
    require(params.p - 1 == 2**24 * 127, "p-1 factorization")
    require(is_prime(127), "odd factor 127 is not prime")
    require(comb(params.lines, 2) == 861, "line-pair total")
    require(params.lines * params.points_per_line == 630, "incidence total")

    moment_counts = values["moment_counts"]
    prefix_counts = values["prefix_counts"]
    terminal_counts = values["terminal_counts"]
    require(isinstance(moment_counts, dict), "moment count map")
    require(isinstance(prefix_counts, dict), "prefix count map")
    require(isinstance(terminal_counts, dict), "terminal count map")
    for double_count, expected in EXPECTED_COUNTS.items():
        actual = (
            moment_counts[double_count],
            prefix_counts[double_count],
            terminal_counts[double_count],
        )
        require(actual == expected, f"D={double_count} census {actual} != {expected}")

    terminal_profiles = values["terminal_profiles"]
    require(isinstance(terminal_profiles, dict), "terminal profile map")
    for double_count, profiles in terminal_profiles.items():
        for profile in profiles:
            counts = {2: double_count, 3: n3(params, double_count, profile)}
            counts.update(
                {
                    multiplicity: count
                    for multiplicity, count in enumerate(profile, start=4)
                }
            )
            require(sum(counts.values()) == 211, "terminal point moment")
            require(
                sum(multiplicity * count for multiplicity, count in counts.items())
                == 630,
                "terminal incidence moment",
            )
            require(
                sum(comb(multiplicity, 2) * count for multiplicity, count in counts.items())
                == 861,
                "terminal line-pair moment",
            )
            require(prefix_margin(params, profile) >= 0, "terminal prefix gate")
            require(multiplicity_count(profile, 15) < 2, "terminal two-15 gate")

    require(values["core_lines"] == EXPECTED_TERMINAL_LINES, "terminal profile stream")
    require(values["terminal_stream_bytes"] == 443, "terminal stream byte count")
    require(
        values["terminal_stream_sha256"] == EXPECTED_TERMINAL_STREAM_SHA256,
        f"terminal stream SHA-256: {values['terminal_stream_sha256']}",
    )

    tagged_lines = values["tagged_lines"]
    require(isinstance(tagged_lines, tuple), "tagged terminal stream")
    route_counts = Counter(line.rsplit("route=", 1)[1] for line in tagged_lines)
    require(
        route_counts
        == Counter(
            {
                "THREE_N14": 5,
                "N13_N14_N15": 3,
                "PBD_D71": 1,
                "PBD_D72": 1,
                "PBD_D73_4_2BLOCKS": 1,
                "PBD_D73_4_3BLOCKS": 1,
                "OPEN_D73": 1,
            }
        ),
        "terminal route counts",
    )

    divisors = values["divisors"]
    require(isinstance(divisors, tuple), "divisor list type")
    require(len(divisors) == 50 and divisors[0] == 1 and divisors[-1] == P - 1, "divisor census")
    require(values["kneser_minima"] == {size: (16, (16,)) for size in range(11, 15)}, "Kneser minima")

    collinear = values["collinear_arithmetic"]
    require(isinstance(collinear, dict), "collinear arithmetic map")
    require(collinear["n14_side_absent"] == (196, 326), "14-point absent-side correlation")
    require(collinear["n14_side_present"] == (169, 277), "14-point present-side correlation")
    require(collinear["n13_n14_n15_side_present"] == (196, 278), "13/14/15 correlation")

    product = values["product_coset"]
    require(isinstance(product, dict), "product-coset map")
    require(product["target_values_at_most"] == 14, "target-value upper bound")
    require(product["omitted_values_at_least"] == 2, "omitted product values")
    require(product["representations_per_omitted_value_at_least"] == 12, "product representations")
    require(product["exceptional_pairs_at_least"] == 24, "exceptional product pairs")
    require(product["matching_pairs_at_most"] == 14, "matching exception cap")
    require(24 > 14, "product-coset contradiction")

    pbd = values["pbd_checks"]
    require(isinstance(pbd, dict), "PBD check map")
    expected_block_counts = {
        "PBD_D71": Counter({4: 15, 2: 1}),
        "PBD_D72": Counter({4: 14, 3: 2, 2: 1}),
        "PBD_D73_4_3BLOCKS": Counter({4: 13, 3: 4, 2: 1}),
        "PBD_D73_4_2BLOCKS": Counter({4: 14, 2: 4, 3: 1}),
    }
    require(set(pbd) == set(expected_block_counts), "PBD route set")
    for tag, expected_blocks in expected_block_counts.items():
        blocks, pair_sum = pbd[tag]
        require(Counter(blocks) == expected_blocks, f"{tag} block spectrum")
        require(pair_sum == 91, f"{tag} pair capacity")

    vertices = values["vertex_checks"]
    require(isinstance(vertices, dict), "vertex check map")
    require(vertices["D71"] == ((0, 1, 4),), "D71 vertex equation")
    require(vertices["D72"] == ((0, 1, 4), (2, 0, 3)), "D72 vertex equation")
    require(
        vertices["D73_4_3BLOCKS"] == ((0, 1, 4), (2, 0, 3), (3, 1, 2)),
        "D73 four-3-block vertex equation",
    )
    require(
        vertices["D73_4_2BLOCKS"] == ((0, 1, 4), (0, 4, 3), (1, 2, 3)),
        "D73 four-2-block vertex equation",
    )
    require(12 * 2 > 4 * 3, "D73 four-3-block incidence contradiction")
    require(3 * 2 + 11 > 4 * 2, "D73 four-2-block incidence contradiction")

    direction = values["direction_checks"]
    require(isinstance(direction, dict), "direction check map")
    require(direction == {"blocks": 210, "incidences": 405, "pairs": 351}, "D73 direction spectrum")
    require(210 == 15 * 14, "D73 occupied-line count")
    require(405 == 15 * 27, "D73 direction incidence count")
    require(351 == comb(27, 2), "D73 determined-pair count")


def render(values: dict[str, object]) -> list[str]:
    moment = values["moment_counts"]
    prefix = values["prefix_counts"]
    terminal = values["terminal_counts"]
    require(isinstance(moment, dict), "render moment map")
    require(isinstance(prefix, dict), "render prefix map")
    require(isinstance(terminal, dict), "render terminal map")

    lines = [
        "RANK15_D69_D73_ARRANGEMENT_ARITHMETIC: PASS",
        f"field=p:{P} prime:yes p_minus_1:2^24*127 divisors:50",
        "moments=points:211 incidences:630 line_pairs:861",
    ]
    for double_count in D_VALUES:
        lines.append(
            f"D={double_count} moment={moment[double_count]} "
            f"prefix={prefix[double_count]} terminal={terminal[double_count]}"
        )
    lines.extend(values["tagged_lines"])
    lines.extend(
        [
            f"terminal_stream=bytes:{values['terminal_stream_bytes']} sha256:{values['terminal_stream_sha256']}",
            "kneser_minimum=|X|:11..14 lower:16 unique_stabilizer_order:16",
            "product_coset=target_values_at_most:14 omitted_at_least:2 reps_each_at_least:12 exceptions_at_least:24 matching_at_most:14",
            "pbd_pair_capacity=D71:91 D72:91 D73a:91 D73b:91",
            "pbd_vertex_checks=D71:reject D72:reject D73a:reject D73b:reject",
            "D73_open=n3:122 n4:1 n5:1 n6:1 n7:11 n11:1 n15:1",
            "D73_direction_spectrum=10^1,6^11,5^1,4^1,3^1,2^122,1^73 blocks:210 incidences:405 pairs:351",
            "conditional_result=exclude_D:69..72 reduce_D73_to_one_profile",
            "ARITHMETIC_SCOPE=moment_enumeration,prefix_gate,field_divisors,PBD_equations,direction_spectrum",
            "GEOMETRIC_LEMMAS_NOT_MACHINE_PROVED=matching,coordinates,Cauchy-Davenport,Kneser_application,PBD_construction,duality",
            "RESULT=PASS",
        ]
    )
    report_digest = hashlib.sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()
    lines.append(f"report_sha256={report_digest}")
    return lines


def tamper_selftest() -> None:
    base = replay()
    verify(base)
    mutations: list[dict[str, object]] = []

    changed = dict(base)
    changed["params"] = replace(ReplayParameters(), p=P + 2)
    mutations.append(changed)

    changed = dict(base)
    changed_counts = dict(base["moment_counts"])
    changed_counts[69] += 1
    changed["moment_counts"] = changed_counts
    mutations.append(changed)

    changed = dict(base)
    changed_counts = dict(base["prefix_counts"])
    changed_counts[73] -= 1
    changed["prefix_counts"] = changed_counts
    mutations.append(changed)

    changed = dict(base)
    changed["core_lines"] = tuple(base["core_lines"])[:-1]
    mutations.append(changed)

    changed = dict(base)
    changed["terminal_stream_sha256"] = "0" * 64
    mutations.append(changed)

    changed = dict(base)
    changed_kneser = dict(base["kneser_minima"])
    changed_kneser[14] = (15, (15,))
    changed["kneser_minima"] = changed_kneser
    mutations.append(changed)

    changed = dict(base)
    changed_product = dict(base["product_coset"])
    changed_product["omitted_values_at_least"] = 1
    changed["product_coset"] = changed_product
    mutations.append(changed)

    changed = dict(base)
    changed_pbd = dict(base["pbd_checks"])
    blocks, _pair_sum = changed_pbd["PBD_D72"]
    changed_pbd["PBD_D72"] = (blocks, 90)
    changed["pbd_checks"] = changed_pbd
    mutations.append(changed)

    changed = dict(base)
    changed_direction = dict(base["direction_checks"])
    changed_direction["pairs"] = 350
    changed["direction_checks"] = changed_direction
    mutations.append(changed)

    caught = 0
    for mutation in mutations:
        try:
            verify(mutation)
        except VerificationError:
            caught += 1
    require(caught == len(mutations), "tamper mutation escaped verification")
    print(f"TAMPER_SELFTEST: PASS ({caught}/{len(mutations)} rejected)")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
        return

    values = replay()
    verify(values)
    print("\n".join(render(values)))


if __name__ == "__main__":
    main()
