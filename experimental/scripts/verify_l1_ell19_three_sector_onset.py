#!/usr/bin/env python3
"""ell=19 exact-three-sector D-positive sharp onset.

Exact cyclotomic five-root gcds compress all 44 exceptional four-minor
characteristics to powers of 7, 11 and 37; none is 1 modulo 19.  Proper
two-sector specializations have gcd one.  Hence every live specialization
available over a prime field has the uniform robust fiber cap c=4.

An optimized exact C++ audit enumerates only full-support projective states
with a four-point fiber.  It proves the uniform proportional bound S_10<=36.
The common-root deficit theorem makes every D>0 row with tau<=9 vacant.

The exceptional geometry also moves the onset earlier than the generic
three-fiber heuristic: over F_4409,

    Gamma = X + 2307 X^9 + 251 X^17

has spectrum 4^8 2^8 1^216 and S_11=38.  Lambda-free anchors for
tau=10,...,16 plus exact common-dead padding supply every remaining D>0 row.
Thus the sharp onset is tau=10.
"""

from __future__ import annotations

import itertools
import json
import math
import os
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path

import verify_l1_ell7_three_sector_counterexample as base
import verify_l1_ell11_three_sector_onset as ell11
import verify_l1_multisector_common_root_deficit as deficit
import verify_l1_ell7_four_sector_counterexample as ell7four
import verify_l1_ell17_three_sector_onset as ell17


ELL = 19
BAD_PRIMES = [
    191,
    229,
    419,
    457,
    571,
    647,
    1103,
    1217,
    1559,
    2243,
    2357,
    2927,
    3041,
    3079,
    4409,
    4637,
    7639,
    7867,
    9767,
    10223,
    12959,
    14821,
    23561,
    23827,
    26297,
    27551,
    28843,
    32909,
    37013,
    40471,
    43853,
    47387,
    53353,
    78167,
    95419,
    137941,
    228989,
    352489,
    362027,
    510683,
    797051,
    1340071,
    3833707,
    8494331,
]
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
CPP_SOURCE = ROOT / "experimental" / "scripts" / "verify_l1_ell19_three_sector_spectrum.cpp"
GPP = shutil.which(os.environ.get("CXX", "g++"))
ARTIFACT = DATA / "ell19_three_sector_onset.json"
UPSTREAM = ROOT
UPSTREAM_RESIDUAL = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_PV = (
    UPSTREAM / "experimental" / "notes" / "l1" / "l1_prime_ell_pv_refutation.md"
)
UPSTREAM_RECONSTRUCTION = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_general_reconstruction_collapse.md"
)


# ============================================================================
# Route comparison and exact five-root compression


def route_preflight() -> dict[str, object]:
    ell19_grid = [
        (tau, core_size, core_size - tau - 1)
        for tau in range(5, 17)
        for core_size in range(tau + 2, 19)
    ]
    ell11_four_grid = [
        (tau, core_size, core_size - tau - 1)
        for tau in range(5, 9)
        for core_size in range(tau + 2, 11)
    ]
    assert len(ell19_grid) == 78 and len(ell11_four_grid) == 10
    ell19_orbits = {
        size: len(ell7four.affine_representatives(19, size))
        for size in (3, 4, 5)
    }
    ell11_orbits = {
        size: len(ell7four.affine_representatives(11, size))
        for size in (4, 5, 6)
    }
    assert ell19_orbits == {3: 4, 4: 14, 5: 36}
    assert ell11_orbits == {4: 4, 5: 6, 6: 6}
    return {
        "route_A_ell19_exact_three": {
            "D_positive_rows": len(ell19_grid),
            "AGL_orbits_sizes_3_4_5": ell19_orbits,
            "payoff": (
                "A complete cross-prime onset law over 78 rows, extending "
                "the ell=11,13,17 sequence and testing whether exceptional "
                "four-fiber geometry shifts the generic onset."
            ),
        },
        "route_B_ell11_exact_four": {
            "D_positive_rows": len(ell11_four_grid),
            "AGL_orbits_sizes_4_5_6": ell11_orbits,
            "deferred_obligation": (
                "Opening exact four sectors requires a new six-root "
                "compression and exact-four proportional envelope.  It is "
                "a valid ten-row grid, but yields less theorem-scale payoff "
                "than the complete ell=19 law."
            ),
        },
        "selected": "route A: ell=19 exact-three-sector complete onset",
    }


