#!/usr/bin/env python3
"""Exact certificate for a two-coset counterexample to literal Conjecture TR.

The terminal-reserve note bounds the product of pooled per-character marginals.
Two qualifying codewords already make every marginal have size two, so the
cartesian product of marginals can have size 2^k although the genuine joint
tuple set has only two points.

For odd primes M large enough, set

    n=2M, k=M-5, A=M, q=3^(M-1).

Choose a dense degree-<k polynomial h with every coefficient nonzero and with
no zero on H_n.  Such an h exists in the one-parameter family

    h_a=1+X+...+X^(k-2)+a X^(k-1),

because each domain point forbids at most one nonzero value of a and q-1>n.
On the two K_M-cosets take c0=h, c1=2h and define the received word piecewise
by c0/c1.  The script verifies the exact prime-field smoke over F_337 and the
integer arithmetic for an asymptotic prime sequence.  Crucially, it also
checks the corridor quantifier without conflating two upstream conventions:
the first `FM<1` level is M-2.  If that level is called `A*`, then
`A=A*+2`; under the offset convention used by the terminal note's pinned row,
`A*=M-3` and `A>A*+2`.  Thus either convention satisfies the literal
quantifier.  The proof of the infinite family is recorded symbolically in the
emitted certificate.
"""

from __future__ import annotations

import json
import itertools
import math
from fractions import Fraction
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "gap1-tr-pooled-marginal-counterexample"
)
SOURCE_TR = (
    REPO_ROOT
    / "experimental"
    / "notes"
    / "roadmaps"
    / "gap1_terminal_reserve.md"
)
SOURCE_TOWER = (
    REPO_ROOT
    / "experimental"
    / "notes"
    / "x1"
    / "x1_gap1_tower_product_bound.md"
)
SOURCE_DAG = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)
ARTIFACT = DATA_DIR / "gap1_tr_pooled_marginal_counterexample.json"


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
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
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ValueError(f"No primitive root found modulo {prime}")


