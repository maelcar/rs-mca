/-!
# Selected power-profile comparison (decidable arithmetic shadow)

Maps to **hard input 4**: the complete profile-envelope comparison
`E_n(a) = 1 + (n-a+1) + sup_line sum_lambda (1 + barN_lambda)` versus the
identity-prefix term alone (`thm:unconditional-support-envelope-bracket` SB1
compares only `L(a)`; `eq:profile-envelope` (1.6) is the complete object).

Note: `experimental/notes/thresholds/profile_envelope_target_comparison.md`.
Verifier: `experimental/scripts/verify_profile_envelope_target_comparison.py`
(`PASS (89/89)`).

This module checks fixed natural-number/binomial equalities and selected
identity/square cross-products emitted by the verifier. It does not construct
finite fields, enumerate first-match ownership units, or prove a complete
profile envelope. The general exact prime-field identity-dominance claim is
false; the companion note and verifier record explicit counterexamples. This
package is the decidable arithmetic shadow, in the stdlib-only `native_decide`
house style. No `sorry`. No mathlib.
-/

namespace ProfileEnvelopeTargetComparison

/-! ## 1. Binomials (stdlib-only Pascal; core `Nat` has no `Nat.choose`) -/

def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

theorem binom_12_6   : binom 12 6 = 924    := by native_decide
theorem binom_6_3    : binom 6 3 = 20      := by native_decide   -- |Omega_sq|, n=12
theorem binom_20_10  : binom 20 10 = 184756 := by native_decide
theorem binom_10_5   : binom 10 5 = 252    := by native_decide   -- |Omega_sq|, n=20

/-! ## 2. Realized-image census integers (the exact ground truth of rung b).

    Each row records `(|Omega_id|, L_id)` and `(|Omega_sq|, L_sq)`; `barN=|Omega|/L`.
    `L_sq = p` on the tower is the field drop; `L_sq = |B|` on the prime is none. -/

-- prime GF(13), n=12, a=6, w=2: exact full-codomain equality, L_id = 13^2
theorem prime13_id_size : binom 12 6 = 924        := by native_decide
theorem prime13_L_id    : (169 : Nat) = 13 ^ 2    := by native_decide
theorem prime13_sq_size : binom 6 3 = 20          := by native_decide
theorem prime13_sq_L    : (13 : Nat) = 13         := by native_decide   -- no drop

-- tower GF(7^2), n=12, a=6, w=2:  field drop L_sq = p = 7,  L_id collapses
theorem tower49_sq_L_is_p : (7 : Nat) = 7          := by native_decide
theorem tower49_id_collapse : (319 : Nat) < 49 ^ 2 := by native_decide

-- tower GF(11^2), n=20, a=10, w=2:  field drop L_sq = p = 11
theorem tower121_sq_size : binom 10 5 = 252        := by native_decide
theorem tower121_sq_L_is_p : (11 : Nat) = 11       := by native_decide

-- prime GF(41), n=20, a=10, w=2: exact full-codomain equality, L_id = 41^2
theorem prime41_L_id : (1681 : Nat) = 41 ^ 2       := by native_decide

/-! ## 3. Selected identity/square comparisons by cross-multiplication
    (`barN_a >= barN_b <=> |Omega_a| * L_b >= |Omega_b| * L_a`). -/

/-- **(c-i) prime domination.** GF(13) `n=12`: `barN_id = 924/169 >= 20/13 =
    barN_sq`, i.e. identity dominates the square slice.  No field drop. -/
theorem prime13_identity_dominates :
    binom 12 6 * 13 ≥ binom 6 3 * 169 := by native_decide      -- 12012 >= 3380

/-- **(c-ii) tower obstruction, n=12.** GF(7^2): `barN_sq = 20/7 >
    924/2401 = C(n,a)|B|^{-w}` (the formal identity budget, 6.3): the c=2
    field-drop square beats the identity-prefix term. -/
theorem tower49_square_beats_formal_identity :
    binom 6 3 * (49 ^ 2) > binom 12 6 * 7 := by native_decide   -- 48020 > 6468

/-- **(c-ii) tower obstruction, n=20 (the deep crossing `barN_1 >= 1`).**
    GF(11^2): `barN_sq = 252/11 > 184756/14641 = C(n,a)|B|^{-w}`.  This is the
    paper's own `thm:smooth-quotient-obstruction` (`e_2 = h/4`), NOT a new floor. -/
theorem tower121_square_beats_formal_identity :
    binom 10 5 * (11 ^ 4) > binom 20 10 * 11 := by native_decide  -- 3689532 > 2032316

/-- Crossing bracket at n=20 (6.3): `1 <= barN_1 = C(20,10)/11^4 < |B|^2 = 11^4`. -/
theorem tower121_crossing_bracket :
    11 ^ 4 ≤ binom 20 10 ∧ binom 20 10 < (11 ^ 4) * (11 ^ 4) := by native_decide

/-! ## 4. Exact full-codomain measurements

These fixed finite equalities do not decide the source's asymptotic `(FI)`
condition `L >= exp(-o(n)) A`. -/

/-- GF(11^2) `n=20`: `L_id = 1331 = 11^3 = |B|^w / p`, a factor-`p` collapse of
    the identity image below its ambient codomain `11^4`. -/
theorem tower121_identity_full_codomain_deficit :
    (1331 : Nat) = 11 ^ 3 ∧ 1331 * 11 = 11 ^ 4 ∧ 1331 < 11 ^ 4 := by native_decide

/-- Contrast: on the prime subgroup GF(41) `n=20`, the identity image equals
    its full ambient codomain (`L_id = 1681 = 41^2 = |B|^w`). -/
theorem prime41_identity_full_codomain_exact : (1681 : Nat) = 41 ^ 2 := by native_decide

end ProfileEnvelopeTargetComparison
