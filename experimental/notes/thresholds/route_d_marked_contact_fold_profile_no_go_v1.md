# Route-D marked-contact fold/profile no-go v1

STATUS: COUNTEREXAMPLE

## Result

A same-cell Route-D Rule-2 defect has an exact contact/off-core decomposition,
but neither part is accepted by an existing typed owner.  The contact with the
deleted packet's carried canonical core can be isolated and reconstructed using
at most `r` nonempty occupancy-profile labels for each fixed off-core signed
weight.  This is not a payment: the off-core weight has an inhomogeneous
moment target, and no current owner bounds the full fixed-key `lambda` family by
`|F|`.

The tempting large signed-defect fold is exactly inert.  It multiplies both
Rule-2 locator products by the same locator of the contact-free part of the
core.  Exact gcd cancellation removes that factor and returns the original
contact-bearing reduced defect.  Thus it preserves the canonical mark and
generated field, but it supplies no new primitive support unit.

At the deployed minimal seam, `r=67472` and `p=2130706433`.  A hypothetical
typed theorem bounding the full admissible off-core `lambda` family by `p`
for each fixed carried representative/recovery key would combine with the
at-most-`r` relative profiles per `lambda` to give, for that one fixed key, exactly

```text
67472 * 2130706433 = 143763024447376.
```

That `lambda`-family owner is absent.  The exact new obstruction is

```text
MARKED_CONTACT_INHOMOGENEOUS_OFFCORE_OWNER.
```

This packet does not execute the named first-match deletions and does not
prove or refute the deployed primitive support bound.

## 1. Canonical same-cell data

Let `F` be a field, `D subset F^*`, and let two canonical degree-`r` boundary
packets in one Rule-2 cell be

```text
P_0=(G_0,A_0,R_0),       P=(G,A,R),
S_0=G_0 disjoint_union A_0,  S'_0=G_0 disjoint_union R_0,
S  =G   disjoint_union A,    S'  =G   disjoint_union R.
```

Assume `A_0 cap R_0=empty`, `A cap R=empty`, and all four sides have size
`r`.  Put

```text
U_0=L_(A_0), V_0=L_(R_0), U=L_A, V=L_R,
U_0-V_0=U-V=c != 0,
L_+=U_0 V, L_-=V_0 U,
H=gcd(L_+,L_-).
```

The reduced Rule-2 signed weight is

```text
mu=1_(A_0)+1_R-1_(R_0)-1_A.                         (MC1)
```

After division by `H`, the valuation difference is still `mu`.  In the
depth-`r` Rule-2 branch its moments satisfy

```text
mu_k=sum_x mu(x)x^k=0, 0<=k<=r.                     (MC2)
```

These are algebraic packet hypotheses.  Admission to a post-first-match
branch is not inferred.

## 2. Exact contact/off-core split

Define

```text
C_+=A_0 cap G, C_-=R_0 cap G, C=C_+ disjoint_union C_-,
kappa=1_(C_+)-1_(C_-),
lambda=mu-kappa.                                    (MC3)
```

**Theorem 1 (canonical marked-contact split).**

```text
mu restricted to G = kappa,
supp(lambda) cap G = empty,
lambda_k=-kappa_k for 0<=k<=r.                      (MC4)
```

Proof.  The packet sides `A,R` are disjoint from their canonical core `G`.
On `G`, their two terms in `(MC1)` vanish, leaving exactly the representative
contacts in `(MC3)`.  Subtracting gives the support statement.  Equation
`(MC2)` then gives the moment statement.  QED.

The Rule-2 gcd cannot remove this contact.  Rootwise,

```text
Roots(H)=(A_0 cap A) disjoint_union (R_0 cap R).     (MC5)
```

Indeed, a common root of `U_0V` and `V_0U` must be in one of the four pairwise
intersections.  The intersections `A_0 cap R_0` and `A cap R` are empty, so
only the two displayed intersections remain.  They have multiplicity one.
Since `G` is disjoint from `A union R`, `(MC5)` is disjoint from `G`; hence
every root of `C` survives exact gcd reduction with coefficient `+1` or `-1`.

## 3. Exact large-fold cancellation-back theorem

Put

```text
F_0=G minus C.
```

The disjointness assumptions above give `F_0 cap (A_0 union R_0 union A union
R)=empty`.  Define the dense folded products

```text
widehat L_+
 =L_(G minus C_-) L_(A_0 minus G) L_R,
widehat L_-
 =L_(G minus C_+) L_(R_0 minus G) L_A.              (MC6)
```

**Theorem 2 (large fold is a common-factor inflation).**

```text
widehat L_+=L_(F_0)L_+,
widehat L_-=L_(F_0)L_-,
gcd(widehat L_+,widehat L_-)=L_(F_0)H.              (MC7)
```

Consequently the reduced quotients of the folded pair are exactly the
original reduced quotients `M_+=L_+/H` and `M_-=L_-/H`.

