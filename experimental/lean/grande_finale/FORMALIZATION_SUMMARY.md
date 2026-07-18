# Grande Finale Formalization Summary

This package is a partial Lean formalization of
`experimental/grande_finale.tex`.

## Package Layout

- `GrandeFinale.lean`: core self-contained kernels for integer budgets,
  first-match ledgers, CA/MCA bad-slope monotonicity, moment inequalities, and
  finite packet arithmetic checks.
- `GrandeFinale/SetSystemJohnson.lean`: abstract set-system Johnson
  multiplicity kernel used by fixed-slope support caps.
- `GrandeFinale/FixedSlopeKernelJohnsonMultiplicity.lean`: fixed-slope
  kernel-Johnson multiplicity compiler; theorem-level combinatorial cap, not a
  full threshold theorem.
- `GrandeFinale/ExactWeightAllPairs.lean`: selector-free exact-weight
  same-slope kernel alternative; different-slope, endpoint, and two-block
  compiler surfaces remain unproved targets.
- `GrandeFinale/Rank16FixedCoreQuotientLineObstruction.lean`: rank-16
  fixed-core quotient-line obstruction kernel for the q64 line family.
- `GrandeFinale/TripleNegativeFirstMatchReduction.lean`: triple-negative
  first-match reduction to one residual wall.
- `GrandeFinale/AugmentedBasisPencilDesignInverse.lean`: augmented-basis
  pencil and deep-hole design inverse audit kernel.
- `GrandeFinale/FirstWallMDSExtensionInverse.lean`: abstract finite
  owner-image bounds, equality/injectivity criteria, the exact owner-fiber
  partition, and five pinned binomial identities used by the first-wall audit.
  Weighted-GRS interpolation, the MDS-extension equivalence, retained/deleted
  slack, and graph-arc normalization remain outside this Lean module.
- `GrandeFinale/C0PeriodicFirstMatchTarget.lean`: exact finite-set proof of
  Danny's #796 four-cell first-match union cap, with the component caps and
  cover supplied explicitly and the complete `c=0` parent kept outside scope.
- `GrandeFinale/C0PeriodicSingletonCertificate.lean`: exact recovery of an
  omitted pair from fixed first and third moments, disjoint powerset-certificate
  packing, the literal q128 singleton caps `34,137` and `12,598,400`, and the
  conditional fixed-singleton compiler for the `b=5,7` subtotal.
- `GrandeFinale/C0PeriodicF29ResidualOwner.lean`: low-block recovery for
  periodic locators, derivation of nonzero projective scale from the short
  nonzero left constant block, support-level residual ownership via locator
  injectivity, and the conditional 64-class compiler for the literal q64
  `f=29` cap `1,619,679,744`.
- `GrandeFinale/C0PeriodicF28ResidualPencil.lean`: support-level projective
  pencil parameter injectivity, common-base root packing, the exact residual
  owner cap 63, and the conditional q64 `f=28` compiler for
  `83,970,774,720`.
- `GrandeFinale/C0PeriodicF28TwoBlockCompiler.lean`: generic two-block
  truncation of periodic locators and recovery of both low coefficient-block
  equations from projective congruence modulo `X^a` when `2B <= a`.
- `GrandeFinale/C0PeriodicF28CanonicalBlocks.lean`: canonical Euclidean
  division of a support locator by `X^B`, with a lower-degree bound, exact
  upper degree, upper monicity, the deployed `32,768 + 30,833`
  specialization, and uniqueness.
- `GrandeFinale/C0PeriodicF28ScalarPencil.lean`: explicit scalar solution of
  the two block equations, direct projective-congruence-to-pencil normal form,
  and the `30,833` low-block degree cut from two distinct monic members.
- `GrandeFinale/C0PeriodicF28DerivedOwner.lean`: certificate compiler from a
  deduplicated literal two-block/projective family to the support-level pencil,
  including the singleton branch, the derived residual-owner cap 63, the exact
  q64 `f=28` target cap `83,970,774,720`, and its first-match composition.
- `GrandeFinale/C0PeriodicF28TargetCompiler.lean`: finite-image
  deduplication and representative selection from target-indexed two-block
  data, choice of scales on nonreference supports from existential projective
  witnesses, canonical reference-scale normalization, derived nonzero chosen
  scales, and the same exact residual, target, and first-match bounds.
