import GrandeFinale.C0PeriodicSingletonCertificate

/-!
# Periodic `q = 64`, `f = 29` residual ownership

This module formalizes the residual-owner step in the deployed monomial
`c = 0` packet.  A locator is written as a residual factor times a quotient
factor evaluated at `X^B`.  Projective congruence modulo `X^a`, with `B ≤ a`,
descends to the low `B`-coefficient block.  If both residual factors are monic
of degree less than `B` and both quotient constants are nonzero, that block
forces the residual factors to be equal.

The final certificate compiler specializes to `B = 32,768`, `a = 67,472`,
and residual degree `30,833`.  It combines the proved residual ownership with
a supplied fixed-residual cap over 64 quotient-constant cells.  The deployed
locator decomposition, projective congruences, quotient-constant
classification, local Hahn cap, and projective-ray cover remain explicit
certificate inputs; no `f ≤ 28` or complete `c = 0` claim is made.
-/

open Polynomial

namespace GrandeFinale.C0PeriodicF29ResidualOwner

/-- The monic locator of a finite residual support. -/
noncomputable def supportLocator
    {F : Type*} [Field F] (S : Finset F) : F[X] :=
  ∏ x ∈ S, (X - C x)

theorem supportLocator_monic
    {F : Type*} [Field F] (S : Finset F) :
    (supportLocator S).Monic := by
  exact monic_prod_of_monic _ _ fun x _hx ↦ monic_X_sub_C x

theorem supportLocator_natDegree
    {F : Type*} [Field F] (S : Finset F) :
    (supportLocator S).natDegree = S.card := by
  rw [supportLocator, natDegree_prod_of_monic]
  · simp +decide [natDegree_sub_eq_left_of_natDegree_lt]
  · exact fun x _hx ↦ monic_X_sub_C x

theorem supportLocator_injective
    {F : Type*} [Field F] :
    Function.Injective (supportLocator (F := F)) := by
  intro S T heq
  have hroots : S.val = T.val := by
    unfold supportLocator at heq
    apply_fun roots at heq
    simpa only [roots_prod_X_sub_C] using heq
  exact Finset.val_inj.mp hroots

/-- The canonical periodic locator factorization `A(X) Q(X^B)`. -/
noncomputable def periodicLocator
    {F : Type*} [CommSemiring F]
    (B : ℕ) (A Q : F[X]) : F[X] :=
  A * Q.comp (X ^ B)

/-- Modulo `X^B`, a periodic locator is its residual factor times the constant
coefficient of the quotient factor. -/
theorem X_pow_dvd_periodicLocator_sub_constantBlock
    {F : Type*} [CommRing F]
    (B : ℕ) (A Q : F[X]) :
    X ^ B ∣ periodicLocator B A Q - C (Q.coeff 0) * A := by
  rcases (X_dvd_sub_C (p := Q)) with ⟨R, hR⟩
  have hcomp := congrArg (fun P : F[X] ↦ P.comp (X ^ B)) hR
  simp only [sub_comp, C_comp, mul_comp, X_comp] at hcomp
  refine ⟨A * R.comp (X ^ B), ?_⟩
  unfold periodicLocator
  calc
    A * Q.comp (X ^ B) - C (Q.coeff 0) * A =
        A * (Q.comp (X ^ B) - C (Q.coeff 0)) := by ring
    _ = A * ((X ^ B) * R.comp (X ^ B)) := by rw [hcomp]
    _ = (X ^ B) * (A * R.comp (X ^ B)) := by ring

