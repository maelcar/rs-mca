# The resonance-denominator window on the fenced Bohr->GAP class: empty, and pinned to the residual line

## Status

`TARGET: re-run the image-face Bohr->GAP denominator question (#661 exp_ilo_fourier,
#663 bohr_gap_volume) ON the newly fenced wall class -- every wall-carrying block
(X=(fL)^{1/b} > 2^{4/3}) now provably has diameter exponent delta=log2(D)/b >
alpha/3+1/9 (=> delta>=1/3 near the fence, #682 Cor 2), large detG (#663), and is
NOT a dilation (#685). Can the dominant resonance denominator q be controlled there?
/ T1 RESOLUTION CEILING (PROVED): a width-w quadratic Bohr trap resolves a
denominator q only if q <= Q_res=1/(2w); for a #661-Thm-B trap of a phi>=1-eta
block, w=sqrt((ln2/2)(eta+1/b)/eps) >= sqrt(ln2/(2b)), so Q_res <= sqrt(b/(2 ln2))
= 0.84932 sqrt(b) -- POLYNOMIAL in b, uniformly over eta,eps / T2 HOST-SMALLNESS
THRESHOLD (PROVED): a rational resonance a/q traps V in q^{o(1)} residue classes
whose host stays diameter-scaled (log-size/b = delta - log2(q)/b + o(1)); the
corridor bound needs log2(q)/b >= beta := delta - alpha/3 - 1/9 > 0 (fenced, #682
Cor 2), i.e. q >= q_cross=2^{beta b} EXPONENTIAL; and 3delta>alpha+1/3 so the
trivial box bound is already useless / T3 MAIN RESULT -- WINDOW EMPTY (PROVED): the
bounded-denominator horn (#663 R3) is VACUOUS on the fenced class, needing q in the
empty interval [2^{beta b}, 0.849 sqrt(b)] (q_cross > Q_res for all b>b_0(beta):
b_0=411 at beta=.01, 19 at beta=.10, 2 at beta>=.193); the delta-crossover (beta=0)
is EXACTLY #682's residual line (alpha+1/3)/3 -- Bohr face = box face / P4 DECOUPLING
(COMPUTED): Bohr trapping is metric, the fiber is additive -- a generic b-subset of
ANY trap (rational OR the #663 golden Diophantine set) is Sidon (f=1); so #663's
counterexample is a non-GAP SET not a wall-BLOCK, and route (B) cannot be built from
the golden family alone / P5 TENSION (COMPUTED, evidence FOR closure): high fiber
concentrates INT|Xhat| at small denominators (mass(den<=5) monotone in f: .32 Sidon
-> .55 champion; champion's best nontrivial secondary peak .224) -- "large fiber"
and "Diophantine resonance" are quantitatively in tension / P6 DESCENT (PROVED core,
OPEN recursion): the productive single-class reduction is exactly a dilation (#685-
excluded); genuine fenced blocks reduce only through MULTI-class steps that do not
factor (f(union)=10 != 4=f*f) -- the residual is the open multi-class recursion /
VERDICT: MIXED leaning negative -- the fencing is Diophantine-BLIND to the cheap
denominator horn (empty window, crossover=residual line), route (B) is obstructed by
decoupling, and the tension is positive evidence the fenced wall class may be empty`.

This packet re-runs, ON the fenced class, the single open estimate that our PR
**#663** (`bohr_gap_volume.md`) left standing after proving three cheap bridges
impossible: the **(Bohr -> GAP)** conversion of #661's quadratic-Bohr trapping into
GAP structure, which requires **Diophantine control of the dominant resonance
denominator `q`**. What is new since #663 shipped is that three of today's packets
**fenced the wall's habitat**: a wall-carrying block `V` (`b` distinct integers,
`X = (fL)^{1/b} > 2^{4/3}`) now provably has (i) diameter exponent
`delta = log2(D)/b > alpha/3 + 1/9`, indeed `D > 2^{d/3+b/9}` (**#682**
`corridor_diameter_map.md`, Cor 2; so `delta >= 1/3` at the full corridor),
(ii) large `det G` (**#663** R2), and (iii) it is **not a dilation** (**#685**
`corridor_interior_hunt.md`; the diameter is structural). No one had re-run the
denominator question under those constraints. We do here, and the answer is clean:
**the cheap bounded-denominator horn is provably dead on the fence**, its
crossover coincides with #682's residual line, and the direction control *could*
come from is pinned.

