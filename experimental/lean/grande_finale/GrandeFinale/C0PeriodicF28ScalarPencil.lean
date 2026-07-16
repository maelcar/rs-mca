import GrandeFinale.C0PeriodicF28TwoBlockCompiler

/-!
# Periodic `q = 64`, `f = 28` scalar pencil and degree cut

This module converts the two coefficient-block equations exposed by
`C0PeriodicF28TwoBlockCompiler` into the explicit reference-member pencil

`A = s * (P + theta * D)`,

where `P = U + X^B V` and `D = X^B U`.  It also proves the algebraic degree
cut: once a normalized family contains a reference member and another distinct
monic residual, a common degree bound `m` on the upper blocks forces
`natDegree U <= m`.

The direct projective-congruence theorem assumes nonzero constant coefficients
for both quotients.  The family degree theorem keeps monicity, residual
injectivity, nonzero normalization scalars, upper-block degree bounds, and the
existence of two members as explicit hypotheses.  This module does not classify
the deployed stratum, construct its finite family, prove the fixed-cell Hahn
cap, or claim a complete `c = 0` parent bound.
-/

open Polynomial
open GrandeFinale.C0PeriodicF29ResidualOwner
open GrandeFinale.C0PeriodicF28TwoBlockCompiler

namespace GrandeFinale.C0PeriodicF28ScalarPencil

/-- The normalization chosen from the constant block solves its scalar
equation. -/
theorem scale_mul_eq
    {F : Type*} [Field F]
    (q c q₀ : F) (hq : q ≠ 0) :
    q * (c * q₀ / q) = c * q₀ := by
  field_simp

/-- The parameter chosen from the two quotient coefficients solves the upper
block scalar equation. -/
theorem scale_parameter_mul_eq
    {F : Type*} [Field F]
    (q q₁ c q₀ q₀₁ : F) (hq : q ≠ 0) (hq₀ : q₀ ≠ 0) :
    q * (c * q₀ / q) * (q₀₁ / q₀ - q₁ / q) =
      c * q₀₁ - q₁ * (c * q₀ / q) := by
  field_simp

/-- Blockwise form of the explicit reference-member pencil compiler. -/
theorem blocks_eq_scaled_reference_pencil_of_block_equations
    {F : Type*} [Field F]
    (A₀ A₁ U V : F[X])
    (q q₁ c q₀ q₀₁ : F)
    (hq : q ≠ 0) (hq₀ : q₀ ≠ 0)
    (hblock₀ : C q * A₀ = C (c * q₀) * U)
    (hblock₁ :
      C q * A₁ + C q₁ * A₀ =
        C c * (C q₀ * V + C q₀₁ * U)) :
    let s := c * q₀ / q
    let theta := q₀₁ / q₀ - q₁ / q
    A₀ = C s * U ∧
      A₁ = C s * (V + C theta * U) := by
  dsimp only
  let s : F := c * q₀ / q
  let theta : F := q₀₁ / q₀ - q₁ / q
  have hs : q * s = c * q₀ :=
    scale_mul_eq q c q₀ hq
  have htheta : q * s * theta = c * q₀₁ - q₁ * s :=
    scale_parameter_mul_eq q q₁ c q₀ q₀₁ hq hq₀
  have hA₀ : A₀ = C s * U := by
    apply mul_left_cancel₀ (C_ne_zero.mpr hq)
    calc
      C q * A₀ = C (c * q₀) * U := hblock₀
      _ = C (q * s) * U := by rw [hs]
      _ = C q * (C s * U) := by rw [C_mul]; ring
  refine ⟨hA₀, ?_⟩
  have hsC : C q * C s = C c * C q₀ := by
    simpa only [C_mul] using congrArg C hs
  have hthetaC :
      (C q * C s) * C theta =
        C c * C q₀₁ - C q₁ * C s := by
    simpa only [C_mul, C_sub] using congrArg C htheta
  apply mul_left_cancel₀ (C_ne_zero.mpr hq)
  calc
    C q * A₁ =
        C c * (C q₀ * V + C q₀₁ * U) - C q₁ * A₀ := by
      linear_combination hblock₁
    _ = C c * (C q₀ * V + C q₀₁ * U) -
        C q₁ * (C s * U) := by rw [hA₀]
    _ = (C c * C q₀) * V +
        (C c * C q₀₁ - C q₁ * C s) * U := by ring
    _ = (C q * C s) * V +
        ((C q * C s) * C theta) * U := by
      rw [hthetaC, hsC]
    _ = C q * (C s * (V + C theta * U)) := by ring

