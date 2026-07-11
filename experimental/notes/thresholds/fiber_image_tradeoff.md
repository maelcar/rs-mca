# The fiber-image tradeoff: is sup_V (phi + lambda) < 2 log 2 ?

## Status

`R1 REDUCTION rho = phi - gamma + moment-curve subset-sum form (PROVED) / R2
FORBIDDEN-CORNER LOGIC: rho*<log2 <=> near-max fiber & near-max image cannot
co-occur; fstar+L1<=2^b+1 is too weak to force it (PROVED) / R3 COMPUTED
frontier + fit: NEW b=18 champion rho=0.158411 (certified rho* >= 0.158411,
supersedes #643's 0.156659); best rho(b) fits a sub-log2 CAP at R ~ 0.20-0.23,
not a climb to log2 (forced-climb model 17-19x worse) / R4
MECHANISM: deficit is ~99% PROPAGATION (MEASURED); sphere-packing trade bound
(PROVED) shows one trade is too weak -> a cap needs a near-perfect matching / R5
CONDITIONAL CAP: rho* < log2 under the named (ILO-moment) hypothesis, which is
OPEN in the required exponential regime (out-of-scope import in the first draft
flagged by the Codex team's read-only theorem-import audit; reduction PROVED) +
in-hypotheses PARTIAL: the poly window phi >= log2 - C log(b)/b forces rho -> 0
(Nguyen-Vu as cited), pinning any rho->log2 family to the corridor
log b/b << 1-phi/log2 << 1 / R6 bounded-diameter => rho->0 (PROVED subfamily
cap); k-ladder peaks at k=2 (MEASURED) / R7 residuals`.

This packet attacks the **named wall PR #646 redirected to** (its R5): the joint
fiber-image cap. In the notation of our #643 (`pte_cluster_packing_frontier.md`)
and #623 (`pte_extremality_image_face.md`): a **block** `V` is `b` distinct
integers; the degree-2 signature of `S ⊆ V` is `Phi(S) = (|S|, sum_{x∈S} x,
sum_{x∈S} x^2)`; `fstar(V)` is the max fiber, `L1(V)` the number of distinct
signatures, `phi = log fstar / b`, `lambda = log L1 / b`, and the packing rate
`rho = phi + lambda - log 2`. #646 proved `phi* = log 2` and concluded the
`phi*`-route to a sub-`log2` cap on `rho*` is dead; any cap must come from the
**joint** constraint.

> **The question.** Is `sup_V (phi + lambda) < 2 log 2 - eps` for an absolute
> `eps > 0`, uniformly in `b`? Equivalently (since `phi + lambda = rho + log2`),
> **is `rho* < log 2`**? Equivalently: can a block have a near-maximal fiber
> (`fstar = 2^{(1-o(1))b}`) *and* a near-maximal image (`L1 = 2^{(1-o(1))b}`)
> at once?

