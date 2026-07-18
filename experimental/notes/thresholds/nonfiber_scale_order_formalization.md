# Realized/group/ambient heavy-count order formalization

## Claim

Fix a finite list `fibers` of fiber sizes and natural numbers `K`, `M`, and
`D`.  Define the division-free heavy count by

```text
heavyCount(fibers, K, M, D)
  = #{f in fibers : K * M <= f * D}.
```

If `D1 <= D2`, then

```text
heavyCount(fibers, K, M, D1)
  <= heavyCount(fibers, K, M, D2).
```

Consequently, `L <= G <= A` gives the source ordering

```text
heavy_realized <= heavy_group <= heavy_ambient.  (ORD)
```

## Status

PROVED.

## Source audit

The authoritative source is Section 1, `The decomposition obligation at
realized-image scale`, of
`experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md` at
integrated snapshot `2633895a`.  Lines defining the three cell scales and
display `(ORD)` were rechecked unchanged on the implementation baseline.

The exact source verifier computes a common list of nonempty fiber sizes and
tests heaviness by the integer inequality `f * D >= 2 * M`.  Lean exposes the
same cleared predicate with a reusable multiplier `K`; no truncated natural
division `M / D` is used.

In the mathematical application, `M` is the total support mass, the list
enumerates each relevant nonempty fiber once, and `L`, `G`, and `A` are the
realized-image, generated-group, and ambient cell counts.  None of those
semantic identifications is needed for the monotonicity proof itself.  This is
an explicit generalization of the arithmetic kernel, not a removal of the
source-side bridge obligations.

The same nonempty-fiber list can represent a full group or ambient census only
after observing that extra cells have size zero and the heaviness threshold is
strictly positive.  This packet does not hide that positivity step inside the
bare natural-number theorem and does not claim a zero-padding invariance lemma.

## Lean correspondence

The declarations are in
`experimental/lean/nonfiber_decomposition_realized_scale/NonfiberDecompositionRealizedScale.lean`.

- `heavyCount` is the exact cleared finite count.
- `heavyCount_mono_denominator` proves monotonicity for one scale comparison.
- `heavyCount_scale_chain` composes the realized/group and group/ambient
  comparisons into `(ORD)`.

The package README records the full source-section to Lean-name status map.

## Validation

From `experimental/lean/nonfiber_decomposition_realized_scale`:

```bash
lake clean
lake build
```

The default build uses the pinned `leanprover/lean4:v4.14.0` toolchain.  The two
new theorem axiom reports contain only Lean's standard propositional
extensionality axiom, with no `sorryAx` or custom axiom.

The source verifier is replayed from the repository root:

```bash
python3 experimental/scripts/verify_nonfiber_decomposition_realized_scale.py
python3 experimental/scripts/verify_nonfiber_decomposition_realized_scale.py --tamper-selftest
```

The expected results are `RESULT: PASS (90/90)` and
`tamper-selftest: caught 3/3` followed by `RESULT: PASS (90/90)`.

## Scope and nonclaims

This theorem does not prove that `(CONC)` holds or fails asymptotically, that
the favorable realized-scale heavy count is exponential, or that the
Sidon-paired construction kills concentration.  It does not formalize the
quotient-coset decomposition identity, charge preservation, semantic
classification, subexponential piece count, or the surviving transverse/direct
signed route `(NFB)`.  It proves no MI/MA or Sidon estimate, profile-envelope
comparison, lower reserve, MCA threshold, or Proximity Prize claim.  Since the
proved count order runs from smaller to larger cell scales, it proves neither
the reverse inequality `heavy_ambient <= heavy_realized` nor equality.  Thus an
ambient lower bound does not transfer to a realized lower bound (while the
displayed order does, of course, transfer an ambient upper bound).
