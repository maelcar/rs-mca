#!/usr/bin/env python3
"""Exact finite certificates refuting the proposed global RS prefix law.

Uses only Python's standard library.  It verifies:
  A. F_7, D={0,...,5}, K=2, a=3: exact list count 4 > L_pref=3,
     exact single-prefix maximum 3, and exact MCA-bad slope count 4 > M_pref=1.
  B. F_23, D=quadratic residues, K=7, a=8: exact prefix list count
     11 > L_pref=8, and exact pole-line MCA-bad slope count 11 > M_pref=2.
"""
from collections import Counter, defaultdict
from itertools import combinations, product
from math import comb
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "prefix-staircase-extremality"
    / "prefix_staircase_counterexamples.json"
)


def ceil_div(a: int, b: int) -> int:
    return (a + b - 1) // b


def eval_affine(A: int, B: int, x: int, p: int) -> int:
    return (A + B * x) % p


def locator_coeffs(S, p):
    """Ascending coefficients of prod_{x in S}(X-x)."""
    coeffs = [1]
    for x in S:
        nxt = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            nxt[i] = (nxt[i] - c * x) % p
            nxt[i + 1] = (nxt[i + 1] + c) % p
        coeffs = nxt
    return coeffs


def case_f7():
    p = 7
    D = tuple(range(6))
    n = len(D)
    K = 2
    a = 3
    U = (0, 0, 0, 1, 5, 4)

    hits = []
    residual_rows = []
    for B in range(p):
        residuals = tuple((U[x] - B * x) % p for x in D)
        counts = Counter(residuals)
        residual_rows.append({
            "B": B,
            "residuals": residuals,
            "max_multiplicity": max(counts.values()),
        })
        for A, multiplicity in counts.items():
            if multiplicity >= a:
                support = tuple(x for x in D if eval_affine(A, B, x, p) == U[x])
                hits.append({"A": A, "B": B, "support": support})

    hits.sort(key=lambda h: (h["B"], h["A"]))
    assert hits == [
        {"A": 0, "B": 0, "support": (0, 1, 2)},
        {"A": 3, "B": 4, "support": (1, 3, 4)},
        {"A": 0, "B": 5, "support": (0, 3, 5)},
        {"A": 2, "B": 6, "support": (2, 4, 5)},
    ]

    # Exhaustive global list maximum over all 7^6 received words.
    code = [
        ((A, B), tuple(eval_affine(A, B, x, p) for x in D))
        for A, B in product(range(p), repeat=2)
    ]
    global_max = 0
    maximizers = 0
    for y in product(range(p), repeat=n):
        count = sum(
            sum(1 for i in range(n) if word[i] == y[i]) >= a
            for _, word in code
        )
        if count > global_max:
            global_max = count
            maximizers = 1
        elif count == global_max:
            maximizers += 1
    assert global_max == 4

    # Exact depth-3 prefix fibers: Phi=-sum mod 7.
    fibers = defaultdict(list)
    for S in combinations(D, a):
        fibers[(-sum(S)) % p].append(S)
    fiber_sizes = {z: len(fibers[z]) for z in range(p)}
    assert fiber_sizes == {0: 3, 1: 3, 2: 3, 3: 2, 4: 3, 5: 3, 6: 3}

    L_pref = ceil_div(comb(n, a), p ** (a - K))
    assert L_pref == 3

    # Pole line at alpha=6 for MCA code k=1 (constants).
    alpha = 6
    k = 1
    f = tuple(U[x] * pow((x - alpha) % p, -1, p) % p for x in D)
    g = tuple(-pow((x - alpha) % p, -1, p) % p for x in D)
    slope_data = []
    for gamma in range(p):
        h = tuple((f[i] + gamma * g[i]) % p for i in range(n))
        counts = Counter(h)
        close_values = sorted(v for v, mult in counts.items() if mult >= a)
        if close_values:
            supports = {
                v: tuple(D[i] for i, hv in enumerate(h) if hv == v)
                for v in close_values
            }
            slope_data.append({"gamma": gamma, "word": h, "supports": supports})
    assert [row["gamma"] for row in slope_data] == [0, 2, 3, 6]

    L_plus = L_pref
    M_pref = ceil_div(L_plus * (p - n), (p - n) + k * (L_plus - 1))
    assert M_pref == 1

    return {
        "field": p,
        "domain": D,
        "n": n,
        "K_list": K,
        "k_MCA": k,
        "agreement": a,
        "received_word": U,
        "list_hits": hits,
        "chosen_word_list_count": len(hits),
        "global_list_max": global_max,
        "number_of_global_maximizers": maximizers,
        "prefix_fiber_sizes": fiber_sizes,
        "prefix_fiber_max": max(fiber_sizes.values()),
        "L_pref": L_pref,
        "pole_alpha": alpha,
        "f": f,
        "g": g,
        "MCA_bad_slopes": [row["gamma"] for row in slope_data],
        "MCA_slope_data": slope_data,
        "MCA_bad_count": len(slope_data),
        "M_pref": M_pref,
        "residual_rows": residual_rows,
    }


