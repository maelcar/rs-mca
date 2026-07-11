# The non-cyclic C5 field-descent slope count is the cyclotomic defect

**Lane.** The **one named wall** of the integrated Gap-2/Frobenius-collapse
routing packet PR #545 (`gap2_collapse_routing.md`): the **field-sensitive
slope count** of the extension/field-descent cell **C5**, in the general
**non-cyclic** case. #545 proved the Gap-2 span-collapse classification exact
(`dim_Fp V_g = |Z_p(q-1,{1..w})|`, collapse iff `w>=p`, vacuous on admissible
leaves) and reduced its residual to exactly this count; PR #451 (Danny) supplies
only the **cyclic** instance. This note proves the **non-cyclic** count and pins
the true remaining obligation.

**Verifier.** `experimental/scripts/verify_noncyclic_c5_count.py` (stdlib-only,
zero-arg, `RESULT: PASS (94 checks)`, ~10 s under `ulimit -v 2097152`; recomputes
every number below with exact `F_{p^m}` arithmetic and direct enumeration).

**Highest rung reached: 4 (fiber-count half PROVED + census-exact; residual wall
re-pinned to the defect-magnitude bound).**

**One-line headline.** *The C5 "direct field-sensitive slope count" is the
**cyclotomic defect** `p^{d_p(G,I)}`, `d_p(G,I)=|G|-|Z_p(G,I)|`, for **every**
finite abelian slope group `G` with `p \nmid |G|` --- cyclic **or non-cyclic** ---
proved by a semisimple group-algebra count that replaces Danny #451's
principal-ideal (cyclic-only) bookkeeping; the residual wall is no longer the
count but its **magnitude** (the non-cyclic Theorem-2 analog), which **fails to
be subexponential** on the Frobenius-trivial sub-class (a measured new floor).*

---

## Wall statement (verbatim, tex-anchored)

`experimental/asymptotic_rs_mca_frontiers.tex`, **Extension and field-descent
cells** paragraph, **L2422--2427**:

> "A witness lies in an extension or field-descent cell if its data is defined
> over a proper subfield (field descent) or factors only after enlarging the
> coefficient field (extension). Frobenius invariance is constructible. Its
> natural subfield profile can be larger than the identity profile, so **a direct
> field-sensitive slope count is required.**" (operative clause **L2426--2427**)

As narrowed by PR #545, `gap2_collapse_routing.md`, **Rung 5 (WALL)** and
**ledger entry L-G2-4 (OPEN OBLIGATION, narrowed)**, verbatim:

> "The **only** residual is C5's own **payment constant** in the general
> **(non-cyclic)** field-descent case at the descended parameters --- a
> *catalogued* C5 obligation (L2426), for which PR #451 supplies the cyclic
> instance `p^{d_p}`." (Rung 5)
>
> "The residual Gap-2 obligation is reduced to **C5's catalogued field-descent
> payment** (L2426, 'a direct field-sensitive slope count') at the descended
> parameters --- PR #451 supplies the cyclic case `p^{d_p}`; the
> **general-field-descent slope count remains C5's standing obligation**, no
> longer a Gap-2/C7-specific gap." (L-G2-4)

