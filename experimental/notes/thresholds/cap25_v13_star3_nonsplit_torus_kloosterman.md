# KoalaBear star3 nonsplit-torus Kloosterman reduction

## Status

`PROVED REDUCTION / SIGNED-ROUTE BRIDGE / DEPLOYED ROW STILL OPEN`

This note rewrites the exact `star3` incidence count from the point-count
packet as a norm-one-torus average, diagonalizes that average by Fourier
inversion, and identifies every nonexceptional torus mode with a classical
Kloosterman sum.  It preserves the sign of the remaining correlation.

The rational conic parametrization, the balanced moment-kernel dictionary, and
the principal-term centering and residual budget already exist elsewhere in
the repository.  The new content here is the nonsplit-torus Fourier
decomposition, its exact `-Kl_p` kernel, the exceptional-mode classification,
and the rewrite of the already-banked centered target in those signed
Kloosterman coordinates.

Concretely, the rational formulas used by the verifier are exactly the
parametrization in `experimental/notes/roadmaps/x12_h3_parametrization.md`
after normalizing the source triple to `(1,a,b)`, substituting `t=-u-1`, and
swapping the final two outputs.  They are used as an imported finite check of
the torus organization, not claimed as a new parametrization.

This note does not prove `P<=H2` or close `star3`.

## Exact incidence

Let `p>3` be prime with `p=2 mod 3`, let

```text
psi(z)=exp(2 pi i z/p),
```

let `A subseteq F_p`, and fix `zeta in F_p\A`.  Let `P_A(zeta)` count
unordered incidences

```text
({x,y},{a,b,c})
```

with `x,y,a,b,c in A`, `x!=y`, `a,b,c` pairwise distinct, and

```text
a+b+c=x+y+zeta,
ab+ac+bc=xy+zeta(x+y).                                  (1)
```

Put

```text
E=F_{p^2}=F_p[rho]/(rho^2+rho+1).
```

The polynomial is irreducible because `p=2 mod 3`; conjugation sends
`rho` to `rho^2`.  Let

```text
T={t in E^*: N(t)=1},   |T|=p+1.                        (2)
```

For each ordered `x,y in A`, `x!=y`, define

```text
s=x+y+zeta,
r=x+rho y+rho^2 zeta,
rbar=x+rho^2 y+rho zeta.
```

Then `r!=0`.  For `t in T`, set

```text
a_t=(s+t r+t^(-1) rbar)/3,
b_t=(s+rho^2 t r+rho t^(-1) rbar)/3,
c_t=(s+rho t r+rho^2 t^(-1) rbar)/3.                    (3)
```

All three values lie in `F_p`.

### Theorem 1 (norm-one-torus parametrization)

The map `t -> (a_t,b_t,c_t)` is a bijection from `T` to the ordered triples
in `F_p^3` having the same first two elementary symmetric functions as
`(x,y,zeta)`.

If

```text
F_A(a,b,c)=1_A(a)1_A(b)1_A(c)1_{a,b,c pairwise distinct},
```

then

```text
12P_A(zeta)
 = sum_{x,y in A, x!=y} sum_{t in T} F_A(a_t,b_t,c_t).   (4)
```

The factor `12` is exactly two orderings of `{x,y}` times six orderings of
`{a,b,c}`.

### Proof

For a triple `(x,y,z)`, put

```text
s=x+y+z,
r=x+rho y+rho^2 z,
rbar=x+rho^2 y+rho z.
```

The inverse three-point Fourier transform gives

```text
x=(s+r+rbar)/3,
y=(s+rho^2 r+rho rbar)/3,
z=(s+rho r+rho^2 rbar)/3.                               (5)
```

Direct multiplication gives

```text
r rbar=s^2-3e_2(x,y,z).                                 (6)
```

Thus fixed `(e_1,e_2)` is equivalent to fixed `s` and fixed norm `r rbar`.
For `(x,y,zeta)`, `r=0` would force `x=y=zeta` by (5), impossible.  Every
other element of the same nonzero norm fiber is uniquely `tr` with `N(t)=1`.
Substitution into (5) proves (3) and the bijection.  Equal-high partner triples
cannot share a point with `{x,y,zeta}`: the corresponding monic cubics would
share a root while differing only by a constant, forcing equality, contrary
to `zeta notin A`.  This proves (4).

## Exact Kloosterman transform

Use the unnormalized transform

```text
Fhat_A(lambda_0,lambda_1,lambda_2)
 = sum_{a,b,c} F_A(a,b,c)
   psi(-lambda_0 a-lambda_1 b-lambda_2 c).               (7)
```

For `lambda=(lambda_0,lambda_1,lambda_2)`, put

```text
L=lambda_0+lambda_1+lambda_2,
kappa=lambda_0+rho^2 lambda_1+rho lambda_2,
Q(x,y)=x^2+y^2+zeta^2-xy-xzeta-yzeta.                   (8)
```

For `x!=y` in `A`, `Q(x,y)!=0`.  Define

```text
Kl_p(c)=sum_{w in F_p^*} psi(w+c/w),   c!=0,             (9)
Delta={(h,h,h):h in F_p}.
```

### Theorem 2 (diagonal plus signed Kloosterman block)

```text
12P_A(zeta)=C_diag+C_Kl,                                 (10)
```

