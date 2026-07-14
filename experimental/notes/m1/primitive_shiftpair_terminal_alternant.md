# Primitive Shift-Pair Terminal Alternant

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED / COUNTEREXAMPLE / OPEN ACTIVE BOUND

## Purpose

This note isolates an algebraic subproblem that occurs when a primitive
shift-pair collision is transported down a two-to-one Chebyshev tower. It
proves two uniform vanishing-stratum bounds, gives an exact linear alternant
representation for every remaining pair, and refutes the unrestricted
full-spark shortcut for that alternant.

The results sharpen the structural shift-pair analysis. They do not prove
the finite active capacity bound and do not replace the max-fiber theorem
used by the current global closure.

## Terminal locator setting

Let `K=F_p` with `p` odd. Normalize

```text
T_2(X) = 2X^2-1
```

and let `D_0` be a complete simple Chebyshev fiber of size `M=2^rho`.
Every map used below is two-to-one. Fix `e=4r`.

At level two, fix a squarefree-coprime monic bottom pair `(F_2,G_2)`, with
both polynomials split and of degree `e`. A level-one mask selects one point
from each two-point fiber above every root of `F_2` and `G_2`. Write its
normalized level-one locators as `mathcal F,mathcal G`.

Terminal compatibility supplies `c in K^*` and polynomials `E,O` such that

```text
E^2 - mathcal G = Y O^2,
mathcal F = mathcal G + 2cE + c^2,                  (1)
```

with

```text
deg(E) <= 2r,    deg(O) <= 2r-1,
deg(mathcal F) = deg(mathcal G) = e.
```

Take two distinct terminal-compatible masks above the same bottom. Add a
prime to data belonging to the second mask. The bottom synchronizes the
same nonzero scalar `c` for both masks. Define

```text
A = E-E',
B = Y(O-O')(O+O'),
V = mathcal G-mathcal G',
U = mathcal F-mathcal F'.                          (2)
```

Subtracting (1) gives

```text
V = A(E+E') - B,
U = A(E+E'+2c) - B,
U-V = 2cA.                                         (3)
```

The common bottom and synchronized leading term give

```text
deg(A) <= 2r-1,    deg(U),deg(V) <= e-1.            (4)
```

Let `Z_G` be the common roots of `mathcal G,mathcal G'`, and let `Z_F` be
the common roots of `mathcal F,mathcal F'`. These sets are disjoint because
the fixed bottom pair is coprime. If `d_bin` is the Hamming distance between
the two binary masks, then

```text
d_bin = 2e-|Z_F|-|Z_G|.                             (5)
```

## Theorem 1: the `A=0` stratum

For two distinct masks satisfying (1)-(4),

```text
A=0  =>  |Z_F|+|Z_G| <= e-1.                       (6)
```

Indeed, (3) gives `U=V`. This common polynomial cannot vanish identically:
otherwise both pairs of level-one locators coincide, hence the two masks
coincide. Every point in the disjoint union `Z_F union Z_G` is a root of
the same nonzero polynomial of degree at most `e-1`. Equation (6) follows.
By (5), this stratum has `d_bin >= e+1`.

## Theorem 2: the `B=0` stratum

For two distinct masks satisfying (1)-(4),

```text
A != 0 and B=0  =>  |Z_F|+|Z_G| <= 6r-1.           (7)
```

Since `K[Y]` is an integral domain, `B=0` implies `O=O'` or `O=-O'`.
Put `W=E+E'`. Then

```text
V=AW,    U=A(W+2c).                                (8)
```

If `W=0`, then all `e` common `G` roots are possible, while the common `F`
roots are roots of the nonzero polynomial `2cA`. Thus their total is at
most `e+2r-1=6r-1`. The case `W+2c=0` is symmetric.

If both `W` and `W+2c` are nonzero, first charge all roots lying in `Z(A)`.
Every remaining root in `Z_G` is a root of `W`, and every remaining root in
`Z_F` is a root of `W+2c`. Therefore

```text
|Z_F|+|Z_G|
  <= deg(A)+deg(W)+deg(W+2c)
  <= (2r-1)+2r+2r = 6r-1.
```

