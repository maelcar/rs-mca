# Lean correspondence: primitive Boolean fibers and energy split

## Status

PROVED for the concrete finite Boolean-family semantics, exact difference and
closure definitions, residual-prefix construction, low/high moment partition,
and the arithmetic consuming a direct Boolean-energy bound.  CONDITIONAL for
the sharp external energy theorem and the Sidon/low-energy payment.  The older
BSG/quasicube route is retained as an explicit alternative.

## Independent promotion audit

No statement from this packet has been moved into
`experimental/asymptotic_rs_mca_frontiers.tex`.  This section audits the new
batch consumer-backward, as requested by the maintainer.

Verdicts are literal: `NO ISSUE` means that the printed hypotheses match the
consumer; `FIXED` records a corrected promotion-ready formulation; `OPEN
GAP` is a missing input rather than a proved conclusion; and
`COUNTEREXAMPLE_NEW_FLOOR` records a counterexample to an asserted bridge or a
newly certified finite floor.

### PR #558: primitive-profile character frame

The finite frame theorem `(CF1)` is sound and uses the same full-slice image
normalization as `def:primitive-q` and `thm:primitive-q`.  It is a
conditional certificate, not an unrestricted proof of primitive Q.  The
large-image and scale-junction rows below incorporate the independent
cross-check in [PR #608](https://github.com/przchojecki/rs-mca/pull/608) and
the follow-up impossibility result in
[PR #609](https://github.com/przchojecki/rs-mca/pull/609).

| Claim or hypothesis | Verdict | Audit |
| --- | --- | --- |
| `(CF1)` frame inequality | `NO ISSUE` | The Gram matrix is `T T*`, and the normalized indicator of a nonempty fiber gives `|A||F_z|/M <= ||K_A||_op`; an empty fiber is trivial. |
| Full-slice versus residual normalization | `NO ISSUE` | #558 uses `L=|Phi(Omega)|`, `barN=M/L`, and residual inclusion.  The TeX consumer uses the full image of `Omega_N^0`, its full-slice average, and `O_N^circ subset Omega_N^0`. |
| Effective affine target | `NO ISSUE` | Characters are evaluated after translation by the affine base point and on the effective difference span, as in `(EF2)`--`(EF4)`. |
| Whole-`(EFP)` substitution: large-image output | `COUNTEREXAMPLE_NEW_FLOOR` | `(EFP)` also supplies `L >= exp(-o(N))A_eff`, but the frame supplies only the max-fiber half.  PR #609 proves that `(CF1)+(CF2)` alone do not imply the image half: PR #558's exact block-parabola witness has `M=L=p^k`, `A_eff=p^(2k)`, and `K_A=I`, so both frame hypotheses hold while `L/A_eff=p^(-k)`.  A consumer replacing all of `(EFP)/(MI)+(MA)` must separately supply a span-normalized `(EF4)/(EFP)` input, with #539's Gap-1 corollary converting it; assume `(FI)` proper; or prove a phase-sensitive Gap-1 estimate. |
| Asymptotic scale pin | `OPEN GAP` | #558 writes `exp(o(N))` without identifying `N` with the TeX leaf's active-coordinate scale `|T|`.  Promotion needs that explicit pin. |
| Nonempty source slice and row index in `(CF6)` | `FIXED` | A promotion-ready statement must say `Omega != empty` and write `max_{gamma in A}`.  The fixed-density consumer supplies nonemptiness, but #558 leaves it implicit. |
| Source-specific `(CF2)` | `OPEN GAP` | Neither #558 nor the TeX constructs `A_lambda` with `|A_lambda| >= exp(-o(N))L_lambda` and `||K_A||_op <= exp(o(N))` uniformly on semantic many-shell profiles. |
| Independent-set bound `(CF4)` | `NO ISSUE` | Maximum degree at most `|Mfrak|-1` gives an independent set of size at least `|G^|/|Mfrak|`; no floor factor is lost. |
| Major-difference packing `(CF5)` | `OPEN GAP` | Its cardinality bound is explicitly not proved for semantic profiles. |
| `(CF6)` plus Gershgorin | `NO ISSUE` | With diagonal entries one, the off-diagonal row-sum bound gives the required operator norm. |
| Effective `(MI)` implies `(CF6)` as printed | `COUNTEREXAMPLE_NEW_FLOOR` | The bridge silently needs `{1} union M_eff subset Mfrak` and `Mfrak=Mfrak^{-1}`, equivalently `A^{-1}A - {1} subset m_eff`.  Without containment, `(MI)` need not control any Gram difference. |
| Block-parabola example | `NO ISSUE` | It is the exact witness deciding the magnitude-only large-image question: `(CF1)+(CF2)` hold with constant one while `L/A_eff` is exponentially small.  It proves an abstract interface separation only; #558 explicitly does not claim semantic residuality. |

The missing `(MI)` containment is material.  Let `G=F_2^d` and

```text
mu = (1/2) delta_0 + (1/(2d)) sum_i delta_{e_i}.
```

The effective span is all of `G`.  Declare every nonidentity character major,
the minor set empty, and take `Mfrak={1}`.  Then `(MI)` is vacuous and
`(CF5)` holds, but the independent set is the whole dual and an off-diagonal
Gram row has absolute mass

```text
sum_{y != 0} |hat_mu(y)| = 2^(d-1)-1.
```

Thus `(CF6)` fails exponentially.  The corrected sufficient bridge is

```text
{1} union M_eff subset Mfrak,   Mfrak = Mfrak^{-1},
```

followed by the printed packing bound on this symmetric hull.

### PR #592: F2 effective energy dichotomy

The symbolic BSG/quasicube composition is correct, but its three numerical
rows are scenarios rather than imported theorems.  The sentence that the F2
branch is closed “with printed constants” is therefore not promotion-ready.

| Claim or hypothesis | Verdict | Audit |
| --- | --- | --- |
| Symbolic `BSG(c1,e1,c2,e2)` composition | `NO ISSUE` | BSG plus Boolean difference growth gives `|A| <= c1 c2^2 K^(e1+2e2)` for nonempty `A subset {0,1}^d`. |
| Quasicube input | `NO ISSUE` | The cited theorem has finite nonempty `P,Q subset Z^d` and Boolean `U`; taking `P=-A`, `Q={0}`, and `U=A` is valid. |
| Three numerical rows | `OPEN GAP` | No cited theorem supplies any displayed constant tuple.  The verifier checks their arithmetic, not their truth. |
| `n=2^41`, `|A|>n^3` consumer | `OPEN GAP` | This is a generic prize-maximum b2 row, not a parameter supplied by the active asymptotic theorem.  The deployed CAP25 Q row has support-domain size `n=2^21`; promotion must name the exact residual object and row. |
| Published explicit BSG row | `FIXED` | Reiher--Schoen Theorem 1.2 gives `c1=(1-epsilon)^(-1)`, `e1=1/2`, `c2=2^33 epsilon^(-9)`, `e2=4`.  Above `2^123` its limiting deficit is only `(123-85)/8.5 = 4.470588...` bits; at `2^63` its constant cost already exceeds the budget. |
| Sharp direct Boolean-energy input | `COUNTEREXAMPLE_NEW_FLOOR` | The published inequality `E(A) <= |A|^(log_2 6)` applies directly and supersedes the BSG table.  It gives `51.049612...` deficit bits above `2^123` and `26.147362...` above `2^63`, with constant one. |
| Lean-certified rational-power consequence | `NO ISSUE` | This package assumes only `E(A)^3 <= |A|^8` and proves `|A|<K^3`, yielding exact 41-bit and 21-bit high-energy exclusions at those two rows.  It does not formalize the sharper irrational exponent. |
| Few-structured-pieces consequence | `NO ISSUE` conditionally | If a model separately proves `E(A) >= |A|^3/c^2`, the sharp theorem strengthens the generic-row exclusion from `c <= 2^3.8` to `c < 2^25.5248...`. |

Primary sources checked:

- [de Dios Pont--Greenfeld--Ivanisvili--Madrid, *Additive Energies on
  Discrete Cubes*](https://arxiv.org/abs/2112.09352), Theorem 1 at `k=2`;
- [Reiher--Schoen, *Note on the Theorem of Balog, Szemerédi, and
  Gowers*](https://arxiv.org/abs/2308.10245), Theorem 1.2;
- [Green--Matolcsi--Ruzsa--Shakan--Zhelezov, *A Weighted
  Prékopa--Leindler Inequality and Sumsets with
  Quasicubes*](https://arxiv.org/abs/2003.04077), Theorem 1.1.

The direct energy theorem's hypotheses match the TeX consumer exactly:
`F_s` is a finite set of Boolean incidence vectors embedded in `Z^T`; no
additional fixed-weight, density, or nonempty hypothesis is needed.  Its
repeated-difference convention is exactly Theorem 1 at `k=2`.

There is one source typo to repair before promotion.  The TeX defines energy by
`a-b=c-d` but then says the forced fourth point is `d=a-b+c`.  The displayed
equation actually forces `d=b-a+c`.  The closure-probability identity remains
correct after swapping the two dummy variables `c,d`; the Lean declarations
`ClosureWitness.swapLast`,
`additiveEnergy_eq_repeatedDifferenceWitnesses`, and
`mem_repeatedDifferenceWitnesses_iff` certify that permutation.  This audit
does not edit the active TeX.

### Promotion decision

- Do not promote #592's three-row table.
- Cite #558 only as a conditional max-fiber frame certificate after the
  major-containment, nonempty/index, and scale-pin repairs.  It does not replace
  the large-image half of `(EFP)`: PR #609 proves that half is unavailable from
  the #558 magnitude frame as stated.  Every consumer must separately supply a
  span-normalized `(EF4)/(EFP)` input, with #539's Gap-1 corollary converting
  it; assume `(FI)` proper; or prove a phase-sensitive Gap-1 estimate.
  Source-specific `(CF2)`, `(CF5)`, and semantic packing remain open.
- Route the high-energy Boolean branch through the external sharp theorem.
  This Lean packet certifies only its rational-power consequence
  `E(F)^3<=|F|^8 => |F|<K^3`, not the full `51.049612...`-bit threshold.
- The remaining research frontier is the low-energy/Sidon payment:
  source-specific packed frames or an equivalent signed-cancellation estimate.

## Source

The source is `experimental/asymptotic_rs_mca_frontiers.tex`, especially the
primitive Boolean slice and Sidon/energy split surrounding
`prop:no-high-energy`.  The Lean modules are:

- `experimental/lean/asymptotic_spine/AsymptoticSpine/BooleanFiber.lean`;
- `experimental/lean/asymptotic_spine/AsymptoticSpine/NoHighEnergy.lean`;
- `experimental/lean/asymptotic_spine/AsymptoticSpine/PrimitiveBoolean.lean`.

## Statement-to-declaration map

| Finite step | Lean declaration | Status |
| --- | --- | --- |
| A duplicate-free fixed-weight family in `{0,1}^n` | `BoolFamily` | PROVED concrete representation |
| Integer embedding and exact ordered-pair difference set | `bitEmbed`, `bitDifference`, `BoolFamily.differenceSet` | PROVED definitions |
| A realized pair `(s,d)` has an actual Boolean family witness | `BoolFiber` | PROVED semantic predicate |
| Nonempty families have nonempty difference sets; in particular `(2,0)` is impossible | `differenceSet_length_pos_of_points_ne_nil`, `not_boolFiber_two_zero` | PROVED |
| `a-b=d-c` iff the forced fourth point satisfies `d=a-b+c` in the integer embedding | `bitDifference_eq_iff_embed_eq_closure` | PROVED |
| Each ordered triple admits at most one closing fourth point | `closureCandidates_length_le_one` | PROVED |
| Exact closure/repeated-difference energy and `E(F)<=|F|^3` | `additiveEnergy`, `additiveEnergy_le_card_cubed` | PROVED |
| The complete fixed-weight slice, routed residual, and prefix key | `PrimitiveBooleanLeaf` | EXPLICIT FINITE DATA; fullness is certified by `full_complete` |
| A residual prefix class is a sublist of the full prefix class | `residualPrefixFiber_sublist_fullPrefixFiber` | PROVED; specializes existing residual filtering |
| Full and residual prefix classes are semantic Boolean fibers | `fullFiberFamily_isBoolFiber`, `residualFiberFamily_isBoolFiber` | PROVED |
| Closure energy is exactly the standard `a-b=c-d` witness count | `additiveEnergy_eq_repeatedDifferenceWitnesses`, `mem_repeatedDifferenceWitnesses_iff` | PROVED |
| Low/high energy tests partition the ordinary finite moment exactly | `ordinaryFiberMoment_eq_low_add_high` | PROVED |
| Moment excess forces a large high-energy member | `exists_large_highEnergyFiber_of_moment_excess` | PROVED exact finite contrapositive |
| `E(F)^3<=|F|^8` plus high energy forces `|F|<K^3` | `count_lt_cube_of_energy_cubed_le_count_eighth`, `booleanFiberStat_count_lt_cube_of_sharpEnergy` | PROVED exact arithmetic; CONDITIONAL on the external sharp-energy input |
| The direct high-energy moment costs at most `length*(K^3-1)^q` | `primitiveBooleanMomentUpper_of_sharpEnergy` | PROVED exact compiler; CONDITIONAL on the external sharp-energy input |
| BSG plus quasicube caps every high-energy member by `K^(3C)` | `booleanFiberStat_count_le_of_bsg_quasicube` | CONDITIONAL alternative on both named inputs; reuses `no_high_energy_bound` |
| The ordinary moment is paid by the low-energy term plus the high-energy cap | `primitiveBooleanMomentUpper` | CONDITIONAL on BSG and quasicube |
| A supplied low-energy/Sidon budget closes the finite compiler | `primitiveBooleanMomentUpper_of_lowEnergyPayment` | CONDITIONAL on all three named inputs |

## Scope guard

All Boolean operations are performed after the coordinatewise embedding into
`Vector Int n`; no characteristic-two cancellation is used.  The energy is the
finite count of ordered quadruples satisfying a repeated-difference equation,
represented through its equivalent forced-closure form.  Duplicate-free point
lists ensure that a fixed ordered triple contributes at most one fourth point.

`PrimitiveBooleanLeaf.full_complete` is a certificate that its list is the
entire fixed-weight slice.  The routed residual is allowed to delete points,
but it must be a displayed sublist.  Filtering by a prefix key therefore gives
a concrete residual `BoolFamily`; it does not assert that the residual remains
the whole prefix class.

The module deliberately reuses the existing exact finite APIs in `Moment.lean`,
`EffectiveClosure.lean`, and `NoHighEnergy.lean`.  It does not prove the sharp Boolean-energy theorem, BSG,
quasicube growth, the low-energy/Sidon payment, a large-fiber-to-high-energy
implication, max-fiber control, C9, an asymptotic `o(n)` estimate, a character
frame theorem, or profile-atlas exhaustiveness.

The companion note `boolean_energy_cubed_direct.md` now gives a self-contained
mathematical proof of the weaker rational-power input
`E(F)^3 <= |F|^8` consumed by `hsharp`.  The Lean declaration remains
conditional until that proof is translated into the kernel; the sharper
`log_2 6` exponent remains an external published theorem.

## Build and trust audit

From `experimental/lean/asymptotic_spine/`:

```text
lake build
```

The package is stdlib-only on Lean 4.31.0.  The selected `#print axioms` checks
report only Lean's standard `propext`, `Quot.sound`, and `Classical.choice`.
There is no `sorryAx`, `sorry`, `admit`, `native_decide`, or added axiom.
