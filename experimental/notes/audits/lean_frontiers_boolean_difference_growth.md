# Lean correspondence: Boolean difference growth

## Main result

**PROVED.**  For duplicate-free finite families
`A,B subset {0,1}^n`, the stdlib-only Lean development proves the exact integer
difference bound

```text
|A-B|^2 >= |A|^2 |B|.
```

Taking `B=A` gives `|A-A|^2 >= |A|^3`, hence the square-root-free quasicube
inequality consumed by the retained BSG high-energy argument.  Its concrete
primitive-Boolean wrappers therefore no longer take quasicube growth as a
hypothesis; BSG extraction and the low-energy/Sidon payment remain explicit
inputs.  The separate direct compiler in PR #605 from `E(F)^3 <= |F|^8` is
unchanged and does not depend on this result.

## Files

- `experimental/lean/asymptotic_spine/AsymptoticSpine/BooleanDifferenceGrowthNat.lean`
- `experimental/lean/asymptotic_spine/AsymptoticSpine/BooleanDifferenceGrowth.lean`
- `experimental/lean/asymptotic_spine/AsymptoticSpine.lean`

## Statement-to-declaration map

| Finite step | Lean declaration | Status |
| --- | --- | --- |
| Four coordinate-block square bounds combine into one square bound | `boolean_difference_growth_nat` | PROVED over `Nat` |
| General duplicate-free Boolean family, without a fixed-weight restriction | `BooleanPointFamily` | PROVED representation |
| Exact deduplicated mixed difference set and membership | `mixedDifferenceSet`, `mem_mixedDifferenceSet_iff` | PROVED |
| Head-bit split preserves total point cardinality | `headTailFamily_card_partition` | PROVED |
| Mixed differences split into first-coordinate fibers `-1`, `0`, and `1` | `mixedDiffCard_head_decomposition` | PROVED exact equality |
| The off-diagonal fibers are `A_0-B_1` and `A_1-B_0`; the zero fiber contains both diagonal differences | `mem_negativeDifferenceTailFiber_iff`, `mem_zeroDifferenceTailFiber_iff`, `mem_positiveDifferenceTailFiber_iff` | PROVED |
| `|A-B|^2 >= |A|^2|B|` | `booleanPointFamily_mixed_difference_growth` | PROVED by dimension induction |
| `|F-F|^2 >= |F|^3` for a fixed-weight `BoolFamily` | `boolFamily_diffCard_cube_growth` | PROVED |
| Exact squared quasicube form for a realized semantic fiber | `boolFiber_quasicube_squared` | PROVED |
| Retained BSG route with quasicube discharged | `no_high_energy_bound_boolean` | CONDITIONAL only on the displayed BSG output |
| Retained BSG moment compiler with quasicube discharged | `primitiveBooleanMomentUpper_of_bsg`, `primitiveBooleanMomentUpper_of_bsg_and_lowEnergyPayment` | CONDITIONAL on BSG, and on the low-energy payment in the paid form |

## Proof boundary

The induction is performed in the torsion-free group `Vector Int n`.  Splitting
the first Boolean coordinate gives three disjoint difference heads.  The
`-1` and `1` fibers are the two off-diagonal mixed differences, while the zero
fiber is the deduplicated union of the two diagonal mixed differences.  Four
lower-dimensional mixed bounds feed the exact natural-number combination
lemma.  This simultaneous mixed statement is stronger than an induction on
self-differences alone and is what makes the zero-fiber overlap harmless.

Duplicate-free point lists are load-bearing because all lengths represent set
cardinalities.  Empty families and dimension zero are included.  Fixed weight
is not needed for difference growth; it enters only when the result is applied
to `BoolFamily` and semantic `BoolFiber` witnesses.

## Nonclaims

This packet does not formalize the full quasicube tripling theorem for arbitrary
`P,Q`, Balog--Szemeredi--Gowers, the BSG extraction producer, the
low-energy/Sidon payment, max-fiber control, C9, character-frame estimates, or
any asymptotic `o(n)` bookkeeping.  It proves exactly the Boolean
self-difference corollary required by `NoHighEnergy.lean`.

## Interaction with open PRs

This branch is stacked on PR #605, which introduces `BoolFamily`, semantic
`BoolFiber`, and primitive finite-moment compilers.  Its amended head preserves
the original BSG/quasicube APIs and also adds a separate direct compiler from
the explicit sharp-energy consequence `E(F)^3 <= |F|^8`.  This packet affects
only the retained BSG alternative; it neither proves nor strengthens that
sharp-energy input.  PR #592 uses BSG/quasicube as external finite inputs; this
packet supplies the quasicube side generically and makes no claim about its F2
constants or BSG producer.

## Lineage

The target corollary is the Boolean difference specialization used in
`experimental/asymptotic_rs_mca_frontiers.tex` and cited there through the
GMRSZ/MRSZ quasicube theorem.  This packet stacks on PR #605 and reuses
the integrated `NoHighEnergy.lean` arithmetic rather than duplicating it.

## Verification

From `experimental/lean/asymptotic_spine/`:

```text
lake build
```

The package is stdlib-only on Lean 4.31.0.  Selected `#print axioms` checks
report only Lean's standard `propext`, `Quot.sound`, and `Classical.choice`.
There is no `sorryAx`, `sorry`, `admit`, `native_decide`, or added axiom.
