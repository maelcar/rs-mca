# Emission arithmetic on the rank-one family: exact budgets, the overdraw wall, and the widened primitive

## Status

```text
Status: PROVED (Lemma R, reality + parity): G_{k,r} is REAL for every
        (k,r) -- the a <-> -a digit pairing (s3(-a) = s3(a)) folds the
        character sum into cosines -- so on EVERY single coset
        chat_v(D) in i^|D| R, and on symmetric pieces {r, 3^k - r} the
        cube data is fully explicit and real:
            h(sigma_eps) = 2 G(s_low) cos(2 pi r tau(eps_top)/3^k),
            chat_v(D)    = (-1)^{|D|/2} 2 G(s_low) prod_top trig  (|D| even),
        with odd-|D| vanishing (= the band-uniform packet's T2 symmetry,
        now in closed form).
      + PROVED (E1, budgets): the cube ell^1 budget of T3's floor is
        closed-form on hierarchy pieces; on a single coset
        |h(sigma)| == |G(s_low)| identically (unimodular character), so
        the budget is 2^s |G(s_low)| exactly.
      + PROVED (E2 + E3, schedules): T3's one-pattern-per-class rule with
        the ARGMAX pattern is the optimal sound schedule, computable from
        the G-table in closed form (single coset: coordinate-wise;
        symmetric piece: flip-weakest even restriction); paying ALL
        patterns OVERDRAWS the budget -- PROVED > 1 on every twisted-top
        single-coset class (factor prod(|sin|+|cos|) in (1, 2^{|top|/2}]);
        on symmetric pieces the ratio ranges below and above 1, with the
        strict overdraw confined to |top| >= 2 classes and the extremal
        ratio EXACTLY 2 at (k,r,v) = (3,10,111111) (B = 6 COMPUTED pin).
        One overdrawing class suffices: this closes the band-uniform
        packet's named design point FOR HIERARCHY PIECES -- there is NO
        sound additive multi-pattern schedule; the per-class cap is
        necessary, not stylistic.
      + PROVED (E4, the primitive must widen): symmetric depth-1 pieces
        are FLAT-EXACT (h is class-constant; flat-cube emission pays the
        FULL budget -- the primitive suffices there, exactly).  From
        depth 2 the twisted pieces are NOT flat (Danny's #805 instance),
        so #791's flat-cube rule is INAPPLICABLE to them (they fail its
        flatness certificate); the relaxed D = empty-only emission
        collects as little as 0.102 of the optimum at k = 2 and 0.010 at
        k = 3 (COMPUTED pins; share = flat coeff / argmax coeff).  The
        maximal band and all subgroup-cylinder unions remain the flat
        boundary case (the exactness-of-the-classification is COMPUTED,
        see E4(c)).
        WIDENED PRIMITIVE: rank-one emission defines the capped scalar-credit
        candidate min(2^s |chat_v(D*)|, sum h_+) at the argmax pattern D*
        on every hierarchy (piece, class) account, certificate = the #816
        G-table + trig factors.  It subsumes flat-cube exactly where flat-cube
        applies; source-to-cell and profile payment remain separate.
      + COMPUTED (E5, the mandatory instance): the transverse-charge
        resonant residue j* = (c-1)/2 is the ALL-ONES digit word:
        s3(j*) = B and j* == (3^k-1)/2 mod 3^k -- maximally twisted at
        EVERY depth; |hatf(j*)| >= 0.70 M re-pinned.  Flat-cube emission
        processes its band only to hierarchy depth 1; any deeper
        localization (where the poly certificates live) needs the
        widened primitive.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- seventh packet of the arc (forcing -> typing ->
        reduction -> scope -> compression -> classification ->
        LOCAL SCALAR EMISSION ARITHMETIC): the rank-one cube data,
        coefficient budgets, and capped schedule are now closed-form.
        This does not close admission: no named mode is mapped to an actual
        same-owner first-match cell, no A4 analytic/Sidon payment or
        separate A6/RC distinct-slope bound is proved, and no aggregate
        subexponential cell/schedule census is certified.  Input-2
        residual: that semantic bridge; a grammar rule for the resulting
        payment; genuinely non-hierarchy bands; atlas totality; and
        large-q Sidon.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays
        or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Reality, the closed
forms, and the budget identities are proved at general `B`; the extremal
constants (overdraw `== 2`, the share floors) are COMPUTED pins at `B = 6`.
Verifier: `experimental/scripts/verify_rank_one_emission_arithmetic.py`
(stdlib only, deterministic, `RESULT: PASS (20/20)`, `--tamper-selftest`
catches `7/7`, ~0.2 s).  Machine-readable certificate:
`experimental/data/certificates/rank-one-emission-arithmetic/rank_one_emission_arithmetic.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/rank_one_emission_arithmetic/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `02728b2`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)**;
**`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Consumed packet on its OWN BRANCH -- **the twisted-coset packet (#816,
`twisted_coset_cube_spectrum.md`; OPEN PR, NOT yet integrated at base
`02728b2`)**: its rank-one product law and G-table are THE input, and
every consumed fact is RE-DERIVED and RE-VERIFIED self-containedly here
(Lemma R re-proves what it uses; the verifier rebuilds the G-tables from
scratch and checks all closed forms against literal brute Fourier
inversion), so nothing in this packet depends on #816's integration.
Lemma R sharpens its C3 (reality holds at every k, not only k = 1, by
the same negation symmetry its Lean stub shadows).

Integrated in-tree packets (consumed and credited, not reproved):
- **The band-uniform packet** (#795, `band_uniform_cube_reduction.md`):
  T3's floor and its "one per class" clause get their converse here (E3:
  the cap is necessary); its Sec-3 design point ("a canonical
  multi-pattern payment SCHEDULE is left ... for the admission decision")
  is resolved only at local scalar schedule-shape scope on hierarchy
  (piece, class) accounts (E2/E3); its Sec-4 open piece 2
  (middle-width certificate compression for structured band families) is
  answered for hierarchy families by #816's G-table, consumed here as the
  emission certificate.
- **The fold-charge packet** (#791, `fold_charge_localization.md`): its
  flat-cube primitive and maximal-band reduction are the boundary case
  (E4); nothing in its (=>)/(<=) argument is modified.
- **The transverse-charge packet** (#776,
  `transverse_charge_obstruction_sidon_paired.md`): its resonant
  spectrum j* is located in the hierarchy (E5) -- the mandatory test
  instance is maximally twisted at every depth.
- **The cylinder packet (#798/#805-corrected)**: V7's failing-band
  decomposition is where the per-piece arithmetic applies.
- **Atlas-totality residual**: unchanged by this packet.

---

## 0. Setup

Chart, classes, signatures, `wtil`, `s3`, `G_{k,r}(l)`, `tau(eps_top)`,
`beta_t = 2 pi r 3^{U_t-(B-k)}/3^k`, and the rank-one product law exactly
as in the twisted-coset packet (#816, OPEN PR -- self-contained here per
Interfaces), Setup and Theorems A/B; `e(x) = e^{2 pi i x}`.  A **symmetric depth-k piece** is `K_{k,r} u K_{k,3^k-r}`
(`3^k` not dividing `2r`); the **maximal band** is `Z_c \ {0}`.  An
emission rule "pays" per (class, pattern) as in band-uniform T3:
`2^s |hcube_v(D)|` against the class's cube `ell^1`
`sum_eps |h(sigma_eps)|`.

---

## 1. Lemma R: every G is real, and symmetric pieces are explicit

> **Lemma R.**  (a) `G_{k,r}(l) = 3^{-k} [wtil(l) + sum_{a=1}^{(3^k-1)/2}
> 2 cos(2 pi a r/3^k) wtil(s3(a)+l)]` is REAL for every `(k, r)`.
> (b) On every single coset, `chat_v(D) in i^{|D|} R`.
> (c) On a symmetric piece, for every class `v`:
> `h(sigma_eps) = 2 G(s_low) cos(2 pi r tau(eps_top)/3^k)`, and
> `chat_v(D) = (-1)^{|D|/2} 2 G(s_low) prod_{t in top}(sin beta_t if t in
> D else cos beta_t)` for even `|D| <= |top|`, `= 0` for odd `|D|` and for
> `D` off the top block.

**Proof.**  (a) Pair `a` with `3^k - a`: `s3(-a) = s3(a)` (negation flips
balanced digits), so the two terms are conjugate with equal weight.
(b) Theorem B's product carries `(-i)^{|D|}` times real sines/cosines
times the real `G`.  (c) Sum the two rank-one characters:
`omega^{-r tau} G_r + omega^{+r tau} G_{3^k-r}` with `G_{3^k-r} =
conj(G_r) = G_r` gives `2 G cos(2 pi r tau/3^k)`; the cube transform of
the cosine of a sum factors as in Theorem B, and odd `|D|` picks an odd
number of sines whose `i`-powers leave a pure imaginary that the real sum
kills -- equivalently band-uniform T2's `eps -> -eps` symmetry. `square`

Verified: complex-vs-paired `G` to `7.0e-15`, ALL `(k,r)`; the symmetric
`h` and cube closed forms to `1.6e-14` over ALL `(k, r-pairs, classes,
eps/patterns)` at `B = 6`; odd-`|D|` vanishing `3.2e-15`.

**Consequence for #816's C3:** reality is not a `k = 1` accident; the
purely-imaginary anatomy generalizes to `chat in i^{|D|} R` at every
depth.

---

## 2. Theorem E1: the budgets are closed-form

> **Theorem E1.**  On a single coset, `|h(sigma)| = |G(s_low)|` for EVERY
> signature (the character is unimodular): the class cube `ell^1` is
> `2^s |G(s_low)|` exactly.  On a symmetric piece it is
> `2 |G(s_low)| sum_eps |cos(2 pi r tau(eps_top)/3^k)|` -- a `2^{|top|}`-term
> explicit sum (the low signs factor out).

**Proof.**  Rank-one form; `|omega^{-r tau}| = 1`; Lemma R(c). `square`

(Convention: `sum_eps` runs over the FULL `2^s` cube; the low signs do
not change `|h|`, so the symmetric budget is
`2^{s_low + 1} |G(s_low)| sum_{eps_top} |cos(2 pi r tau(eps_top)/3^k)|`
with the inner sum over the `2^{|top|}` top signs only.)

Verified: single-coset unimodularity to `2.2e-15`.  T3's floor RHS -- the
quantity any sound emission is capped by -- is therefore computable in
`O(2^k)` per class from the G-table, with no scan.

---

## 3. Theorems E2 + E3: the optimal schedule, and the overdraw wall

> **Theorem E2 (optimal sound schedule).**  Among T3-sound schedules (one
> pattern per class), paying the ARGMAX pattern
> `D* = argmax_D |chat_v(D)|` is optimal, and `D*` and its payment are
> closed-form.  On a single coset the argmax is coordinate-wise: take the
> larger of `|sin beta_t|`, `|cos beta_t|` per top coordinate.  On a
> symmetric piece only even `|D|` survives, and the even-restricted
> optimum is the FLIP-WEAKEST rule: take the coordinate-wise choice, and
> if its `|D|` is odd, flip the coordinate with the smallest
> `max/min(|sin|,|cos|)` gap.  (The odd case is the MAJORITY: 122 of the
> 208 `(k, r, top)` configurations at `k <= 3`.)
>
> **Theorem E3 (the overdraw wall).**  Additive multi-pattern payment is
> UNSOUND.  PROVED on single cosets: the budget is `2^s |G|` (E1) and
> `sum_D 2^s |chat_v(D)| = 2^s |G| prod_top (|sin beta_t| + |cos beta_t|)`,
> each factor in `(1, sqrt 2]` when `sin beta_t != 0` -- so the ratio
> strictly exceeds 1 on every twisted-top class and is at most
> `2^{|top|/2}`.  COMPUTED on symmetric pieces (where the budget is the
> `|cos|`-sum): the ratio ranges BELOW and above 1 -- every depth-1
> symmetric class sits at exactly 1 (only `D = empty` survives), most
> deeper classes under-draw -- and the strict overdraw is confined to
> `|top| >= 2` classes, attaining EXACTLY 2 at the extremal witness
> `(k, r, v) = (3, 10, 111111)` (`B = 6` pin).  One overdrawing class is
> all unsoundness needs: the one-pattern cap in T3 is NECESSARY -- this
> closes the band-uniform packet's multi-pattern-schedule design point
> for hierarchy pieces.

**Proof.**  E2: the payment is `2^s` times a single coefficient's
magnitude; the product law makes the unrestricted argmax coordinate-wise,
and restricting to even cardinality costs exactly one flip, optimally the
smallest gap (any even pattern differs from the unrestricted argmax in an
even number of extra flips, each a penalty factor `< 1`).  E3: expand
`sum_{D subseteq top} prod_{t in D} |sin| prod_{t notin D} |cos| =
prod_t (|sin beta_t| + |cos beta_t|)` and use E1 for the single-coset
budget.  The symmetric extremal value 2 is a computed pin, not claimed in
general. `square`

Verified: argmax closed form == brute argmax to `3.6e-14`; the
flip-weakest rule == brute even-restricted maxima on ALL 208 `(k, r, top)`
configurations (`1.1e-16`); overdraw max `2.000000` over all
pieces/classes at `B = 6`.

---

## 4. Theorem E4: flat-cube must widen to rank-one emission

> **Theorem E4.**  (a) Symmetric depth-1 pieces are FLAT-EXACT: `h` is
> class-constant (`cos(2 pi r tau/3) = -1/2` for both `tau = +-1`), the
> only surviving pattern is `D = empty`, and flat-cube emission pays the
> FULL budget.  (b) From depth 2, twisted symmetric pieces are not flat
> (#805), so the flat-cube rule -- which pays only pieces CERTIFIED flat
> -- does not apply to them at all; the relaxed `D = empty`-only payment
> (share := `|chat_v(empty)| / max_D |chat_v(D)|`, minimized over
> nonflat classes) collects `min share 0.102` at `k = 2` and `0.010` at
> `(k, r) = (3, 7)` (COMPUTED pins, B = 6).  (c) The flat territory
> within the hierarchy CONTAINS the subgroup-cylinder unions and the
> depth-1 symmetric pieces (PROVED flat -- depth 1 is itself a
> cancellation phenomenon: the twisted pair's nonflat masses cancel);
> conversely every single twisted coset is nonflat (#816 C4) and every
> symmetric twisted PAIR at depth in {2, 3} is nonflat (exhaustive at
> B = 6); that NO other hierarchy profile cancels to flat is COMPUTED
> (no counterexample in scans), not proved.  The maximal band is the
> boundary case where flat-cube is budget-exact (T3).
>
> **Definition (rank-one emission, the widened primitive).**  Pay
> `2^s |chat_v(D*)|` at the argmax pattern per class against the #816
> certificate (G-table + trig factors).  On flat territory `D* = empty`
> and the rule IS flat-cube; on twisted pieces it collects the per-class
> optimum.

**Proof.**  (a) Lemma R(c) at `k = 1`: `tau in {+-1}`, cosine even, so
`h == -G(s_low)` on the whole cube; constancy = flatness = exactness
(T3's boundary argument).  (b) is #805 plus the computed shares; (c) the
INCLUSIONS are proved (subgroup unions by #816 C1's linearity; depth-1
pieces by (a); single-coset and depth-`{2,3}`-pair NONflatness by #816
C4 and the exhaustive pair scan) -- but a general no-cancellation
argument for arbitrary deeper profiles is NOT given; the exactness of
the classification is a `B = 6` computed fact. `square`

Verified: depth-1 flat-exactness to `0.0e+00` (exact rationals underneath:
`3 G_{1,r}(l) = wtil(l) - wtil(l+1)`); the share pins; the single-coset
`k = 1` ratio `sqrt(3)` (= `|tan(2 pi/3)|`); the maximal band's
class-constant `h == wtil(s) - M/c` recovered by brute.

---

## 5. The mandatory instance: the resonant residue is maximally twisted

`j* = (c-1)/2` (the transverse-charge packet's resonant point,
`|hatf(j*)| >= 0.70 M`, re-pinned `0.7006`) has ALL-ONES balanced digits:
`s3(j*) = B` and `j* == (3^k-1)/2 mod 3^k` at EVERY depth `k <= B`.  So
the one spectrum any admission decision must process sits in the twisted
regime at every depth: flat-cube emission covers its band only through
the depth-1 symmetric piece; every deeper localization -- where the
`O(B 3^k)` certificates live -- is rank-one territory.  Its per-depth
G-tables are emitted into the certificate.

---

## 6. The admission question, restated with its arithmetic in hand

What this packet settles is local scalar bookkeeping: the candidate rule's
SHAPE (rank-one, one
pattern per class -- E3 makes the cap necessary, E4 makes the widening
necessary), its CERTIFICATE (#816's G-table: `O(B 3^k)` bits exactly,
hence `e^{o(N)}` whenever `k = O(log B)`), its BUDGET and CAPPED SCALAR
CREDIT in closed
form (E1/E2), and its TEST INSTANCE (E5).  What admission now asks, and
what stays open:

1. **The semantic source-to-payment bridge** (open): map a named rank-one
   mode to an actual realized same-owner first-match profile cell, certify
   `|Z_i^circ| <= U_i <= exp(o(n))(1+barN_i)`, prove A4 by image-scale
   MI+MA or a direct Sidon/Fourier moment payment, and separately prove A6
   via RC or a direct distinct-slope theorem.  Constructibility and scalar
   charge capacity alone are not payment.
2. **The aggregate census** (open): bound all encoded modes and cells
   uniformly at subexponential scale; finite pattern counts here do not
   supply an all-depth census.
3. **The grammar and overlap decision** (open): only after the semantic
   bridge exists can the compiler admit the rule and prevent double counting.
4. **Non-hierarchy adversarial bands** (open, outside every packet so
   far): a failing band with no bounded-depth structure has no G-table;
   U1 width forces only `|A| >= (c/L) e^{2 eta N}`.
5. Atlas totality and large-q Sidon, unchanged.

## Nonclaims

- **NOT a proof of admission**: E2/E3/E4 constrain local scalar accounting.
  The governing profile-payment interface remains OPEN: an actual same-owner
  first-match cell, an (A4) analytic/Sidon payment, a separate (A6)/(RC)
  distinct-slope bound, and a uniform subexponential aggregate census.  No
  emission rule is added to the grammar either.
- **The overdraw extremal `2` and the share floors are B = 6 COMPUTED
  pins**; the proved statements are the inequalities (`> 1` on twisted
  pieces, `<= 2^{|top|/2}`) and the exact closed forms.
- **Base 3 only**; single cosets asymmetric (symmetric statements pair
  `r` with `3^k - r`); bands exclude `0` (`D = empty` shift `-M/c` where
  it appears).
- **No claim for non-hierarchy bands** (item 4 above).
- Floats only in scans under the exact Parseval + Lemma-N guards; the
  depth-1 arithmetic and the `j*` digit identities are exact.
- **NOT a reserve payment**: fence (N1) respected.

## Consumers

- **The admission decision (#791 Sec 5, #716 Sec 7.1)**: the yes/no
  grammar question is not discharged or merely upgraded in place.  This
  packet supplies the local scalar candidate -- "flat-cube" widens to
  "rank-one" (E4) and the cap is necessary (E3) -- while the same-owner
  first-match/source-to-cell theorem, A4 payment, separate A6/RC bound, and
  aggregate census remain prerequisites.
- **The band-uniform packet (#795)**: its multi-pattern-schedule design
  point is resolved only at local scalar schedule-shape scope on hierarchy
  (piece, class) accounts; its middle-width compression residual is answered
  for hierarchy families (via #816, referenced).
- **The twisted-coset packet (#816)**: C3's reality generalized (Lemma
  R); its G-table becomes an operational emission certificate.
- **The transverse-charge packet (#776)**: its resonant instance located
  in the hierarchy (E5).
- `rs_mca_thresholds.tex`: paste-ready remark after the PO4 material --
  "on the base-3 chart the sound emission schedule against hierarchy
  bands is one pattern per class (additive schedules overdraw, factor up
  to 2 computed), the optimal pattern and its payment are closed-form in
  the G-table, and the flat-cube rule is exact precisely on subgroup/
  depth-1 territory; these are local scalar facts, while admission still
  requires a same-owner first-match/source-to-cell theorem, A4 payment,
  A6/RC distinct-slope control, and an aggregate census" --
  visible hypotheses: #749-corrected class, base-3 chart, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_rank_one_emission_arithmetic.py
# -> RESULT: PASS (20/20)
python3 experimental/scripts/verify_rank_one_emission_arithmetic.py --tamper-selftest
# -> tamper-selftest: caught 7/7
python3 experimental/scripts/verify_rank_one_emission_arithmetic.py --emit-certificate \
  experimental/data/certificates/rank-one-emission-arithmetic/rank_one_emission_arithmetic.json
cd experimental/lean/rank_one_emission_arithmetic && lake build
# -> Build completed successfully
```
