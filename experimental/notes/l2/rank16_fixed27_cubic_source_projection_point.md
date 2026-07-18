# Rank-16 fixed-27 cubic source-projection point

Claim: Conditional on the exact theorem content of PR #892 at
`d4a33c87ac3e3e1a5078b88fddf085cb6536b75e` and PR #904 at
`213c4ebdebf28c0bd92aa47f293f0138b034037b`, one literal fixed-27,
affine-rank-two cubic source cell has a rational coefficient-curve point
`P_*` with

```text
X^B in F_p(C),       k | B,       mult_(P_*) C = (r-B)/k.
```

Here `C` is the integral coefficient curve, `k` is the generic degree of its
source parametrization, and `r=d-c`.  The resulting additional plane-curve
delta charge proves the conditional local floors

```text
c = 18,619  =>  |U| >= 246,937,
c = 18,618  =>  |U| >= 246,938.
```

In particular, the assigned endpoint `(c,|U|,k)=(18,619,230,415,2)` does
not exist in this source cell.  Neither displayed floor is asserted to be
attained.

Status: PROVED, CONDITIONAL, FINITE, LOCAL.  The parent charge, global ledger
charge, asymptotic charge, Grand MCA charge, Grand List charge, and official
score charge are all zero.  The official score remains `0/2`.

Verifier:
`experimental/scripts/verify_rank16_fixed27_cubic_source_projection_point.py`
checks the exact source pins, deployed arithmetic, boundary rows, output
transcript, package hashes, and semantic mutations.  The verifier is an
arithmetic replay; the algebraic proof is below.

## Frozen source object

The publication base is
`origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.  Work over

```text
p = 2,130,706,433 = 127*2^24+1,
H = mu_(2^21) in F_p^x,
B = 32,768,
d = 63,601,
w = 28,897.
```

Fix one literal fixed-27 source cell produced by the source compiler: one
27-label core, one root-free monic generator, one syndrome projective ray,
one normalized affine-rank-two cell, and seven distinct valid labels.  All
selected/core-fibre, complete-fibre, squarefreeness, splitting, denominator,
and first-source-cell filters of PR #892 remain hypotheses.

Let `R(X,Y)` be the quadratic residual-specialization polynomial supplied by
PR #892.  Its exact common Base has size `c` and polynomial

```text
Gamma(X) = product_(x in Base) (X-x).
```

PR #892 proves exact division by `Gamma`.  Write

```text
R(X,Y) = Gamma(X) F(X,Y),
F(X,Y) = F_0(X) + F_1(X)Y + F_2(X)Y^2.
```

The quotient is `F=R/Gamma`; it is not multiplication by `Gamma`.  For each
actual label `y_i`, the specialization `F(X,y_i)` is a nonzero scalar multiple
of the Base-cancelled residual.  The map

```text
Phi : P^1_X -> C subset P^2,
      X |-> [F_0(X):F_1(X):F_2(X)]
