# Triple-negative first-match reduction: one wall, two complete charges

## Status and exact delta

```text
Arithmetic status: PROVED, including a zero-sorry Lean 4.28 proof.
Counting status: PROVED by composition of existing complete-pair theorems.
Routing status: REDUCTION / AUDIT, not a full first-match owner theorem.
Counted object: distinct retained (slope,error) pairs, including same-slope
multiplicity; never raw support labels attached to an already counted pair.
```

The apparent residual chamber

```text
D_H <= 0,       D_J <= 0,       J_K <= 0                 (1)
```

is not a three-way parameter region.  Under the standard weighted-RS
hypotheses, `J_K<=0` forces both older denominators to be *strictly* negative.
Thus (1) is exactly the single wall `J_K<=0`.

This does not make the sign wall a semantic first-match cell.  It says only
that three spherical/Johnson payments fail together.  Actual ownership still
depends on the surviving profile and on which earlier quotient, planted,
common-support, curve, low-rank, or other owner has already fired.

The second delta is a first-match-safe synthesis.  On `J_K<=0`, the complete
fixed-deficiency theorem always applies, and over a finite field it can be
minimized with the complete paving-basis charge.  These charges are not
multiplied.  They do not dominate one another.

The fixed-slope theorem that introduced `J_K` is pending upstream PR `#817`.
The arithmetic reduction here is standalone and does not vendor or assume the
integration of that packet.  It consumes the pending result only to interpret
`J_K>0` as the neighboring fixed-slope payment.

## 1. Parameters and the three denominators

Let

```text
N=R+kappa,        0<=t<R,        1<=d_dir<=R,
M=N-d_dir,        Delta=R-d_dir+1,
rho=min(t,M),     a=N-t.                                  (2)
```

Here `d_dir` is the minimum direction-coset distance.  It must not be confused
with the beyond-half deficiency

```text
delta=2t-R.                                               (3)
```

Put

```text
D_H=a^2-NM,
D_J=(M-rho)^2-M(kappa-1),
J_K=a^2-N(kappa-1).                                      (4)
```

The first two expressions are exactly the high-direction and punctured
Johnson denominators in
`selector_free_direction_distance_all_pair.md`.  The last is the direct
fixed-syndrome kernel denominator of pending PR `#817`.

## 2. Denominator nesting theorem

### Theorem 1 (the triple signs collapse)

Under (2)--(4),

```text
D_H<=0 and D_J<=0 and J_K<=0
    iff
J_K<=0.                                                   (5)
```

More sharply, if `J_K<=0`, then

```text
D_H <= -N Delta <= -N < 0,                               (6)
```

and

```text
D_J <= -d_dir(R-t+1) < 0          when M>=t,
D_J <= -kappa(kappa-1) < 0        when M<t.               (7)
```

Consequently neither older zero boundary meets this chamber.  Equivalently,

```text
D_H>0  ==> J_K>0,
D_J>0  ==> J_K>0.                                       (8)
```

### Proof

The high-direction denominator has the exact nesting

```text
D_H=J_K-N(R-d_dir+1)=J_K-N Delta.                        (9)
```

Since `Delta>=1`, equation (6) follows immediately.

For the punctured denominator, split only on the definition of `rho`.
If `M>=t`, then `rho=t` and direct expansion gives

```text
D_J=J_K-d_dir(M-delta+1).                               (10)
```

Moreover

```text
M-delta+1=(M-t)+(R-t)+1 >= R-t+1 >=2.                   (11)
```

This proves the first arm of (7).  If `M<t`, then `rho=M`, so

```text
D_J=-M(kappa-1).                                        (12)
```

Because `d_dir<=R`, one has `M=N-d_dir>=N-R=kappa`.
Section 3 shows that `J_K<=0` forces `kappa>=2`, and the second arm of (7)
follows.  The reverse implication in (5) is tautological because its left
side already contains `J_K<=0`.

## 3. Depth--deficiency normal form

Put

```text
g=R-t>=1,        h=g-1=R-t-1.                            (13)
```

The number `h` is the identity-prefix depth `a-kappa-1`.  It is deliberately
not called `w`, because the neighboring fixed-slope packet uses `w=kappa-1`
for a different quantity.

The parameter identities are

```text
R=delta+2g,
N=kappa+delta+2g,
a=kappa+g,
N-(delta+1)=kappa+2g-1.                                 (14)
```

The last expression is also

```text
N-(delta+1)=a+h=2a-kappa-1.                             (14a)
```

Two exact normal forms for the surviving denominator are

```text
J_K=t^2-N(delta-1)
   =(g+1)^2-(kappa-1)(delta-1).                          (15)
```

Hence

```text
J_K<=0
  iff (kappa-1)(delta-1)>=(g+1)^2.                       (16)
```

Since the right side is positive, (16) forces

```text
kappa>=2,        delta>=2.                               (17)
```

Also `delta<t` is equivalent to `t<R`, already assumed.  Therefore every
point of the sign chamber lies strictly beyond half distance with

