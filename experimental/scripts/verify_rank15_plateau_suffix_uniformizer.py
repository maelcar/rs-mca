#!/usr/bin/env python3
"""Verify the rank-15 plateau-suffix uniformizer and recurrence impact.

The verifier uses only the Python standard library.  It derives the finite
optimizer from the pair, deficient-point, and six threshold inequalities;
checks the imported chi=8 skeleton interface; evaluates all 397 plateau
states; and replays the literal affine-section recurrence through dimension
15.  It never relies on ``assert``, so optimized Python has identical logic.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from math import comb
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIR = (
    ROOT
    / "experimental/data/certificates/rank15-plateau-suffix-uniformizer"
)
OUTPUT_PATH = CERTIFICATE_DIR / "verifier_output.txt"
CAPACITY_LEDGER_PATH = CERTIFICATE_DIR / "capacity_ledger.txt"
RECURRENCE_LEDGER_PATH = CERTIFICATE_DIR / "recurrence_changes.txt"
FIXTURE_PATH = CERTIFICATE_DIR / "fixture.json"

P_FIELD = 2_130_706_433
N_CODE = 2_097_152
K_CODE = 1_048_576
AGREEMENT = 1_116_047
LIST_SIZE = 218
SECTION_CAP = 15
TARGET = 274_854_110_496_187_592

PLATEAU_LO = 1_043_552
PLATEAU_HI = 1_043_948
PROVED_LO = 1_043_771
PROVED_HI = PLATEAU_HI
RESIDUAL_HI = PROVED_LO - 1

HIGH_OCCUPANCIES = tuple(range(9, 15))
THRESHOLDS = tuple(range(9, 15))
MAX_FULL_NONRICH_DIRECTIONS = 17

EXPECTED_THRESHOLD_COEFFICIENTS = (1, 1, 1, 3, 6, 21)
EXPECTED_BOUNDARY_MARGINS = {
    210: -8_054,
    211: -8_054,
    212: -3_249,
    213: -3_249,
    214: -1_705,
    215: -6_510,
    216: -6_510,
    217: -1_705,
    218: 1_403,
}
EXPECTED_CHI8_SKELETONS = (
    (18, 25, 0, 2, 1, 1),
    (18, 25, 1, 0, 2, 1),
    (18, 25, 1, 1, 0, 5),
    (26, 24, 1, 3, 0, 1),
    (26, 24, 2, 1, 1, 1),
    (26, 24, 3, 0, 0, 5),
    (34, 23, 3, 2, 0, 1),
    (34, 23, 4, 0, 1, 1),
    (42, 22, 5, 1, 0, 1),
    (50, 21, 7, 0, 0, 1),
)


class VerificationError(RuntimeError):
    """Raised when an always-active certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(numerator: int, denominator: int) -> int:
    require(denominator > 0, "ceil_div requires a positive denominator")
    return (numerator + denominator - 1) // denominator


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_text(payload: str) -> str:
    return sha256_bytes(payload.encode("ascii"))


