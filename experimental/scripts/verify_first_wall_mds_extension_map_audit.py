#!/usr/bin/env python3
"""Audit the Lean ownership maps for the first-wall MDS-extension packet.

Standard-library only and fail-closed. The checker pins the integrated PR #853
producer, frozen certificate, Lean declaration surface, repaired package maps,
and the generic-only #882 consumer excerpt. It replays the producer in normal
and optimized modes and restores each retired map overclaim as a negative
control without rewriting repository files.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
README = Path("experimental/lean/grande_finale/README.md")
SUMMARY = Path("experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md")
LEAN_MODULE = Path(
    "experimental/lean/grande_finale/GrandeFinale/"
    "FirstWallMDSExtensionInverse.lean"
)
LEAN_ROOT = Path("experimental/lean/grande_finale/GrandeFinale.lean")
NOTE = Path("experimental/notes/thresholds/first_wall_mds_extension_inverse.md")
PRODUCER = Path(
    "experimental/scripts/verify_first_wall_mds_extension_inverse.py"
)
CERTIFICATE = Path(
    "experimental/data/certificates/first-wall-mds-extension-inverse/"
    "first_wall_mds_extension_inverse.json"
)

INTEGRATION = "06b2a6fb8c49a5ec0e23b9103af7c92a328fcabf"
PRODUCER_PR_HEAD = "0c8d2c3c9227965a868b03e3a318fcc28ca26152"
CONSUMER_PR_HEAD = "af213091d2201d6e585ed14d8306aa2885c59802"
EXPECTED_PAYLOAD_SHA256 = (
    "65112f380c39047733527493ab9aa233115b0a01a81f72dd7ecfa11b650a2307"
)

SOURCE_SHA256 = {
    str(README):
        "80612e1c49043856b0e57588281bb8120c753039b18fcad298341de98899677e",
    str(SUMMARY):
        "9ef6ec4538e9760c2f05b2b27abce50fa45ecf57a50fe3aee4d4ffa6d56439bc",
    str(LEAN_MODULE):
        "6352005fb4c7223dea2d90e4fe9ba9fa153885c85a4d3e3259facbe753c9449e",
    str(LEAN_ROOT):
        "a36b3e2100f42358f13ed612098055d7c9c77d8e93f4013eaaa049040eed69c7",
    str(NOTE):
        "bbbf4eb88a5a0f693e73393aa27084e66bb68ad249377c88a31596f932743427",
    str(PRODUCER):
        "4286d9d5c6616b03a5c49f9042992efc1d287d735297b0e3faf3e04aa2b4b011",
    str(CERTIFICATE):
        "c0c00c665699622b09d02d0b334a4e6fcee9bb51c753be689a76a9022bb01d67",
}

REPAIRED_README_BLOCK = """- `GrandeFinale/FirstWallMDSExtensionInverse.lean` formalizes the abstract
  finite owner-image cap, equality/injectivity criterion, exact owner-fiber
  partition, and five pinned binomial identities used by the first-wall audit.
  Weighted-GRS interpolation, the MDS-extension equivalence, retained/deleted
  slack, and graph-arc normalization remain in the mathematical note; this is
  not a complete first-match catalogue.
"""
RETIRED_README_BLOCK = """- `GrandeFinale/FirstWallMDSExtensionInverse.lean` formalizes the finite
  first-wall MDS extension inverse: interpolation-owner partition, retained and
  deleted collision slack, graph-arc normalization, and exact finite counting
  kernels. It is an audit module, not a complete first-match catalogue.
"""
REPAIRED_SUMMARY_BLOCK = """- `GrandeFinale/FirstWallMDSExtensionInverse.lean`: abstract finite
  owner-image bounds, equality/injectivity criteria, the exact owner-fiber
  partition, and five pinned binomial identities used by the first-wall audit.
  Weighted-GRS interpolation, the MDS-extension equivalence, retained/deleted
  slack, and graph-arc normalization remain outside this Lean module.
"""
RETIRED_SUMMARY_BLOCK = """- `GrandeFinale/FirstWallMDSExtensionInverse.lean`: first-wall MDS
  extension inverse audit, including owner partition, slack ledger, graph-arc
  normalization, and finite counting kernels.
