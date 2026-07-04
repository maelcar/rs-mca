import Mathlib

/-!
# CAP25 v13 — Chapter: L1 list-side compilers and sunflower residuals

This file formalizes the self-contained mathematical results of the section
"L1 list-side compilers and sunflower residuals" (`\section{sec:v13-l1}`) of
`cap25_v13_experimental.tex`.

We formalize:

* `johnson_intersecting_le_one`, `johnson_intersecting_bound`
  (Theorem *κ-intersecting agreement bound*, `thm:v13-johnson-list`), the abstract
  Johnson/Cauchy–Schwarz list bound in agreement-threshold coordinates;
* `planted_lower_count` (Corollary *complete polynomial-folding planted core*,
  `cor:v13-polyfold-planted`, the general form of Theorem `thm:v13-planted`),
  proved via the explicit planted-codeword construction and a
  substitution/unique-factorization distinctness argument;
* `planted_monotone` (monotonicity step used in `prop:v13-dyadic-planted`);
* `dyadic_planted_crossing_*` (Proposition *dyadic planted crossings*,
  `prop:v13-dyadic-planted`), the exact-arithmetic crossing certificates;
* `list_unsafe` (Corollary *list unsafe test*, `cor:v13-list-unsafe`);
* `planted_budget_window` (Corollary *planted list budget windows*,
  `cor:v13-list-windows`);
* `few_petal_range` (Corollary *few-petal Johnson boundary*, `cor:v13-pma-johnson`);
* `fixed_excess_bound` (Proposition *fixed-excess full-petal compiler*,
  `prop:v13-fixed-excess`).

The concrete polynomial *sunflower layer injection* (`prop:v13-concrete-sunflower`)
and the distinct-label full-petal *charts* (`prop:v13-zero-excess-chart`,
`prop:v13-distinct-excess-chart`) are stated in the text over an explicit
polynomial sunflower decomposition; the abstract reduction `prop:v13-pma` and the
compiler `prop:v13-fixed-excess` that consume them are what we formalize here.
The open `problem` environments (`prob:v13-primitive-image-fiber`,
`prob:v13-l1-residuals`) are open problems and are not formalized as theorems.
-/

open Finset BigOperators
open scoped Classical

namespace CAP25V13.ListSide

/-! ## Agreement-threshold Johnson bounds -/

