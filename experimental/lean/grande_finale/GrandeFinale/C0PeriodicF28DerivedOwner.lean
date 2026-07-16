import GrandeFinale.C0PeriodicF28ScalarPencil
import GrandeFinale.C0PeriodicF28ResidualPencil

/-!
# Periodic `q = 64`, `f = 28` derived residual owner

This module joins the deployed two-block algebra to the support-level residual
pencil.  A typed certificate records distinct residual supports, their literal
`32,768`-block locator decompositions, one representative quotient per support,
and projective congruences modulo `X^67,472` relative to a reference support.

If the family has at least two members, the compiler derives the scalar normal
form of every residual and the `30,833` degree cut, proves the low block has
nonzero constant term, and constructs
`C0PeriodicF28ResidualPencil.ResidualPencilCertificate`.  Zero- and one-member
families are immediate, so every certified family has at most 63 residual
supports.

An outer certificate then reuses the 64 scalar classes and supplied fixed-cell
Hahn cap to recover the exact q64 `f = 28` target cap and PR #819 first-match
payment.  The canonical deployed classification, representative selection,
local Hahn proof, and first-match cover remain explicit inputs.  No complete
`c = 0` parent bound is claimed.
-/

open Polynomial
open GrandeFinale.C0PeriodicF29ResidualOwner

namespace GrandeFinale.C0PeriodicF28DerivedOwner

/-- Literal deployed two-block residual, factored behind a named definition to
keep large exponents out of dependent structure fields. -/
noncomputable def deployedResidual
    {F : Type*} [Field F] (A₀ A₁ : F[X]) : F[X] :=
  A₀ + C0PeriodicF28ResidualPencil.periodicDirection A₁

theorem deployedResidual_eq
    {F : Type*} [Field F] (A₀ A₁ : F[X]) :
    deployedResidual A₀ A₁ = A₀ + X ^ 32768 * A₁ := by
  rw [deployedResidual,
    C0PeriodicF28ResidualPencil.periodicDirection_eq_X_pow_mul]

/-- A generic coefficient-vanishing interface to the two-block compiler.  Its
result contains no large power, so deployed specializations remain compact. -/
theorem blocks_of_projective_coefficients
    {F : Type*} [Field F]
    (B a : ℕ) (h2Ba : B * 2 ≤ a)
    (A₀ A₁ Q U V Qref : F[X]) (c : F)
    (hA₀ : A₀.natDegree < B) (hA₁ : A₁.natDegree < B)
    (hU : U.natDegree < B) (hV : V.natDegree < B)
    (hprojective :
      ∀ d < a,
        (periodicLocator B (A₀ + X ^ B * A₁) Q -
          C c * periodicLocator B (U + X ^ B * V) Qref).coeff d = 0) :
    C (Q.coeff 0) * A₀ = C (c * Qref.coeff 0) * U ∧
      C (Q.coeff 0) * A₁ + C (Q.coeff 1) * A₀ =
        C c * (C (Qref.coeff 0) * V + C (Qref.coeff 1) * U) := by
  apply C0PeriodicF28TwoBlockCompiler.twoBlockApprox_blocks_eq_of_projective
    B a h2Ba A₀ A₁ Q U V Qref c hA₀ hA₁ hU hV
  exact (X_pow_dvd_iff).2 hprojective

/-- Projective congruence for the deployed two-block periodic locators,
represented by coefficient vanishing below degree `67,472`. -/
def DeployedProjective
    {F : Type*} [Field F]
    (A₀ A₁ Q U V Qref : F[X]) (c : F) : Prop :=
  ∀ d < 67472,
    (periodicLocator 32768 (deployedResidual A₀ A₁) Q -
      C c * periodicLocator 32768 (deployedResidual U V) Qref).coeff d = 0