"""
RETIRED_BLOCK_SHA256 = {
    "README": "134f01af332cb3dbd54cfcdbec35028746946f8776535734a4bf4471b177f0d7",
    "SUMMARY": "b3b5952435207c690947afa01867d5af01a43d41dabb4e22f14dae26a8c4b47e",
}

EXPECTED_DECLARATIONS = {
    "ownerImage",
    "ownerFiber",
    "ownerImage_card_le",
    "ownerImage_card_eq_iff_injOn",
    "finite_ownerImage_card_le",
    "finite_ownerImage_card_eq_iff_injective",
    "card_eq_sum_ownerFiber",
    "choose_eight_four",
    "choose_eight_three",
    "choose_seven_three",
    "choose_six_three",
    "f7_nonMDS_weighted_occupancy",
}

CONSUMER_EXCERPT = """import GrandeFinale.RSExactCardPrefixWitnessBridge
import GrandeFinale.FirstWallMDSExtensionInverse
open GrandeFinale.CollisionAwarePole
open GrandeFinale.FirstMatchWitnessBridge
open GrandeFinale.FirstWallMDSExtensionInverse
open GrandeFinale.RSExactCardPrefixWitnessBridge
open GrandeFinale.RSExactCardWitnessBridge
omit [DecidableEq D] in
/-- Literal witnesses split exactly over their realized explanation states. -/
theorem card_eq_sum_retainedSupportOccupancy
    (C : Finset (RSExactCardWitness D F k)) :
    C.card = ∑ rho ∈ explanationStateImage C,
      retainedSupportOccupancy C rho := by
  simpa [explanationStateImage, retainedSupportFiber,
    retainedSupportOccupancy] using
    (card_eq_sum_ownerFiber C explanationState)
