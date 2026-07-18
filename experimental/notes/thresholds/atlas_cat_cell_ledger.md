# The (CAT) exhaustion ledger: a per-cell atlas payment audit

**Hard input.** Hard input 1 (`agents.md`) --- the **witness-exhaustive
first-match atlas**, condition **(A2)** of `def:admissible-sequence`
(`experimental/asymptotic_rs_mca_frontiers.tex`).  This note builds the
**(CAT)** residual named by the print-audit `atlas_missing_witness.md` (PR
`#536`) and the A6 print-audit `a6_atlas_print_audit.md`: the
catalogue-completion audit that turns the scattered integrated per-cell
payments into a single per-cell atlas ledger and asks whether they **compose**
into (A2) --- exhaustion **and** an `e^{o(n)}` summation.

## Status

`CATALOGUE LEDGER (AUDIT) / EXHAUSTION COMPOSES = THEOREM (PROVED, unconditional)
/ PER-PAID-CELL SUMMATION COMPOSES (PROVED on the stated regimes, 5 cells) /
FULL-CATALOGUE SUMMATION BLOCKED AT FOUR NAMED CELLS (CONDITIONAL) / (CAT)
RESIDUAL = {C3 planted census, C7 projection degree, C8 higher-dim core, C9
Sidon payment}, collapsing to the manuscript's own hard inputs 3 and 4/5 plus
one local combinatorial census / (UNIF) = the outer per-line quantifier over
this ledger, prerequisite (CAT).`

Every `.tex` quote below is byte-verified at its cited line (tolerance-window
`+/-2`, offset `0`) by `experimental/scripts/verify_atlas_cat_ledger.py`
(stdlib-only, deterministic, `--check` -> `RESULT: PASS (219/219)`,
`--tamper-selftest`).  Machine-readable ledger at
`experimental/data/certificates/atlas-cat-ledger/atlas_cat_ledger.json`.
Block D loads and SHA-256-pins that JSON, then checks its cell semantics, tally,
composition verdicts, verifier results, and corrected C8 producer provenance;
it is no longer an unbound sidecar.
**No `.tex`/`.pdf` is edited.**  PR numbers are the consumed notes' own lane /
consumer labels; note files are cited by path and exist at this snapshot.

Label key (`agents.md` dialect): **PROVED** / **CONDITIONAL** /
**CONJECTURAL** / **EXPERIMENTAL** / **AUDIT** / **COUNTEREXAMPLE**, plus house
tags **PAID** (a cell whose distinct-slope projection has a certified
`e^{o(n)}(1+\barN)` bound in the sense of `def:paid-cell`, L2306--2313) and
**UNPAID** / **CONDITIONAL** (payment not established unconditionally, with the
sharpest statement of what a payment must provide).

**Credit.** The printed catalogue and (A2) are the manuscript's own. The
free-exhaustion backstop is `atlas_missing_witness.md` (PR `#536`). The
routing-detection theorem is `routing_exhaustiveness.md` (PR `#627`) with
`c7_routing_spectrum.md` (PR `#625`, MASTER-2) and `c7_degree_enumeration.md`
(PR `#626`). The C5 arc is `noncyclic_c5_slope_count.md` (PR `#607`),
`c5_defect_magnitude.md` (PR `#610`), `c5_covering_constant.md`. The C6 laws are
`atom_differential_cell_laws.md` (upgrading PR `#446`). The C8 arc is
`bc_moving_root.md`, `ray_compiler_balanced_core.md` (PR `#528`),
`balanced_core_kappa_growth.md` (PR `#534`, corrected by PR `#868`),
`split_pencil_ray_collapse.md` (matching PR `#518`). The C9 reduction chain
is `c9_payment_reduction_map.md` (PRs
`#575`--`#582`), `sidon_special_case_proof.md`, `prefix_flatness_power_sum_lean.md`.
The C1/C2/C4 payments are `a4_quotient_major_compiler.md` (PR `#465`),
`quotient_census_window_compiler.md`,
`20260709_m31_chebyshev_fixed_remainder_floor/cap25_v13_m31_chebyshev_fixed_remainder_floor.md`,
`agreement_weighted_transverse_secant.md`,
`f17_32_high_agreement_tangent_table.md`. The input-4 factoring reused here is
`profile_envelope_completeness.md`.

