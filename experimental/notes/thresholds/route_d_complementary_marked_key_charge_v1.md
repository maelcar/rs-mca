# Route-D complementary marked-key charge v1

STATUS: PROVED

## Result

This packet proves the exact finite-set theorem that would make the Route-D
generated-support / primitive-defect add-back type-correct.

Let Generated and Defect be finite support families, let I be a row-index type,
let F be the scalar field, and let E be a marked subset of I x F.  Suppose
there are maps

    gamma : Generated -> I x F,
    delta : Defect    -> I x F

such that gamma and delta are separately injective, every gamma value lies in
E, and every delta value lies outside E.  Then the sum map

    Generated disjoint_union Defect -> I x F

is injective.  Consequently

    |Generated| + |Defect| <= |I|*|F|.

At the deployed Route-D shape, I=Fin 67472 and F=F_2130706433, so this gives

    |G_gen(z)| + |D_prim(z)| <= 67472*2130706433.

The theorem is unconditional.  Its application to the deployed residual is
conditional because no current packet supplies the two complementary
support-level injections.

## 1. SHA-pinned context

The target primitive support certificate is isolated at commit
e83962ae5ad7bacb391b691ffd37f0abef977b83.

The corrected fixed-marked-key quantifier theorem and its global key-addback
obstruction are at commit
b23f997474f7a7aec9a889d933c774acc4980050.

The global F17 marked-contact census at commit
6f56b42aff5758f354c72203b07831fd6241eef4 shows that a contact profile and a
nonzero toy pivot are not a support injection: 103 distinct contact weights
map to 30 labels.

The generated first-match ledger at commit
0955594bf354b6a396574b65fbb242715edd3267 bounds image cells, not support
multiplicity.  Generic ordered disjointization at commit
764f1c0243770baa437d4ae790b1448afa091680 sums supplied per-cell support
bounds but does not create them.  The asymptotic add-back shell at commit
4a2f0fbd8ab55ef107d26ebb5064a424430ca327 requires its own nondegeneracy and
mass-partition inputs.

The literal named deletion executor remains unavailable at commit
8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67.  Actual all-maximal-minors
vanishing is owned only by the typed rank-drop adapter at commit
a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0.

## 2. Strict cell-complement charge theorem

The proof is the disjoint-cell argument.

On the Generated summand use gamma.  On the Defect summand use delta.
Same-summand equality is resolved by the corresponding injection.  A
cross-summand equality would put the same cell both inside E and outside E,
which is impossible.  Therefore the sum map is injective into I x F and the
cardinality inequality follows.

The scalar-complement theorem is a stronger corollary.  For C subset F, take

    E={(i,a) in I x F : a in C}.

Then gamma landing over C and delta landing over F minus C imply the cell
hypotheses.  The converse is false because two branches may use different row
slots over the same scalar.

This is stronger than two independent estimates

    |Generated| <= |I|*|F|,
    |Defect|    <= |I|*|F|,

which only give twice the target.  It is also stronger than an image-size
bound for a noninjective labeling map.

## 3. Complete-base factorization

The following scalar-complement factorization remains a useful stronger
sufficient interface.  The primitive-defect charge may factor through a base
B and an explicit slot datum:

    encode  : Defect -> B x Profile,
    slot_b  : Profile -> Fin t,
    scalar  : B -> F_p,

with:

1. encode injective;
2. slot_b injective on the base-indexed realized subset of the ambient Profile
   type for every fixed b;
3. scalar injective on the realized bases;
4. scalar(b) outside C for every realized primitive base b.

Then

    delta(d)=(slot_base(d)(profile(d)),scalar(base(d)))

is injective.  The pair (base,profile) is the complete recovery key.  It must
retain every datum needed by the decoder, including the literal common core G,
the full prefix beta, U0, H, the selected cell, the off-core signed weight, and
any normalization or pivot chart datum.  Erasing any field requires a separate
proof that it is recoverable from the remaining data.

