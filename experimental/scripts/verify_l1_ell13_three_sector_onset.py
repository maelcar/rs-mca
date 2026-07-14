#!/usr/bin/env python3
"""Complete ell=13 exact-three-sector D>0 prime-field grid.

Rows tau=5,6,7 are universally vacant.  Rows tau=8,9,10 are nonvacant,
witnessed over F_521 by Gamma=X+167X^5+371X^9 and exact common-factor
padding.  All arithmetic is deterministic and exact.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import verify_l1_ell7_three_sector_counterexample as base
import verify_l1_ell11_three_sector_onset as ell11


ELL = 13
BAD_PRIMES = [53, 79, 157, 521, 599, 1327]
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
ARTIFACT = DATA / "ell13_three_sector_onset.json"
UPSTREAM = ROOT
UPSTREAM_RESIDUAL = UPSTREAM / "experimental/notes/l1/l1_coset_mixed_vacancy_threshold.md"
UPSTREAM_PV = UPSTREAM / "experimental/notes/l1/l1_prime_ell_pv_refutation.md"
UPSTREAM_RECONSTRUCTION = UPSTREAM / "experimental/notes/l1/l1_general_reconstruction_collapse.md"


# Exact Z[zeta_13] norm engine.
Ring = tuple[int, ...]
ZERO: Ring = (0,) * 12


def ring_power(exponent: int) -> Ring:
    residue = exponent % 13
    if residue == 12:
        return (-1,) * 12
    output = [0] * 12
    output[residue] = 1
    return tuple(output)


def ring_add(first: Ring, second: Ring) -> Ring:
    return tuple(first[index] + second[index] for index in range(12))


def ring_mul(first: Ring, second: Ring) -> Ring:
    output = ZERO
    for i, first_value in enumerate(first):
        if not first_value:
            continue
        for j, second_value in enumerate(second):
            if second_value:
                term = tuple(
                    first_value * second_value * value
                    for value in ring_power(i + j)
                )
                output = ring_add(output, term)
    return output


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
    columns = [ring_mul(value, ring_power(index)) for index in range(12)]
    matrix = [
        [columns[column][row] for column in range(12)] for row in range(12)
    ]
    return base.bareiss_determinant(matrix)


def affine_canonical(support: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((unit * entry + shift) % 13 for entry in support))
        for unit in range(1, 13)
        for shift in range(13)
    )


def orbit_representatives(size: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            affine_canonical(support)
            for support in itertools.combinations(range(13), size)
        }
    )


def normalized_norm(exponents: tuple[int, ...], roots: tuple[int, ...]) -> int:
    determinant = base.alternant_polynomial(exponents, roots)
    vandermonde = base.vandermonde_polynomial(roots)
    quotient = base.integer_poly_exact_division(determinant, vandermonde)
    determinant_norm = abs(ring_norm(polynomial_to_ring(determinant)))
    vandermonde_norm = abs(ring_norm(polynomial_to_ring(vandermonde)))
    quotient_norm = abs(ring_norm(polynomial_to_ring(quotient)))
    pairs = len(roots) * (len(roots) - 1) // 2
    assert vandermonde_norm == 13**pairs
    assert determinant_norm == vandermonde_norm * quotient_norm
    return quotient_norm


def resultant_tables() -> dict[str, object]:
    reps3 = orbit_representatives(3)
    reps4 = orbit_representatives(4)
    assert reps3 == [(0, 1, 2), (0, 1, 3), (0, 1, 4)]
    assert reps4 == [
        (0, 1, 2, 3),
        (0, 1, 2, 4),
        (0, 1, 2, 5),
        (0, 1, 2, 6),
        (0, 1, 3, 4),
        (0, 1, 3, 9),
        (0, 1, 3, 11),
    ]
    table3 = [[normalized_norm(first, second) for second in reps3] for first in reps3]
    table4 = [[normalized_norm(first, second) for second in reps4] for first in reps4]
    assert table3 == [[1, 1, 1], [1, 53, 27], [1, 27, 729]]
    assert table4 == [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 79, 157, 53, 1, 729, 1],
        [1, 157, 599, 521, 1, 27, 1],
        [1, 53, 521, 1327, 1, 729, 625],
        [1, 1, 1, 1, 2809, 729, 625],
        [1, 729, 27, 729, 729, 19683, 4096],
        [1, 1, 1, 625, 625, 4096, 625],
    ]
    admissible = sorted(
        {
            prime
            for value in {entry for row in table4 for entry in row}
            for prime in base.prime_factors(value)
            if prime % 13 == 1
        }
    )
    assert admissible == BAD_PRIMES
    return {
        "three_subset_representatives": [list(row) for row in reps3],
        "four_subset_representatives": [list(row) for row in reps4],
        "two_live_3x3_table": table3,
        "three_live_4x4_table": table4,
        "bad_admissible_primes": admissible,
    }


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    return base.matrix_rank_mod(matrix, prime)


def null_four(matrix: list[list[int]], prime: int) -> list[int]:
    # A rank-three 4x4 matrix: cofactors of its first three rows.
    first_three = matrix[:3]
    output = []
    for omitted in range(4):
        minor = [
            [row[column] for column in range(4) if column != omitted]
            for row in first_three
        ]
        output.append(
            ((-1) ** omitted * base.determinant_three_mod(minor, prime)) % prime
        )
    assert any(output)
    return output


def gamma_spectrum_13(
    prime: int,
    generator: int,
    subgroup: list[int],
    support: tuple[int, int, int],
    gamma: list[int],
) -> list[int]:
    output = []
    for label_index in range((prime - 1) // 13):
        representative = pow(generator, label_index, prime)
        values = [
            sum(
                coefficient * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(gamma, support)
            )
            % prime
            for point in subgroup
        ]
        output.append(max(Counter(values).values()))
    return output


def bad_prime_state_audit() -> dict[str, object]:
    rows = []
    quadruple_reps = sorted(
        {
            min(
                tuple(sorted((entry + shift) % 13 for entry in support))
                for shift in range(13)
            )
            for support in itertools.combinations(range(13), 4)
        }
    )
    assert len(quadruple_reps) == 55
    for prime in BAD_PRIMES:
        generator = base.primitive_root(prime)
        quotient_size = (prime - 1) // 13
        zeta = pow(generator, quotient_size, prime)
        subgroup = [pow(zeta, index, prime) for index in range(13)]
        maximum_top = {size: 3 * size for size in (6, 7, 8)}
        maximum_fiber = 3
        singular_states = 0
        for support in itertools.combinations(range(1, 13), 3):
            exponents = (0,) + support
            for roots in quadruple_reps:
                matrix = [
                    [pow(zeta, root * exponent, prime) for exponent in exponents]
                    for root in roots
                ]
                if matrix_rank_mod(matrix, prime) == 4:
                    continue
                state = null_four(matrix, prime)
                assert all(
                    sum(entry * coefficient for entry, coefficient in zip(row, state))
                    % prime
                    == 0
                    for row in matrix
                ), (prime, support, roots, state)
                if not all(state[index] for index in (1, 2, 3)):
                    continue
                inverse = pow(state[1], -1, prime)
                gamma = [state[index] * inverse % prime for index in (1, 2, 3)]
                spectrum = gamma_spectrum_13(
                    prime, generator, subgroup, support, gamma
                )
                maximum_fiber = max(maximum_fiber, max(spectrum))
                ordered = sorted(spectrum, reverse=True)
                for size in maximum_top:
                    maximum_top[size] = max(
                        maximum_top[size], sum(ordered[: min(size, quotient_size)])
                    )
                singular_states += 1
        assert maximum_fiber <= 4
        rows.append(
            {
                "p": prime,
                "quotient_cosets": quotient_size,
                "minimum_grid_labels": 12,
                "available_somewhere": quotient_size >= 12,
                "singular_projective_states": singular_states,
                "maximum_fiber": maximum_fiber,
                "top_bounds_6_7_8": [maximum_top[size] for size in (6, 7, 8)],
            }
        )
    return {
        "rows": rows,
        "available_bad_primes": [
            row["p"] for row in rows if row["available_somewhere"]
        ],
    }


def vacancy_rows(audit: dict[str, object]) -> list[dict[str, object]]:
    # Generic characteristics have cap 3. Bad characteristics have cap 4,
    # but their exact proportional top-8 audit is <=24.
    rows = []
    for tau in (5, 6, 7):
        h = tau + 1
        for core_size in range(tau + 2, 13):
            D = core_size - tau - 1
            required_labels = tau + core_size
            proportional_top = 3 * h
            for bad_row in audit["rows"]:
                if bad_row["quotient_cosets"] >= required_labels:
                    proportional_top = max(
                        proportional_top,
                        bad_row["top_bounds_6_7_8"][h - 6],
                    )
            listing = (D + 2) * 13
            nonsaturated = (D - 1) * 13 + 4 * (tau + 2)
            saturated = D * 13 + proportional_top
            compiler = max(nonsaturated, saturated)
            assert compiler < listing, (
                tau,
                core_size,
                proportional_top,
                nonsaturated,
                saturated,
                listing,
            )
            rows.append(
                {
                    "tau": tau,
                    "m": core_size,
                    "D": D,
                    "robust_cap": 4,
                    "nonsaturated_bound": nonsaturated,
                    "proportional_top_bound": proportional_top,
                    "required_quotient_labels": required_labels,
                    "saturated_bound": saturated,
                    "listing_requirement": listing,
                    "strict_gap": listing - compiler,
                    "vacant": True,
                }
            )
    assert len(rows) == 15
    assert min(row["strict_gap"] for row in rows) == 2
    return rows


def build_anchor(tau: int) -> dict[str, object]:
    prime = 521
    core_size = tau + 1
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 13
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(13)]
    support = (1, 5, 9)
    active_gamma = [1, 167, 371]
    quotient_rows = []
    for index in range(quotient_size):
        representative = pow(generator, index, prime)
        values = [
            sum(
                coefficient * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(active_gamma, support)
            ) % prime
            for point in subgroup
        ]
        counts = Counter(values)
        multiplicity = max(counts.values())
        level = min(value for value, count in counts.items() if count == multiplicity)
        quotient_rows.append((multiplicity, index, representative, level))
    quotient_rows.sort(key=lambda row: (-row[0], row[1]))
    assert Counter(row[0] for row in quotient_rows) == Counter({1: 28, 2: 4, 3: 8})
    selected = quotient_rows[:core_size]
    core_indices = [row[1] for row in selected]
    core_representatives = [row[2] for row in selected]
    target_levels = [row[3] for row in selected]
    profile = [row[0] for row in selected]
    beta = [pow(value, 13, prime) for value in core_representatives]
    core_locator = base.polynomial_from_roots_mod(beta, prime)
    available_petals = [
        index for index in range(quotient_size) if index not in core_indices
    ]
    solved = None
    for shift in range(len(available_petals) - tau + 1):
        candidate_indices = available_petals[shift : shift + tau]
        candidate_representatives = [
            pow(generator, index, prime) for index in candidate_indices
        ]
        candidate_alpha = [
            pow(value, 13, prime) for value in candidate_representatives
        ]
        try:
            solution = ell11.solve_level_system(
                prime,
                candidate_alpha,
                beta,
                core_locator,
                target_levels,
            )
        except AssertionError:
            continue
        solved = (
            candidate_indices,
            candidate_representatives,
            candidate_alpha,
            solution,
        )
        break
    assert solved is not None
    petal_indices, petal_representatives, alpha, solution = solved
    petal_values, u_value, v_value, scalars, lambda_rank = solution
    assert len(set(alpha + beta)) == tau + core_size
    phi = base.polynomial_from_roots_mod(alpha, prime)
    w = base.polynomial_interpolate_mod(alpha, petal_values, prime)
    gamma_polynomial = [u_value] + [0] * 9
    gamma_polynomial[1], gamma_polynomial[5], gamma_polynomial[9] = active_gamma
    if v_value:
        gamma_polynomial += [0] * (14 - len(gamma_polynomial))
        gamma_polynomial[13] = v_value
    codeword = base.polynomial_add_mod(
        base.substitute_power(w, 13),
        base.polynomial_multiply_mod(
            base.substitute_power(phi, 13), gamma_polynomial, prime
        ),
        prime,
    )
    positive_support = sorted(
        {index % 13 for index, value in enumerate(codeword) if value and index % 13}
    )
    assert positive_support == list(support)

    petal_points = []
    for representative, value, scalar, label in zip(
        petal_representatives, petal_values, scalars, alpha
    ):
        for point in subgroup:
            x = representative * point % prime
            evaluated = base.polynomial_evaluate_mod(codeword, x, prime)
            assert evaluated == value
            assert evaluated == (
                scalar * base.polynomial_evaluate_mod(core_locator, label, prime)
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
    agreement = tau * 13 + len(retained)
    threshold = (core_size + 1) * 13
    assert agreement >= threshold
    assert len(set(petal_points + retained + missed)) == (tau + core_size) * 13
    retained_locator = base.polynomial_from_roots_mod(retained, prime)
    kernel, remainder = base.polynomial_divmod_mod(codeword, retained_locator, prime)
    assert not remainder and len(kernel) - 1 <= len(missed)
    deletable = []
    for point in missed:
        enlarged = base.polynomial_multiply_mod(
            retained_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(codeword, enlarged, prime)
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    assert deletable == []
    assert 13 <= len(missed) <= (tau - 1) * 13
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 13,
        "tau": tau,
        "m": core_size,
        "D": 0,
        "generator": generator,
        "zeta": zeta,
        "active_nonzero_DFT_sectors": list(support),
        "gamma_active_coefficients": active_gamma,
        "spectrum_histogram": [[1, 28], [2, 4], [3, 8]],
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
        "degree_bound": core_size * 13,
        "core_retained_profile": profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": threshold,
        "listing_surplus": agreement - threshold,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "kernel_quotient_degree": len(kernel) - 1,
        "single_point_deletions": deletable,
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
    subgroup = [pow(int(anchor["zeta"]), index, prime) for index in range(13)]
    used = set(anchor["core_quotient_indices"] + anchor["petal_quotient_indices"])
    new_indices = [index for index in range((prime - 1) // 13) if index not in used][:D]
    new_labels = [pow(generator, 13 * index, prime) for index in new_indices]
    Q = base.polynomial_from_roots_mod(new_labels, prime)
    codeword = base.polynomial_multiply_mod(
        anchor["codeword_coefficients_ascending"], base.substitute_power(Q, 13), prime
    )
    core_locator = base.polynomial_multiply_mod(
        anchor["core_locator_coefficients_ascending"], Q, prime
    )
    support = sorted(
        {index % 13 for index, value in enumerate(codeword) if value and index % 13}
    )
    assert support == anchor["active_nonzero_DFT_sectors"]
    for representative, scalar, label in zip(
        anchor["petal_representatives"], anchor["petal_scalars"], anchor["alpha_labels"]
    ):
        for point in subgroup:
            x = representative * point % prime
            assert base.polynomial_evaluate_mod(codeword, x, prime) == (
                scalar * base.polynomial_evaluate_mod(core_locator, label, prime)
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
    assert profile == anchor["core_retained_profile"] + [13] * D
    assert sorted(missed) == anchor["exact_missed_core"]
    agreement = tau * 13 + len(retained)
    threshold = (target_m + 1) * 13
    assert agreement >= threshold and len(codeword) - 1 <= target_m * 13
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]
    return {
        "p": prime,
        "ell": 13,
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
        "degree_bound": target_m * 13,
        "exact_missed_core_size": len(missed),
        "missed_core_identical_to_anchor": True,
        "H_stabilizer": stabilizer,
        "listed": True,
        "minimal": True,
        "primitive": True,
    }


def witness_family() -> dict[str, object]:
    anchors = [build_anchor(tau) for tau in (8, 9, 10)]
    padded = []
    for anchor in anchors:
        for target_m in range(int(anchor["m"]) + 1, 13):
            padded.append(pad_anchor(anchor, target_m))
    assert {(row["tau"], row["m"]) for row in padded} == {
        (8, 10), (8, 11), (8, 12), (9, 11), (9, 12), (10, 12)
    }
    return {"field": "F_521", "anchors_D0": anchors, "D_positive_counterexamples": padded}


def check_upstream() -> dict[str, object]:
    assert "The residual danger is `|S| >= 2`" in UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    assert "all `ell-1` DFT sectors active" in UPSTREAM_PV.read_text(encoding="utf-8")
    assert "explicit BIJECTION" in UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    return {
        "sources": [
            UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            UPSTREAM_PV.relative_to(ROOT).as_posix(),
            UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "Upstream has broader all-sector ell=13 witnesses but no exact-three-sector "
            "D>0 onset/grid theorem and no F_521 {1,5,9} family."
        ),
    }


def main() -> None:
    tables = resultant_tables()
    bad_audit = bad_prime_state_audit()
    vacant = vacancy_rows(bad_audit)
    witnesses = witness_family()
    upstream = check_upstream()
    artifact = {
        "title": "ell=13 exact-three-sector D-positive onset classification",
        "status": "VACANCY_AND_COUNTEREXAMPLE_ONSET_THEOREM",
        "verdict": "PASS_WITH_ELL13_EXACT_THREE_SECTOR_ONSET_CLASSIFIED",
        "theorem": (
            "For ell=13 exact-three-active-sector D>0 prime-field rows, tau=5,6,7 "
            "are universally vacant, while every row with tau=8,9,10 is nonvacant "
            "over F_521. Thus the exact-three-sector D>0 onset is tau=8."
        ),
        "preflight_decision": (
            "Route A was selected over ell=7 exact-four-sector D=0: only 3 and 7 AGL "
            "orbits feed small resultant tables, and common-root deficit theorem converts them into a full "
            "prime-uniform onset law rather than a single finite cell census."
        ),
        "resultant_tables": tables,
        "bad_prime_projective_audit": bad_audit,
        "uniform_vacancy_rows": vacant,
        "counterexample_family": witnesses,
        "parameter_grid": {
            "vacant": [[row["tau"], row["m"]] for row in vacant],
            "nonvacant": [[row["tau"], row["m"]] for row in witnesses["D_positive_counterexamples"]],
        },
        "proof": {
            "vacancy": (
                "Generic characteristics have live cap 3. At the six bad primes, exact "
                "four-fiber state audit gives robust cap 4 and proportional top-8<=24. "
                "common-root deficit theorem then pays every tau<=7 row strictly."
            ),
            "nonvacancy": (
                "Over F_521, Gamma=X+167X^5+371X^9 has spectrum 3^8 2^4 1^28. "
                "Lambda-free anchors at tau=8,9,10 list, and exact common-factor "
                "padding supplies every D>0 row above them."
            ),
        },
        "scope": (
            "Prime fields, ell=13, 5<=tau<m<13, D>0, background-free full petals, "
            "exactly three active nonzero DFT sectors."
        ),
        "nonclaims": [
            "Nonvacancy for tau>=8 is existential over F_521, not all-prime existence.",
            "No extension-field or exact-four-sector theorem is claimed.",
        ],
        "operation_counts": {
            "normalized_3x3_orbit_minors": 9,
            "normalized_4x4_orbit_minors": 49,
            "bad_prime_state_rows": sum(row["singular_projective_states"] for row in bad_audit["rows"]),
            "vacancy_rows": len(vacant),
            "D0_anchors": len(witnesses["anchors_D0"]),
            "D_positive_counterexamples": len(witnesses["D_positive_counterexamples"]),
            "blind_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "Compare ell=17 exact-three-sector onset against ell=7 exact-four-sector D=0; "
            "prefer the route exposing a stable onset law rather than another isolated census."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
    print("ell=13 exact-three-sector D-positive onset")
    print("bad_primes=" + str(tables["bad_admissible_primes"]) + " available=" + str(bad_audit["available_bad_primes"]))
    print("vacant=" + str([(row["tau"], row["m"]) for row in vacant]))
    print("counterexamples=" + str([(row["tau"], row["m"], row["total_agreement"]) for row in witnesses["D_positive_counterexamples"]]))
    print("PASS_WITH_ELL13_EXACT_THREE_SECTOR_ONSET_CLASSIFIED")


if __name__ == "__main__":
    main()