def normalized_norm_table(size: int) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    representatives = ell7four.affine_representatives(19, size)
    table = []
    for exponents in representatives:
        row = []
        for roots in representatives:
            determinant = base.alternant_polynomial(exponents, roots)
            vandermonde = base.vandermonde_polynomial(roots)
            quotient = base.integer_poly_exact_division(
                determinant, vandermonde
            )
            row.append(abs(ell7four.generic_cyclotomic_norm(quotient, 19)))
        table.append(row)
    return representatives, table


def five_root_gcd_compression() -> dict[str, object]:
    reps3, table3 = normalized_norm_table(3)
    reps4, table4 = normalized_norm_table(4)
    reps5 = ell7four.affine_representatives(19, 5)
    assert len(reps3) == 4 and len(reps4) == 14 and len(reps5) == 36
    assert table3 == [
        [1, 1, 1, 1],
        [1, 457, 191, 343],
        [1, 191, 2699, 1331],
        [1, 343, 1331, 117649],
    ]
    distinct_four_norms = sorted({value for row in table4 for value in row})
    bad_primes = sorted(
        {
            prime
            for value in distinct_four_norms
            for prime in ell7four.distinct_prime_factors(value)
            if prime % 19 == 1
        }
    )
    assert bad_primes == BAD_PRIMES

    index3 = {support: index for index, support in enumerate(reps3)}
    index4 = {support: index for index, support in enumerate(reps4)}
    full_gcd_counts = Counter()
    full_exception_rows = []
    for exponent_index, exponents in enumerate(reps4):
        for roots in reps5:
            deletion_norms = []
            for omitted in roots:
                subset = tuple(entry for entry in roots if entry != omitted)
                root_class = ell7four.affine_canonical(subset, 19)
                deletion_norms.append(table4[exponent_index][index4[root_class]])
            gcd_value = math.gcd(*deletion_norms)
            full_gcd_counts[gcd_value] += 1
            if gcd_value != 1:
                full_exception_rows.append(
                    {
                        "exponent_class": list(exponents),
                        "five_root_class": list(roots),
                        "deletion_norms": deletion_norms,
                        "gcd": gcd_value,
                        "prime_factors": ell7four.distinct_prime_factors(gcd_value),
                    }
                )
    assert full_gcd_counts == Counter(
        {1: 489, 343: 9, 1369: 3, 1331: 2, 117649: 1}
    )
    admissible_five_fiber_primes = sorted(
        {
            prime
            for row in full_exception_rows
            for prime in row["prime_factors"]
            if prime % 19 == 1
        }
    )
    assert admissible_five_fiber_primes == []

    two_sector_gcd_counts = Counter()
    for exponent_index, _exponents in enumerate(reps3):
        for roots in reps5:
            deletion_norms = []
            for subset in itertools.combinations(roots, 3):
                root_class = ell7four.affine_canonical(subset, 19)
                deletion_norms.append(table3[exponent_index][index3[root_class]])
            two_sector_gcd_counts[math.gcd(*deletion_norms)] += 1
    assert two_sector_gcd_counts == Counter({1: 144})
    return {
        "three_subset_AGL_orbits": len(reps3),
        "four_subset_AGL_orbits": len(reps4),
        "five_subset_AGL_orbits": len(reps5),
        "two_live_3x3_quotient_norm_table": table3,
        "three_live_4x4_distinct_norms": distinct_four_norms,
        "three_live_4x4_bad_admissible_primes": bad_primes,
        "full_three_sector_five_root_gcd_rows": sum(full_gcd_counts.values()),
        "full_three_sector_gcd_counts": {
            str(key): value for key, value in sorted(full_gcd_counts.items())
        },
        "full_three_sector_exception_rows": full_exception_rows,
        "admissible_five_fiber_primes": admissible_five_fiber_primes,
        "proper_two_sector_five_root_gcd_rows": sum(two_sector_gcd_counts.values()),
        "proper_two_sector_gcd_counts": {
            str(key): value for key, value in sorted(two_sector_gcd_counts.items())
        },
        "robust_live_cap": 4,
        "conclusion": (
            "All nonunit full-support five-root gcds factor over 7, 11 or "
            "37, none congruent to one modulo 19.  Proper two-sector gcds "
            "are all one, and one-sector monomials are injective on mu_19. "
            "Thus every prime p=1 mod 19 has robust live cap c=4, with no "
            "hidden exceptional characteristic."
        ),
    }


