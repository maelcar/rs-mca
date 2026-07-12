# Championship census b=19..26: searching past the b=18 record, and the
# off-corridor slice inside the unconditional bracket

## Status

`R1 CHAMPIONSHIP SEARCH b=19..26: NULL (COMPUTED).` No family tried (two-cluster
interval-with-holes -- exhaustive within an explicit small-hole subclass at
b=19..22 --, unions of <=3 APs, perturbations/extensions of the b=18 winner,
general local search) beats the `b=18` record `rho=0.158411`; best found ranges
`rho=0.1194-0.1448` over `b=19..26` (non-monotonic: dips at `b=21,23,25`, local
peaks at `b=19,22`), never approaching the champion. The null is banked,
consistent with `fiber_image_tradeoff.md`'s own note that its `b=20` search "no
longer converges" (their weak `0.1515` was not used either; our own
best-effort at `b=20` is `0.142978`, in the same neighborhood). /
**Tensor-lift composition is CLOSED analytically (PROVED)**:
combining two blocks via positional `(S+v)Q^j` encoding multiplies `f` and `L`
exactly, so the combined `rho` is the size-weighted average of the two
components' rates -- since every currently-censused `b<18` rate is `<=0.158411`,
no tensor composition landing in `19..26` can beat the champion. / `R2 UPPER-END
TIGHTNESS`: **(a)** the new census's `X=(fL)^{1/b}` stays in `[2.253, 2.312]`
throughout `b=19..26`, well inside `#678`'s off-corridor ceiling `2.5198` and far
from the universal `3` -- the `3^b` bound is not remotely tight on these
structured families (COMPUTED, calibration). **(b)** composing `#678`'s
off-corridor envelope with the base compression gives a **PROVED unconditional**
bound `rho(V) <= (1/3) log 2 = 0.231049 < log(3/2)` **on the explicit slice**
`{V : d(V)/b not in (0.0845, 2/3)}` -- a genuine improvement on that slice, but
it does **not** tighten the global bracket `[0.158411, 0.405465]`, because the
corridor itself is still open and our new witnesses are not shown to lie off it
(exact `d` is not computed here; PROVED-ON-SLICE, sup-tightening OPEN). / `R3`
the Codex team's `F_13` calibration point (`b=10`, `(fL)^{1/b}=2.1600`) is placed
on the census table for scale only -- it is a **modular** (not distinct-integer)
construction, a different class, and sits below every point on our table; no
claim of comparability beyond the raw `X`-axis is made.

This packet works the two open ends of the bracket
`rho* in [0.158411, 0.405465]` established by **#655**
(`fiber_image_tradeoff.md`, the `b=18` champion) and closed unconditionally on
the upper end by **DannyExperiments #668** (`canonical_transversal_vc_compression.md`)
via **our #673**'s consumer reconciliation (`ilo_moment_closed_consumer.md`,
`thresholds-ilo-moment-closed-consumer`). It also consumes **our #678**
(`curve_restricted_product.md`, `thresholds-curve-restricted-product`) for the
off-corridor envelope used in R2(b). Every number below is recomputed by
`experimental/scripts/verify_championship_census_b19_26.py` (stdlib-only,
zero-arg, `RESULT: PASS (75/75)`, ~42s / ~1.7GB peak (fits under
`ulimit -v 2097152`) -- heavier than `#655`/`#678`'s own verifiers because the
witnesses here run to `b=26` with `L1` up to `6.2M`, vs. their `b<=18`/`L1<~151K`;
every witness re-derived by the same exact subset-sum DP `#655`/`#673`/`#678`
use, plus an independent brute-force cross-check on the smallest new witness).

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exact/exhaustive
finite enumeration), **MEASURED** (exact finite objects, trend read off),
**CONDITIONAL** (proved modulo a named input), **AUDIT** (cross-reference),
**OPEN**.

