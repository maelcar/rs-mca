# Attack the exhaustiveness of the witness-exhaustive first-match atlas

**Lane:** hard input 1 (agents.md) --- the **witness-exhaustive first-match
atlas**, condition `(A2)`.  Delta-audit PR #524 verdict on this input: **OPEN
GAP** ("named in `(A2)`, visible in every consumer, falsifiable; unconditional
discharge only when one cell is `binom(D,a)`").  Maintainer's named failure
mode: *"missing witness in the first-match atlas"*.

**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (worktree base
`4e3c4ee`).  **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_atlas_witness.py` (stdlib-only,
zero-arg, `RESULT: PASS (61 checks)`, ~3.3 s under `ulimit -v 2097152`;
recomputes every gated number with exact prime-field arithmetic).

**Highest rung reached: 3 (PROVE) --- all five rungs traversed.**

**Verdict: `PROVED` (unconditional exhaustiveness discharge, strictly wider than
`binom(D,a)`) + `WALL` (the residual missing-witness risk is a *payment* gap,
not a coverage gap).  Falsifier `NULL` (no missing witness, no large-high-energy
fiber) --- labelled EVIDENCE + SCOPE, not an asymptotic discharge.  NO
`COUNTEREXAMPLE`.**

**One-line headline:** *Exhaustiveness DECOUPLES from payment: the depth-`w`
prefix-fiber family `Phi_w^{-1}(z)` is a total map's fibre partition, hence an
**unconditionally** witness-exhaustive first-match atlas --- with subexponential
profile count and no `(A2)` assumption and NOT subject to the `lem:profile-atlas`
planted/higher-dim exclusion guard --- so the maintainer's "missing witness"
cannot be a set-cover fall-through; the real content of the assumed `(A2)`
exhaustiveness is that a **finer, better-paying** algebraic atlas covers the
mass, and there the only genuine missing-witness is a **mis-paid** primitive
prefix fibre (a positive-rate Sidon-heavy obstruction with failing Sidon
payment), which is input 4/5, out of scope to attack.*

**Credit:** reuses the exact census primitives of **PR #534/#535**
(`thresholds-a4-covers-high-kappa` / `thresholds-balanced-core-kappa-growth`):
`prefix_key`, `span_dim_from_prefixes`, `additive_energy`, the fibre=chart
identity, and the shallow-prefix closure `(a-k-1)log|B|=o(n)`.  **Scope vs
LegaSage #519/#526** (`pr-519/526-legasage`): those AUDIT the first-match
FORMALISM (least-index partition + budget summation are mechanically correct,
cells taken as given abstract slope-sets; both verdict NO ISSUE); **this** is an
executable EXHAUSTIVENESS falsifier over the ACTUAL constructible cells plus an
unconditional coverage discharge.  **#533** ships a Lean atlas partition
identity (different deliverable).  Consumes the scottdhughes `(MI)`/`(MA)` and
`prop:high-energy-impossible` (#498/#501/#505) as black-box inputs (not
attacked).

---

## 1. Anatomy (rung 1) --- exact extraction, gated

### 1.1 What is a witness; what is "missing"

`def:exact-witness-incidence` (eq. 2.1, **L1323--1334**): for a received line
`r=(r_0,r_1)` and agreement `a >= k+1`,
```
  W_a(r) = { (gamma, S, h) : gamma in F, S in binom(D,a), h in F[X]_{<k},
             ev_S(h) = (r_0 + gamma r_1)|_S,   NT_C(r;S) }
```
(`NT_C`: the pair is NOT simultaneously explained on `S`, `def:explanation`
L1286).  Slope projection `pi_gamma(gamma,S,h)=gamma`; bad-slope set
`Z_a(r)=pi_gamma(W_a(r))`.  `B_C^MCA(a)=max_r |Z_a(r)|`.

`def:first-match` (**L1452--1467**): an ordered family
`C_1,...,C_s subset W_a(r)` is a **witness-exhaustive first-match atlas** iff
`W_a(r)=union_i C_i`; first-match parts
`Z_i^o = Z_i \ union_{j<i} Z_j`, `C_i^o = C_i cap pi_gamma^{-1}(Z_i^o)`,
`Z_a(r)=coprod_i Z_i^o`.

**Formal meaning of "missing witness":** an exact-agreement witness
`(gamma,S,h) in W_a(r)` whose first-match routing (test `C_1,C_2,...` in order)
matches NO cell `C_i` --- equivalently `S` carries none of the catalogued
structural features and its slopes are never charged.  Then
`W_a(r) != union_i C_i` and `lem:first-match-bound` (L1526, the sole consumer)
does not apply.

### 1.2 The ordered cell list (with tex labels)

Catalogue `sec:cell-catalogue` (**L2366--2496**), in the paper's stated
first-match order (algebraic major arcs first, then Sidon, then high-energy
inverse; explicit at **L5180--5182**):

| # | cell (tex) | structural test | ref |
|---|---|---|---|
| C1 | quotient / periodic (L2374) | `S` a union of complete fibres of a nontrivial `pi:D->D'` | `lem:constructible-cells` |
| C2 | dihedral / Chebyshev (L2385) | `S` inversion-invariant, invariant coord `x=(u+u^{-1})/2`, Dickson `D_d` | `sec:smooth-circle-domains` |
| C3 | planted-block (L2399) | `Q_S` divisible by an algebraically-forced factor `P`, roots in `D` | census input |
| C4 | tangent / deep / common-line (L2409) | rank-defective slope-projection contact | `prop:tangent-payment` |
| C5 | extension / field-descent (L2422) | data over a proper subfield (Frobenius-fixed) | `lem:constructible-cells` |
| C6 | differential-locator (L2429) | prefix-map Jacobian (Vandermonde/Hasse) rank loss | `prop:rank-pivot-payment` |
| C7 | saturation / effective-image-collapse (L2440) | many raw witnesses -> one slope; image << codomain | `def:explanation-occupancy` |
| C8 | balanced-core / split-pencil (L2456) | equal-degree residual locators, common depth-`w` prefix; split pencil `Q_0+lambda Q_1` | `prop:split-pencil-payment` |
| C9 | Fourier/Sidon-heavy analytic (L2476) | primitive prefix fibre, large but low additive energy | `def:sidon-heavy`, `def:sidon-paid-cell` |

`C9` splits (`prop:ordinary-moment-split` **L5108**) into **C9a low-energy**
(`Delta_s <= e^{-sigma N}` -> Sidon payment `def:sidon-paid-cell` L5130) and
**C9b high-energy** (`Delta_s > e^{-sigma N}` -> `prop:high-energy-impossible`).

### 1.3 Where the discharge is unconditional vs assumed

- **UNCONDITIONAL (proved):** the ONE-cell atlas `Omega=binom(D,a)`.
  `thm:small-effective-dual-closure` (**SE1/SE2, L3026--3079**): "Taking the
  support-restricted incidence over `Omega` as one ordered cell is exhaustive
  for that restricted incidence; it is exhaustive for the whole exact-agreement
  incidence **when `Omega=binom(D,a)`**."  This is the *only* unconditional
  discharge PR #524 found, and it pays only at identity scale
  (`(a-k-1)log|B|=o(n)`, i.e. `A<=|B|^{a-k-1}`, L3057--3060).
- **ASSUMED (input `(A2)`):** any FINER atlas.  `def:admissible-sequence` item
  `(A2)` (**L905--911**): "A first-match atlas **covers every bad-slope
  witness** and has `e^{o(n)}` profiles."  `prop:first-match-atlas-finite`
  (**L6516--6531**) proves only the COUNT from an *assumed* exhaustive atlas and
  states outright: "**The proposition deliberately does not derive
  exhaustiveness from smoothness.**"  `thm:main-smooth-circle` proof (L967)
  opens "Condition `(A2)` **supplies** a witness-exhaustive first-match atlas".

### 1.4 The `lem:profile-atlas` guard flagged in #524 --- what "excludes" does

`lem:profile-atlas` (**L4772--4784**) asserts ONLY the COUNT: "the number of
first-match profiles is `e^{o(n)}`."  Its proof: "This is condition `(A2)`. ...
The statement **does not include arbitrary planted subsets or an unproved
decomposition of a higher-dimensional pencil; including either could create
exponentially many profiles**."  (`rem:balanced-core-exhaustion` L4762 repeats
this for C8.)

