# Corridor-interior wall witness hunt: four NULL families, and a free certificate

## Status

`TARGET: exhibit a block V with X(V)=(f(V)L(V))^(1/b) > 2^(4/3)=2.519842, which
(#678 Theorem A, one-sided forcing argument PROVED here) would automatically
be a corridor-interior witness refuting the OPEN corridor bound
L<=2^(d+b/3) -- with NO need to compute the true dissociation dimension d
exactly: f<=2^(b-d) (DannyExperiments #668) plus X>2^(4/3) forces
L>2^(d+b/3) directly, for whatever d actually is. / CERTIFICATE SIMPLIFICATION
(PROVED): ceil(alpha_0*b)<=5 for every b<=59 (alpha_0=0.084497), and #678
Lemma 1 already gives d(V)>=5 for every b>=5 block for free -- so the S0
half of the certificate never needs a bespoke lacunary construction in the
searched range b in [20,40]; ANY 5 elements of ANY witness certify
d/b>alpha_0. The entire hunt therefore reduces to ONE search: find X(V)>
2^(4/3). / RESULT: NULL across all four families (COMPUTED). Family (i)
lacunary-core+dense-cluster: best X=2.308748, declining monotonically as
core size grows (both far-separated and same-scale variants). Family (ii)
two-scale same-block grids {a+M*c}: best X=2.311619 (near-tensor limit,
large M); interaction (small M, more carries) measurably HURTS, both for
plain-interval and trade-bearing base shapes. Family (iii) CRT/modular lift
of the Codex team's F_13 seed: best X=2.222464 (full 2^10 wrap-choice
search), beating the raw modular value 2.160025 but not the champion; our
own attempt to find a BIGGER modular seed (mod 23/29/31, b=16..22) gave
WORSE modular X (2.10-2.15) than the small F_13 seed. Family (iv) direct
anneal + diameter-stretch: anneal reaches X=2.300265 at b=20 within budget;
a diameter-stretch experiment on the champion (scaling its offsets up to
21x, diameter up to 672) leaves f, L, X EXACTLY unchanged (PROVED: affine
dilation invariance, a special case of #643 Lemma A) -- naive spreading is
not a lever by itself. NOTHING in any family beats the existing #655
champion (b=18, X=2.343296), let alone the 2.519842 target.`

This packet hunts for a **corridor-interior wall witness** on top of **our
#678** (`curve_restricted_product.md`) and **our #682**
(`corridor_diameter_map.md`): a block `V` with `X(V) > 2^{4/3} = 2.5198...`,
which by #678's Theorem A can only occur if the block's (unknown, generally
uncomputable-at-scale) dissociation ratio `d(V)/b` lies in the open corridor
`(0.084497, 2/3)` -- the single remaining OPEN piece of the curve-restricted
product wall (`fL <= 3^b` DannyExperiments #668; corridor bound
`L <= 2^{d+b/3}` OPEN, #678 Section 8). We do **not** close the wall. We (i)
make explicit and prove a **one-sided certificate mechanism** that needs no
exact computation of `d`; (ii) observe that #678's own Lemma 1 makes the
`S0`-certificate half of that mechanism free throughout the searched range,
simplifying the hunt to a pure `(f, L)` search; and (iii) run four
constructive families the task menu proposes -- lacunary-core-plus-cluster,
two-scale same-block grids, a CRT/modular lift of a modular calibration
seed, and direct annealing -- none of which finds `X > 2^{4/3}`, or even
beats the existing `b=18` champion. Every number is recomputed by
`experimental/scripts/verify_corridor_interior_hunt.py` (stdlib-only,
zero-arg, `RESULT: PASS (99/99)`, ~3s; every witness's `f, L` recomputed
exactly, every certificate's dissociation re-verified exactly, the
affine-dilation invariance re-derived and checked on two independent
blocks). Two additional witnesses (a `b=36` trade-bearing grid at two `M`
values) are COMPUTED exactly with the identical method but left out of the
fast gate (each costs ~50s); their exact numbers are reported in Section 3
and are reproducible by calling the verifier's own `grid()` + `f_and_L_dp()`
at that scale.

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exact
enumeration), **AUDIT** (cross-reference to an already-proved fact),
**AUDIT+COMPUTED** (a cited fact, independently re-verified numerically
here), **OPEN**.

