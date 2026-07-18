#!/usr/bin/env python3
"""Audit the integrated triple-negative first-match packet and its sources.

Standard-library only and fail-closed.  The checker pins PR #829's arithmetic
and Lean producer, the repaired certificate, the same-wave PR #823 fixed-slope
source, and PR #832's deep-hole pencil/design correction.  It independently
replays the denominator grid and rejects the retired integration-status and
basis-heavy residual descriptions as negative controls.
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
TRIPLE_NOTE = Path(
    "experimental/notes/thresholds/triple_negative_first_match_reduction.md"
)
TRIPLE_SCRIPT = Path(
    "experimental/scripts/verify_triple_negative_first_match_reduction.py"
)
TRIPLE_CERT = Path(
    "experimental/data/certificates/triple-negative-first-match-reduction/"
    "triple_negative_first_match_reduction.json"
)
TRIPLE_LEAN = Path(
    "experimental/lean/grande_finale/GrandeFinale/"
    "TripleNegativeFirstMatchReduction.lean"
)
LEAN_ROOT = Path("experimental/lean/grande_finale/GrandeFinale.lean")
LEAN_README = Path("experimental/lean/grande_finale/README.md")
LEAN_SUMMARY = Path("experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md")

DIRECTION_NOTE = Path(
    "experimental/notes/thresholds/"
    "selector_free_direction_distance_all_pair.md"
)
FIXED_DEFICIENCY_NOTE = Path(
    "experimental/notes/thresholds/fixed_deficiency_complete_absorption.md"
)
PAVING_NOTE = Path(
    "experimental/notes/thresholds/"
    "all_pair_paving_basis_multiplicity_compiler.md"
)
DEPTH_ZERO_NOTE = Path(
    "experimental/notes/thresholds/depth_zero_identity_lineray_owner.md"
)

FIXED_SLOPE_NOTE = Path(
    "experimental/notes/thresholds/fixed_slope_kernel_johnson_multiplicity.md"
)
FIXED_SLOPE_SCRIPT = Path(
    "experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py"
)
FIXED_SLOPE_CERT = Path(
    "experimental/data/certificates/"
    "fixed-slope-kernel-johnson-multiplicity/"
    "fixed_slope_kernel_johnson_multiplicity.json"
)

PENCIL_NOTE = Path(
    "experimental/notes/thresholds/augmented_basis_pencil_design_inverse.md"
)
PENCIL_SCRIPT = Path(
    "experimental/scripts/verify_augmented_basis_pencil_design_inverse.py"
)
PENCIL_CERT = Path(
    "experimental/data/certificates/augmented-basis-pencil-design-inverse/"
    "augmented_basis_pencil_design_inverse.json"
)

INTEGRATION = "168e9ba0280e069a8bd552a6e2098bb9248c70b7"
TRIPLE_PR_HEAD = "abdef3be4bb9e18030b6fd1f4c639849689f3a23"
FIXED_SLOPE_PR_HEAD = "06c06581459a1b6667a9b2afdfc20c90c31949b7"
PENCIL_PR_HEAD = "402b27032187dca3c263575967e49d148443dd6d"

TRIPLE_PAYLOAD = (
    "a8c0ae04007b364cb7d47ec6f04b0985399a18b7a70ab159698dca6aca3e024d"
)
FIXED_SLOPE_PAYLOAD = (
    "e8e4ee730d95d5347d934e2fd610dc453289e844d4688d30c572fe2f5c9e6c4b"
)
PENCIL_PAYLOAD = (
    "59f7da83e72af6a1d94f78c984b13a05949d887f25934e5fec0b87b996959b9a"
)

SOURCE_SHA256 = {
    str(TRIPLE_NOTE):
        "2f0f20c7c03a4c0dd2a3fb0b3aae6001728166aae0798a971aed77666328c953",
    str(TRIPLE_SCRIPT):
        "4cd3d8a1983c5ebc267836884000008c0bdfa14a31b1d06772df4febfa2d736d",
    str(TRIPLE_CERT):
        "f72948230473cd2ff4f4b3d12f1ce3aa2dfded07d4a7fb3918a99885e27b95d1",
    str(TRIPLE_LEAN):
        "ae3ceda8bbf893676b55fef4255d5fff3d8831f29739a36c31d4f8517ecd180b",
    str(DIRECTION_NOTE):
        "6bb3462d93e3e78d4ce83e493579bc64333fcbcc9b4eb3749a23745a57070129",
    str(FIXED_DEFICIENCY_NOTE):
        "d096a7f5e6399a51132d404347bbb4e8ab992fce53387c1dd407e4dd263b8403",
    str(PAVING_NOTE):
        "84d1ed18a110f0e1fee423905bee5710be42f3e8651cefd50db9646d5ffcc239",
    str(DEPTH_ZERO_NOTE):
        "01ab296293d2640269448650c7b2c3d1a9c01a6bdae8c92b8d87a5739a859e6a",
    str(FIXED_SLOPE_NOTE):
        "cdd722913c5823a3b6d253ff9318528d73849defb51bb9296329fb4ce9c4ce21",
    str(FIXED_SLOPE_SCRIPT):
        "8b44fdbef8a564b8e40e72a3a248d29d3b6215091f5d52b708c27d9c6f04143e",
    str(FIXED_SLOPE_CERT):
        "db4deb0235d2bb86f2c169d1bf55bbdb7286738ac9c74834143c006dfbc415c9",
    str(PENCIL_NOTE):
        "df5d9c120dd680fdffc7ea4e1695e9a4b734e63492e8d13e3590ce7f08c6880c",
    str(PENCIL_SCRIPT):
        "dd3018e619941519b334ef2794761b9f73c95b6bc086c73ee53da313ef38a35d",
    str(PENCIL_CERT):
        "0fc39e925b8ce5ff98df38fd0ab6ce0910b16592744f932d84d30d46e1bf081c",
}

RETIRED_SHA256 = {
    str(TRIPLE_NOTE):
        "53bd520b9183a01d0342f1a42ec9e3e668bcf4ec1b5e571b957ae41854dc4583",
    str(TRIPLE_SCRIPT):
        "07ef4aeff6230f64ac23cb7cbc10e3fb34bc1ab43640d4ec3f764983805921bd",
    str(TRIPLE_CERT):
        "ff33f8ea2d3ee0ea2a4f5d0779ca7a1e94b56a1c69c2871230342b00b13afd94",
}

REPAIRED_INTEGRATION_BLOCK = """The fixed-slope theorem that introduced `J_K` originated in PR `#817` and
was integrated through superset PR `#823` head `06c06581` in `168e9ba0`.
The arithmetic reduction here remains standalone.  It uses that integrated
result only to interpret `J_K>0` as the neighboring fixed-slope payment.
"""
RETIRED_INTEGRATION_BLOCK = """The fixed-slope theorem that introduced `J_K` is pending upstream PR `#817`.
The arithmetic reduction here is standalone and does not vendor or assume the
integration of that packet.  It consumes the pending result only to interpret
`J_K>0` as the neighboring fixed-slope payment.
"""
REPAIRED_RESIDUAL_BLOCK = """PR `#832`, integrated in the same `168e9ba0` wave, corrects how (31) may be
used on the deep-hole boundary.  When `d_dir=R`,
`beta_(kappa+1)(A)=binom(N,kappa+1)` automatically, so basis heaviness has no
inverse content.  At the first sharp case `R-t=1`, the exact source target is
the **deep-hole pencil/design owner dichotomy**: prove an image-normalized
deficit for the distributed core pencils or almost-Steiner design, or route
the whole pair fiber to a named earlier owner.  The exact pencil-slack ledger
in `augmented_basis_pencil_design_inverse.md` shows that `beta` alone has no
inverse content.  Its positive-depth affine-line equality fixture has
`kappa=1` and lies outside `J_K<=0`, so it is a source-boundary example,
not a counterexample to a stronger in-chamber inverse.  Any common-flat or
low-degree conclusion on (31) needs additional `J_K` and first-match
hypotheses; it does not follow from basis heaviness.
"""
RETIRED_RESIDUAL_BLOCK = """Equivalently, the remaining atom is basis-heavy and has neither a low-rank
transversal nor uniformly low-rank same-slope fibers.  It needs an inverse
step extracting a common flat/low-degree locator family, or a genuinely new
polynomial-value/beyond-Johnson input.  Another mask-by-mask Johnson count
cannot distinguish it.
"""

CURRENT_SOURCE_MARKER = (
    "The exact remaining wall is the **deep-hole pencil/design owner dichotomy**"
)
RETIRED_SOURCE_MARKER = (
    "The exact remaining wall is the **basis-heavy deep-hole owner dichotomy**"
)
CURRENT_NONCLAIM = (
    "The integrated fixed-slope J_K source theorem from PR #823 is used only "
    "for its displayed neighboring J_K>0 interpretation; it does not make "
    "J_K<=0 a semantic owner cell."
)
CURRENT_REMAINING_WALL = (
    "the local positive-depth J_K<=0 ratio remains conditional; on d=R the "
    "exact source target is the deep-hole core-pencil/design owner dichotomy, "
    "with beta automatically maximal, so prove image-normalized pencil/design "
    "deficit or route the whole fiber"
)

EXPECTED_DECLARATIONS = {
    "kernelJohnsonDenominator",
    "hammingDenominator",
    "puncturedJohnsonDenominator",
    "profileDepth",
    "deficiency",
    "ValidParameters",
    "hamming_denominator_identity",
    "punctured_denominator_high_degree_identity",
    "punctured_denominator_low_degree_identity",
    "punctured_denominator_low_degree_nesting_identity",
    "depth_deficiency_coordinates",
    "depth_deficiency_factorization",
    "kernel_nonpositive_iff_depth_deficiency_wall",
    "kernel_nonpositive_forces_kappa_two",
    "kernel_nonpositive_forces_profile_bounds",
    "kernel_nonpositive_forces_region",
    "kernel_nonpositive_forces_hamming_negative",
    "kernel_nonpositive_forces_punctured_negative_of_high_degree",
    "kernel_nonpositive_forces_punctured_negative_of_low_degree",
    "kernel_nonpositive_forces_punctured_negative",
    "triple_nonpositive_iff_kernel_nonpositive",
}

CHECKS: list[tuple[str, bool]] = []


class AuditError(RuntimeError):
    """Raised when one audit gate fails."""


def check(name: str, condition: bool) -> None:
    passed = bool(condition)
    CHECKS.append((name, passed))
    if not passed:
        raise AuditError(name)


def read(relative: Path) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def file_sha256(relative: Path) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def object_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def norm_ws(value: str) -> str:
    return " ".join(value.split())


def note_scope_honest(text: str) -> bool:
    return (
        text.count(REPAIRED_INTEGRATION_BLOCK) == 1
        and text.count(REPAIRED_RESIDUAL_BLOCK) == 1
        and RETIRED_INTEGRATION_BLOCK not in text
        and RETIRED_RESIDUAL_BLOCK not in text
        and "pending upstream PR `#817`" not in text
        and "fixed-syndrome kernel denominator of pending PR" not in text
        and "treat pending PR `#817` as integrated" not in text
        and "pinned strict-JSON certificate" not in text
    )


def source_scope_honest(paving: str, pencil: str) -> bool:
    paving_normalized = norm_ws(paving)
    pencil_normalized = norm_ws(pencil)
    return (
        paving.count(CURRENT_SOURCE_MARKER) == 1
        and RETIRED_SOURCE_MARKER not in paving
        and "basis heaviness is automatic" in paving_normalized
        and "basis census therefore has no inverse content on its own"
        in paving_normalized
        and "distributed core pencils/design packing" in paving_normalized
        and "Consequently `beta` has no inverse content there"
        in pencil_normalized
        and "positive-depth affine-line family" in pencil_normalized
        and "no global common core" in pencil_normalized
        and "almost-Steiner agreement design" in pencil_normalized
    )


def lean_executable(text: str) -> str:
    without_blocks = re.sub(r"/-.*?-/", "", text, flags=re.DOTALL)
    return re.sub(r"--[^\n]*", "", without_blocks)


def run(
    relative: Path, *arguments: str, optimized: bool = False
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable, "-B"]
    if optimized:
        command.append("-O")
    command.extend([str(ROOT / relative), *arguments])
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


def passes(result: subprocess.CompletedProcess[str], *markers: str) -> bool:
    combined = output(result)
    return result.returncode == 0 and all(marker in combined for marker in markers)


def independent_scan(limit: int = 40) -> dict[str, int]:
    totals = {
        "eligible": 0,
        "nonpositive": 0,
        "zero": 0,
        "positive_depth": 0,
        "rho_t": 0,
        "rho_M": 0,
        "nonpositive_rho_t": 0,
        "nonpositive_rho_M": 0,
    }
    for N in range(2, limit + 1):
        for R in range(1, N):
            kappa = N - R
            for t in range(R):
                for direction_d in range(1, R + 1):
                    totals["eligible"] += 1
                    M = N - direction_d
                    rho = min(t, M)
                    deficiency = 2 * t - R
                    J_K = (N - t) ** 2 - N * (kappa - 1)
                    D_H = (N - t) ** 2 - N * M
                    D_J = (M - rho) ** 2 - M * (kappa - 1)
                    branch = "rho_t" if M >= t else "rho_M"
                    totals[branch] += 1
                    if J_K <= 0:
                        totals["nonpositive"] += 1
                        totals[f"nonpositive_{branch}"] += 1
                        if J_K == 0:
                            totals["zero"] += 1
                        if R - t - 1 >= 1:
                            totals["positive_depth"] += 1
                        if not (
                            D_H < 0
                            and D_J < 0
                            and kappa >= 2
                            and 2 <= deficiency < t
                            and D_H == J_K - N * (R - direction_d + 1)
                        ):
                            raise AuditError("independent denominator implication")
                        if M >= t:
                            if D_J != J_K - direction_d * (M - deficiency + 1):
                                raise AuditError("independent rho=t identity")
                        elif D_J != -M * (kappa - 1):
                            raise AuditError("independent rho=M identity")
    return totals


def source_bindings_fresh(certificate: dict[str, Any]) -> bool:
    rows = certificate.get("source_binding", [])
    expected_paths = {
        str(DIRECTION_NOTE),
        str(FIXED_DEFICIENCY_NOTE),
        str(PAVING_NOTE),
        str(DEPTH_ZERO_NOTE),
    }
    if not isinstance(rows, list) or {row.get("path") for row in rows} != expected_paths:
        return False
    for row in rows:
        relative = Path(row["path"])
        text = read(relative)
        lines = text.splitlines()
        if row.get("sha256") != file_sha256(relative):
            return False
        pins = row.get("pins", [])
        if not isinstance(pins, list) or len(pins) != 2:
            return False
        for pin in pins:
            marker = pin.get("marker")
            line_number = pin.get("line")
            if not isinstance(marker, str) or not isinstance(line_number, int):
                return False
            matches = [
                (index, line)
                for index, line in enumerate(lines, 1)
                if marker in line
            ]
            if len(matches) != 1 or matches[0][0] != line_number:
                return False
            if pin.get("line_sha256") != hashlib.sha256(
                matches[0][1].encode("utf-8")
            ).hexdigest():
                return False
    return True


def audit() -> None:
    check(
        "repaired packet and integrated source artifacts match SHA-256 pins",
        all(
            (ROOT / relative).is_file() and file_sha256(Path(relative)) == expected
            for relative, expected in SOURCE_SHA256.items()
        ),
    )
    check(
        "retired integrated packet hashes are distinct and fully pinned",
        set(RETIRED_SHA256) == {str(TRIPLE_NOTE), str(TRIPLE_SCRIPT), str(TRIPLE_CERT)}
        and all(len(value) == 64 for value in RETIRED_SHA256.values())
        and all(
            SOURCE_SHA256[relative] != retired
            for relative, retired in RETIRED_SHA256.items()
        ),
    )

    triple_note = read(TRIPLE_NOTE)
    check(
        "producer note records #823 as integrated rather than pending",
        note_scope_honest(triple_note)
        and "integrated PR `#823`, which covers\nPR `#817`" in triple_note
        and "use integrated PR `#823` to turn `J_K<=0`" in triple_note,
    )
    check(
        "producer note consumes #832's pencil/design correction",
        "PR `#832`, integrated in the same `168e9ba0` wave" in triple_note
        and "basis heaviness has no\ninverse content" in triple_note
        and "lies outside `J_K<=0`" in triple_note
        and "does not follow from basis heaviness" in triple_note,
    )

    paving = read(PAVING_NOTE)
    pencil = read(PENCIL_NOTE)
    check(
        "current paving and pencil sources reject the retired basis-heavy inverse",
        source_scope_honest(paving, pencil),
    )

    certificate = json.loads(read(TRIPLE_CERT))
    unsigned = copy.deepcopy(certificate)
    claimed_payload = unsigned.pop("payload_sha256")
    check(
        "repaired certificate schema, status, and canonical payload are fresh",
        certificate.get("schema")
        == "rs-mca-triple-negative-first-match-reduction-v1"
        and certificate.get("theorem_id")
        == "triple-negative-first-match-reduction"
        and certificate.get("status")
        == "PROVED ARITHMETIC REDUCTION / AUDITED COUNTING SYNTHESIS"
        and claimed_payload == TRIPLE_PAYLOAD
        and object_sha256(unsigned) == TRIPLE_PAYLOAD,
    )
    check(
        "all four certificate source bindings match current files and unique lines",
        source_bindings_fresh(certificate),
    )
    synthesis = certificate.get("complete_pair_synthesis", {})
    nonclaims = certificate.get("nonclaims", [])
    check(
        "certificate records integrated provenance and the corrected residual",
        synthesis.get("remaining_wall") == CURRENT_REMAINING_WALL
        and CURRENT_NONCLAIM in nonclaims
        and all("pending fixed-slope" not in item for item in nonclaims)
        and "basis-heavy" not in synthesis.get("remaining_wall", ""),
    )

    lean = read(TRIPLE_LEAN)
    declarations = set(
        re.findall(
            r"^(?:def|theorem)\s+([A-Za-z0-9_]+)",
            lean,
            flags=re.MULTILINE,
        )
    )
    executable = lean_executable(lean)
    check(
        "Lean declaration surface is the arithmetic reduction only",
        declarations == EXPECTED_DECLARATIONS
        and not re.search(r"\b(?:sorry|admit|axiom|unsafe)\b", executable)
        and "not the\nalready-proved external counting theorems" in triple_note,
    )

    check(
        "independent N<=40 scan recovers both branches and every strict boundary",
        independent_scan()
        == {
            "eligible": 213_200,
            "nonpositive": 48_012,
            "zero": 447,
            "positive_depth": 38_375,
            "rho_t": 165_130,
            "rho_M": 48_070,
            "nonpositive_rho_t": 30_121,
            "nonpositive_rho_M": 17_891,
        },
    )

    triple_normal = run(TRIPLE_SCRIPT, "--check")
    triple_optimized = run(TRIPLE_SCRIPT, "--check", optimized=True)
    check(
        "repaired producer passes normal and optimized certificate replay",
        passes(triple_normal, "triple-negative-first-match-reduction: PASS", TRIPLE_PAYLOAD)
        and passes(
            triple_optimized,
            "triple-negative-first-match-reduction: PASS",
            TRIPLE_PAYLOAD,
        ),
    )
    triple_tamper = run(TRIPLE_SCRIPT, "--tamper-selftest")
    triple_tamper_optimized = run(
        TRIPLE_SCRIPT, "--tamper-selftest", optimized=True
    )
    check(
        "repaired producer rejects 10/10 mutations in both modes",
        passes(triple_tamper, "tamper_mutations_rejected=10", TRIPLE_PAYLOAD)
        and passes(
            triple_tamper_optimized,
            "tamper_mutations_rejected=10",
            TRIPLE_PAYLOAD,
        ),
    )

    fixed_normal = run(FIXED_SLOPE_SCRIPT, "--check")
    fixed_optimized = run(FIXED_SLOPE_SCRIPT, "--check", optimized=True)
    fixed_tamper = run(FIXED_SLOPE_SCRIPT, "--tamper-selftest")
    fixed_tamper_optimized = run(
        FIXED_SLOPE_SCRIPT, "--tamper-selftest", optimized=True
    )
    check(
        "integrated #823 fixed-slope source replays and rejects 10/10 mutations",
        passes(fixed_normal, "fixed-slope-kernel-johnson-multiplicity: PASS",
               FIXED_SLOPE_PAYLOAD)
        and passes(
            fixed_optimized,
            "fixed-slope-kernel-johnson-multiplicity: PASS",
            FIXED_SLOPE_PAYLOAD,
        )
        and passes(fixed_tamper, "tamper_mutations_rejected=10")
        and passes(fixed_tamper_optimized, "tamper_mutations_rejected=10"),
    )

    pencil_normal = run(PENCIL_SCRIPT, "--check")
    pencil_optimized = run(PENCIL_SCRIPT, "--check", optimized=True)
    pencil_tamper = run(PENCIL_SCRIPT, "--tamper-selftest")
    pencil_tamper_optimized = run(
        PENCIL_SCRIPT, "--tamper-selftest", optimized=True
    )
    check(
        "integrated #832 pencil source replays and rejects 10/10 mutations",
        passes(pencil_normal, "VERIFICATION PASS", PENCIL_PAYLOAD)
        and passes(pencil_optimized, "VERIFICATION PASS", PENCIL_PAYLOAD)
        and passes(pencil_tamper, "TAMPER SELFTEST PASS: 10/10")
        and passes(pencil_tamper_optimized, "TAMPER SELFTEST PASS: 10/10"),
    )

    check(
        "isolated retired note and source regressions are rejected",
        triple_note.count(REPAIRED_INTEGRATION_BLOCK) == 1
        and triple_note.count(REPAIRED_RESIDUAL_BLOCK) == 1
        and not note_scope_honest(
            triple_note.replace(
                REPAIRED_INTEGRATION_BLOCK, RETIRED_INTEGRATION_BLOCK
            )
        )
        and not note_scope_honest(
            triple_note.replace(REPAIRED_RESIDUAL_BLOCK, RETIRED_RESIDUAL_BLOCK)
        )
        and not source_scope_honest(
            paving.replace(CURRENT_SOURCE_MARKER, RETIRED_SOURCE_MARKER), pencil
        ),
    )

    lean_root = read(LEAN_ROOT)
    lean_readme = read(LEAN_README)
    lean_summary = read(LEAN_SUMMARY)
    check(
        "package consumers import one arithmetic module and claim no counting API",
        lean_root.count("import GrandeFinale.TripleNegativeFirstMatchReduction") == 1
        and lean_readme.count(
            "`GrandeFinale/TripleNegativeFirstMatchReduction.lean` formalizes"
        )
        == 1
        and lean_summary.count(
            "`GrandeFinale/TripleNegativeFirstMatchReduction.lean`: triple-negative"
        )
        == 1
        and "theorem triple_nonpositive_iff_kernel_nonpositive" in lean,
    )


def main() -> int:
    if sys.argv[1:] not in ([], ["--check"]):
        print(
            "usage: verify_triple_negative_first_match_correspondence_audit.py "
            "[--check]",
            file=sys.stderr,
        )
        return 2
    try:
        audit()
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        print(f"integration: {INTEGRATION}")
        print(f"triple_pr_head: {TRIPLE_PR_HEAD}")
        print(f"fixed_slope_pr_head: {FIXED_SLOPE_PR_HEAD}")
        print(f"pencil_pr_head: {PENCIL_PR_HEAD}")
        print(f"producer_payload_sha256: {TRIPLE_PAYLOAD}")
        print(f"RESULT: PASS ({len(CHECKS)}/{len(CHECKS)})")
        print("STATUS: COUNTEREXAMPLE")
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
        print("STATUS: COUNTEREXAMPLE")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
