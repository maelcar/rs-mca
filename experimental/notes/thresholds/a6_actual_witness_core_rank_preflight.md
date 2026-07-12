# Actual selected-witness core rank for completed A6 charts

- **Status:** experimental audit packet; proved under the literal hypotheses
  below, but not proposed for TeX promotion.
- **Owner/source snapshot pins:** PR #676 at
  `fe8b6ef7ac57a31228a347d38f6e8d2fbb7323dd`; PR #671 at
  `b0ce6c57049fbafe749d1af1e3a6eef0f9de06e5`; PR #670 at
  `08198f1b7c116710f3b0ba80d4bc00427ed0fe7a`.
- **Pin scope:** PR #676 later advanced to `9ef4cc6f1dbb7007659951f80044fd864991af34`
  with its endpoint repair.  That delta was separately hypothesis-audited;
  the source-pin replay in this packet intentionally remains the frozen
  `fe8b6ef` snapshot.
- **Current-head metadata guard:** the current #676 agents-log shorthand omits
  the hypothesis `Xi_M>=0` from the `e=M` endpoint, and its verifier does
  not assert separate positive coverage of the `e=0`, paid-`e=M`, and
  full-`J` branches.  Neither omission changes the theorem proof, but neither
  shorthand may be promoted.
- **Companion verifier:**
  `experimental/scripts/verify_a6_actual_witness_core_rank_preflight.py`.
  Final normal/optimized replay, source pins, nonuniform core/#670 sums,
  integer rounding, set-pair, exact-weight, endpoint, and semantic-tamper
  gates are green.
- **Relationship to the tree:** the ambient-kernel determinant method is
  already integrated through #528 / `ray_compiler_balanced_core.md`.  The
  ambient-`kappa` growth and shallow-prefix routing audits are already
  integrated through #534 / `balanced_core_kappa_growth.md` and #535 /
  `a4_covers_high_kappa.md`.  PRs #659, #670, #671, and #676 are open source
  heads, not silently treated here as integrated TeX theorems.
- **Novelty posture:** this note makes no external novelty claim.  It records a
  rank-refined application of the existing affine-minor idea to the *actual
  fixed selected witnesses* and audits its exact A6 consumer interface.

## 1. Result in one line

For a fixed actual selected-witness family on one affine syndrome line, let

```text
D_Z = span_F{c_gamma-c_gamma0 : gamma in Z}
```

for any anchor `gamma0 in Z`, and put `s=dim D_Z`.  Under minimum kernel
distance greater than the witness-weight budget and the literal transverse
witness condition, restriction of `D_Z` to every selected witness's complete
zero mask is injective.  A canonical nonzero `s`-minor then labels the slope,
giving the intermediate determinant charge

```text
                         |Z| <= binom(N,s).                (1)
```

Pairing one such basis with each actual selected-witness support gives the
sharper field-general inequalities

```text
sum_gamma 1/binom(s+wt(c_gamma),s)<=1,

|Z|<=B_pair:=binom(s+w_Z,s)<=binom(N,s),
w_Z=max_gamma wt(c_gamma).                                (1a)
```

When `|Z|>=2`, the syndrome map has one-dimensional image on `D_Z`.  Its
kernel is the intrinsic affine-relation image `K_0` defined below, so

```text
s=r+1,  r=dim K_0,  and  |Z|<=binom(N,r+1).                (2)
```

The field-general direct-payment gate is

```text
                         log B_pair=o(n).                  (3)
```

The convenient conditions `N<=n` and either `s=o(n)` or `w_Z=o(n)` are
separately sufficient.  In the nontrivial `|Z|>=2` case, `s=r+1`.

For a nontrivial family `|Z|>=2` under the additional weighted-RS/MDS
hypotheses, if every complete zero mask has size at least
`q>=kappa+1`, `d` is the source minimum `y_1`-lift weight, and
`ell_q=max(1,d+q-N)`, the separate multiplicity theorem supplies the MDS
charge

```text
B_MDS=(s/ell_q) binom(N,s) /
                    binom(q-kappa+r,r),

|Z|<=min(B_pair,B_MDS).                                   (3a)
```

The primary MDS statement is the stronger nonuniform sum
`sum_gamma mu_gamma<=binom(N,s)` of (M2b); `B_MDS` is its uniform
`q`-corollary.  The row-basis denominator is optimal from MDS generalized
weights alone.  A separate
endpoint lemma also supplies the missing `e=0,M` cases needed to make the
#676 `<2N^2` compilation literal; this note does not attribute those
endpoints to the pinned `0<e<M` theorem.

## 2. Exact hypotheses: general linear-code form

Let:

1. `F` be any field and `U` a finite coordinate set of size `N>=1`;
2. `H:F^U -> W` be an arbitrary linear map and `K=ker H`;
3. `t>=0` be an integer such that every nonzero `k in K` has
   `wt(k)>t` (write this as `d(K)>t`);
4. `y_0,y_1 in W`, with `y_1!=0`;
5. `Z subset F` be a finite set of distinct finite slopes; and
6. **before defining any rank**, fix one witness selector
   `gamma |-> c_gamma` on all of `Z` such that, for every `gamma in Z`,

```text
H c_gamma = y_0+gamma y_1,
wt(c_gamma)<=t,
{y_0,y_1} not subset H(F^{S_gamma}),
S_gamma=supp(c_gamma).                                    (4)
```

Here `F^{S}` denotes the coordinate subspace supported on `S`.  Thus the last
line is exactly the transverse completed-witness hypothesis: the support of
the *selected actual witness* does not simultaneously span both direction
syndromes.  Put

```text
T_gamma=U\S_gamma={x in U:c_gamma(x)=0}.                  (5)
```

No Reed--Solomon structure, MDS generalized weights, minimum lift of `y_1`,
punctured weight `e`, two-block inequality, or sign condition on `Xi_e` is
used in the proof of (1).

### Weighted-RS specialization used by #659/#671/#676

Take `H=H_U` with weighted Vandermonde columns

```text
h_x=lambda_x(1,x,...,x^(R-1))^T,  lambda_x!=0,
N=R+kappa,
```

at distinct evaluation points, with `kappa>=1` and `0<=t<R`.  Then
`K=ker H_U` is an `[N,kappa,R+1]` GRS code, so `d(K)=R+1>t`; (4) is exactly
the completed transverse-witness contract printed by the pinned source PRs.
The family `Z` may be the whole actual retained first-match family, or a
subset obtained from it as described in Section 7.

## 3. Intrinsic affine span and coefficient-map rank

Assume first that `Z` is nonempty and fix any anchor `gamma_0 in Z`.  Define

```text
D_Z=span{c_gamma-c_gamma0:gamma in Z},
s=dim D_Z.                                                 (6)
```

The subspace `D_Z` is independent of the anchor: changing the anchor only
replaces the generating differences by linear combinations of the old ones.

Define the intrinsic coefficient space and coefficient map

