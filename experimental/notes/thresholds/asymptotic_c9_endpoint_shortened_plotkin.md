# Endpoint shortened-Plotkin bound for primitive C9

Status: `PROVED / STRICT_SUBREGIME`.

This note proves a pointwise fiber bound for the four endpoint monomial
windows on a prime-field multiplicative coset.  It combines the banked
locator-prefix distance with a constant-weight shortening argument.  The
result is uniform over every fixed-weight Boolean mask, so first-match pruning
does not create a separate mask-stability loss in this subregime.

It does not prove unrestricted primitive C9.

## 1. A shortened constant-weight Plotkin bound

Let `N>=2`, let `1<=m<=N-1`, and let `C` be a family of binary words of
length `N`, all of weight `m`.  Put

```text
q = min(m,N-m),
B(n,q) = 2q(n-q)/n.
```

Complementing every word if necessary preserves Hamming distance and reduces
the weight to `q <= N/2`.  This is only a geometric reduction of a
constant-weight code; the complemented family is not asserted to remain an RS
fiber.

### Theorem 1 (shortened Plotkin bound)

Assume every two distinct words of `C` have Hamming distance at least `d`.
For an integer `u` with `0 <= u <= N-q`, put `n=N-u`.  If

```text
d > B(n,q),
```

then

```text
|C| <= [binom(N,q)/binom(N-u,q)] * d/[d-B(N-u,q)].       (1)
```

For `u=0`, this is the usual constant-weight Plotkin count.

### Proof

At length `N-j`, the total number of zero incidences in a weight-`q` code of
size `J_j` is `(N-j-q)J_j`.  Some coordinate is therefore zero on at least

```text
(N-j-q)J_j/(N-j)
```

words.  Restrict to those words and delete that identically zero coordinate.
After `u` steps the resulting length-`N-u`, weight-`q` code has size

```text
J_u >= |C| * binom(N-u,q)/binom(N,q).                    (2)
```

Let `a_i` be the number of its words containing coordinate `i`.  Summing
Hamming distances over unordered pairs and applying Cauchy--Schwarz gives

```text
d binom(J_u,2)
  <= sum_i a_i(J_u-a_i)
  <= J_u^2 q(n-q)/n.
```

If `d>B(n,q)`, rearrangement gives

```text
J_u <= d/[d-B(n,q)].                                     (3)
```

Combining (2) and (3) proves (1).

### Proposition 2 (the equality line)

If the minimum distance is `d=B(N,q)`, then

```text
|C| <= 2(N-1).                                           (4)
```

Indeed, center every incidence vector in the hyperplane perpendicular to the
all-ones vector and normalize it to unit length.  The resulting Gram matrix
is positive semidefinite, has rank at most `N-1`, diagonal entries `1`, and
nonpositive off-diagonal entries.  If its size is `J`, then positivity on the
all-ones vector and `x^2 <= -x` for `-1 <= x <= 0` give

```text
tr(G^2) <= 2J.
```

Cauchy--Schwarz on the nonzero eigenvalues gives

```text
J^2 = tr(G)^2 <= rank(G) tr(G^2) <= 2(N-1)J,
```

which proves (4).

### Corollary 3 (an explicit near-threshold bound)

Assume `q >= alpha_0 N` for a fixed `alpha_0>0`, define

```text
B_N = B(N,q),
Delta = (B_N-d)_+,
u = ceil((Delta+1)/(2 alpha_0^2)).
```

If `u <= N/4` and `d <= N+2`, then

```text
log |C| <= log(N+2) + u log 4.                            (5)
```

To see this, use the exact identity

```text
B(N,q)-B(N-u,q) = 2q^2u/[N(N-u)] >= 2 alpha_0^2 u.       (6)
```

Thus `d-B(N-u,q) >= 1`.  Moreover, because `q<=N/2` and
`u<=N/4`,

```text
binom(N,q)/binom(N-u,q)
  = product_{j=0}^{u-1} (N-j)/(N-q-j)
  <= 4^u.                                                (7)
```

Substitution in (1) proves (5).  In particular,

```text
(B_N-d)_+ = o(N)  implies  |C| = exp(o(N)).              (8)
```

## 2. Endpoint moment fibers

Let `p` be prime, let `N=2^s` divide `p-1`, and let

```text
T = {t_i=alpha zeta^i : 0<=i<N} subset F_p^x,
```

where `zeta` has order `N`.  Fix a weight-`m` mask
`Omega subseteq {A subseteq T : |A|=m}`.  For

```text
1 <= R <= N/2
```

and

```text
rho_i = c zeta^(a i),  c in F_p^x,
```

define

```text
Phi(A) = sum_{t_i in A} rho_i (1,t_i,...,t_i^(R-1)).
```

Consider the four endpoint exponents

```text
a in {0, 1, 1-R, -R} mod N.
```

Put

```text
D = R      for a in {0,1-R},
D = R+1    for a in {1,-R}.
```

The case `a=0` is the unweighted row.  Since

```text
P_T(X)=X^N-alpha^N,
1/P_T'(t_i)=t_i/(N alpha^N),
```

the exact dual weight is the case `a=1`, up to a nonzero scalar.

