#!/usr/bin/env python3
"""Replay the R31 Role 04 fixed-27 cubic source-projection theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from math import comb, isqrt
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = (
    ROOT
    / "experimental/notes/l2/rank16_fixed27_cubic_source_projection_point.md"
)
EXPECTED_PATH = Path(__file__).with_suffix(".expected.txt")
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "rank16-fixed27-cubic-source-projection-point"
)
MANIFEST_PATH = CERT_DIR / "source_manifest.json"
SHA_SUMS_PATH = CERT_DIR / "SHA256SUMS.txt"

ORIGIN_MAIN = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
PR892_HEAD = "d4a33c87ac3e3e1a5078b88fddf085cb6536b75e"
PR904_HEAD = "213c4ebdebf28c0bd92aa47f293f0138b034037b"
MANIFEST_SHA256 = "e26cc973ff4ae0162150d79673ed1c83622ab4772040bf38aa293f5d79f9d1b2"

P = 2_130_706_433
H_ORDER = 2_097_152
B = 32_768
D = 63_601
W = 28_897

ROOT_CHARGES = {
    (18_619, 1): 758_711_395,
    (18_619, 2): 189_669_415,
    (18_618, 1): 758_711_395,
}

EXPECTED_CONTRACT: dict[str, Any] = {
    "origin_main": ORIGIN_MAIN,
    "pr892_head": PR892_HEAD,
    "pr904_head": PR904_HEAD,
    "source": "one_literal_fixed27_affine_rank2_cubic_source_cell",
    "field_prime": P,
    "subgroup_order": H_ORDER,
    "block_size": B,
    "residual_degree": D,
    "width_degree": W,
    "function_field_identity": "L1(F)=X^B*L0(F)",
    "multiplicity_identity": "mult_Pstar(C)=(r-B)/k",
    "root_charges": dict(ROOT_CHARGES),
    "floor_c18619": 246_937,
    "floor_c18618": 246_938,
    "next_delta_c18619": 1_470,
    "next_delta_c18618": 2_392,
    "local_parent_charge": 0,
    "global_ledger_charge": 0,
    "official_score": "0/2",
}

PACKAGE_PATHS = {
    "experimental/notes/l2/rank16_fixed27_cubic_source_projection_point.md",
    "experimental/scripts/verify_rank16_fixed27_cubic_source_projection_point.py",
    "experimental/scripts/verify_rank16_fixed27_cubic_source_projection_point.expected.txt",
    "experimental/data/certificates/"
    "rank16-fixed27-cubic-source-projection-point/source_manifest.json",
}


class CheckError(RuntimeError):
    """A fail-closed replay check failed."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise CheckError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_strict(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"missing JSON file: {path}")
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicate_object
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CheckError(f"cannot parse JSON file {path}: {exc}") from exc
    require(type(value) is dict, f"top-level JSON object required: {path}")
    return value


def path_value(value: Any, *keys: Any) -> Any:
    current = value
    try:
        for key in keys:
            current = current[key]
    except (KeyError, IndexError, TypeError) as exc:
        joined = ".".join(str(key) for key in keys)
        raise CheckError(f"missing contract path: {joined}") from exc
    return current


def exact(value: Any, expected: Any, label: str) -> None:
    require(
        type(value) is type(expected) and value == expected,
        f"{label}: expected {expected!r}, got {value!r}",
    )


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    limit = isqrt(n)
    while divisor <= limit:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def balanced_pair_charge(total: int) -> int:
    require(type(total) is int and total >= 0, "invalid pair multiplicity total")
    q, s = divmod(total, 21)
    return 21 * comb(q, 2) + s * q


def genus_row(c: int, k: int, union_size: int) -> dict[str, int]:
    for value, label in ((c, "c"), (k, "k"), (union_size, "union_size")):
        require(type(value) is int, f"{label} must be an exact integer")
    require((c, k) in ROOT_CHARGES, f"unsupported branch: {(c, k)}")
    require(k > 0, "map degree must be positive")

    r = D - c
    require(r % k == 0, "map degree does not divide r")
    require(B % k == 0, "map degree does not divide B")
    require((r - B) % k == 0, "source-point multiplicity is nonintegral")

    m = r // k
    occupancy = 7 * D - 6 * c - union_size
    require(occupancy >= 0, "negative occupancy total")
    require(occupancy % k == 0, "descended occupancy total is nonintegral")
    pair_total = occupancy // k

    pair_charge = balanced_pair_charge(pair_total)
    root_charge = ROOT_CHARGES[c, k]
    multiplicity = (r - B) // k
    star_charge = comb(multiplicity, 2)
    arithmetic_genus = comb(m - 1, 2)
    existing_excess = pair_charge + root_charge - arithmetic_genus
    strengthened_excess = existing_excess + star_charge

    return {
        "c": c,
        "k": k,
        "U": union_size,
        "r": r,
        "m": m,
        "E": occupancy,
        "N": pair_total,
        "D_pair": pair_charge,
        "D_root": root_charge,
        "mult": multiplicity,
        "D_star": star_charge,
        "pa": arithmetic_genus,
        "existing_excess": existing_excess,
        "excess": strengthened_excess,
    }


