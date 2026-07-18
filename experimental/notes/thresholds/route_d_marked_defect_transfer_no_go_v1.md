# Route-D marked-defect transfer no-go v1

STATUS: COUNTEREXAMPLE

## Result

The exact `F_31` canonical root comparisons from the predecessor compiler
packet do not admit a large signed-defect transfer which is disjoint from the
deleted packet's carried canonical common core.  For the support-lex toy base
child, all eight reduced defects meet that core.  Exhausting all 29 possible
base children gives 245 comparison occurrences, representing 11 distinct
comparisons, and none is marked-disjoint.

Replacing the canonical mark by the intersection of the two packet cores does
make the reduced defect disjoint from the smaller intersection.  It does not
give the required transfer: the smaller intersection is not the deleted
packet's canonical mark, the residual endpoint locators retain a nontrivial
common factor, and exact gcd reduction returns the original degree-three
boundary decomposition and its original core contact.

Every maximal minor of every weighted-Vandermonde comparison matrix is
nonzero.  Hence this fixture supplies no vanishing maximal-minor family to the
existing rank-drop owner.  The obstruction is a marked-interface/type
obstruction on conditional toy packets.  It is not a post-first-match residual,
does not execute a named deletion, and does not prove or refute the deployed
KoalaBear bound.

## 1. Generic canonical-core restriction lemma

Let two exact boundary packets in one Rule-2 cell be

```text
P_0=(G_0,A_0,R_0),   P=(G,A,R),
```

with disjoint decompositions

```text
S_0=G_0 disjoint_union A_0,  S'_0=G_0 disjoint_union R_0,
S  =G   disjoint_union A,    S'  =G   disjoint_union R.
```

The reduced signed weight is

```text
mu = 1_(A_0) + 1_R - 1_(R_0) - 1_A.              (MD1)
```

Because `A` and `R` are disjoint from `G`, restriction to the carried packet
core gives the exact identity

```text
mu|_G = 1_(A_0 intersect G) - 1_(R_0 intersect G). (MD2)
```

The representative sides `A_0,R_0` are disjoint.  Therefore their two terms
cannot cancel on `G`, and

```text
supp(mu) intersect G is empty
  iff (A_0 union R_0) intersect G is empty.         (MD3)
```

This is the required marked-disjointness test.  Algebraic Rule-2 recovery does
not imply it.

The disjoint endpoint decomposition is also unique:

```text
G=S intersect S',   A=S minus S',   R=S' minus S.  (MD4)
```

Thus there is no different endpoint-preserving disjoint degree-three marking.
If roots are removed from `G` and inserted into both sides, the sides acquire a
common factor; reducing that factor restores `(G,A,R)`.

## 2. Exact `F_31` fixture

Work over `F_31` on `D=F_31^*` with

```text
k=12, A=15, j=15, t=3, w=2,
E={1,2,3}, f=1_E, g(x)=x^12, gamma=0,
B={1,2,3,4,5,7,10,11,12,18,19,20,21,26,28},
Phi_2(B)=(30,9).
```

The predecessor construction has 121 distance-three mates, 119 with trivial
projective signed stabilizer, 120 supports after adjoining `B`, and 29
depth-three children.  For each child it selects the globally least boundary
pair `(S,S')`, computes the canonical mark `G=S intersect S'`, and carries that
literal mark into the comparison.

For the support-lex toy order the base child is `2`.  The eight comparison
fixtures are listed as

```text
(c, representative child, packet child, A_0 intersect G, R_0 intersect G)
```

and are exactly

```text
( 3, 22, 25, {12,18}, {11,28})
( 6, 14, 16, {7},     {19})
(14, 23, 19, {21},    {7,11,18})
(21,  1, 12, {19,20}, {7})
(22, 30, 29, {21},    {12})
(22, 30, 15, {21,29}, {})
(28, 11,  8, {28},    {21})
(30,  5,  6, {},       {11}).
```

Their contact-size multiset is

```text
{1,2,2,2,2,3,4,4},
```

so none is marked-disjoint.  Their reduced-support histogram is

```text
{9:1, 10:5, 11:2}.
```

All reduced weights remain projectively primitive and have
`mu_0=mu_1=mu_2=mu_3=0`, while `mu_4` is nonzero.  Hence these are full-rank
nonextension algebraic comparisons, not zero-defect or extension cases.

