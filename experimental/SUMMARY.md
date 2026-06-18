# Experimental Summary

Status: AUDIT / EXPERIMENTAL.

This file summarizes the recent PR wave integrated into `experimental/`. It is
not a proof-status authority and it does not promote any result into the main
papers. The source triage records are:

- `pr-triage-2026-06-17.md`: PRs #1, #2, #3, and #46 through #66.
- `pr-triage-2026-06-18.md`: PRs #67 through #77, with #68 and #76
  superseded by #77.

The common policy was: keep Papers A-D unchanged, land new material in
`experimental/`, preserve explicit status labels, and require review before any
promotion into `tex/` or `scripts/`.

## Big Picture

The recent PRs are pushing the project from broad corrected-reserve conjectures
toward a finite set of auditable local problems. They do this by turning the
main MCA/list questions into explicit ledgers:

- support-fiber and locator-fiber ledgers for L1;
- support-overlap, quotient-periodic, and occupancy ledgers for M1;
- extension-line and residue-line ledgers for F1;
- line-decoding conversion and separation ledgers for M2;
- full-agreement support intersection ledgers for L2;
- audit/citation/certificate ledgers for Paper D and Paper C style protocol
  accounting.

The direction is constructive: after Paper A rules out no-slack MCA, the recent
experimental material is trying to identify exactly which obstructions remain
after the corrected reserve is paid. The most useful progress is not one single
large theorem yet; it is the reduction of several vague hazards into named,
script-checkable walls.

## What Was Added

### Locator fibers and L1

The locator-fiber work now has three layers:

- `locator_fiber_sweep/` and `locator_fiber_sweep_analysis/` provide Python
  sweep and analysis tooling.
- `sage_locator_fiber_crosscheck/`, `locator_fiber_crosscheck_report/`, and
  `locator_fiber_local_packet/` add independent Sage/Python cross-checks and a
  reproducible local packet runner.
- `l1_aperiodic_prefix_collision.md` and
  `verify_l1_aperiodic_prefix_collision.py` isolate a concrete `F_17`
  monomial-prefix collision packet and a complement-locator formulation.

This helps the MCA program because the corrected conjecture needs polynomial
control of generated-field locator fibers after quotient obstructions are
removed. The new material gives exact toy certificates, catches overstrong
proof routes, and provides a path for separating quotient-periodic fibers from
aperiodic collisions.

What it does not yet give: a general generated-field local-limit theorem in the
fixed-rate corrected-reserve regime.

### M1 support overlap and quotient profiles

The M1 material has become much more ledger-like:

- `m1_average_support_collinearity.md` gives random-line support-collinearity
  estimates and shows covariance is concentrated in high-overlap support pairs.
- `m1_support_coefficient_test.md` records a local coefficient-test route.
- `m1_quotient_periodic_overlap_profile.md`,
  `m1_occupancy_profile_scan.py`, and `m1_support_occupancy_scan.py` give exact
  quotient-periodic and occupancy-profile overlap formulas.
- `quotient_profile.py` and `quotient_profile_dither.py` scan exact quotient
  profiles and dithered dimensions.
- `verify_m1_quotient_remainder_profile.py` and the slack-three verifiers check
  finite quotient/remainder cases.

This pushes toward the MCA conjecture by converting "bad support packing" into
explicit exchange-codegree and quotient-occupancy terms. The quotient terms can
now be budgeted, killed by dimension dithering in some regimes, or separated
from the genuinely aperiodic part of the problem.

What is still missing: a proof that the remaining aperiodic residue-line
packing is small enough above the corrected reserve.

### F1 extension lines and residue-line walls

The F1 work is now the most developed obstruction ledger:

- `f1-extension-witness/` gives an initial extension witness package.
- `f1_extension_slope_sweep.py` scans extension-line slopes.
- `f1_fixed_rate_extension_counterexample.md` proves that an unrestricted
  same-numerator extension-line transfer is false.
- `f1_extension_coordinate_transfer.md` records the reduction of extension-line
  MCA to a multiplication-slice/interleaved base-code problem.