/-- Projective congruence modulo `X^a` descends to congruence of the two
constant quotient blocks modulo `X^B`. -/
theorem X_pow_dvd_constantBlocks_sub_of_projective
    {F : Type*} [CommRing F]
    (B a : ℕ) (hBa : B ≤ a)
    (A₁ Q₁ A₂ Q₂ : F[X]) (c : F)
    (hprojective :
      X ^ a ∣ periodicLocator B A₁ Q₁ - C c * periodicLocator B A₂ Q₂) :
    X ^ B ∣
      C (Q₁.coeff 0) * A₁ - C (c * Q₂.coeff 0) * A₂ := by
  have hprojectiveB :
      X ^ B ∣ periodicLocator B A₁ Q₁ - C c * periodicLocator B A₂ Q₂ :=
    (pow_dvd_pow X hBa).trans hprojective
  rcases X_pow_dvd_periodicLocator_sub_constantBlock B A₁ Q₁ with ⟨R₁, hR₁⟩
  rcases X_pow_dvd_periodicLocator_sub_constantBlock B A₂ Q₂ with ⟨R₂, hR₂⟩
  rcases hprojectiveB with ⟨P, hP⟩
  refine ⟨-R₁ + P + C c * R₂, ?_⟩
  calc
    C (Q₁.coeff 0) * A₁ - C (c * Q₂.coeff 0) * A₂ =
        -(periodicLocator B A₁ Q₁ - C (Q₁.coeff 0) * A₁) +
          (periodicLocator B A₁ Q₁ - C c * periodicLocator B A₂ Q₂) +
          C c * (periodicLocator B A₂ Q₂ - C (Q₂.coeff 0) * A₂) := by
            simp only [C_mul]
            ring
    _ = -(X ^ B * R₁) + X ^ B * P + C c * (X ^ B * R₂) := by
          rw [hR₁, hP, hR₂]
    _ = X ^ B * (-R₁ + P + C c * R₂) := by ring

/-- A congruence below `X^B` between two nonzero scalar multiples of monic
degree-`<B` polynomials is an equality of the monic factors. -/
theorem monic_eq_of_X_pow_dvd_scaled_sub_scaled
    {F : Type*} [Field F]
    (B : ℕ) (A₁ A₂ : F[X]) (u v : F)
    (hA₁ : A₁.Monic) (hA₂ : A₂.Monic)
    (hdeg₁ : A₁.natDegree < B) (hdeg₂ : A₂.natDegree < B)
    (hu : u ≠ 0) (hv : v ≠ 0)
    (hdiv : X ^ B ∣ C u * A₁ - C v * A₂) :
    A₁ = A₂ := by
  have hleft : (C u * A₁).natDegree < B := by
    rw [natDegree_C_mul hu]
    exact hdeg₁
  have hright : (C v * A₂).natDegree < B := by
    rw [natDegree_C_mul hv]
    exact hdeg₂
  have hdiff : (C u * A₁ - C v * A₂).natDegree < B :=
    (natDegree_sub_le _ _).trans_lt (max_lt hleft hright)
  have hzero : C u * A₁ - C v * A₂ = 0 :=
    eq_zero_of_dvd_of_natDegree_lt hdiv (by simpa using hdiff)
  have heq : C u * A₁ = C v * A₂ := sub_eq_zero.mp hzero
  have huv : u = v := by
    have hlc := congrArg leadingCoeff heq
    simpa [hA₁.leadingCoeff_C_mul, hA₂.leadingCoeff_C_mul] using hlc
  rw [huv] at heq
  exact mul_left_cancel₀ (C_ne_zero.mpr hv) heq

/-- Exact residual ownership in one periodic projective ray. -/
theorem residual_eq_of_projective_periodicLocators
    {F : Type*} [Field F]
    (B a : ℕ) (hBa : B ≤ a)
    (A₁ Q₁ A₂ Q₂ : F[X]) (c : F)
    (hA₁ : A₁.Monic) (hA₂ : A₂.Monic)
    (hdeg₁ : A₁.natDegree < B) (hdeg₂ : A₂.natDegree < B)
    (hq₁ : Q₁.coeff 0 ≠ 0) (hq₂ : Q₂.coeff 0 ≠ 0) (hc : c ≠ 0)
    (hprojective :
      X ^ a ∣ periodicLocator B A₁ Q₁ - C c * periodicLocator B A₂ Q₂) :
    A₁ = A₂ := by
  apply monic_eq_of_X_pow_dvd_scaled_sub_scaled B A₁ A₂
    (Q₁.coeff 0) (c * Q₂.coeff 0) hA₁ hA₂ hdeg₁ hdeg₂ hq₁
    (mul_ne_zero hc hq₂)
  exact X_pow_dvd_constantBlocks_sub_of_projective
    B a hBa A₁ Q₁ A₂ Q₂ c hprojective

