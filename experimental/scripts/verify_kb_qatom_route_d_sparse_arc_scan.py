#!/usr/bin/env python3
"""Exact bounded calibration of the post-v54 Route-D terminal wall.

Zero arguments recomputes every registered row, compares the result with the
checked-in JSON certificate, validates all exact witnesses, and runs eight
live tamper tests.  ``--generate`` is the maintainer-only certificate writer.

The scan changes the dimension absent from v54's dense toys: the subgroup
index q=(p-1)/n.  Its largest rows have q=1014,1015,1017, close to the exact
KoalaBear index 1016, and t/n=9/16 close to the deployed 1183520/2097152.

Status is AUDIT / EXPERIMENTAL.  Nothing here proves the deployed
|T| <= H2=77291948627 wall at e=67472.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import resource
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "kb-qatom-route-d-sparse-arc-scan"
    / "kb_qatom_route_d_sparse_arc_scan.json"
)

ADDRESS_SPACE_CAP_BYTES = 2 * 1024**3
SUBSET_EVALUATION_CAP = 70_000_000

P_KB = 2**31 - 2**24 + 1
N_KB = 2**21
T_KB = 1_183_520
E_KB = 67_472
H2_KB = 77_291_948_627
INDEX_KB = (P_KB - 1) // N_KB

# Fixed positive and zero controls across the subgroup-index dimension.
INDEX_GRADIENT = [
    (4, 257),
    (18, 1_153),
    (67, 4_289),
    (253, 16_193),
    (513, 32_833),
    (1_017, 65_089),
]

# Every primitive generator step is scanned in each block.
SPARSE_BLOCKS = [
    ("kb_index_pow2_n64_e3", 65_089, 64, 36, 3),
    ("kb_index_pow2_n64_e4", 65_089, 64, 36, 4),
    ("kb_index_shape_n96_e3", 97_441, 96, 54, 3),
    ("kb_index_shape_n128_e4", 129_793, 128, 72, 4),
]


class CheckFailure(AssertionError):
    pass


class Checks:
    def __init__(self) -> None:
        self.total = 0
        self.passed = 0

    def check(self, condition: bool, label: str) -> None:
        self.total += 1
        if not condition:
            raise CheckFailure(label)
        self.passed += 1

    def equal(self, actual: Any, expected: Any, label: str) -> None:
        self.check(actual == expected, f"{label}: {actual!r} != {expected!r}")


def impose_address_space_cap() -> int:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    cap = ADDRESS_SPACE_CAP_BYTES
    if hard != resource.RLIM_INFINITY:
        cap = min(cap, hard)
    if soft == resource.RLIM_INFINITY or soft > cap:
        resource.setrlimit(resource.RLIMIT_AS, (cap, hard))
        soft = cap
    if soft > ADDRESS_SPACE_CAP_BYTES:
        raise CheckFailure("RLIMIT_AS exceeds 2 GiB")
    return int(soft)


def is_prime(n: int) -> bool:
    """Deterministic Miller--Rabin for all 64-bit integers."""
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 325, 9_375, 28_178, 450_775, 9_780_504, 1_795_265_022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def prime_factors(n: int) -> list[int]:
    factors: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


@lru_cache(maxsize=None)
def primitive_root(p: int) -> int:
    if not is_prime(p):
        raise CheckFailure(f"nonprime field modulus {p}")
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise CheckFailure(f"no primitive root modulo {p}")


@lru_cache(maxsize=None)
def subgroup_values(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise CheckFailure(f"n={n} does not divide p-1={p-1}")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    if pow(omega, n, p) != 1:
        raise CheckFailure("omega^n != 1")
    for q in prime_factors(n):
        if pow(omega, n // q, p) == 1:
            raise CheckFailure("omega does not have exact order n")
    values = tuple(pow(omega, i, p) for i in range(n))
    if len(set(values)) != n:
        raise CheckFailure("subgroup values are not distinct")
    return values


def sig3(a: int, b: int, c: int, p: int) -> tuple[int, int]:
    return (-(a + b + c) % p, (a * b + a * c + b * c) % p)


def sig4(a: int, b: int, c: int, d: int, p: int) -> tuple[int, int, int]:
    e1 = (a + b + c + d) % p
    e2 = (a * b + a * c + a * d + b * c + b * d + c * d) % p
    e3 = (a * b * c + a * b * d + a * c * d + b * c * d) % p
    return (-e1 % p, e2, -e3 % p)


def locator_coefficients(indices: tuple[int, ...], values: list[int], p: int) -> list[int]:
    coeff = [1]
    for index in indices:
        root = values[index]
        nxt = [0] * (len(coeff) + 1)
        for j, value in enumerate(coeff):
            nxt[j] = (nxt[j] + value) % p
            nxt[j + 1] = (nxt[j + 1] - root * value) % p
        coeff = nxt
    return coeff


def witness_record(
    u: tuple[int, ...],
    v: tuple[int, ...],
    values: list[int],
    p: int,
) -> dict[str, Any]:
    cu = locator_coefficients(u, values, p)
    cv = locator_coefficients(v, values, p)
    if cu[:-1] != cv[:-1] or cu[-1] == cv[-1]:
        raise CheckFailure("invalid free-1 witness")
    return {
        "U_indices": list(u),
        "V_indices": list(v),
        "U_values": [values[i] for i in u],
        "V_values": [values[i] for i in v],
        "high_signature": cu[1:-1],
        "constant_U": cu[-1],
        "constant_V": cv[-1],
        "constant_delta": (cu[-1] - cv[-1]) % p,
    }


def scan_step(p: int, n: int, t: int, e: int, step: int) -> dict[str, Any]:
    if e not in (3, 4):
        raise CheckFailure("registered scanner only supports e=3,4")
    if math.gcd(step, n) != 1:
        raise CheckFailure("step is not primitive modulo n")
    base = subgroup_values(p, n)
    values = [base[(step * i) % n] for i in range(n)]
    terminal_index = t - 1
    terminal: dict[tuple[int, ...], tuple[int, ...]] = {}

    if e == 3:
        x = values[terminal_index]
        for i in range(t - 1):
            a = values[i]
            for j in range(i + 1, t - 1):
                high = sig3(a, values[j], x, p)
                if high in terminal:
                    raise CheckFailure("two terminal sets share a high")
                terminal[high] = (i, j, terminal_index)
    else:
        x = values[terminal_index]
        for i in range(t - 1):
            a = values[i]
            for j in range(i + 1, t - 1):
                b = values[j]
                for k in range(j + 1, t - 1):
                    high = sig4(a, b, values[k], x, p)
                    if high in terminal:
                        raise CheckFailure("two terminal sets share a high")
                    terminal[high] = (i, j, k, terminal_index)

    partner_multiplicity: dict[tuple[int, ...], int] = {}
    first_pair: tuple[tuple[int, ...], tuple[int, ...]] | None = None

    if e == 3:
        for i in range(t - 1):
            a = values[i]
            for j in range(i + 1, t - 1):
                b = values[j]
                for k in range(j + 1, t - 1):
                    v = (i, j, k)
                    high = sig3(a, b, values[k], p)
                    u = terminal.get(high)
                    if u is None:
                        continue
                    if set(u) & set(v):
                        raise CheckFailure("equal-high sets are not disjoint")
                    partner_multiplicity[high] = partner_multiplicity.get(high, 0) + 1
                    if first_pair is None:
                        first_pair = (u, v)
    else:
        for i in range(t - 1):
            a = values[i]
            for j in range(i + 1, t - 1):
                b = values[j]
                for k in range(j + 1, t - 1):
                    c = values[k]
                    for ell in range(k + 1, t - 1):
                        v = (i, j, k, ell)
                        high = sig4(a, b, c, values[ell], p)
                        u = terminal.get(high)
                        if u is None:
                            continue
                        if set(u) & set(v):
                            raise CheckFailure("equal-high sets are not disjoint")
                        partner_multiplicity[high] = partner_multiplicity.get(high, 0) + 1
                        if first_pair is None:
                            first_pair = (u, v)

    partner_pairs = sum(partner_multiplicity.values())
    return {
        "step": step,
        "T": len(partner_multiplicity),
        "partner_pairs": partner_pairs,
        "max_partners_per_terminal": max(partner_multiplicity.values(), default=0),
        "first_witness": (
            witness_record(first_pair[0], first_pair[1], values, p)
            if first_pair is not None
            else None
        ),
    }


@lru_cache(maxsize=None)
def reference_scan_step(p: int, n: int, t: int, e: int, step: int) -> dict[str, int]:
    """Independent full-fiber path using general locator multiplication."""
    base = subgroup_values(p, n)
    values = [base[(step * i) % n] for i in range(n)]
    fibers: dict[tuple[int, ...], list[int]] = {}
    for indices in itertools.combinations(range(t), e):
        high = tuple(locator_coefficients(indices, values, p)[1:-1])
        cell = fibers.setdefault(high, [0, 0])
        cell[0] += 1
        if indices[-1] == t - 1:
            cell[1] += 1
    terminal_cells = [cell for cell in fibers.values() if cell[1]]
    if any(cell[1] != 1 for cell in terminal_cells):
        raise CheckFailure("reference path found duplicate terminal high")
    return {
        "T": sum(cell[0] > 1 for cell in terminal_cells),
        "partner_pairs": sum(cell[0] - 1 for cell in terminal_cells),
    }


def phase_gate(p: int, n: int, t: int, e: int, step: int) -> bool:
    """Check coefficient scaling on deterministic terminal/nonterminal sets."""
    base = subgroup_values(p, n)
    values = [base[(step * i) % n] for i in range(n)]
    lam = base[7 % n]
    scaled = [(lam * value) % p for value in values]
    samples = [
        tuple(range(e)),
        tuple(range(t - e, t)),
        tuple(list(range(e - 1)) + [t - 1]),
    ]
    for indices in samples:
        before = locator_coefficients(indices, values, p)[1:-1]
        after = locator_coefficients(indices, scaled, p)[1:-1]
        expected = [(value * pow(lam, j, p)) % p for j, value in enumerate(before, 1)]
        if after != expected:
            return False
    return True


def primitive_steps(n: int) -> list[int]:
    return [r for r in range(1, n) if math.gcd(r, n) == 1]


def gradient_block() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for q, p in INDEX_GRADIENT:
        for e in (3, 4):
            print(f"[scan] index-gradient q={q} p={p} e={e}", flush=True)
            result = scan_step(p, 64, 36, e, 1)
            reference = reference_scan_step(p, 64, 36, e, 1)
            if result["T"] != reference["T"]:
                raise CheckFailure("gradient T dual-path mismatch")
            if result["partner_pairs"] != reference["partner_pairs"]:
                raise CheckFailure("gradient pair dual-path mismatch")
            rows.append(
                {
                    "q": q,
                    "p": p,
                    "n": 64,
                    "t": 36,
                    "e": e,
                    "step": 1,
                    "subsets_enumerated": math.comb(36, e),
                    "terminal_candidates": math.comb(35, e - 1),
                    "birthday_load_numerator": math.comb(35, e - 1)
                    * math.comb(35, e),
                    "birthday_load_denominator": p ** (e - 1),
                    "dual_path": reference,
                    "dual_path_match": True,
                    **{key: value for key, value in result.items() if key != "step"},
                }
            )
    return {
        "status": "EXACT_BOUNDED_INDEX_GRADIENT",
        "steps_mode": "canonical_step_only",
        "rows": rows,
        "nonmonotonicity_warning": True,
    }


def sparse_generator_block() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for block_id, p, n, t, e in SPARSE_BLOCKS:
        steps = primitive_steps(n)
        counts: list[int] = []
        pair_counts: list[int] = []
        first_witness: dict[str, Any] | None = None
        for index, step in enumerate(steps, 1):
            if index == 1 or index % 8 == 0 or index == len(steps):
                print(
                    f"[scan] {block_id} primitive step {index}/{len(steps)}",
                    flush=True,
                )
            result = scan_step(p, n, t, e, step)
            counts.append(result["T"])
            pair_counts.append(result["partner_pairs"])
            if first_witness is None and result["first_witness"] is not None:
                first_witness = {
                    "step": step,
                    **result["first_witness"],
                }
        if n in (64, 96):
            reference = reference_scan_step(p, n, t, e, steps[0])
            dual_path: dict[str, Any] = {
                "step": steps[0],
                **reference,
                "match": (
                    reference["T"] == counts[0]
                    and reference["partner_pairs"] == pair_counts[0]
                ),
                "enumeration_accounting": (
                    "cached in index gradient" if n == 64 else "additional"
                ),
            }
            if not dual_path["match"]:
                raise CheckFailure("sparse step-1 dual-path mismatch")
        else:
            dual_path = {
                "step": None,
                "match": None,
                "enumeration_accounting": "omitted: C(72,4) exceeds remaining cap",
            }
        rows.append(
            {
                "id": block_id,
                "p": p,
                "n": n,
                "t": t,
                "e": e,
                "q": (p - 1) // n,
                "prefix_ratio": [t, n],
                "primitive_steps": steps,
                "step_T_counts": counts,
                "step_partner_pair_counts": pair_counts,
                "steps_scanned": len(steps),
                "subsets_per_step": math.comb(t, e),
                "subsets_enumerated": len(steps) * math.comb(t, e),
                "terminal_candidates_per_step": math.comb(t - 1, e - 1),
                "birthday_load_numerator": math.comb(t - 1, e - 1)
                * math.comb(t - 1, e),
                "birthday_load_denominator": p ** (e - 1),
                "T_min": min(counts),
                "T_max": max(counts),
                "T_sum": sum(counts),
                "all_zero": all(value == 0 for value in counts),
                "first_witness": first_witness,
                "phase_invariant": phase_gate(p, n, t, e, steps[0]),
                "dual_path": dual_path,
            }
        )
    return {
        "status": "EXACT_ALL_PRIMITIVE_STEPS_ON_REGISTERED_ROWS",
        "steps_mode": "all_units_mod_n",
        "rows": rows,
    }


def primary_subset_total() -> int:
    gradient = len(INDEX_GRADIENT) * sum(math.comb(36, e) for e in (3, 4))
    sparse = sum(
        len(primitive_steps(n)) * math.comb(t, e)
        for _block_id, _p, n, t, e in SPARSE_BLOCKS
    )
    return gradient + sparse


def dual_path_subset_total() -> int:
    gradient = len(INDEX_GRADIENT) * sum(math.comb(36, e) for e in (3, 4))
    return gradient + math.comb(54, 3)


def registered_subset_total() -> int:
    return primary_subset_total() + dual_path_subset_total()


def build_certificate() -> dict[str, Any]:
    registered_total = registered_subset_total()
    if registered_total > SUBSET_EVALUATION_CAP:
        raise CheckFailure("registered scan exceeds subset cap")
    gradient = gradient_block()
    sparse = sparse_generator_block()
    computed_primary = sum(row["subsets_enumerated"] for row in gradient["rows"])
    computed_primary += sum(row["subsets_enumerated"] for row in sparse["rows"])
    computed_dual = dual_path_subset_total()
    computed_total = computed_primary + computed_dual
    if computed_total != registered_total:
        raise CheckFailure("derived subset total mismatch")
    return {
        "packet": "kb_qatom_route_d_sparse_arc_scan",
        "date": "2026-07-09",
        "status": "AUDIT_EXPERIMENTAL_DEPLOYED_OPEN",
        "claims": {
            "proves_registered_finite_counts": True,
            "proves_all_primitive_steps_on_sparse_blocks": True,
            "proves_phase_invariance": True,
            "supports_sparse_arc_followup_to_v54": True,
            "proves_deployed_T_le_H2": False,
            "proves_monotonicity_in_index": False,
            "proves_A_SP_le_tp": False,
            "proves_R2_le_ep": False,
        },
        "deployed": {
            "p": P_KB,
            "n": N_KB,
            "n_prime": T_KB,
            "e": E_KB,
            "subgroup_index": INDEX_KB,
            "H2": H2_KB,
            "prefix_ratio": [T_KB, N_KB],
            "wall_status": "OPEN",
        },
        "caps": {
            "address_space_bytes": ADDRESS_SPACE_CAP_BYTES,
            "subset_evaluations_cap": SUBSET_EVALUATION_CAP,
            "primary_subset_evaluations": computed_primary,
            "dual_path_subset_evaluations": computed_dual,
            "registered_subset_evaluations": registered_total,
            "computed_subset_evaluations": computed_total,
            "largest_per_step_chunk": max(
                math.comb(t, e) for _block_id, _p, _n, t, e in SPARSE_BLOCKS
            ),
            "largest_terminal_map": max(
                math.comb(t - 1, e - 1)
                for _block_id, _p, _n, t, e in SPARSE_BLOCKS
            ),
            "e_max": 4,
            "shape_e5_omitted": {
                "n": 160,
                "t": 90,
                "e": 5,
                "one_step_subsets": math.comb(90, 5),
                "all_primitive_steps": len(primitive_steps(160)),
                "all_steps_subsets": len(primitive_steps(160)) * math.comb(90, 5),
                "reason": "all-step row exceeds the registered 70m cap",
            },
        },
        "method": {
            "object": "terminal e-sets with a distinct equal-high locator partner",
            "high_signature": "coefficients X^(e-1) through X of the monic locator",
            "terminal_vs_nonterminal_split": True,
            "equal_high_sets_checked_disjoint": True,
            "steps_chunked_independently": True,
            "independent_full_fiber_crosscheck": True,
            "stdlib_only": True,
            "forbidden_overnight_scans_used": False,
        },
        "scan": {
            "index_gradient": gradient,
            "sparse_generator_exhaustion": sparse,
        },
        "verdict": {
            "registered_sparse_blocks_all_zero": all(
                row["all_zero"] for row in sparse["rows"]
            ),
            "bounded_finite_result": (
                "All registered q~1016 primitive-step arcs have T=0 for e=3,4."
            ),
            "deployment_impact": (
                "No deployed bound: the small-e rows are birthday-underloaded and "
                "do not control e=67472."
            ),
            "v54_comparison": (
                "v54 already refutes pack-k-only bounds on dense n~p toys; this "
                "packet isolates sparse subgroup index and does not repeat that table."
            ),
        },
        "lineage": {
            "supports_scott_hughes_route_d": True,
            "source": "Scott Hughes Route-D line integrated through v54 (PR #423)",
            "independent_followup": True,
        },
    }


def validate_witness(
    row: dict[str, Any], witness: dict[str, Any], step: int, checks: Checks
) -> None:
    p, n, t, e = row["p"], row["n"], row["t"], row["e"]
    base = subgroup_values(p, n)
    values = [base[(step * i) % n] for i in range(n)]
    u = tuple(witness["U_indices"])
    v = tuple(witness["V_indices"])
    checks.equal(len(u), e, "witness |U|")
    checks.equal(len(v), e, "witness |V|")
    checks.equal(list(u), sorted(set(u)), "witness U set")
    checks.equal(list(v), sorted(set(v)), "witness V set")
    checks.check(all(0 <= index < t for index in u + v), "witness prefix")
    checks.check(t - 1 in u, "witness terminal U")
    checks.check(not (set(u) & set(v)), "witness disjoint")
    cu = locator_coefficients(u, values, p)
    cv = locator_coefficients(v, values, p)
    checks.equal(cu[:-1], cv[:-1], "witness equal high")
    checks.check(cu[-1] != cv[-1], "witness nonzero constant difference")
    checks.equal(witness["U_values"], [values[index] for index in u], "U values")
    checks.equal(witness["V_values"], [values[index] for index in v], "V values")
    checks.equal(witness["high_signature"], cu[1:-1], "witness signature")
    checks.equal(witness["constant_U"], cu[-1], "witness constant U")
    checks.equal(witness["constant_V"], cv[-1], "witness constant V")
    checks.equal(
        witness["constant_delta"], (cu[-1] - cv[-1]) % p, "witness delta"
    )


def validate_certificate(
    cert: dict[str, Any], replay: dict[str, Any] | None, checks: Checks
) -> None:
    checks.equal(cert["packet"], "kb_qatom_route_d_sparse_arc_scan", "packet")
    checks.equal(cert["status"], "AUDIT_EXPERIMENTAL_DEPLOYED_OPEN", "status")
    checks.equal(cert["deployed"]["p"], P_KB, "KB p")
    checks.equal(cert["deployed"]["n"], N_KB, "KB n")
    checks.equal(cert["deployed"]["n_prime"], T_KB, "KB n prime")
    checks.equal(cert["deployed"]["e"], E_KB, "KB e")
    checks.equal(cert["deployed"]["H2"], H2_KB, "KB H2")
    checks.equal(cert["deployed"]["subgroup_index"], INDEX_KB, "KB index")
    checks.check(is_prime(P_KB), "KB prime gate")
    checks.equal(cert["deployed"]["wall_status"], "OPEN", "wall stays open")
    checks.equal(cert["claims"]["proves_deployed_T_le_H2"], False, "nonclaim H2")
    checks.equal(
        cert["claims"]["proves_monotonicity_in_index"], False, "nonclaim monotone"
    )
    checks.equal(cert["claims"]["proves_A_SP_le_tp"], False, "nonclaim ASP")
    checks.equal(cert["claims"]["proves_R2_le_ep"], False, "nonclaim R2")
    checks.equal(
        cert["lineage"]["supports_scott_hughes_route_d"], True, "Hughes lineage"
    )
    checks.equal(
        cert["lineage"]["independent_followup"], True, "independent followup"
    )

    caps = cert["caps"]
    derived_total = registered_subset_total()
    checks.equal(
        caps["primary_subset_evaluations"],
        primary_subset_total(),
        "primary cap total",
    )
    checks.equal(
        caps["dual_path_subset_evaluations"],
        dual_path_subset_total(),
        "dual-path cap total",
    )
    checks.equal(
        caps["registered_subset_evaluations"], derived_total, "derived cap total"
    )
    checks.equal(caps["computed_subset_evaluations"], derived_total, "computed cap total")
    checks.check(derived_total <= caps["subset_evaluations_cap"], "total within cap")
    checks.equal(caps["subset_evaluations_cap"], SUBSET_EVALUATION_CAP, "cap pin")
    checks.equal(caps["address_space_bytes"], ADDRESS_SPACE_CAP_BYTES, "memory cap")
    checks.equal(caps["largest_per_step_chunk"], math.comb(72, 4), "chunk cap")
    checks.equal(caps["largest_terminal_map"], math.comb(71, 3), "terminal map cap")
    checks.equal(caps["e_max"], 4, "e truncation")
    checks.equal(
        caps["shape_e5_omitted"]["one_step_subsets"],
        math.comb(90, 5),
        "e5 one step",
    )
    checks.equal(
        caps["shape_e5_omitted"]["all_steps_subsets"],
        len(primitive_steps(160)) * math.comb(90, 5),
        "e5 all steps",
    )
    checks.check(
        caps["shape_e5_omitted"]["all_steps_subsets"] > SUBSET_EVALUATION_CAP,
        "e5 exclusion exceeds cap",
    )

    gradient_rows = cert["scan"]["index_gradient"]["rows"]
    checks.equal(len(gradient_rows), 2 * len(INDEX_GRADIENT), "gradient row count")
    positive_rows = 0
    for row in gradient_rows:
        checks.check(is_prime(row["p"]), "gradient p prime")
        checks.equal(row["p"], row["q"] * row["n"] + 1, "gradient index identity")
        checks.equal(
            row["subsets_enumerated"],
            math.comb(row["t"], row["e"]),
            "gradient subsets",
        )
        checks.equal(
            row["terminal_candidates"],
            math.comb(row["t"] - 1, row["e"] - 1),
            "gradient terminal",
        )
        checks.check(row["T"] <= row["terminal_candidates"], "gradient T range")
        checks.equal(row["dual_path"]["T"], row["T"], "gradient dual T")
        checks.equal(
            row["dual_path"]["partner_pairs"],
            row["partner_pairs"],
            "gradient dual pairs",
        )
        checks.equal(row["dual_path_match"], True, "gradient dual gate")
        if row["T"]:
            positive_rows += 1
            checks.check(row["first_witness"] is not None, "positive row witness")
            validate_witness(row, row["first_witness"], row["step"], checks)
        else:
            checks.equal(row["first_witness"], None, "zero row no witness")
    checks.check(positive_rows >= 3, "positive controls present")

    sparse_rows = cert["scan"]["sparse_generator_exhaustion"]["rows"]
    checks.equal(len(sparse_rows), len(SPARSE_BLOCKS), "sparse block count")
    for row in sparse_rows:
        checks.check(is_prime(row["p"]), "sparse p prime")
        checks.equal(row["p"], row["q"] * row["n"] + 1, "sparse index identity")
        units = primitive_steps(row["n"])
        checks.equal(row["primitive_steps"], units, "all primitive steps")
        checks.equal(row["steps_scanned"], len(units), "step count")
        checks.equal(len(row["step_T_counts"]), len(units), "T vector length")
        checks.equal(
            len(row["step_partner_pair_counts"]), len(units), "pair vector length"
        )
        checks.equal(
            row["subsets_per_step"],
            math.comb(row["t"], row["e"]),
            "step subsets",
        )
        checks.equal(
            row["subsets_enumerated"],
            len(units) * math.comb(row["t"], row["e"]),
            "block subsets",
        )
        checks.equal(
            row["terminal_candidates_per_step"],
            math.comb(row["t"] - 1, row["e"] - 1),
            "block terminal",
        )
        checks.equal(
            row["birthday_load_numerator"],
            math.comb(row["t"] - 1, row["e"] - 1)
            * math.comb(row["t"] - 1, row["e"]),
            "block load numerator",
        )
        checks.equal(
            row["birthday_load_denominator"],
            row["p"] ** (row["e"] - 1),
            "block load denominator",
        )
        checks.equal(row["T_min"], min(row["step_T_counts"]), "T min")
        checks.equal(row["T_max"], max(row["step_T_counts"]), "T max")
        checks.equal(row["T_sum"], sum(row["step_T_counts"]), "T sum")
        checks.equal(
            row["all_zero"],
            all(value == 0 for value in row["step_T_counts"]),
            "all zero flag",
        )
        checks.equal(row["all_zero"], True, "registered sparse block zero")
        checks.equal(row["phase_invariant"], True, "phase gate")
        checks.equal(row["first_witness"], None, "sparse zero witness")
        if row["n"] in (64, 96):
            checks.equal(row["dual_path"]["step"], units[0], "sparse dual step")
            checks.equal(row["dual_path"]["T"], row["step_T_counts"][0], "sparse dual T")
            checks.equal(
                row["dual_path"]["partner_pairs"],
                row["step_partner_pair_counts"][0],
                "sparse dual pairs",
            )
            checks.equal(row["dual_path"]["match"], True, "sparse dual gate")
        else:
            checks.equal(row["dual_path"]["match"], None, "dual-path cap omission")

    checks.equal(
        cert["verdict"]["registered_sparse_blocks_all_zero"], True, "zero verdict"
    )
    checks.equal(
        cert["method"]["forbidden_overnight_scans_used"], False, "do-not gate"
    )
    checks.equal(cert["method"]["steps_chunked_independently"], True, "chunk gate")
    checks.equal(
        cert["method"]["independent_full_fiber_crosscheck"], True, "dual-path gate"
    )
    if replay is not None:
        checks.equal(cert, replay, "full exact replay")


def tamper_suite(cert: dict[str, Any], replay: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []
    mutations.append(
        (
            "promote-deployed-H2",
            lambda d: d["claims"].__setitem__("proves_deployed_T_le_H2", True),
        )
    )
    mutations.append(
        (
            "cap-total",
            lambda d: d["caps"].__setitem__(
                "registered_subset_evaluations",
                d["caps"]["registered_subset_evaluations"] - 1,
            ),
        )
    )
    mutations.append(
        (
            "field-index",
            lambda d: d["scan"]["sparse_generator_exhaustion"]["rows"][
                0
            ].__setitem__("p", 65_091),
        )
    )
    mutations.append(
        (
            "zero-count",
            lambda d: d["scan"]["sparse_generator_exhaustion"]["rows"][0][
                "step_T_counts"
            ].__setitem__(0, 1),
        )
    )
    mutations.append(
        (
            "gradient-count",
            lambda d: d["scan"]["index_gradient"]["rows"][0].__setitem__(
                "T", d["scan"]["index_gradient"]["rows"][0]["T"] + 1
            ),
        )
    )
    mutations.append(
        (
            "dual-path",
            lambda d: d["scan"]["index_gradient"]["rows"][0].__setitem__(
                "dual_path_match", False
            ),
        )
    )

    def mutate_witness_index(d: dict[str, Any]) -> None:
        witness = next(
            row["first_witness"]
            for row in d["scan"]["index_gradient"]["rows"]
            if row["first_witness"] is not None
        )
        witness["U_indices"][0] = witness["U_indices"][1]

    def mutate_witness_signature(d: dict[str, Any]) -> None:
        witness = next(
            row["first_witness"]
            for row in d["scan"]["index_gradient"]["rows"]
            if row["first_witness"] is not None
        )
        witness["high_signature"][0] += 1

    mutations.append(("witness-index", mutate_witness_index))
    mutations.append(("witness-signature", mutate_witness_signature))
    mutations.append(
        (
            "lineage",
            lambda d: d["lineage"].__setitem__(
                "supports_scott_hughes_route_d", False
            ),
        )
    )

    caught = 0
    for label, mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate_certificate(bad, replay, Checks())
        except (CheckFailure, KeyError, IndexError, TypeError, ValueError):
            caught += 1
            print(f"[tamper] CAUGHT {label}")
        else:
            print(f"[tamper] MISSED {label}")
    return caught, len(mutations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true")
    args = parser.parse_args()

    effective_cap = impose_address_space_cap()
    print(f"[cap] RLIMIT_AS={effective_cap} bytes; subset cap={SUBSET_EVALUATION_CAP}")
    replay = build_certificate()

    if args.generate:
        checks = Checks()
        validate_certificate(replay, None, checks)
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n")
        print(f"RESULT: GENERATED ({checks.passed}/{checks.total} checks)")
        print(f"certificate: {CERT_PATH}")
        return

    if not CERT_PATH.exists():
        raise CheckFailure(f"missing certificate: {CERT_PATH}")
    stored = json.loads(CERT_PATH.read_text())
    checks = Checks()
    validate_certificate(stored, replay, checks)
    caught, total = tamper_suite(stored, replay)
    checks.check(total >= 5, "at least five tampers")
    checks.equal(caught, total, "all tampers caught")
    print(f"RESULT: PASS ({checks.passed}/{checks.total} checks; tampers {caught}/{total})")
    print(f"registered subset evaluations: {registered_subset_total()}")
    print("status: AUDIT / EXPERIMENTAL; deployed |T|<=H2 remains OPEN")


if __name__ == "__main__":
    main()
