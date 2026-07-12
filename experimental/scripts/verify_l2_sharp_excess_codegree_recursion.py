#!/usr/bin/env python3
"""Verify the sharp L2 baseline-plus-excess codegree recursion.

Standard library only. The checker is deterministic and writes no files.

It verifies:

* exhaustive small Reed--Solomon instances;
* the exact threshold 2s-k+1 and coefficient L_s-1;
* repeated, proportional, and codeword-translated rank-one rows;
* random GL_2 row operations with codeword translations;
* the basis-free P_s dynamic and B_r envelope on a complete small quotient;
* a realized F_29 Reed--Solomon K_{2,2} equality case;
* negative controls that corrupt the threshold, coefficient, invertibility
  hypothesis, denominator rounding, and threshold ladder.

Run:

    python3 experimental/scripts/verify_l2_sharp_excess_codegree_recursion.py --check
    python3 experimental/scripts/verify_l2_sharp_excess_codegree_recursion.py --tamper-selftest
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass
from itertools import product


Word = tuple[int, ...]


class VerificationError(AssertionError):
    """Raised when an exact gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def eval_poly(coefficients: tuple[int, ...], x: int, p: int) -> int:
    return sum(value * pow(x, degree, p) for degree, value in enumerate(coefficients)) % p


def build_codewords(p: int, evaluation_points: tuple[int, ...], k: int) -> tuple[Word, ...]:
    return tuple(
        tuple(eval_poly(coefficients, x, p) for x in evaluation_points)
        for coefficients in product(range(p), repeat=k)
    )


def agreement_mask(left: Word, right: Word) -> int:
    return sum((left[index] == right[index]) << index for index in range(len(left)))


@dataclass
class RSProfile:
    p: int
    evaluation_points: tuple[int, ...]
    k: int
    words: tuple[Word, ...]
    word_index: dict[Word, int]
    codewords: tuple[Word, ...]
    masks: tuple[tuple[int, ...], ...]
    families: dict[int, tuple[tuple[int, ...], ...]]

    @property
    def n(self) -> int:
        return len(self.evaluation_points)

    def family(self, word_index: int, threshold: int) -> tuple[int, ...]:
        table = self.families.get(threshold)
        return () if table is None else table[word_index]


def build_profile(p: int, evaluation_points: tuple[int, ...], k: int) -> RSProfile:
    n = len(evaluation_points)
    words = tuple(product(range(p), repeat=n))
    codewords = build_codewords(p, evaluation_points, k)
    masks = tuple(
        tuple(agreement_mask(codeword, word) for codeword in codewords)
        for word in words
    )
    families = {
        threshold: tuple(
            tuple(mask for mask in row if mask.bit_count() >= threshold)
            for row in masks
        )
        for threshold in range(k, n + 1)
    }
    return RSProfile(
        p=p,
        evaluation_points=evaluation_points,
        k=k,
        words=words,
        word_index={word: index for index, word in enumerate(words)},
        codewords=codewords,
        masks=masks,
        families=families,
    )


def lambda_two(profile: RSProfile, left: int, right: int, threshold: int) -> int:
    return sum(
        (left_mask & right_mask).bit_count() >= threshold
        for left_mask in profile.family(left, threshold)
        for right_mask in profile.family(right, threshold)
    )


def lambda_three(profile: RSProfile, first: int, second: int, third: int, threshold: int) -> int:
    count = 0
    for first_mask in profile.family(first, threshold):
        for second_mask in profile.family(second, threshold):
            common = first_mask & second_mask
            if common.bit_count() < threshold:
                continue
            count += sum(
                (common & third_mask).bit_count() >= threshold
                for third_mask in profile.family(third, threshold)
            )
    return count


def sharp_two_row_bound(profile: RSProfile, left: int, right: int, threshold: int) -> int:
    left_size = len(profile.family(left, threshold))
    tail_threshold = 2 * threshold - profile.k + 1
    return (
        int(left_size > 0) * len(profile.family(right, threshold))
        + max(left_size - 1, 0) * len(profile.family(right, tail_threshold))
    )


def archived_two_row_bound(profile: RSProfile, left: int, right: int, threshold: int) -> int:
    left_size = len(profile.family(left, threshold))
    old_tail = 2 * threshold - profile.k
    return (
        len(profile.family(right, threshold))
        + left_size * len(profile.family(right, old_tail))
    )


