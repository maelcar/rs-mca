import AsymptoticSpine.EffectiveClosure
import AsymptoticSpine.NoHighEnergy

namespace AsymptoticSpine

/-!
# Primitive Boolean fibers and the exact energy split

This stdlib-only module supplies the finite semantic layer for the primitive
Boolean branch of `experimental/asymptotic_rs_mca_frontiers.tex`.

* `PrimitiveBooleanLeaf` identifies an actual full fixed-weight Boolean slice,
  an arbitrary routed residual sublist, and a finite prefix key.
* Every residual prefix class is packaged as a concrete `BoolFamily`, hence as
  a semantic `BoolFiber` with an exact difference-set cardinality.
* `BooleanFiberStat` derives its size and additive energy from that family; the
  low/high energy filters partition every finite moment exactly.
* The high-energy part composes either with the direct Boolean-energy theorem
  or with the older conditional BSG/quasicube arithmetic in
  `NoHighEnergy.lean`.

The direct sharp energy theorem, the alternative BSG/quasicube inputs, and
payment of the low-energy moment remain explicit hypotheses.  No asymptotic
estimate, character-frame theorem, or profile-atlas exhaustiveness statement
is asserted here.
-/

/-! ## A full slice, routed residual, and prefix fibers -/

/-- Concrete data for one primitive Boolean leaf.  `full_complete` says that
`full.points` enumerates the entire fixed-weight slice, not merely a subfamily;
`residual_sublist` records all deletions performed by earlier routing. -/
structure PrimitiveBooleanLeaf (Key : Type) where
  full : BoolFamily
  full_complete : ∀ x : Vector Bool full.dimension,
    boolWeight x = full.weight ↔ x ∈ full.points
  residual : List (Vector Bool full.dimension)
  residual_sublist : residual.Sublist full.points
  prefixKey : Vector Bool full.dimension → Key

