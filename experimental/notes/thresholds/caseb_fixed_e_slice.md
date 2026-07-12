# The Case-B slope map equidistributes on the fixed-e slice: a theorem, and the exact e-degradation that keeps growing-e open

## Status

`FIXED-e THEOREM (PROVED, explicit constant): for fixed extension degree e and
depth w=0, the deep-fiber slope map S|->prod_{x in S}(alpha-x) over F=F_{q^e}
(q=|B|->infinity) covers a POSITIVE CONSTANT fraction c_e=1/(2+K(e,m)) of F once
|G|>=|F|, with K(e,m)=m! sum_{t=e+1}^m (e-1)^{2t}/((t!)^2(m-t)!) EXPLICIT / the
proof is an EXACT second-moment reduction delta>=|G|^2/E + the injective-on-close
vanishing W(t)=0 (t<=e) + the affine-B-line Weil bound |S(chi)|<=(e-1)sqrt q
(PROVED for norm-characters via N(alpha-x)=(-1)^e mu(x); CITED+VERIFIED for all
chi) / W3 DEGRADATION (COMPUTED): c_e degrades super-exponentially in e
(c_e ~ (e+1)!/(e-1)^{2(e+1)} at m=e+1, below eps=2^-128 at e=23) and
stretched-exponentially in m (~exp(-2(e-1)sqrt m)); the moment constant is
deg(mu)^{2m}=e^{2m}, NON-UNIFORM once e or m grows with n -- exactly why
e=Theta(n/log q) is out of reach / IRREDUCIBILITY: NOT NEEDED (the character-sum
route uses only a 1-parameter line sum; the high-dimensional Lang-Weil
irreducibility obstruction of #652 Rung A2 is SIDESTEPPED) / CENSUS (MEASURED):
#652's e=3 w=0 cells reproduced BYTE-EXACT (441,1352,4907); provable c_e is a
valid but pessimistic lower bound on the measured eta=0.76-1.0 (gap x2 at e=2 to
x2e4 at e=5 -- the standard worst-case-character slack)`.