**One-line verdict. Conditional YES: `rho* < log 2` under one named hypothesis,
`(ILO-moment)` — inverse-Littlewood-Offord-type structure at exponential
concentration — with the reduction PROVED (R5.1) and the hypothesis honestly
labeled OPEN.** The published inverse-LO theorems (Tao-Vu; Nguyen-Vu) assume
*polynomial* concentration with fixed exponent; our first draft imported them
beyond that scope, which was **flagged by the Codex team's read-only
theorem-import audit** — the repaired R5 names the exponential-regime statement
as a hypothesis instead. What survives unconditionally: `rho* <= log 2`, the
exact identification of the residual gap (equality would require a big fiber to
leave the rest of the cube collision-free, a *near-perfect matching* of
propagated collisions), and a new **in-hypotheses PARTIAL** (R5.3): in the
polynomial window `phi >= log2 - C log(b)/b` the corner is dead (`rho -> 0`,
Nguyen-Vu applied within its stated hypotheses), so any `rho -> log2` family is
confined to the corridor `log b/b << 1 - phi/log2 << 1`. Computationally the
best rate climbs to **`0.158411` — a NEW `b=18` champion found by this packet's
census, superseding #643's `0.156659`** — and the three-model fit of `best
rho(b)` over `b = 10..18` **extrapolates to an asymptote `R ≈ 0.20-0.23`, far
below `log 2 = 0.6931`** (the forced-climb model fits 17-19x worse) — a genuine
cap, not a #646-style slow climb. So the *construction* route (a family with
`phi + lambda -> 2 log 2`) is dead in the poly window unconditionally, and dead
everywhere conditional on `(ILO-moment)`.

Every number is recomputed by
`experimental/scripts/verify_fiber_image_tradeoff.py` (stdlib-only, zero-arg,
`RESULT: PASS (36/36)`, ~2.2 s / 56 MB under `ulimit -v 2097152`; every named
witness re-derived exactly, the `b=18` max fiber additionally by DP-independent
direct enumeration). The heavy symmetric census and the fit live in
`experimental/scripts/repro_fiber_image_tradeoff.py` (documented runtime; covers
`b <= 14` — the `b = 16, 18` witnesses came from a deeper overnight hill-climb
whose exact blocks are printed above and certified in the verifier).

Label key: **PROVED** (written re-derivable proof), **COMPUTED** (exhaustive /
certified exact enumeration), **MEASURED** (exact finite objects, trend read
off), **CONDITIONAL** (proved modulo an explicitly named input; each use states
whether the input is a cited theorem applied *within its stated hypotheses* or a
named **OPEN** hypothesis), **AUDIT** (cross-reference), **OPEN**.

**Credit.** Built directly on **our #623** (the `(fstar, L1)` wall, `Lemma B`
trade-deficit `c >= 2^{b-2r}`, `Lemma C` `fstar <= 2^{b-3}`, `rho <= phi`), **our
#643** (`rho = phi + lambda - log2`, affine invariance, the champion
`rho = 0.156659`, the honest bracket `[0.156659, log2]`), and **our #646** (`phi*
= log2`, the polynomial box bound `L1 <= (b+1)(bD+1)(bD^2+1)`, and the poly-loss
lesson that a small-`b` plateau can be an illusion). The minimal degree-2 PTE
trade support 6 is **scottdhughes #564** (`w_a_star_pte_lemma.md`). The analytic
input in R5 is **inverse Littlewood-Offord** (Tao-Vu; Nguyen-Vu, optimal form),
applied **only within its stated polynomial-concentration hypotheses** (R5.3);
the exponential-regime analogue is stated as the named OPEN `(ILO-moment)`
hypothesis — **a scope correction owed to the Codex team's read-only
theorem-import audit**, which flagged the first draft's out-of-scope import. At
exponential concentration the literature has only *counting* inverse-LO
(**Ferber-Jain-Luh-Samotij**), which cannot constrain a per-instance sup (R5.2).
The classical linear-form anticoncentration context is **Erdos-Moser /
Sarkozy-Szemeredi**. All cited by name, none re-derived.

---

## R1 — the reduction (PROVED)

**The deficit-rate identity.** Write the **deficit rate**
`gamma(V) = log2 - lambda = (1/b) log( 2^b / L1 )  >= 0` (it is `0` iff `L1 =
2^b`, a Sidon block). Then trivially

```
    rho = phi + lambda - log 2 = phi - gamma .                         (id)
```

Since `phi <= log2` (only `2^b` subsets) and `gamma >= 0`, `rho <= log2` with
equality **iff** `phi = log2` and `gamma = 0` simultaneously. In particular any
block with `phi <= log2 - delta` already has `rho <= log2 - delta`. **So
`rho -> log2` forces `phi -> log2` (near-max fiber) AND `gamma -> 0` (near-max
image).** The whole question is whether these two can hold together. (Verifier
BLOCK 0.)

**The moment-curve form (PROVED, verifier BLOCK 1).** The signature map is
`x ↦ (1·x, v·x, v^2·x)` on the cube `{0,1}^b`, i.e. the linear map with columns
the `b` points `u_i = (1, v_i, v_i^2)` on the **moment curve** `t ↦ (1,t,t^2)` in
`Z^3`. Hence

```
    L1(V)    = # distinct subset sums of { u_1, ..., u_b } ,
    fstar(V) = max multiplicity of a subset sum of { u_1, ..., u_b } .
