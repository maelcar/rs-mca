import Mathlib

/-!
# Locator fibers, the coefficient pigeonhole, and quotient cores

This file formalizes the unconditional Part I ("List entropy, quotient cores, and Route 1")
core of

  P. Chojecki, *Slack, Quotient Cores, and the Entropy Gap for Smooth-Domain
  Reed–Solomon Codes*.

We work with Reed–Solomon codes `RS[F, H, k] = { (P(x))_{x∈H} : deg P < k }` on an
evaluation set `H : Finset F`.  A degree-`< k` codeword `P` agrees with a received word
(represented by its interpolant `U : F[X]`) on `S ⊆ H` iff `U ≡ P (mod L_S)`, where
`L_S = ∏_{x∈S}(X - x)` is the *locator* polynomial.  This reduces list decoding to counting
*locator fibers*, and specializes for monomial-prefix words to counting fibers of the
elementary-symmetric prefix map.

The main formalized statements are:

* `Chojecki.locator_injective`, `Chojecki.eval_locator_mem` – basic locator facts;
* `Chojecki.PS_mem_codeList` and `Chojecki.PS_injOn` – the monomial-prefix injection
  `S ↦ U_c - L_S` from a prefix fiber into the decoding list (`prop:monomial-fiber`,
  positive direction);
* `Chojecki.pigeonhole_lower` – the coefficient-pigeonhole lower bound (`thm:pigeonhole`):
  some monomial-prefix word has list size `≥ q^{-σ} · C(n, s)`;
* `Chojecki.antipodal` – the antipodal identity for `2`-power roots of unity
  (`lem:antipodal`);
* `Chojecki.quotient_core_lower` – the quotient-core list obstruction (`thm:qcore`).

The `esymPrefix` map records the top `σ` subleading coefficients of the locator; since
`L_S.coeff (|S| - j) = (-1)^j e_j(S)`, this is exactly the paper's elementary-symmetric
prefix `Φ_σ = (e_1, …, e_σ)`.
-/

open Polynomial Finset BigOperators

noncomputable section

namespace Chojecki

variable {F : Type*} [Field F]

/-- The **locator polynomial** `L_S = ∏_{x∈S} (X - x)` of a finite set `S`. -/
def locator (S : Finset F) : F[X] := ∏ x ∈ S, (X - C x)

@[simp] lemma locator_monic (S : Finset F) : (locator S).Monic :=
  monic_prod_X_sub_C _ _

@[simp] lemma locator_natDegree (S : Finset F) : (locator S).natDegree = S.card := by
  simp [locator]

lemma locator_ne_zero (S : Finset F) : locator S ≠ 0 := (locator_monic S).ne_zero

/-- Evaluating the locator at a point of `S` gives `0`. -/
lemma eval_locator_mem {S : Finset F} {x : F} (hx : x ∈ S) : (locator S).eval x = 0 := by
  simp only [locator, eval_prod]
  refine Finset.prod_eq_zero hx ?_
  simp

/-- The locator determines the set: `S ↦ L_S` is injective. -/
lemma locator_injective : Function.Injective (locator (F := F)) := by
  intro S T h
  have hS : (locator S).roots = S.val := by
    simpa [locator] using
      (Polynomial.roots_prod_X_sub_C S)
  have hT : (locator T).roots = T.val := by
    simpa [locator] using
      (Polynomial.roots_prod_X_sub_C T)
  have : S.val = T.val := by rw [← hS, ← hT, h]
  exact Finset.val_injective this

/-- The agreement set of a codeword `P` with the interpolant `U` on `H`. -/
def agreeSet [DecidableEq F] (U P : F[X]) (H : Finset F) : Finset F :=
  H.filter (fun x => P.eval x = U.eval x)

/-- The list of degree-`< k` codewords agreeing with `U` on at least `s` points of `H`
(i.e. the list of codewords within relative radius `1 - s/|H|`). -/
def codeList [DecidableEq F] (U : F[X]) (H : Finset F) (k s : ℕ) : Set F[X] :=
  {P | P.degree < (k : ℕ) ∧ s ≤ (agreeSet U P H).card}

/-- The elementary-symmetric prefix `Φ_σ(S) = (e_1(S), …, e_σ(S))`, recorded here through the
top `σ` subleading coefficients of the locator: `L_S.coeff (|S|-1-j) = (-1)^{j+1} e_{j+1}(S)`. -/
def esymPrefix (σ : ℕ) (S : Finset F) : Fin σ → F :=
  fun j => (locator S).coeff (S.card - 1 - (j : ℕ))

/-- The **monomial-prefix word** `U_c = X^s + ∑_{j<σ} c_j X^{s-1-j}`.  (Up to the sign
convention this is `X^s + ∑_{j=1}^σ (-1)^j c_j X^{s-j}` of the paper.) -/
def Uc (s σ : ℕ) (c : Fin σ → F) : F[X] :=
  X ^ s + ∑ j : Fin σ, C (c j) * X ^ (s - 1 - (j : ℕ))

/-- The candidate codeword attached to a prefix fiber element: `P_S = U_c - L_S`. -/
def PS (s σ : ℕ) (c : Fin σ → F) (S : Finset F) : F[X] := Uc s σ c - locator S

/-
**Coefficient agreement.**  If `1 ≤ σ ≤ s`, `S.card = s` and `esymPrefix σ S = c`, then
`U_c` and `L_S` have the same coefficient at every index `≥ k := s - σ`.
-/
lemma Uc_sub_locator_coeff_high {s σ : ℕ} (hσ : 1 ≤ σ) (hσs : σ ≤ s)
    {c : Fin σ → F} {S : Finset F} (hScard : S.card = s) (hΦ : esymPrefix σ S = c)
    {i : ℕ} (hi : s - σ ≤ i) : (Uc s σ c).coeff i = (locator S).coeff i := by
  rcases lt_trichotomy i s <;> simp_all +decide [ Uc ];
  · rw [ Finset.sum_eq_single ⟨ s - 1 - i, by omega ⟩ ] <;> simp +decide [ *, Nat.sub_sub_self ( by omega : i ≤ s - 1 ) ];
    · rw [ ← hΦ, esymPrefix ];
      grind;
    · grind +qlia;
  · split_ifs <;> simp_all +decide [ locator ];
    · rw [ Finset.sum_eq_zero ] <;> simp_all +decide;
      · rw [ ← hScard, Finset.prod_congr rfl fun x hx => sub_eq_add_neg _ _ ];
        erw [ Finset.prod_congr rfl fun x hx => by rw [ ← Polynomial.C_neg ] ];
        erw [ Finset.prod_X_add_C_coeff ] ; aesop;
        rfl;
      · exact fun x hx => absurd hx ( by omega );
    · rw [ Finset.sum_eq_zero ];
      · rw [ Polynomial.coeff_eq_zero_of_natDegree_lt ];
        rw [ Polynomial.natDegree_prod _ _ fun x hx => Polynomial.X_sub_C_ne_zero x ] ; aesop;
      · exact fun x _ => if_neg ( by omega )

/-
The candidate codeword has degree `< k := s - σ`.
-/
lemma PS_degree {s σ : ℕ} (hσ : 1 ≤ σ) (hσs : σ ≤ s)
    {c : Fin σ → F} {S : Finset F} (hScard : S.card = s) (hΦ : esymPrefix σ S = c) :
    (PS s σ c S).degree < ((s - σ : ℕ) : ℕ) := by
  rw [ Polynomial.degree_lt_iff_coeff_zero ];
  intro m hm; rw [ PS, Polynomial.coeff_sub, Uc_sub_locator_coeff_high hσ hσs hScard hΦ hm ] ; simp +decide ;

/-
The candidate codeword agrees with `U_c` on all of `S`.
-/
lemma PS_agree [DecidableEq F] {s σ : ℕ} {c : Fin σ → F} {S : Finset F} {H : Finset F}
    (hSH : S ⊆ H) : S ⊆ agreeSet (Uc s σ c) (PS s σ c S) H := by
  intro x hx
  simp [PS, agreeSet, eval_sub];
  exact ⟨ hSH hx, eval_locator_mem hx ⟩

/-
**Monomial-prefix injection (`prop:monomial-fiber`, positive direction).**
For `s = k + σ`, the map `S ↦ P_S = U_c - L_S` sends every element of the prefix fiber
`Φ_σ^{-1}(c)` (i.e. `S ⊆ H`, `|S| = s`, `esymPrefix σ S = c`) into the decoding list.
-/
lemma PS_mem_codeList [DecidableEq F] {s σ k : ℕ} (hσ : 1 ≤ σ) (hσs : σ ≤ s) (hk : k = s - σ)
    {c : Fin σ → F} {S : Finset F} {H : Finset F}
    (hScard : S.card = s) (hΦ : esymPrefix σ S = c) (hSH : S ⊆ H) :
    PS s σ c S ∈ codeList (Uc s σ c) H k s := by
  refine' ⟨ _, _ ⟩;
  · convert PS_degree hσ hσs hScard hΦ;
  · exact hScard ▸ Finset.card_le_card ( PS_agree hSH )

/-- On a prefix fiber, `S ↦ P_S` is injective. -/
lemma PS_injOn {s σ : ℕ} (c : Fin σ → F) :
    Function.Injective (fun S : Finset F => PS s σ c S) := by
  intro S T h
  have : locator S = locator T := by
    have := h
    simp only [PS] at this
    linear_combination -this
  exact locator_injective this

/-! ### The coefficient-pigeonhole lower bound (`thm:pigeonhole`) -/

