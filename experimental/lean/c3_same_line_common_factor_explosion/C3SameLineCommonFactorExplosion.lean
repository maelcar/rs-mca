import GrandeFinale.ScalarExtensionListLine

/-!
# Statement target: C3 same-line common-factor explosion

The first theorem below is a proved abstract two-stage pigeonhole kernel.  It
selects one common value which is heavy for many outer indices, with literal
natural ceiling bounds at both stages.

The final declaration records the finite C3 route cut obtained by applying
that kernel to disjoint support blocks and then using the scalar-extension
exact prefix-ray interface.  Its proof is intentionally left as a statement
target: the existing list--line and separating-pole mathematics is proved in
the imported pinned Grande Finale modules, while the support-cell
specialization and its locator divisibility bookkeeping have not yet been
checked in Lean.

This packet-local module is not imported by GrandeFinale.lean and is not
Lean-certified as a whole.
-/

open scoped BigOperators Classical
open Polynomial
open GrandeFinale

noncomputable section

namespace C3SameLineCommonFactorExplosion

/-- Two-stage ceiling pigeonhole.  For every outer index, first choose a heavy
inner fiber.  A second pigeonhole step then finds one fiber value which is the
chosen heavy value for many outer indices. -/
theorem exists_nested_ceiling_fiber
    {A R Z : Type*}
    (left : Finset A) (right : Finset R) (values : Finset Z)
    (hvalues : values.Nonempty) (f : A → R → Z)
    (hf : ∀ a ∈ left, ∀ r ∈ right, f a r ∈ values) :
    ∃ z ∈ values, ∃ heavy : Finset A,
      heavy ⊆ left ∧
      left.card ⌈/⌉ values.card ≤ heavy.card ∧
      ∀ a ∈ heavy,
        right.card ⌈/⌉ values.card ≤
          (right.filter fun r ↦ f a r = z).card := by
  classical
  have hinner : ∀ a ∈ left, ∃ z ∈ values,
      right.card ≤ values.card *
        (right.filter fun r ↦ f a r = z).card := by
    intro a ha
    exact GrandeFinale.prefix_witness_maxfiber
      (s := right) (t := values) (f := f a)
      (fun r hr ↦ hf a ha r hr) hvalues
  let pick : A → Z := fun a ↦
    if ha : a ∈ left then Classical.choose (hinner a ha)
    else Classical.choose hvalues
  have pick_mem (a : A) (ha : a ∈ left) : pick a ∈ values := by
    simp only [pick, dif_pos ha]
    exact (Classical.choose_spec (hinner a ha)).1
  have pick_bound (a : A) (ha : a ∈ left) :
      right.card ≤ values.card *
        (right.filter fun r ↦ f a r = pick a).card := by
    simp only [pick, dif_pos ha]
    exact (Classical.choose_spec (hinner a ha)).2
  obtain ⟨z, hz, houter⟩ := GrandeFinale.prefix_witness_maxfiber
    (s := left) (t := values) (f := pick)
    (fun a ha ↦ pick_mem a ha) hvalues
  let heavy := left.filter fun a ↦ pick a = z
  refine ⟨z, hz, heavy, Finset.filter_subset _ _, ?_, ?_⟩
  · rw [ceilDiv_le_iff_le_mul (Finset.card_pos.mpr hvalues)]
    simpa [heavy] using houter
  · intro a ha
    have haleft : a ∈ left := (Finset.mem_filter.mp ha).1
    have hapick : pick a = z := (Finset.mem_filter.mp ha).2
    rw [ceilDiv_le_iff_le_mul (Finset.card_pos.mpr hvalues)]
    simpa [hapick] using pick_bound a haleft

variable {B F : Type*} [Field B] [Field F] [Algebra B F]

/-- Residual supports on the right block which, after adjoining a fixed core,
land in one prescribed locator-coefficient fiber. -/
def residualPrefixCell
    (E T : Finset B) (r K m : Nat) (z : Fin (m - K) → B) :
    Finset (Finset B) :=
  (E.powersetCard r).filter fun R ↦
    PrefixPigeonhole.coefficientPrefix K m (SP.locator (T ∪ R)) = z

/-- The extension-field slope attached to a base-field prefix support. -/
def mappedSupportSlope
    (K m : Nat) (z : Fin (m - K) → B) (alpha : F)
    (S : Finset B) : F :=
  ((PrefixPigeonhole.prefixPolynomial K m z - SP.locator S).map
      (algebraMap B F)).eval alpha

/-- Full finite C3 route-cut target.  One coefficient prefix supports many
distinct planted cores, each core supports a large residual cell, and a single
extension-field pole realizes the entire coefficient fiber as distinct
MCA-bad slopes on one received line.

The stronger domain-wide field-size hypothesis avoids making the pole budget
depend on the prefix selected by the nested pigeonhole step. -/
theorem c3_sameLine_commonFactorExplosion_target
    [Fintype B] [DecidableEq B] [Fintype F] [DecidableEq F]
    (A E : Finset B) (hAE : Disjoint A E)
    (b r K m : Nat) (hKpos : 0 < K) (hKm : K ≤ m)
    (hbr : b + r = m) (hbA : b ≤ A.card) (hrE : r ≤ E.card)
    (hbudget :
      (A ∪ E).card + (K - 1) * ((A ∪ E).card.choose m).choose 2 <
        Fintype.card F) :
    ∃ z : Fin (m - K) → B, ∃ cores : Finset (Finset B), ∃ alpha : F,
      cores ⊆ A.powersetCard b ∧
      A.card.choose b ⌈/⌉ (Fintype.card B) ^ (m - K) ≤ cores.card ∧
      (∀ T ∈ cores,
        E.card.choose r ⌈/⌉ (Fintype.card B) ^ (m - K) ≤
          (residualPrefixCell E T r K m z).card) ∧
      (∀ T ∈ cores, ∀ R ∈ residualPrefixCell E T r K m z,
        T ∪ R ∈ PrefixPigeonhole.coefficientFiber (A ∪ E) K m z ∧
        SP.locator T ∣ SP.locator (T ∪ R)) ∧
      (∀ x : ↑(A ∪ E),
        ScalarExtensionListLine.extensionEval (F := F) (A ∪ E) x ≠ alpha) ∧
      Set.InjOn (mappedSupportSlope (F := F) K m z alpha)
        (PrefixPigeonhole.coefficientFiber (A ∪ E) K m z :
          Set (Finset B)) ∧
      (PrefixPigeonhole.coefficientFiber (A ∪ E) K m z).image
          (mappedSupportSlope (F := F) K m z alpha) =
        ExactListLine.badSlopeSet
          (ScalarExtensionListLine.extensionEval (F := F) (A ∪ E))
          (ScalarExtensionListLine.extensionWord (F := F)
            (fun x : ↑(A ∪ E) ↦
              (PrefixPigeonhole.prefixPolynomial K m z).eval x.1))
          alpha (K - 1) m := by
  sorry

#print axioms exists_nested_ceiling_fiber

end C3SameLineCommonFactorExplosion
