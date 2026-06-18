# Cycle 4 Balance Notation Route-Cut Audit

Status: `ROUTE_CUT` for Cycle 3's `W-F1-AA-AGR` balanced-case wall; `BANKABLE_LEMMA` retained for the noncontainment lemma.

Raw input:

- `raw/20260618_CYCLE4_BALANCE_NOTATION_AUDIT_RAW.md`

Prompt:

- `prompts/20260618_cycle4_audit_cycle3_balance_notation.md`

Run receipt:

- Packy run id: `2026-06-17T21-41-18-487Z-cycle4-audit-cycle3-balance-notation-20260618-a49d7974`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T21-41-18-487Z-cycle4-audit-cycle3-balance-notation-20260618-a49d7974`
- Model: `claude-opus-4-8`
- Mode: `artifact_stream`
- Status: `OK`
- Elapsed: `278437 ms`
- Cost: `$1.10761475`
- Output tokens: `9920`
- Capture warning: none

## Codex Verdict

Cycle 4 is a useful correction. Bank the route cut.

Cycle 3's high-agreement wall `W-F1-AA-AGR` is not source-valid for the balanced wall. The source defines

```text
a = ceil((1-delta)n),   sigma = a-k.
```

See `tex/proximity_blueprint_v3.tex:240` and `tex/snarks_v4.tex:159-163`.

In the balanced residue-line case `t=sigma`, the forced-interpolant subset size is

```text
k+t = k+sigma = a = s_delta.
```

Thus the Cycle 3 premise `s_delta >> a` is false in the balanced regime. It describes an unbalanced regime `t<sigma`, which was already routed to the residual-slack/list object.

## What Survives

The balanced nonzero-numerator noncontainment lemma remains bankable:

For a degree-`t` residue-line datum with `Bnum != 0`, any support of size at least `k+t` is automatically noncontained. In the balanced case `t=sigma`, every genuine support has size at least `a=k+t=s_delta`, so shrinking to an `a`-subset does not lose noncontainment.

## What Is Cut

Cut `W-F1-AA-AGR` as a balanced-case wall. The condition

```text
nu(S) = |{x in D : interp_S(w)(x)=w(x)}| >= s_delta
```

adds no condition when `|S|=a=s_delta`, because `interp_S(w)` agrees with `w` on all of `S` by construction.

High-agreement is real only when `t<sigma`, i.e. `k+t<s_delta`; this is exactly the unbalanced residual-slack regime already routed away from the balanced paired-readout wall.

## Restored Live Wall

`W-F1-AA`:

For the balanced case `t=sigma`, bound the number of distinct scalar slopes `z in F` such that some `a=s_delta` subset `S` satisfies

```text
[interp_S(w)]_E = z [Bnum]_E,
```

equivalently such that the paired base readout

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
```

lands on the bad line `F * [Bnum]_E`, after tangent/zero-numerator and quotient-periodic contributions are separated.

This is the arbitrary-base-anchor paired analogue of `tex/slackMCA_v3.tex:prob:perfiber`, with no separate high-agreement layer in the balanced regime.

## Rejected Upgrades

- Not a proof of the restored slope-image packing wall.
- Not a protocol denominator claim.
- Not an extension-line MCA lift.
- Not a list-decoding or line-decoding theorem.

## What To Bank

Bank the notation correction and route cut: in the source ledger, balanced means `t=sigma=a-k`, hence `k+t=s_delta`. Keep the noncontainment lemma. Restore the live target to pure balanced slope-image / bad-locus packing for the paired base readout.
