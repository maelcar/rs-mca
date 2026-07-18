# Audit: balanced-core producer-to-atlas correspondence

**STATUS:** `COUNTEREXAMPLE`

**Audited integrations:**

- `d287e1d2`: PR #534 head `e9aca0c5` and PR #535 head `114f845a`;
- `c23dcaa0`: PR #713 head `d78ea57e`;
- `06b2a6fb`: PR #868 head `5055340d`; and
- current audited upstream snapshot `c4856fa6`.

## Verdict

PR #868's factor-aware rank repair is mathematically clean. Its exact F_11
syndrome-line witness, 1,140-triple census, frozen certificate, and
normal/optimized tamper gates all replay.

The integrated producer-to-consumer interface was not clean. PR #713's atlas
verifier still required PR #534's retired sentence
`residual charts force kappa = k = Theta(n)`. After PR #868 correctly removed
that sentence, the exact advertised command failed `218/219` in normal and
optimized Python, while the JSON sidecar still said `PASS 219/219` and
`all_pass: true`. The old #534/#535 verifiers also continued to call raw
prefix-support families actual residual charts and raw member counts realized
slopes.

This is a counterexample to the integrated verifier/certificate and
source-to-consumer claims. It is not a counterexample to the corrected
shortening law, the conditional atlas ledger, or the conditional Lean routing
theorem.

## MUST findings

- **MUST — stale executable consumer.**
  `experimental/scripts/verify_atlas_cat_ledger.py:248-279 @ c4856fa6`
  requires the retired label at line 271. The corrected producer instead says
  `COMPUTED` only for raw empty-core prefix families and leaves positive-rate
  actual first-match residual growth open at
  `experimental/notes/thresholds/balanced_core_kappa_growth.md:15-27,131-213 @ 06b2a6fb`.
  Independent normal and optimized replay gave exactly
  `RESULT: FAIL (218/219)`; all other 218 gates passed.

- **MUST — stale, unbound certificate claim.**
  `experimental/data/certificates/atlas-cat-ledger/atlas_cat_ledger.json:6-12,92-100 @ c4856fa6`
  records `PASS 219/219`, `all_pass: true`, and
  only PRs #518/#528 for C8. The integrated atlas verifier at
  `c4856fa6` never opened the JSON. Its SHA-256 was
  `603d9a2ba28711239f885395b8f9a925eef60fb87ab2e1e148cc797350d20e89`;
  the failing verifier SHA-256 was
  `cdcdae5ee4699a8f2c6106bb49a0216d9124910b98a1f427ac0d04b2701157b1`.

- **MUST — raw family promoted to actual residual.**
  `experimental/scripts/verify_kappa_growth.py:6-24,233-240,282-329 @ c4856fa6`
  called raw prefix classes residual balanced cores, treated the
  largest member class as the class carrying most rays, called a class
  fraction mass, and printed `residual => kappa=k=Theta(n)`.
  `experimental/scripts/verify_a4_coverage.py:6-35,226-263,292-385 @ c4856fa6`
  printed `FIBER = CHART`, said a raw fiber “IS” the actual
  high-kappa chart, and called the raw PTM family paid. Those assertions exceed
  the corrected notes, which explicitly separate raw supports, shortened rows,
  first-match survival, and realized distinct slopes.

- **MUST — two hash-frozen prose consumers remain stale.**
  `experimental/notes/thresholds/a6_actual_witness_core_rank_preflight.md:1420-1432 @ c4856fa6`
  says `kappa=Theta(n)` genuinely occurs on relevant
  balanced cores and that #535 already pays those charts.
  `experimental/notes/roadmaps/b2_l1_reduction_ledger.md:91-101 @ c4856fa6`
  calls #534's PTM pair a residual family that blocks the decoding-side route.
  Both files are byte-bound by independent certificates/verifiers; this packet
  records the overclaims without silently invalidating those unrelated frozen
  packets. They must not be used for promotion until their owning packets
  refresh the wording and hashes together.

## Repair

The executable and unfrozen consumer repair is deliberately narrow.

1. PR #713's Block C now consumes the corrected raw-family sentence.
2. Block D loads and SHA-256-pins the frozen JSON, then folds semantic
   certificate checks into the existing 14 gates, preserving `219/219`. It
   checks the nine cells, tally, blocker set, residual targets, composition
   verdicts, TeX source, verifier results, `all_pass`, and C8 provenance
   `{#518,#528,#534,#868}`.
3. `verify_kappa_growth.py` retains all 95 arithmetic gates, labels the census
   and PTM pair as raw prefix-support families rather than realized slopes, and
   now explicitly checks `n/4 <= kappa <= n/2` on every scalable PTM row.
4. `verify_a4_coverage.py` retains all 63 gates, removes
   raw-fiber-equals-chart claims, and replaces the false “differing kappa”
   sample with explicit synthetic subfamilies of raw `kappa=4,5,6`; transfer
   to an actual residual still requires a separately certified inclusion.
