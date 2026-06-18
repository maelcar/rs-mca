# Cycle 5 Audit: W-F1-AA-RES

Status: EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-17T21-57-22-619Z-cycle5-restored-w-f1-aa-slope-image-20260618-3c19ab5e`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T21-57-22-619Z-cycle5-restored-w-f1-aa-slope-image-20260618-3c19ab5e`
- Lane: `artifact_stream` (clean theorem lane; no ads)
- Raw response copy: `../raw/20260618_CYCLE5_W_F1_AA_RES_RAW.md`

## Verdict

Cycle 5 is significant, but it is not a proof of F1 and not a fresh counterpacket.
It sharpens the active wall from generic paired-readout slope-image packing to
the reserve-indexed wall `W-F1-AA-RES`.

The source-valid content to bank is:

- Restored `W-F1-AA` is a faithful arbitrary-anchor extension-denominator
  instance of the residue-line packing object `Lambda^{NC}_{t,delta}` /
  `prob:perfiber`.
- The tangent / zero-numerator and quotient-periodic separations are necessary
  cleanups, but they do not bind the problem.
- The banked `sigma=1` fixed-rate counterpacket survives both separations and
  still gives `Theta(q_line)` slopes, so the missing invariant is the reserve
  scale `eta=sigma/n`.
- The next wall is a rigidity/value-count law for the paired readout
  `rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)`, analogous to
  `thm:rigidcyclo` / `thm:exactcount` for the monic prefix object.

## What Is Proved Or Source-Valid

The reduction of the Cycle 5 object to `Lambda^{NC}` is source-compatible with
Cycles 1-4:

- Cycle 1 and Cycle 2 reduce quadratic arbitrary anchors to the paired base
  interpolation-residue readout modulo `Ehat=lcm(E,E^tau) in B[X]`.
- Cycle 3 supplies automatic noncontainment for nonzero numerator on supports
  of size at least `a=k+t`.
- Cycle 4 verifies that balanced means `t=sigma`, hence `k+t=a=s_delta`; there
  is no extra high-agreement layer on an `a`-subset.

Thus the balanced nonzero-numerator count is legitimately a `def:residue` /
`prob:perfiber` instance, not a protocol statement and not list decoding.

## What Is Not Proved

Do not bank any of the following from Cycle 5:

- a proof of `conj:B` or `prob:perfiber`;
- a proof that above corrected reserve the paired readout has
  `n^{1+o(1)}` slopes;
- a protocol denominator saving or any use of `ass:extension-mca-lift`;
- a line-decoding theorem;
- a refutation of the corrected-reserve wall from the `sigma=1` counterpacket.

The `sigma=1` counterpacket is sub-reserve because `eta=sigma/n`.

## Exact New Wall

`W-F1-AA-RES`:

For quadratic `B=F_p`, `F=F_{p^2}`, `D subset B`, `E in F[X]\B[X]` with
`deg E=t=sigma`, nonzero numerator `Bnum`, and arbitrary
`w=w0+alpha*w1`, develop:

1. a rigidity / value-count law for the paired readout `rho` on the bad line
   `F*[Bnum]_E`;
2. a reserve threshold `eta*_{AA}(rho,q_gen)` separating the sub-reserve
   `Theta(q_line)` regime from the conjectural above-reserve
   `n^{1+o(1)}` regime;
3. the generated-field ledger needed to say when the count is controlled by
   `q_gen` and quotient profile data rather than by `q_line`.

## Field Ledger

- `q_gen=p`: generated/base field for `D subset B` and base readout
  components.
- `q_line=p^2`: extension/line field where slopes `z` live.
- `q_chal`: not used; no protocol challenge-field saving is claimed.
- `B`: base/generated field.
- `F`: ambient extension/line field.

## Next Prompt Implication

The next high-value target is not another broad W-F1-AA summary. It should attack
the first missing invariant in `W-F1-AA-RES`: either prove a rigidity/value-count
law for the paired readout, find a balanced finite/symbolic counterpacket after
reserve and quotient separation are stated correctly, or cut the proposed wall by
pinpointing a false reduction.
