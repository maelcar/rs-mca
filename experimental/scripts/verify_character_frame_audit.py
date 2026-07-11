#!/usr/bin/env python3
"""Recompute every number reported in
experimental/notes/audits/character_frame_hypothesis_audit.md.

Stdlib only.  Recomputes: (a) the three load-bearing frame identities on
explicit small toys (CF1 frame bound, CF3 converse, full-dual identity),
(b) the block-parabola Gauss/identity facts (C_p, K_{A_k}=I), (c) the
rerun headline numbers of the audited verifier
verify_asymptotic_primitive_profile_character_frame_v1.py, (d) the
adversarial falsifier census (false-floor search), and (e) the claim-table
verdict counts and comparison-table checksum.

Prints PASS/FAIL per check and a final summary line.  Exits 0 iff all
checks pass.  Run under `ulimit -v 2097152`.
"""
from __future__ import annotations

import cmath
import itertools
import math
import random
import sys
import zlib
from collections import Counter
from pathlib import Path
from typing import Any

TOL = 1.0e-7            # numeric tolerance for power-iteration operator norms
EXACT_TOL = 2.0e-9     # matches the audited verifier's TOL for exact rows

# ------------------------------------------------------------------ #
# Values reported in the audit note.  A check enforces equality only  #
# when the expected value is not None (first discovery run leaves     #
# them None and merely prints the computed numbers).                  #
# ------------------------------------------------------------------ #
EXPECT: dict[str, Any] = {
    # rerun of the audited verifier (their summary)
    "their_case_count": 5,
    "their_strict_packed_improvements": 3,
    "their_nonuniform_source_cases": 3,
    "their_menu_rows": 5,
    "their_menu_nonuniform_rows": 4,
    "their_p5_rate": 0.459399339592,
    "their_p5_packed_multiplier": 1.0,
    "their_payload_sha256": "62aa09b75ef64eadf955ac2e745cbd2646bad8756bf78f616808e4150c3ecbcd",
    # falsifier census
    "falsifier_configs": 20,
    "falsifier_pairs": 329,
    "falsifier_false_floors": 0,
    "gershgorin_violations": 0,
    "cf1_opnorm_violations": 0,
    "cf3_violations": 0,
    # claim ledger
    "audited_items": 15,
    "verdict_no_issue": 12,
    "verdict_open": 1,
    "verdict_open_gap": 2,
    "verdict_counterexample": 0,
    "verdict_fixed": 0,
    # comparison table checksum (crc32 of the canonical 3-way string)
    "comparison_crc32": 2397961939,
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


# ============================ group algebra ============================ #
def sub(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((x - y) % p for x, y in zip(a, b))


def dot(a: tuple[int, ...], b: tuple[int, ...], p: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % p


def chi(a: tuple[int, ...], z: tuple[int, ...], p: int) -> complex:
    return cmath.exp(2j * math.pi * dot(a, z, p) / p)


def dual(p: int, rank: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(p), repeat=rank))


def fourier(p: int, rank: int, counts: "Counter[tuple[int, ...]]"):
    d = dual(p, rank)
    total = sum(counts.values())
    val = {
        g: sum(m * chi(g, im, p) for im, m in counts.items()) / total
        for g in d
    }
    return d, val


def gram(A: list[tuple[int, ...]], val, p: int) -> list[list[complex]]:
    return [[val[sub(b, a, p)] for b in A] for a in A]


def row_sum_bound(A: list[tuple[int, ...]], val, p: int) -> float:
    return max(sum(abs(val[sub(b, a, p)]) for b in A) for a in A)


def op_norm_herm(M: list[list[complex]]) -> float:
    """Top eigenvalue of a Hermitian PSD matrix via power iteration."""
    n = len(M)
    if n == 0:
        return 0.0
    if n == 1:
        return abs(M[0][0])
    rng = random.Random(982451653)
    best = 0.0
    for _ in range(6):
        v = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(n)]
        for _ in range(400):
            w = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
            nrm = math.sqrt(sum(abs(x) ** 2 for x in w))
            if nrm < 1e-290:
                break
            v = [x / nrm for x in w]
        Mv = [sum(M[i][j] * v[j] for j in range(n)) for i in range(n)]
        num = sum((v[i].conjugate() * Mv[i]).real for i in range(n))
        den = sum(abs(x) ** 2 for x in v)
        if den > 0:
            best = max(best, num / den)
    return best


def actual_multiplier(counts: "Counter[tuple[int, ...]]") -> float:
    total = sum(counts.values())
    return len(counts) * max(counts.values()) / total


# ============================ toy builders ============================ #
def power_sum_counts(p, support, weight, depth):
    counts: Counter = Counter()
    for chosen in itertools.combinations(support, weight):
        image = tuple(sum(pow(t, k, p) for t in chosen) % p for k in range(1, depth + 1))
        counts[image] += 1
    return counts


def block_parabola_counts(p, blocks):
    counts: Counter = Counter()
    for choices in itertools.product(range(p), repeat=blocks):
        image = tuple(c for t in choices for c in (t, (t * t) % p))
        counts[image] += 1
    return counts


def linear_block_characters(p, blocks):
    return [tuple(c for a in vals for c in (a, 0)) for vals in itertools.product(range(p), repeat=blocks)]


# ============================ individual checks ============================ #
def check_cf1_frame() -> tuple[str, bool, str]:
    """CF1: max_z |F_z| <= M ||K_A||/|A|, using both the Gram row-sum
    upper bound and the true operator norm, on explicit source toys."""
    ok = True
    detail = []
    toys = [
        (5, list(range(5)), 2, 2),
        (7, list(range(7)), 4, 2),
        (11, list(range(7)), 3, 2),
    ]
    for p, support, weight, depth in toys:
        counts = power_sum_counts(p, support, weight, depth)
        d, val = fourier(p, depth, counts)
        M = sum(counts.values())
        max_fiber = max(counts.values())
        # take A = the full dual (a valid nonempty subset)
        rb = row_sum_bound(d, val, p)
        opn = op_norm_herm(gram(d, val, p))
        rhs_row = M * rb / len(d)
        rhs_op = M * opn / len(d)
        good = max_fiber <= rhs_row + EXACT_TOL and max_fiber <= rhs_op + TOL
        ok = ok and good
        detail.append(f"F{p} m{weight}: maxfiber={max_fiber} <= Mrb/|A|={rhs_row:.4f}, Mop/|A|={rhs_op:.4f} {good}")
    return ("CF1 frame inequality (row-sum & operator-norm)", ok, "; ".join(detail))


def check_cf3_converse() -> tuple[str, bool, str]:
    """CF3: ||K_A|| >= |A| mu(z) for every z; and the packed multiplier
    kappa_frame >= actual multiplier."""
    ok = True
    detail = []
    toys = [(5, list(range(5)), 2, 2), (7, list(range(7)), 4, 2)]
    for p, support, weight, depth in toys:
        counts = power_sum_counts(p, support, weight, depth)
        d, val = fourier(p, depth, counts)
        total = sum(counts.values())
        opn = op_norm_herm(gram(d, val, p))
        worst = min(opn - len(d) * (m / total) for m in counts.values())
        good = worst >= -TOL
        ok = ok and good
        detail.append(f"F{p}: min(||K||-|A|mu)={worst:.6f} {good}")
    return ("CF3 converse Rayleigh lower bound", ok, "; ".join(detail))


def check_full_dual_identity() -> tuple[str, bool, str]:
    """||K_{G^}||_op = |G| max_z mu(z)."""
    ok = True
    detail = []
    toys = [(5, list(range(5)), 2, 2), (7, list(range(6)), 3, 2), (3, None, None, None)]
    cases = []
    for p, support, weight, depth in toys:
        if support is None:
            counts = block_parabola_counts(3, 2)
            rank = 4
        else:
            counts = power_sum_counts(p, support, weight, depth)
            rank = depth
        cases.append((p, rank, counts))
    for p, rank, counts in cases:
        d, val = fourier(p, rank, counts)
        total = sum(counts.values())
        lhs = op_norm_herm(gram(d, val, p))
        rhs = len(d) * max(counts.values()) / total
        rel = abs(lhs - rhs) / rhs
        good = rel <= 1e-5
        ok = ok and good
        detail.append(f"p{p}r{rank}: ||K_full||={lhs:.6f} vs |G|maxmu={rhs:.6f} rel={rel:.2e} {good}")
    return ("Full-dual operator identity", ok, "; ".join(detail))


def check_gauss_Cp() -> tuple[str, bool, str]:
    """One-block (t,t^2) absolute Fourier mass = 1 + (p-1) sqrt(p)."""
    ok = True
    detail = []
    for p in (3, 5, 7):
        counts = block_parabola_counts(p, 1)
        d, val = fourier(p, 2, counts)
        mass = sum(abs(v) for v in val.values())
        expected = 1.0 + (p - 1) * math.sqrt(p)
        good = math.isclose(mass, expected, rel_tol=3e-10, abs_tol=3e-10)
        ok = ok and good
        detail.append(f"p{p}: C_p={mass:.9f} vs {expected:.9f} {good}")
    return ("Gauss-sum base constant C_p", ok, "; ".join(detail))


def check_block_parabola_identity() -> tuple[str, bool, str]:
    """K_{A_k}=I and kappa_frame=1 for the packed linear family."""
    ok = True
    detail = []
    for p, k in [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1)]:
        counts = block_parabola_counts(p, k)
        rank = 2 * k
        d, val = fourier(p, rank, counts)
        A = linear_block_characters(p, k)
        G = gram(A, val, p)
        offdiag = max(abs(G[i][j]) for i in range(len(A)) for j in range(len(A)) if i != j)
        diag = max(abs(G[i][i] - 1.0) for i in range(len(A)))
        rb = row_sum_bound(A, val, p)
        kappa = len(counts) * rb / len(A)
        good = offdiag <= EXACT_TOL and diag <= EXACT_TOL and abs(kappa - 1.0) <= EXACT_TOL
        ok = ok and good
        detail.append(f"p{p}k{k}: offdiag={offdiag:.2e} kappa={kappa:.6f} {good}")
    return ("Block-parabola Gram identity K=I", ok, "; ".join(detail))


