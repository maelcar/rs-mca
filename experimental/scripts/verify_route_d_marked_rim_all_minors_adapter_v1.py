#!/usr/bin/env python3
"""Deterministic verifier for the Route-D marked all-minors adapter packet.

The script uses only the Python standard library.  Its primary F31 corpus is
enumerated from definitions; no stored certificate is trusted.

Usage:
  python3 experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py
  python3 experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py --tamper
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import sys
from typing import Callable, Iterable, Sequence


SOURCE_COMMIT = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
SOURCE_BLOBS = {
    "experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md":
        "591c91a6aac6b48db0c16abc586b74d7a51e44e2",
    "experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md":
        "dda538a9a36cd0c8e267c11600a49cdc5bf054d1",
    "experimental/notes/thresholds/cap25_v13_lq_top_seam_marked_incidence.md":
        "a7f2bf4f1338d0b31d999c86a29859317033113f",
    "experimental/notes/m1/m1_kb_branch2_hankel_pivot_adapter_v1.md":
        "0e1becd7ac2f66bf74c034ef0b8165d56cc1c471",
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md":
        "ddfce00907f34128b324a64041f4e0ec8957b7d3",
    "experimental/notes/thresholds/signed_local_minority_fixed_composition.md":
        "376c21252b5ee167839c2d214f173428c0010ff4",
    "experimental/notes/roadmaps/marked_exclusion_cross_gram.md":
        "4ed789595305170556371c87c5773d9e14ba4307",
    "agents.md": "2fea2bce6a348105f0016fcf739b5247bf408d93",
    "experimental/agents-log.md": "45b04597efb40741b807e48b290a0544f2fe6baf",
}


class CertificateError(RuntimeError):
    """Fail-closed certificate error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CertificateError(message)


def canonical(values: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(values))


def det_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "determinant matrix is not square")
    work = [[entry % modulus for entry in row] for row in matrix]
    result = 1
    for col in range(n):
        pivot = next((row for row in range(col, n) if work[row][col]), None)
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = (-result) % modulus
        value = work[col][col]
        result = (result * value) % modulus
        inverse = pow(value, -1, modulus)
        work[col] = [(entry * inverse) % modulus for entry in work[col]]
        for row in range(col + 1, n):
            factor = work[row][col]
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[col])
                ]
    return result


def rank_mod(matrix: Sequence[Sequence[int]], modulus: int) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    require(all(len(row) == width for row in matrix), "ragged matrix")
    work = [[entry % modulus for entry in row] for row in matrix]
    rank = 0
    for col in range(width):
        pivot = next((row for row in range(rank, len(work)) if work[row][col]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][col], -1, modulus)
        work[rank] = [(entry * inverse) % modulus for entry in work[rank]]
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


def maximal_minors(matrix: Sequence[Sequence[int]], modulus: int) -> tuple[int, ...]:
    rows = len(matrix)
    require(rows > 0, "maximal-minor fixture needs a positive row count")
    cols = len(matrix[0])
    require(rows <= cols, "maximal-minor fixture has more rows than columns")
    return tuple(
        det_mod([[matrix[row][col] for col in choice] for row in range(rows)], modulus)
        for choice in itertools.combinations(range(cols), rows)
    )


def check_all_minors() -> dict[str, object]:
    modulus = 3
    checked = 0
    rank_drop = 0
    for entries in itertools.product(range(modulus), repeat=6):
        matrix = (entries[:3], entries[3:])
        rank_lt = rank_mod(matrix, modulus) < 2
        all_vanish = all(value == 0 for value in maximal_minors(matrix, modulus))
        require(rank_lt == all_vanish, "all-maximal-minors equivalence failed over F3")
        checked += 1
        rank_drop += int(rank_lt)
    require(checked == 729 and rank_drop == 105, "F3 exhaustive control count changed")

    selected = ((1, 0, 0), (0, 0, 1))
    minors = maximal_minors(selected, 5)
    require(minors == (0, 1, 0), "selected-minor counterexample changed")
    require(rank_mod(selected, 5) == 2, "selected-minor matrix lost full row rank")
    return {
        "field": 3,
        "matrices_checked": checked,
        "rank_drop_matrices": rank_drop,
        "single_minor_counterexample": {
            "matrix": selected,
            "maximal_minors": minors,
            "rank": 2,
            "selected_zero_minor": (0, 1),
            "surviving_nonzero_minor": (0, 2),
        },
    }


