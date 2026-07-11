# M31 common-height ADE cut: integral-D_s proof repair

**Status:** `PROVED` for the integral-coordinate `D_s` sub-case below;
`FIXED` for the sole proof-completeness gap isolated by PR #648; no change to
the classifier, threshold, census, seven audited census hashes, or remaining
walls.
Independent promotion review is still requested before any statement is moved
into the frontiers TeX.

**Lineage:** DannyExperiments PR #637 supplied the common-height ADE cut and
the exact 113,864-row delta. Claude/holmbuar PR #648 independently reproduced
all counts and seven hashes and verified every proof step except the compressed
integral-coordinate `D_s` sentence. This packet supplies precisely that missing
argument on integrated base `5c9aab7`; it does not replace PR #648's audit.

**Replay:**

```text
python3 experimental/scripts/verify_m31_ade_integral_ds_repair.py --write
python3 experimental/scripts/verify_m31_ade_integral_ds_repair.py --check
python3 experimental/scripts/verify_m31_ade_integral_ds_repair.py --tamper-selftest
```

The verifier is standard-library-only, imposes a 1 GiB address-space cap, and
writes
`experimental/data/certificates/m31-ade-integral-ds-repair/`
`m31_ade_integral_ds_repair.json`.

## 1. Exact local statement

Let `S_C` be selected roots in an irreducible `D_s` component, realized as

```text
{ +/-e_i +/-e_j : 1<=i<j<=s }.
```

Assume the roots are distinct, every two distinct selected roots have inner
product in `{0,1}`, and a dual vector `z` has height
`<alpha,z>=1` on every selected root. In the integral-coordinate sub-case
write `z=(z_1,...,z_s) in Z^s`, put `Z_C=sum_i z_i^2`, and assume

```text
Z_C <= rho,       8 < rho < 17/2.
```

Then

```text
|S_C| < rho*s.                                            (R)
```

This is the exact per-component estimate asserted in #637 Section 4. It is
stronger than the component allowance needed for the global bound
`|S|<=rho*r+4rho(16-rho)`.

## 2. Hypothesis audit

| Printed hypothesis | Exact use in the repair | Supplied to the consumer? |
|---|---|---|
| `D_s` roots are `+/-e_i+/-e_j` | every root has a two-coordinate support and four possible signings | Yes: standard `D_s` realization stated in #637 Section 4 |
| `z` is in the dual lattice, integral-coordinate branch | `z_i` are integers, so nonzero coordinates cost at least one unit of `Z_C` | Yes: #637 Section 3 puts `zeta` in the dual lattice and Section 4 splits integral/half-integral coordinates |
| `<alpha,z>=1` | rules out zero-zero supports, locates zero-coordinate roots at unit anchors, and bounds signings on an internal support | Yes: equation (7) |
| distinct pairwise inner products lie in `{0,1}` | only nonnegativity is used to force sign consistency at a zero coordinate | Yes: equation (6) and the lemma statement |
| `Z_C<=rho<17/2` | integrality gives `Z_C<=8`, hence at most eight nonzero coordinates | Yes: component norm is bounded by the total norm in (7) |
| `rho>8` | upgrades the exact `<8s` count to `<rho*s` | Yes: apply the lemma with the fixed boundary upper bound `rho=rho_0=rho(277868)`, where `8<rho_0<17/2`; monotonicity gives `||zeta||^2<=rho(t)<=rho_0` for every classified `t>=277868` |

No irreducible-rank lower bound beyond `s>0`, no assumption that every
nonzero coordinate equals `+/-1`, and no assumption that internal-support
roots are absent is used. The half-integral `D_s`, `A_s`, and `E` cases are
unchanged and were already marked `PROVED` by PR #648.

For convention clarity, duality against `e_i-e_j` and `e_i+e_j` gives
`z_i-z_j,z_i+z_j in Z`. Thus `2z_i in Z` and the standard dual-coordinate
dichotomy is exactly integral versus half-integral; the repair invokes only
the former branch.

## 3. Proof

Because `Z_C` is an integer and `Z_C<=rho<17/2`,

```text
Z_C<=8.
```

Let `K={i:z_i!=0}` and `k=|K|`. Every nonzero integral coordinate contributes
at least one to `Z_C`, so `k<=8`. If `k=0`, height one is impossible and there
are no selected roots.

Fix a zero coordinate `j notin K`. A height-one root on support `{i,j}` has
the form