```text
2<=delta<t.                                              (18)
```

The boundary is the exact factor equation

```text
(kappa-1)(delta-1)=(g+1)^2.                              (19)
```

It contains both puncture branches even at positive depth.  For example,

```text
(N,R,kappa,t,g,h,delta)=(12,8,4,6,2,1,4)
```

has `J_K=0`.  Taking `d_dir=1` gives `M>=t`, while taking `d_dir=8`
gives `M<t`; in both cases `D_H,D_J<0`.

## 4. Complete-pair charge on the single wall

Let `P` be any finite complete family of distinct transverse
`(slope,error)` pairs in the weighted-RS chart, with every error of weight at
most `t`.  An earlier first-match deletion may already have restricted `P`.

### 4.1 Fixed-deficiency charge

Equations (3) and (18) put the parameters exactly in the theorem of
`fixed_deficiency_complete_absorption.md`, with that note's deficiency `d`
renamed `delta` here.  For every field,

```text
|P| <= binom(N,delta+1).                                 (20)
```

Using (14a), the same cap may be written

```text
binom(N,delta+1)=binom(N,a+h)=binom(N,2a-kappa-1).       (20a)
```

This is a domain-wide complete-pair cap.  It already includes same-slope
multiplicity and remains true after arbitrary first-match deletion.

### 4.2 Paving-basis charge

Over a finite field, retain the notation of
`all_pair_paving_basis_multiplicity_compiler.md`.  Let

```text
A=[b_0 b_1 G]
```

be the augmented lift/kernel matrix, and let `beta_(kappa+1)(A)` be its
number of full-rank `(kappa+1)`-row subsets.  Define

```text
Lambda_(d_dir,t)
 =max{
    binom(N-t-1,kappa),
    ceil((d_dir-t)_+ binom(N-t,kappa)/(kappa+1))
  }.                                                      (21)
```

The existing complete-pair paving theorem gives

```text
|P|
 <= floor(beta_(kappa+1)(A)/Lambda_(d_dir,t))
 <= floor(binom(N,kappa+1)/Lambda_(d_dir,t)).             (22)
```

When `d_dir=R`, its deep-hole strengthening is

```text
|P| <= floor(
  binom(N,kappa+1)/binom(N-t,kappa+1)
).                                                        (23)
```

### 4.3 The valid synthesis is a minimum

Combining (20) and (22) gives

```text
|P| <= min{
  binom(N,delta+1),
  floor(beta_(kappa+1)(A)/Lambda_(d_dir,t))
}.                                                        (24)
```

The two charges arise from different ownership ledgers.  They are minimized,
not multiplied.  Even at positive depth inside `J_K<=0`, neither dominates:

```text
(N,R,kappa,t,d_dir)=(17,6,11,4,1):
  fixed deficiency 680, paving 515;

(N,R,kappa,t,d_dir)=(22,6,16,4,1):
  fixed deficiency 1540, paving 1549.                    (25)
```

These are exact formula calibrations, not attainment claims.

## 5. What (20) already pays asymptotically

On any sequence in `J_K<=0`, equation (20) is subexponential in each of three
large regions.

1. If `delta=o(N)`, then

   ```text
   log binom(N,delta+1)=o(N).                             (26)
   ```

2. If `R=o(N)`, then `0<delta<t<R`, so this is a subcase of (26).

3. If `kappa=o(N)`, equation (16) gives

   ```text
   (g+1)^2 <= (kappa-1)(delta-1) <= kappa N,
   ```

   so `g=o(N)`.  By (14), the complementary binomial index satisfies

   ```text
   N-(delta+1)=kappa+2g-1=o(N),                          (27)
   ```

   and (20) is again `exp(o(N))`.

The depth-zero boundary is `h=0`, equivalently `g=1` or `R=t+1`.
`depth_zero_identity_lineray_owner.md` proves the stronger profile statement

```text
|P|<=binom(N,a)=barN_1                                  (28)
```

with constant one.  The canonical Lagrange route cut

```text
N=2m+1,       R=m+1,       t=kappa=m,       d_dir=R
```

lies in `J_K<0` for `m>=4` and attains

```text
|P|=binom(2m+1,m)=binom(N,delta+1).                      (29)
```

It is exponential but exactly identity-owned; it is not an unowned
obstruction.

Consequently, on a subsequence where (20) retains positive exponential rate,
any residual not paid by this route must have

```text
h>=1,       kappa=Omega(N),       delta=Omega(N).         (30)
```

This is a rate-compact, positive-depth reduction.  It is not a claim that
`h` has linear density, or that every point satisfying (30) survives the
earlier owners.

## 6. Why the sign reduction is not an ownership theorem

The first-match atlas assigns a surviving *profile* to its earliest semantic
owner.  A denominator sign has no quotient, planted, common-support,
curve/pencil, affine-core, or primitive-survival data.  In particular:

- paid exact-weight `Xi_j` or `Q_j` strata may lie inside this sign chamber;
- sublinear global affine rank, or a sublinear-rank selector together with
  uniformly sublinear same-slope ranks, is already paid by
  `all_lineray_affine_core_set_pair.md`;
- locator curves and split pencils may be paid even when a spherical
  denominator is negative; and
- depth zero is already paid by (28).

There is also no absolute owner-free subexponential theorem on all of
`J_K<=0`.  `one_deeper_prefix_anti_host_compiler.md` constructs positive-depth
families with exponentially many exact slopes at the realized identity-image
scale and `J_K<0`.  That note explicitly does **not** prove survival through
every earlier first-match owner, which is exactly the distinction preserved
here.

The principal sharpness and routing families line up as follows.

| family | parameters on the wall | exact routing information |
|---|---|---|
| depth-zero Lagrange route cut | `h=0`, `J_K<0`, complete count `binom(N,delta+1)` | already paid exactly by the depth-zero identity owner |
| twin-pair planted prefix (`heavy_fiber_planted_emission.md`) | `N=2B`, `a=t=B`, `kappa=B-2`, `h=1`, `J_K=B(6-B)<0` for even `B>=8` | emits quotient, one planted template, and saturation precursors; emission is not a completed atlas payment |
| characteristic-two pole / anti-host | `J_K=(h+2)^2-(kappa-1)(delta-1)<0` asymptotically | the pole family is a degree-one rational host; the one-deeper anti-host escapes that host range but does not certify survival of every other owner |

Thus the wall contains both already-routed and not-yet-routed objects.  The
table is a routing audit, not a three-family exhaustion theorem.

The narrow local residual is therefore the one already isolated by the
paving and affine-core packets:

> For one positive-depth, primitive first-match profile in `J_K<=0`, after
> exact-weight, sublinear-deficiency, curve/pencil, low-rank affine-core, and
> earlier semantic owners have been removed, prove
>
> ```text
> beta_(kappa+1)(A_lambda)/Lambda_(d_lambda,t_lambda)
>   <= exp(o(N))(1+barN_lambda),                          (31)
> ```
>
> or route the whole corresponding pair fiber to a named earlier owner.

Equivalently, the remaining atom is basis-heavy and has neither a low-rank
transversal nor uniformly low-rank same-slope fibers.  It needs an inverse
step extracting a common flat/low-degree locator family, or a genuinely new
polynomial-value/beyond-Johnson input.  Another mask-by-mask Johnson count
cannot distinguish it.

Statement (31) is local to one received line/profile.  Claiming that it covers
every survivor, or summing it uniformly over profiles and received lines,
would additionally require the witness-exhaustive atlas and profile add-back.
Neither is supplied here.

## 7. Verification and formalization

The standard-library verifier and pinned strict-JSON certificate are

```text
experimental/scripts/verify_triple_negative_first_match_reduction.py
experimental/data/certificates/triple-negative-first-match-reduction/
  triple_negative_first_match_reduction.json
```

Run

```bash
python3 experimental/scripts/verify_triple_negative_first_match_reduction.py --check
python3 -O experimental/scripts/verify_triple_negative_first_match_reduction.py --check
python3 experimental/scripts/verify_triple_negative_first_match_reduction.py --tamper-selftest
python3 -O experimental/scripts/verify_triple_negative_first_match_reduction.py --tamper-selftest
python3 -m json.tool experimental/data/certificates/triple-negative-first-match-reduction/triple_negative_first_match_reduction.json
```

The verifier recomputes every identity and strict sign implication on all
`3,412,800` valid tuples with `N<=80`.  Exactly `892,834` have `J_K<=0`,
including both `rho` branches and positive-depth boundary points; no sign
exception occurs.  It also checks the noncomparison (25), the sharp
depth-zero family through `m=12`, positive-depth sign stress through `N=80`,
source anchors, payload digest, and ten independent tamper mutations.

The Lean 4.28 module is

```text
experimental/lean/grande_finale/GrandeFinale/
  TripleNegativeFirstMatchReduction.lean
```

It proves the polynomial normal forms and both puncture branches over the
integers with no `sorry`, then derives the strict sign collapse and forced
`kappa,delta` region.  It formalizes the new arithmetic theorem, not the
already-proved external counting theorems (20) and (22).

## 8. Nonclaims

This packet does not:

- declare `J_K<=0` to be a semantic first-match cell;
- prove an owner-free polynomial or subexponential bound on the whole wall;
- assert that any displayed construction survives quotient, planted,
  common-support, curve, rational-host, or other earlier owners;
- multiply unrelated Johnson, paving, locator, or profile denominators;
- count repeated raw support labels for one completed pair;
- prove a witness-exhaustive atlas, primitive survival, profile add-back, or a
  uniform received-line theorem;
- move a deployed finite row, prove an unsafe-side reserve or adjacent
  crossing, or alter Grand MCA, Grand List, or either prize question;
- alter stable paper TeX/PDF; or
- treat pending PR `#817` as integrated.
