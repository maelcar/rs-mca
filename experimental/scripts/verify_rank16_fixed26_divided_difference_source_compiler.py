#!/usr/bin/env python3
"""Fail-closed replay for the fixed-26 source compiler and monomial cap 37."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from functools import lru_cache
from math import comb, isqrt
from pathlib import Path
from typing import Any, Callable


class VerificationError(RuntimeError):
    """Raised when any pinned theorem, artifact, or self-test check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError("CHECK FAILED: " + message)


SCRIPT_PATH = Path(__file__).resolve()
REPO_ROOT = SCRIPT_PATH.parents[2]
CERT_REL = (
    "experimental/data/certificates/"
    "rank16-fixed26-divided-difference-source-compiler"
)
CERT_DIR = REPO_ROOT / CERT_REL
MANIFEST_PATH = CERT_DIR / "manifest.json"
EXPECTED_PATH = CERT_DIR / "verify_fixed26_compiler.expected.txt"
CHECKSUM_PATH = CERT_DIR / "SHA256SUMS.txt"

NOTE_REL = "experimental/notes/l2/rank16_fixed26_divided_difference_source_compiler.md"
SCRIPT_REL = (
    "experimental/scripts/"
    "verify_rank16_fixed26_divided_difference_source_compiler.py"
)
MANIFEST_REL = CERT_REL + "/manifest.json"
EXPECTED_REL = CERT_REL + "/verify_fixed26_compiler.expected.txt"
ARTIFACTS = (NOTE_REL, SCRIPT_REL, MANIFEST_REL, EXPECTED_REL)

SCHEMA = "rs-mca.rank16-fixed26-divided-difference-source-compiler.v1"
BASE = "9c4ca98cf45639407611a3ad5154893fb22e77e2"
OVERLAP_BASELINE = (826, 838, 843, 844)

IDENTITIES = (
    "F_y V_y=xi+g S_y",
    "V_y-V_z=(y-z)U_yz",
    "F_z U_yz=V_y+g Q_yz",
    "F_y U_yz=V_z+g Q_yz",
    "F_y F_z U_yz=xi+g P_yz",
    "U_yz=rem_g(xi(F_y F_z)^-1)",
    "G_C F_y F_z R_yz=q_yz eta+g q_yz(A_C+G_C P_yz)",
    "F_z R_yz=q_yz V_y+g q_yz Q_yz",
    "deg U_yz<=r iff tau_y=tau_z",
    "deg U_yz=r iff tau_y=tau_z and c_y!=c_z",
    "S_y=-y^-3 A_0-y^-2 A_1-y^-1 A_2 for g=X^a",
)

FILTERS = (
    "exact_degree_and_monic_normalization",
    "squarefree",
    "complete_H_splitting",
    "avoid_selected_complete_fibers",
    "no_additional_q64_fiber",
    "residual_q64_footprint_at_least_4",
    "not_fourteen_natural_q32_pairs",
    "outside_prior_agreement_and_paired_owners",
    "actual_canonical_first_match",
)


def manifest_contract(expected_sha256: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "base": BASE,
        "open_overlap_baseline": list(OVERLAP_BASELINE),
        "theorem": {
            "field_prime": 2_130_706_433,
            "domain_order": 2_097_152,
            "fiber_label_order": 64,
            "fiber_size_B": 32_768,
            "fixed_core_labels": 26,
            "remaining_labels": 38,
            "pair_positions": 703,
            "generator_degree_a": 67_472,
            "monomial_generator": "X^67472",
            "s": 1_936,
            "residual_degree_r": 63_601,
            "pade_degree_D": 61_665,
            "normalized_degree_d": 28_897,
            "tail_length": 3_870,
            "monomial_edge_cap": 37,
        },
        "identity_contract": list(IDENTITIES),
        "validity_filters": list(FILTERS),
        "monomial_proof_contract": {
            "tail_map_degree_at_most": 3,
            "nonconstant_class_size_at_most": 3,
            "label_count": 38,
            "max_edges": 37,
            "zero_tail_forces_X_power_divisor": 1_936,
            "H_excludes_zero": True,
        },
        "scope": {
            "arbitrary_g_cap_116": False,
            "source_realized_117_family": False,
            "finite_payment": False,
            "parent_closure": False,
            "grand_list": False,
            "grand_mca": False,
            "score_movement": False,
            "ledger_values_included": False,
            "pr843_rank2_classification_carved_out": True,
            "pr844_claims_carved_out": True,
        },
        "expected_output": {
            "path": EXPECTED_REL,
            "sha256": expected_sha256,
        },
        "artifacts": list(ARTIFACTS),
    }


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError("duplicate JSON key: " + key)
        result[key] = value
    return result


