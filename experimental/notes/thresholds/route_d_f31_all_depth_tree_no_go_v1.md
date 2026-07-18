# Route-D F31 all-depth tree no-go v1

STATUS: COUNTEREXAMPLE

## Result

The natural all-depth power-sum prefix tree on the restricted `120`-support
`F_31` corpus has exactly `119` branch-excess units, but disjoint tree
accounting cannot retain the earlier fixed-base algebraic floor of `81`
Rule-2 candidates.  Exhausting every base-child choice at every non-unary
prefix bucket gives the exact rowwise cell-collision ceilings

```text
r=3:  9,
r=4: 45,
r=5:  6,
r=6:  0,
total: 60 < 81.
```

The ceiling is computed before Rule-1 deletion and before the `U != U_0`
admission check, so it is also an upper bound for executable Rule-2
comparisons.  The result refutes promotion of the fixed-base `>=81` algebraic
candidate floor through this disjoint tree compiler.  It does not prove or
refute the deployed support certificate.

For the explicit lexicographic replay, the `119` units partition as

```text
12 strict-distance classifications
+ 1 nonprimitive boundary packet
+ 4 algebraic extension candidates
+ 46 algebraic nonextension candidates
+ 56 residual cell representatives
= 119.
```

These are classifications inside a restricted toy family, not official
post-first-match residuals or numerical payments.

## Exact restricted corpus

Work over `F_31` on `D=F_31^*` with

```text
k=12, A=15, j=15, t=3, w=2,
E={1,2,3}, f=1_E, g(x)=x^12, gamma=0,
B={1,2,3,4,5,7,10,11,12,18,19,20,21,26,28},
Phi_2(B)=(30,9).
```

The deterministic enumeration gives `121` distance-three mates of `B` and
`119` mates with trivial projective signed stabilizer.  Adjoin `B` to those
`119` supports.  The resulting `120` distinct supports share `P_1,P_2`.

This restriction is material.  The full prefix fiber can contain other
supports, so its complements, canonical pairs, strictness decisions, and
first-match ownership can differ from the objects below.

## Natural all-depth prefix tree

At depth `m`, group the current bucket by `P_(m+1)`.  Order children by their
least support in tuple lexicographic order.  At every non-unary bucket choose
the first child as the lex base child and create one unit for every other
child.  Unary levels are retained but contribute zero excess.

The exact tree census is:

| row `r` | branch buckets | outdegree histogram | excess units |
|---:|---:|---|---:|
| 3 | 1 | `{29:1}` | 28 |
| 4 | 27 | `{2:6,3:6,4:6,5:6,6:2,9:1}` | 78 |
| 5 | 9, plus one unary bucket | `{1:1,2:7,3:2}` | 11 |
| 6 | 2 | `{2:2}` | 2 |

Thus

```text
28+78+11+2=119=120-1.
```

The child-size histograms are:

```text
r=3: {1:2,2:4,3:5,4:8,5:3,6:4,7:1,8:1,9:1}
r=4: {1:95,2:7,3:3}
r=5: {1:19,2:2}
r=6: {1:4}.
```

The verifier reconstructs the tree identity rather than trusting these
printed counts.

## Canonical marked packet

For a child `C` in a restricted parent bucket, minimize

```text
d(S,S')=|S\S'|
```

over `S in C` and `S'` in the other children, then choose the least pair
`(S,S')`.  Prefix equality gives `d(S,S')>=r`.

- `d=r` is a boundary packet;
- `d>=r+1` is classified strict-distance in this toy tree.

For a boundary pair put

```text
G=S intersect S',
A=S\S',
R=S'\S,
U=L_A,
V=L_R,
c=const(U)-const(V).
```

The verifier checks `U-c=V`, `S=G union A`, and `S'=G union R`.  Every
Rule-2 certificate carries the deleted packet's literal `G`; the mark is
never replaced by an image-only label.

## Lex strict/boundary census

| row `r` | units | boundary | strict | primitive boundary | cells | comparisons |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 28 | 28 | 0 | 27 | 19 | 8 |
| 4 | 78 | 66 | 12 | 66 | 27 | 39 |
| 5 | 11 | 11 | 0 | 11 | 8 | 3 |
| 6 | 2 | 2 | 0 | 2 | 2 | 0 |
| total | 119 | 107 | 12 | 106 | 56 | 50 |

The twelve strict units are all at row four: ten have minimum distance five
and two have minimum distance six.

All `107` boundary packets have distinct Rule-1 keys
`(r,c,U,beta)`.  After removing the unique nonprimitive boundary packet, the
primitive cell-size histogram is

```text
{1:26,2:16,3:9,4:4,5:1}.
```

The unique nonprimitive fixture is

```text
r=3, c=4,
S =(1,2,3,4,5,6,7,10,18,19,20,21,22,23,26),
S'=(1,2,3,4,5,6,7,8,10,11,12,18,21,22,26),
A =(19,20,23),
R =(8,11,12),
stabilizer=((1,+1),(30,-1)).
```

This is a projective signed-stabilizer classification, not an invocation of a
printed payment owner.

## Rule-2 replay

Within each primitive boundary cell choose the least `(S,S')` representative.
For another packet use

```text
L_+=U_0*(U-c),
L_-=(U_0-c)*U,
H=gcd(L_+,L_-),
M_+=L_+/H,
M_-=L_-/H,
mu=1_A0+1_R-1_R0-1_A.
```

For all `50` comparisons the verifier checks exact factorization and recovery,
vanishing moments `mu_0,...,mu_r`, a nonzero lexicographic `(r+1)`-column
Vandermonde pivot, full row rank, absence of support collapse and the `r+2`
BC case, projective primitivity, and literal reconstruction from the carried
common core.

