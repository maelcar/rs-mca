# Character-frame hypothesis audit vs frontiers tex

## Status

`AUDIT`. Adversarial mathematical-hypothesis audit of the primitive-profile
character-frame certificate (**avdeev, PR #558**, integrated at `e190193`),
against its intended consumer `experimental/asymptotic_rs_mca_frontiers.tex`.
Deliverable requested in the maintainer's agents-log: audit the hypotheses
before moving any statement into the frontiers manuscript. Every number in
this note is recomputed by
`experimental/scripts/verify_character_frame_audit.py` (exit 0 iff all pass).

Audited objects (all at worktree root):
`experimental/notes/thresholds/asymptotic_primitive_profile_character_frame_v1.md`,
`experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py`,
`experimental/data/certificates/primitive-profile-character-frame/primitive_profile_character_frame_v1.json`.
Inventory below is built directly from the note (independent of the sibling
compiler-hypothesis visibility audit, LegaSage #572).

Label key. Author status is quoted verbatim where it exists; the audit
verdict uses the maintainer vocabulary **NO ISSUE / FIXED / OPEN GAP /
COUNTEREXAMPLE_NEW_FLOOR**, and a proof-status tag **PROVED / MEASURED /
OPEN** is attached to every claim.

---

## Rung 1 - Claim inventory

The note carries one status header,
`PROVED CONDITIONAL CERTIFICATE / OPEN SOURCE-SPECIFIC PACKING INPUT`, and the
following distinct mathematical claims. `M=|Omega|=binom(|T|,m)` (full slice),
`S=image`, `L=|S|`, `barN=M/L`, `G=V_g`, `|G|=A_eff`.

| id | statement | hypotheses (visibility) | author tag | proof-status | verdict |
|----|-----------|-------------------------|------------|--------------|---------|
| C1 | (CF1) `\|F_z\| <= M \|\|K_A\|\|_op/\|A\| = (L\|\|K_A\|\|_op/\|A\|)barN` | A nonempty subset of `G^`; profile constant on each fiber. Visible. | proved | PROVED | NO ISSUE |
| C2 | proof identities `<v_g,v_g'>=hat_mu(g'g^-1)`, `\|<u_z,v_g>\|^2=\|F_z\|/M`, `\|\|T\|\|^2=\|\|K_A\|\|_op` | unit-vector/Gram/Bessel; visible | proved | PROVED | NO ISSUE |
| C3 | (CF2)`=>`exact primitive-profile Q (image-normalized) | requires (CF2): `\|A\|>=exp(-o(N))L` and `\|\|K_A\|\|_op<=exp(o(N))`. Implication visible; (CF2) itself is the open input. | conditional | PROVED (implication) | NO ISSUE |
| C4 | (CF3) `\|\|K_A\|\|_op >= \|A\| mu(z)`; `L\|\|K_A\|\|_op/\|A\| >= L max_z mu(z)` | Rayleigh test vector at `z`; visible | proved | PROVED | NO ISSUE |
| C5 | full-dual identity `\|\|K_{G^}\|\|_op = \|G\| max_z mu(z)` | whole dual `A=G^`; visible | proved | PROVED | NO ISSUE |
| C6 | (CF4) greedy independent set `\|A\| >= \|G^\|/\|Mfrak\|` | `Mfrak` symmetric, contains identity; Cayley-graph degree bound; visible | proved | PROVED | NO ISSUE |
| C7 | packed corollary (CF4)-(CF6)`=>`Q via Gershgorin | needs (CF5) `\|Mfrak\|<=exp(o(N))\|G^\|/L`, (CF6) minor Gram row-sum `<=exp(o(N))`. Conditional structure visible; (CF5)/(CF6) open. | conditional | PROVED (implication) | NO ISSUE |
| C8 | finite multiplier `kappa_frame = L B_A/\|A\|`, `B_A>=\|\|K_A\|\|_op` | any proved upper bound `B_A`; row-sum valid; visible | proved | PROVED | NO ISSUE |
| C9 | block-parabola separation: `C_p=1+(p-1)sqrt(p)`, `kappa_abs=C_p^k`, `K_{A_k}=I`, `kappa_frame=1`, global sum exponential | `p` odd; blockwise `(t,t^2)`; Gauss-sum evaluation; visible. Semantic-residuality of the family **not** claimed. | proved | PROVED | NO ISSUE |
| C10 | residual monotonicity: residual fiber `<=` full-slice fiber; deleting supports cannot enlarge a fiber | residual is a subset of the full slice; visible | proved | PROVED | NO ISSUE |
| C11 | executable census: strict packed improvement, nonuniform cases, exact guardrail, heavy regression | deterministic finite toys; visible | measured | MEASURED | NO ISSUE |
| C12 | the open packing input: construct `A_lambda` with `\|A_lambda\|>=exp(-o(N))L_lambda`, `\|\|K_{A_lambda}\|\|_op<=exp(o(N))`, uniformly over the frontier window | uniform over semantic primitive profiles; **silent existence claim** = the pinned crux | not proved (author) | OPEN | OPEN |

No claim in the note is mislabelled: every asymptotic dependency is printed in
the note's own not-proved list. There is no hidden overclaim.

---

## Rung 2 - Interface check vs frontiers tex

The character-frame payment is intended to substitute for the
absolute-Fourier `(EFP)`/`(MI)+(MA)` route. The exact anchor points and the
consumer chain:

| tex anchor | label | line | role |
|------------|-------|------|------|
| effective span reduction | `lem:effective-span-fourier` (EF2/EF4) | 2869 | denominator normalization to `V_g` |
| certified major/minor partition | `def:effective-major-minor` | 2911 | assigns minor vs major |
| effective Fourier payment | `def:effective-fourier-payment` (EFP, EF4) | 2929 | max-fiber `<= kappa binom/A_eff` **and** image `>= A_eff/kappa` |
| major aggregate | `def:major-arc-aggregate` (MA) | 2984 | `sum_{M} \|e_m\| <= e^{o(\|T\|)}binom` |
| minor aggregate | `def:aggregate-minor-payment` (MI) | 3081 | `sum_{m} \|e_m\| <= e^{o(\|T\|)}binom` |
| MI+MA flatness | `prop:effective-mi-ma-flatness` (EF5, EF6) | 3097 | max-fiber `<= e^{o(\|T\|)}binom/A_eff` |
| low-boundary-entropy closure | `thm:small-effective-dual-closure` (SE1) | 3026 | small-dual analogue of the frame |
| A4 leaf hypothesis | `def` A4 clauses | 912-934 | consumes (MI)+(MA) **or** a Sidon/Fourier payment |
| numerator compiler | `thm:main-smooth-circle` | 956-978 | uses `prop:effective-mi-ma-flatness` at 971 |
| primitive-Q proof | `thm:primitive-q` proof | 7181-7191 | uses (EF5) + the large-image fact at 7185 |

The frame's conclusion (CF1) delivers exactly the `prop:effective-mi-ma-flatness`
output (EF5): `max_z |F_z| <= (subexponential) M/A_eff` **at image
normalization** `barN=M/L`. Three visible-hypothesis junctions:

- **J1 - conclusion shape.** MATCH. Both the frame and (EF5)/(EF6) bound the
  full-slice and every first-match residual fiber by the same image-normalized
  multiplier; the note's monotonicity (C10) reproduces the tex's residual
  handling. Normalization matches (`barN=M/L`, the tex's default image scale,
  `eq:image-ambient-scales`). Quantifier matches (`exp(o)` on the same
  max-fiber quantity). Verdict **NO ISSUE**.

- **J2 - large-image byproduct (named gap).** `(EFP)` supplies **two** outputs:
  the max-fiber bound (EF4) **and** "the realized image contains at least
  `A_eff/kappa` points" (line 2944). The character-frame supplies **only** the
  max-fiber bound; CF1 gives no lower bound on `L` (summing CF1 over the `L`
  nonempty fibers returns the tautology `M<=M exp(o)`). The proof of
  `thm:primitive-q` consumes exactly the missing fact at line 7185,
  `L >= e^{-o(N)}A_eff`, to pass from span- to image-normalization. A leaf that
  replaces `(EFP)`/`prop:effective-mi-ma-flatness` by the frame must source
  `L >= e^{-o(N)}A_eff` separately from `(FI)`/A4's `L_N` clause (lines
  918-923). Verdict **OPEN GAP** - precisely: *the large-image fact is not a
  frame output.*

- **J3 - asymptotic scale pinning (named gap).** The tex's aggregates use
  `e^{o(|T|)}` (MI/MA) and the A4/`thm:primitive-q` scale is the leaf's active
  coordinate set of size `N` with `M=binom(N,m)` (lines 913, 7184). The note's
  `(CF2)` uses `exp(o(N))` but never identifies its `N` with the leaf's
  active-coordinate `N`; in the block-parabola family `N` is instantiated as
  the ambient block length `pk`. The scales are plausibly `Theta(n)` but the
  identification is **silent**. Verdict **OPEN GAP** (low severity) - the note
  must pin `N` to the A4 active-coordinate scale before substitution.

Interface verdict: the substitution is **valid in form** (J1), with two named
unsupplied hypotheses (J2, J3) and the primary open input `(CF2)` (C12). No
consumer relies on a frame conclusion the frame does not deliver, provided J2
and J3 are repaired in-text.

---

## Rung 3 - Re-derivation of the load-bearing identities

Three identities carry everything; each re-derived by hand and reproduced
numerically (`check_cf1_frame`, `check_cf3_converse`,
`check_full_dual_identity`, `check_gauss_Cp`, `check_block_parabola_identity`).

1. **(CF1) frame bound - REPRODUCED.** With `v_g(x)=M^{-1/2}g(Phi(x)-s0)` and
   `u_z=1_{F_z}/sqrt|F_z|`: on `F_z` the profile is constant so
   `<u_z,v_g> = sqrt|F_z| M^{-1/2} conj(g(z))`, hence `|<u_z,v_g>|^2=|F_z|/M`
   (uses `|g(z)|=1`). Summing over `A` and Bessel:
   `|A||F_z|/M = ||T u_z||^2 <= ||T||^2 = ||T T^*||_op = ||K_A||_op`. Convention
   note: `<v_g,v_g'> = hat_mu(g g'^{-1}) = conj(K_A(g,g'))`; the conjugation
   does not change the Hermitian operator norm, so CF1 is unaffected. Numeric:
   `maxfiber <= M||K_A||/|A|` holds on F5/F7/F11 toys with both the row-sum
   bound and the true operator norm.

2. **(CF3) converse + full-dual identity - REPRODUCED.** Test vector
   `c_g=conj(g(z))`: `c^* K_A c = sum_w mu(w)|sum_{g in A} g(z-w)|^2`; the `w=z`
   term is `mu(z)|A|^2`, the rest nonnegative, and `||c||^2=|A|`, giving
   `||K_A||_op >= |A|mu(z)`. For `A=G^`, `K_{G^}` is a convolution operator on
   `G^` with eigenvalues `|G|mu(-z)`, so `||K_{G^}||_op = |G|max_z mu(z)`
   exactly. Numeric: `||K_full|| - |G|max mu = 0` to `<2e-16` relative on
   `p=5,7` and the `F_3^4` block toy; `min(||K||-|A|mu)=0` (tight at the
   heaviest atom, as predicted).

3. **Block-parabola Gauss/identity - REPRODUCED.** One block `(t,t^2)`,
   normalized coefficient `p^{-1}sum_t e_p(at+bt^2)`: `=1` at `(0,0)`, `=0` for
   `b=0,a!=0`, `=p^{-1/2}` for `b!=0` (quadratic Gauss sum, verified via
   `sum_{u,v}psi(b(u^2-v^2))=p`). Absolute mass `C_p=1+(p-1)sqrt(p)`; product
   over `k` blocks gives `kappa_abs=C_p^k`. Packed `A_k={((a_i,0))}` has every
   pairwise difference `((d_i,0))` with some `d_i!=0`, whose one-block factor
   vanishes, so `K_{A_k}=I` and `kappa_frame=1`. Numeric: `C_p` matches
   `1+(p-1)sqrt(p)` to `<3e-10` for `p=3,5,7`; `K_{A_k}` off-diagonal `<2e-16`
   and `kappa_frame=1` for `(p,k)` in `{(3,1),(3,2),(5,1),(5,2),(7,1)}`.

Nothing failed to reproduce. All three load-bearing identities are PROVED.

---

## Rung 4 - Verifier rerun

**Their verifier** `verify_asymptotic_primitive_profile_character_frame_v1.py --check`
under `ulimit -v 2097152`: **RESULT PASS** (well under 500 s). Recorded:
`case_count=5`, `strict_packed_improvements=3`, `nonuniform_source_cases=3`,
`existing_elementary_prefix_rows=5` (of which `4` nonuniform),
`block_parabola_p5_global_rate=0.459399339592`,
`block_parabola_p5_packed_multiplier=1.0`,
`certificate_sha256=62aa09b75ef64eadf955ac2e745cbd2646bad8756bf78f616808e4150c3ecbcd`.
The `--tamper-selftest` design rejects 14 overclaim mutations (status,
nonclaims, pins, note-contract, all summary flags) plus one note-string
overclaim; the checker enforces `>=2` strict improvements and `>=2` nonuniform
cases, so the census cannot silently degrade.

**This audit's verifier** `verify_character_frame_audit.py` under the same
`ulimit`: **ALL PASS, exit 0**. It re-imports and re-runs their `build_payload`
(`errors=[]`), independently recomputes the `p5` rate from
`log(1+4 sqrt 5)/5 = 0.459399339592`, and recomputes their sha256, in addition
to the rungs below.

---

## Rung 5 - The open input, pinned, and the three-way comparison (headline)

**The open input, exact statement (avdeev, C12).** For every semantically
residual many-shell profile, construct `A_lambda subset hat(V_g)` with
`|A_lambda| >= exp(-o(N_lambda))L_lambda` and
`||K_{A_lambda}||_op <= exp(o(N_lambda))`, uniformly over the frontier window.
Operationally (CF5)+(CF6): a symmetric forbidden set `Mfrak` with
`|Mfrak| <= exp(o(N))|G^|/L` whose complement packs a family whose minor Gram
row-sums are `exp(o(N))`. This is an **image-normalized, absolute
(operator-norm / packing) existence** statement. It is the same object as the
tex hard input 2 ("image-scale MI+MA or direct Sidon payment"; prior anchor
`experimental/notes/audits/image_scale_mi_ma.md`).

Compared with the two other live open cruxes:

| object | normalization | mechanism | target sharpness | direction |
|--------|---------------|-----------|------------------|-----------|
| **avdeev (CF2) packing** (#558) | image `M/L` | absolute operator-norm packing | subexponential | certificate/upper side |
| **hughes (LS)** (#564) | ambient `p^w` | signed multilevel large sieve (needs `p^{w/2}` cancellation) | sharp polynomial `N<=n^3` | signed head-on |
| **LegaSage max-fiber razor / hard-input-b** (#573-#585) | image `M/L` | additive combinatorics (near-Sidon fibers) | subexponential | lower/construction side |

**(CF2) vs (LS): INCOMPARABLE.** Three orthogonal axes. (i) Normalization:
image (`M/L`, packing avoids the heavy locus) vs ambient (`p^w`, all `p^w`
frequencies). (ii) Mechanism: (LS) is signed and **requires** square-root
cancellation - hughes's own roadmap states "every absolute-value method is
provably sign-blind here"; (CF2) is an absolute operator-norm object, and the
frame's converse guardrail (CF3) proves it can never see below `|A|max mu(z)`,
i.e. it is magnitude-only. (iii) Sharpness: (LS) targets `N<=n^3` (polynomial,
far stronger than needed); (CF2) targets subexponential. Neither input implies
the other: (LS) produces a sharp fiber count but no well-conditioned packed
`A`; (CF2) produces a packing but says nothing about the signed ambient sum.
Both are, separately, sufficient inputs for primitive-Q, so (CF2) does **not**
subsume, reduce, or route through (LS).

**(CF2) vs the max-fiber razor: (CF2) is STRICTLY STRONGER (implies it).** Both
live on the same image-normalized `R=2`, `Phi=(sum t, sum t^2)` object -
avdeev's block-parabola separation family (C9) is literally the injective
(extreme-Sidon, fiber size 1) corner of LegaSage's razor, its trivial "NO"
corner. If (CF2) holds then `max_z f_z <= barN exp(o(N))` for **all** `z`,
which in particular bounds the near-Sidon low-energy fibers, so the restricted
Sidon-heavy moment `Gsid = e^{o(Nq)}` (hard-input-b) follows: `(CF2) => `
hard-input-b. The reverse fails - hard-input-b is a moment bound on low-energy
fibers and yields no packed character family. But note the cost: (CF2) is a
*stronger hypothesis*, so it may be harder to establish, or even false, on
profiles where hard-input-b holds by cancellation on the low-energy stratum;
it is not automatically an easier proof route.

**Program-level verdict for the maintainer: the character frame does NOT
collapse the program to one crux.** After #558 the board carries (at least)
**two** genuinely distinct open cruxes, not one and not three:
1. hughes's **ambient signed (LS)** - the sharp head-on route.
2. the **image-normalized `R=2` max-fiber control** - probed from below by
   LegaSage's razor (does a near-Sidon exp-large fiber exist?) and now, from
   the certificate side, reformulated by avdeev's (CF2)/(CF5) packing (does a
   well-conditioned dodging character family exist?). avdeev and LegaSage are
   two faces of the same crux (2); avdeev's packing is a **new, strictly
   stronger, still-open** certificate-side sufficient condition for it,
   **incomparable** to (LS). The natural next probe is exactly where both faces
   wall: a near-Sidon **and** exp-large `R=2` fiber at linear density.

---

## Rung 6 - Adversarial falsifier

Goal: a toy where the frame's hypotheses hold but its payment conclusion fails
(a false flatness certificate = COUNTEREXAMPLE_NEW_FLOOR). Because CF1 is an
exact Bessel bound, a violation would be a genuine defect. Search
(`run_falsifier`, deterministic seeds): `20` distributions on `Z_5, Z_7,
Z_2^3, Z_2^4, Z_3^2` (random full-support, seeded partial-support, and
heavy-atom adversaries), each stressed by a battery of character families
(full dual, all singletons, every threshold-greedy packing, seeded random
subsets) - `329` `(config, family)` pairs. For each: `kappa_frame >= actual`?
On a bounded operator-norm sample (`60` families, `|A|<=16`): row-sum bound
`>= ||K_A||_op` (Gershgorin)? `L||K_A||_op/|A| >= actual` (sharp CF1)?
`||K_A||_op >= |A|mu(z)` at every atom (`365` tests, CF3)?

Result: **0** false floors, **0** Gershgorin violations, **0** sharp-CF1
violations, **0** CF3 violations; minimum guardrail slack `>= 0` within `2e-9`
(tight on injective/uniform toys, exactly as the theory predicts); full-dual
identity relative error `< 4e-16`. **Verdict: no counterexample.** This is
**evidence, not proof** - the frame's safety (CF1 exact, CF3 tight) held on
every adversarial toy searched; consistent with the hand re-derivation that
CF1 cannot under-certify while `B_A >= ||K_A||_op`.

---

## Rung 7 - Verdict ledger

15 audited items = 12 note claims (C1-C12) + 3 interface junctions (J1-J3).

| verdict | count | items |
|---------|-------|-------|
| NO ISSUE | 12 | C1-C11, J1 |
| OPEN | 1 | C12 (packing input crux) |
| OPEN GAP | 2 | J2 (large-image fact), J3 (scale pinning) |
| COUNTEREXAMPLE_NEW_FLOOR | 0 | - |
| FIXED | 0 | - |

No overclaim, no counterexample; the note is internally sound and honestly
labelled. The finite theorem is promotion-ready subject to the two named
in-text repairs.

**Proposed ledger entry (repo policy: paper changes are proposed here, never
by diffing the tex).**

> Promote the finite character-frame inequality (CF1), its converse (CF3), the
> full-dual identity, and the packed corollary (CF4)-(CF6) into
> `asymptotic_rs_mca_frontiers.tex` as an ALTERNATIVE sufficient interface for
> the image-normalized max-fiber bound (EF5) of
> `prop:effective-mi-ma-flatness`, placed adjacent to
> `def:effective-fourier-payment`. Gate on two visible-hypothesis repairs:
> (G1/J2) state that the interface supplies only the max-fiber multiplier and
> NOT the large-image byproduct `L >= e^{-o(N)}A_eff` of (EFP); consumers (the
> proof of `thm:primitive-q`, ~line 7185) must source that fact from (FI)/A4's
> `L_N` clause. (G2/J3) identify the frame's scale `N` in-text with the leaf's
> active-coordinate scale (`M=binom(N,m)`). Do NOT promote the asymptotic input
> (CF2)=(CF5)+(CF6): it remains OPEN, is the same object as hard input 2, is
> strictly stronger than LegaSage's hard-input-b, and is incomparable to
> hughes's (LS). Verdict: NO ISSUE on the finite theorem; OPEN on (CF2).

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --check
python3 experimental/scripts/verify_asymptotic_primitive_profile_character_frame_v1.py --tamper-selftest
python3 experimental/scripts/verify_character_frame_audit.py
```
