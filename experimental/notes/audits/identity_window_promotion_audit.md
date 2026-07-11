# Identity-window criterion (#542) --- promotion-gate audit vs frontiers tex

**Status:** `AUDIT`. **This is an adversarial SELF-AUDIT.** The criterion under
audit (PR #542, `envelope_identity_window.md` + `verify_envelope_window.py`) is
our own team's packet (contributor line: Holm Buar / holmbuar, the same as
#542). Because a self-audit cannot borrow the credibility of an independent
check, this audit compensates two ways, both mandatory:

1. **Adversarial protocol.** The goal is to *break* the criterion, not defend
   it: construct rows that pass the window test while identity-dominance fails
   (soundness attack), and rows that fail it while dominance holds (tightness
   probe). A soundness hit is `COUNTEREXAMPLE_NEW_FLOOR` and blocks promotion.
2. **Independent recomputation.** Every number is recomputed from scratch in a
   fresh verifier, `experimental/scripts/verify_identity_window_audit.py`, which
   shares **no** code path with #542's `verify_envelope_window.py`. Where #542
   checked the window edges with a floating-point brute scan, this audit checks
   them in **exact rational arithmetic** (`fractions.Fraction`, entropy value
   `h` and crossing `s` treated as free positive rationals), so the window
   algebra carries zero floating error. `RESULT: PASS (7160 checks)`,
   ~0.9 s under `ulimit -v 2097152`.

**Maintainer trigger.** agents-log 2026-07-10 "Identity-window and finite-prize
theory packets": *"Audit the identity-window criterion against
`experimental/asymptotic_rs_mca_frontiers.tex` before promotion."* Target file
7913 lines (worktree base `e190193`; byte-equal on the audited environments to
the `4e3c4ee` the note cites).

**Credit.** LegaSage **#520** (`profile_envelope_vs_target.md`, `hard_input:"d"`)
independently audited the envelope *formula* `E=1+(n-a+1)+sum(1+barN)` at
statement level, verdict `NO ISSUE`, and was explicit that *"identity-dominant
window holds at deployed scale"* is a `does_not_assert`. This audit consumes
that boundary: #520 pins the formula and brackets; the present audit stresses
the **domination criterion** #542 built on top, and that is exactly where the
defect below lives --- in territory #520 explicitly declined to certify. PR
**#524** (`asymptotic_frontiers_delta_audit.md`) verdicted input (d) `OPEN GAP`
and named "a clean *sufficient* window criterion" as the tractable target; this
audit checks whether #542 delivered a *promotable* one.

---

## VERDICT (headline)

**NOT promotion-ready as written. One blocking defect; one-line atomic repair.**

- **Re-derivation outcome (the headline either way): every constant of #542 is
  reproduced EXACTLY by independent hand re-derivation** from the tex's QR6
  pigeonhole scale --- `e_c=(1/c)(H2-lambda*s)`, `kappa_low=(c-1)/(c-lambda)`,
  `kappa_high=1/lambda`, wall margin `((1-lambda)/c)H2`. No constant, sign, or
  exponent differs from #542. The arithmetic core is sound.
- **The blocking defect is not in a constant --- it is in the Rung-3
  *reduction* to a single "worst competitor".** For a row carrying more than one
  complete-fiber folding (which `(A7)` says is the generic case --- it sums over
  *"all quotient subfields"*), #542's rule *"the binding competitor is the row's
  cheapest folding `c_min` with its deepest field drop `lambda_min`"* is
  **unsound**: a deeper field drop carried by a folding of **non-minimal degree**
  is silently ignored, and it can exponentially break dominance in a window the
  criterion declares safe. This audit exhibits it and censuses 3096 such hits.
- **The repair is atomic and exact:** replace the single worst-competitor window
  by the **per-folding intersection** --- the row is identity-dominant iff `s`
  avoids the *union* of every folding's failure band. With this one change the
  criterion becomes sound (0 soundness hits, verified) and every #542 constant
  stands. The `lambda=1` no-field-drop corollary --- #542's main promoted claim
  --- is **unaffected and sound**.

---

## Task 1 --- Extraction fidelity: definitions vs the tex (source of truth)

Every definition of the criterion was re-extracted and checked against the tex's
own labels and current line numbers. **No material normalization drift**: base
of `H2` (binary), `beta=log2|B|`, `c` = complete-fiber degree, `lambda_c` a
subfield-degree ratio --- all internally base-2-consistent and faithful. Five
minor *citation-labeling* refinements (none change the math):

| # | #542 note says | Tex source (current line) | Finding |
|---|----------------|---------------------------|---------|
| F1 | cites the exponent as **QR8**: `(1/n)log2 barN_{c,r} = (1/c)(H2-g*beta)+(g*beta/c)(1-lambda_c)` | verbatim **QR8** `eq:qr-comparison-general` L3911-3914 is a *plain-log, un-normalized* two-term identity `(1/c)log(C(n,a)|B|^{-w})+(w/c)log(|B|/|B_c|)+o(n)`; `lambda_c` appears only in **QR9** L3917-3924 as `(1-lambda_c)` multiplying `h(alpha)/c` | The note's formula is the correct **per-symbol base-2 normalization** of QR8 (using `w=gn`, `log2|B|=beta`, `log(|B|/|B_c|)=(1-lambda_c)log|B|`) --- verified identical (verifier R1). But it should be cited as *"QR8 normalized (base-2, per-symbol), equivalently QR9 at the crossing"*, not verbatim QR8. `NO ISSUE` for math; label refinement. |
| F2 | annotates `lambda_c in (0,1]` | source (L3918) states only `lambda_c=log|B_c|/log|B|`; the range string `(0,1]` is **not in the tex** | True (subfield ratio in `(0,1]`, `=1` iff `B_c=B`) but note-added. Flag as derived. |
| F3 | writes `(IDW)` as if a tex tag | no `(IDW)` label exists; the domination bound `E_n(a)<=e^{o(n)}(1+n-a+barN_1(a))` is **untagged** (inside `cor:intro-identity-frontier` L1014-1017), and `identity-dominant` is a prose def L1004-1008 | `(IDW)` is the note's own shorthand; harmless if not represented as canonical. |
| F4 | uses `(1/n)log2 barN_1 = H2(rho+g)-beta g+o(1)` | `eq:target-entropy` L6108-6113 is the **un-normalized** `log2 barN_1 = n(H2-beta g)+O(log n+beta_n)` | The `(1/n)` form needs `beta_n=o(n)`, which the paper's regime supplies (tower has `log|B|=o(n)`). Consequence, not verbatim. |
| F5 | line refs at base `4e3c4ee` (`eq:profile-envelope` L858-862, cor L1010-1050, QR8 L3911-3916, obstruction L3985) | current: L862, L1011, L3911-3914, L3986 | Minor line drift only; labels resolve. |

**Extraction-fidelity verdict: NO MATERIAL DRIFT.** The criterion's objects match
the tex; F1-F5 are citation refinements for the promoted text.

---

## Task 2 --- Hypothesis visibility (the #524 pattern)

For each criterion claim, is every hypothesis visible at the point of use in the
tex consumer (`cor:intro-identity-frontier` L1011 and `(A7)` L946-952)?

| Claim | Hypotheses at point of use | Visible? |
|-------|----------------------------|----------|
| Two window bounds `kappa_low,kappa_high` | (i) ledger-admissibility `(A2)/(A4)` for the *upper* (domination) direction | **Visible** --- carried in `(A7)` and flagged CONDITIONAL by #542 |
| | (ii) the row's folding data `(c_i,lambda_i)` | **Visible** --- `(A7)` names the scaled quotient coefficient fields |
| | (iii) **that a single `(c_min,lambda_min)` represents the row** | **SILENT --- OPEN GAP.** `(A7)` sums over *all* quotient subfields; the note's Rung-3 collapses them to one pair with no stated hypothesis. This is the hole the soundness attack drives through. |
| `lambda=1` global-dominance corollary | *every* folding has `lambda=1` (no proper scaled-subfield folding) | **Visible & correct** --- #542 states "no scaled-subfield folding". |
| Band-membership replacement (L-W-2) | `(A2)/(A4)` + single-vs-intersection (iii) | `(A2)/(A4)` visible; single-folding **silent** (same gap). |
| `e_c` wall (crossing in band, `lambda<1`) | none beyond `(c,lambda)` being a *real* folding | **Visible**, unconditional (QR6). |

**Summary:** one silent hypothesis --- the single-folding reduction --- is the
promotion-blocking visibility gap. Everything else is visible.

---

## Task 3 --- Independent re-derivation from the tex (constants MATCH #542)

Re-derived by hand from `QR6` (`eq:qr-natural-scale` L3886-3889),
`barN_{c,r}(w)=C(N-|phi(R)|,m)|B_phi|^{-floor(w/c)}`, `N=n/c`, `m=(a-r)/c`,
`r<c` fixed, `|phi(R)|=O(1)`:

```
(1/n) log2 barN_{c,r}(w)
   = (1/c)(1/n)log2 C(N,m)  -  (floor(w/c)/n) log2|B_phi|  + o(1)
   = (1/c) H2(alpha)  -  (g/c) lambda_c beta  + o(1)          [m/N->alpha, w=gn]
   = (1/c)[ H2(rho+g) - lambda_c * g * beta ]                  =: e_c.
```
with `H2(alpha)=h`, `g*beta=s`, so **`e_c=(1/c)(h-lambda*s)`**. Solving
`(DOM) e_c<=max(0,e_1)`, `e_1=h-s`:
- **Case A** `h>=s`: `(h-lambda s)/c <= h-s  <=>  s(c-lambda)<=h(c-1)  <=>  s <= (c-1)/(c-lambda) h`. So **`kappa_low=(c-1)/(c-lambda) in (0,1]`**.
- **Case B** `h<s`: `(h-lambda s)/c <= 0  <=>  s >= h/lambda`. So **`kappa_high=1/lambda >= 1`**.
- **Wall margin** at the crossing `s=h` (`e_1=0`): excess `= e_c - 0 = (1/c)(h-lambda h) = ((1-lambda)/c) h`; for `c=2,lambda=1/2` this is `h/4`, byte-matching `thm:smooth-quotient-obstruction`'s exponent (L4016-4021, `\frac14 h(alpha)`).

**Every constant equals #542's** (verifier R1: exact over a rational
`(h,s,c,lambda)` grid; R1b: window edges solve `e_c=max(0,e_1)` exactly; R2: the
finite-`n` `QR6` exponent converges to `(1/c)(h-lambda s)` with monotonically
shrinking error). **No discrepancy in any constant or exponent.**

