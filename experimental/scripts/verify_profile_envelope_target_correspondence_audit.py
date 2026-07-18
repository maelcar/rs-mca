#!/usr/bin/env python3
"""Independent correspondence audit for the integrated PR #759 packet.

This stdlib-only verifier checks the repaired selected-power-profile packet
against its immutable integration objects, its bound sources, and independently
recomputed finite-field censuses.  It deliberately does not import the producer.

STATUS: COUNTEREXAMPLE.  The status applies to the original universal exact
prime/no-drop, complete-envelope, asymptotic-FI, and unsafe-target claims.  It
does not invalidate the packet's surviving finite selected-slice arithmetic.

Usage:
  python3 experimental/scripts/verify_profile_envelope_target_correspondence_audit.py
  python3 experimental/scripts/verify_profile_envelope_target_correspondence_audit.py --tamper-selftest
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations
from math import ceil, comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PRODUCER = Path("experimental/scripts/verify_profile_envelope_target_comparison.py")
NOTE = Path("experimental/notes/thresholds/profile_envelope_target_comparison.md")
CERT = Path("experimental/data/certificates/profile-envelope-target-comparison/cert.json")
LEAN = Path(
    "experimental/lean/profile_envelope_target_comparison/"
    "ProfileEnvelopeTargetComparison.lean"
)
COMPLETENESS = Path("experimental/notes/thresholds/profile_envelope_completeness.md")
FRONTIERS = Path("experimental/asymptotic_rs_mca_frontiers.tex")
CONSUMER_NOTE = Path(
    "experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md"
)
CONSUMER_SCRIPT = Path(
    "experimental/scripts/verify_nonfiber_decomposition_realized_scale.py"
)
CONSUMER_LEAN = Path(
    "experimental/lean/nonfiber_decomposition_realized_scale/"
    "NonfiberDecompositionRealizedScale.lean"
)

ORIGINAL_HEAD = "8cd4f4b6"
INTEGRATION = "2633895a"
ORIGINAL_BLOBS = {
    NOTE: "436f5c95fa826b6fd6f9da487c2b75701bb4bc98",
    PRODUCER: "81ac80d00e04269652f5a21ffb26d6f0d6c46c25",
    CERT: "f1734d432786ceaf4500dfd278faa666b1d68468",
    LEAN: "4cb722783bad1b9cc4459efb10a2ed260b74cd16",
}
EXPECTED_BINDINGS = {
    str(NOTE),
    str(PRODUCER),
    str(LEAN),
    str(COMPLETENESS),
    "experimental/notes/thresholds/envelope_identity_window.md",
    str(FRONTIERS),
}


class Checker:
    def __init__(self) -> None:
        self.total = 0
        self.failures: list[str] = []

    def gate(self, label: str, condition: bool, detail: str = "") -> None:
        self.total += 1
        ok = bool(condition)
        if not ok:
            self.failures.append(f"{label}: {detail or 'condition false'}")
        suffix = f" -- {detail}" if detail else ""
        print(f"  [{'ok' if ok else 'XX'}] {label}{suffix}")


def read(path: Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def canonical_payload(data: dict) -> str:
    unsigned = copy.deepcopy(data)
    unsigned.pop("payload_sha256", None)
    raw = json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def git_blob(revision: str, path: Path) -> str:
    proc = run(["git", "rev-parse", f"{revision}:{path}"])
    return proc.stdout.strip() if proc.returncode == 0 else ""


def git_show(revision: str, path: Path) -> str:
    proc = run(["git", "show", f"{revision}:{path}"])
    return proc.stdout if proc.returncode == 0 else ""


# ---------------------------------------------------------------- finite fields

class Field:
    """GF(p) or GF(p^2)=GF(p)[t]/(t^2-nu), with exact hashable elements."""

    def __init__(self, p: int, degree: int = 1) -> None:
        self.p = p
        self.degree = degree
        if degree == 1:
            self.q = p
            self.zero = 0
            self.one = 1
            self.elems = list(range(p))
            self.nu = None
        elif degree == 2:
            self.q = p * p
            self.zero = (0, 0)
            self.one = (1, 0)
            self.elems = [(a, b) for a in range(p) for b in range(p)]
            self.nu = next(
                a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1
            )
        else:
            raise ValueError("only degrees 1 and 2 are used")

    def sub(self, x, y):
        if self.degree == 1:
            return (x - y) % self.p
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def mul(self, x, y):
        if self.degree == 1:
            return (x * y) % self.p
        a, b = x
        c, d = y
        return (
            (a * c + b * d * self.nu) % self.p,
            (a * d + b * c) % self.p,
        )

    def power(self, x, exponent: int):
        result = self.one
        base = x
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result


def prime_factors(n: int) -> set[int]:
    out: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def generator(field: Field):
    order = field.q - 1
    factors = prime_factors(order)
    for value in field.elems:
        if value != field.zero and all(
            field.power(value, order // factor) != field.one for factor in factors
        ):
            return value
    raise RuntimeError("no multiplicative generator")


def prime_domain(p: int) -> tuple[Field, list]:
    field = Field(p)
    return field, list(range(1, p))


def tower_domain(p: int) -> tuple[Field, list]:
    field = Field(p, 2)
    gen = generator(field)
    n = 2 * (p - 1)
    step = (field.q - 1) // n
    subgroup = [field.power(gen, step * i) for i in range(n)]
    domain = [field.mul(gen, h) for h in subgroup]
    if len(set(domain)) != n:
        raise RuntimeError("tower domain is not distinct")
    return field, domain


def prefix(field: Field, support, width: int):
    coeffs = [field.one] + [field.zero] * width
    for x in support:
        for i in range(width, 0, -1):
            coeffs[i] = field.sub(coeffs[i], field.mul(x, coeffs[i - 1]))
    return tuple(coeffs[1:])


def census(field: Field, supports, width: int) -> tuple[int, int, int]:
    buckets: dict[tuple, int] = defaultdict(int)
    size = 0
    for support in supports:
        size += 1
        buckets[prefix(field, support, width)] += 1
    return size, len(buckets), max(buckets.values(), default=0)


def identity_census(field: Field, domain: list, a: int, width: int):
    return census(field, combinations(domain, a), width)


def power_supports(field: Field, domain: list, a: int, c: int, r: int):
    buckets: dict[object, list] = {}
    for x in domain:
        buckets.setdefault(field.power(x, c), []).append(x)
    fibers = list(buckets.values())
    if any(len(fiber) != c for fiber in fibers):
        return
    m = (a - r) // c
    for chosen_tuple in combinations(range(len(fibers)), m):
        chosen = set(chosen_tuple)
        base = [x for i in chosen_tuple for x in fibers[i]]
        if r == 0:
            yield tuple(base)
            continue
        remainder_pool = [
            x for i, fiber in enumerate(fibers) if i not in chosen for x in fiber
        ]
        for remainder in combinations(remainder_pool, r):
            yield tuple(base) + remainder


def power_census(
    field: Field, domain: list, a: int, width: int, c: int, r: int
) -> tuple[int, int, int]:
    return census(field, power_supports(field, domain, a, c, r), width)


def selected_inventory(
    field: Field, domain: list, a: int, width: int, cells: list[tuple[int, int]]
) -> dict[tuple[int, int], tuple[int, int, int]]:
    return {
        cell: power_census(field, domain, a, width, cell[0], cell[1])
        for cell in cells
    }


# ---------------------------------------------------------- certificate checks

def sources_fresh(cert: dict) -> bool:
    bindings = cert.get("source_bindings")
    if not isinstance(bindings, list):
        return False
    paths = [row.get("path") for row in bindings if isinstance(row, dict)]
    if len(paths) != len(set(paths)) or set(paths) != EXPECTED_BINDINGS:
        return False
    return all(
        isinstance(row, dict)
        and isinstance(row.get("sha256"), str)
        and re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None
        and (ROOT / row["path"]).is_file()
        and sha256(Path(row["path"])) == row["sha256"]
        for row in bindings
    )


def cert_semantics(cert: dict) -> bool:
    rows = cert.get("rows", {})
    scope = cert.get("scope", {})
    target = cert.get("target_direction", {})
    return (
        cert.get("schema") == "rs-mca-profile-envelope-target-comparison-v2"
        and cert.get("artifact") == "profile-envelope-target-comparison"
        and cert.get("status") == "COUNTEREXAMPLE"
        and cert.get("producer_head") == ORIGINAL_HEAD
        and cert.get("integration") == INTEGRATION
        and cert.get("verifier") == str(PRODUCER)
        and cert.get("verifier_result") == "PASS (89/89)"
        and scope.get("enumerated")
        == "identity and complete-power-fiber quotient/remainder slices"
        and scope.get("complete_profile_inventory") is False
        and scope.get("universal_prime_theorem") is False
        and scope.get("unsafe_theorem") is False
        and scope.get("asymptotic_FI_decided") is False
        and rows.get("prime_GF13_n12", {}).get("c3r0")
        == {
            "size": 6,
            "L": 1,
            "barN": "6",
            "identity_dominated": False,
            "deep_dominated": True,
        }
        and rows.get("prime_GF19_n18", {})
        == {
            "identity": {"size": 43758, "L": 6859},
            "square": {"size": 126, "L": 19},
            "square_beats_identity": True,
        }
        and rows.get("generic_20subset_GF121", {})
        == {
            "size": 184756,
            "L_id": 9359,
            "max_fiber": 57,
            "ambient": 14641,
            "full_codomain": False,
        }
        and rows.get("tower_GF121_n20", {}).get("power_cells")
        == [
            {"c": 2, "r": 0, "size": 252, "L": 11, "barN": "252/11"},
            {"c": 4, "r": 2, "size": 660, "L": 190, "barN": "66/19"},
            {"c": 5, "r": 0, "size": 6, "L": 1, "barN": "6"},
            {"c": 10, "r": 0, "size": 2, "L": 1, "barN": "2"},
        ]
        and target
        == {
            "B_star": 26,
            "formal_identity_proxy": 26,
            "formal_identity_plus_square_proxy": 50,
            "formal_identity_plus_all_selected_power_cells": 65,
            "realized_identity_selected_budget": 152,
            "realized_identity_plus_square_selected_budget": 176,
            "realized_identity_plus_all_selected_power_cells": 191,
            "conclusion": "selected realized safe test fails; no unsafe theorem",
        }
    )


def cert_valid(cert: dict) -> bool:
    return (
        cert.get("payload_sha256") == canonical_payload(cert)
        and sources_fresh(cert)
        and cert_semantics(cert)
    )


def no_stale_open_claim(text: str) -> bool:
    lowered = text.lower()
    bad = re.search(
        r"#759.{0,180}(?:conditional[- ]on[- ]open|\bopen\b)",
        lowered,
        flags=re.DOTALL,
    )
    return "#759" in lowered and "integrated" in lowered and bad is None


def normal_audit() -> int:
    checker = Checker()
    print("PROFILE-ENVELOPE TARGET CORRESPONDENCE AUDIT")

    # Immutable producer-head / integration provenance.
    blobs_match = all(
        git_blob(ORIGINAL_HEAD, path) == blob
        and git_blob(INTEGRATION, path) == blob
        for path, blob in ORIGINAL_BLOBS.items()
    )
    checker.gate(
        "A1 immutable #759 head/integration blobs",
        blobs_match,
        "four artifacts identical at 8cd4f4b6 and 2633895a",
    )
    old_note = git_show(INTEGRATION, NOTE)
    old_script = git_show(INTEGRATION, PRODUCER)
    old_cert_text = git_show(INTEGRATION, CERT)
    old_overclaim = (
        "identity-dominant **iff**" in old_note
        and "Prime base fields force" in old_note
        and "identity->SAFE, complete->UNSAFE" in old_script
        and '"verdict": "identity dominates all scales"' in old_cert_text
        and '"complete_says": "unsafe"' in old_cert_text
    )
    checker.gate(
        "A2 original universal/unsafe overclaims reproduced",
        old_overclaim,
        "checked from immutable integration text",
    )

    cert = json.loads(read(CERT))
    checker.gate(
        "B1 canonical certificate payload and six SHA-256 bindings",
        cert.get("payload_sha256") == canonical_payload(cert) and sources_fresh(cert),
    )
    checker.gate(
        "B2 repaired certificate semantics",
        cert_semantics(cert),
        "selected inventory; no universal/FI/unsafe theorem",
    )

    note = read(NOTE)
    note_flat = " ".join(note.split())
    note_scope = all(
        marker in note_flat
        for marker in (
            "**STATUS:** `COUNTEREXAMPLE`",
            "not a complete census",
            "failure of the sufficient safe test does not prove an unsafe row",
            "A one-row factor-`p` deficit proves exact non-surjectivity, not failure",
            "received-line/first-match co-realization",
        )
    )
    checker.gate("C1 repaired note states exact scope and one-way target", note_scope)

    producer_text = read(PRODUCER)
    producer_tree = ast.parse(producer_text)
    reserve_calls = [
        node
        for node in ast.walk(producer_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "P_reserve"
    ]
    script_scope = (
        "does not enumerate the Chebyshev" in producer_text
        and "proves no universal" in producer_text
        and "full generic census" in producer_text
        and "samples the first 60000 supports" not in producer_text
        and not reserve_calls
    )
    checker.gate(
        "C2 repaired producer literal scope",
        script_scope,
        "full generic census; P_reserve never invoked",
    )

    lean = read(LEAN)
    lean_flat = " ".join(lean.split())
    proof_escape = re.search(
        r"\bby\s+(?:sorry|admit)\b|^\s*axiom\s", lean, flags=re.MULTILINE
    )
    lean_scope = (
        "tower121_identity_full_codomain_deficit" in lean
        and "prime41_identity_full_codomain_exact" in lean
        and "tower121_identity_FI_fails" not in lean
        and "does not construct finite fields" in lean_flat
        and proof_escape is None
    )
    checker.gate(
        "C3 Lean is a fixed-arithmetic shadow",
        lean_scope,
        "semantic names repaired; no sorry/admit/custom axiom",
    )

    consumer_scope = all(
        no_stale_open_claim(read(path))
        for path in (CONSUMER_NOTE, CONSUMER_SCRIPT, CONSUMER_LEAN)
    )
    checker.gate(
        "C4 #760 consumer status/scope repaired",
        consumer_scope,
        "#759 integrated, not conditional-on-open",
    )

    frontiers = read(FRONTIERS)
    completeness = read(COMPLETENESS)
    source_interface = (
        r"\label{eq:profile-envelope}" in frontiers
        and r"\Lambda(r_0,r_1;a)" in frontiers
        and "first-match cells are nonempty" in frontiers
        and "(PEU) Primitive-residual envelope upper" in completeness
        and "`(PEU)` is" in completeness
        and "`OPEN`" in completeness
    )
    checker.gate(
        "C5 source envelope retains first-match/PEU ownership",
        source_interface,
        "raw power slices are not the source Lambda sum",
    )

    # Independent exact censuses; no producer import or certificate arithmetic.
    f13, d13 = prime_domain(13)
    gf13_id = identity_census(f13, d13, 6, 2)
    gf13 = selected_inventory(f13, d13, 6, 2, [(2, 0), (3, 0), (4, 2), (6, 0)])
    checker.gate(
        "D1 GF13 c=3 counterexample",
        gf13_id[:2] == (924, 169)
        and {cell: row[:2] for cell, row in gf13.items()} == {
            (2, 0): (20, 13),
            (3, 0): (6, 1),
            (4, 2): (84, 66),
            (6, 0): (2, 1),
        }
        and 6 * 169 > 924,
        "c3 barN=6 > 924/169, despite square domination",
    )

    f19, d19 = prime_domain(19)
    gf19_id = identity_census(f19, d19, 8, 3)
    gf19_sq = power_census(f19, d19, 8, 3, 2, 0)
    checker.gate(
        "D2 GF19 exact no-drop counterexample",
        gf19_id[:2] == (43758, 6859)
        and gf19_sq[:2] == (126, 19)
        and gf19_id[1] == 19**3
        and 126 * 6859 > 43758 * 19,
    )

    family_primes = (11, 13, 17, 19, 23, 29, 31, 37, 41)
    family_ok = all(
        Q(p - 1, 2) > Q((p - 1) * (p - 2), 2 * p)
        and Q(p - 1, 2) > 3
        for p in family_primes
    )
    checker.gate(
        "D3 w=1 prime family",
        family_ok,
        "square exceeds identity and deep=3 for p=11..41",
    )

    f49, d49 = tower_domain(7)
    gf49_id = identity_census(f49, d49, 6, 2)
    gf49 = selected_inventory(f49, d49, 6, 2, [(2, 0), (3, 0), (4, 2), (6, 0)])
    gf49_bars = {cell: Q(row[0], row[1]) for cell, row in gf49.items()}
    checker.gate(
        "D4 GF49 selected boundary",
        gf49_id[:2] == (924, 319)
        and {cell: row[:2] for cell, row in gf49.items()} == {
            (2, 0): (20, 7),
            (3, 0): (6, 1),
            (4, 2): (84, 66),
            (6, 0): (2, 1),
        }
        and Q(924, 319) > Q(20, 7)
        and max(gf49_bars, key=gf49_bars.get) == (3, 0),
        "realized identity wins; c3 is selected leader",
    )

    f121, d121 = tower_domain(11)
    gf121_id = identity_census(f121, d121, 10, 2)
    gf121 = selected_inventory(
        f121, d121, 10, 2, [(2, 0), (4, 2), (5, 0), (10, 0)]
    )
    checker.gate(
        "D5 GF121 smooth-coset selected rows",
        gf121_id[:2] == (184756, 1331)
        and {cell: row[:2] for cell, row in gf121.items()} == {
            (2, 0): (252, 11),
            (4, 2): (660, 190),
            (5, 0): (6, 1),
            (10, 0): (2, 1),
        }
        and Q(184756, 1331) > Q(252, 11) > Q(184756, 14641),
    )

    generic_domain = [x for x in f121.elems if x != f121.zero][:20]
    generic = identity_census(f121, generic_domain, 10, 2)
    checker.gate(
        "D6 full generic GF121 census",
        generic == (184756, 9359, 57),
        "all C(20,10) supports, not a 60000-prefix sample",
    )

    formal_identity = Q(comb(20, 10), 121**2)
    realized_identity = Q(comb(20, 10), 1331)
    selected_bars = [Q(252, 11), Q(660, 190), Q(6), Q(2)]
    deep = 11
    formal_id = 1 + deep + 1 + ceil(formal_identity)
    formal_square = formal_id + 1 + ceil(selected_bars[0])
    formal_all = formal_id + sum(1 + ceil(value) for value in selected_bars)
    realized_id = 1 + deep + 1 + ceil(realized_identity)
    realized_square = realized_id + 1 + ceil(selected_bars[0])
    realized_all = realized_id + sum(1 + ceil(value) for value in selected_bars)
    target_ok = (
        (formal_id, formal_square, formal_all) == (26, 50, 65)
        and (realized_id, realized_square, realized_all) == (152, 176, 191)
        and "`E<=B*` implies safe" in note
        and "does not imply unsafe" in note
    )
    checker.gate(
        "E1 target implication is one-way",
        target_ok,
        "26/50/65 formal; 152/176/191 realized; no unsafe inference",
    )

    normal = run([sys.executable, str(PRODUCER)])
    checker.gate(
        "F1 producer normal replay",
        normal.returncode == 0 and "RESULT: PASS (89/89)" in normal.stdout,
    )
    optimized = run([sys.executable, "-O", str(PRODUCER)])
    checker.gate(
        "F2 producer optimized replay",
        optimized.returncode == 0 and "RESULT: PASS (89/89)" in optimized.stdout,
    )
    tamper = run([sys.executable, str(PRODUCER), "--tamper-selftest"])
    checker.gate(
        "F3 producer normal tamper replay",
        tamper.returncode == 0 and "tamper_mutations_rejected=3/3" in tamper.stdout,
    )
    tamper_o = run([sys.executable, "-O", str(PRODUCER), "--tamper-selftest"])
    checker.gate(
        "F4 producer optimized tamper replay",
        tamper_o.returncode == 0
        and "tamper_mutations_rejected=3/3" in tamper_o.stdout,
    )
    unknown = run([sys.executable, str(PRODUCER), "--definitely-unknown"])
    checker.gate(
        "F5 producer unknown option fails closed",
        unknown.returncode == 2 and "RESULT: FAIL (unknown arguments:" in unknown.stdout,
    )

    print()
    if checker.failures:
        print(f"RESULT: FAIL ({len(checker.failures)} of {checker.total})")
        for failure in checker.failures:
            print(f"  - {failure}")
        print("STATUS: COUNTEREXAMPLE")
        return 1
    print(f"RESULT: PASS ({checker.total}/{checker.total})")
    print("STATUS: COUNTEREXAMPLE")
    return 0


def tamper_selftest() -> int:
    cert = json.loads(read(CERT))
    if not cert_valid(cert):
        print("RESULT: FAIL (clean certificate precondition)")
        print("STATUS: COUNTEREXAMPLE")
        return 1

    rejected = 0
    bad_row = copy.deepcopy(cert)
    bad_row["rows"]["prime_GF19_n18"]["square"]["L"] = 20
    bad_row["payload_sha256"] = canonical_payload(bad_row)
    rejected += int(not cert_valid(bad_row))

    bad_scope = copy.deepcopy(cert)
    bad_scope["scope"]["universal_prime_theorem"] = True
    bad_scope["payload_sha256"] = canonical_payload(bad_scope)
    rejected += int(not cert_valid(bad_scope))

    bad_source = copy.deepcopy(cert)
    bad_source["source_bindings"][0]["sha256"] = "0" * 64
    bad_source["payload_sha256"] = canonical_payload(bad_source)
    rejected += int(not cert_valid(bad_source))

    if rejected == 3:
        print("RESULT: PASS (tamper-selftest)")
        print("tamper_mutations_rejected=3/3")
        print("STATUS: COUNTEREXAMPLE")
        return 0
    print(f"RESULT: FAIL (tamper mutations rejected {rejected}/3)")
    print("STATUS: COUNTEREXAMPLE")
    return 1


def main(argv: list[str]) -> int:
    if argv == ["--tamper-selftest"]:
        return tamper_selftest()
    if argv:
        print(f"RESULT: FAIL (unknown arguments: {' '.join(argv)})")
        print("STATUS: COUNTEREXAMPLE")
        return 2
    return normal_audit()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
