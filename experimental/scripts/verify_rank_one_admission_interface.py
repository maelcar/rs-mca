#!/usr/bin/env python3
"""Verify the structure-free boundary of omega-capped Walsh accounting."""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Iterable


CERTIFICATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "rank-one-admission-interface"
    / "rank_one_admission_interface.json"
)


class VerificationError(RuntimeError):
    """Raised when a fail-closed audit gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def walsh_sign(point: int, pattern: int) -> int:
    return -1 if (point & pattern).bit_count() % 2 else 1


def require_cube(values: tuple[int, ...]) -> None:
    require(bool(values), "cube must be nonempty")
    require(len(values) & (len(values) - 1) == 0, "cube size is not a power of two")


def walsh_numerators(values: tuple[int, ...]) -> tuple[int, ...]:
    """Return H_D=sum_x h(x) chi_D(x); normalized coefficients are H_D/n."""
    require_cube(values)
    n = len(values)
    return tuple(
        sum(values[point] * walsh_sign(point, pattern) for point in range(n))
        for pattern in range(n)
    )


def fwht(values: tuple[int, ...]) -> tuple[int, ...]:
    """Independent in-place butterfly implementation of the Walsh transform."""
    require_cube(values)
    transformed = list(values)
    width = 1
    while width < len(transformed):
        for start in range(0, len(transformed), 2 * width):
            for offset in range(width):
                left = transformed[start + offset]
                right = transformed[start + width + offset]
                transformed[start + offset] = left + right
                transformed[start + width + offset] = left - right
        width *= 2
    return tuple(transformed)


def greedy_credit(capacities: Iterable[int], cap: int) -> tuple[int, int]:
    """Credit capacities in decreasing order, stopping exactly at cap."""
    require(cap >= 0, "omega cap is negative")
    remaining = cap
    used = 0
    for capacity in sorted(capacities, reverse=True):
        require(capacity >= 0, "negative coefficient capacity")
        if remaining == 0:
            break
        credit = min(capacity, remaining)
        if credit:
            used += 1
            remaining -= credit
    return cap - remaining, used


def analyze(values: tuple[int, ...]) -> dict[str, object]:
    require_cube(values)
    n = len(values)
    numerators = walsh_numerators(values)
    butterfly = fwht(values)
    direct_matches_butterfly = numerators == butterfly
    double_transform = fwht(butterfly)
    involution = double_transform == tuple(n * value for value in values)
    parseval = sum(value * value for value in numerators) == n * sum(
        value * value for value in values
    )
    inversion = all(
        sum(
            numerators[pattern] * walsh_sign(point, pattern)
            for pattern in range(n)
        )
        == n * values[point]
        for point in range(n)
    )
    l1_mass = sum(abs(value) for value in values)
    positive_mass = sum(max(value, 0) for value in values)
    capacities = tuple(abs(value) for value in numerators)
    available = sum(capacities)
    nontrivial_available = sum(capacities[1:])
    credited, patterns_used = greedy_credit(capacities, positive_mass)
    return {
        "dimension": n.bit_length() - 1,
        "values": list(values),
        "walsh_numerators": list(numerators),
        "direct_matches_butterfly": direct_matches_butterfly,
        "involution": involution,
        "parseval": parseval,
        "inversion": inversion,
        "l1_mass": l1_mass,
        "positive_mass": positive_mass,
        "nontrivial_available_capacity": nontrivial_available,
        "available_capacity": available,
        "max_single_capacity": max(capacities),
        "greedy_credit": credited,
        "greedy_patterns_used": patterns_used,
    }


def check_analysis(result: dict[str, object], label: str) -> int:
    require(
        bool(result["direct_matches_butterfly"]), f"{label}: direct/FWHT mismatch"
    )
    require(bool(result["involution"]), f"{label}: Walsh involution failed")
    require(bool(result["inversion"]), f"{label}: Walsh inversion failed")
    require(bool(result["parseval"]), f"{label}: Parseval identity failed")
    require(
        int(result["available_capacity"]) >= int(result["l1_mass"]),
        f"{label}: Walsh triangle inequality failed",
    )
    require(
        int(result["l1_mass"]) >= int(result["positive_mass"]),
        f"{label}: positive mass exceeds l1 mass",
    )
    require(
        int(result["greedy_credit"]) == int(result["positive_mass"]),
        f"{label}: capped greedy did not reach the omega cap",
    )
    return 7


def exhaustive_regression() -> tuple[int, int, dict[str, int]]:
    checks = 0
    functions = 0
    per_dimension: dict[str, int] = {}
    for dimension in (0, 1, 2, 3):
        count = 0
        for values in product((-1, 0, 1), repeat=1 << dimension):
            checks += check_analysis(analyze(tuple(values)), f"m={dimension}:{count}")
            count += 1
        functions += count
        per_dimension[str(dimension)] = count
    require(
        per_dimension == {"0": 3, "1": 9, "2": 81, "3": 6561},
        "unexpected exhaustive function census",
    )
    checks += 1
    require(functions == 6654, "unexpected exhaustive total")
    checks += 1
    return checks, functions, per_dimension


def lcg_fixture(dimension: int) -> tuple[int, ...]:
    """Return a pinned non-hand-chosen integer cube fixture."""
    require(dimension >= 0, "negative LCG fixture dimension")
    state = 20260716 + dimension
    values: list[int] = []
    for _ in range(1 << dimension):
        state = (1664525 * state + 1013904223) % (1 << 32)
        values.append(state % 7 - 3)
    return tuple(values)


def fixture_regression() -> tuple[int, list[dict[str, object]]]:
    fixtures = {
        "point_mass": (7,) + (0,) * 15,
        "parity": tuple(
            1 if point.bit_count() % 2 == 0 else -1 for point in range(16)
        ),
        "single_pattern_failure": (1, 1, 1, -1),
        "positive_constant": (1,) * 8,
        "complement_symmetric": (3, -2, 1, 0, 0, 1, -2, 3),
        "arbitrary_truth_table": (
            3, -2, 5, 0, -7, 4, 1, -1,
            6, -3, 2, -5, 8, 0, -4, 1,
        ),
        "lcg_seed_20260720_m4": lcg_fixture(4),
        "lcg_seed_20260721_m5": lcg_fixture(5),
    }
    checks = 0
    rows: list[dict[str, object]] = []
    for name, values in fixtures.items():
        result = analyze(values)
        checks += check_analysis(result, name)
        result = {"name": name, **result}
        rows.append(result)

    by_name = {str(row["name"]): row for row in rows}
    require(
        int(by_name["single_pattern_failure"]["max_single_capacity"])
        < int(by_name["single_pattern_failure"]["positive_mass"]),
        "false one-pattern strengthening was not refuted",
    )
    checks += 1
    require(
        int(by_name["single_pattern_failure"]["available_capacity"])
        > int(by_name["single_pattern_failure"]["positive_mass"]),
        "uncapped overpayment fixture did not overpay",
    )
    checks += 1

    symmetric = by_name["complement_symmetric"]
    numerators = tuple(int(value) for value in symmetric["walsh_numerators"])
    require(
        all(
            numerator == 0
            for pattern, numerator in enumerate(numerators)
            if pattern.bit_count() % 2
        ),
        "complement symmetry did not kill odd Walsh patterns",
    )
    checks += 1
    require(
        sum(
            1
            for value in by_name["parity"]["walsh_numerators"]
            if int(value) != 0
        )
        == 1,
        "parity fixture is not a one-character function",
    )
    checks += 1
    require(
        len(set(abs(int(value)) for value in by_name["point_mass"]["walsh_numerators"]))
        == 1,
        "point-mass Walsh magnitudes are not flat",
    )
    checks += 1
    require(
        int(by_name["positive_constant"]["nontrivial_available_capacity"]) == 0
        and int(by_name["positive_constant"]["positive_mass"]) == 8,
        "nontrivial-only negative control failed",
    )
    checks += 1
    lcg_expectations = {
        "lcg_seed_20260720_m4": (4, 116, 35, 19, 21),
        "lcg_seed_20260721_m5": (5, 252, 49, 24, 31),
    }
    for name, expected in lcg_expectations.items():
        row = by_name[name]
        observed = (
            int(row["dimension"]),
            int(row["available_capacity"]),
            int(row["l1_mass"]),
            int(row["positive_mass"]),
            int(row["max_single_capacity"]),
        )
        require(
            observed == expected,
            f"{name}: pinned LCG Walsh summary changed",
        )
        checks += 1

    return checks, rows


def build_certificate() -> tuple[dict[str, object], int, int]:
    exhaustive_checks, functions, per_dimension = exhaustive_regression()
    fixture_checks, fixtures = fixture_regression()
    checks = exhaustive_checks + fixture_checks
    certificate: dict[str, object] = {
        "schema_version": 1,
        "status": {
            "universal_capped_walsh_accounting": "PROVED",
            "rank_one_profile_payment": "NOT_CERTIFIED_BY_THIS_IDENTITY",
            "hard_input_2": "OPEN",
        },
        "theorem": {
            "normalized_coefficient": "hat_h(D)=2^-m sum_e h(e) chi_D(e)",
            "available_capacity": "sum_D 2^m |hat_h(D)|",
            "inequality": "available_capacity >= sum_e |h(e)| >= sum_e h(e)_+",
            "scope": "every real cube function; exact verifier uses integer functions",
        },
        "exhaustive": {
            "alphabet": [-1, 0, 1],
            "dimensions": per_dimension,
            "functions": functions,
            "checks": exhaustive_checks,
        },
        "fixtures": fixtures,
        "fixture_generation": {
            "lcg": (
                "state=(1664525*state+1013904223) mod 2^32; "
                "seed=20260716+m; value=state mod 7 - 3"
            )
        },
        "total_checks": checks,
        "interface": {
            "inputs_used": ["cube values"],
            "inputs_not_used": [
                "source chart",
                "first-match owner",
                "profile cell",
                "slope projection",
                "MI or MA certificate",
                "Sidon moment payment",
                "ray compiler",
                "same-owner first-match profile cell",
                "A4 analytic/Sidon payment",
                "A6/RC distinct-slope bound",
                "uniform subexponential aggregate census",
            ],
        },
    }
    return certificate, checks, functions + len(fixtures)


def run_tamper_selftest() -> int:
    result = analyze((1, 1, 1, -1))
    constant = analyze((1,) * 8)
    rejected = 0
    false_claims = (
        (
            int(result["max_single_capacity"])
            >= int(result["positive_mass"]),
            "single Walsh pattern always reaches the omega cap",
        ),
        (
            int(result["available_capacity"])
            <= int(result["positive_mass"]),
            "uncapped coefficient sum is omega-sound",
        ),
        (
            int(constant["nontrivial_available_capacity"])
            >= int(constant["positive_mass"]),
            "nontrivial Walsh patterns are universally adequate",
        ),
    )
    for condition, message in false_claims:
        try:
            require(condition, message)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {message}")
    require(rejected == len(false_claims), "not every tamper was rejected")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--emit-certificate",
        type=Path,
        metavar="PATH",
        help="write the exact JSON certificate to PATH",
    )
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="reject one-pattern, uncapped, and nontrivial-only strengthenings",
    )
    args = parser.parse_args()

    if args.tamper_selftest:
        rejected = run_tamper_selftest()
        print(f"PASS: rank-one admission tamper self-test rejected {rejected}/{rejected}")
        return

    certificate, checks, functions = build_certificate()
    if args.emit_certificate:
        args.emit_certificate.parent.mkdir(parents=True, exist_ok=True)
        args.emit_certificate.write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE: {args.emit_certificate}")
    else:
        require(CERTIFICATE_PATH.is_file(), f"missing certificate: {CERTIFICATE_PATH}")
        recorded = json.loads(CERTIFICATE_PATH.read_text(encoding="utf-8"))
        require(recorded == certificate, "checked-in certificate is stale")

    print(f"PASS: {checks:,} universal Walsh checks over {functions:,} exact cube functions")
    print("PASS: omega-capped adequacy is structure-free; profile payment not certified")


if __name__ == "__main__":
    main()
