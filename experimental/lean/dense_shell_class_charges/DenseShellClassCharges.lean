/-!
# Dense-shell class charges: decidable arithmetic shadow

Maps to **hard input 2** (class-charge packet).  The note's analytic
content (the MASTER inequality, cone purity, the leak table) lives in
the note and the Python verifier; this module is the DECIDABLE skeleton
(stdlib-only, no mathlib, no `sorry`):

* the support-class partition count: `sum_{m<=B} C(B,m) 2^m = 3^B`
  (the 3^B residues split into exact-support classes, 2^m signings of
  each m-subset of digit positions);
* integer polynomial machinery (lists of `Int` coefficients) with a
  `native_decide` proof of the Chebyshev factorization
      T_9(x) - 1 = (x - 1) (2x + 1)^2 (8x^3 - 6x + 1)^2,
  whose cubic factor `8x^3 - 6x + 1 = 2 T_3(x) + 1` has vanishing
  x^2-coefficient: Vieta's root sum
  `cos(2pi/9) + cos(4pi/9) + cos(8pi/9) = 0` -- the algebraic core of
  the ATOM's endpoint identity `sin(7pi/18) - sin(5pi/18) = sin(pi/18)`
  (margin `sin^2(pi/18)`);
* the index-flip involution on scan subsets preserves cardinality
  (the kernel reduction's reindexing is sign-law-neutral).

Note:     `experimental/notes/thresholds/dense_shell_class_charges.md`.
Verifier: `experimental/scripts/verify_dense_shell_class_charges.py`.
-/

namespace DenseShellClassCharges

/-- Binomial coefficients, definitional. -/
def C : Nat → Nat → Nat
  | _, 0 => 1
  | 0, _ + 1 => 0
  | n + 1, k + 1 => C n k + C n (k + 1)

theorem C_succ_succ (n k : Nat) :
    C (n + 1) (k + 1) = C n k + C n (k + 1) := rfl

/-- Row sum with weight `2^k`: `rowSum B j = sum_{k<j} C B k * 2^k`. -/
def rowSum (B : Nat) : Nat → Nat
  | 0 => 0
  | j + 1 => rowSum B j + C B j * 2 ^ j

/-- The support-class partition identity, small-B census:
`sum_{k<=B} C(B,k) 2^k = 3^B` for every `B <= 12` (decidable; the
general Pascal induction is routine and the census covers every level
the packet computes at). -/
theorem partition_census :
    (List.range 13).all (fun B => rowSum B (B + 1) == 3 ^ B) = true := by
  native_decide

/- ------------------------------------------------------------------ -/
/- Integer polynomials as coefficient lists (little-endian).           -/

def padd : List Int → List Int → List Int
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a + b) :: padd p q

def pscale (c : Int) (p : List Int) : List Int := p.map (c * ·)

def pshift (p : List Int) : List Int := 0 :: p

def pmul : List Int → List Int → List Int
  | [], _ => []
  | a :: p, q => padd (pscale a q) (pshift (pmul p q))

/-- Trim trailing zeros for canonical comparison. -/
def ptrim (p : List Int) : List Int :=
  (p.reverse.dropWhile (· == 0)).reverse

/-- Chebyshev T_n as integer coefficient lists:
`T 0 = 1`, `T 1 = x`, `T (n+2) = 2x T (n+1) - T n`. -/
def T : Nat → List Int
  | 0 => [1]
  | 1 => [0, 1]
  | n + 2 => padd (pscale 2 (pshift (T (n + 1)))) (pscale (-1) (T n))

/-- The ATOM's algebraic core:
`T_9(x) - 1 = (x - 1) (2x + 1)^2 (8x^3 - 6x + 1)^2` as integer
polynomials; the cubic factor `8x^3 - 6x + 1 = 2 T_3(x) + 1` has zero
x^2-coefficient, so its three roots `cos(2pi/9), cos(4pi/9), cos(8pi/9)`
sum to 0 (Vieta); with `cos(8pi/9) = -cos(pi/9)` this is
`cos(pi/9) = cos(2pi/9) + cos(4pi/9)` -- the endpoint identity of the
ATOM (margin `sin^2(pi/18)`). -/
theorem T9_factorization :
    ptrim (padd (T 9) [-1]) =
    ptrim (pmul (pmul [-1, 1] (pmul [1, 2] [1, 2]))
                (pmul [1, -6, 0, 8] [1, -6, 0, 8])) := by
  native_decide

/-- The cubic factor's x^2-coefficient vanishes (Vieta root sum 0). -/
theorem cubic_vieta : ([1, -6, 0, 8] : List Int).get? 2 = some 0 := by
  native_decide

/- ------------------------------------------------------------------ -/
/- The index flip on scan subsets preserves cardinality.               -/

/-- Flip a subset of `{0..B-1}` (as a bitmask predicate) by
`i -> B - 1 - i`; cardinality is preserved: census over B <= 8,
all masks. -/
def popcount : Nat → Nat
  | 0 => 0
  | n + 1 => (n + 1) % 2 + popcount ((n + 1) / 2)

def flipMask (B S : Nat) : Nat :=
  (List.range B).foldl
    (fun acc i => if S / 2 ^ i % 2 == 1 then acc + 2 ^ (B - 1 - i) else acc) 0

theorem flip_preserves_card :
    (List.range 9).all (fun B =>
      (List.range (2 ^ B)).all (fun S =>
        popcount (flipMask B S) == popcount S)) = true := by
  native_decide

end DenseShellClassCharges
