# Exact RS-MCA threshold formalization

This Lean 4 package formalizes the exact support-reduction layer from
`sec:witnesses` of `experimental/rs_mca_thresholds.tex`.

It imports the shared CA/MCA definitions from the Grande Finale package and
proves the challenge-restricted exact sparsification identity for arbitrary
finite linear codes. It also proves both identities in the half-distance
sparse theorem (HD1), including the literal Reed--Solomon distance
specialization `2r ≤ n - k`. Finally, it formalizes the quadratic
mean-overlap incidence argument (MO1--MO6), the literal real-root staircase
(MO7), and proves the exact MO4 numerator for injective Reed--Solomon
evaluation codes under
`n * (k + r) ≤ (n - r)^2` and `k + 1 ≤ n - r`. The package now also certifies the exact closed-ball endpoint conversion,
target-aware quadratic and half-distance window compilers (including the
zero-budget branch), and the asymptotic first-safe certificate formula
`a = k + 1 + gn + o(n)` with radius `1 - ρ - g + o(1)`.

## Actual-error-support lift

`RsMcaThresholds/ActualErrorSupportLift.lean` formalizes the witness lift in
`Exact support and actual error support` and `Lift to the deep agreement` of
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at source
snapshot `168e9ba0`.

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| `Lift`: `S* = D \ E` | `fullAgreementSupport` | DEFINITION |
| `Lift`: membership in the full agreement set | `mem_fullAgreementSupport_iff` | PROVED |
| `Lift`: `|S*| = n - |E|` | `fullAgreementSupport_card` | PROVED |
| `Lift`: `S ⊆ S*`, same explanation, upward noncontainment | `fullAgreementSupport_witness` | PROVED |
| `Lift`: support cap `|E| ≤ r` gives MCA-badness at `n - r` | `mcaBad_lift_of_wordSupport_card_le` | PROVED |
| `Lift`: repaired identity `n - (t - 1) = n - t + 1` | `nat_sub_pred_eq_sub_add_one` | PROVED |
| `Exact support` + `Lift`: rank-depth source wrapper | `rankDepth_mcaBad_lift_of_wordSupport_card_le` | PROVED |

This module consumes the actual-error cap.  It does not prove the upstream
rank-to-support implication, identify the abstract weighted-moment theorem
with the source matrix, or construct a Route-D/RIM-to-owner adapter.

Build with the pinned toolchain:

    lake build
