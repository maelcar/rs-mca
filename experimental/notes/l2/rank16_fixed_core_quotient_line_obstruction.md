# Rank-16 fixed-core quotient-line obstruction

Claim: In one literal root-free fixed-syndrome projective residue cell with a fixed 27-element `q64` core, six distinct extra full-fiber labels cannot have normalized Pade quotients on one affine line.
Status: PROVED local theorem and ROUTE_CUT; it makes no finite-ledger payment and the official score remains `0/2`.
Verifier: `experimental/scripts/verify_rank16_fixed_core_quotient_line_obstruction.py` is an arithmetic replay for every deployed degree and threshold inequality, the conditional cap-eight ledger, and fail-closed mutations; the theorem proof is audited separately.
Consumers: Any six-candidate family, and in particular any nine-label counterexample to the pending cap eight, has normalized quotient affine dimension at least two.
Risk-limits: The theorem does not prove affine-line ownership, the cap eight, a nine-label counterexample, a parent saving, a rank-16 closure, Grand List, or Grand MCA.

## Deployed source cell

Work over

```text
p = 2130706433,
H = mu_(2^21) in F_p^x,
n = 2097152,
K = 1048576,
m = 1116047,
t = n-m = 981105,
sigma = m-K = 67471,
a = sigma+1 = 67472,
B = 32768.
```

Fix a 27-element set `C` of `q64` labels and put

```text
G_C(X) = product_(z in C) (X^B-z).
```

In one root-free fixed-syndrome projective residue ray, cancellation of the
fixed core gives, for every remaining label `y`,

```text
A_y(X) = (X^B-y) R_y(X) = q_y h(X) + g(X) W_y(X),       (1)
```

where

```text
q_y != 0,
deg g = a = 67472,
g(x) != 0 for every x in H,
deg A_y = D = t-27B = 96369,
deg R_y = D-B = 63601,
deg W_y <= w = D-a = 28897.
```

Each `A_y` is a squarefree polynomial splitting completely over `H`. The
theorem below only needs complete splitting, not squarefreeness or the other
residual-footprint and nonpairing restrictions.

## Exact theorem

Let `y_1,...,y_s` be distinct labels outside `C`, and let (1) hold with the
same `g` and `h` for every index. Normalize

```text
P_i = q_i^(-1) A_i = h + g V_i,
V_i = q_i^(-1) W_i.
```

If the normalized quotients lie on one affine line,

```text
V_i = V_0 + c_i V_1,
```

then

```text
s <= 5.                                                    (2)
```

Thus every family of six surviving candidates has normalized quotient affine
dimension at least two. In particular, a source-realized nine-label
counterexample to the pending cap-eight theorem cannot be owned by one
normalized quotient pencil.

## Proof

Assume `s >= 6`. If all `V_i` are equal, then all `P_i` are equal. Scalar
normalization preserves roots, so the six pairwise coprime factors
`X^B-y_i` divide one nonzero degree-`D` polynomial. This forces `6B <= D`,
contrary to

```text
6B = 196608 > 96369 = D.
```

Otherwise choose indices `j,k` with `V_j != V_k`. Because the quotients lie
on one affine line, they can be reparametrized as

```text
V_i = V_j + d_i (V_k-V_j),
H_0 = P_j = h + g V_j,
H_1 = g (V_k-V_j),
P_i = H_0 + d_i H_1.
```

Here `H_0` and `H_1` are nonzero, and the direction is the difference of two
actual quotients. Therefore `deg V_j <= w`, `deg(V_k-V_j) <= w`,
`deg H_0=D`, and `deg H_1 <= a+w=D`.

Let `zeta` generate `mu_B` and define the cross polynomial

```text
Psi(X) = H_0(zeta X) H_1(X) - H_0(X) H_1(zeta X).
```

Both pencil generators have degree at most `D`, so `deg Psi <= 2D`. For every
root `x` in the full fiber `x^B=y_i`, both `x` and `zeta x` are roots of
`P_i`. Substituting `H_0=-d_i H_1` at those two points gives `Psi(x)=0`
without dividing by `H_1(x)`. The six full fibers are disjoint and contribute
`6B` roots. Since

```text
6B = 196608 > 192738 = 2D,
```

we have `Psi=0`.

Write

```text
J = gcd(H_0,H_1),
H_0 = J A,
H_1 = J E,
gcd(A,E)=1.
```

Then

```text
A(zeta X) E(X) = A(X) E(zeta X).                          (3)
```

