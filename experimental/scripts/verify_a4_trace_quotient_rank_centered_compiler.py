#!/usr/bin/env python3
"""Verify the A4 trace-rank and centered uniform-fold successor packet."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import resource
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "a4_trace_quotient_rank_centered_compiler.v1"
STATUS = "PROVED_TRACE_RANK_AND_CENTERED_UNIFORM_FOLD_COMPILER"
BASE_COMMIT = "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532"
PARENT_COMMIT = "6a1e520871dd23ab8a536f4dcd423820990feef1"
CAP_BYTES = 1024**3
NOTE_PATH = Path(
    "experimental/notes/thresholds/"
    "a4_trace_quotient_rank_centered_compiler.md"
)
VERIFIER_PATH = Path(
    "experimental/scripts/"
    "verify_a4_trace_quotient_rank_centered_compiler.py"
)
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/a4-trace-quotient-rank-centered/"
    "a4_trace_quotient_rank_centered_compiler.json"
)
SOURCE_HASHES = {
    "experimental/asymptotic_rs_mca_frontiers.tex":
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
    "experimental/notes/thresholds/a4_quotient_major_compiler.md":
        "4b924af30dc444ab770620cede6895fca47674e64e97d519ecbfa83bd6939222",
    "experimental/scripts/verify_a4_quotient_major_compiler.py":
        "aa233b7815deac1a714c48ca0dae1e4a60334b39672a20bc8cc36e423ea1fa24",
    "experimental/data/certificates/a4-quotient-major-compiler/"
    "a4_quotient_major_compiler.json":
        "c61e116a2c71b29d37263bf6ac1633ed557659adb04e142ac92451231e7fb91b",
    "experimental/notes/roadmaps/b2_l1_reduction_ledger.md":
        "bd35b82b5cec35639b0bf539e15709b53e3316dae0c2b8e298953db424fb0435",
    "experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md":
        "7545779b5ca3454007508b74dd225abab716ae809ad6c7ebe08dcfd716359b25",
    "experimental/notes/thresholds/cap25_v13_qfin_rung_audit_m31.md":
        "b038245aa27ee397f67e8821ba64c6f8d766734eb73c7e1afe177e3230f042d7",
    "experimental/grande_finale.tex":
        "4e3c3f6a898969e5fad70cd09bf354c6a2a12d54bf94525fb62f457dd17ddbc8",
}
EXPECTED_CALIBRATIONS = {
    "KB": {
        "log2_b2": -27.950587886402972,
        "center_log2_average": 28.450587711560137,
        "saddle_scale": 1280.7343136235977,
    },
    "M31": {
        "log2_b2": -20.459194784553773,
        "center_log2_average": 20.959194609712973,
        "saddle_scale": 1280.736207355009,
    },
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

    def close(self, left: float, right: float, tolerance: float, label: str) -> None:
        self.require(
            math.isfinite(left)
            and math.isfinite(right)
            and abs(left - right) <= tolerance,
            f"{label}: {left!r} not within {tolerance} of {right!r}",
        )


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


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def without_hash(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    result.pop("payload_sha256", None)
    return result


def payload_hash(value: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(without_hash(value))).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        if not (root / NOTE_PATH).is_file():
            raise CheckFailure("explicit repo is missing the successor note")
        return root
    env = os.environ.get("A4_TRACE_RANK_REPO")
    if env:
        return locate_repo(Path(env))
    candidates = [Path.cwd().resolve(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / NOTE_PATH).is_file():
            return candidate
    raise CheckFailure("pass --repo or set A4_TRACE_RANK_REPO")


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
    columns = len(data[0])
    cursor = 0
    pivots: list[int] = []
    for column in range(columns):
        pivot = next(
            (row for row in range(cursor, rows) if data[row][column]),
            None,
        )
        if pivot is None:
            continue
        data[cursor], data[pivot] = data[pivot], data[cursor]
        scale = inv_mod(data[cursor][column], p)
        data[cursor] = [(scale * entry) % p for entry in data[cursor]]
        for row in range(rows):
            if row == cursor or data[row][column] == 0:
                continue
            factor = data[row][column]
            data[row] = [
                (left - factor * right) % p
                for left, right in zip(data[row], data[cursor])
            ]
        pivots.append(column)
        cursor += 1
        if cursor == rows:
            break
    return data, pivots


def rank_mod(matrix: list[list[int]], p: int) -> int:
    return len(rref(matrix, p)[1]) if matrix else 0


def row_basis(matrix: list[list[int]], p: int) -> list[list[int]]:
    reduced, _ = rref(matrix, p)
    return [row for row in reduced if any(row)]


def nullspace(matrix: list[list[int]], p: int, columns: int) -> list[list[int]]:
    if not matrix:
        return [
            [1 if i == j else 0 for i in range(columns)]
            for j in range(columns)
        ]
    reduced, pivots = rref(matrix, p)
    free = [column for column in range(columns) if column not in pivots]
    basis: list[list[int]] = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = (-reduced[row][free_column]) % p
        basis.append(vector)
    return basis


def vector_sub(left: list[int], right: list[int], p: int) -> list[int]:
    return [(a - b) % p for a, b in zip(left, right)]


def dot(left: list[int], right: list[int], p: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % p


def linear_combinations(
    basis: list[list[int]], p: int, dimension: int
) -> Iterable[list[int]]:
    if not basis:
        yield [0] * dimension
        return
    for coefficients in product(range(p), repeat=len(basis)):
        vector = [0] * dimension
        for coefficient, generator in zip(coefficients, basis):
            for index, entry in enumerate(generator):
                vector[index] = (
                    vector[index] + coefficient * entry
                ) % p
        yield vector


def partition_rows(
    g: list[list[int]], fibers: list[list[int]], p: int
) -> list[list[int]]:
    rows: list[list[int]] = []
    for fiber in fibers:
        representative = fiber[0]
        for point in fiber[1:]:
            rows.append(vector_sub(g[point], g[representative], p))
    return rows


def trace_rank_record(
    checks: Checks,
    *,
    name: str,
    p: int,
    g: list[list[int]],
    fibers: list[list[int]],
    enumerate_ambient: bool,
) -> dict[str, Any]:
    checks.require(bool(g), f"{name}: nonempty point set")
    ambient = len(g[0])
    checks.require(
        all(len(vector) == ambient for vector in g),
        f"{name}: rectangular vectors",
    )
    flattened = sorted(point for fiber in fibers for point in fiber)
    checks.equal(flattened, list(range(len(g))), f"{name}: partition")
    checks.require(all(fiber for fiber in fibers), f"{name}: nonempty fibers")

    v_rows = [vector_sub(vector, g[0], p) for vector in g]
    w_rows = partition_rows(g, fibers, p)
    v = rank_mod(v_rows, p)
    w = rank_mod(w_rows, p)
    q = len(fibers)
    checks.equal(rank_mod(v_rows + w_rows, p), v, f"{name}: W subset V")
    checks.require(v >= w, f"{name}: quotient rank nonnegative")

    base_fiber = next(index for index, fiber in enumerate(fibers) if 0 in fiber)
    representatives = [fiber[0] for fiber in fibers]
    representative_rows = [
        vector_sub(g[representatives[index]], g[representatives[base_fiber]], p)
        for index in range(q)
        if index != base_fiber
    ]
    quotient_rank = rank_mod(w_rows + representative_rows, p) - w
    checks.equal(quotient_rank, v - w, f"{name}: representative generation")
    checks.require(v - w <= q - 1, f"{name}: q minus one bound")

    z_basis = nullspace(w_rows, p, ambient)
    kernel_basis = nullspace(v_rows, p, ambient)
    checks.equal(len(z_basis), ambient - w, f"{name}: W annihilator")
    checks.equal(len(kernel_basis), ambient - v, f"{name}: V annihilator")
    checks.equal(
        len(z_basis) - len(kernel_basis),
        v - w,
        f"{name}: exact-sequence dimension",
    )

    enumeration: dict[str, Any] | None = None
    if enumerate_ambient:
        checks.require(p ** len(z_basis) <= 200000, f"{name}: enumeration cap")
        v_basis = row_basis(v_rows, p)
        restrictions: set[tuple[int, ...]] = set()
        kernel_count = 0
        ambient_solutions = 0
        for alpha in linear_combinations(z_basis, p, ambient):
            ambient_solutions += 1
            for fiber in fibers:
                values = {dot(alpha, g[point], p) for point in fiber}
                checks.equal(len(values), 1, f"{name}: fiber constancy")
            restriction = tuple(dot(alpha, vector, p) for vector in v_basis)
            restrictions.add(restriction)
            if all(value == 0 for value in restriction):
                kernel_count += 1
        checks.equal(
            ambient_solutions,
            p ** (ambient - w),
            f"{name}: ambient solution count",
        )
        checks.equal(
            len(restrictions),
            p ** (v - w),
            f"{name}: effective restriction count",
        )
        checks.equal(
            kernel_count,
            p ** (ambient - v),
            f"{name}: annihilator multiplicity",
        )
        enumeration = {
            "ambient_solutions": ambient_solutions,
            "distinct_effective_restrictions": len(restrictions),
            "annihilator_multiplicity": kernel_count,
        }

    return {
        "name": name,
        "p": p,
        "N": len(g),
        "ambient_dimension": ambient,
        "fiber_sizes": [len(fiber) for fiber in fibers],
        "q": q,
        "v": v,
        "w_phi": w,
        "effective_dimension": v - w,
        "ambient_solution_dimension": ambient - w,
        "annihilator_dimension": ambient - v,
        "effective_count": p ** (v - w),
        "q_minus_one_count_bound": p ** (q - 1),
        "enumeration": enumeration,
    }


def weighted_vandermonde(
    p: int, points: list[int], redundancy: int
) -> list[list[int]]:
    rows: list[list[int]] = []
    for point in points:
        weight = pow(point, 2, p)
        value = weight
        row: list[int] = []
        for _ in range(redundancy):
            row.append(value)
            value = value * point % p
        rows.append(row)
    return rows


def trace_rank_suite(checks: Checks) -> list[dict[str, Any]]:
    records = [
        trace_rank_record(
            checks,
            name="F2_exact_pairs",
            p=2,
            g=[
                [0, 0, 0, 0],
                [1, 0, 0, 1],
                [0, 1, 0, 1],
                [1, 1, 0, 0],
                [0, 0, 1, 1],
                [1, 0, 1, 0],
            ],
            fibers=[[0, 1], [2, 3], [4, 5]],
            enumerate_ambient=True,
        ),
        trace_rank_record(
            checks,
            name="F3_nonuniform",
            p=3,
            g=[
                [0, 0, 0, 0],
                [1, 0, 1, 1],
                [0, 1, 1, 2],
                [1, 1, 2, 0],
                [2, 1, 0, 1],
            ],
            fibers=[[0, 1, 2], [3], [4]],
            enumerate_ambient=True,
        ),
        trace_rank_record(
            checks,
            name="F3_single_fiber",
            p=3,
            g=[
                [0, 0, 0],
                [1, 0, 1],
                [0, 1, 1],
                [1, 1, 2],
            ],
            fibers=[[0, 1, 2, 3]],
            enumerate_ambient=True,
        ),
    ]

    p = 17
    points = list(range(1, p))
    g = weighted_vandermonde(p, points, len(points))
    by_square: dict[int, list[int]] = {}
    for index, point in enumerate(points):
        by_square.setdefault(pow(point, 2, p), []).append(index)
    fibers = [by_square[key] for key in sorted(by_square)]
    sharp = trace_rank_record(
        checks,
        name="F17_weighted_vandermonde_sharp",
        p=p,
        g=g,
        fibers=fibers,
        enumerate_ambient=False,
    )
    checks.equal(rank_mod(g, p), len(points), "sharp: independent columns")
    checks.equal(sharp["v"], len(points) - 1, "sharp: V rank")
    checks.equal(sharp["w_phi"], len(points) - len(fibers), "sharp: W rank")
    checks.equal(
        sharp["effective_dimension"],
        len(fibers) - 1,
        "sharp: q minus one attained",
    )
    sharp["sharp"] = True
    sharp["legal_A5_large_characteristic"] = len(points) < p
    records.append(sharp)
    return records


def subset_sum_counts(h: list[int], weight: int, group_size: int) -> list[int]:
    counts = [0] * group_size
    for subset in combinations(range(len(h)), weight):
        total = 0
        for index in subset:
            total ^= h[index]
        counts[total] += 1
    return counts


def character_sum(counts: list[int], character: int) -> int:
    return sum(
        multiplicity
        * (-1 if (character & element).bit_count() % 2 else 1)
        for element, multiplicity in enumerate(counts)
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


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def centered_case(
    checks: Checks, *, name: str, rank: int, h: list[int]
) -> dict[str, Any]:
    group_size = 2**rank
    checks.require(
        all(0 <= value < group_size for value in h),
        f"{name}: target values",
    )
    n = len(h)
    m_values = [math.comb(n, weight) for weight in range(n + 1)]
    eta: list[Fraction] = []
    e_by_weight: list[list[int]] = []
    for weight, m_value in enumerate(m_values):
        counts = subset_sum_counts(h, weight, group_size)
        sp = sum(value * value for value in counts)
        kappa = Fraction(group_size * sp, m_value * m_value)
        centered = kappa - 1
        checks.require(centered >= 0, f"{name}: eta nonnegative {weight}")
        checks.require(
            centered <= group_size - 1,
            f"{name}: eta upper bound {weight}",
        )
        e_values = [
            character_sum(counts, character)
            for character in range(group_size)
        ]
        centered_parseval = sum(value * value for value in e_values[1:])
        checks.equal(
            Fraction(centered_parseval, 1),
            centered * m_value * m_value,
            f"{name}: centered Parseval {weight}",
        )
        eta.append(centered)
        e_by_weight.append(e_values)
    checks.equal(eta[0], Fraction(group_size - 1), f"{name}: eta zero")
    checks.equal(eta[n], Fraction(group_size - 1), f"{name}: eta full")

    fold_records: list[dict[str, Any]] = []
    for degree in (2, 3, 4):
        powered_holder_checks = 0
        convolution_checks = 0
        numerical_compiler_checks = 0
        minimum_margin = float("inf")
        values_by_character = [
            [
                -1 if (character & element).bit_count() % 2 else 1
                for element in h
                for _ in range(degree)
            ]
            for character in range(group_size)
        ]
        tuples = list(product(range(n + 1), repeat=degree))
        for total_weight in range(degree * n + 1):
            compositions = [
                item for item in tuples if sum(item) == total_weight
            ]
            denominator = math.comb(degree * n, total_weight)
            full_e = [
                elementary_coeff(values, total_weight)
                for values in values_by_character
            ]
            for character in range(group_size):
                expanded = sum(
                    math.prod(
                        e_by_weight[weight][character]
                        for weight in composition
                    )
                    for composition in compositions
                )
                checks.equal(
                    expanded,
                    full_e[character],
                    f"{name}: convolution d={degree} m={total_weight} "
                    f"chi={character}",
                )
                convolution_checks += 1

            k_centered = 0.0
            k_uncentered = 0.0
            for composition in compositions:
                left = sum(
                    math.prod(
                        abs(e_by_weight[weight][character])
                        for weight in composition
                    )
                    for character in range(1, group_size)
                )
                rhs_power = Fraction(1, 1)
                for weight in composition:
                    rhs_power *= eta[weight] * m_values[weight] ** degree
                checks.require(
                    Fraction(left**degree, 1) <= rhs_power,
                    f"{name}: powered Holder d={degree} "
                    f"composition={composition}",
                )
                powered_holder_checks += 1

                probability = (
                    math.prod(m_values[weight] for weight in composition)
                    / denominator
                )
                centered_root = math.prod(
                    float(eta[weight]) ** (1.0 / degree)
                    for weight in composition
                )
                uncentered_root = math.prod(
                    float(eta[weight] + 1) ** (1.0 / degree)
                    for weight in composition
                )
                k_centered += probability * centered_root
                k_uncentered += probability * uncentered_root

            actual = sum(abs(value) for value in full_e[1:]) / denominator
            checks.require(
                actual <= k_centered + 1e-10,
                f"{name}: centered compiler d={degree} m={total_weight}",
            )
            checks.require(
                k_centered <= k_uncentered - 1 + 1e-10,
                f"{name}: centered no worse d={degree} m={total_weight}",
            )
            numerical_compiler_checks += 2
            minimum_margin = min(minimum_margin, k_centered - actual)

        fold_records.append(
            {
                "degree": degree,
                "convolution_checks": convolution_checks,
                "powered_holder_checks": powered_holder_checks,
                "numerical_compiler_checks": numerical_compiler_checks,
                "minimum_centered_margin": format(minimum_margin, ".12g"),
            }
        )

    return {
        "name": name,
        "target": f"F2^{rank}",
        "h": h,
        "eta": [fraction_text(value) for value in eta],
        "endpoint_eta": [fraction_text(eta[0]), fraction_text(eta[-1])],
        "folds": fold_records,
    }


def polynomial(values: list[int]) -> list[int]:
    coefficients = [1]
    for value in values:
        next_coefficients = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            next_coefficients[index] += coefficient
            next_coefficients[index + 1] += value * coefficient
        coefficients = next_coefficients
    return coefficients


def centered_suite(checks: Checks) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    records = [
        centered_case(
            checks,
            name="surjective_F2_square",
            rank=2,
            h=[0, 1, 2, 3],
        ),
        centered_case(
            checks,
            name="repeated_F2_square",
            rank=2,
            h=[0, 1, 1, 2, 3],
        ),
    ]
    true_coefficients = polynomial([1, -1, -1, -1])
    fake_coefficients = polynomial([1, 1, -1, -1])
    checks.require(
        true_coefficients != fake_coefficients,
        "nonuniform multiplicities falsify uniform power",
    )
    falsifier = {
        "fiber_multiplicities": [1, 3],
        "character_values": [1, -1],
        "true_coefficients": true_coefficients,
        "fake_degree_two_coefficients": fake_coefficients,
        "uniform_fold_identity_valid": False,
    }
    return records, falsifier


def b2_calibration(
    checks: Checks,
    *,
    name: str,
    n: int,
    m: int,
    p: int,
    rank: int,
    k_raw: int,
) -> dict[str, Any]:
    low = max(0, m - n)
    high = min(n, m)
    mode = m // 2
    checks.require(low <= mode <= high, f"{name}: valid mode")
    checks.equal(m % 2, 0, f"{name}: even slice")
    checks.equal(mode - low, high - mode, f"{name}: symmetric range")

    normalized_terms = [1.0]
    term = 1.0
    for weight in range(mode, high):
        ratio = math.sqrt(
            ((n - weight) / (weight + 1))
            * ((m - weight) / (n - m + weight + 1))
        )
        term *= ratio
        normalized_terms.append(2.0 * term)
    checks.equal(
        2 * len(normalized_terms) - 1,
        high - low + 1,
        f"{name}: symmetric recurrence term count",
    )
    saddle_scale = math.fsum(normalized_terms)
    checks.close(
        saddle_scale,
        EXPECTED_CALIBRATIONS[name]["saddle_scale"],
        1e-11,
        f"{name}: scaled saddle recurrence",
    )

    with localcontext() as context:
        context.prec = 70
        ln_two = Decimal(2).ln()
        ln_central = Decimal(math.comb(n, mode)).ln()
        ln_full = Decimal(math.comb(2 * n, m)).ln()
        ln_target = Decimal(rank) * Decimal(p).ln()
        ln_saddle = Decimal(format(saddle_scale, ".17g")).ln()
        ln_b2 = ln_target + ln_central + ln_saddle - ln_full
        log_b2 = ln_b2 / ln_two
        b2 = ln_b2.exp()
        center_log_average = (ln_central - ln_target) / ln_two

    checks.close(
        float(log_b2),
        EXPECTED_CALIBRATIONS[name]["log2_b2"],
        2e-12,
        f"{name}: pinned log2 B2",
    )
    checks.close(
        float(center_log_average),
        EXPECTED_CALIBRATIONS[name]["center_log2_average"],
        2e-12,
        f"{name}: center average pin",
    )
    standalone_allowance = k_raw - 1
    c_ceiling = Decimal(standalone_allowance) / b2
    return {
        "name": name,
        "full_domain_size": 2 * n,
        "quotient_size": n,
        "m": m,
        "p": p,
        "quotient_rank": rank,
        "target_order": f"{p}^{rank}",
        "j_low": low,
        "j_high": high,
        "mode": mode,
        "term_count": high - low + 1,
        "log2_b2": format(log_b2, ".12f"),
        "b2": format(b2, ".13g"),
        "n_times_b2": format(n * b2, ".12g"),
        "center_log2_average": format(center_log_average, ".12f"),
        "saddle_scale": format(saddle_scale, ".16g"),
        "k_raw": k_raw,
        "standalone_nontrivial_ceiling": standalone_allowance,
        "conditional_c_ceiling": format(c_ceiling, ".12g"),
        "conditional_c_ceiling_over_n": format(c_ceiling / n, ".12g"),
        "other_fourier_losses_assigned_zero": False,
        "diagonal_energy_proved": False,
        "row_closed": False,
    }


def calibration_suite(checks: Checks) -> list[dict[str, Any]]:
    return [
        b2_calibration(
            checks,
            name="KB",
            n=2**20,
            m=1116048,
            p=2130706433,
            rank=33735,
            k_raw=4807520,
        ),
        b2_calibration(
            checks,
            name="M31",
            n=2**20,
            m=1116024,
            p=2147483647,
            rank=33723,
            k_raw=9,
        ),
    ]


def source_gate(repo: Path, checks: Checks) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in SOURCE_HASHES.items():
        digest = file_sha256(repo / relative)
        checks.equal(digest, expected, f"source hash {relative}")
        observed[relative] = digest
    return observed


def build_artifact(repo: Path, checks: Checks) -> dict[str, Any]:
    sources = source_gate(repo, checks)
    trace_records = trace_rank_suite(checks)
    centered_records, nonuniform_falsifier = centered_suite(checks)
    calibrations = calibration_suite(checks)
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
                "experimental/notes/thresholds/a4_quotient_major_compiler.md"
            ],
            "verifier_sha256": SOURCE_HASHES[
                "experimental/scripts/verify_a4_quotient_major_compiler.py"
            ],
            "certificate_sha256": SOURCE_HASHES[
                "experimental/data/certificates/a4-quotient-major-compiler/"
                "a4_quotient_major_compiler.json"
            ],
            "non_log_files_preserved": True,
        },
        "theorems": {
            "trace_rank": {
                "ambient_solution_space": "W_phi^perp",
                "ambient_solution_dimension": "sR-w_phi",
                "restriction_kernel": "V^perp",
                "annihilator_dimension": "sR-v",
                "effective_group": "dual(V/W_phi)",
                "effective_count": "p^(v-w_phi)",
                "universal_bound": "p^(q-1)",
                "exact_d_fold_bound": "p^(N/d-1)",
                "nonuniform_uses_actual_q": True,
                "global_every_block_required": True,
                "algebraic_lift_containment_required": False,
                "sharp_weighted_vandermonde": True,
                "sparse_tail_condition":
                    "log|I_N|+(N/D_N)log(p_N)=o(N)",
                "map_family_entropy_required": True,
                "characteristic_growth_required": True,
                "extension_degree_enters_bound": False,
                "fixed_degree_sparse": False,
                "records": trace_records,
            },
            "centered_uniform_fold": {
                "eta_definition": "eta_j=kappa_j-1",
                "centered_parseval":
                    "sum_(chi!=1)|e_j(chi)|^2=eta_j*M_j^2",
                "endpoint_eta": "|A_phi|-1",
                "common_target_required": True,
                "trivial_character_in_major_set": False,
                "exact_uniform_fibers_required": True,
                "degrees_proved": "all d>=2",
                "bound":
                    "Cmaj<=sum_jvec w_jvec prod_s eta_(j_s)^(1/d)",
                "comparison": "K_centered<=K_uncentered-1",
                "strict_on_every_instance": False,
                "records": centered_records,
                "nonuniform_falsifier": nonuniform_falsifier,
            },
            "diagonal_energy_consumer": {
                "hypothesis":
                    "SP_j-M_j^2/|A_phi|<=C_n*M_j",
                "status": "OPEN",
                "owner": "PR564_subgroup_VMVT_Poisson_energy_frontier",
                "consequence":
                    "Cmaj<=C_n*B_d(n,m,A_phi)",
                "claimed_proved": False,
                "calibrations": calibrations,
            },
        },
        "hypothesis_audit": {
            "generic_A4_active_set_fiber_saturated": False,
            "generic_A4_target_rank_equals_full_identity_rank": False,
            "generic_map_entropy_and_logp_over_D_supplied": False,
            "incomplete_fibers_supported_by_centered_power": False,
            "weightwise_effective_targets_allowed": False,
            "centered_energy_supplied": False,
            "PR564_energy_reclaimed_as_new": False,
            "other_fourier_losses_zero": False,
            "other_cell_overlap_assignment_unnecessary": False,
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

    trace = artifact["theorems"]["trace_rank"]
    checks.equal(trace["ambient_solution_space"], "W_phi^perp", "trace ambient")
    checks.equal(trace["effective_count"], "p^(v-w_phi)", "trace effective")
    checks.equal(trace["universal_bound"], "p^(q-1)", "trace q bound")
    checks.equal(trace["exact_d_fold_bound"], "p^(N/d-1)", "trace fold bound")
    checks.equal(trace["nonuniform_uses_actual_q"], True, "actual q guard")
    checks.equal(trace["global_every_block_required"], True, "global guard")
    checks.equal(
        trace["algebraic_lift_containment_required"],
        False,
        "trace lift independence",
    )
    checks.equal(trace["sharp_weighted_vandermonde"], True, "trace sharpness")
    checks.equal(
        trace["sparse_tail_condition"],
        "log|I_N|+(N/D_N)log(p_N)=o(N)",
        "trace entropy",
    )
    checks.equal(trace["map_family_entropy_required"], True, "map entropy")
    checks.equal(
        trace["characteristic_growth_required"],
        True,
        "characteristic growth",
    )
    checks.equal(
        trace["extension_degree_enters_bound"],
        False,
        "extension degree guard",
    )
    checks.equal(trace["fixed_degree_sparse"], False, "fixed-degree nonclaim")
    for record in trace["records"]:
        checks.equal(
            record["ambient_solution_dimension"],
            record["ambient_dimension"] - record["w_phi"],
            f"{record['name']}: ambient dimension record",
        )
        checks.equal(
            record["annihilator_dimension"],
            record["ambient_dimension"] - record["v"],
            f"{record['name']}: annihilator record",
        )
        checks.equal(
            record["effective_dimension"],
            record["v"] - record["w_phi"],
            f"{record['name']}: effective dimension record",
        )
        checks.equal(
            record["effective_count"],
            record["p"] ** record["effective_dimension"],
            f"{record['name']}: effective count record",
        )
        checks.require(
            record["effective_count"] <= record["q_minus_one_count_bound"],
            f"{record['name']}: q bound record",
        )

    centered = artifact["theorems"]["centered_uniform_fold"]
    checks.equal(centered["eta_definition"], "eta_j=kappa_j-1", "eta definition")
    checks.equal(centered["endpoint_eta"], "|A_phi|-1", "eta endpoint")
    checks.equal(centered["common_target_required"], True, "common target")
    checks.equal(
        centered["trivial_character_in_major_set"],
        False,
        "trivial exclusion",
    )
    checks.equal(
        centered["exact_uniform_fibers_required"],
        True,
        "uniform fiber guard",
    )
    checks.equal(centered["degrees_proved"], "all d>=2", "all degrees")
    checks.equal(
        centered["comparison"],
        "K_centered<=K_uncentered-1",
        "centered comparison",
    )
    checks.equal(
        centered["strict_on_every_instance"],
        False,
        "equality-possible guard",
    )
    checks.equal(
        centered["nonuniform_falsifier"]["uniform_fold_identity_valid"],
        False,
        "nonuniform falsifier",
    )
    for record in centered["records"]:
        checks.require(bool(record["folds"]), f"{record['name']}: fold records")
        checks.equal(
            record["endpoint_eta"][0],
            record["endpoint_eta"][1],
            f"{record['name']}: endpoint equality",
        )

    energy = artifact["theorems"]["diagonal_energy_consumer"]
    checks.equal(energy["status"], "OPEN", "energy status")
    checks.equal(
        energy["owner"],
        "PR564_subgroup_VMVT_Poisson_energy_frontier",
        "energy provenance",
    )
    checks.equal(energy["claimed_proved"], False, "energy nonclaim")
    for row in energy["calibrations"]:
        expected = EXPECTED_CALIBRATIONS[row["name"]]
        checks.close(
            float(row["log2_b2"]),
            expected["log2_b2"],
            2e-12,
            f"{row['name']}: calibration validation",
        )
        checks.equal(row["diagonal_energy_proved"], False, f"{row['name']}: energy open")
        checks.equal(row["row_closed"], False, f"{row['name']}: row open")
        checks.equal(
            row["other_fourier_losses_assigned_zero"],
            False,
            f"{row['name']}: other losses unassigned",
        )

    audit = artifact["hypothesis_audit"]
    expected_audit = {
        "generic_A4_active_set_fiber_saturated": False,
        "generic_A4_target_rank_equals_full_identity_rank": False,
        "generic_map_entropy_and_logp_over_D_supplied": False,
        "incomplete_fibers_supported_by_centered_power": False,
        "weightwise_effective_targets_allowed": False,
        "centered_energy_supplied": False,
        "PR564_energy_reclaimed_as_new": False,
        "other_fourier_losses_zero": False,
        "other_cell_overlap_assignment_unnecessary": False,
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
        ("ambient-as-effective", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "effective_count", "p^(sR-w_phi)"
        )),
        ("drop-q-minus-one", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "universal_bound", "p^q"
        )),
        ("nonuniform-use-N-over-d", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "nonuniform_uses_actual_q", False
        )),
        ("local-one-fiber", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "global_every_block_required", False
        )),
        ("erase-map-entropy", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "map_family_entropy_required", False
        )),
        ("erase-characteristic-growth", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "characteristic_growth_required", False
        )),
        ("extension-degree-cost", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "extension_degree_enters_bound", True
        )),
        ("claim-fixed-degree-sparse", lambda x: x["theorems"]["trace_rank"].__setitem__(
            "fixed_degree_sparse", True
        )),
        ("include-trivial", lambda x: x["theorems"]["centered_uniform_fold"].__setitem__(
            "trivial_character_in_major_set", True
        )),
        ("zero-endpoint", lambda x: x["theorems"]["centered_uniform_fold"].__setitem__(
            "endpoint_eta", "0"
        )),
        ("weightwise-target", lambda x: x["theorems"]["centered_uniform_fold"].__setitem__(
            "common_target_required", False
        )),
        ("allow-nonuniform-power", lambda x: x["theorems"]["centered_uniform_fold"].__setitem__(
            "exact_uniform_fibers_required", False
        )),
        ("claim-strict-always", lambda x: x["theorems"]["centered_uniform_fold"].__setitem__(
            "strict_on_every_instance", True
        )),
        ("claim-energy-proved", lambda x: x["theorems"]["diagonal_energy_consumer"].__setitem__(
            "claimed_proved", True
        )),
        ("erase-PR564-credit", lambda x: x["theorems"]["diagonal_energy_consumer"].__setitem__(
            "owner", "new_here"
        )),
        ("assume-generic-rank", lambda x: x["hypothesis_audit"].__setitem__(
            "generic_A4_target_rank_equals_full_identity_rank", True
        )),
        ("assume-other-losses-zero", lambda x: x["hypothesis_audit"].__setitem__(
            "other_fourier_losses_zero", True
        )),
        ("claim-full-MA", lambda x: x["hypothesis_audit"].__setitem__(
            "full_MA_closed", True
        )),
        ("claim-deployed-row", lambda x: x["hypothesis_audit"].__setitem__(
            "deployed_row_closed", True
        )),
        ("claim-TeX", lambda x: x["hypothesis_audit"].__setitem__(
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
