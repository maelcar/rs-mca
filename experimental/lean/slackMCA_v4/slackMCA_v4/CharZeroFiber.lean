import slackMCA_v4.Main

/-!
# Polynomial size of characteristic-zero prefix fibers (`cor:upstairs-poly`)

This file formalizes the finitary core of Chojecki's corollary `cor:upstairs-poly`:
*every characteristic-zero prefix fiber in `binom(μ_n, s)` has size at most `2^{n/M_0}`*,
where `n = 2^m` and `M_0` is the least power of two exceeding the prefix length `σ`.

The characteristic-zero prefix fiber of a base set `S₀ ⊆ μ_n` is the collection of subsets
`T ⊆ μ_n` with `|T| = |S₀|` and matching elementary symmetric prefix `e_1, …, e_σ`.
By the inverse quotient theorem (`Chojecki.inverse_quotient`), any such `T` differs from `S₀`
only by toggling whole `μ_{M_0}`-cosets, i.e. `T △ S₀` is invariant under multiplication by
`2^a`-th roots of unity (`M_0 = 2^a`).  Hence the map `T ↦ (T △ S₀).image (·^{2^a})` injects the
fiber into the powerset of `μ_{n/M_0}`, which has cardinality `2^{n/M_0} = 2^{2^{m-a}}`.

We state the bound in the general parametric form: for any dyadic exponent `a` with `1 ≤ a ≤ m`
and `2^{a-1} ≤ σ`, the fiber has cardinality at most `2^{2^{m-a}}`.  Choosing the least such
`a` (so `2^a = M_0`) gives the paper's `2^{n/M_0}` bound.
-/

open Polynomial Finset BigOperators

open scoped Classical

noncomputable section

namespace Chojecki

