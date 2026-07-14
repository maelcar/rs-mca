# Rank-16 left-kernel / shortened-dual / Forney route cut

**Status:** PROVED route cut, with an exact finite-field certificate.

**Official score:** `0/2`. No official Grand List or Grand MCA statement moves.

## Scope and source credit

This note isolates the exact linear-algebra object behind the rank-16
difference-evaluation matrix. Its new content is deliberately narrow:

1. the natural right-kernel identification with the dual of a quotient of a
   shortened dual code;
2. the natural left-kernel identification with the relation space among the
   shortened pieces;
3. the resulting exact rank, nullity, and defect-`h` formulas;
4. the Forney-index refinement of that same defect; and
5. a source-realized `F_31` Reed--Solomon list attaining `h = 1`.

The audited worktree base is
`origin/main@9262f63cf093a7510a2df435f220390f59e2bcd5`. The following
`origin/main` material is inherited and is not rebranded as new:

- `experimental/notes/l2/affine_section_one_row_rank_reduction.md` supplies
  the deployed rank-16 difference-evaluation matrix, its row-surplus count,
  and the original lower bound `30,961` for the left nullity.
- `experimental/notes/thresholds/projective_line_lift_feasibility_wall.md`
  supplies the global received-word/coset functional and its projective
  hyperplane interpretation. The functional below is its restriction to the
  selected union.
- `experimental/notes/l2/l2_sharp_target_conjecture.md` already supplies the
  generic bounded locator-syzygy presentation for selected vanishing spaces.
  The locator map itself is therefore prior project material. What is added
  here is its exact identification with both kernels in this selected-list
  matrix, the exact defect `h`, the minimal-index formulas, and the sharp
  source-realized endpoint.

No pending PR statement and no stable-paper TeX claim is used as proof
authority.

## Exact hypotheses

Let `F` be a field and let `H subset F` be a set of `n` distinct evaluation
points. Fix integers

```text
t >= 2,
1 <= K <= m <= n,
sigma = m-K.
```

Let

```text
C = RS[F,H,K]
```

be the evaluation code of polynomials of degree less than `K`. Let
`u : H -> F` be one received word. Suppose that

```text
P_0,...,P_{t-1} in F[X]_<K
```

are pairwise distinct and that `S_0,...,S_{t-1}` are pairwise distinct
supports satisfying, for every `i`,

```text
S_i subset H,
|S_i| = m,
S_i subset {x in H : P_i(x)=u(x)}.                       (1)
```

The common received word in (1) is essential for the conclusion `h >= 1`.
The kernel identifications and rank identities need only the selected-support
data; they do not manufacture the nonzero syndrome without (1). Pairwise
distinctness of the `S_i` also follows from the other hypotheses: if
`S_i=S_j`, then `P_i-P_j` has at least `m>=K` roots despite having degree less
than `K`.

Put

```text
U = union_i S_i,
|U| = m+e,
e = |U|-m.
```

For `x in U`, let `I_x={i:x in S_i}`. Choose and orient an arbitrary spanning
tree `T_x` on `I_x`. Anchor `q_0=0`; the column variables are

```text
(q_1,...,q_{t-1}) in (F[X]_<K)^(t-1).
```

For every oriented edge `(i,j)` of `T_x`, the corresponding row of `M`
evaluates

```text
q_i(x)-q_j(x).                                           (2)
```

Let

```text
C_U = RS[F,U,K],
V_U = C_U^perp,
W_i = {z in V_U : supp(z) subset S_i},
W   = sum_i W_i,
h   = dim(V_U)-dim(W).                                   (3)
```

## The exact collapse theorem

Under the hypotheses above,

```text
#rows(M)
  = sum_{x in U} (|I_x|-1)
  = tm-|U|
  = (t-1)K+(t-1)sigma-e.                                (4)
```

Relative to the chosen anchor and local trees, there are natural linear
isomorphisms

```text
ker(M)   ~= (V_U/W)^*,                                   (5)
ker(M^T) ~= ker(direct_sum_i W_i -> V_U),                 (6)
```

where the map in (6) sums the components. Consequently,

```text
dim ker(M)   = h,
rank(M)      = (t-1)K-h,
dim ker(M^T) = (t-1)sigma-e+h.                           (7)
```

The received-word premise (1) supplies a nonzero common syndrome in
`(V_U/W)^*`, and therefore

```text
h >= 1.                                                  (8)
```

Moreover, for `i != j`,

```text
W_i intersect W_j = {0}.                                 (9)
```

Thus the left kernel consists of higher-order relations among the shortened
pieces, not pairwise intersections.

## Proof of the kernel identifications

### Row count

The tree at `x` has `|I_x|-1` edges. Since every selected support has size
`m`,

