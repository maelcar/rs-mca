# Route-D square-fold compatibility graph v1

STATUS: COUNTEREXAMPLE

## Result

The marked square-fold reconstruction

```text
(G,u,sigma) -> (S,T)
```

is lossless, but a transfer that erases the carried depth-two target is not
additive. Reconstructed parents are edges of a bipartite compatibility graph;
the two projected label sets alone need not pay those edges additively.

An exact `F_23` fixture realizes `K_(3,3)` after dropping the target `z`:
three valid even labels and three valid odd labels combine into nine primitive,
nonextension marked pairs, so

```text
9 = 3*3 > 3+3 = 6.
```

This is a target-erasure counterexample, not a fixed-target Route-D
counterexample. The verifier computes `z=(e_1(S),e_2(S))` for every pair and
checks `z(S)=z(T)`. Retaining `z` in both endpoint keys splits the fixture as

```text
K_(2,2) disjoint_union K_(2,1) disjoint_union
K_(1,2) disjoint_union K_(1,1),
```

which is a pseudoforest and admits a multiplicity-one endpoint assignment.
Thus the fixture does not refute a fixed-target additive transfer or the
deployed support bound; it proves that any folding transfer must preserve the
target key.

The sharp additive criterion remains graph-theoretic: a multiplicity-one
endpoint charge exists exactly when every compatibility component is a
pseudoforest. No existing quotient or rank owner supplies the required typed
endpoint maps. This packet constructs no actual incidence matrix, exhibits no
actual all-maximal-minors-vanishing pivot, and routes nothing to rank drop.

## 1. Exact marked reconstruction alphabet

Let `F` have odd characteristic, let `D subset F^*` be stable under negation,
and choose one root `x_y` of every square image `y`; its fiber is
`{x_y,-x_y}`. Write two marked supports as

```text
S=G disjoint_union A,
T=G disjoint_union B,
A intersect B=empty.
```

For `mu=1_A-1_B`, put

```text
a_y=mu(x_y),
b_y=mu(-x_y),
u_y=a_y+b_y,
sigma_y=a_y-b_y.
```

Because the off-core sides are disjoint, `a_y,b_y` belong to `{-1,0,1}`.
The exact per-fiber alphabet is

```text
(u_y,sigma_y) in {
  (0,0),
  (1,1), (1,-1), (-1,-1), (-1,1),
  (2,0), (-2,0), (0,2), (0,-2)
}.
```

Equivalently,

```text
u_y == sigma_y mod 2,
abs(u_y)+abs(sigma_y)<=2.
```

The inverse is

```text
mu(x_y) =(u_y+sigma_y)/2,
mu(-x_y)=(u_y-sigma_y)/2.                  (SF1)
```

Thus `(G,u,sigma)` reconstructs `(S,T)`: use `(SF1)` to recover the disjoint
off-core sides by sign and then adjoin the carried literal `G` to both. The
mark cannot be reconstructed from the defect because common-core additions
cancel.

If `|A|=|B|=r`, the exact global size constraints are

```text
sum_y u_y=0,
sum_y (u_y^2+sigma_y^2)=4r.                (SF2)
```

Indeed,

```text
|A|=(1/4) sum_y (u_y^2+sigma_y^2+2u_y),
|B|=(1/4) sum_y (u_y^2+sigma_y^2-2u_y).
```

These quadratic size constraints already couple the two channels; arbitrary
separately enumerated labels need not be jointly admissible.

## 2. Even and odd moment systems

For every nonnegative integer `h`, direct folding gives

```text
mu_(2h)   =sum_y u_y y^h,
mu_(2h+1) =sum_y sigma_y x_y y^h.           (SF3)
```

Changing `x_y` to `-x_y` negates `sigma_y` as well, so the odd summand is
orientation-independent. If the Route-D prefix equations are
`mu_k=0` for `1<=k<=w`, then the two child systems on the squared domain are

```text
E_h(u)=sum_y u_y y^h=0,
  1<=h<=floor(w/2),

O_h(sigma)=sum_y sigma_y x_y y^h=0,
  0<=h<=floor((w-1)/2).                     (SF4)
```

