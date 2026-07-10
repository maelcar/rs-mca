# Asymptotic RS--MCA frontiers replacement draft --- delta audit vs #494

**Status:** `AUDIT`. Target `experimental/asymptotic_rs_mca_frontiers.tex`
(worktree tip `4e3c4ee`, "Replace asymptotic frontiers draft"; 7913 lines,
224 numbered environments). This is the maintainer's replacement for the draft
our team audited as PR #494 (`experimental/rs_mca_entropy_frontiers.tex`
`@2b1a7e2`, 5940 lines, 179 environments). This packet is a *delta* audit: what
the rewrite changed, whether #494's findings were absorbed, and an adversarial
pass on the five hard inputs the new `agents.md` (`@4e3c4ee`) makes the proof
checklist.

**Mandated vocabulary** (`agents.md@4e3c4ee`): every input ends
`NO ISSUE` / `FIXED` / `OPEN GAP` / `COUNTEREXAMPLE_NEW_FLOOR`, with
`file:label` / `file:line` references. All line numbers are gated by the
verifier against the file on disk.

**Verifier.** `experimental/scripts/verify_frontiers_delta_audit.py`
(zero-arg, stdlib-only, `RESULT: PASS`, **937 checks**, ~3 s, <2 GB). Data
`experimental/notes/audits/data/asymptotic_frontiers_delta_audit.json`. Every
number below is verifier-gated unless tagged `UNGATED`.

**Distinction discipline.** For each item I mark whether I **checked the proof**
(re-derived the steps) or only **checked the statement** (classified the label
and its interfaces). Coverage banked Part 3 > Part 2 > Part 1 per the task's
budget rule; Part 1 granularity was cut first (see "What was cut").

---

## 0. Headline

The rewrite is a **body expansion, not a restructuring**: same **39** top-level
sections in the **same order with the same labels** (delta 0), +1973 lines,
+45 environments. It does exactly two structural things the maintainer's
checklist asks for, and it does them well:

1. **It splits the image-scale payment into two named, falsifiable inputs.**
   The old draft carried `(PF)`+`(MA)`; the new draft introduces `(MI)`
   (`def:aggregate-minor-payment`, L3082) and an *effective* major/minor
   partition (`def:effective-major-minor`, L2912), proves `MI+MA => flatness`
   (`prop:effective-mi-ma-flatness`, L3098), and **demotes `(PF)` to "only one
   sufficient way to prove `(MI)`"** (L3092--3094). `(MI)` occurs 28x in the new
   draft and 0x in the old. This is precisely hard input #2 ("image-scale MI +
   MA, or a direct Sidon payment").
2. **It adds unconditional finite bracket theorems** so the conditional
   asymptotic corollary no longer carries the finite comparison silently:
   `thm:unconditional-support-envelope-bracket` (L6212) and
   `thm:exact-first-adjacent-row` (L1870, literal binomial constants) are both
   new (old-count 0), plus `thm:small-effective-dual-closure` (L3027) which
   discharges all four analytic inputs unconditionally in the
   low-boundary-entropy regime.

**RC is still the sole formal hypothesis.** Exactly one `\begin{hypothesis}`
environment exists, still `hyp:ray-compiler` (L6033). The refined input surface
lives inside `def:admissible-sequence` (A1)--(A7) (L896), not in new hypothesis
environments.

**Verdicts.** No `COUNTEREXAMPLE_NEW_FLOOR`. Four inputs `OPEN GAP` (all
visibly labeled, none silently consumed); input #5 (lower reserve) is
`NO ISSUE` at statement level with one `AUDIT` caveat. #494's only open finding,
**G-1, is `UNADDRESSED`** (verbatim wording survives). #494's `F-1`/`F-2` stay
`FIXED`.

---

## Part 1 --- Structural delta

**Method:** statement-level (environment census + section diff + label
novelty), verifier-gated. Not a line-by-line re-read of all 7913 lines.

### Environment inventory delta (gated)

| class | old `@2b1a7e2` | new `@4e3c4ee` | delta |
|---|---:|---:|---:|
| theorem | 31 | 45 | +14 |
| proposition | 43 | 50 | +7 |
| lemma | 40 | 48 | +8 |
| corollary | 10 | 16 | +6 |
| definition | 36 | 39 | +3 |
| **hypothesis** | **1** | **1** | **0** |
| remark | 18 | 25 | +7 |
| **total** | **179** | **224** | **+45** |
| sections (`\section`) | 39 | 39 | 0 |
| lines | 5940 | 7913 | +1973 |