- `GrandeFinale/C0PeriodicF28PairwiseCompiler.lean`: finite choice of a
  reference from a nonempty target family with pairwise projectivity on
  distinct residual supports, plus a separate empty-family branch requiring
  no inhabitant of the target type; it removes the designated-reference and
  reference-membership inputs while preserving the exact bounds.
- `GrandeFinale/ChallengeIntersection.lean`: exact finite-group
  translate-intersection averaging, linear-code received-line shear invariance,
  challenge-restricted MCA numerators, and the ceiling-density transfer from a
  supplied full-field bad-slope floor.
- `GrandeFinale/CollisionAwarePole.lean`: polynomial root-collision
  averaging, exact distinct-value ceiling, finite codeword representatives,
  simple-pole support semantics, the full-field MCA numerator compiler in
  `thm:collision-aware-pole` / equation (4.2), and its proper-challenge
  composition.
- `GrandeFinale/IdentityPrefixCollisionFloor.lean`: the exact
  coefficient-prefix specialization of the collision-aware compiler, with the
  literal `L_m` and `M(L_m)` ceilings from equation (4.3), plus its
  proper-challenge transfer.
- `GrandeFinale/QFourierTao.lean`: log-moment-to-Q reductions, including the
  finite bit-certificate inequality.
- `GrandeFinale/QEntropyInverse.lean`: deterministic atoms around the entropic
  inverse route, including the reverse moment/max-fiber inequality and
  Vandermonde rank rigidity.
- `GrandeFinale/LargestFiberMoment.lean`: exact largest-fiber normalized
  `q`-moment sandwich, its finite logarithmic lower bound, and the normalized
  Q-to-SP second-moment transfer.
- `GrandeFinale/ExactProfileCompiler.lean`: exact finite incidence double
  counting, residual moment payment with the full-slice mean, the literal
  natural floor in (FC1), and available/minimum first-match budgets in (FC2).
- `GrandeFinale/FirstMatchAddBack.lean`: ordered first-match
  disjointization, the exact finite family-union multiplier, full-slice
  overlap counting, and the weighted add-back formulas (AB1)--(AB3).
- `GrandeFinale/SubfieldConfinement.lean`: exact identification of a finite
  coefficient-vector base-domain RS code with the existing polynomial
  submodule, base-coordinate projection, same-support pair transfer, and MCA
  bad-slope confinement.
- `GrandeFinale/ExactPrefixList.lean`: the exact locator-prefix support/list
  correspondence, unique recovery of the full agreement support, and the
  no-extra-agreement clause from `prop:exact-prefix-list`.
- `GrandeFinale/PrefixPigeonhole.lean`: the explicit locator coefficient map,
  its equivalence with leading cancellation, and the literal natural-ceiling
  lower bound for both a prefix fiber and its complete polynomial list.
- `GrandeFinale/PrefixRigidityPacking.lean`: exact Johnson spheres and ball
  volume, locator-prefix distance at least `w+1`, pairwise ball disjointness,
  and both multiplication and natural-division forms of equation (4.4).
- `GrandeFinale/ExactListLine.lean`: the quotient explaining polynomial,
  exact agreement-set preservation, and the same-field bijection between a
  complete finite polynomial list and the MCA-bad slopes of a fixed
  separating simple-pole line.
- `GrandeFinale/ExactPrefixRay.lean`: the same-field specialization from an
  explicit complete locator-prefix fiber to the full MCA-bad slope set,
  including direct image equality, separating-pole cardinality, and exact
  retained agreement supports.
- `GrandeFinale/ExactPrefixRayUniqueness.lean`: reconstruction of the listed
  polynomial from an arbitrary degree-bounded explanation of its selected
  line point and uniqueness of the exact support/explaining-polynomial
  witness.
- `GrandeFinale/SeparatingPole.lean`: the exact unordered-pair root product,
  its `k * choose L 2` degree bound, off-domain separating-pole existence, and
  the resulting same-field prefix-fiber bad-slope cardinality realization.
