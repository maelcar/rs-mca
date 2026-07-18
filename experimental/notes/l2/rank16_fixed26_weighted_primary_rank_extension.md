# Fixed-26 weighted-primary rank extension

**Claim layer:** conditional local theorem in one deployed fixed-26 source
cell. Under the inherited 64-step collapse and the existence of one actual
source-valid edge, spectral ranks 65 and 66 are impossible. Together with the
integrated rank-gap theorem, the exact local wall is

```text
nu in {3,...,17} or nu >= 67.
```

The same hypotheses give an exact split-complement transform and the
per-fibre residual cap `28,897`.

**Status:** proved after an external hostile audit narrowed the author's
repaired statement and fixed the source normalization. This is a local,
conditional theorem with zero parent, finite-ledger, asymptotic, Grand List,
Grand MCA, or official-score payment. The official score remains `0/2`.

## Fixed source cell

Work over `F = F_p` with

```text
p = 2,130,706,433,  n = 2,097,152 = 64 B,
B = 32,768,         a = 67,472,
r = 63,601,         delta = a-r = 3,871,
d = B-delta = 28,897.
```

Fix one literal source cell from the divided-difference compiler:

* one canonical received word and its actual canonical first-match owner;
* one monic degree-`a` polynomial `g` with `gcd(g,X^n-1)=1`;
* one chosen representative of a nonzero projective residue ray;
* one 26-label core `C` in `Omega = mu_64`.

No squarefreeness assumption is made on `g`. Put

```text
A = F[X]/(g),  T = [X^B],
W = [xi] (T^64-1)^(-1),
```

and let `w(X)` be the canonical representative of `W`, of degree below `a`.
Assume the inherited collapse

```text
deg rem_g(w X^(Bj)) <= r,  0 <= j <= 63.              (G64)
```

Assume the same fixed cell contains an actual valid edge `e={y,z}`. Validity
retains exact degree and monic normalization, squarefreeness and complete
splitting over `H=mu_n`, selected-fibre avoidance, no additional complete
q64 fibre, footprint at least four, nonpairing, every earlier-owner
exclusion, and the actual canonical first-match test.

Let `c_y,c_z` be the compiler boundary coefficients. Exact degree gives
`c_y != c_z`; the source orientation used below is

```text
q_e = (y-z)/(c_y-c_z).
```

Set

```text
h_e(Z) = (Z^64-1)/((Z-y)(Z-z)),
H_e(X) = h_e(X^B) = (X^n-1)/(F_y F_z),
U_e = rem_g(w H_e),
R_e = q_e U_e.
```

Validity makes `R_e` the monic, squarefree, `H`-split residual locator of
degree `r`, and `R_e` divides `H_e`. Define

```text
L_e = H_e/R_e,  deg L_e = 62B-r = 1,968,015.
```

Let `mu_g` be the minimal polynomial of `T` in `A`, and put
`nu = deg mu_g`.

## Theorem

Under the fixed-cell hypotheses above:

1. For every `1 <= k <= min(63,nu-1)`,

   ```text
   k a <= nu r.                                        (1)
   ```

   Hence `nu` lies in `{3,...,17}` or is at least 67. Relative to the
   integrated exclusion `18 <= nu <= 64`, the strict new exclusions are
   `nu=65,66`.

2. For every field extension `K/F` and every `P in K[Z]` of degree at most
   63, if

   ```text
   f_P = rem_(g,K)(w P(X^B)),
   ```

   then `deg f_P <= r` and there is an exact identity in `K[X]`

   ```text
   P(X^B) = q_e f_P L_e + g C_P,                       (2)
   ```

   with

   ```text
   deg C_P <= max(B deg P, 62B)-a.                    (3)
   ```

3. For every `u in Omega\{y,z}`, put

   ```text
   R_(e,u) = gcd(R_e,F_u),  L_(e,u) = F_u/R_(e,u).
   ```

   Then

   ```text
   deg R_(e,u) <= d = 28,897.                         (4)
   ```

## Proof of the weighted-primary inequality

The valid edge makes `W` a unit in `A`. Indeed, the compiler relation gives
`F_y F_z U_e = xi` in `A`. The factors `F_y`, `F_z`, and the valid locator
`R_e` have roots only in `H`, whereas `gcd(g,X^n-1)=1`; they are therefore
units modulo `g`. Since `q_e` is nonzero and `R_e=q_eU_e`, `xi` is a unit,
and so is `W=xi(T^64-1)^(-1)`.

Extend scalars to an algebraic closure. Write

```text
g = X^m0 product_(beta != 0) (X-beta)^m_beta.
```

