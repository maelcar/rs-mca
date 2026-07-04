#!/usr/bin/env python3
"""Exact integer checks for the identity-scale frontier upgrade.

Certified comparisons use integer arithmetic only.  For the c=1 deployed rows,
large binomials are built once from prime exponents and nearby rows are obtained
by exact ratio updates.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math

n = 2**21
k = 2**20
p_kb = 2**31 - 2**24 + 1
p_m31 = 2**31 - 1
q_kb = p_kb**6
q_m31 = p_m31**4


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(limit + 1) if sieve[p]]


primes = primes_upto(n)


def vp_factorial(N: int, p: int) -> int:
    ans = 0
    while N:
        N //= p
        ans += N
    return ans


def binom_prime(N: int, m: int) -> int:
    m = min(m, N - m)
    factors = []
    for p in primes:
        if p > N:
            break
        e = vp_factorial(N, p) - vp_factorial(m, p) - vp_factorial(N - m, p)
        if e:
            factors.append(pow(p, e))
    return math.prod(factors)


@dataclass(frozen=True)
class Check:
    name: str
    pbase: int
    K: int
    threshold_num: int
    threshold_den: int
    c: int
    m: int
    edge: Fraction


def binom_table(N: int, ms: list[int]) -> dict[int, int]:
    lo, hi = min(ms), max(ms)
    val = binom_prime(N, lo)
    out = {lo: val}
    for t in range(lo, hi):
        val = val * (N - t) // (t + 1)
        out[t + 1] = val
    return out


def run_group(c: int, checks: list[Check]) -> None:
    N = n // c
    # Need m and m+1 for adjacent fail.
    ms = sorted({chk.m for chk in checks} | {chk.m + 1 for chk in checks})
    binoms = binom_table(N, ms)
    for chk in checks:
        ceil_K_c = (chk.K + c - 1) // c
        w = chk.m - ceil_K_c
        lhs = binoms[chk.m] * chk.threshold_den
        rhs = pow(chk.pbase, w) * chk.threshold_num
        assert lhs > rhs, f"{chk.name}: m does not pass"
        lhs_next = binoms[chk.m + 1] * chk.threshold_den
        rhs_next = rhs * chk.pbase
        assert lhs_next <= rhs_next, f"{chk.name}: m+1 still passes"
        edge = Fraction(n - chk.m * c, n)
        assert edge == chk.edge, f"{chk.name}: edge mismatch {edge} != {chk.edge}"
        print(
            f"PASS {chk.name:18s} c={c:<2d} m={chk.m:<8d} "
            f"w={w:<6d} Delta={chk.m*c-k:<6d} edge={edge}",
            flush=True,
        )


def main() -> None:
    checks = [
        Check("KB MCA identity", p_kb, k + 1, q_kb + k, k, 1, 1116043, Fraction(981109, 2097152)),
        Check("KB list identity", p_kb, k, q_kb, 2**128, 1, 1116046, Fraction(490553, 1048576)),
        Check("M31 MCA identity", p_m31, k + 1, q_m31 + k, k, 1, 1116021, Fraction(981131, 2097152)),
        Check("M31 list identity", p_m31, k, q_m31, 2**100, 1, 1116022, Fraction(490565, 1048576)),
        Check("KB MCA c=2", p_kb, k + 1, q_kb + k, k, 2, 558019, Fraction(490557, 1048576)),
        Check("KB list c=2", p_kb, k, q_kb, 2**128, 2, 558022, Fraction(245277, 524288)),
        Check("M31 MCA c=2", p_m31, k + 1, q_m31 + k, k, 2, 558009, Fraction(490567, 1048576)),
        Check("M31 list c=2", p_m31, k, q_m31, 2**100, 2, 558010, Fraction(245283, 524288)),
        Check("KB MCA old c=16", p_kb, k + 1, q_kb + k, k, 16, 69748, Fraction(15331, 32768)),
        Check("KB list old c=32", p_kb, k, q_kb, 2**128, 32, 34874, Fraction(15331, 32768)),
        Check("M31 MCA old c=32", p_m31, k + 1, q_m31 + k, k, 32, 34873, Fraction(30663, 65536)),
        Check("M31 list old c=32", p_m31, k, q_m31, 2**100, 32, 34874, Fraction(15331, 32768)),
    ]
    for c in sorted(set(chk.c for chk in checks)):
        run_group(c, [chk for chk in checks if chk.c == c])
    print("All exact frontier checks passed.")


if __name__ == "__main__":
    main()
