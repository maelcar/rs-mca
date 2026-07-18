import GrandeFinale.PrefixPigeonhole
import GrandeFinale.RSExactSupportUpper
import GrandeFinale.SyndromeLine

/-!
# Locator-prefix atlas bridge

This module connects the concrete locator coefficient prefix used in
`PrefixPigeonhole` to the support-family bad-slope set used in `SyndromeLine`.
It formalizes the coverage half of the prefix atlas at the actual
finite-field support and slope types:

* every supplied support belongs to its coefficient-prefix cell;
* the bad slopes witnessed by the whole support family are exactly the union
  of the bad-slope sets of those cells;
* cellwise slope budgets add to a valid budget for the whole family.

The final theorem deliberately assumes the cellwise budgets.  Prefix totality
does not prove a profile count, a first-match catalogue classification, or a
numerical payment.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale.PrefixAtlasBridge

variable {D F W : Type*}
variable [Field F] [Fintype F] [DecidableEq F]
variable [Fintype D] [DecidableEq D]
variable [AddCommGroup W] [Module F W]

/-- The coefficient-prefix key of a support after embedding its domain points
in the coefficient field. -/
def supportPrefixKey (point : D -> F) (K m : Nat) (S : Finset D) :
    Fin (m - K) -> F :=
  PrefixPigeonhole.coefficientPrefix K m (SP.locator (S.image point))

/-- One cell of a supplied support family, cut out by a concrete locator
coefficient prefix. -/
def supportPrefixCell (point : D -> F) (supports : Finset (Finset D))
    (K m : Nat) (z : Fin (m - K) -> F) : Finset (Finset D) :=
  supports.filter fun S => supportPrefixKey point K m S = z

omit [Fintype F] [Fintype D] [DecidableEq D] in
theorem mem_supportPrefixCell_iff (point : D -> F)
    (supports : Finset (Finset D)) (K m : Nat)
    (z : Fin (m - K) -> F) (S : Finset D) :
    S ∈ supportPrefixCell point supports K m z ↔
      S ∈ supports ∧ supportPrefixKey point K m S = z := by
  simp [supportPrefixCell]

omit [Fintype D] in
/-- The concrete prefix cells cover exactly the supplied support family.  This
is the finite-field support-level instantiation of prefix-atlas totality. -/
theorem supportPrefixCells_cover (point : D -> F)
    (supports : Finset (Finset D)) (K m : Nat) :
    (Finset.univ : Finset (Fin (m - K) -> F)).biUnion
        (supportPrefixCell point supports K m) = supports := by
  ext S
  simp [mem_supportPrefixCell_iff]

omit [Field F] [DecidableEq F] in
/-- The ambient number of coefficient-prefix keys is exactly
`|F|^(m-K)`.  The number of nonempty realized cells can only be smaller. -/
theorem supportPrefixKey_space_card (K m : Nat) :
    (Finset.univ : Finset (Fin (m - K) -> F)).card =
      (Fintype.card F) ^ (m - K) := by
  simp

/-- The concrete coefficient fibers partition all `m`-subsets of `A`.

For the source's depth parameter `k`, the intended specialization is
`K := k + 1`; the statement remains general in `K` so that the coverage fact
is independent of that convention. -/
theorem coefficientFiber_biUnion_eq_powersetCard
    (A : Finset F) (K m : Nat) :
    (Finset.univ : Finset (Fin (m - K) -> F)).biUnion
        (PrefixPigeonhole.coefficientFiber A K m) = A.powersetCard m := by
  ext S
  simp [PrefixPigeonhole.coefficientFiber]

/-- The bad slopes witnessed by one concrete coefficient-prefix fiber. -/
def prefixBadSlopeCell (H : (F → F) →ₗ[F] W) (A : Finset F)
    (K m : Nat) (z : Fin (m - K) -> F) (u0 u1 : F -> F) : Finset F :=
  SyndromeLine.badSlopeSetOnSupportFamily H
    (PrefixPigeonhole.coefficientFiber A K m z) u0 u1

/-- Bad slopes witnessed by all `m`-subsets of `A` are exactly the union of
the bad-slope cells indexed by their concrete coefficient prefixes. -/
theorem badSlopeSetOnPowersetCard_eq_prefixCells_biUnion
    (H : (F → F) →ₗ[F] W) (A : Finset F)
    (K m : Nat) (u0 u1 : F -> F) :
    SyndromeLine.badSlopeSetOnSupportFamily H (A.powersetCard m) u0 u1 =
      (Finset.univ : Finset (Fin (m - K) -> F)).biUnion fun z =>
        prefixBadSlopeCell H A K m z u0 u1 := by
  ext gamma
  simp [SyndromeLine.badSlopeSetOnSupportFamily, prefixBadSlopeCell,
    PrefixPigeonhole.coefficientFiber]

