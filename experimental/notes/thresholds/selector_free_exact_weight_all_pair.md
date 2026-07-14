# Selector-free exact-weight payment for all LineRay pairs

## Claim

Let `F` be a finite field, let `U subset F` have `N=R+kappa`, with `R>=1`
and `kappa>=1`, and let `H:F^U -> F^R` have nonzero weighted Vandermonde columns.  Thus
`K=ker H` is an `[N,kappa,R+1]` generalized Reed--Solomon code.  Fix
`0<=t<R` and `y_0,y_1 in F^R` with `y_1!=0`.  Let `P` be any finite set of distinct retained transverse pairs
`(gamma,c)` satisfying

```text
H(c)=y_0+gamma y_1,       wt(c)<=t,
{y_0,y_1} not subset span{h_x:x in supp(c)}.              (1)
```

No witness or slope selector is applied to `P`.

Choose a minimum lift `v` of `y_1` and put `d=wt(v)`, `J=supp(v)`,
`I=U\J`, `M=N-d`, and `Delta=R+1-d=M-kappa+1`.           (2)

For `0<=j<=M`, define the complete exact-weight pair stratum and its set of
distinct realized punctured words by

```text
P_j={ (gamma,c) in P : wt(c|_I)=j },
W_j={ c|_I : (gamma,c) in P_j }.                          (3)
```

Set `h_j=max(1,d+j-t)` and
`Xi_j=d(M-j)^2+M h_j^2-dM^2`.                            (4)

Then the completed two-block bounds count every pair:

```text
0<j<M and Xi_j>0   => |P_j|<=N-1,
0<j<M and Xi_j=0   => |P_j|<=2(N-2),
j=0                => |P_0|<=floor(d/h_0),
j=M and Xi_M>=0    => |P_M|<=2d-1.                       (5)
```

The full-weight endpoint uses the actual GRS kernel distance `R+1>t`, not
merely a generic lower bound by `d`.

Consequently, if every occupied exact stratum has `Xi_j>=0`, then

```text
|P| <= 2(M-1)(N-2)+3d-1
    <= 2(N-2)^2+3N-4
     = 2N^2-5N+4
     < 2N^2.                                               (6)
```

There is also a complementary exact realized-word bound.  Put
`D_j=min(M,max(Delta,d+2j-2t))` and `Q_j=M D_j-2Mj+j^2`.  (7)

Whenever `Q_j>0`, one has

```text
|W_j| <= floor(M(D_j-j)/Q_j),

|P_j| <= floor(d/h_j) floor(M(D_j-j)/Q_j).               (8)
```

This second bound also retains every same-slope witness.  It first counts
distinct punctured words and then restores the exact cluster multiplicity.

## Status

`PROVED` under (1)--(2); the fixtures and route cut below are exact, while the accompanying Lean declarations are `UNPROVED STATEMENT TARGETS`.

## Parameters

An occupied stratum automatically has `0<=j<=rho:=min(t,M)`.

The `Xi_j` theorem uses the minimum-lift and transversality hypotheses, and
the same-slope branch uses kernel distance at least `d`.  Its `j=M`
endpoint additionally uses `d(K)=R+1>t`.                    (9)

The `Q_j` theorem additionally uses the punctured GRS distance `Delta`.
There are no hidden constants and no assumption that one error is selected
per slope.

## Existing paper dependency

The public dependencies are:

- `experimental/notes/thresholds/completed_zero_mask_two_block.md` for the
  selected-slope centered two-block argument;
- `experimental/notes/thresholds/low_direction_minimum_lift_puncture.md` for
  the minimum-lift puncture and exact realized clusters;
- `experimental/notes/thresholds/selector_free_direction_distance_all_pair.md`
  for the all-pair different-slope/same-slope distance split; and
- `experimental/notes/thresholds/all_lineray_affine_core_set_pair.md` for the
  complete-pair affine charge used in the route comparison.

The present claim is a fixed-chart residual-ray compiler.  It does not prove
an exhaustive atlas, an image-scale MI+MA or Sidon input, a full target-profile
envelope comparison, or the lower reserve.  It changes no stable paper.

## Proof idea or experiment

### 1. Common-zero cap for all pairs

Take distinct pairs `(gamma,c),(gamma',c') in P`.

If `gamma!=gamma'`, then `(c-c')/(gamma-gamma')` is a lift of `y_1`, so its
weight is at least `d`.

If `gamma=gamma'`, then `c-c'` is a nonzero kernel word, so its weight is at
least `R+1>=d`.

