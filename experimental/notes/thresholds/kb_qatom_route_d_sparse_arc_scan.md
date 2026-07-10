# KB-MCA Route-D terminal wall: sparse-arc calibration

Status: **AUDIT / EXPERIMENTAL**.  This is an independent finite check of the
post-v54 wall isolated by Scott Hughes,

```text
T = {U subset I_t : |U|=e, t-1 in U, U has a free-1 partner in I_t},
|T| <= H2 = 77291948627                         (deployed target; OPEN).
```

The packet changes the variable missing from v54's dense toys: the subgroup
index `(p-1)/n`.  KoalaBear has index `1016` and terminal prefix ratio
`n'/n = 1183520/2097152`.  No result below is promoted to the deployed row.

## Pre-registered scan

All rows use the exact high signature of the monic locator,
`(coeff X^(e-1), ..., coeff X)`.  A collision between distinct sets is checked
to be disjoint and is therefore an exact free-1 partner witness.

| block | p | n | t | e | primitive steps | purpose |
|---|---:|---:|---:|---:|---:|---|
| index gradient | `q*n+1`, `q in {4,18,67,253,513,1017}` | 64 | 36 | 3,4 | `r=1` | dense-to-KB-index controls |
| KB-index power-of-two | 65089 (`q=1017`) | 64 | 36 | 3,4 | all 32 | all generator choices |
| KB-index shape e=3 | 97441 (`q=1015`) | 96 | 54 | 3 | all 32 | matches `e/n` and `t/n` |
| KB-index shape e=4 | 129793 (`q=1014`) | 128 | 72 | 4 | all 64 | power-of-two, matches `e/t` and `t/n` |

For a primitive step `r`, the prefix is
`(1, omega^r, ..., omega^((t-1)r))`.  Multiplying the entire prefix by a
nonzero phase scales each signature coordinate by a nonzero power, so the
collision count is phase invariant.  Exhausting all units `r mod n` therefore
exhausts all primitive-step cyclic GP arcs for the three KB-index blocks.

## Hard caps and exclusions

```text
primary e-subsets enumerated: 69,145,998
independent dual-path replay:    421,074
total e-subset evaluations:   69,567,072 <= 70,000,000
largest per-step chunk:      C(72,4) = 1,028,790
largest terminal map:        C(71,3) = 57,155
address-space cap:            2 GiB (ulimit -v 2097152)
```

The scan stops at `e=4`.  A shape-matched `e=5` row would use `(n,t)=(160,90)`;
one step already costs `C(90,5)=43,949,268`, and all 64 primitive steps cost
`2,812,753,152`, beyond the registered cap.  This truncation is part of the
verdict, not evidence about `e=67472`.

The repository overnight exclusions are also binding: no `N'=64` birthday
run, no pure-height `N'>=128` fullness attempt, no naive spectral/EML work, and
no exhaustive `sigma>=2, n>=32` worst-word search is performed.  This packet
only enumerates fixed-size locator signatures on GP prefixes.  Its `n=64` and
`n=128` parameters are subgroup orders with prefixes `t=36` and `t=72`; they
are not the forbidden `N'` birthday or pure-height cells.  The displayed
birthday load is derived arithmetic, not a separate randomized search.

## Results

### Index gradient (canonical primitive step)

| q=(p-1)/n | p | T(e=3) | partner pairs | T(e=4) | partner pairs |
|---:|---:|---:|---:|---:|---:|
| 4 | 257 | 55 | 58 | 11 | 11 |
| 18 | 1153 | 4 | 4 | 0 | 0 |
| 67 | 4289 | 0 | 0 | 0 | 0 |
| 253 | 16193 | 0 | 0 | 0 | 0 |
| 513 | 32833 | 0 | 0 | 0 | 0 |
| 1017 | 65089 | 0 | 0 | 0 | 0 |

These six pinned indices are controls, not a monotonicity scan.  The uniform-hash
birthday-load diagnostics fall from `58.960393` to `0.000919203` for `e=3`
and from `20.188773` to `0.000001243` for `e=4`; those diagnostics are not
deterministic bounds.

### All primitive steps at KB-like index

| block | q | steps | subsets enumerated | min T | max T | sum T |
|---|---:|---:|---:|---:|---:|---:|
| `n64,e3` | 1017 | 32/32 | 228480 | 0 | 0 | 0 |
| `n64,e4` | 1017 | 32/32 | 1884960 | 0 | 0 | 0 |
| `n96,e3` | 1015 | 32/32 | 793728 | 0 | 0 | 0 |
| `n128,e4` | 1014 | 64/64 | 65842560 | 0 | 0 | 0 |

Thus every registered primitive-step arc at index `q in {1014,1015,1017}` is
collision-free at the terminal: **T=0**.  The two shape rows have
`t/n=9/16`, versus deployed `1183520/2097152 = 0.5643463134765625`, and
`e/n=1/32`, versus deployed `67472/2097152 = 0.03217315673828125`.
Their uniform-hash load diagnostics are `0.003399882` (`n96,e3`) and
`0.000025398` (`n128,e4`), so zero is consistent with birthday underload.

### Exact positive-control witnesses

The verifier expands both monic locators and checks equality through the
`X` coefficient, unequal constants, disjointness, prefix membership, and the
terminal mark.

| (q,p,e) | U | V | high signature | (c_U,c_V; c_U-c_V) |
|---|---|---|---|---|
| (4,257,3) | (11,12,35) | (0,4,27) | (147,201) | (30,165;122) |
| (4,257,4) | (3,5,6,35) | (0,1,23,31) | (194,133,75) | (11,111;157) |
| (18,1153,3) | (5,31,35) | (6,7,16) | (524,476) | (1103,898;205) |

### Verdict

- **PROVED for the registered finite rows:** the exact counts above, including
  all primitive generator steps in the four sparse blocks and all phases by
  coefficient scaling.
- **AUDIT / EXPERIMENTAL for Route-D:** sparse KB-index arcs behave differently
  from v54's dense `n≈p` toys, but the registered small-e rows are
  birthday-underloaded.
- **OPEN at deployment:** this bounded scan supplies no uniform theorem in `e`
  and therefore does not establish `|T| <= H2` for `e=67472`.

## Reproducibility

Zero-argument, stdlib-only, deterministic replay (including nine live tamper
tests):

```bash
ulimit -v 2097152
python3 experimental/scripts/verify_kb_qatom_route_d_sparse_arc_scan.py
```

The scan is chunked by primitive step.  The verifier also recomputes every
index-gradient row and the `(n,t,e)=(96,54,3)` zero row through an independent
full-fiber/general-locator path; the `n=64` sparse step-1 checks reuse the
matching gradient computations.  The `n=128,e=4` dual path is omitted because
one more `C(72,4)` replay would exceed the remaining cap.  Reference run:
69,567,072 total subset evaluations, `RESULT: PASS`, peak RSS below 35 MiB;
elapsed time is machine dependent.

## Status and nonclaims

- **AUDIT / EXPERIMENTAL:** bounded exact finite enumeration with a capped
  independent full-fiber cross-check.
- Does not prove `|T| <= H2` at deployed `(n',e)=(1183520,67472)`.
- Does not prove monotonicity in subgroup index, `e`, `t`, or the primitive
  step.
- Does not reopen v54's refuted pack-`k`-only or unrestricted-star routes.
- Does not prove `A_SP <= t*p` or the alternate `|R2| <= e*p` close.

## Lineage

This packet supports, and does not race or replace, Scott Hughes's Route-D
line integrated through v54.  In particular it starts from v54's terminal-star
reduction and measures only the sparse-arc dimension absent from its dense
small-field table.
