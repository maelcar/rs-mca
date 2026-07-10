# C9 sparse-pair actual-syndrome compiler

## Status

`PROVED / STRICT SUBREGIME / PARTIAL PROFILE-LD PAYMENT`

This note pays one explicit infinite class of positive-entropy endpoint profiles
whose original block-variance deficit is linear.  It does not pay arbitrary
fixed profiles.  The case `b=2` is the previously banked adjacent-pair
compiler.  The new input is the fixed-dyadic spacing generalization and its
payment for every endpoint density below `1/4`: it compiles every actual
syndrome fiber to a shorter consecutive Vandermonde fiber, after which a
hidden short-weight split crosses the one-block Plotkin line.

## The finite compiler

Let

```text
N=2^s,   2 <= b=2^r <= N/2,   M=N/b,
```

let `p` be an odd prime with `N | (p-1)`, let `zeta` have order `N` in
`F_p^*`, put `xi=zeta^b`, and fix nonzero `alpha,c in F_p`.  Let
`2 <= D <= M`.  At the positive endpoint `a=1`, use the normalized rows

```text
Phi_1(x)_k = c alpha^(k-1) sum_{i=0}^{N-1} x_i zeta^(ki),
1 <= k <= D-1.                                             (1)
```

For each `0 <= j < M`, declare the pair block

```text
V_j={bj,bj+1},   local weight 1,
```

and force every coordinate `bj+r`, `2 <= r < b`, to zero by singleton
weight-zero blocks.  The resulting fixed profile is

```text
P_b={x in {0,1}^N:
     x_{bj}+x_{bj+1}=1,
     x_{bj+r}=0 for 2<=r<b and 0<=j<M}.                    (2)
```

Define the bijection `iota_b:{0,1}^M -> P_b` by

```text
iota_b(u)_{bj}=u_j,
iota_b(u)_{bj+1}=1-u_j,
iota_b(u)_{bj+r}=0  (2<=r<b),
```

and define

```text
Psi_D(u)_k=sum_{j=0}^{M-1} u_j xi^(kj),   1<=k<=D-1.       (3)
```

### Theorem 1 (exact actual-syndrome compression)

For every `u` and every printed row,

```text
Phi_1(iota_b(u))_k
  = c alpha^(k-1)(1-zeta^k) Psi_D(u)_k.                   (4)
```

Every diagonal factor is nonzero.  Consequently, for every additional mask
`Omega subseteq {0,1}^M`,

```text
max_y |iota_b(Omega) intersect Phi_1^(-1)(y)|
  = max_z |Omega intersect Psi_D^(-1)(z)|.                (5)
```

This is an identity of complete actual fibers, not a pairwise-distance
surrogate.

### Proof

For `1<=k<=D-1`, direct expansion gives

```text
sum_i iota_b(u)_i zeta^(ki)
 = sum_j zeta^(kbj)[u_j+zeta^k(1-u_j)]
 = zeta^k sum_j xi^(kj)
   +(1-zeta^k) sum_j u_j xi^(kj).
```

Since `1<=k<=D-1<=M-1` and `xi` has order `M`, the first geometric sum
vanishes.  This proves (4).  Also `zeta^k != 1`, so the rowwise diagonal map
is invertible, proving (5).

Each variable pair contributes `1/2` to the block variance and every forced
singleton contributes zero.  Hence

```text
|P_b|=2^M,   Q_{P_b}=M/2=N/(2b).                          (6)
```

## Polynomial payment above the hidden quarter line

### Theorem 2 (full-profile fiber bound)

Assume `M>=4` and `D>=M/4`.  Then every actual endpoint fiber in `P_b` is
polynomially bounded.  More precisely,

```text
D>M/4:
max_y |P_b intersect Phi_1^(-1)(y)|
  <= (M+1)D/(D-M/4),                                     (7)

D=M/4:
max_y |P_b intersect Phi_1^(-1)(y)|
  <= 2(M-1)+4DM = M^2+2M-2.                              (8)
```

### Proof

Fix a `Psi_D` syndrome and split its fiber by the short weight `w=|u|`.
There are only `M+1` strata.  If two distinct words `u,v` in one stratum have
Johnson distance `e`, let

```text
A={j:u_j=1,v_j=0},   B={j:u_j=0,v_j=1}.
```

