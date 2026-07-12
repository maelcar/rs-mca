# The diameter geography of the corridor wall: a 2D (d/b, log2 D / b) map

## Status

`SETUP: #678 localized the curve product wall to L <= 2^{d+b/3} in the corridor
d/b in (alpha_0, 2/3), alpha_0 = 0.084497; equivalently X = (fL)^{1/b} <= 2^{4/3}
= 2.5198 there. This packet adds the DIAMETER coordinate delta = log2 D / b and
maps exactly where in the (alpha, delta) plane the wall can live / MAIN RESULT
(PROVED, synthesis): composing #668's fiber bound f <= 2^{b-d} with the
#655/#663 image box bound L <= (b+1)(bD+1)(bD^2+1) (= #663 R2 V1 Horn A rank 1;
= #673 Thm 3 rank 1) gives X <= 2^{(1-alpha)+3delta+o(1)}, so a block is
CERTIFIED X <= 2^{4/3} whenever delta <= (alpha + 1/3)/3. Intersecting with #678's
envelope corridor, the RESIDUAL (uncertified) region is exactly R = { alpha_0 <
alpha < 2/3, delta > (alpha+1/3)/3 } / COROLLARY 1 (diameter shrink, PROVED):
for a block of diameter exponent delta the corridor shrinks to (alpha_0,
min(2/3, 3delta - 1/3)); it is EMPTY for delta <= 0.13928, and the full corridor
(up to 2/3) is only reached at delta >= 1/3 / COROLLARY 2 (diameter inflation,
PROVED): every corridor-wall block has D >= 2^{d/3 + b/9} -- a factor 2^{b/9}
above the Lemma-3 dissociation floor 2^{d/3}; so the wall lives entirely among
super-exponential-diameter, spread blocks (matching #663's "large-detG"
residual) / TRANSFER (AUDIT): rank-r GAP host gives lambda <= (r+2) delta
(#673 Thm 3), residual line (alpha+1/3)/(r+2); in the Fourier guise this is
#663's detG horn, in the Bohr->GAP guise it says the trapping host must have
size >= 2^{b/3} / ROUTE-IMPOSSIBILITY (PROVED): the corridor endpoints are
intrinsic to the {#668 fiber, Pajor/SS, signed-span} toolkit -- the only
elementary leverage is diametric (this note), not ratiometric; closing the
delta >= 1/3 core IS #678's / #673's open exponential-regime inverse-LO / FRONTIER
(COMPUTED): every sampled block satisfies L <= 2^{d+b/3} with slack ratio <= 0.577;
no counterexample; min non-degenerate d/b reached = 0.625 (corridor interior
still empty of computed blocks, as #678 measured)`.

