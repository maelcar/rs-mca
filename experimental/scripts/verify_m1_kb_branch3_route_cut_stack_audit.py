#!/usr/bin/env python3
"""Self-contained stdlib audit of the KoalaBear rank-nine route-cut stack.

The audited tree is pinned at integration commit 48115af6.  This verifier
reads no repository file.  It independently rebuilds the actual-core rank
caps, the mask-deficit paid-cell counterexample, the live coarse-failure tail
gate, and the syndrome-rank cap.  It also freezes the old and repaired
terminal vocabularies so an unpaid sparse route cannot silently become an
owner through a machine-readable field name.
"""

from __future__ import annotations

import argparse
import copy
import math
import re
import sys
from typing import Any


STATUS = "AUDIT"
INTEGRATION = "48115af6"

P = 2_130_706_433
EXTENSION_DEGREE = 6
N = 2_097_152
K = 1_048_576
A = 1_116_048
R = N - K
J = N - A
DELTA_ZERO = R - J
RANK = 9
CORE_RANK = 8
DENOMINATOR = 1 << 128
B_STAR = (P**EXTENSION_DEGREE - 1) // DENOMINATOR
U_PAID = 2_602_502_999
B_REMAINING = B_STAR - U_PAID
M = B_REMAINING + 1

PAID_TERMINAL = "NON_CA_RANK9_SYNDROME_REDUCTION_PAID"
SPARSE_TERMINAL = "CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA"
PAID_CELL = "PAID_BY_PREDECESSOR_COARSE_RANK9_BOUND"
ONE_CUT_CELL = "COARSE_FAILURE_ONE_CUT_SCOPE"

SOURCE_PINS = {
    "experimental/notes/m1/m1_kb_branch3_actual_core_mds_rank_ladder_v1.md":
        (INTEGRATION, "c56bcafd7d6ffb1c4b8c65ed13b1d7dcb16a7888955de2cfdfc9bd8cc203f0f0"),
    "experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py":
        (INTEGRATION, "67f2cf1a4a61c0746ffffe17d413f9edcd371caa49a21a1262dec277365851a4"),
    "experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/"
    "m1_kb_branch3_actual_core_mds_v1.json":
        (INTEGRATION, "1d33311376fae565924bf9656d2e5f11b59a735238eb053aa6b485cceea80392"),
    "experimental/notes/m1/m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md":
        (INTEGRATION, "59d0d6075d023c673ff110ea7a7ee89f1b42ec8e51e90e90303843d3512345c3"),
    "experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py":
        (INTEGRATION, "c88d87e11da61f1b2fd2f40a2a39b3c43d3db35afc0bbc01bbded3721de1a880"),
    "experimental/data/certificates/m1-kb-branch3-rank9-mask-deficit-v1/"
    "m1_kb_branch3_rank9_mask_deficit_v1.json":
        (INTEGRATION, "926a2b34bc2c77b974d478d1ff7dc8bc9de97dc47ee4237e0d3d5e04787c7c8b"),
    "experimental/notes/m1/m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md":
        (INTEGRATION, "01cd01406f9994062f416a263e5fa3579631743c69929f9ed6ca2b59b5bc0ea6"),
    "experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py":
        (INTEGRATION, "ede048699dff02e9a1031355b36151b93c94a0df0151af07537c3fa505439c19"),
    "experimental/data/certificates/"
    "m1-kb-branch3-rank9-syndrome-rank-reduction-v1/"
    "m1_kb_branch3_rank9_syndrome_rank_reduction_v1.json":
        (INTEGRATION, "b7f346ed1a2c1136ed10f37f40862021d6e5759e7846e87f3d62e3c1ed79870f"),
}


