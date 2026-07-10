# Balanced-core kappa growth: residual charts force kappa = k = Theta(n)

**Lane:** residual (1) of PR #528 (`thresholds-ray-compiler-balanced-core`,
note `experimental/notes/thresholds/ray_compiler_balanced_core.md`) --- the
**kappa-growth** question for the balanced core, *not* the atlas-count question.
Direct attack. **Target file:** `experimental/asymptotic_rs_mca_frontiers.tex`
(worktree base `4e3c4ee`). **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_kappa_growth.py` (stdlib-only,
zero-arg, `RESULT: PASS (95 checks)`, ~1.6 s; recomputes every gated number
below with exact prime-field arithmetic).

**Highest rung reached: 3 (REFUTE) + 4 (census) + 5 (named wall).**
**Verdict: `REFUTED`** for the proposition *"the per-chart transverse-secant
route can bound the residual balanced-core kernel dimension `kappa` to
`o(n/log n)`"* --- with an explicit `COUNTEREXAMPLE`-class family and an exact
census. Equivalently, PR #528's residual (1) resolves **negatively for the
per-chart reading**: on genuinely residual balanced-core charts `kappa = Theta(n)`
is not merely possible but **generic/dominant**. The content of the
kappa-growth question therefore lives **entirely** in condition (A2) (atlas
decomposition) or (A4) (Sidon/Fourier), which is a **`WALL`** stated precisely
below. No claim is made against the paper's *conditional* theorem: (A6) already
*assumes* each balanced-core chart is paid; this lane shows the PR #528 per-chart
payment is not the mechanism for the residual charts.

Credit: builds directly on **PR #528** (this worktree's parent lane), which
proved the field-independent per-chart bound `|Z| <= C(R+kappa, kappa+1)` and
flagged residual (1) ("is the residual balanced-core kernel dimension
`o(n/log n)`?") as an open `WALL`. This lane answers that flagged wall.

---

## 1. Anatomy (rung 1) --- exact extraction, gated

### 1.1 Two exact relationships for `kappa` (the crux the task asks to pin)

Write `R = n - k` (redundancy), and for a chart `U subset D` let
`kappa(U) = dim ker(H_U : F^U -> F^R)`. For a Reed--Solomon (MDS/Vandermonde)
parity check, `lem:vandermonde-image-rank-expanded` (L7040) gives
`rank H_U = min(|U|, R)`, hence

```
    kappa(U) = max(0, |U| - R).                                   (K1)
```
[`thm:bounded-residual-kernel-ray`, L1684/L1698; recomputed group B, exact.]

Now let a balanced-core chart be a family `{S_gamma}` of **agreement supports**
(size `a`, locators `Q_{S_gamma}`) sharing a depth-`w` common prefix
(`w = a-k-1`, L4443--4446; the profile grouping of `def:profile-cell` L1417).
Its **error supports** are `E_gamma = D \ S_gamma` (the objects of
`thm:syndrome-secant-exact`, L1606, `eq:transverse-secant-count` L1615), and the
chart is `U = union_gamma E_gamma`. Since
`union E_gamma = D \ intersection S_gamma`,

```
    kappa = max(0, k - |C|),      C := intersection_gamma S_gamma
                                     = the common agreement core,  (K2)
