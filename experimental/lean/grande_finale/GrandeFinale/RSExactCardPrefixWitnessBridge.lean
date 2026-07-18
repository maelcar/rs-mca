import GrandeFinale.RSExactCardWitnessBridge
import GrandeFinale.PrefixAtlasBridge

/-!
# Exact-cardinality locator-prefix witness bridge

This module partitions each finite exact-cardinality Reed--Solomon witness
catalogue by the locator prefix of its selected support.  The cells exhaust
raw witnesses.  Under injective evaluation and the parity-check dimension
hypothesis, their slope images agree with the existing support-family
locator-prefix cells.  This is
a structural locator-prefix partition, not a
C1--C9 semantic classification: cell payment and the uniform sum bound remain
explicit hypotheses.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.RSExactCardPrefixWitnessBridge

open GrandeFinale.FirstMatchWitnessBridge
open GrandeFinale.PrefixAtlasBridge
open GrandeFinale.RSExactCardWitnessBridge
open GrandeFinale.RSExactSupportUpper
open GrandeFinale.RSParityKernel
open GrandeFinale.SyndromeLine
open GrandeFinale.CollisionAwarePole

variable {D F : Type*}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]

/-- The locator-prefix key of the selected exact-cardinality support carried by
an RS witness. -/
def rsExactCardWitnessPrefixKey (ev : D -> F) (K a : Nat)
    {k : Nat} (w : RSExactCardWitness D F k) : Fin (a - K) -> F :=
  supportPrefixKey ev K a w.support

/-- The literal witness catalogue cut into cells by the locator prefix of the
selected support. -/
def rsExactCardPrefixWitnessCell (ev : D -> F) (k a K : Nat)
    (p : (D -> F) × (D -> F)) (z : Fin (a - K) -> F) :
    Finset (RSExactCardWitness D F k) :=
  (rsExactCardWitnesses ev k a p.1 p.2).filter fun w =>
    rsExactCardWitnessPrefixKey ev K a w = z

omit [DecidableEq D] in
theorem mem_rsExactCardPrefixWitnessCell_iff
    (ev : D -> F) (k a K : Nat)
    (p : (D -> F) × (D -> F)) (z : Fin (a - K) -> F)
    (w : RSExactCardWitness D F k) :
    w ∈ rsExactCardPrefixWitnessCell ev k a K p z ↔
      w ∈ rsExactCardWitnesses ev k a p.1 p.2 ∧
        rsExactCardWitnessPrefixKey ev K a w = z := by
  simp [rsExactCardPrefixWitnessCell]

/-- Prefix cells cover the finite exact-cardinality witness catalogue exactly.
This is witness-level exhaustivity, not semantic C1--C9 classification. -/
theorem rsExactCardPrefixWitnessCells_cover
    (ev : D -> F) (k a K : Nat)
    (p : (D -> F) × (D -> F)) :
    (Finset.univ : Finset (Fin (a - K) -> F)).biUnion
        (rsExactCardPrefixWitnessCell ev k a K p) =
      rsExactCardWitnesses ev k a p.1 p.2 := by
  ext w
  simp [mem_rsExactCardPrefixWitnessCell_iff]