```text
E_Z={a in F^Z:
       sum_gamma a_gamma=0,
       sum_gamma gamma a_gamma=0},

theta_Z:E_Z -> K,
theta_Z(a)=sum_gamma a_gamma c_gamma,

K_0=im theta_Z,
r=dim K_0.                                                 (7)
```

The map really lands in `K`, because both affine syndrome terms cancel:

```text
H theta_Z(a)
 = (sum a_gamma)y_0+(sum gamma a_gamma)y_1=0.              (8)
```

Moreover,

```text
                         K_0=D_Z intersect K.              (9)
```

Indeed, every `theta_Z(a)` is visibly a linear combination of anchored
differences.  Conversely, write `z in D_Z` as

```text
z=sum_(gamma!=gamma0) b_gamma(c_gamma-c_gamma0).
```

The corresponding coefficients have total sum zero.  If `z in K`, then

```text
0=H z=
  (sum_(gamma!=gamma0)b_gamma(gamma-gamma0))y_1.
```

Since `y_1!=0`, their slope-weighted sum also vanishes, so those coefficients
belong to `E_Z` and `z=theta_Z(a)`.

If `|Z|>=2`, then `H(D_Z)=<y_1>`: one nonzero anchored difference maps to a
nonzero scalar multiple of `y_1`, and every anchored difference maps into
that line.  Rank-nullity and (9) give

```text
                         s=r+1.                            (10)
```

If `|Z|=1`, then `D_Z=0`, `E_Z=0`, and `s=r=0`.  The unified bound (1) is
then the sharp statement `1<=binom(N,0)=1`; formula (10) is deliberately not
invoked.

## 4. Equivalent two-base-slope curvature form

For `|Z|>=2`, choose any distinct base slopes `alpha,beta in Z` and set

```text
v=(c_beta-c_alpha)/(beta-alpha),
u=c_alpha-alpha v,
w_gamma=c_gamma-u-gamma v.                                (11)
```

Then

```text
H u=y_0,
H v=y_1,
w_gamma in K,
w_alpha=w_beta=0,
c_gamma=u+gamma v+w_gamma.                                (12)
```

The intrinsic and base-pair forms agree exactly:

```text
K_0=span{w_gamma:gamma in Z},
D_Z=K_0+<v>.                                               (13)
```

To see the first equality, affine terms cancel in every `theta_Z(a)`.  In the
other direction, for `gamma` different from the two bases, use the relation

```text
a_gamma=1,
a_alpha=(gamma-beta)/(beta-alpha),
a_beta=(alpha-gamma)/(beta-alpha),                         (14)
```

whose coefficient and slope sums are zero; its image under `theta_Z` is
`w_gamma`.  Equation (13) then follows from anchored differences and the fact
that `v=(c_beta-c_alpha)/(beta-alpha)` belongs to `D_Z`.

This proves the promised base-pair invariance, rather than assuming it.  If a
different pair gives `u',v',w'_gamma`, then

```text
span{w'_gamma}=K_0,
v'-v in K_0,
u'-u in K_0,
K_0+<v'>=K_0+<v>=D_Z.                                     (15)
```

The interpolating lift `v` in (11) need **not** be the minimum lift used by
#659/#671/#676 to define `J`, `M`, `e`, or `Xi_e`.  It is introduced only
after the selected slope family has been fixed and does not alter those
earlier profile assignments.

## 5. Main theorem and proof

### Theorem (actual selected-witness affine-rank charge)

Under the hypotheses of Section 2, every nonempty selected family satisfies

```text
                         |Z|<=binom(N,s),                  (16)
```

where `s=dim D_Z`.  Consequently, if `|Z|>=2`,

```text
                         |Z|<=binom(N,r+1),                (17)
```

where `r=dim im(theta_Z)`.  The result remains valid over an arbitrary field
and after arbitrary first-match deletion: on the surviving family, fix any
actual selector satisfying Section 2 and apply the theorem afresh.  Keeping
the restrictions of one previously fixed selector is needed only for the
rank-monotonicity and global exact-`e` bookkeeping statements in Section 7,
not for validity of the theorem itself.

### Step 1: every complete zero mask detects `D_Z`

Fix `gamma in Z`.  We claim that the coordinate restriction

```text
                         D_Z -> F^{T_gamma}                (18)
```

is injective.  Let `z in D_Z` vanish on `T_gamma`.  Then `z` is supported
inside `S_gamma`, so `wt(z)<=|S_gamma|<=t`.  Since `H(D_Z)<=<y_1>`, write

```text
                         H z=beta y_1.                     (19)
```

If `beta=0`, then `z in K`; the kernel-distance hypothesis `d(K)>t` forces
`z=0`.

If `beta!=0`, put `q=beta^{-1}z`.  Both

```text
H q=y_1,
H(c_gamma-gamma q)=y_0                                   (20)
```

have lifts supported inside `S_gamma`, because both `z` and `c_gamma` do.
Thus `y_0` and `y_1` both lie in `H(F^{S_gamma})`, contradicting the third
line of (4).  Hence the second case is impossible and (18) is injective.

In the base-pair notation this is exactly the asserted injectivity of
`K_0+<v>` on every complete zero mask.  The two cases in the preceding proof
are respectively the kernel-distance and transversality branches.

### Step 2: a canonical invertible minor exists

Choose once and for all a total order on `U` and a basis
`b_1,...,b_s` of `D_Z`.  Let `B` be the `N by s` coordinate matrix of this
basis.  Injectivity of (18) says that `B_{T_gamma}` has column rank `s`.
In particular, `|T_gamma|>=s`, and there is an `s`-subset
`I subseteq T_gamma` with

```text
                         det B_I !=0.                      (21)
```

Assign to `gamma` the lexicographically first such `I`.  This makes the
charge canonical relative only to the fixed coordinate order and basis; no
choice of minimum lift or base pair enters.

### Step 3: a fixed minor uniquely recovers the selected slope

For each `gamma`, write uniquely

```text
                         c_gamma=c_gamma0+B x_gamma.       (22)
```

If `I subseteq T_gamma`, its zero equations are

```text
                         B_I x_gamma=-c_gamma0|_I.         (23)
```

When `det B_I!=0`, equation (23) uniquely recovers `x_gamma`, hence uniquely
recovers `c_gamma`.  Finally `Hc_gamma=y_0+gamma y_1` and `y_1!=0` uniquely
recover `gamma`.  Two different slopes therefore cannot receive the same
canonical `I`.  There are `binom(N,s)` possible labels, proving (16).

For `s=0`, the only label is the empty set and (23) says all selected
witnesses equal the anchor; `y_1!=0` then permits only one slope.  Thus the
same argument includes the `|Z|=1` edge case without a fictitious base pair.

## 5A. Field-general support/set-pair refinement

The determinant charge has a second exact consequence under the same
field-general hypotheses.  Define the maximum **actual selected-witness**
weight

```text
w_Z=max_(gamma in Z) wt(c_gamma)<=t.                      (P1)
```

Then