- `GrandeFinale/ScalarExtensionListLine.lean`: interpolation descent of every
  ambient degree-bounded explanation to a base-field polynomial, completeness
  of the mapped base list, and the full extension-field separating-pole image
  and cardinality theorem.
- `GrandeFinale/PrefixChallengeFloor.lean`: exact composition of the
  extension-field prefix-fiber realization with the proper-challenge
  translate-intersection compiler, including the prescribed-fiber floor and
  literal nested-ceiling largest-fiber corollary.
- `GrandeFinale/QPrimitiveCollision.lean`: collision-tuple identities,
  trade-formulation kernels, low-support exclusion, and prefix-collision
  rigidity.
- `GrandeFinale/QFiniteTables.lean`: the four rows of `prop:q-exact-target` and
  `prop:q-moment-order-floor`, including exact integer inputs, budget-ratio
  truncations, printed-margin rounding, and the real-average versus
  ceiling-average moment-floor convention split.
- `GrandeFinale/SyndromeLine.lean`: supported-error syndrome spans, the exact
  support-wise syndrome-line normal form, fixed-support uniqueness,
  deduplicated finite-family incidence, and the exact MCA/syndrome numerator
  equality for a surjective syndrome map.
- `GrandeFinale/RSParityKernel.lean`: barycentric weighted Vandermonde columns,
  at-most-`R` column independence, parity-map surjectivity, Lagrange moment
  annihilation, and exact identification of the parity kernel with the
  injective Reed--Solomon evaluation code.
- `GrandeFinale/RSSupportHyperplanes.lean`: exact identification of
  supported-error syndrome images with weighted-column spans, their dimensions,
  codimension-one functional kernels, and injectivity across exact `(R-1)`
  supports.
- `GrandeFinale/RSExactSupportUpper.lean`: exact reduction from threshold
  witnesses to exact-cardinality supports and the literal full-field
  `choose |D| a` support-atlas upper bound for injective Reed--Solomon codes.
- `GrandeFinale/RSFirstAdjacentRow.lean`: exact Reed--Solomon composition of
  the parity kernel, support hyperplanes, separating line, and support upper
  bound, proving the full-field AD1 numerator equality.
- `GrandeFinale/RSFirstAdjacentThreshold.lean`: exact first-safe proposition,
  its uniqueness, and both literal target-budget implications in AD2.
- `GrandeFinale/ExactAdjacentRow.lean`: exact finite avoidance of the `M`
  syndrome hyperplanes and `choose M 2` collision hyperplanes, followed by the
  generic syndrome-secant and support-wise MCA lower-bound compiler.
- `GrandeFinale/ProfileEnvelopeWindow.lean`: exact rational exponent algebra for
  the corrected per-folding identity-dominance windows, including finite-family
  intersection/union and the positive-crossing no-field-drop characterization.
- `GrandeFinale/BC.lean`: theorem-level reductions around the BC split-pencil
  ledger, including one-parameter moving-root and saturation kernels.
- `GrandeFinale/SP.lean`: theorem-level reductions around the SP ledger,
  including quotient pullback, coefficient-scale, top-stratum, and Q-implies-SP
  kernels.  The Q-implies-SP statement retains the manuscript's exact diagonal
  subtraction, both before and after normalization.
- `GrandeFinale/Frontier.lean`: composite-prefix descent, row-sharp Q atom
  scaffolding, finite BC chart-audit kernels, and extension-cell finite
  comparisons.

## Formalized Scope

The files formalize reusable theorem-level kernels and arithmetic facts from the
Grande Finale program.  They do not prove the full RS-MCA threshold theorem.

The periodic singleton module discharges the algebraic and finite-packing part
of the q128 `b=5,7` component used by the C0 first-match target.  Its
`Q128OccupancyCertificate` deliberately keeps the fixed-singleton Hahn caps and
the cover by the 128 quotient-constant fibers as explicit inputs.  It does not
formalize the frozen Ruby replay, pay `b>=9`, or promote a complete `c=0`
parent bound.

