/-!
# The chart-free pruned signed bound (arithmetic formalization)

Maps to **hard input 2**: image-scale MI + MA / direct Sidon payment -- the
signed-minor clause of avdeevvadim's #716 charge-preserving dichotomy, escalated
from the depth-1 superincreasing family of #728 to a GENERAL finite abelian
source chart.

Note:     `experimental/notes/thresholds/general_pruned_signed_bound.md`.
Verifier: `experimental/scripts/verify_general_pruned_signed_bound.py`
          (193359/193359, tamper 6/6).

This module certifies the EXACT, DECIDABLE backbone of the general theorem:
1. the chart-free DENSITY CRITERION in exact integer form
     window nonempty (q=2)   <=>  M > L         (logM/logL > 1)
     window = all q>=2        <=>  L^3 <= M^2    (logM/logL >= 3/2)
   evaluated on the atlas's depth-R prefix charts (exact L by enumeration);
2. the finite per-q window predicate  prunedDecays M L q  <=>  L^(3q-2) < M^(2q)
   (the crude Theorem-I bound L^{3/2-1/q}/M < 1, cleared of the root);
3. the nonnegative/Nat layer-cake identity  sum_j |{s : b s >= j}| = sum_s b s
   (an unpruned mask of max multiplicity W_max splits into W_max pruned layers),
   together with the general signed pointwise reconstruction;
4. the #728 superincreasing family as the depth-1 special case (finite window,
   rate-limit window {3,4}, heavy-fiber crossover W^2 > L at B>=6).

HONEST NONCLAIM: the analytic `l^q` projection bounds themselves
  Theorem I : R_A(g) <= (L/M)(L delta_A)^{1/2-1/q} <= L^{3/2-1/q}/M
              (all finite abelian G, all bands A, all q>=2, |g|<=1 on |S|<=L),
  Theorem D : pruned packet  =>  c_i <= L^{1/2} <= e^{o(N)} M/L^{1-1/q},
  Theorem II: unpruned excess  >= (L^{1-1/q}/M)(W - M/H)/K_N,
are PROVED in the note + Python verifier, NOT in Lean; they live over `R` with
DFT band projections and Riesz-Thorin interpolation. This package is the
decidable arithmetic/threshold shadow, in the stdlib-only `native_decide` house
style. No `sorry`. No mathlib.
-/

namespace GeneralPrunedSignedBound

/-! ## 0. Binomial (stdlib-only Pascal; core `Nat` lacks `Nat.choose`). -/

def binom : Nat → Nat → Nat
  | _,     0     => 1
  | 0,     _ + 1 => 0
  | n + 1, k + 1 => binom n k + binom n (k + 1)

theorem binom_check : binom 11 4 = 330 := by native_decide

/-! ## 1. The chart-free density criterion (exact integer form).

For a chart with `M = |Omega^0|` supports and image size `L = |Phi(Omega^0)|`,
the crude Theorem-I bound is `R_A(g) <= L^{3/2-1/q}/M`.  It vanishes iff
`(3/2 - 1/q) log L < log M`.  Clearing logs:

* q = 2  boundary  `L < M`               (window nonempty  <=>  M > L);
* all q  boundary  `L^{3/2} <= M`, i.e.  `L^3 <= M^2`  (window = all q>=2). -/

/-- window is nonempty (contains q=2)  <=>  `M > L`  (`logM/logL > 1`). -/
def windowNonempty (M L : Nat) : Bool := L < M

/-- window is all of `q >= 2`  <=>  `L^3 <= M^2`  (`logM/logL >= 3/2`). -/
def windowAllQ (M L : Nat) : Bool := L ^ 3 <= M ^ 2

/-- finite per-`q` decay of the pruned bound: `L^{3/2-1/q}/M < 1`, cleared of
    the `2q`-th root, i.e. `L^(3q-2) < M^(2q)` (needs `q >= 1`). -/
def prunedDecays (M L q : Nat) : Bool := L ^ (3 * q - 2) < M ^ (2 * q)

/-! ### 1.2 The atlas's depth-R prefix charts (exact L, from the verifier).

Rows `(name, Q, N, a, R, L, M=C(N,a))`; the window classification below is the
decidable shadow of the note's density table. -/

