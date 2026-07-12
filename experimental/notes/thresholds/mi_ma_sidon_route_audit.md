# Paying MI/MA (or a direct Sidon payment): a route-constraint audit after the threshold arc

## Status

`ADVERSARIAL ROUTE-AUDIT (AUDIT) of hard input #2 -- "image-scale MI/MA or a
direct Sidon payment" (agents.md L47; frontiers.tex L160-162 / L778-779 / L7105 /
L7128-7129 / L7217) -- against the 2026-07-11/12 threshold arc / CENTRAL FINDING
(applicability verdict (b), PARTIAL): #663's large-sieve impossibility
(INT|S|^4 = 2b^2-b, degree-2 moment curve, integer block) and scottdhughes #564's
engine identity (sum_c|tau_w|^4 = p^w(2n^2-n), degree-w moment curve over the
subgroup mu_n) are the SAME Sidon 4th-moment structure-blindness on two different
instances (COMPUTED, both). #663's cut therefore applies VERBATIM to the UNSIGNED
leg of hughes' max-fiber crux -- which is one of hughes' OWN already-ruled-out
routes -- and independently CORROBORATES the premise of his reduction (magnitude
methods are sign-blind); it does NOT transfer to his SIGNED target (LS)/(SV*),
which is a genuinely different object designed to carry the p^{w/2} cancellation
the 4th moment cannot see. So no cut CONSTRAINS his program; the cuts CONFIRM its
necessity. / ROUTE MAP: 14 routes to MI/MA enumerated -- 4 SURVIVE (with the exact
remaining obligation), 9 CUT (each by a named proved result), 3 TRANSFORMED (2 of
those also survive as reductions). / SHARPEST STATEMENT: what pays MI/MA is a
ONE-SIDED SIGNED exponential-scale inverse theorem for the moment curve, unified
across both lanes; the tex's PRINTED phrasing is already at its sharpest honest
form (NO forced edit, reaffirming #684), and the unified signed-object statement
is offered only as an OPTIONAL non-forced note-level adjacency. / VERIFIER PASS
(61/61), ~0.1 s.`

This packet performs the adversarial route audit that agents.md L206 lists as
maintainer-directed work ("adversarial proof audits focused on the five remaining
hard inputs: ... image-scale MI/MA or Sidon payment"). The question, precisely:
**after the threshold arc, which routes to paying MI/MA survive, which are
provably cut, and does any cut constrain scottdhughes' reduction program?**

It is the *route*-audit companion to the *print*-audit `#684`
(`image_face_print_audit.md`), which verified the same tex anchors byte-exact and
found no forced print change. This note does not re-open that verdict; it maps the
route-space *underneath* the printed input.

**The honest deliverable is the applicability truth, not a forced outcome.** The
verdict below is (b) (partial), reached by stating both large-sieve objects
precisely side by side. It is phrased throughout as a constraint on the *route
space* and a *corroboration* of hughes' reduction, never as a criticism of it.

## Credit

The object and the entire max-fiber reduction are **scottdhughes' #564**
(`b2_l1_reduction_ledger.md`, `b2_l1_crux_milestone.md`,
`b2_barrier_beating_synthesis.md`): the exact chain reducing the L1/b2 max-fiber
crux (E-b: `N <= n^3`) to `(LS)`/`(SV*)`, a **one-sided SIGNED multilevel
large-sieve / inverse theorem** for the moment curve over `mu_n`; the engine
identities `sum_c|tau_w|^2 = p^w n`, `sum_c|tau_w|^4 = p^w(2n^2-n)` (proved all
`w>=2`); the seven-route rule-out ledger; the sign-barrier arithmetic; the
`w<=3`-skeleton / `w>=4` incidence wall; the char-0 `N_0^{(0)}=0` computation; the
Bernoulli/inverse-Littlewood-Offord reframe; the `Gamma_r` (`r>=3`) connection to
`grande_finale`; and the cross-lane insight that his dyadic-block obstruction and
holmbuar's PTE residual family `#534` are the *same* equal-power-sum wall. This
note **consumes** his material and adds only the *side-by-side applicability
comparison* against the image-face cuts and the *route census*.

The image-face cuts are **holmbuar's arc**: **#663** (`bohr_gap_volume.md`: three
bridge routes proved impossible, incl. the structure-blind energy identity
`INT|S|^4 = 2b^2-b`), **#661** (`exp_ilo_fourier.md`: the Fourier atom bound,
quadratic-Bohr trapping, the refuted spectral fiber-upper-bound), **#682**
(`corridor_diameter_map.md`: the `(alpha,delta)` wall localization), and the
integrated **#655/#657/#646** (`fiber_image_tradeoff.md`, `ilo_moment_structured.md`,
`moment_map_max_fiber.md`: the `(ILO-moment)` name, the box bounds, `phi*=log2`).
The unconditional compression cap is **DannyExperiments' #668**
(`canonical_transversal_vc_compression.md`: `f<=2^{b-d}`, `L<=sum_{j<=d}C(b,j)`,
`fL<=3^b`, `omega(eta)=H_2(eta)`, hence `rho*<=log(3/2)`). The `(ILO-moment)`
naming/scope discipline and the read-only theorem-import audits are the **Codex
team's**. No `.tex`/`.pdf` touched; no printed statement changed.

