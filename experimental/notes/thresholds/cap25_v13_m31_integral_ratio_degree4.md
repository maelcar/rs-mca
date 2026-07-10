Continues PR #481 (degree-two spherical-LP cut) and PR #480 (two-shell wall).

# CAP25 v13 raw: the full constant-weight Delsarte LP escalates the M31 two-shell cut — eigenspace `j=3` rules out 340 integral-ratio pairs that #481's degree-two bound misses

Status per claim:
`PROVED` (the Johnson-scheme `J(n,m)` Delsarte LP is a sound elimination for every
integral-ratio grid pair; eigenspace `j=2` set-equals #481's exact 187; eigenspaces
`j<=6` eliminate exactly 527, so 340 pairs strictly beyond #481; the single-forced-
eigenvalue inclusion-moment cut is exactly vacuous on the whole grid) /
`PROVED-AT-TOYS` (soundness gates: the LP never eliminates a realizable two-shell family
on the faithful `p=31,n=8`, `p=127,n=16` (exhaustive), and `p=127,n=32` (witness) toys) /
`ANALYSIS` (the cascade saturates at `j=3`; a thin-band probe finds no elimination through
eigenspace `j=20`; eliminations are confined to `e1` within 284 of the centered radius) /
`OPEN` (the residual 3254358 pairs are Delsarte-LP-consistent; the two-shell cell is not paid).

**Verifier:** `experimental/scripts/verify_m31_integral_ratio_degree4.py`
(zero-argument, stdlib only; regenerates the grid, the Eberlein eigenvalues, the full-grid
LP scan, the moment-vacuity scan, the toy soundness gates, and corruption self-tests).
**Data:** `experimental/data/cap25_v13_m31_integral_ratio_degree4.json`.

## 0. Result

At the binding Mersenne-31 list row, PR #480 reduces every first violating two-shell family
to one of 3,254,885 integral-ratio pairs `(k,t)` with `e1=(k-1)t`, `e2=kt`. PR #481's
degree-two spherical-LP cut eliminates 187 of them. This note replaces that cut by the full
**constant-weight (Johnson-scheme) Delsarte linear-programming bound** and proves:

```text
deployed constants:
  p=2^31-1=2147483647,  n=2^21=2097152,  m=981129,  w=67447,
  B*=2^24-1=16777215,   L0=B*+1=16777216.

grid pairs                                   3254885
eliminated at eigenspace j<=2  (= #481)          187   (set-identical to #481)
newly eliminated at eigenspace j=3              +340
eliminated at eigenspaces j=4,5,6                  0
------------------------------------------------------
total eliminated (Delsarte LP, j<=6)             527
surviving                                    3254358
```

So the escalation is a genuine exact improvement: it removes **340 pairs that no spherical
degree-two bound can reach**, dropping the surviving count from #481's 3,254,698 to 3,254,358.
It does **not** pay the two-shell cell.

## 1. The cut is the constant-weight Delsarte LP  `PROVED`

Let `F` be a family of `m`-subsets of the `n`-point domain whose two exchange distances are
`e1<e2`. Because `|A|=|B|=m`, the exchange distance `e(A,B)=|A\B|=m-|A cap B|` is exactly the
Johnson-scheme distance, so `F` is a **two-distance code in `J(n,m)`**. If `|F|>B*`, retain any
`L0=B*+1` members; the retained set is still a two-distance code, of size `L0`, with distances
`subset {e1,e2}`. Its inner distribution is `(1, alpha, beta)` with

```text
alpha = (#ordered e1-pairs)/L0 >= 0,
beta  = (#ordered e2-pairs)/L0 >= 0,
alpha + beta = L0 - 1.
```

Delsarte's inequality (the primitive idempotent `E_j` of the scheme is positive semidefinite,
so `1_F^T E_j 1_F >= 0`) gives, for every eigenspace `j=0,1,...,m`,

```text
1 + alpha * p_j(e1) + beta * p_j(e2) >= 0,                       (1.1)
```

where `p_j(e)=P_e(j)/v_e` is the normalized Johnson eigenvalue (`P` the Eberlein eigenvalue,
`v_e` the valency). Since the only free variables are `alpha,beta>=0` with `alpha+beta=L0-1`,
(1.1) over `j=1..J` is a one-dimensional interval-feasibility LP. If it is infeasible, no size-`L0`
two-distance code with distances `{e1,e2}` exists, so no `F` with `|F|>B*` and shells `{e1,e2}`
exists: the pair is eliminated. Using a finite set of eigenspaces `j<=J` is a subset of Delsarte's
constraints, hence any infeasibility it detects is sound. Infeasibility is monotone in `L`, so an
elimination at `L0` rules out every `L>=L0`.

## 2. Exact normalized eigenvalues  `PROVED`

The raw Eberlein binomials are astronomically large (`~10^{300000}` digits at the deployed scale),
but the normalized eigenvalue has a tractable falling-factorial form. With `x^{(a)}=x(x-1)...(x-a+1)`,

```text
p_j(e) = N_j(e) / D_j,
N_j(e) = sum_{s=0}^{j} (-1)^s C(j,s) [e^{(s)}]^2 (m-e)^{(j-s)} (n-m-e)^{(j-s)},
D_j    = m^{(j)} (n-m)^{(j)} > 0.                                (2.1)
```

