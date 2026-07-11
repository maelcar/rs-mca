# Low-direction minimum-lift puncture compiler

- **Status:** PROVED for the stated branch.
- **Track:** asymptotic hard input C / the residual ray compiler.
- **Verifier:**
  `python3 experimental/scripts/verify_low_direction_minimum_lift_puncture.py`.

## Theorem

Let `H_U : F^U -> F^R` be the restriction of a Reed-Solomon
parity-check matrix to `N=|U|=R+kappa` coordinates, with `kappa>=1`.
Its kernel is an `[N,kappa,R+1]` generalized Reed-Solomon code.  Fix
`0<=t<R`, a syndrome line `y_0+gamma y_1`, and a set `Z` of distinct
actual transverse slopes.  For every `gamma in Z`, choose a witness
`c_gamma in F^U` satisfying

```text
H_U c_gamma = y_0 + gamma y_1,
wt(c_gamma) <= t,
{y_0,y_1} not subset V_(supp(c_gamma)).                    (1)
```

If `|Z|>=2`, then `y_0,y_1` lie in the image of `H_U`.  Define the
direction distance

```text
d = min{wt(v): H_U v=y_1}.
```

Choose a minimum lift `v`, put `J=supp(v)`, and set

```text
M = N-d,
Delta = R+1-d = M-kappa+1,
s = min(t,M).                                              (2)
```

Puncturing `J` maps `ker H_U` injectively onto an
`[M,kappa,Delta]` GRS code `C_J`.  It maps the affine solution set

```text
{u in F^U : H_U u=y_0}
```

onto one affine coset `A` of `C_J`.

For `w in A`, let `e=wt(w)`.  Then the exact weighted slope reduction is

```text
|Z| <= sum_(w in A, wt(w)<=s)
         floor(d / max(1,d+wt(w)-t)).                      (3)
```

In particular, if

```text
Delta M - 2sM + s^2 > 0,                                  (4)
```

then

```text
|Z| <= d floor( M(Delta-s)/(Delta M-2sM+s^2) ) <= N^3.    (5)
```

When `t<=M`, condition (4) is equivalently

```text
(M-t)^2 > M(kappa-1).                                     (6)
```

This is a field-independent polynomial ray payment, including charts
with `kappa=Theta(N)`.

## Exact puncture and multiplicity proof

Every nonzero kernel word has weight at least `R+1`, while `d<=R`
because any `R` parity columns form a basis.  A kernel word killed by
puncturing `J` would be supported on at most `R` coordinates and hence
would vanish.  Puncturing is therefore injective and preserves dimension
`kappa`.  Its distance is at least `R+1-d`; Singleton gives the reverse
inequality, proving the `[M,kappa,Delta]` statement.  The same argument
is injective on the affine solution set because two solutions differ by a
kernel word.

For one selected slope, put

```text
u_gamma = c_gamma - gamma v.
```

Then `H_U u_gamma=y_0`, and outside `J` one has
`u_gamma=c_gamma`.  Thus its puncture `w_gamma` belongs to `A` and has
weight at most `s`.

Fix `w in A`.  It has a unique affine lift `u`.  Every slope mapping to
`w` has

```text
c_gamma = u + gamma v.                                    (7)
```

Outside `J` this word has exactly `e=wt(w)` nonzero coordinates, so its
weight bound forces at least `d+e-t` zeros on `J` when this is positive.
Transversality forces at least one such zero even when `d+e-t<=0`: if
there were none, both `u` and `v` would be supported inside
`supp(c_gamma)`, putting both line generators in its parity-column span.

Every coordinate in `J` is a nonconstant affine function of `gamma`, so
it vanishes for at most one slope.  The entire cluster has at most `d`
zero incidences, while each slope consumes at least
`max(1,d+e-t)`.  This proves (3).

## Punctured Johnson proof

Let `w_1,...,w_L` be the words of `A` of weight at most `s`, and enlarge
their supports to `s`-sets `T_i`.  Since differences of affine-coset
words are nonzero codewords of distance at least `Delta`,

```text
|T_i union T_j| >= Delta,
|T_i intersect T_j| <= 2s-Delta.                          (8)
```

If `r_x` counts the selected sets containing coordinate `x`, then

```text
sum_x binom(r_x,2) <= binom(L,2)(2s-Delta),
sum_x binom(r_x,2) >= (L^2 s^2/M-Ls)/2.
```

Rearrangement gives

```text
L(Delta-2s+s^2/M) <= Delta-s.                             (9)
```

Under (4), (9) and the crude cluster multiplier `d` prove (5).  The
denominator in (5) is then a positive integer, so the final `N^3` bound
follows directly.

## Strictly new positive-rate regime

For every `m>=5`, take

```text
N=9m, R=8m, kappa=m, t=4m, d=2m.
```

Then `M=7m` and `Delta=6m+1`.  The existing high-direction theorem does
not apply because

```text
(N-t)^2 = 25m^2 <= 63m^2 = N(N-d),
```

and the integrated deep branch does not apply because `3t>R`.  In
contrast, the denominator in (5) is `m(2m+7)>0`, and

```text
|Z| <= 2m floor(7(2m+1)/(2m+7)) <= 12m.                  (10)
```

These parameters occur in actual RS geometry.  In the weighted-kernel
representation

```text
ker H_U = {(omega_x p(x))_(x in U): deg p<m},
```

choose a `7m`-set `T_0` and put

```text
v(x)=omega_x Q_(T_0)(x).
```

It has support `U\T_0` of size `2m`.  Adding a degree-less-than-`m`
kernel polynomial cannot reduce the degree `7m`, so every lift has at
most `7m` zeros and `d=2m` exactly.

The slope locus is nonempty.  Assign distinct field values `gamma_x` to
the `2m` points outside `T_0`; choose `u` to vanish on `T_0` and satisfy
`u(x)=-gamma_x v(x)` there.  At slope `gamma_x`, the witness
`u+gamma_x v` is supported on the other `2m-1` points.  The unique
independent-column representation of `y_1` on this `2m`-set uses every
coordinate, so the witness is transverse.  This gives `2m` actual
slopes while (10) supplies the uniform upper payment.

## Ledger effect and remaining wall

This strictly extends the integrated direction-distance compiler into a
nonempty positive-rate part of its complementary locus.  For one actual
first-match chart satisfying (4), it proves the direct payment

```text
|Z_lambda^o| <= exp(o(n))(1+barN_lambda).
```

After combining the old and new branches, an unpaid chart must satisfy
both

```text
(N-t)^2 <= N(N-d),
Delta M - 2sM + s^2 <= 0.                                 (11)
```

The exact remaining object is therefore a beyond-Johnson low-weight list
in the punctured affine GRS coset `A`, at the actual profile scale.

## Nonclaims

- This does not pay every low-direction chart.
- It does not prove witness-exhaustiveness or a global atlas count.
- It does not prove a Prouhet or prefix max-fiber theorem.
- It does not prove a profile-envelope comparison.
- It does not change any finite M31 or KoalaBear cell.
- It does not prove a deployed adjacent inequality.
- No paper TeX is changed.
