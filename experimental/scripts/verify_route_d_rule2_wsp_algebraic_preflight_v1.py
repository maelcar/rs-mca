#!/usr/bin/env python3
"""Deterministic F31 verifier for the Route-D Rule-2 WSP algebraic preflight.

The corpus and every polynomial, gcd, reduced signed weight, pivot, and count
are recomputed from definitions.  No stored certificate is trusted.

Usage:
  python3 experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py
  python3 experimental/scripts/verify_route_d_rule2_wsp_algebraic_preflight_v1.py --tamper
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence


SOURCE_COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
SHIPMENT_COMMIT = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
SOURCE_BLOBS = {
    "experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md":
        "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py":
        "dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1",
    "experimental/notes/thresholds/cap25_v13_route_d_barrier_map.md":
        "ea896eca8bf89038b76469e51b6dd70eb83d3c02",
    "experimental/data/cap25_v13_route_d_barrier_map.json":
        "4d3d068cf80cd5912c998d86411e8baf33ece156",
    "experimental/scripts/verify_route_d_barrier_map.py":
        "2243a8c987d0493cb5f48f52b6174f735312e54a",
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md":
        "ddfce00907f34128b324a64041f4e0ec8957b7d3",
    "experimental/scripts/verify_m1_kb_branch2_rank_deep_owner_v1.py":
        "1702842190da45806e5a52e932aa4b8dab951ffe",
    "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
    "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
}
SHIPMENT_BLOBS = {
    "experimental/notes/thresholds/route_d_marked_rim_all_minors_adapter_v1.md":
        "f24ce928df7e7170c1b4f3228d5fe9b184be50b4",
    "experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py":
        "ace3e859b917ae87eeffb8c0e7c37155520e311e",
    "experimental/lean/route_d_marked_rim_all_minors_adapter_v1/"
    "RouteDMarkedRimAllMinorsAdapterV1.lean":
        "78e46c6ab97d97191c567041f81a6ca05e76cf41",
}


class CertificateError(RuntimeError):
    """Fail-closed verification error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def trim(poly: Sequence[int], modulus: int) -> tuple[int, ...]:
    values = [value % modulus for value in poly]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return tuple(values)


def poly_add(left: Sequence[int], right: Sequence[int], modulus: int) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)
        for i in range(width)
    ], modulus)


def poly_sub(left: Sequence[int], right: Sequence[int], modulus: int) -> tuple[int, ...]:
    width = max(len(left), len(right))
    return trim([
        (left[i] if i < len(left) else 0) - (right[i] if i < len(right) else 0)
        for i in range(width)
    ], modulus)


def poly_mul(left: Sequence[int], right: Sequence[int], modulus: int) -> tuple[int, ...]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % modulus
    return trim(result, modulus)


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int], modulus: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator, modulus))
    den = trim(denominator, modulus)
    require(den != (0,), "polynomial division by zero")
    if len(num) < len(den):
        return (0,), tuple(num)
    quotient = [0] * (len(num) - len(den) + 1)
    inv_lead = pow(den[-1], -1, modulus)
    while len(num) >= len(den) and any(num):
        shift = len(num) - len(den)
        coeff = num[-1] * inv_lead % modulus
        quotient[shift] = coeff
        for i, value in enumerate(den):
            num[i + shift] = (num[i + shift] - coeff * value) % modulus
        while len(num) > 1 and num[-1] == 0:
            num.pop()
    return trim(quotient, modulus), trim(num, modulus)


def poly_exact_div(
    numerator: Sequence[int], denominator: Sequence[int], modulus: int
) -> tuple[int, ...]:
    quotient, remainder = poly_divmod(numerator, denominator, modulus)
    require(remainder == (0,), "non-exact polynomial division")
    return quotient


def poly_monic(poly: Sequence[int], modulus: int) -> tuple[int, ...]:
    value = trim(poly, modulus)
    require(value != (0,), "zero polynomial has no monic normalization")
    inverse = pow(value[-1], -1, modulus)
    return tuple(entry * inverse % modulus for entry in value)


