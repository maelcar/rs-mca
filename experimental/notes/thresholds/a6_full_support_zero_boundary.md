# A6 full-support and zero-denominator payment

- **Status:** PROVED for the completed-witness chart stated below.
- **Track:** asymptotic hard input C / condition A6.
- **Companion:** `experimental/notes/thresholds/low_direction_hybrid_exact_weight.md`.
- **Verifier:**
  `experimental/scripts/verify_a6_full_support_zero_boundary.py`
  (zero arguments, Python standard library only).

## Scope and independence

Let `F` be any field and let `H_U : F^U -> F^R` have weighted
Reed--Solomon parity columns

```text
h_x = lambda_x (1,x,...,x^(R-1))^T,  lambda_x != 0,
```

at `N` distinct points, where

```text
N = R+kappa,  kappa >= 1.
```

Fix `0 <= t < R`, syndromes `y_0,y_1` with `y_1 != 0`, and a set `Z^o`
of distinct slopes.  For every `gamma in Z^o`, select an actual completed
witness `c_gamma` such that

```text
H_U c_gamma = y_0+gamma y_1,
wt(c_gamma) <= t,
{y_0,y_1} is not contained in
  span{h_x : x in supp(c_gamma)}.                           (1)
```

Choose a minimum lift `v` of `y_1` and define

```text
d = wt(v),  J = supp(v),  M = N-d,
Delta = R+1-d = M-kappa+1.                                 (2)
```

For `w_gamma=P_J(c_gamma)` and `e=wt(w_gamma)`, let `Z_e^o` be the
corresponding exact-weight slopes and put

```text
q_e = d+2e-2t,
D_e = min(M,max(Delta,q_e)),
J_e = M D_e-2Me+e^2,
h_e = max(1,d+e-t).                                        (3)
```

Necessarily `0 <= e <= min(t,M)`.  The results below are proved directly for
these completed tuples.  No positive-`J_e` amendment is a hypothesis.  In
particular, the note does not claim that the `W1+` or `W2+` branches are fully
closed.

## The theorem

Under the preceding hypotheses:

1. If `K=ker(H_U)` and `L=K+<v>`, then `L` is an `[N,kappa+1]` code with

   ```text
   d_1(L)=d,
   d_r(L)=R+r-1  for 2 <= r <= kappa+1.                    (4)
   ```

   Consequently, for every zero mask `T subset U` with `|T| >= N-t`, the
   affine space of completed parameters whose witnesses vanish on `T` is
   empty or has affine dimension at most one.

2. The entire full-separation branch `W3+`, defined by `q_e >= M`, is paid
   without importing a positive-`J_e` result.  For `e<M`,

   ```text
   |Z_e^o| <= floor(d/h_e) floor(M/(M-e)).                  (5)
   ```

   For `e=M` (which forces `t>=M`),

   ```text
   |Z_M^o| <= 1                         if N>2t,
             1                         if N=2t and t=M,
             floor(d/(t-M))            if N=2t and t>M.    (6)
   ```

   Thus every `W3+` exact-weight stratum has an absolute polynomial bound,
   and the sum over that branch is at most `N^3+N`.

3. Every zero-denominator stratum `J_e=0` is paid.  If `e<M`, then

   ```text
   |Z_e^o| <= 2(M-1) floor(d/h_e) <= 2N^2.                 (7)
   ```

   This applies both when

   ```text
   q_e <= Delta,  e^2-2Me+MDelta=0,                        (8)
   ```

   and when

   ```text
   Delta < q_e < M,  e^2=M(2t-d).                          (9)
   ```

   The `e=M, q_M>=M` equality is already covered by (6).  At the only other
   endpoint, `e=M, J_M=0, q_M<M`, one necessarily has `kappa=1`, and

   ```text
   |Z_M^o| <= binom(d,2).                                  (10)
   ```

4. Algebraically, the exact strict-negative locus is

   ```text
   W1-: q_e <= Delta and e^2-2Me+MDelta < 0,

   W2-: Delta < q_e < M and e^2 < M(2t-d).                 (11)
   ```

   There is no strict-negative `W3+` stratum.  Equations (11) are the exact
   remaining `J_e<0` walls after the equality payments in this note.  This is
   a classification of the unresolved strict locus, not a claim that every
   positive stratum of `W1+` or `W2+` has been proved here.

## Proof

### 1. Generalized weights and fixed zero masks

The kernel `K` is an `[N,kappa,R+1]` GRS code, so

```text
d_r(K)=R+r,  1 <= r <= kappa.                              (12)
```

Any `R` parity columns form a basis.  Hence `d<=R`.  Since `v` is not in
`K`, the code `L=K+<v>` has dimension `kappa+1`.  Every word in `L\K` is a
nonzero scalar multiple of a lift of `y_1`, and therefore has weight at least
`d`; the minimum is attained by `v`.  Nonzero words of `K` have weight at
least `R+1>d`.  This proves `d_1(L)=d`.

Let `S` be an `r`-dimensional subcode of `L`, where `r>=2`.  If `S` is
contained in `K`, then (12) gives `|supp(S)|>=R+r`.  Otherwise
`dim(S intersect K)=r-1`, and

