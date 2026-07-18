#!/usr/bin/env python3
"""Exact source audit for the Paving v9.2 retained-factor lift.

This standard-library checker has two independent jobs:

* verify the local Hensel-degree obstruction
  R(X,Y,Z) = Z^2 Y + X(Z^3+1) at x_0=0; and
* evaluate the conservative global-degree envelope
  (1+2 U D_Y^2)D_Z+(r+1)D_Y on all four v9.2 rows.

The checker source-binds the immutable v9.2 assumption.  It does not prove
the retained-factor lift or promote any conditional row.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[2]
MAIN_TEX = ROOT / "experimental" / "RS_MCA_Paving_v9.2.tex"
RELEASE_TEX = (
    ROOT
    / "experimental"
    / "RS_MCA_Paving_v9.2_source"
    / "RS_MCA_Paving_v9.2.tex"
)
EXPECTED_TEX_SHA256 = (
    "8e89be94dd6291dc5563897e72ae34b49880512cd37f72287b4288ff030cbbc0"
)
EXPECTED_ASSUMPTION_SHA256 = (
    "06bd786e80d385e13e71a7197a50763fbc8c795deb668f1734183e52df1dab1d"
)


class VerificationError(RuntimeError):
    """Raised when an exact audit condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


# Univariate polynomials in Z, represented by low-to-high rational
# coefficients.  The zero polynomial is the empty tuple.
ZPoly = tuple[Fraction, ...]


def zpoly(values: tuple[int | Fraction, ...] | list[int | Fraction]) -> ZPoly:
    coefficients = [Fraction(value) for value in values]
    while coefficients and coefficients[-1] == 0:
        coefficients.pop()
    return tuple(coefficients)


def z_add(left: ZPoly, right: ZPoly) -> ZPoly:
    length = max(len(left), len(right))
    values = [Fraction(0) for _ in range(length)]
    for index, value in enumerate(left):
        values[index] += value
    for index, value in enumerate(right):
        values[index] += value
    return zpoly(values)


def z_neg(poly: ZPoly) -> ZPoly:
    return zpoly([-value for value in poly])


def z_mul(left: ZPoly, right: ZPoly) -> ZPoly:
    if not left or not right:
        return ()
    values = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            values[left_index + right_index] += left_value * right_value
    return zpoly(values)


def zpoly_degree(poly: ZPoly) -> int:
    require(bool(poly), "degree requested for the zero Z-polynomial")
    return len(poly) - 1


def z_divmod(numerator: ZPoly, denominator: ZPoly) -> tuple[ZPoly, ZPoly]:
    require(bool(denominator), "division by the zero Z-polynomial")
    remainder = list(numerator)
    quotient = [
        Fraction(0)
        for _ in range(max(0, len(numerator) - len(denominator) + 1))
    ]
    denominator_degree = len(denominator) - 1
    denominator_lead = denominator[-1]
    while remainder and len(remainder) - 1 >= denominator_degree:
        shift = len(remainder) - 1 - denominator_degree
        factor = remainder[-1] / denominator_lead
        quotient[shift] += factor
        for index, value in enumerate(denominator):
            remainder[index + shift] -= factor * value
        remainder = list(zpoly(remainder))
    return zpoly(quotient), zpoly(remainder)


def z_monic(poly: ZPoly) -> ZPoly:
    require(bool(poly), "cannot normalize the zero Z-polynomial")
    return zpoly([value / poly[-1] for value in poly])


def z_gcd(left: ZPoly, right: ZPoly) -> ZPoly:
    while right:
        _quotient, remainder = z_divmod(left, right)
        left, right = right, remainder
    return z_monic(left)


def z_exact_div(numerator: ZPoly, denominator: ZPoly) -> ZPoly:
    quotient, remainder = z_divmod(numerator, denominator)
    require(not remainder, "claimed exact Z-polynomial division has a remainder")
    return quotient


@dataclass(frozen=True)
class Term:
    coefficient: Fraction
    x_degree: int
    y_degree: int
    z_degree: int


