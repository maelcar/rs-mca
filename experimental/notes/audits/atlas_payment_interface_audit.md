# Atlas coverage/payment interface audit

## Status and verdict

`AUDIT / NO MATHEMATICAL ISSUE IN THE GUARDED DOWNSTREAM CLAIMS / GENERIC
PREFIX-FIBRE WITNESS TOTALITY = PROVED, UNCONDITIONAL / GENERIC
WITNESS-EXHAUSTIVE TO SLOPE-FIRST-MATCH FIXED-ROW B_MCA IMPLICATION = PROVED,
HYPOTHESIS-PARAMETRIC / FINITE EXACT-CARDINALITY RS WITNESS CATALOGUE AND
BAD-SLOPE IMAGE = PROVED / LOCATOR-PREFIX CELLS ON THE CONCRETE WITNESS
CATALOGUE, RAW-WITNESS EXHAUSTIVITY, AND PARITY-CHECK SUPPORT-CELL SLOPE ALIGNMENT = PROVED /
CONCRETE LOCATOR-PREFIX TO SYNDROME-LINE BAD-SLOPE
UNION = PROVED / TYPED LOCATOR-PREFIX FIXED-ROW OUTER-LINE B_MCA IMPLICATION =
PROVED / POST-SLOPE-FIRST-MATCH RETAINED-SUPPORT OCCUPANCY (RC1)
ADAPTER = PROVED, LOWER OCCUPANCY AND UNIF EXPLICIT / ACTUAL FIRST-MATCH
BOUNDARY-FIBRE AND COLLISION-PAIR IDENTITIES + FC1 RAY/MOMENT LIFT = PROVED,
C8/C9 GEOMETRY AND PAYMENT EXPLICIT / ACTUAL C1--C9 SEMANTIC WITNESS CLASSIFICATION, PAYMENT, AND
ASYMPTOTIC (UNIF) = NOT PROVED.`

The phrase `atlas-totality lane (in progress)` still appears in downstream
threshold notes, but it no longer names the missing mathematical interface
precisely. Totality is already a theorem. What remains is the typed
classification/payment problem: show which primitive packets survive the
earlier semantic cells and supply cellwise distinct-slope and profile budgets.
The old wording is therefore **legacy/type-ambiguous**, not evidence that a
downstream theorem is false.

Label key: **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.

**Credit.** This audit consumes the integrated generic prefix-atlas
formalization in `AsymptoticSpine.PrefixAtlas`, the locator coefficient fibres
in `GrandeFinale.PrefixPigeonhole`, the finite support-family incidence
compiler in `GrandeFinale.SyndromeLine`, the injective RS exact-support
reduction in `GrandeFinale.RSExactSupportUpper`, and the source analyses
`atlas_missing_witness.md`, `atlas_cat_cell_ledger.md`,
`c3_planted_divisor_census.md`,
`heavy_fiber_admissibility_transfer.md`, and
`staircase_concentration_sidon_paired.md`. The typed leaf modules are
`GrandeFinale.PrefixAtlasBridge` and
`GrandeFinale.FirstMatchWitnessBridge`, together with the concrete
`GrandeFinale.RSExactCardWitnessBridge`,
`GrandeFinale.RSExactCardPrefixWitnessBridge`, and
`GrandeFinale.RSExactCardOccupancyBridge`, followed by
`GrandeFinale.RSExactCardBoundaryPaymentBridge`. No `.tex` or `.pdf` file is
edited.

---

## 1. What totality already proves

The generic theorem is explicit in
`experimental/lean/asymptotic_spine/AsymptoticSpine/PrefixAtlas.lean`:

- L7--16 state the intended separation: a total prefix key partitions every
  witness, while numerical payment is independent.
- L29--45 prove that flattening fibres over a covering key list recovers
  exactly the input witnesses.
- L49--73 prove disjointness for duplicate-free witnesses and keys.
- L143--170 prove `prefixFibreAtlas_total_of_keys`: disjoint coverage, exact
  first-match coverage, and a separately supplied profile-count cap.
- L189--210 prove the realized-image form `prefixFibreAtlas_total`; coverage
  has no atlas hypothesis, and the only numerical input is the key-count bound.

Thus a missing witness cannot be a set-theoretic fall-through from the fibres
of a total prefix map. This is the formal version of the unconditional
coverage statement in `atlas_missing_witness.md` L136--172 and the catalogue
ledger's `Coverage / exhaustion --- COMPOSES` conclusion at
`atlas_cat_cell_ledger.md` L120--146.

That result was generic: witnesses are natural-number identifiers and the key
is an arbitrary total function. The new bridge instantiates the same boundary
on the operational finite-field types:

