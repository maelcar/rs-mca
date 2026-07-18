# Route-D F17 global marked-contact pivot no-go v1

STATUS: COUNTEREXAMPLE

## Result

A complete raw first-seam algebraic census over F_17 shows that marked contact
profiles and nonzero weighted-Vandermonde pivot labels do not provide the
required global injection.

Fix

    D=F_17^*, r=t=2, beta_1=16,

and enumerate every nonzero cell c, every split squarefree degree-two pair

    U=L_A, V=U-c=L_R,

and every singleton literal core G={g} disjoint from A union R with

    g+P_1(A)=16.

After the exact Rule-1 side-key deduplication available in this finite schema,
there are 516 packets in 16 cells.  Choose the lexicographically least packet
in each cell as representative.  Among the resulting 500 comparisons, the
sequential algebraic filters leave 463 full-defect rows:

    projective nonprimitive: 13,
    extension mu_3=0:       20,
    support collapse <=3:    0,
    corank-one BC size 4:     4,
    toy pivot vanishing:      0,
    retained:               463.

Thus the 16 representatives plus 463 primitive full defects give

    479 > 2*17 = 34.

Even forgetting recovery keys leaves 407 distinct full-defect weights.

For the exact common-core contact split, 348 retained rows have empty contact
and 115 have nonempty contact.  These give 103 distinct unkeyed off-core
lambda support weights; every row is projectively primitive and has a nonzero
lexicographic marked Vandermonde pivot.  Their row profiles are

    (|A0 intersect G|,|R0 intersect G|)=(1,0): 47,
    (|A0 intersect G|,|R0 intersect G|)=(0,1): 68.

After support-level deduplication the counts are 46 and 57.  The pair
(profile,pivot) takes only 30 distinct values and has maximum
multiplicity 9.  Therefore it is not an injection; moreover

    103 > 2*17 = 34.

This is a counterexample to the raw algebraic profile/pivot compiler and a new
obstruction floor:

    GLOBAL_MARKED_CONTACT_PIVOT_MULTIPLICITY.

It is not a counterexample to the fully filtered deployed residual.  The
literal named first-match projectors remain non-executable, so this packet
does not claim that any of these 115 rows survive every named deletion.

## 1. SHA-pinned context

The target support certificate is the prefix reduction at commit
e83962ae5ad7bacb391b691ffd37f0abef977b83, note blob
591c91a6aac6b48db0c16abc586b74d7a51e44e2.

The canonical packet and Rule-1/Rule-2 schema is at commit
84b393ec1bc52fa662756bd117a45537007d086a, note blob
dda538a9a36cd0c8e267c11600a49cdc5bf054d1.

The corrected marked-key quantifier theorem is at commit
b23f997474f7a7aec9a889d933c774acc4980050, note blob
5ae8c3f628b8246f9d2c02201854256e56f3ee27.  That packet proves a local
one-scalar cap after literal G and full beta are fixed.  The present census
tests the global sum over cells and varying cores.

The non-executable deletion interface is pinned at commit
8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67, note blob
fdeabf0708cb8806feefae9322ed9002339332cf.

The only accepted actual all-minors rank-drop route is the typed adapter at
commit a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0, note blob
f24ce928df7e7170c1b4f3228d5fe9b184be50b4.

## 2. Canonical global F17 bucket

For each c in F_17^* and two-subset A of D, form U=L_A and V=U-c.  Retain U
when V has two distinct roots R in D.  The parent-prefix condition fixes the
singleton core:

    g=16-P_1(A).

Retain only when g is nonzero and G={g} is disjoint from A union R.  Put

    S=G disjoint union A,
    S'=G disjoint union R.

