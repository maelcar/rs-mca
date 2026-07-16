import GrandeFinale.C0PeriodicF29ResidualOwner

/-!
# Periodic `q = 64`, `f = 28` residual-pencil ownership

This module formalizes the finite-support projective-pencil owner in the
deployed monomial `c = 0` packet.  A certified family of `63,601`-point
residual supports lies in a polynomial pencil inside a `2,097,152`-point
nonzero ambient set.  The pencil direction is `X^32,768 U`, with
`U(0) != 0` and `deg U <= 30,833`.

Distinct pencil members can meet only in the common base locus.  That locus
has at most `30,833` deployed points, and the remaining parts are pairwise
disjoint.  Exact finite packing then gives at most 63 residual supports.

The final compiler multiplies this proved owner cap by 64 quotient-constant
classes and a supplied fixed-residual Hahn cap `20,826,085`.  The two-block
deployed factorization, pencil representation, scalar classification, local
Hahn cap, and first-match cover remain explicit certificate inputs.  No
`f <= 27`, general-modulus, or complete `c = 0` claim is made.
-/

open Polynomial
open GrandeFinale.C0PeriodicF29ResidualOwner

namespace GrandeFinale.C0PeriodicF28ResidualPencil

theorem eval_supportLocator_eq_zero_iff_mem
    {F : Type*} [Field F] [DecidableEq F]
    (S : Finset F) (z : F) :
    eval z (supportLocator S) = 0 <-> z ∈ S := by
  rw [supportLocator, eval_prod]
  simp only [eval_sub, eval_X, eval_C, Finset.prod_eq_zero_iff]
  simp only [sub_eq_zero]
  simp

/-- Nonzero scalar multiples of monic polynomials determine the same monic
representative. -/
theorem monic_eq_of_scaled_eq_scaled
    {F : Type*} [Field F]
    (A B : F[X]) (u v : F)
    (hA : A.Monic) (hB : B.Monic)
    (_hu : u ≠ 0) (hv : v ≠ 0)
    (heq : C u * A = C v * B) :
    A = B := by
  have huv : u = v := by
    have hlc := congrArg leadingCoeff heq
    simpa [hA.leadingCoeff_C_mul, hB.leadingCoeff_C_mul] using hlc
  rw [huv] at heq
  exact mul_left_cancel₀ (C_ne_zero.mpr hv) heq

/-- The deployed pencil direction `X^32,768 U`. -/
noncomputable def periodicDirection
    {F : Type*} [Field F] (U : F[X]) : F[X] :=
  monomial 32768 1 * U

theorem periodicDirection_eq_X_pow_mul
    {F : Type*} [Field F] (U : F[X]) :
    periodicDirection U = X ^ 32768 * U := by
  rw [periodicDirection, monomial_one_right_eq_X_pow]

/-- A support-level certificate for one residual projective pencil. -/
structure ResidualPencilCertificate
    (F : Type*) [Field F] [DecidableEq F] where
  ambient : Finset F
  residuals : Finset (Finset F)
  parameter : Finset F -> F
  scale : Finset F -> F
  basePolynomial : F[X]
  directionPolynomial : F[X]
  lowBlock : F[X]
  ambient_card : ambient.card = 2097152
  ambient_ne_zero : ∀ z ∈ ambient, z ≠ 0
  residual_subset : ∀ R ∈ residuals, R ⊆ ambient
  residual_card : ∀ R ∈ residuals, R.card = 63601
  scale_ne_zero : ∀ R ∈ residuals, scale R ≠ 0
  pencil_representation : ∀ R ∈ residuals,
    supportLocator R =
      C (scale R) *
        (basePolynomial + C (parameter R) * directionPolynomial)
  direction_eq : directionPolynomial = periodicDirection lowBlock
  lowBlock_natDegree : lowBlock.natDegree ≤ 30833
  lowBlock_constant_ne_zero : lowBlock.coeff 0 ≠ 0

/-- Deployed points where both generators of the pencil vanish. -/
def ResidualPencilCertificate.baseRoots
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F) : Finset F :=
  cert.ambient.filter fun z =>
    cert.basePolynomial.eval z = 0 ∧
      cert.directionPolynomial.eval z = 0

theorem ResidualPencilCertificate.pencilEquation_of_mem
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F)
    {R : Finset F} (hR : R ∈ cert.residuals)
    {z : F} (hz : z ∈ R) :
    cert.basePolynomial.eval z +
      cert.parameter R * cert.directionPolynomial.eval z = 0 := by
  have hrep := congrArg (eval z) (cert.pencil_representation R hR)
  have hloc : eval z (supportLocator R) = 0 :=
    (eval_supportLocator_eq_zero_iff_mem R z).2 hz
  rw [hloc] at hrep
  simp only [eval_mul, eval_C, eval_add] at hrep
  exact (mul_eq_zero.mp hrep.symm).resolve_left (cert.scale_ne_zero R hR)

