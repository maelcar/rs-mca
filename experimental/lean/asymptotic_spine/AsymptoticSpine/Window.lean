import AsymptoticSpine.Averaging

namespace AsymptoticSpine

/-!
# (W) Window uniformity of the closed paid ledger — Lemma W, Lemma B (#443)

Stdlib-only (no mathlib) formalization of the two proved engines PR #443
(note `experimental/notes/audits/asymptotic_window_uniformity.md`) uses to discharge
the B3 window-uniformity gap of `thm:frontier`: the frontier proof slides the
agreement over an `o(n)`-window `W_n={a:|a-a_n|≤ψ_n}` (paper L289–L296), and B3 asks
whether the closed paid ledger holds *uniformly* across `W_n` or only at the single
crossing `a_n`.  #443 shows uniformity is **free given single-agreement closure**,
because:

* **Lemma W** (`reference_window_bound`): the reference scale
  `barN_{n,a}=binom(n,a)|B|^{-(a-k-1)}` has `o(n)` log-variation across `W_n`.
  Decompose `log₂ barN = log₂ binom(n,a) − (a−k−1)β`; the subfield term has step-rate
  exactly `β` and the binomial term step-rate `≤|H₂'|≤C_c` on the frontier-interior
  window (`a_n/n→c∈(0,1)`), so `log₂ barN` has step-rate `≤ C_c+β` and total variation
  `≤(C_c+β)ψ = o(n)`.
* **Lemma B** (`budget_window_pointwise`): a bounded-complexity cell budget
  `U(n,a)=∑_{i<P}(…binomials…)` with each summand's log-variation `o(n)` (interior
  arguments) and `log P=o(n)` summands has `o(n)` log-variation, i.e. `U(a)≤ratio·U(a_n)`.
* the **discharge principle** (`discharge_principle`): single-agreement payment
  `U(a_n)≤exp(o(n))barN(a_n)` + Lemma B + Lemma W ⇒ `U(a)≤exp(o(n))barN(a)` on `W_n`
  — this is `(U2)`;
* the **(LC-unif) decomposition** (`lc_unif_combine`): finitely many `exp(o(n))`
  pieces `(U0)+(U1)+(U2)+(U3)` sum to `exp(o(n))` — window uniformity of the whole
  ledger from window uniformity of each part.

## Abstract content and the reals boundary

The essential engine is **bounded local rate ⇒ variation ≤ rate·window** — a discrete
Lipschitz telescope, formalized over `Int`-valued `log₂`-magnitudes (`StepBounded`).
Following this package's standing convention (`Moment.lean`/`SigmaDiagonal.lean`
headers: keep the cleared discrete content, leave the reals limit in the tex), the
`o(n)` passage is carried in the divergence idiom `LittleO` (as `SigmaDiagonal.lean`
carries `σ_N→0` by the Nat divergence `lvl N→∞`): `window_variation_littleO` proves the
window-variation bound `(C_c+β)ψ_n` is `o(n)` whenever `ψ_n` is.

**Not formalized (honest boundary):** the two *analytic* inputs — that the binomial
step-rate is `≤C_c` (the Stirling `log₂binom(n,a)=nH₂(a/n)+O(log n)` bound and the
mean-value `|H₂'|≤C_c` on the interior interval) and that the per-summand budget ratio
is `≤ratio` — enter as the `StepBounded`/ratio hypotheses, exactly as `NoHighEnergy.lean`
takes BSG/quasicube as hypotheses.  The frontier-interior guard `c∈(0,1)` (`β>0 ⇒
ρ+g*<1`) and the `O(1)` base `β=O(1)` are the conditions making those rates finite;
their failure is the note's falsifiers F1/F3, formalized as `spike_falsifier` (an
unbounded rate breaks the bound).

