# Rank-16 fixed-26 divided-difference source compiler

**Status:** proved local source theorem and proved monomial-generator
corollary.  This note makes no finite payment.

## Deployed cell and notation

Work over the literal base field `F_p`, where

```text
p = 2130706433,       n = 2097152,       B = n/64 = 32768,
a = 67472 = 2B+s,    s = 1936,
r = 63601 = 2B-s+1,  D = r-s = 61665,
d = D-B = 28897,     B-d-1 = 3870.
```

Let `H = mu_n` and `Omega = mu_64` inside `F_p^*`, and put
`F_y(X)=X^B-y` for `y in Omega`.  Fix one literal degree-saturated rank-16
`c=0` source cell consisting of all of the following data:

1. one canonical received word together with its actual first-match owner;
2. one monic degree-`a` polynomial `g` satisfying
   `gcd(g,X^n-1)=1`;
3. one nonzero projective residue ray `[eta]` modulo `g`;
4. one set `C` of 26 complete q64 error-fiber labels.

Write

```text
G_C = product(F_c : c in C),
Q   = Omega \ C,                    |Q| = 38,
xi  = rem_g(G_C^(-1) eta),          deg xi < a.
```

All inverses and remainders are in `F_p[X]/(g)`.  They exist because every
root of every `F_y` lies in `H`, whereas `g` is root-free on `H`.

## Theorem: the fixed-26 source compiler

For every `y in Q`, define

```text
V_y = rem_g(xi F_y^(-1)),
F_y V_y = xi + g S_y.                                      (1)
```

Then `deg V_y<a`, `deg S_y<B`, and on the fiber `x^B=y`,

```text
S_y(x) = -xi(x)/g(x).
```

Thus the 38 polynomials `S_y` are the unique degree-`<B` local
interpolants of one fixed rational received function.  They are source data,
not independently selected pair witnesses.

For distinct `y,z in Q`, set

```text
U_yz = (V_y-V_z)/(y-z),
Q_yz = (S_y-S_z)/(y-z),
P_yz = S_y + F_y Q_yz
     = (F_z S_y-F_y S_z)/(y-z).                            (2)
```

The following are exact polynomial identities:

```text
V_y-V_z       = (y-z) U_yz,
F_z U_yz      = V_y + g Q_yz,
F_y U_yz      = V_z + g Q_yz,
F_y F_z U_yz  = xi + g P_yz,
U_yz           = rem_g(xi (F_y F_z)^(-1)).                 (3)
```

Define the high tail and boundary coefficient by

```text
tau_y = ([X^(d+1)]S_y,...,[X^(B-1)]S_y) in F_p^3870,
c_y   = [X^d]S_y.                                          (4)
```

Then

```text
deg U_yz <= r  iff  tau_y=tau_z,                            (5)
deg U_yz  = r  iff  tau_y=tau_z and c_y!=c_z.               (6)
```

In the exact-degree case,

```text
lc(U_yz) = lc(Q_yz) = (c_y-c_z)/(y-z),
q_yz     = (y-z)/(c_y-c_z),
R_yz     = q_yz U_yz.                                      (7)
```

Consequently `R_yz` is the unique possible monic degree-`r` residual
locator for the pair `{y,z}`.  This is a candidate compiler, not a splitting
criterion.

The compiler preserves the source ray.  Indeed,

```text
A_C = (G_C xi-eta)/g
```

is a polynomial, and (3) gives

```text
G_C F_y F_z R_yz
  = q_yz eta + g q_yz (A_C+G_C P_yz).                      (8)
```

It also gives the literal fixed-27 interface

```text
F_z R_yz = q_yz V_y + g(q_yz Q_yz).                        (9)
```

Hence the normalized fixed-27 Pade quotient is exactly the divided
difference `Q_yz`, with the generator, ray, received word, endpoint, and
first-match cell unchanged.

### Validity remains a filter

A compiled pair is an actual valid nonpaired `f=28` edge only after every
one of the following independent conditions is checked:

- `R_yz` has exact degree `r` and the monic normalization (7);
- `R_yz` is squarefree and splits completely over `H`;
- it avoids all roots in the 28 selected complete fibers
  `G_C F_y F_z`;
- no further q64 fiber divides it;
- its residual roots meet at least four further q64 fibers;
- `C union {y,z}` is not a union of fourteen natural q32 pairs under the
  involution `w -> -w`;
- the source lies outside the earlier agreement and
  `f=29`/paired-`f=28` owners;
- `R_yz` is the actual canonical first-match locator of the fixed received
  word.

Neither (5) nor any congruence in (3) implies splitting, squarefreeness,
footprint, nonpairing, or first-match ownership.

## Corollary: the monomial-generator cap

Assume now that

```text
g = X^a = X^67472.
```

For arbitrary source-admissible `xi`, arbitrary fixed core `C`, and arbitrary
fixed source data as above, at most 37 unordered pairs can have a degree-`63601`
candidate that splits completely over `H`.  In particular, the graph of
actual valid pair-candidate edges has

```text
|E| <= 37.                                                  (10)
```

This is only a monomial-generator theorem.  It is not an arbitrary-`g`
cap 116.

## Proof

### Compiler identities and degree test

The root-free hypothesis makes `G_C` and every `F_y` invertible modulo `g`,
so (1) exists uniquely.  Since
`deg(F_y V_y-xi)<=a+B-1`, exact division by the monic degree-`a` polynomial
`g` gives `deg S_y<B`.

Modulo `g`,

```text
V_y-V_z = xi(F_y^(-1)-F_z^(-1))
        = (y-z)xi(F_y F_z)^(-1).
```

