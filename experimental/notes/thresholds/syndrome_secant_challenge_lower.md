# Challenge-restricted syndrome-secant lower bound

## Status

`PROVED`.  This is an exact lower/unsafe-side theorem.  It does not prove the
complete A7 safe envelope, any deployed adjacent certificate, or either prize
threshold.

## Setup

Let `C=RS_F(D,k)`, `q=|F|`, `n=|D|`, and `R=n-k`.  Fix a nonempty challenge
set `Gamma subseteq F` of size `G`.  For `k+1<=a<=n`, put `t=n-a<R` and
`N_t=binom(n,t)`.  If `E subseteq D` has size `t`, let `V_E subseteq F^R` be
the span of the parity-check columns indexed by `E`.

Define

```text
S_t(q) = sum_{j=0}^t binom(t,j) binom(n-t,t-j)
                    q^max(j,2t-R).
```

## Theorem

The maximum challenge-restricted MCA numerator at agreement `a` satisfies

```text
B^MCA_{C,Gamma}(a)
 >= ceil(G N_t q^(2t) (q^R-q^t) / (q^(2R) S_t(q))).       (1)
```

At the first allowed agreement `a=k+1`, so `t=R-1`, this becomes

```text
B^MCA_{C,Gamma}(k+1)
 >= ceil(G (q-1) N / (q(N+q-1))),                         (2)
N = binom(n,k+1).
```

Consequently, for any sequence with `k/n -> rho in (0,1)` and
`log q=o(n)`, the fraction on the right of (2) tends to one.  For every target
sequence with `limsup epsilon<1`, and in particular for `epsilon=2^-128`, the
row `a=k+1` is unsafe for all sufficiently large `n`, uniformly in the actual
nonempty challenge set `Gamma`.

## Proof

For every `t`-set `E`, the MDS parity-column property gives `dim V_E=t`.
For two `t`-sets `E,F` with `j=|E intersect F|`,

```text
dim(V_E intersect V_F) = max(j,2t-R).
```

Let `m(y)=#{E:y in V_E}` and `U_t=union_E V_E`.  The exact first and second
moments are

```text
sum_y m(y)   = N_t q^t,
sum_y m(y)^2 = N_t S_t(q).
```

Cauchy--Schwarz therefore gives

```text
|U_t| >= N_t q^(2t)/S_t(q).                              (3)
```

For each `y in U_t`, select one `E(y)` with `y in V_E(y)`.  For each
`gamma in Gamma` and each `y_1 notin V_E(y)`, set `y_0=y-gamma y_1`.  The
syndrome line `y_0+lambda y_1` meets `V_E(y)` transversely at `lambda=gamma`,
so `gamma` is MCA-bad at agreement `n-t`.

There are exactly `G|U_t|(q^R-q^t)` such triples.  For a fixed syndrome pair
`(y_0,y_1)` and fixed `gamma`, the point `y=y_0+gamma y_1` is unique; hence at
most one selected triple lies over each bad challenge slope of that pair.
Summing bad-slope counts over the `q^(2R)` syndrome pairs, averaging, and using
(3) proves (1).  Surjectivity of the syndrome map lifts the selected syndrome
pair to a received pair.

For `t=R-1`, direct evaluation of `S_t(q)` gives (2).  If `k/n->rho`, then
`log N=n h(rho)+o(n)`.  Under `log q=o(n)`, one has `q/N->0` and `q->infinity`,
so

```text
(q-1)N/(q(N+q-1)) -> 1.
```

This proves the asymptotic unsafe-side assertion.

## Exact remaining wall

The theorem supplies a lower reserve near capacity without A2, A4, or A6.
It does not certify a safe row.  The complete A7 profile envelope and its
comparison with the actual target remain open, as do exact finite deployed
inequalities `U(a0+1)<=B*<L(a0)`.