```

So `rho*` is exactly the **max-multiplicity vs image-size (anticoncentration)
tradeoff for `b` points on the moment curve**. The constant coordinate `1` pins
the cardinality `w = |S|`; dropping it can only enlarge fibers, so the linear
concentration `fstar_1 := max_s #{S : v·x = s} >= fstar` (verifier checks
`fstar_1 >= fstar`). This inequality is the hinge of R5.

The affine invariance of `fstar, L1, rho` (#643 Lemma A) is inherited: it is the
statement that the tradeoff depends only on the affine class of the moment-curve
point set.

---

## R2 — the forbidden corner, and why the simple bound cannot close it (PROVED)

By (id), `rho* < log2` **iff** there is no sequence of blocks with `phi -> log2`
and `gamma -> 0`, i.e. iff `fstar` and `L1` **cannot both be `2^{(1-o(1))b}`**.
Call `(fstar ≈ 2^b, L1 ≈ 2^b)` the **cap-corner**.

The only elementary joint constraint is #623's `fstar + L1 <= 2^b + 1` (the max
fiber alone contributes `fstar - 1` to the deficit `c = 2^b - L1`). **This is far
too weak to forbid the corner** (verifier BLOCK 2): for any `beta < 1` it permits
`fstar = L1 = 2^{beta b}`, since `2^{beta b} + 2^{beta b} = 2^{beta b + 1} <=
2^b + 1` as soon as `beta <= 1 - 1/b`. E.g. `beta = 0.9` is permitted and would
give `rho = (0.9 + 0.9 - 1) log2 = 0.8 log2 = 0.555`, close to `log2`. So a cap
**cannot** come from cardinality bookkeeping; it must use the arithmetic of the
moment curve. (The bound itself is not slack at small `b`: the `b=6` and `b=8`
`rho`-optimizers saturate it **exactly** — `2 + 63 = 2^6 + 1`, `2 + 255 = 2^8 +
1`, verifier BLOCK 0 — but that tightness lives at the clean-single-trade corner
`fstar = 2, L1 = 2^b - 1`, the opposite end from the cap-corner.) (The reason `fstar + L1 <= 2^b` is weak is exactly (id): a giant
fiber `fstar = 2^b/2^{o(b)}` leaves `L1 <= 2^b(1 - 2^{-o(b)})`, still rate `log2`
— losing a `(1 - 2^{-o(b)})` *fraction* of subsets costs only `o(1)` of
`lambda`.)

**Consequence.** The cap must show: *the same arithmetic structure that produces
a big fiber also collapses the image.* R4-R5 do this; R3 measures it.

---

## R3 — computed frontier and the fit (COMPUTED)

Two facts make the computation tractable and its extrapolation meaningful:

- **Moderate diameter is optimal** (COMPUTED, verifier BLOCK 6 + repro). Spreading
  a block increases the image but destroys the fiber faster: at `b = 12` the best
  `rho` over randomized search falls `0.135 -> 0.090 -> 0.057` as the diameter
  grows `2b -> 8b -> 50b` (toward the Sidon corner `rho = 0`). The max-`rho`
  blocks are dense symmetric interval-with-holes clusters of diameter `~1.7-2.2b`
  (matching and slightly widening #643's read; capping the search below `~1.8b`
  measurably undershoots). Larger single-block `b` at bounded relative diameter has
  `L1 = poly(b)` (R6), so its rate is realized only by **tensoring** a moderate
  finite block (which reproduces its rate exactly, #643 Prop E). Hence
  `rho* = sup_b [ max over moderate-diameter blocks ] `, and the census below
  targets exactly that. Structured non-interval families confirm the picture
  (repro): two-scale unions and GAPs top out at `rho ≈ 0.145 < 0.156659`, and
  geometric (Sidon-like) sets give `rho = 0` — none beats the interval-with-holes
  champion, so the max-`rho` structure is genuinely the dense symmetric cluster.

- **The #646 lesson cuts both ways.** A plateau can hide a slow climb to `log2`
  (`~ log2 - C log b / b`), and a climb can hide a cap. We therefore **fit**
  `best rho(b)` against three models and compare.

Best-known `rho(b)` (deep symmetric-hole census, even `b`; every listed witness
re-derived exactly in verifier BLOCK 0/7; the `b=18` max fiber additionally
re-derived by DP-independent direct weight-9 enumeration):

```
    b         6       8      10      12      14      16      18
  rho(b)   0.1129  0.0862  0.1310  0.1414  0.1567  0.1554  0.1584
  fstar        2       2       4       6      12      18      30
  L1          63     255     949    3723   12239   43737  151275
  phi      0.1155  0.0866  0.1386  0.1493  0.1775  0.1806  0.1890
  lambda   0.6905  0.6927  0.6855  0.6852  0.6723  0.6679  0.6626
```

**A NEW champion at `b = 18`:** `V = {2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,
32,33,34}` (symmetric about 18, diameter 32), `fstar = 30`, `L1 = 151275`,
**`rho = 0.158411`** — supersedes #643's `b=14` record `0.156659` by `+0.00175`
and is the new **certified `rho* >= 0.158411`** (this packet's census; validated
by two independent DPs and full `2^18` brute force during the search, and
re-derived in the verifier). The `b=8` dip is structural (the minimal degree-2
trade needs 6 coordinates, hughes #564). Note the two exponents move in
**opposite directions**: `phi` climbs `0.116 -> 0.189` while `lambda` *falls*
`0.691 -> 0.663` — `rho -> log2` would need `phi -> 0.693` with `lambda`
recovering to `log2`, and both trends point the other way. Search reliability:
exact-or-saturated through `b = 18`; at `b = 20` the search no longer converges
(weak lower bound `0.1515`, not used). Optimizer diameters sit at `~1.7-2.2 b`
(searches capped below `~1.8b` undershoot — measured pitfall).

**The fit.** Least squares of `rho(b)` over the reliable window `b = 10..18`
against

```
    (M1) cap:        rho = R - C/b
    (M2) climb:      rho = log2 - C log(b)/b       (asymptote FORCED to log2)
    (M3) cap+poly:   rho = R - C log(b)/b
```

gives (recomputed from the verified table values above; repro re-fits its own
`b <= 14` census the same way):

```
    M1 cap:       R = 0.1969  C = 0.648   RMS = 0.0031
    M2 -> log2:              C = 2.798   RMS = 0.0595   (17-19x worse)
    M3 cap+poly:  R = 0.2271  C = 0.409   RMS = 0.0034
```

Smaller windows tell the same story (`R ≈ 0.17-0.27` on `b in {6..14}` subsets).
The two **cap** models fit `17-19x` better than (M2), the model forced to climb
to `log2`; the asymptote lands at `R ≈ 0.20-0.23`, **far below `log2 = 0.6931`**.
Read against #646's own warning — there the interval's `phi` genuinely climbed to
`log2` because its box is `poly(b)`, and `M2`-type fits won — the contrast is
decisive: here `gamma` does **not** vanish along the optimizers (`gamma` *grows*
along the champions, `0.0026 -> 0.0305` from `b=6` to `b=18`), so `rho = phi -
gamma` shows no route to `log2`. **The data says CAP, with `rho* ≈ 0.16-0.23`.**
(The fit is suggestive, not a proof — the champions still edge upward with `b`;
R5 gives the conditional proof and R5.3 the in-hypotheses poly-window partial.)

The exact `(phi, gamma)` tradeoff at `b = 12` (verifier BLOCK 7) shows the
mechanism quantitatively: the minimum deficit rate `gamma` achievable at fiber
rate `>= phi0` is **increasing** in `phi0` (`0.0075, 0.0075, 0.0090, 0.0112,
0.0176` at `phi0 = 0.06 .. 0.14`) — more fiber demonstrably costs more deficit.

---

## R4 — the mechanism: propagation, and why one trade is too weak (MEASURED + PROVED)

**Deficit is ~99% propagation (MEASURED, verifier BLOCK 4).** Decompose the
deficit `c = 2^b - L1 = (fstar - 1) + (rest)`, where `fstar - 1` is the
contribution of the single heaviest fiber and `rest` is every other collision.
On every heavy block the heaviest fiber is negligible:

```
    block        b   fstar   L1      c       fstar-1   propagation   prop/c
    interval     14    11    9132    7252       10        7242       0.999
    champion     14    12   12239    4145       11        4134       0.997
    16-hole      16    18   39425   26111       17       26094       0.999
```

So a block with *any* nonzero fiber drags in a **macroscopic** number of *other*
collisions: the trades responsible for the heavy fiber also collide subsets all
over the cube. This is the propagation that R5 must quantify — and it is why the
cap has a chance.

**Sphere-packing trade bound (PROVED, verifier BLOCK 5).** A heavy fiber `F` of
weight `w*` with `|F| = fstar = 2^{Rb}` (`R = phi/log2`, the code rate) is a
binary code in the `w*`-layer. By sphere-packing, two codewords lie within
Hamming distance `delta* b` where `H_2(delta*/2) = 1 - R`, i.e. **`V` contains a
degree-2 PTE trade of relative support `<= delta* = 2 H_2^{-1}(1 - R)`**, which
`-> 0` as `R -> 1`. This refines #623 Lemma B's "`fstar >= 2` ⇒ some trade of
support `in [6, b]`" to a *rate-dependent* support bound (`R = 0.9 ⇒ delta* =
0.026`; `R = 0.99 ⇒ delta* = 0.0017`).

**But one trade cannot cap (PROVED, verifier BLOCK 5).** Lemma B turns that trade
(support `2r`) into deficit `c >= 2^{b-2r}`, hence `L1 <= 2^b - 2^{(1-delta*)b} =
2^b(1 - 2^{-delta* b})`, forcing only

```
    gamma >= (1/b) log( 1 / (1 - 2^{-delta* b}) )  ->  0   as  b -> infinity.
```

A *single* trade — however small its support — forces a **vanishing** deficit
rate. So the cap **cannot** be obtained trade-by-trade; it needs the propagated
collisions of **many** trades assembled into a matching covering a `1 - 2^{-Θ(b)}`
fraction of the cube (a **near-perfect matching** of the collision graph, which
would give `c >= 2^b(1 - 2^{-Θ(b)})`, i.e. `L1 <= 2^{(1-Θ(1))b}`). This
near-perfect-matching requirement is the exact unconditional obstruction. R5
names precisely this as the `(ILO-moment)` hypothesis (OPEN) and proves the cap
from it; in the polynomial window the published inverse-LO theorems supply it
as cited (R5.3).

---

## R5 — the conditional cap: `rho* < log 2` under the named `(ILO-moment)` hypothesis

**Correction and credit.** An earlier draft of this section derived the
hypothesis below *from* the inverse Littlewood-Offord theorems of Tao-Vu /
Nguyen-Vu. That import was **flagged by the Codex team's read-only
theorem-import audit** as out of scope, and the flag is correct: those theorems
assume *polynomial* concentration `rho >= n^{-C}` with `C` **fixed** (their GAP
rank and volume constants depend on `C`), while the cap needs the *exponential*
regime `fstar >= 2^{(1-eta)b}` — concentration `2^{-eta b}`, i.e. `C ~ eta b /
log b` **growing with `b`** — where the cited statements' implicit constants
become `b`-dependent and the `omega(eta) -> 0` conclusion does **not** follow.
The section is restructured accordingly: 5.1 names the exponential-regime
statement as an **OPEN hypothesis** and proves the reduction from it; 5.2 states
what is and is not known about the hypothesis; 5.3 keeps the **in-hypotheses**
part of the original argument as a partial (the poly-window cap), which is what
the published theorems genuinely give.

### 5.1 The named hypothesis and the reduction (reduction PROVED; hypothesis OPEN)

> **(ILO-moment) hypothesis (OPEN / CONJECTURAL).** There exist `eta_0 > 0` and
> a function `omega(eta) -> 0` (as `eta -> 0`) such that every block `V` with
> `fstar(V) >= 2^{(1-eta) b}` (`eta < eta_0`) has `L1(V) <= 2^{omega(eta) b}`.

> **Theorem (conditional cap; the reduction is PROVED).** `(ILO-moment)` implies
> `rho* < log 2`, i.e. `sup_V (phi + lambda) < 2 log 2`.

*Proof (self-contained).* Take `delta in (0, eta_0 log2)` and any block.

- If `phi <= log2 - delta`: by (id), `rho = phi - gamma <= phi <= log2 - delta`.
- If `phi > log2 - delta`: then `fstar > 2^{(1 - eta) b}` with
  `eta = delta / log2 < eta_0`, so by `(ILO-moment)` `L1 <= 2^{omega(eta) b}`,
  hence `lambda <= omega(eta)` and `rho = phi + lambda - log2 <= omega(eta)`.

So `rho* <= max( log2 - delta, omega(delta/log2) )` for every such `delta`.
Since `omega(eta) -> 0` as `eta -> 0` while `log2 - delta -> log2`, any
sufficiently small fixed `delta_0` has `omega(delta_0/log2) <= log2 - delta_0`,
giving `rho* <= log2 - delta_0 < log2`. ∎

*Why the hypothesis carries this name.* If `fstar >= 2^{(1-eta)b}` then the
**linear** concentration is at least as large (`fstar_1 >= fstar`, R1, verifier
BLOCK 1), so `(ILO-moment)` is exactly an inverse Littlewood-Offord-type
statement — "large concentration of `v·x` forces arithmetic structure so rigid
that the *moment image* is exponentially small" — posed at **exponential**
concentration, which is beyond the published theorems.

### 5.2 Status of the hypothesis: supported, plausible, OPEN

- **In the polynomial window it is a theorem** (5.3): for `eta = O(log b / b)`
  the cited inverse-LO applies as stated and yields `L1 <= poly(b)`.
- **In the exponential regime it is genuinely open.** Per-instance structure at
  concentration `2^{-eta b}` (fixed small `eta`) is **not** covered by Tao-Vu /
  Nguyen-Vu. What the literature offers there is *counting*, not structure:
  Ferber-Jain-Luh-Samotij bound the **number** of blocks with concentration
  `>= 2^{-eta b}`; a counting theorem constrains "almost all" blocks and cannot
  bound a supremum over all blocks. We know of no published per-instance
  exponential-regime inverse-LO with explicit constants, so none is cited.
- **The computed tradeoff is consistent with it** (verifier BLOCK 7): at `b=12`
  the minimum deficit rate `gamma` achievable at fiber rate `>= phi0` increases
  with `phi0` (`0.0075 -> 0.0176` over `phi0 = 0.06 -> 0.14`), and every
  high-`phi` census block has a collapsing image — the hypothesis direction, at
  toy scale.

### 5.3 The in-hypotheses partial: the poly-window corner is dead (CONDITIONAL on the cited theorem)

> **Proposition (poly-window cap).** Fix `C > 0`. Along any sequence of blocks
> with `fstar(V_b) >= 2^b · b^{-C}` (i.e. `phi >= log2 - C (log b)/b`), the
> image is polynomial: `L1 <= b^{O_C(1)}`, so `lambda = O_C(log b / b)` and
> `rho(V_b) -> 0`.

*Proof (modulo the cited Nguyen-Vu optimal inverse-LO, applied within its stated
polynomial-concentration hypotheses).* Subset sums on `{0,1}^b` and Rademacher
sums on `{-1,1}^b` are affinely equivalent (`sum_{x in S} x = (sum V + sum_i
eps_i v_i)/2`), so concentration transfers exactly: `rho_1 := fstar_1 / 2^b >=
fstar / 2^b >= b^{-C}` (using `fstar_1 >= fstar`, R1). By optimal inverse-LO at
fixed `C`, all but `O_C(1)` of the `v_i` lie in a GAP `P` of rank `r = O_C(1)`
and volume `|P| = O_C(rho_1^{-1}) = O_C(b^C)` (a zero element, if present after
affine normalization, joins the exceptional set). **GAP ⇒ small moment-image:**
writing each `v ∈ P` as `v = a_0 + sum_{i<=r} x_i g_i` (`0 <= x_i < L_i`), a
subset's first moment has `g`-coordinates in `[0, b L_i]`, so its image lies in
a box of size `(b+1) prod_i (b L_i + 1) <= b^{r+1} |P|`; the second moment
`sum v^2` is a linear form in the `O(r^2)` monomials `x_i x_j`, so its image
lies in a box of size `b^{O(r^2)} |P|^2`. Subsets of the `O_C(1)` exceptional
elements multiply the number of distinct signatures by at most `2^{O_C(1)}`.
Total: `L1 <= b^{O_C(1)}`, i.e. `lambda = O_C(log b / b) -> 0`; and
`rho = phi + lambda - log2 <= lambda -> 0` since `phi <= log2`. ∎

> **Corollary (the corridor).** Any sequence with `rho(V_b) -> log2` must have
> `eta_b := 1 - phi/log2 -> 0` **and** `eta_b · b / log b -> infinity`. *(Proof:
> `rho <= phi` forces `eta_b -> 0`; if `eta_b <= C log b / b` along a
> subsequence, the Proposition gives `rho -> 0` there, a contradiction.)* The
> construction route to `2 log 2` is therefore **dead in the polynomial window**
> and confined to the corridor `log b / b << eta_b << 1`; `(ILO-moment)` asserts
> precisely that this corridor carries no near-max image.

**Label summary for R5.** Reduction + corridor corollary logic = `PROVED`.
Poly-window proposition = `CONDITIONAL` (cited theorem, applied in-hypotheses).
`(ILO-moment)` itself = `OPEN / CONJECTURAL`. The headline cap `rho* < log2` =
`CONDITIONAL on (ILO-moment)`. The `eps` is **non-explicit** in every version
(it inherits `omega`); see R7.

---

## R6 — two clean unconditional statements (PROVED + MEASURED)

**Bounded-diameter blocks cannot approach the corner (PROVED, verifier BLOCK 6).**
If `V` is affine-normalized (`min = 0`, `gcd = 1`) with diameter `D`, then every
signature lies in `[0,b] × [0,bD] × [0,bD^2]`, so (the #646 box bound)
`L1 <= (b+1)(bD+1)(bD^2+1)` and thus

```
    rho(V) <= phi + lambda - log2 <= (1/b) log[ (b+1)(bD+1)(bD^2+1) ] .
```

For `D = C b` this is `O(log b / b) -> 0` (verifier: the ceiling falls
`1.005, 0.511, 0.297, 0.095, 0.029` at `b = 20, 50, 100, 400, 1600`, `D = 2b`).
So **any family with `rho` bounded away from `0` must have super-polynomial
diameter** — the tradeoff sup is genuinely a tensor limit of finite blocks, never
a bounded-relative-diameter family. (This is the rigorous form of "the champions
are moderate-diameter but their rate is a tensor limit.")

**The `k`-moment ladder peaks at `k = 2` (MEASURED, verifier BLOCK 3).** For the
degree-`K` signature `(|S|, p_1, ..., p_K)`, define `rho_K` analogously. On the
champion: `rho_1 = 0.1079`, `rho_2 = 0.156659`, `rho_3 = 0.0490`. Two readings:

- **`rho_1 > 0`**: even a *single* linear form has a positive packing rate — the
  "one moment gives rate `log2`" guess is false. The `k = 1` problem is the same
  question one dimension down (max subset-sum multiplicity vs #distinct subset
  sums), and is the clean Erdos-Moser / Littlewood-Offord warm-up for R5.
- **`rho_K -> 0` as `K` grows** (`K = b` determines `S`, so `fstar = 1`,
  `rho = 0`). The degree-2 map is the interesting peak — consistent with #646's
  finding that the second moment is exactly what lifts the rate off the linear
  floor without yet killing the image.

---

## R7 — honest residuals (OPEN)

1. **The hypothesis `(ILO-moment)` (the live wall).** `rho* <= log2` is proved;
   `rho* < log2` is proved only **conditional on the OPEN `(ILO-moment)`
   hypothesis** (R5.1). By the corridor corollary the battlefield is exactly
   `log b/b << eta << 1`: prove per-instance inverse-LO structure at exponential
   concentration there (only *counting* results exist, R5.2), or refute
   `(ILO-moment)` with a corridor construction — a family with
   `fstar = 2^{(1-eta)b}` and `L1 = 2^{Omega(b)}` for `eta -> 0` (note: refuting
   the hypothesis would re-open but not decide the cap).
2. **The unconditional matching route.** Alternatively, prove the
   near-perfect-matching statement of R4 (a big fiber forces `>= 2^b(1 -
   2^{-Θ(b)})` propagated collisions) directly on the moment curve. The
   sphere-packing bound gives the small trades; assembling their `C'`-ranging
   matchings into a near-perfect matching, with the double-counting controlled
   (the `C'`-ranges of distinct trades overlap), is the open combinatorial core.
   *This is where such an argument silently breaks and we do not claim it.*
3. **Explicit `eps`.** Even granting `(ILO-moment)`, the `eps` is non-explicit
   (it inherits `omega`). The computed fit suggests the truth is `rho* ≈
   0.16-0.23` (`phi + lambda ≈ 0.85-0.92`, vs `2 log2 = 1.386`), but that is
   MEASURED, not a proved bound — and the champions still edge upward
   (`0.1567 -> 0.1584` from `b=14` to `b=18`).
4. **Exact `rho*`.** No closed form. The bracket sharpens #643's
   `[0.156659, log2]` to `[0.158411, log2)` with the upper end strict
   **conditionally on `(ILO-moment)`**; unconditionally the bracket is
   `[0.158411, log2]` with the poly window excluded (R5.3).

---

## Summary

```
    QUESTION (#646 R5):  is sup_V (phi+lambda) < 2 log2, i.e. rho* < log2 ?
    ANSWER:              YES, conditional on the named (ILO-moment) hypothesis
                         (OPEN in the required exponential regime).

    id:      rho = phi - gamma;  rho->log2 needs phi->log2 AND gamma->0.
    weak:    fstar+L1<=2^b+1 permits fstar=L1=2^{0.9b} (rho=0.555) -- cannot cap.
    reduce:  rho* = max-multiplicity vs image tradeoff for b points on (1,t,t^2).
    measure: deficit is ~99% PROPAGATION; best rho(b) climbs to 0.158411 (NEW
             b=18 champion, certified rho* >= 0.158411) and the b=10..18 fit
             extrapolates to R ~ 0.20-0.23 << log2 (CAP; the climb-to-log2
             model M2 fits 17-19x worse).
    cap:     NAMED (ILO-moment) hypothesis (OPEN) => rho* < log2 (reduction
             PROVED). In-hypotheses partial: poly window phi >= log2 - C log b/b
             forces rho -> 0 (Nguyen-Vu as cited), so any rho -> log2 family is
             confined to the corridor log b/b << 1 - phi/log2 << 1.
             Construction route: DEAD in the poly window; corridor-conditional
             elsewhere. (Exponential-regime import in the first draft flagged by
             the Codex team's read-only theorem-import audit; repaired here.)
    open:    (ILO-moment) in the corridor (only counting inverse-LO exists at
             exponential concentration) / the matching route / explicit eps.
```