/-
**Coefficient pigeonhole lower bound.**  Let `H` be an evaluation set over a finite field
`F` with `q = |F|`, let `1 ≤ σ ≤ s ≤ |H|` and `k = s - σ`.  Then there is a monomial-prefix
word `U_c` whose decoding list at radius `1 - s/|H|` has size at least `q^{-σ} · C(|H|, s)`.
This is the flagship unconditional exponential lower bound below the entropy scale.
-/
theorem pigeonhole_lower [Fintype F] [DecidableEq F] {H : Finset F} {s σ k : ℕ}
    (hσ : 1 ≤ σ) (hσs : σ ≤ s) (_hsH : s ≤ H.card) (hk : k = s - σ) :
    ∃ c : Fin σ → F,
      (H.card.choose s : ℝ)
        ≤ (Fintype.card F : ℝ) ^ σ * (codeList (Uc s σ c) H k s).ncard := by
  -- By the pigeonhole principle, there exists a prefix fiber F_c with cardinality at least #H.choose s / (Fintype.card F)^σ.
  obtain ⟨c, hc⟩ : ∃ c : Fin σ → F, ((H.powersetCard s).filter (fun S => esymPrefix σ S = c)).card ≥ ((Nat.choose H.card s) : ℝ) / ((Fintype.card F) : ℝ) ^ σ := by
    have h_pigeonhole : (∑ c : Fin σ → F, ((Finset.powersetCard s H).filter (fun S => esymPrefix σ S = c)).card : ℝ) = (Nat.choose H.card s) := by
      rw_mod_cast [ ← Finset.card_biUnion ];
      · convert Finset.card_powersetCard s H using 2 ; ext ; aesop;
      · exact fun x _ y _ hxy => Finset.disjoint_filter.2 fun z => by aesop;
    contrapose! h_pigeonhole;
    refine' ne_of_lt ( lt_of_lt_of_le ( Finset.sum_lt_sum_of_nonempty ( Finset.univ_nonempty ) fun c _ => h_pigeonhole c ) _ );
    simp +decide [ div_eq_mul_inv, mul_comm, Finset.card_univ ];
  -- The map S ↦ PS s σ c S is an injection from the fiber F_c into codeList (Uc s σ c) H k s.
  have h_inj : Set.InjOn (fun S : Finset F => PS s σ c S) {S ∈ H.powersetCard s | esymPrefix σ S = c} := by
    exact fun x hx y hy hxy => PS_injOn c hxy;
  -- By the properties of the codeList, we have that the cardinality of the image of the fiber under the map S ↦ PS s σ c S is less than or equal to the cardinality of the codeList.
  have h_card_image : (Finset.image (fun S : Finset F => PS s σ c S) (Finset.filter (fun S => esymPrefix σ S = c) (Finset.powersetCard s H))).card ≤ (codeList (Uc s σ c) H k s).ncard := by
    rw [ ← Set.ncard_coe_finset ];
    apply_rules [ Set.ncard_le_ncard ];
    · intro P hP
      obtain ⟨S, hS, rfl⟩ := Finset.mem_image.mp hP
      exact PS_mem_codeList hσ hσs hk (Finset.mem_powersetCard.mp (Finset.mem_filter.mp hS).left).right (Finset.mem_filter.mp hS).right (Finset.mem_powersetCard.mp (Finset.mem_filter.mp hS).left).left;
    · refine' Set.Finite.subset ( Set.toFinite ( Finset.image ( fun p : Fin k → F => ∑ i ∈ Finset.univ, C ( p i ) * X ^ ( i : ℕ ) ) ( Finset.univ : Finset ( Fin k → F ) ) ) ) _;
      intro P hP
      obtain ⟨hP_deg, hP_card⟩ := hP
      have hP_poly : P = ∑ i ∈ Finset.range k, C (P.coeff i) * X ^ i := by
        ext i; simp [Polynomial.coeff_C_mul];
        exact fun hi => Polynomial.coeff_eq_zero_of_degree_lt <| lt_of_lt_of_le hP_deg <| WithBot.coe_le_coe.mpr hi;
      rw [ hP_poly ];
      simp +decide [ Finset.sum_range ];
  rw [ ge_iff_le, div_le_iff₀ ] at hc <;> norm_cast at * <;> simp_all +decide [ Finset.card_image_of_injOn ] ;
  · exact ⟨ c, by rw [ mul_comm ] ; exact hc.trans ( Nat.mul_le_mul_right _ h_card_image ) ⟩;
  · exact pow_pos ( Fintype.card_pos ) _

/-! ### The antipodal identity and inverse quotient theorem (`lem:antipodal`, `thm:upstairs`) -/

