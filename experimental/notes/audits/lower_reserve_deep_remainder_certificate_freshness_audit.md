# Audit: lower-reserve deep-remainder certificate freshness

**STATUS:** `COUNTEREXAMPLE`

**Audited integration:** `06b2a6fb`, including PR #869 head `0c8023fa`.
The same bytes remained on `upstream/main` through `c4856fa6`.

## Verdict

The QR4/QR5 window repair and the strict-deep `F_169` mathematical
counterexample replay clean. The certificate-verification claim did not:
`experimental/scripts/verify_lower_reserve_deep_remainder.py --check`
recomputed and unconditionally overwrote the frozen certificate before
returning `RESULT: PASS 44/44`. Thus the advertised check accepted stale or
tampered repository data and erased the evidence.

This is a certificate-freshness and source-to-verifier defect, not a
counterexample to the corrected deep-remainder theorem.

## MUST finding and deterministic witness

- **MUST — `experimental/scripts/verify_lower_reserve_deep_remainder.py:49-54,608-625 @ 06b2a6fb`:**
  the docstring calls default/`--check` a verifier mode, while the dispatcher
  calls `write_certificate(results)` without first reading the frozen JSON.
  The source note makes the same verifier claim at
  `experimental/notes/thresholds/lower_reserve_deep_remainder_atlas.md:53-60 @ 06b2a6fb`.
- The integrated verifier SHA-256 was
  `3878e1d373fda23a30019b44621800bf011efe9a75b7de35eedc62aadfa13834`.
  The frozen certificate SHA-256 was
  `e9815f14e0be85c5b5489d98a944392cbcc997389eed10d2dd05e6860c507016`.
- In an isolated copy, changing
  `key_numbers.guaranteed_list_strict_deep_F169` from `6` to `7` produced
  SHA-256
  `cec46fea6988b0a2d868fe208712e9759174d04dd074b2bafba904ee6a50ad7d`.
  The exact advertised `python3 ... --check` command returned
  `RESULT: PASS 44/44`, rewrote the file, and restored SHA-256
  `e9815f14...`. Optimized Python behaved identically.

## Mathematical and scope audit

The statement windows are kept separate:

- QR4 is used only for `0 <= r < c`; its bounded deep window is
  `w < r < c`.
- Arbitrary remainders `r >= c` use QR5. The no-clean-coordinate statement
  is a coordinate route cut, not a Cartesian-image theorem.
- The #714 strict-deep witness independently replays with labels `7920`,
  supports `554400`, analytic image bound `102960`, realized image
  `86320`, maximum fiber `20`, guaranteed list `6`, and identity floor
  `1`.

The companion verifier passes under normal and optimized Python. PR #869 has
no Lean module, so there is no Lean proof claim to promote or replay here.
Neither O7, a general natural-scale payment, a deployed threshold, nor a paper
theorem is changed.

## Repair

The target verifier now constructs the certificate in memory and has three
disjoint modes:

- `--check` recomputes all 44 gates, byte-compares the required frozen JSON,
  and never writes;
- `--write` is the only certificate-regeneration mode; and
- `--tamper-selftest` retains the 10 mathematical negative controls.

The source note now states that contract. The audit verifier pins the repaired
note, target verifier, certificate, companion verifier, two downstream notes,
and paper source. It independently checks clean normal/`-O` replay, proves a
tampered certificate is rejected without mutation, proves missing data is
rejected, and proves only explicit `--write` restores the canonical bytes.

## Producer and consumer interlocks

- #693 head `5de8e86a`: O5c/O7 coverage.
- #699 head `1909e737`: QR4 quotient/Euclidean/Chebyshev payment and wall.
- #712 head `222c1e14`: retired false field-drop-dead theorem.
- #714 head `1df8a072`: correcting label-factored theorem and exact witness.
- #727 head `c6d09aed`: post-sweep reconciliation consumer.
- #736 head `97e2713f`: pay-per-bit audit consumer.
- #869 head `0c8023fa`: integrated producer repaired by this packet.
- #882 head `af213091`: adjacent atlas-interface work; it does not touch the
  repaired files.

Credit for the label-factored theorem and `F_169` witness remains with
DannyExperiments, PR #714.

## Replay

```bash
python3 experimental/scripts/verify_lower_reserve_deep_remainder_certificate_freshness_audit.py
python3 -O experimental/scripts/verify_lower_reserve_deep_remainder_certificate_freshness_audit.py
python3 experimental/scripts/verify_lower_reserve_deep_remainder.py --check
python3 -O experimental/scripts/verify_lower_reserve_deep_remainder.py --check
python3 experimental/scripts/verify_lower_reserve_deep_remainder.py --tamper-selftest
python3 -O experimental/scripts/verify_lower_reserve_deep_remainder.py --tamper-selftest
python3 experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --check
python3 -O experimental/scripts/verify_deep_remainder_partial_occupancy_counterexample.py --check
```

Expected audit result:

```text
RESULT: PASS (12/12)
STATUS: COUNTEREXAMPLE
```
