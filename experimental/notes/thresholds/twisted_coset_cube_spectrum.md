# The twisted-coset cube spectrum is a rank-one product: complete classification on the base-3 hierarchy

## Status

```text
Status: PROVED (Lemma 0 + Lemma N, exact arithmetic): canonical balanced-
        ternary representations are unique mod 3^B, and the size-B support
        count is
            N(y) = wtil(s3(y)),   wtil(s) = C(B-s,(B-s)/2) [s == B mod 2],
        where s3(y) counts nonzero balanced digits.  On the base-3 chart the
        prior packets' +-2-dissociativity IS balanced uniqueness.
      + PROVED (Theorem A, localization): for EVERY depth-k hierarchy-
        measurable band (any union of cosets mod 3^k), every class-v sign-
        cube coefficient with D touching a coordinate below B-k vanishes
        EXACTLY.  The cube function factors through the top-block digit
        word tau(eps_top) in Z_3^k.
      + PROVED (Theorem B, product law): on the single coset
        K_{k,r} = {xi == r mod 3^k},
            chat_v(D) = [D inside top_v] * G_{k,r}(s_low)
                        * prod_{t in top_v} ( -i sin(beta_t)  if t in D
                                              else  cos(beta_t) ),
            beta_t = 2 pi r 3^{U_t-(B-k)} / 3^k,
            G_{k,r}(l) = 3^{-k} sum_{a in Z_3^k} e(-ar/3^k) wtil(s3(a)+l).
        The class-v cube function on K_{k,r} is the unimodular character
        e(-r tau(eps_top)/3^k) times the class constant G_{k,r}(s_low):
        rank one.  General measurable bands are the r-sums (linearity).
      + COROLLARIES: (C1) r=0 kills every sine -- subgroup flatness drops
        out in one line, with G_{k,0}(l) = 3^{-k} sum_j C(k,j) 2^j
        wtil(j+l).  (C2) A depth-k measurable band's ENTIRE cube spectrum
        is determined by the (B+1) * 3^k table {G_{k,r}(l)} plus closed
        trig factors: certificate size O(B 3^k) -- poly(B) for
        k = O(log B).  The withdrawn hierarchy-measurable compression is
        RESTORED in corrected form: not by flatness, but by the product
        law.  (C3) Bug anatomy: G_{1,r} is real, so at k=1 the whole
        nonflat spectrum is PURELY IMAGINARY -- a cosine projection sees
        exact zeros; the withdrawn packet's twisted scan (k=1) verified
        the wrong functional at float-exact 0.  (C4) chat_v(D) = 0 at a
        D-coordinate iff 3^{k-j_t} | r (sine zero) or G vanishes: exact
        vanishing criterion; every twisted k=1 coset is unconditionally
        nonflat.  (C5) per-class cube energy is
        sum_D |chat_v(D)|^2 = |G_{k,r}(s_low)|^2, and coset mass is
        c 3^k sum_l C(B-k,l) 2^l |G(l)|^2 -- V7 in closed form.
      + COMPUTED pins re-derived symbolically: #805's sqrt(3) (k=1,r=1,
        max nonempty = |G_{1,1}(1) sin(2pi/3)|) and its symmetric depth-two
        -1.336932620625273... (the r in {1,8} product-law sum; equals the
        published closed form).
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- sixth packet of the arc (forcing -> typing ->
        reduction -> scope -> compression -> CLASSIFICATION); repairs the
        cylinder packet's #805-corrected residual: twisted and hierarchy-
        measurable bands are no longer "case by case" -- they are
        classified.  The honest input-2 residual is now: the admission
        decision, genuinely NON-hierarchy adversarial bands, atlas
        totality (the Codex team's lane), and large-q Sidon.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays
        or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Lemmas 0/N and the
counting identities are exact integer arithmetic; the trigonometric side is
float scans under exact Parseval guards, recomputed by
`experimental/scripts/verify_twisted_coset_cube_spectrum.py` (stdlib only,
deterministic, `RESULT: PASS (19/19)`, `--tamper-selftest` catches `6/6`
including a `cosine_only` meta-tamper reproducing the original bug, ~0.5 s).
Machine-readable certificate:
`experimental/data/certificates/twisted-coset-cube-spectrum/twisted_coset_cube_spectrum.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/twisted_coset_cube_spectrum/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `02728b2`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)** -- the
product law is the complete PO3 cube-spectrum structure theorem for
hierarchy bands on the base-3 chart; **`thm:aperiodic-one-ray-saturation`
(SAT1)**: fence (N1).

