# All-pair paving-basis multiplicity compiler

## Status and provenance

```text
Mathematical status: PROVED under the displayed weighted-RS hypotheses.
Counted object: every retained (slope,witness) pair, with same-slope multiplicity.
Verifier status: EXPERIMENTAL exact-integer formula replay; not a proof.
Lean status: UNPROVED STATEMENT TARGET; not Lean-certified.
Paper effect: none.
Official score effect: none; score remains 0/2.
```

This note packages the audited R17B Role 09 result at repository base
`c35a6da31ed0905afcbaaefe4eb0f242572ebb35`.  The read-only worker return was

```text
/Users/danielcabezas/RS_MCA_PRIZEBREAK_9PRO_20260714_R17B/
  returns_raw/pro_safari/ROLE_09_final_response.md
SHA256 8498aaa42ff00a5de80d3b6428552abfd9b1642938e1cdde609d5d9c2dea1588
```

The proof below corrects one sign typo in that return.  In the monotonicity
comparison, the displayed ratio is greater than `1`, not less than `1`.

## 1. Weighted-RS chart and counted object

Let `F` be a finite field, let `U subset F` contain `N` distinct locators, and
let

```text
H : F^U -> F^R,
h_x = lambda_x (1,x,...,x^(R-1))^T,       lambda_x != 0,
N = R + kappa,                            kappa >= 1.
```

Thus `K=ker H` is an `[N,kappa,R+1]` generalized Reed--Solomon code.  Fix

```text
0 <= t < R,       y_0,y_1 in F^R,       y_1 != 0.
```

Let `P` be any finite set of distinct retained pairs `(gamma,c)` satisfying

```text
H c = y_0 + gamma y_1,
wt(c) <= t,
{y_0,y_1} not subset span_F{h_x : x in supp(c)}.          (1)
```

There is no one-witness-per-slope selector.  Distinct witnesses at the same
slope are distinct members of `P`.  The theorem applies to any retained
subset, so an earlier first-match deletion can only decrease its left side.

Choose lifts `b_0,b_1 in F^U` with `H b_i=y_i`, and let `G` be an `N x kappa`
matrix whose columns form a basis of `K`.  Define

```text
A = [b_0  b_1  G],
beta_(kappa+1)(A)
  = #{I subset U : |I|=kappa+1 and rank(A_I)=kappa+1}.    (2)
```

Also define the literal direction-coset distance

```text
d = min{wt(v) : H v = y_1}.                              (3)
```

Every `R` parity columns form a basis, so `1 <= d <= R`.

For integers `0 <= w <= t`, put

```text
Lambda_d(w) = max {
  binom(N-w-1,kappa),
  ceil((d-w)_+ binom(N-w,kappa)/(kappa+1))
},                                                        (4)
```

where `(a)_+=max(a,0)`.  In particular,

```text
Lambda_(d,t) = Lambda_d(t).                              (5)
```

Since `N-t-1 >= kappa`, the first term in (4) is positive.

## 2. The theorem

### Theorem 1 (all-pair weighted basis charge)

Under (1)--(5),

```text
sum_((gamma,c) in P) Lambda_d(wt(c))
  <= beta_(kappa+1)(A)
  <= binom(N,kappa+1).                                   (PB1)
```

Consequently,

```text
|P| <= floor(beta_(kappa+1)(A)/Lambda_(d,t))
    <= floor(binom(N,kappa+1)/Lambda_(d,t)).              (PB2)
```

Dropping the direction term gives the unconditional field-independent bound

```text
|P| <= floor(
  binom(N,kappa+1) / binom(N-t-1,kappa)
).                                                        (PB3)
```

The slope projection of `P` is no larger than `P`, so each inequality also
bounds the number of retained slopes.  Its primary content, however, is the
pair count.

### Theorem 2 (deep-hole specialization)

If `d=R`, then `K+<b_1>` is an `[N,kappa+1,R]` MDS code and

```text
sum_((gamma,c) in P) binom(N-wt(c),kappa+1)
  <= beta_(kappa+1)(A)
   = binom(N,kappa+1).                                   (PB4)
```

Hence

```text
|P| <= floor(
  binom(N,kappa+1) / binom(N-t,kappa+1)
)                                                        (PB5)
```

in the deep-hole case.

### Corollary 3 (one-circuit case)

For `kappa=1`, so `N=R+1`, (PB3) is exactly

```text
|P| <= floor(R(R+1)/(2(R-t))).                            (PB6)
```