def case_f23():
    p = 23
    D = tuple(sorted({(x * x) % p for x in range(1, p)}))
    assert D == (1, 2, 3, 4, 6, 8, 9, 12, 13, 16, 18)
    n = len(D)
    assert n == 11
    assert all((x * y) % p in D for x in D for y in D)

    K = 7
    k = 6
    a = 8
    U = tuple(pow(x, a, p) for x in D)

    zero_sum_triples = tuple(T for T in combinations(D, 3) if sum(T) % p == 0)
    assert len(zero_sum_triples) == 11
    supports = tuple(tuple(x for x in D if x not in T) for T in zero_sum_triples)
    assert all(sum(M) % p == 0 for M in supports)

    codewords = []
    slopes = []
    for T, M in zip(zero_sum_triples, supports):
        loc = locator_coeffs(M, p)
        # U polynomial is X^8. c=X^8-Lambda_M.
        c = [(-coef) % p for coef in loc]
        c[8] = (c[8] + 1) % p
        while c and c[-1] == 0:
            c.pop()
        assert len(c) <= K  # degree < K
        product_T = 1
        product_M = 1
        for x in T:
            product_T = product_T * x % p
        for x in M:
            product_M = product_M * x % p
        gamma = (-product_M) % p
        assert gamma == (-pow(product_T, -1, p)) % p
        codewords.append({
            "T": T,
            "support_M": M,
            "coefficients_ascending": tuple(c),
            "product_T": product_T,
            "gamma": gamma,
        })
        slopes.append(gamma)

    assert len(set(slopes)) == 11
    assert set(slopes) == {(-x) % p for x in D}

    L_pref = ceil_div(comb(n, a), p ** (a - K))
    M_pref = ceil_div(L_pref * (p - n), (p - n) + k * (L_pref - 1))
    assert L_pref == 8
    assert M_pref == 2

    # Exact prefix fiber count at z=0 for 8-subsets.
    zero_sum_eight_sets = tuple(M for M in combinations(D, a) if sum(M) % p == 0)
    assert set(zero_sum_eight_sets) == set(supports)

    return {
        "field": p,
        "domain": D,
        "n": n,
        "K_list": K,
        "k_MCA": k,
        "agreement": a,
        "received_word_U_equals_x_power": a,
        "zero_sum_triples": zero_sum_triples,
        "prefix_supports": supports,
        "codewords": codewords,
        "exact_list_count": len(codewords),
        "L_pref": L_pref,
        "pole_alpha": 0,
        "MCA_bad_slopes": sorted(set(slopes)),
        "MCA_bad_count": len(set(slopes)),
        "M_pref": M_pref,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ARTIFACT)
    args = parser.parse_args()
    result = {"F7_nonprefix": case_f7(), "F23_multiplicative": case_f23()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("prefix/staircase extremality counterexamples")
    print(
        "F7 list="
        + str(result["F7_nonprefix"]["chosen_word_list_count"])
        + " prefix="
        + str(result["F7_nonprefix"]["L_pref"])
        + " MCA="
        + str(result["F7_nonprefix"]["MCA_bad_count"])
        + "/"
        + str(result["F7_nonprefix"]["M_pref"])
    )
    print(
        "F23 list="
        + str(result["F23_multiplicative"]["exact_list_count"])
        + "/"
        + str(result["F23_multiplicative"]["L_pref"])
        + " MCA="
        + str(result["F23_multiplicative"]["MCA_bad_count"])
        + "/"
        + str(result["F23_multiplicative"]["M_pref"])
    )
    print("PASS_WITH_PREFIX_STAIRCASE_EXTREMALITY_COUNTEREXAMPLES")


if __name__ == "__main__":
    main()