Integrated in-tree packets (consumed and credited, not reproved):
- **The cylinder packet as corrected by DannyExperiments' #805**
  (`cylinder_renormalization.md`): its U2/U3 renormalization frame and its
  #805 counterexample constants are this packet's starting point; both
  regression constants are re-derived here in closed form.  Its "twisted
  and general hierarchy-measurable bands ... case by case" residual is
  CLASSIFIED by Theorems A/B.
- **The band-uniform packet** (#795, `band_uniform_cube_reduction.md`): its
  exact cube-spectrum emission criterion receives, for every depth-k
  measurable band, the closed-form input {G-table + trig products} instead
  of a scan.
- **The fold-charge packet** (`fold_charge_localization.md`): its closed
  forms remain the k = 0 base data; `wtil` is its level-fiber count.
- **#739 with DannyExperiments' #749-corrected hypotheses**: the class.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged
  interface; non-hierarchy bands remain outside this packet.

---

## 0. Setup

Class and chart as in the five prior packets: `P_i = 3^i` (`0 <= i < B`),
`c = 3^B = 2L - 1`, `T = P u (c - P)`, `hatf(xi) = sum_S e_c(-xi Phi(S))`
over size-`B` supports `S` of `T`, `M = C(2B,B)`; throughout,
`e(x) = e^{2 pi i x}` and `e_c(x) = e(x/c)`.  Classes are parity
vectors `v in {0,1}^B` at level `s = |v|` with unpaired set
`U = {U_0 < ... < U_{s-1}}` and fiber count `w_s = C(B-s,(B-s)/2)`;
signatures `sigma(eps) = sum_t eps_t 3^{U_t} mod c`, `eps in {+-1}^s`.  For
a band `A` (here: not necessarily symmetric; single cosets are the
primitives and symmetrization is by `r <-> 3^k - r` pairing) the class-`v`
cube function is
`eps -> hv_A(sigma(eps)) = (1/c) sum_{xi in A} hatf(xi) e_c(-xi sigma(eps))`
-- a genuinely COMPLEX number -- and its sign-cube coefficients are
`chat_v(D) = 2^{-s} sum_eps (prod_{t in D} eps_t) hv_A(sigma(eps))`,
`D subset [s]`.  `K_{k,r} = {xi == r mod 3^k}`; the top block of `v` at
depth `k` is `top_v = {t : U_t >= B-k}`; `s_low = s - |top_v|`.
`wtil(s) = w_s` if `0 <= s <= B` and `s == B mod 2`, else `0`.  `s3(y)`
counts the nonzero digits of the canonical balanced-ternary representation
of `y` (digits in `{-1,0,1}`).

---

## 1. Lemma 0 and Lemma N: counting is digit counting

> **Lemma 0 (balanced uniqueness).**  Every residue mod `3^B` has exactly
> one representation `sum_{i<B} d_i 3^i` with `d_i in {-1,0,1}`.  (The
> same statement and proof hold with any modulus `3^k`; `s3` on `Z_3^k`
> below uses this.)

**Proof.**  Both sides have `3^B` elements, so injectivity suffices.  If
two representations agree mod `3^B`, their digit difference
`u_i in {-2,...,2}` satisfies `sum u_i 3^i == 0`; reducing mod 3 forces
`u_0 == 0 mod 3`, hence `u_0 = 0`; divide by 3 and induct. `square`

> **Lemma N (support count).**  For every `y`,
> `N(y) := #{S subset T, |S| = B, Phi(S) = y} = wtil(s3(y))`.

**Proof.**  A size-`B` support takes from each pair `{P_i, c-P_i}` either
one element (`s` unpaired positions, sign `eps_i`), both (`d` positions),
or neither (`e` positions); `s + 2d = B` and `s + d + e = B` force
`d = e = (B-s)/2`, so `s == B mod 2`.  Since `P_i + (c-P_i) == 0 mod c`,
`Phi(S) = sigma(eps)`, and the doubled positions can be chosen in
`C(B-s,(B-s)/2) = w_s` ways for each fixed `(U, eps)`.  The map
`(U, eps) -> sigma(eps)` is a bijection onto residues with `s` nonzero
balanced digits (Lemma 0: the digits ARE `(U, eps)`).  Summing, `N(y) =
w_{s3(y)}` on the realized parity and `0` otherwise. `square`

Verified (exact integers): all `y`, `B in {4,6,8}`; plus the count
`#{a in Z_3^k : s3(a) = j} = C(k,j) 2^j` for `k <= 6`.  Consequence
(Parseval cross-check): `sum_xi hatf(xi)^2 = c sum_s C(B,s) 2^s wtil(s)^2`.

**Reading.**  On the base-3 chart the class machinery linearizes: the
support-count transform of the chart is literally "count nonzero balanced
digits, look up the fiber."  The prior packets' `+-2`-dissociativity is
balanced uniqueness.

---

## 2. Theorem A: exact localization to the top block

> **Theorem A.**  Fix `k` and a class `v`.  For every depth-`k`
> hierarchy-measurable band `A` (any union of cosets mod `3^k`, any
> weights), the class-`v` cube function of `A` depends on `eps` only
> through the top-block word
> `tau(eps_top) = sum_{t in top_v} eps_t 3^{U_t-(B-k)} in Z_3^k`.
> Consequently `chat_v(D) = 0` EXACTLY whenever `D` contains a coordinate
> `t` with `U_t < B-k`.  ("Exactly" = exact zero, not float fuzz; the
> implication is one-way -- top-block coefficients can also vanish, C4.)

**Proof.**  By linearity it suffices to treat `A = K_{k,r}`.  Fourier on
the coset indicator (`e(x) = e^{2 pi i x}`):
```text
hv_{K_{k,r}}(sigma) = 3^{-k} sum_{a in Z_3^k} e(-ar/3^k) N(a 3^{B-k} - sigma),
```
because `(1/c) sum_xi hatf(xi) e_c(-xi(sigma - a 3^{B-k})) =
N(a 3^{B-k} - sigma)` by Lemma N's transform.  Split
`sigma = 3^{B-k} tau(eps_top) + sigma_low`.  Reindexing
`a -> a + tau(eps_top)` (a bijection of `Z_3^k`) extracts a unimodular
character:
```text
hv_{K_{k,r}}(sigma(eps)) = e(-r tau(eps_top)/3^k)
    * 3^{-k} sum_a e(-ar/3^k) N(a 3^{B-k} - sigma_low).
```
Digit lemma: `a 3^{B-k} - sigma_low` has canonical balanced digits `(-eps_t
at the positions U_t < B-k; 0 at the other positions below B-k; the
balanced digits of a mod 3^k at the positions >= B-k)` -- the exhibited
representation has digits in `{-1,0,1}` with no position collisions and no
carries, so Lemma 0 makes it canonical.  Hence
`N(a 3^{B-k} - sigma_low) = wtil(s3(a) + s_low)`: independent of every
sign `eps_t` (low positions contribute one nonzero digit each, regardless
of sign) and of WHICH low positions carry them.  So
```text
hv_{K_{k,r}}(sigma(eps)) = e(-r tau(eps_top)/3^k) * G_{k,r}(s_low),
G_{k,r}(l) = 3^{-k} sum_{a in Z_3^k} e(-ar/3^k) wtil(s3(a)+l),
```
a function of `eps_top` alone.  Averaging any `eps_t` with `t in D`,
`U_t < B-k`, against `prod_{t in D} eps_t` gives `0`. `square`

Verified: worst nonzero-pattern magnitude below the top block `1.5e-15`
over ALL `(k,r)`, `k in {1,2,3}`, all classes, all patterns at `B = 6`
(13104 coefficients); the digit lemma itself checked EXHAUSTIVELY in exact
integers -- all `(a, u)`, `k in {1,2,3}`, `B in {6,8}` -- and shadowed in
Lean at `B in {4,6}`.

---

## 3. Theorem B: the rank-one product law

> **Theorem B.**  On `K_{k,r}`, for `D subset top_v` (else `0`):
> ```text
> chat_v(D) = G_{k,r}(s_low) * prod_{t in top_v} chi_t,
>   chi_t = -i sin(beta_t)   if t in D,     beta_t = 2 pi r 3^{U_t-(B-k)} / 3^k
>         =    cos(beta_t)   if t not in D.
> ```

**Proof.**  From Theorem A's displayed form, the cube transform factors
over top coordinates because `e(-r tau/3^k) = prod_{t in top_v}
e(-r eps_t 3^{U_t-(B-k)}/3^k)`; writing `beta_t = 2 pi r 3^{U_t-(B-k)}/3^k`,
the single-coordinate averages are
`(1/2)(e^{-i beta_t} + e^{+i beta_t}) = cos(beta_t)` (`t not in D`) and
`(1/2)(e^{-i beta_t} - e^{+i beta_t}) = -i sin(beta_t)` (`t in D`). `square`

Verified: ALL 13104 coefficients at `B = 6` (worst `8.9e-15`); spot check
`B = 8`, `(k,r) in {(1,1),(2,5)}` (worst `2.0e-14`); random depth-`k`
unions obey the `r`-summed law (worst `8.3e-15`).

**Structure.**  The class-`v` cube function on a twisted coset is RANK ONE:
a fixed unimodular character of the top signs, scaled by a class constant.
All the `r`-dependence sits in `3^k` explicit trig values and the
`(B+1)`-entry `G`-table.

---

## 4. Corollaries

**C1 (subgroup flatness, one line).**  `r = 0` makes every `beta_t = 0`:
all sines vanish, so only `D = empty` survives, with value
`G_{k,0}(s_low) = 3^{-k} sum_j C(k,j) 2^j wtil(j + s_low)` (by the exact
digit count `#{a : s3(a) = j} = C(k,j) 2^j`).  This re-derives the
cylinder packet's subgroup-flatness theorem and its `D = empty` values
without the slice-staircase apparatus.

**C2 (the corrected compression).**  For any depth-`k` hierarchy-
measurable band, the whole cube spectrum across ALL classes is generated
by the table `{G_{k,r}(l) : 0 <= l <= B, r in the profile}` -- at most
`(B+1) 3^k` complex numbers, each a `3^k`-term explicit sum -- and the
closed trig factors.  Certificate size `O(B 3^k)`: `poly(B)` for
`k = O(log B)`.  The withdrawn "hierarchy-measurable flatness" becomes the
CORRECT statement: hierarchy bands are not flat, but they are exactly this
compressible.  The cylinder packet's V7 relevance pin (the failing maximal
band is the depth-`k` coset union) means the failing band itself carries
this certificate at every depth.

