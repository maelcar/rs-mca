# KoalaBear row-sharp Route-D pivot obstruction

STATUS: COUNTEREXAMPLE

## Claim

The currently checked Route-D packets do not prove

```text
|G_gen(z)| + |D_prim(z)| <= 67472 * 2130706433
                          = 143763024447376.
```

This note gives a counterexample to the proposed exhaustive marked-incidence
and pivot-routing closure, in the sense requested for this lane. It does not
give a primitive KoalaBear target above the deployed bound. The deployed
support certificate remains open.

There are two independent obstruction floors:

1. a vanishing fixed-subgroup RIM pivot is not legally consumable by the
   integrated `DEEP_MCA_RANK_DROP` owner without a new marked adapter;
2. the printed nonvanishing-pivot dichotomy independently leaves a primitive
   weighted SP/Padé count `N_WSP_full(z)` without a finite payment.

The common core `G` remains part of every marked key.

## Exact named-deletion audit

The singleton top-seam certificate lists

```text
generated_field
quotient_planted
sparse_pade_hankel
m1_window_shadow
rank_drop_pivot
bc_chart
sp_shift_pair
extension_slope
```

only as the `examples` field of one aggregate priority-zero item named
`earlier_global_first_match_branches`. This packet verifier checks that exact
tuple. The upstream builder checks only the length of the surrounding order
and does not implement these eight items as global predicates on marked
supports.

Consequently the phrase after the exact named first-match deletions does not
yet denote a machine-checked residual set. In particular, the finite witness
below is not claimed to survive an honest generated-field projector or the
M1-window-shadow projector. A future proof must first print those predicates
and prove their disjoint first-match realization.

## Vanishing-pivot owner boundary

The reduction packet contains an exact singular roots-of-unity RIM
specialization over `F_17`. Its displayed `6 x 6` matrix annihilates the
nonzero vector

```text
(2,14,1,3,0,3).
```

Thus fixed-subgroup pivot vanishing is nonempty and cannot be removed by a
generic-nonsingularity assertion.

The integrated rank-drop owner has a different theorem object. It counts
distinct finite MCA-bad slopes of one received pair for which the field-native
Hankel pencil `M_A(gamma)` has row rank below `t`. Its checked contract says

```text
requires_actual_bad_incidence = true
raw_algebraic_rank_drop_paid  = false
per_support_charge            = false
per_pivot_charge              = false
scope                         = FIRST_MATCH_GLOBAL_ONCE.
```

No checked theorem currently constructs an actual `(f,g,gamma)` incidence
from a marked Route-D RIM object, identifies the RIM minor with the deployed
Hankel rank predicate, or controls the support fiber while retaining `G`.
Charging a raw vanishing pivot to this owner would therefore change both the
unit and the scope of the proved bound.

A legal adapter must:

1. take the full marked key, including `G`;
2. construct an actual bad slope and explaining codeword;
3. prove `rank_F M_A(gamma) < t`;
4. prove a bounded-fiber or injective support transfer;
5. apply the global owner only once.

Until that adapter exists, the vanishing family is unrouted.

## Large signed-defect folding witness

The following exact finite example refutes the bare implication that a
nonvanishing pivot gives a unique marked `(r,c)` charge.

Work over `F_17` with domain `F_17^*`, support size `j=8`, prefix depth
`w=2`, top seam `r=3`, and locator target `z=(1,9)`. Its multiplicative
target stabilizer is trivial. Take the marked base

```text
B = (1,3,5,9,10,11,13,15).
```

Two supports in the same top-seam cell `c=4` are

```text
S_L = (1,3,4,5,6,7,9,15)
G_L = (1,3,5,9,15)

S_R = (1,2,5,8,9,13,14,15)
G_R = (1,5,9,13,15).
```

Their depth-three locator prefixes are both `(1,9,14)`, while the base
prefix is `(1,9,10)`. The folding defects of `B,S_L,S_R` are `8,8,4`.
Thus this is a genuinely large-defect transfer, not a zero-defect descent.

The cross-pair signed defect is

```text
mu = -[2] + [3] + [4] + [6] + [7] - [8] - [13] - [14].
```

It has the exact invariants

```text
|supp(mu)|                 = 8 >= r+3
(mu_0,mu_1,mu_2,mu_3,mu_4) = (0,0,0,0,10)
det V_(2,3,4,6)            = 14 mod 17
multiplicative stabilizer  = {1}.
```

Hence the object is not an extension-slope object, not a vanishing-pivot
object, not a BC corank-one object, and not quotient-periodic. It has the
checked numerical invariants of the full-rank primitive-by-stabilizer
weighted SP/Padé alternative before the unimplemented structural filters.
Since `G_L != G_R`, forgetting the common-core mark merges two different
supports into one cell.

The complete toy primitive fiber has size `49`, below the toy budget
`3 * 17 = 51`. This finite example therefore does not refute even its toy
numerical inequality. It refutes only the bare pre-filter implication from a
nonzero pivot to a unique marked row cell. Independently, the source packet
records `N_WSP_full(z)` as an unpaid terminal count after all structural
filters are realized.

## Theorem-shaped conclusion

**Theorem (current-interface Route-D obstruction).** The checked hypotheses
in the row-sharp prefix reduction and singleton top-seam packets do not imply
the proposed two-way closure

```text
vanishing pivot    -> DEEP_MCA_RANK_DROP payment
nonvanishing pivot -> unique marked row-cell payment.
```

The first implication lacks an actual-incidence, rank-identification, and
marked-fiber adapter. Before the unimplemented structural filters, the second
bare implication is refuted by the exact primitive-by-stabilizer collision
above. The source independently records the post-filter weighted count as
unpaid. Therefore the new obstruction floor is

```text
RIM_TO_DEEP_MCA_MARKED_SUPPORT_ADAPTER
+ executable exact first-match projectors
+ finite bound for N_WSP_full(z).
```

The deployed support inequality is `REDUCED_NOT_PROVED`, not false.

## Nonclaims

- No primitive KoalaBear target above `143763024447376` is exhibited.
- The finite witness is not asserted to survive projectors that are not
  executable in the checked packet.
- No per-pivot or per-support charge is imported from the slope owner.
- No low-moment, Johnson-packing, mode-at-null, image-only, or zero-defect
  shortcut is used.
- No submission-facing theorem is changed.

## Reproduction

```bash
python3 experimental/scripts/verify_kb_rowsharp_route_d_pivot_obstruction.py --check --self-test
cd experimental/lean/kb_rowsharp_route_d_pivot_obstruction
lake build
```

The verifier recomputes the finite fiber, marked cores, folding defects,
moments, pivot, stabilizer, singular RIM kernel, owner-contract fields, named
deletion aggregate, deployed product, and fail-closed mutations. The Lean
companion kernel-checks the deployed product and singular RIM witness, while
leaving the full support certificate as an explicitly unproved theorem target.
