import GrandeFinale.RSExactCardOccupancyBridge
import GrandeFinale.ExactProfileCompiler

/-!
# Exact-cardinality boundary-payment bridge

This module connects an actual slope-first-match cell of literal
Reed--Solomon witnesses to the finite incidence-and-moment compiler in
`ExactProfileCompiler`.

The normalization deliberately keeps two support slices separate:

* `full` supplies the boundary image and its mean fibre size;
* `residual` is the post-first-match support slice whose fibres and collision
  pairs enter the numerator.

The bridge proves the finite fibre and collision identities and instantiates
`primitiveCell_slope_card_le_floor` on the actual assigned slope set.  It does
not identify a semantic C7/C8/C9 cell.  Positive occupancy or incidence-degree
bounds, a semantic boundary map and its deployed moment payment, semantic
first-match survival, and the uniform profile sum remain explicit inputs.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.RSExactCardBoundaryPaymentBridge

open GrandeFinale.ExactProfileCompiler
open GrandeFinale.FirstMatchWitnessBridge
open GrandeFinale.RSExactCardWitnessBridge

/-- A full support slice, a retained residual slice, and their common boundary
map.  The subset proof prevents a residual-only image from being silently used
as the full normalization image. -/
structure ResidualBoundaryProfile (Support Target : Type*)
    [DecidableEq Support] where
  full : Finset Support
  residual : Finset Support
  residual_subset : residual ⊆ full
  boundary : Support -> Target

namespace ResidualBoundaryProfile

variable {Support Target : Type*}
variable [DecidableEq Support] [DecidableEq Target]

/-- Boundary values realized by the full support slice. -/
def targetImage (p : ResidualBoundaryProfile Support Target) : Finset Target :=
  p.full.image p.boundary

/-- Retained residual supports in one boundary fibre. -/
def boundaryFiber (p : ResidualBoundaryProfile Support Target)
    (s : Target) : Finset Support :=
  p.residual.filter fun x => p.boundary x = s

/-- Exact size of one retained residual boundary fibre. -/
def fiberCount (p : ResidualBoundaryProfile Support Target)
    (s : Target) : Nat :=
  (p.boundaryFiber s).card

/-- Ordered residual support pairs with equal boundary value. -/
def collisionPairs (p : ResidualBoundaryProfile Support Target) :
    Finset (Support × Support) :=
  (p.residual ×ˢ p.residual).filter fun pair =>
    p.boundary pair.1 = p.boundary pair.2

/-- Full-slice mean fibre size at the full boundary image scale. -/
def fullMean (p : ResidualBoundaryProfile Support Target) : ℝ :=
  (p.full.card : ℝ) / p.targetImage.card

/-- The retained residual fibre counts sum to the retained support count, even
when some values in the full boundary image have empty residual fibre. -/
theorem card_eq_sum_fiberCount (p : ResidualBoundaryProfile Support Target) :
    p.residual.card = ∑ s ∈ p.targetImage, p.fiberCount s := by
  simpa [targetImage, fiberCount, boundaryFiber] using
    (Finset.card_eq_sum_card_fiberwise
      (s := p.residual) (t := p.targetImage) (f := p.boundary)
      (fun x hx => Finset.mem_image_of_mem p.boundary (p.residual_subset hx)))

/-- Equal-boundary ordered pairs are exactly the second moment of the retained
residual fibre counts. -/
theorem collisionPairs_card_eq_sum_sq_fiberCount
    (p : ResidualBoundaryProfile Support Target) :
    p.collisionPairs.card =
      ∑ s ∈ p.targetImage, p.fiberCount s ^ 2 := by
  rw [Finset.card_eq_sum_card_fiberwise
    (s := p.collisionPairs) (t := p.targetImage)
    (f := fun pair => p.boundary pair.1)]
  · apply Finset.sum_congr rfl
    intro s _hs
    have hfiber :
        p.collisionPairs.filter (fun pair => p.boundary pair.1 = s) =
          p.boundaryFiber s ×ˢ p.boundaryFiber s := by
      ext pair
      simp only [collisionPairs, boundaryFiber, Finset.mem_filter,
        Finset.mem_product]
      constructor
      · rintro ⟨⟨⟨hx, hy⟩, hxy⟩, hxs⟩
        exact ⟨⟨hx, hxs⟩, hy, hxy.symm.trans hxs⟩
      · rintro ⟨⟨hx, hxs⟩, hy, hys⟩
        exact ⟨⟨⟨hx, hy⟩, hxs.trans hys.symm⟩, hxs⟩
    rw [hfiber, Finset.card_product]
    simp [fiberCount, pow_two]
  · intro pair hpair
    have hx : pair.1 ∈ p.residual :=
      (Finset.mem_product.mp (Finset.mem_filter.mp hpair).1).1
    exact Finset.mem_image_of_mem p.boundary (p.residual_subset hx)

/-- A nonempty full slice has positive full-image mean. -/
theorem fullMean_pos (p : ResidualBoundaryProfile Support Target)
    (hfull : p.full.Nonempty) :
    0 < p.fullMean := by
  have himage : p.targetImage.Nonempty := by
    simpa [targetImage] using hfull.image p.boundary
  exact div_pos (by exact_mod_cast hfull.card_pos)
    (by exact_mod_cast himage.card_pos)

end ResidualBoundaryProfile

section ActualFirstMatchCell

variable {D F ι Target : Type*}
variable [DecidableEq D] [DecidableEq F]
variable [LinearOrder ι] [DecidableEq Target]
variable {k : Nat}

/-- Selected supports retained by one actual slope-first-match residual cell. -/
def assignedResidualSupports
    (idx : Finset ι) (cell : ι -> Finset (RSExactCardWitness D F k))
    (i : ι) : Finset (Finset D) :=
  (firstMatchResidualWitnessCell idx cell
    RSExactCardWitness.slope i).image RSExactCardWitness.support