@dataclass(frozen=True)
class ObstructionCase:
    terms: tuple[Term, ...]
    x0: int


PINNED_OBSTRUCTION = ObstructionCase(
    terms=(
        Term(Fraction(1), 0, 1, 2),  # Z^2 Y
        Term(Fraction(1), 1, 0, 3),  # X Z^3
        Term(Fraction(1), 1, 0, 0),  # X
    ),
    x0=0,
)


def normalized_terms(case: ObstructionCase) -> dict[tuple[int, int, int], Fraction]:
    result: dict[tuple[int, int, int], Fraction] = {}
    for term in case.terms:
        require(
            term.x_degree >= 0 and term.y_degree >= 0 and term.z_degree >= 0,
            "a polynomial exponent is negative",
        )
        key = (term.x_degree, term.y_degree, term.z_degree)
        result[key] = result.get(key, Fraction(0)) + term.coefficient
    return {key: value for key, value in result.items() if value != 0}


def z_coefficient(
    terms: dict[tuple[int, int, int], Fraction],
    x_degree: int,
    y_degree: int,
) -> ZPoly:
    maximum = max(
        (
            z_degree
            for (current_x, current_y, z_degree) in terms
            if current_x == x_degree and current_y == y_degree
        ),
        default=-1,
    )
    if maximum < 0:
        return ()
    values = [Fraction(0) for _ in range(maximum + 1)]
    for (current_x, current_y, z_degree), coefficient in terms.items():
        if current_x == x_degree and current_y == y_degree:
            values[z_degree] += coefficient
    return zpoly(values)