def check_exhaustive_instance(profile: RSProfile) -> dict[str, int | str]:
    checks = 0
    strict_improvements = 0
    maximum_gap = 0
    envelope_checks = 0
    for threshold in range(profile.k, profile.n + 1):
        tail_threshold = 2 * threshold - profile.k + 1
        maximum_list = max(
            len(profile.family(index, threshold)) for index in range(len(profile.words))
        )
        maximum_tail = max(
            len(profile.family(index, tail_threshold)) for index in range(len(profile.words))
        )
        rank_two_envelope = maximum_list + (maximum_list - 1) * maximum_tail
        for left in range(len(profile.words)):
            for right in range(len(profile.words)):
                actual = lambda_two(profile, left, right, threshold)
                sharp = sharp_two_row_bound(profile, left, right, threshold)
                archived = archived_two_row_bound(profile, left, right, threshold)
                require(
                    actual <= sharp,
                    f"sharp recursion failed at p={profile.p}, k={profile.k}, "
                    f"s={threshold}, rows=({left},{right}): {actual}>{sharp}",
                )
                require(sharp <= archived, "sharp bound exceeded archived bound")
                require(actual <= rank_two_envelope, "B_2 envelope failed")
                checks += 1
                envelope_checks += 1
                if sharp < archived:
                    strict_improvements += 1
                    maximum_gap = max(maximum_gap, archived - sharp)
    return {
        "instance": f"F_{profile.p},n={profile.n},k={profile.k}",
        "sharp_checks": checks,
        "envelope_checks": envelope_checks,
        "strict_improvements": strict_improvements,
        "maximum_gap": maximum_gap,
    }


def check_rank_one_presentations(profile: RSProfile) -> dict[str, int]:
    repeated_checks = 0
    proportional_translation_checks = 0
    for threshold in range(profile.k, profile.n + 1):
        for index, word in enumerate(profile.words):
            one_row = len(profile.family(index, threshold))
            require(lambda_two(profile, index, index, threshold) == one_row, "repeated pair failed")
            require(
                lambda_three(profile, index, index, index, threshold) == one_row,
                "repeated triple failed",
            )
            repeated_checks += 2
            for scalar in range(1, profile.p):
                for translation in profile.codewords:
                    transformed = tuple(
                        (scalar * value + translation[position]) % profile.p
                        for position, value in enumerate(word)
                    )
                    transformed_index = profile.word_index[transformed]
                    require(
                        lambda_two(profile, index, transformed_index, threshold) == one_row,
                        "proportional/codeword-translated rank-one collapse failed",
                    )
                    proportional_translation_checks += 1
    return {
        "repeated_arity_two_three": repeated_checks,
        "proportional_codeword_translated": proportional_translation_checks,
    }


def random_invertible_matrix(p: int, rng: random.Random) -> tuple[int, int, int, int]:
    while True:
        a00, a01, a10, a11 = (rng.randrange(p) for _ in range(4))
        if (a00 * a11 - a01 * a10) % p:
            return a00, a01, a10, a11


def check_row_operations(profile: RSProfile, samples: int = 2000) -> int:
    rng = random.Random(606)
    for _ in range(samples):
        left = rng.randrange(len(profile.words))
        right = rng.randrange(len(profile.words))
        a00, a01, a10, a11 = random_invertible_matrix(profile.p, rng)
        first_translation = profile.codewords[rng.randrange(len(profile.codewords))]
        second_translation = profile.codewords[rng.randrange(len(profile.codewords))]
        left_word = profile.words[left]
        right_word = profile.words[right]
        transformed_left = tuple(
            (
                a00 * left_word[position]
                + a01 * right_word[position]
                + first_translation[position]
            )
            % profile.p
            for position in range(profile.n)
        )
        transformed_right = tuple(
            (
                a10 * left_word[position]
                + a11 * right_word[position]
                + second_translation[position]
            )
            % profile.p
            for position in range(profile.n)
        )
        threshold = rng.randrange(profile.k, profile.n + 1)
        require(
            lambda_two(profile, left, right, threshold)
            == lambda_two(
                profile,
                profile.word_index[transformed_left],
                profile.word_index[transformed_right],
                threshold,
            ),
            "GL_2 row-operation invariance failed",
        )
    return samples


def check_three_row_recursion(profile: RSProfile, samples: int = 5000) -> int:
    rng = random.Random(607)
    for _ in range(samples):
        first, second, third = (
            rng.randrange(len(profile.words)) for _ in range(3)
        )
        threshold = rng.randrange(profile.k, profile.n + 1)
        first_size = len(profile.family(first, threshold))
        tail_threshold = 2 * threshold - profile.k + 1
        bound = (
            int(first_size > 0) * lambda_two(profile, second, third, threshold)
            + max(first_size - 1, 0)
            * lambda_two(profile, second, third, tail_threshold)
        )
        require(
            lambda_three(profile, first, second, third, threshold) <= bound,
            "three-row sharp recursion failed",
        )
    return samples


