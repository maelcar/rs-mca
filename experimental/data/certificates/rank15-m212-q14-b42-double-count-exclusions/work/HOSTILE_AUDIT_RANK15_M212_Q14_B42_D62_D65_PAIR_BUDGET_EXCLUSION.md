# Hostile audit: rank-15 `D=62..65` pair-budget exclusion

## Verdict

```text
PASS
```

## Scope audit

The claim is conditional on the already integrated source interface: 42
distinct projective lines, 211 reduced arrangement intersections, 15 distinct
intersections on each line, and multiplicity at most 15. The finite proof does
not derive those hypotheses. It applies to both printed aggregate rows only
because the existing source transport gives the same arrangement interface
for both.

## Proof audit

The following load-bearing steps were checked independently.

1. The three global moments are exact; the bounded `c_1,...,c_12` system is
   equivalent to those moments and `n_3>=0`.
2. The line equations `d_L=S_L-11` and `t_L=26-S_L-s_L` follow from the two
   exact per-line counts.
3. At a selected high point, any other point lies on at most one selected
   line, so the required auxiliary groups are disjoint. Enumerating minimal
   group multisets is exhaustive.
4. A line contains at most two heavy points. The bounds on `x_0` and on pairs
   of no-heavy lines use inequalities in the conservative direction.
5. In the subset-pair lemma, two selected projective points determine at most
   one arrangement line. Balancing the 42 line occupancies gives the minimum,
   not the maximum, of the convex pair count.
6. Every one of the 13 `D=65` terminal profiles has an explicit strict
   subset-pair violation.

## Replay audit

The Python verifier assigns high weights in descending order. The independent
Ruby verifier assigns them in ascending order and reconstructs its own minimal
packing groups, heavy-line ledger, and terminal prefixes. It does not import
the Python implementation.

Both normal and optimized Python executions reproduce the frozen output. The
Ruby audit independently reports:

```text
profile_counts=62:1825,63:2172,64:2573,65:3103
packing_survivors=62:26,63:41,64:51,65:138
negative_zmax=62:10,63:12,64:17,65:49
pair_budget=62:16,63:29,64:34,65:76
terminal_profiles=62:0,63:0,64:0,65:13
terminal_subset_pair_rejects=65:13
```

External Pro Roles 01 and 02 independently reconstructed the `D=62..64`
payment. Role 02 isolated the prior stale digest as a serialization-schema
error rather than a mathematical discrepancy. External Pro Roles 01 and 03
independently obtained the `D=65` closure.

## Risk limits

This audit does not establish `M<=211`, remove a recurrence parent, address
affine rank at least 16, or move an official score. The next conservative
boundary wall is `66<=D<=146`.

