import Mathlib

/-!
# CAP25 v13 — Chapter: M1 residue-line tools and Conjecture-F reductions

This file formalizes the self-contained mathematical results of the section
"M1 residue-line tools and Conjecture-F reductions" (`\section{sec:v13-m1}`) of
`cap25_v13_experimental.tex`.

We formalize:

* `gap2_seam` (Lemma *GAP-2 quotient seam*, `lem:v13-gap2`);
* `substitution_pow_injective` (the substitution injectivity used by the
  *quotient-pullback recursion* `lem:v13-quot-pullback`, and by the planted core);
* `dim_one_voting` (Lemma *dimension-one voting*, `lem:v13-dim1`), abstract form;
* `finrank_inf_ker_ge`, `finrank_vanishing_ge`, `greedy_exists`, `vanishing_eq_span`
  (the codimension / greedy-selection lemmas underlying the Conjecture-F bound);
* `conjF_fixed_dim` (Theorem *fixed-dimensional Conjecture-F bound*,
  `thm:v13-fixeddim`), proved in full;
* `hankel_det` (Proposition *Hankel factorization*, `prop:v13-hankel`),
  determinant identity;
* `anticode_packing` (Proposition *anticode packing*, `prop:v13-anticode`);
* `johnson_ball_count` (the Johnson-ball size `D_t(n,j)` of Corollary
  *dependency-degree concentration*, `cor:v13-dependency`).

The split-locator *moment calculus* (`thm:v13-first-moment`, `thm:v13-joint-rank`,
`thm:v13-second-moment`, `cor:v13-exact-variance`, `cor:v13-dependency`) is an
average over a random-word probability space and the *Johnson exchange mixing*
proposition (`prop:v13-johnson-exchange`) is a spectral statement about the Johnson
association scheme; these require probability / association-scheme frameworks beyond
the self-contained algebraic-combinatorial scope reproduced here, and the
combinatorial ingredient `D_t(n,j)` of the concentration corollary is formalized as
`johnson_ball_count`.  The SPI *deficiency-one eliminant* (`thm:v13-spi`) is a
pseudo-division statement over `F[Z]` and is likewise not reproduced.  The
*common-GCD reduction* (`lem:v13-gcd`) and *hyperplane concurrency*
(`lem:v13-concurrency`) are projective-geometry restatements whose algebraic core
is the substitution/vanishing arguments captured by the results above.
-/

open Finset BigOperators Matrix
open scoped Classical

namespace CAP25V13.ResidueLine

/-! ## Quotient seam arithmetic -/

/-
**GAP-2 quotient seam** (`lem:v13-gap2`).  If `M ∣ n` and `M ∣ k`, then
`M ∣ r = n - k`; and since `j + t = r`, one has `M ∣ j ↔ M ∣ t`.
-/
theorem gap2_seam {n k M j t : ℕ} (hMn : M ∣ n) (hMk : M ∣ k)
    (hjt : j + t = n - k) : M ∣ (n - k) ∧ (M ∣ j ↔ M ∣ t) := by
      exact ⟨ Nat.dvd_sub ‹_› ‹_›, ⟨ fun h => by convert Nat.dvd_sub ( dvd_trans ( by simpa ) ( Nat.dvd_sub ‹M ∣ n› ‹M ∣ k› ) ) h using 1; omega, fun h => by convert Nat.dvd_sub ( dvd_trans ( by simpa ) ( Nat.dvd_sub ‹M ∣ n› ‹M ∣ k› ) ) h using 1; omega ⟩ ⟩

/-
**Substitution injectivity** (core of the *quotient-pullback recursion*
`lem:v13-quot-pullback`, and of the planted-core distinctness argument).  Over an
integral domain, `g ↦ g(X^M)` is injective when `M > 0`.
-/
theorem substitution_pow_injective {K : Type*} [CommRing K] [IsDomain K]
    {M : ℕ} (hM : 0 < M) :
    Function.Injective
      (fun g : Polynomial K => g.comp (Polynomial.X ^ M)) := by
        intro f g hfg
        have h_eq : (f - g).comp (Polynomial.X ^ M) = 0 := by
          simp_all +decide [ sub_eq_zero ];
        rw [ Polynomial.comp_eq_zero_iff ] at h_eq;
        cases M <;> simp_all +decide [ sub_eq_zero ]

