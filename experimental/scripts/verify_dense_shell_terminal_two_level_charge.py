#!/usr/bin/env python3
"""Independent stdlib replay for the dense-shell terminal charge theorem."""

from __future__ import annotations

import argparse
import subprocess
import sys
from itertools import product
from math import cos, pi


FAILED: list[str] = []
PASSED = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASSED
    if ok:
        PASSED += 1
    else:
        FAILED.append(name)
    suffix = f" ({detail})" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def scan_states(word: tuple[int, ...]) -> list[float]:
    u = 0.0
    out = []
    for digit in word:
        u = (digit + u) / 3.0
        out.append(u)
    return out


def q_of(u: float) -> float:
    return -0.5 * cos(2.0 * pi * u)


def a_of(u: float) -> float:
    return q_of(u) + 0.5


def multiply_root(coeffs: list[float], a: float) -> list[float]:
    """Multiply by x-a in the shifted-Chebyshev basis T_j(2x-1)."""
    out = [0.0] * (len(coeffs) + 1)
    for j, coeff in enumerate(coeffs):
        if j == 0:
            out[0] += 0.5 * coeff
            out[1] += 0.5 * coeff
        else:
            out[j - 1] += 0.25 * coeff
            out[j] += 0.5 * coeff
            out[j + 1] += 0.25 * coeff
        out[j] -= a * coeff
    return out


def prefix_beta(word: tuple[int, ...], parity_tamper: bool = False) -> list[float]:
    coeffs = [1.0]
    for state in scan_states(word):
        coeffs = multiply_root(coeffs, a_of(state))
    degree = len(word) + (1 if parity_tamper else 0)
    return [((-1.0) ** (degree - j)) * value for j, value in enumerate(coeffs)]


def suffix_h(u: float, h2_tamper: bool = False) -> tuple[float, float, float]:
    raw = [0.0, 0.0, 0.0]
    for d, e in product((-1.0, 1.0), repeat=2):
        v = (d + u) / 3.0
        w = (e + v) / 3.0
        p = q_of(v)
        r = q_of(w)
        weight = p * r
        raw[0] += weight * (0.125 + p * r)
        raw[1] += weight * (-(p + r) / 2.0)
        raw[2] += weight * 0.125
    h = (raw[0], -raw[1], raw[2])
    if h2_tamper:
        h = (h[0], h[1], -h[2])
    return h


def closed_h12(u: float) -> tuple[float, float]:
    theta = 2.0 * pi * u / 9.0
    A = cos(pi / 9.0)
    C = cos(2.0 * pi / 9.0)
    D = cos(4.0 * pi / 9.0)
    h2 = (A * cos(4.0 * theta) - D * cos(2.0 * theta)) / 32.0
    h1 = (
        3.0 * C * cos(theta) / 32.0
        + cos(3.0 * theta) / 16.0
        - A * cos(5.0 * theta) / 16.0
        + D * cos(7.0 * theta) / 32.0
    )
    return h1, h2


def terminal_charge(word: tuple[int, ...], **tamper: bool) -> tuple[float, float]:
    beta = prefix_beta(word, parity_tamper=tamper.get("prefix_parity", False))
    incoming = scan_states(word)[-1] if word else 0.0
    h = suffix_h(incoming, h2_tamper=tamper.get("h2_sign", False))
    value = 0.0
    for j in range(min(len(beta), 3)):
        norm = 1.0 if j == 0 else 0.5
        value += norm * beta[j] * h[j]
    return value, beta[0]


def hatf_middle(word: tuple[int, ...]) -> float:
    poly = [1.0]
    for state in scan_states(word):
        t = 2.0 * cos(2.0 * pi * state)
        nxt = [0.0] * (len(poly) + 2)
        for j, value in enumerate(poly):
            nxt[j] += value
            nxt[j + 1] += value * t
            nxt[j + 2] += value
        poly = nxt
    return poly[len(word)]


def root_anchor_gap(B: int, anchor_tamper: bool = False) -> float:
    lhs = 0.0
    rhs = 0.0
    root_factor = 0.2 if anchor_tamper else 0.25
    for word in product((-1, 1), repeat=B):
        states = scan_states(word)
        q_terminal = q_of(states[-2]) * q_of(states[-1])
        weight = abs(hatf_middle(word)) / (4.0**B)
        lhs += weight * q_of(states[0]) * q_terminal
        rhs += root_factor * weight * q_terminal
    return lhs - rhs


