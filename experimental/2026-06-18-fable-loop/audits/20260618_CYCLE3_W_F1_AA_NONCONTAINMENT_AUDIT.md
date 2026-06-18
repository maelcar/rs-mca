# Cycle 3 W-F1-AA Noncontainment Audit

Status: `BANKABLE_LEMMA` for the noncontainment subset lemma; `EXACT_NEW_WALL` for the agreement-rigidity target.

Raw input:

- `raw/20260618_CYCLE3_W_F1_AA_NONCONTAINMENT_RAW.md`

Prompt:

- `prompts/20260618_cycle3_w_f1_aa_noncontainment.md`

Run receipt:

- Packy run id: `2026-06-17T21-27-17-712Z-cycle3-w-f1-aa-noncontainment-20260618-45885014`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-17T21-27-17-712Z-cycle3-w-f1-aa-noncontainment-20260618-45885014`
- Model: `claude-opus-4-8`
- Mode: `artifact_stream`
- Status: `OK`
- Elapsed: `481466 ms`
- Cost: `$0.58973`
- Output tokens: `4123`
- Capture warning: none

## Codex Verdict

The answer is significant. Bank the noncontainment simplification, with a small correction: Opus states automatic noncontainment under `beta != 0` and `z != 0`. The direction half of `tex/slackMCA_v3.tex:def:residue` gives the stronger source-valid statement: for nonzero numerator `Bnum`, any support of size at least `a=k+t` is noncontained for every slope `z`, because no degree-`<k` polynomial can agree with `-Bnum/E` on that many points.

This removes the suspected support-shrinking obstruction in the balanced nonzero-numerator case. The live wall moves to agreement rigidity: the paired readout sees residues of the forced interpolant, but it does not see whether that interpolant agrees with the arbitrary anchor on enough points to form a genuine radius-`delta` witness.

## Bankable Lemma

Let `(E,Bnum,w)` be a degree-`t` residue-line datum in `tex/slackMCA_v3.tex:def:residue`, with `deg E=t`, `deg Bnum<t`, `E` nonzero on `D`, and `Bnum != 0`. Put

```text
a = k+t.
```

For any `S subset D` with `|S| >= a`, there is no `G in F_{<k}[X]` satisfying

```text
G = -Bnum/E on S.
```

Indeed, `E G + Bnum` has degree `<a` and vanishes on at least `a` points, hence is identically zero. This would force `E | Bnum`, impossible for nonzero `Bnum` with `deg Bnum<t=deg E`.

Therefore every balanced nonzero-numerator support of size at least `a` is automatically noncontained. Shrinking a genuine support `S_z` to any `a`-subset preserves the forced interpolation equation and does not lose noncontainment.

## Degenerate Cases

- If `Bnum=0`, the direction half does not block containment. This is a zero/tangent/degenerate stratum and should be separated from numerator-preserving slope packing.
- If one studies supports of size `<=k`, both `w/E` and `-Bnum/E` can be interpolated by degree-`<k` polynomials on that small set, so noncontainment cannot be certified there.
- This lemma does not prove any slope-counting bound.

## Exact New Wall

The next target is:

```text
W-F1-AA-AGR:
Classify high-agreement paired-readout collisions for arbitrary base anchors.
```

For an `a`-subset `S`, let

```text
Q_S = interp_S(w),
nu(S) = |{x in D : Q_S(x)=w(x)}|.
```

The paired readout

```text
rho(S)=(interp_S(w0) mod Ehat, interp_S(w1) mod Ehat)
```

can determine the residue slope condition, but it does not by itself determine whether `nu(S) >= s_delta`. Genuine bad slopes require this high-agreement condition. Thus the problem is not noncontainment-subset survival; it is a rigidity/collision theorem linking bounded residue readout classes to high agreement with the arbitrary anchor.

This is the arbitrary-base-anchor analogue of the monic collision rigidity feeding `tex/slackMCA_v3.tex:prob:perfiber`.

## Rejected Upgrades

- Not a proof of `W-F1-AA` slope-image packing.
- Not a proof of `ass:extension-mca-lift`.
- Not a protocol denominator claim.
- Not a list-decoding or line-decoding theorem.
- Not a raw arbitrary-anchor fiber bound.

## What To Bank

Bank the balanced nonzero-numerator noncontainment lemma and the replacement wall `W-F1-AA-AGR`. Future prompts should attack high-agreement collision rigidity for the paired base interpolation-residue map, rather than asking whether noncontainment survives shrinking to `a=k+t` subsets.
