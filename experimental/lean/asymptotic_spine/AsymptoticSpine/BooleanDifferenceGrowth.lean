import AsymptoticSpine.PrimitiveBoolean
import AsymptoticSpine.BooleanDifferenceGrowthNat

namespace AsymptoticSpine

/-!
# Structural Boolean difference growth

This module supplies the finite-set scaffolding for induction on a Boolean
coordinate.  Unlike `BoolFamily`, the point families here need not lie in a
fixed-weight slice.  Splitting at the first bit gives duplicate-free tail
families, while a mixed difference set splits exactly into the three possible
first-coordinate values `-1`, `0`, and `1`.

The arithmetic combination is available from
`BooleanDifferenceGrowthNat.lean`.  Together they prove the exact mixed growth
bound `|A-B|² ≥ |A|²|B|`; the self-difference specialization discharges the
quasicube input used by `NoHighEnergy.lean`.
-/

/-! ## General Boolean point families and mixed differences -/

/-- A finite duplicate-free family of Boolean vectors in a fixed dimension. -/
structure BooleanPointFamily (n : Nat) where
  points : List (Vector Bool n)
  points_nodup : points.Nodup

namespace BooleanPointFamily

/-- Cardinality of a general Boolean point family. -/
def card (F : BooleanPointFamily n) : Nat :=
  F.points.length

end BooleanPointFamily

/-- Raw mixed differences `a-b`, retaining ordered-pair multiplicity. -/
def mixedRawDifferences (A B : BooleanPointFamily n) : List (Vector Int n) :=
  A.points.flatMap fun a => B.points.map fun b => bitDifference a b

/-- Mixed difference set, deduplicated in first-occurrence order. -/
def mixedDifferenceSet (A B : BooleanPointFamily n) : List (Vector Int n) :=
  (mixedRawDifferences A B).eraseDups

/-- Cardinality of the exact mixed difference set. -/
def mixedDiffCard (A B : BooleanPointFamily n) : Nat :=
  (mixedDifferenceSet A B).length

/-- Exact membership in a mixed difference set. -/
theorem mem_mixedDifferenceSet_iff (A B : BooleanPointFamily n)
    (z : Vector Int n) :
    z ∈ mixedDifferenceSet A B ↔
      ∃ a ∈ A.points, ∃ b ∈ B.points, bitDifference a b = z := by
  simp [mixedDifferenceSet, mixedRawDifferences,
    List.mem_flatMap, List.mem_map]

/-- `eraseDups` is duplicate-free when Boolean equality is lawful.  This
stdlib fact is proved here because Lean's core API exposes membership, but no
named `Nodup` theorem for `eraseDups`. -/
theorem nodup_eraseDups_local {α : Type} [BEq α] [LawfulBEq α] :
    ∀ xs : List α, xs.eraseDups.Nodup
  | [] => by simp
  | a :: as => by
      rw [List.eraseDups_cons, List.nodup_cons]
      constructor
      · intro ha
        rw [List.mem_eraseDups] at ha
        have haa := (List.mem_filter.mp ha).2
        simp at haa
      · exact nodup_eraseDups_local (as.filter fun b => !b == a)
  termination_by xs => xs.length
  decreasing_by
    have hle : (as.filter fun b => !b == a).length ≤ as.length :=
      List.filter_sublist.length_le
    simpa only [List.length_cons] using Nat.lt_succ_of_le hle

/-- The canonical mixed difference list really is duplicate-free. -/
theorem mixedDifferenceSet_nodup (A B : BooleanPointFamily n) :
    (mixedDifferenceSet A B).Nodup := by
  exact nodup_eraseDups_local _

/-- A duplicate-free source list cannot be longer than a list containing all
of its members.  The target list need not be duplicate-free. -/
theorem length_le_of_subset_of_nodup {α : Type} {xs ys : List α}
    (hxs : xs.Nodup) (hsub : xs ⊆ ys) : xs.length ≤ ys.length := by
  induction xs generalizing ys with
  | nil => simp
  | cons a xs ih =>
      have ha : a ∉ xs := (List.nodup_cons.mp hxs).1
      have htail : xs.Nodup := (List.nodup_cons.mp hxs).2
      have hay : a ∈ ys := hsub (by simp)
      obtain ⟨before, after, hy⟩ := List.append_of_mem hay
      subst ys
      have hsub' : xs ⊆ before ++ after := by
        intro x hx
        have hxcons : x ∈ a :: xs := List.Mem.tail a hx
        have hxall : x ∈ before ++ a :: after := hsub hxcons
        simp only [List.mem_append, List.mem_cons] at hxall ⊢
        rcases hxall with hbefore | hxa | hafter
        · exact Or.inl hbefore
        · exact (ha (hxa ▸ hx)).elim
        · exact Or.inr hafter
      have hle := ih htail hsub'
      simp only [List.length_append] at hle
      simp only [List.length_cons, List.length_append]
      omega

