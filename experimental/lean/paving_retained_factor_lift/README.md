# Paving v9.2 retained-factor-lift companion

This standalone Lean 4 package certifies the proved elementary kernels around
the RF3' content-root repair and the paper-proved RF3'' global-degree bridge for
`experimental/RS_MCA_Paving_v9.2.tex`. It intentionally lives outside
`experimental/lean/grande_finale`: it accompanies the isolated conditional
appendix rather than the Grande Finale frontier library.

## Certified scope

- `ContentCharge.lean` proves over the reals
  `d + alpha*(D-d) <= max 1 alpha * D` for `0 <= d <= D` (in fact for every
  real `alpha`), together with the two coefficient branches, endpoint equalities,
  the additive allowance, and the RF3' specialization
  `alpha = 2 U D_Y^2`. It separately proves the weaker global-degree fallback
  `d + alpha*D <= (1+alpha)*D`; this fallback does not use the specialized
  content-free degree subtraction.
- `F7Threshold.lean` checks the exact rational counterexample arithmetic:
  the old threshold is `533/50000 < 1`, RF3' is `111/100 > 1`, and the
  unabsorbed charge at content degree one is `50503/50000 > 1`.
- `RF3DoublePrime.lean` checks the conservative RF3'' global-degree threshold
  at all four printed parameter rows. It proves the exact ceiling brackets for
  numerators `274589064742753629`, `274721012201293956`,
  `274578888391562205`, and `274861787390263486`, and proves each is at most
  the budget `274980728111395087`.
- `GlobalDegreeBridge.lean` records the full RF3'' bridge as a typed,
  explicitly unasserted proposition and proves the corrected nonlinear-weight,
  direct linear-factor, content/factor aggregation, top-incidence, and
  chosen-support arithmetic kernels. The finite-field factor/Hensel proof is
  given in
  `experimental/notes/audits/paving_v9_2_rf3_global_degree_bridge.md`.
- `RF4ForcesVTwo.lean` defines both finite RF4 sums and proves, with the
  ceiling/degree hypotheses displayed, that strict RF4 forces `V >= 2`; it
  also records the translation `V = ceil(D_Y)`, `V >= 2` implies `D_Y > 1`.
- `Target.lean` retains the generic target for the original RF3/RF3'
  retained-factor assumption. It is not an axiom: its sole consumer requires
  it explicitly as a hypothesis. The separately typed RF3'' target is in
  `GlobalDegreeBridge.lean`.

`CORRESPONDENCE.md` maps these declarations to the v9.2 labels and separates
Lean-certified arithmetic, the paper-proved RF3'' bridge, and the remaining
RF3/RF3' source obstruction.

## Build

```sh
cd experimental/lean/paving_retained_factor_lift
lake update
lake exe cache get
lake build
```

The package pins Lean/Mathlib `v4.28.0`, matching nearby Mathlib-based
standalone companions. No theorem contains `sorry`, `admit`, an axiom, or a
hidden factor-lifting proof.

## Nonclaims

This package does not formalize finite-field factorization, regular
specialization, Hensel lifting, BCIKS Lemma A.1, or the corrected replacement
for Claim A.2. The companion note supplies a paper proof of the RF3''
global-degree bridge, while Lean keeps that algebraic theorem explicitly
unasserted. This does not repair the weaker RF3/RF3' assumption in immutable
v9.2, prove its conditional retained-degree MCA bound, or upgrade any
KoalaBear row to unconditional status.
