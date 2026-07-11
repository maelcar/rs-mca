# `GrandeFinale.ChallengeIntersection` correspondence

## Status

`GrandeFinale/ChallengeIntersection.lean` isolates the proper-challenge part of
the simple-pole lower bound. Its unconditional core is finite: a translate of
any finite bad-slope set meets a fixed challenge set in at least the ceiling of
the average intersection size. For a linear code, shearing a received line
translates its MCA-bad slope set, so the finite-group result gives the same
ceiling for the challenge-restricted MCA numerator.

These translate/intersection and linear-code reparameterization statements are
`PROVED` in Lean. The Reed--Solomon list construction and the inner
collision-aware simple-pole floor remain explicit inputs.

## Source correspondence

The source is `experimental/asymptotic_rs_mca_frontiers.tex`.

| Lean content | Manuscript source | Status |
|---|---|---|
| finite translates `Z - delta` and intersections `Gamma ∩ (Z - delta)` | outer-averaging paragraph in the proof of `prop:simple-pole-lower` | `PROVED` for finite additive groups |
| exact sum `sum_delta |Gamma ∩ (Z-delta)| = |Gamma||Z|` | averaging identity behind the factor `|Gamma|/q` | `PROVED` |
| existence of a translate with intersection at least `ceil(|Gamma||Z|/q)` | outer ceiling in `eq:exact-unsafe-budget` (13.3) | `PROVED` |
| challenge-restricted bad-slope set and numerator | `B_{C,Gamma}^{MCA}(a)` in the introductory definitions and (13.3) | Definition |
| received-line shear `(r0,r1) ↦ (r0+delta*r1,r1)` | translation step in the proof of `prop:simple-pole-lower` | `PROVED` for linear codes |
| transfer from a full-field bad-slope floor `M` to `ceil(|Gamma|M/q)` challenge slopes | outer implication used by `prop:simple-pole-lower` | `PROVED` from the displayed full-field floor hypothesis |
| `M(L)=ceil(L(q-n)/(q-n+k(L-1)))` | `thm:collision-aware-pole`, `eq:collision-aware-pole` (4.2) | Input to this module, not re-proved |
| nested value `ceil((|Gamma|/q) M(L))` | `eq:exact-unsafe-budget` (13.3) | Recovered exactly once the inner floor is supplied |

The natural-number outer ceiling is the exact integer form

```text
ceilDiv (|Gamma| * M) q.
```

It is not a real-valued approximation to `(|Gamma|/q)M`.

## Declaration map

| Declaration | Content | Status |
|---|---|---|
| `translate`, `mem_translate_iff_preimage` | Finite additive translate and its exact membership convention | Definition / `PROVED` |
| `sum_card_translate_inter` | Sum of all translate--challenge intersection sizes is `Z.card * Gamma.card` | `PROVED` |
| `exists_card_translate_inter_ge_ceilAverage` | Some translate attains the exact natural-number ceiling average | `PROVED` |
| `maxTranslateIntersection`, `ceilAverage_le_maxTranslateIntersection` | Maximum-over-translates form of the same ceiling bound | Definition / `PROVED` |
| `explainedPair_add_smul_iff`, `explained_shifted_combination_iff` | Linear-code explanation predicates are invariant under received-line shear | `PROVED` |
| `mcaBad_add_smul_iff` | Shearing the first received word shifts the slope parameter | `PROVED` for a linear code represented by a submodule |
| `mcaBadSlopes`, `restrictedMCABadSlopes` | Complete and challenge-restricted bad-slope sets on one received line | Definition |
| `restrictedMCABadSlopes_shear_eq_translate_inter` | Exact identification of a sheared restricted set with a translate intersection | `PROVED` |
| `exists_shear_restrictedMCABadSlopes_ge_ceilAverage` | A received-line shear realizes the finite-group ceiling inside `Gamma` | `PROVED` |
| `B_MCA_challenge` | Maximum challenge-restricted bad-slope count over received lines | Definition |
| `restrictedMCABadSlopes_card_le_B_MCA_challenge` | Every explicit received line is bounded by the restricted numerator | `PROVED` |
| `ceilAverage_le_B_MCA_challenge` | An explicit full bad-slope set compiles to the outer challenge ceiling | `PROVED` |
| `B_MCA_challenge_univ` | Full-field challenge recovers `B_MCA` exactly | `PROVED` |
| `B_MCA_challenge_le_B_MCA` | Challenge restriction cannot increase the full numerator | `PROVED` |
| `B_MCA_challenge_le_card` | The restricted numerator is at most the challenge-set cardinality | `PROVED` |
| `challenge_floor_of_full_floor` | Any supplied full-numerator floor `M` gives `ceilDiv (Gamma.card * M) |F| ≤ B_MCA_challenge` | `PROVED` |

The module reuses `GrandeFinale.Explained`, `ExplainedPair`, `MCABad`, and
`B_MCA`. The existing declarations `distinct_value_floor`,
`nat_ceil_div_le`, and `exists_le_average` are arithmetic kernels for the
different, inner collision-aware-pole step; their existence does not make that
coding-theoretic step a theorem of this module.

## Exact boundary

The finite-group theorem needs no coding theory and no structure on `Gamma`
beyond finiteness. The challenge set need not be additively invariant. The
linear-code theorem uses closure under linear combinations to identify

```text
MCABad C (r0 + delta • r1) r1 a gamma
  ↔ MCABad C r0 r1 a (gamma + delta).
```

Consequently the sheared line has bad-slope set `Z-delta`, and averaging over
all `delta` keeps `Gamma` fixed. Only finite slopes are counted, matching
`B_{C,Gamma}^{MCA}(a)`.

## Nonclaims

This module does **not** prove:

- the exact prefix-list bijection `prop:exact-prefix-list`;
- that `L(a)=ceil(binomial n a * |B|^(-(a-k-1)))` is realized by a
  dimension-`k+1` Reed--Solomon list;
- existence of a pole outside the evaluation domain, the polynomial
  root-per-collision bound, or the construction of the received simple-pole
  line;
- the full coding-theoretic theorem `thm:collision-aware-pole`;
- a quotient, Chebyshev, planted, or remainder-profile list floor;
- `prop:simple-pole-lower` end to end: the module proves its outer
  proper-challenge bridge, conditional on the inner full-field floor;
- the safe-side bound, SB2/SB3, an asymptotic frontier statement, or a deployed
  finite-row certificate.

Thus (13.3) has a clean formal boundary: the outer challenge-intersection
ceiling is kernel-checked, while the Reed--Solomon/list-size input that supplies
`M(L)` remains separate and visible.

## Verification

Direct compilation of `GrandeFinale/ChallengeIntersection.lean` is green in the
pinned package environment. The full pinned `lake build` is also green: 8036
jobs, with the new module built in 18 seconds.