```text
sum_x (|I_x|-1)
  = sum_x |I_x|-|U|
  = sum_i |S_i|-|U|
  = tm-(m+e),
```

which is (4) after using `m=K+sigma`.

### Right kernel

Take `q in ker(M)` and keep the anchor `q_0=0`. Tree connectivity in (2)
implies that all values `q_i(x)`, `i in I_x`, are equal. Define `a in F^U`
to be this common value. On `S_0`, `a=0`.

If `z in W_i`, then `z` is supported on `S_i` and `a|S_i` is the evaluation
of `q_i`. Hence

```text
<a,z> = <q_i,z> = 0.
```

The perfect pairing

```text
F^U/C_U ~= V_U^*
```

therefore sends `a` to a functional annihilating `W`, namely an element of
`(V_U/W)^*`.

This map is injective. If its value is zero, then `a` is the evaluation of a
polynomial `Q` of degree less than `K`. Since `a=0` on the `m>=K` points of
`S_0`, `Q=0` and `a=0`. Each `q_i` then vanishes on `S_i`, again on at least
`K` points, so every `q_i=0`.

For surjectivity, represent a functional in `(V_U/W)^*` by `a in F^U`.
Annihilation of `W_i` says that `a|S_i` lies in the orthogonal complement of
the shortening of `V_U` to `S_i`. Shortening/puncturing duality identifies
this orthogonal complement with `C_U|S_i`. Since `|S_i|=m>=K`, there is a
unique polynomial `Q_i in F[X]_<K` whose evaluation on `S_i` is `a|S_i`.
Replace `a` by the equivalent representative `a-Q_0|U` and set
`q_i=Q_i-Q_0`. On every overlap, `q_i` and `q_j` equal the new representative
`a`, so all tree rows vanish. This proves (5).

### The common syndrome and `h >= 1`

Define

```text
phi_u(z) = sum_{x in U} u(x) z_x,        z in V_U.       (10)
```

For `z in W_i`, (1) gives

```text
phi_u(z) = sum_{x in S_i} P_i(x)z_x = 0,
```

so `phi_u` annihilates `W`. It is nonzero on `V_U`. Otherwise
`u|U in V_U^perp=C_U`, so some `Q in F[X]_<K` equals `u` on `U`. Then `Q`
and every `P_i` agree on the `m>=K` points of `S_i`, forcing
`Q=P_i` for every `i`. This contradicts the pairwise distinctness of the
`P_i`. Thus `phi_u` is a nonzero element of `(V_U/W)^*`, proving (8).

This is precisely the selected-union restriction of the global coset
functional already present in the projective-line lift note. It is not a
second, independent obstruction.

### Left kernel

At each coordinate `x`, take the signed incidence divergence of coefficients
on the oriented tree `T_x`. Tree incidence is an isomorphism from its edge
space to

```text
{(c_i)_{i in I_x} : sum_i c_i=0}.                        (11)
```

For a global row-coefficient vector `lambda`, let `z_i(x)` be the divergence
at vertex `i`. Then `supp(z_i) subset S_i` and `sum_i z_i=0`. The equation
`M^T lambda=0` says, for each `i>=1` and `0<=d<K`,

```text
sum_{x in U} z_i(x)x^d=0.
```

Hence `z_i in V_U` for `i>=1`; the zero-sum relation gives the same conclusion
for `z_0`. Thus `z_i in W_i` and `(z_i)_i` lies in the kernel of the sum map
in (6).

Conversely, any tuple `z_i in W_i` with `sum_i z_i=0` gives a zero-sum
divergence vector at every coordinate. The local tree isomorphism (11)
recovers unique edge coefficients. This proves (6).

Since puncturing `C_U` to any `S_i` has dimension `K`,

```text
dim W_i = m-K = sigma,
dim V_U = |U|-K = e+sigma.
```

The image of the sum map is `W`, so (3), rank-nullity, and (4) give all three
identities in (7).

Finally, if `i!=j`, then `P_i-P_j` vanishes on `S_i intersect S_j`; because
the polynomial is nonzero of degree less than `K`, that intersection has size
at most `K-1`. A nonzero word of the dual MDS code `V_U` has weight at least
`K+1`. A word in `W_i intersect W_j` would be supported on at most `K-1`
coordinates and must therefore vanish. This proves (9).

## Locator-syzygy and minimal-index refinement

Put

```text
Lambda_U(X) = product_{x in U} (X-x),
lambda_x    = 1/Lambda_U'(x),
E_i(X)      = product_{x in U\S_i} (X-x).
```

Every `E_i` is monic of degree `e`. Lagrange duality gives

```text
V_U = {(lambda_x R(x))_{x in U} : deg R < e+sigma},      (12)
W_i = {(lambda_x E_i(x)A(x))_{x in U} : deg A < sigma}.  (13)
```

