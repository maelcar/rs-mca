#!/usr/bin/env python3
"""Norm-one five-fiber obstruction and exact-four-sector witness.

For every prime p=1 (mod 7), a constant-free polynomial Gamma with exactly
four active monomials among X,...,X^6 has no five-point mu_7-coset fiber.
The proof enumerates all 21^2 normalized 5x5 Fourier minors over Z[zeta_7]:
every quotient by the root Vandermonde has cyclotomic norm one.

The stratum is nonempty at the listing frontier.  Over F_127,

    Gamma = X + 64 X^2 + 112 X^3 + 70 X^5

has spectrum 4^1 2^6 1^11 and top-six 14.  A complete lambda-free
reconstruction gives a background-free full-petal listed word at
(tau,m,ell,D)=(5,6,7,0), with exact nonzero DFT support {1,2,3,5}, distinct
nonzero petal scalars, a primitive divisibility-minimal exact missed core,
and agreement 49.

The verifier also performs the exact ell=17 route comparison: its three- and
four-subset AGL tables have 3 and 11 orbits, while the 11x11 normalized 4x4
table already exposes 23 admissible exceptional primes. The calculation
opens the cleaner ell=7 exact-four stratum without claiming that the ell=17
onset conjecture is false.

Deterministic, offline and stdlib-only; no blind coefficient search.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import verify_l1_ell7_three_sector_counterexample as base
import verify_l1_ell11_three_sector_onset as ell11


ELL = 7
ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
ARTIFACT = DATA / "ell7_four_sector_counterexample.json"
UPSTREAM = ROOT
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
UPSTREAM_DAG = (
    UPSTREAM / "experimental" / "data" / "prize-dag" / "prize_dag.json"
)


# ============================================================================
# Exact orbit and cyclotomic route comparison


def affine_canonical(support: tuple[int, ...], ell: int) -> tuple[int, ...]:
    return min(
        tuple(sorted((scale * entry + shift) % ell for entry in support))
        for scale in range(1, ell)
        for shift in range(ell)
    )


def affine_representatives(ell: int, size: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            affine_canonical(support, ell)
            for support in itertools.combinations(range(ell), size)
        }
    )


def generic_cyclotomic_norm(polynomial: list[int], ell: int) -> int:
    """Norm in Z[zeta_ell], for prime ell, using the power basis."""

    dimension = ell - 1

    def zeta_power(exponent: int) -> tuple[int, ...]:
        residue = exponent % ell
        if residue == dimension:
            return (-1,) * dimension
        output = [0] * dimension
        output[residue] = 1
        return tuple(output)

    def add(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a + b for a, b in zip(first, second))

    def multiply(
        first: tuple[int, ...], second: tuple[int, ...]
    ) -> tuple[int, ...]:
        output = (0,) * dimension
        for first_index, first_value in enumerate(first):
            if not first_value:
                continue
            for second_index, second_value in enumerate(second):
                if second_value:
                    output = add(
                        output,
                        tuple(
                            first_value * second_value * value
                            for value in zeta_power(first_index + second_index)
                        ),
                    )
        return output

    value = (0,) * dimension
    for exponent, coefficient in enumerate(polynomial):
        if coefficient:
            value = add(
                value,
                tuple(coefficient * entry for entry in zeta_power(exponent)),
            )
    columns = [multiply(value, zeta_power(index)) for index in range(dimension)]
    matrix = [
        [columns[column][row] for column in range(dimension)]
        for row in range(dimension)
    ]
    return base.bareiss_determinant(matrix)


def distinct_prime_factors(value: int) -> list[int]:
    value = abs(value)
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


def ell17_route_cut() -> dict[str, object]:
    triple_reps = affine_representatives(17, 3)
    quadruple_reps = affine_representatives(17, 4)
    assert triple_reps == [(0, 1, 2), (0, 1, 3), (0, 1, 4)]
    assert len(quadruple_reps) == 11

    tables = {}
    for size, representatives in [(3, triple_reps), (4, quadruple_reps)]:
        table = []
        for exponents in representatives:
            row = []
            for roots in representatives:
                determinant = base.alternant_polynomial(exponents, roots)
                vandermonde = base.vandermonde_polynomial(roots)
                quotient = base.integer_poly_exact_division(
                    determinant, vandermonde
                )
                row.append(abs(generic_cyclotomic_norm(quotient, 17)))
            table.append(row)
        tables[size] = table

    assert tables[3] == [
        [1, 1, 1],
        [1, 239, 103],
        [1, 103, 1361],
    ]
    distinct_four_norms = sorted({value for row in tables[4] for value in row})
    assert distinct_four_norms == [
        1,
        103,
        137,
        256,
        307,
        443,
        613,
        647,
        953,
        1327,
        2551,
        3061,
        3299,
        3877,
        4217,
        4489,
        4523,
        5441,
        6733,
        9623,
        10201,
        10609,
        13907,
        14111,
        18769,
        28561,
        32743,
        60691,
        63139,
        65536,
        73441,
        88469,
        125903,
        126583,
        407389,
        659941,
    ]
    admissible_bad_primes = sorted(
        {
            prime
            for norm in distinct_four_norms
            for prime in distinct_prime_factors(norm)
            if prime % 17 == 1
        }
    )
    assert len(admissible_bad_primes) == 23
    return {
        "candidate": "ell=17 exact-three-sector onset",
        "three_subset_AGL_orbits": len(triple_reps),
        "four_subset_AGL_orbits": len(quadruple_reps),
        "three_by_three_quotient_norm_table": tables[3],
        "four_by_four_table_shape": [11, 11],
        "distinct_four_by_four_quotient_norms": distinct_four_norms,
        "admissible_bad_primes_before_state_audit": admissible_bad_primes,
        "decision": (
            "DEFER_NOT_REFUTE: the 11x11 exact table has 23 admissible "
            "exceptional primes before the required row-specific state and "
            "availability audits.  The suggested ell=17 onset law is left "
            "open; the norm-one ell=7 exact-four route is theorem-cleaner."
        ),
    }


def five_root_resultant_sieve() -> dict[str, object]:
    subsets = list(itertools.combinations(range(7), 5))
    representatives = affine_representatives(7, 5)
    assert representatives == [(0, 1, 2, 3, 4)]
    norm_counts = Counter()
    rows = 0
    for exponents in subsets:
        for roots in subsets:
            determinant = base.alternant_polynomial(exponents, roots)
            vandermonde = base.vandermonde_polynomial(roots)
            quotient = base.integer_poly_exact_division(
                determinant, vandermonde
            )
            determinant_norm = abs(
                base.ring_norm(base.polynomial_to_ring(determinant))
            )
            vandermonde_norm = abs(
                base.ring_norm(base.polynomial_to_ring(vandermonde))
            )
            quotient_norm = abs(
                base.ring_norm(base.polynomial_to_ring(quotient))
            )
            assert vandermonde_norm == 7**10
            assert determinant_norm == vandermonde_norm * quotient_norm
            assert quotient_norm == 1
            norm_counts[quotient_norm] += 1
            rows += 1
    assert rows == 21 * 21 == 441
    return {
        "five_subset_AGL_orbits": len(representatives),
        "representative": list(representatives[0]),
        "normalized_5x5_minors": rows,
        "quotient_norm_counts": {
            str(key): value for key, value in sorted(norm_counts.items())
        },
        "vandermonde_norm": 7**10,
        "admissible_bad_primes": [],
        "conclusion": (
            "Every 5x5 evaluation determinant has norm 7^10 times one. "
            "For p=1 mod 7, p is not 7, so no determinant vanishes and no "
            "exact-four-sector Gamma has a five-point mu_7 fiber."
        ),
    }


# ============================================================================
# Exact p=127 projective four-fiber census and full witness


FOUR_ROOT_TRANSLATION_REPS = sorted(
    {
        base.translate_canonical(support)
        for support in itertools.combinations(range(7), 4)
    }
)
assert FOUR_ROOT_TRANSLATION_REPS == [
    (0, 1, 2, 3),
    (0, 1, 2, 4),
    (0, 1, 2, 5),
    (0, 1, 3, 4),
    (0, 1, 3, 5),
]


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[value % prime for value in row] for row in matrix]
    output = 1
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            output = -output
        pivot_value = work[column][column]
        output = output * pivot_value % prime
        inverse = pow(pivot_value, -1, prime)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * inverse % prime
            for col in range(column, len(work)):
                work[row][col] = (
                    work[row][col] - factor * work[column][col]
                ) % prime
    return output % prime


def four_state_mod(
    active_support: tuple[int, ...],
    roots: tuple[int, ...],
    zeta: int,
    prime: int,
) -> list[int]:
    exponents = (0,) + active_support
    matrix = [
        [pow(zeta, root * exponent, prime) for exponent in exponents]
        for root in roots
    ]
    cofactors = []
    for omitted in range(5):
        minor = [
            [row[column] for column in range(5) if column != omitted]
            for row in matrix
        ]
        sign = -1 if omitted % 2 else 1
        cofactors.append(sign * determinant_mod(minor, prime) % prime)
    assert all(cofactors[1:])
    return cofactors


def projective_four_state_census_127() -> dict[str, object]:
    prime = 127
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 7
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(7)]
    assert (generator, quotient_size, zeta) == (3, 18, 4)

    top_counts = Counter()
    spectrum_counts = Counter()
    maximum_rows = []
    state_rows = 0
    for active_support in itertools.combinations(range(1, 7), 4):
        for roots in FOUR_ROOT_TRANSLATION_REPS:
            state = four_state_mod(active_support, roots, zeta, prime)
            inverse = pow(state[1], -1, prime)
            active_gamma = [value * inverse % prime for value in state[1:]]
            spectrum = base.gamma_spectrum(
                prime, generator, subgroup, active_support, active_gamma
            )
            histogram = tuple(sorted(Counter(spectrum).items()))
            top_six = sum(sorted(spectrum, reverse=True)[:6])
            top_counts[top_six] += 1
            spectrum_counts[histogram] += 1
            if top_six == 14:
                maximum_rows.append(
                    {
                        "active_support": list(active_support),
                        "root_orbit": list(roots),
                        "normalized_active_gamma": active_gamma,
                        "spectrum_histogram": [list(row) for row in histogram],
                    }
                )
            state_rows += 1
    assert state_rows == 15 * 5 == 75
    assert max(top_counts) == 14 and top_counts[14] == 9
    assert maximum_rows[0] == {
        "active_support": [1, 2, 3, 5],
        "root_orbit": [0, 1, 3, 5],
        "normalized_active_gamma": [1, 64, 112, 70],
        "spectrum_histogram": [[1, 11], [2, 6], [4, 1]],
    }
    return {
        "prime": prime,
        "four_root_translation_orbits": len(FOUR_ROOT_TRANSLATION_REPS),
        "exact_four_active_supports": 15,
        "projective_state_rows": state_rows,
        "top_six_counts": {
            str(key): value for key, value in sorted(top_counts.items())
        },
        "top_six_maximum_among_four_fiber_states": max(top_counts),
        "maximum_rows": maximum_rows,
        "scope_guard": (
            "This 75-state census locates and audits the witness.  It is not "
            "a global p=127 S_6 upper bound for exact-four Gamma having no "
            "four-point fiber."
        ),
    }


def full_witness_127() -> dict[str, object]:
    prime = 127
    tau = 5
    core_size = 6
    generator = base.primitive_root(prime)
    quotient_size = (prime - 1) // 7
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(7)]
    assert (generator, quotient_size, zeta) == (3, 18, 4)

    active_support = (1, 2, 3, 5)
    active_gamma = [1, 64, 112, 70]
    gamma_coefficients = [1, 64, 112, 0, 70, 0]
    core_indices = [0, 1, 3, 8, 9, 14]
    core_representatives = [1, 3, 27, 84, 125, 22]
    target_levels = [120, 47, 113, 26, 39, 1]
    petal_indices = [2, 4, 5, 6, 7]
    petal_representatives = [9, 81, 116, 94, 28]
    expected_petal_values = [45, 29, 42, 69, 110]
    expected_scalars = [102, 88, 22, 36, 69]

    assert core_representatives == [
        pow(generator, index, prime) for index in core_indices
    ]
    assert petal_representatives == [
        pow(generator, index, prime) for index in petal_indices
    ]
    alpha = [pow(value, 7, prime) for value in petal_representatives]
    beta = [pow(value, 7, prime) for value in core_representatives]
    assert len(set(alpha + beta)) == tau + core_size

    spectrum = base.gamma_spectrum(
        prime, generator, subgroup, active_support, active_gamma
    )
    assert Counter(spectrum) == Counter({1: 11, 2: 6, 4: 1})
    assert sum(sorted(spectrum, reverse=True)[:6]) == 14
    selected_profile = []
    for representative, target in zip(core_representatives, target_levels):
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(active_gamma, active_support)
            )
            % prime
            for point in subgroup
        ]
        count = values.count(target)
        assert count == max(Counter(values).values())
        selected_profile.append(count)
    assert selected_profile == [4, 2, 2, 2, 2, 2]

    core_locator = base.polynomial_from_roots_mod(beta, prime)
    (
        petal_values,
        g0_u,
        g0_v,
        actual_scalars,
        lambda_rank,
    ) = ell11.solve_level_system(
        prime, alpha, beta, core_locator, target_levels
    )
    assert petal_values == expected_petal_values
    assert (g0_u, g0_v) == (122, 0)
    assert actual_scalars == expected_scalars
    assert lambda_rank == 6

    phi = base.polynomial_from_roots_mod(alpha, prime)
    w = base.polynomial_interpolate_mod(alpha, petal_values, prime)
    g_polynomial = [g0_u, 1, 64, 112, 0, 70]
    codeword = base.polynomial_add_mod(
        base.substitute_power(w, 7),
        base.polynomial_multiply_mod(
            base.substitute_power(phi, 7), g_polynomial, prime
        ),
        prime,
    )
    degree = len(codeword) - 1
    assert degree == 40 <= core_size * 7
    exact_sector_support = sorted(
        {
            degree_index % 7
            for degree_index, coefficient in enumerate(codeword)
            if coefficient and degree_index % 7
        }
    )
    assert exact_sector_support == list(active_support)

    petal_points = []
    for representative, value, scalar, label in zip(
        petal_representatives, petal_values, actual_scalars, alpha
    ):
        for point in subgroup:
            x = representative * point % prime
            petal_points.append(x)
            evaluated = base.polynomial_evaluate_mod(codeword, x, prime)
            assert evaluated == value
            assert evaluated == (
                scalar
                * base.polynomial_evaluate_mod(core_locator, label, prime)
            ) % prime

    retained = []
    missed = []
    reconstructed_levels = []
    core_profile = []
    for representative, beta_value in zip(core_representatives, beta):
        level = (
            -base.polynomial_evaluate_mod(w, beta_value, prime)
            * pow(
                base.polynomial_evaluate_mod(phi, beta_value, prime),
                -1,
                prime,
            )
            - g0_u
            - g0_v * beta_value
        ) % prime
        reconstructed_levels.append(level)
        retained_here = 0
        for point in subgroup:
            x = representative * point % prime
            if base.polynomial_evaluate_mod(codeword, x, prime) == 0:
                retained.append(x)
                retained_here += 1
            else:
                missed.append(x)
        core_profile.append(retained_here)
    assert reconstructed_levels == target_levels
    assert core_profile == selected_profile
    assert len(retained) == 14
    agreement = tau * 7 + len(retained)
    listing_threshold = (core_size + 1) * 7
    assert agreement == listing_threshold == 49
    assert len(set(petal_points + retained + missed)) == (tau + core_size) * 7

    retained_locator = base.polynomial_from_roots_mod(retained, prime)
    kernel_quotient, remainder = base.polynomial_divmod_mod(
        codeword, retained_locator, prime
    )
    assert not remainder
    assert base.polynomial_multiply_mod(
        kernel_quotient, retained_locator, prime
    ) == codeword
    kernel_degree = len(kernel_quotient) - 1
    assert kernel_degree == 26 <= len(missed) == 28

    deletable = []
    for point in missed:
        enlarged_locator = base.polynomial_multiply_mod(
            retained_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(
            codeword, enlarged_locator, prime
        )
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    assert deletable == []

    negative_missed = missed + [retained[0]]
    negative_locator = base.polynomial_from_roots_mod(retained[1:], prime)
    negative_deletable = []
    for point in negative_missed:
        locator_with_point = base.polynomial_multiply_mod(
            negative_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = base.polynomial_divmod_mod(
            codeword, locator_with_point, prime
        )
        if not rem and len(quotient) - 1 <= len(negative_missed) - 1:
            negative_deletable.append(point)
    assert negative_deletable == [retained[0]]

    missed_traces = [7 - value for value in core_profile]
    assert missed_traces == [3, 5, 5, 5, 5, 5]
    missed_set = set(missed)
    stabilizer = [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % prime for point in missed_set} == missed_set
    ]
    assert stabilizer == [1]

    return {
        "p": prime,
        "ell": 7,
        "tau": tau,
        "m": core_size,
        "D": 0,
        "generator": generator,
        "zeta": zeta,
        "active_nonzero_DFT_sectors": list(active_support),
        "gamma_coefficients_X1_through_X6": gamma_coefficients,
        "spectrum_histogram": [[1, 11], [2, 6], [4, 1]],
        "top_six": 14,
        "core_quotient_indices": core_indices,
        "core_representatives": core_representatives,
        "target_modal_levels": target_levels,
        "lambda_map_rank": lambda_rank,
        "petal_quotient_indices": petal_indices,
        "petal_representatives": petal_representatives,
        "petal_constant_values": petal_values,
        "petal_scalars": actual_scalars,
        "g0_u_v": [g0_u, g0_v],
        "w_coefficients_ascending": w,
        "phi_coefficients_ascending": phi,
        "core_locator_coefficients_ascending": core_locator,
        "codeword_coefficients_ascending": codeword,
        "degree": degree,
        "degree_bound": core_size * 7,
        "exact_nonzero_sector_support_from_codeword": exact_sector_support,
        "core_retained_profile": core_profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": listing_threshold,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "kernel_quotient_degree": kernel_degree,
        "single_point_deletions": deletable,
        "minimality_negative_control": negative_deletable,
        "missed_core_traces": missed_traces,
        "H_stabilizer": stabilizer,
        "listed": True,
        "minimal": True,
        "primitive": True,
    }


# ============================================================================
# Upstream collision guard and assembly


def check_upstream() -> dict[str, object]:
    pv_text = UPSTREAM_PV.read_text(encoding="utf-8")
    reconstruction_text = UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    dag_text = UPSTREAM_DAG.read_text(encoding="utf-8")
    assert "all `ell-1` DFT sectors active" in pv_text
    assert "Gamma` at `p=211`: `[161,178,120,90,1,10]`" in pv_text
    assert "explicit BIJECTION" in reconstruction_text
    assert "pma_wide_residual" in dag_text

    return {
        "sources": [
            UPSTREAM_PV.relative_to(ROOT).as_posix(),
            UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
            UPSTREAM_DAG.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "Upstream has a compatible witness in the same (tau,m,ell) "
            "cell, explicitly with all six nonconstant DFT sectors active. "
            "It has neither the exact-four norm-one theorem nor the "
            "{1,2,3,5}-sector F_127 word. This is a distinct stratum."
        ),
    }


def main() -> None:
    upstream = check_upstream()
    route_cut = ell17_route_cut()
    five_root = five_root_resultant_sieve()
    state_census = projective_four_state_census_127()
    witness = full_witness_127()

    artifact = {
        "title": "ell=7 exact-four-sector norm-one obstruction and counterexample",
        "status": "COUNTEREXAMPLE_WITH_UNIFORM_FIBER_CAP_THEOREM",
        "verdict": "PASS_WITH_ELL7_EXACT_FOUR_SECTOR_COUNTEREXAMPLE",
        "route_comparison": route_cut,
        "uniform_theorem": (
            "For every prime p congruent to 1 mod 7 and every constant-free "
            "Gamma with exactly four active nonzero monomials among "
            "X,...,X^6, every mu_7-coset fiber has size at most four."
        ),
        "proof": [
            "There is one AGL(1,7) orbit of five-subsets. More strongly, all 21^2 exponent/root normalized 5x5 Fourier minors were evaluated exactly.",
            "Every determinant divided by its root Vandermonde has cyclotomic norm one; the Vandermonde norm is 7^10. Thus no p=1 mod 7 can annihilate a five-point evaluation determinant.",
            "At p=127 the exact 75-row projective four-fiber census locates Gamma=X+64X^2+112X^3+70X^5 with spectrum 4^1 2^6 1^11 and S_6=14.",
            "The six selected modal levels [4,2,2,2,2,2] admit a rank-six lambda-free lift. Pointwise petal/core checks give agreement 49 at degree 40<=42.",
            "Kernel division, all 28 one-point deletion tests, the positive negative control, and the trivial mu_7 stabilizer certify divisibility minimality and primitivity.",
        ],
        "five_root_resultant_sieve": five_root,
        "projective_four_state_census_F127": state_census,
        "full_global_counterexample": witness,
        "scope": (
            "Prime fields, ell=7, tau=5, m=6, D=0, background-free full "
            "petals, and exactly four active nonzero DFT sectors.  The fiber "
            "cap theorem is prime-uniform; explicit nonvacancy is over F_127."
        ),
        "nonclaims": [
            "No uniform S_6<=14 theorem is claimed for every exact-four-sector Gamma; the norm-one argument gives only the uniform fiber cap four.",
            "The 75-state p=127 census covers Gamma having a four-point fiber, not all exact-four coefficient vectors without one.",
            "The ell=17 exact-three onset conjecture is deferred, not refuted.",
            "No D>0 or extension-field classification is claimed.",
            "The upstream all-six-sector witnesses are compatible and distinct from the new exact-four-sector word.",
        ],
        "operation_counts": {
            "ell17_normalized_orbit_minors": 3 * 3 + 11 * 11,
            "ell7_normalized_5x5_minors": five_root["normalized_5x5_minors"],
            "F127_projective_four_fiber_states": state_census[
                "projective_state_rows"
            ],
            "full_witness_point_evaluations": 77,
            "blind_four_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "Either return to ell=17 exact-three onset with an arithmetic "
            "classifier that compresses its 23 exceptional primes, or feed "
            "the new robust cap c=4 and exact-four F_127 anchor into common-root deficit theorem "
            "to test the first D>0 rows."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=7 exact-four-sector norm-one obstruction")
    print(
        "ell17_bad_primes="
        + str(len(route_cut["admissible_bad_primes_before_state_audit"]))
        + " five_minor_norms="
        + str(five_root["quotient_norm_counts"])
    )
    print(
        "state_rows="
        + str(state_census["projective_state_rows"])
        + " witness_spectrum="
        + str(witness["spectrum_histogram"])
    )
    print(
        "agreement="
        + str(witness["total_agreement"])
        + " degree="
        + str(witness["degree"])
        + " missed="
        + str(witness["exact_missed_core_size"])
    )
    print("PASS_WITH_ELL7_EXACT_FOUR_SECTOR_COUNTEREXAMPLE")


if __name__ == "__main__":
    main()
