# Cycle 2 Prompt: Audit The Paired Base Readout Endpoint

No internet. You are Claude Opus 4.8 running as a high-effort theorem worker for the RS-MCA / Proximity Prize project.

Work only from the mounted project files. Read the file index first, then read:

1. `input_project/DIRECTOR_STATE.md`
2. `input_project/ROUTE_BOARD_CURRENT.md`
3. `input_project/ACTIVE_WALLS.md`
4. `input_project/BANKED_LEMMAS.md`
5. `input_project/CUTS_AND_FALSE_ROUTES.md`
6. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_AUDIT.md`
7. `input_project/current_loop_20260618/2026-06-18-fable-loop/raw/20260618_CYCLE1_F1_ARBITRARY_ANCHOR_RAW.md`
8. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`.
9. `input_project/upstream_main_20260618/tex/snarks_v4.tex`, especially `ass:extension-mca-lift`, `eq:entropy-necessary`, `op:extension-mca`, `op:line-decoding`.
10. `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`, especially `prob:F1`.

Primary target:

Audit Cycle 1 as an adversary. Do not assume it is correct.

Cycle 1 claim to audit:

For quadratic extensions `B=F_p`, `F=F_{p^2}`, `D subset B`, balanced `t=sigma`, arbitrary anchor `w:D->F`, and `E in F[X]`, the slope condition in `def:residue` factors through the paired base readout

```text
S -> (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
w=w0+alpha*w1,  w0,w1:D->B,
Ehat=lcm(E,E^tau) in B[X].
```

Codex audit status:

- Bankable if interpreted only as a factor-through-base-readout reduction.
- Not a full F1 proof.
- Raw generalized "every fiber is small for arbitrary w0,w1" endpoint is unsafe, because low-degree/codeword anchors can create huge raw fibers.

Your task:

Pick exactly one outcome and justify it with source-valid mathematics.

1. `ROUTE_CUT`: find a flaw in the forced-interpolant/base-split/Ehat readout factorization. Give the exact false step and a finite or symbolic counterexample.
2. `BANKABLE_LEMMA`: prove the factorization cleanly with the weakest correct hypotheses, including general extension degree `e` if it is no harder. State exactly what it does and does not imply.
3. `COUNTERPACKET`: produce explicit finite data showing the paired base interpolation-residue object can create too many slopes after contained/tangent cases are separated.
4. `EXACT_NEW_WALL`: formulate the correct slope-image or bad-locus packing problem that replaces the unsafe raw per-fiber endpoint. The statement must avoid the low-degree-anchor huge-fiber falsehood.

Required checks:

- Does `Ehat=lcm(E,E^tau)` suffice for arbitrary `E`, including mixed `G*E1` denominators?
- Is `z` unique when `[Bnum]_E` is a nonzero zero-divisor in `F[X]/(E)`?
- Does passing from a witness support `S_z` of size `>a` to an `a`-subset preserve enough noncontainment for slope counting, or only for overcounting?
- What is the correct dimension ledger for the paired readout: `deg(Ehat)`, `2deg(Ehat)`, `e deg(Ehat)`, or something else?
- Why exactly is the raw uniform fiber endpoint false or repairable?

Field ledgers:

- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not cite a protocol denominator unless you prove a protocol statement.
- Keep list decoding, CA, MCA, support-wise line-MCA, line-decoding, and protocol ledger statements separate.

Output format:

- Start with `Final classification: ...`.
- Then give a theorem/counterexample/wall statement.
- Then proof or disproof.
- Then a concise "what to bank" paragraph.

Do not give a survey. Do not relabel conditional statements as proved. Do not repeat the sigma=1 extension counterexample unless it is used as a comparison.
