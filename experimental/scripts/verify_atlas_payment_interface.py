#!/usr/bin/env python3
"""Verify the prefix-atlas coverage/payment interface audit.

This stdlib-only verifier checks repository text and Lean declaration anchors,
then records a small exact negative control.  It intentionally does not infer
payment from coverage: the checked Lean bridge carries its cellwise budgets as
an explicit hypothesis.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Callable, Mapping


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "experimental/data/certificates/atlas-payment-interface/atlas_payment_interface.json"

PREFIX_ATLAS = "experimental/lean/asymptotic_spine/AsymptoticSpine/PrefixAtlas.lean"
PREFIX_BRIDGE = "experimental/lean/grande_finale/GrandeFinale/PrefixAtlasBridge.lean"
FIRST_MATCH_WITNESS_BRIDGE = (
    "experimental/lean/grande_finale/GrandeFinale/FirstMatchWitnessBridge.lean"
)
RS_EXACT_CARD_WITNESS_BRIDGE = (
    "experimental/lean/grande_finale/GrandeFinale/RSExactCardWitnessBridge.lean"
)
RS_EXACT_CARD_PREFIX_WITNESS_BRIDGE = (
    "experimental/lean/grande_finale/GrandeFinale/"
    "RSExactCardPrefixWitnessBridge.lean"
)
RS_EXACT_CARD_OCCUPANCY_BRIDGE = (
    "experimental/lean/grande_finale/GrandeFinale/"
    "RSExactCardOccupancyBridge.lean"
)
RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE = (
    "experimental/lean/grande_finale/GrandeFinale/"
    "RSExactCardBoundaryPaymentBridge.lean"
)
ATLAS_LEDGER = "experimental/notes/thresholds/atlas_cat_cell_ledger.md"
C3_CENSUS = "experimental/notes/thresholds/c3_planted_divisor_census.md"
FRONTIERS_TEX = "experimental/asymptotic_rs_mca_frontiers.tex"
HEAVY_FIBER = "experimental/notes/thresholds/heavy_fiber_admissibility_transfer.md"
VERIFIER_SCRIPT = "experimental/scripts/verify_atlas_payment_interface.py"
AUDIT_DOCUMENT = "experimental/notes/audits/atlas_payment_interface_audit.md"
CORRESPONDENCE_DOCUMENT = "experimental/lean/grande_finale/PREFIX_ATLAS_BRIDGE_CORRESPONDENCE.md"
THRESHOLD_NOTES = ROOT / "experimental/notes/thresholds"


class AuditError(RuntimeError):
    """Raised when a semantic source anchor is absent or inconsistent."""


class Audit:
    def __init__(self) -> None:
        self.checks: list[str] = []

    def require(self, condition: bool, label: str) -> None:
        if not condition:
            raise AuditError(f"failed check: {label}")
        self.checks.append(label)


def normalized(text: str) -> str:
    return " ".join(text.split())


def lean_code_without_comments(text: str) -> str:
    """Blank Lean comments and strings while preserving line structure."""

    code: list[str] = []
    block_depth = 0
    line_comment = False
    in_string = False
    escaped = False
    index = 0
    while index < len(text):
        char = text[index]
        pair = text[index : index + 2]

        if line_comment:
            if char == "\n":
                line_comment = False
                code.append("\n")
            else:
                code.append(" ")
            index += 1
            continue

        if block_depth:
            if pair == "/-":
                block_depth += 1
                code.extend((" ", " "))
                index += 2
            elif pair == "-/":
                block_depth -= 1
                code.extend((" ", " "))
                index += 2
            else:
                code.append("\n" if char == "\n" else " ")
                index += 1
            continue

        if in_string:
            code.append("\n" if char == "\n" else " ")
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if pair == "--":
            line_comment = True
            code.extend((" ", " "))
            index += 2
        elif pair == "/-":
            block_depth = 1
            code.extend((" ", " "))
            index += 2
        elif char == '"':
            in_string = True
            code.append(" ")
            index += 1
        else:
            code.append(char)
            index += 1

    return "".join(code)


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def line_of(text: str, needle: str) -> int:
    position = text.find(needle)
    if position < 0:
        raise AuditError(f"missing line anchor: {needle!r}")
    return text.count("\n", 0, position) + 1


def read_source(relative: str, overrides: Mapping[str, str]) -> str:
    if relative in overrides:
        return overrides[relative]
    return (ROOT / relative).read_text(encoding="utf-8")


def declaration_lines(text: str) -> dict[str, int]:
    code = lean_code_without_comments(text)
    declarations: dict[str, int] = {}
    pattern = re.compile(r"^(?:noncomputable\s+)?(?:def|theorem)\s+([A-Za-z0-9_']+)", re.MULTILINE)
    for match in pattern.finditer(code):
        declarations[match.group(1)] = code.count("\n", 0, match.start()) + 1
    return declarations


def theorem_signature(text: str, name: str) -> tuple[str, int]:
    code = lean_code_without_comments(text)
    matches = list(
        re.finditer(
            rf"^theorem\s+{re.escape(name)}\b",
            code,
            re.MULTILINE,
        )
    )
    if len(matches) != 1:
        raise AuditError(f"expected exactly one theorem declaration for {name}")
    start = matches[0].start()
    end = code.find(":= by", start)
    if end < 0:
        raise AuditError(f"missing proof boundary for theorem {name}")
    return (
        normalized(code[start:end]),
        code.count("\n", 0, start) + 1,
    )


def audit_prefix_atlas(text: str, audit: Audit) -> dict[str, object]:
    flat = normalized(text)
    declarations = declaration_lines(text)
    required = [
        "fibreAtlas",
        "mem_fibreAtlas_flatten_iff",
        "nodup_fibreAtlas_flatten",
        "realizedKeys",
        "realizedKeys_nodup",
        "totalFibreAtlas",
        "prefixFibreAtlas_total_of_keys",
        "totalFibreAtlas_cells_nonempty",
        "prefixFibreAtlas_total",
    ]
    for name in required:
        audit.require(name in declarations, f"PrefixAtlas declaration {name}")

    separation = (
        "Coverage and payment remain separate: a total key map partitions every witness, "
        "while any numerical payment for the resulting cells is an independent input."
    )
    profile_boundary = (
        "Only the profile-count bound is supplied separately; coverage has no atlas assumption."
    )
    audit.require(separation in flat, "PrefixAtlas coverage/payment separation")
    audit.require("No payment theorem is used." in flat, "PrefixAtlas payment nonclaim")
    audit.require(profile_boundary in flat, "PrefixAtlas supplied profile-count boundary")
    audit.require(
        "firstMatchLeaves [] (totalFibreAtlas witnesses key)" in flat,
        "PrefixAtlas first-match totality conclusion",
    )

    return {
        "path": PREFIX_ATLAS,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "coverage_payment_separation_line": line_of(text, "Coverage and payment remain separate"),
        "payment_nonclaim_line": line_of(text, "No payment theorem is used."),
        "verified_claim": "total key fibres give witness-exhaustive first-match coverage",
        "verified_nonclaim": "coverage supplies neither cell payment nor a payment theorem",
    }


def audit_prefix_bridge(text: str, audit: Audit) -> dict[str, object]:
    flat = normalized(text)
    declarations = declaration_lines(text)
    required = [
        "supportPrefixKey",
        "supportPrefixCell",
        "mem_supportPrefixCell_iff",
        "supportPrefixCells_cover",
        "supportPrefixKey_space_card",
        "coefficientFiber_biUnion_eq_powersetCard",
        "prefixBadSlopeCell",
        "badSlopeSetOnPowersetCard_eq_prefixCells_biUnion",
        "badSlopeSetOnPowersetCard_card_le_sum_prefixCells",
        "badSlopeSetOnSupportFamily_eq_prefixCells_biUnion",
        "badSlopeSetOnSupportFamily_card_le_sum_prefixCells",
        "badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets",
        "rsPrefixBadSlopeCell",
        "rsMcaBadSlopes_eq_prefixCells_biUnion",
        "rsMcaBadSlopes_card_le_sum_prefixCells",
        "rsMcaBadSlopes_card_le_sum_prefixBudgets",
        "B_MCA_rsEval_le_of_linewise_prefixBudgets",
        "B_MCA_rsEval_le_sum_prefixBudgets",
    ]
    for name in required:
        audit.require(name in declarations, f"PrefixAtlasBridge declaration {name}")

    expected_payment_signatures = {
        "badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets": (
            "theorem badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets "
            "(H : (D → F) →ₗ[F] W) (point : D -> F) "
            "(supports : Finset (Finset D)) (K m : Nat) (u0 u1 : D -> F) "
            "(U : (Fin (m - K) -> F) -> Nat) "
            "(hU : ∀ z, (SyndromeLine.badSlopeSetOnSupportFamily H "
            "(supportPrefixCell point supports K m z) u0 u1).card ≤ U z) : "
            "(SyndromeLine.badSlopeSetOnSupportFamily H supports u0 u1).card ≤ ∑ z, U z"
        ),
        "rsMcaBadSlopes_card_le_sum_prefixBudgets": (
            "theorem rsMcaBadSlopes_card_le_sum_prefixBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k R : Nat) (hsize : k + R = Fintype.card D) "
            "(a K : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F) "
            "(U : (Fin (a - K) -> F) -> Nat) "
            "(hU : ∀ z, (rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z) : "
            "(Finset.univ.filter (fun gamma : F => GrandeFinale.MCABad "
            "(CollisionAwarePole.rsEval ev k : Set (D -> F)) u0 u1 a gamma)).card ≤ ∑ z, U z"
        ),
        "B_MCA_rsEval_le_of_linewise_prefixBudgets": (
            "theorem B_MCA_rsEval_le_of_linewise_prefixBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k R : Nat) (hsize : k + R = Fintype.card D) "
            "(a K : Nat) (hka : k + 1 ≤ a) "
            "(U : (D -> F) -> (D -> F) -> (Fin (a - K) -> F) -> Nat) "
            "(B : Nat) (hcell : ∀ u0 u1 z, "
            "(rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U u0 u1 z) "
            "(hunif : ∀ u0 u1, ∑ z, U u0 u1 z ≤ B) : "
            "GrandeFinale.B_MCA (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ B"
        ),
        "B_MCA_rsEval_le_sum_prefixBudgets": (
            "theorem B_MCA_rsEval_le_sum_prefixBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k R : Nat) (hsize : k + R = Fintype.card D) "
            "(a K : Nat) (hka : k + 1 ≤ a) "
            "(U : (Fin (a - K) -> F) -> Nat) "
            "(hU : ∀ (u0 u1 : D -> F) z, "
            "(rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z) : "
            "GrandeFinale.B_MCA (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ ∑ z, U z"
        ),
    }
    payment_signatures: dict[str, object] = {}
    for name, expected in expected_payment_signatures.items():
        actual, theorem_line = theorem_signature(text, name)
        audit.require(
            actual == expected,
            f"PrefixAtlasBridge exact payment signature {name}",
        )
        payment_signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }

    lean_code = lean_code_without_comments(text)
    forbidden_syntax = {
        "any sorry token": re.compile(
            r"\bsorry\b", re.MULTILINE
        ),
        "any admit token": re.compile(
            r"\badmit\b", re.MULTILINE
        ),
        "same-line proof sorry": re.compile(
            r":=[ \t]*by[ \t]+sorry(?:[ \t]*(?:--[^\n]*)?)?$", re.MULTILINE
        ),
        "same-line proof admit": re.compile(
            r":=[ \t]*by[ \t]+admit(?:[ \t]*(?:--[^\n]*)?)?$", re.MULTILINE
        ),
        "explicit axiom declaration": re.compile(
            r"^[ \t]*axiom[ \t]+[A-Za-z_]", re.MULTILINE
        ),
        "opaque declaration": re.compile(
            r"^[ \t]*opaque[ \t]+[A-Za-z_]", re.MULTILINE
        ),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"PrefixAtlasBridge rejects {label}",
        )

    axiom_print_names = list(expected_payment_signatures)
    for name in axiom_print_names:
        audit.require(
            re.search(
                rf"^#print axioms {re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"PrefixAtlasBridge #print axioms {name}",
        )

    fixed_row_comment = (
        "Exact fixed-row outer-line interface: prefix-cell budgets may depend "
        "on the received line; only their sum must have a bound uniform over "
        "lines in this row."
    )
    audit.require(
        fixed_row_comment in flat,
        "PrefixAtlasBridge frozen fixed-row comment wording",
    )
    audit.require(
        "import GrandeFinale.PrefixPigeonhole" in text
        and "import GrandeFinale.SyndromeLine" in text,
        "PrefixAtlasBridge concrete imports",
    )
    explicit_budget = (
        "(hU : ∀ z, (SyndromeLine.badSlopeSetOnSupportFamily H "
        "(supportPrefixCell point supports K m z) u0 u1).card ≤ U z)"
    )
    audit.require(explicit_budget in flat, "PrefixAtlasBridge explicit cellwise budget hypothesis")
    audit.require(
        "(SyndromeLine.badSlopeSetOnSupportFamily H supports u0 u1).card ≤ ∑ z, U z" in flat,
        "PrefixAtlasBridge summed budget conclusion",
    )
    audit.require(
        "The hypotheses are the missing payment input; coverage alone does not construct them." in flat,
        "PrefixAtlasBridge missing-payment boundary",
    )
    audit.require(
        "Prefix totality does not prove a profile count, a first-match catalogue classification, "
        "or a numerical payment." in flat,
        "PrefixAtlasBridge top-level nonclaim",
    )
    audit.require(
        "The source convention is `K := k+1`, giving depth `a-k-1`." in flat,
        "PrefixAtlasBridge RS source-depth convention",
    )
    audit.require(
        "(hU : ∀ z, (rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z)" in flat,
        "PrefixAtlasBridge RS explicit cellwise budget hypothesis",
    )
    audit.require(
        "The theorem does not construct the budgets." in flat,
        "PrefixAtlasBridge RS budget nonclaim",
    )
    linewise_start = text.find("theorem B_MCA_rsEval_le_of_linewise_prefixBudgets")
    linewise_end = text.find(":= by", linewise_start)
    audit.require(
        linewise_start >= 0 and linewise_end > linewise_start,
        "PrefixAtlasBridge fixed-row outer-line signature bounds",
    )
    linewise_signature = normalized(text[linewise_start:linewise_end])
    linewise_budget_type = (
        "(U : (D -> F) -> (D -> F) -> (Fin (a - K) -> F) -> Nat)"
    )
    linewise_cell = (
        "(hcell : ∀ u0 u1 z, "
        "(rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U u0 u1 z)"
    )
    linewise_uniform = "(hunif : ∀ u0 u1, ∑ z, U u0 u1 z ≤ B)"
    linewise_output = (
        "GrandeFinale.B_MCA (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ B"
    )
    audit.require(
        linewise_budget_type in linewise_signature,
        "PrefixAtlasBridge linewise budget type",
    )
    audit.require(
        linewise_cell in linewise_signature,
        "PrefixAtlasBridge linewise cell hypothesis",
    )
    audit.require(
        linewise_uniform in linewise_signature,
        "PrefixAtlasBridge summed uniformity hypothesis",
    )
    audit.require(
        linewise_output in linewise_signature,
        "PrefixAtlasBridge fixed-row outer-line conclusion",
    )
    audit.require(
        "(hU :" not in linewise_signature,
        "PrefixAtlasBridge fixed-row interface has no line-independent cell budget",
    )
    line_uniform_budget = (
        "(hU : ∀ (u0 u1 : D -> F) z, "
        "(rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z)"
    )
    audit.require(
        line_uniform_budget in flat,
        "PrefixAtlasBridge B_MCA line-uniform budget hypothesis",
    )
    audit.require(
        "GrandeFinale.B_MCA (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ ∑ z, U z"
        in flat,
        "PrefixAtlasBridge B_MCA summed budget conclusion",
    )

    return {
        "path": PREFIX_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "payment_interface_signatures": payment_signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [
            f"#print axioms {name}" for name in axiom_print_names
        ],
        "fixed_row_comment_line": line_of(
            text, "Exact fixed-row outer-line interface"
        ),
        "fixed_row_comment_sha256": digest(fixed_row_comment),
        "coverage_theorem_line": declarations["supportPrefixCells_cover"],
        "bad_slope_union_theorem_line": declarations[
            "badSlopeSetOnSupportFamily_eq_prefixCells_biUnion"
        ],
        "payment_interface_theorem_line": declarations[
            "badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets"
        ],
        "rs_bad_slope_union_theorem_line": declarations[
            "rsMcaBadSlopes_eq_prefixCells_biUnion"
        ],
        "rs_payment_interface_theorem_line": declarations[
            "rsMcaBadSlopes_card_le_sum_prefixBudgets"
        ],
        "b_mca_linewise_payment_interface_theorem_line": declarations[
            "B_MCA_rsEval_le_of_linewise_prefixBudgets"
        ],
        "b_mca_payment_interface_theorem_line": declarations[
            "B_MCA_rsEval_le_sum_prefixBudgets"
        ],
        "payment_input": "for every concrete prefix key z, bad-slope-card(cell z) <= U(z)",
        "payment_output": "bad-slope-card(full support family) <= sum_z U(z)",
        "line_uniform_payment_input": (
            "one U(z) bounds every locator-prefix cell for every received-line pair (u0,u1)"
        ),
        "line_uniform_payment_output": "B_MCA(rsEval(ev,k),a) <= sum_z U(z)",
        "linewise_payment_input": (
            "hcell bounds each cell by U(u0,u1,z); hunif bounds only each linewise sum by B"
        ),
        "linewise_payment_output": "B_MCA(rsEval(ev,k),a) <= B",
        "linewise_signature_sha256": digest(linewise_signature),
        "verified_nonclaim": "the bridge constructs no U and proves no catalogue/profile payment",
    }


def audit_first_match_witness_bridge(
    text: str, audit: Audit
) -> dict[str, object]:
    flat = normalized(text)
    lean_code = lean_code_without_comments(text)
    declarations = declaration_lines(text)
    required = [
        "firstMatchSlopeCell",
        "firstMatchResidualWitnessCell",
        "firstMatchResidualWitnessCell_image_slope",
        "B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets",
        "B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets",
        "slopeImage_cover_not_witnessExhaustive",
        "firstMatchResidualWitnessCells_not_witnessExhaustive",
    ]
    for name in required:
        audit.require(
            name in declarations,
            f"FirstMatchWitnessBridge declaration {name}",
        )

    expected_signatures = {
        "firstMatchResidualWitnessCell_image_slope": (
            "theorem firstMatchResidualWitnessCell_image_slope "
            "(idx : Finset ι) (cell : ι -> Finset ω) "
            "(slope : ω -> σ) (i : ι) : "
            "(firstMatchResidualWitnessCell idx cell slope i).image slope = "
            "firstMatchSlopeCell idx cell slope i"
        ),
        "B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets": (
            "theorem B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets "
            "(C : Set (D -> F)) (a : Nat) "
            "(witnesses : ((D -> F) × (D -> F)) -> Finset ω) "
            "(slope : ω -> F) "
            "(idx : ((D -> F) × (D -> F)) -> Finset ι) "
            "(cell : ((D -> F) × (D -> F)) -> ι -> Finset ω) "
            "(U : ((D -> F) × (D -> F)) -> ι -> Nat) "
            "(hbadImage : ∀ p, Finset.univ.filter (fun gamma : F => "
            "GrandeFinale.MCABad C p.1 p.2 a gamma) = "
            "(witnesses p).image slope) "
            "(hexhaust : ∀ p, (idx p).biUnion (cell p) = witnesses p) "
            "(hcell : ∀ p i, i ∈ idx p -> "
            "(firstMatchSlopeCell (idx p) (cell p) slope i).card ≤ U p i) : "
            "GrandeFinale.B_MCA C a ≤ "
            "Finset.univ.sup (fun p : (D -> F) × (D -> F) => "
            "∑ i ∈ idx p, U p i)"
        ),
        "B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets": (
            "theorem B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets "
            "(C : Set (D -> F)) (a B : Nat) "
            "(witnesses : ((D -> F) × (D -> F)) -> Finset ω) "
            "(slope : ω -> F) "
            "(idx : ((D -> F) × (D -> F)) -> Finset ι) "
            "(cell : ((D -> F) × (D -> F)) -> ι -> Finset ω) "
            "(U : ((D -> F) × (D -> F)) -> ι -> Nat) "
            "(hbadImage : ∀ p, Finset.univ.filter (fun gamma : F => "
            "GrandeFinale.MCABad C p.1 p.2 a gamma) = "
            "(witnesses p).image slope) "
            "(hexhaust : ∀ p, (idx p).biUnion (cell p) = witnesses p) "
            "(hcell : ∀ p i, i ∈ idx p -> "
            "(firstMatchSlopeCell (idx p) (cell p) slope i).card ≤ U p i) "
            "(hunif : ∀ p, ∑ i ∈ idx p, U p i ≤ B) : "
            "GrandeFinale.B_MCA C a ≤ B"
        ),
        "slopeImage_cover_not_witnessExhaustive": (
            "theorem slopeImage_cover_not_witnessExhaustive : "
            "let witnesses : Finset (Fin 2) := Finset.univ "
            "let chosen : Finset (Fin 2) := {0} "
            "let slope : Fin 2 -> Fin 1 := fun _ => 0 "
            "chosen ⊆ witnesses ∧ chosen ≠ witnesses ∧ "
            "chosen.image slope = witnesses.image slope"
        ),
        "firstMatchResidualWitnessCells_not_witnessExhaustive": (
            "theorem firstMatchResidualWitnessCells_not_witnessExhaustive : "
            "let witnesses : Finset (Fin 2) := Finset.univ "
            "let idx : Finset (Fin 2) := Finset.univ "
            "let cell : Fin 2 -> Finset (Fin 2) := fun i => "
            "if i = 0 then {0} else {1} "
            "let slope : Fin 2 -> Fin 1 := fun _ => 0 "
            "idx.biUnion cell = witnesses ∧ "
            "idx.biUnion "
            "(firstMatchResidualWitnessCell idx cell slope) ≠ witnesses ∧ "
            "idx.biUnion (firstMatchSlopeCell idx cell slope) = "
            "witnesses.image slope"
        ),
    }
    signatures: dict[str, object] = {}
    for name, expected in expected_signatures.items():
        actual, theorem_line = theorem_signature(text, name)
        audit.require(
            actual == expected,
            f"FirstMatchWitnessBridge exact signature {name}",
        )
        signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }

    forbidden_syntax = {
        "any sorry token": re.compile(r"\bsorry\b"),
        "any admit token": re.compile(r"\badmit\b"),
        "any axiom token": re.compile(r"\baxiom\b"),
        "any opaque token": re.compile(r"\bopaque\b"),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"FirstMatchWitnessBridge rejects {label}",
        )

    axiom_print_names = list(expected_signatures)
    for name in axiom_print_names:
        audit.require(
            re.search(
                rf"^#print axioms {re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"FirstMatchWitnessBridge #print axioms {name}",
        )

    projection_boundary = (
        "First match is performed after projecting witnesses to slopes. "
        "The residual witness cell selects witnesses realizing the slopes "
        "assigned to a cell; its slope image is exact, but its union need not "
        "exhaust the original witnesses when distinct witnesses share a slope. "
        "Every catalogue, projection identity, first-match slope budget, and "
        "uniform sum below is an explicit hypothesis. No concrete Reed--Solomon "
        "atlas, prefix classification, or payment is claimed."
    )
    residual_boundary = (
        "These residual cells are not asserted to cover all witnesses."
    )
    raw_countermodel_boundary = (
        "Exact `Fin 2 -> Fin 1` countermodel: a proper subset of the witnesses "
        "can have exactly the same slope image as the full witness family."
    )
    residual_countermodel_boundary = (
        "Exact `Fin 2 -> Fin 1` countermodel: the original witness cells cover "
        "all witnesses, but slope-level first match retains only one of two "
        "distinct witnesses sharing the same slope."
    )
    for label, boundary in (
        ("projection boundary", projection_boundary),
        ("residual-cell noncoverage", residual_boundary),
        ("raw slope-image countermodel", raw_countermodel_boundary),
        ("residual-cell countermodel", residual_countermodel_boundary),
    ):
        audit.require(
            boundary in flat,
            f"FirstMatchWitnessBridge {label}",
        )

    return {
        "path": FIRST_MATCH_WITNESS_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "witness_interface_signatures": signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [
            f"#print axioms {name}" for name in axiom_print_names
        ],
        "projection_boundary_line": line_of(
            text, "First match is performed after projecting witnesses to slopes."
        ),
        "residual_noncoverage_line": line_of(
            text, "These residual cells are not asserted to cover all witnesses."
        ),
        "raw_countermodel_line": declarations[
            "slopeImage_cover_not_witnessExhaustive"
        ],
        "residual_countermodel_line": declarations[
            "firstMatchResidualWitnessCells_not_witnessExhaustive"
        ],
        "verified_claim": (
            "witness exhaustion plus exact bad-slope image and cell budgets "
            "bounds B_MCA; a uniform sum bound gives B_MCA <= B"
        ),
        "verified_boundary": (
            "slope-image coverage does not imply witness coverage, and "
            "slope-level first match need not preserve witness exhaustion"
        ),
        "verified_nonclaim": (
            "the bridge constructs no catalogue, bad-image identity, budget, "
            "uniformity certificate, Reed-Solomon classification, or payment"
        ),
    }


def audit_rs_exact_card_witness_bridge(
    text: str, audit: Audit
) -> dict[str, object]:
    flat = normalized(text)
    lean_code = lean_code_without_comments(text)
    declarations = declaration_lines(text)
    required = [
        "ValidRSExactCardWitness",
        "rsExactCardWitnesses",
        "explanation_eq_of_valid_of_slope_eq_support_eq",
        "slope_support_projection_injOn_validRSExactCardWitness",
        "rsMcaBadSlopes_eq_exactCardWitnessSlopeImage",
        "B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets",
        "B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets",
    ]
    for name in required:
        audit.require(
            name in declarations,
            f"RSExactCardWitnessBridge declaration {name}",
        )

    structure_anchor = (
        "structure RSExactCardWitness (D F : Type*) (k : Nat) where "
        "slope : F support : Finset D coeffs : Fin k -> F "
        "deriving Fintype, DecidableEq"
    )
    predicate_anchor = (
        "w.support.card = a ∧ "
        "(∀ d ∈ w.support, "
        "w.explanation.eval (ev d) = u0 d + w.slope * u1 d) ∧ "
        "¬ GrandeFinale.ExplainedPair (rsEval ev k : Set (D -> F)) "
        "u0 u1 w.support"
    )
    audit.require(
        structure_anchor in flat,
        "RSExactCardWitnessBridge finite coefficient-vector structure",
    )
    audit.require(
        predicate_anchor in flat,
        "RSExactCardWitnessBridge exact-cardinality witness predicate",
    )

    expected_signatures = {
        "RSExactCardWitness.explanation_degree_lt": (
            "theorem RSExactCardWitness.explanation_degree_lt "
            "{D F : Type*} [Semiring F] {k : Nat} "
            "(w : RSExactCardWitness D F k) : "
            "w.explanation.degree < (k : WithBot Nat)"
        ),
        "explanation_eq_of_valid_of_slope_eq_support_eq": (
            "theorem explanation_eq_of_valid_of_slope_eq_support_eq "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a : Nat) (hka : k ≤ a) (u0 u1 : D -> F) "
            "{w w' : RSExactCardWitness D F k} "
            "(hw : ValidRSExactCardWitness ev k a u0 u1 w) "
            "(hw' : ValidRSExactCardWitness ev k a u0 u1 w') "
            "(hslope : w.slope = w'.slope) "
            "(hsupport : w.support = w'.support) : "
            "w.explanation = w'.explanation"
        ),
        "slope_support_projection_injOn_validRSExactCardWitness": (
            "theorem slope_support_projection_injOn_validRSExactCardWitness "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a : Nat) (hka : k ≤ a) (u0 u1 : D -> F) : "
            "Set.InjOn "
            "(fun w : RSExactCardWitness D F k => (w.slope, w.support)) "
            "{w | ValidRSExactCardWitness ev k a u0 u1 w}"
        ),
        "rsMcaBadSlopes_eq_exactCardWitnessSlopeImage": (
            "theorem rsMcaBadSlopes_eq_exactCardWitnessSlopeImage "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F) : "
            "Finset.univ.filter (fun gamma : F => "
            "GrandeFinale.MCABad (rsEval ev k : Set (D -> F)) "
            "u0 u1 a gamma) = "
            "(rsExactCardWitnesses ev k a u0 u1).image "
            "RSExactCardWitness.slope"
        ),
        "B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets": (
            "theorem "
            "B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a : Nat) (hka : k + 1 ≤ a) "
            "(idx : ((D -> F) × (D -> F)) -> Finset ι) "
            "(cell : ((D -> F) × (D -> F)) -> ι -> "
            "Finset (RSExactCardWitness D F k)) "
            "(U : ((D -> F) × (D -> F)) -> ι -> Nat) "
            "(hexhaust : ∀ p, (idx p).biUnion (cell p) = "
            "rsExactCardWitnesses ev k a p.1 p.2) "
            "(hcell : ∀ p i, i ∈ idx p -> "
            "(firstMatchSlopeCell (idx p) (cell p) "
            "RSExactCardWitness.slope i).card ≤ U p i) : "
            "GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤ "
            "Finset.univ.sup (fun p : (D -> F) × (D -> F) => "
            "∑ i ∈ idx p, U p i)"
        ),
        "B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets": (
            "theorem "
            "B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a B : Nat) (hka : k + 1 ≤ a) "
            "(idx : ((D -> F) × (D -> F)) -> Finset ι) "
            "(cell : ((D -> F) × (D -> F)) -> ι -> "
            "Finset (RSExactCardWitness D F k)) "
            "(U : ((D -> F) × (D -> F)) -> ι -> Nat) "
            "(hexhaust : ∀ p, (idx p).biUnion (cell p) = "
            "rsExactCardWitnesses ev k a p.1 p.2) "
            "(hcell : ∀ p i, i ∈ idx p -> "
            "(firstMatchSlopeCell (idx p) (cell p) "
            "RSExactCardWitness.slope i).card ≤ U p i) "
            "(hunif : ∀ p, ∑ i ∈ idx p, U p i ≤ B) : "
            "GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤ B"
        ),
    }
    signatures: dict[str, object] = {}
    for name, expected in expected_signatures.items():
        actual, theorem_line = theorem_signature(text, name)
        audit.require(
            actual == expected,
            f"RSExactCardWitnessBridge exact signature {name}",
        )
        signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }

    forbidden_syntax = {
        "any sorry token": re.compile(r"\bsorry\b"),
        "any admit token": re.compile(r"\badmit\b"),
        "any axiom token": re.compile(r"\baxiom\b"),
        "any opaque token": re.compile(r"\bopaque\b"),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"RSExactCardWitnessBridge rejects {label}",
        )

    for name in expected_signatures:
        audit.require(
            re.search(
                rf"^#print axioms {re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"RSExactCardWitnessBridge #print axioms {name}",
        )

    exact_card_boundary = (
        '"Exact" means that the chosen support has cardinality exactly `a`; '
        "it does not mean that this support is the complete agreement set "
        "of the explainer."
    )
    explicit_hypotheses_boundary = (
        "Semantic cells, their exhaustivity, their budgets, and a uniform sum "
        "bound remain explicit hypotheses."
    )
    audit.require(
        exact_card_boundary in flat,
        "RSExactCardWitnessBridge exact-card/full-agreement boundary",
    )
    audit.require(
        "Agreement outside the selected support is allowed." in flat,
        "RSExactCardWitnessBridge outside-agreement allowance",
    )
    audit.require(
        explicit_hypotheses_boundary in flat,
        "RSExactCardWitnessBridge semantic-cell/payment boundary",
    )
    audit.require(
        "the bad-slope image hypothesis is now a theorem rather than a caller obligation."
        in flat,
        "RSExactCardWitnessBridge discharged bad-image boundary",
    )
    audit.require(
        "import GrandeFinale.FirstMatchWitnessBridge" in text
        and "import GrandeFinale.RSExactSupportUpper" in text,
        "RSExactCardWitnessBridge concrete imports",
    )

    return {
        "path": RS_EXACT_CARD_WITNESS_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "witness_adapter_signatures": signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [
            f"#print axioms {name}" for name in expected_signatures
        ],
        "finite_structure_line": line_of(
            text, "structure RSExactCardWitness"
        ),
        "exact_card_boundary_line": line_of(
            text, '"Exact" means that the chosen support'
        ),
        "valid_witness_line": declarations["ValidRSExactCardWitness"],
        "catalogue_line": declarations["rsExactCardWitnesses"],
        "bad_slope_image_line": declarations[
            "rsMcaBadSlopes_eq_exactCardWitnessSlopeImage"
        ],
        "verified_claim": (
            "the finite exact-cardinality RS witness catalogue has exactly "
            "the threshold-a bad slopes as its slope image"
        ),
        "verified_boundary": (
            "same slope and support determine the explainer, but slope alone "
            "need not determine the support"
        ),
        "verified_nonclaim": (
            "the adapter constructs no semantic cells, raw-witness exhaustion, "
            "cell budget, uniform sum, C1-C9 classification, or payment"
        ),
    }


def audit_rs_exact_card_prefix_witness_bridge(
    text: str, audit: Audit
) -> dict[str, object]:
    flat = normalized(text)
    lean_code = lean_code_without_comments(text)
    declarations = declaration_lines(text)
    required = [
        "rsExactCardWitnessPrefixKey",
        "rsExactCardPrefixWitnessCell",
        "mem_rsExactCardPrefixWitnessCell_iff",
        "rsExactCardPrefixWitnessCells_cover",
        "rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell",
        "firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets",
        "B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets",
    ]
    for name in required:
        audit.require(
            name in declarations,
            f"RSExactCardPrefixWitnessBridge declaration {name}",
        )

    key_anchor = (
        "def rsExactCardWitnessPrefixKey (ev : D -> F) (K a : Nat) "
        "{k : Nat} (w : RSExactCardWitness D F k) : Fin (a - K) -> F := "
        "supportPrefixKey ev K a w.support"
    )
    cell_anchor = (
        "(rsExactCardWitnesses ev k a p.1 p.2).filter fun w => "
        "rsExactCardWitnessPrefixKey ev K a w = z"
    )
    audit.require(
        key_anchor in flat,
        "RSExactCardPrefixWitnessBridge locator-prefix key",
    )
    audit.require(
        cell_anchor in flat,
        "RSExactCardPrefixWitnessBridge concrete filtered cell",
    )

    expected_signatures = {
        "rsExactCardPrefixWitnessCells_cover": (
            "theorem rsExactCardPrefixWitnessCells_cover "
            "(ev : D -> F) (k a K : Nat) "
            "(p : (D -> F) × (D -> F)) : "
            "(Finset.univ : Finset (Fin (a - K) -> F)).biUnion "
            "(rsExactCardPrefixWitnessCell ev k a K p) = "
            "rsExactCardWitnesses ev k a p.1 p.2"
        ),
        "rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell": (
            "theorem "
            "rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k R : Nat) (hsize : k + R = Fintype.card D) "
            "(a K : Nat) (p : (D -> F) × (D -> F)) "
            "(z : Fin (a - K) -> F) : "
            "(rsExactCardPrefixWitnessCell ev k a K p z).image "
            "RSExactCardWitness.slope = "
            "rsPrefixBadSlopeCell ev R a K p.1 p.2 z"
        ),
        "B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets": (
            "theorem B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k R : Nat) (hsize : k + R = Fintype.card D) "
            "(a K : Nat) (hka : k + 1 ≤ a) "
            "(U : ((D -> F) × (D -> F)) -> "
            "(Fin (a - K) -> F) -> Nat) "
            "(hcell : ∀ p z, "
            "(rsPrefixBadSlopeCell ev R a K p.1 p.2 z).card ≤ U p z) : "
            "GrandeFinale.B_MCA "
            "(GrandeFinale.CollisionAwarePole.rsEval ev k : "
            "Set (D -> F)) a ≤ "
            "Finset.univ.sup (fun p : (D -> F) × (D -> F) => "
            "∑ z, U p z)"
        ),
        "B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets": (
            "theorem "
            "B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets "
            "(ev : D -> F) (hev : Function.Injective ev) "
            "(k a K B : Nat) (hka : k + 1 ≤ a) "
            "(U : ((D -> F) × (D -> F)) -> "
            "(Fin (a - K) -> F) -> Nat) "
            "(hcell : ∀ p z, "
            "(firstMatchSlopeCell "
            "(Finset.univ : Finset (Fin (a - K) -> F)) "
            "(rsExactCardPrefixWitnessCell ev k a K p) "
            "RSExactCardWitness.slope z).card ≤ U p z) "
            "(hunif : ∀ p, ∑ z, U p z ≤ B) : "
            "GrandeFinale.B_MCA "
            "(GrandeFinale.CollisionAwarePole.rsEval ev k : "
            "Set (D -> F)) a ≤ B"
        ),
    }
    signatures: dict[str, object] = {}
    for name, expected in expected_signatures.items():
        actual, theorem_line = theorem_signature(text, name)
        audit.require(
            actual == expected,
            f"RSExactCardPrefixWitnessBridge exact signature {name}",
        )
        signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }

    forbidden_syntax = {
        "any sorry token": re.compile(r"\bsorry\b"),
        "any admit token": re.compile(r"\badmit\b"),
        "any axiom token": re.compile(r"\baxiom\b"),
        "any opaque token": re.compile(r"\bopaque\b"),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"RSExactCardPrefixWitnessBridge rejects {label}",
        )

    exported = [
        "rsExactCardPrefixWitnessCells_cover",
        "rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell",
        "firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets",
        "B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets",
    ]
    for name in exported:
        audit.require(
            re.search(
                rf"^#print axioms {re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"RSExactCardPrefixWitnessBridge #print axioms {name}",
        )

    coverage_claim = (
        "The cells exhaust raw witnesses. Under injective evaluation and the "
        "parity-check dimension hypothesis, their slope images agree with the "
        "existing support-family locator-prefix cells."
    )
    scope_boundary = (
        "This is a structural locator-prefix partition, not a C1--C9 "
        "semantic classification: cell payment and the uniform sum bound "
        "remain explicit hypotheses."
    )
    audit.require(
        coverage_claim in flat,
        "RSExactCardPrefixWitnessBridge raw-witness coverage claim",
    )
    audit.require(
        scope_boundary in flat,
        "RSExactCardPrefixWitnessBridge C1-C9/payment boundary",
    )
    audit.require(
        "not an order compatible with the field operations." in flat,
        "RSExactCardPrefixWitnessBridge arbitrary attribution order boundary",
    )
    audit.require(
        "import GrandeFinale.RSExactCardWitnessBridge" in text
        and "import GrandeFinale.PrefixAtlasBridge" in text,
        "RSExactCardPrefixWitnessBridge composition imports",
    )

    return {
        "path": RS_EXACT_CARD_PREFIX_WITNESS_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "prefix_witness_signatures": signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [f"#print axioms {name}" for name in exported],
        "raw_witness_cover_line": declarations[
            "rsExactCardPrefixWitnessCells_cover"
        ],
        "per_cell_alignment_line": declarations[
            "rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell"
        ],
        "verified_claim": (
            "locator-prefix cells exhaust the concrete exact-cardinality witness "
            "catalogue and, under injective evaluation and the parity-dimension "
            "equation, align cellwise with support-prefix slopes"
        ),
        "verified_boundary": (
            "raw prefix-witness exhaustivity is discharged, while first-match "
            "cell budgets and their uniform line-sum bound remain inputs"
        ),
        "verified_nonclaim": (
            "the structural prefix partition is not a C1-C9 classification "
            "and constructs no cell payment or asymptotic UNIF certificate"
        ),
    }


def audit_rs_exact_card_occupancy_bridge(
    text: str, audit: Audit
) -> dict[str, object]:
    flat = normalized(text)
    lean_code = lean_code_without_comments(text)
    declarations = declaration_lines(text)
    required = [
        "explanationState",
        "explanationStateImage",
        "retainedSupportFiber",
        "retainedSupportOccupancy",
        "card_eq_sum_retainedSupportOccupancy",
        "support_injOn_retainedSupportFiber",
        "supportImage_retainedSupportFiber_card",
        "slopeImage_card_le_card_div_of_retainedSupportOccupancy",
        "firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy",
        "prefixResidualWitnessCell",
        "prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy",
        "B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy",
    ]
    for name in required:
        audit.require(
            name in declarations,
            f"RSExactCardOccupancyBridge declaration {name}",
        )

    audit.require(
        "def explanationState (w : RSExactCardWitness D F k) : "
        "F × (Fin k -> F) := (w.slope, w.coeffs)" in flat,
        "RSExactCardOccupancyBridge explanation-state projection",
    )
    audit.require(
        "C.filter fun w => explanationState w = rho" in flat,
        "RSExactCardOccupancyBridge retained-support fiber",
    )
    audit.require(
        "C.card = ∑ rho ∈ explanationStateImage C, "
        "retainedSupportOccupancy C rho" in flat,
        "RSExactCardOccupancyBridge exact occupancy sum",
    )
    audit.require(
        "(C.image RSExactCardWitness.slope).card ≤ C.card / H" in flat,
        "RSExactCardOccupancyBridge RC1 quotient conclusion",
    )
    audit.require(
        "(hocc : ∀ rho ∈ explanationStateImage C, "
        "H ≤ retainedSupportOccupancy C rho)" in flat,
        "RSExactCardOccupancyBridge universal lower occupancy",
    )
    audit.require(
        "(hunif : ∀ p, ∑ z, "
        "(prefixResidualWitnessCell ev k a K p z).card / H p z ≤ B)" in flat,
        "RSExactCardOccupancyBridge uniform quotient sum",
    )

    exported = [
        "card_eq_sum_retainedSupportOccupancy",
        "supportImage_retainedSupportFiber_card",
        "slopeImage_card_le_card_div_of_retainedSupportOccupancy",
        "firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy",
        "prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy",
        "B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy",
        "B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy",
    ]
    signatures: dict[str, object] = {}
    for name in exported:
        actual, theorem_line = theorem_signature(text, name)
        signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }
        audit.require(
            re.search(
                rf"^#print axioms {re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"RSExactCardOccupancyBridge #print axioms {name}",
        )

    forbidden_syntax = {
        "any sorry token": re.compile(r"\bsorry\b"),
        "any admit token": re.compile(r"\badmit\b"),
        "any axiom token": re.compile(r"\baxiom\b"),
        "any opaque token": re.compile(r"\bopaque\b"),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"RSExactCardOccupancyBridge rejects {label}",
        )

    scope_boundary = (
        "This is a projection-fiber interface, not a semantic C7 classifier "
        "or payment: the positive lower occupancy bound and the uniform "
        "line-sum bound remain explicit hypotheses. No profile-scale, "
        "boundary-image, or C1--C9 routing claim is made."
    )
    audit.require(
        scope_boundary in flat,
        "RSExactCardOccupancyBridge C7/payment boundary",
    )
    audit.require(
        "No semantic C7 classification or lower occupancy bound is "
        "constructed here." in flat,
        "RSExactCardOccupancyBridge lower-occupancy nonclaim",
    )
    audit.require(
        "import GrandeFinale.RSExactCardPrefixWitnessBridge" in text
        and "import GrandeFinale.FirstWallMDSExtensionInverse" in text,
        "RSExactCardOccupancyBridge composition imports",
    )

    return {
        "path": RS_EXACT_CARD_OCCUPANCY_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "occupancy_signatures": signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [f"#print axioms {name}" for name in exported],
        "exact_occupancy_sum_line": declarations[
            "card_eq_sum_retainedSupportOccupancy"
        ],
        "rc1_line": declarations[
            "slopeImage_card_le_card_div_of_retainedSupportOccupancy"
        ],
        "fixed_row_wrapper_line": declarations[
            "B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy"
        ],
        "verified_claim": (
            "realized explanation-state fibers partition each literal witness "
            "cell exactly, and a positive retained-support lower occupancy "
            "gives the exact floor(|C|/H) slope-image bound"
        ),
        "verified_boundary": (
            "the RC1 quotient is applied only after slope-level first match; "
            "the lower occupancy and uniform line-sum remain hypotheses"
        ),
        "verified_nonclaim": (
            "the adapter is not a semantic C7 classifier, profile payment, "
            "boundary-image theorem, or C1-C9 routing certificate"
        ),
    }


def audit_rs_exact_card_boundary_payment_bridge(
    text: str, audit: Audit
) -> dict[str, object]:
    flat = normalized(text)
    lean_code = lean_code_without_comments(text)
    declarations = declaration_lines(text)
    required = [
        "targetImage",
        "boundaryFiber",
        "fiberCount",
        "collisionPairs",
        "fullMean",
        "card_eq_sum_fiberCount",
        "collisionPairs_card_eq_sum_sq_fiberCount",
        "fullMean_pos",
        "assignedResidualSupports",
        "firstMatchBoundaryProfile",
        "firstMatchSlopeCell_card_le_boundaryRayMomentFloor",
        "firstMatchSlopeCell_card_le_boundaryRayMomentBudget",
    ]
    for name in required:
        audit.require(
            name in declarations,
            f"RSExactCardBoundaryPaymentBridge declaration {name}",
        )

    audit.require(
        "structure ResidualBoundaryProfile (Support Target : Type*) "
        "[DecidableEq Support] where" in flat,
        "RSExactCardBoundaryPaymentBridge profile structure",
    )
    audit.require(
        "residual_subset : residual ⊆ full" in flat,
        "RSExactCardBoundaryPaymentBridge residual subset guard",
    )
    audit.require(
        "p.full.image p.boundary" in flat,
        "RSExactCardBoundaryPaymentBridge full target image",
    )
    audit.require(
        "p.residual.filter fun x => p.boundary x = s" in flat,
        "RSExactCardBoundaryPaymentBridge residual fiber",
    )
    audit.require(
        "(p.residual ×ˢ p.residual).filter fun pair => "
        "p.boundary pair.1 = p.boundary pair.2" in flat,
        "RSExactCardBoundaryPaymentBridge residual collision pairs",
    )
    audit.require(
        "(p.full.card : ℝ) / p.targetImage.card" in flat,
        "RSExactCardBoundaryPaymentBridge full-image mean",
    )
    audit.require(
        "p.residual.card = ∑ s ∈ p.targetImage, p.fiberCount s" in flat,
        "RSExactCardBoundaryPaymentBridge exact residual fiber sum",
    )
    audit.require(
        "p.collisionPairs.card = ∑ s ∈ p.targetImage, p.fiberCount s ^ 2"
        in flat,
        "RSExactCardBoundaryPaymentBridge exact collision identity",
    )
    audit.require(
        "(hres : assignedResidualSupports idx cell i ⊆ fullSupports)" in flat,
        "RSExactCardBoundaryPaymentBridge actual residual-to-full guard",
    )
    audit.require(
        "(hleft : ∀ gamma ∈ firstMatchSlopeCell idx cell "
        "RSExactCardWitness.slope i," in flat,
        "RSExactCardBoundaryPaymentBridge universal slope degree",
    )
    audit.require(
        "(hright : ∀ pair ∈ (firstMatchBoundaryProfile idx cell i "
        "fullSupports Phi hres).collisionPairs," in flat,
        "RSExactCardBoundaryPaymentBridge universal pair degree",
    )
    audit.require(
        "(hpaid : ⌊" in flat and "⌋₊ ≤ U)" in flat,
        "RSExactCardBoundaryPaymentBridge final payment comparison",
    )
    audit.require(
        "(firstMatchSlopeCell idx cell RSExactCardWitness.slope i).card ≤ U"
        in flat,
        "RSExactCardBoundaryPaymentBridge paid-cell conclusion",
    )

    exported = [
        "card_eq_sum_fiberCount",
        "collisionPairs_card_eq_sum_sq_fiberCount",
        "fullMean_pos",
        "firstMatchSlopeCell_card_le_boundaryRayMomentFloor",
        "firstMatchSlopeCell_card_le_boundaryRayMomentBudget",
    ]
    signatures: dict[str, object] = {}
    signature_texts: dict[str, str] = {}
    for name in exported:
        actual, theorem_line = theorem_signature(text, name)
        signature_texts[name] = normalized(actual)
        signatures[name] = {
            "line": theorem_line,
            "normalized_sha256": digest(actual),
        }
        audit.require(
            re.search(
                rf"^#print axioms (?:ResidualBoundaryProfile\.)?"
                rf"{re.escape(name)}[ \t]*$",
                lean_code,
                re.MULTILINE,
            )
            is not None,
            f"RSExactCardBoundaryPaymentBridge #print axioms {name}",
        )

    for name in [
        "firstMatchSlopeCell_card_le_boundaryRayMomentFloor",
        "firstMatchSlopeCell_card_le_boundaryRayMomentBudget",
    ]:
        audit.require(
            "(hleft : ∀ gamma ∈ firstMatchSlopeCell idx cell "
            "RSExactCardWitness.slope i," in signature_texts[name],
            f"RSExactCardBoundaryPaymentBridge {name} universal slope degree",
        )
        audit.require(
            "(hright : ∀ pair ∈ (firstMatchBoundaryProfile idx cell i "
            "fullSupports Phi hres).collisionPairs," in signature_texts[name],
            f"RSExactCardBoundaryPaymentBridge {name} universal pair degree",
        )

    forbidden_syntax = {
        "any sorry token": re.compile(r"\bsorry\b"),
        "any admit token": re.compile(r"\badmit\b"),
        "any axiom token": re.compile(r"\baxiom\b"),
        "any opaque token": re.compile(r"\bopaque\b"),
    }
    for label, pattern in forbidden_syntax.items():
        audit.require(
            pattern.search(lean_code) is None,
            f"RSExactCardBoundaryPaymentBridge rejects {label}",
        )

    audit.require(
        "import GrandeFinale.RSExactCardOccupancyBridge" in text
        and "import GrandeFinale.ExactProfileCompiler" in text,
        "RSExactCardBoundaryPaymentBridge composition imports",
    )
    audit.require(
        "It does not identify a semantic C7/C8/C9 cell." in flat,
        "RSExactCardBoundaryPaymentBridge semantic-cell nonclaim",
    )
    audit.require(
        "Positive occupancy or incidence-degree bounds, a semantic boundary "
        "map and its deployed moment payment, semantic first-match survival, "
        "and the uniform profile sum remain explicit inputs." in flat,
        "RSExactCardBoundaryPaymentBridge unresolved-input boundary",
    )

    return {
        "path": RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
        "sha256": digest(text),
        "declarations": {name: declarations[name] for name in required},
        "boundary_payment_signatures": signatures,
        "forbidden_syntax_checks": sorted(forbidden_syntax),
        "axiom_print_lines": [
            f"#print axioms ResidualBoundaryProfile.{name}"
            if name in {
                "card_eq_sum_fiberCount",
                "collisionPairs_card_eq_sum_sq_fiberCount",
                "fullMean_pos",
            }
            else f"#print axioms {name}"
            for name in exported
        ],
        "fiber_sum_line": declarations["card_eq_sum_fiberCount"],
        "collision_identity_line": declarations[
            "collisionPairs_card_eq_sum_sq_fiberCount"
        ],
        "actual_cell_fc1_line": declarations[
            "firstMatchSlopeCell_card_le_boundaryRayMomentFloor"
        ],
        "verified_claim": (
            "full-image normalization and retained residual fibers give exact "
            "first/second-moment data, and supplied ray degrees plus a residual "
            "moment bound the actual assigned slope cell by the literal FC1 floor"
        ),
        "verified_boundary": (
            "semantic C8 incidence, deployed C9 boundary/moment payment, final "
            "hpaid comparison, and row-uniform summation remain explicit inputs"
        ),
        "verified_nonclaim": (
            "the adapter does not classify a C7/C8/C9 cell or prove any hard input"
        ),
    }


def audit_c3_scope(
    c3_text: str, frontiers_text: str, audit_document: str, audit: Audit
) -> dict[str, object]:
    c3_flat = normalized(c3_text)
    frontiers_flat = normalized(frontiers_text)
    audit_flat = normalized(audit_document)

    audit.require("**C3: PARTIAL.**" in c3_text, "C3 route-scoped partial verdict")
    audit.require(
        "Theorem (exact coset census)" in c3_flat
        and "|𝒫_coset(N)| := Σ_{c∣N} N/c = Σ_{e∣N} e = σ(N)" in c3_flat,
        "C3 exact multiplicative-coset census",
    )
    audit.require(
        "σ(N) ≤ N·(1+ln N)" in c3_flat
        and "|𝒫_coset(N)| = e^{o(N)}" in c3_flat,
        "C3 narrow census subexponential bound",
    )
    audit.require(
        "Claim 3 — ramification polynomials are already coset-type" in c3_flat
        and "every multiplier map" in c3_flat,
        "C3 multiplier-fixed-locus scope",
    )
    audit.require(
        "BLOCKED" in c3_flat
        and "support locators" in c3_flat
        and "received-line resultants" in c3_flat,
        "C3 general row-dependent blocker retained",
    )

    audit.require(
        "payment additionally requires a subexponential census of allowed "
        "\\(P\\), the residual prefix estimate, and its slope projection"
        in frontiers_flat,
        "frontiers C3 three-factor payment criterion",
    )
    audit.require(
        "If the total description entropy is \\(o(n)\\), "
        "\\(\\sum_P\\barN(P)\\le e^{o(n)}\\mathfrak E_n\\), and the "
        "projection from each chart to distinct slopes has cost "
        "\\(e^{o(n)}\\barN(P)\\), then the planted family is paid."
        in frontiers_flat,
        "frontiers repaired planted-payment hypotheses",
    )

    audit.require(
        "proves only the subexponential candidate-family census for explicit "
        "multiplicative subgroup-coset and multiplier-fixed loci" in audit_flat,
        "audit narrows C3 to the proved candidate census",
    )
    audit.require(
        "it does not construct the row-level family or prove residual profile "
        "scale, description entropy, or distinct-slope projection" in audit_flat,
        "audit preserves remaining C3 payment inputs",
    )
    audit.require(
        "no general or row-level C3 family/payment" in audit_flat,
        "audit retains general C3 blocker",
    )

    return {
        "census_path": C3_CENSUS,
        "census_sha256": digest(c3_text),
        "frontiers_path": FRONTIERS_TEX,
        "frontiers_sha256": digest(frontiers_text),
        "partial_verdict_line": line_of(c3_text, "**C3: PARTIAL.**"),
        "planted_payment_line": line_of(
            frontiers_text,
            "payment additionally requires a subexponential",
        ),
        "verified_narrow_result": (
            "the explicit multiplicative subgroup-coset candidate family has "
            "census sigma(N) <= N(1+ln N), and multiplier-fixed loci lie in it"
        ),
        "remaining_scope": (
            "row-level semantic family identification, residual/profile scale, "
            "description entropy, distinct-slope projection, and unrestricted "
            "common-factor/resultant C3 payment remain open"
        ),
    }

def blocker_paragraph(section: str, cell: str) -> tuple[str, int]:
    pattern = re.compile(
        rf"^- \*\*{re.escape(cell)} \(([^)]*)\)\.\*\*(.*?)(?=^- \*\*C[0-9]+ \(|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(section)
    if match is None:
        raise AuditError(f"missing Section 3.2 blocker paragraph for {cell}")
    return normalized(match.group(0)), section.count("\n", 0, match.start()) + 1


def audit_ledger(text: str, audit: Audit) -> dict[str, object]:
    flat = normalized(text)
    audit.require(
        "FULL-CATALOGUE SUMMATION BLOCKED AT FOUR NAMED CELLS" in flat,
        "atlas ledger four-blocker status",
    )
    audit.require(
        "Tally: 5 PAID `{C1, C2, C4, C5, C6}`, 4 UNPAID/CONDITIONAL `{C3, C7, C8, C9}`."
        in text,
        "atlas ledger paid/unpaid tally",
    )
    section_start = text.find("### 3.2 Summation")
    section_end = text.find("### 3.3 Composed", section_start)
    audit.require(section_start >= 0 and section_end > section_start, "atlas ledger Section 3.2 bounds")
    section = text[section_start:section_end]
    requirements = {
        "C3": ["subexponential census", "CONDITIONAL"],
        "C7": ["projection-degree budget", "OPEN"],
        "C8": ["CONDITIONAL on (RC)"],
        "C9": ["UNPAID (general)"],
    }
    blockers: dict[str, object] = {}
    section_base_line = text.count("\n", 0, section_start)
    for cell, tokens in requirements.items():
        paragraph, local_line = blocker_paragraph(section, cell)
        for token in tokens:
            audit.require(token in paragraph, f"atlas ledger {cell} token {token}")
        blockers[cell] = {
            "line": section_base_line + local_line,
            "paragraph_sha256": digest(paragraph),
            "required_status_tokens": tokens,
        }

    audit.require(
        "Coverage / exhaustion --- COMPOSES (PROVED, unconditional)" in text,
        "atlas ledger unconditional exhaustion",
    )
    audit.require(
        "Summation --- COMPOSES over the 5 paid cells, BLOCKED over the full catalogue" in text,
        "atlas ledger payment boundary heading",
    )
    return {
        "path": ATLAS_LEDGER,
        "sha256": digest(text),
        "unconditional_exhaustion_line": line_of(
            text, "Coverage / exhaustion --- COMPOSES (PROVED, unconditional)"
        ),
        "payment_boundary_line": line_of(
            text, "Summation --- COMPOSES over the 5 paid cells"
        ),
        "paid_cells": ["C1", "C2", "C4", "C5", "C6"],
        "blocked_or_conditional_cells": blockers,
        "verified_boundary": "full-catalogue payment remains blocked exactly at C3/C7/C8/C9",
    }


def audit_heavy_fiber(text: str, audit: Audit) -> dict[str, object]:
    flat = normalized(text)
    h4 = (
        "(H4) the packet is a genuine primitive first-match residual whose atlas (A2) is "
        "witness-exhaustive on the depth-R prefix chart (so \"earlier cell\" is meaningful)."
    )
    nonclaim = (
        "Hypothesis (H4) is atlas-internal ((A2) for the prefix chart), assumed from "
        "ledger-admissibility, not re-proved here."
    )
    audit.require("CONDITIONAL (the transfer)" in flat, "HeavyFiber conditional status")
    audit.require(h4 in flat, "HeavyFiber H4 witness-exhaustive hypothesis")
    audit.require(nonclaim in flat, "HeavyFiber H4 nonclaim")
    audit.require(
        "a single depth-1 prefix fiber" in flat,
        "HeavyFiber depth-one concrete fiber",
    )
    audit.require(
        "**Not** an image-scale MI/MA or Sidon payment." in flat,
        "HeavyFiber Sidon-payment nonclaim",
    )
    return {
        "path": HEAVY_FIBER,
        "sha256": digest(text),
        "h4_line": line_of(text, "(H4) the packet is a genuine primitive first-match residual"),
        "h4_nonclaim_line": line_of(text, "Hypothesis (H4) is atlas-internal"),
        "depth_one_fiber_line": line_of(text, "a single depth-1 prefix fiber"),
        "status": "conditional on atlas-internal H4; H4 is assumed, not re-proved",
        "verified_nonclaim": "the transfer does not pay the image-scale MI/MA or Sidon cell",
    }


ATLAS_TERM = re.compile(r"atlas(?:-|[ \t\r\n]+)totality", re.IGNORECASE)


def stale_hits_in_text(text: str) -> list[dict[str, object]]:
    hits: list[dict[str, object]] = []
    for match in ATLAS_TERM.finditer(text):
        paragraph_start = text.rfind("\n\n", 0, match.start()) + 2
        paragraph_end = text.find("\n\n", match.end())
        if paragraph_end < 0:
            paragraph_end = len(text)
        paragraph = normalized(text[paragraph_start:paragraph_end])
        if "codex" not in paragraph.lower():
            continue
        hits.append(
            {
                "line": text.count("\n", 0, match.start()) + 1,
                "term": normalized(match.group(0)).lower(),
                "context_sha256": digest(paragraph),
            }
        )
    return hits


def audit_stale_wording(
    overrides: Mapping[str, str], audit: Audit
) -> dict[str, object]:
    files: dict[str, object] = {}
    occurrence_count = 0
    for path in sorted(THRESHOLD_NOTES.glob("*.md")):
        relative = path.relative_to(ROOT).as_posix()
        text = read_source(relative, overrides)
        hits = stale_hits_in_text(text)
        if hits:
            files[relative] = {"sha256": digest(text), "hits": hits}
            occurrence_count += len(hits)

    audit.require(len(files) >= 5, "stale atlas-totality wording appears downstream")
    audit.require(
        occurrence_count >= len(files),
        "stale atlas-totality occurrence count covers every listed file",
    )
    return {
        "scope": "experimental/notes/thresholds/*.md",
        "file_count": len(files),
        "occurrence_count": occurrence_count,
        "files": files,
        "classification": "legacy owner/lane wording; not a new mathematical escape",
        "replacement_interface": (
            "generic totality is integrated; the remaining obligation is primitive survival/"
            "catalogue classification plus cellwise profile and bad-slope payment"
        ),
    }


def negative_control(audit: Audit) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for bits in range(0, 9):
        count = 1 << bits
        items = list(range(count))
        cells: dict[int, list[int]] = {}
        for item in items:
            key = item  # A total identity key: every item realizes its own key.
            cells.setdefault(key, []).append(item)
        flattened = [item for key in sorted(cells) for item in cells[key]]
        singleton = all(len(cell) == 1 for cell in cells.values())
        audit.require(flattened == items, f"negative control flatten exact at b={bits}")
        audit.require(len(cells) == count, f"negative control one key per item at b={bits}")
        audit.require(singleton, f"negative control singleton cells at b={bits}")
        rows.append(
            {
                "bits": bits,
                "item_count": count,
                "realized_key_count": len(cells),
                "all_cells_singletons": singleton,
                "flatten_exact": flattened == items,
            }
        )
    return {
        "model": "identity total map i -> i on items [0, 2^b)",
        "rows": rows,
        "exact_conclusion": (
            "totality and exact coverage permit 2^b realized singleton cells; "
            "coverage alone gives no subexponential profile or slope-payment bound"
        ),
    }


def max_sum_quantifier_negative_control(audit: Audit) -> dict[str, object]:
    rows: list[dict[str, int]] = []
    for bits in range(0, 9):
        count = 1 << bits
        lines = range(count)
        cells = range(count)

        def cell(line: int, key: int) -> int:
            return int(line == key)

        line_sums = [sum(cell(line, key) for key in cells) for line in lines]
        cell_sups = [max(cell(line, key) for line in lines) for key in cells]
        sup_line_sum = max(line_sums)
        sum_cell_sup = sum(cell_sups)

        audit.require(
            line_sums == [1] * count,
            f"max/sum control every line sum is one at b={bits}",
        )
        audit.require(
            cell_sups == [1] * count,
            f"max/sum control every cell supremum is one at b={bits}",
        )
        audit.require(sup_line_sum == 1, f"max/sum control sup-sum at b={bits}")
        audit.require(
            sum_cell_sup == count,
            f"max/sum control sum-sup at b={bits}",
        )
        rows.append(
            {
                "bits": bits,
                "line_count": count,
                "cell_count": count,
                "sup_line_sum_cells": sup_line_sum,
                "sum_cells_sup_line": sum_cell_sup,
                "overpayment_factor": sum_cell_sup // sup_line_sum,
            }
        )
    return {
        "model": "cell(line,z) = 1 iff z = line on 2^b lines and cells",
        "rows": rows,
        "exact_conclusion": (
            "sup_line sum_z cell(line,z) = 1 while "
            "sum_z sup_line cell(line,z) = 2^b"
        ),
    }


def build_certificate(overrides: Mapping[str, str] | None = None) -> dict[str, object]:
    source_overrides = overrides or {}
    audit = Audit()
    prefix_text = read_source(PREFIX_ATLAS, source_overrides)
    bridge_text = read_source(PREFIX_BRIDGE, source_overrides)
    witness_bridge_text = read_source(FIRST_MATCH_WITNESS_BRIDGE, source_overrides)
    exact_card_witness_text = read_source(
        RS_EXACT_CARD_WITNESS_BRIDGE, source_overrides
    )
    exact_card_prefix_witness_text = read_source(
        RS_EXACT_CARD_PREFIX_WITNESS_BRIDGE, source_overrides
    )
    exact_card_occupancy_text = read_source(
        RS_EXACT_CARD_OCCUPANCY_BRIDGE, source_overrides
    )
    exact_card_boundary_payment_text = read_source(
        RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE, source_overrides
    )
    ledger_text = read_source(ATLAS_LEDGER, source_overrides)
    c3_text = read_source(C3_CENSUS, source_overrides)
    frontiers_text = read_source(FRONTIERS_TEX, source_overrides)
    heavy_text = read_source(HEAVY_FIBER, source_overrides)
    audit_document_text = read_source(AUDIT_DOCUMENT, source_overrides)
    artifact_bindings: dict[str, object] = {}
    for relative in (
        VERIFIER_SCRIPT,
        AUDIT_DOCUMENT,
        CORRESPONDENCE_DOCUMENT,
    ):
        artifact_text = read_source(relative, source_overrides)
        audit.require(
            bool(artifact_text),
            f"bound artifact is nonempty: {relative}",
        )
        artifact_bindings[relative] = {
            "path": relative,
            "sha256": digest(artifact_text),
            "byte_count": len(artifact_text.encode("utf-8")),
        }

    prefix = audit_prefix_atlas(prefix_text, audit)
    bridge = audit_prefix_bridge(bridge_text, audit)
    witness_bridge = audit_first_match_witness_bridge(witness_bridge_text, audit)
    exact_card_witness_bridge = audit_rs_exact_card_witness_bridge(
        exact_card_witness_text,
        audit,
    )
    exact_card_prefix_witness_bridge = (
        audit_rs_exact_card_prefix_witness_bridge(
            exact_card_prefix_witness_text, audit
        )
    )
    exact_card_occupancy_bridge = audit_rs_exact_card_occupancy_bridge(
        exact_card_occupancy_text, audit
    )
    exact_card_boundary_payment_bridge = (
        audit_rs_exact_card_boundary_payment_bridge(
            exact_card_boundary_payment_text, audit
        )
    )
    ledger = audit_ledger(ledger_text, audit)
    c3_scope = audit_c3_scope(c3_text, frontiers_text, audit_document_text, audit)
    heavy = audit_heavy_fiber(heavy_text, audit)
    stale = audit_stale_wording(source_overrides, audit)
    control = negative_control(audit)
    quantifier_control = max_sum_quantifier_negative_control(audit)

    certificate: dict[str, object] = {
        "schema": "atlas-payment-interface/v7",
        "verdict": "AUDIT: coverage proved; catalogue/profile/payment interface remains explicit",
        "artifact_bindings": artifact_bindings,
        "sources": {
            "generic_prefix_atlas": prefix,
            "concrete_prefix_bridge": bridge,
            "first_match_witness_bridge": witness_bridge,
            "rs_exact_card_witness_bridge": exact_card_witness_bridge,
            "rs_exact_card_prefix_witness_bridge": exact_card_prefix_witness_bridge,
            "rs_exact_card_occupancy_bridge": exact_card_occupancy_bridge,
            "rs_exact_card_boundary_payment_bridge": exact_card_boundary_payment_bridge,
            "catalogue_ledger": ledger,
            "c3_scope": c3_scope,
            "heavy_fiber_transfer": heavy,
        },
        "stale_downstream_wording": stale,
        "negative_control": control,
        "max_sum_quantifier_negative_control": quantifier_control,
        "interface_summary": {
            "proved": [
                "total prefix keys partition and first-match-cover all supplied witnesses",
                "concrete locator-prefix cells cover the supplied support family",
                "support-family bad slopes equal the union of cellwise bad slopes",
                "explicit cellwise U(z) budgets sum to a full-family budget",
                "linewise U(u0,u1,z) budgets plus uniform summed bound B imply B_MCA <= B",
                "stronger line-independent U(z) budgets imply B_MCA <= sum_z U(z)",
                "each residual witness cell has exactly its assigned first-match slope image",
                "explicit bad-slope image, witness exhaustion, and cell budgets bound B_MCA by the supremum of line-dependent sums",
                "a uniform bound on those line-dependent sums yields B_MCA <= B",
                "a proper witness subset can have exactly the full witness-family slope image",
                "slope-level first-match residual cells can fail witness exhaustion despite original-cell and slope-image coverage",
                "a finite coefficient-vector exact-cardinality RS witness catalogue is constructed for every received line",
                "the concrete catalogue's slope image is exactly the threshold-a RS MCA-bad slope set",
                "raw witness exhaustion plus first-match slope budgets specializes directly to the concrete RS catalogue",
                "locator-prefix witness cells exactly exhaust every concrete linewise catalogue",
                "under injective evaluation and the parity-dimension equation, each prefix-witness slope image equals its support-prefix bad-slope cell",
                "locator-prefix first-match budgets specialize to B_MCA without a raw-exhaustivity hypothesis",
                "literal witness cells split exactly over realized explanation-state fibers",
                "positive retained-support occupancy bounds each post-first-match slope cell by floor(|residual|/H)",
                "the resulting line-dependent RC1 quotient budgets specialize to the full B_MCA numerator",
                "full-slice boundary image and retained residual fibers remain distinct normalization objects",
                "retained residual fiber counts and equal-boundary collision pairs satisfy exact first/second-moment identities",
                "supplied C8 ray-incidence degrees and C9 residual moment data bound the actual first-match slope cell by the literal FC1 floor",
                "the explicit multiplicative subgroup-coset C3 candidate family has subexponential census sigma(N), with multiplier-fixed loci contained in it",
            ],
            "not_proved": [
                "construction of the cellwise U(z) budgets",
                "witness exhaustion of slope-level residual cells without additional hypotheses",
                "construction of C1-C9 semantic cell indices/cells, per-cell budgets, or uniform sum bound",
                "a concrete C1-C9 Reed-Solomon semantic atlas, prefix classification, or payment",
                "asymptotic-row same-catalogue uniformity (UNIF)",
                "C1-C8 primitive-survival/catalogue classification for the intended row",
                "general or row-level C3 semantic family identification, residual/profile estimate, and distinct-slope payment",
                "a lower retained-support occupancy bound for any intended semantic C7 profile",
                "semantic C8 chart assignment and deployed ray-incidence degree bounds",
                "deployed-scale image-normalized Sidon payment",
                "the final FC1 hpaid comparison and row-uniform sum for intended C8/C9 profiles",
            ],
        },
        "verification_check_count": len(audit.checks),
    }
    return certificate


def canonical(certificate: object) -> str:
    return json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def verify_checked_in(actual: dict[str, object]) -> None:
    if not CERTIFICATE.is_file():
        raise AuditError(f"missing checked-in certificate: {CERTIFICATE.relative_to(ROOT)}")
    expected_text = CERTIFICATE.read_text(encoding="utf-8")
    actual_text = canonical(actual)
    if expected_text != actual_text:
        diff = "".join(
            difflib.unified_diff(
                expected_text.splitlines(keepends=True),
                actual_text.splitlines(keepends=True),
                fromfile="checked-in certificate",
                tofile="recomputed certificate",
                n=2,
            )
        )
        raise AuditError("checked-in certificate mismatch:\n" + diff)


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AuditError(f"tamper fixture expected one occurrence of {old!r}")
    return text.replace(old, new, 1)


def regex_replace_once(text: str, pattern: str, replacement: str) -> str:
    changed, count = re.subn(pattern, replacement, text, count=1, flags=re.IGNORECASE)
    if count != 1:
        raise AuditError(f"tamper fixture did not match {pattern!r}")
    return changed


def commented_signature_spoof(text: str) -> str:
    name = "badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets"
    signature, _ = theorem_signature(text, name)
    renamed = replace_once(
        text,
        f"theorem {name}",
        f"theorem {name}_renamed",
    )
    return renamed + f"\n\n/-\n{signature} := by\n-/\n"


def run_tamper_selftest(baseline: dict[str, object]) -> int:
    generic_budget_prefix = (
        "    (U : (Fin (m - K) -> F) -> Nat)\n"
        "    (hU : ∀ z,"
    )
    semantic_mutations: list[tuple[str, str, Callable[[str], str]]] = [
        (
            "collapse coverage/payment separation",
            PREFIX_ATLAS,
            lambda text: replace_once(
                text,
                "Coverage and payment remain separate",
                "Coverage and payment are identified",
            ),
        ),
        (
            "remove generic universal cellwise budget",
            PREFIX_BRIDGE,
            lambda text: replace_once(
                text,
                generic_budget_prefix,
                generic_budget_prefix.replace("(hU : ∀ z,", "(hU : ∃ z,"),
            ),
        ),
        (
            "rename the C9 blocker",
            ATLAS_LEDGER,
            lambda text: replace_once(text, "- **C9 (Sidon).**", "- **C10 (Sidon).**"),
        ),
        (
            "erase the atlas-internal H4 label",
            HEAVY_FIBER,
            lambda text: replace_once(text, "(H4) the packet", "(H5) the packet"),
        ),
        (
            "weaken the stronger line-independent B_MCA budget",
            PREFIX_BRIDGE,
            lambda text: replace_once(
                text,
                "(hU : ∀ (u0 u1 : D -> F) z,",
                "(hU : ∃ (u0 u1 : D -> F), ∀ z,",
            ),
        ),
        (
            "weaken the fixed-row outer-line summed bound",
            PREFIX_BRIDGE,
            lambda text: replace_once(
                text,
                "(hunif : ∀ u0 u1, ∑ z, U u0 u1 z ≤ B)",
                "(hunif : ∃ u0 u1, ∑ z, U u0 u1 z ≤ B)",
            ),
        ),
        (
            "add an extra hgoal binder",
            PREFIX_BRIDGE,
            lambda text: replace_once(
                text,
                generic_budget_prefix,
                generic_budget_prefix.replace(
                    "    (hU : ∀ z,",
                    "    (hgoal : True)\n    (hU : ∀ z,",
                ),
            ),
        ),
        (
            "insert standalone sorry",
            PREFIX_BRIDGE,
            lambda text: text + "\n\nsorry\n",
        ),
        (
            "weaken linewise hcell",
            PREFIX_BRIDGE,
            lambda text: replace_once(
                text,
                "(hcell : ∀ u0 u1 z,",
                "(hcell : ∃ u0 u1, ∀ z,",
            ),
        ),
        (
            "replace live theorem with commented exact signature",
            PREFIX_BRIDGE,
            commented_signature_spoof,
        ),
        (
            "weaken witness hexhaust",
            FIRST_MATCH_WITNESS_BRIDGE,
            lambda text: regex_replace_once(
                text,
                r"\(hexhaust : ∀ p,",
                "(hexhaust : ∃ p,",
            ),
        ),
        (
            "falsify residual-witness countermodel boundary",
            FIRST_MATCH_WITNESS_BRIDGE,
            lambda text: replace_once(
                text,
                "(firstMatchResidualWitnessCell idx cell slope) ≠ witnesses ∧",
                "(firstMatchResidualWitnessCell idx cell slope) = witnesses ∧",
            ),
        ),
        (
            "weaken exact-cardinality RS witness predicate",
            RS_EXACT_CARD_WITNESS_BRIDGE,
            lambda text: replace_once(
                text,
                "w.support.card = a ∧",
                "a ≤ w.support.card ∧",
            ),
        ),
        (
            "weaken concrete RS witness hexhaust",
            RS_EXACT_CARD_WITNESS_BRIDGE,
            lambda text: regex_replace_once(
                text,
                r"\(hexhaust : ∀ p,",
                "(hexhaust : ∃ p,",
            ),
        ),
        (
            "weaken raw prefix-witness exhaustivity",
            RS_EXACT_CARD_PREFIX_WITNESS_BRIDGE,
            lambda text: replace_once(
                text,
                "        (rsExactCardPrefixWitnessCell ev k a K p) =\n"
                "      rsExactCardWitnesses ev k a p.1 p.2",
                "        (rsExactCardPrefixWitnessCell ev k a K p) ⊆\n"
                "      rsExactCardWitnesses ev k a p.1 p.2",
            ),
        ),
        (
            "weaken prefix-witness per-cell slope alignment",
            RS_EXACT_CARD_PREFIX_WITNESS_BRIDGE,
            lambda text: replace_once(
                text,
                "        RSExactCardWitness.slope =\n",
                "        RSExactCardWitness.slope ⊆\n",
            ),
        ),
        (
            "weaken universal retained-support occupancy",
            RS_EXACT_CARD_OCCUPANCY_BRIDGE,
            lambda text: replace_once(
                text,
                "    (hocc : ∀ rho ∈ explanationStateImage C,\n"
                "      H ≤ retainedSupportOccupancy C rho) :",
                "    (hocc : ∃ rho ∈ explanationStateImage C,\n"
                "      H ≤ retainedSupportOccupancy C rho) :",
            ),
        ),
        (
            "weaken uniform RC1 quotient sum",
            RS_EXACT_CARD_OCCUPANCY_BRIDGE,
            lambda text: replace_once(
                text,
                "    (hunif : ∀ p,\n"
                "      ∑ z, (prefixResidualWitnessCell ev k a K p z).card / H p z ≤ B) :",
                "    (hunif : ∃ p,\n"
                "      ∑ z, (prefixResidualWitnessCell ev k a K p z).card / H p z ≤ B) :",
            ),
        ),
        (
            "reverse boundary residual subset guard",
            RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
            lambda text: replace_once(
                text,
                "  residual_subset : residual ⊆ full",
                "  residual_subset : full ⊆ residual",
            ),
        ),
        (
            "normalize boundary mean by residual image",
            RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
            lambda text: replace_once(
                text,
                "  p.full.image p.boundary",
                "  p.residual.image p.boundary",
            ),
        ),
        (
            "weaken exact collision identity",
            RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
            lambda text: replace_once(
                text,
                "    p.collisionPairs.card =\n"
                "      ∑ s ∈ p.targetImage, p.fiberCount s ^ 2 := by",
                "    p.collisionPairs.card ≤\n"
                "      ∑ s ∈ p.targetImage, p.fiberCount s ^ 2 := by",
            ),
        ),
        (
            "existentialize boundary ray lower degree",
            RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
            lambda text: replace_once(
                text,
                "    (H J q : Nat) (hH : 0 < H) (hq : 2 ≤ q)\n"
                "    (hleft : ∀ gamma ∈\n"
                "      firstMatchSlopeCell idx cell RSExactCardWitness.slope i,",
                "    (H J q : Nat) (hH : 0 < H) (hq : 2 ≤ q)\n"
                "    (hleft : ∃ gamma ∈\n"
                "      firstMatchSlopeCell idx cell RSExactCardWitness.slope i,",
            ),
        ),
        (
            "erase final boundary payment premise",
            RS_EXACT_CARD_BOUNDARY_PAYMENT_BRIDGE,
            lambda text: replace_once(text, "    (hpaid :\n", "    (hpaid_erased :\n"),
        ),
        (
            "broaden narrow C3 census in the audit",
            AUDIT_DOCUMENT,
            lambda text: replace_once(
                text,
                "proves only the subexponential candidate-family census for explicit multiplicative subgroup-coset and multiplier-fixed loci",
                "proves the complete planted-cell payment for all loci",
            ),
        ),
    ]

    stale_files = baseline["stale_downstream_wording"]["files"]  # type: ignore[index]
    stale_path = sorted(stale_files)[0]
    binding_mutations: list[tuple[str, str, Callable[[str], str]]] = [
        (
            "resolve one stale atlas-totality phrase",
            stale_path,
            lambda text: regex_replace_once(text, r"atlas[-\s]+totality", "atlas payment"),
        ),
        (
            "alter verifier module docstring",
            VERIFIER_SCRIPT,
            lambda text: replace_once(
                text,
                "This stdlib-only verifier checks "
                "repository text",
                "This altered stdlib-only verifier checks repository text",
            ),
        ),
    ]

    baseline_text = canonical(baseline)
    detected = 0
    for label, relative, mutate in semantic_mutations:
        original = read_source(relative, {})
        try:
            tampered_text = mutate(original)
        except AuditError as error:
            raise AuditError(
                f"semantic tamper fixture failed to apply: {label}: {error}"
            ) from error
        try:
            build_certificate({relative: tampered_text})
        except AuditError:
            detected += 1
            print(f"TAMPER: DETECTED (AuditError) - {label}")
            continue
        raise AuditError(f"semantic tamper did not raise AuditError: {label}")

    for label, relative, mutate in binding_mutations:
        original = read_source(relative, {})
        try:
            tampered_text = mutate(original)
        except AuditError as error:
            raise AuditError(
                f"binding tamper fixture failed to apply: {label}: {error}"
            ) from error
        try:
            mutated = build_certificate({relative: tampered_text})
        except AuditError as error:
            raise AuditError(
                f"binding tamper must use certificate delta, not AuditError: {label}"
            ) from error
        if canonical(mutated) == baseline_text:
            raise AuditError(f"binding tamper escaped certificate delta: {label}")
        detected += 1
        print(f"TAMPER: DETECTED (certificate delta) - {label}")
    return detected


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the checked-in certificate (the default action)",
    )
    parser.add_argument(
        "--emit-certificate",
        metavar="PATH",
        type=Path,
        help="write the recomputed canonical certificate to PATH",
    )
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="verify the certificate and detect the in-memory mutation suite",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        certificate = build_certificate()
        if args.emit_certificate is not None:
            output = args.emit_certificate
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(canonical(certificate), encoding="utf-8")
            print(f"WROTE: {output}")
            print(f"RESULT: PASS ({certificate['verification_check_count']} checks)")
            return 0

        verify_checked_in(certificate)
        tamper_count = 0
        if args.tamper_selftest:
            tamper_count = run_tamper_selftest(certificate)
        suffix = f", {tamper_count} tamper mutations detected" if tamper_count else ""
        print(f"RESULT: PASS ({certificate['verification_check_count']} checks{suffix})")
        return 0
    except (AuditError, OSError, json.JSONDecodeError) as error:
        print(f"RESULT: FAIL - {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
