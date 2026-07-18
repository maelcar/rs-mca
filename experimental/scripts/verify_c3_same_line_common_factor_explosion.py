#!/usr/bin/env python3
"""Deterministic verifier for the C3 same-line common-factor route cut.

The verifier uses only the Python standard library.  It checks:

  * the complete depth-one prefix-zero fiber of six-subsets of F_17^*;
  * the antipodal A/-A common-divisor cell decomposition;
  * exact multiplicative-stabilizer and scaled-inversion deletions;
  * exact polynomial gcds of the surviving cells;
  * irreducibility of X^5 + X + 3 over F_17;
  * all 472 pole-line slopes and their exact agreement supports; and
  * the frozen JSON certificate and deliberate tamper regressions.

No file is written.  Exit status zero means every check passed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import combinations
from math import comb, gcd
from pathlib import Path


P = 17
D = tuple(range(1, P))
A = frozenset(range(1, 9))
E = frozenset(range(9, 17))
B = 3
R = 3
M = B + R
W = 1
K = M - W - 1
PREFIX = 0
EXT_DEGREE = 5
MODULUS = (3, 1, 0, 0, 0, 1)  # X^5 + X + 3, low coefficient first
FIELD_SIZE = P**EXT_DEGREE
ALPHA = (0, 1, 0, 0, 0)

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = (
    ROOT
    / "experimental/data/certificates/c3-same-line-common-factor-explosion"
    / "c3_same_line_common_factor_explosion.json"
)
FRONTIERS = ROOT / "experimental/asymptotic_rs_mca_frontiers.tex"
GRANDE_FINALE = ROOT / "experimental/grande_finale.tex"

SOURCE_LABELS = (
    "thm:prefix-to-line-hardness",
    "thm:exact-list-line-bijection",
    "cor:exact-prefix-ray-realization",
    "lem:slope-multiplicity-fixed-support",
    "def:algebraically-planted",
    "prop:planted-payment-repaired",
)

_PASS = 0
_FAILURES: list[str] = []


def check(condition: bool, label: str) -> bool:
    global _PASS
    if condition:
        _PASS += 1
    else:
        _FAILURES.append(label)
    return condition


# ---------------------------------------------------------------------------
# Polynomials over F_17
# ---------------------------------------------------------------------------


def trim(poly: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    out = [x % P for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out or [0])


def poly_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % P
    return trim(out)


def poly_sub(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        ) % P
    return trim(out)


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % P
    return trim(out)


def poly_divmod(
    numerator: tuple[int, ...], denominator: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    numerator = trim(numerator)
    denominator = trim(denominator)
    if denominator == (0,):
        raise ZeroDivisionError("polynomial division by zero")
    if len(numerator) < len(denominator):
        return (0,), numerator
    quotient = [0] * (len(numerator) - len(denominator) + 1)
    remainder = list(numerator)
    inverse_lead = pow(denominator[-1], P - 2, P)
    while len(remainder) >= len(denominator) and any(remainder):
        shift = len(remainder) - len(denominator)
        factor = remainder[-1] * inverse_lead % P
        quotient[shift] = factor
        for index, coefficient in enumerate(denominator):
            remainder[index + shift] = (
                remainder[index + shift] - factor * coefficient
            ) % P
        remainder = list(trim(remainder))
    return trim(quotient), trim(remainder)


def poly_mod(poly: tuple[int, ...], modulus: tuple[int, ...]) -> tuple[int, ...]:
    return poly_divmod(poly, modulus)[1]


def poly_gcd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    left, right = trim(left), trim(right)
    while right != (0,):
        left, right = right, poly_mod(left, right)
    if left == (0,):
        return left
    inverse_lead = pow(left[-1], P - 2, P)
    return trim(tuple(inverse_lead * value % P for value in left))


def poly_powmod(
    base: tuple[int, ...], exponent: int, modulus: tuple[int, ...]
) -> tuple[int, ...]:
    result = (1,)
    base = poly_mod(base, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_mul(result, base), modulus)
        base = poly_mod(poly_mul(base, base), modulus)
        exponent >>= 1
    return result


def locator(support: tuple[int, ...] | frozenset[int]) -> tuple[int, ...]:
    result = (1,)
    for point in sorted(support):
        result = poly_mul(result, ((-point) % P, 1))
    return result


def gcd_all(polynomials: list[tuple[int, ...]]) -> tuple[int, ...]:
    result = polynomials[0]
    for poly in polynomials[1:]:
        result = poly_gcd(result, poly)
    return result


def modulus_is_irreducible() -> bool:
    # Rabin's criterion for prime degree five.
    x_poly = (0, 1)
    first_frobenius = poly_powmod(x_poly, P, MODULUS)
    no_linear_factor = poly_gcd(
        MODULUS, poly_sub(first_frobenius, x_poly)
    ) == (1,)
    final_frobenius = poly_powmod(x_poly, P**EXT_DEGREE, MODULUS)
    return no_linear_factor and final_frobenius == x_poly


# ---------------------------------------------------------------------------
# Arithmetic in F_17[X]/(X^5 + X + 3)
# ---------------------------------------------------------------------------


ZERO = (0, 0, 0, 0, 0)
ONE = (1, 0, 0, 0, 0)


def field(value: int) -> tuple[int, ...]:
    return (value % P, 0, 0, 0, 0)


def fadd(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x + y) % P for x, y in zip(left, right))


def fneg(value: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((-x) % P for x in value)


def fsub(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return fadd(left, fneg(right))


def fmul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (2 * EXT_DEGREE - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % P
    for degree in range(len(out) - 1, EXT_DEGREE - 1, -1):
        coefficient = out[degree] % P
        if coefficient:
            # X^5 = -X - 3.
            out[degree - 4] = (out[degree - 4] - coefficient) % P
            out[degree - 5] = (out[degree - 5] - 3 * coefficient) % P
            out[degree] = 0
    return tuple(value % P for value in out[:EXT_DEGREE])


def fpow(base: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = ONE
    while exponent:
        if exponent & 1:
            result = fmul(result, base)
        base = fmul(base, base)
        exponent >>= 1
    return result


def finv(value: tuple[int, ...]) -> tuple[int, ...]:
    if value == ZERO:
        raise ZeroDivisionError("field inversion of zero")
    return fpow(value, FIELD_SIZE - 2)


def eval_base_poly(poly: tuple[int, ...], value: tuple[int, ...]) -> tuple[int, ...]:
    result = ZERO
    for coefficient in reversed(poly):
        result = fadd(fmul(result, value), field(coefficient))
    return result


def eval_ext_poly(
    poly: tuple[tuple[int, ...], ...], value: tuple[int, ...]
) -> tuple[int, ...]:
    result = ZERO
    for coefficient in reversed(poly):
        result = fadd(fmul(result, value), coefficient)
    return result


def divide_by_x_minus_alpha(
    poly: tuple[tuple[int, ...], ...]
) -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    if len(poly) < 2:
        return tuple(), poly[0] if poly else ZERO
    quotient = [ZERO] * (len(poly) - 1)
    quotient[-1] = poly[-1]
    for degree in range(len(poly) - 2, 0, -1):
        quotient[degree - 1] = fadd(poly[degree], fmul(ALPHA, quotient[degree]))
    remainder = fadd(poly[0], fmul(ALPHA, quotient[0]))
    while quotient and quotient[-1] == ZERO:
        quotient.pop()
    return tuple(quotient), remainder


# ---------------------------------------------------------------------------
# Exact support-symmetry tests
# ---------------------------------------------------------------------------


def periodic(support: tuple[int, ...]) -> bool:
    support_set = frozenset(support)
    return any(
        frozenset((multiplier * point) % P for point in support_set) == support_set
        for multiplier in D
        if multiplier != 1
    )


def scaled_inversion_invariant(support: tuple[int, ...]) -> bool:
    support_set = frozenset(support)
    return any(
        frozenset((scale * pow(point, P - 2, P)) % P for point in support_set)
        == support_set
        for scale in D
    )


def is_coset_root_set(candidate: tuple[int, ...]) -> bool:
    size = len(candidate)
    if (P - 1) % size:
        return False
    subgroup = frozenset(x for x in D if pow(x, size, P) == 1)
    return any(
        frozenset((scale * x) % P for x in subgroup) == frozenset(candidate)
        for scale in D
    )


def is_multiplier_fixed_root_set(candidate: tuple[int, ...]) -> bool:
    candidate_set = frozenset(candidate)
    for exponent in range(P - 1):
        if gcd(exponent, P - 1) != 1:
            continue
        fixed = frozenset(x for x in D if pow(x, exponent, P) == x)
        if fixed == candidate_set:
            return True
    return False


def is_twin_coset_root_set(candidate: tuple[int, ...]) -> bool:
    candidate_set = frozenset(candidate)
    for size in range(1, P):
        if (P - 1) % size:
            continue
        subgroup = frozenset(x for x in D if pow(x, size, P) == 1)
        for scale in D:
            coset = frozenset((scale * x) % P for x in subgroup)
            twin = coset | frozenset(pow(x, P - 2, P) for x in coset)
            if twin == candidate_set:
                return True
    return False


def histogram(cell_map: dict[tuple[int, ...], list[tuple[int, ...]]]) -> dict[str, int]:
    return {
        str(size): count
        for size, count in sorted(Counter(map(len, cell_map.values())).items())
    }


def slope_digest(
    supports: list[tuple[int, ...]], slopes: list[tuple[int, ...]]
) -> str:
    payload = [
        {"support": list(support), "slope": list(slope)}
        for support, slope in zip(supports, slopes)
    ]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def compute() -> tuple[dict[str, object], dict[str, object]]:
    frontiers_text = FRONTIERS.read_text(encoding="utf-8")
    finale_text = GRANDE_FINALE.read_text(encoding="utf-8")
    for label in SOURCE_LABELS:
        check(("\\label{" + label + "}") in frontiers_text, f"source label {label}")
    check("\\label{prop:pole-line}" in finale_text, "source label prop:pole-line")

    all_supports = list(combinations(D, M))
    locators = {support: locator(support) for support in all_supports}
    prefix_counts = Counter(poly[M - 1] for poly in locators.values())
    full_fiber = sorted(
        support for support, poly in locators.items() if poly[M - 1] == PREFIX
    )
    balanced = [
        support
        for support in full_fiber
        if len(frozenset(support) & A) == B
    ]

    check(len(all_supports) == comb(16, 6) == 8008, "complete six-set census")
    check(prefix_counts[PREFIX] == 472, "complete prefix-zero fiber size")
    check(all(prefix_counts[value] == 471 for value in range(1, P)), "all nonzero prefix fibers have size 471")
    check(len(balanced) == 256, "balanced A/E slice size")

    cells: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in balanced:
        candidate = tuple(sorted(frozenset(support) & A))
        cells[candidate].append(support)
    cells = dict(sorted(cells.items()))

    expected_histogram = {"1": 4, "2": 4, "3": 6, "4": 8, "5": 10, "6": 24}
    check(len(cells) == comb(8, 3) == 56, "all 56 antipodal candidate cells occur")
    check(histogram(cells) == expected_histogram, "candidate-cell size distribution")
    check(sum(map(len, cells.values())) == 256, "candidate-cell partition total")
    check(len({support for supports in cells.values() for support in supports}) == 256, "candidate cells are disjoint")

    triple_sums = Counter(sum(candidate) % P for candidate in combinations(sorted(A), B))
    triple_sum_vector = [triple_sums[value] for value in range(P)]
    check(triple_sum_vector == [4, 3, 2, 1, 1, 0, 1, 1, 2, 3, 4, 5, 6, 6, 6, 6, 5], "A triple-sum vector")
    check(all(len(supports) == triple_sums[sum(candidate) % P] for candidate, supports in cells.items()), "cell size equals matching triple-sum multiplicity")

    common_divisor_cells = 0
    exact_gcd_cells = 0
    exact_gcd_slopes = 0
    repeated_cells = 0
    repeated_slopes = 0
    for candidate, supports in cells.items():
        candidate_locator = locator(candidate)
        divisibility = [poly_divmod(locators[support], candidate_locator)[1] == (0,) for support in supports]
        if all(divisibility):
            common_divisor_cells += 1
        cell_gcd = gcd_all([locators[support] for support in supports])
        if cell_gcd == candidate_locator:
            exact_gcd_cells += 1
            exact_gcd_slopes += len(supports)
        if len(supports) >= 2:
            repeated_cells += 1
            repeated_slopes += len(supports)
    check(common_divisor_cells == 56, "Q_T divides every locator in all cells")
    check((repeated_cells, repeated_slopes) == (52, 252), "repeated common-divisor cells")
    check((exact_gcd_cells, exact_gcd_slopes) == (48, 244), "exact whole-cell gcd counts")

    a_count_split = Counter(len(frozenset(support) & A) for support in full_fiber)
    check(dict(a_count_split) == {1: 41, 2: 67, 3: 256, 4: 67, 5: 41}, "full-fiber A-occupancy split")

    after_stabilizer = [support for support in balanced if not periodic(support)]
    after_stabilizer_cells: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in after_stabilizer:
        after_stabilizer_cells[tuple(sorted(frozenset(support) & A))].append(support)
    after_stabilizer_cells = dict(sorted(after_stabilizer_cells.items()))
    check(len(balanced) - len(after_stabilizer) == 56, "exact multiplicative-stabilizer deletion count")
    check((len(after_stabilizer_cells), len(after_stabilizer)) == (52, 200), "post-stabilizer cell and slope counts")
    check(histogram(after_stabilizer_cells) == {"1": 4, "2": 6, "3": 8, "4": 10, "5": 24}, "post-stabilizer cell histogram")

    after_scaled_inversion = [
        support
        for support in after_stabilizer
        if not scaled_inversion_invariant(support)
    ]
    after_scaled_inversion_cells: dict[
        tuple[int, ...], list[tuple[int, ...]]
    ] = defaultdict(list)
    for support in after_scaled_inversion:
        after_scaled_inversion_cells[
            tuple(sorted(frozenset(support) & A))
        ].append(support)
    after_scaled_inversion_cells = dict(sorted(after_scaled_inversion_cells.items()))
    check(len(after_stabilizer) - len(after_scaled_inversion) == 6, "additional scaled-inversion deletion count")
    check((len(after_scaled_inversion_cells), len(after_scaled_inversion)) == (52, 194), "post-symmetry cell and slope counts")
    check(histogram(after_scaled_inversion_cells) == {"1": 4, "2": 6, "3": 10, "4": 12, "5": 20}, "post-symmetry cell histogram")

    post_repeated_cells = sum(
        len(supports) >= 2
        for supports in after_scaled_inversion_cells.values()
    )
    post_repeated_slopes = sum(
        len(supports)
        for supports in after_scaled_inversion_cells.values()
        if len(supports) >= 2
    )
    check(
        (post_repeated_cells, post_repeated_slopes) == (48, 190),
        "post-symmetry repeated common-divisor cells",
    )

    post_exact_cells = 0
    post_exact_slopes = 0
    for candidate, supports in after_scaled_inversion_cells.items():
        candidate_locator = locator(candidate)
        check(all(poly_divmod(locators[support], candidate_locator)[1] == (0,) for support in supports), f"post-routing common divisor {candidate}")
        if gcd_all([locators[support] for support in supports]) == candidate_locator:
            post_exact_cells += 1
            post_exact_slopes += len(supports)
    check((post_exact_cells, post_exact_slopes) == (40, 172), "post-symmetry exact gcd counts")

    candidates = list(cells)
    check(all(not is_coset_root_set(candidate) for candidate in candidates), "all 56 candidates are noncoset")
    check(all(not is_multiplier_fixed_root_set(candidate) for candidate in candidates), "all 56 candidates are not multiplier-fixed root sets")
    check(all(not is_twin_coset_root_set(candidate) for candidate in candidates), "all 56 candidates are not twin-coset root sets")
    check(16 % 3 != 0, "cardinality obstruction 3 does not divide 16")

    check(modulus_is_irreducible(), "Rabin irreducibility of X^5 + X + 3")
    check(fpow(ALPHA, FIELD_SIZE) == ALPHA, "alpha lies in F_(17^5)")
    check(fpow(ALPHA, FIELD_SIZE - 1) == ONE, "alpha is nonzero")
    separation_bound = len(D) + K * comb(len(full_fiber), 2)
    check(FIELD_SIZE > separation_bound, "generic extension separation bound")

    u_poly = (0,) * M + (1,)
    slope_values: list[tuple[int, ...]] = []
    explaining_polynomials: dict[tuple[int, ...], tuple[tuple[int, ...], ...]] = {}
    for support in full_fiber:
        p_support = poly_sub(u_poly, locators[support])
        check(len(p_support) - 1 <= K, f"prefix cancellation degree for {support}")
        gamma = eval_base_poly(p_support, ALPHA)
        slope_values.append(gamma)
        numerator = [field(coefficient) for coefficient in p_support]
        numerator[0] = fsub(numerator[0], gamma)
        quotient, remainder = divide_by_x_minus_alpha(tuple(numerator))
        check(remainder == ZERO, f"pole division remainder for {support}")
        check(len(quotient) <= K, f"explaining polynomial degree for {support}")
        explaining_polynomials[support] = quotient
    check(len(set(slope_values)) == len(full_fiber) == 472, "all complete-fiber slopes are distinct")

    inverse_denominators = {
        point: finv(fsub(field(point), ALPHA)) for point in D
    }
    f_word = {
        point: fmul(field(pow(point, M, P)), inverse_denominators[point])
        for point in D
    }
    g_word = {point: fneg(inverse_denominators[point]) for point in D}
    for support, gamma in zip(full_fiber, slope_values):
        quotient = explaining_polynomials[support]
        agreement = tuple(
            point
            for point in D
            if fadd(f_word[point], fmul(gamma, g_word[point]))
            == eval_ext_poly(quotient, field(point))
        )
        check(agreement == support, f"exact agreement support {support}")
    check(all(fadd(fmul(fsub(field(point), ALPHA), g_word[point]), ONE) == ZERO for point in D), "pole word noncommon identity")

    slope_by_support = dict(zip(full_fiber, slope_values))
    check(len({slope_by_support[support] for support in balanced}) == 256, "balanced slopes distinct")
    check(len({slope_by_support[support] for support in after_scaled_inversion}) == 194, "post-symmetry slopes distinct")

    max_intersection = max(
        len(frozenset(left) & frozenset(right))
        for left, right in combinations(full_fiber, 2)
    )
    saturation_pair = (
        (1, 2, 3, 4, 8, 16),
        (1, 2, 3, 4, 9, 15),
    )
    check(all(support in full_fiber for support in saturation_pair), "Johnson-bound witness pair belongs to fiber")
    check(len(set(saturation_pair[0]) & set(saturation_pair[1])) == 4, "Johnson-bound witness pair intersection")
    check(max_intersection == M - W - 1 == 4, "prefix fiber attains Johnson intersection bound")

    computed: dict[str, object] = {
        "schema": "c3_same_line_common_factor_explosion.v1",
        "parameters": {
            "base_prime": P,
            "domain": list(D),
            "A": sorted(A),
            "E": sorted(E),
            "b": B,
            "r": R,
            "m": M,
            "w": W,
            "k": K,
            "prefix": PREFIX,
            "extension_degree": EXT_DEGREE,
            "extension_modulus_low_first": list(MODULUS),
        },
        "results": {
            "all_six_subsets": len(all_supports),
            "prefix_zero_fiber": len(full_fiber),
            "nonzero_prefix_fiber_each": 471,
            "balanced_supports": len(balanced),
            "candidate_cells": len(cells),
            "candidate_cell_size_histogram": histogram(cells),
            "triple_sum_multiplicity_A": triple_sum_vector,
            "full_fiber_A_occupancy": {str(key): value for key, value in sorted(a_count_split.items())},
            "common_divisor_cells": common_divisor_cells,
            "repeated_common_divisor_cells": repeated_cells,
            "repeated_common_divisor_slopes": repeated_slopes,
            "exact_gcd_cells": exact_gcd_cells,
            "exact_gcd_slopes": exact_gcd_slopes,
            "post_exact_stabilizer_cells": len(after_stabilizer_cells),
            "post_exact_stabilizer_slopes": len(after_stabilizer),
            "post_exact_stabilizer_histogram": histogram(after_stabilizer_cells),
            "post_exact_stabilizer_scaled_inversion_cells": len(after_scaled_inversion_cells),
            "post_exact_stabilizer_scaled_inversion_slopes": len(after_scaled_inversion),
            "post_exact_stabilizer_scaled_inversion_histogram": histogram(after_scaled_inversion_cells),
            "post_exact_stabilizer_scaled_inversion_repeated_common_divisor_cells": post_repeated_cells,
            "post_exact_stabilizer_scaled_inversion_repeated_common_divisor_slopes": post_repeated_slopes,
            "post_exact_stabilizer_scaled_inversion_exact_gcd_cells": post_exact_cells,
            "post_exact_stabilizer_scaled_inversion_exact_gcd_slopes": post_exact_slopes,
            "extension_field_size": FIELD_SIZE,
            "generic_separation_bound": separation_bound,
            "complete_line_bad_slopes": len(set(slope_values)),
            "projection_occupancy_max": 1,
            "max_pairwise_intersection": max_intersection,
            "support_slope_sha256": slope_digest(full_fiber, slope_values),
        },
        "verdict": {
            "status": "COUNTEREXAMPLE",
            "refutes": "actual same-line common factors alone force a subexponential candidate census or a subexponential/identity-scale slope charge",
            "does_not_refute": "the repaired planted-payment criterion with explicit description-entropy, natural-profile, and slope-projection hypotheses",
            "deletion_scope": "exact multiplicative-stabilizer and scaled-inversion support predicates only; no full C1/C2 quotient-remainder claim",
        },
    }

    details: dict[str, object] = {
        "full_fiber": full_fiber,
        "balanced": balanced,
        "after_scaled_inversion": after_scaled_inversion,
        "slopes": slope_values,
    }
    return computed, details


def run_tamper_selftest(computed: dict[str, object], details: dict[str, object]) -> None:
    tampered = json.loads(json.dumps(computed))
    tampered["results"]["prefix_zero_fiber"] += 1
    check(tampered != computed, "tamper: corrupted fiber count is rejected")

    truncated = list(details["balanced"])
    truncated.pop()
    check(len(truncated) != computed["results"]["balanced_supports"], "tamper: dropped balanced support is rejected")

    duplicated_slopes = list(details["slopes"])
    duplicated_slopes[-1] = duplicated_slopes[0]
    check(len(set(duplicated_slopes)) != len(duplicated_slopes), "tamper: duplicated slope is rejected")

    reducible_modulus = (0, 0, 0, 0, 0, 1)
    x_poly = (0, 1)
    check(poly_gcd(reducible_modulus, poly_sub(poly_powmod(x_poly, P, reducible_modulus), x_poly)) != (1,), "tamper: reducible modulus is rejected")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="suppress certificate dump")
    parser.add_argument("--dump-json", action="store_true", help="print recomputed certificate JSON")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    computed, details = compute()
    if args.dump_json:
        print(json.dumps(computed, indent=2, sort_keys=True))
    else:
        try:
            frozen = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            _FAILURES.append(f"certificate load failed: {exc}")
        else:
            check(frozen == computed, "frozen JSON certificate matches recomputation")

    if args.tamper_selftest:
        run_tamper_selftest(computed, details)

    total = _PASS + len(_FAILURES)
    if _FAILURES:
        for failure in _FAILURES:
            print("FAIL:", failure)
        print(f"RESULT: FAIL ({_PASS}/{total})")
        return 1
    print(f"RESULT: PASS ({_PASS}/{total})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
