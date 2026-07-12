# A U(2,L) five-slope rank packet for the A6 weighted-RS residual

- **Status:** experimental audit packet.  The conditional theorem and the
  structured counterexample below are proved under their literal hypotheses.
  No statement here is proposed for TeX promotion.
- **Scope:** one fixed actual witness selector on one weighted-RS syndrome
  line, after any declared first-match deletion.  The matrix depends on the
  selected complete zero masks.
- **Relationship to the companion A6 packet:** the actual-core/set-pair charge
  in `a6_actual_witness_core_rank_preflight.md` already pays constant actual
  core rank.  This packet tests a new value-sensitive route on the remaining
  linear-rank, linear-support stress.
- **Companion verifier:**
  `experimental/scripts/verify_a6_u2_five_slope_rank_preflight.py`.
- **Nonclaims:** no primitive-rank theorem, atlas exhaustion, A2, RC, full A6,
  A7, deployed-row result, prize closure, or TeX change.

## 1. Result and route cut in one page

Let `U` be a set of `N=R+kappa` distinct field elements and let

```text
K={ (omega_x f(x))_(x in U) : deg f<kappa }
```

be an `[N,kappa,R+1]` GRS code, with every `omega_x` nonzero.  Fix vectors
`y,v` and put

```text
d=min_{f in P_<kappa} wt(v+omega*f).
```

For distinct slopes `gamma_i`, suppose selected actual witnesses have the form

```text
c_i=y+gamma_i v+omega*f_i,  deg f_i<kappa,  wt(c_i)<=t<d.
```

Write `T_i={x:c_i(x)=0}` and `I_x={i:x in T_i}`.  At every coordinate, the
values `(f_i(x))_(i in I_x)` lie on an affine function of the slope:

```text
f_i(x)=A_x+gamma_i B_x.
```

Consequently every vector `lambda` supported on `I_x` with

```text
sum_i lambda_i=0,  sum_i lambda_i gamma_i=0
```

gives one evaluation row `sum_i lambda_i f_i(x)=0`.  These rows define the
operator `M_2` below.  Its unavoidable kernel is the `2kappa`-dimensional
space `f_i=p+gamma_i q`.

**Conditional theorem.**  If five selected slopes have

```text
rank M_2=3kappa,
```

then the five polynomial approximants form one affine pencil.  The witnesses
then form one affine vector line `a+gamma_i b`, where `b` is a `y_1` lift of
weight at least `d`.  Counting coordinate zeros gives

```text
L(d-t)<=d.
```

For a positive integer `u`, at the central stress

```text
(N,R,kappa,d,t)=(500u,275u,225u,250u,150u),
```

this permits at most two affine-line witnesses.  Hence a full-rank five-tuple
is impossible, and a family satisfying the five-mask rank property has size at
most four.

The row count is not the obstruction: five masks contain at least

```text
5(N-t)-2N=750u
```

local `U_(2,5)` rows for `3kappa=675u` quotient unknowns.

**Exact counterguard.**  The rank property is false for arbitrary structured
GRS domains even with the complete generalized-weight profile.  A finite
`F_11` seed has nine slopes; pulling it back by `X |-> X^(50u)` gives the exact
central stress.  Every five-subfamily is singular.  The masks are complete
power-map pullbacks, and the seed has actual core rank exactly five, so it is
paid both by the earlier quotient branch and by the companion actual-core
theorem.  It is not a primitive high-rank counterexample.

The companion theorem's hypotheses are literal here.  For the GRS quotient,
`d<=R`; hence `t<d` gives `t<R` and kernel distance `R+1>t`.  If both
received syndromes lay in the span of one selected support `S_gamma`, their
difference would give a `y_1`-lift supported on `S_gamma` of weight at most
`t`, contradicting the definition of `d`.

The surviving research statement is therefore hereditary and post-routing:

```text
every post-first-match actual family of at least five slopes is
U_(2,5)-singular on every five-subfamily;
prove that this hereditary singularity forces a paid quotient/pullback,
pencil/balanced-core, or sublinear-core certificate.
```

Mere generalized Hamming weights, individual-mask aperiodicity, witness-color
multiplicity, or a row count do not supply that classification.

## 2. Literal hypotheses and normalization

Let `F` be any field.  Let `U subset F` contain `N` distinct elements and let
`omega=(omega_x)_(x in U)` have no zero entry.  Put