Stacks on the L1–L5 spine (#438), B1 normalization (#440), A6 add-back (#441); shares
the `Averaging` core with the #442 reroute.  Kernel-checked, stdlib-only, no mathlib.
-/

/-! ## Discrete Lipschitz telescope (the Lemma W / Lemma B engine) -/

/-- `StepBounded g V` : the `Int`-valued log-magnitude `g` changes by at most `V` per
unit agreement step, `|g(a+1)−g(a)|≤V`.  For `log₂ barN` this bundles `|H₂'|≤C_c`
(binomial) and the exact subfield rate `β`. -/
def StepBounded (g : Nat → Int) (V : Nat) : Prop := ∀ a, (g (a + 1) - g a).natAbs ≤ V

/-- **Telescope.**  A per-step rate `V` accumulates linearly: `|g(a+d)−g(a)|≤V·d`. -/
theorem bounded_step_variation (g : Nat → Int) (V : Nat) (h : StepBounded g V) :
    ∀ a d, (g (a + d) - g a).natAbs ≤ V * d := by
  intro a d
  induction d with
  | zero => simp
  | succ e ih =>
    have hstep := h (a + e)
    have hsucc : a + (e + 1) = (a + e) + 1 := by omega
    rw [hsucc, Nat.mul_succ V e]
    omega

/-- Step-rates add: `g` at rate `V` plus `h` at rate `W` is at rate `V+W`.  This is the
`log₂ barN = log₂ binom − (a−k−1)β` decomposition: rate `≤ C_c + β`. -/
theorem bounded_step_add (g h : Nat → Int) (V W : Nat)
    (hg : StepBounded g V) (hh : StepBounded h W) :
    StepBounded (fun a => g a + h a) (V + W) := by
  intro a
  have h1 := hg a; have h2 := hh a
  show ((g (a + 1) + h (a + 1)) - (g a + h a)).natAbs ≤ V + W
  omega

/-- **Window bound.**  For `a` in the window `|a−a_n|≤ψ` (`a_n−ψ≤a≤a_n+ψ`), a rate-`V`
sequence varies by at most `V·ψ`: `|g(a)−g(a_n)|≤V·ψ`.  (Both window sides, via the
telescope and `natAbs` symmetry.) -/
theorem window_variation_le (g : Nat → Int) (V ψ an a : Nat) (h : StepBounded g V)
    (hlo : an - ψ ≤ a) (hhi : a ≤ an + ψ) :
    (g a - g an).natAbs ≤ V * ψ := by
  rcases Nat.le_total an a with hle | hle
  · obtain ⟨d, rfl⟩ := Nat.le.dest hle
    have hdψ : d ≤ ψ := by omega
    have hb := bounded_step_variation g V h an d
    have hvm : V * d ≤ V * ψ := Nat.mul_le_mul (Nat.le_refl V) hdψ
    omega
  · obtain ⟨d, rfl⟩ := Nat.le.dest hle
    have hdψ : d ≤ ψ := by omega
    have hb := bounded_step_variation g V h a d
    have hvm : V * d ≤ V * ψ := Nat.mul_le_mul (Nat.le_refl V) hdψ
    omega

/-! ## Lemma W — reference-scale window coherence -/

/-- **Lemma W (`barN` window coherence).**  `log₂ barN = binomLog + subfieldLog` with
binomial step-rate `≤ C_c` (interior `|H₂'|` bound) and subfield step-rate `≤ β` (the
exact `−(a−k−1)β` slope).  Then across the `ψ`-window the reference scale moves by at
most `(C_c+β)·ψ` in `log₂`, i.e. `|log₂ barN_{n,a} − log₂ barN_{n,a_n}| ≤ (C_c+β)ψ`.
The `o(n)` conclusion is `window_variation_littleO`. -/
theorem reference_window_bound (binomLog subfieldLog : Nat → Int) (Cc β ψ an a : Nat)
    (hbin : StepBounded binomLog Cc) (hsub : StepBounded subfieldLog β)
    (hlo : an - ψ ≤ a) (hhi : a ≤ an + ψ) :
    (((binomLog a + subfieldLog a) - (binomLog an + subfieldLog an))).natAbs ≤ (Cc + β) * ψ :=
  window_variation_le (fun x => binomLog x + subfieldLog x) (Cc + β) ψ an a
    (bounded_step_add binomLog subfieldLog Cc β hbin hsub) hlo hhi

/-! ## The `o(n)` divergence idiom (reals boundary, following `SigmaDiagonal`) -/

/-- `LittleO f` : `f n = o(n)`, in the package's Nat-divergence idiom — for every `K`,
eventually `K·f n ≤ n` (i.e. `f n ≤ n/K`).  Mirrors `SigmaDiagonal.lean`'s use of Nat
divergence to carry a `Rat` limit without an ordered field. -/
def LittleO (f : Nat → Nat) : Prop := ∀ K : Nat, ∃ N₀ : Nat, ∀ n, N₀ ≤ n → K * f n ≤ n

/-- A constant multiple of an `o(n)` sequence is `o(n)`: `V·ψ_n = o(n)` when `ψ_n` is. -/
theorem littleO_const_mul (V : Nat) (ψ : Nat → Nat) (h : LittleO ψ) :
    LittleO (fun n => V * ψ n) := by
  intro K
  obtain ⟨N₀, hN₀⟩ := h (K * V)
  refine ⟨N₀, fun n hn => ?_⟩
  have hk := hN₀ n hn
  calc K * (V * ψ n) = (K * V) * ψ n := by rw [Nat.mul_assoc]
    _ ≤ n := hk

/-- A sum of two `o(n)` sequences is `o(n)` (the `C_c·ψ + β·ψ` split, and the
`log P + log max` overhead of Lemma B). -/
theorem littleO_add (f g : Nat → Nat) (hf : LittleO f) (hg : LittleO g) :
    LittleO (fun n => f n + g n) := by
  intro K
  obtain ⟨N₁, h1⟩ := hf (2 * K)
  obtain ⟨N₂, h2⟩ := hg (2 * K)
  refine ⟨max N₁ N₂, fun n hn => ?_⟩
  have hn1 : N₁ ≤ n := Nat.le_trans (Nat.le_max_left _ _) hn
  have hn2 : N₂ ≤ n := Nat.le_trans (Nat.le_max_right _ _) hn
  have e1 : (2 * K) * f n ≤ n := h1 n hn1
  have e2 : (2 * K) * g n ≤ n := h2 n hn2
  have q1 : (2 * K) * f n = 2 * (K * f n) := by rw [Nat.mul_assoc]
  have q2 : (2 * K) * g n = 2 * (K * g n) := by rw [Nat.mul_assoc]
  have qg : K * (f n + g n) = K * f n + K * g n := Nat.mul_add K (f n) (g n)
  show K * (f n + g n) ≤ n
  omega

/-- **Lemma W, `o(n)` form.**  If `ψ_n = o(n)` and the reference-scale step-rate is the
constant `C_c+β`, the window log-variation bound `(C_c+β)ψ_n` is `o(n)`: the reference
scale is window-coherent.  (`reference_window_bound` supplies the per-`n` `≤`.) -/
theorem window_variation_littleO (Cc β : Nat) (ψ : Nat → Nat) (hψ : LittleO ψ) :
    LittleO (fun n => (Cc + β) * ψ n) :=
  littleO_const_mul (Cc + β) ψ hψ

/-! ## Lemma B — bounded-complexity budget window coherence -/

/-- `listSum` pulls out a left scalar: `∑_i c·f i = c·∑_i f i`. -/
theorem listSum_map_mul_left {α : Type} (c : Nat) (f : α → Nat) :
    ∀ l : List α, listSum (l.map (fun i => c * f i)) = c * listSum (l.map f) := by
  intro l
  induction l with
  | nil => simp
  | cons a t ih => simp only [List.map_cons, listSum_cons, ih, Nat.mul_add]

/-- **Lemma B (bounded-complexity budget, pointwise form).**  A cell budget
`U(a)=∑_{i<P} term_i(a)` whose each summand has window ratio bound
`term_i(a)≤ratio·term_i(a_n)` (the Stirling+MVT per-binomial log-variation, interior
argument) satisfies `U(a)≤ratio·U(a_n)`: `o(n)` log-variation.  No leaf-count term is
needed in this direct form (the `log P` overhead is the `via_max` route below). -/
theorem budget_window_pointwise (term : Nat → Nat → Nat) (P ratio a an : Nat)
    (h : ∀ i ∈ List.range P, term i a ≤ ratio * term i an) :
    listSum ((List.range P).map (fun i => term i a))
      ≤ ratio * listSum ((List.range P).map (fun i => term i an)) := by
  have hstep : listSum ((List.range P).map (fun i => term i a))
      ≤ listSum ((List.range P).map (fun i => ratio * term i an)) :=
    listSum_map_le (fun i => term i a) (fun i => ratio * term i an) (List.range P) h
  rw [listSum_map_mul_left ratio (fun i => term i an)] at hstep
  exact hstep

/-- **Lemma B, `log-sum` route (`log U ≤ log P + log max`).**  The budget is at most the
summand count `P` times the max summand — the inequality behind the note's "a `log P(n)`
term absorbs the number of summands".  (Shares `Averaging.listSum_le_length_mul_listMax`
with the pigeonhole floor.) -/
theorem budget_le_count_mul_max (terms : List Nat) :
    listSum terms ≤ terms.length * listMax terms :=
  listSum_le_length_mul_listMax terms

