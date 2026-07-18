# Moment-to-max formalization map

Build the package with its pinned Lean 4.28 / Mathlib environment:

```bash
lake build
```

## Fiber-denominator Vandermonde resolution

Source snapshot:
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`.

| Source label | Lean declaration | Status |
|---|---|---|
| Lemma V, exact identity | `vandermonde_resolution_identity` | PROVED |
| Lemma V, weighted inequality | `vandermonde_resolution_weighted` | PROVED |
| Lemma V, diameter inequality | `vandermonde_resolution_diameter` | PROVED |
| Lemma V, `Vdm(T) > 0` | `vandermondeProduct_pos` | PROVED |
| Corollary V.1, `Vdm(T) ≤ diam(T)^3` | `vandermondeProduct_le_diameter_cube` | PROVED |
| Lemma V, source-facing block wrapper | `lemmaV_of_mem` | PROVED |
| Corollary V.1, trapped rational approximation | `trappedTriple_rationalApproximation` | PROVED |

The algebraic identity is exported without unnecessary block membership or
ordering assumptions; `lemmaV_of_mem` reinstates the source's ordered triple
inside a finite integer block.  `nearestIntegerDistance` is the
`UnitAddCircle` norm, which Mathlib identifies with `|x - round x|`.

This map covers the three-point Vandermonde packet only.  The package's older
modules retain their existing correspondence and audit documents.  No
pointwise cosine estimate, arithmetic-progression resolution theorem, measured
mass trend, or wall-regime conclusion is claimed here.
