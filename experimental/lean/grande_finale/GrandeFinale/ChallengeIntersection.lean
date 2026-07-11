import GrandeFinale

/-!
# Finite challenge-set intersection compiler

This module composes the exact finite translate-intersection identity with
invariance of MCA bad slopes under shearing the first received word. It gives
a challenge-restricted MCA numerator and the exact ceiling-density lower
compiler used by the target-aware lower side. No asymptotic or Reed--Solomon
estimate is assumed.
-/

open scoped BigOperators Classical

namespace GrandeFinale.ChallengeIntersection

variable {G : Type*} [AddCommGroup G] [DecidableEq G]

/-- The translate `Z + delta`, implemented as the injective image `z ↦ z + delta`. -/
def translate (Z : Finset G) (delta : G) : Finset G :=
  Z.image (fun z => z + delta)

/--
Image/preimage convention for translation: `x` lies in `Z + delta` exactly
when its inverse translate `x - delta` lies in `Z`.
-/
theorem mem_translate_iff_preimage (Z : Finset G) (delta x : G) :
    x ∈ translate Z delta ↔ x - delta ∈ Z := by
  constructor
  · intro hx
    rcases Finset.mem_image.mp hx with ⟨z, hz, rfl⟩
    simpa using hz
  · intro hx
    exact Finset.mem_image.mpr ⟨x - delta, hx, sub_add_cancel x delta⟩

/-- The overlap, written in preimage form inside `Gamma`. -/
def overlap (Z Gamma : Finset G) (delta : G) : Finset G :=
  Gamma.filter (fun x => x - delta ∈ Z)

/-- The preimage-form overlap is exactly `(Z + delta) ∩ Gamma`. -/
theorem overlap_eq_translate_inter (Z Gamma : Finset G) (delta : G) :
    overlap Z Gamma delta = translate Z delta ∩ Gamma := by
  ext x
  simp [overlap, mem_translate_iff_preimage, and_comm]

private theorem overlap_card_eq_indicator_sum
    (Z Gamma : Finset G) (delta : G) :
    (overlap Z Gamma delta).card =
      ∑ x ∈ Gamma, if x - delta ∈ Z then 1 else 0 := by
  simpa only [overlap] using
    (Finset.card_filter (fun x : G => x - delta ∈ Z) Gamma)

variable [Fintype G]

private theorem fixed_point_indicator_sum
    (Z : Finset G) (x : G) :
    (∑ delta : G, if x - delta ∈ Z then 1 else 0) = Z.card := by
  rw [← (Equiv.subLeft x).sum_comp]
  rw [Finset.sum_boole]
  simp

/--
Finite translate-intersection identity: summing over all translation parameters
counts every pair `(z, x) ∈ Z × Gamma` exactly once.
-/
theorem sum_card_translate_inter (Z Gamma : Finset G) :
    (∑ delta : G, (translate Z delta ∩ Gamma).card) = Z.card * Gamma.card := by
  simp_rw [← overlap_eq_translate_inter, overlap_card_eq_indicator_sum]
  rw [Finset.sum_comm]
  simp_rw [fixed_point_indicator_sum]
  simp [mul_comm]

omit [DecidableEq G] in
private theorem exists_ceilDiv_le (f : G → ℕ) :
    ∃ x : G, (∑ y : G, f y) ⌈/⌉ Fintype.card G ≤ f x := by
  let total : ℕ := ∑ y : G, f y
  let N : ℕ := Fintype.card G
  let q : ℕ := total ⌈/⌉ N
  have hN : 0 < N := by
    exact Fintype.card_pos
  change ∃ x : G, q ≤ f x
  by_cases hq : q = 0
  · exact ⟨0, by simp [hq]⟩
  · have hqpos : 0 < q := Nat.pos_of_ne_zero hq
    have hstrict : N * (q - 1) < total := by
      by_contra hnot
      have htotal : total ≤ N * (q - 1) := Nat.le_of_not_gt hnot
      have hqle : q ≤ q - 1 := by
        exact (ceilDiv_le_iff_le_mul hN).2 htotal
      omega
    by_contra hnot
    simp only [not_exists, not_le] at hnot
    have hsum : total ≤ N * (q - 1) := by
      calc
        total = ∑ y : G, f y := rfl
        _ ≤ ∑ _y : G, (q - 1) := by
          apply Finset.sum_le_sum
          intro y _hy
          have hy : f y < q := hnot y
          omega
        _ = N * (q - 1) := by simp [N]
    omega

