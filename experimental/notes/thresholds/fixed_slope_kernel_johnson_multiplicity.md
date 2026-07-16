# Fixed-slope kernel-Johnson multiplicity compiler

## Status, object, and ownership

- **Status:** `PROVED / AUDIT` for the fixed-slope theorem below.
- **A6 status:** `PROVED` conditional only on the same named
  characteristic-free Noether-form input already consumed by
  `a6_all_witness_line_section_compiler.md`.  This packet introduces no new
  literature dependency.
- **Lane:** asymptotic hard input 3, the residual ray compiler for
  higher-dimensional balanced cores.
- **Counted object:** distinct completed `(slope,error)` pairs, equivalently
  distinct `(slope,codeword)` pairs.  No witness selector is applied.
- **Formal status:** the companion Lean modules prove the reusable finite
  set-system Johnson inequality, the direct fixed-syndrome theorem, and the
  fixed-slope hosted-pair specialization without `sorry`; the product bound is
  unconditional and only the quotient is positivity-gated.

The source A6 compiler bounds the projection to distinct slopes.  This note
supplies the previously missing intermediate-image multiplicity: the number
of distinct completed errors, or explaining codewords, above one fixed slope.
The two owners compose because slope fibers partition the pair set.

There is one important boundary.  The global source projection is

```text
(gamma,S,h) -> (gamma,h) -> gamma.
```

The theorem below bounds distinct `h`, equivalently distinct errors
`e=r_0+gamma r_1-h`, at fixed `gamma`.  It does **not** count repeated raw
support labels `S` for the same `(gamma,h)`.  Thus it closes the completed
pair/codeword gap at the intermediate image.  The source note's broader
raw-witness multiplicity nonclaim remains: no raw `(gamma,S,h)` incidence
bound is asserted.

The zero-mask inequality itself is an elementary Johnson bound already
present in punctured form in the neighboring direction-distance packet.  The
repository delta here is the unpunctured fixed-syndrome interface and its
cap-six composition with the A6 slope compiler, not a new Johnson inequality.

The exact source interfaces consumed below are:

- `experimental/notes/thresholds/a6_all_witness_line_section_compiler.md`,
  equations (1a), (18), (21)--(22), (26), and (34), together with its global
  `(gamma,S,h) -> (gamma,h) -> gamma` projection;
- `experimental/notes/thresholds/selector_free_direction_distance_all_pair.md`,
  Theorem 1 and equations (5)--(6), for the neighboring extension-code
  payment, and Theorem 4 with equations (16)--(18), for the closest punctured
  Johnson predecessor;
- `experimental/notes/thresholds/all_lineray_affine_core_set_pair.md`,
  equations (3)--(5), for the neighboring complete-pair affine-core payment;
  and
- `experimental/notes/thresholds/fixed_deficiency_complete_absorption.md`,
  equation (4), for the universal top-binomial comparison.

## 1. Exact fixed-syndrome theorem

Let `F` be any field, let `D subset F` contain `N` distinct points, and choose
nonzero weights `lambda_x`.  Put

```text
h_x=lambda_x(1,x,...,x^(R-1))^T,
H(e)=sum_(x in D)e_x h_x,
N=R+kappa,             R>=1,       kappa>=1.             (1)
```

Every `R` columns of `H` are independent.  Hence

```text
K=ker H
```

is an `[N,kappa,R+1]` generalized Reed--Solomon code.  Fix `0<=t<=R` and
one syndrome `y in F^R`.  Let `P_y` be any finite set of distinct errors
satisfying

```text
H(e)=y,                wt(e)<=t             for e in P_y. (2)
```

In the syndrome-line application one takes

```text
y=y_gamma=y_0+gamma y_1
```

and `P_y` is the complete fiber of retained errors above the fixed slope
`gamma`.  Define

```text
s=N-t,
w=kappa-1,
J_K=s^2-Nw=(N-t)^2-N(kappa-1).                          (3)
```

### Theorem 1 (fixed-slope kernel-Johnson payment)

For every family (2),

```text
|P_y| J_K <= N(s-w)=N(R+1-t).                           (4)
```

Consequently, if

```text
J_K>0,                                                   (5)
```

then

```text
|P_y|
 <= floor(N(R+1-t)/J_K)
 = floor(
     N(R+1-t) /
     ((N-t)^2-N(kappa-1))
   ).                                                    (6)
```

The bound is field-independent, characteristic-free, uniform in `y`, and
valid for every subset left after first-match deletion.  It needs neither
transversality nor a slope selector.

