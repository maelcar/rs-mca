#!/usr/bin/env python3
"""Fail-closed verifier for the Route-D priority-zero admission gap."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
BASE = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
FROZEN_RESULT_SHA256 = "687e8616dcbf58cfaaefd4e39e2ef3990aaf79025f0a252f00f57f0ca87cce22"

PREFIX_JSON = Path("experimental/data/certificates/rowsharp-q-prefix-atom-reductions-v1/rowsharp_q_prefix_atom_reductions_v1.json")
SINGLETON_JSON = Path("experimental/data/certificates/rowsharp-q-singleton-topseam-v1/rowsharp_q_singleton_topseam_v1.json")
FIRST_MATCH_NOTE = Path("experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md")
RANK_OWNER_NOTE = Path("experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md")

TREE_BLOBS = {
    PREFIX_JSON: "908ee64976b46b9d8b5bd6015dd8c031dc17df6f",
    SINGLETON_JSON: "6a8aa0c61eeebfa93b97e157b3bc72f8c3dce892",
    FIRST_MATCH_NOTE: "63057656657bed1e9c7ab2e2e515164ccb039d5c",
    RANK_OWNER_NOTE: "ddfce00907f34128b324a64041f4e0ec8957b7d3",
}

NAMES = [
    "generated_field", "quotient_planted", "sparse_pade_hankel",
    "m1_window_shadow", "rank_drop_pivot", "bc_chart", "sp_shift_pair",
    "extension_slope",
]
OLD_ORDER = [
    "contained or noncontained failure", "rank-drop or pivot failure",
    "tangent / common-line / residue-line",
    "quotient-periodic or divisor-stabilized", "planted / prefix-structured",
    "extension-valued slope", "base generated-field collision",
    "sparse sigma or sparse-support", "M1 half-turn / coefficient-shadow",
    "primitive Q-fin residual",
]
EXECUTOR_FIELDS = [
    "typed_projectors", "projector_predicates", "relative_precedence",
    "first_match_disjointness", "owner_recovery", "marked_residual",
    "legacy_order_correspondence",
]

SHIPMENTS = {
    "puncture": ("5343c5876e559e33b6d3bb332cb2d55edbfbcc4b", "experimental/notes/thresholds/route_d_marked_puncture_contact_recursion_v1.md", "7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9", "No executable Route-D first-match predicate is supplied."),
    "rim": ("a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0", "experimental/notes/thresholds/route_d_marked_rim_all_minors_adapter_v1.md", "f24ce928df7e7170c1b4f3228d5fe9b184be50b4", "Actual incidence is load-bearing."),
    "rule2": ("36d560d7421dace47bf48b3fecc9389adaf0977b", "experimental/notes/thresholds/route_d_rule2_wsp_algebraic_preflight_v1.md", "b11def86906c467fc5a1b07caf14a07108b430f6", "does not instantiate a numerical payment theorem"),
    "root": ("91a9e31284adb34a1dfe5c71e434aa709ba2d3fe", "experimental/notes/thresholds/route_d_f31_root_compiler_no_go_v1.md", "97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc", "raw marked support packet = branch-excess unit"),
    "contact": ("332153d6e74403e3ad20f367ff4a3df8406a30bf", "experimental/notes/thresholds/route_d_marked_defect_transfer_no_go_v1.md", "6ce5a571ca05f774a6569a9c78d9cb69e8fc896a", "none is marked-disjoint"),
    "tree": ("909f0c4e1a884f362576b19d4a379656ba3843a1", "experimental/notes/thresholds/route_d_f31_all_depth_tree_no_go_v1.md", "ce926bbdcc96e1168f9440f02ba8f2cfba95dcf6", "|R_D^toy|=4>t=3"),
    "first_match_addback": ("764f1c0243770baa437d4ae790b1448afa091680", "experimental/lean/grande_finale/GrandeFinale/FirstMatchAddBack.lean", "2da56854413d4f77eedab4ea9878f913991202b3", "FirstMatch"),
    "m1_manifest_family": ("168e9ba0280e069a8bd552a6e2098bb9248c70b7", "experimental/data/certificates/m1-a4-spi-atlas-manifest-v1/kb_mca_a1116048_base_generated_family.json", "77285eae5ffed831e1ae4849703c356103798304", "\"scope_complete\""),
}

class Bad(RuntimeError):
    pass

def need(ok: bool, msg: str) -> None:
    if not ok:
        raise Bad(msg)

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def tree_sources() -> dict[Path, bytes]:
    out = {}
    for path, sha in TREE_BLOBS.items():
        data = (ROOT / path).read_bytes()
        need(blob_sha(data) == sha, f"tree blob mismatch: {path}")
        out[path] = data
    return out

def sibling(commit: str, path: str, sha: str, phrase: str) -> int:
    spec = f"{commit}:{path}"
    got = subprocess.run(["git", "rev-parse", spec], cwd=ROOT, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(got.returncode == 0 and got.stdout.strip() == sha, f"cannot resolve {spec}")
    body = subprocess.run(["git", "cat-file", "blob", sha], cwd=ROOT,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(body.returncode == 0 and blob_sha(body.stdout) == sha, f"cannot read {sha}")
    need(phrase.encode() in body.stdout, f"pinned phrase missing: {spec}")
    if path.endswith("kb_mca_a1116048_base_generated_family.json"):
        manifest = json.loads(body.stdout)
        coverage = manifest["coverage"]
        need(coverage["scope_complete"] is False, "M1 scope_complete changed")
        need(coverage["row_complete"] is False, "M1 row_complete changed")
        need(coverage["unit_kind"] == "CAPACITY_INDEX_NOT_CHART", "M1 unit kind changed")
        need(coverage["expected_units"] == 67_472, "M1 expected units changed")
        need(coverage["represented_units"] == 0, "M1 represented units changed")
        need(coverage["missing_units"] == 67_472, "M1 missing units changed")
        family = manifest["compressed_chart_families"]
        need(len(family) == 1 and family[0]["chart_adapter_status"] == "UNPROVEN", "M1 adapter changed")
        need("raw support multiplicity" in manifest["quantifier_scope"]["excluded_scopes"], "M1 raw support exclusion changed")
        need(family[0]["terminal"]["kind"] == "UNPAID_PRIMITIVE", "M1 terminal changed")
    return len(body.stdout)

def snapshot_word_occurrences(word: str) -> int:
    scan = subprocess.run(["git", "grep", "-n", "-w", word, BASE, "--", "experimental"],
                          cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(scan.returncode in (0, 1), f"snapshot grep failed: {word}")
    return sum(len(re.findall(rf"\b{re.escape(word)}\b", line)) for line in scan.stdout.splitlines())

def parse_old(note: str) -> list[str]:
    marker = "This packet uses the following branch order."
    need(marker in note, "old-order marker missing")
    m = re.search(r"```text\n(.*?)\n```", note.split(marker, 1)[1], re.S)
    need(m is not None, "old-order block missing")
    return [x.group(1) for line in m.group(1).splitlines()
            if (x := re.fullmatch(r"\s*\d+\.\s+(.*?)\s*", line))]

def build() -> dict[str, Any]:
    src = tree_sources()
    sib = {name: sibling(*record) for name, record in SHIPMENTS.items()}
    one = json.loads(src[SINGLETON_JSON])
    prefix = json.loads(src[PREFIX_JSON])
    aggregate = one["first_match_order"][0]
    p, t = int(one["parameters"]["p"]), int(one["parameters"]["t"])
    retained = int(one["deployed_arithmetic_closure_if_compiler_is_paid"]["retained_exact_lift_bound"])
    floor = int(one["deployed_arithmetic_closure_if_compiler_is_paid"]["target_floor"])
    tp, cells = t * p, t * (p - 1)
    return {
        "status": "COUNTEREXAMPLE",
        "claim": "SCHEMA_NON_EXECUTABILITY_NOT_NUMERICAL_REFUTATION",
        "schema": {
            "aggregate": aggregate, "keys": sorted(aggregate), "names": NAMES,
            "missing": [x for x in EXECUTOR_FIELDS if x not in aggregate],
            "old_order": parse_old(src[FIRST_MATCH_NOTE].decode()),
            "typed_executor": False, "checked_correspondence": False,
            "D_prim_exact_source_occurrences": snapshot_word_occurrences("D_prim"),
        },
        "semantic_map": {
            "generated_field": "old7_image_only", "quotient_planted": "conflates_old4_old5",
            "sparse_pade_hankel": "changed_semantics", "m1_window_shadow": "approximately_old9",
            "rank_drop_pivot": "old2_moved", "extension_slope": "name_collision_mu_vs_extension_field",
            "bc_chart": "new", "sp_shift_pair": "new", "old1_old3": "omitted", "old10": "terminal",
        },
        "owners": {
            "generated": {"unit": "image_cell", "bound": tp, "support_paid": False},
            "rank": {"unit": "distinct_slope_global_once", "bound": t, "support_paid": False, "rooted_injection": False},
            "planted": {"exact_descent": True, "printed_cost_ledger": False},
            "wsp": {"exact_cost_one": True, "finite_bound": False},
            "strict": {"typed_payment": False}, "row_budget": {"proved": False},
            "slack_is_owner": False,
        },
        "arithmetic": {
            "p": p, "t": t, "tp": tp, "cells": cells, "leaves": 1 + cells,
            "margin": tp - (1 + cells), "retained": retained,
            "paid_plus_retained": tp + retained, "target_floor": floor,
            "slack": floor - (tp + retained),
        },
        "theorem_A": ["finite_marked_universe", "eight_typed_predicates", "unique_first_match_tag", "disjoint_exhaustive", "owner_recovery", "common_core_preservation", "survivor_branch_unit"],
        "theorem_B": ["strict_owner", "planted_ledger", "rank_support_fiber", "marked_contact_owner", "full_rank_wsp_bound", "row_budget", "lhs_is_unpaid_leaf_set"],
        "shipments": {name: {"commit": rec[0], "blob": rec[2], "bytes": sib[name]} for name, rec in SHIPMENTS.items()},
        "prefix_target": prefix["conditional_closure"]["missing_support_certificate"],
        "numerical_refutation": False, "primitive_target_above_bound": False,
    }

def validate(x: dict[str, Any]) -> None:
    need(set(x) == {"status", "claim", "schema", "semantic_map", "owners", "arithmetic", "theorem_A", "theorem_B", "shipments", "prefix_target", "numerical_refutation", "primitive_target_above_bound"}, "top-level keys")
    frozen = hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    need(frozen == FROZEN_RESULT_SHA256, "full emitted result changed")
    need(x["status"] == "COUNTEREXAMPLE", "status")
    need(x["claim"] == "SCHEMA_NON_EXECUTABILITY_NOT_NUMERICAL_REFUTATION", "claim")
    s = x["schema"]
    need(s["names"] == NAMES, "named deletions")
    need(s["aggregate"] == {"examples": NAMES, "name": "earlier_global_first_match_branches", "priority": 0}, "aggregate")
    need(s["keys"] == ["examples", "name", "priority"], "aggregate keys")
    need(s["missing"] == EXECUTOR_FIELDS and not s["typed_executor"], "executor gap")
    need(s["old_order"] == OLD_ORDER and not s["checked_correspondence"], "old correspondence")
    need(s["D_prim_exact_source_occurrences"] == 0, "D_prim occurrence")
    need(x["semantic_map"] == {
        "generated_field": "old7_image_only", "quotient_planted": "conflates_old4_old5",
        "sparse_pade_hankel": "changed_semantics", "m1_window_shadow": "approximately_old9",
        "rank_drop_pivot": "old2_moved", "extension_slope": "name_collision_mu_vs_extension_field",
        "bc_chart": "new", "sp_shift_pair": "new", "old1_old3": "omitted", "old10": "terminal",
    }, "semantic map")
    o = x["owners"]
    need(not o["generated"]["support_paid"] and not o["rank"]["support_paid"], "support owner overclaim")
    need(not o["rank"]["rooted_injection"] and not o["wsp"]["finite_bound"], "missing owner overclaim")
    need(not o["strict"]["typed_payment"] and not o["row_budget"]["proved"] and not o["slack_is_owner"], "payment overclaim")
    need(x["arithmetic"] == {
        "p": 2_130_706_433, "t": 67_472, "tp": 143_763_024_447_376,
        "cells": 143_763_024_379_904, "leaves": 143_763_024_379_905,
        "margin": 67_471, "retained": 11_440,
        "paid_plus_retained": 143_763_024_458_816,
        "target_floor": 274_836_936_291_722_953,
        "slack": 274_693_173_267_264_137,
    }, "arithmetic")
    need(len(x["theorem_A"]) == 7 and len(x["theorem_B"]) == 7, "interfaces")
    need(set(x["shipments"]) == set(SHIPMENTS), "shipments")
    for name, rec in SHIPMENTS.items():
        need(x["shipments"][name]["commit"] == rec[0] and x["shipments"][name]["blob"] == rec[2] and x["shipments"][name]["bytes"] > 0, f"shipment {name}")
    need(x["prefix_target"] == "|G_gen_support(z)| + |D_full_rank_prim(z)| <= t*p", "target")
    need(not x["numerical_refutation"] and not x["primitive_target_above_bound"], "numerical overclaim")

def leaf_paths(value: Any, prefix: tuple[Any, ...] = ()):
    if isinstance(value, dict):
        for key in sorted(value):
            yield from leaf_paths(value[key], prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from leaf_paths(item, prefix + (index,))
    else:
        yield prefix


def mutate_leaf(root: Any, path: tuple[Any, ...]) -> None:
    cursor = root
    for key in path[:-1]:
        cursor = cursor[key]
    key = path[-1]
    value = cursor[key]
    if isinstance(value, bool):
        cursor[key] = not value
    elif isinstance(value, int):
        cursor[key] = value + 1
    elif isinstance(value, str):
        cursor[key] = value + "#"
    elif value is None:
        cursor[key] = "tampered"
    else:
        raise Bad(f"unsupported leaf type: {type(value)}")

def tampers(base: dict[str, Any]) -> tuple[int, int]:
    muts = [
        lambda x: x["schema"]["names"].pop(),
        lambda x: x["schema"]["aggregate"].__setitem__("typed_projectors", []),
        lambda x: x["schema"].__setitem__("typed_executor", True),
        lambda x: x["schema"].__setitem__("checked_correspondence", True),
        lambda x: x["schema"]["old_order"].reverse(),
        lambda x: x["schema"].__setitem__("D_prim_exact_source_occurrences", 1),
        lambda x: x["semantic_map"].__setitem__("rank_drop_pivot", "old2_same_position"),
        lambda x: x["owners"]["generated"].__setitem__("support_paid", True),
        lambda x: x["owners"]["rank"].__setitem__("rooted_injection", True),
        lambda x: x["owners"]["wsp"].__setitem__("finite_bound", True),
        lambda x: x["arithmetic"].__setitem__("tp", 0),
        lambda x: x["arithmetic"].__setitem__("slack", 0),
        lambda x: x["theorem_A"].pop(), lambda x: x["theorem_B"].pop(),
        lambda x: x["shipments"]["tree"].__setitem__("commit", "0" * 40),
        lambda x: x.__setitem__("numerical_refutation", True),
    ]
    rejected = 0
    for mutate in muts:
        trial = copy.deepcopy(base); mutate(trial)
        try: validate(trial)
        except Bad: rejected += 1
    leaves = list(leaf_paths(base))
    for path in leaves:
        trial = copy.deepcopy(base)
        mutate_leaf(trial, path)
        try:
            validate(trial)
        except Bad:
            rejected += 1
    return rejected, len(muts) + len(leaves)

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument("--tamper", action="store_true")
    args = ap.parse_args()
    try:
        result = build(); validate(result)
        if args.tamper:
            got, total = tampers(result); need(got == total, f"tamper {got}/{total}")
            print(f"TAMPER: PASS ({got}/{total})")
        else:
            print(json.dumps({"status": result["status"], "claim": result["claim"], "names": 8, "typed_projectors": 0, "old_branches": 10, "shipments": len(result["shipments"]), "tp": result["arithmetic"]["tp"], "numerical_refutation": False}, sort_keys=True))
            print("RESULT: PASS")
    except (Bad, OSError, ValueError, KeyError) as exc:
        print(f"RESULT: FAIL: {exc}"); return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
