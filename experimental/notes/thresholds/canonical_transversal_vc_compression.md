# Canonical-transversal VC compression for subset-sum fibers

## Status

`PROVED` as a finite theorem for arbitrary subset-sum maps into arbitrary
abelian groups.  The theorem supplies the image conclusion called
`(ILO-moment)` in `fiber_image_tradeoff.md`; it does not supply the
source-specific first-match atlas, block embedding, profile add-back, or slope
charge needed to close A4.

This note is complementary to PRs #661 and #663.  Those packets analyze the
stronger structural route from exponential concentration to quadratic Bohr or
GAP structure.  The result below bypasses that structural conversion when the
consumer needs only an upper bound on the subset-sum image.

## Theorem

Let `G` be an abelian group, let `a_1,...,a_b` be an indexed sequence in `G`,
and define

```text
sigma(S) = sum_{i in S} a_i,                         S subseteq [b],
f(A)     = max_y #{S : sigma(S)=y},
L(A)     = #{sigma(S) : S subseteq [b]}.
```

Call `I subseteq [b]` subset-dissociated when all `2^|I|` subset sums of
`(a_i)_{i in I}` are distinct, and put

```text
d(A) = max{|I| : I is subset-dissociated}.
```

Then

```text
f(A) <= 2^(b-d(A)),
L(A) <= sum_{j=0}^{d(A)} binom(b,j).                  (1)
```

Consequently, with `r(A)=floor(b-log_2 f(A))`, one has

```text
L(A) <= sum_{j=0}^{r(A)} binom(b,j),
f(A)L(A) <= 3^b.                                     (2)
```

If `0 <= eta <= 1/2` and `f(A) >= 2^((1-eta)b)`, then

```text
L(A) <= 2^(H_2(eta)b),                               (3)
```

where `H_2(eta)=-eta log_2 eta-(1-eta)log_2(1-eta)`.
Thus `(ILO-moment)` holds with `eta_0=1/2` and
`omega(eta)=H_2(eta)`.

## Proof

Fix a maximum subset-dissociated set `I`.  On any fiber `sigma^{-1}(y)`, the
projection `S -> S\I` is injective: two sets with the same outside part would
give two equal subset sums on `I`.  There are only `2^(b-|I|)` outside parts,
which proves the first inequality in (1).

Give coordinate `i` cost `2^(i-1)` and each subset the sum of its coordinate
costs.  Every subset has a distinct cost.  From every nonempty fiber of
`sigma`, choose its unique minimum-cost representative, and call the resulting
family `R`.  Then `|R|=L(A)`.

Every set shattered by `R` is subset-dissociated.  Indeed, suppose `J` is
shattered and distinct `B,C subseteq J` have the same subset sum.  Their costs
are distinct; assume `cost(B)>cost(C)`.  Shattering supplies `R_0 in R` with
`R_0 intersect J=B`.  Replacing `B` by `C` preserves `sigma(R_0)` and strictly
decreases its cost, contradicting the definition of `R_0`.  Hence
`VCdim(R)<=d(A)`, and the Sauer--Shelah bound gives the second inequality in
(1).

The first inequality in (1) implies
`d(A)<=floor(b-log_2 f(A))`, which gives the first assertion in (2).  Combining
the two inequalities in (1),

```text
f(A)L(A)
 <= 2^(b-d) sum_{j=0}^d binom(b,j)
 <= 2^b sum_{j=0}^b binom(b,j)2^(-j)
 = 3^b.
```

Finally, the concentration hypothesis gives `d(A)<=eta b`.  The standard
binomial-prefix entropy bound
`sum_{j=0}^{floor(eta b)} binom(b,j)<=2^(H_2(eta)b)` for
`eta<=1/2` proves (3).

## Fixed-density and masked corollary

Take `a_i=(1,v_i,v_i^2)` (or any other moment columns).  If a fixed-density or
first-match residual family `F` lies in one full subset-sum fiber, then
`f(A)>=|F|`, so

```text
L(A) <= sum_{j=0}^{floor(b-log_2 |F|)} binom(b,j).
```

In particular, `|F|>=2^((1-eta)b)` forces
`L(A)<=2^(H_2(eta)b)`.  No phase-independence or algebraic description of the
mask is required.  The image here is the full block image; this is a safe upper
bound for the image of any fixed-density subfamily.

## Frontier consequence and exact remaining wall

For the degree-two moment block used by `fiber_image_tradeoff.md`, write
`phi=b^{-1}log fstar`, `lambda=b^{-1}log L1`, with natural logarithms.  The
product inequality gives

```text
phi + lambda <= log 3,
rho = phi + lambda - log 2 <= log(3/2) < log 2.
```

This closes the named analytic image atom.  It does **not** prove that every
primitive post-atlas A4 leaf has the required block/fiber typing, nor does it
pay the effective image over all leaves, profile add-back, ray overlap, A2,
A6, A7, or LOWER.  It proves no deployed adjacent-row inequality and neither
Grand MCA nor Grand List.
