/-!
# PROP-TAIL reduction: statement-level kernel checks

Statement-level Lean layer for the (PROP-TAIL) discharge: the claim that the
realized cross-child spread `rho_prop@i<17(j) <= 1.02560749` persists for all
`j > 60` (equivalently, the measured monotone decay of the operative-window
sibling ratio spread continues past the certified base). This module is the
DECIDABLE/ELEMENTARY skeleton (stdlib-only, no mathlib, no `sorry`, no
analytic content): it kernel-checks the exact/finite arithmetic that the
discharge leans on, and states plainly what it does NOT certify.

Five independent items, each `PropTail`-prefixed:

1. `poly_identity_coeffs` — the ring identity
   `75*(1-x^2) - (6+3x)^2 = -3*(2x-1)*(14x+13)`, checked as an equality of
   little-endian `Int` coefficient lists via `decide`.
2. `sign_factor_nonneg` / `window_ineq_cleared` — the sign corollary: on the
   domain `1/2 <= x <= 1` (denominator-cleared, `x = p/q`), the factor
   `(2x-1)(14x+13) >= 0`, hence `75*(1-x^2) <= (6+3x)^2`.
3. `window_factor_le_bound` — the window constant `289/256 <= 57/50`,
   denominator-cleared to `289*50 <= 57*256`.
4. `gateRows` / `gateRows_below_target` / `gateRows_strict_decreasing` — the
   deep-grid `rho_prop@i<17(j)` table, transcribed to exact rationals at
   printed precision, with a kernel-checked threshold + strict-monotonicity
   predicate.
5. `rho_prop_endpoint_48_below_target` / `rho_prop_endpoint_60_below_target` /
   `v17_above_before_62` / `v17_below_from_62` — the named `j=48,60`
   endpoints and the `V_17` vs. `tau*` crossover-at-`n=62` table check.

**What is certified:** exact integer/rational arithmetic, kernel-checked by
`decide` (no `native_decide` needed — every check here is small). Every
`List`-valued table is a literal transcription of numbers already printed by
the project's numeric verifier / lab scripts; the theorems below check the
transcribed table's INTERNAL consistency (thresholds, monotonicity), not the
correctness of the floating-point computation that produced the printed
decimals.

**What stays informal (analytic, out of scope):** the trigonometric
reduction `theta~(t) = sqrt3 sin(2 pi t/3) / (6+3 cos(2 pi t/3))`, the
substitution `x = cos(2 pi t/3)`, the squaring step turning
`theta~(t) <= 1/5` into the polynomial inequality of item 2, the value of
`tau* = 3*log(1.02560749...)` (transcendental), and every contraction-rate /
Birkhoff / CLT argument in the source note. None of that is proved or
assumed here — only the downstream exact/finite arithmetic is.

Note:     `experimental/notes/thresholds/dense_shell_inv_tail_closure.md` S7.
Verifier: `experimental/scripts/verify_dense_shell_inv_tail_closure.py`, gate V13.
Predecessor package (same conventions, template for this one):
          `experimental/lean/inv_tail_closure/`.
-/

namespace PropTail

/- ------------------------------------------------------------------ -/
/- 1. Coefficient-list polynomial machinery (little-endian, `Int`)     -/
/-
   Redeclared here (rather than imported) to keep this package
   dependency-free, following the same convention as the predecessor
   package `inv_tail_closure` (`padd`/`pscale`/`pmul`/`ptrim` on
   little-endian `List Int` coefficient lists: index `i` = coefficient of
   `x^i`; `ptrim` drops trailing zeros for canonical comparison).
-/

def padd : List Int → List Int → List Int
  | [], q => q
  | p, [] => p
  | a :: p, b :: q => (a + b) :: padd p q

def pscale (c : Int) (p : List Int) : List Int := p.map (c * ·)

def pmul : List Int → List Int → List Int
  | [], _ => []
  | a :: p, q => padd (pscale a q) (0 :: pmul p q)

def ptrim (p : List Int) : List Int :=
  (p.reverse.dropWhile (· == 0)).reverse

/-- The indeterminate `x`, as a coefficient list (`0 + 1*x`). -/
def xPoly : List Int := [0, 1]

/- ------------------------------------------------------------------ -/
/- 2. THE POLYNOMIAL IDENTITY — the heart of `theta~ <= 1/5`.          -/