```text
P=P_<kappa={f in F[X]:deg f<kappa},
K=omega*ev_U(P).
```

Assume `1<=kappa<N`.  Then `K` is `[N,kappa,N-kappa+1]` GRS; write
`R=N-kappa`.

Fix `y,v in F^U` and define the source direction distance

```text
d=min_{f in P} wt(v+omega*ev_U(f)).                    (2.1)
```

Equivalently, if `H` is any parity map with kernel `K`, then `d` is the
minimum weight of an `Hv` lift.  Fix `0<=t<d`.

Let `Z={gamma_1,...,gamma_L}` be distinct field elements.  Before defining the
matrix, fix one actual witness at every slope:

```text
c_i=y+gamma_i v+omega*ev_U(f_i),
f_i in P,
wt(c_i)<=t.                                             (2.2)
```

This is the exact affine-coset form of a selected syndrome-line family.  Put

```text
T_i={x in U:c_i(x)=0},
S_i=U\T_i,
I_x={i in [L]:x in T_i}.                                (2.3)
```

Thus `|T_i|>=N-t`.  Dividing the zero equation by `omega_x` gives

```text
f_i(x)=-y(x)/omega_x-gamma_i v(x)/omega_x
      =A_x+gamma_i B_x,  i in I_x.                     (2.4)
```

No transversality hypothesis is used in the rank theorem after (2.1)-(2.2).
In the A6 consumer, transversality is already part of the selected-witness
contract.  The strict inequality `t<d` also implies it whenever the direction
syndrome itself cannot be lifted on `S_i`.

## 3. The exact `U_(2,L)` distributed evaluation operator

For every `x in U`, define the local relation space

```text
R_x={lambda in F^L:
       supp(lambda) subset I_x,
       sum_i lambda_i=0,
       sum_i gamma_i lambda_i=0}.                       (3.1)
```

Because the slopes are distinct,

```text
dim R_x=max(|I_x|-2,0).                                 (3.2)
```

Define

```text
M_2:P^L -> direct_sum_(x in U) R_x^*,
(M_2(f))_x(lambda)=sum_i lambda_i f_i(x).               (3.3)
```

After choosing the monomial basis of `P` and any basis of every `R_x`, a row
indexed by `(x,lambda)` has block `i`

```text
lambda_i (1,x,...,x^(kappa-1)).                         (3.4)
```

Changing a local relation basis left-multiplies rows by an invertible block,
so the rank is intrinsic.  Equation (2.4) proves that the selected tuple
`(f_i)` lies in `ker M_2`.

The affine-pencil subspace

```text
A_gamma={(p+gamma_i q)_(i in [L]):p,q in P}             (3.5)
```

is always contained in the kernel.  For `L>=2` its dimension is `2kappa`.
Thus

```text
rank M_2<=(L-2)kappa.                                   (3.6)
```

We call `M_2` full modulo affine pencils when equality holds.  Equivalently,
the induced map on `P^L/A_gamma` is injective.

The notation `U_(2,L)` records the actual local matroid: `R_x` is the
dependency space of the rank-two Vandermonde columns `(1,gamma_i)`.  Minimal
local circuits have size three.

## 4. Exact row-count gate

Let

```text
Q=sum_x max(|I_x|-2,0)
```

be the number of independent local rows before cross-coordinate relations.
Since `max(m-2,0)>=m-2`,

```text
Q >= sum_x |I_x|-2N
  =  sum_i |T_i|-2N
  >= L(N-t)-2N.                                         (4.1)
```

For `N=R+kappa`, subtracting the quotient column count gives

```text
Q-(L-2)kappa >= L(R-t)-2R.                              (4.2)
```

Hence the first integer order at which the weight-only lower bound guarantees
at least as many rows as quotient columns is

```text
L >= ceil(2R/(R-t)).                                    (4.3)
```

At the central stress, the right side is `ceil(550/125)=5`, and

```text
Q>=750u,  (L-2)kappa=675u,  surplus>=75u.               (4.4)
```

This is only a row count.  It does not imply rank.

## 5. Conditional affine-pencil theorem

### Theorem 5.1

Under Sections 2-3, if `M_2` has rank `(L-2)kappa`, then

```text
L(d-t)<=d.                                               (5.1)
```

In particular

```text
L<=floor(d/(d-t)).                                       (5.2)
```

### Proof

Full quotient rank and (3.5)-(3.6) give

