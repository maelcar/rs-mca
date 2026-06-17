# Paper Map

## Paper A: `RS_disproof_v3`

Abstract-level summary: COUNTEREXAMPLE/PROVED. Paper A refutes the no-slack, support-wise line-MCA reading of up-to-capacity smooth-domain RS at prize rates. The mechanism is the quotient locator identity: restricted sums in a smooth quotient subgroup produce many bad slopes for lines of the form `x^(k+a) + z x^k`. Main abstract at `tex/RS_disproof_v3.tex:77`.

Main definitions:
- AUDIT: `def:mca`, support-wise line-MCA error, `tex/RS_disproof_v3.tex:110`.
- AUDIT: `conj:capacity`, the no-slack capacity conjecture being refuted, `tex/RS_disproof_v3.tex:97`.

Main theorems and status:
- COUNTEREXAMPLE/PROVED: `thm:main`, false no-slack conjecture with deployed-field error one, Fermat examples, non-negligible sieve primes, and divisor-level list bound, `tex/RS_disproof_v3.tex:121`.
- PROVED: `lem:locator`, quotient locator, `tex/RS_disproof_v3.tex:156`.
- PROVED: `lem:dsh`, Dias da Silva-Hamidoune coverage import, `tex/RS_disproof_v3.tex:164`.
- PROVED: `thm:sieve`, infinitely many inverse-polylogarithmic bad-slope fields, `tex/RS_disproof_v3.tex:253`.
- PROVED/AUDIT: explicit counterexample table and exact verification record, `tex/RS_disproof_v3.tex:346`, `tex/RS_disproof_v3.tex:517`.

Dependencies:
- PROVED import: Dias da Silva-Hamidoune restricted-sum theorem.
- AUDIT import: standard Siegel-Walfisz and cyclotomic norm arguments in `thm:sieve`.

Open questions created:
- CONJECTURAL: slacked, curve-MCA, exact-threshold, and protocol-specific formulations above the obstruction floors are not refuted by Paper A. See `tex/RS_disproof_v3.tex:509`.
- AUDIT: finite claims should be converted into script certificates beyond the retained verification record.

## Paper B: `slackMCA_v3`

Abstract-level summary: AUDIT. Paper B is a mixed-status source: it contains PROVED lower bounds and strata, CONDITIONAL imports, and CONJECTURAL final local limits. It builds the corrected reserve theory: locator fibers, generated-field entropy, quotient-core list obstructions, characteristic-zero and finite-field collision sieves, exact slack calculus, failure ladders, quotient floors, subfield confinement, and final local-limit conjectures. Integrated status package at `tex/slackMCA_v3.tex:140`.

Main definitions:
- AUDIT: `def:locator-fiber`, locator fibers and monomial prefix map, `tex/slackMCA_v3.tex:166`.
- AUDIT: `def:taustar`, entropy gap, `tex/slackMCA_v3.tex:221`.
- AUDIT: `def:qprofile`, quotient-core profile, `tex/slackMCA_v3.tex:347`.
- AUDIT: `def:mca`, bad parameter and line-MCA error, `tex/slackMCA_v3.tex:643`.
- AUDIT: `def:badset`, multi-symmetric image for exact slack, `tex/slackMCA_v3.tex:684`.
- AUDIT: `def:residue`, residue-line datum and packing number, `tex/slackMCA_v3.tex:1189`.

