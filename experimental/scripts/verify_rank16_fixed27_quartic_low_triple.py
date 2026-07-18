#!/usr/bin/env python3
"""Replay the finite fixed-27 quartic low-triple certificate."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


B = 32_768
D = 63_601
W = 28_897
BASE_CAP = 12_997
PASSING_DEFICIT = 7_319
UNION_CORRECTION = 7_320
P = 2_130_706_433
OMEGA = 1_548_376_985

CERTIFICATE_DIR = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "rank16-fixed27-quartic-low-triple"
)

EXPECTED_HASHES = {
    "independent_field_and_pasch_selftest.py":
        "0628b024daf5aaef80edf5d4859a643b59ba6d9e3a762f307fed073aca969135",
    "independent_field_and_pasch_selftest.expected.txt":
        "c57f426613f0a462cefd142bfcd72c2b7e97df4ebdf22df90da6978537ce1258",
    "independent_low_triple_arithmetic.py":
        "1fd93482ced6dfe45b0cb1a7eee49c85c317e40ee7d4bc304b6eb82e318ba937",
    "independent_low_triple_arithmetic.expected.txt":
        "8f1759c4c2732012981613c5fb153809c2bfbdc6d5f2036522f8dad6883b9106",
    "independent_split_quartic_audit.cpp":
        "9ca0a0fc0a331a346bd68f5929ab19a06c80c14257e223d5701806523d40c8b0",
    "independent_split_quartic_audit.expected.txt":
        "4313da63584beed2bd9bf1a0bd338e0d245aa43523b61e7279f70abe31c46883",
    "independent_triple_line_bound.py":
        "5c2009116a2e552d38ec8b3af36fbaf1cbf3fa4f6d66d75ab910524ac4e6fb1a",
    "independent_triple_line_bound.expected.txt":
        "f12d1ea94930be3e278707c66868e73753c0193068b334a0ed421ead9b371e9c",
}

FAILED: list[str] = []
PASSED = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global PASSED
    if ok:
        PASSED += 1
    else:
        FAILED.append(name)
    suffix = f" ({detail})" if detail else ""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_certificate_manifest() -> tuple[bool, str]:
    manifest = CERTIFICATE_DIR / "SHA256SUMS.txt"
    listed: dict[str, str] = {}
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        listed[name] = digest
    actual_names = {
        path.name for path in CERTIFICATE_DIR.iterdir()
        if path.is_file() and path.name != manifest.name
    }
    if set(listed) != actual_names:
        return False, f"listed={sorted(listed)} actual={sorted(actual_names)}"
    mismatches = [name for name, digest in listed.items()
                  if sha256(CERTIFICATE_DIR / name) != digest]
    return not mismatches, "all entries" if not mismatches else ",".join(mismatches)


def ceil_div(a: int, b: int) -> int:
    return -((-a) // b)


def balanced_pair_sum(total: int, cells: int = 5) -> int:
    q, rem = divmod(total, cells)
    return rem * (q + 1) * q + (cells - rem) * q * (q - 1)


def arithmetic_scan(deficit: int) -> tuple[int, int, int, int, tuple[int, ...]]:
    states = feasible = interval_infeasible = capacity_infeasible = 0
    best: tuple[int, ...] | None = None
    for c in range(BASE_CAP + 1):
        r = D - c
        lam = W - c
        stage = 1
        while stage <= 8_192:
            if r % stage == 0:
                states += 1
                n_min = stage * ceil_div(5 * lam - deficit, stage)
                local_degree = lam // stage
                total = n_min // stage
                if n_min > 2 * r:
                    interval_infeasible += 1
                elif total > 5 * local_degree:
                    capacity_infeasible += 1
                else:
                    feasible += 1
                    quotient_order = B // stage
                    lower = balanced_pair_sum(total)
                    upper = (quotient_order - 1) * (2 * local_degree - 2)
                    row = (
                        lower - upper,
                        c,
                        lam,
                        r,
                        stage,
                        quotient_order,
                        n_min,
                        total,
                        local_degree,
                        lower,
                        upper,
                    )
                    if best is None or row < best:
                        best = row
            stage *= 2
    assert best is not None
    return states, feasible, interval_infeasible, capacity_infeasible, best


def run_python_certificate(name: str) -> tuple[bool, str]:
    source = CERTIFICATE_DIR / f"{name}.py"
    expected = (CERTIFICATE_DIR / f"{name}.expected.txt").read_text()
    command = [sys.executable]
    if not __debug__:
        command.append("-O")
    command.append(str(source))
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    ok = result.returncode == 0 and result.stdout == expected and not result.stderr
    return ok, hashlib.sha256(result.stdout.encode()).hexdigest()


def run_full_census() -> tuple[bool, str]:
    source = CERTIFICATE_DIR / "independent_split_quartic_audit.cpp"
    expected = (CERTIFICATE_DIR / "independent_split_quartic_audit.expected.txt").read_text()
    compiler = shutil.which(os.environ.get("CXX", "c++"))
    if compiler is None:
        return False, "no C++ compiler found"
    with tempfile.TemporaryDirectory(prefix="rs_mca_role06_") as directory:
        binary = Path(directory) / "split_quartic_audit"
        compile_result = subprocess.run(
            [compiler, "-std=c++17", "-O2", "-Wall", "-Wextra", "-pedantic",
             str(source), "-o", str(binary)],
            capture_output=True,
            text=True,
            check=False,
        )
        if compile_result.returncode != 0:
            return False, compile_result.stderr.strip() or "compilation failed"
        result = subprocess.run(
            [str(binary)], capture_output=True, text=True, check=False
        )
    ok = result.returncode == 0 and result.stdout == expected and not result.stderr
    return ok, hashlib.sha256(result.stdout.encode()).hexdigest()


def run(tamper: str | None, full_census: bool) -> bool:
    manifest_ok, manifest_detail = verify_certificate_manifest()
    check("certificate SHA256SUMS", manifest_ok, manifest_detail)
    for name, expected_hash in sorted(EXPECTED_HASHES.items()):
        actual_hash = sha256(CERTIFICATE_DIR / name)
        check(f"artifact hash {name}", actual_hash == expected_hash, actual_hash)

    omega = OMEGA + 1 if tamper == "field-order" else OMEGA
    check("field order divides 64", pow(omega, 64, P) == 1)
    check("field order is exactly 64", pow(omega, 32, P) != 1)
    check("field factorization", P - 1 == 127 * 2**24)

    passing_deficit = 7_320 if tamper == "deficit-off-by-one" else PASSING_DEFICIT
    scan = arithmetic_scan(passing_deficit)
    expected_scan = (
        25_996,
        19_346,
        6_647,
        3,
        (28, 12_401, 16_496, 51_200, 2_048, 16, 75_776, 37, 8, 238, 210),
    )
    check("passing-deficit state partition", scan[:4] == expected_scan[:4], str(scan[:4]))
    check("passing-deficit strict minimum", scan[4] == expected_scan[4], str(scan[4]))

    next_scan = arithmetic_scan(7_320)
    expected_next = (
        25_996,
        19_350,
        6_643,
        3,
        (-6_766, 12_997, 15_900, 50_604, 1, 32_768, 72_180,
         72_180, 15_900, 1_041_918_300, 1_041_925_066),
    )
    check("one-farther state partition", next_scan[:4] == expected_next[:4], str(next_scan[:4]))
    check("one-farther certificate failure", next_scan[4] == expected_next[4], str(next_scan[4]))

    union_floor = (7 * D - 5 * W + UNION_CORRECTION) // 2
    union_expected = 154_020 if tamper == "union-floor" else 154_021
    check("union numerator is even", (7 * D - 5 * W + UNION_CORRECTION) % 2 == 0)
    check("seven-residual union floor", union_floor == union_expected, str(union_floor))

    for name in (
        "independent_low_triple_arithmetic",
        "independent_triple_line_bound",
        "independent_field_and_pasch_selftest",
    ):
        ok, output_hash = run_python_certificate(name)
        check(f"certificate replay {name}", ok, output_hash)

    census_text = (
        CERTIFICATE_DIR / "independent_split_quartic_audit.expected.txt"
    ).read_text()
    target_line = "target_profiles=1" if tamper == "census-target" else "target_profiles=0"
    check("split-quartic census excludes target profile", target_line in census_text)
    check("split-quartic census has 11,328 unique Pasch configurations",
          "pasch_unique=11328 raw_paths=67968" in census_text)
    check("split-quartic census profile partition",
          "profile=8,2,4,0 count=10880" in census_text
          and "profile=12,0,4,0 count=448" in census_text)

    if full_census:
        ok, detail = run_full_census()
        check("compiled split-quartic census replay", ok, detail)

    total = PASSED + len(FAILED)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} ({PASSED}/{total})")
    return not FAILED


def tamper_selftest() -> bool:
    caught = 0
    tampers = ("field-order", "deficit-off-by-one", "union-floor", "census-target")
    for tamper in tampers:
        result = subprocess.run(
            [sys.executable, __file__, "--tamper", tamper],
            capture_output=True,
            text=True,
            check=False,
        )
        detected = result.returncode != 0 and "RESULT: FAIL" in result.stdout
        caught += int(detected)
        print(f"tamper {tamper}: {'caught' if detected else 'MISSED'}")
    print(f"TAMPER SELFTEST: {caught}/{len(tampers)} caught")
    return caught == len(tampers)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tamper",
        choices=("field-order", "deficit-off-by-one", "union-floor", "census-target"),
    )
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--full-census", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        return 0 if tamper_selftest() else 1
    return 0 if run(args.tamper, args.full_census) else 1


if __name__ == "__main__":
    raise SystemExit(main())
