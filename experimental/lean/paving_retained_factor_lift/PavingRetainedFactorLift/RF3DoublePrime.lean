import Mathlib

/-!
# Exact RF3'' arithmetic for the four printed KoalaBear rows

RF3'' is the conservative global-degree fallback obtained by replacing the
candidate content-free subtraction with the unconditional charge

`(1 + 2 U D_Y^2) D_Z + (r+1) D_Y`.

This module proves only exact rational ceiling and budget arithmetic.  It does
not assert or discharge the retained factor lift.
-/

namespace PavingRetainedFactorLift.RF3DoublePrime

set_option autoImplicit false

/-- The convention-safe positive perturbation used by the printed rows. -/
def epsilon : ℚ := 1 / 2 ^ 64

def DY (V : ℕ) : ℚ := ((V - 1 : ℕ) : ℚ) + epsilon
def DZ (W : ℕ) : ℚ := ((W - 1 : ℕ) : ℚ) + epsilon

/-- Conservative RF3'' threshold before taking the ceiling. -/
def threshold (r U V W : ℕ) : ℚ :=
  (1 + 2 * (U : ℚ) * DY V ^ 2) * DZ W + ((r + 1 : ℕ) : ℚ) * DY V

/-- Exact characterization of a positive integer ceiling. -/
def IsExactCeiling (x : ℚ) (N : ℕ) : Prop :=
  ((N : ℚ) - 1 < x) ∧ (x ≤ (N : ℚ))

def halfNumerator : ℕ := 274589064742753629
def quarterNumerator : ℕ := 274721012201293956
def eighthNumerator : ℕ := 274578888391562205
def sixteenthNumerator : ℕ := 274861787390263486
def securityBudget : ℕ := 274980728111395087

theorem half_exact_ceiling :
    IsExactCeiling (threshold 611982 176735230 169 27525) halfNumerator := by
  norm_num [IsExactCeiling, threshold, DY, DZ, epsilon, halfNumerator]

theorem quarter_exact_ceiling :
    IsExactCeiling (threshold 1045433 109378776 209 29028) quarterNumerator := by
  norm_num [IsExactCeiling, threshold, DY, DZ, epsilon, quarterNumerator]

theorem eighth_exact_ceiling :
    IsExactCeiling (threshold 1352390 67028580 256 31500) eighthNumerator := by
  norm_num [IsExactCeiling, threshold, DY, DZ, epsilon, eighthNumerator]

theorem sixteenth_exact_ceiling :
    IsExactCeiling (threshold 1569744 41137824 314 34101)
      sixteenthNumerator := by
  norm_num [IsExactCeiling, threshold, DY, DZ, epsilon, sixteenthNumerator]

/-- All four exact RF3'' ceilings stay below the printed 128-bit numerator
budget. -/
theorem all_numerators_le_securityBudget :
    halfNumerator ≤ securityBudget ∧
      quarterNumerator ≤ securityBudget ∧
      eighthNumerator ≤ securityBudget ∧
      sixteenthNumerator ≤ securityBudget := by
  norm_num [halfNumerator, quarterNumerator, eighthNumerator,
    sixteenthNumerator, securityBudget]

#print axioms half_exact_ceiling
#print axioms quarter_exact_ceiling
#print axioms eighth_exact_ceiling
#print axioms sixteenth_exact_ceiling
#print axioms all_numerators_le_securityBudget

end PavingRetainedFactorLift.RF3DoublePrime
