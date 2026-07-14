import GrandeFinale.DirectionDistanceAllPairs

/-!
# Selector-free exact-weight two-block bounds

This module contains only **UNPROVED STATEMENT TARGETS**. It records the
exact-weight refinement of the realized-puncture compiler for the complete
`(slope,error)` pair set. In particular, it does not choose one witness per
slope and it does not contain a Lean proof.
-/

open scoped BigOperators Classical

noncomputable section

namespace GrandeFinale
namespace ExactWeightAllPairs

open DirectionDistanceAllPairs

set_option autoImplicit false

universe u v w

variable {D : Type u} {F : Type v} {W : Type w}
variable [Fintype D] [DecidableEq D]
variable [Field F] [DecidableEq F]
variable [AddCommGroup W] [Module F W]

abbrev Pair (D : Type u) (F : Type v) := SlopeErrorPair D F

def exactRealizedWords (P : Finset (Pair D F)) (vMin : D → F)
    (j : ℕ) : Finset (D → F) :=
  (realizedWords P vMin).filter fun z => weight z = j

def exactPairs (P : Finset (Pair D F)) (vMin : D → F)
    (j : ℕ) : Finset (Pair D F) :=
  P.filter fun p => weight (pairPuncture vMin p) = j

def exactHeight (d t j : ℕ) : ℕ :=
  max 1 (d + j - t)

/-- Subtraction-safe nonnegative part of
`Ξ_j=d(M-j)²+M h_j²-dM²`. -/
def twoBlockMargin (d M t j : ℕ) : ℕ :=
  d * (M - j) ^ 2 + M * (exactHeight d t j) ^ 2 - d * M ^ 2

def TwoBlockStrict (d M t j : ℕ) : Prop :=
  d * M ^ 2 < d * (M - j) ^ 2 + M * (exactHeight d t j) ^ 2

def TwoBlockEquality (d M t j : ℕ) : Prop :=
  d * M ^ 2 = d * (M - j) ^ 2 + M * (exactHeight d t j) ^ 2

def TwoBlockNonnegative (d M t j : ℕ) : Prop :=
  d * M ^ 2 ≤ d * (M - j) ^ 2 + M * (exactHeight d t j) ^ 2

/-- The separation `D_j=min(M,max(Δ,d+2j-2t))`, with truncated naturals. -/
def exactSeparation (M Δ d t j : ℕ) : ℕ :=
  min M (max Δ (d + 2 * j - 2 * t))

/-- Subtraction-safe form of `Q_j=M D_j-2Mj+j²`. -/
def exactDenominator (M Δ d t j : ℕ) : ℕ :=
  M * exactSeparation M Δ d t j + j ^ 2 - 2 * M * j

def exactNumerator (M Δ d t j : ℕ) : ℕ :=
  M * (exactSeparation M Δ d t j - j)

def ExactWeightPositive (M Δ d t j : ℕ) : Prop :=
  2 * M * j < M * exactSeparation M Δ d t j + j ^ 2

