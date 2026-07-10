# Direction-distance ray compiler for a large residual kernel

**Lane:** asymptotic hard input 3, the residual ray compiler.

**Status:** `PROVED` for the stated high-direction-distance branch, including
some charts with kernel dimension `Theta(n)`; `OPEN` for the complementary
low-direction-distance locus, witness-atlas coverage, and the full residual
ray input.

**Verifier:**
`experimental/scripts/verify_direction_distance_ray_compiler.py` (zero
argument, stdlib only, exact prime-field arithmetic).

## 1. Exact chart theorem

Let `F` be a field, `D` an RS evaluation set, and

```text
h_x = lambda_x(1,x,...,x^(R-1))^T,  lambda_x != 0
```

the weighted RS parity columns of redundancy `R`.  Fix a chart `U` of size

```text
N=|U|=R+kappa,  kappa>=1,
```

and write

```text
H_U e = sum_(x in U)e_x h_x,
K_U = ker H_U.
```

The MDS property gives

```text
dim K_U=kappa,  d_min(K_U)=R+1.                            (1)
```

Fix `0<=t<=R-1`, a nonconstant syndrome line `y0+gamma y1`, and one
actual first-match residual profile `lambda`.  Let `Z^o_(lambda,U)` be its
transverse slopes admitting a witness supported on at most `t` coordinates
inside `U`.

For `y1 in im H_U`, define the chart-direction distance

```text
d_U(y1)=min{wt(v):H_U v=y1},
mu_U(y1)=N-d_U(y1).                                       (2)
```

Equivalently, for any lift `b1`,

```text
d_U(y1)=min_(z in K_U) wt(b1+z),
mu_U(y1)=max_(z in K_U)|{x:b1(x)+z(x)=0}|.
```

If `Z^o_(lambda,U)` has at least two slopes, then `y0,y1` lie in the chart
span.  If

```text
(N-t)^2 > N mu_U(y1),                                     (3)
```

equivalently

```text
d_U(y1) > 2t-t^2/N,
```

then

```text
|Z^o_(lambda,U)|
 <= floor( N(N-t-mu_U) / ((N-t)^2-N mu_U) )
  = floor( N(d_U-t) / ((N-t)^2-N(N-d_U)) )
 <= N^2.                                                   (4)
```

The bound is field-independent and uniform in the received line, profile,
and witness choices.

## 2. Proof by one extension-code ball

Choose lifts `b0,b1` of `y0,y1`.  For each selected slope choose one actual
witness.  It has the form

```text
e_gamma=b0+gamma b1+z_gamma,  z_gamma in K_U,
wt(e_gamma)<=t.                                            (5)
```

Define the direction-extension code

```text
L_U(y1)=K_U+<b1>.
```

Its minimum distance is exactly `d=d_U(y1)`: words outside `K_U` are
nonzero scalings of a lift of `y1`, while words in `K_U` have weight at least
`R+1` and every syndrome has an `R`-coordinate representative, so `d<=R`.

Put

```text
c_gamma=-gamma b1-z_gamma.
```

Distinct slopes give distinct codewords and (5) places all `c_gamma` in one
radius-`t` Hamming ball about `b0`.  Let `s=N-t` and choose an `s`-subset
`B_gamma` of the coordinates on which `b0=c_gamma`.  Distinct extension-code
words have distance at least `d`, hence

```text
|B_gamma intersect B_gamma'| <= N-d=mu.                   (6)
```

If `M` slopes are selected and `r_x` counts the selected sets containing
coordinate `x`, then

```text
M^2 s^2/N <= sum_x r_x^2
            <= Ms+M(M-1)mu.
```

Under (3), rearranging gives

```text
M <= N(s-mu)/(s^2-Nmu),
```

which is (4).  First-match and transversality only restrict the selected set,
so no generic image surrogate replaces the actual witness geometry.

## 3. Direction-MDS specialization

Let `G` be an `N x kappa` kernel basis matrix.  The following are equivalent:

1. `d_U(y1)=R`;
2. `mu_U(y1)=kappa`;
3. `K_U+<b1>` is an `[N,kappa+1,R]` MDS code;
4. every `(kappa+1)`-row minor of `[G|b1]` is nonzero.

The last condition says exactly that every slope coefficient in the affine
minors used by the integrated transverse-secant theorem is nonzero.  On this
branch, (3)-(4) become

```text
(N-t)^2>N kappa,

|Z^o_(lambda,U)|
 <= floor(N(R-t)/((N-t)^2-Nkappa)) <= N^2.                 (7)
```

There is an explicit certificate in RS geometry.  Put

```text
Q_U(X)=prod_(u in U)(X-u),
omega_u=(lambda_u Q'_U(u))^(-1).
```

Then

```text
K_U={(omega_u p(u))_(u in U):deg p<kappa}.                 (8)
```

For any polynomial `f` of exact degree `kappa`, the lift

```text
b1(u)=omega_u f(u)
```

has direction distance `R`: adding a polynomial of degree below `kappa`
does not change the leading term, so every lift has at most `kappa` zeros;
interpolation attains exactly `kappa` zeros.

Thus, for an asymptotic direction-MDS sequence with

```text
kappa/N -> theta in (0,1),  t/N -> tau,
tau < 1-sqrt(theta),                                        (9)
```

the chart has `kappa=Theta(n)` but still

```text
|Z^o_(lambda,U)| <= n^2=e^{o(n)}.
```

For `N=4m`, `R=kappa=2m`, and `t=m`, (7) gives the constant bound `4`,
while the integrated deep condition `3t<=R` fails.  This is a genuinely new
large-kernel branch beyond the existing one-minor charge and deep theorem.

## 4. Exact impact and remaining wall

For each fixed actual first-match chart satisfying (3), this proves the direct
ray budget

```text
|Z^o_(lambda,U)| <= e^{o(n)}(1+barN_lambda).
```

It therefore pays hard input 3 only on the high-direction-distance branch.
It does not prove that all actual residual directions satisfy (3), that every
large-kernel direction is MDS, that all witnesses lie in a fixed chart, or
that an `e^{o(n)}` witness-exhaustive atlas exists.

The exact remaining locus is

```text
d_U(y1) <= 2t-t^2/N.                                      (10)
```

The next target is a witness-preserving reduction of every actual chart in
(10) to an already paid quotient, planted, tangent, rank-drop, curve, pencil,
or bounded-kernel cell, or a direct slope bound at its actual profile scale.

This packet has zero finite-ledger effect: it removes no deployed M31 cell,
does not fit the roughly three-bit M31 margin, and proves no deployed row.

## 5. Validation

Run

```text
python3 experimental/scripts/verify_direction_distance_ray_compiler.py
```

The verifier constructs exact weighted-RS kernels over `F_5` and `F_7`,
checks (8), exhausts extension-code Hamming balls, and enumerates every
projective syndrome direction in three `F_5` charts.  It includes non-MDS
directions, checks the paid predicate independently, and attains the bound
with zero slack in the small cases.  No floating-point computation, optimizer,
or sampling is used.