---

## 1. The printed cell catalogue (verbatim, `sec:cell-catalogue`, L2366--2496)

The catalogue's own framing fixes the audit standard (L2368--2369):

> "The catalogue below is a language for row-specific proofs, **not a theorem**
> that every displayed locus is automatically paid."

So the tex does **not** assert that `C1`--`C9` partition the witnesses, nor
that they are paid; both are the content of **(A2)** (L905--907):

> "A first-match atlas **covers every bad-slope witness** and has `e^{o(n)}`
> profiles.  The total *distinct-slope* contribution of its algebraic cells is
> **at most `e^{o(n)} E_n(a_n)`**."

...held "uniformly in every received line" (`def:admissible-sequence` preamble,
L897--899).  The nine classes (labels `C1`--`C9` as extracted by `#536`):

| # | class (anchor) | defining condition (verbatim, abridged) |
|---|---|---|
| C1 | Quotient/periodic (L2374--2377) | "pullbacks along a nontrivial map `pi:D->D'`: support membership is constant on the relevant fibers of `pi`" |
| C2 | Dihedral/Chebyshev (L2385--2387) | "quotient cells with an additional involution, usually inversion `u|->u^{-1}`" (Dickson/Chebyshev-detected) |
| C3 | Planted-block (L2399--2407) | "a predetermined group of support positions forced by an algebraically controlled common divisor `P`"; **"arbitrary planted subsets are not one profile"** |
| C4 | Tangent/deep/common-line (L2409--2416) | "rank-defective contact between the received line and the support-restricted evaluation incidence"; **"rank drop alone is not payment"** |
| C5 | Extension/field-descent (L2422--2427) | "data defined over a proper subfield (field descent) or factors only after enlarging the coefficient field (extension)" |
| C6 | Differential-locator (L2429--2438) | "the locus where [the Vandermonde/Hasse Jacobian] loses its expected rank" |
| C7 | Saturation/effective-image-collapse (L2440--2455) | "passing through these displayed images with their actual fiber cardinalities"; "boundary map reaches exponentially fewer boundary values than its ambient codomain"; **"projection degree remains an enumerative input"** |
| C8 | Balanced-core/split-pencil (L2456--2474) | "a pair of equal-degree monic residual locators with a common depth-`w` prefix"; **"higher-dimensional balanced-core charts require a proved decomposition or a direct ray estimate"** |
| C9 | Fourier/Sidon-heavy analytic (L2476--2492) | "a primitive prefix fiber [that] may be too large while having exponentially small additive energy"; "deliberately kept separate from the constructible atlas" |

The printed first-match **order** (L5181) is: "algebraic major arcs first, then
a separately certified Sidon/Fourier cell, and only then the high-energy
primitive inverse step."

---

## 2. Per-cell ledger: which integrated result pays each cell

Payment target is `def:paid-cell` (L2307, L2312): `|Z_i^\circ| <= U_i <=
e^{o(n)}(1+\barN_i)`, uniformly in the received line and the realized profile.
Every row's status carries the hypotheses its proof uses.