/-- Concrete coefficient-prefix cells give an unconditional union bound for
the bad slopes witnessed by all `m`-subsets of `A`. -/
theorem badSlopeSetOnPowersetCard_card_le_sum_prefixCells
    (H : (F → F) →ₗ[F] W) (A : Finset F)
    (K m : Nat) (u0 u1 : F -> F) :
    (SyndromeLine.badSlopeSetOnSupportFamily H
      (A.powersetCard m) u0 u1).card ≤
      ∑ z : Fin (m - K) -> F,
        (prefixBadSlopeCell H A K m z u0 u1).card := by
  rw [badSlopeSetOnPowersetCard_eq_prefixCells_biUnion]
  exact Finset.card_biUnion_le

/-- Bad slopes witnessed by a supplied support family are exactly the union of
the bad-slope sets witnessed by its concrete coefficient-prefix cells. -/
theorem badSlopeSetOnSupportFamily_eq_prefixCells_biUnion
    (H : (D → F) →ₗ[F] W) (point : D -> F)
    (supports : Finset (Finset D)) (K m : Nat) (u0 u1 : D -> F) :
    SyndromeLine.badSlopeSetOnSupportFamily H supports u0 u1 =
      (Finset.univ : Finset (Fin (m - K) -> F)).biUnion fun z =>
        SyndromeLine.badSlopeSetOnSupportFamily H
          (supportPrefixCell point supports K m z) u0 u1 := by
  ext gamma
  simp [SyndromeLine.badSlopeSetOnSupportFamily, supportPrefixCell,
    supportPrefixKey]

/-- Prefix-cell bad-slope counts give an unconditional union bound for the
whole support family.  No cell payment estimate is supplied by totality. -/
theorem badSlopeSetOnSupportFamily_card_le_sum_prefixCells
    (H : (D → F) →ₗ[F] W) (point : D -> F)
    (supports : Finset (Finset D)) (K m : Nat) (u0 u1 : D -> F) :
    (SyndromeLine.badSlopeSetOnSupportFamily H supports u0 u1).card ≤
      ∑ z : Fin (m - K) -> F,
        (SyndromeLine.badSlopeSetOnSupportFamily H
          (supportPrefixCell point supports K m z) u0 u1).card := by
  rw [badSlopeSetOnSupportFamily_eq_prefixCells_biUnion]
  exact Finset.card_biUnion_le

/-- Typed coverage-to-payment interface.  If every concrete prefix cell has a
certified distinct-slope budget `U z`, then their sum bounds the whole supplied
support family.  The hypotheses are the missing payment input; coverage alone
does not construct them. -/
theorem badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets
    (H : (D → F) →ₗ[F] W) (point : D -> F)
    (supports : Finset (Finset D)) (K m : Nat) (u0 u1 : D -> F)
    (U : (Fin (m - K) -> F) -> Nat)
    (hU : ∀ z,
      (SyndromeLine.badSlopeSetOnSupportFamily H
        (supportPrefixCell point supports K m z) u0 u1).card ≤ U z) :
    (SyndromeLine.badSlopeSetOnSupportFamily H supports u0 u1).card ≤
      ∑ z, U z := by
  refine (badSlopeSetOnSupportFamily_card_le_sum_prefixCells
    H point supports K m u0 u1).trans ?_
  exact Finset.sum_le_sum fun z _hz => hU z

/-- The locator-prefix bad-slope cell for the exact-`a` support family of
an injectively evaluated Reed--Solomon code. -/
def rsPrefixBadSlopeCell (ev : D -> F) (R a K : Nat)
    (u0 u1 : D -> F) (z : Fin (a - K) -> F) : Finset F :=
  SyndromeLine.badSlopeSetOnSupportFamily
    (RSParityKernel.parityCheck ev R)
    (supportPrefixCell ev (RSExactSupportUpper.supportsExactly a) K a z)
    u0 u1

/-- Direct Reed--Solomon specialization: when `a >= k+1`, every threshold-`a`
MCA-bad slope is witnessed on an exact-`a` support, and those slopes are
exactly the union of the locator-prefix bad-slope cells.  The source convention
is `K := k+1`, giving depth `a-k-1`. -/
theorem rsMcaBadSlopes_eq_prefixCells_biUnion
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F) :
    Finset.univ.filter (fun gamma : F =>
      GrandeFinale.MCABad
        (CollisionAwarePole.rsEval ev k : Set (D -> F))
        u0 u1 a gamma) =
      (Finset.univ : Finset (Fin (a - K) -> F)).biUnion fun z =>
        rsPrefixBadSlopeCell ev R a K u0 u1 z := by
  rw [RSExactSupportUpper.mcaBadSlopes_eq_exactSupportFamily
    ev hev k R hsize a hka u0 u1]
  simpa [rsPrefixBadSlopeCell] using
    badSlopeSetOnSupportFamily_eq_prefixCells_biUnion
      (RSParityKernel.parityCheck ev R) ev
      (RSExactSupportUpper.supportsExactly a) K a u0 u1