def locator_prefix2(support: Sequence[int], modulus: int) -> tuple[int, int]:
    first = (-sum(support)) % modulus
    second = sum(
        support[i] * support[j]
        for i in range(len(support))
        for j in range(i + 1, len(support))
    ) % modulus
    return first, second


def deconvolve_prefix2(target: tuple[int, int], root: int, modulus: int) -> tuple[int, int]:
    first = (target[0] + root) % modulus
    second = (target[1] + root * first) % modulus
    return first, second


def target_stabilizer(target: tuple[int, int], modulus: int) -> tuple[int, ...]:
    return tuple(
        scalar
        for scalar in range(1, modulus)
        if (scalar * target[0]) % modulus == target[0]
        and (scalar * scalar * target[1]) % modulus == target[1]
    )


def scale_support(support: Sequence[int], scalar: int, modulus: int) -> tuple[int, ...]:
    return canonical((scalar * value) % modulus for value in support)


def power_sum(support: Sequence[int], degree: int, modulus: int) -> int:
    return sum(pow(value, degree, modulus) for value in support) % modulus


def locator_ascending(support: Sequence[int], modulus: int) -> tuple[int, ...]:
    coeffs = [1]
    for root in support:
        next_coeffs = [0] * (len(coeffs) + 1)
        for degree, coefficient in enumerate(coeffs):
            next_coeffs[degree] = (next_coeffs[degree] - root * coefficient) % modulus
            next_coeffs[degree + 1] = (next_coeffs[degree + 1] + coefficient) % modulus
        coeffs = next_coeffs
    return tuple(coeffs)


def check_f17_guard() -> dict[str, object]:
    modulus = 17
    generator = 3
    exponents1 = (0, 1, 2, 3, 4, 5, 6, 15)
    exponents2 = (0, 1, 2, 3, 5, 7, 12, 14)
    support1 = tuple(pow(generator, exponent, modulus) for exponent in exponents1)
    support2 = tuple(pow(generator, exponent, modulus) for exponent in exponents2)
    target1 = locator_prefix2(support1, modulus)
    target2 = locator_prefix2(support2, modulus)
    require(target1 == target2 == (6, 1), "F17 locator target changed")
    require(target_stabilizer(target1, modulus) == (1,), "F17 target lost primitivity")

    def antipodal_core(exponents: Sequence[int]) -> tuple[int, ...]:
        values = set(exponents)
        return tuple(exponent for exponent in range(8) if exponent in values and exponent + 8 in values)

    def folded_word(exponents: Sequence[int]) -> tuple[str, ...]:
        values = set(exponents)
        word = []
        for exponent in range(8):
            plus = exponent in values
            minus = exponent + 8 in values
            require(plus != minus, "F17 support is not an antipodal cross-section")
            word.append("+" if plus else "-")
        return tuple(word)

    word1 = folded_word(exponents1)
    word2 = folded_word(exponents2)
    least1 = next((index, sign) for index, sign in enumerate(word1))
    least2 = next((index, sign) for index, sign in enumerate(word2))
    require(antipodal_core(exponents1) == antipodal_core(exponents2) == (),
            "F17 marked antipodal core is not empty")
    require(least1 == least2 == (0, "+"), "F17 least signed contact changed")
    require(exponents1 != exponents2 and len(exponents1) == len(exponents2) == 8,
            "F17 defect-magnitude collision changed")
    return {
        "modulus": modulus,
        "generator": generator,
        "exponent_supports": (exponents1, exponents2),
        "field_supports": (support1, support2),
        "locator_target": target1,
        "target_stabilizer": target_stabilizer(target1, modulus),
        "antipodal_cores": ((), ()),
        "folded_words": (word1, word2),
        "least_signed_contacts": (least1, least2),
        "defect_magnitudes": (8, 8),
    }


