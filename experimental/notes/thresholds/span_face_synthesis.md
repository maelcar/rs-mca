# The span face of the first-match envelope: closure statement and hypothesis-matching

## Status

`ARC SYNTHESIS (AUDIT) / CLOSURE STATEMENT COMPOSED (PROVED-BY-CITATION, NO NEW
MATH GAP) / HYPOTHESIS-MATCHING TABLE (AUDIT, every tex anchor verbatim-checked
at 5c9aab7) / RESIDUAL = ONE PRINTED INPUT (FI-field') / CONSISTENCY SWEEP CLEAN
(three supersessions made explicit; the profile-vs-cell routing point pinned)`.

The maintainer's own instruction at the 5c9aab7 integration entry
(`experimental/agents-log.md`, L59-61, verbatim):

> "Continue treating the remaining saturation/collapse/profile statements as
> input-specific until their hypotheses are matched against
> `asymptotic_rs_mca_frontiers.tex`."

This note performs that hypothesis-matching for the **span-face arc**
(`#622 -> #625 -> #626 -> #627 -> #635 -> #636 -> #642 -> #645`, plus the
just-shipped `#647` and the thick-form comparison `#638`), to promotion grade. It
does **not** introduce new mathematics; it **composes** the arc's proved steps
into the single precise theorem they support, matches each arc statement to its
tex consumer with a verbatim anchor, states exactly what must be printed, records
the open corners honestly, and sweeps the arc against itself for contradictions.

Every tex anchor below was read at the worktree tip `5c9aab7` and matched against
the quoted string at the cited line +/- 3. Every PR-number-to-note mapping, every
stated PASS count, and the S2 internal consistency are re-checked by
`experimental/scripts/verify_span_face_synthesis.py` (stdlib-only, zero-arg,
`RESULT: PASS`, ~1 s under `ulimit -v 2097152`).

Label key: **PROVED** (a genuine step of the composition proof, no new gap),
**AUDIT** (verbatim interface reading of the tex or a sibling arc note),
**SUPERSEDED** (an arc statement whose reading a later arc PR revised),
**NEEDS-PRINTING** (a tex edit the arc identifies), **OPEN** (a genuinely
undischarged corner).

