#!/usr/bin/env python3
"""Fail-closed binder for the dense-shell INV-TAIL dependency audit.

This verifier does not prove INV-TAIL.  It checks that the note, finite-grid
verifier, deep certificate, Lean scope statement, and agents log all expose the
same open mathematical interface.  The emitted certificate binds those source
artifacts by SHA-256 and deliberately separates finite-check success from the
OPEN_GAP mathematical verdict.

stdlib only; deterministic; no repository files are changed except when an
explicit --emit-certificate path is supplied.
"""

import argparse
import copy
import hashlib
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT_CERT_REL = (
    "experimental/data/certificates/"
    "dense-shell-inv-tail-dependency-audit/"
    "dense_shell_inv_tail_dependency_audit.json"
)
DEFAULT_CERT = ROOT / AUDIT_CERT_REL
SNAPSHOT = "a5750192a2fb4ff7e9f6b2f6bf77fa6652dffda7"

SOURCES = {
    "audit_note":
        "experimental/notes/audits/dense_shell_inv_tail_dependency_audit.md",
    "threshold_note":
        "experimental/notes/thresholds/dense_shell_class_charges.md",
    "class_verifier":
        "experimental/scripts/verify_dense_shell_class_charges.py",
    "class_certificate":
        "experimental/data/certificates/dense-shell-class-charges/"
        "dense_shell_class_charges.json",
    "lean_shadow":
        "experimental/lean/dense_shell_class_charges/"
        "DenseShellClassCharges.lean",
    "agents_log": "experimental/agents-log.md",
    "audit_verifier":
        "experimental/scripts/verify_dense_shell_inv_tail_dependency_audit.py",
}

ALLOWED_LOG_STATUSES = {
    "PROVED", "CONDITIONAL", "CONJECTURAL", "EXPERIMENTAL", "AUDIT",
    "COUNTEREXAMPLE",
}


def normalized(text):
    return re.sub(r"\s+", " ", text).strip()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_artifacts():
    return {name: (ROOT / rel).read_text(encoding="utf-8")
            for name, rel in SOURCES.items()}


def finite_number(value):
    return isinstance(value, (int, float)) and math.isfinite(value)


class Recorder:
    def __init__(self):
        self.checks = []
        self.failures = []

    def require(self, name, condition, detail):
        self.checks.append(name)
        if not condition:
            self.failures.append((name, detail))