Label key: **PROVED** (complete proof, either re-derived here or quoted from a
cited note strictly within its printed hypotheses), **COMPUTED** (exact
enumeration in the verifier), **AUDIT** (verbatim cross-reference / side-by-side
reading), **OPEN** (open input, unchanged). Open-PR citations carry an
**[integration flag]** where the result is not present at base `36de5bf`.

---

## Part I -- The applicability analysis: two large-sieve objects, side by side

The task's central honesty requirement is to decide whether #663's proved
large-sieve impossibility transfers to hughes' #564 signed multilevel sieve. That
requires stating both objects precisely. They are **not** the same object, but
they share **one identity**.

### The two objects (AUDIT)

| | **#663 object** (image face) | **scottdhughes #564 object** (max-fiber / Fourier face) |
|---|---|---|
| carrier | a **block** `V` = `b` distinct **integers** | the order-`n` **subgroup** `mu_n <= F_p^*`, `n=2^a`, `n\|p-1` |
| curve | degree-2 moment curve `v -> (1,v,v^2)` | degree-`w` moment curve `x -> (x,...,x^w)`, deployed `w=67471` |
| ambient | continuous torus `[0,1)^2` (Weyl sum `S(t1,t2)`) | finite `F_p^w` (subgroup character sum `tau_w(c)`) |
| target quantity | max fiber `fstar`, image `L1` of `Phi(S)=(\|S\|,sum v,sum v^2)` | fiber count `N = nu(0) = #{\|S\|=m: F(S)=0}`, target `N <= n^3` |
| 4th-moment identity | `INT_{[0,1)^2}\|S\|^4 = 2b^2 - b` (Thm 2, PROVED) | `sum_c \|tau_w(c)\|^4 = p^w(2n^2 - n)` (engine, PROVED all `w>=2`) |
| signing | route V2 amplifies the **unsigned** 4th moment `INT\|S\|^4` | target `(LS)`/`(SV*)` is a **one-sided SIGNED** estimate |

Both `Phi(x)=(x,...,x^w)`, `F(S)=sum Phi`, `N=nu(0)` and `TARGET (E-b): N<=n^3`
are hughes' verbatim statements (`b2_l1_reduction_ledger.md` L35, L38, byte-checked).

### The one shared identity (COMPUTED)

Both 4th-moment values are the **Sidon minimum of the moment curve**: the moment
curve is a `B_2`/Sidon set, so the only `2`-vs-`2` additive quadruples with equal
`p_1` *and* `p_2` are the trivial ones, and the 4th moment collapses to
`2(size)^2 - (size)`. The verifier recomputes both from scratch:

- `INT|S|^4 = 2b^2-b` on five blocks incl. the #655 `b=18` champion (`= 630`);
  and confirms it is **identical** for an interval and a subset-dissociated set
  (BLOCK B, structure-blind), while `INT|S|^6` **differs** between them (the first
  moment that *sees* structure -- exactly #663 Thm 2's remark, and hughes' PTE /
  `INT|S|^6` support-6 trade).
- `sum_c|tau_w|^4 = p^w(2n^2-n)` on `(p,n,w) in {(7,3,2),(13,3,2),(13,4,2),
  (11,5,2),(7,3,3)}` (BLOCK B), and a direct check that no nontrivial `2`-vs-`2`
  quadruple exists on `{(v,v^2)}`.

So `2b^2-b` (block) and `2n^2-n` (subgroup) are **the same formula** with block
size `b` `<->` subgroup size `n` -- the identical Sidon rigidity, one on the
continuous torus at degree 2, one in `F_p^w` at degree `w`.

