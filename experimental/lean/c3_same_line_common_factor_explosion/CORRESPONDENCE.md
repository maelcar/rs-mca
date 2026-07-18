# C3 Same-Line Common-Factor Explosion Correspondence

Status:

- **PROVED** for the abstract two-stage ceiling pigeonhole kernel
  `C3SameLineCommonFactorExplosion.exists_nested_ceiling_fiber`.
- **STATEMENT TARGET** for the combined support-cell, common-factor, and
  extension-field same-line theorem
  `C3SameLineCommonFactorExplosion.c3_sameLine_commonFactorExplosion_target`.
  The latter declaration intentionally contains `sorry`.  This standalone
  package is not imported into the pinned `GrandeFinale.lean` root.

Source: `experimental/notes/audits/c3_same_line_common_factor_explosion.md`,
together with the exact prefix/list--line interfaces in
`experimental/asymptotic_rs_mca_frontiers.tex`.

## Statement map

| Route-cut component | Lean declaration |
| --- | --- |
| Nested inner/outer ceiling pigeonhole | `C3SameLineCommonFactorExplosion.exists_nested_ceiling_fiber` |
| Residual supports for a fixed planted core and prefix | `C3SameLineCommonFactorExplosion.residualPrefixCell` |
| Scalar-extended support-to-slope map | `C3SameLineCommonFactorExplosion.mappedSupportSlope` |
| Full finite same-line common-factor explosion | `C3SameLineCommonFactorExplosion.c3_sameLine_commonFactorExplosion_target` |

## Pinned Grande Finale APIs consumed

The standalone module imports only the pinned API file
`experimental/lean/grande_finale/GrandeFinale/ScalarExtensionListLine.lean`.
That file's import chain supplies the transitive APIs used by the target:

- `experimental/lean/grande_finale/GrandeFinale/SP.lean`;
- `experimental/lean/grande_finale/GrandeFinale/PrefixPigeonhole.lean`;
- `experimental/lean/grande_finale/GrandeFinale/ExactListLine.lean`;
- `experimental/lean/grande_finale/GrandeFinale/ExactPrefixRay.lean`;
- `experimental/lean/grande_finale/GrandeFinale/ExactPrefixRayUniqueness.lean`;
- `experimental/lean/grande_finale/GrandeFinale/SeparatingPole.lean`.

Their pinned scope maps are:

- `experimental/lean/grande_finale/PREFIX_PIGEONHOLE_CORRESPONDENCE.md`;
- `experimental/lean/grande_finale/EXACT_LIST_LINE_CORRESPONDENCE.md`;
- `experimental/lean/grande_finale/EXACT_PREFIX_RAY_CORRESPONDENCE.md`;
- `experimental/lean/grande_finale/EXACT_PREFIX_RAY_UNIQUENESS_CORRESPONDENCE.md`;
- `experimental/lean/grande_finale/SEPARATING_POLE_CORRESPONDENCE.md`;
- `experimental/lean/grande_finale/SCALAR_EXTENSION_LIST_LINE_CORRESPONDENCE.md`.

The package depends on those files through Lake.  It does not modify them or
add an import to the pinned Grande Finale package root.

## Proved kernel

Let `left` be a finite outer family, `right` a finite inner family, and
`values` a nonempty finite prefix-value set.  For a map

~~~text
f : left-type -> right-type -> value-type,
~~~

the proved theorem first applies `GrandeFinale.prefix_witness_maxfiber` to
each outer index.  It chooses one heavy inner-fiber value for that index and
then applies the same theorem to the resulting outer-index-to-value map.  It
therefore produces one value `z` and a subfamily `heavy` satisfying the
literal natural-ceiling bounds

~~~text
ceil(|left| / |values|) <= |heavy|,
ceil(|right| / |values|) <= |{r in right : f(a,r) = z}|
~~~

for every `a` in `heavy`.  The theorem makes no uniformity or asymptotic
assumption.

For the C3 specialization, `left` is the family of `b`-subsets of the left
domain block, `right` is the family of `r`-subsets of the disjoint residual
block, `values` is the full coefficient-prefix space, and

~~~text
f(T,R) = coefficientPrefix K m (locator (T union R)).
~~~

Thus the two denominators both become `|B|^(m-K)`.

## Existing exact interfaces consumed by the target

- `PrefixPigeonhole.coefficientPrefix`, `coefficientFiber`, and
  `prefixPolynomial` provide the literal locator-prefix fiber.
- `ExactPrefixRayUniqueness.listedPolynomial_mem_of_mem_coefficientFiber`
  places every selected support polynomial in the complete base list.
- `ExactPrefixRay.prefixPolynomial_agreementSet_eq_support` identifies its
  exact base-field agreement support.
- `ScalarExtensionListLine.extensionAgreementSet_map_eq_base` preserves that
  support after scalar extension.
- `ScalarExtensionListLine.exists_extensionPole_exact_listLine` supplies an
  off-domain pole, injectivity on the mapped complete list, and equality of
  its evaluation image with the ambient MCA-bad slope set.
- `ScalarExtensionListLine.prefixListedPolynomials_card_eq_coefficientFiber`
  identifies the complete list size with the coefficient-fiber size.
- `SP.locator_injective` reindexes mapped-list injectivity by supports.

The target uses the stronger prefix-independent budget

~~~text
|D| + (K-1) * choose(choose(|D|,m),2) < |F|.
~~~

This dominates the exact equation-(4.6) budget for whichever coefficient
fiber the nested pigeonhole step selects.

## Scope boundaries

The proved theorem is only the abstract nested pigeonhole kernel.  The final
target still requires a Lean proof of the disjoint-block support
specialization, locator divisibility, the bound from the full support census
to the selected prefix-list size, and the support-indexed composition with
the scalar-extension list--line theorem.

The target does not prove a subexponential C3 census, classify algebraically
canonical planted factors, or close the C3 upper-payment hypothesis.  It
records the opposite route cut: unrestricted actual support locators can
carry many planted common factors on one exact received line.

`ExactPrefixRayUniqueness.existsUnique_exactLineWitness` is a same-field
theorem.  This target does not assert extension-field occupancy one; exact
bad-slope image and support preservation are the interfaces used here.

## Verification

With the pinned Lean/Mathlib checkout and matching precompiled cache, from
this package directory run:

~~~text
lake env lean C3SameLineCommonFactorExplosion.lean
~~~

The axiom audit for `exists_nested_ceiling_fiber` reports only Lean's standard
`propext`, `Classical.choice`, and `Quot.sound`.  The compiler also reports the
intentional `sorry` in `c3_sameLine_commonFactorExplosion_target`; accordingly
the module is a documented statement target rather than a certified package
root theorem.
