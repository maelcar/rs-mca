# Weighted cyclic-GRS half-footprint compiler

## Status

`PROVED / NARROW SALVAGE / OFFICIAL SCORE 0/2`

This note records exactly two results surviving the hostile audits of R16 Role
02:

1. a literal weighted cyclic-GRS to arbitrary code-alphabet-linear `Phi`
   half-footprint compiler, including a source realization of every `Phi` and
   the exact discrepancy/nonvanishing identity; and
2. an exact-footprint core-root budget of `L-1`.

No uniform common-27 occupancy bound is proved.  In particular, this note does
not prove `M<=561` or `M<=1417`, does not provide a paid tail consumer,
does not justify a factor-10 parent ledger, and does not move Grand List or
Grand MCA.  The official score remains `0/2`.

## Cyclic weighted source

Let `B=F_p`, with `p` prime, and let `E/B` be a field extension.  Identify
`B` with its canonical subfield in `E`.  The deployed code alphabet is

```text
E=F_{p^6}.
```

This instantiated field ledger is the sextic extension-field layer.  It is
not the separate base-field one-row object in which both the code and list
fields are `B=F_p`.  The identities below specialize algebraically to `E=B`,
but any base-field owner map, occupancy theorem, or parent payment must be
attached and audited again in that source layer.

Let

```text
q0=2k,                n=q0 L,               K=kL,
n | p-1,
H=mu_n subset B^*,    Q=mu_q0 subset B^*.
```

For the deployed row,

```text
p     = 2^31-2^24+1 = 2,130,706,433,
n     = 2^21        = 2,097,152,
K     = 2^20        = 1,048,576,
m     =                         1,116,047,
q0    = 64,
k     = 32,
L     = 2^15        = 32,768,
sigma = m-K         = 67,471.
```

Here `q0` is the outer quotient length.  It is not the challenge-alphabet
cardinality `|E|=p^6`; this packet does not change or cancel the literal
`p^6` denominator.

The map

```text
pi:H -> Q,                 pi(x)=x^L                         (1)
```

is a surjective quotient homomorphism of multiplicative groups.  Its kernel is
`mu_L`; hence every fiber

```text
F_y={x in H:x^L=y}
```

has exactly `L` elements.  Equation (1) is a power map on a multiplicative
cyclic group.  It is not a Frobenius map and is not a subfield descent.  In
particular, `Q=mu_64` is used only as a multiplicative roots-of-unity set, not
as a subfield of `F_p`.

Fix arbitrary multipliers

```text
v=(v_x)_{x in H} in (E^*)^H
```

and the literal weighted code

```text
GRS_K(H,v)={(v_x P(x))_{x in H}: P in E[X], deg P<K}.       (2)
```

For an arbitrary received word `R=(R_x)_{x in H}`, divide coordinatewise by
the nonzero multipliers:

```text
r_x=R_x/v_x.                                                (3)
```

This is a monomial Hamming isometry: `R_x=v_x P(x)` if and only if
`r_x=P(x)`.

For each `y in Q`, evaluation on the `L` distinct points of `F_y` identifies
`r|F_y` with a unique polynomial

```text
u_y(X) in W:=E[X]_{<L}.                                     (4)
```

Put `V=E[Z]_{<k}`.

## Theorem 1: exact half-footprint compiler

For every received word `R`, define

```text
lambda_y = (prod_{z in Q\{y}} (y-z))^{-1} = y/q0,           (5)
s_j       = sum_{y in Q} lambda_y y^j u_y in W,
             0<=j<k,                                       (6)
Phi(sum_{j=0}^{k-1} f_j Z^j) = sum_{j=0}^{k-1} f_j s_j.     (7)
```

Then `Phi:V->W` is `E`-linear.  The construction is surjective onto
`Hom_E(V,W)`: every linear `Phi` is induced by a literal received word for
every choice of nonzero multiplier vector `v`.

More explicitly, for an arbitrary `Phi`, set `s_j=Phi(Z^j)` and define

```text
u_y = sum_{j=0}^{k-1} y^{-(j+1)} s_j.                       (8)
```

The roots-of-unity orthogonality relation gives, for `0<=i<k`,

