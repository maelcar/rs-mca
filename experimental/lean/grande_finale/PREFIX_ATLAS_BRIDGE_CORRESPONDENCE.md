# Locator-Prefix Atlas Bridge Correspondence

Status: **PROVED** for concrete locator-prefix support coverage, exact
support-family and Reed--Solomon MCA bad-slope unions, typed cellwise-budget
summation, and the exact fixed-row outer-line lift to the full
Reed--Solomon `B_MCA` numerator. The companion generic bridge proves the
hypothesis-parametric witness-exhaustive to slope-first-match implication for
the fixed-row `B_MCA` numerator. The concrete witness adapter constructs the
finite exact-cardinality `(gamma,S,h)` catalogue and proves its slope image is
exactly the threshold-`a` RS MCA-bad slope set. The prefix-witness composition
then partitions that raw catalogue exactly and, under injective evaluation and
the parity-dimension equation, aligns each cell's slope image with the
corresponding support-prefix bad-slope cell.

The occupancy adapter then proves the exact retained-support fibre sum and a
conditional post-slope-first-match RC1 quotient/`B_MCA` lift. It supplies no
semantic C7 classifier, lower occupancy theorem, profile payment, or `(UNIF)`.
The boundary-payment adapter keeps the full boundary normalization separate
from the retained residual, proves the residual fibre and collision-pair
identities, and instantiates the FC1 ray/moment floor on the actual assigned
slope cell. It supplies no semantic C8 incidence, deployed C9 moment, final
payment comparison, or uniform profile sum.

Sources:

- `experimental/lean/asymptotic_spine/AsymptoticSpine/PrefixAtlas.lean`, the
  generic total-key first-match partition;
- `experimental/lean/grande_finale/GrandeFinale/PrefixPigeonhole.lean`, the
  finite-field locator coefficient key and its fibres;
- `experimental/lean/grande_finale/GrandeFinale/SyndromeLine.lean`, the actual
  support-family MCA/syndrome-line bad-slope set;
- `experimental/lean/grande_finale/GrandeFinale/RSExactSupportUpper.lean`, the
  exact-support reduction for injectively evaluated Reed--Solomon codes;
- `experimental/lean/grande_finale/GrandeFinale/RSExactCardWitnessBridge.lean`,
  the finite coefficient-vector witness catalogue and its concrete generic-
  bridge specialization;
- `experimental/lean/grande_finale/GrandeFinale/RSExactCardPrefixWitnessBridge.lean`,
  the raw-witness locator-prefix partition and exact support-cell slope
  alignment;
- `experimental/lean/grande_finale/GrandeFinale/RSExactCardOccupancyBridge.lean`,
  the exact explanation-state fibre sum and conditional post-first-match RC1
  quotient/`B_MCA` adapter;
- `experimental/lean/grande_finale/GrandeFinale/RSExactCardBoundaryPaymentBridge.lean`,
  the full/residual boundary normalization, collision-pair identity, and
  actual-cell FC1 ray/moment adapter; and
- `experimental/lean/grande_finale/GrandeFinale/FirstMatchAddBack.lean`, the
  ordered finite-set first-match disjointization used by the generic witness
  bridge.

## Statement map

