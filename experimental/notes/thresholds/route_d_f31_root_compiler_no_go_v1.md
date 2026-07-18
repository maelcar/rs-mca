# Route-D F31 root-compiler no-go v1

STATUS: COUNTEREXAMPLE

## Result

The `99` pre-deletion marked cores in the finite `F_31` fixture do not compile
as `99` Route-D branch-excess units under the singleton schema.  The full
primitive corpus has `119` raw mates but only `28` depth-three mate classes;
after adjoining the reference support, the restricted toy parent has `29`
children and hence only `28` non-base child units.

For the explicit toy order in this packet, children are ordered by their least
support in tuple lexicographic order.  Its base child has cubic power-sum label
`2`.  The globally lexicographically least distance-three boundary packet for
each of the other `28` children occupies `20` algebraic cells and gives only
`8` same-cell comparison candidates.  All eight reduced weights are
projectively primitive, Vandermonde-full, and nonextension.  This is a
conditional pre-filter algebraic replay, not a first-match deletion or an
unpaid residual.

Exhausting all `29` choices of base child removes dependence on the toy base
choice: the `28` canonical packets occupy `19` or `20` cells and yield `9` or
`8` algebraic same-cell comparison candidates, respectively.  Every such
candidate is nonextension and projectively primitive.  The exact counts refute
the type identification

```text
raw marked support packet = branch-excess unit,
```

and expose the missing compiler.  They do not prove that no compiler can
exist, execute any named deletion, or decide the deployed support bound.

## Exact fixture and child partition

Work over `F_31` on `D=F_31^*` with

```text
k=12, A=15, j=15, t=3, w=2,
E={1,2,3}, f=1_E, g(x)=x^12, gamma=0,
B={1,2,3,4,5,7,10,11,12,18,19,20,21,26,28},
Phi_2(B)=(30,9).
```

Enumerate all distance-three mates

```text
T=(B\R) union A,
R subset B\E,
A subset D\B,
|R|=|A|=3,
Phi_2(T)=Phi_2(B).
```

There are `121` mates, of which `119` have trivial projective signed
stabilizer.  Their cubic power-sum child key

```text
chi(T)=P_3(T)=sum_(x in T) x^3
```

takes `28` values.  The reference support has `chi(B)=17`, a value absent from
the primitive mates, so adjoining `B` gives `29` children.  For any selected
base child `C_0`, the child partition has exactly `28` other children.  Thus a
singleton branch schema supplies one root unit `(parent,C)` per non-base
child, not one unit per raw support in `C`.

The predecessor finite verifier records the literal provenance guard
`named_deletions_executed=false`.  Consequently none of these raw supports or
toy packets is asserted to have passed priority zero, the strict-distance
decision, or earlier global first-match filters.  Distance three supplies the
algebraic boundary relation only conditionally on admission.

## Canonical packet and carried mark

For each non-base child `C`, form every ordered pair

```text
(S,S') with S in C, S' outside C,
|S\S'|=|S'\S|=3,
```

inside the restricted `120`-support toy parent, and choose the globally least
pair in lexicographic `(S,S')` order.  Put

```text
G=S intersect S',
A=S\S',
R=S'\S,
U=L_A,
V=L_R,
c=const(U)-const(V).
```

The verifier checks `U-c=V`,

```text
P_3(S)-P_3(S')=-3c in F_31,
```

and the exact marked reconstructions `S=G union A` and `S'=G union R`.
The mark `G` is recomputed for the canonical boundary pair and then carried;
it is not silently replaced by the earlier `(T,B)` mark.  In particular the
`chi=17` child containing `B` receives a valid reverse boundary witness.

The source singleton rule orders children only through a fixed total order; it
does not select the order used here.  The least-support order, and hence the
base label `2`, is an explicit deterministic toy choice.

## Algebraic same-cell replay

The packet key is

```text
(r,c,U,beta)=(3,c,L_A,(30,9)).
```

The fixed `beta` is legitimate only in this explicitly first-exposed toy seam.
No Rule-1 key duplicates occur.  Group the `28` packets by `(3,c)`, choose the
least packet in each cell, and for a representative `(U_0,V_0)` and packet
`(U,V)` set

```text
L_+=U_0 V,
L_-=V_0 U,
H=gcd(L_+,L_-),
M_+=L_+/H,
M_-=L_-/H.
```

The reduced signed weight is

```text
mu=1_A0+1_R-1_R0-1_A.
```

For the least-support toy order the `28` packets have cell-size histogram

```text
{1:13, 2:6, 3:1},
```

so there are `20` cells and `8` algebraic comparisons.  Their reduced-support
histogram, fourth moments, and lexicographic Vandermonde pivots are

```text
support sizes  {9:1,10:5,11:2},
mu_4           {9,10,11,18,21,25,25,28},
pivots         {3,11,14,17,17,23,27,28}.
```

For every comparison the verifier checks exact polynomial factorization and
recovery, `mu_0=mu_1=mu_2=mu_3=0`, full row rank of the degree-`0..3`
Vandermonde, projective primitivity, and `mu_4 != 0`.  The carried packet mark
reconstructs both boundary endpoints.

The representative sides are not disjoint from the deleted packet's carried
core in this toy replay.  Algebraic recovery therefore does not by itself
supply a marked-disjointness transfer theorem for a large signed defect.

## Order-invariant base-child audit

The verifier repeats the construction after excluding each of the `29`
children in turn.  In every case there are `28` root packets, no Rule-1 key
duplicate, and no extension comparison.  The only ranges are