### Lemma 4 (endpoint locator distance)

Every two distinct supports in one fiber of `Phi|_Omega` have Johnson
distance at least `D`, hence Hamming distance at least `2D`.

### Proof

Cancel the common coordinates of two colliding supports and call the disjoint
remainders `E,E'`, each of size `e`.  For `a=0`, equality of syndromes and
fixed weight give equal power sums of orders `1,...,R-1`.  For `a=1`, they
give equal power sums of orders `1,...,R`.  The two negative endpoint windows
reduce to these cases under `t -> t^(-1)` and reversal of the syndrome
coordinates.

Thus the two remainders have equal power sums through order `D-1`.  Since
`p>N`, Newton's triangular identities are invertible through this range.  If
`e<=D-1`, the two monic locator polynomials are equal, contradicting the
disjointness of their nonempty root sets.  Therefore `e>=D`.

## 3. Prime-field dyadic C9 strip

For a fiber `F_y=Omega intersect Phi^(-1)(y)`, apply Theorem 1 with

```text
d = 2D,
B_N = 2m(N-m)/N.
```

If `min(m,N-m) >= alpha_0 N`, Corollary 3 gives

```text
(2m(N-m)/N - 2D)_+ = o(N)
    implies max_y |F_y| = exp(o(N)).                     (9)
```

Equivalently, if `m/N -> theta` away from `0` and `1`, it is sufficient that

```text
(R+delta)/N >= theta(1-theta)-o(1),                     (10)
```

where `delta=0` on the unweighted endpoints and `delta=1` on the exact-dual
endpoints.  At half density this is the quarter-rank strip

```text
R >= N/4-o(N).
```

This improves the generic weighted-MDS threshold near `R/N=1/2`, but only for
the four printed endpoint windows.

For `N` divisible by four, the equality and strict cases give the exact
half-density bounds (with `N>=8` on the `R=N/4-1` line)

```text
a=0 or 1-R, R=N/4:       max_y |F_y| <= 2(N-1),
a=1 or -R, R=N/4-1:      max_y |F_y| <= 2(N-1),
a=1 or -R, R=N/4:        max_y |F_y| <= N/4+1.          (11)
```

The last line uses `u=0`, `d=N/2+2`, and `B_N=N/2` in (1).

Let `Omega^circ` be any nonempty exact residual satisfying the hypotheses and
put

```text
M=|Omega^circ|, L=|Phi(Omega^circ)|, barN=M/L.
```

Since `barN>=1`, the stronger pointwise estimate (9) implies

```text
max_y |F_y| <= exp(o(N)) barN.
```

It therefore pays image-normalized primitive Q and C9 on this strict
subregime.  No parent-average or second-moment-to-maximum conversion is used.

## 4. Relation to existing packets

- `experimental/grande_finale.tex`, `prop:prefix-rigidity`, already proves the
  locator-prefix distance.
- `experimental/notes/l1/l1_aperiodic_prefix_collision.md` already proves the
  algebraically equivalent unshortened Plotkin bound in its co-large strip.
  Neither that `u=0` bound nor locator rigidity is claimed as new here.
- PR #444 gives the `u=0` fixed-weight Plotkin count with the generic weighted
  Vandermonde distance `R+1`.  The repository-new delta is Theorem 1 with
  `u>0`, Proposition 2 at equality, and their explicit endpoint C9 packaging
  in the `o(N)`-deficit quarter-rank strip.
- PR #439 isolates the image-normalized C9 interface.  Section 3 pays it here
  by a pointwise bound on every mask.
- PR #448 records why ordinary second moments do not control the largest
  fiber.  This note bounds each fiber directly.
- PR #451 uses Frobenius orbit expansion in a coefficient-field subregime.
  The present prime-field argument is disjoint and does not use Frobenius.

The shortening and Plotkin arguments are classical.  The contribution here is
the exact RS-MCA endpoint specialization, explicit finite inequality, and
image-normalized C9 corollary.

## 5. Verification

Run

```sh
python3 experimental/scripts/verify_asymptotic_c9_endpoint_shortened_plotkin.py --check
```

The verifier exhausts the four endpoint windows for small prime-field dyadic
rows, checks the endpoint distance and every applicable finite bound, checks
the printed half-density bounds, and replays the shortening
identities and uniform estimate over a broad integer range.

## 6. Nonclaims and next wall

- No full prime-field dyadic C9 theorem is proved.
- No arbitrary interior shifted-monomial or nonconstant-weight theorem is
  proved beyond the generic MDS distance already present in PR #444.
- No exact C1--C8 emission or exhaustion theorem is proved.
- No unrestricted multi-leaf add-back or target-normalized compiler theorem is
  proved.
- No KoalaBear, Mersenne-31, QM31, or other deployed finite row is certified.
- The asymptotic factor `exp(o(N))` does not pay any recorded finite bit margin.

The remaining endpoint region has a fixed linear Plotkin deficit:

```text
2D <= 2m(N-m)/N - eta N.
```

Distance alone is insufficient there.  The next exact target is a
residual-specific split-locator container theorem: every exponential
same-syndrome family must retain exponential mass in one explicit C1--C8
certificate class, or produce a new noncircular obstruction cell with its
payment.
