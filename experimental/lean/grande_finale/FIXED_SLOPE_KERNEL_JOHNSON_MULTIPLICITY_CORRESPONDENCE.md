# Fixed-slope kernel-Johnson multiplicity correspondence

Status: **PROVED / AUDIT** for the reusable set-system inequality, the direct
fixed-syndrome theorem, and the fixed-slope hosted-pair specialization. The
modules typecheck with Lean and Mathlib `v4.28.0` without proof placeholders.

Source: `experimental/notes/thresholds/fixed_slope_kernel_johnson_multiplicity.md`,
especially Theorem 1 and equations (3)--(6), (7)--(13), and (22)--(25).

## Statement map

| Source argument | Lean declaration |
| --- | --- |
| Fixed-slope pair fiber | `GrandeFinale.FixedSlopeKernelJohnsonMultiplicity.fixedSlopeFiber` |
| Johnson denominator, numerator, and positivity gate in (3)--(6) | `kernelJohnsonDenominator`, `kernelJohnsonNumerator`, `KernelJohnsonPositive` |
| Direct fixed-syndrome hypotheses and conclusion | `FixedSyndromeHypotheses`, `FixedSyndromeKernelJohnsonConclusion` |
| Theorem 1: unconditional product inequality and positivity-gated quotient | `fixedSyndromeKernelJohnsonMultiplicity` |
| Proposition surface for both forms of the fixed-slope specialization | `FixedSlopeKernelJohnsonConclusion`, `fixedSlopeKernelJohnsonMultiplicityTarget` |
| Point degrees and the incidence identity in (10) | `GrandeFinale.SetSystemJohnson.pointDegree`, `sum_pointDegree` |
| Ordered-pair second-moment identity underlying (11)--(12) | `GrandeFinale.SetSystemJohnson.sum_pointDegree_sq` |
| Multiplicative inequality `M(s^2-Nw) <= N(s-w)` | `GrandeFinale.SetSystemJohnson.setSystemJohnson` |
| Positive-denominator quotient form | `GrandeFinale.SetSystemJohnson.setSystemJohnson_div` |
| Zero set and `|Z(e)|=N-wt(e)` | `zeroSet`, `zeroSet_card` |
| Choice of an exact `(N-t)`-subset as in (7) | `truncateTo`, `truncateTo_spec`, `chosenZeroSet`, `chosenZeroSet_spec` |
| Same-slope differences are nonzero kernel words | `fixedSlope_sub_mem_kernel`, `fixedSlope_sub_ne_zero` |
| Common-zero cap `|B_e intersect B_f| <= kappa-1` in (8)--(9) | `zeroSet_inter_subset_sub_zeroSet`, `chosenZeroSet_inter_le` |
| Fixed-slope product and quotient conclusions | `fixedSlopeKernelJohnsonMultiplicity` |
| Canonical A6 denominator, numerator, and cap six in (22)--(25) | `canonicalA6_denominator`, `canonicalA6_numerator`, `canonicalA6_kernel_cap`, `canonicalA6_multiplicity_le_six` |

## Hypothesis correspondence

The abstract theorem works on any finite ground type `D` and any finite family
of `s`-element blocks whose differently labelled members intersect in at most
`w` points. It makes no coding-theoretic or field assumption.

The application uses the existing hosted-pair interface
`BasicPairHypotheses H y₀ y₁ P t`. Thus every retained pair has error weight at
most `t` and syndrome `y₀ + gamma*y₁`; after filtering to one `gamma`, all
errors have the same syndrome. `KernelDistanceAtLeast H (N-kappa+1)` supplies
the distance used in (8). The explicit assumptions `0 < kappa`, `kappa <= N`,
and `t <= N` control natural-number subtraction, while
`KernelJohnsonPositive` is exactly the strict gate required for division.

The Lean application is slightly more structural than the paper proof: block
choice is an explicit classical function, and the second moment counts ordered
pairs. On the positive-denominator locus its natural-number subtractions are
literal and its algebraic conclusion matches (4)--(6). Outside that locus the
natural denominator truncates to zero, representing the automatic/vacuous
signed product inequality; no quotient cap is derived. The hosted-pair target
retains the line-direction nonzero clause carried by `BasicPairHypotheses`; the
proof itself uses only the common-syndrome and weight clauses after fixing a
slope.

## Scope boundaries

The formalization proves the direct fixed-syndrome multiplicity statement, its
hosted-line per-slope specialization, and the canonical arithmetic. It does not
prove the separate Noether/interpolation
bound on the number of slopes, count repeated raw support labels `S`, handle the
nonpositive Johnson denominator with a quotient/counting cap, build a
witness-exhaustive atlas, or close a deployed row. No stable paper source is
changed.

## Verification

```text
lake env lean -DwarningAsError=true GrandeFinale/SetSystemJohnson.lean
lake env lean -DwarningAsError=true GrandeFinale/FixedSlopeKernelJohnsonMultiplicity.lean
lake build GrandeFinale
```

The modules print the axioms of their principal results. Expected foundational
axioms are `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` or
added axiom occurs.