| Interface statement | Lean declaration |
| --- | --- |
| Locator coefficient-prefix key of a supplied support | `GrandeFinale.PrefixAtlasBridge.supportPrefixKey` |
| Concrete prefix cell inside a supplied support family | `GrandeFinale.PrefixAtlasBridge.supportPrefixCell` |
| Membership in a concrete prefix cell | `GrandeFinale.PrefixAtlasBridge.mem_supportPrefixCell_iff` |
| Concrete prefix cells cover exactly the supplied support family | `GrandeFinale.PrefixAtlasBridge.supportPrefixCells_cover` |
| Ambient key-space cardinality is `|F|^(m-K)` | `GrandeFinale.PrefixAtlasBridge.supportPrefixKey_space_card` |
| Coefficient fibres cover all `m`-subsets of the evaluation set | `GrandeFinale.PrefixAtlasBridge.coefficientFiber_biUnion_eq_powersetCard` |
| Bad slopes of all `m`-subsets equal the union of concrete coefficient-fibre cells | `GrandeFinale.PrefixAtlasBridge.badSlopeSetOnPowersetCard_eq_prefixCells_biUnion` |
| Corresponding unconditional union bound | `GrandeFinale.PrefixAtlasBridge.badSlopeSetOnPowersetCard_card_le_sum_prefixCells` |
| Bad slopes of an arbitrary supplied support family equal the union over its prefix cells | `GrandeFinale.PrefixAtlasBridge.badSlopeSetOnSupportFamily_eq_prefixCells_biUnion` |
| Corresponding unconditional union bound | `GrandeFinale.PrefixAtlasBridge.badSlopeSetOnSupportFamily_card_le_sum_prefixCells` |
| Explicit cellwise budgets `U(z)` sum to a whole-family budget | `GrandeFinale.PrefixAtlasBridge.badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets` |
| Locator-prefix cell for the exact-`a` Reed--Solomon support family | `GrandeFinale.PrefixAtlasBridge.rsPrefixBadSlopeCell` |
| Fixed-line threshold-`a` RS bad slopes equal the union of locator-prefix cells | `GrandeFinale.PrefixAtlasBridge.rsMcaBadSlopes_eq_prefixCells_biUnion` |
| Corresponding fixed-line unconditional union bound | `GrandeFinale.PrefixAtlasBridge.rsMcaBadSlopes_card_le_sum_prefixCells` |
| Fixed-line cellwise budgets sum to an RS bad-slope budget | `GrandeFinale.PrefixAtlasBridge.rsMcaBadSlopes_card_le_sum_prefixBudgets` |
| Line-dependent cell budgets with a uniform per-line total bound the full RS numerator | `GrandeFinale.PrefixAtlasBridge.B_MCA_rsEval_le_of_linewise_prefixBudgets` |
| A single line-independent family `U(z)` also bounds the full RS numerator | `GrandeFinale.PrefixAtlasBridge.B_MCA_rsEval_le_sum_prefixBudgets` |
| Slope-level first-match part of projected witness cells | `GrandeFinale.FirstMatchWitnessBridge.firstMatchSlopeCell` |
| Residual witnesses realizing one assigned slope part | `GrandeFinale.FirstMatchWitnessBridge.firstMatchResidualWitnessCell` |
| A residual witness cell has exactly its assigned slope image | `GrandeFinale.FirstMatchWitnessBridge.firstMatchResidualWitnessCell_image_slope` |
| Witness-exhaustive slope budgets bound `B_MCA` by the supremum of line sums | `GrandeFinale.FirstMatchWitnessBridge.B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets` |
| A uniform line-sum bound gives `B_MCA <= B` | `GrandeFinale.FirstMatchWitnessBridge.B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets` |
| Full slope-image coverage need not imply witness exhaustivity | `GrandeFinale.FirstMatchWitnessBridge.slopeImage_cover_not_witnessExhaustive` |
| Raw witness cells can be exhaustive while their slope-first-match residual cells are not | `GrandeFinale.FirstMatchWitnessBridge.firstMatchResidualWitnessCells_not_witnessExhaustive` |
| Finite exact-cardinality `(gamma,S,h)` witness representation | `GrandeFinale.RSExactCardWitnessBridge.RSExactCardWitness` |
| Degree-`<k` explainer decoded from the finite coefficient vector | `GrandeFinale.RSExactCardWitnessBridge.RSExactCardWitness.explanation` |
| Finite linewise catalogue of all valid exact-cardinality witnesses | `GrandeFinale.RSExactCardWitnessBridge.rsExactCardWitnesses` |
| Fixed slope and support determine the valid explainer when `k <= a` | `GrandeFinale.RSExactCardWitnessBridge.explanation_eq_of_valid_of_slope_eq_support_eq` |
| Projection to slope and support is injective on valid witnesses | `GrandeFinale.RSExactCardWitnessBridge.slope_support_projection_injOn_validRSExactCardWitness` |
| RS MCA-bad slopes equal the concrete catalogue's slope image | `GrandeFinale.RSExactCardWitnessBridge.rsMcaBadSlopes_eq_exactCardWitnessSlopeImage` |
| Concrete witness-exhaustive slope budgets bound `B_MCA` by the supremum of line sums | `GrandeFinale.RSExactCardWitnessBridge.B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets` |
| A uniform concrete-catalogue line-sum bound gives `B_MCA <= B` | `GrandeFinale.RSExactCardWitnessBridge.B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets` |
| Locator-prefix key of a literal exact-cardinality witness | `GrandeFinale.RSExactCardPrefixWitnessBridge.rsExactCardWitnessPrefixKey` |
| Literal catalogue cell over one locator-prefix key | `GrandeFinale.RSExactCardPrefixWitnessBridge.rsExactCardPrefixWitnessCell` |
| Locator-prefix witness cells exhaust the raw catalogue exactly | `GrandeFinale.RSExactCardPrefixWitnessBridge.rsExactCardPrefixWitnessCells_cover` |
| Under injective evaluation and the parity-dimension equation, each witness cell's slope image equals its support-prefix bad-slope cell | `GrandeFinale.RSExactCardPrefixWitnessBridge.rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell` |
| First-match witness slopes are contained in the aligned support cell | `GrandeFinale.RSExactCardPrefixWitnessBridge.firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell` |
| Prefix-witness first-match budgets bound `B_MCA` without a raw-exhaustivity hypothesis | `GrandeFinale.RSExactCardPrefixWitnessBridge.B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets` |
| Existing support-prefix budgets feed the same witness adapter | `GrandeFinale.RSExactCardPrefixWitnessBridge.B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets` |
| A uniform prefix-witness line-sum bound gives `B_MCA <= B` | `GrandeFinale.RSExactCardPrefixWitnessBridge.B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets` |
| Retained explanation state `(gamma,h)` of a literal witness | `GrandeFinale.RSExactCardOccupancyBridge.explanationState` |
| Realized explanation states and their retained-support occupancies | `GrandeFinale.RSExactCardOccupancyBridge.explanationStateImage`, `GrandeFinale.RSExactCardOccupancyBridge.retainedSupportOccupancy` |
| Literal witness cells split exactly over realized explanation-state fibres | `GrandeFinale.RSExactCardOccupancyBridge.card_eq_sum_retainedSupportOccupancy` |
| Fibre occupancy literally counts retained selected supports | `GrandeFinale.RSExactCardOccupancyBridge.supportImage_retainedSupportFiber_card` |
| Positive lower occupancy gives `|slope(C)| <= floor(|C| / H)` | `GrandeFinale.RSExactCardOccupancyBridge.slopeImage_card_le_card_div_of_retainedSupportOccupancy` |
| The RC1 quotient applies after slope-level first match | `GrandeFinale.RSExactCardOccupancyBridge.firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy` |
| Post-first-match residual of one locator-prefix witness cell | `GrandeFinale.RSExactCardOccupancyBridge.prefixResidualWitnessCell` |
| Locator-prefix residual occupancy conditionally bounds its assigned slope cell | `GrandeFinale.RSExactCardOccupancyBridge.prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy` |
| Line-dependent RC1 quotients bound `B_MCA` by the supremum of line sums | `GrandeFinale.RSExactCardOccupancyBridge.B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy` |
| A uniform RC1 quotient-sum bound gives `B_MCA <= B` | `GrandeFinale.RSExactCardOccupancyBridge.B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy` |
| Full boundary image and retained residual support data | `GrandeFinale.RSExactCardBoundaryPaymentBridge.ResidualBoundaryProfile` |
| Retained boundary-fibre counts sum to the retained support count | `GrandeFinale.RSExactCardBoundaryPaymentBridge.ResidualBoundaryProfile.card_eq_sum_fiberCount` |
| Equal-boundary ordered pairs equal the residual second moment | `GrandeFinale.RSExactCardBoundaryPaymentBridge.ResidualBoundaryProfile.collisionPairs_card_eq_sum_sq_fiberCount` |
| A nonempty full slice has positive full-image mean | `GrandeFinale.RSExactCardBoundaryPaymentBridge.ResidualBoundaryProfile.fullMean_pos` |
| Selected supports of an actual slope-first-match residual | `GrandeFinale.RSExactCardBoundaryPaymentBridge.assignedResidualSupports` |
| FC1 incidence/moment floor for an actual assigned slope cell | `GrandeFinale.RSExactCardBoundaryPaymentBridge.firstMatchSlopeCell_card_le_boundaryRayMomentFloor` |
| Final integer comparison makes the FC1 floor an `hcell` budget | `GrandeFinale.RSExactCardBoundaryPaymentBridge.firstMatchSlopeCell_card_le_boundaryRayMomentBudget` |

