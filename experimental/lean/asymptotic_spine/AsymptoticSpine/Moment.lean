import AsymptoticSpine.Util

namespace AsymptoticSpine

/-!
# (L2) Q pays shift pairs and (L3) moment-max squeeze

Stdlib-only (no mathlib) formalization of the two elementary moment inequalities
of `experimental/asymptotic_rs_mca.tex`.  Both are stated over `Nat` fiber counts
`N(s)`: the normalizations `N̄ = M/L` and `κN̄` are positive scalars, and clearing
them turns the tex's rational statements into the scale-free integer inequalities
formalized here (the asymptotic `o(Nq)` corollaries stay in the tex — they need
reals).

## (L2) `lem:q-sp` (L254–260)

*"If `∑_s N(s) = M`, `N̄ = M/L`, and `max_s N(s) ≤ κN̄`, then
`M^{-1} ∑_s N(s)^2 ≤ κN̄`."*  Paper proof (L259):
`∑_s N(s)^2 ≤ (max_s N(s)) ∑_s N(s) ≤ κN̄ · M`.  The scale-free core is
`∑ N(s)^2 ≤ B · ∑ N(s)` for any upper bound `B ≥ N(s)` (round-2 audit A7:
*"Σ N² ≤ (max N)(Σ N)"*); dividing by `M` gives `M^{-1}∑N^2 ≤ B ≤ κN̄`.

## (L3) `lem:moment-max` (L165–178), discrete core

`L^{-1} R^q ≤ Γ^{ord}_q ≤ R^q` with `R = max_s |F_s|/N̄` and
`Γ^{ord}_q = L^{-1} ∑_s (|F_s|/N̄)^q`.  Multiplying through by `L` and clearing the
positive scalar `N̄^{-q}` gives the scale-free squeeze on the integer fiber counts
`x_s = |F_s|`:
`(max_s x_s)^q ≤ ∑_s x_s^q ≤ L · (max_s x_s)^q`,
formalized here (`L = ` number of levels).  The `q`-th-root / `log L = o(Nq)`
passage to `Γ^{ord}_q ≤ exp(o(Nq)) ⇔ max_s|F_s| ≤ exp(o(N))N̄` is the reals part,
left in the tex.

Kernel-checked, stdlib-only, no mathlib.
-/

/-! ## (L2) Q-to-SP second-moment bound -/

/-- Sum of squares of a `List Nat` (the second-moment numerator `∑_s N(s)^2`). -/
def listSumSq : List Nat → Nat
  | [] => 0
  | a :: l => a * a + listSumSq l

@[simp] theorem listSumSq_nil : listSumSq [] = 0 := rfl
@[simp] theorem listSumSq_cons (a : Nat) (l : List Nat) :
    listSumSq (a :: l) = a * a + listSumSq l := rfl

/-- **(L2) `lem:q-sp`, scale-free core.**  If every fiber count `N(s)` is at most
`B` (in particular `B = κN̄`), then the second moment is at most `B` times the
total: `∑_s N(s)^2 ≤ B · ∑_s N(s)`.  Dividing by `M = ∑_s N(s)` recovers the tex's
`M^{-1}∑_s N(s)^2 ≤ κN̄`. -/
theorem qsp_sumSq_le (B : Nat) :
    ∀ N : List Nat, (∀ x ∈ N, x ≤ B) → listSumSq N ≤ B * listSum N := by
  intro N
  induction N with
  | nil => intro _; simp
  | cons a t ih =>
    intro hB
    have haa : a * a ≤ B * a := Nat.mul_le_mul (hB a List.mem_cons_self) (Nat.le_refl a)
    have ht : listSumSq t ≤ B * listSum t :=
      ih (fun x hx => hB x (List.mem_cons_of_mem _ hx))
    simp only [listSumSq_cons, listSum_cons, Nat.mul_add]
    omega

/-! ## (L3) moment-max squeeze -/

/-- Sum of `q`-th powers of a `List Nat` (the moment numerator `∑_s x_s^q`). -/
def listSumPow (q : Nat) : List Nat → Nat
  | [] => 0
  | a :: l => a ^ q + listSumPow q l

