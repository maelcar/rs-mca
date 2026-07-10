Continues the M31 two-shell wall in
`cap25_v13_m31_two_shell_wall.md`.  The numerical comparison uses the exact
Johnson `j<=6` certificate in open PR #495; the theorem itself is standalone.

# M31 anchored two-shell Gram cut: 97,162 exact pair exclusions, 97,019 new beyond PR #495

Status: `PROVED` (the local Gram/Turan obstruction, its exact M31 cut, and the
comparison with the exact PR #495 scanner) / `OPEN` (the remaining two-shell
grid, the many-shell residual, and the deployed M31 list row).

Verifier:
`experimental/scripts/verify_m31_anchored_shell_gram_cut.py` (stdlib only,
integer decisions).  Data:
`experimental/data/cap25_v13_m31_anchored_shell_gram_cut.json`.

## 1. Result

Use the deployed constants

```text
p=2^31-1=2147483647, n=2^21=2097152,
a+=1116023, m=n-a+=981129, w=67447,
B*=2^24-1=16777215, L0=B*+1=16777216=8n,
R=m(n-m)=1094962529967, r=n-w=2029705.
```

Let `F` be a family of `m`-subsets in one depth-`w` M31 Chebyshev prefix
fiber.  The statement is hereditary: `F` may be any first-match residual
obtained by deleting earlier cells.  Suppose its off-diagonal exchange
distances are exactly `e1<e2`.  If `|F|>=L0`, the existing integral-ratio
reduction gives

```text
e1=(kappa-1)t, e2=kappa*t, 2<=kappa<=774,
ceil(67448/(kappa-1)) <= t
  <= min(floor(981129/kappa), floor(R/(2097152*(kappa-1)))).       (1.1)
```

This note proves the new necessary condition

```text
8*n*kappa^2*t <= (9*kappa+7)*m*(n-m).                            (1.2)
```

The strict reverse of (1.2) excludes exactly these grid intervals:

```text
kappa=2: 407906<=t<=490564       82659 pairs
kappa=3: 246557<=t<=261059       14503 pairs
                                  -----
                                  97162 pairs
```

The exact `j<=6` Johnson scan of PR #495 already excludes 143 of them,
precisely `kappa=3, 260917<=t<=261059`.  The genuinely new cut is therefore

```text
kappa=2: 407906<=t<=490564       82659 pairs
kappa=3: 246557<=t<=260916       14360 pairs
                                  -----
                                  97019 pairs.
```

Relative to PR #495's `3,254,358` survivors, the combined surviving count is

```text
3157339.
```

This applies the local PSD/realizability lever named after the global Johnson
LP and modular-nullity routes saturated.  It pays only the listed two-shell
parameter cells.

## 2. Prefix-fiber one-shell cap

The evaluation rows `T_0,...,T_w` on the `n` distinct M31 domain points have
rank `w+1`: a dependence would be a nonzero polynomial of degree at most
`w<n` vanishing at all domain points.  Since `T_0=1`, fixed weight together
with the depth-`w` prefix puts every incidence vector in an affine subspace
`V` of `F_p^n` with

```text
dim V <= n-w-1.                                                (2.1)
```

Join two members of `F` when their exchange distance is `e1`, obtaining a
graph `G`.  If `C` is a clique, define on `V`

```text
f_A(x)=1_A dot x-(m-e1),  A in C.
```

For `A,B in C`, evaluation at the incidence vector of `B` gives `e1` when
`A=B` and zero otherwise.  Here `0<e1<=m<p`, so `e1` is nonzero in `F_p`.
Thus the restrictions `f_A|V` are linearly independent.  The affine-linear
functions on `V` have dimension at most `dim V+1`, and hence

```text
omega(G) <= n-w = r.                                          (2.2)
```

## 3. Turan forces an eight-vertex anchor shell

Select any `L0` members.  The graph `G` is `K_(r+1)`-free.  Write

```text
L0=8r+8w, q=8, s=8w=539576<r.
```

Turan's theorem says the complement has at least