Main theorems and status:
- PROVED: coefficient and generated-field pigeonhole list lower bounds, `thm:pigeonhole`, `cor:genfield-pigeonhole`, `cor:entropy-lower`, `tex/slackMCA_v3.tex:227`.
- PROVED: quotient-core list obstruction, `thm:qcore`, `tex/slackMCA_v3.tex:284`.
- PROVED: characteristic-zero inverse quotient theorem and polynomial characteristic-zero fibers, `thm:upstairs`, `cor:upstairs-poly`, `tex/slackMCA_v3.tex:390`.
- PROVED: Galois-amplified no-collision lane for split primes in quasi-polynomial range, `thm:no-collision`, `tex/slackMCA_v3.tex:477`.
- CONJECTURAL/CONDITIONAL: positive list theorem depends on `conj:arbitrary-local`, `thm:conditional-list`, `tex/slackMCA_v3.tex:582`.
- PROVED: exact slack characterization and slack-t quotient lower bound, `thm:exactslack`, `thm:slackt`, `tex/slackMCA_v3.tex:692`.
- CONDITIONAL: free-pool ladder depends on exponential-sum input, `thm:ladder`, `tex/slackMCA_v3.tex:869`.
- PROVED: dyadic descent, two-moment fullness, quotient-exact floor, quotient-profile necessity, `thm:descent`, `thm:twomoment`, `prop:qfloor`, `thm:qnecessity`.
- CONDITIONAL: native universal cap through Crites-Stewart, superseded in constants by Paper D, `tex/slackMCA_v3.tex:1464`.
- PROVED: subfield confinement for base-valued lines, `thm:subfield`, `tex/slackMCA_v3.tex:1533`.
- CONJECTURAL: final locator local limit and final floor-/quotient-corrected MCA asymptotic, `conj:final-locator`, `conj:final-mca`, `tex/slackMCA_v3.tex:1702`.

Dependencies:
- Paper A no-slack obstruction floors.
- Imported restricted-sum and exponential-sum estimates, some explicitly conditional.
- Crites-Stewart and ABF restatement for the conditional cap section.

Open questions created:
- L1: generated-field arbitrary-word locator local limit.
- M1: corrected all-line MCA / residue-line packing local limit.
- L3: quotient-profile constants and dimension dithering.
- F1: extension-valued line witnesses and transfer.
- X1: smooth list-CA-MCA equivalence without square-root loss.

## Paper D: `cs25_cap_v4`

Abstract-level summary: CONDITIONAL. Paper D sharpens the universal cap by counting slack-two locator fibers over the field of definition and applying the Crites-Stewart correlated-agreement-to-list conversion as restated by ABF. It gives a field-size-universal cap below `2^256`, including extension fields directly. Summary at `tex/cs25_cap_v4.tex:54`.

Main definitions:
- AUDIT: `def:ca`, correlated agreement error, `tex/cs25_cap_v4.tex:92`.
- AUDIT: `def:mca`, support-wise MCA, `tex/cs25_cap_v4.tex:100`.
- AUDIT: `def:dstar`, challenge threshold, `tex/cs25_cap_v4.tex:113`.

Main theorems and status:
- CONDITIONAL: `thm:A`, imported Crites-Stewart theorem as stated in ABF, `tex/cs25_cap_v4.tex:128`.
- CONDITIONAL: `thm:B`, imported BCHKS slacked fallback, `tex/cs25_cap_v4.tex:137`.
- PROVED relative to algebraic setup: `lem:fiber`, locator fibers are lists, including slack-two and subfield pigeonhole, `tex/cs25_cap_v4.tex:154`.
- CONDITIONAL: `thm:main`, universal cap assuming import, `tex/cs25_cap_v4.tex:219`.
- CONDITIONAL: `cor:grand`, challenge-envelope cap: `2^-9` for rates `1/2,1/4,1/8`; `2^-10` at `1/16`, `tex/cs25_cap_v4.tex:259`.
- CONDITIONAL: `cor:deployed`, KoalaBear sextic failure at gap `2^-7` with error `>2^-22`, `tex/cs25_cap_v4.tex:323`.
- PROVED: `lem:confine`, subfield confinement for CA/MCA bad slopes of base-valued pairs, `tex/cs25_cap_v4.tex:374`.
- CONDITIONAL: `cor:Fvalued`, certifying deployed extension lines must be genuinely `F`-valued because the existence result uses the imported conversion, `tex/cs25_cap_v4.tex:395`.

Dependencies:
- Crites-Stewart `CS25` Theorem 2 as restated in ABF.
- BCHKS slacked theorem as an independent fallback.
- Paper A/B quotient locator and subfield-pigeonhole framework.

Open questions created:
- AUDIT: verify imported Crites-Stewart hypotheses, normalization, constants, and augmented-code monotonicity.
- CONJECTURAL/COUNTEREXAMPLE target: exhibit explicit `F_{p^6}` pairs with CA-bad-slope density `>2^-22`, `prob:explicit`, `tex/cs25_cap_v4.tex:430`.
- CONJECTURAL: error-one in the `2^150` to `2^256` band remains open, `prob:errorone`, `tex/cs25_cap_v4.tex:434`.