def verify_contract(contract: dict[str, Any]) -> None:
    exact(set(contract), set(EXPECTED_CONTRACT), "contract keys")
    for key, expected in EXPECTED_CONTRACT.items():
        exact(contract[key], expected, f"contract.{key}")


def verify_manifest() -> dict[str, Any]:
    require(
        sha256_file(MANIFEST_PATH) == MANIFEST_SHA256,
        "source manifest hash mismatch",
    )
    manifest = load_json_strict(MANIFEST_PATH)

    exact(
        path_value(manifest, "schema"),
        "rs-mca.r31-role04-cubic-source-projection-point.v1",
        "manifest.schema",
    )
    exact(path_value(manifest, "base", "commit"), ORIGIN_MAIN, "manifest base")
    exact(path_value(manifest, "dependencies", 0, "number"), 892, "PR #892")
    exact(
        path_value(manifest, "dependencies", 0, "head"),
        PR892_HEAD,
        "PR #892 head",
    )
    exact(path_value(manifest, "dependencies", 1, "number"), 904, "PR #904")
    exact(
        path_value(manifest, "dependencies", 1, "head"),
        PR904_HEAD,
        "PR #904 head",
    )
    exact(
        path_value(manifest, "contract", "function_field_identity"),
        EXPECTED_CONTRACT["function_field_identity"],
        "function-field identity",
    )
    exact(
        path_value(manifest, "contract", "multiplicity_identity"),
        EXPECTED_CONTRACT["multiplicity_identity"],
        "multiplicity identity",
    )
    exact(
        path_value(manifest, "contract", "official_score"),
        "0/2",
        "manifest official score",
    )
    for key, value in path_value(manifest, "nonclaims").items():
        exact(value, False, f"manifest.nonclaims.{key}")

    pin_path = ROOT / path_value(manifest, "integrated_replay_pin", "path")
    pin_sha = path_value(manifest, "integrated_replay_pin", "sha256")
    require(pin_path.is_file(), f"missing integrated replay pin: {pin_path}")
    exact(sha256_file(pin_path), pin_sha, "integrated replay pin hash")
    return manifest


def verify_note() -> None:
    require(NOTE_PATH.is_file(), f"missing theorem note: {NOTE_PATH}")
    text = NOTE_PATH.read_text(encoding="utf-8")
    markers = (
        "L_1(F) = X^B L_0(F)",
        "mult_(P_*) C = (r-B)/k",
        "c = 18,619  =>  |U| >= 246,937",
        "c = 18,618  =>  |U| >= 246,938",
        "next exact delta requirement is therefore `1,470`",
        "official score remains `0/2`",
    )
    for marker in markers:
        require(marker in text, f"theorem-note marker missing: {marker}")


def verify_sha_sums() -> None:
    require(SHA_SUMS_PATH.is_file(), f"missing package hashes: {SHA_SUMS_PATH}")
    lines = SHA_SUMS_PATH.read_text(encoding="ascii").splitlines()
    parsed: dict[str, str] = {}
    pattern = re.compile(r"^([0-9a-f]{64})  ([A-Za-z0-9_./-]+)$")
    for line in lines:
        match = pattern.fullmatch(line)
        require(match is not None, f"malformed SHA256SUMS line: {line!r}")
        digest, rel_path = match.groups()
        require(rel_path not in parsed, f"duplicate SHA256SUMS path: {rel_path}")
        parsed[rel_path] = digest
    exact(set(parsed), PACKAGE_PATHS, "SHA256SUMS path set")
    for rel_path, digest in parsed.items():
        path = ROOT / rel_path
        require(path.is_file(), f"missing hashed package file: {rel_path}")
        exact(sha256_file(path), digest, f"SHA256SUMS hash for {rel_path}")


def verify_arithmetic() -> None:
    require(is_prime(P), "field modulus is not prime")
    exact(P, 127 * 2**24 + 1, "field decomposition")
    require((P - 1) % H_ORDER == 0, "subgroup order does not divide p-1")
    exact(H_ORDER, 2**21, "deployed subgroup order")
    exact(B, 2**15, "deployed block size")
    exact(D - B, 30_833, "post-block residual degree")
    exact(96_369 - 67_472, W, "width degree")

    endpoint = genus_row(18_619, 2, 230_415)
    endpoint_expected = {
        "r": 44_982,
        "m": 22_491,
        "E": 103_078,
        "N": 51_539,
        "D_pair": 63_218_721,
        "D_root": 189_669_415,
        "mult": 6_107,
        "D_star": 18_644_671,
        "pa": 252_888_805,
        "existing_excess": -669,
        "excess": 18_644_002,
    }
    for key, expected in endpoint_expected.items():
        exact(endpoint[key], expected, f"endpoint.{key}")

    interval_checks = (
        (18_619, 1, 246_939, 10_278, 22_490, 12_214, 74_584_791),
        (18_619, 2, 246_935, 5_139, 11_245, 6_107, 18_644_671),
        (18_618, 1, 246_937, 10_279, 22_489, 12_215, 74_597_005),
    )
    for c, k, union_size, pair_cap, root_floor, mult, delta in interval_checks:
        row = genus_row(c, k, union_size)
        exact(row["mult"], mult, f"multiplicity for {(c, k)}")
        require(pair_cap < mult < root_floor, f"point collision at {(c, k)}")
        exact(row["D_star"], delta, f"source-point delta for {(c, k)}")

    boundary_checks = (
        (18_619, 1, 246_939, 1_529),
        (18_619, 1, 246_940, -2_592),
        (18_619, 2, 246_935, 591),
        (18_619, 2, 246_937, -1_469),
        (18_618, 1, 246_937, 1_730),
        (18_618, 1, 246_938, -2_391),
    )
    for c, k, union_size, expected_excess in boundary_checks:
        exact(
            genus_row(c, k, union_size)["excess"],
            expected_excess,
            f"boundary excess for {(c, k, union_size)}",
        )

    require(
        (7 * D - 6 * 18_619 - 246_936) % 2 == 1,
        "the parity-skipped row unexpectedly descends",
    )
    exact(1_469 + 1, 1_470, "c=18,619 next delta")
    exact(2_391 + 1, 2_392, "c=18,618 next delta")


