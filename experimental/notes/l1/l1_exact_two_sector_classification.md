# L1 Exact Two-Sector Classification over Small Prime Orbit Lengths

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE

**Scope:** Prime fields, background-free coset sunflowers, full-petal words,
and exactly two active nonzero `mu_ell`-DFT sectors.

## Setting

Let `p` and `ell` be primes with `ell | (p-1)`, and put
`H = mu_ell <= F_p^*`. Let

```text
T_i = a_i H,                 1 <= i <= tau,
C   = union_{j=1}^m b_j H,   tau < m < ell,
```

where all displayed cosets are distinct. Define

```text
alpha_i = a_i^ell,
beta_j  = b_j^ell,
phi(Y)  = product_i (Y-alpha_i),
Lambda(Y) = product_j (Y-beta_j),
D = m-tau-1.
```

The received word is constant on each petal and zero on the core. A
full-petal codeword `P` agrees on every point of every `T_i`. Write its
`H`-Fourier decomposition as

```text
P(X) = sum_{u=0}^{ell-1} X^u P_u(X^ell).
```

Full-petal agreement forces `phi | P_u` for every nonzero sector `u`.
If exactly two nonzero sectors `r,s` are active, then

```text
P_r = phi g_r,    P_s = phi g_s,    deg(g_r),deg(g_s) <= D.
```

A core label `beta_j` is *sector-dead* when
`g_r(beta_j)=g_s(beta_j)=0`. There are at most `D` such labels. On every
other core coset, after dividing by nonzero factors, retained positions are
the roots in `H` of a trinomial

```text
A + B h^r + C h^s,    (B,C) != (0,0).
```

Write `R_core` for the number of retained core positions. Since the petals
already contribute `tau*ell` agreements, listing requires

```text
R_core >= (m+1-tau)ell = (D+2)ell.                 (1)
```

## The classification theorem

Assume `tau >= 5`, `tau < m < ell`, and that `F_p^*` contains the
`tau+m` distinct `H`-cosets required by the construction.

For `ell in {7,11,13,19}`, no listed full-petal word has exactly two active
nonzero DFT sectors.

For `ell=17`, the same vacancy statement holds except for

```text
p = 1361,    11 <= tau < m < 17.
```

Every parameter pair in this exceptional range has an explicit listed
full-petal word with active sectors `{1,11}`. Its exact missed core is a
primitive divisibility-minimal kernel set.

Thus the exact-two-sector stratum is completely classified for
`ell in {7,11,13,17,19}` in this prime-field regime. This does not classify
words with three or more active sectors and is not a whole-cell vacancy
theorem.

## 1. Exponent-width vacancy

For a nonzero sector pair define `delta_ell(r,s)` as the least cyclic span of
the exponent triple `{0,ur,us}` over all `u in F_ell^*`. Multiplication by a
monomial and the substitution `h -> h^u` turn the restriction on a live
coset into a nonzero polynomial of degree at most `delta_ell(r,s)`. Hence a
live coset retains at most `delta_ell(r,s)` points.

If `z <= D` core labels are sector-dead, then

```text
R_core <= z ell + (m-z) delta_ell(r,s)
       <= D ell + (tau+1) delta_ell(r,s).           (2)
```

Combining (1) and (2) gives the uniform criterion

```text
(tau+1) delta_ell(r,s) < 2 ell  =>  vacancy.        (3)
```

The certificate also verifies the elementary compression bound

```text
delta_ell(r,s)
  <= ceil(sqrt(ell)) + floor(ell/(ceil(sqrt(ell))+1)).
```

This pays every narrow sector pair and isolates a finite wide-pair
frontier.

## 2. Fourier-minor resultant sieve

Normalize a three-exponent support to `{0,1,e}` under `AGL(1,ell)`, and
normalize three distinct roots to `{1,zeta,zeta^w}`. The corresponding
evaluation determinant is

```text
D_{e,w}(X)
  = (X-1)(X^(ew)-1) - (X^e-1)(X^w-1).
```

Its distinct-root Vandermonde factor is

```text
V_w(X) = (X-1)(X^w-1)(X^w-X).
```

Therefore a three-root event in characteristic `p` requires `p` to divide