## 3. All-base-choice census

Repeat the canonical comparison construction after excluding each possible
base child.  Sixteen choices give 20 cells and 8 comparisons; thirteen give
19 cells and 9 comparisons.  Across the 29 choices there are

```text
comparison occurrences                 245,
distinct comparisons                    11,
marked-disjoint occurrences              0,
contact-size histogram {1:81,2:109,3:27,4:28},
support-size histogram  {9:27,10:136,11:82}.
```

Thus the contact obstruction is not an artifact of choosing child `2` as the
toy base.

## 4. Common-core intersection cancels back

For a comparison put

```text
K=G_0 intersect G.
```

Since every term in `(MD1)` lies outside its own packet core,

```text
supp(mu) intersect K is empty.                       (MD5)
```

In the 245 occurrences the exact `|K|` histogram is

```text
{7:55, 8:55, 9:135}.
```

This smaller common intersection cannot replace the canonical mark.  For the
deleted endpoints, factor only `K` and write

```text
S minus K  = (G minus K) disjoint_union A,
S' minus K = (G minus K) disjoint_union R.
```

The two residual endpoint locators have common gcd

```text
L_(G minus K).
```

Their residual sizes are respectively `8,7,6` when `|K|=7,8,9`, and the
common-factor degrees are `5,4,3`.  Exact division by the gcd returns `L_A`
and `L_R`.  Before that division the locator difference is exactly

```text
L_(S minus K)-L_(S' minus K)=c*L_(G minus K),
```

which has positive degree in every occurrence and is therefore not a
constant-shift top seam.  Thus the attempted re-marking either:

1. keeps the common factor, in which case it is not the degree-three
   constant-shift top seam; or
2. cancels the common factor, in which case it returns the unique canonical
   packet mark `G` and the contact certified by `(MD2)`.

Carrying `K` together with enough leftover data to reconstruct `G` does not
change this conclusion: the original canonical mark is then still present and
still meets the reduced defect.  No recovery datum is discarded in this
audit.

## 5. Puncture and fixed-subgroup rejection

The marked puncture-contact recursion requires padding

```text
P subset D minus E
```

and partitions contact with the shadow boundary `partial_H E=HE minus E`.
Taking `E=G` here does not make `(MD2)` into such a contact: every offending
root lies in `G` itself, so the reduced defect is not legal padding off `G`.

There is also no nontrivial relevant normalization.  For a degree-three side
support, let `u` be its common depth-two locator prefix.  Among all 29
canonical packets, 28 have fixed subgroup `{1}`.  The only exception is

```text
(child,c,H)=(21,4,{1,30}),
```

and that packet occurs in none of the 11 comparisons.  Hence every compared
side target has `H={1}` and empty shadow boundary.

The parent target `z=(30,9)` also has trivial stabilizer.  The earlier
one-root punctured target `(0,9)` has stabilizer `{1,30}`, but its nonidentity
element does not preserve this comparison interface: multiplication by `-1`
does not preserve the parent target and sends a degree-three cell label
`c` to `-c`.  Every comparison has `c!=0`, so this leaves the cell.

All objects lie in the prime field `F_31`; no extension field is introduced
and the generated field is unchanged.  Field preservation does not repair the
lost target, cell, or canonical mark.

## 6. Full maximal-minor census

For a reduced weight `mu` with support `D_mu`, form the `4 x |D_mu|`
weighted-Vandermonde comparison matrix

```text
V_(i,x)=mu(x) x^i,   0<=i<=3, x in D_mu.
```

For four distinct support roots, its maximal minor is the product of four
nonzero weights and the ordinary Vandermonde determinant.  It is therefore
nonzero over `F_31`.  The verifier nevertheless enumerates every maximal
minor and obtains

```text
support-lex eight comparisons       1836 / 1836 nonzero,
all 245 comparison occurrences     59022 / 59022 nonzero,
11 distinct comparison matrices     2706 / 2706 nonzero.
```

This comparison matrix is not the actual-incidence Hankel matrix consumed by
the existing rank-drop owner.  The census therefore does not evaluate the
owner predicate.  Instead it proves that no vanishing comparison-pivot family
exists even before the required actual-incidence adapter could be invoked.
A raw vanishing family, had one appeared, still would not be owner-eligible
without that adapter.