**Credit.** The bracket, the moment-curve reduction, the `b=18` champion, and the
census/fit methodology are **our #655** (`fiber_image_tradeoff.md`) building on
**our #643** (`pte_cluster_packing_frontier.md`) and **our #623**
(`pte_extremality_image_face.md`). The unconditional upper end `log(3/2)` is
**DannyExperiments #668** (`canonical_transversal_vc_compression.md`,
`f<=2^(b-d)`, `L<=sum_{j<=d}binom(b,j)`, `fL<=3^b`), reconciled into the chain by
**our #673** (`ilo_moment_closed_consumer.md`). The dissociation-dimension
envelope `h(alpha)`, Theorem A's off-corridor ceiling `X<=2^{4/3}`, and the
corridor framing consumed in R2(b) are **our #678**
(`curve_restricted_product.md`), which itself credits **Codex team route cuts**
(the signed-span bound, the corridor framing, the
positional-encoding amplification) -- credited again here at one remove since
R2(b) is built directly on Theorem A. The `F_13` calibration point in R3 is
**Codex team calibration, 2026-07-12**. The minimal degree-2 PTE
trade support 6 is **scottdhughes #564** (`w_a_star_pte_lemma.md`).

---

## 0. Setup (AUDIT, recap)

A **block** `V` is `b` distinct integers; `Phi(S) = (|S|, sum_S x, sum_S x^2)` is
its degree-2 signature (the moment-curve reduction, `#655` R1); `fstar(V)` is the
max fiber, `L1(V)` the image size, `phi = log(fstar)/b`, `lambda = log(L1)/b`,
`rho = phi + lambda - log2` (natural log throughout, matching `#655`/`#673`/`#678`).
Equivalently `X := (fstar * L1)^{1/b} = 2 e^rho`, so `rho <= log(3/2) <=> X <= 3`
(`#678` Section 0). The current bracket, both ends unconditional per `#673`:

```
    rho* in [0.158411, 0.405465]     (X* in [2.3433, 3])
```

---

## R1 — Championship search b=19..26 (NULL, COMPUTED)

### 1.1 Method

`fstar, L1` are computed exactly by the same subset-sum DP `#655`/`#673`/`#678`
use: process the `b` elements one at a time, maintaining a dict keyed by
`(|S|, sum_S, sum_S^2)` with the subset count as value; `fstar` = max value,
`L1` = number of keys. This is exact (no sampling, no hashing collisions) and
tractable exactly because the champions live at moderate `lambda` (`L1` stays
many orders of magnitude below `2^b`, `#655` R3) -- the same reason `#655`/`#678`
could census up to `b=18`.

### 1.2 Families searched

Per the work menu, all constructions are (WLOG by affine invariance, `#643` Lemma
A) centered at `0`; the `b=18` champion is symmetric, so the primary
representation is a **symmetric offset set**: `b/2` positive offsets mirrored
(`+` a center element `0` when `b` is odd).

1. **Interval-with-holes, exhaustive within an explicit subclass (b=19..22).**
   Near cluster `{1,...,n}` (`n` fixed) union a far window `[f0, f0+w-1]` with
   `h` holes removed, **every** `binom(w,h)` hole placement checked, `n` and `f0`
   swept over a bounded range, `h<=2`. This class exactly contains the `b=18`
   champion's own structure (`n=5`, far window `[12,16]`, `h=1` hole at `13`) --
   sanity-checked: re-running the identical sweep at `b=18` reproduces
   `rho=0.158411` **exactly** as the class optimum (verifier BLOCK 1), so the
   method is validated before trusting its `b=19..22` nulls. This exhaustive
   sweep alone found the best-known `b=22` witness, `rho=0.144797` (Section 1.3
   table) -- still below `0.158411`, and better than the general hill-climb's
   own `b=22` result (`0.137402`), showing the two methods are complementary.
2. **Unions of <=3 APs.** Explicit parameter grid over two-three arithmetic
   progressions of common differences `1..5`, varying lengths/offsets, spot
   checked at `b=20,24`: best `0.129664` (`b=20`) and `0.118402` (`b=24`),
   both **below** the two-cluster/hill-climb results at the same `b` -- this
   family underperforms throughout, matching `fiber_image_tradeoff.md`'s own
   finding that "two-scale unions and GAPs top out at `rho ~ 0.145`" below the
   interval-with-holes champion.
