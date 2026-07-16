/-!
# The shell-mass spectral law: decidable counting shadow

Maps to **hard input 2**: tenth packet of the arc.  The note proves the
digit-shell generating identity (spectral masses decompose in the
chart's own product algebra), computes the exact shell failure table
(bimodal; the all-dense shell crosses the eta -> 0 failing threshold at
B = 12 -- the first explicit proper failing band), and shows the dense
shell is the level-B signature cube: not bounded-depth measurable, but
digit-product structured with factorizing digit sums.

Note:     `experimental/notes/thresholds/shell_mass_spectral_law.md`.
Verifier: `experimental/scripts/verify_shell_mass_spectral_law.py`
          (13/13 default, 17/17 with --deep, tamper 5/5).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
trig identity and the R-table live in the scans.  This module is the
DECIDABLE arithmetic shadow (stdlib-only `native_decide`, no mathlib,
no `sorry`): dense-shell counts, the digit-product factorization on
pinned profiles, the resonant point's membership, and depth-split
witnesses.
-/

namespace ShellMassSpectralLaw

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Nonzero canonical balanced-ternary digits of `y mod 3^ndig`. -/
def s3 (y ndig : Nat) : Nat :=
  match ndig with
  | 0 => 0
  | n + 1 =>
    let d := y % 3
    if d = 0 then s3 (y / 3) n
    else if d = 1 then 1 + s3 (y / 3) n
    else 1 + s3 (y / 3 + 1) n

/-! ## 1. The dense shell is the 2^B-point signature cube. -/

theorem dense_shell_count :
    ∀ B ∈ [2, 4, 6, 8],
      ((List.range (3 ^ B)).filter (fun a => s3 a B = B)).length
        = 2 ^ B := by
  native_decide

/-- The resonant point `j* = (3^B - 1)/2` (all-ones digits) is a
    dense-shell point. -/
theorem resonant_in_dense_shell :
    ∀ B ∈ [2, 4, 6, 8, 10], s3 ((3 ^ B - 1) / 2) B = B := by
  native_decide

/-! ## 2. Depth-split witnesses behind Theorem D(b): at B = 6, for every
    k < 6 the j*-coset (all-ones fixed low digits) contains BOTH a
    dense-shell member and a non-member -- the split witness (conjuncts
    2-3).  Conjunct 1 is auxiliary: the subgroup coset r = 0 is
    MEMBERLESS (low digits vanish), which is why it cannot serve as the
    witness. -/

theorem depth_split_witnesses :
    ∀ k ∈ [1, 2, 3, 4, 5],
      (List.range (3 ^ (6 - k))).any
          (fun hi => s3 (3 ^ k * hi) 6 = 6) = false ∧
      ((List.range (3 ^ (6 - k))).filter
          (fun hi => s3 ((3 ^ 6 - 1) / 2 % 3 ^ k + 3 ^ k * hi) 6 = 6)).length
        > 0 ∧
      ((List.range (3 ^ (6 - k))).filter
          (fun hi => ¬ s3 ((3 ^ 6 - 1) / 2 % 3 ^ k + 3 ^ k * hi) 6 = 6)).length
        > 0 := by
  native_decide

/-! ## 3. The digit-product factorization (Theorem D(d)) on pinned
    profiles: the full profile gives the census, the nonzero-indicator
    profile gives the dense count. -/

theorem census_via_full_profile :
    ∀ k ∈ [1, 2, 3, 4, 5, 6], ∀ j ∈ List.range 7, j ≤ k →
      ((List.range (3 ^ k)).filter (fun a => s3 a k = j)).length
        = binom k j * 2 ^ j := by
  native_decide

theorem dense_via_indicator_profile :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7, 8],
      ((List.range (3 ^ k)).filter (fun a => s3 a k = k)).length
        = 2 ^ k := by
  native_decide

/-! ## 4. Shared class pins. -/

theorem class_pins :
    binom 12 6 = 924 ∧ binom 16 8 = 12870 ∧
    (3 ^ 6 - 1) / 2 = 364 ∧ (3 ^ 12 : Nat) = 531441 := by
  native_decide

end ShellMassSpectralLaw
