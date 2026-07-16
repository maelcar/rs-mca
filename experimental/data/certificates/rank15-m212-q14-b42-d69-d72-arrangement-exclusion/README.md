# Rank-15 conditional `D=69..72` arrangement certificate

This packet supports

```text
experimental/notes/l2/rank15_m212_q14_b42_d69_d72_arrangement_exclusion.md
```

The standard-library verifier reconstructs the `D=69..73` moment profiles,
descending-prefix filter, terminal rows, field divisor arithmetic, numerical
Kneser bounds, PBD equations, and the surviving `D=73` direction spectrum.
It deliberately does not machine-prove the geometric matching, coordinate,
Cauchy--Davenport, Kneser-application, PBD-construction, or duality lemmas.
Those proofs are written in the theorem note.

Run from the repository root:

```bash
python3 experimental/scripts/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.py \
  > /tmp/rank15_d69_d73.normal.out
cmp /tmp/rank15_d69_d73.normal.out \
  experimental/data/certificates/rank15-m212-q14-b42-d69-d72-arrangement-exclusion/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.expected.txt

python3 -O experimental/scripts/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.py \
  > /tmp/rank15_d69_d73.opt.out
cmp /tmp/rank15_d69_d73.normal.out /tmp/rank15_d69_d73.opt.out

python3 experimental/scripts/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.py \
  --tamper-selftest

cd experimental/data/certificates/rank15-m212-q14-b42-d69-d72-arrangement-exclusion
shasum -a 256 -c SHA256SUMS.txt
```

`SHA256SUMS.txt` binds the theorem note, verifier, this README, and frozen
stdout.  The theorem is field-specific and conditional on the exact 42-line
arrangement interface.  It transports no rank-15 child, removes no recurrence
parent, and makes no Grand List, Grand MCA, asymptotic, all-prime, or official
score claim.