def contiguous_ranges(values: Sequence[int]) -> tuple[tuple[int, int], ...]:
    if not values:
        return ()
    ranges: list[tuple[int, int]] = []
    first = previous = values[0]
    for value in values[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append((first, previous))
        first = previous = value
    ranges.append((first, previous))
    return tuple(ranges)


def format_ranges(ranges: Iterable[tuple[int, int]]) -> str:
    fields = []
    for first, last in ranges:
        fields.append(str(first) if first == last else f"{first}-{last}")
    return ",".join(fields) if fields else "none"


@dataclass(frozen=True, slots=True)
class Profile:
    """Precomputed data for one (n_9,...,n_14) high profile."""

    high_count: int
    incidence: int
    pair_cost: int
    ordered_high_cost: int
    threshold_counts: tuple[int, ...]
    threshold_incidences: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class ThresholdCertificate:
    coefficients: tuple[int, ...]
    witnesses: tuple[int, ...]
    cases_checked: int


@dataclass(frozen=True, slots=True)
class CapacityState:
    u: int
    e: int
    residual_n: int
    residual_a: int
    degree_budget: int
    rich_weight: int
    demand_at_max_degree: int
    minimum_rich_directions: int
    capacities: tuple[tuple[int, int], ...]
    maximum_capacity: int
    maximizing_directions: tuple[int, ...]
    margin: int


@dataclass(frozen=True, slots=True)
class RecurrenceSummary:
    dimension: int
    changed_states: int
    first_changed: int | None
    last_changed: int | None
    maximum_drop: int
    constant_drop_runs: int
    value_runs: int
    base_at_zero: int
    cut_at_zero: int
    row_sha256: str


@dataclass(frozen=True, slots=True)
class RecurrenceResult:
    summaries: tuple[RecurrenceSummary, ...]
    ledger_text: str
    raw_g2_218_ranges: tuple[tuple[int, int], ...]
    raw_g2_219_ranges: tuple[tuple[int, int], ...]


def derive_threshold_certificate() -> ThresholdCertificate:
    coefficients: list[int] = []
    witnesses: list[int] = []
    cases = 0

    for threshold in THRESHOLDS:
        bounds: list[tuple[int, int]] = []
        for multiplicity in range(LIST_SIZE + 1):
            z_value = ceil_div(
                max((threshold - 1) * multiplicity - 7, 0), 14
            )
            denominator = multiplicity - z_value
            if denominator > 0:
                bounds.append(
                    (comb(multiplicity, 2) // denominator, multiplicity)
                )
        require(bounds, f"no finite coefficient bound for H={threshold}")
        coefficient, witness = min(bounds)
        coefficients.append(coefficient)
        witnesses.append(witness)

        tampered_rejected = False
        for multiplicity in range(LIST_SIZE + 1):
            z_value = ceil_div(
                max((threshold - 1) * multiplicity - 7, 0), 14
            )
            lhs = coefficient * (multiplicity - z_value)
            rhs = comb(multiplicity, 2)
            require(lhs <= rhs, f"threshold inequality failed at H={threshold}")
            if (coefficient + 1) * (multiplicity - z_value) > rhs:
                tampered_rejected = True
            cases += 1
        require(tampered_rejected, f"H={threshold} coefficient is not sharp")

    result = ThresholdCertificate(tuple(coefficients), tuple(witnesses), cases)
    require(
        result.coefficients == EXPECTED_THRESHOLD_COEFFICIENTS,
        "derived threshold coefficient tuple changed",
    )
    require(result.cases_checked == 1_314, "threshold case count changed")
    return result


def enumerate_chi8_skeletons() -> tuple[tuple[int, ...], ...]:
    skeletons: list[tuple[int, ...]] = []
    for k7 in range(9):
        for k6 in range(5):
            for k5 in range(3):
                u0 = 8 - k7 - 2 * k6 - 3 * k5
                if u0 < 0:
                    continue
                residual_vertices = 7 * k7 + 6 * k6 + 5 * k5 + u0
                if residual_vertices < 18 or residual_vertices > LIST_SIZE:
                    continue
                if (LIST_SIZE - residual_vertices) % 8 != 0:
                    continue
                removed_k8 = (LIST_SIZE - residual_vertices) // 8
                skeletons.append(
                    (residual_vertices, removed_k8, k7, k6, k5, u0)
                )
    result = tuple(sorted(skeletons))
    require(result == EXPECTED_CHI8_SKELETONS, "chi=8 skeleton interface changed")
    require(
        all(row[-1] in (1, 5) for row in result),
        "chi=8 unassigned counts are not exactly 1 or 5",
    )

    one_unassigned_slack = Fraction(4) - (Fraction(1) + 3 * Fraction(3, 5))
    five_unassigned_slack = (
        Fraction(4) - (Fraction(1) + Fraction(2) + Fraction(3, 5))
    )
    require(one_unassigned_slack == Fraction(6, 5), "u0=1 slack changed")
    require(five_unassigned_slack == Fraction(2, 5), "u0=5 slack changed")
    require(
        min(one_unassigned_slack, five_unassigned_slack) == Fraction(2, 5),
        "uniform chi=8 slack changed",
    )
    return result


def verify_chi8_capacity_arithmetic() -> int:
    """Check the uniform eta bound and the exact d/r optimizer increments."""
    cases = 0
    for u in range(PLATEAU_LO, PLATEAU_HI + 1):
        residual_n = N_CODE - u
        residual_a = AGREEMENT - u
        degree_budget = K_CODE - 1 - u
        demand = residual_a - SECTION_CAP * degree_budget
        if demand <= 0:
            continue

        eta_floor = 8 * demand + ceil_div(2 * demand, 5)
        require(eta_floor <= 10 * demand, "chi>=10 does not dominate chi=8")

        def relaxed_bound(inactive: int, degree: int) -> int:
            local_demand = residual_a - SECTION_CAP * degree
            return (
                8 * (residual_n - inactive)
                + 1_526 * degree
                - 8 * local_demand
                - ceil_div(2 * local_demand, 5)
            )

        maximum = relaxed_bound(0, degree_budget)
        require(
            maximum - relaxed_bound(0, degree_budget - 1) == 1_652,
            "degree optimizer increment changed",
        )
        require(
            maximum - relaxed_bound(1, degree_budget - 1) == 1_660,
            "inactive-root optimizer decrement changed",
        )
        cases += 1

    require(cases == 193, "chi=8 positive-demand state count changed")
    return cases


def build_profiles() -> tuple[tuple[Profile, ...], str]:
    profiles: list[Profile] = []
    vector_digest = hashlib.sha256()

    def add_profile(counts: tuple[int, ...]) -> None:
        vector_digest.update((",".join(map(str, counts)) + "\n").encode("ascii"))
        high_count = sum(counts)
        incidence = sum(h * count for h, count in zip(HIGH_OCCUPANCIES, counts))
        pair_cost = sum(
            comb(h, 2) * count for h, count in zip(HIGH_OCCUPANCIES, counts)
        )
        ordered_high_cost = sum(
            h * (h - 1) * count
            for h, count in zip(HIGH_OCCUPANCIES, counts)
        )
        threshold_counts = tuple(
            sum(count for h, count in zip(HIGH_OCCUPANCIES, counts) if h >= H)
            for H in THRESHOLDS
        )
        threshold_incidences = tuple(
            sum(
                h * count
                for h, count in zip(HIGH_OCCUPANCIES, counts)
                if h >= H
            )
            for H in THRESHOLDS
        )
        profiles.append(
            Profile(
                high_count,
                incidence,
                pair_cost,
                ordered_high_cost,
                threshold_counts,
                threshold_incidences,
            )
        )

    def visit(prefix: tuple[int, ...], remaining: int) -> None:
        if len(prefix) == len(HIGH_OCCUPANCIES) - 1:
            for final_count in range(remaining + 1):
                add_profile(prefix + (final_count,))
            return
        for count in range(remaining + 1):
            visit(prefix + (count,), remaining - count)

    visit((), MAX_FULL_NONRICH_DIRECTIONS)
    expected_count = comb(
        MAX_FULL_NONRICH_DIRECTIONS + len(HIGH_OCCUPANCIES),
        len(HIGH_OCCUPANCIES),
    )
    require(expected_count == 100_947, "stars-and-bars profile count changed")
    require(len(profiles) == expected_count, "high-profile enumeration incomplete")
    return tuple(profiles), vector_digest.hexdigest()


def low_full_occupancy(direction_count: int, pair_budget: int) -> int:
    """Optimize occupancies 1..8 for equal full-weight directions."""
    require(direction_count >= 0 and pair_budget >= 0, "invalid low optimizer input")
    occupancy = direction_count
    for upgrade_cost in range(1, 8):
        upgrades = min(direction_count, pair_budget // upgrade_cost)
        occupancy += upgrades
        pair_budget -= upgrades * upgrade_cost
        if upgrades < direction_count:
            break
    return occupancy


def verify_low_optimizer() -> int:
    max_budget = 9 * comb(8, 2)
    cases = 0
    for direction_count in range(10):
        exact = [-1] * (max_budget + 1)
        exact[0] = 0
        for _ in range(direction_count):
            updated = [-1] * (max_budget + 1)
            for spent, value in enumerate(exact):
                if value < 0:
                    continue
                for occupancy in range(1, 9):
                    next_spent = spent + comb(occupancy, 2)
                    if next_spent <= max_budget:
                        updated[next_spent] = max(
                            updated[next_spent], value + occupancy
                        )
            exact = updated
        running = -1
        for budget in range(max_budget + 1):
            running = max(running, exact[budget])
            require(
                low_full_occupancy(direction_count, budget) == running,
                f"low optimizer mismatch at count={direction_count}, budget={budget}",
            )
            cases += 1
    require(cases == 2_530, "low-optimizer DP case count changed")
    return cases


class CapacityOptimizer:
    """Exact finite optimizer for the relaxed direction-weight capacity."""

    def __init__(
        self,
        profiles: tuple[Profile, ...],
        threshold: ThresholdCertificate,
    ) -> None:
        self.profiles = profiles
        self.threshold = threshold
        self._candidate_cache: dict[
            tuple[int, int, bool], tuple[tuple[int, int], ...]
        ] = {}

    def _pattern_candidates(
        self, rich_directions: int, full_directions: int, has_residual: bool
    ) -> tuple[tuple[int, int], ...]:
        key = (rich_directions, full_directions, has_residual)
        cached = self._candidate_cache.get(key)
        if cached is not None:
            return cached

        pair_budget = comb(LIST_SIZE, 2) - rich_directions * comb(SECTION_CAP, 2)
        ordered_high_budget = 315 * (LIST_SIZE - rich_directions)
        residual_occupancies = range(1, SECTION_CAP) if has_residual else (0,)
        best_full_incidence: dict[int, int] = {}

        for profile in self.profiles:
            if profile.high_count > full_directions:
                continue
            low_count = full_directions - profile.high_count
            for residual_occupancy in residual_occupancies:
                residual_pair_cost = comb(residual_occupancy, 2)
                spent_pairs = profile.pair_cost + residual_pair_cost
                if spent_pairs > pair_budget:
                    continue
                ordered_cost = profile.ordered_high_cost
                if residual_occupancy >= 9:
                    ordered_cost += residual_occupancy * (residual_occupancy - 1)
                if ordered_cost > ordered_high_budget:
                    continue

                feasible = True
                for index, (H, coefficient) in enumerate(
                    zip(THRESHOLDS, self.threshold.coefficients)
                ):
                    line_count = profile.threshold_counts[index]
                    incidence = profile.threshold_incidences[index]
                    if residual_occupancy >= H:
                        line_count += 1
                        incidence += residual_occupancy
                    lhs = coefficient * incidence - comb(line_count, 2)
                    rhs = 15 * coefficient * (LIST_SIZE - rich_directions)
                    if lhs > rhs:
                        feasible = False
                        break
                if not feasible:
                    continue

                remaining_pairs = pair_budget - spent_pairs
                full_incidence = profile.incidence + low_full_occupancy(
                    low_count, remaining_pairs
                )
                previous = best_full_incidence.get(residual_occupancy, -1)
                if full_incidence > previous:
                    best_full_incidence[residual_occupancy] = full_incidence

        require(best_full_incidence, f"empty capacity pattern for {key}")
        candidates = tuple(sorted((value, h) for h, value in best_full_incidence.items()))
        self._candidate_cache[key] = candidates
        return candidates

    def generic_capacity(
        self,
        residual_n: int,
        degree_budget: int,
        rich_directions: int,
    ) -> int:
        rich_weight_capacity = rich_directions * degree_budget
        if rich_weight_capacity >= residual_n:
            return SECTION_CAP * residual_n

        remaining_weight = residual_n - rich_weight_capacity
        full_directions, residual_weight = divmod(remaining_weight, degree_budget)
        require(
            full_directions <= MAX_FULL_NONRICH_DIRECTIONS,
            "deployed optimizer exceeded the enumerated full-direction bound",
        )
        candidates = self._pattern_candidates(
            rich_directions, full_directions, residual_weight > 0
        )
        nonrich = max(
            degree_budget * full_incidence + residual_weight * residual_occupancy
            for full_incidence, residual_occupancy in candidates
        )
        return SECTION_CAP * rich_weight_capacity + nonrich

    def capacity(
        self,
        residual_n: int,
        residual_a: int,
        degree_budget: int,
        rich_directions: int,
    ) -> int:
        capacity = self.generic_capacity(
            residual_n, degree_budget, rich_directions
        )
        demand = residual_a - SECTION_CAP * degree_budget
        if rich_directions == LIST_SIZE and demand > 0:
            chi8_capacity = (
                8 * residual_n
                + 1_526 * degree_budget
                - 8 * demand
                - ceil_div(2 * demand, 5)
            )
            capacity = min(capacity, chi8_capacity)
        return capacity


def build_capacity_states(
    optimizer: CapacityOptimizer,
) -> tuple[CapacityState, ...]:
    states: list[CapacityState] = []
    for u in range(PLATEAU_LO, PLATEAU_HI + 1):
        residual_n = N_CODE - u
        residual_a = AGREEMENT - u
        degree_budget = K_CODE - 1 - u
        e = 1_045_969 - u
        rich_weight = LIST_SIZE * residual_a - 14 * residual_n
        demand = residual_a - SECTION_CAP * degree_budget

        require(residual_n == e + 1_051_183, "N/e identity changed")
        require(residual_a == e + 70_078, "a/e identity changed")
        require(degree_budget == e + 2_606, "lambda/e identity changed")
        require(rich_weight == 204 * e + 560_442, "W/e identity changed")
        require(
            SECTION_CAP * residual_n - LIST_SIZE * residual_a
            == 490_741 - 203 * e,
            "Delta/e identity changed",
        )

        minimum_t = ceil_div(rich_weight, degree_budget)
        require(210 <= minimum_t <= 211, "unexpected rich-direction floor")
        capacities = tuple(
            (
                rich_directions,
                optimizer.capacity(
                    residual_n,
                    residual_a,
                    degree_budget,
                    rich_directions,
                ),
            )
            for rich_directions in range(minimum_t, LIST_SIZE + 1)
        )
        maximum = max(value for _, value in capacities)
        maximizing = tuple(t for t, value in capacities if value == maximum)
        margin = maximum - LIST_SIZE * residual_a
        states.append(
            CapacityState(
                u,
                e,
                residual_n,
                residual_a,
                degree_budget,
                rich_weight,
                demand,
                minimum_t,
                capacities,
                maximum,
                maximizing,
                margin,
            )
        )

    require(len(states) == 397, "plateau state count changed")
    by_u = {state.u: state for state in states}
    require(
        all(by_u[u].margin >= 0 for u in range(PLATEAU_LO, RESIDUAL_HI + 1)),
        "optimizer unexpectedly excludes a claimed residual state",
    )
    require(
        all(by_u[u].margin < 0 for u in range(PROVED_LO, PROVED_HI + 1)),
        "optimizer does not exclude the full proved suffix",
    )

    boundary = by_u[RESIDUAL_HI]
    boundary_margins = {
        t: value - LIST_SIZE * boundary.residual_a for t, value in boundary.capacities
    }
    require(
        boundary_margins == EXPECTED_BOUNDARY_MARGINS,
        "first residual t-margin vector changed",
    )
    require(
        (boundary.residual_n, boundary.residual_a, boundary.degree_budget)
        == (1_053_382, 72_277, 4_805),
        "first residual state arithmetic changed",
    )
    require(boundary.demand_at_max_degree == 202, "boundary demand changed")
    require(
        boundary.maximum_capacity == 15_757_789 and boundary.margin == 1_403,
        "first residual capacity changed",
    )

    first_proved = by_u[PROVED_LO]
    require(
        first_proved.maximum_capacity == 15_756_137
        and first_proved.margin == -31,
        "first proved capacity changed",
    )
    right_endpoint = by_u[PROVED_HI]
    require(
        right_endpoint.maximum_capacity == 15_569_720
        and right_endpoint.margin == -147_862,
        "right-endpoint capacity changed",
    )
    return tuple(states)


def capacity_ledger_text(states: tuple[CapacityState, ...]) -> str:
    lines = [
        "# rank15 plateau-suffix capacity ledger v1",
        "# Every row is derived from the exact profile optimizer.",
        "# t-columns are capacity:margin, with margin = capacity - 218*a; NA means t<W/lambda.",
        "u\te\tN\ta\tlambda\tW\tc0\tt_min\t"
        + "\t".join(f"t{t}" for t in range(210, 219))
        + "\tC\targmax_t\tmargin\tclassification",
    ]
    for state in states:
        target = LIST_SIZE * state.residual_a
        by_t = dict(state.capacities)
        t_fields = []
        for t in range(210, 219):
            if t not in by_t:
                t_fields.append("NA")
            else:
                t_fields.append(f"{by_t[t]}:{by_t[t] - target}")
        classification = "PROVED_M_LE_217" if state.margin < 0 else "RESIDUAL_M218"
        lines.append(
            "\t".join(
                [
                    str(state.u),
                    str(state.e),
                    str(state.residual_n),
                    str(state.residual_a),
                    str(state.degree_budget),
                    str(state.rich_weight),
                    str(state.demand_at_max_degree),
                    str(state.minimum_rich_directions),
                    *t_fields,
                    str(state.maximum_capacity),
                    ",".join(map(str, state.maximizing_directions)),
                    str(state.margin),
                    classification,
                ]
            )
        )
    return "\n".join(lines) + "\n"


def johnson_bound(u: int) -> int | None:
    residual_n = N_CODE - u
    residual_a = AGREEMENT - u
    determinant = residual_a * residual_a - residual_n * (K_CODE - 1 - u)
    if determinant <= 0:
        return None
    return residual_n * (AGREEMENT - K_CODE + 1) // determinant


def row_runs(
    base: list[int], cut: list[int], upper: int
) -> tuple[tuple[int, int, int, int], ...]:
    require(upper >= 0, "negative recurrence row upper endpoint")
    runs: list[tuple[int, int, int, int]] = []
    first = 0
    base_value = base[0]
    cut_value = cut[0]
    for u in range(1, upper + 1):
        if base[u] == base_value and cut[u] == cut_value:
            continue
        runs.append((first, u - 1, base_value, cut_value))
        first = u
        base_value = base[u]
        cut_value = cut[u]
    runs.append((first, upper, base_value, cut_value))
    return tuple(runs)


def replay_recurrence() -> RecurrenceResult:
    base_previous = [1] * (K_CODE + 2)
    cut_previous = [1] * (K_CODE + 2)
    summaries: list[RecurrenceSummary] = []
    ledger_lines = [
        "# rank15 plateau-suffix recurrence ledger v1",
        "# Lossless run-length encoding of every (F_base_d(u),F_cut_d(u)) pair.",
        "# Each run is inclusive: run u_first u_last base cut drop.",
    ]
    raw_g2_218: list[int] = []
    raw_g2_219: list[int] = []

    for dimension in range(1, 16):
        upper = K_CODE - dimension
        base_current = [0] * (K_CODE + 2)
        cut_current = [0] * (K_CODE + 2)
        base_suffix = 0
        cut_suffix = 0

        for u in range(upper, -1, -1):
            base_candidate = (
                (N_CODE - u) * base_previous[u + 1] // (AGREEMENT - u)
            )
            cut_candidate = (
                (N_CODE - u) * cut_previous[u + 1] // (AGREEMENT - u)
            )
            johnson = johnson_bound(u)
            if johnson is not None:
                base_candidate = min(base_candidate, johnson)
                cut_candidate = min(cut_candidate, johnson)

            if dimension == 2 and PLATEAU_LO <= u <= PLATEAU_HI:
                if base_candidate == 218:
                    raw_g2_218.append(u)
                elif base_candidate == 219:
                    raw_g2_219.append(u)
                else:
                    raise VerificationError(f"unexpected raw G2 value at u={u}")
            if dimension == 2 and PROVED_LO <= u <= PROVED_HI:
                cut_candidate = min(cut_candidate, 217)

            base_suffix = max(base_suffix, base_candidate)
            cut_suffix = max(cut_suffix, cut_candidate)
            base_current[u] = base_suffix
            cut_current[u] = cut_suffix

        if dimension == 1:
            require(base_current[0] == cut_current[0] == 15, "dimension-one row changed")
        else:
            changed = [
                u for u in range(upper + 1) if base_current[u] != cut_current[u]
            ]
            changed_ranges = contiguous_ranges(changed)
            require(
                len(changed_ranges) == 1,
                f"dimension {dimension} changed set is not contiguous",
            )
            drops = [base_current[u] - cut_current[u] for u in changed]
            constant_drop_runs = 1
            for left, right in zip(drops, drops[1:]):
                if left != right:
                    constant_drop_runs += 1

            runs = row_runs(base_current, cut_current, upper)
            run_lines = [
                f"run {first} {last} {base_value} {cut_value} {base_value - cut_value}"
                for first, last, base_value, cut_value in runs
            ]
            row_hash = sha256_text("\n".join(run_lines) + "\n")
            summary = RecurrenceSummary(
                dimension,
                len(changed),
                changed[0],
                changed[-1],
                max(drops),
                constant_drop_runs,
                len(runs),
                base_current[0],
                cut_current[0],
                row_hash,
            )
            summaries.append(summary)
            ledger_lines.append(
                "summary "
                f"d={dimension} changed={len(changed)} "
                f"range={changed[0]}-{changed[-1]} max_drop={max(drops)} "
                f"drop_runs={constant_drop_runs} value_runs={len(runs)} "
                f"F_base_0={base_current[0]} F_cut_0={cut_current[0]} "
                f"row_sha256={row_hash}"
            )
            ledger_lines.extend(run_lines)
            ledger_lines.append("end")

        base_previous = base_current
        cut_previous = cut_current

    expected_rows = (
        (2, 1_043_949, 0, 1_043_948, 2, 3, 219, 218),
        (3, 1_043_617, 0, 1_043_616, 15, 1, 3_185, 3_170),
        (4, 1_043_594, 0, 1_043_593, 218, 1, 46_313, 46_095),
        (5, 1_043_593, 0, 1_043_592, 3_170, 1, 673_432, 670_262),
        (6, 1_043_592, 0, 1_043_591, 46_094, 1, 9_792_173, 9_746_079),
        (7, 1_043_591, 0, 1_043_590, 670_230, 1, 142_383_225, 141_712_995),
        (8, 1_043_590, 0, 1_043_589, 9_745_363, 1, 2_070_298_623, 2_060_553_260),
        (9, 1_043_589, 0, 1_043_588, 141_698_942, 1, 30_102_431_698, 29_960_732_756),
        (10, 1_043_588, 0, 1_043_587, 2_060_295_968, 1, 437_687_944_409, 435_627_648_441),
        (11, 1_043_587, 0, 1_043_586, 29_956_221_716, 1, 6_363_880_388_611, 6_333_924_166_895),
        (12, 1_043_586, 0, 1_043_585, 435_550_863_137, 1, 92_528_143_984_263, 92_092_593_121_126),
        (13, 1_043_585, 0, 1_043_584, 6_332_644_960_511, 1, 1_345_303_004_308_571, 1_338_970_359_348_060),
        (14, 1_043_584, 0, 1_043_583, 92_071_627_544_720, 1, 19_559_637_074_221_362, 19_467_565_446_676_642),
        (15, 1_043_583, 0, 1_043_582, 1_338_631_127_196_448, 1, 284_377_931_860_724_492, 283_039_300_733_528_044),
    )
    actual_rows = tuple(
        (
            row.dimension,
            row.changed_states,
            row.first_changed,
            row.last_changed,
            row.maximum_drop,
            row.constant_drop_runs,
            row.base_at_zero,
            row.cut_at_zero,
        )
        for row in summaries
    )
    require(actual_rows == expected_rows, "recurrence summary rows changed")

    raw_218_ranges = contiguous_ranges(sorted(raw_g2_218))
    raw_219_ranges = contiguous_ranges(sorted(raw_g2_219))
    require(
        raw_218_ranges
        == ((1_043_552, 1_043_906), (1_043_948, 1_043_948)),
        "raw G2=218 ranges changed",
    )
    require(
        raw_219_ranges == ((1_043_907, 1_043_947),),
        "raw G2=219 range changed",
    )
    return RecurrenceResult(
        tuple(summaries),
        "\n".join(ledger_lines) + "\n",
        raw_218_ranges,
        raw_219_ranges,
    )


def build_fixture(
    threshold: ThresholdCertificate,
    profile_count: int,
    profiles_sha256: str,
    chi8_skeletons: tuple[tuple[int, ...], ...],
    states: tuple[CapacityState, ...],
    capacity_sha256: str,
    recurrence: RecurrenceResult,
    recurrence_sha256: str,
    verifier_sha256: str,
    low_dp_cases: int,
    chi8_arithmetic_cases: int,
) -> dict[str, object]:
    by_u = {state.u: state for state in states}
    boundary = by_u[RESIDUAL_HI]
    first_proved = by_u[PROVED_LO]
    right = by_u[PROVED_HI]
    return {
        "schema": "rank15-plateau-suffix-uniformizer-v1",
        "status": "PROVED_SOURCE_VALID_THEOREM_WITH_UNPROVED_LEAN_TARGET",
        "parameters": {
            "p": P_FIELD,
            "n": N_CODE,
            "K": K_CODE,
            "m": AGREEMENT,
            "M": LIST_SIZE,
            "q": SECTION_CAP,
            "effective_recurrence_c": 0,
        },
        "imported_dependency": {
            "pending_pr": 746,
            "graph_cost_floor": 8,
            "chi8_skeletons": chi8_skeletons,
            "skeleton_count": len(chi8_skeletons),
        },
        "optimizer": {
            "threshold_coefficients": threshold.coefficients,
            "threshold_witnesses": threshold.witnesses,
            "threshold_cases": threshold.cases_checked,
            "high_profiles": profile_count,
            "high_profiles_sha256": profiles_sha256,
            "low_optimizer_dp_cases": low_dp_cases,
            "chi8_arithmetic_cases": chi8_arithmetic_cases,
            "states": len(states),
        },
        "theorem": {
            "proved_u_interval": [PROVED_LO, PROVED_HI],
            "proved_state_count": PROVED_HI - PROVED_LO + 1,
            "ceiling": 217,
            "residual_u_interval": [PLATEAU_LO, RESIDUAL_HI],
            "residual_state_count": RESIDUAL_HI - PLATEAU_LO + 1,
            "both_divisorial_branches": True,
        },
        "capacity_anchors": {
            str(boundary.u): {
                "capacity": boundary.maximum_capacity,
                "margin": boundary.margin,
                "t_margins": EXPECTED_BOUNDARY_MARGINS,
                "r": 0,
                "d": boundary.degree_budget,
                "budget_7delta_plus_eta": 3_100,
            },
            str(first_proved.u): {
                "capacity": first_proved.maximum_capacity,
                "margin": first_proved.margin,
            },
            str(right.u): {
                "capacity": right.maximum_capacity,
                "margin": right.margin,
            },
        },
        "recurrence": [
            {
                "dimension": row.dimension,
                "changed_states": row.changed_states,
                "first_changed": row.first_changed,
                "last_changed": row.last_changed,
                "maximum_drop": row.maximum_drop,
                "constant_drop_runs": row.constant_drop_runs,
                "value_runs": row.value_runs,
                "base_at_zero": row.base_at_zero,
                "cut_at_zero": row.cut_at_zero,
                "row_sha256": row.row_sha256,
            }
            for row in recurrence.summaries
        ],
        "target": {
            "value": TARGET,
            "baseline_gap": 9_523_821_364_536_900,
            "cut_gap": 8_185_190_237_340_452,
        },
        "artifact_sha256": {
            "verifier": verifier_sha256,
            "capacity_ledger": capacity_sha256,
            "recurrence_ledger": recurrence_sha256,
        },
        "nonclaims": {
            "residual_M218_states": 219,
            "rank_at_least_16_remains": True,
            "grand_list_solved": False,
            "grand_mca_solved": False,
            "official_score": "0/2",
        },
    }


def build_output(
    threshold: ThresholdCertificate,
    profile_count: int,
    profiles_sha256: str,
    chi8_skeletons: tuple[tuple[int, ...], ...],
    states: tuple[CapacityState, ...],
    recurrence: RecurrenceResult,
    verifier_sha256: str,
    capacity_sha256: str,
    recurrence_sha256: str,
    fixture_sha256: str,
    low_dp_cases: int,
    chi8_arithmetic_cases: int,
) -> str:
    by_u = {state.u: state for state in states}
    boundary = by_u[RESIDUAL_HI]
    lines = [
        "RANK15_PLATEAU_SUFFIX_UNIFORMIZER: PASS",
        f"field: p={P_FIELD}; positive_characteristic={P_FIELD > LIST_SIZE}",
        "optimization_safe: explicit failures; no optimization-dependent checks",
        f"high_profiles_checked: {profile_count}",
        f"high_profiles_sha256: {profiles_sha256}",
        f"threshold_cases_checked: {threshold.cases_checked}",
        "threshold_coefficients: "
        + ",".join(
            f"H{H}={coefficient}"
            for H, coefficient in zip(THRESHOLDS, threshold.coefficients)
        ),
        "threshold_sharp_witnesses: "
        + ",".join(
            f"H{H}:r={witness}"
            for H, witness in zip(THRESHOLDS, threshold.witnesses)
        ),
        f"low_optimizer_literal_dp_cases: {low_dp_cases}",
        f"imported_pr746_chi8_skeletons: {len(chi8_skeletons)}",
        "chi8_unassigned_slack: at_least=2/5_per_required_incidence",
        f"chi8_refinement_states_checked: {chi8_arithmetic_cases}",
        f"plateau: {PLATEAU_LO}-{PLATEAU_HI}; states={len(states)}",
        "raw_G2_218: "
        f"{format_ranges(recurrence.raw_g2_218_ranges)}; states=356",
        "raw_G2_219: "
        f"{format_ranges(recurrence.raw_g2_219_ranges)}; states=41",
        f"proved_M_le_217: {PROVED_LO}-{PROVED_HI}; states=178",
        f"residual_M218_states: {PLATEAU_LO}-{RESIDUAL_HI}; states=219",
    ]
    for u in (RESIDUAL_HI, PROVED_LO, PROVED_HI):
        state = by_u[u]
        lines.append(
            f"capacity_boundary[{u}]: capacity={state.maximum_capacity}; margin={state.margin}"
        )
    boundary_target = LIST_SIZE * boundary.residual_a
    margins = {
        t: value - boundary_target for t, value in boundary.capacities
    }
    lines.append(
        f"first_residual_t_margins[{RESIDUAL_HI}]: "
        + ",".join(f"t{t}={margins[t]}" for t in sorted(margins))
    )
    lines.append("recurrence_change_summaries:")
    for row in recurrence.summaries:
        lines.append(
            "  "
            f"d={row.dimension}; changed_states={row.changed_states}; "
            f"first={row.first_changed}; last={row.last_changed}; "
            f"max_drop={row.maximum_drop}; runs={row.constant_drop_runs}; "
            f"F_base_0={row.base_at_zero}; F_cut_0={row.cut_at_zero}"
        )
    row14 = recurrence.summaries[-2]
    row15 = recurrence.summaries[-1]
    lines.extend(
        [
            f"F14_base_0={row14.base_at_zero}; F14_cut_0={row14.cut_at_zero}",
            f"F15_base_0={row15.base_at_zero}; F15_cut_0={row15.cut_at_zero}",
            f"target={TARGET}; baseline_gap={row15.base_at_zero - TARGET}; cut_gap={row15.cut_at_zero - TARGET}",
            "tamper_controls: threshold+1, low-DP mismatch, interval off-by-one, "
            "chi8 slack, recurrence baseline PASS",
            f"verifier_sha256: {verifier_sha256}",
            f"capacity_ledger_sha256: {capacity_sha256}",
            f"recurrence_ledger_sha256: {recurrence_sha256}",
            f"fixture_sha256: {fixture_sha256}",
            "nonclaims: residual_M218=219; rank_ge_16=OPEN; Grand_List=OPEN; "
            "Grand_MCA=OPEN; score=0/2",
        ]
    )
    return "\n".join(lines) + "\n"


def require_frozen(path: Path, expected: str) -> None:
    require(path.is_file(), f"missing frozen artifact: {path}")
    actual = path.read_bytes()
    require(
        actual == expected.encode("ascii"),
        f"frozen artifact differs: {path}",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="write the four deterministic certificate artifacts",
    )
    args = parser.parse_args()

    require(P_FIELD == 2**31 - 2**24 + 1, "field formula changed")
    require(P_FIELD > LIST_SIZE, "positive-characteristic gate failed")
    require(21 * 15 == 315, "deficient-point coefficient changed")
    require(7 * LIST_SIZE == 1_526, "t=218 incidence coefficient changed")

    threshold = derive_threshold_certificate()
    chi8_skeletons = enumerate_chi8_skeletons()
    chi8_arithmetic_cases = verify_chi8_capacity_arithmetic()
    profiles, profiles_sha256 = build_profiles()
    low_dp_cases = verify_low_optimizer()
    optimizer = CapacityOptimizer(profiles, threshold)
    states = build_capacity_states(optimizer)
    capacity_text = capacity_ledger_text(states)
    capacity_sha256 = sha256_text(capacity_text)

    recurrence = replay_recurrence()
    recurrence_sha256 = sha256_text(recurrence.ledger_text)
    verifier_sha256 = sha256_bytes(Path(__file__).read_bytes())

    fixture = build_fixture(
        threshold,
        len(profiles),
        profiles_sha256,
        chi8_skeletons,
        states,
        capacity_sha256,
        recurrence,
        recurrence_sha256,
        verifier_sha256,
        low_dp_cases,
        chi8_arithmetic_cases,
    )
    fixture_text = json.dumps(
        fixture, sort_keys=True, indent=2, ensure_ascii=True
    ) + "\n"
    fixture_sha256 = sha256_text(fixture_text)
    output_text = build_output(
        threshold,
        len(profiles),
        profiles_sha256,
        chi8_skeletons,
        states,
        recurrence,
        verifier_sha256,
        capacity_sha256,
        recurrence_sha256,
        fixture_sha256,
        low_dp_cases,
        chi8_arithmetic_cases,
    )

    if args.write:
        CERTIFICATE_DIR.mkdir(parents=True, exist_ok=True)
        CAPACITY_LEDGER_PATH.write_text(capacity_text, encoding="ascii")
        RECURRENCE_LEDGER_PATH.write_text(
            recurrence.ledger_text, encoding="ascii"
        )
        FIXTURE_PATH.write_text(fixture_text, encoding="ascii")
        OUTPUT_PATH.write_text(output_text, encoding="ascii")
    else:
        require_frozen(CAPACITY_LEDGER_PATH, capacity_text)
        require_frozen(RECURRENCE_LEDGER_PATH, recurrence.ledger_text)
        require_frozen(FIXTURE_PATH, fixture_text)
        require_frozen(OUTPUT_PATH, output_text)

    print(output_text, end="")


if __name__ == "__main__":
    main()
