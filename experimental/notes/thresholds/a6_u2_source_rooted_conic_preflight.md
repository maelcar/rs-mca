# Source-rooted conic and collision preflight for the A6 `U_(2,5)` atom

- **Status:** experimental audit packet.  The algebraic statements below
  are proved under their literal hypotheses.  Nothing is proposed for TeX.
- **Object:** one fixed actual completed-witness selector on one weighted-RS
  syndrome line, after any already-declared first-match deletion.
- **Purpose:** separate the hereditarily conic/simple-pole branch, which is
  polynomially paid, from the sole remaining nonzero collision-determinant
  branch.  The latter is localized but not paid here.
- **Nonclaims:** no primitive atlas, quotient classification, planted-profile
  census, ray-occupancy theorem, full A6/A7 theorem, deployed-row result, or
  prize closure.  No literature novelty is asserted.

## 1. Literal weighted-RS setup

Let `F` be a field, let `U subset F` contain `N` distinct elements, and let
`omega_x != 0` for every `x in U`.  Put

```text
P=P_<kappa={f in F[X]:deg f<kappa},
K={ (omega_x f(x))_(x in U): f in P },
R=N-kappa,
```

where `1<=kappa<N`.  Fix actual vectors `y,v in F^U`.  Define the source
direction distance

```text
d=min_(f in P) wt(v+omega*ev_U(f)).                       (1.1)
```

Fix `0<=t<d`, a retained set `Z` of distinct slopes, and one actual selected
witness at each retained slope:

```text
c_gamma=y+gamma v+omega*ev_U(f_gamma),
f_gamma in P,
wt(c_gamma)<=t.                                           (1.2)
```

Let `T_gamma={x:c_gamma(x)=0}` and `S_gamma=U\T_gamma`.
The selected objects in (1.2), not replacement null tuples, are used
throughout.

To make polynomial divisors literal, let `Y,V in F[X]_<N` be the unique
interpolants of the functions `x |-> y(x)/omega_x` and
`x |-> v(x)/omega_x` on `U`, and put

```text
C_gamma(X)=Y(X)+gamma V(X)+f_gamma(X).                    (1.3)
```

Then `C_gamma(x)=c_gamma(x)/omega_x` on `U`, so every `x in T_gamma` is a
literal root of `C_gamma`.  The polynomial may have other roots outside `U`;
none are counted.

For `|Z|>=2`, fix `gamma_0 in Z` and put

```text
D_Z=span_F{c_gamma-c_(gamma_0):gamma in Z},
s=dim D_Z,
r=dim(D_Z intersect K).                                  (1.4)
```

The strict source hypothesis `t<d` implies `d>0`, hence
`V notin P_<kappa` (equivalently the direction syndrome is nonzero).
The syndrome image of `D_Z` is one-dimensional, so `r=s-1`.  Statements
that use this translation say so explicitly; the determinant identities
themselves need only the displayed polynomial hypotheses.

All statements are deletion-monotone: deleting slopes leaves the same actual
polynomials, masks, and source line on every surviving subfamily.

**Hypothesis ledger.**  The field may have any characteristic, including two
or three.  The domain points and retained slopes are distinct; `1<=kappa<N`;
`Y,V` are the canonical degree-`<N` interpolants; and every selected
`f_gamma` has degree `<kappa`.  No squarefree or reduced-root hypothesis on
`Delta` is used: (3.2) is a genuine multiplicity statement at distinct
domain points.  Only the ambient RS-distance and shortening claims add
`2kappa-1<=N`.

## 2. The symmetric direct-quartic invariant

Choose five distinct retained slopes `gamma_1,...,gamma_5`.  Write

```text
S_1=sum_i gamma_i,
S_2=sum_(i<j) gamma_i gamma_j,
V_i=product_(j!=i)(gamma_i-gamma_j).                      (2.1)
```

Lagrange-interpolate the five actual approximants in a slope variable `Z`:

```text
F(X,Z)=sum_i f_i(X) product_(j!=i)(Z-gamma_j)/V_i
      =g_0(X)+g_1(X)Z+g_2(X)Z^2+g_3(X)Z^3+g_4(X)Z^4.     (2.2)
```

Every `g_j` has degree `<kappa`.  This is the symmetric direct-quartic
convention; no base-pair recentering changes `S_1` or `S_2`.  Define

```text
Delta=g_2 g_4-g_3^2-S_1 g_3 g_4-S_2 g_4^2.               (2.3)
```

