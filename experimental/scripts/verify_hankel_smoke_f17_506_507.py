#!/usr/bin/env python3
"""Verify the M2 Hankel smoke packet for the F_17^32 threshold row."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_n512_k256_a506_507_hankel_smoke_packet.json"
TABLE = ROOT / "experimental/data/certificates/hankel-smoke-f17-506-507/f17_32_n512_k256_a506_507_numerator_table.json"
HIGH_AGREEMENT = ROOT / "experimental/data/certificates/high-agreement-threshold-package/f17_512_high_agreement_threshold_certificate.json"
SCHEMA_CHECKER = ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = ROOT / "scripts/aperiodic_eliminant_schema.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_schema_checker():
    spec = importlib.util.spec_from_file_location("check_aperiodic_eliminant_packet", SCHEMA_CHECKER)
    require(spec is not None and spec.loader is not None, "could not load schema checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    checker = load_schema_checker()
    checker.check_path(PACKET, SCHEMA)

    packet = load_json(PACKET)
    table = load_json(TABLE)
    high = load_json(HIGH_AGREEMENT)

    n = 512
    k = 256
    q_line = 17**32
    budget = q_line // 2**128
    exact_radius = (n - k) // 3
    exact_min_agreement = n - exact_radius

    require(budget == 6, "wrong q_line budget")
    require(6 * 2**128 < q_line < 7 * 2**128, "budget bracket failed")
    require(exact_radius == 85, "wrong exact tangent radius")
    require(exact_min_agreement == 427, "wrong exact tangent agreement")

    require(packet["row"]["n"] == n, "packet n mismatch")
    require(packet["row"]["k"] == k, "packet k mismatch")
    require(packet["agreement_threshold"] == 506, "packet threshold mismatch")
    require(packet["declared_aperiodic_numerator"] == 0, "aperiodic numerator should be zero after tangent removal")

    high_affine = high["f17_512_affine"]
    require(high_affine["budget"] == budget, "high-agreement budget mismatch")
    require(high_affine["last_unsafe_agreement"] == 506, "high-agreement unsafe row mismatch")
    require(high_affine["first_safe_agreement"] == 507, "high-agreement safe row mismatch")
    require(high_affine["unsafe_line_numerator"] == 7, "high-agreement unsafe numerator mismatch")
    require(high_affine["safe_line_numerator"] == 6, "high-agreement safe numerator mismatch")
    require(high_affine["exact_range_min_agreement"] == exact_min_agreement, "high-agreement range mismatch")

    table_rows = {row["A"]: row for row in table["rows"]}
    packet_rows = {row["A"]: row for row in packet["exact_agreements"]}
    expected = {
        506: {
            "j": 6,
            "t": 250,
            "r": 6,
            "numerator": 7,
            "verdict": "UNSAFE_BY_PROVED_LOWER_BOUND",
            "safe": False,
        },
        507: {
            "j": 5,
            "t": 251,
            "r": 5,
            "numerator": 6,
            "verdict": "SAFE_BY_PROVED_UPPER_BOUND",
            "safe": True,
        },
    }

    for agreement, expected_row in expected.items():
        require(agreement in table_rows, f"missing table row {agreement}")
        require(agreement in packet_rows, f"missing packet row {agreement}")
        table_row = table_rows[agreement]
        packet_row = packet_rows[agreement]

        require(packet_row["j"] == n - agreement, f"packet j mismatch at A={agreement}")
        require(packet_row["t"] == agreement - k, f"packet t mismatch at A={agreement}")
        require(packet_row["status"] == "empty", f"packet row should be empty after tangent removal at A={agreement}")
        require(packet_row["residual_after_removed_ledgers"] == 0, f"packet residual mismatch at A={agreement}")
        require(packet_row["known_total_numerator"] == expected_row["numerator"], f"packet numerator mismatch at A={agreement}")

        require(table_row["j"] == expected_row["j"], f"table j mismatch at A={agreement}")
        require(table_row["t"] == expected_row["t"], f"table t mismatch at A={agreement}")
        require(table_row["r"] == expected_row["r"], f"table r mismatch at A={agreement}")
        require(table_row["ld_sw_numerator"] == n - agreement + 1, f"LD formula mismatch at A={agreement}")
        require(table_row["ld_sw_numerator"] == expected_row["numerator"], f"table numerator mismatch at A={agreement}")
        require(table_row["tangent_numerator"] == expected_row["numerator"], f"tangent numerator mismatch at A={agreement}")
        require(table_row["aperiodic_after_removed_ledgers"] == 0, f"aperiodic row mismatch at A={agreement}")
        require(table_row["denominator"] == q_line, f"denominator mismatch at A={agreement}")
        require(table_row["verdict"] == expected_row["verdict"], f"verdict mismatch at A={agreement}")
        require((table_row["ld_sw_numerator"] <= budget) is expected_row["safe"], f"budget comparison mismatch at A={agreement}")

    removed = {ledger["name"]: ledger["numerator"] for ledger in packet["removed_ledgers"]}
    require(removed["tangent_common_code_line_A506"] == 7, "removed A506 ledger mismatch")
    require(removed["tangent_common_code_line_A507"] == 6, "removed A507 ledger mismatch")

    transition = table["closed_grid_transition"]
    require(transition["largest_safe_integer_radius"] == 5, "safe radius mismatch")
    require(transition["first_unsafe_integer_radius"] == 6, "unsafe radius mismatch")
    require(transition["first_safe_agreement"] == 507, "first safe agreement mismatch")
    require(transition["last_unsafe_agreement"] == 506, "last unsafe agreement mismatch")
    require(transition["supremum_attained"] is False, "supremum convention mismatch")

    print("M2 Hankel smoke packet checks passed")
    print("  row: RS[F_17^32,H,256], n=512, k=256")
    print("  budget: floor(17^32 / 2^128) = 6")
    print("  A=506: LD_sw=7 unsafe")
    print("  A=507: LD_sw=6 safe")
    print("  declared aperiodic numerator after tangent removal: 0")


if __name__ == "__main__":
    main()
