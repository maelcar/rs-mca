# Opus 4.8 F1 Residual-Slack Audit

Route verdict: `BANKABLE_LEMMA` / `EXACT_NEW_WALL`

Formal status tags: `PROVED`, `CONDITIONAL`, `EXPERIMENTAL`, `AUDIT`

Raw input:

- `raw/20260617_OPUS48_F1_RESIDUAL_SLACK_RAW_1.md`

Related verifiers:

- `../verify_f1_fixed_rate_slice.py`
- `../verify_f1_sigma2_degree1.py`

## Codex Audit

This answer is significant, but it should not be banked wholesale.

Bankable:

1. **Residual-slack reduction.** A degree-`t` residue-line datum with denominator `E`, numerator `B`, and anchor `w` has its bad slopes bounded by a list-type object for the anchor in an RS code of dimension `k+t`. Equivalently, the relevant list slack is `sigma-t`, not `sigma`. This is a self-contained consequence of `tex/slackMCA_v3.tex` `def:residue`.

2. **New wall.** Above corrected reserve, the unbalanced regime where `sigma-t` still clears the list reserve reduces to the extension/list ledger. The remaining F1 difficulty is the balanced denominator range

```text
t in [sigma - Theta(n/log n), sigma]
```

with `E in F[X] \\ B[X]`. This is the sharp live wall for a repaired extension-line MCA theorem.

Not banked as fully proved:

1. The output claims degree-one denominators give `Theta(p^2)` bad slopes for every fixed `sigma`. It gives a convincing explicit argument for `sigma=2`, and finite checks support it, but the general fixed-`sigma` claim needs a written algebraic-counting proof before it is promoted to `PROVED`.

2. The statement "degree-one is safe above corrected reserve" is `CONDITIONAL` on the needed extension/list local-limit theorem. The previous L1 audit already showed raw arbitrary `Fib_U` is false, so this cannot be cited as an unconditional theorem.

## Banked Lemma

Let `C_F=RS[F,D,k]`, let `a=k+sigma`, and let `(E,B,w)` be a degree-`t` residue-line datum in the sense of `tex/slackMCA_v3.tex` `def:residue`, with `B` nonzero modulo `E`. If slope `z` has a witness `Q_z,S_z`, then:

```text
deg Q_z < k+t,
Q_z = w on S_z,
|S_z| >= k+sigma,
Q_z = z B mod E.
```

For each polynomial `Q` of degree `< k+t`, there is at most one scalar `z` with `Q = zB mod E`. Hence the number of bad slopes contributed by this datum is at most the number of degree-`<k+t` polynomials agreeing with `w` on at least `k+sigma` points, i.e. a list object with residual slack `sigma-t`.

## Consequence

For `t=1`, any above-reserve statement with `sigma >= C n/log n` still has residual slack `sigma-1`, so degree-one denominators should be handled by the same list/local-limit ledger once that ledger is repaired and proved.

For `t approx sigma`, residual slack is small or zero, and the reduction gives no saving. That balanced range is now the important F1 target.

## Finite Evidence

`verify_f1_sigma2_degree1.py` checks the natural `sigma=2`, `E=X-alpha`, `w=X^(k+2)` family over small fields. It is evidence, not the proof of the asymptotic fixed-`sigma` claim.