/-- Canonical two-block data for one deployed q64, `f = 28` residual family in
a single projective residue ray.  The residuals themselves form the index, so
the family is deduplicated by construction. -/
structure TwoBlockFamilyCertificate
    (F : Type*) [Field F] [DecidableEq F] where
  ambient : Finset F
  residuals : Finset (Finset F)
  reference : Finset F
  lowerBlock : Finset F → F[X]
  upperBlock : Finset F → F[X]
  quotient : Finset F → F[X]
  rayScale : Finset F → F
  ambient_card : ambient.card = 2097152
  ambient_ne_zero : ∀ z ∈ ambient, z ≠ 0
  residual_subset : ∀ R ∈ residuals, R ⊆ ambient
  residual_card : ∀ R ∈ residuals, R.card = 63601
  decomposition : ∀ R ∈ residuals,
    supportLocator R = deployedResidual (lowerBlock R) (upperBlock R)
  lower_degree_lt : ∀ R ∈ residuals,
    (lowerBlock R).natDegree < 32768
  upper_degree : ∀ R ∈ residuals,
    (upperBlock R).natDegree = 30833
  quotient_constant_ne_zero : ∀ R ∈ residuals,
    (quotient R).coeff 0 ≠ 0
  rayScale_ne_zero : ∀ R ∈ residuals, rayScale R ≠ 0
  reference_mem_of_two : 2 ≤ residuals.card → reference ∈ residuals
  projective : ∀ R ∈ residuals, R ≠ reference →
    DeployedProjective
      (lowerBlock R) (upperBlock R) (quotient R)
      (lowerBlock reference) (upperBlock reference) (quotient reference)
      (rayScale R)

/-- Normalization relative to the chosen reference residual. -/
def TwoBlockFamilyCertificate.normalization
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F) (R : Finset F) : F :=
  if R = cert.reference then 1
  else cert.rayScale R * (cert.quotient cert.reference).coeff 0 /
    (cert.quotient R).coeff 0

/-- Affine pencil parameter `lambda_reference - lambda_R`. -/
def TwoBlockFamilyCertificate.parameter
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F) (R : Finset F) : F :=
  if R = cert.reference then 0
  else (cert.quotient cert.reference).coeff 1 /
      (cert.quotient cert.reference).coeff 0 -
    (cert.quotient R).coeff 1 / (cert.quotient R).coeff 0

theorem supportLocator_coeff_zero_ne_zero_of_subset
    {F : Type*} [Field F] [DecidableEq F]
    (ambient S : Finset F)
    (hsub : S ⊆ ambient) (hne : ∀ z ∈ ambient, z ≠ 0) :
    (supportLocator S).coeff 0 ≠ 0 := by
  rw [coeff_zero_eq_eval_zero]
  unfold supportLocator
  rw [eval_prod]
  simp only [eval_sub, eval_X, eval_C, zero_sub]
  rw [Finset.prod_ne_zero_iff]
  intro z hz
  exact neg_ne_zero.mpr (hne z (hsub hz))

theorem TwoBlockFamilyCertificate.residualPolynomial_monic
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    {R : Finset F} (hR : R ∈ cert.residuals) :
    (cert.lowerBlock R + X ^ 32768 * cert.upperBlock R).Monic := by
  rw [← deployedResidual_eq, ← cert.decomposition R hR]
  exact supportLocator_monic R

theorem TwoBlockFamilyCertificate.residualPolynomial_injective
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F) :
    Set.InjOn
      (fun R ↦ cert.lowerBlock R + X ^ 32768 * cert.upperBlock R)
      cert.residuals := by
  intro R hR S hS heq
  apply supportLocator_injective
  rw [cert.decomposition R hR, cert.decomposition S hS,
    deployedResidual_eq, deployedResidual_eq]
  exact heq

theorem TwoBlockFamilyCertificate.normalization_ne_zero
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    (htwo : 2 ≤ cert.residuals.card) :
    ∀ R ∈ cert.residuals, cert.normalization R ≠ 0 := by
  have href := cert.reference_mem_of_two htwo
  intro R hR
  by_cases hRref : R = cert.reference
  · simp [TwoBlockFamilyCertificate.normalization, hRref]
  · rw [TwoBlockFamilyCertificate.normalization, if_neg hRref]
    exact div_ne_zero
      (mul_ne_zero (cert.rayScale_ne_zero R hR)
        (cert.quotient_constant_ne_zero cert.reference href))
      (cert.quotient_constant_ne_zero R hR)