The old audit's "179 theorem-environments" reproduces exactly (124 thm-like +
36 def + 1 hyp + 18 rem). No section was added, removed, or renamed at top
level; one section *title* changed (`sec:finite-scope`: "asymptotic scope" ->
"exact scope") with the label preserved. So the "72% rename / +2571 changed
lines" the task cites is git's file-rename diff of same-skeleton bodies.

### Classified environment delta (the load-bearing additions)

New labels absent from the old draft (each gated present in new, git-verified
absent in old):

| new label · line | class | role |
|---|---|---|
| `thm:unconditional-support-envelope-bracket` · 6212 | unconditional-proved | finite bracket `a_- < a* <= a_+` |
| `thm:exact-first-adjacent-row` · 1870 | unconditional-proved | first adjacent row with literal binomials (AD1/AD2) |
| `thm:small-effective-dual-closure` · 3027 | unconditional-proved | discharges MI/MA/Q/RC when `log A = o(|T|)` |
| `def:effective-major-minor` · 2912 | definitional | certified effective Fourier partition |
| `def:effective-fourier-payment` · 2930 | definitional/proved | (EFP) => (EF4) max-fiber |
| `def:aggregate-minor-payment` = `(MI)` · 3082 | conditional-input (named) | the new minor input |
| `prop:effective-mi-ma-flatness` · 3098 | conditional-on-named (proved implication) | MI+MA => flatness |
| `thm:exact-partial-occupancy` · 3609 | unconditional-proved | canonical partial-occupancy slices (A2) |
| `thm:exact-finite-profile-compiler` · 6737 | unconditional-proved | exact finite upper budget |
| `lem:exact-profile-addback` · 7261 | unconditional-proved | image-coverage/overlap add-back |

Preserved anchors (old-count 1): `def:major-arc-aggregate` `(MA)`,
`def:prefix-flat-range` `(PF)`, `hyp:ray-compiler` `(RC)`,
`def:admissible-sequence`, `thm:main-smooth-circle`.

### Where the five hard inputs live in the new text (gated line refs)

1. **witness-exhaustive first-match atlas** --- `def:admissible-sequence` (A2),
   L896 (body L905--911); consumed by `lem:first-match-bound` L1526 and
   `prop:numerator-bound` L6084; profile-count discharge `lem:profile-atlas`
   (proof = A2).
2. **image-scale MI + MA, or direct Sidon** --- `(MI)`
   `def:aggregate-minor-payment` L3082, `(MA)` `def:major-arc-aggregate` L2985,
   Sidon `def:sidon-paid-cell` L5130; `(PF)` `def:prefix-flat-range` L3160 is a
   sufficient certificate for `(MI)`; bundled in (A4) L896 (body L924--934).
3. **residual ray compiler** --- `(RC)` `hyp:ray-compiler` L6033; scope flag
   `rem:balanced-core-exhaustion` L4763; in (A6) L896 (body L942--945).
4. **profile-envelope comparison with target** --- (A7) L896 (body L946--952);
   explicit premise in `cor:intro-identity-frontier` L1011.
5. **lower reserve / unsafe-side comparison** --- `sec:frontier` L6103;
   `prop:simple-pole-lower` L6180; `thm:unconditional-support-envelope-bracket`
   L6212 (SB2 = "the literal target reserve").

---

## Part 2 --- Absorption of #494

Working from #494's own findings list (`entropy_frontiers_submission_audit.md`):