### What each side proves about that identity

- **#663 (PROVED).** Because `INT|S|^4 = 2b^2-b` is pinned at its minimum
  *independent of the arithmetic of `V`*, the large-sieve / additive-energy / BSG
  route "amplify the 4th moment to force structure" is **vacuous at constant
  `eta`** -- it reaches only the corridor `eta ~ 2 log_2(b)/b -> 0`. A moment of
  order `2m` improves the corridor only to `~ m log_2(b)/b`; constant `eta` needs
  `m -> infinity` (exponential-order moments). The *unsigned* large-sieve family
  provably cannot cross the corridor.
- **scottdhughes #564 (PROVED, independently).** The engine identity holds at
  *every* `w`, so it "is NOT the wall." Every **absolute-value** method (`L^2`,
  `L^{2k}`, restriction/extension, Halász, and -- worked out separately -- RV-LCD,
  which reduces to per-frequency Weil at `w<=22`) is **sign-blind** and "forfeits
  exactly that `p^{w/2}` cancellation"; a restriction/large-sieve estimate that is
  "merely an `L^2 -> L^q` amplification is NOT enough; the estimate must be SIGNED
  (one-sided inverse theorem)" (`b2_l1_reduction_ledger.md` L263, byte-checked).

These are the **same finding on the two instances**: the moment-curve Sidon 4th
moment is structure-blind, so the unsigned/magnitude route is dead in *both*
lanes, and the resolution must be *signed*.

### Verdict: (b) PARTIAL -- applies to the unsigned leg, does not transfer to the signed target

> **Applicability verdict (b).** #663's proved large-sieve impossibility applies
> **verbatim to the UNSIGNED leg** of hughes' max-fiber crux -- the leg hughes
> himself already rules out (his ledger routes 5-7, the sign-barrier section) --
> and thereby **independently corroborates** the premise on which his #564
> reduction is built. It does **not** transfer to his **signed** target
> `(LS)`/`(SV*)`.

**The precise hypothesis that breaks in a transfer.** #663 Thm 2 is a statement
about the **nonnegative magnitude** `INT|S|^4` (an unsigned quadruple count).
Hughes' `(LS)`/`(SV*)` is a **one-sided SIGNED** estimate whose whole content is
the `p^{w/2}` cancellation among the `p^w` signed frequencies -- a quantity to
which the 4th-moment magnitude is, by construction, **blind**. To transfer #663's
cut onto hughes' target one would additionally have to prove the *signed* sieve is
*also* structure-blind. #663 does not do this and cannot: its own PI-flag R5(b)
records the opening explicitly -- "A genuinely new idea using `INT|S|^6` (the
PTE-trade count) at growing order is not excluded -- but that is the
exponential-regime inverse-LO itself." That opening **is** hughes' target.

