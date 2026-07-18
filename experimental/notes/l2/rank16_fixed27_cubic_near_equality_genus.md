# Fixed-27 cubic near-equality genus exclusion

## Status and dependency

This note proves a finite local theorem conditional on the exact source setup
and results of PR #892 at head
`d4a33c87ac3e3e1a5078b88fddf085cb6536b75e`.  The base repository snapshot is
`origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

The theorem is confined to one literal fixed-27, affine-rank-two cubic source
cell.  Nothing in this note is charged to a global owner, recurrence parent,
Grand MCA ledger, Grand List ledger, or official score.

## Theorem

Use the deployed constants

```text
p = 2,130,706,433,  |H| = 2^21,  B = 32,768,
a = 67,472,         d = 63,601,  w = 28,897.
```

Fix all literal hypotheses of PR #892: one fixed 27-label core, one root-free
monic generator `g`, one syndrome representative/projective ray, one normalized
source cell, and seven distinct valid labels.  Retain monicity, squarefreeness,
complete splitting over `H`, selected/core-fibre avoidance, the no-extra-q64-
fibre condition, and the literal denominator conditions.

Let `U` be the union of the seven original residual `H`-root sets, including
their exact common Base, and let `c = |Base|`.  Then

```text
c = 18,619  implies  |U| >= 230,415,
c = 18,618  implies  |U| >= 230,415.
```

The improvements over the PR #892 local floors are respectively

```text
230,415 - 176,056 = 54,359,
230,415 - 176,059 = 54,356.
```

The number `230,415` is the first value not excluded by this argument.  It is
not an asserted witness.

## 1. Exact cancellation and the coefficient curve

PR #892 gives a common Base polynomial `Gamma` with

```text
Gamma | h,  Gamma | R_i,  Gamma | W_i.
```

After dividing by `Gamma`, the literal source equations remain

```text
(X^B - y_i) Rbar_i = q_i hbar + g Wbar_i.
```

The residual specialization is

```text
F(X,Y) = R(X,Y)/Gamma(X) = F_0(X) + F_1(X)Y + F_2(X)Y^2,
F(X,y_i) = a_0(y_i) q_i^(-1) Rbar_i(X).
```

Every `Rbar_i` is squarefree, split over `H`, and has degree `r=d-c`.  The
three coefficient polynomials have no common affine zero: a common zero would
be a common root of all seven split residuals and hence an uncancelled common
`H`-root.  There is no base point at infinity because every displayed
specialization has degree exactly `r` with nonzero leading coefficient.

The coefficients are linearly independent.  A dependence would give a
nonzero polynomial `b` of `T`-degree at most two with the PR #892 remainder
`Phi_b` equal to zero, contrary to its nonzero-conductor theorem.  Homogenizing
therefore gives a basepoint-free nondegenerate map

```text
Phi : P^1_X -> P^2,    X |-> [F_0(X):F_1(X):F_2(X)].
```

Let `C` be the integral image, `k` the generic degree onto its normalization,
and `m=deg C`.  Since the pullback of a generic line has degree `r`,

```text
r = k m.
```

The map is separable because `r < p`, and the normalization of `C` is
rational.

## 2. Pair points and their delta charge

For each selected label put

```text
L_y : Z_0 + y Z_1 + y^2 Z_2 = 0.
```

The pullback of `L_{y_i}` is the simple zero divisor of `Rbar_i`.  The
Vandermonde determinant shows that the seven selected lines have 21 distinct
pair intersections and no triple concurrence.

Write

```text
e_ij = deg gcd(Rbar_i,Rbar_j).
```

Squarefreeness makes every normalization branch above the pair point
`P_ij=L_{y_i} intersect L_{y_j}` transverse to both selected lines.  The
degree-`k` cover is unramified there, so each such branch has exactly `k`
distinct preimages.  Hence

```text
e_ij = k b_ij,
```

where `b_ij` is the number of normalization branches above `P_ij`.

In the occupancy-at-most-two range, inclusion-exclusion gives

```text
E = sum_{i<j} e_ij = 7d - 6c - |U|,
N = sum_{i<j} b_ij = E/k.
```

A plane point with `b` branches has delta at least `binom(b,2)`.  Convexity
over the 21 pair points therefore gives

```text
D_pair >= B_21(N),
B_21(N) = 21 binom(q,2) + s q,  N=21q+s,  0<=s<21.
```

## 3. Monochromatic-fibre descent

PR #892 proves the corrected chord statement: every positive pair gcd is
contained in one admissible `B`-fibre.  It does not assert that every pair has
such a fibre.

Let `u` be a coordinate on the normalization of `C` and set

```text
K=F_p(X),  U_0=F_p(u),  tau=X^B,  L=U_0(tau),
e=[K:L],   n=k/e,        M=B/e.
```

The `(u,tau)` image is an integral curve of bidegree `(n,M)` and arithmetic
genus `(n-1)(M-1)`.  Above each of the `N` marked pair branches, all `k`
preimages have the same `tau` value.  If `n>1`, the induced point on the
bidegree curve has `n` distinct branches.  Its delta is at least `binom(n,2)`,
so

```text
N binom(n,2) <= (n-1)(M-1),
E <= 2B - 2e <= 65,534.
```

Every row used below has `E>103,000`.  Thus `n=1`, whence `k|B`; also `k|r`
from `r=km`.  Consequently

```text
c=18,619: k in {1,2},
c=18,618: k=1.
```

## 4. Root-layer charges

The PR #892 resultant budget is

```text
3B-a = 30,832,
3w-(3B-a) = 55,859,
c <= floor(55,859/3) = 18,619.
```

Put `L=w-c` and `x=L-S` in each nested divisor layer.  The total slack is two
at `c=18,619` and five at `c=18,618`.  Conjugate blocks carry equal slack and
repeated-root layers are nonincreasing.  The complete finite atlases are
generated by the verifier:

```text
slack 2: split 2, linear*quadratic 2, double+simple 4, triple 2;
slack 5: split 5, linear*quadratic 3, double+simple 12, triple 5.
```

If an occurrence layer has slack `x`, its degree is

```text
v = B-(w-c)+x.
```

At a nonzero root `xi` of `g`, with `alpha=xi^B`, polynomial division and
exact Base cancellation give a nonzero scalar multiple of
`Q_alpha(Y)=(Y-alpha)/a_0(Y)` as the coefficient specialization.  The nested
divisor layers measure the vanishing order of the perturbation.  A simple
layer contributes at least `ceil(v/k)` branches.  For a double root, the
second-layer branches share the tangent visible in

```text
Q(alpha+s,Y)=(Y-alpha)(Y-beta)+s(Y-beta)+O(s^2).
```

For a triple root, the second and third layers have the nested tangent/conic
contact visible in

```text
Q(alpha+s,Y)=(Y-alpha)^2+s(Y-alpha)+s^2.
```

These contacts make the layer delta charges additive.  A repeated zero root
would consume an entire first layer `X^B`, impossible with total slack two or
five.  A simple zero layer has the same multiplicity bound from two independent
linear forms through its coefficient point.  Therefore every factor type has

```text
D_root >= sum_{nu=1}^3 binom(ceil(v_nu/k),2).
```

Exact minimization over the complete typed atlases gives

```text
c=18,619, k=1: (v_1,v_2,v_3)=(22,490,22,491,22,491),
                    D_root=758,711,395;
