import AsymptoticSpine.Reroute

namespace AsymptoticSpine

set_option maxRecDepth 100000

/-!
# Profile-envelope core

This module formalizes the audit-stable elementary core of
`experimental/asymptotic_rs_mca.tex`:

* the attained pigeonhole floor used in `thm:polynomial-obstruction`;
* the exact GF(11²) complete-square quotient-label replication;
* the cleared Cauchy--Schwarz arithmetic behind
  `prop:collision-aware-lower` / Grande Finale's
  `thm:simple-pole-list-floor`;
* the conditional compiler/bracket skeleton of `thm:frontier`.

The package is stdlib-only.  Field geometry, pole root counts, routed Sidon
payment, and the direct ray compiler enter only through named hypotheses.
Consequently the first two arithmetic targets are proved exactly, while the
frontier theorem is explicitly conditional, as in the source.
-/

/-! ## Ceiling division and an attained pigeonhole fibre -/

/-- Natural-number ceiling division, written in the source as `⌈N / D⌉`.
All theorems using it require a positive denominator. -/
def ceilDiv (N D : Nat) : Nat := (N + D - 1) / D

/-- Cleared ceiling arithmetic: `N ≤ D*M` implies `⌈N/D⌉ ≤ M`. -/
theorem ceilDiv_le_of_le_mul {N D M : Nat} (hD : 0 < D) (h : N ≤ D * M) :
    ceilDiv N D ≤ M := by
  unfold ceilDiv
  rw [Nat.div_le_iff_le_mul hD]
  have h' : N + D - 1 ≤ D * M + D - 1 :=
    Nat.sub_le_sub_right (Nat.add_le_add_right h D) 1
  simpa [Nat.mul_comm] using h'

/-- The computed maximum of a nonempty natural-number list is attained. -/
theorem listMax_mem_of_ne_nil (l : List Nat) (hne : l ≠ []) : listMax l ∈ l := by
  induction l with
  | nil => exact (hne rfl).elim
  | cons a t ih =>
      by_cases h : listMax t ≤ a
      · simpa only [listMax, Nat.max_eq_left h] using
          (List.mem_cons_self : a ∈ a :: t)
      · have hat : a ≤ listMax t := by omega
        have ht : t ≠ [] := by
          intro ht
          subst t
          simp at h
        simpa only [listMax, Nat.max_eq_right hat] using
          List.mem_cons_of_mem a (ih ht)

/-- **Attained fibre floor.**  If every item is keyed into one of `P > 0`
buckets, some bucket has at least `⌈items.length / P⌉` members.

This strengthens the existing cleared `identity_prefix_floor` from a maximum
inequality to the explicit witness needed by equation (5.3). -/
theorem exists_fiber_ge_ceil {α : Type} (items : List α) (key : α → Nat) (P : Nat)
    (hP : 0 < P) (hkey : ∀ x ∈ items, key x < P) :
    ∃ z ∈ List.range P,
      ceilDiv items.length P ≤
        (items.filter (fun x => decide (key x = z))).length := by
  let sizes :=
    (List.range P).map (fun z =>
      (items.filter (fun x => decide (key x = z))).length)
  have hcleared : items.length ≤ P * listMax sizes := by
    simpa [sizes] using identity_prefix_floor items key P hkey
  have hceil : ceilDiv items.length P ≤ listMax sizes :=
    ceilDiv_le_of_le_mul hP hcleared
  have hzero :
      (items.filter (fun x => decide (key x = 0))).length ∈ sizes := by
    exact List.mem_map.mpr ⟨0, List.mem_range.mpr hP, rfl⟩
  have hsizes : sizes ≠ [] := by
    intro hs
    rw [hs] at hzero
    simp at hzero
  have hmax : listMax sizes ∈ sizes := listMax_mem_of_ne_nil sizes hsizes
  obtain ⟨z, hz, hzmax⟩ := List.mem_map.mp hmax
  refine ⟨z, hz, ?_⟩
  rw [hzmax]
  exact hceil

/-! ## The exact GF(11²) complete-square profile replication