/-! ## Head and tail coordinates -/

/-- First coordinate of a nonempty vector. -/
def vectorHead {α : Type} {n : Nat} (x : Vector α (n + 1)) : α :=
  x[0]

/-- All coordinates after the first. -/
def vectorTail {α : Type} {n : Nat} (x : Vector α (n + 1)) : Vector α n :=
  Vector.ofFn fun i => x[i.val + 1]

/-- A nonempty vector is determined by its head and tail. -/
theorem vector_eq_of_head_eq_tail_eq {α : Type} {n : Nat}
    {x y : Vector α (n + 1)}
    (hhead : vectorHead x = vectorHead y)
    (htail : vectorTail x = vectorTail y) : x = y := by
  apply Vector.ext
  intro i hi
  by_cases hzero : i = 0
  · subst i
    simpa [vectorHead] using hhead
  · have hpred : i - 1 < n := by omega
    have ht := congrArg (fun v : Vector α n => v[i - 1]'hpred) htail
    have hidx : i - 1 + 1 = i := by omega
    simpa [vectorTail, hidx] using ht

/-- Tail is injective on vectors with one fixed head. -/
theorem vectorTail_injective_of_head_eq {α : Type} {n : Nat}
    {x y : Vector α (n + 1)} (hhead : vectorHead x = vectorHead y)
    (htail : vectorTail x = vectorTail y) : x = y :=
  vector_eq_of_head_eq_tail_eq hhead htail

/-- The head of a Boolean difference is the difference of its head bits. -/
@[simp] theorem vectorHead_bitDifference {n : Nat}
    (a b : Vector Bool (n + 1)) :
    vectorHead (bitDifference a b) = bitVal (vectorHead a) - bitVal (vectorHead b) := by
  simp [vectorHead, bitDifference]

/-- Taking tails commutes with coordinatewise Boolean difference. -/
@[simp] theorem vectorTail_bitDifference {n : Nat}
    (a b : Vector Bool (n + 1)) :
    vectorTail (bitDifference a b) = bitDifference (vectorTail a) (vectorTail b) := by
  apply Vector.ext
  intro i hi
  simp [vectorTail, bitDifference]

/-- An injective map on the members of a duplicate-free list has a
duplicate-free image. -/
theorem nodup_map_of_injective_on {α β : Type} (f : α → β) :
    ∀ xs : List α, xs.Nodup →
      (∀ a ∈ xs, ∀ b ∈ xs, f a = f b → a = b) →
      (xs.map f).Nodup
  | [], _, _ => by simp
  | a :: as, hnodup, hinj => by
      rw [List.nodup_cons] at hnodup
      rw [List.map_cons, List.nodup_cons]
      constructor
      · intro ha
        rw [List.mem_map] at ha
        obtain ⟨b, hb, hba⟩ := ha
        have hab : b = a := hinj b (by simp [hb]) a (by simp) hba
        subst b
        exact hnodup.1 hb
      · apply nodup_map_of_injective_on f as hnodup.2
        intro b hb c hc hbc
        exact hinj b (by simp [hb]) c (by simp [hc]) hbc

/-! ## Head-bit tail fibers of point families -/

/-- Source points with a prescribed first bit. -/
def headSourcePoints (F : BooleanPointFamily (n + 1)) (b : Bool) :
    List (Vector Bool (n + 1)) :=
  F.points.filter fun x => decide (vectorHead x = b)

/-- Tails of the points with prescribed first bit. -/
def headTailPoints (F : BooleanPointFamily (n + 1)) (b : Bool) :
    List (Vector Bool n) :=
  (headSourcePoints F b).map vectorTail

/-- The duplicate-free tail family over a prescribed first bit. -/
def headTailFamily (F : BooleanPointFamily (n + 1)) (b : Bool) :
    BooleanPointFamily n where
  points := headTailPoints F b
  points_nodup := by
    apply nodup_map_of_injective_on vectorTail (headSourcePoints F b)
    · exact List.filter_sublist.nodup F.points_nodup
    · intro x hx y hy htail
      have hxhead : vectorHead x = b :=
        of_decide_eq_true (List.mem_filter.mp hx).2
      have hyhead : vectorHead y = b :=
        of_decide_eq_true (List.mem_filter.mp hy).2
      exact vectorTail_injective_of_head_eq (hxhead.trans hyhead.symm) htail

/-- Exact membership in a head-bit tail fiber. -/
theorem mem_headTailFamily_iff (F : BooleanPointFamily (n + 1))
    (b : Bool) (t : Vector Bool n) :
    t ∈ (headTailFamily F b).points ↔
      ∃ x ∈ F.points, vectorHead x = b ∧ vectorTail x = t := by
  simp only [headTailFamily, headTailPoints, List.mem_map, headSourcePoints,
    List.mem_filter, decide_eq_true_eq]
  constructor
  · rintro ⟨x, ⟨hx, hxhead⟩, hxt⟩
    exact ⟨x, hx, hxhead, hxt⟩
  · rintro ⟨x, hx, hxhead, hxt⟩
    exact ⟨x, ⟨hx, hxhead⟩, hxt⟩

/-- A list partitions exactly according to a Boolean-valued key. -/
theorem length_eq_bool_filter_partition {α : Type} (xs : List α) (key : α → Bool) :
    xs.length =
      (xs.filter fun x => decide (key x = false)).length +
      (xs.filter fun x => decide (key x = true)).length := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      cases hkey : key x <;> simp [hkey, ih] <;> omega

/-- Splitting a Boolean point family at its head preserves total cardinality. -/
theorem headTailFamily_card_partition (F : BooleanPointFamily (n + 1)) :
    F.card = (headTailFamily F false).card + (headTailFamily F true).card := by
  simpa [BooleanPointFamily.card, headTailFamily, headTailPoints,
    headSourcePoints] using length_eq_bool_filter_partition F.points vectorHead

/-! ## The three first-coordinate difference fibers -/

/-- Full differences with prescribed first coordinate. -/
def differenceHeadFiber (A B : BooleanPointFamily (n + 1)) (k : Int) :
    List (Vector Int (n + 1)) :=
  (mixedDifferenceSet A B).filter fun z => decide (vectorHead z = k)

/-- Tails of full differences with prescribed first coordinate. -/
def differenceTailFiber (A B : BooleanPointFamily (n + 1)) (k : Int) :
    List (Vector Int n) :=
  (differenceHeadFiber A B k).map vectorTail

/-- Cardinality of one first-coordinate difference fiber. -/
def differenceTailCard (A B : BooleanPointFamily (n + 1)) (k : Int) : Nat :=
  (differenceTailFiber A B k).length

/-- Exact membership in a prescribed-head full difference fiber. -/
theorem mem_differenceHeadFiber_iff (A B : BooleanPointFamily (n + 1))
    (k : Int) (z : Vector Int (n + 1)) :
    z ∈ differenceHeadFiber A B k ↔
      z ∈ mixedDifferenceSet A B ∧ vectorHead z = k := by
  simp [differenceHeadFiber]

/-- Exact membership in a prescribed-head tail-difference fiber. -/
theorem mem_differenceTailFiber_iff (A B : BooleanPointFamily (n + 1))
    (k : Int) (t : Vector Int n) :
    t ∈ differenceTailFiber A B k ↔
      ∃ z ∈ mixedDifferenceSet A B,
        vectorHead z = k ∧ vectorTail z = t := by
  simp only [differenceTailFiber, List.mem_map, mem_differenceHeadFiber_iff]
  constructor
  · rintro ⟨z, ⟨hz, hhead⟩, htail⟩
    exact ⟨z, hz, hhead, htail⟩
  · rintro ⟨z, hz, hhead, htail⟩
    exact ⟨z, ⟨hz, hhead⟩, htail⟩

/-- Semantic form of tail-difference membership in terms of a mixed pair of
Boolean points. -/
theorem mem_differenceTailFiber_semantic_iff
    (A B : BooleanPointFamily (n + 1)) (k : Int) (t : Vector Int n) :
    t ∈ differenceTailFiber A B k ↔
      ∃ a ∈ A.points, ∃ b ∈ B.points,
        bitVal (vectorHead a) - bitVal (vectorHead b) = k ∧
        bitDifference (vectorTail a) (vectorTail b) = t := by
  rw [mem_differenceTailFiber_iff]
  constructor
  · rintro ⟨z, hz, hhead, htail⟩
    obtain ⟨a, ha, b, hb, hab⟩ := (mem_mixedDifferenceSet_iff A B z).mp hz
    subst z
    exact ⟨a, ha, b, hb, by simpa using hhead, by simpa using htail⟩
  · rintro ⟨a, ha, b, hb, hhead, htail⟩
    refine ⟨bitDifference a b, ?_, ?_, ?_⟩
    · exact (mem_mixedDifferenceSet_iff A B _).mpr ⟨a, ha, b, hb, rfl⟩
    · simpa using hhead
    · simpa using htail

/-- Tails stay duplicate-free inside one fixed difference-head fiber. -/
theorem differenceTailFiber_nodup (A B : BooleanPointFamily (n + 1)) (k : Int) :
    (differenceTailFiber A B k).Nodup := by
  apply nodup_map_of_injective_on vectorTail (differenceHeadFiber A B k)
  · exact List.filter_sublist.nodup (mixedDifferenceSet_nodup A B)
  · intro x hx y hy htail
    have hxhead : vectorHead x = k :=
      of_decide_eq_true (List.mem_filter.mp hx).2
    have hyhead : vectorHead y = k :=
      of_decide_eq_true (List.mem_filter.mp hy).2
    exact vectorTail_injective_of_head_eq (hxhead.trans hyhead.symm) htail

/-- Mixed differences between two head-tail point fibers have an exact
description using their source points. -/
theorem mem_mixed_headTailFamily_iff
    (A B : BooleanPointFamily (n + 1)) (ba bb : Bool) (t : Vector Int n) :
    t ∈ mixedDifferenceSet (headTailFamily A ba) (headTailFamily B bb) ↔
      ∃ a ∈ A.points, vectorHead a = ba ∧
        ∃ b ∈ B.points, vectorHead b = bb ∧
          bitDifference (vectorTail a) (vectorTail b) = t := by
  rw [mem_mixedDifferenceSet_iff]
  constructor
  · rintro ⟨ta, hta, tb, htb, hdiff⟩
    obtain ⟨a, ha, hahead, hatail⟩ :=
      (mem_headTailFamily_iff A ba ta).mp hta
    obtain ⟨b, hb, hbhead, hbtail⟩ :=
      (mem_headTailFamily_iff B bb tb).mp htb
    subst ta
    subst tb
    exact ⟨a, ha, hahead, b, hb, hbhead, hdiff⟩
  · rintro ⟨a, ha, hahead, b, hb, hbhead, hdiff⟩
    exact ⟨vectorTail a, (mem_headTailFamily_iff A ba _).mpr
      ⟨a, ha, hahead, rfl⟩,
      vectorTail b, (mem_headTailFamily_iff B bb _).mpr
      ⟨b, hb, hbhead, rfl⟩, hdiff⟩

/-- A Boolean head difference is `-1` exactly in the `0-1` block. -/
theorem bitVal_sub_eq_neg_one_iff (a b : Bool) :
    bitVal a - bitVal b = (-1 : Int) ↔ a = false ∧ b = true := by
  cases a <;> cases b <;> simp [bitVal]

/-- A Boolean head difference is zero exactly on the two diagonal blocks. -/
theorem bitVal_sub_eq_zero_iff (a b : Bool) :
    bitVal a - bitVal b = 0 ↔ a = b := by
  cases a <;> cases b <;> simp [bitVal]

/-- A Boolean head difference is `1` exactly in the `1-0` block. -/
theorem bitVal_sub_eq_one_iff (a b : Bool) :
    bitVal a - bitVal b = (1 : Int) ↔ a = true ∧ b = false := by
  cases a <;> cases b <;> simp [bitVal]

/-- The `-1` difference-tail fiber is exactly `A₀-B₁`. -/
theorem mem_negativeDifferenceTailFiber_iff
    (A B : BooleanPointFamily (n + 1)) (t : Vector Int n) :
    t ∈ differenceTailFiber A B (-1) ↔
      t ∈ mixedDifferenceSet (headTailFamily A false) (headTailFamily B true) := by
  rw [mem_differenceTailFiber_semantic_iff, mem_mixed_headTailFamily_iff]
  constructor
  · rintro ⟨a, ha, b, hb, hhead, htail⟩
    have hab := (bitVal_sub_eq_neg_one_iff (vectorHead a) (vectorHead b)).mp hhead
    exact ⟨a, ha, hab.1, b, hb, hab.2, htail⟩
  · rintro ⟨a, ha, hahead, b, hb, hbhead, htail⟩
    exact ⟨a, ha, b, hb,
      (bitVal_sub_eq_neg_one_iff _ _).mpr ⟨hahead, hbhead⟩, htail⟩

/-- The `1` difference-tail fiber is exactly `A₁-B₀`. -/
theorem mem_positiveDifferenceTailFiber_iff
    (A B : BooleanPointFamily (n + 1)) (t : Vector Int n) :
    t ∈ differenceTailFiber A B 1 ↔
      t ∈ mixedDifferenceSet (headTailFamily A true) (headTailFamily B false) := by
  rw [mem_differenceTailFiber_semantic_iff, mem_mixed_headTailFamily_iff]
  constructor
  · rintro ⟨a, ha, b, hb, hhead, htail⟩
    have hab := (bitVal_sub_eq_one_iff (vectorHead a) (vectorHead b)).mp hhead
    exact ⟨a, ha, hab.1, b, hb, hab.2, htail⟩
  · rintro ⟨a, ha, hahead, b, hb, hbhead, htail⟩
    exact ⟨a, ha, b, hb,
      (bitVal_sub_eq_one_iff _ _).mpr ⟨hahead, hbhead⟩, htail⟩

/-- The zero difference-tail fiber is exactly the union of the two diagonal
blocks `A₀-B₀` and `A₁-B₁`. -/
theorem mem_zeroDifferenceTailFiber_iff
    (A B : BooleanPointFamily (n + 1)) (t : Vector Int n) :
    t ∈ differenceTailFiber A B 0 ↔
      t ∈ mixedDifferenceSet (headTailFamily A false) (headTailFamily B false) ∨
      t ∈ mixedDifferenceSet (headTailFamily A true) (headTailFamily B true) := by
  rw [mem_differenceTailFiber_semantic_iff]
  constructor
  · rintro ⟨a, ha, b, hb, hhead, htail⟩
    have hab := (bitVal_sub_eq_zero_iff (vectorHead a) (vectorHead b)).mp hhead
    cases hbit : vectorHead a with
    | false =>
        left
        rw [mem_mixed_headTailFamily_iff]
        exact ⟨a, ha, hbit, b, hb, hab ▸ hbit, htail⟩
    | true =>
        right
        rw [mem_mixed_headTailFamily_iff]
        exact ⟨a, ha, hbit, b, hb, hab ▸ hbit, htail⟩
  · intro ht
    rcases ht with ht | ht
    · rw [mem_mixed_headTailFamily_iff] at ht
      obtain ⟨a, ha, hahead, b, hb, hbhead, htail⟩ := ht
      exact ⟨a, ha, b, hb,
        (bitVal_sub_eq_zero_iff _ _).mpr (hahead.trans hbhead.symm), htail⟩
    · rw [mem_mixed_headTailFamily_iff] at ht
      obtain ⟨a, ha, hahead, b, hb, hbhead, htail⟩ := ht
      exact ⟨a, ha, b, hb,
        (bitVal_sub_eq_zero_iff _ _).mpr (hahead.trans hbhead.symm), htail⟩

/-- Every Boolean difference has head `-1`, `0`, or `1`. -/
theorem mixedDifference_head_cases (A B : BooleanPointFamily (n + 1))
    (z : Vector Int (n + 1)) (hz : z ∈ mixedDifferenceSet A B) :
    vectorHead z = (-1 : Int) ∨ vectorHead z = 0 ∨ vectorHead z = 1 := by
  obtain ⟨a, ha, b, hb, hab⟩ := (mem_mixedDifferenceSet_iff A B z).mp hz
  subst z
  cases h₁ : vectorHead a <;> cases h₂ : vectorHead b <;>
    simp [vectorHead_bitDifference, h₁, h₂, bitVal]

/-- A list whose integer tag has only the values `-1,0,1` splits exactly into
the three corresponding filters. -/
theorem length_eq_three_int_filters {α : Type} (xs : List α) (tag : α → Int)
    (htags : ∀ x ∈ xs, tag x = (-1 : Int) ∨ tag x = 0 ∨ tag x = 1) :
    xs.length =
      (xs.filter fun x => decide (tag x = (-1 : Int))).length +
      (xs.filter fun x => decide (tag x = 0)).length +
      (xs.filter fun x => decide (tag x = 1)).length := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      have hx := htags x (by simp)
      have hxs : ∀ y ∈ xs, tag y = (-1 : Int) ∨ tag y = 0 ∨ tag y = 1 := by
        intro y hy
        exact htags y (by simp [hy])
      have hi := ih hxs
      rcases hx with hx | hx | hx <;> simp [hx, hi] <;> omega

/-- Exact `-1/0/1` cardinal decomposition of a mixed Boolean difference set.
The map to tails changes no length, and each tail fiber is duplicate-free. -/
theorem mixedDiffCard_head_decomposition
    (A B : BooleanPointFamily (n + 1)) :
    mixedDiffCard A B =
      differenceTailCard A B (-1) + differenceTailCard A B 0 +
        differenceTailCard A B 1 := by
  have hsplit := length_eq_three_int_filters (mixedDifferenceSet A B) vectorHead
    (mixedDifference_head_cases A B)
  simpa [mixedDiffCard, differenceTailCard, differenceTailFiber,
    differenceHeadFiber] using hsplit

/-! ## Mixed Boolean difference growth -/

/-- Length-zero vectors are unique. -/
theorem vector_zero_unique {α : Type} (x y : Vector α 0) : x = y := by
  apply Vector.ext
  intro i hi
  omega

/-- A duplicate-free family in dimension zero contains at most one point. -/
theorem booleanPointFamily_zero_card_le_one (F : BooleanPointFamily 0) :
    F.card ≤ 1 := by
  cases hpoints : F.points with
  | nil => simp [BooleanPointFamily.card, hpoints]
  | cons x xs =>
      cases xs with
      | nil => simp [BooleanPointFamily.card, hpoints]
      | cons y ys =>
          have hxy : x = y := vector_zero_unique x y
          subst y
          have hnd := F.points_nodup
          rw [hpoints] at hnd
          simp at hnd

/-- Two nonempty point families represent at least one mixed difference. -/
theorem mixedDiffCard_pos_of_points_ne_nil (A B : BooleanPointFamily n)
    (hA : A.points ≠ []) (hB : B.points ≠ []) :
    0 < mixedDiffCard A B := by
  obtain ⟨a, ha⟩ := List.exists_mem_of_ne_nil A.points hA
  obtain ⟨b, hb⟩ := List.exists_mem_of_ne_nil B.points hB
  have hmem : bitDifference a b ∈ mixedDifferenceSet A B :=
    (mem_mixedDifferenceSet_iff A B _).mpr ⟨a, ha, b, hb, rfl⟩
  cases hdiff : mixedDifferenceSet A B with
  | nil => simp [hdiff] at hmem
  | cons z zs => simp [mixedDiffCard, hdiff]

/-- **Boolean mixed-difference growth.**  For duplicate-free finite families
`A,B ⊆ {0,1}ⁿ`, integer subtraction satisfies
`|A-B|² ≥ |A|²|B|`.

The induction splits at the first coordinate.  The `-1` and `1` fibers are
the off-diagonal mixed differences; the zero fiber contains both diagonal
mixed differences.  `boolean_difference_growth_nat` combines the four
inductive bounds. -/
theorem booleanPointFamily_mixed_difference_growth :
    ∀ {n : Nat} (A B : BooleanPointFamily n),
      A.card ^ 2 * B.card ≤ mixedDiffCard A B ^ 2 := by
  intro n
  induction n with
  | zero =>
      intro A B
      by_cases hA : A.points = []
      · simp [BooleanPointFamily.card, mixedDiffCard, mixedDifferenceSet,
          mixedRawDifferences, hA]
      by_cases hB : B.points = []
      · simp [BooleanPointFamily.card, mixedDiffCard, mixedDifferenceSet,
          mixedRawDifferences, hB]
      have hAcard : A.card = 1 := by
        have hle := booleanPointFamily_zero_card_le_one A
        have hpos : 0 < A.card := by
          unfold BooleanPointFamily.card
          cases hpoints : A.points with
          | nil => exact (hA hpoints).elim
          | cons x xs => simp
        omega
      have hBcard : B.card = 1 := by
        have hle := booleanPointFamily_zero_card_le_one B
        have hpos : 0 < B.card := by
          unfold BooleanPointFamily.card
          cases hpoints : B.points with
          | nil => exact (hB hpoints).elim
          | cons x xs => simp
        omega
      have hdiff := mixedDiffCard_pos_of_points_ne_nil A B hA hB
      have hone : 1 ^ 2 ≤ mixedDiffCard A B ^ 2 :=
        Nat.pow_le_pow_left (by omega) 2
      simpa [hAcard, hBcard] using hone
  | succ n ih =>
      intro A B
      let A0 := headTailFamily A false
      let A1 := headTailFamily A true
      let B0 := headTailFamily B false
      let B1 := headTailFamily B true
      let x := differenceTailCard A B (-1)
      let y := differenceTailCard A B 0
      let z := differenceTailCard A B 1
      have hAcard : A.card = A0.card + A1.card :=
        headTailFamily_card_partition A
      have hBcard : B.card = B0.card + B1.card :=
        headTailFamily_card_partition B
      have hnegCard : mixedDiffCard A0 B1 ≤ x := by
        have hsub : mixedDifferenceSet A0 B1 ⊆ differenceTailFiber A B (-1) := by
          intro t ht
          exact (mem_negativeDifferenceTailFiber_iff A B t).mpr ht
        simpa [mixedDiffCard, differenceTailCard, x] using
          length_le_of_subset_of_nodup (mixedDifferenceSet_nodup A0 B1) hsub
      have hzeroCard₀ : mixedDiffCard A0 B0 ≤ y := by
        have hsub : mixedDifferenceSet A0 B0 ⊆ differenceTailFiber A B 0 := by
          intro t ht
          exact (mem_zeroDifferenceTailFiber_iff A B t).mpr (Or.inl ht)
        simpa [mixedDiffCard, differenceTailCard, y] using
          length_le_of_subset_of_nodup (mixedDifferenceSet_nodup A0 B0) hsub
      have hzeroCard₁ : mixedDiffCard A1 B1 ≤ y := by
        have hsub : mixedDifferenceSet A1 B1 ⊆ differenceTailFiber A B 0 := by
          intro t ht
          exact (mem_zeroDifferenceTailFiber_iff A B t).mpr (Or.inr ht)
        simpa [mixedDiffCard, differenceTailCard, y] using
          length_le_of_subset_of_nodup (mixedDifferenceSet_nodup A1 B1) hsub
      have hposCard : mixedDiffCard A1 B0 ≤ z := by
        have hsub : mixedDifferenceSet A1 B0 ⊆ differenceTailFiber A B 1 := by
          intro t ht
          exact (mem_positiveDifferenceTailFiber_iff A B t).mpr ht
        simpa [mixedDiffCard, differenceTailCard, z] using
          length_le_of_subset_of_nodup (mixedDifferenceSet_nodup A1 B0) hsub
      have hx : A0.card ^ 2 * B1.card ≤ x ^ 2 :=
        Nat.le_trans (ih A0 B1) (Nat.pow_le_pow_left hnegCard 2)
      have hy₀ : A0.card ^ 2 * B0.card ≤ y ^ 2 :=
        Nat.le_trans (ih A0 B0) (Nat.pow_le_pow_left hzeroCard₀ 2)
      have hy₁ : A1.card ^ 2 * B1.card ≤ y ^ 2 :=
        Nat.le_trans (ih A1 B1) (Nat.pow_le_pow_left hzeroCard₁ 2)
      have hz : A1.card ^ 2 * B0.card ≤ z ^ 2 :=
        Nat.le_trans (ih A1 B0) (Nat.pow_le_pow_left hposCard 2)
      have hcombine := boolean_difference_growth_nat
        A0.card A1.card B0.card B1.card x y z hx hy₀ hy₁ hz
      rw [hAcard, hBcard, mixedDiffCard_head_decomposition A B]
      simpa [x, y, z] using hcombine

/-! ## Fixed-weight and high-energy corollaries -/

/-- Forgetting the fixed-weight certificate gives a general Boolean point
family with the same points. -/
def BoolFamily.toBooleanPointFamily (F : BoolFamily) :
    BooleanPointFamily F.dimension :=
  ⟨F.points, F.points_nodup⟩

/-- The mixed self-difference set and the fixed-weight difference set represent
exactly the same integer vectors. -/
theorem mem_mixedSelfDifferenceSet_iff (F : BoolFamily)
    (z : Vector Int F.dimension) :
    z ∈ mixedDifferenceSet F.toBooleanPointFamily F.toBooleanPointFamily ↔
      z ∈ F.differenceSet := by
  rw [mem_mixedDifferenceSet_iff, mem_differenceSet_iff]
  rfl

/-- The two deduplicated representations of the self-difference set have the
same exact cardinality. -/
theorem mixedDiffCard_self_eq_diffCard (F : BoolFamily) :
    mixedDiffCard F.toBooleanPointFamily F.toBooleanPointFamily = F.diffCard := by
  have hleft : mixedDiffCard F.toBooleanPointFamily F.toBooleanPointFamily ≤
      F.diffCard := by
    apply length_le_of_subset_of_nodup
      (mixedDifferenceSet_nodup F.toBooleanPointFamily F.toBooleanPointFamily)
    intro z hz
    exact (mem_mixedSelfDifferenceSet_iff F z).mp hz
  have hright : F.diffCard ≤
      mixedDiffCard F.toBooleanPointFamily F.toBooleanPointFamily := by
    apply length_le_of_subset_of_nodup (nodup_eraseDups_local F.rawDifferences)
    intro z hz
    exact (mem_mixedSelfDifferenceSet_iff F z).mpr hz
  omega

/-- Boolean self-difference growth in the square-root-free form
`|F|³ ≤ |F-F|²`. -/
theorem boolFamily_diffCard_cube_growth (F : BoolFamily) :
    F.card ^ 3 ≤ F.diffCard ^ 2 := by
  have h := booleanPointFamily_mixed_difference_growth
    F.toBooleanPointFamily F.toBooleanPointFamily
  rw [mixedDiffCard_self_eq_diffCard F] at h
  simpa [BooleanPointFamily.card, BoolFamily.toBooleanPointFamily,
    BoolFamily.card, Nat.pow_succ] using h

/-- Exact squared quasicube corollary consumed by `NoHighEnergy.lean`. -/
theorem boolFamily_quasicube_squared (F : BoolFamily) :
    F.card ^ 4 ≤ F.diffCard ^ 2 * F.card := by
  have h := Nat.mul_le_mul_right F.card (boolFamily_diffCard_cube_growth F)
  simpa [Nat.pow_succ] using h

/-- Semantic `BoolFiber` form of Boolean difference growth. -/
theorem boolFiber_quasicube_squared (s d : Nat) (h : BoolFiber s d) :
    s ^ 4 ≤ d ^ 2 * s := by
  obtain ⟨F, hcard, hdiff⟩ := h
  rw [← hcard, ← hdiff]
  exact boolFamily_quasicube_squared F

/-- `NoHighEnergy` with the Boolean difference-growth input discharged. -/
theorem no_high_energy_bound_boolean
    (f K C : Nat)
    (bsg : ∃ s d : Nat,
      f ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d) :
    f ≤ K ^ (3 * C) :=
  no_high_energy_bound boolFiber_quasicube_squared f K C bsg

/-- Concrete primitive-Boolean moment compiler: only the BSG extraction remains
as a high-energy input. -/
theorem primitiveBooleanMomentUpper_of_bsg
    (q K C : Nat) (stats : List BooleanFiberStat)
    (bsg : ∀ stat ∈ stats, highEnergy K stat = true →
      ∃ s d : Nat,
        stat.count ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d) :
    ordinaryFiberMoment q stats ≤
      lowEnergyFiberMoment q K stats +
        stats.length * (K ^ (3 * C)) ^ q :=
  primitiveBooleanMomentUpper q K C stats boolFiber_quasicube_squared bsg

/-- Same concrete compiler after a separately proved low-energy/Sidon payment. -/
theorem primitiveBooleanMomentUpper_of_bsg_and_lowEnergyPayment
    (q K C paid : Nat) (stats : List BooleanFiberStat)
    (bsg : ∀ stat ∈ stats, highEnergy K stat = true →
      ∃ s d : Nat,
        stat.count ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d)
    (hlow : lowEnergyFiberMoment q K stats ≤ paid) :
    ordinaryFiberMoment q stats ≤
      paid + stats.length * (K ^ (3 * C)) ^ q :=
  primitiveBooleanMomentUpper_of_lowEnergyPayment q K C paid stats
    boolFiber_quasicube_squared bsg hlow

#print axioms mem_mixedDifferenceSet_iff
#print axioms headTailFamily_card_partition
#print axioms differenceTailFiber_nodup
#print axioms mem_negativeDifferenceTailFiber_iff
#print axioms mem_zeroDifferenceTailFiber_iff
#print axioms mem_positiveDifferenceTailFiber_iff
#print axioms mixedDiffCard_head_decomposition
#print axioms booleanPointFamily_mixed_difference_growth
#print axioms boolFamily_diffCard_cube_growth
#print axioms boolFiber_quasicube_squared
#print axioms no_high_energy_bound_boolean
#print axioms primitiveBooleanMomentUpper_of_bsg_and_lowEnergyPayment

end AsymptoticSpine