"""
CONSUMER_EXCERPT_SHA256 = (
    "2455b18bb7e55532897f14b05711b2b64fb965ac9a556e9b4e8338d09287c2e0"
)
CONSUMER_BLOB = "2fb56c9709f4923cb46527a28f169908ae7600d1"

CHECKS: list[tuple[str, bool]] = []


class AuditError(RuntimeError):
    """Raised when one audit gate fails."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_sha256(relative: Path) -> str:
    return sha256_bytes((ROOT / relative).read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def object_sha256(value: Any) -> str:
    return sha256_bytes(canonical_json(value).encode("utf-8"))


def read(relative: Path) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def norm_ws(value: str) -> str:
    return " ".join(value.split())


def check(name: str, condition: bool) -> None:
    passed = bool(condition)
    CHECKS.append((name, passed))
    if not passed:
        raise AuditError(name)


def readme_scope_honest(text: str) -> bool:
    return (
        text.count(REPAIRED_README_BLOCK) == 1
        and RETIRED_README_BLOCK not in text
        and "Weighted-GRS interpolation, the MDS-extension equivalence" in text
        and "not a complete first-match catalogue" in text
    )


def summary_scope_honest(text: str) -> bool:
    return (
        text.count(REPAIRED_SUMMARY_BLOCK) == 1
        and RETIRED_SUMMARY_BLOCK not in text
        and "remain outside this Lean module" in text
    )


def lean_executable(text: str) -> str:
    without_blocks = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--[^\n]*", "", without_blocks)


def run_producer(*arguments: str, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-B"]
    if optimized:
        command.append("-O")
    command.extend([str(ROOT / PRODUCER), *arguments])
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=240,
    )


def output(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def producer_passes(result: subprocess.CompletedProcess[str], *markers: str) -> bool:
    combined = output(result)
    return result.returncode == 0 and all(marker in combined for marker in markers)


def audit() -> None:
    check(
        "repaired maps and immutable PR #853 producer match SHA-256 pins",
        all(
            (ROOT / relative).is_file()
            and file_sha256(relative) == expected
            for relative, expected in SOURCE_SHA256.items()
        ),
    )

    readme = read(README)
    summary = read(SUMMARY)
    check("README assigns only abstract finite-counting ownership", readme_scope_honest(readme))
    check(
        "formalization summary assigns only abstract finite-counting ownership",
        summary_scope_honest(summary),
    )

    lean = read(LEAN_MODULE)
    declarations = set(
        re.findall(r"^(?:def|theorem)\s+([A-Za-z0-9_]+)", lean, flags=re.MULTILINE)
    )
    check(
        "Lean header and declaration inventory match the finite counting companion",
        "finite counting companion" in lean
        and "remain in the mathematical note; they are not asserted" in norm_ws(lean)
        and declarations == EXPECTED_DECLARATIONS
        and "variable {Basis : Type u} {Owner : Type v}" in lean,
    )

    executable = lean_executable(lean)
    check(
        "Lean executable has no proof escape or unowned semantic declaration",
        not re.search(r"\b(?:sorry|admit|axiom|unsafe)\b", executable)
        and not re.search(
            r"\b(?:interpolation|retained|deleted|slack|graph|arc|normalization)\b",
            executable,
            flags=re.IGNORECASE,
        ),
    )

    note = norm_ws(read(NOTE))
    lean_root = read(LEAN_ROOT)
    check(
        "note, root import, and frozen #882 excerpt preserve the generic boundary",
        "proves the finite image cap, equality/injectivity criterion, collision partition, and pinned binomial values"
        in note
        and "Weighted-GRS interpolation, the MDS equivalence, and Segre's theorem remain outside its formal scope"
        in note
        and lean_root.count("import GrandeFinale.FirstWallMDSExtensionInverse") == 1
        and sha256_bytes(CONSUMER_EXCERPT.encode("utf-8"))
        == CONSUMER_EXCERPT_SHA256
        and "(card_eq_sum_ownerFiber C explanationState)" in CONSUMER_EXCERPT
        and "theorem card_eq_sum_ownerFiber" in lean,
    )

    certificate = json.loads(read(CERTIFICATE))
    unhashed = copy.deepcopy(certificate)
    claimed_payload = unhashed.pop("payload_sha256")
    check(
        "certificate schema, base, status, and canonical payload hash are fresh",
        certificate.get("schema") == "first_wall_mds_extension_inverse.v1"
        and certificate.get("base_commit")
        == "7f278167e1e51f968896229ae438ea5a76398f90"
        and certificate.get("status") == "verified"
        and claimed_payload == EXPECTED_PAYLOAD_SHA256
        and object_sha256(unhashed) == EXPECTED_PAYLOAD_SHA256,
    )

    sources = certificate.get("sources", {})
    scope = certificate.get("scope", {})
    check(
        "certificate source manifest and Lean-independence boundary match actual files",
        sources
        == {
            str(NOTE): SOURCE_SHA256[str(NOTE)],
            str(PRODUCER): SOURCE_SHA256[str(PRODUCER)],
        }
        and scope.get("lean_target_independent") is True
        and scope.get("python_dependencies") == "standard-library-only"
        and "weighted-GRS interpolation formalization" in scope.get("not_claimed", []),
    )

    fixtures = certificate.get("general_fixtures", [])
    graphs = certificate.get("normalized_graph_arc_exhaustion", [])
    perturbations = certificate.get("one_point_perturbations", [])
    check(
        "frozen finite fixtures retain owner, extension, graph, and perturbation boundaries",
        len(fixtures) == 2
        and [item["p_full"]["pair_count"] for item in fixtures] == [70, 54]
        and fixtures[0]["equality_case"] is True
        and fixtures[1]["equality_case"] is False
        and fixtures[1]["extension_restrictions"]["dependent_count"] == 4
        and [item["arc_count"] for item in graphs] == [100, 294]
        and all(item["arc_equals_nondegenerate_quadratic"] is True for item in graphs)
        and [item["pair_deficit"] for item in perturbations] == [2, 4, 8, 10],
    )

    normal = run_producer("--check")
    check(
        "producer normal replay matches the frozen certificate",
        producer_passes(normal, "certificate check: PASS", EXPECTED_PAYLOAD_SHA256,
                        "verification: PASS"),
    )
    optimized = run_producer("--check", optimized=True)
    check(
        "producer optimized replay matches the frozen certificate",
        producer_passes(optimized, "certificate check: PASS", EXPECTED_PAYLOAD_SHA256,
                        "verification: PASS"),
    )

    tamper = run_producer("--tamper-selftest")
    tamper_optimized = run_producer("--tamper-selftest", optimized=True)
    check(
        "producer rejects 19/19 mutations in normal and optimized modes",
        producer_passes(
            tamper,
            "tamper-selftest: PASS (19/19 mutations rejected)",
            EXPECTED_PAYLOAD_SHA256,
        )
        and producer_passes(
            tamper_optimized,
            "tamper-selftest: PASS (19/19 mutations rejected)",
            EXPECTED_PAYLOAD_SHA256,
        ),
    )

    check(
        "isolated README regression restores and rejects the retired overclaim",
        sha256_bytes(RETIRED_README_BLOCK.encode("utf-8"))
        == RETIRED_BLOCK_SHA256["README"]
        and readme.count(REPAIRED_README_BLOCK) == 1
        and not readme_scope_honest(
            readme.replace(REPAIRED_README_BLOCK, RETIRED_README_BLOCK)
        ),
    )
    check(
        "isolated summary regression restores and rejects the retired overclaim",
        sha256_bytes(RETIRED_SUMMARY_BLOCK.encode("utf-8"))
        == RETIRED_BLOCK_SHA256["SUMMARY"]
        and summary.count(REPAIRED_SUMMARY_BLOCK) == 1
        and not summary_scope_honest(
            summary.replace(REPAIRED_SUMMARY_BLOCK, RETIRED_SUMMARY_BLOCK)
        ),
    )


def main() -> int:
    if sys.argv[1:] not in ([], ["--check"]):
        print(
            "usage: verify_first_wall_mds_extension_map_audit.py [--check]",
            file=sys.stderr,
        )
        return 2
    try:
        audit()
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        print(f"integration: {INTEGRATION}")
        print(f"producer_pr_head: {PRODUCER_PR_HEAD}")
        print(f"producer_payload_sha256: {EXPECTED_PAYLOAD_SHA256}")
        print(f"consumer_pr_head: {CONSUMER_PR_HEAD}")
        print(f"consumer_blob: {CONSUMER_BLOB}")
        print(f"RESULT: PASS ({len(CHECKS)}/{len(CHECKS)})")
        print("STATUS: AUDIT")
        return 0
    except (
        AuditError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.TimeoutExpired,
    ) as error:
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        print("STATUS: AUDIT")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
