# The curve-restricted product bound: fL <= X^b via the dissociation dimension

## Status

`SETUP: DannyExperiments #668's compression bound fL <= 3^b re-expressed through
the dissociation dimension d(V); X := (fL)^{1/b}, rho = log(X/2), the danger for
X=3 localized to d/b = 1/3 (PROVED) / LEMMA 1: d >= 5, every 5-subset
dissociated (PROVED) / LEMMA 2 (Pajor refinement): L <= N_dis(d) := #{dissociated
subsets of size <= d} <= SS(d), strict whenever a trade of support <= d exists
(PROVED) / LEMMA 3 (dissociation box bound): 2^d <= (d+1)(dD+1)(dD^2+1), so
d = O(log(bD)); bounded/poly-diameter => X <= 2 + o(1) (PROVED, reproves #655 R6)
/ LEMMA 2b (signed-span, Codex team route cut): outside columns are signed
{-1,0,1}-combinations of a maximum dissociated set, so L <= (2m+2)^d (PROVED;
dominated by Sauer-Shelah for the count, but the structure drives the corridor) /
THEOREM A (corridor localization): X <= 2^{h(d/b)}; d >= 2b/3 => X <= 2^{4/3} =
2.5198 and d/b <= 0.0845 => X <= 2.5198, so any block with X > 2.5198 lives in the
corridor d/b in (0.0845, 2/3); d >= b/2 => X <= 2^{2-d/b} <= 2.8284 (PROVED, Codex
2.52 framing) / THEOREM B (corner localization): X >= 3-delta => f,L >= ((3-delta)/2)^b,
d/b -> 1/3, both #668 bounds asymptotically tight, diameter >= 2^{Omega(b)}
(PROVED) / S2 overdetermination: b - d <= #{forced outside x}, each forced x
overdetermined (x AND x^2 fixed) (PROVED); does NOT give d >= b - poly(d) because
the forced-tuple count is exponential for designed blocks (this is the S2 tension,
RESOLVED) / AMPLIFICATION (Codex team route cut): positional Q-power encoding
tensors the champion on the curve (f_k=f^k, L_k=L^k, exponential heights) forcing
X* >= 2.3433 = 2^{1.228539} (PROVED lower guard) / WALL: closing the corridor at
2^{4/3} is exactly the OPEN bound L <= 2^{d + b/3} there (equivalently
(Curve-N_dis collapse) `N_dis(d) <= 2^{-cb} SS(d)`, reduction PROVED) = #673's OPEN
exponential-regime inverse-LO; so the honest bracket is X* in [2.3433, 3], and
closing the corridor would give X* in [2.3433, 2.5198] / FRONTIER: every computed
block (b <= 18) has d/b >= 0.611, X <= 2.3433; the corridor interior (near d/b=1/3)
is empty of computed blocks; champion X = 2.3433 (COMPUTED / MEASURED)`.

This packet is a **curve-restricted refinement** of DannyExperiments **#668**
(`canonical_transversal_vc_compression.md`). #668 proves, for subset-sum maps into
ANY abelian group, `f <= 2^{b-d}` and `L <= sum_{j<=d} binom(b,j)`, hence the
universal `fL <= 3^b`. This note specializes to the **distinct-integer degree-2
moment curve** weights `a_i = (1, v_i, v_i^2)` and asks the sharper question our
#673/#655/#643 lane poses: **is `fL <= X^b` with an explicit `X < 3`?** We do not
close it unconditionally (the wall is #673's), but we (i) prove new curve-specific
refinements of #668's two inequalities (the Pajor bound `L <= N_dis(d)`, the
signed-span bound `L <= (2m+2)^d`, and the dissociation box bound); (ii) prove,
with the **Codex team's corridor framing**, that **`X <= 2^{4/3} = 2.5198`
everywhere outside the corridor `d/b in (0.0845, 2/3)`** (in particular for every
computed block); (iii) reproduce the **Codex amplification** forcing `X* >= 2.3433`
on the curve; and (iv) resolve the S2 tension and restate the exact remaining wall
as the single self-contained corridor bound `L <= 2^{d + b/3}`. Net: the honest
bracket is `X* in [2.3433, 3]`, tightening to `[2.3433, 2.5198]` once the corridor
closes.

Every number below is recomputed by
`experimental/scripts/verify_curve_restricted_product.py` (stdlib-only, zero-arg,
`RESULT: PASS (147/147)`, ~22 s / <56 MB under `ulimit -v 2097152`; every witness
`f, L, d`, every box count, `N_dis`, `#shattered`, and frontier bin re-derived
exactly).

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exact
enumeration), **MEASURED** (exact finite objects, trend read off), **AUDIT**
(cross-reference), **OPEN**.

