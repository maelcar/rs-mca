#!/usr/bin/env python3
"""Replay the audited last-predeep cube-fiber profile obstruction.

Standard library only. The checker binds the exact integer identities to the
source interfaces consumed by the proof, replays the cube and square endpoint
families, and rejects scope-changing semantic mutations. It does not certify
semantic C1--C9 ownership or a complete replacement exclusion.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/last-predeep-cube-fiber-profile-obstruction"
CLAIM_PATH = CERT / "claim.json"
SOURCE_PINS_PATH = CERT / "source_pins.json"
MANIFEST_PATH = CERT / "manifest.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def check_source_pins() -> tuple[int, int]:
    pins = json.loads(SOURCE_PINS_PATH.read_text(encoding="utf-8"))
    require(
        pins["base"] == "9908454995f3f195cfe748f35a1135211609d066",
        "wrong publication base",
    )
    anchors = 0
    for relative, expected in pins["files"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing source file: {relative}")
        require(digest(path) == expected, f"source hash drift: {relative}")
    for relative, required in pins["required_anchors"].items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for anchor in required:
            require(anchor in text, f"source anchor drift: {relative}: {anchor}")
            anchors += 1
    return len(pins["files"]), anchors


def check_claim(claim: dict[str, object]) -> None:
    require(claim["minimum_cube_s"] == 65, "cube endpoint drift")
    require(claim["minimum_square_s"] == 129, "square endpoint drift")
    require(claim["target_denominator_exponent"] == 128, "target drift")
    require(claim["target_frozen_first"] is True, "target chronology drift")
    require(claim["full_challenge_field"] is True, "challenge drift")
    require(claim["domain_is_full_multiplicative_group"] is True, "domain drift")
    require(claim["cube_redundancy"] == 8, "cube redundancy drift")
    require(claim["cube_radius"] == 3, "cube radius drift")
    require(claim["cube_exact_numerator"] == "(q-1)/3", "numerator drift")
    require(claim["profile_maximum"] == 1, "profile maximum drift")
    require(claim["safe_on_equality"] is True, "safe-boundary drift")
    require(
        claim["one_sided_cut"] == "B_star>=U is sufficient; exact only when E=U",
        "one-sided cut overclaimed",
    )
    require(claim["replacement_exclusion_proved"] is False, "replacement overclaim")
    require(claim["semantic_owner_proved"] is False, "owner overclaim")
    require(claim["finite_ledger_delta"] == 0, "finite payment overclaim")
    require(claim["asymptotic_ledger_delta"] == 0, "asymptotic payment overclaim")
    require(claim["grand_mca"] is False, "Grand MCA overclaim")
    require(claim["grand_list"] is False, "Grand List overclaim")
    require(claim["recurrence"] is False, "recurrence overclaim")
    require(claim["official_score"] == "0/2", "official score overclaim")


def check_manifest() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    require(
        manifest["base"] == "9908454995f3f195cfe748f35a1135211609d066",
        "manifest base drift",
    )
    require(
        manifest["status"] == "independently-audited-zero-payment-obstruction",
        "manifest status drift",
    )
    for relative, expected in manifest["files"].items():
        path = ROOT / relative
        require(path.is_file(), f"missing manifest file: {relative}")
        require(digest(path) == expected, f"manifest hash drift: {relative}")
    require("no official-score movement" in manifest["nonclaims"], "score nonclaim removed")
    return len(manifest["files"])


def cube_gates(
    s: int,
    *,
    r: int = 3,
    n_delta: int = -1,
    redundancy: int = 8,
    k_delta: int = 0,
    a_delta: int = 0,
    target_shift: int = 128,
    profile: int = 1,
    numerator_delta: int = 0,
    challenge_is_full: bool = True,
    safe_on_equal: bool = True,
    characteristic: int = 2,
) -> tuple[list[bool], dict[str, int]]:
    q = 1 << (2 * s)
    n = q + n_delta
    k = n - redundancy + k_delta
    a = n - r + a_delta
    numerator = (q - 1) // 3 + numerator_delta
    target = 1 << (2 * s - target_shift) if 2 * s >= target_shift else 0
    tangent = min(q, r + 1)
    upper = min(q, max(r + 1, n // r)) if r else 0
    gates = [
        s >= 65,
        characteristic == 2,
        r == 3,
        q % 3 == 1,
        n == q - 1,
        redundancy == 3 * r - 1,
        k == n - redundancy,
        a == n - r,
        1 <= k < n,
        k + 1 <= a <= n,
        challenge_is_full,
        safe_on_equal,
        target_shift == 128,
        numerator == (q - 1) // r,
        upper == numerator,
        numerator > target,
        profile == 1,
        2 * a - n - k == 2,
        max(profile, tangent) <= target,
        tangent <= numerator <= upper,
    ]
    return gates, {
        "s": s,
        "q": q,
        "n": n,
        "R": redundancy,
        "r": r,
        "k": k,
        "a": a,
        "numerator": numerator,
        "target": target,
        "profile": profile,
        "tangent": tangent,
        "upper": upper,
    }


def square_gates(
    s: int, *, target_shift: int = 128, numerator_delta: int = 0
) -> tuple[list[bool], dict[str, int]]:
    q = 1 << (2 * s)
    r = 1 << s
    n = q - 1
    redundancy = 3 * r - 1
    k = n - redundancy
    a = n - r
    numerator = r + 1 + numerator_delta
    target = 1 << (2 * s - target_shift)
    tangent = r + 1
    upper = max(r + 1, n // r)
    gates = [
        s >= 129,
        target_shift == 128,
        redundancy == 3 * r - 1,
        k == n - redundancy,
        a == n - r,
        n // r == r - 1,
        tangent == upper == numerator,
        numerator <= target,
        target > numerator,
    ]
    return gates, {
        "s": s,
        "q": q,
        "n": n,
        "R": redundancy,
        "r": r,
        "k": k,
        "a": a,
        "numerator": numerator,
        "target": target,
        "tangent": tangent,
        "upper": upper,
    }


def check_rows() -> tuple[list[tuple[str, dict[str, int]]], int]:
    rows: list[tuple[str, dict[str, int]]] = []
    checks: list[bool] = []
    for s in (65, 66, 129):
        gates, row = cube_gates(s)
        checks.extend(gates)
        rows.append(("CUBE", row))
    for s in (129, 130):
        gates, row = square_gates(s)
        checks.extend(gates)
        rows.append(("SQUARE", row))
    require(all(checks), "row replay failed")
    return rows, len(checks)


def mutation_results() -> list[tuple[str, bool]]:
    cube_mutations = [
        ("s below endpoint", {"s": 64}),
        ("domain includes zero", {"s": 65, "n_delta": 0}),
        ("wrong last-predeep redundancy", {"s": 65, "redundancy": 9}),
        ("wrong fiber size", {"s": 65, "r": 2}),
        ("wrong k", {"s": 65, "k_delta": 1}),
        ("wrong agreement", {"s": 65, "a_delta": 1}),
        ("wrong target normalization", {"s": 65, "target_shift": 127}),
        ("profile not singleton", {"s": 65, "profile": 2}),
        ("numerator off by one", {"s": 65, "numerator_delta": 1}),
        ("challenge not full field", {"s": 65, "challenge_is_full": False}),
        ("equality declared unsafe", {"s": 65, "safe_on_equal": False}),
        ("wrong characteristic", {"s": 65, "characteristic": 3}),
    ]
    results: list[tuple[str, bool]] = []
    for name, raw in cube_mutations:
        kwargs = dict(raw)
        s = int(kwargs.pop("s"))
        gates, _ = cube_gates(s, **kwargs)
        results.append((name, not all(gates)))
    square_mutations = [
        ("square endpoint too early", 128, {}),
        ("square numerator off by one", 129, {"numerator_delta": 1}),
        ("square target normalization wrong", 129, {"target_shift": 127}),
    ]
    for name, s, kwargs in square_mutations:
        gates, _ = square_gates(s, **kwargs)
        results.append((name, not all(gates)))
    return results


def run_check() -> int:
    source_files, source_anchors = check_source_pins()
    claim = json.loads(CLAIM_PATH.read_text(encoding="utf-8"))
    check_claim(claim)
    manifest_files = check_manifest()
    rows, checks = check_rows()
    mutations = mutation_results()
    require(all(passed for _, passed in mutations), "semantic mutation survived")

    print("LAST_PREDEEP_CUBE_FIBER_PROFILE_OBSTRUCTION: PASS")
    print(f"source_pins=PASS,files={source_files},anchors={source_anchors}")
    print(f"artifact_manifest=PASS,files={manifest_files}")
    print("claim_guard=PASS,status=independently-audited-zero-payment-obstruction")
    for kind, row in rows:
        print(
            "%s s=%d R=%d r=%d numerator=%d target=%d tangent=%d upper=%d"
            % (
                kind,
                row["s"],
                row["R"],
                row["r"],
                row["numerator"],
                row["target"],
                row["tangent"],
                row["upper"],
            )
        )
    print("cube_symbolic=(q-1)/3>2^(2s-128),all_s>=65")
    print("square_cut=s>=129,E=U=2^s+1<2^(2s-128)")
    print("one_sided_cut=B_star>=U_sufficient;exact_only_when_E_equals_U")
    print(f"rows={len(rows)},checks={checks}")
    print(f"mutations={len(mutations)}/{len(mutations)}")
    print("finite_ledger_delta=0 asymptotic_ledger_delta=0 official_score=0/2")
    print("result=PASS")
    return 0


def run_tamper_selftest() -> int:
    results = mutation_results()
    for name, passed in results:
        print(("ok  " if passed else "FAIL") + "mutation: " + name)
    passed = sum(ok for _, ok in results)
    print("RESULT: %s %d/%d" % ("PASS" if passed == len(results) else "FAIL", passed, len(results)))
    return 0 if passed == len(results) else 1


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    if mode == "--check":
        return run_check()
    if mode == "--tamper-selftest":
        return run_tamper_selftest()
    print(
        "usage: verify_last_predeep_cube_fiber_profile_obstruction.py "
        "[--check | --tamper-selftest]"
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
