# Codex Local Audit: Paired Base Readout

Status: `BANKABLE_LEMMA` for the factor-through reduction; `EXACT_NEW_WALL` for the remaining packing statement.

This is a bounded Codex-local audit performed while the shortened Cycle 2 retry was running. It is not a substitute for a human proof review.

Source anchors:

- `tex/slackMCA_v3.tex:1189` (`def:residue`)
- `tex/slackMCA_v3.tex:1197` (`thm:normalform`)
- `tex/slackMCA_v3.tex:1227` (`prob:perfiber`)
- `tex/snarks_v4.tex:242` (`ass:extension-mca-lift`)
- `tex/snarks_v4.tex:765` (`op:extension-mca`)
- `tex/proximity_blueprint_v3.tex:471` (`prob:F1`)

## Bankable Lemma

Let `B=F_p`, let `F/B` be quadratic with Galois involution `tau`, let `D subset B`, and let `w:D->F`. Fix a `B`-basis `1,alpha` and write `w=w0+alpha*w1` with `w0,w1:D->B`.

For a degree-`t` residue-line datum in `def:residue`, put `a=k+t`. If a witness polynomial `Q_z` has degree `<a` and agrees with `w` on a support containing an `a`-subset `S`, then

```text
Q_z = interp_S(w) = interp_S(w0) + alpha interp_S(w1).
```

For any denominator `E in F[X]`, let

```text
Ehat = lcm(E,E^tau)
```

as the monic Galois-invariant lcm, viewed in `B[X]`. Since `E | Ehat` in `F[X]`, the residue class of `interp_S(w)` modulo `E` is determined by

```text
S -> (interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
```

in `(B[X]/Ehat)^2`. Therefore the slope condition

```text
[interp_S(w)]_E = z [Bnum]_E
```

factors through this paired base readout.

This proves only a reduction from arbitrary quadratic extension anchors to a base-field paired interpolation-residue object. It does not prove an MCA numerator bound, a protocol denominator statement, or the extension-line lift.

## Mandatory Checks

1. `Ehat` suffices for arbitrary denominators in the residue-line datum because the only needed operation is reduction from `B[X]/Ehat` to `F[X]/E`. If the denominator has a mixed form such as `G*E1`, the lcm must be taken for the entire denominator actually appearing in `def:residue`, not just one factor.

2. If `[Bnum]_E` is nonzero in `F[X]/(E)`, the scalar slope `z in F` is unique even when `[Bnum]_E` is a zero divisor. Indeed, `(z-z')[Bnum]_E=0` with `z-z' != 0` is impossible because every nonzero scalar in `F` is a unit in the quotient ring. If `[Bnum]_E=0`, uniqueness fails and the datum is tangent/degenerate rather than a numerator-preserving slope packing object.

3. Passing from a witness support `S_z` with `|S_z|>a` to an `a`-subset preserves the forced interpolant and the residue equation. It does not necessarily preserve noncontainment. A subset of a noncontained support may become contained. Thus `a`-subset readouts are safe for overcounting possible slopes, but not by themselves for tangent/contained separation or lower-bound counterpackets.

4. In extension degree `e`, after choosing a `B`-basis of `F`, the readout has `e` component residues in `B[X]/Ehat`, where `Ehat` is the lcm of all Frobenius conjugates of `E`. Its `B`-dimension is `e deg(Ehat)`, with `deg(Ehat) <= e deg(E)`. In the quadratic case this is `2 deg(Ehat) <= 4t`.

5. A raw uniform fiber bound for all arbitrary anchors is false as stated. If each component word `wi` is the evaluation of a polynomial of degree `<a`, then `interp_S(wi)` is independent of `S`, so the raw paired readout fiber can contain all `a`-subsets. This does not imply many bad slopes, because a fixed nonzero numerator residue determines at most one scalar slope.

## Exact New Wall

The correct post-reduction target is:

```text
Bound the number of scalar slopes z in F for which there exists an a-subset S
whose paired base readout satisfies
[interp_S(w)]_E = z [Bnum]_E
and whose original witness can be kept noncontained after tangent/contained
and quotient-periodic contributions are separated.
```

This is a slope-image or bad-locus packing problem, not a raw per-fiber problem for arbitrary component words.

## What To Bank

Bank the factor-through reduction and the five caveats above. Do not bank any statement that arbitrary anchors satisfy the monic locator per-fiber bound, and do not use this reduction to divide a protocol MCA numerator by `q_chal` without a separate extension-line MCA theorem.
