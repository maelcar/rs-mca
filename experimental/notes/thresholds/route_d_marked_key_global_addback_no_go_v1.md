# Route-D marked-key global add-back no-go v1

STATUS: COUNTEREXAMPLE

## Result

The proposed marked-contact payment has a sharp key dichotomy.

1. For a fixed literal marked core G and full parent prefix beta, Newton
   identities reduce the degree-r packet side to one scalar, so the packet
   fiber has size at most |F|.
2. The printed outer fixed-key residual X_(r,c,U0,H,beta)(z) omits G.  That
   omission is material: an exact F_17 fixture has 24 projectively primitive
   full defects among 25 nonextension, full-rank comparisons in one printed
   key, exceeding |F|=17.
3. If G is inserted into the key, the contact profile is already fixed by
   (A0,R0,G), so the earlier at-most-r profile multiplicity cannot be charged
   again inside that same fiber.
4. A per-key field cap never pays the sum over varying keys.  The required
   theorem is a global injection or weighted add-back over all keys.

The new obstruction is

    MARKED_CONTACT_RECOVERY_KEY_MULTIPLICITY.

A nonzero marked Vandermonde or RIM pivot is only a chart label.  The F_17
toy marked Vandermonde is full rank throughout and still has repeated labels.
Only all-maximal-minors vanishing for the actual owner-typed incidence matrix
may be sent to the existing rank-drop owner.

This packet starts from the prefix target at commit
e83962ae5ad7bacb391b691ffd37f0abef977b83 (note blob
591c91a6aac6b48db0c16abc586b74d7a51e44e2), uses the singleton schema at
commit 84b393ec1bc52fa662756bd117a45537007d086a (note blob
dda538a9a36cd0c8e267c11600a49cdc5bf054d1), and sharpens the marked-contact
packet at commit 3d9e4c01ac8dce2e6d9f73b3ab124977f8e18835 (note blob
13479a4b8de5f495508375a16366b62efe39acab).

It does not execute the literal named first-match deletions.  The executable
deletion gap was pinned at commit 8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67
(note blob fdeabf0708cb8806feefae9322ed9002339332cf).  Therefore this packet
refutes a p-cap derived only from printed key shape and checked Rule-2
predicates, and refutes the pivot-value shortcut, but neither
proves nor refutes the deployed primitive support certificate after those
deletions.

## 1. Exact interfaces and quantifiers

For one Rule-2 representative packet and one comparison packet write

    P0=(G0,A0,R0), P=(G,A,R),
    U0=L_(A0), V0=U0-c, U=L_A, V=U-c,
    H=gcd(U0 V, V0 U).

The reduced signed defect and its contact split are

    mu=1_(A0)+1_R-1_(R0)-1_A,
    kappa=1_(A0 intersect G)-1_(R0 intersect G),
    lambda=mu-kappa.

The printed split-shift residual is indexed outside by

    (r,c,U0,H,beta)

while G varies inside the residual set.  A complete recovery key can instead
carry literal G, or equivalently enough data to recover both contact and
G minus contact.

The two localizations must not be merged:

- Fixed (G,beta): the Newton one-scalar cap applies, but contact and its
  occupancy profile are fixed.
- Varying G: contact profiles can vary, but lambda plus a profile does not
  recover G minus contact unless that information or an exact canonical
  selector is carried.

At the first seam beta=z is globally fixed.  At all depths beta is another
multiplicity coordinate.  Neither fact removes the global sum over G and the
remaining representative/cell keys.

## 2. Fixed-mark full-prefix one-scalar theorem

Let F be a finite field with characteristic greater than r.  Fix c, literal
G, and beta_1,...,beta_(r-1).  Suppose every packet has a monic split
squarefree degree-r locator U=L_A and

    P_k(G)+P_k(A)=beta_k, 1<=k<=r-1.

Then P_1(A),...,P_(r-1)(A) are fixed.  Newton identities fix the elementary
symmetric coefficients e_1(A),...,e_(r-1)(A).  Hence every nonconstant
coefficient of U is fixed, and only U(0) can vary.  The map

    packet -> U(0) in F

is injective because U determines A and U-c determines R.  Thus the fiber has
at most |F| packets.  Any primitive, first-match, fixed-H, or fixed-U0
subfamily satisfies the same bound.

For fixed recovery data, lambda also determines the reduced monic pair and
then U, so the corresponding lambda fiber inherits the same cap.  This is a
local p theorem, not a global p theorem.

The source hypotheses and printed residual are from commit
84b393ec1bc52fa662756bd117a45537007d086a, note blob
dda538a9a36cd0c8e267c11600a49cdc5bf054d1.

## 3. Exact F_17 counterexample for the printed key

Work over D=F_17^*, with

    r=2, beta_1=16, c=11.

Enumerate every two-element A subset D, form U=L_A and V=U-c, and retain the
case when V splits squarefreely over D with roots R.  For each singleton
G={g} disjoint from A union R retain the packet when

    g+P_1(A)=16.

