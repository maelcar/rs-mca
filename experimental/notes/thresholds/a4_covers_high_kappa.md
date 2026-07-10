# Does (A4) cover the high-kappa balanced cores? Coverage is kappa-independent

**Lane:** the wall named by PR #534
(`thresholds-balanced-core-kappa-growth`, note
`experimental/notes/thresholds/balanced_core_kappa_growth.md`): *prove or refute
that every residual balanced-core chart with `kappa = Theta(n)` is paid by the
prefix-flatness/Sidon route* `(A4)`.  This is a **coverage / routing** question
about the active draft, **not** an attack on the `(MI)`/`(MA)` inequalities or
the entropy-inverse crux (that is the scottdhughes program #498/#501/#505,
consumed here as an input).
**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (worktree base
`4e3c4ee`).  **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_a4_coverage.py` (stdlib-only,
zero-arg, `RESULT: PASS (63 checks)`, ~1.4 s under `ulimit -v 2097152`;
recomputes every gated number with exact prime-field arithmetic).

**Highest rung reached: 5 (all rungs traversed).**
**Verdict: `PROVED` (coverage, shallow-prefix) + `WALL` (deep-prefix) --- the
#534 named wall is a `ROUTING` gap, NOT a coverage gap; NO `COUNTEREXAMPLE`.**

One-line headline: **the `(A4)` Sidon/Fourier payment is independent of the
residual kernel dimension `kappa`; every shallow-prefix (`(a-k-1)\log|B|=o(n)`)
balanced-core chart --- including all of #534's census and the PTM family, all
with `kappa=k=Theta(n)` --- is paid unconditionally through the closure theorem
`thm:small-effective-dual-closure`, and the deep-prefix residual reduces to
`(MI)`/`(MA)` on the *ambient full slice*, a character-sum condition that again
never mentions `kappa`.**

Credit: builds directly on **PR #534** (reuses its exact prefix/kernel
primitives, its `(K1)=(K2)` identity `kappa=k-|C|`, and its PTM family
`disjoint_equal_prefix_pair`) and **PR #528** (`(RC)` per-chart secant bound,
consumed).  **LegaSage #531** (`pr-531-legasage`) isolates the *residual Sidon
statement* `MISSING_B` as an `OPEN GAP` audit --- theirs pins the missing
analytic payment; **this lane is the complementary coverage/routing result** and
finds that *coverage* is not the obstacle (the payment, once true on the ambient
slice, reaches the high-`kappa` residual `kappa`-freely).  Consumes the
scottdhughes `(MI)`/`(MA)` inequalities and `prop:high-energy-impossible` as
inputs.

---

## 1. Anatomy (rung 1) --- exact extraction, gated

### 1.1 What `(A4)` requires of a chart (exact text, `def:admissible-sequence` item 4)

`(A4)` (`def:admissible-sequence`, L895; item 4 at **L924--934**) requires, on
**every primitive prefix leaf**:

1. Fourier inversion is **normalized on the effective span**
   `V_g = span_{F_p}{g(t)-g(t_0):t in T}` of `lem:effective-span-fourier`
   (L2868; `EF1` L2860), with `A_eff = |V_g|`.  Here `g(t)` is the (weighted)
   Vandermonde column `(rho_0(t),rho_1(t)t,...,rho_{R-1}(t)t^{R-1})` and
   `Psi(S)=sum_{t in S}g(t)` is the fixed-weight boundary map (`sec:fourier`
   L5187--5193).
2. The leaf carries a **certified effective major/minor partition**
   `hat V_g\{1} = m_eff ⊔ M_eff` (`def:effective-major-minor` L2911).
3. **`(MI)` + `(MA)` hold** on that partition, *or* the leaf has a **separately
   proved image-normalized Sidon/Fourier moment payment** of the strength in
   `def:sidon-paid-cell` (L5130).  `(PF)` is *only a sufficient certificate* for
   `(MI)` in the range where its numerical inequality holds (`rem:pf-numerical`
   L6611: `|B|^R C(Lambda+m-1,m) <= e^{o(N)} C(N,m)`).

The two payment inequalities (consumed as inputs, not attacked):

- **`(MA)`** `def:major-arc-aggregate` (L2985):
  `sum_{chi in M_*} |e_m(chi(h(t)):t in T)| <= e^{o(|T|)} C(|T|,m)`.
- **`(MI)`** `def:aggregate-minor-payment` (L3081):
  `sum_{chi in m_eff} |e_m(chi(g(t)-g(t_0)):t in T)| <= e^{o(|T|)} C(|T|,m)`.

When both hold, `prop:effective-mi-ma-flatness` (L3097) gives the flat max-fiber
bound `(EF5)` (L3107):
`max_z |{S:Psi(S)=z}| <= e^{o(|T|)} C(|T|,m)/A_eff`, on the full slice **and
every first-match residual**.

### 1.2 The exact payment criterion --- three computable handles, all `kappa`-free

The `(A4)` payment is decided on **three axes, none of which is `kappa`**:

- **(H1) Prefix-span entropy `A_eff`.** `thm:small-effective-dual-closure`
  (L3026): if `log A_eff = o(|T|)` then effective `(MI)`, effective `(MA)`,
  image-normalized Q, **and the direct alternative in `(RC)`** all hold with
  subexponential loss.  Concrete sufficient form (L3057--3060): for a locator
  prefix with `|T|=Theta(n)`, `(a-k-1)\log|B| = o(n)`, because
  `A_eff <= |B|^{a-k-1}`.  `A_eff` is a function of the **prefix depth `w=a-k-1`
  and base field `B`**, not of the error-support union `U` or its kernel.
- **(H2) Additive energy `Delta_s`** (`def:sidon-heavy` L5093):
  `Delta_s = E(F_s)/f_s^3` on the incidence vectors of the fiber `F_s`.  Low
  energy (`Delta_s <= e^{-sigma N}`) is the Sidon branch, paid by
  `def:sidon-paid-cell`; high energy (`Delta_s=e^{-o(N)}`) is killed by the
  inverse theorem `prop:high-energy-impossible` (L5537, hughes).  `Delta_s` is a
  property of the **support geometry inside the fiber**, not of `kappa`.
- **(H3) `(MI)`/`(MA)` character sums** --- functions of the support/phase
  geometry `chi(g(t)-g(t_0))`, again not of `kappa`.

### 1.3 Where the high-`kappa` balanced cores are routed (the routing map)

Balanced-core charts are governed by **`(A6)`** (`def:admissible-sequence` item
6, **L942--945**), *not* by `(A4)` in the first instance:

> `(A6)` "Every residual shift-pair and **balanced-core chart** satisfies the
> ray compiler `(RC)`..., **or has a direct distinct-slope bound** at most its
> contribution to `e^{o(n)} E_n(a_n)`."

The proof of the conditional compiler `thm:main-smooth-circle` (L956; proof
**L966--977**) routes the payment in two stages:

- `(A4)` "supplies the certified Sidon/Fourier payment" on **every remaining
  primitive profile** (the fiber/max-fiber bound);
- `(A6)` + `prop:q-implies-sp` "convert those bounds to distinct slopes."

So a balanced-core chart is paid by **`(A4)` [fiber bound] then `(A6)` [convert
to slopes]**.  The `(A6)` escape "**or has a direct distinct-slope bound**" is
supplied *verbatim* by the closure theorem's `(SE2)` (L3049): `|Z| <= L*Nbar =
M`, which holds with subexponential loss exactly when `log A_eff = o(|T|)`.  PR
#534 showed the *other* `(A6)` route --- the `(RC)` per-chart secant constant
`C(R+kappa,kappa+1)` of PR #528 --- is **vacuous** at `kappa=Theta(n)`; the
closure/`(A4)` route is the one that survives, and it is `kappa`-free.

### 1.4 The FIBER = CHART identity (the hinge of the whole question)

`lem:effective-span-fourier` `(EF2)` counts `N_g(z) = |{S in C(T,m):
Psi(S)=z}|` --- the size of the **syndrome fiber** over `z`.  A fiber
`F_s = Psi^{-1}(s)` is exactly a **depth-`w` prefix class**, i.e. **#534's
balanced-core chart members**.  Hence:

- `f_s = |F_s|` = the chart's **member count** (#534's "class size");
- the **largest fiber** is the empty-common-core chart, which #534 proved has
  the **maximal kernel `kappa = k`** (`C.largest_bc_kappa`).

Therefore the `(A4)` **max-fiber bound is literally a bound on the highest-`kappa`
chart**, and `lem:residual-monotonicity` (L6574) transfers any full-slice
max-fiber bound *down* to every sub-family.  [Gated `B.fiber_is_chart.*`,
`B.largest_fiber_kappa_k.*`; `B.kappa_two_ways.*` reproduces #534's `(K1)=(K2)`.]

---

## 2. Coverage proof (rung 2) --- `PROVED` for shallow prefix, `kappa`-independent

**Claim (coverage, `kappa`-independence).** The `(A4)` payment criteria (H1)-(H3)
make no reference to `kappa = k - |C|`.  In particular:

**(C-a) `A_eff` is a slice invariant, orthogonal to `kappa`.**  `A_eff = |V_g| =
p^{dim span{g(t)-g(t_0)}}` depends only on the prefix map on the active set `T`,
not on the error-support union `U`.  Every chart (fiber) in one profile slice
shares the *same* `A_eff`, while its member count `f_s` and its kernel `kappa`
range freely.  [Gated `C.A_is_slice_property.*`: on each config `A_eff = p^{dim}`
with `dim<=w`, shared by all fibers, `f_s in [f_min..f_max]`, `kappa_max=k`;
`E.A_orthogonal_to_kappa`: sweeping `w=1,2,3` moves `dim(V)=1,2,3` while
`kappa_max` stays `>= k-1` (near-maximal) --- the two axes are orthogonal.]

**(C-b) The closure theorem discharges the chart `kappa`-freely when the prefix
is shallow.**  If `log A_eff = o(|T|)` --- concretely `(a-k-1)\log|B| = o(n)` ---
then `thm:small-effective-dual-closure` gives effective `(MI)`, `(MA)`,
image-normalized Q, **and the direct `(RC)`/`(A6)` alternative `(SE2)`** with
subexponential loss, *regardless of `kappa`*.  Combined with
`lem:residual-monotonicity` (full-slice payment transfers to every residual),
**every balanced-core chart with `(a-k-1)\log|B| = o(n)` is paid --- through both
`(A4)` and `(A6)` --- for any `kappa`, including `kappa = k = Theta(n)`.**  This
is UNCONDITIONAL (`thm:small-effective-dual-closure` is a proved theorem of the
draft).  [Gated `A.closure_bound.*`, `A.exponent_le_wbound.*`,
`C.closure_met_all_kappa.*`, `F.*` monotonicity transfer.]

**Verdict rung 2: `PROVED` (coverage) for the shallow-prefix regime** ---
which is exactly the regime of #534's entire census **and** the PTM family (all
`w=2` fixed).  The #534 wall ("*no proof that (A4) covers the `kappa=Theta(n)`
charts*") is **closed** for these charts: `(A4)` coverage of a high-`kappa` chart
is not gated on `kappa` at all; it is gated on the ambient slice's prefix-span
entropy `log A_eff`, which residual monotonicity carries down to the residual.

---

## 3. PTM stress test (rung 3) --- `PAID`, no counterexample

The task's suggested stress case: the Prouhet-Thue-Morse family
`disjoint_equal_prefix_pair` (#534) is additively *very* structured (equal power
sums by Prouhet's theorem) and has `kappa = k = Theta(n)`.  Exact numbers
[gated `D.*`]:

| n | a | k | kappa | closure exp `w\log p/n` | (DEAD secant) `log2 C/n` | PTM-pair `Delta` |
|---:|---:|---:|---:|---:|---:|---:|
| 16 | 8 | 5 | **5=k** | 0.392 | 0.810 | 0.750 |
| 32 | 16 | 13 | **13=k** | 0.235 | 0.900 | 0.750 |
| 64 | 32 | 29 | **29=k** | 0.137 | 0.945 | 0.750 |
| 128 | 64 | 61 | **61=k** | 0.077 | 0.969 | 0.750 |

The prefix is **shallow** (`w=2` fixed, `w\log p/n -> 0`), so
`log A_eff <= w\log p = o(|T|)` and the chart is **`PAID` by the closure
theorem, `kappa`-independently**, while the PR #528/#534 per-chart secant route
is simultaneously **vacuous** (`log2 C(R+kappa,kappa+1)/n -> ~1`).  [Gated
`D.shallow_prefix.*`, `D.ptm_paid_by_closure_not_secant`.]

**Refutation NOT achieved: the PTM family is covered.**  A genuine
`COUNTEREXAMPLE` would need a *deep-prefix* (`w\log|B|=Theta(n)`), low-energy,
large fiber where `(PF)`/`(MA)` fails --- and that is a `(PF)`/`(MA)` failure
(hughes's territory), **not** a `kappa`/coverage failure.

---

## 4. Census (rung 4) --- joint `(A_eff, f_s, kappa, Delta_s)` distribution

Exhaustive on #534's four configs.  For each profile slice, `A_eff = p^{dim}`
is one number; the fibers range in size and in kernel:

| p | n | k | slice `A_eff` | `log A_eff/|T|` | `kappa` range (max) | largest fiber `f_s`, `kappa`, `Delta_s` |
|---:|---:|---:|:---:|---:|:---:|:---|
| 13 | 12 | 5 | p^2 | 0.427 | [0..5] (=k) | 5, **5=k**, 0.360 |
| 17 | 14 | 6 | p^2 | 0.405 | [2..6] (=k) | 11, **6=k**, 0.174 |
| 17 | 16 | 7 | p^2 | 0.354 | [7..7] (=k) | 32, **7=k**, 0.062 |
| 19 | 18 | 8 | p^2 | 0.327 | [8..8] (=k) | 95, **8=k**, 0.024 |

**Decisive readings.**
1. `A_eff` (the closure/coverage axis) is **constant across each slice** and its
   exponent `log A_eff/|T|` **decreases with `n`** (0.427 -> 0.327): coverage
   gets *stronger* at scale, opposite to the `kappa=k` concentration #534 found.
   [Gated `C.coverage_strengthens_with_n`.]
2. The `kappa=k` (largest-member) fibers are **low-energy / Sidon-like**:
   `Delta_s = 0.360, 0.174, 0.062, 0.024` --- **strictly decreasing, `~1/f_s ->
   0`.**  So the high-`kappa` charts sit in the **Sidon branch** of
   `def:sidon-heavy`, *not* the high-energy inverse branch: they are precisely
   the charts that need the `(A4)` Sidon/Fourier payment (or, shallow-prefix, the
   closure bound), and are **not** dispatched by `prop:high-energy-impossible`.
   [Gated `C.kappa_k_fiber_is_sidon_low_energy` --- this is the sharpest census
   finding and the one that most directly answers the task's "Sidon-heavy,
   low-energy, high-kappa" worry: yes, the high-`kappa` charts are Sidon-heavy
   candidates, but they are shallow-prefix and hence closure-paid, so **not** a
   gap.]

**Joint distribution summary.** `kappa` and the `(A4)` axes `(A_eff, Delta_s)`
are **statistically decoupled**: `A_eff` is pinned by the slice (`p^w`), `Delta_s`
falls with fiber size, and `kappa` concentrates at `k`.  The payability of a
chart is decided by `(A_eff, Delta_s, MI/MA)`, all of which are compatible with
`kappa = k`.

---

## 5. The wall (rung 5) --- the honest deep-prefix residual, cheap routes dead

**Named wall.**  The closure route (H1) pays only when
`log A_eff = o(|T|)`, i.e. `(a-k-1)\log|B| = o(n)` (**shallow prefix**).  A
balanced-core chart with **deep prefix** `w\log|B| = Theta(n)` has `A_eff` up to
`|B|^{Theta(n)}`; the trivial closure multiplier is then exponential, and its
payment **reduces to genuine `(MI)`/`(MA)` cancellation on the ambient full
slice** (`prop:smooth-circle-prefix-flatness-criterion` L6593 +
`lem:residual-monotonicity`).  That reduction is the scottdhughes
`(MI)`/`(MA)`/entropy-inverse crux and is **out of scope** here --- but note the
key point: **even the deep-prefix payment is a character-sum / additive-energy
condition on the ambient slice, never a condition on `kappa`.**  In every
regime, *coverage of the high-`kappa` residual is `kappa`-free*; what can fail is
the *ambient* `(PF)`/`(MA)`, not the transfer to the residual.  [Gated
`E.deep_prefix_wall_named`: `w=300, p=1009, n=1000` gives `w\log p/n = 2.07`, not
`o(1)` --- closure fails there and `(MI)`/`(MA)` is needed.]

**Cheap routes checked dead.**
- *"`kappa` forces large `A_eff`":* **FALSE** --- `A_eff` is a slice invariant;
  fibers of every `kappa in [0..k]` share the same `A_eff` (`C.A_is_slice_property`,
  `E.A_orthogonal_to_kappa`).  `[DEAD, gated.]`
- *"the high-`kappa` fiber is high-energy, so the inverse theorem (not `(A4)`)
  must pay it":* **FALSE** --- measured `Delta_s -> 0`, the high-`kappa` fibers
  are Sidon-like (`C.kappa_k_fiber_is_sidon_low_energy`).  They need the `(A4)`
  Sidon cell, which closure supplies when shallow.  `[DEAD, measured.]`
- *"the PTM family is a counterexample":* **FALSE** --- shallow prefix, closure
  pays it (`D.*`).  `[DEAD, exact.]`
- *"per-chart secant `(RC)` can reach them":* **FALSE** --- PR #534, vacuous at
  `kappa=Theta(n)`; the surviving `(A6)` alternative is closure `(SE2)`.
  `[DEAD, cited to #534.]`
- *"residual monotonicity might not transfer to a high-`kappa` sub-family":*
  **FALSE** --- it is a set inclusion, holds for every residual regardless of
  `kappa` (`F.*`).  `[DEAD, gated.]`

---

## 6. Routing-gap finding (echoes our #524 visible-hypothesis result)

The paper contains every ingredient (`thm:small-effective-dual-closure`,
`lem:residual-monotonicity`, `(A6)`'s direct-bound alternative) but **never
visibly states** that they discharge the balanced-core payment
`kappa`-independently.  A reader who takes `(A6)`/`(RC)` (the PR #528 secant
route) as *the* balanced-core route --- as its placement in `(A6)` invites ---
concludes with #534 that residual charts are unpaid, missing that closure's
`(SE2)` direct alternative + residual monotonicity cover them at any `kappa`.
This is a **`ROUTING` gap** (unstated inference), not a mathematical gap, exactly
the class flagged in our #524 delta-audit.  The fix is one cross-reference
(ledger entry L-A4-1).

A second, cosmetic hazard: the draft **overloads `kappa`**.  In
`def:effective-fourier-payment` (L2929) and `(EF5)` region, `kappa >= 1` is the
*effective-Fourier payment constant* (a multiplicative loss); in PR #528/#534
(and this note) `kappa = dim ker H_U` is the *transverse-secant kernel
dimension*.  These are unrelated.  Worth a one-line disambiguation
(ledger entry L-A4-2), consistent with the #515 barrier-map "namespace
conflation" guard.

---

## 7. Proposed ledger entries (proposed; NOT applied to `.tex`/`.pdf`)

Format per `experimental/asymptotic_rs_mca.md` (Source / Status / Paper impact /
Next action).

### L-A4-1 (route the balanced-core payment through closure + residual monotonicity, `kappa`-independently)
- **Source:** this lane; `verify_a4_coverage.py`.  Builds on PR #534 (kappa=k on
  residuals) and PR #528 (per-chart secant).
- **Status:** `PROVED` (coverage, shallow-prefix) / `WALL` (deep-prefix) /
  `AUDIT` (routing).
- **Paper impact:** In `(A6)` (`def:admissible-sequence` item 6, L942--945) and
  in the proof of `thm:main-smooth-circle` (L966--977), record that the
  balanced-core "direct distinct-slope bound" alternative is supplied by
  `thm:small-effective-dual-closure` `(SE2)` under `(a-k-1)\log|B| = o(n)`,
  **independent of the kernel dimension `kappa`**, and transferred to first-match
  residuals by `lem:residual-monotonicity`.  State explicitly that the PR
  #528/#534 secant route `C(R+kappa,kappa+1)` is vacuous at `kappa=Theta(n)` and
  is *not* the balanced-core mechanism; the closure/`(A4)` route is.  Add the
  one-line consequence: *coverage of high-`kappa` balanced cores by `(A4)` is
  `kappa`-free; only the ambient-slice `(PF)`/`(MA)` can obstruct payment, and
  that obstruction is a character-sum condition, never a `kappa` condition.*
- **Next action:** insert the cross-reference `(A6) -> (SE2) + residual
  monotonicity`; re-derive `(SE2)` and the `A_eff \perp kappa` orthogonality
  at PI review.  Deep-prefix `(PF)`/`(MA)` remains the hughes crux (unchanged).

### L-A4-2 (disambiguate the two `kappa`'s)
- **Source:** this lane.
- **Status:** `AUDIT` (wording).
- **Paper impact:** Near `def:effective-fourier-payment` (L2929), rename or
  footnote the effective-Fourier payment constant (currently `kappa >= 1`) so it
  is not confused with the transverse-secant kernel dimension `kappa = dim ker
  H_U` used in the ray-compiler line (PR #528/#534).  Prevents a reader from
  conflating a payment *multiplier* with a kernel *dimension*.
- **Next action:** one-line notation note; no proof change.

---

## 8. Files, per-claim labels, credit, exact-vs-heuristic

- Note: `experimental/notes/thresholds/a4_covers_high_kappa.md` (this).
- Verifier: `experimental/scripts/verify_a4_coverage.py`
  (`RESULT: PASS (63 checks)`; group A `A_eff`/closure-bound, B fiber=chart +
  `(K1)=(K2)`, C `kappa`-independence census + Sidon-energy finding, D PTM stress
  test, E `w`-sweep orthogonality + deep-prefix wall, F residual-monotonicity
  transfer).
- Read-only inputs: `experimental/asymptotic_rs_mca_frontiers.tex@4e3c4ee`
  (labels/lines cited inline and re-verified); PR #534 note + verifier
  (`thresholds-balanced-core-kappa-growth`); PR #528 note
  (`thresholds-ray-compiler-balanced-core`); LegaSage #531
  (`pr-531-legasage`, `sidon_residual_input.md`).

**Per-claim status.**
- Anatomy 1.1--1.4 (the `(A4)` criterion, the routing, the fiber=chart identity):
  `EXTRACTED` (exact, gated against the cited lines).
- Coverage (C-a) `A_eff \perp kappa`: `PROVED`/`COMPUTED` (exact, gated).
- Coverage (C-b) shallow-prefix charts paid `kappa`-freely: `PROVED`
  (unconditional; rests on the draft's own `thm:small-effective-dual-closure` +
  `lem:residual-monotonicity`, consumed as proved).
- PTM test (rung 3): `PAID` / no `COUNTEREXAMPLE` (exact).
- Census (rung 4): `COMPUTED` (exhaustive, exact); the `Delta_s -> 0` Sidon
  finding is `MEASURED` (exact on the four configs).
- Wall (rung 5): `WALL` (deep-prefix reduces to `(MI)`/`(MA)`, cheap routes
  checked dead).
- Routing/notation findings (sec 6): `AUDIT`.
- Ledger entries: proposed, not applied.

**Exact vs heuristic.**  All arithmetic is exact prime-field Gaussian
elimination and integer additive-energy counting (no floats, no sampling) in the
gated identities, the census, the PTM family, and the monotonicity transfer.
The two *asymptotic readings* are the single non-finite steps, flagged for PI:
(i) `log A_eff <= (a-k-1)\log|B| = o(n)` on shallow prefixes is the elementary
bound `A_eff <= |B|^{a-k-1}` (from `thm:small-effective-dual-closure` L3059);
(ii) `Delta_s -> 0` is read off the strictly-decreasing finite table, not proved
asymptotically.  Group F uses a fixed-seed random *residual carving* to exhibit
monotonicity, labelled as a demonstration of a set inclusion (the inclusion
itself is exact and holds for every sub-family).

**Flagged for PI re-derivation:**
(a) the identification *fiber `F_s` = depth-`w` prefix class = #534 balanced-core
chart* (`EF2` vs `def:profile-cell`), and *largest fiber has `kappa=k`*;
(b) that `thm:small-effective-dual-closure` `(SE2)` really supplies the `(A6)`
"direct distinct-slope bound" alternative (the closure-to-`(A6)` bridge);
(c) the `kappa`-independence of `A_eff`, `Delta_s`, and the `(MI)`/`(MA)`
character sums (the core coverage claim);
(d) that the deep-prefix reduction to `(PF)`/`(MA)` is faithful and does not
smuggle in a hidden `kappa` dependence.

**Credit.**  PR #534 proved `kappa=k=Theta(n)` on residuals and named this exact
wall; PR #528 proved the per-chart secant bound and isolated residual (1).
LegaSage #531 isolates the residual Sidon *payment* statement as `OPEN GAP`;
this lane answers the complementary *coverage/routing* question --- the payment,
once true on the ambient slice, reaches the high-`kappa` residual
`kappa`-freely, and is unconditional on shallow prefixes.  The `(MI)`/`(MA)`
inequalities and `prop:high-energy-impossible` are the scottdhughes program,
consumed here, not attacked.
