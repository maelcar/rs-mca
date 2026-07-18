# Route-D marked RIM all-maximal-minors adapter v1

STATUS: COUNTEREXAMPLE

## Result

This packet separates two statements that must not be conflated in the
CAP25-v13 KoalaBear-MCA row-sharp-Q Route-D lane.

1. For an **actual marked residual incidence**, vanishing of every maximal
   minor of the field-native Hankel matrix is exactly rank drop.  This is the
   type-correct route into the existing `DEEP_MCA_RANK_DROP` owner, and it
   carries the common-core mark unchanged.
2. Vanishing of one selected maximal minor is not rank drop.  More strongly,
   an exact `F_31` corpus has 99 projectively primitive, distinct-core marked
   representatives in one primitive target slice, all with the same
   full-rank field-native pivot.  Thus the pre-deletion arbitrary-Q marked
   representative interface exceeds both toy capacities `3*31=93` and
   `3*30=90`.

The second statement is a counterexample/new obstruction floor, not a
counterexample to the deployed bound.  The eight named first-match deletions
are not executable in this packet, so no conclusion is drawn about the
post-deletion KoalaBear target.

## 1. Exact all-maximal-minors adapter

Let `F` be a field and let `M` be a `t x m` matrix with `1 <= t <= m`.  For a
`t`-element column set `J`, write `M[J]` for the corresponding square
submatrix.

**Theorem 1 (all-maximal-minors criterion).**

```text
rank_F(M) < t  iff  det(M[J]) = 0 for every t-element column set J.
```

Proof.  The rank of a matrix is the largest order of a nonzero minor.  Since
`M` has `t` rows, it has full row rank exactly when at least one order-`t`
minor is nonzero.  Negating this statement gives the displayed equivalence.

Now fix an actual marked residual incidence

```text
I = (z, G, kappa, f, g, gamma, S, T),
```

where `z` is the fixed primitive target, `G` is the common-core mark, `kappa`
contains every other carried first-match key, `gamma` is an actual finite
noncontained MCA-bad slope at agreement `A`, and

```text
M_A(gamma) = H_{t,j}(Syn(f + gamma*g)).
```

The existing field-native owner uses

```text
Z_2_env(f,g) = Bad_A(f,g) intersect
               {gamma : rank_F M_A(gamma) < t}.
```

**Corollary 2 (type-correct owner route).**  On this actual-incidence domain,

```text
all maximal minors of M_A(gamma) vanish
  iff rank_F M_A(gamma) < t.
```

In the vanishing case `gamma` lies in `Z_2_env(f,g)` and is routed to
`DEEP_MCA_RANK_DROP`.  The routing map changes no component of `(z,G,kappa)`.
The imported owner counts the distinct slope once; this packet does not
recharge it per support, core, minor, or chart.

Actual incidence is load-bearing.  Raw algebraic rank drop is not accepted by
the owner.  Likewise, the least nonzero support-quotient coordinate `h_*` from
the field-native finite-pivot adapter is not a maximal rank minor: `h_*`
always exists on the actual finite noncontained locus, whereas every maximal
minor vanishes precisely on the rank-drop locus.

### A singleton-minor counterexample

Over every field, take

```text
M = [[1,0,0],
     [0,0,1]].
```

The minor in columns `(0,1)` is zero, but the minor in columns `(0,2)` is one,
so `rank(M)=2`.  Consequently a theorem that routes the vanishing of one
preselected maximal minor into `DEEP_MCA_RANK_DROP` is false.

## 2. Minimal-seam marked signed-moment reconstruction

There is a positive large-defect transfer once the missing datum is carried.
Let `U,V` be `r`-element side supports over a field whose characteristic does
not divide `r`.  Assume their first `r-1` **locator coefficients** agree, and write

```text
L_U(X) = X^r - e_1 X^(r-1) + ... + (-1)^r e_r(U),
L_V(X) = X^r - e_1 X^(r-1) + ... + (-1)^r e_r(V).
```

Thus the displayed lower coefficients are common.  Equality of the first
`r-1` power sums is an equivalent sufficient hypothesis when the
characteristic is zero or greater than `r`; that extra characteristic gate is
not silently assumed here.  In the marked-incidence application, division of
the carried full locators by the carried common-core locator `G` supplies the
common side coefficients by triangular deconvolution.  Carry a marked root
`y in U` and the signed residual moment

```text
m_r = P_r(U) - P_r(V).
```

**Theorem 3 (marked minimal-seam reconstruction).**  The data

```text
(common depth-(r-1) prefix, y, m_r)
```