---

## Task 4 --- Adversarial attack

### 4a. Soundness attack (COUNTEREXAMPLE_NEW_FLOOR) --- the blocking defect

**Target:** #542 Rung 3 (L212-215): *"e_c=(h-lambda s)/c is decreasing in c
(numerator>=0) and in lambda, so the binding competitor is the row's cheapest
folding c_min with its deepest field drop lambda_min. Write
(c,lambda)=(c_min,lambda_min)."* --- and the promoted ledger L-W-1 (L341-343),
which instantiates the window at that single pair.

**The logical error.** `e_c` is decreasing in `c` *at fixed lambda* and
decreasing in `lambda` *at fixed c*. It does **not** follow that the joint
minimum `(min c, its lambda)` maximizes `e_c` over the row's *actual* folding
pairs `{(c_i,lambda_i)}`: a folding of **higher** degree with a **much deeper**
drop can have a strictly larger `e_c`. The true worst competitor is
`argmax_i e_{c_i}(g)`, which varies with `g` and need not be the cheapest
folding.

**Concrete refutation (hand-checked, and auto-found by the census).** Row with
two foldings `(c=2,lambda=1/5)` and `(c=3,lambda=1/10)` --- both realizable as
proper-subfield drops of e.g. `B=F_{2^10}` (subfield exponents `1/10,1/5,1/2`).
At `s=5h` (i.e. `g*beta=5*H2`):
- #542's rule picks `c_min=2`, its deepest drop `lambda=1/5`; window `(2,1/5)`
  has `kappa_high=5`, so `s>=5h` reads as **DOMINANT**.