-- F5  a2 R1 : L=5,  M=10  -> nonempty, NOT all-q  (window [2, q_+),  q_+~14.4)
theorem F5a2R1_nonempty  : windowNonempty 10 5 = true  := by native_decide
theorem F5a2R1_not_allq  : windowAllQ 10 5 = false      := by native_decide
-- F7  a3 R1 : L=7,  M=35  -> all q
theorem F7a3R1_allq      : windowAllQ 35 7 = true        := by native_decide
-- F7  a3 R2 : L=28, M=35  -> nonempty, NOT all-q  (deepening R shrinks window)
theorem F7a3R2_nonempty  : windowNonempty 35 28 = true   := by native_decide
theorem F7a3R2_not_allq  : windowAllQ 35 28 = false      := by native_decide
-- F11 a4 R1 : L=11, M=330 -> all q
theorem F11a4R1_allq     : windowAllQ 330 11 = true      := by native_decide
-- F11 a4 R2 : L=110,M=330 -> nonempty, NOT all-q
theorem F11a4R2_nonempty : windowNonempty 330 110 = true := by native_decide
theorem F11a4R2_not_allq : windowAllQ 330 110 = false    := by native_decide
-- F13 a6 R1 : L=13, M=1716 -> all q
theorem F13a6R1_allq     : windowAllQ 1716 13 = true     := by native_decide

/-- Near-injective chart (chart4: `M = L = 10`): the window is EMPTY -- the
    criterion correctly reports that Theorem I's bound does not vanish. -/
theorem injective_empty  : windowNonempty 10 10 = false  := by native_decide

/-- Deepening the prefix (F7 a3: `R=1 -> R=2`) turns an all-q window into a
    finite one -- the exact monotone effect of enlarging `L` toward `Q^R`. -/
theorem deepening_shrinks :
    (windowAllQ 35 7 = true) ∧ (windowAllQ 35 28 = false) := by native_decide

/-! ## 2. The finite q-window on the #728 superincreasing family.

`L(B) = (3^B+1)/2`, `M(B) = C(2B,B)`, `W(B) = C(B, B/2)` (heavy fiber). -/

def Limg  (B : Nat) : Nat := (3 ^ B + 1) / 2
def Mslice (B : Nat) : Nat := binom (2 * B) B
def Wheavy (B : Nat) : Nat := binom B (B / 2)

theorem L_B2 : Limg 2 = 5 := by native_decide
theorem M_B2 : Mslice 2 = 6 := by native_decide
theorem W_B6 : Wheavy 6 = 20 := by native_decide

/-- FINITE per-chart window at `B=2`: the finite `q_+` is `2.586 < 3`, so the
    finite window is EMPTY of integers (`q=3` does NOT decay at `B=2`), even
    though the ASYMPTOTIC window is `{3,4}`.  This is the finite-vs-rate gap the
    note flags: `prunedDecays` uses the true small `L,M`, not the growth rates. -/
theorem B2_finite_q3_not_decay : prunedDecays (Mslice 2) (Limg 2) 3 = false := by
  native_decide
theorem B2_finite_q2_decays : prunedDecays (Mslice 2) (Limg 2) 2 = true := by
  native_decide   -- q=2 always in the finite window when M > L

/-- ASYMPTOTIC (rate) window, exactly #728's form with the growth bases
    `L ~ 3^B`, `M ~ 4^B`: `prunedDecays` on the RATE bases is
    `3^(3q-2) < 4^(2q)`, whose integer solution set is `{3,4}` -- matching the
    `first_match_signed_gain` package.  (`unprunedGrows q := 3^(q-1) > 2^q`.) -/
def rateDecays (q : Nat) : Bool := 3 ^ (3 * q - 2) < 4 ^ (2 * q)
def rateGrows  (q : Nat) : Bool := 3 ^ (q - 1) > 2 ^ q
def rateWindow (q : Nat) : Bool := rateGrows q && rateDecays q

theorem rate_window_is_3_4 :
    ((List.range 8).filter (fun q => rateWindow q)) = [3, 4] := by native_decide
theorem rate_q4_in_window : rateWindow 4 = true := by native_decide

/-- Heavy-fiber crossover (Part 3 residual): `W^2 > L` (i.e. `W > sqrt L`) first
    holds at `B = 6`, where the unpruned mask breaks the pruned ceiling and must
    route to the semantic side.  Below it the pruned bound already covers the
    whole mask. -/
