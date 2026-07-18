# Rank-16 zero-profile scalar-line route cut

**Status:** Finite deployed-field theorem and source-realized route cut. The
certified ledger charge is zero; the official score remains `0/2`.

**Source floor:** `origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.
The construction extends, but does not reclaim, the delta-zero witness at
PR #890 head `a5b98c75d0e3732e9659d8fd220c821329e572e4`.

**Audit:** The independent repaired-proof audit returned `ACCEPT_NARROWED`.
Its immutable packet has SHA-256
`02bb8707b6329a43d947c7aacdaf3e05ace1c6a10c9387c8e916f7926be7c356`;
the frozen public audit contract has SHA-256
`4a24b64e0104fe616b02705ad7a56b3458bc2a325ec01be2781d90639c64bb6e`.

## Exact statement

Work over `F_p`, where

`p=2,130,706,433`, `n=2^21=2,097,152`, `K=2^20=1,048,576`,
`m=1,116,047`, and `B=2^15=32,768`.

Let `H=<omega>` be the order-`n` subgroup of `F_p^*`, with
`omega=3^1016=1,213,133,211 mod p`, and let the 64 deployed blocks be

`H_j={omega^(j+64k): 0<=k<B}`.

For a word `U:H->F_p`, write

`L(U)={P in F_p[X]: deg(P)<K and |Agr(U,P)|>=m}`.

The following finite theorem holds.

1. For every `P_*` and every nonzero `Q`, both of degree less than `K`, the
   intersection
   `{P_*+lambda Q: lambda in F_p} intersect L(U)` has at most 15 members.
   This is a global cap, not a claim that every word attains it.
2. If a listed scalar line has 15 members and common-core size
   `c=K-1-delta`, then `0<=delta<=2606`. If each of the 15 members has
   exactly `m` actual agreements, every petal has size `67,472+delta` and the
   unused remainder has size `36,497-14delta`.
3. The presentation class of a 15-member intersection is unique up to
   `AGL_1(F_p)`. Under `P_*'=P_*+aQ` and `Q'=bQ`, labels transform as
   `lambda'=(lambda-a)/b`. No distinguished canonical representative is
   claimed.
4. Every additional listed polynomial outside the scalar line misses at least
   2,213 points of the common core.
5. For every integer `0<=delta<=2606`, there is a literal deployed-field word
   containing an exact 15-member scalar line and an exact polynomial outside
   that affine line. All 16 displayed candidates have agreement profile
   `(e15,e16,e17,e18,e19,e20)=(0,0,0,0,0,0)` and `f64=0`, hence lie outside
   the current first-match stages `D,Q110,M,Q41,X175,J48,I`.
6. On the displayed packets the current pairwise complete-block agreement and
   error key-deletion inequalities exclude no owner key. Thus their certified
   complete-block resource-mask deficit is zero. The actual value-aware owner
   deficits are not claimed to vanish.

Consequently every displayed word has at least one displayed listed candidate
outside the scalar line and outside the current displayed first-match stages,
while the current complete-block resource-mask lower bound remains zero. This
is a finite, source-realized, zero-ledger route cut.

## Proof

Write the line as `P_i=P_*+lambda_i Q`. Its common core is

`C={x in H: Q(x)=0 and U(x)=P_*(x)}`, `c=|C|`.

Off `C`, each listed member uses a distinct ratio fibre of
`(U-P_*)/Q`. Therefore `c+r(m-c)<=n` for `r` listed members, and

`r<=floor((n-c)/(m-c))<=floor((n-K+1)/(m-K+1))=15`.

At `r=15`, integer rearrangement gives `c>=1,045,969`; at `r=16` it
would give `c>=1,050,640>K-1`. Writing `c=K-1-delta` gives
`0<=delta<=2606`. In the exact class, disjointness gives the petal and
remainder formulas above. The remainder is smaller than a petal, so no
sixteenth scalar label can be listed.

For an additional listed polynomial `P`, let `d` be the number of common-core
points on which `P!=P_*`. Root counting on each of the 15 petals and on the
remainder gives

`14d >= 30,975+E`,

where `E>=0` is the total petal excess above exact size. Hence `d>=2,213`.

For the literal all-delta construction choose root-fibre size `d0=4096` for
`0<=delta<=1757` and `d0=8192` for `1758<=delta<=2606`. Let

