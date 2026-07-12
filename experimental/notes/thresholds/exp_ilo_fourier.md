# Exp-ILO Step B via Fourier / eigenvalue methods: what the moment characteristic function decides

## Status

`R0 CORRECTED Step-B: #657's printed "o(b) exceptions" clause is REFUTED and
replaced by "O(eta b) exceptions" (explicit core+dissociated counterexample);
downstream omega(eta)=O((d+1)eta)->0 survives (PROVED) / R1 (F1, Esseen/Halasz):
the FOURIER ATOM BOUND fstar <= 2^b INT|Xhat| and its exponential form are PROVED
unconditional and affine-invariant; they recast exp-ILO as a SUBLEVEL-VOLUME
statement (PROVED) and yield QUADRATIC-BOHR TRAPPING of all but eps*b elements
(PROVED, tunable eps = the corrected exception scale); Bohr->GAP is the residual
OPEN half / R2 (F2, eigenvalue/det-G): the hoped det-G fiber UPPER bound
fstar <= C 2^b/sqrt(detG) is REFUTED (affine-invariance mismatch + the fstar>=1
floor); the exact Cauchy-Binet identity detG = sum(Vandermonde minors)^2 and the
affine-invariant KERNEL-SLICE reformulation fstar = max cube-points in a coset of
K=ker[1;v;v^2] are PROVED; det-G governs the fiber FLOOR (lower bound), not the
ceiling / R3 (F3): the clean dichotomy big-fiber => quadratic-Bohr-trapping is
PROVED (= R1 core) / R4 verifier PASS (52/52), 4.3 s / 53 MB / R5 VERDICT: the
Fourier route pins the wall precisely -- every spectral (spread-only) quantity is
provably blind to the fiber ceiling, so Step B genuinely needs additive
structure; the one missing step is Bohr-set -> GAP conversion on the eps*b
complement`.

This packet attacks the **(ILO-moment) / Step B** wall named by our PR #657
(`ilo_moment_structured.md`, Step B) and #655 (`fiber_image_tradeoff.md`, R5.1)
by a route orthogonal to #657's Freiman chain: the **moment characteristic
function**. In the notation of #655/#657/#646/#643: a **block** `V` is `b`
distinct integers; the degree-2 signature of `S ⊆ V` is
`Phi(S) = (|S|, sum_{x∈S} x, sum_{x∈S} x^2)`; `fstar(V)` is the max fiber,
`L1(V)` the image size, `phi_2 = (log2 fstar)/b`, `lam_2 = (log2 L1)/b`,
`eta = 1 - phi_2`. Write the moment-curve columns `u_i = (1, v_i, v_i^2) ∈ Z^3`
and the Rademacher/Boolean sum `X = sum_i eps_i u_i` (`eps_i` uniform in
`{0,1}`), so that

```
    fstar(V) = 2^b · max_s P(X = s) ,     P(X=s) = INT_{[0,1)^3} Xhat(theta) e^{-2pi i <theta,s>} dtheta ,
    Xhat(theta) = prod_i (1 + e^{2pi i <theta,u_i>})/2 = prod_i e^{i pi psi_i} cos(pi psi_i) ,
    psi_i(theta) = <theta,u_i> = theta_0 + theta_1 v_i + theta_2 v_i^2 ,
    |Xhat(theta)| = prod_i |cos(pi psi_i)| .
```

**One-line verdict.** The characteristic-function (Esseen) route gives an
**unconditional, affine-invariant fiber bound** `fstar <= 2^b INT|Xhat|` that
recasts Step B as a **sublevel-volume** problem and delivers **quadratic-Bohr
trapping** of all but a tunable `eps·b` fraction of `V` — exactly the shape of
the corrected Step-B conclusion — with the single residual gap being the
conversion *quadratic Bohr set -> GAP*. The eigenvalue/`det-G` route (F2) is
resolved in the **negative for the direction the program hoped**: the fiber
**upper** bound `fstar <= C 2^b/sqrt(detG)` is **REFUTED** (it is not
affine-invariant, while `fstar` is; and it violates the trivial `fstar >= 1`
floor), so *no purely spectral / spread-based quantity can bound the fiber
ceiling* — additive structure is unavoidable, which is precisely why Step B is
hard. What `det-G` *does* control (via `p* >= ||P||_2^2` and the local CLT) is
the fiber **floor**. Net: the Fourier attack does not close Step B, but it
**localizes the obstruction to one concrete analytic step (Bohr->GAP)** and
**proves the whole spectral family cannot substitute for it** — sharpening #657's
"the leak is the existence of Step B."

