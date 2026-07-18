#!/usr/bin/env python3
"""Independent audit of the balanced-core producer-to-atlas interface.

Standard-library only. The checker pins the reviewed producer, repaired
consumers, certificate, historical consumers, and conditional Lean boundary;
replays normal and optimized modes; and proves in isolation that the retired
raw-to-residual label, a tampered JSON ledger, and a missing JSON ledger fail.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
ATLAS_SCRIPT = Path("experimental/scripts/verify_atlas_cat_ledger.py")
ATLAS_CERTIFICATE = Path(
    "experimental/data/certificates/atlas-cat-ledger/atlas_cat_ledger.json"
)
KAPPA_SCRIPT = Path("experimental/scripts/verify_kappa_growth.py")
A4_SCRIPT = Path("experimental/scripts/verify_a4_coverage.py")
FACTORED_SCRIPT = Path(
    "experimental/scripts/verify_balanced_core_factored_rank.py"
)
POST_SCRIPT = Path(
    "experimental/scripts/verify_post_sweep_reconciliation_c23dcaa.py"
)
TEX_SOURCE = Path("experimental/asymptotic_rs_mca_frontiers.tex")

RETIRED_LABEL = "residual charts force kappa = k = Theta(n)"
CORRECTED_LABEL = (
    "raw empty-core prefix families, including the PTM family and the finite "
    "census below, can have `kappa = k = Theta(n)`"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "df79dad137e2ff8241eb35c8bafe977454508917eb2fa714a302e6467f10862d"
)
NEGATIVE_CERTIFICATE_SHA256 = (
    "e49c7c09cab46463dc511272a861e814fd89f778d35f7e753bb906ee24bcbb91"
)
SOURCE_SHA256 = {
    "experimental/scripts/verify_atlas_cat_ledger.py":
        "eade976ae2bade621515c3ac30b735cc58fcb97b468583f85d9382caa75495fe",
    "experimental/notes/thresholds/atlas_cat_cell_ledger.md":
        "a4138d8dcc205bea0957396e1c9ca73779bae48c67764b8c17ab534581993764",
    str(ATLAS_CERTIFICATE):
        EXPECTED_CERTIFICATE_SHA256,
    str(KAPPA_SCRIPT):
        "d1ed722f0139be9f69c5b917abf425543849a4edc8ee75dab768aa1930fa7cbb",
    str(A4_SCRIPT):
        "d171bf89bd755f927b7edcdd8ce2d4c7192e970c601c1f0b77594d3b7623b50a",
    "experimental/notes/thresholds/balanced_core_kappa_growth.md":
        "3a426b40907941afb8065172c81b9177d38fcdf2065a23d5c40cbece6a122410",
    "experimental/notes/thresholds/a4_covers_high_kappa.md":
        "1056567b6caba31c8ab31b95f58bdc01bd2fa8d4b3ba2d21b8c5f14346ab84a6",
    "experimental/notes/audits/balanced_core_factored_rank_audit.md":
        "1c06e8e4f2c483a9dca81a79ae29edb9d7e5d776b86b88c15497d1407590ee6c",
    str(FACTORED_SCRIPT):
        "6d6b38230ef748da6ed37244110841e21ff325caf32cd575d9bff906fc347d36",
    "experimental/data/certificates/balanced-core-factored-rank/"
    "balanced_core_factored_rank.json":
        "b53d34728090219f9fd3e5a88e28d9af7858c5b8cf40a397fe2bfd58f73bbd33",
    "experimental/notes/roadmaps/b2_l1_reduction_ledger.md":
        "bd35b82b5cec35639b0bf539e15709b53e3316dae0c2b8e298953db424fb0435",
    "experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md":
        "40a847b7e0e425d952868cd2f4bfe8db27639051754edbd518754c25d68929a6",
    "experimental/notes/thresholds/mi_ma_sidon_route_audit.md":
        "fdcaad63b9552b48687bf74898d6574aeda6218e226d5f40a77cb71a50ff8926",
    "experimental/notes/thresholds/pte_extremality_image_face.md":
        "cd5928525b0b7193ff75f2b280615a3090c69351f63c13b72584990d90a13fe7",
    "experimental/scripts/verify_pte_extremality.py":
        "16271f53a5f1e6968a54cc9642810da948df470d160219475ccf055413e0682e",
    "experimental/notes/thresholds/post_sweep_reconciliation_c23dcaa.md":
        "db7859e670302a2f72047bcb4767d84cd74c46841968e1b5cb3bfaf5a58ed943",
    str(POST_SCRIPT):
        "d2bf620395d29de414d9ab679490af8aebfd2b1321caae8eade5bbc427f4df18",
    "experimental/lean/asymptotic_spine/HIGH_KAPPA_COVERAGE_AUDIT.md":
        "b5697d85a394425eb97e9fb6a15ce115b74eb668c46a16b383155b8ff5ffc103",
    "experimental/lean/asymptotic_spine/AsymptoticSpine/HighKappaCoverage.lean":
        "f5c90441f12fc49d07d196f2fca7d4afe4e6817cb9195c55560995ae71348107",
    str(TEX_SOURCE):
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
}
CHECKS: list[tuple[str, bool]] = []


class AuditError(RuntimeError):
    """Raised when an audit gate fails."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm_ws(value: str) -> str:
    return " ".join(value.split())