def heavyCrossover (B : Nat) : Bool := (Wheavy B) ^ 2 > Limg B

theorem no_crossover_B4 : heavyCrossover 4 = false := by native_decide  -- 36 < 41
theorem crossover_B6    : heavyCrossover 6 = true  := by native_decide  -- 400 > 365
theorem crossover_B8    : heavyCrossover 8 = true  := by native_decide

/-! ## 3. Layer-cake integer identity (Part 3.1, exact).

An unpruned mask `b : ι → Nat` of max multiplicity `W_max` decomposes into
`W_max` pruned layers `g_j = 1_{b >= j}`; the total mass is preserved:
`sum_{j=1}^{W_max} |{s : b s >= j}| = sum_s b s`.  This is the combinatorial
core of `||P_A b||_q <= sum_j ||P_A g_j||_q <= W_max * L^{1/2}`. -/

/-- `j`-th pruned layer size over a finite list of syndrome multiplicities. -/
def layerSize (b : List Nat) (j : Nat) : Nat :=
  (b.filter (fun bs => j <= bs)).length

/-- total mass split into `W_max` layers. -/
def layerSum (b : List Nat) (Wmax : Nat) : Nat :=
  ((List.range Wmax).map (fun j => layerSize b (j + 1))).foldl (· + ·) 0

private theorem foldl_add_eq_sum (l : List Nat) (acc : Nat) :
    l.foldl (· + ·) acc = acc + l.sum := by
  induction l generalizing acc with
  | nil => simp
  | cons x xs ih =>
      simp only [List.foldl_cons, List.sum_cons]
      rw [ih]
      simp only [Nat.add_assoc]

private theorem layerSize_cons (x : Nat) (xs : List Nat) (j : Nat) :
    layerSize (x :: xs) j = (if j <= x then 1 else 0) + layerSize xs j := by
  by_cases h : j <= x <;> simp [layerSize, h, Nat.add_comm]

private theorem sum_append_nat (l₁ l₂ : List Nat) :
    (l₁ ++ l₂).sum = l₁.sum + l₂.sum := by
  induction l₁ with
  | nil => simp
  | cons x xs ih => simp [ih, Nat.add_assoc]

private theorem indicator_sum_eq_min (x W : Nat) :
    ((List.range W).map (fun j => if Nat.succ j <= x then 1 else 0)).sum =
      Nat.min x W := by
  induction W with
  | zero => simp
  | succ W ih =>
      rw [List.range_succ, List.map_append, sum_append_nat]
      simp only [List.map_singleton, List.sum_cons, List.sum_nil, Nat.add_zero]
      rw [ih]
      by_cases h : Nat.succ W <= x
      · have hminW : Nat.min x W = W :=
          Nat.min_eq_right (Nat.le_trans (Nat.le_succ W) h)
        have hminSucc : Nat.min x (Nat.succ W) = Nat.succ W :=
          Nat.min_eq_right h
        rw [hminW, hminSucc]
        simp [h]
      · have hx : x <= W := Nat.le_of_lt_succ (Nat.lt_of_not_ge h)
        have hx' : x <= Nat.succ W := Nat.le_trans hx (Nat.le_succ W)
        have hminW : Nat.min x W = x := Nat.min_eq_left hx
        have hminSucc : Nat.min x (Nat.succ W) = x := Nat.min_eq_left hx'
        rw [hminW, hminSucc]
        simp [h]

private theorem sum_layerSize_cons (js : List Nat) (x : Nat) (xs : List Nat) :
    (js.map (fun j => layerSize (x :: xs) (Nat.succ j))).sum =
      (js.map (fun j => if Nat.succ j <= x then 1 else 0)).sum +
        (js.map (fun j => layerSize xs (Nat.succ j))).sum := by
  induction js with
  | nil => simp
  | cons j js ih =>
      simp only [List.map_cons, List.sum_cons]
      rw [layerSize_cons, ih]
      simp only [Nat.add_assoc, Nat.add_comm, Nat.add_left_comm]

private theorem sum_layerSize_nil (js : List Nat) :
    (js.map (fun j => layerSize [] (Nat.succ j))).sum = 0 := by
  change (js.map (fun _ => 0)).sum = 0
  induction js with
  | nil => simp
  | cons j js ih => simp [ih]

