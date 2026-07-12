#!/usr/bin/env python3
"""Hardened finite verifier for the experimental A6 U(2,L) rank packet."""

from __future__ import annotations

import ast
import hashlib
import itertools
import math
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tempfile
from fractions import Fraction


P = 11
ROOT = Path(__file__).resolve().parents[2]
NOTE = ROOT / "experimental/notes/thresholds/a6_u2_five_slope_rank_preflight.md"
TAMPER = os.environ.get("A6_U2_TAMPER", "")
VALID_TAMPERS = {
    "census",
    "representative",
    "operator",
    "kernel",
    "parameters",
    "core_rank",
    "five_count",
    "note_marker",
}


class VerificationError(RuntimeError):
    """Raised when a semantic verification gate fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def elementary_symmetric(values: tuple[int, ...], p: int = P) -> list[int]:
    out = [1]
    for value in values:
        out.append(0)
        for j in range(len(out) - 1, 0, -1):
            out[j] = (out[j] + value * out[j - 1]) % p
    return out


def poly_eval(coefficients: list[int], x: int, p: int = P) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % p
    return value


def matrix_rank(matrix: list[list[int]], p: int = P) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged matrix")
    work = [[entry % p for entry in row] for row in matrix]
    rank = 0
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column] % p),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(entry * inverse) % p for entry in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            multiplier = work[row][column] % p
            if multiplier:
                work[row] = [
                    (left - multiplier * right) % p
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def dot(left: list[int], right: list[int], p: int = P) -> int:
    require(len(left) == len(right), "dot-product length mismatch")
    return sum(a * b for a, b in zip(left, right)) % p


def seed_census() -> tuple[dict[int, list[tuple[int, ...]]], int]:
    fiber: list[tuple[tuple[int, ...], int]] = []
    for subset in itertools.combinations(range(1, P), 7):
        e = elementary_symmetric(subset)
        if e[1] == 6:
            fiber.append((subset, e[2]))
    candidates: dict[int, list[tuple[int, ...]]] = {}
    for subset, slope in fiber:
        candidates.setdefault(slope, []).append(subset)
    if TAMPER == "census":
        candidates[2] = [fiber[0][0]]
    if TAMPER == "representative":
        candidates[0] = [(1, 2, 3, 4, 5, 6, 7)]
    return candidates, len(fiber)


def remainder_coefficients(subset: tuple[int, ...]) -> list[int]:
    """Low-to-high coefficients of -e3*Y^4+...-e7."""
    e = elementary_symmetric(subset)
    return [(-e[7]) % P, e[6], (-e[5]) % P, e[4], (-e[3]) % P]


def relation_rows(
    slopes: list[int], masks: list[set[int]], kappa: int = 5
) -> tuple[list[list[int]], int]:
    rows: list[list[int]] = []
    predicted = 0
    for x in range(1, P):
        incidence = [i for i, mask in enumerate(masks) if x in mask]
        predicted += max(len(incidence) - 2, 0)
        if len(incidence) < 3:
            continue
        first, second = incidence[0], incidence[1]
        gamma_first = slopes[first]
        gamma_second = slopes[second]
        for third in incidence[2:]:
            gamma_third = slopes[third]
            relation = [0] * len(slopes)
            relation[first] = (gamma_second - gamma_third) % P
            relation[second] = (gamma_third - gamma_first) % P
            relation[third] = (gamma_first - gamma_second) % P
            require(sum(relation) % P == 0, "local relation misses constants")
            require(
                sum(value * slope for value, slope in zip(relation, slopes)) % P
                == 0,
                "local relation misses slopes",
            )
            powers = [pow(x, degree, P) for degree in range(kappa)]
            row: list[int] = []
            for coefficient in relation:
                row.extend((coefficient * power) % P for power in powers)
            rows.append(row)
    require(len(rows) == predicted, "local relation dimension mismatch")
    return rows, predicted


def flatten(polynomials: list[list[int]]) -> list[int]:
    return [entry for polynomial in polynomials for entry in polynomial]


def verify_note() -> tuple[int, str]:
    require(NOTE.is_file(), "companion note missing")
    text = NOTE.read_text(encoding="utf-8")
    markers = [
        "The exact `U_(2,L)` distributed evaluation operator",
        "Conditional affine-pencil theorem",
        "Exact `F_11` seed and central-stress pullback",
        "Residual hereditary `U_2` target",
        "no primitive-rank theorem",
    ]
    if TAMPER == "note_marker":
        markers.append("THIS MARKER MUST NOT EXIST")
    for marker in markers:
        require(marker in text, f"note marker missing: {marker}")
    require(text.count("```") % 2 == 0, "unbalanced note fences")
    require("\t" not in text, "tab in note")
    require(
        all(line == line.rstrip() for line in text.splitlines()),
        "trailing whitespace in note",
    )
    return len(text.splitlines()), hashlib.sha256(text.encode()).hexdigest()


def verify_source_hygiene() -> tuple[int, str]:
    source_path = Path(__file__).resolve()
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert_nodes = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    require(assert_nodes == 0, "assert statement found; optimized mode would skip it")
    note_text = NOTE.read_text(encoding="utf-8") if NOTE.is_file() else ""
    forbidden_terms = [
        "clau" + "de.ai",
        "anth" + "ropic",
        "ses" + "sion",
        "scratch" + "pad",
        "/" + "tmp/clau" + "de",
        "Co-" + "Authored",
        "Generated" + " with",
    ]
    payload = source + note_text
    require(
        all(term not in payload for term in forbidden_terms),
        "forbidden provenance leak",
    )
    require("\t" not in source, "tab in verifier")
    require(
        all(line == line.rstrip() for line in source.splitlines()),
        "trailing whitespace in verifier",
    )
    return len(source.splitlines()), hashlib.sha256(source.encode()).hexdigest()


def verify_seed_all_selectors() -> dict[str, object]:
    candidates, fiber_size = seed_census()
    expected_slopes = {0, 1, 3, 4, 5, 7, 8, 9, 10}
    expected_multiplicities = {
        0: 1,
        1: 2,
        3: 1,
        4: 2,
        5: 1,
        7: 1,
        8: 1,
        9: 1,
        10: 1,
    }
    expected_representatives = {
        0: (2, 3, 4, 5, 7, 8, 10),
        1: (1, 2, 4, 6, 7, 9, 10),
        3: (1, 2, 3, 4, 5, 6, 7),
        4: (1, 3, 4, 5, 7, 9, 10),
        5: (1, 2, 5, 6, 7, 8, 10),
        7: (1, 3, 4, 6, 7, 8, 10),
        8: (1, 2, 3, 6, 8, 9, 10),
        9: (2, 3, 4, 5, 6, 9, 10),
        10: (1, 2, 4, 5, 8, 9, 10),
    }
    require(fiber_size == 11, "e1=6 fiber size is not 11")
    require(set(candidates) == expected_slopes, "wrong e2 image")
    require(
        {slope: len(values) for slope, values in candidates.items()}
        == expected_multiplicities,
        "wrong duplicate-representative profile",
    )
    deterministic = {slope: values[0] for slope, values in candidates.items()}
    require(deterministic == expected_representatives, "representatives changed")

    slopes = sorted(candidates)
    selector_choices = list(
        itertools.product(*(candidates[slope] for slope in slopes))
    )
    require(len(selector_choices) == 4, "selector-choice count is not four")
    direction_roots = {x for x in range(1, P) if (pow(x, 5, P) - 1) % P == 0}
    require(len(direction_roots) == 5, "seed direction distance witness changed")

    operator_ranks: list[int] = []
    row_counts: list[int] = []
    five_augmented_ranks: list[int] = []
    full_augmented_ranks: list[int] = []
    five_count = 0
    expected_core_rank = 6 if TAMPER == "core_rank" else 5

    for selector_index, selected_subsets in enumerate(selector_choices):
        representatives = dict(zip(slopes, selected_subsets))
        polynomials: dict[int, list[int]] = {}
        for slope in slopes:
            subset = representatives[slope]
            e = elementary_symmetric(subset)
            require(e[1] == 6 and e[2] == slope, "prefix mismatch")
            coefficients = remainder_coefficients(subset)
            polynomials[slope] = coefficients
            zero_set = {
                x
                for x in range(1, P)
                if (
                    pow(x, 7, P)
                    - 6 * pow(x, 6, P)
                    + slope * pow(x, 5, P)
                    + poly_eval(coefficients, x)
                )
                % P
                == 0
            }
            require(zero_set == set(subset), "locator zero set mismatch")
            require(P - 1 - len(zero_set) == 3, "seed witness weight is not three")

        full_augmented = [
            [1, slope] + list(reversed(polynomials[slope])) for slope in slopes
        ]
        full_rank = matrix_rank(full_augmented)
        full_augmented_ranks.append(full_rank)
        require(full_rank == 7, "full seed augmented rank is not seven")
        require(full_rank - 2 == expected_core_rank, "core rank mismatch")

        for subset_index, chosen in enumerate(itertools.combinations(slopes, 5)):
            local_slopes = list(chosen)
            masks = [set(representatives[slope]) for slope in local_slopes]
            local_polynomials = [list(polynomials[slope]) for slope in local_slopes]
            first_case = selector_index == 0 and subset_index == 0
            if TAMPER == "kernel" and first_case:
                local_polynomials[0][0] = (local_polynomials[0][0] + 1) % P
            matrix, row_count = relation_rows(local_slopes, masks)
            vector = flatten(local_polynomials)
            if TAMPER == "operator" and first_case:
                require(bool(matrix), "operator tamper found no row")
                position = next(i for i, value in enumerate(vector) if value % P)
                matrix[0][position] = (matrix[0][position] + 1) % P
            require(
                all(dot(row, vector) == 0 for row in matrix),
                "actual tuple not in kernel",
            )
            operator_rank = matrix_rank(matrix)
            require(operator_rank < 15, "five-subfamily has full quotient rank")
            operator_ranks.append(operator_rank)
            row_counts.append(row_count)
            five_count += 1
            augmented = [
                [1, slope] + local_polynomials[index]
                for index, slope in enumerate(local_slopes)
            ]
            augmented_rank = matrix_rank(augmented)
            five_augmented_ranks.append(augmented_rank)
            require(augmented_rank == 5, "five-subfamily does not have s=4,r=3")

    expected_five_count = 503 if TAMPER == "five_count" else 4 * math.comb(9, 5)
    require(five_count == expected_five_count, "wrong five-subfamily count")
    require(set(row_counts) == {15, 16}, "operator row-count census changed")
    require(set(operator_ranks) == {13, 14}, "operator rank census changed")
    require(set(five_augmented_ranks) == {5}, "five-subfamily core rank changed")
    require(set(full_augmented_ranks) == {7}, "full selector core rank changed")
    return {
        "fiber_size": fiber_size,
        "slopes": slopes,
        "selectors": len(selector_choices),
        "five_subfamilies": five_count,
        "operator_rank_range": (min(operator_ranks), max(operator_ranks)),
        "row_count_range": (min(row_counts), max(row_counts)),
        "five_augmented_rank_range": (
            min(five_augmented_ranks),
            max(five_augmented_ranks),
        ),
        "full_augmented_rank_range": (
            min(full_augmented_ranks),
            max(full_augmented_ranks),
        ),
        "core_rank": full_augmented_ranks[0] - 2,
    }


def verify_parameters() -> dict[str, object]:
    orders = [m for m in range(1, 51) if pow(P, m, 500) == 1]
    require(orders == [50], "ord_500(11) is not 50")
    sample_u = [1, 2, 17, 100]
    reliability_bounds: list[Fraction] = []
    for u in sample_u:
        n = 500 * u
        r_distance = 275 * u
        kappa = 225 * u
        d = 250 * u
        t = (149 if TAMPER == "parameters" else 150) * u
        require(n == r_distance + kappa, "N != R+kappa")
        require((n, r_distance, kappa, d, t) == (500*u, 275*u, 225*u, 250*u, 150*u), "stress tuple changed")
        require(n - t == 350 * u, "zero-mask size changed")
        require(5 * (n - t) - 2 * n == 750 * u, "five-mask row lower bound changed")
        require(3 * kappa == 675 * u, "five-mask quotient dimension changed")
        require(5 * (r_distance - t) - 2 * r_distance == 75 * u, "row surplus changed")
        require(5 * (d - t) > d, "affine five-slope contradiction disappeared")
        require(n - 250 * u == d, "degree/root distance identity changed")
        for j in [2, 3, kappa, kappa + 1]:
            kernel_lower = n - kappa + (j - 1)
            singleton_upper = n - (kappa + 1) + j
            require(kernel_lower == r_distance + j - 1, "GHW lower identity changed")
            require(singleton_upper == r_distance + j - 1, "GHW upper identity changed")
        bound = Fraction(5, 2) * Fraction(
            math.comb(r_distance + 5, 5), math.comb(r_distance - t + 5, 5)
        )
        require(bound >= 9, "reliability bound no longer covers seed")
        reliability_bounds.append(bound)

    for u in range(1, 1001):
        same_color = (125 * u + 1) // (20 * u + 1)
        require(same_color == 6, "same-color stress ceiling changed")

    limit = Fraction(5, 2) * Fraction(11**5, 5**5)
    require(abs(float(limit) - 128.8408) < 1e-10, "reliability limit changed")
    return {
        "sample_u": sample_u,
        "reliability_bounds": [float(value) for value in reliability_bounds],
        "reliability_limit": float(limit),
        "same_color_ceiling": 6,
    }


def run_checks() -> dict[str, object]:
    require(TAMPER in VALID_TAMPERS or not TAMPER, "unknown tamper mode")
    note_lines, note_hash = verify_note()
    seed = verify_seed_all_selectors()
    parameters = verify_parameters()
    source_lines, source_hash = verify_source_hygiene()
    return {
        "note_lines": note_lines,
        "note_sha256": note_hash,
        "source_lines": source_lines,
        "source_sha256": source_hash,
        "seed": seed,
        "parameters": parameters,
    }


def run_subprocess(arguments: list[str], tamper: str = "") -> subprocess.CompletedProcess[str]:
    environment = dict(os.environ)
    environment.pop("A6_U2_TAMPER", None)
    if tamper:
        environment["A6_U2_TAMPER"] = tamper
    return subprocess.run(
        arguments,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
        timeout=30,
    )


def run_selftest() -> dict[str, object]:
    script = str(Path(__file__).resolve())
    normal = run_subprocess([sys.executable, script, "--check"])
    require(normal.returncode == 0 and "RESULT: PASS" in normal.stdout, "normal subprocess failed")
    optimized = run_subprocess([sys.executable, "-O", script, "--check"])
    require(
        optimized.returncode == 0 and "RESULT: PASS" in optimized.stdout,
        "optimized subprocess failed",
    )
    tamper_results: dict[str, tuple[int, int]] = {}
    for tamper in sorted(VALID_TAMPERS):
        ordinary = run_subprocess([sys.executable, script, "--check"], tamper=tamper)
        optimized_bad = run_subprocess(
            [sys.executable, "-O", script, "--check"], tamper=tamper
        )
        require(ordinary.returncode != 0, f"tamper survived normal mode: {tamper}")
        require(optimized_bad.returncode != 0, f"tamper survived -O mode: {tamper}")
        tamper_results[tamper] = (ordinary.returncode, optimized_bad.returncode)

    bad_argument = run_subprocess([sys.executable, script, "--not-a-mode"])
    require(bad_argument.returncode == 2, "bad argument did not exit two")
    with tempfile.TemporaryDirectory(prefix="a6_u2_pycompile_") as directory:
        compiled = str(Path(directory) / "verifier.pyc")
        py_compile.compile(script, cfile=compiled, doraise=True)
        require(Path(compiled).is_file(), "py_compile output missing")
    return {
        "normal": normal.returncode,
        "optimized": optimized.returncode,
        "tampers": tamper_results,
        "bad_argument": bad_argument.returncode,
    }


def print_summary(checks: dict[str, object], selftest: dict[str, object] | None) -> None:
    seed = checks["seed"]
    parameters = checks["parameters"]
    require(isinstance(seed, dict), "internal seed summary type")
    require(isinstance(parameters, dict), "internal parameter summary type")
    print(
        "seed:",
        f"fiber={seed['fiber_size']}",
        f"slopes={len(seed['slopes'])}",
        f"selectors={seed['selectors']}",
        f"five_subfamilies={seed['five_subfamilies']}",
        f"operator_ranks={seed['operator_rank_range']}",
        f"rows={seed['row_count_range']}",
        f"core_rank={seed['core_rank']}",
    )
    print(
        "stress:",
        "rows=750u",
        "quotient_columns=675u",
        "surplus=75u",
        f"same_color<={parameters['same_color_ceiling']}",
        f"reliability_limit={parameters['reliability_limit']:.6f}",
    )
    print(
        "artifacts:",
        f"note_lines={checks['note_lines']}",
        f"note_sha256={checks['note_sha256']}",
        f"verifier_lines={checks['source_lines']}",
    )
    if selftest is not None:
        print(
            "selftest:",
            f"normal={selftest['normal']}",
            f"optimized={selftest['optimized']}",
            f"tampers={len(selftest['tampers'])}",
            f"badarg={selftest['bad_argument']}",
        )


def usage() -> None:
    print(f"usage: {Path(sys.argv[0]).name} [--check|--selftest]", file=sys.stderr)


def main() -> int:
    arguments = sys.argv[1:]
    if arguments not in ([], ["--check"], ["--selftest"]):
        usage()
        return 2
    try:
        if arguments == ["--selftest"]:
            selftest = run_selftest()
            print("selftest:", selftest)
            print("RESULT: PASS")
            return 0
        checks = run_checks()
        selftest = None if arguments == ["--check"] else run_selftest()
        print_summary(checks, selftest)
        print("RESULT: PASS")
        return 0
    except (VerificationError, OSError, subprocess.SubprocessError, ValueError) as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