where

```text
C_diag=(p+1)/p^2
       sum_{x,y in A, x!=y} N_A(x+y+zeta),               (11)

N_A(s)=#{(a,b,c) in A^3:
         a,b,c pairwise distinct, a+b+c=s},
```

and

```text
C_Kl=-1/p^3 sum_{x,y in A, x!=y}
              sum_{lambda in F_p^3\Delta}
 Fhat_A(lambda) psi(L(x+y+zeta)/3)
 Kl_p(N(kappa)Q(x,y)/9).                                 (12)
```

Every one of the `p^3-p` non-diagonal modes is an exact classical
Kloosterman mode.  The only modes without this internal square-root
cancellation are the `p` diagonal modes.

### Proof

Fourier inversion and (3) reduce the torus kernel to

```text
W(alpha)=sum_{t in T} psi(Tr(alpha t)).                  (13)
```

Clearly `W(0)=p+1`.  For `alpha!=0`, multiplication by `alpha` identifies
`T` with a nonzero norm fiber.  The exact trace/norm histogram is

```text
#{y in E:N(y)=c, Tr(y)=s}=1-chi(s^2-4c),                 (14)
```

where `chi(0)=0`.  Comparing with the split quadratic histogram

```text
#{w in F_p^*:w+c/w=s}=1+chi(s^2-4c)                     (15)
```

and using `sum_s psi(s)=0` gives

```text
W(alpha)=-Kl_p(N(alpha)).                                (16)
```

The condition `kappa=0` is equivalent to
`lambda_0=lambda_1=lambda_2`, because `(L,kappa,kappabar)` is the three-point
Fourier transform of `lambda`.  Substituting (16) proves (12).  Summing the
diagonal modes by additive orthogonality proves (11).

The classical Weil estimate gives

```text
|Kl_p(c)|<=2 sqrt(p),   c!=0.                            (17)
```

Reference: A. Weil, *On some exponential sums*, Proc. Natl. Acad. Sci. USA
34 (1948), 204-207, doi:10.1073/pnas.34.5.204.

## Deployed KoalaBear normalization

For the deployed row,

```text
p=2130706433,        n=2^21,
omega=1213133211,    m=|A|=1183519,
A={omega^0,...,omega^(m-1)},   zeta=omega^m,
H2=77291948627,
D2=m(m-1)=1400716039842,
D3=m(m-1)(m-2)=1657771245325684314.                     (18)
```

The point-count packet already proves that the principal contribution satisfies

```text
12P_main=D2 D3/p^2=511478602661.4981...,
12H2=927503383524.                                       (19)
```

and already records the corresponding residual budget.  The new reduction
rewrites that same condition as the single signed torus/Kloosterman target

```text
(C_diag-D2 D3/p^2)+C_Kl
 <= 1888715022792167261828558596848
    /4539909903627583489
 = 416024780862.5018....                                 (20)
```

At this prime,

```text
2sqrt(p)<92320,   p+1=2130706434.                        (21)
```

This is a modewise gain of more than `23079`, but it is not an aggregate
bound.  Applying (17) termwise and then taking absolute values destroys the
joint sign in (12) and misses (20) by many orders of magnitude, exactly as
the integrated second-moment route cut predicts.  The diagonal block (11) is
also not automatically small and must be centered jointly with (12).

For explicit coefficient work, if

```text
G_A(h)=sum_{a in A} psi(-ha),
```

then inclusion-exclusion gives

```text
Fhat_A(lambda_0,lambda_1,lambda_2)
 = G_A(lambda_0)G_A(lambda_1)G_A(lambda_2)
 - G_A(lambda_0+lambda_1)G_A(lambda_2)
 - G_A(lambda_0+lambda_2)G_A(lambda_1)
 - G_A(lambda_1+lambda_2)G_A(lambda_0)
 + 2G_A(lambda_0+lambda_1+lambda_2).                     (22)
```

Thus (20) is a fully explicit signed Kloosterman correlation of five copies
of the deployed multiplicative-prefix transform.

## Exact remaining target

Prove (20) by a product-sensitive trace-function/Kuznetsov estimate that
retains the joint phase

```text
Fhat_A(lambda)
psi(L(x+y+zeta)/3)
Kl_p(N(kappa)Q(x,y)/9),                                  (23)
```

specialized to the deployed multiplicative prefix.  No absolute values may
be inserted between these three factors.

## Nonclaims

- This note does not prove `P<=H2`, `|T(n',3)|<=H2`, the large-`e` paucity
  bound, a deployed adjacent-row inequality, or the prize theorem.
- The rational conic parametrization is not claimed as new.
- The balanced-ternary moment-kernel dictionary is not claimed as new.
- The Weil bound is only cancellation in the internal torus variable.  It
  does not supply the aggregate signed estimate (20).
- No value of the deployed incidence `P` is computed here.

## Verification

`experimental/scripts/verify_star3_nonsplit_torus_kloosterman.py` checks the
rational orbit count against direct incidence enumeration on three nonsplit
toy rows, exhausts the norm/trace histogram, reconstructs (10)-(12) on two
toy rows, and verifies all displayed deployed integer normalizations,
including `m=n/2+2e-1` and the exact order of the printed `omega`.
