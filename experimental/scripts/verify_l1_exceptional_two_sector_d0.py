#!/usr/bin/env python3
"""Exact certificate for the exceptional D=0 two-sector frontier.

The verifier never enumerates coefficient pairs independently on a core
coset.  It first classifies every projective three-root state by ranks of
3x3 evaluation matrices.  It then transports the two-sector coefficient
ratio through the quotient group F_p^*/mu_ell and enumerates only quotient
states.

It proves two deliberately different conclusions.

* Over F_2699, ell=19, every D=0 exact-two-active-sector word has retained
  core R<=30<38, hence is unlisted, for 12<=tau<m<19.
* Over F_1361, ell=17, the fixed sectors {1,11} and coefficient 81 give a
  global spectrum 1^60 2^10 3^10.  For every D=0 cell tau=11,...,15 the
  verifier assembles a full-petal listed word with distinct nonzero petal
  scalars, checks it point by point, and proves that its exact missed core is
  a primitive divisibility-minimal kernel set via the upstream bijection.

Nothing here claims a D>0 theorem or counterexample.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
ARTIFACT = DATA / "exceptional_two_sector_d0.json"

UPSTREAM_RECONSTRUCTION = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_general_reconstruction_collapse.md"
)
UPSTREAM_RESIDUAL = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_DAG = (
    ROOT
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)

EXPECTED_PROJECTIVE = {
    (17, 1361): {
        4: ((0, 2, 10), (1, 84, 1276), 1102, 1150, 876),
        5: ((0, 2, 8), (1, 392, 968), 129, 614, 845),
        7: ((0, 4, 11), (1, 1344, 16), 614, 129, 602),
        11: ((0, 4, 10), (1, 1097, 263), 747, 1093, 564),
        13: ((0, 2, 11), (1, 1153, 207), 1150, 1102, 1357),
        14: ((0, 2, 9), (1, 844, 516), 1093, 747, 685),
    },
    (19, 2699): {
        4: ((0, 3, 7), (1, 2056, 642), 1838, 904, 258),
        5: ((0, 3, 10), (1, 2197, 501), 904, 1838, 676),
        6: ((0, 2, 9), (1, 339, 2359), 861, 1652, 170),
        14: ((0, 2, 12), (1, 2241, 457), 1047, 2284, 2555),
        15: ((0, 3, 12), (1, 2358, 340), 2284, 1047, 156),
        16: ((0, 3, 15), (1, 2055, 643), 1652, 861, 2473),
    },
}

EXPECTED_ELL19_FRONTIER_HISTOGRAMS = {
    ((1, 132), (2, 8), (3, 2)),
    ((1, 135), (2, 6), (3, 1)),
    ((1, 136), (2, 5), (3, 1)),
    ((1, 138), (2, 4)),
    ((1, 140), (2, 2)),
}


def prime_factors(value: int) -> list[int]:
    output = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            output.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        output.append(value)
    return output


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(rank, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(value * inverse) % prime for value in work[rank]]
        for row in range(row_count):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == min(row_count, column_count):
            break
    return rank


def null_vector_three(matrix: list[list[int]], prime: int) -> list[int]:
    first, second = matrix[0], matrix[1]
    vector = [
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    ]
    vector = [entry % prime for entry in vector]
    assert any(vector)
    assert all(
        sum(entry * coefficient for entry, coefficient in zip(row, vector))
        % prime
        == 0
        for row in matrix
    )
    return vector


def affine_canonical(ell: int, support: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((unit * exponent + shift) % ell for exponent in support))
        for unit in range(1, ell)
        for shift in range(ell)
    )


def polynomial_multiply(
    first: list[int], second: list[int], prime: int
) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] = (
                output[first_index + second_index]
                + first_value * second_value
            ) % prime
    return output


def locator(labels: list[int], prime: int) -> list[int]:
    output = [1]
    for label in labels:
        output = polynomial_multiply(output, [(-label) % prime, 1], prime)
    return output


def polynomial_evaluate(polynomial: list[int], point: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % prime
    return value


def interpolate(xs: list[int], ys: list[int], prime: int) -> list[int]:
    assert len(xs) == len(ys) == len(set(xs))
    output = [0] * len(xs)
    for index, point in enumerate(xs):
        basis = [1]
        denominator = 1
        for other_index, other in enumerate(xs):
            if other_index == index:
                continue
            basis = polynomial_multiply(basis, [(-other) % prime, 1], prime)
            denominator = denominator * (point - other) % prime
        scale = ys[index] * pow(denominator, -1, prime) % prime
        for coefficient_index, coefficient in enumerate(basis):
            output[coefficient_index] = (
                output[coefficient_index] + scale * coefficient
            ) % prime
    assert all(
        polynomial_evaluate(output, point, prime) == value
        for point, value in zip(xs, ys)
    )
    return output


def projective_three_root_states(
    ell: int, prime: int, ratios: list[int]
) -> dict[str, object]:
    generator = primitive_root(prime)
    quotient_size = (prime - 1) // ell
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    rows = []
    rank_tests = 0

    for exponent_ratio in ratios:
        evaluations = [
            [1, point, pow(point, exponent_ratio, prime)] for point in subgroup
        ]
        singular = []
        normalized_states = []
        root_counts = []
        for indices in itertools.combinations(range(ell), 3):
            matrix = [evaluations[index] for index in indices]
            rank = matrix_rank_mod(matrix, prime)
            rank_tests += 1
            if rank == 3:
                continue
            assert rank == 2
            vector = null_vector_three(matrix, prime)
            assert all(vector), "a coefficient-zero boundary is not a trinomial"
            inverse = pow(vector[0], -1, prime)
            state = tuple(entry * inverse % prime for entry in vector)
            roots = [
                index
                for index, row in enumerate(evaluations)
                if sum(entry * coefficient for entry, coefficient in zip(row, state))
                % prime
                == 0
            ]
            # This also excludes every four-root polynomial: any such polynomial
            # contains a singular triple, whose unique null state is tested here.
            assert len(roots) == 3 and tuple(roots) == indices
            singular.append(indices)
            normalized_states.append(state)
            root_counts.append(len(roots))

        assert len(singular) == ell
        assert len(set(normalized_states)) == ell
        invariants = set()
        for _constant, linear, high in normalized_states:
            invariant_t = pow(linear, ell, prime)
            invariant_u = pow(high, ell, prime)
            invariant_j = (
                pow(linear, exponent_ratio, prime) * pow(high, -1, prime)
            ) % prime
            invariants.add((invariant_t, invariant_u, invariant_j))
        assert len(invariants) == 1
        invariant_t, invariant_u, invariant_j = next(iter(invariants))

        representative = (
            tuple(singular[0]),
            tuple(normalized_states[0]),
            invariant_t,
            invariant_u,
            invariant_j,
        )
        assert representative == EXPECTED_PROJECTIVE[(ell, prime)][exponent_ratio]
        rows.append(
            {
                "exponent_ratio": exponent_ratio,
                "singular_triples": len(singular),
                "representative_root_indices": list(singular[0]),
                "representative_coefficients_A_B_C": list(normalized_states[0]),
                "T_equals_B_over_A_to_ell": invariant_t,
                "U_equals_C_over_A_to_ell": invariant_u,
                "J_equals_B_to_e_over_A_to_e_minus_1_C": invariant_j,
                "U_over_T": invariant_u * pow(invariant_t, -1, prime) % prime,
                "all_states_one_projective_rotation_orbit": True,
                "exact_root_count": min(root_counts),
            }
        )

    return {
        "ell": ell,
        "p": prime,
        "generator": generator,
        "zeta": zeta,
        "quotient_size": quotient_size,
        "rank_tests_3x3": rank_tests,
        "rows": rows,
        "state_criterion": (
            "For normalized A+B*h+C*h^e with A*B*C nonzero, exact three "
            "roots occur iff B^ell=T*A^ell, C^ell=U*A^ell, and "
            "B^e=J*A^(e-1)*C for the displayed row."
        ),
    }


def quotient_mu_table(
    ell: int,
    prime: int,
    generator: int,
    sector_r: int,
    sector_s: int,
) -> list[int]:
    quotient_size = (prime - 1) // ell
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    powers_r = [pow(point, sector_r, prime) for point in subgroup]
    powers_s = [pow(point, sector_s, prime) for point in subgroup]
    output = []
    for quotient_exponent in range(quotient_size):
        coefficient = pow(generator, quotient_exponent, prime)
        values = [
            (first + coefficient * second) % prime
            for first, second in zip(powers_r, powers_s)
        ]
        output.append(max(Counter(values).values()))
    return output


def spectrum_from_state_table(
    state_mu: list[int], quotient_shift: int, difference: int
) -> list[int]:
    quotient_size = len(state_mu)
    return [
        state_mu[(quotient_shift + difference * coset_index) % quotient_size]
        for coset_index in range(quotient_size)
    ]


def enumerate_global_spectra(
    ell: int,
    prime: int,
    restrict_canonical: tuple[int, ...] | None = None,
) -> dict[str, object]:
    generator = primitive_root(prime)
    quotient_size = (prime - 1) // ell
    pairs = [
        (sector_r, sector_s)
        for sector_r in range(1, ell)
        for sector_s in range(sector_r + 1, ell)
        if restrict_canonical is None
        or affine_canonical(ell, (0, sector_r, sector_s)) == restrict_canonical
    ]
    histogram_set = set()
    quotient_state_rows = 0
    maximum_bonus = -1
    maximum_bonus_row = None
    maximum_top = {m: (-1, None) for m in range(1, ell)}

    for sector_r, sector_s in pairs:
        difference = sector_s - sector_r
        state_mu = quotient_mu_table(
            ell, prime, generator, sector_r, sector_s
        )
        # Shifts in the same residue class modulo gcd(d,N) produce a
        # permutation of the quotient labels, so these are all spectra.
        for quotient_shift in range(math.gcd(difference, quotient_size)):
            spectrum = spectrum_from_state_table(
                state_mu, quotient_shift, difference
            )
            quotient_state_rows += 1
            histogram = tuple(sorted(Counter(spectrum).items()))
            histogram_set.add(histogram)
            bonus = sum(max(0, multiplicity - 1) for multiplicity in spectrum)
            if bonus > maximum_bonus:
                maximum_bonus = bonus
                maximum_bonus_row = (
                    sector_r,
                    sector_s,
                    quotient_shift,
                    histogram,
                )
            ordered = sorted(spectrum, reverse=True)
            for core_size in maximum_top:
                top = sum(ordered[:core_size])
                if top > maximum_top[core_size][0]:
                    maximum_top[core_size] = (
                        top,
                        (sector_r, sector_s, quotient_shift, histogram),
                    )

    return {
        "pair_count": len(pairs),
        "quotient_state_rows": quotient_state_rows,
        "histograms": [
            [[multiplicity, count] for multiplicity, count in histogram]
            for histogram in sorted(histogram_set)
        ],
        "maximum_bonus_sum_mu_minus_1": maximum_bonus,
        "maximum_bonus_witness": {
            "sector_r": maximum_bonus_row[0],
            "sector_s": maximum_bonus_row[1],
            "quotient_shift": maximum_bonus_row[2],
            "histogram": [list(pair) for pair in maximum_bonus_row[3]],
        },
        "maximum_top_by_core_size": {
            str(core_size): {
                "top": row[0],
                "sector_r": row[1][0],
                "sector_s": row[1][1],
                "quotient_shift": row[1][2],
                "histogram": [list(pair) for pair in row[1][3]],
            }
            for core_size, row in maximum_top.items()
        },
        "histogram_set_raw": histogram_set,
    }


def polynomial_full_evaluate(
    point: int,
    ell: int,
    prime: int,
    p0: list[int],
    phi: list[int],
    active_coefficient: int,
) -> int:
    label = pow(point, ell, prime)
    return (
        polynomial_evaluate(p0, label, prime)
        + polynomial_evaluate(phi, label, prime)
        * (point + active_coefficient * pow(point, 11, prime))
    ) % prime


def build_ell17_witnesses() -> dict[str, object]:
    ell = 17
    prime = 1361
    generator = primitive_root(prime)
    assert generator == 3
    quotient_size = (prime - 1) // ell
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    sector_r, sector_s = 1, 11
    quotient_shift = 4
    active_coefficient = pow(generator, quotient_shift, prime)
    assert active_coefficient == 81
    difference = sector_s - sector_r
    state_mu = quotient_mu_table(
        ell, prime, generator, sector_r, sector_s
    )
    spectrum = spectrum_from_state_table(
        state_mu, quotient_shift, difference
    )
    histogram = tuple(sorted(Counter(spectrum).items()))
    assert histogram == ((1, 60), (2, 10), (3, 10))
    order = sorted(range(quotient_size), key=lambda index: (-spectrum[index], index))

    cells = []
    for tau in range(11, 16):
        core_size = tau + 1
        assert core_size < ell
        core_indices = order[:core_size]
        petal_indices = [
            index
            for index in range(quotient_size)
            if index not in core_indices
        ][:tau]
        assert len(set(core_indices + petal_indices)) == core_size + tau
        core_labels = [pow(generator, ell * index, prime) for index in core_indices]
        petal_labels = [pow(generator, ell * index, prime) for index in petal_indices]
        phi = locator(petal_labels, prime)
        core_locator = locator(core_labels, prime)
        assert len(phi) == tau + 1 and len(core_locator) == core_size + 1

        target_constants = []
        root_indices = []
        root_values = []
        profile = []
        for index in core_indices:
            representative = pow(generator, index, prime)
            values = [
                (
                    representative * point
                    + active_coefficient
                    * pow(representative * point, sector_s, prime)
                )
                % prime
                for point in subgroup
            ]
            counts = Counter(values)
            maximum = max(counts.values())
            level = min(value for value, count in counts.items() if count == maximum)
            roots = [i for i, value in enumerate(values) if value == level]
            target_constants.append((-level) % prime)
            root_indices.append(roots)
            root_values.append(
                [(representative * subgroup[i]) % prime for i in roots]
            )
            profile.append(maximum)
        assert profile == [3] * 10 + [2] * (core_size - 10)

        interpolation_values = [
            constant * polynomial_evaluate(phi, label, prime) % prime
            for constant, label in zip(target_constants, core_labels)
        ]
        p0_base = interpolate(core_labels, interpolation_values, prime)
        base_scalars = [
            polynomial_evaluate(p0_base, label, prime)
            * pow(polynomial_evaluate(core_locator, label, prime), -1, prime)
            % prime
            for label in petal_labels
        ]
        assert len(set(base_scalars)) == tau
        shift = 1
        scalars = [(scalar + shift) % prime for scalar in base_scalars]
        assert all(scalars) and len(set(scalars)) == tau
        p0 = p0_base + [0] * (len(core_locator) - len(p0_base))
        p0 = [
            (coefficient + shift * locator_coefficient) % prime
            for coefficient, locator_coefficient in zip(p0, core_locator)
        ]

        petal_agreements = []
        for index, scalar in zip(petal_indices, scalars):
            representative = pow(generator, index, prime)
            agreement = 0
            for point in subgroup:
                x = representative * point % prime
                received = (
                    scalar
                    * polynomial_evaluate(core_locator, pow(x, ell, prime), prime)
                ) % prime
                agreement += polynomial_full_evaluate(
                    x,
                    ell,
                    prime,
                    p0,
                    phi,
                    active_coefficient,
                ) == received
            petal_agreements.append(agreement)
        assert petal_agreements == [ell] * tau

        exact_core_profile = []
        missed_core = set()
        agreement_core = set()
        for index in core_indices:
            representative = pow(generator, index, prime)
            zeros = []
            for point in subgroup:
                x = representative * point % prime
                if (
                    polynomial_full_evaluate(
                        x,
                        ell,
                        prime,
                        p0,
                        phi,
                        active_coefficient,
                    )
                    == 0
                ):
                    zeros.append(x)
                    agreement_core.add(x)
                else:
                    missed_core.add(x)
            exact_core_profile.append(len(zeros))
        assert exact_core_profile == profile

        retained = sum(profile)
        listing_threshold = (core_size + 1) * ell
        total_agreement = tau * ell + retained
        missed_size = core_size * ell - retained
        assert retained >= 2 * ell
        assert total_agreement >= listing_threshold
        assert ell <= missed_size <= (tau - 1) * ell

        # P0(X^ell) has sector zero.  The two monic nonzero terms
        # phi(X^ell)X and 81 phi(X^ell)X^11 give active S={1,11}.
        degree_p0 = max(
            degree * ell for degree, coefficient in enumerate(p0) if coefficient
        )
        degree_sector_r = tau * ell + sector_r
        degree_sector_s = tau * ell + sector_s
        degree = max(degree_p0, degree_sector_r, degree_sector_s)
        assert degree <= core_size * ell

        stabilizer = []
        for multiplier in subgroup:
            if {multiplier * point % prime for point in missed_core} == missed_core:
                stabilizer.append(multiplier)
        assert stabilizer == [1]

        # Anchor the independently verified first cell, including the corrected
        # degree-12 core locator (one must not insert an extra zero).
        if tau == 11:
            assert core_indices == [2, 10, 18, 26, 34, 42, 50, 58, 66, 74, 7, 15]
            assert petal_indices == [0, 1, 3, 4, 5, 6, 8, 9, 11, 12, 13]
            assert phi == [969, 135, 357, 798, 1215, 619, 65, 692, 313, 726, 915, 1]
            assert core_locator == [1136, 1173, 614, 0, 0, 0, 0, 0, 0, 0, 689, 1108, 1]
            assert p0 == [829, 1337, 1168, 629, 167, 100, 864, 855, 486, 449, 747, 943, 1]
            assert scalars == [839, 807, 547, 188, 56, 1286, 1002, 774, 589, 1076, 479]

        cells.append(
            {
                "tau": tau,
                "m": core_size,
                "D": 0,
                "core_quotient_indices": core_indices,
                "petal_quotient_indices": petal_indices,
                "core_beta_labels": core_labels,
                "petal_alpha_labels": petal_labels,
                "phi_coefficients_ascending": phi,
                "Lambda_coefficients_ascending": core_locator,
                "P0_coefficients_ascending": p0,
                "petal_scalars": scalars,
                "target_A_equals_P0_over_phi_on_core": target_constants,
                "core_root_indices": root_indices,
                "core_root_values": root_values,
                "core_zero_profile": profile,
                "retained_core": retained,
                "petal_agreement": tau * ell,
                "total_agreement": total_agreement,
                "listing_threshold": listing_threshold,
                "listed": True,
                "degree": degree,
                "degree_bound": core_size * ell,
                "exact_missed_core_size": missed_size,
                "minimal_kernel_range_upper": (tau - 1) * ell,
                "active_nonzero_DFT_sectors": [sector_r, sector_s],
                "full_DFT_support_including_sector_zero": [0, sector_r, sector_s],
                "H_stabilizer_of_exact_missed_core": stabilizer,
                "primitive": True,
                "minimality": (
                    "The upstream full-petal reconstruction bijection applies: "
                    "the scalars are distinct and nonzero, the word is listed "
                    "and full-petal, and its exact missed core lies in "
                    "[ell,(tau-1)ell].  Therefore that exact missed core is a "
                    "divisibility-minimal kernel set."
                ),
            }
        )

    return {
        "ell": ell,
        "p": prime,
        "generator": generator,
        "zeta": zeta,
        "quotient_size": quotient_size,
        "sector_r": sector_r,
        "sector_s": sector_s,
        "active_coefficient_for_sector_s": active_coefficient,
        "quotient_shift": quotient_shift,
        "global_spectrum_histogram": [list(pair) for pair in histogram],
        "cells": cells,
    }


def check_upstream() -> dict[str, object]:
    assert UPSTREAM_RECONSTRUCTION.exists()
    assert UPSTREAM_RESIDUAL.exists()
    assert UPSTREAM_DAG.exists()
    reconstruction_text = UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    residual_text = UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    dag_text = UPSTREAM_DAG.read_text(encoding="utf-8")
    assert "explicit BIJECTION" in reconstruction_text
    assert "pma_wide_residual" in dag_text
    assert "The residual danger is `|S| >= 2`" in residual_text
    return {
        "reconstruction_source": UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
        "residual_source": UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
        "dag_source": UPSTREAM_DAG.relative_to(ROOT).as_posix(),
        "collision": (
            "No p=1361 exact-two-active-sector global witness and no p=2699 "
            "D=0 quotient-state vacancy theorem were found in the cited "
            "upstream sources.  Upstream retains the "
            "two-or-more-sector/pma_wide_residual target."
        ),
    }


def main() -> None:
    upstream = check_upstream()

    projective_17 = projective_three_root_states(
        17, 1361, [4, 5, 7, 11, 13, 14]
    )
    projective_19 = projective_three_root_states(
        19, 2699, [4, 5, 6, 14, 15, 16]
    )

    ell19_canonical = affine_canonical(19, (0, 1, 4))
    ell19_frontier = enumerate_global_spectra(
        19, 2699, restrict_canonical=ell19_canonical
    )
    assert ell19_frontier["pair_count"] == 54
    assert ell19_frontier["histogram_set_raw"] == EXPECTED_ELL19_FRONTIER_HISTOGRAMS
    assert ell19_frontier["maximum_bonus_sum_mu_minus_1"] == 12

    # The total D=0 theorem is stronger than the residual-only calculation:
    # enumerate all C(18,2)=153 exact nonzero sector pairs.
    ell19_all = enumerate_global_spectra(19, 2699)
    assert ell19_all["pair_count"] == math.comb(18, 2)
    ell19_top_rows = []
    for tau in range(12, 18):
        core_size = tau + 1
        maximum = ell19_all["maximum_top_by_core_size"][str(core_size)]["top"]
        assert maximum == core_size + 12
        assert maximum <= 30 < 2 * 19
        ell19_top_rows.append(
            {
                "tau": tau,
                "m": core_size,
                "D": 0,
                "maximum_retained_core": maximum,
                "listing_requires": 38,
                "gap": 38 - maximum,
                "vacant": True,
            }
        )

    ell17_witnesses = build_ell17_witnesses()
    assert [cell["retained_core"] for cell in ell17_witnesses["cells"]] == [
        34,
        36,
        38,
        40,
        42,
    ]

    # Remove internal set-valued helpers before JSON serialization.
    ell19_frontier.pop("histogram_set_raw")
    ell19_all.pop("histogram_set_raw")
    artifact = {
        "title": "Exceptional D=0 two-sector cross-coset coupling",
        "status": "PROVED_MIXED_VERDICT",
        "verdict": "PASS_WITH_ELL19_D0_VACANCY_AND_ELL17_GLOBAL_COUNTEREXAMPLES",
        "scope": (
            "Prime fields, background-free full-petal words, exactly two "
            "active nonzero DFT sectors, and D=m-tau-1=0 only.  No D>0 "
            "statement is made."
        ),
        "global_coefficient_form": {
            "definition": (
                "On core coset b_j*mu_ell, beta_j=b_j^ell, write "
                "A_j=P0(beta_j)/phi(beta_j), "
                "B_j=b_j^r*g_r(beta_j), C_j=b_j^s*g_s(beta_j)."
            ),
            "normalized_ratio": "e=s*r^{-1} modulo ell",
            "three_root_equations": [
                "B_j^ell=T_e*A_j^ell",
                "C_j^ell=U_e*A_j^ell",
                "B_j^e=J_e*A_j^(e-1)*C_j",
            ],
            "ratio_consequence": (
                "beta_j^(s-r)*(g_s(beta_j)/g_r(beta_j))^ell=U_e/T_e"
            ),
            "D0_consequence": (
                "When g_r,g_s are constants, the number of three-root core "
                "labels is at most gcd(s-r,(p-1)/ell).  Double-root states "
                "are enumerated exactly in the quotient group."
            ),
        },
        "projective_three_root_classification": [projective_17, projective_19],
        "ell19_D0_total_vacancy": {
            "theorem": (
                "Over F_2699 with ell=19, every background-free full-petal "
                "D=0 word with exactly two active nonzero sectors and "
                "12<=tau<m<19 is unlisted."
            ),
            "frontier_orbit_spectra": ell19_frontier,
            "all_sector_pair_spectra": ell19_all,
            "cells": ell19_top_rows,
        },
        "ell17_D0_global_counterexample_family": {
            "theorem": (
                "Over F_1361 with ell=17, each D=0 cell "
                "tau=11,...,15, m=tau+1 has an explicit listed full-petal "
                "word with active nonzero sectors {1,11}; its exact missed "
                "core is a primitive divisibility-minimal kernel set."
            ),
            **ell17_witnesses,
        },
        "proof_steps": [
            "Rank every 3x3 subgroup evaluation matrix in the exceptional orbit. Exactly ell singular triples occur, all rank two and all in one projective-rotation orbit; evaluating every null state gives exactly three roots and excludes four-root states.",
            "Record the complete projective invariants T,U,J. Substitution of the global sector coefficients gives the displayed beta/g_r/g_s coupling equations.",
            "At D=0 identify F_p^*/mu_ell with quotient exponents. For sector difference d, quotient shifts modulo gcd(d,N) exhaust all spectra; no coefficient-pair search per coset occurs.",
            "For ell=19 enumerate all 153 nonzero-sector pairs. The exact maximum top-m is m+12 for m=13,...,18, hence at most 30<38.",
            "For ell=17 the fixed pair {1,11} and coefficient 81 has spectrum 1^60 2^10 3^10. Select the top m quotient labels and interpolate P0 on the core independently for each of the five cells.",
            "Evaluate every petal and core point, check degree, exact DFT support, scalar distinctness/nonzeroness, listing, exact missed-core size, and trivial H-stabilizer. Invoke the upstream full-petal bijection only after all its hypotheses are checked.",
        ],
        "operation_counts": {
            "projective_3x3_rank_tests": projective_17["rank_tests_3x3"]
            + projective_19["rank_tests_3x3"],
            "ell19_all_sector_pairs": ell19_all["pair_count"],
            "ell19_quotient_state_rows": ell19_all["quotient_state_rows"],
            "coefficient_pair_enumerations_per_coset": 0,
            "ell17_pointwise_witness_cells": 5,
        },
        "upstream": upstream,
        "next_obligation": (
            "Return to the exceptional frontier with D>0.  The ratio "
            "equation becomes a rational-function incidence in g_s/g_r; "
            "the present finite D=0 spectra must not be extrapolated."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("Exceptional D=0 two-sector cross-coset coupling")
    print("ell19_top_m=" + str([row["maximum_retained_core"] for row in ell19_top_rows]))
    print(
        "ell17_retained="
        + str([cell["retained_core"] for cell in ell17_witnesses["cells"]])
    )
    print(
        "ell17_anchor_agreement="
        + str(ell17_witnesses["cells"][0]["total_agreement"])
        + " missed="
        + str(ell17_witnesses["cells"][0]["exact_missed_core_size"])
    )
    print(
        f"rank_tests={artifact['operation_counts']['projective_3x3_rank_tests']} "
        f"quotient_rows={ell19_all['quotient_state_rows']}"
    )
    print("PASS_WITH_ELL19_D0_VACANCY_AND_ELL17_GLOBAL_COUNTEREXAMPLES")


if __name__ == "__main__":
    main()
