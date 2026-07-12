# L2-Sharp V0 Repeated-Row Counterexample

- **Status:** COUNTEREXAMPLE / PROVED.
- **Date:** 2026-07-12.
- **Scope:** This note refutes only Conjecture L2-Sharp, Version 0, in
  `l2_sharp_target_conjecture.md`.

## Statement

Conjecture L2-Sharp V0 is false in its stated cyclic generated-field scope.
More precisely, fix

```text
mu = 2,        epsilon = 1/5,        Cq = 2,        C0 = 1/2,
```

and a compact rate window containing `1/2`. There is a sequence
`(q_s,n_s,k_s,sigma_s,a_s)` and repeated received words `U_s=(V_s,V_s)` such
that all V0 reserve hypotheses hold, but

```text
|Lambda_2(U_s,a_s)| >= 2^((1/4-o(1)) n_s),
```

whereas

```text
binom(n_s,a_s) q_s^(-2 sigma_s)
  + Quot_rem_2(n_s,k_s,a_s)
  + n_s^B
```

is polynomial in `n_s` for every fixed `B`.

The obstruction is the rank-one received-row stratum. Repeated rows retain a
worst-case one-row list, so the effective entropy payment there is
`sigma log_2 q`, not `mu sigma log_2 q`.

## Construction

Let `s` tend to infinity and put

```text
q_s     = 2^s,
n_s     = q_s - 1,
H_s     = F_(q_s)^*,
k_s     = floor(n_s/2),
sigma_s = ceil(3 n_s/(4s)),
a_s     = k_s + sigma_s.
```

Write `C_s=RS[F_(q_s),H_s,k_s]`. For a one-row received word `V`, let

```text
L(V) = |{c in C_s : |{x in H_s : c(x)=V(x)}| >= a_s}|.
```

## One-row averaging

Choose `V:H_s -> F_(q_s)` uniformly. For each fixed codeword, its number of
agreements with `V` has distribution `Bin(n_s,1/q_s)`. Therefore

```text
E L(V) = q_s^k_s Pr[Bin(n_s,1/q_s) >= a_s].
```

Keeping only the event of exactly `a_s` agreements gives

```text
E L(V)
 >= binom(n_s,a_s) q_s^(-sigma_s)
      (1-q_s^(-1))^(n_s-a_s).                 (1)
```

Hence some received word `V_s` has list size at least the right-hand side.
Now `a_s/n_s=1/2+O(1/s)`, so the binary-entropy estimate gives

```text
log_2 binom(n_s,a_s) = n_s-o(n_s).
```

Also

```text
s sigma_s = 3n_s/4+O(s)
```

and `(1-1/q_s)^(n_s-a_s)` is bounded below by a positive constant. Taking
base-two logarithms in (1) yields

```text
log_2 L(V_s) >= n_s/4-o(n_s).                 (2)
```

This is an averaging existence proof; no explicit search for `V_s` is needed.

## Repeated-row diagonalization

Set `U_s=(V_s,V_s)`. If `(c_1,c_2)` belongs to the two-row list, then there is
an `a_s`-set on which both codewords equal `V_s`. Thus `c_1-c_2`, a polynomial
of degree `<k_s`, has at least `a_s>=k_s` roots. It follows that `c_1=c_2`.
Conversely, every one-row listed codeword gives the diagonal pair `(c,c)`.
Consequently

```text
|Lambda_2(U_s,a_s)| = L(V_s),
```

and (2) proves the exponential lower bound.

## V0 hypotheses and right-hand side

The rate tends to `1/2`, `k_s<=a_s<n_s`, and
`q_s=n_s+1<=n_s^2` for large `s`. Moreover,

```text
2 sigma_s log_2 q_s = 2s sigma_s >= 3n_s/2.
```

Since `log_2 binom(n_s,a_s)<=n_s`, this is stronger than V0's reserve
condition with `epsilon=1/5`. The coarse guard
`sigma_s >= C0 n_s/log n_s` also holds for `C0=1/2`, whether the unmarked
logarithm is read in base `2` or base `e`.

By contrast, V0's random term satisfies

```text
binom(n_s,a_s) q_s^(-2 sigma_s)
 <= 2^(n_s-2s sigma_s)
 <= 2^(-n_s/2).                              (3)
```

For an active all-remainder scale `M`, the definition has `M>sigma_s` and a
quotient ground set of size

```text
Q_M = n_s/M-1 < 4s/3.
```

For `mu=2`, its packet count is at most the number `4^Q_M` of ordered pairs of
subsets of that ground set. There are at most `n_s` active divisors, so

```text
Quot_rem_2(n_s,k_s,a_s)
 <= n_s 4^(4s/3)
 = O(n_s^(11/3)).                            (4)
```

Equations (3) and (4) make the entire proposed V0 right-hand side polynomial
for every fixed error exponent `B`, contradicting the exponential left-hand
side.

## Repaired target requirement

A uniform replacement cannot use only the independent-row reserve

```text
mu sigma log_2 q >= (1+epsilon) log_2 binom(n,a).
```

It must cover the rank-one stratum. An unstratified replacement therefore
needs, at minimum, the one-row reserve

```text
sigma log_2 q >= (1+epsilon) log_2 binom(n,a),
```

together with an explicit one-row worst-case bound after whatever structured
packets the target chooses to charge. Equivalently, a row-rank-stratified
target must use `r sigma log_2 q` on effective row rank `r`, including `r=1`.
These are requirements on a repaired conjecture, not a proof that such a
conjecture is true.

## Verification

The standard-library verifier checks the parameter inequalities, the exact
finite averaging lower bound on representative values of `s`, the failure of
the one-row reserve, the exponentially small V0 random term, and the
polynomial quotient-budget envelope:

```text
python3 experimental/scripts/verify_l2_sharp_v0_repeated_rows.py
```

This correction makes no claim about a Grand threshold, any official endpoint,
any field ledger, or any separate quotient lower theorem.
