#!/usr/bin/env python3
"""Exact sector-dead propagation of the ell=17 two-sector witnesses.

For each of the five D=0 bases and every in-range D>0, choose D new
core labels with locator Q(Y), and multiply both the codeword and core locator
by Q(X^17).  This preserves the petal scalars and exact missed core while the
new core cosets are retained completely.  The verifier checks all ten new
cells point by point and retains the five bases as anchors.
"""

from __future__ import annotations

import json
from pathlib import Path

from verify_l1_exceptional_two_sector_d0 import (
    build_ell17_witnesses,
    locator,
    polynomial_evaluate,
    polynomial_full_evaluate,
    polynomial_multiply,
)


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-exact-two-sector"
ARTIFACT = DATA / "ell17_two_sector_propagation.json"
UPSTREAM_RECONSTRUCTION = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_general_reconstruction_collapse.md"
)
UPSTREAM_RESIDUAL = (
    ROOT
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)


def padded_evaluate(
    point: int,
    ell: int,
    prime: int,
    p0_padded: list[int],
    phi: list[int],
    q_locator: list[int],
    active_coefficient: int,
) -> int:
    label = pow(point, ell, prime)
    return (
        polynomial_evaluate(p0_padded, label, prime)
        + polynomial_evaluate(phi, label, prime)
        * polynomial_evaluate(q_locator, label, prime)
        * (point + active_coefficient * pow(point, 11, prime))
    ) % prime


