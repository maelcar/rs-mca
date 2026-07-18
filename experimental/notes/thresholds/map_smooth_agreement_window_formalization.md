# Map-smooth agreement-window formalization

## Claim

For natural `k,a`, put `ell=k/a+2` and `A=a*ell`.  Then

```text
A + k % a = k + 2*a.
```

Consequently, if `0<a`, then `k+a+1 ≤ A ≤ k+2*a`; moreover
`A=k+2*a` if and only if `a∣k`.

## Status

PROVED.  The unrestricted lower endpoint without `0<a` is COUNTEREXAMPLE.

## Source audit

The active authority is `lem:map-smooth-fiber` in
`experimental/rs_mca_thresholds.tex`, introduced at `856d8362`.  The identical
broader statement was introduced in the predecessor
`experimental/rs_mca_entropy_frontiers.tex` at `2b1a7e20` and is retained in
the current `experimental/asymptotic_rs_mca_frontiers.tex`; its direct TeX consumer is
`prop:map-smooth-cap`.  The existing finite Lean package was produced by PR
#552 at `81dd418a` and integrated at `e190193c`.

The source defines a map-smooth polynomial to have positive degree, so its
parameter `a` is at least one.  A general Nat theorem must expose this premise:
at `a=k=0`, the lower endpoint becomes `1≤0`.  Positivity is not needed for the
remainder identity, upper endpoint, or exact divisibility characterization.

No divisibility hypothesis belongs on the window itself.  The broader paper
explicitly retains nondivisible `a` for circle parity; divisibility controls
only whether the upper endpoint is attained.

## Lean correspondence

The declarations are in
`experimental/lean/petal_fiber/PetalFiber.lean`.

- `map_smooth_agreement_remainder` proves the exact division-algorithm kernel.
- `map_smooth_agreement_lower` and `map_smooth_agreement_upper` prove the two
  endpoints with their minimal hypotheses.
- `map_smooth_agreement_window` packages the source-facing interval.
- `map_smooth_agreement_eq_of_dvd` proves the printed equality case, and
  `map_smooth_agreement_eq_top_iff` strengthens it to an exact characterization.
- `map_smooth_agreement_lower_false_at_zero` locks the necessary positivity
  repair.
- `A_lower`, `A_upper`, and `A_eq_k_plus_2a` retain the former fixed API as
  corollaries of the general theorems.

The package README contains the complete source-label to Lean-name status map.

## Proof outline

Natural-number division gives

```text
k % a + a * (k / a) = k.
```

Distributing `a*(k/a+2)` and rearranging yields the exact remainder identity.
The upper endpoint drops `k%a`.  For `0<a`, the strict bound `k%a<a` yields the
lower endpoint.  Finally, equality at the upper endpoint is equivalent to zero
remainder, hence to `a∣k`.  The additive identity avoids truncated subtraction.

## Validation

From `experimental/lean/petal_fiber`:

```bash
lake clean
lake build
```

From the repository root:

```bash
python3 experimental/scripts/verify_map_smooth_agreement_window.py --check
python3 experimental/scripts/verify_map_smooth_agreement_window.py --tamper-selftest
```

The first command is expected to end with `RESULT: PASS (66841/66841)`; the
second is expected to report `tamper-selftest: caught 4/4` and the same PASS
result.

## Scope and nonclaims

This packet formalizes only the integer agreement arithmetic.  It does not
encode fields, `phi`, `D`, `Q`, `N`, or map-smooth semantics; prove the general
side condition `ell≤N-1`; construct `z`, `u_z`, a codeword list, or distinctness;
formalize the pigeonhole, polynomial-composition injectivity, or degree
arguments; prove a general list-size lower bound; apply collision-aware pole
conversion; or define and bound an MCA/CA object.  It does not prove a
Chebyshev/circle transfer, profile-envelope comparison, lower reserve,
deployed-row result, MCA threshold, or Proximity Prize claim.
