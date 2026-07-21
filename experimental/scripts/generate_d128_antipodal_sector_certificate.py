#!/usr/bin/env python3
"""Generate exact LLL/GSO certificates for the D128 antipodal sectors."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import re
import struct
from collections import defaultdict
from pathlib import Path

import sympy as sp


MOD = 2_147_483_647
BLOCKS = 32
EVEN_RANK = 32
ODD_RANK = 64
EVEN_ENUMERATION_RADIUS = 9
ODD_ENUMERATION_RADIUS = 16
DELTA = sp.Rational(99, 100)
REPO_ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    REPO_ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "d128-blockfree-seven-moment-injectivity"
)


def fp2_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        (left[0] * right[0] - left[1] * right[1]) % MOD,
        (left[0] * right[1] + left[1] * right[0]) % MOD,
    )


def fp2_power(base: tuple[int, int], exponent: int) -> tuple[int, int]:
    answer = (1, 0)
    while exponent:
        if exponent & 1:
            answer = fp2_multiply(answer, base)
        base = fp2_multiply(base, base)
        exponent //= 2
    return answer


def cayley(parameter: int) -> tuple[int, int]:
    inverse = pow(parameter * parameter + 1, MOD - 2, MOD)
    return (
        (parameter * parameter - 1) * inverse % MOD,
        2 * parameter * inverse % MOD,
    )


def chebyshev4(value: int) -> int:
    square = (2 * value * value - 1) % MOD
    return (2 * square * square - 1) % MOD


def domain() -> list[int]:
    eta = fp2_power(cayley(2), 1 << 22)
    assert fp2_power(eta, 512) == (1, 0)
    assert fp2_power(eta, 256) != (1, 0)
    point = eta
    step = fp2_multiply(eta, eta)
    roots = []
    for _ in range(128):
        roots.append(point[0])
        point = fp2_multiply(point, step)
    assert len(set(roots)) == 128
    return sorted(roots)


def sector_coordinates() -> tuple[list[int], list[int]]:
    fibers: dict[int, list[int]] = defaultdict(list)
    for root in domain():
        fibers[chebyshev4(root)].append(root)
    blocks = [sorted(fibers[value]) for value in sorted(fibers)]
    assert len(blocks) == BLOCKS

    representatives: list[int] = []
    deltas: list[int] = []
    for block in blocks:
        pair_representatives = sorted({min(root, (-root) % MOD) for root in block})
        assert len(pair_representatives) == 2
        u, v = pair_representatives
        assert {u, (-u) % MOD, v, (-v) % MOD} == set(block)
        assert (u * u + v * v) % MOD == 1
        delta = (2 * u * u - 1) % MOD
        assert (2 * v * v - 1) % MOD == (-delta) % MOD
        representatives.extend((u, v))
        deltas.append(delta)
    return representatives, deltas


def modular_kernel_basis(forms: list[list[int]]) -> sp.Matrix:
    rows = len(forms)
    columns = len(forms[0])
    matrix = sp.Matrix(forms)
    pivots = None
    for candidate in itertools.combinations(range(columns), rows):
        if int(matrix[:, candidate].det()) % MOD:
            pivots = candidate
            break
    assert pivots is not None
    inverse = matrix[:, pivots].inv_mod(MOD)

    basis: list[list[int]] = []
    for free in range(columns):
        if free in pivots:
            continue
        correction = (-inverse * matrix[:, free]) % MOD
        vector = [0] * columns
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = int(correction[row])
        basis.append(vector)
    for pivot in pivots:
        vector = [0] * columns
        vector[pivot] = MOD
        basis.append(vector)
    answer = sp.Matrix(basis)
    assert abs(int(answer.det())) == MOD**rows
    return answer


def enclosing_binary64(value: sp.Rational) -> tuple[int, int]:
    approximate = float(value)
    exact_approximate = sp.Rational(*approximate.as_integer_ratio())
    lower = approximate
    upper = approximate
    if exact_approximate > value:
        lower = math.nextafter(approximate, -math.inf)
    if exact_approximate < value:
        upper = math.nextafter(approximate, math.inf)
    lower = math.nextafter(lower, -math.inf)
    upper = math.nextafter(upper, math.inf)
    assert sp.Rational(*lower.as_integer_ratio()) <= value
    assert value <= sp.Rational(*upper.as_integer_ratio())
    return (
        struct.unpack("<Q", struct.pack("<d", lower))[0],
        struct.unpack("<Q", struct.pack("<d", upper))[0],
    )


def reduce_and_gso(basis: sp.Matrix) -> tuple[sp.Matrix, list[sp.Rational], list[list[sp.Rational]]]:
    reduced, transform = basis.lll_transform(delta=DELTA)
    assert transform * basis == reduced
    assert abs(int(transform.det())) == 1
    gso, mu = exact_gso(reduced)
    return reduced, gso, mu


def exact_gso(basis: sp.Matrix) -> tuple[list[sp.Rational], list[list[sp.Rational]]]:
    gram = basis * basis.T
    lower, diagonal = gram.LDLdecomposition(hermitian=False)
    assert lower * diagonal * lower.T == gram
    gso = [sp.Rational(diagonal[index, index]) for index in range(basis.rows)]
    mu = [[sp.Rational(0) for _ in range(basis.rows)] for _ in range(basis.rows)]
    for i in range(basis.rows):
        for j in range(i):
            mu[i][j] = sp.Rational(lower[i, j])
    return gso, mu


def read_fplll_basis(path: Path, dimension: int) -> sp.Matrix:
    rows = []
    for line in path.read_text(encoding="ascii").splitlines():
        values = list(map(int, re.findall(r"-?\d+", line)))
        if values:
            rows.append(values)
    assert len(rows) == dimension
    assert all(len(row) == dimension for row in rows)
    return sp.Matrix(rows)


def write_sector(handle, basis: sp.Matrix, gso: list[sp.Rational], mu: list[list[sp.Rational]]) -> None:
    for row in basis.tolist():
        handle.write(" ".join(map(str, row)) + "\n")
    for value in gso:
        handle.write("%d %d\n" % enclosing_binary64(value))
    for i in range(basis.rows):
        for j in range(i):
            handle.write("%d %d\n" % enclosing_binary64(mu[i][j]))


def main() -> None:
    representatives, deltas = sector_coordinates()
    even_basis = modular_kernel_basis([deltas])
    odd_basis = modular_kernel_basis(
        [representatives, [pow(root, 3, MOD) for root in representatives]]
    )
    even_reduced, even_gso, even_mu = reduce_and_gso(even_basis)
    odd_reduced, _, _ = reduce_and_gso(odd_basis)
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    preferred_odd_basis_path = CERT_DIR / "odd_sector_sdb40_basis.txt"
    if preferred_odd_basis_path.exists():
        odd_reduced = read_fplll_basis(preferred_odd_basis_path, ODD_RANK)
        assert abs(int(odd_reduced.det())) == MOD**2
    odd_gso, odd_mu = exact_gso(odd_reduced)

    assert all(sum(deltas[i] * int(row[i]) for i in range(EVEN_RANK)) % MOD == 0 for row in even_reduced.tolist())
    assert all(
        sum(pow(representatives[i], degree, MOD) * int(row[i]) for i in range(ODD_RANK)) % MOD == 0
        for row in odd_reduced.tolist()
        for degree in (1, 3)
    )
    even_norms = [sum(int(value) ** 2 for value in even_reduced.row(i)) for i in range(EVEN_RANK)]
    odd_norms = [sum(int(value) ** 2 for value in odd_reduced.row(i)) for i in range(ODD_RANK)]
    even_witness = list(map(int, even_reduced.row(even_norms.index(min(even_norms)))))
    assert sum(value * value for value in even_witness) == 10
    odd_witness = list(map(int, odd_reduced.row(odd_norms.index(min(odd_norms)))))
    assert sum(value * value for value in odd_witness) == 17

    enumeration_basis_copy_path = CERT_DIR / "odd_sector_enumeration_basis_copy.txt"
    with enumeration_basis_copy_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("[\n")
        for row in odd_reduced.tolist():
            handle.write("[" + " ".join(map(str, row)) + "]\n")
        handle.write("]\n")

    certificate_path = CERT_DIR / "antipodal_sector_lattice_certificate.txt"
    with certificate_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write("D128_ANTIPODAL_SECTOR_CERT_V1\n")
        handle.write(
            f"{MOD} {BLOCKS} {EVEN_RANK} {ODD_RANK} "
            f"{EVEN_ENUMERATION_RADIUS} {ODD_ENUMERATION_RADIUS}\n"
        )
        handle.write(" ".join(map(str, representatives)) + "\n")
        handle.write(" ".join(map(str, deltas)) + "\n")
        handle.write(" ".join(map(str, even_witness)) + "\n")
        handle.write(" ".join(map(str, odd_witness)) + "\n")
        write_sector(handle, even_reduced, even_gso, even_mu)
        write_sector(handle, odd_reduced, odd_gso, odd_mu)

    output = {
        "verdict": "PASS_D128_ANTIPODAL_SECTOR_CERTIFICATE_GENERATION",
        "field": MOD,
        "T4_blocks": BLOCKS,
        "even_sector_rank": EVEN_RANK,
        "even_sector_index": str(MOD),
        "even_enumeration_radius_squared": EVEN_ENUMERATION_RADIUS,
        "even_exhibited_vector_norm_squared": 10,
        "even_exhibited_vector": even_witness,
        "odd_sector_rank": ODD_RANK,
        "odd_sector_index": str(MOD**2),
        "odd_enumeration_radius_squared": ODD_ENUMERATION_RADIUS,
        "odd_reduced_basis_minimum_norm_squared": min(odd_norms),
        "odd_exhibited_vector_norm_squared": 17,
        "odd_exhibited_vector": odd_witness,
        "odd_enumeration_basis_copy_sha256": hashlib.sha256(enumeration_basis_copy_path.read_bytes()).hexdigest(),
        "odd_enumeration_basis": preferred_odd_basis_path.name if preferred_odd_basis_path.exists() else "internal_LLL",
        "odd_enumeration_basis_sha256": hashlib.sha256(preferred_odd_basis_path.read_bytes()).hexdigest() if preferred_odd_basis_path.exists() else hashlib.sha256(enumeration_basis_copy_path.read_bytes()).hexdigest(),
        "certificate_bytes": certificate_path.stat().st_size,
        "certificate_sha256": hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
    }
    output_path = CERT_DIR / "antipodal_sector_generation_output.json"
    with output_path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(json.dumps(output, indent=2) + "\n")
    print(output["verdict"])


if __name__ == "__main__":
    main()