def evaluate(artifacts):
    rec = Recorder()
    audit = artifacts["audit_note"]
    threshold = artifacts["threshold_note"]
    verifier = artifacts["class_verifier"]
    lean = artifacts["lean_shadow"]
    log = artifacts["agents_log"]
    naudit = normalized(audit)
    nthreshold = normalized(threshold)
    nverifier = normalized(verifier)
    master_pair_block = verifier.split("def master_pair_env", 1)[-1].split(
        "\ndef gate_env", 1)[0]

    try:
        class_cert = json.loads(artifacts["class_certificate"])
    except (TypeError, json.JSONDecodeError) as exc:
        rec.require("class-certificate-json", False, "invalid JSON: %s" % exc)
        class_cert = {}
    else:
        rec.require("class-certificate-json", True, "valid JSON")

    # Audit-note contract and remaining obligations.
    rec.require("audit-open-gap",
                "Status: OPEN GAP / AUDIT" in audit,
                "audit note must retain the fail-closed OPEN GAP verdict")
    rec.require("audit-contract-split",
                "INV-TAIL-SHARP" in audit and "INV-TAIL-LOOSE" in audit,
                "sharp and loose tail contracts must remain distinct")
    rec.require("audit-computed-scope", "COMPUTED" in audit,
                "finite floating grids must be labeled COMPUTED")
    rec.require("audit-p8-implication-only", "implication-only" in audit,
                "P8 must remain implication-only")
    rec.require("audit-c3b-direction", "IMPLIED BY" in audit,
                "C3b must expose one-way per-prefix sufficiency")
    rec.require("audit-charge-formula",
                "omega_U = W_U + ((1+s_U)/2) Sigma_U" in audit,
                "parity-dependent C6 identity missing")
    rec.require("audit-broad-pair-negative-control",
                "1.61013636047 > 1.61" in audit,
                "broad pair-2 negative control missing")
    rec.require("audit-finite-continuum-obligation",
                "rigorously enclose the finite P7/P9/P12 continuum ranges"
                in naudit,
                "finite continuum/error coverage must remain open")
    rec.require("audit-general-k-open", "general-K positivity remains" in audit
                and "CONJECTURAL" in audit,
                "general-K conjecture must remain separate")

    # Threshold note: exact consumed scope and corrected semantic interfaces.
    rec.require("threshold-c3-conditional",
                "CONDITIONAL THEOREM (C3" in threshold,
                "C3 may not be advertised as unconditional")
    rec.require("threshold-contract-split",
                "INV-TAIL-SHARP" in threshold
                and "INV-TAIL-LOOSE" in threshold,
                "threshold note must name both tail contracts")
    rec.require("threshold-correlated-scope",
                "exact correlated Master pairs" in threshold
                and "exact Master-pair secants" in threshold,
                "P7/INV-TAIL scope must be the correlated Master pairs")
    rec.require("threshold-c3b-direction", "is IMPLIED BY" in nthreshold,
                "per-prefix positivity must be sufficient, not equivalent")
    rec.require("threshold-no-prefix-equivalence",
                "is EQUIVALENT to positivity of every decorated subtree"
                not in nthreshold,
                "old C3b equivalence wording returned")
    rec.require("threshold-charge-formula",
                "omega(class) = W_U + ((1+eps_U)/2) Sigma_U" in threshold,
                "corrected parity-dependent charge formula missing")
    rec.require("threshold-no-uniform-charge",
                "omega(class) = h_+ = Sigma_U + W_U always" not in nthreshold,
                "old parity-blind charge formula returned")
    rec.require("threshold-computed-finite",
                "COMPUTED (deterministic floating grids" in threshold
                and "no interval or" in threshold,
                "finite P7/P9/P12 scope must remain floating-grid evidence")
    rec.require("threshold-finite-obligation",
                "rigorous continuum/error coverage for the finite P7/P9/P12"
                in nthreshold,
                "tail proof must not erase the finite continuum obligation")

    # Original verifier: exact domains, complete coverage, strict CLI, and v2.
    for name, token, detail in (
        ("verifier-strict-cli", "def parse_cli(argv)",
         "strict CLI parser missing"),
        ("verifier-correlated-pair1",
         "x = 7.0 / 36.0 - eps / 9.0",
         "pair-1 correlated formula missing"),
        ("verifier-correlated-pair2",
         "x = 5.0 / 12.0 - eps / 9.0",
         "pair-2 correlated formula missing"),
        ("verifier-finite-guards", "math.isfinite",
         "non-finite coefficient guards missing"),
        ("verifier-shape-guards", "shape_mismatches",
         "shape coverage guards missing"),
        ("verifier-expected-counts", "expected_coefficients",
         "expected coefficient counts missing"),
        ("verifier-exact-key-endpoint", "Fend = F(0.25)",
         "KEY must be evaluated at the exact endpoint"),
        ("verifier-charge-tamper", '"charge-uniform"',
         "parity-blind charge tamper missing"),
        ("verifier-open-gap-schema", '"mathematical_verdict": "OPEN_GAP"',
         "OPEN_GAP certificate field missing"),
        ("verifier-deep-scope", '"deep_scope": ["P7", "P12"]',
         "deep scope must be limited to P7/P12"),
    ):
        rec.require(name, token in verifier, detail)
    rec.require("verifier-no-length-truncation",
                "min(len(gx), len(gy))" not in master_pair_block,
                "correlated Master-pair arrays may not be silently truncated")
    rec.require("verifier-no-unqualified-pass-schema",
                '"pass": bool(allok)' not in verifier
                and '"verdict": "PASS"' not in verifier,
                "v2 generator must not emit an unqualified PASS verdict")
    rec.require("verifier-deep-emission",
                'deep = "--deep" in CLI' in verifier
                and "run(deep=deep)" in verifier,
                "--emit-cert must honor --deep")

    # Deep class certificate.  All qualified PASS values are finite checks.
    cc = class_cert
    rec.require("cert-schema", cc.get("schema") ==
                "dense-shell-class-charges/v2", "unexpected schema")
    rec.require("cert-qualified-status",
                cc.get("check_status") == "PASS"
                and cc.get("finite_checks_pass") is True
                and cc.get("mathematical_verdict") == "OPEN_GAP"
                and cc.get("all_depth_proved") is False
                and "pass" not in cc and "verdict" not in cc,
                "finite PASS must be qualified and all-depth verdict open")
    rec.require("cert-deep-scope",
                cc.get("deep") is True
                and cc.get("deep_scope") == ["P7", "P12"]
                and cc.get("envelope_share_horizon_jmax") == 48,
                "deep P7/P12 horizon must be exactly 48")
    rec.require("cert-gate-horizons",
                cc.get("gate_horizons") == {
                    "P6_L4": 12, "P7_envelope": 48,
                    "P9_direct_master": 16, "P12_share": 48,
                }, "per-gate horizons are incomplete or ambiguous")
    rec.require("cert-open-dependencies",
                cc.get("inv_tail_status") == "OPEN"
                and cc.get("general_k_status") == "CONJECTURAL",
                "tail/general-K statuses must remain open")
    contracts = cc.get("inv_tail_contracts", {})
    rec.require("cert-contracts",
                contracts.get("sharp_correlated") == {
                    "pair1_cap": 0.85, "pair2_cap": 1.61,
                    "share_floor": 1.2,
                }
                and contracts.get("loose") == {
                    "pair1_cap": 1.086, "pair2_cap": 1.663,
                    "share_floor": 1.2,
                }
                and contracts.get("proved") is False,
                "sharp/loose contract metadata mismatch")
    rec.require("cert-evidence-method",
                "no interval continuum certificate"
                in cc.get("evidence_method", ""),
                "certificate must deny continuum certification")

    env = cc.get("envelope_sups", {})
    rec.require("cert-envelope-domain",
                cc.get("envelope_scope") ==
                "exact-correlated-master-pairs"
                and env.get("scope") == "exact-correlated-master-pairs"
                and env.get("level_range") == [2, 48]
                and env.get("epsilon_grid_subintervals") == 400
                and env.get("domains") == {
                    "epsilon": "[0,1/4]",
                    "pair1": ["7/36-epsilon/9", "1/4+epsilon/9"],
                    "pair2": ["5/12-epsilon/9", "17/36+epsilon/9"],
                }, "correlated envelope domain metadata mismatch")
    rec.require("cert-envelope-values",
                finite_number(env.get("pair1_correlated"))
                and env.get("pair1_correlated") <= 0.85
                and finite_number(env.get("pair2_correlated"))
                and env.get("pair2_correlated") <= 1.61
                and finite_number(env.get("pair1_tail_j_ge_8"))
                and env.get("pair1_tail_j_ge_8") <= 0.65
                and finite_number(env.get("broad_pair2_counterexample"))
                and env.get("broad_pair2_counterexample") > 1.61,
                "envelope evidence or broad negative control mismatch")
    ecov = env.get("coefficient_coverage", {})
    rec.require("cert-envelope-coverage",
                ecov.get("pair1_checked_coefficients") ==
                ecov.get("pair1_expected_coefficients")
                and ecov.get("pair2_checked_coefficients") ==
                ecov.get("pair2_expected_coefficients")
                and (ecov.get("pair1_expected_coefficients") or 0) > 0
                and (ecov.get("pair2_expected_coefficients") or 0) > 0
                and ecov.get("invalid_coefficients") == 0
                and ecov.get("shape_mismatches") == 0
                and ecov.get("nonpositive_or_omitted_coefficients") == 0,
                "P7 must bind equal checked/expected counts with no omissions")

    share = cc.get("share_coverage", {})
    rec.require("cert-share-coverage",
                share.get("checked_coefficients") ==
                share.get("expected_coefficients")
                and (share.get("expected_coefficients") or 0) > 0
                and share.get("invalid_coefficients") == 0
                and share.get("shape_mismatches") == 0
                and share.get("nonpositive_or_omitted_coefficients") == 0
                and share.get("level_range") == [6, 48]
                and share.get("epsilon_samples") == 199
                and finite_number(cc.get("share_floor"))
                and cc.get("share_floor") >= 1.20,
                "P12 coverage or floor mismatch")
    key = cc.get("key_margins", {})
    rec.require("cert-key-implication-margins",
                finite_number(key.get("sharp_endpoint_margin"))
                and key.get("sharp_endpoint_margin") >= 0.029
                and finite_number(key.get("loose_grid_min_margin"))
                and key.get("loose_grid_min_margin") >= 0.014,
                "P8 supplied-constant margins are missing")
    charge = cc.get("charge_identity", {})
    witness = charge.get("legacy_counterexample", {})
    rec.require("cert-charge-identity",
                finite_number(charge.get("max_identity_deviation"))
                and charge.get("max_identity_deviation") < 1e-9
                and witness.get("B") == 4 and witness.get("mask") == 1
                and finite_number(witness.get("legacy_gap"))
                and witness.get("legacy_gap") > 3.0,
                "corrected charge identity or pinned B4 witness mismatch")

    # Lean is deliberately a bounded decidable shadow, not analytic coverage.
    rec.require("lean-explicit-noncoverage",
                "analytic content (the MASTER inequality, cone purity, "
                "the leak table) lives in" in normalized(lean),
                "Lean module must state its analytic noncoverage")
    declarations = re.findall(r"^(?:def|theorem)\s+([A-Za-z0-9_]+)",
                              lean, flags=re.MULTILINE)
    forbidden = ("invtail", "master", "envelope", "childshare",
                 "classsum", "chargeidentity")
    rec.require("lean-no-analytic-declarations",
                not any(any(word in decl.lower() for word in forbidden)
                        for decl in declarations),
                "Lean declarations unexpectedly claim analytic coverage")

    # Only the newly added log entry is status-gated; do not reinterpret history.
    marker = "### 2026-07-17 - Dense-shell INV-TAIL dependency audit"
    start = log.find(marker)
    end = log.find("\n### ", start + len(marker)) if start >= 0 else -1
    entry = log[start:(len(log) if end < 0 else end)] if start >= 0 else ""
    match = re.search(r"^- \*\*Status:\*\* (.+?)\.$", entry,
                      flags=re.MULTILINE)
    statuses = ([part.strip() for part in match.group(1).split("/")]
                if match else [])
    rec.require("agents-log-entry", bool(entry)
                and "verify_dense_shell_inv_tail_dependency_audit.py" in entry
                and "dense-shell-inv-tail-dependency-audit" in entry,
                "new audit entry or bound artifact paths missing")
    rec.require("agents-log-template-status",
                statuses == ["AUDIT"]
                and all(status in ALLOWED_LOG_STATUSES for status in statuses),
                "new entry must choose the single appropriate template status")
    rec.require("agents-log-no-invented-status",
                "OPEN GAP" not in (match.group(1) if match else ""),
                "OPEN GAP belongs in audit prose, not agents-log Status")

    return rec, class_cert


