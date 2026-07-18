# Heavy-fiber saturation bridge formalization

This standalone Lean 4.14 package formalizes the arithmetic anchors and the
logical saturation-forcing layer of
`experimental/notes/thresholds/heavy_fiber_planted_emission.md`.  The source
packet is PR #735 at `f94d8706`; its prefix-fiber admissibility producer is
PR #717 at `ae5f1f1e`, and its structured-emission consumer is PR #716 at
`bc6280c5`.

## Theorem map

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| Setup: Pascal binomial coefficient and twin-count arithmetic | `binom`, `twinCount` | DEFINITIONS |
| THM 2a: binomial twin-count arithmetic values | `twin_B2`, `twin_B4`, `twin_B6`, `twin_B8`, `twin_B10` | PROVED, arithmetic anchors; fiber cardinality not formalized |
| THM 2a: finite `B - 2` arithmetic values | `twin_saturation_B4`, `twin_saturation_B8` | PROVED, arithmetic anchors; intersection semantics not formalized |
| THM 2a: general involution-planted structural theorem | none | NOT FORMALIZED IN LEAN |
| Corollary 2b: exponential heaviness on the stronger subclass | none | NOT FORMALIZED IN LEAN |
| THM 1: recursive ceiling function | `cwRec`, `cwBound` | DEFINITIONS; Johnson correctness not formalized |
| THM 1: finite `cwBound` values and drop | `cw_12_8_4`, `cw_12_6_3`, `cw_9_6_3`, `ceiling_strict_drop_n12_a4`, `heavy_exceeds_nonsat_ceiling` | PROVED, arithmetic anchors; code-bound semantics not formalized |
| THM 1: list-level intersection helpers | `interLen`, `maxIntersect` | DEFINITIONS; set and constant-weight semantics not encoded |
| THM 1: former unrestricted list target | `old_saturation_target_counterexample` | COUNTEREXAMPLE |
| THM 1: saturation from a non-saturating ceiling | `saturation_forcing_of_nonsaturating_ceiling` | PROVED under explicit ceiling hypothesis |
| THM 1: full constant-weight Johnson saturation theorem | none | NOT FORMALIZED IN LEAN; the logical bridge above imports its ceiling |
| Depth-two involution-shattering counterexample | none | VERIFIER-ONLY; NOT FORMALIZED IN LEAN |
| THM 3: finite list power-sum function and coset identities | `powerSumMod`, `coset_p7_d2`, `coset_p13_d3_p1`, `coset_p13_d3_p2`, `coset_p13_d4_p1`, `coset_p13_d4_p2`, `coset_p13_d4_p3` | DEFINITION plus PROVED arithmetic anchors; coset-family semantics not formalized |
| THM 3: general multiplicative-folding family | none | NOT FORMALIZED IN LEAN |
| THM 3 census: divisor-sum function and values | `sigmaNat`, `sigma_p7`, `sigma_p13` | DEFINITION plus PROVED arithmetic anchors; census theorem not formalized |
| Exhaustive prefix-fiber census and five-precursor discriminator | none | VERIFIER-ONLY; NOT FORMALIZED IN LEAN |

## Statement repair

The source theorem concerns a family of distinct `a`-subsets of an
`n`-element universe and imports a Johnson upper bound for every
non-saturating family.  The former Lean target represented supports as
arbitrary `List Nat` values and assumed neither those set semantics nor the
non-saturating ceiling.  It was false: at `(n,a,R) = (12,4,2)`, four empty
supports have maximum intersection `0`, exceed the computed ceiling `3`, and
do not attain the claimed saturation value `1`.

The repaired declaration takes the actual logical input explicitly:

```text
maxIntersect fibers < a - R - 1
  -> fibers.length <= cwBound n (2 * (R + 2)) a.
```

Together with `hbound`, the explicit max-intersection upper bound, and strict
heaviness, this implies equality by antisymmetry.  Supplying that ceiling for
constant-weight codes remains a separate formalization task.

## Scope

The general theorem proves only the contrapositive order bridge.  It does not
encode finite-set supports, distinctness, constant weight, containment in
`Fin n`, or correctness or sharpness of `cwBound` as a Johnson bound.  The
finite `native_decide` results do not establish the general constant-weight
theorem.  The package also does not prove exhaustive semantic emission, a
subexponential atlas census, a ray compiler or payment, the semantic-or-signed
dichotomy, image-scale MI/MA, direct Sidon payment, profile-envelope comparison,
lower reserve, MCA threshold, deployed-row closure, or a Proximity Prize claim.

Build with the pinned toolchain:

```text
lake build
```