**One-line verdict (PROVED on the fixed-e slice; the wall is the constant's
non-uniformity).** *The census invariance measured by our **#652** -- the
Case-B Vandermonde slope map's coverage is `e`-flat at fixed `rho` -- becomes a
**theorem** the moment `e` is held fixed. For a fixed extension degree `e`, fixed
agreement `m>e`, base field `B=D=F_q`, ambient `F=F_{q^e}`, and the depth-`w=0`
fiber `G` = all `m`-subsets, the slope map `S |-> Q_S(alpha)=prod_{x in S}(alpha-x)`
(the exact map of #647/#652, in its "products of an affine `B`-line" reading)
satisfies, as `q -> infinity`,*
```
        delta = #image  >=  min(|G|, |F|-1) / (2 + K(e,m)),
        K(e,m) = m! * sum_{t=e+1}^{m} (e-1)^{2t} / ( (t!)^2 (m-t)! ),
```
*so once `|G| >= |F|` the image covers the **positive constant fraction**
`c_e = 1/(2+K(e,m))` of `F` -- the measured `eta in [0.76,1]` is now a proved
`eta >= c_e > 0`. The proof is an **exact** second-moment reduction (`delta >=
|G|^2/E` with `E` the collision count), the **exact** combinatorial decomposition
`E = |G| + sum_{t>=e+1} W(t) binom(q-2t,m-t)` with the **injective-on-close**
vanishing `W(t)=0` for `t<=e` (our #652), and a single **complete character sum
over an affine `B`-line**, `S(chi)=sum_{x in F_q} chi(alpha-x)`, controlled by
the Weil bound `|S(chi)| <= (e-1)sqrt q` -- **proved outright for norm-characters**
via the identity `N_{F/B}(alpha-x)=(-1)^e mu(x)` (`mu` = minimal polynomial of the
pole) plus Weil for `sum_x chi'(mu(x))`, and cited+verified for the rest. Because
the phase lives on a **one-parameter line** (dimension `1`, degree `e`), the
high-dimensional irreducibility obstruction that #652 flagged as OPEN (Rung A2,
"the variety's dimension grows with `n`, Weil constant `exp(Theta(n))`") is
**not encountered here**. The price is a **pessimistic** constant: `c_e` is a
rigorous lower bound well below the measured `eta` (the usual worst-case-character
slack). The **decisive W3 payload** is the constant's `e`-dependence, computed
exactly: `c_e` degrades **super-exponentially** in `e` (at the minimal fiber
`m=e+1`, `K = (e-1)^{2(e+1)}/(e+1)!`, so `c_e` falls below the prize threshold
`eps=2^{-128}` at `e=23`) and **stretched-exponentially** in `m`
(`~ exp(-2(e-1)sqrt m)`); the moment's implied constant is `deg(mu)^{2m}=e^{2m}`,
which is a genuine constant for each fixed `(e,m)` but is **not uniform** once
`e` or `m` grows with `n`. That non-uniformity -- not a failure of pointwise Weil
(which stays valid while `e < sqrt q`) -- is the exact reason the deep
`e=Theta(n/log q)` regime is open: the bounded-dimension method proves the law for
every fixed slice and quantifies precisely how fast its guarantee evaporates as
the slice deepens.*

Every number below is recomputed by
`experimental/scripts/verify_caseb_fixed_e_slice.py` (stdlib-only, zero-arg,
`RESULT: PASS (132/132)`, ~12 s, well under `ulimit -v 2097152`).

Label key: **PROVED** (complete re-derivable hand proof, exact), **COMPUTED**
(exact finite recomputation of a derived quantity), **MEASURED** (exact finite
census; the asymptotics are *not* proved from the toy), **AUDIT** (verbatim
reading of a cited source / a use of a cited theorem stated with explicit
constant), **OPEN**.

**Credit.** The object -- the Case-B collapse-cell slope map, its "products of an
affine `B`-line" and "reductions mod `mu`" readings, and the `e<=k` low-degree-pole
setup `|F|=|B|^e` -- is our **#647** (`collapse_field_cost.md`, read first: the
Case-A/Case-B dichotomy and the explicit statement that Case B at `e=Theta(n/log q)`
"is an equidistribution question we do not settle"). The **census invariance** we
upgrade (`delta = min(|G|,|F|)*eta`, `eta in [0.76,1]`, coverage `e`-flat at fixed
`rho`, 14 exact `GF(p^e)` cells) and the **injective-on-close lemma** (`|S triangle
S'|<=2e => S=S'`, giving `W(t)=0` for `t<=e`) are our **#652**
(`caseb_equidistribution.md`), which also isolated the residual as a
growing-dimension character sum with uncontrolled Weil constant (its Rung A2, the
OPEN link we localize here). The prize normalization `e_MCA(r)=delta/|F|` and the
reduction of prize-relevance to the ambient field are our **#645**
(`fi_field_discharge.md`). The field-of-definition law `delta<=|F_r|` (T-FIELD) and
the `GF(p^d)` census machinery are our **#642** (`c7_collapse_image_degree.md`).
The pole-to-slope fiber form `delta=#{Q_S(alpha)}` and the separation gate are the
paper's own (`thm:exact-list-line-bijection`, `thm:prefix-to-line-hardness`);
subfield confinement (`thm:subfield-confinement-full`) is the paper's. **Weil's
theorem** for one-variable multiplicative character sums (the bound `(e-1)sqrt q`
for `sum_{x in F_q} chi'(mu(x))`, `mu` squarefree of degree `e`) is used with its
**explicit** constant and is cited, not re-proved (standard; e.g. Weil 1948; Lidl-
Niederreiter, *Finite Fields*, Thm. 5.41); its extension to the general affine-line
sum `S(chi)` is cited and **verified** exactly on every reachable `(q,e)`. No
finite M31/KoalaBear survivor count, adjacent inequality, or target threshold is
touched. Codex/Danny orientation-cell and pole-transport machinery are not used
(single-fiber projection question), cited only through #642/#645/#647.

---

## HEADLINE (read first): fixing e turns the measured invariance into a proved constant

`#652` **measured**, over 14 exact `GF(p^e)` cells (`e<=4`), that the collapse-cell
slope map is generic -- `delta = eta * min(|G|,|F|)` with `eta in [0.76,1]`, and
crucially **coverage is invariant under `e` at matched `rho=|G|/|F|`** -- and left
the asymptotic proof OPEN because *at growing `e` the parametrizing variety has
dimension `Theta(n)` and the Weil/Deligne implied constant is `exp(Theta(n))`,
uncontrolled*. This packet proves the law on the slice `#652` did **not** claim:
**`e` fixed**. There the variety is bounded, and -- better -- the whole question
collapses onto a **one-parameter** complete character sum, so the constant is
genuinely controlled.