```

is basepoint-free and nondegenerate, and its image `C` is integral and
rational.  If `k` is the generic degree of `Phi`, `m=deg C`, and
`r=d-c`, then

```text
r = k m.
```

These facts, including linear independence of `F_0,F_1,F_2`, are consumed
from the exact PR #892/#904 content.  They are not conclusions about seven
abstract support sets.

## The source-projection point

Let `P_j=F_p[Y]_(<=j)`.  The primitive cubic source syzygy supplies linearly
independent

```text
a_0,a_1,a_2 in P_3,
deg a_0 = 3,
gcd(a_0,a_1,a_2) = 1.
```

Thus `V=span{a_0,a_1,a_2}` is a hyperplane in `P_3`.  Choose a nonzero
functional `lambda:P_3->F_p` with kernel `V`.  On `P_2`, define

```text
L_0(q) = lambda(q),
L_1(q) = lambda(Yq).
```

The two forms are independent.  First, `L_0` cannot vanish identically:
otherwise `P_2` would be contained in `V`; equality would follow from the
dimensions, contradicting the presence in `V` of the cubic `a_0`.  Now
suppose `alpha L_0+beta L_1=0`.  If `beta=0`, then `alpha=0`.  If
`beta!=0`, then every polynomial in

```text
(alpha+beta Y) P_2
```

lies in `ker lambda=V`.  Both spaces have dimension three, so they are equal.
Every element of `V`, hence each `a_j`, would have the common linear factor
`alpha+beta Y`, contradicting `gcd(a_0,a_1,a_2)=1`.

The two independent lines `L_0=L_1=0` meet in one rational point
`P_* in P^2(F_p)`.

## Function-field identity

Put `T=X^B`.  The source identity is

```text
N(X,Y) = (T-Y) R(X,Y).
```

Every coefficient of `N` in `Y` belongs to `V=ker lambda`.  Apply `lambda`
in the `Y` variable, divide the exact nonzero factor `Gamma`, and use the
definitions of `L_0,L_1`:

```text
0 = T L_0(F) - L_1(F),
L_1(F) = X^B L_0(F).                         (1)
```

The sign in (1) is load-bearing.  Set `u=L_0(F)` and `v=L_1(F)`.  The
polynomial `u` is nonzero; otherwise (1) gives `u=v=0` and the nondegenerate
image would collapse to `P_*`.  On `C`, equation (1) therefore gives

```text
v/u = X^B.
```

Consequently

```text
F_p(X^B) subset F_p(C) subset F_p(X).
```

The extension `F_p(X)/F_p(X^B)` has degree `B` and is separable because
`p` does not divide `B`.  The generic map degree is
`[F_p(X):F_p(C)]=k`, so the tower law proves `k|B`.  The already consumed
identity `r=k deg(C)` also gives `k|r`.

## Exact multiplicity

Homogenize `u` and `v` as degree-`r` pullbacks of the two lines through
`P_*`.  Equation (1) has the exact form

```text
U_h = Z^B Q_h,
V_h = X^B Q_h,
```

where `Q_h` is homogeneous of degree `r-B`.  Since `X` and `Z` are coprime,
the homogeneous gcd has exact degree `r-B`, including any contribution at
infinity.  The common pullback divisor is precisely the pullback of the point
`P_*`.  Its degree is `k mult_(P_*) C`.  Hence

```text
k mult_(P_*) C = r-B,
mult_(P_*) C = (r-B)/k.                       (2)
```

At `c=18,619`, one has `r=44,982` and
`gcd(r,B)=2`, so `k in {1,2}`.  Formula (2) gives multiplicity `12,214`
for `k=1` and `6,107` for `k=2`.

This point is new relative to the PR #904 charge atlas.  The exact
multiplicity intervals are

```text
c=18,619, k=1:  pair cap 10,278 < 12,214 < root floor 22,490,
c=18,619, k=2:  pair cap  5,139 <  6,107 < root floor 11,245,
c=18,618, k=1:  pair cap 10,279 < 12,215 < root floor 22,489.
```

Thus `P_*` is neither a selected pair point nor a coefficient-root point.
Its plane-singularity delta floor is additional to the PR #904 charges:

```text
binom(12,214,2) = 74,584,791,
binom( 6,107,2) = 18,644,671,
binom(12,215,2) = 74,597,005.
```

## Exact genus replay

For one row `(c,k,U)`, put

```text
r = d-c,
m = r/k,
E = 7d-6c-U,
N = E/k.
```

PR #904 supplies 21 selected pair points.  If `N=21q+s` with
`0<=s<21`, their balanced delta floor is

```text
D_pair = 21 binom(q,2) + s q.
```

The exact coefficient-root charges consumed from PR #904 are

```text
D_root(18,619,1) = 758,711,395,
D_root(18,619,2) = 189,669,415,
D_root(18,618,1) = 758,711,395.
```

The new charge is

```text
D_* = binom((r-B)/k,2),
```

and the arithmetic genus is `p_a(C)=binom(m-1,2)`.

At the assigned endpoint `(18,619,2,230,415)`, these formulas give

```text
r=44,982, m=22,491, E=103,078, N=51,539,
D_pair=63,218,721,
D_root=189,669,415,
p_a(C)=252,888,805,
old shortfall=669,
D_*=18,644,671,
new excess=18,644,002.
```

The strict positive excess excludes the endpoint.  The complete strengthened
boundary replay is

| `c` | `k` | Last excluded `U` | Excess | First row not excluded | Shortfall |
|---:|---:|---:|---:|---:|---:|
| 18,619 | 1 | 246,939 | 1,529 | 246,940 | 2,592 |
| 18,619 | 2 | 246,935 | 591 | 246,937 | 1,469 |
| 18,618 | 1 | 246,937 | 1,730 | 246,938 | 2,391 |

For `c=18,619,k=2`, integrality of `N=(333,493-U)/2` forces `U` odd, so
the intermediate value `246,936` is inadmissible.  Combining the two possible
degrees yields `U>=246,937`.  The first row not excluded has shortfall
`1,469`; the next exact delta requirement is therefore `1,470`.  At
`c=18,618`, the next exact delta requirement is `2,392`.

## Exact remaining wall and nonclaims

The result is conditional on the exact PR #892 and #904 theorem-bearing
content.  A change to either source normalization or theorem identity requires
repinning and re-audit.

This note does not prove:

- existence of a source-valid witness at either displayed floor;
- the fixed-27 cubic cap-six theorem or any statement for `c<=18,617`;
- a quartic, fixed-26, other-rank, or other-source-cell conclusion;
- a global first-match owner, same-word owner-deficit theorem, cross-cell
  disjointness atlas, or add-back;
- a recurrence parent, asymptotic theorem, Grand MCA row, Grand List row, or
  either official prize statement.

It does not multiply this local theorem over generators, cores, rays,
syndromes, source cells, or profiles.  It does not assert that the first row
not excluded is realizable.  The exact local remaining wall is the missing
`1,470` delta units at `c=18,619,U=246,937`, followed by all lower Base layers
and the global ownership/add-back problem.  The official score remains `0/2`.
