/-!
# Emission arithmetic on the rank-one family: decidable counting shadow

Maps to **hard input 2**: seventh packet of the arc (forcing -> typing ->
reduction -> scope -> compression -> classification -> admission
arithmetic).  The note proves: every `G_{k,r}` is real (a <-> -a digit
pairing), symmetric hierarchy pieces have fully explicit real cube data,
T3 budgets are closed-form, the one-pattern-per-class cap is necessary
(additive schedules overdraw, extremal factor 2 computed), flat-cube
emission is exact on depth-1/subgroup territory and must widen to
rank-one emission from depth 2, and the resonant residue j* = (c-1)/2 is
maximally twisted at every depth.

Note:     `experimental/notes/thresholds/rank_one_emission_arithmetic.md`.
Verifier: `experimental/scripts/verify_rank_one_emission_arithmetic.py`
          (20/20, tamper 7/7).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trig/emission content lives in the note and the scans.  This module is
the DECIDABLE arithmetic shadow (stdlib-only `native_decide`, no mathlib,
no `sorry`): the a <-> -a pairing census behind Lemma R's reality, the
exact-rational depth-1 identity `3 G_{1,r}(l) = wtil(l) - wtil(l+1)`
(`r in {1,2}`) behind flat-exactness, and the all-ones digit identities
locating the resonant residue.
-/

namespace RankOneEmissionArithmetic

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Level fiber `wtil(s)` at `B = 6` on the realized parity, else 0. -/
def wtil6 (s : Nat) : Nat :=
  if s ≤ 6 ∧ s % 2 = 0 then binom (6 - s) ((6 - s) / 2) else 0

/-- Nonzero canonical balanced-ternary digits of `y mod 3^ndig`. -/
def s3 (y ndig : Nat) : Nat :=
  match ndig with
  | 0 => 0
  | n + 1 =>
    let d := y % 3
    if d = 0 then s3 (y / 3) n
    else if d = 1 then 1 + s3 (y / 3) n
    else 1 + s3 (y / 3 + 1) n

/-! ## 1. The pairing behind Lemma R: `s3(-a) = s3(a)`, and the census of
    proper pairs `#{{a, 3^k - a} : a != 0} = (3^k - 1)/2`. -/

theorem pairing_symmetry :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7], ∀ a ∈ List.range (3 ^ k),
      s3 ((3 ^ k - a) % 3 ^ k) k = s3 a k := by
  native_decide

theorem pairing_census :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7],
      ((List.range (3 ^ k)).filter (fun a => 0 < a ∧ 2 * a < 3 ^ k)).length
        = (3 ^ k - 1) / 2 := by
  native_decide

/-! ## 2. The exact-rational depth-1 identity behind flat-exactness:
    `3 G_{1,r}(l) = wtil(l) - wtil(l+1)` for `r in {1,2}` -- as the
    integer identity `2 wtil(l) - (wtil(s3(1)+l) + wtil(s3(2)+l))
    = 2 (wtil(l) - wtil(l+1))`, i.e. both twisted `a`-terms sit at digit
    count 1 and enter with weight `2 cos(2 pi r/3) = -1`. -/

theorem depth1_digit_counts : s3 1 1 = 1 ∧ s3 2 1 = 1 := by
  native_decide

theorem depth1_G_integer :
    ∀ l ∈ List.range 7,
      2 * (wtil6 l : Int) - wtil6 (s3 1 1 + l) - wtil6 (s3 2 1 + l)
        = 2 * ((wtil6 l : Int) - wtil6 (l + 1)) := by
  native_decide

/-! ## 3. The resonant residue `j* = (3^B - 1)/2`: all-ones digits,
    maximally twisted at every depth. -/

theorem resonant_all_ones :
    ∀ B ∈ [2, 4, 6, 8, 10], s3 ((3 ^ B - 1) / 2) B = B := by
  native_decide

theorem resonant_maximally_twisted :
    ∀ B ∈ [4, 6, 8], ∀ k ∈ List.range (B + 1), 1 ≤ k →
      ((3 ^ B - 1) / 2) % 3 ^ k = (3 ^ k - 1) / 2 := by
  native_decide

/-! ## 4. Shared class pins. -/

theorem class_pins :
    wtil6 0 = 20 ∧ wtil6 2 = 6 ∧ wtil6 4 = 2 ∧ wtil6 6 = 1 ∧
    wtil6 1 = 0 ∧ binom 12 6 = 924 := by
  native_decide

end RankOneEmissionArithmetic