Every common zero of `c` and `c'` is a zero of the corresponding difference.
Thus every two complete zero masks meet in at most `N-d=M` coordinates. (10)
This proves the pairwise hypothesis for all retained pairs,
including repeated slopes.

### 2. Completed two-block estimate

For `(gamma,c) in P_j`, put `X_c={x in I:c_x=0}` and
`Y_c={x in J:c_x=0}`.

Exact punctured weight gives `|X_c|=M-j`.  The weight budget gives at least
`d+j-t` zeros on `J` when this number is positive.  Otherwise transversality
still gives one: if `c` had no zero on `J`, then both `v` and
`c-gamma v` would be supported inside `supp(c)`, contradicting (1).  Hence
`|Y_c|>=h_j`.                                              (11)

Center their indicators in `1_M^perp direct-sum 1_d^perp`, of dimension
`N-2`.

By (10)--(11), distinct centered vectors have inner product at most
`M-(M-j)^2/M-h_j^2/d=-Xi_j/(Md)`.                         (12)

The strict negative-inner-product bound gives `N-1`; the right-angle bound
gives `2(N-2)` on the equality face.  Since (10) held for every pair, these
are bounds for `P_j`, not just its slope projection.

At `j=0`, all `X_c` equal `I`, so the `Y_c` are pairwise disjoint and cost at
most `floor(d/h_0)`.

At `j=M`, the centered `J`-indicator can vanish only when `Y_c=J`.  Distinct
slopes cannot both give this zero center by transversality.  If two same-slope
pairs gave it, both errors would be supported on `I`; their difference would
be a nonzero kernel word supported on at most `M<=t` coordinates, contradicting
`R+1>t`.  The zero center is therefore unique, while the nonzero centers cost
at most `2(d-1)`.  This proves `2d-1`.

The stronger endpoint hypothesis is necessary.  Over `F_37`, let

```text
H(x_1,x_2,x_3,x_4)=(x_1,x_2,x_3+x_4),
y_0=(0,0,0),       y_1=(1,1,0),
v=(1,1,0,0),       d=M=t=2.
```

The `36` vectors `(0,0,a,-a)`, `a in F_37^*`, are distinct same-slope
full-weight errors at `gamma=0`, and `Xi_M=0`, contradicting `2d-1=3`.  Here the kernel
distance is `2`, not `t+1=3`; this is a generic-linear-chart counterexample,
not a weighted-RS counterexample.

### 3. Exact realized-word count

Fix `w in W_j`.  Puncturing `J` is injective on the affine solution space
`H(u)=y_0`, so there is one lift `u_w`, and every pair over `w` has
`c=u_w+gamma v`.                                          (13)

The cluster injects into slopes.  Each member has at least `h_j` zeros on
`J`, while a coordinate of `J` can vanish for at most one slope.  Therefore
`|{(gamma,c) in P_j:c|_I=w}|<=floor(d/h_j)`.              (14)

Choose one pair above each distinct word in `W_j`.  Puncturing a nonzero
kernel difference gives distance at least `Delta`.  Independently, the total
pair distance is at least `d`, while the two `J`-restrictions have combined
weight at most `2(t-j)`.  Thus the punctured distance is at least
`d+2j-2t`, and hence at least `D_j`.

The constant-weight column count for length-`M`, weight-`j` words gives
`|W_j|(M D_j-2Mj+j^2)<=M(D_j-j)`.                         (15)

Division when `Q_j>0`, followed by (14), proves (8).

## Ledger impact

The packet upgrades the completed-mask exact-weight theorem from a selected
witness per slope to the complete `(slope,witness)` object.  On every paid
stratum, same-slope differences are charged by the GRS kernel distance.

The `Q_j` arm additionally pays exact punctured lists when the earlier
whole-list Johnson denominator is nonpositive.  It is genuinely sensitive to
same-slope multiplicity, as the `20r` and small-field fixtures below show.

No claim is made when both `Xi_j<0` and `Q_j<=0`.          (16)

The canonical construction in the route cut shows that this remaining locus
cannot receive a universal chart-only subexponential bound.  That boundary is
an ownership boundary for the profile/atlas inputs, not a counterexample to a
target threshold.

## Constants

### F_7 all-pair equality fixture

Take `q=7`, `N=7`, `R=3`, `kappa=4`, `t=2`, `y_0=(0,1,0)`,
`y_1=(0,0,1)`, `d=3`, `J={4,5,6}`, `I={0,1,2,3}`, and `M=4`.

The complete family contains