/-
**Antipodal identity (`lem:antipodal`).**  Let `n' = 2^r` with `r ≥ 1`, and let
`g : ℂ → ℤ` be supported on the `n'`-th roots of unity.  If `∑_{y^{n'}=1} g(y)·y = 0`, then
`g` is antipodally symmetric: `g y = g (-y)` for every `n'`-th root of unity `y`.
-/
set_option maxHeartbeats 1000000 in
theorem antipodal {r : ℕ} (hr : 1 ≤ r) (g : ℂ → ℤ)
    (h : ∑ y ∈ (Polynomial.nthRoots (2 ^ r) (1 : ℂ)).toFinset, (g y : ℂ) * y = 0) :
    ∀ y ∈ (Polynomial.nthRoots (2 ^ r) (1 : ℂ)).toFinset, g y = g (-y) := by
  -- Let `n' = 2^r` and `ζ = exp(2πi/n')` be a primitive `n'`-th root of unity.
  set n' := 2 ^ r with hn'
  set ζ := Complex.exp (2 * Real.pi * Complex.I / n') with hζ_def;
  -- The roots of unity are exactly the powers of ζ.
  have h_roots : (nthRoots n' 1).toFinset = Finset.image (fun k : ℕ => ζ ^ k) (Finset.range n') := by
    ext; simp [nthRoots];
    constructor <;> intro h <;> simp_all +decide [ sub_eq_iff_eq_add ];
    · -- Since $a^{2^r} = 1$, we can write $a$ as $e^{2\pi i k / 2^r}$ for some integer $k$.
      obtain ⟨k, hk⟩ : ∃ k : ℤ, ‹ℂ› = Complex.exp (2 * Real.pi * Complex.I * k / 2 ^ r) := by
        -- Since $a^{2^r} = 1$, we can write $a$ as $e^{i\theta}$ for some $\theta$.
        obtain ⟨θ, hθ⟩ : ∃ θ : ℝ, ‹ℂ› = Complex.exp (θ * Complex.I) := by
          have := congr_arg Complex.normSq h.2 ; norm_num [ Complex.normSq_eq_norm_sq, pow_eq_one_iff_of_nonneg ] at this;
          rw [ Complex.norm_eq_one_iff ] at this ; tauto;
        simp_all +decide [ ← Complex.exp_nat_mul ];
        rw [ Complex.exp_eq_one_iff ] at h;
        exact h.2.imp fun n hn => congr_arg Complex.exp <| by rw [ eq_div_iff ( by norm_num ) ] ; linear_combination' hn;
      -- Since $k$ is an integer, we can write $k = q \cdot 2^r + a$ for some integer $q$ and $0 \leq a < 2^r$.
      obtain ⟨q, a, ha⟩ : ∃ q : ℤ, ∃ a : ℕ, a < 2 ^ r ∧ k = q * 2 ^ r + a := by
        exact ⟨ k / 2 ^ r, Int.toNat ( k % 2 ^ r ), by linarith [ Int.emod_lt_of_pos k ( by positivity : 0 < ( 2 ^ r : ℤ ) ), Int.toNat_of_nonneg ( Int.emod_nonneg k ( by positivity : ( 2 ^ r : ℤ ) ≠ 0 ) ) ], by linarith [ Int.emod_add_mul_ediv k ( 2 ^ r ), Int.toNat_of_nonneg ( Int.emod_nonneg k ( by positivity : ( 2 ^ r : ℤ ) ≠ 0 ) ) ] ⟩;
      use a; simp_all +decide [ ← Complex.exp_nat_mul, mul_div_cancel₀ ] ;
      rw [ Complex.exp_eq_exp_iff_exists_int ] ; use -q ; push_cast ; ring_nf ; norm_num [ show ( 2 : ℂ ) ^ r ≠ 0 by norm_num ] ;
      simp +decide [ mul_assoc, mul_comm, mul_left_comm ];
    · refine' ⟨ ne_of_apply_ne Polynomial.natDegree <| _, _ ⟩ <;> norm_num [ Polynomial.natDegree_pow ];
      obtain ⟨ a, ha, rfl ⟩ := h; rw [ ← pow_mul, Nat.mul_comm, pow_mul, ← Complex.exp_nat_mul, mul_comm ] ; norm_num [ show ( 2 ^ r : ℂ ) ≠ 0 by norm_num ] ;
  -- The powers $1, \zeta, \ldots, \zeta^{n'/2-1}$ are linearly independent over $\mathbb{Q}$.
  have h_lin_indep : LinearIndependent ℚ (fun k : Fin (n' / 2) => ζ ^ (k : ℕ)) := by
    -- The minimal polynomial of $\zeta$ over $\mathbb{Q}$ is the $n'$-th cyclotomic polynomial $\Phi_{n'}(X)$.
    have h_min_poly : minpoly ℚ ζ = Polynomial.cyclotomic n' ℚ := by
      have h_min_poly : IsPrimitiveRoot ζ n' := by
        exact Complex.isPrimitiveRoot_exp _ ( by aesop );
      rw [ h_min_poly.minpoly_eq_cyclotomic_of_irreducible ( Polynomial.cyclotomic.irreducible_rat <| by positivity ) ];
    -- The degree of the cyclotomic polynomial $\Phi_{n'}(X)$ is $\varphi(n') = n'/2$.
    have h_deg : Polynomial.natDegree (Polynomial.cyclotomic n' ℚ) = n' / 2 := by
      rw [ Polynomial.natDegree_cyclotomic, Nat.totient_prime_pow ] <;> norm_num [ hr ];
      · exact Eq.symm ( Nat.div_eq_of_eq_mul_left zero_lt_two ( by rw [ ← pow_succ, Nat.sub_add_cancel hr ] ) );
      · linarith;
    have h_lin_indep : LinearIndependent ℚ (fun k : Fin (Polynomial.natDegree (minpoly ℚ ζ)) => ζ ^ (k : ℕ)) := by
      have h_alg : IsIntegral ℚ ζ := by
        refine' ⟨ Polynomial.X ^ n' - 1, _, _ ⟩;
        · exact Polynomial.monic_X_pow_sub_C _ ( by positivity );
        · norm_num +zetaDelta at *;
          rw [ sub_eq_zero, ← Complex.exp_nat_mul, mul_comm, Complex.exp_eq_one_iff ] ; use 1 ; norm_num
      exact linearIndependent_pow ζ;
    convert h_lin_indep using 1; all_goals rw [ h_min_poly, h_deg ];
  -- By pairing $a$ with $a + n'/2$, we can rewrite the sum as $\sum_{a=0}^{n'/2-1} (g(\zeta^a) - g(-\zeta^a)) \zeta^a = 0$.
  have h_pair : ∑ a ∈ Finset.range (n' / 2), (g (ζ ^ a) - g (-ζ ^ a)) * ζ ^ a = 0 := by
    have h_pair : ∑ y ∈ Finset.image (fun k : ℕ => ζ ^ k) (Finset.range n'), (g y : ℂ) * y = ∑ a ∈ Finset.range (n' / 2), ((g (ζ ^ a) : ℂ) * ζ ^ a + (g (ζ ^ (a + n' / 2)) : ℂ) * ζ ^ (a + n' / 2)) := by
      rw [ Finset.sum_image ];
      · rw [ ← Finset.sum_range_add_sum_Ico _ ( show n' / 2 ≤ n' from Nat.div_le_self _ _ ) ];
        norm_num [ Finset.sum_add_distrib, Finset.sum_Ico_eq_sum_range ];
        rw [ show n' - n' / 2 = n' / 2 by rw [ Nat.sub_eq_of_eq_add ] ; linarith [ Nat.div_mul_cancel ( show 2 ∣ n' from dvd_pow_self _ ( by linarith ) ) ] ] ; ac_rfl;
      · intro k hk l hl hkl; simp_all +decide [ ← Complex.exp_nat_mul ] ;
        rw [ Complex.exp_eq_exp_iff_exists_int ] at hkl;
        obtain ⟨ n, hn ⟩ := hkl; rw [ Complex.ext_iff ] at hn; norm_num [ Complex.exp_re, Complex.exp_im ] at hn;
        norm_num [ Complex.normSq, Complex.div_re, Complex.div_im ] at hn;
        norm_cast at hn ; simp_all +decide;
        -- Simplify the equation $k * (2 * π * 2^r / (2^r * 2^r)) = l * (2 * π * 2^r / (2^r * 2^r)) + n * (2 * π)$ to get $k = l + n * 2^r$.
        have h_simplified : k = l + n * 2 ^ r := by
          field_simp at hn;
          simpa [ ← @Int.cast_inj ℝ ] using by linear_combination' hn;
        nlinarith [ show n = 0 by nlinarith ];
    -- Since $\zeta^{n'/2} = -1$, we have $\zeta^{a + n'/2} = -\zeta^a$.
    have h_zeta_half : ζ ^ (n' / 2) = -1 := by
      rw [ ← Complex.exp_nat_mul, mul_comm, Complex.exp_eq_exp_re_mul_sin_add_cos ] ; norm_num [ show n' ≠ 0 by positivity ];
      rw [ Nat.cast_div ( dvd_pow_self _ ( by linarith ) ) ] <;> norm_num [ hn' ] ; ring_nf ; norm_num [ show n' ≠ 0 by positivity ] ;
      norm_num [ mul_assoc, ← mul_pow ];
    simp_all +decide [ pow_add, sub_mul ];
    simpa only [ Finset.sum_add_distrib, Finset.sum_neg_distrib, sub_eq_add_neg ] using h;
  -- Since the powers $1, \zeta, \ldots, \zeta^{n'/2-1}$ are linearly independent over $\mathbb{Q}$, each coefficient must be zero.
  have h_coeff_zero : ∀ a ∈ Finset.range (n' / 2), (g (ζ ^ a) - g (-ζ ^ a)) = 0 := by
    rw [ Fintype.linearIndependent_iff ] at h_lin_indep;
    specialize h_lin_indep ( fun i => ( g ( ζ ^ ( i : ℕ ) ) - g ( -ζ ^ ( i : ℕ ) ) : ℚ ) ) ; simp_all +decide [ Finset.sum_range, Algebra.smul_def ] ;
    exact fun a ha => mod_cast h_lin_indep h_pair ⟨ a, ha ⟩;
  intro y hy; rw [ h_roots ] at hy; obtain ⟨ k, hk, rfl ⟩ := Finset.mem_image.mp hy; simp_all +decide [ sub_eq_zero ] ;
  by_cases hk' : k < 2 ^ r / 2;
  · exact h_coeff_zero k hk';
  · convert h_coeff_zero ( k - 2 ^ r / 2 ) _ |> Eq.symm using 1;
    · rw [ show k = 2 ^ r / 2 + ( k - 2 ^ r / 2 ) by rw [ Nat.add_sub_cancel' ( le_of_not_gt hk' ) ] ] ; norm_num [ pow_add, pow_mul, ← Complex.exp_nat_mul, mul_div_cancel₀ ];
      rw [ Nat.cast_div ( dvd_pow_self _ ( by linarith ) ) ] <;> norm_num ; ring;
      norm_num [ Complex.exp_neg, Complex.exp_add, mul_assoc, mul_comm Real.pi ];
    · rw [ show k = 2 ^ r / 2 + ( k - 2 ^ r / 2 ) by rw [ Nat.add_sub_cancel' ( le_of_not_gt hk' ) ] ] ; norm_num [ pow_add, pow_mul, ← Complex.exp_nat_mul, mul_div_cancel₀ ] ; ring;
      rw [ Nat.cast_div ( show 2 ∣ 2 ^ r from dvd_pow_self _ ( by linarith ) ) ( by norm_num ) ] ; norm_num ; ring;
      norm_num [ mul_assoc, mul_comm, mul_left_comm ];
      norm_num [ ← mul_assoc, ← mul_pow ];
      norm_num [ mul_assoc, mul_comm Complex.I ];
    · rw [ tsub_lt_iff_left ] <;> linarith [ Nat.div_mul_cancel ( show 2 ∣ 2 ^ r from dvd_pow_self _ ( by linarith ) ), Nat.pow_le_pow_right two_pos hr ]

/-! ### The quotient-core list obstruction (`thm:qcore`) -/

/-
The locator of a set `D` of `M` distinct common `M`-th roots of `α` is `X^M - C α`.
(Each `K`-coset in the smooth domain is such a set: it is a fiber of `x ↦ x^M`.)
-/
lemma locator_pow_coset {D : Finset F} {M : ℕ} {α : F}
    (hM : 0 < M) (hcard : D.card = M) (hroot : ∀ x ∈ D, x ^ M = α) :
    locator D = X ^ M - C α := by
  refine' Polynomial.eq_of_degree_sub_lt_of_eval_finset_eq _ _ _;
  exact D;
  · convert Polynomial.degree_sub_lt _ _ _ <;> norm_num [ hcard, locator_monic, locator_natDegree ];
    · rw [ locator, Polynomial.degree_prod, Finset.sum_congr rfl fun x hx => Polynomial.degree_X_sub_C _ ] ; aesop;
    · rw [ Polynomial.degree_sub_C ] <;> simp +decide [ hM ];
      rw [ locator, Polynomial.degree_prod, Finset.sum_congr rfl fun x hx => Polynomial.degree_X_sub_C _ ] ; aesop;
    · exact locator_ne_zero D;
    · rw [ Polynomial.leadingCoeff_X_pow_sub_C ] ; aesop;
  · intro x hx
    simp [locator, hroot x hx];
    rw [ Polynomial.eval_prod, Finset.prod_eq_zero hx ] ; simp +decide

/-
Cardinality of a `K`-coset in the smooth domain, realized as `{ω^{j+Nt} : t < M}`.
-/
lemma coset_card [DecidableEq F] {ω : F} {n M N j : ℕ} (hω : IsPrimitiveRoot ω n)
    (hn : 0 < n) (hNM : N * M = n) :
    ((Finset.range M).image (fun t => ω ^ (j + N * t))).card = M := by
  rw [ Finset.card_image_of_injOn, Finset.card_range ];
  intro t ht t' ht' h_eq;
  have h_mod : ω ^ (N * t) = ω ^ (N * t') := by
    simp_all +decide [ pow_add ];
    exact h_eq.resolve_right fun h => by have := hω.ne_zero hn.ne'; aesop;
  have := hω.pow_inj ( show N * t < n from by nlinarith [ Finset.mem_range.mp ht, Finset.mem_range.mp ht' ] ) ( show N * t' < n from by nlinarith [ Finset.mem_range.mp ht, Finset.mem_range.mp ht' ] ) ; aesop;

/-
The locator of a `K`-coset `{ω^{j+Nt} : t < M}` is `X^M - C (ω^{jM})`.
-/
lemma coset_locator [DecidableEq F] {ω : F} {n M N j : ℕ} (hω : IsPrimitiveRoot ω n)
    (hn : 0 < n) (hNM : N * M = n) (hMpos : 0 < M) :
    locator ((Finset.range M).image (fun t => ω ^ (j + N * t))) = X ^ M - C (ω ^ (j * M)) := by
  refine' locator_pow_coset hMpos _ _;
  · convert coset_card hω hn hNM;
  · simp +decide [ pow_add, pow_mul' ];
    intro a ha; ring;
    rw [ show ω ^ ( a * N * M ) = ( ω ^ n ) ^ a by rw [ ← hNM ] ; ring, hω.pow_eq_one, one_pow, mul_one ]

/-
The `K`-cosets `{ω^{j+Nt} : t < M}` for `j < N` are pairwise disjoint.
-/
lemma cosets_disjoint [DecidableEq F] {ω : F} {n M N : ℕ} (hω : IsPrimitiveRoot ω n) (hNM : N * M = n) :
    (↑(Finset.range N) : Set ℕ).PairwiseDisjoint
      (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t))) := by
  intro j hj k hk hne; simp_all +decide [ Finset.disjoint_left ] ;
  intro a ha x hx H; have := hω.pow_inj ( show k + N * x < n from by nlinarith ) ( show j + N * a < n from by nlinarith ) ; simp_all +decide [ pow_add, pow_mul ] ;
  exact hne ( by nlinarith [ show x = a by nlinarith ] )

/-
The degree drop: `X^{|A|·M} - ∏_{j∈A}(X^M - C (β j))` has degree `≤ |A|·M - M`
(the leading `X^{|A|·M}` term cancels, and all remaining terms are divisible by `X^M`).
-/
lemma Xpow_sub_prod_natDegree_le {M : ℕ} (A : Finset ℕ) (β : ℕ → F) :
    (X ^ (A.card * M) - ∏ j ∈ A, (X ^ M - C (β j))).natDegree ≤ A.card * M - M := by
  have h_deg : Polynomial.natDegree (Polynomial.X ^ A.card - ∏ j ∈ A, (Polynomial.X - Polynomial.C (β j))) ≤ A.card - 1 := by
    have h_deg : Polynomial.degree (Polynomial.X ^ A.card - ∏ j ∈ A, (Polynomial.X - Polynomial.C (β j))) < A.card := by
      convert Polynomial.degree_sub_lt _ _ _ <;> norm_num [ Polynomial.degree_prod, Polynomial.degree_X_pow, Polynomial.degree_X_sub_C ];
      rw [ Polynomial.leadingCoeff_prod, Finset.prod_congr rfl fun _ _ => Polynomial.leadingCoeff_X_sub_C _ ] ; simp +decide;
    contrapose! h_deg;
    rw [ Polynomial.degree_eq_natDegree ] <;> norm_cast;
    · exact Nat.le_of_pred_lt h_deg;
    · aesop;
  convert Nat.mul_le_mul_right M h_deg using 1;
  · rw [ show ( X ^ ( #A * M ) - ∏ j ∈ A, ( X ^ M - C ( β j ) ) ) = ( X ^ #A - ∏ j ∈ A, ( X - C ( β j ) ) |> Polynomial.comp <| Polynomial.X ^ M ) from ?_, Polynomial.natDegree_comp, Polynomial.natDegree_X_pow ];
    simp +decide [ Polynomial.prod_comp ];
    ring;
  · rw [ tsub_mul, one_mul ]

/-
Over a finite field the decoding list is finite (finitely many degree-`< k` polynomials).
-/
lemma codeList_finite [Fintype F] [DecidableEq F] (U : F[X]) (H : Finset F) (k s : ℕ) :
    (codeList U H k s).Finite := by
  -- The set of polynomials with degree less than k is finite.
  have h_finite_deg : Set.Finite {P : F[X] | P.degree < (k : ℕ)} := by
    refine Set.Finite.subset ( Set.toFinite ( Set.range fun p : Fin k → F => ∑ i : Fin k, Polynomial.C ( p i ) * Polynomial.X ^ ( i : ℕ ) ) ) ?_;
    intro P hP; use fun i => P.coeff i; ext i; by_cases hi : i < k <;> simp_all +decide [ Polynomial.degree_lt_iff_coeff_zero ] ;
    · rw [ Finset.sum_eq_single ⟨ i, hi ⟩ ] <;> aesop;
    · exact Finset.sum_eq_zero fun x hx => if_neg ( by linarith [ Fin.is_lt x ] );
  exact h_finite_deg.subset fun P hP => hP.1

/-
The locator of a disjoint union of sets is the product of the locators.
-/
lemma locator_biUnion {ι : Type*} [DecidableEq F] [DecidableEq ι] {s : Finset ι} {t : ι → Finset F}
    (h : (↑s : Set ι).PairwiseDisjoint t) :
    locator (s.biUnion t) = ∏ i ∈ s, locator (t i) := by
  unfold locator
  exact Finset.prod_biUnion h

/-
Membership of a quotient-core codeword `P_{A'}` in the decoding list.
-/
set_option maxHeartbeats 1000000 in
lemma qcore_mem [Fintype F] [DecidableEq F] {ω : F} {n M N k σ : ℕ}
    (hω : IsPrimitiveRoot ω n) (hn : 0 < n) (hNM : N * M = n)
    (hMk : M ∣ k) (hσ1 : 1 ≤ σ) (hσM : σ < M)
    (A' : Finset ℕ) (hA' : A' ⊆ Finset.Icc 1 (N - 1)) (hd : A'.card = k / M) :
    locator ((Finset.range σ).image (fun t => ω ^ (N * t))) *
        (X ^ k - locator (A'.biUnion (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t)))))
      ∈ codeList (X ^ k * locator ((Finset.range σ).image (fun t => ω ^ (N * t))))
          ((Finset.range n).image (fun i => ω ^ i)) k (k + σ) := by
  refine' ⟨ _, _ ⟩;
  · by_cases hk : k = 0;
    · simp_all +decide [ Finset.ext_iff ];
      rw [ show A' = ∅ by ext; aesop ] ; simp +decide [ locator ];
    · refine' lt_of_le_of_lt ( Polynomial.degree_mul_le _ _ ) _;
      have h_deg : Polynomial.degree (X ^ k - locator (Finset.biUnion A' (fun j => Finset.image (fun t => ω ^ (j + N * t)) (Finset.range M)))) ≤ (k - M : ℕ) := by
        have h_deg : Polynomial.natDegree (X ^ k - ∏ j ∈ A', (X ^ M - Polynomial.C (ω ^ (j * M)))) ≤ k - M := by
          have h_deg : Polynomial.natDegree (X ^ (A'.card * M) - ∏ j ∈ A', (X ^ M - Polynomial.C (ω ^ (j * M)))) ≤ A'.card * M - M := by
            convert Xpow_sub_prod_natDegree_le A' ( fun j => ω ^ ( j * M ) ) using 1;
          rwa [ hd, Nat.div_mul_cancel hMk ] at h_deg;
        rw [ locator_biUnion ];
        · rw [ Finset.prod_congr rfl fun x hx => coset_locator hω hn hNM ( by linarith ) ];
          exact Polynomial.degree_le_of_natDegree_le h_deg;
        · intro j hj j' hj' hij; have := cosets_disjoint hω hNM; simp_all +decide [ Set.PairwiseDisjoint ] ;
          exact this ( show j < N from lt_of_le_of_lt ( Finset.mem_Icc.mp ( hA' hj ) |>.2 ) ( Nat.pred_lt ( ne_bot_of_gt ( show 0 < N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ) ) ) ( show j' < N from lt_of_le_of_lt ( Finset.mem_Icc.mp ( hA' hj' ) |>.2 ) ( Nat.pred_lt ( ne_bot_of_gt ( show 0 < N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ) ) ) hij;
      refine' lt_of_le_of_lt ( add_le_add ( Polynomial.degree_le_natDegree ) h_deg ) _;
      rw [ locator_natDegree ] ; norm_cast ; linarith [ Nat.sub_add_cancel ( show M ≤ k from Nat.le_of_dvd ( Nat.pos_of_ne_zero hk ) hMk ), show Finset.card ( Finset.image ( fun t => ω ^ ( N * t ) ) ( Finset.range σ ) ) ≤ σ from Finset.card_image_le.trans ( by simp ) ] ;
  · refine' le_trans _ ( Finset.card_mono <| show agreeSet _ _ _ ≥ ( Finset.image ( fun t => ω ^ ( N * t ) ) ( Finset.range σ ) ) ∪ ( Finset.biUnion A' fun j => Finset.image ( fun t => ω ^ ( j + N * t ) ) ( Finset.range M ) ) from _ );
    · rw [ Finset.card_union_of_disjoint ];
      · rw [ Finset.card_biUnion ];
        · rw [ Finset.sum_congr rfl fun x hx => coset_card hω hn hNM ] ; simp +decide [ hd ];
          rw [ Finset.card_image_of_injOn, Nat.div_mul_cancel hMk ];
          · simp +decide [ add_comm ];
          · intro a ha b hb; have := hω.pow_inj ( show N * a < n from by nlinarith [ Finset.mem_range.mp ha ] ) ( show N * b < n from by nlinarith [ Finset.mem_range.mp hb ] ) ; aesop;
        · intro i hi j hj hij;
          have := cosets_disjoint hω hNM;
          exact this ( Finset.mem_range.mpr ( by linarith [ Finset.mem_Icc.mp ( hA' hi ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ) ( Finset.mem_range.mpr ( by linarith [ Finset.mem_Icc.mp ( hA' hj ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ) hij;
      · simp +decide [ Finset.disjoint_left ];
        intro a ha x hx y hy H; have := hω.pow_inj ( show x + N * y < n from by nlinarith [ Finset.mem_Icc.mp ( hA' hx ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ( show N * a < n from by nlinarith [ Finset.mem_Icc.mp ( hA' hx ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ; simp_all +decide [ pow_add, pow_mul ] ;
        nlinarith [ show y = a by nlinarith [ Finset.mem_Icc.mp ( hA' hx ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ], Finset.mem_Icc.mp ( hA' hx ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ];
    · intro x hx; simp_all +decide [ agreeSet ] ;
      rcases hx with ( ⟨ a, ha, rfl ⟩ | ⟨ a, ha, b, hb, rfl ⟩ ) <;> simp_all +decide [ locator ];
      · refine' ⟨ ⟨ N * a, _, _ ⟩, _ ⟩;
        · nlinarith;
        · rfl;
        · rw [ Polynomial.eval_prod, Finset.prod_eq_zero ( Finset.mem_image_of_mem _ ( Finset.mem_range.mpr ha ) ) ] <;> simp +decide;
      · refine' ⟨ ⟨ a + N * b, _, rfl ⟩, _ ⟩;
        · nlinarith [ Finset.mem_Icc.mp ( hA' ha ), Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ];
        · simp +decide [ Polynomial.eval_prod, Finset.prod_eq_prod_diff_singleton_mul ( show ω ^ ( a + N * b ) ∈ A'.biUnion ( fun j => Finset.image ( fun t => ω ^ ( j + N * t ) ) ( Finset.range M ) ) from Finset.mem_biUnion.mpr ⟨ a, ha, Finset.mem_image.mpr ⟨ b, Finset.mem_range.mpr hb, rfl ⟩ ⟩ ) ] ; ring

/-
Distinct label sets give distinct quotient-core codewords.
-/
lemma qcore_inj [DecidableEq F] {ω : F} {n M N k σ : ℕ}
    (hω : IsPrimitiveRoot ω n) (hNM : N * M = n)
    {A₁ A₂ : Finset ℕ} (h1 : A₁ ⊆ Finset.Icc 1 (N - 1)) (h2 : A₂ ⊆ Finset.Icc 1 (N - 1))
    (hc1 : A₁.card = k / M) (hc2 : A₂.card = k / M)
    (he : locator ((Finset.range σ).image (fun t => ω ^ (N * t))) *
            (X ^ k - locator (A₁.biUnion (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t)))))
          = locator ((Finset.range σ).image (fun t => ω ^ (N * t))) *
            (X ^ k - locator (A₂.biUnion (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t)))))) :
    A₁ = A₂ := by
  by_cases hM : M = 0;
  · have := hω.eq_orderOf; aesop;
  · -- By `locator_injective`, we have `A₁.biUnion Cset = A₂.biUnion Cset`.
    have h_biUnion_eq : A₁.biUnion (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t))) = A₂.biUnion (fun j => (Finset.range M).image (fun t => ω ^ (j + N * t))) := by
      apply Chojecki.locator_injective;
      exact mul_left_cancel₀ ( show locator ( image ( fun t => ω ^ ( N * t ) ) ( range σ ) ) ≠ 0 from locator_ne_zero _ ) ( by linear_combination' he.symm );
    have h_disjoint : ∀ j j' : ℕ, j ∈ Finset.Icc 1 (N - 1) → j' ∈ Finset.Icc 1 (N - 1) → j ≠ j' → Disjoint (Finset.image (fun t => ω ^ (j + N * t)) (Finset.range M)) (Finset.image (fun t => ω ^ (j' + N * t)) (Finset.range M)) := by
      intros j j' hj hj' hj_ne_j'
      have h_coset_disjoint : Disjoint (Finset.image (fun t => ω ^ (j + N * t)) (Finset.range M)) (Finset.image (fun t => ω ^ (j' + N * t)) (Finset.range M)) := by
        have := cosets_disjoint hω hNM
        exact this ( Finset.mem_range.mpr ( by linarith [ Finset.mem_Icc.mp hj, Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ) ( Finset.mem_range.mpr ( by linarith [ Finset.mem_Icc.mp hj', Nat.sub_add_cancel ( show 1 ≤ N from Nat.pos_of_ne_zero ( by aesop_cat ) ) ] ) ) hj_ne_j';
      exact h_coset_disjoint;
    refine' Finset.Subset.antisymm _ _ <;> intro j hj <;> simp_all +decide [ Finset.ext_iff ];
    · contrapose! h_biUnion_eq;
      refine' ⟨ ω ^ ( j + N * 0 ), Or.inl ⟨ ⟨ j, hj, 0, Nat.pos_of_ne_zero hM, rfl ⟩, _ ⟩ ⟩;
      intro a ha t ht h; specialize h_disjoint a j; simp_all +decide [ Finset.disjoint_left ] ;
      exact h_disjoint ( Finset.mem_Icc.mp ( h2 ha ) |>.1 ) ( Finset.mem_Icc.mp ( h2 ha ) |>.2 ) ( Finset.mem_Icc.mp ( h1 hj ) |>.1 ) ( Finset.mem_Icc.mp ( h1 hj ) |>.2 ) ( by aesop ) t ht 0 ( Nat.pos_of_ne_zero hM ) ( by simpa using h.symm );
    · contrapose! h_biUnion_eq;
      refine' ⟨ _, Or.inr ⟨ _, j, hj, 0, Nat.pos_of_ne_zero hM, rfl ⟩ ⟩;
      intro a ha t ht; specialize h_disjoint a j; simp_all +decide [ Finset.disjoint_left ] ;
      exact fun h => h_disjoint ( Finset.mem_Icc.mp ( h1 ha ) |>.1 ) ( Finset.mem_Icc.mp ( h1 ha ) |>.2 ) ( Finset.mem_Icc.mp ( h2 hj ) |>.1 ) ( Finset.mem_Icc.mp ( h2 hj ) |>.2 ) ( by aesop ) t ht 0 ( Nat.pos_of_ne_zero hM ) ( by simpa using h.symm )

/-- **Quotient-core list obstruction (`thm:qcore`), on the smooth multiplicative domain**
`μ_n = {ω^i : i < n}` for a primitive `n`-th root of unity `ω` (which is exactly a multiplicative
subgroup of `Fˣ` of order `n`).  With `N = n/M` (so `N*M = n`), `M ∣ k`, `k/M ≤ N-1`, and
`1 ≤ σ < M`, there is a received word `U` with at least `C(N-1, k/M)` degree-`< k` codewords
agreeing with it on `k + σ` coordinates of the domain.

The hypothesis `hkM : k/M ≤ N-1` is stated in the source but is not needed for this
inequality (when `k/M > N-1` the binomial coefficient is `0` and the bound is vacuous); it is
kept here for faithfulness to the paper. -/
theorem quotient_core_mun [Fintype F] [DecidableEq F] {ω : F} {n M N k σ : ℕ}
    (hω : IsPrimitiveRoot ω n) (hn : 0 < n) (hNM : N * M = n)
    (hMk : M ∣ k) (_hkM : k / M ≤ N - 1) (hσ1 : 1 ≤ σ) (hσM : σ < M) :
    ∃ U : F[X],
      (N - 1).choose (k / M)
        ≤ (codeList U ((Finset.range n).image (fun i => ω ^ i)) k (k + σ)).ncard := by
  classical
  set T : Finset F := (Finset.range σ).image (fun t => ω ^ (N * t)) with hT
  set Cset : ℕ → Finset F := fun j => (Finset.range M).image (fun t => ω ^ (j + N * t)) with hCset
  set f : Finset ℕ → F[X] := fun A' => locator T * (X ^ k - locator (A'.biUnion Cset)) with hf
  set dom : Finset F := (Finset.range n).image (fun i => ω ^ i) with hdom
  refine ⟨X ^ k * locator T, ?_⟩
  have hsub : ↑((Finset.powersetCard (k / M) (Finset.Icc 1 (N - 1))).image f)
      ⊆ codeList (X ^ k * locator T) dom k (k + σ) := by
    intro P hP
    rw [Finset.coe_image, Set.mem_image] at hP
    obtain ⟨A', hA', rfl⟩ := hP
    rw [Finset.mem_coe, Finset.mem_powersetCard] at hA'
    exact qcore_mem hω hn hNM hMk hσ1 hσM A' hA'.1 hA'.2
  have hinj : Set.InjOn f ↑(Finset.powersetCard (k / M) (Finset.Icc 1 (N - 1))) := by
    intro A₁ h1 A₂ h2 he
    rw [Finset.mem_coe, Finset.mem_powersetCard] at h1 h2
    exact qcore_inj (k := k) (σ := σ) hω hNM h1.1 h2.1 h1.2 h2.2 he
  have hAcard : (Finset.Icc 1 (N - 1)).card = N - 1 := by rw [Nat.card_Icc]; omega
  calc (N - 1).choose (k / M)
      = (Finset.Icc 1 (N - 1)).card.choose (k / M) := by rw [hAcard]
    _ = (Finset.powersetCard (k / M) (Finset.Icc 1 (N - 1))).card :=
          (Finset.card_powersetCard _ _).symm
    _ = ((Finset.powersetCard (k / M) (Finset.Icc 1 (N - 1))).image f).card :=
          (Finset.card_image_of_injOn hinj).symm
    _ = (((Finset.powersetCard (k / M) (Finset.Icc 1 (N - 1))).image f : Finset F[X])
            : Set F[X]).ncard :=
          (Set.ncard_coe_finset _).symm
    _ ≤ (codeList (X ^ k * locator T) dom k (k + σ)).ncard :=
          Set.ncard_le_ncard hsub (codeList_finite _ _ _ _)

/-
**Quotient-core list obstruction (`thm:qcore`).**  Let `H ≤ Fˣ` be a multiplicative
subgroup of order `n`, `K ≤ H` of order `M`, `N = n / M`, with `M ∣ k`, `k / M ≤ N - 1`, and
`1 ≤ σ < M`.  Then there is a received word `U` on the domain `H` (coerced to `F`) with at least
`C(N-1, k/M)` degree-`< k` codewords agreeing with it on `k + σ` coordinates.
-/
theorem quotient_core_lower [Fintype F] [DecidableEq F] (H K : Subgroup Fˣ) (hKH : K ≤ H)
    [Fintype H] [Fintype K]
    (n M k σ : ℕ) (hn : Fintype.card H = n) (hM : Fintype.card K = M)
    (hMk : M ∣ k) (hkM : k / M ≤ n / M - 1) (hσ1 : 1 ≤ σ) (hσM : σ < M) :
    ∃ U : F[X],
      (n / M - 1).choose (k / M)
        ≤ (codeList U (Finset.univ.image (fun x : H => ((x : Fˣ) : F))) k (k + σ)).ncard := by
  obtain ⟨g₀, hg₀⟩ : ∃ g₀ : ↥H, ∀ x : ↥H, x ∈ Subgroup.zpowers g₀ := by
    convert IsCyclic.exists_generator;
    exact inferInstance;
  -- Set ω := (g : Fˣ).val, i.e., ω = Units.val (g₀ : Fˣ).
  set ω : F := (g₀ : Fˣ).val
  have hω : IsPrimitiveRoot ω n := by
    have hω_order : orderOf ω = n := by
      rw [ ← hn, orderOf_units ];
      convert orderOf_eq_card_of_forall_mem_zpowers hg₀;
      · simp +decide;
      · rw [ Nat.card_eq_fintype_card ];
    exact hω_order ▸ IsPrimitiveRoot.orderOf ω;
  convert quotient_core_mun hω ( hn ▸ Fintype.card_pos ) _ hMk ( by omega ) hσ1 hσM using 1;
  · congr! 3;
    congr! 2;
    ext; simp [ω];
    constructor;
    · rintro ⟨ a, ha, rfl ⟩;
      obtain ⟨ k, hk ⟩ := hg₀ ⟨ a, ha ⟩;
      refine' ⟨ Int.toNat ( k % n ), _, _ ⟩;
      · linarith [ Int.emod_nonneg k ( by linarith [ show 0 < n from hn ▸ Fintype.card_pos ] : ( n : ℤ ) ≠ 0 ), Int.emod_lt_of_pos k ( by linarith [ show 0 < n from hn ▸ Fintype.card_pos ] : ( n : ℤ ) > 0 ), Int.toNat_of_nonneg ( Int.emod_nonneg k ( by linarith [ show 0 < n from hn ▸ Fintype.card_pos ] : ( n : ℤ ) ≠ 0 ) ) ];
      · have h_exp : (g₀ : Fˣ) ^ k = (g₀ : Fˣ) ^ (k % n) := by
          rw [ ← Int.emod_add_mul_ediv k n, zpow_add, zpow_mul ] ; norm_cast ; simp +decide;
          simp +decide [ ← hn ];
        convert congr_arg Subtype.val hk using 1;
        simp +decide [ ← Units.val_inj, h_exp ];
        rw [ ← zpow_natCast, Int.toNat_of_nonneg ( Int.emod_nonneg _ ( by linarith [ show n > 0 from hn ▸ Fintype.card_pos ] ) ) ];
    · rintro ⟨ a, ha, rfl ⟩;
      exact ⟨ g₀ ^ a, by exact Subgroup.pow_mem _ g₀.2 _, by simp +decide ⟩;
  · rw [ Nat.div_mul_cancel ];
    have := Subgroup.card_dvd_of_le hKH; aesop;

/-! ### Locator fibers and exact image fibers (`prop:arb-fiber`, `prop:imgfib-list`) -/

/-
If `P` agrees with `U` on `S` and `deg P < |S|`, then the residue `U mod L_S` equals `P`.
This is the algebraic heart of the fiber correspondence: agreement on `S` is congruence mod
`L_S`, and a degree bound pins down the residue.
-/
lemma modByMonic_locator_eq {U P : F[X]} {S : Finset F} (hdeg : P.degree < (S.card : ℕ))
    (hagree : ∀ x ∈ S, U.eval x = P.eval x) : U %ₘ locator S = P := by
  -- Since $P$ agree with $U$ on $S$, we have $U \equiv P \pmod{L_S}$.
  have h_cong : U %ₘ (locator S) = P %ₘ (locator S) := by
    have hcong : (U - P) %ₘ (locator S) = 0 := by
      -- Since $U - P$ has roots at every element of $S$, it is divisible by the locator polynomial $L_S$.
      have h_div : ∏ x ∈ S, (Polynomial.X - Polynomial.C x) ∣ (U - P) := by
        refine' Finset.prod_dvd_of_coprime _ _;
        · exact fun x hx y hy hxy => Polynomial.irreducible_X_sub_C _ |> fun h => h.coprime_iff_not_dvd.mpr fun h' => hxy <| by simpa [ sub_eq_iff_eq_add ] using Polynomial.dvd_iff_isRoot.mp h';
        · exact fun x hx => Polynomial.dvd_iff_isRoot.mpr ( by simp +decide [ hagree x hx ] );
      convert Polynomial.modByMonic_eq_zero_iff_dvd _ |>.2 h_div;
      exact Polynomial.monic_prod_of_monic _ _ fun x hx => Polynomial.monic_X_sub_C x;
    simp_all +decide [ sub_eq_iff_eq_add, Polynomial.sub_modByMonic ];
  convert Polynomial.modByMonic_eq_self_iff _ |>.2 _;
  · infer_instance;
  · exact locator_monic S;
  · rw [ locator ];
    rw [ Polynomial.degree_prod, Finset.sum_congr rfl fun x hx => Polynomial.degree_X_sub_C _ ] ; aesop

open Classical in
/-- The **locator fiber** `Fib_U(s) = {S ⊆ H : |S| = s, deg(U mod L_S) < k}`
(`def:locator-fiber`). -/
def Fib (U : F[X]) (H : Finset F) (k s : ℕ) : Finset (Finset F) :=
  (H.powersetCard s).filter (fun S => (U %ₘ locator S).degree < (k : ℕ))

open Classical in
/-- The **codeword-image fiber** `ImgFib_U(s) = {U mod L_S : S ∈ Fib_U(s)}`
(`def:locator-fiber`). -/
def ImgFib (U : F[X]) (H : Finset F) (k s : ℕ) : Finset F[X] :=
  (Fib U H k s).image (fun S => U %ₘ locator S)

lemma mem_Fib {U : F[X]} {H : Finset F} {k s : ℕ} {S : Finset F} :
    S ∈ Fib U H k s ↔ S ⊆ H ∧ S.card = s ∧ (U %ₘ locator S).degree < (k : ℕ) := by
  classical
  simp [Fib, Finset.mem_filter, Finset.mem_powersetCard, and_assoc]

/-
**Image fibers are exact lists (`prop:imgfib-list`).**  The codeword-image fiber
`ImgFib_U(s)` is exactly the decoding list of degree-`< k` codewords agreeing with `U` on at
least `s` points of `H`.
-/
theorem imgFib_coe_eq_codeList [DecidableEq F] (U : F[X]) (H : Finset F) {k s : ℕ} (hk : k < s) :
    (↑(ImgFib U H k s) : Set F[X]) = codeList U H k s := by
  ext P;
  constructor <;> intro hP;
  · obtain ⟨S, hS⟩ : ∃ S ∈ Fib U H k s, P = U %ₘ locator S := by
      unfold ImgFib at hP; aesop;
    refine' ⟨ _, _ ⟩;
    · exact hS.2 ▸ by simpa using Finset.mem_filter.mp hS.1 |>.2;
    · refine' le_trans _ ( Finset.card_mono <| show S ⊆ agreeSet U P H from _ );
      · rw [ mem_Fib ] at hS ; aesop;
      · intro x hx; simp_all +decide [ agreeSet ] ;
        have := Polynomial.modByMonic_add_div U ( locator_monic S ) ; replace := congr_arg ( Polynomial.eval x ) this; simp_all +decide [ eval_locator_mem ] ;
        exact Finset.mem_powersetCard.mp ( Finset.mem_filter.mp hS.1 |>.1 ) |>.1 hx;
  · -- Choose `S ⊆ agreeSet U P H` with `S.card = s`.
    obtain ⟨S, hScard, hS⟩ : ∃ S : Finset F, S ⊆ agreeSet U P H ∧ S.card = s := by
      exact Finset.exists_subset_card_eq ( by simpa using hP.2 );
    have hP_eq : U %ₘ locator S = P := by
      apply modByMonic_locator_eq;
      · exact lt_of_lt_of_le hP.1 ( WithBot.coe_le_coe.mpr ( by linarith ) );
      · exact fun x hx => Eq.symm ( Finset.mem_filter.mp ( hScard hx ) |>.2 );
    grind +locals

/-
**Arbitrary-word fiber upper bound (`prop:arb-fiber`).**  The decoding list is no larger
than the locator fiber.
-/
theorem arb_fiber_upper [DecidableEq F] (U : F[X]) (H : Finset F) {k s : ℕ} (hk : k < s) :
    (codeList U H k s).ncard ≤ (Fib U H k s).card := by
  rw [ ← imgFib_coe_eq_codeList U H hk, Set.ncard_coe_finset ];
  convert Finset.card_image_le

/-
The fiber of `S ↦ U mod L_S` over a codeword `P ∈ ImgFib_U(s)` consists exactly of the
`s`-subsets of the agreement set of `P` with `U`.
-/
lemma Fib_fiber_eq_powersetCard [DecidableEq F] (U : F[X]) (H : Finset F) {k s : ℕ} (hk : k < s)
    {P : F[X]} (hP : P ∈ ImgFib U H k s) :
    {S ∈ Fib U H k s | U %ₘ locator S = P} = (agreeSet U P H).powersetCard s := by
  ext S;
  constructor;
  · simp +contextual [ Finset.mem_filter, mem_Fib ];
    intro hS hS' hS'' hS''' x hx
    have h_eval : U.eval x = P.eval x := by
      rw [ ← hS''', Polynomial.modByMonic_eq_sub_mul_div _ ( locator_monic S ) ] ; simp +decide [ eval_locator_mem hx ];
    exact Finset.mem_filter.mpr ⟨ hS hx, h_eval.symm ⟩;
  · simp_all +decide [ Finset.subset_iff, Finset.mem_powersetCard, Finset.mem_filter ];
    intro hS hsS
    have hP_deg : P.degree < k := by
      grind +locals
    have hP_mod : U %ₘ locator S = P := by
      apply modByMonic_locator_eq;
      · exact hP_deg.trans_le ( mod_cast hsS.symm ▸ mod_cast hk.le );
      · exact fun x hx => Finset.mem_filter.mp ( hS hx ) |>.2.symm
    exact ⟨by
    grind +locals, hP_mod⟩

/-
**Locator-fiber count (`prop:imgfib-list`, count identity).**  The size of the locator
fiber is the sum over the list of `C(a_P, s)`, where `a_P` is the number of agreement points
of the codeword `P` with `U`.
-/
theorem Fib_card_eq_sum [DecidableEq F] (U : F[X]) (H : Finset F) {k s : ℕ} (hk : k < s) :
    (Fib U H k s).card = ∑ P ∈ ImgFib U H k s, (agreeSet U P H).card.choose s := by
  have h_card : ∀ P ∈ ImgFib U H k s, Finset.card (Finset.filter (fun S => U %ₘ locator S = P) (Fib U H k s)) = Nat.choose (Finset.card (agreeSet U P H)) s := by
    intro P hP
    rw [Fib_fiber_eq_powersetCard U H hk hP];
    rw [ Finset.card_powersetCard ];
  rw [ ← Finset.sum_congr rfl h_card, Finset.card_eq_sum_ones ];
  simp +decide only [card_eq_sum_ones];
  rw [ ← Finset.sum_biUnion ];
  · congr with x ; simp +decide [ ImgFib ];
    exact fun hx => ⟨ x, hx, rfl ⟩;
  · exact fun x hx y hy hxy => Finset.disjoint_left.mpr fun z hz hz' => hxy <| by aesop;

/-! ### The generated-field pigeonhole (`cor:genfield-pigeonhole`) -/

/-
The coefficients of the locator of a set contained in a subfield `B` lie in `B`.
-/
lemma locator_coeff_mem_subfield {B : Subfield F} {S : Finset F} (hS : ∀ x ∈ S, x ∈ B)
    (i : ℕ) : (locator S).coeff i ∈ B := by
  -- Each factor $(X - C x)$ has all coefficients in $B$ (coeff 1 is $1 \in B$, coeff 0 is $-x \in B$ since $x \in B$, others $0 \in B$).
  have h_factor : ∀ x ∈ S, (Polynomial.X - Polynomial.C x) ∈ Polynomial.lifts (B.subtype) := by
    intro x hx; use Polynomial.X - Polynomial.C ⟨ x, hS x hx ⟩ ; simp +decide ;
  -- The product of polynomials in $B[X]$ is also in $B[X]$.
  have h_prod_lifts : ∀ (S : Finset F), (∀ x ∈ S, (Polynomial.X - Polynomial.C x) ∈ Polynomial.lifts (B.subtype)) → (∏ x ∈ S, (Polynomial.X - Polynomial.C x)) ∈ Polynomial.lifts (B.subtype) := by
    exact fun S a => Subsemiring.prod_mem (lifts B.subtype) a;
  obtain ⟨ p, hp ⟩ := h_prod_lifts S h_factor;
  replace hp := congr_arg ( fun q => Polynomial.coeff q i ) hp ; simp_all +decide [ Polynomial.coeff_map ] ;
  exact hp ▸ Subtype.mem _

/-
The elementary-symmetric prefix of a set contained in a subfield `B` takes values in `B`.
-/
lemma esymPrefix_mem_subfield {B : Subfield F} {σ : ℕ} {S : Finset F} (hS : ∀ x ∈ S, x ∈ B)
    (j : Fin σ) : esymPrefix σ S j ∈ B := by
  exact locator_coeff_mem_subfield hS _

/-
**Generated-field pigeonhole (`cor:genfield-pigeonhole`).**  If the evaluation set `H` is
contained in a subfield `B` of size `q_D`, some monomial-prefix word with coefficients in `B`
has decoding list of size at least `q_D^{-σ} · C(|H|, s)`.
-/
theorem genfield_pigeonhole [Fintype F] [DecidableEq F] {H : Finset F} (B : Subfield F) [Fintype B]
    (hHB : ∀ x ∈ H, x ∈ B) {s σ k : ℕ}
    (hσ : 1 ≤ σ) (hσs : σ ≤ s) (hsH : s ≤ H.card) (hk : k = s - σ) :
    ∃ c : Fin σ → F, (∀ j, c j ∈ B) ∧
      (H.card.choose s : ℝ)
        ≤ (Fintype.card B : ℝ) ^ σ * (codeList (Uc s σ c) H k s).ncard := by
  have h_prefixes_card : (Finset.image (fun S : Finset F => esymPrefix σ S) (Finset.powersetCard s H)).card ≤ (Fintype.card B) ^ σ := by
    refine' le_trans ( Finset.card_le_card <| Finset.image_subset_iff.mpr _ ) _;
    exact Finset.image ( fun f : Fin σ → B => fun i => f i ) Finset.univ;
    · simp +decide;
      exact fun S hS hs => ⟨ fun i => ⟨ esymPrefix σ S i, esymPrefix_mem_subfield ( fun x hx => hHB x ( hS hx ) ) i ⟩, rfl ⟩;
    · exact Finset.card_image_le.trans ( by simp +decide [ Finset.card_univ ] );
  obtain ⟨c, hc⟩ : ∃ c ∈ Finset.image (fun S : Finset F => esymPrefix σ S) (Finset.powersetCard s H), ((Finset.filter (fun S : Finset F => esymPrefix σ S = c) (Finset.powersetCard s H)).card : ℝ) ≥ (H.card.choose s : ℝ) / (Fintype.card B) ^ σ := by
    have h_pigeonhole : ∑ c ∈ Finset.image (fun S : Finset F => esymPrefix σ S) (Finset.powersetCard s H), (Finset.filter (fun S : Finset F => esymPrefix σ S = c) (Finset.powersetCard s H)).card = (H.card.choose s : ℕ) := by
      rw [ ← Finset.card_eq_sum_card_fiberwise ];
      · rw [ Finset.card_powersetCard ];
      · exact fun x hx => Finset.mem_image_of_mem _ hx;
    contrapose! h_pigeonhole;
    rw [ ne_eq, ← @Nat.cast_inj ℝ ] ; push_cast ; refine' ne_of_lt ( lt_of_lt_of_le ( Finset.sum_lt_sum_of_nonempty _ h_pigeonhole ) _ );
    · obtain ⟨ S, hS ⟩ := Finset.card_pos.mp ( by rw [ Finset.card_powersetCard ] ; exact Nat.choose_pos hsH ) ; exact ⟨ _, Finset.mem_image_of_mem _ hS ⟩ ;
    · simp +decide [ div_eq_mul_inv ];
      rw [ ← div_eq_mul_inv, mul_div, div_le_iff₀ ] <;> norm_cast <;> nlinarith [ pow_pos ( Fintype.card_pos : 0 < Fintype.card B ) σ, Nat.choose_pos hsH ];
  refine' ⟨ c, _, _ ⟩;
  · simp +zetaDelta at *;
    rcases hc.1 with ⟨ S, ⟨ hS₁, hS₂ ⟩, rfl ⟩ ; exact fun j => esymPrefix_mem_subfield ( fun x hx => hHB x ( hS₁ hx ) ) j;
  · have h_card_image : (Finset.image (fun S : Finset F => PS s σ c S) (Finset.filter (fun S : Finset F => esymPrefix σ S = c) (Finset.powersetCard s H))).card ≤ (codeList (Uc s σ c) H k s).ncard := by
      rw [ ← Set.ncard_coe_finset ];
      apply Set.ncard_le_ncard;
      · simp +decide [ Set.subset_def ];
        rintro _ S hSH hScard hΦ rfl; exact PS_mem_codeList hσ hσs hk hScard hΦ hSH;
      · exact codeList_finite (Uc s σ c) H k s;
    rw [ ge_iff_le, div_le_iff₀ ] at hc <;> norm_cast at *;
    · rw [ Finset.card_image_of_injective _ ( PS_injOn c ) ] at h_card_image ; nlinarith;
    · exact pow_pos ( Fintype.card_pos ) _

/-! ### The characteristic-zero inverse quotient theorem (`thm:upstairs`)

The engine `antipodal` (proved above) is upgraded, by a dyadic induction, to the statement
that a signed function `h` supported on the `2^m`-th roots of unity whose weighted power sums
`∑ h(x) x^j` vanish for `1 ≤ j ≤ σ` is invariant under multiplication by `2^a`-th roots of
unity, for any `a` with `2^{a-1} ≤ σ`.  Taking `2^a = M_0` (least power of two `> σ`) recovers
the inverse quotient theorem. -/

/-
Raising a `2^m`-th root of unity to the `2^i` power lands in the `2^{m-i}`-th roots.
-/
lemma pow_mem_nthRoots_of_le {m i : ℕ} (hi : i ≤ m) {x : ℂ} (hx : x ^ (2 ^ m) = 1) :
    (x ^ (2 ^ i)) ^ (2 ^ (m - i)) = 1 := by
  rw [ ← pow_mul, ← pow_add, add_tsub_cancel_of_le hi, hx ]

/-- Membership in the (finset of) `n`-th roots of unity. -/
lemma mem_nthRoots_iff {n : ℕ} (hn : 0 < n) {x : ℂ} :
    x ∈ (Polynomial.nthRoots n (1 : ℂ)).toFinset ↔ x ^ n = 1 := by
  rw [Multiset.mem_toFinset, Polynomial.mem_nthRoots hn]

/-
There are exactly `n` complex `n`-th roots of unity.
-/
lemma card_nthRoots_toFinset {n : ℕ} (hn : 0 < n) :
    (Polynomial.nthRoots n (1 : ℂ)).toFinset.card = n := by
  rw [ Multiset.toFinset_card_of_nodup ];
  · rw [ nthRoots ];
    rw [ ← Polynomial.Splits.natDegree_eq_card_roots ];
    · rw [ Polynomial.natDegree_X_pow_sub_C ];
    · exact IsAlgClosed.splits (X ^ n - C 1);
  · refine' ( Polynomial.nodup_roots _ );
    refine' Polynomial.separable_X_pow_sub_C _ _ _ <;> norm_num [ hn.ne' ]

/-
**Fiber constancy.**  Over the `μ_{2^i}`-invariant `h`, the fiber of `x ↦ x^(2^i)` above
`z^(2^i)` (inside the `2^m`-th roots) is the `μ_{2^i}`-coset of `z`, and the `h`-sum over it is
`2^i · h z`.
-/
lemma fiber_h_sum {m i : ℕ} (hi : i ≤ m) (h : ℂ → ℤ)
    (hinv : ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ i) = 1 → h (κ * x) = h x)
    {z : ℂ} (hz : z ^ (2 ^ m) = 1) :
    ∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun x => x ^ (2 ^ i) = z ^ (2 ^ i)),
        h x = 2 ^ i * h z := by
  -- The filtered fiber equals `Ri.image (·*z)` (see ` lintsum笺 footnote 12` supplement).
  have h_filter : ((Polynomial.nthRoots (2 ^ m) 1).toFinset).filter (fun x => x ^ (2 ^ i) = z ^ (2 ^ i)) = ((Polynomial.nthRoots (2 ^ i) 1).toFinset.image (fun x => x * z)) := by
    ext x;
    constructor;
    · simp +decide;
      intro hx hx'; use x / z; simp_all +decide [ div_pow ] ;
      exact ⟨ by rintro rfl; simp_all +decide [ zero_pow ], div_mul_cancel₀ _ ( by rintro rfl; simp_all +decide [ zero_pow ] ) ⟩;
    · simp +zetaDelta at *;
      rintro y hy rfl; simp_all +decide [ mul_pow ] ;
      rw [ ← Nat.mul_div_cancel' ( pow_dvd_pow _ hi ), pow_mul, hy, one_pow ];
  convert Finset.sum_image ?_ using 2;
  · rw [ Finset.sum_congr rfl fun x hx => hinv _ _ _ _ ];
    · norm_num [ card_nthRoots_toFinset ];
    · grind;
    · simp +decide;
  · intro x hx y hy; aesop;

/-
**One dyadic step.**  If `h` (supported on `μ_{2^m}`) is invariant under `μ_{2^i}` and its
`2^i`-th weighted power sum vanishes, then `h` is invariant under `μ_{2^{i+1}}`.
-/
lemma antipodal_step {m i : ℕ} (hi : i < m) (h : ℂ → ℤ)
    (hinv : ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ i) = 1 → h (κ * x) = h x)
    (hvan : ∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset, (h x : ℂ) * x ^ (2 ^ i) = 0) :
    ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ (i + 1)) = 1 → h (κ * x) = h x := by
  intros x κ hx hκ
  obtain h_cases | h_cases : κ ^ 2 ^ i = 1 ∨ κ ^ 2 ^ i = -1 := by
    exact eq_or_eq_neg_of_sq_eq_sq _ _ <| by linear_combination' hκ;
  · exact hinv x κ hx h_cases;
  · -- By applying the fiber_h_sum lemma to both x and κ*x, we can derive the required equality.
    have h_fiber_x : ∑ y ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun y => y ^ (2 ^ i) = x ^ (2 ^ i)), h y = 2 ^ i * h x := by
      convert fiber_h_sum hi.le h hinv hx using 1
    have h_fiber_kx : ∑ y ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun y => y ^ (2 ^ i) = (κ * x) ^ (2 ^ i)), h y = 2 ^ i * h (κ * x) := by
      convert fiber_h_sum ( show i ≤ m from hi.le ) h hinv _ using 1;
      rw [ mul_pow, show κ ^ 2 ^ m = ( κ ^ 2 ^ ( i + 1 ) ) ^ ( 2 ^ ( m - ( i + 1 ) ) ) by rw [ ← pow_mul, ← pow_add, Nat.add_sub_of_le ( by linarith ) ], hκ, one_pow, hx, one_mul ];
    -- By applying the antipodal lemma to the function $G$, we get that $G(y) = G(-y)$ for all $y \in Rq$.
    have h_antipodal : ∀ y ∈ (Polynomial.nthRoots (2 ^ (m - i)) (1 : ℂ)).toFinset, (∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun x => x ^ (2 ^ i) = y), h x) = (∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun x => x ^ (2 ^ i) = -y), h x) := by
      have h_antipodal : ∑ y ∈ (Polynomial.nthRoots (2 ^ (m - i)) (1 : ℂ)).toFinset, (∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset.filter (fun x => x ^ (2 ^ i) = y), (h x : ℂ)) * y = 0 := by
        convert hvan using 1;
        simp +decide only [sum_mul _ _ _];
        rw [ Finset.sum_sigma' ];
        refine' Finset.sum_bij ( fun x hx => x.snd ) _ _ _ _ <;> simp +decide;
        · grind +qlia;
        · grind;
        · exact fun x hx => ⟨ by rw [ ← pow_mul, ← pow_add, add_tsub_cancel_of_le hi.le, hx ], hx ⟩;
        · exact fun a ha₁ ha₂ ha₃ => Or.inl ha₃.symm;
      have := antipodal ( show 1 ≤ m - i from Nat.sub_pos_of_lt hi ) ( fun y => ∑ x ∈ ( Polynomial.nthRoots ( 2 ^ m ) 1 |> Multiset.toFinset ) with x ^ 2 ^ i = y, h x ) ?_ <;> simp_all +decide;
    specialize h_antipodal ( x ^ 2 ^ i ) ?_ <;> simp_all +decide [ pow_add, pow_mul ];
    · rw [ ← pow_mul, ← pow_add, add_tsub_cancel_of_le hi.le, hx ];
    · simp_all +decide [ mul_pow ]

/-
**Dyadic vanishing forces quotient invariance.**  If the `2^i`-th weighted power sums of
`h` vanish for all `i < a` (and `a ≤ m`), then `h` is invariant under `μ_{2^a}`.
-/
lemma invariant_of_dyadic_vanish {m : ℕ} (h : ℂ → ℤ)
    (a : ℕ) (ha : a ≤ m)
    (hvan : ∀ i, i < a →
      ∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset, (h x : ℂ) * x ^ (2 ^ i) = 0) :
    ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ a) = 1 → h (κ * x) = h x := by
  induction' a with a ih;
  · grind +extAll;
  · convert antipodal_step ( by linarith : a < m ) h ( ih ( by linarith ) fun i hi => hvan i ( by linarith ) ) ( hvan a ( by linarith ) ) using 1

/-
**Inverse quotient theorem, power-sum form.**  Let `h` be supported on the `2^m`-th roots
of unity and suppose its weighted power sums `∑ h(x) x^j` vanish for `1 ≤ j ≤ σ`.  Then for any
`a ≤ m` with `2^{a-1} ≤ σ`, `h` is invariant under multiplication by `2^a`-th roots of unity.
With `2^a = M_0` the least power of two `> σ`, this is the invariance asserted by
`thm:upstairs`.

The paper's support hypothesis `_hsupp` (that `h` vanishes off the `2^m`-th roots of unity)
is stated for faithfulness but is not needed: the conclusion only concerns points on the
roots of unity, so it is retained under an underscored name. -/
theorem inverse_quotient_psum {m : ℕ} (h : ℂ → ℤ)
    (_hsupp : ∀ x : ℂ, h x ≠ 0 → x ^ (2 ^ m) = 1)
    {σ a : ℕ} (ha : a ≤ m) (hda : 2 ^ (a - 1) ≤ σ)
    (hvan : ∀ j, 1 ≤ j → j ≤ σ →
      ∑ x ∈ (Polynomial.nthRoots (2 ^ m) (1 : ℂ)).toFinset, (h x : ℂ) * x ^ j = 0) :
    ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ a) = 1 → h (κ * x) = h x := by
  convert invariant_of_dyadic_vanish h a ha _ using 1;
  exact fun i hi => hvan _ ( Nat.one_le_pow _ _ ( by decide ) ) ( le_trans ( pow_le_pow_right₀ ( by decide ) ( Nat.le_sub_one_of_lt hi ) ) hda )

/-
**Newton's identity** for a finite set of complex numbers: the `k`-th elementary symmetric
function is expressed through lower ones and the power sums.  (Specialization of
`MvPolynomial.mul_esymm_eq_sum` along the evaluation at the elements of `S`.)
-/
lemma newton_finset (S : Finset ℂ) (k : ℕ) :
    (k : ℂ) * S.val.esymm k =
      (-1) ^ (k + 1) * ∑ a ∈ (Finset.antidiagonal k).filter (fun a => a.1 < k),
        (-1) ^ a.1 * S.val.esymm a.1 * ∑ x ∈ S, x ^ a.2 := by
  convert MvPolynomial.mul_esymm_eq_sum ( Fin S.card ) ℂ k using 1;
  -- By definition of `MvPolynomial.esymm`, we know that `MvPolynomial.esymm (Fin S.card) ℂ k` is equal to `S.val.esymm k`.
  have h_esymm : ∀ k, MvPolynomial.aeval (fun i => (S.equivFin.symm i : ℂ)) (MvPolynomial.esymm (Fin S.card) ℂ k) = S.val.esymm k := by
    intro k; erw [ MvPolynomial.aeval_esymm_eq_multiset_esymm ] ;
    convert rfl;
    refine' Multiset.eq_of_le_of_card_le ( Multiset.le_iff_count.mpr _ ) _;
    · intro x; by_cases hx : x ∈ S <;> simp_all +decide ;
      rw [ List.count_eq_one_of_mem ];
      · exact Multiset.nodup_iff_count_le_one.mp ( Finset.nodup _ ) x;
      · rw [ List.nodup_ofFn ];
        exact fun i j hij => by simpa [ Fin.ext_iff ] using S.equivFin.symm.injective ( Subtype.ext hij ) ;
      · rw [ List.mem_ofFn ];
        exact ⟨ S.equivFin ⟨ x, hx ⟩, by simp +decide ⟩;
    · simp +decide;
  have h_psum : ∀ p, MvPolynomial.aeval (fun i => (S.equivFin.symm i : ℂ)) (MvPolynomial.psum (Fin S.card) ℂ p) = ∑ x ∈ S, x ^ p := by
    intro p
    simp [MvPolynomial.psum];
    conv_rhs => rw [ ← Finset.sum_coe_sort ] ;
    conv_rhs => rw [ ← Equiv.sum_comp ( S.equivFin.symm ) ] ;
  convert Iff.rfl using 2 ; push_cast [ ← h_esymm, ← h_psum ] ; ring;
  constructor <;> intro h <;> simp_all +decide [ MvPolynomial.aeval_def ];
  · convert congr_arg ( MvPolynomial.aeval ( fun i => ( S.equivFin.symm i : ℂ ) ) ) h using 1 <;> simp +decide [ h_esymm, h_psum ];
  · convert MvPolynomial.mul_esymm_eq_sum ( Fin S.card ) ℂ k using 1;
    grind

/-
**Power sums from symmetric functions.**  If two finite sets of complex numbers have equal
elementary symmetric functions `e_1, …, e_σ`, then they have equal power sums `p_1, …, p_σ`.
(By Newton's identities in characteristic zero; the cardinalities need not agree.)
-/
lemma psum_eq_of_esymm_eq {S T : Finset ℂ} {σ : ℕ}
    (he : ∀ j, 1 ≤ j → j ≤ σ → S.val.esymm j = T.val.esymm j) :
    ∀ j, 1 ≤ j → j ≤ σ → ∑ x ∈ S, x ^ j = ∑ x ∈ T, x ^ j := by
  intro j hj hj'; induction' j using Nat.strongRecOn with j ih;
  -- Apply Newton's identities to both sets to get the relation between the power sums and elementary symmetric functions.
  have h_newton_S := newton_finset S j
  have h_newton_T := newton_finset T j;
  -- Split the sum into the term where $a.1 = 0$ and the rest.
  have h_split_sum : ∑ a ∈ (Finset.antidiagonal j).filter (fun a => a.1 < j), (-1) ^ a.1 * S.val.esymm a.1 * ∑ x ∈ S, x ^ a.2 = (∑ x ∈ S, x ^ j) + ∑ a ∈ (Finset.antidiagonal j |>.filter (fun a => 1 ≤ a.1 ∧ a.1 < j)), (-1) ^ a.1 * S.val.esymm a.1 * ∑ x ∈ S, x ^ a.2 := by
    rw [ Finset.sum_eq_add_sum_diff_singleton <| show ( 0, j ) ∈ Finset.filter ( fun a => a.1 < j ) ( Finset.antidiagonal j ) from Finset.mem_filter.mpr ⟨ Finset.mem_antidiagonal.mpr <| by norm_num, by linarith ⟩ ];
    congr! 1;
    · norm_num [ Multiset.esymm ];
    · refine' Finset.sum_bij ( fun x hx => x ) _ _ _ _ <;> simp +contextual;
      · exact fun a b hab ha hb => Nat.pos_of_ne_zero fun ha' => hb ha' ( by linarith );
      · intros; linarith;
  have h_split_sum_T : ∑ a ∈ (Finset.antidiagonal j).filter (fun a => a.1 < j), (-1) ^ a.1 * T.val.esymm a.1 * ∑ x ∈ T, x ^ a.2 = (∑ x ∈ T, x ^ j) + ∑ a ∈ (Finset.antidiagonal j |>.filter (fun a => 1 ≤ a.1 ∧ a.1 < j)), (-1) ^ a.1 * T.val.esymm a.1 * ∑ x ∈ T, x ^ a.2 := by
    rw [ Finset.sum_eq_add_sum_diff_singleton <| show ( 0, j ) ∈ Finset.filter ( fun a => a.1 < j ) ( Finset.antidiagonal j ) from Finset.mem_filter.mpr ⟨ Finset.mem_antidiagonal.mpr <| by norm_num, by linarith ⟩ ];
    congr 1;
    · norm_num [ Multiset.esymm ];
    · refine' Finset.sum_bij ( fun x hx => x ) _ _ _ _ <;> simp +contextual;
      · grobner;
      · intros; linarith;
  -- Apply the induction hypothesis to the remaining terms in the sum.
  have h_ind : ∑ a ∈ (Finset.antidiagonal j |>.filter (fun a => 1 ≤ a.1 ∧ a.1 < j)), (-1) ^ a.1 * S.val.esymm a.1 * ∑ x ∈ S, x ^ a.2 = ∑ a ∈ (Finset.antidiagonal j |>.filter (fun a => 1 ≤ a.1 ∧ a.1 < j)), (-1) ^ a.1 * T.val.esymm a.1 * ∑ x ∈ T, x ^ a.2 := by
    refine' Finset.sum_congr rfl fun x hx => _;
    simp +zetaDelta at *;
    rw [ he x.1 hx.2.1 ( by linarith ), ih x.2 ( by linarith ) ( by linarith ) ( by linarith ) ];
  simp_all +decide [ pow_succ' ]

/-
**Inverse quotient theorem over `ℂ` (`thm:upstairs`).**  Let `S, T ⊆ μ_{2^m}` have equal
elementary symmetric functions `e_1, …, e_σ`.  Then for any `a ≤ m` with `2^{a-1} ≤ σ` (in
particular for `2^a = M_0`, the least power of two `> σ`), the indicator difference
`𝟙_S - 𝟙_T` is invariant under multiplication by `2^a`-th roots of unity, i.e. `S △ T` is a
union of `μ_{M_0}`-cosets.  (The paper's hypothesis `|S| = |T|` is not needed for this
conclusion.)
-/
theorem inverse_quotient {m : ℕ} {S T : Finset ℂ}
    (hS : ∀ x ∈ S, x ^ (2 ^ m) = 1) (hT : ∀ x ∈ T, x ^ (2 ^ m) = 1)
    {σ a : ℕ} (ha : a ≤ m) (hda : 2 ^ (a - 1) ≤ σ)
    (he : ∀ j, 1 ≤ j → j ≤ σ → S.val.esymm j = T.val.esymm j) :
    ∀ x κ : ℂ, x ^ (2 ^ m) = 1 → κ ^ (2 ^ a) = 1 →
      ((if κ * x ∈ S then (1 : ℤ) else 0) - (if κ * x ∈ T then 1 else 0))
        = ((if x ∈ S then (1 : ℤ) else 0) - (if x ∈ T then 1 else 0)) := by
  -- Apply the inverse quotient theorem with the given hypotheses.
  apply inverse_quotient_psum (fun y => (if y ∈ S then 1 else 0) - (if y ∈ T then 1 else 0)) (fun y hy => by
    grind) ha hda (fun j hj hj' => by
    convert sub_eq_zero.mpr ( psum_eq_of_esymm_eq he j hj hj' ) using 1;
    simp +decide [ sub_mul ];
    rcongr x <;> aesop)

end Chojecki

end