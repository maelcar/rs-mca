# Towards-prize Lean Package Summary

This package is the Mathlib-based Lean track for `tex/towards-prize.tex`.
The normalized Lean entry point is:

```text
experimental/lean/towards_prize/TowardsPrize.lean
```

## Contents

The file works in namespace `TowardsPrize` and models the compact threshold
note using finite evaluation types and finite fields:

- words are functions `ι -> F`;
- linear codes are `Submodule F (ι -> F)`;
- distances are integral radii rather than real-radius parameters;
- `CAbad`, `MCAbad`, `epsCA`, `epsMCA`, and `sigmaC` are defined directly;
- `RS ev k` is a Reed-Solomon-style code represented through polynomial
  evaluation over the injected evaluation map `ev`.

Named results in the source include:

- `epsCA_le_epsMCA`;
- `one_div_card_le_epsMCA`;
- `dstar_eq_zero_of_small`;
- `deep_epsMCA_le`;
- `half_epsMCA_le`;
- `line_at_most_one_slope`;
- `sparsify`;
- `safe_half_distance`;
- `prefix_floor`;
- `deep_point_conversion`.

The current source text says the deep-point conversion is proved from first
principles and isolates the supporting lemmas `poleF`, `poleG`, `cs_fiber`,
`eval_eq_count_le`, `poles_colFar`, `poles_closeBy`,
`exists_low_collision`, `final_algebra`, and `deep_fiber_bound`.

## Audit Notes

Codex did not run `lake build` during integration.  A text scan of
`TowardsPrize.lean` found no `sorry`, `admit`, or added `axiom`.

This package is not a complete Lean formalization of Paper D v12, and it does
not formalize the deployed binomial-entropy cap criterion behind every
Theorem 1.1 row in `towards-prize.tex`.  Treat it as a substantial
formalization track for the compact prize note, pending a controlled Mathlib
build and a theorem-by-theorem certification map.
