import GrandeFinale
import GrandeFinale.FirstMatchAddBack

/-!
# First-match witness-image bridge

First match is performed after projecting witnesses to slopes.  The residual
witness cell selects witnesses realizing the slopes assigned to a cell; its
slope image is exact, but its union need not exhaust the original witnesses
when distinct witnesses share a slope.  Every catalogue, projection identity,
first-match slope budget, and uniform sum below is an explicit hypothesis.  No
concrete Reed--Solomon atlas, prefix classification, or payment is claimed.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.FirstMatchWitnessBridge

section FirstMatchCells

variable {ω σ ι : Type*}
variable [DecidableEq σ] [LinearOrder ι]

/-- The slopes assigned to index `i` by first-match disjointization of the
slope images of the witness cells. -/
def firstMatchSlopeCell (idx : Finset ι) (cell : ι -> Finset ω)
    (slope : ω -> σ) (i : ι) : Finset σ :=
  FirstMatchAddBack.firstMatchCell idx
    (fun j => (cell j).image slope) i

/-- The witnesses in cell `i` whose slopes were assigned to `i` by slope-level
first match.  These residual cells are not asserted to cover all witnesses. -/
def firstMatchResidualWitnessCell (idx : Finset ι)
    (cell : ι -> Finset ω) (slope : ω -> σ) (i : ι) : Finset ω :=
  (cell i).filter fun w =>
    slope w ∈ firstMatchSlopeCell idx cell slope i

/-- Every first-match slope has a realizing witness in the corresponding
residual cell, and every residual witness projects to an assigned slope. -/
theorem firstMatchResidualWitnessCell_image_slope
    (idx : Finset ι) (cell : ι -> Finset ω)
    (slope : ω -> σ) (i : ι) :
    (firstMatchResidualWitnessCell idx cell slope i).image slope =
      firstMatchSlopeCell idx cell slope i := by
  apply Finset.Subset.antisymm
  · intro gamma hgamma
    rcases Finset.mem_image.mp hgamma with ⟨w, hw, rfl⟩
    exact (Finset.mem_filter.mp hw).2
  · intro gamma hgamma
    have hgamma' :
        gamma ∈ FirstMatchAddBack.firstMatchCell idx
          (fun j => (cell j).image slope) i := by
      simpa [firstMatchSlopeCell] using hgamma
    have hgammaCell : gamma ∈ (cell i).image slope :=
      (FirstMatchAddBack.mem_firstMatchCell idx
        (fun j => (cell j).image slope) i gamma).mp hgamma' |>.1
    rcases Finset.mem_image.mp hgammaCell with ⟨w, hw, hsw⟩
    refine Finset.mem_image.mpr ⟨w, ?_, hsw⟩
    exact Finset.mem_filter.mpr ⟨hw, by simpa [hsw] using hgamma⟩

end FirstMatchCells

section MCABridge

variable {D F ω ι : Type*}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]
variable [DecidableEq ω] [LinearOrder ι]

/-- A witness-exhaustive catalogue whose slope images have certified
first-match budgets bounds the exact finite-row MCA numerator by the supremum
of its line-dependent budget sums. -/
theorem B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets
    (C : Set (D -> F)) (a : Nat)
    (witnesses : ((D -> F) × (D -> F)) -> Finset ω)
    (slope : ω -> F)
    (idx : ((D -> F) × (D -> F)) -> Finset ι)
    (cell : ((D -> F) × (D -> F)) -> ι -> Finset ω)
    (U : ((D -> F) × (D -> F)) -> ι -> Nat)
    (hbadImage : ∀ p,
      Finset.univ.filter (fun gamma : F =>
        GrandeFinale.MCABad C p.1 p.2 a gamma) =
          (witnesses p).image slope)
    (hexhaust : ∀ p, (idx p).biUnion (cell p) = witnesses p)
    (hcell : ∀ p i, i ∈ idx p ->
      (firstMatchSlopeCell (idx p) (cell p) slope i).card ≤ U p i) :
    GrandeFinale.B_MCA C a ≤
      Finset.univ.sup (fun p : (D -> F) × (D -> F) =>
        ∑ i ∈ idx p, U p i) := by
  unfold GrandeFinale.B_MCA
  apply ExactProfileCompiler.profileCompiler_max_bound
  intro p _hp
  have hprojection :
      (witnesses p).image slope =
        (idx p).biUnion (fun i => (cell p i).image slope) := by
    rw [← hexhaust p, Finset.biUnion_image]
  calc
    (Finset.univ.filter (fun gamma : F =>
        GrandeFinale.MCABad C p.1 p.2 a gamma)).card =
        ((idx p).biUnion (fun i => (cell p i).image slope)).card := by
      rw [hbadImage p, hprojection]
    _ ≤ ∑ i ∈ idx p, U p i :=
      FirstMatchAddBack.firstMatch_union_card_le_sum_budget
        (idx p) (fun i => (cell p i).image slope) (U p) (by
          intro i hi
          simpa [firstMatchSlopeCell] using hcell p i hi)