def run(tamper: str | None = None) -> bool:
    A = cos(pi / 9.0)
    C = cos(2.0 * pi / 9.0)
    D = cos(4.0 * pi / 9.0)
    m2 = D * (A - C) / 32.0
    h1_lower = (6.0 * A - 5.0) / 128.0
    check("analytic constant A > 5/6", A > 5.0 / 6.0, f"A={A:.15f}")
    check("identity A*C = 1/4 + A/2", abs(A * C - (0.25 + 0.5 * A)) < 2e-15)
    check("terminal h2 lower bound m2 is positive", m2 > 9.4e-4, f"m2={m2:.15e}")
    check("terminal h1 coarse lower bound is positive", h1_lower > 0.0, f"lower={h1_lower:.15e}")

    max_formula_error = 0.0
    minima = [float("inf"), float("inf"), float("inf")]
    h0_minus_h2 = float("inf")
    samples = 100_001
    for index in range(samples):
        u = -0.5 + index / (samples - 1)
        h0, h1, h2 = suffix_h(u, h2_tamper=(tamper == "h2-sign"))
        closed1, closed2 = closed_h12(u)
        max_formula_error = max(max_formula_error, abs(h1 - closed1), abs(abs(h2) - closed2))
        minima[0] = min(minima[0], h0)
        minima[1] = min(minima[1], h1)
        minima[2] = min(minima[2], h2)
        h0_minus_h2 = min(h0_minus_h2, h0 - h2)
    check("direct suffix coefficients match closed h1/h2 formulas", max_formula_error < 3e-15, f"max_error={max_formula_error:.3e}")
    check("all three suffix coefficients are positive", min(minima) > 0.0, "minima=" + ",".join(f"{x:.15e}" for x in minima))
    check("h0 strictly exceeds h2", h0_minus_h2 > 0.0, f"min_gap={h0_minus_h2:.15e}")
    check("observed h2 minimum equals m2", abs(minima[2] - m2) < 3e-15)

    cone_min = float("inf")
    charge_min = float("inf")
    bound_ratio = float("inf")
    prefix_count = 0
    for B in range(2, 17):
        for word in product((-1, 1), repeat=B - 2):
            prefix_count += 1
            value, beta0 = terminal_charge(
                word,
                h2_sign=(tamper == "h2-sign"),
                prefix_parity=(tamper == "prefix-parity"),
            )
            beta = prefix_beta(word, parity_tamper=(tamper == "prefix-parity"))
            cone_min = min(cone_min, min(beta))
            charge_min = min(charge_min, value)
            bound_ratio = min(bound_ratio, value / (beta0 * m2))
    check("prefix alternating cone through B=16", cone_min >= -2e-14, f"min_beta={cone_min:.3e}")
    check("terminal two-level charges positive through B=16", charge_min > 0.0, f"min_charge={charge_min:.15e}")
    check("strict beta0*m2 lower bound through B=16", bound_ratio > 1.0, f"min_ratio={bound_ratio:.12f}")
    check("all finite prefixes enumerated", prefix_count == 32_767, f"count={prefix_count}")

    root_gap = max(abs(root_anchor_gap(B, anchor_tamper=(tamper == "root-anchor"))) for B in range(3, 11))
    check("root-anchor deletion factor q1=1/4 through B=10", root_gap < 2e-13, f"max_gap={root_gap:.3e}")

    total = PASSED + len(FAILED)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} ({PASSED}/{total})")
    return not FAILED


def tamper_selftest() -> bool:
    caught = 0
    tampers = ("h2-sign", "prefix-parity", "root-anchor")
    for tamper in tampers:
        result = subprocess.run(
            [sys.executable, __file__, "--tamper", tamper],
            capture_output=True,
            text=True,
            check=False,
        )
        detected = result.returncode != 0 and "RESULT: FAIL" in result.stdout
        caught += int(detected)
        print(f"tamper {tamper}: {'caught' if detected else 'MISSED'}")
    print(f"TAMPER SELFTEST: {caught}/{len(tampers)} caught")
    return caught == len(tampers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper", choices=("h2-sign", "prefix-parity", "root-anchor"))
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return 0 if tamper_selftest() else 1
    return 0 if run(args.tamper) else 1


if __name__ == "__main__":
    raise SystemExit(main())
