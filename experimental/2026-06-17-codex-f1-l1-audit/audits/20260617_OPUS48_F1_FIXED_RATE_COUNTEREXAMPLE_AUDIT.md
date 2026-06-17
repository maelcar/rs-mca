# Opus 4.8 F1 Fixed-Rate Counterexample Audit

Route verdict: `COUNTEREXAMPLE`

Formal status tags: `PROVED`, `COUNTEREXAMPLE`, `AUDIT`

Raw input:

- `raw/20260617_OPUS48_F1_FIXED_RATE_RAW_1.md`

Verifier:

- `../verify_f1_fixed_rate_slice.py`

## Codex Audit

This is significant. The answer strengthens the previous F1 bank from finite witnesses to a fixed-rate asymptotic counterexample to the unrestricted same-numerator extension-line MCA lift.

The target remains:

- `tex/snarks_v4.tex:242` (`ass:extension-mca-lift`)
- `tex/proximity_blueprint_v3.tex:471` (`prob:F1`)

## Banked Theorem

Let `B=F_p`, `F=F_{p^2}=F_p[alpha]/(alpha^2-d)` with `d` nonsquare, `H=F_p^*`, `n=p-1`, `k=floor(rho n)`, `a=k+1`, and `delta=1-a/n`. Define the extension-valued line

```text
f(x) = x^a/(x-alpha)
g(x) = -1/(x-alpha)
u_z = f + z g.
```

For each `a`-subset `S`, set

```text
L_S(X) = product_{s in S}(X-s)
Q_S(X) = X^a - L_S(X)
z_S = Q_S(alpha).
```

Each distinct `z_S` is support-wise MCA-bad over `F`. Fixing an `(a-2)`-subset `T` and varying the pair `{x,y}` outside `T`, the map

```text
{x,y} -> z_{T union {x,y}}
```

is injective because it records `(x+y, xy)` up to an affine bijection over `F`. Therefore

```text
emca(C_F, delta) >= binom(p-a+1, 2) / p^2
                 -> (1-rho)^2/2.
```

The base premise of `ass:extension-mca-lift` holds trivially with numerator `N_mca=p`, since `emca(C_B,delta)<=1=p/p`. The unrestricted lift would predict `p^{1+o(1)}/p^2 -> 0`, contradicting the positive constant lower bound.

## Important Limitation

This counterexample is at `sigma=1`, hence reserve `eta=sigma/n=O(1/n)`. It does not refute a repaired extension-line theorem restricted to the corrected-reserve regime `sigma >= C n/log n`. That is now the live F1 repair target.

## Consequence

The old route "base numerator over `q_gen`, then divide by extension `q_chal`" is dead in the unrestricted form, even at fixed rate. A protocol certificate must either:

- include a theorem over the actual extension line field,
- add an extension-valued residue-line numerator term,
- restrict to a proved corrected-reserve regime,
- or reformulate the extension line as a structured affine-subspace/interleaved-base problem.