/-- Per prefix, the slopes carried by literal exact-cardinality witnesses are
exactly the slopes carried by the corresponding support-family cell. -/
theorem rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (p : (D -> F) × (D -> F))
    (z : Fin (a - K) -> F) :
    (rsExactCardPrefixWitnessCell ev k a K p z).image
        RSExactCardWitness.slope =
      rsPrefixBadSlopeCell ev R a K p.1 p.2 z := by
  ext gamma
  constructor
  · intro hgamma
    rcases Finset.mem_image.mp hgamma with ⟨w, hwcell, rfl⟩
    rw [mem_rsExactCardPrefixWitnessCell_iff] at hwcell
    have hwvalid :
        ValidRSExactCardWitness ev k a p.1 p.2 w := by
      simpa [rsExactCardWitnesses] using hwcell.1
    have hsupport :
        w.support ∈ supportPrefixCell ev (supportsExactly a) K a z := by
      rw [mem_supportPrefixCell_iff]
      refine ⟨?_, hwcell.2⟩
      simp [supportsExactly, hwvalid.1]
    simp only [rsPrefixBadSlopeCell, badSlopeSetOnSupportFamily,
      Finset.mem_filter, Finset.mem_univ, true_and]
    refine ⟨w.support, hsupport, ?_⟩
    unfold BadOnSupport
    rw [ker_parityCheck_eq_rsEval ev hev k R hsize]
    refine ⟨?_, hwvalid.2.2⟩
    refine ⟨fun d => w.explanation.eval (ev d), ?_, ?_⟩
    · exact mem_rsEval.mpr
        ⟨w.explanation, w.explanation_degree_lt, fun _ => rfl⟩
    · intro d hd
      exact hwvalid.2.1 d hd
  · intro hgamma
    simp only [rsPrefixBadSlopeCell, badSlopeSetOnSupportFamily,
      Finset.mem_filter, Finset.mem_univ, true_and] at hgamma
    rcases hgamma with ⟨S, hScell, hbad⟩
    unfold BadOnSupport at hbad
    rw [ker_parityCheck_eq_rsEval ev hev k R hsize] at hbad
    rcases hbad.1 with ⟨c, hc, hcS⟩
    obtain ⟨P, hPdeg, hcP⟩ := mem_rsEval.mp hc
    let pLT : Polynomial.degreeLT F k :=
      ⟨P, Polynomial.mem_degreeLT.mpr hPdeg⟩
    let w : RSExactCardWitness D F k :=
      ⟨gamma, S, Polynomial.degreeLTEquiv F k pLT⟩
    apply Finset.mem_image.mpr
    refine ⟨w, ?_, rfl⟩
    rw [mem_rsExactCardPrefixWitnessCell_iff]
    refine ⟨?_, ?_⟩
    · simp only [rsExactCardWitnesses, Finset.mem_filter,
        Finset.mem_univ, true_and]
      have hSdata := (mem_supportPrefixCell_iff
        ev (supportsExactly a) K a z S).mp hScell
      refine ⟨?_, ?_, hbad.2⟩
      · exact (Finset.mem_powersetCard.mp hSdata.1).2
      · intro d hd
        calc
          w.explanation.eval (ev d) = P.eval (ev d) := by
            simp [RSExactCardWitness.explanation, w, pLT]
          _ = c d := (hcP d).symm
          _ = p.1 d + gamma * p.2 d := hcS d hd
    · exact (mem_supportPrefixCell_iff
        ev (supportsExactly a) K a z S).mp hScell |>.2

-- First-match attribution only needs a set-theoretic ordering of the finite
-- prefix key type, not an order compatible with the field operations.
local instance prefixKeyLinearOrder (n : Nat) : LinearOrder (Fin n -> F) :=
  WellOrderingRel.isWellOrder.linearOrder

/-- Slope-level first match only removes slopes from a raw prefix cell; after
the per-cell alignment, its output is a subset of the existing RS prefix
bad-slope cell. -/
theorem firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (p : (D -> F) × (D -> F))
    (z : Fin (a - K) -> F) :
    firstMatchSlopeCell
        (Finset.univ : Finset (Fin (a - K) -> F))
        (rsExactCardPrefixWitnessCell ev k a K p)
        RSExactCardWitness.slope z ⊆
      rsPrefixBadSlopeCell ev R a K p.1 p.2 z := by
  intro gamma hgamma
  have hraw :
      gamma ∈ (rsExactCardPrefixWitnessCell ev k a K p z).image
        RSExactCardWitness.slope := by
    have hfirst :
        gamma ∈ GrandeFinale.FirstMatchAddBack.firstMatchCell
          (Finset.univ : Finset (Fin (a - K) -> F))
          (fun j => (rsExactCardPrefixWitnessCell ev k a K p j).image
            RSExactCardWitness.slope) z := by
      simpa [firstMatchSlopeCell] using hgamma
    exact (GrandeFinale.FirstMatchAddBack.mem_firstMatchCell
      (Finset.univ : Finset (Fin (a - K) -> F))
      (fun j => (rsExactCardPrefixWitnessCell ev k a K p j).image
        RSExactCardWitness.slope) z gamma).mp hfirst |>.1
  rw [rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell
    ev hev k R hsize a K p z] at hraw
  exact hraw