def make_certificate(artifacts, rec, class_cert):
    env = class_cert["envelope_sups"]
    return {
        "schema": "dense-shell-inv-tail-dependency-audit/v1",
        "audit_checks_status": "PASS",
        "mathematical_verdict": "OPEN_GAP",
        "all_depth_proved": False,
        "finite_artifacts_consistent": True,
        "upstream_snapshot": SNAPSHOT,
        "generated_by": SOURCES["audit_verifier"],
        "source_sha256": {
            SOURCES[name]: sha256_text(artifacts[name])
            for name in sorted(SOURCES)
        },
        "checks": rec.checks,
        "class_certificate_summary": {
            "schema": class_cert["schema"],
            "check_status": class_cert["check_status"],
            "mathematical_verdict": class_cert["mathematical_verdict"],
            "deep_scope": class_cert["deep_scope"],
            "envelope_share_horizon_jmax":
                class_cert["envelope_share_horizon_jmax"],
            "gate_horizons": class_cert["gate_horizons"],
            "inv_tail_status": class_cert["inv_tail_status"],
            "general_k_status": class_cert["general_k_status"],
            "envelope_scope": class_cert["envelope_scope"],
            "pair1_correlated": env["pair1_correlated"],
            "pair2_correlated": env["pair2_correlated"],
            "broad_pair2_counterexample":
                env["broad_pair2_counterexample"],
            "share_floor": class_cert["share_floor"],
        },
        "remaining_obligations": [
            "rigorous finite P7/P9/P12 continuum and rounding enclosures",
            "INV-TAIL-SHARP, or SHARE+CROSS+L4' closure for INV-TAIL-LOOSE",
            "uniform general-K positivity",
        ],
    }


