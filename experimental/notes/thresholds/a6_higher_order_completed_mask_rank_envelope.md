# Higher-order completed-mask core-rank envelope for strict A6 strata

## Status and dependencies

`PROVED`, for the literal completed-witness setup below. This is a narrow A6
successor to PRs #659, #671, and #676 and to the actual selected-witness core
rank packet in PR #681. It adds a high-rank exclusion; it does not prove the
remaining high-rank A6 compiler.

The unconditional result is the forced-overlap theorem (HCM) and its `j=2`
direct compiler. Any use of a separate low-core-rank payment remains
conditional on the corresponding pending theorem.

## Setup

Let `H_U:F^U -> F^R` have weighted Vandermonde columns at `N=R+kappa`
distinct points, so `K=ker H_U` is an `[N,kappa,R+1]` MDS code. Fix

```text
0 <= t < R,
y_1 != 0,
H_U c_gamma = y_0 + gamma y_1,
wt(c_gamma) <= t,
```

for an actual retained first-match family `Z` of distinct slopes. Fix this
witness selector globally before partitioning by the exact punctured weight
`e`. Require each selected witness to be transverse:

```text
{y_0,y_1} is not contained in
H_U(F^{supp(c_gamma)}).
```

Let `v` be a minimum lift of `y_1`, put

```text
d = wt(v),       J = supp(v),
M = N-d,         h_e = max(1,d+e-t),
e = wt(c_gamma restricted to U\J)
```

on one exact-weight stratum. For nonempty `Z`, define the actual selected-core
rank

```text
s = dim span{c_gamma-c_gamma0 : gamma in Z};
```

set `s=0` when `Z` is empty.

## Theorem: higher-order completed-mask envelope

For every integer `j` with `2 <= j <= s`, define

```text
C_{j,e} = (M-(j+1)e)_+ + ((j+1)h_e-jd)_+.
```

Then

```text
C_{j,e} <= kappa-j+1.                                  (HCM_j)
```

Consequently,

```text
C_{j,e} > kappa-j+1  implies  s <= j-1.                (HCM-rank)
```

The range is automatically contained in `2 <= j <= kappa+1`, because the
difference space lies in the `(kappa+1)`-dimensional code `K+<v>`.

### Proof

Write `T_gamma={x:c_gamma(x)=0}`. On `U\J`, every zero mask has size
`M-e`. On `J`, every zero mask has size at least `h_e`: the weight bound gives
`d+e-t`, while transversality supplies at least one zero even when that number
is nonpositive.

For `j+1` selected witnesses, inclusion-exclusion in the two disjoint blocks
gives

```text
|intersection_i T_{gamma_i}| >= C_{j,e}.                (1)
```

If `s>=j`, choose `j+1` witnesses whose `j` anchored differences are
independent, and let `D_j` be their span. Since

```text
H_U(c_{gamma_i}-c_{gamma_0})
  = (gamma_i-gamma_0)y_1,
```

one has `D_j subseteq K+<v>` and `dim D_j=j`.

For `L=K+<v>`, the generalized weights are

```text
d_j(L)=R+j-1,        2 <= j <= kappa+1.                 (2)
```

Indeed, a `j`-space in `L` either lies in `K`, or intersects `K` in a
`(j-1)`-space, so its support has size at least
`d_{j-1}(K)=R+j-1`; generalized Singleton gives the reverse inequality.

Every coordinate in the intersection in (1) vanishes on `D_j`. Hence

```text
|intersection_i T_{gamma_i}|
  <= N-d_j(L)=kappa-j+1.                                (3)
```

Combining (1) and (3) proves (HCM_j).

## The unconditional three-mask compiler

At `j=2`, put

```text
C_{2,e}=(M-3e)_+ + (3h_e-2d)_+.
```

If `C_{2,e}>kappa-1`, then `s<=1`. If `s=0`, distinct slopes and `y_1!=0`
give `|Z|<=1`. If `s=1`, normalize the affine pencil as

```text
c_gamma=a+gamma z,       H_U a=y_0,       H_U z=y_1.
```

Let `G={x:a(x)=z(x)=0}` and `E=U\G`. Every coordinate in `E` vanishes for at
most one slope. Transversality forces every selected witness to have a zero in
`E`, so

```text
|Z| <= |E| <= N.                                         (4)
```

If `d>t`, write `g=|G|`. Since `z` is a lift of `y_1`, `g<=N-d`. Counting the
at least `N-t-g` moving zeros of every selected witness gives

```text
|Z|(N-t-g) <= N-g.
```

The ratio `(N-g)/(N-t-g)` is nondecreasing in `g`, and therefore

```text
|Z| <= floor(d/(d-t)).                                   (5)
```

Equations (4) and (5) are direct realized-family bounds; they require no
abstract mask proxy and are monotone under predecessor deletion.

## A positive-length strict family

