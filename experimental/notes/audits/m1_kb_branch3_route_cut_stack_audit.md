# Audit of the integrated M1 KoalaBear branch-3 rank-nine route-cut stack

- **Status:** AUDIT
- **Integrated target:** commit `48115af6`, which replayed PR #867 at
  `6ad24364`, PR #871 at `05926894`, and PR #874 at `f8d2c0cf`.
- **Companion verifier:**
  `experimental/scripts/verify_m1_kb_branch3_route_cut_stack_audit.py`.
  It is self-contained, uses only the Python standard library, reads no
  repository file, and reproduces the exact deployed arithmetic from embedded
  source pins.
- **Scope:** statement fidelity, hypothesis windows, ownership units,
  first-match scope, source-to-verifier correspondence, certificate freshness,
  Lean status, and current consumers.  No submission-facing file is changed.

## Verdict

The three mathematical route cuts are statement-faithful.  The actual-core
MDS ladder pays intrinsic ranks 4 through 8 once for one complete retained
family; rank nine is the first nonuniform residual.  The mask packet's
committed full-carrier tail gates are exact.  The syndrome packet's non-CA cap
and its route to sparse sigma are exact.  None moves the ledger or closes rank
nine, branch 3, or the KoalaBear row.

Two interface defects were found and repaired:

1. the generic one-cut helper accepted a predecessor-paid cell and emitted an
   impossible sharpness histogram with high-bin count `-1`;
2. the syndrome JSON called the unpaid sparse route an `owner`, despite its
   own payment flags and note saying that the route is unpaid.

Both defects were outside the live mathematical payment path.  The repair
adds the missing coarse-failure precondition, replaces ownership-like schema
names by neutral terminal/route names, and regenerates the bound certificates.

## Audited core arithmetic source pins

Every path below is audited at `48115af6`; the digest is SHA-256 of that
integrated file.  The table covers the nine core note/Python/JSON artifacts;
the replay READMEs and Sage controls were inspected separately.

| Durable source | SHA-256 |
|---|---|
| `experimental/notes/m1/m1_kb_branch3_actual_core_mds_rank_ladder_v1.md` | `c56bcafd7d6ffb1c4b8c65ed13b1d7dcb16a7888955de2cfdfc9bd8cc203f0f0` |
| `experimental/scripts/verify_m1_kb_branch3_actual_core_mds_v1.py` | `67f2cf1a4a61c0746ffffe17d413f9edcd371caa49a21a1262dec277365851a4` |
| `experimental/data/certificates/m1-kb-branch3-actual-core-mds-v1/m1_kb_branch3_actual_core_mds_v1.json` | `1d33311376fae565924bf9656d2e5f11b59a735238eb053aa6b485cceea80392` |
| `experimental/notes/m1/m1_kb_branch3_rank9_mask_deficit_route_cut_v1.md` | `59d0d6075d023c673ff110ea7a7ee89f1b42ec8e51e90e90303843d3512345c3` |
| `experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py` | `c88d87e11da61f1b2fd2f40a2a39b3c43d3db35afc0bbc01bbded3721de1a880` |
| `experimental/data/certificates/m1-kb-branch3-rank9-mask-deficit-v1/m1_kb_branch3_rank9_mask_deficit_v1.json` | `926a2b34bc2c77b974d478d1ff7dc8bc9de97dc47ee4237e0d3d5e04787c7c8b` |
| `experimental/notes/m1/m1_kb_branch3_rank9_syndrome_rank_reduction_v1.md` | `01cd01406f9994062f416a263e5fa3579631743c69929f9ed6ca2b59b5bc0ea6` |
| `experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py` | `ede048699dff02e9a1031355b36151b93c94a0df0151af07537c3fa505439c19` |
| `experimental/data/certificates/m1-kb-branch3-rank9-syndrome-rank-reduction-v1/m1_kb_branch3_rank9_syndrome_rank_reduction_v1.json` | `b7f346ed1a2c1136ed10f37f40862021d6e5759e7846e87f3d62e3c1ed79870f` |

The three integrated packets are byte-identical to their cited PR heads.

## Findings and repairs

### MUST — unpaid route labeled as an owner

At `experimental/scripts/verify_m1_kb_branch3_rank9_syndrome_rank_reduction_v1.py`
@ `48115af6`, durable objects `expected_rank_reduction` and
`expected_classifier_contract` (lines 548--550 and 578--579), the fields were

