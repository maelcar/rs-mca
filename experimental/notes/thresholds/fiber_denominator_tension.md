# The fiber-denominator tension, made a theorem where it lives: the 3-point Vandermonde resolution identity

## Status

`TARGET: convert #691's MEASURED tension (P5: high fiber concentrates the atom mass
INT|Xhat| at SMALL denominators of theta_2) into a THEOREM -- bound the atom mass
carried by frequencies whose dominant resonance denominator exceeds Q, and decide
whether "large fiber" and "large-denominator resonance" are quantitatively
incompatible on the fenced wall class / LEMMA V -- 3-POINT VANDERMONDE RESOLUTION
IDENTITY (PROVED, exact): for any triple T={a<b<c} of a block, (c-b)psi_a -
(c-a)psi_b + (b-a)psi_c = Vdm(T) theta_2 with Vdm(T)=(b-a)(c-b)(c-a); hence
||Vdm(T) theta_2|| <= (c-b)||psi_a||+(c-a)||psi_b||+(b-a)||psi_c|| <= diam(T)(sum
||psi||). A trapped triple pins theta_2 within diam*sum/Vdm of a rational of
denominator dividing Vdm(T) <= diam(T)^3 -- the EXACT arithmetic form of #691's T1
resolution ceiling / POINTWISE MASS BOUND (PROVED): |Xhat(theta)| <= exp(-(2/3)
||Vdm(T) theta_2||^2 / diam(T)^2) for every triple T -- but this SINGLE-triple bound
does NOT decay (its (t0,t1)-marginal P3_T is flat to 3%): the mass suppression is
irreducibly MULTI-point / AP-EMBEDDED DENOMINATOR BOUND (PROVED, the multi-point
resolution): if V contains an AP {a+jt: j<L}, then for ANY theta, (L-2)||2t^2
theta_2|| <= 4 sqrt(L) sqrt(sum_j ||psi_{a+jt}||^2); in a trap sum||psi||^2<=kappa b
this gives ||2t^2 theta_2|| <= 4 sqrt(L kappa b)/(L-2), so a positive-density
embedded AP forces the dominant resonance to the BOUNDED denominator 2t^2 with error
O(sqrt(eta)) -- the "interval to difference over" that #663 R1.4 said a general set
lacks, supplied by the block's own AP / REGIME MAP (PROVED, #668 envelope): the
AP-resolution bites only for eta <= 0.033 (phi >= 0.967), and there the #668 envelope
already gives phi+lambda <= 1.18 < 4/3 -- ENVELOPE-SAFE. The wall regime
(phi+lambda>4/3) needs eta in ~[0.08,0.6], where the trap width w~sqrt(eta) is too
large to pin any denominator. So the trapping/resolution tension is DISJOINT from the
wall / MASS LAW (MEASURED): the minor-arc (large-denominator) atom-mass fraction
decays monotonically to 0 by Q=30 for every census block; dominant resonances sit at
BOUNDED denominators (3, 4, 14, 25 = tied to embedded runs / the mod-7 GAP), never
exponential / #691 P5 CORRECTED (MEASURED): the small-denominator mass fraction is
NOT strictly monotone in f (gap20: f=57 lowest; sidon: f=1 not highest) -- it tracks
arithmetic STRUCTURE (embedded runs), not fiber magnitude / NO COUNTEREXAMPLE: the
AP-with-huge-difference "spread-resonance" block is closed by our gcd=1 normalization
(= #685's non-dilation): {g*j} normalizes to the interval, byte-identical (f,L,X) /
VERDICT: MIXED, clarifying. The tension's RESOLUTION half is now PROVED (Lemma V + the
AP bound pin the atom-mass denominators to trapped Vandermondes = 2t^2), its
MASS-magnitude half is shown irreducibly multi-point, and its whole mechanism
provably bites only where #668's envelope already certifies safety -- so the route is
mechanistically explained and precisely mapped, but does not by itself reach the
fenced wall. Grade (3), reaching (2) on the AP class; not (1); no (4).`

This packet answers the question our PR **#691**
(`fenced_resonance_window.md`) left as its single positive signal: its **P5**
*measured* that a high fiber concentrates the atom mass `INT|Xhat|` at **small
denominators** of `theta_2` (`mass(den<=5): .32 Sidon -> .55 champion`), calling
"large fiber" and "Diophantine resonance" quantitatively in tension. #691 proved the
bounded-denominator horn **vacuous** on the fenced class (its `T1` resolution ceiling
`Q_res <= 0.849 sqrt(b)`, `T2` host threshold `q_cross = 2^{beta b}`, `T3` empty
window) but left P5 as *measured, not proved*. We convert the **resolution** half of
that tension into an **exact identity** and decide the incompatibility question:
mostly *no on the fenced class* (the mechanism is real but provably confined to the
envelope-safe high-fiber regime), and along the way we correct P5's monotonicity
claim and close the one apparent counterexample.

