# RS--MCA Entropy Frontiers submission draft — theorem-by-theorem audit

**Status:** `AUDIT`. Target `experimental/rs_mca_entropy_frontiers.tex`
(upstream tip `2b1a7e2`, "Add RS-MCA entropy frontiers draft"; 5940 lines,
179 theorem-environments). Audited against `experimental/asymptotic_rs_mca.tex`,
`experimental/cap25_cap_v13_raw.tex`, `experimental/grande_finale.tex`, and the
integrated audit packets under `experimental/notes/`.

**Mandated vocabulary** (`agents.md`, `eb42b82`): every item ends
`NO ISSUE` / `FIXED` / `OPEN GAP` / `COUNTEREXAMPLE_NEW_FLOOR`, with
tree-anchored `file:label` / `file:line` references. Per-item classification of
each of the maintainer's five named claim classes:
`PROVED-IN-PAPER` / `CITED` / `HYPOTHESIS` / `UNLABELED-GAP`.

**Maintainer's ask, verbatim (logged next action):** *"Audit it theorem by
theorem ... In particular, verify that every conditional compiler input,
Fourier/Sidon payment, major-arc aggregate, profile-envelope comparison, and
ray-compiler claim is either proved in the paper or clearly labeled as an
[assumption/hypothesis]."*

**Verifier.** `experimental/scripts/verify_entropy_frontiers_audit.py` (zero-arg,
stdlib-only, `RESULT: PASS`, 18/18 gates + 18/18 live tamper tests, 0.07 s,
17 MB RSS). Data JSON `experimental/data/cap25_v13_entropy_frontiers_audit.json`.

---

## 0. Headline

The submission draft is a **model of conditional honesty.** Every one of the
five claim classes is either **proved in the paper as an implication from named
inputs**, or **clearly labeled as a definition/hypothesis/input** — there is no
step where a Fourier/Sidon payment, a major-arc aggregate, a profile-envelope
comparison, a ray-compiler count, or a closed-ledger input is silently asserted
as available. The paper's architecture makes the conditionality explicit:

- The **unconditional** results are the finite-row package
  (`thm:main-unconditional`, L482) and the smooth/circle **countertheorem**
  (`thm:intro-countertheorem` / `thm:smooth-quotient-obstruction`).
- The **conditional** upper theorem `thm:main-smooth-circle` (L675, titled
  *"Conditional profile-envelope compiler"*) rests entirely on the seven
  admissibility conditions `(A1)`–`(A7)` of `def:admissible-sequence` (L623),
  which name **(PF)**, **(MA)**, **(RC)**, **(FI)** and the profile-envelope
  comparison as its inputs.
- Exactly **one** `\begin{hypothesis}` environment exists in the whole paper,
  and it is **(RC)** `hyp:ray-compiler` (L4375) — the ray compiler is formally a
  hypothesis, not a lemma (verifier I2).
- The two named numerical conditions **(PF)** `def:prefix-flat-range` (L2231) and
  **(MA)** `def:major-arc-aggregate` (L2216) are *definitions of conditions*, not
  theorems; the paper repeatedly states they are inputs (*"first-match
  terminology alone does not imply it"*, L2228; scope remark L909
  *"It does not prove the source estimate (PF) or (MA)"*).
- The load-bearing finite ingredients are **proved in-paper** (self-contained);
  `\cite{Cho26CapV13,Cho26Grande}` is a **background** citation only — the paper
  makes **no external theorem-number citation** into those sources for any
  load-bearing asymptotic step (verifier C1, C2).

**Findings.** One low-severity `OPEN GAP` (an exposition wording nit in the
primitive-residual definition). The previous audit's `F-1` (target-reserve named
but undefined) is **`FIXED`** in this draft. No `COUNTEREXAMPLE_NEW_FLOOR`.

### Verdict tally

| verdict | count | items |
|---|---:|---|
| `NO ISSUE` | 33 | every inventoried instance across classes (a)–(e); the C9-counterexample handling; both no-regression checks |
| `FIXED` | 2 | F-1 target-reserve now defined in body (L4476); F-2 open-problem citation structure absent (self-contained) |
| `OPEN GAP` | 1 | G-1: `def:primitive-first-match-residual` closes with a self-referential "primitivity certificate used by the ... arguments" phrase |
| `COUNTEREXAMPLE_NEW_FLOOR` | 0 | — |