theorem ResidualPencilCertificate.parameter_injective
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F) :
    Set.InjOn cert.parameter cert.residuals := by
  intro R hR S hS hparameter
  apply supportLocator_injective
  apply monic_eq_of_scaled_eq_scaled
    (supportLocator R) (supportLocator S) (cert.scale S) (cert.scale R)
    (supportLocator_monic R) (supportLocator_monic S)
    (cert.scale_ne_zero S hS) (cert.scale_ne_zero R hR)
  rw [cert.pencil_representation R hR,
    cert.pencil_representation S hS, hparameter]
  ring

theorem ResidualPencilCertificate.baseRoots_subset_residual
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F)
    {R : Finset F} (hR : R ∈ cert.residuals) :
    cert.baseRoots ⊆ R := by
  intro z hz
  have hzbase := Finset.mem_filter.mp hz
  apply (eval_supportLocator_eq_zero_iff_mem R z).1
  rw [cert.pencil_representation R hR]
  simp [hzbase.2.1, hzbase.2.2]

theorem ResidualPencilCertificate.baseRoots_card_le
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F) :
    cert.baseRoots.card ≤ 30833 := by
  have hlowBlock : cert.lowBlock ≠ 0 := by
    intro hzero
    apply cert.lowBlock_constant_ne_zero
    rw [hzero]
    simp
  apply (card_le_degree_of_subset_roots (p := cert.lowBlock) ?_).trans
    cert.lowBlock_natDegree
  intro z hz
  have hzbase := Finset.mem_filter.mp hz
  have hznonzero := cert.ambient_ne_zero z hzbase.1
  have hdirection := hzbase.2.2
  rw [cert.direction_eq] at hdirection
  unfold periodicDirection at hdirection
  rw [eval_mul, eval_monomial] at hdirection
  simp only [one_mul] at hdirection
  have hlow : cert.lowBlock.eval z = 0 :=
    (mul_eq_zero.mp hdirection).resolve_left (pow_ne_zero _ hznonzero)
  exact (mem_roots hlowBlock).2 hlow

theorem ResidualPencilCertificate.outsideBase_pairwiseDisjoint
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F) :
    ((cert.residuals : Set (Finset F))).PairwiseDisjoint
      (fun R => R \ cert.baseRoots) := by
  intro R hR S hS hRS
  change Disjoint (R \ cert.baseRoots) (S \ cert.baseRoots)
  rw [Finset.disjoint_left]
  intro z hzR hzS
  have hzR' := Finset.mem_sdiff.mp hzR
  have hzS' := Finset.mem_sdiff.mp hzS
  have hparameter : cert.parameter R ≠ cert.parameter S := by
    intro heq
    exact hRS (cert.parameter_injective hR hS heq)
  have heqR := cert.pencilEquation_of_mem hR hzR'.1
  have heqS := cert.pencilEquation_of_mem hS hzS'.1
  have hdirection : cert.directionPolynomial.eval z = 0 := by
    have hmul :
        (cert.parameter R - cert.parameter S) *
          cert.directionPolynomial.eval z = 0 := by
      linear_combination heqR - heqS
    exact (mul_eq_zero.mp hmul).resolve_left (sub_ne_zero.mpr hparameter)
  have hbasePolynomial : cert.basePolynomial.eval z = 0 := by
    simpa [hdirection] using heqR
  have hambient : z ∈ cert.ambient :=
    cert.residual_subset R hR hzR'.1
  have hbase : z ∈ cert.baseRoots :=
    Finset.mem_filter.mpr ⟨hambient, hbasePolynomial, hdirection⟩
  exact hzR'.2 hbase

/-- The deployed residual pencil contains at most 63 distinct residual
supports. -/
theorem ResidualPencilCertificate.residuals_card_le
    {F : Type*} [Field F] [DecidableEq F]
    (cert : ResidualPencilCertificate F) :
    cert.residuals.card ≤ 63 := by
  by_contra hcard
  have h64 : 64 ≤ cert.residuals.card := by omega
  let base := cert.baseRoots
  let outside : Finset F -> Finset F := fun R => R \ base
  have hbaseSubset : ∀ R ∈ cert.residuals, base ⊆ R := by
    intro R hR
    exact cert.baseRoots_subset_residual hR
  have houtsideCard : ∀ R ∈ cert.residuals,
      (outside R).card = 63601 - base.card := by
    intro R hR
    rw [Finset.card_sdiff,
      Finset.inter_eq_left.mpr (hbaseSubset R hR), cert.residual_card R hR]
  have houtsidePairwise :
      ((cert.residuals : Set (Finset F))).PairwiseDisjoint outside := by
    exact cert.outsideBase_pairwiseDisjoint
  have hbaseDisjoint :
      Disjoint base (cert.residuals.biUnion outside) := by
    rw [Finset.disjoint_biUnion_right]
    intro R hR
    rw [Finset.disjoint_left]
    intro z hzbase hzoutside
    exact (Finset.mem_sdiff.mp hzoutside).2 hzbase
  have hunionSubset :
      base ∪ cert.residuals.biUnion outside ⊆ cert.ambient := by
    apply Finset.union_subset
    · exact Finset.filter_subset _ _
    · apply Finset.biUnion_subset.mpr
      intro R hR
      exact Finset.sdiff_subset.trans (cert.residual_subset R hR)
  have houtsideUnionCard :
      (cert.residuals.biUnion outside).card =
        cert.residuals.card * (63601 - base.card) := by
    rw [Finset.card_biUnion houtsidePairwise]
    calc
      (∑ R ∈ cert.residuals, (outside R).card) =
          ∑ _R ∈ cert.residuals, (63601 - base.card) :=
        Finset.sum_congr rfl houtsideCard
      _ = cert.residuals.card * (63601 - base.card) := by simp
  have hpacking :
      base.card + cert.residuals.card * (63601 - base.card) ≤
        2097152 := by
    have hle := Finset.card_le_card hunionSubset
    rw [Finset.card_union_of_disjoint hbaseDisjoint,
      houtsideUnionCard, cert.ambient_card] at hle
    exact hle
  have hbaseCard : base.card ≤ 30833 := cert.baseRoots_card_le
  have hbaseCard' : base.card ≤ 63601 := by omega
  have hmul :
      64 * (63601 - base.card) ≤
        cert.residuals.card * (63601 - base.card) :=
    Nat.mul_le_mul_right (63601 - base.card) h64
  have hpacking64 :
      base.card + 64 * (63601 - base.card) ≤ 2097152 :=
    (Nat.add_le_add_left hmul base.card).trans hpacking
  omega