**What "excludes" does to the claim (pinned):** the subexponential-count
guarantee is *void* if the atlas needs C3-arbitrary-planted or C8-higher-dim
cells to be exhaustive.  This is a genuine **tension**, not a harmless
footnote: exhaustiveness may *require* exactly the cells the count-bound
forbids.  So the assumed `(A2)` bundles two claims that pull against each other
--- (i) COVER every witness (`def:first-match`) and (ii) with `e^{o(n)}`
profiles (`lem:profile-atlas`).  The maintainer's "missing witness" is the
failure of (i) *within the count-admissible cells*: a witness whose only
structural home is an excluded planted/higher-dim cell.

---

## 2. The discharge (rung 3, PROVED) --- exhaustiveness decouples from payment

> **Lemma (prefix-fibre atlas is unconditionally witness-exhaustive).**  Fix a
> row `C=RS_F(D,k)`, agreement `a`, depth `w=a-k-1`.  The boundary map
> `Phi_w : binom(D,a) -> B^w`, `Phi_w(S)=(q_1(S),...,q_w(S))`, is a **total
> function**.  Order its nonempty fibres `C_1,...,C_L`, `L=|im Phi_w|`.  Then:
>
> 1. **(Exhaustive, unconditional)** `union_i C_i = binom(D,a) ⊇ pi_S(W_a(r))`
>    for every received line `r`, so `W_a(r)=coprod_i (W_a(r) cap Phi_w^{-1}(z_i))`
>    is a first-match partition (`def:first-match`) with **no `(A2)` assumption**.
>    *Proof:* fibres of a total function partition its domain; every witness
>    support is an `a`-subset. ∎
> 2. **(Subexponential count, no exclusion guard)** `L <= |im Phi_w| <=
>    min(binom(n,a), p^{dim}) <= p^w`; when `(a-k-1)log|B|=o(n)`, `L=e^{o(n)}`.
>    Because the cells are prefix fibres (NOT planted subsets or higher-dim
>    pencils), the `lem:profile-atlas` exclusion clause **does not bind**.
> 3. **(Paid, shallow prefix)** by `thm:small-effective-dual-closure` with
>    effective span `A_eff=p^{dim}<=p^w`, each fibre is paid at effective-image
>    scale, `|Z_i^o| <= e^{o(n)}(1+barN_i)`, whenever `log A_eff = o(n)`.