This is strictly below `binom(R+1,2)` when `t <= R-2`, and it counts all
pairs rather than only selected slopes.

## 3. Proof

### 3.1 Parameter vectors and exact local rank

For each `(gamma,c) in P`, uniqueness of kernel coordinates gives a unique
`z_(gamma,c) in F^kappa` such that

```text
c = b_0 + gamma b_1 + G z_(gamma,c).
```

Set

```text
p_(gamma,c) = (1,gamma,z_(gamma,c))^T,
Z_c = {x in U : c_x=0},
w = wt(c),
m = |Z_c| = N-w.
```

Then `A p_(gamma,c)=c`, so `A_(Z_c) p_(gamma,c)=0`.  Also

```text
m >= N-t = kappa+(R-t) >= kappa+1.                       (6)
```

We claim

```text
rank(A_(Z_c)) = kappa+1.                                 (7)
```

The rank is at most `kappa+1` because the displayed nonzero parameter vector
lies in the nullspace.  If it were at most `kappa`, that nullspace would have
dimension at least two.  Choose a null vector independent of
`p_(gamma,c)` and subtract its first coordinate times `p_(gamma,c)`.  This
produces a nonzero null vector

```text
q=(0,delta,z)^T.
```

If `delta=0`, then `G_(Z_c) z=0`.  Every `kappa` rows of the GRS generator
`G` are independent, while `|Z_c|>=kappa+1`, so `z=0`, a contradiction.
Thus `delta!=0`.

Now `p'=p_(gamma,c)+q` has first two coordinates `(1,gamma+delta)`.  The word
`c'=A p'` vanishes on `Z_c`, hence is supported on `supp(c)`, and

```text
H c' = y_0 + (gamma+delta)y_1.
```

Both this syndrome and `y_0+gamma y_1=Hc` lie in the parity-column span on
`supp(c)`.  Their difference puts `y_1` in that span, and then `y_0` is in it
as well, contradicting (1).  This proves (7).

Moreover, every set of at most `kappa` rows of `A_(Z_c)` is independent:
projecting any row dependence to the last `kappa` coordinates would give a
dependence among the corresponding rows of `G`.

### 3.2 Paving-matroid lower charge

Use the elementary lemma:

> If a rank-`r` matroid on `m` elements has every `(r-1)`-subset independent,
> then it has at least `binom(m-1,r-1)` bases.

For completeness, induct on `m+r`.  If an element is a coloop, every
`(r-1)`-subset of the other `m-1` elements is a basis of the deletion, giving
exactly the required count.  Otherwise deletion has rank `r`, contraction has
rank `r-1`, and both retain the relevant independence hypothesis.  The two
inductive lower bounds add by Pascal's identity.

Apply the lemma to the row matroid of `A_(Z_c)` with `r=kappa+1`.  Equations
(6)--(7) give at least

```text
binom(m-1,kappa) = binom(N-w-1,kappa)                     (8)
```

local bases contained in `Z_c`.

### 3.3 Direction-distance lower charge

Let

```text
G_1=[b_1  G],       C_1=colspan(G_1)=K+<b_1>.
```

The minimum distance of `C_1` is exactly `d`.  A nonzero kernel word has
weight at least `R+1>d`; a word with nonzero `b_1` coefficient rescales to a
lift of `y_1` and has weight at least `d`; and a minimum lift of `y_1` lies in
`C_1`.

On `Z_c`, the equation `c=0` gives

```text
b_0(x) = -gamma b_1(x) - G_x z_(gamma,c).
```

Thus the rows of `A_(Z_c)` are injective linear images of the rows of
`(G_1)_(Z_c)` and have the same row matroid.

Fix a `kappa`-subset `J subset Z_c`.  It is independent, so its closure is a
hyperplane in the local rank-`kappa+1` matroid.  A nonzero coefficient vector
of `C_1` annihilates that hyperplane.  Since every nonzero `C_1` word has at
most `N-d` zeros, the closure contains at most `N-d` coordinates.  Therefore,
when `d>w`, `J` has at least

```text
m-(N-d)=d-w
```

extensions to a local basis.  Counting `(J,x)` incidences and dividing by the
`kappa+1` subfaces of each basis yields at least

```text
ceil((d-w) binom(N-w,kappa)/(kappa+1))                    (9)
```

local bases.  For `d<=w`, the truncated direction term in (4) is zero.  Taking
the maximum of (8) and (9) proves the local lower charge `Lambda_d(w)`.

If `d=R`, then