def rerun_their_verifier() -> tuple[str, bool, str, dict[str, Any]]:
    """Import the audited verifier and recompute its summary from scratch."""
    scripts = str((repo_root() / "experimental" / "scripts").resolve())
    if scripts not in sys.path:
        sys.path.insert(0, scripts)
    import verify_asymptotic_primitive_profile_character_frame_v1 as V  # type: ignore

    payload = V.build_payload(repo_root())
    errors = V.check_payload(payload)
    s = payload["summary"]
    got = {
        "their_case_count": s["case_count"],
        "their_strict_packed_improvements": s["strict_packed_improvements"],
        "their_nonuniform_source_cases": s["nonuniform_source_cases"],
        "their_menu_rows": s["existing_menu_rows"],
        "their_menu_nonuniform_rows": s["existing_menu_nonuniform_rows"],
        "their_p5_rate": round(s["p5_global_log_loss_per_coordinate"], 12),
        "their_p5_packed_multiplier": s["p5_packed_multiplier"],
        "their_payload_sha256": payload["payload_sha256"],
    }
    # independent recomputation of the p5 rate from the closed form
    indep_rate = math.log(1.0 + 4.0 * math.sqrt(5.0)) / 5.0
    rate_ok = math.isclose(indep_rate, got["their_p5_rate"], rel_tol=1e-9, abs_tol=1e-9)
    ok = (not errors) and rate_ok and s["all_finite_checks_pass"]
    detail = (
        f"errors={errors}; indep p5 rate={indep_rate:.12f}; "
        f"all_finite_checks_pass={s['all_finite_checks_pass']}"
    )
    return ("Rerun audited verifier build_payload/check_payload", ok, detail, got)


