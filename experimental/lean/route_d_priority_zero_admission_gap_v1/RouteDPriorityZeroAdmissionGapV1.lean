namespace RouteDPriorityZeroAdmissionGapV1

inductive NamedDeletion where
  | generatedField | quotientPlanted | sparsePadeHankel | m1WindowShadow
  | rankDropPivot | bcChart | spShiftPair | extensionSlope
  deriving DecidableEq, Repr

def namedDeletions : List NamedDeletion :=
  [.generatedField, .quotientPlanted, .sparsePadeHankel, .m1WindowShadow,
   .rankDropPivot, .bcChart, .spShiftPair, .extensionSlope]

theorem namedDeletionCount : namedDeletions.length = 8 := by native_decide

inductive LegacyBranch where
  | contained | rankDrop | tangent | quotient | planted
  | extension | generated | sparse | m1 | primitive
  deriving DecidableEq, Repr

def legacyOrder : List LegacyBranch :=
  [.contained, .rankDrop, .tangent, .quotient, .planted,
   .extension, .generated, .sparse, .m1, .primitive]

theorem legacyBranchCount : legacyOrder.length = 10 := by native_decide

/-- Theorem A's missing typed data.  The source `examples` list does not
construct an instance of this structure. -/
structure PriorityZeroExecutor (Packet Owner Mark BranchUnit : Type) where
  projector : NamedDeletion → Packet → Bool
  firstMatch : Packet → Option NamedDeletion
  residual : Packet → Prop
  owner : Packet → Option Owner
  mark : Packet → Mark
  branchUnit : Packet → Option BranchUnit
  firstMatchSound : ∀ x i, firstMatch x = some i → projector i x = true
  exhaustive : ∀ x, residual x ∨ ∃ i, firstMatch x = some i
  deletedHasOwner : ∀ x i, firstMatch x = some i → ∃ o, owner x = some o
  survivorHasUnit : ∀ x, residual x → ∃ u, branchUnit x = some u

theorem theoremA_exhaustive
    {Packet Owner Mark BranchUnit : Type}
    (E : PriorityZeroExecutor Packet Owner Mark BranchUnit) (x : Packet) :
    E.residual x ∨ ∃ i, E.firstMatch x = some i := E.exhaustive x

def p : Nat := 2130706433
def t : Nat := 67472

/-- Theorem B's post-admission payment interface.  Constructing an instance
is the missing owner/compiler work; no instance is asserted here. -/
structure ResidualCompilerPayment where
  totalSupport : Nat
  chargedRows : Nat
  strictDistanceTyped : Prop
  plantedCoreLedgerTyped : Prop
  rankSupportFiberTyped : Prop
  markedContactTyped : Prop
  fullRankWspTyped : Prop
  literalCommonCorePreserved : Prop
  rowBudget : chargedRows ≤ t
  cellCover : totalSupport ≤ 1 + chargedRows * (p - 1)
  strictDistanceProof : strictDistanceTyped
  plantedCoreLedgerProof : plantedCoreLedgerTyped
  rankSupportFiberProof : rankSupportFiberTyped
  markedContactProof : markedContactTyped
  fullRankWspProof : fullRankWspTyped
  commonCoreProof : literalCommonCorePreserved

theorem leafArithmetic : 1 + t * (p - 1) ≤ t * p := by native_decide

theorem theoremB_supportBound (C : ResidualCompilerPayment) :
    C.totalSupport ≤ t * p := by
  calc
    C.totalSupport ≤ 1 + C.chargedRows * (p - 1) := C.cellCover
    _ ≤ 1 + t * (p - 1) :=
      Nat.add_le_add_left (Nat.mul_le_mul_right (p - 1) C.rowBudget) 1
    _ ≤ t * p := leafArithmetic

theorem deployedProduct : t * p = 143763024447376 := by native_decide
theorem deployedCellExcess : t * (p - 1) = 143763024379904 := by native_decide
theorem deployedLeafBound : 1 + t * (p - 1) = 143763024379905 := by native_decide
theorem retainedClosure : t * p + 11440 = 143763024458816 := by native_decide
theorem conditionalSlack :
    274836936291722953 - (t * p + 11440) =
      274693173267264137 := by native_decide

end RouteDPriorityZeroAdmissionGapV1
