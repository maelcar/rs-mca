#!/usr/bin/env python3
"""Fail-closed arithmetic replay for the expanded-owner cap-three route cut."""

from __future__ import annotations

import argparse
import hashlib
import math
from pathlib import Path


P = 2_130_706_433
N = 2**21
K = 2**20
M = 1_116_047
B = 2**15
CANDIDATES = 15
SENTINEL = 16

SOURCE_HASHES = {
    "experimental/notes/l2/rank16_global_c0_first_match_ledger.md":
        "d0d0ba41b9d1cd9029b15baa8663a4f7a9b8e3a5c96a6595fd780fa634e003d5",
    "experimental/notes/l2/rank16_global_c0_residual_payment.md":
        "16bdaceaad6d3b9492918868cb1e9c220475a7a71ff1e75f76ecb7d88ad49f08",
    "experimental/notes/l2/rank16_integer_subcore_owner.md":
        "9592188c71c1ed1c9420bd99aca75f4f5ac42f484dcff24b423a5a148185ae3c",
    "experimental/notes/l2/rank16_fixed_core_global_owner_counterexample.md":
        "a7f5421dc7bdcb83e3669c8c4b2db2082123e5b93881058fee9cfe6756599dd3",
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
    limit = math.isqrt(value)
    divisor = 3
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def check_sources() -> None:
    root = repo_root()
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing source: {relative}")
        require(sha256(path) == expected, f"source hash mismatch: {relative}")


def check_configuration(
    alpha: list[int],
    widths: list[int],
    candidate_count: int,
    sentinel: int,
    profile: tuple[int, int, int, int, int, int],
    f64: int,
) -> dict[str, int]:
    require(len(alpha) == 64 and len(widths) == 64, "wrong block count")
    require(alpha == [16_383] + [16_384] * 63, "wrong core block counts")
    require(widths == [1_055] * 16 + [1_054] * 48, "wrong petal widths")
    require(candidate_count == CANDIDATES, "wrong candidate count")
    require(sentinel == SENTINEL, "wrong remainder scalar")
    require(0 < candidate_count < sentinel < P, "scalar collision")
    require(profile == (0, 0, 0, 0, 0, 0), "wrong agreement profile")
    require(f64 == 0, "wrong complete-error count")

    core = sum(alpha)
    petal = sum(widths)
    endpoint = max(a + candidate_count * width for a, width in zip(alpha, widths))
    remainder = N - core - candidate_count * petal
    require(core == K - 1, "wrong core size")
    require(petal == M - K + 1 == 67_472, "wrong petal size")
    require(endpoint == 32_209 and endpoint < B, "petal endpoint overflow")
    require(remainder == 36_497 > 0, "wrong remainder size")
    require(N - core - (candidate_count + 1) * petal < 0, "sixteenth petal fits")
    require(core + petal == M, "wrong agreement count")
    require(core == K - 1, "wrong pairwise intersection")

    e15, e16, _, _, _, _ = profile
    owners = {
        "D": e15 in (33, 34) or (e15 <= 32 and e16 == 16),
        "Q110": e15 == 32,
        "M": f64 in (28, 29),
        "Q41": e15 == 32,
        "X175": f64 == 28,
        "J48": f64 in (26, 27),
        "integer_subcore": e15 == 31 and f64 in (26, 27),
    }
    require(not any(owners.values()), "candidate entered expanded owner")

    return {
        "core": core,
        "petal": petal,
        "endpoint": endpoint,
        "remainder": remainder,
        "agreement": core + petal,
        "intersection": core,
    }


def run_main_check() -> str:
    require(is_prime_trial_division(P), "p is not prime")
    require(P - 1 == 1016 * N, "wrong factorization of p-1")
    omega = pow(3, 1016, P)
    require(pow(omega, N, P) == 1, "omega^n != 1")
    require(pow(omega, N // 2, P) != 1, "omega has smaller order")
    zeta = pow(omega, B, P)
    require(pow(zeta, 64, P) == 1, "zeta^64 != 1")
    require(pow(zeta, 32, P) != 1, "zeta has smaller order")

    check_sources()
    data = check_configuration(
        [16_383] + [16_384] * 63,
        [1_055] * 16 + [1_054] * 48,
        CANDIDATES,
        SENTINEL,
        (0, 0, 0, 0, 0, 0),
        0,
    )

    bstar = P**6 // 2**128
    target = (((bstar + 1) * (P - (N - M))) - 1) // P
    require(bstar == 274_980_728_111_395_087, "wrong Bstar")
    require(target == 274_854_110_496_187_592, "wrong target")
    require(target - 3 == 274_854_110_496_187_589, "wrong owner subtotal")
    require(CANDIDATES > 3, "counterexample does not cross cap three")

    lines = [
        "R29_EXPANDED_OWNER_CAP3_COUNTEREXAMPLE: PASS",
        f"p={P} n={N} K={K} m={M} B={B}",
        f"omega={omega} zeta={zeta} order_omega={N} order_zeta=64",
        f"core={data['core']} petal={data['petal']} endpoint={data['endpoint']} remainder={data['remainder']}",
        f"candidates={CANDIDATES} exact_agreements={data['agreement']} pair_intersection={data['intersection']}",
        "profile=(0,0,0,0,0,0) f64=0 expanded_owner_memberships=none",
        f"owner_paid={target - 3} target={target} complement_lower={CANDIDATES}",
        "ledger_delta=0 official_score=0/2",
        "RESULT: PASS",
    ]
    return "\n".join(lines) + "\n"


def run_tamper_selftest() -> str:
    base_alpha = [16_383] + [16_384] * 63
    base_widths = [1_055] * 16 + [1_054] * 48
    cases = []

    alpha = base_alpha.copy()
    alpha[0] += 1
    cases.append(("core-size", alpha, base_widths, 15, 16, (0, 0, 0, 0, 0, 0), 0))
    widths = base_widths.copy()
    widths[0] += 1
    cases.append(("petal-size", base_alpha, widths, 15, 16, (0, 0, 0, 0, 0, 0), 0))
    cases.append(("candidate-count", base_alpha, base_widths, 16, 17, (0, 0, 0, 0, 0, 0), 0))
    cases.append(("remainder-scalar", base_alpha, base_widths, 15, 15, (0, 0, 0, 0, 0, 0), 0))
    cases.append(("Q-owner", base_alpha, base_widths, 15, 16, (32, 0, 0, 0, 0, 0), 0))
    cases.append(("M-owner", base_alpha, base_widths, 15, 16, (0, 0, 0, 0, 0, 0), 28))
    cases.append(("J-owner", base_alpha, base_widths, 15, 16, (0, 0, 0, 0, 0, 0), 27))
    cases.append(("subcore-owner", base_alpha, base_widths, 15, 16, (31, 0, 0, 0, 0, 0), 26))

    rejected = []
    for name, alpha, widths, count, sentinel, profile, f64 in cases:
        try:
            check_configuration(alpha, widths, count, sentinel, profile, f64)
        except CheckError:
            rejected.append(name)
        else:
            raise CheckError(f"mutation survived: {name}")
    require(len(rejected) == len(cases), "not all mutations rejected")
    return (
        "R29_EXPANDED_OWNER_CAP3_COUNTEREXAMPLE_TAMPER: PASS\n"
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
            print(run_main_check(), end="")
        if args.tamper_selftest:
            print(run_tamper_selftest(), end="")
    except CheckError as exc:
        print(f"RESULT: FAIL ({exc})")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
