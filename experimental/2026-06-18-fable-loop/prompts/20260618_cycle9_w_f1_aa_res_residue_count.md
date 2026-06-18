# Cycle 9 Prompt: W-F1-AA-RES-RESIDUE-COUNT

You are working on the RS-MCA / Proximity Prize repository as a skeptical
mathematical co-director. Your task is not to summarize the project. Attack the
current exact wall.

Use only the provided repository/project source. Do not browse. Do not edit main
papers.

## Required Context Files

Read these first:

- `input_project/ACTIVE_WALLS.md`
- `input_project/BANKED_LEMMAS.md`
- `input_project/CUTS_AND_FALSE_ROUTES.md`
- `input_project/NEXT_PROMPT_QUEUE.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE8_W_F1_AA_RES_TWISTED_READOUT_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle8_twisted_readout_verify.py`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE7_W_F1_AA_RES_VALUECOUNT_TWISTED_READOUT_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RECOVERED_AUDIT.md`
- `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`
- `input_project/upstream_main_20260618/tex/snarks_v4.tex`
- `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`

In `slackMCA_v3.tex`, pay attention to:

- `def:residue`
- `thm:normalform`
- `prob:perfiber`
- `conj:B`
- `rem:aper`
- `thm:rigidcyclo`
- `thm:exactcount`
- any statements distinguishing proved canonical/monomial strata from arbitrary
  residue-line data.

## Current Wall

The live target is:

```text
W-F1-AA-RES-RESIDUE-COUNT
```

Cycle 8 proves that the twisted readout is only a Weil-restricted form of the
original extension residue. Do not reopen the twist.

Setup:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `D subset B`.
- `q_chal` is not used.
- Balanced residue-line ledger:
  `a=ceil((1-delta)n)`, `sigma=a-k`, `t=sigma`, hence `a=k+t=s_delta`.
- Arbitrary anchors split as `w=w0+alpha*w1`, `w_i:D->B`.
- Separated denominator: `E in F[X]`, `deg E=t`, `gcd(E,E^tau)=1`, nonzero on
  `D`, and quotient-periodic/tangent/zero-numerator cases separated as in
  `rem:aper` and prior audits.

The honest object is:

```text
R_E(S) = [interp_S(w0)+alpha interp_S(w1)]_E in F[X]/E
```

on balanced `a=k+t=s_delta` supports, with noncontainment handled by the
nonzero-numerator lemma.

## Forbidden Repeats

Do not:

- re-solve the twisted readout; Cycle 8 proves it is isomorphic to `R_E(S)`;
- absorb nonconstant `theta` into the pointwise word `w0+theta*w1`;
- import `thm:exactcount` / `thm:rigidcyclo` beyond their proved
  canonical/monomial strata;
- re-prove only the same-slope kernel
  `interp_S(w)-interp_S'(w) in E*F_{<k}[X]`;
- use unrestricted `ass:extension-mca-lift`;
- use raw arbitrary locator fibers;
- use `W-F1-AA-AGR` as a balanced high-agreement wall;
- use the `sigma=1` sub-reserve counterpacket as an above-reserve refutation;
- claim protocol denominator savings, list decoding, line decoding, CA, or MCA
  from this local residue-count analysis.

## Your Exact Task

Attack the extension-residue value-count/collision problem.

Produce exactly one of:

1. `BANKABLE_LEMMA`: a source-valid value-count/collision lemma for `R_E(S)`
   above corrected reserve, even in a restricted but meaningful regime. It must
   actually bound or structure distinct residue values.

2. `COUNTERPACKET`: a finite or symbolic balanced counterpacket after reserve,
   tangent/zero-numerator, quotient-periodic, and field-ledger assumptions are
   stated correctly. Give enough data for Codex to implement/verify locally.

3. `ROUTE_CUT`: show that `W-F1-AA-RES-RESIDUE-COUNT` is not source-valid,
   identifying the exact false reduction or missing hypothesis.

4. `EXACT_NEW_WALL`: identify a strictly sharper missing invariant than the
   current extension-residue value-count problem. It must be theorem-sized,
   source-grounded, and actionable.

## Useful Angles

Try at least one hard angle:

- Treat `R_E(S)` as a residue of a degree-`<a` interpolant and look for a
  structural decomposition in terms of the support locator `L_S` and low-degree
  quotient `Q_S`.
- In the smallest balanced case `t=sigma=2`, decide whether many distinct
  residues are generic for random base anchors; if so, specify a corrected
  reserve counterpacket search.
- Ask whether any `q_gen`-governed rigidity remains after Cycle 8, or whether
  all honest counting is necessarily a `q_line` per-fiber problem.
- If a counterpacket seems likely, specify minimal finite data:
  `p`, `D`, `k`, `t=sigma`, `a`, `E`, `Bnum`, `w0`, `w1`, and the statistic
  showing too many distinct extension residues/slopes.
- If proving a lemma, state exactly what extra hypotheses replace the missing
  arbitrary-anchor rigidity. Examples: monomial anchors, affine anchors,
  subgroup-symmetric anchors, denominator normal form, or random-anchor
  high-probability bounds.

## Output Format

Start with:

```text
Final classification: <BANKABLE_LEMMA | COUNTERPACKET | ROUTE_CUT | EXACT_NEW_WALL>
```

Then give:

- precise statement or counterpacket;
- source dependencies;
- field ledger (`q_gen`, `q_line`, `q_chal`, `B`, `F`);
- parameter ledger (`n`, `k`, `rho`, `delta`, `eta`, `sigma/t`, quotient order
  if used, interleaving/list arity if used);
- proof/audit notes;
- what Codex should bank or test next.

If you cannot prove or refute the wall, return `EXACT_NEW_WALL` only if the new
wall is genuinely sharper and actionable.

END_OF_FABLE_RESPONSE
