# Powersum rigidity formalization map

Build the package with the pinned toolchain:

```bash
lake build
```

## Weighted moment rank

Source snapshot:
`experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md` at `168e9ba0`.
The source labels below are section headings or numbered displayed equations
in that note.

| Source label | Lean declaration | Status |
|---|---|---|
| Exact rank factorization, Vandermonde full-row-rank step | `rectangularVandermonde_rows_linearIndependent` | PROVED |
| Exact rank factorization, left-Vandermonde rank step for (2) | `rectangularVandermonde_rank` | PROVED |
| Exact rank factorization, right-Vandermonde surjectivity step for (2) | `rectangularVandermonde_mulVec_surjective` | PROVED |
| Exact rank factorization, invertible diagonal step for (2) | `diagonal_mulVec_surjective` | PROVED |
| Equation (1) | `weightedMomentMatrix_factorization` | PROVED |
| Exact rank factorization, surjective-factor rank step for (2) | `rank_mul_eq_left_of_mulVec_surjective` | PROVED |
| Equation (2) | `weightedMomentMatrix_rank` | PROVED |
| Equation (3), repaired all-natural form | `weightedMomentMatrix_rank_lt_iff_card_lt` | PROVED |
| Equation (3), repaired all-natural conjunction | `weightedMomentMatrix_rank_lt_iff_pos_and_card_le_sub_one` | PROVED |
| Equation (3), source form with necessary `0 < t` | `weightedMomentMatrix_rank_lt_iff_card_le_sub_one` | PROVED |

The rank theorem keeps the source hypotheses.  Equation (3), written with
natural subtraction, is false at `t = 0`; the unconditional statement is
`E.card < t`, while the source's `E.card ≤ t - 1` form requires `0 < t`.
This module does not extract an error support, construct a Route-D/RIM
adapter, or prove any deep-owner or payment statement.