The one-cell `binom(D,a)` discharge is the `w=0` (empty-prefix) special case;
this Lemma extends it to the **entire shallow-prefix regime** and, unlike the
finer algebraic atlas, needs no planted/higher-dim cells at all.  **Newton
dictionary** (`lem:newton-dictionary-expanded` L6472, gated
`P.newton_dictionary.*`): for `char>w` the elementary prefix `(q_1..q_w)` and
power sums `(p_1..p_w)` are triangularly equivalent, so the prefix-fibre atlas
**equals** the syndrome-line (power-sum) atlas --- the "support side" and
"syndrome-line side" of the falsifier coincide.

**Consequence (the reframing).**  The maintainer's "missing witness in the
first-match atlas" **cannot** be realised as a set-theoretic fall-through: the
prefix-fibre atlas (and, within a fibre, the numeric energy dichotomy
`Delta_s <= / > e^{-sigma N}`) is a *total partition*.  Coverage is FREE.  What
the assumed `(A2)` actually buys is a **finer, better-paying** atlas (quotient /
Chebyshev / planted / balanced-core cells that beat the effective-image scale);
its exhaustiveness is a real assumption only because the finer partition need
NOT be total, and its non-algebraic residual must be Sidon-payable.

---

## 3. Falsifier (rung 2) + census (rung 4) --- decisive toy null