def eval_poly(coefficients: list[int], x: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(coefficients):
        value = (value * x + coefficient) % prime
    return value


def order_is(value: int, order: int, prime: int) -> bool:
    if pow(value, order, prime) != 1:
        return False
    return all(pow(value, order // factor, prime) != 1 for factor in prime_factors(order))


def fm(n: int, k: int, agreement: int, q: int) -> Fraction:
    t = agreement - k
    numerator = math.comb(n, n - agreement)
    if t <= 1:
        return Fraction(numerator * q ** (1 - t), 1)
    return Fraction(numerator, q ** (t - 1))


def first_fm_below_one(n: int, k: int, q: int) -> int:
    """First agreement A>k for which the pinned FM expression is <1."""

    for agreement in range(k + 1, n + 1):
        if fm(n, k, agreement, q) < 1:
            return agreement
    raise AssertionError("FM never crossed below one")


def exact_prime_field_smoke() -> dict[str, object]:
    prime = 337
    period = 7
    n = 14
    k = 2
    agreement = 7
    generator = primitive_root(prime)
    omega = pow(generator, (prime - 1) // n, prime)
    zeta = pow(omega, n // period, prime)
    coset0 = {pow(zeta, exponent, prime) for exponent in range(period)}
    coset1 = {omega * x % prime for x in coset0}
    domain = coset0 | coset1

    # Find the first nonzero last coefficient for which the dense h_a has no
    # zero on H_n.  This is the finite-field replay of the asymptotic union
    # bound (at most n forbidden coefficients among q-1 choices).
    h_parameter = next(
        parameter
        for parameter in range(1, prime)
        if all(
            eval_poly([1] * (k - 1) + [parameter], x, prime) != 0
            for x in domain
        )
    )
    h = [1] * (k - 1) + [h_parameter]
    c0 = h
    c1 = [(2 * coefficient) % prime for coefficient in h]
    word = {
        x: eval_poly(c0 if x in coset0 else c1, x, prime) for x in domain
    }
    agreement0 = {
        x for x in domain if eval_poly(c0, x, prime) == word[x]
    }
    agreement1 = {
        x for x in domain if eval_poly(c1, x, prime) == word[x]
    }

    # Exhaust the entire degree-<2 RS code.  This checks the exact object in
    # Conjecture TR, not just the two planted codewords: a qualifying codeword
    # must have a K_M-stable *exact* agreement set of size at least A.
    qualifying_codewords = []
    for coefficients_tuple in itertools.product(range(prime), repeat=k):
        coefficients = list(coefficients_tuple)
        support = {
            x for x in domain if eval_poly(coefficients, x, prime) == word[x]
        }
        stable = all((zeta * x) % prime in support for x in support)
        if len(support) >= agreement and stable:
            qualifying_codewords.append(
                {
                    "coefficients": coefficients,
                    "support": sorted(support),
                }
            )

    inv_period = pow(period, prime - 2, prime)
    fourier_rows = []
    marginal_values: dict[int, set[int]] = {residue: set() for residue in range(k)}
    for codeword_name, coefficients, support in (
        ("c0", c0, coset0),
        ("c1", c1, coset1),
    ):
        representative = min(support)
        for residue in range(k):
            projected = 0
            for exponent in range(period):
                point = pow(zeta, exponent, prime) * representative % prime
                character = pow(zeta, (-residue * exponent) % period, prime)
                projected = (
                    projected + character * eval_poly(coefficients, point, prime)
                ) % prime
            projected = projected * inv_period % prime
            quotient_value = projected * pow(representative, -residue, prime) % prime
            expected = coefficients[residue] % prime
            marginal_values[residue].add(quotient_value)
            fourier_rows.append(
                {
                    "codeword": codeword_name,
                    "residue": residue,
                    "projected_value": projected,
                    "quotient_constant": quotient_value,
                    "expected_coefficient": expected,
                    "matches": quotient_value == expected,
                }
            )

    product_lower_bound = math.prod(len(values) for values in marginal_values.values())
    fm_value = fm(n, k, agreement, prime)
    first_below_one = first_fm_below_one(n, k, prime)
    qa3_a_star = first_below_one - 1
    a_zero = qa3_a_star + 2
    target_b3 = n**3 * fm_value
    fm_before_crossing = fm(n, k, first_below_one - 1, prime)
    fm_at_crossing = fm(n, k, first_below_one, prime)
    n3_fm_before_zero = n**3 * fm(n, k, a_zero - 1, prime)
    n3_fm_at_zero = n**3 * fm(n, k, a_zero, prime)
    checks = {
        "q_is_prime": is_prime(prime),
        "n_divides_q_minus_one": (prime - 1) % n == 0,
        "omega_has_order_n": order_is(omega, n, prime),
        "zeta_has_order_M": order_is(zeta, period, prime),
        "two_cosets_partition_domain": len(coset0) == period
        and len(coset1) == period
        and coset0.isdisjoint(coset1)
        and len(domain) == n,
        "h_nonzero_on_domain": all(eval_poly(h, x, prime) != 0 for x in domain),
        "agreement_c0_exact_coset0": agreement0 == coset0,
        "agreement_c1_exact_coset1": agreement1 == coset1,
        "all_fourier_components_match_coefficients": all(
            row["matches"] for row in fourier_rows
        ),
        "each_active_marginal_has_two_values": all(
            len(values) == 2 for values in marginal_values.values()
        ),
        "exactly_two_qualifying_codewords": len(qualifying_codewords) == 2,
        "qualifying_codewords_are_c0_c1": {
            tuple(row["coefficients"]) for row in qualifying_codewords
        }
        == {tuple(c0), tuple(c1)},
        "product_lower_bound_is_two_to_k": product_lower_bound == 2**k,
        "fm_below_one": fm_value < 1,
        "fm_crossing_is_exact": fm_before_crossing >= 1 and fm_at_crossing < 1,
        "corridor_under_first_below_convention": agreement
        >= first_below_one + 2,
        "corridor_under_qa3_offset_convention": agreement >= a_zero,
        "qa3_zero_offset_convention_matches": a_zero == qa3_a_star + 2,
        "n3_fm_below_one": target_b3 < 1,
    }
    return {
        "parameters": {
            "q": prime,
            "n": n,
            "M": period,
            "k": k,
            "A": agreement,
            "t": agreement - k,
            "generator": generator,
            "omega": omega,
            "zeta": zeta,
            "h_parameter": h_parameter,
            "first_FM_below_one": first_below_one,
            "qa3_A_star": qa3_a_star,
            "A_zero": a_zero,
        },
        "coset0": sorted(coset0),
        "coset1": sorted(coset1),
        "agreement0": sorted(agreement0),
        "agreement1": sorted(agreement1),
        "fourier_rows": fourier_rows,
        "qualifying_codewords_exhaustive": qualifying_codewords,
        "marginal_values_alpha_one": {
            str(residue): sorted(values) for residue, values in marginal_values.items()
        },
        "joint_tuple_count_exhibited": 2,
        "pooled_marginal_product_lower_bound": product_lower_bound,
        "fm_fraction": f"{fm_value.numerator}/{fm_value.denominator}",
        "n3_fm_fraction": f"{target_b3.numerator}/{target_b3.denominator}",
        "fm_before_crossing_fraction": (
            f"{fm_before_crossing.numerator}/{fm_before_crossing.denominator}"
        ),
        "fm_at_crossing_fraction": (
            f"{fm_at_crossing.numerator}/{fm_at_crossing.denominator}"
        ),
        "n3_fm_before_A_zero_fraction": (
            f"{n3_fm_before_zero.numerator}/{n3_fm_before_zero.denominator}"
        ),
        "n3_fm_at_A_zero_fraction": (
            f"{n3_fm_at_zero.numerator}/{n3_fm_at_zero.denominator}"
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def asymptotic_row(period: int) -> dict[str, object]:
    n = 2 * period
    k = period - 5
    agreement = period
    q = 3 ** (period - 1)
    fm_value = fm(n, k, agreement, q)
    target_b3 = n**3 * fm_value
    product_lower_bound = 2**k
    central_binomial_bound = Fraction(4**period, 3 ** (4 * (period - 1)))
    first_below_one = first_fm_below_one(n, k, q)
    qa3_a_star = first_below_one - 1
    a_zero = qa3_a_star + 2
    fm_t2 = fm(n, k, k + 2, q)
    fm_t3 = fm(n, k, k + 3, q)
    n3_fm_before_zero = n**3 * fm(n, k, a_zero - 1, q)
    n3_fm_at_zero = n**3 * fm(n, k, a_zero, q)
    return {
        "M": period,
        "n": n,
        "k": k,
        "A": agreement,
        "t": agreement - k,
        "q": q,
        "prime_M": is_prime(period),
        "M_mod_3": period % 3,
        "two_M_divides_q_minus_one": (q - 1) % (2 * period) == 0,
        "first_FM_below_one": first_below_one,
        "qa3_A_star": qa3_a_star,
        "A_zero": a_zero,
        "corridor_under_first_below_convention": agreement
        >= first_below_one + 2,
        "corridor_under_qa3_offset_convention": agreement >= a_zero,
        "A_minus_A_zero": agreement - a_zero,
        "fm_t2_fraction": f"{fm_t2.numerator}/{fm_t2.denominator}",
        "fm_t2_at_least_one": fm_t2 >= 1,
        "fm_t3_fraction": f"{fm_t3.numerator}/{fm_t3.denominator}",
        "fm_t3_below_one": fm_t3 < 1,
        "n3_fm_before_A_zero_fraction": (
            f"{n3_fm_before_zero.numerator}/{n3_fm_before_zero.denominator}"
        ),
        "n3_fm_at_A_zero_fraction": (
            f"{n3_fm_at_zero.numerator}/{n3_fm_at_zero.denominator}"
        ),
        "available_h_parameters_lower_bound": q - 1 - n,
        "fm_fraction": f"{fm_value.numerator}/{fm_value.denominator}",
        "fm_below_one": fm_value < 1,
        "n3_fm_below_one": target_b3 < 1,
        "central_binomial_upper_fraction": (
            f"{central_binomial_bound.numerator}/{central_binomial_bound.denominator}"
        ),
        "fm_below_central_bound": fm_value < central_binomial_bound,
        "product_lower_bound": product_lower_bound,
        "required_polynomial_exponent": math.log(product_lower_bound, n),
    }


def dag_statuses() -> dict[str, str]:
    data = json.loads(SOURCE_DAG.read_text(encoding="utf-8"))
    nodes = {str(node["id"]): node for node in data["nodes"]}
    return {
        node_id: str(nodes[node_id]["status"])
        for node_id in (
            "gap1_noneq_mass",
            "gap1_product_model",
            "tr_joint_telescope",
            "tr_perleaf_list_ident",
            "x4_exactlist_staircase_split",
        )
    }


def run() -> dict[str, object]:
    tr_text = SOURCE_TR.read_text(encoding="utf-8")
    tower_text = SOURCE_TOWER.read_text(encoding="utf-8")
    smoke = exact_prime_field_smoke()
    periods = [11, 17, 23, 29, 41, 47, 53, 59, 71, 83]
    rows = [asymptotic_row(period) for period in periods]
    statuses = dag_statuses()

    checks = {
        "literal_tr_product_statement_present": (
            "product_{r in R} |A_r(w, A, M, alpha)|" in tr_text
        ),
        "literal_tr_quantifier_uniform_in_R_present": (
            "every active set `R subseteq Z/M`" in tr_text
        ),
        "tower_note_only_claims_product_upper_bound": (
            "multi-isotypic slope set is bounded by the product" in tower_text
            and "does not by itself" in tower_text
        ),
        "exact_prime_field_smoke_passed": bool(smoke["all_checks_pass"]),
        "all_periods_are_odd_primes": all(
            row["prime_M"] and int(row["M"]) % 2 == 1 for row in rows
        ),
        "all_rows_have_valid_cyclic_domain": all(
            row["two_M_divides_q_minus_one"] for row in rows
        ),
        "all_rows_have_dense_nonvanishing_h_available": all(
            int(row["available_h_parameters_lower_bound"]) > 0 for row in rows
        ),
        "all_rows_satisfy_qa3_corridor_quantifier": all(
            row["corridor_under_first_below_convention"]
            and row["corridor_under_qa3_offset_convention"]
            and int(row["A_minus_A_zero"]) >= 0
            and row["fm_t2_at_least_one"]
            and row["fm_t3_below_one"]
            for row in rows
        ),
        "all_rows_are_past_b3_zero_crossing": all(
            row["n3_fm_below_one"] for row in rows
        ),
        "all_fm_bounds_match_central_estimate": all(
            row["fm_below_central_bound"] for row in rows
        ),
        "required_polynomial_exponents_grow_on_sample": all(
            float(rows[index + 1]["required_polynomial_exponent"])
            > float(rows[index]["required_polynomial_exponent"])
            for index in range(len(rows) - 1)
        ),
        "dag_keeps_gap1_open": statuses["gap1_noneq_mass"] == "CONJECTURE"
        and statuses["gap1_product_model"] == "CONJECTURE",
        "dag_joint_node_and_live_targets_recorded": statuses["tr_joint_telescope"]
        == "PROVED"
        and statuses["tr_perleaf_list_ident"] == "TARGET"
        and statuses["x4_exactlist_staircase_split"] == "TARGET",
    }

    return {
        "title": "Two-coset pooled-marginal counterexample to literal TR",
        "status": "COUNTEREXAMPLE_TO_LITERAL_CONJECTURE_TR",
        "verdict": "COUNTEREXAMPLE",
        "scope": (
            "Refutes the uniform product-of-pooled-marginals inequality stated as "
            "Conjecture TR in gap1_terminal_reserve.md.  It does not refute a "
            "corrected theorem for the genuine joint tuple set or a support-stratified sum."
        ),
        "sources": [
            display_path(SOURCE_TR),
            display_path(SOURCE_TOWER),
            display_path(SOURCE_DAG),
        ],
        "theorem_statement": (
            "For arbitrarily large odd primes M, set n=2M, k=M-5, A=M, "
            "q=3^(M-1).  There exist a received word w, an active set R of size "
            "k, and even a nondegenerate Kummer tower such that every agreement "
            "support used is exactly K_M-stable at an agreement satisfying "
            "A>=A*+2 under either upstream crossing convention, but "
            "product_r |A_r| >= 2^(M-5), while FM<1 and n^3 FM<1.  Hence no "
            "absolute exponent B_TR can satisfy the literal TR inequality."
        ),
        "construction": {
            "parameters": (
                "n=2M, k=M-5, first(FM<1)=M-2, A=M; hence A=A*+2 "
                "if A* means first-below, and A=A*+3 under the terminal "
                "note's pinned offset convention; q=3^(M-1)"
            ),
            "domain": "H_n=S_0 disjoint_union S_1, the two K_M cosets",
            "polynomials": (
                "h_a=sum_{r=0}^{k-2} X^r + a X^(k-1), with a avoiding at "
                "most n forbidden values; c0=h_a, c1=2h_a"
            ),
            "received_word": "w=c0 on S0 and w=c1 on S1",
            "active_set": "R={0,...,k-1}",
            "marginals": (
                "Writing b_r for the nonzero coefficient of X^r in h_a, "
                "A_r contains {alpha^r b_r, 2 alpha^r b_r} for every r in R"
            ),
        },
        "proof_certificate": [
            "There are arbitrarily large odd primes (Euclid), so the construction is asymptotic.",
            "Fermat gives M | 3^(M-1)-1 and parity gives 2M | q-1, so H_n exists.",
            "In the family h_a=sum_{r<k-1}X^r+aX^(k-1), each x in H_n forbids at most one a; q-1>2M leaves a nonzero choice, and every coefficient is nonzero.",
            "Therefore Agr(c0,w)=S0 and Agr(c1,w)=S1 exactly.",
            "Because k<M, every active residue contains one monomial with nonzero coefficient b_r: the two quotient amplitudes are b_r and 2b_r, so each pooled marginal has size at least two.",
            "The only K_M-stable supports of size at least M are S0, S1, and H_n. Fixed-support uniqueness gives c0 and c1 on the first two, while H_n is impossible because c0 != c1; hence the genuine joint tuple set has exactly two points.",
            "At t=2, FM=C(2M,M+3)/q>1 for all sufficiently large M, while at t=3 it is C(2M,M+2)/q^2<1. Thus first(FM<1)=M-2. If this is A*, A=M=A*+2; under the terminal note's pinned offset convention A*=M-3 and A=M=A*+3. Either way the literal A>=A*+2 quantifier holds.",
            "At A, FM=C(2M,M)/q^4 < 81*(4/81)^M and (2M)^3 FM tends to zero.",
            "For every fixed B, 2^(M-5)/(2M)^B tends to infinity.",
            "For a nondegenerate tower, take beta primitive and alpha^M=beta; since mu_M lies in F_q and beta is not an M-th power, F_q(alpha)/F_q has degree M.",
        ],
        "exact_prime_field_smoke": smoke,
        "asymptotic_rows": rows,
        "object_repair": {
            "joint_tuple_set": (
                "J_R(w)={(alpha^r G_r(beta))_{r in R}: one qualifying codeword c}"
            ),
            "witness_joint_size": 2,
            "witness_pooled_marginal_product": "2^k",
            "recommended_correction": (
                "Bound |J_R(w)| or a support-stratified sum, not the cartesian "
                "product of marginals pooled across different codewords."
            ),
        },
        "source_alignment": {
            "commit": "c35a6da31ed0905afcbaaefe4eb0f242572ebb35",
            "dag_statuses": statuses,
            "source_boundary": (
                "The tr_joint_telescope proof source is not present in the inspected "
                "tree.  Determine whether that node controls the genuine joint set (then "
                "it is compatible) or the literal pooled marginal product (then this "
                "counterexample falsifies its lifting interpretation)."
            ),
        },
        "next_obligation": (
            "Replace literal TR by a joint-tuple/support-stratified reserve and audit "
            "the upstream telescope definition before consuming the corrected "
            "per-leaf ExactList target."
        ),
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }


def main() -> int:
    out = run()
    ARTIFACT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    smoke = out["exact_prime_field_smoke"]
    last = out["asymptotic_rows"][-1]
    print(out["title"])
    print(
        f"verdict={out['verdict']} smoke_product={smoke['pooled_marginal_product_lower_bound']} "
        f"smoke_joint={smoke['joint_tuple_count_exhibited']} "
        f"smoke_n3FM={smoke['n3_fm_fraction']}"
    )
    print(
        f"rows={len(out['asymptotic_rows'])} last_M={last['M']} "
        f"last_product={last['product_lower_bound']} "
        f"required_B={last['required_polynomial_exponent']:.3f}"
    )
    if not out["all_checks_pass"]:
        print("FAIL")
        for key, value in out["checks"].items():
            if not value:
                print("  -", key)
        return 1
    print("PASS_WITH_TWO_COSET_MARGINAL_TR_COUNTEREXAMPLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