@[simp] theorem listSumPow_nil (q : Nat) : listSumPow q [] = 0 := rfl
@[simp] theorem listSumPow_cons (q a : Nat) (l : List Nat) :
    listSumPow q (a :: l) = a ^ q + listSumPow q l := rfl

/-- **Lower squeeze** (`lem:moment-max`, "the lower bound keeps a maximum
summand").  Any single member's `q`-th power is at most the moment sum; applied to
a maximal `x_s` this is `(max_s x_s)^q ≤ ∑_s x_s^q`. -/
theorem pow_mem_le_listSumPow (q : Nat) :
    ∀ (f : List Nat) (a : Nat), a ∈ f → a ^ q ≤ listSumPow q f := by
  intro f
  induction f with
  | nil => intro a ha; simp at ha
  | cons b t ih =>
    intro a ha
    simp only [listSumPow_cons]
    rcases List.mem_cons.mp ha with h | h
    · subst h; exact Nat.le_add_right _ _
    · exact Nat.le_trans (ih a h) (Nat.le_add_left _ _)

/-- **Upper squeeze** (`lem:moment-max`, "the upper bound replaces every summand by
the maximum").  If every member is at most `mx`, the moment sum is at most
`L · mx^q`, where `L = f.length` is the number of levels. -/
theorem listSumPow_le_length_mul (q : Nat) :
    ∀ (f : List Nat) (mx : Nat), (∀ x ∈ f, x ≤ mx) →
      listSumPow q f ≤ f.length * mx ^ q := by
  intro f
  induction f with
  | nil => intro mx _; simp
  | cons b t ih =>
    intro mx hmx
    have hbq : b ^ q ≤ mx ^ q := Nat.pow_le_pow_left (hmx b List.mem_cons_self) q
    have ht : listSumPow q t ≤ t.length * mx ^ q :=
      ih mx (fun x hx => hmx x (List.mem_cons_of_mem _ hx))
    simp only [listSumPow_cons, List.length_cons, Nat.add_mul, Nat.one_mul]
    omega

/-- **(L3) `lem:moment-max`, discrete squeeze.**  For a finite multiset `f` of
nonnegative integer fiber counts with maximum `mx` (attained, `mx ∈ f`, and
`∀ x ∈ f, x ≤ mx`), the `q`-th moment is squeezed:
`mx^q ≤ ∑_s x_s^q ≤ L · mx^q`, with `L = f.length`.  This is the tex's
`L^{-1}R^q ≤ Γ^{ord}_q ≤ R^q` cleared of the positive normalization `N̄^{-q}`. -/
theorem moment_max_squeeze (q : Nat) (f : List Nat) (mx : Nat)
    (hmem : mx ∈ f) (hmax : ∀ x ∈ f, x ≤ mx) :
    mx ^ q ≤ listSumPow q f ∧ listSumPow q f ≤ f.length * mx ^ q :=
  ⟨pow_mem_le_listSumPow q f mx hmem, listSumPow_le_length_mul q f mx hmax⟩

/-! ## Concrete sanity certificates (closed by kernel `decide`) -/

/-- (L2) A shift-pair profile: counts `[3,1,2]` with bound `B = 3`; the second
moment `9+1+4 = 14 ≤ 3·6 = 18`. -/
theorem qsp_example : listSumSq [3, 1, 2] ≤ 3 * listSum [3, 1, 2] := by decide

/-- (L3) The `q = 2` squeeze on the profile `[3,1,2]` (max `3`, `L = 3`):
`3^2 = 9 ≤ 9+1+4 = 14 ≤ 3·9 = 27`.  Also `Γ_1`-flatness: `listSumPow 1 = listSum`. -/
theorem moment_example :
    3 ^ 2 ≤ listSumPow 2 [3, 1, 2] ∧ listSumPow 2 [3, 1, 2] ≤ [3, 1, 2].length * 3 ^ 2
    ∧ listSumPow 1 [3, 1, 2] = listSum [3, 1, 2] := by decide

end AsymptoticSpine
