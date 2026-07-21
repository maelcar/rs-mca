# Quadratic descent for split Chebyshev fibres

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED.

## Theorem

Let `F` be a field of odd characteristic not dividing `M`.  Assume `T_M`
splits simply over `F`.  Let `d=2^s` with `s>=2`, put `n=M/d`, and let
`H in F[X]` be monic of degree `d`.  Suppose there are distinct values
`c_1,...,c_r in F` such that every `H-c_i` has `d` distinct roots and all
those roots belong to `Z_F(T_M)`.  If

```text
3r >= 2(n+1),
```

then `H` has a quadratic right factor.  Hence, in the absence of such a
factor,

```text
r <= floor((2n+1)/3).
```

Here a quadratic right factor means that `H=G o Q_2` over `F` for
polynomials `G,Q_2 in F[X]` with `deg Q_2=2`.

For `(M,d)=(256,8),(512,16),(1024,32)`, one has `n=32`; therefore 22
complete split fibres force a quadratic right factor and the factor-free cap
is 21.

## Differential divisibility

Select `r` split values and let `A` be their monic squarefree locator.  Then

```text
T_M=A(H)B.
```

There is a unique `V`, with `deg V<r`, such that

```text
V(A')^2=1 mod A.
```

The Chebyshev differential identity

```text
(1-X^2)(T_M')^2=M^2(1-T_M^2)
```

and differentiation modulo `A(H)` give

```text
A(H) | (1-X^2)H'^2B^2-M^2V(H).                 (1)
```

Writing `e=deg H` and `n=M/e`, the degrees of the two terms are

```text
2e(n-r+1),             deg V(H)<=e(r-1).        (2)
```

If `3r=2(n+1)`, the first degree equals `er=deg A(H)` and its leading
coefficient is nonzero.  Equation (1) is therefore an exact scalar multiple
of `A(H)`.  If `3r>2(n+1)`, both terms in (1) have degree below `er`, so the
divisible difference vanishes.  In both cases one obtains

```text
W(H)=(1-X^2)S^2                                      (3)
```

for a nonzero polynomial `W` of positive even degree.

## Ramification-parity lemma

Let `h` be monic of positive even degree.  If (3) holds, then

```text
h=a+q^2
```

for some `a in F` and monic `q in F[X]`.

Over an algebraic closure, let `I` be the roots of `W` having odd
multiplicity.  The only odd valuations of `W(h)` occur at `X=1,-1`.
For each `a in I`, the ramification indices in `h^(-1)(a)` sum to the even
number `deg h`, so each fibre contains an even number of odd indices.  The
number of elements of `I` is even because `deg W` is even.  It is nonzero:
otherwise `W(h)` would be a square, contrary to its odd valuations at `1`
and `-1`.  The two odd indices at `1,-1` must therefore lie over one member
of `I`, while
another member has only even indices above it.  For that value `a`, every
root of `h-a` has even multiplicity, hence `h-a=q^2`.

The monic square root at infinity is recovered recursively from the leading
coefficients using division by two.  Thus `q` and the residual constant `a`
belong to `F`.

## Iteration

If `H=a+Q^2` and `H-c` is a simple completely split fibre, then

```text
H-c=(Q-s)(Q+s)
```

for some nonzero `s in F`.  Thus every split value of `H` yields two
distinct split values of `Q`, and different values yield disjoint pairs.
The transformation is

```text
(e,n,r) -> (e/2,2n,2r).
```

The threshold persists because

```text
3(2r)-2(2n+1)=2(3r-2n)-2 >= 2.
```

Iterating reaches a degree-two inner map.  Composing the square descents
expresses `H=G o Q_2` with `deg Q_2=2`, proving the theorem.

## Reproduction and scope

Run

```text
python experimental/scripts/verify_split_chebyshev_fiber_quadratic_descent.py
```

The verifier checks the Chebyshev identity coefficientwise at the three
active sizes, all degree recurrences, an equality model over `F_17`, and an
exhaustive degree-four ramification test over `F_5`.

The theorem does not sum over varying owners and does not close the mixed
masses `40,48,56,64`.