determine the ordered pair `(L_U,L_V)` uniquely.  If a common-core locator
`G` is also carried, they determine the ordered parent pair
`(G*L_U,G*L_V)` without discarding the mark.

Proof.  The common elementary coefficients recursively give common lower
power sums without division.  Substituting `y` into `L_U` determines
`e_r(U)`.  Subtracting the
degree-`r` Newton identities gives

```text
e_r(U) - e_r(V) = (-1)^(r+1) * m_r / r.
```

Hence `e_r(V)` and both monic locators are determined.  Multiplication by the
carried `G` reconstructs the parents.

This uses the first missing signed moment at the minimal seam.  It is not a
low-moment-only, mode-at-null, image-only, or zero-defect argument.

## 3. Primitive-parent diagonal cross-section

Let a group `H` act on packets and equivariantly on their targets.  Fix a
target `z` with trivial stabilizer in `H`.

**Theorem 4 (fixed-target cross-section).**  Every `H`-orbit meets a fixed-`z`
packet slice in at most one packet, even after intersecting that slice with an
arbitrary predicate `Q`.

Indeed, if `eta=h*xi` and both targets equal `z`, equivariance gives
`h*z=z`; triviality of the stabilizer forces `h=1`, hence `eta=xi`.  The proof
does not require `Q` to be invariant.  Because equality is equality of full
packets, the common-core mark `G` and every carried key remain unchanged.

This theorem is an injective cross-section statement, not an orbit payment.
It neither asserts that a child stabilizer acts freely nor permits division by
its order.

## 4. Exact `F_31` marked full-rank obstruction

Work over `F_31` on `D=F_31^*` with

```text
k=12, A=15, j=15, t=3, w=2,
E={1,2,3}, f=1_E, g(x)=x^12, gamma=0,
B={1,2,3,4,5,7,10,11,12,18,19,20,21,26,28}.
```

For a support `S`, use the depth-two locator prefix

```text
Phi_2(S)=(-sum(S), sum_{x<y in S} x*y).
```

The base target is

```text
z=Phi_2(B)=(30,9).
```

It is primitive under diagonal scaling because its first coordinate is
nonzero, so Theorem 4 applies to the fixed parent slice.  Mark `b=1`.  Signed deconvolution gives the child target

```text
delta_1(z)=(0,9),
```

whose scalar stabilizer is the nontrivial subgroup `H={1,30}={+1,-1}`.
Nevertheless the fixed parent-target slice is a genuine diagonal-orbit
cross-section: if `h*z=z`, then `30h=30`, hence `h=1`.  The child subgroup
cannot be divided out after silently forgetting the parent target and mark.

Enumerate

```text
T=(B minus R) union A_plus,
R subset B minus E,
A_plus subset D minus B,
|R|=|A_plus|=3,
Phi_2(T)=z.
```

The deterministic enumeration gives:

```text
all mates                                      121
projectively primitive signed defects          119
distinct common cores among those defects       99
```

Here the signed defect is `mu=1_{A_plus}-1_R`.  Projective primitivity means
that

```text
h*mu = +mu or h*mu = -mu
```

has only the identity solution `(h,+)=(1,+)`.  The common core
`G=B minus R` is retained as part of every packet.  Selecting one packet for
each of the 99 distinct `G` gives

```text
99 > t*p     = 3*31 = 93  by 6,
99 > t*(p-1) = 3*30 = 90  by 9.
```

Thus even the toy label space `{0,1,2} x F_31` is too small, before named
deletions, for an arbitrary-Q representative injection based on these data.
The nonzero-label space is smaller still.

### Actual-incidence and pivot checks

Every enumerated `T` contains `E`.  On the agreement support `D minus T`, the
zero codeword explains `f`; the function `x^12` cannot agree there with a
polynomial of degree less than 12 because there are 15 distinct agreement
points.  Hence `gamma=0` is an actual finite noncontained incidence for every
packet.

The actual error support is exactly `E`, of size `t=3`, and the standard
Vandermonde factorization gives

```text
rank_F31 M_A(0)=min(t,|E|)=3.
```

The verifier independently constructs `M_A(0)`.  Of its 560 maximal minors,
541 are nonzero; in particular it is not a rank-drop packet.

For `g=x^12`, the full-domain weighted syndrome is zero except at index 17,
where it is one.  Every monic size-15 co-support locator therefore gives

```text
B_T=(0,0,1),
least field-native pivot=(2,1).
```

All 121 packets have this same label.  For every mate, the side sets
`A_plus,R` have equal first and second power sums, their monic cubic locators
differ by a nonzero constant, and their third signed moment is nonzero.  Thus the
simple side weight does not extend its depth-two vanishing to degree three.
This packet does not identify that weight with the reduced multiplicity weight
used by the named `extension_slope` predicate and does not claim that deletion is
executable.

