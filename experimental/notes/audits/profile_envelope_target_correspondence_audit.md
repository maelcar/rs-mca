# Audit: profile-envelope target correspondence

**STATUS:** `COUNTEREXAMPLE`

The integrated packet preserves useful exact finite-field arithmetic, but its
universal prime-field identity-dominance, complete-envelope, exact-`(FI)`,
certificate, and unsafe-target claims exceeded what its verifier checked.  The
smallest repair is to retain the selected power-profile census, record exact
counterexamples, bind its certificate to its sources, narrow the Lean shadow,
and correct one same-wave motivational consumer.  No submission-facing file is
changed.

## Immutable audit subject

The audited upstream base is `c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.
Integration `2633895a66d3edf516120a87b2eb18c994f977ab` imported PR #759
head `8cd4f4b671ba6a3f15042317c7149640aada2e19`.  The following blobs are
byte-identical at that PR head, the integration, and the audited base:

| Path | Git blob |
|---|---|
| `experimental/notes/thresholds/profile_envelope_target_comparison.md` | `436f5c95` |
| `experimental/scripts/verify_profile_envelope_target_comparison.py` | `81ac80d0` |
| `experimental/data/certificates/profile-envelope-target-comparison/cert.json` | `f1734d43` |
| `experimental/lean/profile_envelope_target_comparison/ProfileEnvelopeTargetComparison.lean` | `4cb72278` |

PR #760 head `dabf6510` was imported in the same integration wave.  Its
motivational note/script/Lean blobs at the audited base are respectively
`32ec0604`, `ef6b1186`, and `45c71955`.

The source interfaces used for correspondence checks are
`experimental/asymptotic_rs_mca_frontiers.tex` @ `466b35c5`,
`experimental/notes/thresholds/profile_envelope_completeness.md` @
`6f56feca`, and
`experimental/notes/thresholds/envelope_identity_window.md` @ `0e296a5d`.

## Findings

### MUST-1 — the exact prime-field identity-dominance claim is false

The integrated note says that prime base plus identity `(FI)` makes the
identity term dominate the entire envelope
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:36-40,57-62,243-255,300-308 @ 436f5c95`).
The verifier instead accepts a selected cell when it is dominated by either
the identity **or the separate deep term**, then prints “WHOLE envelope” and
“identity dominates”
(`experimental/scripts/verify_profile_envelope_target_comparison.py:424-446,622-650 @ 81ac80d0`).
Two independent exact boundaries refute the literal claim:

1. On the packet's own `D=F_13^x,n=12,a=6,k=3,w=2` row, the identity
   average is `924/169`, while the selected `c=3,r=0` cell has
   `|Omega|=6,L=1`, hence
   `6*169=1014>924`.  It is bounded by the separate deep term `7`; that
   does not make it identity-dominated.
2. On `D=F_19^x,n=18,a=8,k=4,w=3`, the identity image fills the exact
   codomain: `|Omega_id|=43758,L_id=6859=19^3`.  The `c=2,r=0` cell has
   `|Omega|=126,L=19`, and
   `126*6859=864234>831402=43758*19`.  Thus there is no subfield drop and
   no identity-image deficit, yet literal finite `(ID)` fails.

There is also an exact family:
`D=F_p^x,n=p-1,a=p-3,k=p-5,w=1`, for which
`barN_id=(p-1)(p-2)/(2p)`, `barN_c=2=(p-1)/2`, and the deep term is
`3`.  The square beats the identity for every odd `p`, and beats the
deep term for `p>=11`.  These finite counterexamples do not refute an
asymptotic exponent statement that absorbs polynomial factors.  The repaired
producer records all three boundaries
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:97-153`).

### MUST-2 — “complete envelope” did not correspond to the enumerated object

The integrated note claims exact enumeration of every envelope term
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:1-12,29-35,138-156 @ 436f5c95`).
The executable's complete-census routine enumerates only the identity slice
and complete power-fiber quotient/remainder slices
(`experimental/scripts/verify_profile_envelope_target_comparison.py:357-420 @ 81ac80d0`).
It does not enumerate received lines, first-match admission, Chebyshev cells,
planted cells, arbitrary partial occupancy, balanced cores, or residual
profiles.

That omission is material.  The source object is a supremum over received
lines and a sum over nonempty realized first-match cells
(`experimental/asymptotic_rs_mca_frontiers.tex:843-862 @ 466b35c5`);
first-match ownership is defined at
`experimental/asymptotic_rs_mca_frontiers.tex:1452-1472 @ 466b35c5`.
The verifier's raw support families can overlap and are not a
witness-exhaustive ownership partition.  The source itself says that this
overlap requires first-match assignment
(`experimental/asymptotic_rs_mca_frontiers.tex:7125 @ 466b35c5`).
Its structural wrapper also leaves partial-occupancy and balanced-core upper
payments conditional
(`experimental/notes/thresholds/profile_envelope_completeness.md:145-172,248-261 @ 6f56feca`).

