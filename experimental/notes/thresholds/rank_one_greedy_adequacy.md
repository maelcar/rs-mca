# The adequacy depth law: one pattern reaches the scalar cap through depth 3, fails from depth 4, and capped greedy reaches every depth's scalar cap

## Status

```text
Status: PROVED (T1, B-independence): per class, the single-pattern
        capacity / omega-cap ratio is a PURE trig function of
        (k, top set, r, sign G(s_low)) -- the common factor
        2^{s_low+1} |G| cancels -- so adequacy questions are finite
        PER DEPTH, independent of B.  Anchored: brute Fourier ratios at
        B = 6 match the abstract instances to 1.2e-14.
      + PROVED (T2, by exhaustion, the depth <= 3 law): best >= cap for
        ALL 3-adic instances at k in {1,2,3} (worst ratio exactly 1;
        equality cases proved analytically, strict cases at margin
        >= 0.0230) -- hence for EVERY B, single-pattern rank-one
        emission reaches the scalar cap for every depth <= 3 symmetric
        hierarchy piece.  #820's S5 upgrades from B = 6 computed to an all-B
        theorem at these depths.
      + PROVED (T5, structure is essential): for ARBITRARY real angles
        the reduced inequality already FAILS at m = 3 (deterministic
        witness; ~14% of random m = 3 instances violate) while m <= 2
        holds for ALL angles (the m = 2 case is the exact identity
        |cos(b1+b2)| + |cos(b1-b2)| = 2 max(|c1 c2|, |s1 s2|)).  The
        depth-3 law is base-3 ARITHMETIC, not analytic slack or small
        pattern rank.
      + COUNTEREXAMPLE (T3, depth >= 4): the first violating instance is
        EXACTLY (k, r, top, sG) = (4, 4, {0,1,2}, -1), ratio 0.9910; the
        worst ratio decays with depth -- 0.7229 / 0.5978 / 0.4482 /
        0.3280 at k = 4/5/6/7 (k <= 6 exhaustive in-verifier; k = 7 at
        the pinned worst instance r = 1367, the alternating digit word).
        The violation is REALIZED at B = 6, k = 4 (piece {+-4 mod 81},
        class 101110, brute Fourier).  #820's open question "best >= cap
        at general B" resolves NEGATIVELY at depth >= 4, positively at
        depth <= 3 -- its k <= 3 scan scope was exactly the true law.
      + PROVED (T4, the greedy completion, EVERY depth): credit patterns in
        decreasing |hcube|, CAPPED at the per-class omega-cap sum h_+
        (the cap is what evades #818 E3, which kills only the UNCAPPED
        additive schedule).  Sound by #820 S4's cap; reaches the scalar cap
        always because
            sum_eps |h(sigma_eps)| <= 2^m sum_D |hcube_v(D)|
        (triangle inequality applied to h(eps) = sum_D hcube(D)
        chi_D(eps)), and cap <= sum |h|.  One line, general B and k.
        Verified: 0 failures over all 17820 instances k <= 5 plus the
        exhaustive k = 6 sweep; pattern counts pinned at <= 2 (k <= 5),
        3 (k = 6), 4 (k = 7 worst).  LOCAL WALSH ACCOUNTING IS CLOSED at
        every depth: capped greedy is sound and reaches the scalar cap.
        The proof is universal, however: it uses no rank-one, base-3,
        Sidon, or source structure.  It therefore does NOT certify payment
        to an owned first-match profile cell or a distinct slope.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- ninth packet of the arc (forcing -> typing ->
        reduction -> scope -> compression -> classification -> admission
        arithmetic -> admission soundness -> LOCAL ACCOUNTING CLOSED): a
        substantive interface remains.  One must map credited patterns to
        actual same-owner first-match cells, prove an A4 analytic/Sidon
        payment and, separately, the A6/RC distinct-slope bound, and certify
        the aggregate census.  Admission is therefore NOT grammar acceptance
        alone, and hard input 2 remains OPEN.  Other residuals:
        single-coset/general-profile analogues, genuinely non-hierarchy bands,
        atlas totality, large-q Sidon.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here supplies
        profile payment or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  T1/T4 are general
proofs; T2 and the k <= 6 half of T3 are exhaustive finite checks (the
instance space per depth is finite and B-free, so exhaustion IS proof);
the k = 7 value is a pinned worst instance (not exhaustive).  Verifier:
`experimental/scripts/verify_rank_one_greedy_adequacy.py` (stdlib only,
deterministic, `RESULT: PASS (19/19)`, `--tamper-selftest` catches `5/5`,
~1.6 s).  Machine-readable certificate:
`experimental/data/certificates/rank-one-greedy-adequacy/rank_one_greedy_adequacy.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/rank_one_greedy_adequacy/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `02728b2`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)**;
**`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Consumed packets on their OWN BRANCHES -- **#816 (twisted-coset
classification), #818 (emission arithmetic), #820 (the omega-sound
floor)** (OPEN PRs, NOT yet integrated at base `02728b2`): the rank-one
product law, budgets, argmax schedule, and the omega cap are their
content; every fact used here is RE-DERIVED and RE-VERIFIED
self-containedly (the verifier rebuilds hatf, the cube data, the
G-tables, and the abstract instances from scratch), so nothing depends
on integration order.  T3 resolves #820's stated open question and
CONFIRMS its scan scope (k <= 3) was exactly the domain of validity.

Integrated in-tree packets (consumed and credited, not reproved):
- **The band-uniform packet** (#795): T3's floor and the schedule frame.
- **The fold-charge packet** (#791): the grammar dialect; the reduction
  remains untouched (it operates on flat territory, where one pattern --
  D = empty -- is the whole schedule and adequacy is exact at any depth).
- **The transverse-charge packet** (#776): omega and the accounting.
- **Atlas-totality residual**: unchanged by this packet.

---

## 0. Setup

Chart, classes, `wtil`, `s3`, `G_{k,r}(l)`, symmetric depth-k pieces,
`beta_j = 2 pi r 3^j / 3^k`, budgets, argmax pattern, and the omega cap
`sum_eps h_+` exactly as in #816/#818/#820 (OPEN PRs -- self-contained
here per Interfaces).  Inline pins for a reader without those branches:
base-3 chart `P_i = 3^i` (`0 <= i < B`), `c = 3^B`, `T = P u (c - P)`,
`hatf(xi) = sum_S e^{-2 pi i xi Phi(S)/c}` over size-`B` supports;
classes are parity vectors `v` with unpaired set `U`, signatures
`sigma(eps) = sum_t eps_t 3^{U_t}`, and the class cube function is
`eps -> (1/c) sum_{xi in piece} hatf(xi) e^{-2 pi i xi sigma(eps)/c}`.
Only classes with `s == B (mod 2)` carry weight (`w_s = 0` otherwise) --
the charged-pair counts below quantify over exactly those.  For a class with top set `{j_1 < ... < j_m}
subseteq {0..k-1}` and `sG = sign(G(s_low))`, the ABSTRACT INSTANCE is
the function `eps -> sG cos(sum_i eps_i beta_{j_i})` on `{+-1}^m` with
its even-pattern capacities `2^m prod_i (|sin beta_{j_i}| if i in D else
|cos beta_{j_i}|)`.

---

## 1. Theorem T1: adequacy is B-independent

> **Theorem T1.**  On a symmetric depth-k piece, for any class with
> `G(s_low) != 0`: capacities, budget, and omega-cap all carry the common
> factor `2^{s_low + 1} |G(s_low)|`; the ratios (single-pattern capacity /
> cap, greedy progress / cap) equal those of the abstract instance
> `(k, top set, r, sG)`.  `B` enters only through REALIZATION: which
> `(s_low, sG)` occur (parity and the zero set of `G`).

**Proof.**  Lemma R of #818 (re-derived): `h = 2 G cos(phi_tau)` and
`hcube_v(D) = (-1)^{|D|/2} 2 G prod trig`, both linear in `2 G` with the
low signs contributing the factor `2^{s_low}`.  Divide. `square`

Verified: brute-vs-abstract ratio match `1.2e-14` (B = 6 anchors).
Consequence: each depth `k` presents finitely many instances
(`(2^k - 1) * (3^k - 1) * 2`), so per-depth adequacy is decidable by
exhaustion, once, for all `B`.

---

## 2. Theorem T2: the depth <= 3 law (all B)

> **Theorem T2 (by exhaustion).**  For every instance at `k in {1,2,3}`:
> `best >= cap`, with worst ratio exactly 1.  Hence at EVERY `B`,
> single-pattern rank-one emission (one argmax pattern per class, capped
> per #820) reaches the scalar cap for every depth <= 3 symmetric hierarchy piece.

Verified: all instances `k <= 3` (within the 17820 instances scanned at
`k <= 5`), worst ratios `1.0000/1.0000/1.0000`.  MARGIN STRUCTURE (what
makes float exhaustion honest): of the 268 charged `k <= 3` instances,
148 attain EQUALITY and all 148 are single-sign-nonnegative -- where
equality is PROVED in one line (`h >= 0` gives `|hcube(D)| <=
sum h / 2^m = hcube(empty)`, so the flat capacity is both the maximum and
the cap); the remaining 120 strict instances have minimum relative
margin `0.0230`, more than seven orders above the scan tolerance.
The classification itself is float-safe: no `h` value is ever near zero
at 3-adic angles (`cos(2 pi x) = 0` needs denominator 4, impossible at
3-power denominators -- #816 C4's argument), and the verifier pins the
`|h|`-floor at `|cos(2 pi 7/27)| = 0.0581`; so every tie is certified by
the EXACT `h >= 0` argument, not by floating point.  This
upgrades
#820's S5 from "computed at B = 6" to a theorem at all `B` for
`k <= 3` -- and T3 shows its `k <= 3` scope was not an accident of scan
budget but the exact boundary of the law.

---

## 3. Theorem T3: depth >= 4 fails, with a realized witness

> **Theorem T3 (counterexample).**  The first violating instance (in
> depth, then top-mask, then `r`, then sign order) is
> `(k, r, top, sG) = (4, 4, {0,1,2}, -1)` with ratio `0.9910...`; the
> per-depth worst ratios are
> ```text
> k      : 1..3     4        5        6        7
> worst  : 1.0000   0.7229   0.5978   0.4482   0.3280(pinned instance)
> ```
> (`k <= 6` exhaustive; `k = 7` at the pinned worst `r = 1367`, the
> alternating balanced word `(-1,0,-1,0,-1,0,-1)`).  Realization: at
> `B = 6`, `k = 4`, the piece `{xi == +-4 mod 81}` and class `101110`
> give brute `best 0.0284 < cap 0.0286` (ratio `0.9910`) -- single-
> pattern emission under-collects an actual band piece already at
> `B = 6`, one depth beyond #820's scan.

The decay suggests the single-pattern worst ratio tends to 0 with depth
(COMPUTED trend, no limit claim): deep twisted pieces spread their
positive charge across many patterns, and no single coefficient carries
it.

**Realized census at B = 6, depth 4** (the realized section of the
abstract table): of 958 charged (piece, class) pairs, exactly 10 violate
`best >= cap`, across 7 distinct failing top-configurations; the worst
REALIZED ratio is `0.86405`, attained by the all-top class `001111` on
`{xi == +-10 mod 81}` -- an all-top occupation class, structurally
analogous to (NOT identical with) #818 E5's mandatory resonant instance:
E5's `j*` is a FREQUENCY with all-ones balanced DIGITS, the witness is
an all-top occupation VECTOR -- different objects, same all-ones shape,
and both live where any admission decision must operate.  The abstract worst `0.7229` (top `{0,1,2}`, `r = 71`,
`sG = -1`) is NOT realized at `B = 6`: `G_4(l) > 0` at every
parity-admissible `s_low` there, so no class supplies `sG = -1` --
the abstract table is the B-uniform envelope, the census its `B = 6`
section (realization at other `B` follows `G`'s sign pattern, which
varies with `B`).  Second-`B` insurance: the deep witness (all-ones
class on `{xi == +-10 mod 81}` at `B = 8`) confirms by brute Fourier:
`best 4.52462 < cap 5.23653`, ratio `0.86405` reproducing the `B = 6`
value exactly -- B-independence as T1 requires, at a second brute point
(the l = 19 lesson: guard against single-B artifacts).

---

## 4. Theorem T4: capped greedy reaches every depth's scalar cap

> **Theorem T4.**  The GREEDY schedule -- credit the class's patterns in
> decreasing `|hcube_v(D)|`, accumulating until the omega cap
> `sum_eps h_+` -- is sound (the cap; #820 S4) and reaches the cap on
> every charged class, at every `B` and every depth:
> ```text
> sum_eps h_+ <= sum_eps |h(sigma_eps)| <= 2^m sum_D |hcube_v(D)| ,
> ```
> the second step by the triangle inequality applied to
> `h(eps) = sum_D hcube(D) chi_D(eps)`.  So the total coefficient capacity
> always covers the cap, and greedy stops exactly there.

**Proof.**  The display; greedy exhausts a sum that is at least the
stop value. `square`

Verified: 0 failures over all instances `k <= 5` AND the exhaustive
`k = 6` sweep; the realized `B = 6, k = 4` witness reaches its scalar cap.
Pattern economics (finite pins only): greedy needs at most 2 patterns at
`k <= 5`, 3 at `k = 6`, and 4 at the pinned `k = 7` instance.  These
computations do not give a uniform all-depth subexponential pattern
census; a general `m`-cube can expose up to `2^m` Walsh patterns.

With #816 + #818 + #820 + this packet, rank-one greedy emission on
SYMMETRIC hierarchy pieces is classified, arithmetized, sound, and
adequate as **local scalar bookkeeping**.  The displayed proof is the
universal Walsh triangle inequality and uses none of the rank-one or
base-3 structure.  Consequently it does not establish the governing
profile-payment interface: an actual same-owner first-match cell, an A4
analytic payment, the separate A6/RC or direct-ray distinct-slope bound,
and an aggregate census remain mathematical obligations.

---

## 5. Theorem T5: the 3-adic structure is essential

> **Theorem T5.**  (a) For `m <= 2` the reduced inequality
> `2^m max_{even D} prod(w) >= sum_eps (sG cos(sum eps beta))_+` holds
> for ALL real angles; the `m = 2` case is the exact identity
> `|cos(b1+b2)| + |cos(b1-b2)| = 2 max(|cos b1 cos b2|,
> |sin b1 sin b2|)`.  (b) For `m = 3` it FAILS at general angles:
> deterministic witness `b = (5.524, 5.474, 2.378)`, `sG = -1`, with
> `LHS 2.904 < RHS 4.272` (margin far above float noise); roughly 14%
> of random `m = 3` instances violate.  Yet ALL 3-adic instances at
> `k = 3` (which allow `m <= 3`) satisfy it (T2).

**Proof.**  (a) `m = 1`: `cos` is even, so the two cube values are
equal, the function is constant, and the flat capacity equals the cap
whenever positive.  `m = 2`: over the two distinct values
`a = cos(b1+b2)`, `b = cos(b1-b2)` with `a + b = 2 cos b1 cos b2` and
`b - a = 2 sin b1 sin b2`, sign case analysis gives
`max(|a+b|, |a-b|) >= a_+ + b_+` with equality structure yielding the
displayed identity.  (b) is the witness, verified in-verifier. `square`

**Reading.**  The depth-3 law is NOT a small-`m` analytic fact --
general `m = 3` angles already break it.  It is the base-3 arithmetic
of the angle towers `beta_j = 2 pi r 3^j/3^k` that closes exactly the
first three levels; this preempts any "low pattern rank implies
adequacy" misreading of T2.

---

## Nonclaims

- **NOT a profile-payment theorem**: this packet constructs no actual
  first-match `Z_i^circ`, no admissible bound `U_i`, no same-owner atlas
  cell or A4 analytic/Sidon payment, and no separate A6/RC or direct-ray
  distinct-slope bound.  A scalar cap must not be promoted to any of
  those semantic interfaces.
- **T2 and T3 (k <= 6) are proofs by finite exhaustion of B-free
  instance spaces**; the `k = 7` worst is a pinned instance, not an
  exhaustive depth (its exhaustive sweep lives in the scout data, not
  the verifier).  No claim is made about worst-ratio limits as
  `k -> infinity` beyond the computed trend.
- **Realization granularity**: T2/T3/T4 quantify over the abstract
  instances; which instances are realized at a given `B` depends on
  `G`'s zero set and parity (T1).  The exhibited witness settles
  realization at `B = 6, k = 4`; no claim that EVERY instance is
  realized at every `B`.
- **Symmetric pieces only** (the house band primitive); single-coset
  and general-profile analogues follow from the same reduction but are
  not scanned here.
- **NOT a proof of admission**: both a grammar rule and the semantic
  source-to-cell/profile-payment bridge remain open.  The latter cannot
  be reduced to a syntactic acceptance decision.
- **No uniform pattern-count theorem**: the counts through `k = 7` are
  finite pins, not an all-depth subexponential schedule bound.
- **Base 3 only**; floats under exact Parseval + Lemma-N guards; fence
  (N1) respected.

## Consumers

- **#820 (the omega-sound floor)**: its S5 open question is RESOLVED
  (split verdict: theorem at k <= 3, false from k = 4); its corrected
  rule should be read with the greedy schedule as the locally adequate
  scalar form.
- **The admission decision (#791 Sec 5, #716 Sec 7.1, #818 Sec 6)**:
  rank-one GREEDY emission with the omega cap specifies the local charge
  rule, but admission still requires a same-owner first-match
  source-to-cell/profile-payment theorem.
- **The band-uniform packet (#795)**: its T3 schedule frame gains the
  local scalar form (greedy-to-cap); its semantic middle-band payment is
  not thereby complete.
- `rs_mca_thresholds.tex`: any remark after the PO4 material must say --
  "single-pattern emission reaches the scalar cap exactly up to
  depth 3 (B-independent law; first failure at depth 4, ratio 0.991,
  realized at B = 6); greedy credit capped at the positive part reaches
  every depth's scalar cap by the universal Walsh triangle
  inequality" -- and must not infer profile payment or an all-depth
  handful-of-patterns bound.  Visible hypotheses: #749-corrected class,
  base-3 chart, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_rank_one_greedy_adequacy.py
# -> RESULT: PASS (19/19)
python3 experimental/scripts/verify_rank_one_greedy_adequacy.py --tamper-selftest
# -> tamper-selftest: caught 5/5
python3 experimental/scripts/verify_rank_one_greedy_adequacy.py --emit-certificate \
  experimental/data/certificates/rank-one-greedy-adequacy/rank_one_greedy_adequacy.json
cd experimental/lean/rank_one_greedy_adequacy && lake build
# -> Build completed successfully
```