def load_manifest() -> dict[str, Any]:
    try:
        raw = MANIFEST_PATH.read_text(encoding="ascii")
    except (OSError, UnicodeError) as exc:
        raise VerificationError("cannot read ASCII manifest") from exc
    try:
        value = json.loads(raw, object_pairs_hook=reject_duplicate_keys)
    except (json.JSONDecodeError, VerificationError) as exc:
        raise VerificationError("invalid manifest JSON") from exc
    require(type(value) is dict, "manifest root must be an object")
    return value


def validate_manifest(value: dict[str, Any]) -> None:
    output = value.get("expected_output")
    require(type(output) is dict, "expected_output object")
    digest = output.get("sha256")
    require(
        type(digest) is str and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
        "expected output SHA-256 syntax",
    )
    require(value == manifest_contract(digest), "semantic manifest contract")


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_artifacts(manifest: dict[str, Any]) -> int:
    require(CHECKSUM_PATH.is_file(), "checksum file exists")
    raw = CHECKSUM_PATH.read_bytes()
    require(raw.endswith(b"\n"), "checksum file final newline")
    try:
        lines = raw.decode("ascii").splitlines()
    except UnicodeError as exc:
        raise VerificationError("checksum file is not ASCII") from exc

    expected_paths = tuple(manifest["artifacts"])
    require(len(lines) == len(expected_paths), "checksum entry count")
    pattern = re.compile(r"([0-9a-f]{64})  ([!-~]+)")

    seen: list[str] = []
    for line, relative in zip(lines, expected_paths):
        match = pattern.fullmatch(line)
        require(match is not None, "checksum line syntax")
        digest, listed = match.groups()
        require(listed == relative, "checksum path order for " + relative)
        path = (REPO_ROOT / listed).resolve()
        require(REPO_ROOT == path or REPO_ROOT in path.parents, "artifact path confinement")
        require(path.is_file(), "artifact exists: " + listed)
        require(sha256_path(path) == digest, "artifact digest: " + listed)
        require(listed not in seen, "duplicate checksum path: " + listed)
        seen.append(listed)

    output = manifest["expected_output"]
    require(output["path"] == EXPECTED_REL, "expected output path pin")
    require(
        sha256_path(EXPECTED_PATH) == output["sha256"],
        "expected output digest pin",
    )
    return len(seen)


Poly = tuple[int, ...]


def poly(values: Any, prime: int) -> Poly:
    result = [int(value) % prime for value in values]
    if not result:
        result = [0]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return tuple(result)


def poly_zero(value: Poly) -> bool:
    return value == (0,)


def poly_degree(value: Poly) -> int:
    return -1 if poly_zero(value) else len(value) - 1


def poly_coeff(value: Poly, index: int) -> int:
    return value[index] if 0 <= index < len(value) else 0


def poly_add(left: Poly, right: Poly, prime: int) -> Poly:
    length = max(len(left), len(right))
    return poly(
        (poly_coeff(left, i) + poly_coeff(right, i) for i in range(length)),
        prime,
    )


def poly_sub(left: Poly, right: Poly, prime: int) -> Poly:
    length = max(len(left), len(right))
    return poly(
        (poly_coeff(left, i) - poly_coeff(right, i) for i in range(length)),
        prime,
    )


def poly_scale(value: Poly, scalar: int, prime: int) -> Poly:
    return poly((scalar * coefficient for coefficient in value), prime)


def poly_mul(left: Poly, right: Poly, prime: int) -> Poly:
    if poly_zero(left) or poly_zero(right):
        return (0,)
    result = [0] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] = (result[i + j] + left_value * right_value) % prime
    return poly(result, prime)