def print_failures(rec):
    for name, detail in rec.failures:
        print("  [FAIL] %s: %s" % (name, detail))


def json_mutation(raw, mutate):
    obj = json.loads(raw)
    mutate(obj)
    return json.dumps(obj, sort_keys=True)


def run_tamper_selftest(base):
    variants = []

    def text_variant(name, key, old, new, replace_all=False):
        tampered = copy.deepcopy(base)
        if old not in tampered[key]:
            raise RuntimeError("tamper anchor missing: %s" % name)
        tampered[key] = (tampered[key].replace(old, new) if replace_all
                         else tampered[key].replace(old, new, 1))
        variants.append((name, tampered))

    text_variant("audit-status-promotion", "audit_note",
                 "Status: OPEN GAP / AUDIT", "Status: PROVED")
    text_variant("computed-to-proved", "audit_note", "COMPUTED", "PROVED",
                 replace_all=True)
    text_variant("c3b-equivalence-regression", "threshold_note",
                 "is IMPLIED BY", "is EQUIVALENT to")
    text_variant("uniform-charge-regression", "audit_note",
                 "omega_U = W_U + ((1+s_U)/2) Sigma_U",
                 "omega_U = Sigma_U + W_U always")
    text_variant("broaden-pair-scope", "threshold_note",
                 "exact correlated Master pairs", "all admissible pair supports")
    text_variant("remove-nonfinite-guards", "class_verifier",
                 "math.isfinite", "finite_guard_removed", replace_all=True)
    text_variant("invent-log-status", "agents_log",
                 "- **Status:** AUDIT.",
                 "- **Status:** OPEN GAP.")

    for name, mutation in (
        ("certificate-promotes-tail",
         lambda obj: obj.__setitem__("mathematical_verdict", "PROVED")),
        ("certificate-shallow-horizon",
         lambda obj: obj.__setitem__("envelope_share_horizon_jmax", 16)),
        ("certificate-omits-coefficient",
         lambda obj: obj["envelope_sups"]["coefficient_coverage"].__setitem__(
             "pair1_checked_coefficients",
             obj["envelope_sups"]["coefficient_coverage"]
                ["pair1_checked_coefficients"] - 1)),
        ("certificate-reopens-unqualified-pass",
         lambda obj: obj.__setitem__("pass", True)),
    ):
        tampered = copy.deepcopy(base)
        tampered["class_certificate"] = json_mutation(
            tampered["class_certificate"], mutation)
        variants.append((name, tampered))

    caught = 0
    for name, tampered in variants:
        rec, _ = evaluate(tampered)
        ok = bool(rec.failures)
        caught += int(ok)
        print("  [%s] %s%s" %
              ("PASS" if ok else "FAIL", name,
               " (caught)" if ok else " (NOT CAUGHT)"))
    print("TAMPER SELFTEST: %d/%d caught" % (caught, len(variants)))
    return caught == len(variants)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check", nargs="?", const=str(DEFAULT_CERT),
                       metavar="CERTIFICATE",
                       help="check current sources against a certificate")
    modes.add_argument("--emit-certificate", metavar="CERTIFICATE",
                       help="write a source-bound certificate")
    modes.add_argument("--tamper-selftest", action="store_true",
                       help="run in-memory semantic negative controls")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    artifacts = load_artifacts()

    if args.tamper_selftest:
        return 0 if run_tamper_selftest(artifacts) else 1

    rec, class_cert = evaluate(artifacts)
    if rec.failures:
        print_failures(rec)
        print("AUDIT CHECK: FAIL (%d/%d semantic checks failed)" %
              (len(rec.failures), len(rec.checks)))
        return 1
    expected = make_certificate(artifacts, rec, class_cert)

    if args.emit_certificate:
        path = Path(args.emit_certificate)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(expected, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8")
        print("AUDIT CHECK: PASS (%d/%d)" %
              (len(rec.checks), len(rec.checks)))
        print("certificate written:", path)
        return 0

    path = Path(args.check)
    try:
        actual = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("AUDIT CHECK: FAIL (cannot read certificate: %s)" % exc)
        return 1
    if actual != expected:
        print("AUDIT CHECK: FAIL (certificate/source binding mismatch)")
        actual_hashes = actual.get("source_sha256", {})
        for rel, digest in expected["source_sha256"].items():
            if actual_hashes.get(rel) != digest:
                print("  stale source hash:", rel)
        print("regenerate with --emit-certificate", path)
        return 1
    print("AUDIT CHECK: PASS (%d/%d; source binding exact)" %
          (len(rec.checks), len(rec.checks)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