/-- A uniform bound on the line-dependent first-match slope-budget sums gives
a fixed-row MCA numerator bound. -/
theorem B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets
    (C : Set (D -> F)) (a B : Nat)
    (witnesses : ((D -> F) × (D -> F)) -> Finset ω)
    (slope : ω -> F)
    (idx : ((D -> F) × (D -> F)) -> Finset ι)
    (cell : ((D -> F) × (D -> F)) -> ι -> Finset ω)
    (U : ((D -> F) × (D -> F)) -> ι -> Nat)
    (hbadImage : ∀ p,
      Finset.univ.filter (fun gamma : F =>
        GrandeFinale.MCABad C p.1 p.2 a gamma) =
          (witnesses p).image slope)
    (hexhaust : ∀ p, (idx p).biUnion (cell p) = witnesses p)
    (hcell : ∀ p i, i ∈ idx p ->
      (firstMatchSlopeCell (idx p) (cell p) slope i).card ≤ U p i)
    (hunif : ∀ p, ∑ i ∈ idx p, U p i ≤ B) :
    GrandeFinale.B_MCA C a ≤ B := by
  refine (B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets
    C a witnesses slope idx cell U hbadImage hexhaust hcell).trans ?_
  apply Finset.sup_le
  intro p _hp
  exact hunif p

end MCABridge

/-- Exact `Fin 2 -> Fin 1` countermodel: a proper subset of the witnesses can
have exactly the same slope image as the full witness family. -/
theorem slopeImage_cover_not_witnessExhaustive :
    let witnesses : Finset (Fin 2) := Finset.univ
    let chosen : Finset (Fin 2) := {0}
    let slope : Fin 2 -> Fin 1 := fun _ => 0
    chosen ⊆ witnesses ∧ chosen ≠ witnesses ∧
      chosen.image slope = witnesses.image slope := by
  decide

/-- Exact `Fin 2 -> Fin 1` countermodel: the original witness cells cover all
witnesses, but slope-level first match retains only one of two distinct
witnesses sharing the same slope. -/
theorem firstMatchResidualWitnessCells_not_witnessExhaustive :
    let witnesses : Finset (Fin 2) := Finset.univ
    let idx : Finset (Fin 2) := Finset.univ
    let cell : Fin 2 -> Finset (Fin 2) := fun i =>
      if i = 0 then {0} else {1}
    let slope : Fin 2 -> Fin 1 := fun _ => 0
    idx.biUnion cell = witnesses ∧
      idx.biUnion
        (firstMatchResidualWitnessCell idx cell slope) ≠ witnesses ∧
      idx.biUnion (firstMatchSlopeCell idx cell slope) =
        witnesses.image slope := by
  decide

#print axioms firstMatchResidualWitnessCell_image_slope
#print axioms B_MCA_le_sup_of_witnessExhaustive_firstMatchSlopeBudgets
#print axioms B_MCA_le_of_witnessExhaustive_firstMatchSlopeBudgets
#print axioms slopeImage_cover_not_witnessExhaustive
#print axioms firstMatchResidualWitnessCells_not_witnessExhaustive

end GrandeFinale.FirstMatchWitnessBridge