The complete fixed-syndrome family is finite even when `F` is infinite.
Indeed, two different errors supported in the same set of size at most
`t<=R` would differ by a nonzero kernel word of weight at most `R`,
contradicting `d_min(K)=R+1`.  Thus every support carries at most one error,
and there are only finitely many supports.

## 2. Zero-zero agreement proof

Put

```text
M=|P_y|,       s=N-t,       w=kappa-1.
```

For every `e in P_y`, the zero set of `e` has size at least `s`.  Choose an
`s`-subset

```text
B_e subseteq {x in D:e_x=0}.                            (7)
```

If `e!=f` are in `P_y`, then

```text
H(e-f)=0,       e-f!=0.
```

The kernel distance gives `wt(e-f)>=R+1`.  Therefore `e` and `f` agree on at
most

```text
N-(R+1)=kappa-1=w                                      (8)
```

coordinates.  Common zeros are agreement coordinates, so

```text
|B_e intersect B_f|<=w.                                 (9)
```

For each `x in D` let

```text
r_x=|{e in P_y:x in B_e}|.
```

Double counting incidences and unordered pairs gives

```text
sum_x r_x=Ms,                                           (10)

sum_x binom(r_x,2)
 =sum_{unordered {e,f}} |B_e intersect B_f|
 <=binom(M,2)w.                                         (11)
```

Cauchy--Schwarz and `r_x^2=r_x+2 binom(r_x,2)` now give

```text
M^2 s^2
 =(sum_x r_x)^2
 <=N sum_x r_x^2
 <=N(Ms+M(M-1)w).                                      (12)
```

If `M=0`, (4) is immediate.  Otherwise divide (12) by `M` and rearrange:

```text
M s^2
 <=N(s+(M-1)w)
 =NMw+N(s-w),

M(s^2-Nw)<=N(s-w).                                     (13)
```

Finally,

```text
s-w
 =(N-t)-(kappa-1)
 =R+1-t,                                                (14)
```

which proves (4).  Under (5), integer division of (4) proves (6).

This proof is the elementary zero-incidence form of the Johnson argument.
No polynomial interpolation, algebraic closure, asymptotic estimate, or
finite-field averaging occurs in it.

## 3. Structural coincidence with section capacity

The all-parameter source theorem in
`a6_all_witness_line_section_compiler.md` uses

```text
a=N-t,       w=kappa-1,
J_sec=a^2-Nw.                                           (15)
```

Its equation (21) is therefore the literal identity

```text
J_sec
 =(N-t)^2-N(kappa-1)
 =J_K.                                                   (16)
```

The source equation (22) proves that its monomial family contains a
section-admissible tuple if and only if `J_sec>0`.  The same strict
inequality is exactly the positivity condition needed to divide the
fixed-slope kernel payment (4).

The identical denominator has two different proofs and two different jobs:

1. in the source compiler it is the surplus criterion that produces a
   polynomial **distinct-slope** bound; and
2. here it is the zero-mask Johnson margin that bounds the number of
   distinct completed errors/codewords above one slope.

No two owner denominators are multiplied.  What is multiplied is a bound on
the number of fibers by a uniform bound on the cardinality of each fiber,
using the exact disjoint union

```text
P = disjoint_union_(gamma in Z) P_gamma.                 (17)
```

## 4. General composition with the A6 section compiler

Adopt all hypotheses and notation of the transverse all-parameter extension
in `a6_all_witness_line_section_compiler.md`: one received syndrome line,
one active weighted-RS chart, `kappa>=2`, `0<=t<R`, actual completed
witnesses, the source transversality condition, and a section-admissible
tuple

```text
mu>=1,       L>=q>=1,       qw<=D<mu(N-t).               (18)
```

Let `Z` be its set of retained slopes and let `P` be the complete set of
distinct retained `(slope,error)` pairs.  Source equation (18) gives

```text
|Z| <= U_sec,

U_sec
 = L + qL(12D^6+1) + q
   + floor(q(L+1)rho(t,d)),                              (19)
```

where `d` and `rho(t,d)` are exactly those defined in source equations
(17)--(18).  Section admissibility implies `J_sec>0` by source equations
(21)--(22).  Applying Theorem 1 to every fixed-slope fiber in (17) gives the
general pair compiler

```text
|P|
 <= floor(N(R+1-t)/J_sec) U_sec.                         (20)
```

This corollary preserves every hypothesis and every dependency of the source
slope theorem.  The kernel-Johnson factor itself is unconditional under the
weighted-RS hypotheses (1)--(2).

## 5. Canonical fixed-direction A6 cap

Use the canonical source parameters

