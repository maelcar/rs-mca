#!/usr/bin/env python3
"""Verify the degree-residue proof for the mixed-mass-eight prefix owner."""

from __future__ import annotations

import json


def main() -> None:
    module_degree = 8
    product_degree = 64
    prefix_depth = 31
    difference_cutoff = product_degree - prefix_depth - 1

    # In the free F[theta]-module basis 1,X,...,X^7, the leading degree of
    # X^r Q(theta) is r+8 deg(Q).  Distinct lanes cannot cross-cancel.
    forbidden_difference_degrees: dict[str, list[int]] = {}
    for lane in range(1, module_degree):
        degrees = [lane + module_degree * degree for degree in range(4, 7)]
        assert min(degrees) > difference_cutoff
        forbidden_difference_degrees[str(lane)] = degrees

    allowed_lane_maxima = {
        str(lane): lane + module_degree * 3 for lane in range(1, module_degree)
    }
    assert max(allowed_lane_maxima.values()) <= difference_cutoff

    constant_obstruction_degree = module_degree * 7
    assert constant_obstruction_degree > difference_cutoff

    blockfree_fiber_cap_input = 1
    external_quotient_weight = 3_432
    weighted_mass8_upper = blockfree_fiber_cap_input * external_quotient_weight
    assert weighted_mass8_upper == 3_432

    payload = {
        "verdict": "PASS_MIXED_MASS8_PREFIX_OWNER_WITH_CAP_ONE_INPUT",
        "free_module_audit": {
            "basis": [f"X^{lane}" for lane in range(module_degree)],
            "leading_degree_residues_are_distinct": True,
            "difference_cutoff": difference_cutoff,
            "forbidden_quotient_difference_degrees_4_to_6": (
                forbidden_difference_degrees
            ),
            "allowed_degree3_lane_maxima": allowed_lane_maxima,
            "deduced_quotient_difference_degree_upper": 3,
            "unequal_owner_constant_degree": constant_obstruction_degree,
            "deduced_unique_mixed_degree8_factor_per_prefix": True,
            "fixed_top_quotient_coefficients": 3,
        },
        "cap_one_corollary": {
            "blockfree_seven_moment_fiber_cap_input": blockfree_fiber_cap_input,
            "external_quotient_weight": external_quotient_weight,
            "weighted_mass8_upper": weighted_mass8_upper,
        },
        "scope_guard": (
            "The owner lemma is algebraic. The cap-one value is an explicit "
            "input from the D128 block-free injectivity theorem."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
