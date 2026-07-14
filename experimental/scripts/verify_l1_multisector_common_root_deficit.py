#!/usr/bin/env python3
"""Theorem-scale common-root deficit compiler for active sectors.

This verifier accompanies an elementary theorem, not a finite theorem proof.
It checks the symbolic inequalities over a broad integer grid and audits the
algebra on deterministic finite-field configurations with two, three, and
four active sectors, including D=0, saturated common roots, lower-degree
cofactors, and labels on which only some sectors vanish.

The compiler takes two independently proved inputs:

* c: a robust live-coset fiber cap, valid for every nonzero coefficient
  specialization that may occur after some sectors vanish at a label;
* S_h: the top-h proportional-spectrum envelope when all cofactors are
  scalar multiples of one common locator.

It does not assert a Fourier/uncertainty value for c in finite
characteristic.  Its conclusion is conditional on those inputs.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "experimental" / "data" / "certificates" / "l1-multisector-onsets"
ARTIFACT = DATA / "multisector_common_root_deficit.json"
UPSTREAM = ROOT
UPSTREAM_RESIDUAL = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_coset_mixed_vacancy_threshold.md"
)
UPSTREAM_PROGRAM = (
    UPSTREAM
    / "experimental"
    / "notes"
    / "l1"
    / "l1_full_list_quotient_proof_program.md"
)
UPSTREAM_DAG = (
    UPSTREAM
    / "experimental"
    / "data"
    / "prize-dag"
    / "prize_dag.json"
)


def compiler_bounds(
    ell: int, tau: int, D: int, live_cap: int, proportional_top: int
) -> dict[str, int]:
    assert ell >= 2 and tau >= 0 and D >= 0
    assert 0 <= live_cap <= ell
    assert 0 <= proportional_top <= (tau + 1) * ell
    listing = (D + 2) * ell
    nonsaturated = (D - 1) * ell + live_cap * (tau + 2)
    saturated = D * ell + proportional_top
    return {
        "listing": listing,
        "nonsaturated": nonsaturated,
        "saturated": saturated,
        "compiler": max(nonsaturated, saturated),
        "surplus_bound": max(
            live_cap * (tau + 2) - 3 * ell,
            proportional_top - 2 * ell,
        ),
    }


def symbolic_grid_audit() -> dict[str, int]:
    rows = 0
    branch_rows = 0
    hierarchy_rows = 0
    d0_rows = 0
    for ell in range(2, 48):
        for tau in range(0, ell + 3):
            for D in range(0, 7):
                core_size = tau + 1 + D
                for live_cap in range(0, ell + 1):
                    for proportional_top in {
                        0,
                        min((tau + 1) * ell, live_cap * (tau + 1)),
                        (tau + 1) * ell,
                    }:
                        bounds = compiler_bounds(
                            ell, tau, D, live_cap, proportional_top
                        )
                        assert bounds["compiler"] - bounds["listing"] == (
                            bounds["surplus_bound"]
                        )
                        rows += 1

                        if D == 0:
                            # The z<=D-1 branch is empty.  The exact compiler
                            # is the proportional branch; the displayed max
                            # remains a safe, possibly weaker, unified bound.
                            assert D * ell + proportional_top == proportional_top
                            d0_rows += 1
                            continue

                        for z in range(D + 1):
                            if z < D:
                                raw = z * ell + live_cap * (core_size - z)
                                assert raw <= bounds["nonsaturated"]
                            else:
                                raw = D * ell + proportional_top
                                assert raw == bounds["saturated"]
                            assert raw <= bounds["compiler"]
                            branch_rows += 1

                        # Full deficit hierarchy: q=D-z>=1.
                        for deficit in range(1, D + 1):
                            z = D - deficit
                            raw = z * ell + live_cap * (core_size - z)
                            hierarchy = (
                                (D - deficit) * ell
                                + live_cap * (tau + 1 + deficit)
                            )
                            assert raw == hierarchy
                            assert hierarchy - bounds["listing"] == (
                                live_cap * (tau + 1 + deficit)
                                - (deficit + 2) * ell
                            )
                            hierarchy_rows += 1

    return {
        "compiler_grid_rows": rows,
        "branch_checks": branch_rows,
        "deficit_hierarchy_checks": hierarchy_rows,
        "D0_boundary_rows": d0_rows,
    }


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


def polynomial_multiply(
    first: list[int], second: list[int], prime: int
) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] = (
                output[first_index + second_index]
                + first_value * second_value
            ) % prime
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return output


def polynomial_evaluate(polynomial: list[int], point: int, prime: int) -> int:
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % prime
    return value


def locator(labels: list[int], prime: int) -> list[int]:
    output = [1]
    for label in labels:
        output = polynomial_multiply(output, [(-label) % prime, 1], prime)
    return output


def scalar_multiply(
    polynomial: list[int], scalar: int, prime: int
) -> list[int]:
    return [scalar * coefficient % prime for coefficient in polynomial]


def fiber_size(
    subgroup: list[int], sectors: tuple[int, ...], coefficients: list[int], prime: int
) -> int:
    assert any(coefficients)
    values = []
    for point in subgroup:
        values.append(
            sum(
                coefficient * pow(point, sector, prime)
                for sector, coefficient in zip(sectors, coefficients)
            )
            % prime
        )
    return max(Counter(values).values())


def field_geometry(ell: int, prime: int) -> dict[str, object]:
    assert (prime - 1) % ell == 0
    generator = primitive_root(prime)
    quotient_size = (prime - 1) // ell
    zeta = pow(generator, quotient_size, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ell)]
    labels = [pow(generator, ell * index, prime) for index in range(quotient_size)]
    assert len(set(subgroup)) == ell
    assert len(set(labels)) == quotient_size
    return {
        "ell": ell,
        "prime": prime,
        "generator": generator,
        "quotient_size": quotient_size,
        "subgroup": subgroup,
        "labels": labels,
    }


def proportional_spectrum(
    geometry: dict[str, object], sectors: tuple[int, ...], constants: list[int]
) -> list[int]:
    prime = int(geometry["prime"])
    generator = int(geometry["generator"])
    subgroup = list(geometry["subgroup"])
    quotient_size = int(geometry["quotient_size"])
    spectrum = []
    for label_index in range(quotient_size):
        representative = pow(generator, label_index, prime)
        coefficients = [
            constant * pow(representative, sector, prime) % prime
            for sector, constant in zip(sectors, constants)
        ]
        spectrum.append(fiber_size(subgroup, sectors, coefficients, prime))
    return spectrum


def evaluate_configuration(
    name: str,
    geometry: dict[str, object],
    sectors: tuple[int, ...],
    tau: int,
    D: int,
    cofactors: list[list[int]],
    core_indices: list[int],
    proportional_constants: list[int] | None = None,
) -> dict[str, object]:
    ell = int(geometry["ell"])
    prime = int(geometry["prime"])
    generator = int(geometry["generator"])
    subgroup = list(geometry["subgroup"])
    labels = list(geometry["labels"])
    core_size = tau + 1 + D
    assert len(sectors) == len(cofactors) >= 2
    assert len(core_indices) == core_size == len(set(core_indices))
    assert all(0 <= index < len(labels) for index in core_indices)
    assert all(0 <= len(polynomial) - 1 <= D for polynomial in cofactors)
    assert all(any(polynomial) for polynomial in cofactors)

    all_label_multiplicities = []
    core_multiplicities = []
    common_core_indices = []
    partial_death_labels = 0
    for label_index, beta in enumerate(labels):
        values = [
            polynomial_evaluate(polynomial, beta, prime)
            for polynomial in cofactors
        ]
        zero_count = sum(value == 0 for value in values)
        if zero_count == len(values):
            multiplicity = ell
        else:
            if zero_count:
                partial_death_labels += 1
            representative = pow(generator, label_index, prime)
            coefficients = [
                value * pow(representative, sector, prime) % prime
                for sector, value in zip(sectors, values)
            ]
            multiplicity = fiber_size(
                subgroup, sectors, coefficients, prime
            )
            all_label_multiplicities.append(multiplicity)

        if label_index in core_indices:
            core_multiplicities.append(multiplicity)
            if zero_count == len(values):
                common_core_indices.append(label_index)

    z = len(common_core_indices)
    assert z <= D
    live_cap = max(all_label_multiplicities, default=0)
    retained_core = sum(core_multiplicities)

    if z == D:
        assert proportional_constants is not None
        common_locator = locator(
            [labels[index] for index in common_core_indices], prime
        )
        assert len(common_locator) == D + 1
        for polynomial, constant in zip(cofactors, proportional_constants):
            assert polynomial == scalar_multiply(
                common_locator, constant, prime
            )
        spectrum = proportional_spectrum(
            geometry, sectors, proportional_constants
        )
        live_size = tau + 1
        proportional_top = sum(sorted(spectrum, reverse=True)[:live_size])
    else:
        assert proportional_constants is None
        # An arbitrary safe value is enough because the saturated branch is
        # not the realized one.  Use the tautological proportional envelope.
        proportional_top = (tau + 1) * ell
        spectrum = None

    bounds = compiler_bounds(ell, tau, D, live_cap, proportional_top)
    if D == 0:
        assert z == 0 and retained_core <= bounds["saturated"]
    elif z < D:
        assert retained_core <= bounds["nonsaturated"]
    else:
        assert retained_core <= bounds["saturated"]
    assert retained_core <= bounds["compiler"]

    return {
        "name": name,
        "ell": ell,
        "p": prime,
        "active_sectors": list(sectors),
        "active_sector_count": len(sectors),
        "tau": tau,
        "m": core_size,
        "D": D,
        "cofactor_degrees": [len(polynomial) - 1 for polynomial in cofactors],
        "common_dead_core_labels_z": z,
        "partial_sector_death_labels_in_full_quotient": partial_death_labels,
        "robust_observed_live_cap": live_cap,
        "retained_core_envelope": retained_core,
        "proportional_top": proportional_top,
        "proportional_spectrum": spectrum,
        "bounds": bounds,
        "branch": "z_equals_D" if z == D else "z_less_than_D",
        "pass": True,
    }


def finite_field_audit() -> dict[str, object]:
    geometry = field_geometry(7, 127)
    labels = list(geometry["labels"])
    prime = int(geometry["prime"])
    rows = []

    # D=0: every nonzero cofactor is constant, so the proportional branch is
    # exact.  Include the first three-active-sector cell tau=5,m=6,ell=7.
    for sector_count in (2, 3, 4):
        sectors = tuple(range(1, sector_count + 1))
        constants = [index + 2 for index in range(sector_count)]
        rows.append(
            evaluate_configuration(
                f"D0_T{sector_count}",
                geometry,
                sectors,
                tau=5,
                D=0,
                cofactors=[[constant] for constant in constants],
                core_indices=list(range(6)),
                proportional_constants=constants,
            )
        )

    # Saturated z=D for T=2,3,4 and D=1,2.  Every cofactor is a scalar
    # multiple of the same locator, exactly as the theorem forces.
    for D, tau in ((1, 4), (2, 3)):
        common_indices = list(range(D))
        common_locator = locator(
            [labels[index] for index in common_indices], prime
        )
        for sector_count in (2, 3, 4):
            sectors = tuple(range(1, sector_count + 1))
            constants = [index + 3 for index in range(sector_count)]
            cofactors = [
                scalar_multiply(common_locator, constant, prime)
                for constant in constants
            ]
            rows.append(
                evaluate_configuration(
                    f"saturated_D{D}_T{sector_count}",
                    geometry,
                    sectors,
                    tau=tau,
                    D=D,
                    cofactors=cofactors,
                    core_indices=list(range(6)),
                    proportional_constants=constants,
                )
            )

    # z=D-1 with different remaining roots: this realizes the boundary of
    # the nonsaturated branch and creates labels where only one sector dies.
    for D, tau in ((1, 4), (2, 3)):
        common_indices = list(range(max(0, D - 1)))
        common_locator = locator(
            [labels[index] for index in common_indices], prime
        )
        sectors = (1, 2, 3)
        cofactors = []
        for offset in range(len(sectors)):
            extra = [(-labels[D + offset]) % prime, 1]
            cofactors.append(
                polynomial_multiply(common_locator, extra, prime)
            )
        rows.append(
            evaluate_configuration(
                f"nonsaturated_boundary_D{D}_T3",
                geometry,
                sectors,
                tau=tau,
                D=D,
                cofactors=cofactors,
                core_indices=list(range(6)),
            )
        )

    # Lower-degree guard: one constant cofactor forces z=0<D even though the
    # other sectors have degree D.  It also has partial sector deaths.
    sectors = (1, 2, 3, 4)
    degree_two = [
        locator([labels[1], labels[2]], prime),
        locator([labels[2], labels[3]], prime),
        locator([labels[3], labels[4]], prime),
    ]
    rows.append(
        evaluate_configuration(
            "lower_degree_and_partial_death_D2_T4",
            geometry,
            sectors,
            tau=3,
            D=2,
            cofactors=[[1], *degree_two],
            core_indices=list(range(6)),
        )
    )

    assert len(rows) == 12
    assert {row["active_sector_count"] for row in rows} == {2, 3, 4}
    assert {row["D"] for row in rows} == {0, 1, 2}
    assert any(row["partial_sector_death_labels_in_full_quotient"] for row in rows)
    assert any(0 in row["cofactor_degrees"] and row["D"] > 0 for row in rows)
    return {
        "field": "F_127",
        "ell": 7,
        "quotient_labels": geometry["quotient_size"],
        "configurations": rows,
        "configuration_count": len(rows),
    }


def check_upstream() -> dict[str, object]:
    residual_text = UPSTREAM_RESIDUAL.read_text(encoding="utf-8")
    program_text = UPSTREAM_PROGRAM.read_text(encoding="utf-8")
    dag_text = UPSTREAM_DAG.read_text(encoding="utf-8")
    assert "dead cosets `<= m-t-1`" in residual_text
    assert "The residual danger is `|S| >= 2`" in residual_text
    assert "cofactor" in program_text
    assert "pma_wide_residual" in dag_text

    return {
        "sources": [
            UPSTREAM_RESIDUAL.relative_to(ROOT).as_posix(),
            UPSTREAM_PROGRAM.relative_to(ROOT).as_posix(),
            UPSTREAM_DAG.relative_to(ROOT).as_posix(),
        ],
        "collision": (
            "Upstream contains the underlying sector-dead degree budget "
            "and general cofactor machinery, but no equality-frontier "
            "compiler that isolates z=D, forces simultaneous "
            "proportionality, and substitutes a proportional-spectrum "
            "top envelope. This certificate packages that deduction; it "
            "does not claim the upstream dead-coset budget as new."
        ),
    }


def main() -> None:
    symbolic = symbolic_grid_audit()
    finite = finite_field_audit()
    upstream = check_upstream()
    artifact = {
        "title": "Common-root deficit compiler for active DFT sectors",
        "status": "THEOREM_COMPILER",
        "verdict": "PASS_WITH_COMMON_ROOT_DEFICIT_COMPILER",
        "theorem": {
            "setting": (
                "For a background-free full-petal word with T>=2 active "
                "nonzero DFT sectors A, write their nonzero quotient "
                "cofactors g_a with deg(g_a)<=D=m-tau-1.  Let z be the "
                "number of distinct core labels common to every zero set."
            ),
            "inputs": (
                "Let c<=ell bound every live-coset fiber for every nonzero "
                "coefficient specialization that can occur, including "
                "proper support subsets.  Let S_h bound the sum of the h "
                "largest fibers in the proportional family g_a=c_a Q."
            ),
            "bound": (
                "For D>=1, R_core<=max((D-1)ell+c(tau+2), "
                "D ell+S_(tau+1)).  Equivalently the listing surplus is "
                "at most max(c(tau+2)-3ell, S_(tau+1)-2ell)."
            ),
            "D0_boundary": (
                "For D=0 all nonzero cofactors are constants, z=0, and "
                "the exact bound is R_core<=S_(tau+1).  The unified max "
                "formula remains safe but need not be sharp."
            ),
            "deficit_hierarchy": (
                "More exactly, if q=D-z>=1 then "
                "R_core<=(D-q)ell+c(tau+1+q), whose listing surplus is "
                "at most c(tau+1+q)-(q+2)ell."
            ),
        },
        "proof": [
            "Every common-dead core label is a root of every nonzero g_a, hence z<=min_a deg(g_a)<=D.",
            "A dead coset retains at most ell points. On a live coset the sector-zero value merely chooses a fiber of the nonzero active-sector function, so retained points are at most c.",
            "For fixed z, R_core<=z ell+c(m-z). Since c<=ell this increases with z. If z<=D-1, substitute z=D-1 and m=tau+1+D.",
            "If z=D, the locator Q of those D distinct labels divides every nonzero degree-<=D cofactor. Therefore every g_a=c_a Q simultaneously, with c_a nonzero. On nondead labels Q(beta) is a common nonzero scalar and does not change fiber multiplicities, leaving tau+1 live labels controlled by S_(tau+1).",
            "Subtract the core listing target (D+2)ell to obtain the surplus compiler and the two strict vacancy criteria.",
        ],
        "vacancy_criteria": {
            "D_positive": [
                "c(tau+2)<3ell",
                "S_(tau+1)<2ell",
            ],
            "D_zero": ["S_(tau+1)<2ell"],
            "strictness_guard": (
                "Listing permits equality, so both relevant inequalities "
                "must be strict."
            ),
        },
        "multisector_scope": {
            "algebraic_extension": (
                "The compiler extends verbatim to every T>=2 because the "
                "common-root and proportionality arguments are simultaneous "
                "across all active cofactors."
            ),
            "conditionality": (
                "Usefulness does not extend automatically: c must cover "
                "labels where only some sectors vanish, and S_h must be "
                "proved for the full proportional family.  No generic "
                "finite-characteristic Fourier cap c=T or c=T-1 is used."
            ),
            "first_high_impact_application": (
                "Attack the first exact-three-active-sector cell at "
                "ell=7, tau=5, m=6, D=0.  common-root deficit theorem reduces it purely to the "
                "prime-uniform proportional condition S_6<14 (or an "
                "explicit proportional listing witness).  This is a "
                "4-column Fourier-minor/resultant problem and is higher "
                "impact than extending another two-sector finite census."
            ),
        },
        "guards": {
            "lower_degree": (
                "If any cofactor has degree d<D then z<=d<=D-1, so only "
                "the nonsaturated branch can occur; the displayed bound "
                "is safe and the exact deficit hierarchy can sharpen it."
            ),
            "partial_sector_death": (
                "A label where some but not all g_a vanish is live.  Its "
                "remaining support can have a larger fiber cap than the "
                "full support, so c must be robust over all such nonzero "
                "specializations."
            ),
            "bad_characteristic": (
                "Sparse Fourier uncertainty is not imported.  c and S_h "
                "are external theorem/certificate inputs and may depend on "
                "the characteristic and exponent support."
            ),
        },
        "symbolic_audit": symbolic,
        "finite_field_audit": finite,
        "operation_counts": {
            **symbolic,
            "finite_configurations": finite["configuration_count"],
            "blind_cofactor_coefficient_searches": 0,
        },
        "upstream": upstream,
        "next_obligation": (
            "ell=7 three-sector result should decide the ell=7,D=0 exact-three-sector "
            "proportional spectrum S_6 across all prime characteristics "
            "p congruent to 1 mod 7, using normalized 4x4 Fourier minors, "
            "integer resultants, and exact exceptional-prime rank audits."
        ),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")

    print("common-root deficit compiler")
    print(
        "symbolic_rows="
        + str(symbolic["compiler_grid_rows"])
        + " branches="
        + str(symbolic["branch_checks"])
        + " hierarchy="
        + str(symbolic["deficit_hierarchy_checks"])
    )
    print(
        "finite_configs="
        + str(finite["configuration_count"])
        + " active_counts="
        + str(
            sorted(
                {
                    row["active_sector_count"]
                    for row in finite["configurations"]
                }
            )
        )
        + " D_values="
        + str(sorted({row["D"] for row in finite["configurations"]}))
    )
    print("PASS_WITH_COMMON_ROOT_DEFICIT_COMPILER")


if __name__ == "__main__":
    main()
