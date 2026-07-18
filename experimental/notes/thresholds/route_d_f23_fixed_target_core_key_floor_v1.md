# Route-D F23 fixed-target marked-core key-addback floor v1

STATUS: COUNTEREXAMPLE

## Result

The fixed split-shift key printed by the singleton Route-D schema is not a
global recovery key when the literal common core is allowed to vary.  Over
`F_23`, at fixed parent target, fixed Rule-2 cell, fixed representative, and
fixed exact gcd, there are `55` distinct primitive nonextension off-core
weights under the printed key

```text
(r,c,U0,H,beta).
```

They exceed both available toy label spaces:

```text
55 > |F_23| = 23,
55 > r*|F_23| = 2*23 = 46.
```

The literal marked cores take `21` values.  Fixing the core repairs the local
one-scalar theorem, but summing those fixed-core fibers is precisely the
missing global add-back.  The obstruction is named

```text
FIXED_TARGET_MARKED_CORE_KEY_ADDBACK_FLOOR.
```

This is a raw algebraic Rule-2 obstruction.  The exact named first-match
deletions are not executed, no actual marked-incidence matrix is constructed,
and no packet in the fixture is routed to rank drop.  It is not a
post-first-match counterexample and does not refute the deployed KoalaBear
support bound.

## 1. Source interface

The singleton schema at commit
`84b393ec1bc52fa662756bd117a45537007d086a` and note blob
`dda538a9a36cd0c8e267c11600a49cdc5bf054d1` supplies the following types.

- Rule 1 deduplicates by `(r,c,U,beta)` and retains the least literal core.
- Rule 2 chooses a canonical representative in the cell `(r,c)`.
- Its exact certificate carries `(r,c,U0,G,H,M_plus,M_minus)`.
- Its fixed split-shift stratum is printed as
  `X_(r,c,U0,H,beta)(z)`, with `G` varying inside the set.
- The required numerical bound is a sum over all printed fixed keys, not a
  bound for one fixed literal core.

The target support certificate is recorded at commit
`e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
`591c91a6aac6b48db0c16abc586b74d7a51e44e2`.  The present packet tests only
the key type feeding that target.

## 2. Exact F23 family

Work over

```text
F=F_23, D=F_23^*, r=2, beta_1=10, c=17.
```

A literal marked packet is a triple `(G,A,R)` satisfying

```text
|G|=1, |A|=|R|=2,
G cap (A union R)=empty,
U=L_A is monic split squarefree of degree 2,
R=Roots(U-c),
P_1(G)+P_1(A)=beta_1=10.
```

Put

```text
S=G disjoint_union A,
S'=G disjoint_union R.
```

Thus `G=S cap S'` is the literal common core; it is never erased, quotiented,
or replaced by an unmarked side pair.

Exhausting the unordered two-subsets `A subset F_23^*` gives exactly `75`
packets.  Their side locators `U` are pairwise distinct.  Indeed, once `U`
and the fixed target `beta_1` are known, `A=Roots(U)` and the singleton core is

```text
G={beta_1-P_1(A)}.
```

Therefore the Rule-1 least-core selector has no duplicate `(r,c,U,beta)` key
to delete in this family.

## 3. Canonical representative and exact gcd

Order packets lexicographically by `(S,S')`.  The first packet is

```text
G0={1}, A0={2,7}, R0={4,5},
S0={1,2,7}, S0'={1,4,5},
U0=(X-2)(X-7)=X^2+14X+14,
V0=U0-17=X^2+14X+20=(X-4)(X-5).
```

For every other packet put

```text
L_plus = U0*(U-c),
L_minus=(U0-c)*U,
H=gcd(L_plus,L_minus).
```

Because both packet sides are disjoint, the exact root formula is

```text
Roots(H)=(A0 cap A) disjoint_union (R0 cap R).
```

The complete gcd histogram among the `74` comparisons is

```text
H=1       56
H=X-2      5
H=X-4      5
H=X-5      4
H=X-7      4
```

The obstruction uses only the `56` comparisons with the fixed exact key
`H=1`.

## 4. Marked contact and off-core weight

For a comparison packet define

```text
mu=1_(A0)+1_R-1_(R0)-1_A,
C_plus=A0 cap G,
C_minus=R0 cap G,
kappa=1_(C_plus)-1_(C_minus),
lambda=mu-kappa.
```

The source sides `A,R` are disjoint from their own literal common core `G`, so

```text
mu restricted to G = kappa,
supp(lambda) cap G = empty.
```

The verifier checks the identities pointwise.  It also checks

```text
mu_k=0 for k=0,1,2.
```

This is the exact degree-two Rule-2 identity, not a low-moment payment.

Among the `56` fixed-`H` comparisons, exactly one has `mu_3=0` and is removed
as an algebraic extension candidate.  For each of the remaining `55`, the
verifier checks:

```text
mu_3 != 0,
|supp(lambda)| >= r+3 = 5,
lambda has no nontrivial F_23^* x {+-1} stabilizer,
all 55 lambda are distinct.
```

The support histogram is

```text
{5:1, 6:5, 7:21, 8:28}.
```

The literal marked cores take `21` values, with maximum fixed-core fiber `5`.
The contact profile histogram is

```text
(0,0):43, (1,0):6, (0,1):6.
```

