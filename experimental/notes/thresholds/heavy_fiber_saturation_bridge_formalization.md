# Heavy-fiber saturation bridge formalization

## Claim

Let `sat = a - R - 1` and
`cap = cwBound n (2 * (R + 2)) a`.  If a represented family has maximum
pairwise intersection at most `sat`, that same family's maximum intersection
being strictly below `sat` would force its length to be at most `cap`, and its
length is strictly greater than `cap`, then its maximum intersection equals
`sat`.

## Status

PROVED, with the non-saturating ceiling visible as a hypothesis.  The former
unrestricted Lean target is COUNTEREXAMPLE.

## Source audit

The authoritative source is Theorem 1, “saturation-forcing, general depth R,”
in `experimental/notes/thresholds/heavy_fiber_planted_emission.md`, from source
packet PR #735 at `f94d8706`.  The source first uses PR #717, head `ae5f1f1e`,
to view a depth-`R` prefix fiber of `a`-subsets as a constant-weight code with
maximum pairwise intersection at most `a-R-1`.  It then imports the classical
Johnson ceiling for the strictly non-saturating case and takes its
contrapositive.  The resulting saturation precursor feeds the structured side
owned by PR #716 at `bc6280c5`.

The old Lean target omitted the constant support size, finite-universe,
distinct-support, and set-semantics hypotheses.  More decisively, it omitted
the theorem connecting those semantics to `cwBound`.  Its conclusion therefore
did not follow from its list-level hypotheses.

## Explicit counterexample and repair

At `(n,a,R) = (12,4,2)`, let `fibers` be four empty lists.  The local definitions
compute

```text
maxIntersect fibers = 0,
cwBound 12 8 4 = 3,
fibers.length = 4,
a - R - 1 = 1.
```

Thus both old hypotheses hold but the claimed equality is false.  Lean records
this as `old_saturation_target_counterexample`.

The replacement `saturation_forcing_of_nonsaturating_ceiling` accepts the
missing implication

```text
maxIntersect fibers < a - R - 1
  -> fibers.length <= cwBound n (2 * (R + 2)) a
```

explicitly.  If equality failed, the assumed upper bound on `maxIntersect`
would make it strictly smaller than the saturation value.  The ceiling would
then contradict strict heaviness.

Using strict inequality avoids the false unrestricted natural-number rewrite
`x < t` as `x <= t - 1` at truncated-subtraction boundaries.

## Lean correspondence

The declarations are in
`experimental/lean/heavy_fiber_planted_emission/HeavyFiberPlantedEmission.lean`.

- `old_saturation_target_counterexample` locks the false former interface.
- `saturation_forcing_of_nonsaturating_ceiling` proves the corrected logical
  bridge using `Nat.le_antisymm` and the strict-order contradiction.
- The package README contains the full source-label to Lean-name status map.

## Validation

From `experimental/lean/heavy_fiber_planted_emission`:

```bash
lake clean
lake build
```

From the repository root, the source packet is replayed with:

```bash
python3 experimental/scripts/verify_heavy_fiber_planted_emission.py
python3 experimental/scripts/verify_heavy_fiber_planted_emission.py --tamper-selftest
```

The first command is expected to end with `RESULT: PASS (138/138)`; the second
is expected to report `tamper-selftest: caught 4/4` and the same PASS result.

## Scope and nonclaims

This packet does not formalize the Johnson constant-weight-code bound, prove
that `cwBound` is valid or sharp, or encode that the represented supports are
distinct `a`-subsets of an `n`-element universe.  It does not prove the full
source Theorem 1 without the explicit ceiling hypothesis.  It also does not
prove exhaustive precursor emission, a ledger-wide subexponential saturation
profile count, the ray compiler or its payment, the semantic-or-signed
dichotomy, the finite census beyond its separate verifier, a near-extremal
classification, a general refutation of a sixth precursor clause, image-scale
MI/MA, direct Sidon payment, a residual compiler, profile-envelope comparison,
lower reserve, MCA threshold, deployed-row closure, or a Proximity Prize claim.