def main() -> None:
    base_family = build_ell17_witnesses()
    ell = base_family["ell"]
    prime = base_family["p"]
    generator = base_family["generator"]
    zeta = base_family["zeta"]
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    quotient_size = base_family["quotient_size"]
    active_coefficient = base_family["active_coefficient_for_sector_s"]
    assert (ell, prime, generator, active_coefficient) == (17, 1361, 3, 81)

    reconstruction_text = UPSTREAM_RECONSTRUCTION.read_text(encoding="utf-8")
    residual_text = UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    assert "explicit BIJECTION" in reconstruction_text
    assert "The residual danger is `|S| >= 2`" in residual_text

    cells = []
    new_cell_count = 0
    point_evaluations = 0
    for base in base_family["cells"]:
        tau = base["tau"]
        base_m = base["m"]
        assert base_m == tau + 1
        phi = base["phi_coefficients_ascending"]
        p0 = base["P0_coefficients_ascending"]
        base_core_locator = base["Lambda_coefficients_ascending"]
        scalars = base["petal_scalars"]
        live_core_indices = base["core_quotient_indices"]
        petal_indices = base["petal_quotient_indices"]
        used = set(live_core_indices + petal_indices)
        available = [index for index in range(quotient_size) if index not in used]

        # Reconstruct the exact base missed core once.  It is the object that
        # the multiplicative propagation must preserve literally.
        base_missed = set()
        for index in live_core_indices:
            representative = pow(generator, index, prime)
            for point in subgroup:
                x = representative * point % prime
                if (
                    polynomial_full_evaluate(
                        x,
                        ell,
                        prime,
                        p0,
                        phi,
                        active_coefficient,
                    )
                    != 0
                ):
                    base_missed.add(x)
        assert len(base_missed) == base["exact_missed_core_size"]

        for target_m in range(base_m, ell):
            D = target_m - base_m
            dead_indices = available[:D]
            dead_labels = [
                pow(generator, ell * index, prime) for index in dead_indices
            ]
            q_locator = locator(dead_labels, prime)
            padded_core_locator = polynomial_multiply(
                base_core_locator, q_locator, prime
            )
            p0_padded = polynomial_multiply(p0, q_locator, prime)
            assert len(q_locator) == D + 1
            assert len(padded_core_locator) == target_m + 1
            assert len(p0_padded) == target_m + 1

            # Exact algebraic identities behind the lift.
            assert all(
                polynomial_evaluate(q_locator, label, prime) == 0
                for label in dead_labels
            )
            petal_labels = [
                pow(generator, ell * index, prime) for index in petal_indices
            ]
            propagated_scalars = []
            for label in petal_labels:
                numerator = polynomial_evaluate(p0_padded, label, prime)
                denominator = polynomial_evaluate(
                    padded_core_locator, label, prime
                )
                propagated_scalars.append(
                    numerator * pow(denominator, -1, prime) % prime
                )
            assert propagated_scalars == scalars
            assert all(scalars) and len(set(scalars)) == tau

            petal_agreements = []
            for index, scalar in zip(petal_indices, scalars):
                representative = pow(generator, index, prime)
                agreement = 0
                for point in subgroup:
                    x = representative * point % prime
                    label = pow(x, ell, prime)
                    received = (
                        scalar
                        * polynomial_evaluate(padded_core_locator, label, prime)
                    ) % prime
                    value = padded_evaluate(
                        x,
                        ell,
                        prime,
                        p0_padded,
                        phi,
                        q_locator,
                        active_coefficient,
                    )
                    base_value = polynomial_full_evaluate(
                        x,
                        ell,
                        prime,
                        p0,
                        phi,
                        active_coefficient,
                    )
                    assert value == (
                        polynomial_evaluate(q_locator, label, prime) * base_value
                    ) % prime
                    agreement += value == received
                    point_evaluations += 1
                petal_agreements.append(agreement)
            assert petal_agreements == [ell] * tau

            core_profile = []
            padded_missed = set()
            for index in live_core_indices + dead_indices:
                representative = pow(generator, index, prime)
                zeros = 0
                for point in subgroup:
                    x = representative * point % prime
                    value = padded_evaluate(
                        x,
                        ell,
                        prime,
                        p0_padded,
                        phi,
                        q_locator,
                        active_coefficient,
                    )
                    zeros += value == 0
                    if value != 0:
                        padded_missed.add(x)
                    point_evaluations += 1
                core_profile.append(zeros)
            assert core_profile == base["core_zero_profile"] + [ell] * D
            assert padded_missed == base_missed

            retained_core = base["retained_core"] + D * ell
            total_agreement = tau * ell + retained_core
            listing_threshold = (target_m + 1) * ell
            assert total_agreement >= listing_threshold
            missed_size = len(padded_missed)
            assert ell <= missed_size <= (tau - 1) * ell

            degree_p0 = max(
                degree * ell
                for degree, coefficient in enumerate(p0_padded)
                if coefficient
            )
            degree_sector_1 = (tau + D) * ell + 1
            degree_sector_11 = (tau + D) * ell + 11
            degree = max(degree_p0, degree_sector_1, degree_sector_11)
            assert degree == target_m * ell

            stabilizer = []
            for multiplier in subgroup:
                if {
                    multiplier * point % prime for point in padded_missed
                } == padded_missed:
                    stabilizer.append(multiplier)
            assert stabilizer == [1]

            # The active quotient cofactors are exactly Q and 81Q.  They are
            # nonzero of degree D=m-tau-1, and no third nonzero sector appears.
            active_g1 = q_locator
            active_g11 = [
                active_coefficient * coefficient % prime
                for coefficient in q_locator
            ]
            assert active_g1[-1] == 1 and active_g11[-1] == active_coefficient

            if D:
                new_cell_count += 1
            cells.append(
                {
                    "tau": tau,
                    "m": target_m,
                    "D": D,
                    "base_m": base_m,
                    "live_core_quotient_indices": live_core_indices,
                    "dead_core_quotient_indices": dead_indices,
                    "petal_quotient_indices": petal_indices,
                    "Q_coefficients_ascending": q_locator,
                    "Lambda_padded_coefficients_ascending": padded_core_locator,
                    "P0_padded_coefficients_ascending": p0_padded,
                    "g1_coefficients_ascending": active_g1,
                    "g11_coefficients_ascending": active_g11,
                    "petal_scalars": scalars,
                    "core_zero_profile_live_then_dead": core_profile,
                    "retained_core": retained_core,
                    "total_agreement": total_agreement,
                    "listing_threshold": listing_threshold,
                    "listing_surplus": total_agreement - listing_threshold,
                    "degree": degree,
                    "degree_bound": target_m * ell,
                    "exact_missed_core_size": missed_size,
                    "missed_core_identical_to_D0_base": True,
                    "active_nonzero_DFT_sectors": [1, 11],
                    "full_DFT_support_including_sector_zero": [0, 1, 11],
                    "H_stabilizer_of_exact_missed_core": stabilizer,
                    "listed": True,
                    "primitive": True,
                    "minimality": (
                        "The padded word is full-petal and listed with the "
                        "same distinct nonzero scalars, and its exact missed "
                        "core remains in [ell,(tau-1)ell].  The upstream "
                        "bijection therefore makes that exact missed core a "
                        "divisibility-minimal kernel set."
                    ),
                }
            )

    assert len(cells) == 15
    assert new_cell_count == 10
    assert {(cell["tau"], cell["m"]) for cell in cells} == {
        (tau, m) for tau in range(11, 16) for m in range(tau + 1, 17)
    }

    # Negative control: multiplying only the active cofactors cannot make the
    # proposed tau=11 dead labels fully retained, because the unpadded P0 is
    # nonzero there.  Q must multiply P0 and Lambda as well.
    tau11_base = base_family["cells"][0]
    tau11_used = set(
        tau11_base["core_quotient_indices"]
        + tau11_base["petal_quotient_indices"]
    )
    tau11_dead = [
        index for index in range(quotient_size) if index not in tau11_used
    ][:4]
    assert tau11_dead == [14, 16, 17, 19]
    unpadded_p0_values = [
        polynomial_evaluate(
            tau11_base["P0_coefficients_ascending"],
            pow(generator, ell * index, prime),
            prime,
        )
        for index in tau11_dead
    ]
    assert unpadded_p0_values == [893, 623, 944, 1111]
    assert all(unpadded_p0_values)

    artifact = {
        "title": "Exact sector-dead propagation of the ell=17 witnesses",
        "status": "COUNTEREXAMPLE_FAMILY",
        "verdict": "PASS_WITH_ELL17_FULL_EXCEPTIONAL_PARAMETER_GRID_COUNTEREXAMPLES",
        "theorem": (
            "Over F_1361 with ell=17, every parameter pair "
            "11<=tau<m<17 admits an explicit background-free full-petal "
            "listed word with exactly active nonzero DFT sectors {1,11}; "
            "its exact missed core is a primitive divisibility-minimal "
            "kernel set."
        ),
        "scope": (
            "This propagates the five D=0 bases through common "
            "sector-dead padding.  It proves existence for one fixed sector "
            "pair, not classification or vacancy of every exceptional "
            "exponent ratio, and makes no ell=19 D>0 statement."
        ),
        "propagation_identity": {
            "Y": "X^17",
            "Q_D": "product over D new core labels (Y-delta)",
            "Lambda_D": "Lambda_0*Q_D",
            "P_D": "Q_D(X^17)*P_0_base(X)",
            "P0_D": "P0_base*Q_D",
            "g1_D": "Q_D",
            "g11_D": "81*Q_D",
            "petal_scalar_cancellation": (
                "P0_D(alpha)/Lambda_D(alpha)="
                "P0_base(alpha)/Lambda_0(alpha)"
            ),
        },
        "cells": cells,
        "cell_counts": {
            "total_parameter_pairs": len(cells),
            "D0_anchors": len(cells) - new_cell_count,
            "new_D_positive_counterexamples": new_cell_count,
        },
        "negative_control": {
            "failure_mode": (
                "Multiplying g1,g11 by Q while leaving P0 unchanged does not "
                "retain the new core cosets."
            ),
            "tau11_dead_indices": tau11_dead,
            "unpadded_P0_values_on_dead_labels": unpadded_p0_values,
        },
        "operation_counts": {
            "point_evaluations": point_evaluations,
            "coefficient_pair_enumerations_per_coset": 0,
            "new_cells_checked": new_cell_count,
        },
        "upstream": {
            "reconstruction_source": UPSTREAM_RECONSTRUCTION.relative_to(ROOT).as_posix(),
            "residual_source": UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            "collision": (
                "Upstream already supplies the full-petal minimality "
                "bijection and sector-dead budget, but contains no p=1361 "
                "exact-two-sector witness to propagate.  The propagation is an exact "
                "corollary of the D=0 bases, not a claimed new generic "
                "padding lemma."
            ),
        },
        "next_obligation": (
            "The p=1361 exceptional parameter grid is now nonvacant in every row. "
            "Remaining exact-two-sector work concerns classification/counting "
            "of other ratios and the p=2699 D>0 frontier, not existence in "
            "the p=1361 rows."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    new_cells = [cell for cell in cells if cell["D"] > 0]
    print("ell=17 exact two-sector propagation")
    print(
        "cells_total="
        + str(len(cells))
        + " new_D_positive="
        + str(len(new_cells))
    )
    print(
        "new_agreements="
        + str([cell["total_agreement"] for cell in new_cells])
    )
    print(
        "point_evaluations="
        + str(point_evaluations)
        + " negative_control="
        + str(unpadded_p0_values)
    )
    print("PASS_WITH_ELL17_FULL_EXCEPTIONAL_PARAMETER_GRID_COUNTEREXAMPLES")


if __name__ == "__main__":
    main()
