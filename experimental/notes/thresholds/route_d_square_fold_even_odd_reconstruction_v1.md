# Route-D square-fold even/odd reconstruction v1

STATUS: COUNTEREXAMPLE

## Result

For the square fold `x -> x^2`, odd signed fiber data does not recover a full
raw signed defect, even when the literal common core and a nonzero toy pivot
label are carried. The missing information is the even occupancy difference.
This packet proves both sides of that boundary:

```text
SQUARE_FOLD_ODD_DATA_RECOVERY_NO_GO,
MARKED_SQUARE_FOLD_EVEN_ODD_RECONSTRUCTION.
```

The counterexample is an exact three-member subfamily of the fixed-target
`F_23` Rule-2 census at commit
`f23a3b78a6bbe1d50a81b3976f92aa7c135ab300`. All three defects have fixed
literal `G={10}`, target `beta_1=10`, cell `c=17`, representative
`(A_0,R_0)=({2,7},{4,5})`, exact gcd `H=1`, the same nonzero odd signed fold,
the same nonzero toy pivot `6`, support `8`, and `mu_3=1`.

They are three distinct projectively primitive, nonextension full raw defects.
Their even occupancy folds are different, so odd signed data plus the pivot is
not a recovery key. Support `8` is a full raw stratum because `8 >= r+3=5`;
it is not called deployed-scale "large". The literal core is never inferred
from the defect and remains part of the marked recovery data throughout.

## 1. Exact square-fiber equations

Let `F` have odd characteristic and let `D subset F^*` be stable under
negation. For each square-fiber image `y`, choose one root `x_y`; the fiber is
`{x_y,-x_y}`. For two supports `S,T subset D`, define

```text
u_y
 = (1_S(x_y)+1_S(-x_y))-(1_T(x_y)+1_T(-x_y)),

sigma_y
 = (1_S(x_y)-1_S(-x_y))-(1_T(x_y)-1_T(-x_y)).
```

For `mu=1_S-1_T`, direct addition and subtraction give

```text
mu(x_y)  =(u_y+sigma_y)/2,
mu(-x_y) =(u_y-sigma_y)/2.                         (SF1)
```

Consequently

```text
mu_(2a)   =sum_y u_y y^a,
mu_(2a+1) =sum_y sigma_y x_y y^a.                  (SF2)
```

Changing the chosen root negates `sigma_y` and `x_y` simultaneously, so the
odd moment in `(SF2)` is orientation-independent. For Boolean supports,
`u_y +/- sigma_y` is even and belongs to `{-2,0,2}`.

**Theorem (MARKED_SQUARE_FOLD_EVEN_ODD_RECONSTRUCTION).** If the literal
common core `G=S intersect T` is carried, then `(G,(u_y),(sigma_y))`
reconstructs the marked pair `(S,T)`: recover `mu` by `(SF1)`, put every
coefficient `+1` into `S minus G` and every coefficient `-1` into `T minus G`,
then adjoin `G` to both sides.

Without `G`, `(u,sigma)` recovers only the defect because common-core
additions disappear. Without `u`, the antipodally even component disappears.
The counterexample keeps `G` fixed, so it isolates the second failure. This is
an exact reconstruction theorem, not a low-moment payment.

## 2. SHA-pinned F23 source

The fixed-target precursor is commit
`f23a3b78a6bbe1d50a81b3976f92aa7c135ab300`:

- note blob `5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b`;
- verifier blob `678463a3a188ecdb07c7bd7cd6f66401895d0eeb`;
- Lean blob `c9f2f4cecd1e8aeff18aa9fc041ecdcad66c56e0`.

It works over `F=F_23`, `D=F_23^*`, `r=2`, `beta_1=10`, and `c=17`.
There are `75` Rule-1-deduplicated packets. With canonical representative
`G_0={1}`, `A_0={2,7}`, `R_0={4,5}`, exactly `56` comparisons have `H=1`;
one is an extension, leaving `55` distinct primitive nonextension off-core
weights. The verifier rebuilds that census and reproduces its retained-row
digest

```text
de477753d921638e65fdbd346e6f4a7359afb51760ce32c82861bb3173ad0ce2.
```

## 3. Three-member odd-data collision

For deterministic orientation in `F_23`, choose the smaller integer root of
each pair `{x,23-x}`. The unique nonsingleton `(G,sigma,pivot)` fiber has size
three and key

```text
G={10},
sigma={(2,-1),(3,1),(4,1),(16,-1)},
pivot=6.
```

Its packets are

```text
A={1,22}, R={8,15},  U=X^2+22,
A={8,15}, R={9,14},  U=X^2+5,
A={9,14}, R={11,12}, U=X^2+11.
```

