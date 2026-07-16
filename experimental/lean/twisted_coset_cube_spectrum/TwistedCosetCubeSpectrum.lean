/-!
# The twisted-coset cube spectrum: decidable counting shadow (statement stub)

Maps to **hard input 2**: sixth packet of the arc (forcing -> typing ->
reduction -> scope -> compression -> classification).  The note proves the
rank-one product law for cube spectra of depth-k hierarchy bands on the
base-3 chart:
  chat_v(D) = [D in top block] * G_{k,r}(s_low)
              * prod_top (-i sin(beta_t r) | cos(beta_t r)),
  G_{k,r}(l) = 3^{-k} sum_a e(-ar/3^k) wtil(s3(a)+l),
built on Lemma 0 (balanced-ternary uniqueness), Lemma N (support counting
N(y) = wtil(s3(y))), and the no-carry digit-block lemma.

Note:     `experimental/notes/thresholds/twisted_coset_cube_spectrum.md`.
Verifier: `experimental/scripts/verify_twisted_coset_cube_spectrum.py`
          (19/19, tamper 6/6).

Analytic results (PROVED in note + Python verifier; NOT in Lean): the
character/trig content (the product law itself, purely-imaginary k = 1
anatomy, the #805 constants) lives in the note and the scans.  This module
is the DECIDABLE arithmetic shadow (stdlib-only `native_decide`, no
mathlib, no `sorry`): the balanced digit-count census, Lemma N by brute
enumeration at B = 4, the digit-block additivity behind Theorem A's
localization, the negation symmetry behind the reality of symmetrized
spectra, and the r = 0 counting identity behind Corollary C1.
-/

namespace TwistedCosetCubeSpectrum

/-- `binom n k = C(n,k)` via the running product. -/
def binom (n k : Nat) : Nat :=
  (List.range k).foldl (fun acc i => acc * (n - i) / (i + 1)) 1

/-- Level fiber `wtil(s) = C(B-s,(B-s)/2)` on the realized parity, else 0. -/
def wtil (B s : Nat) : Nat :=
  if s ≤ B ∧ s % 2 = B % 2 then binom (B - s) ((B - s) / 2) else 0

/-- Nonzero canonical balanced-ternary digits of `y mod 3^ndig`
    (digit 2 reads as -1 with carry). -/
def s3 (y ndig : Nat) : Nat :=
  match ndig with
  | 0 => 0
  | n + 1 =>
    let d := y % 3
    if d = 0 then s3 (y / 3) n
    else if d = 1 then 1 + s3 (y / 3) n
    else 1 + s3 (y / 3 + 1) n

/-- The chart pairs at `B = 4`: `T = P u (c - P)`, `P_i = 3^i`, `c = 81`. -/
def T4 : List Nat := [1, 3, 9, 27, 80, 78, 72, 54]

/-- Element sum of the bitmask-selected subset of `T4`. -/
def maskSum (mask : Nat) : Nat :=
  (List.range 8).foldl
    (fun acc i => if mask / 2 ^ i % 2 = 1 then acc + T4.getD i 0 else acc) 0

/-- Popcount over the 8 mask bits. -/
def maskSize (mask : Nat) : Nat :=
  (List.range 8).foldl (fun acc i => acc + mask / 2 ^ i % 2) 0

/-- Brute support count at `B = 4`: size-4 subsets of `T4`, sums mod 81. -/
def bruteN4 (y : Nat) : Nat :=
  (List.range 256).foldl
    (fun acc mask =>
      if maskSize mask = 4 ∧ maskSum mask % 81 = y then acc + 1 else acc) 0

/-! ## 1. Lemma N by brute enumeration: `N(y) = wtil(s3(y))` at `B = 4`. -/

theorem lemmaN_shadow :
    ∀ y ∈ List.range 81, bruteN4 y = wtil 4 (s3 y 4) := by
  native_decide

/-- Negation symmetry `N(y) = N(-y)` (balanced digits negate): brute. -/
theorem lemmaN_negation_shadow :
    ∀ y ∈ List.range 81, bruteN4 y = bruteN4 ((81 - y) % 81) := by
  native_decide

/-- Parseval shadow: `sum_y N(y)^2 = sum_s C(B,s) 2^s wtil(s)^2` at `B = 4`. -/
theorem parseval_shadow :
    (List.range 81).foldl (fun acc y => acc + bruteN4 y * bruteN4 y) 0
      = (List.range 5).foldl (fun acc s =>
          acc + binom 4 s * 2 ^ s * wtil 4 s * wtil 4 s) 0 := by
  native_decide

/-! ## 2. The digit-count census behind `G` and Corollary C1:
    `#{a in Z_3^k : s3(a) = j} = C(k,j) 2^j`. -/

theorem digit_census :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7], ∀ j ∈ List.range 8, j ≤ k →
      ((List.range (3 ^ k)).filter (fun a => s3 a k = j)).length
        = binom k j * 2 ^ j := by
  native_decide

/-- Corollary C1's counting core: the `r = 0` table is the census-weighted
    fiber sum, `3^k G_{k,0}(l) = sum_a wtil(s3(a)+l) = sum_j C(k,j) 2^j
    wtil(j+l)` (B = 6). -/
theorem gZero_census :
    ∀ k ∈ [1, 2, 3], ∀ l ∈ List.range 7,
      (List.range (3 ^ k)).foldl (fun acc a => acc + wtil 6 (s3 a k + l)) 0
        = (List.range (k + 1)).foldl (fun acc j =>
            acc + binom k j * 2 ^ j * wtil 6 (j + l)) 0 := by
  native_decide

/-! ## 3. The digit-block lemma behind Theorem A's localization.

`embed u m B` lifts the canonical balanced integer of `u mod 3^m` into
`Z_3^B`; block additivity `s3(a 3^{B-k} + embed(u)) = s3(a) + s3(u)` is the
no-carry concatenation that makes every cube coefficient below the top
block vanish exactly. -/

def embed (u m B : Nat) : Nat :=
  if 2 * u + 1 ≤ 3 ^ m then u else 3 ^ B + u - 3 ^ m

theorem digit_block_additivity_B4 :
    ∀ k ∈ [1, 2, 3], ∀ a ∈ List.range (3 ^ k),
      ∀ u ∈ List.range (3 ^ (4 - k)),
        s3 ((a * 3 ^ (4 - k) + embed u (4 - k) 4) % 3 ^ 4) 4
          = s3 a k + s3 u (4 - k) := by
  native_decide

theorem digit_block_additivity_B6 :
    ∀ k ∈ [1, 2, 3], ∀ a ∈ List.range (3 ^ k),
      ∀ u ∈ List.range (3 ^ (6 - k)),
        s3 ((a * 3 ^ (6 - k) + embed u (6 - k) 6) % 3 ^ 6) 6
          = s3 a k + s3 u (6 - k) := by
  native_decide

/-! ## 4. Negation symmetry behind symmetrized reality:
    `s3(-a) = s3(a)` on `Z_3^k`. -/

theorem digit_negation :
    ∀ k ∈ [1, 2, 3, 4, 5, 6, 7], ∀ a ∈ List.range (3 ^ k),
      s3 ((3 ^ k - a) % 3 ^ k) k = s3 a k := by
  native_decide

/-! ## 5. Shared class pins (cross-package consistency). -/

theorem class_pins :
    wtil 6 0 = 20 ∧ wtil 6 2 = 6 ∧ wtil 6 4 = 2 ∧ wtil 6 6 = 1 ∧
    wtil 6 1 = 0 ∧ binom 12 6 = 924 := by
  native_decide

end TwistedCosetCubeSpectrum
