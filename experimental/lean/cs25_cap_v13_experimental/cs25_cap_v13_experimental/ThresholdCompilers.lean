import Mathlib

/-!
# CAP25 v13 — Chapter: Threshold certificate compilers

This file formalizes the self-contained mathematical results of the section
"Threshold certificate compilers" (`\section{sec:v13-threshold}`) of
`cap25_v13_experimental.tex`.

The section develops an *exact integer* certificate grammar for deciding, for a
monotone "numerator" staircase `N` and a budget `B`, at which agreement each row
becomes "safe" (`N a ≤ B`).  We formalize:

* `safe_upClosed`, `staircase_localization`, `staircase_interior`
  (Theorem *staircase localization*, `thm:v13-staircase`);
* `endpoint_radius` (Corollary *closed-radius endpoint convention*, `cor:v13-endpoint`);
* `corridor_lower`, `corridor_upper` (Theorem *corridor from lower and upper
  certificates*, `thm:v13-corridor`);
* `steepness_disjoint`, `steepness_unsafe`, `steepness_safe`
  (Theorem *coarse steepness compiler*, `thm:v13-steepness`);
* `extPole_exists` (Proposition *extension-pole conversion cell*, `prop:v13-extension`),
  the Cauchy–Schwarz double-counting core;
* `budget_unsafe`, `budget_safe`, `budget_field_interval`, `budget_gmax`
  (Theorem *budget windows and dodge selection*, `thm:v13-windows`);
* `A2`, `census_identity` (Lemma *rate-1/2 census identity*, `lem:v13-census-identity`);
* `census_crossing_*` (Theorem *bounded quotient census*, `thm:v13-census`),
  the exact-arithmetic crossing certificates;
* `qprofile_bounded`, `qprofile_dyadic` (Proposition *bounded active quotient order*,
  `prop:v13-qprofile`);
* `residual_absorption` (Proposition *polynomial residual absorption*, `prop:v13-integrality`).

The paid-cell results that are stated in the text purely by *citation of external
v12 theorems* (the exact tangent cell `prop:v13-tangent`, which invokes
`thm:deep-mca`, and the quotient safe-sum cell `prop:v13-quotient-safe-sum`, which
invokes the v12 support/image ledgers) are not reproduced here, as they depend on
machinery outside the self-contained scope of this insert.
-/

open Finset BigOperators

namespace CAP25V13.Threshold

/-! ## Integer staircases and corridors -/

