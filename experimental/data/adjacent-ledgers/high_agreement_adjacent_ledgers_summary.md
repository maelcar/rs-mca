# High-agreement adjacent ledgers

This packet extends the tangent staircase beyond finite-slope support-wise MCA.

## Results

Let `C = RS[F,D,k]`, `|D| = n`, `q = |F|`.

### 1. CA and projective-slope MCA

If

```text
3a - 2n >= k,
```

then the high-agreement tangent staircase pins three affine/projective line
quantities:

```text
LD_sw(C,a) = LD_ca(C,a) = LD_sw,proj(C,a) = n-a+1.
```

Here `LD_ca` is the no-loss correlated-agreement finite-slope count, and
`LD_sw,proj` allows the point at infinity in `P^1(F)`.

### 2. Degree-d curve MCA / curve-CA

For finite-parameter degree-`d` power curves

```text
W_gamma = f_0 + gamma f_1 + ... + gamma^d f_d,  gamma in F,
```

if

```text
(d+2)a - (d+1)n >= k,
```

then

```text
CurveLD_sw^(d)(C,a) = CurveLD_ca^(d)(C,a)
                    = min(q, d*(n-a+1)).
```

The lower bound is a degree-`d` tangent construction that assigns up to `d`
bad parameters to each residual coordinate.  The upper bound interpolates
`d+1` bad parameters to recover a common code-curve on a large intersection,
then charges residual roots; each residual coordinate contributes at most `d`
bad parameters.

### 3. Interleaved-list uniqueness

For every interleaving arity `mu >= 1`, if

```text
2a - n >= k,
```

then

```text
Lambda_mu(C,a) = 1.
```

This is the ordinary MDS unique-decoding argument applied row-wise to common
agreement supports.

## F_17^32, n=512, k=256 consequences

Let

```text
C = RS[GF(17^32), H, 256], |H| = 512.
```

Then

```text
floor(17^32 / 2^128) = 6.
```

The high-agreement ledgers are:

```text
LD_sw(C,a) = LD_ca(C,a) = LD_sw,proj(C,a) = 513-a,  for a >= 427.
Lambda_mu(C,a) = 1,                                  for a >= 384.
CurveLD^(d)(C,a) = d*(513-a)                         in the degree-d curve range.
```

Thus, for a protocol whose coding error is exactly one affine/projective
line CA/MCA term plus one interleaved-list term, with no query/folding error,
the combined numerator is

```text
(513-a) + 1 = 514-a.
```

So:

```text
a=507: line numerator 6 + list numerator 1 = 7  -> unsafe for 2^-128
a=508: line numerator 5 + list numerator 1 = 6  -> safe for 2^-128
```

For degree-`d` curves plus the interleaved list term, the condition is

```text
d*(513-a) + 1 <= 6.
```

Consequences:

```text
d=1: safe with list iff a >= 508
d=2: safe with list iff a >= 511
d=3,4,5: safe with list only at a = 512
d>=6: no safe grid point with the list term
```

The result is not a general SNARK theorem.  It is a coding-ledger theorem for
protocol reductions that consume exactly the printed coding terms over the
printed field, plus any separately added query/folding/cryptographic errors.