- But folding `(3,1/10)` has `e_c=(h-(1/10)(5h))/3 = (h-h/2)/3 = h/6 > 0`, while
  `max(0,e_1)=max(0,h-5h)=0`. So the complete envelope exponentially exceeds the
  identity RHS: **dominance FAILS** (QR6 gives this unconditionally).

The window test passes while dominance fails --- a genuine soundness hit.

**Census (verifier section S, exact rationals).** Over 132 two-folding rows x
216 `(h,s)` points = 28512 tests:

| reading of the criterion | soundness hits (says DOMINANT, truth = FAIL) |
|---|---|
| **RED-a** = #542's literal *"cheapest folding, its deepest drop"* | **3096** |
| RED-c = independent-min *(min c combined with min lambda)* | **0** |
| **INT** = per-folding intersection (the repair) | **0** |

RED-a is unsound; the intersection repair is exact (matches `dom_true`
definitionally: `INT <=> for all i: e_{c_i}<=max(0,e_1)`).

**Classification: `COUNTEREXAMPLE_NEW_FLOOR` against the criterion (blocking).**
Honest scope: this is a defect in the *criterion's reduction step and its
promoted ledger text*, **not** a new obstruction floor in the paper --- the
paper's theorems are untouched, and #542's own Corollary C3 (which quantifies
over *"every competitor"*) is correct. The bug is only in collapsing "every
competitor" to one pair.