def verify_obstruction(case: ObstructionCase) -> dict[str, int]:
    require(case.x0 == 0, "the Hensel base point is not x_0=0")
    terms = normalized_terms(case)
    require(bool(terms), "R is the zero polynomial")

    # R is linear in Y and its Y-derivative Z^2 is nonzero.  Therefore it is
    # separable over Q(X,Z), and a root lift is unique whenever it exists.
    y_degree = max(y_degree for _x, y_degree, _z in terms)
    require(y_degree == 1, "R is not linear-separable in Y")
    derivative: dict[tuple[int, int, int], Fraction] = {}
    for (x_degree, current_y, z_degree), coefficient in terms.items():
        if current_y > 0:
            key = (x_degree, current_y - 1, z_degree)
            derivative[key] = derivative.get(key, Fraction(0)) + (
                coefficient * current_y
            )
    derivative = {key: value for key, value in derivative.items() if value != 0}
    require(bool(derivative), "R is not separable in Y")

    # At X=0 the specialization is Z^2 Y.  Its scalar Z-content is Z^2,
    # and division by that content leaves H=Y of total (Y,Z)-degree one.
    specialized = {
        (current_y, z_degree): coefficient
        for (x_degree, current_y, z_degree), coefficient in terms.items()
        if x_degree == 0
    }
    require(
        specialized == {(1, 2): Fraction(1)},
        "the specialization content is not Z^2 with content-free H=Y",
    )
    content_degree = 2
    content_free = {
        (current_y, z_degree - content_degree): coefficient
        for (current_y, z_degree), coefficient in specialized.items()
    }
    require(content_free == {(1, 0): Fraction(1)}, "content-free H is not Y")
    h_yz_degree = max(
        current_y + z_degree for current_y, z_degree in content_free
    )
    require(h_yz_degree == 1, "content-free H does not have (Y,Z)-degree one")

    # Regard R as a polynomial in Y over Q[X,Z].  Its Y-coefficient is the
    # monomial Z^2.  Hence any common divisor of its Y-coefficients must be a
    # power of Z.  The constant coefficient has a nonzero Z^0 term, so the
    # global polynomial is primitive.
    y_coefficient = z_coefficient(terms, 0, 1)
    x_coefficient = z_coefficient(terms, 1, 0)
    require(y_coefficient == zpoly((0, 0, 1)), "the Y-coefficient is not Z^2")
    require(bool(x_coefficient), "the X-linear constant coefficient vanished")
    require(x_coefficient[0] != 0, "R has a nontrivial common Z-content")
    require(z_gcd(y_coefficient, x_coefficient) == zpoly((1,)), "R is not primitive")

    # Solving the unique linear lift Y=alpha_1(Z)X gives
    # alpha_1=-(Z^3+1)/Z^2.  All arithmetic below is in Q(Z), with the
    # fraction reduced by an exact Euclidean gcd.
    common = z_gcd(y_coefficient, x_coefficient)
    alpha_numerator = z_exact_div(z_neg(x_coefficient), common)
    alpha_denominator = z_exact_div(y_coefficient, common)
    require(
        z_add(
            z_mul(y_coefficient, alpha_numerator),
            z_mul(x_coefficient, alpha_denominator),
        )
        == (),
        "the claimed alpha_1 does not solve R(X,alpha_1 X,Z)=0",
    )
    require(
        alpha_numerator == zpoly((-1, 0, 0, -1)),
        "alpha_1 numerator is not -(Z^3+1)",
    )
    require(alpha_denominator == zpoly((0, 0, 1)), "alpha_1 denominator is not Z^2")
    numerator_degree = zpoly_degree(alpha_numerator)
    denominator_degree = zpoly_degree(alpha_denominator)
    require(numerator_degree == 3, "alpha_1 numerator degree is not three")
    require(denominator_degree == 2, "alpha_1 denominator degree is not two")

    global_yz_degree = max(
        current_y + z_degree for _x, current_y, z_degree in terms
    )
    require(global_yz_degree == 3, "R does not have global (Y,Z)-degree three")
    require(
        numerator_degree > h_yz_degree,
        "the lift does not obstruct replacing global D by specialized H-degree",
    )
    require(
        terms
        == {
            (0, 1, 2): Fraction(1),
            (1, 0, 3): Fraction(1),
            (1, 0, 0): Fraction(1),
        },
        "the pinned polynomial is not R=Z^2Y+X(Z^3+1)",
    )

    return {
        "content_degree": content_degree,
        "h_yz_degree": h_yz_degree,
        "alpha_numerator_degree": numerator_degree,
        "alpha_denominator_degree": denominator_degree,
        "global_yz_degree": global_yz_degree,
    }


@dataclass(frozen=True)
class RetainedRow:
    rate_denominator: int
    radius: int
    multiplicity: int
    u_count: int
    v_count: int
    w_count: int
    expected_rf3_double_prime: int


ROWS = (
    RetainedRow(2, 611982, 119, 176735230, 169, 27525, 274589064742753629),
    RetainedRow(4, 1045433, 104, 109378776, 209, 29028, 274721012201293956),
    RetainedRow(8, 1352390, 90, 67028580, 256, 31500, 274578888391562205),
    RetainedRow(16, 1569744, 78, 41137824, 314, 34101, 274861787390263486),
)


def verify_rows(
    rows: tuple[RetainedRow, ...] = ROWS,
    budget_override: int | None = None,
) -> tuple[int, ...]:
    p = (1 << 31) - (1 << 24) + 1
    q = p**6
    n = 1 << 21
    tiny = Fraction(1, 1 << 64)
    budget = q // (1 << 128) if budget_override is None else budget_override
    require(budget > 0, "the row budget is not positive")
    if budget_override is None:
        require(budget == 274980728111395087, "KoalaBear budget changed")

    results: list[int] = []
    for row in rows:
        agreement = n - row.radius
        dy = Fraction(row.v_count - 1) + tiny
        dz = Fraction(row.w_count - 1) + tiny
        require(
            row.u_count == row.multiplicity * agreement,
            "v9.2 row no longer has U=mA",
        )
        alpha = 2 * row.u_count * dy * dy
        require(alpha > 1, "a deployed row left the alpha>1 regime")
        old_rf3 = alpha * dz + (row.radius + 1) * dy
        rf3_double_prime = (1 + alpha) * dz + (row.radius + 1) * dy
        require(rf3_double_prime == old_rf3 + dz, "RF3'' ledger identity failed")
        ceiling = ceil_fraction(rf3_double_prime)
        require(
            ceiling == row.expected_rf3_double_prime,
            "a conservative RF3'' ceiling changed",
        )
        require(ceiling <= budget, "a conservative RF3'' ceiling exceeds budget")
        results.append(ceiling)
    return tuple(results)