This packet is a **diameter refinement + cross-guise reconciliation** of
**#678** (`curve_restricted_product.md`). #678 proved `X <= 2^{4/3} = 2.5198`
outside the corridor `d/b in (0.084497, 2/3)` and restated the wall as the single
corridor bound `L <= 2^{d + b/3}`. That statement is one-dimensional in `alpha =
d/b`. Here we make it **two-dimensional** by carrying the block's diameter
exponent `delta = log2 D / b` (`D` = diameter): the same image box bound #678 cites
only for *poly*-diameter (`X -> 2` corollary) is a **quantitative** `lambda <=
3delta` ceiling that certifies the corridor bound up to an *exponential*
diameter, and the residual region is a thin wedge that only fattens to the full
corridor once `delta >= 1/3`. We do **not** close the wall (its core is #673's
OPEN exponential-regime inverse-Littlewood-Offord); we localize it to a sharp
`(alpha, delta)` region and record what transfers to the Fourier (#661) and
Bohr->GAP (#663) guises.

Every number below is recomputed by
`experimental/scripts/verify_corridor_diameter_map.py` (stdlib-only,
zero-arg, `RESULT: PASS (58/58)`, ~10 s; every witness `f, L, d`, the root
`alpha_0`, the box bound, the residual-map grid, the diameter-inflation floor,
the rank-`r` transfer lines, the amplification base, and the `F_13` calibration
re-derived exactly).

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exact
enumeration), **MEASURED** (exact objects, trend read off), **AUDIT**
(cross-reference), **OPEN**.

**Credit.** The three composed inputs are **not ours** and are the substance:
(i) the fiber bound `f <= 2^{b-d}` and the Sauer--Shelah/Pajor image bound are
**DannyExperiments #668** (`canonical_transversal_vc_compression.md`); (ii) the
image box bound `L1 <= (b+1)(bD+1)(bD^2+1)` is **our #655**
(`fiber_image_tradeoff.md`, the polynomial box bound), and its rank-`r` GAP
generalization `L1 <= (b+1) b^{r(r+3)/2} |P|^{r+2}` with `lambda <= (r+2)delta` is
**our #673** (`ilo_moment_structured.md`, Theorem 3); (iii) the corridor `L <=
2^{d+b/3} <=> X <= 2^{4/3}` and the endpoint `alpha_0`, the champion, the
amplification, and the dissociation-dimension frame are **#678**
(`curve_restricted_product.md`), built on **DannyExperiments #668**. The
**rank-1 diameter horn** `diam <= 2^{eta b} => lam_2 <= 3 eta` is already proved
as **our #663** (`bohr_gap_volume.md`, R2 V1 Horn A); this note's new content is
only the **composition into the `(alpha, delta)` map**, the explicit constants
(`0.13928`, the residual line `alpha/3 + 1/9`, the `2^{b/9}` inflation), and the
cross-guise reconciliation. The `F_13` modular calibration is **Codex team
calibration, team board 2026-07-12** (a modular-signature datapoint, flagged
below as a *different object* from the distinct-integer class). The minimal
degree-2 PTE trade support `6` is **scottdhughes #564**. Pajor's lemma is
classical.

---

## 0. Setup: the corridor, and the two rate coordinates it hides (AUDIT)

A **block** `V` is `b` distinct integers; `Phi(S) = (|S|, sum_S x, sum_S x^2)`;
`f = max_y #Phi^{-1}(y)`, `L = #{Phi(S)}`, `X = (fL)^{1/b}`. Write the two rate
coordinates (base-2 logs)

```
    phi = (log2 f)/b,   lambda = (log2 L)/b,   so  X = 2^{phi + lambda}
```

(verifier BLOCK 0). #678's dissociation dimension `d` (max subset-dissociated
set) gives, via **#668**, `phi <= 1 - alpha` (`alpha := d/b`) and `lambda <=
H_2(min(alpha,1/2))`, hence the **envelope** `X <= 2^{h(alpha)}`,
`h(alpha) = (1-alpha) + H_2(min(alpha,1/2))`, `h < log2 3` off `alpha = 1/3`.
#678's **corridor** is `{alpha : h(alpha) > 4/3}`:

```
    corridor  =  ( alpha_0, 2/3 ),   alpha_0 = 0.084497   (root of h = 4/3),
```

and inside it `X <= 2^{4/3}` is equivalent to the OPEN corridor bound
`L <= 2^{d + b/3}` (i.e. `lambda <= alpha + 1/3`). Outside, #678 proves
`X <= 2^{4/3}` unconditionally. **The corridor is one-dimensional in `alpha`.
This note adds the second coordinate the envelope discards: the diameter.**

Normalize `min V = 0`, so `V subseteq [0, D]`, `D` = diameter, and put

```
    delta := (log2 D) / b     (the diameter exponent).
