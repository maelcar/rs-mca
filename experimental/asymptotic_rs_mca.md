# Asymptotic RS MCA Audit Ledger

This file is the audit companion for `experimental/asymptotic_rs_mca.tex`.
When a PR proposes changes to `asymptotic_rs_mca.tex` or its PDF, do not apply
those files directly.  Record the proposed change here first, with enough detail
for a human maintainer to decide whether the paper should be edited.

Use this ledger for:

- proposed theorem, lemma, proof, or wording changes to `asymptotic_rs_mca.tex`;
- audit results that support or challenge a specific step in the paper;
- references to machine-checkable certificates, scripts, and notes that back an
  audit claim;
- explicit nonclaims and open proof obligations.

For each entry, include the PR/source, proposed paper impact, status, files
preserved elsewhere, and next action.

## Entries

### 2026-07-10 - Initial audit policy for paper-level PR changes

- **Source:** Maintainer instruction during open-PR integration.
- **Status:** AUDIT.
- **Paper impact:** This ledger is now the holding place for proposed
  `asymptotic_rs_mca.tex` / PDF changes.  Paper files are not edited directly
  during PR integration unless a maintainer explicitly promotes the audited
  change.
- **Current scan:** The already-fetched PR refs `#459--#478` contain no
  `.tex` or `.pdf` diffs relative to `main`; their useful asymptotic-paper
  material is in notes, data, Lean, and verifier scripts.
- **Next action:** For future PRs with paper diffs, summarize the intended
  theorem/proof change here, cite the proposed source files, and state whether
  the change is `NO ISSUE`, `NEEDS REVISION`, `COUNTEREXAMPLE`, or
  `PROMOTION CANDIDATE`.

### 2026-07-10 - Second-opinion audit packets for asymptotic_rs_mca.tex

- **Source:** PRs `#459`, `#460`, `#461`, and `#462` by LegaSage.
- **Status:** EXPERIMENTAL / AUDIT.
- **Paper impact:** These PRs do not edit the paper.  They provide independent
  second-opinion checks of four local steps in `asymptotic_rs_mca.tex`:
  Stirling / `g*` table arithmetic, sigma-block diagonal construction,
  BSG/quasicube contradiction arithmetic, and pole-line division over `F_p`.
- **Verdict to preserve:** Each packet reports `NO ISSUE` and agreement with
  the earlier #435 audit route, but this is still audit support rather than a
  paper theorem change.
- **Files preserved elsewhere:** The detailed notes, JSON certificates, and
  verifier scripts should live under `experimental/notes/audits/`,
  `experimental/data/certificates/`, and `experimental/scripts/`.
- **Next action:** If the paper is revised, cite these as independent audit
  support for the corresponding proof steps rather than copying their text into
  the paper.

### 2026-07-10 - C9 / endpoint refinements preserved outside the paper

- **Source:** PRs `#463` and `#464` by DannyExperiments, PR `#465` by
  scottdhughes, and PR `#466` by scottdhughes.
- **Status:** PROVED / EXPERIMENTAL / AUDIT, depending on the subclaim.
- **Paper impact:** These PRs refine the asymptotic C9 story around endpoint
  shortening, split-prime Parseval descent, major-arc value-set structure, and
  Frobenius-closure formal support.  They do not directly edit
  `asymptotic_rs_mca.tex` in this integration pass.
- **Verdict to preserve:** The endpoint Plotkin and split-prime notes are
  useful subregime refinements, but they explicitly do not close the full
  C1--C8 emission/add-back or any deployed finite adjacent row.  The major-arc
  packet is experimental structure evidence explaining why literal C9 fails as
  a standalone target.  The Frobenius-closure Lean packet is useful formal
  backing for the cyclic-code closure primitive invoked by the C9 discussion,
  not a formalization of the whole theorem.
- **Files preserved elsewhere:** Notes are under
  `experimental/notes/thresholds/`, Lean support is under
  `experimental/lean/powersum_rigidity/`, and verifier scripts are under
  `experimental/scripts/`.
- **Next action:** Use these as supporting audit material when revising the
  C9/primitive-residual discussion.  Do not promote them as a complete
  safe-side proof without a separate proof that the residual cells are
  exhausted and paid with constants.
