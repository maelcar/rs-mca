# The non-fiber-indexed decomposition at realized-image scale: #739 kills concentration at BOTH scales, and image-class (coset) indexing is a coarser quotient chart that hits the same abundance — a route-scoped negative

## Status

```text
Status: PROVED (rung a) that the #739 Sidon-paired counterexample kills the
        decomposition's concentration clause at BOTH the ambient AND the
        realized-image (PO5) scale -- the realized scale is the concentration-
        FAVORABLE one (smallest admissible denominator) and is still killed.
      + PROVED (rung c, structural) that an image-class (G_lambda-coset) split is
        EXACTLY the fiber partition of the quotient chart q_H o Phi, so it is NOT
        a genuinely new (non-fiber) object; #732 Theorem A keeps all four charge
        conditions FREE for it (partition-agnostic duality).
      + PROVED (rung c) a prime-field depth-1 DEGENERACY: over F_p (p in
        {7,11,13}) the additive image group has no proper nontrivial subgroup, so
        image-class indexing offers only the two useless extremes {fibers, one
        piece} -- there is no nontrivial coset candidate to try.
      + COUNTEREXAMPLE (rung c, the DECISION): where a nontrivial coset split
        DOES exist (composite modulus 3^B, char-2, or depth >= 2), the
        count-vs-structure product is conserved -- a mod-3^j coarsening carries
        ZERO semantic (single-unpaired-level) charge for every #pieces < 3^{B-2},
        with the first semantic mass at 3^{B-2} and full resolution at 3^{B-1},
        both e^{Theta(N)}.  So no subexponential image-class split carries any
        semantic charge: it HITS the #739 abundance mechanism identically.
LANE: hard input 2 -- the NON-fiber-indexed route to avdeevvadim's #716
        charge-preserving semantic-or-signed decomposition, left open after the
        fiber-indexed route was cut on the Sidon-paired class (#739) and the
        per-fiber emission grammar closed (#735).  Reframed by (N1)
        thm:aperiodic-one-ray-saturation (a heavy fiber can collapse to one slope
        -- emission does NOT pay lower reserve) and (N2) the PO5 realized-image
        renormalization (profile-envelope comparison packet, PR #759).
Verdict per rung (route-scoped):
  (a) WHICH SCALE DOES #739 KILL?  BOTH.  #732 Thm B.2's concentration threshold
      is barN = M/D with the average taken over D cells; PO5 fixes the correct
      denominator to the realized-image group and warns L = |Phi(Omega^0)| may be
      strictly below it: L <= |G_lambda| <= |ambient G|.  #739's own threshold
      M/L already uses the realized image L = (3^B+1)/2 -- the SMALLEST admissible
      denominator, hence the LARGEST mean and the FEWEST heavy fibers.  Heavy
      counts obey heavy_realized <= heavy_group <= heavy_ambient (exact), and the
      favorable heavy_realized is STILL e^{Theta(N)}.  For base 5^i an exponential
      effective-image collapse c/L = (5/3)^B (the PR #759 phenomenon, genuinely
      present) inflates the realized mean, yet the heaviest fiber still exceeds it
      by an exponential factor -- the banked collapse benefit is quantitatively
      insufficient.  Realized-scale renormalization does not rescue this class.
  (c) DOES IMAGE-CLASS INDEXING EVADE THE ABUNDANCE?  NO -- it hits it
      identically.  Coset(H)-indexing = fibers of q_H o Phi (a coarser prefix/
      quotient chart); charges stay free (Thm A); over prime fields at depth 1
      the split is degenerate; where nontrivial, subexponential #pieces forces
      heterogeneous, non-emitting classes (0 semantic charge below 3^{B-2}).
```