**Credit.** The corridor bound, Theorem A, Lemma 1 (`d>=5`), and the
`d/b`-envelope are **our #678** (`curve_restricted_product.md`), building on
**DannyExperiments #668** (`canonical_transversal_vc_compression.md`,
`f<=2^{b-d}`, `L<=SS(d)`, `fL<=3^b`) and **scottdhughes #564**
(`w_a_star_pte_lemma.md`, the minimal degree-2 PTE trade support `6`). The
diameter coordinate, Corollary 2's diameter-inflation floor, and the
search-steering logic are **our #682** (`corridor_diameter_map.md`). The
`b=18` champion and the moment-curve reduction are **our #655**
(`fiber_image_tradeoff.md`). The tensor/positional-encoding averaging lemma
that rules out clean far-separated compositions is **our #683**
(`championship_census_b19_26.md`). The affine-invariance fact specialized
here to pure dilation is **our #643** (`pte_cluster_packing_frontier.md`
Lemma A). The `F_13` modular seed `U={0,1,2,3,4,5,6,7,10,12}` and its
modular value `X=2.1600` are the **Codex team's calibration (2026-07-12)**,
consumed here read-only and lifted to distinct integers as this packet's own
contribution. All cited by name, none re-derived beyond what is proved fresh
below (the one-sided forcing argument, the dilation-invariance proof, and
the four search families' own results).

---

## 0. Setup (AUDIT, recap)

A **block** `V` is `b` distinct integers; its degree-2 signature is
`Phi(S) = (|S|, sum_{x in S} x, sum_{x in S} x^2)` for `S subseteq V`;
`f(V)` is the max fiber of `Phi`, `L(V)` the image size,
`X(V) := (f(V) L(V))^{1/b}`. `I subseteq V` is **subset-dissociated** iff
the `2^{|I|}` signatures `Phi(S)`, `S subseteq I`, are pairwise distinct
(equivalently: `I` contains no equal-size degree-2 PTE trade); `d(V)` is the
max size of a dissociated subset (#678 Section 0, the definition this note
uses throughout, per #678's own note this task points to). #678 Theorem A:

```
    X(V) <= 2^{h(d/b)},   h(alpha) = (1-alpha) + H2(min(alpha,1/2)),
    d/b >= 2/3  =>  X <= 2^{4/3} = 2.5198,   d/b <= alpha_0 = 0.084497  =>  X <= 2^{4/3}.
```

So `X(V) > 2^{4/3}` forces `alpha_0 < d(V)/b < 2/3` -- the **corridor**. Inside
it, `X <= 2^{4/3}` is *equivalent* to the OPEN **corridor bound**
`L(V) <= 2^{d(V) + b/3}` (#678 Section 8), which is #673's open
exponential-regime inverse-Littlewood-Offord problem, restated combinatorially.
Nobody has found a block inside the corridor, let alone one violating the
corridor bound (#678 Section 7's frontier, #683's `b<=26` census).

---

## 1. The one-sided certificate mechanism (PROVED)

The task's premise is that computing `d(V)` exactly is infeasible past
`b~18`, but a witness doesn't need it:

> **Proposition (one-sided corridor-interior forcing).** Let `V` be any
> block, `b = |V|`, `d = d(V)` its true (possibly uncomputed) dissociation
> dimension. If `X(V) > 2^{4/3}`, then `L(V) > 2^{d + b/3}` -- an explicit,
> unconditional refutation of the corridor bound -- and (#678 Theorem A)
> `d/b in (alpha_0, 2/3)`.

*Proof.* DannyExperiments #668 gives `f(V) <= 2^{b-d}` **unconditionally**,
for the block's own true `d`, whatever it is. If `f(V) L(V) > 2^{4b/3}`
(i.e. `X(V) > 2^{4/3}`), then

```
    L(V) > 2^{4b/3} / f(V)  >=  2^{4b/3} / 2^{b-d}  =  2^{d + b/3}.
```

This chain never uses the *value* of `d` -- only that #668's inequality
holds for it -- so `d` never needs to be computed. The corridor membership
follows separately from Theorem A's two proved endpoints (`d>=2b/3 =>
X<=2^{4/3}`; `d/b<=alpha_0 => X<=2^{4/3}`), contraposed. **Verifier BLOCK 0**
checks the forcing algebra `4b/3 - (b-d) = d+b/3` on five `(b,d)` samples and
the arithmetic identity `alpha_0=0.084497`, `h(2/3)=4/3`. ∎

**The `S0` role, and why it is free here (PROVED via #678 Lemma 1, AUDIT).**
#678 Lemma 1 shows every `b>=5` block has `d(V) >= 5` (every 5-subset is
dissociated; the minimal equal-size degree-2 PTE trade needs support `6`,
hughes #564). So `d(V)/b >= 5/b`, which exceeds `alpha_0 = 0.084497`
whenever `b < 5/alpha_0 = 59.17`. **Verifier BLOCK 1** checks
`ceil(alpha_0 * b) <= 5` for every `b` in `20..40` (the searched range) and
`b` up to `59`. Consequently:

> For every block in the searched range, the lower corridor membership
> `d/b > alpha_0` is automatic and free -- **any 5 elements of any witness**
> serve as a valid, instantly-verified `S0` certificate (spot-checked on two
> witnesses below, verifier BLOCK 1). No lacunary/engineered `S0` is needed
> *for this purpose*; the task's `d0 <= ~24` ceiling on certificate cost is
> never binding here. The upper endpoint `d/b < 2/3` is likewise automatic
> the instant `X(V) > 2^{4/3}` is verified (Theorem A's contrapositive).

**This means the entire hunt reduces to a single, purely computational
question: does any block have `X(V) > 2^{4/3}`?** That is what Sections
2-5 search for, and none of the four families finds one. (The lacunary-core
menu item, Section 2, is still tested on its own terms below -- as a
*cluster-boosting* device, not because the certificate needs it.)

---

## 2. Family (i): lacunary core + dense cluster (NULL, COMPUTED)

Menu item (i) suggested a lacunary core (automatically dissociated) unioned
with a dense cluster engineered for high `f`. Two variants, both anchored on
the `#655` champion `CHAMP18 = {2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,
32,33,34}` (`f=30, L=151275, X=2.343296`):

```
    variant                    b   f    L        X          (verifier BLOCK 3)
    far k=2 (core*1000)       20   30   605100   2.306468
    same-scale k=2 ({1,3})    19   32   250614   2.308748
    same-scale k=3 (+{9})     20   38   372969   2.278100
    same-scale k=4 (+{27})    21   49   511034   2.250694
```

**Far separation** (lacunary core scaled far beyond the cluster's span)
behaves as a clean tensor: by **#683**'s two-block positional-tensor lemma
(exact `f_combined = f_1 f_2`, `L_combined = L_1 L_2`), appending `k`
dissociated (Sidon-like, `f=1`) elements contributes marginal exponent
exactly `log2(2) = 1` per element to `log2(fL)` -- **below** the champion's
own average `log2(fL)/b = 1.2285`, let alone the target `4/3 = 1.333`, so
`X` falls as `k` grows. **Same-scale interleaving** (small powers of `3`
placed *inside* the champion's numeric span, so they genuinely interact
with it) does even worse: `X` **declines monotonically** as the core grows
(`2.308748 -> 2.278100 -> 2.250694`, verifier BLOCK 3), i.e. the interaction
here is net-negative, not net-positive. Either way, appending "free" or
near-free dissociated structure to an already-near-optimal cluster dilutes
its rate rather than amplifying it; both variants stay below the champion.

---

## 3. Family (ii): two-scale same-block grids (NULL, COMPUTED)

Menu item (ii): `V = {a + M c : a in A, c in C}` (a genuine rank-2
sumset/GAP, `b = |A||C|`, **not** a union of two blocks), sweeping `M` from
"near-tensor" (large) down to "heavily interacting" (small, forcing carries
between the `a`- and `c`-digits). Two base shapes: plain intervals
`A=0..p-1, C=0..q-1`, and a trade-bearing shape
`A = C = {0,1,2,4,5,6}` (this 6-element set carries a genuine equal-size
degree-2 PTE trade, `#678` BLOCK 8's amplification example).

```
    construction                          b   f     L        X          (verifier BLOCK 4)
    plain interval, M=40                 20   40    474533   2.311619
    plain interval, M=20                 20   40    473763   2.311432
    plain interval, M=4                  20   98    110627   2.247783
    trade base {0,1,2,4,5,6}, C size 3, M=7   18   34    75413    2.270133
    trade base {0,1,2,4,5,6}, C size 4, M=7   24   442   561409   2.237583
```

**Interaction hurts, not helps.** For the plain-interval grid, `X` falls
monotonically as `M` shrinks (`2.311619 -> 2.311432 -> 2.247783`): smaller
`M` induces carries between the two scales, which raise `f` but reduce `L`
by *more*, a net loss (product `fL` falls from `18.98M` at `M=40` to
`10.84M` at `M=4`, both at `b=20`). At large `M` the grid degenerates into
the clean tensor of two small intervals (`#683`'s averaging lemma again),
capping below the target for the same reason as Section 2.

**A larger trade-bearing grid, COMPUTED but not in the fast verifier**
(identical method, `~50s`/case): `A = C = {0,1,2,4,5,6}` at full size
(`p=q=6`, `b=36`) gives, exactly:

```
    M=7:  f=128806   L=12984577   X=2.185435
    M=8:  f=169511   L=16593597   X=2.217223
```

Both `f` and `L` are enormous (hundreds of thousands and tens of millions
respectively) -- the repeated trade structure genuinely explodes both
coordinates -- but their **ratio** relative to `b=36` gives `X` *below* even
the plain-interval grid's `2.31`, because repeating a fixed local gadget
`p times q` times is itself close to a tensor power of that gadget, and
inherits the same averaging cap. Big `f` and big `L` together are not
sufficient; the *exponent* `log2(fL)/b` is what matters, and it stays capped.

---

## 4. Family (iii): CRT/modular lift (NULL, COMPUTED)

Menu item (iii): lift the Codex team's `F_13` calibration seed
`U = {0,1,2,3,4,5,6,7,10,12}` (modular signature over `F_13`,
`(f,L,X)_mod = (3, 737, 2.160025)`, reproduced exactly, verifier BLOCK 5) to
**distinct integers** via `x -> x + 13 k(x)`, searching wrap choices `k(x)`
to minimize the collisions lost on lifting (moving from `Z/13Z` equality,
which the modular construction exploits, to strictly finer `Z` equality).

**Full `2^{10}` search over `k(x) in {0,1}`** (exact, exhaustive over this
wrap class, verifier BLOCK 5): the best lift is
`ks = [1,1,0,1,0,0,0,0,0,0]` (i.e. `V = {2,4,5,6,7,10,12,13,14,16}`), giving
`f=3, L=980, X=2.222464` -- **better than the raw modular value**
(`2.160025`, since `f` is preserved at `3` while `L` rises from `737` to
`980` as some modular collisions break under exact-integer arithmetic and
others survive by design) but still well below the champion.

**Scaling the modular seed itself up (own search, not a lift) makes things
worse, not better:**

```
    seed                b    f    L       X_mod       (verifier BLOCK 5)
    F13 (Codex team)   10    3    737     2.160025
    mod 23 (ours)      16   37   5811     2.154162
    mod 29 (ours)      20  253  12719     2.115333
    mod 31 (ours)      22  776  16647     2.104923
```

A short hill-climb (single-residue swaps) over residues mod `p` for
`p in {23,29,31}` at `b in {16,20,22}` never recovers even the small `F_13`
seed's own modular rate, let alone beats it -- so there is no evidence this
route improves with scale; if anything the modular class degrades as `b/p`
grows past the `F_13` seed's own ratio. Since the lift only ever
**preserves or improves on** the modular `X` by a modest margin (the `F_13`
case: `+0.062`), and the modular seed itself is already the wrong side of
the champion by `>0.18`, this family caps out well short of the target at
the scale tested.

---

## 5. Family (iv): direct anneal + the diameter-stretch invariance (NULL, COMPUTED + PROVED)

**Anneal.** A simulated-annealing search directly on `f L` (symmetric-offset
representation, single-offset perturbation moves) reaches, within its time
budget, `X = 2.300265` at `b=20` (`f=30, L=573373`, verifier BLOCK 6) --
consistent with, and not exceeding, `#683`'s much more extensive `b<=26`
census (best `0.1194`-`0.1448` in their `rho` units, i.e. `X` in
`[2.2538,2.3116]` there). **Why deeper annealing is expensive**: the exact
DP's cost is `O(b * L)`, and `L` reaches the millions by `b~24-36` for any
moderately dense/spread block (Sections 3-4 above); each move then costs
several seconds rather than milliseconds, sharply limiting the number of
moves reachable in a fixed budget (this matches `#683`'s own reported
`~8s`/eval at `b=26`). Pinning an explicit dissociated core (e.g. small
powers of `2`) and annealing only the remaining cluster was also tried, but
is structurally *handicapped*, not helpful: by Section 1, any `b>=5` block
already gets `d>=5` for free, so a deliberately-pinned core only adds
"free-appendage" elements at the Section 2 marginal rate (`~1`, below the
champion's own `1.2285`), pulling the achievable rate down exactly as in
Section 2 -- consistent with the anneal-with-pinned-core runs (not
separately gated in the verifier) underperforming the unconstrained anneal.

**Diameter-stretch invariance (PROVED).** The search-steering menu
emphasizes high diameter (`#682` Corollary 2: any corridor-bound violator
needs `D > 2^{d/3+b/9}`, super-exponential). A natural first test: does
naively *stretching* a good construction raise `X`?

> **Proposition (dilation invariance).** For any block `V` and integer
> `s != 0`, let `sV = {sv : v in V}`. Then `f(sV) = f(V)`, `L(sV) = L(V)`
> (hence `X(sV) = X(V)`) exactly.

*Proof.* For `S subseteq V`, `Phi_{sV}(sS) = (|S|, s * sum_S(v),
s^2 * sum_S(v^2))` is the image of `Phi_V(S) = (|S|, sum_S(v), sum_S(v^2))`
under the injective (for `s != 0`) map `(a,b,c) -> (a, sb, s^2 c)`. Two
subsets collide under `Phi_{sV}` iff their images collide under `Phi_V`, so
the fiber-size multiset and image size are identical. ∎ (A special case of
`#643` Lemma A's general affine invariance.)

**Verifier BLOCK 6** confirms this **exactly** on the champion stretched by
`s in {1,3,21}` (diameter `32 -> 96 -> 672`): `f=30, L=151275,
X=2.343296` in every case, bit-for-bit, and again on a second, unrelated
block `{0,1,2,4,5,6}` stretched by `5`. **Reading:** high diameter is a
*necessary* condition on any corridor-interior witness (`#682` Corollary 2),
but it is manifestly **not sufficient**, and naive dilation cannot
manufacture it -- only genuinely new arithmetic structure at the larger
scale can, which is exactly the open combinatorial core (`#655` R4/R7,
`#678` Section 8) that none of the four families here supplies.

---

## 6. Why every family caps out (structural reading, connects to the `(alpha,delta)` map)

All four families are, in their own way, attempts to buy `L` cheaply
(diversity / spread) without paying for it in `f` (collisions), or vice
versa -- and all four instead reproduce the **same tensor-averaging
ceiling** identified by `#683`'s Lemma: composing (far-separating, or
grid-repeating, or lift-preserving) a known-rate gadget `k` times gives a
`k`-fold product whose *rate* (`log2(fL)/b`) is the weighted **average** of
the gadget's own rate and the champion's, never higher than the larger of
the two. Since **no known gadget** (interval, hole-pattern, modular
residue set) has ever reached a rate above the `#655` champion's own
`1.2285` (itself short of the `4/3 = 1.333` needed for `X = 2^{4/3}`), every
composition built from such gadgets is capped below it too. Section 5's
dilation-invariance result shows that *spreading alone* (the one lever
`#682`'s diameter map identifies as necessary) is exactly orthogonal to this
-- it changes `D` while leaving `(f,L,X)` fixed, so it cannot, by itself,
lift a composition off the tensor-average ceiling. Genuinely escaping the
ceiling needs a **single**, non-composite block whose internal trade
structure is richer than any known gadget's own rate -- precisely the
`(Curve-N_dis collapse)` / near-perfect-matching construction that `#678`
Section 8 and `#655` R4/R7 identify as the open core, and which this hunt's
four families (being compositional or search-limited variants of known
gadgets) do not reach.

---

## Honest residuals (OPEN)

1. **The corridor itself is untouched.** This packet is a negative result
   about four specific search families, not a new bound; `#678`'s corridor
   bound `L <= 2^{d+b/3}` remains OPEN (`#673`'s exponential-regime
   inverse-LO).
2. **Not exhaustive.** `b` was capped at `40` (families i, iii) or `36`
   (family ii, the one COMPUTED-but-ungated case) by the exact DP's cost
   (`O(b*L)`, `L` reaching `10^7` by `b~30-36`); genuinely larger `b`, or a
   meet-in-the-middle / hashing scheme beyond the incremental dict DP used
   here, could reach further and is not attempted.
3. **Anneal depth.** The direct anneal (Section 5) ran for a fixed,
   modest wall-clock budget per `b`; `#683`'s own much longer census
   (overnight-scale) at `b<=26` still found nothing better than the `b=18`
   champion, so there is no reason to expect a longer run of *this*
   anneal alone to succeed, but it is not ruled out.
4. **The CRT/modular family's wrap search** was exhaustive only for the
   `F_13` seed's `k(x) in {0,1}` class (`2^{10}`); wider wrap ranges
   (`k(x) in {0,...,K-1}`, `K>2`) and other primes/residue sets beyond the
   three sampled here are not exhaustively searched.
5. **No lower-bound-only witness was pursued.** Because every exact
   computation here stayed comfortably below `2^{4/3}` (the largest gap
   to the target, `~0.21` in `X`, is far larger than any plausible
   sampling/estimation error), a sampled lower-bound witness (per the
   task's fallback) was not needed and would not have changed the
   qualitative conclusion; it remains available as a technique for any
   future construction whose exact `L` is intractable but whose scale
   looks more promising than anything found here.

---

## Summary

```
    TARGET:    exhibit V with X(V) = (fL)^(1/b) > 2^(4/3) = 2.519842.
    MECHANISM: one-sided forcing (PROVED): f<=2^(b-d) (#668) + X>2^(4/3)
               => L>2^(d+b/3), any d, d never computed => corridor-interior
               witness for free the instant X(V)>2^(4/3) is verified.
    S0 FREE:   ceil(alpha_0*b)<=5 for b<=59 (#678 Lemma 1 gives d>=5 free)
               => the S0 half of the certificate needs no construction in
               the searched range; the hunt reduces to a pure (f,L) search.
    FAMILY i:  lacunary core + dense cluster -- NULL, best X=2.308748,
               declining as core grows (both far and same-scale variants).
    FAMILY ii: two-scale grids {a+Mc} -- NULL, best X=2.311619 (near-tensor,
               large M); interaction (small M) measurably HURTS; a b=36
               trade-grid gives X=2.185-2.217 despite f,L in the 10^5-10^7
               range (COMPUTED, not fast-gated).
    FAMILY iii:CRT/modular lift of the F_13 seed (Codex team calibration) --
               NULL, best X=2.222464 (full 2^10 wrap search, beats the raw
               modular 2.160025 but not the champion); own bigger modular
               seeds (mod 23/29/31) are WORSE (2.10-2.15).
    FAMILY iv: direct anneal (X=2.300265 at b=20) + diameter-stretch
               invariance (PROVED: dilation leaves f,L,X EXACTLY fixed,
               special case of #643 Lemma A) -- spreading alone is not a
               lever; no family beats the champion.
    OVERALL:   NULL. Max X found across all 4 families and 15 checked
               witnesses = 2.311619, vs champion 2.343296, vs target
               2.519842. The tensor/composition-averaging ceiling (#683)
               explains why every compositional family caps below the best
               known single gadget's own rate; escaping it needs a
               non-composite construction richer than any known gadget,
               which is the same open core #678 Section 8 already names.
```

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/corridor_interior_hunt.md` (this).
- Verifier: `experimental/scripts/verify_corridor_interior_hunt.py`
  (`RESULT: PASS (99/99)`, ~3s; recomputes every witness's `f, L, X` exactly,
  re-verifies the `S0` dissociation spot-checks, re-derives the forcing
  algebra and the dilation-invariance check on two blocks, and confirms the
  full `2^{10}` F_13 wrap search reproduces the reported best lift exactly).
- Read-only inputs: our `#655` `fiber_image_tradeoff.md` (champion, moment-
  curve reduction), `#643` `pte_cluster_packing_frontier.md` (affine
  invariance, Lemma A), `#673` `ilo_moment_structured.md` (the open
  exponential-regime inverse-LO wall), `#678` `curve_restricted_product.md`
  (dissociation dimension, Lemma 1, Theorem A, the corridor bound), `#682`
  `corridor_diameter_map.md` (the diameter coordinate, Corollary 2,
  search-steering), `#683` `championship_census_b19_26.md` (the tensor
  averaging lemma, the `b=19..26` census baseline); DannyExperiments `#668`
  `canonical_transversal_vc_compression.md`; scottdhughes `#564`
  `w_a_star_pte_lemma.md`. The `F_13` seed is the Codex team's calibration
  (2026-07-12), consumed read-only.

**Per-claim status.** The one-sided forcing Proposition (Section 1) =
**PROVED**. The `S0`-is-free reduction (Section 1, via #678 Lemma 1) =
**PROVED** (an elementary corollary of an already-proved fact, checked
computationally). The dilation-invariance Proposition (Section 5) =
**PROVED** (special case of #643 Lemma A, fresh proof + fresh numerical
check). Every witness's `f, L, X` in Sections 2-5 (including the two
`b=36` cases reported outside the fast gate) = **COMPUTED** (exact
enumeration or exact incremental DP, no sampling). The "every family caps
below the champion" and "interaction hurts" readings = **COMPUTED**
(direct comparison of the exact numbers) with a structural explanation
(Section 6) that is **AUDIT** (built on #683's proved tensor lemma, not a
new theorem). The overall **NULL** (no corridor-interior witness found) is
the honest, reproducible result of this hunt; it is not a nonexistence
proof (Honest residuals, items 1-2). No claim is made that the four
families are exhaustive, or that a fifth family could not succeed.

**Nonclaims.** No new bound on `X*` or the corridor. No closure of `#673`'s
exponential-regime inverse-LO. No claim that `L(V) > 2^{d+b/3}` for any
actual block (the forcing Proposition is a proved conditional, never fired
here since no `X(V) > 2^{4/3}` was found). No `.tex`/`.pdf` touched.
