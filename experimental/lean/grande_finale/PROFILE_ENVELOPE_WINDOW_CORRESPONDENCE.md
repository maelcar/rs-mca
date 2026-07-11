# `GrandeFinale.ProfileEnvelopeWindow` correspondence

## Status

`GrandeFinale/ProfileEnvelopeWindow.lean` proves the exact rational exponent
algebra for comparing the identity exponent

```text
max(0, h - s)
```

with each actual complete-fiber folding `(c, lambda)` having exponent

```text
(h - lambda*s) / c.
```

For one folding it proves the two closed safe rays and their complementary
strict open failure band.  For a finite row it proves that identity dominance
is the intersection of the safe windows of the row's actual `(c, lambda)`
pairs, equivalently that failure is the union of their open bands.  These are
`PROVED` Lean statements over `ℚ`.

The extraction of these exponents from the manuscript, the identification of
all actual row foldings, and the passage from exponent dominance to the full
profile-envelope or frontier statements remain `CONDITIONAL`/outside this
module.

## Manuscript correspondence

The source manuscript is `experimental/asymptotic_rs_mca_frontiers.tex`; this
formalization does not edit it.

| Lean object or result | Manuscript source | Correspondence status |
|---|---|---|
| `identityExponent h s = max 0 (h-s)` | `eq:target-entropy`, normalized per symbol, together with the exponent-zero universal/deep terms in `eq:profile-envelope` | Algebraic model only; normalization and Stirling extraction are not formalized here |
| `foldingExponent h s c lambda = (h-lambda*s)/c` | normalized per-symbol form of QR8 (`eq:qr-comparison-general`) in `prop:identity-quotient-comparison`; at `s=h`, equivalently QR9 (`eq:qr-comparison-crossing`) | Formula is represented exactly; QR6/QR8/QR9 extraction is not proved in Lean |
| `dominates_iff_windows` | `Dominates` iff `s <= kappaLow c lambda * h` or `kappaHigh lambda * h <= s` | `PROVED` |
| `identity_lt_folding_iff_failureBand` | strict complement of that comparison; `thm:smooth-quotient-obstruction` supplies the manuscript's `(c,lambda)=(2,1/2)`, `s=h` instance | `PROVED` over `ℚ`; no asymptotic obstruction theorem is reproved |
| `profileIdentityDominant_iff_forall_folding` | the “all quotient subfields” quantifier in `def:admissible-sequence` (A7) | `PROVED` for the supplied finite family; A7 and family exhaustiveness are not proved |
| `profileIdentityDominant_iff_avoidsFailureBandUnion` | corrected per-folding intersection/union form of the identity-window criterion | `PROVED` for the supplied finite family |
| `zeroTarget_excess_eq`, `zeroTarget_mem_failureBand` | QR9 at the crossing; compare `thm:smooth-quotient-obstruction` | `PROVED` rational algebra |
| no-field-drop results (`fieldRatio = 1`) | sufficient exponent-level regime relevant to `cor:intro-identity-frontier` | `PROVED` at exponent level only |
| two-folding example `(2,1/5)`, `(3,1/10)` at `s=5h` | public correction audit for the earlier single-pair reduction; not a manuscript theorem | Source-audit arithmetic example; the module preserves the pairs through its finite-family API but does not include a standalone regression declaration |
| full target/frontier conclusion | `cor:intro-identity-frontier`, `eq:target-entropy`, and `cor:frontier-final` | `CONDITIONAL`; not a theorem of this module |

Here `lambda` is a rational field-ratio parameter.  Its mathematical
interpretation as `log |B_c| / log |B|` is manuscript-side input, not a Lean
construction in this module.  The shorthand “identity-dominance window” is
descriptive; `(IDW)` is not a manuscript label.

## Declaration map