**C3 (bug anatomy).**  `G_{1,r}(l) = (1/3)[wtil(l) + 2 cos(2 pi r/3)
wtil(l+1)]` is REAL, and at `k = 1` the top block is a single coordinate,
so every nonempty coefficient is `-i sin(2 pi r/3) G_{1,r}(s_low)`:
PURELY IMAGINARY (worst real part `1.4e-15`, all `r`, verified).  A
cosine-only projection therefore returns EXACT zeros on every twisted
`k = 1` coset -- the withdrawn packet's twisted scan was float-exact on
the wrong functional.  Real parts first appear at `|D| = 2` (depth >= 2),
which is precisely DannyExperiments' #805 counterexample; both of its
regression constants are re-derived here symbolically (`sqrt(3)` at
`k=1,r=1` -- note `|-i| sqrt(3)` in magnitude -- and
`-1.336932620625273...` on the symmetric depth-two union, equal to the
published closed form).

**C4 (exact vanishing + nonflat existence).**  `sin(beta_t) = 0` iff
`3^{k-j_t} | r` (`j_t = U_t - (B-k)`); a coefficient vanishes iff `D`
leaves the top block, meets a sine zero, or `G_{k,r}(s_low) = 0`.  Cosine
factors NEVER vanish (`cos(2 pi x) = 0` needs `x == +-1/4 mod 1`,
impossible with 3-power denominators).  Nonflat existence for a twisted
coset (`3^k` not dividing `r`):
- `k = 1`, unconditionally: a top-occupied class is realized iff
  `s_low + 1 == B mod 2`; on that parity `wtil(s_low) = 0`, so
  `G_{1,r}(s_low) = (1/3)[wtil(s_low) + 2 cos(2 pi r/3) wtil(s_low+1)]
  = -(1/3) wtil(s_low+1) != 0` (`cos = -1/2`, `s_low + 1 <= B`) -- the
  verified purely-imaginary family.