class VerificationError(RuntimeError):
    """The embedded evidence or an exact audit identity drifted."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator > 0, "invalid ceiling division")
    return (numerator + denominator - 1) // denominator


def actual_core_cap(rank: int) -> int:
    core_rank = rank - 1
    mu = ceil_div(math.comb(DELTA_ZERO + core_rank, core_rank), rank)
    return math.comb(N, rank) // mu


def multiplicity(source_distance: int, deficit: int) -> int:
    extension = max(1, source_distance - J + deficit)
    basis_count = math.comb(DELTA_ZERO + CORE_RANK + deficit, CORE_RANK)
    return ceil_div(extension * basis_count, RANK)


def coarse_cap(carrier_size: int, source_distance: int) -> int:
    return math.comb(carrier_size, RANK) // multiplicity(source_distance, 0)


def scope_one_cut(carrier_size: int, source_distance: int) -> str:
    if coarse_cap(carrier_size, source_distance) <= B_REMAINING:
        return PAID_CELL
    return ONE_CUT_CELL


def old_unscoped_paid_cell() -> dict[str, Any]:
    carrier_size = 1_699_344
    source_distance = 1
    cutoff = 0
    budget = math.comb(carrier_size, RANK)
    mu0 = multiplicity(source_distance, 0)
    mu_high = multiplicity(source_distance, cutoff + 1)
    gain = mu_high - mu0
    excess_needed = budget + 1 - M * mu0

    # Literal old helper branch when excess_needed <= 0.
    required_high = 0
    clipped_t_star = M
    bad_low = clipped_t_star + 1
    bad_high = M - bad_low
    bad_weight = bad_low * mu0 + bad_high * mu_high

    displayed_t_star = (M * mu_high - budget - 1) // gain
    return {
        "carrier_size": carrier_size,
        "source_distance": source_distance,
        "cutoff": cutoff,
        "ambient_budget": budget,
        "mu_0": mu0,
        "mu_1": mu_high,
        "coarse_cap": budget // mu0,
        "scope": scope_one_cut(carrier_size, source_distance),
        "excess_needed": excess_needed,
        "old_required_high": required_high,
        "old_formal_T_star": clipped_t_star,
        "displayed_formula_T_star": displayed_t_star,
        "old_sharp_bad_low_count": bad_low,
        "old_sharp_bad_high_count": bad_high,
        "old_sharp_bad_weight": bad_weight,
        "old_sharp_bad_slack_below_budget": budget - bad_weight,
    }


def live_one_cut() -> dict[str, Any]:
    source_distance = 1
    cutoff = 18_014
    budget = math.comb(N, RANK)
    mu0 = multiplicity(source_distance, 0)
    mu_high = multiplicity(source_distance, cutoff + 1)
    gain = mu_high - mu0
    required_high = ceil_div(budget + 1 - M * mu0, gain)
    t_star = M - required_high
    return {
        "scope": scope_one_cut(N, source_distance),
        "cutoff": cutoff,
        "previous_cut_is_useful": (
            M * multiplicity(source_distance, cutoff) > budget
        ),
        "cut_is_useful": M * mu_high > budget,
        "required_high": required_high,
        "T_star": t_star,
        "sharp_bad_high_count": M - (t_star + 1),
    }


def syndrome_cap() -> dict[str, Any]:
    distance = R + 1
    exponent = (RANK + 1) - 2
    numerator = (J + 1) * distance**exponent
    denominator = (distance - J) ** exponent
    cap = numerator // denominator
    return {
        "distance": distance,
        "exponent": exponent,
        "numerator": numerator,
        "denominator": denominator,
        "cap": cap,
        "floor_lower": cap * denominator <= numerator,
        "floor_upper": numerator < (cap + 1) * denominator,
        "margin": B_REMAINING - cap,
    }


def evidence() -> dict[str, Any]:
    rank_caps = {rank: actual_core_cap(rank) for rank in range(4, 10)}
    return {
        "status": STATUS,
        "source_pins": copy.deepcopy(SOURCE_PINS),
        "row": {
            "R": R,
            "j": J,
            "Delta0": DELTA_ZERO,
            "B_star": B_STAR,
            "U_paid_before": U_PAID,
            "U_paid_after": U_PAID,
            "B_remaining_before": B_REMAINING,
            "B_remaining_after": B_REMAINING,
        },
        "actual_core": {
            "rank_caps": rank_caps,
            "rank_caps_are_alternatives_not_a_sum": True,
            "paid_ranks": [rank for rank, cap in rank_caps.items() if cap <= B_REMAINING],
            "first_uniformly_unpaid_rank": 9,
        },
        "mask_paid_cell": old_unscoped_paid_cell(),
        "mask_live_gate": live_one_cut(),
        "syndrome": {
            "old_classifier_fields": ["owner_terminal_count", "owner_terminals"],
            "old_reduction_fields": [
                "correlated_agreement_owner",
                "non_correlated_agreement_owner",
                "sparse_owner_paid_here",
            ],
            "old_terminals": [PAID_TERMINAL, SPARSE_TERMINAL],
            "old_CA_terminal_is_route_not_payment": True,
            "old_correlated_agreement_branch_paid": False,
            "repaired_classifier_fields": ["terminal_count", "terminals"],
            "repaired_reduction_fields": [
                "correlated_agreement_terminal",
                "non_correlated_agreement_terminal",
                "sparse_route_paid_here",
            ],
            "repaired_terminals": [PAID_TERMINAL, SPARSE_TERMINAL],
            "rank_reduction": syndrome_cap(),
        },
    }


def validate(value: dict[str, Any]) -> None:
    require(value["status"] == STATUS, "status drift")
    pins = value["source_pins"]
    require(pins == SOURCE_PINS, "source-pin manifest drift")
    require(len(pins) == 9, "source-pin count drift")
    for path, (commit, digest) in pins.items():
        require(path.startswith("experimental/"), "source path escaped experimental")
        require(commit == INTEGRATION, "integration pin drift")
        require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None, "bad SHA-256")

    row = value["row"]
    require((row["R"], row["j"], row["Delta0"]) == (1_048_576, 981_104, 67_472), "row arithmetic drift")
    require(row["B_star"] == 274_980_728_111_395_087, "B_star drift")
    require(row["U_paid_before"] == row["U_paid_after"] == U_PAID, "U ledger moved")
    require(row["B_remaining_before"] == row["B_remaining_after"] == B_REMAINING, "remaining ledger moved")

    actual = value["actual_core"]
    recomputed = {rank: actual_core_cap(rank) for rank in range(4, 10)}
    require(actual["rank_caps"] == recomputed, "actual-core cap drift")
    require(actual["paid_ranks"] == [4, 5, 6, 7, 8], "paid-rank window drift")
    require(recomputed[8] == 58_747_334_643_050_472, "rank-eight cap drift")
    require(recomputed[8] <= B_REMAINING < recomputed[9], "rank-eight/nine boundary drift")
    require(actual["first_uniformly_unpaid_rank"] == 9, "rank-nine residual erased")
    require(actual["rank_caps_are_alternatives_not_a_sum"] is True, "rank caps became additive")

    paid = value["mask_paid_cell"]
    require(paid == old_unscoped_paid_cell(), "paid-cell evidence drift")
    require(paid["scope"] == PAID_CELL, "paid boundary entered one-cut scope")
    require(paid["coarse_cap"] == 274_980_655_093_567_589, "paid boundary cap drift")
    require(paid["coarse_cap"] <= B_REMAINING, "boundary no longer predecessor-paid")
    require(paid["excess_needed"] < 0, "old paid-cell branch not reached")
    require(paid["displayed_formula_T_star"] == 275_574_617_157_636_283, "displayed threshold drift")
    require(paid["displayed_formula_T_star"] > M, "out-of-window threshold not exposed")
    require(paid["old_formal_T_star"] == M, "old threshold clipping drift")
    require(paid["old_sharp_bad_low_count"] == M + 1, "old bad-low count drift")
    require(paid["old_sharp_bad_high_count"] == -1, "negative histogram counterexample drift")
    require(paid["old_sharp_bad_weight"] > paid["ambient_budget"], "old alleged bad profile unexpectedly feasible")
    require(paid["old_sharp_bad_slack_below_budget"] < 0, "old sharpness sign drift")

    live = value["mask_live_gate"]
    require(live == live_one_cut(), "live one-cut evidence drift")
    require(live["scope"] == ONE_CUT_CELL, "live gate left coarse-failure scope")
    require(live["previous_cut_is_useful"] is False and live["cut_is_useful"] is True, "first useful cutoff drift")
    require(live["T_star"] == 17_907_572_507_584, "live T_star drift")
    require(live["sharp_bad_high_count"] >= 0, "live sharp profile is not a histogram")

    syndrome = value["syndrome"]
    require(syndrome["old_terminals"] == [PAID_TERMINAL, SPARSE_TERMINAL], "old terminal values drift")
    require(any("owner" in field for field in syndrome["old_classifier_fields"] + syndrome["old_reduction_fields"]), "old ownership vocabulary not recorded")
    require(syndrome["old_CA_terminal_is_route_not_payment"] is True, "old route flag drift")
    require(syndrome["old_correlated_agreement_branch_paid"] is False, "old charge flag drift")
    repaired_fields = syndrome["repaired_classifier_fields"] + syndrome["repaired_reduction_fields"]
    require(all("owner" not in field for field in repaired_fields), "repaired schema still calls the route an owner")
    require(syndrome["repaired_terminals"] == syndrome["old_terminals"], "repair changed terminal semantics")
    cap = syndrome["rank_reduction"]
    require(cap == syndrome_cap(), "syndrome cap evidence drift")
    require(cap["floor_lower"] and cap["floor_upper"], "syndrome floor boundary failed")
    require(cap["cap"] == 3_337_935_545_766_696, "syndrome cap drift")
    require(cap["margin"] == 271_642_789_963_125_392, "syndrome margin drift")


def set_path(value: dict[str, Any], path: tuple[Any, ...], replacement: Any) -> None:
    cursor: Any = value
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = replacement


def tamper_selftest() -> None:
    baseline = evidence()
    cases = [
        (("status",), "PROVED"),
        (("source_pins", next(iter(SOURCE_PINS))), (INTEGRATION, "0" * 64)),
        (("row", "U_paid_after"), U_PAID + 1),
        (("actual_core", "rank_caps", 8), actual_core_cap(8) + 1),
        (("actual_core", "paid_ranks"), [4, 5, 6, 7, 8, 9]),
        (("mask_paid_cell", "scope"), ONE_CUT_CELL),
        (("mask_paid_cell", "displayed_formula_T_star"), M),
        (("mask_paid_cell", "old_sharp_bad_high_count"), 0),
        (("mask_live_gate", "previous_cut_is_useful"), True),
        (("mask_live_gate", "T_star"), 17_907_572_507_585),
        (("syndrome", "old_terminals"), [PAID_TERMINAL]),
        (("syndrome", "repaired_classifier_fields", 1), "owner_terminals"),
        (("syndrome", "rank_reduction", "cap"), 3_337_935_545_766_697),
        (("syndrome", "old_correlated_agreement_branch_paid"), True),
    ]
    rejected = 0
    for path, replacement in cases:
        mutated = copy.deepcopy(baseline)
        set_path(mutated, path, replacement)
        try:
            validate(mutated)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError(f"tamper accepted: {path}")
    require(rejected == len(cases), "tamper count drift")
    print(f"PASS tamper-selftest: {rejected}/{len(cases)} mutations rejected")


def check() -> None:
    value = evidence()
    validate(value)
    paid = value["mask_paid_cell"]
    live = value["mask_live_gate"]
    cap = value["syndrome"]["rank_reduction"]
    print("PASS source pins: 9 integrated artifacts at 48115af6")
    print("PASS actual-core: ranks 4..8 paid; rank 9 remains nonuniform")
    print(
        "PASS mask boundary counterexample: "
        f"coarse cap={paid['coarse_cap']}; old sharp_bad_high_count=-1"
    )
    print(
        "PASS live mask gate: "
        f"D={live['cutoff']}; H_D<={live['T_star']}"
    )
    print(
        "PASS syndrome cap and terminology repair: "
        f"cap={cap['cap']}; sparse terminal remains unpaid"
    )
    print(f"STATUS: {STATUS}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.check:
            check()
        else:
            tamper_selftest()
    except (KeyError, TypeError, ValueError, VerificationError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