```text
(1,(6,1,0,0,0,0,0)),
(2,(3,0,4,0,0,0,0)),
(3,(2,0,0,5,0,0,0)),
(3,(0,6,1,0,0,0,0)),
(4,(0,3,0,4,0,0,0)),
(5,(0,0,6,1,0,0,0)).
```

All six pairs lie at `j=2`; slope `3` occurs twice.  Here `h_2=3`, `Xi_2=0`,
and `|P_2|=6<=2(N-2)=10`.

This is a nonredundant all-pair fixture, not a sharpness claim.  Indices are
zero-based.

### F_5 sharp positive-Q fixture

Take `q=5`, `N=4`, `R=3`, `kappa=1`, `t=2`, `y_0=(1,0,1)`,
`y_1=(0,1,3)`, `v=(0,4,1,0)`, `d=2`, `J={1,2}`, `I={0,3}`, `M=2`, and
`Delta=2`.

The complete family is

```text
(1,(0,0,2,4)),
(2,(4,2,0,0)),
(4,(4,0,2,0)),
(4,(0,2,0,4)).
```

It has four pairs, three slopes, `W_1={(0,4),(4,0)}`, `h_1=1`, `D_1=2`, and
`Q_1=1`.

Both realized-word clusters have size two, and both bounds are sharp:
`|W_1|=2` and `|P_1|=4`.

The predecessor diagnostics are `D_H=-4` and `D_J=0`; the older all-pair
affine cap is `6`.

### Genuine central 500r all-pair family

For `r>=1`, take

```text
(N,R,kappa,t,d)=(500r,275r,225r,150r,250r),
M=250r,       Delta=25r+1.
```

Then

```text
Xi_j=500r(j-50r)(j-100r).                                 (17)
```

The intervals

```text
15r<=j<=50r       or       100r<=j<=111r
```

have `Xi_j>=0`, with equality exactly at `50r` and `100r`.  Their complete
all-pair contribution is at most

```text
46r(500r-1)+2(1000r-4)=23000r^2+1954r-8.                 (18)
```

This arithmetic occurs in genuine weighted-RS geometry.  Let `|F|>=500r`,
choose `U subset F`, use the standard weighted-polynomial description

```text
K={(omega_x p(x))_(x in U):deg p<225r},
```

and choose `I subset U` of size `250r`.  Put

```text
f(X)=product_(x in I)(X-x),       v_x=omega_x f(x).
```

Every lift in the coset of `v` retains the degree-`250r` leading term, so it
has at most `250r` zeros.  Hence `J=U\I` and `d=250r` exactly.

Now choose a degree-`200r` polynomial `p` with exactly `152r` roots in `I`
and `48r` roots in `J`.  The kernel word `z=omega p` has support sizes

```text
|supp(z) intersect I|=98r,
|supp(z) intersect J|=202r.
```

Partition both support blocks evenly.  On one `49r+101r` half set `c=z` and
`c'=0`; on the other half set `c=0` and `c'=-z`.  Then

```text
c-c'=z in K,
wt(c)=wt(c')=150r,
wt(c|_I)=wt(c'|_I)=49r.
```

Set `gamma=0` and `y_0=H(c)=H(c')`.  Since `t<d`, both witnesses are
transverse.  Thus this is an actual two-pair same-slope stratum with

```text
Xi_(49r)=25500r^3>0.
```

### Genuine 20r multiplicity calibration

For `r>=1`, take

```text
(N,R,kappa,t,d,M,Delta,j)
 =(20r,11r,9r,6r,10r,10r,r+1,5r).
```

Then

```text
h_j=9r,       D_j=8r,       Q_j=5r^2,
|W_j|<=6,     |P_j|<=6,
D_H=-4r^2,    D_J=-74r^2+10r<0.                           (19)
```

For `|F|>=20r`, choose a degree-`10r` minimum-lift polynomial with exactly
the `10r` roots in `I`, so `J=supp(v)` and `d=10r`.  Choose a minimum kernel
word `z` supported on all of `I` and on a set `L subset J` of size `r+1`;
this is obtained from a degree-`9r-1` polynomial vanishing on the complement.

Partition `I=A disjoint-union A'` with `|A|=|A'|=5r`, and choose distinct
`a,b in L`.  Define `c-c'=z` as follows:

- on `A`, put `c=z` and `c'=0`;
- on `A'`, put `c=0` and `c'=-z`;
- at `a`, put `c_a=0` and `c'_a=-z_a`;
- at `b`, put `c_b=z_b` and `c'_b=0`; and
- for `x in L\{a,b}`, choose `alpha_x notin {0,z_x}` and put
  `c_x=alpha_x`, `c'_x=alpha_x-z_x`.