def poly_divmod(numerator: Poly, denominator: Poly, prime: int) -> tuple[Poly, Poly]:
    require(not poly_zero(denominator), "polynomial division by zero")
    remainder = list(numerator)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    inverse_lead = pow(denominator[-1], -1, prime)

    while not (len(remainder) == 1 and remainder[0] % prime == 0):
        while len(remainder) > 1 and remainder[-1] % prime == 0:
            remainder.pop()
        if len(remainder) < len(denominator):
            break
        shift = len(remainder) - len(denominator)
        factor = remainder[-1] * inverse_lead % prime
        quotient[shift] = factor
        for index, value in enumerate(denominator):
            target = index + shift
            remainder[target] = (remainder[target] - factor * value) % prime

    return poly(quotient, prime), poly(remainder, prime)


def poly_mod(value: Poly, modulus: Poly, prime: int) -> Poly:
    return poly_divmod(value, modulus, prime)[1]


def poly_exact_quotient(numerator: Poly, denominator: Poly, prime: int) -> Poly:
    quotient, remainder = poly_divmod(numerator, denominator, prime)
    require(poly_zero(remainder), "nonexact polynomial quotient")
    return quotient


def poly_inverse_mod(value: Poly, modulus: Poly, prime: int) -> Poly:
    old_r, current_r = value, modulus
    old_s, current_s = (1,), (0,)

    while not poly_zero(current_r):
        quotient, remainder = poly_divmod(old_r, current_r, prime)
        old_r, current_r = current_r, remainder
        old_s, current_s = current_s, poly_sub(
            old_s, poly_mul(quotient, current_s, prime), prime
        )

    require(poly_degree(old_r) == 0 and old_r[0] != 0, "polynomial inverse exists")
    normalized = poly_scale(old_s, pow(old_r[0], -1, prime), prime)
    return poly_mod(normalized, modulus, prime)


def x_power(exponent: int, prime: int) -> Poly:
    require(exponent >= 0, "nonnegative monomial exponent")
    return poly([0] * exponent + [1], prime)


def fiber_factor(label: int, size: int, prime: int) -> Poly:
    values = [0] * (size + 1)
    values[0] = -label
    values[size] = 1
    return poly(values, prime)


def product(values: list[Poly], prime: int) -> Poly:
    result: Poly = (1,)
    for value in values:
        result = poly_mul(result, value, prime)
    return result


def divisible_by_x_power(value: Poly, exponent: int) -> bool:
    return all(poly_coeff(value, index) == 0 for index in range(exponent))


def monomial_s_formula(xi: Poly, label: int, size: int, s: int, prime: int) -> Poly:
    a = 2 * size + s
    require(poly_degree(xi) < a, "monomial formula input degree")
    a0 = [0] * size
    a1 = [0] * size
    a2 = [0] * size

    for index in range(s):
        a0[index + size - s] = poly_coeff(xi, index)
    for index in range(s, size + s):
        a1[index - s] = poly_coeff(xi, index)
    for index in range(size + s, 2 * size + s):
        a2[index - size - s] = poly_coeff(xi, index)

    inverse = pow(label, -1, prime)
    result = poly_scale(poly(a0, prime), -pow(inverse, 3, prime), prime)
    result = poly_add(
        result,
        poly_scale(poly(a1, prime), -pow(inverse, 2, prime), prime),
        prime,
    )
    result = poly_add(
        result,
        poly_scale(poly(a2, prime), -inverse, prime),
        prime,
    )
    return result


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    ceiling = isqrt(value)
    while divisor <= ceiling:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def verify_deployed_parameters(manifest: dict[str, Any]) -> None:
    theorem = manifest["theorem"]
    prime = theorem["field_prime"]
    n = theorem["domain_order"]
    size = theorem["fiber_size_B"]
    generator_degree = theorem["generator_degree_a"]
    s = theorem["s"]
    residual_degree = theorem["residual_degree_r"]
    pade_degree = theorem["pade_degree_D"]
    normalized_degree = theorem["normalized_degree_d"]

    m = 1_116_047
    k = 1_048_576
    u = 1_043_459
    t = n - m
    h = k - u - 1
    active = m - u

    require(is_prime(prime), "deployed p is prime")
    require(prime - 1 == 1_016 * n, "H and Omega embed in F_p^*")
    require(n == theorem["fiber_label_order"] * size, "q64 fiber size")
    require((t, h, active) == (981_105, 5_116, 72_588), "deployed source inputs")
    require(generator_degree == active - h == 2 * size + s, "generator degree")
    require(residual_degree == t - 28 * size == 2 * size - s + 1, "residual degree")
    require(pade_degree == 2 * size + residual_degree - generator_degree, "Pade degree")
    require(pade_degree == residual_degree - s, "Pade degree alternate form")
    require(normalized_degree == pade_degree - size == size - 2 * s + 1, "normalized degree")
    require(size - normalized_degree - 1 == theorem["tail_length"], "tail length")
    require(comb(theorem["remaining_labels"], 2) == theorem["pair_positions"], "pair positions")
    require(theorem["monomial_generator"] == "X^" + str(generator_degree), "monomial label")


