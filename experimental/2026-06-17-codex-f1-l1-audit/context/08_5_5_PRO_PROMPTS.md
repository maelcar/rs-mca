# Three 5.5 Pro Prompts

Purpose: give 5.5 Pro narrow, source-grounded jobs that can either solve a load-bearing target or produce auditable progress. Treat Pro output as a candidate research artifact, not as truth until audited.

Global rules for all three prompts:

- Use the attached repository/context files as source of truth.
- Prefer `.tex` over PDFs for theorem labels, hypotheses, notation, and proof status.
- Do not prove a stronger statement than the files actually support.
- Tag every claim as `PROVED`, `CONDITIONAL`, `CONJECTURAL`, `EXPERIMENTAL`, `AUDIT`, or `COUNTEREXAMPLE`.
- Keep field ledgers separate unless an explicit theorem converts them: `q_gen`, `q_line`, `q_chal`, `B`, `F`.
- Keep list decoding, CA, MCA, support-wise line-MCA, line-decoding, curve-MCA, and protocol ledger claims separate unless an explicit theorem converts them.
- For every mathematical claim, record parameters when available: `q`, `q_gen`, `q_line`, `q_chal`, `B`, `F`, field tower, `n`, `k`, `rho`, `delta`, `eta`, slack `t` or `sigma`, quotient order `N` or `M`, interleaving/list arity `mu` or `nu`, and exact theorem/lemma/problem dependency.
- Output should be directly auditable: exact theorem labels, source file/section references, parameter ledger, dependencies, proof gaps, and final verdict.

## Prompt 1: A0 Crites-Stewart Import Audit

Attach:

- `agent_context/00_RESEARCH_CONTEXT.md`
- `agent_context/02_STATUS_LEDGER.md`
- `agent_context/05_AUDIT_PLAN.md`
- `tex/cs25_cap_v4.tex`
- `tex/slackMCA_v3.tex`
- if available to you: the original Crites-Stewart source and any BCHKS fallback source cited by `tex/cs25_cap_v4.tex`

Copy-ready prompt:

```text
You are auditing the Reed-Solomon MCA / Proximity Prize repository as a skeptical mathematical research director.

Your task is A0: audit the imported Crites-Stewart list-to-agreement conversion used in `tex/cs25_cap_v4.tex`. Do not try to solve the whole prize problem. Decide exactly what the import proves, what hypotheses it requires, and whether the repository’s universal field-size cap statements cite it correctly.

Source priority:
1. repository `.tex` files attached here;
2. original Crites-Stewart / BCHKS sources if available;
3. no tweet/public claim may be used as proof.

Required output:
1. A table with columns:
   - Repository claim
   - Source file and label
   - Imported theorem actually needed
   - Exact imported theorem statement, paraphrased with parameters
   - Hypotheses: field-size, alphabet, rate, list size, radius, agreement, randomness, asymptotic/finite status
   - Does the import match? yes/no/conditional
   - Correction needed, if any
   - Impact on `thm:main`, `cor:grand`, and any protocol-usable cap
2. A parameter ledger separating `q_gen`, `q_line`, `q_chal`, `B`, and `F`.
3. A status verdict for Paper D’s cap:
   - `PROVED` only if all imports and hypotheses match exactly;
   - otherwise `CONDITIONAL` or `AUDIT`;
   - `COUNTEREXAMPLE` only if you exhibit a genuine contradiction or missing hypothesis that breaks a stated theorem.
4. A list of the top five exact follow-up fixes or citations needed.

Be hostile to hidden assumptions. Check finite-vs-asymptotic status, exact error gap, alphabet/field-size constraints, whether `q >= n` or `q >= 2n` is required, whether the list-to-agreement conversion is for list decoding, correlated agreement, MCA, support-wise line-MCA, or a different object, and whether any field ledger is silently merged.

Do not smooth over uncertainty. If a source theorem is unavailable, mark the result `AUDIT` and state exactly what must be fetched.
```

## Prompt 2: F1 Extension-Line MCA Lift or Counterexample

Attach:

- `agent_context/00_RESEARCH_CONTEXT.md`
- `agent_context/01_PAPER_MAP.md`
- `agent_context/02_STATUS_LEDGER.md`
- `agent_context/03_OPEN_PROBLEMS_AND_BACKLOG.md`
- `tex/cs25_cap_v4.tex`
- `tex/slackMCA_v3.tex`
- `tex/snarks_v4.tex`

Copy-ready prompt:

```text
You are attacking target F1 in the Reed-Solomon MCA / Proximity Prize repository: extension-line MCA lift or counterexample.

The question is whether an extension-field line/affine-subspace argument can escape the residue-line/local obstruction while staying compatible with the protocol ledger. Do not conflate the base/generated field with the extension/ambient field.

Goal:
Either prove a precise extension-line MCA transfer theorem, or produce a concrete counterexample/witness packet showing why the transfer fails. A route cut is acceptable if it is exact.

Mandatory field ledger:
- `B`: base or generated subfield;
- `F`: ambient extension field;
- `q_gen`: generated field for entropy/locator fibers;
- `q_line`: field used by line, CA, MCA, or line-decoding experiment;
- `q_chal`: verifier challenge field.
Do not identify any two of these without an explicit theorem.

Required output:
1. State the exact candidate theorem you are proving or refuting, with all parameters:
   `B`, `F`, field tower, `q_gen`, `q_line`, `q_chal`, `n`, `k`, `rho`, `delta`, `eta`, slack `t`/`sigma`, quotient order `N`/`M`, and arity `mu`/`nu`.
2. Separate the objects:
   list decoding, CA, MCA, support-wise line-MCA, line-decoding, curve-MCA, and protocol ledger.
3. If proving: give the proof with source dependencies by theorem/lemma label, and isolate every imported hypothesis.
4. If refuting: give a full witness packet:
   - finite fields and field tower;
   - code/evaluation set;
   - quotient/residue data;
   - bad line or affine subspace;
   - chosen received word(s);
   - list/agreement/MCA failure condition;
   - exact computed inequalities;
   - minimal verification script or pseudocode.
5. Final verdict: `PROVED`, `CONDITIONAL`, `COUNTEREXAMPLE`, or `AUDIT`.

Important: do not merely show that base-rational lines are trapped in a residue coset. That is already known. The useful question is whether extension-valued lines give a valid transfer for the protocol object, or whether they fail for a precise reason.
```

## Prompt 3: L1 Generated-Field Locator Local Limit

Attach:

- `agent_context/00_RESEARCH_CONTEXT.md`
- `agent_context/02_STATUS_LEDGER.md`
- `agent_context/03_OPEN_PROBLEMS_AND_BACKLOG.md`
- `agent_context/04_THEOREM_LABEL_MAP.md`
- `tex/slackMCA_v3.tex`
- `tex/proximity_blueprint_v3.tex`

Copy-ready prompt:

```text
You are attacking target L1 in the Reed-Solomon MCA / Proximity Prize repository: the generated-field locator local limit.

Do not try to solve the whole prize problem. Focus on producing one bankable theorem, one exact route cut, or one counterexample for the L1 local-limit mechanism in `tex/slackMCA_v3.tex`.

Working target:
Analyze the locator-fiber / generated-field obstruction after quotient removal in the monomial-prefix or quotient-separated regime. Determine whether the proposed local limit can be made into a theorem, must be weakened, or is false.

Source priority:
1. `tex/slackMCA_v3.tex`;
2. `tex/proximity_blueprint_v3.tex`;
3. attached context ledgers.

Required output:
1. Identify the exact conjecture/problem/lemma labels in `slackMCA_v3.tex` that L1 depends on.
2. Restate the local-limit target in your own exact notation, including:
   `q_gen`, `B`, `F`, field tower, `n`, `k`, `rho`, `delta`, `eta`, slack `t`/`sigma`, quotient order `N`/`M`, and interleaving/list arity `mu`/`nu`.
3. Try to prove the strongest valid statement in one narrow case first:
   - monomial-prefix messages;
   - quotient-separated evaluation set;
   - explicit generated subfield ledger;
   - no silent conversion to line-MCA or protocol claims.
4. If proof succeeds: state the theorem, proof, dependencies, and exactly where it plugs into Paper B.
5. If proof fails: isolate the first irreducible gap as an `EXACT_NEW_WALL`, not a vague difficulty. Give the minimal missing lemma needed.
6. If false: give a concrete counterexample with finite parameters and verification pseudocode.
7. Final output must include:
   - `BANKABLE_LEMMA`, `ROUTE_CUT`, `EXACT_NEW_WALL`, or `COUNTEREXAMPLE`;
   - formal status tag among `PROVED`, `CONDITIONAL`, `CONJECTURAL`, `EXPERIMENTAL`, `AUDIT`, `COUNTEREXAMPLE`;
   - exact next-step prompt for a follow-up agent.

Be skeptical about entropy heuristics. A dimension count is not a proof unless every fiber bound and exceptional set is controlled at the stated finite parameters.
```
