## Final verdict: COUNTEREXAMPLE

The same-numerator extension-line MCA lift is false for extension-valued lines.

The failure is not the known “base-rational lines are trapped in (B)” phenomenon. The bad line below is genuinely (F)-valued: its residue-line denominator is (E(X)=X-\alpha) with (\alpha\notin B). It produces every extension slope as CA/MCA-bad, while the exact base-field numerator is only (q_{\rm gen}=17).

---

## 1. Exact refutation target and parameters

### Refuted target

Refute the same-numerator form of `snarks_v4.tex` `ass:extension-mca-lift`:

[
\boxed{
\mca(C_B,\delta)\le \frac{N_{\rm mca}}{q_{\rm gen}}
\quad\Longrightarrow\quad
\mca(C_F,\delta)\le \frac{N_{\rm mca}}{q_{\rm line}}
}
]

for the extension code (C_F=\RS[F,H,k]), with arbitrary (F)-valued affine lines
[
u_z=f+zg,\qquad z\in F.
]

The counterexample uses the exact base numerator (N_{\rm mca}=17). The predicted extension bound would be (17/289), but the actual extension line has bad-slope density (1).

### Parameter ledger

| Parameter                             |                                                           Value |
| ------------------------------------- | --------------------------------------------------------------: |
| Base/generated field (B)              |                                                (\mathbb F_{17}) |
| Extension/challenge field (F)         |          (\mathbb F_{17^2}=\mathbb F_{17}[\alpha]/(\alpha^2-3)) |
| Field tower                           |                     (B=\mathbb F_{17}\subset F=\mathbb F_{289}) |
| (q_{\rm gen})                         |                                                            (17) |
| (q_{\rm line})                        |                                                           (289) |
| (q_{\rm chal})                        |             (289), if the protocol samples extension challenges |
| Evaluation set (H)                    |                   (B^\times=\mathbb F_{17}^\times={1,\dots,16}) |
| (n)                                   |                                                            (16) |
| (k)                                   |                                                             (8) |
| (\rho=k/n)                            |                                                           (1/2) |
| Agreement size (a)                    |                                                             (9) |
| Radius (\delta=1-a/n)                 |                                                          (7/16) |
| Reserve (\eta=a/n-\rho)               |                                                          (1/16) |
| Agreement slack (\sigma=a-k)          |                                                             (1) |
| Slack notation (\delta=1-\rho-t/N)    |                                                    (t=1,\ N=16) |
| Quotient/fiber scale for this witness | full quotient (N=16,\ M=n/N=1); no proper quotient core is used |
| Residue-line denominator degree       |                                                 (t_{\rm res}=1) |
| Protocol list arity (\mu)             |                           (1) for this line-only counterexample |
| Implementation interleaving (\nu)     |                                                             (1) |

---

## 2. Separate claim ledger

### List decoding

No list-decoding claim is made. This witness is a many-bad-slopes construction for one affine line, not a many-codewords-near-one-received-word construction.

### CA

The extension code (C_F=\RS[F,H,8]) has

[
\eca(C_F,7/16)=1
]

for the explicit (F)-valued line below. Every (z\in F) makes (f+zg) (7/16)-close to (C_F), while the pair ((f,g)) is not (7/16)-close to (C_F^{\equiv 2}).

### MCA

The same explicit line gives

[
\emca(C_F,7/16)=1.
]

Thus the extension numerator is (q_{\rm line}\emca(C_F,\delta)=289), not the base numerator (17).

### Support-wise line-MCA

The support-wise line-MCA failure is exact: for every (z\in F), there is a support (S_z\subset H) with (|S_z|=9) on which (f+zg) agrees with a degree-(<8) polynomial, but (g) itself cannot agree with any degree-(<8) polynomial on that same support. Hence no simultaneous support-wise explanation of (f) and (g) exists.

### Line-decoding

Any line-decoding statement over (F) implying

[
\emca(C_F,7/16)\le a_{\rm LD}/|F|
]

must have (a_{\rm LD}\ge 289) for this code/radius. Therefore a transferred base value (a_{\rm LD}=17) fails.

### Curve-MCA

Any curve-MCA model that contains affine lines as degree-one curves inherits this counterexample. No separate higher-degree curve construction is used.

### Protocol ledger

A protocol ledger that inserts the base numerator (17) into the extension denominator would budget

[
\varepsilon_{\rm mca}^{\rm used}\le \frac{17}{289}.
]

The actual extension-line MCA term is

[
\varepsilon_{\rm mca}^{\rm actual}=1.
]

So `snarks_v4.tex` `def:cert` / `rule:no-double-credit` cannot cite the same-numerator extension lift for this field/radius. The extension-status flag must be “failed unless a stronger extension-valued residue-line theorem is supplied.”

---

## 3. Full witness packet

### Fields

Take

[
B=\mathbb F_{17},\qquad
F=B(\alpha),\qquad
\alpha^2=3.
]