Label key (agents.md dialect): **PROVED** / **CONDITIONAL** / **CONJECTURAL** /
**EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**.  Every integer below is
recomputed with exact `int`/`Fraction`/`F_p`/`F_2^k` arithmetic by
`experimental/scripts/verify_nonfiber_decomposition_realized_scale.py` (stdlib
only, deterministic, `RESULT: PASS (90/90)`, `--tamper-selftest` catches `3/3`,
< 0.3 s).  No enumeration is silently capped; every printed cap is explicit.
Machine-readable certificate:
`experimental/data/certificates/nonfiber-decomposition-realized-scale/nonfiber_decomposition_realized_scale.json`.
Lean statement stub (decidable `native_decide`, no `sorry`, no mathlib):
`experimental/lean/nonfiber_decomposition_realized_scale/` (`lake build`
succeeds).  No `.tex`/`.pdf` is edited.

## Interfaces

Paper labels (`experimental/rs_mca_thresholds.tex`,
`experimental/asymptotic_rs_mca_frontiers.tex`, base commit `c35a6da`; read, none
edited):
- **`rem` PO5 (effective normalization of a partial-occupancy slice)**
  (thresholds L3527--3553): fixes the correct Fourier denominator to the
  realized-image group `G_lambda = <Phi(S) - Phi(S_0) : S in Omega_lambda>` and
  states it "does not assert that the realized image fills the affine group."
  This is the exact ambient-vs-realized distinction rung (a) evaluates.
- **`eq:profile-envelope` (1.6)** and the realized-image-scale definition
  (frontiers L855--893): `barN_lambda = |Omega_lambda| / L_lambda`,
  `L_lambda = |Phi(Omega_lambda)|` (realized, not codomain); `(FI)`
  `L_lambda >= e^{-o(n)} A_lambda`; and the *effective-image collapse* notion.
  The realized-image scale of the concentration threshold is exactly this
  `L_lambda`.
- **`thm:aperiodic-one-ray-saturation` (SAT1)** (thresholds, sec:further-exact;
  and `aperiodic_one_ray_saturation.md`): a heavy aperiodic prefix fiber can
  project to ONE slope, so emission does not by itself supply lower reserve.
  Respected as fence (N1): no rung here pays reserve via emission.
- **`prop:partial-occupancy-fourier` (PO3/PO4)** and
  **`thm:exact-partial-occupancy` (PO1/PO2)** (thresholds, sec:quotient-
  obstruction): support add-back is unconditional; a finite flatness theorem is
  exactly a bound for the nontrivial-character sum -- the analytic residual the
  surviving open object (sec 7) points at.
- **`thm:unconditional-support-envelope-bracket` (SB1--SB4)** (thresholds
  L3720--3759): the finite `L/P/U` bracket; the identity term is `L(a)`.
- The three proved barriers **`prop:pairwise-overlap-limit`**,
  **`drc:prop-recurrence-nonadditive`**, **`prop:no-growing-prime-density`** --
  none re-attempted.

Integrated in-tree packets (consumed and credited, not reproved):
- **avdeevvadim's #716**
  (`experimental/notes/audits/primitive_signed_payment_barrier_v1.md`): the whole
  target -- the charge-preserving semantic-or-signed dichotomy (Sec 6), its
  "at most `e^{o(N)}` rooted packets" clause, and **Prop 6.1** (a failure forces
  `e^{o(N)}` semantic packets carrying `(1-o(1)) Omega_+`).  This packet studies
  whether a NON-fiber-indexed partition can meet that count on the Sidon-paired
  class.
