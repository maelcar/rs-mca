# F1 Extension-Line MCA Counterexample Audit

Route verdict: `COUNTEREXAMPLE`

Formal status tags: `COUNTEREXAMPLE`, `AUDIT`

Raw inputs:

- `raw/20260617_F1_EXTENSION_MCA_RAW_1.md`
- `raw/20260617_F1_EXTENSION_MCA_RAW_2.md`
- `raw/20260617_F1_EXTENSION_MCA_RAW_3.md`

Verifier:

- `../verify_f1_extension_counterexample.py`

## Codex Audit

This is significant. The Pro outputs give explicit genuinely extension-valued affine-line MCA witnesses that refute the unrestricted same-numerator extension-line lift as stated in:

- `tex/snarks_v4.tex:242` (`ass:extension-mca-lift`)
- `tex/proximity_blueprint_v3.tex:471` (`prob:F1`)

The counterexample is not the known base-rational subfield confinement phenomenon. The bad lines use an extension-valued denominator

```text
E(X) = X - alpha, alpha notin B.
```

For `p=17`, with `B=F_17`, `F=F_17[alpha]/(alpha^2-3)`, `H=B^*`, `n=16`, `k=8`, `delta=7/16`, and agreement size `9`, the verified line is

```text
f(x) = x^9 / (x - alpha)
g(x) = -1 / (x - alpha)
u_z = f + z g.
```

For each 9-subset `S`, set

```text
L_S(X) = product_{s in S}(X-s)
Q_S(X) = X^9 - L_S(X)
z_S = Q_S(alpha)
P_S(X) = (Q_S(X)-z_S)/(X-alpha).
```

Then `deg P_S < 8`, so `u_{z_S}` agrees with a codeword on `S`; meanwhile `g` cannot agree with any degree-`<8` polynomial on the same `S`, since `(X-alpha)G(X)+1` would have degree at most `8`, vanish on `9` base-field points, and still evaluate to `1` at `X=alpha`.

The local verifier confirms:

```text
p=7:  extension bad slopes = 15/49; base numerator = 7.
p=17: extension bad slopes = 288/289; base numerator = 17.
```

The `p=17` instance refutes the finite same-numerator transfer `17/17 -> 17/289` very strongly. The low-rate asymptotic family in RAW_1 also refutes an unrestricted asymptotic version if `rho` is allowed to tend to zero.

## Banked Result

Banked as:

```text
COUNTEREXAMPLE to unrestricted same-numerator extension-line MCA lift.
```

This does not yet prove a fixed-rate asymptotic replacement theorem. It cuts the route that divides a base MCA numerator by `q_chal=|F|` for arbitrary `F`-valued lines.

## Ledger Consequence

Paper C's extension status must be treated as failed for the unrestricted assumption. A repaired certificate needs one of:

- a restricted extension-line theorem above the corrected reserve,
- an extension-valued residue-line numerator term,
- an affine-subspace/interleaved-base reformulation over `B`,
- or a protocol proof that avoids consuming this MCA object.
