# Opus 4.8 F1 Balanced-CRT Audit

Route verdict: `AUDIT` / `EXACT_NEW_WALL`

Formal status tags: `AUDIT`, `CONDITIONAL`, `PROVED` for narrow subclaims only.

Raw input:

- `raw/20260617_OPUS48_F1_BALANCED_CRT_RAW_1.md`

## Codex Audit

This answer is useful but not bankable wholesale. It gives a promising CRT/incidence lens for the balanced-denominator F1 wall, but several headline claims are stronger than what is actually justified.

## Bankable Narrow Content

1. **CRT coordinate lens for split balanced denominators.** If `E` splits over `F` as

```text
E(X)=prod_i (X-alpha_i)
```

with roots nonconjugate to the base field, then `F[X]/(E)` is naturally coordinatized by evaluations at the `alpha_i`. A residue-line condition becomes a collinearity/incidence problem for vectors

```text
(L_S(alpha_1), ..., L_S(alpha_t)).
```

This is a useful lens for the balanced wall.

2. **Conjugate-paired denominators are not genuinely new when fully paired.** If the root set of `E` is Frobenius-stable, then `E in B[X]`, and subfield-confinement logic applies. Fully conjugate-paired products are not the extension-only danger.

3. **The next wall remains balanced extension denominators.** The answer reinforces the prior residual-slack audit: after unbalanced denominators reduce to a residual-list problem, the live F1 target is `t approx sigma`, `E in F[X]\B[X]`.

## Problems / Overclaims

1. **Theorem 1 is too narrow for `Lambda_NC`.** The line-incidence formula using

```text
I_E = { [L_S]_E : |S|=a }
```

is valid for the special monic-degree-`a` anchor where the interpolant on `S` is `w-L_S`. It is not automatically a formula for arbitrary anchor words `w:D->F` in `def:residue`, and therefore it does not characterize the full maximum `Lambda_NC_{sigma,delta}` without extra argument.

2. **The conjugate-pairing dichotomy is false as stated.** It is true that a fully Frobenius-stable root set gives `E in B[X]`. But a genuinely extension polynomial may contain partial conjugate factors, e.g. a base factor times an unpaired extension factor. Thus `E notin B[X]` does not imply `gcd(E,E^tau)=1`. A corrected statement must decompose `E` into base/Frobenius-stable and nonconjugate parts.

3. **The slice cap needs a proof for arbitrary directions.** The answer argues that a single Vieta slice contributes at most `O(n)` slopes. That may be true in the intended nonconjugate split case, but the proof as written only clearly handles aligned directions and does not fully cover arbitrary `Bnum` or mixed-factor `E`.

4. **"No new object appears" is route language, not a theorem.** The CRT incidence object may be equivalent in spirit to the lifted residue-line/local-limit problem, but this equivalence should be stated as `AUDIT` until the arbitrary-anchor and mixed-denominator cases are handled.

## Current Status

Significant as a research lens and source of next tasks, not as a solved theorem.

Bankable route update:

```text
Balanced F1 should now be attacked as a CRT/incidence problem for locator evaluations at extension roots, with special care for arbitrary anchors and mixed Frobenius factorization of E.
```

## Best Next Task

Do not ask another model to "solve the balanced wall" in prose. Ask it to audit/correct the claimed CRT lemmas and produce finite counterexamples or verified corrected statements:

- classify Frobenius factorization of `E`;
- test the line-incidence formula beyond monic anchors;
- search for rich `F`-lines in `I_E`;
- distinguish full `Lambda_NC` from the special locator image.
