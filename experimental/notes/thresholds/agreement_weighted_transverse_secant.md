# Agreement-weighted transverse-secant payment

## Status

`PROVED`.  The theorem strengthens the one-minor-per-slope residual-kernel
bound on any actual retained weighted-RS chart.  It pays fixed low-excess
charts, including the rank-two two-excess fallback after C5.  It does not prove
a witness-exhaustive C1--C8 atlas or a subexponential cover of all residual
supports.

## Setup

Let `H_U:F^U -> F^R` be a weighted Reed--Solomon parity-check restriction,
with `|U|=R+kappa` and `kappa>=1`.  Let `Z` be any set of retained finite
slopes such that each `gamma in Z` has a selected error vector `e_gamma` with

```text
H_U e_gamma = y_0 + gamma y_1,
wt(e_gamma) <= t < R,
{y_0,y_1} not_subseteq V_supp(e_gamma).
```

Put `A_gamma=U\supp(e_gamma)`.

## Theorem

The exact agreement-weighted inequality is

```text
sum_{gamma in Z} binom(|A_gamma|-1,kappa)
    <= binom(R+kappa,kappa+1).                           (1)
```

In particular,

```text
|Z| <= floor(
  binom(R+kappa,kappa+1) /
  binom(R+kappa-t-1,kappa)).                            (2)
```

The result is monotone under arbitrary earlier first-match deletion.

## Proof

Choose lifts `b_0,b_1 in F^U` of `y_0,y_1` and an `|U| x kappa`
kernel generator `G` for `ker H_U`.  Every `kappa x kappa` row minor of `G`
is nonzero: otherwise a nonzero kernel word would be supported on at most `R`
coordinates, contradicting the MDS parity-column property.

We first record a full-spark minor lemma.  If `S` has size at least
`kappa+1`, every `kappa`-row minor of `G_S` is nonzero, and
`b notin col(G_S)`, then at least `binom(|S|-1,kappa)` of the augmented
`(kappa+1)`-row minors `det[G_T|b_T]` are nonzero.  Induct on `|S|`.
At most one coordinate deletion can put the restricted `b` in the restricted
column space; two such deletions would agree on at least `kappa` full-spark
rows and glue to `b in col(G_S)`.  Double-counting the good deletions gives
the stated binomial lower bound.  The lemma is sharp when `b` differs from a
column-space vector in exactly one coordinate.

For a selected slope write

```text
e_gamma = b_0 + gamma b_1 + G c_gamma,
S_gamma = A_gamma.
```

Transversality implies that at least one of `b_0,S_gamma` and
`b_1,S_gamma` is outside `col(G_S_gamma)`.  The lemma therefore supplies at
least `binom(|S_gamma|-1,kappa)` subsets `T subseteq S_gamma`,
`|T|=kappa+1`, for which

```text
Delta_T(X)=det[G_T | b_0,T + X b_1,T]
```

is a nonzero affine polynomial.  Since `e_gamma` vanishes on `T`, one has
`Delta_T(gamma)=0`.  A fixed nonzero affine `Delta_T` has at most one root,
so each `T` certifies at most one retained slope.  Double-counting these
certificates proves (1).  Since `|A_gamma|>=R+kappa-t`, division by the
minimum per-slope contribution proves (2).

## Rank-one and two-excess corollaries

If `rank[y_0 y_1]=1`, transversality permits at most one finite bad slope:
writing `y_0=alpha z`, `y_1=beta z`, every bad slope must satisfy
`alpha+gamma beta=0`.

After proper-field C5 removal, fix an actual field-full, syndrome-rank-two
chart whose discrepancy support is contained in one set `U` of size `R+2`.
With `kappa=2` and `t=n-a`, (2) gives

```text
|Z^circ_{8,U} intersect Gamma|
 <= min(|Gamma|,
        floor(binom(R+2,3)/binom(a-k+1,2))).             (3)
```

This is polynomial and therefore directly pays every fixed chart and every
subexponential ordered family of such charts.

## Exact remaining wall

Enumerating all `(R+2)`-support charts can itself be exponential.  The missing
A2 input is a literal witness-exhaustive atlas, or a theorem that the actual
post-C7 residual support family has a subexponential low-excess shadow cover.
No such atlas or cover is inferred here.  The theorem proves no full A2, A4,
A6, A7, finite deployed certificate, or prize closure.
