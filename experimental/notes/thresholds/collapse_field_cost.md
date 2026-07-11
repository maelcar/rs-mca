# The C7 collapse cell's field cost is linear, not quadratic: delta ~ |F|, not |F|^{1/2}

## Status

`|F|^{1/2} PER-LINE SHARPENING REFUTED (PROVED, explicit Theta(|F|) collapse
line) / eq (4.5) SEPARATION GATE CONFIRMED SUFFICIENT-NOT-NECESSARY, quantified
(COMPUTED) / DOUBLE-COUNTING HEART GIVES NO FIELD BOUND ABOVE JOHNSON (PROVED,
2a-n<k) / POLY-FIELD REFUTATION IS HARMLESS -- span face still closes on it
(#645 column 1) / EXPONENTIAL PRIZE-RELEVANT CORNER STILL OPEN = #645's residual
(equidistribution) / (FI-field') PLACEMENT STANDS`.

**One-line verdict (REFUTED, with a sharp regime split).** *On C7 effective-image-
collapse cell lines, `delta(r) <= |F|^{1/2+o(1)}` is **not** forced. An explicit
**pure** collapse line -- a single depth-`w` prefix fiber, image size `L=1`,
ambient `A=|B|^w`, so `G_1 = A/L = |B|^w` (the effective-image-collapse trigger,
#627 T-DET) and `Q_img = 1` -- carries `delta = Theta(|F|)` distinct MCA-bad
slopes: **linear** in the field, matching the T-FIELD upper bound
`delta <= |F_r|` (#642) up to a constant and refuting the `1/2` exponent. The
mechanism is `#645`'s own honest flag 3 made concrete: the paper's `binom(N,2)`
separation cost (eq (4.5)) is **sufficient, not necessary**, and a structured
list separates `N` slopes in a field of size `~N` rather than `~N^2`. The
refutation is genuine but **harmless for the prize**: the `Theta(|F|)` witnesses
live over a **polynomial** field (`log|F| = O(log n)`, `#645` column 1), where
`delta = poly(n) = e^{o(n)}` and the span face closes unconditionally anyway. In
the **exponential** field regime -- the only one that could be prize-relevant --
the paper's countertheorem **saturates** `delta ~ |F|^{1/2}` (diluted,
`e_{MCA} = 1/N -> 0`), and whether `delta` can climb to `~|F|` (prize-relevant)
reduces to an equidistribution question that is **exactly #645's open residual
corner**. Net: the biggest-prize route ("`|F|^{1/2}` forces a constant field,
closing the span face with no field hypothesis") **does not go through**;
`(FI-field')` remains genuinely load-bearing and `#645`'s placement of it in
`def:admissible-sequence` stands.*

Every number below is recomputed by
`experimental/scripts/verify_collapse_field_cost.py` (stdlib-only, zero-arg,
`RESULT: PASS (42/42)`, ~1.8 s, well under `ulimit -v 2097152`).

Label key: **PROVED** (hand derivation, exact, recomputed), **COMPUTED** (exact
finite recomputation of a promoted/witness quantity), **MEASURED** (exact finite
toy census), **AUDIT** (verbatim interface reading of the tex), **OPEN**.

**Credit.** The residual question -- *does prize-relevance force
`delta <= |F|^{1/2}` on the C7 collapse cell?* -- is the open corner named by our
**#645** (`fi_field_discharge.md`, the `(RED)` reduction `e_{MCA}=delta/|F|` and
honest flag 3: "the `binom(N,2)` field cost is proved **sufficient, not
necessary**"). The field-of-definition law `delta <= |F_r|` (T-FIELD) and the
two-sided `delta = Theta(|F_r|)` (T-LAW) are our **#642**
(`c7_collapse_image_degree.md`, read first). The `(star)` list-`<=1`-above-
`(n+k)/2` rigidity and the identity list floor `L(a)` are our **#544**
(`simple_pole_realizability.md`). The MASTER-2 split `E+1 <= G_1 Q_img` with
`G_1 = A_{eff}/L`, `Q_img = L max mu` is our **#625** (`c7_routing_spectrum.md`);
the router-decidable collapse trigger **T-DET** (`G_1` exponential `<=> L << A`)
is our **#627** (`routing_exhaustiveness.md`); the first-match disjoint charge
`Z_a(r) = coprod_i Z_i^o` is our **#635** (`collapse_payment.md`). The prefix-
image bound `|Phi_u(O)| <= q^{ceil(u/2)}` is **Codex #634**
(`full_agreement_orientation_saturation.md`). The exact counting machinery we
extract and stress -- `thm:collision-aware-pole` (eq (4.2)),
`prop:exact-prefix-list` (eq (4.1)), `prop:prefix-rigidity-full` (Johnson, eq
(4.4)), `thm:prefix-to-line-hardness` (eq (4.5)), and
`thm:exact-list-line-bijection` (eq (4.6)) -- is **THE PAPER'S OWN**, formalized
in Lean by **Codex #624** (statements consumed as trustworthy pins), and the
countertheorem we recompute is `thm:intro-countertheorem`. DannyExperiments
**#621**/**#631**/**#641** are the confined / unbounded-extension instances
consumed through #642. No finite M31/KoalaBear survivor count, adjacent
inequality, or target threshold is touched. (No multiplicative-energy input from
hughes #564 / LegaSage was needed -- see Rung 2: that route does **not** cap the
count, and we say why.)

---

## HEADLINE (read first): the residual field cost is linear

`#642` proved the C7 collapse cell's per-line degree is bounded by the received
line's field of definition, `delta_lambda(r) <= |F_r|` (T-FIELD), and forced
tight `delta = Theta(|F_r|)` **only** on the countertheorem's exponential
extension (`log|F_r| = Theta(n)`). `#645` reduced prize-relevance to the ambient-
field size via `(RED)` `e_{MCA}(r) = delta(r)/|F| <= |F_r|/|F|`, and left **one**
honest gap (flag 3): the countertheorem's field cost

```
   |F| > n + k binom(N,2) ~ k N^2 / 2        (eq (4.5), separate N slopes)
```

is proved **sufficient**, not necessary. If it were also **necessary** -- i.e.
if `delta <= |F|^{1/2+o(1)}` were forced on collapse cells -- then prize-relevance
`delta/|F| > eps = 2^{-128}` would give `|F|^{1/2-o(1)} < 2^{128}`, hence
`|F| < 2^{256+o(n)}`: a **constant** field, `delta = O(1)` per line, and the span
face would close with **no field hypothesis at all**. That is the biggest
available prize on this face. **This packet decides it: the sharpening is FALSE.**

The witness is an explicit **pure effective-image-collapse line**. Take the base
field and domain `B = D = F_p`, the ambient `F = F_{p^2}` (a scalar extension,
`B subsetneq F`), agreement `m = 3`, prefix depth `w = 1` (so `k = m-w-1 = 1`).
The single depth-1 prefix fiber

```
   G = { 3-subsets S of F_p : e_1(S) = sum of S = sigma (fixed) }
```

has prefix-image size `L = |Phi_1(G)| = 1` and ambient `A = |B|^1 = p`, so its
collapse factor is `G_1 = A/L = p = |B|^w` and its occupancy is flat
(`Q_img = 1`): by **#627** T-DET this is a **pure** effective-image-collapse cell
(the extreme case `L << A`, matching #625's worked example `L=p^k, A=p^{2k}`).
Choose any pole `alpha in F setminus F_p` (degree 2 over `B`). Then **every** pair
of the fiber's supports gives a **distinct** slope on the received line
`(f_alpha, g_alpha)`, so

```
   delta(r) = |G| = #{3-subsets of F_p summing to sigma}
            = (p-1)(p-2)/6 = Theta(p^2) = Theta(|F|).      (CENTERPIECE, PROVED)
```

`delta = (p-1)(p-2)/6` is **linear** in `|F| = p^2`; the ratio
`delta/|F| = (p-1)(p-2)/(6p^2)` rises monotonically to `1/6`. So `delta`
**exceeds** `|F|^{1/2} = p` for every `p >= 11` and grows like the field, not its
square root. [verify BLOCK B: injective for `p in {5,...,37}`,
`delta = (p-1)(p-2)/6` exactly, `delta/|F|: 0.080 -> 0.153 (-> 1/6)`.]

The proof of distinctness is one line of linear algebra (Rung 3). The point is
that the `binom(N,2)` collision loci of eq (4.5) are **not independent** for a
structured fiber: a single pole clears them all. [verify BLOCK E: this line
separates `N = (p-1)(p-2)/6` slopes in `|F| = p^2`, while eq (4.5)'s sufficient
size is `n + k binom(N,2) ~ N^2/2`; the ratio grows `1.4x -> 34.7x` across
`p = 13..53`, i.e. the gate over-charges by a factor `~ p^2/2`.]

---

## Rung 1 -- EXTRACT the counting machinery (AUDIT, verbatim tex)

Target `experimental/asymptotic_rs_mca_frontiers.tex`.

### 1a. The pole conversion is a list-to-slope bijection (eq (4.1), (4.6))

`prop:exact-prefix-list` (**L1965-1977**): for `U_z(X)=X^m+sum_{i=1}^w z_i
X^{m-i}` and `w = m-K`, the codewords of `RS_F(D,K)` agreeing with `U_z` on `>= m`
points are **exactly** `(U_z - Q_S)|_D`, `S in Phi_w^{-1}(z)`, where
`Q_S(X)=prod_{x in S}(X-x)`. `thm:exact-list-line-bijection` (**L2096-2126**): for
a separating pole `alpha in F setminus D` (`P |-> P(alpha)` injective on the list
`L_m(U)`), the map `P |-> P(alpha)` is a **bijection** from `L_m(U)` onto the
finite MCA-bad slopes of the received line `(f_alpha, g_alpha)`,
`f_alpha = U/(X-alpha)`, `g_alpha = -1/(X-alpha)`. Such a pole exists whenever
`|F| > n + k binom(L,2)` (eq (4.6)). **Consequence we use throughout:**

```
   delta(r) = #{ distinct P(alpha) : P in L_m(U) }
            = #{ distinct Q_S(alpha) : S in Phi_w^{-1}(z) }   (fiber form),
```

since `P_S(alpha) = U_z(alpha) - Q_S(alpha)` and the `U_z(alpha)` shift is common.

### 1b. The separation gate (eq (4.5)) -- and why it is only SUFFICIENT

`thm:prefix-to-line-hardness` (**L2073-2094**), verbatim: for a fiber `G` of `N`
`m`-sets, `k = m-w-1`, *"Every finite extension `F/B` satisfying `|F|-n >
k binom(N,2)` admits one received line ... with at least `N` distinct MCA-bad
slopes."* Its proof: for distinct `S,T`, `Q_S - Q_T` is nonzero of degree `<= k`
(the shared prefix cancels the top `w+1` coefficients); condition (4.5) leaves a
pole `alpha` avoiding the roots of **all** `binom(N,2)` differences, so the values
`Q_S(alpha)` are pairwise distinct. **AUDIT:** the pole must avoid a union of
`binom(N,2)` root sets, bounded crudely by `k binom(N,2)`; the theorem never
claims this union is that large -- it is an **upper** bound on the forbidden set.
Nothing forces `|F| >= N^2` for a *particular* structured `G`. This is the exact
crack `#645` flag 3 pointed at.

### 1c. The collision-aware floor (eq (4.2)) and the double-count it rests on

`thm:collision-aware-pole` (**L1996-2029**): `L` distinct dim-`(k+1)` codewords
agreeing on `>= m` points give one line with `>= M(L) = ceil(L(q-n)/(q-n+k(L-1)))`
distinct slopes. Its proof is the **double-count** we dissect in Rung 2:
`P_i(alpha)=P_j(alpha)` at `<= k` poles; pole-averaging finds a pole with
`<= k binom(L,2)/(q-n)` colliding pairs; Cauchy-Schwarz `L^2 <= M sum m_i^2`
closes it. Codex **#624** formalized (4.2)/(4.1) in Lean; we treat them as pins.

### 1d. Johnson rigidity (eq (4.4)) and the `(star)` list ceiling (#544)

`prop:prefix-rigidity-full` (**L2044-2071**): two distinct `m`-sets in one depth-
`w` fiber have Johnson distance `>= w+1`. `#544`'s `(star)`: a dim-`(k+1)` list of
size `>= 2` requires agreement `a <= (n+k)/2` (two distinct degree-`<=k`
codewords agree in `<= k` points, so `|A_1 cup A_2| = 2a - |A_1 cap A_2| >= 2a-k`
and `<= n`). **This is the load-bearing arithmetic for Rung 2.**

### 1e. T-FIELD and the collapse trigger (#642, #625/#627)

`thm:subfield-confinement-full` (**L1930-1943**): every MCA-bad slope of a
`B`-valued line lies in `B`; applied to `B subseteq F_r subseteq F` this is
`#642`'s T-FIELD `delta_lambda(r) <= |F_r|`. `#627` T-DET: a cell is
effective-image collapse iff `G_1 = A_{eff}/L` is exponential, predicate
`L << A`, decided from `L=|Phi(Omega)|`, `A=|B^R|`. A single prefix fiber is the
extreme `L=1`.

---

## Rung 2 -- THE COUNTING HEART: where the |F|^{1/2} hope dies (PROVED)

The mission's R2 asked whether the classical list-decoding double-count, plus the
collapse-cell structure, forces `delta <= |F|^{1/2}` via a Sidon / multiplicative-
energy argument on the slope difference set. **It does not, and here is exactly
why -- three failures, each pinned to an inequality.**

### 2a. The support-intersection identity re-derives the list, gives no field bound

Let `gamma_1,...,gamma_N` be the distinct slopes, `gamma_i = P_i(alpha)`, each bad
via `S_i`, `|S_i| >= m = a`. On the line `(f_alpha,g_alpha)`, `gamma_i` is
explained on `S_i` by `h_{P_i}(X) = (P_i(X)-P_i(alpha))/(X-alpha)`, `deg < k`.
For `i != j`, on `S_i cap S_j` subtract the two explanations:

```
   (gamma_i - gamma_j) g_alpha  =  h_{P_i} - h_{P_j}   on  S_i cap S_j.   (INT)
```

So a nonzero `F`-scaling of `r_1 = g_alpha = -1/(X-alpha)` agrees, on
`S_i cap S_j`, with a degree-`<k` polynomial. **Push it exactly:** if
`|S_i cap S_j| > k` and `gamma_i != gamma_j`, then `-1/(x-alpha) = c R(x)` on
`> k` points with `deg R < k`; then `(X-alpha)R(X) + 1/c` has degree `<= k` and
vanishes at `> k` points, so it is identically zero, forcing
`R = -1/(c(X-alpha))` -- not a polynomial, contradiction. Hence

```
   gamma_i != gamma_j  ==>  |S_i cap S_j| <= k.        (re-derives the list)
```

This is **only** the list-decoding structure (`#544`'s `<= k` overlap); it
produces **no bound on `|F|`**. `(INT)` is the identity the mission hoped would
"collapse the cell", but it collapses to a tautology.

### 2b. Above Johnson the rigidity trigger never fires: `2a - n < k` (PROVED)

The `> k` trigger of 2a needs `|S_i cap S_j| > k`. The only unconditional lower
bound is `|S_i cap S_j| >= 2a - n`. But a collapse cell carries an **exponential**
list, which by `(star)` (#544, Rung 1d) requires

```
   a <= (n+k)/2   ==>   2a - n <= k,   strictly < k below the Johnson radius
                        a ~ sqrt(kn)  (there 2a-n ~ 2 sqrt(kn) - n < 0).
```

So on exactly the cells with many slopes, the pairwise intersections are **at or
below `k`**, the rigidity trigger of 2a is vacuous, and the double-count gives
`|S_i cap S_j| <= k` with **nothing on the other side**. *This is the precise
location of the classical failure the mission asked us to find: the double-count
yields polynomial list bounds only for `a > sqrt(kn)` (above Johnson), and the
collapse cell lives below it.* [verify: `(star)` is #544's C2, gated there.]

### 2c. The slopes are NOT confined to a small multiplicative set

The slope is `Q_S(alpha) = prod_{x in S}(alpha - x)`, a product over an `m`-subset
of the fixed `n`-element set `V = {alpha - x : x in D} subset F^*`. The mission's
multiplicative-energy hope was that the collapse image forces the slope
**differences** into a small multiplicative structure, capping `N` by a
Sidon/`|F|^{1/2}` bound. But writing `Q_S(alpha)` in coordinates (Rung 3) shows
the opposite: on a fiber the slopes are an **injective affine image** of the free
symmetric coordinates, so their difference set is as **large** as the fiber, with
**no** multiplicative concentration. There is no Sidon cap because there is no
small multiplicative set to begin with. The collapse structure (`L << A`) is a
statement about the occupancy **across** fibers; it places **no** constraint on a
**single** fiber's per-line slope count -- which is why `#642` needed the *field*
(`|F_r|`), not the image, to bound it.

**Conclusion of Rung 2.** Neither the double-count (2a-2b) nor a multiplicative-
energy argument (2c) yields `delta <= |F|^{1/2}`. The `1/2` in eq (4.5) is a
**sufficient-field** artifact of demanding a pole that separates **every** pair
simultaneously in **general position**; it is not a property of the count.

---

## Rung 3 -- REFUTE: an explicit Theta(|F|) collapse line (PROVED)

### The injectivity lemma (PROVED). One structured pole beats all binom(N,2) loci.

Expand the slope on a depth-`w` fiber (`e_1,...,e_w` fixed):

```
   Q_S(alpha) = sum_{i=0}^m (-1)^i e_i(S) alpha^{m-i}
              = C(alpha) + sum_{j=0}^k a_j(S) alpha^j,   a_j(S)=(-1)^{m-j} e_{m-j}(S),
```

where `C(alpha) = sum_{i=0}^w (-1)^i e_i alpha^{m-i}` is **constant on the fiber**
and `k = m-w-1`. The free coordinates `(a_0,...,a_k)` are the free symmetric
functions `(e_{w+1}(S),...,e_m(S)) in B^{k+1}`, and they **determine `S`** (a set
is recovered from its elementary symmetric functions together with the fixed
prefix). Therefore:

> **Lemma (Case-A injectivity, PROVED).** If `1, alpha, ..., alpha^k` are
> `B`-linearly independent -- i.e. the pole has degree `[B(alpha):B] >= k+1` --
> then `S |-> Q_S(alpha)` is **injective** on the fiber, so
> `delta(r) = |Phi_w^{-1}(z)|` (the full fiber size). A separating pole then
> exists in **any** extension with `[F:B] >= k+1`, i.e. `|F| >= |B|^{k+1}`.

*Proof.* `Q_S(alpha) = Q_T(alpha)` gives `sum_{j=0}^k (a_j(S)-a_j(T)) alpha^j = 0`
with coefficients in `B`; `B`-independence of `1,...,alpha^k` forces
`a_j(S)=a_j(T)` for all `j`, hence equal free symmetric functions, hence `S=T`.
`QED` [verify BLOCK C: injective for `(p,m) in {(5,3),(5,4),(7,3),(7,4),(7,5)}`
over `F_{p^{m-1}}`.]

### The centerpiece (PROVED). `m=3, w=1`: `delta = (p-1)(p-2)/6 = Theta(|F|)`.

Here `k = 1`, so the lemma needs only `[B(alpha):B] >= 2`: **any**
`alpha in F_{p^2} setminus F_p`. The fiber is the `3`-subsets of `F_p` with fixed
sum `sigma`; by translation-transitivity of the sum on `F_p` (`p != 3`) each
`sigma` gets exactly `binom(p,3)/p = (p-1)(p-2)/6` of them. So

```
   delta(r) = (p-1)(p-2)/6,   |F| = p^2,   delta/|F| -> 1/6,   delta > |F|^{1/2}
                                                                    for all p >= 11.
```

This is a single received line for `RS_{F_{p^2}}(F_p, 1)` over an ambient field
that is a **scalar extension** of the base field (`#645`'s "challenge over a
scalar extension"), realizing `Theta(|F|)` distinct MCA-bad slopes on a pure
effective-image-collapse cell. **`delta <= |F|^{1/2+o(1)}` is false.** [verify
BLOCK B.]

### Case B and the regime dichotomy (PROVED upper / OPEN realizability)

If instead `[B(alpha):B] = e < k+1` (a **low-degree** pole, small field
`|F| = |B|^e`), the powers `alpha^0,...,alpha^k` reduce into an `e`-dimensional
`B`-space, and

```
   delta(r) = #{ image of the fiber under the rank-<= e Vandermonde projection
                 (a_0,...,a_k) |-> sum a_j alpha^j }  <=  |B|^e = |F|.
```

So `delta <= |F|` (never better than T-FIELD), and `delta ~ |F|` **iff** the
fiber's free-symmetric-coordinate point set covers a constant fraction of the
`e`-dimensional image. Two consequences:

- **(PROVED, upper) Case A over an exponential field forces `delta <= |F|^{1/2}`.**
  In the deep collapse regime (`n = q_0`, `m = c n`, `w = Theta(n/log n)`), Case-A
  injectivity demands `|F| >= q_0^{k+1} = q_0^{m-w}`, whose square-root exponent
  `(m-w)/2 log q_0 = Theta(n log n)` **dwarfs** `log|fiber| <= log binom(n,m) =
  Theta(n)`. So a high-degree pole buys separation only by making the field so
  large that `delta = |fiber| <= |F|^{1/2}` automatically. The countertheorem
  **realizes this ceiling**: paying the generic-position cost `|F| ~ N^2` for
  `N = e^{(h/4)n}` slopes, it sits at `delta = N = |F|^{1/2}` **exactly**,
  `e_{MCA} = 1/N -> 0` (**diluted**). [verify
  BLOCK F: Case-A `delta <= |F|^{1/2}` holds for `q_0 in {101,1009,10007}`;
  countertheorem `log delta = log|F|^{1/2}` exactly for `n in {100,1000,10000}`.]

- **(OPEN) Case B over an exponential field is #645's residual corner.** A
  prize-relevant exponential counterexample needs `delta ~ |F|` with
  `log|F| = Theta(n)` -- i.e. a **low-degree** pole and a **deep** fiber whose
  Vandermonde image **equidistributes** over `F`. Our `m=3` witness does this for
  `e = 2` (constant degree, polynomial field); whether it survives to
  `e = Theta(n/log q_0)` is an equidistribution question we do **not** settle. It
  is precisely the corner `#645` left OPEN.

---

## Rung 4 -- TOY CENSUS (MEASURED, verifier-recomputed)

Exact `GF(p^d)` (irreducible modulus via a Rabin test), `B = D = F_p`, pole in
`F setminus F_p`, `delta = #{Q_S(alpha)}` on a depth-`w` fiber.

**(a) Centerpiece exact curve (BLOCK B), `m=3, w=1`, `F = F_{p^2}`:**

| `p` | `\|F\|=p^2` | fiber | `delta` | inj? | `delta/\|F\|` | `sqrt\|F\|=p` | `delta>sqrt\|F\|` |
|----:|-----:|-----:|-----:|:--:|-----:|-----:|:--:|
| 5  | 25  | 2   | 2   | yes | .080 | 5  | no |
| 7  | 49  | 5   | 5   | yes | .102 | 7  | no |
| 11 | 121 | 15  | 15  | yes | .124 | 11 | **yes** |
| 13 | 169 | 22  | 22  | yes | .130 | 13 | **yes** |
| 17 | 289 | 40  | 40  | yes | .138 | 17 | **yes** |
| 23 | 529 | 77  | 77  | yes | .146 | 23 | **yes** |
| 31 | 961 | 145 | 145 | yes | .151 | 31 | **yes** |
| 37 | 1369| 210 | 210 | yes | .153 | 37 | **yes** |

`delta = (p-1)(p-2)/6` exactly; `delta/|F| -> 1/6`; `delta > sqrt|F|` for all
`p >= 11` and the gap widens. **Exponent `log delta/log|F| -> 1`** (the exact
`Theta(|F|)` law, PROVED, not merely a finite artifact).

**(b) `N_max(q)` over collapse cells (BLOCK D), max over `m in {3..7}`, `w=1`,
`F = F_{p^2}`, all poles:**

| `p` | `q=\|F\|` | best `m` | max fiber | `N_max` | `sqrt q` | `N_max/sqrt q` | exponent `log N/log q` |
|----:|-----:|:--:|-----:|-----:|-----:|-----:|-----:|
| 5  | 25  | 3 | 2   | 2   | 5  | 0.40 | 0.22 |
| 7  | 49  | 3 | 5   | 5   | 7  | 0.71 | 0.41 |
| 11 | 121 | 5 | 42  | 41  | 11 | 3.73 | **0.77** |
| 13 | 169 | 6 | 132 | 108 | 13 | 8.31 | **0.91** |

The measured exponent climbs `0.22 -> 0.41 -> 0.77 -> 0.91`, crossing `1/2` and
heading to `1` (consistent with the exact `Theta(|F|)` law). `N_max/sqrt q` is
**unbounded** (`0.40 -> 8.31`), so `delta/|F|^{1/2}` is not `q^{o(1)}`: the `1/2`
exponent is refuted, not merely grazed.

**(c) eq (4.5) gate looseness (BLOCK E):** the `m=3` line separates
`N=(p-1)(p-2)/6` slopes in `|F|=p^2`, where eq (4.5)'s **sufficient** size is
`n + k binom(N,2) ~ N^2/2`; the over-charge ratio grows
`1.4x (p=13) -> 34.7x (p=53)`, i.e. the gate is loose by `~p^2/2`. **Sufficient,
not necessary -- quantified.**

**(d) Collapse classification (BLOCK G):** a single fiber has `G_1 = A/L = |B|^w`
(exponential when `w ~ n/log|B|`) and `Q_img = 1` -- a **pure** effective-image-
collapse cell by #627 T-DET, not a saturation cell. **(e) RED harmlessness
(BLOCK H):** the poly-field witness has `e_{MCA} = delta/|F| -> 1/6 = Theta(1)`
(**charges** the target) yet `delta = poly(n) = e^{o(n)}`, so it sits in `#645`
column 1 where the span face closes regardless.

---

## Rung 5 -- VERDICT + ledger entry

**Verdict = REFUTED** (the `|F|^{1/2}` sharpening is false), **with a sharp
regime split that leaves #645's corner exactly where it was.**

- **PROVED (refutation):** there is an explicit **pure** C7 effective-image-
  collapse received line (`m=3, w=1, B=D=F_p, F=F_{p^2}`, `L=1`, `G_1=|B|^w`,
  `Q_img=1`) with `delta(r) = (p-1)(p-2)/6 = Theta(|F|)`. Hence
  `delta <= |F|^{1/2+o(1)}` is **not** forced; the honest per-line exponent is
  `1`, meeting the T-FIELD bound `delta <= |F_r| <= |F|` (#642) up to a constant.
- **PROVED (why the natural proofs fail):** the list-decoding double-count only
  re-derives `|S_i cap S_j| <= k` and gives no field bound; above Johnson the
  rigidity trigger is vacuous because `2a - n < k` (from `#544`'s `(star)`); and
  the slopes carry **no** small multiplicative structure to feed a Sidon/energy
  bound (they are an injective affine image of the free symmetric coordinates).
- **COMPUTED (the gate, quantified):** eq (4.5)'s `binom(N,2)` field cost is
  **sufficient, not necessary**; a structured fiber separates `N` slopes in
  `|F| ~ N` (over-charge ratio `-> p^2/2`). This confirms `#645` flag 3 with an
  explicit family.
- **PROVED (harmless / regime split):** the `Theta(|F|)` witnesses are
  **polynomial-field** (`log|F| = O(log n)`), where `delta = poly(n) = e^{o(n)}`
  and the span face closes unconditionally (`#645` column 1). Over an
  **exponential** field, Case-A injectivity forces `delta <= |F|^{1/2}` (the
  countertheorem's diluted saturation, `e_{MCA} -> 0`).
- **OPEN (unchanged):** whether a **prize-relevant** line can have `delta ~ |F|`
  with `log|F| = Theta(n)` -- Case B with a deep equidistributing fiber -- is
  **exactly** `#645`'s residual corner, untouched by this packet. So `(FI-field')`
  is **not** derivable from a per-line quadratic cap (there is none), and it
  remains a genuine printed input.

### The exponent bracket (final form)

```
   delta(r) = |F|^c  on C7 effective-image-collapse lines:

     c <= 1                     ALWAYS            (T-FIELD, #642; PROVED)
     c  = 1  realized           poly field        (CENTERPIECE; PROVED)   <- refutes 1/2
     c  = 1/2 realized-diluted  exp field         (countertheorem; PROVED-achievable)
     c ->  1  prize-relevant    exp field          OPEN  (= #645 residual, equidistribution)

   There is NO universal cap at c = 1/2.  The proposed unconditional closure
   ("|F|^{1/2} => constant field => O(1) slopes => no field hypothesis") is DEAD.
```

### Superseding note for the maintainer (extends #642 T-LAW and #645 flag 3)

*The C7 collapse cell's per-line field cost is linear, not quadratic. `#642`
proved `delta_lambda(r) <= |F_r|` (T-FIELD) and forced it tight only on the
countertheorem's exponential extension; `#645` reduced prize-relevance to
`e_{MCA}=delta/|F|` and flagged that eq (4.5)'s `|F|>n+k binom(N,2)` separation
cost is proved **sufficient, not necessary**. It is not necessary, and the gap is
**linear in the field, not quadratic**: expanding the slope on a depth-`w` fiber,
`Q_S(alpha) = C(alpha) + sum_{j=0}^k a_j(S) alpha^j` with `a_j` the free symmetric
functions, so a pole of degree `>= k+1` makes `S |-> Q_S(alpha)` **injective** and
`delta = |fiber|`. Concretely, over `F_{p^2}` (`B=D=F_p`, `m=3`, `w=1`, `L=1`) a
single pure-collapse line carries `delta = (p-1)(p-2)/6 = Theta(|F|)` distinct
MCA-bad slopes -- `delta > |F|^{1/2}` for all `p >= 11` -- because the `binom(N,2)`
collision loci are cleared by one structured pole. So T-LAW's tightness
`delta = Theta(|F_r|)` holds already at `[F_r:B] = 2` (a polynomial extension),
not only on the exponential countertheorem field, and no per-line `|F|^{1/2}` cap
exists. The refutation is **harmless for the prize** -- these witnesses are
polynomial-field, hence subexponential `delta` and `#645` column 1 -- but it
**closes off** the biggest-prize route that would have made `(FI-field')`
derivable from a quadratic gate. In the exponential regime the countertheorem
**saturates** `delta = |F|^{1/2}` (diluted), and whether `delta` can reach `~|F|`
(prize-relevant) is the unchanged open corner of `#645`. Action: keep
`(FI-field')` printed as a field condition in `def:admissible-sequence` (per
`#645`); annotate eq (4.5) that its `binom(N,2)` cost is a sufficient generic-
position bound, loose by `~N` for structured fibers; do **not** attempt a
per-line `|F|^{1/2}` sharpening -- it is refuted.*

### What does NOT close (unchanged from #645)

```
 unconditional span-face closure via a per-line |F|^{1/2} cap --REFUTED--> DEAD
   (explicit Theta(|F|) collapse line; c reaches 1, not 1/2)
 (FI-field') derivable from admissibility alone            --STILL OPEN/NO-->
   remains a genuine printed field condition (#645 placement stands)
```