The advertised selected inventory was not internally complete either.  The
integrated note calls `c=2,r=0` the sole tower cell exceeding the formal
identity proxy
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:202-209 @ 436f5c95`).
At `GF(49)`, all four selected cells exceed `924/2401`:
`20/7,6,14/11,2`; the `c=3` cell is the leader.  At `GF(121)`, the
full selected power inventory is
`(c,r,|Omega|,L)=(2,0,252,11),(4,2,660,190),(5,0,6,1),(10,0,2,1)`.
The repair therefore calls this a selected power-profile census, not a
complete source envelope
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:155-193`).

### MUST-3 — the target conclusion reversed a one-way implication

The integrated packet reports `E_identity=26`, `E_complete=50`, and calls
the row “unsafe”
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:149-156,229-237 @ 436f5c95`;
`experimental/scripts/verify_profile_envelope_target_comparison.py:593-619,708-709 @ 81ac80d0`).
But the executable merely tests whether a proposed upper budget is at most
`B*=26`.  Its lower-reserve function `P_reserve` is defined but never
called
(`experimental/scripts/verify_profile_envelope_target_comparison.py:303-316,675-721 @ 81ac80d0`).
The source safe-side lemma is sufficient and one-way
(`experimental/asymptotic_rs_mca_frontiers.tex:6154-6161 @ 466b35c5`):
failure of `E<=B*` means “not certified safe,” not “unsafe.”

Moreover, `50` contains only the formal identity and square proxies.  Under
the verifier's own selected raw-family sum, the formal and realized totals are
`65` and `191`, respectively; neither equals the source envelope without
received-line co-realization and first-match ownership.  The repair makes only
the safe statement that the selected realized test does not certify safety at
`26`, and claims no lower reserve or threshold move
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:211-235`).

### MUST-4 — exact non-surjectivity was mislabeled as asymptotic `(FI)` failure

The integrated packet calls `L_id=1331=11^3<11^4` a failure of `(FI)`
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:47-52,211-227,268-278 @ 436f5c95`).
Yet the same note states the source hypothesis as
`L_id>=e^{-o(n)}|B|^w`
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:158-162 @ 436f5c95`).
A factor-`11` deficit at one finite row proves exact non-surjectivity, not
failure of that asymptotic lower bound.