def check(name: str, condition: bool) -> None:
    passed = bool(condition)
    CHECKS.append((name, passed))
    if not passed:
        raise AuditError(name)


def read(relative: str | Path, root: Path = ROOT) -> str:
    return (root / relative).read_text(encoding="utf-8")


def run_script(
    relative: Path,
    *arguments: str,
    optimized: bool = False,
    root: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.append(str(root / relative))
    command.extend(arguments)
    return subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def output(result: subprocess.CompletedProcess[str]) -> str:
    return result.stdout + result.stderr


def passed(result: subprocess.CompletedProcess[str], marker: str) -> bool:
    return result.returncode == 0 and marker in output(result)


def rejected(result: subprocess.CompletedProcess[str], marker: str) -> bool:
    return result.returncode != 0 and marker in output(result)


def copy_atlas_packet(destination: Path) -> None:
    notes_source = ROOT / "experimental/notes/thresholds"
    notes_target = destination / "experimental/notes/thresholds"
    shutil.copytree(notes_source, notes_target)
    for relative in (ATLAS_SCRIPT, ATLAS_CERTIFICATE, TEX_SOURCE):
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)


def audit() -> None:
    check(
        "producer, consumers, certificates, TeX, and Lean boundary match pins",
        all(
            (ROOT / relative).is_file()
            and sha256(ROOT / relative) == expected
            for relative, expected in SOURCE_SHA256.items()
        ),
    )

    source_note = norm_ws(
        read("experimental/notes/thresholds/balanced_core_kappa_growth.md")
    )
    a4_note = norm_ws(
        read("experimental/notes/thresholds/a4_covers_high_kappa.md")
    )
    check(
        "corrected source separates raw families, shortening, and actual slopes",
        "raw empty-core prefix families" in source_note
        and "positive-rate actual first-match balanced-core residual" in source_note
        and "raw support-family stress test" in a4_note
        and "not proof that the PTM pair is a surviving balanced-core cell"
        in a4_note,
    )

    atlas_text = read(ATLAS_SCRIPT)
    kappa_text = read(KAPPA_SCRIPT)
    a4_text = read(A4_SCRIPT)
    check(
        "repaired verifiers reject the retired raw-to-residual wording",
        CORRECTED_LABEL in atlas_text
        and RETIRED_LABEL not in atlas_text
        and RETIRED_LABEL not in kappa_text
        and RETIRED_LABEL not in a4_text
        and "raw empty-core prefix families can have" in kappa_text
        and "raw prefix family only; realized slopes not counted" in a4_text
        and "len(kappas_seen) >= 3" in a4_text,
    )

    preflight = norm_ws(
        read(
            "experimental/notes/thresholds/"
            "a6_actual_witness_core_rank_preflight.md"
        )
    )
    b2_ledger = norm_ws(
        read("experimental/notes/roadmaps/b2_l1_reduction_ledger.md")
    )
    check(
        "hash-frozen downstream overclaims are present and explicitly audited",
        "genuinely occurs on relevant balanced cores" in preflight
        and "syndrome-secant bound is VACUOUS on the residual "
        "`kappa=Theta(n)` cores" in b2_ledger
        and "Prouhet-Thue-Morse residual family" in b2_ledger,
    )

    certificate = json.loads(read(ATLAS_CERTIFICATE))
    c8 = next(row for row in certificate["cells"] if row["id"] == "C8")
    check(
        "frozen atlas ledger binds 219/219, 4/4, and C8 producer provenance",
        sha256(ROOT / ATLAS_CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
        and certificate["verifier_result"]
        == {"check": "PASS 219/219", "tamper_selftest": "PASS 4/4"}
        and certificate["all_pass"] is True
        and set(c8["prs"]) == {518, 528, 534, 868},
    )

    atlas = run_script(ATLAS_SCRIPT, "--check")
    check(
        "repaired atlas normal mode passes 219/219 and checks frozen ledger",
        passed(atlas, "RESULT: PASS (219/219)")
        and "frozen certificate binds verifier results and C8 provenance"
        in atlas.stdout,
    )
    atlas_opt = run_script(ATLAS_SCRIPT, "--check", optimized=True)
    check(
        "repaired atlas optimized mode passes 219/219",
        passed(atlas_opt, "RESULT: PASS (219/219)"),
    )
    atlas_tamper = run_script(ATLAS_SCRIPT, "--tamper-selftest")
    atlas_tamper_opt = run_script(
        ATLAS_SCRIPT, "--tamper-selftest", optimized=True
    )
    check(
        "atlas TeX-anchor tamper suite remains 4/4 in normal and optimized modes",
        passed(atlas_tamper, "RESULT: PASS (4/4)")
        and passed(atlas_tamper_opt, "RESULT: PASS (4/4)"),
    )

    kappa = run_script(KAPPA_SCRIPT)
    check(
        "raw kappa verifier normal mode passes 95 with honest output boundary",
        passed(kappa, "RESULT: PASS (95 checks)")
        and "[Group D] raw empty-core prefix families can have" in kappa.stdout
        and RETIRED_LABEL not in kappa.stdout,
    )
    kappa_opt = run_script(KAPPA_SCRIPT, optimized=True)
    check(
        "raw kappa verifier optimized mode passes 95 with the same boundary",
        passed(kappa_opt, "RESULT: PASS (95 checks)")
        and "[Group D] raw empty-core prefix families can have" in kappa_opt.stdout,
    )

    a4 = run_script(A4_SCRIPT)
    check(
        "A4 verifier normal mode passes 63 and exercises kappa 4,5,6",
        passed(a4, "RESULT: PASS (63 checks)")
        and "raw prefix family only; realized slopes not counted" in a4.stdout
        and "kappas seen: [4, 5, 6]" in a4.stdout,
    )
    a4_opt = run_script(A4_SCRIPT, optimized=True)
    check(
        "A4 verifier optimized mode passes 63 with the same boundary cases",
        passed(a4_opt, "RESULT: PASS (63 checks)")
        and "kappas seen: [4, 5, 6]" in a4_opt.stdout,
    )

    factored = run_script(FACTORED_SCRIPT)
    factored_opt = run_script(FACTORED_SCRIPT, optimized=True)
    check(
        "factored-rank producer passes normal and optimized exact replays",
        passed(factored, "kappa=1 != k=2")
        and passed(factored_opt, "kappa=1 != k=2"),
    )
    factored_tamper = run_script(FACTORED_SCRIPT, "--tamper-selftest")
    factored_tamper_opt = run_script(
        FACTORED_SCRIPT, "--tamper-selftest", optimized=True
    )
    check(
        "factored-rank producer rejects 5/5 tamper cases in both modes",
        passed(factored_tamper, "tamper self-test rejected 5/5")
        and passed(factored_tamper_opt, "tamper self-test rejected 5/5"),
    )

    post = run_script(POST_SCRIPT, "--check")
    post_opt = run_script(POST_SCRIPT, "--check", optimized=True)
    check(
        "historical post-sweep consumer remains 83/83 in both modes",
        passed(post, "RESULT: PASS (83/83)")
        and passed(post_opt, "RESULT: PASS (83/83)"),
    )

    lean_source = read(
        "experimental/lean/asymptotic_spine/"
        "AsymptoticSpine/HighKappaCoverage.lean"
    )
    lean_audit = read(
        "experimental/lean/asymptotic_spine/HIGH_KAPPA_COVERAGE_AUDIT.md"
    )
    check(
        "Lean consumer is conditional finite routing, not actual-residual existence",
        "does not prove that a family is asymptotically shallow" in lean_source
        and "residual inclusion" in lean_source
        and "NOT CLAIMED" in lean_audit
        and all(token not in lean_source for token in ("sorry", "admit", "axiom ")),
    )

    mi_note = norm_ws(
        read("experimental/notes/thresholds/mi_ma_sidon_route_audit.md")
    )
    pte_note = norm_ws(
        read("experimental/notes/thresholds/pte_extremality_image_face.md")
    )
    pte_script = norm_ws(read("experimental/scripts/verify_pte_extremality.py"))
    check(
        "standalone MI/MA and PTE provenance no longer claims an attained residual",
        "raw PTE prefix-support family" in mi_note
        and "does not certify survival as an actual first-match residual" in mi_note
        and "does not attain that many realized slopes" in pte_note
        and "not an attained realized-slope extremal" in pte_script,
    )

    with tempfile.TemporaryDirectory(
        prefix="balanced-core-atlas-consumer-audit-"
    ) as tmp:
        isolated = Path(tmp)
        copy_atlas_packet(isolated)
        isolated_script = isolated / ATLAS_SCRIPT
        repaired_bytes = isolated_script.read_bytes()
        repaired_text = repaired_bytes.decode("utf-8")
        check(
            "negative-control setup finds exactly one corrected atlas label",
            repaired_text.count(CORRECTED_LABEL) == 1,
        )

        isolated_script.write_text(
            repaired_text.replace(CORRECTED_LABEL, RETIRED_LABEL),
            encoding="utf-8",
        )
        retired = run_script(ATLAS_SCRIPT, "--check", root=isolated)
        retired_opt = run_script(
            ATLAS_SCRIPT, "--check", optimized=True, root=isolated
        )
        check(
            "retired raw-to-residual label fails 218/219 in both modes",
            rejected(retired, "RESULT: FAIL (218/219)")
            and rejected(retired_opt, "RESULT: FAIL (218/219)")
            and "balanced_core_kappa_growth.md carries its cited self-label"
            in output(retired),
        )

        isolated_script.write_bytes(repaired_bytes)
        isolated_certificate = isolated / ATLAS_CERTIFICATE
        clean_certificate = isolated_certificate.read_bytes()
        tampered_certificate = clean_certificate.replace(
            b'"base_sha": "ea4eb0784417ca5ab503a3c31a7eef6464ad100a"',
            b'"base_sha": "fa4eb0784417ca5ab503a3c31a7eef6464ad100a"',
        )
        isolated_certificate.write_bytes(tampered_certificate)
        check(
            "negative-control certificate has the pinned deterministic SHA-256",
            sha256(isolated_certificate) == NEGATIVE_CERTIFICATE_SHA256,
        )
        cert_failure = run_script(ATLAS_SCRIPT, "--check", root=isolated)
        cert_failure_opt = run_script(
            ATLAS_SCRIPT, "--check", optimized=True, root=isolated
        )
        check(
            "tampered frozen ledger fails read-only in normal and optimized modes",
            rejected(cert_failure, "RESULT: FAIL (218/219)")
            and rejected(cert_failure_opt, "RESULT: FAIL (218/219)")
            and sha256(isolated_certificate) == NEGATIVE_CERTIFICATE_SHA256,
        )

        isolated_certificate.unlink()
        missing = run_script(ATLAS_SCRIPT, "--check", root=isolated)
        missing_opt = run_script(
            ATLAS_SCRIPT, "--check", optimized=True, root=isolated
        )
        check(
            "missing frozen ledger fails in normal and optimized modes",
            rejected(missing, "RESULT: FAIL")
            and rejected(missing_opt, "RESULT: FAIL"),
        )


def main() -> int:
    if sys.argv[1:] not in ([], ["--check"]):
        print(
            "usage: verify_balanced_core_atlas_consumer_audit.py [--check]",
            file=sys.stderr,
        )
        return 2
    try:
        audit()
        for name, passed_gate in CHECKS:
            print(("ok  " if passed_gate else "FAIL") + "  " + name)
        print(f"atlas_certificate_sha256: {EXPECTED_CERTIFICATE_SHA256}")
        print(f"negative_control_sha256: {NEGATIVE_CERTIFICATE_SHA256}")
        print(f"RESULT: PASS ({len(CHECKS)}/{len(CHECKS)})")
        print("STATUS: COUNTEREXAMPLE")
        return 0
    except (AuditError, OSError, ValueError, KeyError, StopIteration) as error:
        for name, passed_gate in CHECKS:
            print(("ok  " if passed_gate else "FAIL") + "  " + name)
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        print("STATUS: COUNTEREXAMPLE")
        return 1


if __name__ == "__main__":
    sys.exit(main())