The exact map (extracted from #647 Rung 3 / #652 headline). Base `B=D=F_q`, pole
`alpha` of degree `e=[B(alpha):B]`, ambient `F=B^e`. On the depth-`w=0` fiber
`G = binom(F_q, m)` (all `m`-subsets), after dropping the fiber-common shift, the
received-line MCA-bad slope is
```
   Q_S(alpha) = prod_{x in S} (alpha - x)  in  F^*        (0 is never a slope, #652),
```
a product of an `m`-subset of the `q` points `V = alpha - F_q` on the **affine
`B`-line** `alpha + B subseteq F`. Write `delta = #{Q_S(alpha) : S in G}`. Case B
is `e <= k=m-1`: the image lies in `F` and `delta <= min(|G|,|F|)`.

**Theorem (fixed-e coverage, PROVED).** *Fix `e>=2` and `m>e`. For every prime
power `q`, with `G=binom(F_q,m)`, `|G|=binom(q,m)`, `|F|=q^e`,*
```
   delta  >=  |G|^2 / E_UB(q,e,m),                                            (THM)
   E_UB = |G| + sum_{t=e+1}^{m} [ q^{2t}/(q^e-1) + (e-1)^{2t} q^t ] / (t!)^2
                                 * binom(q-2t, m-t),
```
*and hence, letting `q -> infinity` at fixed `(e,m)`,*
```
   delta  >=  min(|G|, |F|-1) / (2 + K(e,m)) * (1 - o(1)),
   K(e,m) = m! * sum_{t=e+1}^{m} (e-1)^{2t} / ( (t!)^2 (m-t)! ).              (c_e)
```
*In particular, once `|G| >= |F|` the image covers the constant fraction
`c_e = 1/(2+K(e,m))` of `F`.* The four pillars, each rigorous:

1. **Cauchy-Schwarz (PROVED).** `delta >= |G|^2/E`, `E =` #collisions.
2. **Exact decomposition + injective-on-close (PROVED).** `E = |G| + sum_{t>=e+1}
   W(t) binom(q-2t,m-t)`; `W(t)=0` for `t<=e` (#652).
3. **Affine-line Weil linchpin (PROVED norm-chars / CITED+VERIFIED general).**
   `W(t) <= M(t)/(t!)^2`, `M(t)=(|F|-1)^{-1} sum_chi |S(chi)|^{2t}`,
   `S(chi)=sum_{x in F_q} chi(alpha-x)`, `|S(chi_0)|=q`, `|S(chi)|<=(e-1)sqrt q`.
4. **Assembly + `q->infty` (PROVED).** Gives `(THM)`, then `(c_e)`.

---

## Rung 1 -- the exact second-moment reduction (PROVED)

For `y in F^*` let `N(y)=#{S in G : Q_S(alpha)=y}`. Since the image is in `F^*`
(0 never a slope, #652), `sum_{y in F^*} N(y)=|G|` and `delta = #{y:N(y)>0}`. By
Cauchy-Schwarz,
```
   |G|^2 = ( sum_{y:N(y)>0} N(y) )^2  <=  delta * sum_y N(y)^2  =  delta * E,   (1)
```
where `E = sum_{y} N(y)^2 = #{(S,S') in G^2 : Q_S(alpha)=Q_{S'}(alpha)}`. So
`delta >= |G|^2/E`. **To lower-bound `delta` we upper-bound the collision count
`E`.** [verify BLOCK 2: `delta >= |G|^2/E` on 8 cells, all exact.]

**Exact collision decomposition.** For a pair `(S,S')` set `C=S cap S'`,
`A=S setminus S'`, `B'=S' setminus S`, so `A,B',C` are disjoint,
`|A|=|B'|=t`, `|C|=m-t`. Then `Q_S=Q_{S'}` iff `prod_C * prod_A = prod_C * prod_{B'}`
iff `prod_A(alpha-a)=prod_{B'}(alpha-b)` (cancel `prod_C != 0`). Choosing first
the disjoint pair `(A,B')` then the core `C subseteq F_q setminus (A cup B')`,
```
   E = sum_{t=0}^{m} W(t) * binom(q-2t, m-t),                                  (2)
   W(t) = #{ (A,B') : A,B' subseteq F_q disjoint, |A|=|B'|=t,
                      prod_{a in A}(alpha-a)=prod_{b in B'}(alpha-b) }.
```
`W(0)=1` gives the `t=0` term `binom(q,m)=|G|` (the true diagonal `S=S'`).
[verify BLOCK 2: `E` from `(2)` equals `E` from `N(y)` on every cell, exact.]

**Injective-on-close vanishing (our #652, PROVED).** If `1<=t<=e` then `W(t)=0`.
*Proof (recalled).* `prod_A(alpha-a)=prod_{B'}(alpha-b)` with `A,B'` disjoint of
size `t` gives `prod_{a in A}(X-a) - prod_{b in B'}(X-b)`, monic of degree `t` with
leading terms cancelling, a polynomial over `B` of degree `<= t-1 < e` vanishing at
`alpha`; since `[B(alpha):B]=e` it is identically zero, so the two monic
polynomials coincide, forcing `A=B'`, contradicting disjointness unless empty.
`QED` Hence
```
   E = |G| + sum_{t=e+1}^{m} W(t) * binom(q-2t, m-t).                          (3)
```
[verify BLOCK 2: `W(t)=0` for `1<=t<=e` and the first nonzero at `t=e+1`, e.g.
`(p,e,m)=(13,2,6)` gives `W=[1,0,0,290,452,424,96]`, `(11,3,5)` gives
`W=[1,0,0,0,14,0]`.]

---

## Rung 2 -- the affine-`B`-line character sum: fixed `e` gives a controlled Weil bound (PROVED / CITED+VERIFIED)

The task's route W1 proposed bounding a **variety** point count by Lang-Weil,
which needs geometric irreducibility of a variety whose dimension is `2m`. We
avoid it: the second moment collapses to a **one-parameter** complete sum.

**Ordered relaxation (PROVED).** Every disjoint pair `(A,B')` of distinct-element
`t`-subsets with equal product yields exactly `(t!)^2` ordered tuples
`(a,b) in F_q^t x F_q^t` with `prod_i(alpha-a_i)=prod_j(alpha-b_j)`, all distinct,
and distinct pairs give disjoint tuple-sets. Hence
```
   W(t) <= M(t)/(t!)^2,   M(t) = #{ (a,b) in F_q^t x F_q^t :
                                    prod_i(alpha-a_i)=prod_j(alpha-b_j) }.       (4)
```

**Character expansion (PROVED).** All products lie in `F^*`. By orthogonality of
the `q^e-1` multiplicative characters of `F^*`, and since
`sum_{a in F_q^t} prod_i chi(alpha-a_i) = ( sum_{x in F_q} chi(alpha-x) )^t
= S(chi)^t`,
```
   M(t) = (q^e-1)^{-1} sum_{chi} |S(chi)|^{2t},   S(chi)=sum_{x in F_q} chi(alpha-x). (5)
```
[verify BLOCK 2: `(5)` holds exactly on `(p,e,t)` in `{(5,2,2),(7,2,2),(5,2,3),
(7,3,2)}` against a direct tuple count; and `W(t)<=M(t)/(t!)^2`.]

**The linchpin: `|S(chi)| <= (e-1)sqrt q` for `chi != chi_0`.** `S(chi_0)=q` (all
`alpha-x != 0`). For the nonprincipal bound:

- **Norm-characters (PROVED, self-contained).** Let `mu` be the minimal polynomial
  of `alpha` over `B` (monic, degree `e`, `e` distinct roots = the conjugates
  `alpha^{q^i}`). For `x in F_q`,
  ```
     N_{F/B}(alpha-x) = prod_{i=0}^{e-1}(alpha-x)^{q^i}
                      = prod_i (alpha^{q^i}-x) = (-1)^e mu(x).                   (6)
  ```
  So if `chi = chi' o N_{F/B}` for a nontrivial character `chi'` of `B^*`, then
  `S(chi) = chi'((-1)^e) sum_{x in F_q} chi'(mu(x))`, and **Weil's bound** for the
  multiplicative character sum of a squarefree degree-`e` polynomial gives
  `|sum_x chi'(mu(x))| <= (e-1)sqrt q`. [verify BLOCK 1a: `(6)` exact on 5 cells;
  BLOCK 1b: the resulting bound.]
- **General characters (CITED + VERIFIED, explicit constant).** For an arbitrary
  nontrivial `chi`, `S(chi)` is a multiplicative character sum along the affine
  `B`-line `L = alpha - F_q subseteq F`. Its Weil bound `|S(chi)| <= (e-1)sqrt q`
  is standard for a **fixed** `e` (a bounded-genus one-parameter family; the
  branch data is the degree-`e` set of conjugates of `alpha`), and we invoke it
  with the **explicit** constant `e-1`. We do not re-derive it; we **verify it
  exactly** on every reachable `(q,e)`. [verify BLOCK 1b: `max_{chi != chi_0}
  |S(chi)| <= (e-1)sqrt q` for all `(p,e)`, `e<=4`; the ratio `|S|/sqrt q` is
  **exactly `1=e-1`** at `e=2` and rises toward `e-1` (`1.97` at `e=3`, `2.54` at
  `e=4`) -- the constant is tight, not conservative. BLOCK 1c: the `L2` identity
  `sum_chi|S(chi)|^2=(q^e-1)q` holds exactly.]

**Assembled bound on `M(t)` (PROVED given the linchpin).** From `(5)`,
```
   M(t) <= (q^e-1)^{-1}[ q^{2t} + (q^e-2)((e-1)sqrt q)^{2t} ]
        <= q^{2t}/(q^e-1) + (e-1)^{2t} q^t.                                     (7)
```

**Why irreducibility is not needed.** The only geometric input is the degree of
`mu` (the branch data of the **line** sum), namely `e`. There is no
high-dimensional variety and no irreducibility hypothesis: the `2m`-dimensional
collision variety of #652's Rung A2 is replaced, via `(4)-(5)`, by the tensor
power `S(chi)^t` of a single line sum. This is the structural reason the fixed-`e`
slice is provable where the growing-`e` law is not.

---

## Rung 3 -- assembling the theorem and the explicit constant (PROVED)

Insert `(7)` and `W(t)<=M(t)/(t!)^2` into `(3)`:
```
   E <= E_UB = |G| + sum_{t=e+1}^{m} [q^{2t}/(q^e-1)+(e-1)^{2t}q^t]/(t!)^2
                                     * binom(q-2t,m-t),                          (8)
```
and `(1)` gives `(THM)`: `delta >= |G|^2/E_UB`. [verify BLOCK 3: `delta_meas >=
|G|^2/E_UB` on the #652 cells and a `(p,e,m)` grid, all satisfied.]

**The `q->infty` reading (PROVED).** With `binom(q-2t,m-t) = (1+o(1))q^{m-t}/(m-t)!`
and `|G|=(1+o(1))q^m/m!`, the `t`-sum in `(8)` splits into a **main** part (from
`q^{2t}/(q^e-1)`, dominated by `t=m`, contributing `(1+o(1))|G|^2/(|F|-1)` -- the
generic birthday collision rate `~|G|^2/|F|`) and an **excess** part (from
`(e-1)^{2t}q^t`, contributing `(1+o(1))|G|*K(e,m)`). Hence
```
   E <= (1+o(1)) [ |G|*(1+K(e,m)) + |G|^2/(|F|-1) ].                            (9)
```
Then `delta >= |G|^2/E >= |G| / [ (1+K) + |G|/(|F|-1) ] (1-o(1))`. If `|G|<=|F|-1`
this is `>= |G|/(2+K)`; if `|G|>=|F|-1` it is `>= (|F|-1)/(2+K)`. Unified:
```
   delta >= min(|G|,|F|-1)/(2+K(e,m)) * (1-o(1)),   c_e := 1/(2+K(e,m)).        (c_e)
```
[verify BLOCK 4: `K(e,m)` closed form; `eta_prov=c_e` is `<= eta_meas` on every
cell -- a valid (pessimistic) lower bound on the measured fill.]

Sample constants (`q->infty`):
```
   (e,m) | K(e,m)     | c_e = 1/(2+K)
   (2,3) |  0.1667    | 0.4615
   (2,4) |  0.7083    | 0.3692
   (2,5) |  1.8833    | 0.2575
   (3,4) | 10.6667    | 0.0789
   (3,5) | 61.8667    | 0.0157
   (4,5) | 492.075    | 0.00202
   (5,6) | 23301.69   | 0.0000429
```

---

## Rung 4 -- W3: the exact degradation, and where the bounded-dimension method stops (COMPUTED)

### AMENDMENT (hybrid lower bound; correction due to the Codex team's post-#665 reconciliation audit)

Integrated #652's route A1 (the B-linear projection bound `delta >= |G|/q^{k+1-e}`)
already applies verbatim in this packet's setup (`D=B=F_q`, `w=0`, `k=m-1`,
`e<=k`), giving `delta >= C(q,m)/q^{m-e}`, i.e. coverage `delta/|F| >= C(q,m)/q^m
-> 1/m!` as `q -> infinity`. The correct fixed-slice statement is therefore the
HYBRID

```text
   liminf delta/q^e  >=  max{ 1/m!,  1/(2 + K(e,m)) },
```

with the moment constant winning at `e in {2,3}` (0.462, 0.079 vs 1/6, 1/24)
and the linear-projection term winning for every `e >= 4` at minimal `m=e+1`
(e=4: 1/120 = 8.3e-3 vs 2.0e-3). CONSEQUENCE FOR RUNG 4: the prize-threshold
crossover of the best proved constant moves from `e = 23` (moment-only, as
printed below) to **`e = 34`** (`1/(e+1)! < 2^{-128}` first at `e = 34`);
the degradation is now factorial rather than super-exponential, and the
qualitative verdict — the growing-e law needs constants that do not degrade
in `e`, hence stays OPEN — is UNCHANGED. Every `e=23` statement below should
be read with this amendment. (Verifier BLOCK A9, added with this amendment,
recomputes the hybrid table and both crossovers.)


The theorem holds for **every** fixed `(e,m)`, but `c_e` is **not uniform** in the
slice depth. We compute the degradation exactly -- this is the packet's steering
payload for the growing-`e` wall.

**Degradation in `e` (minimal fiber `m=e+1`).** Only the `t=e+1` term survives:
```
   K(e,e+1) = (e-1)^{2(e+1)} / (e+1)!,   c_e = 1/(2 + (e-1)^{2(e+1)}/(e+1)!).   (10)
```
By Stirling this is `c_e = e^{-(2+o(1)) e log e}`: **super-exponential** decay.
Numerically `c_e` crosses the prize threshold `eps=2^{-128}` at **`e=23`**:
```
   e   K(e,e+1)     c_e         log2(c_e)
   2   1.67e-01     4.62e-01     -1.1
   4   4.92e+02     2.02e-03     -8.9
   8   4.49e+09     2.23e-10    -32.1
  16   2.73e+25     3.66e-26    -84.5
  22   2.57e+38     3.89e-39   -127.6      (still > eps)
  23   4.40e+40     2.27e-41   -135.0      (< eps = 2^-128)
```
So the bounded-dimension method certifies a **prize-relevant** coverage
(`c_e > eps`) only for `e <= 22` with this constant, and `log2(1/c_e)` is convex in
`e` (super-exponential). [verify BLOCK 5: `(10)` exact for `e<=5`; first `e` with
`c_e<eps` is `23`; convexity of `log2(1/c_e)`.]

**Degradation in `m` (fixed `e`, deep fiber).** `K(e,m) = sum_t binom(m,t)
(e-1)^{2t}/t!` has its mass at `t ~ (e-1)sqrt m` and is bounded by the Bessel
envelope `~ exp(2(e-1)sqrt m)`, so
```
   c_{e,m} >~ exp(-2(e-1)sqrt m):  STRETCHED-exponential in sqrt(m).           (11)
```
For the prize's deep fiber `m=Theta(n)` this is `exp(-Theta(sqrt n))` (fixed `e`).
[verify BLOCK 5: `K(3,m) < exp(4 sqrt m)` for `m in {6,12,24,48}`.]

**The exact boundary of the method (the answer to "where does bounded-dim stop").**
Two distinct thresholds, both computed:

- **Pointwise Weil validity.** `|S(chi)| <= (e-1)sqrt q` is informative only when
  `(e-1)sqrt q < q`, i.e. `q > (e-1)^2`. So the *pointwise* input survives while
  `e < sqrt q + 1`. In the prize's poly-field regime (`q=n^C`, `C>=2`,
  `e=Theta(n/log q)~n/(C log n)`) one has `e < n < n^{C/2}=sqrt q`, so pointwise
  Weil is **not** the bottleneck. [verify BLOCK 5: `q>(e-1)^2` boundary.]
- **Moment-constant uniformity (the real wall).** The excess constant in `(9)` is
  `deg(mu)^{2m}=e^{2m}` accumulated over the `2t`-th moment; even with every
  pointwise bound valid, this is `exp(Theta(e log e))` in `e` at `m=e+1` and
  `exp(Theta((e-1)sqrt m))` in `m`. It is a genuine constant for each **fixed**
  `(e,m)` but **diverges** once `e` or `m` grows with `n`. This is exactly #652's
  "the Weil constant is a Betti/degree product over an unbounded dimension" made
  quantitative: the dimension here is the **moment order** `2m` (and the degree is
  `e`), and the census sees `eta ~ 0.76` flat precisely because the *typical*
  character is far below the worst case -- the gap the worst-case bound cannot
  close is the same gap that makes growing `e` open.

**Net (W3).** The bounded-dimension argument proves `delta >= c_e|F|` for every
fixed `(e,m)`; the guarantee `c_e` decays super-exponentially in `e` and
stretched-exponentially in `m`, crossing `eps` at `e=23` (`m=e+1`) and at
`m ~ (44/(e-1))^2` (deep fiber). To reach `e=Theta(n/log q)` one would need the
**typical** (not worst-case) character-sum behavior -- i.e. an averaged/`L4`-type
bound on `sum_chi|S(chi)|^{2t}` beating the trivial `(q^e-1)*max`, or a fibered
low-degree reformulation of the phase -- which is precisely the strengthening #652
identified as the open link.

---

## Rung 5 -- W4: census cross-check and the honest provable-vs-measured gap (MEASURED)

**Reproduction of #652.** Our independent `GF(p^e)` census reproduces #652's `w=0`
`e=3` cells **byte-exact**: `delta(11,3,5)=441`, `delta(13,3,6)=1352`,
`delta(17,3,8)=4907`. [verify BLOCK 6.] At **`e=4`** the exact `delta` is mildly
**pole-class dependent** (non-conjugate degree-`4` poles differ): our correct pole
gives `delta(17,4,8)=22445` and `delta(19,4,9)=70986`, within `<0.7%` of #652's
cited `22341, 70521` (a different, equally valid degree-`4` pole). Coverage is
**pole-shift invariant** (`alpha -> alpha+3` leaves `delta` unchanged) at every
`e`, so the `eta` story is robust; only the last-digit integer is pole-sensitive
at composite `e` -- a minor new finding. [verify BLOCK 6.]

**The gap.** `c_e` (provable) is a rigorous lower bound **well below** the measured
`eta` (the truth), and the gap **widens with `(e,m)`** -- the standard slack
between a worst-case-per-character bound and actual equidistribution:
```
    p  e  m |   |G|    |F| | delta | eta_meas  c_e(prov)  gap
    7  2  3 |    35     49 |    32 | 0.9143    0.4615      x2.0
   13  2  5 |  1287    169 |   168 | 0.9941    0.2575      x3.9
    7  3  4 |    35    343 |    35 | 1.0000    0.0789     x12.7
    7  3  5 |    21    343 |    21 | 1.0000    0.0157     x63.9
   11  5  6 |   462 161051 |   462 | 1.0000    0.0000  x23303.7
```
[verify BLOCK 6: `c_e <= eta_meas` on the extended census, `e in {2,3,4,5}`.] The
gap is not a defect of the theorem (which only claims a positive constant) but a
quantitative statement of how much the worst-case character bound over-charges --
and, per Rung 4, it is the same quantity whose growth blocks the deep regime.

---

## Rung V -- VERDICT and closure impact

**VERDICT = the fixed-e slice is PROVED; the open law is exactly the constant's
loss of uniformity.**

- **Fixed `(e,m)`, `q->infty`: PROVED.** `delta >= min(|G|,|F|-1)/(2+K(e,m))`, an
  explicit positive constant; once `|G|>=|F|` the image covers `c_e=1/(2+K(e,m))`
  of `F`. The measured `eta in [0.76,1]` of #652 is now `eta >= c_e > 0`, a
  theorem. This is the slice on which "bounded-dimension Weil genuinely applies
  with controlled constants" -- and we exhibit the control.
- **Growing `e` (or growing `m`): OPEN, quantified.** `c_{e,m}` degrades
  `super-exp` in `e` and `stretched-exp` in `m`; the method's constant is
  `deg(mu)^{2m}=e^{2m}`, uniform in neither. The prize's `e=Theta(n/log q)` (deep
  fiber `m=Theta(n)`) sits strictly beyond the crossover, so this route -- while
  proving every fixed slice -- cannot reach it. Closing it needs a
  typical-character (`L4`/averaged) bound or a low-degree phase reformulation, the
  exact strengthening #652 named.

**Closure impact (#650/#645).** The census's "construction-pointing" reading is now
**partially discharged**: on any fixed-`e` scalar extension the Case-B collapse
cell **does** realize `delta = Theta(|F|)` (a positive constant fraction), so
`(FI-field')` is genuinely load-bearing there and **cannot** be weakened to a
free `|F|^{1/2}` bound at fixed `e` -- confirming #647's refutation asymptotically
for every fixed `e`, not just the `m=3` witness. The prize-relevant verdict for
the deep `e=Theta(n)` regime remains OPEN and is now pinned to a single,
quantified analytic deficiency (worst-case vs. typical character sums), sharpening
#652's OPEN link.

---

## The 2-3 least-certain steps (for the PI)

1. **The general-character Weil bound `|S(chi)| <= (e-1)sqrt q` (Rung 2).** Proved
   here **only** for norm-characters (via `(6)`, self-contained). For the
   remaining characters it is invoked as the standard one-parameter Weil bound for
   a fixed-`e` line sum, with the **explicit** constant `e-1`, and **verified
   exactly** on every reachable `(q,e)` (ratio `-> e-1`, tight). A fully
   self-contained proof for all `chi` (the `L`-function of the line sum has degree
   `e` in the relevant cohomology) is standard but not written out; if one distrusts
   the citation, the verifier's exact check on `e<=4` and the norm-character proof
   are the fallback evidence.
2. **The `q->infty` passage `(8)->(9)->(c_e)` (Rung 3).** The split into main and
   excess terms uses `binom(q-2t,m-t)=(1+o(1))q^{m-t}/(m-t)!`, exact as `q->infty`
   at **fixed** `(e,m)`. The finite inequality `(THM)` `delta>=|G|^2/E_UB` is
   verified directly (no asymptotics) on the cells; the constant `c_e` is the
   clean limit. For small `q` near `(e-1)^2` the finite bound can be vacuous
   (`<1`) -- the positive constant is an asymptotic statement in `q`, as the
   verifier's cell table makes explicit.
3. **The degradation exponents (Rung 4).** `K(e,e+1)=(e-1)^{2(e+1)}/(e+1)!`
   (exact, one term) and the `e=23` crossover are exact. The `m`-degradation
   `~exp(-2(e-1)sqrt m)` is the Bessel envelope of `K(e,m)` (verified as an upper
   envelope, `K(3,m)<exp(4sqrt m)`); the precise deep-fiber crossover
   `m~(44/(e-1))^2` uses this envelope and is an order-of-magnitude statement, not
   an exact threshold.

---

## Reproducibility

```
$ ulimit -v 2097152
$ python3 experimental/scripts/verify_caseb_fixed_e_slice.py
... RESULT: PASS (132/132)      (~12 s)
```

The script is stdlib-only and zero-arg. It builds exact `GF(p^e)` (Rabin
irreducibility, discrete-log tables), verifies the norm identity `(6)` and the
linchpin `|S(chi)|<=(e-1)sqrt q` (over all characters) and the `L2`/`M(t)`
character identities, recomputes the exact second-moment reduction `(1)`, the
collision decomposition `(2)-(3)` with `W(t)=0` for `t<=e`, the provable bound
`(THM)` against measured `delta`, the explicit constant `K(e,m)` and `c_e`, the
W3 degradation (`e`-crossover at `23`, `m`-envelope, the `q>(e-1)^2` boundary),
and reproduces #652's `e=3` `w=0` census byte-exact plus the pole-shift
invariance and the provable-vs-measured gap. `BLOCK n` tags map one-to-one to the
`verify BLOCK n` citations above; it exits nonzero on any mismatch.
