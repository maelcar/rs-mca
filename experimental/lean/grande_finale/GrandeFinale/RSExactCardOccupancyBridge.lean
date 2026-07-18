import GrandeFinale.RSExactCardPrefixWitnessBridge
import GrandeFinale.FirstWallMDSExtensionInverse

/-!
# Exact-cardinality retained-support occupancy bridge

This module formalizes the finite projection
`witness -> (slope, explainer) -> slope` for literal exact-cardinality
Reed--Solomon witnesses.  It proves the exact retained-support fiber sum and
the finite RC1 quotient bound, then applies that bound to post-slope-first-match
locator-prefix residuals and the fixed-row `B_MCA` numerator.

This is a projection-fiber interface, not a semantic C7 classifier or payment:
the positive lower occupancy bound and the uniform line-sum bound remain
explicit hypotheses.  No profile-scale, boundary-image, or C1--C9 routing
claim is made.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.RSExactCardOccupancyBridge

open GrandeFinale.CollisionAwarePole
open GrandeFinale.FirstMatchWitnessBridge
open GrandeFinale.FirstWallMDSExtensionInverse
open GrandeFinale.RSExactCardPrefixWitnessBridge
open GrandeFinale.RSExactCardWitnessBridge

section Occupancy

variable {D F : Type*} [DecidableEq D] [DecidableEq F]
variable {k : Nat}

/-- The explanation state `(slope, explainer coefficients)` obtained by
forgetting the selected support of a literal RS witness.  The coefficient
vector is equivalent to the degree-`<k` polynomial via `degreeLTEquiv`. -/
def explanationState (w : RSExactCardWitness D F k) :
    F × (Fin k -> F) :=
  (w.slope, w.coeffs)

/-- The realized explanation states of a finite literal witness cell. -/
def explanationStateImage (C : Finset (RSExactCardWitness D F k)) :
    Finset (F × (Fin k -> F)) :=
  C.image explanationState

/-- Witnesses in one retained explanation-state fiber. -/
def retainedSupportFiber (C : Finset (RSExactCardWitness D F k))
    (rho : F × (Fin k -> F)) : Finset (RSExactCardWitness D F k) :=
  C.filter fun w => explanationState w = rho

/-- Exact retained-support occupancy of one explanation state. -/
def retainedSupportOccupancy (C : Finset (RSExactCardWitness D F k))
    (rho : F × (Fin k -> F)) : Nat :=
  (retainedSupportFiber C rho).card

omit [DecidableEq D] in
/-- Literal witnesses split exactly over their realized explanation states. -/
theorem card_eq_sum_retainedSupportOccupancy
    (C : Finset (RSExactCardWitness D F k)) :
    C.card = ∑ rho ∈ explanationStateImage C,
      retainedSupportOccupancy C rho := by
  simpa [explanationStateImage, retainedSupportFiber,
    retainedSupportOccupancy] using
    (card_eq_sum_ownerFiber C explanationState)