/--
Some translate has overlap at least the natural ceiling of the average
`|Z| |Gamma| / |G|`, written without a rational coercion.
-/
theorem exists_card_translate_inter_ge_ceilAverage (Z Gamma : Finset G) :
    ∃ delta : G,
      (Z.card * Gamma.card + Fintype.card G - 1) / Fintype.card G ≤
        (translate Z delta ∩ Gamma).card := by
  obtain ⟨delta, hdelta⟩ := exists_ceilDiv_le
    (fun delta : G => (translate Z delta ∩ Gamma).card)
  refine ⟨delta, ?_⟩
  rw [sum_card_translate_inter] at hdelta
  simpa only [Nat.ceilDiv_eq_add_pred_div] using hdelta

/-- The largest translate-intersection cardinality. -/
def maxTranslateIntersection (Z Gamma : Finset G) : ℕ :=
  Finset.univ.sup (fun delta : G => (translate Z delta ∩ Gamma).card)

/-- The maximum translate-intersection size is at least the ceiling average. -/
theorem ceilAverage_le_maxTranslateIntersection (Z Gamma : Finset G) :
    (Z.card * Gamma.card + Fintype.card G - 1) / Fintype.card G ≤
      maxTranslateIntersection Z Gamma := by
  obtain ⟨delta, hdelta⟩ :=
    exists_card_translate_inter_ge_ceilAverage Z Gamma
  unfold maxTranslateIntersection
  exact hdelta.trans
    (Finset.le_sup (f := fun delta : G =>
      (translate Z delta ∩ Gamma).card) (Finset.mem_univ delta))

variable {F D : Type*} [Field F]

theorem explainedPair_add_smul_iff
    (C : Submodule F (D → F)) (f0 f1 : D → F) (S : Finset D) (delta : F) :
    ExplainedPair (C : Set (D → F)) (f0 + delta • f1) f1 S ↔
      ExplainedPair (C : Set (D → F)) f0 f1 S := by
  constructor
  · rintro ⟨c0, hc0, c1, hc1, h0, h1⟩
    refine ⟨c0 - delta • c1, C.sub_mem hc0 (C.smul_mem delta hc1), c1, hc1, ?_, h1⟩
    intro x hx
    have hx0 := h0 x hx
    have hx1 := h1 x hx
    change c0 x = f0 x + delta * f1 x at hx0
    change c1 x = f1 x at hx1
    change c0 x - delta * c1 x = f0 x
    rw [hx0, hx1]
    ring
  · rintro ⟨c0, hc0, c1, hc1, h0, h1⟩
    refine ⟨c0 + delta • c1, C.add_mem hc0 (C.smul_mem delta hc1), c1, hc1, ?_, h1⟩
    intro x hx
    have hx0 := h0 x hx
    have hx1 := h1 x hx
    change c0 x = f0 x at hx0
    change c1 x = f1 x at hx1
    change c0 x + delta * c1 x = f0 x + delta * f1 x
    rw [hx0, hx1]

theorem explained_shifted_combination_iff
    (C : Submodule F (D → F)) (f0 f1 : D → F) (S : Finset D)
    (delta gamma : F) :
    Explained (C : Set (D → F))
        (fun x => (f0 + delta • f1) x + gamma * f1 x) S ↔
      Explained (C : Set (D → F))
        (fun x => f0 x + (gamma + delta) * f1 x) S := by
  constructor <;> rintro ⟨c, hc, h⟩ <;> refine ⟨c, hc, ?_⟩
  · intro x hx
    calc
      c x = (f0 + delta • f1) x + gamma * f1 x := h x hx
      _ = f0 x + (gamma + delta) * f1 x := by
        change f0 x + delta * f1 x + gamma * f1 x = _
        ring
  · intro x hx
    calc
      c x = f0 x + (gamma + delta) * f1 x := h x hx
      _ = (f0 + delta • f1) x + gamma * f1 x := by
        change _ = f0 x + delta * f1 x + gamma * f1 x
        ring

