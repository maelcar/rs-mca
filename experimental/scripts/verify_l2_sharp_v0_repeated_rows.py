#!/usr/bin/env python3
"""Verify the inequality controls in the L2-Sharp V0 counterexample.

Standard library only. The script does not search for the averaged received
word: the exact expectation proves that a word attaining at least the mean
exists. It checks that mean and the reserve/right-hand-side estimates used in
the proof note.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Row:
    s: int
    n: int
    sigma: int
    a: int
    rate: float
    log2_average_lower: float
    average_exponent_per_n: float
    v0_reserve_ratio: float
    one_row_reserve_ratio: float
    random_term_log2_upper: int
    max_active_quotient_size: int
    quotient_log2_envelope: float


def parameters(s: int) -> tuple[int, int, int, int, int]:
    q = 1 << s
    n = q - 1
    k = n // 2
    sigma = math.ceil(3 * n / (4 * s))
    a = k + sigma
    return q, n, k, sigma, a


def log2_binom(n: int, a: int) -> float:
    return (
        math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1)
    ) / math.log(2.0)


def divisors(n: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return small + list(reversed(large))


def exact_average_exceeds_power(s: int, exponent: int) -> bool:
    """Check E L(V) > 2^exponent by exact integer arithmetic."""
    q, n, _, sigma, a = parameters(s)
    numerator = math.comb(n, a) * (q - 1) ** (n - a)
    denominator = q ** (sigma + n - a)
    return numerator > (1 << exponent) * denominator


def check_row(s: int) -> Row:
    q, n, k, sigma, a = parameters(s)
    binom_log = log2_binom(n, a)
    average_log = (
        binom_log
        - s * sigma
        + (n - a) * math.log2(1.0 - 1.0 / q)
    )

    active = [m for m in divisors(n) if sigma < m <= a]
    quotient_sizes = [n // m - 1 for m in active]
    max_q = max(quotient_sizes, default=0)
    q_envelope_log = math.log2(n) + 2 * max_q

    # Exact coarse inequalities used in the note.
    assert 10 * s * sigma >= 6 * n  # 2s sigma >= (6/5)n.
    assert 4 * s * sigma >= 3 * n  # 2s sigma >= (3/2)n.
    assert n - 2 * s * sigma <= -n / 2
    assert q <= n * n
    assert 0.49 <= k / n <= 0.51
    assert k <= a < n
    assert sigma >= 0.5 * n / math.log2(n)
    assert sigma >= 0.5 * n / math.log(n)
    assert all(3 * quotient_size < 4 * s for quotient_size in quotient_sizes)

    # n * 4^Q <= n * q^(8/3), verified without fractional powers.
    envelope = n * (4**max_q)
    assert envelope**3 <= n**3 * q**8

    return Row(
        s=s,
        n=n,
        sigma=sigma,
        a=a,
        rate=k / n,
        log2_average_lower=average_log,
        average_exponent_per_n=average_log / n,
        v0_reserve_ratio=2 * s * sigma / binom_log,
        one_row_reserve_ratio=s * sigma / binom_log,
        random_term_log2_upper=n - 2 * s * sigma,
        max_active_quotient_size=max_q,
        quotient_log2_envelope=q_envelope_log,
    )


def main() -> int:
    sample_s = [8, 10, 12, 14, 16, 18, 20]
    rows = [check_row(s) for s in sample_s]

    # Representative exact finite checks of the averaging lower bound.
    exact_checks = []
    for s in [8, 10, 12, 14]:
        _, n, _, _, _ = parameters(s)
        exponent = n // 8
        ok = exact_average_exceeds_power(s, exponent)
        assert ok
        exact_checks.append({"s": s, "n": n, "lower_power": exponent, "ok": ok})

    # The displayed family approaches exponent 1/4 and has only 3/4 of the
    # entropy payment available in the repeated-row (one-row) stratum.
    assert rows[-1].average_exponent_per_n > 0.24
    assert rows[-1].v0_reserve_ratio > 1.2
    assert rows[-1].one_row_reserve_ratio < 0.8
    assert all(row.random_term_log2_upper <= -row.n / 2 for row in rows)

    result = {
        "status": "PASS",
        "construction": "q=2^s, n=q-1, k=floor(n/2), sigma=ceil(3n/(4s))",
        "exact_average_checks": exact_checks,
        "rows": [asdict(row) for row in rows],
        "interpretation": {
            "left_side": "one-row mean and repeated-row list are exponential",
            "v0_random_term": "at most 2^(-n/2)",
            "quotient_envelope": "at most n*q^(8/3)=O(n^(11/3))",
            "effective_reserve": "sigma*log2(q), not mu*sigma*log2(q)",
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