def projective_signed_stabilizer(
    positive: Sequence[int], negative: Sequence[int], modulus: int
) -> tuple[tuple[int, int], ...]:
    positive_tuple = canonical(positive)
    negative_tuple = canonical(negative)
    stabilizer: list[tuple[int, int]] = []
    for scalar in range(1, modulus):
        scaled_positive = scale_support(positive, scalar, modulus)
        scaled_negative = scale_support(negative, scalar, modulus)
        if scaled_positive == positive_tuple and scaled_negative == negative_tuple:
            stabilizer.append((scalar, 1))
        if scaled_positive == negative_tuple and scaled_negative == positive_tuple:
            stabilizer.append((scalar, -1))
    return tuple(stabilizer)


def syndrome(
    word: Callable[[int], int], modulus: int, domain: Sequence[int], length: int
) -> tuple[int, ...]:
    # For D=F_p^*, the full-domain dual weight is lambda_x=-x.
    return tuple(
        sum(((-x) % modulus) * pow(x, degree, modulus) * word(x) for x in domain)
        % modulus
        for degree in range(length)
    )


def hankel(values: Sequence[int], rows: int, width: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(values[row + col] for col in range(width)) for row in range(rows))


def mat_vec(matrix: Sequence[Sequence[int]], vector: Sequence[int], modulus: int) -> tuple[int, ...]:
    return tuple(sum(left * right for left, right in zip(row, vector)) % modulus for row in matrix)


