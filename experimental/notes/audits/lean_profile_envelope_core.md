# Lean formalization of the profile-envelope core

## Status

`PROVED` for the attained finite pigeonhole theorem, the exact GF(11²)
quotient-label certificate, and the collision-floor arithmetic under its stated
interfaces.  `CONDITIONAL` for the profile-envelope frontier skeleton: closed
ledger coverage, natural-profile payment, routed Sidon payment, the direct ray
compiler (RC), identity dominance, and the target-budget inequality are explicit
hypotheses and are not discharged here.

The package contains no `sorry`, `admit`, or custom axioms.  It targets only
the statements marked audit-stable in
`experimental/notes/audits/asymptotic_profile_envelope_audit.md` and does not
overlap the Li--Wan prefix-flatness, Vandermonde-rank, or finite-anchor Lean
work in open PRs #498, #501, #506, and #507.

## Toolchain and build

- Lean: `leanprover/lean4:v4.31.0`
- Dependencies: Lean standard library only
- Package: `experimental/lean/asymptotic_spine/`
- Build:

  ```text
  cd experimental/lean/asymptotic_spine
  lake build
  ```

The entry point `AsymptoticSpine.lean` imports
`AsymptoticSpine.ProfileEnvelope`.  The public top-level theorems have
`#print axioms` commands in the module.  The exact GF(11²) certificate has no
axiom dependencies; the remaining reports contain only the standard logical
axioms `propext`, `Classical.choice`, and `Quot.sound` (or a subset).

## Statement-to-declaration correspondence

| Source statement | Lean declaration(s) | Scope and status |
|---|---|---|
| Pigeonhole core of `thm:polynomial-obstruction`, equation (5.3): some quotient-profile fiber has size at least its ceiling average | `AsymptoticSpine.ceilDiv`, `ceilDiv_le_of_le_mul`, `listMax_mem_of_ne_nil`, `exists_fiber_ge_ceil` | Exact for any finite list keyed into `P>0` buckets; reuses the existing cleared `identity_prefix_floor` |
| Smallest audited complete-square profile in GF(11²) | `GF11SquareSupport`, `gf11SquareSupports`, `gf11SquarePrefix`, `gf11SquareFibres`, `gf11_square_profile_certificate`, `gf11_square_profile_floor` | Exact exhaustive `by decide` certificate: 210 distinct supports, fiber census `[20,19,...,19]`, and `ceil(210/11)=20` |
| `prop:collision-aware-lower`, equation (7.1), arithmetic core | `collision_aware_distinct_value_floor` | From explicit `L² <= M sumSq` and `d sumSq <= dL+kL(L-1)`, proves `ceil(Ld/(d+k(L-1))) <= M` |
| Grande Finale `thm:simple-pole-list-floor`, abstract MCA-facing form | `simple_pole_list_floor` | Adds `d=q-n>0` and the explicit interface `M <= badSlopes`; root counting, pole averaging, and value-to-bad-slope geometry remain hypotheses |
| Audit replication of the extension-field collision formula | `gf11_extension_collision_floor` | Exact `by decide` check at `q=11^4=14641`, `n=20`, `L=20`, `k=5`: the ceiling is 20 |
| Conditional identity-dominant compiler structure of `thm:frontier` | `ProfileCompilerInputs`, `profile_compiler_upper` | Every represented cell-payment, Sidon, RC, identity-dominance, and target-budget input is named and used to prove the upper agreement safe |
| First-safe agreement and radius bracket in `thm:frontier`, equation (1.2) | `IsFirstSafe`, `first_safe_bracket`, `profile_frontier_bracket` | Exact discrete bracket `a_- < a* <= a_+` and cleared radius bracket, conditional on antitonicity, the lower certificate, and the named compiler inputs |

## New paper mapping

The active paper was renamed to
`experimental/asymptotic_rs_mca_frontiers.tex` after this package was
started.  The audit-reference labels above remain the source of the task; the
following lines record the matching labels in the renamed paper.

