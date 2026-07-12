# Designing the resonance directly: a NEW rho* record via same-block trade-stacking (b=24, rho=0.160847)

## Status

`R1-R2 THE MECHANISM (PROVED): this is exactly the task's flagged gap --
#683's positional-tensor lemma (clean Q-separated encoding) forces f=f1*f2,
L=L1*L2 (a weighted-average rate, capped by the better factor); placing the
SAME copies of hughes #564's minimal degree-2 PTE trade at a common (not
Q-separated) shift instead creates genuine cross-block collisions, and for
shift s past an explicit threshold the construction's (fstar,L1) collapses to
an exact, s-INDEPENDENT closed object (a 6-tuple aggregate-moment map), proved
here. / R3 NEW CHAMPION (COMPUTED, quadruple-verified): b=24, V = union of 4
copies of {0,1,2,4,5,6} at a common shift >=48, gives fstar=190, L1=4192627,
rho=0.160847 -- beats #655's b=18 champion (0.158411) by +0.002436, moving
the certified lower end of the unconditional bracket to rho* >= 0.160847. /
R4 WHY b=24 AND NOT b=18 (COMPUTED): the same construction at k=2,3 copies
(b=12,18) gives rho=0.110644, 0.147481 -- BELOW the old champion at matched
b; only k=4 (b=24) crosses it. A 3-copy alternative gadget (the b=8
joint-bound-saturator) gives rho=0.148558 at the same b=24, below the
4-copy minimal gadget -- more, smaller trades beat fewer, larger ones. / R5
MENU (iv) PARTIAL (COMPUTED): an informed extension of the b=18 champion
(guided by its own top-fiber structure, not blind hill-climbing) beats
#683's own per-b census at b=20,22 but caps at 0.134-0.145, far below the
new champion -- amplifying the OLD champion's resonance is not how the
record falls; a DIFFERENT resonance, designed from scratch, is. / R6 MENU
(ii) NULL (COMPUTED): rank-2 GAP designs cap around rho~0.10-0.14 at every
tested b, well below both champions. / R7 MASS TIE-IN (MEASURED): the new
champion's Fourier mass concentrates at small denominators even more than
#655's champion (extends #691's monotone-in-fiber tension measurement to
f=190). / Residual: k=5 (b=30) is MEMORY-BOUNDED in this environment before
reaching its own asymptotic plateau -- left OPEN, not ruled out.`

This packet answers the assignment directly: **design the resonance, rather
than search for it.** Our **#655** (`fiber_image_tradeoff.md`) set up the
problem -- a **block** `V` is `b` distinct integers, `Phi(S) = (|S|, sum_S x,
sum_S x^2)`, `fstar` the max fiber, `L1` the image size, `rho = (log fstar +
log L1)/b - log 2` -- and found the `b=18` champion `rho = 0.158411`. Our
**#683** (`championship_census_b19_26.md`) searched `b=19..26` across
interval-with-holes, AP-unions, perturbations, and general hill-climbing:
NULL throughout, and separately proved that composing two blocks via
**positional tensor** encoding (`V1 union {(S1+v2)Q : v2 in V2}`, `Q` huge)
always gives the size-weighted-average rate, capping any such composition at
the better of its two factors. That Lemma is airtight for the encoding it
covers. It says nothing about placing copies of the same small trade **at a
common, non-dissociating shift** -- the same-block additive stacking the task
flags as the open gap. We build exactly that, find where it peaks, and prove
why.