## Paper C: `snarks_v4`

Abstract-level summary: CONDITIONAL/AUDIT. Paper C is a protocol-facing ledger. It does not prove the missing local limits. It defines how a protocol must account for generated-field entropy, quotient cores, locator/list bounds, interleaved-list-over-field budgets, MCA or line-decoding over the actual line field, extension status, and failure-ladder audits. Six-ledger abstract at `tex/snarks_v4.tex:92`.

Main definitions:
- AUDIT: agreement reserve `sigma = a-k`, entropy ledger, `tex/snarks_v4.tex:157`.
- AUDIT: feasible locator fiber, `def:fiber`, `tex/snarks_v4.tex:180`.
- AUDIT: protocol list arity `mu`, `def:list-arity`, `tex/snarks_v4.tex:209`.
- CONDITIONAL: extension-line MCA lift assumption, `ass:extension-mca-lift`, `tex/snarks_v4.tex:242`.
- CONDITIONAL: locator local-limit assumption, `ass:locator`, `tex/snarks_v4.tex:353`.
- CONDITIONAL: line/MCA local-limit assumption, `ass:mca`, `tex/snarks_v4.tex:405`.
- AUDIT: field-separated reserve certificate, `def:cert`, `tex/snarks_v4.tex:436`.

Main theorems and status:
- PROVED: `lem:fiber-list`, fiber-to-list bridge, `tex/snarks_v4.tex:191`.
- PROVED: dyadic one-step hygiene and maximal-remainder hygiene, `prop:dyadic-hygiene`, `lem:max-remainder`, `tex/snarks_v4.tex:552`.
- CONDITIONAL: `thm:ledger`, ledger theorem for reductions already written in the required form and certificates whose evidence applies, `tex/snarks_v4.tex:502`.

Dependencies:
- Papers A/B/D for lower-bound floors, quotient profile, cap, and assumptions.
- ABF toy protocol and extension-list identity.
- Protocol-specific FRI/WHIR rewrites not yet completed.

Open questions created:
- CONJECTURAL: locator local limit, extension-line MCA, line-decoding formulation, curve-MCA, sharp constants, interleaved-list constants.
- AUDIT/ENGINEERING: rewrite FRI/WHIR reductions in exact ledger form and emit certificate schema/scripts. See `tex/snarks_v4.tex:757`.

## `proximity_blueprint_v3`

Abstract-level summary: AUDIT/PLANNING. The blueprint is the research control document. It restates the survey challenges, explains how the manuscripts reshape them, gives a problem matrix, and records missing items. It is not the primary theorem source when the TeX papers have labels. Source map at `tex/proximity_blueprint_v3.tex:76`; corrected question at `tex/proximity_blueprint_v3.tex:147`; problem matrix at `tex/proximity_blueprint_v3.tex:288`.

Main definitions/problems:
- CONJECTURAL: survey MCA and interleaved-list challenges, `prob:survey-mca`, `prob:survey-list`, `tex/proximity_blueprint_v3.tex:104`.
- AUDIT: problem matrix L1/L2/L3/M1/M2/M3/F1/X1/P1/P2/etc., `tex/proximity_blueprint_v3.tex:292`.

Open questions created:
- Same as backlog, but in roadmap form.

## `readme.md` and `agents.md`

Abstract-level summary: AUDIT/PLANNING. `readme.md` gives the repository-level status map and script layer; `agents.md` gives operational rules, priorities, toy cases, and contribution format.

Main content:
- AUDIT: rough status map, `readme.md:149`.
- AUDIT: contribution categories, `readme.md:168`.
- AUDIT: script layer, `readme.md:181`.
- AUDIT: status tags and "do not promote" rule, `agents.md:64`.
- AUDIT: script output standard, `agents.md:354`.
- AUDIT: "what not to do" list, `agents.md:440`.

Open questions created:
- AUDIT: A0 Crites-Stewart import audit.
- AUDIT/EXPERIMENTAL: A1 finite-claim reproduction.
- AUDIT: A2 theorem-number/cross-citation audit.
- EXPERIMENTAL/COUNTEREXAMPLE: small-field searches for locator fibers, MCA slopes, extension-valued witnesses.