| #494 finding | status in new draft | evidence |
|---|---|---|
| **G-1** primitive-residual definition closes on a self-referential "certificate used by the ... arguments" phrase (`OPEN GAP`, exposition) | **UNADDRESSED** | `def:primitive-first-match-residual` L1500 still ends "carries the row-specific primitivity certificate used by the analytic and ray arguments" (L1513--1514); the clarifying named-exclusion list ("quotient, field-descent, rank, planted, and ray-saturation") is still one paragraph later (L1523--1524). Verbatim carry-over; the rewrite did not inline it. **checked statement.** |
| **F-1** target-reserve named but undefined | **STILL FIXED** | defined in `sec:frontier` L6135 ("the explicit bit slack in one of the two comparisons"); additionally SB2 of L6212 is called "the literal target reserve". **checked statement.** |
| **F-2** open-problem citation structure | **STILL FIXED** | self-contained; no external theorem-number citation on any load-bearing asymptotic step. **checked statement.** |
| **RC is the sole formal hypothesis** (does the rewrite add/split hypotheses?) | **PRESERVED** | exactly one `\begin{hypothesis}` (gated); still `hyp:ray-compiler`. The rewrite added *conditions inside* `def:admissible-sequence` --- notably the new `(MI)` in (A4) --- but **no new hypothesis environment** and no split of RC. **checked statement.** |
| **33-statement five-class inventory** (did classes shift?) | **GREW, did not shift** | +45 environments; every new thm-like environment is either unconditional-proved (finite bracket, first-adjacent-row, small-effective-dual-closure, partial-occupancy, addback, finite-profile-compiler) or a proved implication from named inputs (`prop:effective-mi-ma-flatness`). The one input-surface change is (A4) naming `(MI)` and demoting `(PF)`; the (a)--(e) claim classes keep their P/H character. The abstract five-class picture from #494 (unconditional finite package + smooth/circle countertheorem; conditional compiler on A1--A7; RC the sole hypothesis) holds unchanged. **checked statement.** |

**Absorption headline: 1 of 4 substantive #494 items still open (G-1
UNADDRESSED); 3 remain FIXED/PRESERVED.** The rewrite absorbed none of G-1 and
did not regress F-1/F-2/RC-sole-hypothesis. (I count G-1, F-1, F-2, and the
RC-sole-hypothesis status; the 33-inventory is a structural observation, not a
fix.)

---

## Part 3 --- Five-inputs adversarial audit (core)

For each input: (a) where stated/deferred; (b) visibility in consuming theorem
statements; (c) falsifiability; (d) verdict. Then the failure-mode checklist and
the two demanded re-derivations.

### Input 1 --- witness-exhaustive first-match atlas
- **(a)** `def:admissible-sequence` (A2), L905--911: "A first-match atlas covers
  every bad-slope witness and has `e^{o(n)}` profiles. The total distinct-slope
  contribution of its algebraic cells is at most `e^{o(n)} E_n(a_n)`."