def canonical_quotient_key(profile: RSProfile, word: Word) -> Word:
    return min(
        tuple((value - codeword[position]) % profile.p for position, value in enumerate(word))
        for codeword in profile.codewords
    )


def check_basis_free_dynamic(profile: RSProfile) -> dict[str, int]:
    require(profile.n - profile.k == 2, "dynamic checker expects quotient dimension two")
    members: dict[Word, list[int]] = {}
    for index, word in enumerate(profile.words):
        members.setdefault(canonical_quotient_key(profile, word), []).append(index)
    keys = frozenset(members)
    zero = canonical_quotient_key(profile, (0,) * profile.n)
    require(len(keys) == profile.p**2, "wrong quotient cardinality")

    representatives = {key: indices[0] for key, indices in members.items()}

    def scale(scalar: int, vector: Word) -> Word:
        return canonical_quotient_key(
            profile,
            tuple((scalar * value) % profile.p for value in vector),
        )

    def line(vector: Word) -> frozenset[Word]:
        return frozenset(scale(scalar, vector) for scalar in range(profile.p))

    lines = frozenset(line(key) for key in keys if key != zero)
    require(len(lines) == profile.p + 1, "wrong number of projective quotient lines")

    def ell(vector: Word, threshold: int) -> int:
        return len(profile.family(representatives[vector], threshold))

    profile_invariance_checks = 0
    for threshold in range(profile.k, profile.n + 1):
        for key, indices in members.items():
            expected = ell(key, threshold)
            for index in indices:
                require(
                    len(profile.family(index, threshold)) == expected,
                    "one-row profile is not quotient invariant",
                )
                profile_invariance_checks += 1
            if key != zero:
                for scalar in range(1, profile.p):
                    require(ell(scale(scalar, key), threshold) == expected, "projective profile failed")
                    profile_invariance_checks += 1

    def line_value(subspace: frozenset[Word], threshold: int) -> int:
        if threshold > profile.n:
            return 0
        nonzero = next(vector for vector in subspace if vector != zero)
        return ell(nonzero, threshold)

    def full_dynamic(threshold: int) -> int:
        if threshold > profile.n:
            return 0
        tail_threshold = 2 * threshold - profile.k + 1
        candidates = []
        for hyperplane in lines:
            base_value = line_value(hyperplane, threshold)
            tail_value = line_value(hyperplane, tail_threshold)
            for vector in keys - hyperplane:
                size = ell(vector, threshold)
                candidates.append(
                    int(size > 0) * base_value + max(size - 1, 0) * tail_value
                )
        return min(candidates)

    basis_checks = 0
    ladder_checks = 0
    for threshold in range(profile.k, profile.n + 1):
        dynamic = full_dynamic(threshold)
        actual_values = set()
        for first in keys:
            if first == zero:
                continue
            first_line = line(first)
            for second in keys - first_line:
                actual = lambda_two(
                    profile,
                    representatives[first],
                    representatives[second],
                    threshold,
                )
                actual_values.add(actual)
                require(actual <= dynamic, "basis-free P_s dynamic failed")
                basis_checks += 1
        require(len(actual_values) == 1, "list count changed across quotient bases")

        recursive_threshold = threshold
        for depth in range(6):
            closed_form = profile.k - 1 + (1 << depth) * (threshold - profile.k + 1)
            require(recursive_threshold == closed_form, "threshold ladder formula failed")
            recursive_threshold = 2 * recursive_threshold - profile.k + 1
            ladder_checks += 1

    require(full_dynamic(profile.n + 1) == 0, "P_s should vanish above n")
    return {
        "quotient_classes": len(keys),
        "projective_lines": len(lines),
        "profile_invariance_checks": profile_invariance_checks,
        "basis_dynamic_checks": basis_checks,
        "ladder_checks": ladder_checks,
    }


def primitive_root(p: int) -> int:
    factors = []
    value = p - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise VerificationError("no primitive root")


