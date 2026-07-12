# Bohr -> GAP: converting the volume of quadratic resonances into rank

## Status

`R0 TARGET: the single Step-B residual localized by #661 -- turn the VOLUME
vol(T_kappa) >= 2^{-eta b}/2 of trapping frequencies into a containing GAP of rank
d(eta)=o(1/eta) (=> (ILO-moment), => rho*<log2 unconditional) / R1 V2 (large-sieve
/ Weyl): T_kappa forces a near-full QUADRATIC WEYL SUM |S(t1,t2)|>=(1-2pi^2 kappa)b
on an area >= 2^{-eta b}/2 (PROVED); but the moment-curve additive energy is
STRUCTURE-BLIND -- int|S|^4 = 2b^2-b for EVERY b-set (PROVED) -- so the
large-sieve / moment method is VACUOUS at constant eta (reaches only the corridor
eta >~ 2 log2(b)/b) (REFUTED as a closing route); and Weyl's inequality is
UNAVAILABLE for an arbitrary set (no interval to difference over), so the
major-arc route is circular -- it bites only when V is already a short interval
(= #657 Thm 1) (REFUTED as a general route) / R2 V1 (volume->structure): the
det-G DICHOTOMY -- Horn A detG<=2^{2 eta b} => normalized diam <= 2^{eta b} =>
#657 Thm1 => lam2<=3eta+o(1) (PROVED, rank 1); the branch decomposition gives a
per-branch Gaussian volume <= (4pi/3)(kappa b)^{3/2}/sqrt(detG) (PROVED), whence
resonance MULTIPLICITY (=> joint rank) is forced only when detG exceeds 2^{2 eta b}
by a further poly*2^{cb} factor -- quantifying EXACTLY the volume != rank gap; and
the two-frequency elimination is linear over R but FAILS mod 1 (PROVED
obstruction) / R3 the one horn that CLOSES: rational resonance theta2=a/q (bounded
q) => v in <= 2^omega(q) residue classes = rank-1 GAP (PROVED; = #661 CONDITIONAL)
/ R4 verifier PASS (56/56), ~2 s / R5 VERDICT: Step B does NOT close via V1/V2;
both routes are localized with PRECISE, verified obstructions (energy
structure-blindness; mod-1 elimination failure; the volume-threshold gap). The
missing input is unchanged -- Diophantine control of the resonance denominator /
per-instance exponential inverse-LO -- but three shortcut families are now proved
impossible, and the residual is pinned to LARGE-detG (spread) blocks`.

