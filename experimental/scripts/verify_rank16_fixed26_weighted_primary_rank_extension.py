#!/usr/bin/env python3
"""Fail-closed replay for the fixed-26 weighted-primary rank extension."""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


P = 2_130_706_433
N = 2_097_152
B = 32_768
A = 67_472
R = 63_601
DELTA = A - R
D = B - DELTA

SOURCE_HASHES = {
    "experimental/notes/l2/rank16_fixed26_divided_difference_source_compiler.md":
        "e508b1847228475e5a71ab12df15d69d4091e7558a91f53e68261f06c42205ab",
    "experimental/notes/l2/rank16_fixed26_global_spectral_rank_gap.md":
        "4d212b4dd1821cefb3866f67a6303e034be88e7ade3b57bd941aedb93e32dcdb",
    "experimental/notes/l2/rank16_fixed26_polynomial_cross_minor_lift.md":
        "a8828bffa507b56ebc9795d9c2badc904a24df02ecbbd980faef1eafa28b81ea",
    "experimental/notes/l2/rank16_fixed26_spectral_resolvent.md":
        "3c8aaddaa9993cb486d918c62101938f9c7bf4604a852863778f0ccd6886f0cd",
    "experimental/scripts/verify_rank16_fixed26_divided_difference_source_compiler.py":
        "2dd8cd4d2df24510a4faa57d4ad70feda1b4505814233547f06dea7293afc744",
    "experimental/scripts/verify_rank16_fixed26_global_spectral_rank_gap.py":
        "37a26c742f09b271f567c2a000810e15cd904ad7f301ff538679766980e0a53d",
    "experimental/scripts/verify_rank16_fixed26_polynomial_cross_minor_lift.py":
        "1a5bec7dd8aefb8079c7cfa5e9d5b732c57e2365adfa94a8e5e28e12c6d2a86e",
    "experimental/scripts/verify_rank16_fixed26_spectral_resolvent.py":
        "1327c517be7d87050785980b2780bbd99862e6de71e50d188b2a353706336014",
}


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_prime_trial_division(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, math.isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def check_sources() -> None:
    root = repo_root()
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing source: {relative}")
        require(sha256(path) == expected, f"source hash mismatch: {relative}")


def allowed_by_inequality(nu: int, a: int = A, r: int = R) -> bool:
    return all(k * a <= nu * r for k in range(1, min(63, nu - 1) + 1))


def check_contract(
    p: int,
    n: int,
    b: int,
    a: int,
    r: int,
    delta: int,
    d: int,
    normalization: str,
    collapse_last: int,
    edge_required: bool,
) -> dict[str, int]:
    require(p == P and is_prime_trial_division(p), "wrong deployed prime")
    require(p - 1 == 1016 * n, "wrong p-1 factorization")
    require(n == N == 64 * b, "wrong subgroup/block relation")
    require((b, a, r) == (B, A, R), "wrong deployed degrees")
    require(delta == a - r == DELTA, "wrong degree deficit")
    require(d == b - delta == D, "wrong fibre cap")
    require(normalization == "(y-z)/(c_y-c_z)", "reversed normalization")
    require(collapse_last == 63, "wrong collapse horizon")
    require(edge_required, "valid-edge hypothesis dropped")

    excluded = [nu for nu in range(3, a + 1) if not allowed_by_inequality(nu, a, r)]
    require(excluded == list(range(18, 67)), "wrong exact rank exclusion")
    require(allowed_by_inequality(17, a, r), "rank 17 should survive")
    require(not allowed_by_inequality(18, a, r), "rank 18 should fail")
    require(not allowed_by_inequality(65, a, r), "rank 65 should fail")
    require(not allowed_by_inequality(66, a, r), "rank 66 should fail")
    require(allowed_by_inequality(67, a, r), "rank 67 should survive")

    ell = 62 * b - r
    require(ell == 1_968_015, "wrong split-complement degree")
    require(ell - delta == 62 * b - a == 1_964_144, "wrong degree-62 cofactor cap")
    require(63 * b - a == 1_996_912, "wrong degree-63 cofactor cap")

    return {
        "excluded_min": excluded[0],
        "excluded_max": excluded[-1],
        "ell": ell,
        "margin65": 63 * a - 65 * r,
        "margin66": 63 * a - 66 * r,
        "margin67": 67 * r - 63 * a,
    }


def run_check() -> str:
    check_sources()
    data = check_contract(
        P, N, B, A, R, DELTA, D,
        "(y-z)/(c_y-c_z)", 63, True,
    )
    return "\n".join([
        "R29_FIXED26_WEIGHTED_PRIMARY_RANK_EXTENSION: PASS",
        f"p={P} n={N} B={B} a={A} r={R} delta={DELTA} d={D}",
        f"excluded={data['excluded_min']}..{data['excluded_max']} new=65,66 survivors=3..17_or_67..{A}",
        f"margin65={data['margin65']} margin66={data['margin66']} margin67={data['margin67']}",
        f"split_complement_degree={data['ell']} fibre_residual_cap={D}",
        "hypotheses=G64+actual_valid_edge normalization=(y-z)/(c_y-c_z)",
        "ledger_delta=0 official_score=0/2",
        "RESULT: PASS",
        "",
    ])


def run_tamper_selftest() -> str:
    base = [P, N, B, A, R, DELTA, D, "(y-z)/(c_y-c_z)", 63, True]
    cases = [
        ("prime", 0, P - 2),
        ("subgroup", 1, N - 64),
        ("block", 2, B // 2),
        ("a", 3, A + 1),
        ("r", 4, R + 1),
        ("delta", 5, DELTA + 1),
        ("fibre-cap", 6, D + 1),
        ("normalization", 7, "(c_y-c_z)/(y-z)"),
        ("collapse", 8, 62),
        ("valid-edge", 9, False),
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
        "R29_FIXED26_WEIGHTED_PRIMARY_RANK_EXTENSION_TAMPER: PASS\n"
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
            print(run_tamper_selftest(), end="")
    except CheckError as exc:
        print(f"RESULT: FAIL ({exc})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
