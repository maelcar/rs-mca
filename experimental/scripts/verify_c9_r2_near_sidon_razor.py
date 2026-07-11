#!/usr/bin/env python3
"""Certify the literal R=2 two-moment near-Sidon razor counterexample.

The construction is an exact degree-two Prouhet upgrade of the block-trade
pattern in avdeevvadim's PR #444.  It works for the unrestricted quantitative
interface with

    Phi(S) = (sum_{t in S} t, sum_{t in S} t^2)

on a full fixed-weight slice.  It does *not* claim that the constructed domain
is a smooth multiplicative/circle domain or that the fiber survives a formally
specified primitive first-match deletion.

The verifier is stdlib-only.  It independently enumerates the 64 local
subsets, the full k=1,2,3 slices, two additive-energy routes, the realized
image, the local image polynomial, bounded log-concavity checks, the
subexponential-image cap, and the full-cube countergate to a fixed c<1 energy
lower bound.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import re
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


STATUS = "COUNTEREXAMPLE_NEW_FLOOR"
SCHEMA = "c9_r2_near_sidon_razor.v1"
BASE_SHA = "e190193cebced1d3752d068a1c24136bc69a85d9"
ARTIFACT = Path(
    "experimental/data/certificates/c9-r2-near-sidon-razor/"
    "c9_r2_near_sidon_razor.json"
)
FRONTIERS_TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
FRONTIERS_LABELS = (
    "def:admissible-sequence",
    "def:primitive-first-match-residual",
    "def:sidon-heavy",
    "def:sidon-paid-cell",
    "eq:exact-power-sum-map",
    "eq:image-ambient-scales",
    "eq:full-image-certificate",
    "def:primitive-q",
    "prop:high-energy-impossible",
    "hyp:ray-compiler",
    "thm:intro-sidon-heavy-repair",
    "thm:primitive-q",
)

# The shift keeps every field locator nonzero.  BASE separates the ordinary
# first-moment digits, while BASE^2 separates the second-moment digits.
SHIFT = 20
BASE = 1000
OFFSETS = (0, 1, 2, 4, 5, 6)
LEFT = (0, 4, 5)
RIGHT = (1, 2, 6)
EXPECTED_LOCAL_POLYNOMIAL = (1, 6, 15, 19, 15, 6, 1)
EXACT_K = (1, 2, 3)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def pin_frontiers_labels(root: Path) -> dict[str, Any]:
    path = root / FRONTIERS_TEX
    if not path.is_file():
        return {
            "path": str(FRONTIERS_TEX).replace("\\", "/"),
            "labels": {label: {"found": False} for label in FRONTIERS_LABELS},
            "all_found": False,
        }
    lines = path.read_text(encoding="utf-8").splitlines()
    pins: dict[str, Any] = {}
    for label in FRONTIERS_LABELS:
        pattern = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}")
        matches = [i for i, line in enumerate(lines, 1) if pattern.search(line)]
        pins[label] = {
            "found": len(matches) == 1,
            "line": matches[0] if len(matches) == 1 else None,
            "paste": lines[matches[0] - 1].strip() if len(matches) == 1 else None,
        }
    return {
        "path": str(FRONTIERS_TEX).replace("\\", "/"),
        "labels": pins,
        "all_found": all(pin["found"] for pin in pins.values()),
    }


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(obj)
    out.pop("payload_sha256", None)
    return out


def payload_hash(obj: dict[str, Any]) -> str:
    raw = json.dumps(
        without_hash(obj), sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def polynomial_product(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def polynomial_power(a: list[int], k: int) -> list[int]:
    out = [1]
    for _ in range(k):
        out = polynomial_product(out, a)
    return out


def log_concavity_margins(a: list[int]) -> list[int]:
    return [a[i] * a[i] - a[i - 1] * a[i + 1] for i in range(1, len(a) - 1)]


def is_prime_64(n: int) -> bool:
    """Deterministic Miller--Rabin for n < 2^64."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_prime(n: int) -> int:
    candidate = max(2, n)
    if candidate == 2:
        return 2
    if candidate % 2 == 0:
        candidate += 1
    while not is_prime_64(candidate):
        candidate += 2
    return candidate


def all_local_subsets() -> list[tuple[int, ...]]:
    rows: list[tuple[int, ...]] = []
    for r in range(len(OFFSETS) + 1):
        rows.extend(itertools.combinations(OFFSETS, r))
    return rows


