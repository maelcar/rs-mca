# Cycle 1 F1 Arbitrary-Anchor Audit

Status: `BANKABLE_LEMMA` for a narrow reduction; `EXACT_NEW_WALL` for the remaining bound.

Raw input:

- `raw/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_RAW.md`

Prompt:

- `prompts/20260618_cycle1_f1_arbitrary_anchor.md`

Run receipt:

- Packy run id: `2026-06-17T19-48-20-428Z-cycle1-f1-arbitrary-anchor-20260618-37d26898`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T19-48-20-428Z-cycle1-f1-arbitrary-anchor-20260618-37d26898`
- Model: `claude-opus-4-8`
- Mode: `artifact_stream`
- Status: `OK`

## Codex Verdict

The answer is significant, but its headline `PROOF` is too strong if read as a solved F1 theorem. Bank the algebraic reduction, not the claimed endpoint.

## Bankable Content

For the quadratic field-transfer setting `B=F_p`, `F=F_{p^2}`, `D subset B`, balanced `t=sigma`, and arbitrary anchor `w:D->F` in `tex/slackMCA_v3.tex:def:residue`:

1. Balanced witnesses are forced by interpolation on any `a=k+t` support. If `Q_z` has degree `<a` and agrees with `w` on at least `a` points, then on any `a`-subset `S` of the witness support,

   ```text
   Q_z = interp_S(w).
   ```

2. After choosing a `B`-basis `1, alpha` of `F`, write

   ```text
   w = w0 + alpha*w1,  w0,w1:D->B.
   ```

   Since `D subset B`, the Lagrange basis for `S` has coefficients in `B`, hence

   ```text
   interp_S(w) = interp_S(w0) + alpha*interp_S(w1)
   ```

   with both component interpolants in `B[X]`.

3. For `E in F[X]`, let

   ```text
   Ehat = lcm(E,E^tau) in B[X].
   ```

   Because `E | Ehat`, the slope condition

   ```text
   [interp_S(w)]_E = z [Bnum]_E
   ```

   factors through the paired base readout

   ```text
   S -> ( interp_S(w0) mod Ehat, interp_S(w1) mod Ehat )
        in (B[X]/Ehat)^2.
   ```

Thus arbitrary anchors do not create a new extension-valued invariant in the quadratic case. They enlarge the base object from the monic locator readout `S -> [L_S]_Ehat` to a paired interpolation-residue readout.

## Downgraded / Rejected Overclaims

1. The answer should not be cited as a full `PROOF` of balanced F1. It proves a factorization/reduction, not the required packing bound.

2. The proposed "generalized per-fiber collision problem" is not safe as stated for arbitrary base words. Low-degree/codeword anchors can make interpolation residues independent of `S`, producing huge fibers. Huge fibers may correspond to few slopes, so the correct endpoint is a slope-image or bad-locus packing statement, not a raw fiber-size statement for every arbitrary anchor.

3. The answer's line "no arbitrary-anchor counterpacket exists above the monic case" is too broad. What is supported is narrower:

   ```text
   no extension-only arbitrary-anchor invariant remains after the paired base readout reduction.
   ```

   A base-field arbitrary-anchor packing obstruction is still possible and must be audited separately.

4. Dimension bookkeeping must be stated carefully. The paired readout lies in `(B[X]/Ehat)^2`, so its `B`-dimension is `2 deg(Ehat) <= 4t` in the quadratic case. The monic locator readout uses one copy.

## Updated Wall

The live F1 wall is no longer "do arbitrary anchors escape the base field?" They do not, in the quadratic setting covered by the answer.

The live wall is:

```text
Bound the slope image of the paired base interpolation-residue readout
S -> (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
on the bad locus [interp_S(w)]_E in F*[Bnum]_E,
after tangent/contained and quotient-periodic contributions are separated.
```

This wall is a base-field arbitrary-anchor analogue of `prob:perfiber`, but it must not be formulated as a raw uniform fiber bound over all `w0,w1`.

## Why It Matters

This narrows F1 substantially:

- unrestricted same-numerator extension lift remains cut;
- unbalanced data remain routed to residual list;
- monic balanced data route to `S -> [L_S]_Ehat`;
- arbitrary balanced data route to a paired base interpolation-residue object.

The extension-field ledger is therefore no longer the immediate F1 obstacle in the quadratic balanced case. The obstacle is the base-field arbitrary-anchor packing/local-limit problem.

## Next Prompt

Ask the next worker to audit this reduction as an adversary:

- find a flaw in the forced-interpolant/base-split/readout factorization; or
- prove a corrected slope-image packing statement; or
- produce a finite base-field arbitrary-anchor packing counterpacket.
