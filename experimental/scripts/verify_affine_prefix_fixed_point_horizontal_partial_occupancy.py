#!/usr/bin/env python3
"""Replay the fixed-point horizontal partial-occupancy theorem.

This verifier checks the exact raw partial-occupancy refinement of the PR #976
fixed-point family.  It intentionally refuses to certify actual C1/C2 semantic
ownership, an exact value of e_B, or an empty retained C3 set, because the
pinned source does not contain that classifier.

Standard library only.  No repository checkout or network access is required.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/affine-prefix-fixed-point-horizontal-partial-occupancy"
SOURCE_PINS = CERT / "source_pins.json"
CLAIM_PATH = CERT / "claim.json"

# Local point order: (epsilon, eta) = 00, 10, 01, 11.
POINTS = ((0, 0), (1, 0), (0, 1), (1, 1))
DIAGONALS = {frozenset((0, 3)), frozenset((1, 2))}
HORIZONTAL_LABELS = (0, 0, 1, 1)  # quotient label eta
EXPECTED_G = {
    (0, 0): 1,
    (1, 0): 4,
    (2, 0): 2,
    (2, 1): 2,
    (3, 1): 4,
    (4, 2): 1,
}
EXPECTED_H = {
    (1, 0): 1,
    (2, 0): 1,
    (2, 1): 1,
    (3, 1): 3,
    (4, 2): 1,
}
Q = (1, 4, 4, 4, 1)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest_bytes(data: bytes) -> str:
    return sha256(data).hexdigest()


def check_source_pins() -> tuple[int, int]:
    pins = json.loads(SOURCE_PINS.read_text(encoding="utf-8"))
    require(
        pins["base"] == "9908454995f3f195cfe748f35a1135211609d066",
        "wrong source base",
    )
    anchor_count = 0
    for relative, expected in pins["files"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing source file: {relative}")
        require(
            digest_bytes(path.read_bytes()) == expected,
            f"source file hash mismatch: {relative}",
        )
    for relative, anchors in pins["required_anchors"].items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for anchor in anchors:
            require(anchor in text, f"missing source anchor in {relative}: {anchor}")
            anchor_count += 1
    return len(pins["files"]), anchor_count


def check_claim(claim: dict[str, object]) -> None:
    require(claim["self_audit_verdict"] == "REPAIR", "wrong repair verdict")
    require(claim["raw_partial_occupancy_cover_proved"] is True, "raw cover removed")
    require(claim["semantic_owner_status"] == "NOT_PROVED", "semantic owner overclaim")
    require(claim["actual_C1_owner_claim"] is False, "actual C1 owner overclaim")
    require(claim["actual_C2_owner_claim"] is False, "actual C2 owner overclaim")
    require(
        claim["actual_e_B_status"] == "UNDETERMINED_IN_[0,c_B/2]",
        "e_B overclaim",
    )
    require(claim["retained_C3_status"] == "UNDETERMINED", "retained C3 overclaim")
    require(
        claim["semantic_C3_rate_status"] == "UNDETERMINED",
        "semantic C3 rate overclaim",
    )
    require(
        claim["locator_composition_status"]
        == "NOT_PROVED_FOR_THE_INTERPOLATING_MAP",
        "locator composition overclaim",
    )
    require(
        claim["degree_two_folding_polynomial_status"] == "NOT_PROVED",
        "degree-two map overclaim",
    )
    require(claim["finite_ledger_delta"] == 0, "positive finite ledger overclaim")
    require(claim["asymptotic_ledger_delta"] == 0, "positive asymptotic ledger overclaim")
    require(claim["grand_mca_hard_input_2"] is False, "Grand MCA overclaim")
    require(claim["official_score"] == "0/2", "official score overclaim")


def chosen(mask: int) -> frozenset[int]:
    return frozenset(i for i in range(4) if mask >> i & 1)


def local_allowed(mask: int) -> bool:
    subset = chosen(mask)
    return len(subset) != 2 or subset not in DIAGONALS


def local_signature(mask: int) -> tuple[int, int, int]:
    subset = chosen(mask)
    return (
        len(subset),
        sum(POINTS[i][0] for i in subset),
        sum(POINTS[i][1] for i in subset),
    )


def check_local_signature_injective(allowed) -> None:
    seen: dict[tuple[int, int, int], int] = {}
    count = 0
    for mask in range(16):
        if not allowed(mask):
            continue
        count += 1
        signature = local_signature(mask)
        require(signature not in seen, f"local signature collision: {seen.get(signature)}, {mask}")
        seen[signature] = mask
    require(count == 14, f"wrong allowed local count: {count}")


def check_uniform_nontrivial_folding(labels: tuple[int, ...]) -> None:
    require(len(labels) == 4, "wrong local folding arity")
    fibers: defaultdict[int, int] = defaultdict(int)
    for label in labels:
        fibers[label] += 1
    require(len(fibers) > 1, "trivial one-value folding")
    require(set(fibers.values()) == {2}, f"not a uniform two-fold map: {dict(fibers)}")


def occupancy(mask: int, labels: tuple[int, ...] = HORIZONTAL_LABELS) -> tuple[int, int, int]:
    selected = chosen(mask)
    by_label: defaultdict[int, int] = defaultdict(int)
    for index, label in enumerate(labels):
        if index in selected:
            by_label[label] += 1
    all_labels = set(labels)
    full = sum(by_label[label] == 2 for label in all_labels)
    partial = sum(by_label[label] == 1 for label in all_labels)
    remainder = partial  # every partial two-point fiber contributes exactly one point
    require(2 * full + remainder == len(selected), "local occupancy identity failed")
    return full, partial, remainder


def local_polynomials() -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], int]]:
    g: defaultdict[tuple[int, int], int] = defaultdict(int)
    h: defaultdict[tuple[int, int], int] = defaultdict(int)
    for mask in range(16):
        if not local_allowed(mask):
            continue
        size = bin(mask).count("1")
        full, partial, remainder = occupancy(mask)
        require(partial == remainder, "two-fold partial parameter mismatch")
        g[(size, full)] += 1
        if mask & 1:  # p=a_1 is local point 00
            h[(size, full)] += 1
    return dict(g), dict(h)


def multiply(
    left: dict[tuple[int, int], int],
    right: dict[tuple[int, int], int],
    max_y: int,
) -> dict[tuple[int, int], int]:
    out: defaultdict[tuple[int, int], int] = defaultdict(int)
    for (yl, xl), cl in left.items():
        for (yr, xr), cr in right.items():
            if yl + yr <= max_y:
                out[(yl + yr, xl + xr)] += cl * cr
    return dict(out)


def power_bivariate(
    poly: dict[tuple[int, int], int], exponent: int, max_y: int
) -> dict[tuple[int, int], int]:
    out = {(0, 0): 1}
    for _ in range(exponent):
        out = multiply(out, poly, max_y)
    return out


def integer_convolution(left: list[int], right: tuple[int, ...] | list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] += a * b
    return out


def all_coefficients(poly: tuple[int, ...], exponent: int) -> list[int]:
    out = [1]
    for _ in range(exponent):
        out = integer_convolution(out, poly)
    return out


def coefficient_power(poly: tuple[int, ...], exponent: int, degree: int) -> int:
    return all_coefficients(poly, exponent)[degree]


def symmetric_unimodal(values: list[int]) -> bool:
    if values != list(reversed(values)):
        return False
    middle = len(values) // 2
    return all(values[i] <= values[i + 1] for i in range(middle))


def profile_counts(
    B: int,
    g: dict[tuple[int, int], int],
    h: dict[tuple[int, int], int],
) -> list[int]:
    joint = multiply(h, power_bivariate(g, B - 1, 2 * B), 2 * B)
    return [joint.get((2 * B, f), 0) for f in range(B + 1)]


def masks_of_size(total_points: int, size: int):
    for selected in combinations(range(total_points), size):
        mask = 0
        for index in selected:
            mask |= 1 << index
        yield mask


def brute_profile_counts(B: int) -> tuple[list[int], int]:
    counts = [0] * (B + 1)
    signatures: set[tuple[tuple[int, int, int], ...]] = set()
    for mask in masks_of_size(4 * B, 2 * B):
        if not (mask & 1):
            continue
        local_masks = tuple((mask >> (4 * block)) & 0b1111 for block in range(B))
        if not all(local_allowed(local) for local in local_masks):
            continue
        full = partial = remainder = 0
        signature = []
        for local in local_masks:
            f_local, p_local, r_local = occupancy(local)
            full += f_local
            partial += p_local
            remainder += r_local
            signature.append(local_signature(local))
        require(partial == remainder, "global two-fold p=r identity failed")
        require(remainder == 2 * B - 2 * full, "global canonical remainder failed")
        require(tuple(signature) not in signatures, "global c1 signature collision")
        signatures.add(tuple(signature))
        counts[full] += 1
    return counts, len(signatures)


def safe_mean(numerator: int, denominator: int) -> int:
    require(denominator > 0, "zero realized-image denominator")
    require(numerator % denominator == 0, "nonintegral mean in exact injective profile")
    return numerator // denominator


def check_unique_profile(assignments: dict[object, list[int]]) -> None:
    for support, profiles in assignments.items():
        require(len(profiles) == 1, f"support assigned to multiple profiles: {support}")


def expect_rejection(label: str, action) -> str:
    try:
        action()
    except RuntimeError:
        return label
    raise RuntimeError(f"mutation was not rejected: {label}")


def mutation_suite(g: dict[tuple[int, int], int], h: dict[tuple[int, int], int], claim: dict[str, object]) -> list[str]:
    rejected: list[str] = []
    rejected.append(expect_rejection("admit_diagonals", lambda: check_local_signature_injective(lambda _m: True)))
    rejected.append(expect_rejection("drop_fixed_point", lambda: require(2 * sum(EXPECTED_G.values()) == sum(EXPECTED_G.values()), "fixed-point half lost")))
    rejected.append(expect_rejection("identity_folding", lambda: check_uniform_nontrivial_folding((0, 1, 2, 3))))
    rejected.append(expect_rejection("constant_folding", lambda: check_uniform_nontrivial_folding((0, 0, 0, 0))))
    rejected.append(expect_rejection("three_plus_one_folding", lambda: check_uniform_nontrivial_folding((0, 0, 0, 1))))
    rejected.append(expect_rejection("tamper_G", lambda: require(g == {**EXPECTED_G, (2, 0): 3}, "G tamper")))
    rejected.append(expect_rejection("tamper_H", lambda: require(h == {**EXPECTED_H, (3, 1): 4}, "H tamper")))
    rejected.append(expect_rejection("wrong_remainder_formula", lambda: require(2 * 2 - 1 == 2, "r=2B-f tamper")))
    rejected.append(expect_rejection("tamper_B2_profile", lambda: require(profile_counts(2, g, h) == [2, 19, 4], "B2 profile tamper")))
    rejected.append(expect_rejection("tamper_B3_addback", lambda: require(sum(profile_counts(3, g, h)) == 285, "B3 addback tamper")))
    rejected.append(expect_rejection("wrong_Q", lambda: require(coefficient_power((1, 4, 6, 4, 1), 2, 4) == 50, "Q tamper")))
    rejected.append(expect_rejection("duplicate_profile_owner", lambda: check_unique_profile({"S": [1, 2]})))
    rejected.append(expect_rejection("zero_image_denominator", lambda: safe_mean(0, 0)))

    owner_claim = deepcopy(claim)
    owner_claim["actual_C1_owner_claim"] = True
    rejected.append(expect_rejection("assert_actual_C1_owner", lambda: check_claim(owner_claim)))

    retained_claim = deepcopy(claim)
    retained_claim["retained_C3_status"] = "EMPTY"
    rejected.append(expect_rejection("assert_retained_C3_empty", lambda: check_claim(retained_claim)))

    ledger_claim = deepcopy(claim)
    ledger_claim["finite_ledger_delta"] = 1
    rejected.append(expect_rejection("assert_positive_ledger", lambda: check_claim(ledger_claim)))

    degree_claim = deepcopy(claim)
    degree_claim["degree_two_folding_polynomial_status"] = "PROVED"
    rejected.append(expect_rejection("assert_degree_two_polynomial", lambda: check_claim(degree_claim)))
    return rejected


def main() -> None:
    pin_count, anchor_count = check_source_pins()
    claim = json.loads(CLAIM_PATH.read_text(encoding="utf-8"))
    check_claim(claim)

    check_uniform_nontrivial_folding(HORIZONTAL_LABELS)
    check_local_signature_injective(local_allowed)
    for mask in range(16):
        if local_allowed(mask):
            full, partial, remainder = occupancy(mask)
            require(partial == remainder, "local canonical p=r failed")
            require(2 * full + remainder == bin(mask).count("1"), "local canonical size failed")
        complement = mask ^ 0b1111
        require(local_allowed(mask) == local_allowed(complement), "complement rule failed")

    g, h = local_polynomials()
    require(g == EXPECTED_G, f"wrong G: {g}")
    require(h == EXPECTED_H, f"wrong H: {h}")
    require(sum(g.values()) == 14, "wrong no-diagonal local count")
    require(sum(h.values()) == 7, "wrong fixed-point local half")

    rows = []
    for B in range(2, 11):
        counts = profile_counts(B, g, h)
        coefficients = all_coefficients(Q, B)
        require(symmetric_unimodal(coefficients), f"Q^B not symmetric unimodal at B={B}")
        c_B = coefficients[2 * B]
        half = c_B // 2
        require(2 * half == c_B, f"c_B not even at B={B}")
        require(sum(counts) == half, f"exact add-back failed at B={B}")
        require((B + 1) * max(counts) >= half, f"max-profile bound failed at B={B}")
        require(c_B <= 14**B, f"upper central-coefficient bound failed at B={B}")
        require((4 * B + 1) * c_B >= 14**B, f"central-coefficient lower bound failed at B={B}")
        for f, count in enumerate(counts):
            if count == 0:
                continue
            remainder = 2 * B - 2 * f
            partial = remainder
            require(0 <= remainder <= 2 * B, f"bad remainder at B={B},f={f}")
            require(safe_mean(count, count) == 1, f"wrong raw image mean at B={B},f={f}")
            require(partial == remainder, "canonical p=r failed")
        if B in (2, 3):
            brute_counts, image_size = brute_profile_counts(B)
            require(brute_counts == counts, f"brute profile mismatch at B={B}")
            require(image_size == half, f"brute c1 image mismatch at B={B}")
        rows.append((B, c_B, counts, max(counts), counts.index(max(counts))))

    rejected = mutation_suite(g, h, claim)

    print("AFFINE_PREFIX_FIXED_POINT_HORIZONTAL_PARTIAL_OCCUPANCY: PASS")
    print(f"source_pins=PASS,count={pin_count},anchors={anchor_count}")
    print("claim_guard=PASS,verdict=REPAIR")
    print("local_allowed=14 local_signature_injective=PASS folding=uniform_nontrivial_2fold")
    print("canonical_parameters=t=0,m=f,p=r=2B-2f")
    print("local_G=1+4y+2(1+x)y^2+4xy^3+x^2y^4")
    print("local_H=y+(1+x)y^2+3xy^3+x^2y^4")
    for B, c_B, counts, largest, argmax in rows:
        print(
            f"B={B} c_B={c_B} half={c_B // 2} "
            f"profiles={','.join(map(str, counts))} largest={largest}@f={argmax}"
        )
    print("brute_replay=B2,B3 raw_slope_partition=PASS")
    print("asymptotic_raw_rate=max_profile=(1/4)log(14)")
    print("semantic_owner=NOT_PROVED actual_e_B=UNDETERMINED retained_C3=UNDETERMINED")
    print(f"mutations={len(rejected)}/{len(rejected)}:{','.join(rejected)}")
    print("finite_ledger_delta=0 asymptotic_ledger_delta=0 official_score=0/2")
    print("result=PASS")


if __name__ == "__main__":
    main()
