import AsymptoticSpine.Util

namespace AsymptoticSpine

/-!
# Concrete finite Boolean fibers

This module supplies the semantic finite-set layer used by the primitive
Boolean branch of `experimental/asymptotic_rs_mca_frontiers.tex`.

The asymptotic spine previously represented a Boolean fiber of cardinalities
`(s,d)` by an empty marker proposition.  That marker was inhabited for every
pair of natural numbers, so the quasicube premise in `NoHighEnergy.lean` could
not be instantiated.  Here `BoolFiber s d` contains an actual duplicate-free
fixed-weight family of length-indexed Boolean vectors whose deduplicated
integer difference set has the displayed cardinality.

All additive operations use the torsion-free integer embedding of Boolean
vectors, as required in `sec:sidon-split`.  The external quasicube and BSG
theorems remain explicit hypotheses downstream.
-/

/-- Coordinatewise embedding `{false,true} → {0,1} ⊂ ℤ`. -/
def bitVal (b : Bool) : Int :=
  if b then 1 else 0

/-- Hamming weight of a Boolean support vector. -/
def boolWeight {n : Nat} (x : Vector Bool n) : Nat :=
  x.toList.count true

/-- Torsion-free integer embedding of a Boolean vector. -/
def bitEmbed {n : Nat} (x : Vector Bool n) : Vector Int n :=
  x.map bitVal

/-- Coordinatewise integer difference. -/
def bitDifference {n : Nat} (a b : Vector Bool n) : Vector Int n :=
  Vector.zipWith (fun x y => bitVal x - bitVal y) a b

/-- The integer closure target `a - b + c`. -/
def closureVector {n : Nat} (a b c : Vector Bool n) : Vector Int n :=
  Vector.zipWith (· + ·) (bitDifference a b) (bitEmbed c)

/-- A duplicate-free family contained in one fixed-weight Boolean slice. -/
structure BoolFamily where
  dimension : Nat
  weight : Nat
  points : List (Vector Bool dimension)
  points_nodup : points.Nodup
  points_fixed : ∀ x ∈ points, boolWeight x = weight

namespace BoolFamily

/-- Cardinality of the Boolean family. -/
def card (F : BoolFamily) : Nat :=
  F.points.length

/-- Restrict a Boolean family along a displayed sublist. -/
def ofSublist (F : BoolFamily) (points : List (Vector Bool F.dimension))
    (hpoints : points.Sublist F.points) : BoolFamily where
  dimension := F.dimension
  weight := F.weight
  points := points
  points_nodup := hpoints.nodup F.points_nodup
  points_fixed := fun x hx => F.points_fixed x (hpoints.subset hx)

/-- The raw ordered-pair list. -/
def pairs (F : BoolFamily) :
    List (Vector Bool F.dimension × Vector Bool F.dimension) :=
  F.points.flatMap fun a => F.points.map fun b => (a, b)

/-- The raw ordered-pair difference list, with multiplicity. -/
def rawDifferences (F : BoolFamily) : List (Vector Int F.dimension) :=
  F.pairs.map fun p => bitDifference p.1 p.2

/-- The canonical deduplicated difference set. -/
def differenceSet (F : BoolFamily) : List (Vector Int F.dimension) :=
  F.rawDifferences.eraseDups

/-- Cardinality of the exact difference set. -/
def diffCard (F : BoolFamily) : Nat :=
  F.differenceSet.length

end BoolFamily

/-- Semantic replacement for the former empty marker: `BoolFiber s d` means
that an actual fixed-weight Boolean family has size `s` and difference-set
size `d`. -/
def BoolFiber (s d : Nat) : Prop :=
  ∃ F : BoolFamily, F.card = s ∧ F.diffCard = d

