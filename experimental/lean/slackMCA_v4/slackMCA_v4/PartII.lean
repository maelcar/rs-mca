import slackMCA_v4.Main

/-!
# Part II: the slack mutual-correlated-agreement (MCA) spine

This file formalizes unconditional finitary results from Part II of Chojecki's paper:

* `Chojecki.rigid_cyclo` — cyclotomic rigidity (`thm:rigidcyclo`): a subset of `μ_{2^s}` with
  vanishing power sum `p_1` is a union of antipodal pairs;
* `Chojecki.signed_binary_zero` — the signed-binary digit-uniqueness lemma underlying the
  Fermat-field digit rigidity (`thm:rigidfermat`);
* `Chojecki.rigid_fermat` — Fermat-field digit rigidity (`thm:rigidfermat`): a subset of the
  cyclic group `⟨2⟩ = {±2^j : 0 ≤ j < M} ≤ 𝔽_pˣ` (`p = 2^M+1` a Fermat prime) with vanishing
  sum in `𝔽_p` is a union of antipodal pairs;
* `Chojecki.mca_onez` — one bad parameter per support (`thm:onez`): for any linear code, any
  line, and any fixed witness set, at most one line parameter is support-wise MCA-bad.
-/

open Polynomial Finset BigOperators

noncomputable section

namespace Chojecki

/-! ### Cyclotomic rigidity (`thm:rigidcyclo`) -/

/-
**Cyclotomic rigidity (`thm:rigidcyclo`).**  If `A ⊆ μ_{2^s}` (with `s ≥ 1`) has vanishing
first power sum `∑_{a ∈ A} a = 0`, then `A` is a union of antipodal pairs: `x ∈ A → -x ∈ A`.
This is the indicator specialization of the antipodal identity `Chojecki.antipodal`.
-/
theorem rigid_cyclo {s : ℕ} (hs : 1 ≤ s) {A : Finset ℂ}
    (hA : ∀ x ∈ A, x ^ (2 ^ s) = 1) (hsum : ∑ x ∈ A, x = 0) :
    ∀ x ∈ A, -x ∈ A := by
  have h_antipodal : ∀ y ∈ (Polynomial.nthRoots (2 ^ s) (1 : ℂ)).toFinset, (if y ∈ A then (1 : ℤ) else 0) = (if -y ∈ A then (1 : ℤ) else 0) := by
    convert antipodal hs ( fun y => if y ∈ A then ( 1 : ℤ ) else 0 ) _ using 1;
    rw [ ← Finset.sum_subset ( show A ⊆ ( Polynomial.nthRoots ( 2 ^ s ) 1 |> Multiset.toFinset ) from fun x hx => by aesop ) ] ; aesop;
    aesop;
  grind +suggestions

/-! ### Signed-binary digit uniqueness (underlying `thm:rigidfermat`) -/

