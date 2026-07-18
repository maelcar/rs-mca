#!/usr/bin/env python3
"""Fail-closed arithmetic replay for the fixed-27 quartic local theorem."""

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
S_DEGREE = 63_600
QRES_BOUND = 4 * R - 3 * A
BASE_CAP = QRES_BOUND // 4

SOURCE_HASHES = {
    "experimental/notes/l2/rank16_fixed27_cubic_divisor_conductor.md":
        "f3fdcaa739c6a09ad824a203fcb1c8bdc2f9bded1111bcdc8e458f9089227305",
    "experimental/notes/l2/rank16_fixed27_residual_specialization_curve.md":
        "dc82be9d643ea9df85f843988acbc38149881297369096e869a6d19082faa195",
    "experimental/notes/l2/rank16_fixed_core_quotient_line_obstruction.md":
        "19325c602ae14082f6ef36db312d815552e0f0eefc0787f3a71fd4254af650f7",
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


def ceil_div(top: int, bottom: int) -> int:
    return -(-top // bottom)


def check_sources() -> None:
    base = root()
    for relative, expected in SOURCE_HASHES.items():
        path = base / relative
        require(path.is_file(), f"missing source: {relative}")
        require(sha256(path) == expected, f"source hash mismatch: {relative}")


def support_minima(base_cap: int) -> tuple[int, int, int]:
    preliminary = None
    refined = None
    refined_argmin = None
    for c in range(base_cap + 1):
        r = R - c
        lam = W - c
        first = c + max(ceil_div(7 * r, 3), ceil_div(14 * r - 21 * lam, 3))
        second = c + ceil_div(7 * r - min(2 * r, 6 * lam), 2)
        if preliminary is None or first < preliminary:
            preliminary = first
        if refined is None or second < refined:
            refined = second
            refined_argmin = c
    require(preliminary is not None and refined is not None, "empty minimum")
    require(refined_argmin is not None, "missing argmin")
    return preliminary, refined, refined_argmin


def check_contract(
    p: int,
    n: int,
    b: int,
    a: int,
    d_total: int,
    residual: int,
    w: int,
    quartic_degree: int,
    pair_secant_degree: int,
    repeated_roots: bool,
    zero_roots: bool,
) -> dict[str, int]:
    require(p == P and is_prime(p), "wrong deployed prime")
    require(p - 1 == 127 * 2**24, "wrong p-1 factorization")
    require(n == N == 64 * b, "wrong subgroup/block relation")
    require((b, a, d_total, residual, w) == (B, A, D, R, W), "wrong degrees")
    require(quartic_degree == 4, "wrong quartic degree")
    require(pair_secant_degree == 2, "wrong pair-secant degree")
    require(repeated_roots, "repeated roots dropped")
    require(zero_roots, "zero roots dropped")
    require(4 * b - a == S_DEGREE, "wrong quotient degree")

    qres = 4 * residual - 3 * a
    base_cap = qres // 4
    require(qres == QRES_BOUND == 51_988, "wrong resultant cofactor cap")
    require(base_cap == BASE_CAP == 12_997, "wrong Base cap")
    require(4 * base_cap == qres, "wrong exact Base endpoint")

    preliminary, refined, argmin = support_minima(base_cap)
    require(preliminary == 133_009, "wrong preliminary union floor")
    require(refined == 141_685, "wrong refined arithmetic endpoint")
    require(argmin == 11_545, "wrong refined minimizer")
    c = argmin
    r = residual - c
    lam = w - c
    require((r, lam) == (52_056, 17_352), "wrong endpoint profile")
    require(ceil_div(7 * residual - 5 * w, 2) == 150_361, "wrong low-triple floor")

    descent = ((17_352, 32_768), (8_676, 16_384), (4_338, 8_192), (2_169, 4_096))
    for degree, modulus in descent:
        require(3 * (degree - 1) > modulus - 1, "density descent failed")
    require(descent[-1][0] % 2 == 1, "final descent degree is not odd")

    return {
        "qres": qres,
        "base_cap": base_cap,
        "preliminary": preliminary,
        "refined": refined,
        "argmin": argmin,
        "r": r,
        "lam": lam,
        "low_triple": 150_361,
        "strict_floor": refined + 1,
    }


def run_check() -> str:
    check_sources()
    data = check_contract(P, N, B, A, D, R, W, 4, 2, True, True)
    return "\n".join([
        "R29_FIXED27_QUARTIC_REPEATED_RESULTANT: PASS",
        f"p={P} n={N} B={B} a={A} D={D} d={R} w={W}",
        f"Qres_cap={data['qres']} Base_cap={data['base_cap']}",
        f"preliminary_union={data['preliminary']} refined_endpoint={data['refined']}",
        f"endpoint=c:{data['argmin']},r:{data['r']},lambda:{data['lam']}",
        f"strict_union_floor={data['strict_floor']} low_triple_floor={data['low_triple']}",
        "descent=17352/32768,8676/16384,4338/8192,2169/4096",
        "pair_secant_degree=2 high_triple=Fano_minus_one_Xm",
        "ledger_delta=0 official_score=0/2",
        "RESULT: PASS",
        "",
    ])


def run_tamper() -> str:
    base = [P, N, B, A, D, R, W, 4, 2, True, True]
    cases = [
        ("prime", 0, P - 2),
        ("subgroup", 1, N - 64),
        ("block", 2, B // 2),
        ("a", 3, A + 1),
        ("D", 4, D + 1),
        ("residual", 5, R + 1),
        ("w", 6, W + 1),
        ("quartic", 7, 3),
        ("secant", 8, 3),
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
        "R29_FIXED27_QUARTIC_REPEATED_RESULTANT_TAMPER: PASS\n"
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
