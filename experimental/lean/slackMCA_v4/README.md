# Lean package for `slackMCA_v4.tex`

This folder contains a Lean formalization package for selected finitary parts of
Paper B, `tex/slackMCA_v4.tex`:

- Part I locator/list machinery: locator polynomials, image fibers, arbitrary
  fiber upper bounds, monomial-prefix lower bounds, generated-field
  pigeonhole, quotient-core list obstructions, and the characteristic-zero
  inverse-quotient theorem.
- Finitary corollary packages: characteristic-zero prefix-fiber size and the
  Stirling-free entropy lower bound.
- Part II spine: one bad parameter per support, the canonical exact-slack
  characterization, quotient locator identities, cyclotomic rigidity, and
  Fermat-field digit rigidity.

The package has been normalized under the Lean module namespace
`slackMCA_v4.*`.  The main import file is `slackMCA_v4.lean`.

## Audit Status

Source-level audit only in this repository pass.  I did not run `lake build`
here.  The scanned Lean source contains no open proof placeholders or new
trust primitives.

## Main Files

- `slackMCA_v4/Main.lean` - Part I locator/list and inverse-quotient core.
- `slackMCA_v4/PartII.lean` - Part II MCA/slack spine.
- `slackMCA_v4/CharZeroFiber.lean` - finitary `cor:upstairs-poly` core.
- `slackMCA_v4/EntropyLower.lean` - finitary `cor:entropy-lower` core.

## Remaining Paper B Scope

This package does not formalize the full asymptotic reserve program, the
positive L1/M1 local-limit conjectures, free-pool exponential-sum inputs,
Siegel-Walfisz-type analytic inputs, or the later protocol-facing ledger
consequences.  Those remain outside the current Lean package.
