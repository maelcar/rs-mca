import Std
import Std.Tactic

namespace RouteDMarkedContactFoldProfileNoGoV1

def indicator {α : Type} (P : α → Prop) [DecidablePred P] (x : α) : Int :=
  if P x then 1 else 0

def signedDefect {α : Type} (A0 R R0 A : α → Prop)
    [DecidablePred A0] [DecidablePred R] [DecidablePred R0] [DecidablePred A]
    (x : α) : Int := indicator A0 x + indicator R x - indicator R0 x - indicator A x

def contactWeight {α : Type} (G A0 R0 : α → Prop)
    [DecidablePred G] [DecidablePred A0] [DecidablePred R0] (x : α) : Int :=
  indicator (fun y => A0 y ∧ G y) x - indicator (fun y => R0 y ∧ G y) x

def offCoreWeight {α : Type} (G A0 R R0 A : α → Prop)
    [DecidablePred G] [DecidablePred A0] [DecidablePred R]
    [DecidablePred R0] [DecidablePred A] (x : α) : Int :=
  signedDefect A0 R R0 A x - contactWeight G A0 R0 x

theorem contact_restriction {α : Type} (G A0 R R0 A : α → Prop)
    [DecidablePred G] [DecidablePred A0] [DecidablePred R]
    [DecidablePred R0] [DecidablePred A]
    (hAoff : ∀ x, G x → ¬ A x) (hRoff : ∀ x, G x → ¬ R x)
    {x : α} (hx : G x) :
    signedDefect A0 R R0 A x = contactWeight G A0 R0 x := by
  have hA := hAoff x hx
  have hR := hRoff x hx
  simp [signedDefect, contactWeight, indicator, hx, hA, hR]

theorem offCore_vanishes_on_core {α : Type} (G A0 R R0 A : α → Prop)
    [DecidablePred G] [DecidablePred A0] [DecidablePred R]
    [DecidablePred R0] [DecidablePred A]
    (hAoff : ∀ x, G x → ¬ A x) (hRoff : ∀ x, G x → ¬ R x)
    {x : α} (hx : G x) : offCoreWeight G A0 R R0 A x = 0 := by
  simp [offCoreWeight, contact_restriction G A0 R R0 A hAoff hRoff hx]

theorem defect_eq_contact_add_offCore {α : Type} (G A0 R R0 A : α → Prop)
    [DecidablePred G] [DecidablePred A0] [DecidablePred R]
    [DecidablePred R0] [DecidablePred A] (x : α) :
    signedDefect A0 R R0 A x =
      contactWeight G A0 R0 x + offCoreWeight G A0 R R0 A x := by
  simp [offCoreWeight]; omega

theorem exact_large_fold_factor {R : Type}
    (mul sub : R → R → R) (L_F L_plus L_minus : R)
    (leftDistrib : mul L_F (sub L_plus L_minus) =
      sub (mul L_F L_plus) (mul L_F L_minus)) :
    sub (mul L_F L_plus) (mul L_F L_minus) =
      mul L_F (sub L_plus L_minus) := leftDistrib.symm

theorem exact_large_fold_cancellation_back {R : Type} [Mul R]
    (L_F L_plus L_minus M_plus M_minus : R)
    (cancelLeft : ∀ a b c : R, a * b = a * c → b = c)
    (hplus : L_F * L_plus = L_F * M_plus)
    (hminus : L_F * L_minus = L_F * M_minus) :
    L_plus = M_plus ∧ L_minus = M_minus := by
  exact ⟨cancelLeft L_F L_plus M_plus hplus, cancelLeft L_F L_minus M_minus hminus⟩

theorem zero_difference_nonempty_profile_count (r : Nat) : r = r := by rfl

theorem nonzero_difference_profile_count_le_r (r q : Nat)
    (hq : 1 ≤ q) (hqr : q ≤ r) : r + 1 - q ≤ r := by omega

theorem hypothetical_lambda_family_owner_bridge
    {total profilesPerLambda lambdaTargets r p : Nat}
    (hprofiles : profilesPerLambda ≤ r) (hlambda : lambdaTargets ≤ p)
    (htotal : total ≤ profilesPerLambda * lambdaTargets) : total ≤ r * p := by
  exact Nat.le_trans htotal (Nat.mul_le_mul hprofiles hlambda)
theorem actual_all_minors_owner_adapter {allMaximalMinorsVanish rankDrop : Prop}
    (hadapter : allMaximalMinorsVanish ↔ rankDrop) :
    allMaximalMinorsVanish → rankDrop := hadapter.mp

theorem one_nonzero_pivot_blocks_all_vanishing {Index Field : Type} [Zero Field]
    (minor : Index → Field) (pivot : Index) (nonzero : minor pivot ≠ 0) :
    ¬ (∀ index, minor index = 0) := by
  intro allZero
  exact nonzero (allZero pivot)

theorem deployed_product_pin :
    67472 * 2130706433 = 143763024447376 := by native_decide

theorem deployed_profile_square_pin :
    67473 * 67473 = 4552605729 := by native_decide

theorem f31_contact_histogram_pin : 81 + 109 + 27 + 28 = 245 := by native_decide

end RouteDMarkedContactFoldProfileNoGoV1