Shared notation (`#661/#663/#655/#646/#643`): a **block** `V` is `b` distinct
integers, normalized `min V = 0`, `gcd = 1`, diameter `D = max V`; the degree-2
signature is `Phi(S) = (|S|, sum_S x, sum_S x^2)`; `f = max fiber`, `L = image
size`; `phi = log2 f / b`, `lambda = log2 L / b`, `eta = 1 - phi`,
`delta = log2 D / b`, `X = 2^{phi+lambda} = (fL)^{1/b}`, `alpha = d/b` with `d`
the dissociation dimension (**#668**). The corridor bound is
`lambda <= alpha + 1/3` (`<=> L <= 2^{d+b/3} <=> X <= 2^{4/3}` inside the corridor
`alpha in (alpha_0, 2/3)`, `alpha_0 = 0.084497`). The moment-curve columns are
`u_i = (1, v_i, v_i^2)`, `X = sum_i eps_i u_i`, `psi_i(theta) = <theta, u_i>`,
`|Xhat(theta)| = prod_i |cos(pi psi_i)|`; the quadratic Bohr set of width `w` is
`Q(theta; w) = { v : ||theta_2 v^2 + theta_1 v + theta_0|| <= w }`.

**One-line verdict.** **MIXED, leaning negative.** On the fenced class the
bounded-denominator rational-resonance horn is **vacuous**: the width-`w` trap can
only *resolve* denominators `q <= Q_res = 1/(2w) <= 0.849 sqrt(b)` (polynomial,
T1), while a residue-class host small enough for the corridor bound needs
`q >= q_cross = 2^{beta b}` (exponential, `beta = delta - alpha/3 - 1/9 > 0` by
#682 Cor 2, T2). The window `[q_cross, Q_res]` is **empty** (T3), and the `delta`
at which it closes (`beta = 0`) is **exactly #682's residual line**
`delta = (alpha+1/3)/3` — the Bohr face and the box face give the *identical*
boundary. So the fencing **does not activate** the cheap horn; it pushes the wall
precisely onto the line where that horn dies. Route **(B)** as literally posed
(extend #663's golden-ratio equidistributing family into the fence) is
**obstructed**: Bohr trapping is *metric* but the fiber is *additive* — a generic
`b`-subset of any trap (rational or golden-Diophantine) is Sidon (`f = 1`, P4), so
the golden family gives a non-GAP *set*, not a high-fiber *block*. And a genuine
positive **(A)** control strip via single-denominator reduction does **not**
intersect the fence: the only productive reduction is a **dilation**, which #685
excludes (P6). What we *do* find pointing toward eventual closure is a
quantitative **tension** (P5): high fiber concentrates the atom mass `INT|Xhat|`
at *small* denominators (monotone in `f`), so the Diophantine resonance route (B)
would need suppresses the very fiber a wall-block requires — direct evidence that
the fenced wall class may be **empty**. Net: three would-be levers of the fencing
are shown Diophantine-blind, the crossover is pinned exactly, and the residual is
localized to the **multi-class recursion** (the open exponential inverse-LO).

Every number is recomputed by
`experimental/scripts/verify_fenced_resonance_window.py` (stdlib-only, zero-arg,
`RESULT: PASS (88/88)`, ~0.4 s / <60 MB under `ulimit -v 2097152`; every
invariance re-checked on exact blocks, both traps' Sidon decoupling enumerated
exactly, the resolution ceiling and residue-count transition recomputed, the
`b_0(beta)` window-emptiness table and the residual-line coincidence re-derived,
the fiber-mass tension quadratured on four blocks, and the multi-class
non-factorization exhibited; several **negative controls** included).

Label key: **PROVED** (complete re-derivable proof, every external theorem quoted
within its printed hypotheses and used only in scope), **COMPUTED** (exact
enumeration), **REFUTED** (a route proved unable to close, obstruction exhibited),
**MEASURED** (exact finite objects, trend read off), **AUDIT** (cross-reference),
**OPEN**.

**Credit.** The fiber bound `f <= 2^{b-d}` and `fL <= 3^b` that the entire fence
rests on are **DannyExperiments #668** (`canonical_transversal_vc_compression.md`).
Built directly on **our #661** (`exp_ilo_fourier.md`: Theorem A atom bound `f <= 2^b
INT|Xhat|`, Theorem B single-frequency quadratic-Bohr trapping at width
`w = sqrt(kappa/eps)`, `kappa = (ln2/2)(eta+1/b)`, and the localization of the wall
to Bohr->GAP), **our #663** (`bohr_gap_volume.md`: R3 the rational-resonance horn
`theta_2 = a/q => <= 2^omega(q)` residue classes, the golden-ratio equidistributing
counterexample R1.4, the R2.4 mod-1 elimination obstruction, the det-G dichotomy
Horn A), **our #682** (`corridor_diameter_map.md`: the diameter coordinate `delta`,
Corollary 2 inflation `D > 2^{d/3+b/9}`, the residual line `delta = (alpha+1/3)/3`,
the rank-`r` transfer), **our #685** (`corridor_interior_hunt.md`: the dilation
invariance of `(f,L)` and the non-dilation fence), and **our #657/#655/#646/#643/
#673/#678/#683** (the corrected Step-B `O(eta b)` exceptions, the `(ILO-moment)`
name and `b=18` champion, `det G`/local-CLT, affine invariance Lemma A, the rank-`r`
GAP box bound Theorem 3, the corridor and `alpha_0`, the tensor-averaging census).
The minimal degree-2 PTE trade support `6` is **scottdhughes #564**. The corrected
`O(eta b)` exception scale and the theorem-import discipline are owed to the Codex
team's read-only import audit (inherited via #661/#663). External inputs cited
**only within printed hypotheses, never re-derived**: three-distance/continued
fractions (classical, for the resolution ceiling); the geometry-of-numbers box
bound (via #673); inverse-Littlewood-Offord (**Tao-Vu; Nguyen-Vu**) and its
exponential-regime counting analogue (**Ferber-Jain-Luh-Samotij**) named as the
open object. **Lane discipline:** this packet stays entirely on the **image face**
(`f`, `L`, `Phi`); it does **not** enter hughes's signed `(LS)/(SV*)/mu_n`
max-fiber reduction object (his #564 target). Where the *inverse* question ("why is
the fiber large") would need signed cancellation over `mu_n`, we record it as a
**transfer, not entry** (P6).

---

## R0 — the target, and the three fencing facts (AUDIT)

**The single open estimate (#663 R5).** #661 proved (unconditional): `f <= 2^b
INT|Xhat|` (Thm A); `f >= 2^{(1-eta)b}` forces `vol(T_kappa) >= 2^{-eta b}/2`
(Lemma 2); one `theta in T_kappa` traps all but `eps b` of the `v_i` in one
quadratic Bohr set `Q(theta; w)`, `w = sqrt(kappa/eps)`, `kappa = (ln2/2)(eta+1/b)`
(Thm B). #663 proved the three cheap bridges Bohr->GAP impossible in general
(large-sieve energy structure-blind `INT|S|^4 = 2b^2-b`; Weyl/major-arc
unavailable, golden-ratio equidistributing counterexample; volume-multiplicity
below `log2 det G >= 2 eta b`), leaving one live requirement: **Diophantine
control of the dominant resonance denominator `q`**. The one horn that closes is
**#663 R3**: if `theta_2 = a/q` with `q = O(1)` and `w < 1/(2q)`, each trapped `v`
satisfies a quadratic congruence `mod q`, so `V` lies in `<= 2^omega(q)` residue
classes.

**What is new: the fence (three of today's packets).** A wall-carrying block
`V` (`X > 2^{4/3}`) now provably satisfies (verifier BLOCK 0 recaps the constants):

1. **Corridor-wedge / diameter inflation (#682 Cor 2).** `alpha in (alpha_0, 2/3)`
   (#678) **and** `delta > alpha/3 + 1/9` (equivalently `D > 2^{d/3+b/9}`), so
   `delta >= 1/3` across the full corridor. Define
   ```
       beta := delta - (alpha/3 + 1/9) = delta - (alpha+1/3)/3  > 0        (fenced)
   ```
   — the signed distance above #682's residual line `delta_res(alpha) =
   (alpha+1/3)/3 = alpha/3 + 1/9`. Verifier BLOCK 0: `delta_res(alpha_0) = 0.13928`,
   `delta_res(2/3) = 1/3`.
2. **Not a dilation (#685).** `(f, L, X)` are exactly dilation-invariant
   (`f(sV) = f(V)`), so a fenced block's structural diameter cannot be an artifact
   of scaling — verifier BLOCK 0 re-checks affine invariance `v -> av+c` and the
   single-residue reduction `v = r + q v''` leave `(f, L)` **exactly** fixed, and a
   **non-affine** relabel `v -> 2^v` changes them (invariance is affine-only).
3. **Large `det G` (#663 R2).** The volume route's failure regime.

The question, precisely: **on this class, can `q` be controlled** — positively
(a Diophantine-control lemma yielding the corridor bound on a sub-class) or
negatively (a fenced counterexample family)?

---

## R1 — T1: the resolution ceiling `Q_res <= 0.849 sqrt(b)` (PROVED, BLOCK 2)

A width-`w` Bohr trap can only "see" arithmetic at bounded denominators. Make this
exact.

> **Theorem 1 (resolution ceiling).** Let `V` be trapped off `eps b` exceptions in
> `Q(theta; w)` with `theta_2 = a/q` rational. The trap **resolves** `q` — i.e.
> `||theta_2 v^2 + theta_1 v + theta_0|| <= w` forces `v` into a proper congruence
> class system `mod q` (the mechanism of #663 R3) — **only if** `q <= Q_res :=
> 1/(2w)`. For a #661-Theorem-B trap of a block with `phi >= 1 - eta`,
> ```
>     w = sqrt( (ln2/2)(eta + 1/b) / eps ) ,   so   w >= sqrt( ln2/(2b) ) ,
>     Q_res = 1/(2w) <= sqrt( b/(2 ln2) ) = (1/sqrt(2 ln2)) sqrt(b) = 0.84932 sqrt(b) ,
> ```
> **polynomial in `b`, uniformly over `eta in (0,1)` and `eps in (0,1]`.**

*Proof.* The values `{theta_2 r^2 + theta_1 r + theta_0 mod 1 : r in Z/q}` lie in
`(1/q)Z + theta_0`; two distinct such values differ by a nonzero multiple of
`1/q`, hence by `>= 1/q`. If `w < 1/(2q)` the width-`w` interval around a target
contains at most the values of a *single* congruence class system (the `<=
2^omega(q)` solutions of the quadratic congruence), which is exactly #663 R3; if
`w >= 1/(2q)` the trap straddles adjacent residues and no `mod q` structure is
forced (verifier BLOCK 2: at `w = 0.10`, `q = 7 <= 1/(2w)=5`... gives 1 residue,
while `q = 100, 600 > 5` give `26, 146 ~ 2wq` residues — the equidistributing
regime). Thus resolution requires `q <= 1/(2w) = Q_res`. For the width: #661
Theorem B has `w = sqrt(kappa/eps)`, `kappa = (ln2/2)(eta + 1/b)`; over the entire
admissible range `eps <= 1` (at most all elements are exceptions) and `eta > 0`,
`w` is minimized at `eps = 1`, `eta -> 0`, giving `w >= sqrt((ln2/2)(1/b)) =
sqrt(ln2/(2b))`. Hence `Q_res = 1/(2w) <= sqrt(b/(2 ln2))`. ∎ (BLOCK 2:
`Q_res_max = 6.01, 8.49, 12.01, 19.0, 26.9` at `b = 50, 100, 200, 500, 1000`;
`1/sqrt(2 ln2) = 0.849322`; any `eps < 1` or `eta > 0` only *increases* `w`, hence
*decreases* `Q_res`, checked.)

The moral: **no Bohr trap arising from a large fiber can certify rationality at a
super-polynomial denominator.** (For `eps <= 1/2`, i.e. a trap of at least half
of `V`, the same bound holds with a factor `sqrt(2)`; the ceiling is
`Theta(sqrt(b))` at the corridor edge `eta ~ 1/b` and `O(1/sqrt(eta))` for fixed
`eta`.)

---

## R2 — T2: the host-smallness threshold `q_cross = 2^{beta b}` (PROVED, BLOCK 3)

The other end of the window: even a *resolved* rational resonance must produce a
**small enough host**, and the fenced diameter makes that expensive.

> **Theorem 2 (host-smallness threshold).** Let `V subseteq [0, D]`, `D = 2^{delta
> b}`, be trapped by a resolved rational resonance `theta_2 = a/q` (so `V` lies, off
> `eps b` exceptions, in `N(q) <= 2^omega(q) = q^{o(1)}` residue classes `mod q`).
> The residue-class host `P` has `log2|P|/b = delta - log2(q)/b + o(1)`, and the
> corridor bound `lambda <= alpha + 1/3` follows from `V subseteq P` (box bound /
> #673 rank-`<=2`) **only if**
> ```
>     log2(q)/b  >=  beta := delta - (alpha+1/3)/3 = delta - alpha/3 - 1/9 ,
>     i.e.  q  >=  q_cross := 2^{beta b} .
> ```
> On the fenced class `beta > 0` (#682 Cor 2), so `q_cross` is **exponential**.

*Proof.* `P = R + q[0, D/q)` with `R subseteq Z/q`, `|R| = N(q) = q^{o(1)}`; hence
`|P| = N(q)·(D/q + O(1)) = D·q^{-1+o(1)}` and `log2|P|/b = delta - log2(q)/b +
o(1)`. Dividing out the common difference is the affine map `v -> (v - r)/q`, which
preserves `(f, L)` exactly (verifier BLOCK 3: dilating `[0,16)` by `q` leaves
`(f,L)` fixed and raises `delta` by *exactly* `log2(q)/b`; run backwards, dividing
by `q` *cuts* `delta` by `log2(q)/b`). For a rank-1 host (`N(q) = 1`) the box
bound gives `lambda <= 3·log2|P|/b = 3(delta - log2 q/b) + o(1)`; `<= alpha + 1/3`
iff `log2 q/b >= delta - (alpha+1/3)/3 = beta` (rank-`<=2` only sharpens the
constant, never the exponential threshold). By #682 Cor 2 the fence sits *above*
the residual line, `delta > alpha/3 + 1/9`, so `beta > 0`. ∎

**Corollary (the box bound is already useless on the fence, BLOCK 3).** Because
`delta > alpha/3 + 1/9`, we have `3 delta > alpha + 1/3`: the trivial diameter box
bound `lambda <= 3 delta` (host `= [0,D]`, #682 Prop 1) *exceeds* the corridor
target. So the horn must genuinely **cut `delta`** — and cutting `delta` by
`beta > 0` needs a common difference `q >= 2^{beta b}`. Verifier BLOCK 3 tabulates:
`alpha = 0.084` fenced `delta = 0.149`, `beta = 0.010`, `3 delta = 0.448 > 0.418
= alpha + 1/3`; `alpha = 2/3` fenced `delta = 0.343`, `beta = 0.010`, `3 delta =
1.030 > 1.000`.

---

## R3 — T3: the window is EMPTY, and its crossover is #682's residual line (PROVED, BLOCK 4)

Combine T1 and T2. The bounded-denominator horn (#663 R3) needs a denominator `q`
that is simultaneously **resolvable** (`q <= Q_res`, T1) and **host-shrinking**
(`q >= q_cross`, T2):

> **Theorem 3 (empty denominator window / main result).** On the fenced class the
> rational-resonance horn requires `q in [q_cross, Q_res] = [2^{beta b},
> 0.84932 sqrt(b)]`. Since `beta > 0`, `2^{beta b} > 0.84932 sqrt(b)` for every
> `b > b_0(beta)`, so **the interval is empty and the horn is vacuous**:
> ```
>     beta      0.0100   0.0500   0.1000   0.1928   0.2222   0.3000
>     b_0       411      53       19       2        2        2         (verifier BLOCK 4)
> ```
> and the gap `q_cross / Q_res` only widens for `b > b_0` (`2^{beta b}` grows
> exponentially, `Q_res` as `sqrt(b)`). Equivalently: **no width-`w` Bohr trap of a
> fenced block can convert its dominant resonance into a corridor-closing GAP by
> the bounded-denominator route.**

*Proof.* `q_cross = 2^{beta b}` (T2) and `Q_res <= 0.84932 sqrt(b)` (T1); a
denominator in `[q_cross, Q_res]` exists iff `2^{beta b} <= 0.84932 sqrt(b)`, false
for `b > b_0(beta)` (BLOCK 4 computes `b_0` by the stated inequality and checks the
gap widens at `4 b_0`). ∎

> **Corollary (Bohr face = box face).** The `delta` at which the window closes is
> `beta = 0`, i.e. `delta = alpha/3 + 1/9 = (alpha+1/3)/3` — **exactly #682's
> residual line** `delta_res(alpha)`. The denominator window (Bohr/#663 face) and
> the diameter residual region (box/#682 face) have the **identical boundary**
> (verifier BLOCK 4 checks the identity at `alpha in {alpha_0, 0.4, 2/3}`).

This is the precise sense in which **the fencing does not help the cheap horn**:
the fence is *defined* by `delta > delta_res` (#682), and `delta > delta_res` is
*exactly* where the horn's window is empty. The fencing pushes every wall block
onto the far side of the one line where bounded-denominator control dies.

**Negative control (BLOCK 4).** The emptiness *hinges* on `Q_res` being polynomial
(T1). The verifier checks the counterfactual: were `Q_res` exponential
(`~ 2^{b/4}`), a window *would* open for `beta < 1/4`. So T3 is not a formality —
it is carried by the `sqrt(b)` ceiling of T1, which is the genuine content.

---

## R4 — P4: fiber-trapping decoupling obstructs route (B) as posed (COMPUTED, BLOCK 1)

Route (B) asks to extend #663's golden-ratio equidistributing family *into* the
fence. There is a structural obstruction, independent of T1-T3:

> **Proposition 4 (decoupling).** Bohr trapping is a **metric** condition; the
> fiber `f` is an **additive** invariant. A generic `b`-subset of *any* quadratic
> Bohr set — rational `a/q` **or** the #663 golden-Diophantine set
> `{v : ||g v^2 + theta_1 v|| <= w}`, `g = (sqrt5-1)/2` — is **Sidon** (`f = 1`):
> being trapped confers no fiber.

Verifier BLOCK 1: the rational `q = 97` trap (`|B| = 1199`) and the golden trap
(`|B| = 503`, reproducing #663 R1.4's `density ~ 0.126`) each yield `f = 1` on
`8/8` sampled `b = 14` subsets, while the *interval* `[0,14)` — additive structure,
not a generic Bohr subset — has `f = 11`. **Consequence for (B):** #663's
equidistributing counterexample exhibits a non-GAP *set*, but a **wall-block**
needs a *large fiber*, which the golden family does not supply. A genuine fenced
counterexample must be **simultaneously additively rich and Diophantine-trapped** —
and P5 shows those two demands pull against each other. Route (B) as literally
posed (the golden family) therefore **cannot be completed**; this is an honest
narrowing of what a negative resolution would require, not a negative resolution.

---

## R5 — P5: the tension — high fiber lives at small denominators (COMPUTED, BLOCK 5)

Where does a high-fiber block's Fourier mass actually sit? The atom bound `f/2^b
<= INT|Xhat|` (#661 Thm A) makes this the right question, and the answer is the
opposite of Diophantine.

> **Proposition 5 (tension, evidence FOR closure).** The mass `INT|Xhat|` of a
> **high-fiber** block concentrates at **small denominators** of `theta_2`; a
> Diophantine (large-`q`) dominant resonance carries **negligible** fiber. Hence
> "large fiber" and "Diophantine dominant resonance" are in quantitative tension.

Verifier BLOCK 5 (exact `Phi` fibers; coarse `30 x 30 x 6` torus quadrature of
`|Xhat|`, mass binned by the denominator of `theta_2`'s nearest rational):
```
    block         f     mass(den<=1)   mass(den<=2)   mass(den<=5)
    sidon12       1        0.051          0.101          0.320
    holes14       6        0.109          0.218          0.425
    interval14   11        0.135          0.270          0.493
    champ18      30        0.186          0.372          0.553      (#655 champion)
```
The small-denominator mass is **monotone increasing in `f`** (`0.320 -> 0.553` at
`den <= 5`), and the #655 champion's best **nontrivial** secondary peak (excluding
the trivial `theta_2 in {0, 1/2}` block-independent parity resonances of #661 R0)
is only `|Xhat| = 0.224` — its fiber is carried by the `q <= 2` major arcs, not by
any rational `a/q` of larger denominator. So the mechanism route (B) would need — a
Diophantine dominant resonance — is exactly the mass distribution of a **low-fiber**
(Sidon-like) block. This is direct evidence that **the fenced wall class may be
empty**: the additive richness that produces a large fiber forces the dominant
resonance toward the smallest denominators, the reducible regime. (It also explains
#685's null hunt: no high-fiber block has a Diophantine-dominated spectrum.)

---

## R6 — P6: the reduction descent, and why there is no single-class strip in the fence (PROVED core + OPEN recursion, BLOCK 6)

Could iterating the horn help — divide out a resolvable `q`, reduce `delta`, repeat?
The one-step reduction is exact, but its productive form is exactly what the fence
excludes.

> **Proposition 6 (descent & stall).** The **single-residue** reduction
> `v = r + q v''` preserves `(f, L)` exactly and cuts `delta` by `log2(q)/b`
> (affine invariance, #643/#685). A block reducible to a *single* class at every
> scale down to `delta_res` is an **affine image of a small block — a dilation**,
> hence **excluded from the fenced class by #685**. A genuine fenced block reduces
> only through **multi-class** steps (`N(q) > 1`), and multi-class does **not
> factor**: cross-class collisions make `f(C_0 cup C_1) != f(C_0) f(C_1)`.

Verifier BLOCK 6: the single-AP tower `{65536·t : t in [0,14)}` has `delta = 1.407`
but `(f, L) = (11, 9132) = ` interval `[0,14)`'s — a **dilation**, #685-excluded;
and the two-class union `C_0 = {3t}`, `C_1 = {1+3t}` (`t in [0,7)`) has
`f(C_0) = f(C_1) = 2` yet `f(C_0 cup C_1) = 10 != 4` — the reduction **stalls** at
multi-class. Those cross-class collisions are the additive structure the reduction
cannot linearize; over `mu_n` they are precisely #663 R2.4's mod-1 elimination
obstruction. **Lane note (transfer, not entry).** Analyzing *which* multi-class
splits carry a large fiber is the signed-`mu_n` inverse question — hughes's #564
`(LS)/(SV*)` object. We do not enter it; we record that the fenced residual is a
**multi-class recursion** whose closure is the open exponential-regime
inverse-Littlewood-Offord (#673), now approached from the denominator side and
stripped of the bounded-`q` shortcut. #663 R3's host, recomputed at bounded `q`
(BLOCK 6: `q = 8`, `D = 2^20`, `b = 60` gives host `~ D/q = 2^17`,
`delta_host = 0.283 ~ delta`), stays diameter-scaled — the concrete restatement of
T2 on a specific instance.

---

## R7 — verdict and the wall, named precisely

```
    TARGET: control the dominant resonance denominator q on the FENCED class
        (delta > alpha/3 + 1/9, large detG, not a dilation).

    T1 RESOLUTION CEILING (PROVED):   a width-w trap resolves q only if
        q <= Q_res = 1/(2w) <= 0.84932 sqrt(b).   [polynomial, uniform in eta,eps]
    T2 HOST THRESHOLD (PROVED):       corridor bound via residue host needs
        q >= q_cross = 2^{beta b},  beta = delta - alpha/3 - 1/9 > 0. [exponential]
        + 3 delta > alpha + 1/3 on the fence: trivial box bound already useless.
    T3 WINDOW EMPTY (PROVED):         [q_cross, Q_res] = [2^{beta b}, 0.849 sqrt b]
        is empty for b > b_0(beta) (411 / 53 / 19 / 2 at beta=.01/.05/.10/>=.19).
        Crossover beta=0  ==  #682 residual line (alpha+1/3)/3.  [Bohr face=box face]

    P4 DECOUPLING (COMPUTED):  trap is metric, fiber additive; generic subset of any
        trap (rational OR golden-Diophantine) is Sidon f=1  =>  #663's counterexample
        is a non-GAP SET not a wall-BLOCK; route (B) needs more than the golden family.
    P5 TENSION (COMPUTED):     high fiber concentrates INT|Xhat| at small denominators
        (mass(den<=5): .32 Sidon -> .55 champion, monotone in f) => "large fiber" and
        "Diophantine resonance" pull apart.  Evidence the fenced wall class is EMPTY.
    P6 DESCENT (PROVED/OPEN):  productive single-class reduction = a dilation (#685-
        excluded); genuine fenced blocks reduce only through non-factoring multi-class
        steps => residual = the open multi-class exponential inverse-LO.
```

**The wall, sharpened (this packet's contribution).** #663 left the wall as
"Diophantine control of `q`." On the fenced class we prove that **bounded-denominator
control is impossible** (T3: the resolvable range is polynomial, the host-shrinking
range is exponential, the window is empty), that this impossibility boundary is
**exactly #682's residual line** (Bohr face = box face), that **route (B) cannot be
built from #663's golden family** (P4 decoupling), and that the residual control, if
any, must come from the **multi-class recursion**, not from a single denominator
(P6). The one genuinely positive signal is the **tension** (P5): the additive
richness that makes a fiber large forces its dominant resonance to the smallest
denominators — quantitative evidence that a fenced wall block, needing *both* a large
fiber *and* a Diophantine (unresolvable) resonance, **may not exist**. Combined with
#661 (upstream spectral shortcuts impossible), #663 (three general bridges
impossible), #682/#685 (the geography and the null hunt), the fence is now known to
be **Diophantine-blind to every cheap denominator lever** — the wall stands
undiminished for those routes, but the class it lives on is pinned to the residual
line, and the tension suggests that class is empty.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/fenced_resonance_window.md` (this).
- Verifier: `experimental/scripts/verify_fenced_resonance_window.py`
  (`RESULT: PASS (88/88)`, ~0.4 s / <60 MB; recomputes `alpha_0`, the residual-line
  identity, the two invariances + a non-affine negative control, both traps' Sidon
  decoupling, the resolution ceiling and residue-count transition, the host
  threshold and box-uselessness, the `b_0(beta)` window-emptiness table + the
  residual-line coincidence + an exponential-`Q_res` negative control, the
  fiber-mass tension on four blocks, and the multi-class non-factorization).
- Read-only inputs: **DannyExperiments #668** `canonical_transversal_vc_compression.md`;
  our **#661** `exp_ilo_fourier.md`, **#663** `bohr_gap_volume.md`, **#682**
  `corridor_diameter_map.md`, **#685** `corridor_interior_hunt.md`, **#657**
  `ilo_moment_structured.md`, **#655** `fiber_image_tradeoff.md`, **#646**
  `moment_map_max_fiber.md`, **#643** `pte_cluster_packing_frontier.md`, **#673**
  (Theorem 3 rank-`r`), **#678** `curve_restricted_product.md`, **#683**
  `championship_census_b19_26.md`; hughes **#564** `w_a_star_pte_lemma.md`.

**Per-claim status.** Theorem 1 (resolution ceiling), Theorem 2 (host threshold)
+ its box-uselessness corollary, Theorem 3 (empty window) + the residual-line
coincidence corollary, and Proposition 6's single-class-reduction core = **PROVED**
(elementary; the `o(1)` in T2 is the explicit `+3(log2 b)/b`/`log2 N(q)/b` overhead,
asymptotic exactly as #682 Prop 1). The bounded-denominator horn on the fenced
class = **REFUTED** as a corridor-closing route (empty window, obstruction the
polynomial `Q_res`). The fiber-trapping decoupling (P4), the multi-class
non-factorization (P6), and the fiber-mass tension (P5) = **COMPUTED** (exact
`Phi` fibers; the `|Xhat|` quadrature is midpoint, used only to *measure* mass
concentration, trend read off = **MEASURED**). The residual-line coincidence with
#682 = **AUDIT** (= #682 Theorem 2, quoted). The unconditional Bohr->GAP on the
fenced class (multi-class recursion / Diophantine control at exponential
concentration) = **OPEN** (unchanged in substance from #663/#673; now known
bounded-denominator-blind).

**Flagged for PI (least-certain, 3 steps).**
(a) **T2's host bound uses `N(q) = q^{o(1)}` and a rank-`<=2` GAP embedding.** The
threshold `q_cross = 2^{beta b}` is exponential regardless of the `q^{o(1)}` factor
or the rank (`1` vs `2` only moves the constant in `(r+2)`), so the empty-window
conclusion (T3) is robust; but the *exact* residual-line coincidence uses rank 1
(single AP). For genuinely multi-class hosts the coincidence is with the rank-`r`
transfer line `(alpha+1/3)/(r+2)` (#682 Section 4), still `beta_r > 0` on the fence.
(b) **P5's tension is measured, not proved.** The monotonicity `f up => small-den
mass up` is exact at the four blocks and `b <= 18`; the asymptotic statement (a
Diophantine-dominated spectrum forces `f = 2^{o(b)}`) is the *inverse* atom
estimate and is **not** proved here — it is offered as evidence, and its proof would
touch the signed `mu_n` object we do not enter.
(c) **P6's stall is a non-factorization, not a nonexistence.** We show single-class
reduction is dilation-only (#685-excluded) and multi-class does not factor; we do
**not** prove no *other* (non-reductive) control exists on the fence — only that the
denominator/reduction family is exhausted, localizing the residual to the
multi-class exponential inverse-LO.

**Exact vs heuristic.** All `f, L, X, delta`, the invariances, the residue counts,
the `b_0(beta)` table, and the multi-class collision counts are exact integer
computation. Theorems 1-3 and Proposition 6's core are elementary closed-form. The
`|Xhat|` mass split (P5) is midpoint quadrature used only to read the concentration
trend. The exponential-regime Bohr->GAP step is cited within its (open) scope and
never re-derived. No signed `mu_n` object entered. No `.tex`/`.pdf` touched.
