# Rank-16 global `c=0` first-match ledger certificate

This directory contains the canonical residual-profile census and expected
stdout for the standard-library verifier
`experimental/scripts/verify_rank16_global_c0_ledger.py`.

The verifier checks exact finite arithmetic and certificate obligations.  The
proof that the three producer inequalities apply to one arbitrary received word
is in `experimental/notes/l2/rank16_global_c0_first_match_ledger.md`.

Run from the repository root:

```bash
python3 experimental/scripts/verify_rank16_global_c0_ledger.py \
  > /tmp/rank16_global_c0_ledger.out
cmp /tmp/rank16_global_c0_ledger.out \
  experimental/data/certificates/rank16-global-c0-first-match-ledger/verify_rank16_global_c0_ledger.expected.txt

python3 -O experimental/scripts/verify_rank16_global_c0_ledger.py \
  > /tmp/rank16_global_c0_ledger.opt.out
cmp /tmp/rank16_global_c0_ledger.out \
  /tmp/rank16_global_c0_ledger.opt.out

python3 experimental/scripts/verify_rank16_global_c0_ledger.py \
  --tamper-selftest

python3 experimental/scripts/verify_rank16_global_c0_ledger.py \
  --write-profiles /tmp/rank16_global_c0_residual_profiles.csv \
  > /tmp/rank16_global_c0_ledger.profiles.out
cmp /tmp/rank16_global_c0_residual_profiles.csv \
  experimental/data/certificates/rank16-global-c0-first-match-ledger/rank16_global_c0_residual_profiles.csv
```

The optional `--archive-root PATH` mode additionally verifies every byte in
the originating role archive's `source/` tree against its manifest.  It adds
one provenance line to stdout and is intentionally not required for the
standalone repository replay.

`SHA256SUMS` binds the verifier, canonical expected output, and profile CSV.