- `k >= 2`, whenever the coset carries any spectral mass: C5's coset-mass
  identity sums over exactly the REALIZABLE `l <= B-k`, so positive mass
  forces `G(l) != 0` for some `l <= B-k`.  Take `s_low = l` low
  coordinates (possible since `l <= B-k`) and one top coordinate at
  `j = 0` (`sin(2 pi r/3^k) != 0` because `3^k` does not divide `r`); if
  `l + 1 != B mod 2`, add the `j = 1` top coordinate (`k >= 2` provides
  the position; its cosine is nonzero as above).  Then
  `D = {the j = 0 coordinate}` has
  `chat_v(D) = -i sin(2 pi r/3^k) [cos(2 pi r 3/3^k)] G(l) != 0`.
Verified: EVERY twisted coset at `B = 6` is nonflat (the per-coset max
nonempty magnitude is bounded away from 0 across all `(k,r)`; verifier
check C4).

**C5 (energy identities).**  Per class:
`sum_D |chat_v(D)|^2 = |G_{k,r}(s_low)|^2` (cube Parseval; the character
is unimodular; verified, worst `2.2e-14`).  Per coset (full-`sigma`
Parseval through the digit split -- every `sigma in Z_c` splits into a
top word and a low balanced word):
```text
sum_{xi in K_{k,r}} hatf(xi)^2 = c 3^k sum_{l=0}^{B-k} C(B-k,l) 2^l |G_{k,r}(l)|^2 ,
```
verified for ALL `(k,r)`, `k in {1,2,3}` (worst relative `3.2e-14`): the
cylinder packet's V7 coset-mass decomposition in closed form.  Flat-part
share `prod cos^2(beta_t)` per class; everything else is honest nonflat
mass, now explicit.