# ============================================================================
# Optimized exceptional-state audit and vacancy grid


def cpp_exceptional_state_audit() -> dict[str, object]:
    assert CPP_SOURCE.is_file() and GPP is not None
    with tempfile.TemporaryDirectory(prefix="ell19_") as directory:
        executable = Path(directory) / "ell19_spectrum.exe"
        environment = os.environ.copy()
        environment["PATH"] = (
            str(Path(GPP).parent) + os.pathsep + environment.get("PATH", "")
        )
        subprocess.run(
            [
                GPP,
                "-std=c++20",
                "-O3",
                "-DNDEBUG",
                str(CPP_SOURCE),
                "-o",
                str(executable),
            ],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        output = subprocess.run(
            [str(executable)],
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        ).stdout.strip().splitlines()
    assert output[0] == "ELL19_THREE_SECTOR_SPECTRUM_V1"
    assert output[-1] == "PASS_ELL19_THREE_SECTOR_SPECTRUM"
    rows = []
    for line in output[1:-1]:
        values = [int(entry) for entry in line.split()]
        assert len(values) == 17
        prime, quotient, singular_rows, projective_states, maximum_fiber = values[:5]
        top_6_through_17 = values[5:]
        rows.append(
            {
                "p": prime,
                "quotient_labels": quotient,
                "singular_four_root_rows": singular_rows,
                "distinct_exact_three_projective_states": projective_states,
                "maximum_fiber": maximum_fiber,
                "top_bounds_6_through_17": top_6_through_17,
            }
        )
    assert [row["p"] for row in rows] == BAD_PRIMES
    assert sum(int(row["singular_four_root_rows"]) for row in rows) == 6837
    assert sum(int(row["distinct_exact_three_projective_states"]) for row in rows) == 6837
    assert all(row["maximum_fiber"] <= 4 for row in rows)
    # index 4 is h=10 in the h=6,...,17 vector.
    assert max(row["top_bounds_6_through_17"][4] for row in rows) == 36
    maximizers = [
        row["p"] for row in rows if row["top_bounds_6_through_17"][4] == 36
    ]
    assert maximizers == [4409]
    return {
        "backend": "C++20 -O3 exact finite-field arithmetic",
        "root_quadruple_translation_orbits": 204,
        "exact_three_active_supports": 816,
        "bad_primes": BAD_PRIMES,
        "rows": rows,
        "singular_four_root_rows": 6837,
        "distinct_projective_states": 6837,
        "uniform_top_ten_bound": 36,
        "top_ten_maximizing_primes": maximizers,
        "state_completeness": (
            "Every Gamma with a four-point fiber translates to one of 204 "
            "root representatives.  Every singular matrix has rank exactly "
            "three; cofactor kernels enumerate exact-three projective states. "
            "Vectors without a four-fiber use cap three and S_10<=30."
        ),
    }


def vacancy_grid(exceptional: dict[str, object]) -> list[dict[str, object]]:
    assert exceptional["uniform_top_ten_bound"] == 36
    rows = []
    for tau in range(5, 10):
        for core_size in range(tau + 2, 19):
            D = core_size - tau - 1
            bounds = deficit.compiler_bounds(
                ell=19,
                tau=tau,
                D=D,
                live_cap=4,
                proportional_top=36,
            )
            assert 4 * (tau + 2) < 3 * 19
            assert 36 < 2 * 19
            assert bounds["compiler"] < bounds["listing"]
            rows.append(
                {
                    "tau": tau,
                    "m": core_size,
                    "D": D,
                    "robust_live_cap": 4,
                    "proportional_top_bound": 36,
                    "nonsaturated_bound": bounds["nonsaturated"],
                    "saturated_bound": bounds["saturated"],
                    "listing_requirement": bounds["listing"],
                    "strict_gap": bounds["listing"] - bounds["compiler"],
                    "vacant": True,
                }
            )
    assert len(rows) == 50
    assert min(int(row["strict_gap"]) for row in rows) == 2
    return rows


# ============================================================================
# F_4409 onset anchors and exact common-dead propagation


def gamma_spectrum_19(
    prime: int,
    generator: int,
    subgroup: list[int],
    support: tuple[int, int, int],
    gamma: list[int],
) -> list[int]:
    output = []
    for label_index in range((prime - 1) // 19):
        representative = pow(generator, label_index, prime)
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(gamma, support)
            )
            % prime
            for point in subgroup
        ]
        output.append(max(Counter(values).values()))
    return output


