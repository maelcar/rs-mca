# Syndrome-Line Correspondence

Status: **PROVED** for the generic linear-code statements listed below.

Source: `experimental/asymptotic_rs_mca_frontiers.tex`, especially
`prop:syndrome-line-normal-form` and `thm:syndrome-secant-exact`.

## Statement map

| Frontiers statement | Lean declaration |
| --- | --- |
| A word explained outside an error set has syndrome in the supported-error span, and conversely | `GrandeFinale.SyndromeLine.explainedOff_iff_syndrome_mem` |
| Fixed-support MCA badness is transverse syndrome-line incidence | `GrandeFinale.SyndromeLine.badOnSupport_iff_syndromeLine` |
| One fixed noncommon support carries at most one finite slope | `GrandeFinale.SyndromeLine.badSlopesOnSupport_card_le_one` |
| A supplied finite support/error family compiles exactly to a deduplicated secant-incidence set | `GrandeFinale.SyndromeLine.badSlopeSetOnSupportFamily_eq_syndromeSecantSet`, `GrandeFinale.SyndromeLine.badSlopeSetOnErrorFamily_eq_syndromeSecantSet` |
| The number of distinct slopes witnessed by a finite family is at most the number of family members | `GrandeFinale.SyndromeLine.badSlopeSetOnSupportFamily_card_le`, `GrandeFinale.SyndromeLine.badSlopeSetOnErrorFamily_card_le` |
| MCA slopes at agreement `a` equal transverse secant slopes for error sets of size at most `|D|-a` | `GrandeFinale.SyndromeLine.mcaBadSlopes_eq_transverseSecantSlopes` |
| The MCA numerator equals the maximum transverse secant count | `GrandeFinale.SyndromeLine.B_MCA_eq_syndromeSecantNumerator` |

The final equality assumes that the linear syndrome map is surjective, exactly
as required when replacing the maximum over received pairs by a maximum over
all syndrome pairs.  The slope sets are `Finset`s filtered from the field, so a
slope with several support witnesses is counted once.

## Scope boundaries

This module does not construct the generalized Vandermonde parity-check matrix,
prove that its kernel is the Reed--Solomon code, or identify its column spans
with secants of the weighted rational normal curve.  It also does not formalize
`lem:exact-agreement-reduction`, the resulting `binom(n,a)` atlas bound, the
point at infinity, or the later circuit/ray estimates.  Those are independent
specialization and downstream targets; none is assumed by the generic
syndrome-line compiler.

## Verification

The pinned Mathlib 4.28 package command is:

```text
lake build GrandeFinale.SyndromeLine
```

The module prints the axioms of its main exported theorems.  The audit reports
only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`; it contains
no `sorry`, `admit`, `native_decide`, or added axiom.
