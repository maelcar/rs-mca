#!/usr/bin/env python3
"""Verify the A4 weighted quotient count and uniform-fold compiler packet."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import resource
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "a4_quotient_major_compiler.v1"
STATUS = "PROVED_WEIGHTED_GRS_COUNT_AND_ALL_DEGREE_UNIFORM_FOLD_COMPILER"
BASE_COMMIT = "5c9aab794e6575d815541e0a5dd8534d03d400aa"
CAP_BYTES = 1024**3
NOTE_PATH = Path(
    "experimental/notes/thresholds/a4_quotient_major_compiler.md"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_a4_quotient_major_compiler.py"
)
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/a4-quotient-major-compiler/"
    "a4_quotient_major_compiler.json"
)
SOURCE_HASHES = {
    "experimental/asymptotic_rs_mca_frontiers.tex":
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
    "experimental/notes/thresholds/c9_major_arc_valueset_structure.md":
        "6fd793af8933749018c109bc7d82d5b4c45972239321c7f469daf3b94e9a15d8",
    "experimental/notes/thresholds/pte_cluster_packing_frontier.md":
        "b99277ea9824acfecfac4d04828dfb05f27c11e43c2617a82c18a5664b4deeb9",
    "experimental/notes/roadmaps/b2_l1_crux_milestone.md":
        "1bae6abe2cf823d2bf9a29d2be21c1f169453d3f27b38c5917669b36d2c231bd",
    "experimental/notes/roadmaps/b2_l1_reduction_ledger.md":
        "bd35b82b5cec35639b0bf539e15709b53e3316dae0c2b8e298953db424fb0435",
    "experimental/notes/thresholds/minimal_phase_supplement.md":
        "637057f902d105ad438e31b0b38f95c0d63d54b0716a1bb547e712c602e49c2a",
    "experimental/notes/thresholds/moment_map_max_fiber.md":
        "f3d7bbc3f3522a9a1c32f31b28aa3c8b547110cd4ad04f1a8742b1553ce1d245",
    "experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md":
        "7545779b5ca3454007508b74dd225abab716ae809ad6c7ebe08dcfd716359b25",
    "experimental/notes/thresholds/cap25_v13_qfin_rung_audit_m31.md":
        "b038245aa27ee397f67e8821ba64c6f8d766734eb73c7e1afe177e3230f042d7",
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


def impose_cap(checks: Checks) -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    checks.require(
        soft != resource.RLIM_INFINITY and soft <= CAP_BYTES,
        "one GiB address-space cap",
    )
    return int(soft)


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(obj)
    value.pop("payload_sha256", None)
    return value


def payload_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(without_hash(obj))).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not (root / NOTE_PATH).is_file():
            raise CheckFailure("explicit repo is missing the A4 note")
        return root
    env = os.environ.get("A4_QUOTIENT_MAJOR_REPO")
    if env:
        return locate_repo(Path(env))
    candidates = [Path.cwd().resolve(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / NOTE_PATH).is_file():
            return candidate
    raise CheckFailure("pass --repo or set A4_QUOTIENT_MAJOR_REPO")


def inv_mod(value: int, p: int) -> int:
    value %= p
    if value == 0:
        raise CheckFailure("attempted inversion of zero")
    return pow(value, p - 2, p)


def rref(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    data = [[entry % p for entry in row] for row in matrix]
    rows = len(data)
    cols = len(data[0])
    pivots: list[int] = []
    cursor = 0
    for col in range(cols):
        pivot = next((r for r in range(cursor, rows) if data[r][col]), None)
        if pivot is None:
            continue
        data[cursor], data[pivot] = data[pivot], data[cursor]
        scale = inv_mod(data[cursor][col], p)
        data[cursor] = [(scale * value) % p for value in data[cursor]]
        for row in range(rows):
            if row == cursor or data[row][col] == 0:
                continue
            factor = data[row][col]
            data[row] = [
                (a - factor * b) % p
                for a, b in zip(data[row], data[cursor])
            ]
        pivots.append(col)
        cursor += 1
        if cursor == rows:
            break
    return data, pivots


def rank_mod(matrix: list[list[int]], p: int, columns: int | None = None) -> int:
    if not matrix:
        return 0
    if columns is not None:
        matrix = [row[:columns] for row in matrix]
    return len(rref(matrix, p)[1])


def nullspace(matrix: list[list[int]], p: int, columns: int) -> list[list[int]]:
    if not matrix:
        return [
            [1 if i == j else 0 for i in range(columns)]
            for j in range(columns)
        ]
    reduced, pivots = rref(matrix, p)
    free = [col for col in range(columns) if col not in pivots]
    basis: list[list[int]] = []
    for free_col in free:
        vector = [0] * columns
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-reduced[row][free_col]) % p
        basis.append(vector)
    return basis


def vector_sum(coefficients: Iterable[int], basis: list[list[int]], p: int) -> list[int]:
    result = [0] * (len(basis[0]) if basis else 0)
    for scalar, vector in zip(coefficients, basis):
        for index, value in enumerate(vector):
            result[index] = (result[index] + scalar * value) % p
    return result


def eval_poly(coefficients: list[int], t: int, p: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * t + coefficient) % p
    return result


def power_fibers(p: int, d: int) -> tuple[list[int], list[list[int]]]:
    points = list(range(1, p))
    by_value: dict[int, list[int]] = {}
    for t in points:
        by_value.setdefault(pow(t, d, p), []).append(t)
    fibers = [by_value[key] for key in sorted(by_value)]
    if any(len(fiber) != d for fiber in fibers):
        raise CheckFailure(f"x -> x^{d} is not exactly {d}-to-one over F_{p}^*")
    return points, fibers


def weighted_grs_record(
    checks: Checks,
    *,
    name: str,
    p: int,
    d: int,
    redundancy: int,
    weight_kind: str,
) -> dict[str, Any]:
    points, fibers = power_fibers(p, d)
    n_total = len(points)
    k = min(redundancy, n_total)

    def weight(t: int) -> int:
        if weight_kind.startswith("monomial:"):
            exponent = int(weight_kind.split(":", 1)[1])
            return pow(t, exponent, p)
        if weight_kind == "quadratic_plus_one":
            return (t * t + 1) % p
        raise CheckFailure(f"unknown weight kind {weight_kind}")

    weights = {t: weight(t) for t in points}
    checks.require(all(value != 0 for value in weights.values()), f"{name}: weights nonzero")

    evaluation = [
        [(weights[t] * pow(t, exponent, p)) % p for exponent in range(redundancy)]
        for t in points
    ]
    eval_rank = rank_mod(evaluation, p)
    checks.equal(eval_rank, k, f"{name}: weighted GRS dimension")

    constraints: list[list[int]] = []
    for fiber in fibers:
        base = fiber[0]
        for t in fiber[1:]:
            constraints.append([
                (
                    weights[t] * pow(t, exponent, p)
                    - weights[base] * pow(base, exponent, p)
                ) % p
                for exponent in range(redundancy)
            ])

    solution_basis = nullspace(constraints, p, redundancy)
    coefficient_solution_dim = len(solution_basis)
    evaluation_kernel_dim = redundancy - eval_rank
    phase_dim = coefficient_solution_dim - evaluation_kernel_dim
    ceiling = (k + d - 1) // d
    checks.require(phase_dim <= ceiling, f"{name}: weighted MDS ceiling")

    phase_words: set[tuple[int, ...]] = set()
    for scalars in product(range(p), repeat=coefficient_solution_dim):
        coefficients = vector_sum(scalars, solution_basis, p)
        phase_words.add(tuple(
            weights[t] * eval_poly(coefficients, t, p) % p
            for t in points
        ))
    checks.equal(len(phase_words), p**phase_dim, f"{name}: phase-space cardinality")

    point_index = {t: index for index, t in enumerate(points)}
    descended: set[tuple[int, ...]] = set()
    for word in phase_words:
        down: list[int] = []
        for fiber in fibers:
            values = {word[point_index[t]] for t in fiber}
            checks.equal(len(values), 1, f"{name}: literal constancy on every fiber")
            down.append(next(iter(values)))
        descended.add(tuple(down))
    checks.equal(len(descended), len(phase_words), f"{name}: descent injective")

    nonzero_up = [word for word in phase_words if any(word)]
    nonzero_down = [word for word in descended if any(word)]
    max_up_zeros = max(
        (sum(value == 0 for value in word) for word in nonzero_up),
        default=0,
    )
    min_down_distance = min(
        (sum(value != 0 for value in word) for word in nonzero_down),
        default=len(fibers) + 1,
    )
    distance_floor = len(fibers) - (k - 1) // d
    checks.require(max_up_zeros <= k - 1, f"{name}: MDS zero bound")
    checks.require(
        min_down_distance >= distance_floor,
        f"{name}: descended distance floor",
    )
    checks.require(
        phase_dim <= len(fibers) - min_down_distance + 1,
        f"{name}: Singleton from measured distance",
    )

    return {
        "name": name,
        "p": p,
        "N": n_total,
        "d": d,
        "R": redundancy,
        "k": k,
        "weight": weight_kind,
        "constraint_rank": rank_mod(constraints, p),
        "phase_dimension": phase_dim,
        "floor_k_over_d": k // d,
        "ceiling_k_over_d": ceiling,
        "phase_count": len(phase_words),
        "max_nonzero_lift_zeros": max_up_zeros,
        "descended_length": len(fibers),
        "descended_minimum_distance": min_down_distance,
        "proved_distance_floor": distance_floor,
    }


def xor_convolution(left: list[int], right: list[int]) -> list[int]:
    if len(left) != len(right) or len(left) & (len(left) - 1):
        raise CheckFailure("xor convolution needs equal power-of-two lengths")
    result = [0] * len(left)
    for a, left_value in enumerate(left):
        if left_value == 0:
            continue
        for b, right_value in enumerate(right):
            if right_value:
                result[a ^ b] += left_value * right_value
    return result


def subset_distributions(values: list[int], group_order: int) -> list[list[int]]:
    distributions: list[list[int]] = []
    for size in range(len(values) + 1):
        counts = [0] * group_order
        for chosen in combinations(range(len(values)), size):
            total = 0
            for index in chosen:
                total ^= values[index]
            counts[total] += 1
        distributions.append(counts)
    return distributions


def fourier_values(counts: list[int]) -> list[int]:
    values: list[int] = []
    for character in range(len(counts)):
        total = 0
        for point, multiplicity in enumerate(counts):
            sign = -1 if (character & point).bit_count() % 2 else 1
            total += sign * multiplicity
        values.append(total)
    return values


def bounded_compositions(total: int, parts: int, upper: int) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def visit(prefix: list[int], remaining: int) -> None:
        if len(prefix) == parts - 1:
            if 0 <= remaining <= upper:
                result.append(tuple(prefix + [remaining]))
            return
        for value in range(max(0, remaining - upper * (parts - len(prefix) - 1)), min(upper, remaining) + 1):
            visit(prefix + [value], remaining - value)

    visit([], total)
    return result


def fraction_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def uniform_fold_record(
    checks: Checks,
    *,
    d: int,
    values: list[int],
    group_order: int,
    selected_m: int,
) -> dict[str, Any]:
    n = len(values)
    checks.require(
        all(0 <= value < group_order for value in values),
        f"d={d}: quotient values lie in target",
    )
    quotient = subset_distributions(values, group_order)
    m_values = [math.comb(n, j) for j in range(n + 1)]
    fourier = [fourier_values(counts) for counts in quotient]
    kappas: list[Fraction] = []
    energies: list[int] = []
    qfi_rows: list[dict[str, Any]] = []
    for j, counts in enumerate(quotient):
        energy = sum(value * value for value in counts)
        energies.append(energy)
        parseval = sum(value * value for value in fourier[j])
        checks.equal(parseval, group_order * energy, f"d={d},j={j}: Parseval")
        kappa = Fraction(group_order * energy, m_values[j] ** 2)
        kappas.append(kappa)
        checks.require(Fraction(1) <= kappa <= group_order, f"d={d},j={j}: kappa range")
        image = sum(value > 0 for value in counts)
        maximum = max(counts)
        q_loss = Fraction(maximum * image, m_values[j])
        fi_loss = Fraction(group_order, image)
        checks.require(kappa <= q_loss * fi_loss, f"d={d},j={j}: Q times FI")
        qfi_rows.append({
            "j": j,
            "M_j": m_values[j],
            "SP_j": energy,
            "image": image,
            "max_fiber": maximum,
            "kappa": fraction_pair(kappa),
            "Q_loss": fraction_pair(q_loss),
            "FI_loss": fraction_pair(fi_loss),
        })
    checks.equal(kappas[0], Fraction(group_order), f"d={d}: kappa zero endpoint")
    checks.equal(kappas[-1], Fraction(group_order), f"d={d}: kappa full endpoint")

    repeated_values = [value for _copy in range(d) for value in values]
    full = subset_distributions(repeated_values, group_order)
    total_checks = 0
    selected: dict[str, Any] | None = None
    for m in range(d * n + 1):
        compositions = bounded_compositions(m, d, n)
        convolution_sum = [0] * group_order
        weight_numerator = 0
        component_l1_sum = 0
        component_count = 0
        for composition in compositions:
            distribution = [1] + [0] * (group_order - 1)
            for j in composition:
                distribution = xor_convolution(distribution, quotient[j])
            convolution_sum = [
                a + b for a, b in zip(convolution_sum, distribution)
            ]
            weight_numerator += math.prod(m_values[j] for j in composition)

            lhs = sum(
                math.prod(abs(fourier[j][character]) for j in composition)
                for character in range(group_order)
            )
            moments = [
                sum(abs(value) ** d for value in fourier[j])
                for j in composition
            ]
            checks.require(
                lhs**d <= math.prod(moments),
                f"d={d},m={m},composition={composition}: Holder",
            )
            for j, moment in zip(composition, moments):
                checks.require(
                    moment
                    <= m_values[j] ** (d - 2)
                    * sum(value * value for value in fourier[j]),
                    f"d={d},m={m},j={j}: L2-Linf fallback",
                )
            component_l1_sum += lhs
            component_count += 1
            total_checks += 1

        checks.equal(convolution_sum, full[m], f"d={d},m={m}: group-ring coefficient identity")
        checks.equal(weight_numerator, math.comb(d * n, m), f"d={d},m={m}: Vandermonde weights")
        full_fourier = fourier_values(full[m])
        coefficient_formula = [
            sum(
                math.prod(fourier[j][character] for j in composition)
                for composition in compositions
            )
            for character in range(group_order)
        ]
        checks.equal(coefficient_formula, full_fourier, f"d={d},m={m}: character coefficient identity")
        checks.require(
            sum(abs(value) for value in full_fourier) <= component_l1_sum,
            f"d={d},m={m}: triangle allocation",
        )
        if m == selected_m:
            selected = {
                "m": m,
                "M": math.comb(d * n, m),
                "composition_count": component_count,
                "weight_numerator_sum": weight_numerator,
                "all_character_L1": sum(abs(value) for value in full_fourier),
                "nontrivial_character_L1": sum(abs(value) for value in full_fourier[1:]),
                "triangle_component_L1_sum": component_l1_sum,
            }
    checks.require(selected is not None, f"d={d}: selected central record")

    return {
        "d": d,
        "n": n,
        "group_order": group_order,
        "quotient_values": values,
        "endpoint_kappa": fraction_pair(kappas[0]),
        "intermediate_weights": qfi_rows,
        "selected_full_slice": selected,
        "holder_compositions_checked": total_checks,
    }


def verify_sources(repo: Path, checks: Checks) -> dict[str, str]:
    for relative, expected in SOURCE_HASHES.items():
        path = repo / relative
        checks.require(path.is_file(), f"source exists: {relative}")
        checks.equal(file_sha256(path), expected, f"source hash: {relative}")

    tex = (repo / "experimental/asymptotic_rs_mca_frontiers.tex").read_text()
    anchors = [
        "Primitive columns are genuine weighted Vandermonde columns",
        "\\label{lem:sparse-major-payment}",
        "\\label{def:major-arc}",
        "weighted phase is constant on a routed quotient fiber",
        "\\tag{PO3}",
        "\\tag{EF7}",
        "\\emph{active coordinate set}",
    ]
    for anchor in anchors:
        checks.require(anchor in tex, f"TeX anchor: {anchor}")

    note = (repo / NOTE_PATH).read_text()
    note_guards = [
        "literal algebraic locus",
        "constant on **every** fiber",
        "proper extension",
        "same target",
        "intermediate collision-energy inputs not supplied",
        "active set is a union of complete fibers",
        "full-slice factor",
        "fixed partial-occupancy statistics",
        "negative applicability stress test only",
        "whole effective factor-through group",
        "changes no paper TeX",
    ]
    for guard in note_guards:
        checks.require(guard in note, f"note guard: {guard}")
    return dict(SOURCE_HASHES)


def build_artifact(repo: Path, checks: Checks) -> dict[str, Any]:
    source_hashes = verify_sources(repo, checks)
    grs_configs = [
        weighted_grs_record(
            checks,
            name="tight_floor_falsifier",
            p=17,
            d=2,
            redundancy=3,
            weight_kind="monomial:2",
        ),
        weighted_grs_record(
            checks,
            name="cubic_fold_tight",
            p=13,
            d=3,
            redundancy=5,
            weight_kind="monomial:2",
        ),
        weighted_grs_record(
            checks,
            name="quartic_fold_tight",
            p=17,
            d=4,
            redundancy=7,
            weight_kind="monomial:2",
        ),
        weighted_grs_record(
            checks,
            name="nonmonomial_common_weight",
            p=11,
            d=2,
            redundancy=4,
            weight_kind="quadratic_plus_one",
        ),
    ]
    tight = grs_configs[0]
    checks.equal(tight["phase_dimension"], 2, "floor falsifier dimension")
    checks.equal(tight["floor_k_over_d"], 1, "floor falsifier old floor")
    checks.equal(tight["ceiling_k_over_d"], 2, "floor falsifier ceiling")

    compiler_records = [
        uniform_fold_record(
            checks,
            d=2,
            values=[0, 1, 2, 4, 3],
            group_order=8,
            selected_m=5,
        ),
        uniform_fold_record(
            checks,
            d=3,
            values=[0, 1, 2, 4],
            group_order=8,
            selected_m=6,
        ),
        uniform_fold_record(
            checks,
            d=4,
            values=[0, 1, 2],
            group_order=4,
            selected_m=6,
        ),
    ]

    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "base_commit": BASE_COMMIT,
        "theorems": {
            "weighted_grs_count": {
                "dimension_bound": "floor((k-1)/d)+1=ceil(k/d)",
                "scope": "global_B_valued_phase_factorization_on_every_exact_fiber",
                "configs": grs_configs,
                "floor_counterexample": {
                    "p": 17,
                    "d": 2,
                    "R": 3,
                    "weight": "rho(t)=t^2",
                    "factor_dimension": 2,
                    "false_floor": 1,
                    "sharp_ceiling": 2,
                },
                "sparse_tail_condition":
                    "log(I_N)+ceil(k/D_N)*log(|B|)=o(N)",
                "sparse_tail_hypotheses": {
                    "global_every_fiber_factorization": True,
                    "certified_effective_major_lift_containment_required": True,
                    "log_map_count_is_o_N_required": True,
                    "k_log_field_is_O_N_required": True,
                    "log_field_is_o_N_required": True,
                    "minimum_degree_tends_to_infinity_required": True,
                    "uniform_over_live_leaves_maps_and_received_lines_required": True,
                    "generic_consumer_supplies_hypotheses": False,
                },
            },
            "uniform_fold_compiler": {
                "degrees_proved": "every integer d>=2",
                "common_target": "A_phi=V_g/W_phi",
                "loss": "C_maj<=K_d(m)-1",
                "records": compiler_records,
            },
        },
        "hypothesis_audit": {
            "algebraic_phase_count_exhausts_prime_field_factor_band": True,
            "algebraic_phase_count_exhausts_extension_trace_band": False,
            "algebraic_major_certified_lift_containment_supplied_generically": False,
            "ambient_FI_or_k_log_field_supplied_generically": False,
            "growing_tail_entropy_verified_for_deployed_sequence": False,
            "required_consumer_uniformity_supplied_generically": False,
            "generic_A4_active_set_is_fiber_saturated": False,
            "intermediate_energies_supplied_by_A4_A5": False,
            "full_slice_partial_selections_in_complete_fibers_included": True,
            "incomplete_active_map_fibers_supported_by_UF10": False,
            "canonical_partial_occupancy_subprofiles_supported_by_UF10": False,
            "all_quotient_scales_overlap_assigned": False,
            "PR643_instantiates_uniform_fold": False,
            "full_A4_closed": False,
            "tex_modified": False,
        },
        "prior_art": {
            "PO3": "exact occupancy generating identity; not an aggregate payment",
            "EF7": "exact finite Fourier bookkeeping; not the uniform-fold compiler",
            "PR465": "pure cyclic fixed-degree count and exponential obstruction",
            "commit_75e5e32": "multilevel coefficient powers and signed LS wall",
            "minimal_phase_supplement":
                "collision and Parseval identity; not the all-degree compiler",
            "PR643": "negative applicability stress test only",
        },
        "source_sha256": source_hashes,
        "note_sha256": file_sha256(repo / NOTE_PATH),
        "verifier_sha256": file_sha256(repo / VERIFIER_PATH),
        "memory_cap_bytes": CAP_BYTES,
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_artifact(artifact: dict[str, Any], repo: Path, checks: Checks) -> None:
    checks.equal(artifact.get("schema"), SCHEMA, "artifact schema")
    checks.equal(artifact.get("status"), STATUS, "artifact status")
    checks.equal(artifact.get("base_commit"), BASE_COMMIT, "artifact base")
    checks.equal(artifact.get("payload_sha256"), payload_hash(artifact), "payload hash")
    checks.equal(artifact.get("memory_cap_bytes"), CAP_BYTES, "artifact cap")
    checks.equal(artifact.get("source_sha256"), SOURCE_HASHES, "source hash ledger")
    checks.equal(artifact.get("note_sha256"), file_sha256(repo / NOTE_PATH), "note hash")
    checks.equal(
        artifact.get("verifier_sha256"),
        file_sha256(repo / VERIFIER_PATH),
        "verifier hash",
    )

    theorems = artifact["theorems"]
    count = theorems["weighted_grs_count"]
    checks.equal(
        count["dimension_bound"],
        "floor((k-1)/d)+1=ceil(k/d)",
        "weighted count formula",
    )
    checks.equal(
        count["scope"],
        "global_B_valued_phase_factorization_on_every_exact_fiber",
        "weighted count scope",
    )
    checks.equal(count["floor_counterexample"]["factor_dimension"], 2, "counterexample dimension")
    checks.equal(count["floor_counterexample"]["false_floor"], 1, "counterexample false floor")
    checks.equal(count["floor_counterexample"]["sharp_ceiling"], 2, "counterexample ceiling")
    checks.equal(
        count["sparse_tail_condition"],
        "log(I_N)+ceil(k/D_N)*log(|B|)=o(N)",
        "exact sparse-tail condition",
    )
    tail = count["sparse_tail_hypotheses"]
    checks.equal(tail["global_every_fiber_factorization"], True, "global factorization hypothesis")
    checks.equal(
        tail["certified_effective_major_lift_containment_required"],
        True,
        "certified lift containment hypothesis",
    )
    checks.equal(tail["log_map_count_is_o_N_required"], True, "map-count entropy hypothesis")
    checks.equal(tail["k_log_field_is_O_N_required"], True, "ambient entropy hypothesis")
    checks.equal(tail["log_field_is_o_N_required"], True, "field entropy hypothesis")
    checks.equal(tail["minimum_degree_tends_to_infinity_required"], True, "growing degree hypothesis")
    checks.equal(
        tail["uniform_over_live_leaves_maps_and_received_lines_required"],
        True,
        "consumer uniformity hypothesis",
    )
    checks.equal(tail["generic_consumer_supplies_hypotheses"], False, "generic tail nonclaim")
    compiler = theorems["uniform_fold_compiler"]
    checks.equal(compiler["degrees_proved"], "every integer d>=2", "all fold degrees")
    checks.equal(compiler["common_target"], "A_phi=V_g/W_phi", "common target")
    checks.equal(compiler["loss"], "C_maj<=K_d(m)-1", "compiler loss")
    checks.equal([row["d"] for row in compiler["records"]], [2, 3, 4], "sample degrees")
    for row in compiler["records"]:
        checks.equal(
            row["endpoint_kappa"],
            [row["group_order"], 1],
            f"d={row['d']}: endpoint common-target kappa",
        )

    audit = artifact["hypothesis_audit"]
    checks.equal(audit["algebraic_phase_count_exhausts_prime_field_factor_band"], True, "prime trace split")
    checks.equal(audit["algebraic_phase_count_exhausts_extension_trace_band"], False, "extension trace split")
    checks.equal(
        audit["algebraic_major_certified_lift_containment_supplied_generically"],
        False,
        "generic lift-containment nonclaim",
    )
    checks.equal(
        audit["ambient_FI_or_k_log_field_supplied_generically"],
        False,
        "generic ambient-entropy nonclaim",
    )
    checks.equal(
        audit["growing_tail_entropy_verified_for_deployed_sequence"],
        False,
        "deployed tail nonclaim",
    )
    checks.equal(
        audit["required_consumer_uniformity_supplied_generically"],
        False,
        "generic uniformity nonclaim",
    )
    checks.equal(audit["generic_A4_active_set_is_fiber_saturated"], False, "active-set guard")
    checks.equal(audit["intermediate_energies_supplied_by_A4_A5"], False, "energy guard")
    checks.equal(
        audit["full_slice_partial_selections_in_complete_fibers_included"],
        True,
        "full-slice occupancy inclusion",
    )
    checks.equal(
        audit["incomplete_active_map_fibers_supported_by_UF10"],
        False,
        "incomplete-live-fiber guard",
    )
    checks.equal(
        audit["canonical_partial_occupancy_subprofiles_supported_by_UF10"],
        False,
        "PO3-subprofile guard",
    )
    checks.equal(audit["all_quotient_scales_overlap_assigned"], False, "overlap guard")
    checks.equal(audit["PR643_instantiates_uniform_fold"], False, "PR643 guard")
    checks.equal(audit["full_A4_closed"], False, "A4 nonclaim")
    checks.equal(audit["tex_modified"], False, "TeX nonclaim")


def tamper_selftest(artifact: dict[str, Any], repo: Path, checks: Checks) -> int:
    mutations = [
        ("floor-for-ceiling", lambda x: x["theorems"]["weighted_grs_count"].__setitem__(
            "dimension_bound", "floor(k/d)"
        )),
        ("local-one-fiber-scope", lambda x: x["theorems"]["weighted_grs_count"].__setitem__(
            "scope", "constant_on_one_routed_fiber"
        )),
        ("erase-trace-split", lambda x: x["hypothesis_audit"].__setitem__(
            "algebraic_phase_count_exhausts_extension_trace_band", True
        )),
        ("weaken-sparse-tail", lambda x: x["theorems"]["weighted_grs_count"].__setitem__(
            "sparse_tail_condition", "k*log(|B|)=O(N)"
        )),
        ("erase-certified-lift", lambda x: x["theorems"]["weighted_grs_count"]["sparse_tail_hypotheses"].__setitem__(
            "certified_effective_major_lift_containment_required", False
        )),
        ("assume-generic-ambient-entropy", lambda x: x["hypothesis_audit"].__setitem__(
            "ambient_FI_or_k_log_field_supplied_generically", True
        )),
        ("claim-deployed-tail", lambda x: x["hypothesis_audit"].__setitem__(
            "growing_tail_entropy_verified_for_deployed_sequence", True
        )),
        ("erase-uniformity", lambda x: x["theorems"]["weighted_grs_count"]["sparse_tail_hypotheses"].__setitem__(
            "uniform_over_live_leaves_maps_and_received_lines_required", False
        )),
        ("assume-generic-uniformity", lambda x: x["hypothesis_audit"].__setitem__(
            "required_consumer_uniformity_supplied_generically", True
        )),
        ("wrong-common-target", lambda x: x["theorems"]["uniform_fold_compiler"].__setitem__(
            "common_target", "one_effective_target_per_weight"
        )),
        ("endpoint-kappa-one", lambda x: x["theorems"]["uniform_fold_compiler"]["records"][0].__setitem__(
            "endpoint_kappa", [1, 1]
        )),
        ("only-two-fold", lambda x: x["theorems"]["uniform_fold_compiler"].__setitem__(
            "degrees_proved", "d=2 only"
        )),
        ("assume-intermediate-energy", lambda x: x["hypothesis_audit"].__setitem__(
            "intermediate_energies_supplied_by_A4_A5", True
        )),
        ("allow-incomplete-live-fibers", lambda x: x["hypothesis_audit"].__setitem__(
            "incomplete_active_map_fibers_supported_by_UF10", True
        )),
        ("claim-PO3-subprofile", lambda x: x["hypothesis_audit"].__setitem__(
            "canonical_partial_occupancy_subprofiles_supported_by_UF10", True
        )),
        ("erase-full-slice-occupancy", lambda x: x["hypothesis_audit"].__setitem__(
            "full_slice_partial_selections_in_complete_fibers_included", False
        )),
        ("assume-generic-saturation", lambda x: x["hypothesis_audit"].__setitem__(
            "generic_A4_active_set_is_fiber_saturated", True
        )),
        ("claim-PR643-instance", lambda x: x["hypothesis_audit"].__setitem__(
            "PR643_instantiates_uniform_fold", True
        )),
        ("claim-full-A4", lambda x: x["hypothesis_audit"].__setitem__(
            "full_A4_closed", True
        )),
        ("claim-TeX-edit", lambda x: x["hypothesis_audit"].__setitem__(
            "tex_modified", True
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
        except (CheckFailure, KeyError, TypeError):
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

    mode = []
    if args.write:
        mode.append("write")
    if args.check:
        mode.append("check")
    if args.tamper_selftest:
        mode.append(f"tamper={rejected}")
    if not mode:
        mode.append("default")
    print(
        f"RESULT: PASS ({checks.count} checks; mode={','.join(mode)}; "
        f"cap={cap}; payload={artifact['payload_sha256']})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, KeyError, ValueError, TypeError) as exc:
        print(f"RESULT: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