The generic control was also truncated after the first `60000` of
`184756` supports, but was labeled “fills” / “does NOT collapse”
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:215-227 @ 436f5c95`;
`experimental/scripts/verify_profile_envelope_target_comparison.py:571-590 @ 81ac80d0`;
`experimental/data/certificates/profile-envelope-target-comparison/cert.json:58-63 @ f1734d43`).
Completing the same deterministic census gives
`L_id=9359<14641`, with maximum fiber `57`.  It is larger than the
smooth-coset image `1331`, but still not full.  The repair labels both rows
as exact full-codomain measurements and leaves asymptotic `(FI)` undecided
(`experimental/notes/thresholds/profile_envelope_target_comparison.md:195-209`).

### MUST-5 — the JSON was neither fresh nor consumed as a certificate

The integrated JSON asserts the universal decision and unsafe target
(`experimental/data/certificates/profile-envelope-target-comparison/cert.json:10-15,17-75 @ f1734d43`),
but contains no payload hash or source manifest.  The producer never reads it;
its `main` runs the arithmetic directly
(`experimental/scripts/verify_profile_envelope_target_comparison.py:675-721 @ 81ac80d0`).
The single tamper test changes one expected integer, and unknown options are
silently accepted
(`experimental/scripts/verify_profile_envelope_target_comparison.py:660-677 @ 81ac80d0`).

The repaired certificate has SHA-256
`452f2fdc8ee5d98153f7afffce33b3cddcdf05ada422b9d504daa423198ba408`
and uses canonical payload hash
`66902d6057db838fd3044b85ec9b829005dbae75e3011b5c8f27a735cbcf98ef`
plus SHA-256 source bindings for the note, producer, Lean source, completeness
source, identity-window source, and frontiers source. The repaired producer validates
the schema, semantics, rows, payload, and every binding; it rejects three
independent mutations under normal and optimized Python and fails closed on
unknown arguments
(`experimental/scripts/verify_profile_envelope_target_comparison.py:743-909`;
`experimental/notes/thresholds/profile_envelope_target_comparison.md:237-245,271-284`).

### MUST-6 — Lean compiled, but did not formalize the promoted claims

The integrated Lean file consists of fixed `Nat` binomial equalities and
cross-products.  Its own header says the universal real-entropy implication is
not in Lean
(`experimental/lean/profile_envelope_target_comparison/ProfileEnvelopeTargetComparison.lean:13-25 @ 4cb72278`).
The theorem named `tower121_identity_FI_fails` proves only
`1331<11^4`; it does not state asymptotic `(FI)`
(`experimental/lean/profile_envelope_target_comparison/ProfileEnvelopeTargetComparison.lean:89-100 @ 4cb72278`).
Direct compilation succeeds with no `sorry`, `admit`, or custom axiom
declaration; representative `native_decide` theorems report only
`Lean.ofReduceBool`.  Thus Lean arithmetic is clean, but it supplied no
formal support for the universal, complete-envelope, first-match, certificate,
or target claims.

The minimal Lean repair narrows the header and renames the finite measurement
to `tower121_identity_full_codomain_deficit`
(`experimental/lean/profile_envelope_target_comparison/ProfileEnvelopeTargetComparison.lean:13-19,82-94`).
No new theorem architecture is introduced.

### SHOULD-1 — correct the same-wave motivational consumer

PR #760 says PR #759 is open and its motivation is conditional
(`experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md:128-134,396-398,424-427 @ 32ec0604`;
`experimental/scripts/verify_nonfiber_decomposition_realized_scale.py:16-17,64-70 @ ef6b1186`;
`experimental/lean/nonfiber_decomposition_realized_scale/NonfiberDecompositionRealizedScale.lean:7-11 @ 45c71955`).
Both were integrated by `2633895a`.  Only this status/scope prose needs
repair: the exact finite full-codomain deficit is motivational, not an
asymptotic `(FI)` theorem, and #760's proof is independent of it.

### NOTE-1 — what remains valid

The original producer replays `RESULT: PASS (71/71)` under both normal and
optimized Python.  Its selected finite census and the tower inequalities
`20*2401>924*7` and `252*14641>184756*11` are arithmetically correct.
Neither tower row beats the **realized** identity average; each beats only the
formal ambient proxy.  The repaired producer retains those facts, adds the
negative controls and complete generic census, and reports
`RESULT: PASS (89/89)`, `STATUS: COUNTEREXAMPLE`.

This status is limited to the integrated packet's exact universal,
correspondence, certificate, and target claims.  It does not refute the
source's asymptotic per-folding window, prove a new threshold, close
`(PEU)`/`(RC)`, or alter the current v9.2 submission package.

## Producer and consumer interlocks

- PR #520 head `73525004`: envelope formula and finite brackets only.
- PR #524 head `5fe12fba`: records the complete comparison as open.
- PR #542 head `dcda4e9f`: sufficient identity-window source, not a
  universal finite identity theorem.
- PR #606 head `96dc5370`: per-folding window repair.
- PR #688 head `48b6487d`: structural wrapper; nontrivial upper directions
  retain `(PEU)`/`(RC)` hypotheses.
- PR #713 head `d78ea57e` and PR #714 head `1df8a072`: adjacent residual
  ledgers, neither closed here.
- PR #759 head `8cd4f4b6`: audited producer.
- PR #760 head `dabf6510`: same-wave motivational consumer; theorem
  independent of #759.
- PR #922 head `c81af250`: adjacent integrated-material audit packet; no
  direct claim or file overlap.

## Deterministic replay

From the repository root:

```bash
python3 experimental/scripts/verify_profile_envelope_target_correspondence_audit.py
# -> RESULT: PASS (21/21)
# -> STATUS: COUNTEREXAMPLE
python3 -O experimental/scripts/verify_profile_envelope_target_correspondence_audit.py
# -> identical result

python3 experimental/scripts/verify_profile_envelope_target_comparison.py
# -> RESULT: PASS (89/89)
# -> STATUS: COUNTEREXAMPLE
python3 -O experimental/scripts/verify_profile_envelope_target_comparison.py
# -> identical result
python3 experimental/scripts/verify_profile_envelope_target_comparison.py --tamper-selftest
# -> RESULT: PASS (tamper-selftest)
# -> tamper_mutations_rejected=3/3
python3 -O experimental/scripts/verify_profile_envelope_target_comparison.py --tamper-selftest
# -> identical result

cd experimental/lean/profile_envelope_target_comparison
lake env lean ProfileEnvelopeTargetComparison.lean
# -> exit 0
```

The audit verifier independently recomputes the GF(13), GF(19), prime-family,
GF(49), and GF(121) cross-products; completes the generic GF(121) census;
checks original immutable blob pins; validates the repaired certificate and
source bindings; replays producer normal/optimized/tamper/unknown-argument
modes; and checks the narrowed Lean and #760 consumer surfaces.