**Design (informative-null by construction).**  Enumerate EVERY `a`-subset of
`D` (= every exact-agreement witness support; one support carries `<=1` slope
per line by `lem:slope-multiplicity-fixed-support` L6533 / `prop:exact-support-
upper` L1360, so the support side is the complete falsifier surface).  Route
each through the CONSTRUCTIBLE algebraic cells in catalogue order:

- **C1 quotient** = `S` a union of full multiplicative-subgroup cosets;
- **C2 Chebyshev** = `S` inversion-closed (`S=S^{-1}`);
- **C3 planted** = `S` contains a full nontrivial subgroup-coset block;
- **C4/C5/C6 = VACUOUS at this scale, with reasons stated:** C4/C6
  (tangent/differential rank loss) is empty for a single distinct-point support
  (its Vandermonde has full rank); C5 (field-descent) is empty over the prime
  field `F_p` (no proper subfield) --- exercised SEPARATELY on `F_{p^2}`
  (`F.field_descent.nonvacuous.Fp2.*`, a subfield support descends, a mixed one
  does not);
- **C8 split-pencil** = `S` shares its depth-`w` prefix with another support and
  the fibre's next-coordinate span dim `<=1` (paid pencil); span dim `>=2` is
  the EXCLUDED higher-dim balanced core (`primitive_highdim_core`);
- else **primitive** -> energy dichotomy (C9).

**Routing order implemented (faithful to L5180):** C1 -> C2 -> C3 -> [C4,C5,C6
vacuous] -> C8 -> C9(energy).  **Parameters (stated so the null is informative):**

- **STRUCTURED** `D=F_p^*` (the task params `(13,12,5,7/8)`, `(17,16,7,10)`,
  `(19,18,8,11)`): here `a>n/2`, so a support must contain a full antipodal pair
  by **pigeonhole** --- the algebraic cells "exhaust" (primitive = 0.0%) as an
  **ARTIFACT**, not structural coverage.  Explicitly labelled.
- **GENERIC** `D=[1..n] subsetneq F_p^*` (`n<p-1`, `a<=n/2`, no pigeonhole
  forcing): `(13,9,4,6)`, `(17,11,4,7)`, `(19,12,4,7)`, `(23,14,5,8)`,
  `(29,18,6,10)` (`w` up to 3, `binom(18,10)=43758`).  This is the honest
  surface.

### 3.1 Falsifier outcome

- **Set-cover:** `F.no_missing_witness.*` PASS on every config --- every witness
  that falls through the constructible algebraic cells is independently
  re-checked to land in a real nonempty prefix fibre.  **0 missing witnesses.**
  (As the Lemma predicts.)
- **GENERIC routing mass (primitive + high-dim-core residual GROWS with scale):**

  | cfg | primitive+core | C3 planted | C8 split | C2 cheb |
  |---|---|---|---|---|
  | (13,9,4,6)  |  3.6% |  92.9% | -    | 1.2% |
  | (17,11,4,7) | 10.0% |  84.2% | 5.5% | 0.3% |
  | (19,12,4,7) | 11.9% |  82.6% | 5.1% | 0.5% |
  | (23,14,5,8) | **27.2%** | 72.3% | 0.4% | 0.2% |
  | (29,18,6,10)| 12.2% |  80.9% | 6.9% | 0.0% |

  The **excluded higher-dim balanced-core** class (`lem:profile-atlas` guard)
  alone carries up to **27.1%** of the mass at `(23,14,5,8)` --- a concrete,
  measurable instance of the guard tension: covering these needs exactly the
  cells the count-bound forbids.  The constructible PAID cells (C1,C2,C3,C8) do
  NOT exhaust; the residual is caught only by the prefix-fibre / analytic
  backstop.
