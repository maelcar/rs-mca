# General pruned signed bound formalization

This standalone Lean 4.14 package formalizes the exact arithmetic and
combinatorial backbone of
`experimental/notes/thresholds/general_pruned_signed_bound.md` at source
snapshot `9262f63c`.

The package now proves the general signed integer layer-cake reconstruction,
its pruned-value and support properties, and the finite nonnegative
cardinality identity.  The Fourier projection, interpolation, charge, and
asymptotic claims remain outside this stdlib-only package.

## Layer-cake theorem map

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| Section 3.1: nonnegative layer size | `layerSize` | DEFINITION |
| Section 3.1: nonnegative layer-mass sum | `layerSum` | DEFINITION |
| Section 3.1: truncated nonnegative layer mass | `layerSum_eq_sum_min` | PROVED |
| Section 3.1: bounded nonnegative mass preservation | `layerSum_eq_foldl_of_le` | PROVED |
| Section 3.1: signed layer | `signedLayer` | DEFINITION |
| Section 3.1: signed layer sum | `signedLayerSum` | DEFINITION |
| Section 3.1: truncated signed reconstruction | `signedLayerSum_eq_sign_mul_min` | PROVED |
| Section 3.1: bounded signed reconstruction | `signedLayerSum_eq` | PROVED |
| Section 3.1: indicator-difference formula | `signedLayer_eq_indicator_diff` | PROVED |
| Section 3.1: values lie in `{-1,0,1}` | `signedLayer_values` | PROVED |
| Section 3.1: layer support stays inside mask support | `signedLayer_ne_zero_imp` | PROVED |
| Section 3.1: function-valued pointwise reconstruction | `signed_layer_cake` | PROVED |

The reusable theorem accepts any common bound `Wmax` on absolute
multiplicities.  Taking the exact maximum recovers the source's minimal layer
count; a larger bound merely appends zero layers.

## Scope

This package does not formalize the analytic `l^q` projection bound, the
charge-preserving decomposition, a subexponential bound on the number of
pieces, heavy-fiber semantic emission, a Sidon payment, max-fiber flatness, or
an MCA threshold.

Build with the pinned toolchain:

```text
lake build
```