**Credit.** The span-face arc is holmbuar's `#622` (`se_on_admissible_leaves.md`),
`#625` (`c7_routing_spectrum.md`), `#626` (`c7_degree_enumeration.md`), `#627`
(`routing_exhaustiveness.md`), `#635` (`collapse_payment.md`), `#636`
(`saturation_payment_repair.md`), `#642` (`c7_collapse_image_degree.md`), `#645`
(`fi_field_discharge.md`), `#638` (`thick_form_comparison_lemmas.md`), and the
just-shipped `#647` (`collapse_field_cost.md`, branch
`thresholds-collapse-field-cost`, commit `e5c2baa` -- **not** integrated at
`5c9aab7`). Foundational: the master identity `L>=A_eff/(1+E)` and the supplement
`(S_E)` are `#614`; the J2 magnitude-blindness impossibility is `#609`; the
depth-`w` prefix atlas is `#536`; the Gap-2 `=>` C5 classification is `#545`. The
block-parabola family and `(CF*)` identities are **avdeevvadim's** `#558`.
**DannyExperiments'** thick correction `(C1)-(C6)` is `#629` (integrated into
`minimal_phase_supplement.md`), the aperiodic one-ray confined extreme is `#621`
(`aperiodic_one_ray_saturation.md`), the profilewise separating-pole realization
is `#631`, the per-line weighted-cover ceiling is `#620`
(`canonical_full_agreement_occupancy_atlas.md`), and `#641` is consumed through
`#642`/`#645`. The **Codex team's** orientation floor is `#634`
(`full_agreement_orientation_saturation.md`) and the antipodal phase bracket is
`#644` (`orientation_prefix_phase_transition.md`). `(LS)` is **scottdhughes'**
`#564`; the C9 max-fiber razor is **LegaSage's** `#585`. The adjacent image-face
moment-map rate `phi*=log 2` (`#646`, revising `#643`'s constant) is
`moment_map_max_fiber.md`. No finite M31/KoalaBear survivor count, adjacent
inequality, or target threshold is touched.

---

## S1 -- THE CLOSURE STATEMENT

The **span face** is the effective-image clause `(FI)` (tex **L4844**,
`L\ge e^{-o(N)}A`, `\label{eq:full-image-certificate}`): the realized boundary
image `L` is within a subexponential factor of the ambient target `A`, so a leaf
may be estimated at span/ambient scale rather than image scale. "The span face of
the first-match envelope closes" means: every leaf the envelope charges at
span/ambient scale carries `(FI)`, and the leaves that **fail** `(FI)`
(effective-image collapse) are routed so that their retained charge to the
envelope is subexponential per received line. The arc composes into exactly one
theorem:

> **Theorem (span-face closure, PROVED-by-citation).** Let
> `(C_n,a_n)=(RS_{F_n}(D_n,k_n),a_n)` be a **ledger-admissible** sequence
> (`def:admissible-sequence`, tex **L896-954**, conditions `(A1)-(A7)`) that
> additionally satisfies the **ambient-field clause**
>
> ```
>    (FI-field')   log|F_n| = o(n)      (equivalently [F_n:B_n] = o(n/log|B_n|)),
> ```
>
> which holds automatically on the prize's polynomial-size smooth/circle rows
> (`log|B_n| = O(log n)`). Then the span face of the first-match envelope
> **closes**. On the product/profile class that carries **every**
> `(S_E)`-violating admissible leaf (`E+1 = A_eff*P_2` multiplicative; single
> admissible power-sum leaves with `R<char`, non-Artin-Schreier have polynomial
> `E` -- `#622` T3 / `#625` T-C, PROVED):
>
> - **(i) DETECT.** Every `(S_E)`-violator fires a **router-decidable**
>   pre-primitive trigger before the high-energy primitive step: the
>   **effective-image-collapse** trigger (`L << A`, tex **L2453-2454**) if
>   `G_1 = A_eff/L` is exponential, or the **ray-saturation** trigger
>   (`max_s f_s > barN^img`, tex **L2440-2449**, = the negation of
>   `def:primitive-q`, tex **L4918**) if `Q_img = L*max mu` is exponential; and no
>   leaf escapes both, because `E+1 <= G_1*Q_img` (MASTER-2) admits no third mode.
>   The primitive step's own max-fiber-Q rejection **coincides** with the
>   pre-primitive ray-saturation trigger, so there is no unaccounted mass.
>   [`#625` MASTER-2, `#627` T-DET; **PROVED**]
> - **(ii) ROUTE.** Every effective-image-collapse profile fails `(FI)` and is
>   "routed---assigned by the first-match rule to an earlier profile so that its
>   slopes and all witnesses above them are removed from the later residual" (tex
>   **L877-881**, `def:closed-asymptotic-ledger` item **L1115-1116**), so its own
>   first-match set `Z_i^circ = empty` and it contributes **0** to the charge. The
>   `e^{Omega(N)}` routed profiles are summed **zero** times, and the
>   "countertheorem" (tex **L889-890**) does **not** fire -- it was a per-profile
>   overcount of a quantity the closed ledger charges as a **first-match disjoint
>   union** `sup_r sum_i |Z_i^circ| = sup_r |Z_a(r)|` (`lem:first-match-bound`,
>   tex **L1526-1538**), each slope counted once. [`#635` T-PAY; **PROVED**]
> - **(iii) PAY.** The single retained **effective-image rank-collapse cell** (the
>   routing **target**, the earlier profile of (ii)) charges
>   `delta_lambda(r) = |Z(cell) cap {MCA-bad slopes of r}| <= |F_r|` distinct
>   slopes per received line, by **subfield confinement**
>   (`thm:subfield-confinement-full`, tex **L1930-1934**: "every MCA-bad slope of
>   a `B`-valued received line lies in `B`") applied to `B subseteq F_r subseteq
>   F`. [`#642` T-FIELD; **PROVED**]
> - **(iv) CONFINE.** In the prize's full-field normalization `e_MCA(r) =
>   delta(r)/|F|`, confinement reads `e_MCA(r) <= |F_r|/|F|`, so any
>   **prize-relevant** line (`e_MCA(r) > eps = 2^{-128}`) has `log|F_r| >= log|F| -
>   128`: `(FI-field)` on the received line is equivalent to `(FI-field')` on the
>   ambient field. Under `(FI-field')`, `delta_lambda(r) <= |F_r| <= |F_n| =
>   e^{o(n)}` per line. [`#645` (RED); **PROVED** reduction]
>
> The surviving primitive first-match residuals carry `(FI)` and max-fiber Q,
> hence `(S_E)` (`E+1 <= G_1*Q_img <= e^{o(N)}`, `#625` T-A) and the span face
> directly (`(A4)`-branch-1 leaves have it free by `prop:effective-mi-ma-flatness`,
> `#622` T1); the Gap-2 span-collapse sub-case is the C5 field-descent cell,
> **vacuous** on admissible leaves (`w<char`, `#545`). Since **no** admissible
> clause `(A1)-(A7)` bounds `|F_n|` (tex **L896-954**, verbatim), `(FI-field')` is
> a genuine **printed input**; the per-line `|F|^{1/2}` cap that would have made it
> free is **refuted** by an explicit `Theta(|F|)` collapse line at `[F_r:B]=2`
> (`#647`). **QED, modulo the printed input `(FI-field')`.**

**Composition audit (no new math gap).** The chain is a proof-by-citation: each
of (i)-(iv) is a PROVED theorem of a named arc PR whose tex consumer is anchored
verbatim in S2. The **only** non-theorem step is the printed hypothesis
`(FI-field')`, which is **sufficient** (T-FIELD, `#642`) and **necessary on the
prize-relevant class** (subfield confinement forces `log|F_r| >= log|F| - 128`,
and the free `|F|^{1/2}` route is refuted, `#645`/`#647`). It is a **hypothesis to
print, not an unproved step** -- composing (i)-(iv) surfaces no gap. On the
poly-field class (`log|F_n| = o(n)` automatic) the closure is **unconditional**.

**Scope note (span face vs image face).** The closure is span-face-specific and
runs through the **collapse** class. The **saturation** class (`Q_img`
exponential, `G_1 = 1`) has a **full** image (`(FI)` **holds**), so it does **not**
threaten the span face; it bears on the MCA **count** / image face, and its own
C7 budget is discharged separately by the mass-weighted `RC_occ` payment (`#636`)
on the heavy-atom **geometric-tail** product class (uniform-tail borderline
flagged, S4). `#636` is therefore **adjacent** to this closure, not load-bearing
for it.

---

## S2 -- THE HYPOTHESIS-MATCHING TABLE

The maintainer's literal ask. One row per arc statement. Columns: **statement** |
**tex consumer/anchor** (verbatim-checked at `5c9aab7`) | **hypotheses FROM the
tex** | **hypotheses BEYOND the tex** (the input-specific residue) | **status**.
Every row is **AUDIT** (anchor-checked interface reading) except where the
composition itself is PROVED. Verbatim anchor quotes are the exact tex strings;
the verifier matches each within +/- 3 lines of the cited line.

### Row 1 -- `(S_E)` stratification on admissible leaves (`#622`, `se_on_admissible_leaves.md`)

- **Statement:** On `(A4)`-branch-1 leaves `(S_E)` is the free `L^2`-fragment of
  the `(MI)`+`(MA)` payment and the span face is already free; admissibility
  `(A1)-(A7)` does **not** exclude the `(S_E)`-violating block-parabola (it enters
  via the branch-2 image-normalized escape) and does **not** imply `(S_E)`.
- **Tex consumer/anchor:** `def:admissible-sequence` `(A4)`, tex **L924-934**,
  verbatim "The aggregate minor payment `(MI)`" ... "or the leaf has a separately
  proved image-normalized Sidon/Fourier moment payment"; image clause `(FI)`, tex
  **L4844**, `\tag{FI}\label{eq:full-image-certificate}`.
- **FROM the tex:** `(A4)` two-branch payment; `(FI)` (L4844); `(A3)` "Any use of
  the ambient scale is accompanied by (FI)" (**L922**).
- **BEYOND the tex:** none as an independent input -- `(S_E)` was *proposed* as
  the extra hypothesis, but `#625` proves it is a **corollary** of `(FI)` +
  max-fiber-Q, not independent.
- **Status:** **SUPERSEDED-BY `#625`** (the needed printed object is not `(S_E)`
  but the collapse-cell field payment; `(S_E)` is discharged as a corollary).

### Row 2 -- MASTER-2 two-cell partition (`#625`, `c7_routing_spectrum.md`)

- **Statement:** `E+1 = A_eff*P_2 = (A_eff/L)(L*max mu) = G_1*Q_img` (one Holder
  step), so every `(S_E)`-violator has `G_1` exponential (**collapse**) or `Q_img`
  exponential (**saturation**); no third mode. The C7 cell is **two** assumed
  enumerative inputs, both load-bearing.
- **Tex consumer/anchor:** C7 cell, tex **L2440-2454**: **L2440**
  "`\paragraph{Saturation and effective-image-collapse cells.}`", **L2452**
  "projection degree remains an enumerative input", **L2454** "reaches
  exponentially fewer boundary values than its ambient codomain contains";
  max-fiber predicate `def:primitive-q`, tex **L4918**,
  `\max_{s\in\Scal}f_s\le e^{o(N)}\barN^{\rm img}`.
- **FROM the tex:** the two C7 events (L2440-2454); `def:primitive-q` (L4918).
- **BEYOND the tex:** none (MASTER-2 is an exact identity + Holder; `E+1 =
  A_eff*P_2` is `#614` Parseval).
- **Status:** **DISCHARGED** (PROVED identity; it is (i)+(ii) of S1).

### Row 3 -- C7 degree = binomial tail (`#626`, `c7_degree_enumeration.md`)

- **Statement:** The number of profiles reaching collapse `G_1>=e^{eps N}` (resp.
  saturation) is the binomial tail `sum_{j>=theta k} C(k,j) = e^{Omega(N)}`;
  direct envelope enumeration cannot pay it, and admitting the profiles with
  singleton-fiber `Nbar=1` realizes "the countertheorem".
- **Tex consumer/anchor:** `eq:profile-envelope`, tex **L862**,
  `\label{eq:profile-envelope}`; guard "the sum and maximum have the same
  exponential scale" (tex **L870**); "The countertheorem is exactly a row for
  which a quotient profile in" (tex **L889**); `(A2)` "A first-match atlas covers
  every bad-slope witness and has" `e^{o(n)}` profiles (tex **L905**).
- **FROM the tex:** the `E_n` guard (L869-870); `(A2)` profile count (L905-907);
  countertheorem (L889-890).
- **BEYOND the tex:** the reading that L869 is a **count** hypothesis.
- **Status:** **SUPERSEDED-BY `#635`** -- the count reading was never the operative
  statement (the charge is a disjoint-union mass, Row 5); the `e^{Omega(N)}` count
  is correct but counts the "arbitrary planted subsets" `lem:profile-atlas`
  already excludes.

### Row 4 -- T-DET router-decidable detection (`#627`, `routing_exhaustiveness.md`)

- **Statement:** Both C7 triggers are finite functions of the profile occupancy
  vector, so **detection is exhaustive and router-decidable**; the primitive
  step's max-fiber-Q rejection **coincides** with the pre-primitive ray-saturation
  trigger, so the "unaccounted-mass" hole does not exist. Residual = payment, not
  detectability.
- **Tex consumer/anchor:** first-match order, tex **L5181** "algebraic major arcs
  first, then a separately certified Sidon/Fourier cell"; detectability split, tex
  **L1497** "Payment is an enumerative assertion about an actual slope projection"
  / **L1498** "constructibility alone is not payment"; the closed-ledger echo,
  tex **L1120-1122** "Constructibility, a raw support count, or a support-pair
  moment alone does not close a ledger"; predicate identity `def:primitive-q`
  (tex **L4918**) vs ray-saturation (tex **L2440-2449**).
- **FROM the tex:** first-match order (L5180-5182); "constructibility alone is not
  payment" (L1497-1498); `def:primitive-q` (L4918); C7 triggers (L2440-2454).
- **BEYOND the tex:** none for detection (MASTER-2 + the definitional fact that
  `L`, `A`, fiber cardinalities are finite functions of the profile).
- **Status:** **DISCHARGED** (detection is a THEOREM; it is (i) of S1). Payment
  residual carried to Rows 5-8.

### Row 5 -- T-PAY first-match disjoint-union charge (`#635`, `collapse_payment.md`)

- **Statement:** The envelope charges the first-match **disjoint union**
  `sup_r sum_i |Z_i^circ| = sup_r |Z_a(r)|`, each slope once; routed collapse
  profiles have `Z_i^circ = empty` (charge 0); the census is **per-line,
  description-entropy** charged, so the countertheorem does **not** fire. Single
  residual T-PAY-RES = the one retained collapse cell's per-line degree.
- **Tex consumer/anchor:** `lem:first-match-bound`, tex **L1534-1535**,
  "exact-agreement reduction and witness" ... `Z_a(r)=\coprod_iZ_i^\circ`;
  `def:closed-asymptotic-ledger` item, tex **L1106-1108** "certified bound for its
  actual first-match slope set `Z_i^circ`, meaning the slopes assigned to profile
  `i` but to no earlier profile"; routing item, tex **L1115-1116**
  "effective-image collapse is either routed to an earlier profile or the
  full-image certificate (FI) is proved"; retention at image scale, tex
  **L4855-4857** "Deleting earlier cells can only decrease every fiber";
  `lem:profile-atlas`, tex **L4781-4782**
  "arbitrary planted subsets or an unproved decomposition" / "including either
  could create exponentially many"; `lem:profile-multiplicity`, tex **L5030** "all
  data outside the moving support is `o(n)` bits"; per-line profiles, tex
  **L1448** "the number of nonempty pairs".
- **FROM the tex:** `lem:first-match-bound` disjoint union (L1526-1538); closed
  ledger items (2)/(4) (L1106-1118); `lem:profile-atlas` (L4772-4784);
  `lem:profile-multiplicity` (L5028-5033); per-line census (L1447-1450).
- **BEYOND the tex:** the single retained collapse cell's per-line projection
  degree (T-PAY-RES).
- **Status:** **DISCHARGED modulo T-PAY-RES**; T-PAY-RES **SUPERSEDED-BY `#642`**
  (resolved to `<= |F_r|`). It is (ii) of S1. Two tex disambiguation findings
  (L869 = disjoint-union charge; A5 scope for routed profiles) -> S3.

### Row 6 -- RC_occ mass-weighted saturation payment (`#636`, `saturation_payment_repair.md`)

- **Statement:** The saturation half of `prop:saturation-payment` is repaired by
  the exact mass-weighted identity `RC_occ` already in
  `lem:exact-occupancy-compiler`: `|Z(C)| <= |R(C)| = sum_w 1/nu`, so a heavy
  slope-atom with a geometric tail self-pays (`rho_block = (t+1)^2/mass <= 1`). The
  orientation floor (`#634`) is re-classified as a **collapse** cell (routed), not
  a saturation counterexample.
- **Tex consumer/anchor:** `lem:exact-occupancy-compiler`, tex **L5677** `\abs{\Ccal}=\sum_{\rho\in\Rcal(\Ccal)}\nu_{\Ccal}(\rho)`, **L5683**
  `\tag{RC$_{\rm occ}$}`; `prop:saturation-payment`, tex **L4727** "A saturation
  cell is paid if the projection from raw witnesses to the" / **L4730** "final
  image has a direct distinct-slope estimate at the profile scale" / **L4738**
  "goes in the wrong direction".
- **FROM the tex:** `RC_occ` (L5674-5698) -- the repair is **already in the tex**;
  `prop:saturation-payment`'s two routes (L4726-4739).
- **BEYOND the tex:** a lower bound on the **dominant** fiber (not uniform `H`);
  fails on the uniform-tail witness unless `M >= A_eff^2` (borderline).
- **Status:** **DISCHARGED on the heavy-atom geometric-tail product class**;
  **adjacent** to the span face (saturation has `(FI)`). NEEDS-PRINTING: replace
  `RC1`'s uniform `H` by `RC_occ` (S3). Uniform-tail borderline -> OPEN corner S4.

### Row 7 -- T-FIELD per-line law `delta <= |F_r|` (`#642`, `c7_collapse_image_degree.md`)

- **Statement:** The retained collapse cell's per-line degree is **not** a free
  enumerative constant; it is the received line's **field of definition**:
  `delta_lambda(r) <= |F_r|` (subfield confinement), tight at `log|F_r| =
  Theta(n)` via the paper's own promoted countertheorem. Supersedes `#635`'s vague
  "`e^{o(n)}` per line".
- **Tex consumer/anchor:** `thm:subfield-confinement-full`, tex **L1933**
  "Hence every MCA-bad slope of" / **L1934** "a `B`-valued received line lies in
  `B`"; field of definition, tex **L2290** "The field of definition is the
  smallest"; forcing witness `thm:intro-countertheorem`, tex **L804**
  `\exp((h(\alpha)/4+o(1))n)` / **L817** "threshold counterexamples result".
- **FROM the tex:** `thm:subfield-confinement-full` (L1930-1943); field of
  definition (L2290-2292); `thm:intro-countertheorem` (L796-819).
- **BEYOND the tex:** a bound on `|F_r|` (the received-line field) -- carried to
  Row 8.
- **Status:** **DISCHARGED** (PROVED from subfield confinement); it is (iii) of
  S1. Residual `(FI-field)` -> Row 8. Finding: the C7 cell is **unlabelled**
  (L2440) -> S3.

### Row 8 -- `(FI-field)` reduces to `(FI-field')` (`#645`, `fi_field_discharge.md`)

- **Statement:** In the full-field normalization `e_MCA(r) = delta(r)/|F| <=
  |F_r|/|F|`, a prize-relevant line has `log|F_r| >= log|F| - 128`, so
  `(FI-field)` on prize-relevant lines is **equivalent** to the ambient-field
  hypothesis `(FI-field') : log|F_n| = o(n)`. Discharged unconditionally on the
  poly-field class; not implied by `(A1)-(A7)` (none bound `|F_n|`); every known
  `Theta(n)`-field witness is diluted (`e_MCA = e^{-Theta(n)}`).
- **Tex consumer/anchor:** `thm:subfield-confinement-full` normalized, tex
  **L1933-1934**; challenge set, tex **L204** "is the challenge set, meaning";
  full-field / scalar extension, tex **L575** "challenge field `F` may be a scalar
  extension, meaning that the"; prize target, tex **L491** "MCA error at most a
  cryptographic target such"; received pair, tex **L187** "A received pair
  `r=(r_0,r_1) in (F^D)^2` determines the"; adversary uniformity, tex **L226**
  "bound is uniform over received pairs, whereas a lower construction need"; scope
  remark, tex **L837** "is polynomial-size, whereas the scalar extension used to
  separate" / **L840** "verify its field and reserve hypotheses"; separation gate
  `thm:prefix-to-line-hardness`, tex **L2079** `\abs\F-n>k\binom N2`.
- **FROM the tex:** subfield confinement (L1930-1934); the full-field challenge
  normalization (L204, L491, L575); the quantifier (L187, L226); the scope remark
  naming the field hypothesis (L829-840); eq (4.5) (L2073-2094).
- **BEYOND the tex:** `(FI-field')` itself -- a row-level ambient-field bound
  `log|F_n| = o(n)`, absent from `(A1)-(A7)`.
- **Status:** **DISCHARGED on the poly-field class (unconditional)**;
  **NEEDS-PRINTING** as an `(A0)` clause otherwise (S3). It is (iv) of S1. The
  challenge-set quantifier (proper subset `Gamma subsetneq F`) -> OPEN corner S4.

### Row 9 -- Thick-form comparison lemmas (`#638`, `thick_form_comparison_lemmas.md`)

- **Statement:** Against DannyExperiments' multiplicity-thick `(S_E)^thick`
  (`#629`): `(S_E)^thick` is **strictly weaker** than hughes `(LS)` (`#564`) and
  **orthogonal** to the LegaSage C9 razor (`#585`) -- razor NO does not imply
  `(S_E)^thick` (block-parabola witness, thick-band energy 0). Lattice: set-dodged
  `(S_E) < (S_E)^thick < (LS)`.
- **Tex consumer/anchor:** none new in the tex -- concerns the supplement's
  **lattice position** vs external inputs. Shares the image clause `(FI)`, tex
  **L4844**. External anchors: `(LS)` = `#564`, razor = `#585` (audit notes, not
  the frontiers tex).
- **FROM the tex:** `(FI)` (L4844) as the common target of all three objects.
- **BEYOND the tex:** `(S_E)^thick` (the live supplement, `#629`), `(LS)`
  (`#564`), the razor (`#585`) -- all input-specific external objects.
- **Status:** **DISCHARGED** (AUDIT/PROVED). NEEDS-PRINTING: cite the **thick**
  form; the stale set-dodged `(S_E)` sections 3.1/3.2 of
  `minimal_phase_supplement.md` are **retracted** (`#629`) -> S3.

### Row 10 -- `|F|^{1/2}` per-line cap refuted (`#647`, `collapse_field_cost.md`, on-branch, NOT integrated at 5c9aab7)

- **Statement:** `delta(r) <= |F|^{1/2+o(1)}` is **not** forced on collapse cells:
  an explicit pure-collapse line (`m=3, w=1, F=F_{p^2}`) carries `delta =
  (p-1)(p-2)/6 = Theta(|F|)`, refuting the `1/2` exponent. Harmless (poly-field,
  `#645` column 1) but **kills** the free-closure route; `(FI-field')` remains
  genuinely load-bearing.
- **Tex consumer/anchor:** separation gate `thm:prefix-to-line-hardness`, tex
  **L2079** `\abs\F-n>k\binom N2` (sufficient-not-necessary); `thm:subfield-confinement-full`, tex **L1933-1934** (T-FIELD upper); scope remark, tex
  **L837-840**.
- **FROM the tex:** eq (4.5) (L2073-2094); subfield confinement (L1930-1934); the
  scope remark's "sufficient, not necessary" gap (implicit at L829-840).
- **BEYOND the tex:** the refuted `|F|^{1/2}` sharpening (a would-be beyond-tex
  theorem) is DEAD; confirms `(FI-field')` (Row 8) is beyond-tex and necessary.
- **Status:** **SUPERSEDED/DEAD** for the sharpening; **confirms Row 8's
  NEEDS-PRINTING**. (Note: not integrated at `5c9aab7`; on branch
  `thresholds-collapse-field-cost`, commit `e5c2baa`.)

### Bottom line

**10 arc statements, by S2 row-status:
6 DISCHARGED (Rows 2,4,5,6,7,9 -- the closure steps of S1),
3 SUPERSEDED (Rows 1,3,10 -> `#625`/`#635`/`#645`, each a monotone sharpening),
1 NEEDS-PRINTING (Row 8 = the single printed input `(FI-field')`),
0 strictly-OPEN.** The one residual **input** is `(FI-field')`, sufficient
(T-FIELD) and necessary on the prize-relevant class (`#645`/`#647`); S3 expands
it into 5 concrete print-edits. The honestly-open **corners** (S4) are all
adjacent (image face: `#646`, `#636` uniform tail, `#564`) or non-reopening
(`#647` Case-B, `#644` critical-window, `#645` proper-subset) -- none is a
dependency of a DISCHARGED row. **No DISCHARGED row cites an OPEN dependency**
(verifier-checked, S2 consistency): every discharged step rests only on other
discharged steps or on `(FI-field')`, which is NEEDS-PRINTING, not an open gap.

---

## S3 -- WHAT MUST BE PRINTED, final form

Superseding `#635`'s four-item entry with the `#642`/`#645`/`#647` resolution.
Replace the L2450-2454 "assumed enumerative input" reading and the L869 count
guard with:

1. **`(FI-field')` as an `(A0)` clause in `def:admissible-sequence` (L896).** *For
   the prize's smooth/circle row sequence the ambient challenge field satisfies
   `log|F_n| = o(n)` (equivalently `[F_n:B_n] = o(n/log|B_n|)`): the challenge is
   not taken over a scalar extension of superpolynomial degree.* This is the "field
   hypothesis" the scope remark already names (`rem:intro-countertheorem-scope`,
   tex **L837-840**, "The domain field `B_n` is polynomial-size, whereas the scalar
   extension ... has `log|F_n| = Theta(n)`"). It is **necessary** (no `(A1)-(A7)`
   clause bounds `|F_n|`; the free `|F|^{1/2}` route is refuted, `#647`) and
   **sufficient** (subfield confinement, `#642` T-FIELD:
   `delta_lambda(r) <= |F_r| <= |F_n| = e^{o(n)}`). Place it in
   `def:admissible-sequence`, **not** the L2450 C7 paragraph -- once the ambient
   field is poly-size the C7 collapse cell needs no per-line certificate at all.

2. **The C7 ledger choice, final resolution (replaces the L2450-2454
   assumed-inputs reading).** The paragraph currently ends "The cell is
   constructible in the projective locator and explanation incidence, but its
   projection degree remains an enumerative input" (tex **L2450-2452**). Replace
   the "enumerative input" clause, per `#635`+`#642`+`#645`, by:
   - **the envelope charge is a first-match disjoint union** `sup_r sum_i
     |Z_i^circ| = sup_r |Z_a(r)|` (`lem:first-match-bound`, tex **L1526-1538**),
     each slope counted once, so profile multiplicity does not multiply it and the
     "countertheorem" (L889-890) is a per-profile overcount that does not fire;
   - **routed collapse profiles contribute 0** (`Z_i^circ = empty`, tex
     **L877-881**/**L1115-1116**);
   - **the single retained collapse cell's per-line degree is
     `delta_lambda(r) <= |F_r|`** by subfield confinement (`thm:subfield-confinement-full`, tex **L1930-1934**), hence `<= |F_n| = e^{o(n)}`
     under `(FI-field')`.
   Give the C7 cell a **label** (`cell:sat-collapse`) so the ledger can `\cref` it
   (it is unlabelled at L2440).

3. **The saturation half:** replace `RC1`'s uniform lower occupancy `H` by the
   exact mass-weighted `RC_occ` **already present** in
   `lem:exact-occupancy-compiler` (tex **L5674-5698**): the saturation cell is paid
   on the heavy-atom product class by the dominant atom (`#636`). This is an
   image-face/count item, adjacent to the span face.

4. **A5 scope for routed profiles.** `(A5)` (`R_N < char B_N`, tex **L935-941**)
   has no stated scope for **routed** effective-image-collapse profiles (which
   carry `R_prod = 2k >= char`). Print: routed/atlas profiles are charged by
   **description entropy** (`lem:profile-multiplicity`, tex **L5028-5033**) and are
   **exempt** from `(A5)`; `(FI-field')` constrains the received-line field, not
   the profile's `R` (`#635` finding 2, `#642` finding 3).

5. **Supplement citation.** Cite the multiplicity-**thick** `(S_E)^thick` (`#629`
   `(C4)/(C5)`), not the retracted set-dodged `(S_E)`; the stale sections 3.1/3.2
   of `minimal_phase_supplement.md` are superseded by `thick_form_comparison_lemmas.md` (`#638`). Lattice for the record: set-dodged
   `(S_E) < (S_E)^thick < (LS)`.

---

## S4 -- OPEN CORNERS (honestly)

One line each: what would close it, who is on it.

1. **Case-B exponential equidistribution (`#647`, the span-face open corner).**
   Whether a **prize-relevant** line can have `delta ~ |F|` with `log|F| =
   Theta(n)` -- a low-degree pole and a **deep** fiber whose Vandermonde image
   equidistributes over `F`. **Closes if:** the deep fiber's free-symmetric
   coordinates are shown **not** to equidistribute over `F` at `[F_r:B] =
   Theta(n/log q_0)` (or, positively, `(FI-field')` is imported). **On it:**
   holmbuar (`#647`), reducible to the Codex `[SUPERCRIT]` transition theorem.

2. **The challenge-set quantifier reading (`#645`, both readings carried).** For a
   **proper** challenge subset `Gamma subsetneq F`, the per-line count rescales by
   `|Gamma|/q` (tex L6204-6206, averaging identity), leaving the leading `delta/q >
   eps` comparison unchanged; but `lem`/L1047-1049 warns "`|Gamma_n|` alone does
   not determine it" -- a certified challenge-intersection lower bound. **Closes
   if:** a challenge-intersection theorem replaces the `|Gamma|`-alignment
   heuristic. **On it:** holmbuar (`#645`), Codex `#624` Lean of the eq (13.3)
   composition is the anchor.

3. **The joint `(phi,gamma)` packing tradeoff (`#646`, image face -- ADJACENT,
   not span).** The degree-2 moment-map max-fiber rate `phi* = log 2`
   (`moment_map_max_fiber.md`, revising `#643`'s conjectural constant) is an
   **image-face** result: it bounds the saturation/count side, not `(FI)`.
   Mentioned for completeness; it does **not** bear on the span-face closure. **On
   it:** the moment-map lane (`#646`).

4. **The saturation uniform-tail borderline (`#636`).** The `#625` uniform-tail
   heavy-atom witness has `|Z| = A_eff` distinct slopes, so `RC_occ` pays only if
   the support is rich (`M >= A_eff^2`). **Closes if:** either every admissible
   saturation violator is shown geometric-tailed, or the uniform-tail cell is
   routed as collapse. **On it:** holmbuar (`#636`); adjacent (image face).

5. **hughes `(LS)` (his corner, untouched).** The signed multilevel large sieve
   (`#564`) with its `p^{w/2}` square-root cancellation targets the sharp
   polynomial `N <= n^3`; it is **strictly stronger** than `(S_E)^thick` and lives
   on the image/count face. **Closes if:** hughes' sharp signed bound lands.
   **On it:** scottdhughes.

6. **Codex critical-window (their corner).** The antipodal phase bracket `(CW)`
   (`#644`, `orientation_prefix_phase_transition.md`) has an unclosed gap: for
   `c >= 2 log 2 / log 3` the lower rate is 0 while the upper endpoint `e^{-c/12}
   log 2 > 0` for every fixed `c`. **Closes if:** the sign-cube intersection with
   the affine Frobenius-cyclic code is controlled (does the true rate vanish at
   finite `c`?). **On it:** the Codex team (`#634`/`#644`). This is a pre-atlas
   orientation-family question; by `#636`/`#642` the orientation floor is a
   **collapse** cell routed by `(FI)`, so it does **not** open the span-face
   closure -- it refines the collapse witness only.

---

## S5 -- CONSISTENCY SWEEP

The arc checked against itself. Every supersession made explicit; no two notes
assigning contradictory statuses to the same tex anchor.

**Supersession 1 -- `#626`'s count reading revised by `#635`.** `#626` reads the
L869 guard ("subexponentially many profiles ... the sum and maximum have the same
exponential scale", tex **L870**) as a **profile count** and proves it "busted" by
the `e^{Omega(N)}` binomial tail, verdict PARTIAL/"the countertheorem". `#635`
proves the operative charge is the **first-match disjoint union**
(`lem:first-match-bound`, tex **L1534-1535**), a **mass** insensitive to profile
multiplicity, and that the same `e^{Omega(N)}` family is exactly the "arbitrary
planted subsets" `lem:profile-atlas` (tex **L4781-4782**) already excludes.
**Resolution:** `#626`'s COUNT is correct but is **not** the load-bearing quantity;
`#635` supersedes the *reading*, not the count. Same anchor (L869-870, L889-890),
non-contradictory statuses (`#626`: count busts guard; `#635`: guard was never the
operative statement). Recorded in Row 3 and Row 5.

**Supersession 2 -- `#635`'s T-PAY-RES ("`e^{o(n)}` per line", vague) resolved by
`#642` (`delta <= |F_r|`, exact) and reduced by `#645` (`(FI-field')`).** `#635`
leaves "the C7 collapse cell's own image-scale projection degree" as one open
per-line cell; `#642` proves it equals the field of definition
(`thm:subfield-confinement-full`, tex **L1933-1934**), and `#645` reduces
prize-relevance to `(FI-field')`. **Resolution:** a monotone sharpening chain, no
contradiction; T-PAY-RES is not left OPEN -- it is DISCHARGED into the printed
input `(FI-field')`. Recorded in Rows 5,7,8.

**Supersession 3 -- `#636`'s supply box: `#634` proved-vs-modeled.** `#636` Rung 4
initially used `Q_img = 1`, `G_1 = q^{w/2}` exact, uniform fibers as if proved;
the corrected supply box (adopting the Codex team's 2026-07-11 consumer-hypothesis
audit) states `#634` PROVES only (i) `|Phi_u(O)| <= q^{ceil(u/2)}`, (ii) one heavy
prefix with `>= J_z` orientations, (iii) a separating pole giving `J_z` slopes on
the complete fiber -- the sharp equalities are **modeled**, exact only at the `F_9`
toy. `#644` (`orientation_prefix_phase_transition.md`) independently confirms this:
"From PR #634 alone, exact orientation image size, asymptotic uniformity of prefix
fibers, `Q_img=1`, exact `G_1`, and one received line realizing all of `O_r` are
not proved." **Resolution:** `#636`'s corrected supply box and `#644` **agree**;
the orientation floor is a **collapse** cell (`G_1 >= J_z` PROVED) routed by
`(FI)`, not a saturation counterexample. No contradiction. Recorded in Row 6 and
S4.6.

**Supersession 4 -- `#643`'s conjecture revised by `#646` (image face, for
completeness).** `#646` decides the degree-2 moment-map max-fiber rate
`phi* = log 2`, revising `#643`'s earlier conjectural constant
(`moment_map_max_fiber.md`; agents-log L55-57). **Both are IMAGE-face**, adjacent
to the span-face arc; neither bears on `(FI)`. Recorded in S4.3. No span-face
anchor is touched.

**The one composition point that could have been a contradiction (pinned, NOT a
gap).** `#635` T-PAY(i): every routed collapse **profile** has `Z_i^circ =
empty` (charge 0). `#642` Rung 1c: the collapse **cell** (the routing target) has
`Z^circ` **NOT** empty -- it carries the full slope set `delta_lambda(r)`. These
refer to **different objects**: the `e^{Omega(N)}` source **profiles** (routed
*away*, charge 0) versus the single **target cell** they are all routed *to*
(charge `delta_lambda(r) <= |F_r|`). The tex routing clause is explicit (tex
**L877-881**): collapse is "assigned by the first-match rule to an **earlier**
profile so that its slopes ... are removed from the **later** residual". `#635`
charges the later residual (0); `#642` charges the earlier target (`<= |F_r|`).
**Two ends of one routing arrow -- consistent, no double-count, no gap.** This is
the load-bearing consistency check for S1 (ii)+(iii), and it holds.

**Status-collision scan.** No two arc notes assign contradictory statuses to the
same tex anchor. The shared anchors -- C7 cell (L2440-2454), `(FI)` (L4844),
`def:primitive-q` (L4918), `lem:first-match-bound` (L1534-1535),
`thm:subfield-confinement-full` (L1933-1934), the countertheorem (L796-819) and
its scope (L829-840) -- carry a single consistent reading across
`#622/#625/#626/#627/#635/#636/#642/#645/#647`. The only status *changes* are the
four supersessions above, each a monotone sharpening, each recorded.

**OPEN-GAP verdict:** **NONE in the composition.** The closure statement (S1) is a
genuine proof-by-citation; its single non-theorem is the printed input
`(FI-field')` (NEEDS-PRINTING, not a gap). The honestly-open items (S4) are all
either adjacent (image face: `#646`, `#636` uniform tail, `#564`) or refinements
of the collapse witness that do not reopen the span-face closure (`#647` Case-B,
`#644` critical-window), plus one quantifier-reading residue (`#645` proper
challenge subset) carried in both readings.

---

## Verdict ledger

| item | verdict | label |
|------|---------|-------|
| closure statement composes (S1), no new math gap | proof-by-citation, residual = printed input | **PROVED-by-citation** |
| every S2 tex anchor verbatim at `5c9aab7` (+/- 3 lines) | ~40 anchors checked | **AUDIT** (verifier) |
| MASTER-2 two-cell + T-DET detection = theorems | `#625`/`#627` | **DISCHARGED** |
| T-PAY disjoint-union charge; countertheorem dissolved | `#635` | **DISCHARGED mod T-PAY-RES** |
| T-PAY-RES = `delta <= |F_r|` (field of definition) | `#642`, supersedes `#635` | **DISCHARGED** |
| `(FI-field) <=> (FI-field')` on prize-relevant lines | `#645` (RED) | **DISCHARGED reduction** |
| `(FI-field')` in `def:admissible-sequence`; C7 ledger rewrite; RC_occ; A5 scope; thick citation | S3 | **NEEDS-PRINTING** |
| `#626` count reading; `#635` T-PAY-RES; `|F|^{1/2}` cap | superseded by `#635`/`#642`/`#647` | **SUPERSEDED (explicit)** |
| Case-B equidistribution; challenge-subset; uniform-tail; `(LS)`; `(CW)`; `#646` | S4 | **OPEN / ADJACENT** |
| profile-`Z^circ=empty` (#635) vs cell-`Z^circ`-full (#642) | two ends of one routing arrow (L877-881) | **CONSISTENT (pinned)** |
| span face closes on poly-field prize rows, unconditional | `(FI-field')` automatic | **PROVED-by-citation** |

**Proposed ledger entry (for the maintainer).** *Consolidating the span-face arc.
On a ledger-admissible sequence (`def:admissible-sequence`, L896-954) satisfying
the ambient-field clause `(FI-field') : log|F_n| = o(n)` -- automatic on the
prize's poly-size smooth/circle rows -- the span face of the first-match envelope
closes. Every `(S_E)`-violating admissible leaf is product/profile-structured
(`#622` T3), fires a router-decidable pre-primitive trigger (`#625` MASTER-2
`E+1 <= G_1*Q_img`, `#627` T-DET: collapse `L<<A` at L2453-2454 or ray-saturation
`max_s f_s > barN^img` at L2440-2449 = negation of `def:primitive-q` L4918), and
is routed (L877-881) with its first-match set `Z_i^circ = empty` (`#635` T-PAY,
disjoint-union charge `lem:first-match-bound` L1534-1535). The single retained
effective-image rank-collapse cell charges `delta_lambda(r) <= |F_r|` distinct
slopes per line (`#642` T-FIELD, subfield confinement L1933-1934), hence `<= |F_n|
= e^{o(n)}` under `(FI-field')` (`#645` (RED): prize-relevance forces `log|F_r| >=
log|F| - 128`). The saturation half is paid separately by the mass-weighted
`RC_occ` already in `lem:exact-occupancy-compiler` (L5674-5698) on the heavy-atom
product class (`#636`); it has full image, so it does not threaten the span face.
No `(A1)-(A7)` clause bounds `|F_n|`, and the per-line `|F|^{1/2}` cap that would
have made `(FI-field')` free is refuted by an explicit `Theta(|F|)` collapse line
(`#647`), so `(FI-field')` is a genuine printed input -- sufficient (T-FIELD) and
necessary on the prize-relevant class. Print: `(FI-field')` as an `(A0)` field
clause; the C7 ledger as first-match disjoint union + routed-to-earlier +
`delta <= |F_r|` (labelling the cell `cell:sat-collapse`); `RC_occ` for the
saturation half; A5 exemption for routed profiles; and the thick supplement
`(S_E)^thick`. The composition uses no new theorem; the residual is exactly the
one printed input. Open corners (all adjacent or non-reopening): Case-B
equidistribution (`#647`), the proper-challenge-subset intersection (`#645`), the
saturation uniform-tail borderline (`#636`), hughes `(LS)` (`#564`), the Codex
critical-window `(CW)` (`#644`), and the image-face moment-map rate `#646`.*

---

## Reproducibility

```sh
ulimit -v 2097152
python3 experimental/scripts/verify_span_face_synthesis.py   # RESULT: PASS
```

Arc verifiers (each reproduces its own note's PASS count; not re-run here):

```
verify_se_admissible.py               RESULT: PASS (208/208)     #622
verify_c7_routing_spectrum.py         RESULT: PASS (731/731)     #625
verify_c7_degree_enumeration.py       RESULT: PASS (233/233)     #626
verify_routing_exhaustiveness.py      RESULT: PASS (3417/3417)   #627
verify_collapse_payment.py            RESULT: PASS (1210/1210)   #635
verify_saturation_payment.py          RESULT: PASS (28/28)       #636
verify_c7_collapse_image_degree.py    RESULT: PASS (115/115)     #642
verify_fi_field_discharge.py          RESULT: PASS (59/59)       #645
verify_thick_form_comparison.py       RESULT: PASS (27/27)       #638
verify_collapse_field_cost.py         RESULT: PASS (42/42)       #647 (on-branch)
```