| # | class | paying note (PR) | regime / hypotheses | profile-count contribution | verdict |
|---|-------|------------------|---------------------|----------------------------|---------|
| **C1** | quotient/periodic | `a4_quotient_major_compiler.md` (`#465`), `quotient_census_window_compiler.md` | cyclic quotient towers; complete uniform fibers (A1) | divisor count **subexponential** (`lem:profile-atlas` L4778--4779) | **PAID** |
| **C2** | dihedral/Chebyshev | `.../cap25_v13_m31_chebyshev_fixed_remainder_floor.md` | dyadic Chebyshev towers | **logarithmic** (`lem:profile-atlas` L4780) | **PAID** |
| **C3** | planted-block | *(printed requirement L2405--2407)* | needs a proved subexponential census of the common divisor `P` | `lem:profile-atlas` **EXCLUDES arbitrary planted** (L4781--4782: "could create exponentially many profiles") | **CONDITIONAL/UNPAID** |
| **C4** | tangent/deep/common-line | `agreement_weighted_transverse_secant.md` (PROVED), `f17_32_high_agreement_tangent_table.md`; `thm:deep-regime-upper`, `prop:tangent-payment` | fixed low-excess charts + deep regime; general high-excess invokes `prop:tangent-payment` (independent minors) | deep regime **exact**; one-minor-per-slope bounded | **PAID** (low-excess/deep) |
| **C5** | extension/field-descent | `noncyclic_c5_slope_count.md` (`#607`), `c5_defect_magnitude.md` (`#610`), `c5_covering_constant.md` | deployed Frobenius families; `p \nmid |G|` | slope count = cyclotomic defect `p^{d_p(G,I)}`, `d_p = o(|G|)` on deployed families -> `e^{o(n)}` | **PAID** |
| **C6** | differential-locator | `atom_differential_cell_laws.md` (upgrades `#446`) | admissible leaves with `R < char` (A5) | differential `K`-rank defect law proved; **inert `index=1` under `R<=p`** | **PAID** |
| **C7** | saturation/effective-image-collapse | `routing_exhaustiveness.md` (`#627`), `c7_routing_spectrum.md` (`#625`), `c7_degree_enumeration.md` (`#626`) | product leaves; MASTER-2 no-third-mode | **detection exhaustive PROVED**; projection degree = binomial tail of `e^{Omega(N)}` candidate profiles | **DETECTION PAID / PAYMENT OPEN** (`#626`) |
| **C8** | balanced-core/split-pencil | `bc_moving_root.md`, `split_pencil_ray_collapse.md` (`#518`); `ray_compiler_balanced_core.md` (`#528`), `balanced_core_kappa_growth.md` (`#534`, corrected by `#868`) | proj. dim 1 (split pencil); higher-dim needs a proved decomposition or direct ray count | split pencil: moving-root incidence `<= n-g` (`eq:moving-root-bound`); higher-dim: `e^{o(n)}` only under (RC) | **PAID (dim 1) / CONDITIONAL on (RC)** (higher-dim = input 3) |
| **C9** | Fourier/Sidon-heavy | `c9_payment_reduction_map.md` (`#575`--`#582`), `sidon_special_case_proof.md`, `prefix_flatness_power_sum_lean.md` | `R>=m` (Newton-injective) or fixed `m`: PROVED-SPECIAL; general linear density `m=Theta(N)`: OPEN | prefix-fibre count `L <= p^w` (`#536`); Sidon moment payment `Gsid = e^{o(Nq)}` (`def:sidon-paid-cell` L5131) UNPROVED at deployed scale | **UNPAID** (general; = hard input 4/5) |

**Tally: 5 PAID `{C1, C2, C4, C5, C6}`, 4 UNPAID/CONDITIONAL `{C3, C7, C8, C9}`.**

---

## 3. The composition (the real question)

(A2) has two clauses: **coverage** ("covers every bad-slope witness") and
**summation** (`e^{o(n)}` profiles, total distinct-slope `<= e^{o(n)} E_n`).
They compose very differently.

### 3.1 Coverage / exhaustion --- COMPOSES (PROVED, unconditional)

> **Claim (exhaustion is free).** For every received line `r` and agreement
> `a >= k+1`, the exact-agreement witness set `W_a(r)` is partitioned by the
> depth-`w` prefix-fibre family `{Phi_w^{-1}(z)}`, `w = a-k-1`: since
> `Phi_w : binom(D,a) -> B^w` is a **total** function and every witness support
> is an `a`-subset, `W_a(r) = coprod_i (W_a(r) cap Phi_w^{-1}(z_i))` is a
> first-match partition (`def:first-match`, L1463) **with no (A2) assumption**.