```text
sign(z_i)e_i + delta*e_j,       |z_i|=1, delta in {+1,-1}.
```

For roots with different anchors, their inner product is the product of their
`e_j`-signs. Pairwise nonnegativity therefore forces those signs to agree. If
one anchor contributes both signs, either sign conflicts with any root at a
different anchor, so that anchor is the only one and contributes at most two
roots. Otherwise there is at most one root per anchor. Hence a fixed zero
coordinate supports at most `max(2,k)<=8` selected roots, and all supports
meeting a zero coordinate contribute at most `8(s-k)`.

Now take a support `{i,j}` contained in `K`. Two distinct nonopposite roots on
that support differ in exactly one sign. Subtracting their two height-one
equations gives `2z_i=0` or `2z_j=0`, contradicting membership in `K`.
Opposite roots have opposite heights. Thus there is at most one selected root
on each internal support, for at most `binom(k,2)` further roots.

Combining the two types gives the all-rank symbolic envelope

```text
|S_C| <= 8(s-k)+binom(k,2)
      = 8s-k(17-k)/2
      < 8s
      < rho*s,                    1<=k<=8.                (1)
```

The strict middle inequality has exact gap `k(17-k)/2>0`. This proves (R).

## 4. Machine checks and their scope

The verifier checks four separate layers:

1. It exhausts the `2k` possible unit-anchor/sign roots at one zero coordinate
   for every `0<=k<=8`; the exact compatible maximum is `0,2,2,3,...,8`.
2. It exhausts every possible pair of nonzero integral coordinates allowed by
   `z_i^2+z_j^2<=8` and confirms at most one height-one signing per internal
   support.
3. It checks the symbolic gap `k(17-k)/2>0` for every possible `1<=k<=8`.
4. It runs two genuine negative controls: if inner product `-1` is permitted,
   all 16 signed roots at eight unit anchors coexist; if the norm cap permits
   nine unit anchors, the local maximum is nine. Both violate the eight-root
   cap and expose exactly where the printed hypotheses are load-bearing.

Layer 3 compares the two affine-in-`s` coefficient pairs exactly; together
with the written support argument, it is the proof for arbitrary rank. The
finite sign catalogues are local checks, not the all-rank proof.

The verifier also pins the unchanged #637 verifier and JSON byte-for-byte,
checks the exact M31 boundary rational, confirms the delivered real/modular
rank gap remains 15 while the determinant step needs 11, and re-reads the
already-audited counts and hashes without regenerating or relabeling them.

## 5. Exact consumer and verdict transition

For #637's actual family of constant-weight supports, equations (6)-(7) supply
every hypothesis in Section 2. Since `rho(t)` decreases, use the fixed lemma
parameter `rho=rho_0`, where

```text
rho_0=rho(277868)=582731431936/70500333905 in (8,17/2).
```

Then `||zeta||^2<=rho(t)<=rho_0`, so the repaired lemma applies to every
classified `t>=277868`. The remainder of
the rank/Smith/determinant proof was audited `NO ISSUE` in PR #648. Therefore
its sole `OPEN GAP` is fixed, restoring soundness of the already-counted band

```text
(2,t,t,2t), 277868<=t<=391731,
```

namely 113,864 new exclusions and the exact two-shell residual change
`3,101,276 -> 2,987,412`. No row, threshold, or rank floor changes, and none
of the seven audited census SHA-256 digests changes.

In the original component summation, the repaired integral branch contributes
strictly less than `rho_0*s` and hence no positive excess. The half-integral
branch remains bounded by `rho_0*s+4(16-rho_0)Z_C`, while the `A` and `E`
bounds are unchanged. Consequently the global additive term remains exactly
`4rho_0(16-rho_0)`: the audit's acceptance margin is untouched, with delivered
rank gap 15 against exact minimum 11. For the patched statement, PR #648's
classifier-soundness verdict therefore upgrades from `OPEN GAP` to `NO ISSUE`.

The only integrated prose consumer is `experimental/agents-log.md`; no paper
TeX currently cites this theorem. Promotion remains gated on independent
hypothesis review of this repair and an updated audit verdict.

## 6. Credits and nonclaims

Credit remains with DannyExperiments for #637's ADE construction and exact
census, and with Claude/holmbuar for #648's adversarial audit that isolated the
one missing sub-case. This repair claims no new exclusion beyond #637, no
additional `kappa` or shell case, no complete M31 upper ledger, and no deployed
CAP25 solution. No paper TeX is changed.