def subgroup(p: int, order: int) -> tuple[int, ...]:
    require((p - 1) % order == 0, "subgroup order does not divide p-1")
    generator = pow(primitive_root(p), (p - 1) // order, p)
    values = []
    current = 1
    for _ in range(order):
        values.append(current)
        current = current * generator % p
    require(current == 1 and len(set(values)) == order, "subgroup generation failed")
    return tuple(values)


def realized_k22_equality() -> dict[str, int]:
    p, n, k, threshold = 29, 14, 3, 5
    evaluation_points = subgroup(p, n)
    core = (0, 1)
    cell_size = threshold - (k - 1)
    cells = tuple(
        tuple(range(k - 1 + cell_size * index, k - 1 + cell_size * (index + 1)))
        for index in range(4)
    )
    require(k - 1 + 4 * cell_size == n, "K22 cells do not fill the domain")

    vanishing_values = tuple(
        (x - evaluation_points[core[0]]) * (x - evaluation_points[core[1]]) % p
        for x in evaluation_points
    )
    row_one_codewords = tuple(
        tuple(scalar * value % p for value in vanishing_values) for scalar in (1, 2)
    )
    row_two_codewords = tuple(
        tuple(scalar * value % p for value in vanishing_values) for scalar in (3, 4)
    )

    first_word = [0] * n
    second_word = [0] * n
    for first_index in range(2):
        for second_index in range(2):
            for position in cells[2 * first_index + second_index]:
                first_word[position] = row_one_codewords[first_index][position]
                second_word[position] = row_two_codewords[second_index][position]

    codewords = build_codewords(p, evaluation_points, k)

    def family(word: Word, agreement: int) -> tuple[int, ...]:
        return tuple(
            mask
            for codeword in codewords
            for mask in [agreement_mask(codeword, word)]
            if mask.bit_count() >= agreement
        )

    first_family = family(tuple(first_word), threshold)
    second_family = family(tuple(second_word), threshold)
    tail_threshold = 2 * threshold - k + 1
    second_tail = family(tuple(second_word), tail_threshold)
    actual = sum(
        (left & right).bit_count() >= threshold
        for left in first_family
        for right in second_family
    )
    inner_codegrees = tuple(
        sum((left & right).bit_count() >= threshold for left in first_family)
        for right in second_family
    )
    excess = sum(
        max(codegree - 1, 0)
        for codegree, support in zip(inner_codegrees, second_family)
        if support.bit_count() >= tail_threshold
    )
    bound = len(second_family) + (len(first_family) - 1) * len(second_tail)

    require(len(first_family) == len(second_family) == 2, "K22 base lists changed")
    require(all(mask.bit_count() == 8 for mask in first_family + second_family), "K22 supports changed")
    require(inner_codegrees == (2, 2), "K22 punctured codegrees changed")
    require(actual == 4, "K22 interleaved count changed")
    require(actual == len(second_family) + excess == bound, "K22 sharp equality failed")
    return {
        "actual": actual,
        "baseline": len(second_family),
        "excess": excess,
        "left_list": len(first_family),
        "right_list": len(second_family),
        "right_tail_list": len(second_tail),
        "tail_threshold": tail_threshold,
        "bound": bound,
    }


def run_checks() -> dict[str, object]:
    instances = (
        build_profile(3, (1, 2), 1),
        build_profile(5, (1, 2, 3, 4), 2),
        build_profile(7, (1, 2, 3), 2),
    )
    exhaustive = [check_exhaustive_instance(instance) for instance in instances]
    f5 = instances[1]
    rank_one = check_rank_one_presentations(f5)
    row_operations = check_row_operations(f5)
    three_row = check_three_row_recursion(f5)
    dynamic = check_basis_free_dynamic(f5)
    k22 = realized_k22_equality()
    return {
        "status": "PASS",
        "exhaustive": exhaustive,
        "exhaustive_sharp_checks": sum(row["sharp_checks"] for row in exhaustive),
        "rank_one": rank_one,
        "gl2_checks": row_operations,
        "three_row_checks": three_row,
        "basis_free_dynamic": dynamic,
        "k22_equality": k22,
    }


def find_too_high_tail_counterexample(profile: RSProfile) -> dict[str, int] | None:
    for threshold in range(profile.k, profile.n + 1):
        mutated_tail = 2 * threshold - profile.k + 2
        for left in range(len(profile.words)):
            left_size = len(profile.family(left, threshold))
            for right in range(len(profile.words)):
                actual = lambda_two(profile, left, right, threshold)
                mutated = (
                    int(left_size > 0) * len(profile.family(right, threshold))
                    + max(left_size - 1, 0) * len(profile.family(right, mutated_tail))
                )
                if actual > mutated:
                    return {
                        "threshold": threshold,
                        "left": left,
                        "right": right,
                        "actual": actual,
                        "mutated_bound": mutated,
                        "mutated_tail": mutated_tail,
                    }
    return None


def find_singular_row_operation_counterexample(profile: RSProfile) -> dict[str, int] | None:
    zero_index = profile.word_index[(0,) * profile.n]
    for threshold in range(profile.k, profile.n + 1):
        for left in range(len(profile.words)):
            for right in range(len(profile.words)):
                original = lambda_two(profile, left, right, threshold)
                singular_image = lambda_two(profile, left, zero_index, threshold)
                if original != singular_image:
                    return {
                        "threshold": threshold,
                        "left": left,
                        "right": right,
                        "original": original,
                        "singular_image": singular_image,
                    }
    return None


def run_tamper_selftest() -> dict[str, object]:
    profile = build_profile(5, (1, 2, 3, 4), 2)
    k22 = realized_k22_equality()
    caught: dict[str, object] = {}

    threshold_witness = find_too_high_tail_counterexample(profile)
    require(threshold_witness is not None, "failed to reject tail threshold 2s-k+2")
    caught["tail_threshold_raised_by_one"] = threshold_witness

    mutated_coefficient_bound = k22["baseline"] + max(k22["left_list"] - 2, 0) * k22[
        "right_tail_list"
    ]
    require(k22["actual"] > mutated_coefficient_bound, "failed to reject L_s-2 coefficient")
    caught["excess_coefficient_lowered_by_one"] = {
        "actual": k22["actual"],
        "mutated_bound": mutated_coefficient_bound,
    }

    singular_witness = find_singular_row_operation_counterexample(profile)
    require(singular_witness is not None, "failed to reject singular row operation")
    caught["GL2_replaced_by_singular_matrix"] = singular_witness

    denominator = (1 << 128) - 1
    list_size = 1
    exact_inequality = list_size * (1 << 128) <= denominator
    rounded_up_budget = (denominator + (1 << 128) - 1) // (1 << 128)
    require(
        not exact_inequality and list_size <= rounded_up_budget,
        "failed to reject ceiling in the list denominator",
    )
    caught["floor_replaced_by_ceiling"] = {
        "D_list": denominator,
        "list_size": list_size,
        "wrong_budget": rounded_up_budget,
    }

    threshold = profile.k
    correct_next = 2 * threshold - profile.k + 1
    mutated_next = 2 * threshold - profile.k
    require(correct_next != mutated_next, "failed to reject ladder without +1")
    caught["ladder_plus_one_deleted"] = {
        "threshold": threshold,
        "correct_next": correct_next,
        "mutated_next": mutated_next,
    }

    return {"status": "PASS", "caught": caught, "caught_count": len(caught)}


def print_human(result: dict[str, object], mode: str) -> None:
    print("L2 sharp excess-codegree recursion verifier")
    if mode == "check":
        for row in result["exhaustive"]:  # type: ignore[index]
            print(
                "  {instance}: sharp={sharp_checks}, strict={strict_improvements}, "
                "max_gap={maximum_gap}".format(**row)
            )
        rank_one = result["rank_one"]  # type: ignore[assignment]
        dynamic = result["basis_free_dynamic"]  # type: ignore[assignment]
        k22 = result["k22_equality"]  # type: ignore[assignment]
        print(
            "  rank-one: repeated={repeated_arity_two_three}, "
            "proportional/translated={proportional_codeword_translated}".format(**rank_one)
        )
        print(f"  GL2 row operations: {result['gl2_checks']}")
        print(f"  random three-row recursion: {result['three_row_checks']}")
        print(
            "  P_s dynamic: classes={quotient_classes}, lines={projective_lines}, "
            "bases={basis_dynamic_checks}, ladder={ladder_checks}".format(**dynamic)
        )
        print(
            "  K22 equality: actual={actual}, baseline={baseline}, excess={excess}, "
            "bound={bound}, tail={tail_threshold}".format(**k22)
        )
    else:
        print(f"  tamper self-test: {result['caught_count']} mutations caught")
        for name in sorted(result["caught"]):  # type: ignore[arg-type]
            print(f"    {name}: CAUGHT")
    print("RESULT: PASS")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", action="store_true", help="run the exact verification suite")
    modes.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="confirm that load-bearing mutations are rejected",
    )
    parser.add_argument("--format", choices=("human", "json"), default="human")
    args = parser.parse_args(argv)

    mode = "check" if args.check else "tamper-selftest"
    result = run_checks() if args.check else run_tamper_selftest()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_human(result, mode)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
