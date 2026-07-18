# Map-smooth agreement-window formalization

This standalone Lean 4.14 package formalizes the integer agreement arithmetic
inside `lem:map-smooth-fiber`.  The statement was introduced in the active
source `experimental/rs_mca_thresholds.tex` at `856d8362`; the identical
statement was introduced in the predecessor
`experimental/rs_mca_entropy_frontiers.tex` at `2b1a7e20` and is retained in
the current `experimental/asymptotic_rs_mca_frontiers.tex`.  The original finite Lean package was produced by PR #552 at
`81dd418a` and integrated at `e190193c`.

## Theorem map

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| Package arithmetic and fixed-toy setup | `binom`, `ceilDiv`, `a`, `k`, `Nq`, `n`, `Bsize`, `ell`, `Aagree`, `Llist`, `qMinusN`, `capNum`, `capDen`, `capExact`, `capCeil`, `mThresh` | DEFINITIONS; the lowercase parameter names are fixed toy values |
| `lem:map-smooth-fiber`: exact remainder identity for `A=a*(k/a+2)` | `map_smooth_agreement_remainder` | PROVED, all natural `a,k` |
| `lem:map-smooth-fiber`: lower agreement endpoint | `map_smooth_agreement_lower` | PROVED with explicit `0<a` |
| `lem:map-smooth-fiber`: upper agreement endpoint | `map_smooth_agreement_upper` | PROVED, all natural `a,k` |
| `lem:map-smooth-fiber`: two-sided agreement window | `map_smooth_agreement_window` | PROVED with explicit `0<a` |
| `lem:map-smooth-fiber`: equality when `a∣k` | `map_smooth_agreement_eq_of_dvd`, `map_smooth_agreement_eq_top_iff` | PROVED; the latter is an iff |
| Missing-positive-degree regression | `map_smooth_agreement_lower_false_at_zero` | COUNTEREXAMPLE to an unrestricted lower endpoint |
| Former fixed agreement anchors | `A_lower`, `A_upper`, `A_eq_k_plus_2a` | PROVED as corollaries of the general arithmetic |
| Remaining fixed parameter, list-size, cap, and threshold declarations | `ell_value`, `n_value`, `Aagree_value`, `ell_le_N_minus_1`, `a_divides_k`, `binom_4_3`, `Llist_value`, `Llist_exact_div`, `list_size_lower`, `capDen_value`, `capNum_value`, `cap_divides`, `capExact_value`, `capCeil_eq_exact`, `map_smooth_cap_instance`, `map_smooth_cap_pos`, `m_ge_k_plus_1`, `m_le_A`, `ell_value'`, `A_eq_k_plus_2a'`, `ell_le_N_minus_1'`, `Llist_value'`, `capExact_value'`, `A_lower'`, `A_upper'` | PROVED, fixed numerical anchors only |
| Full map-smooth fiber/list construction in `lem:map-smooth-fiber` | none | NOT FORMALIZED IN LEAN |
| Collision-aware MCA statement in `prop:map-smooth-cap` | none | NOT FORMALIZED IN LEAN |

## Exact arithmetic and boundary repair

Let `ell = k/a + 2` and `A = a*ell`.  Lean's total natural division gives the
hypothesis-free identity

```text
A + k % a = k + 2*a.
```

The upper endpoint follows by dropping the nonnegative remainder.  If `0<a`,
then `k%a<a`, which yields the lower endpoint.  The source already has this
positivity because `a` is a polynomial degree at least one.  An unrestricted
Nat transcription would be false at `a=k=0`, where it asserts `1≤0`.

The identity also proves that the upper endpoint is attained exactly when
`a∣k`.  No assumption `a∣k`, `a≤k`, `0<k`, `ell≤N-1`, or parameter `N` is
needed for the two-sided arithmetic window beyond `0<a`.

## Scope

The package does not define fields, a polynomial `phi`, the sets `D`, `Q`, or
their map-smooth fibers.  It does not prove a general `ell≤N-1` side condition,
construct `z`, `u_z`, or distinct codewords, perform the pigeonhole argument,
prove polynomial
composition injectivity or degree bounds, establish a general list size, apply
the collision-aware pole conversion, or formalize an MCA/CA object.  It also
does not prove a Chebyshev/circle transport, profile-envelope comparison, lower
reserve, deployed-row result, MCA threshold, or Proximity Prize claim.

Build with the pinned toolchain:

```text
lake build
```