| Formalized statement | Matching label in `asymptotic_rs_mca_frontiers.tex` |
|---|---|
| General attained prefix-fiber ceiling, `exists_fiber_ge_ceil` | `prop:exact-prefix-list`; the paper's complete-square application appears in `thm:smooth-quotient-obstruction` at `eq:polynomial-large-fiber` and `eq:polynomial-image-profile` |
| Exact GF(11²) support census, `gf11_square_profile_certificate` and `gf11_square_profile_floor` | No direct label; it is the smallest finite audit instance of the complete-square construction used in `thm:smooth-quotient-obstruction` |
| Collision Cauchy--Schwarz ceiling, `collision_aware_distinct_value_floor` | The cleared arithmetic step in the proof of `thm:collision-aware-pole` and `eq:collision-aware-pole`; pole selection and root geometry are not formalized |
| MCA-facing collision wrapper, `simple_pole_list_floor` | `thm:collision-aware-pole`; the identity-prefix composition is `cor:identity-prefix-floor` |
| GF(11⁴) numerical collision ceiling, `gf11_extension_collision_floor` | No direct label; it is a finite arithmetic instance of `eq:collision-aware-pole` |
| Named compiler inputs and safe upper bound, `ProfileCompilerInputs` and `profile_compiler_upper` | `def:profile-cell`, `def:profile-payment`, and `def:profile-complexity` supply the vocabulary; `def:sidon-paid-cell` and `hyp:ray-compiler` name assumed inputs.  The composed inequality is the finite skeleton of `thm:main-smooth-circle` / `eq:conditional-numerator` (compare `thm:exact-finite-profile-compiler`), not a formalization of those results.  `cor:intro-identity-frontier` is only the paper's unformalized identity-dominant specialization |
| First-safe and radius brackets, `IsFirstSafe`, `first_safe_bracket`, and `profile_frontier_bracket` | First-safe definition: `eq:intro-asymptotic-threshold`; cleared bracket counterpart: `thm:intro-asymptotic-rs-mca` and `eq:intro-threshold-bracket`.  Lean assumes the first-safe witness and proves neither its existence nor the asymptotic conclusion |

## GF(11²) certificate

For `p=11`, the obstruction has `n=20`, `a=8`, `w=2`, and `k=5`.
The square image is `D²=theta² F_11^x`, so a complete-square support is
encoded by an increasing four-subset of the ten labels `1,...,10`.  Its odd
locator coefficient vanishes and its first surviving coefficient is
`-theta² sum(C)`.  Multiplication by `-theta²` is a relabeling, so the Lean
key `sum(C) mod 11` has exactly the source fibers.

Lean enumerates the increasing subsets rather than accepting the audit census
as input.  It computes

```text
number of supports = 210
supports are Nodup  = true
eleven fiber sizes = [20,19,19,19,19,19,19,19,19,19,19]
maximum fiber       = 20
ceil(210 / 11)      = 20
```

This is an exact finite replication of the quotient-label calculation.  As the
source audit stresses, it is illustrative evidence for the obstruction family,
not a proof of the theorem's asymptotic entropy estimates.

## Collision interface

The stdlib module deliberately exposes the two arithmetic inputs:

```text
L * L <= M * sumSq
d * sumSq <= d * L + k * L * (L - 1)
```

The first is the Cauchy--Schwarz consequence of the value multiplicities and the
second is the cleared pair-collision budget after pole averaging.  The proof
scales, factors, cancels the positive `L`, and applies the ceiling lemma.  The
factor of two is already accounted for: unordered colliding pairs become
`k*L*(L-1)` in the second moment.

The Mathlib package `experimental/lean/grande_finale/` already proves the
Cauchy--Schwarz step from actual finite multiplicities in
`GrandeFinale.distinct_value_floor` and supplies
`GrandeFinale.nat_ceil_div_le`.  This new declaration is the stdlib-only,
paper-facing composition with all omitted polynomial geometry made explicit;
it does not claim novelty for those arithmetic kernels.

## Conditional frontier boundary

`ProfileCompilerInputs` does not use marker propositions that can be ignored.
Its fields are inequalities consumed by `profile_compiler_upper`:

- closed-ledger first-match coverage;
- payment of nonprimitive cells at their natural profile budgets;
- routed Sidon payment of the primitive intermediary, with the permitted RC
  loss absorbed into the printed compiler loss;
- RC from the actual primitive ray image to that paid intermediary;
- comparison of the component budgets with the profile envelope;
- identity dominance with an explicit loss;
- the final target-budget inequality.

`profile_frontier_bracket` combines that safe upper endpoint with a certified
unsafe lower endpoint and an explicitly characterized first safe agreement.
It proves only the discrete agreement/radius bracket.  It does not formalize or
claim the entropy crossing `g_T -> g*`, window uniformity, residual
higher-dimensional split-pencil payments, RC, or Sidon payment.

## Nonclaims

- The package does not formalize GF(11²) arithmetic, the cyclic-domain setup,
  two-to-one squaring, or the locator-coefficient subfield theorem; the finite
  certificate begins after the audited quotient-label reduction.
- It does not prove the pole root-count bound, select the low-collision pole, or
  construct the received MCA line.  Those facts are explicit interfaces of the
  abstract collision theorem.
- It does not formalize the radius interval and CA/MCA endpoint clauses of the
  full Grande Finale theorem.
- It does not discharge the paper's residual Sidon, ray-compiler, identity
  dominance, profile comparison, or target-budget hypotheses.
- It takes `IsFirstSafe` as the exact finite minimum interface; it does not
  construct the minimum from a nonempty safe set.
- It does not formalize the real-analytic binary-entropy crossing or make any
  unconditional asymptotic frontier claim.