### Theorem 2.1 (source-rooted conic identity)

In `F[X]`,

```text
Delta(X)
 =sum_(i<j) ((gamma_i-gamma_j)^2/(V_i V_j)) C_i(X)C_j(X).
                                                                    (2.4)
```

Equivalently, with rows indexed in the chosen slope order,

```text
det [1, gamma_i, gamma_i^2, f_i, gamma_i f_i]_(i=1)^5
 =-product_(i<j)(gamma_j-gamma_i) Delta.                  (2.5)
```

#### Proof

Interpolating the normalized witness polynomials `C_i` instead of `f_i`
adds only `Y+VZ`; hence their coefficients of `Z^2,Z^3,Z^4` are the same
`g_2,g_3,g_4`.  Put

```text
P(a)=(a^2-S_1 a+S_2, a-S_1, 1),
Q(X_2,X_3,X_4)=X_2 X_4-X_3^2-S_1 X_3 X_4-S_2 X_4^2.
```

The nonlinear coefficient vector is

```text
(g_2,g_3,g_4)=sum_i (C_i/V_i) P(gamma_i).
```

Direct substitution gives `Q(P(a))=0`, and the polar pairing satisfies

```text
Q(P(a)+P(b))-Q(P(a))-Q(P(b))=(a-b)^2.
```

Expanding proves (2.4), in every characteristic.  Both sides of (2.5) are
alternating quadratic forms in the five values and vanish on the affine
`span{1,gamma}`; evaluation on one nonzero test gives the displayed minus
sign.  Equivalently, Lagrange expansion proves it coefficientwise.

## 3. Exact divisor, support, and common-GCD consequences

At a coordinate `x in U`, let `j(x)` be the number of the five selected
supports containing `x`, and let `n_j=#{x:j(x)=j}`.  Define the disjoint
exact strata

```text
P_0=product_(x:j(x)=0)(X-x),
P_i=product_(x in (intersection_(j!=i)T_j)\T_i)(X-x).
                                                                    (3.1)
```

Empty products are one.

### Corollary 3.1 (collision divisor)

```text
P_0^2 product_i P_i divides Delta,                        (3.2)

2n_0+n_1 >= 2N-sum_i wt(c_i).                            (3.3)
```

Moreover, `Delta(x)!=0` at every coordinate with exactly two selected
supports.  If `Delta!=0`, then its evaluation support is contained in
`{x:j(x)>=2}`.

#### Proof

If all five `C_i` vanish at `x`, every product in (2.4) has a double root.
If exactly one is nonzero, every product has at least one zero factor.  If
exactly two, (2.4) contains exactly one nonzero summand, whose scalar is
nonzero because the slopes are distinct.  Finally,

```text
sum_i wt(c_i)=sum_j j n_j
             >= n_1+2(N-n_0-n_1),
```

which is (3.3).

The RS-distance consequence requires the additional hypothesis
`2kappa-1<=N`.  Under it, a nonzero `Delta` has degree at most `2kappa-2`
and therefore

```text
wt(ev_U(Delta))>=N-2kappa+2=R-kappa+2.                   (3.4)
```

No distance claim is made from (3.4) when `2kappa-1>N`.

For a positive integer `u`, at the stress

```text
(N,R,kappa,t,d)=(500u,275u,225u,150u,250u),              (3.5)
```

In the nonzero-`Delta` branch, (3.2)--(3.4) give

```text
deg(P_0^2 product_i P_i)>=250u,
deg Delta<=450u-2,
wt(ev_U(Delta))>=50u+2.                                  (3.6)
```

Thus `Delta=(P_0^2 product_i P_i)H` with `deg H<=200u-2`.

There is also an exact four-locator common-GCD consequence.  Put

```text
h_i=|intersection_(j!=i) T_j|=n_0+n_(1,i),
```

where `n_(1,i)` counts coordinates whose unique supported witness is `i`.
Then

```text
sum_i h_i=5n_0+n_1>=2N-sum_i wt(c_i).                    (3.7)
```

At (3.5), some actual four-subfamily has a common locator root divisor of
degree at least `50u`.  This divisor is tuple-dependent.  Equation (3.7)
does not provide the subexponential profile census or moving-slope projection
required to call an arbitrary divisor a paid planted cell.

## 4. What `Delta=0` means for one five-tuple

If `g_4=0` and `Delta=0`, then `g_3=0`; the nonlinear approximants have
rank at most one.  Otherwise put

