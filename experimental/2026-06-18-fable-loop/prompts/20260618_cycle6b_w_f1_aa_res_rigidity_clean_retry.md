# Cycle 6B Prompt: Clean Retry for W-F1-AA-RES Rigidity Half

No internet. You are Claude Opus 4.8 running as a high-effort theorem worker for
the RS-MCA / Proximity Prize project.

This is a retry after a VS Code visible-terminal capture failure. Mathematical
evaluation uses only clean `response.md`. Do not refer to terminal transcripts.

Read these files first:

1. `input_project/ACTIVE_WALLS.md`
2. `input_project/BANKED_LEMMAS.md`
3. `input_project/CUTS_AND_FALSE_ROUTES.md`
4. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE5_W_F1_AA_RES_EXACT_WALL_AUDIT.md`
5. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_HARNESS_MALFORMED.md`
6. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`

Task:

Ignore the corrupted wording of Cycle 6. Re-derive from source whether the
following restricted lemma is correct, false, or too imprecise to bank:

For quadratic `B=F_p`, `F=F_{p^2}`, `D subset B`, balanced `a=k+t=s_delta`,
degree `t=sigma` denominator `E in F[X]` nonzero on `D`, nonzero numerator
`Bnum` with `deg Bnum<t`, and anchor `w:D->F`, each `a`-subset `S` has unique
interpolant `I_S=interp_S(w)` of degree `<a`. A slope `z` on the bad line should
satisfy

```text
[I_S]_E = z [Bnum]_E.
```

Proposed lemma:

```text
For two on-line a-subsets S,S', the same slope condition z(S)=z(S')
is equivalent to I_S - I_S' in E * F_{<k}[X].
Moreover, in the quadratic base-decomposition w=w0+alpha*w1, the residue
[I_S]_E is determined by the paired base readout
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
Ehat=lcm(E,E^tau) in B[X].
```

Pick exactly one classification:

1. `BANKABLE_LEMMA`: the lemma above is source-valid as stated, with precise
   hypotheses.
2. `ROUTE_CUT`: the lemma above is false or not source-valid; identify the false
   step.
3. `EXACT_NEW_WALL`: the lemma is only a tautological restatement and the real
   missing invariant is sharper. Name it exactly.

Mandatory constraints:

- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not claim a value-count bound, `conj:B`, `prob:perfiber`, line decoding,
  list decoding, protocol denominator saving, or `ass:extension-mca-lift`.
- Do not use the `sigma=1` counterpacket.
- Do not rely on the corrupted Cycle 6 output as evidence.
- Use only ASCII characters.
- Keep every line under 90 characters.
- Do not duplicate paragraphs.
- Do not use markdown tables.

Output exactly this shape:

```text
Final classification: <BANKABLE_LEMMA / ROUTE_CUT / EXACT_NEW_WALL>

Object:
<one line>

Verdict:
<at most 5 short lines>

Proof or cut:
<numbered steps, at most 18 short lines>

Field ledger:
<at most 8 short lines>

What to bank:
<at most 6 short lines>
```

Hard limit: 1600 words.