For the smallest audited row, `p=11, n=20, a=8, w=2`.  The square image
`D² = θ² F₁₁ˣ` has labels `1,…,10`.  A complete-square support is therefore
a four-subset `C` of those ten labels.  Its only active prefix coordinate is
`q₂ = -θ² ∑ C`, so keying by `∑ C mod 11` is exactly the quotient-label
computation; no implementation of GF(121) is needed.
-/

/-- An increasing four-subset of the ten nonzero GF(11) labels. -/
structure GF11SquareSupport where
  c1 : Nat
  c2 : Nat
  c3 : Nat
  c4 : Nat
  deriving Repr, DecidableEq

/-- Enumerate the `choose(10,4)=210` increasing four-subsets of `{1,…,10}`. -/
def gf11SquareSupports : List GF11SquareSupport :=
  (List.range 11).flatMap fun c1 =>
    (List.range 11).flatMap fun c2 =>
      (List.range 11).flatMap fun c3 =>
        (List.range 11).filterMap fun c4 =>
          if 1 ≤ c1 ∧ c1 < c2 ∧ c2 < c3 ∧ c3 < c4 then
            some ⟨c1, c2, c3, c4⟩
          else
            none

/-- The depth-two complete-square prefix, reduced to its GF(11) label. -/
def gf11SquarePrefix (C : GF11SquareSupport) : Nat :=
  (C.c1 + C.c2 + C.c3 + C.c4) % 11

/-- The eleven exact prefix-fibre sizes. -/
def gf11SquareFibres : List Nat :=
  (List.range 11).map fun z =>
    (gf11SquareSupports.filter (fun C =>
      decide (gf11SquarePrefix C = z))).length

/-- **GF(11²) finite certificate.**  The computation enumerates all supports
rather than hard-coding the census.  There are 210 supports, all 11 prefixes
occur, the zero prefix contains 20 supports, every other prefix contains 19,
and `⌈210/11⌉=20`. -/
theorem gf11_square_profile_certificate :
    gf11SquareSupports.Nodup ∧
    gf11SquareSupports.length = 210 ∧
    gf11SquareFibres =
      [20, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19] ∧
    listMax gf11SquareFibres = 20 ∧
    ceilDiv 210 11 = 20 := by
  decide

/-- The general attained-fibre theorem applied to the exact GF(11²) labels. -/
theorem gf11_square_profile_floor :
    ∃ z ∈ List.range 11,
      ceilDiv gf11SquareSupports.length 11 ≤
        (gf11SquareSupports.filter (fun C =>
          decide (gf11SquarePrefix C = z))).length :=
  exists_fiber_ge_ceil gf11SquareSupports gf11SquarePrefix 11 (by decide)
    (by
      intro C _
      exact Nat.mod_lt _ (by decide))

/-! ## Collision-aware distinct-value floor -/

/-- **Collision-aware Cauchy--Schwarz floor, cleared form.**

Here `d=q-n>0`, `L≥1` is the list size, `M` is the number of distinct
values at the selected pole, and `sumSq=∑ᵢ mᵢ²`.  The hypotheses are exactly
the two arithmetic interfaces in the paper:

* Cauchy--Schwarz: `L² ≤ M * sumSq`;
* the pole collision budget:
  `d * sumSq ≤ d*L + k*L*(L-1)`.

The conclusion is
`⌈L*d / (d+k(L-1))⌉ ≤ M`.  The separate root-count/averaging argument
supplies the collision hypothesis; it is not silently inferred here. -/
theorem collision_aware_distinct_value_floor
    (L d k M sumSq : Nat) (hL : 0 < L) (hd : 0 < d)
    (hcauchy : L * L ≤ M * sumSq)
    (hcollision : d * sumSq ≤ d * L + k * L * (L - 1)) :
    ceilDiv (L * d) (d + k * (L - 1)) ≤ M := by
  have hbudget : sumSq * d ≤ L * (d + k * (L - 1)) := by
    calc
      sumSq * d = d * sumSq := Nat.mul_comm _ _
      _ ≤ d * L + k * L * (L - 1) := hcollision
      _ = L * (d + k * (L - 1)) := by
        simp [Nat.mul_add, Nat.mul_assoc, Nat.mul_comm]
  have hscaled : L * (L * d) ≤ M * (sumSq * d) := by
    calc
      L * (L * d) = (L * L) * d := by rw [Nat.mul_assoc]
      _ ≤ (M * sumSq) * d := Nat.mul_le_mul_right d hcauchy
      _ = M * (sumSq * d) := by rw [Nat.mul_assoc]
  have hcombined :
      L * (L * d) ≤ M * (L * (d + k * (L - 1))) :=
    Nat.le_trans hscaled (Nat.mul_le_mul_left M hbudget)
  have hfactored :
      L * (L * d) ≤ L * (M * (d + k * (L - 1))) := by
    simpa [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm] using hcombined
  have hcleared : L * d ≤ M * (d + k * (L - 1)) :=
    Nat.le_of_mul_le_mul_left hfactored hL
  exact ceilDiv_le_of_le_mul (Nat.add_pos_left hd _) (by
    simpa [Nat.mul_comm] using hcleared)