/-! ## Conjecture-F reductions -/

/-
**Dimension-one voting** (`lem:v13-dim1`), abstract counting form.  If every
point `h ∈ H` casts exactly one vote `vote h`, and each locator point `p ∈ 𝒫`
receives votes from a `≥ j`-element subset `root p ⊆ H` of points, then
`|𝒫| ≤ ⌊|H|/j⌋`.
-/
theorem dim_one_voting {ι σ : Type*} [DecidableEq σ] (H : Finset σ) (Pts : Finset ι)
    (vote : σ → ι) (root : ι → Finset σ) (j : ℕ) (hj : 0 < j)
    (hroot : ∀ p ∈ Pts, root p ⊆ H ∧ j ≤ (root p).card)
    (hvote : ∀ p ∈ Pts, ∀ h ∈ root p, vote h = p) :
    Pts.card ≤ H.card / j := by
      have h_sum : ∑ p ∈ Pts, (root p).card ≤ H.card := by
        rw [ ← Finset.card_biUnion ];
        · exact Finset.card_le_card ( Finset.biUnion_subset.mpr fun p hp => hroot p hp |>.1 );
        · exact fun p hp q hq hpq => Finset.disjoint_left.mpr fun x hx hx' => hpq <| by have := hvote p hp x hx; have := hvote q hq x hx'; aesop;
      exact Nat.le_div_iff_mul_le hj |>.2 ( by simpa [ mul_comm ] using h_sum.trans' ( Finset.sum_le_sum fun p hp => hroot p hp |>.2 ) )

/-- Intersecting a finite-dimensional subspace with the kernel of a linear
functional drops the finrank by at most one. -/
theorem finrank_inf_ker_ge {K V : Type*} [Field K] [AddCommGroup V] [Module K V]
    (W : Submodule K V) [FiniteDimensional K W] (f : V →ₗ[K] K) :
    Module.finrank K W - 1 ≤ Module.finrank K ↑(W ⊓ LinearMap.ker f) := by
      set g : W →ₗ[K] K := f.comp (Submodule.subtype W)
      have h1 : Module.finrank K (LinearMap.range g) ≤ 1 :=
        le_trans (Submodule.finrank_le _) (by simp)
      have h2 : Module.finrank K (LinearMap.ker g)
          = Module.finrank K W - Module.finrank K (LinearMap.range g) :=
        eq_tsub_of_add_eq (by linarith [LinearMap.finrank_range_add_finrank_ker g])
      rw [show W ⊓ f.ker = Submodule.map W.subtype (LinearMap.ker g) from by aesop]
      rw [Submodule.finrank_map_subtype_eq]
      exact h2.symm ▸ Nat.sub_le_sub_left h1 _

/-- The subspace of `W` of polynomials vanishing on a finite set `A` has finrank
at least `finrank W - |A|`. -/
theorem finrank_vanishing_ge {K : Type*} [Field K] (W : Submodule K (Polynomial K))
    [FiniteDimensional K W] (A : Finset K) :
    Module.finrank K W - A.card
      ≤ Module.finrank K ↑(W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h)) := by
  induction A using Finset.induction with
  | empty =>
    have h0 : (⨅ h ∈ (∅ : Finset K), LinearMap.ker (Polynomial.leval h)) = ⊤ := by simp
    rw [h0, inf_top_eq]; simp
  | @insert a A ha ih =>
    have hins : (⨅ h ∈ insert a A, LinearMap.ker (Polynomial.leval h))
        = LinearMap.ker (Polynomial.leval a) ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h) := by
      simp [iInf_or, iInf_inf_eq]
    have hfd : FiniteDimensional K ↥(W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h)) :=
      Submodule.finiteDimensional_inf_left W _
    have key := finrank_inf_ker_ge (W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h))
      (Polynomial.leval a)
    rw [hins]
    rw [show W ⊓ (LinearMap.ker (Polynomial.leval a) ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h))
        = (W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h)) ⊓ LinearMap.ker (Polynomial.leval a) from by
      rw [inf_comm (LinearMap.ker (Polynomial.leval a)), ← inf_assoc]]
    rw [Finset.card_insert_of_notMem ha]
    omega