```text
rho=S_1+g_3/g_4 in F(X).                                  (4.1)
```

Then (2.3) is equivalent to

```text
[g_2:g_3:g_4]
 =[rho^2-S_1 rho+S_2:rho-S_1:1].                         (4.2)
```

If `P(Z)=product_i(Z-gamma_i)`, comparison of the three nonlinear
coefficients gives

```text
F(X,Z)=a(X)+b(X)Z
       +g_4(X) (P(Z)-P(rho(X)))/(Z-rho(X)).               (4.3)
```

Here `a,b in F(X)`; polynomiality is not asserted in the one-tuple
normal form.  Thus the five graph points lie on a
quadratic-over-linear/simple-pole curve over `F(X)`.  This is an algebraic
description, not by itself a quotient cell: `rho` need not be a finite
uniform folding map on `U`.

The support interpretation is exact.  At a coordinate where (4.2) is
defined, a singleton support of type `i` forces `rho(x)=gamma_i`.  Coordinates
with exactly two supports cannot occur when `Delta=0`.  If `H_3` is the set
of coordinates with at least three supports, summing the ten pair-union
bounds `|S_i union S_j|>=d` gives

```text
10d<=4n_1+10|H_3|.
```

Therefore either some marked fiber has at least `d/3` singleton coordinates
or `|H_3|>=d/3`.  At (3.5) this is `250u/3`.  A large rational-map fiber or
large coordinate-support concentration is still not automatically a paid
quotient or ray-saturation projection.

## 5. Hereditary conic vanishing is polynomially paid

### Theorem 5.1

Assume `|Z|=L>=5` and `Delta_I=0` for every five-subset `I subset Z`, with
`Delta_I` always defined by the symmetric convention (2.1)--(2.3).  Then
one of the following holds:

1. the intrinsic actual core in (1.4) has rank `r<=3`; or
2. `L<=4kappa-3`.

In the first case the completed-mask set-pair charge gives a polynomial
bound, for example `sum_(s=1)^4 binom(N,s)`.  Thus the entire hereditary
`Delta=0` branch is `N^O(1)`.

#### Proof

By (2.5), every `5x5` minor of the global matrix

```text
M_Z=[1,gamma,gamma^2,f_gamma,gamma f_gamma]_(gamma in Z)  (5.1)
```

vanishes over `F(X)`, so `rank M_Z<=4`.

If the rank is at most three, the first three columns are independent.
Thus `f_gamma=a+b gamma+c gamma^2`.  The fact that `gamma f_gamma` also
lies in `span{1,gamma,gamma^2}` on at least four distinct slopes forces
`c=0`; this is an affine pencil.

Now suppose the rank is four.  Choose four independent rows and let
`alpha_0,...,alpha_4 in F[X]` be their signed cofactor relation, divided by
their common polynomial gcd.  Every selected row satisfies

```text
alpha_0+gamma alpha_1+gamma^2 alpha_2
 +(alpha_3+gamma alpha_4) f_gamma=0.                      (5.2)
```

Cofactor degrees give

```text
deg alpha_0,alpha_1,alpha_2<=2kappa-2,
deg alpha_3,alpha_4<=kappa-1.                             (5.3)
```

Put

```text
D_gamma=alpha_3+gamma alpha_4,
N_gamma=alpha_0+gamma alpha_1+gamma^2 alpha_2,
calR=alpha_0 alpha_4^2-alpha_1 alpha_3 alpha_4
     +alpha_2 alpha_3^2.                                 (5.4)
```

If a polynomial divides both `alpha_3` and `alpha_4`, (5.2) at three
distinct slopes makes it divide `alpha_0,alpha_1,alpha_2`; primitivity
therefore gives `gcd(alpha_3,alpha_4)=1`.  Hence distinct nonzero
`D_gamma` are pairwise coprime.  Since `f_gamma` is a polynomial,
`D_gamma` divides `N_gamma`, and substitution modulo `D_gamma` shows

```text
D_gamma divides calR,
deg calR<=4kappa-4.                                      (5.5)
```

If `calR=0`, the linear polynomial
`alpha_3+Z alpha_4` divides
`alpha_0+Z alpha_1+Z^2 alpha_2` over `F(X)`.  All slopes except possibly
the unique one with `D_gamma` identically zero therefore lie in one affine
pencil.  Two nonexceptional polynomial values show that the two affine
coefficients are themselves polynomials.  The exceptional slope raises the
actual core rank by at most one.

