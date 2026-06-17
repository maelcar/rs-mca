# Script Plan

Existing script inspected:

- EXPERIMENTAL: `scripts/run_frontier.py` fixes `N=32`, `l=18`, builds an order-32 subgroup of `F_p`, meet-in-the-middle enumerates elementary-symmetric fingerprints `(e1,e2)` for `l` subgroup elements, records coverage of `F_p^2`, and appends a human line to `frontier_results.txt`. Source: `scripts/run_frontier.py:1`; repo description: `readme.md:183`.
- AUDIT note: it has no argument validation for `32 | p-1`, no JSON certificate, no theorem/problem ID in output, and no dependency pin for `numpy`/`sympy`. It is useful as a prototype for `restricted_sum_dp.py` or `mca_slope_scan.py`, but its outputs remain EXPERIMENTAL.

## Roadmap

| Script | Mathematical object checked | Inputs | Outputs | Certificate format | Theorem/problem ID supported | Output tag |
|---|---|---|---|---|---|---|
| `entropy_margin.py` | Generated-field entropy reserve `entres(a;q_gen)` and `tau*(rho,q_gen)`. | `n,k,a` or `rho,eta`; `q_gen`; target margin; optional field name. | Exact `log2 binom(n,a)`, entropy reserve bits, ratio, pass/fail. | JSON with exact integers plus decimal logs; Markdown table. | `snarks_v4` `eq:entropy-ledger`, `rule:entropy-feasibility`; L1 precondition. | AUDIT / PROVED for arithmetic. |
| `quotient_profile.py` | Active quotient-core list obstructions and dithered dimension hygiene. | `n,k,a` or `sigma`; domain smoothness/factorization; max dither range. | Active divisors `M`, quotient orders `N=n/M`, `log2 binom(n/M-1,k/M)`, remainder warnings. | JSON certificate with divisor list and exact binomial logs. | `slackMCA_v3` `def:qprofile`, `thm:qcore`; `snarks_v4` `eq:qprofile`; L3. | AUDIT / PROVED for arithmetic. |
| `restricted_sum_dp.py` | Restricted sums `h^ wedge Q`, DSH coverage, exact finite Paper A claims. | Field `p`; subgroup order `N`; subset size `h`; generator or subgroup list. | Coverage size, missing residues, witness/backpointer option. | JSON with parameters, subgroup generator, coverage hash, optional witnesses. | Paper A `lem:dsh`, `thm:main`, `app:verify`; A1. | PROVED for exhaustive finite run; COUNTEREXAMPLE if mismatch. |
| `locator_fiber_scan.py` | Feasible locator fibers `Fib_U(a)` and monomial prefix fibers. | Finite field; domain `H`; `k,a`; received word family; quotient-removal flag. | Fiber sizes, largest fibers, support/witness data, quotient-periodic classification. | JSONL rows per word plus summary table. | `slackMCA_v3` `def:locator-fiber`; L1. | EXPERIMENTAL, or COUNTEREXAMPLE if a conjectured finite bound fails. |
| `mca_slope_scan.py` | Support-wise MCA-bad slopes and witness supports. | Finite field; domain; `k`; radius/slack; line family or exhaustive pair mode. | Bad slopes, witness support, explaining codeword, class tag: canonical, quotient-periodic, tangent, residue-line, extension-only. | JSONL witnesses with reproducibility hash. | `slackMCA_v3` `def:mca`, `thm:exactslack`, `thm:normalform`; M1. | EXPERIMENTAL / COUNTEREXAMPLE; PROVED for bounded exhaustive universe. |
| `extension_line_scan.py` | Extension-valued residue-line MCA witnesses. | Base `B=F_p`; extension degree; irreducible polynomial; `H,k,t`; search limits. | `E,B,w,Q_z,S_z` witness data or absence certificate for bounded search. | JSONL witness packet with field representation. | `snarks_v4` `ass:extension-mca-lift`, `op:extension-mca`; Paper D `prob:explicit`; F1. | EXPERIMENTAL / COUNTEREXAMPLE. |
| `interleaved_budget.py` | Interleaved list budget and arity comparison. | Base list bound; direct tiny field instance; `mu`; `q_line`; target lambda. | Product bound, direct enumeration if feasible, list-over-field pass/fail. | JSON certificate plus table. | `snarks_v4` `def:list-arity`, `eq:trivial-interleaving`, `op:interleaving`; L2. | AUDIT / EXPERIMENTAL. |
| `certificate_emit.py` | Full Paper C field-separated reserve certificate. | Outputs of entropy, quotient, list/interleaving, MCA, field ledgers; protocol metadata. | JSON certificate, Markdown/TeX table, failure-ladder audit. | Versioned JSON schema with source refs and status tags. | `snarks_v4` `def:cert`, `rule:reserve`, `thm:ledger`; protocol tasks. | AUDIT / CONDITIONAL depending on evidence. |

## Implementation Standards

- AUDIT: Every script output must print input parameters, exact mathematical object, result, theorem/problem ID, source refs, and status tag.
- AUDIT: Scripts that fetch or install dependencies should not be used during package-registry incidents without explicit approval. Prefer standard library first; if `sympy`/`numpy` is required, document the installed version rather than installing.
- AUDIT: Every exhaustive run should state the finite universe cardinality. If pruning is used, the certificate must explain why pruning is exact.
- AUDIT: Human-readable tables are secondary. JSON certificates are the primary machine-checkable artifact.
- AUDIT: No script should silently append only to a text file. If an append log is useful, also write a deterministic JSON output path or print JSON to stdout.

## Suggested Build Order

1. `entropy_margin.py` and `quotient_profile.py`: cheap, immediately useful for certificates.
2. `restricted_sum_dp.py`: converts Paper A finite claims into reproducible receipts.
3. `locator_fiber_scan.py` and `mca_slope_scan.py`: discovers local-limit obstructions.
4. `extension_line_scan.py`: targets the most important field-transfer unknown.
5. `interleaved_budget.py`: quantifies protocol list denominator pressure.
6. `certificate_emit.py`: integrates the above into Paper C ledger format.