- **The genuine missing-witness probe (energy dichotomy), decisive NULL:**
  `W.no_large_high_energy_fiber` PASS.  Across ALL configs the largest prefix
  fibres are **low-energy** (Sidon-side): `Delta = E/f^3 in [0.024, 0.066]` for
  `f in [32,95]`, with `Delta*f approx 2--3.3` (roughly constant -> `Delta ~
  C/f`, the Sidon-set signature, NOT the `Omega(1)` approximate-group signature).
  Every fibre with high `Delta` (0.36--0.56) is TINY (`f<=8`, small-set noise).
  `C.largest_fiber_low_energy.*` PASS where `f>=16`.  **No fibre is
  simultaneously large and approximate-group-like** --- the toy primitive mass
  sits squarely in the branch (C9a) the analytic Sidon cell is designed to pay.

**HONESTY.**  This null is **EVIDENCE + SCOPE**, not an asymptotic exhaustiveness
discharge.  It confirms (a) the total-partition coverage (Lemma), and (b) that
at toy scale the primitive residual is Sidon-side, consistent with `(A2)` being
completable via the analytic cell.  It does NOT prove the Sidon payment holds
asymptotically (that is input 4/5).

---

## 4. Wall (rung 5) --- the genuine missing-witness is a PAYMENT gap

> **Named statement (un-Sidon-payable primitive prefix fibre).**  A received-line
> sequence for which, after removing all constructible algebraic cells C1--C8,
> some primitive prefix leaf carries a *positive-rate Sidon-heavy obstruction*
> `Gsid_{q,sigma} >= e^{eta N q}` (`def:sidon-heavy` L5093) with no separately
> proved Sidon moment payment (`def:sidon-paid-cell` L5130).  For such a leaf the
> witness is **mis-paid, not missing**: (i) the prefix-fibre/`binom(D,a)` cell
> covers it but pays only at effective-image scale `barN >= e^{eta N}` (above the
> target envelope); (ii) the high-energy inverse branch does NOT reach it
> (`lem:no-go` L5155); (iii) no constructible cell contains it (primitive).

**Cheap routes that die (checked):**

- *"Just use `binom(D,a)`"* --- dies unless `(a-k-1)log|B|=o(n)`; `A_eff=p^{dim}`
  grows with prefix depth (gated `P.count.subexp.*`: `A_eff` reaches `p^3=24389`
  at `w=3`).  Deep prefix breaks *payment*, not coverage.
- *"The constructible algebraic cells are exhaustive"* --- dies: GENERIC census
  shows a primitive+core residual up to 27%, growing with scale.
- *"Force the large low-energy fibre into the high-energy inverse branch"* ---
  dies by `lem:no-go` (L5155): a Sidon-heavy fibre "cannot be forced into the
  high-energy inverse branch ... must be removed by a separate cell."
- *"Name the large low-energy fibre a cell"* --- dies: "Naming a large low-energy
  fibre a cell does not pay it" (L5183).

The wall is therefore **input 4/5** (the analytic Sidon/`(MI)`/`(MA)` payment),
explicitly out of scope to attack.  The exhaustiveness question *itself* is
discharged by the Lemma of Section 2.

---

## 5. Proposed paper changes (ledger entries; NO tex/pdf edits)

Convention per `experimental/asymptotic_rs_mca.md`.  Two proposed entries:

### Entry A --- add the prefix-fibre exhaustiveness lemma (PROVED, unconditional)

- **Source:** this lane (`thresholds-atlas-missing-witness`), verifier
  `verify_atlas_witness.py`.
- **Status:** `PROVED` (finite algebraic fact; scale-independent).
- **Paper impact (proposed):** insert after `thm:small-effective-dual-closure`
  a lemma: *the depth-`w` prefix-fibre family `Phi_w^{-1}(z)` is an
  unconditionally witness-exhaustive first-match atlas with `L=|im Phi_w|<=p^w`
  profiles, paid at effective-image scale when `(a-k-1)log|B|=o(n)`; it strictly
  extends the one-cell `binom(D,a)` discharge (`w=0`) to the shallow-prefix
  regime and is not subject to the `lem:profile-atlas` planted/higher-dim
  exclusion.*  Explicitly record that **exhaustiveness decouples from payment**:
  coverage is unconditional; the binding input is payment (deep prefix / Sidon).