```text
sum_{y in Q} (y/q0)y^i u_y
 = (1/q0) sum_j s_j sum_{y in Q} y^{i-j}
 = s_i.                                                     (9)
```

Here `-(k-1)<=i-j<=k-1`, so `q0=2k` divides `i-j` only when `i=j`.
Evaluate `u_y` on `F_y` and restore the literal weights:

```text
R_x=v_x u_{x^L}(x).                                        (10)
```

Equations (3)--(10) prove source realization for every `Phi`.  The forward
map from received words to `Phi` is surjective, not injective; the two-way
compiler claim is exact realization, not a false bijection.

### Outer-code bookkeeping

Every `P in E[X]_{<K}` decomposes uniquely as

```text
P(X)=sum_{r=0}^{L-1} X^r p_r(X^L),       p_r in E[Z]_{<k}. (11)
```

Thus (2), after (3), is a length-`q0`, dimension-`k` Reed--Solomon code on
the evaluation set `Q` with alphabet the `E`-vector space `W`.  The set
`Q` is not treated as a field, and `W` is used only as an `E`-vector
space.

### Exact discrepancy identity

Let `J subset Q` have `|J|=k`.  There is a unique codeword `P_J` agreeing with
`u` on all fibers indexed by `Q\J`: interpolate each of the `L` coefficient
functions in (11) on those `k` points.  Write its fiber residue as
`(P_J)_y in W` and put

```text
e_{J,y}=u_y-(P_J)_y,
q_{J,y}(Z)=prod_{z in J\{y}}(Z-z) in V.                    (12)
```

For every `y in J`,

```text
Phi(q_{J,y})=lambda_y q_{J,y}(y) e_{J,y}.                  (13)
```

The outer codeword has zero syndromes (6), coefficientwise: if `a(Z)` has degree `<k`,
then `Z^j a(Z)` has degree at most `2k-2=q0-2`, and the Lagrange leading-
coefficient identity on `Q` gives
`sum_y lambda_y y^j a(y)=0`.  Thus subtracting `P_J` does not change (7).
The discrepancy vanishes off `J`, while `q_{J,y}` vanishes on `J\{y}`;
only the `y` summand remains, proving (13).
Every scalar on the right of (13) is nonzero, so

```text
Phi(q_{J,y})=0   iff   e_{J,y}=0.                           (14)
```

Consequently, `J` is exactly the set of non-full-agreement fibers of `P_J` if
and only if

```text
Phi(q_{J,y}) != 0 for every y in J.                         (15)
```

Under (15), the exact agreement count is

```text
kL + sum_{y in J} |{x in F_y:Phi(q_{J,y})(x)=0}|.           (16)
```

The scalar relation (13) makes the roots in (16) exactly the roots of the
literal normalized discrepancy.  The nonzero multipliers preserve the same
coordinate equalities in the weighted code.  In the deployed row, the
threshold condition is that the sum in (16) is at least
`sigma=67,471`; no bound on the number of such `J` is asserted here.

## Theorem 2: exact-footprint core-root budget

Specialize now to the deployed `k=32`.  Let `A subset Q`, `|A|=27`, and define

```text
L_A(Z)=prod_{a in A}(Z-a),
A_a(Z)=prod_{b in A\{a}}(Z-b)=L_A(Z)/(Z-a).                (17)
```

Let

```text
U_A <= E[Z]_{<=5}
```

be any `E`-linear subspace.  For `a in A`, define the literal common-root set

```text
Z_a(U_A)={x in F_a:
  Phi(A_a L)(x)=0 for every L in U_A}.                      (18)
```

For every `S subset A` and every `T in E[Z]_{<=4}`, if

```text
(Z-a)T in U_A for every a in S,                            (19)
Phi(L_A T) != 0,                                           (20)
```

then

```text
sum_{a in S} |Z_a(U_A)| <= L-1.                            (21)
```

All degree bookkeeping is literal: `deg(A_a L)<=26+5=31` and
`deg(L_A T)<=27+4=31`, so every input to `Phi` lies in `V=E[Z]_{<32}`.

### Proof

Fix `a in S` and `x in Z_a(U_A)`.  By (19), use `L=(Z-a)T` in (18):