```text
sum_(gamma in Z)
  1/binom(s+wt(c_gamma),s) <=1,                           (P2)

|Z|<=binom(s+w_Z,s)<=binom(N,s).                          (P3)
```

The first inequality is nonuniform and retains every actual witness weight.
The coarser consequence `|Z|<=binom(s+t,s)` is valid because `w_Z<=t`,
but it need not improve `binom(N,s)` when the budget `t` is loose.  The
actual-weight form in (P3) always does.

### Step 1: selected zero-mask bases cross every other support

For each `gamma`, choose one `s`-subset

```text
                         I_gamma subseteq T_gamma
```

on which the fixed generator of `D_Z` is invertible.  Section 5 proves that
such a basis exists.  Put `B_gamma=S_gamma=supp(c_gamma)`.  By construction,

```text
                         I_gamma intersect B_gamma=empty. (P4)
```

For every ordered pair of distinct slopes `gamma,eta`,

```text
                         I_gamma intersect B_eta!=empty.  (P5)
```

Otherwise `I_gamma` would lie in both complete zero masks
`T_gamma` and `T_eta`.  The same invertible `D_Z`-restriction and the
same zero equations (23) would recover both selected coefficient vectors,
forcing `c_gamma=c_eta`.  Applying `H` and using `y_1!=0` would then force
`gamma=eta`, a contradiction.  This argument uses the actual support of the
fixed selected witness, not an ambient or synthetically padded support.

### Step 2: self-contained nonuniform set-pair inequality

We use the following elementary form of the Bollobas set-pair inequality.
For finite pairs `(A_i,B_i)` satisfying

```text
A_i intersect B_i=empty,
A_i intersect B_j!=empty for i!=j,
```

one has

```text
sum_i 1/binom(|A_i|+|B_i|,|A_i|)<=1.                     (P6)
```

To prove it, choose a uniformly random permutation of the ground set and let
`E_i` be the event that every element of `A_i` appears before every element
of `B_i`.  Relative-order symmetry gives

```text
Pr(E_i)=1/binom(|A_i|+|B_i|,|A_i|).
```

The events are pairwise disjoint.  If both `E_i` and `E_j` occurred, choose

```text
x in A_i intersect B_j,
y in A_j intersect B_i.
```

The own-pair disjointness makes `x!=y`.  Event `E_i` puts `x` before
`y`, while `E_j` puts `y` before `x`, a contradiction.  Summing the
disjoint event probabilities proves (P6).

Apply (P6) to `A_gamma=I_gamma` and `B_gamma=S_gamma`.  Equations
(P4)--(P5) give (P2), and every denominator in (P2) is at most
`binom(s+w_Z,s)`, proving the first inequality in (P3).

Finally choose a slope whose selected witness has weight `w_Z`.
Injectivity of `D_Z` on its complete zero mask gives

```text
                         s<=N-w_Z.
```

Hence `s+w_Z<=N` and `binom(s+w_Z,s)<=binom(N,s)`, proving the second
inequality in (P3).  The singleton branch is included: if `s=0`, (P2)
already gives `|Z|<=1`.

The sharp ambient specialization is compatible with #528.  When
`s=kappa+1` and the only available weight information is `t=R-1`, the
coarse set-pair bound is

```text
binom(s+t,s)=binom(N,kappa+1).
```

Thus the integrated attained `kappa=1,2` examples are not contradicted.
Any improvement in (P3) comes from smaller actual affine dimension or smaller
actual selected-witness support.

More generally, on the full ambient specialization `s=kappa+1`, (P3) reads

```text
|Z|<=binom(kappa+1+w_Z,kappa+1).
```

For `N=O(n)`, this is subexponential whenever `kappa=o(n)` or
`w_Z=o(n)`.  It therefore sharpens the convenient
`kappa=o(n/log n)` regime displayed with the original crude determinant
count, while leaving the deep `kappa=Theta(n)`, `w_Z=Theta(n)` wall intact.
The low-support side is likely shallow/#535 overlap, and the conclusion
reconciles rather than contradicts the ambient-growth finding of #534.

## 5B. Separate MDS basis-multiplicity refinement

The preceding theorem is field-general and uses only `d(K)>t`.  The result
in this section is a strictly separate refinement that uses the full MDS
structure of the weighted-RS kernel, the minimum weight of a source
`y_1`-lift, and a uniform complete-zero-mask floor.  None of those extra
hypotheses is silently imported into Section 5.

Pinned PR #670 is the direct multiplicity antecedent: it weights each slope
by many full-ambient `(kappa+1)` affine minors.  The theorem below changes
the axis to the actual core dimension `r` and adds the source minimum-lift
extension factor.  It is compared explicitly with #670 after the proof and
is not described as the first agreement-multiplicity theorem.

### Theorem (actual-core basis multiplicity)

Assume the weighted-RS specialization of Section 2 and `|Z|>=2`.  Thus

```text
K=[N,kappa,R+1] is MDS,
K_0=D_Z intersect K,
r=dim K_0,
s=dim D_Z=r+1.                                           (M1)
```

Let

```text
d=min{wt(z):H z=y_1}                                     (M2)
```

be the source minimum-lift weight.

Since `y_1!=0`, one has `d>=1`.  Any `R` weighted-Vandermonde parity
columns form a basis of the syndrome space, so `y_1` has an `R`-supported
lift and

```text
                         1<=d<=R.
```

For each selected slope define its actual mask size and exact local
multiplicity

```text
a_gamma=|T_gamma|,
ell_gamma=max(1,d+a_gamma-N),

mu_gamma=ceil[
  (ell_gamma/s)
  binom(a_gamma-kappa+r,r)
].                                                        (M2a)
```

Then the exact nonuniform actual-core inequality is

```text
                         sum_gamma mu_gamma<=binom(N,s).  (M2b)
```

This is the direct actual-core analogue of the nonuniform #670 sum (M16).
It retains every actual complete-mask size and should be used before any
uniform weakening.  The binomial range is valid because
`a_gamma>=N-t>kappa`.

Fix an integer `q` such that

```text
kappa+1<=q<=N,
|T_gamma|>=q for every gamma in Z,                        (M3)
```

and put the matched extension factor

```text
ell_q=max(1,d+q-N).                                       (M4)
```

Then

```text
mu_q=ceil[
       (ell_q/s) binom(q-kappa+r,r)
     ],

|Z|<=floor(binom(N,s)/mu_q)
   <=(s/ell_q) binom(N,s) /
                    binom(q-kappa+r,r)
   =:B_MDS.                                               (M5)
```

The uniform statement is the corollary of (M2b): from
`a_gamma>=q`, both `ell_gamma>=ell_q` and
`binom(a_gamma-kappa+r,r)>=binom(q-kappa+r,r)`, so
`mu_gamma>=mu_q` for every slope.

Since `q>=kappa+1`,

```text
binom(q-kappa+r,r)>=binom(r+1,r)=s,
```

