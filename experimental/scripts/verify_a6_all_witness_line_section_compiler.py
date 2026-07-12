#!/usr/bin/env python3
"""Exact arithmetic checks for the canonical A6 all-witness compiler.

This checks only the finite parameter and degree ledger. It does not
machine-prove the imported Noether-form theorem or the algebraic-geometry
factor-specialization argument.
"""

from __future__ import annotations


def parameters(r: int) -> dict[str, int]:
    assert r >= 1
    return {
        "N": 500 * r,
        "kappa": 225 * r,
        "t": 150 * r,
        "d": 250 * r,
        "m": 4,
        "L": 52,
        "D": 1400 * r - 1,
    }


def unknown_count(D: int, w: int, L: int) -> tuple[int, int]:
    q = D // w
    total = sum((L - c + 1) * (D - c * w + 1) for c in range(q + 1))
    return q, total


def condition_count(m: int, L: int) -> int:
    return sum((m - j) * (L - j + 1) for j in range(m))


def slope_bound(r: int) -> int:
    p = parameters(r)
    q, _ = unknown_count(p["D"], p["kappa"] - 1, p["L"])
    delta = p["D"] + q
    exceptional = p["L"] + q * p["L"] * (12 * delta**6 + 1)
    moving = q + (p["N"] * q * (p["L"] + 1)) // (p["d"] - p["t"])
    return exceptional + moving


def check(r: int) -> int:
    p = parameters(r)
    w = p["kappa"] - 1
    q, unknowns = unknown_count(p["D"], w, p["L"])
    conditions = p["N"] * condition_count(p["m"], p["L"])

    assert q == 6
    assert p["D"] - 6 * w == 50 * r + 5 >= 0
    assert p["D"] - 7 * w == -175 * r + 6 < 0
    assert condition_count(p["m"], p["L"]) == 520
    assert unknowns == 260050 * r + 1022
    assert conditions == 260000 * r
    assert unknowns - conditions == 50 * r + 1022 > 0
    assert p["m"] * (p["N"] - p["t"]) > p["D"]
    assert p["d"] - p["t"] == 100 * r > 0

    delta = p["D"] + q
    assert delta == 1400 * r + 5
    assert q * p["L"] == 312
    assert 12 * q * p["L"] == 3744
    assert q * (p["L"] + 1) == 318

    moving_nontrivial = (
        p["N"] * q * (p["L"] + 1)
    ) // (p["d"] - p["t"])
    assert moving_nontrivial == 1590
    assert q + moving_nontrivial == 1596

    expected = 1960 + 3744 * (1400 * r + 5) ** 6
    assert slope_bound(r) == expected
    return 18


def tamper_checks() -> int:
    p = parameters(1)
    assert 3 * (p["N"] - p["t"]) <= p["D"]

    p = parameters(41)
    q, unknowns = unknown_count(p["D"], p["kappa"] - 1, 51)
    conditions = p["N"] * condition_count(4, 51)
    assert q == 6
    assert unknowns <= conditions

    r = 1
    old_repaired_claim = 1648 + 3744 * (1400 * r + 5) ** 6
    assert slope_bound(r) - old_repaired_claim == 312
    return 3


def main() -> None:
    checks = sum(check(r) for r in (1, 2, 3, 7, 41, 100, 1000))
    checks += tamper_checks()
    print(f"PASS: {checks} exact A6 compiler checks")


if __name__ == "__main__":
    main()
