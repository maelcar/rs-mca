#!/usr/bin/env python3
"""Verify arithmetic for generalized high-agreement ledger formulas."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import floor, log2

EPS_DEN = 2**128


def budget(Q: int) -> int:
    return Q // EPS_DEN


def line_range_radius(n: int, k: int) -> int:
    return (n - k) // 3


def list_range_radius(n: int, k: int) -> int:
    return (n - k) // 2


def curve_range_radius(n: int, k: int, d: int) -> int:
    return (n - k) // (d + 2)


def line_safe_radius(Q: int) -> int:
    return budget(Q) - 1


def line_plus_list_safe_radius(Q: int) -> int:
    return budget(Q) - 2


def curve_safe_radius(Q: int, d: int) -> int:
    return budget(Q) // d - 1


def curve_plus_list_safe_radius(Q: int, d: int) -> int:
    return (budget(Q) - 1) // d - 1


def classify_radius(safe_r: int, exact_r: int) -> str:
    if safe_r < 0:
        return "no radius-zero certificate"
    if safe_r < exact_r:
        return f"threshold pinned in exact range; largest safe r={safe_r}, first unsafe r={safe_r+1}"
    return f"safe throughout exact range up to r={exact_r}; threshold not pinned by tangent method"


@dataclass(frozen=True)
class Row:
    name: str
    n: int
    k: int
    Q: int


def print_row(row: Row) -> None:
    B = budget(row.Q)
    R = row.n - row.k
    print(f"ROW {row.name}")
    print(f"  n={row.n}, k={row.k}, R=n-k={R}")
    print(f"  Q={row.Q}")
    print(f"  B=floor(Q/2^128)={B}")
    print(f"  exact line radius range r<=floor(R/3)={line_range_radius(row.n,row.k)}")
    print(f"  interleaved uniqueness range r<=floor(R/2)={list_range_radius(row.n,row.k)}")
    print(f"  line alone: {classify_radius(line_safe_radius(row.Q), line_range_radius(row.n,row.k))}")
    print(f"  line + one list: {classify_radius(line_plus_list_safe_radius(row.Q), line_range_radius(row.n,row.k))}")
    for d in range(1, 9):
        exact = curve_range_radius(row.n, row.k, d)
        safe_curve = curve_safe_radius(row.Q, d)
        safe_curve_list = curve_plus_list_safe_radius(row.Q, d)
        print(
            f"  degree d={d}: exact r<={exact}; "
            f"curve alone safe r<={safe_curve}; curve+list safe r<={safe_curve_list}"
        )
    print()


def prize_rate_thresholds() -> None:
    print("PRIZE-RATE APPLICABILITY AT k=2^40")
    k = 2**40
    for rho_num, rho_den in [(1,2), (1,4), (1,8), (1,16)]:
        n = k * rho_den // rho_num
        R = n - k
        max_line_r = R / 3
        lambda_max = 128 + log2(max_line_r)
        print(
            f"  rho={rho_num}/{rho_den}: n={n}, R={R}, "
            f"R/3={max_line_r:.6g}, lambda_max≈{lambda_max:.3f}"
        )
    print()


def bit_size_table() -> None:
    print("FIELD-BIT BUDGET TABLE FOR Q=2^lambda")
    for lam in [128, 129, 130, 131, 140, 150, 160, 170, 192, 256]:
        Q = 2**lam
        B = budget(Q)
        print(
            f"  lambda={lam:3d}: B=2^{lam-128}={B}; "
            f"line safe r<={B-1}; line+list safe r<={B-2}"
        )
    print()


def main() -> None:
    q_f17 = 17**32
    row = Row("RS[F_17^32,H,256], |H|=512", n=512, k=256, Q=q_f17)
    print_row(row)

    assert budget(q_f17) == 6
    assert line_range_radius(512, 256) == 85
    assert line_safe_radius(q_f17) == 5
    assert line_plus_list_safe_radius(q_f17) == 4
    assert curve_safe_radius(q_f17, 2) == 2
    assert curve_plus_list_safe_radius(q_f17, 2) == 1
    assert curve_safe_radius(q_f17, 6) == 0
    assert curve_plus_list_safe_radius(q_f17, 6) == -1

    bit_size_table()
    prize_rate_thresholds()

    print("All generalized high-agreement ledger arithmetic checks passed.")


if __name__ == "__main__":
    main()
