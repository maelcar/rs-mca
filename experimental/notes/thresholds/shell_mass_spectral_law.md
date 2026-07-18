# The shell-mass spectral law: bimodal concentration, and the dense shell is the first single-shell failing band

## Status

```text
Status: PROVED (I, the shell identity): balanced-digit independence
        (Lemma 0 of #816) gives the generating identity
            sum_xi x^{s3(xi)} e_c(xi z) = prod_i (1 + 2x cos(theta_i(z))),
        hence EXACT digit-shell spectral masses
            sum_{s3(xi)=t} hatf(xi)^2
              = [x^t] sum_{y,y'} N(y) N(y') prod_i (1 + 2x cos(theta_i(y-y'))).
        The chart's spectrum decomposes over digit shells in its own
        product algebra.
      + COMPUTED (R, the shell table): with R_t = shell mass / (c M^2/L)
        (the eta -> 0 failing threshold, U1 normalization), the profile
        is BIMODAL at every computed B -- mass concentrates on the two
        extreme shells with the middle subordinate:
            B      R_sparse(1-2)  R_mid(3..B-2)  R_dense(B-1,B)  R_{s3=B}
            6      0.2396         0.0271         0.7648          0.6851
            8      0.3957         0.0763         0.9581          0.7908
            10     0.5717         0.1702         1.1976          0.9100
            12     0.7664         0.3304         1.4890          1.0457
        This lane's own opening conjecture ("middle shells are
        asymptotically negligible") is contradicted in the computed
        range (the middle share GROWS with B; the asymptotic is OPEN).
        Proper failing shell-UNION bands exist wherever the maximal
        band fails (sparse + dense-pair reaches 1.0044 already at
        B = 6; the dense PAIR {B-1,B} self-suffices from B = 10 at
        1.1976).  The sharp single-shell pin: R_{s3=B} crosses 1 at
        exactly B = 12 (B = 11 stays below at 0.9757) -- the all-dense
        shell is the FIRST SINGLE digit-shell that fails alone.
      + PROVED (D, dense-shell structure): {xi : s3(xi) = B} IS the
        level-B signature set (the full class syndrome cube, 2^B
        points); it CONTAINS the transverse-charge resonant point
        j* = (c-1)/2 (all-ones digits -- the 0.70 M resonance is a
        dense-shell phenomenon); it is NOT hierarchy-measurable at any
        bounded depth (every depth k < B has a split coset); its band
        transform is closed-form,
            sum_{s3(xi)=B} e_c(xi w) = prod_i 2 cos(theta_i(w));
        and wtil-weighted digit sums of PRODUCT profiles
        (lambda(r) = prod_j lambda_j(d_j(r))) factor digit-wise -- the
        tractability seed for band classes BEYOND bounded depth.
LANE: hard input 2 ("image-scale MI + MA, or a direct Sidon payment",
        agents.md L51) -- tenth packet of the arc; RESHAPES the
        non-hierarchy residual: it is not vacuous (the dense shell is a
        canonical genuinely-non-bounded-depth failing band from B = 12)
        but the canonical inhabitant is STRUCTURED (digit-product
        profile, closed-form transform, factorizing digit sums) -- the
        residual LAYERS: extend the emission machinery to product
        profiles (covers the canonical family), with non-product
        non-hierarchy bands the remaining outer layer.  The governing
        profile-payment interface remains OPEN: an actual same-owner
        first-match cell, an (A4) analytic/Sidon payment, a separate (A6)/(RC)
        distinct-slope bound, and a uniform subexponential aggregate census.
        Also open: a grammar rule; product-profile emission (NEW, named here);
        whether asymptotic failure is always extreme-shell-carried (the R_mid
        growth question); atlas totality; and large-q Sidon.  Fence (N1)
        (thm:aperiodic-one-ray-saturation) respected: nothing here pays
        or claims lower reserve.
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**; COMPUTED marks exact
deterministic scans (sibling usage).  The identity and the
structure lemmas are proved; the R-table is exact computation at
`B in {6,8}` in the default verifier run and `B in {10,12}` behind
`--deep` (~13 s).  Verifier:
`experimental/scripts/verify_shell_mass_spectral_law.py` (stdlib only,
deterministic, `RESULT: PASS (13/13)` default / `(17/17)` with `--deep`,
`--tamper-selftest` catches `5/5`, ~1 s default).  Machine-readable
certificate:
`experimental/data/certificates/shell-mass-spectral-law/shell_mass_spectral_law.json`.
Lean statement stub (decidable `native_decide` identities, no `sorry`, no
mathlib): `experimental/lean/shell_mass_spectral_law/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`, base commit `02728b2`;
read, none edited): **`prop:partial-occupancy-fourier` (PO3/PO4)**;
**`thm:aperiodic-one-ray-saturation` (SAT1)**: fence (N1).

Consumed packets on their OWN BRANCHES -- **#816/#818/#820/#824** (OPEN
PRs, NOT yet integrated at base `02728b2`): Lemma 0/N and the class
machinery; every consumed fact is re-derived and re-verified
self-containedly here.  Inline pins: base-3 chart `P_i = 3^i`, `c = 3^B`,
`T = P u (c-P)`, `hatf(xi) = sum_S e_c(-xi Phi(S))`, `N(y) = wtil(s3(y))`,
`M = C(2B,B)`, `L = (c+1)/2`; `theta_i(z) = 2 pi z 3^i / c`.

Integrated in-tree packets (consumed and credited, not reproved):
- **The cylinder packet (#798/#805-corrected)**: U1's failing threshold
  and V7's failing-band decomposition; the R-normalization is U1's.
- **The resonant-folding packet (#779)**: its digit-sparse shell is
  exactly this law's SPARSE mode (the `s3 <= 2` shells); the census ties.
- **The transverse-charge packet (#776)**: its resonant point j* is
  located in the DENSE mode (D).
- **The band-uniform packet (#795)**: narrow-band list certificates
  cover the sparse mode; Sec-4 item 2's structured-family program gets
  the product-profile family (D).
- **Atlas-totality residual**: unchanged by this packet.

---

## 0. Setup

Chart and class machinery as pinned in Interfaces.  The (digit) SHELL at
count `t` is `S_t = {xi : s3(xi) = t}`; shell mass is
`m_t = sum_{xi in S_t} hatf(xi)^2` (excluding `xi = 0`, whose `t = 0`
mass is `M^2`); the failure ratio is `R_t = m_t / (c M^2 / L)` -- by U1
(`c ||h_A||_2^2 = sum_A hatf^2`), a band supported in a shell family `F`
can fail at `eta -> 0` only if `sum_{t in F} R_t >= 1`.  (Convention:
`R` here is the MASS ratio, i.e. the SQUARE of #795's linear norm ratio
`R_A` -- `R_total(6) = 1.0315 = R_A(6)^2` with `R_A = 1.01563` -- the
two packets' "R"s differ by exactly this square.)

---

## 1. Theorem I: the shell identity

> **Theorem I.**  `sum_xi x^{s3(xi)} e_c(xi z) =
> prod_{i<B} (1 + 2x cos(theta_i(z)))` for every `z`; consequently the
> shell masses are the `x`-coefficients of
> `sum_{y,y'} N(y) N(y') prod_i (1 + 2x cos(theta_i(y-y')))`.

**Proof.**  By Lemma 0 the map `xi <-> (d_0,...,d_{B-1})` (balanced
digits) is a bijection, and `xi = sum d_i 3^i` makes `e_c(xi z) =
prod_i e_c(d_i 3^i z)` with `x^{s3(xi)} = prod_i x^{[d_i != 0]}`: the sum
factors digit-by-digit into `1 + x(e_c(3^i z) + e_c(-3^i z))`.  The mass
form follows from `hatf(xi)^2 = sum_{y,y'} N(y)N(y') e_c(xi(y - y'))`
and swapping sums. `square`

Verified: the generating identity at random `z`, `B in {6,8}` (worst
`4.0e-11`); the mass consequence exactly at `B = 6` (worst relative
`9.2e-14`).  The identity is the chart's own per-pair product evaluated
at difference signatures -- the spectrum's shell decomposition lives in
the same product algebra as `hatf` itself.

---

## 2. The shell table: bimodal, with a crossing at B = 12

Computed exactly (default `B in {6,8}`, `--deep` for `{10,12}`): the
Status-block table.  Findings, stated honestly:

- **Bimodal at every computed B**: `R_mid < R_sparse < R_dense`
  (checked); per-element middle mass is smaller still (the middle
  shells hold most of `Z_c` by count).
- **This lane's opening conjecture fails in the computed range**:
  `R_mid` GROWS (0.027 -> 0.076 -> 0.170 -> 0.330); whether asymptotic
  failure is extreme-shell-carried remains OPEN (Nonclaims).  What is
  true at every computed `B`: a failing band's middle-shell mass
  fraction is at most `R_mid` of threshold -- subordinate, not
  negligible.
- **Proper failing UNION bands are not new to B = 12**: by the
  criterion above (equality for full shell unions), sparse + dense-pair
  fails already at `B = 6` (`0.2396 + 0.7648 = 1.0044`) and the dense
  PAIR `{B-1, B}` self-suffices from `B = 10` (`1.1976`).
- **The single-shell crossing**: `R_{s3=B}` = 0.685 / 0.791 / 0.910 /
  1.046 -- the all-dense shell alone crosses at `B = 12`, and no single
  shell fails alone below it (`B = 11`: 0.9757).  At `B = 6` even the
  full spectrum only reaches 1.03: failure is near-total there, the
  quantitative form of cylinder-V7's "the failing maximal band".  The
  sparse mode also trends up (0.240 -> 0.766), heading toward its own
  crossing (computed trend, no claim).

---

## 3. Theorem D: the dense shell is structured

> **Theorem D.**  (a) `S_B = {xi : s3(xi) = B}` is exactly the level-B
> signature set `{sum_t eps_t 3^t : eps in {+-1}^B}` (2^B points); it is
> SYMMETRIC (`-xi` negates digits, preserving `s3`) and excludes `0` --
> a legitimate house band -- and `j* = (c-1)/2 in S_B` (all-ones
> digits).  (b) `S_B` is NOT
> hierarchy-measurable at any bounded depth: for every `k < B` some
> coset mod `3^k` meets both `S_B` and its complement.  (c) Its band
> transform is closed-form: `sum_{xi in S_B} e_c(xi w) =
> prod_i 2 cos(theta_i(w))`.  (d) For any PRODUCT profile
> `lambda(r) = prod_j lambda_j(d_j(r))` on `Z_3^k`, the wtil-weighted
> digit sums factor:
> `sum_a prod_j lambda_j(d_j(a)) x^{s3(a)} =
> prod_j (lambda_j(0) + x(lambda_j(1) + lambda_j(-1)))`.

**Proof.**  (a) `s3 = B` forces every digit in `{+-1}`; Lemma 0.
`j* = sum_i 3^i`.  (b) Fix `k < B` and take the coset of
`r = j* mod 3^k` (fixed low digits all-ones): it contains `j*` itself
(a member) and `r` itself, whose high digits are all zero (a
non-member, since `s3(r) = k < B`) -- a split coset at every depth.
(Note the SUBGROUP coset `r = 0` is memberless -- its low digits
vanish -- and so witnesses nothing; the witness must have an
all-nonzero fixed part.)  (c) is the `[x^B]`-coefficient of Theorem
I's identity: only the `2x cos` term survives in every factor.
(d) digit independence again (Lemma 0), as in Theorem I. `square`

**Reading.**  The first single-shell failing band is not adversarial
-- it is the class machinery's own signature cube, digit-defined, with
a product-form transform.  "Non-hierarchy" (no bounded depth) does NOT
mean "unstructured": `S_B` is the depth-`B` band with the PRODUCT
profile `prod_j [d_j != 0]`, and (d) is the seed of a transfer-style
calculus for such profiles (their G-analogues are EXPECTED to factor
digit-wise -- gestured, not built here).  The residual program LAYERS:
product-profile emission first (the canonical family), non-product
non-hierarchy bands beyond.

---

## Nonclaims

- **No asymptotic exclusion**: the middle-shell share grows with `B`
  in the computed range; whether asymptotic failure is always
  extreme-shell-carried is OPEN and named as such.
- **The R-table is exact computation at B <= 12**, not an asymptotic
  law; `--deep` carries `B in {10,12}` (~13 s), the default run
  `B in {6,8}`.
- **No emission rule for product profiles is built here**; (d) is the
  factorization seed only.  The dense shell's failing-band status at
  `B >= 12` sharpens the residual, it does not pay anything.
- **Base 3 only, q = 2 rooting only**; floats under the exact
  Parseval + Lemma-N guards;
  the identity, set equalities, and factorization are exact.
- **NOT a reserve payment**: fence (N1) respected.

## Consumers

- **The non-hierarchy residual (all prior packets' Nonclaims)**: now
  has a canonical single-shell inhabitant (S_B from B = 12; proper
  failing UNIONS exist from B = 6) AND a structure theory seed; the
  next question is precise (product-profile emission), with non-product
  bands the outer layer.
- **The resonant-folding packet (#779)**: its digit-sparse shell is the
  sparse mode of a two-mode law; the modes are now jointly quantified.
- **The transverse-charge packet (#776)**: j* is a dense-shell point;
  the resonance and the first single-shell failing band co-locate.
- **The admission lane (#818/#820/#824)**: the greedy machinery's next
  target class is named (product profiles); the dense shell is its
  mandatory instance.
- `rs_mca_thresholds.tex`: paste-ready remark after the PO4 material --
  "spectral mass on the base-3 chart obeys an exact digit-shell
  decomposition in the chart's own product algebra; it is bimodal, and
  the all-dense shell -- the level-B signature cube, containing the
  resonant point -- becomes a self-sufficient proper failing band at
  B = 12" -- visible hypotheses: #749-corrected class, base-3 chart,
  q=2 rooting.

## Reproducibility

```bash
python3 experimental/scripts/verify_shell_mass_spectral_law.py
# -> RESULT: PASS (13/13)
python3 experimental/scripts/verify_shell_mass_spectral_law.py --deep
# -> RESULT: PASS (17/17)   (~17 s; adds the B in {10,11,12} rows + the dense-pair crossing)
python3 experimental/scripts/verify_shell_mass_spectral_law.py --tamper-selftest
# -> tamper-selftest: caught 5/5
python3 experimental/scripts/verify_shell_mass_spectral_law.py --emit-certificate \
  experimental/data/certificates/shell-mass-spectral-law/shell_mass_spectral_law.json --deep
cd experimental/lean/shell_mass_spectral_law && lake build
# -> Build completed successfully
```