def mutation_selftest() -> int:
    mutations = (
        ("field prime", "field_prime", P - 2),
        ("block size", "block_size", B - 1),
        ("PR #892 head", "pr892_head", "0" * 40),
        ("root charge", "root_charges", {(18_619, 2): 189_669_414}),
        ("multiplicity identity", "multiplicity_identity", "mult=(r-B)"),
        ("official score", "official_score", "1/2"),
    )
    caught = 0
    for label, key, replacement in mutations:
        candidate = copy.deepcopy(EXPECTED_CONTRACT)
        candidate[key] = replacement
        try:
            verify_contract(candidate)
        except CheckError:
            caught += 1
        else:
            raise CheckError(f"semantic mutation survived: {label}")
    exact(caught, len(mutations), "mutation catch count")
    return caught


def render_report() -> str:
    endpoint = genus_row(18_619, 2, 230_415)
    c19k1_last = genus_row(18_619, 1, 246_939)
    c19k1_next = genus_row(18_619, 1, 246_940)
    c19k2_last = genus_row(18_619, 2, 246_935)
    c19k2_next = genus_row(18_619, 2, 246_937)
    c18k1_last = genus_row(18_618, 1, 246_937)
    c18k1_next = genus_row(18_618, 1, 246_938)
    caught = mutation_selftest()

    lines = [
        "R31_ROLE04_CUBIC_SOURCE_PROJECTION_POINT: PASS",
        f"origin_main={ORIGIN_MAIN}",
        f"pr892_head={PR892_HEAD}",
        f"pr904_head={PR904_HEAD}",
        (
            "endpoint c=18619 k=2 U=230415 "
            f"r={endpoint['r']} m={endpoint['m']} E={endpoint['E']} "
            f"N={endpoint['N']} D_pair={endpoint['D_pair']} "
            f"D_root={endpoint['D_root']} "
            f"existing_shortfall={-endpoint['existing_excess']}"
        ),
        (
            f"source_point mult={endpoint['mult']} D_star={endpoint['D_star']} "
            f"strengthened_excess={endpoint['excess']}"
        ),
        (
            "boundary c18619_k1 last_excluded_U=246939 "
            f"excess={c19k1_last['excess']} first_unexcluded_U=246940 "
            f"shortfall={-c19k1_next['excess']}"
        ),
        (
            "boundary c18619_k2 last_excluded_U=246935 "
            f"excess={c19k2_last['excess']} parity_skip_U=246936 "
            f"first_unexcluded_U=246937 shortfall={-c19k2_next['excess']}"
        ),
        (
            "boundary c18618_k1 last_excluded_U=246937 "
            f"excess={c18k1_last['excess']} first_unexcluded_U=246938 "
            f"shortfall={-c18k1_next['excess']}"
        ),
        "local_parent_charge=0 global_ledger_charge=0 official_score=0/2",
        f"mutations={caught}/6 caught",
        "RESULT: PASS",
    ]
    return "\n".join(lines) + "\n"


def verify_package() -> str:
    verify_contract(copy.deepcopy(EXPECTED_CONTRACT))
    verify_manifest()
    verify_note()
    verify_arithmetic()
    verify_sha_sums()
    report = render_report()
    require(EXPECTED_PATH.is_file(), f"missing expected output: {EXPECTED_PATH}")
    exact(report, EXPECTED_PATH.read_text(encoding="utf-8"), "expected output")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="run the full replay")
    group.add_argument(
        "--tamper-selftest", action="store_true", help="run semantic mutations"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.tamper_selftest:
            caught = mutation_selftest()
            print(f"MUTATION_SELFTEST: PASS {caught}/6 caught")
        else:
            sys.stdout.write(verify_package())
    except (CheckError, OSError, UnicodeError, ValueError) as exc:
        print(f"R31_ROLE04_CUBIC_SOURCE_PROJECTION_POINT: FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