- `f1_arbitrary_anchor_locator_split.md` and
  `f1_monic_anchor_base_core_reduction.md` isolate the arbitrary-anchor and
  monic-anchor residue-line issues.
- `2026-06-17-codex-f1-l1-audit/` and `2026-06-18-fable-loop/` record audited
  route cuts, local checks, and raw model provenance for balanced-denominator
  and line-incidence routes.

This is useful because extension challenges are a likely protocol pressure
point. The recent work makes clear that one cannot simply use a base-field MCA
numerator and divide by a larger extension challenge field. It also narrows the
positive F1 target to a precise residue-line incidence problem.

The current live wall is the arbitrary-anchor balanced-denominator regime. In
the Fable-loop audit, the restricted `t=sigma=2`, `j=2` and parts of `j=3`
line-incidence story are reduced to explicit conic/quadric/rank-determinant
conditions. The unresolved branch is the rank/determinant resonance, especially
the `Q==0` split-cubic case and the extension of these arguments beyond the
small restricted regimes.

### M2 line decoding

The line-decoding material keeps the protocol object honest:

- `m2_line_decoding_mca_bridge.md` translates between MCA bad slopes and
  line-decoding ambiguity.
- `m2_line_decoding_separation.py` gives a tiny separation check showing that
  close-point line decoding and support-wise noncontainment are not identical
  without the right support accounting.

This matters because Paper C style protocols may consume line-decoding rather
than support-wise MCA directly. The experiments help prevent accidental
replacement of MCA, CA, and line-decoding by each other.

What is still missing: a final corrected-reserve line-decoding theorem with
parameters matched to Paper B's MCA formulation.

### L2 interleaving

The L2 material changes the interleaved-list accounting from a product bound to
an intersection-profile problem:

- `l2_interleaved_support_bridge.md` proves a finite support injection and
  full-agreement support formula.
- `l2_exact_support_diagonalization.md` handles the exact-support case.
- `interleaved_list_enum.py`, `interleaved_budget.py`, and
  `quotient_core_interleaving.py` provide small enumerators and certificates.

This is directly useful for protocol parameters. It says that interleaving does
not automatically multiply the list exponent by the row arity if the rows share
the same agreement columns and the full-support intersection profile is small.

What is still missing: sharp constants near capacity for the concrete arities
and radii used in protocols.

### A0/A1 audits, certificate tooling, and formalization

The support material is also important:

- `a0_cs25_import_audit.md`, `a0_cs25_rational_constant_derivation.md`, and
  `cs25_import_audit.md` track the imported Crites-Stewart/ABF dependency for
  Paper D.
- `a1_paperA_finite_verification_crosswalk.md` maps Paper A finite claims to
  scripts and certificates.
- `certificate_emit.py`, `reserve_certificate_schema.json`, and
  `protocol_ledger_template.md` move toward Paper C style reserve certificates.
- `theorem_label_map.md` and the TeX audit/inventory scripts support citation
  hygiene before promotion.
- `lean_formalization/` is an initial Lean scaffold, not a completed
  formalization.

This work does not prove MCA, but it raises the chance that any future proof is
auditable and that field ledgers do not get mixed.

## How This Points Toward The MCA Conjecture

The strongest emerging picture is:

1. Quotient-periodic support families can be explicitly accounted for.
   The new M1 scanners and dither ledgers make these obstructions visible at
   finite parameters instead of treating them as background risk.

2. The aperiodic problem is now more isolated.
   Once quotient occupancy and high-overlap codegrees are printed, what remains
   is closer to a genuine inverse-additive or residue-line packing theorem.

3. Extension-line behavior is no longer a black box.
   The counterexamples show which extension-transfer statements are false, and
   the coordinate-transfer notes suggest the positive theorem should probably
   be phrased as an interleaved or multiplication-slice statement.

4. Interleaving may be cheaper than the trivial product bound.
   The L2 full-support formula gives a plausible way to keep protocol
   interleaved-list costs within the reserve budget, if the required support
   intersection bounds can be proved.

