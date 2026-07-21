#!/usr/bin/env python3
"""Verify the exact implication chain for D128 block-free injectivity."""

from __future__ import annotations

import json
from pathlib import Path


P = 2_147_483_647
REPO_ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "d128-blockfree-seven-moment-injectivity"
)


def load(name: str) -> dict:
    return json.loads((CERT_DIR / name).read_text(encoding="ascii"))


def main() -> None:
    small = load("small_side_moment_collision_audit.json")
    six_primary = load("six_set_moment_collision_primary.json")
    six_independent = load("six_set_moment_collision_independent.json")
    antipodal = load("antipodal_lee_audit_output.json")

    assert small["verdict"] == "PASS_D128_SMALL_SET_MOMENT_CLASSIFICATION"
    assert small["field"] == P
    assert small["root_count"] == 128
    assert small["T4_block_count"] == 32
    assert small["e4"]["classified_groups"] == 1
    assert small["e4"]["other_collision_groups"] == 0
    assert small["e4"]["exact_group_size_histogram"] == {"32": 1}
    assert small["e5"]["classified_groups"] == 128
    assert small["e5"]["other_collision_groups"] == 0
    assert small["e5"]["exact_group_size_histogram"] == {"31": 128}
    assert small["e5"]["disjoint_collision_pairs"] == 0

    expected_six = {
        "six_subsets_checked": 5_423_611_200,
        "exact_distinct_moment_keys": 5_423_375_296,
        "exact_collision_groups": 8_128,
        "exact_colliding_subsets": 244_032,
        "maximum_exact_group_size": 31,
        "fixed_pair_plus_T4_blocks_groups": 8_128,
        "other_collision_groups": 0,
        "disjoint_collision_pairs": 0,
    }
    assert six_primary["verdict"] == "PASS_ALL_E6_COLLISIONS_ARE_FIXED_PAIR_PLUS_T4_BLOCKS"
    assert six_independent["verdict"] == "ACCEPT_ALL_E6_COLLISIONS_ARE_FIXED_PAIR_PLUS_T4_BLOCKS"
    for key, value in expected_six.items():
        assert six_primary[key] == value
        assert six_independent[key] == value
    assert six_primary["exact_group_size_histogram"] == {"30": 7_936, "31": 192}
    assert six_independent["exact_group_size_histogram"] == six_primary[
        "exact_group_size_histogram"
    ]
    assert six_primary["common_intersection_size_histogram"] == {"2": 8_128}
    assert six_independent["common_intersection_size_histogram"] == six_primary[
        "common_intersection_size_histogram"
    ]

    assert antipodal["verdict"] == "PASS_D128_ANTIPODAL_LEE_COLLISION_EXCLUSION"
    assert antipodal["field"] == P
    assert antipodal["domain_points"] == 128
    assert antipodal["T4_blocks"] == 32
    assert antipodal["collision_profiles_excluded_count"] == 12

    # The e<=5 classification bounds the intersection of two distinct
    # block-free seven-sets by one.  An intersection of one would leave two
    # disjoint equal-moment six-sets, excluded above.  Thus a distinct pair
    # would be disjoint.  The antipodal certificate excludes every possible
    # disjoint seven-versus-seven profile, so no distinct pair exists.
    payload = {
        "verdict": "PASS_D128_BLOCKFREE_SEVEN_MOMENT_INJECTIVITY",
        "field": P,
        "domain": "roots of normalized T_128",
        "domain_points": 128,
        "T4_blocks": 32,
        "support_size": 7,
        "moments": [1, 2, 3],
        "small_side_intersection_upper": 1,
        "six_set_disjoint_collisions": 0,
        "therefore_distinct_seven_sets_are_disjoint": True,
        "antipodal_profiles_excluded": 12,
        "global_maximum_fiber_size": 1,
        "injective": True,
        "scope_guard": (
            "Exact theorem for F_2147483647, the normalized T_128 root set, "
            "and its T_4 partition."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