/-! ## Discharge principle and (LC-unif) decomposition -/

/-- **Discharge principle (the "missing lemma" of B3).**  Single-agreement payment
`U(a_n)≤E·barN(a_n)` (single-agreement closure, `thm:closed-ledger-package`), Lemma B
window slide `U(a)≤RatioB·U(a_n)`, and Lemma W reference slide `barN(a_n)≤EW·barN(a)`
compose to the window-uniform bound `U(a)≤RatioB·(E·(EW·barN(a)))` — i.e.
`U(a)≤exp(o(n))·barN(a)` on the whole window `(U2)`.  All three `exp(o(n))` factors are
cleared `Nat` multipliers. -/
theorem discharge_principle (Ua Uan barNa barNan RatioB E EW : Nat)
    (hB : Ua ≤ RatioB * Uan) (hpay : Uan ≤ E * barNan) (hW : barNan ≤ EW * barNa) :
    Ua ≤ RatioB * (E * (EW * barNa)) :=
  Nat.le_trans hB
    (Nat.le_trans (Nat.mul_le_mul (Nat.le_refl RatioB) hpay)
      (Nat.mul_le_mul (Nat.le_refl RatioB)
        (Nat.mul_le_mul (Nat.le_refl E) hW)))

/-- **(LC-unif) decomposition.**  Window uniformity of each ledger part — `(U0)` reference,
`(U1)` cell count, `(U2)` per-cell budgets, `(U3)` primitive residual — each `Ui≤Ei·barN`,
combines to window uniformity of the whole: `∑Ui ≤ (∑Ei)·barN`.  Finitely many
`exp(o(n))` add to `exp(o(n))` (in `log`, the four rates sum), so
(LC-unif) ⇔ (U0)∧(U1)∧(U2)∧(U3). -/
theorem lc_unif_combine (barN E0 E1 E2 E3 U0 U1 U2 U3 : Nat)
    (h0 : U0 ≤ E0 * barN) (h1 : U1 ≤ E1 * barN) (h2 : U2 ≤ E2 * barN) (h3 : U3 ≤ E3 * barN) :
    U0 + U1 + U2 + U3 ≤ (E0 + E1 + E2 + E3) * barN := by
  have hd : (E0 + E1 + E2 + E3) * barN
      = E0 * barN + E1 * barN + E2 * barN + E3 * barN := by
    rw [Nat.add_mul, Nat.add_mul, Nat.add_mul]
  rw [hd]; omega

