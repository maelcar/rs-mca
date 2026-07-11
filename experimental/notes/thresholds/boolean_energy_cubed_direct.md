# A self-contained Boolean-energy bound for the primitive-Q compiler

## Status

`PROVED` for finite duplicate-free Boolean families embedded in the
torsion-free group `Z^T`. `CONDITIONAL` only when composed with the
source-specific low-energy/Sidon payment required by A4.

This note supplies an elementary rational-power input for the conditional
`hsharp` interface in `AsymptoticSpine/PrimitiveBoolean.lean`. A stronger
published inequality,

```text
E(F) <= |F|^(log_2 6),
```

is already cited in `lean_frontiers_primitive_boolean.md`. The contribution
here is not a better exponent. It is a short self-contained proof of the exact
integer-power inequality consumed by the existing finite compiler, with a
stdlib-only exact verifier.

## Exact theorem

Let `T` be finite and let `F` be a finite subset of `{0,1}^T`, embedded
coordinatewise in `Z^T`. Define the ordered additive energy

```text
E(F) = |{(a,b,c,d) in F^4 : a-b=c-d in Z^T}|.
```

Then

```text
E(F)^3 <= |F|^8.                                      (BE)
```

Consequently, for nonempty `F`,

```text
Delta(F) := E(F)/|F|^3 <= |F|^(-1/3).                (BE1)
```

In the integer-cleared form used by the Lean compiler,

```text
K E(F) > |F|^3  implies  |F| < K^3.                  (BE2)
```

No fixed-weight or density hypothesis is needed for this theorem.

## Proof

Induct on `|T|`. Split on the last coordinate and write

```text
F_i = {x : (x,i) in F},  n_i=|F_i|,  E_i=E(F_i),  i in {0,1}.
```

For `i,j in {0,1}`, let

```text
r_ij(z) = |{(x,y) in F_i x F_j : x-y=z}|,
C = sum_z r_00(z) r_11(z).
```

The last-coordinate-zero differences contribute `E_0+E_1+2C`. The
last-coordinate `+1` and `-1` differences each contribute `C`: the identity

```text
sum_z r_10(z)^2 = sum_z r_00(z)r_11(z)
```

is the bijective reordering of
`x-y=x'-y'` as `y'-y=x'-x`. Hence

```text
E(F) = E_0 + E_1 + 4C.                               (1)
```

Cauchy-Schwarz gives `C^2 <= E_0 E_1`. By induction,
`E_i <= n_i^(8/3)`, so

```text
E(F) <= n_0^(8/3)+n_1^(8/3)+4(n_0 n_1)^(4/3).       (2)
```

It remains to prove, for `x,y>=0`,

```text
x^(8/3)+y^(8/3)+4(xy)^(4/3) <= (x+y)^(8/3).         (3)
```

Put `x=u^3`, `y=v^3`. With

```text
(c_0,...,c_8)=(8,112,464,976,1169,814,304,56,4),
```

direct expansion gives the exact identity

```text
(u^3+v^3)^8 - (u^8+v^8+4u^4v^4)^3
 = (2u^2+uv+2v^2)
   sum_{j=0}^8 c_j u^(11-j)v^(11-j)(u-v)^(2j).
```

Every term on the right is nonnegative for `u,v>=0`. Taking cube roots
proves (3). Combining (1)--(3) gives `E(F)<=|F|^(8/3)`, hence (BE).
Dividing by `|F|^3` proves (BE1), and (BE2) follows immediately.

## Primitive-Q consequence

Let `Omega` be a nonempty full Boolean profile slice, `Phi:Omega->Sigma` its
actual boundary map, `L=|Phi(Omega)|`, and `barN=|Omega|/L`. For a residual
`O subseteq Omega`, put `F_s=O intersect Phi^-1(s)` and `f_s=|F_s|`.
For fixed `sigma>0`, a fiber outside the low-energy/Sidon class

```text
Delta(F_s) <= exp(-sigma N)
```

has, by (BE1), `f_s < exp(3 sigma N)`. Therefore an image-normalized A4
payment for the low-energy fibers implies

```text
max_s f_s <= exp(o(N)) barN.
```

The argument fixes `sigma`, takes the row limit, and then lets `sigma` tend
to zero. It does not need a moving-cutoff diagonal sequence, BSG, quasicube
growth, or fixed density. This is an analytic implication only: proving the
actual post-atlas A4 low-energy payment remains the source-specific wall.

## Verification

Run

```text
python3 experimental/scripts/verify_boolean_energy_cubed_direct.py
```

The verifier checks the polynomial identity over `Z[u,v]`, exhausts every
Boolean family through dimension four (`65,814` families), and checks 2,000
deterministic random families in dimension five.

## Nonclaims

- This does not improve the sharper published exponent `log_2 6`.
- This does not prove A2, A4, A6/RC, A7, or the unsafe reserve.
- This does not apply to multiplicity-weighted frame energy or repeated
  supports.
- Energy is computed in `Z^T`, not modulo two or in the coefficient field.
- This does not kernel-check a new Lean proof; the current Lean wrapper still
  receives (BE) as an argument.
- No deployed finite row or Grand MCA threshold is closed.

The exact next wall is the image-normalized low-energy/Sidon payment on every
actual post-A2 primitive residual.
