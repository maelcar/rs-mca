import Mathlib

/-!
# The RF3' content-charge envelope

This module proves the continuous arithmetic correction used for the
`ass:retained-factor-lift` content ledger in Paving v9.2.  It contains no
polynomial factorization or Hensel-lifting claim.
-/

namespace PavingRetainedFactorLift.ContentCharge

set_option autoImplicit false

/-- The content degree `d` is charged once; the remaining degree budget is
charged with coefficient `alpha`. -/
def contentCharge (alpha D d : ℝ) : ℝ := d + alpha * (D - d)

/-- Low-coefficient branch: when `alpha <= 1`, the content endpoint `d = D`
dominates the continuous interval `0 <= d <= D`. -/
theorem contentCharge_le_total_of_alpha_le_one
    (alpha D d : ℝ) (halpha : alpha ≤ 1) (hdD : d ≤ D) :
    contentCharge alpha D d ≤ D := by
  have hgap : 0 ≤ D - d := sub_nonneg.mpr hdD
  have hmul : alpha * (D - d) ≤ 1 * (D - d) :=
    mul_le_mul_of_nonneg_right halpha hgap
  unfold contentCharge
  linarith

/-- High-coefficient branch: when `1 <= alpha`, the factor endpoint `d = 0`
dominates the continuous interval. -/
theorem contentCharge_le_factor_of_one_le_alpha
    (alpha D d : ℝ) (halpha : 1 ≤ alpha) (hd0 : 0 ≤ d) :
    contentCharge alpha D d ≤ alpha * D := by
  have hnonneg : 0 ≤ (alpha - 1) * d :=
    mul_nonneg (sub_nonneg.mpr halpha) hd0
  calc
    contentCharge alpha D d = alpha * D - (alpha - 1) * d := by
      unfold contentCharge
      ring
    _ ≤ alpha * D := sub_le_self _ hnonneg

/-- The safe continuous content envelope.  This is the elementary kernel of
RF3':

`d + alpha * (D-d) <= max 1 alpha * D` for `0 <= d <= D`.
-/
theorem contentCharge_le_max
    (alpha D d : ℝ) (hd0 : 0 ≤ d) (hdD : d ≤ D) :
    contentCharge alpha D d ≤ max 1 alpha * D := by
  rcases le_total alpha 1 with halpha | halpha
  · rw [max_eq_left halpha]
    simpa using contentCharge_le_total_of_alpha_le_one alpha D d halpha hdD
  · rw [max_eq_right halpha]
    exact contentCharge_le_factor_of_one_le_alpha alpha D d halpha hd0

/-- Explicit case split underlying `contentCharge_le_max`. -/
theorem contentCharge_case_split
    (alpha D d : ℝ) (hd0 : 0 ≤ d) (hdD : d ≤ D) :
    (alpha ≤ 1 ∧ contentCharge alpha D d ≤ D) ∨
      (1 ≤ alpha ∧ contentCharge alpha D d ≤ alpha * D) := by
  rcases le_total alpha 1 with halpha | halpha
  · exact Or.inl ⟨halpha,
      contentCharge_le_total_of_alpha_le_one alpha D d halpha hdD⟩
  · exact Or.inr ⟨halpha,
      contentCharge_le_factor_of_one_le_alpha alpha D d halpha hd0⟩

/-- Adding the constrained-collinearity allowance preserves the envelope. -/
theorem contentCharge_add_le_max_add
    (alpha D d extra : ℝ) (hd0 : 0 ≤ d) (hdD : d ≤ D) :
    contentCharge alpha D d + extra ≤ max 1 alpha * D + extra := by
  simpa [add_comm] using
    add_le_add_right (contentCharge_le_max alpha D d hd0 hdD) extra

/-- RF3' specialization with `alpha = 2 U D_Y^2`. -/
theorem rf3Prime_content_envelope
    (U DY DZ d extra : ℝ) (hd0 : 0 ≤ d) (hdD : d ≤ DZ) :
    d + (2 * U * DY ^ 2) * (DZ - d) + extra ≤
      max 1 (2 * U * DY ^ 2) * DZ + extra := by
  exact contentCharge_add_le_max_add (2 * U * DY ^ 2) DZ d extra
    hd0 hdD

/-- Under the old missing guard `1 <= 2 U D_Y^2`, RF3' reduces exactly to
the printed RF3 coefficient. -/
theorem rf3Prime_reduces_to_old_of_guard
    (U DY DZ extra : ℝ) (hguard : 1 ≤ 2 * U * DY ^ 2) :
    max 1 (2 * U * DY ^ 2) * DZ + extra =
      (2 * U * DY ^ 2) * DZ + extra := by
  rw [max_eq_right hguard]

/-- The two endpoints attain the two candidate envelope values. -/
theorem contentCharge_endpoints (alpha D : ℝ) :
    contentCharge alpha D 0 = alpha * D ∧ contentCharge alpha D D = D := by
  constructor <;> simp [contentCharge]

/-- **Global-degree fallback.**  If the source audit cannot justify subtracting
the content degree from the factor budget, charging the content degree and the
entire global degree separately still gives

`d + alpha * D <= (1 + alpha) * D`.

This bound is unconditional real arithmetic.  It is deliberately weaker than
RF3' and makes no factor-lifting claim. -/
theorem globalDegreeFallback
    (alpha D d : ℝ) (hd : 0 ≤ d ∧ d ≤ D) :
    d + alpha * D ≤ (1 + alpha) * D := by
  linarith [hd.2]

#print axioms contentCharge_le_max
#print axioms contentCharge_case_split
#print axioms rf3Prime_content_envelope
#print axioms globalDegreeFallback

end PavingRetainedFactorLift.ContentCharge
