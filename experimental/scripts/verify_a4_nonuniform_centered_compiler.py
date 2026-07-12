#!/usr/bin/env python3
"""Verify the A4 nonuniform live-fiber centered compiler packet."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import resource
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any


SCHEMA = "a4_nonuniform_centered_compiler.v1"
STATUS = "PROVED_NONUNIFORM_PAIRWISE_CENTERED_COMPILER"
BASE_COMMIT = "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532"
PARENT_COMMIT = "0aee8592065efacedc9f71679e6eda4f704f2469"
CAP_BYTES = 1024**3
NOTE_PATH = Path(
    "experimental/notes/thresholds/a4_nonuniform_centered_compiler.md"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_a4_nonuniform_centered_compiler.py"
)
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/a4-nonuniform-centered-compiler/"
    "a4_nonuniform_centered_compiler.json"
)
SOURCE_HASHES = {
    "experimental/asymptotic_rs_mca_frontiers.tex":
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
    "experimental/notes/thresholds/a4_quotient_major_compiler.md":
        "4b924af30dc444ab770620cede6895fca47674e64e97d519ecbfa83bd6939222",
    "experimental/notes/thresholds/"
    "a4_trace_quotient_rank_centered_compiler.md":
        "1a0a8df519e9e5e5c4b1738ae1d7639d93c38eb88b002351c53130fa97959cd1",
    "experimental/scripts/"
    "verify_a4_trace_quotient_rank_centered_compiler.py":
        "f8dd982e794c9f02303f6b2f5b002fe34b4ea50a3e2e9b84f07eea8285c7d56f",
    "experimental/data/certificates/a4-trace-quotient-rank-centered/"
    "a4_trace_quotient_rank_centered_compiler.json":
        "9163def59f268a4a5759c0cc1fe55d5935d179bbf701aa43c8363a553bc8b6fe",
}


class CheckFailure(AssertionError):
    """Raised when an exact gate fails."""


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, label: str) -> None:
        if not condition:
            raise CheckFailure(label)
        self.count += 1

    def equal(self, left: Any, right: Any, label: str) -> None:
        self.require(left == right, f"{label}: {left!r} != {right!r}")

    def close(
        self, left: float, right: float, tolerance: float, label: str
    ) -> None:
        self.require(
            math.isfinite(left)
            and math.isfinite(right)
            and abs(left - right) <= tolerance,
            f"{label}: {left!r} not within {tolerance} of {right!r}",
        )


def impose_cap(checks: Checks) -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    target = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    checks.require(target <= CAP_BYTES, "address-space cap")
    return target


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise CheckFailure("repository root not found")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def payload_hash(artifact: dict[str, Any]) -> str:
    payload = copy.deepcopy(artifact)
    payload.pop("payload_sha256", None)
    return hashlib.sha256(canonical(payload)).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def margin_text(value: float) -> str:
    if abs(value) <= 1e-12:
        value = 0.0
    return format(value, ".12g")


def character_value(element: int, character: int) -> int:
    return -1 if (element & character).bit_count() % 2 else 1


def subset_sum_counts(
    values: list[int], weight: int, group_size: int
) -> list[int]:
    counts = [0] * group_size
    for subset in combinations(range(len(values)), weight):
        total = 0
        for index in subset:
            total ^= values[index]
        counts[total] += 1
    return counts


def character_sum(counts: list[int], character: int) -> int:
    return sum(
        multiplicity * character_value(element, character)
        for element, multiplicity in enumerate(counts)
    )


def centered_eta_for_values(
    values: list[int], weight: int, group_size: int
) -> Fraction:
    counts = subset_sum_counts(values, weight, group_size)
    m_value = math.comb(len(values), weight)
    return Fraction(
        group_size * sum(count * count for count in counts),
        m_value * m_value,
    ) - 1


def normalized_nontrivial_l1(
    values: list[int], weight: int, group_size: int
) -> Fraction:
    coefficients = [
        elementary_coeff(
            [character_value(element, character) for element in values],
            weight,
        )
        for character in range(group_size)
    ]
    return Fraction(
        sum(abs(value) for value in coefficients[1:]),
        math.comb(len(values), weight),
    )


def elementary_coeff(values: list[int], weight: int) -> int:
    coefficients = [0] * (weight + 1)
    coefficients[0] = 1
    degree = 0
    for value in values:
        degree = min(weight, degree + 1)
        for index in range(degree, 0, -1):
            coefficients[index] += value * coefficients[index - 1]
    return coefficients[weight]


def polynomial(values: list[int]) -> list[int]:
    coefficients = [1]
    for value in values:
        next_coefficients = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            next_coefficients[index] += coefficient
            next_coefficients[index + 1] += value * coefficient
        coefficients = next_coefficients
    return coefficients


def class_data(
    checks: Checks,
    *,
    profile_name: str,
    multiplicity: int,
    rank: int,
    values: list[int],
) -> tuple[dict[str, Any], dict[str, Any]]:
    group_size = 2**rank
    checks.require(bool(values), f"{profile_name}: class nonempty")
    checks.require(
        all(0 <= value < group_size for value in values),
        f"{profile_name}: class values s={multiplicity}",
    )
    n = len(values)
    m_values = [math.comb(n, weight) for weight in range(n + 1)]
    eta: list[Fraction] = []
    e_by_weight: list[list[int]] = []
    sp_values: list[int] = []
    for weight, m_value in enumerate(m_values):
        counts = subset_sum_counts(values, weight, group_size)
        sp = sum(count * count for count in counts)
        centered = Fraction(group_size * sp, m_value * m_value) - 1
        checks.require(
            Fraction(0) <= centered <= group_size - 1,
            f"{profile_name}: eta range s={multiplicity} j={weight}",
        )
        e_values = [
            character_sum(counts, character)
            for character in range(group_size)
        ]
        checks.equal(
            Fraction(sum(value * value for value in e_values[1:]), 1),
            centered * m_value * m_value,
            f"{profile_name}: centered Parseval s={multiplicity} j={weight}",
        )
        eta.append(centered)
        e_by_weight.append(e_values)
        sp_values.append(sp)
    checks.equal(
        eta[0],
        Fraction(group_size - 1),
        f"{profile_name}: zero endpoint s={multiplicity}",
    )
    checks.equal(
        eta[-1],
        Fraction(group_size - 1),
        f"{profile_name}: full endpoint s={multiplicity}",
    )
    internal = {
        "n": n,
        "m_values": m_values,
        "eta": eta,
        "e_by_weight": e_by_weight,
    }
    record = {
        "multiplicity": multiplicity,
        "quotient_points": n,
        "values": values,
        "m_values": m_values,
        "sp_values": sp_values,
        "eta": [fraction_text(value) for value in eta],
    }
    return internal, record


def profile_case(
    checks: Checks,
    *,
    name: str,
    rank: int,
    classes: dict[int, list[int]],
) -> dict[str, Any]:
    group_size = 2**rank
    active = sorted(multiplicity for multiplicity, values in classes.items() if values)
    checks.require(bool(active), f"{name}: active classes")
    checks.require(all(value > 0 for value in active), f"{name}: positive multiplicities")
    d_star = sum(active)
    live_size = sum(multiplicity * len(classes[multiplicity]) for multiplicity in active)
    slots = [
        (multiplicity, copy_index)
        for multiplicity in active
        for copy_index in range(multiplicity)
    ]
    checks.equal(len(slots), d_star, f"{name}: slot count")

    internal: dict[int, dict[str, Any]] = {}
    class_records: list[dict[str, Any]] = []
    for multiplicity in active:
        data, record = class_data(
            checks,
            profile_name=name,
            multiplicity=multiplicity,
            rank=rank,
            values=classes[multiplicity],
        )
        internal[multiplicity] = data
        class_records.append(record)

    ranges = [
        range(internal[multiplicity]["n"] + 1)
        for multiplicity, _ in slots
    ]
    allocations = list(product(*ranges))
    expanded_values = [
        element
        for multiplicity in active
        for element in classes[multiplicity]
        for _ in range(multiplicity)
    ]
    checks.equal(len(expanded_values), live_size, f"{name}: expanded live size")

    coefficient_checks = 0
    weight_checks = 0
    pair_component_checks = 0
    symmetric_component_checks = 0
    aggregate_checks = 0
    strict_improvements = 0
    minimum_pair_margin = float("inf")
    minimum_symmetric_minus_pair = float("inf")
    weight_records: list[dict[str, Any]] = []

    for total_weight in range(live_size + 1):
        compositions = [
            allocation
            for allocation in allocations
            if sum(allocation) == total_weight
        ]
        denominator = math.comb(live_size, total_weight)
        full_e = [
            elementary_coeff(
                [
                    character_value(element, character)
                    for element in expanded_values
                ],
                total_weight,
            )
            for character in range(group_size)
        ]
        weight_numerator = 0
        for allocation in compositions:
            product_m = math.prod(
                internal[multiplicity]["m_values"][weight]
                for (multiplicity, _), weight in zip(slots, allocation)
            )
            weight_numerator += product_m
        checks.equal(
            weight_numerator,
            denominator,
            f"{name}: convex weights m={total_weight}",
        )
        weight_checks += 1

        for character in range(group_size):
            expanded = sum(
                math.prod(
                    internal[multiplicity]["e_by_weight"][weight][character]
                    for (multiplicity, _), weight in zip(slots, allocation)
                )
                for allocation in compositions
            )
            checks.equal(
                expanded,
                full_e[character],
                f"{name}: coefficient identity m={total_weight} chi={character}",
            )
            coefficient_checks += 1

        pair_bound = 0.0
        symmetric_bound = 0.0
        uncentered_bound = 0.0
        if d_star >= 2:
            for allocation in compositions:
                m_factors = [
                    internal[multiplicity]["m_values"][weight]
                    for (multiplicity, _), weight in zip(slots, allocation)
                ]
                eta_factors = [
                    internal[multiplicity]["eta"][weight]
                    for (multiplicity, _), weight in zip(slots, allocation)
                ]
                left = sum(
                    math.prod(
                        abs(internal[multiplicity]["e_by_weight"][weight][character])
                        for (multiplicity, _), weight in zip(slots, allocation)
                    )
                    for character in range(1, group_size)
                )
                product_m = math.prod(m_factors)
                pair_products = [
                    eta_factors[left_index] * eta_factors[right_index]
                    for left_index in range(d_star)
                    for right_index in range(left_index + 1, d_star)
                ]
                minimum_pair = min(pair_products)
                checks.require(
                    Fraction(left * left, 1)
                    <= Fraction(product_m * product_m, 1) * minimum_pair,
                    f"{name}: pairwise Cauchy m={total_weight} "
                    f"allocation={allocation}",
                )
                pair_component_checks += 1

                symmetric_power = Fraction(1)
                for eta_value, m_value in zip(eta_factors, m_factors):
                    symmetric_power *= eta_value * m_value**d_star
                checks.require(
                    Fraction(left**d_star, 1) <= symmetric_power,
                    f"{name}: symmetric Holder m={total_weight} "
                    f"allocation={allocation}",
                )
                symmetric_component_checks += 1

                product_eta = math.prod(eta_factors)
                checks.require(
                    minimum_pair**d_star <= product_eta**2,
                    f"{name}: pair no worse exact m={total_weight} "
                    f"allocation={allocation}",
                )
                probability = product_m / denominator
                pair_root = math.sqrt(float(minimum_pair))
                symmetric_root = float(product_eta) ** (1.0 / d_star)
                uncentered_root = math.prod(
                    float(value + 1) ** (1.0 / d_star)
                    for value in eta_factors
                )
                pair_bound += probability * pair_root
                symmetric_bound += probability * symmetric_root
                uncentered_bound += probability * uncentered_root

            actual = sum(abs(value) for value in full_e[1:]) / denominator
            checks.require(
                actual <= pair_bound + 1e-10,
                f"{name}: aggregate pair compiler m={total_weight}",
            )
            checks.require(
                pair_bound <= symmetric_bound + 1e-10,
                f"{name}: pair no worse m={total_weight}",
            )
            checks.require(
                symmetric_bound <= uncentered_bound - 1 + 1e-10,
                f"{name}: centered no worse m={total_weight}",
            )
            aggregate_checks += 3
            minimum_pair_margin = min(minimum_pair_margin, pair_bound - actual)
            minimum_symmetric_minus_pair = min(
                minimum_symmetric_minus_pair,
                symmetric_bound - pair_bound,
            )
            if symmetric_bound - pair_bound > 1e-10:
                strict_improvements += 1
            weight_records.append(
                {
                    "m": total_weight,
                    "actual": format(actual, ".12g"),
                    "pair_bound": format(pair_bound, ".12g"),
                    "symmetric_bound": format(symmetric_bound, ".12g"),
                    "uncentered_bound": format(uncentered_bound, ".12g"),
                }
            )

    translation_checks = 0
    if rank >= 1:
        shift = 1
        shifted_values = [element ^ shift for element in expanded_values]
        for total_weight in range(live_size + 1):
            for character in range(group_size):
                original = elementary_coeff(
                    [
                        character_value(element, character)
                        for element in expanded_values
                    ],
                    total_weight,
                )
                shifted = elementary_coeff(
                    [
                        character_value(element, character)
                        for element in shifted_values
                    ],
                    total_weight,
                )
                expected = original * character_value(shift, character) ** total_weight
                checks.equal(
                    shifted,
                    expected,
                    f"{name}: affine translation m={total_weight} chi={character}",
                )
                translation_checks += 1

    uniform = len(active) == 1
    uniform_degree = active[0] if uniform else None
    theorem_applicable = d_star >= 2
    return {
        "name": name,
        "target": f"F2^{rank}",
        "target_order": group_size,
        "multiplicities": active,
        "class_sizes": {
            str(multiplicity): len(classes[multiplicity])
            for multiplicity in active
        },
        "live_size": live_size,
        "d_star": d_star,
        "theorem_applicable": theorem_applicable,
        "uniform_profile": uniform,
        "uniform_degree": uniform_degree,
        "parent_symmetric_recovered": uniform and uniform_degree is not None
        and uniform_degree >= 2,
        "pair_equals_parent_when_d2": uniform_degree == 2,
        "classes": class_records,
        "allocation_count": len(allocations),
        "coefficient_checks": coefficient_checks,
        "weight_checks": weight_checks,
        "pair_component_checks": pair_component_checks,
        "symmetric_component_checks": symmetric_component_checks,
        "aggregate_checks": aggregate_checks,
        "translation_checks": translation_checks,
        "strict_improvements": strict_improvements,
        "minimum_pair_margin":
            None if d_star < 2 else margin_text(minimum_pair_margin),
        "minimum_symmetric_minus_pair":
            None if d_star < 2
            else margin_text(minimum_symmetric_minus_pair),
        "weights": weight_records,
    }


def profile_suite(checks: Checks) -> list[dict[str, Any]]:
    profiles = [
        ("one_three", 1, {1: [0], 3: [1]}),
        ("one_two", 2, {1: [0, 1], 2: [1, 2]}),
        ("two_three", 2, {2: [0, 1], 3: [1, 3]}),
        ("one_two_four", 2, {1: [0, 1], 2: [1], 4: [2]}),
        ("uniform_two", 2, {2: [0, 1, 2]}),
        ("uniform_three", 2, {3: [0, 1, 3]}),
        ("uniform_three_strict", 1, {3: [0, 0, 1]}),
        ("uniform_four", 2, {4: [0, 1]}),
        ("zero_eta_class", 2, {1: [0], 2: [0, 1, 2, 3]}),
        ("all_singletons", 2, {1: [0, 1, 2]}),
        ("trivial_target", 0, {1: [0], 3: [0]}),
    ]
    records = [
        profile_case(checks, name=name, rank=rank, classes=classes)
        for name, rank, classes in profiles
    ]
    by_name = {record["name"]: record for record in records}
    strict = by_name["uniform_three_strict"]
    strict_row = next(row for row in strict["weights"] if row["m"] == 3)
    checks.close(
        float(strict_row["pair_bound"]),
        1.0 / 7.0,
        1e-11,
        "uniform-three strict pair value",
    )
    checks.require(
        float(strict_row["symmetric_bound"]) > float(strict_row["pair_bound"]),
        "uniform-three strict improvement",
    )
    checks.equal(
        by_name["all_singletons"]["theorem_applicable"],
        False,
        "all-singleton exclusion",
    )
    checks.equal(
        by_name["trivial_target"]["target_order"],
        1,
        "trivial target record",
    )
    return records


def falsifier_suite(
    checks: Checks, profiles: list[dict[str, Any]]
) -> dict[str, Any]:
    true_nonuniform = polynomial([1, -1, -1, -1])
    collapsed_classes = polynomial([1, -1])
    fake_uniform_two = polynomial([1, 1, -1, -1])
    checks.require(
        true_nonuniform != collapsed_classes,
        "multiplicity copies are load-bearing",
    )
    checks.require(
        true_nonuniform != fake_uniform_two,
        "fake uniform power rejected",
    )

    true_phase = polynomial([1, -1])
    fake_phase = polynomial([1, 1])
    checks.require(true_phase != fake_phase, "phase constancy falsifier")

    d1_values = [0, 1, 2]
    d1_eta = centered_eta_for_values(d1_values, 1, 4)
    d1_loss = normalized_nontrivial_l1(d1_values, 1, 4)
    checks.equal(d1_eta, Fraction(1, 3), "computed D-star-one eta")
    checks.equal(d1_loss, Fraction(1), "computed D-star-one loss")
    checks.require(d1_loss > d1_eta, "D-star-one counterexample")

    q_one = [0, 1]
    q_two = [2, 3]
    pooled_eta = centered_eta_for_values(q_one + q_two, 1, 4)
    pooled_live_values = q_one + [
        value for value in q_two for _ in range(2)
    ]
    pooled_true_loss = normalized_nontrivial_l1(
        pooled_live_values, 1, 4
    )
    checks.equal(pooled_eta, Fraction(0), "computed pooled eta")
    checks.equal(
        pooled_true_loss,
        Fraction(1, 3),
        "computed pooled true loss",
    )
    checks.require(
        pooled_true_loss > pooled_eta,
        "class pooling counterexample",
    )

    local_target_bound = centered_eta_for_values([0], 0, 2)
    local_live_values = [1, 2, 2]
    common_target_true_loss = normalized_nontrivial_l1(
        local_live_values, 1, 4
    )
    checks.equal(
        local_target_bound,
        Fraction(1),
        "computed local target bound",
    )
    checks.equal(
        common_target_true_loss,
        Fraction(5, 3),
        "computed common-target loss",
    )
    checks.require(
        common_target_true_loss > local_target_bound,
        "local target counterexample",
    )

    strict_profile = next(
        profile
        for profile in profiles
        if profile["name"] == "uniform_three_strict"
    )
    strict_row = next(
        row for row in strict_profile["weights"] if row["m"] == 3
    )
    po3_unmarked_pair = float(strict_row["pair_bound"])
    po3_component_loss = normalized_nontrivial_l1([0, 0, 1], 1, 2)
    checks.close(
        po3_unmarked_pair,
        1.0 / 7.0,
        1e-11,
        "computed PO3 unmarked pair bound",
    )
    checks.equal(
        po3_component_loss,
        Fraction(1, 3),
        "computed PO3 component loss",
    )
    checks.require(
        float(po3_component_loss) > po3_unmarked_pair,
        "PO3 marker counterexample",
    )
    return {
        "multiplicity_one_three": {
            "true_coefficients": true_nonuniform,
            "collapsed_class_coefficients": collapsed_classes,
            "fake_uniform_two_coefficients": fake_uniform_two,
            "true_identity_requires_all_multiplicity_copies": True,
        },
        "phase_constancy": {
            "true_coefficients": true_phase,
            "fake_constant_coefficients": fake_phase,
            "fiber_constant_required": True,
        },
        "all_singletons": {
            "target": "F2^2",
            "h": d1_values,
            "m": 1,
            "eta": fraction_text(d1_eta),
            "normalized_nontrivial_l1": fraction_text(d1_loss),
            "pairwise_theorem_valid": False,
        },
        "pooled_classes": {
            "target": "F2^2",
            "Q1": q_one,
            "Q2": q_two,
            "pooled_eta": fraction_text(pooled_eta),
            "true_normalized_l1": fraction_text(pooled_true_loss),
            "pooling_valid": False,
        },
        "local_targets": {
            "target": "F2^2",
            "local_bound": fraction_text(local_target_bound),
            "true_normalized_l1": fraction_text(common_target_true_loss),
            "local_target_normalization_valid": False,
        },
        "po3_markers": {
            "target": "Z/2",
            "multiplicity": 3,
            "h": [0, 0, 1],
            "m": 3,
            "unmarked_pair_bound": strict_row["pair_bound"],
            "unmarked_pair_exact_reference": "1/7",
            "one_full_fiber_component_loss": fraction_text(po3_component_loss),
            "erasing_markers_valid": False,
            "linked_profile": strict_profile["name"],
        },
    }


def source_gate(repo: Path, checks: Checks) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in SOURCE_HASHES.items():
        digest = file_sha256(repo / relative)
        checks.equal(digest, expected, f"source hash {relative}")
        observed[relative] = digest
    return observed


def build_artifact(repo: Path, checks: Checks) -> dict[str, Any]:
    sources = source_gate(repo, checks)
    profiles = profile_suite(checks)
    falsifiers = falsifier_suite(checks, profiles)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "base_commit": BASE_COMMIT,
        "parent_commit": PARENT_COMMIT,
        "sources": sources,
        "files": {
            str(NOTE_PATH): file_sha256(repo / NOTE_PATH),
            str(VERIFIER_PATH): file_sha256(repo / VERIFIER_PATH),
        },
        "parent_packet": {
            "note_sha256": SOURCE_HASHES[
                "experimental/notes/thresholds/"
                "a4_trace_quotient_rank_centered_compiler.md"
            ],
            "verifier_sha256": SOURCE_HASHES[
                "experimental/scripts/"
                "verify_a4_trace_quotient_rank_centered_compiler.py"
            ],
            "certificate_sha256": SOURCE_HASHES[
                "experimental/data/certificates/"
                "a4-trace-quotient-rank-centered/"
                "a4_trace_quotient_rank_centered_compiler.json"
            ],
            "non_log_files_preserved": True,
        },
        "theorem": {
            "factorization":
                "prod_t(1+chi(a(t))Y)=prod_s E_(s,chi)(Y)^s",
            "actual_positive_multiplicities_required": True,
            "factor_slots": "D_star=sum_(s:n_s>0)s",
            "d_star_at_least_two": True,
            "common_target_required": True,
            "translated_effective_phase_required": True,
            "affine_coefficient_factor": "chi_tilde(g(t0))^m",
            "trivial_character_excluded": True,
            "pair_chosen_per_composition_not_character": True,
            "pair_slots_distinct": True,
            "repeated_factor_functions_allowed": True,
            "pair_bound":
                "Cmaj<=sum_j w_j min_(u<v)sqrt(eta_(u,j_u)eta_(v,j_v))",
            "comparison":
                "K_pair<=K_symmetric<=K_uncentered-1",
            "uniform_d2_equals_parent": True,
            "uniform_d_gt_2_can_be_stronger": True,
            "strict_on_every_instance": False,
            "profiles": profiles,
            "falsifiers": falsifiers,
        },
        "consumer_audit": {
            "coordinate_restriction_allowed": True,
            "full_fixed_weight_slice_required": True,
            "support_level_first_match_deletion_supported": False,
            "po3_fixed_statistic_without_markers_supported": False,
            "class_energies_may_be_pooled": False,
            "class_local_targets_allowed": False,
            "classwise_energies_supplied": False,
            "PR564_energy_reclaimed": False,
            "assigned_map_sum_subexponential_required": True,
            "pairwise_target_weighted_tail_required": True,
            "overlap_assignment_supplied": False,
            "full_MA_closed": False,
            "full_A4_closed": False,
            "deployed_row_closed": False,
            "tex_modified": False,
        },
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_artifact(
    artifact: dict[str, Any], repo: Path, checks: Checks
) -> None:
    checks.equal(artifact["schema"], SCHEMA, "schema")
    checks.equal(artifact["status"], STATUS, "status")
    checks.equal(artifact["base_commit"], BASE_COMMIT, "base commit")
    checks.equal(artifact["parent_commit"], PARENT_COMMIT, "parent commit")
    checks.equal(
        artifact["payload_sha256"],
        payload_hash(artifact),
        "payload hash",
    )
    for relative, expected in SOURCE_HASHES.items():
        checks.equal(artifact["sources"][relative], expected, f"stored source {relative}")
        checks.equal(file_sha256(repo / relative), expected, f"live source {relative}")
    for relative, digest in artifact["files"].items():
        checks.equal(file_sha256(repo / relative), digest, f"packet file {relative}")
    checks.equal(
        artifact["parent_packet"]["non_log_files_preserved"],
        True,
        "parent preservation",
    )

    theorem = artifact["theorem"]
    expected_theorem = {
        "actual_positive_multiplicities_required": True,
        "factor_slots": "D_star=sum_(s:n_s>0)s",
        "d_star_at_least_two": True,
        "common_target_required": True,
        "translated_effective_phase_required": True,
        "affine_coefficient_factor": "chi_tilde(g(t0))^m",
        "trivial_character_excluded": True,
        "pair_chosen_per_composition_not_character": True,
        "pair_slots_distinct": True,
        "repeated_factor_functions_allowed": True,
        "comparison": "K_pair<=K_symmetric<=K_uncentered-1",
        "uniform_d2_equals_parent": True,
        "uniform_d_gt_2_can_be_stronger": True,
        "strict_on_every_instance": False,
    }
    for key, expected in expected_theorem.items():
        checks.equal(theorem[key], expected, f"theorem {key}")
    for profile in theorem["profiles"]:
        expected_d = sum(profile["multiplicities"])
        expected_n = sum(
            int(multiplicity) * size
            for multiplicity, size in profile["class_sizes"].items()
        )
        checks.equal(profile["d_star"], expected_d, f"{profile['name']}: d star")
        checks.equal(profile["live_size"], expected_n, f"{profile['name']}: live size")
        checks.equal(
            profile["theorem_applicable"],
            expected_d >= 2,
            f"{profile['name']}: applicability",
        )
    falsifiers = theorem["falsifiers"]
    checks.equal(
        falsifiers["all_singletons"]["pairwise_theorem_valid"],
        False,
        "D-star-one falsifier",
    )
    checks.equal(
        falsifiers["pooled_classes"]["pooling_valid"],
        False,
        "pooling falsifier",
    )
    checks.equal(
        falsifiers["local_targets"]["local_target_normalization_valid"],
        False,
        "local target falsifier",
    )
    checks.equal(
        falsifiers["po3_markers"]["erasing_markers_valid"],
        False,
        "PO3 marker falsifier",
    )

    audit = artifact["consumer_audit"]
    expected_audit = {
        "coordinate_restriction_allowed": True,
        "full_fixed_weight_slice_required": True,
        "support_level_first_match_deletion_supported": False,
        "po3_fixed_statistic_without_markers_supported": False,
        "class_energies_may_be_pooled": False,
        "class_local_targets_allowed": False,
        "classwise_energies_supplied": False,
        "PR564_energy_reclaimed": False,
        "assigned_map_sum_subexponential_required": True,
        "pairwise_target_weighted_tail_required": True,
        "overlap_assignment_supplied": False,
        "full_MA_closed": False,
        "full_A4_closed": False,
        "deployed_row_closed": False,
        "tex_modified": False,
    }
    for key, expected in expected_audit.items():
        checks.equal(audit[key], expected, f"audit {key}")


def tamper_selftest(
    artifact: dict[str, Any], repo: Path, checks: Checks
) -> int:
    mutations = [
        ("allow-D1", lambda x: x["theorem"].__setitem__(
            "d_star_at_least_two", False
        )),
        ("max-multiplicity-slots", lambda x: x["theorem"].__setitem__(
            "factor_slots", "D_star=max_s"
        )),
        ("pool-classes", lambda x: x["consumer_audit"].__setitem__(
            "class_energies_may_be_pooled", True
        )),
        ("local-targets", lambda x: x["consumer_audit"].__setitem__(
            "class_local_targets_allowed", True
        )),
        ("drop-common-target", lambda x: x["theorem"].__setitem__(
            "common_target_required", False
        )),
        ("drop-translation", lambda x: x["theorem"].__setitem__(
            "translated_effective_phase_required", False
        )),
        ("include-trivial", lambda x: x["theorem"].__setitem__(
            "trivial_character_excluded", False
        )),
        ("pair-per-character", lambda x: x["theorem"].__setitem__(
            "pair_chosen_per_composition_not_character", False
        )),
        ("same-slot-pair", lambda x: x["theorem"].__setitem__(
            "pair_slots_distinct", False
        )),
        ("claim-strict-always", lambda x: x["theorem"].__setitem__(
            "strict_on_every_instance", True
        )),
        ("support-deletion", lambda x: x["consumer_audit"].__setitem__(
            "support_level_first_match_deletion_supported", True
        )),
        ("erase-PO3-markers", lambda x: x["consumer_audit"].__setitem__(
            "po3_fixed_statistic_without_markers_supported", True
        )),
        ("claim-class-energy", lambda x: x["consumer_audit"].__setitem__(
            "classwise_energies_supplied", True
        )),
        ("reclaim-PR564", lambda x: x["consumer_audit"].__setitem__(
            "PR564_energy_reclaimed", True
        )),
        ("drop-map-sum", lambda x: x["consumer_audit"].__setitem__(
            "assigned_map_sum_subexponential_required", False
        )),
        ("drop-tail", lambda x: x["consumer_audit"].__setitem__(
            "pairwise_target_weighted_tail_required", False
        )),
        ("claim-overlap", lambda x: x["consumer_audit"].__setitem__(
            "overlap_assignment_supplied", True
        )),
        ("claim-full-MA", lambda x: x["consumer_audit"].__setitem__(
            "full_MA_closed", True
        )),
        ("claim-full-A4", lambda x: x["consumer_audit"].__setitem__(
            "full_A4_closed", True
        )),
        ("claim-row", lambda x: x["consumer_audit"].__setitem__(
            "deployed_row_closed", True
        )),
        ("claim-TeX", lambda x: x["consumer_audit"].__setitem__(
            "tex_modified", True
        )),
        ("parent-not-preserved", lambda x: x["parent_packet"].__setitem__(
            "non_log_files_preserved", False
        )),
    ]
    rejected = 0
    for name, mutation in mutations:
        damaged = copy.deepcopy(artifact)
        mutation(damaged)
        damaged["payload_sha256"] = payload_hash(damaged)
        local = Checks()
        try:
            validate_artifact(damaged, repo, local)
        except (CheckFailure, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise CheckFailure(f"tamper accepted: {name}")
        checks.count += local.count
    checks.equal(rejected, len(mutations), "all semantic tampers rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checks = Checks()
    cap = impose_cap(checks)
    repo = locate_repo(args.repo)
    artifact = build_artifact(repo, checks)
    validate_artifact(artifact, repo, checks)

    artifact_path = args.artifact
    if not artifact_path.is_absolute():
        artifact_path = repo / artifact_path
    if args.write:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        checks.require(artifact_path.is_file(), "certificate exists")
        stored = json.loads(artifact_path.read_text())
        validate_artifact(stored, repo, checks)
        checks.equal(canonical(stored), canonical(artifact), "deterministic certificate")
    rejected = 0
    if args.tamper_selftest:
        rejected = tamper_selftest(artifact, repo, checks)

    modes = []
    if args.write:
        modes.append("write")
    if args.check:
        modes.append("check")
    if args.tamper_selftest:
        modes.append(f"tamper={rejected}")
    if not modes:
        modes.append("default")
    print(
        f"RESULT: PASS ({checks.count} checks; mode={','.join(modes)}; "
        f"cap={cap}; payload={artifact['payload_sha256']})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, KeyError, ValueError, TypeError) as exc:
        print(f"RESULT: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
