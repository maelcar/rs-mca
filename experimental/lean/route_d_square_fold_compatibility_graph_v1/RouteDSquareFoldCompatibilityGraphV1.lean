import Std
import Std.Tactic

/-!
# Route-D square-fold compatibility graph v1

This standalone module records theorem-shaped interfaces for the exact local
square-fold reconstruction, the conditional pseudoforest/additive transfer,
the finite target-erasure `K_(3,3)` arithmetic obstruction, and the actual-rank owner guard.
It does not construct a Route-D first-match compiler or an actual incidence
matrix.
-/

namespace RouteDSquareFoldCompatibilityGraphV1

def baseCommit : String := "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e"
def prefixCommit : String := "e83962ae5ad7bacb391b691ffd37f0abef977b83"
def prefixNoteBlob : String := "591c91a6aac6b48db0c16abc586b74d7a51e44e2"
def f23Commit : String := "f23a3b78a6bbe1d50a81b3976f92aa7c135ab300"
def f23NoteBlob : String := "5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b"
def allMinorsCommit : String := "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0"
def allMinorsNoteBlob : String := "f24ce928df7e7170c1b4f3228d5fe9b184be50b4"

theorem exact_source_pins :
    baseCommit = "c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e" ∧
    prefixCommit = "e83962ae5ad7bacb391b691ffd37f0abef977b83" ∧
    prefixNoteBlob = "591c91a6aac6b48db0c16abc586b74d7a51e44e2" ∧
    f23Commit = "f23a3b78a6bbe1d50a81b3976f92aa7c135ab300" ∧
    f23NoteBlob = "5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b" ∧
    allMinorsCommit = "a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0" ∧
    allMinorsNoteBlob = "f24ce928df7e7170c1b4f3228d5fe9b184be50b4" := by
  native_decide

def foldPair (a b : Int) : Int × Int := (a + b, a - b)

/-- Addition and subtraction recover twice the two Boolean signed
coordinates. Division by two is legal in the intended odd-characteristic
field instantiation. -/
theorem fold_pair_reconstruction (a b : Int) :
    let pair := foldPair a b
    pair.1 + pair.2 = 2 * a ∧ pair.1 - pair.2 = 2 * b := by
  dsimp [foldPair]
  omega

def exactAlphabet : List (Int × Int) :=
  [(-2, 0), (-1, -1), (0, -2), (-1, 1), (0, 0), (1, -1),
    (0, 2), (1, 1), (2, 0)]

def sourceValues : List Int := [-1, 0, 1]

def generatedAlphabet : List (Int × Int) :=
  sourceValues.flatMap fun a => sourceValues.map fun b => foldPair a b

theorem exact_local_alphabet_pin : generatedAlphabet = exactAlphabet := by
  native_decide

/-- Exact theorem-shaped moment-split interface. A future concrete field
instantiation supplies the finite sums; this theorem keeps both channels and
their index ranges visible rather than pretending either projection recovers
the parent. -/
theorem marked_even_odd_moment_split
    (w : Nat)
    (parentMoment evenChild oddChild : Nat → Int)
    (evenIdentity : ∀ h, 2 * h ≤ w → parentMoment (2 * h) = evenChild h)
    (oddIdentity : ∀ h, 2 * h + 1 ≤ w → parentMoment (2 * h + 1) = oddChild h) :
    (∀ h, 2 * h ≤ w → parentMoment (2 * h) = evenChild h) ∧
    (∀ h, 2 * h + 1 ≤ w → parentMoment (2 * h + 1) = oddChild h) := by
  exact ⟨evenIdentity, oddIdentity⟩

def IsPseudoforest (componentEdgeCount componentVertexCount : List Nat) : Prop :=
  componentEdgeCount.length = componentVertexCount.length ∧
    ∀ index, index < componentEdgeCount.length →
      componentEdgeCount.get! index ≤ componentVertexCount.get! index

def HasIndegreeOneEndpointAssignment (assignmentExists : Prop) : Prop :=
  assignmentExists

/-- Exact graph-theorem target. The finite verifier checks this equivalence
for all 512 subgraphs of `K_(3,3)`; a future graph-library instantiation must
discharge `graphBridge` from the standard rooted-tree/unicyclic construction. -/
theorem pseudoforest_iff_indegree_one_endpoint_assignment
    (componentEdgeCount componentVertexCount : List Nat)
    (assignmentExists : Prop)
    (graphBridge :
      IsPseudoforest componentEdgeCount componentVertexCount ↔
        HasIndegreeOneEndpointAssignment assignmentExists) :
    IsPseudoforest componentEdgeCount componentVertexCount ↔
      HasIndegreeOneEndpointAssignment assignmentExists := by
  exact graphBridge

/-- Owner-friendly additive interface: parents assigned to the even endpoint
and parents assigned to the odd endpoint are each bounded injectively by the
corresponding realized label set. -/
theorem additive_of_endpoint_partition
    (parentCount evenAssigned oddAssigned evenLabels oddLabels : Nat)
    (partition : parentCount = evenAssigned + oddAssigned)
    (evenInjective : evenAssigned ≤ evenLabels)
    (oddInjective : oddAssigned ≤ oddLabels) :
    parentCount ≤ evenLabels + oddLabels := by
  omega