def replay_source_algebra() -> dict[str, int]:
    prime = 257
    size = 8
    s = 2
    a = 2 * size + s
    residual_degree = 2 * size - s + 1
    d = size - 2 * s + 1
    modulus = x_power(a, prime)

    omega = pow(3, 16, prime)
    require(pow(omega, 16, prime) == 1, "toy mu16 closure")
    require(pow(omega, 8, prime) != 1, "toy mu16 exact order")
    labels = [pow(omega, index, prime) for index in range(16)]
    require(len(set(labels)) == 16 and 0 not in labels, "toy labels distinct and nonzero")

    core_indices = (0, 8, 1, 9)
    core = [labels[index] for index in core_indices]
    remaining = [label for index, label in enumerate(labels) if index not in core_indices]
    require(len(remaining) == 12, "toy remaining labels")
    require({(-label) % prime for label in remaining} == set(remaining), "toy sign closure")

    factors = {label: fiber_factor(label, size, prime) for label in labels}
    core_product = product([factors[label] for label in core], prime)
    inverse_core = poly_inverse_mod(core_product, modulus, prime)

    generic_one = poly((17 * index * index + 31 * index + 7 for index in range(a)), prime)
    generic_two = poly((19 * index * index * index + 5 * index + 11 for index in range(a)), prime)

    controlled_values = [0] * a
    controlled_values[8] = 1
    controlled_values[15] = 3
    controlled = poly(controlled_values, prime)

    zero_tail_values = [0] * a
    zero_tail_values[2] = 5
    zero_tail_values[3] = 7
    zero_tail_values[7] = 11
    zero_tail_values[15] = 13
    zero_tail = poly(zero_tail_values, prime)
    xi_instances = (generic_one, generic_two, controlled, zero_tail)

    pair_checks = 0
    formula_checks = 0
    exact_candidates = 0
    zero_tail_divisibility_checks = 0

    for instance_index, xi in enumerate(xi_instances):
        eta = poly_mod(poly_mul(core_product, xi, prime), modulus, prime)
        require(not poly_zero(eta), "toy nonzero residue")
        recovered = poly_mod(poly_mul(inverse_core, eta, prime), modulus, prime)
        require(recovered == xi, "toy source xi recovery")
        a_core = poly_exact_quotient(
            poly_sub(poly_mul(core_product, xi, prime), eta, prime),
            modulus,
            prime,
        )

        one_label: dict[int, tuple[Poly, Poly]] = {}
        for label in remaining:
            inverse_factor = poly_inverse_mod(factors[label], modulus, prime)
            v_label = poly_mod(poly_mul(xi, inverse_factor, prime), modulus, prime)
            s_label = poly_exact_quotient(
                poly_sub(poly_mul(factors[label], v_label, prime), xi, prime),
                modulus,
                prime,
            )
            require(poly_degree(v_label) < a, "toy V degree")
            require(poly_degree(s_label) < size, "toy S degree")
            require(
                poly_mul(factors[label], v_label, prime)
                == poly_add(xi, poly_mul(modulus, s_label, prime), prime),
                "toy one-label source identity",
            )
            require(
                s_label == monomial_s_formula(xi, label, size, s, prime),
                "toy monomial S formula",
            )
            formula_checks += 1
            one_label[label] = (v_label, s_label)

        for left_index, y in enumerate(remaining):
            for z in remaining[left_index + 1 :]:
                pair_checks += 1
                v_y, s_y = one_label[y]
                v_z, s_z = one_label[z]
                inverse_difference = pow((y - z) % prime, -1, prime)
                u_yz = poly_scale(poly_sub(v_y, v_z, prime), inverse_difference, prime)
                q_yz = poly_scale(poly_sub(s_y, s_z, prime), inverse_difference, prime)
                p_yz = poly_add(s_y, poly_mul(factors[y], q_yz, prime), prime)

                require(
                    poly_sub(v_y, v_z, prime)
                    == poly_scale(u_yz, y - z, prime),
                    "toy divided difference",
                )
                require(
                    poly_mul(factors[z], u_yz, prime)
                    == poly_add(v_y, poly_mul(modulus, q_yz, prime), prime),
                    "toy F_z resolvent",
                )
                require(
                    poly_mul(factors[y], u_yz, prime)
                    == poly_add(v_z, poly_mul(modulus, q_yz, prime), prime),
                    "toy F_y resolvent",
                )
                require(
                    poly_mul(poly_mul(factors[y], factors[z], prime), u_yz, prime)
                    == poly_add(xi, poly_mul(modulus, p_yz, prime), prime),
                    "toy pair source identity",
                )

                inverse_pair = poly_inverse_mod(
                    poly_mul(factors[y], factors[z], prime), modulus, prime
                )
                require(
                    u_yz == poly_mod(poly_mul(xi, inverse_pair, prime), modulus, prime),
                    "toy pair remainder identity",
                )

                tail_y = tuple(poly_coeff(s_y, index) for index in range(d + 1, size))
                tail_z = tuple(poly_coeff(s_z, index) for index in range(d + 1, size))
                c_y = poly_coeff(s_y, d)
                c_z = poly_coeff(s_z, d)
                degree_at_most = poly_degree(u_yz) <= residual_degree
                exact_degree = poly_degree(u_yz) == residual_degree
                require(degree_at_most == (tail_y == tail_z), "toy degree-tail equivalence")
                require(
                    exact_degree == (tail_y == tail_z and c_y != c_z),
                    "toy exact-degree criterion",
                )

                if exact_degree:
                    exact_candidates += 1
                    expected_lead = (c_y - c_z) * inverse_difference % prime
                    require(u_yz[-1] == expected_lead, "toy U leading coefficient")
                    require(q_yz[-1] == expected_lead, "toy Q leading coefficient")
                    monic_scalar = (y - z) * pow((c_y - c_z) % prime, -1, prime) % prime
                    residual = poly_scale(u_yz, monic_scalar, prime)
                    require(
                        poly_degree(residual) == residual_degree and residual[-1] == 1,
                        "toy monic residual",
                    )

                    left = poly_mul(
                        poly_mul(
                            poly_mul(core_product, factors[y], prime),
                            factors[z],
                            prime,
                        ),
                        residual,
                        prime,
                    )
                    source_tail = poly_add(
                        a_core, poly_mul(core_product, p_yz, prime), prime
                    )
                    right = poly_add(
                        poly_scale(eta, monic_scalar, prime),
                        poly_mul(
                            modulus,
                            poly_scale(source_tail, monic_scalar, prime),
                            prime,
                        ),
                        prime,
                    )
                    require(left == right, "toy fixed-26 source-ray reconstruction")
                    require(
                        poly_mul(factors[z], residual, prime)
                        == poly_add(
                            poly_scale(v_y, monic_scalar, prime),
                            poly_mul(
                                modulus,
                                poly_scale(q_yz, monic_scalar, prime),
                                prime,
                            ),
                            prime,
                        ),
                        "toy fixed-27 interface",
                    )

                if instance_index == len(xi_instances) - 1:
                    require(divisible_by_x_power(xi, s), "toy zero-tail xi divisor")
                    require(divisible_by_x_power(u_yz, s), "toy zero-tail U divisor")
                    zero_tail_divisibility_checks += 1

    require(pair_checks == len(xi_instances) * comb(len(remaining), 2), "toy pair check count")
    require(formula_checks == len(xi_instances) * len(remaining), "toy formula count")
    require(exact_candidates > 0, "toy exact-degree branch exercised")
    require(zero_tail_divisibility_checks == comb(len(remaining), 2), "zero-tail branch coverage")
    return {
        "instances": len(xi_instances),
        "pair_checks": pair_checks,
        "formula_checks": formula_checks,
    }


