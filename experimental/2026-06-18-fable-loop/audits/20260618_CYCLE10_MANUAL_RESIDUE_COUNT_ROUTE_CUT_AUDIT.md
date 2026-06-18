# Cycle 10 Manual Audit: Online Slope Count Restatement

Status: ROUTE_CUT / EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-18T00-35-33-327Z-run-8179c962`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T00-35-33-327Z-run-8179c962`
- Lane: artifact-stream / bare Claude CLI run using the Cycle 10 context zip.
- Harness result: `ok=true`, `runMode=artifact_stream`, no terminal transcript.
- Prompt copied to `../prompts/20260618_cycle10_manual_residue_count_packet.md`.
- Clean response copied to
  `../raw/20260618_CYCLE10_MANUAL_W_F1_AA_RES_RESIDUE_COUNT_RESPONSE.md`.

## Verdict

Cycle 10 independently reinforces the Cycle 9 correction:

- `W-F1-AA-RES-RESIDUE-COUNT`, read as a raw cardinality bound for all
  extension residues, is the wrong object.
- The source object is the online slope count: slopes `z in F` for which a
  noncontained support lands on the bad line `F[Bnum]_E`, after aperiodic
  separation.

This is source-valid and bankable as a route cut / wall restatement. It is not
a proof of the positive bound.

Cycle 10's proposed name

```text
W-F1-AA-RES-ONLINE-SLOPE-COUNT
```

is the same mathematical target as Cycle 9's

```text
W-F1-AA-RES-LINE-INCIDENCE
```

with the source qualifiers made explicit: noncontainment and aperiodicity must
remain attached.

## Source-Valid Content

The source normal form counts slopes, not raw residues:

- `slackMCA_v3.tex:1189`, `def:residue`: a slope `z` is active only when
  `Q_z equiv zB mod E` and the witness is noncontained.
- `slackMCA_v3.tex:1197`, `thm:normalform`: MCA is controlled by
  `Lambda^{NC}_{t,delta}`, a noncontained slope packing number.
- `slackMCA_v3.tex:1255`, `rem:aper`: quotient-periodic denominator families
  must be separated for the conjectural positive statement.
- `slackMCA_v3.tex:1231`, `conj:B`: the conjectural `n^{1+o(1)}` target is a
  packing/slope bound for `Lambda^{aper}`, not a raw residue-image bound.

Cycle 10's corrected object can be written:

```text
#{ z in F : exists noncontained a-subset S with
   [interp_S(w0)+alpha interp_S(w1)]_E = z[Bnum]_E }
```

with quotient-periodic cases removed as in `rem:aper`.

Using Cycle 9's locator-quotient form, this is equivalently the incidence
problem:

```text
[L_S Q_S]_E in [W]_E - F[Bnum]_E,
W=interp_D(w),  W=L_S Q_S+interp_S(w),  deg Q_S<=n-a-1.
```

## What To Bank

Bank:

- the raw residue count is an over-strong proxy and not the source MCA object;
- `ONLINE-SLOPE-COUNT` and `LINE-INCIDENCE` should be identified as the same
  live wall, with noncontainment and aperiodicity attached;
- future prompts should target bad-line landings/slopes, not all residues.

## What Not To Bank

Do not bank Cycle 10's heuristic/generic assertion that the raw residue map is
near-injective or `Theta(binomial(n,a))` for arbitrary anchors as a theorem.
The response gives a proposed finite certificate, not an executed proof.

Do not bank:

- any `n^{1+o(1)}` bound;
- any refutation of the corrected online-slope / line-incidence wall;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK ledger claim.

## Field Ledger

- `q_gen=p`, `B=F_p`: generated/base field for `D`, `w0`, `w1`, and locators.
- `q_line=p^2`, `F=F_{p^2}`: extension field for `E`, `Bnum`, residues, and
  slopes `z`.
- `q_chal`: unused.

## Parameter Ledger

- `n=|D|`.
- `k=rho n`.
- `a=ceil((1-delta)n)=s_delta`.
- `sigma=a-k`.
- Balanced ledger: `t=sigma`, so `a=k+t`.
- `deg E=t`.
- `deg Bnum<t`.
- Co-support size in the Cycle 9 decomposition: `j=n-a=r-t`.
- Bad line codimension: `t-1` in `F[X]/E`.

## Next Target

Attack the source-corrected wall:

```text
W-F1-AA-RES-LINE-INCIDENCE / ONLINE-SLOPE-COUNT
```

First concrete subtask: extend the Cycle 9 checker to perform a reproducible
finite scan for `t=2`, `j=2`, separating raw residue count `C1` from bad-line
slope count `C2`, and search for an excess-slope counterpacket to the corrected
incidence wall.