Proof.  The two set identities

```text
G minus C_- = F_0 disjoint_union C_+,
G minus C_+ = F_0 disjoint_union C_-
```

turn `(MC6)` into the first two factorizations in `(MC7)`.  The load-bearing
disjointness condition makes `L_(F_0)` coprime to `L_+L_-`.  Monic gcds in
`F[X]` therefore give the third identity, and exact division cancels
`L_(F_0)` from both sides.  QED.

The corresponding signed moment identity is

```text
1_(C_+)-1_(C_-)
 =1_(G minus C_-)-1_(G minus C_+).                  (MC8)
```

Equation `(MC8)` looks like a large signed support, but the two dense sides
share `F_0`; `(MC7)` is its exact cancellation.  Counting the dense sides
before gcd reduction would be a common-divisor inflation, not a primitive
support transfer.  The construction introduces no roots outside `D`, changes
no generated field, and carries the literal canonical `G` throughout.

## 4. Exact profile compiler

Write

```text
a=|C_+|, b=|C_-|, d=a-b=-lambda_0.
```

Inside the two disjoint representative blocks `A_0,R_0`, form

```text
Q=C_+ disjoint_union (R_0 minus C_-).               (MC9)
```

It has exact labeled occupancies `(a,r-b)` and

```text
P_k(Q)=P_k(R_0)+kappa_k=P_k(R_0)-lambda_k,
1<=k<=r.                                            (MC10)
```

The exact signed local-minority theorem applies structurally to this fixed
two-block profile when `char(F)>r`.  Its total minority size is

```text
min(a,r-a)+min(b,r-b)<=r.
```

Therefore its depth-`r` power-sum map is injective: for fixed `(a,b,lambda)`,
equations `(MC9)-(MC10)` uniquely reconstruct `Q`, hence

```text
C_+=Q cap A_0, C_-=R_0 minus Q.                     (MC11)
```

This use is only an exact reconstruction lemma.  It is not a low-moment or
Johnson payment and does not bound the number of possible `lambda`.

**Theorem 3 (at most `r` nonempty profile labels).**  For fixed `lambda`, the
number of feasible nonempty pairs `(a,b)` is at most `r`.

Proof.  The difference `d=a-b=-lambda_0` is fixed.  If `d=0`, the feasible
pairs are `(1,1),...,(r,r)`, exactly `r` after excluding empty contact.  If
`d!=0`, there are exactly

```text
r+1-|d|<=r
```

solutions in `[0,r]^2`.  QED.
The compiler thus separates contact with at most `r` profile labels only after
`lambda` is fixed, while retaining `G`, the representative packet, and every
Rule-2 recovery key.  Globally the nonempty actual `(a,b)` profiles number
`(r+1)^2-1`; the at-most-`r` statement cannot be summed before fixing
`lambda`.  It also does not turn `lambda` into a zero-moment defect: by `(MC4)`
its target is the generally nonzero vector `-kappa`.

## 5. Conditional owner bridge and exact obstruction

The exact statement which would reach the desired scale is conditional.

**Corollary 4 (hypothetical `lambda`-family owner bridge).**  Fix one
carried representative/recovery key `mathfrak K`.  Let `Lambda_mathfrakK` be
the set of full off-core signed weights/targets `lambda` occurring in admitted
packets with that key after the literal named first-match deletions.  Suppose

```text
|Lambda_mathfrakK| <= |F|,
and every packet injects into (lambda, its nonempty lambda-relative profile).
                                                        (LAMBDA_OWNER_p)
```

The second line includes recovery of the original packet from the carried key,
`lambda`, and the reconstructed contact; it is not inferred from a pivot
value.  Theorem 3 then gives at most `r|F|` packets for this one fixed key.  At
the deployed seam the conditional product is `143763024447376`.  A global
certificate would additionally need the literal first-match add-back over
carried keys.

Hypothesis `(LAMBDA_OWNER_p)` is much stronger than a scalar-pivot or
fixed-actual-profile cap, and it is not available:

1. `lambda` has the inhomogeneous moment target `-kappa`, so the existing
   zero-moment weighted SP/Padé stratum does not accept it;
2. marked-exclusion cross-Gram reconstruction retains output
   multiplicities and supplies no pointwise `p`-cap;
3. the marked puncture recursion requires padding outside its carried mark,
   whereas `C subset G` lies inside the canonical mark;
4. repeated-side/planted descent requires the same side polynomial, which
   contact does not imply;
5. the fold in Theorem 2 is consumed by common-divisor cancellation and
   returns the original defect.

Thus the remaining typed obligation is exactly
`MARKED_CONTACT_INHOMOGENEOUS_OFFCORE_OWNER`.

The profile count must not be confused with a support count.  Already for a
balanced representative profile the raw number of contact choices is

```text
binom(r,floor(r/2))^2.
```

