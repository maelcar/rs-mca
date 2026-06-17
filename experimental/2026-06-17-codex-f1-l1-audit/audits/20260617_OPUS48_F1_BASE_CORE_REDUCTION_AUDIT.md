# Opus 4.8 F1 Base-Core Reduction Audit

Route verdict: `BANKABLE_LEMMA` with open arbitrary-anchor gap

Formal status tags: `PROVED`, `CONDITIONAL`, `AUDIT`

Raw input:

- `raw/20260617_OPUS48_F1_BASE_CORE_RAW_1.md`

## Codex Audit

This answer is significant. It fixes two problems in the previous balanced-CRT answer and gives bankable algebra for the monic-anchor / locator stratum. It does not fully solve balanced F1 because `def:residue` permits arbitrary anchors `w:D->F`.

## Bankable Content

1. **Frobenius factorization of the denominator.** For squarefree `E in F[X]`, with `F/B` quadratic and Frobenius `tau`, one can decompose

```text
E = G E_1
```

where `G in B[X]` is the Frobenius-stable core and `gcd(E_1,E_1^tau)=1`. This corrects the false dichotomy in the prior CRT audit. A genuinely extension denominator may have a mixed form: base/Frobenius-stable part times conjugate-free extension part.

2. **Corrected confinement.** The `G` part is base-confined. The conjugate-free `E_1` part has no subfield-confinement saving: base polynomials map onto the full `F[X]/(E_1)` as an `F_p`-space via the lcm `E_1 E_1^tau`.

3. **Slope-collision identity for monic anchor.** In the balanced case `t=sigma`, for the special monic anchor `w=X^a`, equal slopes from supports `S,S'` force

```text
lcm(E,E^tau) divides L_S - L_S'
```

because `L_S-L_S' in B[X]`. Thus distinct slopes inject into the base-field readout

```text
S -> [L_S]_{hat E},   hat E = lcm(E,E^tau) in B[X],
deg(hat E) <= 2 sigma.
```

This reduces the monic-anchor balanced extension problem to a base-field per-fiber collision problem at effective prefix length at most `2 sigma`.

## Caveat: Not A Full F1 Closure

The answer still does not handle arbitrary anchor words `w:D->F` in `tex/slackMCA_v3.tex` `def:residue`. The slope-collision identity uses the special identity

```text
Q_S = X^a - L_S
```

for a monic degree-`a` anchor. For arbitrary `w`, the forced interpolant on `S` is not a locator polynomial difference, and the `S -> [L_S]_{hat E}` readout need not capture all balanced residue-line data.

Therefore the correct project status is:

```text
BANKABLE_LEMMA for monic-anchor / locator stratum.
OPEN: arbitrary-anchor balanced F1.
```

## Consequence

The next highest-value target is no longer another CRT wall summary. It is the arbitrary-anchor gap:

- either reduce arbitrary anchors to a base-field readout like `hat E`;
- or exhibit finite balanced data where arbitrary `w` produces richer extension slopes than any locator image;
- or prove a canonical-anchor reduction.
