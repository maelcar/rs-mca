Continues the deployed M31 two-shell wall after the exact Johnson cut and the
anchored Gram cut integrated from PRs #495 and #529.

# M31 rank-inertia anchored cut: 56,059 new two-shell exclusions

**Status:** `PROVED` for the stated two-shell predicate and exact survivor
ledger; `OPEN` for the remaining two-shell rows, all three-or-more-shell
families, the full prefix-fiber bound, and the deployed MCA row.

**Verifier:**
`experimental/scripts/verify_m31_rank_inertia_anchor_cut.py` (zero argument,
stdlib only, exact integer arithmetic).

## 1. Exact result

Use

```text
p = 2^31-1, n = 2^21, m = 981129, w = 67447,
B* = 2^24-1, L = B*+1 = 8n,
R = m(n-m) = 1094962529967.
```

Let `F` be an `L`-member subfamily of one deployed depth-`w` M31 prefix
fiber, including a hereditary first-match residual, and suppose its two
off-diagonal exchange distances are `e1 < e2`.  The integrated two-shell
reduction gives

```text
e1 = (kappa-1)t,  e2 = kappa t,
2 <= kappa <= 774,
ceil(67448/(kappa-1)) <= t
  <= min(floor(981129/kappa), floor(R/(n(kappa-1)))).       (1)
```

Put `lambda = kappa-1`, `q = 7n`, and define

```text
P_kappa(x) = x^2 + (14lambda-8(n-1))x + 7lambda^2(8n-1),

T_kappa(x) = (n-1)^2(q lambda^3+x^3) - (q lambda+x)^3.
```

Let `h2(kappa)` be the first integer on the decreasing side of `P_kappa`
for which `P_kappa(h2) <= 0`, and let `h3(kappa)` be the first integer

```text
h >= ceil(q lambda/(n-2))
```

for which `T_kappa(h) >= 0`.  Set

```text
H_kappa = max(h2(kappa), h3(kappa)).                        (2)
```

Every realization of (1) has a vertex with at least `H_kappa` neighbors at
distance `e2`.  The first values are

```text
kappa:    2       3       128      400       600       774
H:        890     1780    113686   1200745   3077757   8060986
```

For `H = H_kappa`, define

```text
Z = (H(kappa+1)+lambda)R - H n kappa^2 t.                  (3)
```

The rank-inertia predicate `RI(kappa,t)` is:

1. If `H <= n`, then `Z < 0`.
2. If `H > n`, put `d = H-n`.  If `d lambda <= n`, then
   `d lambda^2 R > nZ`.
3. If `H > n` and `d lambda > n`, put

```text
b = 2d lambda-H(n-1),  c = d lambda^2(H-1),
```

and require both

```text
2nZ < -bR,
nZ^2+bZR+cR^2 > 0.                                        (4)
```

Every grid row satisfying `RI` is impossible.  Adding the integrated
degree-two centroid predicate gives the exact ledger

```text
RI rows                                      153483
centroid rows                                   187
overlap                                          65
new union                                     153605
integrated #495/#529 union                    97546
new rows beyond that union                    56059
remaining two-shell rows                    3101280
```

The new union contains the entire exact #495/#529 union.  It also contains
the same-round cubic maximum-degree predicate obtained by combining the
anchored Gram degree cap with the first three traces; that weaker predicate
cuts `108582` rows.

Canonical row hashes, for rows `(kappa,t,e1,e2)` serialized with comma fields
and semicolon separators, are

```text
RI:
f50806d868f320ce8239ea92d466a516253a50089991d862f18f51123e80ebaf

centroid:
358fc8532b53afbdc5cfbdf7b1baa7768cf8cf68f1859147c38cdc0ea2af6564

union:
49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da

new beyond #495/#529:
b207f4a216f3dbe770f2a099e55a3380f8b20acad8a74beaa45b030c027c541c
```

## 2. Rank and inertia force a large anchor shell

Let `A` be the adjacency matrix joining support pairs at distance `e2`.
For each support `S`, center its incidence vector:

```text
y_S = 1_S-(m/n)1.
```

Its Gram matrix `C` is positive semidefinite, has rank at most `n-1`, and

```text
C = (R/n-e1)J + e1 I-tA.
```

Therefore

```text
A-lambda I = (R/(nt)-lambda)J-C/t.                         (5)
```

