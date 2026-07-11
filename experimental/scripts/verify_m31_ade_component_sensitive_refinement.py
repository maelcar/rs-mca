#!/usr/bin/env python3
"""Verify the component-sensitive ADE refinement of the M31 cut.

The checker proves the finite A_s dual-spectrum optimization, replays the
parent PR #653 certificate, and streams the complete M31 source grid to hash
the old and refined ledgers in constant extra memory.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import resource
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import verify_m31_ade_integral_ds_repair as parent_repair
from verify_m31_rank_inertia_anchor_cut import (
    L,
    M,
    N,
    R,
    W,
    anchor_threshold,
    ceil_div,
    centroid_cut,
    rank_inertia_cut,
)


SCHEMA = "m31_ade_component_sensitive_refinement.v1"
STATUS = "PROVED_COMPONENT_SENSITIVE_ADE_RHO_BELOW_NINE_AND_1452_ROW_DELTA"
CAP_BYTES = 1024**3
DEFAULT_ARTIFACT = Path(
    "experimental/data/certificates/m31-ade-component-sensitive/"
    "m31_ade_component_sensitive_refinement.json"
)
VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_ade_component_sensitive_refinement.py"
)
NOTE_PATH = Path(
    "experimental/notes/thresholds/m31_ade_component_sensitive_refinement.md"
)
PARENT_NOTE_PATH = Path(
    "experimental/notes/thresholds/m31_ade_integral_ds_repair.md"
)
PARENT_VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_ade_integral_ds_repair.py"
)
PARENT_CERTIFICATE_PATH = Path(
    "experimental/data/certificates/m31-ade-integral-ds-repair/"
    "m31_ade_integral_ds_repair.json"
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
RANK_INERTIA_VERIFIER_PATH = Path(
    "experimental/scripts/verify_m31_rank_inertia_anchor_cut.py"
)
SOURCE_PATHS = (
    VERIFIER_PATH,
    NOTE_PATH,
    PARENT_NOTE_PATH,
    PARENT_VERIFIER_PATH,
    PARENT_CERTIFICATE_PATH,
    SOURCE_NOTE_PATH,
    SOURCE_VERIFIER_PATH,
    SOURCE_CERTIFICATE_PATH,
    RANK_INERTIA_VERIFIER_PATH,
)

BASE_COMMIT = "8788a2432bd985cc9047fd000e73b98ac91530fb"
PR648_HEAD = "0c84a8f91331e2d35d9de9c69aa873e26aa1c71a"
PARENT_PAYLOAD_SHA256 = (
    "469e21269d2d8fde90408e373049342e8bed4bc7a0337e3759da4ab445426627"
)
PARENT_NOTE_SHA256 = (
    "63c9df5a61b93091d6926d09dd71736a01a7429249cfa0694ca5b62cdd5ebef2"
)
PARENT_VERIFIER_SHA256 = (
    "d4ab187c81e709689b329245f2cb107bed3aaf631bd73b7e845c714bb03d54ea"
)
PARENT_CERTIFICATE_SHA256 = (
    "b99d1c31a330880f4d481cec94cc17249074c4e68f355b42899d34cde9227c3f"
)
SOURCE_NOTE_SHA256 = (
    "99791710842e065fc82d7e37ce75001d531c1aec51457c8846b80e979891d86e"
)
SOURCE_VERIFIER_SHA256 = (
    "4cc59c557dfe964aae96863c062bc66df18f8b01e807abcdae53edbc9147df95"
)
SOURCE_CERTIFICATE_SHA256 = (
    "db8218f5b97fc8b8f211f9cc2e40629bb5cc57575cb40b2c0d86fb068d88220a"
)
RANK_INERTIA_VERIFIER_SHA256 = (
    "1ea1c6a1188895223dfca82d62f1fb05e2b9c7139b98e1f1b80c2a49d17619db"
)

P = 2**31 - 1
D0 = N - W
OLD_T0 = 277_868
T_STAR = 276_416
PR628_ROWS = {
    (2, 391_732, 391_732, 783_464),
    (2, 391_733, 391_733, 783_466),
    (2, 391_734, 391_734, 783_468),
    (2, 391_735, 391_735, 783_470),
}

EXPECTED_OLD_HASHES = {
    "integrated": "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da",
    "pre637_union": "2f57a0a5379a4222869d4e6ab79aad39d7b352df6c0227996ab2da7ec10483a4",
    "pre637_residual": "40925c2c5a3c3928a42f6d92775de87608c7e260bf3c3ff7eda36b5e02193956",
    "old_classifier": "4801bb6740b214cf90590eafa827437fbb6b04da899db970c5f799af74b4750f",
    "old_new_exclusions": "b5f1a8c3d2916dd5077d641eef1dffcb2ae9385fd4707364a62ea37b01808a79",
    "old_union": "842d33d8258fd69c14f6b69ca3a9d5a8880df46225f142f0ea8cdd8daa5bb973",
    "old_residual": "2dcc296964f1a131428baf100f2e5a1c6291c91778fe533655255a5b7e8dce35",
}

EXPECTED_NEW_HASHES = {
    "new_classifier": "784b4e9a6516c1ffad5c1c7e6b95962013fb2adb39f10655bb4d95dec09ef8ae",
    "new_exclusions": "96f444169abec3c3db43c7d8c38b67a989722ce72e1060ca6b39af2cbfad5862",
    "new_union": "8459f6876821c8da56ab96f4f23733878ae6c3423c385be5998071fb3bf4e9ef",
    "new_residual": "330cdf74ec81ef3212335482e849e70249d4d66f5b7ce1ceb9611d006782d177",
    "incremental_delta": "336a42986f9c6abd6347006456a19af960cf52765e6a02ae0679f11aba2ce7e1",
}


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
        require((root / NOTE_PATH).is_file(), "explicit repo has refinement note")
        return root
    if os.environ.get("M31_ADE_COMPONENT_REPO"):
        return locate_repo(Path(os.environ["M31_ADE_COMPONENT_REPO"]))
    candidates = [Path.cwd().resolve(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if (candidate / NOTE_PATH).is_file():
            return candidate
    raise CheckFailure("pass --repo or set M31_ADE_COMPONENT_REPO")


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def rho(t: int) -> Fraction:
    return Fraction(N * t, 2 * N * t - R)


def a_spectrum(n: int, residue: int, level: int) -> Fraction:
    return Fraction(residue * (n - residue), n) + 2 * level


def a_spectrum_payload(boundary: Fraction) -> dict[str, Any]:
    require(8 < boundary < 9, "rho star lies in heavy A window")
    q_ge_10_cases = []
    maximum_ratio = Fraction(-1, 1)
    maximum_case: dict[str, int] | None = None
    for residue in range(18):
        for level in range(5):
            q_value = residue + 2 * level
            if q_value < 10:
                continue
            strict_upper = Fraction(residue * residue, q_value - 9)
            row = {
                "m": residue,
                "j": level,
                "Q": q_value,
                "strict_n_upper": [
                    strict_upper.numerator,
                    strict_upper.denominator,
                ],
            }
            q_ge_10_cases.append(row)
            if strict_upper > maximum_ratio:
                maximum_ratio = strict_upper
                maximum_case = {
                    "m": residue,
                    "j": level,
                    "Q": q_value,
                }
    require(maximum_ratio == 100, "Q>=10 maximum strict n upper")
    require(
        maximum_case == {"m": 10, "j": 0, "Q": 10},
        "Q>=10 maximum witness",
    )

    q_eq_9_cases = [
        {"m": residue, "j": level}
        for residue in range(18)
        for level in range(5)
        if residue + 2 * level == 9
    ]
    require(
        q_eq_9_cases
        == [
            {"m": 1, "j": 4},
            {"m": 3, "j": 3},
            {"m": 5, "j": 2},
            {"m": 7, "j": 1},
            {"m": 9, "j": 0},
        ],
        "Q=9 residue-level cases",
    )

    gap_to_nine = Fraction(9, 1) - boundary
    heavy_n_upper = int(Fraction(81, 1) // gap_to_nine)
    require(heavy_n_upper == 953_224, "heavy A rank cap")
    require(
        heavy_n_upper * gap_to_nine <= 81
        < (heavy_n_upper + 1) * gap_to_nine,
        "heavy A rank floor identity",
    )

    checked = 0
    heavy_rows = 0
    maximum_heavy_n_seen = 0
    for n in range(2, 1001):
        for residue in range(min(17, n // 2) + 1):
            for level in range(5):
                value = a_spectrum(n, residue, level)
                checked += 1
                if not (8 < value <= boundary):
                    continue
                heavy_rows += 1
                maximum_heavy_n_seen = max(maximum_heavy_n_seen, n)
                require(n <= heavy_n_upper, "bounded heavy A rank cap")
                if n >= 111:
                    require(residue + 2 * level == 9, "large heavy A has Q=9")
    require(maximum_heavy_n_seen == 1000, "bounded falsifier reaches scan edge")

    return {
        "spectrum": "Z=m(n-m)/n+2j=Q-m^2/n, Q=m+2j",
        "heavy_window": "8<Z<=rho_star<9",
        "parameter_bounds": {
            "m_upper": 17,
            "j_upper": 4,
            "reason": "m/2<=Z<9 and 2j<=Z<9",
        },
        "Q_at_least_10_cases": q_ge_10_cases,
        "Q_at_least_10_maximum_strict_n_upper": [
            maximum_ratio.numerator,
            maximum_ratio.denominator,
        ],
        "Q_at_least_10_maximum_case": maximum_case,
        "large_n_forces_Q_equals_9_from": 111,
        "Q_equals_9_cases": q_eq_9_cases,
        "gap_to_nine": [gap_to_nine.numerator, gap_to_nine.denominator],
        "heavy_A_n_upper": heavy_n_upper,
        "heavy_A_n_upper_formula": "floor(81/(9-rho_star))",
        "heavy_allocation": {
            "heavy_A_root_count_strict_upper": 9 * heavy_n_upper,
            "remaining_A_root_count_strict_upper": N + 1,
            "remaining_D_root_count": 0,
            "remaining_E_root_count_strict_upper": 30,
            "total_root_count_strict_upper": 9 * heavy_n_upper + N + 31,
            "family_size": L,
            "contradiction": 9 * heavy_n_upper + N + 31 < L,
            "conclusion": "every A component has Z<=8",
        },
        "bounded_falsifier_scope": {
            "n_range": [2, 1000],
            "spectrum_rows_checked": checked,
            "heavy_rows_seen": heavy_rows,
            "maximum_heavy_n_seen": maximum_heavy_n_seen,
            "role": "falsifier only; the finite Q algebra is all-rank",
        },
        "A_component_excess_coefficient_after_heavy_exclusion": 1,
        "all_pass": True,
    }


def component_payload(parent_candidate: dict[str, Any]) -> dict[str, Any]:
    parent_rows = parent_candidate["all_rank_symbolic_envelope"]["rows"]
    require([row["k"] for row in parent_rows] == list(range(1, 9)), "parent D_int k range")
    require(all(row["gap_below_8s"] > 0 for row in parent_rows), "parent D_int strict")
    coefficients = {
        "A_s": 1,
        "D_s_integral": 0,
        "D_s_half_integral": 36,
        "E_6_7_8": 30,
    }
    require(max(coefficients.values()) == 36, "global component excess coefficient")
    require(17 - 8 == 9 and 9 * 4 == 36, "half-integral D coefficient")
    return {
        "component_bounds": {
            "A_s": "|S_C|<=8s+Z_C after the heavy-A exclusion",
            "D_s_integral": "|S_C|<8s (PR #653 replayed)",
            "D_s_half_integral": "|S_C|<=17s<=8s+36Z_C",
            "E_6_7_8": "|S_C|<=30Z_C<=8s+30Z_C",
        },
        "excess_coefficients": coefficients,
        "half_integral_D_inputs": {
            "rank_cost": "s<=4Z_C",
            "matching_cost": "nu/2<=Z_C<9, hence nu<=17",
            "support_edge_bound": "|S_C|<=nu*s",
        },
        "orthogonal_norm_sum": "sum_C Z_C=||zeta||^2<=rho",
        "global_conclusion": "|S|<=8r+36rho_star<8r+324",
        "parent_D_integral_payload_sha256": parent_candidate["payload_sha256"],
        "all_pass": True,
    }


def semantic_negative_controls(boundary: Fraction, heavy_n_upper: int) -> dict[str, Any]:
    relaxed_n = heavy_n_upper + 1
    relaxed_value = a_spectrum(relaxed_n, 9, 0)
    relaxed_left = relaxed_n * relaxed_value
    relaxed_right = 8 * (relaxed_n - 1) + relaxed_value
    require(boundary < relaxed_value < 9, "rho<=9 witness escapes fixed boundary")
    require(relaxed_left > relaxed_right, "rho<=9 breaks light A envelope")

    skipped_n = heavy_n_upper
    skipped_value = a_spectrum(skipped_n, 9, 0)
    skipped_left = skipped_n * skipped_value
    skipped_right = 8 * (skipped_n - 1) + skipped_value
    require(8 < skipped_value <= boundary, "heavy allocation witness range")
    require(skipped_left > skipped_right, "heavy allocation is load-bearing")
    return {
        "relax_fixed_rho_star_to_nonstrict_nine": {
            "n": relaxed_n,
            "m": 9,
            "j": 0,
            "Z": [relaxed_value.numerator, relaxed_value.denominator],
            "nZ": [relaxed_left.numerator, relaxed_left.denominator],
            "8s_plus_Z": [relaxed_right.numerator, relaxed_right.denominator],
            "envelope_fails": relaxed_left > relaxed_right,
        },
        "skip_heavy_A_allocation": {
            "n": skipped_n,
            "m": 9,
            "j": 0,
            "Z": [skipped_value.numerator, skipped_value.denominator],
            "nZ": [skipped_left.numerator, skipped_left.denominator],
            "8s_plus_Z": [skipped_right.numerator, skipped_right.denominator],
            "envelope_fails": skipped_left > skipped_right,
        },
        "all_pass": True,
    }


class StreamDigest:
    def __init__(self) -> None:
        self._hash = hashlib.sha256()
        self.count = 0
        self.first: tuple[int, int, int, int] | None = None
        self.last: tuple[int, int, int, int] | None = None

    def add(self, row: tuple[int, int, int, int]) -> None:
        if self.count:
            self._hash.update(b";")
        self._hash.update(",".join(map(str, row)).encode("ascii"))
        if self.first is None:
            self.first = row
        self.last = row
        self.count += 1

    def record(self) -> dict[str, Any]:
        return {
            "count": self.count,
            "sha256": self._hash.hexdigest(),
            "first": list(self.first) if self.first is not None else None,
            "last": list(self.last) if self.last is not None else None,
        }


def census_payload() -> dict[str, Any]:
    names = (
        "integrated",
        "pre637_union",
        "pre637_residual",
        "old_classifier",
        "old_new_exclusions",
        "old_union",
        "old_residual",
        "new_classifier",
        "new_exclusions",
        "new_union",
        "new_residual",
        "incremental_delta",
    )
    streams = {name: StreamDigest() for name in names}
    grid_count = 0
    thresholds = {kappa: anchor_threshold(kappa) for kappa in range(2, 775)}

    for kappa in range(2, 775):
        anchor = thresholds[kappa][0]
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            row = (kappa, t, (kappa - 1) * t, kappa * t)
            grid_count += 1
            integrated = rank_inertia_cut(kappa, t, anchor) or centroid_cut(kappa, t)
            pr628 = row in PR628_ROWS
            pre637_union = integrated or pr628
            old_classifier = kappa == 2 and t >= OLD_T0
            new_classifier = kappa == 2 and t >= T_STAR
            old_union = pre637_union or old_classifier
            new_union = pre637_union or new_classifier
            flags = {
                "integrated": integrated,
                "pre637_union": pre637_union,
                "pre637_residual": not pre637_union,
                "old_classifier": old_classifier,
                "old_new_exclusions": old_classifier and not pre637_union,
                "old_union": old_union,
                "old_residual": not old_union,
                "new_classifier": new_classifier,
                "new_exclusions": new_classifier and not pre637_union,
                "new_union": new_union,
                "new_residual": not new_union,
                "incremental_delta": new_classifier and not old_classifier,
            }
            if flags["incremental_delta"]:
                require(not pre637_union, "incremental band disjoint from prior union")
            for name, include in flags.items():
                if include:
                    streams[name].add(row)

    require(grid_count == 3_254_885, "source grid count")
    records = {name: stream.record() for name, stream in streams.items()}
    old_hashes = {name: records[name]["sha256"] for name in EXPECTED_OLD_HASHES}
    require(old_hashes == EXPECTED_OLD_HASHES, "all old census hashes")
    expected_counts = {
        "integrated": 153_605,
        "pre637_union": 153_609,
        "pre637_residual": 3_101_276,
        "old_classifier": 212_697,
        "old_new_exclusions": 113_864,
        "old_union": 267_473,
        "old_residual": 2_987_412,
        "new_classifier": 214_149,
        "new_exclusions": 115_316,
        "new_union": 268_925,
        "new_residual": 2_985_960,
        "incremental_delta": 1_452,
    }
    require(
        {name: records[name]["count"] for name in expected_counts} == expected_counts,
        "all old/new census counts",
    )
    require(
        records["incremental_delta"]["first"] == [2, 276_416, 276_416, 552_832]
        and records["incremental_delta"]["last"] == [2, 277_867, 277_867, 555_734],
        "incremental band endpoints",
    )
    require(
        records["new_exclusions"]["last"] == [2, 391_731, 391_731, 783_462],
        "new exclusion endpoint",
    )
    new_hashes = {
        name: records[name]["sha256"]
        for name in (
            "new_classifier",
            "new_exclusions",
            "new_union",
            "new_residual",
            "incremental_delta",
        )
    }
    if EXPECTED_NEW_HASHES:
        require(new_hashes == EXPECTED_NEW_HASHES, "all new census hashes")
    return {
        "method": (
            "canonical kappa,t order; semicolon-delimited row encoding; "
            "all sets hashed in one O(1)-memory pass"
        ),
        "grid_count": grid_count,
        "records": records,
        "expected_counts": expected_counts,
        "old_hashes_reproduced": old_hashes,
        "new_hashes": new_hashes,
        "new_hashes_hard_pinned": bool(EXPECTED_NEW_HASHES),
        "all_pass": True,
    }


def boundary_payload() -> dict[str, Any]:
    boundary = rho(T_STAR)
    previous = rho(T_STAR - 1)
    construction_denominator = 2 * N * T_STAR - R
    require(T_STAR == 9 * R // (17 * N) + 1, "strict rho<9 threshold")
    require(
        boundary == Fraction(579_686_367_232, 64_410_204_497),
        "component boundary rho",
    )
    require(8 < boundary < 9 < previous, "boundary interval split")
    require(
        construction_denominator == 64_410_204_497 > 0,
        "common-height construction positivity",
    )
    source_grid_t_upper = M // 2
    require(
        T_STAR <= source_grid_t_upper == 490_564 < P,
        "classified source-grid t is nonzero modulo p",
    )
    require(0 < M < P, "M31 weight is nonzero modulo p")
    gap_to_nine = 9 - boundary
    heavy_n_upper = int(Fraction(81, 1) // gap_to_nine)
    require(heavy_n_upper == 953_224, "boundary heavy A rank cap")
    require(
        heavy_n_upper * gap_to_nine <= 81
        < (heavy_n_upper + 1) * gap_to_nine,
        "boundary heavy A floor",
    )
    heavy_allocation_upper = 9 * heavy_n_upper + N + 31
    require(heavy_allocation_upper == 10_676_199 < L, "heavy A allocation contradiction")
    rank_lower = ceil_fraction((Fraction(L, 1) - 36 * boundary) / 8)
    require(rank_lower == N - 40 == D0 + 67_407, "component rank lower")
    gap = rank_lower - D0
    minimum_gap = next(value for value in range(1, 20) if P**value > (N + 1) ** 17)
    require(minimum_gap == 12 and gap > minimum_gap, "determinant gap")
    require(P**gap > (N + 1) ** 17, "component determinant contradiction")
    return {
        "t_star": T_STAR,
        "rho_star": [boundary.numerator, boundary.denominator],
        "rho_previous": [previous.numerator, previous.denominator],
        "rho_star_between_8_and_9": True,
        "rho_previous_above_9": True,
        "rho_is_decreasing_successive_difference_numerator": N * R,
        "fixed_parameter_application": "||zeta||^2<=rho(t)<=rho_star for every t>=t_star",
        "common_height_denominator_at_t_star": construction_denominator,
        "common_height_h_squared_positive": True,
        "source_grid_t_upper": source_grid_t_upper,
        "source_grid_t_and_weight_nonzero_mod_p": True,
        "gap_to_nine": [gap_to_nine.numerator, gap_to_nine.denominator],
        "heavy_A_n_upper": heavy_n_upper,
        "heavy_allocation_root_count_strict_upper": heavy_allocation_upper,
        "rank_lower": rank_lower,
        "rank_lower_as_N_minus": 40,
        "rank_gap_over_d0": gap,
        "minimum_determinant_gap": minimum_gap,
        "component_count_upper": 17,
        "first_uncertified_row": [2, 276_415, 276_415, 552_830],
        "all_pass": True,
    }


def replay_parent(root: Path, effective_cap: int) -> dict[str, Any]:
    expected = parent_repair.build_payload(root, effective_cap)
    candidate = json.loads((root / PARENT_CERTIFICATE_PATH).read_text(encoding="utf-8"))
    parent_repair.validate(candidate, expected)
    require(candidate["payload_sha256"] == PARENT_PAYLOAD_SHA256, "parent payload pin")
    return {
        "artifact": str(PARENT_CERTIFICATE_PATH),
        "payload_sha256": candidate["payload_sha256"],
        "status": candidate["status"],
        "exact_replay": True,
    }


def hypothesis_scope(root: Path) -> dict[str, Any]:
    note = (root / NOTE_PATH).read_text(encoding="utf-8")
    markers = [
        "exactly L=8N distinct selected roots",
        "No lower bound on rho(t)",
        "2Nt_*-R=64410204497>0",
        "boundary parameter** rho_*",
        "This packet deliberately stops at rho<9",
        "This is a certificate boundary, not a counterexample",
        "|S| <= 8r+36rho_* < 8r+324",
    ]
    require(all(marker in note for marker in markers), "note hypothesis/scope markers")
    tex_hits = []
    for path in sorted(root.rglob("*.tex")):
        text = path.read_text(encoding="utf-8", errors="replace")
        for needle in (
            "m31_ade_component_sensitive_refinement",
            "CS-ADE-9",
            "214149",
            "2985960",
        ):
            if needle in text:
                tex_hits.append({"path": str(path.relative_to(root)), "needle": needle})
    require(not tex_hits, "no TeX consumer or promotion")
    return {
        "used_hypotheses": [
            "exactly L=8N selected roots and real rank at most N",
            "orthogonal ADE decomposition",
            "component projections of zeta lie in component duals",
            "selected roots have norm squared two and common height one",
            "distinct selected-root inner products belong to {0,1}",
            "total component norm sum is at most fixed rho_star",
            "rho_star<9 with its exact positive gap to nine",
            "positive common-height denominator throughout the classified source grid",
            "source-grid t and M31 weight are nonzero modulo p",
            "M31 modular rank is at most d0",
        ],
        "silently_stronger_hypotheses": [],
        "note_markers": markers,
        "tex_hits": tex_hits,
        "rho_at_least_9_optimization_in_scope": False,
        "all_pass": True,
    }


def verify_hard_pins(root: Path) -> None:
    expected = {
        PARENT_NOTE_PATH: PARENT_NOTE_SHA256,
        PARENT_VERIFIER_PATH: PARENT_VERIFIER_SHA256,
        PARENT_CERTIFICATE_PATH: PARENT_CERTIFICATE_SHA256,
        SOURCE_NOTE_PATH: SOURCE_NOTE_SHA256,
        SOURCE_VERIFIER_PATH: SOURCE_VERIFIER_SHA256,
        SOURCE_CERTIFICATE_PATH: SOURCE_CERTIFICATE_SHA256,
        RANK_INERTIA_VERIFIER_PATH: RANK_INERTIA_VERIFIER_SHA256,
    }
    for path, digest in expected.items():
        require(file_sha256(root / path) == digest, f"hard source pin: {path}")


def build_payload(root: Path, effective_cap: int) -> dict[str, Any]:
    verify_hard_pins(root)
    parent = replay_parent(root, effective_cap)
    boundary = boundary_payload()
    boundary_fraction = Fraction(*boundary["rho_star"])
    spectrum = a_spectrum_payload(boundary_fraction)
    components = component_payload(
        json.loads((root / PARENT_CERTIFICATE_PATH).read_text(encoding="utf-8"))
    )
    negative_controls = semantic_negative_controls(
        boundary_fraction,
        boundary["heavy_A_n_upper"],
    )
    census = census_payload()
    scope = hypothesis_scope(root)
    source_pins = {}
    for path in SOURCE_PATHS:
        require((root / path).is_file(), f"source pin exists: {path}")
        source_pins[str(path)] = file_sha256(root / path)

    checks = {
        "parent_PR653_exact_replay_passes": parent["exact_replay"],
        "A_s_dual_spectrum_and_heavy_allocation_pass": spectrum["all_pass"],
        "component_summation_passes": components["all_pass"],
        "semantic_negative_controls_pass": negative_controls["all_pass"],
        "fixed_boundary_and_determinant_pass": boundary["all_pass"],
        "streamed_old_and_new_census_pass": census["all_pass"],
        "hypothesis_and_promotion_scope_pass": scope["all_pass"],
        "address_space_at_most_one_GiB": effective_cap <= CAP_BYTES,
    }
    require(all(checks.values()), "top-level checks")
    payload = {
        "schema": SCHEMA,
        "status": STATUS,
        "role": (
            "M31-specific rho-below-nine common-height ADE theorem and exact 1452-row "
            "M31 refinement, stacked on PR #653 with no TeX promotion"
        ),
        "provenance": {
            "stacked_base_PR653_commit": BASE_COMMIT,
            "audit_PR648_head": PR648_HEAD,
            "parent_payload_sha256": PARENT_PAYLOAD_SHA256,
            "four_non_log_parent_payload_files_byte_identical": True,
            "parent_agents_log_entry_preserved": True,
        },
        "source_pins_sha256": source_pins,
        "parent_PR653_replay": parent,
        "hypothesis_audit": scope,
        "A_s_dual_spectrum": spectrum,
        "component_envelopes": components,
        "semantic_negative_controls": negative_controls,
        "M31_boundary": boundary,
        "streamed_census": census,
        "address_space_cap_bytes": CAP_BYTES,
        "checks": checks,
        "verification": {
            "zero_argument_mode": "--check",
            "write": (
                "python3 experimental/scripts/"
                "verify_m31_ade_component_sensitive_refinement.py --write"
            ),
            "check": (
                "python3 experimental/scripts/"
                "verify_m31_ade_component_sensitive_refinement.py --check"
            ),
            "tamper_selftest": (
                "python3 experimental/scripts/"
                "verify_m31_ade_component_sensitive_refinement.py --tamper-selftest"
            ),
            "artifact_tamper_mutations": 8,
            "semantic_negative_controls": 2,
        },
        "nonclaims": [
            "No optimization at rho>=9 is claimed.",
            "The first uncertified row is not claimed to be a counterexample.",
            (
                "All four non-log PR #653 payload files are byte-identical; "
                "the shared agents log gains only the successor entry."
            ),
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
    second["A_s_dual_spectrum"]["heavy_A_n_upper"] += 1
    second["payload_sha256"] = payload_hash(second)
    mutations.append(second)
    third = copy.deepcopy(expected)
    third["component_envelopes"]["excess_coefficients"]["D_s_half_integral"] = 35
    third["payload_sha256"] = payload_hash(third)
    mutations.append(third)
    fourth = copy.deepcopy(expected)
    fourth["M31_boundary"]["t_star"] -= 1
    fourth["payload_sha256"] = payload_hash(fourth)
    mutations.append(fourth)
    fifth = copy.deepcopy(expected)
    fifth["streamed_census"]["expected_counts"]["incremental_delta"] += 1
    fifth["payload_sha256"] = payload_hash(fifth)
    mutations.append(fifth)
    sixth = copy.deepcopy(expected)
    sixth["streamed_census"]["new_hashes"]["new_residual"] = "0" * 64
    sixth["payload_sha256"] = payload_hash(sixth)
    mutations.append(sixth)
    seventh = copy.deepcopy(expected)
    seventh["source_pins_sha256"][str(PARENT_CERTIFICATE_PATH)] = "0" * 64
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
    require(caught == len(mutations), "all artifact tampers rejected")
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
        for name, digest in expected["streamed_census"]["new_hashes"].items():
            print(f"{name}_sha256={digest}")
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
    except (CheckFailure, parent_repair.CheckFailure) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
