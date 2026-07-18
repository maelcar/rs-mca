import Mathlib

/-!
# Exact rational arithmetic for the F7 RF3 counterexample

The definitions below are the rational values printed in the RF3' audit.  The
module certifies only their exact arithmetic and ordering around the singleton
cardinality `1`.
-/

namespace PavingRetainedFactorLift.F7Threshold

set_option autoImplicit false

def dy : ℚ := 1 / 100
def dz : ℚ := 11 / 10
def U : ℚ := 3
def alpha : ℚ := 2 * U * dy ^ 2

/-- The unguarded v9.2 RF3 right-hand side for `r = 0`. -/
def oldThreshold : ℚ := alpha * dz + dy

/-- The corrected RF3' right-hand side for `r = 0`. -/
def correctedThreshold : ℚ := max 1 alpha * dz + dy

/-- The unabsorbed content charge at integral content degree `d_C = 1`. -/
def exactContentCharge : ℚ := 1 + alpha * (dz - 1) + dy

theorem alpha_eq : alpha = 3 / 5000 := by
  norm_num [alpha, U, dy]

theorem oldThreshold_eq : oldThreshold = 533 / 50000 := by
  norm_num [oldThreshold, alpha, U, dy, dz]

/-- A singleton slope set satisfies the old strict RF3 trigger. -/
theorem oldThreshold_lt_singleton : oldThreshold < 1 := by
  norm_num [oldThreshold, alpha, U, dy, dz]

theorem correctedThreshold_eq : correctedThreshold = 111 / 100 := by
  norm_num [correctedThreshold, alpha, U, dy, dz, max_eq_left]

/-- The same singleton no longer satisfies the corrected strict trigger. -/
theorem singleton_lt_correctedThreshold : 1 < correctedThreshold := by
  norm_num [correctedThreshold, alpha, U, dy, dz, max_eq_left]

theorem exactContentCharge_eq : exactContentCharge = 50503 / 50000 := by
  norm_num [exactContentCharge, alpha, U, dy, dz]

theorem singleton_lt_exactContentCharge : 1 < exactContentCharge := by
  norm_num [exactContentCharge, alpha, U, dy, dz]

#print axioms oldThreshold_lt_singleton
#print axioms singleton_lt_correctedThreshold
#print axioms exactContentCharge_eq

end PavingRetainedFactorLift.F7Threshold