| Declaration | Lean content | Status |
|---|---|---|
| `identityExponent`, `foldingExponent` | Exact rational exponent functions | Definition |
| `kappaLow`, `kappaHigh` | `(c-1)/(c-lambda)` and `1/lambda` | Definition |
| `Dominates`, `FailureBand` | Weak exponent dominance and strict failure | Definition |
| `dominates_iff_windows` | `Dominates` iff `s <= kappaLow c lambda * h` or `kappaHigh lambda * h <= s` | `PROVED` |
| `identity_lt_folding_iff_failureBand` | Strict folding excess iff the crossing lies in the open band | `PROVED` |
| `zeroTarget_excess_eq` | At `s=h`, excess is `((1-lambda)/c)*h` | `PROVED` |
| `zeroTarget_mem_failureBand` | If `h>0` and `0<lambda<1`, then `s=h` lies strictly in the band | `PROVED` |
| `CompleteFiberFolding` and its exponent/window predicates | Keeps each actual degree and field ratio as one indivisible pair | Definition |
| `CompleteFiberFolding.identityDominant_iff_inWindow` | Concrete single-folding closed-window theorem | `PROVED` |
| `CompleteFiberFolding.identity_lt_exponent_iff_inFailureBand` | Concrete single-folding strict-failure theorem | `PROVED` |
| `CompleteFiberFolding.inWindow_iff_not_inFailureBand` | Closed safe rays are exactly the complement of the open band | `PROVED` |
| `profileIdentityDominant_iff_forall_folding` | Finite-row dominance iff every actual folding passes its own window | `PROVED` |
| `mem_failureBandUnion_iff`, `inEveryFoldingWindow_iff_avoidsFailureBandUnion` | Membership in the union is witnessed by an actual row folding; avoiding it is the window intersection | `PROVED` |
| `profileIdentityDominant_iff_avoidsFailureBandUnion` | Finite-row dominance iff the crossing avoids the union of actual failure bands | `PROVED` |
| `CompleteFiberFolding.identityDominant_of_fieldRatio_eq_one`, `profileIdentityDominant_of_all_fieldRatio_eq_one` | No field drop implies exponent-level global dominance | `PROVED` |
| concrete zero-target specializations | Exact excess and strict failure for a supplied folding | `PROVED` |
| `profileIdentityDominant_at_zeroTarget_iff_all_fieldRatio_eq_one` | At `h>0`, a valid finite row is dominant at `s=h` iff every carried folding has `fieldRatio = 1` | `PROVED` |

## Endpoint and pairing conventions

For `h >= 0`, `c >= 2`, and `0 < lambda <= 1`, one folding is safe exactly on
the closed rays

```text
s <= ((c-1)/(c-lambda))*h    or    (1/lambda)*h <= s.
```

It fails exactly on the open interval

```text
((c-1)/(c-lambda))*h < s < (1/lambda)*h.
```

Thus equality at either endpoint is safe.  When `lambda=1`, both endpoints are
`h`; the open failure band is empty, not a singleton, and the two closed rays
cover every `s`.

Finite rows retain the actual `(c,lambda)` pairs.  The degree from one folding
must never be combined with the field ratio from another.  The exact regression
pair makes this load-bearing: at `h>0` and `s=5h`, `(2,1/5)` is safe at its
closed upper endpoint, while `(3,1/10)` fails because

```text
(20/29)*h < 5h < 10h.
```

Therefore checking only the first pair does not establish row dominance; the
finite-family intersection is essential.

## Boundaries and nonclaims

This module does **not** prove:

- QR6, QR8, QR9, Stirling asymptotics, entropy normalization, or the derivation
  of either exponent from a code family;
- that a supplied `CompleteFiberFolding` is geometrically realized, or that a
  supplied finite row exhausts all quotient/Chebyshev/profile competitors;
- (A2), (A4), MI, MA, Sidon/BSG payment, RC, or (A7) from
  `def:admissible-sequence`;
- the actual profile-envelope maximum in `eq:profile-envelope` or its
  comparison with the target;
- the bridge to `AsymptoticSpine.ProfileEnvelope.ProfileCompilerInputs`, its
  finite `identityDominance` inequality, or any asymptotic `e^{o(n)}` bound;
- the target statement `tau >= max_i tau0_i`;
- that a prime image field forces every supplied ratio to equal one;
- `cor:intro-identity-frontier`, `cor:frontier-final`, a deployed finite-row
  bound, or the full RS--MCA threshold theorem.

## Lineage

The exponent formulas and crossing interpretation come from
`prop:identity-quotient-comparison` (QR6--QR9), with the concrete field-drop
obstruction recorded by `thm:smooth-quotient-obstruction`.  The finite-family
form follows the corrected promotion audit in
[PR #606](https://github.com/przchojecki/rs-mca/pull/606)
(`identity_window_promotion_audit.md`): it replaces the
superseded single-pair reduction in
`experimental/notes/thresholds/envelope_identity_window.md` by an intersection
over actual foldings, or equivalently a union of their failure bands.

The module is complementary to
`AsymptoticSpine/ProfileEnvelope.lean`: that file supplies a finite compiler
interface, while this file isolates the corrected rational window algebra.  No
TeX statement is changed or promoted by this formalization.
