# Cycle 7 Prompt: W-F1-AA-RES-VALUECOUNT

You are working on the RS-MCA / Proximity Prize repository as a skeptical
mathematical co-director. Your task is not to summarize the project. Attack the
current exact wall.

Use only the provided repository/project source. Do not browse. Do not edit
main papers. If you need to cite source, cite filenames and labels/sections.

## Required Context Files

Read these first:

- `input_project/ACTIVE_WALLS.md`
- `input_project/BANKED_LEMMAS.md`
- `input_project/CUTS_AND_FALSE_ROUTES.md`
- `input_project/NEXT_PROMPT_QUEUE.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RECOVERED_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE5_W_F1_AA_RES_EXACT_WALL_AUDIT.md`
- `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`
- `input_project/upstream_main_20260618/tex/snarks_v4.tex`
- `input_project/upstream_main_20260618/tex/proximity_blueprint_v3.tex`

In `slackMCA_v3.tex`, pay special attention to the labels and nearby text for
the residue-line object, per-fiber/local-limit problem, quotient/cyclotomic
rigidity, and exact-count theorem, including labels such as:

- `def:residue`
- `prob:perfiber`
- `conj:B`
- `rem:aper`
- `thm:rigidcyclo`
- `thm:exactcount`

## Current Wall

The live target is:

```text
W-F1-AA-RES-VALUECOUNT
```

After Cycles 1-6B, the balanced arbitrary-anchor extension-denominator route has
been reduced to a paired base interpolation-residue readout.

Setup to keep in mind:

- `B=F_p`.
- `F=F_{p^2}`.
- `D subset B`.
- `q_gen=p` is the base/generated field size.
- `q_line=p^2` is the extension/line field size.
- `q_chal` is a verifier challenge field only in a later protocol statement;
  do not use it here.
- Balanced residue-line ledger:
  `a=ceil((1-delta)n)`, `sigma=a-k`, `t=sigma`, hence `a=k+t=s_delta`.
- In the first meaningful finite test, take `sigma=t=2`; do not confuse this
  with the already-cut sub-reserve `sigma=1` counterpacket.
- Arbitrary anchors split as `w=w0+alpha*w1` over the base field.
- Interpolation over `D subset B` has base-field Lagrange coefficients.
- The paired readout is

```text
rho(S) = (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat),
Ehat = lcm(E,E^tau) in B[X].
```

The slope condition is that `[interp_S(w)]_E` lies on the bad line
`F * [Bnum]_E`.

## Forbidden Repeats

Do not spend the answer proving only the same-slope kernel:

```text
interp_S(w)-interp_S'(w) in E*F_{<k}[X].
```

Cycle 6B already audited this as source-valid but tautological. It describes
the kernel/descent of the slope map. It does not count distinct slope values.

Do not use these false routes:

- unrestricted `ass:extension-mca-lift`;
- raw arbitrary locator fibers;
- `W-F1-AA-AGR` as a balanced high-agreement wall;
- the `sigma=1` sub-reserve counterpacket as an above-reserve refutation;
- protocol denominator savings;
- list decoding, CA, MCA, line-decoding, and protocol-ledger claims as if they
  were interchangeable.

## Your Exact Task

Attack the value-count/collision problem for the paired readout on the bad line.

Produce exactly one of the following:

1. `BANKABLE_LEMMA`: A source-valid value-count or collision lemma for the image
   of `rho` on `F * [Bnum]_E`, even in a restricted but meaningful regime. State
   all hypotheses. The lemma must actually bound or structure the number of
   distinct slope values, not just characterize equal slopes.

2. `COUNTERPACKET`: A finite or symbolic balanced counterpacket to
   `W-F1-AA-RES` after reserve, tangent/zero-numerator, quotient-periodic, and
   field-ledger assumptions are stated correctly. Give enough data that Codex can
   implement or verify it locally.

3. `ROUTE_CUT`: Show that `W-F1-AA-RES-VALUECOUNT` is not a source-valid target.
   Identify the exact false reduction or hidden hypothesis and point to the
   source dependency that fails.

4. `EXACT_NEW_WALL`: Identify a strictly sharper missing invariant than the
   current value-count/collision law. It must be theorem-sized, source-grounded,
   and not merely a rephrasing of the same-slope kernel.

## Useful Angles

Try at least one hard angle before giving up:

- Work in the smallest nontrivial balanced case `t=sigma=2`, with
  `a=k+2`, `D subset F_p`, `F=F_{p^2}`, and denominator `E` genuinely
  extension-valued.
- Separate the tangent/zero-numerator and quotient-periodic cases first, then
  ask whether the remaining aperiodic nonzero-numerator case forces the slope
  values to be governed by `q_gen` rather than `q_line`.
- Express the slope value as a base-linear functional of the pair
  `(interp_S(w0), interp_S(w1))` modulo `Ehat`, and look for the exact place
  where a base-field cyclotomic count like `thm:rigidcyclo` or `thm:exactcount`
  does or does not transfer.
- If you think a counterpacket exists, specify a minimal search:
  field, domain, `k`, `t`, `a`, `E`, `Bnum`, anchors `w0,w1`, and the statistic
  that certifies too many distinct slopes.

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
