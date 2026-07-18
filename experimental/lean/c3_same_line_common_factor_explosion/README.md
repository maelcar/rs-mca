# C3 Same-Line Common-Factor Explosion Lean Companion

This standalone package is the packet-local Lean companion to
`experimental/notes/audits/c3_same_line_common_factor_explosion.md`.  It
depends on the pinned Grande Finale API but does not modify files under
`experimental/lean/grande_finale/` and is not imported into that package's
`GrandeFinale.lean` root.

## Contents and scope

- `C3SameLineCommonFactorExplosion.lean` proves the abstract two-stage
  ceiling-pigeonhole kernel
  `C3SameLineCommonFactorExplosion.exists_nested_ceiling_fiber`.
- The same module records the full support-cell, locator-divisibility, and
  scalar-extension composition as
  `C3SameLineCommonFactorExplosion.c3_sameLine_commonFactorExplosion_target`.
  That theorem intentionally contains `sorry` and remains a statement target.
- `CORRESPONDENCE.md` maps both declarations to the research packet and cites
  the pinned Grande Finale API and correspondence files they consume.

The proved kernel and the full target have distinct proof status.  This
package does not claim C3 payment or certify the complete route-cut
composition.

## Focused verification

Use the pinned Lean/Mathlib cache.  From this directory, check only the
packet-local module:

~~~sh
lake env lean C3SameLineCommonFactorExplosion.lean
~~~

The command should print the standard axiom report for the proved kernel and
an intentional `sorry` warning for the full statement target.
