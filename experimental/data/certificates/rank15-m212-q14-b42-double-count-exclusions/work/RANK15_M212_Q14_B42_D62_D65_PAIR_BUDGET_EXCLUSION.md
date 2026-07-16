# Rank-15 `M=212`, `q=14`, `B=42`: exclusion of `D=62..65`

## Claim

Let `A` be an arrangement of 42 distinct projective lines. Assume that:

- `A` has exactly 211 distinct intersection points;
- every line contains exactly 15 distinct arrangement intersections; and
- every intersection has multiplicity at most 15.

For `2 <= k <= 15`, let `n_k` count the multiplicity-`k`
intersections and put `D=n_2`. Then

```text
D not in {62,63,64,65}.
```

This incidence theorem applies to each of the two source-realized rank-15
aggregate rows under the hypotheses recorded in
`experimental/notes/l2/rank15_m212_q14_b42_double_count_exclusions.md`.
The finite proof below is field-independent after that source interface has
been established.

## Global moments

Counting points, line-point incidences, and pairs of lines gives

```text
sum n_k          = 211,
sum k n_k        = 42*15 = 630,
sum C(k,2) n_k   = C(42,2) = 861.
```

For `1 <= w <= 12`, put `c_w=n_{w+3}`. Since
`sum k^2 n_k=2*861+630=2352`, a fixed value of `D` has exactly the
nonnegative integral profiles satisfying

```text
sum w c_w       = D-3,
sum w^2 c_w     = 471-D,
sum c_w         <= 211-D.
```

The last inequality is equivalent to `n_3>=0`. Thus this is an exact bounded
moment system rather than a relaxation.

## Line equations and packing gate

On a line `L`, let `d_L` and `t_L` count double and triple points. If its
higher-multiplicity points have weights `w=k-3`, let `S_L` be their total
weight and `s_L` their number. Counting support points and the other 41 lines
gives

```text
d_L = S_L-11,
t_L = 26-S_L-s_L.
```

Consequently every line obeys

```text
S_L >= 11,
S_L+s_L <= 26.
```

At a point of weight `w<=10`, its `w+3` lines each require at least `11-w`
additional high-point weight. Any other point lies on at most one of those
lines. The remaining high points must therefore contain at least `w+3`
disjoint groups of weight at least `11-w`, with weight-11 and weight-12
points each supplying one group. The verifier computes the exact maximum
number of such groups by dynamic programming over minimal group multisets.

The exact ledger after this gate is

| `D` | moment profiles | packing survivors |
|---:|---:|---:|
| 62 | 1,825 | 26 |
| 63 | 2,172 | 41 |
| 64 | 2,573 | 51 |
| 65 | 3,103 | 138 |

## Heavy/no-heavy pair budget

Call a point heavy when its multiplicity is at least 11. Three heavy points
cannot lie on one arrangement line because then `S_L+s_L>=27`. Let `H` be
the number of heavy points, `I_H` their total multiplicity, and let `x_j`
count lines containing exactly `j` heavy points. Then

```text
x_0+x_1+x_2 = 42,
x_1+2*x_2   = I_H,
x_2         <= C(H,2).
```

Hence the number of no-heavy lines satisfies

```text
x_0 <= z_max := 42+C(H,2)-I_H.
```

A nonheavy multiplicity-`k` point lies on at least `max(0,k-H)` no-heavy
lines. Distinct nonheavy points cannot consume the same pair of no-heavy
lines. Therefore

```text
sum_nonheavy C(max(0,k-H),2) <= C(z_max,2).
```

For `D=62,63,64`, this rejects every packing survivor. The exact counts are

| `D` | negative `z_max` | pair rejects | minimum positive gap | survivors |
|---:|---:|---:|---:|---:|
| 62 | 10 | 16 | 4 | 0 |
| 63 | 12 | 29 | 3 | 0 |
| 64 | 17 | 34 | 2 | 0 |

For `D=65`, it rejects 49 profiles by negative `z_max` and 76 by the pair
budget, leaving exactly 13 profiles.

## Subset-pair lemma

Let `X` be any set of `s` distinct arrangement intersections. For each of
the 42 lines put `r_L=|X intersect L|`, and let `J` be the sum of the
multiplicities of the points in `X`. Then

```text
sum_L r_L = J.
```

Every pair of points in `X` lies on at most one arrangement line, so

```text
sum_L C(r_L,2) <= C(s,2).
```

Write `J=42q+r`, with `0<=r<42`. Convexity of `C(x,2)` shows that its sum
over 42 nonnegative integers of total `J` is minimized at the balanced
vector. Thus every such `X` must satisfy

```text
(42-r) C(q,2) + r C(q+1,2) <= C(s,2).                 (SP)
```

For each of the 13 `D=65` survivors, a descending multiplicity prefix
violates `(SP)`. The exact terminal margins are:

```text
4 profiles: 17 > 15,
1 profile:  18 > 15,
1 profile:  22 > 21,
7 profiles: 11 > 10.
```

The verifier prints the complete 13-profile ledger, including each terminal
subset and both sides of `(SP)`. Hence no `D=65` profile survives.

## Replays and independent audit

Run from the packet's `work/` directory:

```bash
python3 verify_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.py
python3 -O verify_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.py
ruby --disable-gems -W0 audit_rank15_m212_q14_b42_d62_d65_pair_budget_exclusion.rb
```

The Python verifier follows the descending-weight enumeration used for the
`D=65` proof. The Ruby audit independently enumerates weights in ascending
order and rebuilds the packing and pair budgets without importing the Python
implementation. External Role 02 independently reconstructed `D=62..64` and
identified the old hostile-output digest as a schema-level packaging error;
external Roles 01 and 03 independently obtained the same exclusion endpoints.

## Exact remaining wall

After this theorem, the conservative boundary remainder is

```text
66 <= D <= 146.
```

The theorem does not establish the full `M<=211` child theorem, remove any
rank-15 recurrence parent, address affine rank at least 16, or move either
official RS-MCA score.

