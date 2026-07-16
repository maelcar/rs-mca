import GrandeFinale.PavingBasisAllPairs

/-!
# Augmented-basis pencil/design inverse: formal ledger consequences

This module proves the finite-set and arithmetic consequences consumed by the
audit note.  It does not claim to formalize the source weighted-GRS
linear-algebra bridge that supplies the capacity and load identities.
-/

open scoped BigOperators Classical

namespace GrandeFinale
namespace AugmentedBasisPencilDesignInverse

open PavingBasisAllPairs

set_option autoImplicit false

universe u v

/-! ## Exact capacity/load slack algebra -/

/-- Subtracting the exact pencil load identity from the exact core-capacity
identity gives the global paving slack identity. -/
theorem integer_slack_identity
    {Core Pair : Type*} [Fintype Core] [Fintype Pair]
    (capacity load : Core → ℤ) (localBases : Pair → ℤ)
    (multiplicity beta : ℤ)
    (hcapacity : ∑ J, capacity J = multiplicity * beta)
    (hload : ∑ J, load J = multiplicity * ∑ p, localBases p) :
    multiplicity * (beta - ∑ p, localBases p) =
      ∑ J, (capacity J - load J) := by
  rw [Finset.sum_sub_distrib, hcapacity, hload]
  ring

/-- A finite weighted Markov inequality for a rational threshold
`tau = numerator / denominator`.  Every `bad` core spends at least that
fraction of its capacity in slack. -/
theorem bad_capacity_bound
    {Core : Type*} [Fintype Core] [DecidableEq Core]
    (capacity slack : Core → ℕ) (bad : Finset Core)
    (numerator denominator : ℕ)
    (hbad : ∀ J ∈ bad,
      numerator * capacity J ≤ denominator * slack J) :
    numerator * ∑ J ∈ bad, capacity J ≤
      denominator * ∑ J, slack J := by
  calc
    numerator * ∑ J ∈ bad, capacity J =
        ∑ J ∈ bad, numerator * capacity J := by
          rw [Finset.mul_sum]
    _ ≤ ∑ J ∈ bad, denominator * slack J :=
      Finset.sum_le_sum hbad
    _ ≤ ∑ J, denominator * slack J := by
      exact Finset.sum_le_sum_of_subset (Finset.subset_univ bad)
    _ = denominator * ∑ J, slack J := by
      rw [Finset.mul_sum]

/-! ## Maximal census from an all-bases hypothesis -/

variable {D F : Type*} {kappa : ℕ}
variable [Fintype D] [Field F]

/-- Once every `(kappa+1)`-set is an augmented basis, the basis census is
literally the corresponding binomial coefficient.  The source note proves
the hypothesis from `d=R` using the `[N,kappa+1,R]` MDS subcode `[b1 G]`. -/
theorem basisCensus_eq_choose_of_all_bases
    (A : D → AugmentedCoordinate kappa → F)
    (hall : ∀ I : Finset D, I.card = kappa + 1 →
      rowRank A I = kappa + 1) :
    basisCensus A = Nat.choose (Fintype.card D) (kappa + 1) := by
  have hbasis :
      basisSubsets A = (Finset.univ : Finset D).powersetCard (kappa + 1) := by
    ext I
    simp only [basisSubsets, Finset.mem_filter, Finset.mem_univ,
      true_and, Finset.mem_powersetCard, Finset.subset_univ, true_and]
    constructor
    · exact fun h => h.1
    · intro hcard
      exact ⟨hcard, hall I hcard⟩
  rw [basisCensus, hbasis, Finset.card_powersetCard, Finset.card_univ]

/-! ## Pinned affine-plane PB5 identities -/

theorem f9_affine_line_pb5 :
    Nat.choose 9 2 = 12 * Nat.choose 3 2 := by
  norm_num [Nat.choose]

theorem f25_affine_line_pb5 :
    Nat.choose 25 2 = 30 * Nat.choose 5 2 := by
  norm_num [Nat.choose]

#print axioms integer_slack_identity
#print axioms bad_capacity_bound
#print axioms basisCensus_eq_choose_of_all_bases
#print axioms f9_affine_line_pb5
#print axioms f25_affine_line_pb5

end AugmentedBasisPencilDesignInverse
end GrandeFinale
