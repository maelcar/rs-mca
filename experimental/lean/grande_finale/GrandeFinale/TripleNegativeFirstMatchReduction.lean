import Mathlib

/-!
# Triple-negative first-match reduction

All arithmetic is carried out in `Int`, so the three signed denominators have
their literal mathematical meanings (no truncated natural subtraction).
-/

namespace GrandeFinale
namespace TripleNegativeFirstMatchReduction

set_option autoImplicit false

/-- The fixed-slope kernel-Johnson denominator `J_K`. -/
def kernelJohnsonDenominator (N t kappa : Int) : Int :=
  (N - t) ^ 2 - N * (kappa - 1)

/-- The predecessor Hamming denominator `D_H`, with `M = N-d`. -/
def hammingDenominator (N t d : Int) : Int :=
  (N - t) ^ 2 - N * (N - d)

/-- The punctured Johnson denominator `D_J`, with
`M = N-d` and `rho = min t M`. -/
def puncturedJohnsonDenominator (N t kappa d : Int) : Int :=
  ((N - d) - min t (N - d)) ^ 2 - (N - d) * (kappa - 1)

/-- Depth below the identity profile `R=t+1`. -/
def profileDepth (R t : Int) : Int :=
  R - t - 1

/-- Beyond-half deficiency. -/
def deficiency (R t : Int) : Int :=
  2 * t - R

/-- The integral weighted-RS parameter range used by the reduction. -/
def ValidParameters (N R kappa t d : Int) : Prop :=
  N = R + kappa ∧
    0 ≤ t ∧ t < R ∧
    1 ≤ kappa ∧
    1 ≤ d ∧ d ≤ R

/-! ## Exact identities -/

theorem hamming_denominator_identity
    (N R kappa t d : Int) (hN : N = R + kappa) :
    hammingDenominator N t d =
      kernelJohnsonDenominator N t kappa - N * (R - d + 1) := by
  simp only [hammingDenominator, kernelJohnsonDenominator]
  rw [hN]
  ring

theorem punctured_denominator_high_degree_identity
    (N t kappa d : Int) (hd : N - t < d) :
    puncturedJohnsonDenominator N t kappa d =
      -(N - d) * (kappa - 1) := by
  have hMt : N - d ≤ t := by omega
  simp [puncturedJohnsonDenominator, min_eq_right hMt]
  ring

theorem punctured_denominator_low_degree_identity
    (N t kappa d : Int) (hd : d ≤ N - t) :
    (N - t) * puncturedJohnsonDenominator N t kappa d =
      ((N - t) - d) * kernelJohnsonDenominator N t kappa -
        d * t * (kappa - 1) - (N - t) * d * ((N - t) - d) := by
  have htM : t ≤ N - d := by omega
  simp only [puncturedJohnsonDenominator, kernelJohnsonDenominator,
    min_eq_left htM]
  ring

theorem punctured_denominator_low_degree_nesting_identity
    (N R kappa t d : Int) (hN : N = R + kappa) (hd : d ≤ N - t) :
    puncturedJohnsonDenominator N t kappa d =
      kernelJohnsonDenominator N t kappa -
        d * ((N - d) - deficiency R t + 1) := by
  have htM : t ≤ N - d := by omega
  simp only [puncturedJohnsonDenominator, kernelJohnsonDenominator, deficiency,
    min_eq_left htM]
  rw [hN]
  ring

theorem depth_deficiency_coordinates
    (N R kappa t : Int) (hN : N = R + kappa) :
    N = kappa + 2 * profileDepth R t + deficiency R t + 2 ∧
      N - t = kappa + profileDepth R t + 1 := by
  constructor <;> simp only [profileDepth, deficiency] <;> omega

theorem depth_deficiency_factorization
    (N R kappa t : Int) (hN : N = R + kappa) :
    kernelJohnsonDenominator N t kappa =
      (profileDepth R t + 2) ^ 2 -
        (kappa - 1) * (deficiency R t - 1) := by
  simp only [kernelJohnsonDenominator, profileDepth, deficiency]
  rw [hN]
  ring

theorem kernel_nonpositive_iff_depth_deficiency_wall
    (N R kappa t : Int) (hN : N = R + kappa) :
    kernelJohnsonDenominator N t kappa ≤ 0 ↔
      (profileDepth R t + 2) ^ 2 ≤
        (kappa - 1) * (deficiency R t - 1) := by
  rw [depth_deficiency_factorization N R kappa t hN]
  omega

/-! ## Forced parameter bounds -/

theorem kernel_nonpositive_forces_kappa_two
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0) :
    2 ≤ kappa := by
  rcases hv with ⟨hN, ht0, htR, hkappa, _hd1, _hdR⟩
  have ha : 0 < N - t := by omega
  by_contra hk
  have hkappa_one : kappa = 1 := by omega
  subst kappa
  simp only [kernelJohnsonDenominator] at hJ
  norm_num at hJ
  nlinarith

theorem kernel_nonpositive_forces_profile_bounds
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0) :
    2 ≤ kappa ∧ 2 ≤ deficiency R t := by
  have hkappa := kernel_nonpositive_forces_kappa_two hv hJ
  rcases hv with ⟨hN, _ht0, htR, _hkappa1, _hd1, _hdR⟩
  have hh : 0 ≤ profileDepth R t := by
    simp only [profileDepth]
    omega
  have hsquare : (4 : Int) ≤ (profileDepth R t + 2) ^ 2 := by
    nlinarith [sq_nonneg (profileDepth R t)]
  have hwall :=
    (kernel_nonpositive_iff_depth_deficiency_wall N R kappa t hN).mp hJ
  have hproduct : (4 : Int) ≤
      (kappa - 1) * (deficiency R t - 1) :=
    le_trans hsquare hwall
  have hw : 0 ≤ kappa - 1 := by omega
  have hdelta : 0 < deficiency R t - 1 := by
    by_contra hnot
    have hnonpos : deficiency R t - 1 ≤ 0 := le_of_not_gt hnot
    have hmul : (kappa - 1) * (deficiency R t - 1) ≤ 0 :=
      mul_nonpos_of_nonneg_of_nonpos hw hnonpos
    omega
  exact ⟨hkappa, by omega⟩

