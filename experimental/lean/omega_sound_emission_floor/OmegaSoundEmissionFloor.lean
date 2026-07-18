/-!
# The omega-sound emission floor: decidable counting shadow

Maps to **hard input 2**: eighth packet of the arc (... -> local scalar
arithmetic -> local scalar soundness).  The note shows band-uniform T3's
floor is sound against the cube |h|-ell^1 but overpays the grammar's
charge omega = h_+ on sign-mixed hierarchy classes (263/558 pairs at
B = 6, witness (3,12,011110)); the omega-sound cap is the exact identity
sum h_+ = (sum |h| + 2^s hcube(empty))/2; single-sign (flat) territory is
unaffected so the #791 reduction stands; the corrected rank-one rule is
scalar-accounting-sound with 0 violations and reaches every charged class's
scalar cap at B = 6 (421/421, computed).

Note:     `experimental/notes/thresholds/omega_sound_emission_floor.md`.
Verifier: `experimental/scripts/verify_omega_sound_emission_floor.py`
          (12/12, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trig/charge content lives in the note and the scans.  This module is the
DECIDABLE arithmetic shadow (stdlib-only `native_decide`, no mathlib, no
`sorry`): the pointwise positive-part identity on integers, the depth-1
G-sign alternation behind S3's single-sign safety, and the digit facts
locating the witness residue.
-/

namespace OmegaSoundEmissionFloor

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

/-! ## 1. The S2 identity's integer shadow: `2 max(x,0) = |x| + x`. -/

theorem positive_part_identity :
    ∀ n ∈ List.range 201,
      2 * max ((n : Int) - 100) 0
        = ((n : Int) - 100).natAbs + ((n : Int) - 100) := by
  native_decide

/-! ## 2. Depth-1 G-sign alternation behind S3: with
    `3 G_{1,r}(l) = wtil(l) - wtil(l+1)` (`r in {1,2}`), the sign is
    decided by parity -- positive on the realized parity (`wtil(l) > 0`,
    `wtil(l+1) = 0` for `l < 6`), negative on the opposite one.  At
    depth 1 the class value is `h = 2 G(s_low) cos(2 pi r tau/3)` with
    `cos = -1/2` CONSTANT over the cube, so `h = -G(s_low)` throughout:
    the two sign flips (`G < 0` on odd `s_low`, `cos < 0`) cancel and
    every depth-1 top-occupied class is single-sign POSITIVE (31/31
    verified) -- exactly S3's safe territory. -/

theorem depth1_sign_alternation :
    ∀ l ∈ List.range 6,
      (l % 2 = 0 → wtil6 l > 0 ∧ wtil6 (l + 1) = 0) ∧
      (l % 2 = 1 → wtil6 l = 0 ∧ wtil6 (l + 1) > 0) := by
  native_decide

/-! ## 3. The witness residue `r = 12` at depth 3: digit word `(0,1,1)`,
    `s3 = 2`, and it sits inside the depth-1 SUBGROUP coset
    (`12 == 0 mod 3`) -- the witness class is single-sign NEGATIVE
    (zero charge, positive |hcube|), and such classes appear only in
    deeper refinements of subgroup territory, which is why flat-only
    auditing missed them. -/

theorem witness_digits :
    s3 12 3 = 2 ∧ 12 % 3 = 0 ∧ (27 - 12) % 3 = 0 := by
  native_decide

/-! ## 4. Shared class pins. -/

theorem class_pins :
    wtil6 0 = 20 ∧ wtil6 2 = 6 ∧ wtil6 4 = 2 ∧ wtil6 6 = 1 ∧
    binom 12 6 = 924 := by
  native_decide

end OmegaSoundEmissionFloor
