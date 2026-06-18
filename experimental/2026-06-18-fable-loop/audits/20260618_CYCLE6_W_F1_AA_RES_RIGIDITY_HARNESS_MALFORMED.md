# Cycle 6 Audit: W-F1-AA-RES Rigidity Ads-Lane Run

Status: HARNESS_MALFORMED_VISIBLE_TERMINAL / AUDIT.

Run:

- Run id: `2026-06-17T22-23-23-620Z-cycle6-w-f1-aa-res-rigidity-vscode-credit-20260618-6446e85d`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T22-23-23-620Z-cycle6-w-f1-aa-res-rigidity-vscode-credit-20260618-6446e85d`
- Lane: VS Code credited terminal ads lane.
- Raw/malformed copies:
  - `../raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RAW_MALFORMED.json`
  - `../raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RESPONSE_MALFORMED_VISIBLE_TERMINAL.md`
  - `../raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RUN_RESULT.json`

## Verdict

Do not bank mathematical content from this run.

The wrapper classified the run as `HARNESS_MALFORMED_VISIBLE_TERMINAL` and did
not materialize a clean `response.md`. The visible-terminal answer appears to
contain a substantive `BANKABLE_LEMMA` candidate about the rigidity half of
`W-F1-AA-RES`, but the text is damaged: spaces/letters are missing and several
paragraphs/equations are duplicated. Under the project rule, only clean
`response.md` counts as theorem evidence.

## Receipts

`run_result.json` records:

- `status`: `failed`
- `classification`: `HARNESS_MALFORMED_VISIBLE_TERMINAL`
- `responsePath`: `null`
- `malformedResponsePath`: `response_malformed_visible_terminal.md`
- `adSeenInTranscript`: `true`
- `sentinelSeen`: `true`
- `noOutputTimedOut`: `false`

Hashes of preserved copies:

```text
aef7ac2bf6497f1d71cad2a11112576b935466cea231636fe460e2d5240f48c8  raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RAW_MALFORMED.json
36fe96529921e9e049ccba8b2a0db37fcfc07fb155225ff0037466376f6e4098  raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RESPONSE_MALFORMED_VISIBLE_TERMINAL.md
7fa7e602940ebb7085ff3f6d1cca4374937d8b204b189e1364bf66b8fcd53adf  raw/20260618_CYCLE6_W_F1_AA_RES_RIGIDITY_RUN_RESULT.json
```

## Not Banked

The apparent candidate lemma should be treated only as a retry target:

- balanced `a=k+t` subsets;
- slope as interpolant residue `[interp_S(w)]_E`;
- same-slope kernel allegedly `E*F_{<k}[X]`;
- full count allegedly reduced to the base paired readout modulo `Ehat`;
- conjugation as a bijection to the conjugate datum rather than a self-symmetry.

These statements may be true, but they are not banked from this run because the
artifact is corrupted. A clean rerun should ask for this candidate lemma in a
short ASCII-only format and require no duplicated paragraphs.

## Field Ledger

- `q_gen`, `q_line`, `q_chal`, `B`, and `F` are unchanged from Cycle 5.
- No protocol denominator saving is claimed.
- No line-decoding, list-decoding, or `ass:extension-mca-lift` claim is banked.