/-- Projective congruence exposes both normalized residual blocks relative to
the reference member. -/
theorem TwoBlockFamilyCertificate.normalized_blocks
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    (htwo : 2 ≤ cert.residuals.card)
    {R : Finset F} (hR : R ∈ cert.residuals) :
    cert.lowerBlock R = C (cert.normalization R) *
        cert.lowerBlock cert.reference ∧
      cert.upperBlock R = C (cert.normalization R) *
        (cert.upperBlock cert.reference +
          C (cert.parameter R) * cert.lowerBlock cert.reference) := by
  have href := cert.reference_mem_of_two htwo
  by_cases hRref : R = cert.reference
  · subst R
    simp [TwoBlockFamilyCertificate.normalization,
      TwoBlockFamilyCertificate.parameter]
  · have hblocks :=
      blocks_of_projective_coefficients
      32768 67472 (by norm_num)
      (cert.lowerBlock R) (cert.upperBlock R) (cert.quotient R)
      (cert.lowerBlock cert.reference) (cert.upperBlock cert.reference)
      (cert.quotient cert.reference) (cert.rayScale R)
      (cert.lower_degree_lt R hR)
      (by rw [cert.upper_degree R hR]; norm_num)
      (cert.lower_degree_lt cert.reference href)
      (by rw [cert.upper_degree cert.reference href]; norm_num)
      (fun d hd => by
        simpa only [← deployedResidual_eq] using
          cert.projective R hR hRref d hd)
    have hnormalized :=
      C0PeriodicF28ScalarPencil.blocks_eq_scaled_reference_pencil_of_block_equations
      (cert.lowerBlock R) (cert.upperBlock R)
      (cert.lowerBlock cert.reference) (cert.upperBlock cert.reference)
      ((cert.quotient R).coeff 0) ((cert.quotient R).coeff 1)
      (cert.rayScale R) ((cert.quotient cert.reference).coeff 0)
      ((cert.quotient cert.reference).coeff 1)
      (cert.quotient_constant_ne_zero R hR)
      (cert.quotient_constant_ne_zero cert.reference href)
      hblocks.1 hblocks.2
    simpa [TwoBlockFamilyCertificate.normalization,
      TwoBlockFamilyCertificate.parameter, hRref] using hnormalized

/-- A family containing at least two residuals derives the deployed low-block
degree cut rather than assuming it. -/
theorem TwoBlockFamilyCertificate.lowBlock_degree_le
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    (htwo : 2 ≤ cert.residuals.card) :
    (cert.lowerBlock cert.reference).natDegree ≤ 30833 := by
  have href := cert.reference_mem_of_two htwo
  apply C0PeriodicF28ScalarPencil.lowBlock_degree_le_30833_of_family_card_two
    32768 cert.residuals cert.reference
    (cert.lowerBlock cert.reference) (cert.upperBlock cert.reference)
    cert.lowerBlock cert.upperBlock cert.normalization cert.parameter
    htwo href ⟨rfl, rfl⟩
  · exact cert.normalization_ne_zero htwo
  · intro R hR
    exact (cert.normalized_blocks htwo hR).1
  · intro R hR
    exact (cert.normalized_blocks htwo hR).2
  · intro R hR
    rw [cert.upper_degree R hR]
  · rw [cert.upper_degree cert.reference href]
  · intro R hR
    exact cert.residualPolynomial_monic hR
  · exact cert.residualPolynomial_injective

