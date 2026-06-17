# RS-MCA Research Context

Snapshot inspected: git commit `73b70f73a60dbd0a145a2cc25f8e31009154c220` (`2026-06-13 12:04:19 +0200`, "Clarify contribution file policy").

## Project Goal

AUDIT: This repository is a working package for settling the smooth-domain Reed-Solomon MCA and proximity-list questions in the Proximity Prize regime. The corrected research goal is not an unslacked capacity theorem. It is a theorem-backed reserve certificate: for a specified domain, rate, generated field, line/challenge field, interleaving arity, and protocol reduction, certify a radius `delta = 1 - rho - eta` only after the generated-field entropy floor, quotient-core floor, MCA/list lower-bound ladders, interleaved-list-over-field budget, and actual line-field ledger have all been cleared. See `readme.md:3`, `readme.md:149`, and `tex/proximity_blueprint_v3.tex:147`.

## Repo Source Map

| Source | Role | Status | Stable refs |
|---|---|---|---|
| `tex/RS_disproof_v3.tex` / `RS_disproof_v3.pdf` | Paper A: no-slack obstruction and finite counterexample inventory. | PROVED/COUNTEREXAMPLE for its stated no-slack object. | Abstract and main theorem at `tex/RS_disproof_v3.tex:77`, `tex/RS_disproof_v3.tex:121`; scope boundary at `tex/RS_disproof_v3.tex:505`. |
| `tex/slackMCA_v3.tex` / `slackMCA_v3.pdf` | Paper B: slack, entropy, quotient-core, MCA calculus, final local-limit conjectures. | Mixed: PROVED lower bounds and strata; CONDITIONAL imports; CONJECTURAL final local limits. | Integrated package at `tex/slackMCA_v3.tex:140`; final conjectures at `tex/slackMCA_v3.tex:1702`, `tex/slackMCA_v3.tex:1717`. |
| `tex/cs25_cap_v4.tex` / `cs25_cap_v4.pdf` | Paper D: universal field-size cap via locator fibers plus Crites-Stewart import. | CONDITIONAL on imported list-to-agreement conversion. | Imports at `tex/cs25_cap_v4.tex:126`; main cap at `tex/cs25_cap_v4.tex:219`; caveat at `tex/cs25_cap_v4.tex:425`. |
| `tex/snarks_v4.tex` / `snarks_v4.pdf` | Paper C: protocol ledger, field-separated reserve certificate, modes/fallbacks. | CONDITIONAL ledger theorem: valid only when cited theorem/assumption evidence applies. | Six ledgers at `tex/snarks_v4.tex:92`; certificate at `tex/snarks_v4.tex:436`; ledger theorem at `tex/snarks_v4.tex:502`. |
| `tex/proximity_blueprint_v3.tex` / `proximity_blueprint_v3.pdf` | Control/roadmap document and problem matrix. | AUDIT/PLANNING. | Source map at `tex/proximity_blueprint_v3.tex:76`; problem matrix at `tex/proximity_blueprint_v3.tex:288`. |
| `readme.md` | Repo overview and rough status map. | AUDIT. | Status table at `readme.md:149`; script layer at `readme.md:181`. |
| `agents.md` | Agent guide: rules, priority targets, scripts, toy cases, contribution format. | AUDIT/PLANNING. | Status tags at `agents.md:64`; scripts at `agents.md:334`; "what not to do" at `agents.md:440`. |
| `scripts/run_frontier.py` | Existing heuristic frontier script for a `psi_2` restricted-subset scan. | EXPERIMENTAL. | Script body at `scripts/run_frontier.py:1`; repo description at `readme.md:183`. |

## Logical Reading Order

1. Paper A, `tex/RS_disproof_v3.tex`: read the abstract, main theorem, explicit examples, scope, and verification record.
2. Paper B, `tex/slackMCA_v3.tex`: read the integrated theorem package, list-fiber sections, quotient-core sections, exact slack calculus, residue-line normal form, cap/subfield sections, final conjectures.
3. Paper D, `tex/cs25_cap_v4.tex`: read imported theorem statements, locator-fiber lemma, main cap, grand challenge corollaries, subfield confinement, caveat/open problems.
4. Paper C, `tex/snarks_v4.tex`: read the six-ledger abstract, protocol-facing objects, generated-field and quotient ledgers, assumptions, certificate, ledger theorem, field accounting, modes/open problems.
5. `tex/proximity_blueprint_v3.tex`, `readme.md`, and `agents.md`: use as route board, not as theorem source when a TeX paper has the exact label.

## Dependency Graph

```text
Paper A: no-slack obstruction
        |
        v
Paper B: slack / entropy / quotient-core / MCA theory
        |\
        | \__ Paper D: universal cap via imported Crites-Stewart conversion
        |
        v
Paper C: SNARK / protocol reserve ledger
        ^
        |
proximity_blueprint_v3: roadmap and problem matrix
```

## Glossary