The periodic `f=29` module proves the algebraic residual-support owner and the
64-cell union arithmetic.  Its `F29ProjectiveRayCertificate` deliberately
keeps the deployed locator decomposition, existential pairwise projective
congruences, quotient-constant classification, and the fixed-residual local
Hahn cap as explicit inputs, but derives projective-scale nonzeroness rather
than requiring it in every witness.  It does not construct the literal
deployed stratum, prove the `f=28` component, or promote a complete `c=0`
parent bound.

The periodic `f=28` residual-pencil module proves that a certified pencil of
63,601-point residual supports in the deployed 2,097,152-point ambient set has
at most 63 members when its direction is `X^32,768 U` with `U(0) != 0` and
`deg U <= 30,833`.  It then checks the 63-by-64 local-cell compiler and
replaces the final opaque component
cap in the first-match theorem.  The separate two-block compiler now proves
that projective congruence modulo the deployed monomial forces both low
coefficient-block equations after the same scaling.  The scalar-pencil module
solves those equations when both quotient constants are nonzero and proves the
`30,833` degree cut when a normalized family has at least two distinct monic
members with the deployed upper-block degree bound.  In the at-least-two-member
branch, the derived-owner compiler now constructs the support-level pencil
certificate from a supplied deduplicated family of literal two-block
decompositions and projective congruences.  It obtains the owner cap 63 in all
cases.  Its outer compiler recovers the exact q64 `f=28` target cap and PR
#819 first-match payment from supplied scalar classes and fixed-cell caps.  The
target-indexed compiler now forms the distinct-support image and selects one
representative per support, always retaining the designated reference target;
no duplicate-data coherence is needed.  The canonical-block module now derives
each locator decomposition, the lower-degree bound, exact upper degree, and
upper monicity directly from the residual support.  Constructing the
target-indexed quotient polynomials and existential projective relations from
the canonical stratum remains explicit.  The compiler chooses the
scales for nonreference supports, uses the coefficient-zero equation to prove
them nonzero, and normalizes the reference scale to one.  The fixed-residual
Hahn cap and the first-match cover remain explicit inputs.  These modules do
not treat
`f<=27`, general monic moduli, or a complete `c=0` parent.

The main remaining target is Q:

```text
primitive entropic inverse theorem / row-sharp prefix-fiber bound
```

The Lean files currently formalize deterministic pieces consumed by this target
and consequences that follow after Q is supplied.  The printed finite-Q table
data and its elementary integer relations are now pinned and kernel-checked.
This is not a proof of the row-sharp Q atom: the bit margins and moment floors
remain audited inputs rather than formal derivations of transcendental
logarithms or enormous binomial values.  The entropy-scale inverse
Littlewood-Offord / Balog-Szemeredi-Gowers step remains open.

The largest-fiber-moment module supplies the exact finite compiler arithmetic
in `lem:largest-fiber-log-detail` and `lem:q-to-sp-detail`. Its real-valued
finite-fiber statements strictly include the manuscript's nonnegative integer
case; sequence-level asymptotic notation remains outside this finite module.

The exact-profile compiler proves the finite arithmetic implications in
`thm:exact-finite-profile-compiler`. It treats the witness-exhaustive atlas,
the exact support-pair identity, and the certified incidence relation and
degrees as explicit inputs. It does not assert that those structural inputs
exist for an unrestricted row. Challenge-set intersection and the adjacent
unsafe/safe threshold comparison remain delegated to the package's existing
challenge and threshold results.

The first-match add-back module proves the finite disjoint-union identity
before summing cell budgets and records the exact overlap loss for full profile
slices. Its family-size-times-budget theorem is the finite combinatorial core
of `lem:profile-summation`; the sequence-level `e^{o(n)}` bookkeeping
remains outside the module. A witness-exhaustive atlas and the individual
profile payments remain explicit inputs.

The subfield-confinement module proves `thm:subfield-confinement-full` for an
arbitrary field extension modeled by `Algebra B F`. The evaluation domain and
received line are base-valued, while the code itself is the existing
extension-field `CollisionAwarePole.rsEval`. No finiteness or
finite-dimensionality is needed for same-support transfer; finite fields enter
only in the bad-slope cardinality corollary.