/-- Unconditional RS coverage-to-count boundary: the full threshold-`a`
MCA bad-slope count is at most the sum of its locator-prefix cell counts. -/
theorem rsMcaBadSlopes_card_le_sum_prefixCells
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F) :
    (Finset.univ.filter (fun gamma : F =>
      GrandeFinale.MCABad
        (CollisionAwarePole.rsEval ev k : Set (D -> F))
        u0 u1 a gamma)).card ≤
      ∑ z : Fin (a - K) -> F,
        (rsPrefixBadSlopeCell ev R a K u0 u1 z).card := by
  rw [rsMcaBadSlopes_eq_prefixCells_biUnion
    ev hev k R hsize a K hka u0 u1]
  exact Finset.card_biUnion_le

/-- Typed RS payment interface.  A budget for every concrete locator-prefix
cell sums to a budget for all threshold-`a` MCA-bad slopes.  The theorem does
not construct the budgets. -/
theorem rsMcaBadSlopes_card_le_sum_prefixBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a) (u0 u1 : D -> F)
    (U : (Fin (a - K) -> F) -> Nat)
    (hU : ∀ z, (rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z) :
    (Finset.univ.filter (fun gamma : F =>
      GrandeFinale.MCABad
        (CollisionAwarePole.rsEval ev k : Set (D -> F))
        u0 u1 a gamma)).card ≤
      ∑ z, U z := by
  refine (rsMcaBadSlopes_card_le_sum_prefixCells
    ev hev k R hsize a K hka u0 u1).trans ?_
  exact Finset.sum_le_sum fun z _hz => hU z

/-- Exact fixed-row outer-line interface: prefix-cell budgets may depend on the
received line; only their sum must have a bound uniform over lines in this row. -/
theorem B_MCA_rsEval_le_of_linewise_prefixBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a)
    (U : (D -> F) -> (D -> F) -> (Fin (a - K) -> F) -> Nat)
    (B : Nat)
    (hcell : ∀ u0 u1 z,
      (rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U u0 u1 z)
    (hunif : ∀ u0 u1, ∑ z, U u0 u1 z ≤ B) :
    GrandeFinale.B_MCA
      (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤ B := by
  unfold GrandeFinale.B_MCA
  apply Finset.sup_le
  intro p _hp
  refine (rsMcaBadSlopes_card_le_sum_prefixBudgets
    ev hev k R hsize a K hka p.1 p.2 (U p.1 p.2) (hcell p.1 p.2)).trans ?_
  exact hunif p.1 p.2

/-- A line-uniform family of locator-prefix cell budgets bounds the full
Reed--Solomon MCA numerator. -/
theorem B_MCA_rsEval_le_sum_prefixBudgets
    (ev : D -> F) (hev : Function.Injective ev)
    (k R : Nat) (hsize : k + R = Fintype.card D)
    (a K : Nat) (hka : k + 1 ≤ a)
    (U : (Fin (a - K) -> F) -> Nat)
    (hU : ∀ (u0 u1 : D -> F) z,
      (rsPrefixBadSlopeCell ev R a K u0 u1 z).card ≤ U z) :
    GrandeFinale.B_MCA
      (CollisionAwarePole.rsEval ev k : Set (D -> F)) a ≤
      ∑ z, U z := by
  unfold GrandeFinale.B_MCA
  apply Finset.sup_le
  intro p _hp
  exact rsMcaBadSlopes_card_le_sum_prefixBudgets
    ev hev k R hsize a K hka p.1 p.2 U (hU p.1 p.2)

#print axioms rsPrefixBadSlopeCell
#print axioms rsMcaBadSlopes_eq_prefixCells_biUnion
#print axioms rsMcaBadSlopes_card_le_sum_prefixCells
#print axioms rsMcaBadSlopes_card_le_sum_prefixBudgets
#print axioms B_MCA_rsEval_le_of_linewise_prefixBudgets
#print axioms B_MCA_rsEval_le_sum_prefixBudgets

#print axioms supportPrefixCells_cover
#print axioms supportPrefixKey_space_card
#print axioms coefficientFiber_biUnion_eq_powersetCard
#print axioms badSlopeSetOnPowersetCard_eq_prefixCells_biUnion
#print axioms badSlopeSetOnPowersetCard_card_le_sum_prefixCells
#print axioms badSlopeSetOnSupportFamily_eq_prefixCells_biUnion
#print axioms badSlopeSetOnSupportFamily_card_le_sum_prefixCells
#print axioms badSlopeSetOnSupportFamily_card_le_sum_prefixBudgets

end GrandeFinale.PrefixAtlasBridge