The verifier independently reconstructs the actual `F_31` incidence Hankel
matrix and obtains rank `3`, with `541` of its `560` maximal minors nonzero,
matching the pinned marked-RIM predecessor.  Hence the actual all-minors-vanish predicate is false
as well.  The number routed to the existing rank-drop owner is exactly zero,
first by type separation and also by the full-rank actual-incidence check.  No
new owner or charge is introduced.

## 7. Type conclusion

The finite corpus refutes the implication

```text
conditional canonical Rule-2 comparison + exact algebraic recovery
  => signed defect disjoint from the carried canonical packet core.
```

The exact obstruction is the representative-side contact in `(MD2)`.  A
future large-defect transfer must either carry and pay this contact as a new
typed branch, or prove an executable earlier deletion which removes it.  It
cannot silently shrink the mark, normalize by an unrelated child subgroup, or
route a nonvanishing pivot family to rank drop.

## 8. Exact provenance

The checked base snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

The direct predecessor is root-compiler commit
`91a9e31284adb34a1dfe5c71e434aa709ba2d3fe`:

- note blob `97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc`;
- verifier blob `c6c78f88def94ec460fe33ac4aeb673533ad3a11`;
- Lean module blob `86bca88e3d37c786bc0b4531c1ae96643d8ac5dd`.

The marked puncture recursion is commit
`5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`:

- note blob `7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9`;
- verifier blob `d6bb3cb7e8177d3c52eb245e4f7e142ea3250734`;
- Lean module blob `81d736e0e398210d552ecf307a1abc36702bc520`.

The marked all-maximal-minors adapter is commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`:

- note blob `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`;
- verifier blob `ace3e859b917ae87eeffb8c0e7c37155520e311e`;
- Lean module blob `78e46c6ab97d97191c567041f81a6ca05e76cf41`.

At the base snapshot, the other consumed statements are:

- prefix-reduction note blob `591c91a6aac6b48db0c16abc586b74d7a51e44e2`
  from commit `e83962ae5ad7bacb391b691ffd37f0abef977b83`;
- singleton top-seam note blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1` from commit
  `84b393ec1bc52fa662756bd117a45537007d086a`;
- signed local-minority folding note blob
  `376c21252b5ee167839c2d214f173428c0010ff4`;
- marked cross-Gram note blob
  `4ed789595305170556371c87c5773d9e14ba4307`;
- governance blob `agents.md` at
  `2fea2bce6a348105f0016fcf739b5247bf408d93` and predecessor log blob
  `45b04597efb40741b807e48b290a0544f2fe6baf`.

## 9. Nonclaims

- This packet does not prove or refute
  `67472*2130706433` or the deployed KoalaBear safe row.
- It does not call a conditional toy packet an admitted branch-excess unit or
  post-first-match residual.
- It does not execute `generated_field`, `quotient_planted`,
  `sparse_pade_hankel`, `m1_window_shadow`, `rank_drop_pivot`, `bc_chart`,
  `sp_shift_pair`, or `extension_slope`.
- It does not infer a numerical payment from algebraic recovery or full rank.
- It does not replace the canonical common-core mark by `G_0 intersect G`.
- It does not use a low-moment, Johnson-packing, mode-at-null, image-only, or
  zero-defect shortcut.
- It creates no new charge and does not recharge the existing rank-drop owner.

## 10. Reproduction and formalization

```bash
python3 experimental/scripts/verify_route_d_marked_defect_transfer_no_go_v1.py
python3 -O experimental/scripts/verify_route_d_marked_defect_transfer_no_go_v1.py
python3 experimental/scripts/verify_route_d_marked_defect_transfer_no_go_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_marked_defect_transfer_no_go_v1.py --tamper
(cd experimental/lean/route_d_marked_defect_transfer_no_go_v1 && lake build)
```

The verifier uses only the Python standard library and reconstructs every
finite object from definitions.  The standalone Lean companion records the
generic restriction/disjointness theorem, endpoint uniqueness, cancellation
back interface, fixed-subgroup guards, and exact finite count pins.  The
exhaustive `F_31` enumeration remains in the deterministic verifier.