The exact-prefix-list module formalizes the algebraic bijection in equation
(4.1). It represents a fixed locator prefix by the equivalent leading-term
cancellation condition `degree (U - locator S) < K`, and proves that every
listed polynomial has exactly `m` agreements and a unique support. The
explicit coefficient-vector map, its pigeonhole fiber-size lower bound, and
the later separating-pole line bijection remain separate from this module.
`PrefixPigeonhole` supplies the first two as a separate layer, including the
literal ceiling rather than a floor-division relaxation, while `ExactListLine`
supplies the same-field fixed-pole line bijection. `ExactPrefixRay` supplies
the corresponding direct prefix-fiber specialization.
`PrefixRigidityPacking` supplies the independent finite packing limitation in
`prop:prefix-rigidity-full`; its asymptotic `e^{o(n)}` estimate remains outside
the finite module.
`ExactPrefixRayUniqueness` supplies
arbitrary-explanation witness uniqueness and occupancy one for a supplied
separating pole, while `SeparatingPole` supplies that pole under the exact
same-field equation-(4.6) budget. `ScalarExtensionListLine` supplies
base-to-extension interpolation descent, ambient-list completeness, and the
direct extension-field prefix cardinality realization.

The syndrome-line module is independent of Q.  It proves the generic
linear-code compiler behind `prop:syndrome-line-normal-form` and
`thm:syndrome-secant-exact` in the frontiers paper. The RS parity-kernel module
supplies its weighted Vandermonde parity-check construction and exact kernel
identification, while the support-hyperplane module supplies the distinct
`(R-1)`-support kernel family. The exact-support-upper module supplies the
threshold-to-exact-cardinality reduction and the resulting support-atlas upper
bound, and the exact-adjacent-row module supplies the field-separation and
generic syndrome compiler. The first-adjacent-row module composes these pieces
to prove AD1 with the literal binomial constant and field-size gate. The
first-adjacent-threshold module then derives both AD2 implications on the exact
integer agreement grid.

The collision-aware-pole and challenge-intersection modules are independent
of Q and formalize complementary parts of the frontiers paper's simple-pole
route. `CollisionAwarePole` proves the exact equation-(4.2) full-field floor
from a supplied finite dimension-`k+1` Reed--Solomon codeword list, while
`ChallengeIntersection` transfers a supplied full-field floor to a proper
challenge set after a received-line shear. The direct composition is exported
as `collisionAwarePole_challenge_of_codewordList`.
`IdentityPrefixCollisionFloor` selects an exact-size heavy prefix sublist and
exports the literal equation-(4.3) specialization and its challenge transfer.
The prefix-list construction
and pigeonhole floor are supplied by `ExactPrefixList` and
`PrefixPigeonhole`, and `ExactListLine` proves the exact same-field fixed-pole
list--line conversion. `ExactPrefixRay` composes these layers for a supplied
same-field pole and proves exact bad-slope/fiber cardinality when it separates
the list. `ExactPrefixRayUniqueness` proves that every selected slope has a
unique exact support/explaining-polynomial witness. A scalar-extension
composition and its ambient-list completeness/descent argument are now
supplied by `ScalarExtensionListLine`, while `SeparatingPole` supplies the
exact existence bound. `PrefixChallengeFloor` now exports the finite
proper-challenge composition, with the coefficient-pigeonhole ceiling nested
inside the exact challenge-density ceiling under a uniform equation-(4.6)
field-size budget. This closes that finite compiler spine, but the later
asymptotic parameter translation, row-sharp Q input, and adjacent threshold
comparison remain outside it; the module alone is not the full asymptotic
`prop:simple-pole-lower` conclusion.

The profile-window module is also independent of Q. It proves exponent-level
dominance only after `h`, `s`, and every actual `(c,lambda)` pair are supplied.
QR6/QR8 normalization, folding-family exhaustiveness, (A2)/(A4)/(A7), and the
bridge to the full profile envelope remain explicit outside inputs.

## Build Note

Do not run `lake build` casually in this repository. Build only with the
pinned Lean/Mathlib versions and matching precompiled Mathlib cache. A full
pinned default build on 2026-07-14 completed successfully with 8050 jobs,
including `GrandeFinale.CollisionAwarePole` and the newly integrated
statement-target modules. The compatibility repairs needed for that build
change syntax and required typeclass/scope declarations only; they do not prove
the targets that remain explicitly marked unproved.
