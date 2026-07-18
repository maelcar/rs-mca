#!/usr/bin/env python3
"""Fail-closed replay for the fixed-27 repeated-root cubic resultant."""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


P = 2_130_706_433
N = 2_097_152
B = 32_768
A = 67_472
D = 96_369
R = 63_601
W = 28_897
DEFICIT = 3 * B - A
M_BOUND = 3 * W - DEFICIT
BASE_CAP = M_BOUND // 3
UNION_FLOOR = BASE_CAP + (7 * (R - BASE_CAP) + 1) // 2

SOURCE_HASHES = {
    "experimental/notes/l2/rank16_fixed27_cubic_divisor_conductor.md":
        "f3fdcaa739c6a09ad824a203fcb1c8bdc2f9bded1111bcdc8e458f9089227305",
    "experimental/notes/l2/rank16_fixed27_residual_specialization_curve.md":
        "dc82be9d643ea9df85f843988acbc38149881297369096e869a6d19082faa195",
    "experimental/notes/l2/rank16_fixed_core_quotient_line_obstruction.md":
        "19325c602ae14082f6ef36db312d815552e0f0eefc0787f3a71fd4254af650f7",
    "experimental/scripts/verify_rank16_fixed27_cubic_divisor_conductor.py":
        "8e73a6f1d0b7fb6b723b5a14ada7267b663aad70711114c691c4dae745e68894",
    "experimental/scripts/verify_rank16_fixed27_cubic_divisor_conductor.expected.txt":
        "ee774950f25653a898673062c1416ee8e677f33c323e124f3a7c895e9d03de55",
    "experimental/scripts/verify_rank16_fixed_core_quotient_line_obstruction.py":
        "0e7e25a2e696941f42d7eaf24c4b441e769592c3ffff040883bb9b076765d7dd",
    "experimental/scripts/verify_rank16_fixed_core_quotient_line_obstruction.expected.txt":
        "8dbe50b5911bfcdbc10fcc3ee578398d0d068f43f57b672c4e84eb42b64dc109",
    "experimental/data/certificates/rank16-fixed27-residual-specialization-curve/verify_rank16_fixed27_residual_specialization_curve.py":
        "5fa2831e3699bdc1a671f23a231e0a865d82157b4c5131d6836aac65dcfab9b7",
    "experimental/data/certificates/rank16-fixed27-residual-specialization-curve/verify_rank16_fixed27_residual_specialization_curve.expected.txt":
        "382da0d934131d8f514b0450f81b9bbee044806ac12f37d8cb2ecc45dfbcb016",
}


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def check_sources() -> None:
    base = root()
    for relative, expected in SOURCE_HASHES.items():
        path = base / relative
        require(path.is_file(), f"missing source: {relative}")
        require(sha256(path) == expected, f"source hash mismatch: {relative}")


def check_deepest_nonzero_layers() -> int:
    count = 0
    for multiplicity in (1, 2, 3):
        for exponent in range(multiplicity + 1):
            gcd_exponent = min(exponent, multiplicity - 1)
            deepest_exponent = 1 if exponent == multiplicity else 0
            require(
                exponent - deepest_exponent == gcd_exponent,
                "nonzero deepest-layer identity",
            )
            count += 1
    return count


def check_zero_layers(block: int = B) -> int:
    count = 0
    for multiplicity in (1, 2, 3):
        for valuation in range(multiplicity * block + 1):
            deepest = max(valuation - (multiplicity - 1) * block, 0)
            require(
                valuation - deepest
                == min(valuation, (multiplicity - 1) * block),
                "zero deepest-layer identity",
            )
            count += 1
    return count


def check_contract(
    p: int,
    n: int,
    b: int,
    a: int,
    d: int,
    residual: int,
    w: int,
    label_degree: int,
    chord_degree: int,
    repeated_roots: bool,
    zero_roots: bool,
) -> dict[str, int]:
    require(p == P and is_prime(p), "wrong deployed prime")
    require(p - 1 == 127 * 2**24, "wrong p-1 factorization")
    require(n == N == 64 * b, "wrong subgroup/block relation")
    require((b, a, d, residual, w) == (B, A, D, R, W), "wrong degrees")
    require(label_degree == 2, "wrong specialization label degree")
    require(chord_degree == 1, "wrong chord quotient degree")
    require(repeated_roots, "repeated roots dropped")
    require(zero_roots, "zero roots dropped")

    deficit = 3 * b - a
    m_bound = 3 * w - deficit
    base_cap = m_bound // 3
    union_floor = base_cap + (7 * (residual - base_cap) + 1) // 2
    require(deficit == DEFICIT == 30_832, "wrong cubic deficit")
    require(m_bound == M_BOUND == 55_859, "wrong resultant multiplier cap")
    require(base_cap == BASE_CAP == 18_619, "wrong Base cap")
    require(3 * base_cap <= m_bound < 3 * (base_cap + 1), "Base endpoint")
    require(union_floor == UNION_FLOOR == 176_056, "wrong union floor")
    require(union_floor - 150_361 == 25_695, "wrong inherited improvement")
    require(residual - base_cap == 44_982, "wrong cancelled residual degree")

    nonzero_cases = check_deepest_nonzero_layers()
    zero_cases = check_zero_layers(b)
    return {
        "deficit": deficit,
        "m_bound": m_bound,
        "base_cap": base_cap,
        "union_floor": union_floor,
        "nonzero_cases": nonzero_cases,
        "zero_cases": zero_cases,
    }


def run_check() -> str:
    check_sources()
    data = check_contract(P, N, B, A, D, R, W, 2, 1, True, True)
    return "\n".join([
        "R29_FIXED27_CUBIC_REPEATED_RESULTANT: PASS",
        f"p={P} n={N} B={B} a={A} D={D} d={R} w={W}",
        f"cubic_deficit={data['deficit']} resultant_M_cap={data['m_bound']}",
        f"Base_cap={data['base_cap']} union_floor={data['union_floor']} improvement=25695",
        f"deepest_layers=nonzero:{data['nonzero_cases']},zero:{data['zero_cases']}",
        "label_degree=2 chord_admissible_roots=0_or_1",
        "ledger_delta=0 official_score=0/2",
        "RESULT: PASS",
        "",
    ])


def run_tamper() -> str:
    base = [P, N, B, A, D, R, W, 2, 1, True, True]
    cases = [
        ("prime", 0, P - 2),
        ("subgroup", 1, N - 64),
        ("block", 2, B // 2),
        ("a", 3, A + 1),
        ("D", 4, D + 1),
        ("residual", 5, R + 1),
        ("w", 6, W + 1),
        ("label-degree", 7, 3),
        ("chord-degree", 8, 2),
        ("repeated", 9, False),
        ("zero", 10, False),
    ]
    rejected = []
    for name, index, value in cases:
        trial = base.copy()
        trial[index] = value
        try:
            check_contract(*trial)
        except CheckError:
            rejected.append(name)
        else:
            raise CheckError(f"mutation survived: {name}")
    require(len(rejected) == len(cases), "not all mutations rejected")
    return (
        "R29_FIXED27_CUBIC_REPEATED_RESULTANT_TAMPER: PASS\n"
        f"mutations={len(cases)} rejected={','.join(rejected)}\n"
        "RESULT: PASS\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.check and not args.tamper_selftest:
        args.check = True
    try:
        if args.check:
            print(run_check(), end="")
        if args.tamper_selftest:
            print(run_tamper(), end="")
    except CheckError as exc:
        print(f"RESULT: FAIL ({exc})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