This is `atlas_missing_witness.md`'s (PR `#536`) proved lemma; the `w=0` case is
the manuscript's own one-cell `binom(D,a)` atlas, `thm:small-effective-dual-closure`
SE2 (L3054--3056, `|Z| <= L\barN = M = binom(|T|,m)`).  On top of it, the printed
routing **detects** exhaustively: `routing_exhaustiveness.md` (PR `#627`) +
`c7_routing_spectrum.md` (PR `#625`, MASTER-2 `E+1 = G_1 Q_img`, no third mode)
prove every `(S_E)`-violating product profile fires a **router-decidable**
pre-primitive trigger among `{C1, C3, C5, C4/C6, C7}`, and that the primitive
step's own max-fiber-Q failure predicate (`def:primitive-q`) is *identical* to
the `C7` ray-saturation trigger --- so no witness escapes every cell.

**Reading.** Exhaustion is **not** the binding half of (A2).  The printed
catalogue's own disclaimer (L2368) is exactly right: `C1`--`C8` alone need *not*
partition (at toy `GENERIC` scale the constructible cells leave up to **27.1%**
of witness mass in the primitive residual, `atlas_missing_witness.md` census);
`C9`/primitive is the analytic **backstop** that absorbs that residual.
**Integrated results changed (A2)'s hypotheses here:** `#536` moved the entire
content of the coverage clause to *payment* (coverage is unconditional),
and `#627`/`#625` upgraded routing detection from a conjecture to a theorem.

### 3.2 Summation --- COMPOSES over the 5 paid cells, BLOCKED over the full catalogue

Over the paid cells `{C1, C2, C4, C5, C6}` the summation **composes**: each
carries growth exponent `0` (C1 subexponential divisor count L4778--4779; C2
logarithmic L4780; C4 deep-regime exact + low-excess bounded; C5 cyclotomic
defect `o(|G|)`; C6 inert `index=1` under `R<=p`), and there are `O(1)` cell
types, so `max` of the exponents is `0` and the sum stays `e^{o(n)} E_n`.
**PROVED on the stated regimes.**

Over the **full** catalogue the summation **does not compose.**  It is blocked
at exactly the four unpaid cells, and each blocker is a *payment/count* gap the
manuscript already names:

- **C3 (planted).** `lem:profile-atlas` (L4781--4782) **excludes arbitrary
  planted subsets** from the `e^{o(n)}` profile count; payment additionally
  requires "a subexponential census of allowed `P`" (L2405--2407). A local
  combinatorial census, not yet supplied. **CONDITIONAL.**
- **C7 (saturation/collapse).** Detection is proved exhaustive, but the
  projection-degree budget of the detected collapse cell is a binomial tail of
  `e^{Omega(N)}` candidate profiles that "remains an enumerative input"
  (L2452); `c7_degree_enumeration.md` (`#626`) proves it is **not payable
  by enumeration**, paid only via (FI)-routing = `#622`/`#625`. **OPEN.**
- **C8 (higher-dim balanced core).** Split pencils (proj. dim 1) are paid
  (`prop:split-pencil-payment`, moving-root `<= n-g`); higher-dimensional charts
  "require a proved decomposition or a direct ray estimate" (L2473--2474,
  `rem:balanced-core-exhaustion` L4764--4767) --- i.e. condition **(RC)**, hard
  input 3. `ray_compiler_balanced_core.md` (`#528`) gives a PROVED per-chart
  transverse-secant bound and a CONDITIONAL (RC) discharge *only on
  bounded-kernel cores*. **CONDITIONAL on (RC).**
- **C9 (Sidon).** The backstop that absorbs the primitive residual is itself
  unpaid at deployed scale: the image-normalized Sidon moment payment
  (`def:sidon-paid-cell`, L5131, `Gsid = e^{o(Nq)}`) is hard input 4/5.
  `c9_payment_reduction_map.md` (`#575`--`#582`) reduces it to a single
  additive-combinatorics razor --- does an `R=2` power-sum fiber at linear
  density `m=Theta(N)` exist that is both near-Sidon (`Delta_s ~ 2/f`) and
  exp-large (`f_s >= e^{eta N}\barN`)? --- with special cases PROVED (`R>=m`
  Newton-injective, `sidon_special_case_proof.md`; fixed `m`) and the
  load-bearing power-sum prefix-flatness inequality Lean-verified
  (`prefix_flatness_power_sum_lean.md`). **UNPAID (general).**

