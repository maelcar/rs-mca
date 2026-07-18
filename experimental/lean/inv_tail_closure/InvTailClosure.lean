/-!
# INV-TAIL closure: decidable shadow

Maps to the dense-shell INV-TAIL closure packet.  The analytic content
(the CLT frame, the coupled box, the envelope ports) lives in the note
and the Python verifier; this module is the DECIDABLE/ELEMENTARY
skeleton (stdlib-only, no mathlib, no `sorry`):

* the three scalar inequalities at the heart of the CAPS <= NO-SPIKE step
  (the packet's central proved reduction), denominator-cleared over
  `Int`: writing the branch drift as `d = p/q` (`q > 0`), the branch
  range `d >= -1/4` is `-q <= 4p`, and
  - `interior_row_nonneg` (`(a/4 + d b + c/4) * 4q`): `q a + 4 p b + q c
    >= 0` from nonneg entries + no-spike `b <= a + c`;
  - `center_row_nonneg` (`((d - 1/4) a + b/4) * 4q`, odd extension):
    `(4p - q) a + q b >= 0` from nonneg entries + center no-spike
    `2a <= b`; the plus branch (`d >= 1/4`, i.e. `q <= 4p`) needs no
    no-spike input (first case; interior is monotone in `d`);
  - `aggregate_center_nonneg`: the two-branch aggregate center row, plus
    branch (`q <= 4 pp`, always, since `d_+ >= 0.383 > 1/4`) + minus
    branch, no-spike consumed only on the minus branch;
* the Chebyshev factorization `coup_threshold_core`:
  `T9(x) + 1 = (x+1) (2x-1)^2 (8x^3-6x-1)^2` (`native_decide` on integer
  polynomials): the cubic factor `8x^3 - 6x - 1 = 2 T3(x) - 1`
  (`cubic_is_2T3m1`, the consistency check) has roots `cos(pi/9),
  cos(7pi/9), cos(13pi/9)`; `cos(7pi/9)` pins the (COUP) threshold
  `4 d_+^min = 4 (sin^2(7pi/18) - 1/2) = -2 cos(7pi/9) = 1.53209...`
  as a degree-3 algebraic number (gate V10's constant);
* the trace-identity core `trace_core`: `4x^3 - 3x - 1 = (x - 1) (2x + 1)^2`,
  whose double root pins `cos(2pi/3) = -1/2` — the exact coefficient in the
  branch trace identity `d(t_+) + d(t_-) = -d(t/3)`.

All six theorems (`interior_row_nonneg`, `center_row_nonneg`,
`aggregate_center_nonneg`, `coup_threshold_core`, `cubic_is_2T3m1`,
`trace_core`) are `sorry`-free.

Note:     `experimental/notes/thresholds/dense_shell_inv_tail_closure.md`.
Verifier: `experimental/scripts/verify_dense_shell_inv_tail_closure.py`.
-/

namespace InvTailClosure

/- ------------------------------------------------------------------ -/
/- 1. The caps-step scalar inequalities (the heart of CAPS <= NO-SPIKE) -/

/-- Interior row of the difference cascade under one branch kernel,
denominator-cleared (`d = p/q`, `q > 0`; the row `a/4 + d b + c/4`
scaled by `4q`): nonneg from `-q <= 4p` (`d >= -1/4`), nonneg entries,
and no-spike `b <= a + c`. -/
theorem interior_row_nonneg (p q a b c : Int)
    (hq : 0 < q) (hd : -q <= 4 * p)
    (_ha : 0 <= a) (hb : 0 <= b) (_hc : 0 <= c)
    (hns : b <= a + c) :
    0 <= q * a + 4 * p * b + q * c := by
  have h1 : (-q) * b <= 4 * p * b :=
    Int.mul_le_mul_of_nonneg_right hd hb
  rw [Int.neg_mul, Int.mul_assoc] at h1
  rw [Int.mul_assoc]
  have h2 : q * b <= q * (a + c) :=
    Int.mul_le_mul_of_nonneg_left hns (Int.le_of_lt hq)
  rw [Int.mul_add] at h2
  generalize q * a = A at *
  generalize q * b = B at *
  generalize q * c = C at *
  generalize p * b = P at *
  omega

/-- Center row of the difference cascade (odd extension about `-1/2`),
denominator-cleared (the row `(d - 1/4) a + b/4` scaled by `4q`):
nonneg from `-q <= 4p`, nonneg entries, and the center no-spike
`2a <= b`.  For the plus branch (`q <= 4p`) the no-spike input is not
consumed. -/
theorem center_row_nonneg (p q a b : Int)
    (hq : 0 < q) (hd : -q <= 4 * p)
    (ha : 0 <= a) (hb : 0 <= b) (hcen : 2 * a <= b) :
    0 <= (4 * p - q) * a + q * b := by
  rw [Int.sub_mul, Int.mul_assoc]
  have hqb : 0 <= q * b := Int.mul_nonneg (Int.le_of_lt hq) hb
  have hqa : 0 <= q * a := Int.mul_nonneg (Int.le_of_lt hq) ha
  rcases Int.le_total q (4 * p) with h4p | h4p
  · -- plus case d >= 1/4: q*a <= 4*(p*a)
    have h1 : q * a <= 4 * p * a :=
      Int.mul_le_mul_of_nonneg_right h4p ha
    rw [Int.mul_assoc] at h1
    generalize q * a = A at *
    generalize q * b = B at *
    generalize p * a = P at *
    omega
  · -- minus case d in [-1/4, 1/4]
    have hm1 : q * (2 * a) <= q * b :=
      Int.mul_le_mul_of_nonneg_left hcen (Int.le_of_lt hq)
    rw [Int.mul_left_comm] at hm1
    rcases Int.le_total 0 p with hp | hp
    · -- p >= 0: p*a >= 0 and q*b >= 2*(q*a)
      have hpa : 0 <= p * a := Int.mul_nonneg hp ha
      generalize q * a = A at *
      generalize q * b = B at *
      generalize p * a = P at *
      omega
    · -- p < 0: multiply the center no-spike by -p >= 0
      have hnp : 0 <= -p := by omega
      have hm2 : (-p) * (2 * a) <= (-p) * b :=
        Int.mul_le_mul_of_nonneg_left hcen hnp
      rw [Int.neg_mul, Int.neg_mul, Int.mul_left_comm] at hm2
      have hdb : (-q) * b <= 4 * p * b :=
        Int.mul_le_mul_of_nonneg_right hd hb
      rw [Int.neg_mul, Int.mul_assoc] at hdb
      generalize q * a = A at *
      generalize q * b = B at *
      generalize p * a = P at *
      generalize p * b = R at *
      omega

/-- The aggregated two-branch center row: plus branch at `q <= 4 pp`
(always: `d_+ >= 0.38302 > 1/4`), minus branch at `-q <= 4 pm`; the sum
is nonneg with the no-spike input consumed ONLY on the minus branch. -/
theorem aggregate_center_nonneg (pp pm q ap bp am bm : Int)
    (hq : 0 < q) (hdp : q <= 4 * pp) (hdm : -q <= 4 * pm)
    (hap : 0 <= ap) (hbp : 0 <= bp) (ham : 0 <= am) (hbm : 0 <= bm)
    (hcenm : 2 * am <= bm) :
    0 <= ((4 * pp - q) * ap + q * bp) + ((4 * pm - q) * am + q * bm) := by
  have hplus : 0 <= (4 * pp - q) * ap + q * bp := by
    have hcoef : 0 <= 4 * pp - q := by omega
    have h1 : 0 <= (4 * pp - q) * ap := Int.mul_nonneg hcoef hap
    have h2 : 0 <= q * bp := Int.mul_nonneg (Int.le_of_lt hq) hbp
    omega
  have hminus : 0 <= (4 * pm - q) * am + q * bm :=
    center_row_nonneg pm q am bm hq hdm ham hbm hcenm
  omega

/- ------------------------------------------------------------------ -/
/- 2. Integer polynomial machinery (little-endian coefficient lists)   -/

def padd : List Int → List Int → List Int
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a + b) :: padd p q

def pscale (c : Int) (p : List Int) : List Int := p.map (c * ·)

def pmul : List Int → List Int → List Int
  | [], _ => []
  | a :: p, q => padd (pscale a q) (0 :: pmul p q)

/-- Chebyshev polynomials of the first kind, little-endian coefficients:
`T 0 = [1]`, `T 1 = [0, 1]`, `T (n+2) = 2 x T (n+1) - T n`. -/
def cheb : Nat → List Int
  | 0 => [1]
  | 1 => [0, 1]
  | n + 2 => padd (pmul [0, 2] (cheb (n + 1))) (pscale (-1) (cheb n))

/-- Trim trailing zeros for canonical comparison. -/
def ptrim (p : List Int) : List Int :=
  (p.reverse.dropWhile (· == 0)).reverse

/-- `4x^3 - 3x - 1 = (x - 1)(2x + 1)^2`: the double root pins
`cos(2pi/3) = -1/2`, the exact coefficient of the branch trace identity
`d(t_+) + d(t_-) = -d(t/3)`. -/
theorem trace_core :
    ptrim (padd (cheb 3) [-1]) =
    ptrim (pmul [-1, 1] (pmul [1, 2] [1, 2])) := by
  native_decide

/-- `T9(x) + 1 = (x + 1)(2x - 1)^2 (8x^3 - 6x - 1)^2`: the cubic factor
has roots `cos(pi/9), cos(7pi/9), cos(13pi/9)`; `cos(7pi/9)` pins the
(COUP) threshold `4 d_+^min = -2 cos(7pi/9) = 1.53209...` as a degree-3
algebraic number. -/
theorem coup_threshold_core :
    ptrim (padd (cheb 9) [1]) =
    ptrim (pmul [1, 1] (pmul (pmul [-1, 2] [-1, 2])
          (pmul [-1, -6, 0, 8] [-1, -6, 0, 8]))) := by
  native_decide

/-- The cubic factor really is `2 T3(x) - 1` (consistency of the two
shadows). -/
theorem cubic_is_2T3m1 :
    ptrim (padd (pscale 2 (cheb 3)) [-1]) = [-1, -6, 0, 8] := by
  native_decide

end InvTailClosure