def local_enumeration() -> dict[str, Any]:
    fibers: dict[tuple[int, int, int], list[tuple[int, ...]]] = defaultdict(list)
    shifted_fibers: dict[tuple[int, int], list[tuple[int, ...]]] = defaultdict(list)
    states_by_weight: list[set[tuple[int, int]]] = [set() for _ in range(7)]
    for subset in all_local_subsets():
        weight = len(subset)
        s1 = sum(subset)
        s2 = sum(x * x for x in subset)
        fibers[(weight, s1, s2)].append(subset)
        shifted = tuple(SHIFT + x for x in subset)
        shifted_key = (sum(shifted), sum(x * x for x in shifted))
        shifted_fibers[shifted_key].append(subset)
        states_by_weight[weight].add(shifted_key)

    collisions = []
    for (weight, s1, s2), members in sorted(fibers.items()):
        if len(members) > 1:
            collisions.append(
                {
                    "weight": weight,
                    "offset_sum": s1,
                    "offset_square_sum": s2,
                    "members": [list(x) for x in sorted(members)],
                }
            )
    shifted_collisions = [
        [list(x) for x in sorted(members)]
        for _, members in sorted(shifted_fibers.items())
        if len(members) > 1
    ]
    polynomial = [len(x) for x in states_by_weight]
    left_shifted = tuple(SHIFT + x for x in LEFT)
    right_shifted = tuple(SHIFT + x for x in RIGHT)
    margins = log_concavity_margins(polynomial)
    max_local_sum = sum(SHIFT + x for x in OFFSETS)
    max_local_square_sum = sum((SHIFT + x) ** 2 for x in OFFSETS)
    return {
        "number_of_subsets": 2 ** len(OFFSETS),
        "number_of_distinct_shifted_moment_states": len(shifted_fibers),
        "offsets": list(OFFSETS),
        "left_triple": list(LEFT),
        "right_triple": list(RIGHT),
        "left_shifted": list(left_shifted),
        "right_shifted": list(right_shifted),
        "common_weight": len(LEFT),
        "common_offset_sum": sum(LEFT),
        "common_offset_square_sum": sum(x * x for x in LEFT),
        "common_shifted_sum": sum(left_shifted),
        "common_shifted_square_sum": sum(x * x for x in left_shifted),
        "left_right_equal": (
            len(LEFT) == len(RIGHT)
            and sum(LEFT) == sum(RIGHT)
            and sum(x * x for x in LEFT) == sum(x * x for x in RIGHT)
        ),
        "state_counts_by_weight": polynomial,
        "image_polynomial": polynomial,
        "image_polynomial_formula": "(1+x)^6-x^3",
        "image_polynomial_total": sum(polynomial),
        "collision_fibers": collisions,
        "shifted_collision_fibers": shifted_collisions,
        "only_nontrivial_collision_is_target_pair": (
            len(collisions) == 1
            and collisions[0]["members"] == [list(LEFT), list(RIGHT)]
            and len(shifted_collisions) == 1
        ),
        "log_concavity_margins": margins,
        "log_concave": all(x >= 0 for x in margins),
        "positional_digit_separation": {
            "max_local_sum": max_local_sum,
            "first_moment_base": BASE,
            "first_moment_no_carry": max_local_sum < BASE,
            "max_local_square_sum": max_local_square_sum,
            "second_moment_base": BASE * BASE,
            "second_moment_no_carry": max_local_square_sum < BASE * BASE,
        },
    }


def ground_set(k: int) -> list[int]:
    return [
        (SHIFT + u) * BASE**i
        for i in range(k)
        for u in OFFSETS
    ]


def target_moments(k: int) -> tuple[int, int]:
    local_sum = sum(LEFT) + len(LEFT) * SHIFT
    local_square_sum = sum((SHIFT + x) ** 2 for x in LEFT)
    return (
        local_sum * sum(BASE**i for i in range(k)),
        local_square_sum * sum(BASE ** (2 * i) for i in range(k)),
    )


def incidence_mask(indices: tuple[int, ...]) -> int:
    mask = 0
    for i in indices:
        mask |= 1 << i
    return mask


def difference_key(a: int, b: int) -> tuple[int, int]:
    return a & ~b, b & ~a


def energy_difference_counter(points: list[int]) -> int:
    counts = Counter(difference_key(a, b) for a in points for b in points)
    return sum(x * x for x in counts.values())


def energy_four_tuple(points: list[int]) -> int:
    return sum(
        difference_key(a, b) == difference_key(c, d)
        for a, b, c, d in itertools.product(points, repeat=4)
    )


