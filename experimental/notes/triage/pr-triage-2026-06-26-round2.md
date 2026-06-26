# PR Triage 2026-06-26 Round 2

Status: AUDIT / INTEGRATION.

This note covers the two open Scott Hughes PRs reviewed after the strict352
frontier update:

- PR #120, `L1: add odd-moment Hooley-Katz audit`.
- PR #121, `L1: add proper-subgroup cubic twisted collision bound`.

Both PRs are L1/local-limit material.  Neither supplies a new Proximity Prize
rate row, bad-slope numerator, agreement endpoint, or leaderboard entry.

## PR #120

Integrated files:

- `experimental/notes/l1/l1_prefix_dual_odd_moment_projective_geometry.md`
- `experimental/notes/triage/l1-prefix-dual-odd-moment-hooley-katz-import-audit-2026-06-26.md`
- `experimental/scripts/verify_l1_prefix_dual_odd_moment_hooley_katz_audit.py`

Verdict: useful audit / route cut.

The note proves the projective odd-moment collision geometry for `k>d` and
records the affine-cone conversion and Hooley--Katz/Ghorpade--Lachaud constant
substitution.  The important negative information is that the current generic
full-affine point-count route does not yet give a reserve-scale generated-field
local limit: the MPP field-size condition fails on the tested polynomial-field
grid, and the unrestricted GL lower-weight term is too expensive in many rows.

This is not a subgroup theorem and not a leaderboard update.

## PR #121

Integrated files:

- `experimental/notes/l1/l1_prefix_dual_d2_cubic_subgroup_twisted_bound.md`
- `experimental/notes/triage/l1-prefix-dual-d2-cubic-subgroup-twisted-bound-import-audit-2026-06-26.md`
- `experimental/scripts/verify_l1_prefix_dual_d2_cubic_subgroup_twisted_bound.py`

Verdict: useful theorem/audit for L1.

The note addresses the actual proper-subgroup `H^{2k}` cubic collision object,
not the full-affine proxy.  After expanding `1_H` into multiplicative
characters, it imports standard one-variable Gauss and Kummer--Artin--Schreier
sum bounds and obtains

```text
0 <= V_{H,k}/n^{2k} - 1/p^2
   <= (p-1)/p^2 * (sqrt(p)/n)^{2k}
      + (p-1)/p * (3 sqrt(p)/n)^{2k}.
```

In particular, the error decays exponentially in `k` once

```text
n > (3+epsilon) sqrt(p).
```

This is useful because it cleanly separates proper-subgroup collision counting
from full-affine Hooley--Katz geometry and gives a review-sized template for
higher odd moments.  It remains a `d=2` cubic theorem with imported
one-variable character-sum input, not a general L1 local-limit theorem.

## Site Decision

Both PRs were added to the public updates feed.  They were not added to
`site/data/rate-leaderboards.json`, because the rate leaderboard is reserved
for rows with explicit `rho`, `delta`, field denominator, endpoint convention,
and certified retained mass.

## Next Checks

1. Pin the exact Katz/Gauss source theorem and constant used in PR #121.
2. Decide whether the `d=2` subgroup method extends to higher odd moments
   without losing the reserve-scale exponent.
3. Keep PR #120 as a warning against promoting full-affine point-count audits
   into subgroup or torus statements without twisted character control.