The `FirstMatchWitnessBridge` declarations are generic and logically separate
from locator-prefix support coverage: first match is applied after slope
projection. `RSExactCardWitnessBridge` supplies the concrete finite RS
incidence and bad-slope image. `RSExactCardPrefixWitnessBridge` supplies a
raw-witness-exhaustive structural prefix partition.
`RSExactCardOccupancyBridge` factors retained residual cells through their
`(gamma,h)` explanation states and proves the conditional RC1 quotient.
No C1--C9 semantic cell family, lower occupancy theorem, profile payment, or
`(UNIF)` instance is constructed.

## Statement comparison

`AsymptoticSpine.PrefixAtlas.prefixFibreAtlas_total` proves the abstract
coverage fact: the fibres of a total key map give duplicate-free first-match
coverage of every supplied witness. `PrefixAtlasBridge` replaces the abstract
key by

```text
S |-> coefficientPrefix K m (locator (image point S))
```

and replaces an abstract witness list by a finite family of agreement supports.
On the full evaluation-set chart it uses
`PrefixPigeonhole.coefficientFiber A K m z`; on an arbitrary supplied family it
filters by the same key. The consumer is not an abstract cell count but
`SyndromeLine.badSlopeSetOnSupportFamily`, which deduplicates slopes witnessed
by multiple supports.