By (5), this gives `d_bin >= 2r+1=e/2+1` throughout the `B=0` stratum.

## Theorem 3: shared-even alternant reduction

Choose one global top orientation for each mask. Every common intermediate
coordinate has a selected top root `x` and a tag recording whether the
second selected root is `x` or `-x`. Put

```text
C_- = O-O',    C_+ = O+O',    s=x^2.
```

The top-root equations imply

```text
A(s)+x C_-(s)=0    for a same-orientation coordinate,
A(s)+x C_+(s)=0    for an opposite-orientation coordinate.   (9)
```

For a tagged node define the row

```text
R(x,same) =
  (1,s,...,s^(2r-1); x,xs,...,xs^(2r-1); 0,...,0),

R(x,opposite) =
  (1,s,...,s^(2r-1); 0,...,0; x,xs,...,xs^(2r-1)). (10)
```

Equations (9) say that the coefficient vector of `(A,C_-,C_+)` lies in the
kernel of this matrix. It is nonzero for distinct masks. Consequently every
terminal pair with at least `6r` common coordinates produces a singular
`6r`-row minor of the shared-even alternant (10).

This is an exact reduction, not a rank theorem. Realizable rows additionally
satisfy the two nonlinear fixed-bottom norm-collision identities.

## Counterexample to ambient full spark

The claim that every balanced shared-even alternant on distinct Chebyshev
nodes has full rank is false. Over `F_191`, with `r=1`, take

```text
nodes:   (38,121,64,40,6,74),
tags:    (opposite,opposite,same,opposite,same,same).
```

Their squares

```text
(107,125,85,72,36,128)
```

are distinct. The `6 x 6` matrix (10) has rank five, with kernel vector

```text
(13,183,12,138,71,1)
```

in the column order `(A_0,A_1,C_{-,0},C_{-,1},C_{+,0},C_{+,1})`.

This corrects the unrestricted determinant route. The six tagged nodes are
genuine nodes of the Chebyshev domain, but the kernel vector is not asserted
to reconstruct a terminal locator pair. Hence this example does not refute
a realizable terminal root cap.

## Exact finite certificate

The standalone verifier exhausts the row

```text
(p,M,e) = (191,64,4).
```

It reconstructs every degree-four top support, recovers all strict terminal
pairs, groups them by bottom, and checks the identities (1)-(10). The exact
census is

| quantity | value |
|---|---:|
| strict ordered top pairs | 8832 |
| strict bottoms | 4412 |
| terminal intermediate masks | 4416 |
| singleton bottoms | 4408 |
| two-mask bottoms | 4 |

The four nontrivial fixed-bottom pairs have

```text
binary distances:    {3:2, 5:2},
common-root counts:  {3:2, 5:2},
alternant ranks:     {3:2, 5:2},
A=0 pairs:           0,
B=0 pairs:           0.
```

The distance-three pairs attain `6r-1=5` common roots in the generic
coprime stratum. Thus the proved `B=0` bound is also the observed generic
alternant frontier in this finite row.

## Active boundary

At the active finite row discussed in the threshold ledger,

```text
e = 67448,    r = 16862,    2e = 134896.
```

The required common-root cap is `94191`, equivalently
`d_bin >= 40705`. The `A=0` theorem is stronger than this target. The
`B=0` theorem gives `6r-1=101171`, leaving a deficit of `6980` roots.

Even a hypothetical uniform `6r-1` cap for the generic alternant would give
candidate distance `33725`. The exact Hamming quotient then has floor binary
exponent `61579`, exceeding the mask target exponent `52346` by `9233`.
Therefore neither ambient rank nor ordinary Hamming packing closes the
active row.

The remaining mathematical problem is to classify those alternant rank
drops that also satisfy terminal norm realizability, or to bound each
fixed-bottom terminal code directly. This note proves no `94191` root cap,
no `2^52346` capacity theorem, and no growing counterfamily.

## Reproduction

From the repository root run

```text
python experimental/scripts/verify_primitive_shiftpair_terminal_alternant.py
```

The script uses only the Python standard library and regenerates
`experimental/data/certificates/primitive-shiftpair-terminal-alternant/primitive_shiftpair_terminal_alternant.json`.
