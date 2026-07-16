#!/usr/bin/env python3
"""Verify the triple-negative first-match denominator reduction."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


SCHEMA = "rs-mca-triple-negative-first-match-reduction-v1"
THEOREM_ID = "triple-negative-first-match-reduction"
STATUS = "PROVED ARITHMETIC REDUCTION / AUDITED COUNTING SYNTHESIS"
REPO = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    REPO
    / "experimental/data/certificates/triple-negative-first-match-reduction"
    / "triple_negative_first_match_reduction.json"
)
SOURCE_MARKERS = {
    "experimental/notes/thresholds/selector_free_direction_distance_all_pair.md": (
        "D_H=(N-t)^2-N(N-d).                                       (5)",
        "D_J=Delta M-2rho M+rho^2=(M-rho)^2-M(kappa-1).             (16)",
    ),
    "experimental/notes/thresholds/fixed_deficiency_complete_absorption.md": (
        "|P|<=binom(N,d+1).                                       (4)",
        "It also survives arbitrary first-match",
    ),
    "experimental/notes/thresholds/all_pair_paving_basis_multiplicity_compiler.md": (
        "|P| <= floor(beta_(kappa+1)(A)/Lambda_(d,t))",
        "The exact remaining wall is the **basis-heavy deep-hole owner dichotomy**",
    ),
    "experimental/notes/thresholds/depth_zero_identity_lineray_owner.md": (
        "|P| <= binom(N,a).                                      (1)",
        "This serves hard input 3, the residual ray compiler, only at the depth-zero",
    ),
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding() -> list[dict[str, Any]]:
    rows = []
    for relative, markers in SOURCE_MARKERS.items():
        path = REPO / relative
        lines = path.read_text().splitlines()
        pins = []
        for marker in markers:
            matches = [(i, line) for i, line in enumerate(lines, 1) if marker in line]
            require(len(matches) == 1, f"source marker is not unique: {marker}")
            line_no, line = matches[0]
            pins.append(
                {
                    "line": line_no,
                    "marker": marker,
                    "line_sha256": hashlib.sha256(line.encode()).hexdigest(),
                }
            )
        rows.append(
            {
                "path": relative,
                "sha256": file_sha256(path),
                "pins": pins,
            }
        )
    return rows


def parameter_row(N: int, R: int, t: int, direction_d: int) -> dict[str, int | str]:
    require(N >= 2, "N<2")
    require(1 <= R < N, "R outside [1,N)")
    kappa = N - R
    require(0 <= t < R, "t outside [0,R)")
    require(1 <= direction_d <= R, "direction distance outside [1,R]")

    a = N - t
    M = N - direction_d
    rho = min(t, M)
    Delta = R - direction_d + 1
    deficiency = 2 * t - R
    gap = R - t
    identity_depth = gap - 1

    D_H = a * a - N * M
    D_J = (M - rho) ** 2 - M * (kappa - 1)
    J_K = a * a - N * (kappa - 1)

    require(D_H == J_K - N * Delta, "D_H nesting identity")
    require(J_K == t * t - N * (deficiency - 1), "t/deficiency identity")
    require(
        J_K == (gap + 1) ** 2 - (kappa - 1) * (deficiency - 1),
        "gap/deficiency factorization",
    )

    if M >= t:
        branch = "rho=t"
        require(rho == t, "rho=t branch")
        require(
            D_J == J_K - direction_d * (M - deficiency + 1),
            "D_J rho=t identity",
        )
        require(M - deficiency + 1 >= gap + 1, "rho=t strict gap")
    else:
        branch = "rho=M"
        require(rho == M, "rho=M branch")
        require(D_J == -M * (kappa - 1), "D_J rho=M identity")
        require(M >= kappa, "punctured length below kappa")

    if J_K <= 0:
        require(kappa >= 2, "J_K<=0 did not force kappa>=2")
        require(deficiency >= 2, "J_K<=0 did not force deficiency>=2")
        require(deficiency < t, "deficiency<t failed")
        require(D_H <= -N < 0, "D_H not strictly negative")
        if M >= t:
            require(
                D_J <= -direction_d * (gap + 1) < 0,
                "D_J rho=t not strictly negative",
            )
        else:
            require(
                D_J <= -kappa * (kappa - 1) < 0,
                "D_J rho=M not strictly negative",
            )

    return {
        "N": N,
        "R": R,
        "kappa": kappa,
        "t": t,
        "direction_d": direction_d,
        "a": a,
        "M": M,
        "rho": rho,
        "Delta": Delta,
        "deficiency_delta": deficiency,
        "gap_g": gap,
        "identity_depth_h": identity_depth,
        "D_H": D_H,
        "D_J": D_J,
        "J_K": J_K,
        "rho_branch": branch,
    }


def exhaustive_scan(limit: int = 80) -> dict[str, Any]:
    total = 0
    nonpositive = 0
    boundary = 0
    branch_counts = {"rho=t": 0, "rho=M": 0}
    nonpositive_branches = {"rho=t": 0, "rho=M": 0}
    positive_depth_nonpositive = 0

    for N in range(2, limit + 1):
        for R in range(1, N):
            for t in range(R):
                for direction_d in range(1, R + 1):
                    row = parameter_row(N, R, t, direction_d)
                    total += 1
                    branch = str(row["rho_branch"])
                    branch_counts[branch] += 1
                    if int(row["J_K"]) <= 0:
                        nonpositive += 1
                        nonpositive_branches[branch] += 1
                        require(int(row["D_H"]) < 0, "scan D_H sign")
                        require(int(row["D_J"]) < 0, "scan D_J sign")
                        if int(row["J_K"]) == 0:
                            boundary += 1
                        if int(row["identity_depth_h"]) >= 1:
                            positive_depth_nonpositive += 1

    require(nonpositive == 892_834, "unexpected J_K<=0 scan count")
    require(sum(branch_counts.values()) == total, "branch total")
    require(sum(nonpositive_branches.values()) == nonpositive, "negative branch total")
    require(boundary > 0 and positive_depth_nonpositive > 0, "missing scan strata")
    return {
        "limit_N": limit,
        "eligible_parameter_rows": total,
        "J_K_nonpositive_rows": nonpositive,
        "J_K_zero_rows": boundary,
        "positive_depth_J_K_nonpositive_rows": positive_depth_nonpositive,
        "all_J_K_nonpositive_rows_have_D_H_and_D_J_strictly_negative": True,
        "rho_branch_counts": branch_counts,
        "J_K_nonpositive_rho_branch_counts": nonpositive_branches,
    }


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "ceil_div domain")
    return (numerator + denominator - 1) // denominator


def owner_caps(N: int, R: int, t: int, direction_d: int) -> dict[str, Any]:
    row = parameter_row(N, R, t, direction_d)
    require(int(row["J_K"]) <= 0, "owner comparison outside J_K<=0")
    kappa = int(row["kappa"])
    deficiency = int(row["deficiency_delta"])
    fixed_deficiency = math.comb(N, deficiency + 1)
    paving_first = math.comb(N - t - 1, kappa)
    paving_direction = ceil_div(
        max(direction_d - t, 0) * math.comb(N - t, kappa), kappa + 1
    )
    Lambda = max(paving_first, paving_direction)
    paving = math.comb(N, kappa + 1) // Lambda
    deep_hole = None
    if direction_d == R:
        deep_hole = math.comb(N, kappa + 1) // math.comb(N - t, kappa + 1)
        require(deep_hole <= paving, "deep-hole strengthening went upward")
    return {
        "parameters": row,
        "fixed_deficiency_cap": fixed_deficiency,
        "paving_Lambda": Lambda,
        "paving_first_term": paving_first,
        "paving_direction_term": paving_direction,
        "paving_cap": paving,
        "deep_hole_cap": deep_hole,
        "combined_cap": min(
            fixed_deficiency,
            deep_hole if deep_hole is not None else paving,
        ),
    }


def noncomparability() -> list[dict[str, Any]]:
    first = owner_caps(17, 6, 4, 1)
    second = owner_caps(22, 6, 4, 1)
    require(first["fixed_deficiency_cap"] == 680, "first deficiency cap")
    require(first["paving_cap"] == 515, "first paving cap")
    require(second["fixed_deficiency_cap"] == 1540, "second deficiency cap")
    require(second["paving_cap"] == 1549, "second paving cap")
    require(first["paving_cap"] < first["fixed_deficiency_cap"], "first ordering")
    require(second["fixed_deficiency_cap"] < second["paving_cap"], "second ordering")
    return [first, second]


def boundary_fixtures() -> list[dict[str, Any]]:
    fixtures = [
        parameter_row(12, 8, 6, 1),
        parameter_row(12, 8, 6, 8),
    ]
    require(all(int(row["J_K"]) == 0 for row in fixtures), "boundary J_K")
    require(fixtures[0]["rho_branch"] == "rho=t", "boundary rho=t")
    require(fixtures[1]["rho_branch"] == "rho=M", "boundary rho=M")
    require(all(int(row["identity_depth_h"]) == 1 for row in fixtures), "positive depth")
    return fixtures


def route_cut_fixtures() -> list[dict[str, Any]]:
    rows = []
    for m in range(4, 13):
        cap = owner_caps(2 * m + 1, m + 1, m, m + 1)
        row = cap["parameters"]
        require(int(row["identity_depth_h"]) == 0, "route cut depth")
        require(int(row["D_H"]) == -m * m + m + 1, "route cut D_H")
        require(int(row["D_J"]) == -m * (m - 1), "route cut D_J")
        require(int(row["J_K"]) == -m * m + 3 * m + 2, "route cut J_K")
        sharp_pairs = math.comb(2 * m + 1, m)
        require(cap["fixed_deficiency_cap"] == sharp_pairs, "route cut sharp cap")
        require(cap["deep_hole_cap"] == sharp_pairs, "route cut deep-hole cap")
        rows.append(
            {
                "m": m,
                "parameters": row,
                "canonical_pair_count": sharp_pairs,
                "fixed_deficiency_cap": cap["fixed_deficiency_cap"],
                "deep_hole_cap": cap["deep_hole_cap"],
                "depth_zero_profile_owner_scale": sharp_pairs,
            }
        )
    return rows


def positive_depth_sign_stress() -> list[dict[str, Any]]:
    rows = []
    for B in range(8, 42, 2):
        row = parameter_row(2 * B, B + 2, B, B + 2)
        require(int(row["gap_g"]) == 2, "stress gap")
        require(int(row["identity_depth_h"]) == 1, "stress depth")
        require(int(row["D_H"]) == B * (4 - B), "stress D_H")
        require(int(row["D_J"]) == -(B - 2) * (B - 3), "stress D_J")
        require(int(row["J_K"]) == B * (6 - B), "stress J_K")
        rows.append({"B": B, **row})
    return rows


def build() -> dict[str, Any]:
    out: dict[str, Any] = {
        "schema": SCHEMA,
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "scope": {
            "parameters": [
                "N=R+kappa",
                "0<=t<R",
                "1<=direction_d<=R",
                "M=N-direction_d",
                "rho=min(t,M)",
                "deficiency_delta=2t-R",
                "gap_g=R-t",
                "identity_depth_h=g-1",
            ],
            "denominators": {
                "D_H": "(N-t)^2-N(N-direction_d)",
                "D_J": "(M-rho)^2-M(kappa-1)",
                "J_K": "(N-t)^2-N(kappa-1)",
            },
            "counted_object": "complete distinct retained transverse (slope,error) pairs after any earlier first-match deletion",
        },
        "proved_arithmetic": {
            "nesting": [
                "D_H=J_K-N(R-direction_d+1)",
                "rho=t => D_J=J_K-direction_d(M-deficiency_delta+1)",
                "rho=M => D_J=-M(kappa-1)",
            ],
            "normal_forms": [
                "J_K=t^2-N(deficiency_delta-1)",
                "J_K=(gap_g+1)^2-(kappa-1)(deficiency_delta-1)",
            ],
            "sign_collapse": "D_H<=0 and D_J<=0 and J_K<=0 iff J_K<=0; on J_K<=0 the older two signs are strict",
            "forced_region": "J_K<=0 implies kappa>=2 and 2<=deficiency_delta<t",
        },
        "complete_pair_synthesis": {
            "fixed_deficiency": "|P|<=binom(N,deficiency_delta+1)",
            "paving": "|P|<=floor(beta_(kappa+1)(A)/Lambda_direction_d(t))<=floor(binomial(N,kappa+1)/Lambda_direction_d(t))",
            "composition_rule": "take the minimum of valid complete-pair caps; never multiply independent owner denominators",
            "first_match_safety": "both complete-pair caps are monotone under deletion",
            "subexponential_routes": [
                "deficiency_delta=o(N)",
                "R=o(N), because 0<deficiency_delta<t<R",
                "kappa=o(N), because J_K<=0 forces gap_g=o(N) and the complementary binomial index kappa+2gap_g-1=o(N)",
                "identity_depth_h=0 is paid exactly at the depth-zero identity profile scale",
            ],
            "remaining_wall": "positive-depth first-match profiles with positive-linear kappa and deficiency, after exact-weight, curve/pencil, low-rank affine-core, and earlier semantic owners are removed; compare owned augmented-basis mass to the realized profile scale or route the whole fiber",
        },
        "exhaustive_parameter_scan": exhaustive_scan(),
        "positive_depth_boundary_fixtures": boundary_fixtures(),
        "owner_cap_noncomparability": noncomparability(),
        "depth_zero_sharp_route_cut": route_cut_fixtures(),
        "positive_depth_sign_stress": positive_depth_sign_stress(),
        "source_binding": source_binding(),
        "nonclaims": [
            "The sign chamber is not itself a semantic first-match cell.",
            "No owner-free subexponential bound is claimed on all of J_K<=0.",
            "No theorem says a triple-negative witness survives earlier quotient, planted, curve, common-support, or other owners.",
            "No witness-exhaustive atlas, profile add-back, uniform received-line theorem, deployed-row movement, Grand MCA, or Grand List result is claimed.",
            "The pending fixed-slope J_K source packet is not vendored or treated as integrated by this standalone arithmetic reduction.",
        ],
    }
    out["payload_sha256"] = payload_sha256(out)
    return out


def validate_semantics(value: dict[str, Any]) -> None:
    require(value.get("schema") == SCHEMA, "schema")
    require(value.get("theorem_id") == THEOREM_ID, "theorem id")
    require(value.get("status") == STATUS, "status")
    require(value.get("payload_sha256") == payload_sha256(value), "payload hash")
    proved = value.get("proved_arithmetic", {})
    require("iff J_K<=0" in proved.get("sign_collapse", ""), "sign collapse")
    scan = value.get("exhaustive_parameter_scan", {})
    require(scan.get("limit_N") == 80, "scan limit")
    require(scan.get("J_K_nonpositive_rows") == 892_834, "scan count")
    require(
        scan.get("all_J_K_nonpositive_rows_have_D_H_and_D_J_strictly_negative")
        is True,
        "scan conclusion",
    )
    comparisons = value.get("owner_cap_noncomparability", [])
    require(len(comparisons) == 2, "noncomparability rows")
    require(comparisons[0].get("paving_cap") == 515, "first paving cap")
    require(comparisons[1].get("fixed_deficiency_cap") == 1540, "second fixed cap")
    boundary = value.get("positive_depth_boundary_fixtures", [])
    require(len(boundary) == 2, "boundary fixtures")
    require({row.get("rho_branch") for row in boundary} == {"rho=t", "rho=M"}, "branches")
    require(len(value.get("depth_zero_sharp_route_cut", [])) == 9, "route cut rows")
    require(len(value.get("positive_depth_sign_stress", [])) == 17, "stress rows")
    bindings = value.get("source_binding", [])
    require(len(bindings) == len(SOURCE_MARKERS), "source binding count")
    for binding in bindings:
        path = REPO / binding.get("path", "")
        require(binding.get("sha256") == file_sha256(path), "source digest")
    require(len(value.get("nonclaims", [])) >= 5, "nonclaims")


def validate(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    validate_semantics(actual)
    require(actual == expected, "deterministic recomputation mismatch")


def rehash(value: dict[str, Any]) -> None:
    value["payload_sha256"] = payload_sha256(value)


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = []

    value = copy.deepcopy(expected)
    value["proved_arithmetic"]["sign_collapse"] = "three unrelated signs"
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["exhaustive_parameter_scan"]["J_K_nonpositive_rows"] -= 1
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["exhaustive_parameter_scan"][
        "all_J_K_nonpositive_rows_have_D_H_and_D_J_strictly_negative"
    ] = False
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["owner_cap_noncomparability"][0]["paving_cap"] += 1
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["positive_depth_boundary_fixtures"][1]["rho_branch"] = "rho=t"
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["depth_zero_sharp_route_cut"].pop()
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["positive_depth_sign_stress"].pop()
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["source_binding"][0]["sha256"] = "0" * 64
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["nonclaims"] = []
    rehash(value)
    mutations.append(value)

    value = copy.deepcopy(expected)
    value["payload_sha256"] = "f" * 64
    mutations.append(value)

    rejected = 0
    for mutation in mutations:
        try:
            validate(mutation, expected)
        except (OSError, VerificationError, ValueError):
            rejected += 1
    require(rejected == len(mutations), "tamper mutation accepted")
    return rejected


def check(expected: dict[str, Any]) -> None:
    require(CERTIFICATE.is_file(), f"missing {CERTIFICATE.relative_to(REPO)}")
    try:
        actual = json.loads(CERTIFICATE.read_text())
    except json.JSONDecodeError as error:
        raise VerificationError(f"certificate JSON: {error}") from error
    require(isinstance(actual, dict), "certificate root is not an object")
    validate(actual, expected)


def summary(value: dict[str, Any], tamper: int | None = None) -> None:
    scan = value["exhaustive_parameter_scan"]
    print(f"{THEOREM_ID}: PASS")
    print(
        "scan="
        f"{scan['J_K_nonpositive_rows']}/{scan['eligible_parameter_rows']} "
        "J_K<=0 rows; D_H,D_J strict on all"
    )
    print("boundary=positive-depth rho=t and rho=M branches checked")
    print("caps=first 515<680; second 1540<1549")
    print(f"payload_sha256={value['payload_sha256']}")
    if tamper is not None:
        print(f"tamper_mutations_rejected={tamper}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--emit", action="store_true", help="emit deterministic JSON")
    group.add_argument("--check", action="store_true", help="check pinned certificate")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build()
    if args.emit:
        print(json.dumps(expected, indent=2, sort_keys=True, ensure_ascii=True))
        return 0
    if args.tamper_selftest:
        summary(expected, tamper_selftest(expected))
        return 0
    check(expected)
    summary(expected)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, VerificationError, ValueError) as error:
        print(f"{THEOREM_ID}: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