def check_f31_corpus() -> dict[str, object]:
    modulus = 31
    domain = tuple(range(1, modulus))
    k = 12
    agreement = 15
    j = 15
    t = 3
    w = 2
    error = (1, 2, 3)
    error_set = set(error)
    base = (1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28)
    base_set = set(base)
    target = locator_prefix2(base, modulus)
    require(target == (30, 9), "F31 parent target changed")
    require(target_stabilizer(target, modulus) == (1,), "F31 parent target is not primitive")
    child_target = deconvolve_prefix2(target, 1, modulus)
    require(child_target == (0, 9), "F31 child target changed")
    child_stabilizer = target_stabilizer(child_target, modulus)
    require(child_stabilizer == (1, 30), "F31 child stabilizer changed")
    for scalar in range(1, modulus):
        scaled_target = (
            scalar * target[0] % modulus,
            scalar * scalar * target[1] % modulus,
        )
        require((scaled_target == target) == (scalar == 1),
                "F31 fixed-parent-target cross-section failed")

    removable = tuple(value for value in base if value not in error_set)
    outside = tuple(value for value in domain if value not in base_set)
    mates: list[dict[str, tuple[int, ...]]] = []
    for removed in itertools.combinations(removable, 3):
        removed_set = set(removed)
        core = tuple(value for value in base if value not in removed_set)
        for added in itertools.combinations(outside, 3):
            support = canonical((*core, *added))
            if locator_prefix2(support, modulus) != target:
                continue
            mates.append({
                "removed": canonical(removed),
                "added": canonical(added),
                "core": core,
                "support": support,
            })
    require(len(mates) == 121, "F31 mate count changed")

    primitive: list[dict[str, tuple[int, ...]]] = []
    for mate in mates:
        removed = mate["removed"]
        added = mate["added"]
        support = mate["support"]
        core = mate["core"]
        require(error_set.issubset(support), "F31 actual error support was deleted")
        require(set(core).isdisjoint(added) and set(core).isdisjoint(removed),
                "F31 common-core marking failed")
        require(canonical((*core, *removed)) == base, "F31 marked parent reconstruction failed")
        require(canonical((*core, *added)) == support, "F31 marked mate reconstruction failed")
        require(power_sum(added, 1, modulus) == power_sum(removed, 1, modulus),
                "F31 first signed moment changed")
        require(power_sum(added, 2, modulus) == power_sum(removed, 2, modulus),
                "F31 second signed moment changed")
        signed_third = (power_sum(added, 3, modulus) - power_sum(removed, 3, modulus)) % modulus
        require(signed_third != 0, "F31 simple side third moment vanished")
        plus_locator = locator_ascending(added, modulus)
        minus_locator = locator_ascending(removed, modulus)
        require(plus_locator[1:] == minus_locator[1:], "F31 cubic side prefixes changed")
        require(plus_locator[0] != minus_locator[0], "F31 side-locator constant vanished")
        if projective_signed_stabilizer(added, removed, modulus) == ((1, 1),):
            primitive.append(mate)
    require(len(primitive) == 119, "F31 projectively primitive count changed")
    primitive_cores = {mate["core"] for mate in primitive}
    require(len(primitive_cores) == 99, "F31 primitive common-core count changed")

    redundancy = len(domain) - k
    syn_f = syndrome(lambda x: int(x in error_set), modulus, domain, redundancy)
    syn_g = syndrome(lambda x: pow(x, k, modulus), modulus, domain, redundancy)
    require(syn_g == (0,) * 17 + (1,), "F31 monomial syndrome changed")
    matrix = hankel(syn_f, t, j + 1)
    require(rank_mod(matrix, modulus) == t, "F31 actual-incidence Hankel rank changed")
    minors = maximal_minors(matrix, modulus)
    nonzero_minors = sum(value != 0 for value in minors)
    require(len(minors) == 560 and nonzero_minors == 541,
            "F31 maximal-minor census changed")

    quotient_pivots = set()
    for mate in mates:
        locator = locator_ascending(mate["support"], modulus)
        coordinates = mat_vec(hankel(syn_g, t, j + 1), locator, modulus)
        require(coordinates == (0, 0, 1), "F31 field-native quotient coordinate changed")
        pivot = next((index, value) for index, value in enumerate(coordinates) if value)
        quotient_pivots.add(pivot)

        agreement_support = tuple(value for value in domain if value not in set(mate["support"]))
        require(len(agreement_support) == agreement, "F31 agreement support size changed")
        vandermonde = [
            [pow(x, degree, modulus) for degree in range(k)]
            for x in agreement_support
        ]
        augmented = [
            [*row, pow(x, k, modulus)]
            for row, x in zip(vandermonde, agreement_support)
        ]
        require(rank_mod(vandermonde, modulus) == k, "F31 RS evaluation rank changed")
        require(rank_mod(augmented, modulus) == k + 1,
                "F31 noncontainment control failed")
    require(quotient_pivots == {(2, 1)}, "F31 common pivot label changed")

    capacity_all = t * modulus
    capacity_nonzero = t * (modulus - 1)
    require(len(primitive_cores) == 99 > capacity_all == 93,
            "F31 all-label capacity obstruction changed")
    require(len(primitive_cores) == 99 > capacity_nonzero == 90,
            "F31 nonzero-label capacity obstruction changed")
    return {
        "modulus": modulus,
        "parameters": {"k": k, "agreement": agreement, "j": j, "t": t, "w": w},
        "base": base,
        "error_support": error,
        "parent_target": target,
        "parent_target_stabilizer": target_stabilizer(target, modulus),
        "marked_root": 1,
        "child_target": child_target,
        "child_target_stabilizer": child_stabilizer,
        "mates": len(mates),
        "projectively_primitive_mates": len(primitive),
        "primitive_distinct_common_cores": len(primitive_cores),
        "all_label_capacity": capacity_all,
        "nonzero_label_capacity": capacity_nonzero,
        "all_label_excess": len(primitive_cores) - capacity_all,
        "nonzero_label_excess": len(primitive_cores) - capacity_nonzero,
        "actual_error_size": len(error),
        "hankel_rank": rank_mod(matrix, modulus),
        "maximal_minors": len(minors),
        "nonzero_maximal_minors": nonzero_minors,
        "common_field_native_pivot": next(iter(quotient_pivots)),
        "simple_side_third_moment_nonzero_for_all_mates": True,
        "named_deletions_executed": False,
    }