def build_anchor(tau: int) -> dict[str, object]:
    prime = 4409
    core_size = tau + 1
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 19
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(19)]
    support = (1, 9, 17)
    active_gamma = [1, 2307, 251]
    assert (generator, quotient_size, zeta) == (3, 232, 209)

    spectrum = gamma_spectrum_19(
        prime, generator, subgroup, support, active_gamma
    )
    assert Counter(spectrum) == Counter({1: 216, 2: 8, 4: 8})
    quotient_rows = []
    for index in range(quotient_size):
        representative = pow(generator, index, prime)
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(active_gamma, support)
            )
            % prime
            for point in subgroup
        ]
        counts = Counter(values)
        multiplicity = max(counts.values())
        level = min(value for value, count in counts.items() if count == multiplicity)
        quotient_rows.append((multiplicity, index, representative, level))
    quotient_rows.sort(key=lambda row: (-row[0], row[1]))
    selected = quotient_rows[:core_size]
    core_indices = [row[1] for row in selected]
    core_representatives = [row[2] for row in selected]
    target_levels = [row[3] for row in selected]
    profile = [row[0] for row in selected]
    expected_retained = 38 + 2 * (tau - 10) if tau <= 15 else 49
    assert sum(profile) == expected_retained

    beta = [pow(value, 19, prime) for value in core_representatives]
    core_locator = base.polynomial_from_roots_mod(beta, prime)
    available_petals = [
        index for index in range(quotient_size) if index not in core_indices
    ]
    solved = None
    for shift in range(len(available_petals) - tau + 1):
        petal_indices = available_petals[shift : shift + tau]
        petal_representatives = [
            pow(generator, index, prime) for index in petal_indices
        ]
        alpha = [pow(value, 19, prime) for value in petal_representatives]
        try:
            solution = ell11.solve_level_system(
                prime, alpha, beta, core_locator, target_levels
            )
        except AssertionError:
            continue
        solved = (petal_indices, petal_representatives, alpha, solution)
        break
    assert solved is not None
    petal_indices, petal_representatives, alpha, solution = solved
    petal_values, u_value, v_value, scalars, lambda_rank = solution
    assert v_value == 0 and lambda_rank == core_size
    assert len(set(alpha + beta)) == tau + core_size

    phi = base.polynomial_from_roots_mod(alpha, prime)
    w = base.polynomial_interpolate_mod(alpha, petal_values, prime)
    gamma_polynomial = [u_value] + [0] * 18
    for exponent, coefficient in zip(support, active_gamma):
        gamma_polynomial[exponent] = coefficient
    codeword = base.polynomial_add_mod(
        base.substitute_power(w, 19),
        base.polynomial_multiply_mod(
            base.substitute_power(phi, 19), gamma_polynomial, prime
        ),
        prime,
    )
    positive_support = sorted(
        {
            index % 19
            for index, value in enumerate(codeword)
            if value and index % 19
        }
    )
    assert positive_support == list(support)
    assert len(codeword) - 1 == tau * 19 + 17 <= core_size * 19

    petal_points = []
    for representative, value, scalar, label in zip(
        petal_representatives, petal_values, scalars, alpha
    ):
        for point in subgroup:
            x = representative * point % prime
            evaluated = base.polynomial_evaluate_mod(codeword, x, prime)
            assert evaluated == value
            assert evaluated == (
                scalar
                * base.polynomial_evaluate_mod(core_locator, label, prime)
            ) % prime
            petal_points.append(x)

    retained, missed, point_profile = [], [], []
    for representative in core_representatives:
        count = 0
        for point in subgroup:
            x = representative * point % prime
            if base.polynomial_evaluate_mod(codeword, x, prime) == 0:
                retained.append(x)
                count += 1
            else:
                missed.append(x)
        point_profile.append(count)
    assert point_profile == profile
    agreement = tau * 19 + len(retained)
    threshold = (core_size + 1) * 19
    assert agreement >= threshold
    assert len(set(petal_points + retained + missed)) == (tau + core_size) * 19
    kernel_degree, deletable, negative_deletable = ell17.deletion_certificate(
        codeword, retained, missed, prime
    )
    assert kernel_degree <= len(missed)
    assert 19 <= len(missed) <= (tau - 1) * 19
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 19,
        "tau": tau,
        "m": core_size,
        "D": 0,
        "generator": generator,
        "zeta": zeta,
        "active_nonzero_DFT_sectors": list(support),
        "gamma_active_coefficients": active_gamma,
        "spectrum_histogram": [[1, 216], [2, 8], [4, 8]],
        "core_quotient_indices": core_indices,
        "core_representatives": core_representatives,
        "target_levels": target_levels,
        "petal_quotient_indices": petal_indices,
        "petal_representatives": petal_representatives,
        "petal_values": petal_values,
        "petal_scalars": scalars,
        "g0_u_v": [u_value, v_value],
        "lambda_map_rank": lambda_rank,
        "alpha_labels": alpha,
        "core_locator_coefficients_ascending": core_locator,
        "codeword_coefficients_ascending": codeword,
        "recomputed_positive_DFT_support": positive_support,
        "degree": len(codeword) - 1,
        "degree_bound": core_size * 19,
        "core_retained_profile": profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": threshold,
        "listing_surplus": agreement - threshold,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "kernel_quotient_degree": kernel_degree,
        "single_point_deletions": deletable,
        "minimality_negative_control": negative_deletable,
        "H_stabilizer": stabilizer,
        "listed": True,
        "minimal": True,
        "primitive": True,
    }