/-- Projective periodic locators with short residual supports have the same
residual support.  This is the support-level form of residual ownership. -/
theorem residualSupport_eq_of_projective_periodicLocators
    {F : Type*} [Field F]
    (B a : ℕ) (hBa : B ≤ a)
    (R₁ R₂ : Finset F) (Q₁ Q₂ : F[X]) (c : F)
    (hcard₁ : R₁.card < B) (hcard₂ : R₂.card < B)
    (hq₁ : Q₁.coeff 0 ≠ 0) (hq₂ : Q₂.coeff 0 ≠ 0) (hc : c ≠ 0)
    (hprojective :
      X ^ a ∣ periodicLocator B (supportLocator R₁) Q₁ -
        C c * periodicLocator B (supportLocator R₂) Q₂) :
    R₁ = R₂ := by
  apply supportLocator_injective
  apply residual_eq_of_projective_periodicLocators
    B a hBa (supportLocator R₁) Q₁ (supportLocator R₂) Q₂ c
    (supportLocator_monic R₁) (supportLocator_monic R₂)
  · rwa [supportLocator_natDegree]
  · rwa [supportLocator_natDegree]
  · exact hq₁
  · exact hq₂
  · exact hc
  · exact hprojective

/-! ## Deployed `f = 29` certificate compiler -/

/-- A certificate interface for the `q = 64`, `f = 29` part of one projective
residue ray.  The local theorem is supplied separately on every
residual-support/scalar cell; the projective data prove that all candidates
have the same residual support. -/
structure F29ProjectiveRayCertificate
    (α F : Type*) [DecidableEq α] [Field F] [DecidableEq F] where
  target : Finset α
  residualSupport : α → Finset F
  quotient : α → F[X]
  scalarClass : α → Fin 64
  scalarValue : Fin 64 → F
  residual_card : ∀ x ∈ target, (residualSupport x).card = 30833
  scalarValue_ne_zero : ∀ s, scalarValue s ≠ 0
  quotient_constant : ∀ x ∈ target,
    (quotient x).coeff 0 = scalarValue (scalarClass x)
  projective : ∀ x ∈ target, ∀ y ∈ target,
    ∃ c : F, c ≠ 0 ∧
      X ^ 67472 ∣
        periodicLocator 32768 (supportLocator (residualSupport x)) (quotient x) -
          C c * periodicLocator 32768
            (supportLocator (residualSupport y)) (quotient y)
  fixedResidualScalarCap : ∀ R : Finset F, ∀ s : Fin 64,
    (target.filter fun x ↦
      residualSupport x = R ∧ scalarClass x = s).card ≤ 25307496

/-- Every member of the certified `f = 29` ray has the same residual support. -/
theorem F29ProjectiveRayCertificate.residual_eq
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F29ProjectiveRayCertificate α F)
    {x y : α} (hx : x ∈ cert.target) (hy : y ∈ cert.target) :
    cert.residualSupport x = cert.residualSupport y := by
  rcases cert.projective x hx y hy with ⟨c, hc, hprojective⟩
  apply residualSupport_eq_of_projective_periodicLocators
    32768 67472 (by norm_num)
    (cert.residualSupport x) (cert.residualSupport y)
    (cert.quotient x) (cert.quotient y) c
  · rw [cert.residual_card x hx]
    norm_num
  · rw [cert.residual_card y hy]
    norm_num
  · rw [cert.quotient_constant x hx]
    exact cert.scalarValue_ne_zero _
  · rw [cert.quotient_constant y hy]
    exact cert.scalarValue_ne_zero _
  · exact hc
  · exact hprojective