The support histogram is

```text
{8:1,9:4,10:13,11:4,12:6,13:10,14:5,15:5,16:2}.
```

Exactly four lex certificates satisfy the extension predicate
`mu_(r+1)=0`; all lie at row four:

```text
(c,|supp(mu)|)=(1,14),(3,11),(15,14),(29,12).
```

There are `154` ordered same-cell comparisons and ten ordered extension
certificates.  Exhausting every representative choice gives between two and
five extensions, hence between `45` and `48` nonextension certificates.  This
range is representative-order invariant for the fixed lex tree.

## Every-base-child DP

To remove dependence on the chosen base child, enumerate every possible
omitted child independently in every branch bucket.  For each row the verifier
maintains

```text
occupied nonzero-c bit mask -> maximum selected boundary-packet count.
```

An option mask uses bitwise union, not arithmetic addition.  After all buckets
of a row, the cell-collision surplus is

```text
selected packets - popcount(occupied cells).
```

This is an upper bound for Rule-2 comparisons because Rule 2 can only delete
nonrepresentatives in occupied cells and additionally requires distinct `U`.

After retaining only projective boundary packets the exact DP is:

| row | states | witness packets | witness cells | maximum surplus |
|---:|---:|---:|---:|---:|
| 3 | 13 | 28 | 19 | 9 |
| 4 | 6896 | 70 | 25 | 45 |
| 5 | 153 | 11 | 5 | 6 |
| 6 | 4 | 2 | 2 | 0 |

Therefore every base-child order satisfies

```text
N_Rule2 <= 9+45+6+0 = 60 < 81.
```

Retaining the unique nonprimitive boundary packet leaves the same rowwise
surplus ceilings.  Rule-1 deletion, extension classification, or a failed
`U != U_0` check can only lower the executable Rule-2 count.

## Toy row-budget obstruction

The residual cell representatives occupy all four rows

```text
R_D^toy={3,4,5,6}.
```

Thus `|R_D^toy|=4>t=3`.  Rows `3,4,5` account for `117` of the `119` excess
units, while the two row-six units remain.  This is an exact obstruction to
applying the all-depth `|R_D|<=t` hypothesis to this restricted toy tree.  It
is not a statement about the deployed `t=67472` row set.

## Ownership and scope

The packet proves only a finite restricted-tree no-go:

- it does not execute earlier global first-match predicates or named
  deletions;
- strict-distance and extension labels are algebraic classifications, not
  payments;
- the `50`, `46`, `45..48`, and `<=60` counts are not official
  `N_WSP_full`, genuine unpaid units, or ledger floors;
- the restricted parent need not equal an actual post-first-match bucket;
- it preserves the common core and does not use image-only accounting;
- it does not use low-moment, Johnson-packing, mode-at-null, or zero-defect
  closure shortcuts;
- it does not prove or refute `67472*2130706433` or the KoalaBear safe row.

The counterexample is to the promotion

```text
fixed-base >=81 algebraic candidates
  => >=81 disjoint all-depth Rule-2 branch units.
```

## Exact provenance

Base snapshot commit:
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

Prefix reductions commit `e83962ae5ad7bacb391b691ffd37f0abef977b83`:

- note blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- verifier blob `a2da1c0657600d7497512bfa80138e60f6c89c01`;
- certificate blob `908ee64976b46b9d8b5bd6015dd8c031dc17df6f`;
- marked-incidence note blob `a7f2bf4f1338d0b31d999c86a29859317033113f`.

Singleton schema commit `84b393ec1bc52fa662756bd117a45537007d086a`:

- note blob `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- verifier blob `dc4a7235b3274fbcc5ef0ed8bd8c96620b04a5a1`;
- certificate blob `6a8aa0c61eeebfa93b97e157b3bc72f8c3dce892`.

Marked puncture recursion commit
`5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`:

- note blob `7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9`;
- verifier blob `d6bb3cb7e8177d3c52eb245e4f7e142ea3250734`;
- Lean blob `81d736e0e398210d552ecf307a1abc36702bc520`.

Marked RIM adapter commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`:

- note blob `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`;
- verifier blob `ace3e859b917ae87eeffb8c0e7c37155520e311e`;
- Lean blob `78e46c6ab97d97191c567041f81a6ca05e76cf41`.

Algebraic preflight commit
`36d560d7421dace47bf48b3fecc9389adaf0977b`:

- note blob `b11def86906c467fc5a1b07caf14a07108b430f6`;
- verifier blob `a00d900f5af63babf847ebbaf4efdc2dba4babc7`;
- Lean blob `cfbc2e4ce825247fe638e14464b085226fa403e3`.

Root compiler commit `91a9e31284adb34a1dfe5c71e434aa709ba2d3fe`:

- note blob `97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc`;
- verifier blob `c6c78f88def94ec460fe33ac4aeb673533ad3a11`;
- Lean blob `86bca88e3d37c786bc0b4531c1ae96643d8ac5dd`;
- agents-log blob `d45f9f0bbc5e423dba6bc70f5749996f97a91db9`.

Governance blobs are `agents.md` at
`2fea2bce6a348105f0016fcf739b5247bf408d93` and predecessor
`experimental/agents-log.md` at
`45b04597efb40741b807e48b290a0544f2fe6baf`.

## Reproduction

```bash
python3 experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py
python3 -O experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py
python3 experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_f31_all_depth_tree_no_go_v1.py --tamper
(cd experimental/lean/route_d_f31_all_depth_tree_no_go_v1 && lake build)
```

The verifier uses only the Python standard library and reconstructs every
finite object from definitions.  Tamper mode runs `23` targeted mutations and
an exhaustive mutation of all `157` emitted result leaves; all `180` must be
rejected.