theorem mcaBad_add_smul_iff
    (C : Submodule F (D → F)) (f0 f1 : D → F) (a : ℕ) (delta gamma : F) :
    MCABad (C : Set (D → F)) (f0 + delta • f1) f1 a gamma ↔
      MCABad (C : Set (D → F)) f0 f1 a (gamma + delta) := by
  constructor
  · rintro ⟨S, hcard, hexpl, hpair⟩
    refine ⟨S, hcard, (explained_shifted_combination_iff C f0 f1 S delta gamma).1 hexpl, ?_⟩
    intro horig
    exact hpair ((explainedPair_add_smul_iff C f0 f1 S delta).2 horig)
  · rintro ⟨S, hcard, hexpl, hpair⟩
    refine ⟨S, hcard, (explained_shifted_combination_iff C f0 f1 S delta gamma).2 hexpl, ?_⟩
    intro hshift
    exact hpair ((explainedPair_add_smul_iff C f0 f1 S delta).1 hshift)

variable {F D : Type*} [Field F] [Fintype F]

/-- The complete finite set of MCA-bad slopes on one received line. -/
noncomputable def mcaBadSlopes
    (C : Set (D → F)) (f0 f1 : D → F) (a : ℕ) : Finset F :=
  Finset.univ.filter (fun gamma : F => MCABad C f0 f1 a gamma)

/-- MCA-bad slopes on one line after restriction to a finite challenge set. -/
noncomputable def restrictedMCABadSlopes
    (C : Set (D → F)) (Gamma : Finset F)
    (f0 f1 : D → F) (a : ℕ) : Finset F :=
  Gamma.filter (fun gamma : F => MCABad C f0 f1 a gamma)

/--
Shearing the first received word by `-delta` turns its challenge-restricted bad
slopes into the intersection of `Gamma` with the translate by `delta` of the
original complete bad-slope set.
-/
theorem restrictedMCABadSlopes_shear_eq_translate_inter
    (C : Submodule F (D → F)) (Gamma : Finset F)
    (f0 f1 : D → F) (a : ℕ) (delta : F) :
    restrictedMCABadSlopes (C : Set (D → F)) Gamma
        (f0 + (-delta) • f1) f1 a =
      translate (mcaBadSlopes (C : Set (D → F)) f0 f1 a) delta ∩ Gamma := by
  ext gamma
  simp only [restrictedMCABadSlopes, mcaBadSlopes, Finset.mem_filter,
    Finset.mem_inter]
  rw [mcaBad_add_smul_iff]
  rw [mem_translate_iff_preimage]
  simp [sub_eq_add_neg, and_comm]

/--
There is a shear whose MCA-bad slopes inside `Gamma` attain the ceiling-average
lower bound forced by the complete bad-slope set of the original line.
-/
theorem exists_shear_restrictedMCABadSlopes_ge_ceilAverage
    (C : Submodule F (D → F)) (Gamma : Finset F)
    (f0 f1 : D → F) (a : ℕ) :
    ∃ shear : F,
      ((mcaBadSlopes (C : Set (D → F)) f0 f1 a).card * Gamma.card +
          Fintype.card F - 1) / Fintype.card F ≤
        (restrictedMCABadSlopes (C : Set (D → F)) Gamma
          (f0 + shear • f1) f1 a).card := by
  obtain ⟨delta, hdelta⟩ :=
    exists_card_translate_inter_ge_ceilAverage
      (mcaBadSlopes (C : Set (D → F)) f0 f1 a) Gamma
  refine ⟨-delta, ?_⟩
  rw [restrictedMCABadSlopes_shear_eq_translate_inter]
  exact hdelta

section ChallengeNumerator

variable [Fintype D]

/--
The challenge-restricted MCA numerator: maximize the number of bad slopes in
`Gamma` over all received lines.
-/
noncomputable def B_MCA_challenge
    (C : Set (D → F)) (a : ℕ) (Gamma : Finset F) : ℕ :=
  Finset.univ.sup (fun p : (D → F) × (D → F) =>
    (restrictedMCABadSlopes C Gamma p.1 p.2 a).card)

/-- Every explicit received line is bounded by the challenge numerator. -/
theorem restrictedMCABadSlopes_card_le_B_MCA_challenge
    (C : Set (D → F)) (Gamma : Finset F)
    (f0 f1 : D → F) (a : ℕ) :
    (restrictedMCABadSlopes C Gamma f0 f1 a).card ≤
      B_MCA_challenge C a Gamma := by
  unfold B_MCA_challenge
  exact Finset.le_sup (f := fun p : (D → F) × (D → F) =>
    (restrictedMCABadSlopes C Gamma p.1 p.2 a).card)
    (Finset.mem_univ (f0, f1))

