import GrandeFinale.C0PeriodicF29ResidualOwner

/-!
# Periodic `q = 64`, `f = 28` two-block compiler

This module proves the algebraic two-block extraction used by the deployed
monomial `c = 0` packet.  If two periodic locators are projectively congruent
modulo `X^a`, and `2B <= a`, then their truncations below degree `2B` agree
after the same projective scaling.  For residuals written as
`A₀ + X^B A₁`, this forces both scaled coefficient-block equations explicitly
from the constant and linear coefficients of the quotient.

The result is field-generic and does not assume the literal deployed values
`B = 32,768` and `a = 67,472`.  It does not yet turn the block equations into
the residual-pencil representation, prove the `30,833` degree cut, classify
the deployed stratum, or supply a fixed-cell Hahn bound.
-/

open Polynomial
open GrandeFinale.C0PeriodicF29ResidualOwner

namespace GrandeFinale.C0PeriodicF28TwoBlockCompiler

set_option maxRecDepth 100000

/-- Split a polynomial into its constant term, linear term, and an
`X^2`-divisible tail. -/
theorem quotient_two_coeff_decomposition
    {F : Type*} [CommRing F] (Q : F[X]) :
    ∃ R : F[X],
      Q = C (Q.coeff 0) + C (Q.coeff 1) * X + X ^ 2 * R := by
  rcases (X_dvd_sub_C (p := Q)) with ⟨R₁, hR₁⟩
  have hcoeff := congrArg (fun P : F[X] ↦ P.coeff 1) hR₁
  have hcoeff' : R₁.coeff 0 = Q.coeff 1 := by
    simpa using hcoeff.symm
  rcases (X_dvd_sub_C (p := R₁)) with ⟨R₂, hR₂⟩
  refine ⟨R₂, ?_⟩
  calc
    Q = C (Q.coeff 0) + X * R₁ := by linear_combination hR₁
    _ = C (Q.coeff 0) + X * (C (Q.coeff 1) + X * R₂) := by
      have htail : R₁ = C (Q.coeff 1) + X * R₂ := by
        rw [← hcoeff']
        linear_combination hR₂
      rw [htail]
    _ = C (Q.coeff 0) + C (Q.coeff 1) * X + X ^ 2 * R₂ := by
      ring

/-- The terms below degree `2B` in the periodic locator of a two-block
residual. -/
noncomputable def twoBlockApprox
    {F : Type*} [CommSemiring F]
    (B : ℕ) (A₀ A₁ Q : F[X]) : F[X] :=
  C (Q.coeff 0) * A₀ +
    X ^ B * (C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀)

/-- The terms omitted by `twoBlockApprox` are divisible by `X^(2B)`. -/
theorem periodicLocator_sub_twoBlockApprox_dvd
    {F : Type*} [CommRing F]
    (B : ℕ) (A₀ A₁ Q : F[X]) :
    (X ^ B) ^ 2 ∣
      periodicLocator B (A₀ + X ^ B * A₁) Q -
        twoBlockApprox B A₀ A₁ Q := by
  rcases quotient_two_coeff_decomposition Q with ⟨R, hQ⟩
  have hcomp := congrArg (fun P : F[X] ↦ P.comp (X ^ B)) hQ
  simp only [add_comp, mul_comp, C_comp, X_comp, X_pow_comp] at hcomp
  refine ⟨C (Q.coeff 1) * A₁ +
    (A₀ + X ^ B * A₁) * R.comp (X ^ B), ?_⟩
  unfold periodicLocator twoBlockApprox
  rw [hcomp]
  ring

/-- If both residual blocks have degree below `B`, their two-block
approximation has degree below `2B`. -/
theorem twoBlockApprox_natDegree_lt
    {F : Type*} [CommRing F]
    (B : ℕ) (A₀ A₁ Q : F[X])
    (hA₀ : A₀.natDegree < B) (hA₁ : A₁.natDegree < B) :
    (twoBlockApprox B A₀ A₁ Q).natDegree < B * 2 := by
  have hB : 0 < B := (Nat.zero_le A₀.natDegree).trans_lt hA₀
  have hfirst : (C (Q.coeff 0) * A₀).natDegree < B :=
    (natDegree_C_mul_le _ _).trans_lt hA₀
  have hinner :
      (C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀).natDegree < B :=
    (natDegree_add_le _ _).trans_lt (max_lt
      ((natDegree_C_mul_le _ _).trans_lt hA₁)
      ((natDegree_C_mul_le _ _).trans_lt hA₀))
  have hshift :
      (X ^ B *
        (C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀)).natDegree < B * 2 := by
    have hX : (X ^ B : F[X]).natDegree ≤ B := natDegree_X_pow_le B
    calc
      (X ^ B *
          (C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀)).natDegree ≤
          (X ^ B : F[X]).natDegree +
            (C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀).natDegree :=
        natDegree_mul_le
      _ < B * 2 := by omega
  unfold twoBlockApprox
  exact (natDegree_add_le _ _).trans_lt
    (max_lt (hfirst.trans (by omega)) hshift)

/-- Projective congruence modulo `X^a` determines the entire truncation below
degree `2B` when `2B <= a`. -/
theorem twoBlockApprox_eq_of_projective
    {F : Type*} [Field F]
    (B a : ℕ) (h2Ba : B * 2 ≤ a)
    (A₁₀ A₁₁ Q₁ A₂₀ A₂₁ Q₂ : F[X]) (c : F)
    (hA₁₀ : A₁₀.natDegree < B) (hA₁₁ : A₁₁.natDegree < B)
    (hA₂₀ : A₂₀.natDegree < B) (hA₂₁ : A₂₁.natDegree < B)
    (hprojective :
      X ^ a ∣
        periodicLocator B (A₁₀ + X ^ B * A₁₁) Q₁ -
          C c * periodicLocator B (A₂₀ + X ^ B * A₂₁) Q₂) :
    twoBlockApprox B A₁₀ A₁₁ Q₁ =
      C c * twoBlockApprox B A₂₀ A₂₁ Q₂ := by
  have hprojective2 :
      (X ^ B) ^ 2 ∣
        periodicLocator B (A₁₀ + X ^ B * A₁₁) Q₁ -
          C c * periodicLocator B (A₂₀ + X ^ B * A₂₁) Q₂ := by
    have hpow : (X : F[X]) ^ (B * 2) ∣ X ^ a :=
      pow_dvd_pow (X : F[X]) h2Ba
    simpa only [pow_mul] using hpow.trans hprojective
  rcases periodicLocator_sub_twoBlockApprox_dvd B A₁₀ A₁₁ Q₁ with
    ⟨R₁, hR₁⟩
  rcases periodicLocator_sub_twoBlockApprox_dvd B A₂₀ A₂₁ Q₂ with
    ⟨R₂, hR₂⟩
  rcases hprojective2 with ⟨P, hP⟩
  have hdiv :
      (X ^ B) ^ 2 ∣
        twoBlockApprox B A₁₀ A₁₁ Q₁ -
          C c * twoBlockApprox B A₂₀ A₂₁ Q₂ := by
    refine ⟨-R₁ + P + C c * R₂, ?_⟩
    calc
      twoBlockApprox B A₁₀ A₁₁ Q₁ -
          C c * twoBlockApprox B A₂₀ A₂₁ Q₂ =
        -(periodicLocator B (A₁₀ + X ^ B * A₁₁) Q₁ -
          twoBlockApprox B A₁₀ A₁₁ Q₁) +
        (periodicLocator B (A₁₀ + X ^ B * A₁₁) Q₁ -
          C c * periodicLocator B (A₂₀ + X ^ B * A₂₁) Q₂) +
        C c * (periodicLocator B (A₂₀ + X ^ B * A₂₁) Q₂ -
          twoBlockApprox B A₂₀ A₂₁ Q₂) := by ring
      _ = -((X ^ B) ^ 2 * R₁) + (X ^ B) ^ 2 * P +
          C c * ((X ^ B) ^ 2 * R₂) := by rw [hR₁, hP, hR₂]
      _ = (X ^ B) ^ 2 * (-R₁ + P + C c * R₂) := by ring
  have hleft := twoBlockApprox_natDegree_lt B A₁₀ A₁₁ Q₁ hA₁₀ hA₁₁
  have hright :
      (C c * twoBlockApprox B A₂₀ A₂₁ Q₂).natDegree < B * 2 :=
    (natDegree_C_mul_le _ _).trans_lt
      (twoBlockApprox_natDegree_lt B A₂₀ A₂₁ Q₂ hA₂₀ hA₂₁)
  have hdiff :
      (twoBlockApprox B A₁₀ A₁₁ Q₁ -
        C c * twoBlockApprox B A₂₀ A₂₁ Q₂).natDegree < B * 2 :=
    (natDegree_sub_le _ _).trans_lt (max_lt hleft hright)
  have hzero :
      twoBlockApprox B A₁₀ A₁₁ Q₁ -
        C c * twoBlockApprox B A₂₀ A₂₁ Q₂ = 0 := by
    apply eq_zero_of_dvd_of_natDegree_lt hdiv
    simpa only [← pow_mul, natDegree_X_pow] using hdiff
  exact sub_eq_zero.mp hzero

/-- Equality of two `B`-block decompositions determines each block. -/
theorem eq_blocks_of_add_X_pow_mul_eq
    {F : Type*} [Field F]
    (B : ℕ) (A₀ A₁ R₀ R₁ : F[X])
    (hA₀ : A₀.natDegree < B) (hR₀ : R₀.natDegree < B)
    (heq : A₀ + X ^ B * A₁ = R₀ + X ^ B * R₁) :
    A₀ = R₀ ∧ A₁ = R₁ := by
  have hdiv : X ^ B ∣ A₀ - R₀ := by
    refine ⟨R₁ - A₁, ?_⟩
    linear_combination heq
  have hdiff : (A₀ - R₀).natDegree < B :=
    (natDegree_sub_le _ _).trans_lt (max_lt hA₀ hR₀)
  have hzero : A₀ - R₀ = 0 :=
    eq_zero_of_dvd_of_natDegree_lt hdiv (by simpa using hdiff)
  have hfirst : A₀ = R₀ := sub_eq_zero.mp hzero
  refine ⟨hfirst, ?_⟩
  rw [hfirst] at heq
  have htail : X ^ B * A₁ = X ^ B * R₁ := add_left_cancel heq
  exact mul_left_cancel₀ (pow_ne_zero B X_ne_zero) htail

/-- The explicit pair of low-block equations forced by a projective periodic
locator congruence. -/
theorem twoBlockApprox_blocks_eq_of_projective
    {F : Type*} [Field F]
    (B a : ℕ) (h2Ba : B * 2 ≤ a)
    (A₁₀ A₁₁ Q₁ A₂₀ A₂₁ Q₂ : F[X]) (c : F)
    (hA₁₀ : A₁₀.natDegree < B) (hA₁₁ : A₁₁.natDegree < B)
    (hA₂₀ : A₂₀.natDegree < B) (hA₂₁ : A₂₁.natDegree < B)
    (hprojective :
      X ^ a ∣
        periodicLocator B (A₁₀ + X ^ B * A₁₁) Q₁ -
          C c * periodicLocator B (A₂₀ + X ^ B * A₂₁) Q₂) :
    C (Q₁.coeff 0) * A₁₀ = C (c * Q₂.coeff 0) * A₂₀ ∧
      C (Q₁.coeff 0) * A₁₁ + C (Q₁.coeff 1) * A₁₀ =
        C c *
          (C (Q₂.coeff 0) * A₂₁ + C (Q₂.coeff 1) * A₂₀) := by
  have heq := twoBlockApprox_eq_of_projective B a h2Ba
    A₁₀ A₁₁ Q₁ A₂₀ A₂₁ Q₂ c hA₁₀ hA₁₁ hA₂₀ hA₂₁ hprojective
  unfold twoBlockApprox at heq
  have heq' :
      C (Q₁.coeff 0) * A₁₀ +
        X ^ B *
          (C (Q₁.coeff 0) * A₁₁ + C (Q₁.coeff 1) * A₁₀) =
      C (c * Q₂.coeff 0) * A₂₀ +
        X ^ B *
          (C c *
            (C (Q₂.coeff 0) * A₂₁ + C (Q₂.coeff 1) * A₂₀)) := by
    calc
      C (Q₁.coeff 0) * A₁₀ +
          X ^ B *
            (C (Q₁.coeff 0) * A₁₁ + C (Q₁.coeff 1) * A₁₀) =
        C c *
          (C (Q₂.coeff 0) * A₂₀ +
            X ^ B *
              (C (Q₂.coeff 0) * A₂₁ + C (Q₂.coeff 1) * A₂₀)) := heq
      _ = C (c * Q₂.coeff 0) * A₂₀ +
          X ^ B *
            (C c *
              (C (Q₂.coeff 0) * A₂₁ + C (Q₂.coeff 1) * A₂₀)) := by
        rw [C_mul]
        ring
  apply eq_blocks_of_add_X_pow_mul_eq B at heq'
  · exact heq'
  · exact (natDegree_C_mul_le _ _).trans_lt hA₁₀
  · exact (natDegree_C_mul_le _ _).trans_lt hA₂₀

#print axioms quotient_two_coeff_decomposition
#print axioms periodicLocator_sub_twoBlockApprox_dvd
#print axioms twoBlockApprox_blocks_eq_of_projective

end GrandeFinale.C0PeriodicF28TwoBlockCompiler
