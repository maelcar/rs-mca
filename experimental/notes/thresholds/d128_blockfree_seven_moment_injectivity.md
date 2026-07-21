# D128 block-free seven-subset moment injectivity

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED (computer-assisted exact finite theorem).

## Definitions

Let

```text
p = 2147483647
```

and write `F=F_p`.  Normalize the Chebyshev polynomials by

```text
T_0=1,  T_1=X,  T_(m+1)=2X T_m-T_(m-1).
```

Let `D_128` be the 128 simple roots of `T_128` in `F`.  The fibres of
`T_4` partition `D_128` into 32 four-point blocks.  For a subset `S` put

```text
mu_3(S)=(sum_(x in S) x, sum_(x in S) x^2, sum_(x in S) x^3).
```

A seven-subset is *block-free* if it contains no complete `T_4` block.

## Theorem

The map

```text
S -> mu_3(S)
```

is injective on the block-free seven-subsets of `D_128`.

## Small-intersection reduction

An exhaustive classification gives the following exact statements.

1. For four-subsets, the only nonsingleton moment fibre is the set of all
   32 complete `T_4` blocks.
2. Every nonsingleton five-subset fibre is obtained by fixing one point and
   adjoining a complete `T_4` block disjoint from it.
3. The complete census of all
   `binom(128,6)=5423611200` six-subsets has exactly 8128 nonsingleton
   fibres.  Each is obtained by fixing a pair and adjoining every disjoint
   complete `T_4` block.  In particular, no such fibre contains two
   disjoint six-subsets.

For subsets of size at most three, the first three power sums determine the
elementary symmetric polynomials by Newton's identities.  Since `p>3`, they
therefore determine the subset itself.

The six-subset fibres have the exact distribution

```text
7936 fibres of size 30;
 192 fibres of size 31;
8128 fibres with common intersection size 2;
   0 other collision fibres.
```

Let `S` and `S'` be distinct block-free seven-subsets with equal moments.
If they shared at least two points, cancellation would give an equal-moment
collision of size at most five.  At size at most three, Newton's identities
would make the residual subsets equal and hence give `S=S'`.  At size four
or five, the classification would force a complete `T_4` block on one side,
contradicting block-freeness.  Hence `|S intersect S'|<=1`.  If the
intersection had size one, cancellation
would leave two disjoint equal-moment six-subsets, which statement 3
excludes.  Therefore distinct members of one block-free seven-subset moment
fibre must be disjoint.

## Exclusion of disjoint collisions

Every `T_4` block has the form

```text
{u,-u,v,-v},  u^2+v^2=1.
```

For a disjoint balanced seven-versus-seven difference vector, define the
64 odd antipodal coordinates

```text
alpha_u=z_u-z_(-u),  alpha_v=z_v-z_(-v).
```

This odd coordinate vector is nonzero: if every antipodal difference
vanished, each of the two disjoint seven-subsets would be a union of
antipodal pairs and would have even cardinality.

The first and third moment equations place `alpha` in the index-`p^2`
lattice

```text
O={alpha in Z^64:
   sum alpha_r r=0 mod p,
   sum alpha_r r^3=0 mod p}.
```

Its Lee weight is at most 14.  Exact fixed-radius enumeration proves that
the nonzero ball `sum alpha_r^2<=16` has one sign-normalized class and that
class has Lee weight 16.  Thus a collision vector must have squared norm at
least 17.  If `t` coordinates have absolute value two and `s` have absolute
value one, Lee weight and norm leave precisely

```text
(t,s)=(2,10),(3,6),(3,8),(4,2),(4,4),(4,6),
      (5,0),(5,2),(5,4),(6,0),(6,2),(7,0).
```

Exact meet-in-the-middle and even-first enumerations exclude all twelve
profiles, while checking support disjointness and both odd moment
congruences.  Hence no disjoint block-free seven-versus-seven collision
exists.

The small-intersection reduction says every hypothetical distinct pair must
be disjoint.  The antipodal calculation says no such pair exists.  This
proves the theorem.

## Reproduction

The certificate directory
`experimental/data/certificates/d128-blockfree-seven-moment-injectivity`
contains the complete recorded outputs, lattice bases, profile results, and
hash manifest.  Run the fast implication check with

```text
python experimental/scripts/verify_d128_blockfree_seven_moment_injectivity.py
```

The certificate README gives commands for the exhaustive Rust and C++
replays.  The six-subset census uses external buckets and the odd-lattice
radius proof requires `fplll`.

## Scope

This is an exact finite-field theorem for the stated domain and partition.
It does not assert a uniform theorem over other fields, arbitrary received
words, or varying algebraic owners.