ASSUMPTION_START = b"\\begin{assumption}[Parameter-retained factor lift]"
ASSUMPTION_END = b"\\end{assumption}\n"


def extract_assumption(source: bytes) -> bytes:
    require(source.count(ASSUMPTION_START) == 1, "assumption start is not unique")
    start = source.index(ASSUMPTION_START)
    require(source.count(ASSUMPTION_END, start) >= 1, "assumption end is missing")
    end = source.index(ASSUMPTION_END, start) + len(ASSUMPTION_END)
    return source[start:end]


def verify_assumption_semantics(assumption: str) -> None:
    clauses = (
        ("assumption label", r"\label{ass:retained-factor-lift}"),
        ("RF1 ceiling order", r"V&\ge m,\quad W\ge V,\quad U>K(V-1)"),
        ("RF1 degree guard", r"D_X&<mA,\qquad \operatorname{char}(\F)>V-1"),
        ("RF2 top-degree guard", r"(A-K-1)(2U-1)&>(n-K-1)(2K+1)"),
        ("RF2 field-size guard", r"q&>2UD_Y"),
        ("weighted-degree premise", r"\((1,K,0)\)-weighted degree less than \(D_X\)"),
        ("Y-degree premise", r"\(Y\)-degree less"),
        ("YZ-degree premise", r"\((0,1,1)\)-weighted degree less than \(D_Z\)"),
        ("root premise", r"Q(X,P_\gamma(X),\gamma)=0"),
        ("chosen-support premise", r"A_\gamma\subseteq D"),
        ("RF3 clause", r"\abs S>2U D_Y^2D_Z+(r+1)D_Y"),
        ("simultaneous conclusion", r"u_i=v_i"),
        ("degree conclusion", r"\deg v_i<K"),
    )
    for name, needle in clauses:
        require(needle in assumption, f"v9.2 assumption lost its {name}")


def verify_source_bytes(main_source: bytes, release_source: bytes) -> None:
    require(main_source == release_source, "the two v9.2 TeX copies differ")
    require(
        hashlib.sha256(main_source).hexdigest() == EXPECTED_TEX_SHA256,
        "v9.2 TeX SHA-256 binding changed",
    )
    assumption = extract_assumption(main_source)
    require(
        hashlib.sha256(assumption).hexdigest() == EXPECTED_ASSUMPTION_SHA256,
        "v9.2 assumption-block SHA-256 binding changed",
    )
    assumption_text = assumption.decode("utf-8")
    verify_assumption_semantics(assumption_text)

    full_text = main_source.decode("utf-8")
    for row in ROWS:
        rate = f"1/{row.rate_denominator}"
        parameter_row = (
            f"{rate}&{row.radius}&{row.multiplicity}&"
            f"{row.u_count}&{row.v_count}&{row.w_count}"
        )
        require(parameter_row in full_text, f"v9.2 RF6 row is not bound: {rate}")
    require(
        r"\floor{q2^{-128}}=274980728111395087" in full_text,
        "v9.2 printed KoalaBear budget is not bound",
    )


def verify_source_bindings() -> None:
    verify_source_bytes(MAIN_TEX.read_bytes(), RELEASE_TEX.read_bytes())


def expect_rejected(action: Callable[[], object], reason: str, name: str) -> None:
    try:
        action()
    except VerificationError as exc:
        require(reason in str(exc), f"tamper {name} failed for the wrong reason: {exc}")
    else:
        raise VerificationError(f"tamper accepted: {name}")