def build_certificate() -> dict[str, object]:
    return {
        "schema": "route-d-marked-rim-all-minors-adapter-v1",
        "source_commit": SOURCE_COMMIT,
        "source_blobs": SOURCE_BLOBS,
        "status": "COUNTEREXAMPLE",
        "all_minors": check_all_minors(),
        "f17_reconstruction_guard": check_f17_guard(),
        "f31_marked_obstruction": check_f31_corpus(),
    }


def validate_certificate(certificate: dict[str, object]) -> None:
    require(set(certificate) == {
        "schema", "source_commit", "source_blobs", "status", "all_minors",
        "f17_reconstruction_guard", "f31_marked_obstruction",
    }, "top-level certificate fields changed")
    require(certificate["schema"] == "route-d-marked-rim-all-minors-adapter-v1",
            "schema changed")
    require(certificate["source_commit"] == SOURCE_COMMIT, "source commit changed")
    require(certificate["source_blobs"] == SOURCE_BLOBS, "source blob map changed")
    require(certificate["status"] == "COUNTEREXAMPLE", "status changed")

    all_minors = certificate["all_minors"]
    require(isinstance(all_minors, dict), "all-minors payload missing")
    require(all_minors["matrices_checked"] == 729, "all-minors exhaustive count changed")
    require(all_minors["rank_drop_matrices"] == 105, "rank-drop matrix count changed")
    counterexample = all_minors["single_minor_counterexample"]
    require(counterexample["maximal_minors"] == (0, 1, 0), "single-minor guard changed")
    require(counterexample["rank"] == 2, "single-minor full rank changed")

    f17 = certificate["f17_reconstruction_guard"]
    require(isinstance(f17, dict), "F17 payload missing")
    require(f17["locator_target"] == (6, 1), "F17 target changed")
    require(f17["target_stabilizer"] == (1,), "F17 target primitivity changed")
    require(f17["antipodal_cores"] == ((), ()), "F17 antipodal core changed")
    require(f17["least_signed_contacts"] == ((0, "+"), (0, "+")),
            "F17 least signed contacts changed")
    require(f17["defect_magnitudes"] == (8, 8), "F17 defect magnitude changed")

    f31 = certificate["f31_marked_obstruction"]
    require(isinstance(f31, dict), "F31 payload missing")
    require(f31["parent_target"] == (30, 9), "F31 parent target changed")
    require(f31["parent_target_stabilizer"] == (1,), "F31 parent primitivity changed")
    require(f31["child_target"] == (0, 9), "F31 child target changed")
    require(f31["child_target_stabilizer"] == (1, 30), "F31 child H changed")
    require(f31["mates"] == 121, "F31 mate count changed")
    require(f31["projectively_primitive_mates"] == 119, "F31 primitive count changed")
    require(f31["primitive_distinct_common_cores"] == 99, "F31 core count changed")
    require(f31["all_label_capacity"] == 93 and f31["all_label_excess"] == 6,
            "F31 all-label capacity changed")
    require(f31["nonzero_label_capacity"] == 90 and f31["nonzero_label_excess"] == 9,
            "F31 nonzero-label capacity changed")
    require(f31["actual_error_size"] == 3 and f31["hankel_rank"] == 3,
            "F31 actual-incidence rank changed")
    require(f31["maximal_minors"] == 560 and f31["nonzero_maximal_minors"] == 541,
            "F31 maximal-minor census changed")
    require(f31["common_field_native_pivot"] == (2, 1), "F31 pivot changed")
    require(f31["simple_side_third_moment_nonzero_for_all_mates"] is True,
            "F31 simple side third-moment guard changed")
    require(f31["named_deletions_executed"] is False,
            "F31 packet falsely claims named deletions")