so (M5) always refines the basic MDS-specialized bound
`|Z|<=binom(N,s)`.  The case `r=0` is included:
`binom(q-kappa,0)=1`, `s=1`, and the refinement is the matched
rank-zero pencil bound `|Z|<=N/ell_q`.

### Step 1: the generalized-weight row-flat bound

Choose a generator of `K_0` and write its coordinate rows as

```text
                         g_x in F^r,  x in U.             (M6)
```

Let `L<=F^r` be a **linear** `j`-dimensional subspace with
`0<=j<r`.  The annihilator `L^perp` has dimension `r-j`.  Its coefficient
vectors generate an `(r-j)`-dimensional subcode of `K_0<=K` which vanishes
at every coordinate whose row `g_x` lies in `L`.  The MDS generalized
weight profile

```text
d_(r-j)(K)=R+r-j
```

therefore gives

```text
#{x in U:g_x in L}
 <=N-(R+r-j)
 =kappa-r+j.                                              (M7)
```

This assertion concerns linear row flats, not affine or projective flats.
It is used only for `j<r`.

### Step 2: greedily count `K_0`-row bases in every mask

Fix `gamma` and write `T=T_gamma`.  After `j` independent coordinate
rows have been chosen, their span is a linear `j`-flat.  By (M7), at most
`kappa-r+j` rows of all of `U`, hence of `T`, lie in that span.  The next
row has at least

```text
                         q-kappa+r-j                      (M8)
```

choices.  Multiplying for `j=0,...,r-1` and dividing by the `r!` orders of
each basis shows that the number `b_T` of `r`-subsets of `T` which are
row bases for `K_0` satisfies

```text
b_T>=binom(q-kappa+r,r).                                  (M9)
```

For comparison only, the earlier direct double count gives the weaker
cross-check

```text
b_T>=binom(q,r)/binom(kappa,r).                           (M10)
```

Indeed every `kappa`-subset of `T` has rank `r` on `K_0`, because a
nonzero kernel word vanishing there would have weight at most
`N-kappa=R`.  Count pairs consisting of such a `kappa`-set and one
contained `K_0`-basis.  Formula (M10) is not used in the final bound; the
row-flat profile (M9) dominates it.

### Step 3: every `K_0`-basis has at least `ell_q` extensions

Fix a row basis `B subseteq T` of size `r`.  Choose any `v in D_Z` with
`H v=y_1`.  Restriction `K_0 -> F^B` is an isomorphism, so there is a
unique `k_B in K_0` with

```text
                         k_B|_B=v|_B.
```

The adjusted vector

```text
                         z_B=v-k_B                        (M11)
```

is a lift of `y_1` which vanishes on `B`.  It has weight at least `d`.
Here `v` is an affine-core direction such as the interpolant in (11); it
need not be the source minimum lift `v_min` and need not have support `J`.
Only the defining inequality `wt(z_B)>=d` consumes the minimum-lift object.
Since the complement of `T` has size at most `N-q`,

```text
wt(z_B|_T)>=d-(N-q)=d+q-N.
```

If this lower bound is nonpositive, `z_B|_T` is nevertheless nonzero:
otherwise a `y_1`-lift and, after subtracting it from `c_gamma`, a
`y_0`-lift would both be supported on `S_gamma`, contradicting
transversality.  Thus at least `ell_q` coordinates
`x in T` outside `B` satisfy `z_B(x)!=0`, and every such `x` extends
`B` to an `s`-row basis `B union {x}` for `D_Z`.

### Step 4: extension multiplicity and unique slope labels

A fixed `s`-subset `I` can arise from at most `s` pairs `(B,x)`, one for
each possible deleted coordinate `x in I`.  Hence every complete mask
contains at least

```text
(ell_q/s) binom(q-kappa+r,r)                              (M12)
```

row bases for `D_Z`, and therefore at least the integer `mu_q` in (M5).
Applying the same count with `q=a_gamma` gives at least the exact integer
`mu_gamma` in (M2a).

By Section 5, each fixed `D_Z`-basis `I` can be
contained in the complete zero mask of at most one selected slope.  Counting
the slope-basis incidences against the universe of `binom(N,s)` coordinate
`s`-sets first proves the nonuniform sum (M2b), and then its uniform
integer-sharp corollary in (M5).  The rational `B_MDS` form is retained for
asymptotic comparisons.

Equivalently, the two-stage proof is the greedy row-flat profile of `D_Z`
itself: its proper flats of dimensions `0,...,r-1` give the factors in
(M8), while the final quotient direction gives `ell_q`.  The two-stage form
is retained because it identifies exactly where MDS generalized weights,
minimum-lift weight, and transversality enter.

For completeness, the equivalent generalized-weight profile of `D_Z` is
direct.  A one-dimensional subcode is generated either by a kernel word of
weight at least `R+1` or by a nonkernel word which normalizes to a
`y_1`-lift of weight at least `d`.  If `E<=D_Z` has dimension `h>=2`,
then either `E<=K` and its support has size at least `R+h`, or
`dim(E intersect K)=h-1` and its support has size at least `R+h-1`.
Thus the row-flat sizes of `D_Z` are bounded by (M7) through dimension
`r-1`, followed by the cap `N-d` at dimension `r`.  Greedy basis
selection gives the same factors (M8) and the final matched factor `ell_q`.

### Supplied values of `q`

For the whole weight-`t` family,

```text
q=N-t>kappa,
ell_q=max(1,d-t).                                         (M13)
```

For one #676 exact interior stratum, use the source minimum lift, its support
`J`, `M=N-d`, and

```text
h_e=max(1,d+e-t),
q_e=M-e+h_e,
ell_e=max(1,d+q_e-N)
     =max(1,h_e-e)
     =max(1,d-t).                                         (M14)
```

The complete zero mask has exactly `M-e` outside zeros and at least `h_e`
inside zeros, so `|T_gamma|>=q_e`.  Moreover `q_e>=N-t>kappa`: if
`d+e-t>=1`, then `q_e=N-t`; otherwise
`q_e=N-d-e+1>=N-t+1`.  Thus (M5) applies with the exact specialized values
`(q_e,ell_e)`.  The exact floor can sharpen the denominator, but the
extension factor simplifies exactly to the coarse value `max(1,d-t)`; no
extra extension gain is claimed from `q_e`.

The same exact stratum supplies a coarse actual-support ceiling for the
set-pair theorem.  A selected witness has `e` nonzeros outside `J` and at
most `d-h_e` nonzeros inside, so

```text
w_Z<=w_e:=e+d-h_e=N-q_e,

B_pair<=binom(s+w_e,s).                                   (M15)
```

The actual maximum `w_Z` can be smaller and should be retained when known.
The safe combined charge is the minimum of this set-pair bound and (M5);
no multiplicative combination of the two counts is asserted.

### Comparison with pinned PR #670

Pinned #670 proves the ambient agreement-weighted inequality

```text
sum_gamma binom(|T_gamma|-1,kappa)
 <=binom(N,kappa+1).                                      (M16)
```