---

## 1. TIER 1 — inventory of the five claim classes (core artifact)

Classification legend: **P** = `PROVED-IN-PAPER` (proved outright or proved as an
implication from the named inputs); **H** = `HYPOTHESIS` (a clearly labeled
definition/condition/assumption/input); **C** = `CITED` (resolved to a source
label); **G** = `UNLABELED-GAP` (presented as available but neither proved,
cited, nor flagged). No item is **C** (the paper is self-contained on
load-bearing steps) and no item is **G** except the exposition nit G-1.

### (a) Conditional compiler inputs

| # | claim (label · line) | asserts | class | verdict |
|---|---|---|---|---|
| a1 | `def:admissible-sequence` (A1)–(A7) · L623 | the seven row-uniform admissibility conditions the compiler is conditional on | **H** | `NO ISSUE` |
| a2 | `def:closed-asymptotic-ledger` (L1)–(L4) · L808 | "closed" = each required payment/ray bound is *"supplied as theorems rather than left as hypotheses"* | **H** | `NO ISSUE` |
| a3 | `thm:main-smooth-circle` · L675 | conditional numerator `B^MCA ≤ e^{o(n)}𝔈_n`; proof cites (A2)(A3)(A4)(A5)(A6)(A7) | **P** (implication) | `NO ISSUE` |
| a4 | `thm:main-ledger` · L836 | closed ledger ⟹ safe side; correctly conditional | **P** (implication) | `NO ISSUE` |
| a5 | **(FI)** `eq:full-image-certificate` · L603/L3510 | ambient scale may replace image scale only after `L ≥ e^{-o(n)}A` proved | **H** (dischargeable: `rem:flatness-certifies-image` L3569 proves flatness ⟹ FI) | `NO ISSUE` |
| a6 | window uniformity · L263, L910, `def:admissible-sequence` "uniformly in every received line" | `κ_n=e^{o(n)}` dominating losses uniformly in the window | **H** (imported; explicitly listed as not-proved in `rem:intro-sidon-heavy-scope` L910) | `NO ISSUE` |
| a7 | `lem:first-match-bound` · L1215 | add-back: disjoint first-match slope sets sum to the row bound | **P** | `NO ISSUE` |
| a8 | `def:closed-asymptotic-ledger` closing line · L831 | *"Constructibility, a raw support count, or a support-pair moment alone does not close a ledger."* | **P** (guard) | `NO ISSUE` |

### (b) Fourier / Sidon payments

| # | claim (label · line) | asserts | class | verdict |
|---|---|---|---|---|
| b1 | **(PF)** `def:prefix-flat-range` · L2231 | the pointwise minor-arc scale inequality `R log|B| + log C(Λ+m-1,m) − log C(|T|,m) ≤ o(|T|)` | **H** (definition of a condition) | `NO ISSUE` |
| b2 | `def:sidon-paid-cell` · L3796 | a leaf *has a Sidon moment payment* if `Γ^sid=e^{o(Nq)}`; *"not equivalent to a first-match distinct-slope payment"* | **H** | `NO ISSUE` |
| b3 | `thm:prefix-flatness-power-sum` · L3875 | `|Ψ^{-1}(z)| ≤ |B|^{-R}C(N,m)+C(Λ+m-1,m)` from the pointwise char bound `|P_j|≤Λ` | **P** (Fourier inversion + cycle index) | `NO ISSUE` (verifier T3) |
| b4 | `prop:weighted-weil-minor-arcs` · L3917 | the minor-arc pointwise bound `Λ=C_0(Δ+1)√|B|+|P|` via Weil on smooth cosets / torus | **P** (Weil) | `NO ISSUE` |
| b5 | `thm:bounded-prefix-equidistribution` · L2246 | *If* (PF)+(MA) *then* fiber `≤ e^{o(|T|)}barN_0` (smooth) | **P** (implication) | `NO ISSUE` |
| b6 | `thm:circle-prefix-equidistribution` · L2277 | same for circle twin-cosets under the circle (PF)+(MA) | **P** (implication) | `NO ISSUE` |
| b7 | `cor:sidon-payment-from-prefix-flatness` · L3956 | (PF)+(MA) ⟹ Sidon-heavy log-moment `e^{o(Nq)}` | **P** (implication) | `NO ISSUE` |
| b8 | `thm:sidon-resolved-payment` · L3995 | (PF)+(MA) ⟹ `Γ^sid_{q,σ}≤e^{o(Nq)}`; certifies (FI) | **P** (implication) | `NO ISSUE` |
| b9 | `thm:primitive-q` · L4124 | Sidon-moment hypothesis ⟹ primitive Q `max_s ≤ e^{o(N)}barN` | **P** (BSG+quasicube) | `NO ISSUE` |
| b10 | `prop:high-energy-impossible` · L4113 | `E(F)≥|F|³/K ⟹ |F|≤K^{O(1)}` via BSG + Boolean-cube growth | **P** | `NO ISSUE` |
| b11 | `lem:no-go` · L3821 / §`sec:sidon-necessity` | closure-rich diagrams cannot capture a heavy low-energy fiber ⟹ a Sidon cell is *necessary* | **P** | `NO ISSUE` |
| b12 | `prop:ordinary-moment-split` · L3774 | splits the ordinary moment into low-/high-energy branches | **P** | `NO ISSUE` |
| b13 | `rem:small-characteristic-cycles` · L3905 | small-char leaves *need a direct certificate* — the pointwise theorem is stated in the large-char range | **H** (honest scope flag) | `NO ISSUE` |