/-- Nonzero deployed support points force the reference low block to have
nonzero constant term. -/
theorem TwoBlockFamilyCertificate.lowBlock_constant_ne_zero
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    (htwo : 2 ≤ cert.residuals.card) :
    (cert.lowerBlock cert.reference).coeff 0 ≠ 0 := by
  have href := cert.reference_mem_of_two htwo
  have hsupp := supportLocator_coeff_zero_ne_zero_of_subset
    cert.ambient cert.reference (cert.residual_subset cert.reference href)
    cert.ambient_ne_zero
  have hcoeff : (supportLocator cert.reference).coeff 0 =
      (cert.lowerBlock cert.reference).coeff 0 := by
    rw [cert.decomposition cert.reference href]
    rw [deployedResidual_eq]
    simp
  rw [hcoeff] at hsupp
  exact hsupp

/-- In the nontrivial-family branch, the canonical two-block data compile to
the existing residual-pencil certificate. -/
noncomputable def TwoBlockFamilyCertificate.toResidualPencilCertificate
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F)
    (htwo : 2 ≤ cert.residuals.card) :
    C0PeriodicF28ResidualPencil.ResidualPencilCertificate F where
  ambient := cert.ambient
  residuals := cert.residuals
  parameter := cert.parameter
  scale := cert.normalization
  basePolynomial := cert.lowerBlock cert.reference +
    X ^ 32768 * cert.upperBlock cert.reference
  directionPolynomial := C0PeriodicF28ResidualPencil.periodicDirection
    (cert.lowerBlock cert.reference)
  lowBlock := cert.lowerBlock cert.reference
  ambient_card := cert.ambient_card
  ambient_ne_zero := cert.ambient_ne_zero
  residual_subset := cert.residual_subset
  residual_card := cert.residual_card
  scale_ne_zero := cert.normalization_ne_zero htwo
  pencil_representation := by
    intro R hR
    rw [cert.decomposition R hR]
    rw [deployedResidual_eq]
    rcases cert.normalized_blocks htwo hR with ⟨hlower, hupper⟩
    rw [hlower, hupper,
      C0PeriodicF28ResidualPencil.periodicDirection_eq_X_pow_mul]
    ring
  direction_eq := rfl
  lowBlock_natDegree := cert.lowBlock_degree_le htwo
  lowBlock_constant_ne_zero := cert.lowBlock_constant_ne_zero htwo

/-- Complete owner cap: zero- and one-member families are immediate; every
larger family compiles to the residual-pencil packing theorem. -/
theorem TwoBlockFamilyCertificate.residuals_card_le
    {F : Type*} [Field F] [DecidableEq F]
    (cert : TwoBlockFamilyCertificate F) :
    cert.residuals.card ≤ 63 := by
  by_cases htwo : 2 ≤ cert.residuals.card
  · exact (cert.toResidualPencilCertificate htwo).residuals_card_le
  · omega

/-! ## Explicit fixed-cell and first-match wrapper -/

/-- The deployed two-block owner together with the still-supplied residual
classification and fixed-residual/scalar Hahn cells. -/
structure TwoBlockProjectiveRayCertificate
    (α F : Type*) [DecidableEq α] [Field F] [DecidableEq F] where
  target : Finset α
  owner : TwoBlockFamilyCertificate F
  residualSupport : α → Finset F
  scalarClass : α → Fin 64
  residual_member : ∀ x ∈ target,
    residualSupport x ∈ owner.residuals
  fixedResidualScalarCap : ∀ R ∈ owner.residuals, ∀ s : Fin 64,
    (target.filter fun x ↦
      residualSupport x = R ∧ scalarClass x = s).card ≤ 20826085

def TwoBlockProjectiveRayCertificate.scalarCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F)
    (R : Finset F) (s : Fin 64) : Finset α :=
  cert.target.filter fun x ↦
    cert.residualSupport x = R ∧ cert.scalarClass x = s

def TwoBlockProjectiveRayCertificate.residualCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F)
    (R : Finset F) : Finset α :=
  cert.target.filter fun x ↦ cert.residualSupport x = R

theorem TwoBlockProjectiveRayCertificate.biUnion_scalarCell_eq_residualCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F) (R : Finset F) :
    (Finset.univ : Finset (Fin 64)).biUnion (cert.scalarCell R) =
      cert.residualCell R := by
  ext x
  simp [TwoBlockProjectiveRayCertificate.scalarCell,
    TwoBlockProjectiveRayCertificate.residualCell]

