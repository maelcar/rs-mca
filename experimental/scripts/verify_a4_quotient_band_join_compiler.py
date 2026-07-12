#!/usr/bin/env python3
"""Verify the A4 join-closed quotient-band compiler packet."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import resource
import sys
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "a4_quotient_band_join_compiler.v1"
STATUS = "PROVED_JOIN_CLOSED_QUOTIENT_BAND_COMPILER"
BASE_COMMIT = "36de5bfcc7d6e0ca44806112acec2f4a1b4a7532"
GRANDPARENT_COMMIT = "0aee8592065efacedc9f71679e6eda4f704f2469"
PARENT_COMMIT = "bc51155206842c2944340ad9b1da429491383dec"
CAP_BYTES = 1024**3
NOTE_PATH = Path(
    "experimental/notes/thresholds/a4_quotient_band_join_compiler.md"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_a4_quotient_band_join_compiler.py"
)
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/a4-quotient-band-join-compiler/"
    "a4_quotient_band_join_compiler.json"
)
SOURCE_HASHES = {
    "experimental/asymptotic_rs_mca_frontiers.tex":
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
    "experimental/notes/thresholds/a4_quotient_major_compiler.md":
        "4b924af30dc444ab770620cede6895fca47674e64e97d519ecbfa83bd6939222",
    "experimental/notes/thresholds/"
    "a4_trace_quotient_rank_centered_compiler.md":
        "1a0a8df519e9e5e5c4b1738ae1d7639d93c38eb88b002351c53130fa97959cd1",
    "experimental/scripts/"
    "verify_a4_trace_quotient_rank_centered_compiler.py":
        "f8dd982e794c9f02303f6b2f5b002fe34b4ea50a3e2e9b84f07eea8285c7d56f",
    "experimental/data/certificates/a4-trace-quotient-rank-centered/"
    "a4_trace_quotient_rank_centered_compiler.json":
        "9163def59f268a4a5759c0cc1fe55d5935d179bbf701aa43c8363a553bc8b6fe",
    "experimental/notes/thresholds/a4_nonuniform_centered_compiler.md":
        "0fb9b0bc1b5706944e07ab02ef10ca67fe9707ff9eab75d54f09055d35725320",
    "experimental/scripts/verify_a4_nonuniform_centered_compiler.py":
        "578551df31b2dd9568eaf9f8058c878696c4e6940afd05669f1666573966beba",
    "experimental/data/certificates/a4-nonuniform-centered-compiler/"
    "a4_nonuniform_centered_compiler.json":
        "ee1cb9d3d4a92e942624f2e0b8fc8c33142dd0cf935086e8680c18699388b0b9",
}


class CheckFailure(AssertionError):
    """Raised when an exact gate fails."""


class Checks:
    def __init__(self) -> None:
        self.count = 0

    def require(self, condition: bool, label: str) -> None:
        if not condition:
            raise CheckFailure(label)
        self.count += 1

    def equal(self, left: Any, right: Any, label: str) -> None:
        self.require(left == right, f"{label}: {left!r} != {right!r}")

    def close(
        self, left: float, right: float, tolerance: float, label: str
    ) -> None:
        self.require(
            math.isfinite(left)
            and math.isfinite(right)
            and abs(left - right) <= tolerance,
            f"{label}: {left!r} not within {tolerance} of {right!r}",
        )


def impose_cap(checks: Checks) -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    target = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    resource.setrlimit(resource.RLIMIT_AS, (target, hard))
    checks.require(target <= CAP_BYTES, "address-space cap")
    return target


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    current = Path.cwd().resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise CheckFailure("repository root not found")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def payload_hash(artifact: dict[str, Any]) -> str:
    payload = copy.deepcopy(artifact)
    payload.pop("payload_sha256", None)
    return hashlib.sha256(canonical(payload)).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


Partition = tuple[int, ...]


def partitions(n: int) -> list[Partition]:
    if n == 0:
        return [()]
    out: list[Partition] = []
    row = [0]

    def rec(maximum: int) -> None:
        if len(row) == n:
            out.append(tuple(row))
            return
        for label in range(maximum + 2):
            row.append(label)
            rec(max(maximum, label))
            row.pop()

    rec(0)
    return out


def blocks(partition: Partition) -> list[tuple[int, ...]]:
    grouped: dict[int, list[int]] = {}
    for index, label in enumerate(partition):
        grouped.setdefault(label, []).append(index)
    return [tuple(grouped[label]) for label in sorted(grouped)]


def normalize_partition(labels: Iterable[int]) -> Partition:
    image: dict[int, int] = {}
    out: list[int] = []
    for label in labels:
        if label not in image:
            image[label] = len(image)
        out.append(image[label])
    return tuple(out)


def refines(finer: Partition, coarser: Partition) -> bool:
    image: dict[int, int] = {}
    for left, right in zip(finer, coarser):
        if left in image and image[left] != right:
            return False
        image[left] = right
    return True


def partition_join(left: Partition, right: Partition) -> Partition:
    n = len(left)
    parent = list(range(n))

    def root(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def merge(first: int, second: int) -> None:
        first_root, second_root = root(first), root(second)
        if first_root != second_root:
            parent[second_root] = first_root

    for partition in (left, right):
        first_by_label: dict[int, int] = {}
        for index, label in enumerate(partition):
            if label in first_by_label:
                merge(first_by_label[label], index)
            else:
                first_by_label[label] = index
    return normalize_partition(root(index) for index in range(n))


def partition_meet(left: Partition, right: Partition) -> Partition:
    return normalize_partition(zip(left, right))


def join_all(rows: Iterable[Partition]) -> Partition:
    items = list(rows)
    if not items:
        raise CheckFailure("empty partition join")
    answer = items[0]
    for item in items[1:]:
        answer = partition_join(answer, item)
    return answer


class VectorSpace:
    def __init__(self, prime: int, dimension: int) -> None:
        self.p = prime
        self.d = dimension
        self.q = prime**dimension
        self.digits: list[tuple[int, ...]] = []
        for value in range(self.q):
            cursor = value
            row = []
            for _ in range(dimension):
                row.append(cursor % prime)
                cursor //= prime
            self.digits.append(tuple(row))
        self.encode = {row: index for index, row in enumerate(self.digits)}

    def add(self, left: int, right: int) -> int:
        return self.encode[
            tuple(
                (x + y) % self.p
                for x, y in zip(self.digits[left], self.digits[right])
            )
        ]

    def sub(self, left: int, right: int) -> int:
        return self.encode[
            tuple(
                (x - y) % self.p
                for x, y in zip(self.digits[left], self.digits[right])
            )
        ]

    def scale(self, scalar: int, value: int) -> int:
        return self.encode[
            tuple((scalar * x) % self.p for x in self.digits[value])
        ]

    def dot(self, left: int, right: int) -> int:
        return sum(
            x * y for x, y in zip(self.digits[left], self.digits[right])
        ) % self.p


def span(generators: Iterable[int], space: VectorSpace) -> frozenset[int]:
    answer = {0}
    for generator in generators:
        old = tuple(answer)
        for value in old:
            for scalar in range(space.p):
                answer.add(space.add(value, space.scale(scalar, generator)))
    return frozenset(answer)


def sum_space(
    left: frozenset[int], right: frozenset[int], space: VectorSpace
) -> frozenset[int]:
    return span((*left, *right), space)


def within_space(
    values: tuple[int, ...], partition: Partition, space: VectorSpace
) -> frozenset[int]:
    generators: list[int] = []
    for block in blocks(partition):
        base = block[0]
        for index in block[1:]:
            generators.append(space.sub(values[index], values[base]))
    return span(generators, space)


def character_band(
    within: frozenset[int], space: VectorSpace
) -> frozenset[int]:
    return frozenset(
        character
        for character in range(space.q)
        if all(space.dot(character, value) == 0 for value in within)
    )


def phase_f2(character: int, value: int, space: VectorSpace) -> int:
    if space.p != 2:
        raise CheckFailure("integer phase requested outside characteristic two")
    return -1 if space.dot(character, value) else 1


def subset_sum_values(
    values: list[int], weight: int, space: VectorSpace
) -> list[int]:
    out: list[int] = []
    for subset in combinations(range(len(values)), weight):
        total = 0
        for index in subset:
            total = space.add(total, values[index])
        out.append(total)
    return out


def character_sum_f2(
    subset_sums: list[int], character: int, space: VectorSpace
) -> int:
    return sum(phase_f2(character, value, space) for value in subset_sums)


def elementary_coefficient(values: list[int], weight: int) -> int:
    coefficients = [0] * (weight + 1)
    coefficients[0] = 1
    degree = 0
    for value in values:
        degree = min(weight, degree + 1)
        for index in range(degree, 0, -1):
            coefficients[index] += value * coefficients[index - 1]
    return coefficients[weight]


def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            out[i + j] += first * second
    return out


def polynomial_power(base: list[int], exponent: int) -> list[int]:
    answer = [1]
    for _ in range(exponent):
        answer = polynomial_multiply(answer, base)
    return answer


def allocations(limits: list[int], total: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    row: list[int] = []

    def rec(index: int, left: int) -> None:
        if index == len(limits):
            if left == 0:
                out.append(tuple(row))
            return
        for value in range(min(limits[index], left) + 1):
            row.append(value)
            rec(index + 1, left - value)
            row.pop()

    rec(0, total)
    return out


def poset_mobius(family: tuple[Partition, ...]):
    cache: dict[tuple[Partition, Partition], int] = {}

    def mobius(lower: Partition, upper: Partition) -> int:
        if not refines(lower, upper):
            return 0
        if lower == upper:
            return 1
        key = (lower, upper)
        if key not in cache:
            cache[key] = -sum(
                mobius(lower, middle)
                for middle in family
                if middle != upper
                and refines(lower, middle)
                and refines(middle, upper)
            )
        return cache[key]

    return mobius


def family_is_join_closed(family: tuple[Partition, ...]) -> bool:
    members = set(family)
    return all(
        partition_join(left, right) in members
        for left in family
        for right in family
    )


def band_data(
    values: tuple[int, ...],
    family: tuple[Partition, ...],
    space: VectorSpace,
) -> tuple[
    dict[Partition, frozenset[int]],
    dict[Partition, frozenset[int]],
    dict[Partition, frozenset[int]],
]:
    within = {
        partition: within_space(values, partition, space)
        for partition in family
    }
    bands = {
        partition: character_band(within[partition], space)
        for partition in family
    }
    union = set().union(*(bands[partition] for partition in family))
    strata: dict[Partition, set[int]] = {partition: set() for partition in family}
    for character in union:
        factor_partitions = [
            partition
            for partition in family
            if character in bands[partition]
        ]
        maximum = join_all(factor_partitions)
        if maximum not in strata:
            raise CheckFailure("join-closed maximum missing")
        strata[maximum].add(character)
    return within, bands, {
        partition: frozenset(strata[partition] - {0})
        for partition in family
    }


def partition_text(partition: Partition) -> str:
    return "|".join(
        "".join(str(index + 1) for index in block)
        for block in blocks(partition)
    )


def restrict_partition(
    partition: Partition, indices: tuple[int, ...]
) -> Partition:
    return normalize_partition(partition[index] for index in indices)


def pair_merge_partition(n: int, first: int, second: int) -> Partition:
    labels = list(range(n))
    labels[second] = labels[first]
    return normalize_partition(labels)


def verify_family_strata(
    checks: Checks,
    *,
    name: str,
    values: tuple[int, ...],
    family: tuple[Partition, ...],
    space: VectorSpace,
) -> tuple[
    dict[Partition, frozenset[int]],
    dict[Partition, frozenset[int]],
    dict[Partition, frozenset[int]],
]:
    checks.require(family_is_join_closed(family), f"{name}: join closure")
    checks.equal(len(set(family)), len(family), f"{name}: distinct kernels")
    within, bands, strata = band_data(values, family, space)
    mobius = poset_mobius(family)
    for partition in family:
        checks.equal(
            len(bands[partition]),
            space.q // len(within[partition]),
            f"{name}: annihilator rank {partition_text(partition)}",
        )
        layered: set[int] = set()
        for upper in family:
            if refines(partition, upper):
                checks.require(
                    not layered.intersection(strata[upper]),
                    f"{name}: disjoint strata {partition_text(partition)}",
                )
                layered.update(strata[upper])
        checks.equal(
            layered,
            set(bands[partition]) - {0},
            f"{name}: band decomposition {partition_text(partition)}",
        )
        inversion = sum(
            mobius(partition, upper) * (len(bands[upper]) - 1)
            for upper in family
            if refines(partition, upper)
        )
        checks.equal(
            inversion,
            len(strata[partition]),
            f"{name}: selected-poset Mobius {partition_text(partition)}",
        )
        checks.require(
            inversion >= 0,
            f"{name}: nonnegative stratum {partition_text(partition)}",
        )
    return within, bands, strata


def class_representatives(
    values: tuple[int, ...], anchor: Partition
) -> dict[int, list[int]]:
    by_size: dict[int, list[int]] = {}
    for block in blocks(anchor):
        by_size.setdefault(len(block), []).append(values[block[0]])
    return by_size


def quotient_representative(
    value: int, within: frozenset[int], space: VectorSpace
) -> int:
    return min(space.add(value, shift) for shift in within)


def projected_collision_sum(
    subset_sums: list[int],
    within: frozenset[int],
    space: VectorSpace,
) -> int:
    counts: dict[int, int] = {}
    for value in subset_sums:
        representative = quotient_representative(value, within, space)
        counts[representative] = counts.get(representative, 0) + 1
    quotient_order = space.q // len(within)
    return quotient_order * sum(count * count for count in counts.values())


def stratum_energy_data(
    checks: Checks,
    *,
    name: str,
    values: tuple[int, ...],
    family: tuple[Partition, ...],
    space: VectorSpace,
    anchor: Partition,
    stratum_partition: Partition,
    within: dict[Partition, frozenset[int]],
    bands: dict[Partition, frozenset[int]],
    strata: dict[Partition, frozenset[int]],
) -> tuple[dict[tuple[int, int], Fraction], dict[int, list[int]], list[int]]:
    checks.require(
        refines(anchor, stratum_partition),
        f"{name}: eligible anchor order",
    )
    if space.p != 2:
        raise CheckFailure("exact integer energy suite requires p=2")
    mobius = poset_mobius(family)
    by_size = class_representatives(values, anchor)
    z_values: dict[tuple[int, int], Fraction] = {}
    for multiplicity, representatives in sorted(by_size.items()):
        for weight in range(len(representatives) + 1):
            subset_sums = subset_sum_values(
                representatives, weight, space
            )
            m_value = math.comb(len(representatives), weight)
            inversion = 0
            for upper in family:
                if not refines(stratum_partition, upper):
                    continue
                projected = projected_collision_sum(
                    subset_sums, within[upper], space
                )
                direct_band = sum(
                    character_sum_f2(subset_sums, character, space) ** 2
                    for character in bands[upper]
                )
                checks.equal(
                    projected,
                    direct_band,
                    f"{name}: projected Parseval "
                    f"{partition_text(anchor)}->{partition_text(upper)} "
                    f"s={multiplicity} j={weight}",
                )
                inversion += (
                    mobius(stratum_partition, upper)
                    * (projected - m_value * m_value)
                )
            direct_stratum = sum(
                character_sum_f2(subset_sums, character, space) ** 2
                for character in strata[stratum_partition]
            )
            checks.equal(
                inversion,
                direct_stratum,
                f"{name}: direct Mobius energy "
                f"{partition_text(stratum_partition)} "
                f"s={multiplicity} j={weight}",
            )
            checks.require(
                inversion >= 0,
                f"{name}: nonnegative shell energy",
            )
            z_value = Fraction(inversion, m_value * m_value)
            checks.require(
                Fraction(0) <= z_value <= len(strata[stratum_partition]),
                f"{name}: normalized shell range",
            )
            if weight in (0, len(representatives)):
                checks.equal(
                    z_value,
                    Fraction(len(strata[stratum_partition])),
                    f"{name}: shell endpoint",
                )
            z_values[(multiplicity, weight)] = z_value
    slots = [
        multiplicity
        for multiplicity in sorted(by_size)
        for _ in range(multiplicity)
    ]
    return z_values, by_size, slots


def factorization_at_anchor(
    checks: Checks,
    *,
    name: str,
    values: tuple[int, ...],
    anchor: Partition,
    characters: frozenset[int],
    space: VectorSpace,
) -> None:
    by_size = class_representatives(values, anchor)
    for character in characters:
        full_values = [
            phase_f2(character, value, space) for value in values
        ]
        full = [1]
        for phase in full_values:
            full = polynomial_multiply(full, [1, phase])
        factored = [1]
        for multiplicity, representatives in sorted(by_size.items()):
            class_values = [
                phase_f2(character, value, space)
                for value in representatives
            ]
            class_poly = [
                elementary_coefficient(class_values, weight)
                for weight in range(len(class_values) + 1)
            ]
            factored = polynomial_multiply(
                factored,
                polynomial_power(class_poly, multiplicity),
            )
        checks.equal(
            factored,
            full,
            f"{name}: full-slice factorization {partition_text(anchor)}",
        )


def pairwise_compiler(
    checks: Checks,
    *,
    name: str,
    values: tuple[int, ...],
    family: tuple[Partition, ...],
    space: VectorSpace,
    anchor: Partition,
    stratum_partition: Partition,
    within: dict[Partition, frozenset[int]],
    bands: dict[Partition, frozenset[int]],
    strata: dict[Partition, frozenset[int]],
) -> dict[int, tuple[float, float]]:
    z_values, by_size, slots = stratum_energy_data(
        checks,
        name=name,
        values=values,
        family=family,
        space=space,
        anchor=anchor,
        stratum_partition=stratum_partition,
        within=within,
        bands=bands,
        strata=strata,
    )
    factorization_at_anchor(
        checks,
        name=name,
        values=values,
        anchor=anchor,
        characters=bands[anchor],
        space=space,
    )
    if len(slots) < 2:
        return {}
    limits = [len(by_size[multiplicity]) for multiplicity in slots]
    results: dict[int, tuple[float, float]] = {}
    for total_weight in range(len(values) + 1):
        denominator = math.comb(len(values), total_weight)
        compiler = 0.0
        for allocation in allocations(limits, total_weight):
            m_values = [
                math.comb(limits[index], allocation[index])
                for index in range(len(slots))
            ]
            energies = [
                z_values[(slots[index], allocation[index])]
                for index in range(len(slots))
            ]
            theta = min(
                math.sqrt(float(energies[first] * energies[second]))
                for first in range(len(slots))
                for second in range(first + 1, len(slots))
            )
            numerator_weight = math.prod(m_values)
            compiler += numerator_weight * theta
        compiler /= denominator
        actual = sum(
            abs(
                elementary_coefficient(
                    [
                        phase_f2(character, value, space)
                        for value in values
                    ],
                    total_weight,
                )
            )
            for character in strata[stratum_partition]
        ) / denominator
        checks.require(
            actual <= compiler + 1e-10,
            f"{name}: pairwise compiler m={total_weight}",
        )
        checks.require(
            actual <= len(strata[stratum_partition]),
            f"{name}: cardinality fallback m={total_weight}",
        )
        results[total_weight] = (actual, compiler)
    return results


def partition_census_suite(checks: Checks) -> dict[str, Any]:
    cases = [
        ("n4_f2", (0, 1, 2, 4), VectorSpace(2, 3)),
        ("n5_f2", (0, 1, 2, 4, 3), VectorSpace(2, 3)),
        ("n4_f3", (0, 1, 3, 4), VectorSpace(3, 2)),
    ]
    records: dict[str, Any] = {}
    for name, values, space in cases:
        rows = partitions(len(values))
        pair_count = 0
        for left in rows:
            left_within = within_space(values, left, space)
            left_band = character_band(left_within, space)
            for right in rows:
                right_within = within_space(values, right, space)
                right_band = character_band(right_within, space)
                joined = partition_join(left, right)
                joined_within = within_space(values, joined, space)
                joined_band = character_band(joined_within, space)
                checks.require(
                    refines(left, joined) and refines(right, joined),
                    f"{name}: least common coarsening upper",
                )
                checks.equal(
                    joined_within,
                    sum_space(left_within, right_within, space),
                    f"{name}: W join=sum",
                )
                checks.equal(
                    joined_band,
                    left_band.intersection(right_band),
                    f"{name}: H join=intersection",
                )
                pair_count += 1
        records[name] = {
            "partitions": len(rows),
            "ordered_pairs": pair_count,
            "join_identity_checks": 2 * pair_count,
        }
    checks.equal(records["n4_f2"]["partitions"], 15, "Bell number n=4")
    checks.equal(records["n5_f2"]["partitions"], 52, "Bell number n=5")
    checks.equal(
        records["n4_f2"]["join_identity_checks"],
        450,
        "n=4 identity count",
    )
    checks.equal(
        records["n5_f2"]["join_identity_checks"],
        5408,
        "n=5 identity count",
    )
    return records


def diamond_suite(checks: Checks) -> dict[str, Any]:
    space = VectorSpace(2, 2)
    values = (0, 1, 2, 3)
    zero = (0, 1, 2, 3)
    left = (0, 0, 1, 1)
    right = (0, 1, 0, 1)
    top = (0, 0, 0, 0)
    family = (zero, left, right, top)
    checks.equal(partition_join(left, right), top, "diamond join")
    within, bands, strata = verify_family_strata(
        checks,
        name="diamond",
        values=values,
        family=family,
        space=space,
    )
    checks.equal(
        [len(bands[row]) for row in family],
        [4, 2, 2, 1],
        "diamond band sizes",
    )
    checks.equal(
        [len(bands[row]) - 1 for row in family],
        [3, 1, 1, 0],
        "diamond centered cumulative sizes",
    )
    checks.equal(
        [len(strata[row]) for row in family],
        [1, 1, 1, 0],
        "diamond stratum sizes",
    )
    coefficients = {
        character: elementary_coefficient(
            [
                phase_f2(character, value, space)
                for value in values
            ],
            2,
        )
        for character in range(1, space.q)
    }
    checks.equal(
        list(coefficients.values()),
        [-2, -2, -2],
        "diamond degree-two coefficients",
    )
    compiler_left = pairwise_compiler(
        checks,
        name="diamond-left",
        values=values,
        family=family,
        space=space,
        anchor=left,
        stratum_partition=left,
        within=within,
        bands=bands,
        strata=strata,
    )
    compiler_right = pairwise_compiler(
        checks,
        name="diamond-right",
        values=values,
        family=family,
        space=space,
        anchor=right,
        stratum_partition=right,
        within=within,
        bands=bands,
        strata=strata,
    )
    checks.close(
        compiler_left[2][0], 1 / 3, 1e-12, "diamond actual left"
    )
    checks.close(
        compiler_left[2][1], 1 / 3, 1e-12, "diamond compiler left"
    )
    checks.close(
        compiler_right[2][1], 1 / 3, 1e-12, "diamond compiler right"
    )
    chain = (zero, left, top)
    chain_mobius = poset_mobius(chain)
    checks.equal(chain_mobius(zero, top), 0, "chain distant Mobius zero")
    chain_within, chain_bands, chain_strata = verify_family_strata(
        checks,
        name="diamond-chain",
        values=values,
        family=chain,
        space=space,
    )
    checks.equal(
        [len(chain_strata[row]) for row in chain],
        [2, 1, 0],
        "chain adjacent shells",
    )
    return {
        "band_sizes": [4, 2, 2, 1],
        "centered_cumulative_sizes": [3, 1, 1, 0],
        "stratum_sizes": [1, 1, 1, 0],
        "degree_two_coefficients": list(coefficients.values()),
        "degree_two_normalized_loss": "1/3",
        "left_anchor_pairwise": "1/3",
        "right_anchor_pairwise": "1/3",
        "chain_shell_sizes": [2, 1, 0],
        "chain_distant_mobius": 0,
    }


def multi_anchor_suite(checks: Checks) -> dict[str, Any]:
    space = VectorSpace(2, 3)
    values = (2, 1, 6, 0, 2)
    anchor = (0, 0, 0, 1, 2)
    stratum_partition = (0, 0, 0, 1, 0)
    family = (anchor, stratum_partition)
    checks.require(
        refines(anchor, stratum_partition),
        "multi-anchor refinement",
    )
    effective_span = span(
        (
            space.sub(value, values[0])
            for value in values
        ),
        space,
    )
    checks.equal(len(effective_span), space.q, "multi-anchor full span")
    within, bands, strata = verify_family_strata(
        checks,
        name="multi-anchor",
        values=values,
        family=family,
        space=space,
    )
    checks.equal(
        strata[stratum_partition],
        frozenset({3}),
        "multi-anchor nonempty top stratum",
    )
    finer_results = pairwise_compiler(
        checks,
        name="multi-anchor-finer",
        values=values,
        family=family,
        space=space,
        anchor=anchor,
        stratum_partition=stratum_partition,
        within=within,
        bands=bands,
        strata=strata,
    )
    coarser_results = pairwise_compiler(
        checks,
        name="multi-anchor-coarser",
        values=values,
        family=family,
        space=space,
        anchor=stratum_partition,
        stratum_partition=stratum_partition,
        within=within,
        bands=bands,
        strata=strata,
    )
    finer_value = finer_results[2][1]
    coarser_value = coarser_results[2][1]
    actual = finer_results[2][0]
    checks.close(finer_value, 0.4, 1e-12, "multi-anchor finer compiler")
    checks.close(coarser_value, 1.0, 1e-12, "multi-anchor coarser compiler")
    checks.close(
        coarser_results[2][0],
        actual,
        1e-12,
        "multi-anchor common stratum target",
    )
    checks.close(
        min(finer_value, coarser_value),
        finer_value,
        1e-12,
        "whole-anchor minimum",
    )
    checks.require(
        finer_value < coarser_value,
        "whole-anchor choice is strict",
    )
    return {
        "values": list(values),
        "finer_anchor": partition_text(anchor),
        "coarser_anchor": partition_text(stratum_partition),
        "stratum_characters": sorted(strata[stratum_partition]),
        "weight": 2,
        "actual_normalized_loss": format(actual, ".12g"),
        "finer_anchor_compiler": format(finer_value, ".12g"),
        "coarser_anchor_compiler": format(coarser_value, ".12g"),
        "whole_anchor_minimum": format(
            min(finer_value, coarser_value),
            ".12g",
        ),
        "compositionwise_anchor_mixing_allowed": False,
    }


def falsifier_suite(checks: Checks) -> dict[str, Any]:
    records: dict[str, Any] = {}

    # Chosen subposet Mobius, not the ambient partition-lattice value.
    space2 = VectorSpace(2, 2)
    values2 = (0, 1, 0, 2)
    zero = (0, 1, 2, 3)
    tau = (0, 0, 0, 1)
    family = (zero, tau)
    _, bands, strata = verify_family_strata(
        checks,
        name="wrong-mobius",
        values=values2,
        family=family,
        space=space2,
    )
    chosen_mu = poset_mobius(family)(zero, tau)
    ambient_mu = poset_mobius(tuple(partitions(4)))(zero, tau)
    chosen_size = (len(bands[zero]) - 1) + chosen_mu * (
        len(bands[tau]) - 1
    )
    ambient_printed = (len(bands[zero]) - 1) + ambient_mu * (
        len(bands[tau]) - 1
    )
    checks.equal(chosen_mu, -1, "selected two-element Mobius")
    checks.equal(chosen_size, len(strata[zero]), "selected Mobius size")
    checks.equal(chosen_size, 2, "selected stratum target")
    checks.equal(ambient_printed, 5, "ambient Mobius falsifier")
    records["ambient_mobius"] = {
        "chosen_mu": chosen_mu,
        "ambient_mu": ambient_mu,
        "true_stratum": chosen_size,
        "ambient_printed": ambient_printed,
        "ambient_substitution_valid": False,
    }

    # Missing incomparable join leaves a nontrivial intersection unassigned.
    space3 = VectorSpace(2, 3)
    values3 = (0, 1, 3, 4)
    left = (0, 0, 1, 2)
    right = (0, 1, 1, 2)
    joined = partition_join(left, right)
    left_band = character_band(
        within_space(values3, left, space3), space3
    )
    right_band = character_band(
        within_space(values3, right, space3), space3
    )
    joined_band = character_band(
        within_space(values3, joined, space3), space3
    )
    nontrivial_intersection = (left_band & right_band) - {0}
    nontrivial_union = (left_band | right_band) - {0}
    raw_sum = len(left_band - {0}) + len(right_band - {0})
    checks.require(not family_is_join_closed((left, right)), "missing join")
    checks.equal(len(nontrivial_intersection), 1, "missing-join overlap")
    checks.equal(len(nontrivial_union), 5, "missing-join union")
    checks.equal(raw_sum, 6, "missing-join double charge")
    checks.equal(
        left_band & right_band,
        joined_band,
        "missing-join repaired intersection",
    )
    meet = partition_meet(left, right)
    checks.require(meet != joined, "meet differs from join")
    checks.require(
        within_space(values3, meet, space3)
        != within_space(values3, joined, space3),
        "meet-for-join falsifier",
    )
    records["missing_join"] = {
        "join_closed": False,
        "nontrivial_intersection": 1,
        "nontrivial_union": 5,
        "raw_double_charge": 6,
        "meet_substitution_valid": False,
    }

    # Restriction need not commute with a nonnested full-domain join.
    first = (0, 0, 1)
    second = (0, 1, 1)
    indices = (0, 2)
    live_first = restrict_partition(first, indices)
    live_second = restrict_partition(second, indices)
    live_join = partition_join(live_first, live_second)
    restricted_full_join = restrict_partition(
        partition_join(first, second), indices
    )
    checks.equal(live_first, (0, 1), "live first discrete")
    checks.equal(live_second, (0, 1), "live second discrete")
    checks.equal(live_join, (0, 1), "actual live join")
    checks.equal(restricted_full_join, (0, 0), "restricted full join")
    checks.require(
        live_join != restricted_full_join,
        "restriction/join noncommutation",
    )
    records["live_restriction"] = {
        "actual_live_join": partition_text(live_join),
        "restricted_full_join": partition_text(restricted_full_join),
        "restriction_commutes_with_join": False,
    }

    # Coincident bands create empty lower strata, never negative ones.
    space1 = VectorSpace(2, 1)
    duplicate_values = (0, 0, 1, 1)
    duplicate_left = (0, 0, 1, 2)
    duplicate_right = (0, 1, 2, 2)
    duplicate_top = partition_join(duplicate_left, duplicate_right)
    duplicate_family = (
        duplicate_left,
        duplicate_right,
        duplicate_top,
    )
    _, duplicate_bands, duplicate_strata = verify_family_strata(
        checks,
        name="duplicate-bands",
        values=duplicate_values,
        family=duplicate_family,
        space=space1,
    )
    checks.equal(
        [len(duplicate_bands[row]) for row in duplicate_family],
        [2, 2, 2],
        "duplicate band sizes",
    )
    checks.equal(
        [len(duplicate_strata[row]) for row in duplicate_family],
        [0, 0, 1],
        "duplicate empty strata",
    )
    records["duplicate_bands"] = {
        "band_sizes": [2, 2, 2],
        "stratum_sizes": [0, 0, 1],
        "negative_stratum_created": False,
    }

    # The all-singleton anchor has one slot and needs cardinality fallback.
    d1_values = [0, 1, 2]
    d1_space = VectorSpace(2, 2)
    d1_coefficients = [
        elementary_coefficient(
            [
                phase_f2(character, value, d1_space)
                for value in d1_values
            ],
            1,
        )
        for character in range(1, d1_space.q)
    ]
    d1_l1 = Fraction(sum(abs(value) for value in d1_coefficients), 3)
    d1_eta = Fraction(
        sum(value * value for value in d1_coefficients), 9
    )
    checks.equal(d1_l1, Fraction(1), "D-star-one true loss")
    checks.equal(d1_eta, Fraction(1, 3), "D-star-one fake eta")
    checks.require(d1_l1 > d1_eta, "D-star-one falsifier")
    records["all_singletons"] = {
        "d_star": 1,
        "normalized_l1": fraction_text(d1_l1),
        "fake_one_slot_eta": fraction_text(d1_eta),
        "pairwise_theorem_valid": False,
        "cardinality_fallback_required": True,
    }

    # Three independent pair-merges have exponential join closure.
    discrete6 = tuple(range(6))
    generators = [
        pair_merge_partition(6, 0, 1),
        pair_merge_partition(6, 2, 3),
        pair_merge_partition(6, 4, 5),
    ]
    closure = {discrete6, *generators}
    changed = True
    while changed:
        changed = False
        for first_partition in tuple(closure):
            for second_partition in tuple(closure):
                joined_partition = partition_join(
                    first_partition, second_partition
                )
                if joined_partition not in closure:
                    closure.add(joined_partition)
                    changed = True
    checks.equal(len(closure), 8, "three-generator join closure")
    records["closure_entropy"] = {
        "generators": 3,
        "closure_size": len(closure),
        "subexponential_automatic": False,
    }

    # One-sided cumulative upper bounds cannot be naively inverted.
    exact_cumulative = (3, 1, 1, 0)
    upper_bounds = (3, 2, 2, 0)
    exact_shell = (
        exact_cumulative[0]
        - exact_cumulative[1]
        - exact_cumulative[2]
        + exact_cumulative[3]
    )
    naive_shell = (
        upper_bounds[0]
        - upper_bounds[1]
        - upper_bounds[2]
        + upper_bounds[3]
    )
    checks.equal(exact_shell, 1, "exact diamond shell")
    checks.equal(naive_shell, -1, "one-sided inversion falsifier")
    records["one_sided_energy"] = {
        "exact_cumulative": list(exact_cumulative),
        "valid_upper_bounds": list(upper_bounds),
        "exact_shell": exact_shell,
        "naive_signed_result": naive_shell,
        "one_sided_inversion_valid": False,
    }

    # The inherited PO3 marker erasure remains false.
    quotient_values = [0, 0, 1]
    m_values = [math.comb(3, weight) for weight in range(4)]
    e_values = [
        elementary_coefficient(
            [1, 1, -1],
            weight,
        )
        for weight in range(4)
    ]
    compiler = Fraction(0)
    for allocation in allocations([3, 3, 3], 3):
        weights = [m_values[index] for index in allocation]
        pair_terms = [
            Fraction(
                abs(e_values[allocation[first]] * e_values[allocation[second]]),
                weights[first] * weights[second],
            )
            for first in range(3)
            for second in range(first + 1, 3)
        ]
        compiler += Fraction(math.prod(weights), math.comb(9, 3)) * min(
            pair_terms
        )
    po3_component = Fraction(
        abs(sum(1 if value == 0 else -1 for value in quotient_values)),
        len(quotient_values),
    )
    checks.equal(compiler, Fraction(1, 7), "PO3 unmarked compiler")
    checks.equal(po3_component, Fraction(1, 3), "PO3 component")
    checks.require(po3_component > compiler, "PO3 marker falsifier")
    records["po3_markers"] = {
        "unmarked_pairwise": fraction_text(compiler),
        "one_full_fiber_component": fraction_text(po3_component),
        "erasing_markers_valid": False,
    }

    # Incomparable anchors need not contain a stratum character.
    core_space = VectorSpace(2, 2)
    core_values = (0, 1, 2, 3)
    core_left = (0, 0, 1, 1)
    core_right = (0, 1, 0, 1)
    core_top = (0, 0, 0, 0)
    core_family = (
        (0, 1, 2, 3),
        core_left,
        core_right,
        core_top,
    )
    _, core_bands, core_strata = band_data(
        core_values, core_family, core_space
    )
    left_character = next(iter(core_strata[core_left]))
    checks.require(
        left_character not in core_bands[core_right],
        "incomparable anchor exclusion",
    )
    records["anchor_order"] = {
        "left_stratum_character": left_character,
        "in_incomparable_band": False,
        "anchor_must_refine_stratum": True,
    }

    return records


def source_gate(repo: Path, checks: Checks) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in SOURCE_HASHES.items():
        digest = file_sha256(repo / relative)
        checks.equal(digest, expected, f"source pin {relative}")
        observed[relative] = digest
    note = (repo / NOTE_PATH).read_text()
    required = [
        "W_{\\pi\\vee\\sigma}=W_\\pi+W_\\sigma",
        "H_{\\pi\\vee\\sigma}=H_\\pi\\cap H_\\sigma",
        "\\mu_{\\mathcal P}",
        "actual live set",
        "One-sided upper bounds",
        "quotient-versus-quotient dual-character overlap only",
        "fresh audit",
        "\\tag{JB31}",
    ]
    for needle in required:
        checks.require(needle in note, f"note guard: {needle}")
    return observed


def build_artifact(repo: Path, checks: Checks) -> dict[str, Any]:
    sources = source_gate(repo, checks)
    census = partition_census_suite(checks)
    diamond = diamond_suite(checks)
    multi_anchor = multi_anchor_suite(checks)
    falsifiers = falsifier_suite(checks)
    artifact: dict[str, Any] = {
        "schema": SCHEMA,
        "status": STATUS,
        "base_commit": BASE_COMMIT,
        "grandparent_commit": GRANDPARENT_COMMIT,
        "parent_commit": PARENT_COMMIT,
        "sources": sources,
        "files": {
            str(NOTE_PATH): file_sha256(repo / NOTE_PATH),
            str(VERIFIER_PATH): file_sha256(repo / VERIFIER_PATH),
        },
        "parent_packet": {
            "commit": PARENT_COMMIT,
            "note_sha256": SOURCE_HASHES[
                "experimental/notes/thresholds/"
                "a4_nonuniform_centered_compiler.md"
            ],
            "verifier_sha256": SOURCE_HASHES[
                "experimental/scripts/"
                "verify_a4_nonuniform_centered_compiler.py"
            ],
            "certificate_sha256": SOURCE_HASHES[
                "experimental/data/certificates/"
                "a4-nonuniform-centered-compiler/"
                "a4_nonuniform_centered_compiler.json"
            ],
            "parent_replay_payload":
                "d9ae52282f690c6ab7c055ded41a44d063e0891f909daf030bc88aff10b2ca67",
            "non_log_files_preserved": True,
        },
        "theorem": {
            "partition_order": "refinement",
            "join": "least_common_coarsening",
            "join_identity": "W_join=W_pi+W_sigma",
            "band_identity": "H_join=H_pi_intersection_H_sigma",
            "same_actual_live_T_required": True,
            "common_effective_dual_required": True,
            "join_closed_family_required": True,
            "deduplicate_kernel_partitions": True,
            "selected_poset_mobius_required": True,
            "trivial_character_excluded": True,
            "exact_projected_cross_energies_required": True,
            "native_partition_energies_mixable": False,
            "one_sided_cumulative_inversion_valid": False,
            "anchor_in_family_required": True,
            "anchor_refines_stratum_required": True,
            "whole_anchor_minimization_required": True,
            "d_star_at_least_two_for_pairwise": True,
            "full_fixed_weight_slice_required": True,
            "cardinality_fallback_supplied": True,
            "chain_shell_specialization": True,
            "nested_restriction_after_dedup": True,
            "census": census,
            "diamond": diamond,
            "multi_anchor": multi_anchor,
            "falsifiers": falsifiers,
        },
        "consumer_audit": {
            "selected_quotient_band_overlap_resolved": True,
            "generic_partition_family_supplied": False,
            "generic_nonnested_live_join_compatibility_supplied": False,
            "selected_union_exhausts_effective_majors": False,
            "complement_payment_supplied": False,
            "closure_entropy_bound_supplied": False,
            "stratum_energy_bounds_supplied": False,
            "subexponential_compiler_sum_supplied": False,
            "other_cell_overlap_assignment_supplied": False,
            "primal_first_match_atlas_supplied": False,
            "support_level_deletion_supported": False,
            "po3_fixed_statistic_without_markers_supported": False,
            "PR564_energy_reclaimed": False,
            "MI_Q_FI_RC_supplied": False,
            "full_MA_closed": False,
            "full_A4_closed": False,
            "deployed_row_closed": False,
            "tex_modified": False,
            "fresh_tex_promotion_audit_required": True,
        },
    }
    artifact["payload_sha256"] = payload_hash(artifact)
    return artifact


def validate_artifact(
    artifact: dict[str, Any], repo: Path, checks: Checks
) -> None:
    checks.equal(artifact["schema"], SCHEMA, "schema")
    checks.equal(artifact["status"], STATUS, "status")
    checks.equal(artifact["base_commit"], BASE_COMMIT, "base commit")
    checks.equal(
        artifact["grandparent_commit"],
        GRANDPARENT_COMMIT,
        "grandparent commit",
    )
    checks.equal(artifact["parent_commit"], PARENT_COMMIT, "parent commit")
    checks.equal(
        artifact["payload_sha256"],
        payload_hash(artifact),
        "payload hash",
    )
    for relative, expected in SOURCE_HASHES.items():
        checks.equal(
            artifact["sources"][relative],
            expected,
            f"stored source {relative}",
        )
        checks.equal(
            file_sha256(repo / relative),
            expected,
            f"live source {relative}",
        )
    for relative, digest in artifact["files"].items():
        checks.equal(
            file_sha256(repo / relative),
            digest,
            f"packet file {relative}",
        )
    parent = artifact["parent_packet"]
    checks.equal(parent["commit"], PARENT_COMMIT, "parent packet commit")
    checks.equal(
        parent["note_sha256"],
        SOURCE_HASHES[
            "experimental/notes/thresholds/"
            "a4_nonuniform_centered_compiler.md"
        ],
        "parent note pin",
    )
    checks.equal(
        parent["verifier_sha256"],
        SOURCE_HASHES[
            "experimental/scripts/verify_a4_nonuniform_centered_compiler.py"
        ],
        "parent verifier pin",
    )
    checks.equal(
        parent["certificate_sha256"],
        SOURCE_HASHES[
            "experimental/data/certificates/"
            "a4-nonuniform-centered-compiler/"
            "a4_nonuniform_centered_compiler.json"
        ],
        "parent certificate pin",
    )
    checks.equal(
        parent["parent_replay_payload"],
        "d9ae52282f690c6ab7c055ded41a44d063e0891f909daf030bc88aff10b2ca67",
        "parent replay payload",
    )
    checks.equal(
        parent["non_log_files_preserved"],
        True,
        "parent preservation",
    )

    theorem = artifact["theorem"]
    expected_theorem = {
        "partition_order": "refinement",
        "join": "least_common_coarsening",
        "join_identity": "W_join=W_pi+W_sigma",
        "band_identity": "H_join=H_pi_intersection_H_sigma",
        "same_actual_live_T_required": True,
        "common_effective_dual_required": True,
        "join_closed_family_required": True,
        "deduplicate_kernel_partitions": True,
        "selected_poset_mobius_required": True,
        "trivial_character_excluded": True,
        "exact_projected_cross_energies_required": True,
        "native_partition_energies_mixable": False,
        "one_sided_cumulative_inversion_valid": False,
        "anchor_in_family_required": True,
        "anchor_refines_stratum_required": True,
        "whole_anchor_minimization_required": True,
        "d_star_at_least_two_for_pairwise": True,
        "full_fixed_weight_slice_required": True,
        "cardinality_fallback_supplied": True,
        "chain_shell_specialization": True,
        "nested_restriction_after_dedup": True,
    }
    for key, expected in expected_theorem.items():
        checks.equal(theorem[key], expected, f"theorem {key}")
    census = theorem["census"]
    checks.equal(census["n4_f2"]["partitions"], 15, "stored Bell n=4")
    checks.equal(census["n5_f2"]["partitions"], 52, "stored Bell n=5")
    checks.equal(
        census["n4_f2"]["join_identity_checks"],
        450,
        "stored n=4 identities",
    )
    checks.equal(
        census["n5_f2"]["join_identity_checks"],
        5408,
        "stored n=5 identities",
    )
    checks.equal(
        census["n4_f3"]["join_identity_checks"],
        450,
        "stored characteristic-three identities",
    )
    diamond = theorem["diamond"]
    checks.equal(
        diamond["band_sizes"],
        [4, 2, 2, 1],
        "stored diamond bands",
    )
    checks.equal(
        diamond["centered_cumulative_sizes"],
        [3, 1, 1, 0],
        "stored diamond cumulative",
    )
    checks.equal(
        diamond["stratum_sizes"],
        [1, 1, 1, 0],
        "stored diamond strata",
    )
    checks.equal(
        diamond["degree_two_coefficients"],
        [-2, -2, -2],
        "stored diamond coefficients",
    )
    checks.equal(
        diamond["left_anchor_pairwise"],
        "1/3",
        "stored diamond pairwise",
    )
    checks.equal(
        diamond["right_anchor_pairwise"],
        "1/3",
        "stored right diamond pairwise",
    )
    checks.equal(
        diamond["degree_two_normalized_loss"],
        "1/3",
        "stored diamond normalized loss",
    )
    checks.equal(
        diamond["chain_shell_sizes"],
        [2, 1, 0],
        "stored chain shells",
    )
    checks.equal(
        diamond["chain_distant_mobius"],
        0,
        "stored distant chain Mobius",
    )
    multi_anchor = theorem["multi_anchor"]
    checks.equal(
        multi_anchor["stratum_characters"],
        [3],
        "stored multi-anchor stratum",
    )
    checks.equal(
        multi_anchor["weight"],
        2,
        "stored multi-anchor weight",
    )
    checks.equal(
        multi_anchor["values"],
        [2, 1, 6, 0, 2],
        "stored multi-anchor values",
    )
    checks.equal(
        multi_anchor["actual_normalized_loss"],
        "0.2",
        "stored multi-anchor actual",
    )
    checks.equal(
        multi_anchor["finer_anchor_compiler"],
        "0.4",
        "stored finer-anchor compiler",
    )
    checks.equal(
        multi_anchor["coarser_anchor_compiler"],
        "1",
        "stored coarser-anchor compiler",
    )
    checks.equal(
        multi_anchor["whole_anchor_minimum"],
        "0.4",
        "stored whole-anchor minimum",
    )
    checks.equal(
        multi_anchor["compositionwise_anchor_mixing_allowed"],
        False,
        "stored no compositionwise mixing",
    )
    falsifiers = theorem["falsifiers"]
    checks.equal(
        falsifiers["ambient_mobius"]["chosen_mu"],
        -1,
        "stored selected Mobius",
    )
    checks.equal(
        falsifiers["ambient_mobius"]["ambient_mu"],
        2,
        "stored ambient Mobius",
    )
    checks.equal(
        falsifiers["ambient_mobius"]["true_stratum"],
        2,
        "stored true Mobius stratum",
    )
    checks.equal(
        falsifiers["ambient_mobius"]["ambient_printed"],
        5,
        "stored ambient Mobius failure",
    )
    checks.equal(
        falsifiers["ambient_mobius"]["ambient_substitution_valid"],
        False,
        "stored ambient Mobius invalid",
    )
    checks.equal(
        falsifiers["missing_join"]["join_closed"],
        False,
        "stored missing join closure",
    )
    checks.equal(
        falsifiers["missing_join"]["nontrivial_intersection"],
        1,
        "stored missing-join intersection",
    )
    checks.equal(
        falsifiers["missing_join"]["nontrivial_union"],
        5,
        "stored missing-join union",
    )
    checks.equal(
        falsifiers["missing_join"]["raw_double_charge"],
        6,
        "stored missing-join charge",
    )
    checks.equal(
        falsifiers["missing_join"]["meet_substitution_valid"],
        False,
        "stored meet invalid",
    )
    checks.equal(
        falsifiers["live_restriction"]["actual_live_join"],
        "1|2",
        "stored actual live join",
    )
    checks.equal(
        falsifiers["live_restriction"]["restricted_full_join"],
        "12",
        "stored restricted full join",
    )
    checks.equal(
        falsifiers["live_restriction"]["restriction_commutes_with_join"],
        False,
        "stored live restriction",
    )
    checks.equal(
        falsifiers["duplicate_bands"]["stratum_sizes"],
        [0, 0, 1],
        "stored duplicate strata",
    )
    checks.equal(
        falsifiers["duplicate_bands"]["band_sizes"],
        [2, 2, 2],
        "stored duplicate bands",
    )
    checks.equal(
        falsifiers["duplicate_bands"]["negative_stratum_created"],
        False,
        "stored no negative stratum",
    )
    checks.equal(
        falsifiers["all_singletons"]["normalized_l1"],
        "1/1",
        "stored D-star-one loss",
    )
    checks.equal(
        falsifiers["all_singletons"]["fake_one_slot_eta"],
        "1/3",
        "stored D-star-one eta",
    )
    checks.equal(
        falsifiers["all_singletons"]["pairwise_theorem_valid"],
        False,
        "stored D-star-one invalid",
    )
    checks.equal(
        falsifiers["all_singletons"]["cardinality_fallback_required"],
        True,
        "stored D-star-one fallback",
    )
    checks.equal(
        falsifiers["closure_entropy"]["generators"],
        3,
        "stored closure generators",
    )
    checks.equal(
        falsifiers["closure_entropy"]["closure_size"],
        8,
        "stored closure size",
    )
    checks.equal(
        falsifiers["closure_entropy"]["subexponential_automatic"],
        False,
        "stored closure nonautomatic",
    )
    checks.equal(
        falsifiers["one_sided_energy"]["exact_cumulative"],
        [3, 1, 1, 0],
        "stored exact cumulative energy",
    )
    checks.equal(
        falsifiers["one_sided_energy"]["valid_upper_bounds"],
        [3, 2, 2, 0],
        "stored one-sided upper bounds",
    )
    checks.equal(
        falsifiers["one_sided_energy"]["naive_signed_result"],
        -1,
        "stored one-sided failure",
    )
    checks.equal(
        falsifiers["one_sided_energy"]["one_sided_inversion_valid"],
        False,
        "stored one-sided inversion invalid",
    )
    checks.equal(
        falsifiers["po3_markers"]["unmarked_pairwise"],
        "1/7",
        "stored PO3 compiler",
    )
    checks.equal(
        falsifiers["po3_markers"]["one_full_fiber_component"],
        "1/3",
        "stored PO3 component",
    )
    checks.equal(
        falsifiers["po3_markers"]["erasing_markers_valid"],
        False,
        "stored PO3 marker requirement",
    )
    checks.equal(
        falsifiers["anchor_order"]["in_incomparable_band"],
        False,
        "stored incomparable anchor exclusion",
    )
    checks.equal(
        falsifiers["anchor_order"]["anchor_must_refine_stratum"],
        True,
        "stored anchor refinement",
    )

    audit = artifact["consumer_audit"]
    expected_audit = {
        "selected_quotient_band_overlap_resolved": True,
        "generic_partition_family_supplied": False,
        "generic_nonnested_live_join_compatibility_supplied": False,
        "selected_union_exhausts_effective_majors": False,
        "complement_payment_supplied": False,
        "closure_entropy_bound_supplied": False,
        "stratum_energy_bounds_supplied": False,
        "subexponential_compiler_sum_supplied": False,
        "other_cell_overlap_assignment_supplied": False,
        "primal_first_match_atlas_supplied": False,
        "support_level_deletion_supported": False,
        "po3_fixed_statistic_without_markers_supported": False,
        "PR564_energy_reclaimed": False,
        "MI_Q_FI_RC_supplied": False,
        "full_MA_closed": False,
        "full_A4_closed": False,
        "deployed_row_closed": False,
        "tex_modified": False,
        "fresh_tex_promotion_audit_required": True,
    }
    for key, expected in expected_audit.items():
        checks.equal(audit[key], expected, f"audit {key}")


def tamper_selftest(
    artifact: dict[str, Any], repo: Path, checks: Checks
) -> int:
    mutations = [
        ("reverse-order", lambda x: x["theorem"].__setitem__(
            "partition_order", "coarsening"
        )),
        ("use-meet", lambda x: x["theorem"].__setitem__(
            "join", "greatest_common_refinement"
        )),
        ("full-domain-join", lambda x: x["theorem"].__setitem__(
            "same_actual_live_T_required", False
        )),
        ("abstract-duals", lambda x: x["theorem"].__setitem__(
            "common_effective_dual_required", False
        )),
        ("omit-join-closure", lambda x: x["theorem"].__setitem__(
            "join_closed_family_required", False
        )),
        ("duplicate-label-maps", lambda x: x["theorem"].__setitem__(
            "deduplicate_kernel_partitions", False
        )),
        ("ambient-mobius", lambda x: x["theorem"].__setitem__(
            "selected_poset_mobius_required", False
        )),
        ("include-trivial", lambda x: x["theorem"].__setitem__(
            "trivial_character_excluded", False
        )),
        ("drop-exact-cross-energy", lambda x: x["theorem"].__setitem__(
            "exact_projected_cross_energies_required", False
        )),
        ("native-energy-mix", lambda x: x["theorem"].__setitem__(
            "native_partition_energies_mixable", True
        )),
        ("one-sided-inversion", lambda x: x["theorem"].__setitem__(
            "one_sided_cumulative_inversion_valid", True
        )),
        ("anchor-outside-family", lambda x: x["theorem"].__setitem__(
            "anchor_in_family_required", False
        )),
        ("incomparable-anchor", lambda x: x["theorem"].__setitem__(
            "anchor_refines_stratum_required", False
        )),
        ("compositionwise-anchors", lambda x: x["theorem"].__setitem__(
            "whole_anchor_minimization_required", False
        )),
        ("allow-D1", lambda x: x["theorem"].__setitem__(
            "d_star_at_least_two_for_pairwise", False
        )),
        ("support-deleted-factorization", lambda x: x["theorem"].__setitem__(
            "full_fixed_weight_slice_required", False
        )),
        ("drop-cardinality-fallback", lambda x: x["theorem"].__setitem__(
            "cardinality_fallback_supplied", False
        )),
        ("skip-restricted-level-dedup", lambda x: x["theorem"].__setitem__(
            "nested_restriction_after_dedup", False
        )),
        ("deny-selected-overlap-result", lambda x: x[
            "consumer_audit"
        ].__setitem__("selected_quotient_band_overlap_resolved", False)),
        ("claim-generic-family", lambda x: x["consumer_audit"].__setitem__(
            "generic_partition_family_supplied", True
        )),
        ("claim-live-join", lambda x: x["consumer_audit"].__setitem__(
            "generic_nonnested_live_join_compatibility_supplied", True
        )),
        ("claim-exhaustion", lambda x: x["consumer_audit"].__setitem__(
            "selected_union_exhausts_effective_majors", True
        )),
        ("claim-complement", lambda x: x["consumer_audit"].__setitem__(
            "complement_payment_supplied", True
        )),
        ("claim-closure-entropy", lambda x: x["consumer_audit"].__setitem__(
            "closure_entropy_bound_supplied", True
        )),
        ("claim-stratum-energy", lambda x: x["consumer_audit"].__setitem__(
            "stratum_energy_bounds_supplied", True
        )),
        ("claim-sum", lambda x: x["consumer_audit"].__setitem__(
            "subexponential_compiler_sum_supplied", True
        )),
        ("claim-other-overlap", lambda x: x["consumer_audit"].__setitem__(
            "other_cell_overlap_assignment_supplied", True
        )),
        ("claim-first-match", lambda x: x["consumer_audit"].__setitem__(
            "primal_first_match_atlas_supplied", True
        )),
        ("claim-support-deletion", lambda x: x["consumer_audit"].__setitem__(
            "support_level_deletion_supported", True
        )),
        ("erase-PO3-markers", lambda x: x["consumer_audit"].__setitem__(
            "po3_fixed_statistic_without_markers_supported", True
        )),
        ("reclaim-PR564", lambda x: x["consumer_audit"].__setitem__(
            "PR564_energy_reclaimed", True
        )),
        ("claim-MI-Q-FI-RC", lambda x: x["consumer_audit"].__setitem__(
            "MI_Q_FI_RC_supplied", True
        )),
        ("claim-MA", lambda x: x["consumer_audit"].__setitem__(
            "full_MA_closed", True
        )),
        ("claim-A4", lambda x: x["consumer_audit"].__setitem__(
            "full_A4_closed", True
        )),
        ("claim-row", lambda x: x["consumer_audit"].__setitem__(
            "deployed_row_closed", True
        )),
        ("claim-TeX", lambda x: x["consumer_audit"].__setitem__(
            "tex_modified", True
        )),
        ("drop-promotion-audit", lambda x: x["consumer_audit"].__setitem__(
            "fresh_tex_promotion_audit_required", False
        )),
        ("wrong-diamond", lambda x: x["theorem"]["diamond"].__setitem__(
            "stratum_sizes", [2, 1, 1, 0]
        )),
        ("wrong-anchor-minimum", lambda x: x["theorem"][
            "multi_anchor"
        ].__setitem__("whole_anchor_minimum", "1")),
        ("wrong-Mobius-number", lambda x: x["theorem"]["falsifiers"][
            "ambient_mobius"
        ].__setitem__("ambient_printed", 2)),
        ("hide-closure-growth", lambda x: x["theorem"]["falsifiers"][
            "closure_entropy"
        ].__setitem__("closure_size", 4)),
        ("parent-not-preserved", lambda x: x["parent_packet"].__setitem__(
            "non_log_files_preserved", False
        )),
    ]
    rejected = 0
    for name, mutation in mutations:
        damaged = copy.deepcopy(artifact)
        mutation(damaged)
        damaged["payload_sha256"] = payload_hash(damaged)
        local = Checks()
        try:
            validate_artifact(damaged, repo, local)
        except (CheckFailure, KeyError, TypeError, ValueError):
            rejected += 1
        else:
            raise CheckFailure(f"tamper accepted: {name}")
        checks.count += local.count
    checks.equal(rejected, len(mutations), "all semantic tampers rejected")
    return rejected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path)
    parser.add_argument(
        "--artifact",
        type=Path,
        default=Path(
            os.environ.get(
                "RS_MCA_A4_JOIN_ARTIFACT",
                str(DEFAULT_ARTIFACT),
            )
        ),
    )
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checks = Checks()
    cap = impose_cap(checks)
    repo = locate_repo(args.repo)
    artifact = build_artifact(repo, checks)
    validate_artifact(artifact, repo, checks)

    artifact_path = args.artifact
    if not artifact_path.is_absolute():
        artifact_path = repo / artifact_path
    if args.write:
        artifact_path.parent.mkdir(parents=True, exist_ok=True)
        artifact_path.write_text(
            json.dumps(artifact, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        checks.require(artifact_path.is_file(), "certificate exists")
        stored = json.loads(artifact_path.read_text())
        validate_artifact(stored, repo, checks)
        checks.equal(
            canonical(stored),
            canonical(artifact),
            "deterministic certificate",
        )
    rejected = 0
    if args.tamper_selftest:
        rejected = tamper_selftest(artifact, repo, checks)

    modes = []
    if args.write:
        modes.append("write")
    if args.check:
        modes.append("check")
    if args.tamper_selftest:
        modes.append(f"tamper={rejected}")
    if not modes:
        modes.append("default")
    print(
        f"RESULT: PASS ({checks.count} checks; mode={','.join(modes)}; "
        f"cap={cap}; payload={artifact['payload_sha256']})"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, KeyError, ValueError, TypeError) as exc:
        print(f"RESULT: FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
