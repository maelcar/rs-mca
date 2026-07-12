# Projective syndrome descent and proper-field C5 first match

**Status:** `PROVED` for Theorems 1--5 below. Theorem 4 is a coverage and
first-match statement, not a profile-payment certificate. Theorem 5 is a
route cut for coefficientwise Frobenius, not an orbit-divisibility theorem.

**Source interface:** `experimental/asymptotic_rs_mca_frontiers.tex`,
especially `def:exact-witness-incidence`, `def:profile-cell`,
`def:first-match`, `def:primitive-first-match-residual`,
`prop:syndrome-line-normal-form`, and `thm:syndrome-secant-exact`.

## Setup

Let `B subseteq F` be finite fields, let `D subseteq B`, and let

```text
C = RS_F(D,k),        1 <= k < |D|,        k+1 <= a <= |D|.
```

Fix a full-row-rank weighted Vandermonde parity-check matrix `H` for `C`
whose entries lie in `B`. For a received word `u in F^D`, put
`s(u)=H u^T`. Write a received pair as `R=[r_0 r_1]` and set

```text
Y_R = [y_0 y_1] = H R,             W_R = im_F(Y_R) subseteq F^(n-k).
```

A codeword gauge replaces `R` by `R+K`, where both columns of `K` lie in
`C`. A projective reparametrization replaces `R` by `RA` for
`A in GL_2(F)`. Both operations preserve support-wise nontriviality and
transport the exact witness incidence.

For completeness, use the projective completion of the source incidence.
A projective exact-`a` witness is an equivalence class

```text
(u,v,S,h) ~ (lambda*u,lambda*v,S,lambda*h),  lambda in F^x,
```

where `(u,v) != (0,0)`, `|S|=a`, `deg(h)<k`,

```text
ev_S(h) = (u*r_0+v*r_1)|_S,
```

and `r_0,r_1` are not both individually explainable on `S`. Its direction
is `[u:v] in P^1(F)`. Denote the projective witness incidence and direction
set by `W_hat_a(R)` and `Z_hat_a(R)`. The source finite-slope objects are
the chart `u=1`, where `[u:v]=[1:gamma]`.

An `F`-subspace `W subseteq F^N` is *defined over* an intermediate field
`E` if `W=F W_E` for some `E`-subspace `W_E subseteq E^N`.

When `y_1 != 0`, define `F_aff(R)` to be the unique smallest intermediate
field over which the flag

```text
F y_1 subseteq W_R
```

is defined. This is the affine-syndrome flag field, not the raw coordinate
field of a representative. When `y_1=0`, use the source finite-chart
convention `F_aff(R)=B`; projective descent is then read after choosing a
projective chart with nonzero second syndrome.

If `rank(Y_R)=0`, both received words are codewords, so support-wise
nontriviality fails and the exact witness incidence is empty. The descent
statements below therefore concern precisely the positive-rank case.

## Theorem 1 - Intrinsic projective syndrome field

Assume `rank(Y_R)>0`. There is a unique smallest intermediate field

```text
B subseteq F_proj(R) subseteq F
```

over which `W_R` is defined. It depends only on the codeword-gauge and
projective-reparametrization class of `R`.

For every intermediate field `E`, the following are equivalent:

1. `W_R` is defined over `E`.
2. There are `A in GL_2(F)` and a codeword gauge `K` such that
   `RA+K in (E^D)^2`.
3. There is `A in GL_2(F)` whose second transformed syndrome is nonzero and
   for which `F_aff(RA) subseteq E`.

Thus `F_proj(R)` is exactly the smallest coefficient field of a received-pair
representative after codeword gauge and projective slope reparametrization.
Equivalently, it is the smallest affine-syndrome flag field obtained after a
projective reparametrization with nonzero second syndrome. In particular,

```text
F_proj(R) subseteq F_aff(R)
```

whenever the displayed affine field is attached to a nonzero second syndrome.

### Proof

Let `M_R` be the unique reduced-row-echelon matrix whose row space consists
of the transposes of the vectors in `W_R`. The subspace is defined over `E`
if and only if every entry of `M_R` lies in `E`: an `E`-basis row-reduces
over `E`, and uniqueness of reduced row-echelon form gives the converse.
Hence the field generated over `B` by the entries of `M_R` is the unique
smallest field of definition. This defines `F_proj(R)` intrinsically.

Suppose `W_R` is defined over `E`, and choose an `E`-basis of it. If
`rank(Y_R)=2`, a matrix `A in GL_2(F)` changes the two syndrome columns into
that basis. If `rank(Y_R)=1`, choose a nonzero `z in E^(n-k)` spanning
`W_R`; an invertible column operation changes the syndrome matrix to
`[0 z]`. In both cases the columns can therefore be chosen with nonzero
second syndrome and with an `E`-defined flag.

