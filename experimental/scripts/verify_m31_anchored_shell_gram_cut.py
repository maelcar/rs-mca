#!/usr/bin/env python3
"""Exact verifier for the M31 anchored two-shell Gram cut.

The theorem is a local, anchor-conditioned PSD obstruction.  It is not a
row-sharp Q theorem and does not pay a union of different shell-pair cells.
All deployed decisions below use integer arithmetic.
"""

import copy
import hashlib
import json
import os
import sys
from itertools import combinations
from math import comb


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(
    ROOT,
    "experimental",
    "data",
    "cap25_v13_m31_anchored_shell_gram_cut.json",
)
CHECKS = []


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    suffix = f" ({detail})" if detail else ""
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{suffix}")


def ceil_div(a, b):
    return -((-a) // b)


def falling(x, length):
    out = 1
    for i in range(length):
        out *= x - i
    return out


def normalized_eberlein_numerator(v, m, distance, level):
    """Numerator of the normalized Johnson eigenvalue.

    The common positive denominator is
    falling(m, level) * falling(v-m, level).  This is the exact formula
    independently used by PR #495's Johnson-scheme verifier.
    """
    return sum(
        (-1) ** s
        * comb(level, s)
        * falling(distance, s) ** 2
        * falling(m - distance, level - s)
        * falling(v - m - distance, level - s)
        for s in range(level + 1)
    )


def normalized_eberlein_denominator(v, m, level):
    return falling(m, level) * falling(v - m, level)


def johnson_lp_infeasible(v, m, e1, e2, size, level_max=6):
    """Exact two-variable Johnson Delsarte feasibility through level_max.

    For inner distribution (1, alpha, beta), alpha+beta=size-1, each
    Johnson eigenspace imposes 1+alpha*p_j(e1)+beta*p_j(e2)>=0.  The
    feasible alpha interval is intersected with exact rational endpoints.
    """
    low_num, low_den = 0, 1
    high_num, high_den = size - 1, 1
    for level in range(1, level_max + 1):
        den = normalized_eberlein_denominator(v, m, level)
        if den == 0:
            continue
        n1 = normalized_eberlein_numerator(v, m, e1, level)
        n2 = normalized_eberlein_numerator(v, m, e2, level)
        coefficient = n1 - n2
        rhs = -den - (size - 1) * n2
        if coefficient > 0:
            if rhs * low_den > low_num * coefficient:
                low_num, low_den = rhs, coefficient
        elif coefficient < 0:
            endpoint_num, endpoint_den = -rhs, -coefficient
            if endpoint_num * high_den < high_num * endpoint_den:
                high_num, high_den = endpoint_num, endpoint_den
        elif rhs > 0:
            return True, level
        if low_num * high_den > high_num * low_den:
            return True, level
    return False, None


def canonical_hash(rows):
    payload = ";".join(",".join(map(str, row)) for row in sorted(rows))
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def exchange_distance(a, b, m):
    return m - (a & b).bit_count()


def sos_identity_holds(n, m, anchor, shell):
    """Replay the exact block-centering SOS identity on bit-mask supports."""
    h = len(shell)
    if not shell:
        return True
    e = exchange_distance(anchor, shell[0], m)
    if any(exchange_distance(anchor, b, m) != e for b in shell):
        return False

    p_counts = [0] * n
    q_counts = [0] * n
    summed = [0] * n
    for b in shell:
        for i in range(n):
            a_i = (anchor >> i) & 1
            b_i = (b >> i) & 1
            summed[i] += b_i - a_i
            if not a_i and b_i:
                p_counts[i] += 1
            if a_i and not b_i:
                q_counts[i] += 1

    lhs = m * (n - m) * sum(x * x for x in summed) - n * h * h * e * e
    in_anchor = [i for i in range(n) if (anchor >> i) & 1]
    outside = [i for i in range(n) if not ((anchor >> i) & 1)]
    rhs = (n - m) * sum(
        (q_counts[i] - q_counts[j]) ** 2 for i, j in combinations(in_anchor, 2)
    )
    rhs += m * sum(
        (p_counts[i] - p_counts[j]) ** 2 for i, j in combinations(outside, 2)
    )
    return lhs == rhs and rhs >= 0


def sos_toy_checks():
    n, m = 8, 4
    anchor = sum(1 << i for i in range(m))
    supports = [sum(1 << i for i in c) for c in combinations(range(n), m)]
    by_distance = {}
    for support in supports:
        if support != anchor:
            by_distance.setdefault(exchange_distance(anchor, support, m), []).append(support)

    tests = []
    for distance, shell in sorted(by_distance.items()):
        selections = [
            shell,
            shell[:1],
            shell[: min(3, len(shell))],
            shell[::2],
            shell[1::3],
        ]
        for selected in selections:
            if selected:
                tests.append(sos_identity_holds(n, m, anchor, selected))
        # Exhaust every subfamily of the distance-one shell (16 members).
        if distance == 1:
            for mask in range(1, 1 << len(shell)):
                selected = [shell[i] for i in range(len(shell)) if (mask >> i) & 1]
                tests.append(sos_identity_holds(n, m, anchor, selected))
    return all(tests), len(tests)


def build_packet():
    p = 2**31 - 1
    n = 2**21
    a_plus = 1_116_023
    m = n - a_plus
    w = 67_447
    budget = 2**24 - 1
    first_violating_size = budget + 1
    product = m * (n - m)
    clique_cap = n - w

    quotient, remainder = divmod(first_violating_size, clique_cap)
    complement_edges_min = remainder * comb(quotient + 1, 2)
    complement_edges_min += (clique_cap - remainder) * comb(quotient, 2)

    grid = []
    gram_cut = []
    for kappa in range(2, 775):
        low = ceil_div(w + 1, kappa - 1)
        high = min(m // kappa, product // (n * (kappa - 1)))
        for scale in range(low, high + 1):
            e1 = (kappa - 1) * scale
            e2 = kappa * scale
            row = (kappa, scale, e1, e2)
            grid.append(row)
            if 8 * n * kappa * kappa * scale > (9 * kappa + 7) * product:
                gram_cut.append(row)

    overlap = []
    overlap_levels = {}
    for row in gram_cut:
        kappa, scale, e1, e2 = row
        infeasible, level = johnson_lp_infeasible(
            n, m, e1, e2, first_violating_size, level_max=6
        )
        if infeasible:
            overlap.append(row)
            overlap_levels[str(level)] = overlap_levels.get(str(level), 0) + 1

    overlap_set = set(overlap)
    new_cut = [row for row in gram_cut if row not in overlap_set]
    cut_by_kappa = {}
    for row in gram_cut:
        cut_by_kappa[str(row[0])] = cut_by_kappa.get(str(row[0]), 0) + 1

    intervals = {}
    for kappa in sorted({row[0] for row in gram_cut}):
        values = [row[1] for row in gram_cut if row[0] == kappa]
        intervals[str(kappa)] = [min(values), max(values)]

    pr495_survivors = 3_254_358
    packet = {
        "schema": "cap25-v13-m31-anchored-shell-gram-cut-v1",
        "status": (
            "PROVED anchored two-shell Gram/Turan obstruction and exact deployed "
            "cut; OPEN remaining two-shell grid and full M31 row"
        ),
        "deployed": {
            "p": p,
            "n": n,
            "a_plus": a_plus,
            "m": m,
            "w": w,
            "Bstar": budget,
            "L0": first_violating_size,
            "m_times_n_minus_m": product,
            "one_shell_clique_cap": clique_cap,
        },
        "turan": {
            "quotient": quotient,
            "remainder": remainder,
            "complement_edges_min": complement_edges_min,
            "twice_edges_minus_7L0": 2 * complement_edges_min
            - 7 * first_violating_size,
            "forced_e2_degree_min": 8,
        },
        "grid": {
            "pair_count": len(grid),
            "first_row": list(grid[0]),
            "last_row": list(grid[-1]),
        },
        "anchored_gram_cut": {
            "necessary_inequality": "8*n*kappa^2*t <= (9*kappa+7)*m*(n-m)",
            "cut_count": len(gram_cut),
            "cut_by_kappa": cut_by_kappa,
            "cut_intervals": intervals,
            "all_cut_sha256": canonical_hash(gram_cut),
            "first_failure_margins": {
                "2,407905": 8 * n * 2**2 * 407_905 - 25 * product,
                "2,407906": 8 * n * 2**2 * 407_906 - 25 * product,
                "3,246556": 8 * n * 3**2 * 246_556 - 34 * product,
                "3,246557": 8 * n * 3**2 * 246_557 - 34 * product,
            },
        },
        "comparison_to_pr495": {
            "baseline": "open PR #495 exact Johnson LP scan through j<=6",
            "baseline_surviving_count": pr495_survivors,
            "overlap_count": len(overlap),
            "overlap_binding_levels": overlap_levels,
            "overlap_interval": [
                min(row[1] for row in overlap),
                max(row[1] for row in overlap),
            ],
            "overlap_sha256": canonical_hash(overlap),
            "new_cut_count": len(new_cut),
            "new_cut_sha256": canonical_hash(new_cut),
            "surviving_after_both": pr495_survivors - len(new_cut),
        },
        "nonclaims": {
            "full_m31_row_paid": False,
            "many_shell_residual_paid": False,
            "row_sharp_q_proved": False,
            "union_of_shell_pair_cells_paid": False,
        },
    }
    return packet, grid, gram_cut, overlap, new_cut


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        packet, *_ = build_packet()
        print(json.dumps(packet, indent=2, sort_keys=True))
        return 0
    if len(sys.argv) != 1:
        print("usage: verify_m31_anchored_shell_gram_cut.py [--emit]")
        return 2

    with open(DATA, encoding="utf-8") as handle:
        committed = json.load(handle)
    expected, grid, gram_cut, overlap, new_cut = build_packet()

    dep = expected["deployed"]
    turan = expected["turan"]
    cut = expected["anchored_gram_cut"]
    comparison = expected["comparison_to_pr495"]

    print("== Deployed constants and one-shell affine cap ==")
    check("M31 constants", (dep["n"], dep["m"], dep["w"])
          == (2_097_152, 981_129, 67_447))
    check("first violating size L0=8n", dep["L0"] == 8 * dep["n"])
    check("one-shell clique cap n-w", dep["one_shell_clique_cap"] == 2_029_705)

    print("\n== Turan anchor forcing ==")
    check("L0=8r+8w with remainder below r",
          turan["quotient"] == 8 and turan["remainder"] == 8 * dep["w"]
          and turan["remainder"] < dep["one_shell_clique_cap"])
    check("minimum e2-pair count", turan["complement_edges_min"] == 61_148_348)
    check("average e2-degree is strictly above 7",
          turan["twice_edges_minus_7L0"] == 72 * dep["w"] > 0)
    check("integral anchor shell has size at least 8",
          turan["forced_e2_degree_min"] == 8)

    print("\n== Exact SOS identity ==")
    sos_ok, sos_count = sos_toy_checks()
    check("block-centering identity on deterministic/exhaustive toys", sos_ok,
          f"families={sos_count}")

    print("\n== Deployed grid and anchored Gram cut ==")
    check("integral-ratio grid has 3,254,885 pairs", len(grid) == 3_254_885)
    check("complete Gram cut has 97,162 pairs", len(gram_cut) == 97_162)
    check("cut is confined to kappa=2,3", {row[0] for row in gram_cut} == {2, 3})
    check("kappa=2 interval and count",
          cut["cut_intervals"]["2"] == [407_906, 490_564]
          and cut["cut_by_kappa"]["2"] == 82_659)
    check("kappa=3 interval and count",
          cut["cut_intervals"]["3"] == [246_557, 261_059]
          and cut["cut_by_kappa"]["3"] == 14_503)
    check("exact first-failure margins", cut["first_failure_margins"] == {
        "2,407905": -22_079_255,
        "2,407906": 45_029_609,
        "3,246556": -16_606_014,
        "3,246557": 134_388_930,
    })
    check("no cut for kappa>=4 by exact scan",
          all(row[0] < 4 for row in gram_cut))

    print("\n== Exact overlap with open PR #495 ==")
    check("Johnson j<=6 overlap is 143", len(overlap) == 143)
    check("overlap is kappa=3, t=260917..261059",
          {row[0] for row in overlap} == {3}
          and comparison["overlap_interval"] == [260_917, 261_059])
    check("97,019 cuts are new beyond #495", len(new_cut) == 97_019)
    check("combined survivor count is 3,157,339",
          comparison["surviving_after_both"] == 3_157_339)

    print("\n== Committed certificate ==")
    check("JSON packet exactly matches regeneration", committed == expected)
    tampered = copy.deepcopy(committed)
    tampered["anchored_gram_cut"]["cut_count"] -= 1
    check("cut-count corruption is rejected", tampered != expected)
    tampered = copy.deepcopy(committed)
    tampered["comparison_to_pr495"]["new_cut_sha256"] = "0" * 64
    check("hash corruption is rejected", tampered != expected)
    tampered = copy.deepcopy(committed)
    tampered["nonclaims"]["full_m31_row_paid"] = True
    check("scope corruption is rejected", tampered != expected)

    passed = sum(ok for _name, ok in CHECKS)
    total = len(CHECKS)
    print(f"\nRESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total} checks)")
    print(f"grid={len(grid)}")
    print(f"gram_cut={len(gram_cut)}")
    print(f"overlap_with_pr495={len(overlap)}")
    print(f"new_beyond_pr495={len(new_cut)}")
    print(f"surviving_after_both={comparison['surviving_after_both']}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