```text
0=Phi(A_a (Z-a)T)(x)=Phi(L_A T)(x).                        (22)
```

The fibers `F_a` are pairwise disjoint.  Hence the left side of (21) counts a
disjoint set of roots of the single polynomial `Phi(L_A T)`.  By (20), that
polynomial is nonzero; it lies in `W=E[X]_{<L}` and therefore has at most
`L-1` roots.  This proves (21).

The exact-footprint specialization is as follows.  If `R subset Q\A` has five
elements, `J=A union R` is an exact footprint, `y in R`, and

```text
T=prod_{r in R\{y}}(Z-r),
```

then `L_A T=q_{J,y}`.  Condition (20) follows from (15).  Thus (21) applies
whenever the core memberships (19) actually hold.  The theorem does not claim
that they hold for an exhaustive family of owners.

## Consumed locator corollary, not novelty

For a nonempty family of degree-five split locators

```text
L_R(Z)=prod_{r in R}(Z-r),          R in binom(C,5),
C subset Q,                         |C|=37,
```

reserve the names

```text
d_loc = dim_E span_E{L_R}-1,
g_loc = deg gcd{L_R}.                                      (23)
```

Because every `L_R` has coefficients in `B subset E`, this `E`-dimension is
the dimension of the `B`-linear span after scalar extension.

Pending `#747` supplies the split-locator-star flat-intersection theorem.  Its
already-owned corollary gives the caps

```text
d_loc=0,1,2  ->  1,33,561.                                (24)
```

Equation (24) is consumed from `#747`; it is not new content of this packet.
Moreover, `g_loc>=3` implies `d_loc<=5-g_loc<=2` after the common factor is
removed, so it is not a separate exclusion and is not advertised as one.

The names in (23) are deliberately distinct from the ongoing source
invariants `r_T` and `g_inner`.  No compiler from `d_loc` to `r_T`, from
`g_loc` to `g_inner`, or conversely is proved here.  Therefore (24) does not
give a uniform `M<=561` theorem for the live `q0=64` outer-quotient residual.

## Exact remaining wall and nonclaims

- This packet does not supply an exhaustive paid first-match consumer.  An
  external first-32/fractional owner map may cover the outer-quotient
  footprint-`>=33`
  tail, but it still requires a true weighted occupancy theorem before it pays
  the parent ledger; this compiler proves no such cap.
- There is no theorem identifying the locator coordinates `d_loc/g_loc` with
  the live `q0=64` outer-quotient coordinates `r_T/g_inner`.
- The `1,33,561` caps are the consumed `#747` locator-flat corollary.  They do
  not prove a uniform `M<=561`, and this packet proves no uniform `M<=1417`.
- No six-cell locator list is promoted to the official residual.  Such a list
  would require the missing invariant compiler and a paid tail consumer.
- No common-27 parent double count is used as an official consumer.  No
  `1417/1418` allowance, factor-10 parent recurrence, or parent saving is
  claimed.
- The pinned sextic-layer compiler is not substituted into the distinct
  base-field one-row ledger.  In particular, it does not pay that ledger's
  weighted tail obligation.
- No finite deployed list ceiling, Grand List theorem, Grand MCA theorem, or
  asymptotic theorem follows.  Official score: `0/2`.

## Verification

`experimental/scripts/verify_weighted_cyclic_grs_half_footprint_compiler.py`
is dependency-free and uses explicit runtime checks rather than `assert`.  It
exhausts a complete weighted `F_5` source fixture in the forward and inverse
directions, exhausts every linear `Phi` on a nontrivial-fiber `F_17` fixture,
checks quotient fibers, source realization, (13)--(16), exhaustive toy
core-root cases including equality, the exact deployed constants, and a suite
of deliberately corrupted mutations.  Its normal and `python -O` outputs are
required to be byte-identical and are frozen under
`experimental/data/certificates/weighted-cyclic-grs-half-footprint/`.
These exhaustive fixtures are explicitly prime-field evidence only.  The
extension-field theorem is proved symbolically above; the verifier also pins
`|E|=p^6` and does not reinterpret `q0=64` as that denominator.