def tamper_selftest(certificate: dict[str, object]) -> int:
    mutations: tuple[tuple[str, Callable[[dict[str, object]], None]], ...] = (
        ("status", lambda c: c.__setitem__("status", "PROVED")),
        ("source", lambda c: c.__setitem__("source_commit", SOURCE_COMMIT[:-1])),
        ("all-minors count", lambda c: c["all_minors"].__setitem__("matrices_checked", 728)),
        ("single minor", lambda c: c["all_minors"]["single_minor_counterexample"].__setitem__(
            "maximal_minors", (0, 0, 0))),
        ("F17 target", lambda c: c["f17_reconstruction_guard"].__setitem__(
            "locator_target", (6, 0))),
        ("F17 mark", lambda c: c["f17_reconstruction_guard"].__setitem__(
            "least_signed_contacts", ((0, "+"), (1, "+")))),
        ("child H", lambda c: c["f31_marked_obstruction"].__setitem__(
            "child_target_stabilizer", (1,))),
        ("mate count", lambda c: c["f31_marked_obstruction"].__setitem__("mates", 120)),
        ("primitive count", lambda c: c["f31_marked_obstruction"].__setitem__(
            "projectively_primitive_mates", 121)),
        ("core count", lambda c: c["f31_marked_obstruction"].__setitem__(
            "primitive_distinct_common_cores", 90)),
        ("rank", lambda c: c["f31_marked_obstruction"].__setitem__("hankel_rank", 2)),
        ("minor census", lambda c: c["f31_marked_obstruction"].__setitem__(
            "nonzero_maximal_minors", 0)),
        ("pivot", lambda c: c["f31_marked_obstruction"].__setitem__(
            "common_field_native_pivot", (0, 1))),
        ("capacity", lambda c: c["f31_marked_obstruction"].__setitem__(
            "all_label_capacity", 99)),
        ("deletions", lambda c: c["f31_marked_obstruction"].__setitem__(
            "named_deletions_executed", True)),
    )
    caught = 0
    for label, mutate in mutations:
        altered = copy.deepcopy(certificate)
        mutate(altered)
        try:
            validate_certificate(altered)
        except (CertificateError, KeyError, TypeError):
            caught += 1
        else:
            raise CertificateError(f"tamper mutation escaped validation: {label}")
    require(caught == len(mutations), "tamper self-test did not catch every mutation")
    return caught


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="explicit normal verification mode")
    parser.add_argument("--tamper", action="store_true", help="run fail-closed mutation tests")
    args = parser.parse_args(argv)
    try:
        certificate = build_certificate()
        validate_certificate(certificate)
        all_minors = certificate["all_minors"]
        f31 = certificate["f31_marked_obstruction"]
        print(
            "all-minors: "
            f"{all_minors['matrices_checked']} F3 matrices; "
            f"{all_minors['rank_drop_matrices']} rank-drop"
        )
        print(
            "F31 obstruction: "
            f"mates {f31['mates']}; primitive {f31['projectively_primitive_mates']}; "
            f"marked cores {f31['primitive_distinct_common_cores']}; "
            f"pivot {f31['common_field_native_pivot']}; rank {f31['hankel_rank']}"
        )
        print(
            "capacities: "
            f"99 > {f31['all_label_capacity']} by {f31['all_label_excess']}; "
            f"99 > {f31['nonzero_label_capacity']} by {f31['nonzero_label_excess']}"
        )
        if args.tamper:
            caught = tamper_selftest(certificate)
            print(f"tamper-selftest: caught {caught}/15 mutations")
        print("STATUS COUNTEREXAMPLE")
        return 0
    except (CertificateError, KeyError, TypeError, ValueError) as error:
        print(f"STATUS FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