Every number is recomputed by
`experimental/scripts/verify_exp_ilo_fourier.py` (stdlib-only, zero-arg,
`RESULT: PASS (52/52)`, 4.3 s / 53 MB under `ulimit -v 2097152`; every inequality
re-checked on exact instances, every Fourier integral cross-checked for
grid-convergence, the `b=18` champion carried throughout).

Label key: **PROVED** (complete re-derivable proof, every external theorem quoted
with its exact hypotheses and used only in scope), **REFUTED** (explicit
counterexample), **COMPUTED** (exact enumeration), **MEASURED** (exact finite
objects, trend read off), **CONDITIONAL** (proved modulo a named cited-in-scope
input), **AUDIT** (cross-reference), **OPEN**.

**Credit.** Built directly on **our #657** (`ilo_moment_structured.md`: the Step
A/B/C chain, Theorem 3 GAP box bound, the exceptional-element lemma, the
reduction `omega=(d+2)eta`), **our #655** (`fiber_image_tradeoff.md`: the
`(ILO-moment)` name and reduction, the `b=18` champion `V =
{2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34}` with `fstar=30, L1=151275`),
**our #646** (`moment_map_max_fiber.md`: `phi*=log2`, the interval box bound, and
the measured `fstar(interval) = Theta(2^b/b^{9/2})` with `det G = b^9/2160` and
local-CLT covolume `2` — which this packet re-derives as the parity sublattice),
and **our #643** (`pte_cluster_packing_frontier.md`: `rho = phi+lam-log2`, affine
invariance Lemma A). The minimal degree-2 PTE trade support 6 is
**scottdhughes #564**. **The corrected Step-B exception scale `O(eta b)` (in
place of #657's printed `o(b)`) and the discipline of never importing a theorem
past its printed hypotheses are owed to the Codex team's read-only theorem-import
audit** — this packet incorporates that correction (R0) and marks #657's printed
Step-B superseded on that one clause. External inputs cited **only within printed
hypotheses, never re-derived**: **Esseen**'s concentration inequality and the
Fourier/`|Xhat|` inversion (classical); the **Halasz** method converting many
"resonant frequencies" to additive structure; inverse-Littlewood-Offord
(**Tao-Vu**; **Nguyen-Vu**, optimal) in the polynomial window; its
exponential-regime **counting** analogue (**Ferber-Jain-Luh-Samotij**); the
multidimensional lattice **local CLT** (**Bhattacharya-Rao**) for the `det-G`
floor constant; **Minkowski**'s second theorem for the kernel-slice remark. No
implicit constant is used quantitatively.

---

## R0 — the corrected Step B, and the Fourier reduction target (PROVED / AUDIT)

**#657's chain.** `fstar >= 2^{(1-eta)b}` --(A)--> linear concentration
`fstar_1 >= 2^{(1-eta)b}` --(B)--> `V` minus few elements in a bounded-rank GAP of
size `2^{O(eta)b+o(b)}` --(C=Thm 3)--> `lam_2 = O((d+2)eta)`. Steps A, C PROVED
in #657; **Step B is the wall**. This packet attacks Step B (equivalently the
full-signature version, which is only stronger) directly through `|Xhat|`.

**The exception scale is `O(eta b)`, not `o(b)` (Codex audit; PROVED, verifier
BLOCK 11).** #657's printed Step-B asks for *all but `o(b)`* elements in a GAP.
That is **false as stated**:

> **Counterexample (shape).** Let `A` be a structured core of size
> `|A| = (1-c·eta)b` (`c < 1`) with a near-maximal moment fiber
> `fstar(A) >= 2^{|A| - o(b)}` (e.g. an interval — #646). Adjoin
> `E = c·eta·b` **arbitrary, widely separated, dissociated** integers. The
> empty-`E` subsets already give
> `fstar(A ∪ E) >= fstar(A) >= 2^{(1-c·eta)b - o(b)} >= 2^{(1-eta)b}`,
> yet `E` is unstructured. So a block satisfying the hypothesis can have a
> genuinely `Theta(eta b)`-size set of elements lying in **no** low-rank GAP.

The verifier exhibits this exactly (core `A = {0..13}`, `fstar(A)=11`; adjoining
`|E| = 1,2,4` dissociated giants leaves `fstar(A∪E) = 11` unchanged, with
`eta·b >> |E|`). Hence:

> **(Step B, corrected).** There are `eta_0 > 0`, `d(eta)`, `c_1` with:
> `fstar_1(V) >= 2^{(1-eta)b}` (`eta < eta_0`) implies **all but `O(eta b)`**
> elements of `V` lie in a proper GAP of rank `d(eta)` and size
> `2^{c_1 eta b + o(b)}`.

**Downstream survives (PROVED, BLOCK 12).** With `|E| = O(eta b)` exceptions,
#657's exceptional-element lemma multiplies the image by at most `2^{|E|} =
2^{O(eta)b}`, so Theorem 3 on the core plus the multiplier give
`lam_2(V) <= (d+2)c_1 eta + O(eta) = O((d+1)eta) =: omega(eta) -> 0` whenever
`d(eta)` stays bounded (indeed `o(1/eta)`). **The correction changes only the
lemma statement, not the conclusion `rho* < log2`.** It also *helps the Fourier
attack*: an `O(eta b)` exception budget is exactly what
characteristic-function/Halasz arguments produce — they never pin down every
coordinate.

**Two structural facts used throughout (PROVED, BLOCK 0).**
- *Affine invariance.* `x -> a x + b` (`a != 0`) fixes `fstar, L1` (#643 Lemma
  A). Crucially it also fixes `INT|Xhat|` (R1.4) but multiplies `det G` by
  `a^6` (R2). Any valid fiber bound must be affine-invariant; `det G` is not.
- *Parity sublattice.* For every `S`, `sum x + sum x^2 = sum x(x+1) ≡ 0 (mod 2)`,
  so the image lattice sits in the index-2 sublattice `{(w,s,q): s+q even}`. This
  is a **block-independent** resonance (the frequency `theta=(0,1/2,1/2)`, where
  `psi_i = v_i(v_i+1)/2 ∈ Z` for *all* `v_i`); it is exactly #646's local-CLT
  covolume factor `2`, here derived, not measured.

---

## R1 — F1: the Esseen/Halász route (PROVED foundation; Bohr->GAP OPEN)

### 1.1 The cosine bound (PROVED, BLOCK 1)

> **Lemma 1.** For all real `t`, `|cos(pi t)| <= exp(-2 ||t||^2)`, where
> `||t||` is the distance from `t` to the nearest integer.

*Proof.* By evenness and period 1 reduce to `u = ||t|| ∈ [0, 1/2)`. Put
`h(u) = -log cos(pi u) - 2u^2`. Then `h(0)=0`, `h'(u) = pi tan(pi u) - 4u`,
`h'(0)=0`, and `h''(u) = pi^2 sec^2(pi u) - 4 >= pi^2 - 4 > 0`. So `h` is convex
with `h'(0)=0`, hence `h' >= 0` on `[0,1/2)`, hence `h` is nondecreasing from
`h(0)=0`, so `h >= 0`, i.e. `cos(pi u) <= exp(-2u^2)`. ∎

### 1.2 The Fourier atom bound (PROVED, unconditional, BLOCK 2/3)

> **Theorem A (atom bound).** For every block `V`,
> ```
>   fstar(V) <= 2^b · INT_{[0,1)^3} prod_i |cos(pi psi_i(theta))| dtheta
>            <= 2^b · INT_{[0,1)^3} exp(-2 sum_i ||psi_i(theta)||^2) dtheta .
> ```

*Proof.* `X` is `Z^3`-valued, so Fourier inversion on the torus gives
`P(X=s) = INT_{[0,1)^3} Xhat(theta) e^{-2pi i <theta,s>} dtheta`, whence
`max_s P(X=s) <= INT |Xhat| = INT prod_i |cos(pi psi_i)|` (triangle inequality;
`|Xhat| = prod|cos(pi psi_i)|` from the display in the header). Multiply by `2^b`.
The second inequality is Lemma 1 applied coordinatewise. ∎

This is the rigorous Esseen skeleton the task asks for: the concentration
`2^{-eta b}` is a **lower bound on an integral of `|Xhat|`**, and `|Xhat|` is
large only where many `psi_i` are near integers. The bound is **loose but
honest** — verifier BLOCK 2 finds `RHS/fstar ≈ 3.5` (interval/AP), `≈ 3.3` (GAP),
`≈ 5-7` (random/dissociated) at `b=8`, and confirms grid-convergence (the
inequality is analytic; the grid only certifies it numerically). Unlike every
box/`det-G` bound, **Theorem A is affine-invariant** (R1.4).

### 1.3 The sublevel-volume reduction (PROVED, BLOCK 9)

Let `T_kappa = { theta ∈ [0,1)^3 : sum_i ||psi_i(theta)||^2 <= kappa b }`.

> **Lemma 2 (sublevel volume).** If `fstar >= 2^{(1-eta)b}` then, taking
> `kappa = (ln2/2)(eta + 1/b)`,
> ```
>       vol(T_kappa) >= (1/2) · 2^{-eta b} .
> ```

*Proof.* By Theorem A, `2^{-eta b} <= fstar/2^b <= I := INT exp(-2 sum||psi||^2)`.
Split the torus at `T_kappa`: on `T_kappa` the integrand is `<= 1`; off it the
integrand is `< e^{-2 kappa b}`. Hence `I <= vol(T_kappa) + e^{-2 kappa b}`. The
choice of `kappa` gives `e^{-2 kappa b} = 2^{-eta b}/2`, so
`vol(T_kappa) >= I - 2^{-eta b}/2 >= 2^{-eta b}/2`. ∎

So a near-maximal fiber **forces a fat sublevel set of the quadratic phase
energy**. (BLOCK 9 confirms the inequality for the interval; at small `b` it is
loose — `eta` is near `1`, target `~2^{-b}`, and `T_kappa` fills the cube — but
the mechanism is exact.)

### 1.4 Affine invariance of the atom integral (PROVED, BLOCK 4)

> **Proposition 3.** `INT_{[0,1)^3} |Xhat_V(theta)| dtheta` is invariant under
> integer affine maps `V -> aV + c`.

*Proof.* Under `v -> a v + c`, `psi_i(theta) = theta_0 + theta_1(a v_i + c) +
theta_2 (a v_i + c)^2` is `<M^T theta, u_i>` for the integer lower-triangular
`M = [[1,0,0],[c,a,0],[c^2, 2ac, a^2]]`. The map `theta -> M^T theta (mod 1)` is a
**surjective endomorphism of the torus** (integer matrix, nonzero determinant
`a^3`), hence pushes Haar measure to Haar measure, so
`INT F(M^T theta) dtheta = INT F(theta) dtheta` for the periodic integrand
`F = |Xhat|`. ∎

Verifier BLOCK 4 confirms `atomI(id) = atomI(x2) = atomI(x3)` to `<5e-3` (the
`a=3` case needs a finer grid — `9x` frequency in `theta_2` — matching the proof),
while `det G` visibly changes (`56448 -> 2857680`). **This is the structural
reason the Fourier route sees the right invariant and the `det-G` route (R2) does
not.**

### 1.5 Quadratic-Bohr trapping (PROVED existence; the corrected-Step-B shape)

> **Theorem B (trapping).** If `fstar >= 2^{(1-eta)b}` then for every
> `eps ∈ (0,1]` there is a frequency `theta ∈ T_kappa` (`kappa` as in Lemma 2)
> such that **all but `eps·b`** of the elements `v_i` satisfy
> ```
>    || theta_1 v_i + theta_2 v_i^2 + theta_0 || <= sqrt(kappa/eps) ,
> ```
> i.e. all but `eps·b` of the `v_i` lie in one **quadratic Bohr set**
> `B(theta_1,theta_2; delta) = { v : ||theta_1 v + theta_2 v^2 + theta_0|| <= delta }`
> of width `delta = sqrt(kappa/eps) = O(sqrt(eta/eps))`.

*Proof.* Lemma 2 gives `vol(T_kappa) > 0`, so pick any `theta ∈ T_kappa`:
`sum_i ||psi_i(theta)||^2 <= kappa b`. By Markov,
`#{ i : ||psi_i||^2 > kappa/eps } <= eps b`; the complement satisfies
`||psi_i|| <= sqrt(kappa/eps)`. ∎ (BLOCK 10 verifies the Markov step on `4000`
sampled `theta ∈ T_kappa` for the champion, both `eps=0.25, 0.10`.)

**This is exactly the corrected Step-B shape.** Taking `eps = Theta(eta)`
(constant-times-`eta`) yields the `O(eta b)` exception budget of R0. The
trade-off is transparent: fewer exceptions widen the Bohr set. At the corrected
exception scale `eps = O(eta)` the width is
`sqrt(kappa/eps) = sqrt(O(1)) = O(1)`; at a constant-fraction budget `eps = O(1)`
the width shrinks to `O(sqrt(eta))`.

**What is proved vs. what is open.** Theorem B is the **honest, unconditional
half** of F1: heavy fiber ⟹ most `v_i` trapped in a single quadratic Bohr set.
The **missing half** is the classical, genuinely hard step:

> **(Bohr->GAP) OPEN.** Do many integers `v_i` in one quadratic Bohr set of
> width `delta` (for a positive-measure family of `(theta_1,theta_2)`, cf.
> Lemma 2's *volume* `2^{-eta b}`, not a single frequency) lie, up to `O(eta b)`
> exceptions, in a proper GAP of rank `O(1)` and size `2^{O(eta)b}`?

For a **single** frequency this can fail: if `theta_2` is Diophantine-generic the
Bohr set `{v: ||theta_2 v^2 + theta_1 v|| <= delta}` equidistributes with density
`~2 delta` over `[0,D]` and is *not* GAP-like unless `delta·D = O(1)` (small
diameter). The content is that Lemma 2 supplies a **volume** `2^{-eta b}` of
frequencies, an `L^2`/large-sieve input from which Halász's method extracts
structure — but making that quantitative at *exponential* concentration is
precisely the open exp-ILO estimate. Two honest partial reductions:

- *Rational-resonance case (CONDITIONAL/illustrative).* If the dominant
  resonance has `theta_2 = a/Q` with `Q = O(1)`, then `||psi_i|| <= delta <
  1/(2Q)` forces each trapped `v_i` into `O(Q)` residue classes mod `Q` — i.e.
  `(1-eps)b` of `V` lies in `O(Q)` arithmetic progressions, a rank-`O(Q)` GAP.
  This is the `d = O(1)` restricted conclusion *when the resonance is rational of
  bounded denominator*; the unconditional statement needs Diophantine control of
  `theta_2`, which is the open part.
- *Small-diameter case (PROVED, subsumed by #657).* If `diam(V) = O(1/delta)` the
  Bohr set is `O(1)` intervals outright — but bounded diameter is already #657
  Theorem 1. Fourier adds nothing new there; its value is the *general*-diameter
  reduction to (Bohr->GAP).

---

## R2 — F2: the eigenvalue / det-G route (upper bound REFUTED; the true role of det G)

### 2.1 The Gram determinant and its exact Cauchy-Binet form (PROVED, BLOCK 5)

Let `G = sum_i u_i u_i^T` be the `3x3` moment matrix
(`G_{jk} = sum_i v_i^{j+k}`, `j,k ∈ {0,1,2}`). Cauchy-Binet gives the exact,
verifier-checked identity

```
    det G = sum_{i<j<k} [ det(u_i,u_j,u_k) ]^2 = sum_{i<j<k} [ (v_j-v_i)(v_k-v_i)(v_k-v_j) ]^2 .   (CB)
```

So `det G` is a sum of squared Vandermonde `3x3` minors: it measures the
**spread** of `V`, dominated by well-separated triples. It scales as `a^6` under
`v -> a v` (invariant under shifts).

### 2.2 The hoped fiber UPPER bound is REFUTED (PROVED, BLOCK 6)

The task's F2 target is a standalone unconditional bound of the form
`fstar <= C · 2^b · poly(b) / sqrt(det G)` (a rigorous Gaussian-heuristic ceiling
sharper than #623's Lemma C). **This is false**, for two independent reasons:

1. **Affine-invariance mismatch.** `fstar(aV) = fstar(V)` (Lemma A) but
   `sqrt(det G(aV)) = a^3 sqrt(det G(V))`. Fix any `V` with `fstar >= 2` (e.g.
   the interval `{0..7}`, `fstar=2`) and let `a -> infinity`: the left side stays
   `2` while `C·2^b/sqrt(det G(aV)) -> 0`. The verifier shows the bound already
   failing at `a=1` (`fstar=2 > 2^8/sqrt(det G)=1.08`) and blowing past any `C`
   as `a: 1 -> 1000` (`RHS: 1.08 -> 1.08e-9`).
2. **The `fstar >= 1` floor.** A dissociated block (`{2^i}`, or any Sidon set)
   has `fstar = 1` but, by (CB), `det G` astronomically large
   (`~1.7e12` already at `b=8`), so `C·2^b/sqrt(det G) << 1 = fstar`.

**Conclusion (REFUTED).** No purely spectral / spread-based quantity can serve as
a fiber *upper* bound: `fstar` is affine-invariant and floored at `1`, `det G` is
neither. **This is a positive clarification of the wall:** it explains *why*
Step B cannot be closed by eigenvalue/`det-G` estimates alone and *must* invoke
additive structure — sharpening #657's diagnosis that "the leak is the *existence*
of structure, not its constants."

### 2.3 The true role of det G: the fiber FLOOR (PROVED identity + MEASURED bound)

The correct one-sided statement runs the *other* way. From
`p* = ||P||_infinity >= ||P||_2^2` (since `sum_s P_s = 1`):

> **Proposition 4 (L2 floor, PROVED, BLOCK 8).**
> ```
>    fstar/2^b = max_s P(X=s) >= sum_s P(X=s)^2 = INT_{[0,1)^3} prod_i cos^2(pi psi_i) dtheta = E2(V)/4^b ,
> ```
> where `E2(V) = sum_f n_f^2 = #{(S,S'): Phi(S)=Phi(S')}` is the exact moment
> **collision count** (Parseval on `Z^3`).

Local CLT (Bhattacharya-Rao, cited in scope, as in #646) evaluates the collision
integral: `INT prod cos^2(pi psi_i) ~ (const)/sqrt(det Sigma)` with
`Sigma = (1/4) G_c` the covariance, giving `fstar >~ c · 2^b / sqrt(det G)`. So
`det G` **lower-bounds** the fiber (spread ⟹ at least the Gaussian collisions),
the exact opposite of the hoped ceiling. Verifier BLOCK 7 measures the
affine-invariant-corrected ratio `fstar·sqrt(det G)/2^b`:

```
    min over 400 random blocks + all intervals b=4..18 :  0.559   (approached by tiny blocks)
    intervals b=6..18                                   :  0.98 .. 2.05   (near the CLT constant)
    b=18 champion                                       :  8.67
    dissociated {2^i}                                   :  >5000  (floor vacuous when det G huge)
```

so `fstar >= c · 2^b/sqrt(det G)` holds with `c ≈ 0.55` empirically (MEASURED; the
sharp constant is the CLT one of #646, cited not re-derived). The floor is
**minimized by dense blocks** (intervals) and **vacuous for spread blocks** — it
is exactly the baseline every block clears, never the ceiling.

### 2.4 The kernel-slice reformulation (PROVED, exact)

The doubling/eigenvalue framing has a clean exact form. The signature map
`pi: {0,1}^b -> Z^3`, `x -> (1^T x, v^T x, (v^2)^T x)` has fibers = cosets of the
rank-`(b-3)` integer lattice `K = ker[1; v; v^2] ⊆ Z^b`. Hence

> **Proposition 5.** `fstar(V) = max_{c ∈ Z^b} #( {0,1}^b ∩ (c + K) )` — the
> **maximum number of cube vertices in a single coset of `K`**. Moreover `K` is
> **affine-invariant** (row operations `v -> a v + b` do not change the kernel),
> so `covol(K)` is affine-invariant (consistent with `fstar`, and reconciling the
> `a^6` scaling of `det G` against the invariance of `fstar` via
> `covol(Lambda)·covol(K) = sqrt(det G)` with the image lattice
> `Lambda = pi(Z^b)` absorbing the `a^3`).

This is the honest content of the F2 "doubling" route: the fiber is an exact
cube-slice count of an affine-invariant lattice, and by Minkowski's second
theorem it is governed by the **successive minima** of `K` — but those minima
*encode the additive structure of `V`* (short vectors of `K` are exactly
low-support PTE trades, #643 Lemma B). So the reformulation is exact yet gives no
free bound: the successive minima **are** the missing structure. (Consistent with
R2.2: a spectral invariant `det G = covol` cannot see them; one needs the *shape*
of `K`, i.e. additive combinatorics.)

---

## R3 — F3: the dichotomy (PROVED)

The clean Fourier-mass dichotomy the task asks for is exactly the combination of
Lemma 2 and Theorem B, stated contrapositively:

> **Theorem C (dichotomy, PROVED).** For every `eta < eta_0` and `eps ∈ (0,1]`,
> **at least one** holds:
> - (spread) `fstar < 2^{(1-eta)b}` — the moment concentration is below
>   `2^{-eta b}`, i.e. the `L^1` Fourier mass `INT|Xhat| < 2^{-eta b}`; or
> - (structured) all but `eps·b` of the `v_i` lie in a common quadratic Bohr set
>   of width `sqrt(kappa/eps)`, `kappa = (ln2/2)(eta+1/b)`.

The structured branch is the corrected-Step-B premise on the `(1-eps)b` core;
Step B is closed iff that branch always upgrades to a GAP (the OPEN Bohr->GAP
step). The dichotomy itself is unconditional and needs no inverse-LO input — it
merely *localizes* where an exponential-regime inverse-LO must do its work. This
is the shippable F3 fragment: it turns "prove Step B" into "prove one quadratic
Bohr set with a volume of resonances is GAP-like off an `O(eta b)` set."

---

## R4 — verifier (COMPUTED)

`experimental/scripts/verify_exp_ilo_fourier.py` recomputes everything:
the champion + parity sublattice + affine (non)invariances (BLOCK 0); the cosine
bound on a fine grid + its convexity engine (BLOCK 1); Theorem A on five block
families with grid-convergence (BLOCK 2) and its exponential form (BLOCK 3);
affine invariance of the atom integral vs `det G` (BLOCK 4); Cauchy-Binet (BLOCK
5); the `det-G` upper-bound refutation, at `a=1` and under scaling (BLOCK 6); the
`det-G` lower-bound floor `fstar·sqrt(det G)/2^b >= 0.559` (BLOCK 7); the `L^2`
collision identity (BLOCK 8); the sublevel-volume lemma (BLOCK 9); the
quadratic-Bohr Markov step on sampled resonances (BLOCK 10); the corrected-Step-B
counterexample (BLOCK 11); the surviving reduction arithmetic (BLOCK 12).
`RESULT: PASS (52/52)`, 4.3 s / 53 MB.

---

## R5 — verdict and the honest wall

```
    (Step B, corrected -- Codex audit):  fstar_1 >= 2^{(1-eta)b}
        => all but O(eta b) elts of V in a rank-d(eta) GAP of size 2^{O(eta)b+o(b)}
        => (Thm3 + exceptional lemma, #657)  lam_2 <= omega(eta) = O((d+1)eta) -> 0
        => rho* < log2.        [ #657's printed "o(b)" clause SUPERSEDED. ]

    F1 (Esseen/Halasz):  PROVED, unconditional, affine-invariant --
        fstar <= 2^b INT|Xhat| = 2^b INT prod|cos pi psi_i|            (Theorem A)
        =>  vol(T_kappa) >= 2^{-eta b}/2, kappa=(ln2/2)(eta+1/b)        (Lemma 2)
        =>  all but eps*b of v_i in one quadratic Bohr set, width sqrt(kappa/eps)  (Theorem B)
        RESIDUAL: (Bohr -> GAP) on the (1-eps)b core -- the OPEN exp-ILO step.

    F2 (eigenvalue/det-G):  the hoped fiber UPPER bound fstar<=C 2^b/sqrt(detG)
        is REFUTED (affine-invariance mismatch + fstar>=1 floor). det G is the
        fiber FLOOR (fstar >= c 2^b/sqrt(detG), c~0.55 MEASURED; CLT-sharp cited),
        never the ceiling. Exact tools banked: Cauchy-Binet (CB), the L2 collision
        identity (Prop 4), the affine-invariant kernel-slice fstar = max cube-pts
        in a coset of K=ker[1;v;v^2] (Prop 5). NO spectral quantity bounds the
        ceiling: additive structure is unavoidable.

    F3 (dichotomy):  PROVED -- big fiber => quadratic-Bohr trapping, unconditional
        (Theorem C). Localizes the wall to (Bohr -> GAP).
```

**The wall, named precisely (this packet's contribution).** Step B reduces,
*unconditionally and via a route disjoint from #657's Freiman chain*, to a single
classical statement:

> *(Bohr->GAP at exponential concentration).* If `(1-eps)b` integers of a block
> lie in one quadratic Bohr set of width `O(sqrt(eta/eps))` — for a
> `2^{-eta b}`-measure family of frequencies `(theta_1,theta_2)` — then, off an
> `O(eta b)` exception set, they lie in a proper GAP of rank `O(1)` and size
> `2^{O(eta)b}`.

Two things are now proved that were not before: (i) the reduction is
**affine-invariant** and needs *no* import of any inverse-LO theorem (Theorems
A/B/C are self-contained), so it cannot be an out-of-scope-import artifact; and
(ii) the **entire spectral / `det-G` family is provably unable** to supply the
missing ceiling (R2.2), which pins the difficulty to the additive
(Bohr->GAP/Halász) content and *only* there. Combined with #657's Freiman chain
(which converts *energy* to GAP downstream), the two packets bracket the wall from
both sides: #657 shows the *downstream* Freiman constants are safe; this packet
shows the *upstream* spectral shortcuts are impossible and reduces the premise to
one Bohr-set structure step.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/exp_ilo_fourier.md` (this).
- Verifier: `experimental/scripts/verify_exp_ilo_fourier.py`
  (`RESULT: PASS (52/52)`, 4.3 s / 53 MB; recomputes every inequality and
  integral, carries the `b=18` champion throughout).
- Read-only inputs: our #657 `ilo_moment_structured.md`, #655
  `fiber_image_tradeoff.md`, #646 `moment_map_max_fiber.md`, #643
  `pte_cluster_packing_frontier.md`; hughes #564 `w_a_star_pte_lemma.md`.

**Per-claim status.** Lemma 1 (cosine bound), Theorem A (atom bound), Lemma 2
(sublevel volume), Proposition 3 (affine invariance of the integral), Theorem B
(trapping, existence), Proposition 4 (`L^2` floor identity), Cauchy-Binet (CB),
Proposition 5 (kernel-slice), Theorem C (dichotomy), the corrected-Step-B
counterexample, and the surviving reduction arithmetic = **PROVED**. The `det-G`
fiber upper bound = **REFUTED**. The `det-G` lower-bound constant `c ≈ 0.55` and
the CLT floor = **MEASURED** (sharp constant cited, not re-derived, from #646's
Bhattacharya-Rao local CLT). The rational-resonance restricted conclusion =
**CONDITIONAL** (needs Diophantine control of the resonance denominator).
(Bohr->GAP) at exponential concentration = **OPEN** (the residual exp-ILO step).

**Flagged for PI (least-certain, 3 steps).**
(a) **(Bohr->GAP) is the whole game and remains open.** Theorem B gives trapping
in *one* quadratic Bohr set for *one* frequency; the structural upgrade needs the
*volume* `2^{-eta b}` of resonances (Lemma 2) fed through a Halász/large-sieve
argument at exponential concentration — exactly the estimate the literature lacks
per-instance. We do **not** claim to bridge it; we prove the reduction *to* it is
clean and spectral-shortcut-free.
(b) **The `det-G` floor's sharp constant is CLT-imported.** `fstar >= c 2^b/sqrt
(det G)` is proved in the weak form via `p* >= ||P||_2^2` (Prop 4, exact) plus a
crude box; the sharp `c` (matching #646's `sqrt(2160)`-type constant) rests on the
multidimensional local CLT (Bhattacharya-Rao), cited in scope, not re-derived
here. The MEASURED `c ≈ 0.55` is a finite-`b` floor, approached by degenerate
small blocks.
(c) **Sublevel-volume sharpness is untested at large `b`.** Lemma 2 is exact but
BLOCK 9 verifies it only where it is loose (small `b`, `eta ≈ 1`); the regime
`eta -> 0, b -> infinity` where it bites is beyond exact enumeration (as always
here — the #646 poly-loss lesson that small-`b` plateaus can mislead applies).

**Exact vs heuristic.** All `fstar, L1, E2, det G`, and the Cauchy-Binet /
parity / counterexample facts are exact integer computation. Theorems A/B/C,
Lemmas 1/2, Propositions 3/4/5 are elementary closed-form proofs. The Fourier
integrals are midpoint quadrature used only to *confirm* analytic inequalities and
measure tightness (grid-convergence checked). The local CLT (`det-G` floor
constant) and the exponential-regime (Bohr->GAP) step are cited within their
printed scopes and never re-derived. No `.tex`/`.pdf` touched.
