#!/usr/bin/env python3
"""Replay the quadratic-exact last-predeep target counterexample.

Standard library only. No network access, subprocess, dependency installation,
or repository writes are performed.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/quadratic-exact-last-predeep-target-counterexample"
CLAIM_PATH = CERT / "claim.json"
SOURCE_PINS = CERT / "source_pins.json"
MANIFEST_PATH = CERT / "manifest.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def ceil_div(x: int, y: int) -> int:
    require(x >= 0 and y > 0, "ceil_div domain")
    return (x + y - 1) // y


def poly_degree(f: int) -> int:
    return f.bit_length() - 1


def poly_mod(f: int, modulus: int) -> int:
    degree = poly_degree(modulus)
    while f and poly_degree(f) >= degree:
        f ^= modulus << (poly_degree(f) - degree)
    return f


def poly_mul_mod(a: int, b: int, modulus: int) -> int:
    degree = poly_degree(modulus)
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & (1 << degree):
            a ^= modulus
    return out


def poly_gcd(a: int, b: int) -> int:
    while b:
        a, b = b, poly_mod(a, b)
    return a


def rabin_irreducible_binary(modulus: int, degree: int) -> bool:
    require(degree == 129, "endpoint degree changed")
    if poly_degree(modulus) != degree or not (modulus & 1):
        return False
    x = 0b10
    value = x
    checkpoints: dict[int, int] = {}
    wanted = {3, 43, 129}
    for exponent in range(1, degree + 1):
        value = poly_mul_mod(value, value, modulus)
        if exponent in wanted:
            checkpoints[exponent] = value
    return (
        checkpoints[129] == x
        and poly_gcd(checkpoints[43] ^ x, modulus) == 1
        and poly_gcd(checkpoints[3] ^ x, modulus) == 1
    )


def check_source_pins() -> tuple[int, int]:
    pins = json.loads(SOURCE_PINS.read_text(encoding="utf-8"))
    require(
        pins["base"] == "9908454995f3f195cfe748f35a1135211609d066",
        "wrong publication base",
    )
    require(
        pins["dependency_origin_commit"]
        == "6f4e918f27a11995d3951f4ebe7546d4add0f345",
        "wrong dependency source floor",
    )
    for relative, expected in pins["files"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing source file: {relative}")
        require(digest(path) == expected, f"source hash drift: {relative}")
    anchors = 0
    for relative, required in pins["required_anchors"].items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for anchor in required:
            require(anchor in text, f"source anchor drift: {relative}: {anchor}")
            anchors += 1
    return len(pins["files"]), anchors


def check_claim(claim: dict[str, object]) -> None:
    require(claim["minimum_s"] == 129, "minimum s drift")
    require(claim["target_denominator_exponent"] == 128, "target drift")
    require(claim["target_frozen_first"] is True, "target chronology drift")
    require(claim["full_challenge_field"] is True, "challenge drift")
    require(claim["domain_is_full_multiplicative_group"] is True, "domain drift")
    require(claim["collision_formula_orientation"] == "source", "pole orientation drift")
    require(claim["reserve_combination"] == "maximum", "reserve combination drift")
    require(claim["exact_support_first_match"] is True, "owner routing drift")
    require(claim["complete_profile_envelope"] is True, "profile envelope dropped")
    require(claim["redundancy_defect"] == 1, "redundancy defect drift")
    require(claim["q_minus_n"] == 1, "domain length drift")
    require(claim["exact_mca_numerator"] == "2^s+1", "numerator drift")
    require(claim["target"] == "2^(2s-128)", "target formula drift")
    require(claim["strict_target_failure"] is True, "strict failure removed")
    require(claim["replacement_exclusion_proved"] is False, "replacement exclusion overclaim")
    require(claim["finite_ledger_delta"] == 0, "finite payment overclaim")
    require(claim["asymptotic_ledger_delta"] == 0, "asymptotic payment overclaim")
    require(claim["grand_mca"] is False, "Grand MCA overclaim")
    require(claim["grand_list"] is False, "Grand List overclaim")
    require(claim["recurrence"] is False, "recurrence overclaim")
    require(claim["official_score"] == "0/2", "official score overclaim")


def check_manifest() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    require(manifest["base"] == "9908454995f3f195cfe748f35a1135211609d066", "manifest base drift")
    require(manifest["status"] == "independently-audited-zero-payment-counterexample", "manifest status drift")
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing manifest file: {relative}")
        require(digest(path) == expected, f"manifest hash drift: {relative}")
    require("no official-score movement" in manifest["nonclaims"], "manifest score nonclaim removed")
    return len(manifest["files"])


def validate_s(s: int, claim: dict[str, object]) -> dict[str, int]:
    require(s >= claim["minimum_s"], "target endpoint")
    r = 1 << s
    q = r * r
    n = q - claim["q_minus_n"]
    R = 3 * r - claim["redundancy_defect"]
    k = n - R
    a = n - r
    target = q // (1 << claim["target_denominator_exponent"])

    require(q == 1 << (2 * s), "square-field size")
    require(n == q - 1, "multiplicative-domain length")
    require(1 <= k < n and k + 1 <= a <= n, "RS parameter range")
    require(0 <= r <= R - 1, "quadratic theorem radius range")
    require(3 * r - R == 1, "not the last-predeep row")
    require(3 * r > R, "row accidentally exact-deep")

    left_margin = a * a - n * (k + r)
    right_margin = r * r - n * (3 * r - R)
    require(left_margin == 1, "left quadratic margin")
    require(right_margin == 1, "right quadratic margin")

    pair_overlap = 2 * a - n
    require(pair_overlap - k == r - 1 > 0, "adjacent-list singleton margin")
    profile_cap = 1
    pole_numerator = profile_cap * (q - n)
    pole_denominator = (q - n) + k * (profile_cap - 1)
    pole_slopes = ceil_div(pole_numerator, pole_denominator)
    profile_floor = ceil_div(q * pole_slopes, q)
    require(profile_floor == 1, "profile floor")

    tangent_floor = min(q, r + 1)
    exact_numerator = tangent_floor
    require(exact_numerator == r + 1, "exact numerator")
    require(max(profile_floor, tangent_floor) == r + 1, "reserve maximum")
    require(target >= 2 * r, "target endpoint comparison")
    require(exact_numerator < target, "strict crossing did not fail")

    require(2 <= r <= n // 2, "support-atlas range")
    atlas_log_bound = r * (1.0 + math.log(n / r))
    require(atlas_log_bound / n < 1e-30, "atlas not subexponential at endpoint")

    return {
        "s": s,
        "r": r,
        "q": q,
        "n": n,
        "R": R,
        "k": k,
        "a": a,
        "numerator": exact_numerator,
        "target": target,
        "left_margin": left_margin,
        "right_margin": right_margin,
        "list_margin": pair_overlap - k,
    }


def expect_rejection(label: str, action) -> str:
    try:
        action()
    except RuntimeError:
        return label
    raise RuntimeError(f"mutation was not rejected: {label}")


def mutations(claim: dict[str, object]) -> list[str]:
    cases: list[tuple[str, str, object]] = [
        ("lower_s", "minimum_s", 128),
        ("target_density", "target_denominator_exponent", 129),
        ("target_after_family", "target_frozen_first", False),
        ("restricted_challenge", "full_challenge_field", False),
        ("wrong_domain", "domain_is_full_multiplicative_group", False),
        ("reciprocal_pole", "collision_formula_orientation", "reciprocal"),
        ("sum_reserves", "reserve_combination", "sum"),
        ("drop_first_match", "exact_support_first_match", False),
        ("drop_profile_envelope", "complete_profile_envelope", False),
        ("exact_deep", "redundancy_defect", 0),
        ("wrong_length", "q_minus_n", 2),
        ("wrong_numerator", "exact_mca_numerator", "2^s"),
        ("claim_replacement", "replacement_exclusion_proved", True),
        ("claim_payment", "finite_ledger_delta", 1),
        ("claim_grand_mca", "grand_mca", True),
        ("claim_recurrence", "recurrence", True),
        ("claim_score", "official_score", "1/2"),
    ]
    rejected = []
    for label, key, value in cases:
        mutated = deepcopy(claim)
        mutated[key] = value
        rejected.append(expect_rejection(label, lambda m=mutated: check_claim(m)))
    return rejected


def main() -> None:
    source_files, source_anchors = check_source_pins()
    claim = json.loads(CLAIM_PATH.read_text(encoding="utf-8"))
    check_claim(claim)
    manifest_files = check_manifest()

    modulus = (1 << 129) | (1 << 5) | 1
    require(rabin_irreducible_binary(modulus, 129), "T^129+T^5+1 reducible")
    r129 = 1 << 129
    require((r129 - 1) % 3 != 0, "quadratic tower polynomial has a root")

    rows = [validate_s(s, claim) for s in range(129, 161)]
    rejected = mutations(claim)

    first = rows[0]
    last = rows[-1]
    print("QUADRATIC_EXACT_LAST_PREDEEP_TARGET_COUNTEREXAMPLE: PASS")
    print(f"source_pins=PASS,files={source_files},anchors={source_anchors}")
    print(f"artifact_manifest=PASS,files={manifest_files}")
    print("claim_guard=PASS,status=independently-audited-zero-payment-counterexample")
    print("endpoint_field=GF(2^129)[Y]/(Y^2+Y+1),irreducibility=PASS")
    print(
        "family=q=2^(2s),n=q-1,R=3*2^s-1,k=n-R,a=n-2^s,"
        "Gamma=GF(q)"
    )
    print("quadratic_margins=left=1,right=1 adjacent_list_cap=1 profile_floor=1")
    print(
        f"s={first['s']} numerator={first['numerator']} target={first['target']} "
        f"list_margin={first['list_margin']}"
    )
    print(
        f"s={last['s']} numerator={last['numerator']} target={last['target']} "
        f"list_margin={last['list_margin']}"
    )
    print("symbolic_result=2^s+1<2^(2s-128),all_s>=129")
    print("occurring_lengths=n=2^(2s)-1 replacement_exclusion=NOT_PROVED")
    print(f"mutations={len(rejected)}/{len(rejected)}:{','.join(rejected)}")
    print("finite_ledger_delta=0 asymptotic_ledger_delta=0 official_score=0/2")
    print("result=PASS")


if __name__ == "__main__":
    main()
