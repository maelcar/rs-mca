# Audit: triple-negative first-match source correspondence

**STATUS:** `COUNTEREXAMPLE`

**Audited references:**

- PR #829 head `abdef3be`, based on `9c4ca98c` and manually integrated in
  `168e9ba0`;
- the current audited upstream snapshot `c4856fa6`;
- fixed-slope source PR #823 head `06c06581`, which covers PR #817 head
  `5c4c6a42`; and
- augmented-basis correction PR #832 head `402b2703`.

## Verdict

The arithmetic theorem and its Lean kernel are clean.  Independent finite
enumeration finds no exception to the denominator nesting, either puncture
branch, or the forced `kappa,delta` region.  The Lean module compiles without
proof escapes and formalizes exactly the integer arithmetic, not the external
pair-counting or semantic first-match claims.

The integrated packet did not replay.  PR #829 pinned a sentence and full-file
hash from the old paving source.  The same manual integration also imported
PR #832, which deliberately replaced that sentence and refined the residual.
All four commands advertised by PR #829 therefore failed on integration day
and still failed at `c4856fa6`.  The packet also continued to call PR #817
pending even though the same integration imported its superset PR #823.

This is an integration-correspondence and statement-ownership repair.  It is
not a counterexample to the triple-sign collapse, either complete-pair bound,
or an in-chamber inverse theorem.  Credit for the underlying deep-hole
pencil/design correction belongs to PR #832; this audit catches the omitted
refresh in its PR #829 consumer.

The status applies to the advertised replay and source/certificate
correspondence claim, not to the mathematical reduction itself.

## MUST findings

- **MUST — the advertised certificate replay was stale at integration.**
  `experimental/scripts/verify_triple_negative_first_match_reduction.py:36 @ c4856fa6`
  required the retired marker
  `basis-heavy deep-hole owner dichotomy`.
  `experimental/data/certificates/triple-negative-first-match-reduction/triple_negative_first_match_reduction.json:751-764 @ c4856fa6`
  pinned that marker at line 475 and pinned the old source SHA-256
  `01a819ab3fea134c22bfebb51d0074ee32c378b0452f6f682f44304fec7db43d`.

  PR #832 changed the source in the same `168e9ba0` integration.  Current
  `experimental/notes/thresholds/all_pair_paving_basis_multiplicity_compiler.md:487-512 @ c4856fa6`
  instead has the unique marker
  `deep-hole pencil/design owner dichotomy`, line SHA-256
  `26e7b28d3a9e6e08f184bcbea949600c14727570761fc323ccf6a8fe80c59fc1`,
  and full SHA-256
  `84d1ed18a110f0e1fee423905bee5710be42f3e8651cefd50db9646d5ffcc239`.
  The retired marker occurs zero times, so the verifier's old diagnostic
  “not unique” meant missing, not duplicated.

  On untouched `c4856fa6`, normal and optimized `--check` and
  `--tamper-selftest` all exited 1 with:

  ```text
  triple-negative-first-match-reduction: FAIL: source marker is not unique:
  The exact remaining wall is the **basis-heavy deep-hole owner dichotomy**
  ```

- **MUST — the packet certified the wrong dependency state.**
  `experimental/notes/thresholds/triple_negative_first_match_reduction.md:33-36,66,459 @ c4856fa6`
  called PR #817 pending and denied treating it as integrated.
  `experimental/scripts/verify_triple_negative_first_match_reduction.py:373 @ c4856fa6`
  and the certificate at line 250 repeated that nonclaim.  Manual integration
  `168e9ba0` imported PR #823 head `06c06581`, explicitly covering PR #817
  head `5c4c6a42`, alongside PR #829.  The arithmetic reduction remains
  standalone, but its source-status claim was false.

## SHOULD and NOTE findings

- **SHOULD — consume PR #832's corrected residual boundary.**
  `experimental/notes/thresholds/triple_negative_first_match_reduction.md:394-398 @ c4856fa6`
  treated basis heaviness as inverse information pointing toward a common
  flat or low-degree locator.  PR #832 proves at
  `experimental/notes/thresholds/augmented_basis_pencil_design_inverse.md:14-33,125-139 @ c4856fa6`
  that `beta=binom(N,kappa+1)` is automatic when `d=R`; basis heaviness
  alone has no inverse content.  The correct source target is the distributed
  core-pencil/almost-Steiner design dichotomy at lines 389-400.

- **NOTE — the PR #832 affine-line fixtures are not in-chamber
  counterexamples.**  Their `kappa=1` lies outside `J_K<=0`, which forces
  `kappa>=2`.  They show that generic deep-hole basis saturation need not
  have a global core; they do not refute a stronger inverse using the
  additional `J_K` and first-match hypotheses.

- **SHOULD — narrow the package-map ownership wording after its current
  overlap clears.**
  `experimental/lean/grande_finale/README.md:30-31 @ c4856fa6` and
  `experimental/lean/grande_finale/FORMALIZATION_SUMMARY.md:21-22 @ c4856fa6`
  say the module formalizes the “first-match reduction.”  The module has no
  first-match object, pair family, owner, or counting theorem.  Its exact
  surface is integer denominator identities, the forced parameter region, and
  the triple-sign collapse to `J_K<=0`.  Open PR #925 head `c8b4860e`
  already edits both package maps for a separate ownership repair, so this
  packet records the remaining wording issue without creating a conflicting
  second map edit.

