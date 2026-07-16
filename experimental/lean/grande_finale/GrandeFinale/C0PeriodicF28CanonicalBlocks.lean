import GrandeFinale.C0PeriodicF28TwoBlockCompiler

/-!
# Canonical blocks of the periodic `q = 64`, `f = 28` residual locator

Euclidean division by `X^B` canonically splits a support locator into its
lower and upper coefficient blocks.  For a support of size `B + m`, this
module proves the exact decomposition, lower-block degree bound, upper-block
degree, and upper-block monicity.  The deployed specialization
`B = 32,768`, `m = 30,833` derives three algebraic fields previously
supplied to the target-indexed owner and also proves uniqueness of any valid
deployed two-block decomposition.
-/

open Polynomial
open GrandeFinale.C0PeriodicF29ResidualOwner
open GrandeFinale.C0PeriodicF28TwoBlockCompiler

namespace GrandeFinale.C0PeriodicF28CanonicalBlocks

/-- Coefficients of the support locator below the periodic block boundary. -/
noncomputable def canonicalLowerBlock
    {F : Type*} [Field F] (B : ℕ) (R : Finset F) : F[X] :=
  supportLocator R %ₘ X ^ B

/-- The remaining support-locator coefficients after the periodic boundary. -/
noncomputable def canonicalUpperBlock
    {F : Type*} [Field F] (B : ℕ) (R : Finset F) : F[X] :=
  supportLocator R /ₘ X ^ B

/-- A support locator of degree `B + m` has a canonical monic two-block
decomposition at boundary `B`. -/
theorem supportLocator_canonical_twoBlock
    {F : Type*} [Field F]
    (B m : ℕ) (hB : 0 < B) (R : Finset F)
    (hcard : R.card = B + m) :
    supportLocator R =
        canonicalLowerBlock B R + X ^ B * canonicalUpperBlock B R ∧
      (canonicalLowerBlock B R).natDegree < B ∧
      (canonicalUpperBlock B R).natDegree = m ∧
      (canonicalUpperBlock B R).Monic := by
  have hXpow_ne_one : (X ^ B : F[X]) ≠ 1 := by
    intro heq
    have hdegree := congrArg natDegree heq
    have : B = 0 := by
      simpa only [natDegree_X_pow, natDegree_one] using hdegree
    omega
  constructor
  · exact (modByMonic_add_div (supportLocator R) (monic_X_pow B)).symm
  constructor
  · unfold canonicalLowerBlock
    simpa only [natDegree_X_pow] using natDegree_modByMonic_lt
      (supportLocator R) (monic_X_pow B) hXpow_ne_one
  constructor
  · rw [canonicalUpperBlock,
      natDegree_divByMonic (supportLocator R) (monic_X_pow B),
      supportLocator_natDegree, natDegree_X_pow, hcard]
    omega
  · have hdegree : (X ^ B : F[X]).degree ≤
        (supportLocator R).degree := by
      rw [degree_eq_natDegree (monic_X_pow B).ne_zero,
        degree_eq_natDegree (supportLocator_monic R).ne_zero,
        natDegree_X_pow, supportLocator_natDegree, hcard]
      exact_mod_cast Nat.le_add_right B m
    rw [Monic, canonicalUpperBlock,
      leadingCoeff_divByMonic_of_monic (monic_X_pow B) hdegree,
      (supportLocator_monic R).leadingCoeff]

/-- Literal q64, `f = 28` canonical block data for a residual support of
size `63,601`. -/
theorem supportLocator_deployed_twoBlock
    {F : Type*} [Field F] (R : Finset F)
    (hcard : R.card = 63601) :
    supportLocator R =
        canonicalLowerBlock 32768 R +
          X ^ 32768 * canonicalUpperBlock 32768 R ∧
      (canonicalLowerBlock 32768 R).natDegree < 32768 ∧
      (canonicalUpperBlock 32768 R).natDegree = 30833 ∧
      (canonicalUpperBlock 32768 R).Monic := by
  exact supportLocator_canonical_twoBlock
    32768 30833 (by norm_num) R (by omega)

/-- Every deployed two-block representation with a short lower block is the
canonical Euclidean-division representation. -/
theorem supportLocator_deployed_twoBlock_unique
    {F : Type*} [Field F] (R : Finset F)
    (hcard : R.card = 63601) (A₀ A₁ : F[X])
    (hA₀ : A₀.natDegree < 32768)
    (heq : supportLocator R = A₀ + X ^ 32768 * A₁) :
    A₀ = canonicalLowerBlock 32768 R ∧
      A₁ = canonicalUpperBlock 32768 R := by
  have hcanonical := supportLocator_deployed_twoBlock R hcard
  exact eq_blocks_of_add_X_pow_mul_eq
    32768 A₀ A₁ (canonicalLowerBlock 32768 R)
    (canonicalUpperBlock 32768 R) hA₀ hcanonical.2.1
    (heq.symm.trans hcanonical.1)

#print axioms supportLocator_canonical_twoBlock
#print axioms supportLocator_deployed_twoBlock
#print axioms supportLocator_deployed_twoBlock_unique

end GrandeFinale.C0PeriodicF28CanonicalBlocks
