## Final verdict: COUNTEREXAMPLE

This refutes the unconditional **same-numerator extension-line MCA lift**:

[
\emca(C_B,\delta)\le \frac{N_{\rm mca}}{q_{\rm gen}}
\quad\Longrightarrow\quad
\emca(C_F,\delta)\le \frac{N_{\rm mca}}{q_{\rm line}}
]

for the extension code (C_F) and arbitrary (F)-valued affine lines (f+zg). The failure is caused by a genuinely extension-valued residue-line denominator (E(X)=X-\theta\notin B[X]), not by base-rational lines.

This is a low-reserve counterexample; it refutes the unconditional transfer statement, but it does **not** refute a possible future theorem with extra corrected-reserve hypotheses.

---

## 1. Exact refutation target and parameters

**Refuted target.** The target is the same-numerator form of `snarks_v4.tex` `ass:extension-mca-lift`:

[
C_B=\RS[B,D,k],\quad C_F=\RS[F,D,k],\quad D\subseteq B,
]
[
\emca(C_B,\delta)\le \frac{N_{\rm mca}}{|B|}
\quad\stackrel{\text{false}}{\Longrightarrow}\quad
\emca(C_F,\delta)\le \frac{N_{\rm mca}}{|F|}.
]

**Witness parameters.**

| ledger item                                |                                                                                    value |
| ------------------------------------------ | ---------------------------------------------------------------------------------------: |
| base/generated field (B)                   |                                                                            (\mathbb F_7) |
| extension / line / challenge field (F)     |                                        (\mathbb F_{49}=\mathbb F_7[\theta]/(\theta^2-3)) |
| (q_{\rm gen})                              |                                                                                      (7) |
| (q_{\rm line})                             |                                                                                     (49) |
| (q_{\rm chal})                             |                                                                                     (49) |
| field tower                                |                                                      (\mathbb F_7\subset \mathbb F_{49}) |
| evaluation domain (D)                      |                                                                 (B^\times={1,2,3,4,5,6}) |
| (n)                                        |                                                                                      (6) |
| (k)                                        |                                                                                      (3) |
| rate (\rho=k/n)                            |                                                                                    (1/2) |
| radius (\delta)                            |                                                                                    (1/3) |
| agreement size (a=\lceil(1-\delta)n\rceil) |                                                                                      (4) |
| agreement slack (\sigma=a-k)               |                                                                                      (1) |
| reserve (\eta=\sigma/n)                    |                                                                                    (1/6) |
| slack stratum                              |                                                                                    (T=1) |
| residue denominator degree (t)             |                                                                                      (1) |
| quotient order (N/M)                       | no quotient-core construction used; whole-domain normalization (N=6,a_{\rm quot}=1) only |
| protocol list arity (\mu)                  |                                                                                      (1) |
| implementation interleaving (\nu)          |                                                                                      (1) |

The base code is

[
C_B=\RS[\mathbb F_7,D,3],
]

and the extension code is

[
C_F=\RS[\mathbb F_{49},D,3].
]

---

## 2. Witness packet

Work in

[
F=\mathbb F_7[\theta]/(\theta^2-3).
]

Since (3) is a nonsquare in (\mathbb F_7), this is (\mathbb F_{49}). Define

[
E(X)=X-\theta,\qquad w(X)=X^4,\qquad B_{\rm num}(X)=1.
]

The affine line over (F^D) is

[
u_z=f+zg,
]

where

[
f(x)=\frac{x^4}{x-\theta},\qquad
g(x)=\frac{-1}{x-\theta}
\quad\text{for }x\in D.
]

Thus

[
u_z(x)=\frac{x^4-z}{x-\theta}.
]

This is a degree-(1) residue-line datum in the sense of `slackMCA_v3.tex` `def:residue`:

[
(E,B_{\rm num},w)=\bigl(X-\theta,;1,;X^4\bigr).
]

### Received words (f,g)

Elements are written (a+b\theta).

| (x) | (f(x)=x^4/(x-\theta)) | (g(x)=-1/(x-\theta)) |
| --: | --------------------: | -------------------: |
|   1 |           (3+3\theta) |          (4+4\theta) |
|   2 |           (4+2\theta) |          (5+6\theta) |
|   3 |           (2+3\theta) |           (3+\theta) |
|   4 |           (5+3\theta) |           (4+\theta) |
|   5 |           (3+2\theta) |          (2+6\theta) |
|   6 |           (4+3\theta) |          (3+4\theta) |

For every (4)-subset (S\subset D), let

[
L_S(X)=\prod_{s\in S}(X-s),
\qquad
Q_S(X)=X^4-L_S(X).
]

Because (L_S) is monic of degree (4), (Q_S) has degree (<4=k+1). Define

[
z_S=Q_S(\theta)=\theta^4-L_S(\theta).
]

Then (Q_S\equiv z_S\pmod{E}), and (Q_S=w) on (S). Therefore

[
P_S(X)=\frac{Q_S(X)-z_S}{X-\theta}
]

is a polynomial of degree (<3=k), so (P_S\in C_F), and

[
P_S(x)=u_{z_S}(x)\qquad\text{for all }x\in S.
]

So each (z_S) has a valid agreement witness on (S).

### Bad-slope table

The (15=\binom64) supports give (15) distinct slopes.