def replay_nonmonomial_source_algebra() -> dict[str, int]:
    prime = 257
    size = 8
    s = 2
    a = 2 * size + s
    residual_degree = 2 * size - s + 1
    d = size - 2 * s + 1
    modulus = poly_add(x_power(a, prime), poly((1, 1), prime), prime)
    require(modulus != x_power(a, prime), "nonmonomial modulus")
    require(poly_degree(modulus) == a and modulus[-1] == 1, "nonmonomial monic degree")

    omega = pow(3, 16, prime)
    labels = [pow(omega, index, prime) for index in range(16)]
    core_indices = (0, 8, 1, 9)
    core = [labels[index] for index in core_indices]
    remaining = [label for index, label in enumerate(labels) if index not in core_indices]
    factors = {label: fiber_factor(label, size, prime) for label in labels}

    # Invertibility of all 16 factors is the toy root-free check because their
    # product is X^128-1, the polynomial of the toy H=mu_128 domain.
    inverse_factors = {
        label: poly_inverse_mod(factors[label], modulus, prime) for label in labels
    }
    core_product = product([factors[label] for label in core], prime)
    inverse_core = poly_inverse_mod(core_product, modulus, prime)

    xi_instances = (
        poly((23 * index * index + 9 * index + 5 for index in range(a)), prime),
        poly((29 * index * index * index + 13 * index + 17 for index in range(a)), prime),
    )
    pair_checks = 0

    for xi in xi_instances:
        eta = poly_mod(poly_mul(core_product, xi, prime), modulus, prime)
        require(not poly_zero(eta), "nonmonomial nonzero residue")
        require(
            poly_mod(poly_mul(inverse_core, eta, prime), modulus, prime) == xi,
            "nonmonomial source xi recovery",
        )
        a_core = poly_exact_quotient(
            poly_sub(poly_mul(core_product, xi, prime), eta, prime),
            modulus,
            prime,
        )

        one_label: dict[int, tuple[Poly, Poly]] = {}
        for label in remaining:
            v_label = poly_mod(
                poly_mul(xi, inverse_factors[label], prime), modulus, prime
            )
            s_label = poly_exact_quotient(
                poly_sub(poly_mul(factors[label], v_label, prime), xi, prime),
                modulus,
                prime,
            )
            require(poly_degree(v_label) < a, "nonmonomial V degree")
            require(poly_degree(s_label) < size, "nonmonomial S degree")
            require(
                poly_mul(factors[label], v_label, prime)
                == poly_add(xi, poly_mul(modulus, s_label, prime), prime),
                "nonmonomial one-label source identity",
            )
            one_label[label] = (v_label, s_label)

        for left_index, y in enumerate(remaining):
            for z in remaining[left_index + 1 :]:
                pair_checks += 1
                v_y, s_y = one_label[y]
                v_z, s_z = one_label[z]
                inverse_difference = pow((y - z) % prime, -1, prime)
                u_yz = poly_scale(poly_sub(v_y, v_z, prime), inverse_difference, prime)
                q_yz = poly_scale(poly_sub(s_y, s_z, prime), inverse_difference, prime)
                p_yz = poly_add(s_y, poly_mul(factors[y], q_yz, prime), prime)

                require(
                    poly_mul(factors[z], u_yz, prime)
                    == poly_add(v_y, poly_mul(modulus, q_yz, prime), prime),
                    "nonmonomial F_z resolvent",
                )
                require(
                    poly_mul(factors[y], u_yz, prime)
                    == poly_add(v_z, poly_mul(modulus, q_yz, prime), prime),
                    "nonmonomial F_y resolvent",
                )
                require(
                    poly_mul(poly_mul(factors[y], factors[z], prime), u_yz, prime)
                    == poly_add(xi, poly_mul(modulus, p_yz, prime), prime),
                    "nonmonomial pair source identity",
                )
                require(
                    u_yz
                    == poly_mod(
                        poly_mul(
                            xi,
                            poly_inverse_mod(
                                poly_mul(factors[y], factors[z], prime),
                                modulus,
                                prime,
                            ),
                            prime,
                        ),
                        modulus,
                        prime,
                    ),
                    "nonmonomial pair remainder identity",
                )

                tail_y = tuple(poly_coeff(s_y, index) for index in range(d + 1, size))
                tail_z = tuple(poly_coeff(s_z, index) for index in range(d + 1, size))
                c_y = poly_coeff(s_y, d)
                c_z = poly_coeff(s_z, d)
                require(
                    (poly_degree(u_yz) <= residual_degree) == (tail_y == tail_z),
                    "nonmonomial degree-tail equivalence",
                )
                require(
                    (poly_degree(u_yz) == residual_degree)
                    == (tail_y == tail_z and c_y != c_z),
                    "nonmonomial exact-degree criterion",
                )

                source_left = poly_mul(
                    poly_mul(
                        poly_mul(core_product, factors[y], prime), factors[z], prime
                    ),
                    u_yz,
                    prime,
                )
                source_right = poly_add(
                    eta,
                    poly_mul(
                        modulus,
                        poly_add(a_core, poly_mul(core_product, p_yz, prime), prime),
                        prime,
                    ),
                    prime,
                )
                require(source_left == source_right, "nonmonomial source-ray reconstruction")

    require(pair_checks == len(xi_instances) * comb(len(remaining), 2), "nonmonomial pair count")
    return {"instances": len(xi_instances), "pair_checks": pair_checks}


