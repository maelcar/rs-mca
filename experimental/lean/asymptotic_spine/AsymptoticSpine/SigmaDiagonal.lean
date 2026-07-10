namespace AsymptoticSpine

/-!
# (L4) The σ block-diagonalization — the gap `prop:energy-extract` skips

Stdlib-only (no mathlib) formalization of the block-diagonal construction that
`experimental/asymptotic_rs_mca.tex` elides in one phrase and that the round-2
in-paper audit (§A3) flags as the step *"a formalizer must supply … it is not
automatic"*:

> `prop:energy-extract` (L207): *"Letting σ↓0 slowly along the sequence …"*
>
> audit §A3: *"the fix … is a standard block-diagonal: put `σ_N = 1/k` on
> `N`-blocks `[N_k, N_{k+1})`, choosing `N_k` so that `ε_{1/k}(N)/N ≤ 1/k` for
> `N ≥ N_k`."*

Abstractly: a `Prop`-valued property `P : Nat → Rat → Prop` (read `P N ε` as
"the Sidon-heavy null rate at tolerance `ε` is under control at scale `N`") is
given *per fixed tolerance* `1/k`: for each `k ≥ 1` there is a threshold `N0 k`
with `P N (1/k)` for all `N ≥ N0 k`.  The conclusion produces a **single** moving
tolerance `σ : Nat → Rat` with `σ N → 0` and `P N (σ N)` eventually — the
simultaneous "`ε_{σ_N}(N)/N → 0` and `σ_N → 0`".

`σ N` is exhibited as `1 / lvl N` for an explicit **block level** `lvl : Nat → Nat`
built from a monotonized threshold `Mrec`.  Convergence `σ N → 0` is certified by
the pure-`Nat` divergence `lvl N → ∞` (for every `K` eventually `K ≤ lvl N`),
together with `σ N = 1 / lvl N`; this needs no ordered-field reasoning over `Rat`
(the sole `Rat`-limit wrapper `1/lvl → 0` is exactly the Nat divergence of `lvl`).

Kernel-checked, stdlib-only, no mathlib.
-/

/-- Monotonized threshold: strictly increasing and dominating `N0`.  `Mrec N0 k`
is the start of the `k`-th block. -/
def Mrec (N0 : Nat → Nat) : Nat → Nat
  | 0 => N0 0
  | k + 1 => max (N0 (k + 1)) (Mrec N0 k) + 1

/-- The **block level** at scale `N`: the largest crossed block index.  It stays
put or advances by one at each step, advancing exactly when the next threshold is
reached. -/
def level (N0 : Nat → Nat) : Nat → Nat
  | 0 => 0
  | N + 1 => if Mrec N0 (level N0 N + 1) ≤ N + 1 then level N0 N + 1 else level N0 N

theorem level_succ (N0 : Nat → Nat) (N : Nat) :
    level N0 (N + 1)
      = if Mrec N0 (level N0 N + 1) ≤ N + 1 then level N0 N + 1 else level N0 N :=
  rfl

section
variable (N0 : Nat → Nat)

/-- `Mrec` dominates `N0`. -/
theorem Mrec_ge_N0 (k : Nat) : N0 k ≤ Mrec N0 k := by
  cases k with
  | zero => exact Nat.le_refl _
  | succ j => exact Nat.le_trans (Nat.le_max_left _ _) (Nat.le_succ _)

/-- `Mrec` strictly increases at each step. -/
theorem Mrec_lt_succ (k : Nat) : Mrec N0 k < Mrec N0 (k + 1) := by
  show Mrec N0 k < max (N0 (k + 1)) (Mrec N0 k) + 1
  exact Nat.lt_succ_of_le (Nat.le_max_right _ _)

/-- `Mrec` dominates the identity (so it is unbounded). -/
theorem Mrec_ge_self (k : Nat) : k ≤ Mrec N0 k := by
  induction k with
  | zero => exact Nat.zero_le _
  | succ j ih => have := Mrec_lt_succ N0 j; omega

/-- `Mrec` is monotone. -/
theorem Mrec_mono {a b : Nat} (h : a ≤ b) : Mrec N0 a ≤ Mrec N0 b := by
  induction b with
  | zero => have : a = 0 := Nat.le_zero.mp h; subst this; exact Nat.le_refl _
  | succ j ih =>
    rcases Nat.lt_or_ge a (j + 1) with hlt | hge
    · exact Nat.le_trans (ih (Nat.lt_succ_iff.mp hlt)) (Nat.le_of_lt (Mrec_lt_succ N0 j))
    · have : a = j + 1 := Nat.le_antisymm h hge; subst this; exact Nat.le_refl _

/-- `level` advances by at most one per step. -/
theorem level_le_succ (N : Nat) : level N0 N ≤ level N0 (N + 1) := by
  rw [level_succ]; split <;> omega

/-- `level` is monotone. -/
theorem level_mono {m n : Nat} (h : m ≤ n) : level N0 m ≤ level N0 n := by
  induction n with
  | zero => have : m = 0 := Nat.le_zero.mp h; subst this; exact Nat.le_refl _
  | succ j ih =>
    rcases Nat.lt_or_ge m (j + 1) with hlt | hge
    · exact Nat.le_trans (ih (Nat.lt_succ_iff.mp hlt)) (level_le_succ N0 j)
    · have : m = j + 1 := Nat.le_antisymm h hge; subst this; exact Nat.le_refl _