- **(b) Visible.** Consumers name it: `lem:first-match-bound` L1526 ("If every
  received line admits a witness-exhaustive first-match atlas ..."),
  `prop:numerator-bound` L6084 ("paid by (A2)"), `thm:main-smooth-circle` proof
  L967 ("Condition (A2) supplies a witness-exhaustive first-match atlas"). No
  silent consumption. `lem:profile-atlas` proof (L4777) explicitly excludes
  "arbitrary planted subsets or an unproved decomposition of a higher-dimensional
  pencil ... could create exponentially many profiles" --- honest.
- **(c) Falsifiable** (an exhaustiveness + profile-count assertion), though
  exhaustiveness is hard to *refute* without exhibiting a missing-witness family.
- **Partial unconditional discharge:** `thm:small-effective-dual-closure` L3027
  makes a one-cell support-restricted incidence "exhaustive for the whole
  exact-agreement incidence when `Omega = binom(D,a)`, or after an exhaustive
  partition into such slices." That is honest about when one cell is global.
- **(d) Verdict: `OPEN GAP`.** Named, visible, falsifiable; still an input in
  general. **checked proof** of the disjointization interface
  (`lem:first-match-bound`, `prop:exact-support-upper` L1361 --- the injective
  noncommon-support map is correct); **checked statement** of (A2) exhaustiveness.

### Input 2 --- image-scale MI + MA, or a direct Sidon payment
- **(a)** `(MI)` `def:aggregate-minor-payment` L3082:
  `sum_{chi in m_eff} |e_m(chi(g(t)-g(t_0)))| <= e^{o(|T|)} binom(|T|,m)`.
  `(MA)` `def:major-arc-aggregate` L2985: the analogous major-character sum bound
  (with an ambient `|B|^{-R}...<= e^{o(|T|)} barN_0` equivalent). Sidon
  alternative `def:sidon-paid-cell` L5130. `(PF)` L3160 is demoted to a pointwise
  certificate for `(MI)`.
- **(b) Visible.** (A4) (L924--934) names (MI), (MA), the Sidon alternative, and
  (PF)-as-certificate; `thm:main-smooth-circle` proof cites (A4) and
  `prop:effective-mi-ma-flatness`. `def:effective-fourier-payment` L2930 warns
  (EFP) "does not pay an ambient annihilator twice" (image-scale normalization
  guard). No silent consumption.
- **(c) Falsifiable:** three explicit character-sum inequalities.
- **Proved bridges:** `prop:effective-mi-ma-flatness` L3098 (MI+MA => max-fiber
  `<= e^{o(|T|)} binom(|T|,m)/A_eff`), `thm:small-effective-dual-closure` L3027
  (when `log A = o(|T|)`, designate all characters major: `C_maj <= A-1`, so MI,
  MA, image-normalized Q and RC's direct alternative all hold with subexponential
  loss). I **checked the proof** of the EF7 reduction: with `C_min=0`,
  `C_maj=A-1`, `A_eff=A` the bound `(M/A)(1+0+(A-1)) = M` matches the trivial
  slice bound SE1 (gated). And `A <= |B|^{a-k-1}` gives `log A = o(n)` when
  `(a-k-1) log|B| = o(n)` (gated).
- **(d) Verdict: `OPEN GAP`** (substantially sharpened vs old). The rewrite's
  best move: the payment is now three precise inputs plus a real unconditional
  discharge in the shallow/low-boundary-entropy regime.

### Input 3 --- residual ray compiler for higher-dimensional balanced cores
- **(a)** `(RC)` `hyp:ray-compiler` L6033: either a direct
  `|Z^o_lambda| <= e^{o(n)}(1+barN_lambda)`, or an incidence
  `I_lambda subseteq Z x P` with `deg(gamma) >= H`, `deg(A,B) <= J`,
  `J m_lambda / H = e^{o(n)}`. Scope flag `rem:balanced-core-exhaustion` L4763:
  the one-parameter moving-root bound (`prop` L4744, `|Z| <= floor((n-g)/h)`)
  "neither covers a higher-dimensional coefficient family nor proves that such a
  family decomposes into subexponentially many pencils. That structural statement
  is part of (RC) or must be established by a direct ray count."
- **(b) Visible.** (A6) names (RC); `prop:q-implies-sp` L6059 ("if primitive Q
  is discharged and (RC) holds ..."), `prop:primitive-residual-numerator` L6073,
  `prop:numerator-bound` L6084 all name it. The non-inference is explicit inside
  the hypothesis: "its existence is not a consequence of Q or SP. In particular,
  one representing pair per ray does not supply the required lower degree" (L6054
  --6056) --- this is the exact `A6`-class concern from #494 (present-as-proved
  what is only hypothesized), and it is discharged by keeping RC a hypothesis.
- **(c) Falsifiable:** a quantified incidence-degree inequality.
- **(d) Verdict: `OPEN GAP`.** The one genuinely open structural object
  (higher-dimensional balanced core) is isolated and precisely stated.
  **checked proof** of the moving-root pencil bound (L4754--4759: incidence count,
  one projective parameter per moving root, `n-g` moving points --- correct) and
  of `prop:q-implies-sp`; **checked statement** of RC itself.