@lru_cache(maxsize=None)
def max_partition_edges(total: int, largest_part: int) -> int:
    if total == 0:
        return 0
    best = -1
    for part in range(1, min(total, largest_part) + 1):
        tail = max_partition_edges(total - part, part)
        if tail >= 0:
            best = max(best, comb(part, 2) + tail)
    return best


def verify_monomial_cap(manifest: dict[str, Any]) -> int:
    theorem = manifest["theorem"]
    proof = manifest["monomial_proof_contract"]
    labels = proof["label_count"]
    class_cap = proof["nonconstant_class_size_at_most"]
    quotient, remainder = divmod(labels, class_cap)
    convex_bound = quotient * comb(class_cap, 2) + comb(remainder, 2)
    exhaustive_bound = max_partition_edges(labels, class_cap)

    require(proof["tail_map_degree_at_most"] == 3, "cubic tail map")
    require(labels > proof["tail_map_degree_at_most"], "zero cubic root threshold")
    require(convex_bound == exhaustive_bound == 37, "finite 38-label cap")
    require(theorem["monomial_edge_cap"] == exhaustive_bound, "manifest monomial cap")
    require(
        proof["zero_tail_forces_X_power_divisor"] == theorem["s"] > 0,
        "zero-tail positive X divisor",
    )
    require(proof["H_excludes_zero"] is True, "H excludes zero")
    return exhaustive_bound