/-- The candidates assigned to one quotient-constant class. -/
def F29ProjectiveRayCertificate.scalarCell
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F29ProjectiveRayCertificate α F) (s : Fin 64) : Finset α :=
  cert.target.filter fun x ↦ cert.scalarClass x = s

theorem F29ProjectiveRayCertificate.biUnion_scalarCell_eq
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F29ProjectiveRayCertificate α F) :
    (Finset.univ : Finset (Fin 64)).biUnion cert.scalarCell = cert.target := by
  ext x
  simp [F29ProjectiveRayCertificate.scalarCell]

/-- The certificate-level `f = 29` projective-ray cap.  Residual ownership is
used to select the relevant fixed-residual local cell before summing the 64
quotient-constant classes. -/
theorem F29ProjectiveRayCertificate.target_card_le
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    (cert : F29ProjectiveRayCertificate α F) :
    cert.target.card ≤ 1619679744 := by
  by_cases htarget : cert.target.Nonempty
  · rcases htarget with ⟨x₀, hx₀⟩
    have hresidual : ∀ x ∈ cert.target,
        cert.residualSupport x = cert.residualSupport x₀ := by
      intro x hx
      exact cert.residual_eq hx hx₀
    calc
      cert.target.card =
          ((Finset.univ : Finset (Fin 64)).biUnion cert.scalarCell).card :=
        congrArg Finset.card cert.biUnion_scalarCell_eq.symm
      _ ≤ (Finset.univ : Finset (Fin 64)).card * 25307496 :=
        FirstMatchAddBack.profileUnion_card_le_family_mul_budget
          (Finset.univ : Finset (Fin 64)) cert.scalarCell 25307496
          (fun s _hs ↦ by
            have hlocal := cert.fixedResidualScalarCap
              (cert.residualSupport x₀) s
            have hcell : cert.scalarCell s =
                cert.target.filter fun x ↦
                  cert.residualSupport x = cert.residualSupport x₀ ∧
                    cert.scalarClass x = s := by
              ext x
              simp only [F29ProjectiveRayCertificate.scalarCell,
                Finset.mem_filter]
              constructor
              · intro hx
                exact ⟨hx.1, hresidual x hx.1, hx.2⟩
              · intro hx
                exact ⟨hx.1, hx.2.2⟩
            rw [hcell]
            exact hlocal)
      _ = 1619679744 := by norm_num
  · rw [Finset.not_nonempty_iff_eq_empty.mp htarget]
    simp

/-- PR #819's first-match theorem with both the q64 `f = 29` cap and the q128
`b = 5, 7` cap replaced by their typed certificate interfaces. -/
theorem c0_periodic_first_match_payment_of_f29_and_singleton_certificates
    {α F : Type*} [DecidableEq α] [Field F] [DecidableEq F]
    {ambient : Finset F}
    (bad q64f28 : Finset α)
    (cert29 : F29ProjectiveRayCertificate α F)
    (cert5 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 5 14641173)
    (cert7 : C0PeriodicSingletonCertificate.Q128OccupancyCertificate
      α F ambient 7 10193410)
    (hthree : (3 : F) ≠ 0) (hambient : ambient.card = 128)
    (hcover : bad ⊆
      cert29.target ∪ q64f28 ∪ cert5.target ∪ cert7.target)
    (h28 : q64f28.card ≤ 83970774720) :
    bad.card ≤ 16501904760592192 :=
  C0PeriodicSingletonCertificate.c0_periodic_first_match_payment_of_singleton_certificates
    bad cert29.target q64f28 cert5 cert7 hthree hambient hcover
    cert29.target_card_le h28

#print axioms X_pow_dvd_periodicLocator_sub_constantBlock
#print axioms residual_eq_of_projective_periodicLocators
#print axioms residualSupport_eq_of_projective_periodicLocators
#print axioms F29ProjectiveRayCertificate.residual_eq
#print axioms F29ProjectiveRayCertificate.target_card_le
#print axioms c0_periodic_first_match_payment_of_f29_and_singleton_certificates

end GrandeFinale.C0PeriodicF29ResidualOwner
