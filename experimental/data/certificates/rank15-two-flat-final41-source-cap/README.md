# Rank-15 exact two-flat final-41 source-cap certificate

This standard-library packet replays the exact integer certificate used by

```text
experimental/notes/l2/rank15_two_flat_final41_source_cap.md
```

It proves only the 41 source-child replacements

```text
D_2(u) <= 211 for u=1,043,917..1,043,957.
```

The immediate unclosed state is `u=1,043,916`, with relaxed margin `+878`.

Run the theorem replay and tamper suite with any suitable Python 3 runtime:

```bash
python3 verify_rank15_two_flat_final41_source_cap.py
python3 -O verify_rank15_two_flat_final41_source_cap.py
python3 verify_rank15_two_flat_final41_source_cap.py --tamper-selftest
```

The verifier uses explicit exceptions rather than `assert`, rejects duplicate
keys, unknown fields, non-integer numeric fields, booleans in integer fields,
and non-finite JSON constants, and checks its frozen certificate, outputs, and
manifest.  `SHA256SUMS.txt` covers every packet file except the manifest itself.

The external return's C++ source was inspected but was not compiled because
Apple developer tools were unavailable.  The Python verifier independently
replays its three theorem-relevant local knapsacks, exact layer optimizer,
boundary, and all 41 printed margins.  The extra next-wall cut that the return
marked as unused is not part of this packet.

No parent recurrence, 366-child closure, arrangement transport, rank-16
result, Grand List/MCA theorem, or score movement is claimed.
