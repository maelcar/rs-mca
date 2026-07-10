# Grande Finale Formalization Summary

This package is a partial Lean formalization of
`experimental/grande_finale.tex`.

## Package Layout

- `GrandeFinale.lean`: core self-contained kernels for integer budgets,
  first-match ledgers, CA/MCA bad-slope monotonicity, moment inequalities, and
  finite packet arithmetic checks.
- `GrandeFinale/QFourierTao.lean`: log-moment-to-Q reductions, including the
  finite bit-certificate inequality.
- `GrandeFinale/QEntropyInverse.lean`: deterministic atoms around the entropic
  inverse route, including the reverse moment/max-fiber inequality and
  Vandermonde rank rigidity.
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

The syndrome-line module is independent of Q.  It proves the generic
linear-code compiler behind `prop:syndrome-line-normal-form` and
`thm:syndrome-secant-exact` in the frontiers paper.  The Reed--Solomon
parity-check construction, rational-normal-curve interpretation, and reduction
from threshold witnesses to exact-cardinality supports remain separate.

## Build Note

Do not run `lake build` casually in this repository.  Build only with the
pinned Lean/Mathlib versions and matching precompiled Mathlib cache.  On
2026-07-09 the full default target completed successfully in that exact-pin
environment, including `GrandeFinale.lean` and every `GrandeFinale/*` module.