Both sides after division by `y-z` have degree `<a`, so the congruence is
the exact identity for `U_yz` in (3).  Substituting (1) and
`F_z=F_y+(y-z)` gives the remaining identities in (3).

If `deg U_yz<=r`, then `g Q_yz=F_z U_yz-V_y` has degree at most `B+r`,
whence `deg Q_yz<=B+r-a=d`.  This is exactly `tau_y=tau_z`.
Conversely, equality of the tails gives `deg Q_yz<=d`, and (3) gives
`deg U_yz<=a+d-B=r`.  This proves (5).

Under equal tails, the coefficient of `X^d` in `Q_yz` is
`(c_y-c_z)/(y-z)`.  If it is nonzero, the leading term of `g Q_yz` has
degree `a+d=B+r` and cannot cancel against `V_y`, whose degree is `<a`.
This proves exact degree and (7).  If it vanishes, the same identity gives
`deg U_yz<=r-1`.  Uniqueness follows because two degree-`<a` solutions of
the same residue congruence differ by a multiple of the degree-`a`
polynomial `g`.

Finally, `G_C xi-eta` is divisible by `g`.  Multiplying
`F_y F_z R_yz=q_yz(xi+gP_yz)` by `G_C` proves (8); multiplying the second
identity in (3) by `q_yz` proves (9).

### Monomial cap

Write `xi=sum_{k=0}^{a-1} xi_k X^k`, and define degree-`<B` polynomials

```text
A_0 = sum_{k=0}^{s-1}       xi_k X^(k+B-s),
A_1 = sum_{k=s}^{B+s-1}     xi_k X^(k-s),
A_2 = sum_{k=B+s}^{2B+s-1}  xi_k X^(k-B-s).
```

Truncating the geometric inverse of `X^B-y` modulo `X^a` gives

```text
S_y = -y^(-3)A_0-y^(-2)A_1-y^(-1)A_2.                     (11)
```

Let `pi_>d` retain coefficients in degrees `d+1,...,B-1`, and put
`v=y^(-1)`.  Since all of `A_0` lies above degree `d`,

```text
tau_y = -(v^3 A_0+v^2 pi_>d(A_1)+v pi_>d(A_2)).            (12)
```

If the vector-valued cubic in (12) is nonzero, one coordinate is a
nonconstant scalar polynomial of degree at most three.  Each high-tail
collision class among the 38 distinct labels therefore has size at most
three.  Convexity, or direct integer partitioning, gives

```text
12*binom(3,2)+binom(2,2) = 37.
```

All degree-`r` pair candidates lie inside these collision classes by (5),
so there are at most 37 before the remaining validity filters are applied.

If (12) vanishes on all 38 labels, each coordinate cubic has more than
three roots and is identically zero.  In particular `A_0=0`, hence
`X^s` divides `xi`.  The truncated inverse of `X^B-y` has nonzero constant
term and only powers of `X^B`, so `X^s` divides every `V_y`, every `U_yz`,
and every scalar multiple `R_yz`.  Such a candidate has root zero, whereas
`H` is contained in `F_p^*`.  It cannot split completely over `H`.  This
proves (10).

## Novelty and ownership

The overlap baseline is `origin/main@9c4ca98cf45639407611a3ad5154893fb22e77e2`
plus open PRs #826, #838, #843, and #844.

- PR #826 owns its fixed-27 affine-line obstruction.  This packet does not
  reclaim that theorem; the compiler and monomial cap do not depend on it.
- PR #838 owns the global first-match ledger and its 1,682-profile residual.
  No local count here is composed into that ledger.
- PR #843 owns the fixed-27 rank-two cubic/quartic block-wedge structural
  classification.  That classification, and every rank-two consequence of
  it, is explicitly carved out of this packet.
- PR #844 is treated wholesale as prior ownership in the supplied overlap
  baseline.  This packet does not restate or consume any #844 claim.

The only claimed novelty is (i) the 38-interpolant, 703-pair fixed-26 source
compiler with its exact degree and source-ray identities, and (ii) the
monomial-generator cap 37.

The stale 116/117 ledger is deliberately absent.  In particular, this note
does not print all-`f=28` totals, does not spend the main-owned `Q110` owner,
and makes zero finite payment.

## Exact scope and remaining wall

This theorem does **not** prove an arbitrary-generator cap 116, construct a
117-family, close a recurrence parent, close the rank-16 `c=0` ledger, prove
Grand List or Grand MCA, or move the official score.

For an arbitrary root-free degree-67472 generator, the compiler reduces the
remaining cap-116 theorem-or-counterexample problem to the literal valid-edge
graph inside the high-tail collision classes.  A 117-edge family must force
either a collision class of size at least nine, or a size-eight class with at
least 25 valid edges.  Every edge must still pass the splitting,
squarefreeness, footprint, q32-pairing, prior-owner, and first-match filters.
After #843, rank two remains at its cubic/quartic split-block wall; ranks
three through six remain transverse/syzygetic.  Any eventual global cap must
be uniform over every core, generator, syndrome, and residue ray and must
compose into #838 without double spending.

## Reproducibility

The standard-library verifier is
`experimental/scripts/verify_rank16_fixed26_divided_difference_source_compiler.py`.
Its semantic manifest, frozen expected output, and checksums are under
`experimental/data/certificates/rank16-fixed26-divided-difference-source-compiler/`.
It replays the source identities in deterministic finite-field models, checks
the deployed parameter identities and monomial formula, computes the finite
cap 37, retains the literal filter contract, and runs fail-closed semantic
tamper tests.  Normal and optimized Python runs must be byte-identical.
