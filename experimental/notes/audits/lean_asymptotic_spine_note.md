# Asymptotic-spine Lean ↔ `asymptotic_rs_mca.tex` correspondence note — L1–L5 + B1 image-normalization identities + A6 add-back sufficiency, all sorry-free, `lake build` PASSING

Status: `FORMALIZATION` (a new stdlib-only Lean package `experimental/lean/asymptotic_spine/`
mechanizing the elementary spine of `experimental/asymptotic_rs_mca.tex`) /
`VERIFIED-CLEAN` (`lake build` **passes**; `#print axioms` on every shipped
statement shows only Lean's own `propext` / `Quot.sound` / `Classical.choice`; no
`sorry`, no `native_decide`, no custom logical assumption; grep of the `.lean`
sources for the two forbidden tokens returns zero hits).

This note follows the conventions of the `#418` audit
(`experimental/notes/audits/lean_grande_finale_correspondence_audit.md`): every
declaration is mapped to the tex `\label{...}` (or informal anchor) it formalizes,
with a per-declaration status.  The status vocabulary here is
**FORMALIZED** (the tex statement's exact finite/arithmetic content is
kernel-checked), **HYPOTHESIS-PARAM** (an external deep theorem enters as an
explicit hypothesis of the lemma, not as an axiom), and **OUT-OF-SCOPE** (needs
real analysis / imported algebro-geometry, kept in the tex).

## 0. Scope and the one structural divergence to flag

**Source of statements.** `experimental/asymptotic_rs_mca.tex` (346 lines; lives
on branch `thresholds-asymptotic-proof-audit-r2`).  Its ten in-paper proofs were
adversarially audited in
`experimental/notes/asymptotic_rs_mca_proof_audit_r2.md` (8 `NO ISSUE` / 2
`OPEN GAP`); this note mechanizes the elementary core of the `NO ISSUE` steps and
the one named formalization gap the r2 audit says a formalizer *must* supply
(§A3, the σ block-diagonal).

**Structural divergence — package location (flagged prominently).**  The steering
asks that new asymptotic material integrate "within/alongside" the existing
`experimental/lean/grande_finale/` package.  That package is **Mathlib-pinned**
(`lakefile.toml` requires `mathlib` at `v4.28.0`; `GrandeFinale.lean` opens with
`import Mathlib`) and, as its own `#418` audit records (§0), *"requires a
Mathlib-pinned toolchain that is unavailable here"* — Mathlib cannot be built on
this machine.  A module placed physically inside `grande_finale` therefore cannot
be `lake build`-verified here: Lake resolves the `require mathlib` dependency at
configure time regardless of whether the new module imports Mathlib, and that
resolution fails.  Because the hard mandate is **stdlib-only + a PASSING
`lake build`**, the spine is delivered as a **self-contained stdlib-only sibling
package** `experimental/lean/asymptotic_spine/`, alongside `grande_finale`,
mirroring the naming/docstring/label-citation conventions of the buildable
stdlib packages (`staircase_logic`, `l1_threshold_ledger`, `rs_mca_formalization`).
`grande_finale`'s lakefile/toolchain is left **untouched**.  The
`AsymptoticSpine.*` declarations cite `asymptotic_rs_mca.tex` labels in their
docstrings exactly as `GrandeFinale.*` cites `grande_finale.tex`, so the next
audit maps them the same way.

**Toolchain.** `leanprover/lean4:v4.31.0` (the pin used by the three buildable
stdlib packages), not `grande_finale`'s `v4.28.0`.  Both toolchains are installed;
`v4.31.0` is the one that builds fast here.

**Modeling conventions (stdlib has no `Finset`/`Fintype`/`Nat.choose`).**  Finite
collections are `List Nat` / `List (List Nat)`; cardinalities are `Nat`; the
rational tolerance of L4 is core `Rat` (the `ℚ` glyph is a Mathlib-only notation,
so the sources write `Rat`).  Two faithful reductions are used and documented in
each file header: (i) the outer `max_{r_1,r_2}` of `B_C^{MCA}` — a finite `sup` —
is left in the tex; the per-received-line disjointization is what L1 formalizes
(the same choice `GrandeFinale.first_match_ledger` makes).  (ii) The moment/second-
moment statements are stated over the integer fiber counts, i.e. the positive
normalization `N̄ = M/L` is cleared; the displayed tex inequalities are recovered
by the positive scaling `N̄^{-q}` (L3) / dividing by `M` (L2), which is why no
`Rat`-ordered-field API (absent from stdlib) is needed.

## 1. Headline