- `PrefixPigeonhole.coefficientPrefix` and `coefficientFiber`
  (`GrandeFinale/PrefixPigeonhole.lean` L20--34) define the locator coefficient
  key and its concrete fibres.
- `SyndromeLine.badSlopeSetOnSupportFamily`
  (`GrandeFinale/SyndromeLine.lean` L311--315) is the actual deduplicated set of
  slopes witnessed by a supplied support family; L327--365 connect it to
  syndrome-line incidence and its fixed-support union.
- `PrefixAtlasBridge.supportPrefixCells_cover` (L57--62) and
  `coefficientFiber_biUnion_eq_powersetCard` (L77--82) prove concrete support
  coverage.
- `badSlopeSetOnSupportFamily_eq_prefixCells_biUnion` (L116--125) proves that
  the bad slopes of the full support family are exactly the union of the bad
  slopes of its locator-prefix cells.
- `RSExactSupportUpper.mcaBadSlopes_eq_exactSupportFamily`
  (`RSExactSupportUpper.lean` L166--191) reduces fixed-line threshold-`a`
  RS MCA-bad slopes to exact-`a` supports. The bridge composes it with the
  locator-prefix partition at L169--184; taking `K := k + 1` gives source
  depth `a - k - 1`.

These are theorem-level equalities. They do not depend on a catalogue payment
assumption.

---

## 2. The typed coverage-to-payment boundary

The generic support-family bridge theorem,
`PrefixAtlasBridge.badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets`
(`PrefixAtlasBridge.lean` L143--154), has the interface

```text
hU : for every prefix key z,
       |bad slopes witnessed by cell(z)| <= U(z)
--------------------------------------------------
|bad slopes witnessed by the full support family| <= sum_z U(z).
```

The RS fixed-line specialization
`rsMcaBadSlopes_card_le_sum_prefixBudgets` (L205--218) has the same form
for threshold-`a` MCA-bad slopes. It still assumes every cell budget and
constructs none.

The exact fixed-row outer-line interface is
`B_MCA_rsEval_le_of_linewise_prefixBudgets` (L222--238). Its cell budget
`U(u0,u1,z)` may depend on the received line. It assumes each line-cell bound
and only a uniform bound `B` on `sum_z U(u0,u1,z)`, then concludes
`B_MCA <= B`. This is `sup_line sum_z U(line,z) <= B`; it does not interchange
the supremum and sum. The stronger line-independent corollary at L242--256 is
valid, but can overpay exponentially when different lines activate different
cells.

The companion generic leaf `GrandeFinale.FirstMatchWitnessBridge` separates
raw witness exhaustivity from slope assignment. `firstMatchSlopeCell` and
`firstMatchResidualWitnessCell` (L28--38) project each witness cell to slopes
before ordered first match, then pull the assigned slope set back into the raw
cell. `firstMatchResidualWitnessCell_image_slope` (L42--61) proves that this
residual cell has exactly the assigned slope image.

`B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets` (L75--108) assumes,
line by line, that MCA-bad slopes are the image of `witnesses`, that the raw
cells union to those witnesses, and that the first-match slope cells satisfy
the budgets `U`. It concludes
`B_MCA <= sup_line sum_i U(line,i)`. The uniform corollary (L112--132) adds
`sum_i U(line,i) <= B` and concludes `B_MCA <= B`.

Two exact `Fin 2 -> Fin 1` controls delimit the result. First,
`slopeImage_cover_not_witnessExhaustive` (L138--144) shows that a proper subset
of witnesses may have the full slope image. Second,
`firstMatchResidualWitnessCells_not_witnessExhaustive` (L149--160) has raw
cells exhausting all witnesses while their residual witness cells do not;
their first-match slope union is nevertheless the full witness-slope image.
Thus slope coverage is sufficient for the numerical count but is strictly
weaker than witness exhaustivity, and residual witness cells are
projection-exact rather than witness-exhaustive.

The concrete leaf `GrandeFinale.RSExactCardWitnessBridge` now discharges the
generic bad-slope image hypothesis for injectively evaluated Reed--Solomon
codes. Its finite witness record stores a slope, a support, and a coefficient
vector `Fin k -> F`; `Polynomial.degreeLTEquiv` decodes that vector to the
degree-`< k` explainer. The valid-witness predicate requires support cardinality
exactly `a`, agreement of the explainer with `u0 + gamma*u1` on that chosen
support, and pair nonexplanation there.

