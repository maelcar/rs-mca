#!/usr/bin/env python3
"""ell=17 exact-three-sector D-positive onset theorem.

The apparent ell=7 exact-four D>0 alternative is empty: under the
domain 5<=tau<m<ell, ell=7 permits only (tau,m)=(5,6), hence D=0.

At ell=17 this verifier compresses the 23 exceptional characteristics.
Five-root gcd certificates over the 11x25 AGL orbit grid leave only p=137;
that field has eight quotient labels and cannot host any parameter row, whose
minimum is tau+m=12.  Thus every geometrically available live specialization
with at most three active sectors has robust fiber cap four.

An optimized C++ exact-state auditor then checks only coefficient states with
a four-point fiber.  Across all 23 exceptional primes their proportional
top-eleven envelope is at most 33 (and all available fibers have size <=4).
The common-root deficit theorem proves every D>0 row with tau<=10 vacant.

Over F_5441, Gamma=X^3+3370X^8+3741X^13 has spectrum
4^5 2^15 1^300.  Lambda-free anchors at tau=11,12,13,14 and common-dead
padding provide every remaining D>0 row.  Hence the sharp onset is tau=11.
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


ELL = 17
BAD_PRIMES = [
    103,
    137,
    239,
    307,
    443,
    613,
    647,
    919,
    953,
    1327,
    2551,
    3061,
    3299,
    3877,
    4217,
    4523,
    5441,
    6733,
    9623,
    13907,
    88469,
    126583,
    659941,
]
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
CPP_SOURCE = ROOT / "experimental" / "scripts" / "verify_l1_ell17_three_sector_spectrum.cpp"
GPP = shutil.which(os.environ.get("CXX", "g++"))
ARTIFACT = DATA / "ell17_three_sector_onset.json"
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
# Route cut and exact cyclotomic compression


def empty_ell7_D_positive_route() -> dict[str, object]:
    rows = []
    for tau in range(5, 7):
        for core_size in range(tau + 1, 7):
            rows.append((tau, core_size, core_size - tau - 1))
    assert rows == [(5, 6, 0)]
    assert not [row for row in rows if row[2] > 0]
    return {
        "candidate": "ell=7 exact-four-sector D-positive onset",
        "domain": "5<=tau<m<7 and D=m-tau-1",
        "all_parameter_rows": [list(row) for row in rows],
        "D_positive_rows": [],
        "decision": (
            "EMPTY_ROUTE_CUT: ell=7 four-sector result already decided the unique ell=7 row, "
            "which has D=0.  No D>0 row may be invented."
        ),
    }


def normalized_norm_table(size: int) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    representatives = ell7four.affine_representatives(17, size)
    table = []
    for exponents in representatives:
        row = []
        for roots in representatives:
            determinant = base.alternant_polynomial(exponents, roots)
            vandermonde = base.vandermonde_polynomial(roots)
            quotient = base.integer_poly_exact_division(
                determinant, vandermonde
            )
            row.append(abs(ell7four.generic_cyclotomic_norm(quotient, 17)))
        table.append(row)
    return representatives, table


def five_root_gcd_compression() -> dict[str, object]:
    reps3, table3 = normalized_norm_table(3)
    reps4, table4 = normalized_norm_table(4)
    reps5 = ell7four.affine_representatives(17, 5)
    assert len(reps3) == 3 and len(reps4) == 11 and len(reps5) == 25
    assert table3 == [
        [1, 1, 1],
        [1, 239, 103],
        [1, 103, 1361],
    ]
    distinct_four_norms = sorted({value for row in table4 for value in row})
    bad_primes = sorted(
        {
            prime
            for value in distinct_four_norms
            for prime in ell7four.distinct_prime_factors(value)
            if prime % 17 == 1
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
                root_class = ell7four.affine_canonical(subset, 17)
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
    assert full_gcd_counts == Counter({1: 271, 256: 2, 137: 1, 28561: 1})
    assert sorted(
        {
            prime
            for row in full_exception_rows
            for prime in row["prime_factors"]
            if prime % 17 == 1
        }
    ) == [137]

    two_sector_gcd_counts = Counter()
    for exponent_index, _exponents in enumerate(reps3):
        for roots in reps5:
            deletion_norms = []
            for subset in itertools.combinations(roots, 3):
                root_class = ell7four.affine_canonical(subset, 17)
                deletion_norms.append(table3[exponent_index][index3[root_class]])
            two_sector_gcd_counts[math.gcd(*deletion_norms)] += 1
    assert two_sector_gcd_counts == Counter({1: 75})

    minimum_grid_labels = min(tau + core_size for tau in range(5, 15) for core_size in range(tau + 2, 17))
    assert minimum_grid_labels == 12
    assert (137 - 1) // 17 == 8 < minimum_grid_labels
    return {
        "three_subset_AGL_orbits": len(reps3),
        "four_subset_AGL_orbits": len(reps4),
        "five_subset_AGL_orbits": len(reps5),
        "two_live_3x3_quotient_norm_table": table3,
        "three_live_4x4_bad_admissible_primes": bad_primes,
        "full_three_sector_five_root_gcd_rows": sum(full_gcd_counts.values()),
        "full_three_sector_gcd_counts": {
            str(key): value for key, value in sorted(full_gcd_counts.items())
        },
        "full_three_sector_exception_rows": full_exception_rows,
        "proper_two_sector_five_root_gcd_rows": sum(two_sector_gcd_counts.values()),
        "proper_two_sector_gcd_counts": {
            str(key): value for key, value in sorted(two_sector_gcd_counts.items())
        },
        "only_admissible_five_fiber_prime": 137,
        "p137_quotient_labels": 8,
        "minimum_parameter_grid_labels": minimum_grid_labels,
        "robust_available_live_cap": 4,
        "conclusion": (
            "A five-point fiber forces every deletion minor to vanish, so "
            "its characteristic divides their norm gcd.  Proper two-sector "
            "supports have gcd one.  Full three-sector supports leave only "
            "p=137 among p=1 mod 17, but its eight quotient labels are below "
            "the grid minimum twelve.  One-sector monomials are injective on "
            "mu_17.  Hence c=4 is robust on every available parameter row."
        ),
    }


# ============================================================================
# Optimized exact exceptional-state audit


def cpp_exceptional_state_audit() -> dict[str, object]:
    assert CPP_SOURCE.is_file() and GPP is not None
    with tempfile.TemporaryDirectory(prefix="ell17_") as directory:
        executable = Path(directory) / "ell17_spectrum.exe"
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
    assert output[0] == "ELL17_THREE_SECTOR_SPECTRUM_V1"
    assert output[-1] == "PASS_ELL17_THREE_SECTOR_SPECTRUM"
    rows = []
    for line in output[1:-1]:
        values = [int(entry) for entry in line.split()]
        assert len(values) == 15
        prime, quotient, singular_rows, projective_states, maximum_fiber = values[:5]
        top_6_through_15 = values[5:]
        rows.append(
            {
                "p": prime,
                "quotient_labels": quotient,
                "singular_four_root_rows": singular_rows,
                "distinct_exact_three_projective_states": projective_states,
                "maximum_fiber": maximum_fiber,
                "top_bounds_6_through_15": top_6_through_15,
                "available_somewhere": quotient >= 12,
            }
        )
    assert [row["p"] for row in rows] == BAD_PRIMES
    assert sum(int(row["singular_four_root_rows"]) for row in rows) == 4000
    assert sum(int(row["distinct_exact_three_projective_states"]) for row in rows) == 3828
    p137 = next(row for row in rows if row["p"] == 137)
    assert p137["maximum_fiber"] == 5 and not p137["available_somewhere"]
    for row in rows:
        if row["available_somewhere"]:
            assert row["maximum_fiber"] <= 4
            # index 5 corresponds to h=11 in the h=6,...,15 vector.
            assert row["top_bounds_6_through_15"][5] <= 33
    return {
        "backend": "C++20 -O3 exact finite-field arithmetic",
        "root_quadruple_translation_orbits": 140,
        "exact_three_active_supports": 560,
        "bad_primes": BAD_PRIMES,
        "rows": rows,
        "singular_four_root_rows": sum(
            int(row["singular_four_root_rows"]) for row in rows
        ),
        "distinct_projective_states": sum(
            int(row["distinct_exact_three_projective_states"]) for row in rows
        ),
        "uniform_available_top_eleven_bound": 33,
        "state_completeness": (
            "Any Gamma with a four-point fiber has a translated root "
            "quadruple among the 140 representatives.  Cofactor kernels "
            "enumerate and projectively deduplicate every exact-three state. "
            "Coefficient vectors without a four-fiber use the generic cap "
            "three, hence S_11<=33 directly."
        ),
    }


def vacancy_grid(exceptional_audit: dict[str, object]) -> list[dict[str, object]]:
    assert exceptional_audit["uniform_available_top_eleven_bound"] == 33
    rows = []
    for tau in range(5, 11):
        for core_size in range(tau + 2, 17):
            D = core_size - tau - 1
            bounds = deficit.compiler_bounds(
                ell=17,
                tau=tau,
                D=D,
                live_cap=4,
                proportional_top=33,
            )
            assert 4 * (tau + 2) < 3 * 17
            assert 33 < 2 * 17
            assert bounds["compiler"] < bounds["listing"]
            rows.append(
                {
                    "tau": tau,
                    "m": core_size,
                    "D": D,
                    "required_quotient_labels": tau + core_size,
                    "robust_live_cap": 4,
                    "proportional_top_bound": 33,
                    "nonsaturated_bound": bounds["nonsaturated"],
                    "saturated_bound": bounds["saturated"],
                    "listing_requirement": bounds["listing"],
                    "strict_gap": bounds["listing"] - bounds["compiler"],
                    "vacant": True,
                }
            )
    assert len(rows) == 45
    assert min(int(row["strict_gap"]) for row in rows) == 1
    return rows


# ============================================================================
# F_5441 sharp onset anchors and exact common-dead propagation


def gamma_spectrum_17(
    prime: int,
    generator: int,
    subgroup: list[int],
    support: tuple[int, int, int],
    gamma: list[int],
) -> list[int]:
    output = []
    for label_index in range((prime - 1) // 17):
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


def deletion_certificate(
    codeword: list[int], retained: list[int], missed: list[int], prime: int
) -> tuple[int, list[int], list[int]]:
    retained_locator = base.polynomial_from_roots_mod(retained, prime)
    kernel, remainder = base.polynomial_divmod_mod(
        codeword, retained_locator, prime
    )
    assert not remainder
    deletable = []
    for point in missed:
        enlarged = base.polynomial_multiply_mod(
            retained_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(codeword, enlarged, prime)
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    assert deletable == []

    negative_missed = missed + [retained[0]]
    negative_locator = base.polynomial_from_roots_mod(retained[1:], prime)
    negative_deletable = []
    for point in negative_missed:
        enlarged = base.polynomial_multiply_mod(
            negative_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(codeword, enlarged, prime)
        if not rem and len(quotient) - 1 <= len(negative_missed) - 1:
            negative_deletable.append(point)
    assert negative_deletable == [retained[0]]
    return len(kernel) - 1, deletable, negative_deletable


def build_anchor(tau: int) -> dict[str, object]:
    prime = 5441
    core_size = tau + 1
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 17
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(17)]
    support = (3, 8, 13)
    active_gamma = [1, 3370, 3741]
    assert (generator, quotient_size, zeta) == (3, 320, 2670)

    spectrum = gamma_spectrum_17(
        prime, generator, subgroup, support, active_gamma
    )
    assert Counter(spectrum) == Counter({1: 300, 2: 15, 4: 5})
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
    expected_retained = 34 + 2 * (tau - 11)
    assert sum(profile) == expected_retained

    beta = [pow(value, 17, prime) for value in core_representatives]
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
        alpha = [pow(value, 17, prime) for value in petal_representatives]
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
    gamma_polynomial = [u_value] + [0] * 16
    for exponent, coefficient in zip(support, active_gamma):
        gamma_polynomial[exponent] = coefficient
    codeword = base.polynomial_add_mod(
        base.substitute_power(w, 17),
        base.polynomial_multiply_mod(
            base.substitute_power(phi, 17), gamma_polynomial, prime
        ),
        prime,
    )
    positive_support = sorted(
        {
            index % 17
            for index, value in enumerate(codeword)
            if value and index % 17
        }
    )
    assert positive_support == list(support)
    assert len(codeword) - 1 == tau * 17 + 13 <= core_size * 17

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
    agreement = tau * 17 + len(retained)
    threshold = (core_size + 1) * 17
    assert agreement >= threshold
    assert len(set(petal_points + retained + missed)) == (tau + core_size) * 17
    kernel_degree, deletable, negative_deletable = deletion_certificate(
        codeword, retained, missed, prime
    )
    assert kernel_degree <= len(missed)
    assert 17 <= len(missed) <= (tau - 1) * 17
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 17,
        "tau": tau,
        "m": core_size,
        "D": 0,
        "generator": generator,
        "zeta": zeta,
        "active_nonzero_DFT_sectors": list(support),
        "gamma_active_coefficients": active_gamma,
        "spectrum_histogram": [[1, 300], [2, 15], [4, 5]],
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
        "degree_bound": core_size * 17,
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
    subgroup = [pow(int(anchor["zeta"]), index, prime) for index in range(17)]
    used = set(anchor["core_quotient_indices"] + anchor["petal_quotient_indices"])
    new_indices = [
        index for index in range((prime - 1) // 17) if index not in used
    ][:D]
    new_labels = [pow(generator, 17 * index, prime) for index in new_indices]
    Q = base.polynomial_from_roots_mod(new_labels, prime)
    codeword = base.polynomial_multiply_mod(
        anchor["codeword_coefficients_ascending"],
        base.substitute_power(Q, 17),
        prime,
    )
    core_locator = base.polynomial_multiply_mod(
        anchor["core_locator_coefficients_ascending"], Q, prime
    )
    support = sorted(
        {
            index % 17
            for index, value in enumerate(codeword)
            if value and index % 17
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
    assert profile == anchor["core_retained_profile"] + [17] * D
    assert sorted(missed) == anchor["exact_missed_core"]
    agreement = tau * 17 + len(retained)
    threshold = (target_m + 1) * 17
    assert agreement >= threshold and len(codeword) - 1 <= target_m * 17
    kernel_degree, deletable, negative_deletable = deletion_certificate(
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
        "ell": 17,
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
        "degree_bound": target_m * 17,
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
    anchors = [build_anchor(tau) for tau in range(11, 15)]
    padded = []
    for anchor in anchors:
        for target_m in range(int(anchor["m"]) + 1, 17):
            padded.append(pad_anchor(anchor, target_m))
    expected = {
        (tau, core_size)
        for tau in range(11, 15)
        for core_size in range(tau + 2, 17)
    }
    assert {(row["tau"], row["m"]) for row in padded} == expected
    assert len(padded) == 10
    return {
        "field": "F_5441",
        "anchors_D0": anchors,
        "D_positive_counterexamples": padded,
    }


# ============================================================================
# Upstream collision guard and assembly


def check_upstream() -> dict[str, object]:
    assert "The residual danger is `|S| >= 2`" in UPSTREAM_RESIDUAL.read_text(
        encoding="utf-8"
    )
    pv_text = UPSTREAM_PV.read_text(encoding="utf-8")
    assert "all `ell-1` DFT sectors active" in pv_text
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
            "Upstream has broader all-sector ell=17 witnesses and the "
            "general cofactor machinery, but no exact-three-sector D>0 "
            "onset law, no five-root gcd compression, and no F_5441 "
            "{3,8,13} family."
        ),
    }


def main() -> None:
    upstream = check_upstream()
    empty_route = empty_ell7_D_positive_route()
    compression = five_root_gcd_compression()
    exceptional = cpp_exceptional_state_audit()
    vacant = vacancy_grid(exceptional)
    witnesses = witness_family()
    artifact = {
        "title": "ell=17 exact-three-sector D-positive sharp onset",
        "status": "VACANCY_AND_COUNTEREXAMPLE_ONSET_THEOREM",
        "verdict": "PASS_WITH_ELL17_EXACT_THREE_SECTOR_ONSET_CLASSIFIED",
        "route_comparison": {
            "ell7_exact_four_D_positive": empty_route,
            "selected": "ell=17 exceptional-characteristic compression",
        },
        "theorem": (
            "For ell=17 exact-three-active-sector D>0 rows over prime "
            "fields, the sharp tau-onset is 11: every row with 5<=tau<=10 "
            "is universally vacant, while every row with 11<=tau<=14 is "
            "nonvacant over F_5441."
        ),
        "proof": [
            "The ell=7 exact-four D>0 route is empty in the scoped domain and is cut without inventing rows.",
            "Exact 11x25 AGL five-root gcd certificates compress 23 full-support bad characteristics to p=137; proper two-sector five-root gcds are all one. Since F_137 has only eight quotient labels versus the grid minimum twelve, every available live specialization has robust cap c=4.",
            "Every proportional Gamma without a four-fiber has S_11<=33. The optimized exact audit enumerates only projective states with a four-fiber at all 23 exceptional primes; every available state still has fiber cap four and S_11<=33.",
            "common-root deficit theorem gives nonsaturated surplus 4(tau+2)-51<0 and saturated surplus 33-34<0 for tau<=10, proving all 45 such D>0 rows vacant.",
            "Over F_5441, Gamma=X^3+3370X^8+3741X^13 has spectrum 4^5 2^15 1^300. Lambda-free anchors at tau=11,12,13,14 meet listing, and exact common-dead padding supplies all ten remaining D>0 rows.",
            "All anchors and padded words pass exact sector support, original-scalar, degree, pointwise listing, kernel division, deletion, negative-control and stabilizer checks.",
        ],
        "five_root_exception_compression": compression,
        "exceptional_projective_state_audit": exceptional,
        "vacancy_rows": vacant,
        "witness_family": witnesses,
        "scope": (
            "Prime fields, ell=17, 5<=tau<m<17, D=m-tau-1>0, "
            "background-free full petals, and exactly three active nonzero "
            "DFT sectors."
        ),
        "nonclaims": [
            "The p=137 five-fiber exception is not erased algebraically; it is unavailable because the field has too few quotient labels for the scoped grid.",
            "Nonvacancy for tau>=11 is existential over F_5441, not an all-prime existence theorem.",
            "No extension-field theorem is claimed.",
            "No ell=7 exact-four D>0 row exists in the scoped domain.",
            "The upstream all-sixteen-sector witnesses are compatible and distinct from the exact-three-sector family.",
        ],
        "operation_counts": {
            "full_three_sector_five_root_AGL_rows": compression[
                "full_three_sector_five_root_gcd_rows"
            ],
            "proper_two_sector_five_root_AGL_rows": compression[
                "proper_two_sector_five_root_gcd_rows"
            ],
            "exceptional_singular_four_root_rows": exceptional[
                "singular_four_root_rows"
            ],
            "exceptional_distinct_projective_states": exceptional[
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
            "Test whether the five-root gcd compression and the onset "
            "tau=ceil(2ell/3)-1 stabilize at ell=19 for exact-three sectors, "
            "or open the first nonempty exact-four D>0 grid at ell=11."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=17 exact-three-sector D-positive onset")
    print(
        "five_root_exception="
        + str(compression["only_admissible_five_fiber_prime"])
        + " state_rows="
        + str(exceptional["singular_four_root_rows"])
        + " S11="
        + str(exceptional["uniform_available_top_eleven_bound"])
    )
    print(
        "vacant="
        + str([(row["tau"], row["m"]) for row in vacant])
    )
    print(
        "counterexamples="
        + str(
            [
                (row["tau"], row["m"], row["retained_core"])
                for row in witnesses["D_positive_counterexamples"]
            ]
        )
    )
    print("PASS_WITH_ELL17_EXACT_THREE_SECTOR_ONSET_CLASSIFIED")


if __name__ == "__main__":
    main()
