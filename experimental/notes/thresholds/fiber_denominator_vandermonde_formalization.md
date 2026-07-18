# Fiber-denominator Vandermonde formalization

## Claim

For integers `a < b < c` and the quadratic phase

\[
\psi_x=\theta_0+\theta_1x+\theta_2x^2,
\qquad
\operatorname{Vdm}(a,b,c)=(b-a)(c-b)(c-a),
\]

the exact three-point combination isolates the quadratic coefficient:

\[
(c-b)\psi_a-(c-a)\psi_b+(b-a)\psi_c
=\operatorname{Vdm}(a,b,c)\theta_2.
\]

Taking distance to the nearest integer gives the weighted and diameter bounds
of Lemma V.  If all three phase values have nearest-integer distance at most
`w` and `3(c-a)w < 1/2`, then `θ₂` is within

\[
\frac{3(c-a)w}{\operatorname{Vdm}(a,b,c)}
\]

of the explicit quotient
`round(Vdm(a,b,c) θ₂) / Vdm(a,b,c)`, this distance is strictly less than
`1 / (2 Vdm(a,b,c))`, and
`Vdm(a,b,c) ≤ (c-a)^3`.

## Status

PROVED.

## Source and statement audit

This packet formalizes Lemma V and Corollary V.1 from
`experimental/notes/thresholds/fiber_denominator_tension.md` at source
snapshot `ea4eb078`.  The deterministic source check is
`experimental/scripts/verify_fiber_denominator_tension.py` at the same
snapshot.  The source packet was introduced by Holm Buar in PR #692.

The correspondence is exact on the load-bearing data:

| Source item | Lean statement |
|---|---|
| Ordered triple `a < b < c` in a finite integer block | `lemmaV_of_mem` retains membership and ordering; the algebraic helpers explicitly drop unused block hypotheses. |
| `Vdm(T)=(b-a)(c-b)(c-a)>0` | `vandermondeProduct` and `vandermondeProduct_pos`. |
| Exact resolution identity | `vandermonde_resolution_identity`. |
| Weighted nearest-integer inequality | `vandermonde_resolution_weighted`. |
| Diameter relaxation | `vandermonde_resolution_diameter`. |
| Three trapped phases and `3 diam(T) w < 1/2` | `trappedTriple_rationalApproximation`. |
| `Vdm(T) ≤ diam(T)^3` | `vandermondeProduct_le_diameter_cube`. |

The identity, positivity, and inequalities do not use the source block's
normalization or gcd condition.  The module therefore exports the smallest
correct helpers under only the hypotheses they consume, and also supplies
`lemmaV_of_mem` with the source's ordered-triple membership interface.  This
generalization is explicit; no source hypothesis is being used covertly.

Mathlib's `UnitAddCircle` norm is used for nearest-integer distance, with
`UnitAddCircle.norm_eq` giving `|x - round x|`.  The trapped theorem exhibits
an integer numerator divided by the positive integer `Vdm`.  It does not add a
separate proposition about the denominator of the reduced rational form.

## Lean correspondence

The declarations are in
`experimental/lean/moment_to_max/MomentToMax/FiberDenominatorVandermonde.lean`:

- `vandermonde_resolution_identity`;
- `vandermonde_resolution_weighted`;
- `vandermonde_resolution_diameter`;
- `vandermondeProduct_pos`;
- `vandermondeProduct_le_diameter_cube`;
- `lemmaV_of_mem`;
- `trappedTriple_rationalApproximation`.

The theorem-by-theorem source map is
`experimental/lean/moment_to_max/README.md`, and the package aggregate imports
the new module through `MomentToMax.lean`.

## Validation

From `experimental/lean/moment_to_max`:

```bash
lake clean
lake exe cache get
lake build
```

The deterministic source verifier is replayed with:

```bash
python3 experimental/scripts/verify_fiber_denominator_tension.py
```

Its expected terminal line is `RESULT: PASS (56/56)`.  Axiom printing for all
seven theorem declarations and a changed-source scan for `sorry`, `admit`, new
`axiom`, and `sorryAx` are part of the packet check.

## Producer and consumer interlocks

PR #692 is the direct producer of Lemma V and Corollary V.1.  It resolves the
three-point denominator mechanism motivated by PR #691; PR #700 corrects the
T1 window used in that broader antecedent analysis.  PR #701 is the direct
downstream consumer that combines PR #692 with the corrected denominator
window.  PR #663 supplies bounded-denominator-horn context but is not a Lean
dependency.

## Scope and nonclaims

This packet proves only Lemma V's three-point Vandermonde kernel and Corollary
V.1's explicit trapped quotient.  It does not formalize the pointwise cosine
estimate, Theorem AP, a measured mass law, regime disjointness, or any
wall/no-pincer conclusion in PR #701.  It makes no claim about an MCA owner,
rank-drop adapter, or submission-facing theorem.