`rsMcaBadSlopes_eq_exactCardWitnessSlopeImage` proves that the slope image of
this finite catalogue is exactly the threshold-`a` RS MCA-bad slope set. It
uses `RSExactSupportUpper.mcaBad_has_exact_support` directly, so it needs no
parity dimension `R` or equation `k + R = |D|`. Equal slope and support
determine the explainer once `k <= a`, but slope alone can still occur on
several supports.

The two generic-concrete outer-line theorems instantiate the first-match bridge
with this catalogue while retaining raw witness-cell exhaustivity, first-match
slope-cell budgets, and the uniform line-sum bound as hypotheses.

The leaf `GrandeFinale.RSExactCardPrefixWitnessBridge` now supplies raw
exhaustivity for one honest structural choice: it filters the literal catalogue
by the locator prefix of each witness's selected support and proves that the
union over all prefix keys is exactly the raw catalogue. Under injective
evaluation and the parity-check dimension equation, each witness cell's slope
image is exactly the existing `rsPrefixBadSlopeCell`; its slope-first-match set
is therefore a subset of that
support-level cell. The specialized `B_MCA` theorems no longer assume
`hbadImage` or raw prefix-cell `hexhaust`, but still assume every `hcell` budget
and, for a fixed bound, `hunif`. The arbitrary prefix-key well-order is used
only for first-match attribution and has no compatibility with field operations.

The occupancy leaf `GrandeFinale.RSExactCardOccupancyBridge` formalizes the
exact two-stage projection `(gamma,S,h) -> (gamma,h) -> gamma`.
`explanationState = (slope, coeffs)` represents the retained
`(gamma,h)` explanation state.

`card_eq_sum_retainedSupportOccupancy` splits a finite literal witness cell
exactly over its realized explanation-state fibres, while
`supportImage_retainedSupportFiber_card` shows that each occupancy literally
counts retained selected supports.

`slopeImage_card_le_card_div_of_retainedSupportOccupancy` gives the exact
finite RC1 quotient `|slope(C)| <= floor(|C| / H)` only under
`H > 0` and a universal lower occupancy hypothesis on every realized state.
The first-match and prefix specializations apply this bound to the retained
`prefixResidualWitnessCell`; the supremum-form `B_MCA` wrapper still takes
the lower occupancies as inputs, and the fixed wrapper additionally assumes the
uniform quotient-sum bound `hunif`.

No semantic C7 profile-scale, classifier, boundary-image theorem, profile
payment, or C1--C9 routing theorem follows from this conditional adapter.

The boundary-payment leaf
`GrandeFinale.RSExactCardBoundaryPaymentBridge` continues from that C7
projection boundary to the C8/C9 finite compiler. Its
`ResidualBoundaryProfile` keeps the full support slice (which determines the
boundary image and mean fibre size) distinct from the retained residual
support slice (whose fibres and equal-boundary pairs enter the numerator).
`card_eq_sum_fiberCount` and
`collisionPairs_card_eq_sum_sq_fiberCount` prove the exact first and second
moment identities. `fullMean_pos` proves that a nonempty full slice has a
positive full-image normalization.

`firstMatchSlopeCell_card_le_boundaryRayMomentFloor` instantiates
`ExactProfileCompiler.primitiveCell_slope_card_le_floor` on the actual
`firstMatchSlopeCell`. The C8 incidence relation and its universal lower/upper
degrees `H,J`, the C9 boundary map/profile data and largest-fibre witness, and
the residual-to-full support inclusion remain inputs. A deployed estimate for
the resulting moment is still needed to discharge `hpaid`.
`firstMatchSlopeCell_card_le_boundaryRayMomentBudget` adds the final integer
comparison `hpaid`, so its result is directly usable as an `hcell` premise in
the existing exact-cardinality `B_MCA` wrappers. This is a structural
composition theorem, not a proof that any intended row supplies those inputs.

These locator-prefix witness cells are not a C1--C9 semantic classification.
Here “exact-cardinality” still does not assert that the chosen support is the
explainer's complete agreement set: agreement at additional coordinates is
allowed.

The certificate checks the exact diagonal model with `2^b` lines and cells:
`sup_line sum_z = 1`, while `sum_z sup_line = 2^b`.

This conditional implication is for one finite row. It neither constructs nor
stabilizes a paid semantic catalogue along an asymptotic row, so the ledger's
full `(UNIF)` obligation remains open.

Coverage constructs the cells and proves their union. It does **not**
construct `U`, show that `sum_z U(z)` has the required asymptotic scale, prove
that the realized semantic profile set is subexponential, or classify a cell
as C1--C9. Those are additional hypotheses, visible in the type of `hU` rather
than hidden in the word “totality.”

