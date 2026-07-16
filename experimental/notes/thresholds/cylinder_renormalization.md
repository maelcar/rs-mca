# Failing bands are wide, and base-3 subgroup cylinders renormalize

## Status

```text
Status: PROVED (U1, every base) that failing bands are WIDE: |hatf(xi)| <= M
        for every character, and c ||h_A||_2^2 = sum_{xi in A} hatf(xi)^2
        (Parseval, full norm), so any failing band (||h_A||_2 >=
        e^{eta N} M / L^{1/2}) has
            |A| >= (c/L) e^{2 eta N} .
        Narrow bands NEVER fail; the band-uniform packet's narrow-band
        certificate covers band PIECES, not standalone failures -- the
        middle-band compression residual is therefore THE failing-band
        case.  This packet solves the subgroup-cylinder subcase only.
      + PROVED (U2, base 3 only, c = 3^B) the suffix structure: theta_i(xi)
        depends on xi mod 3^{B-i+1} (the low digits) -- the angle vector is
        the x3-orbit of theta_1 = 2 pi xi / 3^B, and low-digit cylinders
        A_{k,r} = {xi == r (mod 3^k)} are the natural band hierarchy.  This
        is BASE-3-SPECIFIC: the modulus must be a power of the base
        (COUNTEREXAMPLE pin: on base 5 the k = 1 renormalization below
        fails at max deviation 0.40 of M -- M-relative -- against
        absolute deviations < 1e-13 on base 3).
      + PROVED (U3, exact renormalization) on the subgroup cylinder
        (r = 0): for xi = 3^k m the top k factors sit at angle 0 exactly
        ((1+z)^2 each) and the low factors are EXACTLY the scale-(B-k)
        packet's factors at m, so
            hatf_B(3^k m) = sum_j C(2k, B-j) [z^j] p_{B-k, m}(z) :
        the scale-B spectrum on the cylinder is the GRADED (all-slice)
        scale-(B-k) spectrum convolved with (1+z)^{2k}.  Twisted cylinders
        (r != 0): the same factorization with explicit top factors at
        2 pi r 3^{i-1}/3^B and low-factor phase offsets phi_i(r).
        Verified to absolute deviation 6e-12 (~5e-16 of M): B in {6,8},
        k in {1,2,3}, ALL m (subgroup); B = 6, ALL r < 3^k, ALL m
        (twisted); Parseval-guarded at BOTH scales.
      + PROVED (slice staircase + subgroup flatness; the certificate)
        every graded slice of the chart is class-constant (the j-slice
        staircase, same dissociativity proof), so every slice is
        CUBE-FLAT; with the polynomial-level renormalization this PROVES
        that subgroup bands' entire cube spectra concentrate at D = empty.
        Their certificate is therefore the per-class D = empty list,
        O(poly B) per level, with at most 3 distinct values per level in
        the checked cases.  This conclusion does not extend automatically
        to twisted cosets or their finite unions.
      + COUNTEREXAMPLE (twisted flatness): the former verifier evaluated
        only the cosine, hence real, projection of a generally complex
        cube coefficient.  At B=6,k=1,r=1 the omitted nonempty coefficient
        has magnitude sqrt(3).  Even after symmetrizing the depth-two pair
        xi mod 9 in {1,8}, a real nonempty coefficient remains:
            -1.336932620625273... .
        Therefore the former blanket twisted-coset and hierarchy-measurable
        flatness claims are withdrawn.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- fifth packet of the arc (forcing -> typing ->
        reduction -> scope -> compression): the middle-band certificate-
        compression residual named by the band-uniform packet is SOLVED only
        for subgroup cylinders {xi == 0 mod 3^k}.  Twisted and non-hierarchy
        failing bands remain the honest residual, alongside the admission
        decision, atlas totality (the Codex team's lane), and the large-q
        Sidon residual.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays or
        claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  The width identity and
all pins are exact; every trigonometric scan uses floats under exact
Parseval guards at BOTH scales, recomputed by
`experimental/scripts/verify_cylinder_renormalization.py` (stdlib only,
deterministic, `RESULT: PASS`, `--tamper-selftest` catches `5/5`,
~1.4 s).  Machine-readable certificate:
`experimental/data/certificates/cylinder-renormalization/cylinder_renormalization.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/cylinder_renormalization/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `2633895`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)** -- the
renormalization is a structure theorem for the PO3 character sums on the
base-3 chart; **`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Integrated in-tree packets (consumed and credited, not reproved):
- **The transverse-charge packet** (#776,
  `transverse_charge_obstruction_sidon_paired.md`): its Sec-6 closing
  remark -- that the class's self-similar image measure is non-Rajchman
  (integer-base Bernoulli convolutions) and that THIS is the invariant
  content of its resistance -- acquires its exact finite form here: the
  self-similarity is the renormalization identity, and the digit-sparse
  shell is the k ~ B cylinder tail.
- **The band-uniform packet** (#795, `band_uniform_cube_reduction.md` on
  its own branch -- OPEN PR, NOT yet integrated): U1 sharpens its T2 scope
  (narrow bands never fail standalone) and this packet answers its named
  middle-band compression residual on the hierarchy.  Its T2 theta-product
  identity is consumed per band and re-verified here inside the cube
  corollary scans; nothing depends on its integration.
- **The fold-charge packet** (#791, OPEN PR): its closed forms are the
  recursion's base case; its scaled-ledger integers are not consumed here.
- **The resonant-folding packet** (#779, OPEN PR): its digit-sparse shell
  census (42, re-pinned V6) is the cylinder tail's finite face.
- **#739** (`staircase_concentration_sidon_paired.md`) with
  **DannyExperiments' #749-corrected hypotheses**: the class.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged
  interface.

---

## 0. Setup

Class and notation as in the four prior packets; base-3 chart means
`A_i = 3^{i-1}`, `c = 3^B` (so `c = 2L - 1` exactly, V1).  Write
`p_{B,m}(z) = prod_{i=1}^{B} (1 + z^2 + 2 z cos(2 pi m 3^{i-1} / 3^B))`
for the scale-`B` per-pair product, so `hatf_B(m) = [z^B] p_{B,m}` and
`[z^j] p_{B,m}` is the `j`-slice character sum (supports of size `j`).
Bands are symmetric and exclude `0`.

---

## 1. Theorem U1: failing bands are wide (every base)

> **Theorem U1.**  `|hatf(xi)| <= M` for every `xi`, and
> `c ||h_A||_2^2 = sum_{xi in A} hatf(xi)^2`; hence every failing band
> (`||h_A||_2 >= e^{eta N} M / L^{1/2}`) satisfies
> `|A| >= (c/L) e^{2 eta N}`.

**Proof.**  `hatf(xi) = sum_S e_c(-xi Phi(S))` is a sum of `M` unimodular
terms; Parseval on `Z_c` restricted to the band gives the identity; divide.
`square`

Verified (V1): `|hatf| <= M` on full scans (`B in {6,8}` base 3, `B = 6`
base 5) under the Parseval guard; the width chain instantiated on the
six-family band battery; `c = 2L - 1` exact for even `B <= 64` (base 3).
Consequence for the program: the band-uniform packet's narrow-band
certificate never faces a standalone failure -- compression for
`|A| = e^{Theta(N)}` is not an optimization but THE failing-band case.

---

## 2. Theorem U2: the suffix structure of the base-3 chart

> **Theorem U2.**  On the base-3 chart, `theta_i(xi) = 2 pi xi 3^{i-1}/3^B
> mod 2 pi` depends only on `xi mod 3^{B-i+1}`; equivalently the angle
> vector is the x3-orbit of `theta_1 = 2 pi xi / 3^B`.  Low-digit
> cylinders `A_{k,r} = {xi : xi == r (mod 3^k)}` fix the top `k` factors'
> phases relative to the low-scale structure.

One line: `xi 3^{i-1} mod 3^B` discards the top `i-1` digits of `xi`.
This is where `c = 3^B` enters irreplaceably; on base 5,
`c = (5^B+1)/2` is not a power of the base and the digit lattice does not
align with the modulus -- the COUNTEREXAMPLE pin (V5): the k = 1
renormalization below fails on base 5 at max deviation `0.3999 M`
(pinned), against `< 1e-13 M` on base 3.

---

## 3. Theorem U3: exact renormalization on the cylinder hierarchy

> **Theorem U3 (subgroup cylinder).**  For `xi = 3^k m` on the base-3
> chart:  factors `i > B-k` sit at angle `0` exactly, and factors
> `i <= B-k` are the scale-`(B-k)` factors at `m`; hence
> ```text
> hatf_B(3^k m) = [z^B] (1+z)^{2k} p_{B-k, m}(z)
>              = sum_j C(2k, B-j) [z^j] p_{B-k, m}(z) .
> ```
> **(Twisted cylinders.)**  For `xi = r + 3^k m`, `0 < r < 3^k`: the top
> factors sit at the explicit angles `2 pi r 3^{i-1}/3^B` (`i > B-k`) and
> the low factors acquire the phase offsets `phi_i(r) = 2 pi r 3^{i-1}/3^B`:
> `hatf_B(r + 3^k m) = [z^B] (T_r(z) * p^{phi(r)}_{B-k, m}(z))`.

**Proof.**  `theta_i(3^k m) = 2 pi m 3^{k+i-1}/3^B`; for `i > B-k` the
exponent reaches `3^B` and the angle is an integer multiple of `2 pi`
(factor `= (1+z)^2`); for `i <= B-k` it equals `2 pi m 3^{i-1}/3^{B-k}`,
the scale-`(B-k)` angle.  The identity is therefore POLYNOMIAL-LEVEL:
`p_{B, 3^k m}(z) = (1+z)^{2k} p_{B-k, m}(z)` as polynomials, so EVERY
graded slice renormalizes -- `[z^d] p_{B, 3^k m} = sum_t C(2k, d-t)
[z^t] p_{B-k, m}` for every `d`, not only `d = B` -- which is exactly what
closes the recursion's induction (Sec 4).  Twisted: split
`xi = r + 3^k m` in each angle; the `m`-part vanishes on the top factors
and renormalizes on the low ones; the `r`-part is the stated constant
offset. `square`

Verified (V2/V3): subgroup form at `B in {6,8}`, `k in {1,2,3}`, ALL `m`
(max deviation `6e-12 M`); twisted form at `B = 6`, ALL `r < 3^k`, ALL
`m` (max `2.6e-13 M`); the scale-`(B-k)` weights are Parseval-guarded at
their own scale.

**Reading.**  The graded slices `[z^j] p_{B-k,m}` are the smaller chart's
unbalanced character sums -- known objects.  The cylinder's spectrum at
scale `B` is those, convolved with the explicit `(1+z)^{2k}` -- the
top-`k` pairs enter in their degenerate all-angle-zero state.  The whole
identity is the x3-shift self-similarity of the class made exact at
finite `B`.

---

## 4. The cube corollary and the twisted-coset correction

> **Lemma (slice staircase).**  For EVERY slice size `j` (not only
> `j = B`), the `j`-slice of the chart is class-constant: within a class
> at level `s` (`s <= j`, `s == j mod 2`), every realized value is
> attained by exactly `C(B-s, (j-s)/2)` supports, and distinct values do
> not collide across classes (the same +-2-dissociativity).  Hence every
> graded slice measure is CUBE-FLAT: its sign-cube spectrum on every
> class is concentrated at `D = empty`.
>
> **Corollary (subgroup flatness + the certificate).**  Over the
> subgroup band `A_{k,0} \ {0}` (= `{3^k m : m in [1, 3^{B-k})}` after
> symmetrization): the entire cube spectrum is concentrated at
> `D = empty` -- every `D != empty` coefficient VANISHES (PROVED: the
> polynomial-level renormalization writes the band's weights as graded
> combinations of scale-`(B-k)` slices, and each slice is cube-flat by
> the Lemma).  Its certificate is therefore its per-class `D = empty`
> value list -- NOT the `hatf` list -- and those values renormalize to the
> graded-convolved scale-`(B-k)` data and take at most 3 distinct values
> per level (pinned).

> **Counterexample (twisted flatness).**  Twisted renormalization does not
> preserve cube-flatness.  For `B=6`, `k=1`, and `r=1`, literal complex
> Fourier inversion gives a nonempty sign-cube coefficient of magnitude
> `sqrt(3)`.  The old verifier used only
> `cos(2*pi*xi*sigma/c)`, discarding the imaginary component.  This is not
> repaired by symmetric finite unions: for
> `Q_1={xi : xi mod 9 in {1,8}}` and the top-coordinate pattern
> `U={B-2,B-1}`, the full two-coordinate coefficient equals
>
> ```text
> -(2/9) sin(2*pi/9) sin(2*pi/3)
>   * (w0 + 2*w2*(cos(4*pi/9)+cos(8*pi/9)))
> = -1.336932620625273...,
> w0 = C(B,B/2), w2 = C(B-2,(B-2)/2).
> ```
>
> Here `cos(4*pi/9)+cos(8*pi/9)=-cos(2*pi/9)`.  For every even `B>=4`,
> `w2/w0=B/(4(B-1))<=1/3`, so the bracket divided by `w0` is at least
> `1-2/3>0`; both sine factors are nonzero.  This proves an infinite
> nonflat symmetric family without relying on floating-point separation.

Verified (V4): flatness on subgroup cosets, all classes and all patterns;
the literal complex regression pins `sqrt(3)` on the twisted `B=6,k=1,r=1`
coset and `-1.336932620625273...` on the symmetric depth-two union.  The
nonzero subgroup spectrum is exactly the 31 per-class `D = empty` values at
`B = 6, k = 1`; the renormalized `D = empty` values agree with
the graded-convolved scale-`(B-k)` sum (absolute `2e-15`); the
`<= 3` distinct values per level; and the slice staircase by brute force
at EVERY slice size (`B in {4,6}`, both bases).  The compression is thus
of the CUBE SPECTRUM, not the `hatf` list (which stays irreducibly
exponential): a subgroup band's certificate is its per-class
`D = empty` list, `O(poly B)` per level via the renormalization, with
flatness PROVED on subgroup bands (Lemma + renormalization).  Disjoint-band
norms remain orthogonal, but their cube spectra do not become flat merely by
addition.  Twisted and general hierarchy-measurable bands require the exact
cube-spectrum criterion from the band-uniform packet, case by case.

**Relevance** (V7, pinned): the failing maximal band IS the depth-`k`
coset union at every `k` (coset spectral masses add exactly; the per-coset
shares are pinned at `k = 1`: `.2065 / .3968 / .3968` at `B = 6` and
`.3164 / .3418 / .3418` at `B = 10` -- the subgroup coset is
under-weighted at small `B` and the shares drift toward `1/3`, COMPUTED
trend), and the subgroup band's own failure ratio grows with `B` at fixed
`k` (`R = 0.4615 / 0.6226 / 0.7834` at `B = 6/8/10`, `k = 1`, strictly
increasing -- COMPUTED; not yet failing at the scanned sizes).  This norm
decomposition does not imply cube-flat certificates for the twisted pieces.

## Nonclaims

- **Twisted and adversarial bands are NOT compressed** -- a failing band need
  not be a subgroup cylinder, and a twisted cylinder or finite coset union can
  have nonzero cube spectrum.  The honest residual is "compress, pay, or
  exclude non-subgroup failing bands"; U1 removes only the narrow case.
- **Base 3 only** for U2/U3/the corollary (COUNTEREXAMPLE pin on base 5,
  V5); U1 is every-base.
- **No admission claim**: the certificates are inputs for the (open)
  cube-spectrum emission decision; no payment is made here.
- **One recursion level is verified**; deeper levels are by induction on
  the same proved identity, not separately scanned.
- Floats only in the scans, under Parseval guards at both scales; the
  `c = 2L - 1` identity, the census, and the M2 pins are exact.
- **NOT a reserve payment**: fence (N1) respected.

## Consumers

- **The band-uniform packet (#795 note)**: its T2 scope is sharpened (U1)
  and its named middle-band residual is answered on subgroup cylinders (U3 +
  corollary); twisted pieces return to its exact cube-spectrum criterion.
- **The fold-charge packet (#791 note)**: its closed forms become the
  recursion's base case.
- **The resonant-folding packet (#779 note)**: its digit-sparse shell is
  the hierarchy's `k ~ B` tail; its census re-pins here.
- **#716**: the sixth alternative's certificate inputs cover subgroup
  cylinders at every width, not arbitrary twisted unions.
- `rs_mca_thresholds.tex`: paste-ready as a remark after the PO4 material
  -- "on the base-3 Sidon-paired chart the character sums renormalize
  exactly on subgroup cylinders (top factors degenerate to (1+z)^{2k};
  the rest is the smaller chart's graded spectrum), so those bands carry
  recursive e^{o(N)} cube certificates; twisted cylinders need separate
  cube-spectrum checks; failing bands are always exponentially wide" --
  visible hypotheses: #749-corrected class, base-3 chart (c = 3^B), q=2
  rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_cylinder_renormalization.py
# -> RESULT: PASS (42/42)
python3 experimental/scripts/verify_cylinder_renormalization.py --tamper-selftest
# -> tamper-selftest: caught 5/5 ; then RESULT: PASS (42/42)
python3 experimental/scripts/verify_cylinder_renormalization.py --emit-certificate \
  experimental/data/certificates/cylinder-renormalization/cylinder_renormalization.json
cd experimental/lean/cylinder_renormalization && lake build
# -> Build completed successfully
```