```

---

## 1. The diameter box ceiling and the composed X-bound (PROVED, verifier BLOCKS 1,2)

The image lives in the integer box `[0,b] x [0,bD] x [0,bD^2]`, so

```
    L <= (b+1)(bD+1)(bD^2+1)           (image box bound, #655 / #663 R2V1 / #673 Thm3 rank 1)
```

(verifier BLOCK 2 confirms it exactly on `interval12..16`, `champ12`, `hole14`,
`twoscale12`). Taking `log2`, dividing by `b`:

```
    lambda <= 3 delta + 3(log2 b)/b + O(1/b) = 3 delta + o(1).            (box-lambda)
```

Compose with `phi <= 1 - alpha` (#668):

> **Proposition 1 (composed X-bound, PROVED).** For every block,
> `X = 2^{phi+lambda} <= 2^{(1-alpha) + 3 delta + o(1)}`. In particular
> `X <= 2^{4/3}` (the corridor bound `L <= 2^{d+b/3}` holds) whenever
> `delta <= (alpha + 1/3)/3`.

*Proof.* `phi <= 1-alpha` is #668's fiber bound. `lambda <= 3delta+o(1)` is
(box-lambda). Sum the exponents: `phi+lambda <= (1-alpha)+3delta+o(1)`. This is
`<= 4/3` iff `3delta <= alpha + 1/3`, i.e. `delta <= (alpha+1/3)/3`. Since
`X = 2^{phi+lambda}` and `lambda <= alpha + 1/3` is `L <= 2^{d+b/3}`, both forms
follow. ∎

This is the rank-1 case of **#673 Theorem 3** (`lambda <= (r+2)delta`, `r=1`) fed
into **#668**'s fiber bound; equivalently it is **#663 R2 V1 Horn A**
(`diam <= 2^{eta b} => lam_2 <= 3 eta`) restated with `eta = delta`. The **new**
content is the composition with `phi` and the corridor comparison. It **sharpens
#678's poly-diameter corollary** (`D = poly(b) => X -> 2`) to a certificate that
holds up to an *exponential* diameter `D = 2^{delta b}` with `delta` as large as
`(alpha+1/3)/3`.

**Finite-`b` caveat (verifier BLOCK 1).** The `3(log2 b)/b` overhead is real at
small `b`: for the `b=18` champion (`alpha = 2/3`, `delta = 5/18`) the asymptotic
form certifies (`delta = 0.278 < (2/3+1/3)/3 = 1/3`), but the exact inequality
`(b-d) + log2[(b+1)(bD+1)(bD^2+1)] = 33.59` exceeds `4b/3 = 24.00` by `9.59` --
the poly overhead dominates until `b` is large (`3 log2 b < (alpha+1/3 - 3delta)b`
needs `b` in the hundreds mid-corridor). Proposition 1 is therefore an
**asymptotic** statement -- which is exactly the regime of the wall (a `b -> inf`
question); we do not claim finite-`b` certification of specific blocks.

---

## 2. The 2D residual map (PROVED, verifier BLOCK 3)

Envelope certifies `alpha <= alpha_0` or `alpha >= 2/3`; box (Proposition 1)
certifies `delta <= (alpha+1/3)/3`. A block is uncertified iff neither fires:

> **Theorem 2 (residual region, PROVED asymptotically).** The set of
> `(alpha, delta)` NOT certified `X <= 2^{4/3}` by {envelope, box} is exactly
> ```
>     R = { (alpha, delta) : alpha_0 < alpha < 2/3,  delta > (alpha + 1/3)/3 }.
> ```
> The lower boundary is the line `delta_res(alpha) = (alpha+1/3)/3 = alpha/3 + 1/9`,
> rising from `delta_res(alpha_0) = 0.13928` to `delta_res(2/3) = 1/3`.

*Proof.* `R` is `{h(alpha) > 4/3}` (uncertified by envelope) intersected with
`{(1-alpha)+3delta > 4/3}` (uncertified by box). The first is `(alpha_0, 2/3)`;
the second is `delta > (alpha+1/3)/3`. The verifier checks on a `101 x 61` grid
that `residual == not certified` everywhere. ∎

Two corollaries read the map along its two axes:

> **Corollary 1 (diameter shrink).** For blocks of diameter exponent `delta`, the
> corridor shrinks to `(alpha_0, min(2/3, 3delta - 1/3))`. It is **empty** for
> `delta <= 0.13928` (`X <= 2^{4/3}` unconditionally), and reaches the full
> `(alpha_0, 2/3)` only at `delta >= 1/3`.

```
    delta        residual corridor          width       (verifier BLOCK 3)
    <= 0.13928   empty                       0
    0.16         (0.0845, 0.1467)            0.0622
    0.20         (0.0845, 0.2667)            0.1822
    0.25         (0.0845, 0.4167)            0.3322
    0.30         (0.0845, 0.5667)            0.4822
    >= 1/3       (0.0845, 0.6667)            0.5822   (full corridor)
```

So a corridor-bound counterexample cannot merely sit in `(alpha_0, 2/3)`: it must
*also* be diameter-inflated to `delta > 3^{-1}(alpha+1/3)`, and to threaten the
whole corridor it needs `delta >= 1/3`, i.e. `D >= 2^{b/3}`.

---

## 3. Diameter inflation: the wall needs D >= 2^{d/3 + b/9} (PROVED, verifier BLOCK 4)

The residual line `delta_res(alpha) = alpha/3 + 1/9` says exactly:

> **Corollary 2 (diameter inflation).** Every block in `R` (in particular any
> corridor-bound counterexample) has `delta > alpha/3 + 1/9`, i.e.
> ```
>     D  >  2^{d/3 + b/9}.
> ```

Compare **#678's Lemma 3** (dissociation box) `2^d <= (d+1)(dD+1)(dD^2+1)`, i.e.
`alpha <= 3delta + o(1)`, equivalently `D >= 2^{d/3 - o(b)}`: this is the **floor**
every block obeys (verifier BLOCK 4 checks `2^d <= box` on `interval12`,
`champ18`, `twoscale12`). Corollary 2 says a wall block sits a **factor
`2^{b/9}`** above that floor -- its diameter exceeds the minimum forced by its
own dissociation dimension by a full exponential margin. This is the precise,
quantitative form of #678's remark that "the danger blocks are exactly the
exponential-diameter / tensor-limit blocks," and it matches **#663's** independent
verdict that the residual is confined to **"large-detG (spread) blocks."** The
`b=18` champion has `delta = 0.278` versus floor `alpha/3 = 0.222` -- a margin of
only `0.056 < 1/9`, so it sits **below** the inflation line and is (asymptotically)
safe, consistent with its `X = 2.343 < 2.520`.

---

## 4. What transfers to the Fourier and Bohr->GAP guises (AUDIT, verifier BLOCK 5)

The image box bound has a rank-`r` GAP generalization, **#673 Theorem 3**: if `V`
sits in a rank-`r` GAP host `P` of size `|P| = 2^{delta b}` then
`lambda <= (r+2) delta + o(1)`. Feeding this into Proposition 1's `phi <= 1-alpha`:

> **Transfer (rank-`r` residual line).** For blocks hosted in a rank-`r`
> subexponential GAP of log-size `delta`, `X <= 2^{4/3}` whenever
> `delta <= (alpha + 1/3)/(r+2)`; the residual line is `delta = (alpha+1/3)/(r+2)`.

```
    rank r   empty-threshold delta<=      full-corridor delta>=   (verifier BLOCK 5)
    1        0.1393                        0.3333   (= the diameter map, host [0,D])
    2        0.1045                        0.2500
    3        0.0836                        0.2000
```

The three guises of the wall now read off one line:

- **Consumer / this note (#678):** `delta` = diameter exponent. Wall needs
  `delta >= 1/3` (`D >= 2^{b/3}`).
- **Fourier (#661/#663):** `delta` is `#663 R2 V1`'s normalized `log2(diam)`; the
  bound `lambda <= 3delta` **is** #663's rank-1 detG **Horn A**
  (`diam <= 2^{eta b} => lam_2 <= 3 eta`). The `(alpha, delta)` map is the
  consumer image of that horn; **the step transfers verbatim** (`eta = delta`).
- **Bohr->GAP (#663 R3):** `delta` is the log-size of the trapping GAP host `P`.
  The statement "`X <= 2^{4/3}` unless `delta >= 1/3`" says the wall requires a
  **host of size `>= 2^{b/3}`**; #663's rational-resonance horn (R3, bounded
  denominator `q` => rank-1 host) already closes the small-host case, exactly the
  `delta` small end. What remains open in all three is the **large-host /
  large-diameter / large-detG** core -- the single object.

**Transfer summary (one line).** Progress on *any* guise's control of the host
size / diameter / denominator directly moves the same residual line
`delta = (alpha+1/3)/(r+2)` in the others; the diameter coordinate `delta` is the
shared handle.

---

## 5. The endpoints are intrinsic; the only elementary shrink is diametric (PROVED)

Could the *envelope* corridor `(alpha_0, 2/3)` be narrowed in `alpha` alone,
without the diameter? Within the elementary toolkit
`T = { #668 f <= 2^{b-d};  Pajor L <= N_dis(d) <= SS(d);  signed-span L <=
(2m+2)^d }` (all of #678's `alpha`-only bounds), **no**:

- **Upper endpoint `2/3`.** For `alpha in [1/2, 2/3]` the only `T`-bound on `L`
  is the trivial `L <= 2^b` (`SS(d) = 2^b(1-o(1))`, and `(2m+2)^d > SS(d)`).
  There `X <= 2^{4/3}` is *equivalent* to `L <= 2^{d+b/3}` -- the corridor bound
  itself. Pushing `2/3` down = proving the corridor bound = the wall.
- **Lower endpoint `alpha_0`.** The signed-span `L <= (2m+2)^d` gives the corridor
  bound only for `d log2(2m+2) <= d + b/3`, i.e. `alpha = O(1/log b) -> 0`, strictly
  **below** `alpha_0`. So `T` never lifts `alpha_0`.

Hence **the corridor is intrinsic in the `alpha` coordinate**: every elementary
`alpha`-only route reduces to the wall. The diameter coordinate is the one place
the toolkit has slack -- and Proposition 1 spends exactly that slack. This is the
sense in which the diameter map is the *only* elementary shrink, and it is a
conditional (per-diameter-class) one. Closing `R`'s `delta >= 1/3` core is
`(Curve-N_dis collapse)` (#678 Section 8) = #673's OPEN exponential-regime
inverse-LO.

---

## 6. Frontier, amplification, calibration (COMPUTED / MEASURED, verifier BLOCKS 2,6,7)

**Corridor-bound slack (BLOCK 2).** Every sampled block satisfies
`L <= 2^{d+b/3}` with room; the largest slack ratio `L / 2^{d+b/3}` over the
family is `0.572` (`interval16`). The champion `f=30, L=151275, d=12` gives
`L/2^{d+b/3} = 151275/262144 = 0.577` -- the corridor bound holds with a `1.73x`
margin even at the record block.

**Amplification base sits in the wall-diameter regime (BLOCK 6).** #678's
positional `Q`-power tensor on `V = {0,1,2,4,5,6}` (`f_0=2, L_0=63, d_0=5,
X_0=2.239`) uses `Q = b_0 S^2 + ... = 2185`, giving `delta_inf = log2 Q / b_0 =
1.849 >> 1/3`. So the amplified curve `sup` lives at **large `delta`** (as it
must, by Corollary 1, to be a candidate near the corridor) -- yet `X_0 = 2.239 <
2.520`: **large `delta` is necessary, not sufficient, for the wall.** The map
constrains the geography; it does not manufacture a violator.

**`F_13` modular calibration (Codex team, team board 2026-07-12).**
`U = {0,1,2,3,4,5,6,7,10,12}`, full modular quadratic signature over `F_13`, gives
`(b,f,L,d) = (10,3,737,7)`, `X = (fL)^{1/b} = 2.1600`, `d/b = 0.7`. Reproduced
exactly (BLOCK 6). **Caveat carried from the seed:** these are signatures **mod
13** (wrap-around), *not* the distinct-integer / no-wrap class of #678's Lemma 1
and this note. It is a calibration datapoint (the modular class behaves
comparably, `X = 2.16 < 2.34 < 2.52`), **not a bound** on the integer class.

**Counterexample probe (BLOCK 7).** Over `54` blocks -- the box family, both
champions, six interval-with-holes families, and a deterministic 40-block random
sample (`b in {12,13,14}`, moderate diameter) -- **no block** has `L > 2^{d+b/3}`;
`max L/2^{d+b/3} = 0.577`. The minimum non-degenerate `d/b` reached is `0.625`
(`interval16`). Reaching `d/b < ~0.6` needs `b` beyond the exact-`d` range
(`max_dissoc` is exponential in `b-d`), so the corridor interior `d/b -> 1/3`
remains **empty of computed blocks**, exactly as #678 MEASURED. The probe is
evidence *for* the corridor bound, not a proof.

---

## 7. Honest residuals (OPEN)

1. **The `delta >= 1/3` core of `R` is the wall.** Everything with `delta` below
   the line `alpha/3 + 1/9` is certified (Proposition 1); the residual is a
   super-exponential-diameter wedge, unchanged in substance from #678's
   `L <= 2^{d+b/3}` / #673's exponential inverse-LO. We close **no** part of it.
2. **Asymptotic only.** Proposition 1 carries a `+3(log2 b)/b` overhead
   (`+0.70` at `b=18`); it certifies specific finite blocks only for `b` in the
   hundreds mid-corridor. The map is the `b -> inf` limit shape.
3. **The box exponent `3` is a ceiling.** The `(k,s,q)` image is intrinsically
   3-coordinate; the Newton/power-mean constraint `q >= s^2/k` improves only the
   constant, not the `3delta` slope (the `D`-exponent stays `3`). So the residual
   line `alpha/3 + 1/9` is the best this method gives; moving it down needs a
   genuinely sub-box `L`-bound = the wall.
4. **`R` is not proven inhabited.** No computed or constructed block lies inside
   `R` with `X > 2^{4/3}`; whether `R` contains *any* block at all (equivalently,
   whether the corridor bound is tight or merely provable) is the open question,
   and the frontier (Section 6) shows no climb toward it.

---

## Summary

```
    QUESTION (from #678): where in (alpha=d/b, delta=log2 D/b) can the corridor
             wall  L <= 2^{d+b/3}  (X <= 2^{4/3})  possibly fail?

    inputs:  phi <= 1 - alpha                      (#668 fiber bound)
             lambda <= 3 delta + o(1)              (#655/#663/#673 image box, rank 1)
             corridor = (alpha_0, 2/3), alpha_0=0.084497   (#678 envelope)
    Prop 1:  X <= 2^{(1-alpha)+3delta+o(1)};  certified iff delta <= (alpha+1/3)/3.
    Thm 2:   RESIDUAL  R = { alpha_0 < alpha < 2/3,  delta > (alpha+1/3)/3 }.
    Cor 1:   per-diameter corridor (alpha_0, min(2/3, 3delta-1/3));
             EMPTY for delta <= 0.13928;  full corridor iff delta >= 1/3.
    Cor 2:   wall block => D > 2^{d/3 + b/9}  (factor 2^{b/9} above Lemma-3 floor).
    transfer:rank-r host: residual line (alpha+1/3)/(r+2)  (#673 Thm3);
             = #663 Horn A (Fourier),  = host-size >= 2^{b/3} (Bohr->GAP).
    intrinsic:alpha-only toolkit {#668,Pajor/SS,signed-span} cannot shrink the
             corridor in alpha (upper end = corridor bound; lower end reaches only
             alpha=O(1/log b)); the shrink is purely diametric.
    computed:every sampled block obeys L<=2^{d+b/3}, slack <= 0.577; no violator;
             min d/b = 0.625; corridor interior empty (as #678 measured).
    OPEN:    the delta>=1/3 core of R = #678/#673's exponential-regime inverse-LO.
```

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/corridor_diameter_map.md` (this).
- Verifier: `experimental/scripts/verify_corridor_diameter_map.py`
  (`RESULT: PASS (58/58)`, ~10 s; recomputes `alpha_0`, the champion
  `f,L,d,X,D,delta`, the box bound on the family, the `101x61` residual-map grid,
  the residual widths, the diameter-inflation floor, the rank-`r` transfer lines,
  the amplification base `delta_inf`, and the `F_13` calibration).
- Read-only inputs: **#678** `curve_restricted_product.md`; **DannyExperiments
  #668** `canonical_transversal_vc_compression.md`; **#655**
  `fiber_image_tradeoff.md` (image box bound); **#673** `ilo_moment_structured.md`
  (Theorem 3, rank-`r`); **#663** `bohr_gap_volume.md` (R2 V1 Horn A, R3); **#661**
  `exp_ilo_fourier.md`; hughes **#564** `w_a_star_pte_lemma.md`.

**Per-claim status.** Proposition 1 (composed X-bound), Theorem 2 (residual
region), Corollary 1 (diameter shrink), Corollary 2 (diameter inflation), and the
Section 5 route-impossibility = **PROVED** (asymptotic; the finite-`b` overhead
is stated). The rank-`r` transfer line and the identification with #663's Horn A /
Bohr->GAP host = **AUDIT** (= #673 Thm 3 / #663 R2V1, quoted). The box-bound
checks, the champion, the residual-map grid, the amplification base, the probe
(no violator), and the slack ratios = **COMPUTED**. "Corridor interior empty of
computed blocks", "min d/b = 0.625" = **MEASURED**. The `F_13` datapoint =
**COMPUTED** but **modular** (flagged not-a-bound). Closing `R`'s `delta >= 1/3`
core = **OPEN** (= #678 Section 8 = #673's wall).

**Exact vs heuristic.** All `f, L, d`, the box counts, the grid classification,
and the probe are exact integer enumeration. Proposition 1, Theorems, and
Corollaries are elementary closed-form (the `o(1)` is the explicit `3(log2 b)/b`).
No external theorem is re-derived; #655/#663/#668/#673's inputs are cited within
their printed hypotheses. No `.tex`/`.pdf` touched.