def semantic_tamper_selftests(manifest: dict[str, Any]) -> int:
    def set_generator_degree(value: dict[str, Any]) -> None:
        value["theorem"]["generator_degree_a"] += 1

    def set_cap(value: dict[str, Any]) -> None:
        value["theorem"]["monomial_edge_cap"] = 38

    def claim_arbitrary_g(value: dict[str, Any]) -> None:
        value["scope"]["arbitrary_g_cap_116"] = True

    def claim_payment(value: dict[str, Any]) -> None:
        value["scope"]["finite_payment"] = True

    def add_ledger(value: dict[str, Any]) -> None:
        value["scope"]["ledger_values_included"] = True

    def remove_overlap(value: dict[str, Any]) -> None:
        value["open_overlap_baseline"].remove(844)

    def reclaim_pr843(value: dict[str, Any]) -> None:
        value["scope"]["pr843_rank2_classification_carved_out"] = False

    def reclaim_pr844(value: dict[str, Any]) -> None:
        value["scope"]["pr844_claims_carved_out"] = False

    def alter_identity(value: dict[str, Any]) -> None:
        value["identity_contract"][2] = "F_z U_yz=V_y-g Q_yz"

    def drop_split_filter(value: dict[str, Any]) -> None:
        value["validity_filters"].remove("complete_H_splitting")

    def alter_pair_count(value: dict[str, Any]) -> None:
        value["theorem"]["pair_positions"] = 702

    def redirect_expected(value: dict[str, Any]) -> None:
        value["expected_output"]["path"] = "experimental/forged-output.txt"

    mutators: tuple[tuple[str, Callable[[dict[str, Any]], None]], ...] = (
        ("generator_degree", set_generator_degree),
        ("monomial_cap", set_cap),
        ("arbitrary_g_claim", claim_arbitrary_g),
        ("finite_payment", claim_payment),
        ("ledger_reintroduction", add_ledger),
        ("overlap_baseline", remove_overlap),
        ("pr843_reclamation", reclaim_pr843),
        ("pr844_reclamation", reclaim_pr844),
        ("identity_sign", alter_identity),
        ("split_filter", drop_split_filter),
        ("pair_count", alter_pair_count),
        ("expected_path", redirect_expected),
    )

    rejected = 0
    for name, mutate in mutators:
        candidate = copy.deepcopy(manifest)
        mutate(candidate)
        try:
            validate_manifest(candidate)
        except VerificationError:
            rejected += 1
        else:
            raise VerificationError("semantic tamper accepted: " + name)
    require(rejected == len(mutators), "all semantic tampers rejected")
    return rejected