Suppose `calR!=0`.  Then `D_gamma` cannot be identically zero for a selected
slope, because (5.2) would give `N_gamma=0` and hence `calR=0`.  If
`alpha_3,alpha_4` are constants, every `f_gamma` lies in the fixed
`F`-span of `alpha_0,alpha_1,alpha_2`, so the actual core rank is at most
three.  Otherwise at most one `D_gamma` has degree zero.  The remaining
pairwise-coprime nonconstant divisors of `calR` give

```text
L-1<=sum_gamma deg D_gamma<=deg calR<=4kappa-4,
```

which proves `L<=4kappa-3`.

For the constant-core alternative, complete-zero-mask detection gives one
detecting basis of size at most four per slope.  The usual cross-support
property and the nonuniform set-pair permutation argument give the displayed
polynomial charge.  No generic-rank or literature input is used.

The companion actual-core theorem's hypotheses hold in this GRS setup:
`d<=R`, so `t<d` implies `t<R` and kernel distance `R+1>t`; if both
received syndromes lay in one selected support span, their difference would
give a `y_1`-lift of weight at most `t`, contradicting the definition of
`d`.

## 6. Fixing four actual slopes in the nonzero branch

Assume some actual five-tuple has `Delta!=0`.  Its five graph rows in (2.5)
are independent over `F(X)`.  For each omitted index `i`, the other four
rows form a rank-four base and have common zero count `h_i` from (3.7).
Choose an omission maximizing `h_i`; call the resulting base
`mathcal B`.  At the stress,

```text
g=|G_mathcalB|=|intersection_(i in mathcalB)T_i|>=50u.   (6.1)
```

Let `bar beta_0,...,bar beta_4` be the raw signed cofactors of the fixed
four graph rows and define, for every retained `gamma notin mathcal B`,

```text
bar E_gamma=bar beta_0+gamma bar beta_1+gamma^2 bar beta_2
            +(bar beta_3+gamma bar beta_4)f_gamma.        (6.2)
```

Then

```text
bar E_gamma
 =+/- V_mathcalB product_(i in mathcalB)(gamma-gamma_i)
       Delta_(mathcalB union {gamma}).
                                                                    (6.3)
```

At a root common to the four base locators, the base values `f_i(x)` are
affine in `gamma_i`, so the four graph rows have rank at most three.
Every cofactor vanishes.  Consequently the fixed polynomial

```text
G_mathcalB(X)=product_(x in intersection_(i in mathcalB)T_i)(X-x)
                                                                    (6.4)
```

divides every `bar beta_j`.  Because the base rows have rank four,
`g<=kappa-1`.

Let `H=gcd(bar beta_3,bar beta_4)`.  Applying the four base relations at
any three base slopes shows that `H` divides every `bar beta_j`;
conversely every common cofactor divisor divides these last two entries.
Thus `H` is the full common cofactor gcd and `G_mathcalB divides H`.
Put `beta_j=bar beta_j/H` and `E_gamma=bar E_gamma/H`.  The resulting
degree bounds are at most

```text
2kappa-2-g for beta_0,beta_1,beta_2,E_gamma,
kappa-1-g  for beta_3,beta_4.                             (6.5)
```

### 6.1 The zero-determinant class and multiplier rank cell

The slopes satisfying `E_gamma=0` obey one fixed relation of the form (5.2).
The proof of Theorem 5.1, applied to this fixed relation, shows that this
class is polynomially bounded or has constant actual core.

After primitive division, put `D_gamma=beta_3+gamma beta_4`.  The nonzero
polynomials `D_gamma` are pairwise coprime.  Their root sets on `U` are
therefore disjoint.  At most `N` slopes can have a nonempty domain-root set,
plus at most one slope can have `D_gamma` identically zero.  This literal
multiplier/rank-pivot sub-branch is directly `O(N)`-paid.  The residual may
be assumed to have `D_gamma(x)!=0` for every `x in U`.

### 6.2 The exact four-block probe

For `i in mathcal B`, let `A_i` be the coordinates where base witness
`i` is the unique supported member of `mathcal B`, and put
`A^(1)=disjoint_union_i A_i`.  If `x in A_i`, the base graph matrix has
rank four, so `H(x)!=0`; primitive division preserves the following
identity:

```text
E_gamma(x)=q_i(x) (gamma_i-gamma) C_i(x)C_gamma(x),        (6.6)
```

