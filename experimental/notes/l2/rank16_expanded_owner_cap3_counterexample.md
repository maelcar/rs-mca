# Rank-16 expanded-owner complement-cap-three counterexample

**Claim:** In the deployed base-field row there is one normalized received
word with 15 distinct list polynomials outside the complete expanded owner

```text
D -> Q110 -> M -> Q41 -> X175 -> J48 -> integer-subcore owner.
```

Thus the proposed universal bound that at most three list polynomials remain
outside this unchanged owner is false.

**Status:** Proved finite source-valid route cut. The construction has only 15
displayed list polynomials, contributes no owner payment, and does not close or
refute the rank-16 parent, Grand List, Grand MCA, or either official question.
The official score remains `0/2`.

**Verifier:**
`experimental/scripts/verify_rank16_expanded_owner_cap3_counterexample.py`
checks the deployed constants, primality, subgroup orders, block arithmetic,
exact agreement and intersection counts, all expanded-owner exclusions, source
hashes, and eight semantic mutations using only the Python standard library.

## Deployed row

Work over `F_p`, where

```text
p = 2,130,706,433,  n = 2^21,  K = 2^20,
m = 1,116,047,      B = 2^15,  t = n-m.
```

Let

```text
omega = 3^1016 in F_p,  H = <omega>,  zeta = omega^B.
```

Since `p-1=1016*n`, `omega` has order `n` and `zeta` has order 64. The
fixed q64 blocks are

```text
H_j = {omega^(j+64k) : 0 <= k < B},  0 <= j < 64.
```

They are disjoint, cover `H`, and satisfy `x^B=zeta^j` on `H_j`.

For one normalized word `U:H->F_p`, let

```text
L(U) = {P in F_p[X] : deg(P)<K and |Agr(U,P)|>=m}.
```

Fix any total order on `H`. The owner stack canonically takes the first
exactly `m` agreements of each `P in L(U)`. In the construction below every
displayed polynomial has exactly `m` agreements, so its canonical agreement
set is independent of that order.

## Construction

Inside block `H_j`, take an initial core segment of size

```text
alpha_0 = 16,383,
alpha_j = 16,384 for 1 <= j < 64.
```

Let `C` be the union of these 64 segments. Then

```text
|C| = 16,383 + 63*16,384 = 1,048,575 = K-1.
```

Put

```text
lambda_j = 1,055 for 0 <= j < 16,
lambda_j = 1,054 for 16 <= j < 64.
```

For each `i=1,...,15`, let `W_i` use, in every block, the half-open exponent
interval immediately following the core segment:

```text
W_(i,j) = {omega^(j+64k) :
           alpha_j+(i-1)lambda_j <= k < alpha_j+i*lambda_j},
W_i = union_j W_(i,j).
```

The intervals are mutually disjoint and disjoint from `C`. Their largest
endpoint is

```text
max_j(alpha_j+15*lambda_j) = 32,209 < B.
```

Each petal has size

```text
|W_i| = 16*1,055 + 48*1,054 = 67,472 = m-K+1.
```

The unused remainder has size

```text
|R| = n-(K-1)-15(m-K+1) = 36,497.
```

Define

```text
Q(X) = product_(x in C) (X-x),
P_i(X) = i Q(X),  1 <= i <= 15.
```

The polynomial `Q` is monic and squarefree of degree `K-1<K`; its roots in
`H` are exactly `C`. The scalars `1,...,15` are distinct and nonzero in
`F_p`, so the `P_i` are distinct.

Define one word by

```text
U(x) = 0       for x in C,
U(x) = i Q(x) for x in W_i,
U(x) = 16 Q(x) for x in R.
```

For `x` outside `C`, `Q(x)` is nonzero. Hence, for every `i`,

```text
Agr(U,P_i) = C disjoint-union W_i
```

exactly, and

```text
|Agr(U,P_i)| = (K-1)+(m-K+1) = m.
```

For `i != j`, the two exact agreement sets intersect in exactly `C`, so

```text
|Agr(U,P_i) intersect Agr(U,P_j)| = K-1.
```

This saturates the standard degree intersection bound without violating it.
Coordinatewise multiplication by nonzero GRS weights preserves all displayed
agreements, so the normalized construction gives the literal weighted-GRS
source object as well.

## Why every expanded owner misses

Each exact agreement set meets every q64 block but contains no complete q64
block. Therefore it contains no complete larger dyadic block either, and

```text
(e15,e16,e17,e18,e19,e20) = (0,0,0,0,0,0).
```

Its exact error complement also meets every q64 block but contains no complete
q64 block, so

```text
f64 = 0.
```

These two structural facts exclude every owner stage:

* `D` requires `e15=33`, `e15=34`, or `e16=16`;
* `Q110` and `Q41` contain only `e15=32` profile cells;
* `M` requires `f64=29` or paired `f64=28`;
* `X175` contains nonpaired `f64=28` cells;
* `J48` contains selected `f64=27` and `f64=26` cells;
* the integer-subcore owner is inside `e15=31` cells with `f64=27` or 26.

Thus for every total order `prec` on `H`,

```text
P_i in L(U) \ O_expanded^prec(U),  1 <= i <= 15,
|L(U) \ O_expanded^prec(U)| >= 15 > 3.
```

The counterexample is chosen independently of `prec`; order independence is
not obtained by selecting a different word or different polynomials afterward.

## Audit provenance

The theorem was independently checked in two frozen external-Pro audits:

```text
proof-audit packet:
41c1cfcbe53f6561544e23edabf2d01f8c2aa5814452b2b6e41627a8cc9ce68b
proof-audit final:
fca31b30f42f7d3470b191122b556498ca18d820bf3bd9bc49836d09d60eb4a4

source-audit packet:
7af2878e2dacad9c8f45e32dc10a5f16a939284756c4e4f614935c897510eef9
source-audit final:
4b8d8ee721e6cb2bdd178f878cb9b902ed91b13323d8c22caaf71e4e07d995b7
```

Both verdicts were `ACCEPT_NARROWED`. The present note uses only the common
narrowed theorem and does not import unavailable author-bundle replay claims.

## Ledger impact and exact remaining wall

The integrated expanded owner retains its proven cap `T-3`. This construction
shows only that one cannot finish the parent by asserting a universal
three-candidate cap on its complement. It does not show that this word has
`T-3` owner candidates, and its 15 displayed list polynomials are far below
the official target.

The exact rank-16 wall is therefore a different source-valid global payment
for the residual complement, or a replacement owner whose proof actually
covers this zero-profile, `f64=0` scalar-sunflower family. Local fixed-core
caps still require a valid global incidence/occupied-key compiler.

## Nonclaims

This result does not claim:

* a list of size greater than `T`;
* that the expanded owner's `T-3` cap is false;
* that 15 is the maximum complement size;
* population of the printed first unpaid `(A*,F*)` bucket;
* failure of any fixed-26 or fixed-27 local theorem;
* a rank-16 parent closure or counterexample;
* an all-rank, asymptotic, Grand List, or Grand MCA theorem;
* any official score change.
