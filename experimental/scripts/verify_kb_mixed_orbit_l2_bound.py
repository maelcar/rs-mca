#!/usr/bin/env python3
"""Exact mixed-orbit L2-to-L1 bound for the PR #467 KB toy family.

Zero-argument, stdlib-only verifier.  The normal path recomputes the exact
prefix-fiber tables, checks the committed JSON, and runs live tamper tests.
Set KB_MIXED_ORBIT_WRITE_JSON=1 to regenerate the JSON mechanically.
"""

from array import array
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import resource
import sys
import time
from typing import Any, Callable


P = 193
N = 64
M = 30
W = 2
ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3
BOUND_SCALE = 10**18
PACKET = "cap25_v13_kb_mixed_orbit_l2_bound"
DATA_NAME = f"{PACKET}.json"
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR = Path(os.environ.get("KB_MIXED_ORBIT_DATA_DIR", DEFAULT_DATA_DIR))
DATA_PATH = DATA_DIR / DATA_NAME


class CheckFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            raise CheckFailure(label)
        self.passed += 1

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.check(actual == expected, f"{label}: {actual!r} != {expected!r}")


def impose_address_space_cap() -> int:
    requested_gb = float(os.environ.get("KB_MIXED_ORBIT_AS_CAP_GB", "2"))
    if not (0 < requested_gb <= 2):
        raise CheckFailure("KB_MIXED_ORBIT_AS_CAP_GB must lie in (0,2]")
    cap = min(int(requested_gb * 1024**3), ADDRESS_SPACE_CAP_BYTES)
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    if soft > ADDRESS_SPACE_CAP_BYTES:
        raise CheckFailure("RLIMIT_AS exceeds 2 GiB")
    return int(soft)


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def is_prime(value: int) -> bool:
    return value >= 2 and prime_factors(value) == [value]


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // q, p) != 1 for q in factors):
            return candidate
    raise CheckFailure("no primitive root")