c=18,619, k=2: (v_1,v_2,v_3)=(22,490,22,490,22,492),
                    D_root=189,669,415;
c=18,618, k=1: (v_1,v_2,v_3)=(22,490,22,491,22,491),
                    D_root=758,711,395.
```

The pair points and coefficient-root points are distinct by the same nonzero
remainder/conductor condition used above.

## 5. Genus contradiction

The rational plane curve `C` of degree `m=r/k` has arithmetic genus

```text
p_a(C)=binom(m-1,2).
```

Its total singularity delta cannot exceed this genus.  The pair and root
charges are disjoint, so `p_a(C) >= D_pair+D_root`.  At the largest admissible
union size below `230,415` in each map-degree branch, exact replay gives

```text
c       k  tested |U|  E       N       D_pair      D_root      p_a(C)       excess
18,619  1    230,414  103,079 103,079 252,931,326 758,711,395 1,011,622,690 20,031
18,619  2    230,413  103,080  51,540  63,221,175 189,669,415   252,888,805  1,785
18,618  1    230,414  103,085 103,085 252,960,774 758,711,395 1,011,667,671  4,498
```

The `k=2` row uses `E=333,493-|U|`, so admissibility forces odd `|U|`.
The balanced pair charge increases as `|U|` decreases.  These three positive
excesses therefore exclude every admissible row below `230,415`, proving the
theorem.

## Exact remaining wall

At `c=18,619`, `|U|=230,415`, only the `k=2` branch survives this package.
Its descended degree is `22,491`; its pair-branch total is `51,539`; and the
genus shortfall is `669`.  A uniform additional delta charge of `670` would
exclude it.

At `c=18,618`, `|U|=230,415`, the map is birational of degree `44,983`, the
pair mass is `103,084`, and the genus shortfall is `410`.  A uniform additional
delta charge of `411` would exclude it.

## Nonclaims

This theorem does not prove:

- the fixed-27 cubic cap six;
- nonexistence of seven labels for arbitrary Base size or arbitrary union;
- a seven-label source witness;
- any statement for `c<=18,617`;
- existence of an admissible third fibre for every pair;
- a received-word owner, first-match atlas, or disjoint add-back;
- multiplication across generators, cores, rays, syndromes, cells, or profiles;
- finite, asymptotic, recurrence-parent, Grand MCA, Grand List, or score
  payment.

The official score remains `0/2`.

## Replay

```bash
python3 experimental/scripts/verify_rank16_fixed27_cubic_near_equality_genus.py
python3 -O experimental/scripts/verify_rank16_fixed27_cubic_near_equality_genus.py
```

Both runs must be byte-identical and match the checked-in expected output.
