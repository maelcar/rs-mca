import GrandeFinale.C0PeriodicF28TargetCompiler

/-!
# Periodic `q = 64`, `f = 28` pairwise target compiler

This module removes the designated-reference boundary from the target-indexed
two-block compiler.  Its input gives projective witnesses between every pair
of targets with distinct residual supports.  When the target is nonempty,
finite choice selects a reference target and the existing target compiler
chooses the remaining projective scales.  When it is empty, the residual and
target bounds are immediate, so no inhabitant of the target type is required.

The deployed classification, quotient data, fixed-residual/scalar Hahn cap,
and first-match cover remain explicit inputs.  No complete `c = 0` parent
bound is claimed.
-/

open Polynomial

namespace GrandeFinale.C0PeriodicF28PairwiseCompiler

open C0PeriodicF28CanonicalBlocks
open C0PeriodicF28DerivedOwner
open C0PeriodicF28TargetCompiler
open C0PeriodicF29ResidualOwner

/-- Target-indexed canonical two-block data with projectivity stated between
every pair of targets on distinct residual supports.  No reference target or
reference-membership proof is supplied. -/
structure PairwiseTargetTwoBlockCertificate
    (α F : Type*) [DecidableEq α] [Field F] [DecidableEq F] where
  target : Finset α
  ambient : Finset F
  residualSupport : α → Finset F
  quotient : α → F[X]
  ambient_card : ambient.card = 2097152
  ambient_ne_zero : ∀ z ∈ ambient, z ≠ 0
  residual_subset : ∀ x ∈ target, residualSupport x ⊆ ambient
  residual_card : ∀ x ∈ target, (residualSupport x).card = 63601
  quotient_constant_ne_zero : ∀ x ∈ target, (quotient x).coeff 0 ≠ 0
  projective : ∀ x ∈ target, ∀ y ∈ target,
    residualSupport x ≠ residualSupport y →
      ∃ c : F,
        DeployedProjective
          (canonicalLowerBlock 32768 (residualSupport x))
          (canonicalUpperBlock 32768 (residualSupport x)) (quotient x)
          (canonicalLowerBlock 32768 (residualSupport y))
          (canonicalUpperBlock 32768 (residualSupport y)) (quotient y) c

/-- Distinct residual supports realized by the pairwise target family. -/
def PairwiseTargetTwoBlockCertificate.residuals
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F) : Finset (Finset F) :=
  cert.target.image cert.residualSupport

/-- Choose a reference target from a proof that the target family is
nonempty. -/
noncomputable def PairwiseTargetTwoBlockCertificate.chosenReference
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F)
    (hne : cert.target.Nonempty) : α :=
  Classical.choose hne

theorem PairwiseTargetTwoBlockCertificate.chosenReference_mem
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F)
    (hne : cert.target.Nonempty) : cert.chosenReference hne ∈ cert.target :=
  Classical.choose_spec hne

/-- On a nonempty target family, finite choice supplies the reference required
by the target-indexed compiler.  Pairwise projectivity supplies every
projective witness relative to that chosen reference. -/
noncomputable def PairwiseTargetTwoBlockCertificate.toTargetTwoBlockCertificate
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F)
    (hne : cert.target.Nonempty) : TargetTwoBlockCertificate α F where
  target := cert.target
  ambient := cert.ambient
  residualSupport := cert.residualSupport
  referenceTarget := cert.chosenReference hne
  quotient := cert.quotient
  reference_mem_of_nonempty := fun _ ↦ cert.chosenReference_mem hne
  ambient_card := cert.ambient_card
  ambient_ne_zero := cert.ambient_ne_zero
  residual_subset := cert.residual_subset
  residual_card := cert.residual_card
  quotient_constant_ne_zero := cert.quotient_constant_ne_zero
  projective := by
    intro x hx hsupport
    exact cert.projective x hx (cert.chosenReference hne)
      (cert.chosenReference_mem hne) hsupport

@[simp] theorem PairwiseTargetTwoBlockCertificate.toTarget_residuals
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F)
    (hne : cert.target.Nonempty) :
    (cert.toTargetTwoBlockCertificate hne).residuals = cert.residuals := rfl

/-- The pairwise certificate has at most 63 distinct residual supports.  The
empty branch is immediate; the nonempty branch chooses a reference and invokes
the target-indexed compiler. -/
theorem PairwiseTargetTwoBlockCertificate.distinct_residuals_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F) :
    cert.residuals.card ≤ 63 := by
  by_cases hne : cert.target.Nonempty
  · simpa only [cert.toTarget_residuals hne] using
      (cert.toTargetTwoBlockCertificate hne).distinct_residuals_card_le
  · rw [PairwiseTargetTwoBlockCertificate.residuals,
      Finset.not_nonempty_iff_eq_empty.mp hne]
    simp

/-- Exact deployed q64, `f = 28` target cap from pairwise projectivity and the
supplied fixed cells, without a designated reference target. -/
theorem PairwiseTargetTwoBlockCertificate.target_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : PairwiseTargetTwoBlockCertificate α F)
    (scalarClass : α → Fin 64)
    (fixedResidualScalarCap : ∀ R ∈ cert.residuals, ∀ s : Fin 64,
      (cert.target.filter fun x ↦
        cert.residualSupport x = R ∧ scalarClass x = s).card ≤ 20826085) :
    cert.target.card ≤ 83970774720 := by
  by_cases hne : cert.target.Nonempty
  · apply (cert.toTargetTwoBlockCertificate hne).target_card_le scalarClass
    intro R hR s
    exact fixedResidualScalarCap R hR s
  · rw [Finset.not_nonempty_iff_eq_empty.mp hne]
    simp

/-- PR #819's first-match payment with q64, `f = 28` pairwise projectivity
and no supplied reference target. -/
theorem c0_periodic_first_match_payment_of_pairwise_target_certificate
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (bad : Finset α)
    (cert28 : PairwiseTargetTwoBlockCertificate α F)
    (scalarClass : α → Fin 64)
    (fixedResidualScalarCap : ∀ R ∈ cert28.residuals, ∀ s : Fin 64,
      (cert28.target.filter fun x ↦
        cert28.residualSupport x = R ∧ scalarClass x = s).card ≤ 20826085)
    (cert29 : F29ProjectiveRayCertificate α F)
    (cert5 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 5 14641173)
    (cert7 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128)
    (hcover : bad ⊆
      cert29.target ∪ cert28.target ∪ cert5.target ∪ cert7.target) :
    bad.card ≤ 16501904760592192 :=
  C0PeriodicSingletonCertificate.c0_periodic_first_match_payment_of_singleton_certificates
    bad cert29.target cert28.target cert5 cert7 hthree hambient hcover
    cert29.target_card_le
    (cert28.target_card_le scalarClass fixedResidualScalarCap)

#print axioms PairwiseTargetTwoBlockCertificate.chosenReference_mem
#print axioms PairwiseTargetTwoBlockCertificate.toTargetTwoBlockCertificate
#print axioms PairwiseTargetTwoBlockCertificate.distinct_residuals_card_le
#print axioms PairwiseTargetTwoBlockCertificate.target_card_le
#print axioms c0_periodic_first_match_payment_of_pairwise_target_certificate

end GrandeFinale.C0PeriodicF28PairwiseCompiler