theorem target_erased_k33_multiplicative_not_additive_pin :
    3 * 3 = 9 ∧ 3 + 3 = 6 ∧ 9 > 6 ∧ 9 - 6 + 1 = 4 := by
  native_decide


/-- Once the depth-two target is carried on both endpoints, the nine fixture
edges split as `K_(2,2)`, `K_(2,1)`, `K_(1,2)`, and `K_(1,1)`. Each component
is a pseudoforest and the global cycle-rank equation has value one. -/
theorem target_tagged_fixture_pseudoforest_pin :
    4 + 2 + 2 + 1 = 9 ∧
    4 + 3 + 3 + 2 = 12 ∧
    4 ≤ 4 ∧ 2 ≤ 3 ∧ 2 ≤ 3 ∧ 1 ≤ 2 ∧
    9 + 4 = 12 + 1 := by
  native_decide
theorem deployed_moment_row_pin :
    67471 / 2 = 33735 ∧ (67471 + 1) / 2 = 33736 := by
  native_decide

def squareFoldPredecessorCommit : String :=
  "f64e03a1215653eeafe3186df55269273d9f7653"
def squareFoldPredecessorNoteBlob : String :=
  "301144d04458027131779907f7f74aa5a6682bf4"
def squareFoldPredecessorVerifierBlob : String :=
  "2507f09115c7eefbc86025dbaf204ea83c744283"
def squareFoldPredecessorLeanBlob : String :=
  "ab061b3c53a320fbb8881bab4e6fa8e573f83248"

theorem exact_square_fold_predecessor_pins :
    squareFoldPredecessorCommit =
      "f64e03a1215653eeafe3186df55269273d9f7653" ∧
    squareFoldPredecessorNoteBlob =
      "301144d04458027131779907f7f74aa5a6682bf4" ∧
    squareFoldPredecessorVerifierBlob =
      "2507f09115c7eefbc86025dbaf204ea83c744283" ∧
    squareFoldPredecessorLeanBlob =
      "ab061b3c53a320fbb8881bab4e6fa8e573f83248" := by
  native_decide


def predecessorRowsDigest : String :=
  "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2"
def predecessorAllFoldRowsDigest : String :=
  "f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877"
def predecessorBaseGraphDigest : String :=
  "620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5"
def predecessorPreExtensionGraphDigest : String :=
  "9bb01a03239c81b4e8110ba55f835f22366920346e00dbe3fef5c9c486519853"

/-- Statement-level digest pins for the exact replay performed by the Python
verifier. Lean does not recompute SHA-256 or enumerate the finite rows. -/
theorem exact_predecessor_replay_digest_pins :
    predecessorRowsDigest =
      "de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2" ∧
    predecessorAllFoldRowsDigest =
      "f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877" ∧
    predecessorBaseGraphDigest =
      "620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5" ∧
    predecessorPreExtensionGraphDigest =
      "9bb01a03239c81b4e8110ba55f835f22366920346e00dbe3fef5c9c486519853" := by
  native_decide

def CycleRankZero (edgeCount vertexCount componentCount : Nat) : Prop :=
  edgeCount + componentCount = vertexCount

/-- Adding an isolated edge adds one edge, two vertices, and one component,
so the cycle-rank-zero equation is preserved. -/
theorem isolated_edge_addition_preserves_cycle_rank_zero
    (edgeCount vertexCount componentCount : Nat)
    (forest : CycleRankZero edgeCount vertexCount componentCount) :
    CycleRankZero (edgeCount + 1) (vertexCount + 2) (componentCount + 1) := by
  unfold CycleRankZero at forest ⊢
  omega

/-- Arithmetic census pins for the replay-derived retained and pre-extension
graphs, including the single isolated extension component. -/
theorem pinned_predecessor_replay_census :
    75 = 75 ∧ 56 = 55 + 1 ∧
    CycleRankZero 55 (55 + 52) 52 ∧
    CycleRankZero 56 (56 + 53) 53 ∧
    56 = 55 + 1 ∧ (56 + 53) = (55 + 52) + 2 ∧ 53 = 52 + 1 := by
  simp [CycleRankZero]
/-- Arithmetic pins for the replay-derived raw forest: 51 isolated edges plus one
`K_(1,4)`, and the pivot-right refinement with 52 isolated edges plus one
`K_(1,3)`. These pins do not assert first-match admission or owner typing. -/
theorem pinned_raw_forest_arithmetic :
    51 + 1 = 52 ∧ 51 + 4 = 55 ∧ 55 ≤ 55 + 52 ∧
    52 + 1 = 53 ∧ 52 + 3 = 55 ∧ 55 ≤ 55 + 53 := by
  native_decide

structure ActualRankGuard where
  actualIncidence : Prop
  allMaximalMinorsVanish : Prop

def RoutesToRankDrop (guard : ActualRankGuard) : Prop :=
  guard.actualIncidence ∧ guard.allMaximalMinorsVanish

/-- A projected child label cannot enter the existing rank owner without both
actual-incidence typing and the all-maximal-minors-vanishing predicate. -/
theorem no_rank_route_without_actual_vanishing
    (guard : ActualRankGuard)
    (noActualVanishing : ¬guard.allMaximalMinorsVanish) :
    ¬RoutesToRankDrop guard := by
  intro route
  exact noActualVanishing route.2

end RouteDSquareFoldCompatibilityGraphV1