### 3.3 Composed statement of what (CAT) still needs

> **(CAT) reduces to the manuscript's own named hard inputs --- no new open
> object.** Its exhaustion half is discharged unconditionally (`#536` +
> `#627`/`#625`). Its summation half is (A2)'s payment obligation, and that
> obligation is exactly the payment of `{C3, C7, C8, C9}`, which collapse to:
>   1. **C9 -> hard input 4/5** (the Sidon / `(MI)` / `(MA)` moment payment) --- the dominant open, reduced to the `R=2` linear-density near-Sidon razor;
>   2. **C7 + C8(higher-dim) -> hard input 3, condition (RC)** (the ray compiler / projection-degree count);
>   3. **C3 -> a subexponential planted census** --- the one genuinely (CAT)-local combinatorial item, comparatively minor.

This mirrors and reuses `profile_envelope_completeness.md`, which factors hard
input 4 into inputs 2 and 3 with no independent analytic core; (CAT) factors
the same way, with the C3 census as the only piece internal to the atlas.

---

## 4. How (UNIF) relates to this ledger

The ledger above is the **(CAT)** object for **one received line** (and, for the
A6 candidate `C8`-adjacent completed-witness chart, one *scaled canonical
family* `N=500r, kappa=225r, ...`, `#697`/`#704`).  Condition (A2) is asserted
"**uniformly in every received line**" of a genuine asymptotic row sequence
`(C_n, a_n)` as `n -> infinity` (`def:admissible-sequence` preamble L897--899);
`lem:first-match-bound` (L1527) and `def:asymptotic-row` (L2256) carry the same
`for-all`-line quantifier.  **(UNIF)** is precisely this outer universal
quantifier applied to the (CAT) ledger: the *same paid catalogue*, holding as
the line varies and as `n -> infinity`.  **(CAT) is the prerequisite** --- a
per-line or per-family payment (a proved C9 razor on one fiber, or the A6
one-line/one-chart bound) advances (CAT) for one cell **without touching
(UNIF)**, and a uniformity argument that ignored the `C1`--`C9` split would leave
(CAT) open.  Closing hard input 1 needs both at once, exactly as printed. This
note constructs no (UNIF) object; it records only the dependency `(UNIF)`
requires `(CAT)` first.

---

## 5. Per-claim label ledger

| # | claim | verdict | basis |
|---|-------|---------|-------|
| A | 9 cell anchors + composition anchors byte-current at this snapshot, tolerance-window verified, negative-tested | **AUDIT** | verifier BLOCK A |
| B | exhaustion composes: prefix-fibre total partition + routing-detection theorem cover every witness unconditionally | **PROVED** | Section 3.1; `#536`, `#627`, `#625` |
| C | summation composes over the 5 paid cells `{C1,C2,C4,C5,C6}` (each `e^{o(n)}`, `O(1)` types) | **PROVED** (stated regimes) | Section 3.2; verifier BLOCK B |
| D | full-catalogue summation blocked at `{C3, C7, C8, C9}`; SE2/prefix-fibre arithmetic recomputed | **CONDITIONAL** | Section 3.2; verifier BLOCK B |
| E | (CAT) residual = `{C3 census, C7 #626, C8 (RC), C9 Sidon}` -> hard inputs 3 and 4/5 + one census | **AUDIT** | Section 3.3 |
| F | each paying note's own text carries its cited status/PR self-label | **AUDIT** | verifier BLOCK C |
| G | (UNIF) = outer per-line quantifier over (CAT); (CAT) is its prerequisite | **AUDIT** | Section 4 |
| -- | any deployed finite-row, Grand MCA/List, or prize-threshold claim | NOT CLAIMED | this is a hard-input-1 composition audit only |

## 6. Replay

```bash
python3 experimental/scripts/verify_atlas_cat_ledger.py --check
# -> RESULT: PASS (219/219)
python3 experimental/scripts/verify_atlas_cat_ledger.py --tamper-selftest
# -> confirms a corrupted anchor is detected, then RESULT: PASS (4/4)
```
