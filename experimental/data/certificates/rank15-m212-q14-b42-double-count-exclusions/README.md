# Rank-15 `M=212`, `q=14`, `B=42` certificate packet

This packet supports

```text
experimental/notes/l2/rank15_m212_q14_b42_double_count_exclusions.md
```

The `work/` directory contains seven full proof notes, seven claimant verifiers,
seven frozen claimant outputs, seven independent hostile verifiers, seven frozen
hostile outputs, and seven hostile audit reports. Three source-interface files
and the exact packing replays are included because the hostile verifiers pin
them by SHA-256. The `source/` directory preserves the literal locator normal
form at the source commit.

Run all finite replays from this directory:

```bash
cd experimental/data/certificates/rank15-m212-q14-b42-double-count-exclusions/work
for f in verify_rank15_m212_q14_b42_*.rb \
         audit_rank15_m212_q14_b42_*.rb; do
  ruby --disable-gems -W0 "$f"
done
python3 verify_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.py
python3 -O verify_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.py
```

Every script is standard-library only. No downloaded binary or dependency is
required. `SHA256SUMS.txt` covers every preserved input and expected output.

The source pin is

```text
origin/main@2633895a66d3edf516120a87b2eb18c994f977ab
```

The packet pays `D=39` and `D=44..65` under the hypotheses in the theorem
note. It makes no recurrence or official-score claim.