Coprimality in (3) gives `A(X) | A(zeta X)` and
`E(X) | E(zeta X)`. Degrees agree, so there are nonzero constants
`lambda_A,lambda_E` with

```text
A(zeta X)=lambda_A A(X),
E(zeta X)=lambda_E E(X).
```

Equation (3) makes the two constants equal. A polynomial satisfying this
semi-invariance has all exponent degrees in one residue class modulo `B`.
Hence, for one `0 <= r < B`,

```text
A(X)=X^r U(X^B),
E(X)=X^r V(X^B).
```

The same residue `r` occurs because the characters are equal. Since `A` and
`E` are coprime, `r=0`. Therefore

```text
A,E in F_p[X^B],
P_i/J = A+d_iE in F_p[X^B].                               (4)
```

The common divisor `J` divides every `P_i`. Each `P_i` is a nonzero scalar
multiple of a polynomial splitting over `H`, so `J` also splits over `H`.
On the other hand, `J | H_1=g(V_k-V_j)`. The roots of `J` lie in `H`, while
`g` has no root in `H`; therefore `gcd(J,g)=1`, so `J | (V_k-V_j)` and

```text
deg J <= deg(V_k-V_j) <= w = 28897.                        (5)
```

By (4), `D-deg J = deg(P_i/J)` is a multiple of `B`. By (5), it lies in

```text
[D-w,D] = [67472,96369].
```

There is no multiple of `32768` in this interval:

```text
2B = 65536 < 67472,
3B = 98304 > 96369.
```

This contradiction proves (2).

## Source compiler

The post-core equation (1) is a modular inverse reduction, not literal
division of a chosen syndrome representative.

Before deleting the fixed core, let the full locator be `L_i=G_C A_i`, and
let the source ray give

```text
L_i == q_i h_src  (mod g).
```

Every root of `G_C` lies in `H`, while `g` is root-free on `H`. Therefore
`gcd(G_C,g)=1`, and `G_C` has an inverse modulo `g`. Define the canonical
post-core representative

```text
h = rem_g(G_C^(-1) h_src).
```

Then `A_i == q_i h (mod g)`, which gives (1). Because `deg h<a`,
`deg A_i=D`, and `deg g=a`, the quotient satisfies

```text
deg W_i <= D-a = 28897.
```

This preserves the literal field, subgroup, source ray, fixed core, and extra
full-fiber labels. It does not assert that an arbitrary fixed-core family is
affine-collinear after normalization.

## Finite ledger and exact remaining wall

There is no unconditional ledger payment. The pending transition is still

```text
nonpaired cap 8: top total = 272133314965102416,
target margin              =   2720795531085176,
nonpaired cap 9: top total = 301327693533216784,
target excess              =  26473583037029192.
```

The theorem says that a cap-nine witness, if it exists, cannot come from
affine quotient dimension zero or one. The exact surviving object is a
simultaneous-Pade family of affine quotient dimension `r` with

```text
2 <= r <= 8.
```

A degree-at-most-eight Lagrange interpolation in the label variable is a
convenient parametrization, not an equivalent dimension bound: its coefficient
span must still have affine dimension `r` in the displayed range. Every one of
the nine residual polynomials must satisfy all seven live source conditions:

1. degree exactly `63601`;
2. monic and squarefree;
3. split completely over `H`;
4. no root in the 28 selected full fibers;
5. no additional complete `q64` fiber;
6. residual `q64` footprint at least four; and
7. full `q64` label set with `q32` full-pair count at most 13.

Any next proof must combine those conditions with the literal fixed-syndrome
congruences. A dimension count or an abstract support packing is not enough.

## Novelty and nonclaims

At `origin/main@02728b208`, the integrated rank-16 packets contain periodic,
active-pencil, fixed-core counting, and owner ledgers, but no theorem excluding
one affine line of normalized fixed-core Pade quotients. This theorem is
orthogonal to the integrated rank-15 D-range exclusions and to the global
pair-intersection/moment payments.

No affine-line owner is proved. No cap eight, fixed-26-core cap, nine-label
construction, lower-`q64` payment, `q128` payment, owner/add-back step,
rank-16 parent closure, asymptotic result, Grand List theorem, Grand MCA
theorem, deployed solve, or official score change is claimed.

The Lean file
`experimental/lean/grande_finale/GrandeFinale/Rank16FixedCoreQuotientLineObstruction.lean`
records the exact hypotheses and conclusion as an unproved statement target.