```text
ker M_2=A_gamma.
```

The selected tuple lies in the kernel, so there are `p,q in P` with

```text
f_i=p+gamma_i q.
```

Put

```text
a=y+omega*ev_U(p),
b=v+omega*ev_U(q).
```

Then `c_i=a+gamma_i b`.  By (2.1), `wt(b)>=d`, so the common zero set

```text
C={x:a(x)=b(x)=0}
```

has size at most `N-d`.  At a coordinate outside `C`, the nonzero affine
function `a(x)+gamma b(x)` vanishes for at most one selected slope.  Therefore

```text
sum_i |T_i|
 <= L|C|+(N-|C|)
 <= L(N-d)+d.                                            (5.3)
```

The lower bound `sum_i |T_i|>=L(N-t)` and (5.3) give (5.1).  This proves the
theorem.

### Corollary 5.2 (conditional no-five theorem at the stress)

At `(d,t)=(250u,150u)`, (5.2) gives `L<=2`.  Thus any actual five-tuple has

```text
rank M_2<3kappa.                                         (5.4)
```

Consequently, if a retained family is known a priori to have full quotient
rank on every five masks, then it has at most four slopes.

The more useful contrapositive is hereditary: every actual family with at
least five slopes is singular on **every** five-subfamily.  Closure must
classify hereditary singularity into paid structure; it cannot merely search
inside an existing list for a nonsingular five-tuple without proving such a
classification.

The argument is deletion-monotone.  Any five surviving slopes use the same
selected witnesses and masks after first-match deletion, and the theorem is
applied afresh to that five-subfamily.

## 6. Why generalized-weight Johnson moments do not supply the rank

Let `a=N-t` and write `E=K+<v>` for the ambient one-dimensional code
extension.  If `h+1` list points are affinely independent, their differences
span an `h`-subcode of `E`, so the number of coordinates on which all points
are equal is at most `N-d_h(E)`.  Even under the favorable extra assumption
that every
`h+1` tuple is independent, convexity of common-zero incidences can only become
positive asymptotically when

```text
(a/N)^(h+1)>1-d_h(E)/N.                                 (6.1)
```

At the stress, `a/N=7/10`.  For `h=1`, (6.1) reads

```text
0.49>0.50,
```

which fails by the ordinary Johnson gap.  For `h>=2`, the exact profile is

```text
d_h(E)=R+h-1,
1-d_h(E)/N=(kappa-h+1)/N.                               (6.2)
```

At `h=2`, the two sides are `0.343` and approximately `0.45`; the gap is
larger.  For every `2<=h<=kappa`, the inequality continues to fail.  One way
to see this is that

```text
500u*(7/10)^(h+1)/(225u-h+1)
```

has logarithm convex in `225u-h+1`, so its maximum is at an endpoint; it is
less than one at both `h=2` and `h=kappa`.  The top value `h=kappa+1` has
`d_h=N`, but common-zero `(kappa+2)`-tuples at one coordinate already lie in
an affine hyperplane and are dependent.  Thus the top moment cannot be used.

Nonnegative combinations of these support moments cannot repair a moment
vector that has slack at every order.  The missing information is the joint
value-sensitive rank of (3.3), not another ordinary GHW inequality.

The companion actual-core theorem is the selected-core consequence needed
here: it is polynomial for fixed actual rank and stays exponential when both
actual rank and support are linear.  The sharper reliability comparison below
is optional and does not change the route classification.

## 7. Exact `F_11` seed and central-stress pullback

### 7.1 Finite seed census

Let `Q=F_11^*={1,...,10}`.  For a seven-subset `A`, let `e_j(A)` be its
elementary symmetric functions in `F_11`.  Exhaustive enumeration of all
`C(10,7)=120` subsets gives:

```text
e_1(A)=6  =>  e_2(A) in {0,1,3,4,5,7,8,9,10}.           (7.1)
```

Thus there are nine distinct second-prefix values.  Deterministic
representatives used by the verifier are:

```text
e2  A
 0  {2,3,4,5,7,8,10}
 1  {1,2,4,6,7,9,10}
 3  {1,2,3,4,5,6,7}
 4  {1,3,4,5,7,9,10}
 5  {1,2,5,6,7,8,10}
 7  {1,3,4,6,7,8,10}
 8  {1,2,3,6,8,9,10}
 9  {2,3,4,5,6,9,10}
10  {1,2,4,5,8,9,10}.
```