Equal side size supplies the omitted equation `E_0=0`. At the deployed
`w=67471`, `(SF4)` has `33735` printed even equations and `33736` odd
equations, exactly as in prefix-reduction commit
`e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
`591c91a6aac6b48db0c16abc586b74d7a51e44e2`.

Writing `v_y=sigma_y x_y` makes the odd equations ordinary moments in `y`,
but `v_y` belongs to the root-dependent alphabet
`{0,+-x_y,+-2x_y}` and remains locally coupled to `u_y`. It is not a Boolean
support on the quotient domain.

## 3. Exact `F_23` target-erasure fixture

Work over `F_23^*`. Use the following square roots:

```text
y    1  2  3  4  6  8  9  12 13 16 18
x_y  1  5  7  2 11 10  3   9  6  4  8.
```

Reserve the entire `y=13` fiber and carry the literal core

```text
G={6}.
```

Define three even labels, with every undisplayed coordinate zero:

```text
u_1: +2 on {1,4}, -2 on {2,3},
u_2: -u_1,
u_3: +2 on {1,6}, -2 on {3,4}.
```

Define three odd labels on disjoint square fibers:

```text
sigma_1: +2 on {8,9},  -2 on {12,16},
sigma_2: -sigma_1,
sigma_3: +2 on {9,12}, -2 on {16,18}.
```

Every `u_i` satisfies

```text
sum u_i=0,
sum u_i*y=0.
```

Every `sigma_j` satisfies

```text
sum sigma_j*x_y=0.
```

The even and odd coordinate pools are disjoint. Hence every one of the nine
pairs `(u_i,sigma_j)` obeys the exact local alphabet. Reconstruction gives
disjoint sides `A_(i,j),B_(i,j)` of size eight, both avoiding `G`; adjoining
`G` gives marked nine-subsets with common core exactly `G`. Their defect
moments satisfy

```text
mu_0=mu_1=mu_2=0.
```

The next odd moments for `sigma_1,sigma_2,sigma_3` are respectively

```text
8, 15, 15 mod 23,
```

so none is an extension or zero-defect degeneration. Exhaustive scalar/sign
testing shows all nine defects are projectively primitive.

The graph obtained after erasing the depth-two target is exactly `K_(3,3)`.
It has nine edges, six vertices, one component, and cyclomatic number

```text
9-6+1=4.
```

That projection is the counterexample: it has no multiplicity-one endpoint
assignment. It is not a graph inside one fixed target slice. For each marked
pair the verifier computes

```text
z=(e_1(S),e_2(S))=(e_1(T),e_2(T)) mod 23.
```

The exact target histogram is

```text
z=(6,7): 4 edges,
z=(6,2): 2 edges,
z=(6,5): 2 edges,
z=(6,0): 1 edge.
```

Putting `z` into both endpoint labels yields respectively `K_(2,2)`,
`K_(2,1)`, `K_(1,2)`, and `K_(1,1)`. Globally the tagged graph has nine
edges, twelve vertices, four components, and cycle rank one. Each component
is a pseudoforest, and exhaustive endpoint assignment succeeds. Therefore the
fixture refutes target erasure only; it does not refute a fixed-target
additive transfer or the deployed primitive support certificate. It remains a
raw algebraic route cut and does not execute unavailable named first-match
deletions.

## 4. Pinned precursor forest boundary

The pinned square-fold predecessor at commit
`f64e03a1215653eeafe3186df55269273d9f7653` (note blob
`301144d04458027131779907f7f74aa5a6682bf4`, verifier blob
`2507f09115c7eefbc86025dbaf204ea83c744283`, Lean blob
`ab061b3c53a320fbb8881bab4e6fa8e573f83248`) supplies the positive boundary.
On its exact 55 retained raw rows, the bipartite graph with left labels
`(G,u)` and right labels `(G,sigma)` has

```text
left vertices                         55,
right vertices                        52,
edges                                 55,
components                            52,
cycle rank                             0,
left degrees                      {1:55},
right degrees                {1:51,4:1}.
```

It is the disjoint union of 51 copies of `K_(1,1)` and one `K_(1,4)`, so it
is a forest and the left projection is already injective. Its canonical graph
digest is

```text
620013449005471279d314a991283f139d2f31169d084b6ff1cdf2c1058018b5.
```

Adding the odd-side pivot label gives 53 right vertices with degree histogram
`{1:52,3:1}`, still a forest. The pivot-right graph digest is

```text
cff105369ac7be403c85f2c5ff594b19b085883919550533059ae5bdf83fd6fd.
```

The exact extension deletion removes one isolated edge only.


The compatibility verifier does not import this census as literal graph
constants. It independently rebuilds the exact `F_23` precursor: 75 packets,
56 comparisons with empty `H` (the `H=1` class), one `mu_3=0` extension
deletion, and 55 retained rows. It recomputes both predecessor row digests and
serializes each realized graph edge, in retained-row order, as

```text
(packet_index, left_label, right_label).
```

The base, pivot-left, pivot-right, and pivot-both digests are all checked from
those derived labels. Before extension deletion the graph has 56 edges, 56
left vertices, 53 right vertices, 53 components, and digest
`9bb01a03239c81b4e8110ba55f835f22366920346e00dbe3fef5c9c486519853`.
The unique deleted row is packet 2; its left and right labels each have degree
one in the 56-row graph and neither occurs after deletion. Thus the claimed
isolated-edge removal is derived from the exact rows rather than assumed.

This establishes an additive orientation for that pinned raw corpus, but not for arbitrary
square-fold parents. The corpus is still pre-first-match, its pivot is not an
actual RIM pivot, and its forest orientation is not an owner-typed payment.
The target-erased `K_(3,3)` fixture above shows why a theorem must preserve every carried key and prove forest structure
rather than infer it from reconstruction.

## 5. Sharp additive criterion

Fix a carried key and literal `G`. Let `Gamma` be the simple bipartite graph
whose left vertices are realized even labels, whose right vertices are
realized odd labels, and whose edges are reconstructed marked parents.
Marked reconstruction makes distinct parents distinct edges.

**Theorem (pseudoforest endpoint assignment).** The following are equivalent:

1. every component of `Gamma` has at most one cycle;
2. every edge can be assigned to one endpoint so that no vertex receives more
   than one edge.

For `2 -> 1`, a component with `m` edges and `n` vertices has
`m<=n`, because the assigned-edge count is the sum of vertex loads. For
`1 -> 2`, assign every tree edge to its child after choosing a root. In a
unicyclic component, orient the unique cycle cyclically and assign every tree
attached to the cycle away from its attachment vertex. Every vertex then
receives at most one edge.

Consequently, on a pseudoforest,

```text
|parents|<=|even labels|+|odd labels|.
```

For a forest the sharper bound subtracts the number of components. In
general, the exact excess is the cyclomatic contribution. The target-erased
`K_(3,3)` fixture is not a pseudoforest and has no multiplicity-one endpoint
assignment. The target-tagged fixture is a pseudoforest and does have such an
assignment; this criterion therefore diagnoses target erasure, not a
fixed-target obstruction.

An owner-friendly equivalent is a disjoint partition

```text
X=X_even disjoint_union X_odd
```

such that `u` is injective on `X_even` and `sigma` is injective on `X_odd`.
This is precisely the endpoint assignment above. It is the additional
conditional theorem needed to change the square-fold product encoding into
an additive transfer.

## 6. Owner typing and pivot scope

The even channel has the algebraic shape of a lower-domain signed quotient
defect after division by two, but it does not pay the compatible odd lifts of
a nonquotient parent. The parent itself descends through the square quotient
only in the pointwise special case `sigma=0`, when both off-core sides are
unions of antipodal pairs. The odd channel is square-root-twisted weighted
data, not a Boolean quotient support.

The named quotient/planted schema has no executable generic projector at
admission-gap commit `8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`, note
blob `fdeabf0708cb8806feefae9322ed9002339332cf`. Therefore neither projected
channel currently enters a typed quotient owner with its parent multiplicity.

Neither channel enters the rank owner. The actual owner at base commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`, note blob
`ddfce00907f34128b324a64041f4e0ec8957b7d3`, requires an actual received pair,
bad slope, explaining codeword, agreement set, noncontainment witness, and
the field-native Hankel matrix. Rank drop means every maximal minor of that
actual matrix vanishes. The conditional adapter is commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
`f24ce928df7e7170c1b4f3228d5fe9b184be50b4`.

