# Cycle 7 Audit: Twisted Readout Boundary

Status: ROUTE_CUT / EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-17T23-48-15-533Z-cycle7-w-f1-aa-res-valuecount-20260618-1b3d071b`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T23-48-15-533Z-cycle7-w-f1-aa-res-valuecount-20260618-1b3d071b`
- Lane: VS Code credited terminal ads lane.
- Harness result: `run_result.json` reported `BANKABLE_LEMMA`, `answerSource=terminal_tui`, and `terminalMalformedVisible=false`.
- Receipt correction: the written `response.md` has missing spaces and duplicated repaint fragments. It was copied to
  `response_malformed_visible_terminal_manual.md`. The clean assistant message
  was recovered from the Claude structured session log and copied to
  `../raw/20260618_CYCLE7_W_F1_AA_RES_VALUECOUNT_RECOVERED_CLAUDE_JSONL.md`.

## Verdict

Do not bank Cycle 7 as the claimed `BANKABLE_LEMMA`.

The safe content is a route cut plus a sharper wall:

```text
W-F1-AA-RES-TWISTED-READOUT:
The quotient equation
  [P0]_Ehat + theta [P1]_Ehat = z b_hat
with nonconstant theta in B[X]/Ehat is a twisted readout. It is not, in
general, the ordinary residue-line readout of a base word w0+theta*w1.
Therefore thm:exactcount/thm:rigidcyclo cannot be imported verbatim to the
z in B stratum through this identification.
```

Cycle 7 Part A is source-valid but mostly already banked: the slope is a
function of the paired base readout, so the number of slopes is bounded by the
number of paired readout values. This does not prove the required value-count
bound.

Cycle 7 Part B is the false step. It correctly constructs a base quotient
class `theta in B[X]/Ehat` by CRT, but then treats

```text
[interp_S(w0)]_Ehat + theta [interp_S(w1)]_Ehat
```

as if it were the residue of the interpolant of the pointwise base word
`w0 + theta*w1`. That commutation fails for nonconstant `theta`.

## Local Algebra Check

The minimal check is in:

- `../local_checks/20260618_cycle7_theta_multiplier_check.py`

It uses `B=F_5`, `Ehat=X^2+1`, and `theta=X`. On `S={0,1}`, take `w0=0` and
`w1(0)=0`, `w1(1)=1`. Then `interp_S(w1)=X`, so

```text
theta * interp_S(w1) = X^2 = -1 mod (X^2+1),
```

whereas the pointwise word `theta*w1` has values `0,1` on `S`, so

```text
interp_S(theta*w1) = X mod (X^2+1).
```

These residues are not equal. Thus the nonconstant multiplier cannot be
absorbed into an ordinary base word without an additional theorem.

## Source Dependencies

- `tex/slackMCA_v3.tex:def:residue` and `thm:normalform`: ordinary residue-line
  data are about interpolants of pointwise words on supports.
- `tex/slackMCA_v3.tex:thm:rigidcyclo` and `thm:exactcount`: exact counts are
  proved for the canonical/cyclotomic strata, not arbitrary twisted paired
  readouts.
- Cycle 1/Cycle 2 paired-readout reductions remain valid.
- Cycle 6B remains valid: the same-slope kernel is not the wall.

## Field Ledger

- `B=F_p`, `q_gen=p`: base/generated field for `D`, `w0`, `w1`, `Ehat`, and the
  paired readout.
- `F=F_{p^2}`, `q_line=p^2`: extension field for `E`, `Bnum`, and slopes.
- `q_chal`: unused; no protocol denominator saving is claimed.

## Parameter Ledger

- `n=|D|`.
- `k=rho n`.
- `a=ceil((1-delta)n)`.
- `sigma=a-k`.
- Balanced case: `t=sigma`, hence `a=k+t=s_delta`.
- First meaningful finite test: `t=sigma=2`, `deg(Ehat)=4`.
- Quotient/list/interleaving arities: not used.

## What To Bank

Bank as `ROUTE_CUT / EXACT_NEW_WALL`:

- Do not identify the nonconstant CRT-multiplier equation with an ordinary base
  residue-line datum.
- Do not import `thm:exactcount` or `thm:rigidcyclo` to the `z in B` stratum
  without proving a new twisted-readout theorem.
- The live wall sharpens from generic value-count to a twisted paired-readout
  value-count:

```text
W-F1-AA-RES-TWISTED-READOUT:
bound or refute the value count of
  S -> [interp_S(w0)]_Ehat + theta [interp_S(w1)]_Ehat
for nonconstant theta in B[X]/Ehat, after reserve, tangent, and
quotient-periodic separations.
```

Do not bank:

- the claimed `BANKABLE_LEMMA` classification;
- the claimed exact transfer to the base datum `(Ehat,b_hat,w0+theta*w1)`;
- any proof of `prob:perfiber`, `conj:B`, line decoding, list decoding, MCA, or
  protocol ledger statements.

## Next Prompt

Ask the next worker to attack `W-F1-AA-RES-TWISTED-READOUT` directly. The
worker should either prove a twisted-readout value-count lemma, produce a finite
balanced counterpacket, or identify the next sharper invariant. It must not try
to absorb `theta` into the word without proving the nonconstant-multiplier
commutation theorem, which is false in general.