This packet attacks the **single estimate** localized by our PR #661
(`exp_ilo_fourier.md`): the **(Bohr -> GAP)** conversion that is the last open
half of the corrected Step B (#657 `ilo_moment_structured.md`; the corridor is
#655 `fiber_image_tradeoff.md`). In the shared notation: a **block** `V` is `b`
distinct integers; `Phi(S) = (|S|, sum x, sum x^2)`; `fstar` = max fiber, `L1` =
image size; `phi_2 = (log2 fstar)/b`, `lam_2 = (log2 L1)/b`, `eta = 1 - phi_2`.
Moment-curve columns `u_i = (1, v_i, v_i^2)`; `X = sum_i eps_i u_i`;
`psi_i(theta) = <theta,u_i>`; `|Xhat| = prod_i |cos(pi psi_i)|`. The **quadratic
Weyl sum** is `S(t1,t2) = sum_i e(t1 v_i + t2 v_i^2)`, `e(x) = exp(2 pi i x)`, and
`T_kappa = { theta in [0,1)^3 : sum_i ||psi_i(theta)||^2 <= kappa b }`.

**#661's residual, verbatim.** #661 proved (unconditional): `fstar <= 2^b INT|Xhat|`
(Theorem A); `fstar >= 2^{(1-eta)b}` forces `vol(T_kappa) >= 2^{-eta b}/2` with
`kappa = (ln2/2)(eta + 1/b)` (Lemma 2); and **one** `theta in T_kappa` traps all
but `eps b` of the `v_i` in **one** quadratic Bohr set `Q(theta,w)` of width
`w = sqrt(kappa/eps)` (Theorem B). The wall: a **single** frequency's Bohr trap is
far weaker than GAP containment; the **volume** `2^{-eta b}` of `T_kappa` is an
exponentially rich family of simultaneous trapping frequencies, and the missing
move is **volume of resonances -> rank/size of a GAP** (all but `O(eta b)`
exceptions, rank `d(eta) = o(1/eta)`, size `2^{O(eta)b}`).

**One-line verdict.** **Step B does not close by either route, and this packet
proves *why* — pinning three concrete shortcut families as impossible.** On the
**large-sieve side (V2)**: `T_kappa` does force a near-full quadratic Weyl sum on
a `2^{-eta b}`-area set (PROVED), but the moment curve's additive energy is
**structure-blind** — `INT|S|^4 = 2b^2 - b` for *every* block (PROVED) — so no
energy-increment / large-sieve / moment argument can force structure; the method
is **vacuous at constant `eta`**, reaching only the known corridor
`eta >~ 2 log2(b)/b`. And **Weyl's inequality is not available** for an arbitrary
`b`-set (there is no ambient interval to difference over), so the "major arcs"
route is circular — for a general set "near-full Weyl sum" *is* the Bohr condition
itself, with no arithmetic content; it bites only when `V` already lies in a short
interval, where #657 Theorem 1 wins outright. On the **volume->structure side
(V1)**: the genuine win-win dichotomy is real but **only its easy horn closes** —
`det G <= 2^{2 eta b}` forces normalized diameter `<= 2^{eta b}` hence #657 Theorem
1 (`lam_2 <= 3 eta + o(1)`, rank 1, PROVED); the hard horn does **not**, because a
branch decomposition of `T_kappa` shows each single resonance branch already
carries Gaussian volume `(4pi/3)(kappa b)^{3/2}/sqrt(det G)`, so Lemma 2's volume
`2^{-eta b}` forces resonance **multiplicity** (the prerequisite for joint rank)
**only** when `det G` exceeds the volume threshold `2^{2 eta b}` by a further
`poly * 2^{cb}` factor — a precise quantification of the volume `!=` rank gap. The
two-frequency elimination that would manufacture rank is **linear over `R` but
fails mod 1** (real coefficients do not commute with `||.||`), a PROVED
obstruction. The one horn that *does* close is rational resonance (`theta_2 = a/q`,
bounded `q`), matching #661's CONDITIONAL case exactly. Net: the wall is unmoved,
but three would-be shortcuts are now proved dead and the residual is localized to
large-`det G` (spread) blocks.

Every number is recomputed by
`experimental/scripts/verify_bohr_gap_volume.py` (stdlib-only, zero-arg,
`RESULT: PASS (56/56)`, ~2 s / <60 MB under `ulimit -v 2097152`; the moment-curve
energy identity re-derived exactly on five block families, the Weyl lower bound
certified on sampled `T_kappa` frequencies, the per-branch volume bound checked on
enumerated sublevel sets, the `b=18` champion carried throughout).

Label key: **PROVED** (complete re-derivable proof, every external theorem quoted
with its exact hypotheses and used only in scope), **REFUTED** (a route proved
unable to close, with the obstruction exhibited), **COMPUTED** (exact
enumeration), **MEASURED** (exact finite objects, trend read off), **CONDITIONAL**
(proved modulo a named cited-in-scope input), **AUDIT** (cross-reference),
**OPEN**.

**Credit.** Built directly on **our #661** (`exp_ilo_fourier.md`: Theorem A atom
bound, Lemma 2 sublevel volume, Theorem B single-frequency quadratic-Bohr
trapping, the affine-invariant Fourier reduction, and the localization of the wall
to `Bohr -> GAP`), **our #657** (`ilo_moment_structured.md`: the corrected Step-B
chain with **`O(eta b)`** exceptions, Theorem 1 AP box bound
`L1 <= (b+1)(bD+1)(bD^2+1)`, Theorem 3 GAP box bound, the reduction
`omega = (d+2)eta`), **our #655** (`fiber_image_tradeoff.md`: the `(ILO-moment)`
name and reduction, the corridor `log b/b << eta << 1`, the `b=18` champion
`V = {2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34}` with
`fstar=30, L1=151275`), **our #646** (`moment_map_max_fiber.md`: `phi*=log2`, the
interval box bound and `det G = b^9/2160`, the local-CLT covolume), and **our
#643** (`pte_cluster_packing_frontier.md`: `rho = phi + lam - log2`, affine
invariance Lemma A). The minimal degree-2 PTE trade support 6 is **scottdhughes
#564**. **The corrected Step-B exception scale `O(eta b)` (not #657's printed
`o(b)`) and the discipline of never importing a theorem past its printed
hypotheses are owed to the Codex team's read-only theorem-import audit** — this
packet inherits #661's incorporation of that correction. External inputs cited
**only within printed hypotheses, never re-derived**: **Weyl**'s inequality (its
hypothesis of summation over an *interval* is exactly what an arbitrary block
lacks — R1.4); the **large sieve** (Montgomery; the `L^2`/`L^4` moment method); the
**Halász** method (many resonant frequencies -> additive structure), whose
input here is shown structure-blind on the moment curve; the **Vinogradov** /
inverse-Weyl philosophy (large exponential sum -> major arcs), shown circular for
general sets; inverse-Littlewood-Offord (**Tao-Vu; Nguyen-Vu**, optimal) in the
polynomial window; its exponential-regime **counting** analogue
(**Ferber-Jain-Luh-Samotij**). No implicit constant is used quantitatively.