### 4b. Tightness probe (measures conservatism only)

RED-c (independent-min) never claims false dominance but **over-declares
failure**: e.g. the fictitious pair `(2,1/10)` for the row above marks
`s in (0.526h, 0.667h)` as band-membership-failure although both real foldings
are dominated there. Harmless for soundness (safe side), a measured
conservatism. The **INT repair has no tightness loss** (exact). Recorded as
tightness, not a defect.

### 4c. Placement of the paper's own obstruction (verified exactly)

`thm:smooth-quotient-obstruction` `=` `(c=2,lambda=1/2,s=h)` (verifier P):
- band `= (kappa_low h, kappa_high h) = (2/3 h, 2h)`; `s=h` is **strictly
  interior** --- confirmed at every tested `h`. #542's "one point of the failure
  band" placement is **exact**.
- the excess `e_c-max(0,e_1)` **peaks at `s=h`** with value `h/4`, and is
  *strictly smaller* just inside the band on both sides --- so `s=h` is the
  **excess-maximizer**. #542's prose *"sits at the band's centre"* (L293) is
  loose: the geometric midpoint is `(2/3+2)/2 h = 4/3 h != h`. Wording nit,
  flagged; the math ("deepest point" = max excess) is right.

### 4d. Generous-target regime (verified)

For `lambda<1`, `tau>=tau0:=F(g_low)` pushes the right crossing `g_T` into the
LOWER window (verifier T): `g_low<g*` strictly and `tau0>0` at every tested
`(rho,beta)`, `g_T<=g_low`, and `s_T<=kappa_low h_T`. #542's target-threshold
claim holds **for a single folding**. Multi-folding extension: the row needs
`tau>=max_i tau0^i` (the deepest-drop folding sets the threshold) --- a
one-symbol change to the same repair.

---

## Task 5 --- Band-membership replacement rule (L-W-2) conservativity

#542's L-W-2 proposes replacing `(A7)`'s guard *"it is not replaced by the
identity term unless that comparison is proved for the row"* with the
band-membership test.

- For a **single** actual folding the test is **exact** (`prim==closed` at 4608
  exact rational points, verifier W): replacing is justified iff dominance holds,
  given `(A2)/(A4)`. Conservative (indeed tight) --- `NO ISSUE`.
- For a **multi-folding** row under L-W-1's single-pair form, band-membership can
  read "dominant" off one folding while another breaks it, i.e. it would replace
  the envelope by the identity term when **not** justified --- **NOT
  conservative** (this is the same soundness hit).