### (c) Major-arc aggregate

| # | claim (label · line) | asserts | class | verdict |
|---|---|---|---|---|
| c1 | **(MA)** `def:major-arc-aggregate` · L2216 | `|B|^{-R}Σ_{major}|e_m(...)| ≤ e^{o(|T|)}barN_0`; *"first-match terminology alone does not imply it"* | **H** (definition of a condition) | `NO ISSUE` |
| c2 | `def:major-arc` · L3929 | the algebraic classification of major vs minor characters; *"major arcs still require (MA)"* | **H** (classification, not an estimate) | `NO ISSUE` |
| c3 | `prop:major-arcs-are-cells` · L3938 | the classification is constructible but *"does not prove (MA)"* | **P** (guard) | `NO ISSUE` |
| c4 | `prop:frontier-weil-separation` · L3978 | minor arcs alone cannot create positive rate at near-zero ambient scale; *"a full flatness conclusion also requires (MA)"* | **P** (minor-arc only) | `NO ISSUE` |

### (d) Profile-envelope comparison

| # | claim (label · line) | asserts | class | verdict |
|---|---|---|---|---|
| d1 | `eq:profile-envelope` `𝔈_n(a)` · L587 | the image-normalized envelope `1+(n-a+1)+sup Σ_λ(1+barN_λ)` | **H** (definition) | `NO ISSUE` |
| d2 | `eq:intro-identity-scale` `barN_1` · L386 | ambient identity scale `C(n,a)|B|^{-w}` | **H** (definition) | `NO ISSUE` |
| d3 | `thm:smooth-quotient-obstruction` (=`thm:intro-countertheorem`) · L2690/L524 | a square-quotient profile is `exp((h(α)/4)n)`, exponentially above `barN_1` ⟹ identity scale is **not** a universal bound | **P** (unconditional counterexample) | `NO ISSUE` (verifier T4) |
| d4 | `thm:binary-cubic-obstruction` · char-2 · L2865 | cubic-quotient analogue `exp((h(α)/6)n)` | **P** | `NO ISSUE` |
| d5 | `cor:intro-identity-frontier` · L727 | identity frontier recovered **only** *"suppose in a window `𝔈_n(a) ≤ e^{o(n)}(1+n-a+barN_1)`"* | **H** (the comparison is an explicit premise) | `NO ISSUE` |
| d6 | `cor:final-no-ledger-assumption` · L5616 | the identity-dominance comparison *"cannot be deleted"* — proven non-deletable by the counterexample | **P** (guard) | `NO ISSUE` |
| d7 | §`sec:complete-cell-budgets` quotient/planted/tangent/extension/split-pencil · L5403-5469 | each cell retained at its own `1+barN_λ`; *"the identity scale is not used as a universal budget"* (L5369); each payment routed to a named criterion, not automatic | **H/P** (per-cell criteria named; `barN^img≤e^{o(n)}barN_1` explicitly *"not automatic and is false in `thm:smooth-quotient-obstruction`"*, L5425) | `NO ISSUE` |
| d8 | `def:quotient-remainder-profile` + `eq:qr-comparison-crossing` · L2327 | the exact field-drop term separating quotient from identity | **P** (exact normal form) | `NO ISSUE` |