**A (c)-flavored route-separation, recorded precisely.** The two objects also live
in genuinely different spaces (continuous torus, degree 2, integer block vs.
`F_p^w`, degree `w`, algebraic subgroup), so #663's identity is not *literally*
hughes' engine identity -- it is the same *phenomenon* on a different instance.
The clean separation lemma: **the two large-sieve objects are distinct (space,
degree, signing), CUT by the same structure-blindness on their unsigned legs, and
OPEN by the same signed-cancellation crux on their signed cores.** This unifies
the wall across the image face and the max-fiber face -- extending hughes' own
cross-lane insight (his dyadic-block obstruction `==` holmbuar's PTE family `#534`)
up from the PTE/6th-moment level to the 4th-moment level.

**Flagged for scottdhughes (with credit, as a route constraint -- not a
criticism).** The convergence is a positive datum for the #564 program: it shows
the unsigned family is closed off in *both* independently-developed lanes by *one*
phenomenon, so effort is correctly concentrated on the signed target. Nothing here
weakens the reduction; it sharpens the case that `(LS)`/`(SV*)` is the irreducible
content.

---

## Part II -- The route map to MI/MA

Every route to paying image-scale MI/MA (or a direct Sidon payment) visible in the
sources, classified **SURVIVES** (with the exact remaining obligation) / **CUT**
(by which proved result) / **TRANSFORMED** (reduced to a named object). "MA" here
is the max-fiber/moment-accessibility payment; "MI" the image/minor payment; the
two share the same crux on the moment curve.

| # | Route | Verdict | By / obligation |
|---|-------|---------|-----------------|
| 1 | hughes #564 signed multilevel sieve (max-fiber E-b) | **SURVIVES / TRANSFORMED** | reduces `N<=n^3` to `(LS)`/`(SV*)`; obligation OPEN [flag #564 fork] |
| 2 | direct **unsigned** Sidon payment (moment curve is `B_w`) | **CUT** | #663 Thm 2 `=` #564 engine: 4th moment `= 2n^2-n` is the Sidon minimum, structure-blind |
| 3 | Fourier/trapping via #661 (image face) | **SURVIVES / TRANSFORMED** | `fstar<=2^b INT\|Xhat\|` + quadratic-Bohr trapping; obligation `Bohr->GAP` OPEN [flag #661] |
| 4 | large-sieve / additive-energy / BSG bridge | **CUT** | #663 Thm 2 (structure-blind); #564 routes 5-7 (sign-blind); RV-LCD `=` Weil wall |
| 5 | Weyl / major-arc / inverse-Weyl bridge | **CUT** | #663 R1.4: no interval to difference over; "big Weyl sum" `=` Bohr condition (tautology) [flag #663] |
| 6 | det-G / spectral fiber-**upper** bound | **CUT** | #661 F2 REFUTED: spectral (spread-only) quantities blind to the fiber ceiling [flag #661] |
| 7 | volume-multiplicity bridge (Lemma-2 volume `->` joint rank) | **CUT** | #663 R2.3: volume forces multiplicity only if `log2 detG >= 2eta b + O(log b)` [flag #663] |
| 8 | two-frequency elimination (`->` rank) | **CUT** | #663 R2.4: linear over `R` but fails mod 1 [flag #663] |
| 9 | compression side via DannyExperiments #668 | **SURVIVES (atom only) / TRANSFORMED** | unconditional `fL<=3^b => rho*<=log(3/2)`; discharges the **analytic atom** only, necessary-not-sufficient [flag #668] |
| 10 | RV-LCD / Littlewood-Offord anti-concentration | **CUT** | #564: RV-LCD `=` per-frequency Weil `=` the `w<=22` wall; deployment `w=67471` is ~3000x past |
| 11 | per-frequency Weil | **CUT** | #564: degree `w > sqrt(p)` (`67471 > 46340`) |
| 12 | higher-dim incidence geometry (Rudnev `F_p^2/F_p^3`) | **CUT at `w>=4`** | #564: no high-dim incidence bound; `w<=3` only a *numerically-validated skeleton*, not a theorem |
| 13 | rational-resonance / Diophantine horn | **SURVIVES (CONDITIONAL) / TRANSFORMED** | #663 R3 `=` #661 CONDITIONAL: closes if dominant resonance rational, bounded `q`; unconditional `=` Diophantine control [flag #663] |
| 14 | positive-count razor `->` C9 max-fiber **lower** bound | **SEPARATE object** | #582/#564: a positive (no-cancellation) route to the *lower* bound, not the MI/MA *upper* payment |

**Counts: 4 SURVIVE (routes 1, 3, 9, 13), 9 CUT (2, 4, 5, 6, 7, 8, 10, 11, 12),
3 TRANSFORMED (1, 3, 9; also 13 conditionally). Route 14 is an adjacent but
distinct target (the C9 lower bound), recorded to prevent conflation.
(4 + 9 + 1 separate = 14.)**

### The surviving routes, with their exact remaining obligations

- **Route 1 (hughes #564).** Survives as an *exact reduction*: `E-b` (`N<=n^3`)
  `->` `(LS)` `->` `(SV*)` `->` (terminally, `b2_l1_reduction_ledger.md`) the
  `w`-dimensional moment-curve extension of Shkredov (arXiv:1802.09066 Thm 3), i.e.
  the primitive collision moment `Gamma_r` (`r>=3`) `<= e^{o(n)}`, equivalently a
  **signed square-root cancellation** `|P(n,w)| <~ p^{w/2} poly(n)` in the regime
  `w > sqrt(p)` **and** `w >= 4`. **Obligation: prove that signed cancellation.**
  OPEN; numerically supported (`(SV*)` holds with ~5 orders of room through the
  `theta`-controlled deployment proxy) but not proved. This is the same crux as
  `grande_finale`'s `conj:q-active` / `thm:primitive-log-collision`, which its own
  Lean docstring marks "a genuinely open ingredient ... NOT discharged here."
- **Route 3 (#661, image face).** Survives to the single residual step
  `Bohr -> GAP`: convert `vol(T_kappa) >= 2^{-eta b}/2` into a bounded-rank GAP
  containing all but `O(eta b)` elements. **Obligation:** that conversion, which
  #663 proves is immune to energy/large-sieve/Weyl/naive-multiplicity arguments,
  leaving Diophantine control of the resonance denominator.
- **Route 9 (#668, compression).** Survives *unconditionally* but only as the
  **analytic atom**: `fL<=3^b`, hence `rho*<=log(3/2)<log2`. Danny's own note
  states it "does **not** ... pay the effective image over all leaves, profile
  add-back, ray overlap, A2, A6, A7, or LOWER ... neither Grand MCA nor Grand
  List." **Obligation (necessary-not-sufficient):** the first-match atlas, block
  typing, profile add-back, and slope charge -- exactly the residual #684 records
  as the still-open remainder of the printed input.
- **Route 13 (Diophantine horn).** Survives *conditionally*: closes when the
  dominant resonance is rational of bounded denominator (`theta_2=a/q =>` trapped
  `v` in `<= 2^omega(q)` residue classes `=` rank-1 GAP). Unconditional statement
  `=` Diophantine control of `theta_2` at exponential concentration `=` the
  exponential-regime inverse-LO (route 1's crux, seen from the volume side).

### Why the cut routes cannot be rescued

Routes 2, 4, 10, 11 are one family: **sign-blind magnitude estimates on a
Sidon-rigid curve**. Their common ceiling is the Cauchy-Schwarz loss of `p^{w/2}`
(`= n^{~49784}` at deployment) against a target slack of only `n^{1.3}` -- no
`L^2`/energy bound of any exponent can be rescued by slack (hughes' exponent
arithmetic, `b2_l1_reduction_ledger.md`). Routes 5-8 are the image-face bridges
#663 individually refutes. Route 12 is the incidence-geometry frontier, present at
`w>=4`. **Every cut route is on the wrong side of the sign barrier; only routes
1/3/13 (all signed/Diophantine) and route 9 (a different, compression object that
pays only the atom) survive.**

---

## Part III -- Does any cut constrain scottdhughes' reduction program?

**No -- and this is the load-bearing conclusion of the audit.** The cuts land
entirely on the **unsigned** route family (routes 2, 4-8, 10-12). Hughes' #564
reduction is *precisely the move that steps around that family*: it transforms the
`sup` (max fiber `N`, sign-blind-unreachable) into a **signed** object
(`(LS)`/`(SV*)` / `Gamma_r` / `P(n,w)`) whose whole content is the cancellation
the cut routes forfeit. So:

1. The one cut that would *constrain* him -- a proof that the **signed** target is
   also impossible -- **does not exist**. #663 explicitly leaves that door open
   (R5(b)); its impossibility is for the unsigned leg only.
2. The cuts that *do* exist **corroborate** his reduction. #663's structure-blind
   `INT|S|^4=2b^2-b` is the image-face twin of his own engine identity
   `sum_c|tau_w|^4=p^w(2n^2-n)`; #661's refuted spectral fiber-upper-bound is the
   image-face twin of his sign-barrier arithmetic; RV-LCD `=` per-frequency Weil is
   his `w<=22` wall. Two independently-developed lanes reach the same wall.
3. Therefore the audit *tightens the case* that his `(LS)`/`(SV*)` is the
   irreducible content, and *localizes* effort: the unsigned family is closed in
   both lanes; the open frontier is exactly the signed exponential-scale inverse
   theorem (his terminal reduction: the moment-curve extension of Shkredov Thm 3).

The honest one-line answer: **the threshold arc cuts constrain the ROUTE SPACE
(the unsigned family is dead in both lanes), not hughes' reduction -- which is
built on exactly that constraint and survives it intact.**

---

## Part IV -- The sharpest honest statement of what would pay MI/MA

Per the #684 pattern, the question is whether a statement sharper than the tex's
*printed* phrasing is forced. It is **not** forced -- but a sharper *note-level*
characterization is available, and is offered as an optional, non-forced
adjacency.

**The tex's printed input is already at its sharpest honest form.** The three
printed clauses -- "image-scale MI and MA or a direct Sidon payment" (L160-161),
"remain separate checks" (L7105-7106), "does not close the Sidon ... branches"
(L7128-7129) -- are each verified current and exactly true. Narrowing the printed
"or a direct Sidon payment" to the signed-sieve object would import a note-level
route conclusion into a manuscript hypothesis that is correctly stated as broadly
open (the overclaim #684 warns against). **No forced edit.**

**The route audit's sharpest note-level statement** (unifying both lanes):

> What pays image-scale MI/MA is a **one-sided SIGNED exponential-scale inverse
> theorem for the moment curve** -- on the max-fiber/Fourier face, hughes' `(LS)`/
> `(SV*)` over `mu_n` at degree `w`, equivalently the `w`-dimensional moment-curve
> extension of Shkredov Thm 3 / the primitive collision moment `Gamma_r`
> (`r>=3`); on the image face, the `Bohr->GAP` conversion of #661/#663.
> The **entire unsigned/magnitude family** (`L^2`, `L^{2k}`, restriction, Halász,
> per-frequency Weil, RV-LCD, additive-energy/large-sieve, and `F_p^{>=4}`
> incidences) is provably insufficient, because the moment curve's 4th moment is
> pinned at its Sidon minimum (`2n^2-n` on the subgroup, `2b^2-b` on the block),
> which is structure-blind; the payment's whole content is the `p^{w/2}`
> cancellation that lives in the signs the 4th moment cannot see.

This is sharper than the tex on *mechanism* (it says the payment must be signed
and why), but it is note-level and route-specific, so it does not force a print
change.

**Optional, non-forced adjacency (maintainer discretion only; NOT a print-list
item).** Should the maintainer wish to record the route cartography, a single
sentence could follow the robustness paragraph (after L7130):

> *Both faces of the image-scale input reduce to one object: a one-sided signed
> exponential-scale inverse theorem for the moment curve (the signed multilevel
> large-sieve `(LS)`/`(SV*)` on the max-fiber face; the `Bohr`-to-`GAP` conversion
> on the image face). The unsigned/magnitude family -- `L^2`, restriction, Halász,
> per-frequency Weil, and additive-energy/large-sieve -- is provably insufficient,
> since the moment curve's fourth moment is pinned at its Sidon minimum and hence
> structure-blind; the payment's content is the square-root cancellation among the
> signed frequencies.*

This is **new exposition** crediting **scottdhughes #564** and holmbuar's
#661/#663, not a correction. **[integration flags:** the signed-sieve reduction
requires #564 (base-integrated); the `Bohr->GAP` localization requires #661/#663;
`rho*<=log(3/2)` requires #668 -- open PRs at base `36de5bf`.**]** Nothing printed
is wrong without it.

---

## Files, labels, reproducibility

- Note: `experimental/notes/thresholds/mi_ma_sidon_route_audit.md` (this).
- Verifier: `experimental/scripts/verify_mi_ma_sidon_route_audit.py`
  (`RESULT: PASS (61/61)`, ~0.1 s, stdlib-only, zero-arg).

**Per-claim status.** The two 4th-moment identities `INT|S|^4=2b^2-b` and
`sum_c|tau_w|^4=p^w(2n^2-n)` and their coincidence at the Sidon minimum, the
6th-moment structure-sensitivity, and #668's `fL<=3^b`/`rho*<=log(3/2)` =
**COMPUTED** (BLOCK B/C, re-derived from scratch). The side-by-side object
comparison and the route classifications = **AUDIT** (each verdict attributed to a
named cited result within its printed hypotheses). The applicability verdict (b),
the "no cut constrains hughes" conclusion, and the "tex already sharpest" verdict
= **AUDIT**. The terminal obligations of routes 1/3/9/13 (the signed
exponential-scale inverse theorem; `Bohr->GAP`; the atlas/typing/add-back/charge;
Diophantine control) = **OPEN**, unchanged.

**Reproducibility.**
```sh
ulimit -v 2097152
python3 experimental/scripts/verify_mi_ma_sidon_route_audit.py   # RESULT: PASS (61/61)
```
The verifier byte-checks every quoted anchor (frontiers.tex, agents.md,
`b2_l1_reduction_ledger.md`, `fiber_image_tradeoff.md`) at its exact line with a
negative control, recomputes both Sidon 4th-moment identities (incl. the #655
`b=18` champion, `INT|S|^4=630`) and the 6th-moment structure-sensitivity, and
recomputes #668's subset-sum bounds by exhaustive enumeration on small degree-2
moment blocks. No `.tex`/`.pdf` touched.