For a nonzero value `lambda`, the exponent of `Z-lambda` in `mu_g` is
the largest `m_beta` among roots satisfying `beta^B=lambda`; this uses
`p` not dividing `B`. Its primary layers have weights

```text
s_(lambda,t) = #{beta : beta^B=lambda and m_beta >= t}.
```

The zero primary has `ceil(m0/B)` layers, of weights `B` except possibly the
last, whose weight is the remaining positive part of `m0`. Across all
primaries there are exactly `nu` positive layers and their total weight is
`a`.

Choose the `k` heaviest layers, breaking ties so each chosen set is a prefix
inside its primary chain. If `k_lambda` layers are selected in the
`lambda`-chain, define

```text
P_k(Z) = product_lambda (Z-lambda)^k_lambda.
```

Then `deg P_k=k<nu`, so `P_k(T)` is nonzero. Since `W` is a unit,
`W P_k(T)` is nonzero. By (G64) and `k<=63`, its canonical remainder `f_k`
is nonzero and has degree at most `r`.

The gcd `gcd(g,f_k)` has degree exactly the total selected layer mass `S_k`:
at a nonzero root the multiplicity is `min(m_beta,k_lambda)`, while at zero
it is `min(m0,Bk_0)`. Thus

```text
S_k <= deg f_k <= r.
```

The `k` largest of `nu` positive weights of total `a` have mass at least
`ka/nu`. This proves (1).

For `nu<=64`, take `k=nu-1`. Inequality (1) becomes `nu*delta<=a`, which
forces `nu<=17` because

```text
17*delta = 65,807 <= 67,472 < 69,678 = 18*delta.
```

For `nu>=65`, take `k=63`. The deployed margins are

```text
63a - 65r = 116,671,
63a - 66r =  53,070,
67r - 63a =  10,531.
```

Thus ranks 65 and 66 are excluded, while this argument stops at rank 67.

## Proof of the transform and fibre cap

From `H_e=R_eL_e`, `U_e = wH_e` in `A`, and `R_e=q_eU_e`, cancellation of
the unit `R_e` gives

```text
q_e w L_e = 1 in A.                                  (5)
```

For `f_P = rem_(g,K)(wP(X^B))`, (5) gives (2). The product `f_PL_e` has
degree at most `62B`, so division by the monic degree-`a` polynomial `g`
gives (3).

For `u` outside the selected endpoints, use the Lagrange selector

```text
E_(e,u)(Z) = h_e(Z)/((Z-u)h_e'(u)),
```

which has degree 61, equals one at `u`, and vanishes at the other roots of
`h_e`. Apply (2) with this selector. Squarefreeness gives

```text
C_(e,u) = (L_e/L_(e,u)) D_(e,u),
```

where `D_(e,u)` is nonzero and coprime to `L_(e,u)`. The degree bound (3)
then yields

```text
deg D_(e,u) <= deg L_(e,u)-delta.
```

Consequently `deg L_(e,u)>=delta`, and (4) follows from
`deg F_u=B`.

## Audit and replay scope

The frozen independent hostile audit accepted the theorem above after fixing
the displayed normalization and independently deriving every load-bearing
step. Its packet and final-answer hashes are

```text
packet: cda4bec0138629df50655c70a23aa18e7c2816c768c55b1c1bc1268d2ac2f122
final:  2622e26e20a142b972c7fe16b757f33824401aea17180d49c270dcffdff4339b
```

The audit also independently replayed the four inherited standard-library
verifiers in normal and optimized modes. The new verifier accompanying this
note checks the deployed arithmetic, source hashes, exact boundary sweep, and
semantic mutations. It does not claim to mechanically prove the universal
primary-layer argument.

## Exact remaining wall

This theorem does not prove that a valid edge exists and does not convert the
per-fibre cap into an edge count. The fixed-26 cell still needs a theorem for
`nu in {3,...,17}` or `nu>=67`, followed by a source-valid aggregation and
owner/add-back argument. No rank-16 parent or recurrence is paid.

## Nonclaims

This note does not claim:

* exclusion of ranks 3 through 17 or any rank at least 67;
* existence or construction of a valid edge or received-word witness;
* a 117-edge contradiction, cap 116, seven-star exclusion, or cross-minor;
* conversion of the per-fibre cap into an edge count;
* ownership, marked-incidence, occupied-key, or first-match aggregation;
* a complement cap of three, rank-16 parent closure, or recurrence payment;
* any finite or asymptotic ledger payment;
* Grand List, Grand MCA, or an official score change.