The exact union theorem is therefore the concrete bridge:

```text
badSlopeSet(supports)
  = union_z badSlopeSet(prefixCell(supports, z)).
```

The generic support-family theorem carries payment as an explicit hypothesis:

```text
(forall z, card (badSlopeSet (prefixCell z)) <= U z)
  -> card (badSlopeSet supports) <= sum_z U z.
```

This is the prefix-cell counting interface, not a construction of the budgets
or a semantic first-match classification.

The direct Reed--Solomon specialization first invokes
`RSExactSupportUpper.mcaBadSlopes_eq_exactSupportFamily`. For injective
evaluation, `k + R = |D|`, and `k + 1 <= a`, it identifies a fixed received
line's threshold-`a` MCA-bad slopes with the exact-`a` support family and
then partitions that family by locator prefixes. Taking `K := k + 1` gives
the source depth `a - k - 1`.

The exact full-numerator theorem allows line-dependent budgets
`U(u0,u1,z)`. It assumes each cell bound on each line and only requires a
uniform bound `B` on the resulting per-line sum. Its conclusion is
`B_MCA <= B`, with the quantifier order `sup_line sum_z U(line,z) <= B`.

The line-independent theorem is a valid stronger sufficient condition,
effectively bounding `sum_z sup_line cell(line,z)`. This can overpay
exponentially when different lines activate different cells. The
certificate checks the diagonal family with `2^b` lines and cells: every
per-line sum is one, while the sum of cellwise line maxima is `2^b`.

The linewise theorem is the exact fixed-row outer-line `B_MCA` interface. Neither
theorem constructs a cell budget or a catalogue classification, and neither
establishes one paid semantic catalogue uniformly along an asymptotic row;
that stronger ledger `(UNIF)` obligation remains open.

The concrete witness adapter models the literal `(gamma,S,h)` incidence by
storing `gamma`, an exact-cardinality support `S`, and the `Fin k -> F`
coefficient vector of `h`. Its bad-slope image theorem uses
`mcaBad_has_exact_support` directly:

```text
badSlopes(rsEval(ev,k),u0,u1,a)
  = image slope (rsExactCardWitnesses(ev,k,a,u0,u1)).
```

The generic concrete outer-line bounds therefore no longer assume that image
identity, but they still accept a raw-witness-exhaustive cell family.
`RSExactCardPrefixWitnessBridge` supplies one structural instance:

```text
cell(line,z) = { w in rsExactCardWitnesses(line) :
                   supportPrefixKey(w.support) = z }.
```

These cells exhaust the raw catalogue exactly. Under injective evaluation and
the parity-check dimension equation, each cell's slope image equals the
corresponding `rsPrefixBadSlopeCell`.
`RSExactCardOccupancyBridge` then factors each post-first-match residual
through the projection
`(gamma,S,h) -> (gamma,h) -> gamma`. Its exact fibre sum records all realized
explanation states, and a supplied universal occupancy lower bound `H > 0`
gives the exact quotient
`|assigned slopes| <= floor(|retained residual| / H)`.
The lower occupancy and uniform quotient-sum cap remain inputs. Exact
cardinality does not assert that `S` is the complete agreement locus of `h`.

`RSExactCardBoundaryPaymentBridge` supplies the parallel C8/C9 structural
route. For one actual `firstMatchSlopeCell`, its `ResidualBoundaryProfile`
uses the full support slice to define `targetImage` and `fullMean`, while the
post-first-match selected-support image defines `fiberCount` and
`collisionPairs`. The exact identities

```text
sum_s fiberCount(s) = |residual supports|,
|collisionPairs| = sum_s fiberCount(s)^2
```

discharge the support-mass and pair-count premises of
`ExactProfileCompiler.primitiveCell_slope_card_le_floor`. The remaining
premises are deliberately semantic: a residual-to-full inclusion, one
largest residual fibre, a ray incidence with universal degrees `H,J`, and a
final comparison of the resulting floor to the named cell budget. Thus the
theorem reaches the same actual assigned slope cell as the C7 occupancy
adapter without manufacturing a C8 chart or a C9 estimate.