```text
|supp(S)| >= d_(r-1)(K)=R+r-1.                             (13)
```

The generalized Singleton bound for the `[N,kappa+1]` code `L` gives the
reverse inequality

```text
d_r(L) <= N-(kappa+1)+r=R+r-1.                             (14)
```

This proves (4).

Choose a basis `k_1,...,k_kappa` of `K` and a lift `u_*` of `y_0`.  The
completed parameterization is

```text
c(alpha,gamma)=u_*+sum_j alpha_j k_j+gamma v.              (15)
```

For a fixed zero mask `T`, the translation space of the equations
`c(alpha,gamma)|_T=0` is the shortened code

```text
L_T={z in L:z|_T=0}.                                       (16)
```

If `dim(L_T)>=2`, it contains a two-dimensional subcode supported on at most
`N-|T|<=t` coordinates.  This contradicts
`d_2(L)=R+1>t`.  The affine incidence is therefore empty, a point, or an
affine line.

### 2. Multiplicity above a punctured word

Puncturing on `J` is injective on `K`: a kernel word killed by puncturing
would have support at most `d<=R`, below the kernel distance `R+1`.  Thus the
punctured kernel is an `[M,kappa,Delta]` GRS code, and the punctured
`y_0`-solution space is one affine coset of it.

Fix a punctured word `w` of weight `e` and let `u` be its unique affine lift.
Every selected slope above `w` has

```text
c_gamma=u+gamma v.                                        (17)
```

The weight condition forces at least `d+e-t` zeros on `J` when this is
positive.  Even if it is nonpositive, (1) forces at least one zero on `J`:
otherwise both `supp(u)` and `supp(v)` would lie in `supp(c_gamma)`, placing
both `y_0` and `y_1` in the forbidden span.  Hence each selected slope above
`w` uses at least `h_e` zeros on `J`.  For each `x in J`, the nonconstant
affine function `u(x)+gamma v(x)` vanishes for at most one slope.  Counting
zero incidences gives

```text
#{gamma : P_J(c_gamma)=w} <= floor(d/h_e).                 (18)
```

### 3. Direct payment of all of W3+

Retain one completed tuple for each distinct punctured word of exact weight
`e`, and let `X_w` be its zero set in the `M`-coordinate outside block.  The
punctured GRS distance first gives

```text
|X_w intersect X_w'| <= M-Delta.                           (19)
```

Let `Y_w` be the zero set of the retained completed witness on `J`.  The
weight condition gives `|Y_w|>=max(0,d+e-t)`, and hence

```text
|Y_w intersect Y_w'| >= max(0,d+2e-2t)=max(0,q_e).         (20)
```

After division by the nonzero slope difference, the difference of the two
completed witnesses is a lift of `y_1`; it has at most `M=N-d` zeros in all
`N` coordinates.  Combining this fact with (19)--(20), and observing that no
distinct pair exists if the uncapped lower separation exceeds `M`, gives

```text
|X_w intersect X_w'| <= M-D_e.                             (21)
```

If `q_e>=M`, then `D_e=M`.  For `e<M`, the sets `X_w`, each of size `M-e`,
are pairwise disjoint.  There are therefore at most `floor(M/(M-e))`
distinct punctured words.  Multiplication by (18) proves (5).  This argument
is direct and does not invoke the sign of `J_e`.

It remains to prove (6).  Suppose `e=M`, and for each selected slope let

```text
Y_gamma={x in J:c_gamma(x)=0}.
```

The outside block already has weight `M`, so

```text
|Y_gamma| >= d-(t-M)=N-t.                                  (22)
```

For distinct slopes, `(c_gamma-c_gamma')/(gamma-gamma')` is a lift of
`y_1`, hence has at most `M` zeros.  Thus

```text
|Y_gamma intersect Y_gamma'| <= M.                         (23)
```

On the other hand, inclusion-exclusion inside the `d`-set `J` yields

```text
|Y_gamma intersect Y_gamma'|
  >= 2(N-t)-d = N+M-2t = q_M.                              (24)
```

The condition `q_M>=M` is equivalent to `N>=2t`.  If `N>2t`, (23)--(24)
allow at most one slope.  If `N=2t` and at least two slopes occur, equality
must hold throughout: every `Y_gamma` has size `t`, and every pair intersects
in `M` points.  The complements

```text
A_gamma=J\Y_gamma
```

are pairwise disjoint sets of size `t-M`.  If `t>M`, packing them in `J`
gives the last bound in (6).  If `t=M`, every witness is supported on the
same outside set `U\J`.  Two slopes would put two points of the syndrome line
in the parity-column span of that set; subtraction would put `y_1` there and
then `y_0` there, contradicting (1).  This proves (6).

For `e<M`, each factor in (5) is at most `N`, and there are at most `N`
weights.  The endpoint bound is at most `N`, proving the stated branch sum.

### 4. The nonendpoint equality faces

We use the elementary right-angle lemma: if nonzero vectors
`z_1,...,z_L` lie in a real inner-product space of dimension `s` and
`<z_i,z_j><=0` for `i!=j`, then `L<=2s`.

