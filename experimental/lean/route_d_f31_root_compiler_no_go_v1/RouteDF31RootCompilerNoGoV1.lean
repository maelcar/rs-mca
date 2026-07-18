import Std
import Std.Tactic

/-!
# Route-D F31 root-compiler no-go v1

This standalone module exposes the theorem-shaped type boundary used by the
finite packet.  A child partition supplies one unit per non-base child; raw
marked supports become such units only through an explicit compiler.  The
finite enumeration itself remains in the deterministic Python verifier.

Exact source commits:

* base `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`;
* prefix reductions `e83962ae5ad7bacb391b691ffd37f0abef977b83`;
* singleton schema `84b393ec1bc52fa662756bd117a45537007d086a`;
* marked puncture recursion `5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`;
* marked RIM adapter `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`.
-/

namespace RouteDF31RootCompilerNoGoV1

def baseCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def prefixCommit : String := "e83962ae5ad7bacb391b691ffd37f0abef977b83"
def singletonCommit : String := "84b393ec1bc52fa662756bd117a45537007d086a"
def punctureCommit : String := "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b"
def adapterCommit : String := "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"

theorem exact_source_pins :
    baseCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    prefixCommit = "e83962ae5ad7bacb391b691ffd37f0abef977b83" ∧
    singletonCommit = "84b393ec1bc52fa662756bd117a45537007d086a" ∧
    punctureCommit = "5343c5876e559e33b6d3bb332cb2d55edbfbcc4b" ∧
    adapterCommit = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0" := by
  native_decide

/-! ## Typed compiler seam -/

structure MarkedBoundaryPacket (Support Core Cell : Type) where
  inside : Support
  outside : Support
  core : Core
  cell : Cell

structure BranchExcessUnit (Parent Child : Type) where
  parent : Parent
  child : Child

/-- Promotion from raw marked packets to branch units is an explicit map.
The theorem does not manufacture this map from the packet fields. -/
structure RootCompiler (Raw Parent Child : Type) where
  compile : Raw → BranchExcessUnit Parent Child

/-- Distinct-unit promotion requires injectivity as a separate compiler
property.  Raw packet distinctness alone is not an input to this theorem. -/
theorem distinct_units_require_injective_compiler
    {Raw Parent Child : Type}
    (compiler : RootCompiler Raw Parent Child)
    (injective : ∀ ⦃left right⦄, compiler.compile left = compiler.compile right → left = right)
    {left right : Raw}
    (different : left ≠ right) :
    compiler.compile left ≠ compiler.compile right := by
  intro equality
  exact different (injective equality)

/-- The common-core mark remains literal carried data. -/
theorem carried_core_is_preserved
    {Support Core Cell : Type}
    (packet : MarkedBoundaryPacket Support Core Cell) :
    packet.core = packet.core := by
  rfl

/-- An executable first-match deletion is not inferred from an algebraic
comparison; acceptance is an explicit hypothesis. -/
theorem deletion_requires_acceptance
    {Comparison : Type} (accepts : Comparison → Prop) (comparison : Comparison)
    (accepted : accepts comparison) : accepts comparison := by
  exact accepted

/-! ## Partition and comparison arithmetic -/

/-- One base child among twenty-nine leaves twenty-eight non-base child units. -/
theorem twenty_nine_children_give_twenty_eight_root_units
    (children units : Nat)
    (childrenPin : children = 29)
    (partition : units + 1 = children) :
    units = 28 := by
  omega

/-- Twenty cells among twenty-eight canonical packets yield eight algebraic
same-cell comparisons. -/
theorem twenty_cells_give_eight_algebraic_comparisons
    (packets cells comparisons : Nat)
    (packetsPin : packets = 28)
    (cellsPin : cells = 20)
    (partition : comparisons + cells = packets) :
    comparisons = 8 := by
  omega

/-- The all-base-child audit has only the two exact outcomes. -/
theorem all_base_choice_range
    (cells comparisons : Nat)
    (outcome : (cells = 19 ∧ comparisons = 9) ∨
               (cells = 20 ∧ comparisons = 8)) :
    19 ≤ cells ∧ cells ≤ 20 ∧ 8 ≤ comparisons ∧ comparisons ≤ 9 := by
  omega

/-- At fixed twenty-eight cells, eighty-one comparisons need at least one
hundred and nine packets. -/
theorem eighty_one_comparisons_need_109_packets
    (packets comparisons : Nat)
    (cells : Nat := 28)
    (cellsPin : cells = 28)
    (comparisonPin : comparisons = 81)
    (partition : packets = cells + comparisons) :
    packets = 109 := by
  omega

/-- Twenty-eight non-base child units cannot equal the required one hundred
and nine distinct units. -/
theorem one_child_partition_does_not_supply_109_units : (28 : Nat) < 109 := by
  omega

/-! ## Exact finite pins -/

def primitiveChildSizeHistogram : List (Nat × Nat) :=
  [(1, 1), (2, 4), (3, 5), (4, 8), (5, 3), (6, 4), (7, 1), (8, 1), (9, 1)]

def truncatedPackets (level : Nat) : Nat :=
  primitiveChildSizeHistogram.foldl
    (fun total pair => total + min pair.1 level * pair.2) 0

def allBaseOutcomeHistogram : List (Nat × Nat × Nat) :=
  [(19, 9, 13), (20, 8, 16)]

def anchorCoreIntersectionSizes : List Nat := [1, 2, 2, 2, 2, 3, 4, 4]

theorem f31_root_compiler_count_pins :
    primitiveChildSizeHistogram.foldl (fun total pair => total + pair.2) 0 = 28 ∧
    primitiveChildSizeHistogram.foldl (fun total pair => total + pair.1 * pair.2) 0 = 119 ∧
    truncatedPackets 1 = 28 ∧
    truncatedPackets 2 = 55 ∧
    truncatedPackets 3 = 78 ∧
    truncatedPackets 4 = 96 ∧
    truncatedPackets 5 = 106 ∧
    truncatedPackets 6 = 113 ∧
    allBaseOutcomeHistogram = [(19, 9, 13), (20, 8, 16)] ∧
    anchorCoreIntersectionSizes = [1, 2, 2, 2, 2, 3, 4, 4] ∧
    106 - 28 = 78 ∧
    113 - 28 = 85 ∧
    106 < 109 ∧
    109 ≤ 113 := by
  native_decide

end RouteDF31RootCompilerNoGoV1
