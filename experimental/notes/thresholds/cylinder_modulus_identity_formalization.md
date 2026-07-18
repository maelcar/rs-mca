# Cylinder modulus identity formalization

## Claim

For every natural depth `B`, let

```text
L = (3^B + 1) / 2.
```

Then Lean proves the subtraction-free identity

```text
2*L = 3^B + 1,
```

and hence the U1/V1 normalization `3^B = 2*L - 1`.

## Status

PROVED.

## Source audit

The exact source is U1/V1 in
`experimental/notes/thresholds/cylinder_renormalization.md`.  The packet was
produced at `c844abb1`, integrated on main at `764f1c02`, and critically
corrected at `02728b20`.  The correction exhibited nonzero twisted-coset cube
coefficients and narrowed the certificate claim to subgroup cylinders.  It
left the U1/V1 modulus normalization unchanged, so current main after
`02728b20` is the authority; the older experimental branch is not.

The source verifies `c=2L-1` for positive even depths through 64.  The Lean
definition `realizedImage B=(3^B+1)/2` satisfies the arithmetic identity for
all natural `B`, because `3^B` is odd.  Thus `B=0` and odd `B` are legitimate
arithmetic boundary cases, not extensions of the source's chart semantics.

The active thresholds paper at `856d8362` provides both the surrounding
PO3/PO4 interface and the SAT1 fence.  The frontiers paper at `4e3c4ee8`
provides PO3/PO4, but not SAT1.  Neither paper states U2/U3 or the cylinder
normalization as a standalone theorem.

## Lean correspondence

The declarations are in
`experimental/lean/cylinder_renormalization/CylinderRenormalization.lean`.

- `realizedImage_double` is the subtraction-free primary theorem.
- `modulus_identity_all` derives the printed normalization.
- `modulus_identity` preserves the former finite API and delegates every
  listed depth to `modulus_identity_all`.

The package README gives the complete source-section to Lean-name status map.

## Proof outline

Induction proves `3^B % 2 = 1`.  The natural-number division algorithm then
gives

```text
1 + 2*(3^B/2) = 3^B,
```

so `3^B+1 = 2*(3^B/2+1)`.  Exact division by two proves the additive identity;
the source's subtractive form follows without assuming positivity or evenness.

## Validation

From `experimental/lean/cylinder_renormalization`:

```bash
lake clean
lake build
```

From the repository root:

```bash
python3 experimental/scripts/verify_cylinder_modulus_identity.py --check
python3 experimental/scripts/verify_cylinder_modulus_identity.py --tamper-selftest --check
```

The first command is expected to end with `RESULT: PASS (1558/1558)`; the
second is expected to report `tamper-selftest: caught 4/4` and the same PASS
result.

## Scope and nonclaims

This packet formalizes only exact base-3 modulus arithmetic.  It does not
formalize U1's Parseval or wide-band estimates; U2 suffix structure; U3
trigonometric or polynomial cylinder renormalization; a general Vandermonde
identity; the slice-staircase/class-constancy lemma; subgroup cube-flatness; or
recursive certificate compression.  It does not restore twisted-coset
flatness, which the corrected source refutes; transfer U2/U3 to base 5; prove
admission; supply image-scale MI/MA or a direct Sidon payment; compile a
residual ray; compare the complete profile envelope; establish lower reserve;
close a deployed row or branch; or prove an MCA threshold, charge, deep-MCA
count, or Proximity Prize claim.
