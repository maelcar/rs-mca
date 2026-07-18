# Rank-one admission interface audit

## Claim

This packet audits the conclusion of
`experimental/notes/thresholds/rank_one_greedy_adequacy.md` that omega-capped
greedy emission has no remaining mathematical obligation and needs only a
grammar-acceptance decision.

The capped accounting theorem is correct.  It is not a profile payment.  Its
adequacy proof is the universal Walsh triangle inequality, valid for every
function on a Boolean cube without a source chart, owner, algebraic precursor,
or slope projection.  A separate source-to-cell and distinct-slope theorem
therefore remains necessary.

## Status

```text
rank_one_greedy_adequacy.md, Theorem T4:        NO ISSUE / PROVED
omega_sound_emission_floor.md, statement S4:   NO ISSUE / PROVED LOCALLY
structure-specific reading of T4 adequacy:     OPEN GAP / TYPE MISMATCH
grammar-only wording in the #824 consumer:     OPEN GAP / FIXED HERE
#818/#820/#827/#842 related wording:            OPEN GAP / FIXED IN FOLLOW-UP
source-to-verifier correspondence:             BOUND IN FOLLOW-UP
hard input 2 and the ray interface:             OPEN
```

The correction changes no Walsh identity, rank-one product formula, finite
scan, soundness cap, or adequacy computation.  It changes only what those
facts are allowed to certify at the compiler interface.

## Governing payment interface

The governing frontiers manuscript fixes the relevant type:

- its glossary defines a payment as a proved distinct-slope bound at the
  relevant profile scale;
- `def:profile-cell` requires an actual realized witness cell and boundary
  data;
- `def:first-match` defines its actual first-match slope projection
  `Z_i^circ`;
- `def:profile-payment` requires a certified enumerative bound

  ```text
  |Z_i^circ| <= U_i <= exp(o(n)) (1+barN_i).
  ```

That definition explicitly says constructibility alone is not payment.
Condition `(A4)` separately requires effective MI+MA or a direct
image-normalized Sidon/Fourier moment payment.  Condition `(A6)` separately
requires `(RC)` or a direct distinct-slope theorem.  Moreover,
`def:sidon-paid-cell` warns that even a Sidon moment payment is not itself a
first-match distinct-slope payment.

The exact-threshold manuscript says the same thing after
`prop:partial-occupancy-fourier`: support add-back does not bound the
nontrivial Fourier terms, realized boundary image, or slope projection.

## Universal capped-Walsh lemma

Let `h` be any real function on `{0,1}^m`.  With normalized Walsh
coefficients

```text
hat_h(D) = 2^(-m) sum_e h(e) chi_D(e),
h(e) = sum_D hat_h(D) chi_D(e),
```

the triangle inequality gives, pointwise,

```text
|h(e)| <= sum_D |hat_h(D)|.
```

Summing over the `2^m` cube points gives

```text
sum_D 2^m |hat_h(D)|
  >= sum_e |h(e)|
  >= sum_e h(e)_+ .                                (W1)
```

Therefore a schedule that visits Walsh coefficients in any order and caps
its cumulative credit at `sum_e h(e)_+` is:

1. sound by definition, because it never exceeds the cap; and
2. adequate by `(W1)`, because its total available coefficient capacity
   reaches the cap.

Greedy ordering can reduce the number of coefficients used, but it is not
needed for existence.  Rank-one factorization, 3-adic angles, the
Sidon-paired chart, and source algebra do not occur in the proof.

On complement-symmetric cubes, odd Walsh patterns vanish and the same proof
uses the remaining even patterns.  This explains why Theorem T4 is valid on
the symmetric hierarchy.  It also shows why T4 alone cannot distinguish that
hierarchy from an arbitrary truth table.

## Exact negative controls

The verifier exhausts every function

```text
h : {0,1}^m -> {-1,0,1},   0 <= m <= 3,
```

all `6,654` functions, using both direct Walsh sums and an independent
butterfly transform.  It checks inversion, involution, Parseval, `(W1)`, and
greedy-to-cap with explicit fail-closed gates.  Named exact controls include:

```text
h = (1,1,1,-1):
  positive mass                  = 3
  largest single-pattern credit = 2
  all-pattern capacity           = 8
```

Thus one-pattern adequacy is false while capped multi-pattern adequacy is
automatic.  For the positive constant cube,

```text
h = (1,1,1,1,1,1,1,1):
  positive mass                       = 8
  nontrivial-pattern capacity         = 0
  empty-pattern capacity              = 8.
```

So even the universal argument needs every pattern allowed by its inversion
formula; it does not produce nontrivial-character capacity for free.

Two pinned deterministic LCG fixtures (arithmetic modulo `2^32`, seed
`20260716 + m`, output `state mod 7 - 3`) provide non-hand-chosen regressions:

```text
m = 4: Walsh capacity = 116, l1 mass = 35, positive mass = 19
m = 5: Walsh capacity = 252, l1 mass = 49, positive mass = 24
```

The hand-picked and pinned-LCG arbitrary-truth-table fixtures pass the same
capped-greedy theorem with no chart input.  This establishes that scalar
adequacy is structure-free.  It is not a source-derived counterexample and
certifies no source-semantic implication.

## Exact interface mismatch

| Capped-Walsh packet supplies | A paid compiler cell still requires |
|---|---|
| cube values and Walsh coefficients | an actual realized first-match cell |
| scalar positive charge | the same surviving owner slope |
| a cap preventing scalar overcredit | a certified `U_i` for `Z_i^circ` |
| enough coefficient mass to reach the cap | image-scale MI+MA or a direct Sidon theorem |
| finite rank-one pattern data on the model family | `(RC)` or a direct distinct-slope bound |
| finite depth scans for short schedules | a uniform subexponential aggregate census |

No theorem in either governing TeX file maps a rank-one/flat-cube/greedy
pattern credit to the right column.

This is also the boundary already printed by two older guardrails:

- `owner_rooted_dense_band_localization_v1.md`, Assumption 7.1, requires the
  same positive owner, canonical earlier atlas cell, realized parameters,
  and a validated distinct-slope payment;
- `selected_owner_cube_mean_boundary_v1.md`, `(EQ4)`, requires a
  verifier-checkable source derivation, exact selected owners, an owner-level
  projection/payment theorem, whole-slope first-match semantics, and a
  subexponential aggregate census.  It explicitly warns that omitting this
  payment theorem merely renames the admission problem.

The newest rank-one conclusion cannot remove those hypotheses by calling the
remaining step grammar acceptance.

## Required repair

A valid completion needs at least one theorem of the following form:

```text
rank-one pattern certificate
  -> actual same-owner first-match profile cell
  -> certified |Z_i^circ| <= exp(o(n)) (1+barN_i),
```

with exact cell parameters, add-back, and aggregate census; or it must prove
the analytic `(A4)` payment and then supply `(RC)`.  Until then, the
omega-capped greedy rule is useful charge bookkeeping and a candidate
structure certificate, not an admitted payment.

The all-depth pattern-count issue is separate.  Theorem T4 may use every
Walsh coefficient, up to `2^m`; the reported handful-of-pattern counts are
finite pins through the scanned depths, not a uniform subexponential
schedule theorem.  A future bridge must either compress that schedule or
show that its encoded aggregate complexity is subexponential.

## Nonclaims

- This does not refute Theorems T1--T5, S4, the rank-one product law, or any
  finite scan in the emission arc.
- This does not prove that a source-to-cell bridge is impossible.
- This does not change the main Papers A--D or either active TeX manuscript.
- This does not turn emission into a lower-reserve payment; fence `(N1)`
  remains in force.

## Reproducibility

```bash
python3 experimental/scripts/verify_rank_one_admission_interface.py
python3 -O experimental/scripts/verify_rank_one_admission_interface.py
python3 experimental/scripts/verify_rank_one_admission_interface.py --tamper-selftest
python3 -O experimental/scripts/verify_rank_one_admission_interface.py --tamper-selftest
```

The normal and optimized theorem runs report `46,644` exact gates over
`6,662` exhaustive and named cube functions.  Both tamper runs reject the
one-pattern, uncapped-soundness, and nontrivial-only strengthenings.