/-- Exact membership in the raw ordered-pair list. -/
theorem mem_pairs_iff (F : BoolFamily)
    (p : Vector Bool F.dimension × Vector Bool F.dimension) :
    p ∈ F.pairs ↔ p.1 ∈ F.points ∧ p.2 ∈ F.points := by
  simp only [BoolFamily.pairs, List.mem_flatMap, List.mem_map]
  constructor
  · rintro ⟨a, ha, b, hb, hab⟩
    cases hab
    exact ⟨ha, hb⟩
  · rintro ⟨ha, hb⟩
    exact ⟨p.1, ha, p.2, hb, rfl⟩

/-- Deduplication changes no represented difference. -/
theorem mem_differenceSet_iff (F : BoolFamily) (z : Vector Int F.dimension) :
    z ∈ F.differenceSet ↔
      ∃ a ∈ F.points, ∃ b ∈ F.points, bitDifference a b = z := by
  simp only [BoolFamily.differenceSet, List.mem_eraseDups,
    BoolFamily.rawDifferences, List.mem_map, mem_pairs_iff]
  constructor
  · rintro ⟨p, hp, hdiff⟩
    exact ⟨p.1, hp.1, p.2, hp.2, hdiff⟩
  · rintro ⟨a, ha, b, hb, hdiff⟩
    exact ⟨(a, b), ⟨ha, hb⟩, hdiff⟩

/-- Every nonempty family has a represented self-difference. -/
theorem selfDifference_mem (F : BoolFamily)
    (a : Vector Bool F.dimension) (ha : a ∈ F.points) :
    bitDifference a a ∈ F.differenceSet := by
  rw [mem_differenceSet_iff]
  exact ⟨a, ha, a, ha, rfl⟩

/-- A nonempty Boolean family has a nonempty difference set. -/
theorem differenceSet_length_pos_of_points_ne_nil
    (F : BoolFamily) (hpoints : F.points ≠ []) :
    0 < F.diffCard := by
  obtain ⟨a, ha⟩ := List.exists_mem_of_ne_nil F.points hpoints
  have hmem := selfDifference_mem F a ha
  cases hdiff : F.differenceSet with
  | nil => simp [hdiff] at hmem
  | cons z zs => simp [BoolFamily.diffCard, hdiff]

/-- In particular the semantic predicate rules out the formerly spurious
`BoolFiber 2 0` instance. -/
theorem not_boolFiber_two_zero : ¬ BoolFiber 2 0 := by
  rintro ⟨F, hcard, hdiff⟩
  have hpoints : F.points ≠ [] := by
    intro hnil
    simp [BoolFamily.card, hnil] at hcard
  have hpos := differenceSet_length_pos_of_points_ne_nil F hpoints
  omega

/-- The exact integer identity relating a repeated difference to its forced
closure point: `a - b = d - c` iff `d = a - b + c`. -/
theorem bitDifference_eq_iff_embed_eq_closure {n : Nat}
    (a b c d : Vector Bool n) :
    bitDifference a b = bitDifference d c ↔
      bitEmbed d = closureVector a b c := by
  constructor <;> intro h <;> apply Vector.ext <;> intro i hi
  · have hc := congrArg (fun v => v[i]) h
    simp [bitDifference, bitEmbed, closureVector] at hc ⊢
    omega
  · have hc := congrArg (fun v => v[i]) h
    simp [bitDifference, bitEmbed, closureVector] at hc ⊢
    omega

/-- The integer embedding of Boolean vectors is injective. -/
theorem bitEmbed_injective {n : Nat} : Function.Injective (@bitEmbed n) := by
  intro a b h
  apply Vector.ext
  intro i hi
  have hc := congrArg (fun v => v[i]) h
  cases ha : a[i] <;> cases hb : b[i] <;>
    simp [bitEmbed, bitVal, ha, hb] at hc ⊢