/-! ## Deployed `f = 28` certificate compiler -/

/-- Candidate cells over a certified residual pencil.  The fixed-residual
Hahn theorem is supplied separately for each residual support and each of the
64 quotient-constant classes. -/
structure F28ProjectiveRayCertificate
    (α F : Type*) [DecidableEq α] [Field F] [DecidableEq F] where
  target : Finset α
  owner : ResidualPencilCertificate F
  residualSupport : α -> Finset F
  scalarClass : α -> Fin 64
  residual_member : ∀ x ∈ target, residualSupport x ∈ owner.residuals
  fixedResidualScalarCap : ∀ R ∈ owner.residuals, ∀ s : Fin 64,
    (target.filter fun x =>
      residualSupport x = R ∧ scalarClass x = s).card ≤ 20826085

def F28ProjectiveRayCertificate.scalarCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F)
    (R : Finset F) (s : Fin 64) : Finset α :=
  cert.target.filter fun x =>
    cert.residualSupport x = R ∧ cert.scalarClass x = s

def F28ProjectiveRayCertificate.residualCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F)
    (R : Finset F) : Finset α :=
  cert.target.filter fun x => cert.residualSupport x = R

theorem F28ProjectiveRayCertificate.biUnion_scalarCell_eq_residualCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F) (R : Finset F) :
    (Finset.univ : Finset (Fin 64)).biUnion (cert.scalarCell R) =
      cert.residualCell R := by
  ext x
  simp [F28ProjectiveRayCertificate.scalarCell,
    F28ProjectiveRayCertificate.residualCell]

theorem F28ProjectiveRayCertificate.residualCell_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F)
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
        (fun s _hs => cert.fixedResidualScalarCap R hR s)
    _ = 1332869440 := by norm_num

theorem F28ProjectiveRayCertificate.biUnion_residualCell_eq
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F) :
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

/-- The certificate-level q64 `f = 28` projective-ray cap. -/
theorem F28ProjectiveRayCertificate.target_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F28ProjectiveRayCertificate α F) :
    cert.target.card ≤ 83970774720 := by
  calc
    cert.target.card =
        (cert.owner.residuals.biUnion cert.residualCell).card :=
      congrArg Finset.card cert.biUnion_residualCell_eq.symm
    _ ≤ cert.owner.residuals.card * 1332869440 :=
      FirstMatchAddBack.profileUnion_card_le_family_mul_budget
        cert.owner.residuals cert.residualCell 1332869440
        (fun R hR => cert.residualCell_card_le hR)
    _ ≤ 63 * 1332869440 :=
      Nat.mul_le_mul_right 1332869440 cert.owner.residuals_card_le
    _ = 83970774720 := by norm_num

/-- PR #819's first-match theorem with all three formalized component
certificate interfaces: q64 `f = 28`, q64 `f = 29`, and q128 `b = 5, 7`. -/
theorem c0_periodic_first_match_payment_of_periodic_certificates
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (bad : Finset α)
    (cert28 : F28ProjectiveRayCertificate α F)
    (cert29 : F29ProjectiveRayCertificate α F)
    (cert5 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 5 14641173)
    (cert7 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128)
    (hcover : bad ⊆
      cert29.target ∪ cert28.target ∪ cert5.target ∪ cert7.target) :
    bad.card ≤ 16501904760592192 :=
  C0PeriodicF29ResidualOwner.c0_periodic_first_match_payment_of_f29_and_singleton_certificates
    bad cert28.target cert29 cert5 cert7 hthree hambient hcover
    cert28.target_card_le

#print axioms ResidualPencilCertificate.residuals_card_le
#print axioms F28ProjectiveRayCertificate.target_card_le
#print axioms c0_periodic_first_match_payment_of_periodic_certificates

end GrandeFinale.C0PeriodicF28ResidualPencil
