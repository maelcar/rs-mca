# Nonfiber realized-scale formalization

This standalone Lean 4.14 package formalizes exact finite arithmetic from
`experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md` at
source snapshot `2633895a`.

## Theorem map

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| Section 2: exact binomial arithmetic | `binom` | DEFINITION |
| Section 2: realized image, slice, max fiber, and ambient modulus | `realizedImage`, `slice`, `maxFiber`, `ambientMod` | DEFINITIONS |
| Section 1 `(CONC)`: cleared heavy-fiber count on a fixed census | `heavyCount` | DEFINITION |
| Section 1 `(ORD)`: monotonicity under `D1 <= D2` | `heavyCount_mono_denominator` | PROVED |
| Section 1 `(ORD)`: realized <= group <= ambient chain | `heavyCount_scale_chain` | PROVED |
| Section 2: realized image is below the ambient modulus | `realized_below_ambient_base3`, `realized_below_ambient_base5` | PROVED, finite rows |
| Section 2: collapse is bounded/exponential in the two toy bases | `collapse_bounded_base3`, `collapse_exponential_base5` | PROVED, finite rows |
| Section 2: realized-scale collapse is insufficient at `B = 8` | `collapse_insufficient_B8` | PROVED, finite row |
| Section 5: divisor census | `divisors` | DEFINITION |
| Section 5: prime-field divisor census | `primeDivisors_7`, `primeDivisors_11`, `primeDivisors_13`, `noProperSubgroup_7_11_13` | PROVED, finite rows |
| Section 5: composite-modulus contrast | `compositeHasProperSubgroup` | PROVED, finite row |
| Section 6: abundance crossover arithmetic | `crossover_superpoly`, `abundance_recurs_B60` | PROVED, finite row |

For one fixed list `fibers`, the new definition uses the exact cleared test

```text
K * M <= f * D
```

instead of natural-number division by `D`.  Instantiating `D` successively with
the realized-image, generated-group, and ambient cell counts gives `(ORD)` from
their cardinality order.

The source verifier reuses the list of nonempty realized fibers at all three
scales.  Identifying this with a full group or ambient census padded by zero
cells additionally uses positivity of the threshold; that zero-padding bridge
is not asserted by `heavyCount_scale_chain`.

## Scope

The new theorem is only the finite normalization-order kernel.  It does not
prove an exponential or subexponential concentration estimate, that the
Sidon-paired family remains heavy, a charge-preserving or semantic
decomposition, the surviving `(NFB)` route, image-scale MI/MA, a Sidon payment,
an MCA threshold, or a Proximity Prize claim.  It proves neither the reverse
inequality `heavy_ambient <= heavy_realized` nor equality; in particular, an
ambient lower bound does not transfer to a realized lower bound.

Build with the pinned toolchain:

```text
lake build
```