/-- Subtracting the same Boolean vector is injective. -/
theorem bitDifference_left_cancel {n : Nat} (a b c : Vector Bool n)
    (h : bitDifference a c = bitDifference b c) : a = b := by
  apply Vector.ext
  intro i hi
  have hc := congrArg (fun v => v[i]) h
  cases ha : a[i] <;> cases hb : b[i] <;> cases hz : c[i] <;>
    simp [bitDifference, bitVal, ha, hb, hz] at hc ⊢

/-- A closure witness is an ordered quadruple with
`a - b = d - c`, equivalently `a - b + c = d`.  The swapped order of the
last pair is only a relabelling of the standard energy equation. -/
structure ClosureWitness (n : Nat) where
  a : Vector Bool n
  b : Vector Bool n
  c : Vector Bool n
  d : Vector Bool n

/-- Candidate fourth points for the additive closure of `(a,b,c)`. -/
def closureCandidates (F : BoolFamily)
    (a b c : Vector Bool F.dimension) : List (Vector Bool F.dimension) :=
  F.points.filter fun d => decide (bitDifference a b = bitDifference d c)

/-- Exact semantic form of a closure candidate. -/
theorem mem_closureCandidates_iff (F : BoolFamily)
    (a b c d : Vector Bool F.dimension) :
    d ∈ closureCandidates F a b c ↔
      d ∈ F.points ∧ bitEmbed d = closureVector a b c := by
  simp only [closureCandidates, List.mem_filter]
  rw [decide_eq_true_eq, bitDifference_eq_iff_embed_eq_closure]

/-- For fixed `(a,b,c)` there is at most one closing fourth point. -/
theorem closureCandidates_length_le_one (F : BoolFamily)
    (a b c : Vector Bool F.dimension) :
    (closureCandidates F a b c).length ≤ 1 := by
  have hnodup : (closureCandidates F a b c).Nodup :=
    List.filter_sublist.nodup F.points_nodup
  cases hlist : closureCandidates F a b c with
  | nil => simp
  | cons d ds =>
      cases ds with
      | nil => simp
      | cons e es =>
          have hdmem : d ∈ closureCandidates F a b c := by simp [hlist]
          have hemem : e ∈ closureCandidates F a b c := by simp [hlist]
          have hdEq := of_decide_eq_true (List.mem_filter.mp hdmem).2
          have heEq := of_decide_eq_true (List.mem_filter.mp hemem).2
          have hde : d = e := bitDifference_left_cancel d e c (hdEq.symm.trans heEq)
          rw [hlist] at hnodup
          subst e
          simp at hnodup

/-- A uniform block bound gives the corresponding bound on a flattened
finite family. -/
theorem length_flatMap_le {α β : Type} (xs : List α) (f : α → List β)
    (B : Nat) (hB : ∀ x ∈ xs, (f x).length ≤ B) :
    (xs.flatMap f).length ≤ xs.length * B := by
  induction xs with
  | nil => simp
  | cons x xs ih =>
      have hx := hB x (by simp)
      have hxs : ∀ y ∈ xs, (f y).length ≤ B := by
        intro y hy
        exact hB y (by simp [hy])
      have ht := ih hxs
      simp only [List.flatMap_cons, List.length_append, List.length_cons,
        Nat.add_mul, Nat.one_mul]
      omega

/-- Exact list of additive-energy/closure witnesses. -/
def closureWitnesses (F : BoolFamily) : List (ClosureWitness F.dimension) :=
  F.points.flatMap fun a =>
    F.points.flatMap fun b =>
      F.points.flatMap fun c =>
        (closureCandidates F a b c).map fun d => ⟨a, b, c, d⟩

/-- Additive energy, represented as the exact number of repeated-difference
quadruples after swapping the two dummy variables in the second pair. -/
def additiveEnergy (F : BoolFamily) : Nat :=
  (closureWitnesses F).length

/-- The closure-witness formulation and repeated-difference formulation are
the same finite count by construction. -/
theorem additiveEnergy_eq_closureWitnesses (F : BoolFamily) :
    additiveEnergy F = (closureWitnesses F).length := rfl

