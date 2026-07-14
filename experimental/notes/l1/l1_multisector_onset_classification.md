# L1 Multisector Onsets and the Common-Root Deficit Theorem

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE

## Setting

Let `p` and `ell` be primes with `ell | (p-1)`, and put
`H=mu_ell <= F_p^*`. Consider a background-free coset sunflower with `tau`
petals and `m` core cosets, where

```text
5 <= tau < m < ell,    D=m-tau-1.
```

For a full-petal codeword, write the nonzero `H`-DFT sectors as

```text
P_a(X^ell) X^a,    a in A,
```

where `A` is the active sector set. Full-petal agreement forces

```text
P_a = phi g_a,    deg(g_a) <= D,
```

for every `a in A`. A core label is *fully sector-dead* when every `g_a`
vanishes there. Let `z` be the number of fully sector-dead core labels.
Then `z <= D`.

Write `R_core` for retained core positions. Listing requires

```text
R_core >= (D+2)ell.                                  (1)
```

This note treats the first strata beyond exact two-sector support. It gives
a general compiler for any number of active sectors, classifies the
exact-three-sector `D>0` onset for `ell=11,13,17,19`, and gives exact-three-
and exact-four-sector witnesses in the unique `ell=7` cell.

## The common-root deficit theorem

Assume two independent inputs for the active support family under study.

1. Every live core coset has fiber size at most `c`, for every nonzero
   coefficient specialization arising when any proper subset of the
   cofactors vanishes.
2. If all active cofactors are scalar multiples of one locator, the sum of
   the `h` largest live-label fibers is at most `S_h`.

Then, for `D>=1`,

```text
R_core
 <= max((D-1)ell+c(tau+2), D ell+S_(tau+1)).          (2)
```

Equivalently, the surplus over the listing threshold is at most

```text
max(c(tau+2)-3ell, S_(tau+1)-2ell).                  (3)
```

More precisely, if `q=D-z>=1`, then

```text
R_core <= (D-q)ell+c(tau+1+q),                       (4)
```

whose listing surplus is at most

```text
c(tau+1+q)-(q+2)ell.
```

### Proof

If `z<D`, grant all `z` fully dead cosets their `ell` points and apply the
robust cap `c` to every other core coset:

```text
R_core <= z ell+c(m-z).
```

Substituting `m=tau+1+D` and `q=D-z` gives (4). Since `c<=ell`, the largest
bound in this branch occurs at `q=1`, giving the first term of (2).

If `z=D`, every nonzero polynomial `g_a` of degree at most `D` vanishes on
the same `D` distinct labels. Hence

```text
g_a = lambda_a Q
```

for their common monic degree-`D` locator `Q`. On live labels, `Q` cancels
from all fiber multiplicities. There are `m-D=tau+1` live labels, so their
total is at most `S_(tau+1)`, while the dead labels contribute `D ell`.
This gives the second term of (2).

For `D=0`, all nonzero cofactors are constants and the exact bound is simply

```text
R_core <= S_(tau+1).                                 (5)
```

The theorem is elementary but load-bearing: it turns local Fourier-minor
caps and proportional spectra into whole-grid vacancy statements without
extrapolating constant cofactor ratios into the genuinely rational branch.

## The unique `ell=7` cell

Here `(tau,m,D)=(5,6,0)`.

### Exact three sectors

For every prime `p=1 mod 7` and every constant-free `Gamma` with exactly
three nonzero monomials among `X,...,X^6`, let `S_6(Gamma)` denote the sum
of its six largest `mu_7`-coset fibers. Then

```text
S_6(Gamma) <= 14.                                    (6)
```

The proof combines normalized `4 x 4` Fourier-minor norms, a complete
translation-orbit invariant for triple fibers, and exact exceptional-prime
state enumeration. The bound is sharp. Over `F_113`,

```text
Gamma = X+67X^3+75X^5
```

has spectrum `3^2 2^4 1^10` and top-six sum `14`. Reconstruction gives a
listed word with exactly active sectors `{1,3,5}`, agreement `49`, degree
`40`, and a primitive divisibility-minimal missed core of size `28`.

### Exact four sectors

