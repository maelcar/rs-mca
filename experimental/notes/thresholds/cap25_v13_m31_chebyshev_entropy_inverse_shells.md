Stacks on PR #434.

# M31 Chebyshev entropy inverse: sublinear exchange shells close the skeleton; primitive-only `PR <= 55` does not survive quotient deletion

Status per claim: `PROVED` (the affine few-shell lemma, its
fixed-profile signed extension, the Chebyshev-prefix specialization, the
mass-aware Renyi consequence, and the exact deployed one-shell cap) /
`PROVED-AT-TOYS` + `COUNTEREXAMPLE` (the exact faithful `p=127,n=32,m=15,w=2`
primitive-participation witness) / `CONJECTURAL` (the unrestricted deployed fiber at
`w=67447`). This is **rung 1**: it proves the Chebyshev-domain entropy-inverse
conclusion in the stated sublinear-shell subregime, at the actual M31 depth,
without claiming the unrestricted row.

Verifier: `experimental/scripts/verify_m31_chebyshev_entropy_inverse_shells.py`
(zero argument, stdlib only). Data:
`experimental/data/cap25_v13_m31_chebyshev_entropy_inverse_shells.json`.

## 1. Result and exact deployed consequence

Let `D` be the Mersenne-31 Chebyshev/twin-coset domain from PR #434, and let

```text
p = 2^31-1 = 2147483647,  n = 2^21 = 2097152,
m = 981129,                w = 67447,
B* = 2^24-1 = 16777215.
```

For a family `F` of `m`-subsets of `D`, its **exchange shells** are the distinct
integers

```text
e(A,B) = |A\B| = m-|A cap B|,       A != B in F.
```

The theorem below proves the entropy-inverse conclusion whenever every residual
prefix fiber uses `s=o(n)` shells. In the finite one-shell case it gives, at the
actual deployed `w`,

```text
max_z |F_z| <= n-w = 2029705 < B* = 16777215,
exact headroom B*-(n-w) = 14747510.
```

Thus a one-shell M31 Chebyshev residual is paid outright. The remaining finite
cell is named `CHEBYSHEV-MULTISHELL-RESIDUAL`; positive-rate asymptotic collision
excess requires the stronger `CHEBYSHEV-MANY-SHELL-RESIDUAL`, with a linear
number of shells.

## 2. Affine few-inner-product lemma  `PROVED`

**Lemma.** Let `p>n`, let `V=a+K` be an affine subspace of `F_p^n` with
`dim K=N`, and let `F` be a fixed-weight family in
`V cap {0,1}^n`. If the off-diagonal intersections

```text
Lambda = {|A cap B| : A,B in F, A != B}
```

take `s=|Lambda|` values, then

```text
|F| <= binom(N+s,s).                                           (2.1)
```

**Proof.** Choose affine coordinates `x(u)=a+Lu`, `u in F_p^N`, on `V`.
For each `A in F`, put

```text
f_A(u) = product_{lambda in Lambda} (1_A . x(u)-lambda).
```

This polynomial has total degree at most `s`. At the coordinate `u_B` of
`B != A`, one factor is `|A cap B|-lambda=0`. At `u_A`, its value is
`product_lambda (m-lambda)`, which is nonzero in `F_p`: every off-diagonal
intersection lies in `[0,m-1]`, and `m<=n<p`. Hence the evaluation matrix
`(f_A(u_B))` is diagonal with nonzero diagonal. The `f_A` are linearly
independent, while the space of total-degree-at-most-`s` polynomials in `N`
variables has dimension `binom(N+s,s)`. This proves (2.1).

The same argument covers the skeleton's signed trades. If
`F subset {-1,0,1}^n` has a fixed `(+,-,0)` profile, then every vector has the
same real norm `a=x.x`. For distinct `x,y`,
`1 <= a-x.y <= 2n`; therefore, when `p>2n`, the diagonal factors remain
nonzero modulo `p`. Thus (2.1) also holds for a fixed-profile signed family
whose off-diagonal dot products take `s` values.

## 3. Chebyshev-prefix specialization  `PROVED`

