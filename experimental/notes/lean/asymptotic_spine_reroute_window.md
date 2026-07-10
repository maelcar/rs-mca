# Asymptotic-spine Lean ↔ tex correspondence — lower-side reroute (#442) + window uniformity (#443), sorry-free, `lake build` PASSING

Status: `FORMALIZATION` (two new stdlib-only modules in
`experimental/lean/asymptotic_spine/` mechanizing the *proved* cores of the two
audit-corner repairs of `experimental/asymptotic_rs_mca.tex`) /
`VERIFIED-CLEAN` (`lake build` **passes**, clean build ≈ 6 s, `v4.31.0`, 13 jobs;
`#print axioms` on every top statement shows only `propext` / `Quot.sound` /
`Classical.choice` — several `decide` certificates depend on **no** axioms; no
`sorry`, no `native_decide`, no `import Mathlib`).

## Stack

`#438` (L1–L5 elementary spine) → `#440` (B1 image-normalization identities,
`Normalization.lean`) → `#441` (A6 add-back sufficiency, `AddBack.lean`) → **this**
(`#442` lower-side reroute + `#443` window uniformity), on the base tip of the open
rollup `#445`.  The two new modules **share** a factored combinatorial core
`Averaging.lean` (both repairs run on the same "total over bounded buckets" engine),
which imports `AddBack.lean` to reuse `listMax` and the list scaffolding of the
existing spine.

New files:

- `AsymptoticSpine/Averaging.lean` — shared pigeonhole / Markov core.
- `AsymptoticSpine/Reroute.lean` — (R) the #442 collision-free reroute.
- `AsymptoticSpine/Window.lean` — (W) the #443 window uniformity engine.
- root `AsymptoticSpine.lean` — three added imports.