Every contact profile is `(0,0)`, so `mu=lambda` and literal `G={10}` is
disjoint from every defect. Each defect has support `8`, trivial scalar/sign
stabilizer, and `mu_3=1`. The common odd data is nonzero. The distinct even
occupancy vectors are

```text
{(1,-2),(2,-1),(3,1),(4,1),(16,-1),(18,2)},
{(2,-1),(3,1),(4,1),(12,2),(16,-1),(18,-2)},
{(2,-1),(3,1),(4,1),(6,2),(12,-2),(16,-1)}.
```

Each varying packet side is an antipodal pair, so its contribution is even
under negation. The fixed representative supplies the common nonzero odd
part. This does not use a zero-defect or zero-odd-data degeneration.

For the odd data the chosen roots are `x_2=5`, `x_3=7`, `x_4=2`, `x_16=4`,
and hence

```text
sum sigma_y x_y=0,
sum sigma_y x_y y=1 mod 23.
```

Every even vector satisfies `sum u_y=0` and `sum u_y y=0 mod 23`. Thus the
three defects share the available degree-two equations and the same nonzero
next odd moment while remaining distinct. The family JSON digest is

```text
0b95b519f541e314a5809cea782afaad97126c2a9f44ca1de21ec5c5c2da52b7.
```

## 4. Complete folded census

Across all `55` precursor rows:

```text
distinct sigma                       52,
distinct (G,sigma)                   52,
distinct (G,sigma,pivot)             53,
distinct (G,u,sigma)                 55,
(G,sigma,pivot) fiber histogram      {1:52,3:1},
vanishing toy pivots                   0.
```

The digest of the complete folded records is

```text
f6ac27af0adff1a4e864c0b565c9e3b3e524c08ab7bfac9ac940e7f1583b8877.
```

The equality `distinct (G,u,sigma)=55`, together with coordinatewise replay
of `(SF1)`, is the finite regression for the positive theorem.

## 5. Pivot and first-match scope

The finite pivot is the lexicographic three-column weighted-Vandermonde
determinant of the off-core defect. It is nonzero for all `55` rows and is a
toy chart label, not the actual marked residual incidence matrix.

The only legal actual rank-drop interface is the all-maximal-minors adapter at
commit `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
`f24ce928df7e7170c1b4f3228d5fe9b184be50b4`. If every maximal minor of a
future actual owner-typed matrix vanishes, route it once while carrying
literal `G`; otherwise a nonzero actual pivot supplies only a chart.

No toy pivot vanishes here, so there is no vanishing family to route. The
named deletion executor remains unavailable at commit
`8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`, note blob
`fdeabf0708cb8806feefae9322ed9002339332cf`. The collision is therefore raw
algebraic, not post-first-match.

## 6. Provenance

- prefix folding target: commit
  `e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
  `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- singleton Rule-2 schema: commit
  `84b393ec1bc52fa662756bd117a45537007d086a`, note blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- marked transfer boundary: commit
  `332153d6e74403e3ad20f367ff4a3df8406a30bf`, note blob
  `6ce5a571ca05f774a6569a9c78d9cb69e8fc896a`;
- marked fold boundary: commit
  `3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835`, note blob
  `13479a4b8de5f495508375a16366b62efe39acab`.

Every imported object is pinned by a full commit or blob SHA.

## 7. Nonclaims

- No unavailable named first-match projector is executed.
- No raw packet is called an admitted post-first-match unit.
- No low-moment, Johnson-packing, mode-at-null, image-only, zero-defect, or
  zero-odd-data shortcut is used.
- No toy pivot is called the actual RIM pivot.
- No vanishing family is left unrouted: the toy vanishing count is zero.
- No deployed-scale large-defect claim is made.
- The literal common core is not erased, shrunk, or reconstructed from the
  defect.
- The deployed primitive support certificate is neither proved nor refuted.

## 8. Reproduction and Lean layer

```bash
python3 experimental/scripts/verify_route_d_square_fold_even_odd_reconstruction_v1.py
python3 -O experimental/scripts/verify_route_d_square_fold_even_odd_reconstruction_v1.py
python3 experimental/scripts/verify_route_d_square_fold_even_odd_reconstruction_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_square_fold_even_odd_reconstruction_v1.py --tamper
(cd experimental/lean/route_d_square_fold_even_odd_reconstruction_v1 && lake build)
```

The standalone Lean module proves the coordinate equations, pins the exact
collision arithmetic, and preserves the legal all-minors guard. The exhaustive
field census remains in the deterministic verifier.