Each `N_j(e)` is a sum of `j+1` products of at most `2j` integer factors, so (1.1) is decided by
exact integer cross-multiplication. The verifier proves (2.1) equals `P_e(j)/v_e` and proves the
`P_e(j)`, together with the multiplicities `mu_j=C(n,j)-C(n,j-1)`, are the true spectrum by matching
`tr(A_i^t)=sum_j mu_j P_i(j)^t` against brute-force Johnson schemes `J(6,3),J(7,3),J(8,3),J(9,4)`.

## 3. Exact scan certificate  `PROVED`

Scanning every grid pair with the LP over eigenspaces `j<=6`:

| gate | exact count |
|---|---:|
| PR #480 grid | 3,254,885 |
| eliminated at eigenspace `j<=2` (set-identical to PR #481) | 187 |
| newly eliminated at eigenspace `j=3` | 340 |
| eliminated at eigenspaces `j=4,5,6` | 0 |
| **total eliminated (Delsarte LP)** | **527** |
| **surviving** | **3,254,358** |

The binding eigenspace of every eliminated pair is `2` or `3`; the cascade saturates at `j=3`.
All 527 eliminations satisfy `e1 in [521834, 522118]` — within 284 of the centered-radius floor
`floor(m(n-m)/n)=522118`. A restricted probe of that band through eigenspace `j=20` finds the same
527 and nothing more, so no higher harmonic contributes. The `j=2` block equals #481's cut exactly
(the verifier checks set-equality against #481's closed-form degree-two certificate).

The 340 newly eliminated pairs use 340 distinct `(k,t)`; their canonical row list
(`k,t,e1,e2,j` joined by commas, rows by semicolons) and SHA-256, plus per-column checksums, are
in the data JSON and recomputed by the verifier.

## 4. The naive M31-moment cut is exactly vacuous  `PROVED`

PR #480's named next step was "rule out using M31 moments". The clean inclusion-matrix version is:
for each `t`, the Gram matrix `M_t=(C(|A cap B|,t))_{A,B}` (entries `C(m-e,t)`) is positive
semidefinite, and `-k` is a forced eigenvalue of the `e1`-adjacency in `1^perp`; evaluating `M_t`
on that eigenvector gives

```text
C(m,t) - k*C(m-e1,t) + (k-1)*C(m-e2,t) >= 0.                     (4.1)
```

The verifier evaluates (4.1) for `t=2,3,4` on **every** grid pair: the minimum is `>= 0`. So this
single-forced-eigenvalue moment constraint is **vacuous** — it fires nowhere. The escalation in this
packet comes instead from the *distributional* Delsarte LP (1.1), which couples all pairs of the two
shells through the whole eigenvalue column, not just the extreme eigenvalue `-k`.

## 5. Soundness gates  `PROVED-AT-TOYS`

A cut that eliminates a realizable pair is worthless. The verifier reconstructs the faithful
twin-coset toys of #476/#480 and asserts the LP never eliminates a realizable two-shell family:

```text
p=31,  n=8,  m=4, w=2:  1 realizable family  (max size 2)          -> not eliminated
p=127, n=16, m=8, w=1:  62 realizable (e1,e2,size), exhaustive     -> none eliminated
                         (includes the size-23 family, shells {2,4})
p=127, n=32, m=15,w=2:  the inclusion-maximal size-17 witness,
                         shells {7,8}                              -> not eliminated
```

Each gate runs the LP at the toy's own `(v,m)` up to eigenspace `j=m` and confirms feasibility at
the realized size. The Eberlein formula used at deployment is the same polynomial verified against
the brute-force toy spectra, so the soundness established on the toys transfers as an identity.

## 6. Wall and nonclaims

- The residual **3,254,358** pairs are Delsarte-LP-consistent: feasible at every eigenspace `j<=6`
  on the full grid, and `j<=20` on the confinement band. No harmonic of the Johnson scheme pays
  them. The obstruction, if any, is genuinely beyond the Delsarte hierarchy — the natural remaining
  lever is the modular `-k` `F_p`-nullity certificate of #480 §5, or a realizability/SDP argument,
  neither of which is an LP inequality.

Nonclaims:

- This packet does not rule out all 3,254,885 pairs or pay the two-shell cell `|F|<=B*`.
- It does not construct a family above `B*`, at deployment or in any toy.
- "Surviving" means "not eliminated by the Delsarte LP through eigenspace `j<=6` (band `j<=20`)",
  not "realizable".
- The `j<=20` band saturation is `ANALYSIS`, not a proof that no eigenspace `j>6` ever fires
  off-band; the exact deployed theorem is the `j<=6` full-grid count 527.
- No faithful-toy statement is promoted to a deployed theorem.

## 7. Reproduce

```text
ulimit -v 2097152; python3 experimental/scripts/verify_m31_integral_ratio_degree4.py
```

The verifier recomputes the grid, the Eberlein eigenvalues (brute-force checked), the full-grid LP
scan (527 eliminated / 3,254,358 surviving, binding eigenspaces `{2:187, 3:340}`), the moment-cut
vacuity, the three toy soundness gates, the exact JSON packet, and eight corruption self-tests.