/--
An explicit bad-slope set on one line compiles, after a shear and challenge
restriction, to the same ceiling-average lower bound for `B_MCA_challenge`.
-/
theorem ceilAverage_le_B_MCA_challenge
    (C : Submodule F (D → F)) (Gamma : Finset F)
    (f0 f1 : D → F) (a : ℕ) :
    ((mcaBadSlopes (C : Set (D → F)) f0 f1 a).card * Gamma.card +
        Fintype.card F - 1) / Fintype.card F ≤
      B_MCA_challenge (C : Set (D → F)) a Gamma := by
  obtain ⟨shear, hshear⟩ :=
    exists_shear_restrictedMCABadSlopes_ge_ceilAverage C Gamma f0 f1 a
  exact hshear.trans
    (restrictedMCABadSlopes_card_le_B_MCA_challenge
      (C : Set (D → F)) Gamma (f0 + shear • f1) f1 a)

/-- With every field element challenged, the challenge numerator is the full numerator. -/
theorem B_MCA_challenge_univ (C : Set (D → F)) (a : ℕ) :
    B_MCA_challenge C a Finset.univ = B_MCA C a := by
  simp [B_MCA_challenge, B_MCA, restrictedMCABadSlopes]

/-- Restricting slopes to a challenge set cannot increase the full MCA numerator. -/
theorem B_MCA_challenge_le_B_MCA
    (C : Set (D → F)) (a : ℕ) (Gamma : Finset F) :
    B_MCA_challenge C a Gamma ≤ B_MCA C a := by
  unfold B_MCA_challenge B_MCA
  refine Finset.sup_le fun p hp => ?_
  refine (Finset.card_le_card ?_).trans
    (Finset.le_sup
      (f := fun p : (D → F) × (D → F) =>
        (Finset.univ.filter
          (fun gamma : F => MCABad C p.1 p.2 a gamma)).card) hp)
  intro gamma hgamma
  simp only [restrictedMCABadSlopes, Finset.mem_filter] at hgamma ⊢
  exact ⟨Finset.mem_univ gamma, hgamma.2⟩

/-- The challenge numerator is bounded by the number of challenged slopes. -/
theorem B_MCA_challenge_le_card
    (C : Set (D → F)) (a : ℕ) (Gamma : Finset F) :
    B_MCA_challenge C a Gamma ≤ Gamma.card := by
  unfold B_MCA_challenge
  refine Finset.sup_le fun p _hp => ?_
  simpa only [restrictedMCABadSlopes] using
    Finset.card_le_card
      (Finset.filter_subset
        (p := fun gamma : F => MCABad C p.1 p.2 a gamma) Gamma)

/--
A lower bound for the full MCA numerator compiles to the exact ceiling-density
lower bound for every finite challenge set.
-/
theorem challenge_floor_of_full_floor
    (C : Submodule F (D → F)) (a M : ℕ) (Gamma : Finset F)
    (hM : M ≤ B_MCA (C : Set (D → F)) a) :
    (Gamma.card * M) ⌈/⌉ Fintype.card F ≤
      B_MCA_challenge (C : Set (D → F)) a Gamma := by
  let fullCount : (D → F) × (D → F) → ℕ := fun p =>
    (mcaBadSlopes (C : Set (D → F)) p.1 p.2 a).card
  have huniv :
      (Finset.univ : Finset ((D → F) × (D → F))).Nonempty :=
    Finset.univ_nonempty
  obtain ⟨p, _hp, hpmax⟩ :=
    Finset.exists_mem_eq_sup Finset.univ huniv fullCount
  have hB :
      B_MCA (C : Set (D → F)) a = fullCount p := by
    simpa [B_MCA, fullCount, mcaBadSlopes] using hpmax
  have hMline : M ≤ fullCount p := hM.trans_eq hB
  have hcardF : 0 < Fintype.card F := Fintype.card_pos
  have hceil :
      (Gamma.card * M) ⌈/⌉ Fintype.card F ≤
        (Gamma.card * fullCount p) ⌈/⌉ Fintype.card F :=
    (gc_mul_ceilDiv hcardF).monotone_l
      (Nat.mul_le_mul_left Gamma.card hMline)
  refine hceil.trans ?_
  rw [Nat.ceilDiv_eq_add_pred_div]
  simpa [fullCount, mul_comm] using
    (ceilAverage_le_B_MCA_challenge C Gamma p.1 p.2 a)

end ChallengeNumerator

end GrandeFinale.ChallengeIntersection