private theorem layerSum_cons (x : Nat) (xs : List Nat) (W : Nat) :
    layerSum (x :: xs) W = Nat.min x W + layerSum xs W := by
  unfold layerSum
  rw [foldl_add_eq_sum, foldl_add_eq_sum]
  simp only [Nat.zero_add]
  change
    ((List.range W).map (fun j => layerSize (x :: xs) (Nat.succ j))).sum =
      Nat.min x W +
        ((List.range W).map (fun j => layerSize xs (Nat.succ j))).sum
  rw [sum_layerSize_cons, indicator_sum_eq_min]

/-- Exact nonnegative layer-cake formula, including the truncated case
    `Wmax < max b`.  This is the mass identity in Section 3.1 of
    `experimental/notes/thresholds/general_pruned_signed_bound.md` at
    `9262f63c`, before imposing that `Wmax` bounds every multiplicity. -/
theorem layerSum_eq_sum_min (b : List Nat) (Wmax : Nat) :
    layerSum b Wmax = (b.map (fun x => Nat.min x Wmax)).sum := by
  induction b with
  | nil =>
      unfold layerSum
      rw [foldl_add_eq_sum]
      simp only [Nat.zero_add]
      change ((List.range Wmax).map (fun j => layerSize [] (Nat.succ j))).sum = 0
      exact sum_layerSize_nil (List.range Wmax)
  | cons x xs ih =>
      rw [layerSum_cons, ih]
      simp

private theorem sum_min_eq_sum_of_le (b : List Nat) (Wmax : Nat) :
    (forall x, x ∈ b -> x <= Wmax) ->
      (b.map (fun x => Nat.min x Wmax)).sum = b.sum := by
  induction b with
  | nil => simp
  | cons x xs ih =>
      intro h
      have hx : x <= Wmax := h x (by simp)
      have hxs : forall y, y ∈ xs -> y <= Wmax := by
        intro y hy
        exact h y (by simp [hy])
      simp [Nat.min_eq_left hx, ih hxs]

/-- Total mass is preserved when `Wmax` bounds every multiplicity.  This is the
    nonnegative specialization reused by the charge-preserving split packet. -/
theorem layerSum_eq_foldl_of_le (b : List Nat) (Wmax : Nat)
    (h : forall x, x ∈ b -> x <= Wmax) :
    layerSum b Wmax = b.foldl (· + ·) 0 := by
  rw [layerSum_eq_sum_min, foldl_add_eq_sum]
  simp only [Nat.zero_add]
  exact sum_min_eq_sum_of_le b Wmax h

/-! ### 3.2 Signed pointwise reconstruction.

The source statement is pointwise for an integer-valued syndrome mask.  Its
`j`-th positive-index layer has the sign of the multiplicity while
`j ≤ |b(s)|`, and vanishes above that absolute multiplicity. -/

/-- The signed layer at positive threshold `j`. -/
def signedLayer (z : Int) (j : Nat) : Int :=
  if j <= z.natAbs then z.sign else 0

/-- Sum the signed layers at thresholds `1, ..., Wmax`. -/
def signedLayerSum (z : Int) (Wmax : Nat) : Int :=
  ((List.range Wmax).map (fun j => signedLayer z (j + 1))).foldl (· + ·) 0

private theorem foldl_int_add_eq_sum (l : List Int) (acc : Int) :
    l.foldl (· + ·) acc = acc + l.sum := by
  induction l generalizing acc with
  | nil => simp
  | cons x xs ih =>
      simp only [List.foldl_cons, List.sum_cons]
      rw [ih]
      simp only [Int.add_assoc]

private theorem sum_signed_indicator (js : List Nat) (c : Int) (n : Nat) :
    (js.map (fun j => if Nat.succ j <= n then c else 0)).sum =
      c * (((js.map (fun j => if Nat.succ j <= n then 1 else 0)).sum : Nat) : Int) := by
  induction js with
  | nil => simp
  | cons j js ih =>
      by_cases h : Nat.succ j <= n <;>
        simp [h, ih, Int.mul_add, Int.add_assoc]

private theorem sum_signedLayer (z : Int) (Wmax : Nat) :
    ((List.range Wmax).map (fun j => signedLayer z (Nat.succ j))).sum =
      z.sign * (Nat.min z.natAbs Wmax : Int) := by
  change
    ((List.range Wmax).map
      (fun j => if Nat.succ j <= z.natAbs then z.sign else 0)).sum = _
  rw [sum_signed_indicator, indicator_sum_eq_min]