```text
r>=1,
N=500r,       kappa=225r,       R=275r,
t=150r,       a=N-t=350r,       d=250r.                 (21)
```

Then

```text
J_sec=J_K
 =(350r)^2-500r(225r-1)
 =10000r^2+500r
 =500r(20r+1)>0,                                        (22)

N(R+1-t)
 =500r(125r+1).                                         (23)
```

Hence the fixed-slope cap is

```text
floor(N(R+1-t)/J_sec)
 =floor((125r+1)/(20r+1))
 =6.                                                     (24)
```

The last equality is exact for every `r>=1` because

```text
6(20r+1)<=125r+1<7(20r+1).                              (25)
```

Source equations (1a) and (26) give, on one fixed received line and one
fixed active chart,

```text
|Z| <= 1165+3744D_r^6,

D_r=floor((489950r-1372)/350)+1.                        (26)
```

Combining (24), (26), and the slope partition (17) yields

```text
|P|
 <=6(1165+3744D_r^6)
 =6990+22464D_r^6.                                      (27)
```

This is a polynomial bound for every distinct completed pair on the
canonical fixed-direction A6 line/chart, including all same-slope
codeword multiplicity.  It closes the source note's explicit multiplicity
nonclaim at the `(gamma,h)` intermediate image.

## 6. Global line-uniform A6 corollary

The global section-positive cell in the source note has a different scope.
It represents the complete exact support-wise bad-witness object for every
received pair, makes the one-cell first-match order automatic, and pays the
distinct-slope projection uniformly in the received line.  Its canonical
equation (34) is

```text
|Z_a(r)| <= 3744D_r^6+47700r+688                        (28)
```

for `n=500r`, `k=225r`, and `a=350r`.

Let `P_a(r)` denote the corresponding set of distinct completed
`(gamma,h)` codeword pairs, or equivalently the distinct
`(gamma,error)` pairs

```text
e=r_0+gamma r_1-h.
```

At fixed `gamma`, distinct `h` give distinct `e` with the same syndrome, so
(24) applies.  Therefore, for every received line on the source global cell,

```text
|P_a(r)|
 <=6|Z_a(r)|
 <=22464D_r^6+286200r+4128.                             (29)
```

Equation (29) is line-uniform and uses the global source cell.  Equation
(27) is the smaller fixed-direction/fixed-chart bound using the sharper
source factor `rho(t,d)=5/2`.  Neither statement counts different raw support
labels `S` attached to one already counted `(gamma,h)`.

## 7. Relation to neighboring all-pair payments

The distinction from
`selector_free_direction_distance_all_pair.md` is load-bearing.  Its
high-direction Theorem 1 places the whole pair family in a ball of the
extension code

```text
K+<b_1>,
```

whose minimum distance is the direction distance `d<=R`.  On canonical A6,
`d=250r` and its denominator is

```text
D_H
 =(350r)^2-500r(500r-250r)
 =-2500r^2<=0.                                          (30)
```

Thus that all-slope branch does not pay this row.  After fixing one slope,
differences lie in `K` itself, whose distance is `R+1=275r+1`; the common
zero cap improves from `N-d=250r` to `kappa-1=225r-1`, producing the positive
margin (22).  This note is a fixed-fiber complement to the selector-free
direction theorem, not a replacement for it.

The closest combinatorial predecessor is Theorem 4 of that packet.  Under the
formal substitution

```text
(M_punct,rho,Delta)=(N,t,R+1),
```

its denominator `D_J` becomes `J_K` and its equation (17) becomes (6).
This is not a literal theorem specialization: the predecessor constructs
`M_punct=N-d` by puncturing a nonzero syndrome direction with `d>=1`,
whereas Theorem 1 here works directly in an unpunctured `N`-coordinate
coset at an arbitrary fixed syndrome.

The theorem in `all_lineray_affine_core_set_pair.md` already counts every
same-slope pair when the actual affine-core rank is small.  The present
payment requires no a priori affine-rank estimate on `J_K>0`; when it gives
a constant cap, it consequently forces constant affine dimension.
Conversely, the affine-core theorem can work where `J_K<=0`.  Neither
subsumes the other.

There is also prior sharpness calibration in
`first_beyond_half_kernel_pencil.md`.  Its `F_7` example has
`N=7`, `R=3`, `kappa=4`, and `t=2`, so

```text
J_K=4,       floor(N(R+1-t)/J_K)=floor(14/4)=3.
```

The exhibited same-slope multiplicity is exactly three.  This calibrates the
fixed-syndrome constant sharply in a small case; it is not a duplicate of the
general per-fiber theorem or the canonical A6 composition.