The element (3) is a nonsquare in (\mathbb F_{17}), so (F\cong \mathbb F_{17^2}).

Let

[
H=B^\times={1,2,\dots,16}.
]

Let

[
C_B=\RS[B,H,8],\qquad
C_F=\RS[F,H,8].
]

---

### Base-field numerator

For the base code (C_B), at (\delta=7/16), the canonical base line

[
u_z(x)=x^9+zx^8,\qquad z\in B,
]

has bad-slope set

[
-9^{\wedge}H.
]

By Dias da Silva–Hamidoune,

[
|9^{\wedge}H|
\ge
\min{17,\ 9(16-9)+1}
====================

17.

]

Therefore (9^{\wedge}H=B), so every (z\in B) is bad. Hence

[
\emca(C_B,7/16)=1
]

and the exact base numerator is

[
N_B=q_{\rm gen}\emca(C_B,7/16)=17.
]

The same-numerator lift would predict

[
\emca(C_F,7/16)\le \frac{17}{289}.
]

---

### Extension-valued residue-line datum

Use residue-line datum over (F):

[
E(X)=X-\alpha,\qquad R(X)=1,
]

where (R) is the residue numerator, avoiding conflict with the base field (B).

Define the anchor word

[
w:H\to F
]

by

[
w(1)=1,\qquad w(x)=0\quad\text{for }x\in H\setminus{1}.
]

The affine line is

[
f(x)=\frac{w(x)}{x-\alpha},\qquad
g(x)=-\frac{1}{x-\alpha},
]

so

[
u_z(x)=f(x)+zg(x)=\frac{w(x)-z}{x-\alpha}.
]

This is not a base-rational line. For example,

[
\frac{g(2)}{g(1)}
=================

\frac{1-\alpha}{2-\alpha}
\notin B,
]

so no common scalar can make the direction word (g) (B)-valued.

---

### Bad supports and slopes

For a (9)-subset (S\subset H), let (Q_S(X)) be the degree-(<9) interpolant of (w|_S). Define

[
z_S:=Q_S(\alpha).
]

If (1\notin S), then (Q_S=0), so (z_S=0).

If (1\in S), write (S={1}\cup T), (|T|=8), (T\subset{2,\dots,16}). Then

[
Q_S(X)=\prod_{y\in T}\frac{X-y}{1-y},
]

so

[
z_S
===

\prod_{y\in T}\frac{\alpha-y}{1-y}.
]

Let

[
\omega=1+2\alpha.
]

A finite check gives (\omega) primitive in (F^\times), of order (288). For

[
r_y:=\frac{\alpha-y}{1-y},\qquad y=2,\dots,16,
]

the discrete logs (r_y=\omega^{e_y}) are:

[
\begin{array}{c|ccccccccccccccc}
y&2&3&4&5&6&7&8&9&10&11&12&13&14&15&16\
\hline
e_y&
112&173&174&147&242&257&19&161&247&190&249&150&25&194&70
\end{array}
]

The (8)-fold restricted sums of these exponents cover every residue modulo (288):

[
8^{\wedge}{112,173,174,147,242,257,19,161,247,190,249,150,25,194,70}
====================================================================

\mathbb Z/288\mathbb Z.
]

Therefore

[
{z_S:\ |S|=9,\ 1\in S}=F^\times,
]

and supports not containing (1) give (z_S=0). Hence

[
{z_S:\ |S|=9}=F.
]

Every extension slope occurs.

---

### Why each slope is CA/MCA-bad

Fix any (z\in F). Choose a (9)-subset (S\subset H) with (z=z_S=Q_S(\alpha)).

Because (Q_S(\alpha)=z), the polynomial (Q_S(X)-z) is divisible by (X-\alpha). Define

[
P_z(X):=\frac{Q_S(X)-z}{X-\alpha}.
]

Since (\deg Q_S<9), we have

[
\deg P_z<8,
]

so (P_z) is a codeword polynomial for (C_F).

For every (x\in S),

[
P_z(x)
======

# \frac{Q_S(x)-z}{x-\alpha}

# \frac{w(x)-z}{x-\alpha}

u_z(x).
]

Thus (u_z) agrees with (C_F) on (9) of (16) points, so

[
\dist(u_z,C_F)\le 7/16.
]

Now suppose (g) were explained on the same (S) by some (G\in F[X]_{<8}). Then

[
G(x)=-\frac1{x-\alpha}
\quad\text{for all }x\in S.
]

So

[
(X-\alpha)G(X)+1
]

has degree at most (8) and vanishes on the (9) distinct points of (S). Hence it would be the zero polynomial. But evaluating at (X=\alpha) gives (1), contradiction.

Therefore (g) is not explained on (S) by any degree-(<8) polynomial. So no pair of degree-(<8) codewords can simultaneously explain ((f,g)) on (S).