/-- **Greedy codimension selection.**  For each finite set `A`, there is a subset
`A₀ ⊆ A` cutting out the *same* vanishing subspace as `A`, of size exactly
`(d+1) - finrank` of that subspace.  Proved by strong induction, removing a point
that does not drop the finrank and otherwise peeling off one that drops it by one
(via `finrank_inf_ker_ge`). -/
theorem greedy_exists {K : Type*} [Field K] (W : Submodule K (Polynomial K))
    [FiniteDimensional K W] (d : ℕ) (hdim : Module.finrank K W = d + 1) :
    ∀ (A : Finset K), ∃ A₀ ⊆ A,
      (W ⊓ ⨅ h ∈ A₀, LinearMap.ker (Polynomial.leval h))
        = (W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h)) ∧
      A₀.card = (d + 1) - Module.finrank K ↑(W ⊓ ⨅ h ∈ A, LinearMap.ker (Polynomial.leval h)) := by
  intro A
  induction A using Finset.strongInductionOn with
  | _ A IH =>
    by_cases hstep : ∃ h ∈ A,
        (W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h'))
          ≠ (W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
    · obtain ⟨h, hhA, hne⟩ := hstep
      have hins : (⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
          = LinearMap.ker (Polynomial.leval h) ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h') := by
        conv_lhs => rw [← Finset.insert_erase hhA]
        simp [iInf_or, iInf_inf_eq]
      have hVA : (W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
          = (W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) ⊓ LinearMap.ker (Polynomial.leval h) := by
        rw [hins, inf_comm (LinearMap.ker (Polynomial.leval h)), ← inf_assoc]
      haveI hfdE : FiniteDimensional K ↥(W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) :=
        Submodule.finiteDimensional_inf_left W _
      have hle : (W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
          ≤ (W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) := by
        rw [hVA]; exact inf_le_left
      have hlt : (W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
          < (W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) :=
        lt_of_le_of_ne hle (fun hh => hne hh.symm)
      have hfinlt : Module.finrank K ↥(W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h'))
          < Module.finrank K ↥(W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) :=
        Submodule.finrank_lt_finrank_of_lt hlt
      have hge2 : Module.finrank K ↥(W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) - 1
          ≤ Module.finrank K ↥(W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h')) := by
        conv_rhs => rw [hVA]
        exact finrank_inf_ker_ge (W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h'))
          (Polynomial.leval h)
      have hfr : Module.finrank K ↥(W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h'))
          = Module.finrank K ↥(W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h')) + 1 :=
        le_antisymm (Nat.sub_le_iff_le_add.mp hge2) hfinlt
      have hAd : Module.finrank K ↥(W ⊓ ⨅ h' ∈ A, LinearMap.ker (Polynomial.leval h')) ≤ d := by
        have hEmono : Module.finrank K ↥(W ⊓ ⨅ h' ∈ A.erase h, LinearMap.ker (Polynomial.leval h')) ≤ d + 1 := by
          rw [← hdim]; exact Submodule.finrank_mono inf_le_left
        omega
      obtain ⟨A₀, hsub, hV, hcard⟩ := IH (A.erase h) (Finset.erase_ssubset hhA)
      have hhA0 : h ∉ A₀ := fun hmem => (Finset.mem_erase.mp (hsub hmem)).1 rfl
      refine ⟨insert h A₀, ?_, ?_, ?_⟩
      · exact Finset.insert_subset hhA (hsub.trans (Finset.erase_subset _ _))
      · have hinsA0 : (⨅ h' ∈ insert h A₀, LinearMap.ker (Polynomial.leval h'))
            = LinearMap.ker (Polynomial.leval h) ⊓ ⨅ h' ∈ A₀, LinearMap.ker (Polynomial.leval h') := by
          simp [iInf_or, iInf_inf_eq]
        rw [show (W ⊓ ⨅ h' ∈ insert h A₀, LinearMap.ker (Polynomial.leval h'))
            = (W ⊓ ⨅ h' ∈ A₀, LinearMap.ker (Polynomial.leval h')) ⊓ LinearMap.ker (Polynomial.leval h) from by
          rw [hinsA0, inf_comm (LinearMap.ker (Polynomial.leval h)), ← inf_assoc]]
        rw [hV, ← hVA]
      · rw [Finset.card_insert_of_notMem hhA0, hcard, hfr]; omega
    · push_neg at hstep
      rcases A.eq_empty_or_nonempty with rfl | ⟨h, hhA⟩
      · refine ⟨∅, by simp, by simp, ?_⟩
        have h0 : (⨅ h ∈ (∅ : Finset K), LinearMap.ker (Polynomial.leval h)) = ⊤ := by simp
        rw [h0, inf_top_eq, hdim]; simp
      · obtain ⟨A₀, hsub, hV, hcard⟩ := IH (A.erase h) (Finset.erase_ssubset hhA)
        exact ⟨A₀, hsub.trans (Finset.erase_subset _ _),
          by rw [hV, hstep h hhA], by rw [hcard, hstep h hhA]⟩

open Polynomial in
/-- The vanishing subspace of `W` on a `j`-set `S` whose locator lies in `W` is the
line spanned by that locator. -/
theorem vanishing_eq_span {K : Type*} [Field K] (W : Submodule K (Polynomial K)) (j : ℕ)
    (hWdeg : ∀ f ∈ W, f.degree ≤ (j : WithBot ℕ)) (S : Finset K) (hScard : S.card = j)
    (hLS : (∏ h ∈ S, (X - C h)) ∈ W) :
    (W ⊓ ⨅ h ∈ S, LinearMap.ker (Polynomial.leval h))
      = Submodule.span K {∏ h ∈ S, (X - C h)} := by
  have hLSne : (∏ h ∈ S, (X - C h)) ≠ 0 :=
    Finset.prod_ne_zero_iff.mpr (fun h _ => X_sub_C_ne_zero h)
  have hdegLS : (∏ h ∈ S, (X - C h)).natDegree = j := by
    rw [Polynomial.natDegree_prod _ _ (fun h _ => X_sub_C_ne_zero h)]; simp [hScard]
  apply le_antisymm
  · intro f hf
    obtain ⟨hfW, hfv⟩ := Submodule.mem_inf.mp hf
    have hvan : ∀ h ∈ S, f.IsRoot h := by
      intro h hh
      have h1 := (Submodule.mem_iInf _).mp hfv h
      have h2 := (Submodule.mem_iInf _).mp h1 hh
      simpa [Polynomial.IsRoot, LinearMap.mem_ker, Polynomial.leval_apply] using h2
    have hdvd : (∏ h ∈ S, (X - C h)) ∣ f := by
      apply Finset.prod_dvd_of_coprime
      · intro a _ b _ hab
        exact Polynomial.pairwise_coprime_X_sub_C Function.injective_id (by simpa using hab)
      · intro h hh
        exact Polynomial.dvd_iff_isRoot.mpr (hvan h hh)
    obtain ⟨q, rfl⟩ := hdvd
    have hqdeg : q.natDegree = 0 := by
      by_cases hq : q = 0
      · simp [hq]
      · have hnd : ((∏ h ∈ S, (X - C h)) * q).natDegree ≤ j :=
          Polynomial.natDegree_le_iff_degree_le.mpr (hWdeg _ hfW)
        rw [Polynomial.natDegree_mul hLSne hq, hdegLS] at hnd
        omega
    obtain ⟨c, hc⟩ := Polynomial.natDegree_eq_zero.mp hqdeg
    refine Submodule.mem_span_singleton.mpr ⟨c, ?_⟩
    rw [Polynomial.smul_eq_C_mul, ← hc, mul_comm]
  · rw [Submodule.span_le, Set.singleton_subset_iff]
    refine Submodule.mem_inf.mpr ⟨hLS, ?_⟩
    rw [Submodule.mem_iInf]; intro h; rw [Submodule.mem_iInf]; intro hh
    simp only [LinearMap.mem_ker, Polynomial.leval_apply, Polynomial.eval_prod]
    exact Finset.prod_eq_zero hh (by simp)

open Polynomial in
/-- **Fixed-dimensional Conjecture-F bound** (`thm:v13-fixeddim`).  For a
`(d+1)`-dimensional space `W` of polynomials of degree `≤ j`, the number of
`j`-subsets `S ⊆ H` whose locator `∏_{h∈S}(X-h)` lies in `W` is at most `C(|H|, d)`.
The paper additionally assumes `W` is gcd-trivial on `H` (`hgcd`); that hypothesis
is kept for faithfulness but turns out not to be needed for this bound. -/
theorem conjF_fixed_dim {K : Type*} [Field K] (H : Finset K)
    (W : Submodule K (Polynomial K)) (j d : ℕ)
    (hdim : Module.finrank K W = d + 1)
    (hWdeg : ∀ f ∈ W, f.degree ≤ (j : WithBot ℕ))
    (hgcd : ∀ h ∈ H, ∃ f ∈ W, Polynomial.eval h f ≠ 0) :
    ((H.powersetCard j).filter
        (fun S => (∏ h ∈ S, (Polynomial.X - Polynomial.C h)) ∈ W)).card
      ≤ Nat.choose H.card d := by
  haveI : FiniteDimensional K W := FiniteDimensional.of_finrank_pos (by rw [hdim]; omega)
  choose g hg using fun A => greedy_exists W d hdim A
  have hone : ∀ S, S ⊆ H → S.card = j → (∏ h ∈ S, (X - C h)) ∈ W →
      Module.finrank K ↥(W ⊓ ⨅ h ∈ S, LinearMap.ker (Polynomial.leval h)) = 1 := by
    intro S _ hScard hLS
    rw [vanishing_eq_span W j hWdeg S hScard hLS]
    exact finrank_span_singleton (Finset.prod_ne_zero_iff.mpr (fun h _ => X_sub_C_ne_zero h))
  rw [← Finset.card_powersetCard d H]
  apply Finset.card_le_card_of_injOn g
  · intro S hS
    simp only [Finset.coe_filter, Set.mem_setOf_eq, Finset.mem_powersetCard] at hS
    obtain ⟨⟨hSH, hSc⟩, hLS⟩ := hS
    obtain ⟨hgsub, _, hgcard⟩ := hg S
    simp only [Finset.mem_coe, Finset.mem_powersetCard]
    refine ⟨hgsub.trans hSH, ?_⟩
    rw [hgcard, hone S hSH hSc hLS]
    omega
  · intro S₁ hS₁ S₂ hS₂ hgeq
    simp only [Finset.coe_filter, Set.mem_setOf_eq, Finset.mem_powersetCard] at hS₁ hS₂
    obtain ⟨⟨hS₁H, hS₁c⟩, hLS₁⟩ := hS₁
    obtain ⟨⟨hS₂H, hS₂c⟩, hLS₂⟩ := hS₂
    obtain ⟨_, hgV₁, _⟩ := hg S₁
    obtain ⟨_, hgV₂, _⟩ := hg S₂
    have hspan : Submodule.span K {∏ h ∈ S₁, (X - C h)} = Submodule.span K {∏ h ∈ S₂, (X - C h)} := by
      rw [← vanishing_eq_span W j hWdeg S₁ hS₁c hLS₁, ← vanishing_eq_span W j hWdeg S₂ hS₂c hLS₂,
        ← hgV₁, ← hgV₂, hgeq]
    have hmem : (∏ h ∈ S₁, (X - C h)) ∈ Submodule.span K {∏ h ∈ S₂, (X - C h)} := by
      rw [← hspan]; exact Submodule.mem_span_singleton_self _
    obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp hmem
    have hmon₁ : (∏ h ∈ S₁, (X - C h)).Monic := monic_prod_of_monic _ _ (fun h _ => monic_X_sub_C h)
    have hmon₂ : (∏ h ∈ S₂, (X - C h)).Monic := monic_prod_of_monic _ _ (fun h _ => monic_X_sub_C h)
    have hc1 : c = 1 := by
      have hlc := congrArg Polynomial.leadingCoeff hc
      rw [Polynomial.smul_eq_C_mul, Polynomial.leadingCoeff_mul, hmon₁.leadingCoeff,
        hmon₂.leadingCoeff, Polynomial.leadingCoeff_C] at hlc
      simpa using hlc
    have heqL : (∏ h ∈ S₁, (X - C h)) = (∏ h ∈ S₂, (X - C h)) := by rw [← hc, hc1, one_smul]
    have hr := congrArg Polynomial.roots heqL
    rw [Polynomial.roots_prod_X_sub_C, Polynomial.roots_prod_X_sub_C] at hr
    exact Finset.val_injective hr

/-! ## Hankel tools -/

/-
**Hankel factorization determinant** (`prop:v13-hankel`).  For distinct points
`x`, the square syndrome-Hankel block `Vᵀ · diag(xⁱ ↦ xⁱ^h) · V` has determinant
`(det V)² · ∏ᵢ xᵢ^h`.
-/
theorem hankel_det {F : Type*} [CommRing F] {m : ℕ} (x : Fin m → F) (h : ℕ) :
    ((Matrix.vandermonde x).transpose * Matrix.diagonal (fun i => x i ^ h)
        * Matrix.vandermonde x).det
      = (Matrix.vandermonde x).det ^ 2 * ∏ i, x i ^ h := by
        simp +decide [ sq, mul_assoc, mul_comm, Matrix.det_mul ]

/-! ## Support combinatorics -/

/-
**Anticode packing** (`prop:v13-anticode`).  If a family `ℱ` of `j`-subsets of
an `n`-set satisfies `|A \ B| > s` for all distinct `A, B`, then
`|ℱ|·C(j,s) ≤ C(n, j-s)`.
-/
theorem anticode_packing {σ : Type*} [DecidableEq σ] (Ω : Finset σ)
    (ℱ : Finset (Finset σ)) (n j s : ℕ)
    (hΩ : Ω.card = n) (hsub : ∀ A ∈ ℱ, A ⊆ Ω) (hcard : ∀ A ∈ ℱ, A.card = j)
    (hsj : s ≤ j)
    (hsep : ∀ A ∈ ℱ, ∀ B ∈ ℱ, A ≠ B → s < (A \ B).card) :
    ℱ.card * Nat.choose j s ≤ Nat.choose n (j - s) := by
      -- Consider the set of all (j-s)-element subsets of Ω that are contained in some member of ℱ.
      let S := Finset.biUnion ℱ (fun A => (A.powersetCard (j - s)));
      have h_card_S : S.card = ℱ.card * Nat.choose j (j - s) := by
        rw [ Finset.card_biUnion ];
        · aesop;
        · intro A hA B hB hAB; simp_all +decide [ Finset.disjoint_left ] ;
          intro C hC₁ hC₂ hC₃; have := hsep A hA B hB hAB; have := Finset.card_le_card ( show A \ B ⊆ A \ C from Finset.sdiff_subset_sdiff ( Finset.Subset.refl _ ) hC₃ ) ; simp_all +decide ;
          grind;
      rw [ Nat.choose_symm hsj ] at *; exact h_card_S ▸ le_trans ( Finset.card_le_card ( show S ⊆ Finset.powersetCard ( j - s ) Ω from Finset.biUnion_subset.mpr fun A hA => Finset.powersetCard_mono ( hsub A hA ) ) ) ( by simp +decide [ hΩ ] ) ;

/-
**Johnson-ball size `D_t(n,j)`** (`cor:v13-dependency`).  The number of
`j`-subsets `S` of an `n`-set at Johnson distance `d(R,S) = j - |R ∩ S| ≤ T` from a
fixed `j`-subset `R` equals `∑_{d=0}^{T} C(j,d)·C(n-j,d)`.
-/
theorem johnson_ball_count {σ : Type*} [DecidableEq σ] (Ω R : Finset σ) (j T : ℕ)
    (hR : R ⊆ Ω) (hj : R.card = j) :
    ((Ω.powersetCard j).filter (fun S => j - (R ∩ S).card ≤ T)).card
      = ∑ d ∈ Finset.range (T + 1), Nat.choose j d * Nat.choose (Ω.card - j) d := by
  have h_count : Finset.card (Finset.filter (fun S => j - (R ∩ S).card ≤ T) (Finset.powersetCard j Ω)) = Finset.card (Finset.biUnion (Finset.range (T + 1)) (fun d => Finset.image (fun (p : Finset σ × Finset σ) => (R \ p.1) ∪ p.2) (Finset.product (Finset.powersetCard d R) (Finset.powersetCard d (Ω \ R))))) := by
    congr with S ; simp +decide [ Finset.subset_iff, Finset.mem_powersetCard, Finset.mem_biUnion ];
    constructor;
    · intro hS
      use R \ S, by
        grind, S \ R, by
        grind;
      grind;
    · rintro ⟨ a, ha, x, hx, rfl ⟩;
      rw [ Finset.card_union_of_disjoint ];
      · simp_all +decide [ Finset.card_sdiff, Finset.subset_iff ];
        rw [ show a ∩ R = a from Finset.inter_eq_left.mpr hx.1 ] ; simp_all +decide [ Finset.inter_union_distrib_left ];
        rw [ show R ∩ ( R \ a ) = R \ a by ext; aesop, show R ∩ x = ∅ by ext; aesop ] ; simp_all +decide [ Finset.card_sdiff ];
        exact ⟨ ⟨ fun y hy => by cases hy <;> aesop, Nat.sub_add_cancel ( by linarith [ show #a ≤ j from hj ▸ Finset.card_le_card ( show a ⊆ R from fun y hy => hx.1 hy ) ] ) ⟩, by rw [ show a ∩ R = a from Finset.inter_eq_left.mpr hx.1 ] ; omega ⟩;
      · exact Finset.disjoint_left.mpr fun y hy₁ hy₂ => hx.2.1 hy₂ |>.2 ( Finset.mem_sdiff.mp hy₁ |>.1 );
  rw [ h_count, Finset.card_biUnion, Finset.sum_congr rfl ];
  · intro d hd; erw [ Finset.card_image_of_injOn ] ; simp +decide [ hj, Finset.card_sdiff ] ;
    · rw [ Finset.inter_eq_left.mpr hR, hj ] ; aesop;
    · intro p hp q hq h_eq; simp_all +decide [ Finset.ext_iff ] ;
      ext x; specialize h_eq x; by_cases hx : x ∈ R <;> simp_all +decide [ Finset.subset_iff ] ;
      · grind;
      · grind;
      · grind;
  · intro d hd d' hd' hdd'; simp_all +decide [ Finset.disjoint_left ] ;
    rintro _ x y hx hx' hy hy' rfl z t hz hz' ht ht';
    contrapose! hdd';
    have h_eq : x = z := by
      ext a; replace hdd' := Finset.ext_iff.mp hdd' a; simp_all +decide [ Finset.subset_iff ] ;
      grind;
    grind

end CAP25V13.ResidueLine