Equal weight gives the power sum of order zero, and equal syndromes give
orders `1,...,D-1`.  If `e<=D-1`, Newton identities through order `e` force
the monic locator polynomials of `A` and `B` to agree.  Since `A` and `B` are
disjoint, this is impossible unless both are empty.  Thus distinct words in
the stratum have Johnson distance at least `D`.

Put `Q_w=w(M-w)/M`, and let the stratum have size `A_w`.  Summing pairwise
Johnson distances and applying Cauchy-Schwarz to coordinate incidences gives

```text
D binom(A_w,2) <= (A_w^2/2) Q_w.
```

If `D>Q_w`, then

```text
A_w <= D/(D-Q_w).                                        (9)
```

If `D=Q_w`, the centered incidence vectors have squared norm `Q_w`,
nonpositive pairwise inner products, and lie in dimension `M-1`.  The
equality-line Gram bound gives

```text
A_w <= 2(M-1).                                           (10)
```

Since `Q_w<=M/4`, summing (9) over weights proves (7) when `D>M/4`.  At
`D=M/4`, write `w=M/2+t`.  The central stratum uses (10), while for `t!=0`,

```text
D-Q_w=t^2/M,   A_w<=DM/t^2.
```

Using `sum_{t>=1} 1/t^2 <= 2` proves (8).

The same result holds at the `a=0, R=D` endpoint: its exponent-zero row is
the fixed value `cM`, and rows `1,...,D-1` use the same compiler.  Coordinate
reversal gives the corresponding negative endpoint windows with the reversed
profile.

## Fixed-linear consequence

Fix `0<kappa<1/4`.  Let `b=b(kappa)` be the unique power of two satisfying

```text
1/(4kappa) <= b < 1/(2kappa),                             (11)
```

and, along sufficiently large powers of two divisible by `b`, set

```text
M=N/b,   D_N=floor(kappa N).
```

Then `D_N/M=kappa b+o(1)` lies in `[1/4,1/2)`.  If `kappa b>1/4`, the fixed
positive gap gives `D_N>=M/4` for all sufficiently large `M`.  If
`kappa b=1/4`, then sufficiently large dyadic `M` is divisible by four and
`D_N=floor(M/4)=M/4`.  Thus Theorem 2 applies in both cases.  Moreover,

```text
Q_{P_b}-D_N
 = (1/(2b)-kappa)N + (kappa N-floor(kappa N))
 = Theta_kappa(N).                                       (12)
```

Nevertheless, uniformly over every admissible split prime, order-`N`
locator, nonzero row scaling, and syndrome,

```text
max_y |P_b intersect Phi_1^(-1)(y)|
  = N^O_kappa(1) = exp(o(N)).                             (13)
```

The profile itself has entropy rate `(log 2)/b>0`.  Thus a linear value of
`Q_P-D` is not, by itself, a positive-rate floor for actual endpoint fibers.

## Exact remaining wall

The compiler (5) remains valid below the hidden quarter line, but the payment
does not.  Fix a dyadic `b` and `0<theta<1/4`.  Uniformly over every sequence

```text
M=2^t -> infinity,   N=bM,
p prime with N | (p-1),
xi in F_p^* of order M,   D=floor(theta M),
```

the next theorem-or-counterexample target is

```text
max_{w,z} |{u in {0,1}^M:
             |u|=w,
             sum_j u_j xi^(kj)=z_k for 1<=k<=D-1}|
  = exp(o(M)),                                            (14)
```

uniformly for `D=floor(theta M)`, or an explicit admissible sequence with a
fiber of size `exp(cM)`.  By (5), such a positive-rate construction would be
an actual endpoint same-syndrome fixed-profile counterexample.

## Nonclaims

- This does not pay arbitrary fixed block profiles with `Q_P-D=Theta(N)`.
- It constructs no positive-rate same-syndrome family.
- Forced singleton coordinates are declared profile blocks, not silently
  deleted coordinates.
- It proves no source-to-profile atlas, residual-to-full comparison, Sidon or
  major-arc payment, ray compiler, add-back theorem, full C9 theorem, deployed
  finite row, or prize theorem.
- Direct application of the field-free block-profile bound does not prove
  (7)-(13); the syndrome compiler (4) is the new step.

## Verification

`experimental/scripts/verify_asymptotic_c9_sparse_pair_profile_compiler.py`
exhaustively checks four split-prime fixtures, including the complete long and
short fiber multisets, the `a=1` and `a=0` positive windows, both reversed
negative windows, rowwise identity (4), fixed-weight Johnson separation,
strict/equality Plotkin inequalities, and the displayed full-fiber bounds.
