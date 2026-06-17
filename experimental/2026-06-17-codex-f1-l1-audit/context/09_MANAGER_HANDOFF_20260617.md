# Manager Handoff: Pro Audit Findings, 2026-06-17

Repo checked against GitHub `main` at commit `73b70f73a60dbd0a145a2cc25f8e31009154c220`.

No main `.tex` papers were edited. All additions are companion audit/context files under `agent_context/`.

## Executive Summary

Three batches of 5.5 Pro answers were audited against the current repository.

1. **F1 extension-line MCA lift: significant counterexample.**
   - Status: `COUNTEREXAMPLE`
   - The unrestricted same-numerator extension-line MCA lift in `tex/snarks_v4.tex` `ass:extension-mca-lift` is false.
   - Verified finite witnesses:
     - `B=F_7`, `F=F_49`, `n=6`, `k=3`, `delta=1/3`: extension bad-slope density `15/49`, while base numerator is `7`.
     - `B=F_17`, `F=F_17^2`, `n=16`, `k=8`, `delta=7/16`: extension bad-slope density `288/289`, while base numerator is `17`.
   - Mechanism: genuinely extension-valued residue denominator `E(X)=X-alpha` with `alpha notin B`; this is not the known base-rational subfield confinement phenomenon.
   - Consequence: Paper C cannot safely divide a base-field MCA numerator by `q_chal=|F|` for arbitrary extension-valued lines. The protocol ledger needs a repaired extension theorem, an extension-valued residue-line numerator term, or an affine-subspace/interleaved-base reformulation.

2. **L1 arbitrary locator-fiber local limit: raw formulation is false.**
   - Status: `COUNTEREXAMPLE`
   - The literal arbitrary feasible-fiber statement in `tex/slackMCA_v3.tex` `conj:arbitrary-local` / `conj:final-locator` and `tex/snarks_v4.tex` `ass:locator` overcounts supports.
   - If `U` is already a codeword, every `s`-subset is feasible, so raw `|Fib_U(s)|` can be exponential while the actual list size is `1`.
   - Verified finite packet:
     - `B=F=F_97`, `n=16`, `k=7`, `sigma=4`, `s=11`, `U=0`;
     - `|Fib_0(11)|=binom(16,11)=4368 > 16^2`;
     - entropy inequality clears and `gcd(n,k)=1`, so this is not an active quotient-core issue.
   - Consequence: the L1 target must be repaired before it can support a list theorem. Plausible repairs include maximal-support fibers, exact-agreement supports, or codeword-indexed canonical supports. Monomial-prefix L1 remains open and is not refuted.

3. **A0 Crites-Stewart import audit: no upgrade to proved.**
   - Status: `AUDIT_ONLY` / `CONDITIONAL`
   - Pro found no internal arithmetic failure in Paper D's universal cap calculation, but did not verify the primary Crites-Stewart / ABF theorem source.
   - Consequence: Paper D's universal field-size cap remains `CONDITIONAL`, not `PROVED`. The highest-value audit remains fetching the exact imported theorem and checking field scope, radius/off-by-one conventions, and normalization.

## Files To Review

Primary audit summaries:

- `agent_context/pro_answer_bank/20260617_F1_EXTENSION_MCA_COUNTEREXAMPLE_AUDIT.md`
- `agent_context/pro_answer_bank/20260617_L1_LOCATOR_FIBER_COUNTEREXAMPLE_AUDIT.md`
- `agent_context/pro_answer_bank/20260617_A0_CRITES_STEWART_AUDIT.md`

Reproducibility verifiers:

- `agent_context/verify_f1_extension_counterexample.py`
- `agent_context/verify_l1_arbitrary_fiber_overcount.py`

Updated ledgers:

- `agent_context/02_STATUS_LEDGER.md`
- `agent_context/03_OPEN_PROBLEMS_AND_BACKLOG.md`

Raw Pro outputs and hashes:

- `agent_context/pro_answer_bank/raw/`
- `agent_context/pro_answer_bank/raw/SHA256SUMS.txt`

Existing source files these findings touch:

- `tex/snarks_v4.tex`:
  - `ass:extension-mca-lift`
  - `op:extension-mca`
  - `def:cert`
  - `rule:no-double-credit`
- `tex/proximity_blueprint_v3.tex`:
  - `prob:F1`
- `tex/slackMCA_v3.tex`:
  - `def:locator-fiber`
  - `conj:arbitrary-local`
  - `conj:final-locator`
- `tex/cs25_cap_v4.tex`:
  - `thm:A`
  - `thm:main`
  - `cor:grand`

## Suggested Project Actions

1. **Do not cite `ass:extension-mca-lift` as a valid assumption in its current unrestricted form.**
   - Replace it with a repaired formulation or explicitly charge an extension-valued MCA numerator.

2. **Repair the arbitrary L1 locator-fiber object before further proof work.**
   - The raw support fiber `Fib_U(s)` is too coarse.
   - Preserve the monomial-prefix target as a live narrow proof problem.

3. **Keep Paper D universal cap conditional until the imported Crites-Stewart / ABF theorem is verified from primary source.**
   - No internal algebraic counterexample was found.
   - The import audit is still the top bounded audit target.

## Verification Commands

Run from repo root:

```bash
python3 agent_context/verify_f1_extension_counterexample.py
python3 agent_context/verify_l1_arbitrary_fiber_overcount.py
python3 -m py_compile agent_context/verify_f1_extension_counterexample.py agent_context/verify_l1_arbitrary_fiber_overcount.py
```

Expected output includes:

```text
F1 verifier passed
p=7: extension bad slopes = 15/49; base numerator = 7
p=17: extension bad slopes = 288/289; base numerator = 17

L1 arbitrary-fiber overcount verifier passed
|Fib_0(11)| = binom(16,11) = 4368
actual list size for U=0 is 1, but raw feasible supports are all s-subsets
```