def subgroup(p: int, n: int) -> tuple[int, tuple[int, ...]]:
    if not is_prime(p) or (p - 1) % n:
        raise CheckFailure("invalid subgroup parameters")
    generator = primitive_root(p)
    step = pow(generator, (p - 1) // n, p)
    values = tuple(pow(step, index, p) for index in range(n))
    if len(set(values)) != n or pow(step, n, p) != 1:
        raise CheckFailure("subgroup order failure")
    for q in prime_factors(n):
        if pow(step, n // q, p) == 1:
            raise CheckFailure("subgroup step has smaller order")
    return generator, values


def exact_prefix_fibers(p: int, domain: tuple[int, ...], m: int) -> array:
    """Exact counts N(z1,z2) for m-subsets, stored in uint64 cells."""
    size = p * p
    zero = array("Q", [0]) * size
    dp = [array("Q", zero) for _ in range(m + 1)]
    dp[0][0] = 1
    for used, x in enumerate(domain):
        x2 = x * x % p
        permutation = array("I", [0]) * size
        source_index = 0
        for z1 in range(p):
            target_base = ((z1 + x) % p) * p
            for z2 in range(p):
                permutation[source_index] = target_base + ((z2 + x2) % p)
                source_index += 1
        for cardinality in range(min(m, used + 1), 0, -1):
            source = dp[cardinality - 1]
            target = dp[cardinality]
            for index, count in enumerate(source):
                if count:
                    target[permutation[index]] += count
    return dp[m]


def marginal_sums(fibers: array, p: int) -> tuple[list[int], list[int]]:
    first = [0] * p
    second = [0] * p
    for index, count in enumerate(fibers):
        z1, z2 = divmod(index, p)
        first[z1] += count
        second[z2] += count
    return first, second


def fraction_record(value: Fraction) -> dict[str, Any]:
    with localcontext() as context:
        context.prec = 70
        decimal_value = Decimal(value.numerator) / Decimal(value.denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": format(decimal_value, ".18E"),
    }


def fraction_from_record(record: dict[str, Any]) -> Fraction:
    return Fraction(record["numerator"], record["denominator"])


def ceil_sqrt_scaled(value: Fraction, scale: int) -> int:
    target = value.numerator * scale * scale
    denominator = value.denominator
    units = math.isqrt(target // denominator)
    while units * units * denominator < target:
        units += 1
    while units and (units - 1) ** 2 * denominator >= target:
        units -= 1
    return units


def fixed_decimal(units: int, scale: int) -> str:
    digits = len(str(scale)) - 1
    return f"{units // scale}.{units % scale:0{digits}d}"


def permuted_fiber_match(
    base: array, shifted: array, p: int, alpha: int
) -> bool:
    alpha2 = alpha * alpha % p
    for z1 in range(p):
        target_base = (alpha * z1 % p) * p
        source_base = z1 * p
        for z2 in range(p):
            if shifted[target_base + alpha2 * z2 % p] != base[source_base + z2]:
                return False
    return True


def compute_certificate() -> dict[str, Any]:
    generator, domain = subgroup(P, N)
    subset_count = math.comb(N, M)
    if subset_count >= 2**64:
        raise CheckFailure("uint64 fiber cells are not exact")

    fibers = exact_prefix_fibers(P, domain, M)
    first, second = marginal_sums(fibers, P)
    fiber_sum = sum(fibers)
    joint_sum_squares = sum(count * count for count in fibers)
    first_sum_squares = sum(count * count for count in first)
    second_sum_squares = sum(count * count for count in second)

    total_nonzero_energy = P * P * joint_sum_squares - subset_count**2
    linear_nonzero_energy = P * first_sum_squares - subset_count**2
    quadratic_nonzero_energy = P * second_sum_squares - subset_count**2
    mixed_energy = (
        total_nonzero_energy
        - linear_nonzero_energy
        - quadratic_nonzero_energy
    )
    mixed_formula = (
        P * P * joint_sum_squares
        - P * first_sum_squares
        - P * second_sum_squares
        + subset_count**2
    )
    if mixed_energy != mixed_formula or mixed_energy < 0:
        raise CheckFailure("mixed Parseval subtraction failed")

    mixed_modes = (P - 1) ** 2
    if mixed_modes % N:
        raise CheckFailure("mixed modes do not split into full twist orbits")
    mixed_orbits = mixed_modes // N
    mixed_energy_share = Fraction(mixed_energy, total_nonzero_energy)
    mixed_bound_sq = Fraction(mixed_modes * mixed_energy, subset_count**2)
    bound_units = ceil_sqrt_scaled(mixed_bound_sq, BOUND_SCALE)

    representatives = [pow(generator, index, P) for index in range((P - 1) // N)]
    offset_matches = []
    for alpha in representatives:
        shifted_domain = tuple(alpha * x % P for x in domain)
        shifted_fibers = fibers if alpha == 1 else exact_prefix_fibers(P, shifted_domain, M)
        offset_matches.append(permuted_fiber_match(fibers, shifted_fibers, P, alpha))

    return {
        "packet": PACKET,
        "date": "2026-07-10",
        "deployed_reference": {
            "p": 2**31 - 2**24 + 1,
            "n": 2**21,
            "a_plus": 1_116_048,
            "subgroup_index": ((2**31 - 2**24 + 1) - 1) // (2**21),
        },
        "status": {
            "mixed_orbit_bound": "PROVED",
            "toy_replay": "MEASURED",
            "interpretation": "ANALYSIS",
            "deployed_transfer": "OPEN",
        },
        "parameters": {
            "p": P,
            "n": N,
            "m": M,
            "w": W,
            "subgroup_index": (P - 1) // N,
            "primitive_root": generator,
            "coset_representatives": representatives,
            "mixed_modes": mixed_modes,
            "mixed_twist_orbits": mixed_orbits,
            "twist_orbit_size": N,
        },
        "exact": {
            "subset_count": subset_count,
            "fiber_sum": fiber_sum,
            "all_fibers_nonempty": all(count > 0 for count in fibers),
            "fiber_min": min(fibers),
            "fiber_max": max(fibers),
            "joint_sum_squares": joint_sum_squares,
            "first_marginal_sum_squares": first_sum_squares,
            "second_marginal_sum_squares": second_sum_squares,
            "total_nonzero_energy": total_nonzero_energy,
            "linear_nonzero_energy": linear_nonzero_energy,
            "quadratic_nonzero_energy": quadratic_nonzero_energy,
            "mixed_energy": mixed_energy,
            "mixed_energy_share": fraction_record(mixed_energy_share),
            "mixed_l1_over_C_bound_squared": fraction_record(mixed_bound_sq),
            "mixed_l1_over_C_bound_ceiling": {
                "scale": BOUND_SCALE,
                "units": bound_units,
                "decimal": fixed_decimal(bound_units, BOUND_SCALE),
            },
        },
        "coset_check": {
            "distinct_cosets": (P - 1) // N,
            "all_coordinate_permutations_match": all(offset_matches),
            "per_coset_match": offset_matches,
        },
        "claims": {
            "proves_mixed_orbit_l1_bound_for_toy_cosets": True,
            "proves_exact_mixed_l2_energy_for_toy_cosets": True,
            "proves_deployed_mixed_orbit_bound": False,
            "proves_raw_signed_em_inverse": False,
            "proves_masked_transfer": False,
            "is_counterexample": False,
        },
    }


def validate_certificate(
    certificate: dict[str, Any], replay: dict[str, Any] | None, checks: Checks
) -> None:
    checks.equal(certificate["packet"], PACKET, "packet id")
    checks.equal(certificate["status"]["mixed_orbit_bound"], "PROVED", "bound status")
    checks.equal(certificate["status"]["toy_replay"], "MEASURED", "replay status")
    checks.equal(certificate["status"]["interpretation"], "ANALYSIS", "analysis status")
    checks.equal(certificate["status"]["deployed_transfer"], "OPEN", "deployment status")

    deployed = certificate["deployed_reference"]
    checks.equal(deployed["p"], 2**31 - 2**24 + 1, "deployed field")
    checks.equal(deployed["n"], 2**21, "deployed domain")
    checks.equal(deployed["a_plus"], 1_116_048, "deployed agreement")
    checks.equal(deployed["subgroup_index"], 1016, "deployed subgroup index")

    parameters = certificate["parameters"]
    checks.equal(parameters["p"], P, "field")
    checks.equal(parameters["n"], N, "domain size")
    checks.equal(parameters["m"], M, "subset size")
    checks.equal(parameters["w"], W, "prefix depth")
    checks.equal(parameters["subgroup_index"], (P - 1) // N, "subgroup index")
    checks.check(is_prime(P), "field is prime")
    checks.equal(parameters["mixed_modes"], (P - 1) ** 2, "mixed mode count")
    checks.equal(
        parameters["mixed_twist_orbits"] * parameters["twist_orbit_size"],
        parameters["mixed_modes"],
        "mixed orbit partition",
    )
    checks.equal(parameters["twist_orbit_size"], N, "primitive orbit size")

    exact = certificate["exact"]
    subset_count = exact["subset_count"]
    checks.equal(subset_count, math.comb(N, M), "subset count")
    checks.equal(exact["fiber_sum"], subset_count, "fiber sum")
    checks.equal(exact["all_fibers_nonempty"], True, "fiber support")
    checks.check(exact["fiber_min"] <= exact["fiber_max"], "fiber extrema")
    checks.equal(
        exact["total_nonzero_energy"],
        P * P * exact["joint_sum_squares"] - subset_count**2,
        "two-dimensional Parseval",
    )
    checks.equal(
        exact["linear_nonzero_energy"],
        P * exact["first_marginal_sum_squares"] - subset_count**2,
        "linear-axis Parseval",
    )
    checks.equal(
        exact["quadratic_nonzero_energy"],
        P * exact["second_marginal_sum_squares"] - subset_count**2,
        "quadratic-axis Parseval",
    )
    checks.equal(
        exact["mixed_energy"],
        exact["total_nonzero_energy"]
        - exact["linear_nonzero_energy"]
        - exact["quadratic_nonzero_energy"],
        "mixed-axis subtraction",
    )
    checks.check(exact["mixed_energy"] >= 0, "mixed energy nonnegative")

    share = fraction_from_record(exact["mixed_energy_share"])
    checks.equal(
        share,
        Fraction(exact["mixed_energy"], exact["total_nonzero_energy"]),
        "mixed energy share",
    )
    bound_sq = fraction_from_record(exact["mixed_l1_over_C_bound_squared"])
    checks.equal(
        bound_sq,
        Fraction(parameters["mixed_modes"] * exact["mixed_energy"], subset_count**2),
        "Cauchy bound squared",
    )
    ceiling = exact["mixed_l1_over_C_bound_ceiling"]
    checks.equal(ceiling["scale"], BOUND_SCALE, "bound scale")
    checks.equal(ceiling["decimal"], fixed_decimal(ceiling["units"], BOUND_SCALE), "bound decimal")
    target = bound_sq.numerator * BOUND_SCALE * BOUND_SCALE
    checks.check(
        ceiling["units"] ** 2 * bound_sq.denominator >= target,
        "bound ceiling is an upper bound",
    )
    checks.check(
        (ceiling["units"] - 1) ** 2 * bound_sq.denominator < target,
        "bound ceiling is minimal",
    )

    cosets = certificate["coset_check"]
    checks.equal(cosets["distinct_cosets"], (P - 1) // N, "coset count")
    checks.equal(len(cosets["per_coset_match"]), cosets["distinct_cosets"], "coset vector")
    checks.equal(cosets["all_coordinate_permutations_match"], True, "coset invariance")
    checks.check(all(cosets["per_coset_match"]), "every coset permutation")

    claims = certificate["claims"]
    checks.equal(claims["proves_mixed_orbit_l1_bound_for_toy_cosets"], True, "toy theorem")
    checks.equal(claims["proves_exact_mixed_l2_energy_for_toy_cosets"], True, "energy theorem")
    checks.equal(claims["proves_deployed_mixed_orbit_bound"], False, "deployed nonclaim")
    checks.equal(claims["proves_raw_signed_em_inverse"], False, "inverse nonclaim")
    checks.equal(claims["proves_masked_transfer"], False, "mask nonclaim")
    checks.equal(claims["is_counterexample"], False, "counterexample nonclaim")

    if replay is not None:
        checks.equal(certificate, replay, "full exact JSON replay")


def tamper_suite(certificate: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("subset-count", lambda data: data["exact"].__setitem__("subset_count", data["exact"]["subset_count"] + 1)),
        ("joint-energy", lambda data: data["exact"].__setitem__("joint_sum_squares", data["exact"]["joint_sum_squares"] + 1)),
        ("marginal-energy", lambda data: data["exact"].__setitem__("first_marginal_sum_squares", data["exact"]["first_marginal_sum_squares"] + 1)),
        ("mixed-energy", lambda data: data["exact"].__setitem__("mixed_energy", data["exact"]["mixed_energy"] + 1)),
        ("orbit-count", lambda data: data["parameters"].__setitem__("mixed_twist_orbits", data["parameters"]["mixed_twist_orbits"] + 1)),
        ("bound-numerator", lambda data: data["exact"]["mixed_l1_over_C_bound_squared"].__setitem__("numerator", data["exact"]["mixed_l1_over_C_bound_squared"]["numerator"] + 1)),
        ("bound-ceiling", lambda data: data["exact"]["mixed_l1_over_C_bound_ceiling"].__setitem__("units", data["exact"]["mixed_l1_over_C_bound_ceiling"]["units"] - 1)),
        ("deployed-overclaim", lambda data: data["claims"].__setitem__("proves_deployed_mixed_orbit_bound", True)),
        ("status-promotion", lambda data: data["status"].__setitem__("mixed_orbit_bound", "MEASURED")),
        ("coset-invariance", lambda data: data["coset_check"].__setitem__("all_coordinate_permutations_match", False)),
    ]
    caught = 0
    for label, mutation in mutations:
        bad = deepcopy(certificate)
        mutation(bad)
        try:
            validate_certificate(bad, None, Checks())
        except (CheckFailure, KeyError, IndexError, TypeError, ValueError, ZeroDivisionError):
            caught += 1
            print(f"[tamper] CAUGHT {label}")
        else:
            print(f"[tamper] MISSED {label}")
    return caught, len(mutations)


def main() -> None:
    effective_cap = impose_address_space_cap()
    started = time.monotonic()
    replay = compute_certificate()
    elapsed = time.monotonic() - started
    print(f"[cap] RLIMIT_AS={effective_cap} bytes")
    print(f"[compute] exact three-coset replay in {elapsed:.2f}s")

    if os.environ.get("KB_MIXED_ORBIT_WRITE_JSON") == "1":
        checks = Checks()
        validate_certificate(replay, None, checks)
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        print(f"RESULT: GENERATED ({checks.passed}/{checks.total} checks)")
        print(DATA_PATH)
        return

    if not DATA_PATH.exists():
        raise CheckFailure(f"missing data JSON: {DATA_PATH}")
    stored = json.loads(DATA_PATH.read_text())
    checks = Checks()
    validate_certificate(stored, replay, checks)
    caught, total = tamper_suite(stored)
    checks.check(total >= 5, "at least five live tamper tests")
    checks.equal(caught, total, "all live tamper tests caught")

    exact = stored["exact"]
    print(f"mixed L2 share: {exact['mixed_energy_share']['decimal']}")
    print(
        "mixed L1/C upper bound: "
        f"{exact['mixed_l1_over_C_bound_ceiling']['decimal']}"
    )
    print(f"RESULT: PASS ({checks.passed}/{checks.total} checks; tampers {caught}/{total})")


if __name__ == "__main__":
    try:
        main()
    except (CheckFailure, MemoryError, OverflowError) as error:
        print(f"RESULT: FAIL ({error})", file=sys.stderr)
        raise SystemExit(1)