/-- Exact closure-probability numerator bound: `E(F) ≤ |F|³`.  Each ordered
triple has at most one closing fourth point in the integer embedding. -/
theorem additiveEnergy_le_card_cubed (F : BoolFamily) :
    additiveEnergy F ≤ F.card ^ 3 := by
  have hc (a b : Vector Bool F.dimension) :
      (F.points.flatMap fun c =>
        (closureCandidates F a b c).map fun d =>
          (⟨a, b, c, d⟩ : ClosureWitness F.dimension)).length ≤ F.card := by
    have h := length_flatMap_le F.points
      (fun c => (closureCandidates F a b c).map fun d =>
        (⟨a, b, c, d⟩ : ClosureWitness F.dimension))
      1 (fun c _hc => by simpa using closureCandidates_length_le_one F a b c)
    simpa [BoolFamily.card] using h
  have hb (a : Vector Bool F.dimension) :
      (F.points.flatMap fun b =>
        F.points.flatMap fun c =>
          (closureCandidates F a b c).map fun d =>
            (⟨a, b, c, d⟩ : ClosureWitness F.dimension)).length
        ≤ F.card * F.card := by
    have h := length_flatMap_le F.points
      (fun b => F.points.flatMap fun c =>
        (closureCandidates F a b c).map fun d =>
          (⟨a, b, c, d⟩ : ClosureWitness F.dimension))
      F.card (fun b _hb => hc a b)
    simpa [BoolFamily.card] using h
  unfold additiveEnergy closureWitnesses
  calc
    (F.points.flatMap fun a =>
      F.points.flatMap fun b =>
        F.points.flatMap fun c =>
          (closureCandidates F a b c).map fun d =>
            (⟨a, b, c, d⟩ : ClosureWitness F.dimension)).length
        ≤ F.card * (F.card * F.card) := by
          have h := length_flatMap_le F.points
            (fun a => F.points.flatMap fun b =>
              F.points.flatMap fun c =>
                (closureCandidates F a b c).map fun d =>
                  (⟨a, b, c, d⟩ : ClosureWitness F.dimension))
            (F.card * F.card) (fun a _ha => hb a)
          simpa [BoolFamily.card] using h
    _ = F.card ^ 3 := by simp [Nat.pow_succ, Nat.mul_comm]

/-! ## Standard repeated differences and the closure-variable permutation -/

/-- Swap the last two dummy variables in a closure witness. -/
def ClosureWitness.swapLast {n : Nat} (w : ClosureWitness n) : ClosureWitness n :=
  ⟨w.a, w.b, w.d, w.c⟩

@[simp] theorem ClosureWitness.swapLast_swapLast {n : Nat}
    (w : ClosureWitness n) : w.swapLast.swapLast = w := by
  cases w
  rfl

/-- Standard additive-energy witnesses with equation `a-b = c-d`.

`closureWitnesses` enumerates the equivalent closure convention
`a-b = d-c`; swapping the last two dummy variables converts it to the
manuscript's displayed repeated-difference convention. -/
def repeatedDifferenceWitnesses (F : BoolFamily) :
    List (ClosureWitness F.dimension) :=
  (closureWitnesses F).map ClosureWitness.swapLast

/-- The variable swap preserves the exact energy count.  This is the formal
bridge required because the equation `a-b=c-d` forces `d=b-a+c`, whereas the
closure expression `a-b+c=d` uses the swapped pair. -/
theorem additiveEnergy_eq_repeatedDifferenceWitnesses (F : BoolFamily) :
    additiveEnergy F = (repeatedDifferenceWitnesses F).length := by
  simp [additiveEnergy, repeatedDifferenceWitnesses]