This finite census is computational; every subsequent algebraic implication
from the displayed representatives is exact.

On the seed domain, write

```text
L_A(Y)=product_(b in A)(Y-b)
      =Y^7-6Y^6+e_2(A)Y^5+R_A(Y),  deg R_A<=4.          (7.2)
```

This is a nine-slope list for the affine line over the `[10,5,6]` RS kernel,
with direction `Y^5`, direction distance five, and witness weight three.

### 7.2 Pullback to the exact central stress

Take `q=11^m` with `m` a positive multiple of `50`, and put

```text
u=(q-1)/500,
U=F_q^*,
N=500u,
kappa=225u,
R=275u,
h=50u.                                                   (7.3)
```

The power map `x |-> x^h` on `U` has kernel size `h` and image the unique
order-ten subgroup, namely `F_11^*`.

Let

```text
K=ev_U(P_<225u),
v=ev_U(X^(250u)),
y=ev_U(X^(350u)-6X^(300u)).                              (7.4)
```

The direction distance is exactly `d=250u`.  Indeed, for every
`f in P_<225u`, the nonzero polynomial `X^(250u)+f` has at most `250u` roots,
while `f=-1` makes `X^(250u)-1` vanish on exactly `250u` elements of `U`.

For each representative in (7.1), put

```text
C_A(X)=product_(b in A)(X^h-b)
      =X^(350u)-6X^(300u)+e_2(A)X^(250u)+R_A(X^h).       (7.5)
```

Here `deg R_A(X^h)<=200u<kappa`, so the evaluation vector is

```text
c_A=y+e_2(A)v+k_A,  k_A in K.                            (7.6)
```

Its complete zero mask is the union of seven `X^h` fibers and has size
`7h=350u`; hence `wt(c_A)=150u=t`.  The nine second-prefix values are distinct
slopes.  They are transverse in the A6 sense because an `Hv` lift supported on
`supp(c_A)` would have weight at most `150u<d`.

Put `E=K+<v>`.  Then `dim E=kappa+1` and

```text
d_1(E)=250u,
d_j(E)=R+j-1  for 2<=j<=kappa+1.                         (7.7)
```

For the lower bound in (7.7), every `j`-subcode of `E` meets `K` in dimension
at least `j-1`, and the MDS kernel has
`d_(j-1)(K)=R+j-1`.  The generalized Singleton bound for the
`[N,kappa+1]` code `E` gives the matching upper bound.

Thus the complete GHW profile does not imply five-mask rank.  Every one of the
`C(9,5)=126` five-subfamilies has `rank M_2<3kappa`: otherwise Theorem 5.1
would give `5(250u-150u)<=250u`, which is false.

### 7.3 Exact low-core reconciliation

For the nine deterministic seed representatives, the coefficient rows

```text
(1,e_2,-e_3,e_4,-e_5,e_6,-e_7)
```

have rank seven over `F_11`.  Thus the selected witness-difference code
`D_Z` has

```text
s=7-1=6,  r=s-1=5.                                      (7.8)
```

The two colors `e_2=1,4` each have two representatives in the eleven-element
`e_1=6` fiber.  There are consequently four global selectors.  Exact replay
checks all four: the full nine-slope family always has `s=6,r=5`, and every
one of the `4*C(9,5)=504` selected five-subfamilies has augmented coefficient
rank five, hence

```text
s_5=5-1=4,  r_5=s_5-1=3.                               (7.8a)
```

For these 504 five-tuples the local operator has 15 or 16 rows and rank 13 or
14, against quotient dimension 15.  The pullback does not change the selected
core ranks.  Therefore the companion actual-core theorem already pays the
family by `|Z|<=binom(N,6)`.  The optional sharper reliability comparison,
with

```text
ell=d-t=100u,
```

its uniform bound is

```text
|Z| <= (5/2) C(275u+5,5)/C(125u+5,5)
     -> (5/2)(11/5)^5 = 128.8408... .                   (7.9)
```

The actual list size nine is consistent.  This counterguard refutes a universal
rank implication; it is not the unpaid linear-core family sought by A6.

## 8. Standard higher-order MDS versus this operator

The condition here is not ordinary MDS(5), not a consequence of the Wei GHW
profile, and not literally the standard list-decoding intersection matrix.