/-- **Abstract simple-pole list-to-MCA floor.**  This is the natural-number
content common to `prop:collision-aware-lower` and Grande Finale's
`thm:simple-pole-list-floor`.  The polynomial root count and pole averaging
produce `hcollision`; `hbad` is the explicit interface saying each distinct
pole value gives a bad slope. -/
theorem simple_pole_list_floor
    (L q n k M sumSq badSlopes : Nat)
    (hL : 0 < L) (hqn : n < q)
    (hcauchy : L * L ≤ M * sumSq)
    (hcollision :
      (q - n) * sumSq ≤ (q - n) * L + k * L * (L - 1))
    (hbad : M ≤ badSlopes) :
    ceilDiv (L * (q - n)) ((q - n) + k * (L - 1)) ≤ badSlopes := by
  exact Nat.le_trans
    (collision_aware_distinct_value_floor L (q - n) k M sumSq hL
      (Nat.sub_pos_of_lt hqn) hcauchy hcollision)
    hbad

/-- The audit's GF(11⁴) scalar-extension parameters reproduce the full
20-slope floor: `q=14641, n=20, d=14621, L=20, k=5`. -/
theorem gf11_extension_collision_floor :
    ceilDiv (20 * (14641 - 20)) ((14641 - 20) + 5 * (20 - 1)) = 20 := by
  decide

/-! ## Conditional profile-envelope compiler and threshold bracket -/

/-- The exact finite data consumed by the identity-dominant specialization of
the profile-envelope compiler.  Every load-bearing finite compiler interface
represented here is named: closed first-match coverage, natural-profile
payment, routed Sidon payment, RC, identity dominance, and the target-budget
inequality.  No field theorem is hidden in the structure. -/
structure ProfileCompilerInputs
    (badUpper nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target : Nat) : Prop where
  closedLedger : badUpper ≤ nonprimitive + primitiveRay
  naturalProfilePayment : nonprimitive ≤ compilerLoss * nonprimitiveBudget
  /-- The routed Sidon/primitive budget after absorbing the permitted RC loss
  into `compilerLoss`. -/
  sidonPayment : primitivePaid ≤ compilerLoss * sidonBudget
  /-- RC itself: the actual primitive ray image is bounded by the paid
  intermediary. -/
  rayCompiler : primitiveRay ≤ primitivePaid
  profileEnvelopeBudget : nonprimitiveBudget + sidonBudget ≤ profileEnvelope
  identityDominance : profileEnvelope ≤ identityLoss * identityBudget
  targetBudget : (compilerLoss * identityLoss) * identityBudget ≤ target

/-- The named compiler inputs imply that the upper agreement is safe. -/
theorem profile_compiler_upper
    (badUpper nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target : Nat)
    (h : ProfileCompilerInputs badUpper nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target) :
    badUpper ≤ target := by
  calc
    badUpper ≤ nonprimitive + primitiveRay := h.closedLedger
    _ ≤ nonprimitive + primitivePaid := Nat.add_le_add_left h.rayCompiler _
    _ ≤ compilerLoss * nonprimitiveBudget + compilerLoss * sidonBudget :=
      Nat.add_le_add h.naturalProfilePayment h.sidonPayment
    _ = compilerLoss * (nonprimitiveBudget + sidonBudget) := by
      rw [Nat.mul_add]
    _ ≤ compilerLoss * profileEnvelope :=
      Nat.mul_le_mul_left compilerLoss h.profileEnvelopeBudget
    _ ≤ compilerLoss * (identityLoss * identityBudget) :=
      Nat.mul_le_mul_left compilerLoss h.identityDominance
    _ = (compilerLoss * identityLoss) * identityBudget := by
      rw [Nat.mul_assoc]
    _ ≤ target := h.targetBudget

