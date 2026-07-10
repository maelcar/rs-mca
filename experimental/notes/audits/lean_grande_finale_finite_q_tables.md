# Grande Finale Lean finite-Q correspondence packet

Status: **FORMALIZATION / AUDIT**.

This packet follows the 112-declaration correspondence audit in
`lean_grande_finale_correspondence_audit.md`.  It closes two mechanical gaps:

1. it pins the four finite rows printed in `prop:q-exact-target` and
   `prop:q-moment-order-floor`; and
2. it makes the Lean Q-to-SP statement retain the exact diagonal subtraction
   printed in `thm:q-implies-sp`.

It does **not** prove the row-sharp Q atom or an adjacent safe row.

## Finite table module

`GrandeFinale/QFiniteTables.lean` records the rows in manuscript order:

| row | base | `w` | ceiling average | `B*` | `floor(10^4 B*/ceil(avg))` | pinned bit margin | pinned real-average floor | ceiling-average floor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| KoalaBear MCA | 2130706433 | 67471 | 57198030366 | 274980728111395087 | 48075209295 | 22.196861707683 | 94196 | 94196 |
| KoalaBear list | 2130706433 | 67471 | 65065153468 | 274980728111395087 | 42262365253 | 22.010942080645 | 94991 | 94991 |
| Mersenne-31 MCA | 2147483647 | 67447 | 1752700 | 16777215 | 95722 | 3.258852879362 | 641593 | 641594 |
| Mersenne-31 list | 2147483647 | 67447 | 1993678 | 16777215 | 84152 | 3.072999568105 | 680397 | 680397 |

The ratio column is an integer scaled by `10^4`; for example `95722` means
`9.5722`.  The module proves, by evaluated integer arithmetic:

- `row_names` and `base_fields`: row order and field assignment;
- `exact_target_inputs`: the four `(w, ceiling average, B*)` triples;
- `average_ceil_le_budget`: each displayed ceiling fits its full budget;
- `exact_ratio_truncations`: the four exact four-decimal budget-ratio
  truncations; and
- `printed_margin_rounding`: the pinned twelve-decimal margins round to the
  four decimals printed in the manuscript.

`moment_order_floors`, `ceiling_average_moment_order_floors`, and
`convention_sensitive_rows` lock the audited convention choice.  They expose
the only convention-sensitive entry: Mersenne-31 MCA is `641593` with the
manuscript's real-average convention and `641594` if the ceiling average is
substituted first.

The decimal and floor pins come from the existing finite-Q recomputation in
`experimental/notes/thresholds/cap25_v13_q_moment_floor_reconciliation.md` and
its deterministic checker
`experimental/scripts/verify_q_moment_order_floor_reconciliation.py`; this
module packages their correspondence facts for Lean consumers.  The checker
now pins the four high-precision real-average margins at twelve decimals and
tamper-checks each pin.

### Exact proof boundary

The average ceilings, twelve-decimal bit margins, and moment-order floors are
pinned correspondence data.  Lean checks their transcription and the integer
relations above.  It does not derive them from `Real.log`, evaluate
`binom(2^21, a_+)`, or prove that a Q fiber obeys the displayed budget.  In
particular, `moment_order_floors` is a certified table identity, not a formal
proof of the logarithmic floor calculation in `prop:q-moment-order-floor`.

## Exact Q-to-SP reconciliation

Write

```text
Nsub = binom(n,m),    Bw = |B|^w,
Fbar = Nsub / Bw,     RQ = kappa.
```

The manuscript's `thm:q-implies-sp` gives

```text
(kappa - 1/Fbar) * Nsub * Fbar
  = kappa * Nsub^2 / Bw - Nsub.
```

`SP.sp_from_q` now concludes exactly the right-hand side, retaining `-Nsub`.
After multiplication by `Bw/Nsub^2`, `SP.sp_from_q_normalized` concludes

```text
RQ - Bw/Nsub = kappa - 1/Fbar.
```

Thus the Lean density normalization and the manuscript normalization agree
term for term.  The section and theorem docstrings now cite the real label
`thm:q-implies-sp`, rather than the former phantom Q/SP labels.

## Build and trust check

The package default target now includes both `GrandeFinale.lean` and every
child module.  Under Lean `v4.28.0` and the exact manifest-pinned Mathlib
revision `8f9d9cff6bd728b17a24e163c9402775d9e6a365`, using the matching
precompiled Mathlib cache, the full build reported:

```text
Build completed successfully (8034 jobs).
```

The packet contains no `sorry`, `admit`, or custom `axiom`.  The controlled
build checks the new native-decide certificates and both strengthened SP
statements.  Representative `#print axioms` results are:

- `exact_ratio_truncations`, `moment_order_floors`, and
  `convention_sensitive_rows` depend on `propext`, `Lean.ofReduceBool`, and
  `Lean.trustCompiler`, the expected `native_decide` trust boundary; and
- `sp_from_q` and `sp_from_q_normalized` depend on `propext`,
  `Classical.choice`, and `Quot.sound` only.

No packet theorem introduces a project-specific axiom.

## Nonclaims

- No row-sharp Q max-fiber theorem is proved.
- No complete finite upper ledger or adjacent safe row is proved.
- No transcendental logarithm or enormous binomial evaluation is formalized.
- No asymptotic-spine claim is added or changed.