Because `U=union_i S_i`, no point of `U` lies in every complement
`U\S_i`. The split polynomials therefore satisfy

```text
gcd(E_0,...,E_{t-1})=1.                                  (14)
```

Equations (6), (12), and (13) identify the left kernel with the bounded
locator-syzygy space

```text
ker(M^T) ~= {
  (A_0,...,A_{t-1}) :
  deg A_i < sigma and sum_i E_i A_i = 0
}.                                                       (15)
```

Indeed, the corresponding dual words sum to zero exactly when
`sum_i E_i(x)A_i(x)=0` on `U`. This polynomial has degree at most
`e+sigma-1`, whereas `|U|=K+e+sigma` and `K>=1`, so vanishing on `U` makes it
the zero polynomial.

For `D>=0`, define the truncated Macaulay map

```text
Theta_D : direct_sum_i F[X]_<D -> F[X]_<e+D,
Theta_D((A_i)_i) = sum_i E_i A_i.                        (16)
```

Let `B_1,...,B_{t-1}` be a row-reduced basis of
`Syz(E_0,...,E_{t-1})`, and let `mu_1,...,mu_{t-1}` be its vector degrees,
the Forney indices. Then

```text
sum_j mu_j = e,                                          (17)
dim ker(M^T) = sum_j max(0,sigma-mu_j),                  (18)
h = sum_j max(0,mu_j-sigma).                             (19)
```

To prove (17), the predictable-degree property gives

```text
dim ker(Theta_D) = sum_j max(0,D-mu_j).                  (20)
```

For all sufficiently large `D`, (14) makes `Theta_D` surjective. Divide a
target polynomial by monic `E_0`; its quotient has degree less than `D`, and
its remainder has degree less than `e`. Fixed Bezout representations of
`1,X,...,X^(e-1)` handle every such remainder once `D` exceeds the finitely
many coefficient degrees in those representations. Therefore, for large
`D`,

```text
dim ker(Theta_D)=tD-(e+D)=(t-1)D-e.
```

Comparing with (20) proves (17). At `D=sigma`, (15) and (20) give (18).
The image of `Theta_sigma` corresponds to `W`, so

```text
h=(e+sigma)-rank(Theta_sigma).
```

Substituting (17) and (18), then separating positive and negative parts of
`mu_j-sigma`, proves (19). In particular, the received-word syndrome (8)
forces at least one

```text
mu_j >= sigma+1.                                         (21)
```

## Deployed rank-16 consequence

For the deployed parameters

```text
n     = 2,097,152,
K     = 1,048,576,
m     = 1,116,047,
sigma = 67,471,
n-m   = 981,105,
t     = 16,
```

one has `e<=n-m`. Hence every selected affine 16-basis satisfying the common
received-word premise emits

```text
dim ker(M^T)
  = 15 sigma-e+h
  >= 15(67,471)-981,105+1
  = 30,961.                                               (22)
```

The lower bound decomposes exactly as

```text
30,961 = 30,960 row-surplus dimensions
           + 1 common-syndrome dimension.
```

For a full union `U=H`, the matrix has

```text
15,759,600 rows,
15,728,640 columns.
```

If additionally `h=1`, then its rank is `15,728,639` and its left nullity is
exactly `30,961`. Equation (21) only forces `max_j mu_j>=67,472`. This note
does not prove that a deployed source-selected tuple with `U=H` and `h=1`
exists.

## Sharp source-realized `F_31` fixture

Take

```text
F = F_31,
H = F_31^*,
K = 15,
m = 16,
sigma = 1,
u(x)=x^16.
```

For every 16-subset `S subset H` with `sum_{s in S}s=0`, define

```text
Q_S(X)=product_{s in S}(X-s),
P_S(X)=X^16-Q_S(X).
```

The leading terms cancel, and the `X^15` coefficient of `Q_S` is `-sum S=0`,
so `deg P_S<15`. Moreover,

```text
u(x)-P_S(x)=Q_S(x),
```

so the exact agreement support of `P_S` is `S`.

Conversely, let `P in F_31[X]_<15` agree with `x^16` on at least 16 points of
`H`, and put

```text
D_P(X)=X^16-P(X).
```

Then `D_P` is monic of degree 16 and its `X^15` coefficient is zero. Its roots
in `H` are exactly the agreement points of `P`. Since a nonzero degree-16
polynomial has at most 16 roots, there are exactly 16 such points; call their
unique set `S`. Monicity and the complete set of 16 roots give

```text
D_P(X)=product_{s in S}(X-s).
```

Vieta's formula now gives

```text
0 = coefficient of X^15 in D_P = -sum_{s in S}s,
```

