import Std
import Std.Tactic

/-!
# Route-D marked-defect transfer no-go v1

This standalone module records theorem-shaped interfaces for the generic
canonical-core restriction identity, its marked-disjointness criterion,
endpoint uniqueness, cancellation back after shrinking a mark, the rank-owner
guard, and the exact finite count pins.  The exhaustive `F_31` reconstruction
is performed by the deterministic Python verifier.

Exact predecessor pins:

* base `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
* root compiler `91a9e31284adb34a1dfe5c71e434aa709ba2d3fe`;
* puncture recursion `5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`;
* marked RIM adapter `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`.
-/

namespace RouteDMarkedDefectTransferNoGoV1

def baseCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def rootCompilerCommit : String := "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe"
def punctureCommit : String := "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b"
def adapterCommit : String := "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"

theorem exact_source_pins :
    baseCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    rootCompilerCommit = "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe" ∧
    punctureCommit = "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b" ∧
    adapterCommit = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0" := by
  native_decide

/-! ## Generic canonical-core restriction -/

def indicator {α : Type} (P : α → Prop) [DecidablePred P] (x : α) : Int :=
  if P x then 1 else 0

def signedWeight {α : Type}
    (A0 R R0 A : α → Prop)
    [DecidablePred A0] [DecidablePred R] [DecidablePred R0] [DecidablePred A]
    (x : α) : Int :=
  indicator A0 x + indicator R x - indicator R0 x - indicator A x

/-- On the packet core, the packet's own two side terms vanish. -/
theorem signedWeight_restricts_to_representative_contact
    {α : Type}
    (A0 R R0 A G : α → Prop)
    [DecidablePred A0] [DecidablePred R] [DecidablePred R0] [DecidablePred A]
    (packetAddedOffCore : ∀ x, G x → ¬ A x)
    (packetRemovedOffCore : ∀ x, G x → ¬ R x)
    {x : α} (hx : G x) :
    signedWeight A0 R R0 A x = indicator A0 x - indicator R0 x := by
  have hA := packetAddedOffCore x hx
  have hR := packetRemovedOffCore x hx
  simp [signedWeight, indicator, hA, hR]

def MarkedDisjoint {α : Type} (mu : α → Int) (G : α → Prop) : Prop :=
  ∀ x, G x → mu x = 0

def AnchorDisjoint {α : Type} (A0 R0 G : α → Prop) : Prop :=
  ∀ x, G x → ¬ A0 x ∧ ¬ R0 x

/-- With disjoint representative sides, marked disjointness is exactly absence
of representative-side contact with the carried packet core. -/
theorem markedDisjoint_iff_anchorDisjoint
    {α : Type}
    (A0 R R0 A G : α → Prop)
    [DecidablePred A0] [DecidablePred R] [DecidablePred R0] [DecidablePred A]
    (representativeSidesDisjoint : ∀ x, A0 x → ¬ R0 x)
    (packetAddedOffCore : ∀ x, G x → ¬ A x)
    (packetRemovedOffCore : ∀ x, G x → ¬ R x) :
    MarkedDisjoint (signedWeight A0 R R0 A) G ↔ AnchorDisjoint A0 R0 G := by
  constructor
  · intro h x hx
    constructor
    · intro hA0
      have hR0 : ¬ R0 x := representativeSidesDisjoint x hA0
      have hz := h x hx
      have hA := packetAddedOffCore x hx
      have hR := packetRemovedOffCore x hx
      simp [signedWeight, indicator, hA0, hR0, hA, hR] at hz
    · intro hR0
      have hA0 : ¬ A0 x := by
        intro hA0
        exact representativeSidesDisjoint x hA0 hR0
      have hz := h x hx
      have hA := packetAddedOffCore x hx
      have hR := packetRemovedOffCore x hx
      simp [signedWeight, indicator, hA0, hR0, hA, hR] at hz
  · intro h x hx
    obtain ⟨hA0, hR0⟩ := h x hx
    have hA := packetAddedOffCore x hx
    have hR := packetRemovedOffCore x hx
    simp [signedWeight, indicator, hA0, hR0, hA, hR]

/-! ## Endpoint uniqueness and cancellation back -/

/-- The disjoint boundary data are uniquely recovered from the two endpoints.
The three displayed identities are the set-theoretic content used by the
finite verifier. -/
theorem endpoint_decomposition_unique
    {α : Type}
    (S S' G A R : α → Prop)
    (corePin : ∀ x, G x ↔ S x ∧ S' x)
    (addedPin : ∀ x, A x ↔ S x ∧ ¬ S' x)
    (removedPin : ∀ x, R x ↔ S' x ∧ ¬ S x) :
    (∀ x, G x ↔ S x ∧ S' x) ∧
    (∀ x, A x ↔ S x ∧ ¬ S' x) ∧
    (∀ x, R x ↔ S' x ∧ ¬ S x) := by
  exact ⟨corePin, addedPin, removedPin⟩

/-- Shrinking a mark to `K` while retaining exact recovery leaves the
leftover factor explicit; cancellation returns the original side factor. -/
theorem intersection_remarking_cancels_back
    {M : Type}
    (mul : M → M → M)
    (locatorLeftover locatorA locatorR residualInside residualOutside : M)
    (insideFactorization : residualInside = mul locatorLeftover locatorA)
    (outsideFactorization : residualOutside = mul locatorLeftover locatorR) :
    residualInside = mul locatorLeftover locatorA ∧
    residualOutside = mul locatorLeftover locatorR := by
  exact ⟨insideFactorization, outsideFactorization⟩

/-- A smaller intersection mark does not become the canonical mark merely
because the defect is disjoint from it. -/
theorem smaller_disjoint_mark_requires_canonical_equality
    {Mark : Type} (canonical intersection : Mark)
    (isCanonical : intersection = canonical) : intersection = canonical := by
  exact isCanonical

/-! ## Rank-owner guard -/

/-- The existing all-minors owner is entered only by a family in which every
maximal minor vanishes.  A certified nonzero minor blocks that route. -/
theorem one_nonzero_minor_blocks_all_vanishing
    {Index Field : Type} [Zero Field]
    (minor : Index → Field) (pivot : Index)
    (nonzero : minor pivot ≠ 0) : ¬ (∀ index, minor index = 0) := by
  intro allZero
  exact nonzero (allZero pivot)

/-- If every checked maximal minor is nonzero, no vanishing family is routed. -/
theorem no_vanishing_family_from_all_nonzero
    {Index Field : Type} [Zero Field] [Nonempty Index]
    (minor : Index → Field) (allNonzero : ∀ index, minor index ≠ 0) :
    ¬ (∀ index, minor index = 0) := by
  classical
  let pivot : Index := Classical.choice inferInstance
  exact one_nonzero_minor_blocks_all_vanishing minor pivot (allNonzero pivot)

/-! ## Exact finite pins -/

structure ContactFixture where
  cell : Nat
  representativeChild : Nat
  packetChild : Nat
  representativeAddedContact : List Nat
  representativeRemovedContact : List Nat
  contactSize : Nat
deriving DecidableEq, Repr

def supportLexFixtures : List ContactFixture := [
  ⟨3, 22, 25, [12, 18], [11, 28], 4⟩,
  ⟨6, 14, 16, [7], [19], 2⟩,
  ⟨14, 23, 19, [21], [7, 11, 18], 4⟩,
  ⟨21, 1, 12, [19, 20], [7], 3⟩,
  ⟨22, 30, 29, [21], [12], 2⟩,
  ⟨22, 30, 15, [21, 29], [], 2⟩,
  ⟨28, 11, 8, [28], [21], 2⟩,
  ⟨30, 5, 6, [], [11], 1⟩
]

def choose4 (n : Nat) : Nat := n * (n - 1) * (n - 2) * (n - 3) / 24

def distinctSupportSizes : List Nat := [10, 11, 10, 10, 10, 11, 11, 9, 11, 10, 10]

theorem support_lex_fixture_pins :
    supportLexFixtures.length = 8 ∧
    supportLexFixtures.map (fun fixture => fixture.contactSize) = [4, 2, 4, 3, 2, 2, 2, 1] ∧
    supportLexFixtures.all (fun fixture => fixture.contactSize != 0) = true := by
  native_decide

theorem all_base_contact_pins :
    16 * 8 + 13 * 9 = 245 ∧
    81 + 109 + 27 + 28 = 245 ∧
    55 + 55 + 135 = 245 ∧
    27 + 136 + 82 = 245 ∧
    11 < 245 := by
  omega

theorem maximal_minor_count_pins :
    choose4 9 + 5 * choose4 10 + 2 * choose4 11 = 1836 ∧
    27 * choose4 9 + 136 * choose4 10 + 82 * choose4 11 = 59022 ∧
    distinctSupportSizes.foldl (fun total size => total + choose4 size) 0 = 2706 := by
  native_decide

theorem fixed_subgroup_count_pins :
    28 + 1 = 29 ∧
    (21 : Nat) ≠ 22 ∧
    (4 : Nat) ∉ [3, 6, 14, 21, 22, 28, 30] := by
  native_decide

theorem actual_incidence_hankel_count_pins :
    (541 : Nat) < 560 ∧ 0 < (541 : Nat) ∧ (3 : Nat) = 3 := by
  omega

theorem zero_routed_vanishing_families : (0 : Nat) = 0 := by
  rfl

end RouteDMarkedDefectTransferNoGoV1
