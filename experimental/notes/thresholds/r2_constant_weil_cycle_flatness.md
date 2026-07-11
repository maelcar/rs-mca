# R=2 constant-Weil-ratio flatness with exact characteristic cycles

- **Status:** PROVED, conditional only on the classical Weil input already
  stated in `prop:weighted-weil-minor-arcs`.
- **Track:** asymptotic hard input B / the linear-density `R=2` max-fiber
  razor.
- **Verifier:**
  `python3 experimental/scripts/verify_r2_constant_weil_cycle_flatness.py`.

## Theorem

Let `B_nu` be finite fields of odd characteristic `p_nu` and cardinality
`Q_nu`.  Let

```text
D_nu = theta_nu H_nu subset B_nu^x
T_nu = D_nu \ P_nu
N_nu = |T_nu| -> infinity,
```

where `P_nu` is an allowed planted exceptional set.  Fix
`0 < alpha < 1/2`, and take

```text
alpha <= m_nu/N_nu <= 1-alpha.
```

On the fixed-weight slice `Omega_nu=binom(T_nu,m_nu)`, define

```text
Phi_nu(S) = (sum_{t in S} t, sum_{t in S} t^2) in B_nu^2,
M_nu      = binom(N_nu,m_nu).
```

Let `C_0` be the absolute constant in the integrated weighted-Weil
proposition, and put

```text
C_W       = 3 C_0,
Lambda_nu = C_W sqrt(Q_nu) + |P_nu|.
```

Assume that fixed constants `K < infinity` and `lambda < 1/2` satisfy,
eventually,

```text
N_nu/p_nu <= K,
log Q_nu = o(N_nu),
Lambda_nu/N_nu <= lambda.                                (1)
```

Then there is `c=c(alpha,lambda,K)>0` such that, uniformly for every
`z in B_nu^2`,

```text
|#{S in Omega_nu : Phi_nu(S)=z} - M_nu/Q_nu^2|
    <= exp(-c N_nu) M_nu/Q_nu^2.                         (2)
```

Consequently the realized full-slice image is exactly `B_nu^2`, its
source-prescribed image average is `M_nu/Q_nu^2`, and every primitive
first-match residual `Omega_nu^o subset Omega_nu` obeys

```text
max_z |Omega_nu^o intersect Phi_nu^(-1)(z)|
      / (M_nu/Q_nu^2)
    <= 1 + exp(-c N_nu).                                 (3)
```

Thus no residual in this class can have a positive exponential max-fiber
excess, whether or not that fiber lies near the Sidon energy floor.

## Proof

Suppress `nu`, and write `Q,p,N,m,M,Lambda` for the row parameters.  Fix a
nonzero dual parameter `u=(a,b)` and a nontrivial additive character
`psi` of `B`.  Put

```text
x_t    = psi(a t + b t^2),
P_j(u) = sum_{t in T} x_t^j.
```

If `p` does not divide `j`, the phase `j(aX+bX^2)` is nonconstant, has
pole degree at most two, and is not Artin-Schreier: in odd
characteristic its pole order is one or two, hence not divisible by `p`.
The integrated weighted-Weil proposition therefore gives

```text
|P_j(u)| <= 3 C_0 sqrt(Q) + |P| = Lambda.                 (4)
```

If `p` divides `j`, every additive-character value has `p`-torsion, so

```text
P_j(u) = N.                                               (5)
```

Let `e_r` be the elementary symmetric coefficient of the phase values.
Newton's generating identity and coefficientwise absolute majorization
give

```text
|e_r(x_t:t in T)| <= B_r,

B_r = [v^r] (1-v)^(-Lambda)
              (1-v^p)^(-(N-Lambda)/p).                   (6)
```

This is the exact small-characteristic factor recorded but left unpaid in
`rem:small-characteristic-cycles`.  No integrality of `Lambda` is needed:
under (1), both real exponents in (6) are positive and their generalized
binomial expansions have nonnegative coefficients.

Expanding the second factor gives

```text
B_r = sum_{ell=0}^{floor(r/p)}
        binom((N-Lambda)/p+ell-1,ell)
        binom(Lambda+r-p ell-1,r-p ell).                  (7)
```

Put `K_0=ceil(K)`.  Since `r<=N`, condition `N/p<=K` bounds both `ell`
and `(N-Lambda)/p` by `K_0`.  Also `Lambda>=1` eventually, and then
`binom(Lambda+s-1,s)` is increasing in the integer `s`.  Hence

