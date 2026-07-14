#!/usr/bin/env python3
"""Exact checks for universal RS list and MCA incidence envelopes.

Uses only Python's standard library and the companion counterexample verifier.
It verifies:
  1. list incidence-envelope values on the F7 and F23 certificates;
  2. MCA incidence-envelope values on the F7 and F23 certificates;
  3. exact active-row arithmetic showing that the universal envelopes do not
     fit the adjacent challenge budgets.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
import verify_prefix_staircase_extremality_counterexamples as counterexamples


ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "prefix-staircase-extremality"
    / "repaired_incidence_envelopes.json"
)


def list_envelope(n: int, K: int, a: int) -> int:
    return comb(n, K) // comb(a, K)


def mca_envelope(q: int, n: int, k: int, a: int) -> int:
    return min(q, comb(n, k + 1) // (a - k))


def active_list_lower_bound(n: int, a: int, r: int) -> int:
    """Lower bound for floor(C(n,K)/C(a,K)) using its first r factors."""
    return n**r // a**r


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ARTIFACT)
    args = parser.parse_args()

    cert = {
        "F7_nonprefix": counterexamples.case_f7(),
        "F23_multiplicative": counterexamples.case_f23(),
    }

    f7 = cert["F7_nonprefix"]
    f23 = cert["F23_multiplicative"]

    certificate_checks = {
        "F7": {
            "list_count": f7["chosen_word_list_count"],
            "list_incidence_envelope": list_envelope(6, 2, 3),
            "mca_count": f7["MCA_bad_count"],
            "mca_incidence_envelope": mca_envelope(7, 6, 1, 3),
        },
        "F23": {
            "list_count": f23["exact_list_count"],
            "list_incidence_envelope": list_envelope(11, 7, 8),
            "mca_count": f23["MCA_bad_count"],
            "mca_incidence_envelope": mca_envelope(23, 11, 6, 8),
        },
    }
    assert certificate_checks["F7"] == {
        "list_count": 4,
        "list_incidence_envelope": 5,
        "mca_count": 4,
        "mca_incidence_envelope": 7,
    }
    assert certificate_checks["F23"] == {
        "list_count": 11,
        "list_incidence_envelope": 41,
        "mca_count": 11,
        "mca_incidence_envelope": 23,
    }

    n = 2**21
    k = 2**20
    p_kb = 2**31 - 2**24 + 1
    p_m31 = 2**31 - 1
    q_kb = p_kb**6
    q_m31 = p_m31**4
    budget_kb = q_kb // 2**128
    budget_m31 = q_m31 // 2**100
    assert budget_kb == 274980728111395087
    assert budget_m31 == 16777215

    active_list = {
        "KoalaBear_list": {
            "agreement": 1116047,
            "r": 64,
            "certified_envelope_lower_bound": active_list_lower_bound(n, 1116047, 64),
            "budget": budget_kb,
        },
        "Mersenne31_list": {
            "agreement": 1116023,
            "r": 27,
            "certified_envelope_lower_bound": active_list_lower_bound(n, 1116023, 27),
            "budget": budget_m31,
        },
    }
    assert active_list["KoalaBear_list"]["certified_envelope_lower_bound"] == 340906412957980610
    assert active_list["Mersenne31_list"]["certified_envelope_lower_bound"] == 24936335
    for row in active_list.values():
        assert row["certified_envelope_lower_bound"] > row["budget"]

    # Since C(n,k+1)=C(n,k-1) and binomial coefficients increase up to n/2,
    # C(n,k+1) >= C(n,t) for the small t used below.
    active_mca = {
        "KoalaBear_MCA": {
            "agreement": 1116048,
            "a_minus_k": 1116048 - k,
            "small_t": 11,
            "small_binomial_quotient": comb(n, 11) // (1116048 - k),
            "q": q_kb,
            "budget": budget_kb,
        },
        "Mersenne31_MCA": {
            "agreement": 1116024,
            "a_minus_k": 1116024 - k,
            "small_t": 8,
            "small_binomial_quotient": comb(n, 8) // (1116024 - k),
            "q": q_m31,
            "budget": budget_m31,
        },
    }
    assert active_mca["KoalaBear_MCA"]["small_binomial_quotient"] == 1281263064760791573455387992015131136989861512155475723735
    assert active_mca["Mersenne31_MCA"]["small_binomial_quotient"] == 137576378584499828391747397785739544924774
    for row in active_mca.values():
        assert row["small_binomial_quotient"] >= row["q"]
        assert row["q"] > row["budget"]
        row["universal_mca_envelope"] = row["q"]

    output = {
        "certificate_checks": certificate_checks,
        "active_parameters": {
            "n": n,
            "k": k,
            "p_KoalaBear": p_kb,
            "q_KoalaBear": q_kb,
            "budget_KoalaBear": budget_kb,
            "p_Mersenne31": p_m31,
            "q_Mersenne31": q_m31,
            "budget_Mersenne31": budget_m31,
        },
        "active_list": active_list,
        "active_mca": active_mca,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print("universal RS incidence envelopes")
    print(
        "F7 list/MCA="
        + str(certificate_checks["F7"]["list_count"])
        + "/"
        + str(certificate_checks["F7"]["mca_count"])
        + " envelopes="
        + str(certificate_checks["F7"]["list_incidence_envelope"])
        + "/"
        + str(certificate_checks["F7"]["mca_incidence_envelope"])
    )
    print(
        "F23 list/MCA="
        + str(certificate_checks["F23"]["list_count"])
        + "/"
        + str(certificate_checks["F23"]["mca_count"])
        + " envelopes="
        + str(certificate_checks["F23"]["list_incidence_envelope"])
        + "/"
        + str(certificate_checks["F23"]["mca_incidence_envelope"])
    )
    print("PASS_WITH_UNIVERSAL_RS_INCIDENCE_ENVELOPES")


if __name__ == "__main__":
    main()
