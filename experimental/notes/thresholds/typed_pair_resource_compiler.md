# Typed pair-resource occupancy compiler for an M31 max-fibre ledger

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED resource partition and occupancy inequalities;
CONDITIONAL finite-row ledger.

## Finite combinatorial setting

Work on a 1023-point punctured dyadic domain with 32 outer fibres: 31 have
size 32 and one has size 31.  Every full outer fibre is partitioned into
four eight-point inner blocks.  The punctured outer fibre has three
eight-point inner blocks and one seven-point punctured block.

Let `S` be a 64-point support in the residual class under consideration.
Write `s_y` for its occupancy in outer fibre `y`, let `h(S)` be the number
of occupied outer fibres, and let `c(S)` count selected complete eight-point
inner blocks.  The compiler below is for the explicitly stated range

```text
3<=h(S)<=17,  0<=c(S)<=4.
```

## Resource partition

The supportwise pair resource is

```text
rho(S)=sum_y binom(s_y,2)-28c(S).                    (1)
```

The number of same-outer-fibre pairs in the punctured domain is

```text
31 binom(32,2)+binom(31,2)=15841.
```

These resources split canonically as

```text
inter-inner-block pairs:                            12264
internal pairs in the permanently punctured block:    21
base resources:                                     12285
internal pairs in 127 complete-available blocks:     3556
total resources:                                    15841.
```

The last 3556 pairs contribute to (1) whenever their block is only
partially selected.  They cannot be omitted from the global double count.
For example, one complete block and eight seven-point partial blocks give
`rho=168`, all of it from partial-block pairs.

Let `b(S)` and `p(S)` denote the base and partial contributions.  Then

```text
b(S)+p(S)=rho(S).                                    (2)
```

## External weights and occupancy inequalities

The compiler takes the following explicit external weight table as input:

```text
B3=3432; B4=B5=1716; B6=B7=792; B8=B9=330;
B10=B11=120; B12=B13=36; B14=B15=8; B16=B17=1.
```

For a fixed prefix `z`, let `q_z(S)` be any nonnegative support
contribution satisfying

```text
q_z(S)<=B_(h(S)).
```

The following inequalities are therefore statements about the displayed
weight table; no locator-realizability claim is hidden in their definition.
The exact supportwise equal-price inequality is

```text
q_z(S) <= (858/133)(b(S)+p(S)).                      (3)
```

A sharper typed inequality is

```text
q_z(S) <= (2244/599)b(S)+(45342/599)p(S).            (4)
```

To verify (4), decompose each outer fibre into four inner occupancies.  For
a full fibre with occupancies `(t0,t1,t2,t3)`, define

```text
b=binom(sum ti,2)-sum_i binom(ti,2),
p=sum_(i:ti<8) binom(ti,2).
```

In the punctured outer fibre, allow `t0<=7` and move `binom(t0,2)` from the
partial to the base count.  Exact dynamic programming over the stated
64-point occupancy space checks (4) against the displayed weights.  Equality
occurs only at

```text
(h,c,b,p)=(5,4,256,10), (7,4,171,2).
```

For a support family `F_z`, define `Delta_base` as the maximum number of
members of `F_z` charging one base pair, and define `Delta_partial`
analogously for a partial-block pair.  Summing (3) over `F_z` and exchanging
the support-pair incidences gives

```text
W_(>=32)(z)
 <= floor((858/133)(12285 Delta_base+3556 Delta_partial)).   (5)
```

Equation (4) gives the analogous two-price bound.  At `(21,2)` it is

```text
floor(901390644/599)=1504825.
```

The two realized equality profiles force

```text
256 alpha+10 beta >=1716,
171 alpha+ 2 beta >= 792.
```

Their intersection is `(alpha,beta)=(2244/599,45342/599)`.  Nonnegative
dual multipliers `350091/599` and `379589/599` reproduce the objective
coefficients `12285*21` and `3556*2`, certifying optimality for that typed
point among linear two-price compilers.

## Mixed-mass-eight owner lemma

Let `theta` be monic of degree eight.  Call a monic degree-eight polynomial
`G` *mixed* when it is not a complete `theta`-fibre locator.  Equivalently,
write uniquely

```text
G=theta+D0+g,  D0 in X F[X],  deg D0<=7;
```

then mixed means `D0` is nonzero.

Let `G,G'` be mixed and let `P,P'` be monic degree-seven polynomials.  If
`G P(theta)` and `G' P'(theta)` share their first 31 nonleading
coefficients, then

```text
G=G',  deg(P-P')<=3.                                 (6)
```

Indeed, equal prefixes give product difference degree at most 32.  The first
seven coefficients identify the nonconstant remainder `D0` of `G` and
`G'`.  Writing `Q=P-P'`, the difference is

```text
A(theta)+D0 Q(theta).
```

The ring `F[X]` is a free `F[theta]`-module with basis
`1,X,...,X^7`; different lanes have different leading degrees modulo eight.
If `deg Q>=4`, a nonzero lane of `D0 Q(theta)` has degree at least 33,
contradicting the cutoff.  Thus `deg Q<=3`.  Unequal constants in `G,G'`
would leave a scalar-lane term of degree 56, so the constants and hence the
owners agree.

Conditional on the separate block-free seven-subset three-moment theorem,
(6) leaves one mixed-mass-eight support per prefix.  With external quotient
weight 3432, that layer contributes at most 3432.

## M31 adjacent-row transfer cap

For the deployed parameters

```text
n=2097152,  m=1116023,  B*=16777215,
```

marked-point deletion gives

```text
(m+1) M_(m+1) <= n M_m.
```

Thus the largest integer list max-fibre cap that transfers inside the
adjacent MCA budget is

```text
C=floor(B*(m+1)/n)=8928191.
```

The integer `C` is a max-fibre transfer cap.  It is not the global M31 v3
budget `B*`.

## Refined conditional closing point

Assume the following already-paid inputs in this max-fibre decomposition:

```text
complete T8:       3866016
canonical T16:      216216
mixed mass 8:         3432
mixed mass 16:       68640
mixed mass 24:     3012372
```

Their paid total is `7166676`, leaving inside `C`

```text
C-7166676=1761515.                                    (7)
```

Consequently the global hypotheses

```text
Delta_base<=21,  Delta_partial<=4                    (8)
```

would pay the residual tail, because (5) gives

```text
floor((858/133)(12285*21+3556*4))
  =1756055 <=1761515,
```

with slack 5460.

## Reproduction and scope

Run the eight Python verifiers listed in the certificate README.  They use
exact integer or rational arithmetic and record the occupancy minima,
primal-dual certificate, owner degree calculation, and ledger propagation.

The inequalities in (8) and the five displayed paid inputs remain
hypotheses of the finite ledger.  This package does not prove arbitrary
varying-owner collinearity, pay opposite-pair carrier pencils, or close a
deployed row globally.
