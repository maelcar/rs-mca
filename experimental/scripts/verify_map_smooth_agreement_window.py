#!/usr/bin/env python3
"""Verify source correspondence and finite arithmetic for the map-smooth window."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def nat_div(k: int, a: int) -> int:
    return 0 if a == 0 else k // a


def nat_mod(k: int, a: int) -> int:
    return k if a == 0 else k % a


def agreement(k: int, a: int) -> int:
    return a * (nat_div(k, a) + 2)


def divides(a: int, k: int) -> bool:
    return k == 0 if a == 0 else k % a == 0


def labeled_environment(source: str, label: str) -> str:
    """Return the exact TeX environment containing ``\\label{label}``."""
    marker = f"\\label{{{label}}}"
    label_at = source.index(marker)
    begin_at = source.rfind("\\begin{", 0, label_at)
    if begin_at < 0:
        raise ValueError(f"no TeX environment begins before {label}")
    env_start = begin_at + len("\\begin{")
    env_end = source.index("}", env_start)
    environment = source[env_start:env_end]
    end_marker = f"\\end{{{environment}}}"
    end_at = source.index(end_marker, label_at) + len(end_marker)
    return source[begin_at:end_at]


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

    thresholds = (ROOT / "experimental/rs_mca_thresholds.tex").read_text()
    frontiers = (ROOT / "experimental/asymptotic_rs_mca_frontiers.tex").read_text()
    lean = (
        ROOT / "experimental/lean/petal_fiber/PetalFiber.lean"
    ).read_text()

    for name, source in (("thresholds", thresholds), ("frontiers", frontiers)):
        block = labeled_environment(source, "lem:map-smooth-fiber")
        check("\\label{lem:map-smooth-fiber}" in block, f"{name}: source label")
        check("k+a+1\\le A\\le k+2a" in block, f"{name}: agreement window")
        check("a\\mid k" in block, f"{name}: divisibility equality")
    map_smooth_definition = labeled_environment(thresholds, "def:map-smooth")
    check("c\\ge1" in map_smooth_definition, "thresholds: positive map degree")

    declarations = (
        "map_smooth_agreement_remainder",
        "map_smooth_agreement_lower",
        "map_smooth_agreement_upper",
        "map_smooth_agreement_window",
        "map_smooth_agreement_eq_of_dvd",
        "map_smooth_agreement_eq_top_iff",
        "map_smooth_agreement_lower_false_at_zero",
    )
    for declaration in declarations:
        check(f"theorem {declaration}" in lean, f"Lean declaration: {declaration}")
    check(
        "+ k₀ % a₀ = k₀ + 2 * a₀" in lean,
        "Lean remainder-identity statement",
    )
    check("(ha : 0 < a₀)" in lean, "Lean explicit positivity hypothesis")
    check("↔ a₀ ∣ k₀" in lean, "Lean exact divisibility characterization")

    for a in range(65):
        for k in range(257):
            value = agreement(k, a)
            remainder = nat_mod(k, a)
            top = k + 2 * a
            check(value + remainder == top, f"remainder identity a={a}, k={k}")
            check(value <= top, f"upper endpoint a={a}, k={k}")
            check(
                (k + a + 1 <= value) == (a > 0),
                f"lower endpoint iff positivity a={a}, k={k}",
            )
            check(
                (value == top) == divides(a, k),
                f"top equality iff divisibility a={a}, k={k}",
            )

    check(agreement(2, 3) == 6, "lower-sharp anchor a=3, k=2")
    check(agreement(6, 3) == 12, "upper-sharp anchor a=3, k=6")
    check(agreement(7, 3) == 12 < 13, "strict-top anchor a=3, k=7")
    check(not (1 <= agreement(0, 0)), "zero-degree lower counterexample")

    if not check_only:
        print("MAP-SMOOTH AGREEMENT WINDOW SOURCE VERIFIER")
        print("range: 0 <= a <= 64, 0 <= k <= 256; Lean-style total Nat division")
        print("source labels: thresholds + frontiers; declarations: 7")
    return passed, total


def tamper_selftest() -> None:
    caught = 0
    caught += int(not (agreement(7, 3) + 1 + nat_mod(7, 3) == 7 + 2 * 3))
    caught += int(not (2 + 3 + 1 <= agreement(2, 3) - 1))
    caught += int(not (agreement(6, 3) + 1 <= 6 + 2 * 3))
    caught += int(not ((7 + 2 * 3 == 7 + 2 * 3) == divides(3, 7)))
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
