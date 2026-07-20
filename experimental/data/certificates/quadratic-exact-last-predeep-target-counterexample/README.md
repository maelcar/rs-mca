# Quadratic-exact last-predeep target counterexample certificate

This certificate binds the independently audited R33 Role 12 theorem to the
current source files and its deterministic standard-library replay.

Run:

```bash
python3 experimental/scripts/verify_quadratic_exact_last_predeep_target_counterexample.py
python3 -O experimental/scripts/verify_quadratic_exact_last_predeep_target_counterexample.py
```

Both outputs must match
`verify_quadratic_exact_last_predeep_target_counterexample.expected.txt`.
The object is a zero-payment necessary route cut. It is not a replacement O5c
exclusion and does not change the official `0/2` score.