def enumerate_exact_row(k: int, polynomial: list[int]) -> dict[str, Any]:
    values = ground_set(k)
    n = len(values)
    m = 3 * k
    target = target_moments(k)
    integer_image: set[tuple[int, int]] = set()
    target_points: list[int] = []
    enumerated_supports = 0
    for indices in itertools.combinations(range(n), m):
        enumerated_supports += 1
        s1 = sum(values[i] for i in indices)
        s2 = sum(values[i] * values[i] for i in indices)
        syndrome = (s1, s2)
        integer_image.add(syndrome)
        if syndrome == target:
            target_points.append(incidence_mask(indices))

    total_square_sum = sum(x * x for x in values)
    prime_test_range_ok = 2 * total_square_sum < 2**64
    if not prime_test_range_ok:
        raise ValueError("exact row exceeds deterministic 64-bit primality range")
    prime = next_prime(total_square_sum + 1)
    modular_image = {(a % prime, b % prime) for a, b in integer_image}
    image_coefficients = polynomial_power(polynomial, k)
    image_formula = image_coefficients[m]
    M = math.comb(n, m)
    L = len(integer_image)
    f = len(target_points)
    energy_counter = energy_difference_counter(target_points)
    energy_quadruples = energy_four_tuple(target_points)
    expected_energy = 6**k
    delta = Fraction(energy_counter, f**3)
    sidon_floor = Fraction(2 * f * f - f, f**3)
    energy_over_floor = Fraction(energy_counter, 2 * f * f - f)
    normalized_ratio = Fraction(f * L, M)
    central_bound_lhs = L * (6 * k + 1)
    central_bound_rhs = 63**k
    return {
        "k": k,
        "N": n,
        "m": m,
        "density": "1/2",
        "full_slice_size_M": M,
        "enumerated_full_slice_size": enumerated_supports,
        "realized_image_size_L": L,
        "realized_image_size_from_polynomial": image_formula,
        "barN": fraction_record(Fraction(M, L)),
        "target": {"sum": target[0], "square_sum": target[1]},
        "target_fiber_size": f,
        "target_fiber_expected_size": 2**k,
        "normalized_target_ratio_f_over_barN": fraction_record(normalized_ratio),
        "energy_difference_counter": energy_counter,
        "energy_four_tuple": energy_quadruples,
        "energy_expected_6_pow_k": expected_energy,
        "Delta": fraction_record(delta),
        "universal_sidon_floor": fraction_record(sidon_floor),
        "energy_over_universal_sidon_floor": fraction_record(energy_over_floor),
        "total_ground_square_sum": total_square_sum,
        "field_prime": prime,
        "field_prime_is_64bit_prime": is_prime_64(prime),
        "prime_test_range_below_2_pow_64": prime_test_range_ok and prime < 2**64,
        "no_wrap": prime > total_square_sum,
        "bertrand_upper_bound_p_lt_2_times_square_sum": prime < 2 * total_square_sum,
        "modular_image_equals_integer_image": len(modular_image) == L,
        "all_locators_nonzero_mod_p": all(0 < x < prime for x in values),
        "central_average_bound": {
            "lhs_L_times_6k_plus_1": central_bound_lhs,
            "rhs_63_pow_k": central_bound_rhs,
            "holds": central_bound_lhs >= central_bound_rhs,
        },
        "image_cap_gate": {
            "L_le_p_squared": L <= prime * prime,
            "f_over_barN_le_p_squared_cross_multiplied": f * L <= M * prime * prime,
        },
        "checks": {
            "full_slice_count": enumerated_supports == M,
            "image_size_at_most_slice_size": len(integer_image) <= M,
            "image_polynomial_matches_enumeration": L == image_formula,
            "target_fiber_is_exact_product": f == 2**k,
            "energy_routes_agree": energy_counter == energy_quadruples,
            "energy_is_6_pow_k": energy_counter == expected_energy,
            "delta_is_3_over_4_pow_k": delta == Fraction(3**k, 4**k),
            "field_model_is_exact": (
                prime_test_range_ok
                and prime > total_square_sum
                and is_prime_64(prime)
                and prime < 2 * total_square_sum
                and len(modular_image) == L
            ),
        },
    }