/-- Supremum form of the concrete adapter on locator-prefix witness cells. -/
theorem B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k a K : Nat) (hka : k + 1 ≤ a)
    (U : ((D -> F) × (D -> F)) -> (Fin (a - K) -> F) -> Nat)
    (hcell : ∀ p z,
      (firstMatchSlopeCell
        (Finset.univ : Finset (Fin (a - K) -> F))
        (rsExactCardPrefixWitnessCell ev k a K p)
        RSExactCardWitness.slope z).card ≤ U p z) :
    GrandeFinale.B_MCA
      (GrandeFinale.CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤
      Finset.univ.sup (fun p : (D -> F) × (D -> F) => ∑ z, U p z) := by
  apply
    B_MCA_rsEval_le_sup_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets
      ev hev k a hka
      (fun _ => (Finset.univ : Finset (Fin (a - K) -> F)))
      (rsExactCardPrefixWitnessCell ev k a K) U
  · exact rsExactCardPrefixWitnessCells_cover ev k a K
  · intro p z _hz
    exact hcell p z

/-- Existing support-family prefix-cell budgets feed the witness-first-match
adapter via the exact per-cell alignment.  The budgets remain hypotheses. -/
theorem B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a)
    (U : ((D -> F) × (D -> F)) -> (Fin (a - K) -> F) -> Nat)
    (hcell : ∀ p z,
      (rsPrefixBadSlopeCell ev R a K p.1 p.2 z).card ≤ U p z) :
    GrandeFinale.B_MCA
      (GrandeFinale.CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤
      Finset.univ.sup (fun p : (D -> F) × (D -> F) => ∑ z, U p z) := by
  apply B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets
    ev hev k a K hka U
  intro p z
  exact (Finset.card_le_card
    (firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell
      ev hev k R hsize a K p z)).trans (hcell p z)

/-- Specialize the concrete RS adapter to locator-prefix witness cells.  The
raw catalogue exhaustivity hypothesis disappears; cell budgets and their
line-uniform sum remain explicit. -/
theorem B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k a K B : Nat) (hka : k + 1 ≤ a)
    (U : ((D -> F) × (D -> F)) -> (Fin (a - K) -> F) -> Nat)
    (hcell : ∀ p z,
      (firstMatchSlopeCell
        (Finset.univ : Finset (Fin (a - K) -> F))
        (rsExactCardPrefixWitnessCell ev k a K p)
        RSExactCardWitness.slope z).card ≤ U p z)
    (hunif : ∀ p, ∑ z, U p z ≤ B) :
    GrandeFinale.B_MCA
      (GrandeFinale.CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ B := by
  apply
    B_MCA_rsEval_le_of_exactCardWitnessExhaustive_firstMatchSlopeBudgets
      ev hev k a B hka
      (fun _ => (Finset.univ : Finset (Fin (a - K) -> F)))
      (rsExactCardPrefixWitnessCell ev k a K) U
  · exact rsExactCardPrefixWitnessCells_cover ev k a K
  · intro p z _hz
    exact hcell p z
  · intro p
    simpa using hunif p

#print axioms rsExactCardPrefixWitnessCells_cover
#print axioms rsExactCardPrefixWitnessCell_image_slope_eq_rsPrefixBadSlopeCell
#print axioms firstMatchExactCardPrefixWitnessSlopeCell_subset_rsPrefixBadSlopeCell
#print axioms B_MCA_rsEval_le_sup_of_exactCardPrefixWitness_firstMatchSlopeBudgets
#print axioms B_MCA_rsEval_le_sup_of_exactCardPrefixBadSlopeBudgets
#print axioms B_MCA_rsEval_le_of_exactCardPrefixWitness_firstMatchSlopeBudgets

end GrandeFinale.RSExactCardPrefixWitnessBridge