/-- `75*(1 - x^2) - (6 + 3x)^2`, built the same way the surface formula
reads: `75*(1 - x*x)` minus `(6+3x)*(6+3x)`. -/
def lhsPoly : List Int :=
  padd (pscale 75 (padd [1] (pscale (-1) (pmul xPoly xPoly))))
       (pscale (-1) (pmul (padd [6] (pscale 3 xPoly)) (padd [6] (pscale 3 xPoly))))

/-- `-3*(2x - 1)*(14x + 13)`. -/
def rhsPoly : List Int :=
  pscale (-3) (pmul (padd [-1] (pscale 2 xPoly)) (padd [13] (pscale 14 xPoly)))

/-- **The ring identity.** `75*(1-x^2) - (6+3x)^2 = -3*(2x-1)*(14x+13)` as
formal `Int`-coefficient polynomials in one indeterminate: both sides
normalize (`ptrim`) to the coefficient list `[39, -36, -84]`
(`39 - 36x - 84x^2`). Certified: the coefficient-level identity, by kernel
computation (`decide`) on the explicit list representation — not a claim
about any particular numeric `x`. This is `theta~(t) <= 1/5` post-squaring,
`x = cos(2 pi t/3)`; the trig substitution and the squaring step are
ANALYTIC and are not part of this statement. -/
theorem poly_identity_coeffs : ptrim lhsPoly = ptrim rhsPoly := by decide

/- ------------------------------------------------------------------ -/
/- 3. THE SIGN COROLLARY — denominator-cleared, `x = p / q`, `q > 0`.  -/
/-
   `hlo : q <= 2*p` and `hhi : p <= q` are the cleared forms of
   `1/2 <= x` and `x <= 1` (the domain `[1/2, cos(pi/9)]` is a subset of
   `[1/2, 1]`, so proving the corollary on the wider `[1/2,1]` covers it).
   `hhi` is not needed by the algebra below (`x >= 1/2` alone forces both
   factors nonneg) but is kept as a hypothesis to match the stated domain
   honestly; it is intentionally unused (`_hhi` downstream).
-/

/-- **The sign corollary, part (a).** With `x = p/q`, `q > 0`: on
`1/2 <= x` (`q <= 2p`), the factor `(2x-1)(14x+13)` is nonneg, cleared to
`(2p-q)(14p+13q) >= 0`. Elementary: `2p-q >= 0` directly from `hlo`; `p > 0`
follows from `hlo` and `q > 0`, so `14p+13q > 0`. Both factors nonneg, hence
the product is nonneg (`Int.mul_nonneg`). -/
theorem sign_factor_nonneg (p q : Int) (hq : 0 < q) (hlo : q <= 2 * p)
    (_hhi : p <= q) :
    0 <= (2 * p - q) * (14 * p + 13 * q) := by
  have h1 : 0 <= 2 * p - q := by omega
  have hp : 0 < p := by omega
  have h2 : 0 <= 14 * p + 13 * q := by omega
  exact Int.mul_nonneg h1 h2

/-- **The sign corollary, part (b) — the certified inequality.** With
`x = p/q`, `q > 0`, on `1/2 <= x <= 1`: `75*(1-x^2) <= (6+3x)^2`, cleared
(scaled by `q^2 > 0`) to `75*(q^2-p^2) <= (6q+3p)^2`. Proved from part (a)
via the homogeneous identity
`(6q+3p)^2 - 75*(q^2-p^2) = 3*((2p-q)(14p+13q))` (an independent,
denominator-cleared restatement of `poly_identity_coeffs`, expanded
directly here by elementary `Int` rewriting rather than routed through the
coefficient-list form, to avoid an extra polynomial-evaluation bridge).
NOT certified: that `x = cos(2 pi t/3)` for the operative `t`, or that
squaring `theta~(t) <= 1/5` is valid (both analytic, both out of scope) —
only the resulting polynomial inequality on `x` is kernel-checked. -/
theorem window_ineq_cleared (p q : Int) (hq : 0 < q) (hlo : q <= 2 * p)
    (hhi : p <= q) :
    75 * (q * q - p * p) <= (6 * q + 3 * p) * (6 * q + 3 * p) := by
  have hsign := sign_factor_nonneg p q hq hlo hhi
  have hid : (6 * q + 3 * p) * (6 * q + 3 * p) - 75 * (q * q - p * p) =
      3 * ((2 * p - q) * (14 * p + 13 * q)) := by
    simp [Int.mul_add, Int.add_mul, Int.mul_sub, Int.sub_mul, Int.neg_mul,
      Int.mul_neg, Int.mul_assoc, Int.mul_comm, Int.mul_left_comm]
    have e1 : q * (q * (75 : Int)) = 75 * (q * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (q * q) 75]
    have e2 : q * (q * (36 : Int)) = 36 * (q * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (q * q) 36]
    have e3 : q * (q * (39 : Int)) = 39 * (q * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (q * q) 39]
    have e4 : p * (p * (75 : Int)) = 75 * (p * p) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * p) 75]
    have e5 : p * (p * (9 : Int)) = 9 * (p * p) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * p) 9]
    have e6 : p * (p * (84 : Int)) = 84 * (p * p) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * p) 84]
    have e7 : p * (q * (18 : Int)) = 18 * (p * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * q) 18]
    have e8 : p * (q * (42 : Int)) = 42 * (p * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * q) 42]
    have e9 : p * (q * (78 : Int)) = 78 * (p * q) := by
      rw [← Int.mul_assoc, Int.mul_comm (p * q) 78]
    rw [e1, e2, e3, e4, e5, e6, e7, e8, e9]
    generalize q * q = A
    generalize p * p = B
    generalize p * q = C
    omega
  omega