The universal theorem in `fixed_deficiency_complete_absorption.md` gives, on
the canonical A6 parameters where `2t-R=25r`,

```text
|P|<=binom(500r,25r+1).                                  (31)
```

It needs none of the source interpolation hypotheses but is exponential in
this positive-linear-deficiency slice.  Equation (27) is stronger only
because it consumes the specialized A6 distinct-slope compiler.  No smaller
universal top-binomial theorem is claimed.

## 8. Verification and formalization

The deterministic standard-library verifier and pinned certificate are

```text
experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py
experimental/data/certificates/fixed-slope-kernel-johnson-multiplicity/
  fixed_slope_kernel_johnson_multiplicity.json
```

They independently recompute the zero-mask incidence ledger on exact small
weighted-RS fixed-syndrome fibers, the product inequality (4), the positivity
gate, the exact canonical cap (22)--(25), both A6 compositions (27) and (29),
and the certificate digest.  The tamper suite mutates theorem arithmetic,
the A6 parameters, source-bound constants, scope tags, and the digest.

Run

```bash
python3 experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py --check
python3 -O experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py --check
python3 experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py --tamper-selftest
python3 -O experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py --tamper-selftest
python3 -m json.tool experimental/data/certificates/fixed-slope-kernel-johnson-multiplicity/fixed_slope_kernel_johnson_multiplicity.json
PYTHONPYCACHEPREFIX=/tmp/fixed-slope-kernel-johnson-pycache python3 -m py_compile experimental/scripts/verify_fixed_slope_kernel_johnson_multiplicity.py
```

The Lean proof surfaces are

```text
experimental/lean/grande_finale/GrandeFinale/
  SetSystemJohnson.lean
  FixedSlopeKernelJohnsonMultiplicity.lean
```

with the isolated check

```bash
(cd experimental/lean/grande_finale &&
  lake env lean -DwarningAsError=true GrandeFinale/SetSystemJohnson.lean &&
  lake env lean -DwarningAsError=true \
    GrandeFinale/FixedSlopeKernelJohnsonMultiplicity.lean)
```

`SetSystemJohnson.lean` proves the incidence identities, the multiplicative
Johnson inequality, and its positive-denominator quotient form for a finite
constant-block family.  `FixedSlopeKernelJohnsonMultiplicity.lean` proves the
zero-set cardinality and truncation lemmas, shows that distinct errors in one
fixed-syndrome family differ by a nonzero kernel word, obtains the `kappa-1`
common-zero cap, and instantiates the abstract Johnson theorem.  Its direct
declaration

```text
fixedSyndromeKernelJohnsonMultiplicity
```

formalizes Theorem 1: equation (4) is unconditional, while equations (5)--(6)
form the second, positivity-gated conclusion.  On `J_K>0` the natural-number
subtractions are literal.  If the signed source denominator is negative, Lean's
natural denominator truncates to zero and records the corresponding automatic
product inequality; no quotient cap is claimed there.  The application
declaration

```text
fixedSlopeKernelJohnsonMultiplicity
```

proves the corrected proposition `fixedSlopeKernelJohnsonMultiplicityTarget`.
This is the hosted-pair line interface used by the A6 composition:
`BasicPairHypotheses` includes the nonzero line direction and the common
affine-syndrome equations.  It likewise leaves the product inequality
unconditional and gates only division.  The modules print the axioms of their
principal results; the audit contains no `sorryAx`.

## 9. Nonclaims

This note does not:

- count the number of retained slopes without a separate source theorem;
- count repeated raw support labels `S` for one completed
  `(gamma,h)` pair;
- prove the A6 interpolation/Noether slope bound or remove its named
  literature dependency;
- multiply independent owner denominators or claim an injection between
  unrelated paving, locator, and kernel-basis ledgers;
- pay the `J_K<=0` or `J_sec<=0` locus;
- prove a witness-exhaustive atlas outside the source global
  section-positive cell;
- aggregate arbitrary charts, profiles, received lines, or first-match cells
  beyond the exact source compositions (20), (27), and (29);
- prove interior distinct-slope sharpness, a growing-deficiency theorem, an
  unsafe-side lower reserve, or a target crossing;
- alter a deployed KoalaBear or Mersenne-31 row, Grand MCA, Grand List, or
  either prize question;
- transfer counts between generated, line, challenge, extension, or list
  fields;
- change any stable paper TeX or PDF; or
- claim Lean certification for the source interpolation/Noether slope
  compiler, the global atlas, or any full deployed-row closure.