# ============================ adversarial falsifier ============================ #
def falsifier_configs():
    """Deterministic adversarial distributions: random + heavy-atom on
    several small effective groups.  Yields (name, p, rank, counts)."""
    rng = random.Random(20260711)
    specs = [
        (5, 1),   # Z_5
        (7, 1),   # Z_7
        (2, 3),   # Z_2^3
        (2, 4),   # Z_2^4
        (3, 2),   # Z_3^2
    ]
    out = []
    for p, rank in specs:
        elems = dual(p, rank)
        # (a) two random full-support distributions
        for r in range(2):
            counts = Counter({e: rng.randint(1, 9) for e in elems})
            out.append((f"rand_p{p}r{rank}_{r}", p, rank, counts))
        # (b) heavy-atom adversary: one dominant atom, rest light
        counts = Counter({e: 1 for e in elems})
        counts[elems[0]] = 4 * len(elems)
        out.append((f"heavy_p{p}r{rank}", p, rank, counts))
        # (c) random partial-support distribution (some empty fibers)
        support = [e for e in elems if rng.random() < 0.6] or elems[:1]
        counts = Counter({e: rng.randint(1, 6) for e in support})
        out.append((f"partial_p{p}r{rank}", p, rank, counts))
    return out


def candidate_families(d, val, p):
    """A deterministic battery of character families A to stress the frame:
    the full dual, every singleton, threshold-greedy packings, and seeded
    random subsets."""
    rng = random.Random(1_000_003)
    zero = (0,) * len(d[0])
    fams: list[list[tuple[int, ...]]] = [list(d)]
    fams.extend([[g] for g in d])
    # threshold-greedy forbidden-difference packings (mirror the note's rule)
    thresholds = sorted({0.0} | {round(abs(val[x]), 12) for x in d if x != zero})
    for thr in thresholds:
        major = {g for g in d if g == zero or abs(val[g]) > thr + 1e-11}
        sel: list[tuple[int, ...]] = []
        for g in d:
            if all(sub(g, q, p) not in major for q in sel):
                sel.append(g)
        if sel:
            fams.append(sel)
    # seeded random subsets
    for _ in range(6):
        k = rng.randint(1, len(d))
        fams.append(rng.sample(d, k))
    # dedupe by frozenset
    seen = set()
    uniq = []
    for f in fams:
        key = frozenset(f)
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def run_falsifier() -> tuple[str, bool, str, dict[str, Any]]:
    configs = falsifier_configs()
    pairs = 0
    false_floors = 0
    min_slack = math.inf
    gersh_samples = 0
    gersh_viol = 0
    cf1_op_samples = 0
    cf1_op_viol = 0
    cf3_tests = 0
    cf3_viol = 0
    fulldual_max_relerr = 0.0
    op_budget = 60  # cap operator-norm computations for runtime

    for name, p, rank, counts in configs:
        d, val = fourier(p, rank, counts)
        total = sum(counts.values())
        act = actual_multiplier(counts)
        fams = candidate_families(d, val, p)
        for A in fams:
            rb = row_sum_bound(A, val, p)
            kappa = len(counts) * rb / len(A)     # frame multiplier (row-sum bound)
            slack = kappa - act
            min_slack = min(min_slack, slack)
            if slack < -EXACT_TOL:
                false_floors += 1
            pairs += 1
        # full-dual identity (operator norm)
        opn_full = op_norm_herm(gram(d, val, p))
        rhs = len(d) * max(counts.values()) / total
        fulldual_max_relerr = max(fulldual_max_relerr, abs(opn_full - rhs) / rhs)
        # sharp operator-norm checks on a bounded sample of packings
        sample = [A for A in fams if 1 < len(A) <= 16][:6]
        for A in sample:
            if op_budget <= 0:
                break
            op_budget -= 1
            opn = op_norm_herm(gram(A, val, p))
            rb = row_sum_bound(A, val, p)
            # Gershgorin: row-sum bound dominates the true operator norm
            gersh_samples += 1
            if rb + TOL < opn:
                gersh_viol += 1
            # CF1 with the true operator norm
            cf1_op_samples += 1
            if len(counts) * opn / len(A) + TOL < act:
                cf1_op_viol += 1
            # CF3 converse at every atom
            for m in counts.values():
                cf3_tests += 1
                if opn + TOL < len(A) * (m / total):
                    cf3_viol += 1

    got = {
        "falsifier_configs": len(configs),
        "falsifier_pairs": pairs,
        "falsifier_false_floors": false_floors,
        "gershgorin_violations": gersh_viol,
        "cf1_opnorm_violations": cf1_op_viol,
        "cf3_violations": cf3_viol,
    }
    ok = (
        false_floors == 0
        and gersh_viol == 0
        and cf1_op_viol == 0
        and cf3_viol == 0
        and min_slack >= -EXACT_TOL
        and fulldual_max_relerr <= 1e-5
    )
    detail = (
        f"configs={len(configs)} pairs={pairs} false_floors={false_floors} "
        f"min_slack={min_slack:.6f} gershgorin={gersh_viol}/{gersh_samples} "
        f"cf1_op={cf1_op_viol}/{cf1_op_samples} cf3={cf3_viol}/{cf3_tests} "
        f"fulldual_max_relerr={fulldual_max_relerr:.2e}"
    )
    return ("Adversarial false-floor falsifier census", ok, detail, got)


