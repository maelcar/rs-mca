#!/usr/bin/env python3
"""Replay the deployed Mersenne-31 scalar-descent arithmetic.

This stdlib-only checker verifies the source-pinned parameters, projective
functional counts, strict support-distance incidence inequality, and exact
dyadic threshold. The mathematical incidence proof is in the accompanying
note; this script does not prove either unresolved scalar upper.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isqrt


class VerificationError(RuntimeError):
    """Raised when an always-active certificate check fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def is_prime_64(value: int) -> bool:
    """Deterministic Miller--Rabin for unsigned 64-bit integers."""
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if value % prime == 0:
            return value == prime

    exponent = value - 1
    shift = 0
    while exponent % 2 == 0:
        exponent //= 2
        shift += 1

    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % value == 0:
            continue
        witness = pow(base, exponent, value)
        if witness in (1, value - 1):
            continue
        for _ in range(shift - 1):
            witness = (witness * witness) % value
            if witness == value - 1:
                break
        else:
            return False
    return True


@dataclass(frozen=True)
class Deployment:
    p: int = (1 << 31) - 1
    r: int = 4
    n: int = 1 << 21
    k: int = 1 << 20
    a: int = 1_116_023
    list_size: int = 1 << 24
    target_bits: int = 100
    domain_in_base_field: bool = True


def verify(deployment: Deployment) -> dict[str, int]:
    require(is_prime_64(deployment.p), "p must be prime")
    require(deployment.r >= 1, "extension degree must be positive")
    require(deployment.domain_in_base_field, "evaluation domain must lie in F_p")
    require(deployment.n <= deployment.p, "base field is too small for the domain")
    require(1 <= deployment.k <= deployment.a <= deployment.n, "invalid RS parameters")
    require(deployment.list_size >= 1, "list size must be positive")
    require(deployment.target_bits >= 1, "target exponent must be positive")

    t = deployment.n - deployment.a
    g = deployment.a - deployment.k + 1
    n_r, remainder = divmod(deployment.p**deployment.r - 1, deployment.p - 1)
    require(remainder == 0, "N_r is not integral")
    h_r, remainder = divmod(
        deployment.p ** (deployment.r - 1) - 1, deployment.p - 1
    )
    require(remainder == 0, "H_r is not integral")

    left = deployment.list_size * t * h_r
    right = g * n_r
    require(left < right, "strict scalar-descent incidence inequality failed")

    b_star = deployment.p**deployment.r // (1 << deployment.target_bits)
    require(b_star == (1 << 24) - 1, "unexpected deployed B_star")
    require(deployment.list_size == b_star + 1, "wrong forbidden-list boundary")
    require(isqrt(deployment.p) == 46_340, "unexpected Mersenne-31 square root")

    return {
        "t": t,
        "g": g,
        "N_r": n_r,
        "H_r": h_r,
        "left": left,
        "right": right,
        "margin": right - left,
        "B_star": b_star,
    }


def verify_semantic_mutations(base: Deployment) -> int:
    mutations = (
        replace(base, p=base.p - 2),
        replace(base, r=0),
        replace(base, domain_in_base_field=False),
        replace(base, k=0),
        replace(base, a=base.n + 1),
        replace(base, a=base.k),
        replace(base, list_size=base.list_size - 1),
        replace(base, target_bits=99),
    )
    rejected = 0
    for mutation in mutations:
        try:
            verify(mutation)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "a semantic mutation was not rejected")
    return rejected


def main() -> None:
    base = Deployment()
    result = verify(base)
    rejected = verify_semantic_mutations(base)

    print("certificate_id=m31-scalar-descent-equivalence-v1")
    print("base_commit=9908454995f3f195cfe748f35a1135211609d066")
    print(f"p={base.p}")
    print(f"r={base.r}")
    print(f"n={base.n}")
    print(f"k={base.k}")
    print(f"a={base.a}")
    print(f"L={base.list_size}")
    print(f"t={result['t']}")
    print(f"g={result['g']}")
    print(f"N_r={result['N_r']}")
    print(f"H_r={result['H_r']}")
    print(f"LtH_r={result['left']}")
    print(f"gN_r={result['right']}")
    print(f"strict_margin={result['margin']}")
    print(f"B_star={result['B_star']}")
    print(f"forbidden_size={base.list_size}")
    print("threshold_equivalence=PASS")
    print(f"semantic_mutations={rejected}/{rejected}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