/-- The two exposed coefficient-block equations give the explicit pencil
normal form relative to one reference member. -/
theorem residual_eq_scaled_reference_pencil_of_block_equations
    {F : Type*} [Field F]
    (B : ℕ) (A₀ A₁ U V : F[X])
    (q q₁ c q₀ q₀₁ : F)
    (hq : q ≠ 0) (hq₀ : q₀ ≠ 0)
    (hblock₀ : C q * A₀ = C (c * q₀) * U)
    (hblock₁ :
      C q * A₁ + C q₁ * A₀ =
        C c * (C q₀ * V + C q₀₁ * U)) :
    let s := c * q₀ / q
    let theta := q₀₁ / q₀ - q₁ / q
    A₀ + X ^ B * A₁ =
      C s *
        ((U + X ^ B * V) + C theta * (X ^ B * U)) := by
  dsimp only
  rcases blocks_eq_scaled_reference_pencil_of_block_equations
      A₀ A₁ U V q q₁ c q₀ q₀₁ hq hq₀ hblock₀ hblock₁ with
    ⟨hA₀, hA₁⟩
  rw [hA₀, hA₁]
  ring

/-- Projective periodic-locator congruence, together with nonzero quotient
constants, gives the explicit reference-member pencil normal form directly. -/
theorem residual_eq_scaled_reference_pencil_of_projective
    {F : Type*} [Field F]
    (B a : ℕ) (h2Ba : B * 2 ≤ a)
    (A₀ A₁ Q U V Qref : F[X]) (c : F)
    (hA₀ : A₀.natDegree < B) (hA₁ : A₁.natDegree < B)
    (hU : U.natDegree < B) (hV : V.natDegree < B)
    (hq : Q.coeff 0 ≠ 0) (hqref : Qref.coeff 0 ≠ 0)
    (hprojective :
      X ^ a ∣
        periodicLocator B (A₀ + X ^ B * A₁) Q -
          C c * periodicLocator B (U + X ^ B * V) Qref) :
    let s := c * Qref.coeff 0 / Q.coeff 0
    let theta := Qref.coeff 1 / Qref.coeff 0 -
      Q.coeff 1 / Q.coeff 0
    A₀ + X ^ B * A₁ =
      C s *
        ((U + X ^ B * V) + C theta * (X ^ B * U)) := by
  have hblocks := twoBlockApprox_blocks_eq_of_projective
    B a h2Ba A₀ A₁ Q U V Qref c hA₀ hA₁ hU hV hprojective
  exact residual_eq_scaled_reference_pencil_of_block_equations
    B A₀ A₁ U V (Q.coeff 0) (Q.coeff 1) c
    (Qref.coeff 0) (Qref.coeff 1) hq hqref hblocks.1 hblocks.2

/-- If the upper block stays below degree `m` while `U` rises above it, the
pencil parameter must vanish. -/
theorem parameter_eq_zero_of_topBlock_degree_le
    {F : Type*} [Field F]
    (m : ℕ) (U V W : F[X]) (s theta : F)
    (hs : s ≠ 0)
    (hV : V.natDegree ≤ m) (hW : W.natDegree ≤ m)
    (hrep : W = C s * (V + C theta * U))
    (hU : m < U.natDegree) :
    theta = 0 := by
  by_contra htheta
  have hthetaU : (C theta * U).natDegree = U.natDegree :=
    natDegree_C_mul htheta
  have hVthetaU : V.natDegree < (C theta * U).natDegree := by
    rw [hthetaU]
    omega
  have hsum : (V + C theta * U).natDegree = U.natDegree := by
    rw [natDegree_add_eq_right_of_natDegree_lt hVthetaU, hthetaU]
  have hdegree : W.natDegree = U.natDegree := by
    rw [hrep, natDegree_C_mul hs, hsum]
  omega

/-- A scalar equality between two monic polynomials has scalar one. -/
theorem monic_eq_of_eq_scaled
    {F : Type*} [Field F]
    (A R : F[X]) (s : F)
    (hA : A.Monic) (hR : R.Monic)
    (heq : A = C s * R) :
    A = R := by
  have hs : s = 1 := by
    have hlc := congrArg leadingCoeff heq
    simpa [hA.leadingCoeff, hR.leadingCoeff] using hlc.symm
  simpa [hs] using heq

