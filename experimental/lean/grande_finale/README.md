# Grande Finale Lean Formalization

This Lean package contains partial formalization tracks for
`experimental/grande_finale.tex`.

The package root is `GrandeFinale`, with additional modules under
`GrandeFinale/`:

- `GrandeFinale.lean` formalizes the core staircase, first-match, moment, and
  finite certificate kernels.
- `GrandeFinale/QFourierTao.lean` formalizes the log-moment-to-Q reduction.
- `GrandeFinale/QEntropyInverse.lean` formalizes the deterministic atoms around
  the entropic inverse route.
- `GrandeFinale/QPrimitiveCollision.lean` formalizes collision-tuple and
  low-support exclusion kernels.
- `GrandeFinale/QFiniteTables.lean` pins the four finite Q table rows and
  kernel-checks their exact integer inputs, budget-ratio truncations, printed
  margin rounding, and moment-floor convention split.
- `GrandeFinale/BC.lean`, `GrandeFinale/SP.lean`, and
  `GrandeFinale/Frontier.lean` formalize theorem-level reductions around the
  BC, SP, and frontier ledgers.

The central open mathematical target remains Q: the primitive entropic inverse
theorem / row-sharp prefix-fiber bound needed by `grande_finale.tex`.  The
finite-table module certifies the transcription and elementary integer
arithmetic of the printed target; its decimal margins and moment-order floors
are pinned audited data, not Lean derivations of `Real.log` or the huge
binomial coefficients.  These Lean files do not prove the full adjacent safe
rows or the full asymptotic closure by themselves.

Do not run `lake build` casually in this repository.  Build this package only
with the pinned Lean/Mathlib versions and the matching precompiled Mathlib
cache.  The full default target, including the package root and all child
modules, was checked successfully under that exact-pin setup on 2026-07-09.