# ============================ ledger + comparison ============================ #
def comparison_canonical() -> str:
    """Canonical 3-way comparison string; crc32 is the note's checksum."""
    rows = [
        ("object", "normalization", "mechanism", "target", "vs_CF2"),
        ("avdeev_CF2_packing", "image_M/L", "absolute_operator_norm_packing", "subexponential", "self"),
        ("hughes_LS", "ambient_p^w", "signed_multilevel_large_sieve", "sharp_polynomial", "incomparable"),
        ("legasage_maxfiber_razor", "image_M/L", "additive_combinatorics_near_sidon", "subexponential", "CF2_stronger_implies_it"),
    ]
    return "|".join(",".join(r) for r in rows)


def check_ledger() -> tuple[str, bool, str, dict[str, Any]]:
    verdicts = {
        # 12 note-internal claims
        "C1_cf1": "NO_ISSUE",
        "C2_proof_identities": "NO_ISSUE",
        "C3_cf2_implies_q": "NO_ISSUE",
        "C4_cf3_converse": "NO_ISSUE",
        "C5_full_dual_identity": "NO_ISSUE",
        "C6_cf4_packing_size": "NO_ISSUE",
        "C7_packed_corollary": "NO_ISSUE",
        "C8_kappa_frame_formula": "NO_ISSUE",
        "C9_block_parabola_separation": "NO_ISSUE",
        "C10_residual_monotonicity": "NO_ISSUE",
        "C11_executable_evidence": "NO_ISSUE",
        "C12_cf2_cf5_cf6_packing_input": "OPEN",
        # 3 interface junctions
        "J1_conclusion_shape_match": "NO_ISSUE",
        "J2_large_image_fact": "OPEN_GAP",
        "J3_asymptotic_scale_pinning": "OPEN_GAP",
    }
    counts = Counter(verdicts.values())
    got = {
        "audited_items": len(verdicts),
        "verdict_no_issue": counts["NO_ISSUE"],
        "verdict_open": counts["OPEN"],
        "verdict_open_gap": counts["OPEN_GAP"],
        "verdict_counterexample": counts["COUNTEREXAMPLE_NEW_FLOOR"],
        "verdict_fixed": counts["FIXED"],
        "comparison_crc32": zlib.crc32(comparison_canonical().encode()),
    }
    ok = got["audited_items"] == 15 and got["verdict_counterexample"] == 0
    detail = f"{dict(counts)} crc32={got['comparison_crc32']}"
    return ("Claim ledger counts + comparison checksum", ok, detail, got)