- **#732** (`charge_preserving_split_decomposition.md`): **Theorem A** (fourth
  charge condition free for ANY partition of a positive-rooted packet -- the
  duality bound `c_i <= ||P_A b_{U_i}||_q`, `g` feasible) and **Theorem B.2**
  (the fiber-indexed split realizes #716 iff staircase-concentration) are the
  exact statements rungs (a) and (c) build on.  Theorem A is what makes coset
  charges free (sec 4).
- **#739** (`staircase_concentration_sidon_paired.md`): the exact fiber staircase
  `|Phi^{-1}(sigma)| = C(B-s,(B-s)/2)` with `C(B,s) 2^s` syndromes at
  unpaired-count `s`, and the COUNTEREXAMPLE `#{fiber >= e^{eta N} M/L} =
  e^{Theta(N)}` that cut the fiber-indexed route.  Its threshold `M/L` uses the
  realized image `L = (3^B+1)/2`; rung (a) shows this is already the PO5 scale.
  Its hypotheses were **DannyExperiments-corrected (#749)** to 2-dissociated `P`
  with `c > 2 sum P`; this packet consumes the corrected statements only.
- **#735** (`heavy_fiber_planted_emission.md`): the five-precursor grammar and
  the per-fiber emission census over `F_p` (`p in {7,11,13}`); rung (c)'s
  census reuses its `prec_saturation`/`prec_planted` tests verbatim, and its
  corrected **Thm 2a** central fiber is the `s=0` staircase slice.
- **#729** (`general_pruned_signed_bound.md`): the density criterion
  `q_+ = 1/(3/2 - logM/logL) = 4.199` and the layer-cake; the signed clause the
  surviving open object (sec 7) proposes routing the moderately-unpaired fibers
  through.
- **#717** (`heavy_fiber_admissibility_transfer.md`): the depth-R locator/power-
  sum prefix chart and Johnson bound; **#725** (`c3_planted_divisor_census.md`):
  the `sigma(p-1)` coset census (the semantic coarsenings that DO exist are its
  coset-unions, sec 6).
- **The profile-envelope comparison packet (PR #759)**
  (`profile_envelope_target_comparison.md`, integrated in the same `2633895a`
  wave): its exact finite full-codomain deficit for the identity map on a smooth
  coset `D = theta H` is the (N2) reframing that motivates rung (a).  This is not
  an asymptotic `(FI)` conclusion.  Rung (a)'s proof is independent of #759 (the
  Sidon-paired realized images are computed exactly here).

Classical facts used by name: distinct-subset-sum / `B[+-2]`-dissociativity
(#739); the additive group `(Z/pZ, +)` of prime order is simple; a subgroup
`H <= G` and its quotient `q_H : G -> G/H` make `{S : Phi(S) in gH}` the fiber of
`q_H o Phi` over `q_H(g)`.

---

## 1. The decomposition obligation at realized-image scale (rung a, PROVED setup)

A positive-rooted failure packet `b_+` on chart `Phi` has the norming dual `g`
(`||g||_{q'}=1`), pointwise owner weights `omega_s = Re conj((P_A g)(s)) > 0`, and
positive charge `Omega_+ = sum_{s: omega_s>0} f(s) omega_s` (#716 Sec 2 / #732
Sec 1).  Write `f(sigma) = |Phi^{-1}(sigma)|`, `M = |Omega^0|`, `N = |T|`.

**The obligation (#732 Thm B.2).** The fiber-indexed heavy/light split realizes
#716 Sec 6's "at most `e^{o(N)}` packets" (and hence Prop 6.1) **iff** there is a
threshold `T_h` with

```text
   #{sigma in b_+ : f(sigma) >= T_h} = e^{o(N)}   AND
   max{f(sigma) : sigma in b_+, f(sigma) < T_h} = e^{o(N)},
```

equivalently, on the profile `f`: for every fixed `eta > 0`,

```text
   #{ sigma : f(sigma) >= e^{eta N} * barN }  =  e^{o(N)},      barN = M / D,   (CONC)
```

where `barN` is the average fiber and `D` is the number of cells the `M` supports
are averaged over.

**What is `D`? The PO5 question.** `rem` PO5 fixes the correct Fourier
denominator to the realized-image group `G_lambda = <Phi(S)-Phi(S_0)>` and warns
that the realized image `L = |Phi(Omega^0)|` (the number of NONEMPTY fibers,
`= L_lambda` of `eq:profile-envelope`) may be strictly below it. So there are
three nested normalizations, with **PO5 normalization on both the syndrome-count
and the fiber-average sides**:

```text
   D_realized = L            (realized image = # nonempty fibers; #759's L_lambda)
   D_group    = |G_lambda|                                                       (>= L)
   D_ambient  = |G|          (codomain, e.g. Z_c or the integer range)     (>= |G_lambda|)
```

Because `L <= |G_lambda| <= |G|`, the means and thresholds are ordered
`barN_realized >= barN_group >= barN_ambient`, so

```text
   heavy_realized  <=  heavy_group  <=  heavy_ambient,                            (ORD)
```

i.e. the **realized-image scale gives the FEWEST heavy fibers** -- it is the
concentration-FAVORABLE normalization.  `(N2)`'s "renormalization moves both
sides" is exactly the move `D_ambient -> D_realized`, which raises the threshold.

---

## 2. Which scale does #739 kill? BOTH (rung a, PROVED / COUNTEREXAMPLE)

For the Sidon-paired chart (`T = P u (c-P)`, `c = 2 sum P + 1`, `a = B`), the
realized image is intrinsic and base-independent:

```text
   L = |Phi(Omega^0)| = (3^B+1)/2,       M = C(2B,B).
```

The realized image is strictly below the ambient (verified `L < |G_lambda| = c <=
range`), and the collapse index depends on the base:

| base | `c = 2 sum P + 1` | `L` (`B=8`) | `c/L` (`B=8`) | collapse index `c/L` |
|------|-------------------|-------------|---------------|----------------------|
| `3^i` | `3^B` (`= 2L-1`)  | `3281`      | `6561/3281`   | `-> 2` (BOUNDED) |
| `5^i` | `(5^B+1)/2`       | `3281`      | `195313/3281 = 59.53` | `= (5/3)^B` (EXPONENTIAL) |

So for `5^i` an **exponential effective-image collapse IS present** -- the
realized image fills only `(3/5)^B` of `G_lambda = Z_c` -- exactly PR #759's
phenomenon, on this additive chart.

**Heavy counts at the three scales** (heaviness ratio `>= 2`, i.e.
`f(sigma) * D >= 2M`, exact integers):

```text
   B      heavy_realized (D=L)     heavy_group (D=c)      heavy_ambient (D=range)
   4            1                     25 (3^i)/41 (5^i)        41
   6           61                     61 (3^i)/365 (5^i)      365
   8          113                   1233 (3^i)/3281 (5^i)    3281
```

`heavy_realized = 1, 61, 113` is **base-independent** (both `L` and the fiber
profile are intrinsic) and **grows exponentially** (#739's exact
`#{f >= e^{eta N} M/L} = e^{Theta(N)}`, `eta in (0, ln(3/2)/2)`), while
`(ORD)` `heavy_realized <= heavy_group <= heavy_ambient` holds at every row.

**Collapse present but insufficient (`5^i`).** The heaviest fiber is
`maxfiber = C(B,B/2) = 70` at `B=8`.  Even at the concentration-favorable
realized scale it is heavy: `maxfiber * L = 229670 >= 2M = 25740`
(`maxfiber / (M/L) = 17.85` at `B=8`), while at the ambient scale
`maxfiber / (M/c) = 1062`.  The collapse inflates the realized mean by the factor
`c/L = (5/3)^B`, but the heaviest fibers `~ 2^B` outrun even the inflated
threshold `M/L`.

> **Decision (rung a, route-scoped).** #739 kills the concentration clause at
> **BOTH** the ambient and the realized-image scale.  Its own threshold `M/L`
> already normalizes by the realized image `L=(3^B+1)/2` (the PO5 `L_lambda`, the
> smallest admissible denominator), so it is the tight/favorable case; ambient
> normalization only lowers the threshold `(ORD)` and kills harder.  The PR #759
> rescue mechanism -- an exponential effective-image collapse inflating the mean
> -- is genuinely present for `5^i` but is banked into `M/L` already and is
> quantitatively insufficient.  So realized scale is killed: proceed to rung (c).

---

## 3. The non-fiber-indexed candidate = a coarser quotient chart (rung c, PROVED)

The proposed non-fiber object is: **decompose by realized-image classes, i.e. by
cosets of a subgroup `H <= G_lambda`**, instead of by prefix fibers.  For a
support `S` assign it to the class of `Phi(S)` in `G/H`.

**Structural identity.** For a subgroup `H <= G` with quotient `q_H : G -> G/H`,
```text
   { S : Phi(S) in gH }  =  { S : (q_H o Phi)(S) = q_H(g) }  =  (q_H o Phi)^{-1}(q_H(g)),
```
so an image-class (coset) split **is exactly the fiber partition of the coarser
chart `q_H o Phi`**.  It is a *coarsening* of the fiber chart, never an escape
from it (verified: each mod-`3^j` class of the Sidon-paired chart is the disjoint
union of the integer fibers hitting that residue, mass-conserving,
`m in {3,9,27,81}`).  Coarsening merges fibers, so class sizes only grow; the
extremes are `H = {0}` (the fibers themselves, the #739 staircase) and `H = G`
(one piece = the whole packet).

---

## 4. Charge-preservation for an image-class split (rung c, PROVED; #732 Thm A extends)

**#732 Theorem A is partition-agnostic**: for a positive-rooted packet with
norming dual `g`, ANY partition `{U_i}` of its support with natural charges
`c_i = sum_{S in U_i} omega(S)` and the common band `B_i = A` satisfies all four
#716 charge conditions, the fourth (`c_i <= ||P_A b_{U_i}||_q`) FREE by the single
duality inequality (`g` feasible).  A coset partition is a partition, so:

> **Charge-preservation condition (image-class split).** For any subgroup
> `H <= G_lambda`, the `H`-coset partition `U_i = {S : Phi(S) in coset_i}` with
> natural charges `c_i = sum_{S in U_i} omega(S)` and band `A` satisfies
> `(C1) c_i >= 0`, `(C2) sum c_i = Omega_+`, `(C3) c_i = sum omega(S)`,
> `(C4) c_i <= ||P_A b_{U_i}||_q` -- the fourth condition is free.

Verified exactly at `q=2` over `F_2^6` (`H = 64`, band `|A|` moment-parity) with
the subspace-coset partition `q_H(s) = s & ~0b000111` (4 cosets of the
positive-rooted support): `(C1)` and `(C4)` hold on every coset with strict slack
(`min ||P_A b_i||_2^2 ||h||_2^2 - c_i^2 ||h||_2^2 = 6531875436 > 0`), and `(C2)`
`sum c_i = Omega_+` exactly.  **So charge is NOT the obstruction for image-class
splits either** -- exactly as for the fiber split.  What can fail is, again, the
per-piece semantic-or-signed classification and the piece count.

---

## 5. Prime-field depth-1 degeneracy (rung c, PROVED)

Over a **prime** field `F_p` at depth 1 the additive image group `(F_p, +)` is
cyclic of prime order, so its only subgroups are `{0}` and `F_p` (verified: the
only divisors of `p in {7,11,13}` are `1` and `p`). Hence the ONLY image-class
(coset) decompositions are the two useless extremes:

```text
   H = {0}   -> the fibers (the #739 staircase: exponentially many pieces),
   H = F_p   -> one piece (the whole packet: not a decomposition).
```

There is **no nontrivial image-class candidate to try** over the emission-census
fields at depth 1.  (By contrast the composite modulus `3^B` -- verified `>= 4`
proper nontrivial subgroups at `B=6` -- and char-2 `F_2^6` DO carry nontrivial
subgroups, which is where a genuine coset split can even be posed, and where
sec 6's abundance argument then bites.)  So the non-fiber route is not merely cut
but often *unformable* at the census scale of the emission work.

---

## 6. Abundance recurs: the count-vs-semantic conservation (rung c, COUNTEREXAMPLE)

Where a nontrivial coset split exists (modulus `3^B`), coarsening trades piece
count against per-piece structure at a **conserved product**.  Index the
Sidon-paired supports by unpaired-count `s` (the "signed" pairs); the fiber at `s`
has size `C(B-s,(B-s)/2)` and there are `C(B,s) 2^s` syndromes at level `s`
(#739).  A coset-piece is **semantic-candidate** only if it is *homogeneous* --
supported on a single unpaired-level `s` (a union of like-structured fibers);
a piece spanning several levels `s` is a heterogeneous union of fibers of
different sizes and different Johnson agreement, hence neither a single planted
template nor a single ray-saturation profile (the #735 precursors), so it emits
nothing.

**Exact mod-`3^j` census (base `3^i`), fraction of the `M` supports in
single-unpaired-level (semantic-candidate) coset classes:**

```text
   B=8 (L=3281, M=12870):
     modulus 3^j :  1    3    9   27   81  243   729  2187  6561
     #pieces     :  1    3    9   27   81  243   729  2187  3281
     semantic %  :  0%   0%   0%   0%   0%   0%  49.2% 100%  100%
   B=6 (L=365, M=924):
     modulus 3^j :  1    3    9   27   81  243   729
     #pieces     :  1    3    9   27   81  243   365
     semantic %  :  0%   0%   0%   0%  48.5% 100% 100%
```

The first positive semantic mass appears exactly at modulus `3^{B-2}`
(`#pieces = 3^{B-2}`) and full resolution at `3^{B-1}` -- **both `e^{Theta(N)}`**
(`N = 2B`; the crossover `3^{B-2}` is super-polynomial, `3^58 > 60^12` at
`B=60`).  Hence:

> **Decision (rung c, route-scoped COUNTEREXAMPLE).** For every image-class
> (coset) split with **subexponential** piece count (`#pieces < 3^{B-2}`), the
> classes carry **zero** semantic (single-unpaired-level) charge; the semantic
> charge is `100%` only once `#pieces` reaches `3^{B-1} ~ L = e^{Theta(N)}`.  So
> no subexponential image-class split places any of the charge `Omega_+` on
> semantic pieces, and Prop 6.1's "`e^{o(N)}` semantic packets carrying
> `(1-o(1)) Omega_+`" fails on this class -- **identically to the fiber-indexed
> case**.  Image-class indexing does NOT evade the Sidon-paired abundance
> mechanism; it relabels it (the semantic-piece count IS the #739 max-fiber
> count).

Confirmed at census scale on the emission families too: coarsening a depth-2
`F_p` chart to depth-1 (forgetting `p_2`, `p in {7,11}`) yields `7,7,11,11`
coset-pieces that emit NONE of {planted, saturation} -- every coarse class is a
heterogeneous union (`emit_none = #pieces`).  The only coarsenings that *are*
semantic are the multiplicative coset-unions of #735 Thm 3 / #725 (`sigma(p-1)`
census), but those form a single deep fiber, not a decomposition of the whole
packet.

---

## 7. The surviving open object (rung d, OPEN, route-scoped)

> **(NFB)** Whether the moderately-unpaired fibers (`s = Theta(B)`) of the
> Sidon-paired chart can be discharged by a partition **transverse to every
> prefix-quotient fiber** (a non-`q_H o Phi` split), or paid **without any
> semantic decomposition** by the #729 signed clause / `prop:partial-occupancy-
> fourier` (PO4) nontrivial-character bound at `q <= q_+ = 4.199`.

This narrows #739 Sec 5's open branch ("a DIFFERENT, non-fiber-indexed
decomposition, e.g. routing the moderately-unpaired fibers through the signed
clause"): **every GROUP-COSET / image-class partition is a coarser fiber chart
and is now cut** (secs 3--6), and every fiber-indexed partition was cut by #739,
so the only decomposition candidates left are genuinely transverse (non-quotient)
partitions -- or no decomposition at all, i.e. a direct analytic PO4/signed
payment.  By fence (N1) that payment must be established WITHOUT inferring lower
reserve from emission (a heavy fiber can one-ray-saturate,
`thm:aperiodic-one-ray-saturation`).

## Nonclaims

- **NOT** a proof or refutation of #716's dichotomy.  Rung (a) confirms the
  fiber route stays cut at realized scale; rung (c) cuts the image-class/coset
  sub-route; the transverse / direct-signed route (sec 7) is untouched.
- **NOT** a new floor, primitive-Q / max-fiber flatness, A4, the signed
  minor-arc/Sidon inverse, or the Proximity Prize.
- The PO5 denominator `|G_lambda|` and the realized image `L` differ (the image
  need not fill `G_lambda`; verified exponentially for `5^i`); the concentration
  threshold uses `L` (# nonempty fibers), the smaller, favorable denominator.
  Both are killed either way `(ORD)`.
- Rung (a)'s decision is UNCONDITIONAL (exact Sidon-paired realized images).
  The `(N2)` framing via integrated PR #759's exact finite full-codomain deficit
  is used only as motivation, not in any proof; it is not an asymptotic `(FI)`
  conclusion.
- The abundance census (sec 6) is exhaustive for `B <= 8` (Sidon) and the
  depth-2 `F_p` families `p in {7,11}`; the `3^{B-2}`/`3^{B-1}` crossovers and the
  `(3^B+1)/2` scale are closed-form, tabulated by the verifier.
- Charge conditions verified exactly at `q=2` over `F_2^6`; the duality proof
  (Thm A) is `q`-agnostic and per #732.

## Consumers

- **#716** (`primitive_signed_payment_barrier_v1.md` Sec 6 / Prop 6.1): the
  image-class (coset) family of non-fiber decompositions is decided negatively on
  the Sidon-paired class -- it is a coarser quotient chart carrying no semantic
  charge below an exponential piece count.  The residual is relocated to the
  transverse / direct-PO4-signed payment (sec 7).
- **#732** (`charge_preserving_split_decomposition.md`): its Theorem A is shown
  partition-agnostic down to coset partitions (charge stays free); its Prop 3.1
  cardinality obstruction is shown scale-invariant (rung a) and coarsening-
  invariant (rung c).
- **#739** (`staircase_concentration_sidon_paired.md`): its `M/L` threshold is
  identified as the PO5 realized-image scale; its non-concentration is shown to be
  the FAVORABLE-scale statement, so the ambient scale is killed a fortiori.  Its
  Sec 5 open branch is narrowed to the transverse/signed route.
- **#735** (`heavy_fiber_planted_emission.md`) / **#725**
  (`c3_planted_divisor_census.md`): the only semantic coarsenings are their
  multiplicative coset-unions (single deep fiber, `sigma(p-1)` census), not a
  whole-packet decomposition.
- **profile-envelope comparison packet (PR #759, integrated in wave
  `2633895a`)**: rung (a) supplies the additive-chart companion to its exact
  finite smooth-coset full-codomain deficit -- on the Sidon-paired chart the
  collapse is present (`5^i`) but insufficient for concentration.  The link is
  motivational only; this packet's proof is independent of #759.
- `asymptotic_rs_mca_frontiers.tex` / `rs_mca_thresholds.tex`: paste-ready as the
  remark after the decomposition proposition and PO5 -- image-class normalization
  does not create a new decomposition; the open input is the transverse/signed
  payment, stated with visible hypotheses.
- Lean statement stub: `experimental/lean/nonfiber_decomposition_realized_scale/`
  (prime-field divisor degeneracy; realized `< ` ambient with bounded/exponential
  collapse index; collapse-insufficiency `maxFiber * L > 2M`; the exponential
  `3^{B-2}` abundance crossover; statements only, `lake build` succeeds).

## Reproducibility

```bash
python3 experimental/scripts/verify_nonfiber_decomposition_realized_scale.py
# -> RESULT: PASS (90/90)
python3 experimental/scripts/verify_nonfiber_decomposition_realized_scale.py --tamper-selftest
# -> tamper-selftest: caught 3/3 ; then RESULT: PASS (90/90)
cd experimental/lean/nonfiber_decomposition_realized_scale && lake build
# -> Build completed successfully
```