An exact negative control makes the logical separation unavoidable. On
`2^b` items, the identity key `i |-> i` is total and its fibre atlas covers
every item exactly once, but it realizes `2^b` singleton cells. Totality alone
therefore permits exponentially many profiles and supplies no nontrivial
slope-payment estimate.

---

## 3. The full-catalogue residual

The current payment ledger already records the correct split:
`atlas_cat_cell_ledger.md` L14--20 declares unconditional exhaustion and four
blocked cells; L98--110 gives the per-cell tally; and L148--196 separates the
five paid regimes from the full-catalogue residual. The exact residual is:

| Cell | Remaining obligation | Current anchor |
| --- | --- | --- |
| C3 planted | General semantic payment remains open. `c3_planted_divisor_census.md` proves only the subexponential candidate-family census for explicit multiplicative subgroup-coset and multiplier-fixed loci. That discharges one census factor after a row is proved to use this family; it does not construct the row-level family or prove residual profile scale, description entropy, or distinct-slope projection. Unrestricted common-factor/resultant readings remain open. | `c3_planted_divisor_census.md` Sections 3--10; `atlas_cat_cell_ledger.md` L161--164 |
| C7 saturation | Prove semantic profile collapse/classification and a positive retained-support occupancy `H` at the intended profile scale, or an equivalent direct final-slope estimate. | L165--169 |
| C8 higher-dimensional balanced core | Prove the higher-dimensional ray-compiler condition `(RC)` or an equivalent direct decomposition/payment. | L170--176 |
| C9 Fourier/Sidon | Prove the deployed-scale image-normalized Sidon payment. | L177--186 |

Equivalently, the unresolved interface is **general C3 semantic planted
payment + C7 semantic classification/profile collapse and positive
intended-profile occupancy (or a direct final-slope estimate) + C8
higher-dimensional `(RC)` + C9 Sidon payment**. For the explicit
subgroup-coset/multiplier-fixed C3 family, only the candidate-census factor is
already proved; calling the whole cell paid would also require the missing
row-level identification, residual/profile estimate, and slope projection.
Generic prefix coverage, the conditional RC1 adapter, and the new FC1 bridge
remove none of those semantic hypotheses. The FC1 bridge instead pins the
exact conclusion once the C8 incidence and C9 moment inputs are supplied.

---

## 4. The Sidon-paired consumer needs survival or earlier payment

The Sidon-paired depth-one class makes the distinction concrete.
`heavy_fiber_admissibility_transfer.md` L242--278 states its transfer theorem
as **CONDITIONAL** and makes `(H4)` explicit at L256--257: the packet must be a
genuine primitive first-match residual for which “earlier cell” is meaningful.
The note repeats at L334--352 that `(H4)` is assumed and that no image-scale
MI/MA or Sidon payment follows. Its depth-one concrete fibre is identified at
L326--330.

Meanwhile `staircase_concentration_sidon_paired.md` L20--40 and L150--190 prove
that this actual depth-one atlas family has an exponential staircase of fibre
sizes and exponentially many relevant syndromes; L319--345 records the route
cut for the fibre-indexed heavy/light decomposition. It is not an artificial
support family that totality could simply omit.

Consequently a downstream use of this consumer needs one of two semantic
statements on the intended deployed row:

1. prove that the Sidon-paired depth-one packet genuinely survives the C1--C8
   first-match tests and reaches the primitive/C9 consumer; or
2. classify it into an earlier C1--C8 cell and pay that cell, including its
   profile census and distinct-slope budget.

The prefix-atlas theorem cannot “exclude the class”: it covers the class by a
prefix cell. Exclusion from the primitive residual is a first-match
classification theorem, not a totality theorem.

---

## 5. Audit of the legacy downstream wording

A whitespace-tolerant scan finds 28 occurrences of `atlas totality` or
`atlas-totality` in 11 threshold notes. Twenty-seven are each contained on a
single physical line; the remaining phrase is split across `twisted_coset_cube_spectrum.md`
L53--54. Representative examples include:

- `rank_one_emission_arithmetic.md` L114 and L303;
- `band_uniform_cube_reduction.md` L112 and L267;
- `fold_charge_localization.md` L125 and L375;
- `resonant_folding_inverse.md` L118 and L441; and
- `transverse_charge_obstruction_sidon_paired.md` L59, L139, and L448.

The recurring text calls this an `atlas-totality lane (in progress)` and, in a
few places, treats it as an escape that could exclude the Sidon-paired class.
That description predates the integrated total-fibre theorem and conflates
three different types:

```text
total key map / set coverage
    versus semantic C1--C9 first-match classification
    versus per-cell profile and distinct-slope payment.
```