# ============================ driver ============================ #
def enforce(got: dict[str, Any]) -> list[str]:
    """Compare recomputed values against the note's reported EXPECT values."""
    problems = []
    for key, val in got.items():
        if key not in EXPECT:
            continue
        exp = EXPECT[key]
        if exp is None:
            continue
        if isinstance(exp, float):
            if not math.isclose(float(val), exp, rel_tol=1e-9, abs_tol=1e-9):
                problems.append(f"{key}: recomputed {val} != note {exp}")
        elif val != exp:
            problems.append(f"{key}: recomputed {val} != note {exp}")
    return problems


def main() -> int:
    results: list[tuple[str, bool, str]] = []
    collected: dict[str, Any] = {}

    for fn in (
        check_cf1_frame,
        check_cf3_converse,
        check_full_dual_identity,
        check_gauss_Cp,
        check_block_parabola_identity,
    ):
        label, ok, detail = fn()
        results.append((label, ok, detail))

    label, ok, detail, got = rerun_their_verifier()
    collected.update(got)
    results.append((label, ok, detail))

    label, ok, detail, got = run_falsifier()
    collected.update(got)
    results.append((label, ok, detail))

    label, ok, detail, got = check_ledger()
    collected.update(got)
    results.append((label, ok, detail))

    # enforce note-reported values
    mism = enforce(collected)
    results.append(("Note-reported values match recomputation", not mism, "; ".join(mism) if mism else "all match"))

    print("=== character-frame hypothesis audit: recomputation ===")
    all_ok = True
    for label, ok, detail in results:
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")
        print(f"       {detail}")

    print("--- recomputed values (for the note) ---")
    for key in sorted(collected):
        print(f"  {key} = {collected[key]}")

    print(f"SUMMARY: {'ALL PASS' if all_ok else 'FAILURES PRESENT'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
