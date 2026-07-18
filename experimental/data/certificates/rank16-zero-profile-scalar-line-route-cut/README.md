# Rank-16 zero-profile scalar-line route-cut certificate

This packet certifies the deterministic count compiler for the deployed-field
finite theorem in
`experimental/notes/l2/rank16_zero_profile_scalar_line_route_cut.md`.

Run from the repository root:

```bash
python3 experimental/scripts/verify_rank16_zero_profile_scalar_line_route_cut.py
python3 -O experimental/scripts/verify_rank16_zero_profile_scalar_line_route_cut.py
python3 experimental/scripts/verify_rank16_zero_profile_scalar_line_route_cut.py \
  --self-test-mutations
```

Both ordinary and optimized output must match
`verify_rank16_zero_profile_scalar_line_route_cut.expected.txt` exactly. The
mutation self-test must reject all nine changes.

The verifier uses only the Python standard library. It checks the deployed
field and subgroup orders, the scalar-line cap, all 2,607 exact delta cells,
the deterministic integral transports, the 15 line totals, the nonlinear
companion total, the zero complete-block profiles, the stated endpoint
fingerprints, and the zero charge of the current complete-block deletion
interface.

The independent hostile audit accepted only this finite route cut. It did not
accept an actual owner deficit, add-back, parent inequality, recurrence,
Grand List, Grand MCA, or official-score claim.