Under the uniform floor `|T_gamma|>=q`, its per-slope multiplicity and
uniform charge are

```text
mu_670=binom(q-1,kappa),

B_670_rat=binom(N,kappa+1)/mu_670,
B_670=floor(B_670_rat).                                   (M17)
```

The exact nonuniform sum (M16) should be retained when the mask sizes vary.
When the actual core fills the ambient kernel, `r=kappa` and
`s=kappa+1`.  Before the ceiling in (M5), the ratio of the two per-slope
multiplicities is

```text
mu_core(gamma)/mu_670(gamma)
 =ell_gamma a_gamma/[s(a_gamma-kappa)],

mu_core/mu_670
 =[(ell_q/s)binom(q,kappa)]/binom(q-1,kappa)
 =ell_q q/[s(q-kappa)].                                   (M18)
```

Thus neither multiplicity generally dominates the other.  At the sharp
`t=R-1` specialization, `q=s=kappa+1` and `ell_q=1`, so they agree
exactly and both recover #528.  The genuinely new axis in (M5) is
`r<kappa`, where the actual-core row-flat profile uses smaller bases and a
different certificate universe.  The safe compiler takes the minimum of
#670 and (M5), along with the other applicable bounds; it does not multiply
their certificate counts.

For `r=kappa`, the corresponding **pre-rounding rational-charge** ratio is
the reciprocal of (M18),

```text
B_MDS/B_670_rat=s(q-kappa)/(ell_q q).
```

No equality between this rational ratio and the ratio of the two floored
integer charges is asserted.  Integer comparisons use `B_670` from (M17)
and the integer-sharp first bound in (M5).

When these parameters scale linearly, this is only a constant-factor
comparison and the two bounds have the same exponential rate.  The set-pair
charge is independent as well: finite comparison finds both orderings
between `B_pair` and #670, so it too remains a separate minimum term.

Realizable finite verifier fixtures witness both directions already at
`F_7`:

```text
K=[6,2,5], t=2, r=2, q=4, d=2, ell_q=1:
  mu_core=2 < mu_670=3;

K=[6,1,6], t=3, r=1, q=3, d=5, ell_q=2:
  mu_core=3 > mu_670=2.
```

The first favors #670 and the second favors the actual-core theorem.

### Sharpness of the basis denominator and scope

The denominator `binom(q-kappa+r,r)` is optimal from ambient MDS generalized
weights alone.  Fix `kappa-r` coordinates and let `K_0` be the
`r`-dimensional shortening of `K` which vanishes on them.  A generator of
`K_0` has those zero rows and is uniform MDS on the remaining coordinates.
A `q`-mask containing all fixed zero coordinates therefore has exactly

```text
                         binom(q-kappa+r,r)
```

`K_0`-row bases.  Any further improvement must use more than the ambient MDS
generalized-weight profile.  This sharpness statement concerns the local
basis multiplicity only; it does not construct an actual syndrome-line slope
family attaining (M5).

The refinement is also compatible with the attained ambient examples behind
#528.  If `r=kappa` and `t=R-1`, then the coarse values are
`q=N-t=kappa+1` and `ell_q=1`, while

```text
binom(q-kappa+r,r)=binom(r+1,r)=s.
```

Formula (M5) therefore collapses exactly to
`binom(N,kappa+1)`.  The new gain comes only from actual
`r<kappa`, extra zero-mask slack `q>kappa+1`, or `ell_q>1`; it does not
contradict the integrated sharp `kappa=1,2` examples.

The set-pair and MDS bounds are genuinely incomparable, so the minimum in
(3a) is load-bearing.  Two admissible parameter-level checks using the coarse
exact support ceiling `w_e` are:

```text
(N,R,kappa,t,d,e,r)=(7,6,1,4,1,4,1):
  B_MDS=14 < B_pair=15;

(N,R,kappa,t,d,e,r)=(6,5,1,1,1,1,1):
  B_pair=3 < B_MDS=6.
```

These rows compare the proved formulas; they are not asserted to realize
actual multi-slope syndrome-line families.  Asymptotically, the
`w_e=o(n)` set-pair regime forces `e=o(n)`, where the pinned #671 split
Cramer count is already subexponential.  The second MDS regime
`t+kappa-r=o(n)` is likewise likely shallow-route overlap with #535.
Thus the new counts provide real finite/exponent diagnostics but do not close
a new linear central-band stratum by themselves.

At the #676 central stress

```text
(N,R,kappa,t,d,e)
 =(500u,275u,225u,150u,250u,75u),
```

the ambient-rank specialization `r=225u=kappa` has the asymptotic base-two
rates

```text
B_MDS:             167.287141,
#670 ambient:      167.287141,
B_pair using w_e:  364.106,
#671 split Cramer: 400.805,
raw support count: 440.645.
```

Thus the MDS rate at `r=kappa` is calibration against #670, not novelty
evidence; only lower-order constants can differ there.  On the same stress
parameters, the actual-core MDS rates for

```text
r/u=25,50,75,100
```

are respectively

```text
45.695, 83.452, 114.033, 137.972 bits/u.
```

Writing `alpha=r/u`, the actual-core leading rate is below #670 for
`alpha<150`, above #670 for `150<alpha<225`, and equal at
`alpha=150,225`.  The final consumer must therefore retain the minimum.  At
`u=1,r=225`, the integer actual-core bound is only `0.309` bits better
than #670, a lower-order rounding gain rather than an exponent gain.

The genuinely new diagnostic axis is consequently `r` well below
`kappa`.  The table is a parameter-level exponent comparison, not an
actual-family construction or a prize payment; the surviving linear central
regime remains exponential.

## 6. Rank-zero and low-rank interpretation

For a nontrivial family `|Z|>=2`, `r=0` means exactly that all selected
witnesses lie on one literal affine pencil

```text
                         c_gamma=u+gamma v.                (24)
```

Then `s=1`, every complete zero mask contains a coordinate on which the
one-dimensional space `<v>` restricts injectively, and (17) gives

```text
                         |Z|<=N.                           (25)
```

For `|Z|<=1`, the direct bound is already sharp and no base pair is chosen.

The invariant `r` measures the affine curvature of the **selected coefficient
vectors inside the kernel**.  It is not automatically a locator degree, a
moving-root count, a C8 certificate, or a proof that the family decomposes
into subexponentially many locator pencils.  Low `r` gives the direct
cardinality charge (17) and nothing more structural unless a separate
consumer lemma supplies that bridge.

## 7. Selector dependence, deletion, and exact-`e` compilation

The theorem is deliberately selector-sensitive.  A slope can admit several
actual completed witnesses, and different choices can produce different
subspaces `D_Z`, `K_0`, and ranks.  The following contracts are safe.

### Fixed global selector

Fix one witness for every slope in the retained family before computing any
rank.  The theorem applies to that selection.  Optionally define

```text
r_*(Z)=min over all global actual witness selectors of dim im(theta_Z). (26)
```