---

## Nonclaims

- **Base 3 only** (`c = 3^B`); inherits U2's chart-specificity.  U1
  (wide bands) is every-base and untouched.
- **Non-hierarchy (adversarial) bands are NOT covered**: a band that is
  not measurable at any bounded depth has no `G`-table of bounded size;
  those remain in the input-2 residual, with the admission decision and
  large-q Sidon.
- **No admission claim, no payment**: the closed-form spectra are inputs
  to the (open) cube-spectrum emission decision; fence (N1) respected.
- **Single cosets are asymmetric** (`hatf` real but `hv` complex);
  symmetric statements pair `r` with `3^k - r`, as in the derived #805
  constant.  Bands excluding `xi = 0` shift only `D = empty` (by `-M/c`
  per the subgroup coset), stated where used.
- Floats appear only in trig scans under exact Parseval guards; Lemmas
  0/N, the digit lemma, and all counting identities are exact integers.

## Consumers

- **The cylinder packet (#805-corrected)**: its "must be classified or
  paid case by case" residual for twisted/hierarchy-measurable bands is
  CLASSIFIED; its subgroup theorem is re-derived in one line (C1); its
  V7 failing-band decomposition now carries closed-form certificates at
  every depth (C2).
- **The band-uniform packet (#795)**: the exact cube-spectrum emission
  criterion gets closed-form inputs for every hierarchy band -- the
  emission decision can now be posed against `{G-table + trig products}`
  instead of scans.
- **The sixth-alternative / admission lane (#791, #716)**: the certified
  grammar's twisted instances are now the explicit rank-one family.
- **DannyExperiments' #805**: both regression constants derived
  symbolically; the correction's scope confirmed exactly (twisted bands
  are nonflat, and THIS is their spectrum).
- `rs_mca_thresholds.tex`: paste-ready remark after the PO4 material --
  "on the base-3 chart, every depth-k hierarchy band's sign-cube spectrum
  is the rank-one product of an explicit top-block character transform
  and a (B+1)x3^k G-table; subgroup flatness is the r=0 sine degeneracy;
  certificates are O(B 3^k)" -- visible hypotheses: #749-corrected class,
  base-3 chart, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_twisted_coset_cube_spectrum.py
# -> RESULT: PASS (19/19)
python3 experimental/scripts/verify_twisted_coset_cube_spectrum.py --tamper-selftest
# -> tamper-selftest: caught 6/6
python3 experimental/scripts/verify_twisted_coset_cube_spectrum.py --emit-certificate \
  experimental/data/certificates/twisted-coset-cube-spectrum/twisted_coset_cube_spectrum.json
cd experimental/lean/twisted_coset_cube_spectrum && lake build
# -> Build completed successfully
```
