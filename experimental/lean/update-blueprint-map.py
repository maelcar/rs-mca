#!/usr/bin/env python3
"""Map existing Lean declarations into lean-blueprint.json.

This is intentionally a source scanner, not a Lean/Lake verifier.  It answers:

  * which Lean declarations already exist under experimental/lean;
  * which blueprint nodes they plausibly correspond to;
  * which mappings are exact label matches, curated aliases, or name heuristics;
  * which mapped declarations visibly contain `sorry` or `admit`.

The script updates:

  * experimental/lean/lean-blueprint.json
  * experimental/lean/lean-inventory.json
  * experimental/lean/lean-blueprint-report.md
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "experimental" / "lean"
BLUEPRINT = LEAN_ROOT / "lean-blueprint.json"
INVENTORY = LEAN_ROOT / "lean-inventory.json"
REPORT = LEAN_ROOT / "lean-blueprint-report.md"

DECL_RE = re.compile(
    r"^\s*(?:(?:@[\w\[\](),.\s]+)\s*)?"
    r"(?:noncomputable\s+)?(?:private\s+|protected\s+)?"
    r"(theorem|lemma|def|structure|class|inductive|axiom|abbrev|opaque)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*)"
)
LABEL_RE = re.compile(r"\b(?:thm|lem|prop|cor|def|rem|prob):[A-Za-z0-9_.-]+\b")
NAMESPACE_RE = re.compile(r"^\s*namespace\s+(.+)")
END_RE = re.compile(r"^\s*end(?:\s+(.+))?")


@dataclass
class Declaration:
    lean_file: str
    lean_name: str
    short_name: str
    decl_kind: str
    line: int
    source_scan_status: str
    doc_labels: list[str]
    blueprint_matches: list[str]
    mapping_sources: list[str]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def strip_comments(source: str) -> str:
    source = re.sub(r"/--.*?-/", "", source, flags=re.S)
    source = re.sub(r"/-!.*?-/", "", source, flags=re.S)
    source = re.sub(r"/-.*?-/", "", source, flags=re.S)
    source = re.sub(r"--.*", "", source)
    return source


def doc_block_before(lines: list[str], idx: int) -> str:
    """Return immediate doc block before declaration line idx, if present."""
    j = idx - 1
    while j >= 0 and (lines[j].strip() == "" or lines[j].lstrip().startswith("@[")):
        j -= 1
    if j < 0 or "-/" not in lines[j]:
        return ""
    block: list[str] = []
    while j >= 0:
        block.append(lines[j])
        if "/--" in lines[j] or "/-!" in lines[j]:
            return "\n".join(reversed(block))
        j -= 1
    return ""


def block_comment_mask(lines: list[str]) -> list[bool]:
    """Return True for lines whose code starts inside a Lean block comment.

    This is a lightweight scanner for declaration discovery.  It is not a full
    Lean lexer, but it prevents doc/module comments from being misread as code.
    """
    mask: list[bool] = []
    depth = 0
    for line in lines:
        mask.append(depth > 0)
        i = 0
        while i < len(line):
            if depth == 0 and line.startswith("--", i):
                break
            if line.startswith("/-", i):
                depth += 1
                i += 2
                continue
            if depth > 0 and line.startswith("-/", i):
                depth -= 1
                i += 2
                continue
            i += 1
    return mask


def scan_declarations() -> list[Declaration]:
    declarations: list[Declaration] = []
    for path in sorted(LEAN_ROOT.rglob("*.lean")):
        lines = path.read_text(errors="ignore").splitlines()
        in_comment = block_comment_mask(lines)
        decl_line_indices = [
            i for i, line in enumerate(lines) if not in_comment[i] and DECL_RE.match(line)
        ]
        namespace_stack: list[str] = []

        for i, line in enumerate(lines):
            if in_comment[i]:
                continue
            match = DECL_RE.match(line)
            if match:
                decl_kind, short_name = match.groups()
                lean_name = ".".join(namespace_stack + [short_name]) if namespace_stack else short_name
                next_decl = next((j for j in decl_line_indices if j > i), len(lines))
                block = "\n".join(lines[i:next_decl])
                status = (
                    "contains_sorry_or_admit"
                    if re.search(r"\b(sorry|admit)\b", strip_comments(block))
                    else "no_sorry_or_admit_seen"
                )
                doc = doc_block_before(lines, i)
                declarations.append(
                    Declaration(
                        lean_file=rel(path),
                        lean_name=lean_name,
                        short_name=short_name,
                        decl_kind=decl_kind,
                        line=i + 1,
                        source_scan_status=status,
                        doc_labels=LABEL_RE.findall(doc),
                        blueprint_matches=[],
                        mapping_sources=[],
                    )
                )

            ns_match = NAMESPACE_RE.match(line)
            if ns_match:
                namespace_stack.extend(ns_match.group(1).split())
                continue
            end_match = END_RE.match(line)
            if end_match and namespace_stack and not DECL_RE.match(line):
                namespace_stack.pop()

    return declarations


# Curated aliases are intentionally explicit.  They capture renamed labels between
# the current v13 raw manuscript and older Lean packages/correspondence maps.
CURATED_ALIASES: dict[str, list[str]] = {
    "def:capf-staircase": ["StaircaseLogic.Staircase.Staircase"],
    "thm:capf-staircase": [
        "CAP25V13.Threshold.staircase_localization",
        "StaircaseLogic.Staircase.safe_iff_ge_firstSafe",
        "StaircaseLogic.Staircase.firstSafe_unique",
    ],
    "cor:capf-endpoint": [
        "CAP25V13.Threshold.endpoint_radius",
        "StaircaseLogic.Staircase.endpoint_supremum",
    ],
    "thm:capf-corridor": [
        "CAP25V13.Threshold.corridor_lower",
        "CAP25V13.Threshold.corridor_upper",
    ],
    "thm:capf-steepness": [
        "CAP25V13.Threshold.steepness_disjoint",
        "CAP25V13.Threshold.steepness_unsafe",
        "CAP25V13.Threshold.steepness_safe",
    ],
    "prop:capf-extension": ["CAP25V13.Threshold.extPole_exists"],
    "thm:capf-windows": [
        "CAP25V13.Threshold.budget_field_interval",
        "CAP25V13.Threshold.budget_gmax",
        "CAP25V13.Threshold.budget_unsafe",
        "CAP25V13.Threshold.budget_safe",
    ],
    "lem:capf-census-identity": ["CAP25V13.Threshold.census_identity"],
    "thm:capf-census": [
        "CAP25V13.Threshold.census_crossing_relaxed_half",
        "CAP25V13.Threshold.census_crossing_relaxed_quarter",
        "CAP25V13.Threshold.census_crossing_relaxed_eighth",
        "CAP25V13.Threshold.census_crossing_relaxed_sixteenth",
        "CAP25V13.Threshold.census_crossing_dyadic_half",
        "CAP25V13.Threshold.census_crossing_dyadic_sixteenth",
    ],
    "prop:capf-qprofile": [
        "CAP25V13.Threshold.qprofile_bounded",
        "CAP25V13.Threshold.qprofile_dyadic",
    ],
    "prop:capf-integrality": ["CAP25V13.Threshold.residual_absorption"],
    "thm:capf-pma-johnson": [
        "CAP25V13.List.johnson_intersecting_bound",
        "CAP25V13.List.johnson_real_core",
    ],
    "prop:capf-polyfold-planted": [
        "CAP25V13.List.planted_lower_count",
        "CAP25V13.List.planted_monotone",
    ],
    "prop:capf-dyadic-planted": [
        "CAP25V13.List.dyadic_planted_crossing_half",
        "CAP25V13.List.dyadic_planted_crossing_quarter",
        "CAP25V13.List.dyadic_planted_crossing_eighth",
        "CAP25V13.List.dyadic_planted_crossing_sixteenth",
    ],
    "cor:capf-list-unsafe": ["CAP25V13.List.list_unsafe"],
    "cor:capf-list-windows": ["CAP25V13.List.planted_budget_window"],
    "prop:capf-fixed-excess": ["CAP25V13.List.fixed_excess_bound"],
    "cor:capf-fixed-excess-poly": ["CAP25V13.List.few_petal_range"],
    "lem:capf-gap2": ["CAP25V13.Residue.gap2_seam"],
    "lem:capf-dim1": ["CAP25V13.Residue.dim_one_voting"],
    "thm:capf-dim2": ["CAP25V13.Residue.conjF_fixed_dim"],
    "prop:capf-hankel": ["CAP25V13.Residue.hankel_det"],
    "prop:capf-anticode": ["CAP25V13.Residue.anticode_packing"],
    "prop:capf-johnson-exchange": ["CAP25V13.Residue.johnson_ball_count"],
    "thm:johnson-list": ["RSCap.johnson_list_bound"],
    "thm:mca-from-ca": ["RSCap.emca_le_max_eca_tangent"],
    "cor:band-reduction": ["RSCap.emca_le_of_eca_le"],
    "thm:deep-mca": ["RSCap.emcaErr_le_deep", "RSCap.ecaErr_le_deep", "RSCap.rs_emcaErr_le_deep"],
    "lem:mca-monotone": ["RSCap.emca_mono"],
    "lem:diag-invariance": ["RSCap.caBad_diag_imp_mcaBad"],
    "def:ca": ["RSCap.caBad", "RSCap.ecaErr"],
    "def:mca": ["RSCap.mcaBad", "RSCap.emcaErr"],
    "def:dstar": ["RSCap.dStar", "TowardsPrize.dstar"],
    "lem:one-support-one-line": ["RSCap.lem_one_support_one_line"],
    "lem:one-support-d-curve": ["RSCap.lem_one_support_d_curve"],
    "prop:distinct-parameter-line-ledger": ["RSCap.prop_support_family_line_ledger"],
    "thm:exact-quotient-image-lcm-ledger": ["RSCap.prop_support_family_curve_ledger"],
    "lem:quotient-remainder-prefix": ["RSCap.lem_quotient_remainder_prefix"],
    "lem:heaviest-prefix-locator-floor": ["RSCap.lem_heaviest_prefix_locator_floor"],
    "thm:quotient-remainder-deep-floor": ["RSCap.thm_quotient_remainder_deep_floor"],
    "cor:quotient-remainder-trigger": ["RSCap.cor_quotient_remainder_trigger"],
    "cor:quantitative-first-grid-floor": ["RSCap.cor_quantitative_first_grid_floor"],
    "cor:first-grid-cap": ["RSCap.cor_first_grid_cap"],
    "lem:fiber": ["RSCap.lem_fiber_ii"],
    "lem:phi-fiber": ["RSCap.lem_phi_fiber_ii"],
    "thm:phi-cap": ["RSCap.thm_phi_cap"],
    "thm:main": ["RSCap.universal_cap_emca_of_fiber_list", "RSCap.universal_cap_of_fiber_list"],
    "def:rational-smooth": ["RSCap.RationalSmooth"],
    "prop:rational-floor": ["RSCap.prop_rational_floor"],
    "cor:ecfft-onestep": ["RSCap.cor_ecfft_onestep"],
    "prop:graded-rational-floor": ["RSCap.prop_graded_rational_floor"],
    "cor:ecfft-macroscopic": ["RSCap.cor_ecfft_macroscopic"],
    "lem:cheb-fibers": ["RSCap.lem_cheb_fibers"],
    "lem:circle-rs": ["RSCap.lem_circle_rs"],
    "cor:circle-grand": ["RSCap.cor_circle_grand"],
    "lem:stereographic": ["RSCap.lem_stereographic"],
    "prop:small-field": ["RSCap.emca_ge_inv_q", "RSCap.dStar_eq_zero_of_small_field"],
    "thm:scanner-sound": ["RSCap.scanner_deep_safe", "RSCap.scanner_deep_safe_ca"],
    "lem:regular-exact-agreement-eliminant": ["RSCap.lem_regular_exact_agreement_eliminant"],
    "thm:regular-closed-ball-hankel-packing": ["RSCap.thm_regular_closed_ball_hankel_packing"],
    "thm:scanner-checkable-residual-aperiodic-ledger": [
        "RSCap.thm_scanner_checkable_residual_aperiodic_ledger"
    ],
    "prop:onestep": [
        "StaircaseLogic.Staircase.oneStep_isFirstSafe",
        "StaircaseLogic.Staircase.oneStep_firstSafe",
    ],
}


PRIMARY_OVERRIDES = {
    "thm:deep-mca": "RSCap.emcaErr_le_deep",
    "thm:mca-from-ca": "RSCap.emca_le_max_eca_tangent",
    "cor:band-reduction": "RSCap.emca_le_of_eca_le",
    "lem:fiber": "RSCap.lem_fiber_ii",
    "lem:inter": "RSCap.lem_inter_emca",
    "thm:main": "RSCap.universal_cap_emca_of_fiber_list",
    "prop:onestep": "StaircaseLogic.Staircase.oneStep_isFirstSafe",
}


def candidate_labels(decl: Declaration, blueprint_ids: set[str]) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for label in decl.doc_labels:
        if label in blueprint_ids:
            candidates.append((label, "exact_label_match"))

    short = decl.short_name
    for prefix, label_prefix in [
        ("thm_", "thm:"),
        ("lem_", "lem:"),
        ("prop_", "prop:"),
        ("cor_", "cor:"),
        ("def_", "def:"),
        ("rem_", "rem:"),
        ("prob_", "prob:"),
    ]:
        if short.startswith(prefix):
            label = label_prefix + short[len(prefix) :].replace("_", "-")
            if label in blueprint_ids:
                candidates.append((label, "name_heuristic"))

    for label_prefix in ["thm:", "lem:", "prop:", "cor:", "def:"]:
        label = label_prefix + short.replace("_", "-")
        if label in blueprint_ids:
            candidates.append((label, "name_heuristic"))

    return candidates


def build_mappings(
    declarations: list[Declaration], blueprint_ids: set[str]
) -> dict[str, list[dict[str, Any]]]:
    by_name = {d.lean_name: d for d in declarations}
    by_short = {d.short_name: d for d in declarations}
    mappings: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for decl in declarations:
        for label, source in candidate_labels(decl, blueprint_ids):
            d = asdict(decl)
            d["mapping_confidence"] = source
            d["mapping_reason"] = source
            mappings[label].append(d)

    for label, lean_names in CURATED_ALIASES.items():
        if label not in blueprint_ids:
            continue
        for lean_name in lean_names:
            decl = by_name.get(lean_name) or by_short.get(lean_name.split(".")[-1])
            if not decl:
                mappings[label].append(
                    {
                        "lean_file": "",
                        "lean_name": lean_name,
                        "short_name": lean_name.split(".")[-1],
                        "decl_kind": "unknown",
                        "line": None,
                        "source_scan_status": "unresolved",
                        "doc_labels": [],
                        "blueprint_matches": [label],
                        "mapping_sources": ["curated_alias_unresolved"],
                        "mapping_confidence": "curated_alias",
                        "mapping_reason": "curated_alias_unresolved",
                    }
                )
                continue
            d = asdict(decl)
            d["mapping_confidence"] = "curated_alias"
            d["mapping_reason"] = "curated_alias"
            mappings[label].append(d)

    for label in list(mappings):
        seen = set()
        unique = []
        for entry in mappings[label]:
            key = (entry.get("lean_file"), entry.get("lean_name"))
            if key in seen:
                continue
            seen.add(key)
            unique.append(entry)
        mappings[label] = unique

    return dict(mappings)


def entry_score(label: str, entry: dict[str, Any]) -> tuple[int, str, int, str]:
    confidence = entry.get("mapping_confidence", "")
    source_score = {
        "curated_alias": 0,
        "exact_label_match": 1,
        "name_heuristic": 2,
    }.get(confidence, 3)
    preferred = PRIMARY_OVERRIDES.get(label)
    if preferred and entry.get("lean_name") == preferred:
        source_score = -1
    short = entry.get("lean_name", "").split(".")[-1]
    suffix = label.split(":", 1)[1].replace("-", "_")
    name_penalty = 0 if short == suffix or suffix in short else 1
    line = entry.get("line") or 10**9
    return (source_score, name_penalty, line, entry.get("lean_name", ""))


def node_statement_status(entries: list[dict[str, Any]]) -> str:
    statuses = [entry.get("source_scan_status") for entry in entries]
    if any(status == "contains_sorry_or_admit" for status in statuses):
        if any(status == "no_sorry_or_admit_seen" for status in statuses):
            return "lean_mixed_proved_and_skeleton_source_scan"
        return "lean_statement_skeleton_sorry_source_scan"
    if all(status == "no_sorry_or_admit_seen" for status in statuses if status):
        return "lean_statement_present_no_sorry_source_scan"
    return "lean_statement_mapped_source_scan"


def node_confidence(entries: list[dict[str, Any]]) -> str:
    confs = {entry.get("mapping_confidence") for entry in entries}
    if confs == {"exact_label_match"}:
        return "exact_label_match"
    if confs == {"curated_alias"}:
        return "curated_alias"
    if confs == {"name_heuristic"}:
        return "name_heuristic"
    return "mixed"


def node_audit_status(statement_status: str, confidence: str) -> str:
    if statement_status == "lean_statement_skeleton_sorry_source_scan":
        return "mapped_skeleton_needs_proof"
    if statement_status == "lean_mixed_proved_and_skeleton_source_scan":
        return "mapped_split_package_needs_statement_audit"
    if confidence in {"name_heuristic", "mixed"}:
        return "mapped_needs_statement_audit"
    return "mapped_source_scanned_not_built"


def reset_formalization(node: dict[str, Any]) -> None:
    form = node.setdefault("formalization", {})
    form.clear()
    form.update(
        {
            "lean_file": "",
            "lean_name": "",
            "statement_status": "not_started",
            "notes": "",
        }
    )


def apply_mappings(blueprint: dict[str, Any], mappings: dict[str, list[dict[str, Any]]]) -> None:
    nodes = {node["id"]: node for node in blueprint["nodes"]}
    for node in blueprint["nodes"]:
        reset_formalization(node)

    for label, entries in mappings.items():
        if label not in nodes or not entries:
            continue
        ordered = sorted(entries, key=lambda entry: entry_score(label, entry))
        primary = ordered[0]
        related = []
        for entry in ordered:
            related.append(
                {
                    "lean_file": entry.get("lean_file", ""),
                    "lean_name": entry.get("lean_name", ""),
                    "decl_kind": entry.get("decl_kind", ""),
                    "line": entry.get("line"),
                    "source_scan_status": entry.get("source_scan_status", ""),
                    "mapping_confidence": entry.get("mapping_confidence", ""),
                    "mapping_reason": entry.get("mapping_reason", ""),
                }
            )

        confidence = node_confidence(ordered)
        status = node_statement_status(ordered)
        form = nodes[label]["formalization"]
        form.update(
            {
                "lean_file": primary.get("lean_file", ""),
                "lean_name": primary.get("lean_name", ""),
                "statement_status": status,
                "mapping_confidence": confidence,
                "audit_status": node_audit_status(status, confidence),
                "notes": (
                    "Mapped from existing Lean source by update-blueprint-map.py. "
                    f"Primary selected from {len(ordered)} related declaration(s); "
                    "source-level scan only, Lake not run."
                ),
                "related_lean": related,
            }
        )

    mapped_nodes = [
        node
        for node in blueprint["nodes"]
        if node.get("formalization", {}).get("statement_status") != "not_started"
    ]
    blueprint.setdefault("mapping_policy", {}).update(
        {
            "direction": (
                "Lean-to-blueprint: existing Lean declarations and correspondence notes "
                "are mapped into TeX blueprint nodes, not used to create new blueprint nodes."
            ),
            "verification_scope": (
                "Source-level scan only. statement_status records whether the mapped "
                "declaration block visibly contains sorry/admit; no Lake build was run."
            ),
            "primary_selection": (
                "A primary lean_file/lean_name is selected for convenience. related_lean "
                "preserves all matched declarations for split Lean proof packages."
            ),
            "confidence_values": {
                "exact_label_match": "Lean doc comment names the exact TeX blueprint label.",
                "curated_alias": "Explicit alias from local Lean correspondence maps or package headers.",
                "name_heuristic": "Declaration name normalizes to a blueprint label.",
                "mixed": "More than one mapping source was used for the node.",
            },
        }
    )
    counts = blueprint.setdefault("counts", {})
    counts["lean_mapped_nodes"] = len(mapped_nodes)
    counts["lean_unmapped_nodes"] = len(blueprint["nodes"]) - len(mapped_nodes)
    counts["lean_related_declarations"] = sum(
        len(node.get("formalization", {}).get("related_lean", [])) for node in mapped_nodes
    )
    counts["tex_conjecture_environments"] = counts.get("by_environment", {}).get("conjecture", 0)
    counts["conjectural_target_nodes"] = sum(
        1 for node in blueprint["nodes"] if node.get("kind") == "conjectural_target"
    )
    counts["certificate_target_nodes"] = sum(
        1 for node in blueprint["nodes"] if node.get("kind") == "certificate_target"
    )
    counts["final_goal_nodes"] = sum(
        1 for node in blueprint["nodes"] if node.get("kind") == "final_goal"
    )
    note = (
        "Lean mapping is generated by experimental/lean/update-blueprint-map.py; "
        "related_lean entries record split theorem packages and source-scan proof status."
    )
    if note not in blueprint.setdefault("notes", []):
        blueprint["notes"].append(note)


def update_inventory(declarations: list[Declaration], mappings: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    matches_by_decl: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for label, entries in mappings.items():
        for entry in entries:
            key = (entry.get("lean_file", ""), entry.get("lean_name", ""))
            if not key[0] or not key[1]:
                continue
            matches_by_decl[key].append(
                {
                    "blueprint_id": label,
                    "mapping_confidence": entry.get("mapping_confidence", ""),
                    "mapping_reason": entry.get("mapping_reason", ""),
                }
            )

    inventory_decls = []
    for decl in declarations:
        key = (decl.lean_file, decl.lean_name)
        matches = sorted(matches_by_decl.get(key, []), key=lambda item: item["blueprint_id"])
        inventory_decls.append(
            {
                **asdict(decl),
                "blueprint_matches": [match["blueprint_id"] for match in matches],
                "mapping_sources": sorted({match["mapping_confidence"] for match in matches}),
            }
        )

    return {
        "schema_version": "0.1",
        "purpose": "Reverse Lean declaration inventory for CAP25 blueprint mapping.",
        "source_root": "experimental/lean",
        "verification_scope": "Source scan only; no Lake build was run.",
        "counts": {
            "lean_files": len(list(LEAN_ROOT.rglob("*.lean"))),
            "declarations": len(inventory_decls),
            "mapped_declarations": sum(1 for decl in inventory_decls if decl["blueprint_matches"]),
            "unmapped_declarations": sum(1 for decl in inventory_decls if not decl["blueprint_matches"]),
            "by_decl_kind": dict(Counter(decl["decl_kind"] for decl in inventory_decls)),
            "by_source_scan_status": dict(Counter(decl["source_scan_status"] for decl in inventory_decls)),
        },
        "declarations": inventory_decls,
    }


def dependency_closure(blueprint: dict[str, Any], root_id: str) -> set[str]:
    by_id = {node["id"]: node for node in blueprint["nodes"]}
    seen: set[str] = set()
    queue: deque[str] = deque([root_id])
    while queue:
        current = queue.popleft()
        if current in seen or current not in by_id:
            continue
        seen.add(current)
        for dep in by_id[current].get("depends_on", []):
            if dep not in seen:
                queue.append(dep)
    return seen


def render_report(blueprint: dict[str, Any], inventory: dict[str, Any]) -> str:
    nodes = blueprint["nodes"]
    mapped = [
        node for node in nodes if node.get("formalization", {}).get("statement_status") != "not_started"
    ]
    unmapped = [node for node in nodes if node.get("formalization", {}).get("statement_status") == "not_started"]
    by_module = defaultdict(lambda: [0, 0])
    for node in nodes:
        row = by_module[node.get("module", "miscellaneous")]
        row[0] += 1
        if node in mapped:
            row[1] += 1

    status_counts = Counter(node.get("formalization", {}).get("statement_status") for node in nodes)
    confidence_counts = Counter(
        node.get("formalization", {}).get("mapping_confidence", "unmapped") for node in nodes
    )
    audit_counts = Counter(node.get("formalization", {}).get("audit_status", "unmapped") for node in nodes)

    lines: list[str] = []
    lines.append("# Lean Blueprint Coverage Report")
    lines.append("")
    lines.append("Generated by `experimental/lean/update-blueprint-map.py`.")
    lines.append("")
    lines.append("Scope: source-level scan only. No Lake build was run.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Blueprint nodes: `{len(nodes)}`")
    lines.append(f"- Mapped blueprint nodes: `{len(mapped)}`")
    lines.append(f"- Unmapped blueprint nodes: `{len(unmapped)}`")
    lines.append(f"- Related Lean declarations attached to mapped nodes: `{blueprint['counts'].get('lean_related_declarations')}`")
    lines.append(f"- Lean declarations inventoried: `{inventory['counts']['declarations']}`")
    lines.append(f"- Lean declarations mapped to at least one blueprint node: `{inventory['counts']['mapped_declarations']}`")
    lines.append("")
    lines.append("## Mapping Status")
    lines.append("")
    for key, value in sorted(status_counts.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Mapping Confidence")
    lines.append("")
    for key, value in sorted(confidence_counts.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Audit Status")
    lines.append("")
    for key, value in sorted(audit_counts.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Mapped Nodes By Module")
    lines.append("")
    lines.append("| Module | Mapped | Total |")
    lines.append("| --- | ---: | ---: |")
    for module, (total, mapped_count) in sorted(by_module.items()):
        lines.append(f"| `{module}` | {mapped_count} | {total} |")
    lines.append("")

    lines.append("## Q / BC / SP Dependency Closures")
    lines.append("")
    by_id = {node["id"]: node for node in nodes}
    for target in [
        "target:Q_prefix_flatness",
        "target:BC_base_field_split_pencil",
        "target:SP_primitive_shift_pair_control",
        "target:finite_adjacent_deployed_ledgers",
        "target:RS_MCA_full_resolution",
    ]:
        closure = dependency_closure(blueprint, target)
        mapped_in = [
            node_id
            for node_id in sorted(closure)
            if by_id[node_id].get("formalization", {}).get("statement_status") != "not_started"
        ]
        unmapped_in = sorted(closure - set(mapped_in))
        lines.append(f"### `{target}`")
        lines.append("")
        lines.append(f"- Closure nodes including target: `{len(closure)}`")
        lines.append(f"- Mapped in closure: `{len(mapped_in)}`")
        lines.append(f"- Unmapped in closure: `{len(unmapped_in)}`")
        if mapped_in:
            lines.append("- Mapped:")
            for node_id in mapped_in[:25]:
                form = by_id[node_id].get("formalization", {})
                lines.append(f"  - `{node_id}` -> `{form.get('lean_name')}`")
        if unmapped_in:
            lines.append("- Unmapped:")
            for node_id in unmapped_in[:40]:
                lines.append(f"  - `{node_id}`")
        lines.append("")

    skeleton = [
        node
        for node in mapped
        if node.get("formalization", {}).get("statement_status")
        in {"lean_statement_skeleton_sorry_source_scan", "lean_mixed_proved_and_skeleton_source_scan"}
    ]
    lines.append("## Nodes With Skeleton Or Mixed Lean Status")
    lines.append("")
    if not skeleton:
        lines.append("None.")
    else:
        for node in sorted(skeleton, key=lambda item: item["id"]):
            form = node["formalization"]
            lines.append(
                f"- `{node['id']}` -> `{form.get('lean_name')}` "
                f"({form.get('statement_status')}, {form.get('audit_status')})"
            )
    lines.append("")

    high_priority_modules = {
        "q_prefix_flatness",
        "bc_split_pencil",
        "sp_shift_pairs",
        "frontier_final_targets",
        "capg_final_frontier_package",
        "staircase_and_certificates",
    }
    lines.append("## Unmapped High-Priority Nodes")
    lines.append("")
    priority_unmapped = [
        node
        for node in unmapped
        if node.get("module") in high_priority_modules or node.get("id", "").startswith("target:")
    ]
    for node in sorted(priority_unmapped, key=lambda item: (item.get("module", ""), item["id"])):
        lines.append(f"- `{node['id']}` ({node.get('module')}, {node.get('kind')})")
    lines.append("")

    lines.append("## Reverse Inventory Notes")
    lines.append("")
    lines.append(
        "`lean-inventory.json` is the authoritative reverse list of Lean declarations. "
        "A declaration with an empty `blueprint_matches` list exists in Lean but is not yet "
        "mapped to a CAP25 v13 raw blueprint node."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate and print counts without writing")
    args = parser.parse_args()

    blueprint = json.loads(BLUEPRINT.read_text())
    blueprint_ids = {node["id"] for node in blueprint["nodes"]}
    declarations = scan_declarations()
    mappings = build_mappings(declarations, blueprint_ids)
    apply_mappings(blueprint, mappings)
    inventory = update_inventory(declarations, mappings)
    report = render_report(blueprint, inventory)

    if args.check:
        print(json.dumps(blueprint["counts"], indent=2))
        print(json.dumps(inventory["counts"], indent=2))
        return

    BLUEPRINT.write_text(json.dumps(blueprint, indent=2, sort_keys=False) + "\n")
    INVENTORY.write_text(json.dumps(inventory, indent=2, sort_keys=False) + "\n")
    REPORT.write_text(report)
    print(f"updated {rel(BLUEPRINT)}")
    print(f"wrote {rel(INVENTORY)}")
    print(f"wrote {rel(REPORT)}")
    print(f"mapped blueprint nodes: {blueprint['counts']['lean_mapped_nodes']}")


if __name__ == "__main__":
    main()
