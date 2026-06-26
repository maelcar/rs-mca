#!/usr/bin/env python3
"""Arithmetic checks for the high-agreement adjacent-ledger theorem package.

This script does not verify the algebraic proofs.  It checks the finite
integer thresholds used in the F_17^32, n=512, k=256 corollaries.
"""

from math import ceil

def main() -> None:
    n = 512
    k = 256
    q = 17 ** 32
    target = 2 ** 128
    budget = q // target

    print("Field and target")
    print(f"q = 17^32 = {q}")
    print(f"floor(q / 2^128) = {budget}")
    print(f"6*2^128 < q: {6*target < q}")
    print(f"7*2^128 > q: {7*target > q}")
    print()

    tangent_start = ceil((2*n + k) / 3)
    list_unique_start = ceil((n + k) / 2)
    print("High-agreement starts")
    print(f"affine/projective line exact start ceil((2n+k)/3) = {tangent_start}")
    print(f"interleaved unique-list start ceil((n+k)/2) = {list_unique_start}")
    print()

    print("Affine/projective line plus interleaved-list ledger")
    for a in [506, 507, 508]:
        line_num = n - a + 1
        list_num = 1 if a >= list_unique_start else None
        total = line_num + (list_num or 0)
        print(
            f"a={a}, r={n-a}: line={line_num}, list={list_num}, "
            f"total={total}, total<=budget? {total <= budget}"
        )
    print()

    print("Degree-d finite-parameter curve ledger")
    print("d | curve exact start | safe with list | safe curve alone")
    for d in range(1, 11):
        curve_start = ceil(((d + 1) * n + k) / (d + 2))

        # With list term: d*(n-a+1)+1 <= budget.
        max_m_with_list = (budget - 1) // d
        if max_m_with_list >= 1:
            a_with_list = n + 1 - max_m_with_list
            safe_with_list = f"a >= {a_with_list} (r <= {n-a_with_list})"
        else:
            safe_with_list = "none"

        # Curve term alone: d*(n-a+1) <= budget.
        max_m_curve = budget // d
        if max_m_curve >= 1:
            a_curve = n + 1 - max_m_curve
            safe_curve = f"a >= {a_curve} (r <= {n-a_curve})"
        else:
            safe_curve = "none"

        print(f"{d:2d} | {curve_start:17d} | {safe_with_list:24s} | {safe_curve}")

if __name__ == "__main__":
    main()