At `r=67472` this is larger than `r*p`; the verifier checks the comparison
without printing the enormous integer.  The fixed-profile theorem injects
these choices into a full `r`-coordinate moment target, not into one field
scalar.

## 6. Pivot and fixed-subgroup dichotomy

Let `M_A(gamma)` be the field-native matrix of an actual marked residual
incidence accepted by the existing rank-drop interface.

**Theorem 5 (legal pivot dichotomy).**

- If every maximal minor of the actual matrix vanishes, then
  `rank_F M_A(gamma)<t` and the slope is routed once to
  `DEEP_MCA_RANK_DROP`, carrying `G` and every marked key unchanged.
- Otherwise choose the lexicographically first nonzero maximal minor.  This
  gives a full-rank chart, not a count.  Its value has at most `|F|-1` possible
  labels but may have arbitrary multiplicity.

A raw contact or weighted-Vandermonde pivot is not the actual incidence
matrix consumed by the owner.  In particular, nonvanishing does not inject
packets into `F`, and vanishing of one selected minor is not rank drop.

Fixed-subgroup folding also does not remove this obligation.  On a primitive
fixed parent target, the diagonal cross-section theorem says that every
scalar orbit meets the fixed-target slice at most once.  A subgroup visible
only after forgetting the parent target cannot act on the typed packet unless
it also preserves the cell, the canonical `G`, and both representative sides.
Support stabilizers must first enter the existing quotient/planted branch;
free orbit representatives still require an owner.

## 7. Exact `F_31` replay

The verifier reconstructs the predecessor finite corpus over `F_31`:

```text
raw distance-three mates                 121
projectively primitive mates             119
depth-three children                       29
all-base comparison occurrences          245
contact-size histogram {1:81,2:109,3:27,4:28}
marked-disjoint occurrences                0
```

For all 245 occurrences it independently checks `(MC3)-(MC7)`, the moment
split through degree three, the exact Rule-2 gcd root formula `(MC5)`, and
cancellation back to the original reduced quotients.  This replay is a
conditional algebraic fixture, not an admitted first-match residual.

## 8. Exact provenance

The checked base snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- row-sharp prefix reduction: commit
  `e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
  `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- singleton top-seam Rule-2 schema: commit
  `84b393ec1bc52fa662756bd117a45537007d086a`, note blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- signed local-minority fixed-composition theorem: commit
  `208b4773687f0fbb01194ac20082872ec4a291cc`, note blob
  `376c21252b5ee167839c2d214f173428c0010ff4`;
- marked-exclusion cross-Gram theorem: commit
  `5c9aab794e6575d815541e0a5dd8534d03d400aa`, note blob
  `4ed789595305170556371c87c5773d9e14ba4307`;
- marked puncture recursion: commit
  `5343c5876e559e33b6d3bb332cb2d55edbfbcc4b`, note blob
  `7f8f2042c5fe0f5eb45f36f626ee47e4967e95c9`;
- F31 root compiler: commit
  `91a9e31284adb34a1dfe5c71e434aa709ba2d3fe`, note blob
  `97f6b77a877e7c7d8efdf4661ccf84856bd5d0fc`;
- marked-defect transfer no-go: commit
  `332153d6e74403e3ad20f367ff4a3df8406a30bf`, note blob
  `6ce5a571ca05f774a6569a9c78d9cb69e8fc896a`;
- marked all-maximal-minors adapter: commit
  `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`.

Every cited object is pinned by a full commit or blob SHA.

## 9. Nonclaims

- No named first-match deletion is executed.
- No conditional toy packet is called an admitted branch-excess unit.
- The `<=r` profile theorem is not a numerical support payment.
- No low-moment, Johnson-packing, mode-at-null, image-only, or zero-defect
  shortcut is used to close a branch.
- No raw algebraic pivot is routed to `DEEP_MCA_RANK_DROP`.
- No nonzero pivot value is treated as an injective field label.
- The canonical common core is not shrunk or replaced.
- No generated field is changed and no extension-field charge is introduced.
- The hypothetical `r|F|` bridge is scoped to one fixed carried key; no
  global carried-key add-back is proved.
- The deployed primitive support certificate remains undecided.

## 10. Reproduction and Lean layer

```bash
python3 experimental/scripts/verify_route_d_marked_contact_fold_profile_no_go_v1.py
python3 -O experimental/scripts/verify_route_d_marked_contact_fold_profile_no_go_v1.py
python3 experimental/scripts/verify_route_d_marked_contact_fold_profile_no_go_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_marked_contact_fold_profile_no_go_v1.py --tamper
(cd experimental/lean/route_d_marked_contact_fold_profile_no_go_v1 && lake build)
```

The standalone Lean module proves theorem-shaped contact restriction,
off-core vanishing on the mark, common-factor fold, cancellation-back,
profile-count arithmetic, the explicitly hypothetical owner bridge, and the
actual-incidence all-minors guard.  The exhaustive finite reconstruction stays
in the deterministic verifier.
