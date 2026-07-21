# D128 quartic-line dichotomy certificate

**Author:** Manuel E. Rey-Álvarez Zafiria

`primary_output.json` records the full line census.  The independent source
reconstructs the domain and uses separate filters and key recovery;
`independent_output.json` records its result.

From the repository root:

```text
g++ -O3 -std=c++20 experimental/scripts/verify_d128_quartic_line_dichotomy.cpp -o quartic_lines
./quartic_lines --full
g++ -O3 -std=c++20 experimental/scripts/audit_d128_quartic_line_dichotomy.cpp -o quartic_lines_audit
./quartic_lines_audit experimental/data/certificates/d128-quartic-line-dichotomy/independent_output.json
```

The full replay is CPU and memory intensive.  `SHA256SUMS.txt` authenticates
both implementations, the note, and the recorded outputs.