/-- The finset of complex `2^m`-th roots of unity, i.e. the smooth domain `μ_{2^m}`. -/
def muRoots (m : ℕ) : Finset ℂ := (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset

lemma mem_muRoots {m : ℕ} {x : ℂ} : x ∈ muRoots m ↔ x ^ (2 ^ m) = 1 :=
  mem_nthRoots_iff (by positivity)

@[simp] lemma card_muRoots (m : ℕ) : (muRoots m).card = 2 ^ m :=
  card_nthRoots_toFinset (by positivity)

/-- The **characteristic-zero prefix fiber** of a base set `S₀`: all subsets of `μ_{2^m}`
of the same cardinality as `S₀` whose first `σ` elementary symmetric functions match those
of `S₀`. -/
def charZeroFiber (m σ : ℕ) (S₀ : Finset ℂ) : Finset (Finset ℂ) :=
  (muRoots m).powerset.filter
    (fun T => T.card = S₀.card ∧ ∀ j ∈ Finset.Icc 1 σ, T.val.esymm j = S₀.val.esymm j)

lemma mem_charZeroFiber {m σ : ℕ} {S₀ T : Finset ℂ} :
    T ∈ charZeroFiber m σ S₀ ↔
      (∀ x ∈ T, x ^ (2 ^ m) = 1) ∧ T.card = S₀.card ∧
        (∀ j, 1 ≤ j → j ≤ σ → T.val.esymm j = S₀.val.esymm j) := by
  classical
  simp only [charZeroFiber, Finset.mem_filter, Finset.mem_powerset, Finset.subset_iff,
    mem_muRoots, Finset.mem_Icc]
  constructor
  · rintro ⟨hsub, hcard, hesymm⟩
    exact ⟨hsub, hcard, fun j hj1 hj2 => hesymm j ⟨hj1, hj2⟩⟩
  · rintro ⟨hsub, hcard, hesymm⟩
    exact ⟨hsub, hcard, fun j hj => hesymm j hj.1 hj.2⟩

/-- **Coset invariance of the symmetric difference.**  For a fiber element `T`, the symmetric
difference `T △ S₀` is invariant under multiplication by `2^a`-th roots of unity, whenever
`a ≤ m` and `2^{a-1} ≤ σ`.  This is the finitary translation of `Chojecki.inverse_quotient`. -/
lemma symmDiff_mem_iff_of_fiber {m σ a : ℕ} (ha : a ≤ m) (hda : 2 ^ (a - 1) ≤ σ)
    {S₀ T : Finset ℂ} (hS₀ : ∀ x ∈ S₀, x ^ (2 ^ m) = 1)
    (hT : T ∈ charZeroFiber m σ S₀)
    {x κ : ℂ} (hx : x ^ (2 ^ m) = 1) (hκ : κ ^ (2 ^ a) = 1) :
    (κ * x ∈ symmDiff T S₀) ↔ (x ∈ symmDiff T S₀) := by
  obtain ⟨hTsub, -, hesymm⟩ := mem_charZeroFiber.mp hT
  have key := inverse_quotient (S := T) (T := S₀) hTsub hS₀ ha hda hesymm x κ hx hκ
  simp only [Finset.mem_symmDiff]
  by_cases h1 : κ * x ∈ T <;> by_cases h2 : κ * x ∈ S₀ <;>
    by_cases h3 : x ∈ T <;> by_cases h4 : x ∈ S₀ <;>
    simp_all

/-- The image of a `μ_{2^a}`-invariant subset of `μ_{2^m}` under `x ↦ x^{2^a}` lands in
`μ_{2^{m-a}}`. -/
lemma pow_image_subset_muRoots {m a : ℕ} (ha : a ≤ m) {U : Finset ℂ}
    (hU : ∀ x ∈ U, x ^ (2 ^ m) = 1) :
    U.image (fun x => x ^ (2 ^ a)) ⊆ muRoots (m - a) := by
  intro y hy
  rw [Finset.mem_image] at hy
  obtain ⟨x, hx, rfl⟩ := hy
  exact mem_muRoots.mpr (pow_mem_nthRoots_of_le ha (hU x hx))

/-- If `y ≠ 0` and `y^{2^a} = x^{2^a}`, then `x` is a `2^a`-th-root-of-unity multiple of `y`. -/
lemma exists_kappa_of_pow_eq {a : ℕ} {x y : ℂ} (hy : y ≠ 0) (h : y ^ (2 ^ a) = x ^ (2 ^ a)) :
    ∃ κ, κ ^ (2 ^ a) = 1 ∧ x = κ * y := by
  refine ⟨x / y, ?_, ?_⟩
  · rw [div_pow, ← h, div_self (pow_ne_zero _ hy)]
  · rw [div_mul_cancel₀ _ hy]

/-- **Polynomial size of characteristic-zero fibers (`cor:upstairs-poly`, finitary form).**
For `n = 2^m`, if `1 ≤ a ≤ m` and `2^{a-1} ≤ σ`, then the characteristic-zero prefix fiber of
any `S₀ ⊆ μ_n` has size at most `2^{2^{m-a}} = 2^{n/2^a}`.  Taking the least valid `a` (so
`2^a = M_0`, the least power of two exceeding `σ`) recovers the paper's bound `2^{n/M_0}`. -/
theorem charZeroFiber_card_le {m σ a : ℕ} (ham : a ≤ m)
    (hda : 2 ^ (a - 1) ≤ σ) {S₀ : Finset ℂ} (hS₀ : ∀ x ∈ S₀, x ^ (2 ^ m) = 1) :
    (charZeroFiber m σ S₀).card ≤ 2 ^ (2 ^ (m - a)) := by
  classical
  set φ : Finset ℂ → Finset ℂ :=
    fun T => (symmDiff T S₀).image (fun x => x ^ (2 ^ a)) with hφ
  -- Each fiber element's image lands in the powerset of `μ_{2^{m-a}}`.
  have hmaps : Set.MapsTo φ (charZeroFiber m σ S₀) (muRoots (m - a)).powerset := by
    intro T hT
    rw [Finset.mem_coe] at hT
    rw [Finset.mem_coe, Finset.mem_powerset]
    obtain ⟨hTsub, -, -⟩ := mem_charZeroFiber.mp hT
    apply pow_image_subset_muRoots ham
    intro x hx
    rw [Finset.mem_symmDiff] at hx
    rcases hx with ⟨hxT, -⟩ | ⟨hxS, -⟩
    · exact hTsub x hxT
    · exact hS₀ x hxS
  -- The map `φ` is injective on the fiber.
  have hinj : Set.InjOn φ (charZeroFiber m σ S₀) := by
    intro T₁ hT₁ T₂ hT₂ hEq
    rw [Finset.mem_coe] at hT₁ hT₂
    obtain ⟨hT₁sub, -, -⟩ := mem_charZeroFiber.mp hT₁
    obtain ⟨hT₂sub, -, -⟩ := mem_charZeroFiber.mp hT₂
    -- It suffices to prove the symmetric differences coincide.
    have hsymm : symmDiff T₁ S₀ = symmDiff T₂ S₀ := by
      ext x
      -- Membership in each symmDiff forces `x ∈ μ_{2^m}`.
      constructor
      · intro hx
        have hxmem : x ^ (2 ^ m) = 1 := by
          rw [Finset.mem_symmDiff] at hx
          rcases hx with ⟨hxT, -⟩ | ⟨hxS, -⟩
          · exact hT₁sub x hxT
          · exact hS₀ x hxS
        -- `x^{2^a} ∈ φ T₁ = φ T₂`, so some `y ∈ symmDiff T₂ S₀` has `y^{2^a} = x^{2^a}`.
        have himg : x ^ (2 ^ a) ∈ φ T₂ := by
          rw [← hEq, hφ]; exact Finset.mem_image_of_mem _ hx
        rw [hφ, Finset.mem_image] at himg
        obtain ⟨y, hy, hxy⟩ := himg
        have hymem : y ^ (2 ^ m) = 1 := by
          rw [Finset.mem_symmDiff] at hy
          rcases hy with ⟨hyT, -⟩ | ⟨hyS, -⟩
          · exact hT₂sub y hyT
          · exact hS₀ y hyS
        -- `x = κ y` with `κ^{2^a} = 1`; invariance of `symmDiff T₂ S₀` gives `x ∈ symmDiff T₂ S₀`.
        have hy0 : y ≠ 0 := fun h => by
          simp [h, zero_pow (show 2 ^ m ≠ 0 by positivity)] at hymem
        obtain ⟨κ, hκ, rfl⟩ := exists_kappa_of_pow_eq hy0 hxy
        exact (symmDiff_mem_iff_of_fiber ham hda hS₀ hT₂ hymem hκ).mpr hy
      · intro hx
        have hxmem : x ^ (2 ^ m) = 1 := by
          rw [Finset.mem_symmDiff] at hx
          rcases hx with ⟨hxT, -⟩ | ⟨hxS, -⟩
          · exact hT₂sub x hxT
          · exact hS₀ x hxS
        have himg : x ^ (2 ^ a) ∈ φ T₁ := by
          rw [hEq, hφ]; exact Finset.mem_image_of_mem _ hx
        rw [hφ, Finset.mem_image] at himg
        obtain ⟨y, hy, hxy⟩ := himg
        have hymem : y ^ (2 ^ m) = 1 := by
          rw [Finset.mem_symmDiff] at hy
          rcases hy with ⟨hyT, -⟩ | ⟨hyS, -⟩
          · exact hT₁sub y hyT
          · exact hS₀ y hyS
        have hy0 : y ≠ 0 := fun h => by
          simp [h, zero_pow (show 2 ^ m ≠ 0 by positivity)] at hymem
        obtain ⟨κ, hκ, rfl⟩ := exists_kappa_of_pow_eq hy0 hxy
        exact (symmDiff_mem_iff_of_fiber ham hda hS₀ hT₁ hymem hκ).mpr hy
    -- Recover `T₁ = T₂` from equal symmetric differences.
    have := congrArg (fun U => symmDiff U S₀) hsymm
    simpa [symmDiff_symmDiff_cancel_right] using this
  calc (charZeroFiber m σ S₀).card
      ≤ ((muRoots (m - a)).powerset).card := Finset.card_le_card_of_injOn φ hmaps hinj
    _ = 2 ^ (2 ^ (m - a)) := by rw [Finset.card_powerset, card_muRoots]

end Chojecki
