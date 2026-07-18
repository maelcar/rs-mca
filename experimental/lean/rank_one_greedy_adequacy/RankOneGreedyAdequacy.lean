/-!
# The adequacy depth law and the greedy completion: decidable shadow

Maps to **hard input 2**: ninth packet of the arc (... -> local scalar
soundness -> local scalar cap adequacy).  The note proves: adequacy ratios are
B-independent pure-trig instances (T1), single-pattern coefficient capacity
reaches each class's local scalar cap for every B at depths k <= 3 (T2,
instance space), fails from depth 4 (T3; first instance
(k,r,top,sG) = (4,4,{0,1,2},-1), ratio 0.9910, realized at B = 6), and
the greedy schedule capped at sum h_+ reaches EVERY depth's scalar cap (T4, the
triangle inequality sum|h| <= 2^m sum|hcube|).

Note:     `experimental/notes/thresholds/rank_one_greedy_adequacy.md`.
Verifier: `experimental/scripts/verify_rank_one_greedy_adequacy.py`
          (19/19, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trig instances live in the scans.  This module is the DECIDABLE
arithmetic shadow (stdlib-only `native_decide`, no mathlib, no `sorry`):
instance-space counts behind T1's finiteness, the digit words of the
onset and deep-worst residues, and the class pins.
-/

namespace RankOneGreedyAdequacy

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

/-! ## 1. T1's finiteness: the per-depth instance space is
    `(2^k - 1)(3^k - 1) * 2`, independent of `B`. -/

theorem instance_space_counts :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7],
      (2 ^ k - 1) * (3 ^ k - 1) * 2
        = ((List.range (2 ^ k)).filter (0 < ·)).length
          * ((List.range (3 ^ k)).filter (0 < ·)).length * 2 := by
  native_decide

/-- The `k <= 5` sweep size the verifier reports: `sum_{k<=5}
    (2^k-1)(3^k-1)*2 = 17820`. -/
theorem sweep_size_k5 :
    (List.range 6).foldl
      (fun acc k => if k = 0 then acc
        else acc + (2 ^ k - 1) * (3 ^ k - 1) * 2) 0 = 17820 := by
  native_decide

/-! ## 2. The onset and deep-worst residues, located by their digits. -/

/-- Onset `r = 4` at depth 4: digit word `(1,1,0,0)`, `s3 = 2`, and it is
    twisted at depth 4 but SUBGROUP at depth 1 is false (`4 % 3 = 1`):
    a genuinely twisted residue. -/
theorem onset_digits :
    s3 4 4 = 2 ∧ 4 % 3 = 1 ∧ 4 % 81 = 4 := by
  native_decide

/-- Deep worst `r = 1367` at depth 7: the ALTERNATING balanced word
    `(-1,0,-1,0,-1,0,-1)` -- `s3 = 4` and `1367 = 3^7 - 820` with
    `820 = 1 + 9 + 81 + 729`. -/
theorem deep_worst_digits :
    s3 1367 7 = 4 ∧ 820 = 1 + 9 + 81 + 729 ∧ 3 ^ 7 - 820 = 1367 := by
  native_decide

/-! ## 3. Realization arithmetic for the B = 6 witness: the class
    `101110` has `s = 4 == 6 mod 2`, top positions `{2,3,4}` at depth 4
    (`B - k = 2`), `s_low = 1`. -/

theorem witness_class_arithmetic :
    (4 % 2 = 6 % 2) ∧ (2 + 4 = 6) ∧ wtil6 4 = 2 := by
  native_decide

/-! ## 4. The greedy schedule's soundness skeleton: the capped payment
    never exceeds the cap (T4's soundness half, as a general lemma). -/

theorem greedy_cap_sound (pay cap : Nat) : min pay cap ≤ cap :=
  Nat.min_le_right pay cap

/-! ## 5. Shared class pins. -/

theorem class_pins :
    wtil6 0 = 20 ∧ wtil6 2 = 6 ∧ wtil6 4 = 2 ∧ wtil6 6 = 1 ∧
    binom 12 6 = 924 := by
  native_decide

end RankOneGreedyAdequacy