Because `H` has full row rank over `B`, it has a `B`-linear right inverse
`J`. Applying `J` to the normalized syndrome columns gives an `E`-valued
pair `Q in (E^D)^2` with the same syndrome as `RA`. Therefore `RA-Q` has
both columns in `ker(H)=C`, proving (2).

Conversely, if `RA+K` is `E`-valued, its syndrome columns are `E`-valued
and span `W_R`, since gauges do not change syndromes and `A` is invertible.
Thus `W_R` is defined over `E`. An `E`-defined transformed flag also has an
`E`-defined ambient syndrome subspace, so (3) implies (1). Gauge leaves
`W_R` unchanged and projective reparametrization changes only its spanning
matrix, proving invariance and all three equivalences.

## Theorem 2 - Galois stabilizer

Let `G=Gal(F/B)` and

```text
G_proj(R) = {sigma in G : sigma(W_R)=W_R}.
```

Then

```text
F_proj(R) = F^(G_proj(R)).
```

Moreover, for every `sigma in G`,

```text
sigma(R) is codeword-gauge/projectively equivalent to R
    iff sigma(W_R)=W_R
    iff F_proj(R) subseteq F^sigma.
```

When `y_1 != 0`, the affine analogue is

```text
G_aff(R) = {sigma in G :
            sigma(W_R)=W_R and sigma(F y_1)=F y_1},
F_aff(R) = F^G_aff(R).
```

### Proof

If `sigma(W_R)=W_R`, then `sigma(M_R)` is another reduced-row-echelon basis
matrix for `W_R`, so uniqueness gives `sigma(M_R)=M_R`. Conversely, if
`sigma` fixes the entries of `M_R`, it stabilizes `W_R`. The subgroup
`G_proj(R)` is therefore exactly the subgroup fixing the field generated by
the entries of `M_R`. The finite-field Galois correspondence gives the
fixed-field formula.

If `sigma(R)=RA+K` for some `A in GL_2(F)` and codeword gauge `K`, applying
`H` gives `sigma(Y_R)=Y_R A`, hence `sigma(W_R)=W_R`. Conversely, if the
two syndrome matrices have the same column span and rank, an invertible
column operation `A` satisfies `sigma(Y_R)=Y_R A`. Both columns of
`sigma(R)-RA` then have zero syndrome and are codewords. The final
equivalence follows because `sigma(W_R)=W_R` exactly when `sigma` fixes the
entries generating `F_proj(R)`, equivalently when
`F_proj(R) subseteq F^sigma`. Applying the same reduced-row-echelon argument
to an adapted basis of the flag `F y_1 subseteq W_R` proves the affine
formula.

## Theorem 3 - Projective subline confinement

If `F_proj(R) subseteq E`, then for some `A in PGL_2(F)`,

```text
Z_hat_a(R) subseteq A P^1(E).
```

Consequently `|Z_hat_a(R)| <= |E|+1`. After the normalizing gauge and
projective reparametrization, every projective witness has an `E`-rational
direction and an explaining polynomial in `E[X]`.

If the normal form is reached by an affine reparametrization preserving the
point at infinity, then there are `alpha != 0` and `beta in F` such that

```text
Z_a(R) subseteq alpha E+beta,
```

so the finite-slope set has size at most `|E|`.

### Proof

By Theorem 1, normalize `R` to an `E`-valued pair `Q=[q_0 q_1]`. Put
`z_i=s(q_i)`. Let `[u:v]` be bad on `S`, and put `T=D\S`. Define

```text
V_T(E) = span_E{H_x : x in T},       V_T(F) = F V_T(E).
```

Since a word is explained on `S` exactly when its syndrome is supported
through the parity columns indexed by `T`,

```text
u*z_0+v*z_1 in V_T(F).
```

The parity columns lie in `B^(n-k)`, so `V_T(F)` is the scalar extension of
`V_T(E)`. Consider the `E`-linear map

```text
E^2 -> E^(n-k)/V_T(E),      (c,d) |-> c*z_0+d*z_1 mod V_T(E).
```

Support-wise nontriviality says this map is not zero. The bad direction
gives a nonzero kernel after scalar extension to `F`; therefore the map has
rank one and its kernel is the scalar extension of a one-dimensional
`E`-kernel. Hence `[u:v] in P^1(E)`.

Choose an `E`-valued representative `(u,v)`. The explained word
`u q_0+v q_1` is `E`-valued on `D`. Interpolation of `h` on any `k` points
of `S subseteq B` uses a Vandermonde matrix over `B`, so `h in E[X]`.
Transporting directions back through the normalizing projective matrix gives
the displayed subline containment. If that matrix preserves infinity, its
finite-chart action sends `E` to an affine coset `alpha E+beta`, proving the
last assertion.