### (e) Ray-compiler (RC) claims

| # | claim (label · line) | asserts | class | verdict |
|---|---|---|---|---|
| e1 | **(RC)** `hyp:ray-compiler` · L4375 | direct slope bound OR the `(H_λ,J_λ)` incidence with `J_λ|Ω^0|/H_λ=e^{o(n)}`; *"its existence is not a consequence of Q or SP"* | **H** (the only formal `\begin{hypothesis}`) | `NO ISSUE` |
| e2 | `prop:q-sp-no-ray` · L4299 | Q and SP alone **cannot** determine rays (an abstract incidence realizes any `M∈[1,min]`) | **P** (the non-inference the maintainer worried about) | `NO ISSUE` |
| e3 | `prop:pair-ray-multiplicity` · L4325 | the exact double-count `|Z|≤J·SP/H`; a ray estimate follows only if `J|Ω|/H=e^{o(n)}` | **P** | `NO ISSUE` |
| e4 | `prop:q-implies-sp` · L4400 | *If* Q discharged *and* (RC) *then* all primitive ray ledgers discharged | **P** (implication) | `NO ISSUE` |
| e5 | `lem:saturation-quotient-rays` · L4255 | a noncommon support carries at most one finite slope (interpolation functional) | **P** | `NO ISSUE` (verifier T2) |
| e6 | `prop:split-pencil-payment` / `lem:pencil-payment` · L3407 / L1930 | one-parameter moving-root bound `|Z|≤⌊(n-g)/h⌋` | **P** (incidence count) | `NO ISSUE` |
| e7 | `rem:balanced-core-exhaustion` · L3428 | higher-dimensional balanced-core is **not** covered by the one-pencil bound — *"part of (RC) or a direct ray count"* | **H** (honest scope flag) | `NO ISSUE` |
| e8 | `def:saturated-line-rays` · L4222 | saturated ray count *"is not obtained by dividing the raw witness count unless a lower fiber bound is proved"* | **P** (guard) | `NO ISSUE` |

**Class totals (verifier I1/I3).** `(PF)` appears 29×, `(MA)` 39×, `(RC)` 30×,
`(FI)` 12× across the paper; every occurrence I traced is consistent with the
definitions above (a labeled input or an implication from it). No occurrence
promotes a condition to a proved fact.

---

## 2. Findings (ranked)

### G-1 — `def:primitive-first-match-residual` closes on a self-referential phrase: `OPEN GAP` (low severity, exposition)

`def:primitive-first-match-residual` (L1189–1206) declares a residual primitive
when *"the remaining boundary map carries **the row-specific primitivity
certificate used by the analytic and ray arguments**."* Read in isolation, the
definition names its certificate by the arguments that consume it, rather than
inlining the certificate. The **content is present and correct** — the very next
paragraph (L1211–1213) states *"it records the specific quotient, field-descent,
rank, planted, and ray-saturation exclusions certified by the atlas,"* i.e. the
same named-exclusion list used in the intro (L287–292). So this is **not** a
mathematical gap and the paper does **not** commit the circularity error the C9
literal-interface note warned about (see §3). It is an exposition tightening: a
referee reading `def:primitive-first-match-residual` alone should not have to
reach forward one paragraph to learn what the certificate is.

**Why it is worth flagging.** `c9_literal_interface_counterexample_v1.md` §5
proves that *"'Primitive' must not be defined by the absence of a positive-rate
Sidon-heavy fiber, because Proposition 2 would make that definition circular."*
The submission draft complies (the Sidon payment is a *separate* condition,
`def:sidon-paid-cell`), but a definition that points at "the certificate used by
the arguments" invites exactly the circular reading the note cautions against.
Inlining the exclusion list removes the ambiguity. Verdict: `OPEN GAP`
(exposition only). Ledger entry L-1 below.

