#!/usr/bin/env python3
"""Verify the Route-D complementary marked-key charge v1.

The script checks saturated scalar- and strict cell-complement fixtures for
the complementary charge theorem and two negative interfaces: image-only
labeling and summing local per-key caps.  It is deterministic and fail-closed.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from typing import Mapping


T = 2
P = 5
TARGET = T * P
MARKED = frozenset({0, 1})
SCALARS = tuple(range(P))
CELL_T = 2
CELL_P = 3
CELL_TARGET = CELL_T * CELL_P
SOURCE_PINS = {
    "prefix_commit": "e83962ae5ad7bacb391b691ffd37f0abef977b83",
    "marked_key_commit": "b23f997474f7a7aec9a889d933c774acc4980050",
    "f17_contact_commit": "6f56b42aff5758f354c72203b07831fd6241eef4",
    "first_match_commit": "0955594bf354b6a396574b65fbb242715edd3267",
    "disjointization_commit": "764f1c0243770baa437d4ae790b1448afa091680",
    "addback_commit": "4a2f0fbd8ab55ef107d26ebb5064a424430ca327",
    "priority_zero_commit": "8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67",
    "rank_adapter_commit": "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0",
}


class CertificateError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def positive_fixture() -> dict[str, object]:
    generated = tuple(
        ("generated", row, scalar)
        for row in range(T)
        for scalar in sorted(MARKED)
    )
    complement = tuple(scalar for scalar in SCALARS if scalar not in MARKED)
    bases = tuple(
        (
            "base",
            scalar,
            ("literal_G", scalar),
            ("beta", 16),
            ("U0", scalar * scalar % P),
            ("H", 1),
            ("decoder", scalar + 100),
        )
        for scalar in complement
    )
    defects = tuple(
        ("defect", profile, base)
        for base in bases
        for profile in range(T)
    )

    generated_charge = {
        item: (item[1], item[2])
        for item in generated
    }
    base_scalar = {
        base: base[1]
        for base in bases
    }
    defect_charge = {
        item: (item[1], base_scalar[item[2]])
        for item in defects
    }

    require(len(set(generated_charge.values())) == len(generated),
            "generated charge is not injective")
    require(len(set(defect_charge.values())) == len(defects),
            "defect charge is not injective")
    require(all(label[1] in MARKED for label in generated_charge.values()),
            "generated scalar left marked set")
    require(all(label[1] not in MARKED for label in defect_charge.values()),
            "defect scalar entered marked set")

    combined = {
        ("left", item): label
        for item, label in generated_charge.items()
    }
    combined.update({
        ("right", item): label
        for item, label in defect_charge.items()
    })
    require(len(set(combined.values())) == len(combined),
            "combined complementary charge is not injective")
    require(len(combined) <= TARGET, "complementary target failed")
    require(len(combined) == TARGET, "positive fixture did not saturate target")

    realized_base_scalars = tuple(base_scalar[base] for base in bases)
    require(len(set(realized_base_scalars)) == len(bases),
            "complete-base scalar is not injective")
    profile_base_keys = {
        (item[1], item[2])
        for item in defects
    }
    require(len(profile_base_keys) == len(defects),
            "profile/complete-base factorization is not injective")

    return {
        "marked_size": len(MARKED),
        "complement_size": len(complement),
        "generated_count": len(generated),
        "defect_count": len(defects),
        "combined_count": len(combined),
        "combined_label_count": len(set(combined.values())),
        "target": TARGET,
        "saturates_target": len(combined) == TARGET,
        "complete_base_count": len(bases),
        "profile_base_key_count": len(profile_base_keys),
    }


def strict_cell_complement_fixture() -> dict[str, object]:
    scalars = tuple(range(CELL_P))
    generated = tuple(("generated", scalar) for scalar in scalars)
    defects = tuple(
        (
            "defect",
            scalar,
            ("literal_G", scalar),
            ("beta", 7),
            ("U0", scalar * scalar % CELL_P),
            ("H", 1),
            ("decoder", scalar + 20),
        )
        for scalar in scalars
    )
    generated_charge = {item: (0, item[1]) for item in generated}
    defect_charge = {item: (1, item[1]) for item in defects}
    marked_cells = {(0, scalar) for scalar in scalars}
    literal_common_core_preserved = all(
        item[2] == ("literal_G", item[1]) for item in defects
    )
    require(literal_common_core_preserved, "cell fixture lost literal common core")

    require(len(set(generated_charge.values())) == len(generated),
            "cell fixture generated charge is not injective")
    require(len(set(defect_charge.values())) == len(defects),
            "cell fixture defect charge is not injective")
    require(all(label in marked_cells for label in generated_charge.values()),
            "cell fixture generated charge left E")
    require(all(label not in marked_cells for label in defect_charge.values()),
            "cell fixture defect charge entered E")

    combined_labels = set(generated_charge.values()) | set(defect_charge.values())
    require(len(combined_labels) == len(generated) + len(defects),
            "cell fixture combined charge is not injective")
    require(len(combined_labels) == CELL_TARGET,
            "cell fixture did not saturate target")

    generated_scalars = {label[1] for label in generated_charge.values()}
    defect_scalars = {label[1] for label in defect_charge.values()}
    scalar_subsets = tuple(
        frozenset(s for s in scalars if mask & (1 << s))
        for mask in range(1 << CELL_P)
    )
    scalar_separators = tuple(
        marked for marked in scalar_subsets
        if generated_scalars <= marked and defect_scalars.isdisjoint(marked)
    )
    require(generated_scalars == set(scalars),
            "cell fixture generated scalar projection drift")
    require(defect_scalars == set(scalars),
            "cell fixture defect scalar projection drift")
    require(not scalar_separators,
            "cell fixture unexpectedly admits scalar separation")

    return {
        "t": CELL_T,
        "p": CELL_P,
        "target": CELL_TARGET,
        "generated_count": len(generated),
        "defect_count": len(defects),
        "combined_label_count": len(combined_labels),
        "marked_cell_count": len(marked_cells),
        "generated_scalar_count": len(generated_scalars),
        "defect_scalar_count": len(defect_scalars),
        "scalar_separator_count": len(scalar_separators),
        "cell_separation_saturates_target": len(combined_labels) == CELL_TARGET,
        "scalar_separation_impossible": not scalar_separators,
        "literal_common_core_preserved": literal_common_core_preserved,
    }


def negative_fixtures() -> dict[str, object]:
    labels = tuple((row, scalar) for row in range(T) for scalar in SCALARS)
    generated_supports = tuple(
        (label, copy_bit)
        for label in labels
        for copy_bit in range(2)
    )
    image = {support[0] for support in generated_supports}
    require(len(image) == TARGET, "image fixture target drift")
    require(len(generated_supports) == 2 * TARGET,
            "copy-bit support fixture drift")
    require(len(generated_supports) > TARGET,
            "image-only countermodel did not violate support target")

    keys = tuple(range(3))
    local_families = {
        key: tuple((key, scalar) for scalar in SCALARS)
        for key in keys
    }
    require(all(len(family) <= P for family in local_families.values()),
            "local one-scalar cap fixture drift")
    local_sum = sum(len(family) for family in local_families.values())
    require(local_sum == len(keys) * P, "key sum drift")
    require(local_sum > TARGET, "local caps accidentally imply global cap")

    return {
        "label_image_count": len(image),
        "copy_bit_support_count": len(generated_supports),
        "image_only_violates_target": len(generated_supports) > TARGET,
        "local_key_count": len(keys),
        "per_key_cap": P,
        "summed_local_mass": local_sum,
        "local_caps_do_not_imply_global_cap": local_sum > TARGET,
    }


def summarize() -> dict[str, object]:
    return {
        "source_pins": dict(SOURCE_PINS),
        "parameters": {"t": T, "p": P, "target": TARGET},
        "positive": positive_fixture(),
        "strict_cell_complement": strict_cell_complement_fixture(),
        "negative": negative_fixtures(),
    }


EXPECTED = {
    "parameters": {"t": 2, "p": 5, "target": 10},
    "positive": {
        "marked_size": 2,
        "complement_size": 3,
        "generated_count": 4,
        "defect_count": 6,
        "combined_count": 10,
        "combined_label_count": 10,
        "target": 10,
        "saturates_target": True,
        "complete_base_count": 3,
        "profile_base_key_count": 6,
    },
    "strict_cell_complement": {
        "t": 2,
        "p": 3,
        "target": 6,
        "generated_count": 3,
        "defect_count": 3,
        "combined_label_count": 6,
        "marked_cell_count": 3,
        "generated_scalar_count": 3,
        "defect_scalar_count": 3,
        "scalar_separator_count": 0,
        "cell_separation_saturates_target": True,
        "scalar_separation_impossible": True,
        "literal_common_core_preserved": True,
    },
    "negative": {
        "label_image_count": 10,
        "copy_bit_support_count": 20,
        "image_only_violates_target": True,
        "local_key_count": 3,
        "per_key_cap": 5,
        "summed_local_mass": 15,
        "local_caps_do_not_imply_global_cap": True,
    },
}


def verify(summary: Mapping[str, object]) -> None:
    require(summary["source_pins"] == SOURCE_PINS, "source pin drift")
    for key, value in EXPECTED.items():
        require(summary[key] == value, f"{key} drift")


def tamper_suite(summary: Mapping[str, object]) -> int:
    trials = [
        ("parameters", "target", 9),
        ("positive", "generated_count", 5),
        ("positive", "defect_count", 5),
        ("positive", "combined_count", 9),
        ("positive", "combined_label_count", 9),
        ("positive", "saturates_target", False),
        ("positive", "complete_base_count", 2),
        ("positive", "profile_base_key_count", 5),
        ("strict_cell_complement", "target", 5),
        ("strict_cell_complement", "generated_count", 2),
        ("strict_cell_complement", "defect_count", 2),
        ("strict_cell_complement", "combined_label_count", 5),
        ("strict_cell_complement", "marked_cell_count", 2),
        ("strict_cell_complement", "scalar_separator_count", 1),
        ("strict_cell_complement", "cell_separation_saturates_target", False),
        ("strict_cell_complement", "scalar_separation_impossible", False),
        ("strict_cell_complement", "literal_common_core_preserved", False),
        ("negative", "label_image_count", 9),
        ("negative", "copy_bit_support_count", 19),
        ("negative", "image_only_violates_target", False),
        ("negative", "local_key_count", 2),
        ("negative", "summed_local_mass", 10),
        ("negative", "local_caps_do_not_imply_global_cap", False),
    ]
    detected = 0
    for section, key, replacement in trials:
        forged = copy.deepcopy(summary)
        forged[section][key] = replacement
        try:
            verify(forged)
        except CertificateError:
            detected += 1
    require(detected == len(trials), "tamper suite failed open")
    return detected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        summary = summarize()
        verify(summary)
        if args.self_test:
            summary["tamper_trials"] = tamper_suite(summary)
    except CertificateError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print("PASS: Route-D complementary marked-key charge v1")
        print(f"positive mass: {summary['positive']['combined_count']}")
        print(f"target: {summary['parameters']['target']}")
        print(
            "strict cell mass: "
            f"{summary['strict_cell_complement']['combined_label_count']}"
        )
        print(
            "strict cell scalar separators: "
            f"{summary['strict_cell_complement']['scalar_separator_count']}"
        )
        print(f"image-only support: {summary['negative']['copy_bit_support_count']}")
        print(f"summed local mass: {summary['negative']['summed_local_mass']}")
        if args.self_test:
            print(f"tamper trials: {summary['tamper_trials']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