/-- Exact membership in the closure-convention witness list. -/
theorem mem_closureWitnesses_iff (F : BoolFamily)
    (w : ClosureWitness F.dimension) :
    w ∈ closureWitnesses F ↔
      w.a ∈ F.points ∧ w.b ∈ F.points ∧ w.c ∈ F.points ∧ w.d ∈ F.points ∧
        bitDifference w.a w.b = bitDifference w.d w.c := by
  cases w with
  | mk wa wb wc wd =>
      constructor
      · intro hw
        unfold closureWitnesses at hw
        rw [List.mem_flatMap] at hw
        obtain ⟨a, ha, hw⟩ := hw
        rw [List.mem_flatMap] at hw
        obtain ⟨b, hb, hw⟩ := hw
        rw [List.mem_flatMap] at hw
        obtain ⟨c, hc, hw⟩ := hw
        rw [List.mem_map] at hw
        obtain ⟨d, hd, heq⟩ := hw
        have hclose := (mem_closureCandidates_iff F a b c d).mp hd
        have hdiff :=
          (bitDifference_eq_iff_embed_eq_closure a b c d).mpr hclose.2
        cases heq
        exact ⟨ha, hb, hc, hclose.1, hdiff⟩
      · rintro ⟨ha, hb, hc, hd, hdiff⟩
        unfold closureWitnesses
        rw [List.mem_flatMap]
        refine ⟨wa, ha, ?_⟩
        rw [List.mem_flatMap]
        refine ⟨wb, hb, ?_⟩
        rw [List.mem_flatMap]
        refine ⟨wc, hc, ?_⟩
        rw [List.mem_map]
        refine ⟨wd, ?_, rfl⟩
        exact (mem_closureCandidates_iff F wa wb wc wd).mpr
          ⟨hd, (bitDifference_eq_iff_embed_eq_closure wa wb wc wd).mp hdiff⟩

/-- Exact membership in the standard repeated-difference witness list. -/
theorem mem_repeatedDifferenceWitnesses_iff (F : BoolFamily)
    (w : ClosureWitness F.dimension) :
    w ∈ repeatedDifferenceWitnesses F ↔
      w.a ∈ F.points ∧ w.b ∈ F.points ∧ w.c ∈ F.points ∧ w.d ∈ F.points ∧
        bitDifference w.a w.b = bitDifference w.c w.d := by
  have hswap : w ∈ repeatedDifferenceWitnesses F ↔
      w.swapLast ∈ closureWitnesses F := by
    constructor
    · intro hw
      rw [repeatedDifferenceWitnesses, List.mem_map] at hw
      obtain ⟨v, hv, hvw⟩ := hw
      have hv_eq : v = w.swapLast := by
        have hs := congrArg ClosureWitness.swapLast hvw
        simpa using hs
      rw [← hv_eq]
      exact hv
    · intro hw
      rw [repeatedDifferenceWitnesses, List.mem_map]
      exact ⟨w.swapLast, hw, by simp⟩
  rw [hswap, mem_closureWitnesses_iff]
  cases w with
  | mk a b c d =>
      change
        (a ∈ F.points ∧ b ∈ F.points ∧ d ∈ F.points ∧ c ∈ F.points ∧
          bitDifference a b = bitDifference c d) ↔
        (a ∈ F.points ∧ b ∈ F.points ∧ c ∈ F.points ∧ d ∈ F.points ∧
          bitDifference a b = bitDifference c d)
      constructor
      · rintro ⟨ha, hb, hd, hc, heq⟩
        exact ⟨ha, hb, hc, hd, heq⟩
      · rintro ⟨ha, hb, hc, hd, heq⟩
        exact ⟨ha, hb, hd, hc, heq⟩

#print axioms not_boolFiber_two_zero
#print axioms bitDifference_eq_iff_embed_eq_closure
#print axioms additiveEnergy_le_card_cubed
#print axioms additiveEnergy_eq_repeatedDifferenceWitnesses
#print axioms mem_repeatedDifferenceWitnesses_iff

end AsymptoticSpine