def pad_anchor(anchor: dict[str, object], target_m: int) -> dict[str, object]:
    prime = int(anchor["p"])
    tau = int(anchor["tau"])
    base_m = int(anchor["m"])
    D = target_m - base_m
    generator = int(anchor["generator"])
    subgroup = [pow(int(anchor["zeta"]), index, prime) for index in range(19)]
    used = set(anchor["core_quotient_indices"] + anchor["petal_quotient_indices"])
    new_indices = [
        index for index in range((prime - 1) // 19) if index not in used
    ][:D]
    new_labels = [pow(generator, 19 * index, prime) for index in new_indices]
    Q = base.polynomial_from_roots_mod(new_labels, prime)
    codeword = base.polynomial_multiply_mod(
        anchor["codeword_coefficients_ascending"],
        base.substitute_power(Q, 19),
        prime,
    )
    core_locator = base.polynomial_multiply_mod(
        anchor["core_locator_coefficients_ascending"], Q, prime
    )
    support = sorted(
        {
            index % 19
            for index, value in enumerate(codeword)
            if value and index % 19
        }
    )
    assert support == anchor["active_nonzero_DFT_sectors"]
    for representative, scalar, label in zip(
        anchor["petal_representatives"],
        anchor["petal_scalars"],
        anchor["alpha_labels"],
    ):
        for point in subgroup:
            x = representative * point % prime
            assert base.polynomial_evaluate_mod(codeword, x, prime) == (
                scalar
                * base.polynomial_evaluate_mod(core_locator, label, prime)
            ) % prime

    retained, missed, profile = [], [], []
    representatives = anchor["core_representatives"] + [
        pow(generator, index, prime) for index in new_indices
    ]
    for representative in representatives:
        count = 0
        for point in subgroup:
            x = representative * point % prime
            if base.polynomial_evaluate_mod(codeword, x, prime) == 0:
                retained.append(x)
                count += 1
            else:
                missed.append(x)
        profile.append(count)
    assert profile == anchor["core_retained_profile"] + [19] * D
    assert sorted(missed) == anchor["exact_missed_core"]
    agreement = tau * 19 + len(retained)
    threshold = (target_m + 1) * 19
    assert agreement >= threshold and len(codeword) - 1 <= target_m * 19
    kernel_degree, deletable, negative_deletable = ell17.deletion_certificate(
        codeword, retained, missed, prime
    )
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 19,
        "tau": tau,
        "m": target_m,
        "D": D,
        "base_m": base_m,
        "new_dead_core_quotient_indices": new_indices,
        "Q_coefficients_ascending": Q,
        "active_nonzero_DFT_sectors": support,
        "petal_scalars": anchor["petal_scalars"],
        "core_retained_profile": profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": threshold,
        "listing_surplus": agreement - threshold,
        "degree": len(codeword) - 1,
        "degree_bound": target_m * 19,
        "exact_missed_core_size": len(missed),
        "missed_core_identical_to_anchor": True,
        "kernel_quotient_degree": kernel_degree,
        "single_point_deletions": deletable,
        "minimality_negative_control": negative_deletable,
        "H_stabilizer": stabilizer,
        "listed": True,
        "minimal": True,
        "primitive": True,
    }