so `sum S=0` and `P=P_S`. Thus `S |-> P_S` is a bijection from the zero-sum
16-subsets of `F_31^*` to the complete agreement-16 list around `x^16`; the
list count below is exact, not merely a constructed sublist.

For completeness, let `psi` range over the 31 additive characters of `F_31`.
The zero-sum filter is

```text
#{S subset F_31^* : |S|=16, sum S=0}
  = (1/31) sum_psi [z^16]
      product_{x in F_31^*}(1+z psi(x)).
```

For every nontrivial `psi`, its values on `F_31` are all 31st roots of unity,
and hence

```text
product_{x in F_31^*}(1+z psi(x))
  = (1+z^31)/(1+z)
  = 1-z+z^2-...+z^30.                                   (23)
```

The coefficient of `z^16` in (23) is `+1`. For the trivial character the
same coefficient is `binom(30,16)`. Character orthogonality therefore gives
the exact full list size

```text
(binom(30,16)+30)/31
  = (145,422,675+30)/31
  = 4,691,055.                                           (24)
```

The explicit 16 supports are pinned in
`experimental/data/certificates/rank16-left-kernel-forney/f31_fixture.json`.
They cover all 30 coordinates. For rows indexed by `P_i-P_0` and columns in
coefficient order `1,X,...,X^14`, the affine-difference matrix has

```text
rank = 15,
determinant = 2 mod 31.                                  (25)
```

Thus these are 16 affinely independent polynomials in the literal list. Their
complement locators span a 14-dimensional space, so

```text
e=14,
dim V_U=15,
h=15-14=1.                                               (26)
```

Using at each coordinate the star rooted at the least support index, the
difference-evaluation matrix has

```text
226 rows,
225 columns,
rank 224,
right nullity 1,
left nullity 2.                                          (27)
```

The truncated Macaulay ranks and nullities are

```text
D    rank(Theta_D)    nullity(Theta_D)
1          14                 2
2          16                16
3          17                31
```

Successive nullity differences force exactly two indices `0`, twelve indices
`1`, and one index `2`:

```text
(mu_1,...,mu_15) = (0,0,1 x 12,2).                       (28)
```

Hence `sum_j max(0,mu_j-1)=1`, exactly as (19) requires. This is an actual
Reed--Solomon list, not an abstract support design. It proves that affine
independence and the selected-support matrix alone cannot force `h>=2`.

## Verifier

The dependency-free verifier is

```text
experimental/scripts/verify_rank16_left_kernel_forney_route_cut.py
```

It reads the pinned JSON fixture and independently checks:

- all field, support-size, zero-sum, union, and exact-agreement conditions;
- the full list count (24);
- the affine rank and determinant (25);
- the restricted common syndrome and every shortened-dual orthogonality test;
- the complement-locator span and `h=1` in (26);
- all entries and the rank/nullities of the `226 x 225` matrix in (27);
- the Macaulay ranks and the inferred Forney profile (28);
- the deployed arithmetic in (22); and
- three in-memory tamper rejections.

It contains no `assert` statement. Its successful transcript is pinned at

```text
experimental/data/certificates/rank16-left-kernel-forney/verifier_output.txt
```

and is required to be byte-identical under normal and optimized Python.

## Ledger impact

The exact high-rank ledger is refined from

```text
rank(M) <= (t-1)K-1
```

to

```text
rank(M)      = (t-1)K-h,
dim ker(M^T) = (t-1)sigma-e+h,
h            = sum_j max(0,mu_j-sigma),
h >= 1.
```

The `F_31` fixture shows that the endpoint `h=1` is sharp for a literal
source-realized Reed--Solomon list. Future progress must classify or count the
minimal-excess `h=1` stratum globally, or exploit genuinely larger `h`; it
cannot charge one independent extra dependency to every affine basis.

## Explicit nonclaims

- No deployed ceiling `L_p^*(1,116,047) <= T` is proved.
- No deployed received word with list size greater than `T` is constructed.
- The `F_31` fixture is not a counterexample to the deployed statement.
- No theorem here forces `h>=2`; the fixture proves that field-uniform claim
  false under the stated local hypotheses.
- No affine-rank interval, rank-15 recurrence state, or finite ledger row is
  paid.
- No upper bound on the number of high-rank listed polynomials is proved.
- Local syndrome defects from different affine bases are not claimed to be
  independent.
- No global projective-line lift, Krawtchouk inequality, asymptotic list bound,
  or uniform `B_L` is proved.
- No Grand MCA denominator, ownership, signed/Sidon, residual-ray, or profile
  cell moves.
- The Lean companion contains scaffold definitions and exact certificate data
  contracts only. It does not prove source selection, deployed fixture
  existence, a kernel/Forney formula, or any theorem in this note.
- No stable-paper TeX is changed.
- The official score remains exactly `0/2`.