def log_concavity_checks(polynomial: list[int]) -> dict[str, Any]:
    rows = []
    for k in range(1, 13):
        coefficients = polynomial_power(polynomial, k)
        center = coefficients[3 * k]
        margins = log_concavity_margins(coefficients)
        rows.append(
            {
                "k": k,
                "central_coefficient": center,
                "symmetric": coefficients == list(reversed(coefficients)),
                "log_concave": all(x >= 0 for x in margins),
                "central_is_maximum": center == max(coefficients),
                "central_average_bound": center * (6 * k + 1) >= 63**k,
            }
        )
    return {
        "base_polynomial": polynomial,
        "base_log_concavity_margins": log_concavity_margins(polynomial),
        "base_is_log_concave": all(x >= 0 for x in log_concavity_margins(polynomial)),
        "bounded_convolution_check_range": [1, 12],
        "rows": rows,
        "all_bounded_checks_pass": all(
            r["symmetric"]
            and r["log_concave"]
            and r["central_is_maximum"]
            and r["central_average_bound"]
            for r in rows
        ),
        "asymptotic_use": (
            "The standard preservation of nonnegative log-concavity under convolution "
            "makes the central coefficient maximal; summing the 6k+1 coefficients "
            "then gives L_k >= 63^k/(6k+1). The separate k=3r proof below "
            "does not rely on this preservation theorem."
        ),
    }


def cube_energy_brute(d: int) -> int:
    points = list(range(1 << d))
    return energy_difference_counter(points)


def fixed_c_countergate() -> dict[str, Any]:
    rows = []
    for d in (1, 2, 3, 6, 12):
        f = 2**d
        energy = 6**d
        delta = Fraction(3**d, 4**d)
        rows.append(
            {
                "dimension": d,
                "fiber_size": f,
                "energy": energy,
                "Delta": fraction_record(delta),
                "Delta_squared_ge_1_over_f": energy * energy >= f**5,
                "equivalent_integer_gate_9_pow_d_ge_8_pow_d": 9**d >= 8**d,
                "brute_energy_if_d_le_6": cube_energy_brute(d) if d <= 6 else None,
                "brute_energy_matches": cube_energy_brute(d) == energy if d <= 6 else True,
            }
        )
    return {
        "claim_audited": (
            "A lower bound Delta(F)>=|F|^{-c} for one fixed c<1 does not, "
            "by itself, rule out Delta(F)=exp(-Theta(N))."
        ),
        "witness": "the full Boolean cubes F_d={0,1}^d",
        "exact_formulas": {
            "size": "2^d",
            "energy": "6^d",
            "Delta": "(3/4)^d",
            "power_exponent_c0": "log_2(4/3)",
            "exponential_decay_rate": "log(4/3)",
        },
        "fixed_c_example": {
            "c": "1/2",
            "bound": "Delta(F_d)>=|F_d|^{-1/2}",
            "exact_gate": "9^d>=8^d",
            "coexists_with_fixed_sigma_low_energy": True,
        },
        "rows": rows,
        "all_checks_pass": all(
            r["Delta_squared_ge_1_over_f"]
            and r["equivalent_integer_gate_9_pow_d_ge_8_pow_d"]
            and r["brute_energy_matches"]
            for r in rows
        ),
        "conclusion": (
            "Beating the Sidon exponent 1 by an unspecified fixed c<1 is not "
            "the same as an exp(-o(N)) energy floor and is insufficient for the "
            "printed every-fixed-sigma Sidon cut without an additional quantified argument."
        ),
    }