For every prime `p=1 mod 7`, every constant-free four-monomial `Gamma` has
fiber size at most four. All `21^2` normalized five-point Fourier minors
have cyclotomic quotient norm one.

The cap is attained over `F_127` by

```text
Gamma = X+64X^2+112X^3+70X^5,
```

whose spectrum is `4^1 2^6 1^11`. Reconstruction gives a listed word with
active sectors `{1,2,3,5}`, agreement `49`, degree `40`, and a primitive
divisibility-minimal missed core of size `28`.

Thus the all-six-sector witness already present in this cell is not the
first multisector phenomenon: exact-three and exact-four strata are both
nonempty.

## Exact-three-sector `D>0` onsets

The common-root theorem, complete AGL-normalized Fourier-minor resultants,
exceptional-characteristic state censuses, and explicit common-dead padding
give the following sharp classification.

| `ell` | universally vacant rows | first nonvacant `tau` | witness field | active polynomial |
|---:|---|---:|---:|---|
| 11 | `tau=5,6` | 7 | `F_353` | `X+345X^5+49X^9` |
| 13 | `tau=5,6,7` | 8 | `F_521` | `X+167X^5+371X^9` |
| 17 | `5<=tau<=10` | 11 | `F_5441` | `X^3+3370X^8+3741X^13` |
| 19 | `5<=tau<=9` | 10 | `F_4409` | `X+2307X^9+251X^17` |

In every row below the listed onset, every prime field supporting the full
sunflower is vacant in the exact-three-sector `D>0` stratum. At and above
the onset, every admissible `D>0` row has an explicit primitive listed word
over the displayed field.

The exact grid sizes are:

| `ell` | vacant parameter pairs | explicit nonvacant pairs |
|---:|---:|---:|
| 11 | 7 | 3 |
| 13 | 15 | 6 |
| 17 | 45 | 10 |
| 19 | 50 | 28 |

Each witness is checked pointwise for full-petal agreement, exact active
DFT support, degree, listing, exact missed core, divisibility minimality,
and trivial `H`-stabilizer. The `D>0` families are obtained from verified
`D=0` anchors by multiplying both the codeword and core locator by the same
`Q_D(X^ell)`, so the petal scalars and missed core are preserved.

## Exceptional-state compression

For `ell=17`, normalized five-root gcds reduce the 23 exceptional
characteristics to `p=137`. That field has only eight quotient labels and
cannot host the smallest parameter row. Every available live specialization
therefore has robust cap four. A complete projective census checks 4,000
singular four-root rows and gives `S_11<=33`.

For `ell=19`, five-root gcds reduce to powers of `7,11,37`; none is
`1 mod 19`. Thus the robust cap is again four. A complete projective census
checks 6,837 singular states over 44 exceptional primes and gives
`S_10<=36`, with equality only at `p=4409`.

Substitution in (2) proves all vacancy rows in the table.

## Strong correction: the onset is not monotone

The values

```text
7, 8, 11, 10    for ell=11,13,17,19
```

show that the sharp exact-three-sector onset is not monotone in `ell`.
In particular, the natural extrapolation

```text
tau_onset = ceil(2ell/3)-1
```

matches `ell=17` but predicts `12` at `ell=19`; the exact onset is `10`.
The cause is arithmetic: `F_4409` has eight four-point fibers for one
three-sector polynomial, giving spectrum

```text
4^8 2^8 1^216
```

and `S_11=38`. A generic three-fiber heuristic misses this exceptional
geometry.

This is a correction to any safe-side strategy that extrapolates onset from
orbit length alone. Exceptional field arithmetic must remain in the finite
ledger.

## Scope and next boundary

The theorem covers prime fields, background-free full petals, exact-three
active sectors for the displayed `D>0` grids, and the exact-three/four
`ell=7,D=0` cell. It does not classify extension fields, backgrounds,
partial petals, four-or-more-sector `D>0` grids, or the whole RS-MCA cell.

The next nonempty unresolved layer is exact four active sectors with `D>0`,
beginning at `ell=11`. Its analogous local obstruction requires six-root
Fourier-minor compression and a proportional exact-four spectrum envelope.

## Reproduction

Commands and generated artifacts are listed in
`experimental/data/certificates/l1-multisector-onsets/README.md`.
