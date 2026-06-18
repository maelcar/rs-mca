# Cycle 6 Prompt: W-F1-AA-RES Rigidity / Value-Count Law

No internet. You are Claude Opus 4.8 running as a high-effort theorem worker for
the RS-MCA / Proximity Prize project.

This run is intended for the VS Code credited terminal ads lane. Ads and terminal
transcripts are revenue/debug evidence only. Mathematical evaluation uses only a
clean `response.md`.

Read these files first:

1. `input_project/ACTIVE_WALLS.md`
2. `input_project/BANKED_LEMMAS.md`
3. `input_project/CUTS_AND_FALSE_ROUTES.md`
4. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE5_W_F1_AA_RES_EXACT_WALL_AUDIT.md`
5. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_AUDIT.md`
6. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CODEX_LOCAL_NONCONTAINMENT_SUBSET_LEMMA.md`
7. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`, `prob:perfiber`, `conj:B`, `thm:rigidcyclo`, `thm:exactcount`, `rem:aper`
8. `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`, only as needed for `prob:F1` and notation

Current banked facts:

- Balanced means `t=sigma`, `a=k+t=s_delta`.
- Nonzero numerator gives automatic noncontainment on supports of size at least `a=k+t`.
- Quadratic arbitrary anchors reduce to the paired base readout

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
Ehat=lcm(E,E^tau) in B[X].
```

- Restored `W-F1-AA` is a faithful arbitrary-anchor extension-denominator
  instance of `Lambda^{NC}_{t,delta}` / `prob:perfiber`.
- The tangent/zero-numerator and quotient-periodic separations are necessary but
  non-binding: the banked `sigma=1` fixed-rate counterpacket survives both and
  has `Theta(q_line)` slopes.
- The missing axis is reserve `eta=sigma/n`; the new live wall is `W-F1-AA-RES`.

Target:

Attack `W-F1-AA-RES`, not generic F1.

For quadratic `B=F_p`, `F=F_{p^2}`, `D subset B`, `E in F[X]\B[X]` of degree
`t=sigma`, nonzero numerator `Bnum`, and arbitrary `w=w0+alpha*w1`, analyze the
paired readout on `a=k+t=s_delta` subsets:

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
```

restricted to the bad line `F*[Bnum]_E`.

Pick exactly one classification:

1. `BANKABLE_LEMMA`: prove a source-valid rigidity/value-count lemma for
   `rho`, even in a restricted but meaningful regime.
2. `COUNTERPACKET`: produce explicit finite or symbolic data showing that the
   reserve-indexed wall is false even above corrected reserve, with
   q_gen/q_line/q_chal separated.
3. `ROUTE_CUT`: show `W-F1-AA-RES` is not source-valid and identify the false
   reduction.
4. `EXACT_NEW_WALL`: isolate a strictly sharper missing invariant than
   "rigidity/value-count law for rho".

Mandatory constraints:

- Keep `q_gen`, `q_line`, `q_chal`, `B`, and `F` separate.
- Do not use the sub-reserve `sigma=1` counterpacket as a corrected-reserve
  refutation.
- Do not claim `ass:extension-mca-lift`, protocol denominator saving, list
  decoding, or line decoding.
- Do not spend the answer re-proving noncontainment unless you find an actual
  flaw.
- If you give finite evidence, label it EXPERIMENTAL unless it is a symbolic
  source-valid counterpacket.

Output format:

```text
Final classification: <BANKABLE_LEMMA / COUNTERPACKET / ROUTE_CUT / EXACT_NEW_WALL>

Object:
<exact theorem/counterpacket/wall name>

Short verdict:
<one paragraph>

Proof / counterpacket / wall:
<source-valid argument with parameters>

Field and status audit:
<q_gen/q_line/q_chal/B/F and what is or is not proved>

What to bank:
<one short paragraph>
```

Hard limit: 6000 words. Do not survey the repo.