def build_payload() -> dict[str, Any]:
    frontiers_pins = pin_frontiers_labels(repo_root())
    local = local_enumeration()
    polynomial = local["image_polynomial"]
    exact_rows = [enumerate_exact_row(k, polynomial) for k in EXACT_K]
    lc = log_concavity_checks(polynomial)
    cube_gate = fixed_c_countergate()
    ratio_formula_checks = []
    for row in exact_rows:
        k = row["k"]
        f = row["target_fiber_size"]
        exact_ratio = Fraction(row["energy_difference_counter"], 2 * f * f - f)
        displayed_ratio = Fraction(3, 2) ** k / (2 - Fraction(1, 2) ** k)
        ratio_formula_checks.append(exact_ratio == displayed_ratio)
    near_sidon_semantics = {
        "printed_pr_585_property": (
            "For every fixed threshold thr>0, Delta=(3/4)^k<=thr eventually, "
            "and Delta-(2f-1)/f^2 tends to zero in absolute value."
        ),
        "tex_fixed_sigma_membership": (
            "Delta=exp(-(log(4/3)/6)N), so the fiber lies in every TeX cut "
            "Delta<=exp(-sigma N) with fixed sigma<log(4/3)/6."
        ),
        "literal_sidon_energy_floor": "2f^2-f",
        "exact_multiplicative_ratio": "E/(2f^2-f)=(3/2)^k/(2-2^(-k))",
        "ratio_formula_verified_on_exact_rows": all(ratio_formula_checks),
        "ratio_diverges_exponentially": Fraction(3, 2) > 1,
        "multiplicatively_near_the_literal_sidon_floor": False,
        "permitted_language": (
            "#585 fixed-threshold/absolute-o(1) near-Sidon and TeX-low-energy only; "
            "never multiplicatively or literally Sidon"
        ),
    }
    open_pr_interactions = {
        "pr_564": {
            "author": "scottdhughes",
            "url": "https://github.com/przchojecki/rs-mca/pull/564",
            "evidence_status": "MEASURED / FRAMING",
            "finding": (
                "Structured-moment-curve toys support the large-doubling / "
                "nearly-Sidon framing and show that BSG/Freiman is the wrong tool."
            ),
            "interaction": (
                "This packet adopts that tool-selection warning, but its exact "
                "Prouhet block product is a different construction and is not "
                "multiplicatively near the literal Sidon floor."
            ),
            "same_construction": False,
            "bsg_freiman_closure_claimed": False,
            "prouhet_product_multiplicatively_near_floor": False,
        },
        "pr_614": {
            "author": "holmbuar",
            "url": "https://github.com/przchojecki/rs-mca/pull/614",
            "evidence_status": "PROVED / INTERFACE",
            "finding": (
                "The image-normalized razor is orthogonal to the span-normalized "
                "(S_E) image clause."
            ),
            "interaction": (
                "This packet stays entirely on the image-normalized fiber side "
                "and makes no span-side consequence claim in either direction."
            ),
            "normalizations_orthogonal": True,
            "span_side_consequence_claimed": False,
        },
    }

    row3 = next(r for r in exact_rows if r["k"] == 3)
    elementary_base_num = row3["realized_image_size_L"]
    elementary_base_den = 32768
    three_block_binomial_terms = {
        "binom_18_9": math.comb(18, 9),
        "minus_3_binom_12_6": -3 * math.comb(12, 6),
        "plus_3_binom_6_3": 3 * math.comb(6, 3),
        "minus_1": -1,
    }
    three_block_binomial_total = sum(three_block_binomial_terms.values())

    checks = {
        "local_64_subsets": local["number_of_subsets"] == 64,
        "local_63_states": local["number_of_distinct_shifted_moment_states"] == 63,
        "local_unique_collision": local["only_nontrivial_collision_is_target_pair"],
        "local_polynomial": polynomial == list(EXPECTED_LOCAL_POLYNOMIAL),
        "local_polynomial_log_concave": local["log_concave"],
        "positional_digit_separation": all(
            local["positional_digit_separation"][key]
            for key in ("first_moment_no_carry", "second_moment_no_carry")
        ),
        "all_exact_rows": all(all(r["checks"].values()) for r in exact_rows),
        "all_row_central_bounds": all(r["central_average_bound"]["holds"] for r in exact_rows),
        "all_row_image_caps": all(all(r["image_cap_gate"].values()) for r in exact_rows),
        "bounded_log_concavity_checks": lc["all_bounded_checks_pass"],
        "elementary_45907_over_32768_is_gt_one": elementary_base_num > elementary_base_den,
        "cube_fixed_c_countergate": cube_gate["all_checks_pass"],
        "frontiers_labels_pinned": frontiers_pins["all_found"],
        "three_block_binomial_derivation": (
            three_block_binomial_total == elementary_base_num == 45907
        ),
        "near_sidon_semantics_scope": (
            near_sidon_semantics["ratio_formula_verified_on_exact_rows"]
            and near_sidon_semantics["ratio_diverges_exponentially"]
            and not near_sidon_semantics["multiplicatively_near_the_literal_sidon_floor"]
        ),
        "open_pr_interaction_scope": (
            not open_pr_interactions["pr_564"]["same_construction"]
            and not open_pr_interactions["pr_564"]["bsg_freiman_closure_claimed"]
            and not open_pr_interactions["pr_564"]["prouhet_product_multiplicatively_near_floor"]
            and open_pr_interactions["pr_614"]["normalizations_orthogonal"]
            and not open_pr_interactions["pr_614"]["span_side_consequence_claimed"]
        ),
    }

    payload: dict[str, Any] = {
        "schema": SCHEMA,
        "object": "exact R=2 two-nontrivial-moment near-Sidon razor",
        "status": STATUS,
        "verdict": (
            "COUNTEREXAMPLE_NEW_FLOOR for the unrestricted literal interface; "
            "OPEN/SPECIFICATION-GATED for a smooth or circle primitive first-match residual"
        ),
        "base_sha": BASE_SHA,
        "generated_by": str(Path(__file__).relative_to(repo_root())).replace("\\", "/"),
        "lineage_and_credit": [
            {
                "pr": 444,
                "credit": "avdeevvadim",
                "url": "https://github.com/przchojecki/rs-mca/pull/444",
                "role": (
                    "degree-one predecessor: the fixed-weight (|S|,sum t) block-trade "
                    "literal-interface counterexample and specification floor"
                ),
            },
            {
                "pr": 564,
                "credit": "scottdhughes",
                "url": "https://github.com/przchojecki/rs-mca/pull/564",
                "role": (
                    "structured-moment-curve toy evidence for the large-doubling / "
                    "nearly-Sidon framing and against a BSG/Freiman attack"
                ),
            },
            {
                "pr": 575,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/575",
                "role": "image-normalized Sidon payment reduced to max-fiber control",
            },
            {
                "pr": 577,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/577",
                "role": "Newton--Girard injectivity for R>=m",
            },
            {
                "pr": 579,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/579",
                "role": "R=2 fixed-m max-fiber bound and localization to linear density",
            },
            {
                "pr": 581,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/581",
                "role": "finite R=2 large-fiber/energy sweep audited by this certificate",
            },
            {
                "pr": 582,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/582",
                "role": "reduction to beating the Sidon floor; fixed-c claim countergated here",
            },
            {
                "pr": 585,
                "credit": "LegaSage",
                "url": "https://github.com/przchojecki/rs-mca/pull/585",
                "role": "capstone map that printed the exact remaining R=2 razor",
            },
            {
                "pr": 614,
                "credit": "holmbuar",
                "url": "https://github.com/przchojecki/rs-mca/pull/614",
                "role": (
                    "proved orthogonality of the image-normalized razor and the "
                    "span-normalized (S_E) image clause"
                ),
            },
        ],
        "open_pr_interactions": open_pr_interactions,
        "frontiers_label_pins": frontiers_pins,
        "construction": {
            "shift_D": SHIFT,
            "positional_base": BASE,
            "local_offsets_U": list(OFFSETS),
            "prouhet_pair": [list(LEFT), list(RIGHT)],
            "ground_set": "T_k={(D+u)B^i: 0<=i<k, u in U}",
            "active_coordinates_N": "6k",
            "fixed_weight_m": "3k",
            "map": "Phi(S)=(sum_{t in S}t, sum_{t in S}t^2) in F_p^2",
            "weighted_vandermonde_form": "(t,t^2)=rho(t)(1,t) with rho(t)=t!=0",
            "field_choice": (
                "choose a prime p greater than sum_{t in T_k}t^2; all first and "
                "second subset moments then have no modular wrap"
            ),
            "digit_separation": (
                "max local first digit 138<1000 and max local second digit "
                "3202<1000^2, so equality of global moments is blockwise"
            ),
            "total_square_sum": "3202*(B^(2k)-1)/(B^2-1)",
            "field_growth": (
                "Bertrand gives a prime between the no-wrap threshold and twice "
                "that threshold, hence log p=2k log B+O(1)=Theta(N)"
            ),
            "target_fiber": "choose exactly one of the two Prouhet triples in every block",
            "target_fiber_size": "2^k",
            "target_energy": "6^k",
            "target_Delta": "(3/4)^k=exp(-(log(4/3)/6)N)",
            "literal_sidon_floor_ratio": (
                "E/(2f^2-f)=6^k/(2*4^k-2^k), asymptotic to (3/2)^k/2; "
                "the construction is TeX-low-energy but not multiplicatively close "
                "to the literal Sidon minimum"
            ),
        },
        "local_enumeration": local,
        "full_slice_exact_rows": exact_rows,
        "log_concavity_and_central_bound": lc,
        "elementary_positive_rate_subsequence": {
            "subsequence": "k=3r, hence N=18r and m=9r",
            "three_block_image_count": elementary_base_num,
            "three_block_binomial_derivation": {
                "identity": (
                    "[x^9]((1+x)^6-x^3)^3="
                    "C(18,9)-3C(12,6)+3C(6,3)-1"
                ),
                "terms": three_block_binomial_terms,
                "total": three_block_binomial_total,
                "matches_exact_image_count": three_block_binomial_total == elementary_base_num,
            },
            "three_block_target_fiber_size": 8,
            "target_fiber_size": "8^r",
            "full_slice_bound": "M_{3r}=binom(18r,9r)<=2^(18r)",
            "image_lower_bound": (
                "L_{3r}>=45907^r: in each group of three blocks choose one of "
                "the 45907 realized states of total weight 9; positional digits make "
                "the r group choices distinct and their total weight is 9r"
            ),
            "denominator_derivation": "2^(18r)/8^r=32768^r",
            "normalized_ratio_lower_bound": "f/barN=fL/M>=(45907/32768)^r",
            "ratio_base": fraction_record(Fraction(elementary_base_num, elementary_base_den)),
            "strictly_greater_than_one": elementary_base_num > elementary_base_den,
            "positive_rate_per_active_coordinate": "log(45907/32768)/18",
            "energy_cut": (
                "Delta=(3/4)^(3r)=exp(-(log(4/3)/6)N), so every fixed "
                "sigma<log(4/3)/6 eventually includes the target fiber"
            ),
            "moment_accessibility": (
                "L<=63^k gives log(L)/(Nq)<=log(63)/(6q)->0 for every q->infinity"
            ),
            "sidon_moment_lower_bound": (
                "one target contributes L^{-1}(f/barN)^q, whose normalized "
                "logarithmic rate tends to at least log(45907/32768)/18>0"
            ),
            "uses_log_concavity": False,
        },
        "image_cap_cut": {
            "exact_identity": "f_s/barN=f_s L/M<=L",
            "R2_codomain_bound": "L<=p^2",
            "consequence": (
                "If log p=o(N), then every fiber has f_s/barN<=exp(o(N)) and "
                "Gsid<=p^(2q)=exp(o(Nq)); no energy calculation is needed."
            ),
            "audit_of_pr_581": (
                "Its p=O(N) rows lie entirely inside this automatic cap. Rows "
                "with sampled Omega are additionally bounded by the fixed sample size."
            ),
            "construction_escapes_cap_only_by": "log p=Theta(N)",
            "all_exact_row_cap_checks": all(all(r["image_cap_gate"].values()) for r in exact_rows),
        },
        "fixed_c_less_than_one_countergate": cube_gate,
        "near_sidon_semantics_gate": near_sidon_semantics,
        "hypothesis_audit": {
            "matches_literal_quantitative_interface": [
                "full fixed-weight slice with m/N=1/2",
                "two nontrivial power sums over an odd prime field",
                "nonzero weighted Vandermonde columns with rho(t)=t",
                "actual realized-image normalization barN=M/L",
                "torsion-free additive energy on incidence vectors in Z^T",
                "logarithmic-moment accessibility",
                "a fixed-sigma exponentially low-energy fiber",
                "positive-exponential max-fiber ratio and Sidon moment",
            ],
            "not_supplied_or_not_claimed": [
                "T_k is not a smooth multiplicative coset or circle domain",
                "the visible six-point block/Prouhet product has not survived a formal first-match atlas",
                "no exact primitive-residual complement predicate is asserted",
                "no quotient, folding, planted, or block-profile nonmembership is asserted",
                "the construction is not a deployed finite RS-MCA row",
            ],
            "promotion_boundary": (
                "The certificate settles the unrestricted literal #585 question. A theorem for "
                "smooth/circle rows must state the domain class and exact primitive first-match "
                "exclusions before this construction can be declared absorbed."
            ),
        },
        "nonclaims": [
            "Not a counterexample to a formally specified smooth multiplicative-domain theorem.",
            "Not a counterexample to a formally specified circle-domain theorem.",
            "Not a claim that the block product survives an exact primitive first-match residual.",
            "Not a refutation of the conditional compiler theorem; it shows that the unrestricted literal Sidon-payment premise can fail.",
            "Not a finite deployed-row result and not a modification of any TeX draft.",
            "The phrase near-Sidon here means the printed fixed-sigma exponential-energy cut; the target is exponentially above the literal energy minimum in multiplicative ratio.",
        ],
        "verification": {
            "stdlib_only": True,
            "exact_local_enumeration": True,
            "exact_full_slice_enumeration_k": list(EXACT_K),
            "independent_energy_routes": ["difference multiplicities", "four-tuple enumeration"],
            "artifact_path": str(ARTIFACT).replace("\\", "/"),
            "regeneration": (
                "python3 experimental/scripts/verify_c9_r2_near_sidon_razor.py --write"
            ),
            "check": (
                "python3 experimental/scripts/verify_c9_r2_near_sidon_razor.py --check"
            ),
            "tamper_selftest": (
                "python3 experimental/scripts/verify_c9_r2_near_sidon_razor.py --tamper-selftest"
            ),
        },
        "checks": checks,
        "all_pass": all(checks.values()),
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate_against(candidate: dict[str, Any], expected: dict[str, Any]) -> list[str]:
    errors = []
    if candidate.get("payload_sha256") != payload_hash(candidate):
        errors.append("payload_sha256 does not authenticate candidate payload")
    if without_hash(candidate) != without_hash(expected):
        errors.append("candidate payload differs from exact recomputation")
    if not candidate.get("all_pass"):
        errors.append("all_pass is false")
    checks = candidate.get("checks")
    if not isinstance(checks, dict) or not checks or not all(checks.values()):
        errors.append("one or more top-level checks fail")
    return errors


def write_artifact(root: Path) -> int:
    payload = build_payload()
    if not payload["all_pass"]:
        print("RESULT: FAIL internal checks", file=sys.stderr)
        return 1
    path = root / ARTIFACT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE {path}")
    print(f"payload_sha256: {payload['payload_sha256']}")
    print(f"verdict: {payload['verdict']}")
    print("RESULT: PASS")
    return 0


def check_artifact(root: Path) -> int:
    path = root / ARTIFACT
    if not path.is_file():
        print(f"RESULT: FAIL missing artifact {path}", file=sys.stderr)
        return 1
    candidate = json.loads(path.read_text(encoding="utf-8"))
    expected = build_payload()
    errors = validate_against(candidate, expected)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print("RESULT: FAIL", file=sys.stderr)
        return 1
    print("C9 R=2 near-Sidon razor artifact check passed")
    print(f"payload_sha256: {candidate['payload_sha256']}")
    print(f"verdict: {candidate['verdict']}")
    print("exact rows: k=1,2,3; local subsets=64; two energy routes")
    print("RESULT: PASS")
    return 0


def tamper_selftest() -> int:
    expected = build_payload()

    def bump_local_polynomial(x: dict[str, Any]) -> None:
        x["local_enumeration"]["image_polynomial"][3] += 1

    def bump_row_image(x: dict[str, Any]) -> None:
        x["full_slice_exact_rows"][2]["realized_image_size_L"] += 1

    def bump_energy(x: dict[str, Any]) -> None:
        x["full_slice_exact_rows"][2]["energy_difference_counter"] += 2

    def weaken_elementary_base(x: dict[str, Any]) -> None:
        x["elementary_positive_rate_subsequence"]["three_block_image_count"] -= 1

    def flip_image_cap(x: dict[str, Any]) -> None:
        x["image_cap_cut"]["all_exact_row_cap_checks"] = False

    def corrupt_cube(x: dict[str, Any]) -> None:
        x["fixed_c_less_than_one_countergate"]["rows"][2]["energy"] += 1

    def delete_nonclaim(x: dict[str, Any]) -> None:
        x["nonclaims"].pop()

    def corrupt_credit(x: dict[str, Any]) -> None:
        x["lineage_and_credit"][0]["pr"] = 445

    def assert_multiplicative_near_sidon(x: dict[str, Any]) -> None:
        x["near_sidon_semantics_gate"]["multiplicatively_near_the_literal_sidon_floor"] = True

    def corrupt_frontiers_pin(x: dict[str, Any]) -> None:
        x["frontiers_label_pins"]["labels"]["def:sidon-heavy"]["found"] = False

    def assert_span_side_consequence(x: dict[str, Any]) -> None:
        x["open_pr_interactions"]["pr_614"]["span_side_consequence_claimed"] = True

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("local polynomial", bump_local_polynomial),
        ("k=3 image", bump_row_image),
        ("target energy", bump_energy),
        ("elementary 45907 base", weaken_elementary_base),
        ("image cap", flip_image_cap),
        ("full cube", corrupt_cube),
        ("nonclaim", delete_nonclaim),
        ("lineage credit", corrupt_credit),
        ("multiplicative Sidon overclaim", assert_multiplicative_near_sidon),
        ("frontiers label pin", corrupt_frontiers_pin),
        ("PR #564/#614 interaction scope", assert_span_side_consequence),
    ]
    accepted = []
    for name, mutate in mutations:
        bad = copy.deepcopy(expected)
        mutate(bad)
        # Model an adversary who recomputes the public hash after tampering.
        bad["payload_sha256"] = payload_hash(bad)
        if not validate_against(bad, expected):
            accepted.append(name)
    if accepted:
        print(f"RESULT: FAIL undetected mutations: {accepted}", file=sys.stderr)
        return 1
    print(f"tamper self-test rejected {len(mutations)} semantic mutations")
    print("RESULT: PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--write", action="store_true", help="write the exact JSON artifact")
    modes.add_argument("--check", action="store_true", help="recompute and check the artifact")
    modes.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="ensure semantic mutations are rejected even after rehashing",
    )
    args = parser.parse_args(argv)
    root = repo_root()
    if args.write:
        return write_artifact(root)
    if args.check:
        return check_artifact(root)
    return tamper_selftest()


if __name__ == "__main__":
    raise SystemExit(main())
