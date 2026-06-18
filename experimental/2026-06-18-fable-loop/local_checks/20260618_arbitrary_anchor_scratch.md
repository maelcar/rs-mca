# 2026-06-18 Arbitrary-Anchor Scratch Scan

Status: EXPERIMENTAL / AUDIT_ONLY / NOT_BANKED.

Purpose: bounded Codex-side sanity check while Cycle 1 Opus 4.8 was running.

Target: balanced `t=sigma=2`, quadratic extension `F=F_{p^2}`, structured direction `g=-1/E` with `E=(X-alpha)(X-beta)`, and arbitrary anchors `f:D->F`.

This was an ad hoc Python heredoc, not a reusable verifier. The run was interrupted after the first `p=11` case became slow.

Observed scratch output:

```text
{'p': 5, 'n': 4, 'k': 1, 'sigma': 2, 'supports': 4, 'monic_slopes_inc': (0, 0), 'best_random_slopes_inc': (1, 4)}
{'p': 7, 'n': 6, 'k': 2, 'sigma': 2, 'supports': 15, 'monic_slopes_inc': (0, 0), 'best_random_slopes_inc': (4, 4)}
{'p': 7, 'n': 6, 'k': 3, 'sigma': 2, 'supports': 6, 'monic_slopes_inc': (0, 0), 'best_random_slopes_inc': (1, 1)}
{'p': 11, 'n': 10, 'k': 3, 'sigma': 2, 'supports': 252, 'monic_slopes_inc': (9, 9), 'best_random_slopes_inc': (10, 10)}
```

Interpretation: tiny arbitrary anchors can produce support-coefficient collinearities not visible in the chosen monic-anchor instance. This is not yet a counterpacket: the code was not saved as a verifier, noncontainment/field-ledger details need audit, and the cases are far below corrected reserve. It only supports the prompt design: the arbitrary-anchor gap is real and should not be waved away by the monic `hat E` reduction.
