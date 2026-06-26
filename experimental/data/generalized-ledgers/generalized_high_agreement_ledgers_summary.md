# Generalized high-agreement ledgers beyond the F_17^32 row

## What changed

The high-agreement tangent method is not special to `F_17^32`.  It gives a row-independent finite-grid calculator for any Reed--Solomon row `RS[F,D,k]` with `D subset F`; most upper-bound arguments only need the MDS property.  This is still a coding-ledger theorem, not a full protocol theorem.

Write

```text
n = |D|,
k = dimension,
R = n-k,
a = agreement threshold,
r = n-a = integer Hamming radius,
q = |F|,
B_Q = floor(Q / 2^128)
```

where `Q` is the denominator used by the sampler or challenge field.

## Line / CA / projective slope

In the exact high-agreement range

```text
3a - 2n >= k
```

equivalently

```text
r <= floor((n-k)/3),
```

one has

```text
LD_sw(C,a) = LD_ca(C,a) = LD_sw,proj(C,a) = n-a+1 = r+1.
```

This generalizes the `F_17^32` row formula `513-a`.

If the line denominator is `Q`, the line term alone is safe at target `2^-128` when

```text
r + 1 <= B_Q.
```

The first unsafe radius is `r = B_Q`, provided `B_Q <= floor((n-k)/3)`.

## Interleaved-list uniqueness

For every interleaving arity `mu >= 1`, if

```text
2a - n >= k
```

equivalently

```text
r <= floor((n-k)/2),
```

then

```text
Lambda_mu(C,a) = 1.
```

Thus in the line exact range the interleaved-list term contributes exactly one numerator unit.

A line/CA/MCA term plus one interleaved-list term over the same field is safe when

```text
(r + 1) + 1 <= B_Q,
```

so

```text
r <= B_Q - 2.
```

The first unsafe radius is `r = B_Q - 1`, if it lies in the exact line range.

## Degree-d finite-parameter curves

For a finite-parameter power curve

```text
W_gamma = f_0 + gamma f_1 + ... + gamma^d f_d,
gamma in F,
```

in the exact curve range

```text
(d+2)a - (d+1)n >= k
```

equivalently

```text
r <= floor((n-k)/(d+2)),
```

the support-wise curve-MCA and no-loss curve-CA numerators are

```text
CurveLD_sw^(d)(C,a) = CurveLD_ca^(d)(C,a) = min(q, d(r+1)).
```

The curve term alone is safe when

```text
d(r+1) <= B_Q.
```

A curve term plus one interleaved-list term is safe when

```text
d(r+1) + 1 <= B_Q.
```

## General protocol numerator with common denominator

If a protocol ledger uses curve or line terms of degrees `d_1,...,d_s`, where affine/projective line is `d=1`, and `ell` interleaved-list terms, all over the same denominator `Q`, then in the common exact range

```text
N_total(r) = ell + sum_i d_i (r+1).
```

It is certified at target `2^-128` if

```text
N_total(r) <= B_Q.
```

If different terms use different fields, do not combine numerators.  Use

```text
sum_i N_i(r)/Q_i + query_error <= 2^-128.
```

## Prize-rate applicability

For prize rates `rho in {1/2,1/4,1/8,1/16}` and `k <= 2^40`, the tangent line method can pin the threshold only if

```text
2^(lambda-128) <= (n-k)/3,
```

where `q approx 2^lambda`.

At maximal `k = 2^40`, the largest approximate field sizes for which the line threshold can still be pinned inside the exact tangent range are:

| rho | max line-range radius at k=2^40 | lambda up to about |
|---:|---:|---:|
| 1/2 | 2^40 / 3 | 166.4 |
| 1/4 | 2^40 | 168.0 |
| 1/8 | 7*2^40 / 3 | 169.2 |
| 1/16 | 5*2^40 | 170.3 |

For fields around `2^192` or `2^256`, the tangent numerator is below the `2^-128` budget throughout the exact high-agreement range.  The threshold then has to be controlled by quotient-core, generated-field entropy, curve/folding, or aperiodic local-limit ledgers.


## Integration notes

- Put the LaTeX section after the tangent staircase section and before the older finite-threshold/prize-gate material.
- Wording now avoids claiming that every construction is an abstract MDS theorem: the lower constructions are phrased for `RS[F,D,k]` / evaluation-domain codes, while the uniqueness and upper-bound arguments are MDS.
- The verifier output in this packet is clean and contains only the generalized ledger arithmetic.
- The protocol statement remains conditional: it applies only to reductions whose coding error is exactly the printed sum of line/curve/list terms over the stated denominators, plus any separately supplied query/folding error.
