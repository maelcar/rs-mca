# Experiment Run - 2026-06-26

Status: AUDIT / EXPERIMENTAL RUN.

This run follows the strict264 and finite-row plan: check the existing
Cycle116/119 obstruction, run strict264 one script at a time, then run the
theorem-infrastructure validators that support the next proof attempts.

Machine-readable run data is in
`experimental/data/experiment-run-2026-06-26.json`.

## Outcome

No new prize-worthy frontier point was produced.  Do not change
`site/data/frontier.json`.

The current row remains:

```text
C = RS[F_17^32,H,256], |H|=512, N_bad=52,747,567,092.
```

The validators confirm the known gate:

```text
floor(17^32 / 2^128) = 6,
```

so seven retained slopes are enough at any listed agreement target over this
line field.  The strict264 target remains exactly:

```text
agreement = 264, sigma = 8, delta = 31/64, need N_bad >= 7.
```

## Scripts Run

### Current finite row

- `verify_m1_cycle120_standalone_ldsw_proof.py --json`: PASS.
  Confirms the source-conditional statement
  `LD_sw(RS[F_17^32,H,256],262) >= 52,747,567,092`.
- `verify_audit_pr100_cycle120_gate.py --json`: PASS.
  Confirms `N/17^32` is about `2^-95.18`, and records the unverified imports:
  Cycle84 count, fixed-jet transfers, ABF wording, and generator/domain
  certificate.

### Strict264 and reserve ladder

- `verify_m1_strict264_admissibility.py --json`: PASS.
- `verify_m1_strict264_bridge.py --json`: PASS.
- `verify_m1_strict264_mechanism.py --json`: PASS.
- `verify_m1_strict264_two_ended_transfer.py --json`: PASS.
- `verify_m1_strict264_end_to_end.py --json`: PASS.
- `verify_m1_reserve_scale_bridge.py --json`: PASS.
- `verify_m1_reserve_scale_richness.py --json`: PASS.

These scripts validate the endpoint arithmetic, the corrected fixed-jet
condition, the toy transfer mechanism, and the reserve-ladder bookkeeping.
They do not produce the seven actual retained slopes for the `F_17^32` row.

The most important strict264 lesson is that the valid two-ended transfer fixes
the top `sigma-1` coefficients plus the endpoint.  The literal top
`sigma-2` plus endpoint reading fails in the top parity row.

### Theory infrastructure

- `verify_f1_syndrome_pencil_normal_form.py --json`: PASS.
- `verify_l2_codegree_decomposition.py --json`: PASS.
- `verify_l2_reduction_bound.py --json`: PASS.
- `verify_l2_mu_recursion.py --json`: PASS.
- `verify_l2_profile_decay.py --json`: PASS.
- `verify_l2_punctured_johnson.py --json`: PASS.
- `verify_l2_stratified_sum.py --json`: PASS.
- `verify_a0_deep_point_cap_algebra.py --json`: PASS.
- `verify_m2_common_code_line_residual_budget.py`: PASS.

The L2 profile-decay run reinforces the current caveat: generic/random tails
decay in the sampled cases, but quotient-periodic mass can persist, so quotient
exceptions must be split before any saving claim.

## Next Experiments

1. Produce the strict264 seven-slope certificate:
   `(gamma, J_gamma, S_gamma, P_gamma, rank/noncontainment proof)` for seven
   distinct retained slopes at agreement 264.
2. Produce an independent replayable certificate for the existing
   `52,747,567,092` count and Cycle116/119 transfer.
3. Start the threshold-pinning side: test whether `LD_sw(C,265) <= 6`, or find
   the next obstruction, using the syndrome-pencil normal form.