3. **Perturbations/extensions of the b=18 winner.** Direct extensions of the
   champion's own 9 offsets (add 1-8 offsets at the near or far end, fill a
   gap), spot-checked at `b=22,24,26`: best `0.132374`, `0.125605`, `0.112228`
   respectively -- again below the hill-climbed results at the same `b`,
   confirming naive extension of the exact `b=18` structure is not optimal at
   larger `b` (some drift away from it, e.g. dropping an offset from the near
   cluster, does better). Plus a general local hill-climb (random
   single-offset swaps, multi-start, simulated-annealing-style acceptance),
   incrementally seeded from each previous `b`'s best, run for `b=19..26` with
   a per-`b` time budget that grows with `b` (evaluation cost grows with `L1`,
   itself exponential in `b`; a single eval already costs `~8s` at `b=26` for
   a moderate-diameter candidate, and the best-found `L1` there is `6.2M`).
4. **Tensor-lift compositions.** Handled analytically, not by search --
   Section 1.4.

None of (1)-(3) is a claim of *exhaustive* search over all `b`-element integer
sets (that space is far too large); (1) is exhaustive **within** the stated
explicit subclass at `b=19..22`, and (2)-(3) are documented, time-boxed,
best-effort searches. This is exactly the scope the task calibrates: a
diligent, reproducible null, not a nonexistence proof.

### 1.3 Results

Best-found `rho(b)` combining all of (1)-(3) above (every row re-derived
exactly by the verifier, BLOCK 1; witness offsets given as symmetric-offset
representation, `+center` if `b` is odd):

```
    b    best rho found   f       L          X=(fL)^(1/b)   vs 0.158411
   18       0.158411     30     151275         2.3433       (champion, #655)
   19       0.144045     35     231262         2.3099       below
   20       0.142978     36     508381         2.3074       below
   21       0.132500     46     736714         2.2834       below
   22       0.144797     96    1056451         2.3116       below
   23       0.127856     66    2405852         2.2728       below
   24       0.130839    104    3727586         2.2796       below
   25       0.119448    133    4997920         2.2538       below
   26       0.123031    266    6181859         2.2618       below
```

The best-found sequence is **non-monotonic** (local peaks at `b=19` and
`b=22`, dips at `b=21`, `b=23`, `b=25`) and stays in `rho in [0.1194, 0.1448]`
throughout -- well below the champion, and below even `fiber_image_tradeoff.md`'s
own unused weak `b=20` bound (`0.1515`). No family or method found anything
close to `0.158411`. This is the **NULL** the task anticipated: a clean,
reproducible decline that calibrates the fit rather than a new record --
`fiber_image_tradeoff.md`'s three-model fit put the asymptote at `R~0.20-0.23`
from a `b=10..18` window in which the champion happened to sit at the local
peak `b=18`; this census shows the *very next* stretch (`b=19..26`) is not a
continued climb but a fluctuation an order of magnitude below that asymptote,
consistent with a slow, noisy approach rather than a near-term one (re-fitting
with these new, lower points is left as a residual, Section "Honest residuals"
item 4, since the fit's own three models were calibrated against a
monotonic-looking window that this data complicates).

### 1.4 Tensor-lift compositions are closed (PROVED)

> **Lemma (two-block positional tensor).** Let `V1` (size `b1`) and `V2` (size
> `b2`) be blocks with `(fstar_1, L1_1)` and `(fstar_2, L1_2)`. Choose
> `S0 > ` (max possible `|sum of a V1-subset|`), `S1 > ` (same for `V2`), and `Q`
> large enough that `S1+v2` scaled by `Q` cannot overlap the digit range of the
> `V1` part in either the sum or the sum-of-squares coordinate (explicit
> sufficient constants in the verifier). Then
> `V = V1 union { (S1+v2)*Q : v2 in V2 }` is a block of size `b1+b2` with
> `fstar(V) = fstar_1 * fstar_2` and `L1(V) = L1_1 * L1_2` **exactly**.

