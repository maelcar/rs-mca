#!/usr/bin/env python3
"""Verify the integral-coordinate D_s repair for the M31 ADE cut.

The all-rank proof is the symbolic support envelope in the accompanying note.
Finite root enumerations here are adversarial falsifier checks, not a substitute
for that proof.  The checker is standard-library-only and pins the unchanged
PR #637 census verifier and certificate byte-for-byte.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import os
import resource
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "m31_ade_integral_ds_repair.v1"
STATUS = "PROVED_PR648_INTEGRAL_DS_OPEN_GAP_FIXED"
CAP_BYTES = 1024**3
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/m31-ade-integral-ds-repair/"
    "m31_ade_integral_ds_repair.json"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_ade_integral_ds_repair.py"
)
REPAIR_NOTE_PATH = Path(
    "experimental/notes/thresholds/m31_ade_integral_ds_repair.md"
)
SOURCE_NOTE_PATH = Path(
    "experimental/notes/thresholds/"
    "cap25_v13_m31_k2_common_height_ade_cut.md"
)
SOURCE_VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_k2_common_height_ade_cut.py"
)
SOURCE_CERTIFICATE_PATH = Path(
    "experimental/data/cap25_v13_m31_k2_common_height_ade_cut.json"
)
SOURCE_PATHS = (
    VERIFIER_PATH,
    REPAIR_NOTE_PATH,
    SOURCE_NOTE_PATH,
    SOURCE_VERIFIER_PATH,
    SOURCE_CERTIFICATE_PATH,
)

BASE_COMMIT = "5c9aab794e6575d815541e0a5dd8534d03d400aa"
PR637_COMMIT = "178fec2363e276fa1dde4541673f5a3b2a2c01f2"
PR648_HEAD = "0c84a8f91331e2d35d9de9c69aa873e26aa1c71a"
PR648_AUDIT_NOTE_SHA256 = (
    "4eb93aaf0202baba5d809105b7e0a51e417dd2e62964aeacdc453062f146b554"
)
PR648_AUDIT_VERIFIER_SHA256 = (
    "5456bfb600aba2d2e9dd6de1919614fc85cc9f728e97aa2ba818c19718a30bf3"
)
PRE_REPAIR_NOTE_SHA256 = (
    "1c577650b65df78ce447368cee0d515d2fca69670d8f7e81956e7246f23eae27"
)
SOURCE_VERIFIER_SHA256 = (
    "4cc59c557dfe964aae96863c062bc66df18f8b01e807abcdae53edbc9147df95"
)
SOURCE_CERTIFICATE_SHA256 = (
    "db8218f5b97fc8b8f211f9cc2e40629bb5cc57575cb40b2c0d86fb068d88220a"
)

P = 2**31 - 1
N = 2**21
M = 981_129
W = 67_447
D0 = N - W
L = 2**24
R = M * (N - M)
T0 = 277_868


class CheckFailure(AssertionError):
    """Raised when a replay invariant fails."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise CheckFailure(label)