```text
s*C(9,2)+(r-s)*C(8,2)=28n+36w=61148348                   (3.1)
```

edges.  Complement edges are exactly the `e2` pairs, so their average degree
is at least

```text
2(28n+36w)/(8n)=7+9w/n>7.                                (3.2)
```

Some anchor `A` therefore has an integral `e2`-shell

```text
H={B in F: d(A,B)=e2}, h=|H|>=8.                          (3.3)
```

## 4. Anchored Gram sum-of-squares certificate

For `B in H`, put `y_B=1_B-1_A`.  For `i` outside `A`, let `P_i` count the
members of `H` adding `i`; for `i` in `A`, let `Q_i` count the members deleting
`i`.  Both coordinate totals are `h*e2`.  Expanding pairwise squared
differences gives the exact identity

```text
m(n-m)*|sum_B y_B|^2-n*h^2*e2^2
 = (n-m)*sum_{i<j in A}(Q_i-Q_j)^2
   + m*sum_{i<j outside A}(P_i-P_j)^2
 >= 0.                                                       (4.1)
```

Consequently

```text
|sum_B y_B|^2 >= n*h^2*e2^2/[m(n-m)].                       (4.2)
```

For distinct `B,C in H`,

```text
y_B dot y_C = 2e2-d(B,C) <= 2e2-e1,
|y_B|^2=2e2.
```

Therefore

```text
|sum_B y_B|^2
 <= 2e2*h+h(h-1)(2e2-e1)
 = t*((kappa+1)h^2+(kappa-1)h).                              (4.3)
```

Combining (4.2) and (4.3), cancelling positive `h,t`, and using `h>=8`
gives

```text
n*kappa^2*t
 <= m(n-m)*(kappa+1+(kappa-1)/h)
 <= m(n-m)*(kappa+1+(kappa-1)/8),
```

which is exactly (1.2).  This is an anchor-conditioned Gram/Terwilliger
constraint, not another inequality in the global two-point Johnson inner
distribution.

## 5. Exact finite arithmetic

For `kappa=2`, (1.2) is `32nt<=25R` and

```text
floor(25R/(32n))=407905.
```

For `kappa=3`, it is `72nt<=34R` and

```text
floor(34R/(72n))=246556.
```

The exact first-failure cross-products are

```text
(2,407905): -22079255
(2,407906):  45029609
(3,246556): -16606014
(3,246557): 134388930.
```

There is no cut for `kappa>=4`.  The grid gives
`t<=R/[n(kappa-1)]`, while

```text
(9kappa+7)(kappa-1)-8kappa^2
  = kappa^2-2kappa-7 >= 1.
```

The verifier regenerates all `3,254,885` grid pairs, all `97,162` Gram cuts,
the exact PR #495 overlap through `j<=6`, the three canonical hashes, and the
SOS identity on `65,554` deterministic toy shell families.  Its all-cut and
new-cut hashes independently match the worker packet:

```text
all: d0aee9adbf972674d42e496d10584340e2208d27bb5bc234c29cbcf322a4e91b
new: 0c58ac156c4a147c09712a818e409d475295b7f3a082686bfdf4c801a75d32c6
```

## 6. Ledger impact and nonclaims

For every listed cut pair, no two-shell subfamily of one deployed M31 prefix
fiber can have `B*+1` members.  Equivalently, that individual shell-pair cell
has size at most `B*`.

This does **not** sum different shell-pair cells.  It does not pay the
remaining `3,157,339` parameter pairs, a residual with three or more shells,
the many-shell inverse problem, row-sharp Q, a complete first-match upper
ledger, or the M31 deployed row.  It proves no MCA statement from this list
fiber theorem.

The next exact target is `M31-ANCHORED-MULTISHELL-TERWILLIGER-DUAL`: retain all
anchor-shell populations and cross-shell triple-intersection blocks, then
combine their local PSD constraints with the deployed modular nullity.  Either
produce an exact infeasibility dual at total size `L0`, or print an integral
feasible local-distribution certificate that cuts this route.