```text
occupied cells                         19..20,
algebraic same-cell comparisons         8..9,
nonextension projectively primitive     8..9.
```

Exactly `13` base-child choices give `(19 cells,9 comparisons)` and exactly
`16` give `(20 cells,8 comparisons)`.

This range is independent of which child an unspecified upstream total order
would place first.  It is still a toy pre-filter statement because admission
to an actual branch-excess parent has not been constructed.

## Forced-reference anchor and multiplicity obstruction

For comparison, force `S'=B` and choose one least mate in each of the `28`
mate children.  Every individual packet has `G,A,R` pairwise disjoint,
contains `E` in `G`, and preserves the common-core mark.  The `28` packets
have `28` distinct `c` labels, hence zero algebraic same-cell comparisons.
All reuse the same outside boundary witness `B`; such witness reuse does not
invalidate the `28` child units.  Rather, it makes the type collapse explicit:
the `119` anchored raw pairs still belong to only `28` children and do not
become `119` distinct branch units.

At fixed `28` algebraic cells, obtaining `81` comparisons would require

```text
28+81=109 packets.
```

A single `29`-child partition has only `28` non-base child units.  If one
nevertheless counts overlapping raw anchored pairs, truncating every mate
child at multiplicity `L=1,...,6` gives

```text
N_L       = 28,55,78,96,106,113,
N_L-28    =  0,27,50,68, 78, 85.
```

Thus an overlap-only replay first reaches `81` comparisons at level six.  This
is a diagnostic for the missing deeper multiplicity/compiler theorem, not a
construction of six disjoint branch layers and not a numerical payment.

## Compiler/type conclusion

The marked-incidence and fixed-subgroup machinery operates on typed
branch-excess units, canonical packets, and executable first-match predicates.
The finite `F_31` corpus supplies raw marked supports and exact algebraic
boundary packets, but no named map converts the within-child multiplicity into
additional branch units.  The singleton schema instead collapses the `119`
raw mates to `28` child units.

Therefore the primitive algebraic candidate counts from the raw fixed-target
corpus cannot be promoted as a post-first-match floor.  A valid promotion would
need a separately stated compiler that constructs the actual `(parent,C)`
units, proves admission and priority decisions, carries the canonical `G`, and
specifies how deeper multiplicity remains disjoint.  Absence of such a witness
here is a type obstruction, not a proof of global nonexistence.

## Exact provenance

The checked base snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

Prefix-reduction shipment commit
`e83962ae5ad7bacb391b691ffd37f0abef977b83`:

- `experimental/notes/thresholds/rowsharp_q_prefix_atom_reductions_v1.md`,
  blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- `experimental/scripts/verify_rowsharp_q_prefix_atom_reductions_v1.py`,
  blob `a2da1c0657600d7497512bfa80138e60f6c89c01`;
- `experimental/data/certificates/rowsharp-q-prefix-atom-reductions-v1/rowsharp_q_prefix_atom_reductions_v1.json`,
  blob `908ee64976b46b9d8b5bd6015dd8c031dc17df6f`;
- `experimental/notes/thresholds/cap25_v13_lq_top_seam_marked_incidence.md`,
  blob `a7f2bf4f1338d0b31d999c86a29859317033113f`.

Singleton schema commit `84b393ec1bc52fa662756bd117a45537007d086a`:

- `experimental/notes/thresholds/rowsharp_q_singleton_topseam_v1.md`, blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- `experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py`, blob
  `dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1`;
- `experimental/data/certificates/rowsharp-q-singleton-topseam-v1/rowsharp_q_singleton_topseam_v1.json`,
  blob `6a8aa0c61eeebfa93b97e157b3bc72f8c3dce892`.

Marked puncture recursion commit
`5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`:

- note blob `7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9`;
- verifier blob `d6bb3cb7e8177d3c52eb245e4f7e142ea3250734`;
- Lean module blob `81d736e0e398210d552ecf307a1abc36702bc520`.

Marked RIM adapter and finite `F_31` fixture commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`:

- note blob `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`;
- verifier blob `ace3e859b917ae87eeffb8c0e7c37155520e311e`;
- Lean module blob `78e46c6ab97d97191c567041f81a6ca05e76cf41`;
- agents-log blob `760678a6e45e00e66fe9af4fe741ce59734719eb`.

The base governance blobs are `agents.md` at
`2fea2bce6a348105f0016fcf739b5247bf408d93` and the predecessor
`experimental/agents-log.md` at
`45b04597efb40741b807e48b290a0544f2fe6baf`.

## Nonclaims

- This packet does not prove or refute
  `67472*2130706433` or the deployed KoalaBear safe row.
- It does not call a raw support packet a branch-excess unit.
- It does not call an algebraic comparison a Rule-2 deletion, unpaid unit,
  numerical payment, or ledger floor.
- It does not claim priority-zero survival, strict-distance survival, or
  execution of any named first-match deletion.
- It does not infer marked disjointness from algebraic Rule-2 recovery.
- It does not discard or normalize away the canonical common-core mark `G`.
- It does not change the generated field or invoke an extension-field payment.
- It does not infer global nonexistence of a deeper compiler from the absence
  of a compiler witness in this finite packet.

## Reproduction

```bash
python3 experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py
python3 -O experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py
python3 experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_f31_root_compiler_no_go_v1.py --tamper
(cd experimental/lean/route_d_f31_root_compiler_no_go_v1 && lake build)
```

The verifier uses only the Python standard library and reconstructs every
finite object from definitions.
