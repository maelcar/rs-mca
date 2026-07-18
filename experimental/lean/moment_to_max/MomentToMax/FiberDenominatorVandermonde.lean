import Mathlib

/-!
# Three-point Vandermonde resolution

This module formalizes Lemma V and Corollary V.1 in
`experimental/notes/thresholds/fiber_denominator_tension.md` at source snapshot
`ea4eb078`.

For the quadratic phase

`ψₓ = θ₀ + θ₁ x + θ₂ x²`,

the ordered triple `a < b < c` isolates `θ₂` through the exact Vandermonde
combination.  Transport to `UnitAddCircle` turns its norm into distance to the
nearest integer and gives the source's weighted and diameter inequalities.

The module proves only this exact three-point resolution kernel and its trapped
rational approximation.  It does not prove the pointwise cosine estimate, the
multi-point arithmetic-progression theorem, the measured mass law, or any
wall-regime conclusion from the source note.
-/

noncomputable section

namespace MomentToMax.FiberDenominatorVandermonde

/-- The degree-two phase `ψₓ(θ)`.

Source: Lemma V in
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
def quadraticPhase (θ₀ θ₁ θ₂ : ℝ) (x : ℤ) : ℝ :=
  θ₀ + θ₁ * x + θ₂ * x ^ 2

/-- The signed three-point Vandermonde product.  It is positive for
`a < b < c`.

Source: Lemma V in
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
def vandermondeProduct (a b c : ℤ) : ℤ :=
  (b - a) * (c - b) * (c - a)

/-- Distance to the nearest integer, represented by the norm on
`UnitAddCircle = ℝ / ℤ`.