Shared notation (`#661/#663/#682/#685/#691/#668`): a **block** `V` is `b` distinct
integers, normalized `min V = 0`, `gcd = 1`, diameter `D = max V`; the degree-2
signature is `Phi(S) = (|S|, sum_S x, sum_S x^2)`; `f` = max fiber, `L` = image size;
`phi = log2 f/b`, `lambda = log2 L/b`, `eta = 1-phi`, `delta = log2 D/b`,
`alpha = d/b` (`d` = dissociation dimension, **#668**), `X = 2^{phi+lambda} =
(fL)^{1/b}`. The moment-curve columns are `u_i = (1,v_i,v_i^2)`,
`X_vec = sum_i eps_i u_i` (`eps_i` uniform in `{0,1}`),
`psi_i(theta) = <theta,u_i> = theta_0 + theta_1 v_i + theta_2 v_i^2`. The **atom
identity** (#661 Thm A, re-derived R0) is `f = 2^b max_s P(X_vec=s)`,
`P(X_vec=s) = INT_{[0,1)^3} Xhat(theta) e^{-2pi i<theta,s>} dtheta`,
`Xhat(theta) = prod_i (1+e(psi_i))/2`, `|Xhat| = prod_i |cos(pi psi_i)|`, giving the
**atom bound** `f/2^b <= INT_{[0,1)^3}|Xhat| = INT M(theta_2) dtheta_2` where
`M(theta_2) := INT_{[0,1)^2}|Xhat| dtheta_0 dtheta_1` is the `theta_2`-marginal. The
**corridor bound** is `lambda <= alpha+1/3 <=> L <= 2^{d+b/3} <=> X <= 2^{4/3}`
inside `(alpha_0, 2/3)`, `alpha_0 = 0.084497`. The **fence** (#682 Cor 2): a wall
block has `delta > alpha/3 + 1/9`, `beta := delta - alpha/3 - 1/9 > 0`, and is **not
a dilation** (#685).

**One-line verdict.** **MIXED, clarifying.** The **resolution** half of #691's
tension is now a **theorem**: the exact **3-point Vandermonde identity** (Lemma V)
turns "a trapped triple `T`" into "`theta_2` within `diam(T)*sum||psi||/Vdm(T)` of a
rational of denominator dividing `Vdm(T) <= diam(T)^3`", and summed over an
**embedded AP** of difference `t` it forces the dominant resonance to the **bounded**
denominator `2t^2` with error `O(sqrt(eta))` -- the arithmetic form of #691's `T1`
ceiling and the exact mechanism behind P5's measured concentration. But three honest
findings **confine** it: (i) the **mass-magnitude** half is *irreducibly
multi-point* -- the single-triple mass bound `|Xhat| <= exp(-(2/3)||Vdm theta_2||^2/
diam^2)` is true but its marginal `P3_T` is **flat** (`< 3%` spread), so no
bounded-support object witnesses the suppression (a REFUTED sub-route, twin of #663's
structure-blind `INT|S|^4`); (ii) the whole trapping/resolution mechanism **bites
only for `eta <= 0.033`** (`phi >= 0.967`), and there the **#668 envelope** already
gives `phi+lambda <= 1.18 < 4/3` -- **off the wall**; the wall regime
(`phi+lambda > 4/3`, `eta ~ [0.08,0.6]`) has trap width `w ~ sqrt(eta)` too large to
pin any denominator; (iii) the natural **counterexample** (a high-fiber block with a
large-denominator, spread resonance -- an AP of huge common difference) is **closed
by our `gcd=1` normalization**: `{g*j}` normalizes to the interval,
*byte-identical* `(f,L,X)`, so it is `#685`'s excluded dilation, not a wall block.
Net: the tension is **mechanistically explained and precisely mapped**, its
resolution content proved, its magnitude content localized as multi-point, and its
domain shown disjoint from the fenced wall -- sharpening #691's "leaning negative"
with the exact arithmetic and cleanly deciding *why* the route does not close the
wall.

Every number is recomputed by
`experimental/scripts/verify_fiber_denominator_tension.py` (stdlib-only, zero-arg,
`RESULT: PASS (48/48)`, ~4 s / <60 MB under `ulimit -v 2097152`; the atom bound
re-checked on seven blocks, Lemma V's identity/inequality/relaxation and the
pointwise bound enumerated on `6*10^4` random `(theta,T)`, the AP-embedded bound on
`2*10^5` random `theta`, the single-triple flatness quadratured, the minor-arc mass
law tabulated across the census, the P5 non-monotonicity exhibited, the regime map
recomputed against the envelope, and the dilation closure checked byte-for-byte with
a Sidon negative control).

Label key: **PROVED** (complete re-derivable proof, every external theorem quoted
within its printed hypotheses and used only in scope), **COMPUTED** (exact
enumeration), **MEASURED** (exact finite objects, trend read off; `|Xhat|` by
midpoint quadrature used only to read concentration), **REFUTED** (a route proved
unable to do what was hoped, obstruction exhibited), **AUDIT** (cross-reference),
**OPEN**.

**Credit.** The fiber bound `f <= 2^{b-d}` and `fL <= 3^b` are **DannyExperiments
#668** (`canonical_transversal_vc_compression.md`) -- the envelope this whole
regime-map rests on. The **atom bound** `f <= 2^b INT|Xhat|` (Thm A), the cosine
bound `|cos pi t| <= exp(-2||t||^2)` (Lemma 1), the sublevel volume and
single-frequency quadratic-Bohr **trapping** at width `w = sqrt(kappa/eps)`,
`kappa=(ln2/2)(eta+1/b)` (Thm B), are **our #661** (`exp_ilo_fourier.md`). The
**resonance/denominator wall**, the rational-resonance horn (`theta_2 = a/q =>
<= 2^omega(q)` residue classes, R3), the golden-Diophantine equidistributing set that
a *general* block lacks an interval to difference over (R1.4), and the structure-blind
`INT|S|^4 = 2b^2-b` are **our #663** (`bohr_gap_volume.md`). The `(alpha,delta)`
diameter map, `alpha_0`, the residual line `delta=(alpha+1/3)/3`, and Cor 2's
inflation `delta > alpha/3+1/9` are **our #682** (`corridor_diameter_map.md`). The
**dilation invariance** `f(sV)=f(V)` and the non-dilation fence are **our #685**
(`corridor_interior_hunt.md`), a special case of **#643**'s affine invariance Lemma A
(`pte_cluster_packing_frontier.md`). The **T1/T2/T3 window emptiness** and the **P5
tension we here formalize and correct** are **our #691** (`fenced_resonance_window.md`).
The `b=18` champion `V={2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34}`
(`f=30, L=151275`) and the moment-curve reduction are **our #655**
(`fiber_image_tradeoff.md`); the tensor-averaging census is **#683**
(`championship_census_b19_26.md`); the `b=18` champion diameter map and residual line
are **#682/#678** (`curve_restricted_product.md`). The minimal degree-2 PTE trade
support `6` is **scottdhughes #564** (`w_a_star_pte_lemma.md`). External inputs cited
**only within printed hypotheses, never re-derived**: the classical **divided-difference /
Newton** identity behind Lemma V; **three-distance / continued fractions** (for the
denominator reading); **Weyl / van der Corput** for AP exponential sums (invoked only
as the *shape* the AP bound realizes elementarily); inverse-Littlewood-Offord
(**Tao-Vu; Nguyen-Vu**) and its exponential-regime analogue
(**Ferber-Jain-Luh-Samotij**) named as the open magnitude object. **Lane discipline:**
this packet stays entirely on the **image face** (`f, L, Phi, theta`); it does **not**
enter hughes's signed `(LS)/(SV*)/mu_n` object (#564). Where the *magnitude* inverse
question ("why is the atom mass at a given denominator large") would need signed
cancellation, we record it as **transfer, not entry** (R3, R6).

---

## R0 -- the target, and the atom identity re-derived (AUDIT / PROVED)

**#691's P5, verbatim.** #691 proved the bounded-denominator horn empty on the fence
(`T1`: a width-`w` trap resolves only `q <= Q_res = 1/(2w) <= 0.849 sqrt(b)`, poly;
`T2`: a corridor-closing residue host needs `q >= q_cross = 2^{beta b}`, exp; `T3`:
`[q_cross, Q_res]` empty), and *measured* (P5) that high fiber puts `INT|Xhat|` at
small denominators, offering it as evidence the fenced wall class may be empty. It
flagged P5 as **measured, not proved** (its PI note (b)). **This packet proves the
resolution content of P5 and decides the incompatibility.**

**The atom identity (re-derived, PROVED, verifier BLOCK 0/5).** `X_vec = sum_i eps_i
u_i` is `Z^3`-valued, so Fourier inversion on the torus gives `P(X_vec=s) =
INT_{[0,1)^3} Xhat(theta) e^{-2pi i<theta,s>} dtheta` with `Xhat(theta) =
E[e(<theta,X_vec>)] = prod_i (1+e(psi_i))/2`, hence `|Xhat| = prod_i|cos(pi psi_i)|`
and `f/2^b = max_s P(X_vec=s) <= INT|Xhat|` (triangle inequality). The verifier
confirms `f/2^b <= INT|Xhat|` on all seven census blocks (ratios `2.2`-`24`, BLOCK 5).
We write the **`theta_2`-marginal** `M(theta_2) = INT_{[0,1)^2}|Xhat| dtheta_0
dtheta_1`, so `f/2^b <= INT_0^1 M(theta_2) dtheta_2`; the "denominator of the
dominant resonance" is the denominator of the `theta_2` at which `M` concentrates.

**Normalization closes the dilation loophole (COMPUTED, BLOCK 0).** The obvious
counterexample to any "high fiber => small denominator" claim is an **AP of huge
common difference**: `W = {g*j : j<b}` has `f(W)=f(interval)` (large) yet its
resonance sits at `theta_2 ~ a/(2g^2)`, a *large* denominator. But `W` is a dilation:
`gcd(W)=g`, and our standard normalization divides it out, returning the interval
*byte-identically* (`f,L,X` bit-for-bit; verifier checks `g in {5,16,97}`). A
**normalized `gcd=1` block is never a nontrivial dilation** -- which is *exactly*
#685's "not a dilation" fence condition. So the loophole is closed by normalization,
there is **no counterexample of this shape**, and the tension is a statement about
`gcd=1` blocks throughout (as it must be, matching the fence).

---

## R1 -- Lemma V: the exact 3-point Vandermonde resolution identity (PROVED, BLOCK 1)

The mechanism that pins `theta_2` is a Newton divided-difference on the moment curve,
isolating the `v^2` coordinate.

> **Lemma V (Vandermonde resolution identity).** For any triple `T = {a<b<c}` of a
> block and any `theta`, writing `Vdm(T) = (b-a)(c-b)(c-a) > 0`,
> ```
>     (c-b) psi_a - (c-a) psi_b + (b-a) psi_c  =  Vdm(T) * theta_2        (exact)
> ```
> and therefore, with `||.||` = distance to the nearest integer,
> ```
>     || Vdm(T) theta_2 ||  <=  (c-b)||psi_a|| + (c-a)||psi_b|| + (b-a)||psi_c||
>                           <=  diam(T) * ( ||psi_a|| + ||psi_b|| + ||psi_c|| ),
>     diam(T) = c-a.
> ```

*Proof.* The coefficients `(c-b, -(c-a), b-a)` annihilate `(1,1,1)` and `(a,b,c)`
(a size-2 divided difference kills constants and linears) and pair the `v^2`-row to
`(c-b)a^2 - (c-a)b^2 + (b-a)c^2 = (b-a)(c-b)(c-a) = Vdm(T)`; so the combination equals
`Vdm(T) theta_2` identically in `(theta_0,theta_1,theta_2)`. Taking `||.||`,
`||Vdm(T)theta_2|| = ||(c-b)psi_a-(c-a)psi_b+(b-a)psi_c||`, and `||m x|| <= |m|·||x||`
for integer `m` with the triangle inequality gives the weighted bound; each weight is
`<= c-a`. ∎ (Verifier BLOCK 1: over `6*10^4` random `(theta,T)`, signed-identity error
`1.8e-11` = float roundoff; weighted inequality violation `1.2e-13`; diameter
relaxation violation `0`.)

> **Corollary V.1 (resolution = Vandermonde, PROVED).** If a triple `T` is
> `w`-trapped (`||psi_a||,||psi_b||,||psi_c|| <= w`) and `3 diam(T) w < 1/2`, then
> `theta_2` lies within `3 diam(T) w / Vdm(T)` of the rational `round(Vdm(T)theta_2)/
> Vdm(T)`, of denominator dividing `Vdm(T) <= diam(T)^3`.

This is the **exact arithmetic form of #691's `T1`**: #691 proved the *metric*
ceiling `q <= 0.849 sqrt(b)`; Lemma V says the resolvable denominator *divides the
Vandermonde of a trapped triple*, and is `<= diam(T)^3`. The two agree in force -- a
short-diameter trapped triple resolves only a *bounded* denominator -- but Lemma V is
an **identity**, exact and structural, and it is the object that scales to many points.

**Pointwise mass bound, and why one triple is not enough (PROVED + REFUTED-route,
BLOCK 1/3).** Feeding Lemma V into the cosine bound (`|cos pi t| <= exp(-2||t||^2)`)
and the power-mean `sum||psi||^2 >= (sum||psi||)^2/3`:
```
    |Xhat(theta)|  <=  |cos pi psi_a · cos pi psi_b · cos pi psi_c|
                   <=  exp(-2 (||psi_a||^2+||psi_b||^2+||psi_c||^2))
                   <=  exp( -(2/3) ||Vdm(T) theta_2||^2 / diam(T)^2 ).     (pointwise)
```
Verified pointwise (BLOCK 1, violation `0`). **But it does not decay usefully:**
`||Vdm(T)theta_2|| <= 1/2` while `diam(T) >= 2`, so the exponent is `<= (1/6)/4`, a
factor `~0.96`. Concretely the `(theta_0,theta_1)`-marginal `P3_T(theta_2) =
INT|cos pi psi_a cos pi psi_b cos pi psi_c|` is **flat** -- over the whole `theta_2`
circle its relative spread is `2.97%` (verifier BLOCK 3), even though the true
`M(theta_2)` swings by `>10x`. **A single triple (indeed any bounded-support
sub-product) cannot witness the mass suppression:** the decay is *irreducibly
multi-point*. This is the Fourier-marginal twin of #663's `INT|S|^4 = 2b^2-b`
structure-blindness -- the tension's *magnitude* lives above every fixed-order object.

---

## R2 -- the AP-embedded denominator bound: the multi-point resolution (PROVED, BLOCK 2)

The decay a single triple lacks is recovered by summing Lemma V's `t=` second
difference along an **embedded arithmetic progression** -- the "interval to difference
over" that #663 R1.4 correctly said an *arbitrary* set lacks, here supplied by the
block's own AP.

> **Theorem AP (embedded-AP denominator bound).** Suppose `V` contains an AP
> `{a + j t : 0 <= j < L}` (`t >= 1`). Then for **every** `theta`,
> ```
>     (L-2) || 2 t^2 theta_2 ||  <=  4 sqrt(L) · sqrt( sum_{j=0}^{L-1} ||psi_{a+jt}||^2 ).
> ```
> Consequently, in a trap `sum_{i in V} ||psi_i||^2 <= kappa b`
> (`kappa = (ln2/2)(eta+1/b)`, #661 Lemma 2),
> ```
>     || 2 t^2 theta_2 ||  <=  4 sqrt(L kappa b) / (L-2).
> ```
> For a **positive-density** AP (`L = c b`), `||2t^2 theta_2|| <= 4 sqrt(kappa/c)·
> (1+o(1)) = O(sqrt(eta))`: the dominant resonance is pinned within `O(sqrt(eta))` of
> the **bounded** denominator `2t^2`.

*Proof.* The second difference of the AP is constant: `psi_{a+jt} - 2 psi_{a+(j+1)t}
+ psi_{a+(j+2)t} = 2 t^2 theta_2` (Lemma V with the equally spaced triple `{a+jt,
a+(j+1)t, a+(j+2)t}`, whose `Vdm = t·t·2t = 2t^3` and `diam=2t`, giving the sharper
`2t^2` after cancellation). Hence each of the `L-2` consecutive triples yields
`||2t^2 theta_2|| <= ||psi_{a+jt}|| + 2||psi_{a+(j+1)t}|| + ||psi_{a+(j+2)t}||`. Sum
over `j=0..L-3`: the left side is `(L-2)||2t^2 theta_2||`; on the right each
`||psi_{a+jt}||` carries total weight `<= 4`, so the sum is `<= 4 sum_{j<L}
||psi_{a+jt}||`, and Cauchy-Schwarz gives `<= 4 sqrt(L) sqrt(sum_j ||psi_{a+jt}||^2)
<= 4 sqrt(L) sqrt(sum_{i in V}||psi_i||^2)`. In a trap the last radicand is
`<= kappa b`. ∎ (Verifier BLOCK 2: worst ratio `lhs/rhs` over `2*10^5` random `theta`
is `0.74`-`0.79 < 1` for `AP(t=1,2,3)`, several `a,L`; the in-trap closeness table
gives `||2t^2 theta_2|| <= 0.42` at `eta=0.02`, `0.56` at `eta=0.045`.)

So **any block with a positive-density embedded AP of common difference `t`** has its
dominant resonance provably at the **bounded** denominator `2t^2`. Intervals
(`t=1 => q=2`, the parity), intervals-with-holes with a surviving run, and unions of
bounded-`t` APs (the census structured classes) all qualify. This is the promised
formalization of "seeing = arithmetic value": the trap does not merely *fail to
resolve* large denominators (a metric ceiling), it *positively pins* `theta_2` to the
small denominator `2t^2` set by the AP's difference -- the exact mechanism producing
#691 P5's measured small-denominator concentration.

**Negative control (BLOCK 2).** For a **Sidon** set (no genuine common difference) the
same `t=1` template is arithmetically vacuous: `M(1/2)` (the would-be parity peak) and
`M` at a generic point agree to within `6%` (measured `0.00368` vs `0.00346`) -- no
structured resonance, consistent with `f=1` (nothing to concentrate).

---

## R3 -- the incompatibility, decided: the mechanism is off the wall (PROVED envelope, BLOCK 6)

Does Theorem AP make the fenced profile impossible? **On the fenced wall class, no --
and we can say exactly why.** The AP bound pins `theta_2` to `2t^2` only while it is
non-vacuous, `||2t^2 theta_2|| < 1/2`, i.e. (verifier BLOCK 2/6, from the **proven**
trap bound `4 sqrt(b kappa b)/(b-2)`, `L=b=100`) `eta <= 0.033` (`phi >= 0.967`). But:

> **Proposition R3 (disjoint regimes, PROVED via #668).** For `eta <= 0.033` the
> #668 envelope `lambda <= H_2(min(alpha,1/2))`, `phi <= 1-alpha` gives
> `phi + lambda <= (1-eta) + H_2(eta) <= 1.177 < 4/3` -- the block is **certified
> `X < 2^{4/3}` (off the wall)** before any resonance analysis. The wall regime
> `phi + lambda > 4/3` occupies `eta ~ [0.08, 0.6]`, where the trap width
> `w = sqrt(kappa/eps) = Theta(sqrt(eta))` is too large for Corollary V.1
> (`3 diam(T) w < 1/2` fails for any `diam(T) >= 2`). The two regimes are **disjoint**.

Verifier BLOCK 6 tabulates it: `eta = 0.033 -> phi+lambda = 1.18 < 4/3` (AP bound
`0.498`, bites); `eta = 0.10 -> 1.37 > 4/3` (AP bound `0.80`, vacuous). The check
`bite AND wall` is empty. The **champion** sits at `eta = 0.727`, `phi+lambda = 1.23`
-- far outside the biting regime, and its trap is vacuous (as #661 BLOCK 9 / #663 R4
already found the enumerable regime to be).

**Reading.** The fiber-denominator tension is **real and now proved where it lives**
-- the high-fiber (`eta -> 0`) regime, where Lemma V + Theorem AP pin the resonance to
`2t^2`. But that regime is *exactly* the one #668's envelope already certifies safe;
the actual wall lives at *moderate* `eta`, where the trap is too wide for the
resolution mechanism to bite at all. So the tension route, pursued through trapping,
**cannot reach the fenced wall by itself** -- not because the tension is false, but
because its lever (a narrow trap) is unavailable in the wall's regime. This is the
precise sense in which #691's "leaning negative" is correct, now with the mechanism
and the regime boundary made explicit rather than measured.

**What a wall block must therefore look like (transfer, not entry).** To carry a
fiber at moderate `eta` *without* an embedded positive-density AP (which would pin it,
by Theorem AP, to a bounded denominator and place it in #663 R3's closable horn), a
wall block must be **AP-free at every bounded difference while still additively rich**
-- i.e. its fiber must come from PTE trades that create *no* long progression. Whether
such a block exists is the residual, and it is the signed-`mu_n` inverse question
(#564) we do not enter: a PTE trade `{a1,a2,a3}={b1,b2,b3}` is a `±1` relation among
the `u_i` that kills all three moments jointly and so, unlike Lemma V's triple, does
**not** isolate `theta_2` -- the magnitude inverse-LO, transferred here to "additive
richness without an AP."

---

## R4 -- the mass law, measured: minor-arc mass -> 0 at bounded Q (MEASURED, BLOCK 4)

Independently of the trap, we measure where the atom mass actually sits. For each
census block we grid `M(theta_2)` (`420` points, `14x14` inner quadrature) and bin the
mass by whether `theta_2` is within `0.02` of some `a/q`, `q <= Q` (a **major arc**)
or not (a **minor arc**, "large denominator"):

```
  block         f    total     minor-arc (large-denominator) mass fraction
                               Q=2     Q=5     Q=8    Q=16    Q=30
  sidon12       1  0.00446   0.919   0.612   0.279   0.049   0.000
  interval12    5  0.00470   0.867   0.534   0.219   0.029   0.000
  interval14   11  0.00200   0.840   0.505   0.201   0.024   0.000
  holes14       5  0.00189   0.900   0.581   0.249   0.035   0.000
  unionAP18     7  0.00031   0.885   0.574   0.238   0.036   0.000
  gap20        57  0.00029   0.808   0.558   0.207   0.024   0.000
  champ18      30  0.00032   0.864   0.519   0.212   0.036   0.000
```

The minor-arc fraction is **monotone decreasing in `Q`** and hits `0` by `Q = 30` for
**every** block (verifier BLOCK 4). So *all* the atom mass -- hence, via the atom
bound, all the fiber it certifies -- sits on **bounded-denominator (`<= 30`) major
arcs** at these scales; the large-denominator mass is empirically **zero**. The
verifier also reports each block's dominant **non-trivial** resonance (the `argmax`
of `M` away from the parity `{0,1/2}`): the intervals and `holes14` peak at `q=4`
(`theta_2 ~ 1/4, 3/4`), `unionAP18` at `q=3`, the rank-2 GAP `gap20` (`{a+7c}`) at
`q=14` (`= 7 x 2`, its modulus times parity), and the champion at `q=25` -- **all
bounded (`<= 30`)**, never exponential (Sidon, `f=1`, has no genuine peak: its
`M*/peak = 1.00` is flat noise). This is exactly what Lemma V / Theorem AP predict:
the resonance denominators are the Vandermondes / progression-differences of the
block's own runs, hence bounded by its diameter -- never the `2^{beta b}` a fenced
host would need (#691 T2).

---

## R5 -- #691's P5, corrected: concentration tracks structure, not fiber (MEASURED, BLOCK 5)

#691 P5 read the small-denominator mass as **monotone in `f`** (`.32 -> .55`). With a
proper marginal (not the coarse `30x30x6` cube of #691) the monotonicity **fails**:
ordering the seven blocks by `f`, the `den<=5` mass fraction is
```
    f:     1     5     5     7    11    30    57
    frac: .388  .419  .466  .426  .495  .481  .442      (verifier BLOCK 5)
```
non-monotone (`gap20`, the **largest** fiber `f=57`, has among the **lowest**
concentration `.442`; `sidon`, `f=1`, is not the lowest). The concentration instead
tracks **arithmetic structure**: dense embedded runs (intervals, `t=1`) concentrate
most; a spread rank-2 GAP concentrates less despite a large fiber. This corrects P5's
causal reading -- it is the **embedded-AP structure** (Theorem AP), not the fiber
*magnitude*, that puts mass at small denominators. (The two correlate across #691's
particular `Sidon -> champion` slice because there structure and fiber rise together;
the correlation is not the mechanism, and breaks on `gap20`.)

---

## R6 -- verdict, and the tension named precisely

```
  TARGET (#691 P5): prove "high fiber => atom mass at small denominators", decide
      whether large fiber and large-denominator resonance are incompatible on the fence.

  LEMMA V (PROVED, exact): (c-b)psi_a-(c-a)psi_b+(b-a)psi_c = Vdm(T) theta_2;
      ||Vdm(T)theta_2|| <= diam(T)(sum||psi||). Trapped triple => theta_2 near a rational
      of denominator | Vdm(T) <= diam^3. Exact arithmetic form of #691 T1.

  POINTWISE MASS BOUND (PROVED, but WEAK):  |Xhat| <= exp(-(2/3)||Vdm theta_2||^2/diam^2);
      single-triple marginal P3_T is FLAT (<3%) => suppression is irreducibly MULTI-point.  (REFUTED sub-route)

  THEOREM AP (PROVED, multi-point):  V >= AP{a+jt}(len L) => (L-2)||2t^2 theta_2||
      <= 4 sqrt(L) sqrt(sum||psi||^2);  positive-density AP => dominant resonance at the
      BOUNDED denominator 2t^2, error O(sqrt(eta)). The interval #663 R1.4 said was missing.

  REGIME MAP (PROVED via #668):  AP-resolution bites only eta<=0.033 (phi>=0.967), where
      #668 envelope gives phi+lambda<=1.18<4/3 (OFF the wall). Wall regime eta~[.08,.6] has
      trap width ~sqrt(eta) too large to pin any denominator. BITE and WALL are DISJOINT.

  MASS LAW (MEASURED):  minor-arc (large-q) mass fraction -> 0 by Q=30 on all 7 blocks;
      dominant resonances bounded (q=3,4,14,25 = runs/moduli), never exponential.
  P5 CORRECTED (MEASURED):  small-den mass NOT monotone in f (gap20 f=57 lowest); it tracks
      embedded-run STRUCTURE, not fiber magnitude.
  NO COUNTEREXAMPLE:  AP{g*j} of huge difference -> normalize -> interval (gcd=1 == #685
      non-dilation), byte-identical (f,L,X). The spread-resonance block does not exist as
      a normalized block.
```

**The tension, sharpened (this packet's contribution).** #691 *measured* that a high
fiber concentrates the atom mass at small denominators and left it as its one positive
signal. We prove the **resolution** content of that signal exactly (Lemma V), give the
genuine **multi-point** version that produces the concentration (Theorem AP: dominant
denominator `= 2t^2`), and then **decide** the incompatibility question against the
fence: the mechanism is real but **provably confined to the high-fiber regime the
#668 envelope already certifies safe**, and the natural counterexample is **closed by
normalization**. So the tension is not a hidden route to the wall -- it is a true,
now-explained feature of the *safe* part of the plane, and the wall's residual is
localized (matching #663/#691) to blocks that are **additively rich yet AP-free** at
moderate `eta` -- the exponential-regime inverse-LO, approached here from the exact
resonance-denominator side and stripped of the trapping shortcut. Combined with #661
(spectral shortcuts impossible), #663 (energy/Weyl/multiplicity impossible), #682/#685
(geography, dilation excluded), and #691 (the bounded-`q` window empty), the fence is
now known to be immune to the *resolution* form of the fiber-denominator tension as
well, with the exact reason (regime disjointness) in hand.

---

## Files, labels, PI re-derivation

- Note: `experimental/notes/thresholds/fiber_denominator_tension.md` (this).
- Verifier: `experimental/scripts/verify_fiber_denominator_tension.py`
  (`RESULT: PASS (48/48)`, ~4 s / <60 MB; recomputes the census + `#668` envelope +
  dilation closure, Lemma V's identity/inequality/relaxation + the pointwise bound,
  the AP-embedded bound + in-trap table + Sidon negative control, the single-triple
  flatness, the minor-arc mass law, the P5 non-monotonicity + atom bound, and the
  regime map against the envelope).
- Read-only inputs: **DannyExperiments #668** `canonical_transversal_vc_compression.md`;
  our **#661** `exp_ilo_fourier.md`, **#663** `bohr_gap_volume.md`, **#682**
  `corridor_diameter_map.md`, **#685** `corridor_interior_hunt.md`, **#691**
  `fenced_resonance_window.md`, **#655** `fiber_image_tradeoff.md`, **#683**
  `championship_census_b19_26.md`, **#678** `curve_restricted_product.md`, **#643**
  `pte_cluster_packing_frontier.md`; hughes **#564** `w_a_star_pte_lemma.md`.

**Outcome grade (stated up top).** **Primarily (3)** -- an exact structural theorem
(Lemma V) plus its multi-point strengthening (Theorem AP) that convert the
**resolution** half of #691's measured tension into proof, identifying the exact
mechanism (embedded-run Vandermondes) behind the measured small-denominator
concentration. **Reaching (2)** on the AP-structured class (their dominant resonance
is provably at the bounded denominator `2t^2`). **Not (1)**: the **magnitude** half is
shown irreducibly multi-point (BLOCK 3) and the mechanism bites only off the wall
(BLOCK 6), so the fenced wall class is **not** proved empty by this route. **Not (4)**:
the apparent counterexample (spread-resonance high-fiber block) is closed by `gcd=1`
normalization, so none exists; the tension survives, mechanistically explained, on the
normalized (`= #685` non-dilation) class.

**Per-claim status.** Lemma V (identity + weighted/diameter inequalities), the
pointwise mass bound, Theorem AP, and Proposition R3 (disjoint regimes, via the #668
envelope) = **PROVED** (elementary; the `o(1)` in Theorem AP is the explicit
`L/(L-2)` and the Cauchy-Schwarz slack, both bounded in the verifier). The atom
identity/bound, the dilation closure, and the `alpha_0`/envelope arithmetic =
**COMPUTED**. The minor-arc mass law and the P5 non-monotonicity correction =
**MEASURED** (exact `f,L`; `|Xhat|` by midpoint quadrature, used only to read the
concentration trend). The single-triple flatness (mass suppression is multi-point) =
**REFUTED sub-route** (the bounded-support marginal cannot witness the decay). The
identification of #691 T1 with Lemma V's resolution content = **AUDIT**. The
magnitude inverse-LO / "additive richness without an AP at moderate eta" =
**OPEN** (unchanged in substance from #663/#691; now approached from the exact
resonance-denominator side).

**Flagged for PI (least-certain, 3 points).**
(a) **Theorem AP's constant `4` is not optimized** (measured worst ratio `~0.79`, so
the effective constant is `~3.2`); the *shape* `||2t^2 theta_2|| = O(sqrt(eta))` and
the `eta <= 0.033` biting threshold move only by a constant under sharpening, and
Proposition R3's disjointness has slack (`1.18` vs `4/3`), so the *conclusion* (bite
and wall disjoint) is robust to the constant.
(b) **The regime-disjointness uses the #668 *envelope* upper bound**, not a per-block
fact: it certifies that *no* block with `eta <= 0.033` can be a wall block, hence the
AP mechanism never meets a wall block. It does **not** claim a wall block has no
embedded AP -- only that if it did, Theorem AP would place it at a bounded denominator
in #663 R3's already-closable-in-principle horn (still open at large diameter, R3).
(c) **The mass law (R4) and the P5 correction (R5) are midpoint quadrature at
`b <= 20`**; the trend (minor-arc mass small, concentration structure-driven) is exact
in the finite objects, but the `b -> inf` behaviour where the wall lives is beyond
enumeration (the standing #646/#661 small-`b`-plateau caveat applies).

**Exact vs heuristic.** All `f, L, X, phi, lambda, eta`, the dilation closure, the
`alpha_0`/envelope values, Lemma V's identity, and Theorem AP's inequality are exact
integer/closed-form computation. Lemma V, the pointwise bound, Theorem AP, and
Proposition R3 are elementary closed-form proofs. The `|Xhat|` marginals (R4, R5) are
midpoint quadrature used only to read concentration. The exponential-regime magnitude
inverse-LO is cited within its (open) scope and never re-derived. No signed `mu_n`
object entered. No `.tex`/`.pdf` touched.