def witness_family() -> dict[str, object]:
    anchors = [build_anchor(tau) for tau in range(10, 17)]
    padded = []
    for anchor in anchors:
        for target_m in range(int(anchor["m"]) + 1, 19):
            padded.append(pad_anchor(anchor, target_m))
    expected = {
        (tau, core_size)
        for tau in range(10, 17)
        for core_size in range(tau + 2, 19)
    }
    assert {(row["tau"], row["m"]) for row in padded} == expected
    assert len(padded) == 28
    return {
        "field": "F_4409",
        "anchors_D0": anchors,
        "D_positive_counterexamples": padded,
    }


# ============================================================================
# Upstream guard and assembly


def check_upstream() -> dict[str, object]:
    assert "The residual danger is `|S| >= 2`" in UPSTREAM_RESIDUAL.read_text(
        encoding="utf-8"
    )
    assert "all `ell-1` DFT sectors active" in UPSTREAM_PV.read_text(
        encoding="utf-8"
    )
    assert "explicit BIJECTION" in UPSTREAM_RECONSTRUCTION.read_text(
        encoding="utf-8"
    )
    return {
        "sources": [
            UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            UPSTREAM_PV.relative_to(ROOT).as_posix(),
            UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "Upstream has broader all-sector ell=19 context and the general "
            "cofactor machinery, but no exact-three-sector D>0 onset, no "
            "five-root gcd compression, and no F_4409 {1,9,17} family."
        ),
    }