### Input 4 --- complete profile-envelope comparison with the target
- **(a)** (A7) L946--952 (the envelope "is used in the final budget; it is not
  replaced by the identity term unless that comparison is proved for the row");
  explicit premise in `cor:intro-identity-frontier` L1012--1017 ("suppose in a
  window that `E_n(a) <= e^{o(n)}(1 + n-a + barN_1(a))`").
- **(b) Visible.** The comparison is a hypothesis of the corollary, not a lemma.
  The proof block (L6252--6287) states it plainly: "The corollary assumes, rather
  than deduces from exponent notation, that quantitative reserves furnish the
  exact safe and unsafe tests within `o(n)` of that crossing" (L6279--6281). This
  is the anti-silent-consumption sentence.
- **(c) Falsifiable, and known false in general:** `thm:smooth-quotient-
  obstruction` shows the identity scale is not a universal envelope bound, so the
  comparison is genuinely a per-window premise. `cor:final-no-ledger-assumption`
  proves it "cannot be deleted".
- **(d) Verdict: `OPEN GAP`.** Correctly carried as an explicit premise; the
  content is *which windows are identity-dominant*, which the paper does not
  claim to settle. **checked statement.**

### Input 5 --- lower reserve / unsafe-side comparison
- **(a)** `sec:frontier` L6103; exact unsafe test `prop:simple-pole-lower` L6180
  (`P(a) > B*` => unsafe); unconditional bracket
  `thm:unconditional-support-envelope-bracket` L6212, SB2
  `P(a_-) > B* , U(a_+) <= B*` => `a_- < a* <= a_+`, adjacent => `a* = a_+`.
- **(b) Visible.** `thm:intro-asymptotic-rs-mca` L989 names both legs ("a
  certified profile-list construction is unsafe at `a_-` and the closed-ledger
  ... budget is safe at `a_+`").
- **(c) Falsifiable / concrete:** SB2 is stated with literal binomials and "no
  asymptotic placeholder"; the upper leg `U(a) = min{|Gamma|, binom(n,a)}` is
  unconditional (`prop:exact-support-upper` L1361, injective noncommon-support
  map --- **checked proof**).
- **(d) Verdict: `NO ISSUE`** (statement) **+ one `AUDIT` caveat.** The lower leg
  `P(a_-)` inherits the *realizability* of the collision-aware pole construction
  (`prop:simple-pole-lower`, via `thm:collision-aware-pole` and
  `prop:exact-prefix-list`). "Unconditional" is accurate in the sense the theorem
  intends (placeholder-free finite comparison), but the lower reserve's validity
  at a chosen `a_-` is the pole construction's, not a trivial count. This is the
  "unsafe-side lower reserve not actually crossing the target" failure mode:
  **it does cross, unconditionally, via SB2** --- but only where the pole
  construction realizes the identity list (non-deep, separating-field regime;
  the deep regime uses `cor:exact-deep-numerator` instead, and there the raw
  identity-list heuristic `P` overshoots the true `r+1` numerator, so `P` must
  not be applied inside the deep regime). `AUDIT`: flag for PI that
  `prop:simple-pole-lower`'s realizability hypotheses be printed alongside SB2.

### Re-derivation A --- `thm:unconditional-support-envelope-bracket` (L6212) [checked proof]

Statement: `L(a) = ceil(binom(n,a)|B|^{-(a-k-1)})`,
`P(a) = ceil((|Gamma|/q) ceil(L(q-n)/(q-n+k(L-1))))`,
`U(a) = min{|Gamma|, binom(n,a)}`; SB2 => SB3; adjacent => equality; SB4
`binom(n,k+1) <= B* => a*=k+1`.

Proof audit:
- Lower leg `B^MCA(a) >= P(a)` is `prop:simple-pole-lower` (L6180); its `P`
  matches (13.3) exactly. **Sourced correctly.**
- Upper leg `B^MCA(a) <= U(a)` is `prop:exact-support-upper` (L1361), whose
  `min{|Gamma|, binom(n,a)}` matches `U` exactly. **Sourced correctly.**
- Bracket = monotonicity of the numerator in `a` (every witness at `a+1` is a
  witness at `a`): `P(a_-) > B* => a_-` unsafe, `U(a_+) <= B* => a_+` safe, so
  `a* in (a_-, a_+]`; adjacent => `a_+`. **Logic correct** and does not require
  `U` or `P` to be monotone (only the numerator is) --- gated with a synthetic
  nonincreasing numerator.
- SB4: `U(k+1) = min{|Gamma|, binom(n,k+1)} <= binom(n,k+1) <= B*` makes the
  first permitted agreement safe, so `a* = k+1`. **Gated.**
- `M(L) = ceil(L(q-n)/(q-n+k(L-1)))` satisfies `1 <= M(L) <= L`, `M(1)=1`,
  `M -> L` as `q -> infty` --- **gated** (old-audit T1 content).
- Companion `thm:exact-first-adjacent-row` (L1870) AD1/AD2 gated on `n=6,k=3`:
  `M = binom(6,4) = 15`, `Q_sep = max{15, binom(15,2)=105} = 105`; `q > 105`
  => `B^MCA(k+1)=15`; `b>=15 => a*=4`; `6 <= b < 15 => a*=5`.
- **Verdict: `NO ISSUE`** (proof checked). Sole caveat = Input 5's `AUDIT` on
  `P`'s realizability.

### Re-derivation B --- `thm:deep-regime-upper` (L1790) [checked proof]

Statement: linear `C`, min weight `d`, `r = n-a`, `3r <= d-1` =>
`B^MCA(a) <= r+1`.

Proof audit (L1799--1823):
- From two bad slopes `gamma_1, gamma_2` solve the affine system to get
  codewords `c_0,c_1` and errors `e_i = u_i - c_i` supported on `T = E_1 cup E_2`,
  `|T| <= 2r`. **Correct** (subtract the two explanations, divide by
  `gamma_1-gamma_2`).
- For any `gamma in Z`, `p - (c_0 + gamma c_1)` is supported on `<= 3r <= d-1`
  positions hence zero; so `wt(e_0 + gamma e_1) <= r`. **Correct.**
- Case `|T'| >= r+1`: incidence count gives `|Z|(|T'|-r) <= |T'|`, hence
  `|Z| <= floor(|T'|/(|T'|-r)) <= r+1`. I **gated** `floor(s/(s-r)) <= r+1` for
  all `r+1 <= s <= 2r`. **Correct.**
- Case `|T'| <= r`: the written received-word argument ("`S` must meet `T'`")
  is **terse**: read literally it does not exclude the degenerate configuration
  where the received line is already within `r` of a codeword line (`u_i = c_i`
  off `T'`), which would make *every* slope "within distance `r`". The exclusion
  is supplied by the **numerator definition** at L1776--1783: a slope is recorded
  only from a **noncommon** support (project both syndromes to `F^R/V_E`; if the
  second projection is zero, "record nothing"). The degenerate line has both
  syndromes in `V_{T'}`, so it contributes nothing. With that convention each
  recorded slope is pinned by a coordinate of `T'`, giving `<= |T'| <= r` slopes.
- Independent numeric confirmation: **faithful RS--MCA brute force** (constants
  `k=1` over `F_5`, `n=4`, `a=3`, `r=1`, deep regime `3r=3 <= d-1=3`), using the
  noncommon-support definition, gives `max_{(u_0,u_1)} #bad = 2 = min{|Gamma|,
  n-a+1} = r+1` exhaustively over all `5^8` pairs (gated); an `F_7` sample
  (120k pairs) never exceeds `r+1`. This matches `cor:exact-deep-numerator`
  (L1854) equality.
- **Verdict: statement `NO ISSUE` (checked, brute-force confirmed);**
  the `|T'| <= r` proof case is **`OPEN GAP` (exposition)**: it should cite the
  noncommon-support / "record nothing" convention explicitly rather than assert
  "`S` must meet `T'`". Ledger entry L-2.

### Ten-failure-mode checklist (against the sections that own each)

| failure mode | section | result |
|---|---|---|
| missing witness in first-match atlas | `sec:coordinate-atlas` L6435, (A2) | `OPEN GAP` --- exhaustiveness is an input; guarded (`lem:profile-atlas` excludes planted/higher-dim) |
| incorrect image-scale normalization for MI/MA or Sidon | `sec:smooth-circle-domains`, L2929--3160 | `NO ISSUE` --- `def:effective-fourier-payment` bars double-paying an annihilator; MI/MA normalized on `V_g`/`A_eff` |
| unsupported major-arc aggregate | `def:major-arc-aggregate` L2985 | `NO ISSUE` (labeled input; "first-match terminology alone does not imply it", L3006) |
| residual higher-dim balanced core without ray compiler | `rem:balanced-core-exhaustion` L4763 | `OPEN GAP` --- explicitly routed to (RC) or a direct count |
| incomplete profile-envelope comparison with target | (A7); `cor:intro-identity-frontier` L1011 | `OPEN GAP` --- carried as explicit premise |
| unsafe-side lower reserve not crossing target | `sec:frontier`, SB2 L6227 | `NO ISSUE` --- SB2 crosses unconditionally (caveat: `P` realizability, Input 5 `AUDIT`) |
| incorrect first-match disjointization | `lem:first-match-bound` L1526, `prop:exact-support-upper` L1361 | `NO ISSUE` (checked proof: injective noncommon-support map) |
| wrong field denominator / base-vs-extension ledger | `thm:subfield-confinement-full` L1930; `sec:mca-ledger` | `NO ISSUE` --- confinement keeps bad slopes in `B`; `|B|` vs `q` kept separate in SB1 |
| misuse of BSG / quasicube growth | `sec:entropy-role`, `thm:primitive-q` L5548 | statement-level `NO ISSUE` (implication `Sidon payment => Q`; premise labeled). **checked statement only** |
| asymptotic proof vs finite deployed rows | `sec:finite-scope` L6299, `thm:exact-finite-profile-compiler` L6737 | `NO ISSUE` --- finite compiler is exact; "row-sharp" Q target stated inside actual residual, not raw null fiber |

---

## Part 4 --- Mapping table + softness ranking

### #494 five-class inventory -> five hard inputs

| #494 class (label sample) | feeds hard input | supporting audited statement in new draft |
|---|---|---|
| (a) conditional compiler inputs (`def:admissible-sequence`, `lem:first-match-bound`) | #1 atlas, #4 envelope | (A2),(A7); `prop:numerator-bound` |
| (b) Fourier/Sidon payments (`thm:prefix-flatness-power-sum`, `def:sidon-paid-cell`, `prop:high-energy-impossible`) | #2 MI+MA/Sidon | `(MI)`,`(MA)`, `prop:effective-mi-ma-flatness`, `def:sidon-paid-cell`, `thm:primitive-q` |
| (c) major-arc aggregate (`def:major-arc-aggregate`, `prop:major-arcs-are-cells`) | #2 (MA half) | `def:major-arc-aggregate` L2985 |
| (d) profile-envelope comparison (`eq:profile-envelope`, `thm:smooth-quotient-obstruction`) | #4 envelope, #5 lower reserve | `cor:intro-identity-frontier` premise; SB2 bracket |
| (e) ray-compiler (`hyp:ray-compiler`, `prop:q-sp-no-ray`, `prop:pair-ray-multiplicity`) | #3 ray compiler | `hyp:ray-compiler` L6033; `rem:balanced-core-exhaustion` |

**Input with no supporting audited statement of its own beyond the labeled
hypothesis:** #3 (ray compiler) --- the higher-dimensional balanced-core
decomposition has *no* proved statement anywhere; it is entirely `(RC)` or "a
direct ray count". #1 (atlas exhaustiveness) is similar but has a partial
unconditional discharge (`thm:small-effective-dual-closure` when
`Omega=binom(D,a)`).

### Softness ranking (softest = best target for a direct proof/counterexample) [steering payload]

1. **#3 ray compiler.** Sole hypothesis; sharply quantified
   (`J m/H = e^{o(n)}`); the higher-dim balanced core is the one open structural
   object with no supporting statement. A single MDS-circuit case is already
   proved (`thm:single-mds-circuit-ray` L1734, `|Z| <= binom(R+1,2)`) --- extend
   or break the higher-dimensional decomposition here.
2. **#1 atlas exhaustiveness.** Not refutable without a concrete missing-witness
   family; that family (or a proof no such family exists in the structured
   classes) is the attack. Discharged only when one cell is `binom(D,a)`.
3. **#2 image-scale MI+MA/Sidon.** Now three precise inequalities with a proved
   `MI+MA=>flatness` bridge and an unconditional low-`A` discharge --- attackable
   by pushing `thm:small-effective-dual-closure` past `log A = o(|T|)`, or by a
   char-sum counterexample to `(MA)` on a designated major set.
4. **#4 envelope comparison.** Explicit premise, false in general; the tractable
   question is a clean *sufficient* window criterion for identity-dominance.
5. **#5 lower reserve.** Least soft: SB2 already realizes the crossing with
   literal constants; only `prop:simple-pole-lower`'s realizability wants a
   printed hypothesis.

---

## Proposed ledger entries (proposed; NOT applied to the paper)

Per policy no `.tex`/`.pdf` was touched. If the maintainer opens
`experimental/asymptotic_rs_mca_frontiers.md`, format per the
`experimental/asymptotic_rs_mca.md` convention (Source / Status / Paper impact /
Next action).

### Ledger entry L-1 (carried from #494 G-1; still open)
- **Source:** this delta audit; #494 finding G-1.
- **Status:** `OPEN GAP` (exposition; not a mathematical gap).
- **Paper impact:** `def:primitive-first-match-residual` L1500 still closes on
  "the row-specific primitivity certificate used by the analytic and ray
  arguments"; the exclusion list is at L1523--1524.
- **Next action:** inline the named exclusions into the definition, e.g. "...
  carries the certified removal of its named quotient, field-descent, rank,
  planted, and ray-saturation degeneracies (the row-specific primitivity
  certificate)", so it cannot be read as "primitive = no Sidon-heavy fiber".

### Ledger entry L-2 (new; deep-regime proof terseness)
- **Source:** this delta audit, Re-derivation B; verifier deep-MCA gate.
- **Status:** `OPEN GAP` (exposition; statement is correct and brute-force
  confirmed).
- **Paper impact:** `thm:deep-regime-upper` proof, case `|T'| <= r` (L1816
  --1822), asserts "`S` must meet `T'`" without invoking the numerator's
  noncommon-support / "record nothing when the second projection vanishes"
  convention (L1776--1783), which is what actually excludes the degenerate
  within-`r` line.
- **Next action:** add one clause pointing the `|T'| <= r` case at the
  noncommon-support recording rule.

### Ledger entry L-3 (new; bracket lower-leg realizability)
- **Source:** this delta audit, Input 5 / Re-derivation A.
- **Status:** `AUDIT`.
- **Paper impact:** `thm:unconditional-support-envelope-bracket` is titled
  "Unconditional" and SB2 is called placeholder-free; the lower leg `P(a_-)`
  relies on `prop:simple-pole-lower`'s pole-construction realizability, and `P`
  overshoots the true numerator inside the deep regime (where
  `cor:exact-deep-numerator` governs).
- **Next action:** print `prop:simple-pole-lower`'s realizability/regime
  hypotheses next to SB2, and note `P` is used outside the deep regime.

---

## Nonclaims / could-not-verify (for PI spot-check)

- `thm:primitive-q` (L5548) and the BSG/quasicube application: **statement-level
  only.** I did not re-derive the additive-combinatorics internals; the premise
  (Sidon moment payment) is labeled, and #494's T3 already gated the Fourier
  core.
- `thm:small-effective-dual-closure` (L3027) and `thm:exact-partial-occupancy`
  (L3609) are **new**; I checked the EF7-reduction algebra and the
  `log A <= (a-k-1)log|B|` bound, not the full partial-occupancy add-back proof
  (`lem:exact-profile-addback` L7261, `sec:complete-cell-budgets`).
- `prop:effective-mi-ma-flatness` (L3098): checked that MI+MA additively give the
  displayed max-fiber bound; the `A_eff` image-size lower bound
  (`e^{-o(|T|)} A_eff`) I checked at statement level.
- The deep-regime brute force is exhaustive only for `k=1` constants over `F_5`
  (and sampled over `F_7`); it confirms the numerator equality for that family,
  not the general linear-code statement.
- `(MI)`/`(MA)`/`(RC)`/`(FI)` textual occurrence census beyond `(MI)`=28 was not
  re-tabulated per-line (only `(MI)` is gated).

## What was cut (budget rule: Part 3 > 2 > 1)

- **Part 1 granularity:** I did not re-classify all 224 new environments into the
  five-class taxonomy; I classified the 10 load-bearing additions and gated the
  aggregate counts. The (a)--(e) inventory is inherited from #494 (labels
  preserved) rather than re-enumerated row-by-row.
- Sections not line-audited (recorded `OPEN`, no coverage claim):
  `sec:li-wan-details` L6547, `sec:threshold-details` L6639,
  `sec:algebraic-repairs` L7580, `sec:smooth-domain-detail` L7429,
  `sec:circle-domain-detail` L7497, `sec:complete-cell-budgets` L7235.

## Files
- note: `experimental/notes/audits/asymptotic_frontiers_delta_audit.md` (this)
- verifier: `experimental/scripts/verify_frontiers_delta_audit.py` (937 checks,
  `RESULT: PASS`)
- data: `experimental/notes/audits/data/asymptotic_frontiers_delta_audit.json`
- audited: `experimental/asymptotic_rs_mca_frontiers.tex` `@4e3c4ee` vs
  `experimental/rs_mca_entropy_frontiers.tex` `@2b1a7e2`; #494 note
  `entropy_frontiers_submission_audit.md` (branch `thresholds-entropy-frontiers-audit`)