**One-line verdict.** **NEW CHAMPION.** `V = {0,1,2,4,5,6} union {48+v}
union {96+v} union {144+v}` (`v` ranging over the same 6-element set each
time), a **comb of 4 shifted copies of the minimal degree-2 PTE trade**
(support 6, **scottdhughes #564**), gives `fstar = 190`, `L1 = 4192627`,
**`rho = 0.160847`** -- exceeding #655's `b=18` record (`0.158411`) by
`+0.002436`. The mechanism is proved, not just observed: for shift `s`
exceeding an explicit threshold, two subsets of the comb collide **iff** their
per-block size/sum/sumsq choices agree on a fixed 6-tuple of aggregate
invariants, **independent of `s`** -- so the construction has a genuine
`s -> infinity` limit object, computed exactly by a second, s-free DP that
agrees with the direct computation to the last digit. Four independent
methods certify the same `(fstar, L1)`. The same family does **not** beat
the old champion at its own `b=18` (only at `b=24`), a smaller-trade,
more-copies design beats a larger-trade, fewer-copies one at matched `b`, and
the other three menu items (GAP design, and amplifying the OLD champion's own
resonance) cap well below both records -- so this is not a free lunch
anywhere on the menu, it is one specific, provable mechanism that happens to
cross the line at `b=24`.

Every number is recomputed by
`experimental/scripts/verify_comb_trade_champion.py` (stdlib-only, zero-arg,
`RESULT: PASS (34/34)`, ~44s under `ulimit -v 2097152` -- the champion is
re-derived by **four independent methods**: the standard sequential
subset-sum DP, meet-in-the-middle enumeration, direct brute-force weight-class
enumeration, and the s-independent aggregate-moment DP that proves the
asymptotic mechanism). The shift-scan that **discovered** the champion, the
alternative-gadget comparison, the fuller GAP sweep, and the memory-bounded
`k=5` (`b=30`) exploration live in
`experimental/scripts/repro_comb_trade_champion.py` (documented runtime,
~3 minutes, deliberately probes where the exact-DP approach becomes
infeasible in `k=5`).

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exact /
exhaustive finite enumeration), **MEASURED** (exact finite objects, trend read
off), **AUDIT** (cross-reference / recap of a prior result), **OPEN**.

