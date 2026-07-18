# Rank-one emission arithmetic formalization

This standalone Lean 4.14 package formalizes the arithmetic shadow of
`experimental/notes/thresholds/rank_one_emission_arithmetic.md` at integrated
source snapshot `168e9ba0`.  The original source packet is #818 at `03fa2958`;
its upstream twisted-coset product-law producer is #816 at `98e2a620`.

## Theorem map

| Source section / label | Lean declaration | Status |
| --- | --- | --- |
| Setup: running-product binomial coefficient | `binom` | DEFINITION |
| Setup: realized `B = 6` level fiber | `wtil6` | DEFINITION |
| Setup: width-indexed balanced-ternary support count | `s3` | DEFINITION |
| Lemma R(a): bounded complement kernel | `s3_pow_sub` | PROVED, all depths |
| Lemma R(a): `s3(-a) = s3(a)` on canonical residues | `pairing_symmetry_all` | PROVED, all depths |
| Lemma R(a): arbitrary natural representative, normalized modulo `3^k` | `pairing_symmetry_mod` | PROVED, all depths |
| Former finite negation scan | `pairing_symmetry` | PROVED from the all-depth theorem; compatibility API |
| Lemma R(a): number of proper pairs | `pairing_census` | PROVED, depths 1--7 only |
| Theorem E4(a): depth-one digit counts and cleared `G` identity | `depth1_digit_counts`, `depth1_G_integer` | PROVED, finite rows |
| Theorem E5: resonant all-ones count and prefix congruence | `resonant_all_ones`, `resonant_maximally_twisted` | PROVED, finite rows |
| Shared finite arithmetic anchors | `class_pins` | PROVED, finite row |

## Exact statement and normalization

For `a < 3^k`, the source-shaped theorem is

```text
s3 ((3^k - a) % 3^k) k = s3 a k.
```

For an arbitrary natural representative, `a` must be reduced before natural
subtraction:

```text
s3 ((3^k - (a % 3^k)) % 3^k) k = s3 (a % 3^k) k.
```

The unrestricted expression `s3 (3^k - a) k = s3 a k` is false because `Nat`
subtraction saturates.  At `k = 1`, `a = 4`, its two sides are `0` and `1`.

The induction behind `s3_pow_sub` splits `a % 3` into `0`, `1`, and `2`.  The
digit-`2` branch carries into the next balanced trit and invokes the induction
hypothesis at `a / 3 + 1`.

## Scope

The new theorems prove equality of the number of nonzero width-`k`
balanced-ternary digits.  They do not construct the digit vector or prove its
uniqueness, periodicity of unnormalized `s3`, the complex finite-sum pairing,
cosine folding, or reality of `G`.  They also do not prove Lemma R(b,c), any
cube-spectrum or emission payment, soundness or admission, image-scale MI/MA,
a Sidon payment, a residual compiler, a profile-envelope comparison, a lower
reserve, an MCA threshold, or a Proximity Prize claim.

Build with the pinned toolchain:

```text
lake build
```
