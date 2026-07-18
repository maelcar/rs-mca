#!/usr/bin/env python3
"""Verify source correspondence and all-depth cylinder modulus arithmetic."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def realized_image(depth: int) -> int:
    return (3**depth + 1) // 2


def markdown_section(source: str, heading: str) -> str:
    """Return the exact level-two Markdown section beginning at ``heading``."""
    marker = f"{heading}\n"
    start = source.index(marker)
    end = source.find("\n## ", start + len(marker))
    return source[start:] if end < 0 else source[start:end]


def verify(check_only: bool) -> tuple[int, int]:
    passed = 0
    total = 0

    def check(condition: bool, label: str) -> None:
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
        elif not check_only:
            print(f"FAIL: {label}")

    note = (
        ROOT / "experimental/notes/thresholds/cylinder_renormalization.md"
    ).read_text()
    lean = (
        ROOT
        / "experimental/lean/cylinder_renormalization/CylinderRenormalization.lean"
    ).read_text()

    setup = markdown_section(note, "## 0. Setup")
    check("`c = 3^B`" in setup, "source setup: base-3 modulus")
    check("`c = 2L - 1` exactly, V1" in setup, "source setup: exact ratio")

    u1 = markdown_section(note, "## 1. Theorem U1: failing bands are wide (every base)")
    check(
        "`c = 2L - 1` exact for even `B <= 64` (base 3)" in u1,
        "source U1/V1: verified modulus identity",
    )

    correction = markdown_section(
        note, "## 4. The cube corollary and the twisted-coset correction"
    )
    check(
        "Counterexample (twisted flatness)" in correction,
        "corrected source: twisted-flatness counterexample",
    )
    check(
        "magnitude\n> `sqrt(3)`" in correction,
        "corrected source: nonzero complex coefficient",
    )

    declarations = (
        "realizedImage_double",
        "modulus_identity_all",
        "modulus_identity",
    )
    for declaration in declarations:
        check(f"theorem {declaration}" in lean, f"Lean declaration: {declaration}")
    check(
        "2 * realizedImage B = 3 ^ B + 1" in lean,
        "Lean subtraction-free identity statement",
    )
    check(
        "3 ^ B = 2 * realizedImage B - 1" in lean,
        "Lean source normalization statement",
    )

    for depth in range(513):
        power = 3**depth
        image = realized_image(depth)
        check(power % 2 == 1, f"odd power depth={depth}")
        check(2 * image == power + 1, f"double identity depth={depth}")
        check(power == 2 * image - 1, f"modulus identity depth={depth}")

    for depth in (4, 6, 8, 16, 32, 64):
        check(
            3**depth == 2 * realized_image(depth) - 1,
            f"former finite API anchor depth={depth}",
        )

    check(3**8 == 2 * realized_image(8) - 1, "B=8 explanatory consumer")
    check(realized_image(0) == 1, "zero-depth boundary")
    check(realized_image(1) == 2, "odd-depth boundary")

    if not check_only:
        print("CYLINDER MODULUS IDENTITY SOURCE VERIFIER")
        print("range: 0 <= B <= 512; exact Python integers")
        print("source: corrected U1/V1 packet; Lean declarations: 3")
    return passed, total


def tamper_selftest() -> None:
    caught = 0
    caught += int(not (2 * realized_image(7) == 3**7))
    caught += int(not (3**8 == 2 * (realized_image(8) + 1) - 1))
    caught += int(not (3**5 % 2 == 0))
    caught += int(not (5**4 == 2 * realized_image(4) - 1))
    if caught != 4:
        raise AssertionError(f"tamper-selftest caught {caught}/4")
    print("tamper-selftest: caught 4/4")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="print only the result")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        tamper_selftest()
    passed, total = verify(args.check)
    if passed != total:
        print(f"RESULT: FAIL ({passed}/{total})")
        return 1
    print(f"RESULT: PASS ({passed}/{total})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