There is an important no-double-charge guardrail.  Once literal G and U0 are
inside B, the marked contact and its occupancy profile are already fixed.  If
B also contains the off-core signed weight and all packet identity, a contact
profile cannot supply an independent t-fold gain: its realized fiber is
trivially of size at most one.  Any nontrivial Fin t slot must therefore be a
separately defined residual datum with its own realized-fiber injectivity
proof, or B must be deliberately coarsened while literal-G recovery is proved
elsewhere.

The generated side must independently supply an injective charge

    gamma : G_gen(z) -> Fin t x C.

The set C may depend on the fixed primitive target z, but both sides must use
the same C_z.  More generally, the minimal theorem needs only an injective
primitive charge into the complement of the actual generated cell set E_z; it
need not exclude every row slot above a generated scalar.

## 4. Interface countermodel

An image-cell cap cannot substitute for the charge theorem.  Let

    L=Fin t x F_p,
    Generated=L x Fin 2,

and forget the copy bit.  The label image has exactly t*p points while the
support family has 2*t*p elements.  The generated image ledger remains true
and any unrelated primitive-defect family may be empty, but the target
support bound fails.

Likewise, a local one-scalar cap for every marked key gives a sum with a key
multiplicity factor.  First-match disjointness prevents double counting; it
does not remove that factor.

The deterministic verifier instantiates the scalar corollary and both
negative interfaces at t=2,p=5.  Its positive scalar-complement fixture splits
the scalar coordinates into C={0,1} and its complement, charges four generated
and six primitive-defect objects injectively, and saturates the ten-point
target.  Its image-only negative fixture has twenty generated supports but
only ten image labels.

It also gives the strict cell-complement fixture t=2,p=3.  Generated objects
use every scalar in row 0 and primitive objects use every scalar in row 1:

    E={0} x F_3,
    gamma(a)=(0,a),
    delta(a)=(1,a).

The six charges are injective, disjoint, and saturate 2*3.  Scalar separation
is impossible because both scalar projections equal all of F_3.  Thus an
arbitrary cell subset E_z is strictly more general than I x C_z.

## 5. RIM pivot dichotomy

This charge theorem does not replace the marked-incidence/fixed-subgroup RIM
dichotomy.

- If every actual maximal minor vanishes, route the family only through the
  SHA-pinned typed rank-drop adapter.
- If an actual pivot is nonzero, it certifies the chosen chart but not support
  injectivity.  Its output multiplicity must remain explicit until a charge
  map satisfying the theorem is constructed.

The F17 raw census has no vanishing toy pivot and therefore creates no new
rank-drop family.

## 6. Large signed-defect folding transfer

The theorem supplies the exact destination type for a successful large
signed-defect folding transfer.  After all named first-match deletions, such a
transfer must do one of the following:

- send an actual all-minors-vanishing family to the rank-drop owner;
- inject generated supports into a target-dependent cell set
  E_z subset Fin t x F_p;
- factor every primitive full-rank defect through a complete marked base and
  inject it into the full cell complement (Fin t x F_p) minus E_z.

The scalar-C interface remains a stronger sufficient specialization when
E_z=Fin t x C_z.

A transfer that outputs only an image label, contact profile, nonzero pivot,
unmarked side pair, or per-key scalar cap does not meet this interface.

## 7. Scope

This packet proves the abstract complementary-charge theorem and verifies its
finite boundary/countermodel fixtures.  It does not construct E_z, gamma,
delta, or the complete marked-base decoder for the deployed KoalaBear row.
It therefore does not prove the deployed primitive support certificate.

The literal common-core marking is preserved.  The packet does not use
low-moment payment, Johnson packing, mode-at-null, image-only normalization,
or zero-defect descent.

## Verdict

The minimal frame theorem is

    ROUTE_D_COMPLEMENTARY_CELL_CHARGE.

The scalar-coordinate specialization remains

    ROUTE_D_COMPLEMENTARY_MARKED_KEY_CHARGE.

It is sufficient for the desired t*p support certificate and exposes the
remaining research obligation without conflating image size, local key caps,
or pivot nonvanishing with support injectivity.
