# Rank-one admission prose/source correspondence audit

## Claim and status

```text
STATUS: COUNTEREXAMPLE
```

The counterexample is narrow and repository-semantic.  At upstream
`c4856fa6`, the audit integrated from PR #866 head `0b45db15` said that the
claim "grammar acceptance alone remains" was `FIXED IN PROSE`.  Only the note
originating in PR #824 head `2f5162fc` had been repaired.  Four integrated
producer/consumer notes remained unchanged from PR #818 head `03fa2958`, PR
#820 head `d5f67b4b`, PR #827 head `1512ff45`, and PR #842 head `ea8318ff`, and
still narrowed the residual to grammar acceptance.

Those four immutable blobs are counterexamples to the unqualified claim that
the prose repair was complete and source-bound.  They are not source-derived
counterexamples to the rank-one construction.  In particular, they do not
refute the T4 capped-Walsh inequality, the S4 scalar omega cap, any finite
scan, or the arithmetic Lean shadows.

## Immutable pre-repair pins

The affected producer/consumer notes were integrated in `168e9ba0`; the audit
packet was integrated in `06b2a6fb`; all remained present at upstream
`c4856fa6` before this repair.

| Artifact | Immutable producer | Git blob | SHA-256 | Pre-repair statement |
|---|---|---|---|---|
| `experimental/notes/thresholds/rank_one_emission_arithmetic.md` | PR #818 head `03fa2958` | `03df4497` | `03c19def9af114fa45b4b134b308a9257cef7849e36d50eb49bb076db7b7e7b9` | lines 57--63 and 292--309 reduced admission to the grammar decision |
| `experimental/notes/thresholds/omega_sound_emission_floor.md` | PR #820 head `d5f67b4b` | `8d8f9b04` | `a29e4682aad5be95fe4d5ca16245432fa8a480a2da74a496c8c1ca9ab5d31671` | lines 46--50, 179--188, 225--227, and 238--253 said pure grammar acceptance / compiler soundness |
| `experimental/notes/thresholds/shell_mass_spectral_law.md` | PR #827 head `1512ff45` | `be949c19` | `57a8521197d79ef9757f65162d912f6dd06f8262361f8ab9014f280260dbc273` | lines 51--52 named only "the admission acceptance" |
| `experimental/notes/thresholds/product_profile_transfer_certificate.md` | PR #842 head `ea8318ff` | `6365c949` | `29ec195f210bca5e7ffe597166653b24744191c7f46219c8b2adfe80dc675b60` | lines 44--51 and 209--211 retained the same incomplete residual |
| `experimental/notes/audits/rank_one_admission_interface_audit.md` | PR #866 head `0b45db15` | `d46c6263` | `ac8bf14464be4ab43bdfb403fea0f3a4514759393a6f3885bcf2abc996789b77` | lines 19--23 said `FIXED IN PROSE` without identifying the unchanged consumers |
| `experimental/scripts/verify_rank_one_admission_interface.py` | PR #866 head `0b45db15` | `ef4e4b28` | `42340a2de3f5417e3d453826ff2603d2b9cfd5de79ca006c4a49239398b83ca0` | checked universal cube arithmetic and its JSON, but no source note or source hash |
| `experimental/data/certificates/rank-one-admission-interface/rank_one_admission_interface.json` | PR #866 head `0b45db15` | `d14924fa` | `8722646da230e5dd64412759afefef560a4a11c51ec896e96eaedcbac4f108c3` | fresh against its verifier, but not source-bound |
| `experimental/scripts/verify_rank_one_greedy_adequacy.py` | PR #824 head `2f5162fc` | `9b6e0ad4` | `70257d229c45a2fe28409c5275330c25148fce04f3bedf0a1f0d6c3fa7dcaa1f` | lines 13--30 and 300--306 used unscoped paid-in-full wording |
| `experimental/data/certificates/rank-one-greedy-adequacy/rank_one_greedy_adequacy.json` | PR #824 head `2f5162fc` | `cfafec6a` | `a2855d5505c1976fec5b8cca21ded8ec0fcd523478757f7b3679eec2d12415a9` | listed T1--T4 without a semantic-scope field |
| `experimental/lean/rank_one_greedy_adequacy/RankOneGreedyAdequacy.lean` | PR #824 head `2f5162fc` | `3e11e3d2` | `ad80ce541b5a18f2c2ca003a8f5a96e75eca23a37bcde3a90214c2118f0c80f8` | comment header said adequacy closed; code remained an arithmetic shadow |
| `experimental/scripts/verify_omega_sound_emission_floor.py` | PR #820 head `d5f67b4b` | `ee39de61` | `6f9b85eebb46a1030bd844147c428efb025ea9d01a27bb9ed18f5c02588a6e50` | docstring/output used compiler-sound and paid-in-full wording |
| `experimental/data/certificates/omega-sound-emission-floor/omega_sound_emission_floor.json` | PR #820 head `d5f67b4b` | `e61ce3e3` | `4b4864557377273b7a0197f3204197e5caecc7ada91dcc9628e35e998a06a663` | listed S1--S5 without a semantic-scope field |
| `experimental/lean/omega_sound_emission_floor/OmegaSoundEmissionFloor.lean` | PR #820 head `d5f67b4b` | `8062cfe7` | `8587303252c4174d93a562b3c8011a5406e32c54354d0821aa5b5d363fd7819e` | comment header promoted local arithmetic to compiler soundness |