def ExactWeightConclusion (P : Finset (Pair D F)) (vMin : D → F)
    (t Δ j : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  let den := exactDenominator M Δ d t j
  let num := exactNumerator M Δ d t j
  let Wj := exactRealizedWords P vMin j
  let Pj := exactPairs P vMin j
  Wj.card * den ≤ num ∧
    Wj.card ≤ num / den ∧
    Pj.card = ∑ z ∈ Wj, (realizedCluster P vMin z).card ∧
    Pj.card ≤ (d / exactHeight d t j) * Wj.card ∧
    Pj.card ≤ (d / exactHeight d t j) * (num / den)

def ExactWeightHypotheses (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t Δ j : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  LowExactHypotheses H y₀ y₁ b₀ vMin P t ∧
    KernelDistanceAtLeast H d ∧
    PuncturedKernelDistanceAtLeast H (wordSupport vMin) Δ ∧
    Δ ≤ M ∧ j ≤ min t M ∧ ExactWeightPositive M Δ d t j

def CompletedTwoBlockHypotheses (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t j : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  BasicPairHypotheses H y₀ y₁ P t ∧
    HostedMinimumLift H y₀ y₁ b₀ vMin ∧
    PairTransverse H y₀ y₁ P ∧
    KernelDistanceAtLeast H d ∧
    j ≤ min t M

/-! ## Complete-zero-mask two-block targets -/

/--
**UNPROVED STATEMENT TARGET (strict completed two-block all-pair bound).**

The counted object is the complete exact-weight pair set, not a set obtained
by selecting one witness at each slope.
-/
def strictTwoBlockAllPairTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t j : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  CompletedTwoBlockHypotheses H y₀ y₁ b₀ vMin P t j →
    0 < j → j < M → TwoBlockStrict d M t j →
    (exactPairs P vMin j).card ≤ Fintype.card D - 1

/-- **UNPROVED STATEMENT TARGET (equality-face all-pair bound).** -/
def equalityTwoBlockAllPairTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t j : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  CompletedTwoBlockHypotheses H y₀ y₁ b₀ vMin P t j →
    0 < j → j < M → TwoBlockEquality d M t j →
    (exactPairs P vMin j).card ≤ 2 * (Fintype.card D - 2)

/-- **UNPROVED STATEMENT TARGET (zero punctured-weight all-pair endpoint).** -/
def zeroWeightTwoBlockAllPairTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t : ℕ) : Prop :=
  let d := weight vMin
  CompletedTwoBlockHypotheses H y₀ y₁ b₀ vMin P t 0 →
    (exactPairs P vMin 0).card ≤ d / exactHeight d t 0

/-- **UNPROVED STATEMENT TARGET (full punctured-weight all-pair endpoint).** -/
def fullWeightTwoBlockAllPairTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  CompletedTwoBlockHypotheses H y₀ y₁ b₀ vMin P t M →
    KernelDistanceAtLeast H (t + 1) →
    TwoBlockNonnegative d M t M →
    (exactPairs P vMin M).card ≤ 2 * d - 1

def AllOccupiedTwoBlockNonnegative (P : Finset (Pair D F))
    (vMin : D → F) (t : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  ∀ j ≤ min t M, (exactPairs P vMin j).Nonempty →
    TwoBlockNonnegative d M t j

/-- **UNPROVED STATEMENT TARGET (all nonnegative two-block strata).** -/
def allNonnegativeTwoBlockTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t : ℕ) : Prop :=
  CompletedTwoBlockHypotheses H y₀ y₁ b₀ vMin P t 0 →
    KernelDistanceAtLeast H (t + 1) →
    AllOccupiedTwoBlockNonnegative P vMin t →
    P.card < 2 * (Fintype.card D) ^ 2

/--
**UNPROVED STATEMENT TARGET (selector-free exact-weight two-block bound).**

No hypothesis `t < M` is imposed. The target applies to every individual
positive-denominator stratum, including those inside a `t ≥ M` chart.
-/
def exactWeightAllPairTarget (H : (D → F) →ₗ[F] W) (y₀ y₁ : W)
    (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t Δ j : ℕ) : Prop :=
  ExactWeightHypotheses H y₀ y₁ b₀ vMin P t Δ j →
    ExactWeightConclusion P vMin t Δ j

/-- **UNPROVED STATEMENT TARGET (same-slope kernel alternative).** -/
def sameSlopeKernelDifferenceTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t : ℕ) : Prop :=
  LowExactHypotheses H y₀ y₁ b₀ vMin P t →
    KernelDistanceAtLeast H (weight vMin) →
    ∀ p ∈ P, ∀ q ∈ P, p ≠ q → p.1 = q.1 →
      H (p.2 - q.2) = 0 ∧ p.2 - q.2 ≠ 0 ∧
        weight vMin ≤ weight (p.2 - q.2)

def AllOccupiedExactWeightsPositive (P : Finset (Pair D F))
    (vMin : D → F) (t Δ : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  ∀ j ≤ min t M, (exactPairs P vMin j).Nonempty →
    ExactWeightPositive M Δ d t j

/-- **UNPROVED STATEMENT TARGET (polynomial compilation of all occupied strata).** -/
def allPositiveExactWeightsTarget (H : (D → F) →ₗ[F] W)
    (y₀ y₁ : W) (b₀ vMin : D → F) (P : Finset (Pair D F))
    (t Δ : ℕ) : Prop :=
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  LowExactHypotheses H y₀ y₁ b₀ vMin P t →
    KernelDistanceAtLeast H d →
    PuncturedKernelDistanceAtLeast H (wordSupport vMin) Δ →
    Δ ≤ M → AllOccupiedExactWeightsPositive P vMin t Δ →
    P.card ≤ (Fintype.card D) ^ 4

/-- **UNPROVED STATEMENT TARGET (direct LineRay exact-weight transfer).** -/
def lineRayExactWeightTarget (H : (D → F) →ₗ[F] W)
    (u vLine vMin : D → F) (P : Finset (Pair D F))
    (t Δ j : ℕ) : Prop :=
  let Q := lineRaySyndromePairs u vLine P
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  BasicLineRayHypotheses H u vLine P t →
    LineRayTransverse H u vLine P →
    HostedMinimumLift H (H u) (H vLine) u vMin →
    PunctureInjectiveOnKernel H (wordSupport vMin) →
    KernelDistanceAtLeast H d →
    PuncturedKernelDistanceAtLeast H (wordSupport vMin) Δ →
    Δ ≤ M → j ≤ min t M → ExactWeightPositive M Δ d t j →
    Q.card = P.card ∧ ExactWeightConclusion Q vMin t Δ j

/-- **UNPROVED STATEMENT TARGET (direct LineRay strict-Xi transfer).** -/
def lineRayStrictTwoBlockTarget (H : (D → F) →ₗ[F] W)
    (u vLine vMin : D → F) (P : Finset (Pair D F))
    (t j : ℕ) : Prop :=
  let Q := lineRaySyndromePairs u vLine P
  let d := weight vMin
  let M := (outsideCoords (wordSupport vMin)).card
  BasicLineRayHypotheses H u vLine P t →
    LineRayTransverse H u vLine P →
    HostedMinimumLift H (H u) (H vLine) u vMin →
    KernelDistanceAtLeast H d →
    0 < j → j ≤ min t M → j < M → TwoBlockStrict d M t j →
    Q.card = P.card ∧
      (exactPairs Q vMin j).card ≤ Fintype.card D - 1

/-- **UNPROVED STATEMENT TARGET (direct LineRay all-nonnegative transfer).** -/
def lineRayAllNonnegativeTwoBlockTarget (H : (D → F) →ₗ[F] W)
    (u vLine vMin : D → F) (P : Finset (Pair D F))
    (t : ℕ) : Prop :=
  let Q := lineRaySyndromePairs u vLine P
  let d := weight vMin
  BasicLineRayHypotheses H u vLine P t →
    LineRayTransverse H u vLine P →
    HostedMinimumLift H (H u) (H vLine) u vMin →
    KernelDistanceAtLeast H d →
    KernelDistanceAtLeast H (t + 1) →
    AllOccupiedTwoBlockNonnegative Q vMin t →
    Q.card = P.card ∧ P.card < 2 * (Fintype.card D) ^ 2

end ExactWeightAllPairs
end GrandeFinale