/-- Boundary profile whose residual slice is the selected-support image of one
actual slope-first-match residual cell. -/
def firstMatchBoundaryProfile
    (idx : Finset ι) (cell : ι -> Finset (RSExactCardWitness D F k))
    (i : ι) (fullSupports : Finset (Finset D))
    (Phi : Finset D -> Target)
    (hres : assignedResidualSupports idx cell i ⊆ fullSupports) :
    ResidualBoundaryProfile (Finset D) Target where
  full := fullSupports
  residual := assignedResidualSupports idx cell i
  residual_subset := hres
  boundary := Phi

/-- The exact finite boundary/ray/moment compiler applied to the *actual*
assigned slope cell.  `I`, `H`, and `J` are the C8 ray-incidence input; the
map `Phi` and the resulting residual moment are C9 boundary data.  Semantic
classification and the numerical payment comparison remain outside this
theorem. -/
theorem firstMatchSlopeCell_card_le_boundaryRayMomentFloor
    (idx : Finset ι) (cell : ι -> Finset (RSExactCardWitness D F k))
    (i : ι) (fullSupports : Finset (Finset D))
    (hfull : fullSupports.Nonempty)
    (Phi : Finset D -> Target)
    (hres : assignedResidualSupports idx cell i ⊆ fullSupports)
    (smax : Target)
    (hsmax : smax ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage)
    (hmax : ∀ s ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage,
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount s ≤
        (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount smax)
    (I : F -> ((Finset D) × (Finset D)) -> Prop) [DecidableRel I]
    (H J q : Nat) (hH : 0 < H) (hq : 2 ≤ q)
    (hleft : ∀ gamma ∈
      firstMatchSlopeCell idx cell RSExactCardWitness.slope i,
      H ≤ ((firstMatchBoundaryProfile idx cell i fullSupports Phi hres).collisionPairs.filter
        fun pair => I gamma pair).card)
    (hright : ∀ pair ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).collisionPairs,
      ((firstMatchSlopeCell idx cell RSExactCardWitness.slope i).filter
        fun gamma => I gamma pair).card ≤ J) :
    (firstMatchSlopeCell idx cell RSExactCardWitness.slope i).card ≤
      ⌊(((J : ℝ) *
          (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).residual.card) / H) *
        (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fullMean *
        (((firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage.card : ℝ) *
          residualMoment
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fullMean q) ^
              ((q : ℝ)⁻¹)⌋₊ := by
  let p := firstMatchBoundaryProfile idx cell i fullSupports Phi hres
  exact primitiveCell_slope_card_le_floor
    (firstMatchSlopeCell idx cell RSExactCardWitness.slope i)
    p.collisionPairs I p.targetImage p.fiberCount hsmax hmax
    p.residual.card H J q p.fullMean
    (p.fullMean_pos hfull) hH hq
    (p.card_eq_sum_fiberCount.symm)
    p.collisionPairs_card_eq_sum_sq_fiberCount
    hleft hright

/-- A checked comparison from the exact FC1 floor to a named integer budget
makes the actual assigned slope cell available to the existing first-match
`B_MCA` wrappers. -/
theorem firstMatchSlopeCell_card_le_boundaryRayMomentBudget
    (idx : Finset ι) (cell : ι -> Finset (RSExactCardWitness D F k))
    (i : ι) (fullSupports : Finset (Finset D))
    (hfull : fullSupports.Nonempty)
    (Phi : Finset D -> Target)
    (hres : assignedResidualSupports idx cell i ⊆ fullSupports)
    (smax : Target)
    (hsmax : smax ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage)
    (hmax : ∀ s ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage,
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount s ≤
        (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount smax)
    (I : F -> ((Finset D) × (Finset D)) -> Prop) [DecidableRel I]
    (H J q U : Nat) (hH : 0 < H) (hq : 2 ≤ q)
    (hleft : ∀ gamma ∈
      firstMatchSlopeCell idx cell RSExactCardWitness.slope i,
      H ≤ ((firstMatchBoundaryProfile idx cell i fullSupports Phi hres).collisionPairs.filter
        fun pair => I gamma pair).card)
    (hright : ∀ pair ∈
      (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).collisionPairs,
      ((firstMatchSlopeCell idx cell RSExactCardWitness.slope i).filter
        fun gamma => I gamma pair).card ≤ J)
    (hpaid :
      ⌊(((J : ℝ) *
          (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).residual.card) / H) *
        (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fullMean *
        (((firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage.card : ℝ) *
          residualMoment
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).targetImage
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fiberCount
            (firstMatchBoundaryProfile idx cell i fullSupports Phi hres).fullMean q) ^
              ((q : ℝ)⁻¹)⌋₊ ≤ U) :
    (firstMatchSlopeCell idx cell RSExactCardWitness.slope i).card ≤ U := by
  exact (firstMatchSlopeCell_card_le_boundaryRayMomentFloor
    idx cell i fullSupports hfull Phi hres smax hsmax hmax I H J q hH hq
    hleft hright).trans hpaid

#print axioms ResidualBoundaryProfile.card_eq_sum_fiberCount
#print axioms ResidualBoundaryProfile.collisionPairs_card_eq_sum_sq_fiberCount
#print axioms ResidualBoundaryProfile.fullMean_pos
#print axioms firstMatchSlopeCell_card_le_boundaryRayMomentFloor
#print axioms firstMatchSlopeCell_card_le_boundaryRayMomentBudget

end ActualFirstMatchCell

end GrandeFinale.RSExactCardBoundaryPaymentBridge