```text
B_r <= C_K binom(Lambda+r-1,r),                           (8)

C_K = sum_{ell=0}^{K_0} binom(K_0+ell-1,ell).
```

The characteristic-divisible cycles therefore cost only a row-independent
constant factor.

It remains to compare (8) with the fixed-weight main term.  For natural
binary entropy `h`, define

```text
J_lambda(x)
  = h(x) - (x+lambda) h(x/(x+lambda)).                    (9)
```

Direct differentiation gives

```text
J_lambda(0)=J_lambda(1-lambda)=0,
J_lambda'(x)=log((1-x)/(x+lambda)).
```

Therefore `J_lambda(x)>0` on `0<x<1-lambda`.  With
`r=min(m,N-m)`, one has `r/N in [alpha,1/2]`, a compact subset of that
interval because `lambda<1/2`.  Stirling's formula, monotonicity in the
upper generalized-binomial parameter, and (8) now give some `delta>0`
with

```text
Q^2 B_r / binom(N,r) <= exp(-delta N + o(N)).             (10)
```

Fourier inversion on the additive group `B^2` has zero-character term
`M/Q^2`; each of the other `Q^2-1` terms is bounded by `B_m`.  Equation
(10) proves (2) when `m<=N/2`.  If `m>N/2`, complementing supports
translates the boundary value and reduces to `r=N-m`.

The error in (2) is eventually smaller than its main term, so every
target is attained.  This proves the full-image statement before the
image normalization is used.  Finally, a first-match residual is a subset
of the full slice, and deletion cannot enlarge any fixed fiber.  This
proves (3); no monotonicity claim about additive energy is used.

## Explicit class beyond the shallow theorem

Fix an integer `d>2 C_W`.  There are infinitely many odd primes
`p=1 mod d`.  For each such prime, take

```text
B = F_(p^2),
|H| = d(p+1),
T = theta H,
P = empty.
```

The subgroup exists because `d` divides `p-1` and `B^x` is cyclic of
order `(p-1)(p+1)`.  Here

```text
N/p -> d,
C_W sqrt(|B|)/N -> C_W/d < 1/2,
log |B| = o(N),
2 sqrt(|B|)/N -> 2/d > 0.                                (11)
```

Thus every fixed density window satisfies the theorem, while the existing
shallow hypothesis `R sqrt(|B|)=o(N)` fails for `R=2`.  Also
`|H|>p-1`, so the domain is not contained in the only proper subfield
`F_p` of `F_(p^2)`.

## Exact finite predicate

For one finite leaf with `Lambda<N`, put `r=min(m,N-m)` and compute

```text
B_p(N,r,Lambda)
  = sum_{ell=0}^{floor(r/p)}
      binom((N-Lambda)/p+ell-1,ell)
      binom(Lambda+r-p ell-1,r-p ell),

epsilon = Q^2 B_p(N,r,Lambda) / binom(N,m).                (12)
```

The exact predicate `epsilon<1` implies

```text
realized image = B^2,
max_z |Omega^o intersect Phi^(-1)(z)| / (M/Q^2)
  <= 1+epsilon                                             (13)
```

for every residual subset.  This is a finite theorem interface, but no
deployed leaf is certified here because the required numerical Weil
constant and leaf mapping have not been supplied.

## Ledger effect

This pays asymptotic hard input B on the stated unweighted `R=2`
multiplicative-coset class.  It strictly extends:

- `thm:unconditional-shallow-mi-ma`, which requires Weil parameter
  `o(N)`;
- `prop:frontier-weil-separation`, which also assumes `Lambda=o(N)`;
- open PR #596, whose Newton majorant stays in the range `m<p` and hence
  has no characteristic-divisible cycles.

The result directly resolves the near-Sidon/max-fiber razor on this class:
the full-slice maximum is already at random scale, so every residual is
paid before any energy split.

## Nonclaims

- This does not close hard input B for all primitive leaves.
- It does not cover weighted rational charts or circle twin-cosets.
- It does not cover `Lambda/N >= 1/2` or unbounded `N/p`.
- It does not prove a general major-arc theorem.
- It changes zero finite M31 or KoalaBear cells.
- It does not prove any deployed adjacent inequality.
- No paper TeX is changed.
