# Realized-image energy lift on a Boolean slice

## Status and scope

This note proves an exact source-level inequality for a realized additive
image and an arbitrary residual subset of one fixed-weight fiber.  It gives a
new fixed-density refinement of the universal `f L <= 3^N` image atom and an
energy-sensitive Sidon cutoff.  It does **not** prove the signed multi-class
inverse theorem, all of hard input 2, a rooted ray compiler, Grand MCA, Grand
List, or a deployed finite crossing.

Let

```text
Omega_m = {x in {0,1}^N : |x| = m},
Phi : Z^N -> G,
S_m = Phi(Omega_m),
L = |S_m|,
```

where `G` is a finite abelian group.  Fix `s in S_m`, and let

```text
F subseteq Omega_m intersect Phi^{-1}(s),   f = |F| > 0.
```

The set `F` may be a proper first-match residual subset.  Define its additive
energy in the torsion-free incidence group by

```text
E(F) = |{(a,b,c,d) in F^4 : a+b=c+d in Z^N}|,
Delta(F) = E(F)/f^3.
```

Thus `1/f <= Delta(F) <= 1`.

## Exact theorem

Put

```text
A(N,m) = [z^(2m)] (1+z+z^2)^N,
B(N,m) = [z^(3m)] (1+z+z^2+z^3)^N.
```

Let `h_2` be binary entropy, set

```text
a(p) = 1 + h_2(p)/2,
q_0(p) = (1-p)^2/2,
q_1(p) = (1-p^2)/2,
q_2(p) = p(2-p)/2,
q_3(p) = p^2/2,
g(p) = H_2(q_0(p),q_1(p),q_2(p),q_3(p)).
```

For `theta=m/N`, every `F` above satisfies

```text
f L <= A(N,m),                                      (1)
f L <= B(N,m) Delta(F),                             (2)
f L <= 2^(N a(theta)),                              (3)
f L <= 2^(N g(theta)) Delta(F).                     (4)
```

Consequently, with

```text
D(N,m) = min(A(N,m), 2^(N a(theta))),
K(N,m) = min(B(N,m), 2^(N g(theta))),
```

one has

```text
f L <= D(N,m),
f L <= K(N,m) Delta(F).                             (5)
```

The entropy bounds (3)--(4) also hold with `L` equal to the full
realized image of the cardinality-augmented map

```text
x |-> (|x|, Phi(x))
```

on the whole Boolean cube, provided `F` is one augmented fiber.

## Proof

Choose one representative `tau(u) in Omega_m` for each `u in S_m`.  The map

```text
F x S_m -> {0,1,2}^N,   (x,u) |-> x+tau(u),
```

is injective: applying `Phi` recovers `u`, after which the chosen
representative recovers `x`.  Every output has coordinate sum `2m`, proving
(1).

The `L` sets `F+F+tau(u)` are pairwise disjoint.  Their union lies in the
`3m` layer of `{0,1,2,3}^N`, so

```text
L |F+F| <= B(N,m).
```

If `r(z)=|{(x,y) in F^2:x+y=z}|`, then Cauchy--Schwarz gives

```text
f^4 <= |F+F| sum_z r(z)^2 = |F+F| E(F).
```

Combining the last two displays gives `f L <= B(N,m) Delta(F)`, which is
(2).

For the entropy refinements, augment `Phi` by cardinality.  Its Boolean image
has the complement involution

```text
J(u) = Phi_tilde(1)-u.
```

On each orbit choose realized representatives `y` and `1-y`, and choose
uniformly between the two orientations.  This produces a realized syndrome
`U` and an independent representative `Y` such that every coordinate of `Y`
has marginal `1/2`.

Let `X` be uniform on `F`.  The syndrome `U` is determined by `X+Y`, while
`X` is recovered from `(X+Y,U,Y)`.  Hence

```text
log_2(fL) <= H(X+Y)
            <= sum_i H(X_i+Y_i)
            <= N a(theta),
```

where the last step is entropy concavity.  This proves (3).

For two independent copies `X_1,X_2`, Renyi monotonicity gives

```text
H(X_1+X_2) >= log_2(f/Delta(F)).
```

The coordinate law of `X_1+X_2+Y` is the four-vector defining `g(p_i)`.
The function `g` is symmetric and strictly concave, so the same argument gives

```text
log_2(fL/Delta(F)) <= N g(theta),
```

which is (4).

## Fenced-wall consequence

Suppose `L_all` is the full image of the cardinality-augmented map, `F` is
one augmented fiber, and

```text
(f L_all)^(1/N) > 2^(4/3).
```

Then

```text
h_2(theta) > 2/3,
Delta(F) > 2^(-N(g(theta)-4/3)).                    (6)
```

The function `g` is maximized at `1/2`, where

```text
g(1/2) = 3-(3/4)log_2(3),
g(1/2)-4/3 = 0.477944791125799... .
```

Thus every finite fenced wall obeys

```text
-log Delta(F)/N < 0.331286084432160... .           (7)
```

Using the already recorded sharp Boolean-cube energy theorem
`E(F) <= f^(log_2 6)` and `L_all <= 2^N` also gives the lower restriction

```text
ln(4/3)/3 < -log Delta(F)/N.                       (8)
```

The strict inequalities in (6)--(8) are finite wall statements.  Limits of
families need not retain a strict endpoint without a uniform wall margin.

## Primitive Sidon compiler

Return to a fixed slice.  Put

```text
M = binom(N,m),   barN = M/L,
F_s subseteq Omega_m intersect Phi^{-1}(s),
f_s = |F_s|,      Delta_s = E(F_s)/f_s^3.
```

For every nonempty residual fiber, (5) gives the exact normalized estimate

```text
f_s/barN <= min(D(N,m)/M, K(N,m) Delta_s/M).        (9)
```

Consequently the source Sidon-heavy moment satisfies

```text
G_sid(q,sigma)
 <= [min(D(N,m)/M, exp(-sigma N)K(N,m)/M)]^q.       (10)
```

Define

```text
kappa(N,m) = (1/N) ln(K(N,m)/M).
```

Then (10) pays the range

```text
sigma >= max(0,kappa(N,m)).                         (11)
```

This is a cutoff theorem, not payment for every fixed `sigma>0`.  If
`f_s/barN >= exp(eta N)`, then (9) forces

```text
Delta_s >= exp(-N(kappa(N,m)-eta)).                 (12)
```

Let `alpha=log_2(4/3)`.  Combining (12) with the sharp Boolean-cube energy
upper bound confines every positive-rate surviving fiber to

```text
alpha eta <= -ln Delta_s/N <= kappa(N,m)-eta.       (13)
```

The exact remaining wall is a source-specific multi-class amplification or a
canonical paid-cell emission on this fixed-exponential band.  Generic BSG
constants, the bounded-denominator horn, and the already known Prouhet block
do not close (13).  The witness atlas and rooted completed-ray compiler remain
separate obligations.

## Verification

`experimental/scripts/verify_realized_image_energy_lift.py` checks the exact
integer inequalities on exhaustive small cyclic syndrome maps, checks the
cardinality-augmented entropy form, reproduces all displayed constants, and
rejects a strengthened extra-`Delta` tamper.