where `q_i(x) in F^*` depends only on the fixed base and the harmless global
normalization.  In particular,

```text
E_gamma(x)=0 iff x in T_gamma,  x in A_i.                 (6.7)
```

This is an exact actual-witness probe, not a statement about an arbitrary
null tuple.

If `a_1=|A^(1)|`, the four-base support budget gives

```text
2g+a_1>=2N-sum_(i in mathcal B)wt(c_i)>=2N-4t.           (6.8)
```

At the stress, `2g+a_1>=400u`.

### 6.3 Exact distance and Johnson route cut

Factoring the fixed `G_mathcalB` shortens length and degree equally.  Under
`2kappa-1<=N`, the ambient residual collision code has parameters bounded by

```text
length=N-g,
dimension<=2kappa-1-g,
distance>=N-2kappa+2.                                    (6.9)
```

At the stress the last quantity is still only `50u+2`, while moving
witnesses may have weight `150u`.  The fixed divisor therefore gives no
MDS-distance improvement.

There is a separate residual-polynomial Johnson failure.  Put

```text
D_0=2kappa-2-g,
a=|A^(1)|<=N-g.
```

For `a>=t`, the ordinary polynomial agreement condition would require
`(a-t)^2/a>D_0`.  The left side increases with `a`, so at the stress,
using `50u<=g<=kappa-1<225u`,

```text
D_0-(a-t)^2/a
 >=450u-2-g-(350u-g)^2/(500u-g)
 >=(1850/11)u-2>0.                                      (6.10)
```

If `a<t`, there is no positive guaranteed probe agreement at all.  Thus the
residual-polynomial Johnson route misses by a positive linear amount.

The ordinary pairwise Johnson denominator also remains nonpositive.  On a
probe of size `a_1`, the guaranteed agreement is only `a_1-t`, and two
different actual witnesses have at most `N-d=250u` common zeros.  For every
relevant `150u<=a_1<=500u`,

```text
(a_1-150u)^2-250u a_1
 =a_1^2-550u a_1+22500u^2<=0,                            (6.11)
```

because the two roots are `(275+/-25 sqrt(85))u`, approximately
`44.512u` and `505.488u`.  The original full-mask comparison misses by
exactly `5u`:

```text
(N-t)^2/N=245u < N-d=250u.                               (6.12)
```

Thus neither ordinary RS distance nor the pairwise Johnson incidence pays
the fixed-base residual.  What remains is a value-sensitive four-block
masked-product slope-projection/occupancy theorem for (6.2) and (6.6).

## 7. Exact `F_101` counterguard

This finite guard prevents the fixed determinant factor from being renamed a
moving planted locator or a local witness-multiplicity/ray-occupancy payment.

Take

```text
F=F_101,
U={0,1,...,9},
kappa=5,
y=ev_U(X^7-31X^6),
v=ev_U(X^5),
t=3.                                                       (7.1)
```

For every three-subset `B subset U` with integer sum `14`, let `T=U\B`.
Then

```text
product_(a in T)(X-a)
 =X^7-31X^6+gamma_T X^5+f_T(X),
deg f_T<5,
gamma_T=e_2(T).                                           (7.2)
```

The ten supports and distinct slopes are

```text
support B   slope gamma_T
{0,5,9}     88
{0,6,8}     85
{1,4,9}     84
{1,5,8}     80
{1,6,7}     78
{2,3,9}     82
{2,4,8}     77
{2,5,7}     74
{3,4,7}     72
{3,5,6}     70.                                           (7.3)
```

The direction distance is `d=5`: a nonzero monic degree-five polynomial has
at most five roots, and equality is attained.  Hence `t<d`.  The ten colors
are singleton colors in this locator-prefix line, because (7.3) exhausts all
seven-subsets with first coefficient `31`, and their second coefficients are
distinct.

Exhaustive exact replay gives:

```text
ten-slope actual core:              s=6, r=5
five-subsets:                       252
five-subset graph rank:             5 in all 252
U_(2,5) operator rank:              13 once, 14 in 251 cases (<15)
operator row count:                 15 in 246, 16 in 6 cases
Delta=0:                            0 cases
deg Delta:                          7 in 7, 8 in 245 cases
roots of Delta on U:
  3/4/5/6/7 roots:                  7/58/112/66/9 cases.   (7.4)
```