```text
(R-w) binom(N-w,kappa)/(kappa+1)
  = binom(N-w,kappa+1).                                  (10)
```

The right side is the total number of `(kappa+1)`-subsets of `Z_c`, so every
such subset is a local basis.  This is the strengthened deep-hole charge.

The same MDS fact also determines the global census.  Every
`(kappa+1)`-row restriction of `[b_1 G]` has rank `kappa+1`, and `[b_1 G]`
is a column submatrix of `A`.  Therefore every `(kappa+1)`-row subset of
`A` is a basis:

```text
beta_(kappa+1)(A)=binom(N,kappa+1).                      (10a)
```

Thus the second relation in (PB4) is equality, not merely the generic upper
bound inherited from (PB1).

### 3.4 A global basis has at most one pair-owner

Let `I subset U`, `|I|=kappa+1`, and `rank(A_I)=kappa+1`.  Since `A_I` has
`kappa+2` columns, its nullspace is one-dimensional.  If `I subset Z_c`, then
`p_(gamma,c)` spans that nullspace.

If the same `I` were contained in `Z_(c')` for another retained pair, the two
parameter vectors would span the same line.  Both have first coordinate one,
so they are equal.  Their slope and kernel coordinates are equal, hence their
errors are equal.  Distinct pairs therefore cannot charge the same global
basis.

Summing the local basis charges over all pairs proves the first inequality in
(PB1).  The second is immediate because there are only
`binom(N,kappa+1)` row subsets of that size.

### 3.5 Correct monotonicity comparison

Both terms in (4) are nonincreasing in `w`.  For the direction numerator set

```text
f(w)=(d-w) binom(N-w,kappa),       w<d.
```

For `w<=d-2`, the exact comparison is

```text
f(w)/f(w+1)
  = ((d-w)/(d-w-1)) ((N-w)/(N-w-kappa))
  > 1.                                                    (11)
```

This is the corrected sign.  At `w=d-1`, the next truncated value is zero;
for `w>=d`, both truncated values are zero.  Hence the direction numerator,
its ceiling quotient, and `Lambda_d(w)` are nonincreasing.  Therefore every
pair contributes at least `Lambda_d(t)`, proving (PB2).  Dropping the direction
term gives (PB3), and (10) gives (PB4)--(PB5).

### 3.6 Choice invariance

Any other lifts and kernel basis have the form

```text
b_i' = b_i + G alpha_i,       G'=GQ,       Q in GL_kappa(F).
```

Thus `A'=AT` for an invertible block-triangular matrix `T`.  Right
multiplication by `T` preserves every row-subset rank, so
`beta_(kappa+1)(A)` is independent of all auxiliary choices.

## 4. Sharp boundary family

Take `t>=2` and

```text
R=t+1,       N=t+kappa+1,
h_a=(1,a,...,a^t)^T,
y_0=e_(t-1),       y_1=e_t,
```

over a field containing `N` distinct points `U`.  For every `t`-subset
`S subset U`, put

```text
Q_S(X)=product_(a in S)(X-a),
c_S(a)=1/Q_S'(a) for a in S, and 0 otherwise.
```

Lagrange coefficient extraction gives

```text
H c_S = y_0 + (sum_(a in S) a)y_1.
```

The coefficient functional defined by the monic polynomial `Q_S` annihilates
the columns indexed by `S` and takes value one on `y_1`; every pair is
transverse.  Also `d=R`.  The family has

```text
|P|=binom(N,t)=binom(N,kappa+1),
Lambda_(R,t)=binom(N-t,kappa+1)=1,
```

so equality holds in (PB2) and (PB5).  At `F_5,t=kappa=2`, the ten pairs have
five slopes, each with two witnesses.

This family is not new here.  It is the route-cut family already recorded in
`selector_free_exact_weight_all_pair.md`; this theorem consumes it as the
equality witness.  In particular, the family proves that even `d=R` does not
force a universal chart-only subexponential pair bound.

## 5. Exact overlap and novelty boundary

The result is deliberately narrower than the worker return's broad novelty
language.

1. `agreement_weighted_transverse_secant.md` already proves the denominator
   `binom(N-t-1,kappa)` for one selected witness per slope.  Formula (PB3) is
   not claimed as a new selected-slope formula.  The new step is the normalized
   parameter-vector ownership showing that the same denominator charges every
   retained pair, including repeated-slope witnesses.
