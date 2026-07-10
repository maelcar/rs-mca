# The deep-prefix Gap-2 span-collapse routing lemma: collapse is Frobenius closure

**Lane:** the last open witness/payment object named at the close of today's
five-packet sweep (PRs #524, #528/#534/#535, #536, #539) --- the **deep-prefix
Gap-2 routing lemma**. PR #539 (`fi_full_image_primitive.md`) split the
full-image certificate (FI) `L >= e^{-o(n)} A` along the scale tower
`L <= A_eff <= A` into Gap-1 (`L >= e^{-o(n)} A_eff`, PROVED free by `(A4)`) and
Gap-2 (`A_eff >= e^{-o(n)} A`), and isolated the single remaining contentful
residue: a deep-prefix **span collapse** `dim_Fp V_g < R f` (`A_eff << A`), which
the paper discharges by **re-routing the leaf "to an earlier structural
profile"** --- but per #539 that re-route is an *assumed enumerative input*
(C7 cell L2451: "its projection degree remains an enumerative input"; the L1115
item-(4) disjunction). This packet **proves the routing lemma by classifying
every span-collapse relation.** It is a **routing / hypothesis-discharge** audit
of the active draft, in the pattern of #524/#536/#539 --- **not** an attack on
`(MI)`/`(MA)` or the entropy-inverse crux (scottdhughes #498/#501/#505, consumed
as input), nor on Danny #529 (M31) or latifkasuli #518 (split-pencil).

**Target file:** `experimental/asymptotic_rs_mca_frontiers.tex` (worktree base
`4e3c4ee`). **No `.tex`/`.pdf` edited.**
**Verifier:** `experimental/scripts/verify_gap2_routing.py` (stdlib-only,
zero-arg, `RESULT: PASS (120 checks)`, ~0.04 s under `ulimit -v 2097152`;
recomputes every gated number with exact `F_{p^d}` arithmetic).

**Highest rung reached: 5 (all rungs traversed).**

**Verdict: `PROVED` (existence half --- the classification is exact and
exhaustive; and the routing obligation is VACUOUS on every admissible power-sum
leaf) + `PARTIAL` (budget: the forbidden-regime re-route inherits cell C5's
catalogued field-descent payment, quantified by PR #451's fiber bound, not a NEW
unconditional bound) + `WALL` (the precise residual) --- NO `COUNTEREXAMPLE`:
the classification leaves no room for a collapse relation with no earlier
profile.**

**One-line headline.** *Every universal `F_p`-linear relation among the
power-sum prefix coordinates on a full slice is a **Frobenius-closure**
relation --- exactly `dim_Fp V_g = |Z_p(q-1,\{1,\dots,w\})|`, the size of the
Frobenius closure of `{1,...,w}` in `Z/(q-1)Z` under `x -> p x` --- so span
collapse is precisely the extension/field-descent cell C5, an earlier
first-match profile; and since collapse holds **iff `w >= p`**, the entire
phenomenon lies **outside** the power-sum admissibility window `R_N < char`
(L940, the primitive-column item; `(A5)`), making the Gap-2 re-route **vacuous
on every admissible power-sum leaf** and, in the forbidden small-characteristic
regime, a **coordinate artifact** that the paper's mandated switch to elementary
coordinates removes.*

**Credit.** The classification is the **exact same primitive** measured at toys
in the integrated `fp-span` lineage: PR #451
(`asymptotic_c9_frobenius_cyclotomic_defect.md`, Theorem 1) --- its Frobenius
closure `Z_p(N,I)` and defect `d_p(N,I)=N-|Z_p(N,I)|` --- and the Lean-verified
closure step `psum_pow`/`root_pow` `(sum_i a_i \omega_i)^p = sum_i a_i \omega_i^p`
of `c9_frobenius_closure_lean_backing.md` (zero-`sorry`). The
`#red = floor((R-1)/p)` reduced-coordinate count of
`cap25_v13_entropy_inverse_fp_span_cell.md` is the same defect for a moment
curve, and its `image subset V_T` containment is the same span-cell mechanism.
GF arithmetic reuses `verify_entropy_inverse_fp_span_cell.py`. Consumes the
scottdhughes ambient `(MI)`/`(MA)` as black box. Builds on #539's Gap tower and
its char-2 probe.

---

## Rung 1 --- EXTRACT: the re-route assertion, its consumers, and what "earlier profile" requires

### 1.1 The object that collapses

`def:effective-span-fourier` region (**EF0/EF1, L2855--2868**): for the
fixed-weight sum map `Psi(S)=sum_{t in S} g(t)` with **power-sum generator**
`g(t)=(t,t^2,\dots,t^R) in B^R` (so `Psi(S)_j = sum_{t in S} t^j = p_j(S)`, the
depth-`R=w` power-sum prefix), the **effective Fourier span** is
```
  V_g = Span_{F_p}{ g(t) - g(t_0) : t in T } ⊆ B^R,   A_eff = |V_g| = p^{dim_Fp V_g}.
```
Ambient `A = |B|^R = p^{R f}`, `f=[B:F_p]`. **Gap-2 fails iff `dim_Fp V_g < R f`**
(span collapse; `A_eff << A`).

### 1.2 The re-route assertion and its consumers (exact, tex-pinned)

| # | line | site | content |
|---|------|------|---------|
| P0 | **L1115--1116** | `(L4)` closed-ledger clause | *disjunction*: "effective-image collapse **is either routed to an earlier profile** or (FI) is proved before an ambient scale is used" --- the routing branch, stated as a hypothesis |
| P1 | **L2440--2452** | C7 saturation / effective-image-collapse cell | "constructible in the projective locator and explanation incidence, **but its projection degree remains an enumerative input**"; "effective-image collapse is the event that a boundary map reaches exponentially fewer boundary values than its ambient codomain contains" |
| P2 | **L4349--4358** | `rem:binary-ambient-image` | ambient moments "do not, **without (FI)**, assert failure of an image-normalized primitive payment. In particular, `p_{2j}=p_j^2` in characteristic two, so the power-sum map has a **Frobenius image collapse**... the exact MCA construction uses the **elementary locator prefix only**" |

**Candidate catcher cells** (the "earlier structural profile"):

| cell | line | test |
|------|------|------|
| C1 quotient/periodic | **L2374** | support descends along `pi:D->D'` (multiplicative-subgroup periodicity) |
| C5 extension/field-descent | **L2422--2427** | "data is defined over a proper subfield (field descent) ... **Frobenius invariance is constructible**. Its natural subfield profile can be larger than the identity profile, so a **direct field-sensitive slope count is required**" |

**What "earlier structural profile" formally requires** (three obligations, the
triple #539 named): (i) **existence** --- the collapse locus *is* a constructible
cell in the catalogue; (ii) **first-match order** --- that cell **precedes** the
primitive leaf, so `Z_i^o` charging is not double-counted. The first-match order
(**L5180--5182**) is *"algebraic major arcs first, then a separately certified
Sidon/Fourier cell, and only then the high-energy primitive inverse step"*; C5
is an algebraic major arc, the collapsing power-sum leaf is a primitive/C9-type
leaf, so **any route to C5 respects the order**; (iii) **mass + budget** --- the
cell's payment applies at the collapsed leaf's parameters and stays within
`e^{o(n)} E_n(a_n)`.

### 1.3 The decisive standing constraint (the admissibility window)

`def:admissible-sequence` (**L896**), primitive-column item (**L935--941**, the
`(A5)` item in #539's labelling):

> "Primitive columns are genuine weighted Vandermonde columns... **Every use of
> power-sum coordinates satisfies `R_N < char B_N`; small-characteristic leaves
> instead retain elementary coordinates or carry a direct Sidon/Q theorem.**"

And the Newton-dictionary boundary (**L6488--6492**): `p_j + q_1 p_{j-1} + ... +
j q_j = 0`, so `q_j` is recoverable from `p_1..p_j` *"when `j` is invertible"*
(i.e. `char > j`), and *"No small-characteristic linearization is claimed; one
must retain elementary coordinates."* **These fix `w < char = p` as the entire
window in which power-sum coordinates are used.** Rung 2 shows this window is
*exactly* the no-collapse window.

---

## Rung 2 --- CLASSIFY: universal `F_p`-linear relations = Frobenius closure

### 2.1 The classification theorem

> **Theorem (span dimension = Frobenius closure).** Let `B=F_q`, `q=p^f`,
> `g(t)=(t,t^2,\dots,t^w)`, and take the full slice `D=F_q` (so `t_0=0` and
> `V_g = Span_{F_p}{g(t):t in F_q}`). Then
> ```
>    dim_Fp V_g  =  | Z_p(q-1, {1,...,w}) |,                                (*)
> ```
> the size of the Frobenius closure of `{1,...,w}` in `Z/(q-1)Z` under
> `x -> p x`. Equivalently, the universal `F_p`-linear relations among
> `p_1,...,p_w` are **exactly** the Frobenius-closure relations, of two kinds:
> - **(chain)** `p_{p j} = Frob(p_j)` whenever `p j <= w` (the image link);
> - **(subfield)** `p_j in F_{p^d}`, `d = |cyclotomic coset of j| < f` (descent).
>
> Both are constructible **Frobenius-invariance** = the extension/field-descent
> cell **C5** (L2422). There is **no third kind**: the classification is
> **exhaustive**.

*Proof.* A universal relation is `(c_1,...,c_w) in B^w` with
`\phi_c(t)=sum_j Tr_{B/F_p}(c_j t^j)` constant on `D=F_q` (trace duality on the
non-degenerate `F_p`-space `B^w`, as the lemma's own proof of EF3 uses). Since
`t=0` gives `0`, "constant" means `\phi_c \equiv 0`. The relation module is thus
the kernel of `\Psi:B^w -> Map(F_q,F_q)`, `(c_j) \mapsto sum_j Tr(c_j t^j)`, so
`dim_Fp V_g = wf - dim ker\Psi = dim (image \Psi)`. The image is the `F_p`-span
of `{ t\mapsto Tr(c t^j) : c in B, 1<=j<=w }`. For a single `j`, expanding the
trace, `Tr(c t^j) = sum_{i=0}^{f-1} c^{p^i} t^{j p^i}`, whose exponents are the
`p`-cyclotomic coset `C_j` of `j` mod `q-1`; as `c` ranges over `B` this spans
the coset function space of dimension exactly `|C_j|` (a standard
Mattson--Solomon / Delsarte fact --- the reduced monomials `{t^e:e in [1,q-1]}`
are `F_p`-independent functions, and distinct cosets are independent). Summing
over the distinct cosets meeting `{1,...,w}` gives
`dim(image\Psi) = sum_{cosets C, C∩[1,w]≠∅} |C| = |Z_p(q-1,{1,...,w})|`.
The chain relation `p_{pj}=Frob(p_j)` is the Lean-backed identity
`(sum_x x^j)^p = sum_x x^{pj}` (`psum_pow`); the subfield relation is
`Frob^d(p_j)=p_j` for a short coset. `∎`

**Status `PROVED`** (finite / scale-independent; the Delsarte coset-dimension
fact is standard). The verifier checks `(*)` **exactly** against a direct
`F_p`-rank on all 24 census leaves (`R1_classification_exact`), both closure
computations agreeing (`closure_two_ways`).

### 2.2 The vacuity corollary (the operative content)

> **Corollary (collapse `<=>` `w >= p`).** `dim_Fp V_g < wf` (span collapse)
> holds **iff `w >= p`**. Hence on every leaf inside the power-sum admissibility
> window `w < char = p` (L940), `dim_Fp V_g = wf`, `A_eff = A`, and **Gap-2 holds
> with no collapse**.

*Proof.* If `w < p`: (a) no chain, since `pj <= w < p <= pj` forces `j<1`; (b) no
subfield descent, since a short coset needs `j(p^i-1) \equiv 0 (q-1)` with
`i<f`, i.e. `j >= (q-1)/(p^i-1) >= (p^f-1)/(p^{f-1}-1) > p > w`; (c) no
wraparound collision, since `j p^i \equiv j' (q-1)` with `j'<j` needs
`j p^{f-1} >= q-1`, i.e. `j >= (q-1)/p^{f-1} > p-1`, so `j >= p > w`. Thus the `w`
cosets of `1,...,w` are full (size `f`) and disjoint, `|Z_p| = wf`, no collapse.
Conversely a collapse needs at least one of (a)-(c), each of which forces some
coordinate index `>= p`, i.e. `w >= p`. `∎`

**Status `PROVED`.** Verifier `R2_no_collapse_when_w<p` (all `w<p` leaves:
`dim=wf`) and `R2_collapse_forces_w>=p` (every collapse leaf has `w>=p`); the
`newton_boundary` check confirms the window `w<p` (Newton `j` invertible) equals
the no-collapse window byte-for-byte.

---

## Rung 3 --- PROVE mass absorption + budget

### 3.1 Existence + first-match order (`PROVED`)

By the Theorem every collapse relation is a **Frobenius-closure** relation =
constructible Frobenius-invariance = **C5** (field descent, L2422, "Frobenius
invariance is constructible"). C5 is an algebraic major-arc cell, so it
**precedes** the primitive/Sidon leaf in first-match order (L5180). The collapse
locus therefore *is* an earlier structural profile in the atlas --- obligation
(i)+(ii) discharged. **Note it is caught even earlier than C7 itself:** the
span-collapse sub-case of the C7 "effective-image-collapse" event does not need
the C7 enumerative input at all --- it lands in C5.

### 3.2 Mass absorption (`PROVED` structurally)

The re-routed mass lands where the leaf's data actually lives. Two exact
mechanisms, both verified on every collapse leaf (`R3_full_absorption`: the
identified C5 relations account for the **full** codimension `wf - dim`):

- **chain (`p_{pj}=Frob(p_j)`).** The power-sum data lies on the Frobenius graph
  `{(x,Frob x)}`; this is a **coordinate artifact**, removed by the paper's own
  mandate (P2, L4355; L940) to **switch to the elementary prefix**. Verified
  (`R5`): on `F_8` the power-sum prefix `(p_1,p_2)` collapses (support-span dim
  `3`) while the **elementary** prefix `(e_1,e_2)` has **full** span (dim `6`);
  the mandated switch removes the collapse entirely. This is exactly #539's
  char-2 finding, now shown to be the generic chain mechanism.
- **subfield (`p_j in F_{p^d}`).** The coordinate descends to `F_{p^d}`; the mass
  is a genuine field-descent profile over the subfield --- C5's "natural subfield
  profile", paid by "a direct field-sensitive slope count" at the **descended**
  domain/field parameters. Verified nonvacuously on `F_9`, `w=4` (`p_4 in F_3`,
  the quadratic character) and `F_4`, `w>=3`.

### 3.3 Budget (`PARTIAL`)

C5's payment at the descended parameters is quantified by the **integrated**
cyclotomic-defect fiber bound (PR #451, Theorem 1): a Frobenius-closed leaf's
fibre satisfies `|Omega ∩ Phi^{-1}(y)| <= p^{d_p(N,I)}` with
`d_p = N - |Z_p(N,I)|` --- i.e. the collapse defect is *itself* the payment
exponent, and the Lean-backed closure step makes the mechanism rigorous. This
keeps the re-route inside the profile's own paid budget. **But** this is C5's
**standing, catalogued** obligation ("a direct field-sensitive slope count is
required", L2426) instantiated in the cyclic case, not a *new unconditional*
bound proved here for every admissible leaf; hence **budget is `PARTIAL`**, not
independently closed. Crucially, on **admissible** power-sum leaves (`w<p`) there
is *nothing to pay* (Corollary 2.2), so the budget question is live only in the
forbidden regime the paper already routes away by coordinate switch.

---

## Rung 4 --- CENSUS: six extension fields, all `w <= 4`

Exact enumeration, `D=F_q`, direct `F_p`-rank of `V_g` vs the closure `(*)`.

| field | `p` | `w` | `dim V_g` | `A_eff` | `A` | collapse | relation kind | catcher |
|-------|-----|-----|-----------|---------|-----|----------|---------------|---------|
| `F_4`  | 2 | 2 | 2 | 4    | 16    | YES | chain            | C5 / elem-switch |
| `F_4`  | 2 | 3 | 3 | 8    | 64    | YES | chain+subfield   | C5 (wraparound) |
| `F_4`  | 2 | 4 | 3 | 8    | 256   | YES | chain+subfield   | C5 (wraparound) |
| `F_8`  | 2 | 2 | 3 | 8    | 64    | YES | chain            | C5 / elem-switch |
| `F_8`  | 2 | 3 | 6 | 64   | 512   | YES | chain            | C5 / elem-switch |
| `F_8`  | 2 | 4 | 6 | 64   | 4096  | YES | chain            | C5 / elem-switch |
| `F_9`  | 3 | 3 | 4 | 81   | 729   | YES | chain            | C5 / elem-switch |
| `F_9`  | 3 | 4 | 5 | 243  | 6561  | YES | **chain+subfield** | C5 (`p_4 in F_3`) |
| `F_16` | 2 | 2 | 4 | 16   | 256   | YES | chain            | C5 / elem-switch |
| `F_16` | 2 | 3 | 8 | 256  | 4096  | YES | chain            | C5 / elem-switch |
| `F_16` | 2 | 4 | 8 | 256  | 65536 | YES | chain            | C5 / elem-switch |
| `F_27` | 3 | 3 | 6 | 729  | 19683 | YES | chain            | C5 / elem-switch |
| `F_27` | 3 | 4 | 9 | 19683| 531441| YES | chain            | C5 / elem-switch |
| `F_25` | 5 | 1..4 | `2w` | `A` | `A` | **NO** | --- (window `w<p`) | vacuous |
| all others `w < p` | | | `wf` | `A` | `A` | **NO** | --- | vacuous |

**Readout (`PROVED` where scale-independent; `evidence + scope` for the null):**

- **Classification exact on all 24 leaves:** `dim_Fp V_g = |Z_p(q-1,{1..w})|`
  with zero exceptions (`R1`), in both the clean frontier regime `w<q-1` and the
  wraparound regime `w>=q-1` (`F_4`, `w=3,4`).
- **Every collapse forces `w >= p`** and every leaf with `w<p` (all of `F_25`,
  the shallow rows of every field) has `A_eff=A` (`R2`). The admissibility window
  and the no-collapse window coincide.
- **Every collapse's relations verified exactly** and account for the full
  codimension (`R3`): chain links `p_{pj}=Frob(p_j)` hold pointwise; subfield
  descents `p_j in F_{p^d}` hold pointwise. The **mixed** leaf `F_9,w=4` shows
  both kinds simultaneously (codim `3 = 2` (chain) `+ 1` (subfield)).
- **Uncaught collapses: NONE** (`R4_zero_uncaught_collapses`). No leaf carries a
  collapse relation outside the Frobenius closure. **No `COUNTEREXAMPLE`.**
- **Coordinate-switch catcher confirmed** (`R5`): elementary prefix full span,
  power-sum prefix collapsed, on `F_8`.

Toy nulls are `evidence + scope`; the classification `(*)` and the vacuity
corollary are the `PROVED`, scale-independent facts.

---

## Rung 5 --- WALL: precise residual + dead cheap routes

> **Gap-2 routing status.** The span-collapse re-route is **discharged** to the
> extent it is contentful: (existence) span collapse `\iff` a Frobenius-closure
> relation `\iff` cell C5; (order) C5 precedes the primitive leaf; (vacuity) on
> every admissible power-sum leaf (`w<p`) there is no collapse to route. The
> **only** residual is C5's own **payment constant** in the general
> (non-cyclic) field-descent case at the descended parameters --- a *catalogued*
> C5 obligation (L2426), for which PR #451 supplies the cyclic instance
> `p^{d_p}`. This residual is **not** a Gap-2-specific gap and **not** a new
> obstruction cell: the classification proves there is no collapse relation
> without a C5 home.

**Dead cheap routes (checked):**

1. **"The re-route target must be assumed (C7 enumerative input)."** DEAD for the
   *span-collapse* sub-case: `(*)` proves the target is always the constructible
   C5 field-descent cell; no assumption needed. (C7's saturation/occupancy
   content --- many raw witnesses to one slope --- is separate and untouched.)
2. **"There could be a non-Frobenius span collapse (a new cell)."** DEAD:
   `dim_Fp V_g = |Z_p|` is an *equality* (trace duality), so every collapse is
   Frobenius closure. Census: zero uncaught over six fields.
3. **"Route to the quotient cell C1."** DEAD as the *general* catcher: C1 is
   multiplicative-subgroup periodicity `pi:D->D'`, a different mechanism; the
   span collapse is additive-Frobenius = C5. (C1 can co-occur on structured
   domains but is not what catches the collapse.)
4. **"Newton dictionary removes the collapse."** DEAD in small char: the
   dictionary needs `char > w` (L6490, `j` invertible) --- exactly `w<p`, where
   there is no collapse anyway; at `w>=p` Newton breaks and the collapse is real,
   patched only by the elementary-coordinate switch, not by the dictionary.
5. **"BSG / additive-combinatorial smallness."** Not cheap and collides with the
   boundary: quantifying image smallness via fibre energy is the `(MI)`/`(MA)`
   inverse theory (scottdhughes), consumed, not attacked.

---

## Proposed paper changes (ledger entries, `asymptotic_rs_mca.md` convention)

Audit ledger entries only; **no `.tex`/`.pdf` edited.**

- **L-G2-1 (`AUDIT`, gap discharged).** In the C7 cell (L2440--2454) add: *the
  span-collapse component of effective-image collapse (`dim_Fp V_g < R[B:F_p]`)
  is not an enumerative input --- by `dim_Fp V_g = |Z_p(q-1,\{1,\dots,R\})|`
  (Frobenius closure) every such collapse is a Frobenius-invariance = C5
  field-descent locus, an earlier first-match profile; the C7 "projection degree
  is an enumerative input" caveat then applies only to the saturation/occupancy
  component.* Cross-reference C5 (L2422) and PR #451.

- **L-G2-2 (`AUDIT`, hypothesis made vacuous).** After the primitive-column item
  (L940) record the corollary: *since span collapse holds iff `R_N >= char`, the
  admissibility window `R_N < char` already guarantees `A_eff = A` on every
  power-sum leaf; the Gap-2 branch of the (L4) disjunction (L1115) is therefore
  vacuous on admissible power-sum leaves, and the collapse only arises for the
  small-characteristic leaves that the same item routes to elementary
  coordinates.* Ties L940, L1115, L4355 into one discharge.

- **L-G2-3 (`AUDIT`, clarity).** In `rem:binary-ambient-image` (L4349) note that
  `p_{2j}=p_j^2` is the `p=2` case of the general chain relation
  `p_{pj}=Frob(p_j)` (valid for every `pj<=w` in char `p`), so the
  elementary-prefix mandate resolves the collapse in *all* small characteristics,
  not only char 2.

- **L-G2-4 (`OPEN OBLIGATION`, narrowed).** The residual Gap-2 obligation is
  reduced to **C5's catalogued field-descent payment** (L2426, "a direct
  field-sensitive slope count") at the descended parameters --- PR #451 supplies
  the cyclic case `p^{d_p}`; the general-field-descent slope count remains C5's
  standing obligation, no longer a Gap-2/C7-specific gap.

---

## Per-claim label summary

| claim | label |
|-------|-------|
| Re-route assertion + consumers (P0--P2), candidate catchers C1/C5, first-match order extracted | `AUDIT` (exact) |
| `dim_Fp V_g = |Z_p(q-1,\{1..w\})|` (universal relations = Frobenius closure); exhaustive | `PROVED` (trace duality + Delsarte; census-exact) |
| chain `p_{pj}=Frob(p_j)` and subfield `p_j in F_{p^d}` are the only two kinds | `PROVED` |
| collapse `<=>` `w >= p`; hence vacuous on admissible power-sum leaves (`w<p`) | `PROVED` |
| collapse locus = C5 field-descent, an earlier first-match profile (existence + order) | `PROVED` |
| mass absorption: chain = coordinate artifact (elem-switch), subfield = descent profile; full codim | `PROVED` (structural + census-exact) |
| char-2 named collapse resolved by elementary prefix; general-char chain likewise | `PROVED` (exact, `R5`) instantiating `rem:binary-ambient-image` |
| budget: re-route inside C5's paid budget via PR #451 `p^{d_p}` fibre bound | `PARTIAL` (inherits C5's catalogued payment) |
| census: no uncaught collapse over `F_4,F_8,F_9,F_16,F_25,F_27`, `w<=4` | `evidence + scope` (toy) + decisive null |
| no non-Frobenius span collapse exists (no new obstruction cell) | `PROVED` (equality `(*)`) --- NO `COUNTEREXAMPLE` |

**Boundaries respected:** `(MI)`/`(MA)`/entropy-inverse (scottdhughes
#498/#501/#505) consumed, never attacked; Danny #529, latifkasuli #518
untouched; PR #451 cyclotomic defect + `c9_frobenius_closure_lean_backing`
Lean primitive + `cap25_v13` span-cell + #539 Gap tower credited and re-verified.