For `|Z|>=2`, applying the theorem to a selector attaining the minimum gives

```text
                         |Z|<=binom(N,r_*(Z)+1).            (27)
```

This optional minimum is a consequence, not an extra uniformity hypothesis.
Conversely, an exponential family forces *every* global selector to have
linear actual rank in the regime described in Section 8.

### First-match deletion

If `Z' subseteq Z` is obtained by deleting slopes and keeps the already
selected witnesses, then zero-extension embeds `E_{Z'}` into `E_Z`; hence

```text
K_0(Z') subseteq K_0(Z),
r(Z')<=r(Z).                                               (28)
```

Nevertheless, the refined theorem should be reapplied to `Z'`: its anchor,
affine span, basis, canonical minors, and perhaps its `s=0` edge case must be
recomputed.  One must not silently reuse an old pivot label or an old equality
`r(Z')=r(Z)`.  Reselecting witnesses after deletion is a different selector
and need not satisfy (28).

### Exact punctured weight

To use the result inside the #671/#676 exact-`e` compiler:

1. fix one selector on the whole actual retained set `Z^circ_lambda`;
2. fix the #671/#676 minimum lift `v_min`, its support `J`, and the existing
   profile data;
3. assign each selected slope once and for all, where `P_J` deletes the
   coordinates in `J`,

   ```text
   e_gamma=wt(P_J(c_gamma));
   ```

4. form `Z^circ_(lambda,e)={gamma:e_gamma=e}`; and
5. restrict the same selector to this subset and recompute its intrinsic
   `D_e`, `K_{0,e}`, `s_e`, and `r_e`.

Then

```text
|Z^circ_(lambda,e)|<=binom(N,s_e)
                   =binom(N,r_e+1)  when its size is at least two. (29)
```

It is not safe to choose mutually incompatible witness selectors separately
for different exact weights while also claiming that every original slope
received one fixed `e` assignment.  The theorem itself needs no `Xi_e` sign:
it may be applied to `Xi_e<0`, `Xi_e=0`, or `Xi_e>0` strata, but only after
the actual selected-witness contract above is met.

The rank theorem also applies directly to the endpoint strata `e=0` and
`e=M`, because it never assumes `0<e<M`.  At the audited `fe8b6ef`
snapshot, the #676 two-block theorem required `0<e<M`; current head
`9ef4cc6` incorporates the separate endpoint repair in Section 7A.  At
`e=M`, the present rank theorem still supplies a payment only when its own
binomial-rank gate holds.

## 7A. Separately proved endpoint repair for the #676 compilation

This subsection records the endpoint repair relative to the pinned
`fe8b6ef` snapshot.  PR #676 later incorporated that repair at
`9ef4cc6`; no additional current-head theorem is imported here.  Keep its
selected completed-witness setup, source minimum lift `v_min`, support `J`,
and

```text
d=wt(v_min),
M=N-d,
h_e=max(1,d+e-t).
```

For bookkeeping only, extend the displayed algebraic expression

```text
Xi_e=d(M-e)^2+M h_e^2-dM^2
```

to `e=0,M`.  The theorem at the audited `fe8b6ef` snapshot was restricted
to `0<e<M`; current head `9ef4cc6` includes these endpoint statements.

### Endpoint `e=0`

Every selected witness vanishes on the entire outside block `U\J`, so its
outside zero mask `X_gamma` is the same fixed `M`-set.  If two slopes also
shared one inside zero coordinate, their difference quotient would be a
`y_1`-lift with more than `M=N-d` zeros, contradicting the minimum-lift
weight `d`.  Hence the inside masks `Y_gamma` are pairwise disjoint.
Transversality and the weight budget give `|Y_gamma|>=h_0`, so

```text
                         |Z_0|<=floor(d/h_0).              (E1)
```

This endpoint always lies on the nonnegative algebraic side, since
`Xi_0=M h_0^2>0`.

### Endpoint `e=M`

Here the outside zero mask is empty.  Every inside zero mask
`Y_gamma subseteq J` has `|Y_gamma|>=h_M`, and two distinct masks satisfy

```text
                         |Y_gamma intersect Y_eta|<=M.    (E2)
```

Indeed every common zero is a zero of their difference quotient, a
`y_1`-lift, which has at most `N-d=M` zeros.  Center the incidence vectors
in the real space `1_d^perp`:

```text
z_gamma=1_(Y_gamma)-(|Y_gamma|/d)1_d.
```

For distinct slopes `gamma,eta`,

```text
<z_gamma,z_eta>
 <=M-h_M^2/d
 =-Xi_M/(Md).                                              (E3)
```

A centered vector is zero only when `Y_gamma=J`.  At most one selected
slope has this mask: two such witnesses would give both a `y_1`-lift and a
`y_0`-lift supported on `U\J`, violating transversality.

If `Xi_M>0`, the nonzero centers have strictly negative pairwise inner
products in dimension `d-1`, so there are at most `d`; a zero center
cannot coexist with another center under the strict inequality.  If
`Xi_M=0`, the right-angle bound gives at most `2(d-1)` nonzero centers,
plus the possible unique zero center.  Uniformly,

```text
Xi_M>=0  =>  |Z_M|<=2d-1.                                 (E4)
```

No endpoint payment is asserted here when `Xi_M<0`; that case can use the
rank theorems only if their own hypotheses and binomial gate hold.

### Literal `<2N^2` compilation

For every interior exact weight `1<=e<=M-1` with `Xi_e>=0`, use the pinned
#676 theorem.  There are at most `M-1<=N-2` such weights.  When `N>=3`,
both of its alternatives are at most `2(N-2)`; when `N=2`, there is no
interior weight.  Combining (E1), the interior theorem, and (E4), and using
`d<=N`, gives the explicit arithmetic

```text
sum_(0<=e<=M, Xi_e>=0) |Z_e|
 <=2(N-2)^2+N+(2N-1)
 =2N^2-5N+7
 <2N^2                                                    (E5)
```

for every `N>=2`.  Thus the advertised polynomial compilation is valid
after this separately audited endpoint lemma is added.  The historical
`fe8b6ef` theorem did not contain it; current `9ef4cc6` does.

## 8. Exact asymptotic gates

For the field-general support/set-pair theorem, define

```text
B_pair(Z)=binom(s+w_Z,s).                                 (30)
```

Its direct-payment gate is

```text
                         log B_pair=o(n).                 (30a)
```

The actual-weight inequality `s+w_Z<=N` is part of Section 5A, not an
extra assumption.  If `N<=n`, either one of

```text
                         s=o(n),
                         w_Z=o(n)                         (31)
```

is sufficient, because

```text
log binom(s+w_Z,s)
 <=min{
      s log(e(s+w_Z)/s),
      w_Z log(e(s+w_Z)/w_Z)
    }=o(n)
```

with the zero-parameter cases interpreted directly.  For nontrivial
families, `s=r+1`, so `r=o(n)` remains one simple sufficient regime.

For the separate MDS multiplicity theorem, define

