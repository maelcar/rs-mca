import Mathlib

/-!
# RF4 forces V >= 2

This module formalizes the elementary contradiction used in the RF3' impact
audit.  If `V = 1`, positivity and `m <= V` force `m = 1`; RF4 then reads
`n * W < U * W`, while `D_X < m A`, `A <= n`, and `U = ceil(D_X)` give
`U <= n`.
-/

open Finset BigOperators

namespace PavingRetainedFactorLift.RF4ForcesVTwo

set_option autoImplicit false

/-- Left coefficient count in v9.2 equation RF4. -/
def rf4Left (K U V W : ℕ) : ℕ :=
  ∑ j ∈ Finset.range V, (U - K * j) * (W - j)

/-- Right constraint count in v9.2 equation RF4. -/
def rf4Right (n m W : ℕ) : ℕ :=
  n * ∑ s ∈ Finset.range m, (W - s) * (m - s)

/-- The RF4 contradiction after the ceiling ledger has supplied `U <= n`. -/
theorem rf4_forces_V_ge_two_of_U_le_n
    (n K m U V W : ℕ)
    (hm : 0 < m) (hmV : m ≤ V) (hUn : U ≤ n)
    (hRF4 : rf4Right n m W < rf4Left K U V W) :
    2 ≤ V := by
  by_contra hV
  have hVeq : V = 1 := by omega
  have hmeq : m = 1 := by omega
  subst V
  subst m
  simp [rf4Left, rf4Right] at hRF4
  exact (not_lt_of_ge (Nat.mul_le_mul_right W hUn)) hRF4

/-- `D_X < A <= n` and `U = ceil(D_X)` give the ceiling bound used above. -/
theorem ceilDX_le_n
    (DX : ℝ) (A n U : ℕ)
    (hUceil : U = ⌈DX⌉₊) (hDXA : DX < (A : ℝ)) (hAn : A ≤ n) :
    U ≤ n := by
  rw [hUceil]
  apply (Nat.ceil_le).2
  exact hDXA.le.trans (by exact_mod_cast hAn)

/-- Full elementary RF1/RF4 implication used by the content-repair audit.

The ordering and rank hypotheses are retained verbatim for correspondence with
v9.2 even though the `V = 1` contradiction needs only their displayed subset.
-/
theorem rf4_forces_V_ge_two
    (n A K m U V W : ℕ) (DX : ℝ)
    (hm : 0 < m)
    (_hAK : K + 2 ≤ A) (hAn : A ≤ n)
    (hmV : m ≤ V) (_hVW : V ≤ W)
    (_hRank : K * (V - 1) < U)
    (_hDXpos : 0 < DX) (hUceil : U = ⌈DX⌉₊)
    (hDX : DX < (m * A : ℕ))
    (hRF4 : rf4Right n m W < rf4Left K U V W) :
    2 ≤ V := by
  by_contra hV
  have hmeq : m = 1 := by omega
  have hDXA : DX < (A : ℝ) := by
    simpa [hmeq] using hDX
  have hUn : U ≤ n := ceilDX_le_n DX A n U hUceil hDXA hAn
  exact hV (rf4_forces_V_ge_two_of_U_le_n n K m U V W hm hmV hUn hRF4)

/-- Translating `V >= 2` back through `V = ceil(D_Y)` gives `D_Y > 1`. -/
theorem DY_gt_one_of_V_ge_two
    (DY : ℝ) (V : ℕ) (hVceil : V = ⌈DY⌉₊) (hV : 2 ≤ V) :
    1 < DY := by
  by_contra hDY
  have hDYle : DY ≤ (1 : ℝ) := le_of_not_gt hDY
  have hceil : ⌈DY⌉₊ ≤ 1 := (Nat.ceil_le).2 (by
    simpa only [Nat.cast_one] using hDYle)
  rw [hVceil] at hV
  omega

#print axioms rf4_forces_V_ge_two_of_U_le_n
#print axioms ceilDX_le_n
#print axioms rf4_forces_V_ge_two

end PavingRetainedFactorLift.RF4ForcesVTwo