### F-1 (predecessor) — target-reserve now defined in body: `FIXED`

The profile-envelope audit's `F-1` flagged that the abstract named a
*target-reserve* hypothesis never defined in the body. In this draft
**target reserve is defined** at L4476 (*"the explicit bit slack in one of the
two comparisons ..."*), used in the intro (L773–774) and fixed in the
terminology map (L972). Verdict: `FIXED`.

### F-2 (predecessor) — open-problem citation structure absent: `FIXED`

The profile-envelope audit's `F-2` flagged that the C8 CapV13 sub-citation
bottomed out in the open problem `prob:capfp-split`. This self-contained draft
carries **no C8-style external theorem citation**: the moving-root/split-pencil
content is proved in-paper (`prop:split-pencil-payment` L3407) and the
higher-dimensional case is deferred to `(RC)`. The citation structure that
produced `F-2` does not recur (verifier C2). Verdict: `FIXED`.

---

## 3. TIER 2 — cross-consistency and known-counterexample handling

**No regression to unconditional.** The submission draft's asymptotic frontier
theorems are all conditional: `thm:main-smooth-circle` (titled *Conditional*),
`thm:intro-asymptotic-rs-mca` (premised on certified unsafe + closed-ledger safe
agreements), `cor:intro-identity-frontier` (premised on the identity-dominance
comparison), `thm:main-ledger`, and `cor:frontier-final`. The paper states
outright *"The profile-envelope compiler is conditional only on the explicit
enumerative statements in (A1)–(A7)"* (L777). The audited
`asymptotic_rs_mca.tex` is itself conditional after the `2acc7be` pivot; the
submission draft **claims no more than** the audited paper (verifier X1, X2).

**Sidon-heavy obstruction — stated as an obstruction, not assumed away.** The
square-quotient/cubic-quotient Sidon-heavy families are the paper's **own**
countertheorem (`thm:intro-countertheorem`, `thm:smooth-quotient-obstruction`),
and §`sec:sidon-necessity` (`lem:no-go`) proves the Sidon cell is *necessary* —
a heavy low-energy fiber cannot be forced into the high-energy inverse branch.
The paper never assumes the Sidon payment holds; it makes it condition `(A4)`
(verifier X3, T4).

**avdeev/Danny literal-C9 counterexample — correctly handled.** The note
`c9_literal_interface_counterexample_v1.md` proves (Prop 2) that the
image-normalized C9 (Sidon) moment bound is **equivalent to primitive Q** at
exponential scale, and exhibits an explicit family (`R=2`, exploding field
`Q=100k+1`, block-trade fibers) that satisfies every displayed finite-set /
fixed-density / weighted-Vandermonde / image-normalization requirement yet has a
**positive-rate** Sidon-heavy moment (rate `log 2 / 4`). The submission draft is
**consistent with this counterexample and does not assume it away**, for three
independent reasons the verifier checks (C3, C4):

1. **The Sidon moment stays a hypothesis.** `thm:primitive-q` (L4124) reads
   *"Suppose there is a logarithmic moment order ... for which `Γ^sid ≤ e^{o(Nq)}`
   ... Then the leaves satisfy primitive Q."* The draft proves the *implication*
   (Sidon payment ⟹ Q), never the premise. This is exactly the non-trivial
   direction of the C9 ⟺ primitive-Q equivalence, with the premise labeled.
2. **Primitivity is not defined circularly.** `def:primitive-first-match-residual`
   defines primitive by removal of **named algebraic degeneracies** (quotient /
   field-descent / rank / planted / ray-saturation), and `def:sidon-paid-cell`
   keeps the Sidon payment a **separate analytic statement**
   (*"not equivalent to a first-match distinct-slope payment"*). This is the
   precise repair the C9 note (§5, item "Primitive must not be defined by the
   absence of ...") demanded. (See finding G-1 for the residual wording nit.)
3. **The counterexample is a `(MA)` failure, and (MA) is a separate input.** The
   C9 family's heavy fiber is a **block-trade / major-arc** phenomenon
   (constant on a positive-density structured fiber), not a minor-arc one.
   `prop:frontier-weil-separation` only controls minor arcs and explicitly adds
   *"a full flatness conclusion also requires (MA),"* while
   `prop:major-arcs-are-cells` states the classification *"does not prove (MA)."*
   So the draft's minor-arc control (Weil) does **not** contradict the
   counterexample; the unmet condition is `(MA)` / atlas exhaustiveness `(A2)`,
   both of which the draft carries as explicit inputs. No silent assumption.

Net Tier-2 verdict: `NO ISSUE`. The submission draft neither over-claims relative
to `asymptotic_rs_mca.tex` nor assumes away either known obstruction.

---

## 4. TIER 3 — exact numeric spot-replication

All replications use exact integer / small-prime-field arithmetic and are gated
by the verifier (each with a live tamper test). Smallest instances of claims
specific to this draft:

| gate | paper claim | replication | result |
|---|---|---|---|
| **T1** | `thm:collision-aware-pole` (L1527): `M(L)=⌈L(q−n)/(q−n+k(L−1))⌉` distinct bad slopes | formula + Cauchy–Schwarz boundary algebra `L²≤M·(L+kL(L−1)/(q−n))`; the profile-envelope-audit GA5 cross-check `⌈20·14621/14716⌉=20`; monotonicity `1≤M(L)≤L`, `M→L` as `q→∞`; genuine `F_37` instance (5 polys, pole sweep, best pole realizes `5≥M(L)=4`) | `PASS` |
| **T2** | `thm:main-unconditional` (ii) / `lem:saturation-quotient-rays` (L4255): a noncommon support carries `≤1` finite bad slope | brute force over `F_13`, 720 (support, `u_0`, `u_1`) trials via the interpolation functional `A_T`; **0 violations**; explanation-iff spot-checks pass | `PASS` |
| **T3** | `thm:prefix-flatness-power-sum` (L3875): `|Ψ^{-1}(z)| ≤ |B|^{-R}C(N,m)+C(Λ+m−1,m)`, with the cycle index `C(Λ+m−1,m)=[u^m](1−u)^{−Λ}` | explicit weighted map on `F_5`, `R=1`, `N=7`, `m=3`: brute Fourier inversion `max fiber=7 ≤ bound=11` (`Λ=2`); cycle-index identity verified for several `(Λ,m)` | `PASS` |
| **T4** | `thm:smooth-quotient-obstruction` (L2690): square-quotient fiber `exp((h(α)/4)n)` ≫ `barN_1=e^{o(n)}` | scales at `p∈{11,13,17,23,101,1009}`, `α=0.4`: separation grows in the tail; `(1/n)ln barN_sq → 0.1700 ≈ h(0.4)/4 = 0.1683`; `(1/n)ln barN_1 → 0` | `PASS` |

These cover the unconditional lower side (T1), the finite exact numerator and the
(e) non-inference (T2), the (b) Fourier core (T3), and the (d) counterexample
scale (T4). They are illustrative replications of the integer content, not
proofs of the asymptotic statements.

---

## 5. TIER 4 — OPEN (sections not line-audited)

Coverage was banked depth-first on Tier 1; the following sections were read for
structure and their headline claims classified above, but were **not** audited
line-by-line and are recorded `OPEN` (no silent coverage claim):

- §`sec:mca-ledger` (L976), §`sec:deep-regime` (L1235) — the finite MCA-witness
  ledgers and deep-regime exact numerator internals (the deep exact count is
  used by T1/T2 at the interface level only).
- §`sec:smooth-circle-domains` (L1963) folding-tower constructions;
  §`sec:quotient-obstruction` internal steps beyond the scale gate (T4 gates the
  scales, not the full char-2 cubic construction of `thm:binary-cubic-obstruction`).
- §`sec:li-wan-details` (L4820), §`sec:threshold-details` (L4910),
  §`sec:coordinate-atlas` (L4708) — the Li–Wan/Weil residual-stability and
  entropy-crossing appendices (the entropy algebra was checked at statement
  level, cf. profile-envelope audit GB2).
- §`sec:algebraic-repairs` (L5632), §`sec:smooth-domain-detail` (L5484),
  §`sec:circle-domain-detail` (L5551) — the planted/determinantal/circle
  edge-case payment criteria (classified as per-cell named criteria in d7, not
  re-derived).
- The internal proofs of the imported `thm:bsg` and `thm:quasicube` (only their
  *stated forms* and the Boolean *application* are used; the application is gated
  by T3 in the profile-envelope audit and by `prop:high-energy-impossible` here).

---

## 6. Ready-to-paste ledger entries (proposed; NOT applied to the paper)

Per policy, no `.tex`/`.pdf` was touched. A dedicated audit ledger for this paper
(`experimental/rs_mca_entropy_frontiers.md`) **does not yet exist**; if the
maintainer opens one it should follow the `experimental/asymptotic_rs_mca.md`
conventions (Source / Status / Paper impact / Files preserved elsewhere / Next
action). The single actionable entry:

### Ledger entry L-1 (primitive-residual definition wording)

- **Source:** this audit `entropy_frontiers_submission_audit.md` (finding G-1),
  verifier gate C4; motivated by `c9_literal_interface_counterexample_v1.md` §5.
- **Status:** `OPEN GAP` (exposition; not a mathematical gap).
- **Paper impact:** `def:primitive-first-match-residual` (L1199–1203) ends with
  *"the remaining boundary map carries the row-specific primitivity certificate
  used by the analytic and ray arguments,"* naming the certificate by its
  consumers. The clarifying named-exclusion list is one paragraph later
  (L1211–1213), so a standalone reading of the definition is momentarily
  circular — the exact shape the C9 note warns against, even though the draft
  does not commit the error.
- **Next action:** Inline the exclusion list into the definition, e.g.
  *"... carries the certified removal of its named quotient, field-descent,
  rank, planted, and ray-saturation degeneracies (the row-specific primitivity
  certificate),"* so the definition is self-contained and cannot be read as
  "primitive = no Sidon-heavy fiber."

(Informational, no action: the previous audit's `F-1` target-reserve gap is
already `FIXED` in this draft at L4476; `F-2`'s open-problem citation structure
does not recur because the load-bearing finite ingredients are proved in-paper.)

---

## 7. Nonclaims

- A `NO ISSUE` verdict means the printed step survived a genuine attempt to break
  it **under the paper's stated hypotheses**; it does **not** re-verify the
  internal proofs of imported `Cho26CapV13`/`Cho26Grande`/BSG/quasicube results
  (their stated forms and the Boolean application are checked; the application is
  gated exactly).
- The five-class inventory tables list every **distinct claim/use**; the raw
  textual occurrence counts are larger (`(PF)` 29×, `(MA)` 39×, `(RC)` 30×,
  `(FI)` 12×) and were traced for consistency, not tabulated row-by-row.
- Tier 3 replications are **illustrative** of the integer content at the smallest
  instances (`F_5`, `F_13`, `F_37`, `p∈{11..1009}`); they are not proofs of the
  asymptotic statements.
- Tier 4 sections are recorded `OPEN`; this audit makes **no** coverage claim for
  them beyond the structural/headline classification in §1.
- No `COUNTEREXAMPLE_NEW_FLOOR`: nothing here refutes a printed claim of the
  submission draft. The Sidon-heavy and literal-C9 constructions are obstructions
  the paper itself states or is consistent with, not refutations of its theorems.
- This note lives under `experimental/notes/audits/` labelled `AUDIT`; it makes
  **no** promotion or merge recommendation. That is the maintainer's decision;
  this packet is collaborative input to it.

## 8. Files

- note: `experimental/notes/audits/entropy_frontiers_submission_audit.md` (this)
- verifier: `experimental/scripts/verify_entropy_frontiers_audit.py`
  (18 gates, 18 tamper tests, `RESULT: PASS`, 0.07 s, 17 MB)
- data: `experimental/data/cap25_v13_entropy_frontiers_audit.json`
- audited: `experimental/rs_mca_entropy_frontiers.tex` `@2b1a7e2`, against
  `experimental/asymptotic_rs_mca.tex`, `experimental/cap25_cap_v13_raw.tex`,
  `experimental/grande_finale.tex`
- context packets: `experimental/notes/audits/asymptotic_profile_envelope_audit.md`,
  `experimental/notes/audits/c9_literal_interface_counterexample_v1.md`,
  `experimental/notes/thresholds/asymptotic_c9_*.md`