Because U-V is constant, g+P_1(R)=16 also holds.  Order packets
lexicographically by (S,S',U,G), where S=G union A and S'=G union R, and keep
the first packet per Rule-1 key (r,c,U,beta).  The exhaustive bucket has 38
packets and 38 distinct U, so this deduplication removes none.

The canonical representative is

    G0={2}, A0={1,13}, R0={15,16},
    U0=X^2+3X+13, V0=X^2+3X+2.

Among the other packets, the exact gcd histogram is

    H=1: 25,
    H=X+1: 3,
    H=X+2: 3,
    H=X+4: 4,
    H=X+16: 2.

Thus the one printed key (r,c,U0,H=1,beta) has 25 comparisons.  For each set

    mu=1_(A0)+1_R-1_(R0)-1_A,
    kappa=1_(A0 intersect G)-1_(R0 intersect G),
    lambda=mu-kappa.

The deterministic verifier proves:

- mu_k=0 for k=0,1,2;
- lambda_k=-kappa_k for k=0,1,2 and lambda is disjoint from literal G;
- 24 of 25 full mu and all 25 exact off-core lambda are projectively
  primitive under scalar/sign transport;
- all 25 fail the extension deletion mu_3=0;
- all 25 U, affine shifts K=U-U0, full mu, lambda, and packets are distinct;
- lambda support sizes have histogram {5:1,6:5,7:13,8:6};
- exact contact is empty in 16 rows and nonempty in 9 rows;
- every marked degree-0..2 Vandermonde has rank 3 and a nonzero
  lexicographic three-column minor;
- no support-collapse or corank-one BC case occurs.

Consequently

    24 > 17

refutes any p-cap derived from the unsplit printed key shape and checked
Rule-2 predicates alone; it does not refute the fully filtered residual X.
The genuine nonempty-contact lambda subfamily has only 9 rows and does not
refute its own p-cap.  There are 13 literal G fibers, with maximum size 4.
Adding G to the key splits the full residual exactly where the Newton theorem
predicts.  This
fixture is algebraic preflight evidence.  It does not assert P0/P1 admission
or complete execution of every named first-match deletion.

## 4. Independent beta-omission stress test

A second exhaustive fixture fixes literal G={1} over F_101 but lets beta vary:

    r=2,
    U0=(X-1)(X-2),
    c=1,
    V0=U0-1=(X-24)(X-80),
    H=1,
    U=U0+aX+b,
    V=U-1.

Requiring U,V to split squarefreely over F_101^*, requiring
Roots(U) disjoint {1,2} and Roots(V) disjoint {1,24,80}, and excluding
(a,b)=(0,0) gives 2098 distinct primitive
inhomogeneous lambda.  Exactly 21 extend through degree 3, leaving 2077>101.
Every lexicographic marked Vandermonde minor is nonzero.  Grouping by

    beta_1=4-a

has maximum fiber size 23, consistent with the fixed-(G,beta) theorem.  This
fixture shows beta cannot be silently omitted at all depths.  It is not a
post-first-match deployed-row counterexample.

## 5. Correct global owner theorem

Fix primitive z after the literal named deletions.  Let Gen_z be the generated
support objects and Prim_z the admitted primitive packets.  Let Base_z be the
set of complete keyed off-core bases (K(P),lambda(P)) that preserve literal G.

A sufficient factorized theorem is:

    Prim_z injects into the disjoint union over b in Base_z of Profile(b),
    |Profile(b)|<=t for every b,
    |Gen_z|+t|Base_z|<=t p.

Then

    |Gen_z|+|Prim_z|<=t p.

The last displayed weighted inequality is the global add-back.  It cannot be
replaced by a statement saying each fixed key has at most p lambda values:
that only gives a factor of the number of keys.

The minimal direct owner is an injection

    Gen_z disjoint_union Prim_z -> Fin(t) x F_p

whose decoder recovers the literal support and common core G.  At the deployed
seam the codomain size is

    67472*2130706433=143763024447376.

## 6. Pivot routing and nonclaims

The F_17 and F_101 fixtures have a nonzero marked Vandermonde pivot for every
member, but many members share a field-sized pivot codomain.  Nonzero pivot is
therefore a chart condition, not an injection or payment.

For an actual incidence matrix, vanishing of all maximal minors may be routed
only through the typed adapter at commit
a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0 (note blob
f24ce928df7e7170c1b4f3228d5fe9b184be50b4).  The toy weighted Vandermonde in
this packet is not substituted for that actual matrix.  No vanishing family
is left unrouted: the fixtures are full rank, and any future actual all-minors
vanishing family must use that owner.

This packet does not use low moments as a payment, Johnson packing,
mode-at-null, image-only normalization, or zero-defect reduction.  It preserves
the literal common-core marking throughout.

## Verdict

The proposed primitive certificate remains unproved because the exact named
deletions are not executable and the global marked-key add-back is absent.
The F_17 fixture refutes a p-cap from printed-key shape and checked Rule-2
predicates alone, not the fully filtered residual X.  The repaired
fixed-(G,beta) p-cap is proved locally, but it cannot supply the r profile
factor and it does not sum over keys.

The obstruction floor is

    MARKED_CONTACT_RECOVERY_KEY_MULTIPLICITY.