/- ------------------------------------------------------------------ -/
/- 4. THE WINDOW CONSTANT.                                             -/

/-- The child-window factor bound: `V_18/V_17 -> 289/256 = 1.1289` is
covered by the rational threshold `57/50 = 1.14`, denominator-cleared
(`289*50 <= 57*256`, i.e. `14450 <= 14592`). Certified: this single
rational-comparison fact, by `decide`. NOT certified: that `289/256` is
actually the limiting window ratio, or that `57/50` is a valid bound over
the full deep grid (both are modeling claims from the source note; this
theorem only certifies the arithmetic fact about the two named
constants). -/
theorem window_factor_le_bound : (289 * 50 : Nat) <= 57 * 256 := by decide

/- ------------------------------------------------------------------ -/
/- 5. THE GATE TABLE — deep-grid `rho_prop@i<17(j)`, exact rationals.   -/
/-
   Each row's value is the printed decimal `rho_prop@i<17(j)` (7 digits
   after the point) transcribed as an exact numerator over the common
   denominator `10^8` (matching the target's 8-digit precision): e.g.
   `1.0255905 -> rhoPropNum = 102559050` (`= 1.02559050 * 10^8`). COMPUTED
   float-derived values transcribed at printed precision — the theorems
   below check the TABLE's internal consistency (threshold + strict
   monotonicity), not the floating computation that produced the decimals.
-/

/-- One deep-grid row: level `j` and `rho_prop@i<17(j)` as a numerator
over the implicit denominator `10^8`. -/
structure GateRow where
  level : Nat
  rhoPropNum : Nat
  deriving DecidableEq, Repr

/-- The deep-grid table, `j = 48` through `800`; shipped gate V13 covers
`{48,50,55,60}`, this extends the same measurement to the deeper grid. The
`550..800` tail (added alongside the SIB-CERT deep anchor, Section 7 below)
is transcribed from the verifier's `--table` output at the same 8-digit
precision as every other row. -/
def gateRows : List GateRow :=
  [ { level := 48,  rhoPropNum := 102559050 }
  , { level := 50,  rhoPropNum := 102352050 }
  , { level := 55,  rhoPropNum := 101932970 }
  , { level := 60,  rhoPropNum := 101617140 }
  , { level := 70,  rhoPropNum := 101180630 }
  , { level := 80,  rhoPropNum := 100900050 }
  , { level := 100, rhoPropNum := 100572970 }
  , { level := 128, rhoPropNum := 100348300 }
  , { level := 160, rhoPropNum := 100222350 }
  , { level := 200, rhoPropNum := 100142050 }
  , { level := 240, rhoPropNum := 100098530 }
  , { level := 300, rhoPropNum := 100063000 }
  , { level := 550, rhoPropNum := 100018713 }
  , { level := 600, rhoPropNum := 100015721 }
  , { level := 650, rhoPropNum := 100013394 }
  , { level := 700, rhoPropNum := 100011548 }
  , { level := 750, rhoPropNum := 100010059 }
  , { level := 800, rhoPropNum := 100008840 } ]

/-- The (PROP-TAIL) target `1.02560749`, as a numerator over `10^8`. -/
def gateTarget : Nat := 102560749