The guarded mathematical claims remain sound. For example,
`transverse_charge_obstruction_sidon_paired.md` L139--143 labels its use
conditional and assumes no result from it, while L441--456 explicitly lists
atlas totality among the nonclaims. The issue is nomenclature and dependency
typing, not a failed proof.

For future references, replace the legacy shorthand by the exact obligation:
“primitive survival / C1--C8 classification on the deployed row, together with
general C3 semantic payment (with the narrow coset/fixed-locus census factor
already proved), C7 occupancy or direct projection, C8 ray incidence, and C9
image-normalized moment payment.”

---

## 6. Nonclaims and module placement

- No actual C1--C9 semantic witness cells, realized profile index, or
  primitive-survival theorem is constructed.
- `RSExactCardWitnessBridge` constructs the finite RS witness catalogue and
  proves its exact bad-slope image. It does not construct `idx`, `cell`,
  `hexhaust`, `hcell`, or `hunif`; those generic inputs remain parameters or
  hypotheses in that module.
- `RSExactCardPrefixWitnessBridge` constructs `idx`, `cell`, and `hexhaust`
  only for the structural locator-prefix partition. It constructs no C1--C9
  classifier, `hcell` payment, or `hunif` bound.
- `RSExactCardOccupancyBridge` turns supplied positive lower retained-support
  occupancies into exact post-first-match quotient cell bounds. It constructs
  neither the lower bound, a semantic C7 classifier/profile payment, a
  boundary-image theorem, nor `hunif`.
- `RSExactCardBoundaryPaymentBridge` proves the full-image normalization,
  retained-fibre sum, collision-pair identity, and actual-cell FC1 implication.
  It does not construct semantic C8 incidence degrees, a deployed C9 moment,
  the final `hpaid` comparison, or the row-uniform sum.
- First-match residual witness cells need not cover the raw witnesses. Only
  their per-cell slope images are proved exact.
- No bridge proves a semantic cell payment or the uniform sum hypothesis
  `(UNIF)`. The narrow subgroup-coset/multiplier-fixed C3 candidate census is
  proved elsewhere, but no general or row-level C3 family/payment,
  intended-profile C7 occupancy, semantic C8 incidence bound, or deployed C9
  Sidon payment is constructed here.
- No deployed smooth/circle row, main asymptotic theorem, or reserve theorem is
  closed.
- No guarded result in the downstream notes is retracted or corrected.
- No `.tex` or `.pdf` file is changed.

`PrefixAtlasBridge.lean`, `FirstMatchWitnessBridge.lean`,
`RSExactCardWitnessBridge.lean`, `RSExactCardPrefixWitnessBridge.lean`, and
`RSExactCardOccupancyBridge.lean`, and
`RSExactCardBoundaryPaymentBridge.lean` are deliberately leaf modules. The first
reaches the root module through `GrandeFinale.SyndromeLine`; the generic
witness bridge imports `GrandeFinale` directly; the concrete adapter imports
that generic bridge; the prefix-witness composition imports the concrete
adapter and support-prefix leaf; and the occupancy leaf imports that prefix
composition plus `FirstWallMDSExtensionInverse`. The boundary-payment leaf
imports the occupancy leaf and `ExactProfileCompiler`. Importing these leaves
back into `GrandeFinale.lean` would create an import cycle. The focused
verification targets are therefore

```text
lake build GrandeFinale.PrefixAtlasBridge
lake build GrandeFinale.FirstMatchWitnessBridge
lake build GrandeFinale.RSExactCardWitnessBridge
lake build GrandeFinale.RSExactCardPrefixWitnessBridge
lake build GrandeFinale.RSExactCardOccupancyBridge
lake build GrandeFinale.RSExactCardBoundaryPaymentBridge
```

The companion stdlib verifier
`experimental/scripts/verify_atlas_payment_interface.py` checks the theorem
anchors, the exact-cardinality catalogue and bad-slope image, raw prefix-cell
witness exhaustivity and support-cell alignment, the exact explanation-state
fibre sum, the universal lower-occupancy `hocc` boundary, the RC1 quotient,
the full-vs-residual normalization boundary, the retained boundary-fibre and
collision-pair identities, the exact C8/C9 FC1 signature, its final `hpaid`
boundary, and the fixed `hunif` boundary. It also checks the fixed-line `hU`
and exact linewise `hcell` boundary, the four-cell ledger, the narrow scope of
the integrated C3 census, the conditional `(H4)` interface, the legacy wording
census, and the exponential-cell negative control. Its machine-readable output is
`experimental/data/certificates/atlas-payment-interface/atlas_payment_interface.json`.
