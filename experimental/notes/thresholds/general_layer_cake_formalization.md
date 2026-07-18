# General signed layer-cake formalization

## Claim

Let `b : α → Int`, and suppose `Wmax` bounds every absolute multiplicity:

```text
forall s, (b s).natAbs <= Wmax.
```

For positive thresholds `j`, put

```text
g_j(s) = 1_{j <= b(s)} - 1_{b(s) <= -j}.
```

Then every `g_j(s)` lies in `{-1,0,1}`, its support is contained in the
support of `b`, and the pointwise sum of the first `Wmax` layers reconstructs
`b`.  For a finite nonnegative multiplicity list, summing this pointwise
identity gives the exact cardinality formula

```text
sum_{j=1}^{Wmax} #{s : j <= b(s)} = sum_s b(s).
```

The formalization also proves the exact truncated forms when `Wmax` is below
some multiplicity.

## Status

PROVED.

## Source audit

The authoritative source is Section 3.1, `Multiplicity-carrying (unpruned)
packets`, of
`experimental/notes/thresholds/general_pruned_signed_bound.md` at integrated
snapshot `9262f63c`.  The positive specialization is reused in
`experimental/notes/thresholds/charge_preserving_split_decomposition.md` at
the same snapshot.  The source packet and its charge-preserving interfaces
credit Vadim Avdeev's signed-clause framework; this packet formalizes only the
elementary layer-cake component.

The source chooses `Wmax = max_s |b(s)|`.  Lean exposes the stronger reusable
form in which `Wmax` is any common upper bound.  This is an explicit
generalization, not an extra hidden hypothesis: larger bounds contribute only
zero layers.

The signed statement is pointwise.  The unsigned cardinality identity is
proved separately for nonnegative natural multiplicities; it is not asserted
for a signed mask, where summing unsigned support sizes would be false.

## Lean correspondence

The declarations are in
`experimental/lean/general_pruned_signed_bound/GeneralPrunedSignedBound.lean`.

- `layerSum_eq_sum_min` proves the exact truncated nonnegative mass formula.
- `layerSum_eq_foldl_of_le` gives total mass preservation under a common
  multiplicity bound.
- `signedLayerSum_eq_sign_mul_min` proves the exact truncated signed formula.
- `signedLayerSum_eq` proves bounded pointwise reconstruction.
- `signedLayer_eq_indicator_diff` identifies the `natAbs`/`sign`
  implementation with the source's two signed indicators.
- `signedLayer_values` proves every layer is pointwise pruned.
- `signedLayer_ne_zero_imp` proves layer support is contained in mask support.
- `signed_layer_cake` exports the function-valued source form.

The package README records the complete source-section to Lean-name map.

## Dependency boundary

The identity itself uses only integer multiplicities, a natural layer bound,
and finite list folds for the mass corollary.  It needs no group operation,
characters, Fourier band, moment order, image size, norming dual, or code.

The finite-chart support-cardinality conclusion follows downstream by
combining `signedLayer_ne_zero_imp` with the chart's existing support bound;
it is not baked into the pointwise theorem.

## Validation

From `experimental/lean/general_pruned_signed_bound`:

```bash
lake clean
lake build
```

The default build uses the pinned `leanprover/lean4:v4.14.0` toolchain.
Principal theorem axiom reports contain only Lean's standard quotient and
propositional extensionality axioms, with no `sorryAx` or custom axiom.

The source verifier is replayed from the repository root:

```bash
python3 experimental/scripts/verify_general_pruned_signed_bound.py
python3 experimental/scripts/verify_general_pruned_signed_bound.py --tamper-selftest
```

The first command regenerates the checked-in JSON certificate before printing
`RESULT: PASS (193359/193359)`; the tamper self-test rejects all six mutations.

## Scope and nonclaims

This packet does not formalize or strengthen Theorem I's Fourier projection
bound, Theorem D's signed-clause discharge, charge compatibility, or the
positive-rooted decomposition.  It does not prove that the number of layers
is subexponential; the integrated charge packet gives exact profiles where
the piece count is exponential without staircase concentration.  It does not
prove heavy-fiber semantic emission, a large-moment signed/Sidon estimate,
primitive-Q flatness, a profile-envelope comparison, an MCA threshold, or a
Proximity Prize claim.