Fix base slopes `{88,85,80,78}`.  Its common zero set and probe are

```text
G_B={2,3,4},
A^(1)={7,9}.                                               (7.5)
```

The raw cofactor degrees are `(8,8,8,4,4)`; after division by `G_B` they are
`(5,5,5,1,1)`.  Among the six moving slopes only `gamma=82` has a multiplier
root on `U`, at `x=3`, as required by the disjoint-root rank sub-branch.

Every one of the six moving supports meets `G_B`:

```text
gamma 84/82/77/74/72/70 meets G_B in
      {4}/{2,3}/{2,4}/{2}/{3,4}/{3}.                      (7.6)
```

Therefore none of their moving locators contains all of `G_B`, although
`G_B` divides every fixed-base collision determinant.  The colors are also
singleton, so the explanation-to-slope occupancy is one.  This is an exact
finite falsifier of both naive implications

```text
common determinant divisor => common moving-locator planted block,
nonzero collision determinant => local witness-multiplicity or
                                  ray-occupancy payment.   (7.7)
```

The guard is constant-size and directly paid.  It is not an asymptotic
primitive counterexample.  Amplifying this kind of locator-prefix seed by
composition or positional tensoring introduces a declared quotient or
planted/moment structure and, in the known tensor, makes `(R-t)/N -> 0`.

## 8. Exact surviving atom

After the theorem above, an unpaid family can be reduced, using only actual
surviving witnesses, to one fixed rank-four base with:

1. `E_gamma!=0` for all but polynomially many slopes;
2. the multiplier `D_gamma` nonzero on every domain coordinate;
3. one fixed base divisor removed, with no gain in MDS distance;
4. the exact four-block probe (6.6)--(6.7); and
5. linear actual core and singleton-compatible colors still allowed.

The missing statement is a direct distinct-slope or occupancy bound for this
fixed-base masked-product incidence.  Naming its base divisor `planted`, or
its nonzero collision word `saturation`, is not a proof: the moving locators
need not contain the divisor, and occupancy can be one.

## 9. Provenance and ownership

This preflight is a consumer/reduction note, not a novelty claim.

- PR #71 (`17adfc4`) and PR #95 (`5f6132a`) are moving-scroll,
  rank-determinant, quadric, and conic adjacency only; none is imported as a
  theorem for the present operator.
- PR #198 (`352bd615`) is the earlier Cramer/evaluation-eliminant and
  projectivized first-layer audit provenance.
- PR #221 (`ba0d19e`) owns the cofactor/identically-split repair warning:
  roots of a cofactor stay in the rank-drop ledger, while an identically
  split top chart can be contained rather than residual.
- PR #528 (`12f68ec`) owns the field-independent transverse-secant/bounded-core
  payment used for comparison with constant actual core.
- PR #659 (`a8a53aa`) owns the completed-witness/full-support and zero-boundary
  A6 setup.
- PR #670 (`08198f1`) owns ambient agreement-multiplicity weighting.
- PR #671 (`b0ce6c5`) owns the completed-Cramer subexponential strata.
- PR #676 (audited source snapshot `fe8b6ef`; endpoint-repair head
  `9ef4cc6`) owns the completed-zero-mask two-block payment and the central
  stress used here.
- PR #640 (`7d83103`) owns the minimal-polynomial simple-pole residue and
  slope-saturation terminology; (4.3) is a coefficient-side transpose, not a
  claimed instance of that theorem.
- PR #678 (`042a4ff`) is cited only for the nearby seed/moment-image and
  tensor-amplification overlap, not for the conic determinant proof.
- PR #666 (`01c66ae`) owns the split-pencil ray-collapse/deduplicated list
  distinction.
- PR #679 (`53bb72c`) owns the warning that raw support counts at planted
  near-codeword lines must be replaced by slope/ray-deduplicated counts.

The determinant algebra does not supersede any of these.  In particular it
does not promote a tuple-dependent divisor into a paid planted profile or a
collision word into a paid saturation image.

## 10. Verification and nonpromotion guard

The companion standard-library verifier is

```text
experimental/scripts/verify_a6_u2_source_rooted_conic_preflight.py
```

It reconstructs (2.4)--(2.5), the complete `F_101` census, the fixed-base
cofactor/gcd/probe/multiplier facts, the stress arithmetic, and tamper guards.
This experimental note has been hypothesis-audited for repository publication.
Every later consumer must still match its literal hypotheses before any
statement is promoted into TeX.