```text
B_MDS(N,kappa,r,q,d)
 =(s/ell_q) binom(N,s)/binom(q-kappa+r,r),
s=r+1,
ell_q=max(1,d+q-N).                                       (31a)
```

For a nontrivial weighted-RS family the final direct charge is

```text
B_direct=min(B_pair,B_MDS).                               (31b)
```

Thus its exact gate is `log B_direct=o(n)`; in particular either
`log B_pair=o(n)` or

```text
                         log B_MDS=o(n)                   (31c)
```

is a sufficient direct-payment gate.

For every live nontrivial family `|Z|>=2`, (M5) makes `B_MDS>=1`; if the
displayed quantity is smaller than one, the hypotheses themselves rule out
such a family.  Because both direct bounds are at most `binom(N,s)`, the
earlier sufficient condition `r=o(n)` remains valid.

There is a second honest sufficient regime.  If `N=O(n)` and, uniformly,

```text
N-(q-kappa+r)=N-q+kappa-r=o(n),                            (31d)
```

then the logarithm of the binomial ratio in (31a) is `o(n)` by the standard
entropy estimate, while the factor `s/ell_q` is only polynomial.  For the
coarse floor `q=N-t`, condition (31d) reads

```text
                         t+kappa-r=o(n).                   (31e)
```

For the exact floor `q=q_e`, the same condition is

```text
                         w_e+kappa-r=o(n),                 (31f)
```

because `w_e=N-q_e`.

This is a shallow or near-full-actual-core regime and is likely already
routed by the integrated #535 A4/SE2 mechanism.  It is recorded as a precise
consumer overlap, not advertised as closure of the deep central band.  In
particular, when the weight budget and `r` occupy fixed positive normalized
fractions and `q-kappa+r` stays a fixed fraction below `N`, the entropy
difference in (31a) is generally positive.  The multiplicity theorem does
not by itself pay the linear-rank deep interior.

Conversely, if `N=Theta(n)` and `|Z|>=exp(cn)` for a fixed `c>0`, then
(P3) and the intermediate determinant charge force

```text
                         s=Omega(n),
                         w_Z=Omega(n),
                         N-s=Omega(n).                     (32)
```

Indeed either `s=o(n)` or `w_Z=o(n)` makes `log B_pair=o(n)`, while
`binom(N,s)=binom(N,N-s)` rules out `N-s=o(n)`.  In particular
`r=s-1=Omega(n)`.  Because the set-pair and determinant theorems apply to
every fixed actual selector, an exponential actual family forces linear
actual rank and linear maximum selected-witness weight for every global
selector.  Existence of one selector with either parameter sublinear would
already pay the family.

This is a per-family/per-chart charge.  It does not by itself show that the
number of charts or selectors summed by A2 is subexponential.

## 9. Positive-rank common-zero intersection

There is a related but strictly secondary MDS statement.  Let `A subseteq Z`
be any `h` selected slopes, use the restricted fixed selector, and define

```text
K_A=im(theta_A),
r_h=dim K_A,
C(K_A)={x in U:k(x)=0 for every k in K_A}.                 (33)
```

Every common complete-zero coordinate of the `h` witnesses lies in
`C(K_A)`, because every coefficient-map relation is a linear combination of
those witnesses.  For the weighted-RS kernel
`K=[N,kappa,R+1]`, and **only when `r_h>0`**, the MDS generalized weights give

```text
d_(r_h)(K)=N-kappa+r_h=R+r_h.                              (34)
```

Equivalently, this is equality in the generalized Singleton profile for an
MDS code.  Since the support of the particular `r_h`-dimensional subcode
`K_A` has size at least `d_(r_h)(K)`, one obtains

```text
|C(K_A)|<=N-(R+r_h)=kappa-r_h,

|intersection_(gamma in A) T_gamma|<=kappa-r_h.           (35)
```

For a general linear code the honest form is

```text
|C(K_A)|<=N-d_(r_h)(K),                                   (36)
```

again only for positive rank.

### Why rank zero must be separated

There is no `r_h=0` continuation of (35).  For an explicit weighted-RS
example, take `R>=3`, `kappa=1`, `N=R+1`, and `t=1`.  At two distinct
coordinates `i,j`, choose

```text
c_0=e_i,
c_1=e_j,
y_0=H e_i,
y_1=H(e_j-e_i).                                           (37)
```

The two witnesses lie at slopes `0,1`, have weight one, and are transverse:
any two weighted Vandermonde columns are independent, so neither one-point
support spans both `y_0` and `y_1`.  But `E_{\{0,1\}}=0`, hence `r_h=0`, while

```text
                         |T_0 intersect T_1|=N-2=R-1>1=kappa. (38)
```

This is the rank-zero affine-pencil branch, not a violation of (35).

There is also no claimed sharpening of (17) obtained by deleting all of
`C(K_0)` from the minor universe.  At a coordinate of `C(K_0)`, every kernel
basis column vanishes but the affine direction `v` may be nonzero.  An
invertible `(r+1)`-minor of `[B|v]` may therefore use one such coordinate
(though not two).  In particular this note does **not** assert
`binom(N-|C(K_0)|,r+1)`.

## 10. Exact abstract-mask route cut at the #676 stress point

The pairwise two-block geometry of #676 cannot by itself pay its central
band.  Here is the exact probabilistic route cut, included so it is never
mistaken for an RS construction.

Use the positive-integer #676 scale parameter `r_0` (unrelated to the
intrinsic rank `r`) and

```text
(N,R,kappa,t,d)=(500r_0,275r_0,225r_0,150r_0,250r_0),
M=250r_0,
e=75r_0,
h_e=175r_0,
Xi_e=-312500 r_0^3<0.                                    (39)
```

An abstract complete mask at this exact weight consists of a pair `(X,Y)`,
one subset in each `250r_0`-coordinate block, with

```text
                         |X|=|Y|=175r_0.                  (40)
```

The pairwise condition inherited by the #676 proof is

```text
|X_i intersect X_j|+|Y_i intersect Y_j|<=250r_0.          (41)
```

Choose the `X` and `Y` sets independently and uniformly.  For two masks,
each overlap has the hypergeometric law

```text
Hyp(250r_0,175r_0,175r_0),
mean=(175r_0)^2/(250r_0)=122.5r_0.                        (42)
```

Hoeffding's sampling-without-replacement inequality gives the explicit tail

```text
Pr(overlap>125r_0)
 <= exp(-2(2.5r_0)^2/(175r_0))
 = exp(-r_0/14).                                          (43)
```

For the sharp two-block use, expose both overlaps simultaneously.  The
sampling-without-replacement Hoeffding moment-generating-function comparison
tensorizes across the two independent blocks (equivalently, convolve the two
exact hypergeometric laws).  Their sum has mean `245r_0`, so

```text
Pr(a fixed mask pair is incompatible)
 =Pr(overlap_X+overlap_Y>250r_0)
 <=exp(-2(5r_0)^2/(2*175r_0))
 =exp(-r_0/7).                                             (44)
```

