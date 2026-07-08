# CAP25 v13 Q/logmoment mass-aware audit

Status: REPAIR / ROUTE_CUT / EXACT_NEW_WALL / AUDIT.

This note records a narrow normalization repair for the Q/logmoment route in
`experimental/grande_finale.tex`.  It does not prove an adjacent deployed safe
row and does not prove

```text
U(a0 + 1) <= B*.
```

The point is narrower: the primitive first-match residual family has residual
mass `tau <= 1`.  Therefore the full-mass lower bound `Gamma_r >= 1` cannot be
imported into the pruned primitive residual moment unless `tau = 1` is proved.
The raw ordinary entropy-inverse problem for `Gamma_r^{prim}` also remains a
route cut until it is replaced by an off-diagonal/falling-factorial theorem, or
by a formulation that separately forces dense heavy fibers or exponentially
many distinct residual supports.

## Normalization

Let

```text
K = |B|^w,
C = binom(n,m),
```

where `K` is the prefix-fiber denominator.  It is not the deployed row-budget
denominator.

Let `P` be the first-match-pruned primitive residual support family, and let

```text
N_s = #{ A in P : prefix(A) = s },   s in B^w.
```

Normalize against the full ambient prefix average

```text
Nbar = C / K.
```

Define

```text
R_s     = N_s / Nbar,
M       = max_s R_s,
tau     = K^{-1} sum_s R_s = |P| / C,
Gamma_r = K^{-1} sum_s R_s^r,       r >= 2.
```

The use of `Nbar = C/K`, rather than `|P|/K`, is deliberate: the Q target is a
max-fiber bound measured against the original full-support prefix average.  The
pruning loss is tracked explicitly by `tau`.

If `P` is empty, then `tau = 0`, `M = 0`, and the primitive residual branch is
already void.  The logarithmic statements below are only meaningful for
`tau > 0`.

## Mass-aware moment sandwich

For every `r >= 2`,

```text
max(K^{-1} M^r, tau^r) <= Gamma_r <= tau M^{r-1} <= M^{r-1}.
```

Proof.  A fiber with `R_s = M` gives

```text
Gamma_r = K^{-1} sum_s R_s^r >= K^{-1} M^r.
```

Jensen with respect to the uniform measure on `B^w` gives

```text
Gamma_r >= (K^{-1} sum_s R_s)^r = tau^r.
```

Finally, since `R_s <= M`,

```text
R_s^r <= M^{r-1} R_s,
```

and hence

```text
Gamma_r <= M^{r-1} K^{-1} sum_s R_s = tau M^{r-1} <= M^{r-1}.
```

This is the correct primitive residual replacement for the full-mass sandwich.

## The finite moment criterion survives

The spike lower bound gives

```text
M^r <= K Gamma_r.
```

Thus the ordinary moment criterion

```text
log2 Gamma_r + w log2 |B| <= r Delta_Q
```

still certifies

```text
M <= 2^{Delta_Q}.
```

So the finite criterion itself is not the problem.  The problem is the lower
floor used to judge whether such a criterion can fit inside a deployed row.

## Corrected mass-aware order floor

The full-mass proof of `prop:q-moment-order-floor` uses `Gamma_r >= 1`.  That
line is valid for the unpruned full distribution because its normalized mass is
one.  For the primitive first-match residual family, the universal lower bound
is only

```text
Gamma_r >= tau^r.
```

Therefore any certificate of the form

```text
log2 Gamma_r + w log2 |B| <= r Delta_Q
```

is compatible with the mass lower bound only if

```text
r >= ceil( w log2 |B| / (Delta_Q + log2(1/tau)) )
```

for `0 < tau <= 1`.

When `tau = 1`, this recovers the full-mass floor

```text
r >= ceil( w log2 |B| / Delta_Q ).
```

When `tau < 1`, the full-mass floor is not the correct primitive residual
floor.  In particular, the statement

```text
Holder's inequality gives Gamma_r >= 1
```

should not be applied to `Gamma_r^{prim}` after first-match pruning unless a
separate proof shows that the primitive residual family has full mass.

## Small counterexample to the imported floor

Let `K = 2`, `C = 2`, and let the residual family contain one support in one
prefix fiber:

```text
N = (1,0).
```

Then `Nbar = 1`, `R = (1,0)`, `M = 1`, and

```text
tau = 1/2,
Gamma_r = 1/2.
```

Thus `Gamma_r < 1` for every `r >= 2`, even though the normalization by the
full ambient average has been used correctly.  The correct lower bound is
`Gamma_r >= tau^r`, not `Gamma_r >= 1`.

## Ordinary entropy-inverse route cut

The raw problem `prob:entropy-inverse-q` asks for an inverse theorem from a
large ordinary primitive moment

```text
Gamma_r^{prim} >= exp(eta n r).
```

As a theorem-facing input this is too broad.  The ordinary moment

```text
sum_s N_s^r
```

counts ordered `r`-tuples with repetitions, including fully diagonal
contributions and sparse singleton heavy fibers.  It does not by itself count
many distinct primitive trades, nor does it force a dense population of
distinct residual supports.

The inverse target should therefore be reformulated in one of the following
stronger forms:

1. an off-diagonal or falling-factorial moment that removes diagonal
   repetitions and counts distinct residual supports;
2. a dense-heavy-fiber hypothesis that separately proves the heavy fiber
   contains exponentially many distinct residual supports; or
3. an explicit new obstruction cell for sparse heavy primitive fibers.

Without one of these strengthenings, the raw ordinary entropy-inverse route is
a route cut, not a proof of primitive Q.

## Deployed-row bookkeeping

The adjacent safe-side Q depths currently used by the packet are:

```text
KoalaBear rows: w_Q = 67471,
Mersenne-31 rows: w_Q = 67447.
```

These are prefix depths.  They should not be confused with row-budget
denominators, row challenge budgets, or safe-side bit margins.

The note also does not change the deployed-row status:

```text
No adjacent safe row is proved.
No row-sharp Q theorem is proved.
No BC/SP closure is proved here.
No entropy-inverse theorem is proved.
```

The remaining exact wall is a row-sharp Q atom theorem with a theorem-facing
inverse formulation:

```text
CAP25-V13-ROW-SHARP-Q-ATOM
```

or a counterpacket/new obstruction cell replacing it.
