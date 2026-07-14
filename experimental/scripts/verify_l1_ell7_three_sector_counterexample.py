#!/usr/bin/env python3
"""Exact-three-sector threshold theorem and full counterexample at ell=7.

For Gamma(X)=a X^r+b X^s+c X^t with exactly three nonzero coefficients,
this certificate proves uniformly over every prime p=1 (mod 7):

    S_6(Gamma) <= 14.

The bound is sharp.  Over F_113, Gamma=X+67X^3+75X^5 has spectrum
3^2 2^4 1^10 and top-six 14.  A complete lambda-free reconstruction gives
a background-free full-petal listed word at (tau,m,ell,D)=(5,6,7,0), with
exactly active nonzero DFT sectors {1,3,5}, distinct nonzero petal scalars,
and a primitive divisibility-minimal exact missed core.

Uniform upper-bound mechanism:

* every normalized 4x4 Fourier minor has cyclotomic quotient norm 1 or 8,
  so odd p=1 mod 7 permits no four-point fiber;
* triple fibers are classified by the five translation orbits of 3-subsets
  of mu_7; their monomial-curve invariant separates the orbits except at a
  finite exact prime support, and exact state audit at those primes still
  gives at most two triple cosets for one Gamma;
* with fiber cap three and at most two triple cosets, top-six is at most
  3+3+2+2+2+2=14.

The verifier is deterministic, offline and stdlib-only.  It uses exact
integer/cyclotomic arithmetic, not floating point or coefficient sampling.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ELL = 7
EXCEPTIONAL_TRIPLE_PRIMES = [29, 71, 113, 239, 421, 1583]
FACTOR_CANDIDATES = [2, 3, 5, 7, 13, 29, 71, 113, 239, 421, 1583]

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
ARTIFACT = DATA / "ell7_three_sector_counterexample.json"
UPSTREAM = ROOT
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
UPSTREAM_DAG = (
    UPSTREAM
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)


# ============================================================================
# Integer polynomials, ascending coefficients


def trim(polynomial: list[int]) -> list[int]:
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def integer_poly_add(first: list[int], second: list[int]) -> list[int]:
    output = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        output[index] += value
    for index, value in enumerate(second):
        output[index] += value
    return trim(output)


def integer_poly_mul(first: list[int], second: list[int]) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] += first_value * second_value
    return trim(output)


def integer_poly_exact_division(
    dividend: list[int], divisor: list[int]
) -> list[int]:
    work = trim(dividend[:])
    divisor = trim(divisor[:])
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    while work != [0] and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient, remainder = divmod(work[-1], divisor[-1])
        assert remainder == 0
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[index + shift] -= coefficient * value
        trim(work)
    assert work == [0]
    return trim(quotient)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def alternant_polynomial(
    exponents: tuple[int, ...], roots: tuple[int, ...]
) -> list[int]:
    size = len(exponents)
    output = [0]
    for permutation in itertools.permutations(range(size)):
        degree = sum(
            roots[row] * exponents[permutation[row]] for row in range(size)
        )
        term = [0] * degree + [permutation_sign(permutation)]
        output = integer_poly_add(output, term)
    return output


def vandermonde_polynomial(roots: tuple[int, ...]) -> list[int]:
    output = [1]
    for first, second in itertools.combinations(roots, 2):
        factor = [0] * first + [-1]
        monomial_second = [0] * second + [1]
        factor = integer_poly_add(factor, monomial_second)
        output = integer_poly_mul(output, factor)
    return output


# ============================================================================
# Exact cyclotomic ring Z[zeta_7], basis 1,z,...,z^5 and z^6=-(1+...+z^5)


Ring = tuple[int, int, int, int, int, int]
ZERO: Ring = (0, 0, 0, 0, 0, 0)
ONE: Ring = (1, 0, 0, 0, 0, 0)


def ring_add(first: Ring, second: Ring) -> Ring:
    return tuple(first[i] + second[i] for i in range(6))  # type: ignore[return-value]


def ring_neg(value: Ring) -> Ring:
    return tuple(-entry for entry in value)  # type: ignore[return-value]


def ring_sub(first: Ring, second: Ring) -> Ring:
    return ring_add(first, ring_neg(second))


def ring_zeta_power(exponent: int) -> Ring:
    residue = exponent % 7
    if residue == 6:
        return (-1, -1, -1, -1, -1, -1)
    output = [0] * 6
    output[residue] = 1
    return tuple(output)  # type: ignore[return-value]


def ring_mul(first: Ring, second: Ring) -> Ring:
    output = ZERO
    for first_index, first_value in enumerate(first):
        if not first_value:
            continue
        for second_index, second_value in enumerate(second):
            if second_value:
                term = tuple(
                    first_value * second_value * entry
                    for entry in ring_zeta_power(first_index + second_index)
                )
                output = ring_add(output, term)  # type: ignore[arg-type]
    return output


def ring_pow(value: Ring, exponent: int) -> Ring:
    output = ONE
    base = value
    while exponent:
        if exponent & 1:
            output = ring_mul(output, base)
        base = ring_mul(base, base)
        exponent //= 2
    return output


def polynomial_to_ring(polynomial: list[int]) -> Ring:
    output = ZERO
    for exponent, coefficient in enumerate(polynomial):
        if coefficient:
            output = ring_add(
                output,
                tuple(
                    coefficient * entry for entry in ring_zeta_power(exponent)
                ),  # type: ignore[arg-type]
            )
    return output


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for column in range(size - 1):
        if work[column][column] == 0:
            swap = next(
                (
                    row
                    for row in range(column + 1, size)
                    if work[row][column]
                ),
                None,
            )
            if swap is None:
                return 0
            work[column], work[swap] = work[swap], work[column]
            sign *= -1
        pivot = work[column][column]
        for row in range(column + 1, size):
            for col in range(column + 1, size):
                numerator = (
                    work[row][col] * pivot
                    - work[row][column] * work[column][col]
                )
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                work[row][col] = quotient
        for row in range(column + 1, size):
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def ring_norm(value: Ring) -> int:
    matrix = []
    columns = [ring_mul(value, ring_zeta_power(index)) for index in range(6)]
    for row in range(6):
        matrix.append([columns[column][row] for column in range(6)])
    return bareiss_determinant(matrix)


def ring_determinant(matrix: list[list[Ring]]) -> Ring:
    size = len(matrix)
    output = ZERO
    for permutation in itertools.permutations(range(size)):
        term = ONE
        for row in range(size):
            term = ring_mul(term, matrix[row][permutation[row]])
        if permutation_sign(permutation) < 0:
            term = ring_neg(term)
        output = ring_add(output, term)
    return output


def factor_over_candidates(value: int) -> dict[int, int]:
    value = abs(value)
    output = {}
    for prime in FACTOR_CANDIDATES:
        multiplicity = 0
        while value and value % prime == 0:
            value //= prime
            multiplicity += 1
        if multiplicity:
            output[prime] = multiplicity
    assert value == 1
    return output


# ============================================================================
# Fourier 4x4 cap and triple-state invariant proof record


def four_root_resultant_sieve() -> dict[str, object]:
    values = Counter()
    rows = 0
    for active_support in itertools.combinations(range(1, 7), 3):
        exponents = (0,) + active_support
        for roots in itertools.combinations(range(7), 4):
            determinant = alternant_polynomial(exponents, roots)
            vandermonde = vandermonde_polynomial(roots)
            quotient = integer_poly_exact_division(determinant, vandermonde)
            determinant_norm = abs(ring_norm(polynomial_to_ring(determinant)))
            vandermonde_norm = abs(ring_norm(polynomial_to_ring(vandermonde)))
            quotient_norm = abs(ring_norm(polynomial_to_ring(quotient)))
            assert vandermonde_norm == 7**6
            assert determinant_norm == vandermonde_norm * quotient_norm
            assert quotient_norm in {1, 8}
            values[quotient_norm] += 1
            rows += 1
    assert rows == 20 * 35 == 700
    assert set(values) == {1, 8}
    return {
        "normalized_4x4_minors": rows,
        "quotient_norm_counts": {str(key): value for key, value in sorted(values.items())},
        "quotient_norm_values": sorted(values),
        "admissible_bad_primes": [],
        "conclusion": (
            "A four-point fiber would make one normalized 4x4 minor vanish. "
            "Its characteristic must divide 1 or 8.  Every p=1 mod 7 is "
            "odd, so every exact-three-sector fiber has size at most three."
        ),
    }


def translate_canonical(support: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((entry + shift) % 7 for entry in support))
        for shift in range(7)
    )


TRIPLE_REPRESENTATIVES = sorted(
    {
        translate_canonical(support)
        for support in itertools.combinations(range(7), 3)
    }
)
assert TRIPLE_REPRESENTATIVES == [
    (0, 1, 2),
    (0, 1, 3),
    (0, 1, 4),
    (0, 1, 5),
    (0, 2, 4),
]


def triple_state_ring(
    active_support: tuple[int, int, int], roots: tuple[int, int, int]
) -> list[Ring]:
    exponents = (0,) + active_support
    matrix = [
        [ring_zeta_power(root * exponent) for exponent in exponents]
        for root in roots
    ]
    cofactors = []
    for omitted in range(4):
        minor = [
            [row[column] for column in range(4) if column != omitted]
            for row in matrix
        ]
        value = ring_determinant(minor)
        cofactors.append(value if omitted % 2 == 0 else ring_neg(value))
    return cofactors


def invariant_collision_element(
    first: list[Ring],
    second: list[Ring],
    first_gap: int,
    second_gap: int,
) -> Ring:
    # I=(B_s/B_r)^d2/(B_t/B_r)^d1.  Cross-multiply I_first=I_second.
    left = ring_mul(
        ring_pow(first[2], second_gap),
        ring_mul(
            ring_pow(second[3], first_gap),
            ring_pow(second[1], second_gap - first_gap),
        ),
    )
    right = ring_mul(
        ring_pow(second[2], second_gap),
        ring_mul(
            ring_pow(first[3], first_gap),
            ring_pow(first[1], second_gap - first_gap),
        ),
    )
    return ring_sub(left, right)


def triple_invariant_sieve() -> dict[str, object]:
    collision_norms = Counter()
    exact_duplicate_rows = []
    active_coefficient_norms = set()
    generic_max_triples = 0
    support_rows = []

    for active_support in itertools.combinations(range(1, 7), 3):
        sector_r, sector_s, sector_t = active_support
        first_gap = sector_s - sector_r
        second_gap = sector_t - sector_r
        kernel_bound = math.gcd(first_gap, second_gap)
        states = [
            triple_state_ring(active_support, roots)
            for roots in TRIPLE_REPRESENTATIVES
        ]
        for state in states:
            for coefficient in state[1:]:
                coefficient_norm = abs(ring_norm(coefficient))
                active_coefficient_norms.add(coefficient_norm)
                assert coefficient_norm in {343, 2744}

        equality_graph = {index: {index} for index in range(5)}
        support_norms = []
        for first_index, second_index in itertools.combinations(range(5), 2):
            collision = invariant_collision_element(
                states[first_index],
                states[second_index],
                first_gap,
                second_gap,
            )
            norm = abs(ring_norm(collision))
            collision_norms[norm] += 1
            support_norms.append(norm)
            if collision == ZERO:
                equality_graph[first_index].add(second_index)
                equality_graph[second_index].add(first_index)
                exact_duplicate_rows.append(
                    {
                        "active_support": list(active_support),
                        "triple_orbits": [first_index, second_index],
                    }
                )

        # Connected components of exact characteristic-zero invariant equality.
        seen = set()
        maximum_exact_multiplicity = 0
        for start in range(5):
            if start in seen:
                continue
            stack = [start]
            component = set()
            while stack:
                current = stack.pop()
                if current in component:
                    continue
                component.add(current)
                stack.extend(equality_graph[current])
            seen.update(component)
            maximum_exact_multiplicity = max(
                maximum_exact_multiplicity, len(component)
            )
        support_generic_bound = kernel_bound * maximum_exact_multiplicity
        assert support_generic_bound <= 2
        generic_max_triples = max(generic_max_triples, support_generic_bound)
        support_rows.append(
            {
                "active_support": list(active_support),
                "gap_gcd": kernel_bound,
                "maximum_exact_invariant_multiplicity": maximum_exact_multiplicity,
                "generic_triple_coset_bound": support_generic_bound,
                "collision_norm_values": sorted(set(support_norms)),
            }
        )

    factorizations = {}
    exceptional = set()
    for norm in collision_norms:
        if norm == 0:
            continue
        factorization = factor_over_candidates(norm)
        factorizations[str(norm)] = {
            str(prime): multiplicity
            for prime, multiplicity in sorted(factorization.items())
        }
        exceptional.update(
            prime for prime in factorization if prime % 7 == 1
        )
    assert sorted(exceptional) == EXCEPTIONAL_TRIPLE_PRIMES
    assert active_coefficient_norms == {343, 2744}
    assert generic_max_triples == 2
    return {
        "root_triple_translation_orbits": len(TRIPLE_REPRESENTATIVES),
        "representatives": [list(row) for row in TRIPLE_REPRESENTATIVES],
        "active_coefficient_norms": sorted(active_coefficient_norms),
        "invariant_collision_rows": sum(collision_norms.values()),
        "distinct_collision_norms": len(collision_norms),
        "collision_norm_counts": {
            str(key): value for key, value in sorted(collision_norms.items())
        },
        "collision_norm_factorizations": factorizations,
        "exact_duplicate_rows": exact_duplicate_rows,
        "generic_maximum_triple_cosets": generic_max_triples,
        "exceptional_admissible_primes": sorted(exceptional),
        "support_rows": support_rows,
        "invariant": (
            "I=(B_s/B_r)^(t-r)/(B_t/B_r)^(s-r).  Along core labels "
            "B_e=gamma_e b^e, I is independent of b.  Equal invariants "
            "are necessary for one Gamma to hit two root-triple orbits."
        ),
    }


# ============================================================================
# Finite fields and exact exceptional-state audit


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def determinant_three_mod(matrix: list[list[int]], prime: int) -> int:
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    ) % prime


def triple_state_mod(
    active_support: tuple[int, int, int],
    roots: tuple[int, int, int],
    zeta: int,
    prime: int,
) -> list[int]:
    exponents = (0,) + active_support
    matrix = [
        [pow(zeta, root * exponent, prime) for exponent in exponents]
        for root in roots
    ]
    cofactors = []
    for omitted in range(4):
        minor = [
            [row[column] for column in range(4) if column != omitted]
            for row in matrix
        ]
        cofactors.append(
            ((-1) ** omitted * determinant_three_mod(minor, prime)) % prime
        )
    assert all(cofactors[1:])
    return cofactors


def gamma_spectrum(
    prime: int,
    generator: int,
    subgroup: list[int],
    active_support: tuple[int, int, int],
    gamma: list[int],
) -> list[int]:
    quotient_size = (prime - 1) // 7
    output = []
    for label_index in range(quotient_size):
        representative = pow(generator, label_index, prime)
        values = [
            sum(
                coefficient * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(gamma, active_support)
            )
            % prime
            for point in subgroup
        ]
        output.append(max(Counter(values).values()))
    return output


def exact_threshold_from_triple_states(prime: int) -> dict[str, object]:
    generator = primitive_root(prime)
    quotient_size = (prime - 1) // 7
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(7)]
    maximum_top = min(12, 2 * quotient_size)
    maximum_row = None
    maximum_triple_cosets = 0
    state_rows = 0

    for active_support in itertools.combinations(range(1, 7), 3):
        for roots in TRIPLE_REPRESENTATIVES:
            state = triple_state_mod(active_support, roots, zeta, prime)
            inverse = pow(state[1], -1, prime)
            gamma = [state[index] * inverse % prime for index in (1, 2, 3)]
            spectrum = gamma_spectrum(
                prime, generator, subgroup, active_support, gamma
            )
            triple_cosets = spectrum.count(3)
            maximum_triple_cosets = max(maximum_triple_cosets, triple_cosets)
            top = sum(sorted(spectrum, reverse=True)[: min(6, quotient_size)])
            if top > maximum_top:
                maximum_top = top
                maximum_row = {
                    "active_support": list(active_support),
                    "root_triple_orbit": list(roots),
                    "gamma_normalized": gamma,
                    "spectrum_histogram": [
                        [multiplicity, count]
                        for multiplicity, count in sorted(Counter(spectrum).items())
                    ],
                }
            state_rows += 1

    assert state_rows == 20 * 5 == 100
    assert maximum_triple_cosets <= 2
    if quotient_size >= 6:
        assert maximum_top <= 14
    return {
        "p": prime,
        "quotient_size": quotient_size,
        "state_rows": state_rows,
        "maximum_triple_cosets": maximum_triple_cosets,
        "exact_S6_if_six_labels_exist": maximum_top if quotient_size >= 6 else None,
        "maximum_row": maximum_row,
        "completeness": (
            "If Gamma has no triple fiber then S6<=12.  Otherwise input "
            "rescaling moves one triple coset to H and root translation "
            "moves its root set to one of the five representatives, so "
            "one of these 100 projective states has the same full spectrum."
        ),
    }


def exceptional_state_audit() -> dict[str, object]:
    rows = [
        exact_threshold_from_triple_states(prime)
        for prime in EXCEPTIONAL_TRIPLE_PRIMES
    ]
    # Two nonexceptional controls demonstrate that the uniform upper bound is
    # sometimes strict; do not misstate S6(p)=14 for every p.
    controls = [
        exact_threshold_from_triple_states(prime) for prime in (449, 463)
    ]
    assert all(row["maximum_triple_cosets"] <= 2 for row in rows + controls)
    assert [row["exact_S6_if_six_labels_exist"] for row in controls] == [13, 13]
    return {
        "exceptional_rows": rows,
        "strict_bound_controls": controls,
        "total_projective_state_rows": 100 * (len(rows) + len(controls)),
    }


# ============================================================================
# Full F_113 witness: exact-three-sector listed primitive minimal codeword


def polynomial_add_mod(
    first: list[int], second: list[int], prime: int
) -> list[int]:
    output = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        output[index] = (output[index] + value) % prime
    for index, value in enumerate(second):
        output[index] = (output[index] + value) % prime
    while output and output[-1] == 0:
        output.pop()
    return output


def polynomial_multiply_mod(
    first: list[int], second: list[int], prime: int
) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] = (
                output[first_index + second_index]
                + first_value * second_value
            ) % prime
    while output and output[-1] == 0:
        output.pop()
    return output


def polynomial_from_roots_mod(labels: list[int], prime: int) -> list[int]:
    output = [1]
    for label in labels:
        output = polynomial_multiply_mod(output, [(-label) % prime, 1], prime)
    return output


def polynomial_evaluate_mod(polynomial: list[int], point: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % prime
    return value


def polynomial_interpolate_mod(
    xs: list[int], ys: list[int], prime: int
) -> list[int]:
    output = [0] * len(xs)
    for index, point in enumerate(xs):
        basis = [1]
        denominator = 1
        for other_index, other in enumerate(xs):
            if other_index == index:
                continue
            basis = polynomial_multiply_mod(
                basis, [(-other) % prime, 1], prime
            )
            denominator = denominator * (point - other) % prime
        scale = ys[index] * pow(denominator, -1, prime) % prime
        output = polynomial_add_mod(
            output,
            [scale * coefficient % prime for coefficient in basis],
            prime,
        )
    return output


def substitute_power(polynomial: list[int], power: int) -> list[int]:
    if not polynomial:
        return []
    output = [0] * ((len(polynomial) - 1) * power + 1)
    for index, coefficient in enumerate(polynomial):
        output[index * power] = coefficient
    return output


def polynomial_divmod_mod(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    work = numerator[:]
    while work and work[-1] == 0:
        work.pop()
    degree_denominator = len(denominator) - 1
    inverse = pow(denominator[-1], -1, prime)
    quotient = [0] * max(0, len(work) - degree_denominator)
    while len(work) - 1 >= degree_denominator and work:
        degree = len(work) - 1
        coefficient = work[-1] * inverse % prime
        shift = degree - degree_denominator
        quotient[shift] = coefficient
        for index, value in enumerate(denominator):
            work[shift + index] = (
                work[shift + index] - coefficient * value
            ) % prime
        while work and work[-1] == 0:
            work.pop()
    while quotient and quotient[-1] == 0:
        quotient.pop()
    return quotient, work


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [value * inverse % prime for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][column]:
                factor = work[row][column]
                work[row] = [
                    (value - factor * pivot_value) % prime
                    for value, pivot_value in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def full_witness_113() -> dict[str, object]:
    prime = 113
    tau = 5
    core_size = 6
    generator = primitive_root(prime)
    quotient_size = (prime - 1) // 7
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(7)]
    assert (generator, zeta, quotient_size) == (3, 49, 16)

    active_support = (1, 3, 5)
    gamma_active = [1, 67, 75]
    gamma = [1, 0, 67, 0, 75, 0]
    core_indices = [0, 8, 4, 6, 12, 14]
    core_representatives = [1, 7, 81, 51, 2, 18]
    target_levels = [30, 83, 22, 39, 91, 74]
    petal_indices = [1, 2, 3, 5, 7]
    petal_representatives = [3, 9, 27, 17, 40]
    petal_values = [38, 72, 92, 51, 15]
    g0_u = 61
    g0_v = 0

    assert core_representatives == [
        pow(generator, index, prime) for index in core_indices
    ]
    assert petal_representatives == [
        pow(generator, index, prime) for index in petal_indices
    ]
    alpha = [pow(value, 7, prime) for value in petal_representatives]
    beta = [pow(value, 7, prime) for value in core_representatives]
    assert len(set(alpha + beta)) == tau + core_size
    assert all(petal_values) and len(set(petal_values)) == tau

    # Verify the complete honest quotient spectrum and the selected modal levels.
    spectrum = gamma_spectrum(
        prime,
        generator,
        subgroup,
        active_support,
        gamma_active,
    )
    assert Counter(spectrum) == Counter({1: 10, 2: 4, 3: 2})
    assert sum(sorted(spectrum, reverse=True)[:6]) == 14
    selected_profile = []
    for representative, target in zip(core_representatives, target_levels):
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(gamma_active, active_support)
            )
            % prime
            for point in subgroup
        ]
        count = values.count(target)
        assert count == max(Counter(values).values())
        selected_profile.append(count)
    assert selected_profile == [3, 3, 2, 2, 2, 2]

    core_locator = polynomial_from_roots_mod(beta, prime)
    phi = polynomial_from_roots_mod(alpha, prime)
    actual_scalars = [
        value
        * pow(polynomial_evaluate_mod(core_locator, label, prime), -1, prime)
        % prime
        for value, label in zip(petal_values, alpha)
    ]
    assert actual_scalars == [51, 69, 91, 20, 66]
    assert all(actual_scalars) and len(set(actual_scalars)) == tau

    # Instantiate upstream Lemma LF: the map from five petal values and the
    # two sector-zero parameters (u,v) to six core levels has full row rank.
    def level_map(values: list[int], u_value: int, v_value: int) -> list[int]:
        interpolant = polynomial_interpolate_mod(alpha, values, prime)
        return [
            (
                -polynomial_evaluate_mod(interpolant, label, prime)
                * pow(polynomial_evaluate_mod(phi, label, prime), -1, prime)
                - u_value
                - v_value * label
            )
            % prime
            for label in beta
        ]

    level_columns = []
    for variable in range(7):
        basis = [0] * 7
        basis[variable] = 1
        level_columns.append(level_map(basis[:5], basis[5], basis[6]))
    lambda_rank = matrix_rank_mod(
        [
            [level_columns[column][row] for column in range(7)]
            for row in range(6)
        ],
        prime,
    )
    assert lambda_rank == 6

    w = polynomial_interpolate_mod(alpha, petal_values, prime)
    g_polynomial = [g0_u, 1, 0, 67, 0, 75]
    codeword = polynomial_add_mod(
        substitute_power(w, 7),
        polynomial_multiply_mod(
            substitute_power(phi, 7), g_polynomial, prime
        ),
        prime,
    )
    degree = len(codeword) - 1
    assert degree == 40 <= core_size * 7

    petal_points = []
    for representative, value, scalar, label in zip(
        petal_representatives, petal_values, actual_scalars, alpha
    ):
        for point in subgroup:
            x = representative * point % prime
            petal_points.append(x)
            evaluated = polynomial_evaluate_mod(codeword, x, prime)
            assert evaluated == value
            assert evaluated == (
                scalar * polynomial_evaluate_mod(core_locator, label, prime)
            ) % prime

    retained = []
    missed = []
    core_profile = []
    reconstructed_levels = []
    for representative, beta_value in zip(core_representatives, beta):
        level = (
            -polynomial_evaluate_mod(w, beta_value, prime)
            * pow(polynomial_evaluate_mod(phi, beta_value, prime), -1, prime)
            - g0_u
            - g0_v * beta_value
        ) % prime
        reconstructed_levels.append(level)
        retained_here = 0
        for point in subgroup:
            x = representative * point % prime
            if polynomial_evaluate_mod(codeword, x, prime) == 0:
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

    retained_locator = polynomial_from_roots_mod(retained, prime)
    kernel_quotient, remainder = polynomial_divmod_mod(
        codeword, retained_locator, prime
    )
    assert not remainder
    assert polynomial_multiply_mod(
        kernel_quotient, retained_locator, prime
    ) == codeword
    degree_kernel = len(kernel_quotient) - 1
    assert degree_kernel == 26 <= len(missed) == 28

    # Exact one-point deletion criterion for divisibility minimality.
    deletable = []
    for point in missed:
        enlarged_locator = polynomial_multiply_mod(
            retained_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = polynomial_divmod_mod(
            codeword, enlarged_locator, prime
        )
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    assert deletable == []

    # Negative control: M+{retained[0]} is nonminimal and the same criterion
    # detects precisely the added retained point.
    negative_missed = missed + [retained[0]]
    negative_retained = retained[1:]
    negative_locator = polynomial_from_roots_mod(negative_retained, prime)
    negative_deletable = []
    for point in negative_missed:
        locator_with_point = polynomial_multiply_mod(
            negative_locator, [(-point) % prime, 1], prime
        )
        quotient, rem = polynomial_divmod_mod(
            codeword, locator_with_point, prime
        )
        if not rem and len(quotient) - 1 <= len(negative_missed) - 1:
            negative_deletable.append(point)
    assert negative_deletable == [retained[0]]

    missed_traces = [7 - value for value in core_profile]
    assert missed_traces == [4, 4, 5, 5, 5, 5]
    stabilizer = []
    missed_set = set(missed)
    for multiplier in subgroup:
        if {multiplier * point % prime for point in missed_set} == missed_set:
            stabilizer.append(multiplier)
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
        "gamma_coefficients_X1_through_X6": gamma,
        "spectrum_histogram": [[1, 10], [2, 4], [3, 2]],
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
        "core_retained_profile": core_profile,
        "retained_core": len(retained),
        "total_agreement": agreement,
        "listing_threshold": listing_threshold,
        "exact_missed_core": sorted(missed),
        "exact_missed_core_size": len(missed),
        "kernel_quotient_degree": degree_kernel,
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
            "Upstream has a compatible listed witness in the same "
            "(tau,m,ell) cell, but explicitly with all six nonconstant DFT "
            "sectors active.  It has no exact-three-sector threshold "
            "theorem and no {1,3,5}-sector witness. This certificate separates that "
            "new stratum and does not rebrand the upstream six-sector word."
        ),
    }


def main() -> None:
    four_root = four_root_resultant_sieve()
    triple_invariants = triple_invariant_sieve()
    exceptional_audit = exceptional_state_audit()
    witness = full_witness_113()
    upstream = check_upstream()

    artifact = {
        "title": "ell=7 exact-three-sector proportional threshold and counterexample",
        "status": "COUNTEREXAMPLE_WITH_UNIFORM_THRESHOLD_THEOREM",
        "verdict": "PASS_WITH_ELL7_EXACT_THREE_SECTOR_COUNTEREXAMPLE",
        "uniform_theorem": (
            "For every prime p congruent to 1 mod 7 and every constant-free "
            "Gamma with exactly three active nonzero monomials among "
            "X,...,X^6, the sum S_6 of its six largest mu_7-coset fibers "
            "satisfies S_6<=14 whenever six quotient labels exist.  The "
            "bound is sharp globally but S_6(p) need not equal 14 for each p."
        ),
        "proof": [
            "The normalized integer 4x4 Fourier-minor quotient norms are exactly {1,8}; hence no odd p=1 mod 7 admits a four-point fiber and every coset multiplicity is at most three.",
            "Every triple fiber belongs to one of five translation orbits. Its active coefficient state has the invariant I=(B_s/B_r)^(t-r)/(B_t/B_r)^(s-r), constant along the global core-label monomial curve.",
            "Exact cyclotomic norms separate invariant orbits away from six admissible primes. Characteristic-zero duplicate orbits and the kernel gcd contribute at most two triple cosets. Exact 100-state audits at every exceptional prime also give at most two.",
            "A spectrum with cap three and at most two triple cosets has top-six at most 3+3+2+2+2+2=14.",
            "At p=113 the explicit {1,3,5}-sector Gamma has spectrum 3^2 2^4 1^10 and a lambda-free full-petal reconstruction at equality, proving sharpness and nonvacancy.",
        ],
        "four_root_resultant_sieve": four_root,
        "triple_invariant_sieve": triple_invariants,
        "exceptional_state_audit": exceptional_audit,
        "full_global_counterexample": witness,
        "scope": (
            "Prime fields, ell=7, tau=5, m=6, D=0, background-free full "
            "petals, and exactly three active nonzero DFT sectors.  The "
            "uniform spectrum theorem applies to every such three-sector "
            "support.  The explicit nonvacancy statement is at F_113."
        ),
        "nonclaims": [
            "S_6(p)=14 is not asserted for every prime; exact state audit gives S_6=13 at p=449 and p=463.",
            "No vacancy or classification is claimed for four, five, or six active sectors.",
            "No extension-field theorem is claimed.",
            "The upstream all-six-sector witnesses are compatible and distinct from the new exact-three-sector word.",
        ],
        "operation_counts": {
            "normalized_4x4_minors": four_root["normalized_4x4_minors"],
            "triple_invariant_collision_rows": triple_invariants[
                "invariant_collision_rows"
            ],
            "exceptional_and_control_projective_state_rows": exceptional_audit[
                "total_projective_state_rows"
            ],
            "full_witness_point_evaluations": 77,
            "blind_three_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "Use common-root deficit theorem on the first D>0 exact-three-sector rows, where the "
            "new inputs are a robust partial-support live cap c and the "
            "proportional S_h threshold.  Alternatively classify exact four "
            "active sectors at ell=7; compare theorem-scale payoff before "
            "starting another finite orbit census."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=7 exact-three-sector threshold and counterexample")
    print(
        "minor_norms="
        + str(four_root["quotient_norm_values"])
        + " exceptional="
        + str(triple_invariants["exceptional_admissible_primes"])
    )
    print(
        "state_rows="
        + str(exceptional_audit["total_projective_state_rows"])
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
    print("PASS_WITH_ELL7_EXACT_THREE_SECTOR_COUNTEREXAMPLE")


if __name__ == "__main__":
    main()
