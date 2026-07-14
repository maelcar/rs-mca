#!/usr/bin/env python3
"""Classify the ell=11 exact-three-sector D>0 parameter grid.

Uniform vacancy:
    tau in {5,6}, tau < m < 11, D=m-tau-1>0.

Explicit nonvacancy over F_353:
    tau in {7,8}, tau < m < 11, D>0.

The vacancy half compiles the common-root deficit theorem. Exact
AGL-normalized cyclotomic resultants
show that every geometrically available prime has robust live cap c=3 even
when one or two active sectors vanish at a label.  Hence the proportional
envelopes S_6<=18 and S_7<=21 are strictly below 2ell=22.

The nonvacancy half starts from two D=0 lambda-free witnesses for
Gamma=X+345X^5+49X^9 over F_353 and applies exact common sector-dead padding.
Every padded word is checked pointwise and keeps the same primitive minimal
missed core.

Deterministic, offline, stdlib-only; no coefficient sampling.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import verify_l1_ell7_three_sector_counterexample as base


ELL = 11
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
ARTIFACT = DATA / "ell11_three_sector_onset.json"
UPSTREAM = ROOT
UPSTREAM_RESIDUAL = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_PV = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_prime_ell_pv_refutation.md"
)
UPSTREAM_RECONSTRUCTION = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_general_reconstruction_collapse.md"
)


# ============================================================================
# Z[zeta_11] exact norm engine


Ring = tuple[int, ...]
ZERO: Ring = (0,) * 10
ONE: Ring = (1,) + (0,) * 9


def ring_add(first: Ring, second: Ring) -> Ring:
    return tuple(first[index] + second[index] for index in range(10))


def ring_mul(first: Ring, second: Ring) -> Ring:
    output = ZERO
    for first_index, first_value in enumerate(first):
        if not first_value:
            continue
        for second_index, second_value in enumerate(second):
            if not second_value:
                continue
            residue = (first_index + second_index) % 11
            if residue == 10:
                term = tuple(-first_value * second_value for _ in range(10))
            else:
                values = [0] * 10
                values[residue] = first_value * second_value
                term = tuple(values)
            output = ring_add(output, term)
    return output


def ring_power(exponent: int) -> Ring:
    residue = exponent % 11
    if residue == 10:
        return (-1,) * 10
    output = [0] * 10
    output[residue] = 1
    return tuple(output)


def polynomial_to_ring(polynomial: list[int]) -> Ring:
    output = ZERO
    for exponent, coefficient in enumerate(polynomial):
        if coefficient:
            output = ring_add(
                output,
                tuple(coefficient * value for value in ring_power(exponent)),
            )
    return output


def ring_norm(value: Ring) -> int:
    columns = [ring_mul(value, ring_power(index)) for index in range(10)]
    matrix = [
        [columns[column][row] for column in range(10)] for row in range(10)
    ]
    return base.bareiss_determinant(matrix)


def affine_canonical(support: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((unit * entry + shift) % 11 for entry in support))
        for unit in range(1, 11)
        for shift in range(11)
    )


def orbit_representatives(size: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            affine_canonical(support)
            for support in itertools.combinations(range(11), size)
        }
    )


def normalized_minor_norm(
    exponents: tuple[int, ...], roots: tuple[int, ...]
) -> int:
    determinant = base.alternant_polynomial(exponents, roots)
    vandermonde = base.vandermonde_polynomial(roots)
    quotient = base.integer_poly_exact_division(determinant, vandermonde)
    determinant_norm = abs(ring_norm(polynomial_to_ring(determinant)))
    vandermonde_norm = abs(ring_norm(polynomial_to_ring(vandermonde)))
    quotient_norm = abs(ring_norm(polynomial_to_ring(quotient)))
    pair_count = len(roots) * (len(roots) - 1) // 2
    assert vandermonde_norm == 11**pair_count
    assert determinant_norm == vandermonde_norm * quotient_norm
    return quotient_norm


def robust_live_cap_sieve() -> dict[str, object]:
    triple_reps = orbit_representatives(3)
    quadruple_reps = orbit_representatives(4)
    assert triple_reps == [(0, 1, 2), (0, 1, 3)]
    assert quadruple_reps == [
        (0, 1, 2, 3),
        (0, 1, 2, 4),
        (0, 1, 2, 5),
        (0, 1, 3, 4),
    ]

    two_sector_table = [
        [normalized_minor_norm(exponents, roots) for roots in triple_reps]
        for exponents in triple_reps
    ]
    three_sector_table = [
        [normalized_minor_norm(exponents, roots) for roots in quadruple_reps]
        for exponents in quadruple_reps
    ]
    assert two_sector_table == [[1, 1], [1, 23]]
    assert three_sector_table == [
        [1, 1, 1, 1],
        [1, 23, 89, 1],
        [1, 89, 67, 1],
        [1, 1, 1, 529],
    ]
    bad_primes = [23, 67, 89]
    availability = [
        {
            "p": prime,
            "quotient_cosets": (prime - 1) // 11,
            "minimum_cell_labels": 12,
            "available": (prime - 1) // 11 >= 12,
        }
        for prime in bad_primes
    ]
    assert all(not row["available"] for row in availability)
    return {
        "two_sector_3x3_quotient_norm_table": two_sector_table,
        "three_sector_4x4_quotient_norm_table": three_sector_table,
        "bad_admissible_primes": bad_primes,
        "availability": availability,
        "robust_cap": 3,
        "support_specializations": {
            "three_live_sectors": (
                "cap 3: a four-point fiber forces a normalized 4x4 minor; "
                "all bad primes are unavailable"
            ),
            "two_live_sectors": (
                "cap 2: a three-point fiber forces a normalized 3x3 minor; "
                "its only bad prime 23 is unavailable"
            ),
            "one_live_sector": (
                "cap 1 because every nonzero exponent permutes prime-order "
                "mu_11"
            ),
        },
    }


def vacancy_rows() -> list[dict[str, int | bool]]:
    rows = []
    for tau in (5, 6):
        proportional_top = 3 * (tau + 1)
        for core_size in range(tau + 2, 11):
            D = core_size - tau - 1
            nonsaturated = (D - 1) * 11 + 3 * (tau + 2)
            saturated = D * 11 + proportional_top
            listing = (D + 2) * 11
            compiler = max(nonsaturated, saturated)
            assert compiler < listing
            rows.append(
                {
                    "tau": tau,
                    "m": core_size,
                    "D": D,
                    "nonsaturated_bound": nonsaturated,
                    "proportional_top_bound": proportional_top,
                    "saturated_bound": saturated,
                    "compiler_bound": compiler,
                    "listing_requirement": listing,
                    "strict_gap": listing - compiler,
                    "vacant": True,
                }
            )
    assert len(rows) == 7
    assert min(int(row["strict_gap"]) for row in rows) == 1
    return rows


# ============================================================================
# F_353 D=0 anchors and exact common-factor propagation


def solve_level_system(
    prime: int,
    alpha: list[int],
    beta: list[int],
    core_locator: list[int],
    target_levels: list[int],
) -> tuple[list[int], int, int, list[int], int]:
    tau = len(alpha)
    core_size = len(beta)
    phi = base.polynomial_from_roots_mod(alpha, prime)

    def level_map(values: list[int], u_value: int, v_value: int) -> list[int]:
        w = base.polynomial_interpolate_mod(alpha, values, prime)
        return [
            (
                -base.polynomial_evaluate_mod(w, label, prime)
                * pow(
                    base.polynomial_evaluate_mod(phi, label, prime),
                    -1,
                    prime,
                )
                - u_value
                - v_value * label
            )
            % prime
            for label in beta
        ]

    columns = []
    for variable in range(tau + 2):
        basis = [0] * (tau + 2)
        basis[variable] = 1
        columns.append(level_map(basis[:tau], basis[tau], basis[tau + 1]))
    matrix = [
        [columns[column][row] for column in range(tau + 2)]
        + [target_levels[row]]
        for row in range(core_size)
    ]

    rank = 0
    pivots = []
    for column in range(tau + 2):
        pivot = next(
            (row for row in range(rank, core_size) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [value * inverse % prime for value in matrix[rank]]
        for row in range(core_size):
            if row != rank and matrix[row][column]:
                factor = matrix[row][column]
                matrix[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        pivots.append(column)
        rank += 1
    assert rank == core_size
    free = [column for column in range(tau + 2) if column not in pivots]
    assert len(free) == 1

    for free_value in range(prime):
        solution = [0] * (tau + 2)
        solution[free[0]] = free_value
        for row, column in enumerate(pivots):
            solution[column] = (
                matrix[row][-1]
                - sum(matrix[row][index] * solution[index] for index in free)
            ) % prime
        petal_values = solution[:tau]
        actual_scalars = [
            value
            * pow(
                base.polynomial_evaluate_mod(core_locator, label, prime),
                -1,
                prime,
            )
            % prime
            for value, label in zip(petal_values, alpha)
        ]
        if all(actual_scalars) and len(set(actual_scalars)) == tau:
            assert level_map(
                petal_values, solution[tau], solution[tau + 1]
            ) == target_levels
            return (
                petal_values,
                solution[tau],
                solution[tau + 1],
                actual_scalars,
                rank,
            )
    raise AssertionError("no distinct-nonzero scalar preimage")


def build_anchor(tau: int) -> dict[str, object]:
    prime = 353
    core_size = tau + 1
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 11
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(11)]
    active_support = (1, 5, 9)
    active_gamma = [1, 345, 49]
    assert (generator, zeta, quotient_size) == (3, 140, 32)

    quotient_rows = []
    for index in range(quotient_size):
        representative = pow(generator, index, prime)
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(active_gamma, active_support)
            )
            % prime
            for point in subgroup
        ]
        counts = Counter(values)
        multiplicity = max(counts.values())
        level = min(value for value, count in counts.items() if count == multiplicity)
        quotient_rows.append((multiplicity, index, representative, level))
    quotient_rows.sort(key=lambda row: (-row[0], row[1]))
    spectrum = [row[0] for row in quotient_rows]
    assert Counter(spectrum) == Counter({1: 24, 3: 8})

    selected = quotient_rows[:core_size]
    core_indices = [row[1] for row in selected]
    core_representatives = [row[2] for row in selected]
    target_levels = [row[3] for row in selected]
    retained_profile = [row[0] for row in selected]
    petal_indices = [
        index for index in range(quotient_size) if index not in core_indices
    ][:tau]
    petal_representatives = [pow(generator, index, prime) for index in petal_indices]
    alpha = [pow(value, 11, prime) for value in petal_representatives]
    beta = [pow(value, 11, prime) for value in core_representatives]
    assert len(set(alpha + beta)) == tau + core_size
    core_locator = base.polynomial_from_roots_mod(beta, prime)
    petal_values, u_value, v_value, actual_scalars, lambda_rank = solve_level_system(
        prime, alpha, beta, core_locator, target_levels
    )
    phi = base.polynomial_from_roots_mod(alpha, prime)
    w = base.polynomial_interpolate_mod(alpha, petal_values, prime)
    gamma_polynomial = [u_value] + [0] * 9
    gamma_polynomial[1] = 1
    gamma_polynomial[5] = 345
    gamma_polynomial[9] = 49
    if v_value:
        if len(gamma_polynomial) <= 11:
            gamma_polynomial += [0] * (12 - len(gamma_polynomial))
        gamma_polynomial[11] = v_value
    codeword = base.polynomial_add_mod(
        base.substitute_power(w, 11),
        base.polynomial_multiply_mod(
            base.substitute_power(phi, 11), gamma_polynomial, prime
        ),
        prime,
    )
    positive_support = sorted(
        {
            exponent % 11
            for exponent, coefficient in enumerate(codeword)
            if coefficient and exponent % 11
        }
    )
    assert positive_support == list(active_support)

    petal_points = []
    for representative, value, scalar, label in zip(
        petal_representatives, petal_values, actual_scalars, alpha
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

    retained = []
    missed = []
    point_profile = []
    for representative in core_representatives:
        retained_here = 0
        for point in subgroup:
            x = representative * point % prime
            if base.polynomial_evaluate_mod(codeword, x, prime) == 0:
                retained.append(x)
                retained_here += 1
            else:
                missed.append(x)
        point_profile.append(retained_here)
    assert point_profile == retained_profile
    retained_core = len(retained)
    assert retained_core >= 22
    agreement = tau * 11 + retained_core
    listing_threshold = (core_size + 1) * 11
    assert agreement >= listing_threshold
    assert len(set(petal_points + retained + missed)) == (tau + core_size) * 11

    retained_locator = base.polynomial_from_roots_mod(retained, prime)
    kernel, remainder = base.polynomial_divmod_mod(
        codeword, retained_locator, prime
    )
    assert not remainder
    kernel_degree = len(kernel) - 1
    assert kernel_degree <= len(missed)
    deletable = []
    for point in missed:
        enlarged = base.polynomial_multiply_mod(
            retained_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(codeword, enlarged, prime)
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    assert deletable == []
    assert 11 <= len(missed) <= (tau - 1) * 11
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    missed_traces = [11 - value for value in point_profile]
    assert all(0 < value < 11 for value in missed_traces)

    return {
        "p": prime,
        "ell": 11,
        "tau": tau,
        "m": core_size,
        "D": 0,
        "generator": generator,
        "zeta": zeta,
        "active_nonzero_DFT_sectors": list(active_support),
        "recomputed_positive_DFT_support": positive_support,
        "gamma_active_coefficients": active_gamma,
        "spectrum_histogram": [[1, 24], [3, 8]],
        "core_quotient_indices": core_indices,
        "core_representatives": core_representatives,
        "target_levels": target_levels,
        "petal_quotient_indices": petal_indices,
        "petal_representatives": petal_representatives,
        "petal_values": petal_values,
        "petal_scalars": actual_scalars,
        "g0_u_v": [u_value, v_value],
        "lambda_map_rank": lambda_rank,
        "alpha_labels": alpha,
        "beta_labels": beta,
        "phi_coefficients_ascending": phi,
        "core_locator_coefficients_ascending": core_locator,
        "w_coefficients_ascending": w,
        "codeword_coefficients_ascending": codeword,
        "degree": len(codeword) - 1,
        "degree_bound": core_size * 11,
        "core_retained_profile": point_profile,
        "retained_core": retained_core,
        "total_agreement": agreement,
        "listing_threshold": listing_threshold,
        "listing_surplus": agreement - listing_threshold,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "kernel_quotient_degree": kernel_degree,
        "single_point_deletions": deletable,
        "missed_core_traces": missed_traces,
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
    assert 1 <= D and target_m < 11
    generator = int(anchor["generator"])
    zeta = int(anchor["zeta"])
    subgroup = [pow(zeta, index, prime) for index in range(11)]
    used = set(anchor["core_quotient_indices"] + anchor["petal_quotient_indices"])
    new_indices = [index for index in range((prime - 1) // 11) if index not in used][:D]
    new_labels = [pow(generator, 11 * index, prime) for index in new_indices]
    Q = base.polynomial_from_roots_mod(new_labels, prime)
    padded_codeword = base.polynomial_multiply_mod(
        anchor["codeword_coefficients_ascending"],
        base.substitute_power(Q, 11),
        prime,
    )
    padded_core_locator = base.polynomial_multiply_mod(
        anchor["core_locator_coefficients_ascending"], Q, prime
    )
    assert len(padded_codeword) - 1 == int(anchor["degree"]) + 11 * D
    assert len(padded_codeword) - 1 <= target_m * 11
    positive_support = sorted(
        {
            exponent % 11
            for exponent, coefficient in enumerate(padded_codeword)
            if coefficient and exponent % 11
        }
    )
    assert positive_support == anchor["active_nonzero_DFT_sectors"]

    petal_profile = []
    for representative, scalar, label in zip(
        anchor["petal_representatives"],
        anchor["petal_scalars"],
        anchor["alpha_labels"],
    ):
        retained_here = 0
        for point in subgroup:
            x = representative * point % prime
            value = base.polynomial_evaluate_mod(padded_codeword, x, prime)
            received = (
                scalar
                * base.polynomial_evaluate_mod(
                    padded_core_locator, label, prime
                )
            ) % prime
            retained_here += value == received
        petal_profile.append(retained_here)
    assert petal_profile == [11] * tau

    retained = []
    missed = []
    core_profile = []
    core_representatives = anchor["core_representatives"] + [
        pow(generator, index, prime) for index in new_indices
    ]
    for representative in core_representatives:
        retained_here = 0
        for point in subgroup:
            x = representative * point % prime
            if base.polynomial_evaluate_mod(padded_codeword, x, prime) == 0:
                retained.append(x)
                retained_here += 1
            else:
                missed.append(x)
        core_profile.append(retained_here)
    assert core_profile == anchor["core_retained_profile"] + [11] * D
    assert sorted(missed) == anchor["exact_missed_core"]
    assert 11 <= len(missed) <= (tau - 1) * 11
    agreement = tau * 11 + len(retained)
    listing_threshold = (target_m + 1) * 11
    assert agreement >= listing_threshold

    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 11,
        "tau": tau,
        "m": target_m,
        "D": D,
        "base_m": base_m,
        "new_dead_core_quotient_indices": new_indices,
        "Q_coefficients_ascending": Q,
        "padded_core_locator_coefficients_ascending": padded_core_locator,
        "padded_codeword_coefficients_ascending": padded_codeword,
        "active_nonzero_DFT_sectors": anchor["active_nonzero_DFT_sectors"],
        "recomputed_positive_DFT_support": positive_support,
        "petal_scalars": anchor["petal_scalars"],
        "core_retained_profile": core_profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": listing_threshold,
        "listing_surplus": agreement - listing_threshold,
        "degree": len(padded_codeword) - 1,
        "degree_bound": target_m * 11,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "missed_core_identical_to_anchor": True,
        "H_stabilizer": stabilizer,
        "listed": True,
        "minimal": True,
        "primitive": True,
    }


def witness_family() -> dict[str, object]:
    anchors = [build_anchor(tau) for tau in (7, 8)]
    padded = []
    for anchor in anchors:
        for target_m in range(int(anchor["m"]) + 1, 11):
            padded.append(pad_anchor(anchor, target_m))
    assert {(row["tau"], row["m"]) for row in padded} == {
        (7, 9),
        (7, 10),
        (8, 10),
    }
    return {
        "field": "F_353",
        "anchors_D0": anchors,
        "D_positive_counterexamples": padded,
    }


def check_upstream() -> dict[str, object]:
    residual = UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    pv = UPSTREAM_PV.read_text(encoding="utf-8")
    reconstruction = UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    assert "The residual danger is `|S| >= 2`" in residual
    assert "all `ell-1` DFT sectors active" in pv
    assert "explicit BIJECTION" in reconstruction
    return {
        "sources": [
            UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            UPSTREAM_PV.relative_to(ROOT).as_posix(),
            UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "Upstream has general all-sector ell=11 spectrum witnesses and "
            "the full-petal reconstruction machinery, but no exact-three-"
            "sector D>0 classification, no robust partial-death cap, and no "
            "F_353 {1,5,9}-sector family."
        ),
    }


def main() -> None:
    cap_sieve = robust_live_cap_sieve()
    vacant = vacancy_rows()
    witnesses = witness_family()
    upstream = check_upstream()
    artifact = {
        "title": "ell=11 exact-three-sector D-positive grid classification",
        "status": "VACANCY_AND_COUNTEREXAMPLE_CLASSIFICATION",
        "verdict": "PASS_WITH_ELL11_EXACT_THREE_SECTOR_D_POSITIVE_GRID_CLASSIFIED",
        "theorem": (
            "Over every prime field supporting the full sunflower, all "
            "ell=11 exact-three-active-sector D>0 rows with tau=5 or 6 are "
            "vacant.  The remaining rows tau=7,8 are nonvacant: explicit "
            "primitive minimal listed words exist over F_353 for every "
            "tau<m<11."
        ),
        "robust_live_cap_sieve": cap_sieve,
        "uniform_vacancy_rows": vacant,
        "counterexample_family": witnesses,
        "proof": {
            "vacancy": (
                "All bad characteristics for the exact-three-sector cap 3 "
                "or partial two-sector cap 2 have fewer than 12 quotient "
                "labels and cannot realize any D>0 cell.  Thus c=3 is robust. "
                "For tau=5,6, common-root deficit theorem gives c(tau+2)<33 and "
                "S_(tau+1)<=3(tau+1)<22."
            ),
            "nonvacancy": (
                "At F_353, Gamma=X+345X^5+49X^9 has eight triple cosets. "
                "Lambda-free D=0 anchors at tau=7,8 are listed.  Multiplying "
                "the entire codeword and core locator by Q_D(X^11) preserves "
                "petal scalars and the exact primitive minimal missed core "
                "while adding D fully retained common-dead core cosets."
            ),
        },
        "parameter_grid": {
            "vacant": [[row["tau"], row["m"]] for row in vacant],
            "nonvacant": [
                [row["tau"], row["m"]]
                for row in witnesses["D_positive_counterexamples"]
            ],
        },
        "scope": (
            "Prime fields, ell=11, 5<=tau<m<11, D>0, background-free full "
            "petals, and exactly three active nonzero DFT sectors."
        ),
        "nonclaims": [
            "Nonvacancy at tau=7,8 is existential over F_353, not a statement for every prime.",
            "No classification is claimed for extension fields or four-plus active sectors.",
            "The D=0 anchors are included only to certify the D>0 propagation family.",
        ],
        "operation_counts": {
            "normalized_3x3_orbit_minors": 4,
            "normalized_4x4_orbit_minors": 16,
            "D_positive_vacancy_rows": len(vacant),
            "D0_anchor_witnesses": len(witnesses["anchors_D0"]),
            "D_positive_counterexamples": len(
                witnesses["D_positive_counterexamples"]
            ),
            "blind_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "Move to ell=13 exact-three-sector D>0 or the first exact-four-"
            "sector row.  Choose after comparing whether the AGL resultant "
            "tables still leave a theorem-scale availability gap."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=11 exact-three-sector D-positive grid")
    print(
        "minor_tables="
        + str(cap_sieve["two_sector_3x3_quotient_norm_table"])
        + "/"
        + str(cap_sieve["three_sector_4x4_quotient_norm_table"])
    )
    print(
        "vacant_rows="
        + str([(row["tau"], row["m"]) for row in vacant])
        + " min_gap="
        + str(min(int(row["strict_gap"]) for row in vacant))
    )
    print(
        "counterexamples="
        + str(
            [
                (row["tau"], row["m"], row["total_agreement"])
                for row in witnesses["D_positive_counterexamples"]
            ]
        )
    )
    print("PASS_WITH_ELL11_EXACT_THREE_SECTOR_D_POSITIVE_GRID_CLASSIFIED")


if __name__ == "__main__":
    main()