`K_i(d0)={omega^(i+(n/d0)q): 0<=q<d0}`.

Each `K_i(d0)` lies in block `H_i` and is a fibre of `x->x^d0`. Choose core
block counts `16,383-delta` in `H_0` and `16,384` in every other block, with
`K_0(d0)` inside the core and the 15 nonzero fibres outside it. Define

`Q=L_C`, `P_i=lambda_i Q`, `P=L_(C\K_0) X^d0`,

where the distinct nonzero labels are
`lambda_i=omega^(d0*i)/(omega^(d0*i)-1)`. Then

`Zeros_H(P-P_i)=(C\K_0) disjoint-union K_i(d0)`.

The verifier supplies a deterministic count compiler for the remaining point
sets. It balances the exact remainder over 64 blocks, reserves all 4,096
points of `K_i` in petal `i` in the low regime, and balances exactly
`75,664+delta` selected root points over the 15 literal diagonal fibres in the
high regime. A deterministic integral max-flow assigns every residual petal
point to a non-diagonal block while retaining at least one non-petal point per
block. In the low regime it balances `10,128+delta` companion agreements over
the remainder; in the high regime it uses no remainder agreement.

For all 2,607 delta cells, the compiler verifies the full block partition,
all 15 exact line totals, the exact nonlinear companion total, and literal
diagonal root intersections. The aggregate count certificate is:

- maximum petal block: `18,987`;
- line agreement-block range: `13,777..32,767`;
- companion agreement-block range: `5,585..21,602`;
- endpoint fingerprints:
  `0:16383-32198:12446-20639`,
  `1757:14626-32583:10716-20666`,
  `1758:14625-32583:6433-21546`,
  `2606:13777-32767:5585-21602`.

The first range after each delta is the line range and the second is the
companion range. Because every block occupancy is strictly between 0 and
`B`, all displayed candidates have the zero dyadic profile and `f64=0`.

For a line member, any 34 agreement blocks contain at most
`34*16,384+70,078<K`, any 32 contain at most
`32*16,384+70,078<K`, and any 29 error blocks contain at most
`29*(32,768-13,777)<=913,633`. For the companion, replace `70,078` by
`78,270` and `13,777` by `5,585`; the same three inequalities hold. Thus the
current complete-block key-deletion interfaces certify no owner vacancy on
these packets.

All locator roots are distinct elements of `H`. The right-hand sides used in
the construction are `alpha_i=omega^(d0 i)=(omega^i)^d0`, so they are explicit
`d0`-th powers. Since `p` does not divide `d0`, each
`X^d0-alpha_i` is squarefree and splits over `F_p` into exactly `d0` roots.
Every label denominator is nonzero. Defining `U` by the stated values on the
disjoint core, petals, companion-remainder set, and leftover points gives one
literal word, not merely an abstract support family.

## Replay record

The supplied verifier is Python-standard-library only, uses exact integer
ceilings, and contains no assert statements. Normal Python and `python -O`
produced the frozen expected output byte-for-byte. Nine semantic mutations
were caught: deployed generator, scalar cap, delta endpoint, regime switch,
owner threshold, exact agreement total, remainder total, diagonal root
reservation, and flow-column demand. Treat the transcript as untrusted and
replay it independently.

The final publication verifier incorporates the audit's exact-integer-ceiling
repair. Its normal and optimized outputs are byte-identical to the checked-in
expected output, all 2,607 transport cells saturate, and all nine semantic
mutations are rejected.

## Nonclaims

This theorem does not prove `|O(U)|+unowned(U)<=T`, any positive actual owner
deficit, the parent inequality `Delta_total>=12+u_notF`, completeness of the
16 displayed candidates, uniqueness of the nonlinear companion, attainment
of the 15-line cap for every word, a nonlinear companion for every 15-line,
impossibility of all support-only arguments, an asymptotic or extension-field
version, Grand MCA, Grand List, or an official theorem. The official score
remains `0/2`.

## Remaining wall

The exact value-aware deficit inequality on the displayed packets remains
open, as does control of every additional candidate outside the displayed
line. Any paying continuation must construct a source-valid disjoint owner or
add-back mechanism that controls all additional candidates, not only the 16
displayed polynomials or the present complete-block deletion masks.