*Proof.* For `T = T1 union {(S1+v2)Q : v2 in T2}`, `sum(T) = sum(T1) + Q(|T2| S1
+ sum(T2))` and `sumsq(T) = sumsq(T1) + Q^2((S1+v2)`-square sum`)`; since `Q` is
larger than every possible value of the first (T1-side) term, reading `sum(T)`
in base `Q` recovers `sum(T1)` exactly as the low part and `|T2| S1 + sum(T2)`
as the high part, which itself (since `S1` exceeds every possible `sum(T2)`)
splits into `(|T2|, sum(T2))` by division. The same base-`Q^2` argument on
`sumsq(T)` recovers `sumsq(T1)` and (combined with the already-known `|T2|,
sum(T2)`) `sumsq(T2)`. So `Phi(T) = (|T|, sum(T), sumsq(T))` determines
`(Phi(T1), Phi(T2))` bijectively (given the size constants), whence the fiber of
`Phi(T)` over any achieved value is exactly the product of the two component
fibers, and the image is exactly the product of the two component images. ∎

**Verified exactly** (verifier BLOCK 2) on: two dissociated blocks (`f=1` each,
confirms `f_combined=1`, `L_combined` = product); a block with a genuine
degree-2 PTE trade `{1,5,6} vs {2,3,7}` (`f=2`, `L=63`) tensored against a
dissociated 9-element block (`f_combined=2` exactly, matching `f1*f2`); and the
trade-bearing block tensored against **itself** as two independent slots
(`f_combined=4=2^2`, `L_combined=63^2` exactly).

**Corollary (tensor-lift cannot help in 19..26, PROVED given the current
census).** Writing `q(b) := max known rho` at size `b`, the Lemma gives
`rho(V1 tensor V2) = (b1 q(b1) + b2 q(b2))/(b1+b2)`, a weighted average. Every
currently censused `b<18` value is `<0.158411` strictly (`fiber_image_tradeoff.md`'s
table, `b=6..16`; verifier BLOCK 3 additionally re-derives the plain-interval
value at every `b=1..17` by exhaustive brute force, confirming none exceeds
`0.158411`), and `b=18` itself attains `0.158411` only at `b1=b2=18` (giving
`b=36`, out of range). Hence **every** two-block tensor composition landing in
`b in [19,26]` uses at least one factor with `q(b_i) < 0.158411`, so the
weighted average is **strictly** below `0.158411`. (The same argument extends to
`k`-fold compositions.) This closes the tensor-lift family for this range
analytically -- no search needed.

---

## R2 — Upper-end tightness

### 2(a). Is the 3^b compression tight on these structured classes? (COMPUTED, calibration)

For every new census witness, `X := (fstar*L1)^{1/b}` measures how close the
block sits to `#668`'s universal ceiling `fL<=3^b` (`X<=3`):

```
    b    X=(fL)^(1/b)     vs 2.5198 (#678 off-corridor ceiling)   vs 3
   18       2.3433                below                          well below
   19       2.3099                below                          well below
   20       2.3074                below                          well below
   21       2.2834                below                          well below
   22       2.3116                below                          well below
   23       2.2728                below                          well below
   24       2.2796                below                          well below
   25       2.2538                below                          well below
   26       2.2618                below                          well below
```

Every value (same witnesses as 1.3) sits comfortably inside `#678`'s
off-corridor regime (`X<=2.52`), and in fact the whole `b=19..26` range
(`X in [2.2538, 2.3116]`) sits **below** the `b=18` champion's own `X=2.3433`
-- the new census does not even approach the previous frontier's tightness,
let alone the universal `3`. This reinforces `#678`'s own `b<=18` finding
(there, all computed blocks have `X<=2.3433`): the universal `3^b` bound is
not remotely tight on the structured families either census explores. This
**calibrates** tightness (per the task) -- it does not by itself prove a
smaller unconditional exponent, since it is silent on whether some *other*,
uncensused block could sit nearer the corridor.

### 2(b). Composing the off-corridor envelope with the compression (PROVED on an explicit slice; does not tighten the global bracket)