Git blob identifiers in the table are content identifiers, not abbreviated
branch tips.  The accompanying verifier also embeds the full 40-character PR
heads, full blob identifiers, and full SHA-256 digests.

## MUST — statement accuracy and first-match scope

The repaired T4 theorem has the following exact window: one fixed Boolean
cube/class, all Walsh modes allowed by inversion, and the scalar cap
`sum h_+`.  Its ownership unit is a cube truth table.  Its proof uses no
source chart, owner, realized profile cell, first-match projection, or
source-derived slope.

The repaired S4 theorem has a different but still local window: already-given
disjoint pieces and classes, a named scalar coefficient, and a cap preventing
omega overcredit.  Its ownership units are the supplied piece/class accounts.
It constructs none of those units from a source word.

The governing profile-payment interface therefore remains open after both
results.  It requires an actual same-owner first-match cell, an A4
analytic/Sidon payment, a separate A6/RC distinct-slope bound, and a uniform
subexponential aggregate census.  A grammar rule is an additional syntactic
step, not a replacement for any of these mathematical interfaces.

## MUST — source-to-verifier correspondence

The PR #866 head `0b45db15` verifier correctly reports that capped-Walsh
adequacy is structure-free and that profile payment is not certified.  Normal
and optimized replay both give 46,644 exact checks over 6,662 cube functions;
tamper replay rejects 3/3 false strengthenings.  Its checked JSON regenerated
byte-for-byte before this audit.

That freshness relation covered only Python-to-JSON arithmetic.  The verifier
read no producer note, consumer note, governing source, Lean file, or source
manifest.  Consequently it could pass while the four stale prose consumers
remained unchanged.  This is the precise source-to-verifier correspondence
failure; it is not a failed arithmetic gate.

The follow-up verifier
`experimental/scripts/verify_rank_one_admission_prose_correspondence_audit.py`
imports none of the audited verifiers.  It computes Git blob SHA-1 and SHA-256
with the standard library, pins fourteen repaired live artifacts, validates
the locally available pre-repair, producer-head, and integration commits,
checks integration-message PR references and ancestry, resolves each path in
the producer head, integration tree, and pre-repair tree to the same pinned
blob, recomputes every historic SHA-1/SHA-256, checks every historic excerpt
byte-exactly, checks a canonical digest of the complete historic manifest, parses
Python literal scope objects with `ast`, compares checked JSON status/interface
and both scalar-scope objects, checks all four repaired prose boundaries,
and checks the two Lean files after stripping nested comments.