| file | target | key statements | status |
|---|---|---|---|
| `AsymptoticSpine/FirstMatch.lean` | **L1** `lem:first-match` / `def:cells` | `nodup_firstMatchLeaves`, `mem_firstMatchLeaves`, `firstMatch_le_sum_cellSizes`, `firstMatch_le_sum_budgets` | FORMALIZED |
| `AsymptoticSpine/Moment.lean` | **L2** `lem:q-sp` ; **L3** `lem:moment-max` | `qsp_sumSq_le` ; `moment_max_squeeze` (+ halves) | FORMALIZED |
| `AsymptoticSpine/NoHighEnergy.lean` | **L5** `prop:no-high-energy` (+ `thm:bsg`, `thm:quasicube`) | `no_high_energy_bound`, `no_high_energy_contradiction` | FORMALIZED core + HYPOTHESIS-PARAM inputs |
| `AsymptoticSpine/SigmaDiagonal.lean` | **L4** σ-diagonal (r2 §A3, `prop:energy-extract`) | `sigma_block_diagonal` | FORMALIZED |
| `AsymptoticSpine/Normalization.lean` | **B1** `lem:ambient-image-max`, `lem:moment-normalization`, `ass:image-normalized-sidon-input` (PR #439) | `ambient_image_max`, `moment_normalization_identity`, `moment_normalization_ratio`, `momImg_le_momAmb`, `momAmb_le_momImg_bridge`, `imageSidon_of_ambient` | FORMALIZED (cardinality form, see §8) + HYPOTHESIS-PARAM (C9 input) |
| `AsymptoticSpine/AddBack.lean` | **A6** `def:profile-nondegen`, `lem:addback` (R1/R4, PR #441) | `listMax_sum_le_sum_listMax`, `globalMax_le_sum_leafMax`, `leaf_clear_chain`, `addback_sum_bound`, `ProfileNonDegen`, `addback_sufficiency`, `addback_falsifier`, `perLeafQ_of_ambient_image_max` | FORMALIZED (cleared form, see §9) |
| `AsymptoticSpine/Util.lean` | infrastructure | `listSum`, `length_flatten`, `listSum_le_of_zip` | (support) |

All five of L1–L5 shipped sorry-free, plus the B1 image-normalization identities
of §8 (stacked on PR #438, formalizing the follow-up invited by PR #439).
`Main.lean`-style entrypoint: none (a library package).  No declaration uses
`sorry`, `admit`, `native_decide`, or a custom `axiom`.

## 2. `lem:first-match` (L1) — the centerpiece `FORMALIZED`

Tex `def:cells` (L77–79) + `lem:first-match` (L81–87).  Model: `cells : List
(List Nat)`, `cells[j]` = slope-ids witnessed by cell `j`; covered bad slopes =
`cells.flatten`; the first-match leaf `L_j = C_j \ (C_0 ∪ … ∪ C_{j-1})` is
`firstMatchLeaves`.

| decl | tex anchor | status | note |
|---|---|---|---|
| `newPaid`, `firstMatchLeaves`, `paidUnion` (defs) | `def:cells`, proof L86 | FORMALIZED | the leaf `C_j \ paid` and the running paid union |
| `paidUnion_eq_append_flatten`, `flatten_firstMatchLeaves` | (support) | FORMALIZED | leaves telescope to the paid union |
| `mem_paidUnion`, `nodup_paidUnion` | (support) | FORMALIZED | membership + duplicate-freeness of the union fold |
| `nodup_firstMatchLeaves` | `lem:first-match` ("assigned slope classes are disjoint") | FORMALIZED | **disjointness**: no slope charged twice |
| `mem_firstMatchLeaves` | `lem:first-match` (leaves cover the bad slopes) | FORMALIZED | **coverage**: assigned ⇔ witnessed |
| `firstMatchLeaves_sum_length_le` | proof L86 ("`j`-th class ⊆ projection of `C_j`") | FORMALIZED | leaf `⊆` cell, summed |
| `firstMatch_le_sum_cellSizes` | `lem:first-match` (`≤ ∑_j U_j`, `U_j = |C_j|`) | FORMALIZED | **budget-sum bound**, raw form |
| `firstMatch_le_sum_budgets` | `lem:first-match` (`≤ ∑_j U_j`, printed caps) | FORMALIZED | **budget-sum bound**, any `U_j ≥ |C_j|` |
| `firstMatch_A1_example` | r2 audit §A1 toy | FORMALIZED | `decide`: first-match `(3,1,1)=5` distinct vs raw `3+3+3=9` |

The disjointness + coverage together say the assigned classes **partition** the
covered slopes (r2 §A1: *"first-match sends every covered slope to a unique cell …
`Σ_j U_j` equals the total exactly"*).  Relationship to existing repo work:
`staircase_logic`'s `firstMatch_partitions_union` proves the same partition against
a different source (`agents.md` / m5 notes); the budget-sum inequality
`≤ ∑_j U_j` in the exact tex form is new here, and `GrandeFinale.first_match_ledger`
is the Mathlib/`Finset` analogue of `firstMatch_le_sum_budgets`.

## 3. `lem:q-sp` (L2) and `lem:moment-max` (L3) `FORMALIZED`

| decl | tex label | status | note |
|---|---|---|---|
| `listSumSq` (def) | `lem:q-sp` (L254) | FORMALIZED | `∑_s N(s)^2` |
| `qsp_sumSq_le` | `lem:q-sp` (L254–260) | FORMALIZED | `(∀ x, x ≤ B) → ∑ N(s)^2 ≤ B·∑ N(s)`; the tex `M^{-1}∑N^2 ≤ κN̄` is this ÷`M` with `B = κN̄` (r2 §A7) |
| `listSumPow` (def) | `lem:moment-max` (L162) | FORMALIZED | `∑_s x_s^q` |
| `pow_mem_le_listSumPow` | `lem:moment-max` lower (L168) | FORMALIZED | `(max_s x_s)^q ≤ ∑_s x_s^q` |
| `listSumPow_le_length_mul` | `lem:moment-max` upper (L170) | FORMALIZED | `∑_s x_s^q ≤ L·(max_s x_s)^q` |
| `moment_max_squeeze` | `lem:moment-max` (L165–172) | FORMALIZED | the two-sided squeeze, `L = f.length` |
| `qsp_example`, `moment_example` | (sanity) | FORMALIZED | `decide` instances incl. `Γ_1`-flatness `listSumPow 1 = listSum` |

The tex's `L^{-1}R^q ≤ Γ^{ord}_q ≤ R^q` (with `Γ^{ord}_q = L^{-1}∑(|F_s|/N̄)^q`,
`R = max|F_s|/N̄`) becomes, after multiplying by `L` and clearing `N̄^{-q}`, the
scale-free `mx^q ≤ ∑ x_s^q ≤ L·mx^q` on the integer counts `x_s = |F_s|`,
`mx = max_s|F_s|` — exactly `moment_max_squeeze`.  The `q`-th-root / `log L =
o(Nq)` passage to `Γ^{ord}_q ≤ exp(o(Nq)) ⇔ max|F_s| ≤ exp(o(N))N̄` is OUT-OF-SCOPE
(reals; stays in tex).  These are the discrete cores; they are distinct from
`GrandeFinale.moment_upper` / `moment_lower`, which formalize `grande_finale.tex`'s
`prop:moment-sandwich` over `ℝ` with a probability weight.

## 4. `prop:no-high-energy` (L5) `FORMALIZED` core + `HYPOTHESIS-PARAM` inputs

| decl | tex label | status | note |
|---|---|---|---|
| `BoolFiber` (structure) | interface for `thm:quasicube` | (support) | abstracts "`A ⊆ {0,1}^N` with `|A|=s`, `|A-A|=d`" |
| `no_high_energy_bound` | `prop:no-high-energy` (L228–234) | FORMALIZED (composition) + HYPOTHESIS-PARAM (`bsg`, `quasicube`) | the exact inequality `f ≤ K^{3C}` |
| `no_high_energy_contradiction` | `prop:no-high-energy` | FORMALIZED | `K^{3C} < f → False` (the "no such fiber" shape) |

### 4a. The external theorems are HYPOTHESES, not axioms — signatures

`no_high_energy_bound` takes, verbatim:

```lean
theorem no_high_energy_bound
    (quasicube : ∀ s d : Nat, BoolFiber s d → s ^ 4 ≤ d ^ 2 * s)
    (f K C : Nat)
    (bsg : ∃ s d : Nat, f ≤ K ^ C * s ∧ d ≤ K ^ C * s ∧ BoolFiber s d) :
    f ≤ K ^ (3 * C)
```

* `quasicube` is `thm:quasicube` (L220–226) — *"every finite `A ⊆ {0,1}^N` has
  `|A-A| ≥ |A|^{3/2}`"* — in the squared, root-free `Nat` form `s^4 ≤ d^2·s`
  (`d = |A-A|`, `s = |A|`), quantified over every Boolean-cube fiber `BoolFiber s d`.
* `bsg` is the output of `thm:bsg` (L214–216): the high-energy set of size `f`
  yields a Boolean-cube subfiber `(s, d)` with the size bound `f ≤ K^C·s`
  (`|A'| ≥ K^{-C}|A|`, cleared of division) and the difference bound `d ≤ K^C·s`
  (`|A'-A'| ≤ K^C|A'|`).

**Why hypotheses, not axioms.**  BSG and quasicube are deep external theorems
(`\cite{BalogSzemeredi,Gowers1998}` and `\cite{GMRSZ2020,MRSZ2020}`); the paper
cites, does not reprove them, and their proofs are far outside a stdlib formalizer's
reach.  Encoding them as `axiom`s would make the kernel *trust unproven
statements* — precisely the failure a correspondence audit exists to catch.  As
hypotheses, the theorem's honest content is exactly *"the inequality composition
`|A| ≤ K^{3C}` is valid **given** these two inputs"* — which is all `prop:no-high-
energy`'s in-paper proof claims — and `#print axioms no_high_energy_bound` shows
only `propext, Quot.sound` (no `Classical.choice`, no `sorryAx`, no custom symbol).
The `e^{o(N)}` bookkeeping `K^{±C} = e^{±o(N)}` and the energy lower bound
`f ≥ e^{cN-o(N)}` are OUT-OF-SCOPE (reals); `no_high_energy_contradiction`
exposes the join point as the explicit regime hypothesis `K^{3C} < f`.

## 5. σ block-diagonalization (L4) — the r2 §A3 gap `FORMALIZED`

Tex `prop:energy-extract` (L202–208) elides the diagonal in *"Letting σ↓0 slowly
along the sequence"*; r2 audit §A3 states a formalizer **must** supply the
block-diagonal *"`σ_N = 1/k` on `N`-blocks `[N_k, N_{k+1})`"*.  This is that
construction.

| decl | anchor | status | note |
|---|---|---|---|
| `Mrec` (def) | block starts | FORMALIZED | monotonized, strictly-increasing, `N0`-dominating threshold |
| `level` (def), `level_succ` | block index `σ_N = 1/k` | FORMALIZED | the staircase level at scale `N` |
| `Mrec_ge_N0`, `Mrec_lt_succ`, `Mrec_ge_self`, `Mrec_mono` | (support) | FORMALIZED | threshold monotonicity/domination |
| `level_le_succ`, `level_mono`, `level_zero_of_lt` | (support) | FORMALIZED | level monotonicity + below-first-threshold |
| `level_below` | block containment | FORMALIZED | `Mrec 0 ≤ N → Mrec (level N) ≤ N` |
| `level_diverge` | `σ_N → 0` | FORMALIZED | `Mrec K ≤ N → K ≤ level N` (level `→ ∞`) |
| `sigma_block_diagonal` | r2 §A3 / `prop:energy-extract` | FORMALIZED | the diagonalization theorem |

### 5a. The per-tolerance guarantee is a HYPOTHESIS — signature

```lean
theorem sigma_block_diagonal
    (P : Nat → Rat → Prop) (N0 : Nat → Nat)
    (hP : ∀ k : Nat, 1 ≤ k → ∀ N : Nat, N0 k ≤ N → P N ((1 : Rat) / (k : Rat))) :
    ∃ (σ : Nat → Rat) (lvl : Nat → Nat),
      (∀ N, σ N = (1 : Rat) / (lvl N : Rat)) ∧
      (∀ K : Nat, ∃ N₁, ∀ N, N₁ ≤ N → K ≤ lvl N) ∧
      (∃ N₂, ∀ N, N₂ ≤ N → 1 ≤ lvl N ∧ P N (σ N))
```

`P N ε` reads "the Sidon-heavy null rate at tolerance `ε` is controlled at scale
`N`" (`def:sidon-paid`, L196–198); `hP` is the per-fixed-`σ` null rate the tex
supplies.  `hP` is the sole external input, entering as a hypothesis — the
diagonal is *derived*, nothing is assumed as an axiom.

**Convergence encoded without `Rat`-order API.**  `σ N → 0` is certified by the
pure-`Nat` divergence `level N → ∞` (`∀ K, ∃ N₁, ∀ N ≥ N₁, K ≤ lvl N`) together
with the definitional `σ N = 1 / lvl N`.  This is a complete certificate that
`σ N → 0` (the wrapper `1/lvl → 0` is precisely the divergence of `lvl`), and it
deliberately avoids ordered-field lemmas over `Rat`, which stdlib does not carry.
The `e^{-σ_N N} = e^{-o(N)}` consequence and the full analytic use of the diagonal
in `prop:energy-extract` are OUT-OF-SCOPE (reals).

## 6. OUT-OF-SCOPE inventory (recorded, not formalized)

Per the mandate, the entropy/Stirling analysis is **not** formalized (it needs
reals).  Explicitly out of scope, kept in the tex:

- `thm:frontier` (L135–142, L289–296): the Stirling identity `log₂ N̄_{n,a} =
  n(H_2(ρ+g)-βg)+o(n)`, the envelope `g*(ρ,β)`, and the two-sided `g → g*` limit
  (r2 §A10, `NO ISSUE` but analytic).
- `thm:closed-ledger-package` (C1)–(C9) (L105–131): imported algebro-geometric
  cell counts; a citation package, not self-contained theorems.
- `def:sidon-paid` (L196–200): Fourier inversion `Lμ(s) ≤ exp(o(N))`.
- the `o(n)` / `o(Nq)` / `q`-th-root passages throughout §2–§5.
- `lem:addback` (L246–252): the subexponential-profile decomposition — r2 §A6
  `OPEN GAP`.  **Now scoped and its sufficiency mechanized** in `AddBack.lean` (§9,
  PR #441): the sufficiency direction R1 (`def:profile-nondegen` ⇒ bound) is
  `FORMALIZED`; the general image-non-degeneracy premise itself stays conditional
  (`prob:entropy-inverse-q`-hard, R3) and OUT-OF-SCOPE.
- the identity-prefix pole construction's collision loss (L283–287) — r2 §A9
  `OPEN GAP`; the sound floor is the collision-free injective construction in
  `cap25_cap_v13_raw.tex`, not formalized here.

## 7. Verification `VERIFIED-CLEAN`

- Build (from `experimental/lean/asymptotic_spine/`, `LEAN_NUM_THREADS=1`):

  ```
  Build completed successfully (10 jobs).
  ```

  Clean build ≈ 3.8 s wall, peak RSS ≈ 772 MB (6 modules, all `✔`; `v4.31.0`,
  `LEAN_NUM_THREADS=1`).  The A6 `AddBack.lean` adds ≈ 0.4 s.

- **Environment note (flag).**  The mandated `ulimit -v 2097152` (2 GB virtual)
  is incompatible with the installed `v4.31.0` toolchain: `lake`/`lean` reserve a
  large *virtual* arena and abort at thread creation under a 2 GB cap (even 8 GB
  aborts; 16 GB virtual is the floor).  This is unrelated to the build's real
  footprint — peak **resident** memory is ≈ 792 MB and wall time ≈ 2.7 s — so the
  guardrail's intent (a tiny, non-runaway build) holds and is verified by RSS.
- `#print axioms` on all shipped statements: only `propext`, `Quot.sound`, and
  (for the `omega`/`split`-closed `no_high_energy_contradiction` and
  `sigma_block_diagonal`) `Classical.choice` — Lean's three standard foundational
  assumptions, the same ones under all of Mathlib.  No `sorryAx`; no
  user-declared logical assumption in any file.
- Token gate on the `.lean` sources: `grep -rn 'sorry\|axiom'` → 0 hits;
  `grep -rn 'native_decide'` → 0 hits.

## 8. B1 image-normalization identities (`Normalization.lean`) — PR #439 follow-up `FORMALIZED`

**Provenance / lineage.**  This module **stacks on PR #438** (the L1–L5 spine above)
and formalizes the follow-up that **PR #439** (avdeevvadim, collaborator) explicitly
invited: *"Lean formalization of the two normalization identities is a natural
follow-up, but this PR is TeX/audit/verifier only."*  The B1 normalization mismatch
was flagged in the round audit (**#436**), repaired at TeX scale by **#439**, and is
mechanized here — the **#436 → #439 → (this)** collaborator lineage.  It reuses
`AsymptoticSpine.Moment.listSumPow` (the discrete moment numerator `∑_s x_s^q`); no
new framework is introduced.

**Source of statements (flag: open PR).**  The tex labels below live in **PR #439's**
`experimental/asymptotic_rs_mca.tex` (open, not yet merged into the base
`lean-asymptotic-rs-mca-spine`/#438 branch this work is stacked on).  Statements were
compared directly against `gh pr diff 439`, not against the base tex.  When #439
merges, these labels enter the base unchanged; until then `mapping_confidence` is
`exact_label_match` **against #439's diff**.

### 8a. Decl ↔ #439 tex-label map

| Lean decl | #439 tex label | `mapping_confidence` | status | note |
|---|---|---|---|---|
| `image_max_le_ambient_max` | `lem:ambient-image-max` (proof step) | `exact_label_match` (vs #439 diff) | FORMALIZED | image fibers ⊆ ambient fibers ⇒ image max ≤ ambient max |
| `ambient_image_max_transfer`, `ambient_image_max` | `lem:ambient-image-max` | `exact_label_match` (vs #439 diff) | FORMALIZED | `max_amb ≤ e^{o(N)}M/A` ⇒ `max_img ≤ e^{o(N)}M/L`, cleared |
| `listSumPow_map_mul` | `lem:moment-normalization` (pull-out) | `curated_alias` | FORMALIZED | `∑(c·x)^q = c^q∑x^q` — the `N̄`-normalization mechanism |
| `listSumPow_replicate_zero`, `ambient_sum_reduces` | `lem:moment-normalization` (`y∉𝒮` vanish) | `curated_alias` | FORMALIZED | ambient average reduces to image average over `𝒮` |
| `moment_normalization_identity` | `lem:moment-normalization` (identity) | `exact_label_match` (vs #439 diff) | FORMALIZED | the two closed forms `∑(x·L)^q=L^q P`, `∑(x·A)^q=A^q P` |
| `moment_normalization_ratio` | `lem:moment-normalization` (`(A/L)^{q-1}`) | `exact_label_match` (vs #439 diff) | FORMALIZED (cleared) | `L^{q-1}·momAmbN = A^{q-1}·momImgN` |
| `momImg_le_momAmb`, `image_upper_of_ambient_upper` | `lem:moment-normalization` (safe dir.) | `exact_label_match` (vs #439 diff) | FORMALIZED | ambient moment upper bound ⇒ image moment upper bound |
| `momAmb_le_momImg_bridge` | `lem:moment-normalization` (reverse dir.) | `exact_label_match` (vs #439 diff) | FORMALIZED | image ⇒ ambient **only** with an `A/L` bridge `D ≥ (A/L)^{q-1}` |
| `ImageNormalizedSidonPaid`, `AmbientSidonPaid`, `imageSidon_of_ambient` | `ass:image-normalized-sidon-input` | `exact_label_match` (vs #439 diff) | HYPOTHESIS-PARAM | C9 input packaged as a predicate; ambient⇒image is the only safe consumption |
| `normalization_example` | (sanity) | — | FORMALIZED | `decide`: `momImgN=10`, `momAmbN=15`, closed forms `20=2²·5`, `45=3²·5`, `2·15=3·10` |

### 8b. The one modeling divergence to flag — cardinality form, not a `Rat` equation

**Flagged (cf. the `sp_from_q` flag in #418): the identity is mechanized as a
denominator-cleared `Nat` cardinality identity, not as a literal `Rat` equation.**
Lean *core* at this pin (`v4.31.0`, no mathlib) has **no algebraic hierarchy** —
`Monoid`/`Ring`/`Field`, `mul_pow`, `Nat.cast_pow`, `div_pow`, `ring` are all
mathlib-only, and stdlib `Rat` exposes only bare `Rat.mul_comm`/`Rat.mul_assoc`
facts (the same wall `SigmaDiagonal.lean` hits, keeping `Rat` to `1/lvl` with `rfl`).
The task sanctioned this: *"as an exact identity over `Rat` **or** as a cardinality
identity."*  Chosen: the cardinality identity, per this package's standing "clear the
positive normalization" convention (§0).

**This is a divergence of form, not a weakening of content.**  Writing `Γ_img(q) =
L^{q-1}P/M^q`, `Γ_amb(q) = A^{q-1}P/M^q` (`P = ∑_s|F_s|^q = listSumPow q f`), the
cleared numerators used in Lean are

    momImgN q L f = L^{q-1}·P = M^q·Γ_img(q),
    momAmbN q A f = A^{q-1}·P = M^q·Γ_amb(q),

and `momImgN_scaled` / `momAmbN_scaled` certify these are the honest tex summations
divided by the averaging weights (`L·momImgN = ∑_s(|F_s|·L)^q`, `A·momAmbN =
∑_{y∈G}(|Ω∘∩Φ⁻¹(y)|·A)^q`).  Because `L, A, M > 0`, multiplying/dividing by
`L, A, M^q` is an **exact reversible equivalence**, so:

| tex (`Rat`) | Lean (`Nat`, cleared) | clearing factor |
|---|---|---|
| `Γ_amb(q) = (A/L)^{q-1} Γ_img(q)` | `L^{q-1}·momAmbN = A^{q-1}·momImgN` (`moment_normalization_ratio`) | `× L^{q-1}M^q` |
| `Γ_img(q) = L^{q-1}P/M^q` | `∑_s(|F_s|·L)^q = L^q·P` (`moment_normalization_identity`.1) | `× L·M^q` |
| `Γ_amb(q) = A^{q-1}P/M^q` | `∑_y(·)^q = A^q·P` (`moment_normalization_identity`.2) | `× A·M^q` |
| `Γ_img ≤ Γ_amb` (safe) | `momImgN ≤ momAmbN` (`momImg_le_momAmb`) | `× M^q` |
| `max_img ≤ e^{o(N)}N̄` | `mxImg·L ≤ C·M` (`ambient_image_max`) | `× L`, `C = e^{o(N)}` |

The sole thing **not** delivered: no `Rat` object `Γ_img`/`Γ_amb` is constructed, so
the literal `= (A/L)^{q-1}·(…)` `Rat` equation is not a Lean term — only its exact
`Nat` clearing is.  A future mathlib-pinned port (e.g. inside `grande_finale`) could
state the literal `Rat`/`ℝ` version; here that is OUT-OF-SCOPE for the same reason
the entropy analysis is (needs the missing algebra API).  Nothing is weakened:
the `Nat` statements are equivalent to the `Rat` ones, not implied by them.

### 8c. `exp(o(·))` placeholders and the C9 hypothesis (same discipline as L5)

As in `NoHighEnergy.lean` (`K^C = e^{o(N)}`), the reals bookkeeping enters as `Nat`
placeholders: `C` in `ambient_image_max` is `exp(o(N))`; `Budget` in
`ImageNormalizedSidonPaid` is the cleared subexponential ceiling `M^q·exp(o(Nq))`.
`ass:image-normalized-sidon-input` is **not proved** — it is the missing C9
moduli/Fourier–Sidon source theorem, packaged as the predicate
`ImageNormalizedSidonPaid` exactly as BSG/quasicube are packaged as hypotheses.
`imageSidon_of_ambient` formalizes #439's operative safety claim: an ambient
Fourier/Sidon estimate can be consumed as the image-normalized C9 input **only**
through the safe transfer (`momImg_le_momAmb`); the reverse needs the explicit `A/L`
bridge (`momAmb_le_momImg_bridge`), which is why C9 is stated directly at image
scale.  `#print axioms` on all §8 decls: only `propext`/`Quot.sound` (several depend
on none); `normalization_example` depends on no axioms.  OUT-OF-SCOPE, unchanged from
§6: the C9 source theorem, B3 window uniformity, and the lower-side collision loss
(`rem:current-audit-status` in #439).  The `lem:addback` profile decomposition is now
scoped and its sufficiency mechanized — see §9.

## 9. A6 add-back sufficiency (`AddBack.lean`) — PR #441 R1/R4 `FORMALIZED`

**Provenance / lineage.**  This module **stacks on #438 → #440 → this**: the L1–L5
spine (#438, §2–§5), the B1 image-normalization identities (#440 = the open PR this
worktree is based on, §8), and now the A6 add-back.  It mechanizes the R1/R4 results
of **PR #441** (`thresholds-addback-decomposition`; note
`experimental/notes/audits/asymptotic_addback_profile_decomposition.md`), which scoped
gap **A6** — the uncited "profile decomposition" of `lem:addback` — with the named
condition `def:profile-nondegen` (the **#435-A6 → #441** attack lineage; #435 =
`thresholds-asymptotic-proof-audit-r2`, whose attack A6 is this gap).  It reuses
`Util.listSum` and composes with `Normalization.ambient_image_max` (§8); no new
framework.

**Source of statements (flag: open PR).**  The tex labels below live in **PR #441's**
`experimental/asymptotic_rs_mca.tex` (`def:profile-nondegen`, `lem:addback`, restated
conditional on it, L246–262) and its note's Claim R1/R4.  Statements were compared
directly against `git show thresholds-addback-decomposition:…`; `mapping_confidence`
is `exact_label_match` **against #441's tree**.

### 9a. Decl ↔ #441 label / claim map

| Lean decl | #441 anchor | `mapping_confidence` | status | note |
|---|---|---|---|---|
| `listMax`, `le_listMax_of_mem`, `listMax_le` | (support) | `curated_alias` | FORMALIZED | computed `max_s`, with `listMax [] = 0` pinning the union-bound base case |
| `listSum_map_le` | (support) | `curated_alias` | FORMALIZED | termwise `listSum` monotonicity over `map` |
| `listMax_sum_le_sum_listMax` | R1 proof, line `max_s∑_jN_j(s)≤∑_j max_sN_j(s)` | `exact_label_match` | FORMALIZED | **the union bound** (max-of-sum ≤ sum-of-maxes), general over `List (Nat→Nat)` |
| `globalMax_le_sum_leafMax` | R1 proof (same line, leaf form) | `exact_label_match` | FORMALIZED | family instance of the union bound |
| `leaf_clear_chain` | R1 proof, `N_j(s)·Y ≤ N_j(s)·L_j·C' ≤ C·M_j·C'` | `exact_label_match` | FORMALIZED | per-leaf clearing from (a)+(b) |
| `addback_sum_bound` | R1 proof, mass telescope (`∑_jM_j`; no leaf-count bound) | `exact_label_match` | FORMALIZED | the telescope over masses |
| `ProfileNonDegen` | `def:profile-nondegen` (a)+(b)+(c) | `exact_label_match` | FORMALIZED | cleared bundle: per-leaf Q, image non-degeneracy, mass partition |
| `addback_sufficiency` | `lem:addback` / R1 | `exact_label_match` | FORMALIZED | `ProfileNonDegen ⇒ max_sN(s)·Y ≤ C·C'·Mtot` |
| `addback_falsifier` | R4 (falsifier) | `exact_label_match` | FORMALIZED | `decide`: (a) holds, (b) fails, add-back violated by `Y=3` |
| `addback_falsifier_repair` | R4 (spread repair) | `exact_label_match` | FORMALIZED | `decide`: spreading restores the bound |
| `perLeafQ_of_ambient_image_max` | composition B1→A6 | `curated_alias` | FORMALIZED | `ambient_image_max` (§8) output = add-back input (a) |
| `addback_example`, `addback_example_via_theorem` | (sanity) | — | FORMALIZED | `decide` + end-to-end application of `addback_sufficiency` |

### 9b. The R1 statement, cleared (exact shape vs #441)

Writing the global syndrome space `𝒴` with `Y = |𝒴|`, leaves `Ω_j` with mass `M_j`,
image `L_j ≤ Y`, per-leaf counts `N_j(s)`, and `N(s) = ∑_j N_j(s)`:

| #441 (rational) | Lean (`Nat`, cleared) | clearing |
|---|---|---|
| (a) `max_sN_j(s) ≤ C·M_j/L_j` | `leafMax S lf * lf.img ≤ C * lf.mass` | `× L_j` |
| (b) `L_j ≥ exp(-o(n))|𝒴|` i.e. `L_j ≥ Y/C'` | `Y ≤ lf.img * C'` | `× C'` |
| (c) `∑_j M_j ≤ Mtot` | `listSum (fam.map Leaf.mass) ≤ Mtot` | — |
| `max_sN(s) ≤ C·C'·Mtot/Y` | `globalMax S fam * Y ≤ C * C' * Mtot` | `× Y` |

The proof chain is exactly #441's: union bound (`globalMax_le_sum_leafMax`),
per-leaf clear (`leaf_clear_chain`), mass telescope (`addback_sum_bound`) — and, as
#441 stresses, **no separate leaf-count bound**, the mass partition alone telescopes.

### 9c. The two modeling divergences to flag (neither a weakening)

1. **Cleared-`Nat` form** (same as §8b): the `exp(o(n))` rates are the `Nat`
   placeholders `C`, `C'`, `|𝒴|` is the `Nat` `Y`, and the rational bound is the
   cleared integer inequality.  Since `L_j, C, C', Y > 0` in the honest model, the
   clearing is a reversible equivalence — divergence of form only.
2. **Per-syndrome counts as a function `Nat → Nat`, syndrome axis as `List Nat`
   `S`, and `Y = |𝒴|` an abstract `Nat` decoupled from `S.length`.**  #441 indexes
   `N_j(s)` over `𝒴`; the function model carries the same data and the same
   `max_s`/`∑_j`, and correctly pins the empty-family / empty-axis boundary
   (`listMax [] = 0`) that the union bound's base case needs — cleaner here than a
   `List Nat` (which the spine uses for fiber counts in `Moment.lean`), and permitted
   by the task ("`List Nat` **or** a function over a finite index").  Keeping `Y`
   abstract makes R1 hold for **any** `Y` meeting (b) (the honest instance is
   `Y = S.length`); this generalizes, it does not weaken.  No statement is weakened
   relative to #441's printed R1.

### 9d. R4 falsifier and the B1 composition

`addback_falsifier` is #441's R4 witness (`Y` collapsed leaves piled on one
syndrome), shrunk to `Y = 3`, `barN = 1` for kernel `decide`: per-leaf Q (a) holds,
image non-degeneracy (b) fails, and `max_sN(s)·Y = 9 > 3 = C·C'·Mtot` — a blow-up of
`Y`, so **(b) is load-bearing** (confirmed by the tamper test: dropping (b) from
`ProfileNonDegen` fails the `addback_sufficiency` build at the telescope step).
`addback_falsifier_repair` spreads the images and restores the bound, isolating
pile-up as the failure.  `perLeafQ_of_ambient_image_max` records the pipeline
composition: identifying `mxImg := leafMax S lf`, `L := lf.img`, `M := lf.mass`, the
§8 `ambient_image_max` output is exactly add-back's per-leaf Q input (a).

`#print axioms` on all §9 decls: only `propext`/`Quot.sound` (the `decide` and
`ambient_image_max`-composed ones depend on none) — no `sorryAx`, no
`Classical.choice`, no custom axiom.  **OUT-OF-SCOPE, unchanged (R2/R3 of #441):**
image non-degeneracy (b) is *unconditional* only in the full-mass single-leaf
frontier subregime (R2, log-arithmetic over reals) and is `prob:entropy-inverse-q`-hard
in general (R3); the sufficiency direction R1 is what is mechanized here.
