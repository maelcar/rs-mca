# Codex Local Audit: Balanced Noncontainment Subset Lemma

Status: `BANKABLE_LEMMA` / `AUDIT`.

This is a bounded Codex-local observation made while Cycle 3 was running. It should be reviewed against `tex/slackMCA_v3.tex:def:residue`.

Source anchor:

- `tex/slackMCA_v3.tex:1189`, `def:residue`.

## Lemma

Let `(E,Bnum,w)` be a degree-`t` residue-line datum with `deg E=t`, `E` nonzero on `D`, `deg Bnum<t`, and `Bnum != 0`. Put

```text
a = k+t.
```

For any subset `S subset D` with `|S| >= a`, there is no polynomial `G in F_{<k}[X]` satisfying

```text
G = -Bnum/E on S.
```

Consequently, every such support is automatically noncontained in the sense of `def:residue`, regardless of the anchor word `w`.

## Proof

If such a `G` existed, then the polynomial

```text
E G + Bnum
```

would vanish on all points of `S`. Its degree is `< k+t = a`, since `deg E=t`, `deg G<k`, and `deg Bnum<t`. If `|S| >= a`, the polynomial must be identically zero. Thus `E G = -Bnum`, so `E` divides `Bnum`. This is impossible because `Bnum != 0` and `deg Bnum<t=deg E`.

Therefore the direction half of containment already fails on every support of size at least `a`; no pair `(A,G)` as in `def:residue` can exist.

## Consequence For W-F1-AA

In the balanced case where the witness threshold is `s_delta=a=k+t` and the numerator is nonzero, shrinking a larger witness support to an `a`-subset preserves noncontainment automatically. The earlier caveat that noncontainment might be lost under shrinking applies only to degenerate numerator-zero or sub-balanced support thresholds, not to the nonzero-numerator balanced slope-packing object.

This sharpens `W-F1-AA`: the remaining problem is purely the slope-image / bad-locus packing bound for the paired base readout, not a separate noncontainment-subset invariant, provided `Bnum != 0`.

## Caveats

- If `Bnum=0`, the above argument does not apply. That case is tangent/zero-direction degenerate for slope packing and should be separated.
- If the radius threshold permits supports smaller than `k+t`, the argument does not apply.
- This does not prove the slope-image packing bound.