## Scope boundaries

The modules prove support coverage, bad-slope union identities, and their
finite union bounds. It does not prove a semantic C1--C9 classification, a
subexponential count of realized profiles, any numerical `U(z)`, primitive
survival after C1--C8, or a Sidon payment. In particular, totality does not
turn the four residual cells C3/C7/C8/C9 into paid cells.

The integrated C3 census must also be read narrowly. It proves the
subexponential candidate-family count for explicit multiplicative
subgroup-coset and multiplier-fixed loci. That is one input to C3 payment only
after a semantic row is proved to use that family. It does not construct the
row-level family, residual/profile estimate, description-entropy sum, or
distinct-slope projection, and it does not pay unrestricted common-factor or
received-line-resultant C3 cells. General C3 therefore remains an explicit
semantic blocker alongside C7/C8/C9.

The generic module alone supplies no concrete Reed--Solomon witness type. Its
`witnesses`, `slope`, `idx`, `cell`, bad-slope image equality,
witness-exhaustivity equality, cell budgets, and uniform sum are parameters or
hypotheses. Its residual witness cells need not cover the original witnesses;
only their per-cell slope images are exact.

The concrete adapter supplies the finite RS witnesses and discharges the
bad-slope image equality. On its own it constructs no `idx`, `cell`, raw
witness exhaustivity proof, cell budget, or uniform sum. The prefix-witness
composition constructs a structural locator-prefix `idx`, `cell`, and raw
exhaustivity theorem.
The occupancy adapter turns supplied positive lower retained-support
occupancies into exact post-first-match quotient cell bounds and a conditional
`B_MCA` bound, but it does not construct `H`/`hocc`, a semantic C7 classifier,
profile payment, boundary-image theorem, or `hunif`.
The boundary-payment adapter turns supplied C8 incidence degrees and C9
boundary data into an exact FC1 floor for the actual slope cell, but it does
not construct those semantic inputs or prove the final `hpaid`/`hunif` bounds.
Consequently none of these adapters constructs a semantic payment or an
asymptotic `(UNIF)` instance.

The arbitrary-domain definition accepts a map `point : D -> F`; injectivity
is not needed for its coverage/union statements because cells are cut out on
the original support family. The full `m`-subset theorem is stated directly
over `A : Finset F`, matching `PrefixPigeonhole.coefficientFiber`. The direct
RS specialization requires injective evaluation and `k + R = |D|` only to
invoke the exact-support reduction. Its full-numerator theorem additionally
requires a uniform bound on the line-dependent budget sum.
The concrete witness adapter requires only injective evaluation and
`k + 1 <= a`; it does not require a parity dimension or the cardinality
equation used by the locator-prefix specialization.
The parameter `K` remains generic and `a - K` is truncated natural-number
subtraction. In the intended specialization `K := k + 1`, `hka` ensures
`K <= a`; for `K > a` the theorem remains true but degenerates to the
single empty-function key and one global cell.

## Module placement

All six bridges are leaf modules. `PrefixAtlasBridge` imports
`GrandeFinale.SyndromeLine`, which imports the root module `GrandeFinale`;
`FirstMatchWitnessBridge` imports `GrandeFinale` directly; and
`RSExactCardWitnessBridge` imports the generic witness bridge; the
prefix-witness composition imports both concrete leaves; and
`RSExactCardOccupancyBridge` imports that composition plus
`FirstWallMDSExtensionInverse`. `RSExactCardBoundaryPaymentBridge` imports the
occupancy leaf plus `ExactProfileCompiler`. Consequently the root
`GrandeFinale.lean` cannot import these leaves without creating an import
cycle. They remain available through their fully qualified module names and
are checked directly.

## Verification

From `experimental/lean/grande_finale`:

```text
lake build GrandeFinale.PrefixAtlasBridge
lake build GrandeFinale.FirstMatchWitnessBridge
lake build GrandeFinale.RSExactCardWitnessBridge
lake build GrandeFinale.RSExactCardPrefixWitnessBridge
lake build GrandeFinale.RSExactCardOccupancyBridge
lake build GrandeFinale.RSExactCardBoundaryPaymentBridge
```

The six modules print the axioms of their exported coverage, union,
first-match, finite-witness image, exact occupancy sum, RC1 quotient,
boundary-fibre sum, collision-pair identity, FC1 actual-cell floor, fixed-line
budget, and full-numerator theorems. No proof placeholder or added axiom is
used.
