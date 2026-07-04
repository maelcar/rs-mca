# CAP25 v13 Experimental Lean Summary

This package formalizes selected self-contained compiler lemmas from
`cap25_v13_experimental.tex` under namespace `CAP25V13`, with Lean modules
normalized under `cs25_cap_v13_experimental.*`.

## Formalized Core

- `cs25_cap_v13_experimental.ThresholdCompilers`
  - Monotone staircase localization and interior transition.
  - Closed integer endpoint/radius bookkeeping.
  - Lower/upper corridor lemmas.
  - Coarse steepness interval checks.
  - Extension-pole Cauchy-Schwarz counting core.
  - Budget-window arithmetic and unresolved field-size intervals.
  - Rate-1/2 census identity and exact arithmetic crossing certificates.
  - Bounded active quotient-order and residual-absorption lemmas.

- `cs25_cap_v13_experimental.ListSideCompilers`
  - Agreement-threshold Johnson bounds.
  - Polynomial-folding/planted quotient-core lower count.
  - Dyadic planted crossing certificates.
  - List unsafe test and planted budget windows.
  - Few-petal Johnson range.
  - Fixed-excess full-petal compiler bound.

- `cs25_cap_v13_experimental.ResidueLineTools`
  - GAP-2 quotient seam arithmetic.
  - Substitution injectivity.
  - Dimension-one voting.
  - Fixed-dimensional Conjecture-F bound.
  - Hankel determinant identity.
  - Anticode packing.
  - Johnson-ball size identity.

## Source-Audit Result

The scanned Lean source contains no open proof placeholders or new trust
primitives.  Imports and package metadata have been normalized away from the
temporary draft package name to `cs25_cap_v13_experimental`.

I did not run Lake in this repository pass.  The package should be built in a
Mathlib-enabled Lean 4.28 environment before promotion.

## Scope Limits

This is not a complete formalization of CAP25/Paper D.  It omits the v12 imports
needed for the exact tangent cell and quotient support/image ledgers, the full
split-locator probability/moment calculus, Johnson association-scheme spectral
input, and the SPI pseudo-division eliminant theorem.  Those remain separate
formalization targets.
