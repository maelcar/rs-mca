# Lean correspondence: frontiers staircase and deep-regime core

## Status

PROVED for the exact identity-scale arithmetic, integer-staircase order theory,
and post-incidence coordinate-ledger double count.  CONDITIONAL for the
source-level deep-regime upper bound: the finite-field/minimum-distance recovery
and semantic root construction are named inputs and are not claimed by this
packet.

## Source

The source is `experimental/asymptotic_rs_mca_frontiers.tex`, especially
equation (1.2), `def:integer-staircase-detail`, and
`thm:deep-regime-upper`.

## Statement-to-declaration map

| TeX statement or proof step | Lean declaration | Status |
| --- | --- | --- |
| Identity raw scale at `a=K+w`, `binom(n,a)|B|^{-w}` | `AsymptoticSpine.IdentityRawScale`, `.numerator`, `.denominator`, `.ratio` | PROVED exact definition |
| In-range/nonzero well-definedness of that raw scale | `IdentityRawScale.ratio_wellDefined` | PROVED |
| Integer agreement grid `{k+1,...,n}` and antitone MCA numerator | `AsymptoticSpine.FrontiersStaircase`, `.inGrid`, `.toCore` | PROVED interface |
| Safety is upward closed | `FrontiersStaircase.safe_up` | PROVED |
| Every nonempty safe grid has a unique first-safe threshold | `FrontiersStaircase.exists_firstSafe_of_safe`, `.threshold_exists_iff_top_safe`, `.firstSafe_unique`, `.firstSafe_spec_of_top_safe` | PROVED |
| Target-budget monotonicity of agreement/radius frontiers | `FrontiersStaircase.firstSafe_antitone_budget`, `.closedRadius_monotone_budget` | PROVED |
| Adjacent unsafe/safe staircase certificate | `FrontiersStaircase.adjacent_isFirstSafe` | PROVED |
| Dense branch: every ledger row consumes at least `t-r` distinct coordinates | `TransverseRootCertificate`, `transverse_root_double_count` | PROVED from abstract ledger data |
| Arithmetic `z(t-r) <= t`, `r<t` implies `z<=r+1` | `card_le_radius_succ_of_mul_gap_le` | PROVED |
| Sparse/tangent branch bounds a supplied injective coordinate ledger by `r` | `TangentRootCertificate`, `tangent_badCount_le` | PROVED from abstract ledger data |
| Recovered-pair dichotomy | `DeepPairCertificate`, `deep_pair_badCount_le` | PROVED |
| `3(n-a)<=d-1` and exhaustive received-pair maximum imply `B_C^MCA(a)<=n-a+1` | `deep_regime_upper` | CONDITIONAL on the named `incidenceLedger` producer |
| Truncated versus strict deep-range convention | `deep_range_iff_lt` | PROVED for `d>0` |

The exact dense and tangent ledger smoke tests are `denseRootToy` /
`dense_root_toy_exact` and `tangentRootToy` /
`tangent_root_toy_exact`.

## Named boundary

`deep_regime_upper` does not claim the code geometry.  Its inputs include an
exhaustive finite received-pair enumeration and an `incidenceLedger` function
producing one of
the following for every pair:

- a transverse root ledger whose pooled root coordinates are duplicate-free;
- a tangent injective coordinate ledger.

The missing link is the two-slope linear-code recovery from
`3(n-a)<=d-1`, together with the affine-coordinate root equations and the
support-wise nontriviality argument that construct these ledgers.  The Lean
certificate types contain natural-number coordinates and injectivity data; they
do not themselves contain slopes, error values, or vanishing equations.  That
semantic link is the natural consumer of a later syndrome-line formalization.
Until it is supplied, this packet certifies the post-incidence combinatorial
core but not the unconditional finite-field theorem by itself.

The MCA witness scheme and the row-sequence asymptotic bracket are outside this
packet.  No Fourier, first-match-atlas, Sidon, profile-envelope, or ray-compiler
hypothesis is used here.

## Build and trust audit

From `experimental/lean/asymptotic_spine/`:

```text
lake build
```

The build is green on Lean 4.31.0.  The package has a local stdlib-only
dependency on `experimental/lean/staircase_logic/`, reusing its audited
staircase search instead of duplicating it.  Every theorem declaration has a
`#print axioms` line.  The reported dependencies are limited to Lean's standard
`propext`, `Quot.sound`, and `Classical.choice`.  There is no `sorryAx`, `sorry`,
`admit`, `native_decide`, or added axiom.