/-- Below the first threshold the level is `0`. -/
theorem level_zero_of_lt : ∀ N, N < Mrec N0 0 → level N0 N = 0 := by
  intro N
  induction N with
  | zero => intro _; rfl
  | succ M ih =>
    intro h
    have hlevM : level N0 M = 0 := ih (by omega)
    rw [level_succ, hlevM]
    have h1 : Mrec N0 0 < Mrec N0 (0 + 1) := Mrec_lt_succ N0 0
    have hcond : ¬ Mrec N0 (0 + 1) ≤ M + 1 := by omega
    rw [if_neg hcond]

/-- **Block containment.**  For `N` past the first threshold, `Mrec (level N) ≤ N`
— the level's own block start is at most `N` (paper: "the `j`-th class is
contained in the projection of `C_j` after earlier cells have been removed", here
the block form). -/
theorem level_below : ∀ N, Mrec N0 0 ≤ N → Mrec N0 (level N0 N) ≤ N := by
  intro N
  induction N with
  | zero => intro h; exact h
  | succ M ih =>
    intro h
    rw [level_succ]
    by_cases hc : Mrec N0 (level N0 M + 1) ≤ M + 1
    · rw [if_pos hc]; exact hc
    · rw [if_neg hc]
      by_cases hM : Mrec N0 0 ≤ M
      · exact Nat.le_trans (ih hM) (Nat.le_succ M)
      · have hMlt : M < Mrec N0 0 := by omega
        rw [level_zero_of_lt N0 M hMlt]; exact h

/-- **Level divergence.**  Once `N` reaches the `K`-th block start `Mrec K`, the
level is at least `K`.  Hence `lvl N → ∞`, which is exactly `σ N = 1/lvl N → 0`. -/
theorem level_diverge : ∀ N K, Mrec N0 K ≤ N → K ≤ level N0 N := by
  intro N
  induction N with
  | zero =>
    intro K h
    have hself : K ≤ Mrec N0 K := Mrec_ge_self N0 K
    have : level N0 0 = 0 := rfl
    omega
  | succ M ih =>
    intro K h
    by_cases hcase : Mrec N0 K ≤ M
    · exact Nat.le_trans (ih K hcase) (level_le_succ N0 M)
    · cases K with
      | zero => exact Nat.zero_le _
      | succ k =>
        have hstep : Mrec N0 k < Mrec N0 (k + 1) := Mrec_lt_succ N0 k
        have hMk : Mrec N0 k ≤ M := by omega
        have hik : k ≤ level N0 M := ih k hMk
        by_cases hbig : k + 1 ≤ level N0 M
        · exact Nat.le_trans hbig (level_le_succ N0 M)
        · have hlevMk : level N0 M = k := by omega
          rw [level_succ]
          have hcond : Mrec N0 (level N0 M + 1) ≤ M + 1 := by rw [hlevMk]; exact h
          rw [if_pos hcond]; omega

end

/-- **(L4) σ block-diagonalization** (the step `prop:energy-extract` skips;
round-2 audit §A3).  Given a per-tolerance guarantee — for every `k ≥ 1` a
threshold `N0 k` with `P N (1/k)` for all `N ≥ N0 k` — there is a single moving
tolerance `σ : Nat → Rat` and a block level `lvl : Nat → Nat` with

* `σ N = 1 / lvl N` (the tolerance is `1` over the block index);
* `lvl N → ∞` (for every `K`, eventually `K ≤ lvl N`) — this is `σ N → 0`;
* eventually `1 ≤ lvl N` and `P N (σ N)` — the property holds at the moving
  tolerance.

External analytic input enters only through `hP`, as an explicit hypothesis. -/
theorem sigma_block_diagonal
    (P : Nat → Rat → Prop) (N0 : Nat → Nat)
    (hP : ∀ k : Nat, 1 ≤ k → ∀ N : Nat, N0 k ≤ N → P N ((1 : Rat) / (k : Rat))) :
    ∃ (σ : Nat → Rat) (lvl : Nat → Nat),
      (∀ N, σ N = (1 : Rat) / (lvl N : Rat)) ∧
      (∀ K : Nat, ∃ N₁, ∀ N, N₁ ≤ N → K ≤ lvl N) ∧
      (∃ N₂, ∀ N, N₂ ≤ N → 1 ≤ lvl N ∧ P N (σ N)) := by
  refine ⟨fun N => (1 : Rat) / (level N0 N : Rat), level N0, fun _ => rfl, ?_, ?_⟩
  · -- lvl N → ∞ : take N₁ = Mrec N0 K
    intro K
    exact ⟨Mrec N0 K, fun N hN => level_diverge N0 N K hN⟩
  · -- P eventually : take N₂ = Mrec N0 1
    refine ⟨Mrec N0 1, fun N hN => ?_⟩
    have h1le : 1 ≤ level N0 N := level_diverge N0 N 1 hN
    refine ⟨h1le, ?_⟩
    have hMrec0N : Mrec N0 0 ≤ N :=
      Nat.le_trans (Mrec_mono N0 (Nat.zero_le 1)) hN
    have hbelow : Mrec N0 (level N0 N) ≤ N := level_below N0 N hMrec0N
    have hN0le : N0 (level N0 N) ≤ N :=
      Nat.le_trans (Mrec_ge_N0 N0 (level N0 N)) hbelow
    exact hP (level N0 N) h1le N hN0le

end AsymptoticSpine