```text
correlated_agreement_owner
non_correlated_agreement_owner
sparse_owner_paid_here
owner_terminals
owner_terminal_count
```

The value of `correlated_agreement_owner` was
`CORRELATED_AGREEMENT_ROUTE_TO_SPARSE_SIGMA`, while the same certificate said
`CA_terminal_is_route_not_payment = true` and
`correlated_agreement_branch_paid = false`.  The packet note's
`§6 Exact sparsification route` and `§8 Fail-closed classifier and ledger
semantics`, and its README's `The only mathematical terminals`, all say the
sparse branch is a route rather than an owner.  Thus the mathematics and
charge flags were safe, but the machine-readable ownership vocabulary
contradicted them and was unsafe for a future consumer.

The repaired schema uses

```text
correlated_agreement_terminal
non_correlated_agreement_terminal
sparse_route_paid_here
terminals
terminal_count
```

and changes `next_route` to `SPARSE_SIGMA_FIRST_MATCH_AUDIT`.  Terminal
values, cap, classifier partition, charge flags, and ledger values are
unchanged.  Integrated `main` has no consumer of the removed keys, but the
open sparse-chart lineage does.  PR #909 head `aec5127e` reads
`owner_terminals` and `sparse_owner_paid_here`, and freezes both the old
syndrome certificate SHA-256 and payload hash.  The same consumer is carried
by open PR #883 head `9810a7b4`, #886 head `7b3177c2`, #887 head `8904b7af`,
#889 head `6c268b57`, #895 head `34e08af5`, #896 head `aa66f483`, #898 head
`7a20a509`, #899 head `c68f673c`, #901 head `1e37d22f`, #906 head `bb5e2fff`,
#907 head `aa0fe903`, and #908 head `1ead0a7b`.  These queue consumers must
migrate the keys and regenerate their certificates before rebasing.  Keeping
compatibility aliases would retain the unsafe owner vocabulary, so this v1
shape change is intentionally fail-closed and disclosed as a breaking queue
contract.

### SHOULD — one-cut helper lacked its coarse-failure window

At `experimental/scripts/verify_m1_kb_branch3_rank9_mask_deficit_v1.py`
@ `48115af6`, durable object `one_cut_gate` (line 477), the helper accepted
every residual carrier rather than only the predecessor coarse-failure cells
for which `§5 Sharp one-cut cumulative compiler` derives its threshold.

The exact predecessor boundary

```text
N_V = 1699344,  d_V = 1,  D = 0
```

is already paid because

```text
coarse_cap = 274980655093567589
           <= B_remaining = 274980725508892088.
```

On that input, the displayed threshold formula gives

```text
T_star = 275574617157636283 > m = 274980725508892089,
```

while the old helper clipped `formal_T_star` to `m`, then emitted

```text
sharp_bad_low_count  = m + 1
sharp_bad_high_count = -1.
```

That is not a histogram, and its alleged bad weight still exceeds the ambient
budget.  The helper therefore overstated sharpness outside its theorem window.

The repair requires `coarse_cap(N_V,d_V) > B_remaining` before compiling a
one-cut gate.  The classifier already returns
`PAID_BY_PREDECESSOR_COARSE_RANK9_BOUND` first, so no certified deployed
terminal changes.  The source note now states the equivalent premise
`C_V >= (B_remaining+1)*mu_0`, so the displayed theorem and code have the same
window.  The committed full-carrier gate remains in scope and rechecks exactly:

```text
D = 18014,  H_D <= 17907572507584.
```

### SHOULD — replay instructions overwrote before checking freshness

The `Replay` blocks in all three certificate READMEs at `48115af6` invoked
`--write` before `--check`.  That sequence could replace a stale committed
certificate before freshness was measured.  Each block now checks the shipped
artifact first and labels `--write` as regeneration after an intentional
source change, followed by another check.  This documentation-only change
cascades through source-binding hashes, so all three certificates were rebuilt
in dependency order.

### NOTE — no mathematical or ledger defect

- `actual-core §3 Exact import of the actual-core MDS theorem` uses exactly the imported P2/M1--M5
  hypotheses on one complete selector and one restricted map.  The independent
  rank-cap rebuild gives ranks 4 through 8 paid, worst cap
  `58,747,334,643,050,472`, and rank nine unpaid in the uniform
  worst case.
