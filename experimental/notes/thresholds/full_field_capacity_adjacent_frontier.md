# Exact full-field capacity-adjacent MCA frontier

## Status

`PROVED`, conditional only on the exact syndrome-secant lower theorem in PR
#669 until that dependency is integrated.  This is a full-field Grand MCA
threshold theorem at the first admissible agreement.  It is not a complete
Grand MCA theorem and says nothing about Grand List.

## Setup

Let

```text
C = RS_F(D,k),       q = |F| = q_line,
Gamma = F,           E = 2^128,
R = n-k >= 1,        M = binom(n,k+1),
b = floor(q/E).
```

Assume the official line-field cap `2 <= q < E^2 = 2^256`.  The target is
the literal closed-grid value `B* = b`.

## Theorem

At the first admissible agreement,

```text
B_C^MCA(k+1) <= b  iff  M <= b  iff  q >= E M,           (F1)
B_C^MCA(k+1) >  b  iff  M >  b  iff  q <  E M.           (F2)
```

Equality `q=EM` is therefore on the safe side.  Moreover,

```text
M <= b+1  implies  B_C^MCA(k+1) = M.                    (F3)
```

Thus the exact full-field capacity-adjacent transition below the official
field cap is

```text
q_crit(n,k) = 2^128 binom(n,k+1).
```

## Proof

The exact support ceiling gives

```text
B_C^MCA(k+1) <= M.                                      (1)
```

PR #669, specialized to the full-field challenge `Gamma=F`, gives

```text
B_C^MCA(k+1)
  >= ceil((q-1) M / (M+q-1)).                            (2)
```

There are three integer branches.

### 1. `M <= b`

Equation (1) proves safety.  Also `q >= bE >= ME`.  Since `q<E^2`, one has
`b<=E-1`, hence `M<E`.  Therefore

```text
q >= ME > max(M, binom(M,2)) = Q_sep(M)
```

(with `M=1` immediate).  The exact adjacent separating theorem gives
`B_C^MCA(k+1)=M`.

### 2. `M >= b+2`

The real function

```text
f_q(x) = (q-1)x/(x+q-1)
```

is strictly increasing.  It is enough to test `x=b+2`.  The inequality
`f_q(b+2)>b` is equivalent to

```text
2(q-1) - b(b+2) > 0.                                   (3)
```

For `b=0`, this is immediate.  For `b>=1`, use `q>=bE` and `b<=E-1`:

```text
2(q-1)-b(b+2)
  >= b(2E-b-2)-2
  >= b(E-1)-2
  > 0.
```

Equation (2) is therefore at least `b+1`, proving unsafety.

### 3. `M=b+1`

Here `M<=E`.  Since `q>=bE=(M-1)E`, one has

```text
q > max(M, binom(M,2)) = Q_sep(M).
```

The exact adjacent separating theorem gives
`B_C^MCA(k+1)=M=b+1`, so the seam is unsafe.

The three branches prove (F1)--(F3).  The equivalence
`M<=floor(q/E) iff EM<=q` fixes the closed endpoint.

## Exact top-two-row consumer

For `R>=2`, put `M_2=binom(n,k+2)`.  Then

```text
M_2 <= b < M  implies
B_C^MCA(k+2) <= M_2 <= B* < B_C^MCA(k+1),
```

so the first safe agreement is exactly `a*=k+2`.  This is a genuine adjacent
certificate, but only for rows satisfying the displayed integer interval.

## Same-domain field pair

Take `n=128`, `k=64`, and an order-128 subgroup `D` of `F_(3^32)^*`.
The domain-generated field is `q_D=3^32`.  Use the same domain in the two
ambient line fields

```text
q_unsafe = 3^96,        q_safe = 3^160.
```

Both contain `F_(3^32)` and both are below `2^256`.  For
`M=binom(128,65)`, the first field satisfies `q_unsafe<2^128 M`, while the
second satisfies `q_safe>2^128 M`.  The theorem makes the first agreement
unsafe in the first ambient field and safe in the second.  This uses no
ambient-field entropy payment and does not assert that the generated field
of an arbitrary received pair is `F_(3^32)`.

## Ownership and novelty

PR #669 owns the syndrome-secant theorem and equation (2).  Holmbuar's
earlier comment on #669 owns the general `a=k+s` shell specialization.  The
new delta here is only the exact target-aware closure of the three integer
branches at `s=1`, including the closed endpoint and the top-two-row
consumer.  No `s=2` shell formula is claimed as new.

## Nonclaims and remaining wall

This theorem does not prove:

- an iff statement for a proper challenge subset `Gamma`;
- a safe envelope at deeper agreements outside the top-two-row interval;
- a quotient-aware adjacent lower;
- a complete witness-exhaustive first-match upper ledger;
- Grand MCA, Grand List, or either official prize question;
- a finite deployed row without the literal inequality
  `U(a0+1)<=B*<L(a0)`.

After this partition, the lower-side wall is no longer uniform unsafety at
`k+1`.  In the unsafe branch where `binom(n,k+2)>B*`, one must locate the
first deeper lower crossing and pair it with a complete safe ledger one
agreement later.