For every `r>=1`, take

```text
(N,R,kappa,t,d)=(15r,9r,6r,3r,5r),
M=10r.
```

For every physical exact weight `0<=e<=3r`,

```text
h_e=2r+e,
Xi_e=5r(3e^2-12er+8r^2).
```

Thus the `Xi_e<0` interval is

```text
Xi_e<0  iff  (2-2/sqrt(3))r < e <= 3r.                  (6)
```

The source strict dispatcher uses

```text
q_e=2e-r,
Delta=4r+1,
D_e=min(M,max(Delta,q_e)),
J_e=e^2-2Me+M D_e.
```

It follows that the genuinely strict `W1- union W2-` interval is

```text
10r-sqrt(10r(6r-1)) < e <= 3r,                           (7)
```

or asymptotically

```text
(10-sqrt(60))/15 < e/N <= 1/5.
```

This remains a positive-length, linear-weight interval. More strongly, for
every physical exact weight `0<=e<=3r`,

```text
C_{2,e}=(10r-3e)_+ + (3e-4r)_+
       >= 6r > 6r-1=kappa-1.
```

Therefore every physical exact weight has

```text
s<=1,       |Z|<=floor(5r/(5r-3r))=2.                   (8)
```

On the interval (7), the exact W1-/W2- inequalities place every row in the
strict residual left by #659 and #671, while #676 applies only to
`Xi_e>=0`. The older completed-Cramer count is exponential on any subinterval
with `e/r` bounded away from zero. Hence (8) supplies a genuinely new payment
on the strict interval. It also directly pays the non-strict exact weights,
without mislabeling them as strict.

All physical exact weights on this particular parameter ray are directly
paid. For the one fixed selector, summing the disjoint exact-weight strata
gives the explicit polynomial total

```text
sum_{e=0}^{3r} |Z_e| <= 2(3r+1).                         (9)
```

This does not close A6 for other parameter rays.

## Exact sharpness regression

Over `F_17`, let `K` be an `[15,6,10]` GRS code. Choose a minimum kernel word
supported on ten coordinates and split its support into disjoint five-sets
`J` and `Q`. The restrictions give two weight-five lifts `v` and `z` of the
same nonzero syndrome. Minimum distance proves that the lift weight is exactly
`d=5`.

Splitting `Q=A dotcup B dotcup {p}` with `|A|=|B|=2` produces two explicitly
zero-extended witnesses `c_0,c_1` of weight three with

```text
c_1-c_0=z,       e=3,       Xi_3=-5.
```

Their supports are transverse because the direction syndrome has no lift on
three coordinates. Every other point of the pencil is nonzero on both `A`
and `B`, hence has weight at least four. Exactly two low-weight points occur,
so (8) is locally sharp. This proves local completed-witness nonvacuity, not
primitive first-match survival.

## Source compiler and remaining wall

PR #681 supplies the rank-one pencil bounds `|Z|<=N` and
`|Z|<=floor(d/(d-t))`. The new HCM criterion forces `s<=1`, activating those
existing bounds on the displayed strict ray. They are
`exp(o(n))(1+Nbar_lambda)` payments because `N<=n` and every nonempty realized
image has `Nbar_lambda>=1`.

The exact dispatcher can therefore add:

```text
if Xi_e >= 0:
    use #676;
elif C_{j,e} > kappa-j+1 for some fixed j:
    collapse actual core rank and use the direct payment;
else:
    retain the high-rank higher-order-mask residual.
```

For the canonical stress family

```text
(N,R,kappa,t,d)=(500r,275r,225r,150r,250r),
50r<e<100r,
```

the full higher-order calculation is

```text
C_{2,e} <= 100r,
C_{3,e} <= 50r,
C_{j,e} = 0,       4 <= j <= kappa+1.
```

Every fixed HCM inequality therefore retains linear slack against
`kappa-j+1`. The next theorem must use completed values, realized-image
collisions, predecessor routing, or a genuine all-witness pair-multiplicity
bound, not only complete-mask cardinalities.

## Ownership and nonclaims

PR #659 owns the generalized-weight common-zero cap. PR #681 records the
actual selected-witness core-rank charge, including `|Z|<=binom(N,s)` and the
rank-one `|Z|<=N` bound. PR #671 owns the completed-Cramer
branch, and PR #676 owns the `Xi_e>=0` two-block payment. The new delta here is
the exact two-block forced-overlap lower bound, its combination with the
generalized-weight cap to exclude high actual core rank, and the corrected
strict-ray closure with its sharpness regression. The pencil bounds are reused
from #681 and are not claimed as new.

This note proves no full A6 theorem, witness-exhaustive atlas, image-scale
MI/MA or Sidon payment, profile-envelope target comparison, deployed adjacent
certificate, Grand MCA theorem, Grand List theorem, or prize result. The
official score remains `0/2`.