```
since `|U| = |D \ C| = n - |C|` exactly and (K1) caps at zero. On any chart
with `|C| <= k` this reads `kappa = k - |C|`; the `max` clause only bites on
families whose common core exceeds `k` (barely-residual charts outside the
refutation regime; `C = empty` is unaffected).
[Set-theoretic identity `|U| = n - |C|` + (K1); verified equal to (K1) over
**every** enumerated prefix class in group C, all four configs --- gated
`C.identity.*`, exact.]

**(K2) is the precise "kappa vs profile data" relationship.** It is the paper's
own description made quantitative: L892--893 states *"a balanced-core chart
records the higher-dimensional locator **kernel** that may remain **after their
common core is factored**."* Equation (K2) is exactly that sentence:
`kappa` = (residual code dimension `k`) minus (size of the factored-out common
core `|C|`).

### 1.2 The moving-coefficient projective dimension is INDEPENDENT of `kappa`

The balanced-core chart is *defined* (L4526--4530, and L2456--2474) by its
**moving coefficient space having projective dimension > 1**; projective
dimension `1` is the split pencil `Q_0 + lambda Q_1` (L2461--2464, and the
top-stratum `A-B=c` picture at L7056). Denote this dimension `d_proj`
(the projective span of the deep-coefficient vectors `(q_{w+1},...,q_a)(S)`).

**Finding [`EXTRACTED`, gated]:** `d_proj` (agreement/locator side; *which* ray
tool applies) and `kappa` (error/kernel side; *how good* the secant tool is) are
**independent**. The census exhibits balanced cores with `d_proj < kappa`
(n=12: `d_proj=4 < kappa=5`) and with `d_proj > kappa`
(n=14: `d_proj=7 > kappa=6`); `kappa` is not a function of `d_proj`
[gated `C.projdim_kappa_independent`, exact]. Consequently:

> "Projective dimension > 1" (balanced core) does **not** constrain `kappa`.
> A chart can be a genuine higher-dimensional balanced core (`d_proj >= 2`)
> and simultaneously have the largest possible kernel `kappa = k`.

This corrects the tempting guess `d_proj = kappa`: the pencil/curve escalation
(`prop:split-pencil-payment` L4741, `prop:curve-degree-ray-compiler` L5895) is
graded by `d_proj`, while the secant-bound *quality* `C(R+kappa,kappa+1)` is
graded by the **orthogonal** parameter `kappa = k - |C|`.

### 1.3 Why profile complexity does NOT bound `kappa`

`def:profile-complexity` (L7241) bounds the **number** of realized `(lambda,xi)`
pairs (the atlas census, condition (A2), `lem:profile-atlas` L4772), *not* the
dimension inside one chart. It is the per-chart's-count / number-of-charts split
that PR #528 already named as residuals (1) vs (2). So there is no route from
`profile complexity = o(n)` to `kappa = o(n/log n)`; they are different axes.
[`EXTRACTED`, checked against L7241, L4772, L905--911.]

### 1.4 What the per-chart bound needs, and the trivial ceiling

The moving coefficients live in the deep-coefficient space of dimension
`a - w = k+1`, so trivially `d_proj <= k` and (via `U subset D`)
`kappa <= k`. In the constant-rate regime `k = Theta(n)`, this ceiling is
`kappa <= Theta(n)`, **not** `o(n/log n)`: the dimension count alone gives no
subexponential secant bound. [`EXTRACTED`, elementary.]

---

## 2. Refutation (rungs 2--3): residual => empty core => kappa = k = Theta(n)

### 2.1 The mechanism

The balanced core is the residual **after all common factors are removed**
(L4526--4529). A common factor is a shared `D`-root, i.e. a point in *every*
`S_gamma`, i.e. an element of the common core `C`. Removing common factors
**empties `C`**. By (K2), an empty common core forces the **maximal** kernel:

```
    C = empty   ==>   kappa = k - 0 = k = Theta(n)   (constant rate).   (R1)