/-
**κ-intersecting agreement bound, part (i)** (`thm:v13-johnson-list`).  If a
family of listed agreement sets `A i ⊆ Ω` each of size `≥ s` has pairwise
intersections of size `≤ κ`, and `2s > |Ω| + κ`, then at most one member is
listed.
-/
theorem johnson_intersecting_le_one {σ ι : Type*} [DecidableEq σ]
    (Ω : Finset σ) (Lset : Finset ι) (A : ι → Finset σ) (s κ : ℕ)
    (hsub : ∀ i ∈ Lset, A i ⊆ Ω) (hs : ∀ i ∈ Lset, s ≤ (A i).card)
    (hint : ∀ i ∈ Lset, ∀ j ∈ Lset, i ≠ j → (A i ∩ A j).card ≤ κ)
    (hcond : Ω.card + κ < 2 * s) : Lset.card ≤ 1 := by
      by_contra h_contra; push_neg at h_contra; (
      obtain ⟨ i, hi, j, hj, hij ⟩ := Finset.one_lt_card.mp h_contra; have := Finset.card_union_add_card_inter ( A i ) ( A j ) ; simp_all +decide ;
      linarith [ hs i hi, hs j hj, ‹∀ i ∈ Lset, ∀ j ∈ Lset, ¬i = j → # ( A i ∩ A j ) ≤ κ› i hi j hj hij, show # ( A i ∪ A j ) ≤ #Ω from Finset.card_le_card ( Finset.union_subset ( hsub i hi ) ( hsub j hj ) ) ]);

/-
Linear double-count: `∑_{x∈Ω} #{i∈Lset : x∈A i} = ∑_{i∈Lset} |A i|` when each
`A i ⊆ Ω`.  Helper for `johnson_intersecting_bound`.
-/
theorem johnson_lin_count {σ ι : Type*} [DecidableEq σ]
    (Ω : Finset σ) (Lset : Finset ι) (A : ι → Finset σ)
    (hsub : ∀ i ∈ Lset, A i ⊆ Ω) :
    ∑ x ∈ Ω, (Lset.filter (fun i => x ∈ A i)).card
      = ∑ i ∈ Lset, (A i).card := by
        simp +decide only [card_eq_sum_ones, sum_filter];
        rw [ Finset.sum_comm, Finset.sum_congr rfl ];
        intro i hi; rw [ ← Finset.sum_filter ] ; congr; ext; aesop;

/-
Quadratic double-count: `∑_{x∈Ω} (#{i∈Lset : x∈A i})² = ∑_{i∈Lset} ∑_{j∈Lset} |A i ∩ A j|`
when each `A i ⊆ Ω`.  Helper for `johnson_intersecting_bound`.
-/
theorem johnson_sq_count {σ ι : Type*} [DecidableEq σ]
    (Ω : Finset σ) (Lset : Finset ι) (A : ι → Finset σ)
    (hsub : ∀ i ∈ Lset, A i ⊆ Ω) :
    ∑ x ∈ Ω, ((Lset.filter (fun i => x ∈ A i)).card) ^ 2
      = ∑ i ∈ Lset, ∑ j ∈ Lset, (A i ∩ A j).card := by
        simp +decide only [card_filter, sq];
        simp +decide only [sum_mul _ _ _];
        rw [ Finset.sum_comm, Finset.sum_congr rfl ];
        intro i hi; rw [ Finset.sum_congr rfl fun x hx => by rw [ Finset.mul_sum _ _ _ ] ] ; rw [ Finset.sum_comm ] ; simp +decide [ Finset.sum_add_distrib, Finset.sum_ite ] ;
        exact Finset.sum_congr rfl fun j hj => congr_arg Finset.card ( by ext; aesop )

/-
Real-arithmetic core of the Johnson bound.  From `L ≥ 1`, the incidence lower
bound `L·s ≤ I`, the Cauchy–Schwarz consequence `I² ≤ n0·(I + κ·L·(L-1))`, the
Johnson condition `κ·n0 < s²`, and `s ≤ n0`, deduce `L·(s²-κ·n0) ≤ n0·(s-κ)`.
-/
theorem johnson_real_core {I L s κ n0 : ℝ}
    (hL : 1 ≤ L) (hs0 : 0 ≤ s) (hκ0 : 0 ≤ κ) (hn0 : 0 ≤ n0)
    (hILs : L * s ≤ I)
    (hCS : I ^ 2 ≤ n0 * (I + κ * L * (L - 1)))
    (hcond : κ * n0 < s ^ 2) (hns : s ≤ n0) :
    L * (s ^ 2 - κ * n0) ≤ n0 * (s - κ) := by
      by_cases h_case : L * s ≤ n0;
      · nlinarith [ mul_le_mul_of_nonneg_left h_case hs0, mul_le_mul_of_nonneg_left h_case hκ0, mul_le_mul_of_nonneg_left h_case hn0, mul_le_mul_of_nonneg_left hL hs0, mul_le_mul_of_nonneg_left hL hκ0, mul_le_mul_of_nonneg_left hL hn0 ];
      · nlinarith [ mul_le_mul_of_nonneg_left hL hs0, mul_le_mul_of_nonneg_left hL hκ0, mul_le_mul_of_nonneg_left hL hn0 ]

/-
**κ-intersecting agreement bound, part (ii)** (`thm:v13-johnson-list`).  With
agreement threshold `0 < s ≤ |Ω|`, if `s² > κ·|Ω|` then the number of listed
members obeys the Johnson bound `L·(s² - κ|Ω|) ≤ |Ω|·(s - κ)` (the
cross-multiplied, division-free form).
-/
theorem johnson_intersecting_bound {σ ι : Type*} [DecidableEq σ]
    (Ω : Finset σ) (Lset : Finset ι) (A : ι → Finset σ) (s κ : ℕ)
    (hsub : ∀ i ∈ Lset, A i ⊆ Ω) (hs : ∀ i ∈ Lset, s ≤ (A i).card)
    (hint : ∀ i ∈ Lset, ∀ j ∈ Lset, i ≠ j → (A i ∩ A j).card ≤ κ)
    (hsn : s ≤ Ω.card)
    (hcond : (κ : ℝ) * Ω.card < (s : ℝ) ^ 2) :
    (Lset.card : ℝ) * ((s : ℝ) ^ 2 - κ * Ω.card)
      ≤ (Ω.card : ℝ) * ((s : ℝ) - κ) := by
        by_cases hL : Lset.card ≥ 1;
        · have hILs : (Lset.card : ℝ) * s ≤ ∑ i ∈ Lset, (A i).card := by
            exact_mod_cast le_trans ( by simp +decide [ mul_comm ] ) ( Finset.sum_le_sum hs )
          have hCS : (∑ i ∈ Lset, (A i).card : ℝ)^2 ≤ Ω.card * (∑ i ∈ Lset, (A i).card + κ * Lset.card * (Lset.card - 1)) := by
            have hCS : (∑ x ∈ Ω, ((Lset.filter (fun i => x ∈ A i)).card : ℝ)^2) ≤ (∑ i ∈ Lset, (A i).card : ℝ) + κ * Lset.card * (Lset.card - 1) := by
              have hCS : (∑ x ∈ Ω, ((Lset.filter (fun i => x ∈ A i)).card : ℝ)^2) = (∑ i ∈ Lset, ∑ j ∈ Lset, (A i ∩ A j).card : ℝ) := by
                exact_mod_cast johnson_sq_count Ω Lset A hsub;
              have hCS : (∑ i ∈ Lset, ∑ j ∈ Lset, (A i ∩ A j).card : ℝ) ≤ (∑ i ∈ Lset, (A i).card : ℝ) + κ * Lset.card * (Lset.card - 1) := by
                have hCS : ∀ i ∈ Lset, (∑ j ∈ Lset, (A i ∩ A j).card : ℝ) ≤ (A i).card + κ * (Lset.card - 1) := by
                  intro i hi; rw [ Finset.sum_eq_add_sum_diff_singleton hi ] ; norm_cast; simp +decide [ mul_comm ] ;
                  exact le_trans ( Finset.sum_le_sum fun j hj => ‹∀ i ∈ Lset, ∀ j ∈ Lset, i ≠ j → # ( A i ∩ A j ) ≤ κ› i hi j ( Finset.mem_sdiff.mp hj |>.1 ) ( by aesop ) ) ( by simp +decide [ mul_comm, Finset.card_sdiff, * ] )
                convert Finset.sum_le_sum hCS using 1 ; simp +decide [ Finset.sum_add_distrib, mul_assoc, mul_comm, mul_left_comm, Finset.mul_sum _ _ _ ];
              linarith;
            have hCS : (∑ x ∈ Ω, ((Lset.filter (fun i => x ∈ A i)).card : ℝ))^2 ≤ Ω.card * (∑ x ∈ Ω, ((Lset.filter (fun i => x ∈ A i)).card : ℝ)^2) := by
              exact sq_sum_le_card_mul_sum_sq;
            convert hCS.trans ( mul_le_mul_of_nonneg_left ‹_› <| Nat.cast_nonneg _ ) using 1;
            · rw_mod_cast [ johnson_lin_count Ω Lset A hsub ];
            · norm_cast;
          have := johnson_real_core ( show 1 ≤ ( Lset.card : ℝ ) by norm_cast ) ( show 0 ≤ ( s : ℝ ) by positivity ) ( show 0 ≤ ( κ : ℝ ) by positivity ) ( show 0 ≤ ( Ω.card : ℝ ) by positivity ) hILs ( by simpa using hCS ) hcond ( by norm_cast ) ; linarith;
        · simp_all +decide [ Finset.notMem_empty ];
          norm_cast at *;
          rw [ Int.subNatNat_eq_coe ] ; nlinarith

/-! ## Planted quotient-core lower counts -/

open Polynomial in
/-- **Complete polynomial-folding planted core** (`cor:v13-polyfold-planted`; the
general form of the planted quotient-core lower count `thm:v13-planted`).  If a
degree-`M` polynomial `φ` maps a finite set `H` onto `Q` with every fibre of size
exactly `M`, and `M ∣ k`, `1 ≤ σ < M`, `k/M ≤ |Q|-1`, then some received word `U`
has at least `C(|Q|-1, k/M)` distinct degree-`< k` codewords agreeing with `U`
on at least `k + σ` positions. -/
theorem planted_lower_count {F : Type*} [Field F]
    (H Q : Finset F) (φ : Polynomial F) (M k σ : ℕ)
    (hMdeg : φ.natDegree = M) (hM0 : 0 < M)
    (honto : ∀ b ∈ Q, (H.filter (fun x => φ.eval x = b)).card = M)
    (hcover : ∀ x ∈ H, φ.eval x ∈ Q)
    (hQ : 1 ≤ Q.card)
    (hMk : M ∣ k) (hσ1 : 1 ≤ σ) (hσM : σ < M) (hkQ : k / M ≤ Q.card - 1) :
    ∃ (U : F → F) (S : Finset (Polynomial F)),
      (∀ P ∈ S, P.degree < (k : WithBot ℕ)) ∧
      (∀ P ∈ S, k + σ ≤ (H.filter (fun x => U x = P.eval x)).card) ∧
      Nat.choose (Q.card - 1) (k / M) ≤ S.card := by
  obtain ⟨ℓ, rfl⟩ : ∃ ℓ, k = M * ℓ := hMk
  have hℓ : M * ℓ / M = ℓ := Nat.mul_div_cancel_left _ hM0
  obtain ⟨b0, hb0Q⟩ := Finset.card_pos.mp (by omega : 0 < Q.card)
  obtain ⟨T, hTsub, hTcard⟩ : ∃ T ⊆ H.filter (fun x => φ.eval x = b0), T.card = σ :=
    Finset.exists_subset_card_eq (by rw [honto b0 hb0Q]; omega)
  have hφne : φ ≠ 0 := fun h => by rw [h] at hMdeg; simp at hMdeg; omega
  set ET : Polynomial F := ∏ t ∈ T, (X - C t) with hET
  have hETne : ET ≠ 0 := Finset.prod_ne_zero_iff.mpr (fun t _ => X_sub_C_ne_zero t)
  have hETdeg : ET.natDegree = σ := by
    rw [hET, Polynomial.natDegree_prod _ _ (fun t _ => X_sub_C_ne_zero t)]; simp [hTcard]
  have hprodcomp : ∀ A : Finset F, (∏ b ∈ A, (φ - C b)) = (∏ b ∈ A, (X - C b)).comp φ := by
    intro A; rw [Polynomial.prod_comp]; simp
  have hcompinj : ∀ p q : F[X], p.comp φ = q.comp φ → p = q := by
    intro p q hpq
    have h0 : (p - q).comp φ = 0 := by rw [Polynomial.sub_comp, hpq, sub_self]
    rcases Polynomial.comp_eq_zero_iff.mp h0 with h | ⟨_, h2⟩
    · exact sub_eq_zero.mp h
    · exfalso; rw [h2] at hMdeg; simp at hMdeg; omega
  set Pw : Finset F → Polynomial F :=
    fun A => ET * φ ^ ℓ - ET * (∏ b ∈ A, (φ - C b)) with hPw
  have hPwcomp : ∀ A : Finset F, Pw A = ET * (-(((∏ b ∈ A, (X - C b)) - X ^ ℓ).comp φ)) := by
    intro A; simp only [hPw]; rw [hprodcomp A, Polynomial.sub_comp, Polynomial.X_pow_comp]; ring
  refine ⟨fun x => eval x (ET * φ ^ ℓ),
    (Finset.powersetCard ℓ (Q.erase b0)).image Pw, ?_, ?_, ?_⟩
  · intro P hP
    rw [Finset.mem_image] at hP; obtain ⟨A, hAmem, rfl⟩ := hP
    rw [Finset.mem_powersetCard] at hAmem; obtain ⟨hAsub, hAc⟩ := hAmem
    set D : F[X] := (∏ b ∈ A, (X - C b)) - X ^ ℓ with hD
    by_cases hDz : D = 0
    · rw [hPwcomp A, ← hD, hDz]
      simp only [Polynomial.zero_comp, neg_zero, mul_zero, Polynomial.degree_zero]
      exact WithBot.bot_lt_coe _
    · have hmon : (∏ b ∈ A, (X - C b)).Monic := monic_prod_of_monic _ _ (fun b _ => monic_X_sub_C b)
      have h1 : (∏ b ∈ A, (X - C b)).natDegree = ℓ := by
        rw [Polynomial.natDegree_prod _ _ (fun b _ => X_sub_C_ne_zero b)]; simp [hAc]
      have hDdeg : D.degree < (ℓ : WithBot ℕ) := by
        rw [hD]
        have hpne : (∏ b ∈ A, (X - C b)) ≠ 0 := hmon.ne_zero
        have := Polynomial.degree_sub_lt (p := ∏ b ∈ A, (X - C b)) (q := X ^ ℓ)
          (by rw [Polynomial.degree_eq_natDegree hpne, h1, Polynomial.degree_X_pow]) hpne
          (by rw [hmon.leadingCoeff, (Polynomial.monic_X_pow ℓ).leadingCoeff])
        rwa [Polynomial.degree_eq_natDegree hpne, h1] at this
      have hDnat : D.natDegree < ℓ := (Polynomial.natDegree_lt_iff_degree_lt hDz).mpr hDdeg
      have hℓpos : 0 < ℓ := by omega
      rw [hPwcomp A, ← hD]
      apply lt_of_le_of_lt (Polynomial.degree_mul_le _ _)
      rw [Polynomial.degree_neg, Polynomial.degree_eq_natDegree hETne,
        Polynomial.degree_eq_natDegree (by simpa using fun hc => hDz (by
          rcases (Polynomial.comp_eq_zero_iff.mp hc) with h | ⟨_, h2⟩
          · exact h
          · exfalso; rw [h2] at hMdeg; simp at hMdeg; omega)),
        Polynomial.natDegree_comp, hETdeg, hMdeg]
      have hlt : (σ : ℕ) + D.natDegree * M < M * ℓ := by nlinarith [hDnat, hσM, hℓpos]
      exact_mod_cast hlt
  · intro P hP
    rw [Finset.mem_image] at hP; obtain ⟨A, hAmem, rfl⟩ := hP
    rw [Finset.mem_powersetCard] at hAmem; obtain ⟨hAsub, hAc⟩ := hAmem
    have hdisj : Disjoint T (A.biUnion (fun b => H.filter (fun x => φ.eval x = b))) := by
      rw [Finset.disjoint_left]; intro x hxT hxB
      rw [Finset.mem_biUnion] at hxB; obtain ⟨b, hbA, hxb⟩ := hxB
      rw [Finset.mem_filter] at hxb
      have hxT' := hTsub hxT; rw [Finset.mem_filter] at hxT'
      exact (Finset.mem_erase.mp (hAsub hbA)).1 (by rw [← hxb.2, hxT'.2])
    have hbcard : (A.biUnion (fun b => H.filter (fun x => φ.eval x = b))).card = M * ℓ := by
      rw [Finset.card_biUnion (fun b _ b' _ hbb' => Finset.disjoint_left.mpr (fun x hx hx' => by
        simp only [Finset.mem_filter] at hx hx'; exact hbb' (hx.2 ▸ hx'.2 ▸ rfl)))]
      rw [Finset.sum_congr rfl (fun b hb => honto b (Finset.mem_of_mem_erase (hAsub hb))),
        Finset.sum_const, hAc, smul_eq_mul, mul_comm]
    have hsubset : T ∪ A.biUnion (fun b => H.filter (fun x => φ.eval x = b))
        ⊆ H.filter (fun x => eval x (ET * φ ^ ℓ) = (Pw A).eval x) := by
      intro x hx
      have hzero : eval x (ET * ∏ b ∈ A, (φ - C b)) = 0 ∧ x ∈ H := by
        rw [Finset.mem_union] at hx
        rcases hx with hxT | hxB
        · have hxT' := hTsub hxT; rw [Finset.mem_filter] at hxT'
          have hE0 : eval x ET = 0 := by
            rw [hET, Polynomial.eval_prod]; exact Finset.prod_eq_zero hxT (by simp)
          exact ⟨by rw [Polynomial.eval_mul, hE0, zero_mul], hxT'.1⟩
        · rw [Finset.mem_biUnion] at hxB; obtain ⟨b, hbA, hxb⟩ := hxB
          rw [Finset.mem_filter] at hxb
          have hP0 : eval x (∏ b ∈ A, (φ - C b)) = 0 := by
            rw [Polynomial.eval_prod]; exact Finset.prod_eq_zero hbA (by simp [hxb.2])
          exact ⟨by rw [Polynomial.eval_mul, hP0, mul_zero], hxb.1⟩
      rw [Finset.mem_filter]
      refine ⟨hzero.2, ?_⟩
      simp only [hPw, Polynomial.eval_sub, hzero.1, sub_zero]
    calc M * ℓ + σ = (T ∪ A.biUnion (fun b => H.filter (fun x => φ.eval x = b))).card := by
          rw [Finset.card_union_of_disjoint hdisj, hTcard, hbcard]; ring
      _ ≤ _ := Finset.card_le_card hsubset
  · rw [hℓ]
    rw [Finset.card_image_of_injOn, Finset.card_powersetCard, Finset.card_erase_of_mem hb0Q]
    intro A₁ hA₁ A₂ hA₂ heq
    simp only [hPw] at heq
    rw [sub_right_inj] at heq
    have hp : (∏ b ∈ A₁, (φ - C b)) = (∏ b ∈ A₂, (φ - C b)) := mul_left_cancel₀ hETne heq
    rw [hprodcomp A₁, hprodcomp A₂] at hp
    have hpp := hcompinj _ _ hp
    have hr := congrArg Polynomial.roots hpp
    rw [Polynomial.roots_prod_X_sub_C, Polynomial.roots_prod_X_sub_C] at hr
    exact Finset.val_injective hr

/-
**Dyadic planted monotonicity** (the injection step in `prop:v13-dyadic-planted`).
Adjoining a fixed `m`-element set to an `m`-subset of `{1,…,N-1}` injects into the
`2m`-subsets of `{1,…,2N-1}`, so `C(N-1, m) ≤ C(2N-1, 2m)`.
-/
theorem planted_monotone (N m : ℕ) (h : m ≤ N) :
    Nat.choose (N - 1) m ≤ Nat.choose (2 * N - 1) (2 * m) := by
      rcases N with ( _ | N ) <;> rcases m with ( _ | m ) <;> simp_all +arith +decide [ Nat.choose_eq_zero_of_lt ];
      induction' N with N ih generalizing m <;> simp_all +arith +decide [ Nat.choose_succ_succ, Nat.mul_succ ];
      rcases h with ( _ | h ) <;> simp_all +arith +decide [ Nat.choose_succ_succ, add_mul ];
      · simp +arith +decide [ Nat.choose_eq_zero_of_lt ];
      · rcases m with ( _ | m ) <;> simp_all +arith +decide [ Nat.choose_succ_succ, add_mul ];
        grind

/-- **Dyadic planted crossing** (`prop:v13-dyadic-planted`), rate `ρ = 1/2`: the
planted count `C(N-1, ρN)` first exceeds `2¹²⁸-1` at dyadic order `N = 256`, with
predecessor `N = 128` still within budget. -/
theorem dyadic_planted_crossing_half :
    2 ^ 128 - 1 < Nat.choose 255 128 ∧ Nat.choose 127 64 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `prop:v13-dyadic-planted`, rate `ρ = 1/4`: first crossing at `N = 256`,
predecessor `N = 128`. -/
theorem dyadic_planted_crossing_quarter :
    2 ^ 128 - 1 < Nat.choose 255 64 ∧ Nat.choose 127 32 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `prop:v13-dyadic-planted`, rate `ρ = 1/8`: first crossing at `N = 256`,
predecessor `N = 128`. -/
theorem dyadic_planted_crossing_eighth :
    2 ^ 128 - 1 < Nat.choose 255 32 ∧ Nat.choose 127 16 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `prop:v13-dyadic-planted`, rate `ρ = 1/16`: first crossing at `N = 512`,
predecessor `N = 256`. -/
theorem dyadic_planted_crossing_sixteenth :
    2 ^ 128 - 1 < Nat.choose 511 32 ∧ Nat.choose 255 16 ≤ 2 ^ 128 - 1 := by
  native_decide

/-
**List unsafe test** (`cor:v13-list-unsafe`).  If a certified planted count
exceeds the allowed numerator `⌊q/2¹²⁸⌋`, the normalized list quantity
`count/q` exceeds the target `2⁻¹²⁸`.
-/
theorem list_unsafe {count q : ℕ} (hq : 0 < q) (h : q / 2 ^ 128 < count) :
    (2 : ℝ) ^ (-128 : ℤ) < (count : ℝ) / q := by
      rw [ lt_div_iff₀ ] <;> norm_num <;> norm_cast;
      rw [ div_mul_eq_mul_div, div_lt_iff₀ ] <;> norm_cast;
      grind

/-
**Planted list budget window** (`cor:v13-list-windows`).  With a planted exact
count `P` and certified lower count `L ≤ P`, the unresolved list denominators are
exactly `L·2¹²⁸ ≤ q ≤ P·2¹²⁸ - 1`.
-/
theorem planted_budget_window (L P q : ℕ) (hP : 1 ≤ P) :
    (L ≤ q / 2 ^ 128 ∧ q / 2 ^ 128 < P) ↔
      (L * 2 ^ 128 ≤ q ∧ q ≤ P * 2 ^ 128 - 1) := by
        bv_omega

/-! ## Sunflower and petal interfaces -/

/-
**Few-petal Johnson-covered range** (`cor:v13-pma-johnson`).  With auxiliary
petal domain of size `M(σ+1)`, degree cap `d`, and agreement `a`, the strict
Johnson condition `a² > M(σ+1)d` is equivalent to the floor range
`M ≤ ⌊(a²-1)/(d(σ+1))⌋`.
-/
theorem few_petal_range {a d σ M : ℕ} (hd : 0 < d) :
    M * (d * (σ + 1)) ≤ a ^ 2 - 1 ↔ M ≤ (a ^ 2 - 1) / (d * (σ + 1)) := by
      rw [ Nat.le_div_iff_mul_le ( by positivity ) ]

/-
**Fixed-excess full-petal compiler** (`prop:v13-fixed-excess`).  If the
zero-excess layer is bounded by `C(M,2)·q` and each `e`-excess layer
(`1 ≤ e ≤ E`) by `2^M·q^{e+1}`, then a full-petal atlas has total size at most
`C(M,2)·q + 2^M·∑_{e=1}^{E} q^{e+1}`.
-/
theorem fixed_excess_bound (M E q : ℕ) (layer0 : ℕ) (layer : ℕ → ℕ)
    (h0 : layer0 ≤ Nat.choose M 2 * q)
    (he : ∀ e ∈ Finset.Icc 1 E, layer e ≤ 2 ^ M * q ^ (e + 1)) :
    layer0 + ∑ e ∈ Finset.Icc 1 E, layer e
      ≤ Nat.choose M 2 * q + 2 ^ M * ∑ e ∈ Finset.Icc 1 E, q ^ (e + 1) := by
        simpa only [ Finset.mul_sum _ _ _ ] using add_le_add h0 ( Finset.sum_le_sum he )

end CAP25V13.ListSide
