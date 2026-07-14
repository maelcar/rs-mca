#!/usr/bin/env python3
"""Close the ell=19, p=2699, D>0 exact-two-sector frontier.

The apparent new difficulty is that the active quotient cofactors g_r,g_s
have degree at most D=m-tau-1, so their ratio need not be constant.  The
load-bearing observation is a sharp common-root dichotomy.

Let z be the number of core labels at which both cofactors vanish.  The
exact local census gives at most three retained points on every other core
coset.  If z<D, losing even one 19-point sector-dead coset pays for all
possible three-root live cosets in the entire D>0 parameter range.  If z=D,
both nonzero cofactors are scalar multiples of their common degree-D locator,
so the common factor cancels on live cosets and the proved D=0 quotient
spectrum* applies legitimately.  This is the only branch in which that
spectrum is transported.

The verifier independently recomputes the complete 153-sector-pair by
142-quotient-state fiber census over F_2699.  It checks the three-root cap,
the exact double/triple state counts, every quotient spectrum, the top-n
envelope for n=13,...,17, and every D>0 parameter cell.  No coefficient
brute force, scalar sampling, or rational-function extrapolation is used.
"""

from __future__ import annotations

import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path


ELL = 19
PRIME = 2699
QUOTIENT_SIZE = (PRIME - 1) // ELL
TAU_MIN = 12
SOURCE_BASELINE = "c35a6da31ed0905afcbaaefe4eb0f242572ebb35"
EXPECTED_STATE_COUNTS = {1: 20637, 2: 1035, 3: 54}
EXPECTED_TOP = {13: 25, 14: 26, 15: 27, 16: 28, 17: 29}

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
ARTIFACT = DATA / "ell19_two_sector_dpositive_vacancy.json"
UPSTREAM = ROOT
UPSTREAM_RESIDUAL = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_RECONSTRUCTION = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_general_reconstruction_collapse.md"
)
UPSTREAM_ELL19 = (
    UPSTREAM / "experimental" / "notes" / "l1" / "l1_ell19_attainment.md"
)
UPSTREAM_DAG = (
    UPSTREAM
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def quotient_state_table(
    generator: int, subgroup: list[int], sector_r: int, sector_s: int
) -> list[int]:
    """Maximum fiber size for h^r+c*h^s, one c per F_p^*/mu_ell state."""

    powers_r = [pow(point, sector_r, PRIME) for point in subgroup]
    powers_s = [pow(point, sector_s, PRIME) for point in subgroup]
    output = []
    for quotient_state in range(QUOTIENT_SIZE):
        coefficient = pow(generator, quotient_state, PRIME)
        values = [
            (first + coefficient * second) % PRIME
            for first, second in zip(powers_r, powers_s)
        ]
        output.append(max(Counter(values).values()))
    return output


def verify_three_root_equation(
    generator: int,
    subgroup: list[int],
    sector_r: int,
    sector_s: int,
    quotient_state: int,
) -> dict[str, int]:
    """Check beta^(s-r)(g_s/g_r)^ell=U/T on a three-fiber state."""

    coefficient = pow(generator, quotient_state, PRIME)
    values = [
        (
            pow(point, sector_r, PRIME)
            + coefficient * pow(point, sector_s, PRIME)
        )
        % PRIME
        for point in subgroup
    ]
    fibers: dict[int, list[int]] = {}
    for index, value in enumerate(values):
        fibers.setdefault(value, []).append(index)
    value, roots = next(
        (value, roots) for value, roots in fibers.items() if len(roots) == 3
    )

    # A+B*h^r+C*h^s has the three selected roots with A=-value, B=1,
    # C=coefficient.  Thus T=(B/A)^ell, U=(C/A)^ell and U/T=C^ell.
    constant = (-value) % PRIME
    assert constant != 0
    invariant_t = pow(pow(constant, -1, PRIME), ELL, PRIME)
    invariant_u = pow(
        coefficient * pow(constant, -1, PRIME) % PRIME,
        ELL,
        PRIME,
    )
    invariant_ratio = invariant_u * pow(invariant_t, -1, PRIME) % PRIME
    assert invariant_ratio == pow(coefficient, ELL, PRIME)

    # On beta_i=(generator^(ell*i)), b_i=generator^i.  The transported
    # coefficient is b_i^(s-r) C, so its ell-th power is exactly the global
    # left-hand side beta_i^(s-r) C^ell.  Test every quotient label.
    difference = sector_s - sector_r
    for label_index in range(QUOTIENT_SIZE):
        beta = pow(generator, ELL * label_index, PRIME)
        transported = pow(
            generator,
            quotient_state + difference * label_index,
            PRIME,
        )
        assert pow(transported, ELL, PRIME) == (
            pow(beta, difference, PRIME) * invariant_ratio
        ) % PRIME

    return {
        "sector_r": sector_r,
        "sector_s": sector_s,
        "quotient_state": quotient_state,
        "representative_fiber_value": value,
        "representative_root_indices": roots,
        "U_over_T": invariant_ratio,
    }


def exact_state_census() -> dict[str, object]:
    generator = primitive_root(PRIME)
    assert generator == 2
    zeta = pow(generator, QUOTIENT_SIZE, PRIME)
    subgroup = [pow(zeta, index, PRIME) for index in range(ELL)]
    assert len(set(subgroup)) == ELL and pow(zeta, ELL, PRIME) == 1

    state_counts: Counter[int] = Counter()
    spectrum_histograms: Counter[tuple[tuple[int, int], ...]] = Counter()
    maximum_top: dict[int, tuple[int, tuple[int, int, int, Counter[int]]]] = {
        live_size: (-1, (0, 0, 0, Counter()))
        for live_size in EXPECTED_TOP
    }
    triple_equation_rows = []
    quotient_tables: dict[tuple[int, int], list[int]] = {}

    for sector_r, sector_s in itertools.combinations(range(1, ELL), 2):
        table = quotient_state_table(
            generator, subgroup, sector_r, sector_s
        )
        quotient_tables[(sector_r, sector_s)] = table
        assert all(1 <= multiplicity <= 3 for multiplicity in table)
        state_counts.update(table)

        for quotient_state, multiplicity in enumerate(table):
            if multiplicity == 3:
                triple_equation_rows.append(
                    verify_three_root_equation(
                        generator,
                        subgroup,
                        sector_r,
                        sector_s,
                        quotient_state,
                    )
                )

        difference = sector_s - sector_r
        for quotient_shift in range(QUOTIENT_SIZE):
            # beta_i=g^(ell*i), b_i=g^i and constant cofactor ratio g^shift:
            # the live coefficient state is shift+(s-r)i modulo 142.
            spectrum = [
                table[(quotient_shift + difference * label_index) % QUOTIENT_SIZE]
                for label_index in range(QUOTIENT_SIZE)
            ]
            histogram = tuple(sorted(Counter(spectrum).items()))
            spectrum_histograms[histogram] += 1
            ordered = sorted(spectrum, reverse=True)
            for live_size in maximum_top:
                top = sum(ordered[:live_size])
                if top > maximum_top[live_size][0]:
                    maximum_top[live_size] = (
                        top,
                        (
                            sector_r,
                            sector_s,
                            quotient_shift,
                            Counter(spectrum),
                        ),
                    )

    assert dict(sorted(state_counts.items())) == EXPECTED_STATE_COUNTS
    assert len(triple_equation_rows) == EXPECTED_STATE_COUNTS[3]
    assert sum(state_counts.values()) == 153 * QUOTIENT_SIZE == 21726
    assert sum(spectrum_histograms.values()) == 21726
    assert len(spectrum_histograms) == 11
    assert {
        live_size: row[0] for live_size, row in maximum_top.items()
    } == EXPECTED_TOP
    assert all(
        maximum_top[live_size][0] == live_size + 12
        for live_size in maximum_top
    )

    return {
        "ell": ELL,
        "p": PRIME,
        "generator": generator,
        "zeta": zeta,
        "quotient_size": QUOTIENT_SIZE,
        "sector_pairs": len(quotient_tables),
        "quotient_states_per_pair": QUOTIENT_SIZE,
        "quotient_reduction_reason": (
            "Every c in F_p^* is generator^q times xi with 0<=q<142 "
            "and xi in mu_19.  Since s-r is invertible modulo 19, choose "
            "u in mu_19 with u^(s-r)=xi^(-1).  Then "
            "f_(c*xi)(u*h)=u^r f_c(h), so fiber multiplicities are "
            "identical.  Thus the 142 representatives exhaust all "
            "nonzero scalar ratios."
        ),
        "state_rows": sum(state_counts.values()),
        "state_multiplicity_counts": {
            str(key): value for key, value in sorted(state_counts.items())
        },
        "triple_equation_checks": len(triple_equation_rows),
        "triple_equation_representatives": triple_equation_rows,
        "spectrum_rows": sum(spectrum_histograms.values()),
        "distinct_spectrum_histograms": len(spectrum_histograms),
        "spectrum_histogram_counts": [
            {
                "histogram": [list(pair) for pair in histogram],
                "rows": count,
            }
            for histogram, count in sorted(spectrum_histograms.items())
        ],
        "maximum_top_by_live_size": {
            str(live_size): {
                "top": row[0],
                "sector_r": row[1][0],
                "sector_s": row[1][1],
                "quotient_shift": row[1][2],
                "histogram": [
                    [multiplicity, count]
                    for multiplicity, count in sorted(row[1][3].items())
                ],
            }
            for live_size, row in maximum_top.items()
        },
    }


def parameter_cells() -> list[dict[str, object]]:
    rows = []
    for tau in range(TAU_MIN, ELL - 2):
        for core_size in range(tau + 2, ELL):
            D = core_size - tau - 1
            assert 1 <= D <= 5 and tau <= 16
            listing_requirement = (D + 2) * ELL

            # Branch I: z<=D-1.  Every dead coset contributes at most ell;
            # every other coset contributes at most three by the exact census.
            nonsaturated_bound = (
                (D - 1) * ELL + 3 * (core_size - (D - 1))
            )
            assert nonsaturated_bound == ELL * D + 3 * tau - 13
            nonsaturated_gap = listing_requirement - nonsaturated_bound
            assert nonsaturated_gap == 51 - 3 * tau > 0

            # Branch II: z=D.  Since both nonzero cofactors have degree <=D,
            # both are scalar multiples of the common degree-D locator.  The
            # D dead labels contribute 19D.  The remaining tau+1 labels have
            # the exact constant-ratio envelope top_(tau+1)=tau+13.
            live_size = tau + 1
            saturated_live_bound = EXPECTED_TOP[live_size]
            saturated_bound = D * ELL + saturated_live_bound
            assert saturated_bound == ELL * D + tau + 13
            saturated_gap = listing_requirement - saturated_bound
            assert saturated_gap == 25 - tau > 0

            rows.append(
                {
                    "tau": tau,
                    "m": core_size,
                    "D": D,
                    "listing_core_requirement": listing_requirement,
                    "z_at_most_D_minus_1": {
                        "retained_core_upper_bound": nonsaturated_bound,
                        "strict_gap": nonsaturated_gap,
                    },
                    "z_equals_D": {
                        "dead_core_contribution": D * ELL,
                        "live_core_labels": live_size,
                        "exact_constant_ratio_live_envelope": saturated_live_bound,
                        "retained_core_upper_bound": saturated_bound,
                        "strict_gap": saturated_gap,
                    },
                    "uniform_retained_core_upper_bound": max(
                        nonsaturated_bound, saturated_bound
                    ),
                    "uniform_strict_gap": min(
                        nonsaturated_gap, saturated_gap
                    ),
                    "vacant": True,
                }
            )

    assert len(rows) == 15
    assert {(row["tau"], row["m"]) for row in rows} == {
        (tau, core_size)
        for tau in range(12, 17)
        for core_size in range(tau + 2, 19)
    }
    assert min(int(row["uniform_strict_gap"]) for row in rows) == 3
    return rows


def check_upstream() -> dict[str, object]:
    baseline_check = subprocess.run(
        [
            "git",
            "-C",
            str(UPSTREAM),
            "merge-base",
            "--is-ancestor",
            SOURCE_BASELINE,
            "HEAD",
        ],
        capture_output=True,
        text=True,
    )
    assert baseline_check.returncode == 0

    residual_text = UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    reconstruction_text = UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    ell19_text = UPSTREAM_ELL19.read_text(encoding="utf-8")
    dag_text = UPSTREAM_DAG.read_text(encoding="utf-8")
    assert "The residual danger is `|S| >= 2`" in residual_text
    assert "explicit BIJECTION" in reconstruction_text
    assert "2699..5701" in ell19_text
    assert "pma_wide_residual" in dag_text

    return {
        "source_baseline": SOURCE_BASELINE,
        "baseline_is_ancestor": True,
        "sources": [
            UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
            UPSTREAM_ELL19.relative_to(ROOT).as_posix(),
            UPSTREAM_DAG.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "The cited sources supply the sector decomposition, the "
            "sector-dead degree budget, the full-petal/minimal-kernel "
            "bijection, and unrelated general ell=19 spectrum work.  They "
            "leave the exact-two-sector p=2699 D>0 closure and the "
            "|S|>=2 pma_wide_residual open."
        ),
    }


def main() -> None:
    state_census = exact_state_census()
    cells = parameter_cells()
    upstream = check_upstream()

    artifact = {
        "title": "ell=19 p=2699 D-positive exact-two-sector vacancy",
        "status": "VACANCY_THEOREM",
        "verdict": "PASS_WITH_ELL19_FULL_EXCEPTIONAL_FRONTIER_VACANCY",
        "theorem": (
            "Over F_2699 with ell=19, every background-free full-petal "
            "word with exactly two active nonzero DFT sectors is unlisted "
            "throughout 12<=tau<m<19 and D=m-tau-1>0.  Together with "
            "the D=0 theorem, the entire p=2699 exceptional "
            "frontier is vacant."
        ),
        "scope": (
            "Prime field F_2699, ell=19, background-free full petals, "
            "exactly two active nonzero DFT sectors, and the "
            "exceptional parameter range.  This is not whole-cell vacancy "
            "for words with three or more active sectors and not an "
            "extension-field theorem."
        ),
        "normal_form": {
            "word": (
                "P(X)=P0(X^19)+phi(X^19)(X^r g_r(X^19)+"
                "X^s g_s(X^19))"
            ),
            "cofactor_degrees": "deg(g_r),deg(g_s)<=D=m-tau-1",
            "common_dead_labels": (
                "z=#{beta in core: g_r(beta)=g_s(beta)=0}<=D"
            ),
            "three_root_equation": (
                "beta^(s-r)(g_s(beta)/g_r(beta))^19=U/T"
            ),
            "listing_core_requirement": "R_core>=(D+2)*19",
        },
        "saturated_dead_coset_dichotomy_lemma": {
            "statement": (
                "Let two nonzero quotient cofactors have degree <=D, let "
                "z be their number of distinct common core-label roots, "
                "and suppose every nondead core coset has retained cap c. "
                "For m=tau+1+D: if z<=D-1 then "
                "R_core<=(D-1)ell+c(tau+2); if z=D then both cofactors "
                "are scalar multiples of the common degree-D locator and "
                "R_core<=D*ell+S_(tau+1), where S_n is the exact "
                "constant-ratio top-n spectrum envelope."
            ),
            "specialization": (
                "Here ell=19, c=3 and S_n=n+12.  The first branch has "
                "gap 51-3tau>=3; the saturated branch has gap "
                "25-tau>=9."
            ),
            "novelty_guard": (
                "The dead-coset budget itself is upstream machinery.  "
                "The contribution here is the equality-frontier split and "
                "its exact F_2699 application, not a claim of new generic "
                "sector-dead machinery."
            ),
        },
        "proof": {
            "branch_z_less_than_D": (
                "If z<=D-1, the exact local cap three gives "
                "R_core<=19z+3(m-z)<=19D+3tau-13.  Since D>0 and m<19 "
                "force tau<=16, the listing gap is at least "
                "51-3tau>=3.  Thus no rational-incidence estimate is "
                "needed in the genuinely nonconstant branch."
            ),
            "branch_z_equals_D": (
                "If z=D, the nonzero degree-<=D cofactors share D distinct "
                "roots, hence g_r=c_r Q and g_s=c_s Q.  On live labels Q "
                "is nonzero and cancels from fiber multiplicities, so the "
                "constant-ratio quotient census applies.  Its exact top-n "
                "envelope is n+12 for n=tau+1=13,...,17.  Therefore "
                "R_core<=19D+tau+13, with listing gap 25-tau>=9."
            ),
            "logical_guard": (
                "The D=0 spectrum is used only after z=D algebraically "
                "forces the reduced ratio to be constant.  It is never "
                "transported into the z<D rational-function branch."
            ),
            "interpolation_and_minimality": (
                "The fiber census maximizes independently over the sector-"
                "zero value A=P0(beta)/phi(beta) on every live label and "
                "the top-n step maximizes over every choice of core labels. "
                "It is therefore an upper envelope before imposing P0 "
                "interpolation, distinct/nonzero petal scalars, exact "
                "degree, minimality, or primitivity.  Those constraints can "
                "only remove candidates; strict unlistedness makes their "
                "individual feasibility moot."
            ),
        },
        "exact_double_triple_state_census": state_census,
        "parameter_cells": cells,
        "uniform_minimum_listing_gap": min(
            int(row["uniform_strict_gap"]) for row in cells
        ),
        "operation_counts": {
            "quotient_fiber_state_rows": state_census["state_rows"],
            "quotient_spectrum_rows": state_census["spectrum_rows"],
            "three_root_equation_checks": state_census[
                "triple_equation_checks"
            ],
            "parameter_cells": len(cells),
            "blind_coefficient_pairs_enumerated": 0,
        },
        "upstream": upstream,
        "scientific_consequence": (
            "The D=0 and D-positive arguments close the complete exact-two-active-sector "
            "frontier over F_2699.  The propagation theorem separately shows the "
            "F_1361 frontier is nonvacant.  The arithmetic dichotomy is "
            "therefore genuinely prime-dependent."
        ),
        "next_obligation": (
            "Return to the broader prime-ell pma_wide_residual: three or "
            "more active DFT sectors, extension fields, or an asymptotic "
            "version of the common-root deficit principle.  No p=2699 "
            "exact-two-sector cell remains open."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("ell=19 D-positive exact-two-sector vacancy")
    print(
        "state_rows="
        + str(state_census["state_rows"])
        + " multiplicities="
        + str(state_census["state_multiplicity_counts"])
    )
    print(
        "top_live="
        + str(
            [
                state_census["maximum_top_by_live_size"][str(size)]["top"]
                for size in range(13, 18)
            ]
        )
        + " cells="
        + str(len(cells))
    )
    print(
        "branch_gaps="
        + str(
            sorted(
                {
                    int(row["z_at_most_D_minus_1"]["strict_gap"])
                    for row in cells
                }
            )
        )
        + "/"
        + str(
            sorted(
                {
                    int(row["z_equals_D"]["strict_gap"])
                    for row in cells
                }
            )
        )
    )
    print("PASS_WITH_ELL19_FULL_EXCEPTIONAL_FRONTIER_VACANCY")


if __name__ == "__main__":
    main()
