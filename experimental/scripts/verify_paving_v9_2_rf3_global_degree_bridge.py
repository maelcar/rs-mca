#!/usr/bin/env python3
"""Verify the Paving v9.2 RF3'' global-degree bridge packet.

This standard-library checker is an arithmetic and source-binding companion to
``experimental/notes/audits/paving_v9_2_rf3_global_degree_bridge.md``.  It
checks the corrected nonlinear Hensel weight recurrence, both exact defects in
the printed source recurrence, the direct linear-factor recurrence, the
factor/content/common-regular-point ledgers, the incidence and chosen-support
arithmetic, and the four conservative RF3'' row ceilings.

The paper note contains the algebraic-function-field proof.  This program does
not claim to replace that proof or BCIKS Lemma A.1.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import sys
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Callable, Iterable, Iterator, Sequence


ROOT = Path(__file__).resolve().parents[2]
NOTE = (
    ROOT
    / "experimental"
    / "notes"
    / "audits"
    / "paving_v9_2_rf3_global_degree_bridge.md"
)
MAIN_TEX = ROOT / "experimental" / "RS_MCA_Paving_v9.2.tex"
RELEASE_TEX = (
    ROOT
    / "experimental"
    / "RS_MCA_Paving_v9.2_source"
    / "RS_MCA_Paving_v9.2.tex"
)
SOURCE_AUDIT = (
    ROOT
    / "experimental"
    / "scripts"
    / "verify_paving_v9_2_retained_factor_source_audit.py"
)
CONTENT_GUARD = (
    ROOT
    / "experimental"
    / "scripts"
    / "verify_paving_v9_2_retained_factor_content_guard.py"
)

EXPECTED_NOTE_SHA256 = (
    "284b4cb81f308499eb91d5d2470c71c097d2fd36e4bbfebfe2d6432b683e5092"
)
EXPECTED_TEX_SHA256 = (
    "8e89be94dd6291dc5563897e72ae34b49880512cd37f72287b4288ff030cbbc0"
)
EXPECTED_SOURCE_AUDIT_SHA256 = (
    "e33c819a2bb8cb4ce94d831561de51c084505b490bc6d359b59c91e43d513312"
)
EXPECTED_CONTENT_GUARD_SHA256 = (
    "15e5f5e990b98215c89c617e6a6f023cb92cf2a1686414dc43ff9abba3a46097"
)


class VerificationError(RuntimeError):
    """Raised when a fail-closed packet check does not hold."""


class Checks:
    """Count successful semantic checks while retaining useful errors."""

    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            raise VerificationError(message)
        self.count += 1

    def equal(self, left: object, right: object, message: str) -> None:
        self.require(left == right, f"{message}: {left!r} != {right!r}")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def verify_digest(
    checks: Checks, payload: bytes, expected: str, label: str
) -> None:
    checks.equal(sha256_bytes(payload), expected, f"{label} SHA-256 binding")


def verify_note_semantics(checks: Checks, text: str) -> None:
    clauses = (
        ("status", "Status: PROVED"),
        ("integer theorem", "## Integer core theorem"),
        ("integer RF3 bound", "(1+2Ud^2)G+(r+1)d"),
        ("leading-coefficient guard", "both discriminants and\n\\(Y\\)-leading coefficients"),
        ("nonlinear y definition", "y=\\ell-w\\ge1"),
        ("nonlinear chi definition", "\\chi:=g-a+(a-1)y+(a-2)w"),
        ("nonlinear chi identity", "ag-1-(a-1)b-w"),
        ("nonlinear L definition", "L_t=y+(t+1)w+e_t\\chi"),
        ("first defect witness", "H=Y^2+Z^3"),
        ("second defect witness", "R=X+(Y+Z^2)(Y+1)(Y+2)"),
        ("linear recurrence", "N_t&=-B_tA_0^t-"),
        ("factor-pair sum", "\\sum_{i,j}a_i b_{ij}g_i"),
        ("RF3 double-prime corollary", "## 7. RF3'' corollary"),
        ("RF3-prime nonclaim", "does not recover RF3'"),
    )
    for name, needle in clauses:
        checks.require(needle in text, f"bridge note lost its {name}")


ASSUMPTION_START = "\\begin{assumption}[Parameter-retained factor lift]"
ASSUMPTION_END = "\\end{assumption}"


def extract_assumption(text: str) -> str:
    if text.count(ASSUMPTION_START) != 1:
        raise VerificationError("v9.2 assumption start is not unique")
    start = text.index(ASSUMPTION_START)
    try:
        end = text.index(ASSUMPTION_END, start) + len(ASSUMPTION_END)
    except ValueError as exc:
        raise VerificationError("v9.2 assumption end is missing") from exc
    return text[start:end]


def verify_v9_semantics(checks: Checks, text: str) -> None:
    assumption = extract_assumption(text)
    clauses = (
        ("RF1 characteristic guard", "\\operatorname{char}(\\F)>V-1"),
        ("RF2 field-size guard", "q&>2UD_Y"),
        ("RF2 top-incidence guard", "(A-K-1)(2U-1)&>(n-K-1)(2K+1)"),
        ("old immutable RF3 clause", "\\abs S>2U D_Y^2D_Z+(r+1)D_Y"),
        ("chosen-support conclusion", "u_i=v_i"),
        ("degree conclusion", "\\deg v_i<K"),
    )
    for name, needle in clauses:
        checks.require(needle in assumption, f"v9.2 source lost its {name}")


def verify_bindings(checks: Checks) -> None:
    note_bytes = NOTE.read_bytes()
    main_bytes = MAIN_TEX.read_bytes()
    release_bytes = RELEASE_TEX.read_bytes()
    source_audit_bytes = SOURCE_AUDIT.read_bytes()
    content_guard_bytes = CONTENT_GUARD.read_bytes()

    verify_digest(checks, note_bytes, EXPECTED_NOTE_SHA256, "bridge note")
    checks.equal(main_bytes, release_bytes, "the two immutable v9.2 TeX copies")
    verify_digest(checks, main_bytes, EXPECTED_TEX_SHA256, "v9.2 TeX")
    verify_digest(
        checks,
        source_audit_bytes,
        EXPECTED_SOURCE_AUDIT_SHA256,
        "predecessor source audit",
    )
    verify_digest(
        checks,
        content_guard_bytes,
        EXPECTED_CONTENT_GUARD_SHA256,
        "predecessor content guard",
    )
    verify_note_semantics(checks, note_bytes.decode("utf-8"))
    verify_v9_semantics(checks, main_bytes.decode("utf-8"))


# Polynomials in Z over F_p, represented low coefficient first.
ModPoly = tuple[int, ...]


def mod_poly(values: Iterable[int], prime: int) -> ModPoly:
    coefficients = [value % prime for value in values]
    while coefficients and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def mod_add(left: ModPoly, right: ModPoly, prime: int) -> ModPoly:
    size = max(len(left), len(right))
    values = [0] * size
    for index, value in enumerate(left):
        values[index] += value
    for index, value in enumerate(right):
        values[index] += value
    return mod_poly(values, prime)


def mod_mul(left: ModPoly, right: ModPoly, prime: int) -> ModPoly:
    if not left or not right:
        return ()
    values = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            values[left_index + right_index] += left_value * right_value
    return mod_poly(values, prime)


def mod_neg(poly: ModPoly, prime: int) -> ModPoly:
    return mod_poly((-value for value in poly), prime)


def mod_degree(poly: ModPoly) -> int:
    if not poly:
        raise VerificationError("degree requested for the zero polynomial")
    return len(poly) - 1


def verify_base_case_defect_witness(checks: Checks, z_degree: int = 3) -> None:
    # H=Y^2+Z^3 has b=2, global g=3, leading coefficient W=1.
    b = 2
    g = max(2, z_degree)
    w = 0
    ell = g - b + 1
    lambda_t = ell
    printed_lambda_t = w + 1
    checks.equal(z_degree, 3, "base-case witness Z degree")
    checks.equal((b, g, w, ell), (2, 3, 0, 2), "base-case witness parameters")
    checks.require(
        lambda_t != printed_lambda_t,
        "base-case witness no longer refutes Lambda(T)=Lambda(W)+1",
    )
    checks.equal(lambda_t, 2, "base-case witness Lambda(T)")
    checks.equal(printed_lambda_t, 1, "base-case printed Lambda(W)+1")


def verify_derivative_defect_witness(checks: Checks, z_power: int = 2) -> None:
    # Over F_5, at alpha_0=-Z^2 the derivative of
    # (Y+Z^2)(Y+1)(Y+2) is (1-Z^2)(2-Z^2).
    prime = 5
    z_term = mod_poly([0] * z_power + [1], prime)
    alpha = mod_neg(z_term, prime)
    one = mod_poly((1,), prime)
    two = mod_poly((2,), prime)
    f0 = mod_add(alpha, z_term, prime)
    f1 = mod_add(alpha, one, prime)
    f2 = mod_add(alpha, two, prime)
    derivative = mod_add(
        mod_add(mod_mul(f1, f2, prime), mod_mul(f0, f2, prime), prime),
        mod_mul(f0, f1, prime),
        prime,
    )
    g = z_power + 2
    a = 3
    w = 0
    printed_bound = (g - 1) + (a - 2) * w
    checks.equal(z_power, 2, "derivative-defect witness Z power")
    checks.equal(f0, (), "H(alpha_0,Z) vanishes")
    checks.equal(derivative, mod_poly((2, 0, 2, 0, 1), prime), "exact derivative")
    checks.equal(mod_degree(derivative), 4, "derivative-defect degree")
    checks.equal(printed_bound, 3, "printed derivative-numerator bound")
    checks.require(
        mod_degree(derivative) > printed_bound,
        "derivative witness no longer exceeds the printed bound",
    )
    # X+f(Y,Z) is monic linear in X over the integral ring F_5[Y,Z].
    checks.equal((a, g), (3, 4), "derivative-defect global degrees")


def e_index(t: int) -> int:
    return 0 if t == 0 else 2 * t - 1


def multiplicity_vectors(total_weight: int) -> Iterator[tuple[int, ...]]:
    """Yield lambda_1,...,lambda_total with sum s*lambda_s=total."""

    if total_weight == 0:
        yield ()
        return
    values = [0] * total_weight

    def rec(part: int, remaining: int) -> Iterator[tuple[int, ...]]:
        if part > total_weight:
            if remaining == 0:
                yield tuple(values)
            return
        for count in range(remaining // part + 1):
            values[part - 1] = count
            yield from rec(part + 1, remaining - part * count)
        values[part - 1] = 0

    yield from rec(1, total_weight)


def verify_nonlinear_case(
    checks: Checks,
    *,
    a: int,
    b: int,
    g: int,
    w: int,
    max_t: int,
    y_override: int | None = None,
    chi_override: int | None = None,
    l_shift: int = 0,
) -> None:
    checks.require(a >= 2, "nonlinear factor has a<2")
    checks.require(1 <= b <= a, "nonlinear specialized degree is outside 1..a")
    checks.require(g >= a and g >= b, "nonlinear global degree is too small")
    checks.require(0 <= w <= g - b, "nonlinear leading-coefficient degree range")

    ell = g - b + 1
    actual_y = ell - w
    y = actual_y if y_override is None else y_override
    checks.equal(y, actual_y, "nonlinear y identity")
    checks.require(y >= 1, "nonlinear y lost its positive slack")

    actual_chi = g - a + (a - 1) * y + (a - 2) * w
    chi = actual_chi if chi_override is None else chi_override
    checks.equal(chi, actual_chi, "nonlinear chi definition")
    checks.equal(chi, a * g - 1 - (a - 1) * b - w, "nonlinear chi closed form")
    checks.require(chi >= a - 1 > 0, "nonlinear chi positivity")

    def level(t: int) -> int:
        return y + (t + 1) * w + e_index(t) * chi + l_shift

    checks.equal(l_shift, 0, "nonlinear L recurrence shift")
    checks.equal(level(0), ell, "corrected nonlinear base level")

    # Equation (10): reduction by the monicized H does not increase weight.
    for s in range(1, b + 1):
        coefficient_degree = g - b + s
        term_weight = (
            coefficient_degree + (s - 1) * w + (b - s) * ell
        )
        checks.require(term_weight <= b * ell, "monicized-H reduction weight")

    for t in range(max_t + 1):
        l_t = level(t)
        checks.require(l_t < (2 * t + 1) * a * g, "nonlinear coarse L bound")
        if t == 0:
            checks.equal(l_t, ell, "nonlinear t=0 level")
            continue

        envelope = g - a + a * y + (a + t - 1) * w + (2 * t - 2) * chi
        checks.equal(envelope, l_t, "nonlinear recurrence envelope identity")
        difference = (2 * t + 1) * a * g - l_t
        displayed_difference = (
            2 * a * g
            - g
            + b
            - 1
            + (t - 1) * w
            + (2 * t - 1) * (1 + (a - 1) * b)
        )
        checks.equal(difference, displayed_difference, "nonlinear L gap identity")
        checks.require(difference > 0, "nonlinear L gap positivity")

        # Equations (14)--(19), exhaustively over every coefficient partition.
        for i in range(t + 1):
            for lam in multiplicity_vectors(t - i):
                s_lambda = sum(lam)
                if s_lambda > a:
                    continue
                if i == 0 and s_lambda == 1:
                    # The omitted term linear in alpha_t.
                    continue
                delta_i = 1 if i == 0 else 0
                w_exponent = i + delta_i - 1
                xi_exponent = 2 * i + s_lambda - 2
                checks.require(w_exponent >= 0, "nonlinear W exponent")
                checks.require(xi_exponent >= 0, "nonlinear xi exponent")

                for j in range(a - s_lambda + 1):
                    raw_weight = (
                        g
                        - s_lambda
                        - j
                        + j * ell
                        + (a - s_lambda - delta_i - j) * w
                    )
                    b_bound = (
                        g
                        - a
                        + (a - s_lambda) * y
                        + (a - s_lambda - delta_i) * w
                    )
                    checks.require(raw_weight <= b_bound, "nonlinear B coefficient bound")

                b_bound = (
                    g
                    - a
                    + (a - s_lambda) * y
                    + (a - s_lambda - delta_i) * w
                )
                beta_weight = sum(
                    count * level(index + 1)
                    for index, count in enumerate(lam)
                )
                contribution = (
                    w_exponent * w
                    + xi_exponent * chi
                    + b_bound
                    + beta_weight
                )
                checks.require(contribution <= l_t, "nonlinear recurrence contribution")

    pole_cost = w + b * chi
    pair_charge = a * b * g
    pole_gap = pair_charge - pole_cost
    displayed_pole_gap = b + b * b * (a - 1) + (b - 1) * w
    checks.equal(pole_gap, displayed_pole_gap, "nonlinear pole-gap identity")
    checks.require(pole_gap > 0, "nonlinear pole deletion is not below abg")


def verify_nonlinear_recurrence(checks: Checks) -> int:
    cases = 0
    for a in range(2, 7):
        for b in range(1, a + 1):
            for g in range(a, a + 5):
                if g < b:
                    continue
                for w in range(g - b + 1):
                    verify_nonlinear_case(
                        checks, a=a, b=b, g=g, w=w, max_t=6
                    )
                    cases += 1
    checks.equal(cases, 475, "nonlinear exhaustive case count")
    return cases


def verify_linear_case(
    checks: Checks,
    *,
    g: int,
    max_t: int,
    target_shift: int = 0,
) -> None:
    checks.require(g >= 1, "linear global degree is not positive")
    bounds = [g]
    checks.equal(bounds[0], g, "linear N_0 degree bound")
    for t in range(1, max_t + 1):
        first_term = g + t * (g - 1)
        summands = [
            (g - 1) + bounds[t - s] + (s - 1) * (g - 1)
            for s in range(1, t + 1)
        ]
        recurrence_bound = max([first_term, *summands])
        target = (t + 1) * g - t + target_shift
        checks.equal(recurrence_bound, target, "linear numerator recurrence bound")
        checks.require(target <= (2 * t + 1) * g, "linear coarse numerator bound")
        bounds.append(recurrence_bound)

    checks.require(g - 1 < g, "linear leading-coefficient pole charge")
    for k in range(1, max_t + 2):
        coordinate_bound = k * g - k + 1
        checks.require(
            coordinate_bound <= (2 * k - 1) * g,
            "linear coordinate numerator bound",
        )


def verify_linear_recurrence(checks: Checks) -> int:
    cases = 0
    for g in range(1, 17):
        verify_linear_case(checks, g=g, max_t=64)
        cases += 1
    return cases


@dataclass(frozen=True)
class Factor:
    a: int
    delta: int
    g: int
    multiplicity: int
    parts: tuple[int, ...]
    specialization_content: int


def verify_factor_ledger(
    checks: Checks,
    *,
    factors: Sequence[Factor],
    k: int,
    u: int,
    r: int,
    delta_content: int,
    z_content: int,
    q: int,
    content_coefficient: int = 1,
) -> dict[str, int]:
    checks.require(k >= 1 and u >= 1 and r >= 0, "factor ledger base parameters")
    checks.require(delta_content >= 0 and z_content >= 0, "global content degrees")
    for factor in factors:
        checks.require(factor.a >= 1, "factor Y-degree is not positive")
        checks.require(factor.delta >= k * factor.a, "factor weighted degree too small")
        checks.require(factor.g >= factor.a, "factor global YZ-degree too small")
        checks.require(factor.multiplicity >= 1, "factor multiplicity is not positive")
        checks.require(bool(factor.parts), "factor has no specialization parts")
        checks.require(all(part >= 1 for part in factor.parts), "nonpositive b_ij")
        checks.equal(sum(factor.parts), factor.a, "specialization degrees sum to a_i")
        checks.require(
            0 <= factor.specialization_content <= factor.g,
            "specialization content exceeds global factor degree",
        )

    d = sum(factor.multiplicity * factor.a for factor in factors)
    e = delta_content + sum(
        factor.multiplicity * factor.delta for factor in factors
    )
    global_degree = z_content + sum(
        factor.multiplicity * factor.g for factor in factors
    )
    checks.require(d >= 1, "positive-Y factor ledger is empty")
    checks.require(e <= u - 1, "global X/Y weighted degree exceeds U-1")
    checks.require(q > 2 * u * d, "common-point field-size guard")

    regular_exact = delta_content + sum(
        (2 * factor.a - 1) * factor.delta - k * factor.a * factor.a
        for factor in factors
    )
    regular_without_savings = delta_content + sum(
        (2 * factor.a - 1) * factor.delta for factor in factors
    )
    distinct_delta = delta_content + sum(factor.delta for factor in factors)
    checks.require(regular_exact <= regular_without_savings, "regular-point exact bound")
    checks.require(
        regular_without_savings <= 2 * d * distinct_delta,
        "regular-point factor sum",
    )
    checks.require(distinct_delta <= e, "distinct weighted degrees exceed E")
    checks.require(2 * d * e <= 2 * d * (u - 1), "regular-point E bound")
    checks.require(2 * d * (u - 1) < 2 * u * d < q, "regular-point root count")

    content_degree = z_content + sum(
        factor.specialization_content for factor in factors
    )
    checks.require(content_degree <= global_degree, "content root ledger exceeds G")

    pair_sum = sum(
        factor.a * part * factor.g
        for factor in factors
        for part in factor.parts
    )
    collapsed_pair_sum = sum(factor.a * factor.a * factor.g for factor in factors)
    checks.equal(pair_sum, collapsed_pair_sum, "factor-pair collapse")
    distinct_g = sum(factor.g for factor in factors)
    checks.require(distinct_g <= global_degree, "distinct global degrees exceed G")
    checks.require(pair_sum <= d * d * distinct_g, "factor-pair d^2 sum")
    checks.require(pair_sum <= d * d * global_degree, "factor-pair global bound")

    pair_count = sum(len(factor.parts) for factor in factors)
    checks.require(pair_count <= sum(factor.a for factor in factors), "factor-pair count")
    checks.require(pair_count <= d, "factor-pair count exceeds d")

    exceptional = (
        content_degree
        + 2 * u * pair_sum
        + (r + 1) * pair_count
    )
    rf3_double_prime = (
        content_coefficient + 2 * u * d * d
    ) * global_degree + (r + 1) * d
    checks.equal(content_coefficient, 1, "RF3'' content coefficient")
    checks.require(exceptional <= rf3_double_prime, "RF3'' aggregate bound")
    return {
        "d": d,
        "E": e,
        "G": global_degree,
        "regular": regular_exact,
        "content": content_degree,
        "pair_sum": pair_sum,
        "pairs": pair_count,
        "exceptional": exceptional,
        "rf3_double_prime": rf3_double_prime,
    }


def compositions(total: int) -> tuple[tuple[int, ...], ...]:
    if total <= 0:
        return ()
    result: list[tuple[int, ...]] = []

    def rec(remaining: int, prefix: tuple[int, ...]) -> None:
        if remaining == 0:
            result.append(prefix)
            return
        for value in range(1, remaining + 1):
            rec(remaining - value, prefix + (value,))

    rec(total, ())
    return tuple(result)


def weak_compositions(total: int, length: int) -> Iterator[tuple[int, ...]]:
    if length == 0:
        if total == 0:
            yield ()
        return
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in weak_compositions(total - first, length - 1):
            yield (first, *tail)


def verify_aggregate_partition(
    checks: Checks,
    a_values: tuple[int, ...],
    g_values: tuple[int, ...],
    part_values: tuple[tuple[int, ...], ...],
) -> None:
    d = sum(a_values)
    global_degree = sum(g_values)
    pair_sum = sum(
        a * b * g
        for a, g, parts in zip(a_values, g_values, part_values)
        for b in parts
    )
    checks.equal(pair_sum, sum(a * a * g for a, g in zip(a_values, g_values)),
                 "exhaustive factor-pair collapse")
    checks.require(pair_sum <= d * d * global_degree, "exhaustive d^2G bound")
    checks.require(sum(map(len, part_values)) <= d, "exhaustive pair-count bound")


def verify_factor_ledgers(checks: Checks) -> tuple[int, dict[str, int]]:
    sample = (
        Factor(1, 2, 3, 2, (1,), 2),
        Factor(2, 5, 4, 1, (1, 1), 1),
    )
    sample_result = verify_factor_ledger(
        checks,
        factors=sample,
        k=2,
        u=10,
        r=3,
        delta_content=0,
        z_content=1,
        q=83,
    )

    cases = 0
    for d in range(1, 6):
        for a_values in compositions(d):
            length = len(a_values)
            for extra in range(3):
                for g_extra in weak_compositions(extra, length):
                    g_values = tuple(
                        a + addition for a, addition in zip(a_values, g_extra)
                    )
                    choices = [compositions(a) for a in a_values]
                    for part_values in itertools.product(*choices):
                        verify_aggregate_partition(
                            checks, a_values, g_values, part_values
                        )
                        cases += 1
    checks.require(cases >= 500, "factor-partition exhaustive case count is too small")
    return cases, sample_result


def verify_leading_coefficient_witness(
    checks: Checks, *, include_leading_coefficient: bool = True
) -> None:
    # R=XY+1 at x_0=0 is linear in Y.  Its discriminant is 1, but its
    # Y-leading coefficient X vanishes at x_0, so Y-degree drops to zero.
    x0 = 0
    discriminant_at_x0 = 1
    leading_coefficient_at_x0 = x0
    checks.equal(discriminant_at_x0, 1, "linear discriminant witness")
    checks.equal(leading_coefficient_at_x0, 0, "linear leading coefficient witness")
    checks.require(
        include_leading_coefficient,
        "regular-point guard omitted the Y-leading coefficient",
    )
    checks.require(
        discriminant_at_x0 != 0 and leading_coefficient_at_x0 == 0,
        "linear witness does not separate discriminant from leading coefficient",
    )


def verify_v9_top_implication(checks: Checks) -> int:
    cases = 0
    for n in range(4, 31):
        for k in range(1, n - 1):
            for agreement in range(k + 2, n + 1):
                for u in range(1, 31):
                    v9_left = (agreement - k - 1) * (2 * u - 1)
                    v9_right = (n - k - 1) * (2 * k + 1)
                    if v9_left <= v9_right:
                        continue
                    exact_left = (agreement - k) * (2 * u - 1)
                    exact_right = (n - k) * (2 * k - 1)
                    checks.require(
                        exact_left > exact_right,
                        "printed top guard does not imply exact top guard",
                    )
                    cases += 1
    checks.require(cases > 1000, "top-guard implication case count is too small")
    return cases


def verify_incidence_instance(
    checks: Checks,
    *,
    n: int,
    agreement: int,
    k: int,
    u: int,
    charge: int,
    survivors: int,
) -> None:
    r = n - agreement
    checks.require(1 <= k and k + 2 <= agreement <= n, "incidence dimensions")
    checks.require(charge > 0, "incidence pair charge is not positive")
    checks.require(
        (agreement - k) * (2 * u - 1) > (n - k) * (2 * k - 1),
        "exact top-incidence guard",
    )
    checks.require(
        survivors > (2 * u - 1) * charge + (r + 1),
        "survivor count lost its strict r+1 allowance",
    )
    checks.require(
        (agreement - k) * survivors
        > (n - k) * (2 * k - 1) * charge,
        "top-K incidence does not clear the coordinate charge",
    )


def verify_chosen_support_rule(checks: Checks, margin: int = 1) -> int:
    counterexamples = 0
    tested = 0
    for r in range(0, 41):
        for slopes in range(1, 101):
            if slopes <= r + margin:
                continue
            for bad_points in range(0, 101):
                if bad_points * (slopes - 1) > r * slopes:
                    continue
                tested += 1
                if bad_points > r:
                    counterexamples += 1
    checks.equal(margin, 1, "chosen-support strict margin")
    checks.equal(counterexamples, 0, "chosen-support integer lemma")
    checks.require(tested > 1000, "chosen-support case count is too small")
    return tested


def verify_affine_slope_uniqueness(checks: Checks) -> int:
    cases = 0
    for prime in (2, 3, 5, 7, 11):
        for delta_0 in range(prime):
            for delta_1 in range(prime):
                if delta_0 == 0 and delta_1 == 0:
                    continue
                roots = [
                    slope
                    for slope in range(prime)
                    if (delta_0 + slope * delta_1) % prime == 0
                ]
                checks.require(len(roots) <= 1, "one bad point serves two slopes")
                cases += 1
    return cases


def verify_incidence_and_support(checks: Checks) -> tuple[int, int, int]:
    top_cases = verify_v9_top_implication(checks)
    verify_incidence_instance(
        checks,
        n=10,
        agreement=8,
        k=2,
        u=5,
        charge=3,
        survivors=31,
    )
    chosen_cases = verify_chosen_support_rule(checks)
    affine_cases = verify_affine_slope_uniqueness(checks)
    return top_cases, chosen_cases, affine_cases


@dataclass(frozen=True)
class RetainedRow:
    rate_denominator: int
    radius: int
    u: int
    v: int
    w: int
    expected_ceiling: int


ROWS = (
    RetainedRow(2, 611982, 176735230, 169, 27525, 274589064742753629),
    RetainedRow(4, 1045433, 109378776, 209, 29028, 274721012201293956),
    RetainedRow(8, 1352390, 67028580, 256, 31500, 274578888391562205),
    RetainedRow(16, 1569744, 41137824, 314, 34101, 274861787390263486),
)


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def verify_rows(
    checks: Checks,
    rows: Sequence[RetainedRow] = ROWS,
) -> tuple[int, ...]:
    p = (1 << 31) - (1 << 24) + 1
    q = p**6
    epsilon = Fraction(1, 1 << 64)
    budget = q // (1 << 128)
    checks.equal(budget, 274980728111395087, "KoalaBear RF3'' budget")
    ceilings: list[int] = []
    for row in rows:
        dy = Fraction(row.v - 1) + epsilon
        dz = Fraction(row.w - 1) + epsilon
        threshold = (
            (1 + 2 * row.u * dy * dy) * dz
            + (row.radius + 1) * dy
        )
        ceiling = ceil_fraction(threshold)
        checks.equal(ceiling, row.expected_ceiling, "RF3'' row ceiling")
        checks.require(ceiling <= budget, "RF3'' row exceeds budget")
        ceilings.append(ceiling)
    return tuple(ceilings)


def load_module(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise VerificationError(f"cannot load predecessor module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_predecessor_replay(checks: Checks) -> dict[str, int]:
    module = load_module(SOURCE_AUDIT, "paving_v9_2_source_audit_dependency")
    obstruction = module.verify_obstruction(module.PINNED_OBSTRUCTION)
    expected_obstruction = {
        "content_degree": 2,
        "h_yz_degree": 1,
        "alpha_numerator_degree": 3,
        "alpha_denominator_degree": 2,
        "global_yz_degree": 3,
    }
    checks.equal(obstruction, expected_obstruction, "global-degree defect replay")
    checks.require(
        obstruction["alpha_numerator_degree"]
        > obstruction["h_yz_degree"],
        "specialized content-free degree was incorrectly accepted",
    )
    predecessor_rows = tuple(module.verify_rows())
    checks.equal(
        predecessor_rows,
        tuple(row.expected_ceiling for row in ROWS),
        "predecessor RF3'' row replay",
    )
    module.verify_source_bindings()
    checks.require(True, "predecessor immutable source replay")
    return obstruction


def verify_all(checks: Checks) -> dict[str, object]:
    verify_bindings(checks)
    verify_base_case_defect_witness(checks)
    verify_derivative_defect_witness(checks)
    nonlinear_cases = verify_nonlinear_recurrence(checks)
    linear_cases = verify_linear_recurrence(checks)
    factor_cases, sample_factor = verify_factor_ledgers(checks)
    verify_leading_coefficient_witness(checks)
    incidence_counts = verify_incidence_and_support(checks)
    ceilings = verify_rows(checks)
    obstruction = verify_predecessor_replay(checks)
    return {
        "nonlinear_cases": nonlinear_cases,
        "linear_cases": linear_cases,
        "factor_cases": factor_cases,
        "sample_factor": sample_factor,
        "incidence_counts": incidence_counts,
        "ceilings": ceilings,
        "obstruction": obstruction,
    }


def expect_rejected(
    name: str,
    expected_reason: str,
    action: Callable[[Checks], object],
) -> None:
    try:
        action(Checks())
    except VerificationError as exc:
        if expected_reason not in str(exc):
            raise VerificationError(
                f"tamper {name} failed for the wrong reason: {exc}"
            ) from exc
    else:
        raise VerificationError(f"tamper accepted: {name}")


def run_tamper_selftest() -> int:
    note_text = NOTE.read_text(encoding="utf-8")
    source_text = MAIN_TEX.read_text(encoding="utf-8")
    sample = (
        Factor(1, 2, 3, 2, (1,), 2),
        Factor(2, 5, 4, 1, (1, 1), 1),
    )
    mutations: tuple[tuple[str, str, Callable[[Checks], object]], ...] = (
        (
            "note-status",
            "status",
            lambda c: verify_note_semantics(
                c, note_text.replace("Status: PROVED", "Status: AUDIT", 1)
            ),
        ),
        (
            "source-RF3",
            "old immutable RF3 clause",
            lambda c: verify_v9_semantics(
                c,
                source_text.replace(
                    "\\abs S>2U D_Y^2D_Z+(r+1)D_Y",
                    "\\abs S>(1+2U D_Y^2)D_Z+(r+1)D_Y",
                    1,
                ),
            ),
        ),
        (
            "note-digest",
            "bridge note SHA-256",
            lambda c: verify_digest(
                c,
                NOTE.read_bytes() + b"tamper",
                EXPECTED_NOTE_SHA256,
                "bridge note",
            ),
        ),
        (
            "base-case-defect",
            "base-case witness Z degree",
            lambda c: verify_base_case_defect_witness(c, z_degree=2),
        ),
        (
            "derivative-defect",
            "derivative-defect witness Z power",
            lambda c: verify_derivative_defect_witness(c, z_power=1),
        ),
        (
            "nonlinear-y",
            "nonlinear y identity",
            lambda c: verify_nonlinear_case(
                c, a=3, b=1, g=4, w=0, max_t=3, y_override=3
            ),
        ),
        (
            "nonlinear-chi",
            "nonlinear chi definition",
            lambda c: verify_nonlinear_case(
                c, a=3, b=1, g=4, w=0, max_t=3, chi_override=10
            ),
        ),
        (
            "nonlinear-L",
            "nonlinear L recurrence shift",
            lambda c: verify_nonlinear_case(
                c, a=3, b=1, g=4, w=0, max_t=3, l_shift=1
            ),
        ),
        (
            "linear-recurrence",
            "linear numerator recurrence bound",
            lambda c: verify_linear_case(c, g=3, max_t=5, target_shift=-1),
        ),
        (
            "specialization-parts",
            "specialization degrees sum",
            lambda c: verify_factor_ledger(
                c,
                factors=(replace(sample[0], parts=(1, 1)), sample[1]),
                k=2,
                u=10,
                r=3,
                delta_content=0,
                z_content=1,
                q=83,
            ),
        ),
        (
            "specialization-content",
            "specialization content exceeds",
            lambda c: verify_factor_ledger(
                c,
                factors=(replace(sample[0], specialization_content=4), sample[1]),
                k=2,
                u=10,
                r=3,
                delta_content=0,
                z_content=1,
                q=83,
            ),
        ),
        (
            "leading-coefficient",
            "omitted the Y-leading coefficient",
            lambda c: verify_leading_coefficient_witness(
                c, include_leading_coefficient=False
            ),
        ),
        (
            "incidence-off-by-one",
            "survivor count lost",
            lambda c: verify_incidence_instance(
                c,
                n=10,
                agreement=8,
                k=2,
                u=5,
                charge=3,
                survivors=30,
            ),
        ),
        (
            "chosen-support-margin",
            "chosen-support strict margin",
            lambda c: verify_chosen_support_rule(c, margin=0),
        ),
        (
            "RF3-content-coefficient",
            "RF3'' content coefficient",
            lambda c: verify_factor_ledger(
                c,
                factors=sample,
                k=2,
                u=10,
                r=3,
                delta_content=0,
                z_content=1,
                q=83,
                content_coefficient=0,
            ),
        ),
        (
            "row-ceiling",
            "RF3'' row ceiling",
            lambda c: verify_rows(
                c,
                (replace(ROWS[0], expected_ceiling=ROWS[0].expected_ceiling + 1),
                 *ROWS[1:]),
            ),
        ),
    )
    for name, reason, action in mutations:
        expect_rejected(name, reason, action)
    return len(mutations)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        rejected = run_tamper_selftest()
        print(
            "PAVING_V9_2_RF3_GLOBAL_DEGREE_BRIDGE_TAMPER_PASS "
            f"rejected={rejected}/{rejected}"
        )
        return 0

    checks = Checks()
    summary = verify_all(checks)
    print("PAVING_V9_2_RF3_GLOBAL_DEGREE_BRIDGE_PASS")
    print(
        "recurrences: nonlinear_cases=%d linear_cases=%d; "
        "factor_partitions=%d"
        % (
            summary["nonlinear_cases"],
            summary["linear_cases"],
            summary["factor_cases"],
        )
    )
    print(
        "source defects: Lambda(T)=2 != Lambda(W)+1=1; "
        "derivative_degree=4 > printed_bound=3; "
        "specialized/global lift degrees=1/3"
    )
    print("RF3'': ceilings=%s" % (summary["ceilings"],))
    print(f"semantic_checks={checks.count}")
    print(
        "NOTE: the algebraic-function-field proof is in the bound note; "
        "this verifier checks its exact arithmetic and bindings."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