def render_output(
    algebra: dict[str, int], cap: int, tamper_count: int, artifact_count: int
) -> bytes:
    lines = (
        "FIXED26_DIVIDED_DIFFERENCE_SOURCE_COMPILER: PASS",
        "manifest_schema=" + SCHEMA,
        "deployed=B32768,s1936,a67472,r63601,D61665,d28897,tail3870",
        "compiler=labels38,pairs703,identity_contract11,degree_criterion=PASS",
        (
            "algebra_replay=moduli{moduli},instances{instances},pair_checks{pair_checks},"
            "monomial_formula_checks{formula_checks},source_reconstruction=PASS"
        ).format(**algebra),
        "monomial_cap=37,class_size<=3,partition=3x12+2,zero_tail_branch=NO_H_SPLIT_EDGES",
        "filters=9,status=RETAINED_NOT_CONSEQUENCES",
        "overlap=826,838,843,844;pr843_rank2=CARVED_OUT;pr844=CARVED_OUT",
        "ledger=OMITTED;finite_payment=0;parent_closure=0;score_delta=0",
        "semantic_tamper_selftests=PASS,count=" + str(tamper_count),
        "artifact_checksums=PASS,count=" + str(artifact_count),
        "RESULT=PASS",
    )
    require(cap == 37, "rendered cap")
    return ("\n".join(lines) + "\n").encode("ascii")


def run_default() -> None:
    manifest = load_manifest()
    validate_manifest(manifest)
    verify_deployed_parameters(manifest)
    monomial_algebra = replay_source_algebra()
    nonmonomial_algebra = replay_nonmonomial_source_algebra()
    algebra = {
        "moduli": 2,
        "instances": monomial_algebra["instances"] + nonmonomial_algebra["instances"],
        "pair_checks": monomial_algebra["pair_checks"] + nonmonomial_algebra["pair_checks"],
        "formula_checks": monomial_algebra["formula_checks"],
    }
    cap = verify_monomial_cap(manifest)
    tamper_count = semantic_tamper_selftests(manifest)
    artifact_count = verify_artifacts(manifest)
    output = render_output(algebra, cap, tamper_count, artifact_count)
    expected = EXPECTED_PATH.read_bytes()
    require(output == expected, "frozen expected output byte match")
    sys.stdout.buffer.write(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--tamper-self-test",
        action="store_true",
        help="run the semantic mutation rejection suite",
    )
    group.add_argument(
        "--check-checksums",
        action="store_true",
        help="validate the pinned artifact checksum set",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = load_manifest()
        validate_manifest(manifest)
        if args.tamper_self_test:
            count = semantic_tamper_selftests(manifest)
            print("SEMANTIC_TAMPER_SELFTESTS: PASS count=" + str(count))
        elif args.check_checksums:
            count = verify_artifacts(manifest)
            print("ARTIFACT_CHECKSUMS: PASS count=" + str(count))
        else:
            run_default()
    except (OSError, VerificationError, ValueError) as exc:
        print("FIXED26_DIVIDED_DIFFERENCE_SOURCE_COMPILER: FAIL", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