Reference notes mechanized:
`experimental/notes/audits/asymptotic_lowerside_collision_free_reroute.md` (#442)
and `experimental/notes/audits/asymptotic_window_uniformity.md` (#443).

## Modeling conventions

Same as the rest of the package (stdlib has no `Finset`/`Fintype`/`Nat.choose`; see
the `#441` note `experimental/notes/audits/lean_asymptotic_spine_note.md` §0):
finite collections are `List`; cardinalities and the `exp(o(n))` / `|B|^w` / ceiling
data are `Nat`; a positive normalization is cleared and the scale-free integer
content is stated.  Two new choices:

- **Signed log-magnitudes over `Int`.**  Lemma W is about a *signed* variation of
  `log₂ barN` (which rises then falls), so the window engine works over
  `Nat → Int` and measures variation by `Int.natAbs`.  The `o(n)` passage is carried
  in the package's Nat-divergence idiom `LittleO` (as `SigmaDiagonal.lean` carries a
  `Rat` limit by a Nat divergence); the reals limit stays in the tex.
- **External algebra as hypotheses, never axioms.**  The RS/CA facts the two repairs
  cite (injectivity of the identity-prefix codeword map; the `≤k`-roots distinct-slope
  bound; the Stirling/MVT rate bounds) enter as explicit lemma hypotheses, exactly as
  `NoHighEnergy.lean` takes BSG/quasicube as hypotheses.  This is flagged per row in
  the honest-boundary list (§4).

---

## 1. (R) Reroute correspondence table — `Reroute.lean` + shared `Averaging.lean`

Status vocabulary: **FORMALIZED** (the claim's exact finite/arithmetic content is
kernel-checked); **HYPOTHESIS-PARAM** (an external algebraic fact enters as an
explicit hypothesis); **CERT** (`decide` sanity/contrast certificate).

| Lean declaration | tex / #442-note claim | status |
|---|---|---|
| `Averaging.pigeonhole_floor` | `lem:capff1-identity-prefix-floor` core: `M↦(e_j(M))_{1≤j≤w}` into `B^w` ⇒ one fibre `≥⌈binom(n,m)/\|B\|^w⌉`; cleared `total ≤ P·maxFibre` (`cap25_cap_v13_raw.tex:6909`, "one fiber contains at least `binom nm/\|B\|^w` subsets") | FORMALIZED |
| `Averaging.partition_sum` | the fibre decomposition itself: buckets over the `≤P` prefix values partition the `binom(n,m)` subsets (the counting content of the prefix map) | FORMALIZED |
| `Reroute.identity_prefix_floor` | `lem:capff1-identity-prefix-floor`, packaged at `ks = range P` (`P=\|B\|^w`): `\|subsets\| ≤ P·maxFibre` | FORMALIZED |
| `Averaging.nodup_map_of_injective` | the **collision-free** content: injective `M↦c_M` (locator identity) keeps the `binom(n,m)` codewords distinct — the raw pole map does not (#442-note §"gap it fixes") | FORMALIZED |
| `Reroute.identity_prefix_codewords_nodup` | packaged: `subsets.Nodup` + `hinj` ⇒ `binom(n,m)` distinct codewords (no support collision) | FORMALIZED (`hinj` = HYPOTHESIS-PARAM) |
| `Reroute.identity_prefix_fibre_nodup` | each prefix fibre is a genuine duplicate-free list-decoding list `\|Lst(…)\|≥⌈…⌉`, not a multiset | FORMALIZED |
| `Reroute.collision_contrast` | Gate E `462↦12`: injective map keeps the image `Nodup`; the collapsing (raw-pole) map does not | CERT (`decide`) |
| `Averaging.markov_count`, `Reroute.reservoir_high_collision_few` | `thm:A` reservoir averaging, Markov direction: over `Ω=F∖D`, `\|{α:coll≥B}\|·B ≤ T` — "most reservoir poles have bounded collisions" (#442-note step 2) | FORMALIZED |
| `Averaging.exists_lt_of_listSum_lt` | averaging existence: subcritical total collision mass ⇒ a low-collision pole exists | FORMALIZED |
| `Reroute.reservoir_distinct_slope_floor` | `thm:A` distinct-slope floor: bounded collision mass ⇒ some reservoir pole realizes `> L−B` distinct CA-bad slopes — the **proved replacement** for `asymptotic_rs_mca.tex:283`'s asserted "subexponential collision loss" | FORMALIZED (`hgood`, `hmass≤T` = HYPOTHESIS-PARAM) |
| `Reroute.reroute_bridge` | the two-step bridge = floor ∘ reservoir, replacing the pole assertion: distinct codewords (collision-free) + `binom(n,m)≤P·L` + a pole with `>L−B` slopes | FORMALIZED |
| `Reroute.identity_prefix_floor_example`, `…_fibres`, `reservoir_floor_example` | worked `binom→fibre→pole` instances (one end-to-end through the theorem, not `decide`) | CERT |
| `Reroute.reservoir_saturated_falsifier` | tamper: a *saturated* reservoir (mass `=B·\|Ω\|`, not subcritical) has **no** `>L−B` pole — subcriticality is load-bearing | CERT (`decide`) |

## 2. (W) Window correspondence table — `Window.lean`

| Lean declaration | #443-note claim | status |
|---|---|---|
| `Window.StepBounded`, `bounded_step_variation` | the discrete Lipschitz telescope: per-step rate `V` ⇒ `\|g(a+d)−g(a)\|≤V·d` (the engine under Lemma W and Lemma B) | FORMALIZED |
| `Window.bounded_step_add` | the `log₂ barN = log₂ binom − (a−k−1)β` rate split: rate `≤ C_c + β` | FORMALIZED |
| `Window.window_variation_le` | window bound: `a∈W_n` (`\|a−a_n\|≤ψ`) ⇒ `\|g(a)−g(a_n)\|≤V·ψ` | FORMALIZED |
| `Window.reference_window_bound` | **Lemma W** (`barN` window coherence): `\|log₂barN_{n,a}−log₂barN_{n,a_n}\| ≤ (C_c+β)ψ` (#443-note §1 Lemma W) | FORMALIZED (`C_c`, `β` rate bounds = HYPOTHESIS-PARAM) |
| `Window.LittleO`, `littleO_const_mul`, `littleO_add` | the `o(n)` idiom (`f n = o(n)` as `∀K ∃N₀ ∀n≥N₀, K·f n ≤ n`); closed under `V·(·)` and `+` | FORMALIZED |
| `Window.window_variation_littleO` | **Lemma W, `o(n)` form**: `ψ_n=o(n)` ⇒ `(C_c+β)ψ_n=o(n)` — the reference scale is window-coherent | FORMALIZED |
| `Window.budget_window_pointwise` | **Lemma B** (bounded-complexity budget): per-summand ratio bound ⇒ `U(a)≤ratio·U(a_n)` (#443-note §1 Lemma B) | FORMALIZED (per-summand ratio = HYPOTHESIS-PARAM) |
| `Window.budget_le_count_mul_max` | Lemma B's `log-sum` route `log U ≤ log P + log max` (the `log P(n)=o(n)` overhead); shares `Averaging.listSum_le_length_mul_listMax` with the floor | FORMALIZED |
| `Window.discharge_principle` | **the "missing lemma" of B3**: single-agreement payment + Lemma B + Lemma W ⇒ `U(a)≤exp(o(n))barN(a)` on `W_n` (i.e. `(U2)`) — window uniformity is *free given single-agreement closure* | FORMALIZED |
| `Window.lc_unif_combine` | **(LC-unif) ⇔ (U0)∧(U1)∧(U2)∧(U3)**: finitely many `exp(o(n))` pieces `∑Ui≤(∑Ei)barN` (#443-note §1, claim-ledger #1) | FORMALIZED |
| `Window.lemmaW_example`, `lemmaB_example`, `discharge_example` | worked rate/budget/discharge instances | CERT |
| `Window.spike_falsifier` | tamper (#443-note F1/F3): an **unbounded** step-rate (`\|H₂'\|→∞` interior, or `β→∞` base) breaks Lemma W — the bounded-rate hypothesis is load-bearing | CERT (`decide`) |

---

## 3. Build, axioms, tamper

- **Build.** `cd experimental/lean/asymptotic_spine && lake build` → `Build
  completed successfully (13 jobs)`, ≈ 6 s clean, `leanprover/lean4:v4.31.0`,
  stdlib-only.  Grep of the two new sources for `sorry` / `native_decide` /
  `import Mathlib` returns zero hits.
- **Axioms** (`#print axioms`, top statements): `pigeonhole_floor`, `markov_count`,
  `partition_sum`, `nodup_map_of_injective`, `reference_window_bound`,
  `window_variation_le`, `budget_window_pointwise`, `lc_unif_combine`,
  `littleO_add`, `window_variation_littleO` → `[propext, Quot.sound]` (or a subset);
  `exists_lt_of_listSum_lt`, `identity_prefix_floor`, `reservoir_distinct_slope_floor`,
  `reroute_bridge` → `[propext, Classical.choice, Quot.sound]`;
  `discharge_principle`, `collision_contrast`, `reservoir_saturated_falsifier`,
  `spike_falsifier` → **no axioms**.  All within the allowed
  `propext` / `Quot.sound` / `Classical.choice`.
- **Tamper checks.** Three, each *verified by actually trying*:
  1. **`Reroute.reservoir_saturated_falsifier`** (in-tree, `decide`): a saturated
     reservoir (collision mass `= B·|Ω|`, not subcritical) admits **no** pole with
     `>L−B` distinct slopes, so the strict subcriticality `T<B·|Ω|` in
     `reservoir_distinct_slope_floor` is load-bearing.
  2. **`Window.spike_falsifier`** (in-tree, `decide`): a `spike` sequence with a
     one-step jump `1000` has window variation `1000 > V·ψ = 2`, so the
     `StepBounded` rate hypothesis of `window_variation_le` / `reference_window_bound`
     is load-bearing (the note's F1/F3).
  3. **Live "drop hypothesis → build fails"** (transient, off-tree): a copy of
     `reservoir_distinct_slope_floor` with `hsub` removed was compiled; the shared
     proof's `omega` step (deriving `listSum < B·|Ω|`) **fails** and `lake build`
     exits nonzero.  Confirms the hypothesis is not cosmetic.  (File not committed.)

---

## 4. Honest boundary — what is NOT formalized

The two repairs are formalized at their *proved-core* granularity; the deep
external inputs enter as hypotheses (never axioms), and one reservoir step is
narrowed.  Explicitly out of scope:

**(R) reroute.**

- **Injectivity of `M↦c_M` is a hypothesis** (`hinj`), not derived.  It is the tex's
  locator identity (`c_M` fixes `e_j(M)` for `j>w`, the prefix fibre fixes `j≤w`);
  proving it needs the RS polynomial algebra (`\deg(c_M−c_{M'})≤K−1<n` vanishing on
  `D`), which is `cap25_cap_v13_raw.tex`'s content, not the pigeonhole's.
- **The distinct-slope bound `good α ≥ L−coll α` is a hypothesis** (`hgood`), not
  derived.  It is the `≤k`-roots fact (`P_i−P_j` has degree `≤k`, so a collision at
  `α` costs `≤1` distinct slope) — `thm:A`'s pole algebra.
- **The total collision mass bound `≤T` is a hypothesis** (`hmass`).  The tex value
  `T=k·C(L,2)` (from `≤k` roots per pair over `≤C(L,2)` pairs) is not computed; only
  its *use* in averaging is formalized.
- **Narrowed reservoir conclusion.**  The #442-note states the sharp fraction
  "some pole realizes `M(α)≥L(q−n)/(q−n+kL)` distinct slopes".  We formalize the
  cleaner, equivalent-in-spirit **min-≤-mean** form: bounded mass ⇒ some pole with
  collisions `<B` ⇒ `>L−B` distinct slopes (via the subcritical-existence
  `exists_lt_of_listSum_lt`).  This is the same averaging content stated at the
  granularity that abstracts cleanly; the exact rational fraction (a sharper
  argmin/harmonic bound) is **not** reproduced.  This is the honest narrowing the
  task calls for.
- **Ceiling / concrete values.**  The pigeonhole delivers `total ≤ P·maxFibre`
  (`⌈·⌉` and the concrete `binom(n,m)`, `|B|^w`, deployed rows / margins are the
  tex's finite certificates — `prop:capff1-identity-frontier` — not re-derived).
- **`thm:A`'s `η`-slack / `eca ≤ eps_mca` monotonicity / `1/2k` deep-point floor**
  are the tex's; only the *reservoir-averaging* sub-step is mechanized.

**(W) window.**

- **The analytic rate bounds are hypotheses.**  `StepBounded binomLog C_c` encodes
  the Stirling `log₂binom(n,a)=nH₂(a/n)+O(log n)` bound **and** the interior MVT
  `|H₂'(ξ)|≤C_c` on `[c/2,(1+c)/2]⊂(0,1)`; `StepBounded subfieldLog β` encodes the
  exact `−(a−k−1)β` slope.  Neither the Stirling expansion nor the entropy
  derivative is formalized (no reals in stdlib); their *failure* (unbounded rate) is
  witnessed by `spike_falsifier`.
- **The frontier-interior guard is not formalized.**  `β>0 ⇒ ρ+g*<1` (so
  `c∈(0,1)`, keeping `|H₂'|` finite) and the `O(1)`-base condition `β=O(1)` are the
  note's G5 / F1 / F3 — the conditions making the rates finite.  They are the
  *premises* of Lemma W here (the finite `C_c`, `β`), not theorems.
- **Cell activation/deactivation straddle not formalized.**  Lemma B assumes each
  binomial argument stays interior throughout `W_n` (uniformly-active cell).  The
  note's §1 "activation remark" — that a cell switching `0↔poly(n)` across a
  threshold is contained because first match (`lem:first-match`) conserves the
  *total* — is **not** mechanized (it would compose with `FirstMatch.lean`; left as
  OPEN below).
- **`o(n)` is the divergence idiom, not reals.**  `LittleO` is the Nat surrogate for
  `f n = o(n)`; the genuine real limit stays in the tex.
- **Per-cell table (#443-note §3) not enumerated.**  The 6-by-inspection /
  2-with-proof / 1-not-established verdicts are audit content; only the *engines*
  (Lemma W, Lemma B, discharge, LC-unif) they invoke are formalized.

**Both / pre-existing (unchanged by either repair).**

- No claim that `thm:frontier` is unconditional.  The C9 moduli/Fourier-Sidon
  routing (`Cho26Moduli*`, absent) and the primitive-Q atom `prob:entropy-inverse-q`
  remain the open gaps both notes name; the reroute *avoids* the pole fibres and the
  window discharge *slides* single-agreement closure — neither closes those atoms.
- No Lean claim on the deployed finite margins (`+9.2` bits etc.); those are the
  verifiers' exact-integer certificates, not asymptotic-spine content.

### OPEN (dropped-for-now, would extend cleanly)

- **Activation-straddle conservation** (W): compose `budget_window_pointwise` with
  `FirstMatch.firstMatch_le_sum_budgets` to formalize that a deactivating cell's mass
  is first-match-reassigned, so the *total* has `o(n)` log-variation even across an
  `exp(o(n))` straddle.  Deferred (needs a first-match/budget interface lemma).
- **Sharp reservoir fraction** (R): the exact `L(q−n)/(q−n+kL)` argmin bound, if a
  clean Nat form is found, would replace the `>L−B` min-≤-mean statement.

---

## 5. Nonclaims

- Not a proof of `thm:frontier`, single-agreement closure, `thm:A`, or
  `lem:capff1-identity-prefix-floor`'s RS algebra; those are the tex's, taken as the
  hypotheses named above.
- Not an edit to `asymptotic_rs_mca.tex` or any other lane's files; this is the Lean
  formalization lane only (the tex edits are #442's, the note is #443's).
- Not `native_decide` / not Mathlib; stdlib-only, kernel-checked.