theorem TwoBlockProjectiveRayCertificate.residualCell_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F)
    {R : Finset F} (hR : R ∈ cert.owner.residuals) :
    (cert.residualCell R).card ≤ 1332869440 := by
  calc
    (cert.residualCell R).card =
        ((Finset.univ : Finset (Fin 64)).biUnion
          (cert.scalarCell R)).card :=
      congrArg Finset.card
        (cert.biUnion_scalarCell_eq_residualCell R).symm
    _ ≤ (Finset.univ : Finset (Fin 64)).card * 20826085 :=
      FirstMatchAddBack.profileUnion_card_le_family_mul_budget
        (Finset.univ : Finset (Fin 64)) (cert.scalarCell R) 20826085
        (fun s _hs ↦ cert.fixedResidualScalarCap R hR s)
    _ = 1332869440 := by norm_num

theorem TwoBlockProjectiveRayCertificate.biUnion_residualCell_eq
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F) :
    cert.owner.residuals.biUnion cert.residualCell = cert.target := by
  ext x
  constructor
  · intro hx
    rcases Finset.mem_biUnion.mp hx with ⟨R, _hR, hxR⟩
    exact (Finset.mem_filter.mp hxR).1
  · intro hx
    exact Finset.mem_biUnion.mpr
      ⟨cert.residualSupport x, cert.residual_member x hx,
        Finset.mem_filter.mpr ⟨hx, rfl⟩⟩

/-- Complete deployed q64, `f = 28` projective-ray cap from canonical
two-block data and the explicit local Hahn cells. -/
theorem TwoBlockProjectiveRayCertificate.target_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : TwoBlockProjectiveRayCertificate α F) :
    cert.target.card ≤ 83970774720 := by
  calc
    cert.target.card =
        (cert.owner.residuals.biUnion cert.residualCell).card :=
      congrArg Finset.card cert.biUnion_residualCell_eq.symm
    _ ≤ cert.owner.residuals.card * 1332869440 :=
      FirstMatchAddBack.profileUnion_card_le_family_mul_budget
        cert.owner.residuals cert.residualCell 1332869440
        (fun R hR ↦ cert.residualCell_card_le hR)
    _ ≤ 63 * 1332869440 :=
      Nat.mul_le_mul_right 1332869440 cert.owner.residuals_card_le
    _ = 83970774720 := by norm_num

/-- PR #819's first-match payment with q64 `f = 28` supplied by canonical
two-block data.  The deployed classification, local Hahn cells, and global
cover remain fields or hypotheses. -/
theorem c0_periodic_first_match_payment_of_twoBlock_certificate
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (bad : Finset α)
    (cert28 : TwoBlockProjectiveRayCertificate α F)
    (cert29 : C0PeriodicF29ResidualOwner.F29ProjectiveRayCertificate α F)
    (cert5 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 5 14641173)
    (cert7 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128)
    (hcover : bad ⊆
      cert29.target ∪ cert28.target ∪ cert5.target ∪ cert7.target) :
    bad.card ≤ 16501904760592192 :=
  GrandeFinale.c0_periodic_first_match_payment_target
    bad cert29.target cert28.target cert5.target cert7.target hcover
    (C0PeriodicF29ResidualOwner.F29ProjectiveRayCertificate.target_card_le cert29)
    (TwoBlockProjectiveRayCertificate.target_card_le cert28)
    (C0PeriodicSingletonCertificate.q128_b5_b7_card_le
      cert5 cert7 hthree hambient)

#print axioms TwoBlockFamilyCertificate.normalized_blocks
#print axioms TwoBlockFamilyCertificate.lowBlock_degree_le
#print axioms TwoBlockFamilyCertificate.toResidualPencilCertificate
#print axioms TwoBlockFamilyCertificate.residuals_card_le
#print axioms TwoBlockProjectiveRayCertificate.target_card_le
#print axioms c0_periodic_first_match_payment_of_twoBlock_certificate

end GrandeFinale.C0PeriodicF28DerivedOwner