**Credit / lineage.** The **cyclic** slope count is **Danny's** result, PR #451
(`asymptotic_c9_frobenius_cyclotomic_defect.md`, Theorem 1): for a cyclic
frequency group `Z/NZ` (the character group of a cyclic multiplicative subgroup
`<zeta>` of `K^x`, `p \nmid N`) and a syndrome interval `I`, the fiber bound
`|Omega \cap Phi^{-1}(y)| <= p^{d_p(N,I)}`, `d_p(N,I)=N-|Z_p(N,I)|`,
`Z_p(N,I)=\bigcup_{\ell>=0} p^\ell I`. The Frobenius-closure primitive
`(\sum_i a_i \omega_i)^p = \sum_i a_i \omega_i^p` (for `a_i \in F_p`) is
Lean-backed zero-`sorry` (`c9_frobenius_closure_lean_backing.md`,
`FrobeniusClosure.sum_smul_pow`). This note **consumes #451's cyclic theorem and
its Lean primitive as inputs** and supplies the **non-cyclic** case; it builds on
the #545 span-collapse classification and reuses its `GF`/rank idiom (credited in
the verifier header). Boundaries: `(MI)`/`(MA)`/entropy-inverse (scottdhughes
#498/#501/#505) consumed as black box, never attacked; Danny #529, latifkasuli
#518 untouched.

---

## Rung 1 --- EXACT STATEMENT: the atomic object and where cyclicity breaks

### 1.1 The object (pinned from the note + tex)

C5's slope count is the **per-slope fibre size** of the descended field-descent
profile: how many raw witnesses `x` map to one slope value `y` under the
weighted power-sum / moment map `Phi(x)=\sum_g x_g v_g`. In #451 the slope group
is a **cyclic** `Z/NZ`. The **non-cyclic** case is the slope group of a
**product / multivariate** field-descent profile:

> a **finite abelian group** `G = Z/n_1 \times \dots \times Z/n_r` (`r>=2`, so
> **non-cyclic**) with `p \nmid |G|`; a **slope profile** `I \subseteq \hat G`
> (dual group, identified with `G`); the **Frobenius closure**
> `Z_p(G,I) = \bigcup_{\ell>=0} p^\ell \cdot I \subseteq \hat G` under the
> multiplication-by-`p` Frobenius `\chi \mapsto \chi^p`; and the **defect**
> `d_p(G,I) = |G| - |Z_p(G,I)|`.

The count that **would suffice to close the routing** is the fibre bound
`|Omega \cap Phi^{-1}(y)| <= p^{d_p(G,I)}` (Theorem A below) --- i.e. the
field-sensitive slope count is `p^{d_p(G,I)}`. This is the exact non-cyclic
analog of #451 Theorem 1. **Why non-cyclic is the live case:** a finite subgroup
of a field's multiplicative group `K^x` is always **cyclic**, so genuinely
non-cyclic slope groups arise only from **product / multivariate** domains ---
precisely the deployed rows Danny #451 sec. 7 lists as **uncovered** ("circle or
twin-coset row", the `N | p-1` prime-field-dyadic row where Frobenius acts
trivially, and the KoalaBear / Mersenne-31 / QM31 rows). `[label: AUDIT (exact
extraction)]`

### 1.2 What the cyclic case gives and exactly where non-cyclicity breaks it

Danny's #451 proof forms the fibre-difference polynomial
`f_x(X)=\sum_i e_i X^i \in F_p[X]` (`e_i = u_i(x_i-x_i^{(0)}) \in F_p`), uses
`f_x(\zeta^{pk})=f_x(\zeta^k)^p` to get a Frobenius-closed root set, concludes
`G_Z(X)=\prod_{k \in Z_p}(X-\zeta^k)` **divides** `f_x` in `F_p[X]`, and counts
`deg h < d_p` to get `p^{d_p}` polynomials. **This is principal-ideal /
polynomial-degree bookkeeping in `F_p[X]/(X^N-1)`, a principal ideal ring
precisely because `Z/NZ` is cyclic.**

For non-cyclic `G` the group algebra is
`F_p[G] = F_p[X_1,\dots,X_r]/(X_1^{n_1}-1,\dots,X_r^{n_r}-1)`, a **multivariate**
ring that is **not a principal ideal ring** for `r>=2` (e.g. the augmentation-type
ideal needs `>=2` generators). There is **no single generator `G_Z`** and **no
degree count**: Danny's Theorem-1 proof does not port. This is the exact
breakpoint. `[label: PROVED (structural)]`

---

## Rung 2 --- STRUCTURE REDUCTION: semisimple group-algebra count (Theorem A)

Replace the (cyclic-only) PID bookkeeping with a **Fourier / Maschke** dimension
count that is insensitive to the group being cyclic.

> **Theorem A (non-cyclic cyclotomic-defect fibre bound).** Let `p` be prime,
> `K` a finite field of characteristic `p`, `G` a finite abelian group with
> `p \nmid |G|`. Fix weights `u_g \in F_p^\times`, `\rho_g \in K^\times`, a slope
> profile `I \subseteq \hat G`, and set `v_g = \rho_g\,(\chi(g))_{\chi \in I}`,
> `Phi(x)=\sum_g x_g v_g` for `x` in any `Omega \subseteq \{0,1\}^G`. Then for
> every `y`,
> ```
>     |Omega \cap Phi^{-1}(y)|  <=  p^{d_p(G,I)},   d_p(G,I) = |G|-|Z_p(G,I)|.
> ```

