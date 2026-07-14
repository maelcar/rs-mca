# Rank-15 `d = 4828` weighted-clique and pencil-defect cut

**Status:** PROVED under the imported rank-15 locator-saturation normal form,
with a replayable exact finite certificate.

## Result

This note sharpens the first residual state left by
`experimental/notes/l2/rank15_locator_incidence_capacity_degree_floor.md`.
It consumes that note's exact deployed state

```text
M = 218,  d = 4828,  t = b = 218,  0 <= r <= 151,
G simple and 7-regular on the 218 listed points,
8r + 7delta + eta <= 1658,
```

and the coprime-pencil notation of
`experimental/notes/thresholds/rank15_locator_saturation_normal_form.md`.
In particular, the proper-section cap `q = 15` remains an imported
hypothesis. No cyclic identity for the evaluation-domain locator is used.

### Theorem

Every state satisfying the hypotheses above obeys

```text
eta >= 248,
deg(E) <= delta,
8r + 7delta <= 1410.
```

More exactly, if `F_nu` is the selected pencil member in direction `nu`,
`R_nu` is its set of roots in `H\Z`, and `e_nu` is the multiplicity of the
unique rich coordinate line in that direction, then

```text
d - e_nu = alpha_nu + sigma_nu + iota_nu + zeta_nu,
delta = alpha + sigma + iota + deg(E),
```

where all terms are nonnegative integers and at most one `alpha_nu` is
nonzero. Consequently,

```text
deg(E) <= delta,
|C| = 1052 + delta - sigma - iota <= 1052 + delta,
number of perfect selected fibers >= 218 - delta.
```

A perfect selected fiber has `d - e_nu = 0`; for such a fiber,

```text
deg(F_nu) = d,
F_nu = L_{R_nu} divides L_H,
```

and its `d` roots are exactly the active coordinates belonging to its rich
line. In particular,

```text
delta <= floor((1410 - 8r)/7),
```

so `delta, deg(E) <= 201` globally and `delta, deg(E) <= 28` at `r = 151`.
At least 17 selected fibers are perfect globally, and at least 190 are
perfect at `r = 151`.

The finite parameter ledger changes as follows:

```text
coarse (r, delta) pairs:       22,973 -> 17,589  (5,384 removed)
coarse (r, delta, eta) triples: 13,502,312 -> 8,469,896
                                      (5,032,416 removed)
```

These are counts of integer parameter states, not counts of source-realizable
Reed--Solomon configurations.

## Exact fiber-defect decomposition

Use the normalized coprime pencil

```text
V_1 = L_Z G A,  V_2 = L_Z G B,  gcd(A,B) = 1.
```

For a selected projective direction `nu = [lambda:mu]`, let

```text
F_nu = monic(mu A - lambda B),
R_nu = {x in H\Z : F_nu(x) = 0},
F_nu = L_{R_nu} E_nu.
```

Let `c_nu` count active coordinates of normal direction `nu`. Define

```text
alpha_nu = d - deg(F_nu),
sigma_nu = c_nu - e_nu,
iota_nu = |R_nu intersect I|,
zeta_nu = deg(F_nu) - |R_nu| = deg(E_nu).
```

Every root of `F_nu` in `H\Z` is either an active coordinate of direction
`nu` or an inactive point in `I`. Thus

```text
|R_nu| = c_nu + iota_nu,
```

and insertion of `deg(F_nu)`, `|R_nu|`, and `c_nu` gives

```text
d - e_nu
  = (d - deg(F_nu))
  + (deg(F_nu) - |R_nu|)
  + (|R_nu| - c_nu)
  + (c_nu - e_nu)
  = alpha_nu + zeta_nu + iota_nu + sigma_nu.
```

Summing over the 218 selected directions and using
`E = product_nu E_nu` proves

```text
delta = alpha + sigma + iota + deg(E).
```

The leading coefficient of `mu A-lambda B` can cancel in at most one projective
direction, so at most one `alpha_nu` is nonzero. Nonnegativity already gives
`deg(E) <= delta`.

The selected pencil members are pairwise coprime. Hence the sets `R_nu` are
disjoint and, with `R` their union,

```text
deg(Q_T) = 218d - alpha,
|R| = deg(Q_T) - deg(E).
```

Since `N - 218d = 1,053,556 - 1,052,504 = 1,052`, the complement
`C = (H\Z)\R` satisfies

```text
|C| = 1052 + alpha + deg(E)
    = 1052 + delta - sigma - iota.
```