Source: the notation `‖·‖` used in Lemma V and Corollary V.1 of
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`.
Mathlib's `UnitAddCircle.norm_eq` identifies this with `|x - round x|`. -/
def nearestIntegerDistance (x : ℝ) : ℝ :=
  ‖(x : UnitAddCircle)‖

/-- The exact three-point Vandermonde resolution identity.  This algebraic
helper is slightly more general than the source-facing block theorem below:
block membership and ordering are unnecessary for the equality itself.

Source: the exact identity in Lemma V of
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem vandermonde_resolution_identity (a b c : ℤ) (θ₀ θ₁ θ₂ : ℝ) :
    (c - b : ℝ) * quadraticPhase θ₀ θ₁ θ₂ a -
        (c - a : ℝ) * quadraticPhase θ₀ θ₁ θ₂ b +
          (b - a : ℝ) * quadraticPhase θ₀ θ₁ θ₂ c =
      (vandermondeProduct a b c : ℝ) * θ₂ := by
  simp only [quadraticPhase, vandermondeProduct, Int.cast_sub, Int.cast_mul]
  ring

/-- The weighted nearest-integer inequality from Lemma V.

Source: the first displayed inequality in Lemma V of
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem vandermonde_resolution_weighted
    (a b c : ℤ) (hab : a < b) (hbc : b < c) (θ₀ θ₁ θ₂ : ℝ) :
    nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
      (c - b : ℝ) * nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
        (c - a : ℝ) * nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          (b - a : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) := by
  have hcircle :
      (((vandermondeProduct a b c : ℤ) : ℝ) * θ₂ : UnitAddCircle) =
        (c - b) • (quadraticPhase θ₀ θ₁ θ₂ a : UnitAddCircle) -
          (c - a) • (quadraticPhase θ₀ θ₁ θ₂ b : UnitAddCircle) +
            (b - a) • (quadraticPhase θ₀ θ₁ θ₂ c : UnitAddCircle) := by
    have h := congrArg (fun x : ℝ => (x : UnitAddCircle))
      (vandermonde_resolution_identity a b c θ₀ θ₁ θ₂).symm
    simpa only [← Int.cast_sub, ← zsmul_eq_mul, AddCircle.coe_add,
      AddCircle.coe_sub, AddCircle.coe_zsmul] using h
  have habsolute :
      nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
        ‖c - b‖ * nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          ‖c - a‖ * nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
            ‖b - a‖ *
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) := by
    rw [nearestIntegerDistance, hcircle]
    calc
      ‖(c - b) • (quadraticPhase θ₀ θ₁ θ₂ a : UnitAddCircle) -
            (c - a) • (quadraticPhase θ₀ θ₁ θ₂ b : UnitAddCircle) +
            (b - a) • (quadraticPhase θ₀ θ₁ θ₂ c : UnitAddCircle)‖
          ≤ ‖(c - b) • (quadraticPhase θ₀ θ₁ θ₂ a : UnitAddCircle) -
                (c - a) • (quadraticPhase θ₀ θ₁ θ₂ b : UnitAddCircle)‖ +
              ‖(b - a) •
                (quadraticPhase θ₀ θ₁ θ₂ c : UnitAddCircle)‖ :=
            norm_add_le _ _
      _ ≤ (‖(c - b) •
                (quadraticPhase θ₀ θ₁ θ₂ a : UnitAddCircle)‖ +
              ‖(c - a) •
                (quadraticPhase θ₀ θ₁ θ₂ b : UnitAddCircle)‖) +
              ‖(b - a) •
                (quadraticPhase θ₀ θ₁ θ₂ c : UnitAddCircle)‖ := by
            gcongr
            exact norm_sub_le _ _
      _ ≤ ‖c - b‖ *
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
            ‖c - a‖ *
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
            ‖b - a‖ *
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) := by
            dsimp [nearestIntegerDistance]
            gcongr <;> apply norm_zsmul_le
  have hcb : (0 : ℝ) < c - b := by exact_mod_cast sub_pos.mpr hbc
  have hca : (0 : ℝ) < c - a := by
    exact_mod_cast sub_pos.mpr (hab.trans hbc)
  have hba : (0 : ℝ) < b - a := by exact_mod_cast sub_pos.mpr hab
  simpa [Int.norm_eq_abs, abs_of_pos hcb, abs_of_pos hca,
    abs_of_pos hba] using habsolute

/-- The diameter relaxation of the weighted nearest-integer inequality.

Source: the second displayed inequality in Lemma V of
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem vandermonde_resolution_diameter
    (a b c : ℤ) (hab : a < b) (hbc : b < c) (θ₀ θ₁ θ₂ : ℝ) :
    nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
      (c - a : ℝ) *
        (nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c)) := by
  have hweighted :=
    vandermonde_resolution_weighted a b c hab hbc θ₀ θ₁ θ₂
  have hcb : (c - b : ℝ) ≤ c - a := by
    exact_mod_cast sub_le_sub_left (le_of_lt hab) c
  have hba : (b - a : ℝ) ≤ c - a := by
    exact_mod_cast sub_le_sub_right (le_of_lt hbc) a
  have hna :
      0 ≤ nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) := norm_nonneg _
  have hnb :
      0 ≤ nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) := norm_nonneg _
  have hnc :
      0 ≤ nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) := norm_nonneg _
  calc
    nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
        (c - b : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          (c - a : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          (b - a : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) := hweighted
    _ ≤ (c - a : ℝ) *
        (nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c)) := by
      nlinarith

/-- Positivity of the ordered-triple Vandermonde product.

Source: the assertion `Vdm(T) > 0` in Lemma V of
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem vandermondeProduct_pos
    (a b c : ℤ) (hab : a < b) (hbc : b < c) :
    0 < vandermondeProduct a b c := by
  simp only [vandermondeProduct]
  exact mul_pos (mul_pos (sub_pos.mpr hab) (sub_pos.mpr hbc))
    (sub_pos.mpr (hab.trans hbc))

/-- The source's denominator ceiling `Vdm(T) ≤ diam(T)³`.

Source: Corollary V.1 in
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem vandermondeProduct_le_diameter_cube
    (a b c : ℤ) (hab : a < b) (hbc : b < c) :
    vandermondeProduct a b c ≤ (c - a) ^ 3 := by
  have hca : 0 ≤ c - a := (sub_pos.mpr (hab.trans hbc)).le
  have hcb : 0 ≤ c - b := (sub_pos.mpr hbc).le
  have hba : 0 ≤ b - a := (sub_pos.mpr hab).le
  have hcb_le : c - b ≤ c - a := by omega
  have hba_le : b - a ≤ c - a := by omega
  unfold vandermondeProduct
  calc
    (b - a) * (c - b) * (c - a) ≤
        ((c - a) * (c - a)) * (c - a) :=
      mul_le_mul_of_nonneg_right
        (mul_le_mul hba_le hcb_le hcb hca) hca
    _ = (c - a) ^ 3 := by ring

/-- Source-facing form of Lemma V for an ordered triple contained in a block.
The block's normalization and gcd conditions are not needed by this local
identity.

Source: Lemma V in
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem lemmaV_of_mem
    (V : Finset ℤ) (a b c : ℤ) (_ha : a ∈ V) (_hb : b ∈ V) (_hc : c ∈ V)
    (hab : a < b) (hbc : b < c) (θ₀ θ₁ θ₂ : ℝ) :
    (c - b : ℝ) * quadraticPhase θ₀ θ₁ θ₂ a -
          (c - a : ℝ) * quadraticPhase θ₀ θ₁ θ₂ b +
            (b - a : ℝ) * quadraticPhase θ₀ θ₁ θ₂ c =
        (vandermondeProduct a b c : ℝ) * θ₂ ∧
      0 < vandermondeProduct a b c ∧
      nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
        (c - b : ℝ) * nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          (c - a : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          (b - a : ℝ) *
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) ∧
      nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
        (c - a : ℝ) *
          (nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
            nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c)) := by
  exact ⟨vandermonde_resolution_identity a b c θ₀ θ₁ θ₂,
    vandermondeProduct_pos a b c hab hbc,
    vandermonde_resolution_weighted a b c hab hbc θ₀ θ₁ θ₂,
    vandermonde_resolution_diameter a b c hab hbc θ₀ θ₁ θ₂⟩

/-- A `w`-trapped ordered triple approximates `θ₂` by the explicit rational
`round(Vdm · θ₂) / Vdm`.  The same hypothesis makes the approximation narrower
than half a `1 / Vdm` interval, and the displayed denominator is at most the
cube of the triple's diameter.

Source: Corollary V.1 in
`experimental/notes/thresholds/fiber_denominator_tension.md` at `ea4eb078`. -/
theorem trappedTriple_rationalApproximation
    (V : Finset ℤ) (a b c : ℤ)
    (_ha : a ∈ V) (_hb : b ∈ V) (_hc : c ∈ V)
    (hab : a < b) (hbc : b < c) (θ₀ θ₁ θ₂ w : ℝ)
    (ha : nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) ≤ w)
    (hb : nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) ≤ w)
    (hc : nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) ≤ w)
    (hresolve : 3 * (c - a : ℝ) * w < 1 / 2) :
    |θ₂ - (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ) /
        (vandermondeProduct a b c : ℝ)| ≤
          3 * (c - a : ℝ) * w / (vandermondeProduct a b c : ℝ) ∧
      |θ₂ - (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ) /
          (vandermondeProduct a b c : ℝ)| <
            1 / (2 * (vandermondeProduct a b c : ℝ)) ∧
        vandermondeProduct a b c ≤ (c - a) ^ 3 := by
  have hvdmZ : 0 < vandermondeProduct a b c :=
    vandermondeProduct_pos a b c hab hbc
  have hvdm : (0 : ℝ) < (vandermondeProduct a b c : ℝ) := by
    exact_mod_cast hvdmZ
  have hdiam := vandermonde_resolution_diameter a b c hab hbc θ₀ θ₁ θ₂
  have hsum :
      nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
          nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c) ≤ 3 * w := by
    linarith
  have hdiam_nonneg : (0 : ℝ) ≤ c - a := by
    exact_mod_cast (sub_pos.mpr (hab.trans hbc)).le
  have htrap :
      nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
        3 * (c - a : ℝ) * w := by
    calc
      nearestIntegerDistance ((vandermondeProduct a b c : ℤ) * θ₂) ≤
          (c - a : ℝ) *
            (nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ a) +
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ b) +
              nearestIntegerDistance (quadraticPhase θ₀ θ₁ θ₂ c)) := hdiam
      _ ≤ (c - a : ℝ) * (3 * w) :=
        mul_le_mul_of_nonneg_left hsum hdiam_nonneg
      _ = 3 * (c - a : ℝ) * w := by ring
  have hround :
      |(vandermondeProduct a b c : ℝ) * θ₂ -
          (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ)| ≤
        3 * (c - a : ℝ) * w := by
    have hround' := htrap
    rw [nearestIntegerDistance, UnitAddCircle.norm_eq] at hround'
    exact hround'
  have hrewrite :
      θ₂ - (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ) /
          (vandermondeProduct a b c : ℝ) =
        ((vandermondeProduct a b c : ℝ) * θ₂ -
          (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ)) /
            (vandermondeProduct a b c : ℝ) := by
    field_simp
  have happrox :
      |θ₂ - (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ) /
          (vandermondeProduct a b c : ℝ)| ≤
        3 * (c - a : ℝ) * w / (vandermondeProduct a b c : ℝ) := by
    rw [hrewrite, abs_div, abs_of_pos hvdm]
    exact (div_le_div_iff_of_pos_right hvdm).mpr hround
  refine ⟨happrox, ?_,
    vandermondeProduct_le_diameter_cube a b c hab hbc⟩
  calc
    |θ₂ - (round ((vandermondeProduct a b c : ℤ) * θ₂) : ℝ) /
        (vandermondeProduct a b c : ℝ)| ≤
        3 * (c - a : ℝ) * w / (vandermondeProduct a b c : ℝ) := happrox
    _ < (1 / 2) / (vandermondeProduct a b c : ℝ) :=
      (div_lt_div_iff_of_pos_right hvdm).mpr hresolve
    _ = 1 / (2 * (vandermondeProduct a b c : ℝ)) := by field_simp

end MomentToMax.FiberDenominatorVandermonde