Consequently this packet is a no-go for the complete global marked-core
add-back.  It does not claim that the nonempty-contact subfamily alone exceeds
`|F_23|`.

## 5. Cardinality no-go

Let `B` be the set of the `55` surviving complete algebraic bases
`(K,lambda)` under the common printed key

```text
K=(2,17,U0,1,(10)).
```

Since the weights `lambda` are pairwise distinct,

```text
|B|=55.
```

Therefore there is no injection

```text
B -> F_23
```

and no injection

```text
B -> {0,1} x F_23.
```

This refutes a global add-back theorem that fixes only the printed
`(r,c,U0,H,beta)` key and then attempts to encode all literal-core variation
by one field label, even with one extra `r`-profile label.

## 6. Correct fixed-core theorem

The finite obstruction does not contradict the following local result.

**Theorem (fixed literal core one-scalar cap).**  Let `F` be finite with
`char(F)>r`.  Fix a literal core `G`, a full parent prefix
`beta=(beta_1,...,beta_(r-1))`, and `c != 0`.  Among packets with

```text
A=Roots(U), |A|=r,
U monic split squarefree,
R=Roots(U-c),
P_k(G)+P_k(A)=beta_k for 1<=k<=r-1,
```

there are at most `|F|` possible `U`.

**Proof.**  Fixing `G` and `beta` fixes `P_k(A)` for `1<=k<=r-1`.
Newton identities are triangular and invertible because `char(F)>r`, so they
fix the first `r-1` elementary symmetric functions of `A`.  Equivalently, all
nonconstant coefficients of the monic degree-`r` locator `U` are fixed.  The
constant coefficient `U(0) in F` is the only remaining scalar, and hence
`U -> U(0)` is injective.  QED.

If `U0,H` are also fixed, literal `G` fixes `kappa`; the reduced coprime signed
divisor `lambda+kappa` fixes the monic pair `(M_plus,M_minus)`, and

```text
U=H*M_minus/(U0-c).
```

Thus the corresponding fixed-`G` lambda family also has size at most `|F|`.
The F23 family shows that this theorem cannot be summed after silently
dropping `G` from the key.

## 7. Pivot and rank-drop boundary

The projective-primitivity test above only excludes scalar/sign stabilizers of
the raw off-core weight.  It does not construct the actual marked residual
incidence matrix.

The all-maximal-minors adapter is owned by commit
`a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
`f24ce928df7e7170c1b4f3228d5fe9b184be50b4`.  Its legal interface is:

- if every maximal minor of the actual owner-typed matrix vanishes, route once
  to the existing rank-drop owner while carrying the literal `G`;
- otherwise a nonzero maximal minor selects a full-rank chart but supplies no
  count and no injective field label.

No actual matrix is available in this fixture, so no raw Vandermonde or contact
pivot is routed.  The missing admission/deletion compiler is recorded at
commit `8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`, note blob
`fdeabf0708cb8806feefae9322ed9002339332cf`.  Until that compiler is supplied,
the `55` objects are an unrouted algebraic obstruction floor rather than
post-first-match support units.

## 8. Provenance

The checked base snapshot is commit
`c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

- singleton Rule-2 schema: commit
  `84b393ec1bc52fa662756bd117a45537007d086a`, note blob
  `dda538a9a36cd0c8e267c11600a49cdc5bf054d1`;
- primitive support target: commit
  `e83962ae5ad7bacb391b691ffd37f0abef977b83`, note blob
  `591c91a6aac6b48db0c16abc586b74d7a51e44e2`;
- priority-zero admission gap: commit
  `8cb3b3ae4c57cf44ef13cda24e4532b3dbe1bb67`, note blob
  `fdeabf0708cb8806feefae9322ed9002339332cf`;
- actual all-maximal-minors adapter: commit
  `a6a3be8b1a967bbec5fa17fc9afa7daaf5b2d0c0`, note blob
  `f24ce928df7e7170c1b4f3228d5fe9b184be50b4`.

Every referenced packet is pinned by a full commit and note-blob SHA.

## 9. Nonclaims

- No exact named first-match deletion executor is claimed.
- No raw algebraic packet is called an admitted branch-excess unit.
- No raw Vandermonde, contact, or selected pivot is called the actual
  owner-typed incidence matrix.
- No single vanishing minor is routed to rank drop.
- No nonzero pivot is treated as an injective field label.
- No image-cell count is used as a support count.
- The literal common core is not forgotten, shrunk, or replaced.
- No deployed primitive support bound is proved or refuted.

## 10. Reproduction and Lean layer

```bash
python3 experimental/scripts/verify_route_d_f23_fixed_target_core_key_floor_v1.py
python3 -O experimental/scripts/verify_route_d_f23_fixed_target_core_key_floor_v1.py
python3 experimental/scripts/verify_route_d_f23_fixed_target_core_key_floor_v1.py --tamper
python3 -O experimental/scripts/verify_route_d_f23_fixed_target_core_key_floor_v1.py --tamper
(cd experimental/lean/route_d_f23_fixed_target_core_key_floor_v1 && lake build)
```

The standalone Lean module pins the exact cardinality obstruction, states the
fixed-core injection interface, and includes only the legal all-maximal-minors
rank-drop guard.  The exhaustive finite-field census remains in the
deterministic verifier.