**Verdict:** L-W-2 is conservative **iff** the intersection repair is applied
(require every folding's band-membership). As written (single pair) it is not
conservative for the generic multi-folding row. Same blocker, same one-line fix.

---

## Per-claim label ledger

| # | Claim | Verdict |
|---|-------|---------|
| C1 | `e_c=(1/c)(H2-lambda*g*beta)`; `=h/4` at the CE crossing | `NO ISSUE` (re-derived exact; cite as normalized-QR8/QR9, F1) |
| C2 | envelope exponent `=max(0,e_1,max e_c)`; competitors = field-drop quotients | `NO ISSUE` (reduction lemma; upper dir CONDITIONAL on (A2)/(A4), as #542 labels; PI re-derivation still wanted) |
| C3 | `(IDW)<=>(DOM)` for **every** competitor | `NO ISSUE` (correctly universally quantified) |
| C4 | single-competitor window `{s<=kappa_low h} U {s>=kappa_high h}` | `NO ISSUE` (exact, 4608 rational points) |
| **RED** | **Rung-3 reduction / L-W-1: one pair `(c_min,lambda_min)` represents a multi-folding row** | **`COUNTEREXAMPLE_NEW_FLOOR`** (3096 hits; blocks promotion; repair = intersection) |
| C5 | `lambda=1` (no scaled-subfield folding) `=>` global dominance, corollary unconditional | `NO ISSUE` (sound; unaffected by RED --- it is the all-`lambda=1` case) |
| C6 | failure band; envelope provably exceeds identity there | `NO ISSUE` **per actual folding** (QR6 unconditional); `OPEN GAP` if the pair is fictitious --- fixed by intersection |
| C7 | zero-target crossing `s=h` strictly in band for `lambda<1` (WALL) | `NO ISSUE` (verified; "band centre" -> "excess-maximizer") |
| C8 | `tau>=tau0>0 =>` crossing in lower window | `NO ISSUE` single folding; multi-folding needs `tau>=max_i tau0^i` |
| C9 | `F_{p^2}` census: quotient cell carries more than identity | `NO ISSUE` / `AUDIT` (independent tower: `quo>barN1` exact; toy scope) |
| C10 | no new obstruction floor in the *paper* beyond smooth-quotient-obstruction | `NO ISSUE` / `AUDIT` (true; the RED counterexample is against the *criterion*, not the paper) |

---

## Blocking defect + atomic repair + corrected ledger entries

**Blocking defect (RED):** the single-worst-competitor reduction (#542 Rung 3
and ledger L-W-1) is unsound for rows with more than one complete-fiber folding
--- the generic case under `(A7)`.

**Atomic repair:** state the criterion per folding and intersect.
`e_c=(1/c)(h-lambda s)` maximized over the row's *actual* pairs `{(c_i,lambda_i)}`
is the binding exponent; the safe region is the **intersection** of per-folding
safe windows, i.e. the failure region is the **union** of per-folding bands.

**Corrected, ready-to-paste ledger entries** (for
`experimental/asymptotic_rs_mca.md`; NO tex edits):

> **Entry L-W-1' (identity-dominance window, corrected).** After
> `cor:intro-identity-frontier` (L1011): let a ledger-admissible row carry
> complete-fiber foldings `{(c_i,lambda_i)}_i`, `c_i>=2`,
> `lambda_i=log|B_{c_i}|/log|B| in (0,1]` (a subfield-degree ratio; `lambda_i=1`
> if folding `i` lands in no proper scaled subfield). Writing `h=H2(rho+g)`,
> `s=g*beta`, `(IDW)` holds (given `(A2)/(A4)` admissibility) iff **for every
> folding** `s <= ((c_i-1)/(c_i-lambda_i)) h` or `s >= (1/lambda_i) h`;
> equivalently `s` avoids the union of failure bands
> `Union_i ( ((c_i-1)/(c_i-lambda_i)) h , (1/lambda_i) h )`.
>
> **Entry L-W-2' (band-membership guard, corrected).** Replace `(A7)`'s "unless
> that comparison is proved for the row" by: the identity term may replace the
> envelope on an agreement window iff **every** folding's band-membership test
> reports dominant on that window (the per-folding intersection). This is exact
> given `(A2)/(A4)`; it is not conservative if applied to only one folding.
>
> **Entry L-W-3' (wall + sufficient conditions).** (i) For each folding with
> `lambda_i<1`, the zero-target crossing `s=H2` lies strictly inside band `i`
> (margin `((1-lambda_i)/c_i)H2>0`, maximal excess); so the corollary's
> zero-target identity specialization is unconditional **only** when *every*
> folding has `lambda_i=1` (e.g. a prime image field). (ii) Otherwise it is
> unconditional for generous targets `tau_n >= max_i tau0^i`,
> `tau0^i=F(g_low^i)>0`.

**Promotion status:** `NOT READY`. Promotable after L-W-1'/2'/3' replace
L-W-1/2/3 (single-line change: "cheapest folding" -> "every folding /
intersection"). With that change all #542 constants stand and the `lambda=1`
corollary (the main unconditional win) is delivered.

---

## Flagged for PI re-derivation (ranked)

1. **The intersection repair is the whole finding** --- re-derive that
   `max_i e_{c_i}(g)` (not `e_{(min c, min lambda)}`) is the binding exponent, and
   that `dom_true <=> per-folding intersection`. One page; the audit's verifier
   proves it over an exact rational grid (0 hits), but a human should confirm the
   quantifier logic before the corrected ledger is promoted.
2. **`(A7)`'s multiplicity** --- confirm at the tex that a single received line
   genuinely admits several foldings of differing `(c,lambda)` (L946-952 "all
   quotient subfields ... all profile fields" strongly implies yes). If instead
   the paper guarantees a unique folding class per row, that hypothesis must be
   printed --- then L-W-1 (single pair) is sound but only under that stated
   restriction.
3. **F1 citation** --- the promoted formula should read as *"QR8 normalized,
   equivalently QR9 at the crossing"*, since verbatim QR8 (L3911) is plain-log
   and `lambda_c`-free.

---

*Reproduce:* `python3 experimental/scripts/verify_identity_window_audit.py`
(stdlib-only, exit 0 on all-pass; sections R/W/S/P/T/E recompute every number
above independently of #542's verifier).