Finally, each imperfect direction spends at least one integer unit of
`delta`. This proves the perfect-fiber count and all pencil conclusions.

## Weighted non-rich demand

Each listed point lies on exactly 15 rich lines. For a rich line `ell`, set

```text
delta_ell = d - e_ell,
epsilon_p = sum_{ell contains p} delta_ell.
```

The rich coordinates give point `p` at most

```text
15d - epsilon_p = 72,420 - epsilon_p
```

agreements outside the universal set, while `p` needs `a = 72,451`.
Therefore its non-rich incidence count `n_p` satisfies

```text
n_p >= 31 + epsilon_p,
sum_p epsilon_p = 15delta.                         (1)
```

An occupancy-eight non-rich line induces a `K_8` component in the
7-regular uncovered-pair graph `G`. Remove every such component. If `c` were
removed, the residual graph has

```text
v = 218 - 8c
```

vertices. The source determinant obstruction excludes `v = 10`, while
`v = 2` cannot support a simple 7-regular graph. Thus every nonempty residual
has `v >= 18`.

All distinct residual parameter-line supports of occupancies 7, 6, and 5 are
disjoint: two distinct supports sharing a point would give that point at least
eight distinct uncovered neighbors. Let `k_7,k_6,k_5` count these distinct
supports, and let `u` residual vertices lie on none of them. Different active
coordinates may induce the same support; the weights below are assigned to
points, while `eta`, `n_p`, and the double count retain every coordinate
occurrence. Assign weights

```text
1/7 on a designated K_7,
1/3 on a designated K_6,
3/5 on a designated K_5,
1   on an unassigned residual vertex,
0   on a removed K_8 component.
```

Put

```text
chi = k_7 + 2k_6 + 3k_5 + u.
```

For every actual non-rich coordinate section `x`, including repeated
sections, the sum of its point weights is at most `8-h_x`. The weights of a
designated `K_7,K_6,K_5` are respectively `1,2,3`; a section of occupancy at
most four has weight at most `h_x <= 8-h_x`; and a `K_8` has weight zero.
Double counting (1), assigning each coordinate occurrence its weight once,
gives

```text
eta >= 31chi + sum_{ell rich} delta_ell W_ell >= 31chi,       (2)
W_ell = sum_{p in ell} w_p.
```

The graph equations are

```text
v = 7k_7 + 6k_6 + 5k_5 + u,
chi = k_7 + 2k_6 + 3k_5 + u.
```

They imply `v-chi` is even, so `chi` is even, and `v <= 7chi`. Since
`v >= 18`, one has `chi >= 4`. If `chi = 4`, elimination of `k_7` gives

```text
v = 28 - 8k_6 - 16k_5 - 6u.
```

The congruence `v = 218 (mod 8)` forces `u = 3`, whence `v <= 10`, a
contradiction. Thus `chi >= 6`.

## Exact exclusion of `chi = 6`

After the already-proved `v >= 18` gate, the integer equations have exactly
seven solutions:

```text
label  v   c  k_7 k_6 k_5 u
A1    18  25   0   3   0  0
A2    18  25   1   1   1  0
A3    18  25   2   0   0  4
B1    26  24   2   2   0  0
B2    26  24   3   0   1  0
C     34  23   4   1   0  0
D     42  22   6   0   0  0
```

The bare integer equations also have two `v = 10` rows; they are omitted
here because the source determinant theorem already excludes `v = 10`.

Case A3 is impossible without computation. The two `K_7` blocks have only
14 external stubs. The four remaining vertices need 28 degree units, while
their internal edges supply at most 12. Thus at most 26 units are available.

For the other six cases, every vertex in a `K_h` block has external degree
`8-h`. This gives the following exhaustive finite classifications:

```text
A1: properly three-colored 2-regular cycle multisets;
A2: K_7-K_6, K_7-K_5, K_6-K_5 edge totals respectively 2,5,10;
B1: paths with K_7 endpoints and alternating K_6 interiors, plus even
    alternating K_6-only cycles;
B2: five K_5 attachment triples followed by a three-edge matching;
C:  six K_6 attachment pairs followed by an eight-edge matching;
D:  labelled symmetric zero-diagonal nonnegative-integer 6 by 6 matrices
    with row sum 7.
```

