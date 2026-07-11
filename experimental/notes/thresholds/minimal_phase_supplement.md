# Minimal phase supplement completing the character frame

## Status

`RUNG-1 CROSS-REFERENCE (PROVED) / MINIMAL S PINNED (PROVED) / CRUX MAP UPDATED`.

Research packet answering the named question our packet **PR #609**
(`frame_image_completion.md`) created: what is the **weakest phase-sensitive
supplement `S`** such that avdeev's character frame (**PR #558**, integrated at
`e190193`) plus `S` delivers the image clause
`L >= e^{-o(N)} A_eff` of `def:effective-fourier-payment` (EFP), completing the
frame's **half-interface** (#609) to a full (EFP)-replacement.

Every number below is recomputed by
`experimental/scripts/verify_minimal_phase_supplement.py` (stdlib-only,
`RESULT: PASS (14/14)`, ~0.09 s under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact), **MEASURED** (exact finite toy,
asymptotic not proved from the toy), **AUDIT** (cross-reference / interface
reading of the tex or a sibling note), **OPEN**.

Credit. The block-parabola family and the `(CF1)/(CF2)/(CF3)` identities are
**avdeevvadim's** (PR #558). The J2 gap is our audit **PR #608**; the
magnitude-blindness theorem is our **PR #609**. **scottdhughes's** signed `(LS)`
large sieve is **PR #564**; the **LegaSage** C9 max-fiber razor is the **#585**
chain (`thresholds-c9-r2-near-sidon-razor`, Codex-team attack). **PR #539**
(`fi_full_image_primitive.md`) is the Gap-1 split contrasted below.

---

## HEADLINE (read this first): Rung 1 already closes the *practical* question

**The manuscript already contains a span-normalized route to the image clause.**
The last sentence of `thm:prefix-flatness-package` (tex L7190) names *"the
pointwise sufficient route"*: `thm:bounded-prefix-equidistribution`,
`thm:circle-prefix-equidistribution`, `prop:equidistribution-to-sidon`. Their
max-fiber conclusion is bounded against the **ambient** scale
`barN_0 = |B|^{-R} binom(|T|,m)` (tex **L2822**), *not* the image scale `M/L`.
The tex states the payoff in one sentence at **L2823-2827**:

> *"Here `barN_0` is the ambient profile scale. The theorems below prove an
> **ambient max-fiber bound, which is stronger than image-normalized Q** and, by
> `rem:flatness-certifies-image`, **simultaneously certifies that the realized
> image has full exponential size**."*

and `rem:flatness-certifies-image` (**L4900-4912**) closes the loop: an ambient
flatness bound `max_s f_s <= e^{o(N)} barN^amb` gives, by averaging over the `L`
nonempty fibers, `A_eff/L <= e^{o(N)}` — *"such an ambient flatness theorem
itself proves `(FI)`."* **That `(FI)` is exactly the image clause
`L >= e^{-o(N)} A_eff`.**

**Rung-1 verdict (AUDIT, PROVED cross-reference): the printed route IS
span/ambient-normalized and DOES deliver the image clause.** It is *not* the
#609 image-normalized trap. The whole `(EFP)` two-output bundle (max-fiber
`EF4` **and** image clause) follows from the printed hypotheses. The exact
contrast with the frame:

| route | max-fiber bounded against | normalization | image clause? | anchor |
|-------|---------------------------|---------------|---------------|--------|
| frame `(CF1)` | `M \|\|K_A\|\|/\|A\| = (L\|\|K_A\|\|/\|A\|)barN`, `barN=M/L` | **image** `M/L` | **NO** (#609) | note L83 |
| printed route | `e^{o} barN_0 = e^{o} M/\|B\|^R` | **ambient** `M/\|B\|^R` | **YES** (pigeonhole) | tex L2822, L4900 |

The one-line practical answer: **a phase-sensitive equidistribution input `(PF)`
suffices, and the tex already routes it.** `(PF)` is the pointwise minor-arc
Weil condition `|B|^R binom(Λ+m-1,m) <= e^{o(N)} binom(N,m)` (`rem:pf-numerical`,
tex ~L5); paired with the major aggregate `(MA)`, the two equidistribution
theorems deliver both outputs of `(EFP)`.

**But `(PF)+(MA)` is a REPLACEMENT, not a supplement to the frame.** It never
uses `(CF1)/(CF2)`; it re-proves the *entire* max-fiber bound (both `EF4` and
the image clause). So it answers "is there a printed phase-sensitive route to the
image clause? — **yes**," but it does **not** answer "what is the *minimal
addition* to the frame." For that, Rungs 2-3 exploit the fact that the frame
already controls the packed `b=0` band, so the supplement only needs the dodged
band. The block-parabola shows this is nonempty: it **violates `(PF)`** (its
minor aggregate is exponential, `E = p^k-1`), which is exactly why the printed
route does not apply to it and the image collapses — no contradiction.

### Rung-1 hypotheses and the honest residual (AUDIT)

| statement | hypotheses | supplied by | conclusion |
|-----------|------------|-------------|------------|
| `thm:bounded-prefix-equidistribution` (tex L3300) | `T` mult. coset (or `o(\|T\|)` planted deletions) over `B`; primitive **smooth**-domain chart; ambient `(PF)` + `(MA)` | smooth charts with non-Artin-Schreier minor phases, Weil power-sum `Λ=o(N)` | `\|Ψ^{-1}(z)\| <= e^{o(\|T\|)} barN_0`, all `z`, all first-match residuals |
| `thm:circle-prefix-equidistribution` (tex L3332) | `T=χ(gH∪g^{-1}H)` circle twin-coset; branch points isolated; primitive **circle**/circle-code chart; ambient circle `(PF)` + `(MA)` | circle charts, Weil on the two torus branches | same, `e^{o(\|T\|)} barN_0` |
| `prop:equidistribution-to-sidon` (tex L6622) | hypotheses of `prop:smooth-circle-prefix-flatness-criterion` | the two theorems above | image-normalized Sidon submoment `= e^{o(Nq)}` |

**The honest residual** = rows where `(PF)` **fails**: (i) Artin-Schreier
degenerate minor phases (`def:artin-schreier-phase`, tex L4825: `aR=G^p-G+c`
kills Weil cancellation), and (ii) **effective-image-collapse** profiles where
the image lands in a proper subvariety of `V_g` with heavy dodged-band mass —
the block-parabola is the canonical instance. On exactly these rows the printed
route is silent and the minimal supplement below is the live object.

---

## Rung 2 — the minimal supplement `(S_E)` (PROVED)

### 2.1 Master identity — one Cauchy-Schwarz line carries the whole rung

Let `mu(z) = N_g(z)/M` be the image profile on `V_g`, `|V_g|=A_eff`, characters
`χ ∈ V_g^`, `hat_mu(χ)=Σ_z mu(z)χ(z)`, `hat_mu(0)=1`. Define the **nontrivial
spectral energy**

```
   E  =  Σ_{χ≠0 in V_g^} |hat_mu(χ)|^2  =  A_eff · Σ_z mu(z)^2  −  1      (Parseval)
```

(the second equality is Parseval; `Σ_z mu(z)^2` is the collision probability
`P_2`). Cauchy-Schwarz on the support: `1 = (Σ_{z∈supp} mu(z))^2 ≤ L·P_2`, hence

```
   L  ≥  1/P_2  =  A_eff / (1 + E).                                (MASTER)
```

**Therefore the image clause `L ≥ e^{-o(N)} A_eff` holds whenever
`E ≤ e^{o(N)}`.** This is the minimal supplement.

> **(S_E) (PROVED sufficient).** *Aggregate dodged-band spectral energy is
> subexponential:* `Σ_{χ ∈ V_g^ \ (A−A)} |hat_mu(χ)|^2 ≤ e^{o(N)}`. Equivalently
> (given the frame controls the `A−A` band via `(CF2)`) the total `E ≤ e^{o(N)}`;
> equivalently the collision probability `P_2 ≤ e^{o(N)}/A_eff`; equivalently
> `mu` is image-normalized `L^2`-flat on `V_g`.

Verifier BLOCK 0 recomputes `E = A_eff·P_2 − 1` and `L ≥ A_eff/(1+E)` on random
measures over `Z_5, Z_7, Z_3^2, Z_2^3, Z_5×Z_3`, with equality for the uniform
measure.

### 2.2 frame + `(S_E)` ⇒ `(EFP)` — both outputs, and neither alone (PROVED)

The frame and the supplement deliver **complementary** halves of `(EFP)`:

- **frame ⇒ `EF5`** (image-normalized max-fiber): `(CF1)` gives
  `max_s f_s ≤ ||K_A||·M/|A| ≤ e^{o(N)} M/L = e^{o(N)} barN^img`.
- **`(S_E)` ⇒ image clause**: `L ≥ e^{-o(N)} A_eff` by (MASTER).
- **together ⇒ `EF4`** (span-normalized max-fiber): the image clause upgrades the
  image scale to the span scale, `barN^img = (A_eff/L) barN^amb ≤ e^{o(N)}
  barN^amb`, so `max_s f_s ≤ e^{o(N)} M/A_eff = EF4`. Both `(EFP)` outputs.

**Neither alone suffices.** The frame lacks the image clause (#609, exactly).
And `(S_E)` alone gives only `max_s f_s ≤ M·sqrt((1+E)/A_eff) = e^{o(N)}
M/sqrt(A_eff)` (from `max mu ≤ sqrt(P_2)`), which is a `sqrt(A_eff)`-max-fiber
bound, **weaker** than `EF4`'s `M/A_eff`. So the two are genuinely
complementary — the frame supplies the max-fiber multiplier, `(S_E)` supplies the
image size, and only the pair is the full interface. This is the **cheapest
honest completion** #609 routed, now with `S` pinned. Verifier BLOCK 3
(160 trials) recomputes both implications.

### 2.3 Minimality — the block-parabola calibration (PROVED / MEASURED)

The candidate classes of increasing strength, and where the parabola kills them:

| id | supplement | suffices? | parabola verdict |
|----|------------|-----------|------------------|
| (S1) | per-character `\|hat_mu(χ)\| ≤ e^{o(N)}` on the dodged band | **NO** | **SATISFIED** (max dodged `\|hat_mu\|=p^{-1/2}≤1`) yet `L/A_eff=p^{-k}` |
| **(S_E)** | **aggregate** `Σ_{dodged}\|hat_mu\|^2 ≤ e^{o(N)}` | **YES** (MASTER) | **VIOLATED** exactly: `E=p^k−1=e^{Θ(N)}` |
| (S0) | support: `hat_mu≡0` off `(A−A)` | YES (`E_dodged=0`) | VIOLATED (all `E` is dodged) |
| (S2) | hughes `(LS)` signed multilevel large sieve | YES | VIOLATED (signed sums exponential) |
| (S3) | span-normalized `(EFP)`/`(FI)` itself | YES (target) | VIOLATED (`L<A_eff`) |

**The key minimality fact (PROVED).** `(S1)`, the per-character relaxation, is
**insufficient**: the block-parabola has `max_{χ dodged} |hat_mu(χ)| = p^{-1/2}`,
a fixed constant `≤ 1 = e^{o(N)}`, so it *satisfies* any per-character bound at
the `e^{o(N)}` threshold — yet `L/A_eff = p^{-k} = e^{-Θ(N)}`. Aggregation cannot
be dropped: there are `~p^{2k}` dodged characters and `E = Σ = p^k−1` even though
each term is a constant. **`(S_E)` is the weakest natural (aggregate `L^2`)
sufficient condition**, and it is *calibrated to the parabola*: the parabola sits
exactly on its boundary because Cauchy-Schwarz is an **equality** there,
`L = A_eff/(1+E) = p^{2k}/p^k = p^k` (verifier BLOCK 2). Weakening the norm past
`L^2` (to `L^0`/per-character) provably fails; strengthening past `L^2` (`L^1`,
signed `(LS)`, support `(S0)`) all suffice but overshoot.

### 2.4 The parabola kill-test table (MEASURED, exact — verifier BLOCK 2)

`p` odd prime, `k` blocks, `N=pk`, `M=L=p^k`, `A_eff=p^{2k}`. `E=p^k−1`
brute-checked `== ` closed form; Cauchy-Schwarz tight.

| p | k | M=L | A_eff | E=p^k−1 | L/A_eff | max\|hat_dodged\| | (S1)? | (S_E)? |
|---|---|-----|-------|---------|---------|-------------------|-------|--------|
| 3 | 1 | 3 | 9 | 2 | 0.3333 | 0.5774 | pass | **fail** |
| 3 | 2 | 9 | 81 | 8 | 0.1111 | 0.5774 | pass | **fail** |
| 5 | 1 | 5 | 25 | 4 | 0.2000 | 0.4472 | pass | **fail** |
| 5 | 2 | 25 | 625 | 24 | 0.0400 | 0.4472 | pass | **fail** |
| 7 | 1 | 7 | 49 | 6 | 0.1429 | 0.3780 | pass | **fail** |
| 3 | 3 | 27 | 729 | 26 | 0.0370 | 0.5774 | pass | **fail** |

Every row: `(S1)` passes (per-character mass is a constant `≤1`), `(S_E)` fails
(`E` exponential), image clause fails — the calibration point. The `b=0` band
carries **zero** energy (verifier BLOCK 2, `phi(a,0)=0`), so *all* of `E` is on
the dodged band the frame's packing avoids; `kappa_frame=1` (BLOCK 5, matches
#609).

---

## Rung 3 — updated crux map (AUDIT)

With minimal-`S = (S_E)` pinned, its relation to the two live open objects of
tex hard input 2:

### 3.1 `(S_E)` vs hughes `(LS)` (#564): `(S_E)` is STRICTLY WEAKER

`(LS)` is a **signed** multilevel large sieve at ambient `p^w` normalization,
targeting the *sharp polynomial* `N ≤ n^3`, and (hughes's roadmap) *requires*
square-root cancellation — "every absolute-value method is provably sign-blind
here." `(S_E)` is an **absolute** (`L^2`, magnitude-squared) energy bound at the
effective-span scale, targeting merely *subexponential*. `(LS)` ⇒ `(S_E)`
(sharp per-level signed control bounds each `|hat_mu|`, hence `E`); the reverse
fails (`E` aggregate gives no sharp per-level signed count). So the **image
clause needs far less than `(LS)`** — only subexponential aggregate energy, not
sharp cancellation. `(S_E) < (LS)`.

### 3.2 `(S_E)` vs the LegaSage C9 razor (#585): ORTHOGONAL, and a razor NO does NOT imply `(S_E)`

The razor asks a **max-fiber, image-normalized** question: *does a near-Sidon
exp-large `R=2` fiber exist?* (`c9_literal_interface_counterexample_v1`:
a heavy fiber inside a Sidon cut, singletons dodging the heavy image). A razor
**NO** = no such fiber = image-normalized Q holds (`max_s f_s ≤ e^{o(N)}
barN^img`). `(S_E)` is a **span-normalized, image-size** question (`L` vs
`A_eff`). These are separated by exactly the **#609 factor `A_eff/L`**.

> **A razor NO does NOT imply `(S_E)` (PROVED, verifier BLOCK 4).** The
> block-parabola is a razor **NO** — all fibers have size 1, so
> `max_s f_s = 1 = barN^img` and image-normalized Q holds (`kappa_img=1`) — yet
> it violates `(S_E)` (`E=p^k−1`) and the image clause (`L/A_eff=p^{-k}`). The
> razor's normalization is blind to the image collapse.

### 3.3 Does input 2 still have two independent open objects? — YES, now NORMALIZATION-STRATIFIED

minimal-`S` does **not** expose a common weakening that both routes imply.
Instead it **stratifies input 2 by normalization**, sharpening #608's "two
distinct cruxes":

| stratum | normalization | objects | frame reach |
|---------|---------------|---------|-------------|
| **max-fiber** | image `M/L` | avdeev `(CF2)` packing (certificate side) ≡ LegaSage razor (construction side) — #608's single crux 2 | frame **delivers** this (`EF5`) |
| **image-size** | span `M/A_eff` | **minimal `(S_E)`**; stronger sufficient inputs: printed `(PF)`, hughes `(LS)` | frame **provably cannot** cross here (#609) |

The frame lives entirely on the image-normalized stratum; `(S_E)` is the
**minimal object on the span-normalized stratum**, the one the frame cannot
reach. `(LS)` and the printed `(PF)` are *stronger* sufficient inputs on that
same stratum. So input 2 remains genuinely two-object, but the two objects are
now cleanly separated by the `A_eff/L` gap rather than being incomparable
mechanisms: **the razor is on the frame's side of the gap; `(S_E)`/`(LS)`/`(PF)`
are on the far side.**

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| Rung-1: printed route span/ambient-normalized, delivers image clause | anchors tex L2822-2827 + `rem:flatness-certifies-image` L4900 | AUDIT / PROVED |
| Rung-1: `(PF)+(MA)` is a replacement, not a frame supplement | never uses `(CF1)/(CF2)`; re-proves both `(EFP)` outputs | AUDIT |
| master identity `L ≥ A_eff/(1+E)`, `E=A_eff·P_2−1` | Parseval + Cauchy-Schwarz | PROVED |
| **minimal supplement `(S_E)`: `E ≤ e^{o(N)}`** | frame + `(S_E)` ⇒ `(EFP)` (both outputs); neither alone | **PROVED** |
| per-character `(S1)` insufficient | parabola satisfies it (`p^{-1/2}`) yet collapses | PROVED / MEASURED |
| parabola calibration: `E=p^k−1`, CS equality | kill test, exact | MEASURED |
| `(S_E) < (LS)` strictly weaker | absolute `L^2` subexp vs signed sharp poly | AUDIT |
| razor NO ⇏ `(S_E)` | parabola: razor-NO yet `(S_E)`-fail | PROVED |
| input 2 = two normalization-stratified objects | image-norm (frame/razor) vs span-norm (`(S_E)`/`(LS)`/`(PF)`) | AUDIT |

**Proposed ledger entry (for the maintainer).** Promote, alongside #609's
half-interface promotion of #558: *"The character frame (`EF5`, image-normalized
max-fiber) is completed to a full `(EFP)` interface by the minimal supplement
`(S_E)` — subexponential aggregate dodged-band spectral energy
`Σ_{χ∈V_g^\(A−A)}|hat_mu(χ)|^2 ≤ e^{o(N)}`. `(S_E)` is strictly weaker than
hughes `(LS)`, orthogonal to (and un-implied by) the LegaSage razor, and is the
`e^{o(N)}`-fragment of the printed `(PF)` route restricted to the band the
frame's packing dodges."* Do not promote `(S_E)` as *established* — it is, like
`(CF2)` and `(LS)`, an **OPEN** input; this packet pins *which* input, and that
it is the weakest one, not that it holds.

### The 2-3 steps the PI should re-derive

1. **The master identity (2.1) and (MASTER).** Confirm `E = A_eff·P_2 − 1`
   (Parseval) and `L ≥ A_eff/(1+E)` (Cauchy-Schwarz on the support). This one
   line is the whole sufficiency of `(S_E)`.
2. **frame + `(S_E)` ⇒ `(EFP)`, neither alone (2.2).** Confirm the frame gives
   `EF5` (image-norm max-fiber), `(S_E)` gives the image clause, and the image
   clause upgrades `EF5` to span-normalized `EF4`; and that `(S_E)` alone gives
   only `M/sqrt(A_eff)`, so the two halves are genuinely complementary.
3. **The Rung-1 normalization contrast (headline).** Confirm `barN_0=M/|B|^R`
   (tex L2822) is ambient, so the printed route's max-fiber bound + pigeonhole
   yields `A_eff/L ≤ e^{o(N)}` (`rem:flatness-certifies-image`, L4900) — the
   image clause — whereas the frame's `(CF1)` is against `M/L` (image) and
   cannot. This is why one route escapes the #609 trap and the other does not.

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_minimal_phase_supplement.py   # RESULT: PASS (14/14)
```