**Credit.** The base theorem `f <= 2^{b-d}`, `L <= SS(d)`, `fL <= 3^b` and the
Sauer--Shelah / min-cost-representative method are **DannyExperiments #668**
(`canonical_transversal_vc_compression.md`); this note is a subclass refinement
and he owns the compression method. Built on **our #673**
(`ilo_moment_structured.md`: the `(ILO-moment)` wall, the AP/GAP box bounds, the
Freiman chain, the champion cross-check), **our #655**
(`fiber_image_tradeoff.md`: the moment-curve reduction `rho = phi + lambda - log2`,
the `b=18` champion `fstar=30, L1=151275`, the sphere-packing one-trade bound and
the "one trade is too weak" lesson, `phi* = log2`), **our #643**
(`pte_cluster_packing_frontier.md`: `rho = phi + lambda - log2`, affine invariance,
Lemma B trade-deficit), and **our #623** (`pte_extremality_image_face.md`: the
`(fstar, L1)` wall). The minimal degree-2 PTE trade support **6** is
**scottdhughes #564** (`w_a_star_pte_lemma.md`). The universal-weights constant
`X* in [2.450, 3]` (a paired-tag counterexample beating `sqrt(6)`) is the **Codex
team's** side (TEAM_BOARD 01:25Z); our lane is strictly the curve-restricted
subclass, no overlap. Three banked **Codex team route cuts (TEAM_BOARD 03:02Z)**
are consumed here with credit: the **signed-span bound** `L <= (2m+2)^d` (Section
2b), the **corridor framing** `fL <= 2^{4b/3}` outside `d/b in (~0, 2/3)` (Section
4), and the **positional-encoding amplification** forcing `X* >= 2.3433` on the
curve (Section 7), together with the exact counterguard numbers reproduced in the
verifier. Pajor's lemma (`|R| <= #shattered`) is classical.

---

## 0. Setup: #668 through the dissociation dimension (AUDIT + PROVED)

A **block** `V` is `b` distinct integers. For `S subseteq V` the degree-2
signature is `Phi(S) = (|S|, sum_{x in S} x, sum_{x in S} x^2)`; equivalently the
subset-sum of the moment-curve columns `a_i = (1, v_i, v_i^2)`. Write

```
    f = fstar(V) = max_y #{S : Phi(S) = y},        L = L1(V) = #{Phi(S) : S subseteq V}.
```