**Proof.**
1. *(Injectivity --- as in #451.)* For two fibre points `x,x^{(0)}` set
   `e_g = u_g(x_g-x_g^{(0)}) \in F_p` and `a = \sum_g e_g[g] \in F_p[G]`. Since
   `u_g \ne 0` and `x^{(0)}` is fixed, `x \mapsto a` is injective on the fibre, so
   `|fibre| <= \#\{admissible\ a\}`.
2. *(Syndrome vanishing.)* Equality of the slope coordinate `\chi \in I` reads
   `\hat a(\chi):=\sum_g e_g \chi(g)=0` for every `\chi \in I` (the Fourier/character
   transform of `a`).
3. *(Frobenius closure --- the Lean primitive.)* As `e_g \in F_p`,
   `\hat a(\chi)^p=(\sum_g e_g\chi(g))^p=\sum_g e_g\chi(g)^p=\sum_g e_g(\chi^p)(g)
   =\hat a(\chi^p)`, the boxed identity `(\sum a_i\omega_i)^p=\sum a_i\omega_i^p`
   (`c9_frobenius_closure_lean_backing.md`, `sum_smul_pow`; **field-structure
   agnostic** --- this is why step 2->3 ports verbatim from the cyclic case).
   Hence `\hat a(\chi)=0 \Rightarrow \hat a(\chi^p)=0`, so `\hat a` vanishes on all
   of `Z_p(G,I)`.
4. *(Semisimple dimension count --- the NEW step, replacing PID divisibility.)*
   Because `p \nmid |G|`, by Maschke `F_p[G]` is semisimple and the character
   table is invertible over `\bar K` (needs `|G|` invertible, i.e. `p \nmid |G|`),
   so the Fourier transform `a \mapsto (\hat a(\chi))_\chi` is an isomorphism
   `\bar K[G] \cong \bar K^{\hat G}`. For a **Frobenius-closed** `Z \subseteq \hat G`
   the subspace `V_Z=\{a \in F_p[G]:\hat a|_Z=0\}` is `Gal(\bar K/F_p)`-stable
   (the Galois action on `\hat G` is `\chi \mapsto \chi^p`, which preserves `Z`),
   hence defined over `F_p` with `\dim_{F_p} V_Z = \dim_{\bar K}\{\,\hat a|_Z=0\,\}
   = |\hat G|-|Z| = |G|-|Z_p(G,I)| = d_p(G,I)`. Each killed Frobenius orbit of
   size `m` removes exactly `m` (one `F_{p^m}` simple component). Therefore
   `\#\{admissible\ a\} = |V_{Z_p(G,I)}| = p^{d_p(G,I)}`. `\square`

`[label: PROVED --- Maschke + Fourier + the Lean-backed closure primitive;
finite / scale-independent; census-exact below.]`

### 2.1 The defect functional and its (non-)multiplicativity

> **Orbit formula.** The Frobenius (`\chi \mapsto \chi^p`) orbit of
> `\chi=(c_1,\dots,c_r) \in \prod Z/n_i` has size
> `\ell(\chi) = \mathrm{lcm}_i\, \mathrm{ord}_{\,n_i/\gcd(c_i,n_i)}(p)`, and
> `|Z_p(G,I)| = \sum_{\text{orbits }O\ :\ O\cap I\ne\emptyset} |O|`.

`[label: PROVED (closed form) + MEASURED --- verifier `ORBIT.*` (13 groups, all
`|G|` elements) and `DEFECT.*` (39 profiles, orbit-sum == iterated closure).]`

> **Non-multiplicativity (structure-reduction obstruction).** The slope-count
> functional does **not** factor over the product: for a box `I=I_1\times\dots
> \times I_r`, in general `|Z_p(G,I)| \ne \prod_i |Z_p(Z/n_i,I_i)|`, because
> Frobenius acts **diagonally** (one shared `p`), coupling the factors.

Measured witness (`NONMULT.*`): `G=(Z/3)^2`, `p=2`, `I=\{1\}\times\{0,1\}`:
`|Z_2(G,I)| = 4`, while `|Z_2(Z/3,\{1\})|\cdot|Z_2(Z/3,\{0,1\})| = 2\cdot 3 = 6`.
So a naive "decompose-and-multiply" derivation of the count is **wrong**; the
semisimple argument (Theorem A) is required precisely because the defect is a
**global** orbit count on `\hat G`, not a product. `[label: MEASURED --- decisive
against factoring.]`

---

## Rung 3 --- CENSUS: exact fibre counts vs `p^{d_p(G,I)}`

Direct field realization `K=F_{p^m}` (`m=\mathrm{ord}_{\exp G}(p)`), characters
`\chi_c(g)=\zeta^{\langle c,g\rangle}`, Boolean `Omega=\{0,1\}^G` fully
enumerated for `|G|<=18`; buckets over `Phi(x)`; and independent `F_p`-rank.

| group `G` | `p` | profile `I` | `d_p` | max fibre | `p^{d_p}` | rank | `|Z_p|` | `K` |
|-----------|-----|-------------|-------|-----------|-----------|------|---------|-----|
| `(Z/3)^2` | 2 | box `{1,2}^2` | 5 | **32** | **32** | 4 | 4 | `F_4` |
| `(Z/3)^2` | 2 | gen `(1,0)` | 7 | **128** | **128** | 2 | 2 | `F_4` |
| `(Z/3)^2` | 2 | L `(1,0),(0,1)` | 5 | **32** | **32** | 4 | 4 | `F_4` |
| `(Z/3)^2` | 5 | box `{1,2}^2` | 5 | 14 | 3125 | 4 | 4 | `F_25` |
| `(Z/2)^2` | 3 | box | 3 | 6 | 27 | 1 | 1 | `F_3` |
| `Z/2 x Z/4` | 3 | box | 5 | 18 | 243 | 3 | 3 | `F_9` |
| `Z/2 x Z/4` | 5 | box | 6 | 18 | 15625 | 2 | 2 | `F_5` |
| `(Z/2)^3` | 3 | box | 7 | 86 | 2187 | 1 | 1 | `F_3` |

**Readout.**
- **Bound (A) holds on every census leaf** (`FIBER<=.*`, 8 leaves): measured max
  fibre `<= p^{d_p(G,I)}`, zero exceptions. `[label: MEASURED]`
- **Bound (A) is TIGHT** (equality) exactly where predicted: `p=2`, `|G|` odd,
  `Omega=\{0,1\}^G` full --- every nonempty fibre equals `2^{d_p}` (`FIBER=.*`,
  bold rows: `32=2^5`, `128=2^7`). For `p>2` the Boolean `Omega` is a strict
  subset of `F_p[G]`, so the fibre is strictly below `p^{d_p}` (loose, still `<=`).
  `[label: MEASURED --- matches Theorem A: fibre `= p^{d_p}` iff `Omega` spans.]`
- **Semisimple count confirmed**: `F_p`-rank of the syndrome map `== |Z_p(G,I)|`
  on all 10 `RANK.*` leaves --- the Theorem-A dimension count is exactly the
  measured rank. `[label: MEASURED]`
- **Cyclic specialization reproduces #451** (`CYCLIC.*`, 5 leaves): the `r=1` case
  recovers `|Z_p(N,I)|`, incl. the #545 anchor `|Z_2(7,\{1,2\})|=3`. `[label:
  MEASURED --- lineage: Theorem A specializes to #451 Theorem 1.]`

---

## Rung 4 --- OUTCOME: what closes, and the re-pinned wall

### 4.1 What closes in the Gap-2 routing (if Theorem A stands)

The C5 "direct field-sensitive slope count" (L2426) is, on **every** admissible
field-descent profile with `p \nmid |G|` --- **cyclic or non-cyclic** --- the
cyclotomic-defect payment `p^{d_p(G,I)}`, by the **same** mechanism (Frobenius
closure of the syndrome profile), with **no new cell** and no extra hypothesis
beyond semisimplicity. Concretely this **closes #545's stated residual at the
count level**: L-G2-4's "the general-field-descent slope count remains C5's
standing obligation" is discharged --- the count is `p^{d_p(G,I)}` uniformly, and
the Gap-2 re-route inherits **one** C5 payment law across cyclic and non-cyclic
descent profiles. `[label: PROVED (count) --- Theorem A.]`

### 4.2 The re-pinned wall (honest residual + falsifier evidence)

The count `p^{d_p(G,I)}` is a **valid** bound always, but is
**routing-admissible (subexponential)** only when `d_p(G,I)=o(|G|)`. Danny's
cyclic **Theorem 2** achieves this for **large** intervals (`R>=\kappa N`) in the
dyadic regime. **The non-cyclic analog is NOT automatic and provably fails on a
named sub-class:**

> **Trivial-Frobenius floor (measured new floor).** If `p \equiv 1 \pmod{\exp G}`
> (Frobenius acts trivially --- Danny #451 sec. 7's excluded `N|p-1` row, now in
> the product), then `Z_p(G,I)=I` exactly and `d_p(G,I)=|G|-|I|`, which is
> `\Theta(|G|)` for any bounded-density profile. Then `p^{d_p}` is **exponential**
> and the payment is **vacuous** --- the routing does **not** close uniformly on
> non-cyclic C5 leaves, only on the **Frobenius-active** sub-class.

Measured (`DEGEN.*`, 11 checks): the defect is **Frobenius-sensitive**, e.g.
`G=(Z/7)^2`, `|I|=9`: `d_{active}(p{=}2)=25` vs `d_{trivial}(p{=}29)=40` (both
`\Theta(49)`); the trivial-Frobenius law `d_p=|G|-|I|` holds exactly on all five
`DEGEN` groups. This **bounds where a counterexample to uniform subexponential
payment lives**: exactly the `p \equiv 1 \pmod{\exp G}` (and small-Frobenius-order)
profiles. `[label: MEASURED --- COUNTEREXAMPLE to uniform payment / NEW FLOOR.]`

> **Next atomic lemma (the residual wall).** *A non-cyclic Theorem-2: bound
> `d_p(G,I)=o(|G|)` (ideally `O_\kappa(1)`) for the **Frobenius-active** deployed
> profiles --- the circle/twin-coset row and the QM31 / Mersenne-31 tower ---
> where `p` has large multiplicative order in each factor `n_i` and `I` is a
> Frobenius-generating profile of density `>=\kappa`; OR prove the `(A5)`
> admissibility window (L935--941, `R_N<\mathrm{char}`) admits **only** such
> Frobenius-active descent leaves, excluding the trivial-Frobenius floor.* This
> is exactly parallel to Danny's cyclic Theorem 2, now over a product group; the
> orbit geometry of diagonal multiplication-by-`p` on `\prod Z/n_i` is the open
> analytic content. `[label: OPEN.]`

### 4.3 Scope guard (hypothesis is load-bearing)

`p \nmid |G|` (semisimplicity) is **essential**, not decorative: dropping it
**breaks** Theorem A. Measured (`MODULAR`): `G=(Z/2)^2`, `p=2` (so `p \mid |G|`),
characters degenerate in characteristic 2, and a measured fibre `=8` **exceeds**
`p^{d_p}=4`. This matches Danny's own `p \nmid N` hypothesis and confirms the
count law is confined to the char-coprime (separable / FFT-friendly) descent
profiles that RS-MCA actually uses. `[label: MEASURED --- scope falsifier.]`

---

## Per-claim label summary

| claim | label |
|-------|-------|
| Wall extracted as the C5 non-cyclic fibre count; object = `(G,I,Z_p,d_p)` | `AUDIT` (exact) |
| Danny #451 cyclic proof is PID/degree bookkeeping; breaks for non-cyclic `F_p[G]` (`r>=2`) | `PROVED` (structural) |
| **Theorem A**: `|Omega\cap Phi^{-1}(y)| <= p^{d_p(G,I)}` for non-cyclic `G`, `p\nmid|G|` | `PROVED` (Maschke+Fourier+Lean primitive; census-exact) |
| orbit size `= \mathrm{lcm}_i \mathrm{ord}_{n_i/\gcd}(p)`; `|Z_p|=\sum_{O\cap I\ne\emptyset}|O|` | `PROVED` (closed form) + `MEASURED` |
| slope-count functional is **not** multiplicative over the product decomposition | `MEASURED` (decisive) |
| census: fibre `<= p^{d_p}` on all leaves; tight (`=`) for `p=2`, full `Omega`; rank `= |Z_p|` | `MEASURED` |
| cyclic `r=1` specialization reproduces #451 `|Z_p(N,I)|` | `MEASURED` (lineage) |
| C5 slope count `= p^{d_p(G,I)}` uniformly (cyclic+non-cyclic) closes #545 residual at count level | `PROVED` (count) |
| trivial-Frobenius floor `d_p=|G|-|I|` maximal => payment vacuous (non-uniform) | `MEASURED` (new floor) |
| non-cyclic Theorem-2 (defect magnitude for active profiles) = the residual wall | `OPEN` |
| `p\nmid|G|` load-bearing: `p\mid|G|` breaks Theorem A (measured fibre > `p^{d_p}`) | `MEASURED` (scope) |

**Boundaries respected:** `(MI)`/`(MA)`/entropy-inverse (scottdhughes) consumed,
never attacked; Danny #451 (cyclic foundation) + `sum_smul_pow` Lean primitive +
#545 span-collapse classification credited and re-used; Danny #529, latifkasuli
#518 untouched. No `.tex`/`.pdf` edited.
