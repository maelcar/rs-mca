# Cycle 8 Prompt: W-F1-AA-RES-TWISTED-READOUT

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
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE7_W_F1_AA_RES_VALUECOUNT_TWISTED_READOUT_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle7_theta_multiplier_check.py`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE6B_W_F1_AA_RES_RIGIDITY_RECOVERED_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE5_W_F1_AA_RES_EXACT_WALL_AUDIT.md`
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

## Current Wall

The live target is:

```text
W-F1-AA-RES-TWISTED-READOUT
```

Setup:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `D subset B`.
- `q_chal` is not used.
- Balanced residue-line ledger:
  `a=ceil((1-delta)n)`, `sigma=a-k`, `t=sigma`, hence `a=k+t=s_delta`.
- Arbitrary anchors split as `w=w0+alpha*w1`, `w_i:D->B`.
- `Ehat=lcm(E,E^tau) in B[X]`.
- In the separated case, CRT gives a generally nonconstant
  `theta in B[X]/Ehat` with `theta == alpha mod E` and
  `theta == alpha^tau mod E^tau`.

The object is the twisted quotient readout:

```text
T_theta(S) = [interp_S(w0)]_Ehat + theta [interp_S(w1)]_Ehat
             in B[X]/Ehat.
```

The previous Cycle 7 route cut is crucial:

```text
T_theta(S) is not generally [interp_S(w0+theta*w1)]_Ehat.
```

The local check over `F_5` with `Ehat=X^2+1` shows that
`theta*interp_S(w1)` need not equal `interp_S(theta*w1)` modulo `Ehat`.

## Forbidden Repeats

Do not:

- absorb nonconstant `theta` into the pointwise word `w0+theta*w1`;
- import `thm:exactcount` / `thm:rigidcyclo` verbatim through that false base
  datum;
- re-prove only the same-slope kernel
  `interp_S(w)-interp_S'(w) in E*F_{<k}[X]`;
- use unrestricted `ass:extension-mca-lift`;
- use raw arbitrary locator fibers;
- use `W-F1-AA-AGR` as a balanced high-agreement wall;
- use the `sigma=1` sub-reserve counterpacket as an above-reserve refutation;
- claim protocol denominator savings, list decoding, line decoding, CA, or MCA
  from this local readout analysis.

## Your Exact Task

Attack the twisted-readout value-count/collision problem.

Produce exactly one of:

1. `BANKABLE_LEMMA`: a source-valid value-count/collision lemma for
   `T_theta(S)` on balanced `a=k+t=s_delta` supports, even in a restricted but
   meaningful regime. It must actually bound or structure distinct values and
   must handle nonconstant `theta` honestly.

2. `COUNTERPACKET`: a finite or symbolic balanced counterpacket after reserve,
   tangent/zero-numerator, quotient-periodic, and field-ledger assumptions are
   stated correctly. Give enough data for Codex to implement/verify locally.

3. `ROUTE_CUT`: show that `W-F1-AA-RES-TWISTED-READOUT` is not source-valid,
   identifying the exact false reduction or missing hypothesis.

4. `EXACT_NEW_WALL`: identify a strictly sharper missing invariant than the
   current twisted-readout value-count problem. It must be theorem-sized,
   source-grounded, and actionable.

## Useful Angles

Try at least one hard angle:

- Treat `S -> interp_S(w1)` as a linear support-interpolation operator and
  study multiplication by `theta` modulo `Ehat` as a fixed endomorphism on the
  quotient. Is there a commutator/error term that can be isolated?
- In the smallest nontrivial balanced case `t=sigma=2`, express the failure of
  commutation as a locator-divisible correction and ask whether that correction
  is low-dimensional enough to count.
- Seek an exact formula:

```text
theta*interp_S(w1) - interp_S(theta*w1) = L_S * R_S mod Ehat
```

where `L_S` is the support locator and `R_S` has controlled degree. If true,
determine whether it helps or creates a counterpacket.
- If a counterpacket seems likely, specify minimal finite data:
  `p`, `D`, `k`, `t=sigma`, `a`, `E`, `Bnum`, `theta`, `w0`, `w1`, and the
  statistic showing too many distinct twisted values/slopes.

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
