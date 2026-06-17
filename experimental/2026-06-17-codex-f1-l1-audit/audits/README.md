# Pro Answer Bank

Use this directory for raw 5.5 Pro outputs and subsequent Codex audits.

## Naming

- Raw answer: `YYYYMMDD_HHMM__TASK__RAW.md`
- Audit: `YYYYMMDD_HHMM__TASK__AUDIT.md`
- Banked lemma/counterexample/cut, if any: `YYYYMMDD_HHMM__TASK__BANKED.md`

Examples:

- `20260617_1540__A0_CRITES_STEWART_RAW.md`
- `20260617_1540__A0_CRITES_STEWART_AUDIT.md`
- `20260617_1540__A0_CRITES_STEWART_BANKED.md`

## Audit Verdicts

Use one of these route verdicts in the audit header:

- `BANKABLE_LEMMA`: a precise proved lemma that advances a target.
- `COUNTEREXAMPLE`: an explicit finite or symbolic witness breaking a claim.
- `ROUTE_CUT`: a route is impossible under exact stated hypotheses.
- `EXACT_NEW_WALL`: a newly isolated missing lemma or hypothesis.
- `AUDIT_ONLY`: useful checking but no mathematical progress.
- `ROUTE_REFRESH_ONLY`: restates known repository content with no new advance.

Every mathematical claim inside the audit must also carry one formal status tag:

- `PROVED`
- `CONDITIONAL`
- `CONJECTURAL`
- `EXPERIMENTAL`
- `AUDIT`
- `COUNTEREXAMPLE`

## Audit Checklist

For each Pro answer:

1. Preserve the raw answer before judging it.
2. Check source references against `.tex` files.
3. Check theorem labels against `agent_context/04_THEOREM_LABEL_MAP.md`.
4. Verify field ledgers remain separated: `q_gen`, `q_line`, `q_chal`, `B`, `F`.
5. Verify object ledgers remain separated: list decoding, CA, MCA, support-wise line-MCA, line-decoding, curve-MCA, protocol ledger.
6. Record parameters: `q`, `q_gen`, `q_line`, `q_chal`, `B`, `F`, field tower, `n`, `k`, `rho`, `delta`, `eta`, slack `t`/`sigma`, quotient order `N`/`M`, arity `mu`/`nu`.
7. Classify dependencies as proved, imported, conditional, conjectural, experimental, or missing.
8. If and only if something is bankable, update the appropriate context ledger after audit.
