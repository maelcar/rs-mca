# The transfer certificate for product-profile bands: the dense-band transform is an IFS cocycle, and a carry DP evaluates its class data

## Status

```text
Status: PROVED (C1, the cocycle form): scanning the balanced digits
        d_0, d_1, ... of w upward with state u <- (d + u)/3 (from
        u = 0) and multiplying 2 cos(2 pi u) after each step gives
            prod_{i<B} 2 cos(theta_i(w))
        EXACTLY -- the dense-band indicator transform (#827 D(c)) is an
        iterated-function-system cocycle with contraction 1/3.
      + PROVED (C2, the carry DP): the dense band's class function
        h_v(sigma) = (1/c) sum_y N(y) prod_i 2 cos(theta_i(y - sigma))
        is computed EXACTLY by a digit dynamic program over sigma's
        balanced word: registers (carry in {-1,0,1}, level count, IFS
        tail u), transition v = e - g_j + carry_in, digit
        d = ((v+1) mod 3) - 1, carry_out = (v-d)/3 (closed on
        {-1,0,1}, checked exactly on all 27 cases), terminal weights
        wtil(count), and EVERY final carry accepted -- mod 3^B the
        produced digit word is canonical regardless of the final carry
        (balanced uniqueness; rejecting nonzero final carries is
        wrong by O(1), tamper-pinned).
      + COMPUTED (C3, the spectral evaluation): the adjoint
        function-valued DP on K Chebyshev nodes evaluates h_v(sigma)
        in O(B^2 K^2) work with GEOMETRIC K-convergence: worst error
        7.0e-5 / 6.1e-10 / 1.5e-14 at K = 8/12/16 (B = 8, 16
        signatures) -- machine precision at K = 16, ~20 ms/signature.
        The rigorous interpolation-error bound (Bernstein-ellipse; the
        factors are entire and the branch maps contract [-1/2,1/2]
        into itself) is the named open step.
      + PROVED (C4, generality): for ANY symmetric product profile
        (lambda_j(1) = lambda_j(-1)) the band indicator transform
        factors digit-wise with affine factors
        lambda_j(0) + 2 lambda_j(1) cos(theta_j(w)) (same Lemma-0
        digit independence) -- the identical DP machinery covers the
        whole symmetric product-profile family, with the dense shell
        the a_j = 0, b_j = 1 instance.
      + COMPUTED (C5, positivity pin): hatf > 0 on the ENTIRE dense
        shell at B in {6,8} (min hatf/M = 0.0177 / 0.0045); proof open.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- eleventh packet of the arc; REMOVES the
        certificate obstacle #827 left for the canonical non-hierarchy
        family: product-profile band class data is poly-evaluable
        (empirically to machine precision), so the omega-capped greedy
        machinery (#818/#820/#824) has computable inputs on the dense
        shell and its family.  Remaining for product-profile EMISSION:
        the rigorous truncation bound (C3's open step), the emission
        arithmetic on top (mechanical given trusted evaluation), and
        the positivity pin's proof.  Input-2 residual: the admission
        acceptance, those three steps, non-product non-hierarchy
        bands, atlas totality (the Codex team's lane), large-q Sidon.
        Fence (N1) (thm:aperiodic-one-ray-saturation) respected:
        nothing here pays or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**; COMPUTED marks exact
deterministic scans (sibling usage).  Verifier:
`experimental/scripts/verify_product_profile_transfer.py` (stdlib only,
deterministic, `RESULT: PASS (11/11)`, `--tamper-selftest` catches `5/5`,
~1.2 s).  Machine-readable certificate:
`experimental/data/certificates/product-profile-transfer/product_profile_transfer.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/product_profile_transfer/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `9c4ca98`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)**;
**`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Consumed packets on their OWN BRANCHES -- **#816/#818/#820/#824/#827**
(OPEN PRs, NOT yet integrated at base `9c4ca98`): Lemma 0/N, the class
machinery, the omega-capped greedy schedule, and #827's dense-shell
structure (closed-form transform, the shell = the level-B signature
cube) are their content; every fact used here is RE-DERIVED and
RE-VERIFIED self-containedly (this verifier rebuilds hatf, the shell,
and all identities from scratch).  Inline pins: base-3 chart
`P_i = 3^i`, `c = 3^B`, `T = P u (c - P)`, `Phi(S) = sum S mod c` over
size-`B` supports `S` of `T`, `hatf(xi) = sum_S e_c(-xi Phi(S))`,
`N(y) = wtil(s3(y))`, `wtil(s) = C(B-s,(B-s)/2)` on parity
`s == B mod 2` else 0, `theta_i(z) = 2 pi z 3^i / c`.  Classes are
parity vectors `v in {0,1}^B` (unpaired set `U`, level `s = |U|`);
signatures `sigma(eps) = sum_t eps_t 3^{U_t} mod c`; the class function
of a band is `sigma -> (1/c) sum_{xi in band} hatf(xi) e_c(-xi sigma)`.
The dense band is `S_B = {xi : s3(xi) = B}`.

Integrated in-tree packets (consumed and credited, not reproved):
- **The cylinder packet (#798/#805-corrected)** and **the band-uniform
  packet (#795)**: the band/class conventions.
- **Codex team's atlas-totality lane** (in progress, theirs): unchanged.

---

## 0. Setup

As pinned in Interfaces.  Balanced digits `d_j(w)` from the canonical
representation; the IFS state after scanning `d_0..d_{m-1}` is
`u_m = (0.d_{m-1}...d_0)_3` (balanced fraction), satisfying
`u_m = (d_{m-1} + u_{m-1})/3`, `u_0 = 0`.

---

## 1. Theorem C1: the cocycle form

> **Theorem C1.**  `theta_i(w) = 2 pi u_{B-i}(w)`, hence
> `prod_{i<B} 2 cos(theta_i(w)) = prod_{m=1}^{B} 2 cos(2 pi u_m(w))`:
> the digit scan with state map `u <- (d+u)/3` and factor
> `2 cos(2 pi u)` computes the dense-band indicator transform.

**Proof.**  `w 3^i mod 3^B = sum_{j < B-i} d_j 3^{j+i}` (the top terms
vanish mod `3^B`), so `theta_i(w)/2pi = sum_{j<B-i} d_j 3^{j-(B-i)} =
u_{B-i}`; the products agree as multisets of factors. `square`

Verified: 800 random `w`, `B in {6,8}`, worst `8.5e-14`.
Consequence: digit-product-weighted sums over `w` are transfer-operator
powers -- `(T_lambda g)(u) = sum_d lambda(d) 2cos(2pi(d+u)/3)
g((d+u)/3)`, contraction `1/3`, analytic weights.  The factor vanishes
at `u = +-1/4`, which the 3-adic orbit provably never hits (no 3-power
fraction equals 1/4 -- #816 C4's argument) though it approaches at
distance `>= 1/(4 * 3^m)` at depth `m`.

---

## 2. Theorem C2: the carry DP for class data

> **Theorem C2.**  For a class signature `sigma` with balanced digits
> `g_j`: enumerate `y` by its digits `e_j in {-1,0,1}`; the difference
> `w = y - sigma mod 3^B` is produced digit-by-digit by the carry
> automaton `v = e_j - g_j + carry_in`, `d_j = ((v+1) mod 3) - 1`,
> `carry_out = (v - d_j)/3` -- closed on `{-1,0,1}` (all 27 cases,
> exact) -- and the DP over states (carry, level count, IFS tail `u`)
> with per-step factor `2 cos(2 pi u_new)` and terminal weight
> `wtil(count)` computes `c * h_v(sigma)` EXACTLY, provided every
> final carry is ACCEPTED: mod `3^B` the produced word is the
> canonical representation of `w` whatever the final carry (it is a
> B-digit balanced word representing the same residue; Lemma 0's
> uniqueness).  Rejecting nonzero final carries is wrong by `O(1)`
> (tamper-pinned at `1.7` absolute).

Verified: 80 signatures across three classes, `B in {6,8}`, worst
`1.1e-14` against literal brute Fourier inversion.

---

## 3. The spectral evaluation (computed convergence)

The exact DP's `u`-register takes up to `3^B` values (it is a
reorganized exact sum).  The ADJOINT formulation -- process digits from
the top, maintaining for each (carry, count) register the contribution
function `F(u)` of the remaining digits -- makes each step an
application of an analytic 3-branch operator; representing `F` by its
values at `K` Chebyshev nodes on `[-1/2, 1/2]` (barycentric
interpolation) gives an `O(B^2 K^2)`-work evaluation.  Measured
convergence at `B = 8` (16 signatures): worst error
`7.0e-5 / 6.1e-10 / 1.5e-14` at `K = 8/12/16` -- geometric in `K`,
machine precision by `K = 16` at ~20 ms/signature.  The interpolation
tail should admit a Bernstein-ellipse bound (the factors are entire;
the branch maps contract the interval into itself); making that bound
rigorous -- including the conditioning near the `u = +-1/4` factor
zeros -- is the named open step between this packet and a certified
product-profile EMISSION packet.

---

## 4. Theorem C4: the whole symmetric product-profile family

> **Theorem C4.**  For any profile `lambda(w) = prod_j lambda_j(d_j(w))`
> with `lambda_j(1) = lambda_j(-1)`:
> `sum_w lambda(w) e_c(w z) = prod_j (lambda_j(0) +
> 2 lambda_j(1) cos(theta_j(z)))`.

**Proof.**  Lemma 0's digit independence, as in #827 Theorem I; the
symmetric pairing turns `e_c(+-3^j z)` into the cosine. `square`

Verified: random integer profiles at `B = 6`, worst `7.4e-12` against
brute indicator transforms.  The DP of Sec 2-3 generalizes with the
affine factor in place of `2cos(2 pi u)` -- with the INDEX REVERSAL
that C1 dictates: scan step `j` (processing digit `d_j` of `w`)
produces the factor of PROFILE POSITION `B-1-j`, so position-varying
coefficients enter reversed (`a_{B-1-j} + b_{B-1-j} 2cos(2 pi u)` at
step `j`); applying `a_j` at step `j` instead is wrong by O(1)
(verifier-checked on a position-varying profile).  The dense shell is
the constant `a = 0, b = 1` instance (where the reversal is
invisible); bounded-depth product profiles, dense-shell intersections
with cylinders, and smoothed variants are all in scope.

---

## Nonclaims

- **C3 is computed, not certified**: no rigorous interpolation-error
  bound is proved; the convergence pins are exhaustive over the tested
  signature sets only.  No emission rule is added; no payment is made.
- **C5 (shell positivity) is a computed pin** at `B in {6,8}`.
- **Asymmetric profiles** (`lambda_j(1) != lambda_j(-1)`) need the
  complex-exponential factor form -- same structure, not scanned here.
- **Base 3 only, q = 2 rooting only**; floats under exact Parseval +
  Lemma-N guards; the cocycle identity, carry closure, and C4 are
  exact.
- **NOT a reserve payment**: fence (N1) respected.

## Consumers

- **#827 (the shell law)**: its "product-profile emission" residual
  gets its evaluation engine; the transfer-style calculus it gestured
  at (Theorem D(d)) is now the working C1-C4 machinery.
- **The admission chain (#818/#820/#824)**: the omega-cap, budgets,
  and greedy schedule become computable on the canonical non-hierarchy
  family once C3's bound is rigorous.
- **The transverse-charge packet (#776)**: j*'s band data is now
  poly-evaluable (empirically, via C3; it lives in the dense shell).
- `rs_mca_thresholds.tex`: paste-ready remark after the PO4 material --
  "the dense-shell indicator transform is an IFS cocycle in the
  balanced-digit scan; class data of symmetric product-profile bands
  is computed exactly by a carry DP and, in O(B^2 K^2) work, by a
  Chebyshev transfer evaluation with geometric K-convergence
  (computed)" -- visible hypotheses: #749-corrected class, base-3
  chart, q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_product_profile_transfer.py
# -> RESULT: PASS (11/11)
python3 experimental/scripts/verify_product_profile_transfer.py --tamper-selftest
# -> tamper-selftest: caught 5/5
python3 experimental/scripts/verify_product_profile_transfer.py --emit-certificate \
  experimental/data/certificates/product-profile-transfer/product_profile_transfer.json
cd experimental/lean/product_profile_transfer && lake build
# -> Build completed successfully
```