Order packets in each cell lexicographically by (S,S',U,G).  The Rule-1 key
at the first seam is (r,c,U), because beta is fixed globally.  In this fixture
each retained U has one compatible G, so exact Rule-1 deduplication leaves all
516 packets.

All 16 nonzero cells are occupied.  Their packet-count histogram is

    26:2, 27:2, 28:2, 29:2, 35:2, 37:2, 38:4.

Select the first packet in each cell as its representative P0=(G0,A0,R0).

## 3. Exact full-defect filters

For every other packet P=(G,A,R) in that cell define

    mu=1_(A0)+1_R-1_(R0)-1_A.

The constant-difference locator identity gives

    mu_k=0, k=0,1,2.

The verifier applies these filters sequentially:

1. scalar/sign projective primitivity;
2. extension deletion mu_3!=0;
3. support size at least r+2, with size r+2 assigned to the BC chart;
4. nonzero lexicographic three-column weighted-Vandermonde determinant.

The surviving support histogram is

    5:63, 6:174, 7:108, 8:118.

The 463 typed rows project to 407 distinct literal full-defect weights.

Every surviving toy matrix has row rank 3.  This is only the marked
weighted-Vandermonde matrix of the algebraic defect, not an actual owner-typed
RIM incidence matrix.

Per-cell retained counts are

    c=1:21,  c=2:25,  c=3:34,  c=4:24,
    c=5:33,  c=6:34,  c=7:32,  c=8:24,
    c=9:26,  c=10:31, c=11:36, c=12:34,
    c=13:25, c=14:34, c=15:27, c=16:23.

In particular, even several fixed cells contain more than |F| retained raw
defects.  A nonzero scalar pivot is not a fixed-cell injection.

## 4. Literal marked-contact split

For each retained comparison define the exact contact and off-core weights

    kappa=1_(A0 intersect G)-1_(R0 intersect G),
    lambda=mu-kappa.

Then

    supp(lambda) intersect G=empty,
    lambda_k=-kappa_k, k=0,1,2.

The exhaustive split is

    kappa=0:    348,
    kappa!=0:  115.

Because G is a singleton, the nonempty profiles are precisely (1,0) and
(0,1), giving the counts 47 and 68 above.  All 115 lambda are projectively
primitive.  Every selected marked Vandermonde pivot is nonzero.

There are 103 distinct unkeyed lambda and 115 distinct (c,lambda) pairs.
After support-level deduplication their profile counts are (1,0):46 and
(0,1):57.  The complete recovery base must retain c and the literal marking
context; erasing the key would merge genuinely different packets.

The proposed target codomain at this analogue has only

    |Fin 2 x F_17|=34

points.  Even the 103 distinct unkeyed contact support weights cannot inject
into it.  Their concrete profile/pivot map is more visibly many-to-one: it
uses 30 labels and has a fiber of size 9.

## 5. RIM pivot dichotomy

No selected toy pivot vanishes, so this fixture creates no toy vanishing
family to route.  It instead refutes the implication

    nonzero pivot plus contact profile => support injection.

For a future actual incidence matrix, the legal dichotomy remains:

- if all maximal minors vanish, invoke only the typed rank-drop adapter at
  commit a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0;
- if one actual pivot is nonzero, retain its output multiplicity unless an
  independent decoder theorem proves injectivity.

The present weighted-Vandermonde pivot is not substituted for that actual
incidence pivot.

## 6. First-match scope and nonclaims

This packet executes only the finite algebraic operations that are fully
defined here: packet enumeration, first-seam Rule-1 deduplication, projective
primitivity, extension, support-collapse, BC-size, exact contact splitting,
and toy marked-Vandermonde rank.

It does not execute generated-field, quotient/planted, sparse Padé/Hankel,
M1/window-shadow, actual rank-drop, or other projectors named only inside an
aggregate.  Therefore it does not prove or refute

    |G_gen_support(z)|+|D_full_rank_prim(z)|<=t*p

after the literal full first-match partition.  It proves that any such theorem
must delete or independently encode at least the 103 distinct raw contact
support weights; the profile and nonzero-pivot labels alone cannot do so.

The packet preserves the literal common-core marking and does not use
low-moment payment, Johnson packing, mode-at-null, image-only normalization,
or zero-defect descent.

## Verdict

At the raw algebraic first seam, both the typed representative-plus-defect
mass and the 103 distinct nonempty-contact support weights exceed the analogue
target.  Every retained contact row is primitive and toy-full-rank, while the
support-level profile/pivot map has multiplicity 9.

The deployed certificate remains unproved because the exact named deletion
executor and a global support-injective owner are absent.  The new obstruction
floor is

    GLOBAL_MARKED_CONTACT_PIVOT_MULTIPLICITY.
