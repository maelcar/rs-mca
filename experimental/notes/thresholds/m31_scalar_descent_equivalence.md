# Mersenne-31 scalar-descent equivalence

## Status

**PROVED / ZERO-PAYMENT THRESHOLD EQUIVALENCE / AUDITED.** This note is
pinned to `origin/main@9908454995f3f195cfe748f35a1135211609d066` and
records one narrow result: under an explicit support-distance incidence
inequality, an extension-field Reed--Solomon list can be projected to the
base field without losing a codeword. At the deployed Mersenne-31 adjacent
list row, this makes the unresolved quartic-field upper exactly equivalent to
the unresolved prime-field upper.

This is not the deployed scalar upper. It makes no ledger payment and causes
no official-score movement.

## Definitions

Let `F = F_q` be a finite field, let `E/F` be a finite-field extension of
degree `r >= 1`, and let `D` be a set of `n` distinct elements of `F`. For
`1 <= k <= n`, write

```text
RS_K(D,k) = {(f(x))_(x in D) : f in K[X], deg(f) < k}
```

for `K = F` or `E`. For `k <= a <= n`, let `B_K(a)` be the maximum, over all
centers `y in K^D`, of the number of distinct words of `RS_K(D,k)` agreeing
with `y` in at least `a` coordinates.

Put

```text
t   = n - a,
g   = a - k + 1,
N_r = (q^r - 1)/(q - 1),
H_r = (q^(r-1) - 1)/(q - 1).
```

Here `N_r` is the number of projective nonzero `F`-linear functionals
`E -> F`, and `H_r` is the number of their projective classes that kill one
fixed nonzero element of `E`.

## Theorem

Let `L >= 1`. If

```text
L t H_r < g N_r,                                           (1)
```

then every `E`-valued center with `L` distinct codewords of `RS_E(D,k)`
agreeing in at least `a` coordinates admits a nonzero `F`-linear functional
`lambda:E -> F` for which the projected center has `L` distinct codewords of
`RS_F(D,k)` agreeing in at least `a` coordinates. Consequently,

```text
B_E(a) >= L  if and only if  B_F(a) >= L.                  (2)
```

The reverse implication in (2) is the scalar embedding `F -> E`. The forward
implication is the content of the theorem.

## Proof

Take distinct polynomials `f_1,...,f_L in E[X]` of degree below `k` and a
center `y in E^D`. Let

```text
T_i = {x in D : f_i(x) != y(x)}.
```

Then `|T_i| <= t`. For `i != j`, the polynomial `f_i-f_j` has at most `k-1`
zeros on `D`. On every point outside `T_i union T_j`, however, both
polynomials equal `y`. Therefore

```text
|T_i triangle T_j| >= 2(n-k+1) - 2t = 2g.                 (3)
```

Index nonzero `F`-linear functionals `E -> F` up to multiplication by
`F^*`. For a projective functional `lambda`, partition the indices by equality
of the projected polynomials `lambda(f_i)`. Let `M_lambda` be the number of
parts. For each `i`, define the killed-error set

```text
Z_(i,lambda) = {x in T_i : lambda(f_i(x)-y(x)) = 0}.
```

Inside one collision part, all projected polynomials are equal. Hence their
projected error sets are equal, and (3) gives

```text
|Z_(i,lambda)| + |Z_(j,lambda)| >= 2g
```

for every pair in that part. Summing over pairs in a part of size `s` shows
that its killed-error incidence is at least `g s`, and therefore at least
`g(s-1)`. Summing over all parts gives

```text
L - M_lambda <= (1/g) sum_i |Z_(i,lambda)|.                (4)
```

Each nonzero error value is killed by exactly `H_r` projective functionals.
There are at most `L t` error incidences. Summing (4) over the `N_r`
projective functionals therefore yields

```text
sum_lambda (L-M_lambda) <= L t H_r / g.                    (5)
```

If every projection had a collision, every term on the left of (5) would be
at least one, contradicting (1). Thus some `lambda` has `M_lambda=L`.
Projection preserves every agreement coordinate. The projected polynomials
are distinct and, because `k <= |D|`, evaluate to distinct base-field
codewords. This proves the forward implication.

## Deployed Mersenne-31 row

The deployed list row in `experimental/grande_finale.tex` has

```text
p = 2^31 - 1,       F = F_p,       E = F_(p^4),
n = 2^21,           k = 2^20,      a = 1,116,023,
L = 2^24,           t = 981,129,    g = 67,448.
```

Its evaluation domain is contained in `F_p`. Direct integer replay gives

```text
L t H_4 = 75,911,179,514,902,718,909,260,442,370,048,
g N_4   = 667,972,637,535,664,633,399,075,080,765,440,
margin  = 592,061,458,020,761,914,489,814,638,395,392.
```

The strict hypothesis (1) holds. Since

```text
B* = floor(p^4 / 2^100) = 16,777,215 = 2^24 - 1,
```

the forbidden list size is `B*+1=L`. The exact deployed consequence is

```text
B_F_(p^4)(1,116,023) <= 16,777,215
    if and only if
B_F_p(1,116,023) <= 16,777,215.                            (6)
```

Equation (6) is an equivalence of two open upper predicates, not a proof of
either predicate.

## Provenance and overlap

- R34 Role 07 archive SHA-256:
  `200366473c003ab58d0895f4eff5ba25aa3cfba4827d6104a6d33d57ecdcc5db`.
- Frozen worker text SHA-256:
  `d7a2c8952fe897f427d6dbe75546bf06550b8dfff8c715d3a98d79fa0ec26075`.
- Independent hostile-proof packet SHA-256:
  `8c803e54f99bd36e96c9cede102aa3d213900ffb9ef2c23a92c3a3a4714b83b1`.
- Frozen audit text SHA-256:
  `2058a1e6cc820213bdd50d00b33aab25347002d9559e427723981d44a865b8af`.
- Audit verdict: `ACCEPT_NARROWED`, for the theorem and deployed equivalence
  above only.
- Live overlap was refreshed through open PR #992 on 2026-07-20. No open PR
  states this support-distance scalar-descent or deployed threshold
  equivalence.

## Nonclaims and remaining wall

This note proves no prime-field arbitrary-center upper, no quartic-field
scalar upper, no counterexample, no equality-case version of (1), and no
version for evaluation domains outside the base field. It proves no Grand
List theorem, Grand MCA theorem, recurrence, ledger payment, or official
score movement.

The exact remaining wall is

```text
B_F_p(1,116,023) <= 16,777,215
```

for every prime-field center on the pinned Mersenne-31 evaluation domain.