`#678` Theorem A proves, for every block, `X(V) <= 2^{h(d(V)/b)}`, and in
particular `d(V)/b >= 2b/3` or `d(V)/b <= 0.0845` each force
`X(V) <= 2^{4/3} = 2.5198`. Composing this with the rate identity
`rho = log(X/2)` gives immediately:

> **Proposition.** On the slice `Sigma := {V : d(V)/b not in (0.0845, 2/3)}`,
> `rho(V) <= log(2^{4/3}/2) = (1/3) log 2 = 0.231049`, **unconditionally**. Since
> `0.231049 < log(3/2) = 0.405465`, this is a genuine unconditional improvement
> of the upper bound **restricted to `Sigma`**.

*Proof.* Immediate composition of `#678` Theorem A with `X=2e^rho` (Section 0).
Verifier BLOCK 4 rechecks the arithmetic (`2^{4/3}/2 = 2^{1/3}`,
`log(2^{1/3}) = (1/3)log2 = 0.230...< log(3/2)`) and re-verifies Theorem A's two
closed-form endpoints (`h(2/3)=4/3`, `h(0.0845...)~4/3`) from `#678`'s own
envelope formula.

**Why this does not move the reported bracket (be surgical).** `rho*` is a
supremum over **every** block, including any that might one day be found **inside**
the corridor `d/b in (0.0845, 2/3)` -- exactly where `#678`'s own Theorem B
localizes the corner `X->3` and where the wall (`#678` Section 8, `#673`'s open
exponential-regime inverse-LO) remains open. So:

- The Proposition is **PROVED** as a statement about the **slice** `Sigma`.
- It does **not** prove `rho* <= 0.231049`, because `Sigma` is not all blocks --
  a hypothetical corridor-dwelling block is not excluded by anything in this
  packet or in `#678`.
- Our own new `b=19..26` witnesses are **not shown to lie in `Sigma`**: we did
  not compute their exact dissociation dimension `d` (expensive -- the natural
  brute-force check costs `binom(b,d)*2^d`, infeasible much past `b=18`, see
  Residual 1). Their `X` values (2a) are measured directly from `(fstar,L1)`,
  independent of `d`; that they land below `2.5198` is consistent with `Sigma`
  but is not itself a `d`-based proof they are in `Sigma`.

So R2(b)'s honest content is: **the only way any future block can beat
`X=2.5198` is to live in the corridor**, sharpening where a search for a bigger
bracket-mover would have to look -- a calibration of the open problem's
location, not a new bound on `rho*`. The global bracket stays
`rho* in [0.158411, 0.405465]`, both ends per `#673`.

---

## R3 — The Codex team's F_13 calibration point (AUDIT, placed for scale only)

Per the Codex team's calibration (credited above): at `b=10`, a
**modular** (over `F_13`) construction attains `(fL)^{1/b} = 2.1600`, i.e.
`rho = log(2.1600/2) = 0.076961`. This is a **different class** from every
other entry in this note -- a modular residue construction, not `b` distinct
integers on the degree-2 moment curve -- so it is **not** a competing witness
for the distinct-integer bracket and is not independently re-derived here (we
do not have its source construction). It is placed on the census table purely
for scale:

```
    b     class                 X            rho              role
   10     modular F_13         2.1600        0.076961         Codex team calibration point
   18     distinct-integer     2.3433        0.158411         champion (#655)
   19-26  distinct-integer     2.2538-2.3116 0.1194-0.1448    this packet's census (R1)
```

No claim is made that the `F_13` point bears on the distinct-integer `rho*`;
it sits below every distinct-integer entry on the table, consistent with the
modular class being a weaker (or simply differently-scaled) construction at
this small `b`, and is reported exactly as received.

---

## Honest residuals (OPEN)

1. **Exact `d(V)` for the new witnesses is not computed.** The brute-force
   method `#678` uses to pin `d` exactly (checking `binom(b,d)` subsets of size
   `d`, each needing a `2^d` internal check) costs `binom(26,17)*2^17 ~ 10^12`
   operations at the sizes here -- infeasible in this budget. R2(b)'s slice
   membership for our own witnesses is therefore unresolved; only a cheap
   witness lower bound would be tractable (verify one candidate large subset is
   dissociated), and it is not attempted here.