/-- Truncated signed layer cake: stopping at `Wmax` reconstructs `z` clipped
    in absolute value at `Wmax`. -/
theorem signedLayerSum_eq_sign_mul_min (z : Int) (Wmax : Nat) :
    signedLayerSum z Wmax = z.sign * (Nat.min z.natAbs Wmax : Int) := by
  unfold signedLayerSum
  rw [foldl_int_add_eq_sum]
  simp only [Int.zero_add]
  change
    ((List.range Wmax).map (fun j => signedLayer z (Nat.succ j))).sum = _
  exact sum_signedLayer z Wmax

/-- Pointwise signed layer-cake identity from Section 3.1 of
    `experimental/notes/thresholds/general_pruned_signed_bound.md` at
    `9262f63c`.  Any common upper bound on the absolute multiplicity suffices;
    exact maximality is needed only to minimize the number of layers. -/
theorem signedLayerSum_eq (z : Int) (Wmax : Nat) (h : z.natAbs <= Wmax) :
    signedLayerSum z Wmax = z := by
  rw [signedLayerSum_eq_sign_mul_min]
  have hmin : Nat.min z.natAbs Wmax = z.natAbs := Nat.min_eq_left h
  rw [hmin]
  exact Int.sign_mul_natAbs z

/-- For positive layer indices, the `natAbs`/`sign` definition is exactly the
    source's `1_{z ≥ j} - 1_{z ≤ -j}` signed indicator. -/
theorem signedLayer_eq_indicator_diff (z : Int) (j : Nat) (hj : 0 < j) :
    signedLayer z j =
      (if (j : Int) <= z then (1 : Int) else 0) -
        (if z <= -(j : Int) then (1 : Int) else 0) := by
  cases z with
  | ofNat n =>
      cases n with
      | zero => simp [signedLayer]; omega
      | succ n => simp [signedLayer]; omega
  | negSucc n => simp [signedLayer, Int.negSucc_eq]; omega

/-- Every layer is pruned: its pointwise value lies in `{-1, 0, 1}`. -/
theorem signedLayer_values (z : Int) (j : Nat) :
    signedLayer z j = -1 ∨ signedLayer z j = 0 ∨ signedLayer z j = 1 := by
  unfold signedLayer
  split
  · cases z with
    | ofNat n =>
        cases n <;> simp
    | negSucc n => simp
  · simp

/-- A signed layer never creates support outside the original mask. -/
theorem signedLayer_ne_zero_imp (z : Int) (j : Nat)
    (h : signedLayer z j ≠ 0) : z ≠ 0 := by
  intro hz
  subst z
  simp [signedLayer] at h

/-- Function-valued source form: reconstruction holds at every syndrome. -/
theorem signed_layer_cake {α : Type} (b : α → Int) (Wmax : Nat)
    (h : forall s, (b s).natAbs <= Wmax) :
    forall s, signedLayerSum (b s) Wmax = b s := by
  intro s
  exact signedLayerSum_eq (b s) Wmax (h s)

/-- layer-cake identity on a concrete unpruned mask (`W_max = 3`):
    `b = [3,1,2,0,3,1]`, `sum b = 10`, three layers of sizes `[5,3,2]`. -/
theorem layer_cake_example :
    layerSum [3, 1, 2, 0, 3, 1] 3 = ([3,1,2,0,3,1].foldl (· + ·) 0) := by
  native_decide

theorem layer_sizes_example :
    ((List.range 3).map (fun j => layerSize [3,1,2,0,3,1] (j+1))) = [5, 3, 2] := by
  native_decide

/-- a second instance (`W_max = 4`) to exercise the identity at higher
    multiplicity. -/
theorem layer_cake_example2 :
    layerSum [4, 0, 2, 4, 1, 3, 2] 4 = ([4,0,2,4,1,3,2].foldl (· + ·) 0) := by
  native_decide

/-! ## 4. Dual `decide` spot checks. -/

theorem F7a3R1_allq'      : windowAllQ 35 7 = true       := by decide
theorem injective_empty'  : windowNonempty 10 10 = false := by decide
theorem rate_q4'          : rateWindow 4 = true          := by decide

end GeneralPrunedSignedBound