def main() -> None:
    upstream = check_upstream()
    preflight = route_preflight()
    compression = five_root_gcd_compression()
    exceptional = cpp_exceptional_state_audit()
    vacant = vacancy_grid(exceptional)
    witnesses = witness_family()
    artifact = {
        "title": "ell=19 exact-three-sector D-positive sharp onset",
        "status": "VACANCY_AND_COUNTEREXAMPLE_ONSET_THEOREM",
        "verdict": "PASS_WITH_ELL19_EXACT_THREE_SECTOR_ONSET_CLASSIFIED",
        "route_comparison": preflight,
        "theorem": (
            "For ell=19 exact-three-active-sector D>0 rows over prime "
            "fields, the sharp tau-onset is 10: every row with 5<=tau<=9 "
            "is universally vacant, while every row with 10<=tau<=16 is "
            "nonvacant over F_4409."
        ),
        "scientific_surprise": (
            "The generic cap-three heuristic would first permit listing at "
            "h=13, tau=12.  The exceptional F_4409 spectrum has eight "
            "four-fibers and reaches S_11=38, moving the true onset two "
            "steps earlier to tau=10."
        ),
        "proof": [
            "Route A dominates: it gives a complete 78-row cross-prime onset law, while ell=11 exact-four is a valid but separate ten-row grid requiring new six-root machinery.",
            "The 14x36 five-root gcd table compresses all 44 four-minor exceptional characteristics to factors 7, 11 and 37, none admissible modulo 19. Proper two-sector gcds are all one, so c=4 is robust over every prime p=1 mod 19.",
            "Full-support vectors without a four-fiber have S_10<=30. The optimized exact audit covers all 6,837 singular projective states at the 44 bad primes and gives S_10<=36, with equality only at p=4409.",
            "common-root deficit theorem yields 4(tau+2)<57 and S_(tau+1)<=S_10<=36<38 for tau<=9, proving all 50 lower D>0 rows vacant.",
            "Over F_4409, Gamma=X+2307X^9+251X^17 has spectrum 4^8 2^8 1^216 and S_11=38. Seven lambda-free anchors and common-dead padding give all 28 upper D>0 rows.",
            "Every anchor and padded word passes exact support, original-scalar, degree, listing, missed-core, kernel-division, deletion, negative-control and stabilizer checks.",
        ],
        "five_root_exception_compression": compression,
        "exceptional_projective_state_audit": exceptional,
        "vacancy_rows": vacant,
        "witness_family": witnesses,
        "scope": (
            "Prime fields, ell=19, 5<=tau<m<19, D=m-tau-1>0, "
            "background-free full petals and exactly three active nonzero "
            "DFT sectors."
        ),
        "nonclaims": [
            "The ell=11 exact-four D>0 grid is deferred, not classified.",
            "Nonvacancy for tau>=10 is existential over F_4409, not all-prime existence.",
            "No extension-field theorem is claimed.",
            "The upstream all-eighteen-sector witnesses remain distinct.",
        ],
        "operation_counts": {
            "full_three_sector_five_root_AGL_rows": compression[
                "full_three_sector_five_root_gcd_rows"
            ],
            "proper_two_sector_five_root_AGL_rows": compression[
                "proper_two_sector_five_root_gcd_rows"
            ],
            "exceptional_singular_projective_states": exceptional[
                "distinct_projective_states"
            ],
            "vacancy_grid_rows": len(vacant),
            "D0_anchor_words": len(witnesses["anchors_D0"]),
            "D_positive_counterexample_words": len(
                witnesses["D_positive_counterexamples"]
            ),
            "blind_three_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "Return to the deferred first nonempty exact-four D>0 grid at "
            "ell=11, now using a six-root gcd compression and a proportional "
            "exact-four spectrum audit analogous to ell=19 onset result."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=19 exact-three-sector D-positive onset")
    print(
        "bad_primes="
        + str(len(BAD_PRIMES))
        + " admissible_five_fiber_primes="
        + str(compression["admissible_five_fiber_primes"])
        + " states="
        + str(exceptional["distinct_projective_states"])
    )
    print(
        "S10="
        + str(exceptional["uniform_top_ten_bound"])
        + " vacant_rows="
        + str(len(vacant))
        + " counterexample_rows="
        + str(len(witnesses["D_positive_counterexamples"]))
    )
    print(
        "anchor_retained="
        + str(
            [
                (row["tau"], row["retained_core"])
                for row in witnesses["anchors_D0"]
            ]
        )
    )
    print("PASS_WITH_ELL19_EXACT_THREE_SECTOR_ONSET_CLASSIFIED")


if __name__ == "__main__":
    main()
