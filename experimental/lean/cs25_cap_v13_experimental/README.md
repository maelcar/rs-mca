# Lean package for `cap25_v13_experimental.tex`

This folder contains a Lean package for selected self-contained pieces of the
experimental CAP25 v13 insert:

- threshold certificate compilers;
- L1 list-side compiler lemmas;
- M1 residue-line and Conjecture-F helper lemmas.

The package is normalized under the Lean module namespace
`cs25_cap_v13_experimental.*`.  The main import file is
`cs25_cap_v13_experimental.lean`.

## Scope

This package is not a formalization of the main Paper D v12 and does not merge
the experimental v13 insert into the paper.  It formalizes reusable local
compiler statements from `cap25_v13_experimental.tex` where the arguments are
standalone arithmetic, combinatorics, or algebra.

The source TeX snapshot `cap25_v13_experimental.tex` is included in this folder
as local context.  The repository-level experimental insert remains
`experimental/cap25_v13_experimental.tex`.

## Main Files

- `cs25_cap_v13_experimental/ThresholdCompilers.lean`
  Threshold staircases, corridors, budget windows, extension-pole counting,
  quotient-census arithmetic, and residual absorption.

- `cs25_cap_v13_experimental/ListSideCompilers.lean`
  Agreement-threshold Johnson bounds, planted quotient-core/list compiler
  pieces, dyadic planted crossing certificates, and full-petal fixed-excess
  counting.

- `cs25_cap_v13_experimental/ResidueLineTools.lean`
  GAP-2 quotient seam arithmetic, substitution injectivity, dimension-one and
  fixed-dimensional Conjecture-F tools, Hankel determinant, anticode packing,
  and Johnson-ball counting.

## Audit Status

Source-level audit only in this repository pass.  I did not run Lake.  The
scanned Lean source contains no open proof placeholders or new trust primitives.
Several numeric crossing certificates use `native_decide`, which should be
reviewed as executable arithmetic certificates.

## Not Formalized Here

This package does not formalize the exact tangent cell from Paper D v12, the
quotient safe-sum support/image ledger imports, the full probabilistic
split-locator moment calculus, Johnson association-scheme spectral arguments,
or the SPI pseudo-division eliminant theorem.  The package headers list these as
out-of-scope dependencies or residual branches.