Use the Chebyshev basis `T_0,...,T_w` on `D`. Each `T_j` has degree `j` and
nonzero leading coefficient (`2^(j-1)` for `j>=1`). Since `D` contains `n>w`
distinct points, a degree-at-most-`w` polynomial vanishing on all of `D` is
zero. The `(w+1) x n` evaluation matrix therefore has rank `w+1`.

A fixed-size prefix fiber is cut out by the weight row `T_0` and the first `w`
moment rows. Its ambient affine kernel consequently has dimension

```text
N = n-w-1.                                                     (3.1)
```

The monomial and Chebyshev descriptions give exactly the same fibers. Indeed,
`(T_0,...,T_w)` and `(1,X,...,X^w)` differ by an invertible triangular change
of basis; the even-degree constant terms are fixed once `|A|=m` is fixed.
The dual Fourier directions are correspondingly bijected, up to unit phases.

Combining (2.1) and (3.1), every possibly pruned Chebyshev prefix fiber using at
most `s` exchange shells satisfies

```text
|F_z| <= A_s := binom(n-w-1+s,s).                              (3.2)
```

For `s=1`, (3.2) is `A_1=n-w=2029705`, giving the exact deployed cap in
section 1.

## 4. Mass-aware entropy-inverse conclusion  `PROVED`

Let `Omega^circ` be any pruned fixed-profile family, let `M=|Omega^circ|`,
let `N_z` be its Chebyshev-prefix fiber sizes, and put `nu(z)=N_z/M`. With the
normalization of `prob:entropy-inverse-q`,

```text
Gamma_l = p^(w(l-1)) sum_z nu(z)^l.
```

If every nonempty residual fiber has at most `s` shells, then (3.2) and
`sum_z nu(z)=1` give the exact inequality

```text
Gamma_l <= (A_s p^w/M)^(l-1).                                 (4.1)
```

This uses the actual residual mass `M`, not the mass of the unpruned slice, so
the caveat in `rem:mass-aware-logmoment` is already paid.

Now suppose `log M-w log p=o(n)` and `s=o(n)`. Since
`log binom(n-w-1+s,s)=o(n)`, (4.1) gives

```text
Gamma_l = exp(o(n) l).
```

Therefore the positive-rate antecedent
`Gamma_l >= exp(eta n l)` of the entropy-inverse skeleton is impossible in
this subregime. Conversely, for fixed `eta>0`, such an excess forces at least
one contributing fiber to have `Omega(n)` distinct exchange shells. This is
the named `CHEBYSHEV-MANY-SHELL-RESIDUAL`. The argument applies before or after
first-match pruning and also to fixed-profile signed trades.

This closes the desired inverse **conclusion** on the few-shell branch; it does
not purport to execute the open entropy-BSG/PFR/slice-derivative steps on the
many-shell branch.

## 5. What a first finite violation must contain  `PROVED`

Two distinct supports in one depth-`w` prefix fiber have exchange size
`e>=w+1`. To see this, cancel their common part. If the two remaining
`e`-sets had `e<=w`, their first `e` power sums would agree. Newton identities
(all denominators are invertible because `e<p`) would give identical locator
polynomials, hence identical sets, a contradiction.

Take any hypothetical M31 fiber larger than `B*` and retain exactly

```text
L = B*+1 = 16777216 = 8n
```

members. Join two members when their exchange size is the minimum `w+1`.
Every clique is a one-shell family and hence has size at most
`r=n-w=2029705`. Turan's theorem applied to the complement gives at least

```text
L = 8r + 539576,
539576*binom(9,2) + (r-539576)*binom(8,2)
  = 61148348
```

unordered pairs with exchange size at least `w+2=67449`. Consequently some
member has at least `8` such higher-shell neighbors. This does not pay the
multishell cell, but it replaces a vague exception with an exact combinatorial
obligation.

## 6. A faithful primitive-`PR` falsifier  `PROVED-AT-TOYS` / `COUNTEREXAMPLE`

The following exhaustive toy narrows what the many-shell theorem may say. Let

```text
p=127, n=32, m=15, w=2,
D=chi(gH union g^-1 H), |H|=32 in the order-128 norm-one torus.
```