`I subseteq V` is **subset-dissociated** iff the `2^{|I|}` signatures of its
subsets are distinct, and `d = d(V) = max{|I| : I dissociated}`. Because the first
coordinate `|S|` pins cardinality, two subsets collide iff, after deleting their
intersection, they form an **equal-size degree-2 PTE trade** `(A, B)` with
`|A| = |B|`, `sum_A = sum_B`, `sum_A^2 = sum_B^2`; the minimal support of such a
trade is `6` (`3` per side, hughes #564). So dissociated = **contains no
equal-size degree-2 PTE trade**.

**The rate coordinates.** Put `X := (fL)^{1/b}`, so `fL <= X^b` by definition, and
(natural logs, matching #655/#643)

```
    rho = (log f + log L)/b - log 2 = log( (fL)^{1/b} / 2 ) = log(X/2),   X = 2 e^rho.
```

(Verifier BLOCK 0.) Thus `X <= 3  <=>  rho <= log(3/2) = 0.405465`, and the
current bracket is `rho* in [0.158411, 0.405465]`, i.e. `X* in [2.3433, 3]` (lower
end = #655's `b=18` champion, upper end = #668).

**#668 in these terms (AUDIT).** `f <= 2^{b-d}` and `L <= min(2^b, SS(d))` where
`SS(d) := sum_{j=0}^{d} binom(b,j)`. Hence, writing `alpha = d/b`,

```
    fL <= 2^{b-d} min(2^b, SS(d)) = 2^{ h(alpha) b },
    h(alpha) := (1 - alpha) + H_2( min(alpha, 1/2) ),                 (envelope)
```

with `H_2` the binary entropy (base 2). `h` **increases on `[0, 1/3]` and
decreases on `[1/3, 1]`**, with a single interior maximum

```
    max_alpha h(alpha) = h(1/3) = log2 3 = 1.584963   (X = 2^{log2 3} = 3),
```

recovering #668's `fL <= 3^b` (verifier BLOCK 0 checks `2^{b-d} SS(d) <= 3^b` for
every `d` and every `b in {12,18,30}`). **The single most important structural
fact of this note:**

> `h(alpha) < log2 3` for every `alpha != 1/3`. So a block can approach `X = 3`
> **only** if its dissociation ratio `d/b` sits at `1/3`. Two representative
> off-peak values (verifier BLOCK 0): `h(1/2) = 1.5` (`X = 2.8284`),
> `h(1/6) = 1.4834` (`X = 2.7960`).

Everything below is about where `d/b` actually lives on the moment curve, and what
extra the curve buys inside the two inequalities.

---

## 1. LEMMA 1 -- `d(V) >= 5` (PROVED, verifier BLOCK 2)

> **Lemma 1.** For every block with `b >= 5`, every 5-element subset is
> dissociated; hence `d(V) >= 5`.

*Proof.* A dissociation failure inside `I` is an equal-size degree-2 PTE trade
`(A, B)` supported on `A cup B subseteq I` with `|A| = |B| >= 3`, so its support
`|A cup B| = |A| + |B| >= 6`. (Unequal-size trades are excluded by the cardinality
coordinate `|S|`: `Phi(A) = Phi(B)` forces `|A| = |B|`, so the relevant minimal
support is that of **equal-size** degree-2 trades, `= 6`, hughes #564 -- not the
smaller support of general PTE systems.) A 5-set has no subset of size `>= 6`,
hence no trade, hence is dissociated. ∎

The verifier confirms on `interval12` and the `b=18` champion that all
`binom(b,5)` 5-subsets are dissociated while some 6-subset is a trade (support
exactly 6). Lemma 1 pins the S1 base but does not grow with `b`; the content is in
Lemmas 2--3 and Theorems A--B.

---

## 2. LEMMA 2 -- the Pajor refinement `L <= N_dis(d)` (PROVED, verifier BLOCK 3)

#668 bounds `L` by Sauer--Shelah applied to the min-cost representative family
`R` (one representative per fiber, so `|R| = L`), using its two facts: **(a)**
every set shattered by `R` is subset-dissociated, and **(b)** `VCdim(R) <= d`.
Inserting **Pajor's lemma** between them gives a strictly curve-specific bound.

> **Lemma 2.** `L(V) <= N_dis(d) := #{ J subseteq V : J dissociated, |J| <= d }
> <= SS(d)`. The first inequality is **strict** whenever `V` has a trade of
> support `<= d` (in particular whenever `f >= 2` and the minimal trade support is
> `<= d`, i.e. for essentially every block with `b >= 12`).

*Proof.* Pajor's lemma: for any set system `R subseteq 2^V`,
`|R| <= #{ J : J shattered by R }`. By #668(a) every shattered `J` is
dissociated, and by #668(b) `|J| <= VCdim(R) <= d`. Therefore

```
    L = |R| <= #{ J shattered by R } <= #{ J dissociated, |J| <= d } = N_dis(d) <= SS(d).
```

Strictness: if `V` has a trade `T` of support `s <= d`, then `T` is a
non-dissociated set of size `s <= d`, so it is one of the `SS(d)` sets of size
`<= d` that is **not** counted in `N_dis(d)`; hence `N_dis(d) <= SS(d) - 1 < SS(d)`.
∎

This is a genuine unconditional improvement of #668's `L <= SS(d)` on the moment
curve: it replaces "all sets of size `<= d`" by "the **dissociated** sets of size
`<= d`", and every trade removes a macroscopic block of the difference. Verifier
BLOCK 3 checks the **entire chain** `L <= #shattered <= N_dis(d) <= SS(d)` by
direct enumeration for `b <= 11` and `L <= N_dis(d) < SS(d)` for `b <= 12`:

```
    block         b   L      #shattered   N_dis(d)   SS(d)
    interval8     8   247    249          249        255
    interval10   10   908    951          951       1013
    champ_ish10  10   952    969          972       1023
    interval12   12  3067    ---         3535       4017     (N_dis/SS = 0.880)
    champ12      12  3315    ---         3580       4017     (N_dis/SS = 0.891)
```

**Why it does not (yet) give `X < 3`.** A single support-`6` trade removes only the
`sum_{i<=d-6} binom(b-6,i)` sets of size `<= d` that contain it -- a **constant
factor** of `SS(d)` at `d = b/3` (`~ SS(b/3)/45` in the exponent-leading term), so
`N_dis(b/3) <= (1 - o(1)) SS(b/3)` and the rate is unmoved. Cutting `N_dis(b/3)`
by a constant **exponent** needs many disjoint small trades -- the same
near-perfect-matching obstruction #655 R4 identified. Lemma 2's value is that it
recasts that obstruction as a clean count of dissociated sets (Section 8).

## 2b. LEMMA 2b -- the signed-span bound (PROVED, Codex team route cut, verifier BLOCK 3b)

A dual bound, banked by the **Codex team (TEAM_BOARD 03:02Z)**, controls `L` from
the *outside* elements rather than the dissociated core.

> **Lemma 2b.** Let `D` be a **maximum** dissociated set, `d = |D|`, `m = b - d`.
> Every outside column `a_x = (1, x, x^2)` (`x in V \ D`) is a signed
> `{-1,0,1}`-combination of the `D`-columns. Consequently
> `L(V) <= (2m + 2)^d`.

*Proof.* Maximality gives disjoint `A', B subseteq D` with `Phi(A' cup {x}) =
Phi(B)` (the trade witnessing `x`), i.e. `a_x = sum_{i in B} a_i - sum_{i in A'}
a_i`, a `{-1,0,1}`-combination of `D`-columns. Now for any `S subseteq V`, writing
`S_0 = S cap D` and `S_1 = S \ D`,

```
    Phi(S) = sum_{i in S_0} a_i + sum_{x in S_1} a_x
           = sum_{j in D} c_j a_j,   c_j = [j in S_0] + sum_{x in S_1} eps^{(x)}_j,
```

with each `eps^{(x)} in {-1,0,1}^D`. Since `|S_1| <= m`, every coordinate `c_j in
[-m, m+1]`, a range of `2m+2` integers. Distinct signatures need distinct
coefficient vectors, so `L = #{Phi(S)} <= #{(c_j)_{j in D}} <= (2m+2)^d`. ∎

**Reading (verifier BLOCK 3b).** The count `(2m+2)^d` is **dominated by
Sauer--Shelah** `SS(d)` throughout the relevant range (`SS(d) < (2m+2)^d` for all
`d >= 1`, checked on the witnesses), so Lemma 2b does not by itself beat #668's
`L`-bound. Its value is **structural**: it is the S2 overdetermination (Section 6)
in global form -- "the whole block is a signed span of its dissociated core" -- and
it makes the two clean endpoints of Theorem A explicit. In particular the large-`d`
end `d >= 2b/3` gives `f <= 2^{b/3}`, `L <= 2^b`, hence `fL <= 2^{4b/3}` (the Codex
`X <= 2.52` regime), and the very-small-`d` end is where the signed span is tight.
The corridor is where both this bound and Sauer--Shelah are weak (Section 4).

---

## 3. LEMMA 3 -- the dissociation box bound (PROVED, verifier BLOCK 4)

> **Lemma 3.** Affine-normalize `V` (`min = 0`, so `V subseteq [0, D]`, `D` the
> diameter). Any dissociated set of size `k` satisfies `2^k <= (k+1)(kD+1)(kD^2+1)`.
> Hence `d(V) <= 3 log2 D + O(log b)`, i.e. `d = O(log(bD))`.

*Proof.* If `J` is dissociated its `2^k` subset-signatures `(|S|, sum, sum^2)` are
distinct and lie in the integer box `[0,k] x [0,kD] x [0,kD^2]`, which has
`(k+1)(kD+1)(kD^2+1)` points. Since `(k+1)(kD+1)(kD^2+1) <= (k+1)^3 D^3`, taking
`log2` gives `k <= 3 log2 D + 3 log2(k+1)`, so `k = 3 log2 D + O(log log D)`. ∎

> **Corollary (bounded/poly diameter => `X -> 2`).** If `D = poly(b)` then
> `d = O(log b)`, so `d/b -> 0`, and by the envelope
> `X <= 2^{h(d/b)} = 2 + O((log b)^2 / b) -> 2`. (`h(eps) = 1 + eps log2(1/eps) +
> O(eps)`.)

This **reproves #655 R6** ("bounded relative diameter => `rho -> 0`") by a
different, purely combinatorial route -- distinct 3-dimensional signatures cannot
be too many -- and makes the limit explicit (`X -> 2`, not merely `rho -> 0`).
Verifier BLOCK 4 confirms `2^d <= (d+1)(dD+1)(dD^2+1)` on `interval12`
(`d=9, D=11`), the champion (`d=12, D=32`), and a Sidon block (`d=10, D=80`), and
prints the interval `d`-growth table (Section 6). **Two consequences feed the main
theorems:** small `d` forces small diameter is false, but small diameter forces
small `d`; and conversely `d/b = 1/3` (the danger ratio) **requires**
`D >= 2^{Omega(b)}` -- the danger blocks are exactly the exponential-diameter /
tensor-limit blocks, never a bounded-diameter family.

---

## 4. THEOREM A -- corridor localization; X <= 2.5198 off the corridor (PROVED, verifier BLOCK 5)

Adopting the **Codex team's corridor framing (TEAM_BOARD 03:02Z)**: the envelope
`h(alpha) = 4/3` at `alpha = 2/3` (`h(2/3) = 1/3 + 1 = 4/3`) and at a lower root
`alpha_0 = 0.0845` (`h` increasing on `[0,1/3]`), so `h <= 4/3` exactly outside the
open interval `(alpha_0, 2/3)`.

> **Theorem A.** For every block, `X(V) <= 2^{h(d/b)} < 3` unless `d/b = 1/3`.
> Explicitly:
> **(i)** `d >= 2b/3`: then `f <= 2^{b/3}` and `L <= 2^b`, so `fL <= 2^{4b/3}` and
> `X(V) <= 2^{4/3} = 2.5198`;
> **(ii)** `d/b <= alpha_0 = 0.0845`: then `h(d/b) <= 4/3`, so `X(V) <= 2.5198`;
> **(iii)** intermediate `b/2 <= d < 2b/3`: `X(V) <= 2^{2 - d/b}`, ranging from
> `2.8284` (at `d = b/2`) down to `2.5198` (at `d = 2b/3`).
> Hence **any block with `X(V) > 2^{4/3} = 2.5198` has `d/b in (0.0845, 2/3)`** --
> the corridor.

*Proof.* `fL <= 2^{b-d} min(2^b, SS(d)) = 2^{h(d/b) b}` is #668 rewritten (Section
0). For (i), `d >= 2b/3` gives `f <= 2^{b-d} <= 2^{b/3}` and the trivial `L <= 2^b`
(this is the Codex `X <= 2.52` regime, also `= 2^{2-d/b}` since `min(2^b,SS(d)) =
2^b` for `d >= b/2`). For (ii), `h` is increasing on `[0,1/3]` with `h(alpha_0) =
4/3`. For (iii), `min(2^b,SS(d)) = 2^b` at `d >= b/2`, so `fL <= 2^{2b-d}`,
`X <= 2^{2-d/b}`. ∎

Theorem A is the **headline regime bound**: `X <= 2.5198 = 2^{4/3}` for every block
outside the corridor. It holds for **every block we can compute** -- all sampled
blocks and all intervals through `b = 18` have `d/b >= 0.611`, and the champion
sits at `d/b = 0.667 = 2/3` exactly (the `X <= 2.52` boundary), with actual
`X = 2.3433` well inside. Verifier BLOCK 5 checks `X <= 2^{h(d/b)}` on every
witness, the `2.5198` bound for `d >= 2b/3`, and the `2.8284` bound for `d >= b/2`:

```
    block       d/b      X        2^{h(d/b)}   regime
    interval14  0.714   2.2766    2.4330       d>=2b/3 => X<=2.5198
    champ12     0.750   2.2815    2.3746       d>=2b/3 => X<=2.5198
    champ18     0.667   2.3433    2.5129       d=2b/3  => X<=2.5198  (champion)
    sidon14     1.000   2.0000    2.0000       d>=2b/3 => X<=2.5198
```

The one thing Theorem A cannot do unconditionally is close the corridor
`d/b in (0.0845, 2/3)`, where the envelope rises to `3` at `d/b = 1/3`. Inside the
corridor `fL <= 2^{4b/3}` is equivalent to `L <= 2^{d + b/3}` (since `f <= 2^{b-d}`
may be as large as `2^{m}`, `m = b - d >= b/3`), and both Sauer--Shelah and the
signed span (Lemma 2b) are weak there. That is the wall (Theorem B, Sections 6, 8).

---

## 5. THEOREM B -- corner localization (PROVED, verifier BLOCK 6)

> **Theorem B.** Fix `delta > 0`. If `X(V) >= 3 - delta` then
> **(a)** `f(V) >= ((3-delta)/2)^b` and `L(V) >= ((3-delta)/2)^b` (both large);
> **(b)** `h(d/b) >= log2(3-delta)`, so as `delta -> 0`, `d/b -> 1/3`,
> `f -> 2^{2b/3}` (the `f <= 2^{b-d}` bound asymptotically tight) and
> `L -> SS(b/3)` (Sauer--Shelah asymptotically tight, hence by Lemma 2 also
> `N_dis(b/3) -> SS(b/3)`);
> **(c)** the diameter satisfies `D >= 2^{Omega(b)}` (Lemma 3).

*Proof.* `f, L <= 2^b`, so `X^b = fL >= (3-delta)^b` forces each of `f, L >=
(3-delta)^b / 2^b = ((3-delta)/2)^b`, giving (a). From `fL <= 2^{h(d/b) b}` and
`fL >= (3-delta)^b` we get `h(d/b) >= log2(3-delta)`; since `h <= log2 3` with
equality only at `1/3`, `d/b -> 1/3` as `delta -> 0`, and then both `2^{b-d} =
2^{2b/3}` and `SS(d) = SS(b/3)` must be met to leading exponent, giving (b);
Lemma 2 upgrades the `L`-tightness to `N_dis(b/3) -> SS(b/3)`. Lemma 3 with
`d/b -> 1/3` forces `log2 D >= d/3 - O(log b) = b/9 - o(b)`, giving (c). ∎

The rate of the corner is `log2((3-delta)/2) -> log2(3/2) = 0.5850` (verifier
BLOCK 6): **any block within `delta` of `X = 3` has both a fiber and an image of
rate at least `0.585`** -- a **large** fiber (`phi_2 >= 0.585`), squarely in the
regime where #673's structural theorems apply on AP/GAP classes and where the
general case is #673's OPEN exponential-regime inverse-LO. Sample values:

```
    X >= 2.7  =>  f, L >= 2^{0.4330 b},  d/b <= 0.5670
    X >= 2.9  =>  f, L >= 2^{0.5361 b},  d/b <= 0.4639
    X  = 3    =>  f, L >= 2^{0.5850 b},  d/b <= 0.4150,  and d/b = 1/3 at the envelope.
```

---

## 6. The S2 overdetermination lemma and the tension it raised (PROVED + RESOLVED)

The lane's S2 lever asks whether the moment curve **forces `d` linearly large**,
which would bound `X`. The mechanism is real but does **not** give `d >= b - poly`.

> **Lemma 4 (S2 overdetermination).** Let `I` be a **maximal** dissociated set,
> `|I| = d`. Every `x in V \ I` makes `I cup {x}` non-dissociated, so there are
> disjoint `A', B subseteq I` with `|B| = |A'| + 1` and
> `x = sum_B v - sum_{A'} v`  **and**  `x^2 = sum_B v^2 - sum_{A'} v^2`.
> Thus each outside `x` is **overdetermined**: for a fixed pair `(A', B)` the first
> (linear) equation determines `x` uniquely, and it is admissible only if the
> second (quadratic) equation `(sum_B v - sum_{A'} v)^2 = sum_B v^2 - sum_{A'} v^2`
> also holds. Consequently `b - d <= #{ distinct forced x that lie in V \ I } <=
> Con(I)`, where `Con(I)` is the number of consistent `(A', B)` pairs.

*Proof.* Maximality gives a trade in `I cup {x}` using `x` (as `I` is
dissociated); moving `x` to one side yields the two displayed equations. The map
`(A', B) -> x = sum_B v - sum_{A'} v` is single-valued, so distinct outside
elements need distinct consistent pairs. ∎

Verifier BLOCK 6 exhibits this at `b = 12`: for both `champ12` and `interval12`,
a maximal dissociated `I` has `b - d = 3`, and exactly `3` outside elements are
forced (bound tight), out of `Con(I) = 34` consistent pairs.

**The tension, and its resolution.** If `Con(I)` were `poly(d)` one would get
`d >= b - poly(d)`, hence `f <= 2^{o(b)}` and `X -> 2` -- which **contradicts** the
proved `rho* >= 0.158` (`X* >= 2.3433`). The resolution is that `Con(I)` is
**exponential** for designed blocks: the quadratic consistency
`(sum_B v - sum_{A'} v)^2 = sum_B v^2 - sum_{A'} v^2` is one integer equation that
a block can be **built** to satisfy on exponentially many tuples (indeed a fiber
of size `f` produces `~ binom(f,2)` trades, each a bundle of consistent pairs).
So S2 does **not** force `d` large; instead it exposes the true dichotomy the data
shows (Section 7):

- **Small `d` (many consistent tuples).** Many trades = strong additive structure.
  On the curve this means `V` is close to a short AP / low-rank GAP, where #673's
  Theorems 1--3 (UNCONDITIONAL on those classes) and #655/#646's box bound force
  `L` **small** (the image collapses). Lemma 3 says small `d` needs small diameter
  only in the contrapositive; but empirically the small-`d` blocks ARE the
  interval-like ones, and there `X -> 2` (Section 6 table).
- **Large `d` (few trades).** Then `f <= 2^{b-d}` is **small**. Again `X` is
  bounded away from `3` (Sidon blocks: `f = 1`, `X = 2`).

The envelope peak `d/b = 1/3` demands **both** a large fiber and a large image, and
the two mechanisms pull apart: the structure that makes `d` small (to allow a large
fiber) is exactly the structure that collapses `L`. That is why every computed
optimizer sits at `d/b = 0.61..0.75` with `X <= 2.3433`, **never** at `1/3`.

---

## 7. MEASURED frontier (COMPUTED, verifier BLOCK 4 + BLOCK 7)

**Interval `d`-growth (exact `d`, verifier BLOCK 4).** The interval `{0,...,b-1}`
is the densest additive block and carries the smallest `d/b`; yet its `X` is flat:

```
    b        10     11     12     13     14     15     16     17     18
    d         8      9      9      9     10     10     10     11     11
    d/b    .800   .818   .750   .692   .714   .667   .625   .647   .611
    X      2.206  2.228  2.233  2.249  2.277  2.274  2.276  2.273  2.268
```

`d/b` descends slowly (consistent with Lemma 3: `phi_2 -> 1` for the interval, so
`d/b -> 0` at a `log`-rate) while `X` stays pinned near `2.27` -- the interval's
image is `poly(b)` (#646 box bound), so it never approaches `3` no matter how small
`d/b` gets. The exploratory search (reproducible, not in the fast verifier) extends
this to `b = 20` with `d/b = 0.600` and `X = 2.248`, and to `b = 19` with `d/b =
0.579`, `X = 2.254` -- still flat.

**Frontier by dissociation ratio (verifier BLOCK 7).** Over a curated sample
(intervals, both champions, Sidon, geometric, two-scale, hole, random), the maximum
`X` in each `d/b` bin is:

```
    d/b ~ 0.6 : maxX = 2.2764  (interval16)
    d/b ~ 0.7 : maxX = 2.3433  (champion, b=18)
    d/b ~ 0.8 : maxX = 2.2815  (champ12)
    d/b ~ 1.0 : maxX = 2.0000  (Sidon)
```

Every non-degenerate block has `d/b >= 0.611` (min `0.625` in the verifier
sample), the **corridor interior `d/b in [1/3, 1/2]` is empty** (no computed block
has `d/b < 0.611`, and the champion sits at the `2/3` boundary), and the sampled
maximum is exactly the `b = 18` champion `X = 2.3433`. This is the `(d/b, X)`
picture the theorems predict: a single hump near `d/b ~ 0.67`, capped well below
`2.52`, with both tails running to `X = 2`.

**Lower end (S4) + the amplification guard (COMPUTED, Codex team route cut,
verifier BLOCK 8).** Maximizing `fL` is identical to maximizing `rho = log(X/2)`
(fixed offset `log 2`), so #655's census already sweeps it; the `b = 18` champion
`V = {2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34}` (`f = 30`, `L = 151275`,
verifier BLOCK 1) gives exponent `log2(fL)/b = 1.2285391474842977`, i.e. `X = 2^{
1.228539} = 2.3432959`. The **Codex team's positional-encoding amplification**
(TEAM_BOARD 03:02Z) turns this finite-`b` record into a genuine curve `sup`: with
`S = sum(V) + 1`, `Q = b·S^2 + sum(V) + 1`, the `kb` integers `u_{j,v} = (S+v)Q^j`
(`0 <= j < k`, `v in V`) are distinct, lie on the moment curve, and their no-carry
`Q`-power spacing makes each degree-2 signature recover the `k` per-copy
`V`-signatures independently, so `f_k = f^k`, `L_k = L^k`, and the exponent is
**exactly preserved**: `log2(f_k L_k)/(kb) = log2(fL)/b`. Verifier BLOCK 8 confirms
this at `k = 2` on `V = {0,1,2,4,5,6}` (`f_2 = 4 = f^2`, `L_2 = 3969 = 63^2`,
exponent `1.162880` unchanged). Hence, allowing **unrestricted integer heights**
(the caveat: `u ~ Q^{k-1}` is exponential in `k`, so the diameter is exponential --
consistent with Lemma 3, which demands large diameter for large `d = kd_0`),

```
    X*(curve) >= 2^{1.228539} = 2.3432959.
```

The honest bracket is therefore `X* in [2.3433, 3]`; closing the corridor at
`2^{4/3}` (Section 8) would sharpen it to `X* in [2.3433, 2.5198]`. Independent
hill-climbs at `b = 12, 14, 16` land on symmetric interval-with-holes blocks with
`X <= 2.30` and `d/b in [0.75, 0.79]`; no curve-feasible construction we found
exceeds `~2.35`. Codex's counterguard numbers reproduced exactly (verifier BLOCK 8):
`interval16` exponent `1.1867543039302069`, champion exponent `1.2285391474842977`
(so any `2^{3/2 - delta}` claim needs `delta <= 0.2714608525157023`, and the
`2^{4/3}` corridor target `delta = 1/6` is safely above the champion).

---

## 8. The wall, restated combinatorially (OPEN)

By Theorem A, the only route to `X > 2^{4/3} = 2.5198` is the corridor
`d/b in (0.0845, 2/3)`, and there `fL <= 2^{4b/3}` is **equivalent to the corridor
bound**

```
    L <= 2^{d + b/3}                              (corridor target, Codex framing)
```

(since `f <= 2^{b-d} = 2^{m}` may be as large as `2^m`; `L <= 2^{d+b/3}` gives
`fL <= 2^{m} 2^{d + b/3} = 2^{b + b/3} = 2^{4b/3}`). Proving it would give
unconditional `X* <= 2^{4/3} = 2.5198`, hence the bracket `X* in [2.3433, 2.5198]`.
Theorems A--B and Lemma 2 restate this corridor bound as one self-contained finite
statement about counting dissociated sets, free of any inverse-LO black box. Because
the envelope only touches `3` at `d/b = 1/3`, it suffices to break the peak on a
fixed neighborhood of `1/3`:

> **(Curve-N_dis collapse) -- OPEN.** There exist `c > 0`, `eps > 0`, `b_0` such
> that for all `b >= b_0`, every block `V` with `d(V)/b in [1/3 - eps, 1/3 + eps]`
> has `N_dis(d) <= 2^{-c b} SS(d)` -- i.e. a **constant-exponent** fraction of the
> size-`<= d` subsets is non-dissociated.

*Reduction (PROVED that this hypothesis gives `X < 3`).* Take any block.
- If `d/b not in [1/3 - eps, 1/3 + eps]`: by Theorem A, `fL <= 2^{h(d/b) b} <=
  2^{H b}` with `H := max( h(1/3 - eps), h(1/3 + eps) ) < log2 3`, so `X <= 2^H < 3`.
- If `d/b in [1/3 - eps, 1/3 + eps]`: by Lemma 2 and the hypothesis
  `L <= N_dis(d) <= 2^{-cb} SS(d)`, so `fL <= 2^{b-d} · 2^{-cb} SS(d) = 2^{-cb}
  · 2^{(b-d) + log2 SS(d)} <= 2^{-cb} · 2^{h(d/b) b} <= 2^{-cb} 3^b`, giving
  `X <= 3 · 2^{-c} < 3`.
Both branches give `X <= max(2^H, 3·2^{-c}) < 3`, uniformly in `b >= b_0`. ∎

The hypothesis is a **large-fiber phenomenon**: `d/b <= 1/3 + eps` allows (and, near
`X = 3`, forces via Theorem B) a fiber of rate `>= 2/3 - eps > log2(3/2)`, so
`(Curve-N_dis collapse)` is exactly the "many trades assemble into a near-perfect
matching" statement (#655 R4 / #673 Step B) counted as dissociated-set collapse.
The literature supplies it **polynomially** (Nguyen--Vu inverse-LO, in scope for
`f >= 2^b b^{-C}`) and **countingly** (Ferber--Jain--Luh--Samotij) but not
per-instance in the exponential regime. On the structured classes the extremal
blocks actually inhabit (subsets of a length-`O(b)` AP, unions of `c` APs,
bounded-rank subexponential GAPs) it is a **theorem** -- #673's Theorems 1--3 give
`L <= 2^{o(b)}`, hence `X -> 2 < 3` unconditionally there. What remains open is
only the structurally-wild case, and the frontier (Section 7) shows no wild block
climbing.

---

## 9. Honest residuals (OPEN)

1. **The corridor `d/b in (0.0845, 2/3)`** is the whole open problem. Outside it
   `X <= 2^{4/3} = 2.5198` (Theorem A, PROVED). Closing it -- proving the corridor
   bound `L <= 2^{d + b/3}`, equivalently `(Curve-N_dis collapse)` (Section 8) --
   would give the unconditional `X* <= 2.5198`, hence `X* in [2.3433, 2.5198]`. It
   is #673's OPEN exponential-regime inverse-LO; not closed here.
2. **`d >= 2b/3` is not universal.** Lemma 3 forces `d/b -> 0` for poly-diameter
   families (e.g. the interval, `d/b` measured descending to `0.579` at `b = 19`),
   so the large-`d` regime of Theorem A eventually fails on the interval -- but
   there `X -> 2` (poly image), so the block is safe by a *different* bound (the
   AP/GAP box bound, #646/#673). A single unconditional `X < 3` must glue the
   large-`d` regime to the small-image structure inside the corridor; the glue is
   the open wall.
3. **Explicit constant.** Even granting the wall, `c` is non-explicit. The frontier
   suggests the truth is `X* ~ 2.34` (`rho* ~ 0.16`), but that is MEASURED; the
   champions still edge up (`X = 2.2815 -> 2.3433` from `b=12` to `b=18`).
4. **`N_dis(d)` asymptotics.** Lemma 2 is exact and strict but only a
   constant-factor gain per trade (Section 2); a self-contained proof of
   `(Curve-N_dis collapse)` would need the disjoint-trade packing that #655 R7
   flags as the point where such arguments silently break. We do not claim it.

---

## Summary

```
    QUESTION:  distinct-integer moment curve -- is fL <= X^b with explicit X < 3?
    BASE:      #668  fL <= 3^b  (X <= 3).  HONEST BRACKET:  X* in [2.3433, 3],
               and X* in [2.3433, 2.5198] IF the corridor closes.

    envelope:  fL <= 2^{h(d/b) b}, h(alpha)=(1-alpha)+H2(min(alpha,1/2)),
               h < log2 3 EXCEPT at alpha=1/3 (the sole route to X=3).
    Lemma 1:   d >= 5 (every 5-subset dissociated; min trade support 6).
    Lemma 2:   L <= N_dis(d) = #{dissociated sets size<=d} <= SS(d) (Pajor); strict.
    Lemma 2b:  outside cols = signed {-1,0,1}-combos of max dissoc set => L <=
               (2m+2)^d (Codex route cut; dominated by SS, structural).
    Lemma 3:   2^d <= (d+1)(dD+1)(dD^2+1) => d=O(log bD); poly-diam => X->2.
    Thm A:     X <= 2^{h(d/b)}; d>=2b/3 => X<=2^{4/3}=2.5198 and d/b<=0.0845 =>
               X<=2.5198, so X>2.5198 forces the CORRIDOR d/b in (0.0845, 2/3)
               (Codex framing); d>=b/2 => X <= 2^{2-d/b} <= 2.8284.
    Thm B:     X>=3-delta => f,L >= ((3-delta)/2)^b, d/b->1/3, both #668 bounds
               tight, diameter >= 2^{Omega(b)}.
    S2:        b-d <= #{forced outside x}, each overdetermined (x AND x^2 fixed);
               NOT d>=b-poly (consistent-tuple count is exponential) -- tension
               RESOLVED: small d <=> structure <=> small L; large d <=> small f.
    amplify:   positional Q-power tensor (f_k=f^k, L_k=L^k, exp preserved, exp
               heights) => X* >= 2^{1.228539} = 2.3433 on the curve (Codex cut).
    frontier:  every block b<=18 has d/b>=0.611, X<=2.3433; corridor interior
               (near d/b=1/3) EMPTY of computed blocks; champion X=2.3433.
    WALL:      close corridor  <=  corridor bound L <= 2^{d+b/3} (equiv.
               (Curve-N_dis collapse) N_dis(d) <= 2^{-cb}SS(d) near d/b=1/3;
               reduction PROVED) = #673's OPEN exponential-regime inverse-LO;
               a THEOREM on AP/GAP classes (#673) => corridor empty of wild climbs.
```

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/curve_restricted_product.md` (this).
- Verifier: `experimental/scripts/verify_curve_restricted_product.py`
  (`RESULT: PASS (176/176)`, ~22 s; recomputes every witness `f, L, d`, the
  envelope + its peak + corridor endpoints (`alpha_0`), Lemmas 1--3, the Pajor
  chain `L <= #shattered <= N_dis <= SS`, the signed-span bound `L <= (2m+2)^d`
  (Lemma 2b), Theorems A--B (incl. `d>=2b/3 => X<=2.5198`), the S2 count, the
  frontier bins, and the amplification `f_k=f^k, L_k=L^k` with the exact champion /
  interval16 counterguard exponents).
- Read-only inputs: DannyExperiments #668 `canonical_transversal_vc_compression.md`
  (fetched via `refs/pull/668/head`); our #673 `ilo_moment_structured.md`, #655
  `fiber_image_tradeoff.md`, #643 `pte_cluster_packing_frontier.md`, #623
  `pte_extremality_image_face.md`; hughes #564 `w_a_star_pte_lemma.md`.

**Per-claim status.** Envelope + peak + corridor endpoints, Lemma 1, Lemma 2
(Pajor refinement), Lemma 2b (signed-span, Codex route cut), Lemma 3 (box bound +
poly-diameter corollary), Theorem A (corridor localization, `d>=2b/3 => X<=2.5198`,
`d>=b/2 => X<=2.8284`), Theorem B (corner localization), Lemma 4 (S2
overdetermination), and the Section 8 reduction = **PROVED**. Interval `d`-growth,
the frontier bins, the Pajor chain counts, the amplification tensor, and the
champion = **COMPUTED**. "Corridor interior empty", "`X* ~ 2.34`" = **MEASURED**.
The amplified `X* >= 2.3433` lower guard = **PROVED** (exact finite-`k` tensor,
exponential-height caveat stated). Closing the corridor (`L <= 2^{d+b/3}`) /
unconditional `X < 3` = **OPEN** (= #673's wall).

**Flagged for PI (least-certain, 3 steps).**
(a) **Lemma 2's Pajor step** uses #668's own two facts (shattered => dissociated;
`VCdim(R) <= d`) unchanged; the only new ingredient is Pajor `|R| <= #shattered`.
The chain is verified by direct enumeration for `b <= 11`, so the risk is only in
reading #668 correctly, not in the combinatorics.
(b) **Theorem B(b)'s "both bounds tight"** is an asymptotic (leading-exponent)
statement: `fL -> 3^b` forces `2^{b-d} -> 2^{2b/3}` and `SS(d) -> SS(b/3)`
simultaneously; the finite-`b` corner is not claimed exactly.
(c) **The S2 exponential-`Con` claim** (Section 6) is argued structurally (a fiber
of size `f` yields `~binom(f,2)` trades) and checked at `b=12` (`Con=34`), but the
exact growth of `Con(I)` on adversarial blocks is not computed at scale -- it is
the same object as the wall's trade count.

**Exact vs heuristic.** All `f, L, d`, `N_dis`, `#shattered`, box counts, and
frontier optima are exact integer enumeration. The envelope, Theorems A--B, and the
Section 8 reduction are elementary closed-form proofs. No external theorem is
re-derived; #673's inverse-LO inputs are cited within their printed hypotheses. No
`.tex`/`.pdf` touched.