---

## R0 — the target, and two structural facts (AUDIT / PROVED)

**What must be shown (the Step-B residual, #661/#657).** Convert
`vol(T_kappa) >= 2^{-eta b}/2` (Lemma 2) into: *all but `O(eta b)` of the `v_i`
lie in a proper GAP of rank `d(eta) = o(1/eta)` and size `2^{O(eta) b}`.* By #657
Theorem 3 this yields `lam_2 <= (d+2) eta + o(1) =: omega(eta) -> 0`, hence
`(ILO-moment)`, hence `rho* < log2` unconditional (#655). **Any `d(eta) = o(1/eta)`
closes it** — e.g. `d = 1/sqrt(eta)` gives `omega ~ sqrt(eta) -> 0`.

Two facts used throughout (verifier BLOCK 0):

- *Affine invariance / normalization.* `fstar, L1` are invariant under
  `v -> a v + c` (#643 Lemma A), but `det G` scales by `a^6` (verifier: exact).
  So we work with the **affine-normalized** block (`min V = 0`, `gcd = 1`)
  throughout; `det G`, diameter `D = max V`, and `T_kappa` are all read on the
  normalized block.
- *Cauchy-Binet.* `det G = sum_{i<j<k} [(v_j-v_i)(v_k-v_i)(v_k-v_j)]^2` (verifier:
  exact on every test block). Each summand is a squared nonzero integer, so
  `det G >= C(b,3) >= 1`: **the moment matrix is never degenerate** (there is no
  "small `det G`" horn from collinearity — three points on the moment curve are
  never collinear).

---

## R1 — V2 (large sieve / Weyl): the route is localized and its two shortcuts are dead

### 1.1 `T_kappa` forces a near-full quadratic Weyl sum (PROVED, BLOCK 2)

> **Lemma 1 (Weyl lower bound on `T_kappa`).** For every `theta in T_kappa`,
> ```
>     |S(theta_1, theta_2)| >= (1 - 2 pi^2 kappa) b .
> ```

*Proof.* `1 - cos(2 pi x) = 2 sin^2(pi x) <= 2 pi^2 ||x||^2` for all real `x`
(since `|sin(pi x)| = sin(pi ||x||) <= pi ||x||`; verifier BLOCK 2 checks the
pointwise inequality to `0`). Hence
`Re( e(-theta_0) S(theta_1,theta_2) ) = sum_i cos(2 pi psi_i)
>= b - 2 pi^2 sum_i ||psi_i||^2 >= b - 2 pi^2 kappa b`, and `|S| >= Re(e(-theta_0)S)`. ∎

With `kappa = (ln2/2)(eta + 1/b) = O(eta)` and `eta` small enough
(`eta < 1/(pi^2 ln2) ~ 0.146` suffices for a positive constant), `|S| >= (1 -
O(eta)) b`: a **near-maximal** Weyl sum. The verifier samples `T_kappa` for the
`b=12` interval at `kappa = 0.02` and finds `min |S|/((1-2pi^2 kappa) b) = 1.099
>= 1` over all sampled resonances.

**Projection.** The condition `|S| >= (1-2pi^2 kappa) b` involves only
`(theta_1, theta_2)`. Since for each `(theta_1,theta_2)` the set of `theta_0` with
`theta in T_kappa` has measure `<= 1`, the area of the projection satisfies
`area{ (t1,t2) : |S| >= (1-2pi^2 kappa) b } >= vol(T_kappa) >= 2^{-eta b}/2`
(BLOCK 2). So Step B is now: *a `2^{-eta b}`-area set of near-full quadratic Weyl
sums forces a GAP.* This is precisely the large-sieve / inverse-Weyl-sum shape of
V2.

### 1.2 The moment-curve additive energy is structure-blind (PROVED, BLOCK 1)

> **Theorem 2 (energy identity).** For **every** block `V` of size `b`,
> ```
>     INT_{[0,1)^2} |S(t1,t2)|^2 dt = b ,
>     INT_{[0,1)^2} |S(t1,t2)|^4 dt = 2 b^2 - b ,
> ```
> both **independent of the arithmetic of `V`**. More generally
> `INT |S|^{2m} = #{ ordered (i_1..i_m; j_1..j_m) : sum v_i = sum v_j and
> sum v_i^2 = sum v_j^2 }`, and the `m=2` value is universal.

*Proof.* `INT |S|^{2m}` counts `2m`-tuples with `sum_{a} v_{i_a} = sum_a v_{j_a}`
and `sum_a v_{i_a}^2 = sum_a v_{j_a}^2` (orthogonality of `e(...)` on `[0,1)^2`).
For `m=1`: only `i=j` (distinct `v`), giving `b`. For `m=2`: the two equations say
the multisets `{v_i, v_k}` and `{v_j, v_l}` share both power sums `p_1, p_2`; a
size-2 multiset is **determined** by `(p_1, p_2)` (its elements are the roots of
`x^2 - p_1 x + (p_1^2 - p_2)/2`), so `{v_i,v_k} = {v_j,v_l}`. Counting ordered
`(i,k,j,l)`: `b^2` choices of `(i,k)`, then `2` for `i != k` and `1` for `i = k`,
total `2b^2 - b`. **Only the distinctness of `V` is used** — the value is the same
for an interval, an AP, a random set, a dissociated set, or a PTE cluster
(verifier BLOCK 1 confirms all five give `2b^2 - b`). ∎

This is the **exact 2-dimensional Sidon/rigidity property of the moment curve**:
two points determined by two moments ⟹ no nontrivial 2-vs-2 additive
quadruples. The first moment that *sees* structure is `INT|S|^6` (degree-2 PTE
trades of support `<= 6`, hughes #564) — the verifier confirms it differs between
the interval (`1032`) and a dissociated set (`996`).

### 1.3 Consequence: the large-sieve / moment method is vacuous at constant `eta` (REFUTED as a closing route, BLOCK 3)

Combine 1.1 and 1.2. With `c_1 = 1 - 2pi^2 kappa` and `A >= 2^{-eta b}/2` the
large-values area, Markov on the fourth moment gives
```
    (1/2) 2^{-eta b} <= A <= INT|S|^4 / (c_1 b)^4 = (2b^2 - b)/(c_1 b)^4 < 2/(c_1^4 b^2) ,
```
hence `2^{-eta b} < 4/(c_1^4 b^2)`, i.e. `eta b >= 2 log2 b - O(1)`. **This is only
the poly-window corridor boundary** `eta ~ 2 log2(b)/b`, which *decreases to `0`*;
so for any **fixed constant `eta`** the inequality is automatically satisfied and
the `L^4` bound gives **no information** (verifier BLOCK 3: boundary
`0.16 -> 0.06 -> 0.017 -> 0.002` at `b = 50, 200, 10^3, 10^4`). A moment of order
`2m` only improves the boundary to `~ m log2(b)/b`; reaching constant `eta`
demands `m ~ eta b / log b -> infinity`, i.e. **exponential-order moments** — the
input the literature lacks. Because Theorem 2 makes `INT|S|^4` (and the whole
low-order moment ladder's leading behaviour) **structure-blind**, *no
energy-increment / Balog-Szemerédi-Gowers / large-sieve argument on the moment
curve can force structure*: the additive energy that such arguments amplify is
already pinned at its minimum `2b^2 - b`, independent of whether `V` is structured
or wild. **The large-sieve route provably cannot cross the corridor.** (This is
the Fourier-side analogue of #661 R2.2, where every *spectral* quantity was shown
blind to the fiber ceiling; here every *large-sieve/energy* quantity is blind to
`V`'s structure.)

### 1.4 Weyl's inequality is unavailable; the major-arc route is circular (REFUTED as a general route, BLOCK 4)

V2's most optimistic form hoped that "`|S(theta_1,theta_2)|` large forces
`theta_2` near a rational `a/q` (major arcs), and the total major-arc measure with
`q <= Q` is too small to hold `vol = 2^{-eta b}`." This uses **Weyl's inequality**,
whose printed hypothesis is that the sum runs over an **interval** `n in [1,N]` (the
proof differences the phase over the interval). An arbitrary block `{v_i}` has
**no such interval structure**; there is nothing to difference over, and Weyl's
inequality **does not apply**. Concretely, for an arbitrary set "`|S| ~ b`" is
*equivalent* to the Bohr condition `||t1 v_i + t2 v_i^2|| ~ 0` for most `i` — a
**tautology with no arithmetic content**, forcing no rationality of `theta_2`. The
verifier exhibits a **Diophantine** `theta_2 = (sqrt5-1)/2` for which the Bohr set
`{v in [0,4000] : ||theta_2 v^2 + theta_1 v|| <= 0.06}` **equidistributes**
(density `0.120 ~ 2w`, gaps ranging over `{1,2,3,4,5,6,...}` up to `65`): a large
trapped set that is **not** a bounded-rank GAP (BLOCK 4). So a single generic
frequency genuinely fails `Bohr -> GAP`, and the major-arc mechanism is available
**only** where `V` already lies in a short interval — exactly the regime #657
Theorem 1 settles outright (Fourier adds nothing there, as #661 R1.5 already
noted). **V2 does not close Step B.**

*(The discrete large sieve gives the same verdict: for `R`-separated frequencies
`sum |S|^2 <= (D^2 + R^{-2}) b`, whose "box term" `D^2` is the diameter dependence
already captured by R2.1 — no new traction.)*

---

## R2 — V1 (volume -> structure): the win-win dichotomy, its easy horn, and the exact gap in the hard horn

### 2.1 The det-G dichotomy, Horn A: small spread => structured (PROVED, BLOCK 5)

> **Proposition 3 (spread lower bound).** For a normalized block (`min=0`,
> `gcd=1`, `b >= 3`) with diameter `D = max V`, `det G >= D^2`, so
> `D <= sqrt(det G)`.

*Proof.* The Cauchy-Binet minor of the triple `{argmin, 2nd-smallest, argmax}` is
`v_{(2)} · D · (D - v_{(2)})` with `v_{(2)} >= 1` and `D - v_{(2)} >= 1`, hence
`>= D`; `det G` dominates its square. ∎ (Empirically `det G >~ D^4`; verifier
BLOCK 5 measures `det G / D^4 >= 1` across blocks.)

> **Corollary (Horn A).** If `det G <= 2^{2 eta b}` then `D <= 2^{eta b}`, so `V`
> lies in an interval of length `<= 2^{eta b}`, and #657 Theorem 1 gives
> `L1 <= (b+1)(bD+1)(bD^2+1) <= b^3 2^{eta b}·(1+o(1))`, i.e.
> `lam_2 <= 3 eta + o(1)`. **`(ILO-moment)` holds unconditionally on the class
> `det G <= 2^{2 eta b}`, with rank `d = 1`.**

This is the **easy horn**, and it disposes of exactly the low-spread blocks. The
verifier confirms the box bound on the `b=14` interval. Note this is a *spectral
threshold* form of #657 Theorem 1 (it re-expresses "small diameter" as "small
`det G`"), so it is coverage #657 already had — its value here is to **name the
residual**: everything not closed lies in the **large-`det G`** (spread) regime.

### 2.2 The branch decomposition and the per-branch Gaussian volume (PROVED, BLOCK 6)

Partition `T_kappa` by the nearest-integer vector `n(theta) = (round(psi_i))_i in
Z^b` (well-defined off a measure-zero set). On the branch of a fixed `n`,
`F(theta) := sum_i ||psi_i||^2 = sum_i (theta·u_i - n_i)^2` is a genuine quadratic
form in `theta in R^3` with **Hessian `2G`** and minimum
`F_min(n) = dist(n, W)^2`, `W = span_R(1, v, v^2) ⊆ R^b`. The branch cell
`{ n(theta)=n, F <= kappa b }` is contained in the ellipsoid
`{ (theta-theta_n^*)^T G (theta-theta_n^*) <= kappa b - F_min(n) }`, so

> **Proposition 4 (per-branch volume).**
> `vol(branch_n ∩ T_kappa) <= (4pi/3) (kappa b - F_min(n))_+^{3/2} / sqrt(det G)
> <= (4pi/3)(kappa b)^{3/2} / sqrt(det G)`.

Verifier BLOCK 6 confirms the largest single branch is within this cap for the
`b=6` interval and a two-cluster block. Summing over the `N_branch(kappa)`
realizable patterns,
```
    2^{-eta b}/2 <= vol(T_kappa) <= N_branch · (4pi/3)(kappa b)^{3/2}/sqrt(det G) .
```

### 2.3 The volume `!=` rank gap, quantified (PROVED threshold, BLOCK 6)

Rearranging Proposition 4's sum:
```
    N_branch(kappa) >= vol(T_kappa) · sqrt(det G) / [ (4pi/3)(kappa b)^{3/2} ]
                    >= 2^{-eta b} sqrt(det G) / [ (8pi/3)(kappa b)^{3/2} ] .
```
Resonance **multiplicity** (`N_branch >= 2`, the prerequisite for any joint-rank
argument) is therefore forced **only** when
```
    sqrt(det G) >= (16 pi/3)(kappa b)^{3/2} 2^{eta b} ,  i.e.
    log2 det G >= 2 eta b + 3 log2(kappa b) + O(1) .
```
So Lemma 2's volume `2^{-eta b}` — despite being *exponentially large as a lower
bound* — is **too small to force even two resonance branches** until `det G`
exceeds the Horn-A threshold `2^{2 eta b}` by a further `poly(b)` factor, and to
force *exponentially many* branches needs `det G >= 2^{(2 eta + c) b}` (verifier
BLOCK 6: at `b=100, eta=0.05`, forcing `N_branch >= 2` needs `log2 det G >= 12.4 >
2 eta b = 10`). **This is the precise arithmetic of the volume `!=` rank gap:** a
single deep resonance branch already accounts for a volume `~ kappa^{3/2}/poly`,
which dwarfs `2^{-eta b}` in the regime `eta -> 0, b -> infinity` where Lemma 2 is
supposed to bite. The census (R4) confirms that at every enumerable scale
`T_kappa` is *spread over many shallow branches* precisely because `eta ~ 1`
there — the loose regime — so the multiplicity that a Halász argument would need is
**not** delivered by the volume alone; it would have to come from `det G` being
extreme, i.e. from `V` being very spread. But a very spread block with a large
fiber is a **union of few far-apart APs** (e.g. the verifier's `two-AP far`
block), which #657 Theorem 2 already covers. The genuinely open residual — spread,
large fiber, *not* a union of few APs — is untouched by the volume bound.

### 2.4 The two-frequency elimination fails mod 1 (PROVED obstruction, BLOCK 7)

The natural way to manufacture rank from two resonances `theta^(1), theta^(2) in
T_kappa` is to **eliminate `v^2`**: the real combination
`theta_2^(2) Q_1(v) - theta_2^(1) Q_2(v)` (with `Q_j(v) = theta_1^(j) v +
theta_2^(j) v^2 + theta_0^(j)`) has **zero `v^2`-coefficient**, i.e. is *linear*
in `v` with slope `mu = theta_2^(2) theta_1^(1) - theta_2^(1) theta_1^(2)`. Over
`R` this is exact. **But it fails mod 1:** `||alpha x|| != |alpha| ||x||` for
non-integer `alpha`, so from `||Q_1(v_i)||, ||Q_2(v_i)|| <= w` one cannot conclude
`||mu v_i + c||` is small — the real-linear combination of two near-integers is a
real-linear combination of *integers*, generically far from `Z`. The verifier
takes two genuine near-resonances of the `b=10` interval and forms the eliminated
form: `max_i ||mu v_i + c|| = 0.45` (near the maximum `1/2`), **not** small (BLOCK
7). So two quadratic Bohr conditions do **not** combine into a linear Bohr
condition, and the "two generic quadratics pin `v`" heuristic (a *resultant* fact
over `R` or `F_p`) has **no mod-1 counterpart** at real frequencies. This is the
exact reason the *volume* of resonances resists conversion to *joint rank*: the
intersection of quadratic Bohr sets is again a positive-measure quadratic Bohr
set, not a rigid finite system, unless the frequencies are **commensurable**
(rational) — which is R3.

---

## R3 — the one horn that closes: rational resonance (PROVED, BLOCK 8)

> **Proposition 5 (rational-resonance horn).** Suppose the dominant resonance has
> `theta_2 = a/q`, `theta_1 = a'/q` with `q = O(1)`, and width `w < 1/(2q)`. Then
> each trapped `v` satisfies `a v^2 + a' v ≡ r_0 (mod q)` for a fixed residue
> `r_0`, a quadratic congruence with `<= 2^omega(q)` solutions `mod q` (`<= 2` per
> prime, CRT; a small `2`-power slack for even `q`). Hence the `(1-eps)b` trapped
> elements lie in `<= 2^omega(q)` residue classes `mod q` — a **rank-1 GAP** (union
> of `O(1)` APs of common difference `q`). Then #657 Theorem 2/3 gives
> `lam_2 = O(1) · o(1) -> 0`.

The verifier confirms the solution-count bound `<= 2^omega(q)` for
`q in {7, 11, 15, 12, 16}` (BLOCK 8). This is exactly the **CONDITIONAL** horn of
#661 R1.5: it closes when the resonance is rational of bounded denominator, and
the unconditional statement needs **Diophantine control of `theta_2`** — the same
missing input, now seen from the volume side. R2.4 shows *why* this rationality is
essential: only commensurable frequencies survive elimination mod 1.

---

## R4 — census: which horn is real? (MEASURED, BLOCK 9)

For the three families that are small enough to grid (interval `b=6`, a
champion-slice, and a `core + dissociated` block), the verifier tabulates
`det G`, `vol(T_kappa)`, the branch count, the biggest branch, `INT|S|^4`, and
`fstar/L1`. The reading (BLOCK 9):

- **Every enumerable case is in the loose regime `eta ~ 1`.** There
  `vol(T_kappa) ~ 0.1` is spread over hundreds of shallow branches (`120, 726,
  952`), and the biggest branch is `~0.001-0.005` — i.e. multiplicity is high but
  only because Lemma 2 is far from tight (as #661 BLOCK 9 also found). The regime
  `eta -> 0, b -> infinity` where the volume bound bites — and where R2.3 predicts
  a *single* branch dominates — is beyond exact enumeration.
- `INT|S|^4 = 2b^2 - b` holds on the nose (`66` at `b=6`, `630` at the `b=18`
  champion), reconfirming structure-blindness at scale.
- `det G` spans `3920` (interval) to `1.2·10^14` (`core+dissoc`), tracking the
  diameter as Proposition 3 predicts.

**Verdict of the data:** the census cannot distinguish the horns because at
enumerable scale both collapse into the same loose regime — consistent with #657's
finding that the `(phi_2, lam_2)` corner is empty (evidence `(ILO-moment)` is
TRUE) — and it confirms that the volume-to-rank conversion is *not* a finite-`b`
phenomenon one can read off; it is an asymptotic statement blocked by the
obstructions of R1.3, R2.3, R2.4.

---

## R5 — verdict and the wall, named precisely

```
    TARGET (#661 residual):  vol(T_kappa) >= 2^{-eta b}/2  =>  all but O(eta b) of
        v_i in a GAP of rank d(eta)=o(1/eta), size 2^{O(eta)b}.  (=> (ILO-moment).)

    V2 (large sieve / Weyl):  DOES NOT CLOSE.
      + T_kappa => |S(t1,t2)| >= (1-2pi^2 kappa)b on area >= 2^{-eta b}/2  (Lemma 1, PROVED)
      - INT|S|^4 = 2b^2-b for EVERY block (Theorem 2, PROVED): energy structure-BLIND
        => large-sieve/moment method VACUOUS at constant eta (only corridor)      (REFUTED route)
      - Weyl's inequality needs an INTERVAL; arbitrary set has none; "big Weyl sum"
        == Bohr condition (tautology); Diophantine theta2 traps a non-GAP set     (REFUTED route)

    V1 (volume -> structure):  ONLY THE EASY HORN CLOSES.
      + Horn A: detG <= 2^{2 eta b} => diam <= 2^{eta b} => #657 Thm1, lam2<=3eta  (PROVED, rank 1)
      - Horn B: per-branch Gaussian vol <= (4pi/3)(kappa b)^{3/2}/sqrt(detG)       (Prop 4, PROVED)
        => Lemma-2 volume forces multiplicity only if log2 detG >= 2 eta b + 3log2(kb):
        the volume != rank gap, quantified. Residual = large-detG (spread) blocks.
      - two-frequency elimination linear over R but FAILS mod 1                    (Prop, PROVED obstruction)

    HORN THAT CLOSES:  rational resonance theta2=a/q => v in <=2^omega(q) classes  (Prop 5, PROVED
        = #661 CONDITIONAL); unconditional needs Diophantine control of theta2 (unchanged).
```

**The wall, sharpened (this packet's contribution).** #661 localized Step B to
`Bohr -> GAP`; this packet proves that **three of the four natural bridges are
impossible**, leaving exactly one:

1. *Large-sieve / additive-energy bridge — IMPOSSIBLE.* The moment curve's energy
   `INT|S|^4 = 2b^2 - b` is structure-blind (Theorem 2), so the method sees no
   difference between a structured and a wild block and cannot cross the corridor
   `eta ~ log b/b`. (Fourier-side twin of #661's "no spectral quantity bounds the
   ceiling.")
2. *Major-arc / inverse-Weyl bridge — IMPOSSIBLE for general sets.* Weyl's
   inequality is out of scope (no interval); the near-full-Weyl-sum condition is
   the Bohr condition itself.
3. *Volume-multiplicity bridge — QUANTIFIED AND INSUFFICIENT.* Lemma 2's volume
   forces resonance multiplicity only in the extreme-spread regime
   `log2 det G >= 2 eta b + O(log b)`, so it cannot manufacture joint rank in the
   regime that matters; and the elimination that would has no mod-1 form.
4. *The surviving bridge — Diophantine / commensurability.* Only when the dominant
   resonance is rational (bounded `q`) does `Bohr -> GAP` go through (Proposition
   5). The unconditional statement is exactly a **Diophantine control of the
   resonance denominator** at exponential concentration — equivalently the
   per-instance exponential-regime inverse-LO named by #657 — now seen from the
   volume side and stripped of every shortcut.

Combined with #657 (downstream Freiman constants safe) and #661 (upstream spectral
shortcuts impossible), the three packets bracket the wall: **the only remaining
content of Step B is the passage from a positive *volume* of resonant frequencies
to the *commensurability* of the dominant one** — and that passage is now known to
be immune to energy, large-sieve, Weyl, and naive multiplicity arguments.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/bohr_gap_volume.md` (this).
- Verifier: `experimental/scripts/verify_bohr_gap_volume.py`
  (`RESULT: PASS (56/56)`, ~2 s / <60 MB; recomputes the energy identity, the
  Weyl lower bound on sampled `T_kappa`, the per-branch volume bound, the det-G
  dichotomy, the mod-1 elimination obstruction, and the rational-congruence horn;
  carries the `b=18` champion).
- Read-only inputs: our #661 `exp_ilo_fourier.md` (branch `thresholds-exp-ilo-fourier`),
  #657 `ilo_moment_structured.md`, #655 `fiber_image_tradeoff.md`, #646
  `moment_map_max_fiber.md`, #643 `pte_cluster_packing_frontier.md`; hughes #564
  `w_a_star_pte_lemma.md`.

**Per-claim status.** Lemma 1 (Weyl lower bound), Theorem 2 (energy identity),
Proposition 3 (spread bound) + Horn A corollary, Proposition 4 (per-branch
volume), the R2.3 multiplicity threshold, the R2.4 mod-1 obstruction, and
Proposition 5 (rational-resonance horn) = **PROVED**. The claims "large-sieve /
moment route cannot reach constant `eta`" and "Weyl / major-arc route unavailable
for general sets" = **REFUTED** (each with an exhibited obstruction — the
structure-blind energy, and the equidistributing Diophantine Bohr set). The census
trends = **MEASURED**. The unconditional `Bohr -> GAP` (Diophantine control of
`theta_2` at exponential concentration) = **OPEN** (unchanged from #661/#657).

**Flagged for PI (least-certain, 3 steps).**
(a) **The multiplicity threshold `log2 det G >= 2 eta b + O(log b)` is a *necessary*
condition for `N_branch >= 2`, read from an *upper* bound on each branch's volume
(Prop 4).** It correctly shows the volume cannot *force* multiplicity below the
threshold; it does not by itself prove that above the threshold the many branches
*are* independent enough to give joint rank (that would still need R2.4's
elimination, which fails at real frequencies). So R2.3 is a clean obstruction, not
a hidden closure — the honest reading is "volume is insufficient," not "spread is
sufficient."
(b) **Theorem 2 kills the low-order-moment / `L^4` large sieve, and I argue the
whole bounded-order ladder inherits the corridor cap.** The `INT|S|^6` structure
dependence (BLOCK 1) leaves a logical opening for a *sixth*-moment argument I have
not ruled out in full generality; I claim only that *bounded* moment order caps at
`eta ~ m log b/b`, which is the corridor for fixed `m`. A genuinely new idea using
`INT|S|^6` (the PTE-trade count) at growing order is not excluded — but that is the
exponential-regime inverse-LO itself.
(c) **The Weyl-unavailability argument is a scope statement, not a theorem that no
arithmetic can be extracted.** I prove Weyl's inequality does not apply and exhibit
a Diophantine counterexample to single-frequency `Bohr -> GAP`; I do not prove that
*no* Vinogradov-type input could ever help — only that the naive major-arc count
is circular for general sets. A future argument that first *reduces* to the
interval case (via the very structure Step B seeks) would re-open it.

**Exact vs heuristic.** All `fstar, L1, det G, INT|S|^{2m}`, the Cauchy-Binet and
congruence facts, and the mod-1 elimination example are exact integer / rational
computation. Lemma 1, Theorem 2, Propositions 3-5 are elementary closed-form
proofs. The Weyl lower bound is additionally certified on sampled `T_kappa`
frequencies; the per-branch volume bound is checked on enumerated sublevel sets
(midpoint grid; the inequality is analytic, the grid only confirms). The
exponential-regime `Bohr -> GAP` step is cited within its (open) scope and never
re-derived. No `.tex`/`.pdf` touched.