**Credit.** The setting, the `rho` definition, the moment-curve reduction, and
the `b=18` champion `rho=0.158411` are **our #655** (`fiber_image_tradeoff.md`),
building on **our #643/#646/#623**. The minimal degree-2 PTE trade support `6`
is **scottdhughes #564** (`w_a_star_pte_lemma.md`) -- the exact gadget used
throughout this packet (`{0,1,2,4,5,6}`, trade `{1,2,6}` vs `{0,4,5}`, both
sum `9`, sumsq `41`). The `b=19..26` null census, the exact
size-folding positional-tensor lemma (reproduced here as the baseline this
packet's construction deliberately departs from), and the honest identification
of "same-block additive stacking" as untested territory are **our #683**
(`championship_census_b19_26.md`). The small-denominator Fourier-mass
measurement method (BLOCK 6 / R6) is **our #691** (`fenced_resonance_window.md`),
reused here on the new champion. The unconditional bracket ends
(`[0.158411, 0.405465]` before this packet) are per **#673**
(`ilo_moment_closed_consumer.md`) and **DannyExperiments #668**
(`canonical_transversal_vc_compression.md`); this packet moves only the
COMPUTED lower end.

---

## 0. Setup (AUDIT, recap)

Notation as in #655/#683: a block `V` is `b` distinct integers,
`Phi(S) = (|S|, sum_S x, sum_S x^2)`, `fstar(V)` the max fiber, `L1(V)` the
image size, `phi = log(fstar)/b`, `lambda = log(L1)/b`,
`rho = phi + lambda - log2` (natural log), `X = (fstar L1)^{1/b} = 2 e^rho`.
The reported bracket going in: `rho* in [0.158411, 0.405465]`, both ends
unconditional per #673.

**The construction menu this packet works** (as posed): (i) designed
quadratic relations -- stacked degree-2 PTE trades; (ii) small-denominator /
GAP design; (iii) multi-scale PTE stacking, specifically same-block additive
stacking (not #683's positional tensor); (iv) amplifying the `b=18`
champion's own resonance. R1-R4 below is (i)+(iii) together (they turn out to
be the same construction); R5 is (iv); R6 is (ii); R7 connects to #691's
tension measurement; the `k=5` residual (resource-bounded) is in Honest
Residuals at the end.

---

## R1 -- the construction, and why it is NOT #683's tensor (PROVED + COMPUTED)

**The gadget.** `G = {0,1,2,4,5,6}` (`b=6`), hughes #564's minimal degree-2
PTE trade: `A = {1,2,6}` and `B = {0,4,5}` are disjoint, `|A|=|B|=3`,
`sum(A)=sum(B)=9`, `sumsq(A)=sumsq(B)=41` -- the unique nontrivial collision
among `G`'s `2^6=64` subsets, giving `fstar(G)=2`, `L1(G)=63`,
`rho(G) = 0.112900` (matches #655's `b=6` row exactly).

**The comb.** For `k` copies at common shift `s`:

```
    Comb(G, k, s) := union_{i=0}^{k-1} { i*s + v : v in G } .
```

**#683's positional tensor is a DIFFERENT construction.** Their Lemma
combines two blocks `V1, V2` via `V = V1 union {(S1+v2)*Q : v2 in V2}`, with
`S1` exceeding every possible `V2`-subset sum and `Q` exceeding every possible
`V1`-subset sum (and sumsq, suitably) -- a **nested, size-folding** encoding
built precisely so that no cross term ever survives. It is exact:
`fstar(V) = fstar(V1) fstar(V2)`, `L1(V) = L1(V1) L1(V2)` (reproduced exactly
in the verifier, BLOCK 0). Reproducing this construction with `V1=V2=G`
gives `fstar=4=2^2`, `L1=3969=63^2`, `rho=0.112900` -- **exactly `G`'s own
rate**, since tensoring two copies of an identical-rate block gives the
weighted average of that rate with itself (#683's own corollary, applied to
the degenerate `b1=b2` case). No tensor composition of copies of a
`rho<0.158411` block can ever exceed `0.158411` (#683 R1.4) -- this is airtight
for the encoding it describes.

**`Comb(G,k,s)` is a different encoding: no `S1`-fold, no `Q`-separation, just
a flat common difference.** A subset `T` of the comb corresponds to a choice
`T_i subseteq G` for each block `i = 0..k-1`. Writing it out:

```
    |T|      = sum_i |T_i|
    sum(T)   = s * A + B,           A = sum_i i|T_i|,   B = sum_i sum(T_i)
    sumsq(T) = s^2*C + 2s*D + E,    C = sum_i i^2|T_i|, D = sum_i i sum(T_i),
                                    E = sum_i sumsq(T_i)
```

Unlike the tensor's `Q`, the shift `s` appears **linearly and quadratically**
in a single coordinate rather than isolating each block into its own digit
range -- so `A` and `C` (integer combinatorial data about the SIZE choices
`|T_i|` alone) can coincide across genuinely different `(T_0,...,T_{k-1})`
tuples, creating collisions the tensor construction is built to avoid. This
is the task's flagged gap, made concrete.

**A first, small instance already beats the clean tensor (COMPUTED, verifier
BLOCK 1).** At `k=2`, the small-shift stack `G union (10+G)` (`b=12`) gives
`fstar=6, L1=3579, rho=0.138069` -- comfortably above the clean tensor's
`0.112900` for the same two blocks. This is the demonstrative instance of the
opening; R2-R3 push it to where it actually sets a new record.

---

## R2 -- the asymptotic structure is exact and s-independent (PROVED, verifier BLOCK 2-3)

**Theorem (aggregate-collision characterization).** Fix a NON-NEGATIVE gadget
`G` (size `n`, `SG := sum(G)` -- the max possible `|sum(T_i)|` over
`T_i subseteq G`, attained at `T_i=G` since `G >= 0` -- and `QG := sumsq(G)`,
similarly the max possible `sumsq(T_i)`) and `k` copies. (For a gadget with
negative elements, replace `SG, QG` by the true max-subset bounds; both
`PROUHET` and `GADGET8` used in this packet are non-negative, so `SG=sum(G)`
literally.) Define

```
    s_0 := max( k*SG + 1,
                ceil( Dmax + sqrt(Dmax^2 + Emax) ) + 1,
                ceil( Emax/2 ) + 1 ),
    where  Dmax = SG * k(k-1)/2,   Emax = k*QG .
```

For every shift `s > s_0` (in particular, uniformly over ALL such `s`), two
subsets `T, T'` of `Comb(G,k,s)` satisfy `Phi(T) = Phi(T')` **if and only if**
their per-block decompositions agree on all six aggregate invariants
`(W,A,C,B,D,E)` defined above (`W = sum_i|T_i|`).

*Proof.* (<=) is immediate: `(|T|,sum(T),sumsq(T))` is a fixed function of
`(W,A,C,B,D,E)` for any `s`, so equal aggregates give equal `Phi` regardless
of `s`. (=>) Suppose `Phi(T)=Phi(T')`. From `s*A+B = s*A'+B'`: if `A != A'`
then `s = |B-B'|/|A-A'| <= |B-B'| <= k*SG` (since `B,B' in [0,k*SG]` and
`|A-A'| >= 1`), contradicting `s > k*SG`; so `A=A'`, hence `B=B'`. Then from
`s^2 C + 2sD + E = s^2 C' + 2sD' + E'` with `A=A'` established: if `C != C'`,
`s^2 <= s^2|C-C'| = |2s(D-D')+(E-E')| <= 2s*Dmax + Emax`, i.e.
`s <= Dmax + sqrt(Dmax^2+Emax)`, contradicting `s > s_0`; so `C=C'`. The
equation reduces to `2s(D-D') = E'-E`; if `D != D'`, `s <= Emax/2`,
contradicting `s > s_0`; so `D=D'`, and then `E=E'`. ∎

This threshold is an explicit, **sufficient** bound -- not claimed tight (the
verifier's negative control, BLOCK 3, confirms `s=10` genuinely does NOT match
the plateau, so the distinction is real, not vacuous). For `(G,k) = (PROUHET,
4)`: `SG=18, QG=82, Dmax=108, Emax=328`, giving the three component bounds
`k*SG+1 = 73`, the quadratic-term bound `= 219`, the linear-term bound
`= 165` -- `s_0 = max(73,219,165) = 219`, all COMPUTED in the verifier.

**Consequence: a clean, s-free computation.** `fstar` and `L1` of
`Comb(G,k,s)` (`s > s_0`) equal the max fiber and image size of the **6-tuple
aggregate-moment map** `(W,A,C,B,D,E)` over `(2^G)^k` -- computable directly
by a DP over the `k` blocks that never mentions `s` at all (verifier BLOCK 2,
Method 4). For `(PROUHET, k=4)` this gives `fstar_inf = 190`, `L1_inf =
4192627` **exactly matching** the direct DP at `s=48` (COMPUTED: the plateau
is empirically reached far below the proved-safe `s_0=219`) and at `s=219`
itself, `s=269`, `s=500` (all checked). Four methods, one number.

---

## R3 -- THE NEW CHAMPION: b=24, rho=0.160847 (COMPUTED, quadruple-verified)

```
    V = {0,1,2,4,5,6, 48,49,50,52,53,54, 96,97,98,100,101,102, 144,145,146,148,149,150}
    b = 24     fstar = 190     L1 = 4192627     rho = 0.160847     X = 2.349011
```

(`s=48` here -- any `s >= 48`, or in particular any `s > 219`, gives the
identical `(fstar, L1)` by R2's theorem; `s=48` is simply the smallest shift
at which the plateau was found to already hold exactly, reported as the
concrete witness.) This **beats #655's certified `b=18` champion
(`rho=0.158411`) by `+0.002436`**, moving the bracket's computed lower end to

```
    rho* >= 0.160847     (X* >= 2.349011)
```

**Four independent derivations agree exactly** (verifier BLOCK 2):

1. **Sequential subset-sum DP** (the standard method used throughout
   #655/#683/#691): `fstar=190, L1=4192627`.
2. **Meet-in-the-middle**: split `V` into two 12-element halves, brute-force
   each half's `2^12` subsets exactly, convolve the two signature
   multisets (`4096 x 4096` pairs) -- a fully independent algorithm.
   Agrees exactly.
3. **Direct brute-force weight-class enumeration**: the argmax signature is
   `(w,s,q) = (12, 900, 102116)`; directly enumerating all
   `C(24,12) = 2704156` weight-12 subsets and counting exact matches gives
   `190` -- the same DP-independent style of cross-check #655/#683 used for
   their own champions.
4. **The s-independent 6-tuple aggregate-moment DP** (R2): `190, 4192627`,
   proving this is not a coincidence of the specific shift `48` but the
   provable limit value for the entire family `s > s_0`.

This is not a marginal, borderline-precision result: `0.160847 - 0.158411 =
0.002436`, about `1.5%` of the previous margin over the next-best census
value, and the plateau holds identically over a `450`-wide range of shifts
(`s = 48` through `500`), so it is not sensitive to any particular numeric
choice.

---

## R4 -- this family peaks at k=4/b=24, not at the old champion's b=18 (COMPUTED)

The same construction at other `k` (verifier BLOCK 4):

```
    k    b    gadget     fstar_inf     L1_inf     rho_inf     vs 0.158411
    2   12    PROUHET        4           3863     0.110644    below
    3   18    PROUHET       23         162075     0.147481    below (!)
    4   24    PROUHET      190        4192627     0.160847    NEW CHAMPION
```

At `k=2` the asymptotic `fstar` equals the naive product `f1*f2=4` exactly --
with only two blocks, the "leading coefficient" `A = sum_i i|T_i|` is just
`|T_1| in {0,...,6}`, all distinct, so no aggregate collision is possible and
the family cannot beat the plain tensor at all. At `k=3` (**the OLD
champion's own `b=18`**), the asymptotic rate `0.147481` is comfortably
**below** `0.158411` -- this specific family does not touch the old record at
its own size; only at `k=4/b=24` does the accumulated aggregate-collision
structure (now genuinely 3-dimensional: `A,C` each range over enough values
that ties become common) cross the line. This is a real, checked
non-monotonicity, not an assumption: `k=5/b=30` was attempted and is
MEMORY-BOUNDED before reaching its own plateau (R7); whether it exceeds
`0.160847` is open.

**More, smaller trades beat fewer, larger trades at matched `b` (COMPUTED).**
Repeating the construction with the alternative `b=8` gadget (`{0,1,2,3,6,7,
8,9}`, hughes-#564-style, saturating #623's joint bound `f+L=2^b+1` exactly,
`#655`'s own `b=8` row) at `k=3` copies (also `b=24`):

```
    gadget      k    b    fstar_inf    L1_inf     rho_inf
    PROUHET     4   24       190      4192627    0.160847   <- champion
    b=8 gadget  3   24       104      5703121    0.148558
```

Four copies of the smaller (support-6) gadget beat three copies of the larger
(support-8) gadget at the identical total size -- more independent
aggregate-collision "slots" (`k=4` vs `k=3`) matters more than each slot's
individual richness. (Reproduced in `repro_comb_trade_champion.py`, BLOCK R2;
cited, not re-run, by the fast verifier -- the `2^8=255`-signature alphabet
makes this specific check cost ~9s on its own.)

---

## R5 -- menu (iv): amplifying the OLD champion's own resonance (COMPUTED, PARTIAL)

Per the menu's instruction, we extracted the `b=18` champion's actual
collision structure (all `30` subsets realizing its max fiber `(w,s,q) =
(9,162,3792)`) and used a **fast incremental prescan** (`O(L1)` per candidate
new element, not a full `O(b*L1)` re-derivation) to find which single
elements, when adjoined, best exploit that structure -- an *informed* search,
not #683's blind hill-climb. Chaining the best symmetric-offset pair-adds:

```
    b    added offset (about center 18)   fstar    L1        rho          vs #683's own b-census
   20    +/-31                              33     574502    0.144741     beats 0.142978
   22    +/-30 (cumulative)                 63    1618338    0.145037     beats 0.144797
   24    +/-46 (cumulative)                 83    5039960    0.134009     (#683 reported 0.130839 at b=24)
```

So informed champion-extension **does** out-perform #683's own per-`b`
census at `b=20` and `b=22` (confirming the prescan method has some genuine
power over blind search), and even its `b=24` value edges past #683's
reported `b=24` census (`0.134009 > 0.130839`). But it caps far below the
`comb` champion's `0.160847` at the same `b=24` -- amplifying the *old*
resonance runs into the same ceiling #683 already found (dense
interval-with-holes structures decay once pushed past their natural diameter,
R6 of #655), while the *new*, designed resonance (R1-R3) does not, because it
is not a perturbation of the old structure at all.

---

## R6 -- menu (ii): small-denominator / GAP design (COMPUTED, NULL)

Rank-2 GAP blocks `V = {i + j*g2 : 0<=i<n1, 0<=j<n2}` (`g1=1` WLOG,
`g2 != n1` so it is not just a relabeled interval), swept over
`n1,n2 in [2,8]` and `g2` in a bounded window (diameter capped at `3b`, per
#655's own box-bound reasoning that large relative diameter is already a
dead end):

```
    b     best rank-2 GAP rho     vs best known at that b
    12          0.131684           below 0.1414 (interval-with-holes)
    18          0.136924           below 0.158411 (old champion)
    20          0.139478           below 0.142978 (#683 census)
    24          0.138002           below 0.160847 (new champion)
```

Every entry stays in `rho ~ 0.10-0.14`, well below whatever is already known
at that `b` -- consistent with #683's own related finding that unions of a
few APs top out similarly. A genuine rank-2 lattice spreads mass too evenly
across residues to concentrate the fiber the way a **degenerate** (trade-based)
collision does; the small-denominator resonance #691 measures (R7 below)
turns out to live in exact repeated-trade structure, not in a generic
modular grid. (Full sweep to `b<=26`: `repro_comb_trade_champion.py`
BLOCK R3.)

---

## R7 -- tying the new champion to #691's tension measurement (MEASURED)

**#691** (`fenced_resonance_window.md`) measured that a block's Fourier mass
`|Xhat|` concentrates at **small denominators** of the dominant resonance as
the fiber grows (`mass(den<=5)`: `0.32` Sidon `-> 0.55` old champion,
monotone in `f`). Repeating that exact measurement (same `absXhat` method,
credited) on the new champion, at a resolution scaled to its larger diameter
(`150` vs the old champion's `32` -- the coarse grid #691 used for a
diameter-`32` block visibly under-resolves a diameter-`150` one, so absolute
mass values are grid-sensitive; the **ordering** is checked to be stable
across grid choices, verifier BLOCK 6):

```
    block          fstar    mass(den<=5) at grid=(150,150,6)
    sidon12          1            0.059
    old champ18     30            0.213
    NEW CHAMP       190            0.556
```

The monotone trend **extends** to this much higher fiber: the new champion's
mass is even more concentrated at small denominators than the old champion's,
consistent with #691's reading that high fiber and small-denominator
resonance go together. This is exactly what the comb construction's mechanism
(R2) predicts qualitatively: the aggregate-collision structure that produces
the large fiber is a **highly repetitive, low-complexity** arithmetic
pattern (four literal copies of a 6-element set), which is about as
"small-denominator" a resonance as a block can have. The new champion does
not escape the tension #691 identified -- it is a particularly extreme point
along the same axis.

---

## Honest residuals (OPEN)

1. **k=5 (b=30) is memory-bounded, not resolved.** The same `Comb(PROUHET,
   5, s)` family was attempted; at the shifts tried (`s=8,10,12`) `L1` was
   already `2.9M-8.1M` and climbing steeply, and this environment's exact-DP
   approach (a Python dict keyed by `(size,sum,sumsq)` triples) hits a
   `MemoryError` before the shift is large enough to see this family's own
   asymptotic plateau (by analogy with `k=2,3,4`, that plateau likely needs a
   substantially larger shift, hence a substantially larger `L1`). **Not
   ruled out**: `k=5` might exceed `0.160847`; it might not. `b=25..29`
   (non-multiples of `6`) and `b=30` via other `(gadget, k)` combinations
   (e.g. `5` copies of a smaller gadget, if one existed below support `6` --
   none does, by hughes #564's minimality) are likewise unexplored here.
2. **The threshold `s_0` is proved but not tight.** The proof (R2) gives
   `s_0=219` for `(PROUHET, k=4)`; the plateau is empirically reached by
   `s=48`. Sharpening the bound (or finding the exact minimal `s` at which
   the plateau first holds) is not attempted.
2b. **No general formula for `fstar_inf(k)`, `L1_inf(k)` in closed form.**
   R2 reduces the asymptotic values to an explicit, exactly-computable DP
   (the 6-tuple aggregate-moment map), but does not give a closed-form
   expression for `190` or `4192627` as a function of `k`; the qualitative
   jump between `k=3` (below record) and `k=4` (new record) is observed and
   computed, not explained by a formula.
3. **Whether an even better `(gadget, k, arrangement)` exists is open.** We
   tried the minimal support-6 gadget and one alternative (support-8); we did
   not search over all possible gadgets, nor over non-uniform per-block
   shifts (`i -> c_i` for an arbitrary increasing integer sequence `c_i`
   rather than the flat AP `i*s`), which is a strictly larger design space
   than what this packet covers. The mechanism (R2) generalizes to any
   sequence of per-block weights, not just `0,1,2,...,k-1`; whether a
   different weight sequence does better at the same total `b` is untested.
4. **The unconditional bracket's upper end is untouched.** This packet moves
   only the COMPUTED lower end (`0.158411 -> 0.160847`); `#673`'s conditional
   / unconditional upper-end analysis (`log 2` conditional on `(ILO-moment)`,
   `log(3/2)` unconditional) is not engaged here.

---

## Summary

```
    TARGET:  rho* > 0.158411 at some b <= ~30, via a construction #683 did not try.

    NEW CHAMPION (COMPUTED, quadruple-verified):
        V = 4 shifted copies of hughes #564's minimal degree-2 PTE trade
        {0,1,2,4,5,6} at common shift s>=48 (any s > the PROVED threshold
        s_0=219 gives the identical exact values).
        b=24   fstar=190   L1=4192627   rho=0.160847   X=2.349011
        (beats #655's b=18 champion 0.158411 by +0.002436)

    MECHANISM (PROVED): #683's positional-tensor lemma forces a weighted-
        average rate for a SEPARATE, Q-isolating encoding; the SAME-shift
        comb is a different encoding whose collisions are governed by an
        explicit, s-independent 6-tuple aggregate-moment map for s past a
        proved threshold -- the task's flagged gap, made rigorous.

    WHY b=24: this exact family gives rho=0.110644 (k=2,b=12), 0.147481
        (k=3,b=18, BELOW the old champion at its own size), 0.160847
        (k=4,b=24, NEW CHAMPION); a 3-copy support-8 alternative at the same
        b=24 gives only 0.148558 (more, smaller trades wins).

    OTHER MENU ITEMS:
      (ii) small-denominator/GAP design: NULL, caps ~0.10-0.14 at every b.
      (iv) informed b=18-champion amplification: beats #683's own per-b
        census at b=20,22 but caps at 0.134-0.145, far below the new record.

    MASS TIE-IN (MEASURED): the new champion's Fourier mass concentrates at
        small denominators even more than the old champion's (extends #691's
        monotone-in-fiber tension finding to f=190) -- the champion does not
        escape that tension, it sits at an extreme point of it.

    BRACKET: rho* in [0.158411, 0.405465]  ->  rho* in [0.160847, 0.405465]
        (lower end COMPUTED, quadruple-verified; upper end unchanged, per #673).

    OPEN: k=5 (b=30), memory-bounded in this environment; the exact
        s_0-vs-empirical-convergence gap; non-uniform per-block weight
        sequences; other gadgets.
```

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/comb_trade_champion.md` (this).
- Verifier: `experimental/scripts/verify_comb_trade_champion.py`
  (stdlib-only, zero-arg, `RESULT: PASS (34/34)`, ~44s; re-derives the new
  champion by four independent methods, the asymptotic-threshold lemma with a
  negative control, the k=2/k=3 comparison points, the menu-(iv) chain, the
  menu-(ii) GAP sample, and the #691-style mass measurement).
- Reproducer: `experimental/scripts/repro_comb_trade_champion.py` (documented
  runtime, ~3 minutes; the shift scan that discovered the champion, the
  GADGET8 comparison, the full GAP sweep, and the memory-bounded k=5
  exploration).
- Read-only inputs: `#655` `fiber_image_tradeoff.md`, `#683`
  `championship_census_b19_26.md`, `#691` `fenced_resonance_window.md`,
  `#673` `ilo_moment_closed_consumer.md`, DannyExperiments `#668`
  `canonical_transversal_vc_compression.md`; scottdhughes `#564`
  `w_a_star_pte_lemma.md`.

**Per-claim status.** R1 (the comb construction, its distinction from #683's
tensor, the small demonstrative instance) = **PROVED** (the distinction) +
**COMPUTED** (the instance). R2 (the aggregate-collision theorem and its
proof) = **PROVED**; the specific threshold value `219` and the plateau
values = **COMPUTED**. R3 (the new champion and its quadruple verification)
= **COMPUTED**. R4 (the k-dependence table, the GADGET8 comparison) =
**COMPUTED**. R5 (the champion-extension chain) = **COMPUTED**. R6 (the GAP
sweep) = **COMPUTED**, null. R7 (the mass measurement) = **MEASURED** (exact
finite objects; the coarse-quadrature absolute values are grid-sensitive,
the monotone ordering is the checked, stable claim, exactly as #691 labels
its own analogous finding). Honest residuals = **OPEN**.

**Nonclaims.** No claim about `k=5` (b=30) one way or the other -- explicitly
left open, not folded into either the champion or a null. No claim that the
comb family is the GLOBAL optimum at `b=24` (only that it beats every prior
census entry at every `b` tried). No re-derivation of `#655`/`#683`/`#691`'s
own theorems beyond the audited recaps in Section 0 and the exact
reproduction of #683's tensor lemma in R1. No `.tex` touched.