theorem kernel_nonpositive_forces_region
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0) :
    2 ≤ kappa ∧ 2 ≤ deficiency R t ∧ deficiency R t < t := by
  rcases kernel_nonpositive_forces_profile_bounds hv hJ with ⟨hkappa, hdelta⟩
  rcases hv with ⟨_hN, _ht0, htR, _hkappa1, _hd1, _hdR⟩
  refine ⟨hkappa, hdelta, ?_⟩
  simp only [deficiency]
  omega

/-! ## Sign reduction -/

theorem kernel_nonpositive_forces_hamming_negative
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0) :
    hammingDenominator N t d < 0 := by
  rcases hv with ⟨hN, ht0, htR, hkappa, _hd1, hdR⟩
  have hNpos : 0 < N := by omega
  have hgap : 0 < R - d + 1 := by omega
  have hprod : 0 < N * (R - d + 1) := mul_pos hNpos hgap
  rw [hamming_denominator_identity N R kappa t d hN]
  omega

theorem kernel_nonpositive_forces_punctured_negative_of_high_degree
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0)
    (hd : N - t < d) :
    puncturedJohnsonDenominator N t kappa d < 0 := by
  have hkappa := kernel_nonpositive_forces_kappa_two hv hJ
  rcases hv with ⟨hN, _ht0, _htR, _hkappa1, _hd1, hdR⟩
  have hM : 0 < N - d := by omega
  have hw : 0 < kappa - 1 := by omega
  have hprod : 0 < (N - d) * (kappa - 1) := mul_pos hM hw
  rw [punctured_denominator_high_degree_identity N t kappa d hd]
  nlinarith

theorem kernel_nonpositive_forces_punctured_negative_of_low_degree
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0)
    (hd : d ≤ N - t) :
    puncturedJohnsonDenominator N t kappa d < 0 := by
  have hbounds := kernel_nonpositive_forces_profile_bounds hv hJ
  rcases hbounds with ⟨hkappa, hdelta⟩
  rcases hv with ⟨hN, ht0, htR, _hkappa1, hd1, _hdR⟩
  have ha : 0 < N - t := by omega
  have hq : 0 ≤ (N - t) - d := by omega
  have ht : 0 < t := by
    simp only [deficiency] at hdelta
    omega
  have hw : 0 < kappa - 1 := by omega
  have hterm1 :
      ((N - t) - d) * kernelJohnsonDenominator N t kappa ≤ 0 :=
    mul_nonpos_of_nonneg_of_nonpos hq hJ
  have hterm2 : 0 < d * t * (kappa - 1) :=
    mul_pos (mul_pos (by omega) ht) hw
  have hterm3 : 0 ≤ (N - t) * d * ((N - t) - d) :=
    mul_nonneg (mul_nonneg (le_of_lt ha) (by omega)) hq
  have hid := punctured_denominator_low_degree_identity N t kappa d hd
  have hprod :
      (N - t) * puncturedJohnsonDenominator N t kappa d < 0 := by
    rw [hid]
    omega
  by_contra hnot
  have hD : 0 ≤ puncturedJohnsonDenominator N t kappa d :=
    le_of_not_gt hnot
  have : 0 ≤ (N - t) * puncturedJohnsonDenominator N t kappa d :=
    mul_nonneg (le_of_lt ha) hD
  omega

theorem kernel_nonpositive_forces_punctured_negative
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d)
    (hJ : kernelJohnsonDenominator N t kappa ≤ 0) :
    puncturedJohnsonDenominator N t kappa d < 0 := by
  by_cases hd : d ≤ N - t
  · exact kernel_nonpositive_forces_punctured_negative_of_low_degree hv hJ hd
  · exact kernel_nonpositive_forces_punctured_negative_of_high_degree
      hv hJ (lt_of_not_ge hd)

/-- On valid parameters, the apparent triple-negative region is exactly the
single wall `J_K ≤ 0`; in fact the two predecessor denominators are strict. -/
theorem triple_nonpositive_iff_kernel_nonpositive
    {N R kappa t d : Int}
    (hv : ValidParameters N R kappa t d) :
    (hammingDenominator N t d ≤ 0 ∧
        puncturedJohnsonDenominator N t kappa d ≤ 0 ∧
        kernelJohnsonDenominator N t kappa ≤ 0) ↔
      kernelJohnsonDenominator N t kappa ≤ 0 := by
  constructor
  · exact fun h => h.2.2
  · intro hJ
    exact ⟨
      le_of_lt (kernel_nonpositive_forces_hamming_negative hv hJ),
      le_of_lt (kernel_nonpositive_forces_punctured_negative hv hJ),
      hJ⟩

#print axioms hamming_denominator_identity
#print axioms punctured_denominator_high_degree_identity
#print axioms punctured_denominator_low_degree_identity
#print axioms depth_deficiency_factorization
#print axioms kernel_nonpositive_forces_profile_bounds
#print axioms kernel_nonpositive_forces_region
#print axioms triple_nonpositive_iff_kernel_nonpositive

end TripleNegativeFirstMatchReduction
end GrandeFinale