/-
The "safe" set `{a : N a ≤ B}` of a nonincreasing numerator staircase is
upward closed.  This is the monotonicity that underlies `thm:v13-staircase`.
-/
theorem safe_upClosed {N : ℕ → ℕ} (hN : Antitone N) {B a a' : ℕ}
    (h : N a ≤ B) (hle : a ≤ a') : N a' ≤ B := by
      exact le_trans ( hN hle ) h

/-
**Staircase localization** (`thm:v13-staircase`).  For a nonincreasing
`N : ℕ → ℕ`, exactly one of the following holds on the agreement interval
`Icc amin amax`: every agreement is safe, every agreement is unsafe, or there is a
first safe agreement `astar` such that the safe set is exactly `{a : astar ≤ a}`.
-/
theorem staircase_localization {N : ℕ → ℕ} (hN : Antitone N) (B amin amax : ℕ) :
    (∀ a ∈ Finset.Icc amin amax, N a ≤ B) ∨
    (∀ a ∈ Finset.Icc amin amax, ¬ N a ≤ B) ∨
    (∃ astar ∈ Finset.Icc amin amax,
        ∀ a ∈ Finset.Icc amin amax, (N a ≤ B ↔ astar ≤ a)) := by
          by_cases h : ∃ a ∈ Finset.Icc amin amax, N a ≤ B;
          · obtain ⟨astar, h_astar⟩ : ∃ astar ∈ Finset.Icc amin amax, N astar ≤ B ∧ ∀ a ∈ Finset.Icc amin amax, N a ≤ B → astar ≤ a := by
              exact ⟨ Nat.find h, Nat.find_spec h |>.1, Nat.find_spec h |>.2, fun a ha ha' => Nat.find_min' h ⟨ ha, ha' ⟩ ⟩;
            refine Or.inr <| Or.inr <| ⟨ astar, h_astar.1, fun a ha => ⟨ fun ha' => h_astar.2.2 a ha ha', fun ha' => ?_ ⟩ ⟩;
            exact le_trans ( hN ha' ) h_astar.2.1;
          · grind +splitImp

/-
**Interior transition** of `thm:v13-staircase`: at a first safe agreement
`astar` strictly above `amin`, the predecessor is unsafe and `astar` is safe, i.e.
`N (astar-1) > B ≥ N astar`.
-/
theorem staircase_interior {N : ℕ → ℕ} {B amin astar : ℕ}
    (hmin : amin < astar) (hsafe : N astar ≤ B)
    (hfirst : ∀ a, a < astar → ¬ N a ≤ B) :
    B < N (astar - 1) ∧ N astar ≤ B := by
      grind +qlia

/-
**Closed-radius endpoint convention** (`cor:v13-endpoint`).  With the closed
integer radius `r = n - a`, the first safe agreement `astar` gives largest safe
radius `n - astar`; the next radius (corresponding to `astar - 1`) is unsafe.
-/
theorem endpoint_radius {N : ℕ → ℕ} {B n astar : ℕ}
    (h1 : 1 ≤ astar) (hastar : astar ≤ n)
    (hsafe : N astar ≤ B) (hunsafe : ¬ N (astar - 1) ≤ B) :
    N (n - (n - astar)) ≤ B ∧ ¬ N (n - (n - astar + 1)) ≤ B := by
      grind

/-
**Corridor, lower side** (`thm:v13-corridor`).  If a certified lower bound
`L ≤ N` exceeds the budget at `a`, then `a` lies strictly below the threshold
`astar`.
-/
theorem corridor_lower {N L : ℕ → ℕ} (hL : ∀ a, L a ≤ N a) {B astar : ℕ}
    (hthr : ∀ b, (N b ≤ B ↔ astar ≤ b)) {a : ℕ} (ha : B < L a) : a < astar := by
      grind

/-
**Corridor, upper side** (`thm:v13-corridor`).  If a certified upper bound
`N ≤ U` is within budget at `a`, then `a` is at or above the threshold `astar`.
-/
theorem corridor_upper {N U : ℕ → ℕ} (hU : ∀ a, N a ≤ U a) {B astar : ℕ}
    (hthr : ∀ b, (N b ≤ B ↔ astar ≤ b)) {a : ℕ} (ha : U a ≤ B) : astar ≤ a := by
      exact hthr a |>.1 ( le_trans ( hU a ) ha )

/-! ## Coarse steepness compiler -/

/-
**Steepness disjointness** (`thm:v13-steepness`).  For `E ≥ 1` and a positive
model count, the separation `M a > E² · M (a+1)` forces the ambiguity intervals
`[M a / E, E·M a]` and `[M (a+1)/E, E·M (a+1)]` to be disjoint: the lower end of the
first is above the upper end of the second.
-/
theorem steepness_disjoint {E Ma Ma1 : ℝ} (hE : 1 ≤ E)
    (hsep : E ^ 2 * Ma1 < Ma) : E * Ma1 < Ma / E := by
      rw [ lt_div_iff₀ ] <;> linarith

/-
**Steepness certifies unsafe** (`thm:v13-steepness`): a budget below the lower
end of the ambiguity interval is certified unsafe.
-/
theorem steepness_unsafe {E Mb Nb Bstar : ℝ} (hlo : Mb / E ≤ Nb)
    (h : Bstar < Mb / E) : Bstar < Nb := by
      linarith

/-
**Steepness certifies safe** (`thm:v13-steepness`): a budget at or above the
upper end of the ambiguity interval is certified safe.
-/
theorem steepness_safe {E Mb Nb Bstar : ℝ} (hhi : Nb ≤ E * Mb)
    (h : E * Mb ≤ Bstar) : Nb ≤ Bstar := by
      linarith

/-! ## Extension-pole conversion cell -/

/-
**Extension-pole conversion cell** (`prop:v13-extension`), Cauchy–Schwarz core.
Given a base list `P` of size `L`, a set of poles `poles` of size `m ≥ 1`, and for
each pole `a` a value assignment `lam a : ι → V` whose pairwise collision count over
`P` is at most `κ`, some pole realizes at least `⌈Lm/(m+κ(L-1))⌉` distinct values,
recorded here in the equivalent integer form
`Mα · (m + κ(L-1)) ≥ L · m`.
-/
theorem extPole_exists {α ι V : Type*} [DecidableEq α] [DecidableEq V]
    (poles : Finset α) (P : Finset ι) (lam : α → ι → V) (κ : ℕ)
    (hm : 0 < poles.card) (hL : 0 < P.card)
    (hcol : ∀ p ∈ P, ∀ p' ∈ P, p ≠ p' →
      (poles.filter (fun a => lam a p = lam a p')).card ≤ κ) :
    ∃ a ∈ poles,
      P.card * poles.card
        ≤ (P.image (lam a)).card * (poles.card + κ * (P.card - 1)) := by
          by_contra! h_contra;
          have h_total_collisions : ∑ a ∈ poles, (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) ≤ poles.card * #P + κ * #P * (#P - 1) := by
            have h_total_collisions : ∑ a ∈ poles, (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) = poles.card * #P + ∑ a ∈ poles, (Finset.sum (Finset.offDiag P) (fun v => if lam a v.1 = lam a v.2 then 1 else 0)) := by
              have h_total_collisions : ∀ a ∈ poles, (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) = #P + (Finset.sum (Finset.offDiag P) (fun v => if lam a v.1 = lam a v.2 then 1 else 0)) := by
                intro a ha
                have h_total_collisions : (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) = (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card)) + (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card * ((Finset.filter (fun p => lam a p = v) P).card - 1))) := by
                  rw [ ← Finset.sum_add_distrib ] ; congr ; ext v ; cases h : Finset.card ( Finset.filter ( fun p => lam a p = v ) P ) <;> simp +decide ; ring;
                have h_total_collisions : (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card * ((Finset.filter (fun p => lam a p = v) P).card - 1))) = (Finset.sum (Finset.offDiag P) (fun v => if lam a v.1 = lam a v.2 then 1 else 0)) := by
                  have h_total_collisions : ∀ v ∈ Finset.image (lam a) P, (Finset.filter (fun p => lam a p = v) P).card * ((Finset.filter (fun p => lam a p = v) P).card - 1) = (Finset.sum (Finset.offDiag P) (fun v' => if lam a v'.1 = v ∧ lam a v'.2 = v then 1 else 0)) := by
                    intro v hv
                    have h_total_collisions : (Finset.filter (fun p => lam a p = v) P).card * ((Finset.filter (fun p => lam a p = v) P).card - 1) = (Finset.offDiag (Finset.filter (fun p => lam a p = v) P)).card := by
                      simp +decide [ mul_tsub, Finset.offDiag_card ];
                    rw [ h_total_collisions, ← Finset.card_filter ];
                    refine' Finset.card_bij ( fun x hx => ( x.1, x.2 ) ) _ _ _ <;> simp +contextual;
                  rw [ Finset.sum_congr rfl h_total_collisions, Finset.sum_comm ];
                  refine' Finset.sum_congr rfl fun x hx => _;
                  by_cases h : lam a x.1 = lam a x.2 <;> simp +decide [ h ];
                  · exact ⟨ x.1, Finset.mem_offDiag.mp hx |>.1, h ⟩;
                  · grind;
                rw [ ‹∑ v ∈ image ( lam a ) P, # ( { p ∈ P | lam a p = v } ) ^ 2 = _›, h_total_collisions, ← Finset.card_eq_sum_card_fiberwise ];
                exact fun x hx => Finset.mem_image_of_mem _ hx;
              rw [ Finset.sum_congr rfl h_total_collisions, Finset.sum_add_distrib, Finset.sum_const, Finset.card_eq_sum_ones, smul_eq_mul, mul_comm ];
            have h_total_collisions : ∑ a ∈ poles, (Finset.sum (Finset.offDiag P) (fun v => if lam a v.1 = lam a v.2 then 1 else 0)) ≤ ∑ v ∈ Finset.offDiag P, κ := by
              rw [ Finset.sum_comm ];
              exact Finset.sum_le_sum fun x hx => by simpa using hcol x.1 ( Finset.mem_offDiag.mp hx |>.1 ) x.2 ( Finset.mem_offDiag.mp hx |>.2.1 ) ( Finset.mem_offDiag.mp hx |>.2.2 ) ;
            simp_all +decide [ mul_assoc, mul_comm, Finset.offDiag_card ];
            rwa [ Nat.mul_sub_left_distrib, Nat.mul_one ];
          have h_total_collisions : ∑ a ∈ poles, (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) ≥ ∑ a ∈ poles, (#P ^ 2 / (Finset.card (Finset.image (lam a) P) : ℝ)) := by
            have h_total_collisions : ∀ a ∈ poles, (Finset.sum (Finset.image (lam a) P) (fun v => (Finset.filter (fun p => lam a p = v) P).card ^ 2)) ≥ (#P ^ 2 / (Finset.card (Finset.image (lam a) P) : ℝ)) := by
              intro a ha
              have h_cauchy_schwarz : (∑ v ∈ Finset.image (lam a) P, (Finset.filter (fun p => lam a p = v) P).card) ^ 2 ≤ (∑ v ∈ Finset.image (lam a) P, (Finset.filter (fun p => lam a p = v) P).card ^ 2) * #(image (lam a) P) := by
                have h_cauchy_schwarz : ∀ (u v : Finset V) (f g : V → ℝ), (∑ x ∈ u, f x * g x) ^ 2 ≤ (∑ x ∈ u, f x ^ 2) * (∑ x ∈ u, g x ^ 2) := by
                  exact fun u _ f g => sum_mul_sq_le_sq_mul_sq u f g;
                simpa [ ← @Nat.cast_le ℝ ] using h_cauchy_schwarz ( image ( lam a ) P ) ( image ( lam a ) P ) ( fun x => ( Finset.card ( Finset.filter ( fun p => lam a p = x ) P ) : ℝ ) ) ( fun x => 1 );
              rw [ ge_iff_le, div_le_iff₀ ] <;> norm_cast;
              · grind +suggestions;
              · exact Finset.card_pos.mpr ⟨ _, Finset.mem_image_of_mem _ ( Classical.choose_spec ( Finset.card_pos.mp hL ) ) ⟩;
            exact le_trans ( Finset.sum_le_sum h_total_collisions ) ( by simp +decide );
          have h_total_collisions : ∑ a ∈ poles, (#P ^ 2 / (Finset.card (Finset.image (lam a) P) : ℝ)) > poles.card * (#P ^ 2 / (#P * poles.card / (#poles + κ * (#P - 1)) : ℝ)) := by
            have h_total_collisions : ∀ a ∈ poles, (#P ^ 2 / (Finset.card (Finset.image (lam a) P) : ℝ)) > (#P ^ 2 / (#P * poles.card / (#poles + κ * (#P - 1)) : ℝ)) := by
              intro a ha
              have h_card_image : (Finset.card (Finset.image (lam a) P) : ℝ) < (#P * poles.card / (#poles + κ * (#P - 1)) : ℝ) := by
                rw [ lt_div_iff₀ ] <;> norm_cast;
                · grind +revert;
                · rw [ Int.subNatNat_eq_coe ] ; push_cast ; nlinarith;
              gcongr;
              exact Nat.cast_pos.mpr ( Finset.card_pos.mpr ⟨ _, Finset.mem_image_of_mem _ ( Classical.choose_spec ( Finset.card_pos.mp hL ) ) ⟩ );
            simpa using Finset.sum_lt_sum_of_nonempty ( Finset.card_pos.mp hm ) h_total_collisions;
          refine' h_total_collisions.not_ge ( le_trans ‹_› _ );
          field_simp;
          norm_cast;
          rw [ Int.subNatNat_of_le ( Nat.one_le_iff_ne_zero.mpr hL.ne' ) ] ; norm_cast ; nlinarith [ Nat.sub_add_cancel hL ]

/-! ## Budget windows and dodge selection -/

/-
**Budget window, unsafe side** (`thm:v13-windows`): a budget strictly below the
certified lower bound `L ≤ N` certifies unsafety.
-/
theorem budget_unsafe {N L B : ℕ} (hL : L ≤ N) (h : B < L) : B < N := by
  linarith

/-
**Budget window, safe side** (`thm:v13-windows`): a budget at or above the
certified upper bound `N ≤ K` certifies safety.
-/
theorem budget_safe {N K B : ℕ} (hK : N ≤ K) (h : K ≤ B) : N ≤ B := by
  grind

/-
**Unresolved field-size interval** (`thm:v13-windows`) with `B(q) = ⌊q/2¹²⁸⌋`.
The unresolved budgets `L ≤ B(q) < K` correspond exactly to the field-size interval
`L·2¹²⁸ ≤ q ≤ K·2¹²⁸ - 1`.
-/
theorem budget_field_interval (L K q : ℕ) (hK : 1 ≤ K) :
    (L ≤ q / 2 ^ 128 ∧ q / 2 ^ 128 < K) ↔
      (L * 2 ^ 128 ≤ q ∧ q ≤ K * 2 ^ 128 - 1) := by
        constructor <;> intro h <;> omega

/-
**Largest tolerable missing mass** (`thm:v13-windows`): if the lower proof is
`L = K - g`, unsafety (`B(q) < L`) holds iff the missing mass `g` is below
`K - B(q)`, whose largest integer value is `K - B(q) - 1`.
-/
theorem budget_gmax {K g B : ℕ} (hg : g ≤ K) :
    (B < K - g) ↔ (g < K - B) := by
      constructor <;> intro h <;> omega

/-! ## Rate-1/2 census identity and the bounded quotient census -/

/-- The characteristic-zero antipodal quotient count `A₂(N', ℓ')` of the quotient
census, with `n₁ = N'/2`:
`A₂(N',ℓ') = ∑_{u ≥ 0, t = ℓ'-2u ≥ 0, u+t ≤ n₁} C(n₁,t) 2^t`. -/
def A2 (N' l' : ℕ) : ℕ :=
  let n1 := N' / 2
  ∑ u ∈ Finset.range (l' / 2 + 1),
    (if l' - u ≤ n1 then Nat.choose n1 (l' - 2 * u) * 2 ^ (l' - 2 * u) else 0)

/-
**Rate-1/2 census identity** (`lem:v13-census-identity`).  For every even
`N' ≥ 2`, with `n₁ = N'/2`, one has `A₂(N', n₁+1) = (3^{n₁} - 1)/2`, stated here in
the division-free form `2·A₂(N', n₁+1) = 3^{n₁} - 1`.
-/
theorem census_identity (N' : ℕ) (hN' : Even N') (h2 : 2 ≤ N') :
    2 * A2 N' (N' / 2 + 1) = 3 ^ (N' / 2) - 1 := by
      -- By definition of $A2$, we have:
      have hA2_def : A2 N' (N' / 2 + 1) = ∑ t ∈ Finset.filter (fun t => t % 2 ≠ (N' / 2) % 2) (Finset.range (N' / 2 + 1)), Nat.choose (N' / 2) t * 2 ^ t := by
        obtain ⟨ k, hk ⟩ := hN' ; simp_all +decide;
        simp +decide [ ← two_mul, A2 ];
        rw [ ← Finset.sum_filter ];
        refine' Finset.sum_bij ( fun x hx => k + 1 - 2 * x ) _ _ _ _ <;> simp +arith +decide;
        · omega;
        · intros; omega;
        · intro b hb hb'; use ( k + 1 - b ) / 2; omega;
      -- By definition of $A2$, we have $2 \cdot A2(N', N'/2 + 1) = 3^{N'/2} - 1$.
      have hA2_eq : ∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (if t % 2 ≠ (N' / 2) % 2 then 2 else 0) = 3 ^ (N' / 2) - 1 := by
        have hA2_eq : ∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (if t % 2 ≠ (N' / 2) % 2 then 2 else 0) = ∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (1 - (-1 : ℤ) ^ (t + (N' / 2))) := by
          push_cast [ Finset.sum_mul _ _ _ ];
          refine' Finset.sum_congr rfl fun x hx => _ ; rcases Nat.even_or_odd' x with ⟨ k, rfl | rfl ⟩ <;> rcases Nat.even_or_odd' ( N' / 2 ) with ⟨ l, hl | hl ⟩ <;> norm_num [ Nat.add_mod, Nat.mul_mod, hl, pow_add, pow_mul, Nat.even_iff ] ;
        have hA2_eq : ∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (1 - (-1 : ℤ) ^ (t + (N' / 2))) = (1 + 2) ^ (N' / 2) - (1 - 2) ^ (N' / 2) * (-1) ^ (N' / 2) := by
          have hA2_eq : ∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (1 - (-1 : ℤ) ^ (t + (N' / 2))) = (∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t) - (∑ t ∈ Finset.range (N' / 2 + 1), Nat.choose (N' / 2) t * 2 ^ t * (-1 : ℤ) ^ (t + (N' / 2))) := by
            simp +decide [ mul_sub, Finset.sum_sub_distrib ];
          convert hA2_eq using 2;
          · rw [ add_comm 1, add_pow ] ; norm_num [ mul_comm ];
          · rw [ sub_eq_neg_add, add_pow ] ; norm_num ; ring;
            rw [ Finset.sum_mul _ _ _ ] ; exact Finset.sum_congr rfl fun _ _ => by rw [ mul_assoc ] ; rw [ mul_assoc ] ; rw [ ← mul_pow ] ; ring;
        norm_num [ ← @Nat.cast_inj ℤ ] at *;
        simp_all +decide [ ← mul_pow ];
      simp_all +decide [ Finset.sum_ite, mul_comm ];
      rw [ ← hA2_eq, Finset.mul_sum _ _ _ ]

/-- **Bounded quotient census** (`thm:v13-census`), relaxed even-scale model,
rate `ρ = 1/2`: the first even scale at which `A₂ > 2¹²⁸-1` is `N' = 164`, with
predecessor `N' = 162` still within budget. -/
theorem census_crossing_relaxed_half :
    2 ^ 128 - 1 < A2 164 83 ∧ A2 162 82 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `thm:v13-census`, relaxed even model, rate `ρ = 1/4`: first crossing at
`N' = 176`, predecessor `N' = 172`. -/
theorem census_crossing_relaxed_quarter :
    2 ^ 128 - 1 < A2 176 45 ∧ A2 172 44 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `thm:v13-census`, relaxed even model, rate `ρ = 1/8`: first crossing at
`N' = 248`, predecessor `N' = 240`. -/
theorem census_crossing_relaxed_eighth :
    2 ^ 128 - 1 < A2 248 32 ∧ A2 240 31 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `thm:v13-census`, relaxed even model, rate `ρ = 1/16`: first crossing at
`N' = 384`, predecessor `N' = 368`. -/
theorem census_crossing_relaxed_sixteenth :
    2 ^ 128 - 1 < A2 384 25 ∧ A2 368 24 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `thm:v13-census`, dyadic model `N' = 2^a`, rate `ρ = 1/2`: first dyadic
crossing at `N' = 256`, predecessor `N' = 128`. -/
theorem census_crossing_dyadic_half :
    2 ^ 128 - 1 < A2 256 129 ∧ A2 128 65 ≤ 2 ^ 128 - 1 := by
  native_decide

/-- `thm:v13-census`, dyadic model, rate `ρ = 1/16`: first dyadic crossing at
`N' = 512`, predecessor `N' = 256`. -/
theorem census_crossing_dyadic_sixteenth :
    2 ^ 128 - 1 < A2 512 33 ∧ A2 256 17 ≤ 2 ^ 128 - 1 := by
  native_decide

/-! ## Bounded active quotient order -/

/-
**Bounded active quotient order** (`prop:v13-qprofile`).  An active quotient
scale requires slack `σ < M` with `M ∣ n`; hence if `σ ≥ n/256` (i.e. `n ≤ 256σ`),
every active scale has quotient order `N = n/M < 256`.
-/
theorem qprofile_bounded {n M σ : ℕ} (hMn : M ∣ n) (hn : 0 < n)
    (hact : σ < M) (hσ : n ≤ 256 * σ) : n / M < 256 := by
      exact Nat.div_lt_of_lt_mul <| by linarith;

/-
**Dyadic sharpening** (`prop:v13-qprofile`): a power-of-two quotient order
strictly below `256 = 2⁸` is at most `128 = 2⁷`.
-/
theorem qprofile_dyadic {N e : ℕ} (hN : N = 2 ^ e) (h : N < 256) : N ≤ 128 := by
  exact hN.symm ▸ by exact le_trans ( pow_le_pow_right₀ ( by decide ) ( show e ≤ 7 by exact le_of_not_gt fun he => by linarith [ Nat.pow_le_pow_right ( by decide : 1 ≤ 2 ) he ] ) ) ( by decide ) ;

/-! ## Polynomial residual absorption -/

/-
**Polynomial residual absorption** (`prop:v13-integrality`).  A nonnegative
integer residual bounded above by a real number strictly below `1` must be `0`.
-/
theorem residual_absorption {r : ℕ} {x : ℝ} (h1 : (r : ℝ) ≤ x) (h2 : x < 1) :
    r = 0 := by
      exact Nat.eq_zero_of_le_zero ( Nat.le_of_lt_succ ( by rw [ ← @Nat.cast_lt ℝ ] ; push_cast; linarith ) )

end CAP25V13.Threshold