The field-size hypothesis supplies the required overlap values.  Both errors
have five-r punctured and `r` on-`J` nonzeros, so

```text
wt(c)=wt(c')=6r,       wt(c|_I)=wt(c'|_I)=5r.
```

Set `gamma=0` and `y_0=H(c)=H(c')`.  Since `t<d`, both pairs are transverse.
This proves genuine same-slope multiplicity on the positive-`Q` ray.

### Selector-complete 90m formula calibration

For `(N,R,kappa,t,d,M,Delta)=(90m,86m,4m,31m,50m,40m,36m+1)`, every
admissible exact weight has `Q_j>=81m^2`, and summing (8) gives
`|P|<=112m+2`.

Here `D_H=-119m^2` and `D_J=m(40-79m)<0`.  This is a formula calibration,
not a multiplicity example: `2t=62m<R+1=86m+1`, so two weight-`t` errors at
one slope cannot differ by a nonzero kernel word.

### Exact R=t+1 route cut

Let `t>=2`, `kappa>=1`,

```text
N=t+kappa+1,       R=t+1,
```

and take the canonical moment columns

```text
h_a=(1,a,...,a^t)^T,       a in U,
```

over a field containing the `N` distinct points of `U`.  Put

```text
y_0=e_(t-1),       y_1=e_t.
```

For every `t`-set `S subset U`, let

```text
Q_S(X)=product_(a in S)(X-a),
c_S(a)=1/Q'_S(a) for a in S,       c_S(a)=0 otherwise.
```

Lagrange coefficient extraction gives

```text
H(c_S)=y_0+(sum_(a in S)a)y_1.                             (20)
```

The monic `Q_S` functional proves `y_1 notin V_S`, so every pair is
transverse.  A monic degree-`t-1` polynomial vanishing on a smaller support
would evaluate to `1` on `y_0+gamma y_1`, proving that no pair has weight
below `t`.  Hence the complete family is exactly

```text
|P|=binom(N,t).                                            (21)
```

For this family,

```text
d=t+1,       M=kappa,       Delta=1,
D_H=1-kappa(t-1)<=0,
D_J=kappa(1-2rho)+rho^2<=0,       rho=min(t,kappa).         (22)
```

On the symmetric even subfamily `t=kappa` and at `j=t/2`,

```text
h_j=j+1,       D_j=1,
Q_j=t-3t^2/4<0,
Xi_j=-t^3/2+t^2/4+t<0,                                   (23)

|P_j|=binom(t,t/2) binom(t+1,t/2),
```

which is exponential in `t`.  The affine-core charge has
`s=kappa+1=t+1` and is sharp:

```text
binom(s+t,s)=binom(2t+1,t)=binom(N,t).
```

The realized punctured affine rank is `kappa=t`.  Thus neither exact-weight
denominator can yield a universal chart-only subexponential theorem on this
locus.  This is an ownership boundary for atlas/profile structure, not a
target-threshold counterexample.

## Reproducibility

The verifier and pinned certificate are

```text
experimental/scripts/verify_selector_free_exact_weight_all_pair.py
experimental/data/certificates/selector-free-exact-weight-all-pair/selector_free_exact_weight_all_pair.json
```

Run

```bash
python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --summary-only
python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --check
python3 experimental/scripts/verify_selector_free_exact_weight_all_pair.py --tamper-selftest
python3 -O experimental/scripts/verify_selector_free_exact_weight_all_pair.py --check
python3 -O experimental/scripts/verify_selector_free_exact_weight_all_pair.py --tamper-selftest
python3 -m json.tool experimental/data/certificates/selector-free-exact-weight-all-pair/selector_free_exact_weight_all_pair.json
```

The exhaustive sweep covers `q in {2,3,5}`, every enumerated `N<=q`, all
admissible `R,t,y_0`, and normalized nonzero `y_1`.  It retains same-slope
pairs.  The pinned totals are

```text
414250 parameter rows,
209846 nonempty complete families,
310632 exact-weight strata,
222106 positive-Q strata,
0 violations.
```

The `F_7` equality fixture is checked separately.  The certificate pins base

```text
9262f63cf093a7510a2df435f220390f59e2bcd5.
```

The statement-only Lean target is

```text
experimental/lean/grande_finale/GrandeFinale/ExactWeightAllPairs.lean
```

and may be typechecked narrowly with

```bash
lake env lean experimental/lean/grande_finale/GrandeFinale/ExactWeightAllPairs.lean
```

This checks declarations and types; it does not certify the unproved target
theorems.