/-- Full prefix class inside the complete fixed-weight slice. -/
def fullPrefixFiber {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    List (Vector Bool leaf.full.dimension) :=
  mapFiber leaf.full.points leaf.prefixKey z

/-- Routed residual prefix class. -/
def residualPrefixFiber {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    List (Vector Bool leaf.full.dimension) :=
  mapFiber leaf.residual leaf.prefixKey z

/-- Exact membership description of a full prefix class: fixed Hamming weight
and the displayed prefix key. -/
theorem mem_fullPrefixFiber_iff {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key)
    (x : Vector Bool leaf.full.dimension) :
    x ∈ fullPrefixFiber leaf z ↔
      boolWeight x = leaf.full.weight ∧ leaf.prefixKey x = z := by
  simp only [fullPrefixFiber, mapFiber, List.mem_filter, decide_eq_true_eq]
  rw [← leaf.full_complete x]

/-- Deleting routed points commutes with taking a fixed prefix class. -/
theorem residualPrefixFiber_sublist_fullPrefixFiber
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    (residualPrefixFiber leaf z).Sublist (fullPrefixFiber leaf z) := by
  exact leaf.residual_sublist.filter
    (fun x => decide (leaf.prefixKey x = z))

/-- Exact residual monotonicity at one prefix key. -/
theorem residualPrefixFiber_length_le_fullPrefixFiber
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    (residualPrefixFiber leaf z).length ≤ (fullPrefixFiber leaf z).length :=
  (residualPrefixFiber_sublist_fullPrefixFiber leaf z).length_le

/-- The full prefix class, retaining its inherited Boolean-slice semantics. -/
def fullFiberFamily {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) : BoolFamily :=
  leaf.full.ofSublist (fullPrefixFiber leaf z) List.filter_sublist

@[simp] theorem fullFiberFamily_points
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    (fullFiberFamily leaf z).points = fullPrefixFiber leaf z := rfl

/-- A residual prefix class, retaining its inherited Boolean-slice semantics. -/
def residualFiberFamily {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) : BoolFamily :=
  leaf.full.ofSublist (residualPrefixFiber leaf z)
    (List.filter_sublist.trans leaf.residual_sublist)

@[simp] theorem residualFiberFamily_points
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    (residualFiberFamily leaf z).points = residualPrefixFiber leaf z := rfl

/-- The concrete residual family is a displayed subfamily of the concrete full
prefix family. -/
theorem residualFiberFamily_sublist_fullFiberFamily
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    (residualFiberFamily leaf z).points.Sublist
      (fullFiberFamily leaf z).points :=
  residualPrefixFiber_sublist_fullPrefixFiber leaf z

/-- Every full prefix class is itself a semantic Boolean fiber. -/
theorem fullFiberFamily_isBoolFiber
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    BoolFiber (fullFiberFamily leaf z).card
      (fullFiberFamily leaf z).diffCard := by
  exact ⟨fullFiberFamily leaf z, rfl, rfl⟩

/-- Every routed residual prefix class supplies an actual semantic Boolean
fiber at its displayed size and exact difference-set size. -/
theorem residualFiberFamily_isBoolFiber
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    BoolFiber (residualFiberFamily leaf z).card
      (residualFiberFamily leaf z).diffCard := by
  exact ⟨residualFiberFamily leaf z, rfl, rfl⟩

/-- The exact closure energy of a residual prefix class is bounded by the cube
of its actual cardinality. -/
theorem residualFiberEnergy_le_card_cubed
    {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) :
    additiveEnergy (residualFiberFamily leaf z) ≤
      (residualFiberFamily leaf z).card ^ 3 :=
  additiveEnergy_le_card_cubed (residualFiberFamily leaf z)

/-! ## Exact low/high energy partition -/

/-- A fiber statistic contains the family itself.  Its count and energy below
are therefore semantic definitions, not independently supplied numerals. -/
structure BooleanFiberStat where
  family : BoolFamily

namespace BooleanFiberStat

/-- Actual cardinality of a Boolean fiber statistic. -/
def count (stat : BooleanFiberStat) : Nat :=
  stat.family.card

/-- Actual repeated-difference additive energy. -/
def energy (stat : BooleanFiberStat) : Nat :=
  additiveEnergy stat.family

/-- The universal closure bound inherited from the Boolean embedding. -/
theorem energy_le_count_cubed (stat : BooleanFiberStat) :
    stat.energy ≤ stat.count ^ 3 :=
  additiveEnergy_le_card_cubed stat.family

end BooleanFiberStat

/-- Statistic attached to one routed residual prefix class. -/
def residualFiberStat {Key : Type} [DecidableEq Key]
    (leaf : PrimitiveBooleanLeaf Key) (z : Key) : BooleanFiberStat :=
  ⟨residualFiberFamily leaf z⟩

/-- Cleared low-energy test `K E(F) ≤ |F|³`.  Equality is assigned to the low
side, so the complementary high side has the strict inequality
`|F|³ < K E(F)`. -/
def lowEnergy (K : Nat) (stat : BooleanFiberStat) : Bool :=
  decide (K * stat.energy ≤ stat.count ^ 3)

/-- Complementary high-energy test. -/
def highEnergy (K : Nat) (stat : BooleanFiberStat) : Bool :=
  !(lowEnergy K stat)

/-- Proposition-level meaning of the low-energy Boolean test. -/
theorem lowEnergy_eq_true_iff (K : Nat) (stat : BooleanFiberStat) :
    lowEnergy K stat = true ↔ K * stat.energy ≤ stat.count ^ 3 := by
  simp [lowEnergy]

/-- Proposition-level meaning of the high-energy Boolean test. -/
theorem highEnergy_eq_true_iff (K : Nat) (stat : BooleanFiberStat) :
    highEnergy K stat = true ↔ stat.count ^ 3 < K * stat.energy := by
  simp [highEnergy, lowEnergy]

/-- Ordinary finite moment numerator. -/
def ordinaryFiberMoment (q : Nat) (stats : List BooleanFiberStat) : Nat :=
  listSumPow q (stats.map BooleanFiberStat.count)

/-- Contribution from the low-energy sublist.  Calling this contribution
"paid" requires a separate Sidon/low-energy estimate downstream. -/
def lowEnergyFiberMoment (q K : Nat)
    (stats : List BooleanFiberStat) : Nat :=
  listSumPow q
    ((stats.filter (lowEnergy K)).map BooleanFiberStat.count)

/-- Contribution from the complementary high-energy sublist. -/
def highEnergyFiberMoment (q K : Nat)
    (stats : List BooleanFiberStat) : Nat :=
  listSumPow q
    ((stats.filter (highEnergy K)).map BooleanFiberStat.count)

/-- A Boolean filter and its complement split a finite power sum exactly. -/
theorem listSumPow_filter_partition {α : Type}
    (q : Nat) (f : α → Nat) (p : α → Bool) :
    ∀ xs : List α,
      listSumPow q (xs.map f) =
        listSumPow q ((xs.filter p).map f) +
          listSumPow q ((xs.filter (fun x => !(p x))).map f) := by
  intro xs
  induction xs with
  | nil => simp
  | cons a t ih =>
      cases hp : p a <;>
        simp [hp, ih, Nat.add_assoc, Nat.add_left_comm]

/-- Exact low/high partition of the ordinary Boolean-fiber moment. -/
theorem ordinaryFiberMoment_eq_low_add_high
    (q K : Nat) (stats : List BooleanFiberStat) :
    ordinaryFiberMoment q stats =
      lowEnergyFiberMoment q K stats + highEnergyFiberMoment q K stats := by
  unfold ordinaryFiberMoment lowEnergyFiberMoment highEnergyFiberMoment
  change listSumPow q (stats.map BooleanFiberStat.count) =
    listSumPow q ((stats.filter (lowEnergy K)).map BooleanFiberStat.count) +
      listSumPow q
        ((stats.filter (fun stat => !(lowEnergy K stat))).map
          BooleanFiberStat.count)
  exact listSumPow_filter_partition q BooleanFiberStat.count (lowEnergy K) stats

/-- If every high-energy fiber has size at most `H`, its entire moment costs at
most the number of displayed fibers times `H^q`. -/
theorem highEnergyFiberMoment_le
    (q K H : Nat) (stats : List BooleanFiberStat)
    (hhigh : ∀ stat ∈ stats, highEnergy K stat = true → stat.count ≤ H) :
    highEnergyFiberMoment q K stats ≤ stats.length * H ^ q := by
  have hterms : ∀ x ∈
      (stats.filter (highEnergy K)).map BooleanFiberStat.count, x ≤ H := by
    intro x hx
    obtain ⟨stat, hstat, rfl⟩ := List.mem_map.mp hx
    have hs := List.mem_filter.mp hstat
    exact hhigh stat hs.1 hs.2
  have hpow := listSumPow_le_length_mul q
    ((stats.filter (highEnergy K)).map BooleanFiberStat.count) H hterms
  calc
    highEnergyFiberMoment q K stats
        ≤ (stats.filter (highEnergy K)).length * H ^ q := by
          simpa [highEnergyFiberMoment] using hpow
    _ ≤ stats.length * H ^ q :=
      Nat.mul_le_mul_right (H ^ q) List.filter_sublist.length_le

/-- Finite energy-split upper bound before paying the low-energy term. -/
theorem ordinaryFiberMoment_le_low_add_uniform_high
    (q K H : Nat) (stats : List BooleanFiberStat)
    (hhigh : ∀ stat ∈ stats, highEnergy K stat = true → stat.count ≤ H) :
    ordinaryFiberMoment q stats ≤
      lowEnergyFiberMoment q K stats + stats.length * H ^ q := by
  rw [ordinaryFiberMoment_eq_low_add_high]
  exact Nat.add_le_add_left
    (highEnergyFiberMoment_le q K H stats hhigh) _

/-- Exact contrapositive compiler: if the ordinary moment exceeds the paid
low-energy budget plus a uniform high-fiber allowance, some high-energy fiber
must exceed that allowance. -/
theorem exists_large_highEnergyFiber_of_moment_excess
    (q K H paid : Nat) (stats : List BooleanFiberStat)
    (hlow : lowEnergyFiberMoment q K stats ≤ paid)
    (hexcess : paid + stats.length * H ^ q < ordinaryFiberMoment q stats) :
    ∃ stat ∈ stats, highEnergy K stat = true ∧ H < stat.count := by
  apply Classical.byContradiction
  intro hnone
  have hbound : ∀ stat ∈ stats,
      highEnergy K stat = true → stat.count ≤ H := by
    intro stat hstat henergy
    apply Nat.le_of_not_lt
    intro hlarge
    exact hnone ⟨stat, hstat, henergy, hlarge⟩
  have hupper := ordinaryFiberMoment_le_low_add_uniform_high
    q K H stats hbound
  have hpaid : lowEnergyFiberMoment q K stats + stats.length * H ^ q ≤
      paid + stats.length * H ^ q := Nat.add_le_add_right hlow _
  omega

/-! ## Conditional direct Boolean-energy composition -/

/-- One semantic Boolean fiber is strictly smaller than `K^3` once supplied
with the integer-power consequence `E(F)^3 ≤ |F|^8` of the sharp
Boolean-cube energy theorem. -/
theorem booleanFiberStat_count_lt_cube_of_sharpEnergy
    (stat : BooleanFiberStat) (K : Nat)
    (hsharp : stat.energy ^ 3 ≤ stat.count ^ 8)
    (henergy : highEnergy K stat = true) :
    stat.count < K ^ 3 :=
  count_lt_cube_of_energy_cubed_le_count_eighth
    stat.count stat.energy K hsharp
    ((highEnergy_eq_true_iff K stat).mp henergy)

/-- Direct finite high-energy compiler.  Every high-energy fiber is bounded by
the largest natural number strictly below `K^3`; the low-energy contribution
remains separate. -/
theorem primitiveBooleanMomentUpper_of_sharpEnergy
    (q K : Nat) (stats : List BooleanFiberStat)
    (hsharp : ∀ stat ∈ stats,
      stat.energy ^ 3 ≤ stat.count ^ 8) :
    ordinaryFiberMoment q stats ≤
      lowEnergyFiberMoment q K stats +
        stats.length * (K ^ 3 - 1) ^ q := by
  apply ordinaryFiberMoment_le_low_add_uniform_high
  intro stat hstat henergy
  have hlt := booleanFiberStat_count_lt_cube_of_sharpEnergy
    stat K (hsharp stat hstat) henergy
  omega

/-- Same direct compiler after an independently supplied low-energy/Sidon
payment. -/
theorem primitiveBooleanMomentUpper_of_sharpEnergyPayment
    (q K paid : Nat) (stats : List BooleanFiberStat)
    (hsharp : ∀ stat ∈ stats,
      stat.energy ^ 3 ≤ stat.count ^ 8)
    (hlow : lowEnergyFiberMoment q K stats ≤ paid) :
    ordinaryFiberMoment q stats ≤
      paid + stats.length * (K ^ 3 - 1) ^ q := by
  have hsplit := primitiveBooleanMomentUpper_of_sharpEnergy
    q K stats hsharp
  exact Nat.le_trans hsplit (Nat.add_le_add_right hlow _)

/-! ## Conditional BSG/quasicube composition -/

/-- Applying the exact `NoHighEnergy` arithmetic to one semantic Boolean-fiber
statistic.  The BSG output and quasicube theorem are deliberately arguments. -/
theorem booleanFiberStat_count_le_of_bsg_quasicube
    (quasicube : ∀ s d : Nat, BoolFiber s d → s ^ 4 ≤ d ^ 2 * s)
    (stat : BooleanFiberStat) (K C : Nat)
    (bsg : ∃ s d : Nat,
      stat.count ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d) :
    stat.count ≤ K ^ (3 * C) :=
  no_high_energy_bound quasicube stat.count K C bsg

/-- End-to-end finite primitive-Boolean energy compiler.  BSG is requested only
for members of the high-energy sublist; quasicube then caps their sizes, and
the exact moment partition pays the rest as the low-energy contribution. -/
theorem primitiveBooleanMomentUpper
    (q K C : Nat) (stats : List BooleanFiberStat)
    (quasicube : ∀ s d : Nat, BoolFiber s d → s ^ 4 ≤ d ^ 2 * s)
    (bsg : ∀ stat ∈ stats, highEnergy K stat = true →
      ∃ s d : Nat,
        stat.count ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d) :
    ordinaryFiberMoment q stats ≤
      lowEnergyFiberMoment q K stats +
        stats.length * (K ^ (3 * C)) ^ q := by
  apply ordinaryFiberMoment_le_low_add_uniform_high
  intro stat hstat henergy
  exact booleanFiberStat_count_le_of_bsg_quasicube quasicube stat K C
    (bsg stat hstat henergy)

/-- Same compiler after a separately proved low-energy/Sidon payment. -/
theorem primitiveBooleanMomentUpper_of_lowEnergyPayment
    (q K C paid : Nat) (stats : List BooleanFiberStat)
    (quasicube : ∀ s d : Nat, BoolFiber s d → s ^ 4 ≤ d ^ 2 * s)
    (bsg : ∀ stat ∈ stats, highEnergy K stat = true →
      ∃ s d : Nat,
        stat.count ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d)
    (hlow : lowEnergyFiberMoment q K stats ≤ paid) :
    ordinaryFiberMoment q stats ≤
      paid + stats.length * (K ^ (3 * C)) ^ q := by
  have hsplit := primitiveBooleanMomentUpper q K C stats quasicube bsg
  exact Nat.le_trans hsplit (Nat.add_le_add_right hlow _)

#print axioms fullFiberFamily_isBoolFiber
#print axioms residualFiberFamily_isBoolFiber
#print axioms ordinaryFiberMoment_eq_low_add_high
#print axioms exists_large_highEnergyFiber_of_moment_excess
#print axioms count_lt_cube_of_energy_cubed_le_count_eighth
#print axioms primitiveBooleanMomentUpper_of_sharpEnergyPayment
#print axioms primitiveBooleanMomentUpper_of_lowEnergyPayment

end AsymptoticSpine