Thus every (z\in F) is support-wise MCA-bad.

Moreover, the same argument shows no (9)-point support can simultaneously explain ((f,g)), so

[
\dist_2((f,g),C_F^{\equiv 2})\ge 8/16>7/16.
]

Since each (u_z) is (7/16)-close to (C_F), every (z\in F) is also CA-bad.

Therefore

[
\eca(C_F,7/16)=\emca(C_F,7/16)=1.
]

---

## 4. Inequality proving failure of the lift

Base:

[
\emca(C_B,7/16)=1=\frac{17}{17}.
]

Same-numerator extension lift would give:

[
\emca(C_F,7/16)\le \frac{17}{289}.
]

Actual extension-valued line:

[
\emca(C_F,7/16)=1=\frac{289}{289}.
]

Contradiction:

[
1>\frac{17}{289}.
]

So the same numerator does not transfer from (q_{\rm gen}=17) to (q_{\rm line}=q_{\rm chal}=289).

---

## 5. Verification pseudocode

```python
# F = F_17[a] / (a^2 - 3)
p = 17

def add(x, y): return ((x[0]+y[0]) % p, (x[1]+y[1]) % p)
def sub(x, y): return ((x[0]-y[0]) % p, (x[1]-y[1]) % p)
def neg(x): return ((-x[0]) % p, (-x[1]) % p)

def mul(x, y):
    # (u + v a)(r + s a), with a^2 = 3
    return ((x[0]*y[0] + 3*x[1]*y[1]) % p,
            (x[0]*y[1] + x[1]*y[0]) % p)

def inv(x):
    # inverse of u + v a is (u - v a)/(u^2 - 3v^2)
    u, v = x
    den = (u*u - 3*v*v) % p
    den_inv = pow(den, p-2, p)
    return ((u * den_inv) % p, (-v * den_inv) % p)

def div(x, y): return mul(x, inv(y))

def powF(x, n):
    out = (1, 0)
    base = x
    while n:
        if n & 1:
            out = mul(out, base)
        base = mul(base, base)
        n >>= 1
    return out

a = (0, 1)
omega = (1, 2)

# Check omega has order 288
assert powF(omega, 288) == (1, 0)
for d in [1,2,3,4,6,8,9,12,16,18,24,32,36,48,72,96,144]:
    assert powF(omega, d) != (1, 0)

# Build discrete log table for F^*
logs = {}
x = (1, 0)
for e in range(288):
    logs[x] = e
    x = mul(x, omega)

# r_y = (a - y)/(1 - y), y = 2..16
exps = []
for y in range(2, 17):
    r_y = div(sub(a, (y, 0)), sub((1, 0), (y, 0)))
    exps.append(logs[r_y])

assert exps == [
    112, 173, 174, 147, 242,
    257, 19, 161, 247, 190,
    249, 150, 25, 194, 70
]

# Verify nonzero slope coverage:
# products over 8-subsets correspond to sums of 8 exponents mod 288.
from itertools import combinations

covered = set()
for T in combinations(range(15), 8):
    covered.add(sum(exps[i] for i in T) % 288)

assert len(covered) == 288

# Base-field DSH sanity check:
base_slopes = set()
H = list(range(1, 17))
for S in combinations(H, 9):
    base_slopes.add((-sum(S)) % 17)

assert base_slopes == set(range(17))
```

This verifies the two finite claims used above:

[
9^{\wedge}\mathbb F_{17}^{\times}=\mathbb F_{17},
]

and

[
{z_S:|S|=9}=F_{17^2}.
]

---

## 6. Exact repository dependencies by label

The counterexample uses these source dependencies:

* `RS_disproof_v3.tex` `def:mca`: support-wise line-MCA definition.
* `RS_disproof_v3.tex` `lem:locator`: base canonical quotient/locator bad-slope construction.
* `RS_disproof_v3.tex` `lem:dsh`: Dias da Silva–Hamidoune restricted-sum coverage.
* `slackMCA_v3.tex` `thm:exactslack`: exact slack-one canonical bad-slope interpretation.
* `slackMCA_v3.tex` `def:residue`: residue-line datum.
* `slackMCA_v3.tex` `lem:denom` and `thm:normalform`: why extension-valued denominators (E\notin B[X]) are the right coordinate form for all-line MCA.
* `cs25_cap_v4.tex` `def:ca` and `def:mca`: CA/MCA definitions in the cap-paper normalization.
* `cs25_cap_v4.tex` `lem:confine`: explains why this is outside the base-rational confinement theorem.
* `snarks_v4.tex` `ass:extension-mca-lift`: the exact same-numerator extension lift refuted here.
* `snarks_v4.tex` `def:cert`, `rule:no-double-credit`, and `thm:ledger`: protocol ledger entries that cannot use (17/q_{\rm chal}) for this extension-line MCA term.

Final status: **COUNTEREXAMPLE**.
