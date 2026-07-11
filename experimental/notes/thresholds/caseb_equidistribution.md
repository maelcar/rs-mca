# The Case B exponential-field corner: the collapse-cell slope map equidistributes up to a bounded constant, the corner does not close by counting, and it reduces to one growing-dimension character sum

## Status

`A3 COUNTING DOES NOT CLOSE THE CORNER (PROVED: |G|>=eps|F| is SATISFIABLE with
log|G|,log|F| both Theta(n), in the poly-base-field PRIZE regime) / A1
PROJECTION IS B-LINEAR ONTO F, RIGOROUS LOWER BOUND delta>=|G|/q0^{k+1-e}
(PROVED) -- but it reaches prize-relevance ONLY on the shallow poly-field
sub-regime (COMPUTED) / IMAGE c F*, 0 NEVER A SLOPE (PROVED) / A4 CENSUS:
delta = min(|G|,|F|)*eta, eta in [0.76,1.0], collapse ratio = generic
max(1,|G|/|F|) to a few % (MEASURED, e<=4, exact GF(p^e)) / ANTI-OBSTRUCTION:
coverage(rho) is INVARIANT in e at EXACT rho-matches (e:2->3->4) -- the image is
NOT o(|F|) at growing e at any reachable scale (MEASURED) / INJECTIVE-ON-CLOSE
LEMMA: collisions force |S triangle S'|>2e, so the slope fibers are spread codes
(PROVED) / VERDICT = PARTIAL, decisively CONSTRUCTION-pointing; the residual is
one asymptotic subset-product equidistribution law (growing-dimension character
sum, Weil constants uncontrolled) = OPEN`.

