# Cycle 2 Paired Base Readout Retry Audit

Status: `BANKABLE_LEMMA` for the reduction; `EXACT_NEW_WALL` for the next target.

Raw input:

- `raw/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_RAW.md`

Prompt:

- `prompts/20260618_cycle2_retry_paired_base_readout_short.md`

Run receipt:

- Packy run id: `2026-06-17T21-02-03-967Z-cycle2-retry-paired-base-readout-short-20260618-024a717b`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T21-02-03-967Z-cycle2-retry-paired-base-readout-short-20260618-024a717b`
- Model: `claude-opus-4-8`
- Mode: `artifact_stream`
- Status: `OK`
- Elapsed: `377724 ms`
- Cost: `$1.05131125`
- Output tokens: `4823`
- Capture warning: none

## Codex Verdict

The retry answer is significant and agrees with the bounded Codex local audit. Bank the algebraic reduction and the sharpened wall. Do not promote this to a proof of F1, the corrected MCA local limit, or the extension-line MCA lift.

## Bankable Reduction

For the quadratic setting

```text
B=F_p, F=F_{p^2}, D subset B, balanced a=k+t with t=sigma,
w:D->F arbitrary, w=w0+alpha*w1 with w0,w1:D->B,
```

and a residue-line datum `(E,Bnum,w)` from `tex/slackMCA_v3.tex:def:residue`, every slope witness and every `a`-subset `S` of its support satisfies

```text
Q_z = interp_S(w) = interp_S(w0) + alpha interp_S(w1).
```

For

```text
Ehat = lcm(E,E^tau) in B[X],
```

the slope condition

```text
[interp_S(w)]_E = z [Bnum]_E
```

factors through the paired base readout

```text
rho(S) = (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
       in (B[X]/Ehat)^2.
```

This confirms the useful part of Cycle 1: arbitrary quadratic extension anchors do not introduce a new `S`-dependent extension-only invariant. They reduce to a base-field paired interpolation-residue object.

## Mandatory Caveats

1. `Ehat` must be the lcm for the full denominator `E` in the residue-line datum. If `E` has mixed factors, `Ehat=lcm(E,E^tau)` still suffices because `E|Ehat`; it is also the minimal base-field modulus with that property.

2. The slope `z` is unique whenever `[Bnum]_E` is nonzero in `F[X]/(E)`, even if `[Bnum]_E` is a zero divisor. Nonzero field scalars are units. If `[Bnum]_E=0`, the datum is degenerate/tangent rather than a numerator-preserving slope packing object.

3. Shrinking a witness support `S_z` with `|S_z|>a` to an `a`-subset preserves the forced interpolant and residue equation, but it may lose noncontainment. Thus `a`-subset readouts are safe for overcounting possible slopes, not for exact tangent/contained separation.

4. The quadratic readout has `B`-dimension `2 deg(Ehat) <= 4t`. In general extension degree `e`, the analogous component readout has `B`-dimension `e deg(Ehat)`, where `Ehat` is the lcm of Frobenius conjugates of `E`.

5. A raw uniform fiber bound over arbitrary anchors is false. Low-degree/codeword anchors make `interp_S(wi)` independent of `S`, so a raw readout fiber can contain all `a`-subsets. This does not imply many slopes, because a fixed nonzero numerator residue determines at most one scalar slope and degenerate anchors are contained/tangent.

## Exact New Wall

The live target is:

```text
W-F1-AA:
Bound the number of distinct scalar slopes z in F for which there exists
an a-subset S whose paired base readout lands on the fixed bad line
F * [Bnum]_E in F[X]/(E), while the original witness remains noncontained
after tangent/contained and quotient-periodic contributions are separated.
```

Equivalently, bound the slope image or distinct bad-locus readout classes, not the fibers of `S -> rho(S)`.

This is the arbitrary-base-anchor analogue of `tex/slackMCA_v3.tex:prob:perfiber`; the monic locator problem is the special case where the paired readout collapses to the usual locator/symmetric-function prefix.

## Rejected Upgrades

- Not a full F1 proof.
- Not a proof of `tex/snarks_v4.tex:ass:extension-mca-lift`.
- Not a protocol certificate claim.
- Not a line-decoding theorem.
- Not a list-decoding statement.
- Not permission to divide a base-field MCA numerator by `q_chal`.
- Not a raw per-fiber local limit for arbitrary anchors.

## Why It Matters

This closes one ambiguity in the F1 route. The immediate obstruction is not an uncontrolled extension-valued interpolation invariant in the quadratic balanced case. The obstruction is now sharper and base-fielded: prove a slope-image/bad-locus packing theorem for the paired interpolation-residue readout.