Here `g^2 notin H`, `chi` is two-to-one, `D=-D`, and `T_2` is exactly
two-to-one. The exact subset DP finds

```text
C=binom(32,15)=565722720, p^2=16129, floor(C/p^2)=35074;
all 16129 prefix fibers are nonempty;
min N_z=34139, max N_z=36079,
p^2 max(N_z)/C = 581918191/565722720 < 1.03.
```

Thus this is a dense, near-uniform (`avg>>1`) faithful Chebyshev toy, not the
subsampling regime from PR #434's falsification guard.

For a quadratic phase `t_1 x+t_2 x^2`, constancy on `T_2`-fibers is equivalent
to `t_1=0`; these are exactly the quotient directions. Primitive directions
are uniquely `lambda(1,s)`, with `lambda!=0` and `s in F_127`. For each `s`,
let

```text
N_s(u) = #{M subset D: |M|=15,
                    sum_{x in M}(x+s x^2)=u},
Q_s = 127 sum_u N_s(u)^2-C^2.
```

Fourier Parseval says `Q_s=sum_{lambda!=0}|E(lambda,lambda s)|^2`. Hence

```text
A := sum_s floor(sqrt(Q_s)) <= sum_primitive |E(t)|,
Q := sum_s Q_s                  = sum_primitive |E(t)|^2,
PR_primitive >= A^2/Q.
```

The exhaustive integer certificate is

```text
A = 6615676,  Q = 649241132046,
A^2/Q = 21883584468488/324620566023,
A^2-55Q = 8058906674446 > 0.
```

Moreover PR #434's exact reference is

```text
nu*_ref = (14783537/1993678)^2
        = 218552966230369/3974751967684,
```

and exact cross multiplication gives

```text
A^2*3974751967684 - Q*218552966230369
  = 32070065644787419800378610 > 0.
```

So the uniform lemma

```text
delete every Chebyshev-fold direction, then prove PR_primitive <= nu*_ref
```

is false already at this faithful toy. The mechanism is exact: the quotient
line carries

```text
Q_quotient/Q_raw = 28792390764628/29117011330651 > 98/100
```

of the nonzero `L^2` energy. Deleting it removes almost all of the participation
ratio denominator. This does **not** refute the raw signed-`e_m` target, the
few-shell theorem, or an entropy inverse with stratum-specific energy. It says
the many-shell proof must retain cross-stratum energy, renormalize its budget,
or avoid a primitive-only participation ratio.

Two smaller exhaustive gates also replay the shell statistic:

```text
p=31,n=8,m=4,w=2: 69 occupied fibers; the sole collision fiber is (p1,p2)=(0,2), equivalently (T1,T2)=(0,0);
                    it has size 2 and shell set {4}; affine cap 6.
p=127,n=16,m=8,w=1: the z=0 fiber has size 132 and shell set {2,3,4,5,6,8};
                     affine cap binom(20,6)=38760.
```

All exhaustive statements in this section are `PROVED-AT-TOYS`, not general
theorems.

## 7. Ledger impact and nonclaims

The new proved branch is the exact Chebyshev-domain counterpart missing from
PR #434 in the **sublinear exchange-shell** regime. It is basis-faithful,
mass-aware, valid after pruning, and reaches the actual deployed depth. It
turns any remaining positive-rate entropy excess into a named linear-shell
obstruction instead of silently assuming entropy-small doubling.

It does **not** prove `U(1116023)<=B*`, `prob:row-sharp-q`, the unrestricted
M31 signed-`e_m` inverse at `w=67447`, or `PR(Rhat)<=nu*_ref` for the full
spectrum. It also does not claim that every deployed fiber is one-shell or has
`o(n)` shells. Those assertions remain open.

## 8. Reproduce

```text
ulimit -v 2097152; python3 experimental/scripts/verify_m31_chebyshev_entropy_inverse_shells.py
```

The verifier recomputes every integer above, the M31 average ceiling, both
faithful Chebyshev domains, the exact DPs and Parseval split, two shell censuses,
and at least five independent corruption self-tests.
