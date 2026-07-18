# Cylinder modulus identity formalization

This standalone Lean 4.14 package formalizes the exact base-3 modulus
normalization in U1/V1 of
`experimental/notes/thresholds/cylinder_renormalization.md`.  The original
packet is `c844abb1`, its main integration is `764f1c02`, and the corrected
current authority is `02728b20`.  That correction withdrew false
twisted-coset and hierarchy-wide cube-flatness claims; it did not change the
modulus identity.

The TeX connection is interface-only.  The thresholds paper at `856d8362`
contains both the PO3/PO4 interface and the SAT1 fence; the frontiers paper at
`4e3c4ee8` contains PO3/PO4, but not SAT1.  Neither paper states the cylinder
normalization as a standalone theorem.

## Theorem map

| Source section | Lean declaration | Status |
| --- | --- | --- |
| Arithmetic and finite-anchor definitions | `binom`, `slice`, `realizedImage`, `collisionMass` | DEFINITIONS |
| U1/V1, subtraction-free base-3 normalization | `realizedImage_double` | PROVED for every natural `B` |
| U1/V1, `c = 2L - 1` | `modulus_identity_all` | PROVED for every natural `B` |
| Former finite modulus check | `modulus_identity` | PROVED as a compatibility wrapper around `modulus_identity_all` |
| Degenerate `m=0` U3 convolution anchors | `degenerate_cylinder_consistency` | PROVED for the displayed finite parameter lists only |
| Shifted Vandermonde anchors | `graded_vandermonde` | PROVED for the displayed finite parameter lists only |
| Collision-mass and slice anchors | `class_pins` | PROVED for `B=6,8` only |
| U1 Parseval identity and wide-band conclusion | none | NOT FORMALIZED IN LEAN |
| U2 suffix structure and U3 trigonometric/polynomial renormalization | none | NOT FORMALIZED IN LEAN |
| Corrected source section 4, slice-staircase/class-constancy lemma | none | NOT FORMALIZED IN LEAN |
| Subgroup cube-flatness and certificate recursion | none | NOT FORMALIZED IN LEAN |
| Corrected twisted-coset nonflatness counterexample | none | NOT FORMALIZED IN LEAN |

## Arithmetic boundary

Lean defines

```text
realizedImage B = (3^B + 1) / 2.
```

Every power of three is odd, so natural division is exact and Lean first
proves the subtraction-free identity

```text
2 * realizedImage B = 3^B + 1.
```

The printed `3^B = 2L - 1` formula is then a corollary.  No positivity or
evenness hypothesis is needed for this arithmetic: `B=0` and odd `B` are valid
boundary cases for the defined function.  The displayed V1 finite verification
uses positive even depths through 64; the all-natural theorem does not assert
that the source's realized-image interpretation has the same formula at odd or
zero depth.

## Scope

The package does not formalize complex characters, Fourier transforms,
Parseval, band norms, the U1 wide-band implication, phase or suffix structure,
U2/U3 cylinder renormalization, graded polynomial coefficients in general,
the slice-staircase/class-constancy lemma, subgroup cube-flatness, or certificate
compression.  It does not restore the false twisted-coset flatness claim,
transfer U2/U3 to base 5, prove admission,
pay an image-scale MI/MA or Sidon bill, compile a residual ray, compare the
complete profile envelope, establish lower reserve, close a deployed row, or
prove an MCA threshold or Proximity Prize claim.

Build with the pinned toolchain:

```text
lake build
```