This corpus refutes the following pre-deletion claim:

```text
primitive target + actual noncontained incidence + projectively primitive
signed defect + common-core marking + one field-native pivot
  => arbitrary-Q marked representative injection into t field rows times F_p.
```

It does not refute a theorem after the exact named first-match deletions.

## 5. `F_17` reconstruction guard

Let `g=3` generate `F_17^*`, and encode supports by exponents modulo 16:

```text
S1={0,1,2,3,4,5,6,15},
S2={0,1,2,3,5,7,12,14}.
```

Both have size eight and depth-two locator target `(6,1)`.  That target is
primitive.  Neither support contains an antipodal exponent pair.  Folding
each antipodal pair `{e,e+8}` to a signed contact at `e in {0,...,7}`, both
supports have least signed contact `(0,+)` and defect magnitude eight, but
the supports are distinct.  Therefore target, least signed contact, and
defect magnitude do not reconstruct a primitive support.  The marked
signed-moment datum in Theorem 3 is genuine additional information.

## 6. Scope and ownership

What is proved here:

- the all-maximal-minors/rank-drop equivalence;
- the conditional, type-correct route from an actual marked incidence into
  the existing rank-drop predicate while carrying `(z,G,kappa)` unchanged;
- minimal-seam reconstruction after carrying the marked root and first
  missing signed moment;
- the primitive-parent fixed-target cross-section without an invariance
  hypothesis;
- the exact F31 and F17 obstruction fixtures.

What is not proved here:

- the deployed bound
  `|G_gen(z)|+|D_prim(z)| <= 67472*2130706433`;
- executable implementations of the eight named first-match deletions;
- an injection for nonvanishing marked representatives;
- a finite add-back over every signed-local-minority profile;
- that one selected minor controls rank;
- any new charge beyond the already existing distinct-slope rank-drop owner.

The next honest theorem is a deployed first-match adapter that constructs the
actual-incidence record from each marked Route-D survivor and then proves a
nonvanishing representative injection on the complement of the all-minors
rank-drop locus.  The F31 corpus must be deleted or multiplicity-paid by one
of those executable predicates.

## 7. Exact provenance

All repository references below are read at immutable commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- `experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md`,
  blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`, states the open primitive
  support certificate and the RIM specialization guardrail.
- `experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md`, blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`, supplies the carried weighted
  SP/Padé keys and the currently schematic `rim_rank_drop_pivot` route.
- `experimental/notes/thresholds/cap25_v13_lq_top_seam_marked_incidence.md`,
  blob `a7f2bf4f1338d0b31d999c86a29859317033113f`, proves that the common core is
  part of the counted marked incidence.
- `experimental/notes/m1/m1_kb_branch2_hankel_pivot_adapter_v1.md`, blob
  `0e1becd7ac2f66bf74c034ef0b8165d56cc1c471`, defines the field-native least
  nonzero quotient-coordinate pivot on actual noncontained incidences.
- `experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md`, blob
  `ddfce00907f34128b324a64041f4e0ec8957b7d3`, defines the actual-incidence
  rank-drop predicate and `DEEP_MCA_RANK_DROP` distinct-slope owner.
- `experimental/notes/thresholds/signed_local_minority_fixed_composition.md`,
  blob `376c21252b5ee167839c2d214f173428c0010ff4`, supplies the exact carried-offset
  signed folding identity on fixed occupancy profiles.
- `experimental/notes/roadmaps/marked_exclusion_cross_gram.md`, blob
  `4ed789595305170556371c87c5773d9e14ba4307`, supplies the exact marked
  cross-Gram reconstruction and records that actual-slope compilation remains
  open.
- `agents.md`, blob `2fea2bce6a348105f0016fcf739b5247bf408d93`,
  and the predecessor `experimental/agents-log.md`, blob
  `45b04597efb40741b807e48b290a0544f2fe6baf`, govern packet scope and logging.

## 8. Reproduction and formalization

Run the deterministic standard-library verifier with

```bash
python3 experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py
python3 experimental/scripts/verify_route_d_marked_rim_all_minors_adapter_v1.py --tamper
```

The standalone Lean companion is under

```text
experimental/lean/route_d_marked_rim_all_minors_adapter_v1/
```

It records theorem-shaped interfaces for the generic all-minors and
minimal-seam statements, together with kernel-checked matrix, F17, F31, and
capacity pins.  The exhaustive F31 corpus is certified by the Python verifier;
it is not presented as a kernel-evaluated Lean enumeration.