In the standard one-received-word matrix, values on `I_x` are equal; the local
relation space is orthogonal only to `1`, has dimension `|I_x|-1`, and the
trivial global kernel has dimension `kappa`.  Here values lie on an affine
function of a prescribed slope; the local relation space is orthogonal to both
`1` and `gamma`, has dimension `|I_x|-2`, and the trivial kernel has dimension
`2kappa`.

Equivalently, this is a `U_(2,L)` or affine-line cycle-rigidity minor.  It is
only analogous to a rank-two tensor-erasure / matrix-completion condition with
the slope-side `[L,2]` GRS code.  No equivalence to standard MDS(5), a generic
RS theorem, or a maximally recoverable tensor theorem is proved here, so none
may be imported without a separate reduction.  The exact pullback (7.5)
demonstrates that the required rank fails on a literal structured GRS domain.

## 9. What rank failure certifies, and what it does not

Abstract singularity says only that there is a non-affine null tuple

```text
(g_1,...,g_5) in P^5\A_gamma
```

whose evaluations on every `I_x` lie on an affine function of `gamma`.  This is
an algebraic rank certificate, but the extra tuple has no source-rooted
attachment to the actual received line.

At the central stress, the **actual** approximant tuple `(f_i)` cannot be an
affine pencil by Theorem 5.1, and it already lies in the kernel by (2.4).
Only for this actual tuple may one divide by the GRS weights and interpolate
the fixed received vectors by degree-`<N` polynomials `Y,V`, obtaining

```text
Y+gamma_i V+f_i=Q_i A_i,
Q_i=product_(x in T_i)(X-x),
deg A_i<t.                                                (9.1)
```

For every affine slope relation `lambda`,

```text
sum_i lambda_i Q_i A_i=sum_i lambda_i f_i
```

has degree `<kappa`.  In the exact counterguard, all objects descend through
`X^h` and one has `f_i=R_A(X^h)`, so (9.1) is a literal
quotient/pullback certificate.

Generic singularity has no source-rooted semantic certificate and does **not**
by itself imply a common `X^h` factor.  Locator
prefix families at the `t=R-1` singleton extremal already give large singular
families without a required nontrivial power pullback.  Converting (9.1) into a
declared quotient, planted block, split pencil, balanced core, or low-rank cell
is precisely the missing structural theorem and must not be silently assumed.

## 10. Interaction with all-witness and same-color counts

The full-color audit supplies no missing exponent.  At one slope, distinct
weight-`<=t` corrections differ by the `[N,kappa,R+1]` kernel.  With
`a=N-t` and `b=kappa-1`, the ordinary incidence bound gives

```text
L_gamma(a^2/N-b)<=a-b.                                  (10.1)
```

At the stress this is

```text
L_gamma<=floor((125u+1)/(20u+1))=6.                     (10.2)
```

Thus all witnesses at one color buy at most a constant.  Separate exact
singleton-color families show that high selector rank need not force two
witnesses; an `X^2` example is itself quotient-routed.  These facts rule out
using witness-color surplus as a substitute for the `U_(2,5)` value rank.

## 11. Exact post-first-match target

The minimal surviving hypothesis is not "every mask is aperiodic."  It is the
following joint hereditary statement for the literal first-match consumers:

> **Residual hereditary `U_2` target.**  Let a fixed actual selector survive
> all earlier declared quotient/pullback, planted/common-block, tangent,
> split-pencil/balanced-core, saturation, and low-actual-core charges.  If it
> has at least five central-stress slopes, then the singularity of every
> five-subfamily's operator (3.3) forces one of those already paid
> certificates after all.

Equivalently, there is no primitive, linearly high-core family with hereditary
`U_(2,5)` singularity.  Proving this statement would combine with Corollary 5.2
to eliminate the remaining family.  The present packet proves the reduction
and supplies a quotient/low-core counterguard; it does not prove the hereditary
classification.

First-match compatibility must be literal:

1. the selected witnesses and complete zero masks are the actual surviving
   objects, not replacement witnesses;
2. every structural conclusion from singularity is attached to the same
   received line, profile, and slope root;
3. the conclusion names an earlier declared cell with its existing payment;
4. deletion only removes slopes, so Theorem 5.1 may be reapplied to any fixed
   surviving five-subfamily; and
5. no rank statement is promoted merely from the row count (4.4), the GHW
   profile (7.7), or generic/random-locator literature.

That is the exact prize-facing gradient left by this preflight.
