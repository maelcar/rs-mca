# Lean correspondence: effective prefix closure and the A6 ray route

## Status

PROVED for the exact finite routing lemmas after the displayed semantic
certificates are supplied.  CONDITIONAL for their instantiation as the full
shallow-prefix theorem in the frontiers paper: the finite-field Newton chart,
the RS noncommon-support assignment, the subexponential effective-span bound,
and the profile-envelope comparison remain explicit inputs.

## Source

The source is `experimental/asymptotic_rs_mca_frontiers.tex`, especially:

- the depth-prefix definition near equation (1.5);
- condition `(A6)` in `def:admissible-sequence`;
- `lem:effective-span-fourier` and its translated fiber `(EF2)`;
- `thm:small-effective-dual-closure`, in particular `(SE2)`;
- `hyp:ray-compiler` and its direct `(RC)` branch;
- `lem:newton-equivalence`;
- `lem:residual-monotonicity`;
- the merged `ProfileEnvelope.ProfileCompilerInputs` Lean consumer.

The Lean module is
`experimental/lean/asymptotic_spine/AsymptoticSpine/EffectiveClosure.lean`.

## Statement-to-declaration map

| Frontiers-paper step | Lean declaration | Status |
| --- | --- | --- |
| A depth-labelled raw locator-prefix map | `AsymptoticSpine.DepthPrefix` | PROVED interface |
| Effective syndrome coordinates are carried to raw prefix coordinates by the based Newton/affine map | `PrefixFiberBridge` | EXPLICIT INPUT (`toPrefix_injective`, `compatible`) |
| The full effective syndrome fiber at `z` equals the full prefix class at `toPrefix z` | `syndromeFiber_eq_depthPrefixChart` | PROVED from the bridge |
| A first-match residual cannot enlarge a fixed syndrome fiber | `residualSyndromeFiber_sublist`, `residualSyndromeFiber_length_le` | PROVED |
| A routed residual chart contained in a full prefix class is no larger than the corresponding full syndrome fiber | `residualChart_length_le_syndromeFiber` | PROVED |
| One chosen noncommon support per distinct slope gives `(SE2)` | `SE2Certificate`, `se2_support_injection` | PROVED from explicit support assignment |
| A residual prefix-chart slope cell has size at most the full-slice support mass | `se2_residualChart_le_fullSlice` | PROVED |
| `|Z|<=M`, `M<=L*avg`, `L<=A_eff`, and `A_eff<=loss` imply `|Z|<=loss*(1+avg)` | `se2_to_directRC` | PROVED |
| The full reindexed residual chain supplies the direct `(RC)` branch | `prefixResidualClosure_to_directRC` | PROVED from named inputs |
| That direct `(RC)` branch supplies the `(RC)` disjunct of `(A6)` | `prefixResidualClosure_to_A6_via_RC` | PROVED |
| The closure route fills the integrated compiler `rayCompiler` field | `profileCompilerInputs_of_prefixResidualClosure` | PROVED; every other compiler field remains explicit |
| The existing profile-envelope compiler consumes that field | `profileCompilerUpper_of_prefixResidualClosure` | CONDITIONAL on the other named compiler inputs |

## Scope guard

The equality theorem concerns the **full raw prefix class**.  The paper's
balanced-core chart has additional common-factor, quotient, planted, rank, and
first-match removals.  Such a routed chart is therefore represented only as a
sublist of the full prefix class unless a separate fullness theorem is supplied.
The module deliberately uses `depthPrefixChart`, not `BalancedCoreChart`, for
the equality statement.

The effective coordinate `z` in `(EF2)` is based/translated, whereas the raw
locator prefix is an uncentered coefficient vector.  `PrefixFiberBridge.toPrefix`
records this affine translation together with the triangular Newton coordinate
change.  Injectivity is a field-specific semantic input.  Instantiating it with
locator coefficients and power sums additionally requires a fixed support size
and `R < char(B)`; the paper also chooses a base support, so its effective-span
instance is nonempty.  The generic Lean theorem keeps the empty case valid and
prevents the unsafe same-label assertion "fiber `z` = chart `z`".

`SE2Certificate.chosen_sublist` is the other semantic boundary.  It records the
output of the RS fact that each first-match slope can be assigned a noncommon
support and one such support cannot serve two distinct slopes.  The certificate
does not itself contain parity-check columns, received words, error values, or a
proof of that RS incidence statement.

Finally, the exact `Nat` arithmetic uses a printed integral `average` satisfying
`M <= L*average` and a finite `loss` satisfying `A_eff <= loss`.  Promoting this
to the paper's asymptotic direct bound still requires the uniform shallow-prefix
hypothesis `log A_eff=o(|T|)` and the active-size comparison.  The module now
constructs the merged `ProfileCompilerInputs` record and invokes its upper
compiler, but atlas coverage, natural-profile payment, Sidon-budget absorption,
envelope dominance, and the target inequality remain explicit hypotheses.  No
MI, MA, PF, deep-prefix cancellation, unrestricted balanced-core ray compiler,
or full high-kappa theorem is claimed here.

## Build and trust audit

From `experimental/lean/asymptotic_spine/`:

```text
lake build
```

The package is stdlib-only.  Every theorem in the module has a `#print axioms`
audit.  The reported dependencies are limited to Lean's standard `propext`,
`Quot.sound`, and `Classical.choice`; there is no `sorryAx`, `sorry`, `admit`,
`native_decide`, or added axiom.