omit [DecidableEq D] in
/-- On a fixed explanation-state fiber, the selected support determines the
literal witness. -/
theorem support_injOn_retainedSupportFiber
    (C : Finset (RSExactCardWitness D F k))
    (rho : F × (Fin k -> F)) :
    Set.InjOn RSExactCardWitness.support
      (↑(retainedSupportFiber C rho) : Set (RSExactCardWitness D F k)) := by
  intro w hw w' hw' hsupport
  have hwstate : explanationState w = rho :=
    (Finset.mem_filter.mp hw).2
  have hwstate' : explanationState w' = rho :=
    (Finset.mem_filter.mp hw').2
  have hstate : explanationState w = explanationState w' :=
    hwstate.trans hwstate'.symm
  have hslope : w.slope = w'.slope := congrArg Prod.fst hstate
  have hcoeffs : w.coeffs = w'.coeffs := congrArg Prod.snd hstate
  cases w
  cases w'
  simp only at hslope hsupport hcoeffs
  cases hslope
  cases hsupport
  cases hcoeffs
  rfl

/-- The fiber cardinality is literally the number of retained selected
supports, not a count with hidden witness multiplicity. -/
theorem supportImage_retainedSupportFiber_card
    (C : Finset (RSExactCardWitness D F k))
    (rho : F × (Fin k -> F)) :
    ((retainedSupportFiber C rho).image
      RSExactCardWitness.support).card = retainedSupportOccupancy C rho := by
  simpa [retainedSupportOccupancy] using
    (Finset.card_image_of_injOn
      (support_injOn_retainedSupportFiber C rho))

omit [DecidableEq D] in
/-- Exact finite RC1: if every realized explanation state retains at least
`H > 0` selected supports, the final distinct-slope image has size at most
`floor(|C| / H)`. -/
theorem slopeImage_card_le_card_div_of_retainedSupportOccupancy
    (C : Finset (RSExactCardWitness D F k)) (H : Nat) (hH : 0 < H)
    (hocc : ∀ rho ∈ explanationStateImage C,
      H ≤ retainedSupportOccupancy C rho) :
    (C.image RSExactCardWitness.slope).card ≤ C.card / H := by
  have hmul : H * (explanationStateImage C).card ≤ C.card := by
    calc
      H * (explanationStateImage C).card =
          ∑ _rho ∈ explanationStateImage C, H := by
            simp [Nat.mul_comm]
      _ ≤ ∑ rho ∈ explanationStateImage C,
          retainedSupportOccupancy C rho := Finset.sum_le_sum hocc
      _ = C.card := (card_eq_sum_retainedSupportOccupancy C).symm
  have himage :
      (explanationStateImage C).image Prod.fst =
        C.image RSExactCardWitness.slope := by
    simp [explanationStateImage, explanationState,
      Finset.image_image, Function.comp_def]
  rw [← himage]
  refine Finset.card_image_le |>.trans ?_
  rw [Nat.le_div_iff_mul_le hH]
  simpa [Nat.mul_comm] using hmul

end Occupancy

section FirstMatch

variable {D F ι : Type*} [DecidableEq D] [DecidableEq F]
variable [LinearOrder ι] {k : Nat}

omit [DecidableEq D] in
/-- RC1 applied after slope-level first match.  The occupancy hypothesis is
required only on the retained residual cell. -/
theorem firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy
    (idx : Finset ι) (cell : ι -> Finset (RSExactCardWitness D F k))
    (i : ι) (H : Nat) (hH : 0 < H)
    (hocc : ∀ rho ∈ explanationStateImage
        (firstMatchResidualWitnessCell idx cell
          RSExactCardWitness.slope i),
      H ≤ retainedSupportOccupancy
        (firstMatchResidualWitnessCell idx cell
          RSExactCardWitness.slope i) rho) :
    (firstMatchSlopeCell idx cell RSExactCardWitness.slope i).card ≤
      (firstMatchResidualWitnessCell idx cell
        RSExactCardWitness.slope i).card / H := by
  rw [← firstMatchResidualWitnessCell_image_slope]
  exact slopeImage_card_le_card_div_of_retainedSupportOccupancy
    _ H hH hocc

end FirstMatch

section PrefixAdapter

variable {D F : Type*}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

-- This well-order is used only for set-theoretic first-match attribution.
local instance prefixKeyLinearOrder (n : Nat) : LinearOrder (Fin n -> F) :=
  WellOrderingRel.isWellOrder.linearOrder

/-- The post-slope-first-match residual of one literal locator-prefix witness
cell. -/
def prefixResidualWitnessCell (ev : D -> F) (k a K : Nat)
    (p : (D -> F) × (D -> F)) (z : Fin (a - K) -> F) :
    Finset (RSExactCardWitness D F k) :=
  firstMatchResidualWitnessCell
    (Finset.univ : Finset (Fin (a - K) -> F))
    (rsExactCardPrefixWitnessCell ev k a K p)
    RSExactCardWitness.slope z

omit [DecidableEq D] in
/-- Per-cell RC1 for the structural locator-prefix witness atlas.  No semantic
C7 classification or lower occupancy bound is constructed here. -/
theorem prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy
    (ev : D -> F) (k a K : Nat)
    (p : (D -> F) × (D -> F)) (z : Fin (a - K) -> F)
    (H : Nat) (hH : 0 < H)
    (hocc : ∀ rho ∈ explanationStateImage
        (prefixResidualWitnessCell ev k a K p z),
      H ≤ retainedSupportOccupancy
        (prefixResidualWitnessCell ev k a K p z) rho) :
    (firstMatchSlopeCell
      (Finset.univ : Finset (Fin (a - K) -> F))
      (rsExactCardPrefixWitnessCell ev k a K p)
      RSExactCardWitness.slope z).card ≤
      (prefixResidualWitnessCell ev k a K p z).card / H := by
  exact firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy
    _ _ z H hH hocc

/-- Supremum-form `B_MCA` bound from explicit post-first-match retained-support
occupancy lower bounds.  The quotient sum is still line dependent. -/
theorem B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy
    (ev : D -> F) (hev : Function.Injective ev)
    (k a K : Nat) (hka : k + 1 ≤ a)
    (H : ((D -> F) × (D -> F)) -> (Fin (a - K) -> F) -> Nat)
    (hH : ∀ p z, 0 < H p z)
    (hocc : ∀ p z rho, rho ∈ explanationStateImage
        (prefixResidualWitnessCell ev k a K p z) ->
      H p z ≤ retainedSupportOccupancy
        (prefixResidualWitnessCell ev k a K p z) rho) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤
      Finset.univ.sup (fun p : (D -> F) × (D -> F) =>
        ∑ z, (prefixResidualWitnessCell ev k a K p z).card / H p z) := by
  apply B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets
    ev hev k a K hka
    (fun p z => (prefixResidualWitnessCell ev k a K p z).card / H p z)
  intro p z
  exact prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy
    ev k a K p z (H p z) (hH p z) (hocc p z)

/-- A uniform line-sum bound on the exact RC1 quotients gives a fixed
`B_MCA` bound.  The occupancy lower bounds and uniform sum remain hypotheses. -/
theorem B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy
    (ev : D -> F) (hev : Function.Injective ev)
    (k a K B : Nat) (hka : k + 1 ≤ a)
    (H : ((D -> F) × (D -> F)) -> (Fin (a - K) -> F) -> Nat)
    (hH : ∀ p z, 0 < H p z)
    (hocc : ∀ p z rho, rho ∈ explanationStateImage
        (prefixResidualWitnessCell ev k a K p z) ->
      H p z ≤ retainedSupportOccupancy
        (prefixResidualWitnessCell ev k a K p z) rho)
    (hunif : ∀ p,
      ∑ z, (prefixResidualWitnessCell ev k a K p z).card / H p z ≤ B) :
    GrandeFinale.B_MCA (rsEval ev k : Set (D -> F)) a ≤ B := by
  exact (B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy
    ev hev k a K hka H hH hocc).trans (by
      apply Finset.sup_le
      intro p _hp
      exact hunif p)

#print axioms card_eq_sum_retainedSupportOccupancy
#print axioms supportImage_retainedSupportFiber_card
#print axioms slopeImage_card_le_card_div_of_retainedSupportOccupancy
#print axioms firstMatchSlopeCell_card_le_residual_card_div_of_retainedSupportOccupancy
#print axioms prefixFirstMatchSlopeCell_card_le_residual_card_div_of_occupancy
#print axioms B_MCA_rsEval_le_sup_of_exactCardPrefixRetainedSupportOccupancy
#print axioms B_MCA_rsEval_le_of_exactCardPrefixRetainedSupportOccupancy

end PrefixAdapter

end GrandeFinale.RSExactCardOccupancyBridge