2. **The b=19..26 search is not exhaustive** outside the small-hole subclass at
   `b=19..22` (Section 1.2). A better search (deeper hill-climb, more seed
   families, more time) could still find a `b<=26` block beating `0.158411`;
   nothing here rules that out, only that a diligent, time-boxed, multi-family
   effort did not find one. This is the calibrated null the task asked for, not
   a nonexistence proof.
3. **The corridor (`#678`'s wall) is untouched.** Closing it remains
   `#673`'s open exponential-regime inverse-LO problem; this packet does not
   attempt it.
4. **The fit.** `#655`'s three-model fit (`R ~ 0.20-0.23`) is not re-fit here
   with the new (lower) `b=19..23` points; folding a declining-then-partial-
   recovery segment into that fit is future work, not attempted (would require
   re-running the least-squares over an extended, non-monotonic window and is
   out of this packet's scope).

---

## Summary

```
    TARGET:  narrow rho* in [0.158411, 0.405465].
    R1:      championship search b=19..26 -- NULL (COMPUTED); best found per b
             all below 0.158411; tensor-lift compositions CLOSED analytically
             (PROVED product lemma + weighted-average corollary).
    R2(a):   new census X=(fL)^(1/b) stays in [2.2538,2.3116], below even the
             b=18 champion's own 2.3433, far under #678's off-corridor 2.5198
             and the universal 3 (COMPUTED, calibration -- the 3^b bound is
             not tight on these families).
    R2(b):   off-corridor envelope composed with the compression =>
             rho<=0.231049 on the slice {d/b not in (0.0845,2/3)} (PROVED on
             the slice). Bracket UNCHANGED: corridor still open, our witnesses
             not shown to be off it.
    R3:      Codex team's F_13 modular point (b=10, X=2.1600) placed for scale
             only -- different class, not a competing witness.
    BRACKET (unchanged, both ends unconditional per #673):
             rho* in [0.158411, 0.405465].
```

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/championship_census_b19_26.md` (this).
- Verifier: `experimental/scripts/verify_championship_census_b19_26.py`
  (stdlib-only, zero-arg, `RESULT: PASS (75/75)`, ~42s / ~1.7GB peak; recomputes
  every `(fstar, L1, rho, X)` reported above via the same DP as `#655`/`#673`/
  `#678`, re-derives the tensor lemma on 3 explicit instances, re-derives the
  R2(b) arithmetic, and cross-checks the smallest new census witness by an
  independent brute-force enumeration).
- Read-only inputs: `#655` `fiber_image_tradeoff.md`, `#673`
  `ilo_moment_closed_consumer.md`, `#678`
  `curve_restricted_product.md`, DannyExperiments
  `#668` `canonical_transversal_vc_compression.md` (fetched via
  `refs/pull/668/head`).

**Per-claim status.** R1 championship table = **COMPUTED** (exact `fstar,L1`
for every witness; declining/null trend = **MEASURED**). Tensor lemma = **PROVED**
(verified exactly on 3 instances); the b<19..26 non-improvement corollary =
**PROVED given the current census** (not a universal nonexistence claim). R2(a)
`X` values = **COMPUTED**; "not tight" reading = calibration, not a new bound.
R2(b) slice proposition = **PROVED**; global-bracket non-improvement = the
**honest scope note**, not itself a separate claim needing a label. R3 = the
external point is reported **AS RECEIVED** (not independently re-derived; the
`X -> rho` arithmetic conversion is verified). Bracket
`rho* in [0.158411, 0.405465]` = **unchanged**, both ends per `#673`
(**COMPUTED** lower / **PROVED** upper, per that note's own labels).

**Nonclaims.** No new champion. No change to the reported bracket. No claim
that `Sigma` (R2(b)) contains any block in this census. No re-derivation of
`#668`/`#673`/`#678`'s own theorems beyond the audited recap in Section 0/R2(b).
No `.tex` touched. No A6/conic/ray material.
