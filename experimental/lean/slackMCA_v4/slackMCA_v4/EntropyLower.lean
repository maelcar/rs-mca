import slackMCA_v4.Main

/-!
# Failure below the entropy gap (`cor:entropy-lower`)

This file formalizes the finitary core of Chojecki's corollary `cor:entropy-lower`.

The corollary states that if `σ·log₂ q ≤ (1-ε)·log₂ binom(n, s)` (where `n = |H|`,
`q = |F|`, `s = k+σ` is the agreement level), then some received word has list size at least
`2^{ε·n·H(ρ+τ) - o(n)}`.  Since `log₂ binom(n, s) = n·H(ρ+τ) - o(n)` by Stirling, the entropy
form `2^{ε·n·H(ρ+τ) - o(n)}` is exactly the asymptotic rewriting of the clean finitary bound
`binom(n, s)^ε`.  We formalize that clean bound, which is the genuine (Stirling-free)
mathematical content of the corollary and follows directly from the coefficient pigeonhole
lower bound `Chojecki.pigeonhole_lower`.
-/

open Polynomial Finset BigOperators

noncomputable section

namespace Chojecki

variable {F : Type*} [Field F]

/-
**Failure below the entropy gap (`cor:entropy-lower`, finitary form).**
Let `H` be an evaluation set over a finite field `F` with `q = |F|`, let `1 ≤ σ ≤ s ≤ |H|`,
`k = s - σ`, and let `0 ≤ ε ≤ 1`.  If
`σ · log₂ q ≤ (1 - ε) · log₂ binom(|H|, s)`,
then some monomial-prefix word `U_c` has list size at least `binom(|H|, s)^ε`.

The paper's entropy conclusion `2^{ε·n·H(ρ+τ) - o(n)}` is the Stirling rewriting of
`binom(|H|, s)^ε = 2^{ε · log₂ binom(|H|, s)}`.  (The corollary intends `ε ∈ (0,1)` as a
fixed multiplicative slack below the entropy scale, but the inequality in fact holds for every
real `ε`, so no constraint on `ε` is imposed.)
-/
theorem entropy_lower [Fintype F] [DecidableEq F] {H : Finset F} {s σ k : ℕ}
    (hσ : 1 ≤ σ) (hσs : σ ≤ s) (hsH : s ≤ H.card) (hk : k = s - σ)
    {ε : ℝ}
    (hlog : (σ : ℝ) * Real.logb 2 (Fintype.card F)
        ≤ (1 - ε) * Real.logb 2 (H.card.choose s)) :
    ∃ c : Fin σ → F,
      (H.card.choose s : ℝ) ^ ε ≤ ((codeList (Uc s σ c) H k s).ncard : ℝ) := by
  obtain ⟨ c, hc ⟩ := Chojecki.pigeonhole_lower hσ hσs hsH hk;
  refine' ⟨ c, _ ⟩;
  -- From the hypothesis `hlog`, we have `q^σ ≤ C^(1-ε)`.
  have h_q_sigma_le_C_one_minus_eps : (Fintype.card F : ℝ) ^ σ ≤ (Nat.choose H.card s : ℝ) ^ (1 - ε) := by
    rw [ ← Real.log_le_log_iff ( by positivity ) ( by exact Real.rpow_pos_of_pos ( Nat.cast_pos.mpr ( Nat.choose_pos hsH ) ) _ ), Real.log_pow, Real.log_rpow ( Nat.cast_pos.mpr ( Nat.choose_pos hsH ) ) ];
    rwa [ Real.logb, Real.logb, mul_div, mul_div, div_le_div_iff_of_pos_right ( Real.log_pos one_lt_two ) ] at hlog;
  contrapose! hc;
  refine' lt_of_le_of_lt ( mul_le_mul_of_nonneg_right h_q_sigma_le_C_one_minus_eps <| Nat.cast_nonneg _ ) _;
  refine' lt_of_lt_of_le ( mul_lt_mul_of_pos_left hc ( Real.rpow_pos_of_pos ( Nat.cast_pos.mpr ( Nat.choose_pos hsH ) ) _ ) ) _;
  rw [ ← Real.rpow_add ( Nat.cast_pos.mpr ( Nat.choose_pos hsH ) ), sub_add_cancel, Real.rpow_one ]

end Chojecki