/-- Characterization of the first safe agreement in a finite interval. -/
structure IsFirstSafe
    (bad : Nat → Nat) (target lower upper first : Nat) : Prop where
  inRange : lower ≤ first ∧ first ≤ upper
  safe : bad first ≤ target
  minimal : ∀ a, lower ≤ a → a < first → target < bad a

/-- Safe upper and unsafe lower certificates bracket a first safe agreement.
Antitonicity is the monotonicity of the MCA bad-slope numerator in agreement. -/
theorem first_safe_bracket
    (bad : Nat → Nat) (target lower upper first aMinus aPlus : Nat)
    (hanti : ∀ a b, a ≤ b → bad b ≤ bad a)
    (hfirst : IsFirstSafe bad target lower upper first)
    (_hminus : lower ≤ aMinus) (hplus : lower ≤ aPlus)
    (hlower : target < bad aMinus) (hupper : bad aPlus ≤ target) :
    aMinus < first ∧ first ≤ aPlus := by
  -- The source-domain side condition `_hminus` is retained in the interface.
  -- Global antitonicity plus `hfirst.safe` makes it logically redundant here.
  constructor
  · apply Nat.lt_of_not_ge
    intro hle
    have hbad : bad aMinus ≤ bad first := hanti first aMinus hle
    exact (Nat.not_lt_of_ge (Nat.le_trans hbad hfirst.safe)) hlower
  · apply Nat.le_of_not_gt
    intro hlt
    exact (Nat.not_lt_of_ge hupper) (hfirst.minimal aPlus hplus hlt)

/-- **Conditional identity-dominant frontier skeleton.**  A certified lower
construction and the named compiler inputs at the upper agreement give the
agreement bracket `a₋ < a* ≤ a₊`; the second conjunct is its cleared radius
form `n-a₊ ≤ n-a* < n-a₋`.

This theorem does not claim RC, Sidon payment, identity dominance, or the
target-budget inequality: they are fields of `ProfileCompilerInputs` and are
all used to derive the safe upper certificate. -/
theorem profile_frontier_bracket
    (bad : Nat → Nat)
    (target lower n first aMinus aPlus : Nat)
    (nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget : Nat)
    (hanti : ∀ a b, a ≤ b → bad b ≤ bad a)
    (hfirst : IsFirstSafe bad target lower n first)
    (hminus : lower ≤ aMinus) (hplus : lower ≤ aPlus)
    (hplusn : aPlus ≤ n)
    (hlower : target < bad aMinus)
    (hcompiler :
      ProfileCompilerInputs (bad aPlus) nonprimitive primitiveRay primitivePaid
        nonprimitiveBudget sidonBudget profileEnvelope
        compilerLoss identityLoss identityBudget target) :
    (aMinus < first ∧ first ≤ aPlus) ∧
      (n - aPlus ≤ n - first ∧ n - first < n - aMinus) := by
  have hupper : bad aPlus ≤ target :=
    profile_compiler_upper (bad aPlus) nonprimitive primitiveRay primitivePaid
      nonprimitiveBudget sidonBudget profileEnvelope
      compilerLoss identityLoss identityBudget target hcompiler
  have hagree :=
    first_safe_bracket bad target lower n first aMinus aPlus
      hanti hfirst hminus hplus hlower hupper
  refine ⟨hagree, ?_⟩
  have hfirstn : first ≤ n := hfirst.inRange.2
  omega

#print axioms ceilDiv_le_of_le_mul
#print axioms listMax_mem_of_ne_nil
#print axioms exists_fiber_ge_ceil
#print axioms gf11_square_profile_certificate
#print axioms gf11_square_profile_floor
#print axioms collision_aware_distinct_value_floor
#print axioms simple_pole_list_floor
#print axioms gf11_extension_collision_floor
#print axioms profile_compiler_upper
#print axioms first_safe_bracket
#print axioms profile_frontier_bracket

end AsymptoticSpine
