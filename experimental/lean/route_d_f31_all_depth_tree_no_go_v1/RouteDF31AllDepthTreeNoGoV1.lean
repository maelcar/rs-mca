import Std
import Std.Tactic

/-!
# Route-D F31 all-depth tree no-go v1

The finite enumeration and mask DP live in the deterministic Python verifier.
This standalone module exposes the theorem-shaped arithmetic and ownership
interfaces consumed by the note.  It does not turn a restricted toy packet
into an actual first-match residual.
-/

namespace RouteDF31AllDepthTreeNoGoV1

def baseCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def preflightCommit : String := "36d560d7421dace47bf48b3fecc9389adaf0977b"
def rootCompilerCommit : String := "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe"

theorem exact_source_pins :
    baseCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    preflightCommit = "36d560d7421dace47bf48b3fecc9389adaf0977b" ∧
    rootCompilerCommit = "91a9e31284adb34a1dfe5c71e434aa709ba2d3fe" := by
  native_decide

structure MarkedBoundaryPacket (Support Core Cell : Type) where
  inside : Support
  outside : Support
  core : Core
  cell : Cell

/-- The common-core mark remains literal carried data. -/
theorem carried_core_is_preserved
    {Support Core Cell : Type}
    (packet : MarkedBoundaryPacket Support Core Cell) :
    packet.core = packet.core := by
  rfl

/-- An algebraic label becomes an executable deletion only through an explicit
acceptance hypothesis. -/
theorem deletion_requires_acceptance
    {Packet : Type} (accepts : Packet → Prop) (packet : Packet)
    (accepted : accepts packet) : accepts packet := by
  exact accepted

/-- Branch excess in a finite rooted partition is the sum of outdegree minus
one.  The finite verifier pins the concrete tree realizing the hypotheses. -/
theorem four_row_excess_identity
    (row3 row4 row5 row6 total : Nat)
    (h3 : row3 = 28) (h4 : row4 = 78)
    (h5 : row5 = 11) (h6 : row6 = 2)
    (sumPin : total = row3 + row4 + row5 + row6) :
    total = 119 := by
  omega

/-- The rowwise cell-collision caps force the all-order ceiling. -/
theorem all_depth_rule2_ceiling
    (n3 n4 n5 n6 : Nat)
    (h3 : n3 ≤ 9) (h4 : n4 ≤ 45)
    (h5 : n5 ≤ 6) (h6 : n6 ≤ 0) :
    n3 + n4 + n5 + n6 ≤ 60 := by
  omega

/-- The all-depth ceiling cannot recover the prior finite floor of 81. -/
theorem sixty_is_strictly_below_eighty_one : (60 : Nat) < 81 := by
  omega

/-- Combined theorem-shaped no-go. -/
theorem disjoint_tree_cannot_recover_eighty_one
    (comparisons : Nat)
    (ceiling : comparisons ≤ 60) :
    comparisons < 81 := by
  omega

/-- Fifty comparisons and two-to-five extensions leave forty-five to
forty-eight nonextension certificates. -/
theorem representative_choice_nonextension_range
    (extensions nonextensions : Nat)
    (partition : extensions + nonextensions = 50)
    (lower : 2 ≤ extensions) (upper : extensions ≤ 5) :
    45 ≤ nonextensions ∧ nonextensions ≤ 48 := by
  omega

/-- Four charged toy rows cannot satisfy a toy budget of three. -/
theorem four_rows_do_not_fit_three : ¬ (4 : Nat) ≤ 3 := by
  omega

/-- Rows three through five cover 117 excess units, leaving two on row six. -/
theorem first_three_rows_leave_two
    (firstThree rowSix total : Nat)
    (firstPin : firstThree = 117)
    (rowSixPin : rowSix = 2)
    (totalPin : total = 119)
    (partition : firstThree + rowSix = total) :
    firstThree = 117 ∧ rowSix = 2 ∧ total = 119 ∧ firstThree + rowSix = total := by
  exact ⟨firstPin, rowSixPin, totalPin, partition⟩

/-! Exact finite pins exported by the deterministic verifier. -/

def excessByRow : List Nat := [28, 78, 11, 2]
def branchBucketsByRow : List Nat := [1, 27, 9, 2]
def nonSingletonBucketsByRow : List Nat := [1, 27, 10, 2]
def dpStatesByRow : List Nat := [13, 6896, 153, 4]
def dpCapsByRow : List Nat := [9, 45, 6, 0]
def lexPartition : List Nat := [12, 1, 4, 46, 56]
def chargedRows : List Nat := [3, 4, 5, 6]

theorem exact_finite_count_pins :
    excessByRow.foldl (· + ·) 0 = 119 ∧
    branchBucketsByRow = [1, 27, 9, 2] ∧
    nonSingletonBucketsByRow = [1, 27, 10, 2] ∧
    dpStatesByRow = [13, 6896, 153, 4] ∧
    dpCapsByRow.foldl (· + ·) 0 = 60 ∧
    lexPartition.foldl (· + ·) 0 = 119 ∧
    chargedRows.length = 4 ∧
    60 < 81 := by
  native_decide

end RouteDF31AllDepthTreeNoGoV1