/-! ## Concrete certificates (closed by kernel `decide`) -/

/-- **Lemma W, worked.**  Rates `C_c=3`, `β=2` (so `C_c+β=5`), window half-width `ψ=4`.
A rate-`5` `log₂ barN` moves by at most `5·4=20` across the window.  Sanity: a concrete
`log₂ barN` sequence `g a = 5·a` (rate exactly `5`) has `|g 7 − g 3| = 20 ≤ 20`. -/
theorem lemmaW_example :
    (((5 * (7 : Int)) - 5 * 3)).natAbs ≤ (3 + 2) * 4 := by decide

/-- **Lemma B, worked.**  Two summands (`P=2`), `term_i(a)=[4,6]`, `term_i(a_n)=[2,3]`,
`ratio=2`: pointwise `4≤2·2`, `6≤2·3`, so the budget `10≤2·5=ratio·U(a_n)`. -/
theorem lemmaB_example :
    listSum ((List.range 2).map (fun i => [4, 6].getD i 0))
      ≤ 2 * listSum ((List.range 2).map (fun i => [2, 3].getD i 0)) := by decide

/-- **Discharge, end-to-end (not `decide`).**  `RatioB=2`, `E=3`, `EW=2`, `barN(a)=10`,
`barN(a_n)=8`, `U(a_n)=20`, `U(a)=39`: the three slides compose to
`U(a)=39 ≤ 2·(3·(2·10))=120`. -/
theorem discharge_example : (39 : Nat) ≤ 2 * (3 * (2 * 10)) :=
  discharge_principle 39 20 10 8 2 3 2 (by decide) (by decide) (by decide)

/-! ### Tamper witness — the bounded step-rate is load-bearing (F1/F3)

If the per-step rate is *not* bounded by `V` — the note's F1 (interior `c→1`,
`|H₂'|→∞`) or F3 (unbounded base `β→∞`) — Lemma W fails: a single big jump makes the
window variation exceed `V·ψ`.  Documented tamper: a `spike` sequence whose one-step
jump `1000` violates any small-rate window bound. -/

/-- A `spike` log-magnitude: flat `0`, then a jump to `1000` at agreement `5` (an
unbounded-rate corner — `H₂'→∞` or `β→∞`). -/
def spike : Nat → Int := fun a => if 5 ≤ a then 1000 else 0

/-- **(Tamper) unbounded rate breaks Lemma W.**  `spike` is **not** `StepBounded` by a
small `V`: its step at `a=4` is `1000` (`(spike 5 − spike 4).natAbs = 1000 > 1`), and its
window variation `(spike 6 − spike 4).natAbs = 1000` exceeds the would-be bound
`V·ψ = 1·2 = 2`.  So the `StepBounded` hypothesis of `window_variation_le` /
`reference_window_bound` is load-bearing (drop it and the conclusion is false). -/
theorem spike_falsifier :
    (spike 5 - spike 4).natAbs = 1000                 -- one-step jump: not rate ≤ 1
    ∧ ¬ ((spike 6 - spike 4).natAbs ≤ 1 * 2) := by decide

end AsymptoticSpine