## Repair

The producer note now records PR #823 as integrated, keeps the arithmetic
standalone, and distinguishes the general local ratio target from PR #832's
deep-hole pencil/design correction.  It explicitly records that the
positive-depth affine-line fixture lies outside `J_K<=0`.

The verifier now binds the current unique source sentence and reports an exact
marker count on future failures.  The certificate refreshes:

- the paving-source full SHA-256 from `01a819ab...` to `84d1ed18...`;
- the source pin from retired line 475 / `e55399f1...` to current line 487 /
  `26e7b28d...`;
- the false pending-source nonclaim; and
- the remaining-wall description.

No arithmetic fixture changes.  The canonical payload moves from
`6ee918e4c6034cc4f97e5aa436a312934acd291ecda3bff5453cb20fee7313fe`
to
`a8c0ae04007b364cb7d47ec6f04b0985399a18b7a70ab159698dca6aca3e024d`.

The repaired full-file SHA-256 values are:

- producer note:
  `2f0f20c7c03a4c0dd2a3fb0b3aae6001728166aae0798a971aed77666328c953`;
- producer verifier:
  `4cd3d8a1983c5ebc267836884000008c0bdfa14a31b1d06772df4febfa2d736d`;
- certificate:
  `f72948230473cd2ff4f4b3d12f1ce3aa2dfded07d4a7fb3918a99885e27b95d1`.

The retired integrated hashes were respectively `53bd520b...`,
`07ef4aef...`, and `ff33f8ea...`.

## Producer correspondence and independent arithmetic

PR #829's note, verifier, certificate, and Lean source are byte-identical at
head `abdef3be`, integration `168e9ba0`, and current main `c4856fa6`.
Their Git blobs are `85aafd67`, `3f52f78a`, `863b3b1d`, and
`75d3cf90`.  The break was created by the same-wave source replacement, not
by later drift.

The original certificate's canonical payload `6ee918e4...` recomputes
exactly against its retired source state.  All 30 arithmetic fixtures
reconstruct.  Exactly one of its four full source digests and one of its eight
line pins was stale on integrated main.

The repaired producer independently scans all `3,412,800` valid tuples with
`N<=80`: exactly `892,834` have `J_K<=0`, including `2,287` equality
rows and `811,157` positive-depth rows.  Every such row has both predecessor
denominators strictly negative.  The audit verifier separately scans
`213,200` tuples through `N<=40`, recovering `48,012` nonpositive rows,
both `rho` branches, `447` equality rows, and no exception.

The fixed-slope PR #823 packet replays in normal and optimized modes with
payload
`e8e4ee730d95d5347d934e2fd610dc453289e844d4688d30c572fe2f5c9e6c4b`;
both tamper modes reject `10/10`.  The PR #832 packet likewise replays with
payload
`59f7da83e72af6a1d94f78c984b13a05949d887f25934e5fec0b87b996959b9a`
and rejects `10/10` mutations in both modes.

## Lean and consumers

From `experimental/lean/grande_finale`,

```bash
lake env lean GrandeFinale/TripleNegativeFirstMatchReduction.lean
```

exits zero.  The module has six definitions and fifteen theorems, no `sorry`,
`admit`, declared `axiom`, `unsafe`, `opaque`, `partial`, or
`noncomputable` declaration.  Its printed foundations are only
`propext`, `Classical.choice`, and `Quot.sound`.  It proves the arithmetic
sign collapse and forced region; complete-pair bounds (20)/(22), their minimum,
first-match ownership, profile add-back, and asymptotics remain outside Lean.

Current upstream has only the umbrella import in
`experimental/lean/grande_finale/GrandeFinale.lean:42 @ c4856fa6`; no
downstream theorem references this namespace.  Open PR #882 head `af213091`
imports the umbrella transitively but uses none of these declarations.  No
open PR overlaps a repaired PR #829 file.

## Replay

From repository root:

```bash
python3 experimental/scripts/verify_triple_negative_first_match_correspondence_audit.py
python3 -O experimental/scripts/verify_triple_negative_first_match_correspondence_audit.py
python3 experimental/scripts/verify_triple_negative_first_match_reduction.py --check
python3 -O experimental/scripts/verify_triple_negative_first_match_reduction.py --check
python3 experimental/scripts/verify_triple_negative_first_match_reduction.py --tamper-selftest
python3 -O experimental/scripts/verify_triple_negative_first_match_reduction.py --tamper-selftest
```

Expected audit result:

```text
RESULT: PASS (16/16)
STATUS: COUNTEREXAMPLE
```

The repaired producer returns
`triple-negative-first-match-reduction: PASS` with payload `a8c0ae04...`
in both check modes and `tamper_mutations_rejected=10` in both tamper modes.

No submission-facing TeX/PDF, mathematical theorem, numerical fixture, Lean
declaration, theorem API, first-match assignment, deployed threshold, or proof
architecture is changed.