| Object | Meaning | Do not merge with |
|---|---|---|
| `q_gen` | Generated field for domain/locator coefficients and entropy pigeonhole. | `q_line`, `q_chal`, ambient extension `F`. |
| `q_line` | Field over which CA/MCA/line-decoding experiment is analyzed and slopes are sampled. | `q_gen` unless a transfer theorem applies. |
| `q_chal` | Verifier challenge field. Often equals `q_line`, but only after protocol proof says so. | `q_line` by notation alone. |
| `B` | Base/generated subfield containing domain and locator coefficients. | Ambient `F`. |
| `F` | Ambient or extension field for code values/challenges. | Base/generated field credit. |
| `n,k,rho` | Domain size, dimension, rate `rho = k/n`. | Dithered `k` must be recorded exactly. |
| `delta, eta, sigma` | Radius, reserve from capacity, agreement slack `sigma = a-k`. | Quotient slack `t/N` unless explicitly identified. |
| `N` or `M` | Quotient order or quotient-fiber scale, depending on paper. | Always record the local definition in the source paper. |
| `mu` | Protocol list arity consumed by the reduction. | Implementation interleaving `nu`. |
| `nu` | Implementation interleaving factor. | Protocol list arity `mu`. |
| List decoding | Nearby-codeword list size. | CA, MCA, line-decoding, curve-MCA. |
| CA | Correlated agreement error in the ABF/Crites-Stewart normalization. | Support-wise MCA; Paper D uses CA-to-MCA chain. |
| MCA | Support-wise same-set line badness. | List decoding or line-decoding without a theorem. |
| Residue-line packing | Paper B normal form for all-line MCA. | Monomial-line or quotient-periodic subfamilies only. |
| Protocol ledger | Certificate accounting for exact reduction terms. | A theorem about one coding object. |

## Do Not Confuse These

- AUDIT: A large extension field cannot pay the `q_gen` entropy bill. Paper B's generated-field pigeonhole is at `tex/slackMCA_v3.tex:238`; Paper C repeats the rule at `tex/snarks_v4.tex:308`.
- AUDIT: Paper D's universal cap is not an unconditional theorem until the imported Crites-Stewart statement is audited. The import caveats are at `tex/cs25_cap_v4.tex:146` and `tex/cs25_cap_v4.tex:425`.
- AUDIT: Paper D caps the `2^-128` threshold with error roughly `1/k`; it is not an error-one result in the whole forbidden band. See `tex/cs25_cap_v4.tex:412` and `readme.md:223`.
- AUDIT: Base-code list bounds do not automatically solve interleaved-list protocol terms. Paper C defines protocol list arity at `tex/snarks_v4.tex:209`.
- AUDIT: Base-field MCA bounds do not automatically lift to extension-line MCA. Paper C isolates this as `ass:extension-mca-lift` at `tex/snarks_v4.tex:242`.
- AUDIT: `k = rho*n - 1` can kill dyadic quotient cores, but it is an arithmetization change, not a free theorem. See `tex/snarks_v4.tex:552` and `tex/snarks_v4.tex:581`.
- AUDIT: Small-case scripts are evidence or counterexample finders unless they emit a proof certificate tied to a finite theorem.

## Current High-Level State

| Topic | Status | Source |
|---|---|---|
| No-slack support-wise line-MCA up-to-capacity statement | COUNTEREXAMPLE / PROVED refutation. | `tex/RS_disproof_v3.tex:121`, `tex/RS_disproof_v3.tex:507`. |
| Deployed-field obstruction floors | PROVED for stated no-slack/support-wise settings. | `tex/RS_disproof_v3.tex:124`, `tex/slackMCA_v3.tex:1390`. |
| Generated-field entropy lower bound | PROVED. | `tex/slackMCA_v3.tex:227`, `tex/slackMCA_v3.tex:238`. |
| Quotient-core list obstruction | PROVED. | `tex/slackMCA_v3.tex:284`. |
| Exact slack calculus / canonical-line MCA strata | PROVED for stated strata. | `tex/slackMCA_v3.tex:692`, `tex/slackMCA_v3.tex:715`. |
| Universal cap below `2^256` | CONDITIONAL on imported conversion; Paper D is canonical. | `tex/cs25_cap_v4.tex:219`, `tex/cs25_cap_v4.tex:259`. |
| Generated-field locator local limit | CONJECTURAL / open. | `tex/slackMCA_v3.tex:1702`, `tex/snarks_v4.tex:760`. |
| Corrected all-line MCA / residue-line local limit | CONJECTURAL / open. | `tex/slackMCA_v3.tex:1717`, `tex/snarks_v4.tex:405`. |
| Extension-line MCA lift | CONJECTURAL / open; likely false below reserve due to Paper D fiber mass, unresolved above reserve. | `tex/snarks_v4.tex:242`, `tex/cs25_cap_v4.tex:395`. |
| Protocol reserve certificate | CONDITIONAL/AUDIT framework, not a universal compiler. | `tex/snarks_v4.tex:502`, `tex/snarks_v4.tex:533`. |