def replace_obstruction_term(index: int, **changes: object) -> ObstructionCase:
    terms = list(PINNED_OBSTRUCTION.terms)
    terms[index] = replace(terms[index], **changes)
    return replace(PINNED_OBSTRUCTION, terms=tuple(terms))


def run_tamper_selftest() -> int:
    rejected = 0
    cases = (
        (
            "specialized-content",
            lambda: verify_obstruction(replace_obstruction_term(0, z_degree=1)),
            "specialization content",
        ),
        (
            "global-content",
            lambda: verify_obstruction(
                replace(
                    PINNED_OBSTRUCTION,
                    terms=(
                        PINNED_OBSTRUCTION.terms[0],
                        Term(Fraction(1), 1, 0, 4),
                        Term(Fraction(1), 1, 0, 1),
                    ),
                )
            ),
            "common Z-content",
        ),
        (
            "lift-numerator-degree",
            lambda: verify_obstruction(replace_obstruction_term(1, z_degree=1)),
            "alpha_1 numerator",
        ),
        (
            "nonlinear-Y",
            lambda: verify_obstruction(replace_obstruction_term(0, y_degree=2)),
            "linear-separable",
        ),
        (
            "base-point",
            lambda: verify_obstruction(replace(PINNED_OBSTRUCTION, x0=1)),
            "base point",
        ),
    )
    for name, action, reason in cases:
        expect_rejected(action, reason, name)
        rejected += 1

    source = MAIN_TEX.read_bytes()
    assumption_text = extract_assumption(source).decode("utf-8")
    changed_rf3 = assumption_text.replace(
        r"\abs S>2U D_Y^2D_Z+(r+1)D_Y",
        r"\abs S>(1+2U D_Y^2)D_Z+(r+1)D_Y",
        1,
    )
    expect_rejected(
        lambda: verify_assumption_semantics(changed_rf3),
        "RF3 clause",
        "source-RF3",
    )
    rejected += 1
    changed_conclusion = assumption_text.replace(r"\deg v_i<K", r"\deg v_i\le K", 1)
    expect_rejected(
        lambda: verify_assumption_semantics(changed_conclusion),
        "degree conclusion",
        "source-conclusion",
    )
    rejected += 1

    changed_row = replace(ROWS[0], expected_rf3_double_prime=ROWS[0].expected_rf3_double_prime + 1)
    expect_rejected(
        lambda: verify_rows((changed_row,) + ROWS[1:]),
        "RF3'' ceiling changed",
        "row-ceiling",
    )
    rejected += 1
    expect_rejected(
        lambda: verify_rows(ROWS, budget_override=ROWS[0].expected_rf3_double_prime - 1),
        "exceeds budget",
        "row-budget",
    )
    rejected += 1
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.tamper_selftest:
        rejected = run_tamper_selftest()
        print(
            "PAVING_V9_2_RETAINED_FACTOR_SOURCE_AUDIT_TAMPER_PASS "
            f"rejected={rejected}/{rejected}"
        )
        return 0

    obstruction = verify_obstruction(PINNED_OBSTRUCTION)
    ceilings = verify_rows()
    verify_source_bindings()
    print("PAVING_V9_2_RETAINED_FACTOR_SOURCE_AUDIT_PASS")
    print(
        "local obstruction: content=Z^%d; H-degree=%d; "
        "alpha_1 numerator/denominator degrees=%d/%d; global degree=%d"
        % (
            obstruction["content_degree"],
            obstruction["h_yz_degree"],
            obstruction["alpha_numerator_degree"],
            obstruction["alpha_denominator_degree"],
            obstruction["global_yz_degree"],
        )
    )
    print("RF3'': ceilings=%s; all 4 remain under 274980728111395087" % (ceilings,))
    print(
        "NOTE: specialized content-free degree is not a drop-in replacement "
        "for BCIKS Claim A.2's global degree."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
