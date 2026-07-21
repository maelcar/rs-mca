#!/usr/bin/env python3
"""Verify the cap-one M31 transfer-cap ledger and typed closing point."""

from __future__ import annotations

import json
from fractions import Fraction


def main() -> None:
    blockfree_fiber_cap = 1
    external_weight = 3_432
    refined_mass8_upper = blockfree_fiber_cap * external_weight
    assert refined_mass8_upper == 3_432

    ledger_components = {
        "complete_T8": 3_866_016,
        "canonical_T16": 216_216,
        "mixed_mass8": refined_mass8_upper,
        "mixed_mass16": 68_640,
        "mixed_mass24": 3_012_372,
    }
    refined_paid = sum(ledger_components.values())
    n = 2_097_152
    list_cardinality = 1_116_023
    global_budget = 16_777_215
    transfer_cap = global_budget * (list_cardinality + 1) // n
    transferred_upper = n * transfer_cap // (list_cardinality + 1)
    assert transfer_cap == 8_928_191
    assert transferred_upper == global_budget - 1

    refined_residual = transfer_cap - refined_paid
    assert refined_paid == 7_166_676
    assert refined_residual == 1_761_515

    # The least integer tau for which 26*q <= 33*tau can pay every integer
    # q up to the residual is ceil(26*(residual+1)/33).
    incidence_target = (26 * (refined_residual + 1) - 1) // 33
    assert incidence_target == 1_387_861

    ratio = Fraction(858, 133)
    base_resources = 12_285
    partial_resources = 3_556
    typed_upper = ratio * (base_resources * 21 + partial_resources * 4)
    floor_upper = typed_upper.numerator // typed_upper.denominator
    assert typed_upper == Fraction(33_365_046, 19)
    assert floor_upper == 1_756_055
    assert refined_residual - floor_upper == 5_460

    payload = {
        "verdict": "PASS_M31_TRANSFER_CAP_LEDGER",
        "inputs": {
            "blockfree_seven_moment_fiber_cap": blockfree_fiber_cap,
            "mixed_mass8_prefix_owner_is_unique": True,
            "external_weight": external_weight,
        },
        "ledger": {
            "components": ledger_components,
            "paid_total": refined_paid,
            "global_M31_budget": global_budget,
            "list_cardinality": list_cardinality,
            "transfer_cap": transfer_cap,
            "transferred_adjacent_upper": transferred_upper,
            "higher_tail_residual": refined_residual,
            "tail_incidence_sufficient_target": incidence_target,
        },
        "typed_sufficient_point": {
            "delta_base": 21,
            "delta_partial": 4,
            "price": "858/133",
            "exact_upper": str(typed_upper),
            "floor_upper": floor_upper,
            "slack": refined_residual - floor_upper,
        },
        "scope_guard": (
            "The typed codegrees 21 and 4 are sufficient hypotheses; this "
            "arithmetic verifier does not prove either global codegree."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
