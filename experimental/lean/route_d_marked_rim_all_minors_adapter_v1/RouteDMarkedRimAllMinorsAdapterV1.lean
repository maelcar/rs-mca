import Std
import Std.Tactic

/-!
# Route-D marked RIM all-maximal-minors adapter v1

This standalone module exposes two theorem-shaped research interfaces:

* the generic all-maximal-minors/rank-drop equivalence;
* marked minimal-seam signed-moment reconstruction.

Both interfaces state their required linear-algebra/Newton bridge hypotheses
explicitly and are proved from them; no unconstrained theorem is present.  The conditional marked-owner route, primitive
fixed-target cross-section, selected-minor counterexample, and finite F17/F31
pins are proved or kernel checked.  The exhaustive F31 counts `121/119/99`
belong to the deterministic Python verifier and are not claimed as Lean
enumeration theorems here.

Exact source provenance:

* commit `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
* row-sharp reduction blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
* marked-incidence blob `a7f2bf4f1338d0b31d999c86a29859317033113f`;
* field-native pivot blob `0e1becd7ac2f66bf74c034ef0b8165d56cc1c471`;
* rank-drop owner blob `ddfce00907f34128b324a64041f4e0ec8957b7d3`;
* cross-Gram blob `4ed789595305170556371c87c5773d9e14ba4307`.
-/

namespace RouteDMarkedRimAllMinorsAdapterV1

def sourceCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def rowsharpBlob : String := "591c91a6aac6b48db0c16abc586b74d7a51e44e2"
def markedIncidenceBlob : String := "a7f2bf4f1338d0b31d999c86a29859317033113f"
def fieldNativePivotBlob : String := "0e1becd7ac2f66bf74c034ef0b8165d56cc1c471"
def rankDropOwnerBlob : String := "ddfce00907f34128b324a64041f4e0ec8957b7d3"
def crossGramBlob : String := "4ed789595305170556371c87c5773d9e14ba4307"

theorem exact_source_pins :
    sourceCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    rowsharpBlob = "591c91a6aac6b48db0c16abc586b74d7a51e44e2" ∧
    markedIncidenceBlob = "a7f2bf4f1338d0b31d999c86a29859317033113f" ∧
    fieldNativePivotBlob = "0e1becd7ac2f66bf74c034ef0b8165d56cc1c471" ∧
    rankDropOwnerBlob = "ddfce00907f34128b324a64041f4e0ec8957b7d3" ∧
    crossGramBlob = "4ed789595305170556371c87c5773d9e14ba4307" := by
  native_decide

/-! ## Generic theorem interfaces -/

def IsMaximalColumnChoice (rowCount columnCount : Nat) (columns : List Nat) : Prop :=
  columns.length = rowCount ∧ columns.Nodup ∧ ∀ column ∈ columns, column < columnCount

/-- Exact linear-algebra interface.  `maximalMinor columns` denotes the
determinant of the square submatrix using all rows and the chosen columns.
`fullRank_iff_exists_nonzero` is the standard rank/minor bridge that an
eventual Mathlib instantiation must discharge.  The Python verifier
exhaustively checks the concrete criterion over every 2x3 matrix over F3. -/
theorem all_maximal_minors_vanish_iff_rank_lt
    {F : Type} [Zero F]
    (rowCount columnCount matrixRank : Nat)
    (maximalMinor : List Nat → F)
    (_positiveRows : 0 < rowCount) (_wide : rowCount ≤ columnCount)
    (rankLE : matrixRank ≤ rowCount)
    (fullRank_iff_exists_nonzero :
      matrixRank = rowCount ↔
        ∃ columns, IsMaximalColumnChoice rowCount columnCount columns ∧
          maximalMinor columns ≠ 0) :
    ((∀ columns, IsMaximalColumnChoice rowCount columnCount columns →
        maximalMinor columns = 0) ↔ matrixRank < rowCount) := by
  constructor
  · intro hall
    have hne : matrixRank ≠ rowCount := by
      intro heq
      obtain ⟨columns, hchoice, hminor⟩ :=
        fullRank_iff_exists_nonzero.mp heq
      exact hminor (hall columns hchoice)
    exact Nat.lt_of_le_of_ne rankLE hne
  · intro hrank columns hchoice
    apply Classical.byContradiction
    intro hminor
    have heq : matrixRank = rowCount :=
      fullRank_iff_exists_nonzero.mpr ⟨columns, hchoice, hminor⟩
    exact (Nat.ne_of_lt hrank) heq

structure MarkedActualIncidence
    (Mark Core Key Matrix : Type) where
  mark : Mark
  core : Core
  key : Key
  matrix : Matrix
  actualBad : Prop
  noncontained : Prop

def RoutesToActualRankDrop
    {Mark Core Key Matrix : Type}
    (rankLT : Matrix → Prop)
    (incidence : MarkedActualIncidence Mark Core Key Matrix) : Prop :=
  incidence.actualBad ∧ incidence.noncontained ∧ rankLT incidence.matrix

/-- Conditional type-correct owner route.  The actual-bad and noncontained
hypotheses are explicit; raw algebraic rank drop is not accepted.  The result
returns the unchanged mark, core, and key. -/
theorem all_minors_route_carries_mark
    {Mark Core Key Matrix : Type}
    (allVanish rankLT : Matrix → Prop)
    (incidence : MarkedActualIncidence Mark Core Key Matrix)
    (criterion : ∀ matrix, allVanish matrix ↔ rankLT matrix)
    (hactual : incidence.actualBad)
    (hnoncontained : incidence.noncontained)
    (hvanish : allVanish incidence.matrix) :
    RoutesToActualRankDrop rankLT incidence ∧
      incidence.mark = incidence.mark ∧
      incidence.core = incidence.core ∧
      incidence.key = incidence.key := by
  exact ⟨⟨hactual, hnoncontained, (criterion incidence.matrix).mp hvanish⟩,
    rfl, rfl, rfl⟩

/-- Primitive fixed-target cross-section.  The arbitrary predicate `Q` is
carried but no invariance hypothesis on it is used. -/
theorem primitive_fixed_target_cross_section
    {H Packet Target : Type}
    (one : H) (actPacket : H → Packet → Packet)
    (actTarget : H → Target → Target) (target : Packet → Target)
    (Q : Packet → Prop) (z : Target) (h : H) (xi eta : Packet)
    (equivariant : ∀ scalar packet,
      target (actPacket scalar packet) = actTarget scalar (target packet))
    (trivialStabilizer : ∀ scalar, actTarget scalar z = z → scalar = one)
    (oneActs : ∀ packet, actPacket one packet = packet)
    (hxi : target xi = z) (heta : target eta = z)
    (orbitRelation : eta = actPacket h xi)
    (_qxi : Q xi) (_qeta : Q eta) : eta = xi := by
  have hstab : actTarget h z = z := by
    calc
      actTarget h z = actTarget h (target xi) := congrArg (actTarget h) hxi.symm
      _ = target (actPacket h xi) := (equivariant h xi).symm
      _ = target eta := congrArg target orbitRelation.symm
      _ = z := heta
  have hh : h = one := trivialStabilizer h hstab
  calc
    eta = actPacket h xi := orbitRelation
    _ = actPacket one xi := by rw [hh]
    _ = xi := oneActs xi

/-- Marked minimal-seam reconstruction interface.  `valid r` includes: monic
split side locators of size `r`, equal first `r-1` locator coefficients,
characteristic not dividing `r`, the marked root on the positive side, and
the signed degree-`r` moment.  Equality is of the ordered side locators, so a
carried common-core locator may be multiplied back without losing the mark.
`newtonReconstruction` is the exact polynomial/field bridge required from a
future concrete instantiation; this stdlib package does not pretend to define
field characteristic or split polynomials. -/
theorem marked_minimal_seam_signed_moment_reconstruction
    {Side Prefix Mark Moment : Type}
    (valid : Nat → Side → Prop) (sidePrefix : Side → Prefix)
    (contains : Mark → Side → Prop)
    (signedMoment : Side → Side → Moment)
    (r : Nat) (positive negative positive' negative' : Side) (mark : Mark)
    (hvalid : valid r positive ∧ valid r negative ∧
      valid r positive' ∧ valid r negative')
    (hpref : sidePrefix positive = sidePrefix negative ∧
      sidePrefix positive' = sidePrefix negative' ∧
      sidePrefix positive = sidePrefix positive')
    (hmark : contains mark positive ∧ contains mark positive')
    (hmoment : signedMoment positive negative =
      signedMoment positive' negative')
    (newtonReconstruction :
      valid r positive ∧ valid r negative ∧
        valid r positive' ∧ valid r negative' →
      sidePrefix positive = sidePrefix negative ∧
        sidePrefix positive' = sidePrefix negative' ∧
        sidePrefix positive = sidePrefix positive' →
      contains mark positive ∧ contains mark positive' →
      signedMoment positive negative = signedMoment positive' negative' →
      positive = positive' ∧ negative = negative') :
    positive = positive' ∧ negative = negative' := by
  exact newtonReconstruction hvalid hpref hmark hmoment

/-! ## Kernel-checked finite pins -/

def det2Mod (p a b c d : Nat) : Nat := (a * d + p - (b * c) % p) % p

theorem one_selected_minor_is_not_rank_drop_pin :
    det2Mod 5 1 0 0 0 = 0 ∧ det2Mod 5 1 0 0 1 = 1 := by
  native_decide

def sumMod (p : Nat) (values : List Nat) : Nat :=
  values.foldl (fun total value => (total + value) % p) 0

def pairSumMod (p : Nat) : List Nat → Nat
  | [] => 0
  | x :: xs =>
      ((xs.foldl (fun total y => (total + x * y) % p) 0) + pairSumMod p xs) % p

def locatorPrefix2 (p : Nat) (support : List Nat) : List Nat :=
  [(p - sumMod p support) % p, pairSumMod p support]

def deconvolve2 (p root : Nat) (target : List Nat) : List Nat :=
  match target with
  | [a1, a2] =>
      let child1 := (a1 + root) % p
      [child1, (a2 + root * child1) % p]
  | other => other

def targetStabilizer2 (p : Nat) (target : List Nat) : List Nat :=
  (List.range (p - 1)).map (fun x => x + 1) |>.filter (fun scalar =>
    match target with
    | [a1, a2] =>
        (scalar * a1) % p == a1 && (scalar * scalar * a2) % p == a2
    | _ => false)

def f17ExponentSupport1 : List Nat := [0, 1, 2, 3, 4, 5, 6, 15]
def f17ExponentSupport2 : List Nat := [0, 1, 2, 3, 5, 7, 12, 14]
def f17FieldSupport1 : List Nat := [1, 3, 9, 10, 13, 5, 15, 6]
def f17FieldSupport2 : List Nat := [1, 3, 9, 10, 5, 11, 4, 2]

def antipodalFree16 (support : List Nat) : Bool :=
  support.all (fun exponent => !(support.contains ((exponent + 8) % 16)))

theorem f17_reconstruction_collision_pin :
    f17ExponentSupport1.length = 8 ∧
    f17ExponentSupport2.length = 8 ∧
    f17ExponentSupport1 ≠ f17ExponentSupport2 ∧
    locatorPrefix2 17 f17FieldSupport1 = [6, 1] ∧
    locatorPrefix2 17 f17FieldSupport2 = [6, 1] ∧
    targetStabilizer2 17 [6, 1] = [1] ∧
    antipodalFree16 f17ExponentSupport1 = true ∧
    antipodalFree16 f17ExponentSupport2 = true ∧
    f17ExponentSupport1.contains 0 = true ∧
    f17ExponentSupport1.contains 8 = false ∧
    f17ExponentSupport2.contains 0 = true ∧
    f17ExponentSupport2.contains 8 = false := by
  native_decide

def f31Base : List Nat :=
  [1, 2, 3, 4, 5, 7, 10, 11, 12, 18, 19, 20, 21, 26, 28]

def f31Removed : List Nat := [4, 5, 7]
def f31Added : List Nat := [8, 15, 24]
def f31FirstMate : List Nat :=
  [1, 2, 3, 8, 10, 11, 12, 15, 18, 19, 20, 21, 24, 26, 28]

def powerSumMod (p degree : Nat) (support : List Nat) : Nat :=
  support.foldl (fun total value => (total + value ^ degree) % p) 0

theorem f31_target_child_and_cross_section_pins :
    locatorPrefix2 31 f31Base = [30, 9] ∧
    targetStabilizer2 31 [30, 9] = [1] ∧
    deconvolve2 31 1 [30, 9] = [0, 9] ∧
    targetStabilizer2 31 [0, 9] = [1, 30] ∧
    locatorPrefix2 31 f31FirstMate = [30, 9] := by
  native_decide

theorem f31_side_nonextension_fixture_pin :
    powerSumMod 31 1 f31Removed = powerSumMod 31 1 f31Added ∧
    powerSumMod 31 2 f31Removed = powerSumMod 31 2 f31Added ∧
    powerSumMod 31 3 f31Removed ≠ powerSumMod 31 3 f31Added := by
  native_decide

theorem f31_capacity_and_pivot_arithmetic_pin :
    99 > 3 * 31 ∧ 99 - 3 * 31 = 6 ∧
    99 > 3 * 30 ∧ 99 - 3 * 30 = 9 ∧
    [0, 0, 1].get? 2 = some 1 := by
  native_decide

end RouteDMarkedRimAllMinorsAdapterV1