5. The unfrozen #686/#623 provenance wording now calls #534 a raw PTE
   stress family and the secant quantity an upper-bound constant, not an
   attained actual-residual slope count.

The repaired atlas certificate SHA-256 is
`df79dad137e2ff8241eb35c8bafe977454508917eb2fa714a302e6467f10862d`.
Changing only the first byte of the historical `base_sha` field gives
deterministic SHA-256
`e49c7c09cab46463dc511272a861e814fd89f778d35f7e753bb906ee24bcbb91`;
normal and optimized atlas checks reject it `218/219` without rewriting it.
A missing certificate is also rejected.

## Mathematical, ownership, and Lean boundaries

- The raw identity is
  `kappa_raw = max(0, k - |C_raw|)`.
- Factoring a common core `K` shortens the row to `k' = k - |K|`; empty
  residual core gives `kappa' = k'`, not the original `k`.
- Raw prefix-family size is a support count, not a realized distinct-slope
  count. A raw family is not automatically a surviving first-match owner.
- The atlas C8 row remains **CONDITIONAL** for higher-dimensional charts; no
  hard input, deployed threshold, or paper theorem is promoted.
- PR #782 head `34f91bd6` is a clean conditional consumer.
  `HighKappaCoverage.lean` requires an ambient shallow-prefix certificate,
  semantic bridge, residual inclusion, and SE2 certificate. It erases
  `kernelDim` only from that finite inequality and explicitly does not prove
  actual-residual existence, asymptotic shallowness, or deep-prefix MI/MA.
  Direct compilation succeeds; `kernelIndependentDirectRC_iff` has no
  axioms, and the general theorems report only `propext` and `Quot.sound`
  (the toy also reports `Classical.choice`). No `sorry`, `admit`, or
  custom axiom occurs.

No submission-facing TeX, PDF, theorem row, or proof architecture is changed.

## Producer and consumer interlocks

- #518 head `c4f55508`: split-pencil counterexample/owner boundary.
- #528 head `12f68ecc`: field-independent transverse-secant upper bound.
- #534 head `e9aca0c5`: original raw prefix/kernel census and stale wording.
- #535 head `114f845a`: kernel-independent shallow-slice routing.
- #564 head `96f0698a`: hash-frozen roadmap consumer with stale residual
  wording.
- #623 head `c2027dc`: PTE image-face consumer repaired here.
- #681 head `af46e334`: hash-frozen actual-core consumer with stale wording.
- #686 head `db160c6f`: MI/MA route-map provenance repaired here.
- #713 head `d78ea57e`: atlas producer repaired and certificate-bound here.
- #727 head `c6d09aed`: historical `c23dcaa` reconciliation; its recorded
  #713 `219/219` replay was true at that commit and is true again after this
  repair.
- #782 head `34f91bd6`: conditional Lean consumer, clean.
- #868 head `5055340d`: corrected factored-rank producer, clean.

## Replay

From repository root:

```bash
python3 experimental/scripts/verify_balanced_core_atlas_consumer_audit.py
python3 -O experimental/scripts/verify_balanced_core_atlas_consumer_audit.py
python3 experimental/scripts/verify_atlas_cat_ledger.py --check
python3 -O experimental/scripts/verify_atlas_cat_ledger.py --check
python3 experimental/scripts/verify_atlas_cat_ledger.py --tamper-selftest
python3 -O experimental/scripts/verify_atlas_cat_ledger.py --tamper-selftest
python3 experimental/scripts/verify_kappa_growth.py
python3 -O experimental/scripts/verify_kappa_growth.py
python3 experimental/scripts/verify_a4_coverage.py
python3 -O experimental/scripts/verify_a4_coverage.py
python3 experimental/scripts/verify_balanced_core_factored_rank.py
python3 -O experimental/scripts/verify_balanced_core_factored_rank.py
python3 experimental/scripts/verify_balanced_core_factored_rank.py --tamper-selftest
python3 -O experimental/scripts/verify_balanced_core_factored_rank.py --tamper-selftest
python3 experimental/scripts/verify_pte_extremality.py
python3 -O experimental/scripts/verify_pte_extremality.py
```

Expected audit result:

```text
RESULT: PASS (22/22)
STATUS: COUNTEREXAMPLE
```

The PTE verifier returns `RESULT: PASS (45/45)` in both modes. The pre-existing
#686 route-map verifier is not represented as clean: at `c4856fa6`,
`python3 experimental/scripts/verify_mi_ma_sidon_route_audit.py` and its `-O`
replay both return `RESULT: FAIL (58/61)` solely at stale `agents.md` anchors
47, 61, and 62. This packet pins and checks only the repaired provenance
sentences in that note; it does not alter `agents.md` or claim a full #686
packet replay.

Lean replay from `experimental/lean/asymptotic_spine`:

```bash
lake env lean AsymptoticSpine/HighKappaCoverage.lean
```
