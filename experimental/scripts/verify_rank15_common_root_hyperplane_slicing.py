#!/usr/bin/env python3
"""Replay the narrow rank-15 common-root hyperplane-slicing certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
import sys
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/rank15-common-root-hyperplane-slicing"
    / "rank15_common_root_hyperplane_slicing.json"
)
EXPECTED_BASE = "9262f63cf093a7510a2df435f220390f59e2bcd5"


class VerificationError(RuntimeError):
    """Raised when an always-active certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime_by_trial_division(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def gaussian_binomial(n: int, k: int, q: int) -> int:
    require(0 <= k <= n, "Gaussian-binomial index out of range")
    require(q >= 2, "Gaussian-binomial field size must be at least two")
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for index in range(k):
        numerator *= q ** (n - index) - 1
        denominator *= q ** (k - index) - 1
    require(numerator % denominator == 0, "Gaussian-binomial division is not exact")
    return numerator // denominator


def recurrence_value(n: int, k: int, s: int, dimension: int = 14) -> int:
    """Evaluate the integrated stateful affine-section recurrence at z=0."""
    require(0 < dimension <= k <= s <= n, "invalid affine-section row")
    previous = [1] * (k + 2)
    for current_dimension in range(1, dimension + 1):
        current = [0] * (k + 2)
        suffix_maximum = 0
        for u in range(k - current_dimension, -1, -1):
            incidence = (n - u) * previous[u + 1] // (s - u)
            determinant = (s - u) ** 2 - (n - u) * (k - 1 - u)
            candidate = incidence
            if determinant > 0:
                johnson = (n - u) * (s - k + 1) // determinant
                candidate = min(candidate, johnson)
            suffix_maximum = max(suffix_maximum, candidate)
            current[u] = suffix_maximum
        previous = current
    return previous[0]


def boundary_scan(
    n: int,
    k: int,
    s: int,
    ceiling: int,
    c_max: int,
) -> dict[str, int]:
    best_value = -1
    best_c = -1
    best_shift = -1
    for c in range(c_max + 1):
        shifted_state = k - c - ceiling
        require(shifted_state >= 0, "negative boundary shifted state")
        value = recurrence_value(
            n - shifted_state,
            ceiling,
            s - shifted_state,
        )
        if value > best_value:
            best_value = value
            best_c = c
            best_shift = shifted_state
    return {"value": best_value, "c": best_c, "shifted_state": best_shift}


def scalar_minimum_table(
    n: int,
    s: int,
    list_size: int,
    states: range | tuple[int, ...],
    degree_floor: int,
) -> list[dict[str, int]]:
    table: list[dict[str, int]] = []
    pair_count = comb(list_size, 2)
    for t in range(1, 16):
        best: tuple[int, int] | None = None
        pair_capacity = pair_count * comb(degree_floor, t)
        for u in states:
            residual_n = n - u
            residual_a = s - u
            slack = (
                comb(residual_n, t)
                + pair_capacity
                - list_size * comb(residual_a, t)
            )
            candidate = (slack, u)
            if best is None or candidate < best:
                best = candidate
        require(best is not None, "empty scalar state set")
        table.append({"t": t, "slack": best[0], "u": best[1]})
    return table


def minimum_baseline_t16(
    n: int,
    s: int,
    list_size: int,
    states: range | tuple[int, ...],
) -> tuple[int, int]:
    best: tuple[int, int] | None = None
    for u in states:
        residual_n = n - u
        residual_a = s - u
        require(residual_n > residual_a >= 16, "invalid t=16 baseline row")
        slack = comb(residual_n, 16) - list_size * comb(residual_a, 16)
        candidate = (slack, u)
        if best is None or candidate < best:
            best = candidate
    require(best is not None, "empty t=16 state set")
    return best


def check_static_provenance(data: dict[str, Any]) -> None:
    require(data["schema"] == "rank15-common-root-hyperplane-slicing-v1", "schema")
    require(
        data["status"] == "PROVED_NARROW_THEOREM_CONDITIONAL_RESIDUAL_CONSUMER",
        "certificate status",
    )
    provenance = data["provenance"]
    require(provenance["base_commit"] == EXPECTED_BASE, "base commit")
    require(
        provenance["worker_model"]
        == "native gpt-5.6-sol ultra hostile integration worker",
        "worker model provenance",
    )
    require(
        provenance["worker_return_sha256"]
        == "d9f28077534f9d9aab30f9a7b69b9df57c40cbf3bb45843b72a10e97b2c213a7",
        "worker return hash",
    )
    require(
        provenance["conditional_r13_status"] == "NOT_UPSTREAM_CONSUMER_ONLY",
        "R13 consumer status",
    )
    require(
        provenance["conditional_r13_commit"]
        == "0e776db208da795930d343dca4343f815f258c28",
        "R13 conditional commit",
    )
    expected_paths = {
        "experimental/notes/l2/affine_section_one_row_rank_reduction.md",
        "experimental/scripts/verify_affine_section_one_row_rank.py",
        "experimental/notes/l2/affine_interleaved_shell_compression.md",
    }
    require(
        {source["path"] for source in data["source_imports"]} == expected_paths,
        "source import set",
    )
    for source in data["source_imports"]:
        path = ROOT / source["path"]
        require(path.is_file(), f"missing source import: {source['path']}")
        require(file_sha256(path) == source["sha256"], f"source hash: {source['path']}")


def check_field_ledger(data: dict[str, Any]) -> dict[str, int]:
    field = data["field_ledger"]
    p = field["base_field_prime"]
    n = field["evaluation_domain_size"]
    k = field["code_dimension"]
    s = field["agreement_threshold"]
    require(p == 2**31 - 2**24 + 1, "base-field formula")
    require(is_prime_by_trial_division(p), "base field is not prime")
    require((p - 1) % n == 0, "evaluation-domain order does not divide p-1")
    require((p - 1) // n == field["subgroup_index"] == 1016, "subgroup index")
    omega = pow(3, field["subgroup_index"], p)
    require(omega == field["subgroup_generator"], "subgroup generator")
    require(pow(omega, n, p) == 1, "subgroup generator n-th power")
    require(pow(omega, n // 2, p) == p - 1, "subgroup generator exact order")

    q_list = p ** field["extension_degree"]
    require(q_list == field["list_denominator"], "sextic list denominator")
    require(field["budget_denominator"] == 2**128, "budget denominator")
    budget = q_list // field["budget_denominator"]
    require(budget == field["budget"], "budget")
    shell_denominator = p - n + s
    require(shell_denominator == field["shell_denominator"], "shell denominator")
    target = ((budget + 1) * shell_denominator - 1) // p
    require(target == field["one_row_target"], "one-row target")
    require(k == 2**20 and n == 2**21, "deployed n/K ledger")
    return {"p": p, "n": n, "k": k, "s": s, "target": target, "q_list": q_list}


def check_theorem_static(data: dict[str, Any], field: dict[str, int]) -> None:
    theorem = data["theorem"]
    p = field["p"]
    target = field["target"]
    require(theorem["name"] == "R15-HYP14-ROOT-SLICE", "theorem name")
    require(theorem["c_min"] == 0 and theorem["c_max"] == 152, "c range")
    require(theorem["affine_rank"] == 15, "affine rank")
    require(theorem["hyperplane_dimension"] == 14, "hyperplane dimension")
    require(theorem["fiber_count"] == p, "base-field fiber count")
    require(theorem["paid_quotient_ceiling"] == 4985, "paid ceiling")
    require(theorem["rank14_fiber_bound"] == 20008483, "rank-14 fiber bound")
    require(
        theorem["list_bound"] == p * theorem["rank14_fiber_bound"],
        "p-fiber list bound",
    )
    require(theorem["list_bound"] == 42632203442671139, "list-bound integer")
    require(theorem["target_slack"] == target - theorem["list_bound"], "target slack")
    require(theorem["target_slack"] > 0, "theorem does not clear target")
    require(theorem["violator_root_cap_constant"] == 1043590, "root-cap constant")
    boundary = theorem["boundary_scan"]
    require(boundary["paid_ceiling"] == 4985, "boundary paid ceiling")
    require(boundary["tamper_ceiling"] == 4986, "boundary tamper ceiling")
    require(
        boundary["tamper_product"] == p * boundary["tamper_max"],
        "tamper p-product",
    )
    require(
        boundary["tamper_excess_over_target"] == boundary["tamper_product"] - target,
        "tamper target excess",
    )
    require(boundary["tamper_excess_over_target"] > 0, "tamper unexpectedly pays")


def check_ownership(data: dict[str, Any], p: int) -> dict[str, int]:
    ownership = data["ownership_ledger"]
    require(ownership["nullity_min"] == 1, "ownership minimum nullity")
    require(ownership["nullity_max"] == 14, "ownership maximum nullity")
    require(
        ownership["integral_owner_status"] == "REQUIRES_AN_ARBITRARY_TOTAL_ORDER",
        "integral owner status",
    )
    identity_checks = 0
    for nullity in range(1, 15):
        total = 0
        for dimension in range(nullity + 1):
            coefficient = (-1) ** dimension * p ** (dimension * (dimension - 1) // 2)
            total += coefficient * gaussian_binomial(nullity, dimension, p)
        require(total == 0, f"Gaussian-binomial Mobius identity s={nullity}")
        identity_checks += 1
    line_count = (p**14 - 1) // (p - 1)
    require(
        line_count == ownership["projective_lines_nullity_14"],
        "nullity-14 projective-line count",
    )
    return {"identity_checks": identity_checks, "a14": line_count}


def check_residual_consumer(
    data: dict[str, Any], field: dict[str, int]
) -> dict[str, Any]:
    residual = data["conditional_residual_consumer"]
    require(
        residual["status"] == "CONDITIONAL_ON_UNPUBLISHED_R13_RECURRENCE",
        "residual consumer status",
    )
    row = residual["c_le_151"]
    require(row["u_min"] == 1042375 and row["u_max"] == 1043582, "u range")
    require(row["c_min"] == 0 and row["c_max"] == 151, "c<=151 range")
    require(row["u_plus_c_max"] == 1043588, "u+c restriction")
    require(row["e14_floor"] == 4986 and row["e15_floor"] == 4987, "pivot floors")
    defect = sum(range(13)) + row["e14_floor"] + row["e15_floor"] - comb(15, 2)
    require(defect == row["alternant_defect_floor"] == 9946, "defect floor")

    k = field["k"]
    state_count = 0
    for u in range(row["u_min"], row["u_max"] + 1):
        c_max = min(row["c_max"], row["u_plus_c_max"] - u)
        require(c_max >= 0, f"empty residual c range at u={u}")
        for c in range(row["c_min"], c_max + 1):
            k_a = k - u - c
            require(k_a - 1 >= row["e15_floor"], "state violates e15 feasibility")
            require(k_a - 4986 == 1043590 - u - c, "common-root cap formula")
            state_count += 1
    require(state_count == row["state_count"] == 173031, "residual state count")
    require(
        1043590 - row["nullity_14_empty_u_plus_c_min"] == 14,
        "nullity-14 diagonal threshold",
    )
    require(1043590 - (row["nullity_14_empty_u_plus_c_min"] - 1) == 15, "diagonal sharpness")

    c152 = residual["c_152"]
    require(c152["states"] == [1043403, 1043404, 1043405, 1043406], "c=152 states")
    require(c152["e14_floor"] == 5010 and c152["e15_floor"] == 5017, "c=152 pivots")
    c152_defect = sum(range(13)) + c152["e14_floor"] + c152["e15_floor"] - comb(15, 2)
    require(c152_defect == c152["alternant_defect_floor"] == 10000, "c=152 defect")
    caps = [k - u - 152 - 4986 for u in c152["states"]]
    require(caps == c152["common_root_caps"] == [35, 34, 33, 32], "c=152 caps")
    require(residual["unpaid_nullities"] == list(range(1, 14)), "unpaid nullities")
    return {"state_count": state_count, "c152_caps": caps, "row": row, "c152": c152}


def check_scalar_route(
    data: dict[str, Any], field: dict[str, int], residual: dict[str, Any]
) -> dict[str, Any]:
    scalar = data["scalar_route_cut"]
    list_size = field["target"] + 1
    require(scalar["test_list_size"] == list_size, "scalar test list size")
    row = residual["row"]
    states = range(row["u_min"], row["u_max"] + 1)
    degree_floor = scalar["c_le_151_degree_floor_envelope"]
    require(degree_floor == row["e15_floor"] == 4987, "c<=151 scalar envelope")
    table = scalar_minimum_table(field["n"], field["s"], list_size, states, degree_floor)
    require(all(entry["slack"] > 0 for entry in table), "scalar route closes at t<=15")
    require(table[0]["slack"] == scalar["c_le_151_minimum_t1_slack"], "scalar t=1 anchor")
    require(table[14]["slack"] == scalar["c_le_151_minimum_t15_slack"], "scalar t=15 anchor")
    table_digest = canonical_sha256(table)
    require(table_digest == scalar["c_le_151_minimum_table_sha256"], "scalar table digest")
    baseline = minimum_baseline_t16(field["n"], field["s"], list_size, states)
    require(baseline[0] > 0, "t=16 baseline closes")
    require(
        baseline[0] == scalar["c_le_151_minimum_baseline_t16_slack"],
        "t=16 baseline anchor",
    )

    c152_states = tuple(residual["c152"]["states"])
    c152_floor = scalar["c_152_degree_floor_envelope"]
    require(c152_floor == residual["c152"]["e15_floor"] == 5017, "c=152 scalar envelope")
    c152_table = scalar_minimum_table(
        field["n"], field["s"], list_size, c152_states, c152_floor
    )
    require(all(entry["slack"] > 0 for entry in c152_table), "c=152 scalar route closes")
    require(c152_table[0]["slack"] == scalar["c_152_minimum_t1_slack"], "c=152 t=1 anchor")
    require(c152_table[14]["slack"] == scalar["c_152_minimum_t15_slack"], "c=152 t=15 anchor")
    c152_digest = canonical_sha256(c152_table)
    require(c152_digest == scalar["c_152_minimum_table_sha256"], "c=152 table digest")
    c152_baseline = minimum_baseline_t16(
        field["n"], field["s"], list_size, c152_states
    )
    require(c152_baseline[0] > 0, "c=152 t=16 baseline closes")
    require(
        c152_baseline[0] == scalar["c_152_minimum_baseline_t16_slack"],
        "c=152 t=16 anchor",
    )
    return {
        "table": table,
        "table_digest": table_digest,
        "baseline": baseline,
        "c152_table": c152_table,
        "c152_digest": c152_digest,
        "c152_baseline": c152_baseline,
    }


def check_construction(
    data: dict[str, Any], field: dict[str, int], a14: int
) -> dict[str, int]:
    construction = data["construction"]
    state = construction["state"]
    n = field["n"]
    k = field["k"]
    s = field["s"]
    require(state == {"u": 1043576, "c": 0, "N": 1053576, "a": 72471, "k_A": 5000}, "construction state")
    require(state["N"] == n - state["u"], "construction N")
    require(state["a"] == s - state["u"], "construction a")
    require(state["k_A"] == k - state["u"] - state["c"], "construction k_A")

    z_start, z_end = construction["Z_exponent_interval"]
    r_start, r_end = construction["R_exponent_interval"]
    require((z_start, z_end) == (0, state["u"]), "Z interval")
    require(r_start == z_end, "Z/R intervals overlap or gap")
    common_roots = r_end - r_start
    require(common_roots == construction["common_root_cluster_size"] == 4986, "R size")
    require(construction["agreement_block_start"] == r_end, "agreement block start")
    used_end = r_end + construction["agreement_block_count"] * construction["agreement_block_size"]
    require(used_end == construction["used_exponent_end"], "agreement block end")
    require(n - used_end == construction["unused_coordinates"] == 36315, "unused coordinates")
    scalars = construction["listed_scalars"]
    require(scalars == list(range(1, 16)), "listed scalars")
    require(len(set(value % field["p"] for value in scalars)) == 15, "scalar distinctness")
    require(all(value % field["p"] != 0 for value in scalars), "zero listed scalar")

    pivots = construction["pivot_degrees"]
    require(pivots == [0] + list(range(4986, 5000)), "construction pivot degrees")
    require(len(pivots) == 15 and len(set(pivots)) == 15, "pivot dimension")
    require(construction["e14"] == pivots[-2] == 4998, "construction e14")
    require(construction["e15"] == pivots[-1] == 4999, "construction e15")
    defect = sum(pivots) - comb(15, 2)
    require(defect == construction["alternant_defect"] == 69790, "construction defect")
    require(state["u"] + pivots[-1] == k - 1, "maximum direction degree")
    require(state["u"] + common_roots < k, "listed polynomial degree")

    agreement = state["u"] + common_roots + construction["agreement_block_size"]
    require(agreement == construction["each_exact_agreement"] == s, "exact agreement")
    require(construction["listed_points_certified"] == 15, "listed point count")
    rank_one_subsets = comb(common_roots, 15)
    require(rank_one_subsets == construction["rank_one_15_subsets"], "rank-one subset count")
    require(construction["overcount_factor"] == a14, "construction overcount factor")
    require(construction["dependent_incidence"] == 15 * rank_one_subsets, "dependent incidence")
    require(construction["first_owner_excess"] == 14 * rank_one_subsets, "first-owner excess")
    return {
        "common_roots": common_roots,
        "unused": construction["unused_coordinates"],
        "rank_one_subsets": rank_one_subsets,
    }


def check_gate(data: dict[str, Any]) -> dict[str, Any]:
    expected_nonclaims = [
        "no rank-15 bound",
        "no paid (u,c) state",
        "no c=152 closure",
        "no canonical order-independent owner",
        "no extension-field factor-p claim",
        "no unsigned-Mobius upper bound",
        "no target-sized counterexample",
        "no score movement",
    ]
    require(data["nonclaims"] == expected_nonclaims, "required nonclaims")
    gate = data["publication_gate"]
    require(gate["decision"] == "NARROW_PR_CANDIDATE_ONLY", "publication gate")
    require(gate["refuse_broader_claim"] is True, "broad-claim refusal")
    require(gate["score"] == "0/2", "score ledger")
    overlap = data["live_overlap"]
    require(overlap["maximum_pull_ref"] == 741, "live overlap maximum PR")
    expected_heads = {
        733: "db323972ea22dca0fecda4d2da6ebcb4c664b574",
        734: "fbcb0b53e010e7dcbb53d07ef3dbf9127217da5a",
        735: "f94d8706ae95e99462038e6d462a34332865be02",
        736: "97e2713f880c856ed4dace2440567cc11740ac57",
        737: "8fcd4152709889da768ec1453d05ec09bccfb41a",
        738: "72f559a5822ef00508a6fc7f8f772dfb14a31ed0",
        739: "1e8b9871de0f89c87c0d7339218e619fb6d57ae5",
        740: "0c7e2bec70bc1aef1c49e20f4341a43a6d85e991",
        741: "299e8160b51d8b45d205ae6978b3b97696dcb83f",
    }
    actual_heads = {entry["number"]: entry["head"] for entry in overlap["pulls"]}
    require(actual_heads == expected_heads, "live overlap heads")
    require("cross-credit" in overlap["pulls"][0]["relation"], "PR #733 cross-credit")
    relations = {entry["number"]: entry["relation"] for entry in overlap["pulls"]}
    require("no common-root slicing overlap" in relations[737], "PR #737 nonoverlap")
    require("no common-root slicing overlap" in relations[738], "PR #738 nonoverlap")
    require("no common-root slicing overlap" in relations[739], "PR #739 nonoverlap")
    require("no common-root slicing overlap" in relations[740], "PR #740 nonoverlap")
    require("no common-root slicing overlap" in relations[741], "PR #741 nonoverlap")
    return {"max_pr": overlap["maximum_pull_ref"], "heads": actual_heads}


def check_boundary_recurrence(
    data: dict[str, Any], field: dict[str, int]
) -> dict[str, dict[str, int]]:
    boundary = data["theorem"]["boundary_scan"]
    paid = boundary_scan(field["n"], field["k"], field["s"], 4985, 152)
    require(paid["value"] == boundary["paid_max"] == 20008483, "4985 boundary max")
    require(paid["c"] == boundary["paid_argmax_c"] == 0, "4985 boundary argmax c")
    require(
        paid["shifted_state"] == boundary["paid_shifted_state"] == 1043591,
        "4985 boundary shifted state",
    )
    tamper = boundary_scan(field["n"], field["k"], field["s"], 4986, 152)
    require(tamper["value"] == boundary["tamper_max"] == 290933620, "4986 boundary max")
    require(tamper["c"] == boundary["tamper_argmax_c"] == 0, "4986 boundary argmax c")
    require(
        tamper["shifted_state"] == boundary["tamper_shifted_state"] == 1043590,
        "4986 boundary shifted state",
    )
    return {"paid": paid, "tamper": tamper}


def check_certificate(data: dict[str, Any]) -> dict[str, Any]:
    check_static_provenance(data)
    field = check_field_ledger(data)
    check_theorem_static(data, field)
    residual = check_residual_consumer(data, field)
    ownership = check_ownership(data, field["p"])
    scalar = check_scalar_route(data, field, residual)
    construction = check_construction(data, field, ownership["a14"])
    overlap = check_gate(data)
    boundary = check_boundary_recurrence(data, field)
    return {
        "field": field,
        "residual": residual,
        "ownership": ownership,
        "scalar": scalar,
        "construction": construction,
        "overlap": overlap,
        "boundary": boundary,
    }


def load_certificate() -> dict[str, Any]:
    require(CERTIFICATE_PATH.is_file(), "certificate JSON is missing")
    value = json.loads(CERTIFICATE_PATH.read_text(encoding="ascii"))
    require(isinstance(value, dict), "certificate root is not an object")
    return value


def print_report(report: dict[str, Any]) -> None:
    field = report["field"]
    boundary = report["boundary"]
    ownership = report["ownership"]
    residual = report["residual"]
    scalar = report["scalar"]
    construction = report["construction"]
    overlap = report["overlap"]
    print("RANK15_COMMON_ROOT_HYPERPLANE_SLICING")
    print(f"base_commit={EXPECTED_BASE}")
    print(
        "field="
        f"p{field['p']},n{field['n']},K{field['k']},m{field['s']},"
        f"q_list={field['q_list']},T={field['target']}"
    )
    print(
        "rank14_boundary="
        f"4985:{boundary['paid']['value']},c{boundary['paid']['c']},"
        f"u{boundary['paid']['shifted_state']},p_product=42632203442671139,"
        "slack=232221907053516453;"
        f"4986:{boundary['tamper']['value']},c{boundary['tamper']['c']},"
        f"u{boundary['tamper']['shifted_state']},p_product=619894135709977460,"
        "excess=345040025213789868"
    )
    print(
        "mobius="
        f"nullities1..14,checks={ownership['identity_checks']},A14={ownership['a14']}"
    )
    print(
        "residual="
        f"c<=151_states={residual['state_count']},u=1042375..1043582,"
        "u+c<=1043588,nullity14_empty_for_u+c>=1043576;"
        f"c152_caps={','.join(map(str, residual['c152_caps']))}"
    )
    print(
        "scalar_route="
        f"t1_min={scalar['table'][0]['slack']},"
        f"t15_min={scalar['table'][14]['slack']},"
        f"baseline16_min={scalar['baseline'][0]},"
        f"table_sha256={scalar['table_digest']};"
        f"c152_table_sha256={scalar['c152_digest']}"
    )
    print(
        "construction="
        f"15_points,common_roots={construction['common_roots']},"
        f"agreement={field['s']},unused={construction['unused']},"
        f"rank_one_15_subsets={construction['rank_one_subsets']}"
    )
    heads = ",".join(f"{number}:{head}" for number, head in sorted(overlap["heads"].items()))
    print(f"overlap=max_pr={overlap['max_pr']},heads={heads}")
    print(f"certificate_sha256={file_sha256(CERTIFICATE_PATH)}")
    print("RESULT: PASS (narrow theorem only; no state or score movement)")


def tamper_selftest(data: dict[str, Any]) -> list[str]:
    check_certificate(data)
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("base_commit", lambda item: item["provenance"].__setitem__("base_commit", "0" * 40)),
        (
            "target",
            lambda item: item["field_ledger"].__setitem__(
                "one_row_target", item["field_ledger"]["one_row_target"] + 1
            ),
        ),
        (
            "list_bound",
            lambda item: item["theorem"].__setitem__(
                "list_bound", item["theorem"]["list_bound"] + 1
            ),
        ),
        (
            "nullity_range",
            lambda item: item["ownership_ledger"].__setitem__("nullity_max", 13),
        ),
        (
            "residual_state_count",
            lambda item: item["conditional_residual_consumer"]["c_le_151"].__setitem__(
                "state_count", 173030
            ),
        ),
        (
            "scalar_t15",
            lambda item: item["scalar_route_cut"].__setitem__(
                "c_le_151_minimum_t15_slack",
                item["scalar_route_cut"]["c_le_151_minimum_t15_slack"] + 1,
            ),
        ),
        (
            "construction_agreement",
            lambda item: item["construction"].__setitem__("each_exact_agreement", 1116046),
        ),
    ]
    rejected: list[str] = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(data)
        mutate(candidate)
        try:
            check_certificate(candidate)
        except VerificationError:
            rejected.append(name)
        else:
            raise VerificationError(f"tamper was accepted: {name}")
    require(len(rejected) == len(mutations), "tamper rejection count")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify the rank-15 common-root hyperplane-slicing packet."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="run the exact certificate")
    mode.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="prove that representative certificate mutations are rejected",
    )
    args = parser.parse_args()
    try:
        data = load_certificate()
        if args.tamper_selftest:
            rejected = tamper_selftest(data)
            print("RANK15_COMMON_ROOT_HYPERPLANE_SLICING_TAMPER_SELFTEST")
            print(f"rejected={','.join(rejected)}")
            print(f"RESULT: PASS ({len(rejected)}/{len(rejected)} tamper cases rejected)")
        else:
            print_report(check_certificate(data))
    except (OSError, ValueError, KeyError, TypeError, VerificationError) as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