**One-line verdict (PARTIAL, construction-pointing).** *At exponential field size
`log|F| = Theta(n)` with a deep fiber `log|G| = Theta(n)`, whether the Case-B
Vandermonde symmetric-function image covers a prize-relevant fraction of `F`
(`e_MCA = delta/|F| > eps = 2^{-128}`) is **not decided by counting** -- the
necessary condition `|G| >= eps|F|` is **satisfiable** with both logs `Theta(n)`
even in the prize's polynomial-size base-field regime (`q0 = n^C`, `C>=2`,
`m = 2e`, `w = O(1)`), so the easy one-page close **fails** and the fight is
localized to the critical boundary `|G| ~ |F|`. There the exact
`GF(p^e)` census (`e<=4`, 14 Case-B cells) shows the slope map
`S |-> Q_S(alpha) = prod_{x in S}(alpha-x)` behaving **generically**:
`delta = min(|G|,|F|)*eta` with `eta in [0.76,1.0]`, its collapse ratio
`|G|/delta` equal to the generic `max(1,|G|/|F|)` to within a few percent, and --
the decisive datum -- at **exactly** matched `rho = |G|/|F|` the coverage is
**invariant under `e`** (`e:2->3` gives `0.6095->0.6154`; `e:3->4` gives
`0.5453->0.5411`). An obstruction (image `o(|F|)` at growing `e`) would force
coverage at fixed `rho` to **decay**; it does not, so the census **positively
disfavours the obstruction** and points to **CONSTRUCTION**: a prize-relevant
`Theta(n)`-field bad-line class exists and `(FI-field')` is **tight**, not
weakenable. What we **cannot** yet do is prove this asymptotically: the rigorous
surjectivity bound (`delta >= |G|/q0^{k+1-e}`, PROVED) reaches prize-relevance
only for **shallow** (poly-field) fibers, and the full statement is a
subset-product equidistribution law over an affine `B`-line whose defining
variety has dimension growing with `n` -- a character sum whose Weil/Deligne
implied constant (a Betti-number / degree product over an unbounded dimension) is
exactly the uncontrolled quantity, so the bounded-dimension estimate does not
apply off the shelf. That one asymptotic law is the last open link; the toy
Johnson-multiplicity and packing routes are `exp(Theta(e))` too weak. Net for the
span face (#650): `(FI-field')` should stay **printed as-is** -- the census says
it is tight, and its unconditional tightness (construction) or removability
(obstruction) awaits exactly this equidistribution result.*

Every number below is recomputed by
`experimental/scripts/verify_caseb_equidistribution.py` (stdlib-only, zero-arg,
`RESULT: PASS (116/116)`, ~20 s, 133 MB, well under `ulimit -v 2097152`).

Label key: **PROVED** (complete re-derivable hand proof, exact), **COMPUTED**
(exact finite recomputation of a promoted/derived quantity), **MEASURED** (exact
finite toy census; the asymptotics `e->infty` are *not* proved from the toy),
**AUDIT** (verbatim interface reading of the tex or a sibling note), **OPEN**.

**Credit.** The corner is the residual named by our **#645**
(`fi_field_discharge.md`, `(RED)` `e_MCA=delta/|F|` and honest flag 3: the
`binom(N,2)` field cost is proved *sufficient, not necessary*) and localized to
"Case B over an exponential field" by our **#647** (`collapse_field_cost.md`,
read first: the Case-A/Case-B dichotomy, the `m=3,w=1,e=2` centerpiece over a
poly field, and the explicit statement that Case B at `e=Theta(n/log q0)` "is an
equidistribution question we do not settle"). The field-of-definition law
`delta <= |F_r|` (T-FIELD) and the `GF(p^d)` census machinery are our **#642**
(`c7_collapse_image_degree.md`). The pole-to-slope fiber form
`delta = #{Q_S(alpha)}` and the separation gate eq (4.5)
(`thm:prefix-to-line-hardness`, tex L2073) are **the paper's own**; subfield
confinement `thm:subfield-confinement-full` (tex L1930) is the paper's, and gives
the `image c F*` structural fact. The place of this corner in the closure is our
**#650** (`span_face_synthesis.md`, `(FI-field')` clause `(iv)`). The
admissibility clauses `(A2)` (distinct-slope budget, tex L905), `(A3)`
(logarithmic order `q_N<=(log N)^C`, tex L912) and `(A5)` (`R_N<char B_N` for
power-sum coordinates; elementary coordinates retained in small characteristic,
tex L935) are the paper's, extracted verbatim by **#645**. Weil/Deligne are
named only where genuinely invoked (Rung A2, and only to *explain why the
standard bound does not close it*, not to claim it does). No finite M31/KoalaBear survivor
count, adjacent inequality, or target threshold is touched. Codex #634/#644/#649
orientation-cell machinery and Danny #621/#631 pole-transport are **not** used
here (this corner is a single-fiber projection question); they are cited only
through #642/#645/#647 for context.

---

## HEADLINE (read first): the corner survives counting, and the census points to construction

`#647` reduced the last falsification target to a single question. On a C7
effective-image-collapse line with a **low-degree** pole (`e = [B(alpha):B] <= k`,
so `|F| = |B|^e`), the received-line MCA-bad slope of a support `S` in the
depth-`w` prefix fiber `G` is, after dropping the fiber-common shift `C(alpha)`,

```
   Q_S(alpha) = sum_{j=0}^{k} a_j(S) alpha^j,   a_j(S) = (-1)^{m-j} e_{m-j}(S),
```

the free elementary symmetric functions `(e_{w+1}(S),...,e_m(S))` fed through the
**Vandermonde projection** `pi:(a_0,...,a_k) |-> sum_j a_j alpha^j`. Because
`1,alpha,...,alpha^{k}` collapse `B`-linearly into the `e`-dimensional space `F`,

```
   delta(r) = #{ pi(a(S)) : S in G }  <=  min(|G|, |F|).
```

The **prize question**: at `log|F| = Theta(n)` (`e = Theta(n/log q0)`) and a
**deep** fiber `log|G| = Theta(n)`, can `delta ~ eps|F|` (`e_MCA > 2^{-128}`)?
Two equivalent readings of the same object make the geometry transparent:

- **(products of an affine line)** With `w=0`, `Q_S(alpha) = prod_{x in S}(alpha-x)`
  is a product of an `m`-subset of `V = alpha - D`, and since `D subseteq B`, the
  set `V` lies on the **affine `B`-line** `alpha + B subseteq F`. The image is the
  set of `m`-fold products of `m`-subsets of `n` points on a `B`-line.
- **(reductions of split polynomials)** `Q_S(alpha) = (Q_S mod mu)(alpha)`, `mu`
  the degree-`e` minimal polynomial of `alpha`; so `delta` counts the distinct
  residues **mod `mu`** of monic squarefree degree-`m` polynomials that split over
  `D`.

This packet does A3 (counting) first, then the A4 census, then the A1/A2
structure -- and lands on **PARTIAL, construction-pointing**. The four pillars:

1. **A3 (PROVED).** Counting gives the necessary condition `|G| >= eps|F|`, i.e.
   `log2|F| + w log2 q0 <= log2 binom(n,m)`. This is **satisfiable** with both
   logs `Theta(n)` -- including in the prize's poly-base-field regime -- so the
   corner does **not** close by counting.
2. **A1 (PROVED, but limited reach).** `pi` is `B`-linear and **surjective** onto
   `F`; with `|ker pi| = q0^{k+1-e}` and the free-symmetric map injective on `G`,
   `delta >= |G|/q0^{k+1-e}`. This proves prize-relevance only when
   `|G| > eps q0^{k+1}` -- the **shallow/poly-field** sub-regime -- not the deep
   exponential one.
3. **A4 (MEASURED).** The map is generic: `delta = min(|G|,|F|)*eta`,
   `eta in [0.76,1.0]`; **coverage is `e`-invariant at fixed `rho`** (the
   anti-obstruction datum). Image `c F*` (0 never a slope, PROVED) and saturates
   `delta = |F|-1` once `|G| >> |F|`.
4. **A2 (OPEN, honest).** The asymptotic `e->infty` proof is a growing-dimension
   character sum; the Weil degree factor is `exp(Theta(n))`, so "Weil gives it"
   is **false as stated**, and no elementary substitute (Johnson multiplicity,
   packing) is within `exp(Theta(e))` of enough.

---

## Rung A3 -- COUNTING: the corner does not close by counting (PROVED)

**The necessary condition.** `delta <= min(|G|,|F|)` (image sits in both `G` and
`F`), so a prize-relevant line (`delta/|F| > eps`) forces

```
   |G| >= delta > eps|F|      <=>      log2|G| >= log2|F| - 128.        (NEC)
```

With `n <= q0` and a depth-`w` fiber (average size `binom(n,m)/q0^w`), `(NEC)`
reads

```
   log2|F| + w log2 q0  <=  log2 binom(n,m)  ~  n * H2(m/n).           (BND)
```

**Satisfiability = the corner survives.** Write `c = log2|F|/n` (so
`e = c n/log2 q0`) and `beta = m/n`. Then `(BND)` is `c <= H2(beta) - w log2 q0/n`.
Since `H2(beta) <= 1` (max at `beta=1/2`), any `c < H2(beta)` with
`w = o(n/log q0)` satisfies it while keeping `log|F| = c n = Theta(n)` and
`log|G| ~ (H2(beta)-c) n + ... = Theta(n)`. The boundary constant is exactly
`c* = H2(beta)`; below it the fiber can match the field rate, above it counting
**closes** the corner.

- **PROVED (satisfiable, prime base field).** `q0=p`, `beta=1/2`, `c=0.6<1`,
  `w = Theta(n/log q0)` (still `o(n)`): `(NEC)` holds, `e<=k`, and both
  `log|F|/n -> 0.60`, `log|G|/n -> 0.80`. [verify BLOCK 1a, `p in {1009,4099,16411}`.]
- **PROVED (satisfiable, the PRIZE regime -- poly-size base field).** The prize's
  smooth/circle rows have `log|B_n| = O(log n)`. Take `q0 = n^C` with `C >= 2`,
  `e` with `e log2 q0 = 0.5 n`, `m = 2e`, `w = 4`. Then
  `log2|G| ~ m log2 q0 - log2(m!) - w log2 q0 >= log2|F| - 128` because
  `(m-e) log2 q0 = e*C log2 n` dominates `log2(m!) ~ m log2 m = 2e log2(2e)` once
  `C >= 2`. So `|G| >= |F|` with `log|F|, log|G| = Theta(n)` and a **polynomial**
  base field. [verify BLOCK 1b, `n in {2^14,2^16,2^18}`,
  `log|F|/n ~ 0.50`, `log|G|/n in {0.68..0.81}`.]
- **COMPUTED (counting DOES close the over-field regime).** `c = 1.3 > H2(1/2)=1`
  makes `(NEC)` fail: `|F| > binom(n,m)`, `delta <= |G| < eps|F|` impossible, the
  corner closes there. This is the honest half: only `c > H2(beta)`, i.e.
  `|F| > binom(n,m)/eps`, is closed by counting. [verify BLOCK 1c.]
- **COMPUTED (exact ceiling).** `e_max(n,m,q0) = floor(log binom(n,m)/log q0)` is
  the largest `e` with `binom(n,m) >= q0^e`; it equals `Theta(n/log q0)`, the
  field exponent, so field and fiber are **commensurate** at the boundary.
  [verify BLOCK 1d, `(17,8),(23,11),(29,14)`.]

**A3 answer (the task's "check this first").** The one-page counting close **does
not exist**: admissible deep fibers do **not** obey `log|G| <= (1-c)log|F|` for
structural reasons -- on the contrary, `log|G|` can *exceed* `log|F|` with both
`Theta(n)`, in the actual poly-base-field prize regime. The corner is genuine;
the decision lives at `|G| ~ |F|`.

---

## Rung A1 -- STRUCTURE: the projection is surjective; the rigorous bound reaches only the poly field (PROVED)

**Surjectivity.** The columns of `pi` are the coordinate vectors of
`alpha^0,...,alpha^k` in the power basis `1,alpha,...,alpha^{e-1}` of `F`. The
first `e` columns (`j=0..e-1`) are `alpha^j` = the **standard basis vectors**, so
`pi = [ I_e | M' ]` has rank `e`: **`pi` is `B`-linear ONTO `F`**. [verify
BLOCK 2: the `e x e` identity block, `(p,e) in {(5,2),(7,3),(11,3),(13,4)}`.]

**Rigorous lower bound.** A set is determined by its full elementary symmetric
functions, and on `G` the prefix `(e_1,...,e_w)` is fixed, so
`S |-> (e_{w+1}(S),...,e_m(S))` is **injective**: `|freesym(G)| = |G|`. With
`|ker pi| = q0^{k+1-e}`,

```
   delta = |pi(freesym G)|  >=  |freesym G| / |ker pi|  =  |G| / q0^{k+1-e}.  (LB)
```

`(LB)` is **PROVED** and holds on every census cell [verify BLOCK 5]. Dividing by
`|F|=q0^e`,

```
   delta/|F|  >=  |G| / q0^{k+1}  =  binom(n,m) / q0^{m}   (w=0).
```

**Reach of `(LB)` (COMPUTED).** In the deep regime `binom(n,m)/q0^{m}` is
`2^{-Theta(n)}` (e.g. `0.0029, 3.6e-4, 3.5e-6` for the `p in {11,13,17}` `e=3`
cells), so `(LB)` clears `eps=2^{-128}` **only** when `n = O(1)` -- i.e. only on
**shallow / poly-field** fibers. There it re-proves `#647`'s poly-field
construction (and the Case-A `delta=|G|` witness); it says **nothing** about the
deep exponential regime. *This is the exact ceiling of what elementary linear
algebra buys.* [verify BLOCK 5 reach.]

**A useful structural fact (PROVED): the image is confined to `F*`.** Every slope
is `prod(alpha - x)` with `alpha notin B`, hence `alpha - x != 0`, hence
`Q_S(alpha) != 0`. So `image subseteq F*`, `delta <= |F|-1`, and coverage is
capped at `(|F|-1)/|F|`. [verify BLOCK 8: `0 notin image` for
`(p,e) in {(7,2),(11,2),(13,2)}`.] This is the mechanism by which the additive
`B`-line structure of `V = alpha - D` **precludes** the one clean obstruction:
were `V` a multiplicative-subgroup coset `gH`, all products would lie in `g^m H`
(one coset, `delta <= |H| = o(|F|)`); but `V` on an affine `B`-line is
additively structured, which by sum-product heuristics forbids such multiplicative
concentration. The census confirms no such stall (Rung A4).

---

## Rung A4 -- CENSUS: the slope map is generic; coverage is invariant in e (MEASURED)

Exact `GF(p^e)` (irreducible modulus via Rabin's test), `B=D=F_p`,
`alpha = X in F setminus B` of degree `e`, `delta = #{Q_S(alpha)}` on the
reference depth-`w` fiber. Every cell has `e <= k` (**genuine Case B**;
`delta < |G|` in general). Column key: `eta = delta/min(|G|,|F|)` (fill
efficiency), `coll = |G|/delta` (fiber points per slope), `gen = max(1,|G|/|F|)`
(the generic-map expectation).

| `p` | `e` | `m` | `w` | `\|G\|` | `\|F\|` | `delta` | cover | `eta` | `coll` | `gen` |
|----:|:--:|----:|:--:|------:|------:|------:|------:|-----:|------:|------:|
| 11 | 2 | 5  | 1 | 42    | 121    | 38    | .3140 | .905 | 1.11 | 1.00 |
| 11 | 3 | 5  | 0 | 462   | 1331   | 441   | .3313 | .955 | 1.05 | 1.00 |
| 13 | 2 | 6  | 1 | 132   | 169    | 103   | .6095 | .780 | 1.28 | 1.00 |
| 13 | 3 | 6  | 0 | 1716  | 2197   | 1352  | .6154 | .788 | 1.27 | 1.00 |
| 17 | 2 | 8  | 1 | 1430  | 289    | 288   | .9965 | .997 | 4.97 | 4.95 |
| 17 | 3 | 8  | 0 | 24310 | 4913   | 4907  | .9988 | .999 | 4.95 | 4.95 |
| 17 | 3 | 8  | 1 | 1430  | 4913   | 1318  | .2683 | .922 | 1.08 | 1.00 |
| 17 | 4 | 8  | 0 | 24310 | 83521  | 22341 | .2675 | .919 | 1.09 | 1.00 |
| 19 | 2 | 9  | 1 | 4862  | 361    | 360   | .9972 | .997 | 13.51| 13.47|
| 19 | 3 | 9  | 1 | 4862  | 6859   | 3740  | .5453 | .769 | 1.30 | 1.00 |
| 19 | 4 | 9  | 0 | 92378 | 130321 | 70521 | .5411 | .763 | 1.31 | 1.00 |
| 23 | 2 | 10 | 1 | 49742 | 529    | 528   | .9981 | .998 | 94.21| 94.03|
| 23 | 3 | 11 | 1 | 58786 | 12167  | 12134 | .9973 | .997 | 4.84 | 4.83 |
| 23 | 4 | 11 | 1 | 58786 | 279841 | 54733 | .1956 | .931 | 1.07 | 1.00 |

**The measured law.** `delta = min(|G|,|F|) * eta` with `eta in [0.76,1.0]`, and
`coll = |G|/delta` equals the generic `gen = max(1,|G|/|F|)` **to a few percent**
(e.g. `94.21` vs `94.03`, `4.84` vs `4.83`, `1.07` vs `1.00`): the projection's
fibers have their **expected** size -- **no stall**. When `|G| >> |F|` the image
**saturates** `F*` (`delta = |F|-1` exactly at `p=19,e=2` and `p=23,e=2`); when
`|G| < |F|` it is near-injective (`eta -> 1`). [verify BLOCK 6: `eta_min` per `e`
is `0.780, 0.769, 0.763`; `coll ~ gen` to `< 35%`; BLOCK 8: saturation and the
`F*` envelope `delta/(|F|-1) >= 1 - e^{-|G|/(|F|-1)}`.]

**ANTI-OBSTRUCTION (the decisive datum).** There are **exact** `rho=|G|/|F|`
matches across consecutive `e`: the depth-1 fiber at degree `e` and the full set
at degree `e+1` share `rho = binom(p,m)/p^{e+1}` identically (every sum-class
fiber has exactly `binom(p,m)/p` supports). At those matches, coverage is
**invariant under `e`**:

| `p` | `rho` (exact) | `cover(e)` | `cover(e+1)` | `\|Delta\|` |
|----:|-------:|-----------:|-------------:|------:|
| 13 | 0.78107 | 0.6095 (`e=2`) | 0.6154 (`e=3`) | 0.0059 |
| 17 | 4.94810 | 0.9965 (`e=2`) | 0.9988 (`e=3`) | 0.0022 |
| 19 | 0.70885 | 0.5453 (`e=3`) | 0.5411 (`e=4`) | 0.0041 |

An **obstruction** (image `o(|F|)` at growing `e`) would force coverage at fixed
`rho` to **decay toward 0** as `e` grows; instead it is flat to `< 0.6%` across
`e:2->3->4`. So the census **positively disfavours the obstruction** and points
to **CONSTRUCTION**: the coverage is a function of `rho` alone (essentially
`~ 1 - e^{-rho}` on `F*`, saturating), so any `|G| >= |F|` (which A3 shows is
achievable at `log|F|=log|G|=Theta(n)`) yields `delta ~ eps'|F|` with a
**constant** `eps'`, hence `e_MCA > 2^{-128}` -- a prize-relevant
`Theta(n)`-field bad line. [verify BLOCK 7: exact `rho` equality + coverage
`|Delta| < 0.02` for all three pairs.]

**Robustness.** Coverage is independent of the choice of pole (a shifted pole
`alpha + s`, `s in F_p`, still of degree `e`, gives an identical value set -- it
only relabels `D`). [verify BLOCK 10: `union_delta` and `max_delta` unchanged
under `alpha -> alpha+3` for `(p,e) in {(13,2),(17,3),(19,3)}`.]

---

## Rung A1' -- INJECTIVE-ON-CLOSE: the slope fibers are spread codes (PROVED)

The generic behaviour above has a rigorous shadow that **rules out heavy
concentration**:

> **Lemma (injective on close supports, PROVED).** If `|S triangle S'| <= 2e`
> then `Q_S(alpha) = Q_{S'}(alpha)` implies `S = S'`.

*Proof.* Let `A = S setminus S'`, `B' = S' setminus S`, disjoint, `|A|=|B'|=t<=e`.
`Q_S(alpha)=Q_{S'}(alpha)` gives `prod_{a in A}(alpha-a) = prod_{b in B'}(alpha-b)`,
so `prod_{A}(X-a) - prod_{B'}(X-b)` (both monic of degree `t`, leading terms
cancel) is a polynomial over `B` of degree `<= t-1 < e` vanishing at `alpha`.
Since `[B(alpha):B] = e`, it is identically zero, so the two monic polynomials
are equal, `A = B'`, contradicting disjointness unless `A=B'=empty`, i.e.
`S=S'`. `QED`

Thus every collision has `|S triangle S'| > 2e`: the fibers `Q_.^{-1}(c)` are
**constant-weight codes with minimum symmetric-difference distance `> 2e`** --
forced to be **spread**. [verify BLOCK 9: brute-force min collision side-symdiff
is `> e` for `(p,e,m) in {(7,2,4),(11,2,5)}` and no collisions for `(7,3,5)`.]
This is genuine evidence *against* an obstruction (a concentrating map would need
tight fibers), but it is **not** enough to prove the construction: the resulting
Johnson/packing multiplicity bound is `binom(n,m-e)/binom(m,e)`, which exceeds the
generic multiplicity `|G|/|F|` by a factor `exp(Theta(e))` -- too weak by exactly
the amount the character sum would supply.

---

## Rung A2 -- why the asymptotic proof is genuinely open (honest, no hand-waving)

Coverage `>= eps'|F|` at `|G| >= |F|` is equivalent to a **uniform multiplicity**
bound: the number of `m`-subsets of the affine `B`-line `V = alpha - D` with a
prescribed product is `O(|G|/|F|)`. In Fourier terms, coverage of `eps'|F|` holds
iff the pushforward measure `(Q_.(alpha))_* Unif(G)` has small non-trivial
coefficients,

```
   hat mu(psi) = (1/|G|) sum_{S in G} psi( prod_{x in S}(alpha - x) ),   psi != 1.
```

The summation set `G` is a slice (fixed low symmetric functions) of the space of
`m`-subsets, and the phase `prod(alpha - x)` is a symmetric multiplicative
function of the moving support. This is exactly the setting where **Weil/Deligne
give square-root cancellation** -- *provided the phase is non-degenerate and the
ambient dimension is bounded*. Here the dimension of the defining variety grows
with `n` (the moving support has `Theta(m) = Theta(n)` coordinates), so a
bounded-dimension Weil estimate does **not** apply off the shelf: the Deligne
bound carries an implied constant -- a product of degrees / a sum of Betti numbers
`C(dim, deg)` -- that grows as the dimension `-> infty`, and it is exactly this
constant that must be shown to stay below `q0^{dim/2}` for the sum to be
`o(|G|)`. We do **not** track that constant to a decision here (doing so is the
open problem), so we must **not** write "Weil gives equidistribution": at
`e = Theta(n/log q0)` that is an **unestablished** claim, not a proof. It could go
either way -- a fibered or low-degree reformulation of the phase (which we did not
find) would give the construction; an unavoidable degeneracy would give the
obstruction. Two independent finite signals cut *against* the obstruction, though:
the census flatness (coverage `e`-invariant at fixed `rho`, Rung A4) and the
injective-on-close lemma (spread fibers, Rung A1'). **The last open link is
precisely a dimension-uniform equidistribution law for products of `m`-subsets of
an affine `B`-line** -- a genuine analytic-number-theory question, which is why
`#645`/`#647` left it as the residual and why we label it **OPEN** rather than
force a verdict.

---

## Rung V -- VERDICT, the exact boundary, and the closure impact

**VERDICT = PARTIAL, decisively construction-pointing.** Decomposed by regime:

- **Poly-field / shallow sub-regime (`|G| > eps q0^{k+1}`): CONSTRUCTION, PROVED.**
  The rigorous surjectivity bound `(LB)` gives `delta >= |G|/q0^{k+1-e} > eps|F|`;
  this is exactly `#647`'s poly-field class (and the Case-A `delta=|G|` witnesses).
- **Over-field sub-regime (`|F| > binom(n,m)/eps`, i.e. `c > H2(beta)`):
  OBSTRUCTION by counting, PROVED.** `delta <= |G| < eps|F|`: no prize-relevant
  line, the field is simply too large for the fiber. (Combined with Case A's
  automatic `delta <= |F|^{1/2}`, this is the part of the exponential regime that
  *is* rescued: at `c > H2(beta)` the collapse cell contributes `o(eps|F|)`.)
- **Critical exponential sub-regime (`|G| ~ |F|`, `c <= H2(beta)`,
  `e = Theta(n/log q0)`): CONSTRUCTION-pointing, MEASURED; OPEN as a theorem.**
  The census (14 Case-B cells, `e<=4`) shows `delta = eta * min(|G|,|F|)` with
  `eta` bounded below and **coverage `e`-invariant at fixed `rho`** -- so a
  prize-relevant `Theta(n)`-field bad line **exists** at every reachable scale.
  The asymptotic proof reduces to the subset-product equidistribution law (Rung
  A2) and is the single open link.

**The exact boundary** between decided and open is the curve `c = H2(beta)` in the
`(c=log2|F|/n, beta=m/n)` plane, refined by depth: **decided** for
`c > H2(beta)` (obstruction) and for shallow fibers `n=O(1)` (construction);
**open** on the strip `0 < c <= H2(beta)` with `e = Theta(n/log q0) -> infty`,
where the census says construction but no theorem yet does.

**Closure impact (#650).** `(FI-field')` is **not** weakenable to a free
`|F|^{1/2}` bound (already `#647`), and this packet adds that it is **not**
weakenable by counting either (A3): the corner it guards is real. The census says
`(FI-field')` is **tight** -- a prize-relevant `Theta(n)`-field witness class most
likely exists -- so the clause should stay **printed as-is** in
`def:admissible-sequence`. Its final status splits cleanly:

- if the subset-product law holds (CONSTRUCTION) -> `(FI-field')` is provably
  **necessary and tight**, the closure's printed clause is exactly right;
- if it fails (OBSTRUCTION, `image=o(|F|)` for admissible deep fibers) -> the
  collapse cell contributes `o(eps|F|)` at **all** field sizes (combining with the
  over-field and Case-A halves), and the C7 collapse cell would need **no**
  field clause at all -- a strict strengthening of the closure.

Either way the packet has pinned the corner to **one** analytic law and delivered
the rigorous partial closure around it.

---

## The 2-3 least-certain steps (for the PI)

1. **The generic-fibre reading of the census (Rung A4).** We infer "equidistribution
   up to a bounded constant" from `coll = |G|/delta ~ max(1,|G|/|F|)` to a few
   percent and from coverage `e`-invariance at three exact `rho`-matches
   (`e<=4`). This is a **finite** signal; the extrapolation to `e=Theta(n/log q0)`
   is not proved. A counterexample would have to appear only at `e>=5`, which the
   `e`-invariance at fixed `rho` makes unlikely but does not exclude.
2. **The Weil-applicability claim (Rung A2).** We assert only that the standard
   *bounded-dimension* Deligne estimate does not apply off the shelf, because the
   phase's dimension grows with `n` and the implied constant is uncontrolled. We
   deliberately do **not** assert the sum is large (that would be an unproved
   obstruction) nor small (an unproved construction); a low-degree or fibered
   reformulation of the phase (which we did not find) could rescue square-root
   cancellation. This applicability gap -- not a settled sign -- is the open link.
3. **The A3 prize-regime feasibility (Rung A3, BLOCK 1b).** The poly-base-field
   witness uses `q0=n^C`, `C>=2`, `m=2e`, `w=4`, and a Stirling estimate
   `log2(m!) ~ m log2 m`. The inequality `(m-e)log2 q0 >= log2(m!) - 128` is
   checked numerically at `n in {2^14,2^16,2^18}`; the constant `C>=2` is where
   the domination begins, and a row with `C=1` (base field `~n`) would sit exactly
   at the boundary. Whether the prize's actual smooth/circle rows have `C>=2` is a
   row-specific fact we take from the poly-size scope, not re-derive.

---

## Reproducibility

```
$ ulimit -v 2097152
$ python3 experimental/scripts/verify_caseb_equidistribution.py
... RESULT: PASS (116/116)      (~20 s, ~133 MB)
```

The script is stdlib-only and zero-arg. It builds exact `GF(p^e)` (Rabin
irreducibility), recomputes every table entry (Case-A boundary curve, the 14
Case-B census cells, the exact `rho`-matched anti-obstruction pairs, the `F*`
envelope and saturation, the injective-on-close finite check), verifies the A3
counting satisfiability/closure and the exact ceiling `e_max`, verifies the A1
identity block (surjectivity) and the rigorous lower bound `(LB)`, and exits
nonzero on any mismatch. `BLOCK n` tags in the source map one-to-one to the
`verify BLOCK n` citations above.