- `mask-deficit §4 Current-interface extremizer and route cut` correctly identifies the all-zero
  deficit profile as an interface-level extremizer, not a constructed
  Reed--Solomon family.  The repair does not strengthen that claim.
- `syndrome-rank §4 Specialized deterministic rank reduction` has
  `d=1,048,577`, `E=E+=981,104`, witness rank `t=10`, syndrome rank `h=2`,
  and exponent 8.  Exact floor checks give `3,337,935,545,766,696`, with
  margin `271,642,789,963,125,392`.  The deterministic specialization agrees
  with Yuan--Zhu, [arXiv:2605.07595v2](https://arxiv.org/abs/2605.07595),
  Theorem 3.5 and Corollary 3.6; the local note supplies its own proof.

## Hypothesis windows, first match, and consumers

- The actual-core ladder applies once to the one complete retained family.
  Its rank caps are mutually exclusive alternatives, not additive charges.
- The one-cut compiler applies only after the same selector and restricted map
  reach a predecessor coarse-failure cell and after a cumulative tail lemma is
  proved.  No such lemma is promoted by this audit.
- The syndrome classifier partitions the **original received pair** at
  agreement `A=1,116,048`: column-far pays only the non-CA terminal;
  not-column-far routes through exact sparsification to sparse sigma and stays
  unpaid.
- All three packets sit after their named predecessor owners.  They leave
  `U_paid = 2602502999` and
  `B_remaining = 274980725508892088` unchanged.
- `experimental/grande_finale.tex`, durable label
  `rem:audit-convention`, still records no KoalaBear `A=1,116,048`
  U-certificate.  No paper, ledger, or Lean consumer was promoted.
- The open PR #883/#886/#887/#889/#895/#896/#898/#899/#901/#906--#909
  lineage consumes the old v1 syndrome keys and hashes.  It must be updated
  and regenerated; this repair does not silently bless those queue artifacts.
- Intrinsic rank nine outside the paid joint boundary, intrinsic ranks at
  least ten, sparse sigma, branch 3, and the KoalaBear row remain open.

## Source-to-verifier correspondence and replay

The actual-core verifier checks exact caps, selector/classifier prerequisites,
source hashes, and ledger immobility; it string-anchors rather than formalizes
the imported theorem, exactly as its note disclaims.  The mask and syndrome
verifiers rebuild their JSON payloads and source bindings, enforce fail-closed
classifiers, and reject semantic tampers.  None performs a deployed selector
census, and none claims to.

The following all passed under ordinary CPython and `python3 -O`:

```text
actual-core  --check; --tamper-selftest  58/58
mask-deficit --check; --tamper-selftest  67/67
syndrome     --check; --tamper-selftest  68/68
stack audit  --check; --tamper-selftest  14/14
```

Sage was unavailable, so no Sage execution is claimed.  Its companions were
read for scope; their finite-field examples are controls, not deployed-field
censuses.  Lean is explicitly unstarted and unauthorized for these packets;
no Lean result is claimed.

There is no `SHA256SUMS` manifest in the three certificate directories.  The
JSON payload hashes and every declared source binding were independently
recomputed.  Certificate SHA-256 values changed only through the repairs and
their dependency bindings:

| Certificate | Integrated `48115af6` | Repaired |
|---|---|---|
| actual-core | `1d33311376fae565924bf9656d2e5f11b59a735238eb053aa6b485cceea80392` | `750d2ff597730fcf47b3867f08bbf34bce613ab7aca2746bee923b1f9d585eca` |
| mask-deficit | `926a2b34bc2c77b974d478d1ff7dc8bc9de97dc47ee4237e0d3d5e04787c7c8b` | `365a57690651e2a72fe32c5104b05f710e5cb07ac364fda4b1492217483ee7d1` |
| syndrome-rank | `b7f346ed1a2c1136ed10f37f40862021d6e5759e7846e87f3d62e3c1ed79870f` | `e08a427159df818b79995532d11ecdc27f98d8f3a874d9eb76d449ade85090a9` |

## Risk limits

This audit validates the integrated route-cut statements and their exact
finite arithmetic.  It does not construct a rank-nine family, prove a missing
tail or sparse-sigma incidence lemma, promote a zero-cost owner, add caps from
exclusive cases, move a ledger value, close branch 3, or close the KoalaBear
row.