```

Then the PR #528 per-chart bound is
`C(R+kappa, kappa+1) = C(R+k, k+1) = e^{Theta(n)}` --- **vacuous**:
`log2 C(R+k, k+1) / n -> ~1` [gated `A.growth.*`, group A: the ratio is
`0.73, 0.84, 0.91, 0.95, 0.97` at `n = 8, 16, 32, 64, 128`]. Because PR #528
proved this constant **sharp for `kappa <= 2`**, no better field-independent
per-chart constant of that shape exists; the per-chart route *cannot* be
rescued by a smaller constant. `[REFUTED for the per-chart route.]`

The o(n/log n)-good regime of PR #528 therefore requires
`kappa = k - |C| = o(n/log n)`, i.e. a common core `|C| = k - o(n/log n)` that
retains an **almost-full common factor** --- precisely the situation the
balanced core is defined to have *removed*. So the secant bound only helps on
charts that are barely residual.

### 2.2 Explicit scalable residual family (`COUNTEREXAMPLE`, exact)

`disjoint_equal_prefix_pair` builds, via a tiled **Prouhet--Thue--Morse** split
of `[1..n]`, two **disjoint** equal-size supports `S_1, S_2` with equal power
sums `p_1,...,p_w` (Prouhet's theorem), hence an equal depth-`w` locator prefix
over `F_p` [directly verified, gated `D1.prefix_eq.*`]. Disjoint `=> C = empty
=> kappa = k` [gated `D1.core_empty.*`, `D1.kappa_eq_k.*`]:

| n | a | k | R | kappa | log2 C(R+kappa,kappa+1) | / n |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 8 | 5 | 11 | 5 | 13.0 | 0.81 |
| 32 | 16 | 13 | 19 | 13 | 28.8 | 0.90 |
| 64 | 32 | 29 | 35 | 29 | 60.5 | 0.945 |
| 128 | 64 | 61 | 67 | 61 | 124.1 | 0.969 |

`kappa = k` grows linearly in `n` and the secant constant is superpolynomial
[gated `D1.kappa_theta_n`]. These pairs are proj-dim-1 residual **shift-pair**
charts (still requiring payment under (A6)); the proj-dim-`>= 2` genuine
balanced cores with `kappa = k` are exhibited by the census in section 3.

**Residual proxies checked** on these charts: empty common core (no removable
common factor), `H_U` full rank `R` (no certified rank degeneracy on the chart),
and --- for the census witnesses --- `d_proj >= 2` (genuine balanced core, not a
pencil/curve). These are the four removal classes of L4526--4529.

### 2.3 Robustness to the actual removal pipeline (checked)

The census (section 3) groups **raw** prefix classes, not post-first-match
residuals. Set arithmetic cuts both ways here and the honest statement is
definitional: (i) deleting members from a family can only **enlarge** the
intersection (`C` over fewer sets contains `C` over all), so a sub-chart carved
out by planted/quotient removal may regain a nonempty core and a *smaller*
per-sub-chart `kappa` --- but any regained common core is itself a common
factor, which the pipeline (L4526--4529) factors out again; a chart that is
*genuinely residual* (no common factor left, which is what "balanced core"
means) has `C = empty` **by definition** and hence `kappa = k` by (K2).
(ii) Subdividing a large `C = empty` class into many low-`kappa` sub-charts is
therefore not a rescue of the single-chart route: it trades kernel dimension
for **chart count**, which is exactly condition (A2)'s decomposition question
(`lem:profile-atlas` L4772) --- the wall named in section 4, not avoided.
(iii) A class with subexponential mass has `|Z| = e^{o(n)}` trivially and needs
no ray bound; the dangerous large-mass classes already have `C = empty` in the
census. [`AUDIT`, argued; the census `C = empty` on the largest classes is
exact, and the definitional step is the chart definition itself.]

---

## 3. Census (rung 4) --- exact, `RESULT: PASS`

Exhaustive enumeration of all `a`-subsets of `D = {1,...,n} subset F_p`, grouped
by depth-`w=2` common prefix; each class with `d_proj >= 2` is a balanced-core
chart. Every `kappa` is recomputed two ways ((K1) direct kernel, (K2) core) and
they agree on **all** classes.

| p | n | k | classes | balanced cores | largest BC (size, d_proj, kappa, core) | frac(kappa=k) |
|---:|---:|---:|---:|---:|:---|---:|
| 13 | 12 | 5 | 169 | 97 | (5, 4, **5=k**, 0) | 0.26 |
| 17 | 14 | 6 | 289 | 288 | (11, 7, **6=k**, 0) | 0.84 |
| 17 | 16 | 7 | 289 | 289 | (32, 8, **7=k**, 0) | **1.00** |
| 19 | 18 | 8 | 361 | 361 | (95, 9, **8=k**, 0) | **1.00** |

**Outcome.** (i) The **largest** balanced core (most members ~ most rays)
*always* has empty common core and `kappa = k` [gated `C.largest_bc_kappa.*`].
(ii) The mass **concentrates** at maximal `kappa = k`: the fraction of balanced
cores with `kappa = k` rises `0.26 -> 0.84 -> 1.00 -> 1.00`; by `n = 16` **every**
enumerated balanced core has `kappa = k` [gated `C.mass_concentrates_at_kappa_k`].
(iii) `kappa_max = k` in every config and grows with `n`
[gated `C.kappa_grows_with_n`] --- an empirical `kappa_max = Theta(n)`.
(iv) Largest-BC class size grows `5 -> 11 -> 32 -> 95` while `kappa = k` ---
these are large families *and* maximal kernel simultaneously. This is the
empirical calibration the task asked for: **the mass sits at `kappa = k`, the
opposite of the `o(n/log n)` regime the per-chart bound needs.**

A concrete `n=18` witness (empty core, `d_proj=9`, `kappa=8=k`), first four of
95 members, printed by the verifier:
`{1..10,12}`, `{1..8,15,17,18}`, `{1..6,8,10,13,16,18}`, `{1..6,9,12,13,15,16}`.

---

## 4. The wall (rung 5) --- precise missing statement, cheap routes dead

**Named wall.** The per-chart transverse-secant bound (PR #528) discharges (A6)
`only` on charts with `kappa = k - |C| = o(n/log n)`, i.e. common core
`|C| = k - o(n/log n)`. Residual balanced-core charts have `|C| = 0` (generic),
so **(A6) on the residual is not dischargeable per-chart.** The missing input,
in the paper's vocabulary, is exactly the *second* half of
`rem:balanced-core-exhaustion` (L4762--4769):

> a proof that a higher-dimensional residual balanced core **decomposes into
> `e^{o(n)}` sub-charts each of kernel dimension `o(n/log n)`** (condition (A2),
> `lem:profile-atlas` L4772), **or** that its large-mass instances are paid by
> the analytic (A4) Sidon/Fourier route (`prop:smooth-circle-prefix-flatness-
> criterion` L6593, `lem:residual-monotonicity` L6574).

This lane proves the *first* half of that remark (the "higher-dimensional
coefficient family" per-chart count, via PR #528) is **the wrong tool for the
residual**: it is exponential exactly where it is needed. The burden is 100% on
(A2)/(A4). Note the census hint: the large-`kappa` charts are large *families*
(size 32, 95, ...), i.e. exactly the regime where the Fourier/Sidon flatness of
(A4) --- not the ray compiler --- is designed to pay; but no proof that (A4)
covers precisely the `kappa = Theta(n)` charts is given here or in the paper.

**Cheap routes checked dead.**
- *Smaller per-chart constant:* impossible --- PR #528's `C(R+kappa,kappa+1)` is
  sharp for `kappa <= 2` (its group-D null), so no `C(R+kappa,kappa+1)`-shape
  constant beats it. `[DEAD, cited.]`
- *Dimension ceiling:* `kappa <= k` only, `= Theta(n)` at constant rate (1.4).
  `[DEAD, elementary.]`
- *Profile-complexity bound:* bounds chart **count**, not `kappa` (1.3).
  `[DEAD, def:profile-complexity L7241.]`
- *"Balanced core has small U by construction":* false --- L4526 imposes no size
  bound; (A6) L942 *assumes* payment, `rem:balanced-core-exhaustion` explicitly
  leaves decomposition open. `[DEAD, textual.]`
- *proj-dim controls kappa:* false --- independent (1.2). `[DEAD, gated.]`

---

## 5. Proposed ledger entries (proposed; NOT applied to `.tex`/`.pdf`)

Format per `experimental/asymptotic_rs_mca.md` (Source / Status / Paper impact /
Next action).

### L-KG-1 (sharpen PR #528's residual (1) from "open" to "negatively resolved for the per-chart route")
- **Source:** this lane; `verify_kappa_growth.py`.
- **Status:** `REFUTED` (per-chart route) / `COUNTEREXAMPLE` (explicit residual
  family) / `AUDIT`.
- **Paper impact:** In `rem:balanced-core-exhaustion` (L4762) and at
  L1088--1090, record that the per-chart transverse-secant bound
  `C(R+kappa,kappa+1)` is **vacuous on residual charts**, because
  `kappa = k - |common core| = k = Theta(n)` once common factors are removed
  (K2, matching the paper's own L892--893 wording). The remark's residual open
  statement should be narrowed to the **decomposition/atlas (A2)** claim (or the
  (A4) coverage of large-mass charts); the per-chart half is not a viable route
  for `kappa = o(n/log n)`.
- **Next action:** state the `kappa = k - |C|` identity as a lemma; add the
  observation that (A6) for residual balanced cores must be discharged by (A2)
  or (A4), never by PR #528 alone. Re-derive (K2) and the census concentration
  at PI review.

### L-KG-2 (the moving-dimension / kernel-dimension decoupling)
- **Source:** this lane.
- **Status:** `AUDIT` (gated finding).
- **Paper impact:** Note near the balanced-core definition (L4526) that the
  defining parameter `d_proj` ("projective dimension > 1") and the secant kernel
  `kappa` are **independent**; "higher-dimensional" (large `d_proj`) does not
  imply small `kappa`. This prevents a reader from assuming the secant bound is
  usable merely because `d_proj` is a fixed small number.
- **Next action:** add one sentence distinguishing the two dimensions; cite the
  census (both `d_proj < kappa` and `d_proj > kappa` occur).

---

## 6. Files, per-claim labels, credit, exact-vs-heuristic

- Note: `experimental/notes/thresholds/balanced_core_kappa_growth.md` (this).
- Verifier: `experimental/scripts/verify_kappa_growth.py`
  (`RESULT: PASS (95 checks)`; group A secant-constant growth, B MDS identity
  (K1), C exact census + (K1)=(K2) + independence + concentration, D explicit
  PTM residual family, E direct transverse-count grounding).
- Read-only inputs: `experimental/asymptotic_rs_mca_frontiers.tex@4e3c4ee`
  (labels/lines cited inline); PR #528 note
  `experimental/notes/thresholds/ray_compiler_balanced_core.md`
  (`thresholds-ray-compiler-balanced-core`).

**Per-claim status.** (K1),(K2) = `PROVED`/`EXTRACTED` (exact, gated over all
census classes). `d_proj` vs `kappa` independence = `EXTRACTED` (gated).
Refutation 2.1 + explicit family 2.2 = `REFUTED`/`COUNTEREXAMPLE` (exact).
Robustness 2.3 = `AUDIT` (argued; the `C=empty` inputs are exact). Census 3 =
`COMPUTED` (exhaustive, exact). Wall 4 = `WALL` (cheap routes checked). Ledger
entries = proposed, not applied.

**Credit.** PR #528 proved the per-chart bound and isolated residual (1) as the
open kappa-growth wall; this lane resolves that wall negatively for the
per-chart route and hands the content to (A2)/(A4). The kappa-vs-core identity
(K2) is the quantitative form of the paper's own L892--893 sentence.

**Exact vs heuristic.** All arithmetic is exact prime-field Gaussian elimination
(no floats, no sampling) in the gated identities, the census, and the explicit
family. Group E samples received lines (labelled `UNGATED`) and only grounds the
secant **direction**; sharpness is PR #528's result, not re-claimed here. The
asymptotic reading `C(R+k,k+1) = e^{Theta(n)}` is the elementary Stirling bound
on the printed table, flagged for the PI as the single non-finite step.

**Flagged for PI re-derivation:** (a) the identity `kappa = k - |C|` (K2) and its
match to L892--893; (b) the claim that the removal pipeline cannot lower `kappa`
on large-mass residual charts (2.3); (c) whether (A4) Sidon/Fourier provably
covers exactly the `kappa = Theta(n)` large-family charts --- the honest residual.