def impose_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = CAP_BYTES if hard == resource.RLIM_INFINITY else min(CAP_BYTES, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    require(soft != resource.RLIM_INFINITY and soft <= CAP_BYTES, "one GiB cap")
    return int(soft)


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def without_hash(obj: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(obj)
    result.pop("payload_sha256", None)
    return result


def payload_hash(obj: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(without_hash(obj))).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_repo(explicit: Path | None) -> Path:
    if explicit is not None:
        root = explicit.expanduser().resolve()
        require((root / SOURCE_NOTE_PATH).is_file(), "explicit repo has source note")
        return root
    if os.environ.get("M31_ADE_REPAIR_REPO"):
        return locate_repo(Path(os.environ["M31_ADE_REPAIR_REPO"]))
    candidates = [Path.cwd().resolve(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / SOURCE_NOTE_PATH).is_file():
            return candidate
    raise CheckFailure("pass --repo or set M31_ADE_REPAIR_REPO")


def dot(left: Iterable[int], right: Iterable[int]) -> int:
    return sum(a * b for a, b in zip(left, right))


def maximum_compatible_size(
    vectors: list[tuple[int, ...]],
    allowed_inner_products: tuple[int, ...] = (0, 1),
) -> int:
    """Exact maximum subset with prescribed distinct-root inner products."""
    count = len(vectors)
    adjacency = [0] * count
    for left in range(count):
        for right in range(left + 1, count):
            if dot(vectors[left], vectors[right]) in allowed_inner_products:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left

    best = 0

    def expand(size: int, candidates: int) -> None:
        nonlocal best
        if size + candidates.bit_count() <= best:
            return
        while candidates:
            vertex_bit = candidates & -candidates
            vertex = vertex_bit.bit_length() - 1
            expand(size + 1, candidates & adjacency[vertex])
            candidates ^= vertex_bit
            if size + candidates.bit_count() <= best:
                return
        best = max(best, size)

    expand(0, (1 << count) - 1)
    return best


def zero_coordinate_catalogue() -> dict[str, Any]:
    rows = []
    for unit_anchors in range(9):
        vectors = []
        for anchor in range(unit_anchors):
            for zero_sign in (-1, 1):
                vector = [0] * (unit_anchors + 1)
                vector[anchor] = 1
                vector[-1] = zero_sign
                vectors.append(tuple(vector))
        maximum = maximum_compatible_size(vectors)
        expected = 0 if unit_anchors == 0 else max(2, unit_anchors)
        require(maximum == expected, f"zero-coordinate maximum k={unit_anchors}")
        rows.append(
            {
                "unit_anchor_count": unit_anchors,
                "eligible_root_count": len(vectors),
                "maximum_pairwise_nonnegative_count": maximum,
                "claimed_max_2_or_anchor_count": expected,
            }
        )
    return {
        "model": "roots sign(z_i)e_i +/- e_j at one zero coordinate j",
        "pairwise_condition": "distinct-root inner product belongs to {0,1}",
        "rows": rows,
        "global_upper_used": 8,
        "all_pass": all(row["maximum_pairwise_nonnegative_count"] <= 8 for row in rows),
    }


def internal_support_catalogue() -> dict[str, Any]:
    rows = []
    maximum = 0
    checked = 0
    for left in range(-2, 3):
        if left == 0:
            continue
        for right in range(-2, 3):
            if right == 0 or left * left + right * right > 8:
                continue
            signings = [
                (left_sign, right_sign)
                for left_sign, right_sign in itertools.product((-1, 1), repeat=2)
                if left_sign * left + right_sign * right == 1
            ]
            checked += 1
            maximum = max(maximum, len(signings))
            require(len(signings) <= 1, f"internal support uniqueness {left},{right}")
            rows.append(
                {
                    "z_i": left,
                    "z_j": right,
                    "height_one_signings": [list(signing) for signing in signings],
                }
            )
    require(maximum == 1, "internal support maximum attained")
    return {
        "coordinate_bound": "nonzero integral |z_i|<=2 because Z_C<=8",
        "ordered_coordinate_pairs_checked": checked,
        "rows": rows,
        "maximum_height_one_signings_per_internal_support": maximum,
        "all_pass": maximum == 1,
    }


def symbolic_envelope() -> dict[str, Any]:
    rows = []
    for nonzero_coordinates in range(1, 9):
        k = nonzero_coordinates
        gap = k * (17 - k) // 2
        require(gap > 0, f"strict symbolic gap k={k}")
        left_slope = 8
        left_constant = -8 * k + k * (k - 1) // 2
        right_slope = 8
        right_constant = -gap
        require(
            (left_slope, left_constant) == (right_slope, right_constant),
            f"affine envelope identity k={k}",
        )
        rows.append(
            {
                "k": k,
                "zero_support_bound_per_coordinate": 8,
                "internal_support_bound": k * (k - 1) // 2,
                "gap_below_8s": gap,
                "identity": "8(s-k)+binom(k,2)=8s-k(17-k)/2",
                "affine_coefficients_left": [left_slope, left_constant],
                "affine_coefficients_right": [right_slope, right_constant],
                "strict_for_every_rank_s_at_least_k": True,
            }
        )
    return {
        "proof_role": (
            "all-rank arithmetic closure after the written support argument; "
            "unlike the finite sign catalogues, this is theorem-bearing"
        ),
        "k_range": [1, 8],
        "rows": rows,
        "conclusion": "|S_C|<8s<rho_0*s because rho_0>8",
        "all_pass": all(row["gap_below_8s"] > 0 for row in rows),
    }


def semantic_negative_controls() -> dict[str, Any]:
    vectors_k8 = []
    for anchor in range(8):
        for zero_sign in (-1, 1):
            vector = [0] * 9
            vector[anchor] = 1
            vector[-1] = zero_sign
            vectors_k8.append(tuple(vector))
    relaxed_nonnegative = maximum_compatible_size(
        vectors_k8, allowed_inner_products=(-1, 0, 1)
    )
    require(relaxed_nonnegative == 16 > 8, "negative control: permit -1")

    vectors_k9 = []
    for anchor in range(9):
        for zero_sign in (-1, 1):
            vector = [0] * 10
            vector[anchor] = 1
            vector[-1] = zero_sign
            vectors_k9.append(tuple(vector))
    norm_cap_nine = maximum_compatible_size(vectors_k9)
    require(norm_cap_nine == 9 > 8, "negative control: permit k=9")
    return {
        "purpose": "show both load-bearing local hypotheses fail when weakened",
        "permit_inner_product_minus_one": {
            "k": 8,
            "maximum": relaxed_nonnegative,
            "violates_eight_root_cap": relaxed_nonnegative > 8,
        },
        "permit_norm_cap_nine_and_k_nine": {
            "k": 9,
            "maximum": norm_cap_nine,
            "violates_eight_root_cap": norm_cap_nine > 8,
        },
        "all_pass": True,
    }


def rho(t: int) -> Fraction:
    return Fraction(N * t, 2 * N * t - R)


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def root_count_rank_floor(t: int) -> int:
    value = Fraction(L, 1) / rho(t) - 64 + 4 * rho(t)
    return ceil_fraction(value)


def m31_consumer_payload(root: Path) -> dict[str, Any]:
    source_verifier = root / SOURCE_VERIFIER_PATH
    source_certificate = root / SOURCE_CERTIFICATE_PATH
    require(file_sha256(source_verifier) == SOURCE_VERIFIER_SHA256, "source verifier pin")
    require(
        file_sha256(source_certificate) == SOURCE_CERTIFICATE_SHA256,
        "source certificate pin",
    )
    certificate = json.loads(source_certificate.read_text(encoding="utf-8"))
    require(
        certificate["schema"] == "cap25-v13-m31-k2-common-height-ade-cut-v1",
        "source schema",
    )
    require(
        certificate["constants"]
        == {"p": P, "N": N, "m": M, "w": W, "d0": D0, "L": L, "R": R, "t0": T0},
        "source constants",
    )
    boundary_rho = rho(T0)
    require(
        boundary_rho == Fraction(582_731_431_936, 70_500_333_905),
        "boundary rho",
    )
    require(8 < boundary_rho < Fraction(17, 2), "boundary rho interval")
    require(2 * N * T0 - R > 0 and N * R > 0, "monotonicity signs")
    require(rho(T0 + 1) < boundary_rho, "rho first monotonicity step")
    require(root_count_rank_floor(T0) == D0 + 15, "delivered rank gap")
    minimum_gap = next(gap for gap in range(1, 16) if P**gap > (N + 1) ** 16)
    require(minimum_gap == 11, "minimum determinant gap")

    expected_hashes = {
        "base_integrated": "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da",
        "old_union": "2f57a0a5379a4222869d4e6ab79aad39d7b352df6c0227996ab2da7ec10483a4",
        "old_residual": "40925c2c5a3c3928a42f6d92775de87608c7e260bf3c3ff7eda36b5e02193956",
        "classifier": "4801bb6740b214cf90590eafa827437fbb6b04da899db970c5f799af74b4750f",
        "new_exclusions": "b5f1a8c3d2916dd5077d641eef1dffcb2ae9385fd4707364a62ea37b01808a79",
        "new_union": "842d33d8258fd69c14f6b69ca3a9d5a8880df46225f142f0ea8cdd8daa5bb973",
        "new_residual": "2dcc296964f1a131428baf100f2e5a1c6291c91778fe533655255a5b7e8dce35",
    }
    actual_hashes = {
        "base_integrated": certificate["source_ledger"]["base_integrated_sha256"],
        "old_union": certificate["source_ledger"]["old_union_sha256"],
        "old_residual": certificate["source_ledger"]["old_residual_sha256"],
        "classifier": certificate["classifier"]["sha256"],
        "new_exclusions": certificate["classifier"]["new_exclusions_sha256"],
        "new_union": certificate["new_ledger"]["union_sha256"],
        "new_residual": certificate["new_ledger"]["residual_sha256"],
    }
    require(actual_hashes == expected_hashes, "all seven source hashes unchanged")
    counts = {
        "grid": certificate["source_ledger"]["grid_count"],
        "old_residual": certificate["source_ledger"]["old_residual_count"],
        "classifier": certificate["classifier"]["count"],
        "new_exclusions": certificate["classifier"]["new_exclusions_count"],
        "new_residual": certificate["new_ledger"]["residual_count"],
    }
    require(
        counts
        == {
            "grid": 3_254_885,
            "old_residual": 3_101_276,
            "classifier": 212_697,
            "new_exclusions": 113_864,
            "new_residual": 2_987_412,
        },
        "source counts unchanged",
    )
    return {
        "role": (
            "consumer/certificate pin only; PR #648 independently regenerated the "
            "census, while this verifier changes no classifier arithmetic"
        ),
        "boundary": {
            "rho_0_numerator": boundary_rho.numerator,
            "rho_0_denominator": boundary_rho.denominator,
            "eight_less_than_rho_0_less_than_17_over_2": True,
            "rho_successive_difference_positive_numerator": N * R,
            "fixed_parameter_application": "||zeta||^2<=rho(t)<=rho_0 for t>=t0",
            "rank_floor": root_count_rank_floor(T0),
            "delivered_rank_gap": 15,
            "minimum_determinant_gap": minimum_gap,
            "rank_gap_margin": 15 - minimum_gap,
        },
        "counts": counts,
        "seven_unchanged_sha256": actual_hashes,
        "classifier_band": "(2,t,t,2t), 277868<=t<=391731",
        "all_pass": True,
    }


def hypothesis_audit(root: Path) -> dict[str, Any]:
    source = (root / SOURCE_NOTE_PATH).read_text(encoding="utf-8")
    repair = (root / REPAIR_NOTE_PATH).read_text(encoding="utf-8")
    source_markers = [
        "distinct pairwise inner products in `{0,1}`",
        "also places `zeta` in the dual lattice",
        "|S intersect D_s| <= 8(s-k)+binom(k,2)",
        "8<rho0<17/2",
    ]
    repair_markers = [
        "finite sign catalogues are local checks, not the all-rank proof",
        "parameter `rho=rho_0`",
        "No paper TeX is changed",
    ]
    require(all(marker in source for marker in source_markers), "source hypothesis markers")
    require(all(marker in repair for marker in repair_markers), "repair scope markers")

    tex_hits = []
    for path in sorted(root.rglob("*.tex")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in ("113,864", "m31_k2_common_height_ade_cut"):
            if needle in text:
                tex_hits.append({"path": str(path.relative_to(root)), "needle": needle})
    require(not tex_hits, "no current TeX consumer")
    return {
        "printed_hypotheses_used": [
            "standard D_s roots +/-e_i+/-e_j",
            "integral coordinate branch of zeta in D_s dual",
            "common height one",
            "distinct selected-root inner products in {0,1}",
            "component norm Z_C at most fixed rho_0",
            "8<rho_0<17/2",
        ],
        "silently_stronger_hypotheses_used": [],
        "source_markers": source_markers,
        "repair_scope_markers": repair_markers,
        "tex_consumer_hits": tex_hits,
        "promotion_gate": "independent audit before any frontiers-TeX move",
        "all_pass": True,
    }


def build_payload(root: Path, effective_cap: int) -> dict[str, Any]:
    zero_catalogue = zero_coordinate_catalogue()
    internal_catalogue = internal_support_catalogue()
    symbolic = symbolic_envelope()
    negative_controls = semantic_negative_controls()
    consumer = m31_consumer_payload(root)
    hypotheses = hypothesis_audit(root)
    source_pins = {}
    for path in SOURCE_PATHS:
        require((root / path).is_file(), f"source pin exists: {path}")
        source_pins[str(path)] = file_sha256(root / path)

    checks = {
        "zero_coordinate_catalogue_passes": zero_catalogue["all_pass"],
        "internal_support_catalogue_passes": internal_catalogue["all_pass"],
        "all_rank_symbolic_envelope_passes": symbolic["all_pass"],
        "semantic_negative_controls_pass": negative_controls["all_pass"],
        "M31_consumer_and_boundary_pins_pass": consumer["all_pass"],
        "printed_hypotheses_and_promotion_scope_pass": hypotheses["all_pass"],
        "address_space_at_most_one_GiB": effective_cap <= CAP_BYTES,
    }
    require(all(checks.values()), "top-level checks")
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "role": (
            "proof-completeness repair for PR #637's integral-coordinate D_s "
            "count, resolving PR #648's sole open gap; no new classifier or TeX claim"
        ),
        "provenance": {
            "integrated_base_commit": BASE_COMMIT,
            "original_PR637_commit": PR637_COMMIT,
            "audit_PR648_head": PR648_HEAD,
            "audit_PR648_note_sha256": PR648_AUDIT_NOTE_SHA256,
            "audit_PR648_verifier_sha256": PR648_AUDIT_VERIFIER_SHA256,
            "audit_PR648_artifact_pins_role": "remote provenance, not a local replay dependency",
            "pre_repair_source_note_sha256": PRE_REPAIR_NOTE_SHA256,
            "unchanged_source_verifier_sha256": SOURCE_VERIFIER_SHA256,
            "unchanged_source_certificate_sha256": SOURCE_CERTIFICATE_SHA256,
        },
        "source_pins_sha256": source_pins,
        "hypothesis_audit": hypotheses,
        "zero_coordinate_sign_catalogue": zero_catalogue,
        "internal_support_sign_catalogue": internal_catalogue,
        "all_rank_symbolic_envelope": symbolic,
        "semantic_negative_controls": negative_controls,
        "M31_consumer": consumer,
        "address_space_cap_bytes": CAP_BYTES,
        "checks": checks,
        "verification": {
            "zero_argument_mode": "--check",
            "write": (
                "python3 experimental/scripts/"
                "verify_m31_ade_integral_ds_repair.py --write"
            ),
            "check": (
                "python3 experimental/scripts/"
                "verify_m31_ade_integral_ds_repair.py --check"
            ),
            "tamper_selftest": (
                "python3 experimental/scripts/"
                "verify_m31_ade_integral_ds_repair.py --tamper-selftest"
            ),
            "artifact_tamper_mutations": 8,
            "semantic_negative_controls": 2,
        },
        "nonclaims": [
            "The finite sign catalogues are local checks, not the all-rank proof.",
            "No census row, threshold, rank floor, or audited census hash is changed.",
            "No kappa other than the existing kappa=2 classifier is addressed.",
            "No complete M31 upper ledger or deployed CAP25 solution is claimed.",
            "No statement is promoted to the frontiers TeX.",
        ],
        "all_pass": all(checks.values()),
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    require(candidate.get("schema") == SCHEMA, "artifact schema")
    require(candidate.get("status") == STATUS, "artifact status")
    require(candidate.get("payload_sha256") == payload_hash(candidate), "artifact hash")
    require(canonical(candidate) == canonical(expected), "artifact exact replay")


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = []
    first = copy.deepcopy(expected)
    first["all_pass"] = False
    mutations.append(first)
    second = copy.deepcopy(expected)
    second["zero_coordinate_sign_catalogue"]["rows"][8][
        "maximum_pairwise_nonnegative_count"
    ] += 1
    second["payload_sha256"] = payload_hash(second)
    mutations.append(second)
    third = copy.deepcopy(expected)
    third["internal_support_sign_catalogue"][
        "maximum_height_one_signings_per_internal_support"
    ] = 2
    third["payload_sha256"] = payload_hash(third)
    mutations.append(third)
    fourth = copy.deepcopy(expected)
    fourth["all_rank_symbolic_envelope"]["rows"][0]["gap_below_8s"] = 0
    fourth["payload_sha256"] = payload_hash(fourth)
    mutations.append(fourth)
    fifth = copy.deepcopy(expected)
    fifth["semantic_negative_controls"]["permit_inner_product_minus_one"][
        "maximum"
    ] -= 1
    fifth["payload_sha256"] = payload_hash(fifth)
    mutations.append(fifth)
    sixth = copy.deepcopy(expected)
    sixth["source_pins_sha256"][str(SOURCE_NOTE_PATH)] = "0" * 64
    sixth["payload_sha256"] = payload_hash(sixth)
    mutations.append(sixth)
    seventh = copy.deepcopy(expected)
    seventh["M31_consumer"]["counts"]["new_exclusions"] += 1
    seventh["payload_sha256"] = payload_hash(seventh)
    mutations.append(seventh)
    eighth = copy.deepcopy(expected)
    eighth["nonclaims"].pop()
    eighth["payload_sha256"] = payload_hash(eighth)
    mutations.append(eighth)

    caught = 0
    for mutation in mutations:
        try:
            validate(mutation, expected)
        except CheckFailure:
            caught += 1
    require(caught == len(mutations), "all tamper mutations rejected")
    return caught


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--write", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--repo", type=Path)
    parser.add_argument("--artifact", type=Path, default=DEFAULT_ARTIFACT)
    args = parser.parse_args(argv)

    effective_cap = impose_cap()
    root = locate_repo(args.repo)
    expected = build_payload(root, effective_cap)
    artifact = args.artifact.expanduser()
    if not artifact.is_absolute():
        artifact = root / artifact

    if args.write:
        artifact.parent.mkdir(parents=True, exist_ok=True)
        artifact.write_text(
            json.dumps(expected, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"WROTE {artifact} {expected['payload_sha256']}")
        print(f"RLIMIT_AS {effective_cap} bytes")
        return 0
    if args.tamper_selftest:
        count = tamper_selftest(expected)
        print(f"PASS tamper-selftest ({count} mutations)")
        return 0

    require(artifact.is_file(), f"artifact exists: {artifact}")
    candidate = json.loads(artifact.read_text(encoding="utf-8"))
    validate(candidate, expected)
    print(f"PASS {artifact} {candidate['payload_sha256']}")
    print(f"RLIMIT_AS {effective_cap} bytes")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CheckFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
