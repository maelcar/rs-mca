# The (FI) full-image certificate on primitive leaves: two-gap decomposition

**Lane:** the binding open content named at the close of the balanced-core arc
(PRs #528/#534/#535/#536): payment on primitive prefix leaves is settled at
*effective-image* scale, but the profile-envelope target comparison is written
at *ambient* scale. The converter is the full-image certificate **(FI)**,
`L >= e^{-o(n)} A`. This packet characterizes when (FI) holds on primitive
leaves and what happens when it fails. It is a **visible-hypothesis / routing**
audit of the active draft, in the pattern of #524/#536 --- **not** an attack on
the `(MI)`/`(MA)` inequalities or the entropy-inverse crux (scottdhughes
#498/#501/#505, consumed as input), nor on the isolated residual Sidon
statement (LegaSage #531) or RC input (#530).
**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (worktree base
`4e3c4ee`). **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_fi_certificate.py` (stdlib-only,
zero-arg, `RESULT: PASS (31 checks)`, ~0.8 s under `ulimit -v 2097152`;
recomputes every gated number with exact prime-field / `F_{2^k}` arithmetic).

**Highest rung reached: 5 (all rungs traversed).**
**Verdict: `PROVED` (Gap-1 criterion; shallow-prefix automatic-FI) + `AUDIT`
(the deep-prefix span-collapse routing is an assumed enumerative input, not a
theorem) + `WALL` (deep-prefix Gap-2) --- NO `COUNTEREXAMPLE`: no census leaf
has uncaught collapsing mass.**

One-line headline: **(FI)-as-written conflates two independent scale gaps along
the tower `L <= A_eff <= A`; the image-fills-span gap is PROVED equivalent to
the effective-scale Q that `(A4)` already supplies (so it is free on every
admissible leaf), the shallow-prefix case is PROVED automatic because the whole
ambient space is subexponential, and the only contentful residue is the
deep-prefix span-collapse `A_eff << A`, whose re-routing to an earlier
structural profile the paper leaves as an unproved enumerative input --- the
same class of gap as #524's atlas exhaustiveness.**

Credit: census primitives (`prefix_key`, `span_dim`, prime-field rank) reuse the
exact code of **PR #534/#535/#536** (`thresholds-a4-covers-high-kappa`,
`thresholds-atlas-missing-witness`); the shallow threshold
`(a-k-1)\log|B|=o(n)` and the closure route are #535's `(SE2)` finding.
avdeev's image-normalization identities (#439-era `Gamma_amb=(A/L)^{q-1}Gamma_img`,
integrated as `lem:image-ambient-moment-conversion`) are the algebraic backbone
of Gap-1 and are re-verified here.

---

## Rung 1 --- EXTRACT: the exact (FI) statement, every consumer, and the C7 routing status

### 1.1 The certificate

Two byte-identical printings, one scalar content:

- `def` block **L4841--4844** (`eq:full-image-certificate`):
  with `M=|Omega_{T,m}|`, `S=Phi(Omega_{T,m})`, `L=|S|`, `A=|B|^R`,
  `barN^img=M/L`, `barN^amb=M/A`,
  > "Unless an ambient full-image certificate has been proved, we set
  > `barN=barN^img`. The certificate is `L >= e^{-o(N)} A`."
- envelope intro **L874--876** (same tag `(FI)`): `L_lambda >= e^{-o(n)} A_lambda`
  "has been proved uniformly."

`S` is the **effective image** (targets actually attained); `B^R` is the formal
ambient codomain. (FI) says the two target counts agree at exponential
resolution (L4846--4854). Its negation is an **effective-image collapse**
(L4850, and the C7 cell L2453: "a boundary map reaches exponentially fewer
boundary values than its ambient codomain contains").

### 1.2 Consumer list (every site that spends (FI))

Every consumer is a place where the *ambient* scale `barN^amb=M/A` is substituted
for the *realized* `barN^img=M/L`. (FI) is the licence.

| # | line | consumer | role |
|---|------|----------|------|
| C-a | L873--876 | envelope intro | `barN^amb` may replace `barN` **only after (FI)** proved uniformly |
| C-b | L922--923 | `(A3)` admissibility | "Any use of the ambient scale is accompanied by (FI)" |
| C-c | L1115--1118 | `(L4)` closed-ledger def | **disjunction**: collapse "is either routed to an earlier profile **or** (FI) is proved before an ambient scale is used" |
| C-d | L1246 | interfaces | "ambient codomain scale may replace it only after (FI)" |
| C-e | L1443--1444 | `def:realized-profile-scale` | "ambient codomain size is not substituted for `L` without (FI)" |
| C-f | L3366--3372 | `cor:fourier-sidon-paid-smooth-circle` proof | ambient max-fiber bound "certifies (FI)", then `lem:image-ambient-moment-conversion` |
| C-g | L4349--4358 | `rem:binary-ambient-image` | ambient moments "do not, **without (FI)**, assert failure of an image-normalized primitive payment"; names char-2 `p_{2j}=p_j^2` collapse |
| C-h | L5387--5398 | `cor` proof | `(PF)+(MA)` ambient flatness -> `rem:flatness-certifies-image` -> (FI) -> conversion |
| C-i | L5437--5449 | `thm:sidon-resolved-payment` proof | same chain: full-slice flatness proves (FI), conversion transfers to image scale |
| C-j | L5608--5609 | ledger requirement | "the ledger must also record (FI) or a direct ambient theorem" |
| C-k | L6377--6379 | primitive-prefix interface | "ambient scale may be substituted only after (FI) or a direct ambient theorem" |
| C-l | L6459--6465 | unprofiled locator-list | **Under (FI) `L_w >= e^{-o(n)}|B|^w`**, image-Q `<=> ` ambient-Q at exp accuracy |
| C-m | L6581--6583 | `lem:residual-monotonicity` | "If `U=e^{o(N)}barN_0^amb`, then (FI) follows" |
| C-n | L7378--7379 | planted cells | "ambient prefix depth may be used only under (FI)" |

### 1.3 How (FI) is *proved* wherever it is claimed --- and where it is not

**Finding (AUDIT, exact):** (FI) is **never an independent lemma**. Every proof
of it (C-f, C-h, C-i, C-m) routes through **`rem:flatness-certifies-image`**
(L4902--4910): *if* an ambient max-fiber bound
`max_s f_s <= e^{o(N)} barN^amb` is in hand, then pigeonhole over the `L`
nonempty fibers gives `A/L <= e^{o(N)}`, i.e. (FI). The two-line derivation is
exact (verifier check `A3.flatness_certifies_image`):

    M = sum_{s in image} f_s  <=  L * max_s f_s  <=  L * e^{o(N)} * M/A
      =>  A/L <= e^{o(N)}  =>  L >= e^{-o(N)} A.

So **(FI) is a re-badging of ambient flatness**: it is free exactly where the
hard ambient max-fiber bound `(PF)+(MA)` (or `lem:residual-monotonicity`'s `U`)
is already available, and it is *not* proved on the leaves that `(A4)` can only
pay at *effective/image* scale (`def:effective-fourier-payment`, `A_eff`
normalization). The remark itself flags this (L4908): "image collapse cannot be
silently assumed away before that estimate has been established." This is the
anti-circularity guard, and it is correctly placed.

### 1.4 The C7 / effective-image-collapse routing status

**Where does the mass go when `L << A`?** The paper's two escape hatches (C-c
disjunction, and L877--881): (i) **route** the collapse "by the first-match rule
to an earlier profile so that its slopes and all witnesses above them are
removed from the later residual," recording it as an *effective-image
rank-collapse profile*; or (ii) keep every estimate at image scale.

Status of the **routing** branch (i):

- The **C7 saturation / effective-image-collapse cell** (L2440--2454) is
  declared **constructible** "in the projective locator and explanation
  incidence, **but its projection degree remains an enumerative input**"
  (L2451--2452). **=> the payment is ASSUMED, not proved.**
- The `(L4)` closed-ledger clause (C-c, L1115) states the route **as a
  hypothesis** ("is either routed ... or (FI)"), not a theorem. `def:closed-ledger`
  closes only when this is "verified for the row" (L1242).
- There is **no lemma** asserting that a collapsing leaf's re-route *target*
  earlier profile exists **and** absorbs the mass **and** stays inside the
  `e^{o(n)}E_n` budget. That triple obligation is exactly what a proof would
  need.

**Verdict rung 1:** (FI) is a **cleanly gated hypothesis** (every ambient-scale
use is explicitly conditioned on it, C-a..C-n) --- no silent ambient
substitution found. But the *routing alternative* that discharges (FI)-failure
is **AUDIT: assumed / enumerative input**, the same status class as #524's atlas
exhaustiveness (A2) and the C7 projection degree.

---

## Rung 2 --- CHARACTERIZE: the two-gap decomposition and the proved Gap-1 criterion

The effective-span Fourier machinery (`lem:effective-span-fourier` L2868,
`def:effective-fourier-payment` L2929) introduces a **third** scale between `L`
and `A`, and this is the key to characterizing (FI):

    L   <=   A_eff   <=   A ,
      L     = |Phi(Omega_{T,m})|                        realized image
      A_eff = |V_g| = p^{dim_Fp Span{g(t)-g(t_0): t in T}}   effective span (EF1 L2861)
      A     = |B|^R = p^{Rf},   f=[B:F_p]                ambient codomain

Both inclusions are definitional: the fixed-weight sum map lands in the affine
coset `m g(t_0)+V_g` (L2864), so `L<=A_eff`; and `V_g <= B^R`, so `A_eff<=A`.
This splits the certificate:

> **(FI)-ambient `L>=e^{-o(n)}A`  <=>  Gap-1 `L>=e^{-o(n)}A_eff`  AND  Gap-2 `A_eff>=e^{-o(n)}A`.**

### 2.1 Gap-1 (image fills its effective span) --- `PROVED` free on admissible leaves

`def:effective-fourier-payment` (EFP, L2929) with constant `kappa` gives, via
(EF3)/(EF4), the exact max-fiber bound `max_z N_g(z) <= kappa*binom(|T|,m)/A_eff`,
and the paper states (L2944): *"It also implies that the realized image contains
at least `A_eff/kappa` points."* Re-derived and verified exactly
(`A1.EFP.image_ge_Aeff_over_kappa`): with `M=binom(|T|,m)=sum_z N_g(z)`,
`F_max=max_z N_g(z)`, and `L` = number of nonempty fibers,

    M = sum_z N_g(z) <= L*F_max     (pigeonhole)
      =>  L >= M/F_max = A_eff/kappa*,   kappa* := A_eff*F_max/M.

`kappa*` is the **smallest** admissible EFP constant (the tightest EF4), and it
equals `F_max / (M/A_eff)` = **(max fiber)/(effective-average fiber)** = the
*effective-scale max-fiber ratio*. Therefore:

> **Criterion (PROVED).** On a primitive leaf, Gap-1 `L>=e^{-o(n)}A_eff` holds
> **iff** the effective-scale max-fiber ratio `kappa*` is subexponential, i.e.
> **iff image-normalized Q holds at effective-span normalization**. Condition
> `(A4)` requires exactly this payment (`(MI)+(MA)` on the effective span
> `V_g`, or a `def:sidon-paid-cell` bound). **Hence Gap-1(FI) is NOT an
> independent obligation --- it is discharged by the payment every admissible
> primitive leaf already carries.** This is the fiber=chart pigeonhole route
> made exact.

This closes the "route (i)" candidate of the task's goal ladder (fibre-count x
max-fibre pigeonhole) with equality, and grounds it in the paper's own EFP.

### 2.2 Gap-2 (effective span is ambient) --- the genuine content

Gap-2 `A_eff>=e^{-o(n)}A` is a pure `F_p`-rank condition:

    dim_Fp V_g  >=  Rf - o(n/log p),     A_eff/A = p^{dim V_g - Rf}.

`V_g` is the `F_p`-span of `|T|-1 = Theta(n)` generator differences inside the
`Rf`-dimensional space `B^R`. Generic behaviour: `dim V_g = min(|T|-1, Rf)`.

- **Large characteristic, prime field `B=F_p` (`f=1`):** `A=p^R`, and by the
  Vandermonde structure of the power-sum/elementary prefix the difference
  vectors have full rank whenever `|T| > R`. So **`dim V_g = R`, Gap-2 holds**
  whenever `N=|T| > R` --- the generic frontier condition. (Census confirms:
  every prime-field leaf has `dim=w`, `A_eff=A`, r2=1.000.)
- **Extension field, `f>1`, deep prefix `R=Theta(n)`:** `Rf` can exceed
  `N ~ n`, so `dim V_g <= N < Rf`, giving `A_eff = p^N << p^{Rf} = A`: a genuine
  **span collapse**. This is exactly the char-`p` / Frobenius mechanism named in
  `rem:binary-ambient-image` (L4355: in char 2 `p_{2j}=p_j^2`, the power-sum map
  has a Frobenius image collapse).

**Interpretation.** A span collapse `dim V_g < Rf` is a **universal `F_p`-linear
relation among the prefix coordinates**, holding for *every* support on the
leaf. Such a relation is an algebraic subvariety = a **lower-complexity
structural profile** (field-descent / Frobenius / planted / quotient). The
routing claim of 1.4 is precisely that first-match assigns the collapsed mass to
that earlier profile. Whether the earlier profile **exists, catches the mass,
and is paid** is the unproved enumerative input.

---

## Rung 3 --- CENSUS: collapse-ratio distribution and the uncaught-leaf hunt

Exact enumeration over the #534/#536 configs (structured `D=F_p^*` and generic
`D=[1..n]<F_p^*`, `w in 1..3`), elementary depth-`w` prefix. For each leaf:
`r1 = lnL/lnA_eff` (Gap-1), `r2 = dim/w` (Gap-2), `r_all = lnL/lnA` (overall);
`kappa* = A_eff*F_max/M` and its exponential rate `ln(kappa*)/n`.

| regime | (p,n,k,a) | w | M | L | dim | A_eff | A | kappa* | r1 | r2 | r_all |
|--------|-----------|---|---|---|-----|-------|---|--------|----|----|-------|
| struct | (13,12,5,7) | 1 | 792 | 13 | 1 | 13 | 13 | 1.001 | 1.000 | 1.000 | 1.000 |
| struct | (13,12,5,8) | 2 | 495 | 169 | 2 | 169 | 169 | 1.707 | 1.000 | 1.000 | 1.000 |
| struct | (17,16,7,10) | 2 | 8008 | 289 | 2 | 289 | 289 | 1.155 | 1.000 | 1.000 | 1.000 |
| struct | (19,18,8,11) | 2 | 31824 | 361 | 2 | 361 | 361 | 1.078 | 1.000 | 1.000 | 1.000 |
| generic | (13,9,4,6) | 1 | 84 | 13 | 1 | 13 | 13 | 1.238 | 1.000 | 1.000 | 1.000 |
| generic | (17,11,4,7) | 2 | 330 | 217 | 2 | 289 | 289 | 2.627 | 0.949 | 1.000 | 0.949 |
| generic | (19,12,4,7) | 2 | 792 | 341 | 2 | 361 | 361 | 2.279 | 0.990 | 1.000 | 0.990 |
| generic | (23,14,5,8) | 2 | 3003 | 529 | 2 | 529 | 529 | 1.938 | 1.000 | 1.000 | 1.000 |
| generic | (29,18,6,10) | 3 | 43758 | 21265 | 3 | 24389 | 24389 | 3.902 | 0.986 | 1.000 | 0.986 |

**Distribution readout (`evidence + scope`, toy scale):**

- **Gap-2 (span): `r2 = dim/w = 1.000` on every prime-field leaf.** No span
  collapse over prime fields at `w<=3`; `A_eff = A` identically. The generic
  Vandermonde span is full whenever `N>R` (2.2).
- **Gap-1 (image/span): `r1 in [0.949, 1.000]`, `kappa* in [1.0, 3.9]`
  (a bounded constant, rate `ln kappa*/n < 0.05`).** The realized image fills
  its effective span up to a subexponential factor on every leaf; the largest
  `kappa*` (3.9) is at the deepest config and is a *constant*, not exponential.
- **Overall: `r_all in [0.949, 1.000]`.** The realized image is within a
  subexponential factor of the full ambient on every census leaf. **Zero leaves
  with genuine collapse (`r_all` bounded away from 1).**
- **Uncaught collapsing leaf: NONE** (`B.no_uncaught_collapsing_leaf`). No leaf
  combines an overall collapse with a span drop, so there is no
  `COUNTEREXAMPLE`-class routing gap at this scale. Consistent with #536's null.

### 3.1 The one place a genuine Gap-2 collapse appears: char-2 Frobenius (Part C)

Over `F_8 = F_2[t]/(t^3+t+1)`, domain = the full field, `a=2`, depth `w=2`
(ambient `F_2`-dim `= 2*3 = 6`, `A=2^6=64`):

| coordinates | image size | dim_Fp V_g | A_eff | r2 = dim/6 |
|-------------|-----------|-----------|-------|-----------|
| **power-sum** `(p_1,p_2)` | 7 | 3 | 8 | **0.500** |
| **elementary** `(e_1,e_2)` | 28 | 6 | 64 | **1.000** |

Since Frobenius `x->x^2` is `F_2`-linear, the power-sum image lies in the
`F_2`-linear graph `{(x,x^2)}` of dimension exactly `k=3` --- **half** the
ambient exponent: a genuine, decisive Gap-2 span collapse `A_eff=8 << A=64`,
directly instantiating `rem:binary-ambient-image`. **The paper's own routing
catches it:** `(A5)` (L935--941) mandates elementary coordinates in small
characteristic, and the elementary prefix has full span `r2=1.000`. So this
named collapse is a **coordinate artifact**, re-routed by a coordinate change,
not an image loss --- the one concretely paid instance of the C7 mechanism.

---

## Rung 4 --- Shallow-prefix automatic-FI: `PROVED`

> **Proposition (PROVED).** On a shallow prefix, meaning `log A = o(|T|)`,
> equivalently `(a-k-1)\log|B| = o(n)` (SE2, L3054--3060), the certificate (FI)
> holds automatically with **no payment**.

*Proof.* Pointwise for any nonempty leaf, `1 <= L <= A`, hence
`A/L <= A`. If `A = |B|^R = e^{o(N)}` (shallow), then `A/L <= A = e^{o(N)}`,
which is exactly `L >= e^{-o(N)} A`. **qed** (verifier `D.shallow.A_over_L_le_A`,
`D.shallow.discrepancy_bounded_by_logA`: `max ln(A/L)/ln(A) = 1.000` across all
configs --- the (FI) discrepancy never exceeds the ambient budget `log A`).

This is *not* a statement that `L` fills `A`; it is that when the entire ambient
target is subexponential, image- and ambient-normalized moments coincide at
exponential resolution **regardless of collapse**. It matches `(SE2)` exactly:
`log A = o(|T|)` already gives image-normalized Q, effective `(MI)`, effective
`(MA)`, and the direct `(RC)` alternative "with subexponential loss" (L3054), so
(FI) is subsumed there. It is also #535's shallow-prefix closure regime.

**Scope of contentfulness.** (FI) therefore has content **only on deep
prefixes**, `R\log|B| = Theta(n)`. There Gap-1 is still free (2.1), and the sole
residue is Gap-2 span-collapse + its routing (1.4, 2.2). The toy census is
entirely shallow (`max (log A)/n` finite; `D.shallow.toy_configs_are_shallow`),
so the deep-prefix Gap-2 wall is **not reachable at toy scale** --- honestly a
`SCOPE` limit, not a discharge.

---

## Rung 5 --- WALL: precise statement and dead cheap routes

> **(FI) deep-prefix wall.** Fix an admissible primitive leaf sequence with
> `(a_n-k_n-1)\log|B_n| = Theta(n)` (deep) over a growing extension
> `f_n=[B_n:F_p]\to\infty` with `R_n f_n > (1-c)\,|T_n|`. Then the effective
> Fourier span can collapse, `A_eff = p^{\dim V_g} <= p^{|T_n|} = e^{-Theta(n)} A`,
> and the ambient-normalized envelope term `barN^amb=M/A` is **not** licensed
> from the effective-scale payment `L>=A_eff/kappa*` alone. Closing the row
> requires **either** a proof that the collapse locus routes (first-match) to an
> earlier structural profile whose paid budget absorbs the collapsed mass inside
> `e^{o(n)}E_n`, **or** a direct ambient max-fiber theorem
> (`lem:residual-monotonicity` `U`), which is the `(MI)/(MA)`-on-ambient-slice
> input owned by the scottdhughes program.**

**Dead cheap routes (checked):**

1. **"EFP already gives `L>=A_eff/kappa`, so (FI) holds."** DEAD as stated: EFP
   gives (FI) at *`A_eff` scale* (Gap-1), not at ambient `A`. When `A_eff<<A`
   the two differ by `p^{Rf-\dim V_g}`, exactly the missing factor. (Verifier
   separates `r1` from `r_all`.)
2. **"`rem:flatness-certifies-image` proves (FI)."** DEAD as a *cheap* route: it
   requires the ambient max-fiber bound `max_s f_s <= e^{o(N)}barN^amb`, which is
   the hard `(PF)+(MA)` ambient-flatness theorem itself --- circular if used to
   *avoid* proving ambient flatness (the remark says so, L4908).
3. **"Pigeonhole `L>=M/F_max` closes it."** DEAD for Gap-2: pigeonhole bounds
   `L` below by `A_eff/kappa*`, never above `A_eff`; it is blind to the span
   deficiency `A_eff/A`.
4. **"Newton dictionary makes power-sum = elementary, so no collapse."** DEAD in
   small characteristic: the dictionary needs `char > w` (L6473); the char-2
   Frobenius collapse (Part C) is precisely the failure, patched only by the
   `(A5)` coordinate switch --- which routes but does not eliminate the
   phenomenon in general extensions.
5. **BSG / additive-combinatorial "image smallness forces fiber energy."** Not a
   *cheap* route and it collides with the boundary: quantifying `L<<A_eff` via
   fiber energy is the `(MI)/(MA)` inverse theory itself (hughes #498/#501/#505),
   consumed here, not attacked.

---

## Proposed paper changes (ledger entries, `experimental/asymptotic_rs_mca.md` convention)

These are **audit ledger entries only**; no `.tex`/`.pdf` edited.

- **L-FI-1 (`AUDIT`, clarity).** In `def:effective-fourier-payment` (L2944)
  make the standing implication explicit as a named corollary:
  *`(EFP)` with constant `kappa` implies `L >= A_eff/kappa`, hence the
  effective-scale full-image certificate `L >= e^{-o(n)}A_eff` whenever
  `kappa=e^{o(n)}`.* This records that **Gap-1 of (FI) is discharged by `(A4)`**
  and is not an independent obligation, removing a latent double-counting worry
  in the C-a..C-n consumer sites.

- **L-FI-2 (`AUDIT`, gap made visible).** Split the (FI) certificate text
  (L4841--4863) along the tower `L<=A_eff<=A`: state Gap-1 (proved from `(EFP)`,
  L-FI-1) and Gap-2 (`A_eff>=e^{-o(n)}A`, the rank condition
  `dim V_g >= R[B:F_p]-o(.)`) separately, so that the **only** contentful
  obligation on deep prefixes is Gap-2 + its routing. Cross-reference the C7 cell.

- **L-FI-3 (`AUDIT`, hypothesis discharge).** Add a shallow-prefix remark after
  `thm:small-effective-dual-closure` (L3060): *when `log A=o(|T|)`, (FI) holds
  unconditionally because `A/L<=A=e^{o(N)}`; thus (FI) is contentful only on
  deep prefixes `R\log|B|=Theta(n)`.* Makes the "or (FI)" branch of `(L4)`
  (L1115) vacuous in the shallow regime, matching #535.

- **L-FI-4 (`OPEN OBLIGATION`).** Flag the C7 routing (L2452, L1115) as the
  paper's one remaining unproved discharge for deep-prefix span-collapse:
  the earlier-profile re-route needs a lemma giving *(existence + mass
  absorption + `e^{o(n)}E_n` budget)*, or it must be replaced by the
  ambient `(MI)/(MA)` input (scottdhughes). Same status class as `(A2)`.

---

## Per-claim label summary

| claim | label |
|-------|-------|
| (FI) statement + full consumer list C-a..C-n extracted | `AUDIT` (exact) |
| (FI) is never an independent lemma; always via `rem:flatness-certifies-image` (ambient flatness) | `PROVED` (reading, verified pigeonhole) |
| C7 collapse-routing to an earlier profile is an assumed enumerative input, not a theorem | `AUDIT` |
| Scale tower `L<=A_eff<=A` splits (FI) into Gap-1 and Gap-2 | `PROVED` (definitional; verifier tower checks) |
| Gap-1 `L>=e^{-o(n)}A_eff` <=> effective-scale Q; discharged by `(A4)`'s `(EFP)` | `PROVED` (exact, `A1`) |
| `lem:image-ambient-moment-conversion` identity `Gamma^amb=(A/L)^{q-1}Gamma^img` | `PROVED` (exact, `A2`) |
| Gap-2 holds over prime fields when `N>R` (Vandermonde full span) | `PROVED` (finite) + census `evidence` |
| char-2 Frobenius span collapse `r2=1/2`, resolved by elementary coords `(A5)` | `PROVED` (exact, `C`) instantiating `rem:binary-ambient-image` |
| Census: no uncaught collapsing leaf; `r_all in [0.949,1]` | `evidence + scope` (toy) |
| Shallow-prefix `(a-k-1)\log|B|=o(n)` => (FI) automatic, no payment | `PROVED` |
| Deep-prefix Gap-2 span-collapse + routing is the binding wall | `WALL` / `AUDIT` |
| deep-prefix Gap-2 not reachable at toy scale | `SCOPE` |

**Boundaries respected:** `(MI)/(MA)`/entropy-inverse (hughes #498/#501/#505)
consumed as the ambient input, never attacked; residual Sidon (#531) and RC
(#530) inputs consumed; Danny #529 two-shell, latifkasuli #518 split-pencil
untouched; avdeev image-normalization identities re-verified and credited.