/-- Two distinct monic members of the same normalized pencil force the low
block below the common upper-block degree budget. -/
theorem lowBlock_degree_le_of_distinct_monic_pair
    {F : Type*} [Field F]
    (B m : ℕ) (A₀ A₁ U V : F[X]) (s theta : F)
    (hs : s ≠ 0)
    (hA₁degree : A₁.natDegree ≤ m) (hVdegree : V.natDegree ≤ m)
    (hA₀ : A₀ = C s * U)
    (hA₁ : A₁ = C s * (V + C theta * U))
    (hmonic : (A₀ + X ^ B * A₁).Monic)
    (hrefMonic : (U + X ^ B * V).Monic)
    (hne : A₀ + X ^ B * A₁ ≠ U + X ^ B * V) :
    U.natDegree ≤ m := by
  by_contra hdegree
  have hhigh : m < U.natDegree := by omega
  have htheta : theta = 0 :=
    parameter_eq_zero_of_topBlock_degree_le
      m U V A₁ s theta hs hVdegree hA₁degree hA₁ hhigh
  apply hne
  apply monic_eq_of_eq_scaled
    (A₀ + X ^ B * A₁) (U + X ^ B * V) s hmonic hrefMonic
  rw [hA₀, hA₁, htheta]
  simp only [C_0, zero_mul, add_zero]
  ring

/-- Once a normalized pencil contains a reference member and one other
distinct monic member, its low block has degree at most the common upper-block
budget. -/
theorem lowBlock_degree_le_of_family_card_two
    {α F : Type*} [DecidableEq α] [Field F]
    (B m : ℕ) (members : Finset α) (reference : α)
    (U V : F[X]) (A₀ A₁ : α → F[X]) (s theta : α → F)
    (hcard : 2 ≤ members.card) (href : reference ∈ members)
    (hrefBlocks : A₀ reference = U ∧ A₁ reference = V)
    (hs : ∀ i ∈ members, s i ≠ 0)
    (hA₀ : ∀ i ∈ members, A₀ i = C (s i) * U)
    (hA₁ : ∀ i ∈ members,
      A₁ i = C (s i) * (V + C (theta i) * U))
    (htopDegree : ∀ i ∈ members, (A₁ i).natDegree ≤ m)
    (hVDegree : V.natDegree ≤ m)
    (hmonic : ∀ i ∈ members,
      (A₀ i + X ^ B * A₁ i).Monic)
    (hinjective : Set.InjOn
      (fun i ↦ A₀ i + X ^ B * A₁ i) members) :
    U.natDegree ≤ m := by
  have hother : ∃ i ∈ members, i ≠ reference := by
    by_contra hnone
    push_neg at hnone
    have hsub : members ⊆ {reference} := by
      intro i hi
      simp [hnone i hi]
    have hle := Finset.card_le_card hsub
    simp only [Finset.card_singleton] at hle
    omega
  rcases hother with ⟨i, hi, hine⟩
  apply lowBlock_degree_le_of_distinct_monic_pair
    B m (A₀ i) (A₁ i) U V (s i) (theta i)
  · exact hs i hi
  · exact htopDegree i hi
  · exact hVDegree
  · exact hA₀ i hi
  · exact hA₁ i hi
  · exact hmonic i hi
  · simpa [hrefBlocks.1, hrefBlocks.2] using hmonic reference href
  · intro heq
    apply hine
    apply hinjective hi href
    simpa [hrefBlocks.1, hrefBlocks.2] using heq

/-- The literal upper-block budget used by the deployed `f = 28` packet. -/
theorem lowBlock_degree_le_30833_of_family_card_two
    {α F : Type*} [DecidableEq α] [Field F]
    (B : ℕ) (members : Finset α) (reference : α)
    (U V : F[X]) (A₀ A₁ : α → F[X]) (s theta : α → F)
    (hcard : 2 ≤ members.card) (href : reference ∈ members)
    (hrefBlocks : A₀ reference = U ∧ A₁ reference = V)
    (hs : ∀ i ∈ members, s i ≠ 0)
    (hA₀ : ∀ i ∈ members, A₀ i = C (s i) * U)
    (hA₁ : ∀ i ∈ members,
      A₁ i = C (s i) * (V + C (theta i) * U))
    (htopDegree : ∀ i ∈ members, (A₁ i).natDegree ≤ 30833)
    (hVDegree : V.natDegree ≤ 30833)
    (hmonic : ∀ i ∈ members,
      (A₀ i + X ^ B * A₁ i).Monic)
    (hinjective : Set.InjOn
      (fun i ↦ A₀ i + X ^ B * A₁ i) members) :
    U.natDegree ≤ 30833 :=
  lowBlock_degree_le_of_family_card_two B 30833 members reference
    U V A₀ A₁ s theta hcard href hrefBlocks hs hA₀ hA₁ htopDegree
    hVDegree hmonic hinjective

#print axioms residual_eq_scaled_reference_pencil_of_projective
#print axioms lowBlock_degree_le_of_distinct_monic_pair
#print axioms lowBlock_degree_le_30833_of_family_card_two

end GrandeFinale.C0PeriodicF28ScalarPencil
