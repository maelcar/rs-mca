# Cycle 4 Prompt: Audit Cycle 3 Balance/Agreement Notation

No internet. You are Claude Opus 4.8 running as a high-effort theorem auditor for the RS-MCA / Proximity Prize project.

Work only from mounted project files. Read:

1. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE3_W_F1_AA_NONCONTAINMENT_AUDIT.md`
2. `input_project/current_loop_20260618/2026-06-18-fable-loop/raw/20260618_CYCLE3_W_F1_AA_NONCONTAINMENT_RAW.md`
3. `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE2_PAIRED_BASE_READOUT_RETRY_AUDIT.md`
4. `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`, especially `def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`, and any nearby definitions of `s_delta`, slack `sigma`, and balanced `t=sigma`.
5. `input_project/ACTIVE_WALLS.md`
6. `input_project/BANKED_LEMMAS.md`

Primary audit target:

Cycle 3 banked a good-looking noncontainment lemma, but may have introduced a false wall by confusing two regimes.

Potential issue:

In `def:residue`, witnesses have `|S_z| >= s_delta`, and the forced-interpolant subset has size

```text
a = k+t.
```

The balanced case in the previous loop is supposed to be `t=sigma`, where `sigma` is the slack above `k`; if `sigma = s_delta-k`, then

```text
a = k+t = k+sigma = s_delta.
```

In that balanced case, there is no extra high-agreement condition `nu(S)>=s_delta` beyond choosing the `a`-subset itself. Cycle 3 nevertheless stated a new wall `W-F1-AA-AGR` based on `s_delta >> a`, apparently treating `t` as constant while `eta n` is large.

Your task:

Pick exactly one classification:

1. `ROUTE_CUT`: Cycle 3's `W-F1-AA-AGR` wall is not source-valid for the balanced `t=sigma` wall. Identify the exact false step and restore the correct live wall.
2. `BANKABLE_LEMMA`: The noncontainment lemma is correct, and in the balanced nonzero-numerator case it removes noncontainment entirely; the remaining wall is exactly slope-image packing for `a=s_delta` subsets.
3. `EXACT_NEW_WALL`: There are two source-valid regimes: balanced `t=sigma` and unbalanced `t<sigma`; state the correct wall in each and say where high-agreement belongs.
4. `COUNTERPACKET`: Provide finite/symbolic data showing the restored balanced wall is false after all source hypotheses are checked.

Mandatory questions:

- In the source notation, is `sigma` equal to `s_delta-k`, or is it something else in the relevant F1/Cycle 2 target?
- In the balanced case `t=sigma`, is `a=k+t` equal to `s_delta`?
- Does Cycle 3's high-agreement invariant `nu(S)>=s_delta` add any condition in the balanced case?
- Is the balanced nonzero-numerator noncontainment lemma correct? State the strongest correct version.
- What should the next prompt target be after this audit?

Output format:

```text
Final classification: <ROUTE_CUT / BANKABLE_LEMMA / EXACT_NEW_WALL / COUNTERPACKET>

Verdict:
<short answer>

Notation audit:
<source-grounded parameter check>

Corrected bank:
<what survives from Cycle 3>

Corrected live wall:
<exact next target>

What to bank:
<one short paragraph>
```

Do not give a survey. Do not prove the prize problem. This is a source-ledger audit.