This fixture constructs no such actual incidence. It selects no raw or toy
pivot, proves no actual maximal minor vanishes, leaves no vanishing pivot
family unrouted, and routes exactly zero objects to `DEEP_MCA_RANK_DROP`.

Thus even a future pseudoforest theorem would still need two owner-typed
endpoint maps preserving the literal `G` and every carried key. The graph
criterion controls multiplicity; it does not manufacture those maps.

## 7. Exact provenance

The checked base snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- prefix reduction commit `e83962ae5ad7bacb391b691ffd37f0abef977b83`,
  note blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- singleton schema commit `84b393ec1bc52fa662756bd117a45537007d086a`,
  note blob `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- F23 precursor commit `f23a3b78a6bbe1d50a81b3976f92aa7c135ab300`,
  note blob `5214d5d7fc91dab3f5ba12aabf5fef0c26922e9b`, verifier
  blob `678463a3a188ecdb07c7bd7cd6f66401895d0eeb`;
- square-fold predecessor commit
  `f64e03a1215653eeafe3186df55269273d9f7653`, note blob
  `301144d04458027131779907f7f74aa5a6682bf4`, verifier blob
  `2507f09115c7eefbc86025dbaf204ea83c744283`, Lean blob
  `ab061b3c53a320fbb8881bab4e6fa8e573f83248`;
- marked-transfer boundary commit
  `332153d6e74403e3ad20f367ff4a3df8406a30bf`, note blob
  `6ce5a571ca05f774a6569a9c78d9cb69e8fc896a`;
- marked-contact fold boundary commit
  `3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835`, note blob
  `13479a4b8de5f495508375a16366b62efe39acab`;
- admission-gap commit `8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`,
  note blob `fdeabf0708cb8806feefae9322ed9002339332cf`;
- marked all-minors adapter commit
  `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`.

The target-erased `F_23` `K_(3,3)` fixture and its target-tagged split are reconstructed from the displayed definitions;
it is not imported as a payment from any predecessor.

## 8. Nonclaims

- No unavailable first-match projector is executed.
- No toy packet is called an admitted post-first-match unit.
- No low-moment, Johnson-packing, mode-at-null, image-only, or zero-defect
  shortcut is used.
- No child-image count is promoted to a parent-support payment.
- No actual RIM matrix or actual pivot is constructed.
- No vanishing pivot family exists in this packet, so none is left unrouted.
- No rank-drop charge is created or reused.
- The literal common core is never erased, shrunk, or inferred from the defect.
- No fixed-target additive transfer or deployed bound is refuted.
- The deployed primitive support certificate remains undecided.

## 9. Reproduction and formalization

```bash
python3 experimental/scripts/verify_route_d_square_fold_compatibility_graph_v1.py
python3 -O experimental/scripts/verify_route_d_square_fold_compatibility_graph_v1.py
python3 experimental/scripts/verify_route_d_square_fold_compatibility_graph_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_square_fold_compatibility_graph_v1.py --tamper
(cd experimental/lean/route_d_square_fold_compatibility_graph_v1 && lake build)
```

The deterministic verifier uses only the Python standard library. It rebuilds
the exact
75/56/55 predecessor family and its graph digests, and checks
the alphabet, all nine marked pairs, exact moments, primitive stabilizers, the
`K_(3,3)` obstruction, and the pseudoforest/orientation equivalence over every
subgraph of `K_(3,3)`. The standalone Lean layer records the exact
reconstruction, additive conditional interface, arithmetic fixture pins, and
the legal actual-rank guard.