The grid has `e1 <= R/n`, so (5) has rank at most `n` and at most one
positive eigenvalue.  Hence `A` has at least `L-n = 7n` copies of
`lambda`, and at most one eigenvalue strictly above `lambda`.

Let `rho` be the Perron eigenvalue and write the remaining spectrum as

```text
lambda (7n times), rho, x_1,...,x_(n-1),  x_i <= lambda.
```

The trace and Cauchy-Schwarz give

```text
tr(A^2) >= 7n lambda^2 + rho^2
          +(7n lambda+rho)^2/(n-1).
```

Since `tr(A^2) = L*average_degree <= L rho`, this is exactly
`P_kappa(rho) <= 0`, proving `rho >= h2` at the integer degree level.

For the cubic bound, put `a=(7n lambda+rho)/(n-1)`.  The trace forces
`rho >= a`, and for every `x_i <= lambda < 2a`,

```text
x_i^3 <= 3a^2 x_i+2a^3
```

because the difference is `(2a-x_i)(a+x_i)^2`.  Using
`tr(A^3) >= 0` yields `T_kappa(rho) >= 0`.  The derivative

```text
T'_kappa(x)=3((n-2)x-7n lambda)(nx+7n lambda)
```

is nonnegative on the valid range, proving the `h3` bound and hence (2).

## 3. Recurse inside the large anchor shell

Fix an anchor with an `e2`-neighborhood of size `h >= H`.  Its induced
adjacency matrix `A_H` has

```text
rank(A_H-lambda I) <= n.
```

When `h>n`, put `d=h-n`; then `A_H` has at least `d` copies of `lambda`.
If `a_h` is its average degree, Cauchy-Schwarz gives

```text
a_h >= d lambda^2/n.                                      (6)
```

When `d lambda > n`, separating the Perron eigenvalue and applying
Cauchy-Schwarz to the other `n-1` eigenvalues strengthens (6) to

```text
n a_h^2 + (2d lambda-h(n-1))a_h
  + d lambda^2(h-1) <= 0.                                 (7)
```

Thus `a_h` is at least the lower root of (7).  On that branch implicit
differentiation shows

```text
(lambda-a_h)/h
```

is decreasing in `h`; the same monotonicity is immediate from (6) on the
middle branch and from `a_h >= 0` on the first branch.  It is therefore
sound to evaluate the weakest consequence at `h=H`.

For the anchor-neighbor differences `z_U=1_U-1_anchor`, direct expansion and
centering give

```text
|sum_U z_U|^2 = t h^2(kappa+1+(lambda-a_h)/h),
|sum_U z_U|^2 >= n h^2 kappa^2 t^2/R.                     (8)
```

Combining (6)-(8) at `H` gives exactly the three integer branches (3)-(4).
No regularity, integral Seidel spectrum, modular-to-real transfer, or SDP
optimizer is used.

## 4. Centroid closure

The all-ones quadratic form in `C` gives the exact average-degree cap

```text
average_degree <= U = LR/(nt)-L lambda+lambda.
```

The same second-moment inequality forces

```text
P_kappa(average_degree) <= 0.
```

If `U` is strictly left of the lower root of `P_kappa`, no average degree is
possible.  Cross-multiplying this condition gives the exact 187-row
degree-two centroid set already integrated from #495.  It is included in the
union only to make the new survivor ledger self-contained.

## 5. Validation and scope

Run

```text
python3 experimental/scripts/verify_m31_rank_inertia_anchor_cut.py
```

The verifier regenerates all `3254885` grid rows; computes every `h2`, `h3`,
and `H` by exact integer bisection; replays the Johnson `j<=6` and anchored
Gram predicates at their integrated scope; checks containment of both the old
union and the same-round cubic predicate; verifies all counts, intervals,
hashes, and threshold boundary signs.

This result pays only the listed exact two-shell parameter cells.  It does
not add sizes of cells, exclude the remaining `3101280` two-shell rows, handle
a family with three or more distances, prove a complete first-match upper
ledger, prove `U(a0+1) <= B*`, or solve the deployed M31 row.  It has no
asymptotic effect.

The next exact target is the low-anchor-rank residual: classify or exclude the
remaining two-shell rows using the star-complement structure of
`A-(kappa-1)I`, while retaining the coordinate-labeled M31 prefix equations.