/-
**Signed-binary digit uniqueness.**  If `c : ℕ → ℤ` has all digits in `{-1, 0, 1}`, is
supported on `[0, M)`, and `∑_{j < M} c j · 2^j = 0`, then every digit vanishes.  This is the
integer core of the Fermat-field digit rigidity theorem `thm:rigidfermat`.
-/
theorem signed_binary_zero {M : ℕ} (c : ℕ → ℤ)
    (hc : ∀ j, c j = -1 ∨ c j = 0 ∨ c j = 1)
    (h : ∑ j ∈ Finset.range M, c j * 2 ^ j = 0) :
    ∀ j < M, c j = 0 := by
  induction' M with M ih <;> simp_all +decide [ Finset.sum_range_succ ];
  -- From the hypothesis h, we can deduce that $c M = 0$.
  have hcM : c M = 0 := by
    rcases hc M with ( hM | hM | hM ) <;> simp_all +decide [ add_eq_zero_iff_eq_neg ];
    · have h_sum_bound : ∑ j ∈ Finset.range M, c j * 2 ^ j ≤ ∑ j ∈ Finset.range M, 2 ^ j := by
        exact Finset.sum_le_sum fun i hi => by rcases hc i with ( H | H | H ) <;> rw [ H ] <;> norm_num;
      linarith [ geom_sum_mul_neg ( 2 : ℤ ) M, pow_pos ( zero_lt_two' ℤ ) M ];
    · have h_sum_bound : ∑ j ∈ Finset.range M, c j * 2 ^ j ≥ -∑ j ∈ Finset.range M, 2 ^ j := by
        rw [ ← Finset.sum_neg_distrib ] ; exact Finset.sum_le_sum fun i hi => by rcases hc i with ( H | H | H ) <;> norm_num [ H ] ;
      linarith [ geom_sum_mul_neg ( 2 : ℤ ) M ];
  grind

/-! ### Field-level digit rigidity (`thm:rigidfermat`) -/

/-- In `ZMod (2^M+1)` we have `2^M = -1` (since `2^M = p - 1`). -/
lemma two_pow_eq_neg_one {M : ℕ} : (2 : ZMod (2 ^ M + 1)) ^ M = -1 := by
  have h : ((2 ^ M : ℕ) : ZMod (2 ^ M + 1)) = ((2 ^ M + 1 : ℕ) : ZMod (2 ^ M + 1)) - 1 := by
    push_cast; ring
  rw [ZMod.natCast_self] at h; push_cast at h; simpa using h

/-- For a Fermat prime `p = 2^M+1`, the element `2` has multiplicative order `2M` in `ZMod p`.
The order divides `2M` because `2^{2M} = (2^M)^2 = (-1)^2 = 1`; it equals `2M` because
`M = 2^t` (Fermat exponents are powers of two), so any proper power-of-two order would divide
`M` and force `2^M = 1`, contradicting `2^M = -1`. -/
lemma two_orderOf {M : ℕ} (hM : 1 ≤ M) (hp : Nat.Prime (2 ^ M + 1)) :
    orderOf (2 : ZMod (2 ^ M + 1)) = 2 * M := by
  haveI : Fact (Nat.Prime (2 ^ M + 1)) := ⟨hp⟩
  have h2M2 : 2 ≤ 2 ^ M :=
    calc (2 : ℕ) = 2 ^ 1 := (pow_one 2).symm
      _ ≤ 2 ^ M := Nat.pow_le_pow_right (by norm_num) hM
  haveI : Fact (2 < 2 ^ M + 1) := ⟨by omega⟩
  have hneg : (2 : ZMod (2 ^ M + 1)) ^ M = -1 := two_pow_eq_neg_one
  obtain ⟨t, ht⟩ := Nat.pow_of_pow_add_prime (by norm_num) (by omega) hp
  have h2M : (2 : ZMod (2 ^ M + 1)) ^ (2 * M) = 1 := by rw [mul_comm, pow_mul, hneg]; ring
  have hdvd : orderOf (2 : ZMod (2 ^ M + 1)) ∣ 2 * M := orderOf_dvd_of_pow_eq_one h2M
  have h2Mpow : 2 * M = 2 ^ (t + 1) := by rw [ht]; ring
  rw [h2Mpow] at hdvd
  obtain ⟨s, hs_le, hs⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp hdvd
  have hne : (-1 : ZMod (2 ^ M + 1)) ≠ 1 := ZMod.neg_one_ne_one
  have hs_eq : s = t + 1 := by
    rcases Nat.lt_or_ge s (t + 1) with hlt | hge
    · exfalso
      have hdd : orderOf (2 : ZMod (2 ^ M + 1)) ∣ 2 ^ t := by
        rw [hs]; exact pow_dvd_pow 2 (by omega)
      have hpow : (2 : ZMod (2 ^ M + 1)) ^ (2 ^ t) = 1 := orderOf_dvd_iff_pow_eq_one.mp hdd
      have h1 : (2 : ZMod (2 ^ M + 1)) ^ M = 1 := ht.symm ▸ hpow
      rw [hneg] at h1; exact hne h1
    · omega
  rw [hs, hs_eq, ← h2Mpow]

/-- Powers `2^i` for `i < 2M` are pairwise distinct in `ZMod (2^M+1)` (a Fermat prime), since
`2` has order exactly `2M`. -/
lemma two_pow_injOn {M : ℕ} (hM : 1 ≤ M) (hp : Nat.Prime (2 ^ M + 1))
    {i j : ℕ} (hi : i < 2 * M) (hj : j < 2 * M)
    (h : (2 : ZMod (2 ^ M + 1)) ^ i = 2 ^ j) : i = j := by
  have hinj := pow_injOn_Iio_orderOf (x := (2 : ZMod (2 ^ M + 1)))
  rw [two_orderOf hM hp] at hinj
  exact hinj (by simpa using hi) (by simpa using hj) h

/-- **Digit decomposition of the sum.**  For a Fermat prime `p = 2^M+1` and `A ⊆ {±2^j : j < M}`,
the sum `∑_{a ∈ A} a` splits along the `M` antipodal directions: it equals the sum of the
"positive" powers `2^j ∈ A` plus the "negative" powers `-2^j ∈ A`.  This is the field-side
bookkeeping that lets the signed-binary digit lemma apply. -/
lemma fermat_sum_eq {M : ℕ} (hM : 1 ≤ M) (hp : Nat.Prime (2 ^ M + 1))
    {A : Finset (ZMod (2 ^ M + 1))}
    (hAQ : ∀ a ∈ A, ∃ j < M, a = 2 ^ j ∨ a = -(2 ^ j)) :
    ∑ a ∈ A, a
      = (∑ j ∈ Finset.range M, (if (2 : ZMod (2 ^ M + 1)) ^ j ∈ A then (2 : ZMod (2 ^ M + 1)) ^ j else 0))
        + (∑ j ∈ Finset.range M, (if -(2 : ZMod (2 ^ M + 1)) ^ j ∈ A then -(2 : ZMod (2 ^ M + 1)) ^ j else 0)) := by
  classical
  have neg_one_eq : (-1 : ZMod (2 ^ M + 1)) = 2 ^ M := two_pow_eq_neg_one.symm
  set P := (Finset.range M).filter (fun j => (2 : ZMod (2 ^ M + 1)) ^ j ∈ A) with hP
  set N := (Finset.range M).filter (fun j => -(2 : ZMod (2 ^ M + 1)) ^ j ∈ A) with hN
  have hinjP : Set.InjOn (fun j => (2 : ZMod (2 ^ M + 1)) ^ j) P := by
    intro i hi j hj h
    simp only [hP, Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hi hj
    exact two_pow_injOn hM hp (by omega) (by omega) h
  have hinjN : Set.InjOn (fun j => -(2 : ZMod (2 ^ M + 1)) ^ j) N := by
    intro i hi j hj h
    simp only [hN, Finset.mem_coe, Finset.mem_filter, Finset.mem_range] at hi hj
    have : (2 : ZMod (2 ^ M + 1)) ^ i = 2 ^ j := by simpa using neg_injective h
    exact two_pow_injOn hM hp (by omega) (by omega) this
  set imgP := P.image (fun j => (2 : ZMod (2 ^ M + 1)) ^ j) with himgP
  set imgN := N.image (fun j => -(2 : ZMod (2 ^ M + 1)) ^ j) with himgN
  have hdisj : Disjoint imgP imgN := by
    rw [Finset.disjoint_left]
    intro a haP haN
    simp only [himgP, himgN, Finset.mem_image, hP, hN, Finset.mem_filter, Finset.mem_range] at haP haN
    obtain ⟨i, ⟨hi, _⟩, rfl⟩ := haP
    obtain ⟨j, ⟨hj, _⟩, hij⟩ := haN
    have h2 : (2 : ZMod (2 ^ M + 1)) ^ (M + j) = 2 ^ i := by
      rw [pow_add, ← neg_one_eq, neg_one_mul]; exact hij
    have := two_pow_injOn hM hp (by omega) (by omega) h2
    omega
  have hAeq : A = imgP ∪ imgN := by
    apply Finset.Subset.antisymm
    · intro a ha
      obtain ⟨j, hj, hor⟩ := hAQ a ha
      rcases hor with h | h
      · rw [Finset.mem_union]; left
        simp only [himgP, Finset.mem_image, hP, Finset.mem_filter, Finset.mem_range]
        exact ⟨j, ⟨hj, by rw [← h]; exact ha⟩, h.symm⟩
      · rw [Finset.mem_union]; right
        simp only [himgN, Finset.mem_image, hN, Finset.mem_filter, Finset.mem_range]
        exact ⟨j, ⟨hj, by rw [← h]; exact ha⟩, h.symm⟩
    · intro a ha
      simp only [Finset.mem_union, himgP, himgN, Finset.mem_image, hP, hN, Finset.mem_filter,
        Finset.mem_range] at ha
      rcases ha with ⟨i, ⟨_, hi⟩, rfl⟩ | ⟨j, ⟨_, hj⟩, rfl⟩
      · exact hi
      · exact hj
  conv_lhs => rw [hAeq]
  rw [Finset.sum_union hdisj]
  congr 1
  · rw [himgP, Finset.sum_image hinjP, hP, Finset.sum_filter]
  · rw [himgN, Finset.sum_image hinjN, hN, Finset.sum_filter]

/-
**Digit rigidity on Fermat fields (`thm:rigidfermat`).**  Let `p = 2^M+1` be a Fermat prime and
`Q = ⟨2⟩ = {±2^j : 0 ≤ j < M} ≤ 𝔽_pˣ`.  If `A ⊆ Q` has `∑_{a∈A} a = 0` in `𝔽_p`, then `A` is a
union of antipodal pairs.  The sum lifts to `s = ∑_j c_j 2^j` with digits `c_j ∈ {-1,0,1}` and
`|s| ≤ 2^M - 1 < p`, so `s = 0`; uniqueness of signed-binary representations
(`signed_binary_zero`) forces every digit to vanish, i.e. `2^j ∈ A ↔ -2^j ∈ A`.
-/
theorem rigid_fermat {M : ℕ} (hM : 1 ≤ M) (hp : Nat.Prime (2 ^ M + 1))
    {A : Finset (ZMod (2 ^ M + 1))}
    (hAQ : ∀ a ∈ A, ∃ j < M, a = 2 ^ j ∨ a = -(2 ^ j))
    (hsum : ∑ a ∈ A, a = 0) :
    ∀ x ∈ A, -x ∈ A := by
  classical
  set c : ℕ → ℤ := fun j =>
    (if (2 : ZMod (2 ^ M + 1)) ^ j ∈ A then (1 : ℤ) else 0)
      - (if -(2 : ZMod (2 ^ M + 1)) ^ j ∈ A then 1 else 0) with hc_def
  have hc : ∀ j, c j = -1 ∨ c j = 0 ∨ c j = 1 := by
    intro j; simp only [hc_def]; split_ifs <;> norm_num
  -- The lifted integer sum reduces to `0` in `ZMod p`.
  have hcast : ((∑ j ∈ Finset.range M, c j * 2 ^ j : ℤ) : ZMod (2 ^ M + 1)) = 0 := by
    rw [← hsum, fermat_sum_eq hM hp hAQ]
    push_cast [hc_def]
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro j _
    split_ifs <;> ring
  -- and it is bounded in absolute value by `2^M - 1 < p`.
  have hbound : |∑ j ∈ Finset.range M, c j * 2 ^ j| < (2 ^ M + 1 : ℤ) := by
    calc |∑ j ∈ Finset.range M, c j * 2 ^ j|
        ≤ ∑ j ∈ Finset.range M, |c j * 2 ^ j| := Finset.abs_sum_le_sum_abs _ _
      _ ≤ ∑ j ∈ Finset.range M, (2 : ℤ) ^ j := by
          apply Finset.sum_le_sum
          intro j _
          rw [abs_mul, abs_pow]
          rcases hc j with h | h | h <;> simp [h]
      _ = 2 ^ M - 1 := by simpa using geom_sum_mul (2 : ℤ) M
      _ < 2 ^ M + 1 := by linarith
  -- hence the integer sum is `0`, so all digits vanish.
  have hsum_int : (∑ j ∈ Finset.range M, c j * 2 ^ j : ℤ) = 0 := by
    rw [ZMod.intCast_zmod_eq_zero_iff_dvd] at hcast
    push_cast at hcast
    rcases eq_or_ne (∑ j ∈ Finset.range M, c j * 2 ^ j) 0 with h | h
    · exact h
    · exact absurd (Int.le_of_dvd (abs_pos.mpr h) ((dvd_abs _ _).mpr hcast)) (by linarith)
  have hzero := signed_binary_zero c hc hsum_int
  -- conclude that every antipodal partner of an element of `A` is in `A`.
  intro x hx
  obtain ⟨j, hj, hor⟩ := hAQ x hx
  have hcj : c j = 0 := hzero j hj
  simp only [hc_def] at hcj
  have hind : ((2 : ZMod (2 ^ M + 1)) ^ j ∈ A) ↔ (-(2 : ZMod (2 ^ M + 1)) ^ j ∈ A) := by
    by_cases h1 : (2 : ZMod (2 ^ M + 1)) ^ j ∈ A <;>
      by_cases h2 : -(2 : ZMod (2 ^ M + 1)) ^ j ∈ A <;> simp [h1, h2] at hcj ⊢
  rcases hor with h | h
  · rw [h]; rw [h] at hx; exact hind.mp hx
  · rw [h, neg_neg]; rw [h] at hx; exact hind.mpr hx

/-! ### One bad parameter per support (`thm:onez`) -/

variable {F : Type*} [Field F]

/-- A word `u : F → F` is *explained* by the linear code `C` on the support `S` if some
codeword agrees with `u` on all of `S`. -/
def ExplainedOn (C : Submodule F (F → F)) (S : Finset F) (u : F → F) : Prop :=
  ∃ c ∈ C, ∀ x ∈ S, u x = c x

/-- The parameter `z` is *support-wise MCA-bad with witness `S`* for the line `f + z • g` if the
line value is explained on `S` while the pair `(f, g)` is not both explained on `S`. -/
def MCAbadWitness (C : Submodule F (F → F)) (S : Finset F) (f g : F → F) (z : F) : Prop :=
  ExplainedOn C S (fun x => f x + z * g x) ∧ ¬ (ExplainedOn C S f ∧ ExplainedOn C S g)

/-
**One bad parameter per support (`thm:onez`).**  For any linear code `C`, any line
`f + z • g`, and any fixed witness set `S`, at most one parameter `z` is support-wise MCA-bad
with witness `S`.
-/
theorem mca_onez (C : Submodule F (F → F)) (S : Finset F) (f g : F → F) {z₁ z₂ : F}
    (h₁ : MCAbadWitness C S f g z₁) (h₂ : MCAbadWitness C S f g z₂) : z₁ = z₂ := by
  unfold MCAbadWitness at h₁ h₂;
  obtain ⟨c₁, hc₁⟩ := h₁.left
  obtain ⟨c₂, hc₂⟩ := h₂.left
  have h_diff : ∀ x ∈ S, (z₁ - z₂) * g x = c₁ x - c₂ x := by
    grind;
  by_cases h : z₁ = z₂ <;> simp_all +decide;
  refine' h₂.2 _ _;
  · refine' ⟨ c₁ - ( z₁ • ( ( z₁ - z₂ ) ⁻¹ • ( c₁ - c₂ ) ) ), _, _ ⟩ <;> simp_all +decide [ Submodule.sub_mem_iff_right ];
    · exact C.smul_mem _ ( C.smul_mem _ ( C.sub_mem hc₁.1 hc₂.1 ) );
    · grind;
  · use (z₁ - z₂)⁻¹ • (c₁ - c₂);
    exact ⟨ C.smul_mem _ ( C.sub_mem hc₁.1 hc₂.1 ), fun x hx => by simp +decide [ ← h_diff x hx, sub_ne_zero.2 h ] ⟩

/-! ### The exact slack characterization (`thm:exactslack`) -/

/-- The linear map `P ↦ (x ↦ P.eval x)` from polynomials to words. -/
def evalPi : F[X] →ₗ[F] (F → F) where
  toFun P := fun x => P.eval x
  map_add' P Q := by ext x; simp
  map_smul' a P := by ext x; simp

/-- The **Reed–Solomon code** `RS[F, ·, k]` as the submodule of words `F → F` that are
evaluations of polynomials of degree `< k`. -/
def RScode (k : ℕ) : Submodule F (F → F) := (Polynomial.degreeLT F k).map evalPi

lemma mem_RScode {k : ℕ} {u : F → F} :
    u ∈ RScode k ↔ ∃ P : F[X], P.degree < k ∧ (fun x => P.eval x) = u := by
  simp only [RScode, Submodule.mem_map, Polynomial.mem_degreeLT]; rfl

/-- The degree-`(|S|-j)` coefficient of the locator `L_S` is `(-1)^j · e_j(S)`. -/
lemma locator_coeff_eq_esymm {S : Finset F} {j : ℕ} (hj : j ≤ S.card) :
    (locator S).coeff (S.card - j) = (-1) ^ j * S.val.esymm j := by
  have hloc : locator S = (S.val.map (fun t => X - C t)).prod := by rw [locator, Finset.prod]
  rw [hloc, Multiset.prod_X_sub_C_coeff S.val (Nat.sub_le S.card j)]
  have hc : S.val.card = S.card := rfl
  rw [hc, Nat.sub_sub_self hj]

/-- The **multi-symmetric image** `B_T(D, k)` of `def:badset`: the set of values
`(-1)^T e_T(S)` over `S ⊆ D` of size `k+T` whose lower elementary symmetric functions
`e_1, …, e_{T-1}` all vanish. -/
def BadImage (D : Finset F) (k T : ℕ) : Set F :=
  {z | ∃ S : Finset F, S ⊆ D ∧ S.card = k + T ∧
        (∀ j, 1 ≤ j → j < T → S.val.esymm j = 0) ∧ z = (-1) ^ T * S.val.esymm T}

/-
The monomial `g = x^k` is never explained on a set of more than `k` points (a codeword of
degree `< k` agreeing with `x^k` on `> k` points would force `X^k` to have degree `< k`).
-/
lemma xpow_not_explained {S : Finset F} {k : ℕ} (hcard : k < S.card) :
    ¬ ExplainedOn (RScode k) S (fun x => x ^ k) := by
  rintro ⟨ c, hc, hc' ⟩;
  obtain ⟨ P, hP₁, hP₂ ⟩ := mem_RScode.mp hc;
  -- Let $Q := P - X^k$. For every $x \in S$, $Q.eval x = P.eval x - x^k = 0$.
  set Q : F[X] := P - Polynomial.X ^ k
  have hQ_zero : ∀ x ∈ S, Q.eval x = 0 := by
    aesop;
  -- Since $Q$ is a polynomial of degree at most $k$ and has $k+1$ roots, it must be the zero polynomial.
  have hQ_zero_poly : Q = 0 := by
    refine' Polynomial.eq_zero_of_degree_lt_of_eval_finset_eq_zero S _ _;
    · exact lt_of_le_of_lt ( Polynomial.degree_sub_le _ _ ) ( max_lt ( lt_of_lt_of_le hP₁ ( WithBot.coe_le_coe.mpr hcard.le ) ) ( lt_of_le_of_lt ( Polynomial.degree_X_pow_le _ ) ( WithBot.coe_lt_coe.mpr hcard ) ) );
    · exact hQ_zero;
  rw [ sub_eq_zero ] at hQ_zero_poly ; aesop

/-
**Exact slack characterization (`thm:exactslack`), `⊆` direction.**  Every support-wise
MCA-bad parameter for the canonical line `x^{k+T} + z·x^k` (with a witness of at least `k+T`
points) lies in `B_T(D, k)`.
-/
lemma exact_slack_subset {D : Finset F} {k T : ℕ} (hT : 1 ≤ T) {z : F}
    (hz : ∃ S : Finset F, S ⊆ D ∧ k + T ≤ S.card ∧
      MCAbadWitness (RScode k) S (fun x => x ^ (k + T)) (fun x => x ^ k) z) :
    z ∈ BadImage D k T := by
  obtain ⟨ S, hSD, hcard, hbad ⟩ := hz;
  obtain ⟨c, hc, hc'⟩ := hbad.left
  obtain ⟨R, hR⟩ : ∃ R : F[X], R.degree < k ∧ (fun x => R.eval x) = c := by
    exact mem_RScode.mp hc
  set Pz : F[X] := Polynomial.X ^ (k + T) + Polynomial.C z * Polynomial.X ^ k - R with hPz_def
  have hPz_zero : ∀ x ∈ S, Pz.eval x = 0 := by
    simp_all +decide [ funext_iff ]
  have hPz_deg : Pz.natDegree = S.card := by
    have hPz_deg : Pz.natDegree = k + T := by
      rw [ Polynomial.natDegree_sub_eq_left_of_natDegree_lt ] <;> rw [ Polynomial.natDegree_add_eq_left_of_natDegree_lt ] <;> norm_num;
      · by_cases hz : z = 0 <;> simp +decide [ hz ];
        · exact Or.inr hT;
        · linarith;
      · exact lt_of_le_of_lt ( Polynomial.natDegree_le_of_degree_le hR.1.le ) ( by linarith );
      · by_cases hz : z = 0 <;> simp +decide [ hz ];
        · exact Or.inr hT;
        · linarith;
    refine' le_antisymm _ _;
    · linarith;
    · refine' le_of_not_gt fun h => _;
      have hPz_zero_poly : Pz = 0 := by
        exact Polynomial.eq_zero_of_degree_lt_of_eval_finset_eq_zero S ( lt_of_le_of_lt ( Polynomial.degree_le_natDegree ) ( WithBot.coe_lt_coe.mpr h ) ) hPz_zero;
      simp_all +decide [ sub_eq_iff_eq_add ];
      norm_num [ ← hPz_def ] at hPz_deg;
      linarith
  have hPz_monic : Pz.Monic := by
    rw [ Polynomial.Monic, Polynomial.leadingCoeff_sub_of_degree_lt ];
    · rw [ add_comm, Polynomial.leadingCoeff_add_of_degree_lt ] <;> by_cases h : z = 0 <;> simp +decide [ h ];
      exact WithBot.coe_lt_coe.mpr ( Nat.lt_add_of_pos_right hT );
    · by_cases hz : z = 0 <;> simp_all +decide;
      · exact lt_of_lt_of_le hR.1 ( WithBot.coe_le_coe.mpr ( Nat.le_add_right _ _ ) );
      · rw [ Polynomial.degree_add_eq_left_of_degree_lt ] <;> simp +decide [ hz, Polynomial.degree_C ];
        · exact lt_of_lt_of_le hR.1 ( WithBot.coe_le_coe.mpr ( Nat.le_add_right _ _ ) );
        · exact WithBot.coe_lt_coe.mpr ( Nat.lt_add_of_pos_right hT )
  have hPz_eq_locator : Pz = locator S := by
    refine' Polynomial.eq_of_degree_sub_lt_of_eval_finset_eq S _ _;
    · convert Polynomial.degree_sub_lt _ _ _ <;> norm_num [ hPz_deg, hPz_monic ];
      · rw [ Polynomial.degree_eq_natDegree hPz_monic.ne_zero, hPz_deg ];
      · rw [ Polynomial.degree_eq_natDegree hPz_monic.ne_zero, Polynomial.degree_eq_natDegree ];
        · rw [ hPz_deg, locator_natDegree ];
        · exact Finset.prod_ne_zero_iff.mpr fun x hx => Polynomial.X_sub_C_ne_zero x;
      · aesop;
    · intro x hx; rw [ hPz_zero x hx, eval_locator_mem hx ] ;
  refine' ⟨ S, hSD, _, _, _ ⟩;
  · have hPz_deg_le : Pz.natDegree ≤ k + T := by
      refine' le_trans ( Polynomial.natDegree_sub_le _ _ ) ( max_le _ _ );
      · exact le_trans ( Polynomial.natDegree_add_le _ _ ) ( max_le ( by simp +decide ) ( by by_cases h : z = 0 <;> simp +decide [ h ] ) );
      · exact le_trans ( Polynomial.natDegree_le_of_degree_le hR.1.le ) ( by linarith );
    linarith;
  · intro j hj₁ hj₂
    have h_coeff : Pz.coeff (k + T - j) = 0 := by
      simp +zetaDelta at *;
      rw [ if_neg ( by omega ), if_neg ( by omega ), Polynomial.coeff_eq_zero_of_degree_lt ] ; aesop;
      exact lt_of_lt_of_le hR.1 ( WithBot.coe_le_coe.mpr ( Nat.le_sub_of_add_le ( by linarith ) ) );
    have h_coeff_eq : Pz.coeff (k + T - j) = (-1) ^ j * S.val.esymm j := by
      rw [hPz_eq_locator];
      convert locator_coeff_eq_esymm ( show j ≤ S.card from by linarith ) using 1;
      rw [ show k + T = S.card from _ ];
      refine' le_antisymm hcard ( hPz_deg ▸ _ );
      refine' le_trans ( Polynomial.natDegree_sub_le _ _ ) _ ; simp +decide;
      exact ⟨ le_trans ( Polynomial.natDegree_add_le _ _ ) ( max_le ( by simp +decide ) ( by exact le_trans ( Polynomial.natDegree_C_mul_X_pow_le _ _ ) ( by linarith ) ) ), le_trans ( Polynomial.natDegree_le_of_degree_le hR.1.le ) ( by linarith ) ⟩;
    aesop;
  · convert congr_arg ( fun p => p.coeff k ) hPz_eq_locator using 1;
    · simp +zetaDelta at *;
      rw [ Polynomial.coeff_eq_zero_of_degree_lt hR.1 ] ; aesop;
    · convert locator_coeff_eq_esymm ( show T ≤ S.card from by linarith ) |> Eq.symm using 1;
      rw [ ← hPz_deg, Polynomial.natDegree_sub_eq_left_of_natDegree_lt ] <;> rw [ Polynomial.natDegree_add_eq_left_of_natDegree_lt ] <;> norm_num;
      · by_cases hz : z = 0 <;> simp +decide [ hz ];
        · exact Or.inr hT;
        · linarith;
      · exact lt_of_le_of_lt ( Polynomial.natDegree_le_of_degree_le hR.1.le ) ( Nat.lt_add_of_pos_right hT );
      · by_cases hz : z = 0 <;> simp +decide [ hz ];
        · exact Or.inr hT;
        · linarith

/-
**Exact slack characterization (`thm:exactslack`), `⊇` direction.**  Every value in
`B_T(D, k)` is a support-wise MCA-bad parameter for the canonical line `x^{k+T} + z·x^k` with
a witness of exactly `k+T` points.
-/
lemma exact_slack_superset {D : Finset F} {k T : ℕ} (hT : 1 ≤ T) {z : F}
    (hz : z ∈ BadImage D k T) :
    ∃ S : Finset F, S ⊆ D ∧ k + T ≤ S.card ∧
      MCAbadWitness (RScode k) S (fun x => x ^ (k + T)) (fun x => x ^ k) z := by
  obtain ⟨ S, hS₁, hS₂, hS₃ ⟩ := hz;
  refine' ⟨ S, hS₁, hS₂.ge, _, _ ⟩;
  · -- Define `R : F[X] := X^(k+T) + C z * X^k - locator S`.
    set R : F[X] := Polynomial.X ^ (k + T) + Polynomial.C z * Polynomial.X ^ k - locator S;
    -- We must show `R.degree < k`, i.e. `R.coeff i = 0` for all `i ≥ k`.
    have hR_deg : R.degree < k := by
      rw [ Polynomial.degree_lt_iff_coeff_zero ];
      intro m hm
      simp [R];
      by_cases hm' : m = k + T <;> by_cases hm'' : m = k <;> simp +decide [ hm', hm'' ];
      · linarith;
      · rw [ show ( locator S ).coeff ( k + T ) = 1 from _ ] ; aesop;
        convert Polynomial.Monic.coeff_natDegree ( locator_monic S ) using 1;
        rw [ locator_natDegree, hS₂ ];
      · rw [ show k = S.card - T by rw [ hS₂, Nat.add_sub_cancel ] ] ; rw [ locator_coeff_eq_esymm ] ; aesop;
        linarith;
      · by_cases hm''' : m < k + T;
        · convert locator_coeff_eq_esymm ( show k + T - m ≤ S.card from by omega ) using 1;
          · rw [ hS₂, Nat.sub_sub_self ( by linarith ) ];
          · grind;
        · rw [ Polynomial.coeff_eq_zero_of_natDegree_lt ] ; simp +decide [ locator_natDegree, hS₂ ] ; omega;
    refine' ⟨ fun x => R.eval x, _, _ ⟩;
    · exact ⟨ R, Polynomial.mem_degreeLT.mpr hR_deg, rfl ⟩;
    · intro x hx; simp +decide [ R, eval_locator_mem hx ] ;
  · exact fun h => xpow_not_explained ( by linarith ) h.2

/-! ### The quotient locator (`lem:tlocator`) -/

/-
**Quotient locator identity (`lem:tlocator`).**  The quotient locator
`L_A(X) = ∏_{b ∈ A} (X^a - b)` is the composition of the ordinary locator `L_A` (in the
quotient variable) with `X^a`.  Substituting `Y = X^a` into `∏_{b∈A}(Y - b)` spreads the
coefficient `(-1)^j e_j(A)` (the degree-`(|A|-j)` coefficient of `locator A`, by
`locator_coeff_eq_esymm`) to degree `a·(|A|-j)`, which is the paper's displayed expansion.
-/
lemma quotient_locator_comp (A : Finset F) (a : ℕ) :
    ∏ b ∈ A, (X ^ a - C b) = (locator A).comp (X ^ a) := by
  -- By definition of polynomial composition and product, we have:
  simp [locator, Polynomial.prod_comp]

/-- **Quotient locator vanishing (`lem:tlocator`).**  The quotient locator vanishes on the
full preimage `S_A = {x : x^a ∈ A}`: if `x^a ∈ A`, then `(∏_{b∈A}(X^a - b)).eval x = 0`. -/
lemma quotient_locator_vanish {A : Finset F} {a : ℕ} {x : F} (hx : x ^ a ∈ A) :
    (∏ b ∈ A, (X ^ a - C b)).eval x = 0 := by
  rw [quotient_locator_comp, Polynomial.eval_comp, Polynomial.eval_pow, Polynomial.eval_X,
    eval_locator_mem hx]

/-- **Exact slack characterization (`thm:exactslack`).**  For the canonical line
`u_z = x^{k+T} + z·x^k` on any evaluation set `D`, the set of support-wise MCA-bad parameters
at radius `δ_T = 1 - (k+T)/|D|` is exactly the multi-symmetric image `B_T(D, k)`. -/
theorem exact_slack {D : Finset F} {k T : ℕ} (hT : 1 ≤ T) :
    {z : F | ∃ S : Finset F, S ⊆ D ∧ k + T ≤ S.card ∧
        MCAbadWitness (RScode k) S (fun x => x ^ (k + T)) (fun x => x ^ k) z}
      = BadImage D k T := by
  ext z
  exact ⟨fun hz => exact_slack_subset hT hz, fun hz => exact_slack_superset hT hz⟩

end Chojecki