Now sample

```text
                         m=floor(exp(r_0/14))              (45)
```

mask pairs independently.  The expected number of incompatible unordered
pairs is strictly less than

```text
binom(m,2) exp(-r_0/7)
 < (1/2)exp(r_0/7-r_0/7)
 =1/2<1.                                                   (46)
```

Hence there exists a family of `floor(exp(r_0/14))` distinct abstract masks
satisfying (40)--(41).  (A duplicate would itself be incompatible, so the
zero-bad-pair outcome is automatically distinct.)  The weaker one-block
union bound from (43) also gives the earlier conservative
`floor(exp(r_0/40))` family.

This is **not a Reed--Solomon counterexample**.  The random masks are not
shown to be zero sets of coefficient vectors on one syndrome line, to obey
completed-Cramer consistency, to have any actual witness selector, or to
satisfy the transverse syndrome equations.  It proves only that pairwise
mask sizes and the two-block cap are insufficient.  If an actual RS family
of this exponential size existed with fixed selected witnesses, (32) would
force its actual affine span and coefficient-map rank to be linear.

## 11. Comparison and credit ledger

1. **Integrated #528 / `ray_compiler_balanced_core`.**  That theorem uses the
   full ambient kernel `K` of dimension `kappa` and charges a slope to a
   nonzero affine completed determinant, giving
   `binom(N,kappa+1)`.  The present proof restricts the same mechanism to the
   actual affine-difference space `D_Z=K_0+<v>` of dimension `r+1`, giving
   `binom(N,r+1)`; the support/set-pair layer charges those minors against
   the actual selected supports, and the separate MDS layer counts how many
   such minors lie in every complete mask.  These are natural rank, support,
   and multiplicity refinements, not replacements or independent novelty
   claims.

2. **Integrated #534 / ambient growth.**  The audit shows that ambient
   `kappa=Theta(n)` genuinely occurs on relevant balanced cores, making the
   ambient determinant count exponential.  The new escape is conditional on
   small *actual selected-witness rank* or support, despite large ambient
   `kappa`; it does not refute or weaken #534.

3. **Integrated #535 / shallow-prefix A4 route.**  Shallow-prefix high-`kappa`
   charts are already paid through A4/SE2 independently of `kappa`.  The
   intended consumer here is only a retained deep-prefix/A4-unavailable
   family, especially an actual `Xi_e<0` stratum.  No duplicate shallow-route
   claim is made.  In particular, the new sufficient regime
   `t+kappa-r=o(n)` is flagged as likely overlap with #535, not sold as a new
   deep-wall closure.

4. **PR #659.**  It supplies the direction-extension generalized weights,
   fixed-mask affine-dimension control, `W3+`, and `J_e=0` payments.  The
   current theorem uses only its literal completed-witness setup in the RS
   specialization and does not supersede those rank-unrestricted branches.

5. **Pinned PR #670.**  Its agreement-weighted theorem is the direct
   multiplicity antecedent: it assigns at least
   `binom(|T_gamma|-1,kappa)` ambient affine-minor certificates per slope and
   proves the exact weighted sum (M16).  The actual-core MDS theorem adds the
   `r<kappa` row-flat axis and minimum-lift extension factor.  Neither
   generally dominates when `r=kappa`, so #670 remains a separate compiler
   input and receives explicit credit rather than being silently subsumed.

6. **Pinned PR #671.**  Its terminal full-mask rigidity uses the full
   `(kappa+1)`-dimensional completed parameter space and its split Cramer count
   pays all sufficiently small `e`, even when actual `r` is large.  The
   present theorem can instead pay linear `e` when actual `r` is small; neither
   statement contains the other.

7. **Pinned PR #676.**  Its `Xi_e>=0` two-block theorem is rank-unrestricted.
   The actual-core theorems are aimed at the named `Xi_e<0` central band and
   require either the field-general rank/support set-pair gate or the MDS
   multiplicity gate.  The abstract route cut above confirms why pairwise
   mask geometry alone does not supply either gate.  Section 7A independently
   repairs the `e=0,M` compilation cases omitted at the audited `fe8b6ef`
   snapshot; current head `9ef4cc6` incorporates them.

## 12. Exact consumer consequence and remaining walls

For a retained completed-witness family, whole or exact-`e`, the
field-general affine-rank/set-pair theorem provides a direct subexponential
slope count when all of the following are true:

1. the family consists of actual slopes on one fixed affine syndrome line;
2. one actual witness per slope has been fixed consistently with the
   first-match/exact-`e` assignment;
3. every selected witness satisfies the weight and transversality clauses
   (4);
4. the kernel minimum distance exceeds `t`; and
5. the actual parameters `s` and `w_Z` satisfy
   `log binom(s+w_Z,s)=o(n)` uniformly over the live families being summed.

Under `N<=n`, either uniform `r=o(n)` on every nontrivial selected family
or uniform `w_Z=o(n)` is a simple sufficient form of item 5.  Failure of
this field-general route means that a surviving exponential family must have
both linear actual rank and linear maximum selected-witness weight for every
global selector.  It does not mean such a family exists.

The MDS multiplicity refinement replaces item 5 by the potentially stronger
gate `log B_MDS=o(n)`, but additionally requires that the kernel be MDS,
`d` be the actual source minimum-lift weight, and one uniform integer
`q>=kappa+1` lower-bound every complete zero mask in the family.  For exact
strata, the selector, `e` assignment, actual `w_Z` or guarded `w_e`,
`q_e`, and `ell_e` must be the matched objects of Sections 7, 5A, and 5B.
Failure of both direct routes in a
deep family leaves linear actual rank and a non-sublinear deficit
`N-q+kappa-r`; it still does not construct such a family.

At an exact profile, the safe compiler may take the minimum of every
independently applicable bound: `B_pair`, the nonuniform actual-core MDS sum
or its integer-sharp uniform charge,
the pinned #670 nonuniform ambient multiplicity charge, the pinned #671 split
Cramer charge, literal support-pattern counts, and the #676 interior or
Section 7A endpoint charges on their `Xi_e>=0` domains.
Each term keeps its own hypotheses.  No multiplicative combination or silent
transfer of selectors, lifts, or endpoint scope is asserted.

Still open and not claimed here:

- the high-actual-rank `Xi_e<0` central band outside both binomial gates;
- a theorem forcing low actual rank from the RS moment/locator structure;
- A2 atlas or selector exhaustiveness and the number of profiles;
- a boundary-equal RC incidence theorem beyond the direct count above;
- an A4 payment on deep-prefix/A4-unavailable families;
- the whole of A6 or A7;
- any deployed finite-row improvement, safe envelope, Grand MCA/List result,
  prize threshold, or stable-TeX statement.

This packet is therefore a conditional exact payment theorem and a precise
localization: after #659/#670/#671/#676, any central-band family not paid by
the new direct charges must retain genuinely high actual affine rank and
support weight, not merely high ambient kernel dimension.
