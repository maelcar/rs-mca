#!/usr/bin/env python3
"""Verify the augmented-basis pencil and deep-hole design audit."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


SCHEMA = "rs-mca-augmented-basis-pencil-design-inverse-v1"
THEOREM_ID = "augmented-basis-pencil-design-inverse"
STATUS = "PROVED LINEAR ALGEBRA / AUDITED FINITE FIXTURES"
REPO = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    REPO
    / "experimental/data/certificates/augmented-basis-pencil-design-inverse"
    / "augmented_basis_pencil_design_inverse.json"
)
SOURCE_MARKERS = {
    "experimental/notes/thresholds/all_pair_paving_basis_multiplicity_compiler.md": (
        "### Theorem 2 (deep-hole specialization)",
        "The exact remaining wall is the **deep-hole pencil/design owner dichotomy**",
    ),
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode()


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_binding() -> list[dict[str, Any]]:
    rows = []
    for relative, markers in SOURCE_MARKERS.items():
        path = REPO / relative
        lines = path.read_text().splitlines()
        pins = []
        for marker in markers:
            matches = [(i, line) for i, line in enumerate(lines, 1) if marker in line]
            require(len(matches) == 1, f"source marker is not unique: {marker}")
            line_no, line = matches[0]
            pins.append(
                {
                    "line": line_no,
                    "marker": marker,
                    "line_sha256": hashlib.sha256(line.encode()).hexdigest(),
                }
            )
        rows.append(
            {
                "path": relative,
                "sha256": file_sha256(path),
                "pins": pins,
            }
        )
    return rows


class PrimeField:
    def __init__(self, p: int) -> None:
        self.p = p
        self.q = p
        require(p >= 2, "bad prime")

    def add(self, a: int, b: int) -> int:
        return (a + b) % self.p

    def neg(self, a: int) -> int:
        return (-a) % self.p

    def sub(self, a: int, b: int) -> int:
        return (a - b) % self.p

    def mul(self, a: int, b: int) -> int:
        return (a * b) % self.p

    def pow(self, a: int, exponent: int) -> int:
        return pow(a % self.p, exponent, self.p)

    def inv(self, a: int) -> int:
        require(a % self.p != 0, "division by zero")
        return pow(a, self.p - 2, self.p)

    def from_base(self, a: int) -> int:
        return a % self.p


class QuadraticField:
    """F_(p^2)=F_p[u]/(u^2-2), for p=3 or 5."""

    def __init__(self, p: int) -> None:
        require(p in (3, 5), "the pinned quadratic fixtures use p=3 or p=5")
        require(pow(2, (p - 1) // 2, p) == p - 1, "2 is not a nonsquare")
        self.p = p
        self.q = p * p
        self.nonsquare = 2

    def parts(self, x: int) -> tuple[int, int]:
        return x % self.p, (x // self.p) % self.p

    def encode(self, a: int, b: int) -> int:
        return (a % self.p) + self.p * (b % self.p)

    def add(self, x: int, y: int) -> int:
        a, b = self.parts(x)
        c, d = self.parts(y)
        return self.encode(a + c, b + d)

    def neg(self, x: int) -> int:
        a, b = self.parts(x)
        return self.encode(-a, -b)

    def sub(self, x: int, y: int) -> int:
        return self.add(x, self.neg(y))

    def mul(self, x: int, y: int) -> int:
        a, b = self.parts(x)
        c, d = self.parts(y)
        return self.encode(a * c + self.nonsquare * b * d, a * d + b * c)

    def pow(self, x: int, exponent: int) -> int:
        result = 1
        base = x
        power = exponent
        while power:
            if power & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            power //= 2
        return result

    def inv(self, x: int) -> int:
        require(x != 0, "division by zero")
        return self.pow(x, self.q - 2)

    def from_base(self, a: int) -> int:
        return self.encode(a, 0)


Field = PrimeField | QuadraticField


def dot(field: Field, row: Sequence[int], vector: Sequence[int]) -> int:
    require(len(row) == len(vector), "dot dimension")
    total = 0
    for a, b in zip(row, vector):
        total = field.add(total, field.mul(a, b))
    return total


def matrix_rank(field: Field, rows: Sequence[Sequence[int]]) -> int:
    if not rows:
        return 0
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    matrix = [list(row) for row in rows]
    rank = 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column] != 0),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = field.inv(matrix[rank][column])
        matrix[rank] = [field.mul(scale, value) for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or matrix[index][column] == 0:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(matrix[index], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def solve_square(
    field: Field, matrix: Sequence[Sequence[int]], rhs: Sequence[int]
) -> list[int]:
    n = len(matrix)
    require(len(rhs) == n and all(len(row) == n for row in matrix), "solve shape")
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    pivot_row = 0
    for column in range(n):
        pivot = next(
            (index for index in range(pivot_row, n) if augmented[index][column] != 0),
            None,
        )
        require(pivot is not None, "singular square system")
        augmented[pivot_row], augmented[pivot] = augmented[pivot], augmented[pivot_row]
        scale = field.inv(augmented[pivot_row][column])
        augmented[pivot_row] = [
            field.mul(scale, value) for value in augmented[pivot_row]
        ]
        for index in range(n):
            if index == pivot_row or augmented[index][column] == 0:
                continue
            factor = augmented[index][column]
            augmented[index] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(augmented[index], augmented[pivot_row])
            ]
        pivot_row += 1
    return [augmented[index][-1] for index in range(n)]


def in_column_span(
    field: Field, matrix_rows: Sequence[Sequence[int]], rhs: Sequence[int]
) -> bool:
    require(len(matrix_rows) == len(rhs), "column-span shape")
    base_rank = matrix_rank(field, matrix_rows)
    augmented = [list(row) + [value] for row, value in zip(matrix_rows, rhs)]
    return matrix_rank(field, augmented) == base_rank


def subsets(items: Sequence[int], size: int) -> Iterable[tuple[int, ...]]:
    return itertools.combinations(items, size)


def evaluate_word(
    field: Field,
    b0: Sequence[int],
    b1: Sequence[int],
    grows: Sequence[Sequence[int]],
    gamma: int,
    z: Sequence[int],
) -> list[int]:
    word = []
    for index in range(len(b0)):
        value = field.add(b0[index], field.mul(gamma, b1[index]))
        value = field.add(value, dot(field, grows[index], z))
        word.append(value)
    return word


def pencil_fixture(
    *,
    name: str,
    field: Field,
    points: Sequence[int],
    kappa: int,
    b0_function: Callable[[int], int],
    b1_function: Callable[[int], int],
    minimum_zeros: int,
) -> tuple[dict[str, Any], list[frozenset[int]]]:
    N = len(points)
    indices = list(range(N))
    grows = [
        [field.pow(x, exponent) for exponent in range(kappa)] for x in points
    ]
    b0 = [b0_function(x) for x in points]
    b1 = [b1_function(x) for x in points]
    arows = [
        [b0[index], b1[index]] + grows[index] for index in range(N)
    ]

    basis_sets = {
        frozenset(I)
        for I in subsets(indices, kappa + 1)
        if matrix_rank(field, [arows[index] for index in I]) == kappa + 1
    }
    beta = len(basis_sets)

    deficient = 0
    common_flat = 0
    for I in subsets(indices, kappa + 1):
        rows = [grows[index] for index in I]
        both_in_complement_span = in_column_span(
            field, rows, [b0[index] for index in I]
        ) and in_column_span(field, rows, [b1[index] for index in I])
        is_deficient = frozenset(I) not in basis_sets
        require(
            is_deficient == both_in_complement_span,
            f"{name}: common-flat complement equivalence",
        )
        deficient += int(is_deficient)
        common_flat += int(both_in_complement_span)
    require(
        math.comb(N, kappa + 1) - beta == common_flat == deficient,
        f"{name}: common-flat complement identity",
    )

    core_data: dict[frozenset[int], dict[str, Any]] = {}
    for J_tuple in subsets(indices, kappa):
        J = frozenset(J_tuple)
        matrix = [grows[index] for index in J_tuple]
        z0 = solve_square(field, matrix, [b0[index] for index in J_tuple])
        z1 = solve_square(field, matrix, [b1[index] for index in J_tuple])
        u0 = [
            field.sub(b0[index], dot(field, grows[index], z0))
            for index in indices
        ]
        u1 = [
            field.sub(b1[index], dot(field, grows[index], z1))
            for index in indices
        ]
        common = frozenset(
            index for index in indices if u0[index] == 0 and u1[index] == 0
        )
        require(J <= common, f"{name}: core not in common zeros")
        capacity = N - len(common)
        extensions = {
            index
            for index in indices
            if index not in J and frozenset(set(J) | {index}) in basis_sets
        }
        require(
            extensions == set(indices) - set(common),
            f"{name}: basis-extension/common-zero equivalence",
        )
        require(len(extensions) == capacity, f"{name}: core capacity")
        core_data[J] = {
            "common": common,
            "capacity": capacity,
            "u0": u0,
            "u1": u1,
        }

    require(
        sum(int(data["capacity"]) for data in core_data.values())
        == (kappa + 1) * beta,
        f"{name}: capacity sum",
    )

    pairs = []
    for gamma in range(field.q):
        for z in itertools.product(range(field.q), repeat=kappa):
            word = evaluate_word(field, b0, b1, grows, gamma, z)
            zeros = frozenset(index for index, value in enumerate(word) if value == 0)
            if len(zeros) < minimum_zeros:
                continue
            if matrix_rank(field, [arows[index] for index in zeros]) != kappa + 1:
                continue
            local_bases = sum(1 for basis in basis_sets if basis <= zeros)
            require(local_bases > 0, f"{name}: retained word has no local basis")
            pairs.append(
                {
                    "gamma": gamma,
                    "z": tuple(z),
                    "zeros": zeros,
                    "local_bases": local_bases,
                }
            )

    load_sum = 0
    pencil_rows = []
    for J, data in core_data.items():
        members = [pair for pair in pairs if J <= pair["zeros"]]
        gammas = [int(pair["gamma"]) for pair in members]
        require(len(gammas) == len(set(gammas)), f"{name}: repeated pencil slope")
        moving_sets = [
            set(pair["zeros"]) - set(data["common"]) for pair in members
        ]
        for first, second in itertools.combinations(moving_sets, 2):
            require(first.isdisjoint(second), f"{name}: moving-zero collision")
        load = sum(len(moving) for moving in moving_sets)
        require(load <= int(data["capacity"]), f"{name}: pencil overload")
        load_sum += load
        pencil_rows.append(
            {
                "core": sorted(J),
                "common_zero_count": len(data["common"]),
                "capacity": int(data["capacity"]),
                "pair_count": len(members),
                "load": load,
                "slack": int(data["capacity"]) - load,
            }
        )

    local_basis_sum = sum(int(pair["local_bases"]) for pair in pairs)
    require(
        load_sum == (kappa + 1) * local_basis_sum,
        f"{name}: exact pencil disintegration",
    )
    total_capacity = sum(int(data["capacity"]) for data in core_data.values())
    require(
        total_capacity - load_sum
        == (kappa + 1) * (beta - local_basis_sum),
        f"{name}: exact slack identity",
    )

    return (
        {
            "name": name,
            "field_order": field.q,
            "domain_size": N,
            "kappa": kappa,
            "minimum_zeros": minimum_zeros,
            "augmented_rank": matrix_rank(field, arows),
            "basis_census": beta,
            "all_possible_bases": math.comb(N, kappa + 1),
            "basis_deficiency": deficient,
            "common_flat_complements": common_flat,
            "retained_pairs": len(pairs),
            "local_basis_sum": local_basis_sum,
            "core_capacity_sum": total_capacity,
            "core_load_sum": load_sum,
            "core_slack_sum": total_capacity - load_sum,
            "pencils": pencil_rows,
        },
        [pair["zeros"] for pair in pairs],
    )


def prime_nonmaximal_fixture() -> dict[str, Any]:
    field = PrimeField(7)
    row, _blocks = pencil_fixture(
        name="F7_nonmaximal_common_flat",
        field=field,
        points=list(range(6)),
        kappa=2,
        b0_function=lambda x: field.pow(x, 5),
        b1_function=lambda x: field.pow(x, 3),
        minimum_zeros=3,
    )
    require(row["basis_deficiency"] > 0, "nonmaximal fixture missed deficiency")
    require(row["retained_pairs"] > 0, "nonmaximal fixture missed retained pairs")
    return row


def affine_lines(field: QuadraticField) -> set[frozenset[int]]:
    lines: set[frozenset[int]] = set()
    for anchor in range(field.q):
        for direction in range(1, field.q):
            line = frozenset(
                field.add(anchor, field.mul(field.from_base(s), direction))
                for s in range(field.p)
            )
            require(len(line) == field.p, "affine line size")
            lines.add(line)
    return lines


def affine_line_fixture(p: int) -> dict[str, Any]:
    field = QuadraticField(p)
    q = field.q
    row, blocks = pencil_fixture(
        name=f"F{q}_F{p}_affine_lines",
        field=field,
        points=list(range(q)),
        kappa=1,
        b0_function=lambda x: field.neg(field.pow(x, p)),
        b1_function=lambda x: x,
        minimum_zeros=p,
    )
    canonical_lines = affine_lines(field)
    block_set = set(blocks)
    expected_pairs = q * (q - 1) // (p * (p - 1))
    require(block_set == canonical_lines, "retained blocks are not all affine lines")
    require(len(blocks) == len(block_set), "multiple pairs share one affine line")
    require(len(blocks) == expected_pairs, "affine-line pair count")
    require(row["basis_census"] == math.comb(q, 2), "deep-hole beta not maximal")
    require(row["basis_deficiency"] == 0, "deep-hole beta deficiency")
    require(row["augmented_rank"] == 3, "affine-line augmented rank collapse")
    require(
        row["local_basis_sum"] == row["basis_census"],
        "affine-line PB5 saturation",
    )
    require(
        expected_pairs * math.comb(p, 2) == math.comb(q, 2),
        "affine-line PB5 binomial identity",
    )
    pair_coverage = Counter(
        pair for block in block_set for pair in itertools.combinations(sorted(block), 2)
    )
    require(len(pair_coverage) == math.comb(q, 2), "Steiner pair coverage size")
    require(set(pair_coverage.values()) == {1}, "Steiner pair coverage multiplicity")
    common_core = set(range(q))
    for block in block_set:
        common_core.intersection_update(block)
    require(not common_core, "unexpected global common core")

    slope_counts: Counter[int] = Counter()
    for gamma in range(q):
        for z in range(q):
            word = [
                field.add(
                    field.neg(field.pow(x, p)),
                    field.add(field.mul(gamma, x), z),
                )
                for x in range(q)
            ]
            if sum(value == 0 for value in word) == p:
                slope_counts[gamma] += 1
    require(
        len(slope_counts) == (q - 1) // (p - 1),
        "affine-line direction count",
    )
    require(set(slope_counts.values()) == {q // p}, "affine-line slope multiplicity")

    direction_weights = [
        sum(field.add(x, constant) != 0 for x in range(q))
        for constant in range(q)
    ]
    require(
        set(direction_weights) == {q - 1},
        "deep-hole direction coset does not have constant weight q-1",
    )
    direction_distance = min(direction_weights)

    row.update(
        {
            "characteristic": p,
            "identity_depth": p - 2,
            "direction_distance": direction_distance,
            "direction_coset_weights_checked": len(direction_weights),
            "error_weight": q - p,
            "agreement_size": p,
            "expected_pair_count": expected_pairs,
            "PB5_denominator": math.comb(p, 2),
            "PB5_ratio": math.comb(q, 2) // math.comb(p, 2),
            "Steiner_system": f"S(2,{p},{q})",
            "pair_coverage_multiplicity": 1,
            "slope_count": len(slope_counts),
            "slope_multiplicity": q // p,
            "global_common_core_size": len(common_core),
        }
    )
    return row


def build_certificate() -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "source_binding": source_binding(),
        "common_flat_and_slack_fixture": prime_nonmaximal_fixture(),
        "deep_hole_affine_line_fixtures": [
            affine_line_fixture(3),
            affine_line_fixture(5),
        ],
        "claims": {
            "common_flat_complement_identity": True,
            "core_capacity_identity": True,
            "moving_zero_disjointness": True,
            "exact_pencil_disintegration": True,
            "exact_slack_identity": True,
            "deep_hole_basis_heaviness_is_automatic": True,
            "PB5_equality_is_Steiner_design": True,
            "no_owner_or_target_closure_claimed": True,
        },
    }
    result["payload_sha256"] = payload_sha256(result)
    return result


def verify_certificate(candidate: dict[str, Any]) -> None:
    require(candidate.get("schema") == SCHEMA, "certificate schema")
    require(candidate.get("theorem_id") == THEOREM_ID, "certificate theorem id")
    require(
        candidate.get("payload_sha256") == payload_sha256(candidate),
        "certificate payload hash",
    )
    expected = build_certificate()
    require(candidate == expected, "certificate differs from exact replay")


def tamper_selftest() -> int:
    base = build_certificate()
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda value: value.__setitem__("schema", "tampered"),
        lambda value: value.__setitem__("status", "tampered"),
        lambda value: value["claims"].__setitem__(
            "deep_hole_basis_heaviness_is_automatic", False
        ),
        lambda value: value["common_flat_and_slack_fixture"].__setitem__(
            "basis_deficiency", 0
        ),
        lambda value: value["common_flat_and_slack_fixture"].__setitem__(
            "core_load_sum",
            value["common_flat_and_slack_fixture"]["core_load_sum"] + 1,
        ),
        lambda value: value["deep_hole_affine_line_fixtures"][0].__setitem__(
            "expected_pair_count", 11
        ),
        lambda value: value["deep_hole_affine_line_fixtures"][0].__setitem__(
            "slope_multiplicity", 4
        ),
        lambda value: value["deep_hole_affine_line_fixtures"][1].__setitem__(
            "pair_coverage_multiplicity", 2
        ),
        lambda value: value["source_binding"][0].__setitem__("sha256", "0" * 64),
        lambda value: value.__setitem__("payload_sha256", "f" * 64),
    ]
    rejected = 0
    for mutate in mutations:
        candidate = copy.deepcopy(base)
        mutate(candidate)
        try:
            verify_certificate(candidate)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper rejection count")
    print(f"TAMPER SELFTEST PASS: {rejected}/{len(mutations)} mutations rejected")
    return rejected


def summary(value: dict[str, Any]) -> None:
    common = value["common_flat_and_slack_fixture"]
    print(
        "COMMON-FLAT FIXTURE:",
        f"beta={common['basis_census']}/{common['all_possible_bases']}",
        f"deficiency={common['basis_deficiency']}",
        f"pencil_slack={common['core_slack_sum']}",
    )
    for row in value["deep_hole_affine_line_fixtures"]:
        print(
            "AFFINE-LINE FIXTURE:",
            f"F_{row['field_order']}/F_{row['characteristic']}",
            f"pairs={row['retained_pairs']}",
            f"slopes={row['slope_count']}x{row['slope_multiplicity']}",
            f"beta={row['basis_census']}",
            row["Steiner_system"],
        )
    print("PAYLOAD SHA256:", value["payload_sha256"])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    require(
        sum((args.write, args.check, args.tamper_selftest)) <= 1,
        "choose at most one mode",
    )

    if args.tamper_selftest:
        tamper_selftest()
        return 0

    value = build_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {CERTIFICATE.relative_to(REPO)}")
    elif args.check:
        require(CERTIFICATE.exists(), "certificate does not exist")
        candidate = json.loads(CERTIFICATE.read_text())
        verify_certificate(candidate)
        print(f"CHECKED {CERTIFICATE.relative_to(REPO)}")
    summary(value)
    print("VERIFICATION PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"VERIFICATION FAILED: {exc}", file=sys.stderr)
        raise SystemExit(1)