def poly_gcd(left: Sequence[int], right: Sequence[int], modulus: int) -> tuple[int, ...]:
    a = trim(left, modulus)
    b = trim(right, modulus)
    while b != (0,):
        _, remainder = poly_divmod(a, b, modulus)
        a, b = b, remainder
    return poly_monic(a, modulus)


def locator(support: Sequence[int], modulus: int) -> tuple[int, ...]:
    result = (1,)
    for root in support:
        result = poly_mul(result, ((-root) % modulus, 1), modulus)
    return result


def locator_prefix2(support: Sequence[int], modulus: int) -> tuple[int, int]:
    loc = locator(support, modulus)
    return loc[-2], loc[-3]


def power_sum(support: Iterable[int], degree: int, modulus: int) -> int:
    return sum(pow(value, degree, modulus) for value in support) % modulus


def signed_moment(weight: Mapping[int, int], degree: int, modulus: int) -> int:
    return sum(coeff * pow(root, degree, modulus) for root, coeff in weight.items()) % modulus


def det_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "determinant input is not square")
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result % modulus
        value = work[col][col]
        result = result * value % modulus
        inverse = pow(value, -1, modulus)
        for row in range(col + 1, n):
            factor = work[row][col] * inverse % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[col])
                ]
    return result


def rank_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    if not matrix:
        return 0
    work = [[entry % modulus for entry in row] for row in matrix]
    width = len(work[0])
    require(all(len(row) == width for row in work), "ragged rank matrix")
    rank = 0
    for col in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][col], -1, modulus)
        work[rank] = [value * inverse % modulus for value in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def projective_signed_stabilizer(
    weight: Mapping[int, int], modulus: int
) -> tuple[tuple[int, int], ...]:
    normalized = {root: coeff for root, coeff in weight.items() if coeff}
    answers: list[tuple[int, int]] = []
    for scalar in range(1, modulus):
        scaled = {(scalar * root) % modulus: coeff for root, coeff in normalized.items()}
        for sign in (1, -1):
            signed = {root: sign * coeff for root, coeff in normalized.items()}
            if scaled == signed:
                answers.append((scalar, sign))
    return tuple(answers)


def side_weight(
    positive: Sequence[int], negative: Sequence[int]
) -> dict[int, int]:
    result: Counter[int] = Counter(positive)
    result.subtract(negative)
    return {root: coeff for root, coeff in result.items() if coeff}


def make_mates() -> tuple[dict[str, object], ...]:
    modulus = 31
    domain = tuple(range(1, modulus))
    error = {1, 2, 3}
    base = (1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28)
    base_set = set(base)
    target = locator_prefix2(base, modulus)
    require(target == (30, 9), "parent target changed")
    removable = tuple(value for value in base if value not in error)
    outside = tuple(value for value in domain if value not in base_set)
    records: list[dict[str, object]] = []
    for removed in itertools.combinations(removable, 3):
        removed_set = set(removed)
        core = tuple(value for value in base if value not in removed_set)
        for added in itertools.combinations(outside, 3):
            support = canonical((*core, *added))
            if locator_prefix2(support, modulus) != target:
                continue
            nu = side_weight(added, removed)
            nu3 = signed_moment(nu, 3, modulus)
            loc_removed = locator(removed, modulus)
            loc_added = locator(added, modulus)
            c = (loc_added[0] - loc_removed[0]) % modulus
            require(c != 0, "top-seam cell label vanished")
            require(c == -nu3 * pow(3, -1, modulus) % modulus, "c != -nu3/3")
            require(
                poly_sub(loc_added, (c,), modulus) == loc_removed,
                "orientation U-c=L_R failed",
            )
            records.append({
                "removed": canonical(removed),
                "added": canonical(added),
                "core": core,
                "support": support,
                "c": c,
                "nu3": nu3,
                "nu": nu,
            })
    require(len(records) == 121, "mate count changed")
    return tuple(records)


def primitive_mates(records: Sequence[dict[str, object]]) -> tuple[dict[str, object], ...]:
    primitive = []
    for record in records:
        nu = record["nu"]
        require(isinstance(nu, dict), "bad side-weight record")
        if projective_signed_stabilizer(nu, 31) == ((1, 1),):
            primitive.append(record)
    require(len(primitive) == 119, "primitive mate count changed")
    return tuple(primitive)


def rule2_certificate(
    representative: dict[str, object], packet: dict[str, object]
) -> dict[str, object]:
    modulus = 31
    r = 3
    c = packet["c"]
    require(c == representative["c"], "cross-cell Rule2 comparison")
    r0 = representative["removed"]
    a0 = representative["added"]
    removed = packet["removed"]
    added = packet["added"]
    require(all(isinstance(value, tuple) for value in (r0, a0, removed, added)), "bad packet sides")
    u0 = locator(a0, modulus)
    v0 = locator(r0, modulus)
    u = locator(added, modulus)
    v = locator(removed, modulus)
    require(poly_sub(u0, (int(c),), modulus) == v0, "U0-c != L_R0")
    require(poly_sub(u, (int(c),), modulus) == v, "U-c != L_R")
    l_plus = poly_mul(u0, v, modulus)
    l_minus = poly_mul(v0, u, modulus)
    h = poly_gcd(l_plus, l_minus, modulus)
    m_plus = poly_exact_div(l_plus, h, modulus)
    m_minus = poly_exact_div(l_minus, h, modulus)
    require(m_plus != m_minus, "Rule2 reduced pair became identical")
    require(poly_gcd(m_plus, m_minus, modulus) == (1,), "reduced sides not coprime")
    require(len(m_plus) == len(m_minus), "reduced sides have unequal degree")
    require(len(poly_sub(m_plus, m_minus, modulus)) - 1 <= len(m_plus) - 2 - r,
            "Rule2 degree bound failed")

    mu_counter: Counter[int] = Counter(a0)
    mu_counter.update(removed)
    mu_counter.subtract(r0)
    mu_counter.subtract(added)
    mu = {root: coeff for root, coeff in mu_counter.items() if coeff}
    positive_roots = tuple(sorted(root for root, coeff in mu.items() for _ in range(coeff)))
    negative_roots = tuple(sorted(root for root, coeff in mu.items() for _ in range(-coeff)))
    require(locator(positive_roots, modulus) == m_plus, "M_plus weight factorization failed")
    require(locator(negative_roots, modulus) == m_minus, "M_minus weight factorization failed")

    recovered_u = poly_exact_div(poly_mul(h, m_minus, modulus), v0, modulus)
    require(recovered_u == u, "Rule2 packet recovery failed")
    require(packet["core"] == tuple(value for value in packet["core"]), "core mark drift")
    require(canonical((*packet["core"], *removed)) ==
            (1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28),
            "marked base reconstruction failed")
    require(canonical((*packet["core"], *added)) == packet["support"],
            "marked mate reconstruction failed")
    moments = tuple(signed_moment(mu, degree, modulus) for degree in range(5))
    require(moments[:4] == (0, 0, 0, 0), "Rule2 moments mu0..mu3 do not vanish")

    support = tuple(sorted(mu))
    vandermonde = tuple(
        tuple(pow(root, degree, modulus) for root in support)
        for degree in range(r + 1)
    )
    pivot_columns = tuple(range(r + 1))
    pivot_matrix = tuple(tuple(row[column] for column in pivot_columns) for row in vandermonde)
    pivot = det_mod(pivot_matrix, modulus)
    require(pivot != 0, "lex Vandermonde pivot vanished")
    require(rank_mod(vandermonde, modulus) == r + 1, "WSP Vandermonde lost full row rank")
    require(len(support) > r + 1, "support collapse occurred")
    require(len(support) != r + 2, "BC corank-one support occurred")
    require(projective_signed_stabilizer(mu, modulus) == ((1, 1),),
            "reduced WSP weight is not projectively primitive")
    return {
        "cell": (r, c),
        "representative": (r0, a0),
        "packet": (removed, added),
        "core": packet["core"],
        "H": h,
        "M_plus": m_plus,
        "M_minus": m_minus,
        "mu": tuple(sorted(mu.items())),
        "support_size": len(support),
        "moments_0_through_4": moments,
        "extension": moments[4] == 0,
        "pivot": pivot,
        "rank": r + 1,
    }


def summarize() -> dict[str, object]:
    records = make_mates()
    primitive = primitive_mates(records)
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for record in primitive:
        groups[int(record["c"])].append(record)
    for group in groups.values():
        group.sort(key=lambda row: (row["removed"], row["added"]))
    require(len(groups) == 28, "occupied Rule2 cell count changed")
    cell_size_hist = Counter(len(group) for group in groups.values())
    require(cell_size_hist == Counter({1: 1, 2: 4, 3: 5, 4: 8, 5: 3, 6: 4, 7: 1, 8: 1, 9: 1}),
            "cell-size histogram changed")

    rule1_keys = [
        (3, record["c"], locator(record["added"], 31), (30, 9))
        for record in primitive
    ]
    rule1_duplicates = len(rule1_keys) - len(set(rule1_keys))
    require(rule1_duplicates == 0, "Rule1 key duplicate appeared")

    lex_certificates = []
    representatives = []
    for c in sorted(groups):
        group = groups[c]
        representative = group[0]
        representatives.append(representative)
        lex_certificates.extend(rule2_certificate(representative, packet) for packet in group[1:])
    require(len(representatives) == 28 and len(lex_certificates) == 91,
            "lex Rule2 partition changed")
    support_hist = Counter(int(cert["support_size"]) for cert in lex_certificates)
    require(support_hist == Counter({8: 40, 10: 30, 12: 21}), "lex support histogram changed")
    extensions = [cert for cert in lex_certificates if cert["extension"]]
    nonextensions = [cert for cert in lex_certificates if not cert["extension"]]
    require(len(extensions) == 3 and len(nonextensions) == 88, "lex extension split changed")
    extension_fixtures = tuple(
        (cert["cell"][1], cert["representative"], cert["packet"])
        for cert in extensions
    )
    expected_extensions = (
        (5, ((5, 11, 19), (15, 24, 27)), ((12, 26, 28), (6, 14, 15))),
        (26, ((4, 7, 26), (16, 22, 30)), ((5, 12, 20), (15, 23, 30))),
        (28, ((5, 7, 11), (13, 14, 27)), ((7, 19, 28), (8, 17, 29))),
    )
    require(extension_fixtures == expected_extensions, "lex extension fixtures changed")
    source_groups = {
        c: sorted(group, key=lambda row: (row["support"], row["removed"], row["added"]))
        for c, group in groups.items()
    }
    source_certificates = []
    source_representatives = []
    for c in sorted(source_groups):
        group = source_groups[c]
        representative = group[0]
        source_representatives.append(representative)
        source_certificates.extend(rule2_certificate(representative, packet) for packet in group[1:])
    require(len(source_representatives) == 28 and len(source_certificates) == 91,
            "source-oriented Rule2 partition changed")
    source_extensions = [cert for cert in source_certificates if cert["extension"]]
    source_nonextensions = [cert for cert in source_certificates if not cert["extension"]]
    require(len(source_extensions) == 6 and len(source_nonextensions) == 85,
            "source-oriented extension split changed")
    source_support_hist = Counter(int(cert["support_size"]) for cert in source_certificates)
    source_extension_support_hist = Counter(int(cert["support_size"]) for cert in source_extensions)
    source_nonextension_support_hist = Counter(int(cert["support_size"]) for cert in source_nonextensions)
    require(source_support_hist == Counter({8: 32, 10: 40, 12: 19}),
            "source-oriented support histogram changed")
    require(source_extension_support_hist == Counter({10: 5, 12: 1}),
            "source-oriented extension support histogram changed")
    require(source_nonextension_support_hist == Counter({8: 32, 10: 35, 12: 18}),
            "source-oriented candidate support histogram changed")


    ordered_certificates = []
    per_cell_extension_range: dict[int, tuple[int, int]] = {}
    for c in sorted(groups):
        group = groups[c]
        extension_counts = []
        for representative in group:
            certs = [
                rule2_certificate(representative, packet)
                for packet in group
                if packet is not representative
            ]
            ordered_certificates.extend(certs)
            extension_counts.append(sum(bool(cert["extension"]) for cert in certs))
        per_cell_extension_range[c] = (min(extension_counts), max(extension_counts))
    require(len(ordered_certificates) == 484, "ordered same-cell pair count changed")
    ordered_support_hist = Counter(int(cert["support_size"]) for cert in ordered_certificates)
    require(ordered_support_hist == Counter({8: 198, 10: 188, 12: 98}), "ordered support histogram changed")
    ordered_extension = sum(bool(cert["extension"]) for cert in ordered_certificates)
    require(ordered_extension == 32, "ordered extension count changed")
    require(len(ordered_certificates) - ordered_extension == 452,
            "ordered nonextension count changed")
    maximum_extensions_for_any_canonical_choice = sum(high for _, high in per_cell_extension_range.values())
    minimum_extensions_for_any_canonical_choice = sum(low for low, _ in per_cell_extension_range.values())
    require(maximum_extensions_for_any_canonical_choice == 10,
            "canonical-choice extension maximum changed")
    require(minimum_extensions_for_any_canonical_choice == 1,
            "canonical-choice extension minimum changed")

    return {
        "status": "COUNTEREXAMPLE",
        "source_commit": SOURCE_COMMIT,
        "shipment_commit": SHIPMENT_COMMIT,
        "source_blobs": SOURCE_BLOBS,
        "shipment_blobs": SHIPMENT_BLOBS,
        "fixture": {
            "p": 31,
            "r": 3,
            "target": (30, 9),
            "mates": len(records),
            "projectively_primitive_mates": len(primitive),
        },
        "rule1": {"key_duplicates": rule1_duplicates},
        "cells": {
            "occupied": len(groups),
            "size_histogram": dict(sorted(cell_size_hist.items())),
            "representatives": len(representatives),
            "one_row_nonzero_capacity": 30,
            "algebraic_cell_labels_fit": len(representatives) <= 30,
        },
        "boundary_pair_lex_t_rule2": {
            "emitted": len(source_certificates),
            "support_size_histogram": dict(sorted(source_support_hist.items())),
            "extension_candidates": len(source_extensions),
            "extension_support_size_histogram": dict(sorted(source_extension_support_hist.items())),
            "nonextension_algebraic_candidates": len(source_nonextensions),
            "candidate_support_size_histogram": dict(sorted(source_nonextension_support_hist.items())),
            "algebraic_emissions": len(source_certificates),
        },
        "auxiliary_lex_ra_rule2": {
            "emitted": len(lex_certificates),
            "support_size_histogram": dict(sorted(support_hist.items())),
            "extension_candidates": len(extensions),
            "nonextension_algebraic_candidates": len(nonextensions),
            "algebraic_emissions": len(lex_certificates),
            "extension_fixtures": extension_fixtures,
        },
        "all_ordered_same_cell_pairs": {
            "count": len(ordered_certificates),
            "support_size_histogram": dict(sorted(ordered_support_hist.items())),
            "extension": ordered_extension,
            "nonextension_projectively_primitive": len(ordered_certificates) - ordered_extension,
            "max_extensions_for_any_canonical_choice": maximum_extensions_for_any_canonical_choice,
            "min_extensions_for_any_canonical_choice": minimum_extensions_for_any_canonical_choice,
            "min_nonextension_for_any_canonical_choice": 91 - maximum_extensions_for_any_canonical_choice,
            "max_nonextension_for_any_canonical_choice": 91 - minimum_extensions_for_any_canonical_choice,
            "per_cell_extension_range": per_cell_extension_range,
        },
        "ownership": {
            "numerical_payment_inferred": False,
            "official_N_WSP_full_claimed": False,
            "genuine_first_match_units_claimed": False,
            "common_core_preserved": True,
        },
    }


def validate(certificate: dict[str, object]) -> None:
    require(certificate["status"] == "COUNTEREXAMPLE", "status drift")
    require(certificate["source_commit"] == SOURCE_COMMIT, "source commit drift")
    require(certificate["shipment_commit"] == SHIPMENT_COMMIT, "shipment commit drift")
    require(certificate["source_blobs"] == SOURCE_BLOBS, "source blob drift")
    require(certificate["shipment_blobs"] == SHIPMENT_BLOBS, "shipment blob drift")
    fixture = certificate["fixture"]
    cells = certificate["cells"]
    primary = certificate["boundary_pair_lex_t_rule2"]
    lex = certificate["auxiliary_lex_ra_rule2"]
    ordered = certificate["all_ordered_same_cell_pairs"]
    ownership = certificate["ownership"]
    require(isinstance(fixture, dict) and fixture["mates"] == 121, "mate certificate drift")
    require(fixture["projectively_primitive_mates"] == 119, "primitive certificate drift")
    require(isinstance(cells, dict) and cells["occupied"] == 28 and cells["algebraic_cell_labels_fit"] is True,
            "cell certificate drift")
    require(isinstance(primary, dict) and primary["emitted"] == 91, "primary Rule2 emitted drift")
    require(primary["extension_candidates"] == 6, "primary extension split drift")
    require(primary["nonextension_algebraic_candidates"] == 85, "primary candidate count drift")
    require(primary["algebraic_emissions"] == 91, "primary emission total drift")
    require(isinstance(lex, dict) and lex["emitted"] == 91, "Rule2 emitted drift")
    require(lex["extension_candidates"] == 3, "extension split drift")
    require(lex["nonextension_algebraic_candidates"] == 88, "auxiliary candidate count drift")
    require(lex["algebraic_emissions"] == 91, "emission total drift")
    require(isinstance(ordered, dict) and ordered["count"] == 484, "ordered count drift")
    require(ordered["support_size_histogram"] == {8: 198, 10: 188, 12: 98},
            "ordered support histogram drift")
    require(ordered["extension"] == 32, "ordered extension drift")
    require(ordered["nonextension_projectively_primitive"] == 452,
            "ordered primitive residual drift")
    require(ordered["max_extensions_for_any_canonical_choice"] == 10,
            "robust extension maximum drift")
    require(ordered["min_extensions_for_any_canonical_choice"] == 1,
            "robust extension minimum drift")
    require(ordered["min_nonextension_for_any_canonical_choice"] == 81,
            "robust lower-bound drift")
    require(ordered["max_nonextension_for_any_canonical_choice"] == 90,
            "robust ceiling drift")
    require(isinstance(ownership, dict), "ownership block missing")
    require(all(ownership[key] is False for key in (
        "numerical_payment_inferred",
        "official_N_WSP_full_claimed",
        "genuine_first_match_units_claimed",
    )), "false ownership claim")
    require(ownership["common_core_preserved"] is True, "common-core mark lost")


def tamper_selftest(certificate: dict[str, object]) -> None:
    mutations = []
    for path, value in (
        (("boundary_pair_lex_t_rule2", "nonextension_algebraic_candidates"), 84),
        (("auxiliary_lex_ra_rule2", "emitted"), 90),
        (("auxiliary_lex_ra_rule2", "extension_candidates"), 4),
        (("auxiliary_lex_ra_rule2", "nonextension_algebraic_candidates"), 87),
        (("ownership", "numerical_payment_inferred"), True),
        (("ownership", "common_core_preserved"), False),
        (("all_ordered_same_cell_pairs", "support_size_histogram", 8), 197),
        (("all_ordered_same_cell_pairs", "min_nonextension_for_any_canonical_choice"), 80),
        (("source_commit",), "0" * 40),
    ):
        candidate = copy.deepcopy(certificate)
        cursor: object = candidate
        for key in path[:-1]:
            require(isinstance(cursor, dict), "bad tamper path")
            cursor = cursor[key]
        require(isinstance(cursor, dict), "bad tamper leaf")
        cursor[path[-1]] = value
        mutations.append((path, candidate))
    for path, candidate in mutations:
        try:
            validate(candidate)
        except CertificateError:
            continue
        raise CertificateError(f"tamper was not rejected: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tamper", action="store_true", help="run fail-closed mutation tests")
    args = parser.parse_args()
    certificate = summarize()
    validate(certificate)
    if args.tamper:
        tamper_selftest(certificate)
        print("TAMPER: PASS")
    else:
        print(json.dumps(certificate, sort_keys=True, separators=(",", ":")))
        print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CertificateError as error:
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
