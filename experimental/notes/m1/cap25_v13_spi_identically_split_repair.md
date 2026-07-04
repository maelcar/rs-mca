# CAP25 v13 SPI identically split repair

Status: PROVED / AUDIT / EXACT_NEW_WALL.

This note records a hostile-audited repair to the CAP25 v13 experimental SPI
deficiency-one chart in `experimental/cap25_v13_experimental.tex`.  The repair
is local: it removes one overconservative residual branch and records a fixed
generic-kernel-dimension payment theorem.  It is not a proof of the full M1
aperiodic local limit and it does not close the CAP25 Johnson-facing band.

## 1. Identically split top charts are contained

Work in the v13 deficiency-one SPI chart:

```text
j = n-A,   t = A-k = j,   M(Z)=U+ZV.
```

For the `j x (j+1)` pencil, let `c_i(Z)` be the signed maximal minors and

```text
L_Z(X)=sum_{i=0}^j c_i(Z) X^i.
```

Assume the domain polynomial is split and squarefree over the constant field,
as in the v13 root-of-unity row

```text
P_D(X)=X^n-1=prod_{h in H}(X-h),   char(F) does not divide n.
```

If `c_j` is not identically zero and the pseudo-remainder

```text
c_j(Z)^Delta P_D(X) = Q(Z,X)L_Z(X)+R(Z,X)
```

has `R(Z,X)=0`, then over `F(Z)` the monic normalization `L_Z/c_j` is a
degree-`j` divisor of the split squarefree polynomial `P_D`.  Hence

```text
L_Z(X)=c_j(Z)L_T(X)
```

for one fixed split locator `L_T`, `T subset D`, `|T|=j`.

The cofactor identity gives

```text
M(Z)(c_0(Z),...,c_j(Z))^T=0,
```

and therefore

```text
M(Z) ell_T = 0.
```

In the exact syndrome-pencil application this means

```text
U ell_T = 0,   V ell_T = 0.
```

By the support-locator syndrome recurrence and exact line-image map, both line
coordinates are explained on the same support `D \ T`.  The support-wise
noncontainment gate `V ell_T != 0` fails.  Thus the full-rank identically split
top chart contributes zero exact-`A` support-wise noncontained MCA slopes.

Roots of `c_j` are not erased.  In this branch `c_i=c_j ell_{T,i}` for every
`i`, so roots of `c_j` are roots of every maximal minor and remain in the
rank-drop ledger.

## 2. Fixed generic kernel dimension is paid

Let

```text
M(Z)=U+ZV in F[Z]^{t x (j+1)},
rho = rank_{F(Z)} M(Z),
s = j+1-rho.
```

Count finite slopes `z` for which some split locator `L_T`, `|T|=j`, satisfies

```text
M(z) ell_T = 0,   V ell_T != 0.
```

The hostile audit supports the sharper fixed-`s` bound

```text
0,                         if rho = 0;
rho,                       if s = 0;
rho + rho * binom(n,s),    if 1 <= s <= j.
```

The proof chooses one nonzero `rho x rho` pivot minor.  Away from its roots,
the kernel has dimension `s`.  For each `Y subset D`, `|Y|=s`, stack the pencil
with evaluation at `Y`; any transverse stacked determinant has degree at most
`rho`.  If all such `Y subset T` determinants vanish identically for a
witnessed support `T`, then the evaluation map from `ker M(Z)` to `F(Z)^T`
has rank below `s`, so a nonzero kernel polynomial of degree at most `j`
vanishes on all `j` points of `T`.  It is a scalar multiple of `L_T`, hence
`M(Z)ell_T=0` and `Vell_T=0`, contradicting noncontainment.

This fixed-`s` payment does not compress the binomial term when `s` grows.

## 3. Remaining wall

The remaining M1 wall is:

```text
CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-DETERMINANT-COMPRESSION
```

Equivalently, one must either compress the growing-`s` term
`rho * binom(n,s)` using the special syndrome-Hankel one-parameter pencil and
the noncontainment projection, or construct a primitive growing-`s`
counterpacket.

## 4. Non-claims

This note is not an official prize solve.  It is not protocol soundness
failure.  It is not ordinary list decoding unless separately proved.  It does
not determine the exact `delta_C^*`.  It does not refute Paper B's corrected
positive theory above its full reserve.  It is not evidence that no reserve
theorem exists.  It is not a reason to ignore the distinctions between
`q_gen`, `q_line`, `q_code`, and `q_chal`.
