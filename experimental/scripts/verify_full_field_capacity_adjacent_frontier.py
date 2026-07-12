#!/usr/bin/env python3
"""Exact replay for the full-field capacity-adjacent MCA frontier."""
from __future__ import annotations

from math import comb


def ceil_div(num: int, den: int) -> int:
    assert num >= 0 and den > 0
    return (num + den - 1) // den


def qsep(m: int) -> int:
    return max(m, m * (m - 1) // 2)


def adjacent_secant_lower(q: int, m: int) -> int:
    """PR #669 at a=k+1 with the full-field challenge G=q."""
    return ceil_div((q - 1) * m, m + q - 1)


def check_symbolic_instance(epsilon_den: int, q: int, m: int) -> None:
    """Replay the three proof branches for a scaled target denominator."""
    assert epsilon_den >= 4
    assert 2 <= q < epsilon_den * epsilon_den
    assert m >= 1
    target = q // epsilon_den
    if m <= target:
        assert q > qsep(m)
        return
    if m == target + 1:
        assert q > qsep(m), (epsilon_den, q, m, target, qsep(m))
        return
    assert m >= target + 2
    assert adjacent_secant_lower(q, m) > target


def scaled_exhaustive() -> int:
    count = 0
    for epsilon_den in range(4, 65):
        for q in range(2, epsilon_den * epsilon_den):
            target = q // epsilon_den
            for m in range(1, target + 9):
                check_symbolic_instance(epsilon_den, q, m)
                count += 1
    return count


def main() -> None:
    epsilon_den = 1 << 128

    n, k = 128, 64
    q_domain = 3**32
    q_unsafe = 3**96
    q_safe = 3**160
    m = comb(n, k + 1)
    target_unsafe = q_unsafe // epsilon_den
    target_safe = q_safe // epsilon_den
    lower_unsafe = adjacent_secant_lower(q_unsafe, m)

    assert [pow(3, d, 128) for d in (1, 2, 4, 8, 16, 32)] \
        == [3, 9, 81, 33, 65, 1]
    assert 96 % 32 == 0 and 160 % 32 == 0
    assert (q_domain - 1) % 128 == 0

    for q in (q_unsafe, q_safe):
        assert q < 1 << 256
        check_symbolic_instance(epsilon_den, q, m)

    assert q_unsafe < epsilon_den * m
    assert lower_unsafe > target_unsafe
    assert q_unsafe < qsep(m)

    assert q_safe > epsilon_den * m
    assert m <= target_safe
    assert q_safe > qsep(m)

    n2, k2 = 32, 16
    q_domain2, q2 = 3**8, 3**104
    m2 = comb(n2, k2 + 1)
    target2 = q2 // epsilon_den
    assert [pow(3, d, 32) for d in (1, 2, 4, 8)] == [3, 9, 17, 1]
    assert 104 % 8 == 0 and (q_domain2 - 1) % 32 == 0
    assert q2 < 1 << 256 and q2 > epsilon_den * m2 and q2 > qsep(m2)
    assert adjacent_secant_lower(q2, m2) == m2 <= target2
    check_symbolic_instance(epsilon_den, q2, m2)

    q_below = epsilon_den * m - 1
    q_equal = epsilon_den * m
    assert q_below // epsilon_den == m - 1
    assert q_equal // epsilon_den == m
    assert q_below < epsilon_den * m
    assert not (q_equal < epsilon_den * m)

    tested = scaled_exhaustive()
    print("status=PASS")
    print(f"epsilon_den={epsilon_den}")
    print(f"q_domain=3^32={q_domain}")
    print(f"M=binom(128,65)={m}")
    print(f"q_line_unsafe=3^96={q_unsafe}")
    print(f"B_star_unsafe={target_unsafe}")
    print(f"syndrome_secant_lower={lower_unsafe}")
    print(f"q_line_safe=3^160={q_safe}")
    print(f"B_star_safe={target_safe}")
    print(f"B_MCA_safe(k+1)=M={m}")
    print(f"small_safe_M={m2}")
    print(f"small_safe_B_star={target2}")
    print(f"endpoint_minus_one_unsafe={q_below < epsilon_den*m}")
    print(f"endpoint_equal_unsafe={q_equal < epsilon_den*m}")
    print(f"scaled_exhaustive_instances={tested}")


if __name__ == "__main__":
    main()
