# RS-MCA Thresholds Integration Audit

Date: 2026-07-13

## File

- `experimental/rs_mca_thresholds.tex`
- `experimental/rs_mca_thresholds.pdf`

## Verdict

This is a coherent exact-threshold integration draft and should be read before
`experimental/asymptotic_rs_mca_frontiers.tex` for exact MCA staircase work.
It is shorter, cleaner, and more self-contained for the proved finite/deep
regimes.

It should not simply delete the older frontiers draft yet.  The frontiers draft
still contains broader conditional profile-envelope, cell-budget, Sidon/BSG,
and v13-raw interface material that is only partially represented in the new
threshold paper.

## Main Additions

- Exact CA/sparse decomposition for support-wise MCA.
- Exact deep and quadratic MCA staircases, including MDS-compatible upper
  bounds and the universal tangent floor.
- Self-contained half-Johnson CA/MCA bound.
- Four certified prime-field Proth rows at the official rates with
  `k = 2^40`, `p < 2^256`, power-of-two smooth domains, exact budgets
  `B = floor(p / 2^128)`, and half-open safe sets `[0, B/n)`.
- Exact `F_17^32`, `n=512`, `k=256` 6/7 gate.
- Smooth, generalized-RS, and circle-code transports where diagonal or
  stereographic agreement equivalence is proved.
- A target-aware certificate formula: matching safe/unsafe certificates at
  agreement `k+1+gn+o(n)` give `delta* = 1-rho-g+o(1)`.

## Status

`SUBMISSION DRAFT / PROVED WHERE STATED / AUDIT`.

The TeX compiles with `tectonic experimental/rs_mca_thresholds.tex`.
The four Proth rows are printed with enough integer data for independent
checking, but they should still receive a separate adversarial arithmetic and
definition audit before being promoted into Paper D or treated as final prize
submission authority.

## Recommended Next Steps

1. Audit the exact CA/sparse decomposition against the official support-wise
   MCA definition and endpoint convention.
2. Independently verify the four Proth certificates and the displayed
   `F_{n,k}(B-1) >= 0 > F_{n,k}(B)` signs.
3. Add a small machine-readable JSON packet for the four Proth rows.
4. Decide whether to promote this paper as the main experimental submission
   draft and keep `asymptotic_rs_mca_frontiers.tex` as the long audit appendix.
5. Start Lean formalization with the exact definitions, monotonicity/endpoint
   lemma, tangent floor, and quadratic mean-overlap theorem.