The verifier generates exhaustive records with explicit conventions. A1, B1,
and B2 keep block colors fixed and may retain equal-block relabelings; A2
quotients the within-block permutations preserving its attachment data; C
quotients the simultaneous `S_4` action on its four `K_7` blocks; and D
deliberately enumerates every labelled block-count matrix. The totals below
are therefore exhaustive generated-record counts, not minimal unlabeled
graph-isomorphism counts. Their determinant-square survivors are

```text
case  types checked  determinant-square survivors
A1          3,311             0
A2             78             0
B1          6,204             0
B2            454             0
C           1,125             0
D         100,135           675
```

To justify the test, let `B_inc` be the square point-rich-line incidence
matrix. Then

```text
B_inc B_inc^T = 14I + J - A_G.                              (3)
```

If `G` consists of `c` copies of `K_8` and residual graph `R`, the determinant
lemma gives

```text
det(B_inc B_inc^T)
  = 225 * 7^(c-1) * 15^(7c) * det(14I_v - A_R).             (4)
```

The left side is an integer square. Exact Bareiss determinants eliminate
A1, A2, B1, B2, and C.

In D, the external edges are a perfect matching among six `K_7` blocks. Let
`H=(h_ij)` count matching edges between blocks. It is symmetric, has zero
diagonal, and every row sums to seven. Writing `P` for the matching adjacency
and `U` for the block-indicator matrix gives

```text
14I_42 - A_R = 15I_42 - P - UU^T,
det(14I_42 - A_R) = 224^15 det(119I_6 - H).                 (5)
```

Exactly 675 of the 100,135 labelled matrices survive the square test. For
each survivor, use the rational quadratic form, not merely its determinant.
Put `D_G = 14I-A_G`. Since `D_G 1 = 7 1`, completing the rank-one square
gives

```text
(14I + J - A_G) direct-sum <-1>
  congruent_Q D_G direct-sum <-225/7>.                     (6)
```

If (3) held, the left side would be rationally congruent to
`I_218 direct-sum <-1>`, whose 7-adic Hasse invariant is `+1`. Exact rational
LDL diagonalization gives invariant `-1` on the right side of (6) for every
one of the 675 survivors. Hence D is impossible.

All `chi = 6` states are excluded. Since `chi` is even, `chi >= 8`, and (2)
proves `eta >= 248`. The source budget then gives the asserted
`8r+7delta <= 1410` and all derived bounds.

## Verification

Run

```text
python3 experimental/scripts/verify_rank15_d4828_weighted_clique_pencil_defect.py
python3 -O experimental/scripts/verify_rank15_d4828_weighted_clique_pencil_defect.py
```

Both runs must match
`experimental/data/certificates/rank15-d4828-weighted-clique-pencil-defect/verifier_output.txt`
byte for byte. The verifier uses only the Python standard library and explicit
failures rather than `assert`. It checks the source constants, the seven
`chi=6` skeletons, all six finite graph classifications, every determinant,
all 675 Hasse failures, and the pair/triple counts.

The preserved artifact hashes are

```text
verifier SHA-256: fed7a1e611348bb73fd789b9aa5b02cd43cfe659bc61cda73738e2163cf136a6
output SHA-256:   fee6c895ad7a4ddba6024c9d4e2857e437edac997e1f81bffc79776d37f8384d
```

## Exact remaining wall

The minimum unresolved weighted cost is `chi = 8`. Its ten exact skeletons
`(v,c,k_7,k_6,k_5,u)` are

```text
(18,25,0,2,1,1)  (18,25,1,0,2,1)  (18,25,1,1,0,5)
(26,24,1,3,0,1)  (26,24,2,1,1,1)  (26,24,3,0,0,5)
(34,23,3,2,0,1)  (34,23,4,0,1,1)
(42,22,5,1,0,1)  (50,21,7,0,0,1)
```

They should be tested against graph-degree feasibility, the determinant-square
condition, local Hasse invariants, existence of a `0/1` incidence square root,
the weighted term in (2), and the new defect-`<=201` pencil constraints. If
all ten are excluded, then `chi >= 10`, `eta >= 310`, and
`8r+7delta <= 1348`.

## Nonclaims

This result does not eliminate the complete `M=218,d=4828` state. It does not
prove `M <= 217`, the required rank-15 ceiling `M <= 211`, or the all-rank
Grand List inequality. It does not eliminate affine rank at least 16, prove a
source realization of any remaining skeleton, change Grand MCA, change either
official score, or prove a finite deployed adjacent certificate. The
conclusions are conditional on the exact imported rank-15 normal form,
including `q=15`.
