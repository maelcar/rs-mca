#!/usr/bin/env python3
"""Independent audit for the lower-reserve deep-remainder certificate contract.

Standard-library only. The checker binds the repaired source packet, replays
normal and optimized target modes, and exercises stale, missing, and explicitly
regenerated frozen-certificate states in an isolated temporary directory.
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
TARGET_REL = Path("experimental/scripts/verify_lower_reserve_deep_remainder.py")
CERT_REL = Path(
    "experimental/data/certificates/lower-reserve-deep-remainder/"
    "deep_remainder_atlas.json"
)
EXPECTED_CERT_SHA256 = (
    "e9815f14e0be85c5b5489d98a944392cbcc997389eed10d2dd05e6860c507016"
)
NEGATIVE_CERT_SHA256 = (
    "cec46fea6988b0a2d868fe208712e9759174d04dd074b2bafba904ee6a50ad7d"
)
SOURCE_SHA256 = {
    "experimental/notes/thresholds/lower_reserve_deep_remainder_atlas.md":
        "a44bad2171efa07d4c2546f932055c244b2fcd95e5dd1e929e63830a235c6139",
    "experimental/scripts/verify_lower_reserve_deep_remainder.py":
        "e31de8b93e68cf49b67770583442962c54adb7053ca20f26b385d2bf2282a9ac",
    str(CERT_REL):
        EXPECTED_CERT_SHA256,
    "experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py":
        "47886a6a3c9d31017b175606cb96336fed7b00bb7f7a5532d4f1c35364b9674c",
    "experimental/notes/thresholds/lower_reserve_o5c_profile_lists.md":
        "97fbf00c01a9b41f516f61110920700b7dc04096d80e1573c26e521c685018ea",
    "experimental/notes/thresholds/post_sweep_reconciliation_c23dcaa.md":
        "db7859e670302a2f72047bcb4767d84cd74c46841968e1b5cb3bfaf5a58ed943",
    "experimental/asymptotic_rs_mca_frontiers.tex":
        "0e3aa7b1ba79b1065439ae484f4cb989d80cabe18afb68ec63a6b21d1f3370fd",
}
CHECKS: list[tuple[str, bool]] = []


class AuditError(RuntimeError):
    """Raised when an audit gate fails."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def check(name: str, condition: bool) -> None:
    passed = bool(condition)
    CHECKS.append((name, passed))
    if not passed:
        raise AuditError(name)


def run_target(root: Path, mode: str, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(root / TARGET_REL), mode])
    return subprocess.run(
        command,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def target_passed(result: subprocess.CompletedProcess[str], marker: str) -> bool:
    output = result.stdout + result.stderr
    return result.returncode == 0 and marker in output


def target_rejected(result: subprocess.CompletedProcess[str], marker: str) -> bool:
    output = result.stdout + result.stderr
    return result.returncode != 0 and marker in output


def copy_target_packet(destination: Path) -> None:
    for relative in (TARGET_REL, CERT_REL):
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, output)


def audit() -> None:
    check(
        "repaired note, verifier, certificate, companion, consumers, and TeX match pins",
        all((ROOT / relative).is_file() and sha256(ROOT / relative) == expected
            for relative, expected in SOURCE_SHA256.items()),
    )

    stored = json.loads((ROOT / CERT_REL).read_text(encoding="utf-8"))
    check(
        "frozen certificate has 44/44 gates and strict-deep list 6 > identity 1",
        stored.get("checks_total") == 44
        and stored.get("checks_pass") == 44
        and stored.get("key_numbers", {}).get("guaranteed_list_strict_deep_F169") == 6
        and stored.get("key_numbers", {}).get("identity_floor_strict_deep_F169") == 1,
    )

    clean_hash = sha256(ROOT / CERT_REL)
    normal = run_target(ROOT, "--check")
    check(
        "normal --check passes 44/44, checks the certificate, and does not mutate it",
        target_passed(normal, "RESULT: PASS 44/44")
        and "certificate check: PASS" in normal.stdout
        and sha256(ROOT / CERT_REL) == clean_hash,
    )

    optimized = run_target(ROOT, "--check", optimized=True)
    check(
        "optimized --check passes 44/44, checks the certificate, and does not mutate it",
        target_passed(optimized, "RESULT: PASS 44/44")
        and "certificate check: PASS" in optimized.stdout
        and sha256(ROOT / CERT_REL) == clean_hash,
    )

    math_tamper = run_target(ROOT, "--tamper-selftest")
    check(
        "normal mathematical tamper suite remains 10/10",
        target_passed(math_tamper, "RESULT: PASS 10/10"),
    )

    math_tamper_opt = run_target(ROOT, "--tamper-selftest", optimized=True)
    check(
        "optimized mathematical tamper suite remains 10/10",
        target_passed(math_tamper_opt, "RESULT: PASS 10/10"),
    )

    with tempfile.TemporaryDirectory(prefix="deep-remainder-cert-audit-") as tmp:
        isolated = Path(tmp)
        copy_target_packet(isolated)
        isolated_cert = isolated / CERT_REL

        tampered = json.loads(isolated_cert.read_text(encoding="utf-8"))
        tampered["key_numbers"]["guaranteed_list_strict_deep_F169"] = 7
        isolated_cert.write_bytes(canonical_json_bytes(tampered))
        check(
            "negative-control certificate has the independently reproduced SHA-256",
            sha256(isolated_cert) == NEGATIVE_CERT_SHA256,
        )

        rejected = run_target(isolated, "--check")
        check(
            "normal --check rejects the tampered frozen certificate",
            target_rejected(rejected, "frozen certificate mismatch"),
        )
        check(
            "normal rejection leaves the tampered certificate byte-identical",
            sha256(isolated_cert) == NEGATIVE_CERT_SHA256,
        )

        rejected_opt = run_target(isolated, "--check", optimized=True)
        check(
            "optimized --check rejects without rewriting the tampered certificate",
            target_rejected(rejected_opt, "frozen certificate mismatch")
            and sha256(isolated_cert) == NEGATIVE_CERT_SHA256,
        )

        regenerated = run_target(isolated, "--write")
        check(
            "only explicit --write restores the reviewed canonical certificate",
            target_passed(regenerated, "RESULT: PASS 44/44")
            and "certificate written:" in regenerated.stdout
            and sha256(isolated_cert) == EXPECTED_CERT_SHA256,
        )

        isolated_cert.unlink()
        missing = run_target(isolated, "--check")
        check(
            "missing frozen certificate is rejected",
            target_rejected(missing, "missing frozen certificate"),
        )


def main() -> int:
    if sys.argv[1:] not in ([], ["--check"]):
        print(
            "usage: verify_lower_reserve_deep_remainder_certificate_freshness_audit.py "
            "[--check]",
            file=sys.stderr,
        )
        return 2
    try:
        audit()
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        print(f"certificate_sha256: {EXPECTED_CERT_SHA256}")
        print(f"negative_control_sha256: {NEGATIVE_CERT_SHA256}")
        print(f"RESULT: PASS ({len(CHECKS)}/{len(CHECKS)})")
        print("STATUS: COUNTEREXAMPLE")
        return 0
    except (AuditError, OSError, ValueError, json.JSONDecodeError) as error:
        for name, passed in CHECKS:
            print(("ok  " if passed else "FAIL") + "  " + name)
        print(f"RESULT: FAIL: {error}", file=sys.stderr)
        print("STATUS: COUNTEREXAMPLE")
        return 1


if __name__ == "__main__":
    sys.exit(main())
