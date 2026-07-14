# Prefix/Staircase Extremality Certificates

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** COUNTEREXAMPLE / REPAIRED THEOREM

Run from the repository root:

```text
python experimental/scripts/verify_prefix_staircase_extremality_counterexamples.py
python experimental/scripts/verify_rs_incidence_envelopes.py
```

The first verifier exhausts all received words in the `F_7` affine case and
checks the multiplicative `F_23` construction exactly. It regenerates
`prefix_staircase_counterexamples.json`.

The second verifier checks the repaired list and MCA incidence envelopes on
both examples and performs the exact active-row budget arithmetic. It
regenerates `repaired_incidence_envelopes.json`.

Both scripts use only the Python standard library. They terminate with a
`PASS_WITH_...` verdict or raise an exception on the first failed invariant.