2. `all_lineray_affine_core_set_pair.md` already counts every pair by the
   nonuniform Bollobas charge
   `sum 1/binom(s+wt(c),s)<=1`, using the actual all-pair affine-core dimension
   `s`.  It does not define `beta_(kappa+1)(A)`, charge all zero-set bases, or
   give (PB1), the direction refinement, or the deep-hole census.  Neither
   compiler subsumes the other: the affine-core theorem is strongest when its
   global or nested ranks are small, while the present theorem is rank-free but
   may remain exponential.
3. `selector_free_direction_distance_all_pair.md` already proves the
   high-direction Johnson bound and the minimum-lift punctured realized-word
   bound for all pairs.  Those compilers count a ball or punctured clusters.
   They do not count augmented row bases or obtain the local paving charge.
   The present theorem remains valid on their double-nonpositive locus, but it
   need not pay that locus subexponentially.
4. `ray_compiler_balanced_core.md` and the later agreement-weighted note already
   contain the one-minor-per-slope and selected-slope transverse-secant routes.
   A basis determining only a slope is not claimed as new.

The publishable delta is therefore exactly: an intrinsic augmented-basis
census, a many-bases-per-pair charge, one-pair-per-basis ownership, and the
direction/deep-hole strengthening, all on the complete retained pair set.

## 6. Finite arithmetic and reproducibility

For the formula calibration

```text
(N,R,kappa,t,d)=(90,86,4,31,50),
```

one obtains

```text
binom(90,5) = 43,949,268,
binom(58,4) = 424,270,
ceil(19 binom(59,4)/5) = 1,729,479,
|P| <= floor(43,949,268/1,729,479) = 25.
```

This is a formula calibration, not a deployed-row certificate and not an
attainment claim.

Run the standard-library arithmetic verifier with

```bash
python3 experimental/scripts/verify_all_pair_paving_basis_compiler.py --check
python3 -O experimental/scripts/verify_all_pair_paving_basis_compiler.py --check
python3 experimental/scripts/verify_all_pair_paving_basis_compiler.py --tamper-selftest
python3 -O experimental/scripts/verify_all_pair_paving_basis_compiler.py --tamper-selftest
```

The canonical `--check` transcript and packet hashes are under

```text
experimental/data/certificates/all-pair-paving-basis-compiler/
```

The verifier checks only exact finite formulas, monotonicity comparisons, the
one-circuit specialization, the deep-hole binomial identity, the small sharp
multiplicity count, and pinned mutation rejection.  It does not construct the
weighted-RS source object, verify transversality, prove the paving-matroid
lemma, prove basis ownership, or replace the proof above.

The matching Lean file is

```text
experimental/lean/grande_finale/GrandeFinale/PavingBasisAllPairs.lean
```

It contains definitions and **UNPROVED STATEMENT TARGETS** only.  Successful
typechecking is not a formal proof of this note.

## 7. Ledger impact, nonclaims, and exact next wall

For one actual residual profile `lambda`, (PB2) replaces a field-size surrogate
by the literal local ratio

```text
beta_(kappa+1)(A_lambda) / Lambda_(d_lambda,t_lambda).
```

That is a local compiler, not a complete first-match or profile-envelope
theorem.  This packet does not prove a witness-exhaustive atlas, an image-scale
MI+MA or Sidon payment, ownership or summation for every surviving profile, a
lower unsafe-side reserve, a target crossing, Grand MCA, or Grand List.  It
does not merge generated, line, challenge, list, base, or extension fields.
It changes no stable paper and moves no official score.

The exact remaining wall is the **deep-hole pencil/design owner dichotomy**,
with first sharp case

```text
d=R,       R-t=1.
```

Here basis heaviness is automatic: (10a) fixes `beta_(kappa+1)(A)` at its
maximum for every chart, regardless of whether the two hosted syndromes have
rank one or two and regardless of planted or generic presentation.  The basis
census therefore has no inverse content on its own.  For every
first-match-surviving primitive chart on this boundary, one must instead
either prove that the resulting distributed core pencils/design packing has
subexponential normalized mass, or route the entire corresponding pair fibers
to a named earlier source owner before this compiler is applied.  Numerically
the local ratio is already forced to be

```text
binom(N,kappa+1) / Lambda_(R,t).
```

The sharp family in Section 4 disproves the owner-free universal
subexponential alternative.  The exact core-pencil slack identity, its
Steiner-design equality case, and a positive-depth Frobenius fixture are
recorded in `augmented_basis_pencil_design_inverse.md`.  No unpublished
recurrence is used as part of this theorem claim.