5. The line-decoding ledger is becoming compatible with MCA.
   M2 is not solved, but there is now a concrete bridge and a warning example
   against using the wrong object.

6. The main missing proof is getting smaller and sharper.
   The recent Fable-loop work repeatedly converts broad residue-line claims
   into explicit algebraic surfaces, rank conditions, and finite verifier
   targets. That is progress even when the conclusion is a route cut.

## What Is Still Missing

The project still needs the following before the MCA conjecture can be treated
as settled.

1. A general M1 corrected-reserve local limit.
   The current material controls random baselines, quotient-periodic families,
   and several toy occupancy regimes. It does not yet prove that all aperiodic
   residue-line support packings are polynomially small above the reserve.

2. A general L1 generated-field locator local limit.
   The locator-fiber tools are strong enough to find and classify finite
   packets, but the desired theorem for arbitrary received words over
   polynomial generated fields is still open.

3. A repaired F1 extension-transfer theorem or corrected-reserve
   counterexample.
   The naive same-numerator lift is false. The live positive route must handle
   arbitrary anchors, balanced denominators, multiplication-slice behavior, and
   the rank/determinant resonance branch.

4. Sharp L2 interleaved-list constants.
   The support-intersection formula is promising, but protocol use needs
   constants for actual arities and radii, not only structural reductions.

5. A clean M2 line-decoding theorem.
   The bridge note must become a parameter-exact statement that says exactly
   when Paper B's MCA form implies the line-decoding object Paper C wants.

6. A completed A0 dependency audit.
   Paper D's universal cap still depends on the imported list-to-agreement
   conversion being checked against primary sources and exact constants.

7. Promotion discipline.
   Several files contain local `PROVED` or `BANKABLE_LEMMA` claims, but the
   project should not promote them into the papers until a human review checks
   hypotheses, constants, notation compatibility, and field-ledger separation.

## Next Steps

Recommended next work:

1. Run a full experimental verifier suite and record a machine-readable result
   ledger, starting from the scripts named in the two PR triage files.

2. Turn the M1 quotient occupancy formulas into a compact theorem note with
   exact hypotheses, then separate "budgeted quotient" terms from the
   aperiodic residue-line target.

3. Continue the F1 rank/determinant split work from
   `2026-06-18-fable-loop/`, especially the `Q==0` split-cubic branch and the
   transition from `t=2` toy regimes to corrected-reserve slack.

4. Use `locator_fiber_local_packet/` as the canonical L1 cross-check entry
   point and expand it from tiny examples toward the `q=17`, `q=257`, and
   dyadic toy cases in `agents.md`.

5. Convert the L2 full-support intersection formula into concrete certificates
   for `mu=2` and then for protocol-relevant arities.

6. Finish the A0 Crites-Stewart/ABF import audit before relying on Paper D's
   cap as theorem-backed infrastructure.

7. Choose a small set of stable lemmas for Lean formalization: support
   injection, full-support interleaving formula, complement-prefix locator
   lemma, and quotient-periodic overlap profile.

8. Keep all new material in `experimental/` first, with an `agents-log.md`
   entry and a reproducible command or certificate whenever possible.

## Reading Order

For a new contributor trying to understand the current experimental state:

1. Read `agents-log.md`.
2. Read `pr-triage-2026-06-17.md` and `pr-triage-2026-06-18.md`.
3. Read `m1_quotient_periodic_overlap_profile.md`,
   `m1_average_support_collinearity.md`, and `quotient_profile_dither.md`.
4. Read `f1_fixed_rate_extension_counterexample.md`,
   `f1_extension_coordinate_transfer.md`, and
   `2026-06-18-fable-loop/README.md`.
5. Read `l1_aperiodic_prefix_collision.md` and the locator-fiber packet
   READMEs.
6. Read `l2_interleaved_support_bridge.md` and
   `m2_line_decoding_mca_bridge.md`.
7. Read `a0_cs25_import_audit.md`,
   `a1_paperA_finite_verification_crosswalk.md`, and
   `protocol_ledger_template.md` before touching protocol claims.