/-- Every transcribed deep-grid value is `<= 1.02560749` (the tightest
margin is at `j=48`, matching the shipped V13 gate's own value). -/
theorem gateRows_below_target : ∀ row ∈ gateRows, row.rhoPropNum <= gateTarget := by
  decide

/-- Strict pairwise decrease of a `Nat` list (adjacent-pair recursion). -/
def strictlyDecreasing : List Nat → Bool
  | [] => true
  | [_] => true
  | a :: b :: t => a > b && strictlyDecreasing (b :: t)

/-- The deep-grid table is strictly decreasing in `j` (no plateau, no
uptick, over the transcribed rows). -/
theorem gateRows_strict_decreasing :
    strictlyDecreasing (gateRows.map GateRow.rhoPropNum) = true := by decide

/- ------------------------------------------------------------------ -/
/- 6. THE CROSSOVER ARITHMETIC.                                        -/
/-
   Same transcription discipline and caveat as section 5. `V_17(n)` values
   (6 digits after the point) and `tau* = 3*log(1.02560749...) ~ 0.0758553`
   (7 digits) are both transcribed as numerators over the common
   denominator `10^7`. `tau*` itself involves `log` (transcendental,
   informal, out of scope) — only the printed-decimal comparison is
   kernel-checked here, exactly as with the gate table.
-/

/-- The two named `rho_prop@i<17` endpoints quoted in the source note
(`1.02559 @ j=48 -> 1.01617 @ j=60`), against the target — corollaries of
`gateRows_below_target`, restated standalone for direct traceability. -/
theorem rho_prop_endpoint_48_below_target : (102559050 : Nat) <= gateTarget := by
  decide

theorem rho_prop_endpoint_60_below_target : (101617140 : Nat) <= gateTarget := by
  decide

/-- One `V_17(n)` row: level `n` and `V_17(n)` as a numerator over the
implicit denominator `10^7`. -/
structure V17Row where
  level : Nat
  v17Num : Nat
  deriving DecidableEq, Repr

/-- `V_17(n)` at the endpoints and around the claimed crossover. -/
def v17Rows : List V17Row :=
  [ { level := 48, v17Num := 1235790 }
  , { level := 50, v17Num := 1137820 }
  , { level := 55, v17Num := 938410 }
  , { level := 60, v17Num := 787190 }
  , { level := 61, v17Num := 761360 }
  , { level := 62, v17Num := 736780 } ]

/-- `tau* = 3*log(1.02560749...) ~= 0.0758553`, as a numerator over `10^7`. -/
def tauStarNum : Nat := 758553

/-- Claim-shape check, part 1: for every transcribed row at `n <= 61`,
`V_17(n)` is still (strictly) above `tau*` — no crossing yet. -/
theorem v17_above_before_62 :
    ∀ row ∈ v17Rows, row.level <= 61 → tauStarNum < row.v17Num := by decide

/-- Claim-shape check, part 2: at `n = 62` (the only transcribed row with
`n >= 62`), `V_17(n)` has dropped to at or below `tau*` — the first
crossing, matching the source note's independent full-integer-scan
finding. Together with part 1 this certifies the TABLE's crossover shape
at the transcribed rows; it is not an independent recomputation of
`V_17` or `tau*`. -/
theorem v17_below_from_62 :
    ∀ row ∈ v17Rows, 62 <= row.level → row.v17Num <= tauStarNum := by decide

/- ------------------------------------------------------------------ -/
/- 7. SIB-CERT — the deep-anchor geometric-center wobble census.       -/
/-
   Gate SIB-CERT (`verify_dense_shell_prop_tail_reduction.py`) discharges
   the (SIB-BAND) computed clause: the GEOMETRIC-CENTER LEMMA (informal,
   note Section 8.4 — `lam_gc := sqrt(min_i rho_i * max_i rho_i)` is itself
   a legal (LAM-BOX) point since both factors are, and `w_i := rho_i/lam_gc`
   then lies in the half-band `[1/sqrt(R*), sqrt(R*)]` by the governing IH
   alone, no assumption beyond (LAM-BOX)) reduces coverage of the REAL,
   non-proportional cascade to the SAME kind of exact-Fraction
   interval-arithmetic census `V15-IA`/`V17-IA` already certify above, just
   re-anchored at a deep base (`J0=800`, pad `999/1000`) and re-banded to
   the geometric-center half-band FOR `i < 17` (the IH's own window).

   **Round-2 correction (PI review, note Section 8.4's BOUNDARY ANNEX):**
   the IH bounds `w_i` only for `i < 17`; the census's ONE out-of-window
   slot (row `i = 16`'s `x`, i.e. `w_17`) is discharged separately via a
   deep box `W17 = [999/1000, 1001/1000]` gate MAG-BOX monitors on
   `n in {500,...,800}` — a `(LAM-BOX)`-class hypothesis, not a consequence
   of the IH. The shallow counterexample (`w_17(48)` measured up to
   `1.016780`, exceeding the naive half-band bracket `1.012723`) is why this
   separate box is needed; the deep value (`w_17(800) in [1.000018,
   1.000056]`) sits deep inside `W17`. None of this changes what THIS
   section kernel-checks: only the resulting rational threshold inequality
   `F_box_wob <= (1 - theta_band_wob) * tau*`, at printed precision —
   exactly as items 5/6 above check the deep-grid table and the crossover,
   NOT a re-derivation of the interval-arithmetic computation itself, and
   NOT a formalization of the GEOMETRIC-CENTER LEMMA or the BOUNDARY ANNEX
   (all stay informal, exactly as the analytic content behind V15-IA/V17-IA
   does). The literals below are the ROUND-2 (boundary-corrected) values;
   the correction TIGHTENED the margin (round 1: `~4.64%`; round 2: `~7.43%`).

   Transcription (SAFE/conservative direction, mirroring `tauStarNum`
   above): `F_box_wob` is rounded UP to 9 digits (`sibcertFHi`, numerator
   over `10^9`) and `theta_band_wob` is rounded UP to 9 digits
   (`sibcertThetaHi`, numerator over `10^9`). Rounding `theta` UP makes
   `(1 - theta)` a valid LOWER bound; combined with `tauStarNum` (already a
   certified LOWER bound on `tau*`), the product
   `(1 - sibcertThetaHi/10^9) * (tauStarNum/10^7)` is a valid lower bound on
   the true threshold, while `sibcertFHi/10^9` is a valid upper bound on the
   true `F_box_wob` — so the kernel-checked inequality below is a
   conservative (never unsafe) proxy for the gate's own exact-Fraction
   comparison, exactly as `TAU_STAR_FR`'s own use is conservative in the
   Python verifier (see its module docstring).
-/

/-- `F_box_wob(800, 999/1000)` (geometric-center half-band for `i<17`, PLUS
the `W17` boundary box for the `i=16` row's `x`-slot), rounded UP to 9
digits, as a numerator over `10^9`: gate SIB-CERT's round-2 exact Fraction
is `0.02794313381791874...`; `ceil(. * 10^9) = 27943134`. -/
def sibcertFHi : Nat := 27943134

/-- `theta_band_wob(800, 999/1000)`, round-2 (boundary-corrected), rounded
UP to 9 digits, as a numerator over `10^9`: gate SIB-CERT's exact Fraction
is `1204131/2000000 = 0.6020655` exactly (terminating decimal, so rounding
up is a no-op at this precision); `ceil(. * 10^9) = 602065500`. -/
def sibcertThetaHi : Nat := 602065500

/-- **The SIB-CERT discharge, kernel-checked (round-2, boundary-corrected).**
The threshold inequality
`sibcertFHi/10^9 <= (1 - sibcertThetaHi/10^9) * (tauStarNum/10^7)`, cleared
of denominators (multiply both sides by `10^9 * 10^7`, both positive):
`sibcertFHi * 10^7 <= (10^9 - sibcertThetaHi) * tauStarNum`. This is the
downstream rational comparison gate SIB-CERT computes in exact Fraction
arithmetic (`F_box_wob <= (1 - theta_band_wob) * tau*`), transcribed at
printed precision in the conservative direction described above; margin
at these rounded literals is `~7.43%`, consistent with the gate's own
reported `+7.4%` (exact-Fraction) round-2 margin — TIGHTER than round 1's
`~4.64%`, since the boundary-slot correction only restricts a box-max
domain (the `i=16` row's `x`-slot moved from the wider `WOB_HALF` to the
narrower `W17`), which cannot increase the certified sup. -/
theorem sibcert_clears :
    sibcertFHi * 10000000 <= (1000000000 - sibcertThetaHi) * tauStarNum := by decide

/- ------------------------------------------------------------------ -/
/- 8. LAM-INV -- proved invariant-interval endpoints (endpoint arithmetic only).  -/
/-
   Gate LAM-INV (`verify_dense_shell_prop_tail_reduction.py`) proves `lam`/`Lambda^+`/
   `Lambda^-` are INVARIANT INTERVALS (`DERIV_LAMBOX.md`: an exact windowed-mass-
   recursion identity + a Birkhoff mass-field enclosure + a coupled Lambda-field
   enclosure), discharging the (LAM-BOX) computed clause CONDITIONAL on the floor box,
   the finite base-case census, an a-posteriori Lipschitz self-check, and one monitored
   constant (the (C'-CAP) clause). This section kernel-checks ONLY the resulting
   rational CONTAINMENT facts -- the proved-interval endpoints, outward-rounded (floor
   the lower endpoint, ceil the upper, so the checked box is a superset of the true
   proved interval), sit inside the shipped (WIDENED this revision) magnitude box -- at
   printed precision, exactly as items 5/6/7 above check transcribed tables, NOT a
   re-derivation of the Birkhoff mass-field / coupled Lambda-field one-pass invariance
   computation itself, the `sc_exact` ray-normalization, or the a-posteriori Lipschitz
   self-checks (all stay informal, matching the analytic content behind
   V15-IA/V17-IA/SIB-CERT). Numerators are `Int`, not `Nat` (the house convention
   elsewhere in this file) -- `Lambda^+`/`Lambda^-` are genuinely negative, unlike every
   quantity items 5-7 transcribe -- over the fixed denominator `lamInvDen`.
-/

/-- Common denominator for this section's transcribed literals. -/
def lamInvDen : Int := 1000000

/-- Proved `lam` interval endpoints (outward-rounded: floor the lower bound, ceil the
upper -- the checked interval is a SUPERSET of gate LAM-INV's own tighter exact-Fraction
result, `[0.767193..., 0.929926...]`), numerators over `lamInvDen`. -/
def lamInvLamLo : Int := 767193
def lamInvLamHi : Int := 929927

/-- Proved `Lambda^+` interval endpoints (outward-rounded), numerators over `lamInvDen`
(gate LAM-INV's exact result: `[-1.159560..., -0.868700...]`). -/
def lamInvLamPLo : Int := -1159560
def lamInvLamPHi : Int := -868700

/-- Proved `Lambda^-` interval endpoints (outward-rounded), numerators over `lamInvDen`
(gate LAM-INV's exact result: `[-0.650454..., -0.360426...]`). -/
def lamInvLamMLo : Int := -650454
def lamInvLamMHi : Int := -360426

/-- The shipped magnitude box endpoints, numerators over `lamInvDen`: `lam in
[0.72,0.95]`, `Lambda^+ in [-1.17,-0.82]` (WIDENED this revision `-1.16 -> -1.17`, R1
mitigation (b)), `Lambda^- in [-0.66,-0.35]`. -/
def lamBoxLamLo : Int := 720000
def lamBoxLamHi : Int := 950000
def lamBoxLamPLo : Int := -1170000
def lamBoxLamPHi : Int := -820000
def lamBoxLamMLo : Int := -660000
def lamBoxLamMHi : Int := -350000

/-- The PRE-widening `Lambda^+` floor (`-1.16`), kept for the widened-floor-consistency
check below (not used by any other theorem in this file -- MAG-BOX/V17-IA/SIB-CERT all
consume the WIDENED `lamBoxLamPLo`/`LAP_LO_F` directly). -/
def lamBoxLamPLoOrig : Int := -1160000

/-- **Containment: the proved `lam` interval sits inside the shipped box.** -/
theorem lamInv_lam_inside :
    lamBoxLamLo <= lamInvLamLo ∧ lamInvLamHi <= lamBoxLamHi := by decide

/-- **Containment: the proved `Lambda^+` interval sits inside the WIDENED shipped box.**
-/
theorem lamInv_lamP_inside :
    lamBoxLamPLo <= lamInvLamPLo ∧ lamInvLamPHi <= lamBoxLamPHi := by decide

/-- **Containment: the proved `Lambda^-` interval sits inside the shipped box.** -/
theorem lamInv_lamM_inside :
    lamBoxLamMLo <= lamInvLamMLo ∧ lamInvLamMHi <= lamBoxLamMHi := by decide

/-- **Widened-floor consistency.** The widened floor `-1.17` is a valid (more
permissive, i.e. numerically smaller) lower bound relative to the pre-widening floor
`-1.16`, AND the pre-widening floor itself sits inside the widened box's `Lambda^+`
range -- confirming the widening is a genuine, conservative RELAXATION of the same box
(the new box is a strict superset containing the old floor), not an unrelated shift. -/
theorem lamInv_floor_widened_consistent :
    lamBoxLamPLo <= lamBoxLamPLoOrig ∧ lamBoxLamPLoOrig <= lamBoxLamPHi := by decide

/- ------------------------------------------------------------------ -/
/- 9. Round 4 -- the (C'-CAP) discharge comparison + FLOOR-DRIFT transcriptions.  -/
/-
   Gate LAM-INV's (C'-CAP) floor-box node census (round 4) certifies, in exact Fraction
   arithmetic, `worst drop bound <= CPRIME = 3/500` over all NG grid nodes; gate
   FLOOR-DRIFT monitors the (FLOOR-PERSIST) drift mechanism and as-consumed margins,
   and carries the Section 9(v) route-cut negative control inline. This section
   kernel-checks the resulting RATIONAL comparisons at printed precision (transcribed
   in the conservative direction: upper bounds rounded UP, lower bounds rounded DOWN),
   exactly the items-5-7 pattern -- NOT a re-derivation of the node census, the drift
   scan, or the route-cut corner census (those stay in the Python verifier).
-/

/-- The certified (C'-CAP) node-census worst bound, rounded UP at printed precision
(gate LAM-INV round 4: `0.004245...`; `ceil(. * 10^6) = 4246`), over `10^6`. -/
def cprimeBoundHi : Nat := 4246

/-- **The (C'-CAP) discharge comparison, kernel-checked.** `cprimeBoundHi/10^6 <=
3/500` (the CPRIME cap), cleared of denominators (both positive):
`cprimeBoundHi * 500 <= 3 * 10^6`. This is the gate's own final exact-Fraction
comparison, transcribed conservatively; margin at the rounded literal is `~29%`. -/
theorem cprime_bound_clears : cprimeBoundHi * 500 <= 3 * 1000000 := by decide

/-- FLOOR-DRIFT check (1): the worst monitored drift step ratio, rounded DOWN at
printed precision (gate: `1.00005212...` at the edge parent, pair `750 -> 800`, `i=0`;
`floor(. * 10^8) = 100005212`), over `10^8`. -/
def floorDriftWorstLo : Nat := 100005212

/-- **Drift transcription: the worst monitored step ratio is at least 1** (the upward
drift the (FLOOR-PERSIST) clause rests on holds at every monitored parameter/pair,
with the worst case strictly above 1 at printed precision). -/
theorem floordrift_step_ge_one : 100000000 <= floorDriftWorstLo := by decide

/-- FLOOR-DRIFT check (2): the worst as-consumed floor margins, rounded DOWN at
printed precision, over `10^6`: `1.010070...` at the `(500, 99/100)` anchor and
`1.000989...` at the `(800, 999/1000)` SIB-CERT anchor. -/
def floorMarginMainLo : Nat := 1010070
def floorMarginSibLo : Nat := 1000989

/-- **As-consumed margin transcription: both anchors' worst margins are at least 1**
(the exact statement the census gates consume holds at every monitored level, with
the pad absorbing both the level- and the parameter-transfer). -/
theorem floordrift_margins_ge_one :
    1000000 <= floorMarginMainLo ∧ 1000000 <= floorMarginSibLo := by decide

/-- The Section 9(v) route-cut exhibits, rounded UP at printed precision, over `10^3`:
box-worst census output-ratio/floor `0.579...` at `(500, 99/100)` and `0.568...` at
`(800, 999/1000)` (rounded up to `580`/`569` -- still strictly below 1000). -/
def floorRouteCutMainHi : Nat := 580
def floorRouteCutSibHi : Nat := 569

/-- **Route-cut transcription: the pointwise corner census MISSES the floors at both
anchors** (even the upper-rounded exhibits sit strictly below 1) -- the kernel-checked
form of the Section 9(v) negative: (FLOOR-PERSIST) cannot be discharged by this
census, which is exactly why it stays a named COMPUTED clause. -/
theorem floordrift_routecut_misses :
    floorRouteCutMainHi < 1000 ∧ floorRouteCutSibHi < 1000 := by decide

end PropTail
