# Rank-15 conditional arrangement certificate packet

This packet supports

```text
experimental/notes/l2/rank15_m212_q14_b42_uniform_geometric_transport.md
```

It excludes `D=66,67,68,146` under the conditional rank-15 `M=212`, `q=14`,
`B=42`, `R=211` arrangement interface. It does not prove that the literal
source or any child interval reaches that interface.

The `work/` directory contains:

- the exact 4,387-certificate JSON;
- a standard-library Python verifier;
- frozen canonical output; and
- the hostile audit recording the repaired `D=68` concurrency lemma.

Run:

```text
cd experimental/data/certificates/rank15-m212-q14-b42-uniform-geometric-transport/work
python3 verify_rank15_uniform_geometric_transport.py
python3 -O verify_rank15_uniform_geometric_transport.py
```

Both runs must match `verify_rank15_uniform_geometric_transport.expected.txt`
byte for byte.

Conditionally on the arrangement interface and pending #804, the remaining
wall is `69<=D<=145`. The packet transports no child state, removes zero
recurrence parents, and makes no rank-16, Grand List, Grand MCA, deployed
adjacent-certificate, or official-score claim.