For completeness, project onto `z_L^perp`.  At most one other vector has zero
projection, since two nonzero negative multiples of `z_L` have positive
mutual inner product.  The remaining projections still have nonpositive
pairwise inner products.  Induction on `s`, followed by adding `z_L` and the
possible negative multiple, proves the lemma.

First suppose `e<M`, `D_e=Delta`, and `J_e=0`.  Put

```text
A=M-e,  C=M-Delta.
```

For distinct punctured words, the GRS distance gives
`|X_w intersect X_w'|<=C`.  The equality `J_e=0` says `A^2=MC`.  Since
`0<A<M`, the centered incidence vectors

```text
z_w=1_(X_w)-(A/M)1
```

are nonzero, lie in the `(M-1)`-dimensional space `1^perp`, and satisfy

```text
<z_w,z_w'> = |X_w intersect X_w'|-A^2/M <= 0.              (25)
```

The right-angle lemma gives at most `2(M-1)` punctured words.

Next suppose `e<M`, `D_e=q_e`, and `J_e=0`.  Let `B_w=supp(w)`, so
`|B_w|=e`.  From (21),

```text
|B_w intersect B_w'|
  =2e-M+|X_w intersect X_w'|
  <=2e-q_e=2t-d=:C.                                       (26)
```

Now `J_e=0` says `e^2=MC`; also `0<e<M`.  The vectors

```text
z_w=1_(B_w)-(e/M)1
```

again form a nonpositive-inner-product family in `1^perp`, so there are at
most `2(M-1)` punctured words.  Multiplying both face bounds by (18) proves
(7)--(9).

### 5. The kappa=1 endpoint

Suppose `e=M`, `J_M=0`, and `q_M<M`.  Since

```text
J_M=M(D_M-M),
```

we have `D_M=M`.  The cap cannot come from `q_M`, so `Delta=M`.  Equation
(2) then forces `kappa=1`.

Let `k` generate the `[N,1,N]` kernel and choose a lift `u_*` of `y_0`.
Every selected witness has a unique representation

```text
c_gamma=u_*+alpha_gamma k+gamma v.                         (27)
```

Every coordinate of `k` is nonzero, and every coordinate of `v` on `J` is
nonzero.  For `x in J`, its zero condition is therefore an affine line in
the `(alpha,gamma)` plane,

```text
l_x: u_*(x)+alpha k(x)+gamma v(x)=0,                       (28)
```

which is a genuine graph over `gamma`.  A selected full-outside-support
witness has at least `N-t>=2` zeros on these lines.

Group coordinates that define identical lines.  If a selected parameter
point lies on at least two distinct line classes, it is among at most
`binom(g,2)<=binom(d,2)` pairwise intersections, where `g` is the number of
classes.  If it lies on only one class `T`, then that class has at least two
coordinates and is the complete zero set of the selected witness.  Write its
line as `alpha=A+B gamma`.  Along it, (27) becomes

```text
c_gamma=a+gamma b,
H_U a=y_0,  H_U b=y_1,
```

with both `a` and `b` zero on `T`.  At the selected point every coordinate
outside `T` is nonzero.  Thus both syndromes lie in the column span of the
selected support, contradicting (1).  Every selected slope is consequently
represented by an intersection of two distinct line classes, proving (10).

### 6. Exact strict wall

The three possibilities in (3) give exact formulas:

```text
q_e <= Delta:       J_e=e^2-2Me+MDelta,
Delta < q_e < M:   J_e=e^2-M(2t-d),
q_e >= M:           J_e=(M-e)^2.                           (29)
```

The first two formulas give exactly (11), while the third is never negative.
This proves the strict-wall classification.

## Ledger effect and nonclaims

- The theorem pays all of `W3+` and all `J_e=0` strata for an actual completed
  witness chart satisfying (1).
- The fixed-mask theorem reduces each individual full-zero-mask incidence to
  dimension at most one.  It does not aggregate exponentially many masks.
- The strict `W1-` and `W2-` loci in (11) remain unpaid.
- This note does not claim `W1+` or `W2+` fully closed and does not use an
  unlanded positive-`J_e` amendment as a theorem input.
- No A2 witness-exhaustive atlas, A4 image-normalized payment, A7 envelope
  comparison, finite M31 ledger reduction, Grand MCA theorem, or Grand list
  theorem is proved.
- No stable TeX source is changed.

## Verification coverage

Run

```text
/Users/danielcabezas/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  experimental/scripts/verify_a6_full_support_zero_boundary.py
```

The verifier uses exact integer and prime-field arithmetic.  It:

1. exhausts bounded admissible parameter tuples and checks all three formulas
   in (29), every equality endpoint, and the exact equivalence (11);
2. verifies that zero-denominator full-support points with `q_M<M` force
   `kappa=1`, and checks explicit examples of both equality faces and both
   strict walls;
3. computes generalized weights of several small weighted-RS direction
   extensions by exhaustive shortening and checks every fixed-zero-mask
   dimension bound; and
4. runs deliberate tamper checks against a falsified parameter record, a
   falsified generalized-weight sequence, and a family violating the
   right-angle hypothesis.