The Git pass gate never fetches and fails closed when a pinned object is
unavailable.  The canonical manifest digest makes every literal historic-pin
change fail even if another local commit resolves to the same blob.  Local Git
cannot authenticate GitHub's PR-number-to-head
metadata: it corroborates the integration message's PR number and the cited
head's exact content independently.  Reviewers must check that external
PR/head pairing separately with `gh`.

## Applied statement repair

This follow-up makes no theorem stronger and changes no numerical gate.

1. The #818/#820 producer notes and #827/#842 consumer notes now state the same
   open same-owner first-match, A4, A6/RC, and aggregate-census boundary.
2. The #866 audit status now says exactly that #824 prose was repaired there
   and that the four related notes required this follow-up.
3. The #824 and #820 verifiers/certificates now label their result as local
   scalar accounting and explicitly list the four interfaces they do not
   certify.
4. The #866 audit certificate now lists those same four unused inputs.
5. The #818/#820 producer prose and the #824/#820 Lean comments replace
   closed/paid-in-full promotions with exact local scalar-cap scope.  Their
   theorem declarations are unchanged.

## SHOULD — certificate and Lean reading

The source-bound audit pins the repaired artifacts themselves; a later edit to
any pinned note, verifier, JSON, or Lean source fails closed until independently
reviewed and repinned.  This is a correspondence/freshness guard, not a new
proof architecture.

The Lean packages remain arithmetic shadows.  The rank-one package proves
finite counts, digit pins, class arithmetic, and
`min pay cap <= cap`; the omega package proves decidable arithmetic pins.  Both
explicitly say that the analytic results live in the notes and Python
verifiers.  Neither formalizes the Walsh inequality as a real theorem or any
same-owner/source-to-cell/profile-payment implication.

## Consumers

- PR #818 head `03fa2958` and PR #820 head `d5f67b4b` remain valid producers of
  local scalar coefficient/cap arithmetic only.
- PR #824 head `2f5162fc` remains valid for T1--T5 at its stated scalar scope.
- PR #827 head `1512ff45` and PR #842 head `ea8318ff` may consume the local
  scalar machinery as candidate inputs, not as admission acceptance.
- PR #866 head `0b45db15` remains the governing type-boundary audit; this
  follow-up repairs its incomplete prose/source binding.

## Nonclaims

- This audit does not refute T1--T5, S1--S5, the Walsh identity, the omega cap,
  the rank-one product law, or any reported finite scan.
- It does not provide a source-valid counterexample to rank-one emission.
- It does not prove that the missing source-to-cell/profile-payment bridge is
  impossible.
- It does not add a grammar rule, a proof architecture, or formalization work.
- It edits no submission-facing paper and makes no lower-reserve claim.

## Reproducibility

```bash
python3 experimental/scripts/verify_rank_one_admission_prose_correspondence_audit.py
python3 -O experimental/scripts/verify_rank_one_admission_prose_correspondence_audit.py
# -> RESULT: PASS (368/368)
# -> STATUS: COUNTEREXAMPLE
python3 experimental/scripts/verify_rank_one_admission_prose_correspondence_audit.py --tamper-selftest
python3 -O experimental/scripts/verify_rank_one_admission_prose_correspondence_audit.py --tamper-selftest
# -> TAMPER SELFTEST: PASS (10/10 caught)
# -> STATUS: COUNTEREXAMPLE
```

The existing arithmetic replays remain independently required:

```bash
python3 experimental/scripts/verify_rank_one_admission_interface.py
# -> PASS: 46,644 universal Walsh checks over 6,662 exact cube functions
python3 experimental/scripts/verify_rank_one_greedy_adequacy.py
# -> RESULT: PASS (19/19)
python3 experimental/scripts/verify_omega_sound_emission_floor.py
# -> RESULT: PASS (12/12)
```
