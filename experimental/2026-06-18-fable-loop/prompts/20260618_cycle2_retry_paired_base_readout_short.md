# Cycle 2 Retry Prompt: Paired Base Readout Audit, Short Form

No internet. Work only from the mounted RS-MCA project files.

This is a retry after the previous Cycle 2 artifact-stream run exceeded the normal answer window and ended with no final result event. Do not write a survey. Do not spend the answer recapitulating source files.

Read only what is needed:

1. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_AUDIT.md`
2. `input_project/current_loop_20260618/2026-06-18-fable-loop/raw/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_RAW.md`
3. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`.
4. `input_project/upstream_main_20260618/tex/snarks_v4.tex`, only for ledger discipline around `ass:extension-mca-lift`, `op:extension-mca`, and `op:line-decoding`.
5. `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`, only `prob:F1`.

Target:

Audit this Cycle 1 bank candidate:

```text
B=F_p, F=F_{p^2}, D subset B, balanced t=sigma, arbitrary w:D->F.
Choose w=w0+alpha*w1 with w0,w1:D->B.
For E in F[X], Ehat=lcm(E,E^tau) in B[X].
Then the def:residue slope condition for an a-subset S factors through
S -> (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat).
```

Pick one classification only:

- `ROUTE_CUT`: the factor-through-readout reduction is false. Give the false step and counterexample.
- `BANKABLE_LEMMA`: the reduction is true under exact hypotheses. State the lemma, prove it, and state exactly what it does not imply.
- `COUNTERPACKET`: the paired base readout creates too many slopes after tangent/contained cases are separated. Give finite data or a symbolic construction.
- `EXACT_NEW_WALL`: the reduction is true but the correct next target is a sharper slope-image/bad-locus packing problem. State it precisely and explain why raw uniform fiber bounds are false.

Mandatory checks, in no more than one paragraph each:

1. Does `Ehat=lcm(E,E^tau)` suffice for arbitrary denominators, including mixed `G*E1` style denominators?
2. Is the slope `z` unique when `[Bnum]_E` is a nonzero zero-divisor in `F[X]/(E)`?
3. Does replacing a support `S_z` of size `>a` by an `a`-subset preserve slope counting, or only overcounting?
4. What is the correct dimension ledger: `deg(Ehat)`, `2 deg(Ehat)`, `e deg(Ehat)`, or another value?
5. Why is the raw uniform fiber endpoint false or repairable?

Field ledgers:

- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not cite protocol denominator savings unless you prove a protocol statement.
- Keep list decoding, CA, MCA, support-wise line-MCA, line-decoding, curve-MCA, and protocol ledger statements separate.

Output format:

```text
Final classification: <one label>

Statement:
<theorem/counterexample/wall>

Proof or disproof:
<tight source-valid argument>

Mandatory checks:
<five short answers>

What to bank:
<one short paragraph>
```

Hard limit: keep the final answer under 5000 words. If you need more than that, choose `EXACT_NEW_WALL` and state the precise obstruction instead of expanding a survey.
