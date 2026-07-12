#!/usr/bin/env python3
"""Verify the exact low-layer L2 decomposition on small RS instances."""

from __future__ import annotations

import argparse
import itertools
import math


def codewords(q: int, domain: tuple[int, ...], k: int) -> tuple[tuple[int, ...], ...]:
    out = []
    for coeffs in itertools.product(range(q), repeat=k):
        out.append(tuple(sum(coeffs[j] * pow(x, j, q) for j in range(k)) % q
                         for x in domain))
    return tuple(out)


def agreement_mask(word: tuple[int, ...], codeword: tuple[int, ...]) -> int:
    mask = 0
    for i, (u, c) in enumerate(zip(word, codeword)):
        if u == c:
            mask |= 1 << i
    return mask


def profiles(q: int, domain: tuple[int, ...], k: int):
    cws = codewords(q, domain, k)
    rows = tuple(itertools.product(range(q), repeat=len(domain)))
    masks = {
        row: tuple(agreement_mask(row, cw) for cw in cws)
        for row in rows
    }
    return cws, rows, masks


def list_count(masks: tuple[int, ...], threshold: int) -> int:
    return sum(mask.bit_count() >= threshold for mask in masks)


def check_instance(q: int = 5, k: int = 2) -> dict[str, int]:
    domain = tuple(range(1, q))
    n = len(domain)
    _, rows, masks_by_row = profiles(q, domain, k)
    pair_checks = 0
    shell_checks = 0
    theorem_checks = 0
    compiler_checks = 0

    for s in range(k, n + 1):
        tau = 2 * s - k + 1
        row_data = {}
        for row in rows:
            masks = masks_by_row[row]
            row_data[row] = (
                masks,
                list_count(masks, s),
                list_count(masks, tau),
            )

        for v in rows:
            v_masks, l_s_v, l_tau_v = row_data[v]
            for w in rows:
                w_masks, l_s_w, _ = row_data[w]
                high = tuple(mask for mask in w_masks if mask.bit_count() >= tau)
                delta_sum = 0
                doubly_high = 0
                shell_sum = 0

                for b_mask in high:
                    r = n - b_mask.bit_count()
                    delta = 0
                    gamma = 0
                    for a_mask in v_masks:
                        total = a_mask.bit_count()
                        if (a_mask & b_mask).bit_count() >= s:
                            gamma += 1
                            if s <= total <= s + r - 1:
                                delta += 1
                                if total >= tau:
                                    doubly_high += 1
                    shell = list_count(v_masks, s + r)
                    assert gamma == shell + delta
                    shell_checks += 1
                    delta_sum += delta
                    shell_sum += max(shell - 1, 0)

                assert delta_sum <= l_s_v - l_tau_v + doubly_high
                theorem_checks += 1

                literal = sum(
                    (a_mask & b_mask).bit_count() >= s
                    for a_mask in v_masks
                    for b_mask in w_masks
                )
                rhs = l_s_w + shell_sum + (l_s_v - l_tau_v) + doubly_high
                assert literal <= rhs
                compiler_checks += 1
                pair_checks += 1

    return {
        "rows": len(rows),
        "pair_checks": pair_checks,
        "shell_checks": shell_checks,
        "theorem_checks": theorem_checks,
        "compiler_checks": compiler_checks,
    }


def check_unit_anchor(q: int = 7, k: int = 3) -> int:
    domain = tuple(range(1, q))
    n = len(domain)
    cws = codewords(q, domain, k)
    checked = 0
    for x_index in range(n):
        unit = tuple(1 if i == x_index else 0 for i in range(n))
        agreements = sorted(
            sum(a == b for a, b in zip(unit, cw))
            for cw in cws
        )
        assert agreements[-1] == n - 1
        assert agreements[-2] <= k
        checked += len(cws)
    return checked


def check_asymptotic_arithmetic() -> int:
    primes = (101, 1009, 10007, 100003, 1000003)
    previous_ratio = -1.0
    checks = 0
    for q in primes:
        n = q - 1
        h = math.log2(q)
        sigma = math.ceil(3 * n / (4 * h))
        k = n // 2
        a = k + sigma
        tau = k + 2 * sigma + 1
        assert k < a < tau <= n - 1
        assert 3 * n / 4 <= h * sigma <= 3 * n / 4 + h

        log_binom = (
            math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1)
        ) / math.log(2)
        log_expectation = (
            log_binom - sigma * h + (n - a) * math.log2(1 - 1 / q)
        )
        ratio = log_expectation / n
        assert ratio > previous_ratio
        previous_ratio = ratio

        assert n / sigma < 4 * h / 3
        assert n / (2 * sigma + 1) < 2 * h / 3
        assert n - 2 * h * sigma <= -n / 2
        checks += 8
    assert previous_ratio > 0.245
    return checks + 1


def tamper_selftest() -> int:
    # The low one-row layer is load-bearing. Omitting it leaves only R_hh and
    # fails already on a four-coordinate exact RS instance.
    q, k, s = 5, 2, 2
    domain = tuple(range(1, q))
    _, rows, masks_by_row = profiles(q, domain, k)
    tau = 2 * s - k + 1
    for v in rows:
        v_masks = masks_by_row[v]
        for w in rows:
            high = tuple(m for m in masks_by_row[w] if m.bit_count() >= tau)
            delta_sum = 0
            doubly_high = 0
            for b_mask in high:
                r = len(domain) - b_mask.bit_count()
                for a_mask in v_masks:
                    total = a_mask.bit_count()
                    if ((a_mask & b_mask).bit_count() >= s and
                            s <= total <= s + r - 1):
                        delta_sum += 1
                        if total >= tau:
                            doubly_high += 1
            if delta_sum > doubly_high:
                return 1
    raise AssertionError("omitted low layer was not rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        print(f"tamper rejections: {tamper_selftest()}")
        print("RESULT: PASS (omitted low layer rejected)")
        return

    counts = check_instance()
    counts["unit_anchor_checks"] = check_unit_anchor()
    counts["asymptotic_checks"] = check_asymptotic_arithmetic()
    for key, value in counts.items():
        print(f"{key}: {value}")
    print("RESULT: PASS (exact low layer and four-term compiler verified)")


if __name__ == "__main__":
    main()