- **Next action:** a maintainer may cite this to narrow `(A2)` in the paper from
  "assume a witness-exhaustive atlas" to "assume a witness-exhaustive atlas that
  BEATS effective-image scale", making explicit that only the *payment* half of
  `(A2)` is a genuine input.

### Entry B --- record the missing-witness = mis-paid-fibre characterisation (WALL)

- **Source:** this lane; `sec:sidon-necessity` (L5142), `lem:no-go` (L5155),
  `prop:ordinary-moment-split` (L5108).
- **Status:** `AUDIT` / `WALL`.  No proof of the Sidon payment is claimed.
- **Paper impact (proposed):** add a remark after `lem:profile-atlas` clarifying
  that the maintainer's "missing witness" failure mode is NOT a set-cover gap
  (Entry A closes that) but a *payment* gap --- a positive-rate Sidon-heavy
  obstruction with failing Sidon payment --- and cross-reference the C9 wall.
- **Next action:** keep `(A2)` conditional; do not promote C9 exhaustion until
  the Sidon payment (input 4/5) is proved at the printed profile scale.

---

## 6. Per-claim label ledger

| # | claim | verdict |
|---|---|---|
| 1 | `W_a(r)`, `def:first-match`, `(A2)`, `lem:profile-atlas`, cell list extracted exactly with tex labels/lines | `EXTRACT` (rung 1) |
| 2 | only unconditional discharge in the paper is the one-cell `binom(D,a)` (`thm:small-effective-dual-closure` SE2); all finer atlases assume `(A2)` | `AUDIT` (verified against L3055, L6530, L967) |
| 3 | `lem:profile-atlas` guard excludes arbitrary-planted & higher-dim cells; those same cells carry up to 27% of GENERIC witness mass | `AUDIT` + census (rung 4) |
| 4 | **prefix-fibre family `Phi_w^{-1}(z)` is an unconditionally witness-exhaustive first-match atlas, `L<=p^w` profiles, paid shallow-prefix; strictly wider than `binom(D,a)`** | **`PROVED`** (rung 3) |
| 5 | Newton dictionary: prefix (support) side = power-sum (syndrome-line) side | `PROVED` (gated `P.newton_dictionary.*`) |
| 6 | toy falsifier: 0 missing witnesses; every algebraic fall-through lands in a real prefix fibre | `NULL` (evidence+scope) |
| 7 | toy energy dichotomy: no large-high-energy fibre; largest fibres are Sidon-side (`Delta*f ~ 2-3`) | `NULL` (evidence+scope) |
| 8 | STRUCTURED `a>n/2` "exhaustion" is a pigeonhole ARTIFACT (forced coset blocks), not structural coverage | `AUDIT` (labelled) |
| 9 | genuine missing-witness = mis-paid primitive fibre (Sidon-heavy obstruction, failing Sidon payment) | `WALL` (input 4/5) |

**Flagged for PI re-derivation:** claim 4 (Entry A) --- the prefix-fibre
exhaustiveness Lemma and its "exhaustiveness decouples from payment" reading;
confirm it genuinely narrows `(A2)` to its payment half and that no consumer of
`(A2)` secretly needs the *finer* atlas to be exhaustive for a reason beyond
payment.

## 7. Recommended next lane

The exhaustiveness half of hard input 1 is now discharged (Entry A) and the
residual risk is pinned to input 4/5 (the Sidon payment).  Recommended next: the
**effective-image collapse / `(FI)` certificate** on primitive leaves --- i.e.
*when does `L >= e^{-o(n)}A_eff` hold*, since Entry A's payment is at
effective-image scale and the whole envelope turns on whether that scale equals
the ambient scale.  This is the natural continuation of the payment-side wall
and does not overlap the deep-prefix `(MI)`/`(MA)` (scottdhughes) or
C9/split-pencil (#518) lanes.
