# SlackMCA v4 Lean Formalization Summary

This package formalizes a substantial finitary core of Chojecki's
`slackMCA_v4.tex` in namespace `Chojecki`, with Lean modules normalized under
`slackMCA_v4.*`.

## Formalized Core

- `slackMCA_v4.Main`
  - Locator polynomials and agreement/list definitions.
  - Monomial-prefix injection and coefficient-pigeonhole lower bound.
  - Quotient-core list obstruction in smooth multiplicative subgroups.
  - Arbitrary-word fiber upper bound, image fibers as exact lists, and the
    fiber-count identity.
  - Generated-field pigeonhole.
  - Characteristic-zero inverse quotient theorem over dyadic roots of unity.

- `slackMCA_v4.PartII`
  - Cyclotomic rigidity.
  - Signed-binary uniqueness and Fermat-field digit rigidity.
  - One bad MCA parameter per support.
  - Exact slack characterization for the canonical line
    `x^(k+T) + z*x^k`.
  - Quotient locator composition and vanishing identities.

- `slackMCA_v4.CharZeroFiber`
  - Finitary polynomial-size bound for characteristic-zero prefix fibers.

- `slackMCA_v4.EntropyLower`
  - Finitary, Stirling-free entropy lower bound derived from
    `pigeonhole_lower`.

## Source-Audit Result

The scanned Lean source contains no open proof placeholders or new trust
primitives.  Imports and package metadata have been normalized away from the
temporary draft package name to `slackMCA_v4`.

I did not run a full `lake build` in this repository pass.  The package should
be built in a Mathlib-enabled Lean 4.28 environment before promotion.

## Not Formalized Here

The package does not claim to formalize the full Paper B research program:
the asymptotic `o(n)` statements, Siegel-Walfisz or primes-in-progressions
inputs, positive L1/M1 local-limit conjectures, extension-transfer theory,
free-pool exponential-sum estimates, and protocol-level consequences remain
outside this package.