```text
Res(Phi_ell, D_{e,w}/V_w).                          (4)
```

Exact integer Sylvester determinants, evaluated by fraction-free Bareiss
elimination, give the following complete orbit tables.

| `ell` | normalized resultant values | consequence |
|---:|---|---|
| 7 | `{1,8}` | no admissible odd `p` gives three roots |
| 11 | `{1,23}` | only `p=23`, with too few `H`-cosets |
| 13 | `{1,27,53,729}` | only `p=53`, with too few `H`-cosets |
| 17 | `{1,103,239,1361}` | only `p=1361` survives all guards |
| 19 | `{1,191,343,457,1331,2699,117649}` | only `p=2699` survives all guards |

For `ell=7,11,13`, the resulting live-coset cap is two. Thus

```text
R_core <= D ell + 2(tau+1) < (D+2)ell,
```

which proves vacancy.

For `ell=17,19`, exhaustive ranks of every relevant `3 x 3` and `4 x 3`
evaluation submatrix show that the exceptional local cap is exactly three,
never four. This pays all rows through `tau=10` for `ell=17` and through
`tau=11` for `ell=19`. Coset availability removes the smaller exceptional
characteristics, leaving only

```text
ell=17, p=1361, tau>=11, ratios {4,5,7,11,13,14};
ell=19, p=2699, tau>=12, ratios {4,5,6,14,15,16}.
```

## 3. The `F_1361` counterexample family

At `ell=17`, the sector pair `{1,11}` with normalized coefficient `81` has
quotient spectrum

```text
1^60 2^10 3^10.
```

Selecting the top `m=tau+1` quotient labels and interpolating `P_0` gives
explicit `D=0` listed words for `tau=11,...,15`. Their retained-core counts
are

```text
34, 36, 38, 40, 42.
```

For `D>0`, let `Q_D(Y)` be the locator of `D` new core labels and set

```text
Lambda_D = Lambda_0 Q_D,
P_D(X)   = Q_D(X^17) P_0(X),
g_{1,D}  = Q_D,
g_{11,D} = 81 Q_D.
```

The common factor cancels in every petal scalar and retains each new core
coset completely. This propagates the five anchors to all fifteen pairs
`11 <= tau < m < 17`. The verifier checks every evaluation point, exact
degree, exact DFT support, distinct nonzero petal scalars, listing, exact
missed-core size, and trivial `H`-stabilizer before applying the existing
full-petal/minimal-kernel bijection.

## 4. The `F_2699` vacancy theorem

For `ell=19`, the exact `D=0` quotient census over all
`binom(18,2)=153` sector pairs gives

```text
S_n = n+12,    13 <= n <= 18,
```

where `S_n` is the largest total obtained from the top `n` live-label
multiplicities. Hence `R_core <= 30 < 38`, uniformly in every `D=0` cell.

Now let `D>0`, and let `z` be the number of common core-label roots of
`g_r,g_s`.

If `z <= D-1`, the exact local cap three gives

```text
R_core <= (D-1)19 + 3(tau+2).
```

Its deficit from the listing requirement is

```text
(D+2)19 - R_core >= 3(17-tau) >= 3.
```

If `z=D`, two nonzero polynomials of degree at most `D` sharing `D`
distinct roots are scalar multiples of their common locator. That factor
cancels on all live labels, so the `D=0` quotient census applies without any
rational-function extrapolation:

```text
R_core <= 19D + S_{tau+1} = 19D + tau+13.
```

The deficit is at least `25-tau >= 9`. Both branches are strictly unlisted,
so the entire `F_2699` exact-two-sector frontier is vacant.

## Reproduction

The exact certificates and commands are listed in
`experimental/data/certificates/l1-exact-two-sector/README.md`.

## Consequence and boundary

The result replaces the open two-or-more-sector chart by a complete theorem
on its first nontrivial stratum for five prime orbit lengths. It also shows
that local three-root feasibility does not determine global behavior:
`F_1361` supports a primitive family, whereas the analogous `F_2699`
frontier is globally vacant.

The next unresolved stratum has at least three active nonzero DFT sectors.
No statement here applies to extension fields, backgrounds, partial-petal
words, or the full RS-MCA threshold without the existing reconstruction
hypotheses.