## Theorem 4 - Canonical proper-field C5 first-match coverage

For each proper intermediate field `E` define the intrinsic minimal-field
stratum

```text
D_E = {R : rank(Y_R)>0 and F_proj(R)=E}
```

More explicitly, on the rank-`d` chart, `d in {1,2}`, put

```text
X_E,d = {R : rank(Y_R)=d and
             rank[Y_R | phi_E(Y_R)]=d},
phi_E(x)=x^|E|.

D_E cap {rank(Y_R)=d}
  = X_E,d \ union_{B subseteq E' subsetneq E} X_E',d.
```

Define the C5 incidence over the source finite-slope chart by

```text
C_5,E = {(R,w) : R in D_E and w in W_a(R)}.
```

This is a locally constructible profile cell. For every `R in D_E`, its
realized witness fiber is all of `W_a(R)` and its raw slope projection is
all of `Z_a(R)`.

Now place `C_5,E` after any realized C1--C4 cells in the printed order. If
`Z_<5(R)` is the union of their actual slope projections, then the C5
first-match projection is exactly

```text
Z_5,E^circ(R) = Z_a(R) \ Z_<5(R).
```

Thus C1--C5 are witness-exhaustive for every proper-field descended pair,
their first-match slope projections partition `Z_a(R)`, and no slope of such
a pair reaches C6--C8 or the primitive residual.

### Proof

Let `phi_E(x)=x^|E|`. On a chart where `rank(Y_R)=d`, the condition that
`W_R` is defined over `E` is

```text
rank[Y_R | phi_E(Y_R)] = d.
```

Indeed, this rank condition says `phi_E(W_R)=W_R`; Theorem 2 then says that
the minimal field is contained in the fixed field `E`. Rank equalities and
inequalities are finite Boolean combinations of minor vanishings and
nonvanishing rank pivots. Subtracting the corresponding loci for the finitely
many proper intermediate fields `E' subsetneq E` gives `D_E`. Intersecting
with the locally constructible universal witness incidence proves that
`C_5,E` is locally constructible.

The definition of `C_5,E` makes its fiber over `R in D_E` equal to the
entire exact witness fiber. Theorem 3 supplies an `E`-defined normal form for
every witness, so this is a literal field-descent cell rather than a raw
coordinate-field label. The source first-match definition now gives the
displayed set difference. Since C5 contains every witness not already
assigned earlier, the C1--C5 family is witness-exhaustive for this pair and
all later first-match parts are empty.

## Theorem 5 - Post-C5 fixed-fiber Frobenius route cut

Let `Z_5(R)` be `Z_a(R)` when `F_proj(R)` is a proper intermediate field,
and let it be empty when `F_proj(R)=F`. Define the literal post-C5 residual

```text
W_>5(R) = W_a(R) cap
          pi_gamma^(-1)(F \ (Z_<5(R) union Z_5(R))).
```

If `W_>5(R)` is nonempty, then

```text
F_proj(R)=F.
```

For every nonidentity `sigma in Gal(F/B)`, there are no
`A in GL_2(F)` and no codeword gauge `K` with

```text
sigma(R)=RA+K.
```

Therefore coefficientwise Frobenius covariance cannot be converted, by
codeword gauge and projective reparametrization, into a nontrivial action on
the fixed residual fiber `W_>5(R)`. Any post-C5 orbit-divisibility argument
must prove a separate automorphism preserving the literal residual equations,
first-match masks, and slope or codeword projection.

### Proof

If `F_proj(R)` were proper, Theorem 4 would give `Z_5(R)=Z_a(R)`, making
`W_>5(R)` empty. Thus a nonempty residual has `F_proj(R)=F`.

If a nonidentity `sigma` admitted the displayed gauge/projective
compensation, Theorem 2 would imply

```text
F_proj(R) subseteq F^sigma subsetneq F,
```

contradicting `F_proj(R)=F`.

Coefficientwise Galois action always gives a bijection

```text
(gamma,S,h) |-> (sigma(gamma),S,sigma(h))
W_a(R) -> W_a(sigma(R)).
```

When the chosen C1--C5 masks are Galois-equivariant, this restricts to
covariance between the corresponding residual fibers. The preceding
contradiction shows that the standard gauge/projective compensation cannot
turn that between-pair covariance into a fixed-pair action after C5.

## Exact scope

The five theorems prove only the intrinsic projective syndrome field, its
Galois stabilizer, projective subline confinement, proper-field C5 coverage
after C1--C4 first match, and the post-C5 fixed-fiber Frobenius route cut.

They do not prove that C1--C8 cover field-full pairs, certify a profile
payment for C5, bound a deployed finite ledger, compare an asymptotic profile
envelope with its target, construct a residual automorphism, prove an
adjacent inequality, or establish an MCA or interleaved-list threshold. No
stable TeX is changed.