| support (S) | bad slope (z_S) |
| ----------- | --------------: |
| ({1,2,3,4}) |     (4+3\theta) |
| ({1,2,3,5}) |     (1+3\theta) |
| ({1,2,3,6}) |     (5+3\theta) |
| ({1,2,4,5}) |     (2+2\theta) |
| ({1,2,4,6}) |     (1+5\theta) |
| ({1,2,5,6}) |             (4) |
| ({1,3,4,5}) |     (1+6\theta) |
| ({1,3,4,6}) |             (0) |
| ({1,3,5,6}) |     (1+2\theta) |
| ({1,4,5,6}) |     (5+4\theta) |
| ({2,3,4,5}) |             (3) |
| ({2,3,4,6}) |      (1+\theta) |
| ({2,3,5,6}) |     (2+5\theta) |
| ({2,4,5,6}) |     (1+4\theta) |
| ({3,4,5,6}) |     (4+4\theta) |

### Why condition (ii) holds

For any (4)-subset (S), (g) cannot be explained on (S) by a degree-(<3) polynomial.

Indeed, if some (G\in F[X]) with (\deg G<3) satisfied

[
G(x)=\frac{-1}{x-\theta}\qquad\forall x\in S,
]

then

[
(X-\theta)G(X)+1
]

would have degree at most (3) and would vanish on the (4) distinct points of (S). Hence it would be the zero polynomial, forcing ((X-\theta)G(X)=-1), impossible.

Therefore no pair of degree-(<3) codewords can simultaneously explain (f) and (g) on (S). Each listed (z_S) is support-wise MCA-bad.

---

## 3. Inequality contradiction

For the base code (C_B=\RS[\mathbb F_7,D,3]), the exact base MCA numerator at this radius is (7):

[
\emca(C_B,1/3)=1=\frac{7}{7}.
]

One way to see equality is by `slackMCA_v3.tex` `thm:exactslack` applied to the base line

[
X^4+zX^3.
]

At slack (T=1), the bad slopes are

[
-\sum_{s\in S}s,\qquad |S|=4.
]

Since (D=\mathbb F_7^\times), these values cover all of (\mathbb F_7). Thus the exact base numerator is

[
N_{\rm mca}=7.
]

A same-numerator extension lift would predict

[
\emca(C_F,1/3)\le \frac{7}{49}.
]

But the extension-valued line above gives

[
\emca(C_F,1/3)\ge \frac{15}{49}.
]

Hence

[
\frac{15}{49}>\frac{7}{49},
]

contradicting the extension-line MCA lift.

The same witness also gives

[
\eca(C_F,1/3)\ge \frac{15}{49},
]

because (g) is not (\delta)-close to (C_F) on any support of size (4), so the pair ((f,g)) is not jointly (\delta)-close while each listed (u_{z_S}) is (\delta)-close.

---

## 4. Separate claim ledger

| object                | claim status                           | exact claim                                                                                                                                                                                           |
| --------------------- | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| List decoding         | no transfer claim used                 | This is not a list-decoding counterexample. No fixed received word is claimed to have a large list.                                                                                                   |
| CA                    | counterexample lower bound             | (\eca(C_F,1/3)\ge 15/49).                                                                                                                                                                             |
| MCA                   | counterexample lower bound             | (\emca(C_F,1/3)\ge 15/49).                                                                                                                                                                            |
| Support-wise line-MCA | explicit witness                       | The line (f+zg) has at least (15) support-wise bad slopes over (F).                                                                                                                                   |
| Line-decoding         | inherited affine-line obstruction only | Any line-decoding formulation whose bad event is “line point close, line data not jointly close” has at least the same (15/49) bad-parameter density here. No separate list-size theorem is asserted. |
| Curve-MCA             | no higher-degree curve claim           | This is a degree-(1) affine-line counterexample only. No claim for power-curve batching.                                                                                                              |
| Protocol ledger       | fails if it books same numerator       | With (q_{\rm chal}=q_{\rm line}=49), booking the base numerator (7) gives (7/49), but the actual CA/MCA line term is at least (15/49).                                                                |

---

## 5. Exact source dependencies by label

Used definitions and source facts:

[
\texttt{snarks_v4.tex: ass:extension-mca-lift}
]

is the refuted target.

[
\texttt{slackMCA_v3.tex: def:mca}
]

is the support-wise MCA definition.

[
\texttt{slackMCA_v3.tex: thm:exactslack}
]

certifies the base-field slack-one line (X^4+zX^3) has all (7) base slopes bad.

[
\texttt{slackMCA_v3.tex: def:residue}
]

is the residue-line normal form used by the extension witness with (E=X-\theta).

[
\texttt{cs25_cap_v4.tex: def:ca}
]

is the CA definition used for the separate CA lower bound.

[
\texttt{cs25_cap_v4.tex: lem:confine}
]

explains why this is not a base-rational-line obstruction: (f,g) are genuinely (F)-valued, so subfield confinement does not apply.

---

## 6. Verification pseudocode

```python
B = GF(7)
F = GF(7)[theta] / (theta^2 - 3)
D = [1,2,3,4,5,6]
k = 3
delta = 1/3
theta = F.theta

E = X - theta
w = X^4

f(x) = x^4 / (x - theta)
g(x) = -1 / (x - theta)

bad_slopes = set()

for each 4-subset S of D:
    L_S = product(X - s for s in S)
    Q_S = X^4 - L_S
    z_S = Q_S(theta)

    assert degree(Q_S) < 4
    assert Q_S(theta) == z_S

    P_S = (Q_S - z_S) / (X - theta)
    assert degree(P_S) < 3

    for x in S:
        assert P_S(x) == f(x) + z_S * g(x)

    # g cannot be explained on S by degree < 3
    # because (X-theta)G + 1 would have degree <= 3 and 4 roots
    assert no degree_lt_3_polynomial_matches(g on S)

    bad_slopes.add(z_S)

assert len(bad_slopes) == 15
assert 15/49 > 7/49
```

A runnable verifier is here: [f1_extension_mca_counterexample.py](sandbox:/mnt/data/f1_extension_mca_counterexample.py).
