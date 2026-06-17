## Final verdict: COUNTEREXAMPLE

The numerator-preserving scalar extension-line lift in `prob:F1` is false as stated. The exact reason is not base-rational line confinement; the failure comes from genuinely extension-valued residue-line denominators (E\in F[X]\setminus B[X]).

A weaker but exact replacement theorem is true: extension-line MCA over (F) is exactly a structured affine-subspace / multiplication-slice MCA problem for the (e=[F:B])-interleaved base code. That theorem does **not** follow from scalar base-field MCA.

---

# 1. Exact refutation target and parameters

## Refuted target

For finite fields (B\subset F), (H\subset B), (C_B=\RS[B,H,k]), (C_F=\RS[F,H,k]), the target is the numerator-preserving scalar lift:

[
\emca_{z\in B}(C_B,\delta)\le \frac{N_{\rm mca}}{|B|}
\quad\Longrightarrow\quad
\emca_{z\in F}(C_F,\delta)\le \frac{N_{\rm mca}}{|F|}.
]

The asymptotic version in `prob:F1` allows (N_{\rm mca}^{1+o(1)}) in the numerator. The infinite family below refutes that unrestricted form as well.

---

## Infinite asymptotic counterexample to the (N^{1+o(1)}) form

Let (p) be any odd prime, choose a nonsquare (d\in\mathbb F_p), and set

[
B=\mathbb F_p,\qquad
F=\mathbb F_p(\alpha),\qquad
\alpha^2=d.
]

Parameters:

[
q_{\rm gen}=p,\qquad
q_{\rm line}^{B}=p,\qquad
q_{\rm line}^{F}=q_{\rm chal}=p^2,
]
[
H=B^\times,\qquad
n=p-1,\qquad
k=1,\qquad
\rho=\frac1{p-1}.
]

Take agreement size

[
a=k+\sigma=2,\qquad
\sigma=1,\qquad
\delta=1-\frac2{p-1},\qquad
\eta=\frac1{p-1}.
]

Residue-line data:

[
t_{\rm res}=1,\qquad
E(X)=X-\alpha,\qquad
B_0(X)=1,\qquad
w(X)=X^2.
]

No quotient-core construction is used:

[
M_{\rm quot}=1,\qquad N_{\rm quot}\text{ inactive}.
]

Arity:

[
\mu=1,\qquad \nu=1\text{ over }F,\qquad e=[F:B]=2
]
or, in base-coordinate form, (\nu_B=2).

The base premise holds with the trivial but valid scalar numerator

[
N_{\rm mca}=q_{\rm line}^{B}=p,
\qquad
\emca(C_B,\delta)\le 1=\frac p p.
]

Define the extension-valued line on (H):

[
f(x)=\frac{x^2}{x-\alpha},
\qquad
g(x)=-\frac1{x-\alpha},
\qquad
u_z(x)=f(x)+zg(x)=\frac{x^2-z}{x-\alpha}.
]

For each unordered pair (S={x,y}\subset H), (x\ne y), set

[
z_{x,y}
=\alpha^2-(\alpha-x)(\alpha-y)
=(x+y)\alpha-xy.
]

The slope map is injective on unordered pairs: (z_{x,y}) records the pair’s sum (x+y) and product (xy) in the (B)-basis ({1,\alpha}). Hence there are

[
\binom{p-1}{2}
]

distinct bad slopes.

For (S={x,y}), the explaining codeword is the constant polynomial

[
P_S(X)=x+y\in F[X]_{<1},
]

because on (S),

[
\frac{X^2-z_{x,y}}{X-\alpha}=x+y.
]

The same support cannot explain (g): a degree-(<1) codeword is constant, while

[
-\frac1{x-\alpha}\ne -\frac1{y-\alpha}.
]

Thus each (z_{x,y}) is support-wise MCA-bad. Therefore

[
\emca(C_F,\delta)\ge
\frac{\binom{p-1}{2}}{p^2}
==========================

# \frac{(p-1)(p-2)}{2p^2}

\frac12-o(1).
]

But the claimed (N^{1+o(1)}) lift with (N=p) would give

[
\emca(C_F,\delta)\le \frac{p^{1+o(1)}}{p^2}
=p^{-1+o(1)}.
]

Contradiction.

This already refutes the unrestricted numerator-preserving extension-line lift.

---

# 2. Concrete fixed-rate smooth witness packet

The asymptotic family above has (\rho\to0). The same mechanism appears in a small smooth, half-rate instance.

## Fields and tower

[
B=\mathbb F_{17},\qquad
F=\mathbb F_{17}(\alpha),\qquad
\alpha^2=3.
]

Here (3) is a nonsquare mod (17), so (F\cong\mathbb F_{17^2}).

[
q_{\rm gen}=17,\qquad
q_{\rm line}^{B}=17,\qquad
q_{\rm line}^{F}=q_{\rm chal}=289.
]

## Code and evaluation set

[
H=B^\times=\mathbb F_{17}^\times,\qquad
n=16,\qquad
k=8,\qquad
\rho=\frac12.
]

This is the full multiplicative subgroup of order (16), so it is power-of-two smooth.

Agreement/radius parameters:

[
a=k+\sigma=9,\qquad
\sigma=1,\qquad
\delta=1-\frac9{16}=\frac7{16},
\qquad
\eta=\frac{\sigma}{n}=\frac1{16}.
]

Residue-line data:

[
t_{\rm res}=1,\qquad
E(X)=X-\alpha,\qquad
B_0(X)=1,\qquad
w(X)=X^9.
]

Quotient data:

[
M_{\rm quot}=1,\qquad
N_{\rm quot}\text{ inactive}.
]

This is not a quotient-core or residue-coset attack. It is a degree-one extension-denominator residue-line attack.

Arity:

[
\mu=1,\qquad
\nu=1\text{ over }F,\qquad
e=[F:B]=2.
]

In base-coordinate form, the same object is a structured (2)-interleaved base-code affine-subspace test.

## Bad line

For (x\in H), define

[
f(x)=\frac{x^9}{x-\alpha},
\qquad
g(x)=-\frac1{x-\alpha},
\qquad
u_z(x)=f(x)+zg(x)=\frac{x^9-z}{x-\alpha}.
]

For each (9)-subset (S\subset H), let

[
L_S(X)=\prod_{s\in S}(X-s),
\qquad
Q_S(X)=X^9-L_S(X).
]

Then (\deg Q_S\le 8), and define

[
z_S=Q_S(\alpha)=\alpha^9-L_S(\alpha).
]

For this slope, set

[
P_S(X)=\frac{Q_S(X)-z_S}{X-\alpha}.
]

Since (Q_S(\alpha)=z_S), the numerator is divisible by (X-\alpha), and

[
\deg P_S<8=k.
]

For every (x\in S), (L_S(x)=0), hence

[
P_S(x)
======

# \frac{x^9-z_S}{x-\alpha}

u_{z_S}(x).
]

So (u_{z_S}) agrees with a codeword of (C_F=\RS[F,H,8]) on the (9)-point support (S).

## Failure of simultaneous explanation

Suppose (G\in F[X]_{<8}) agreed with (g) on (S). Then

[
(X-\alpha)G(X)+1
]

has degree at most (8), vanishes on the (9) distinct points of (S), and is not the zero polynomial because its value at (X=\alpha) is (1). Contradiction.

Therefore (g) has no degree-(<8) explanation on (S), so no pair ((A,G)\in F[X]_{<8}^2) simultaneously explains ((f,g)) on (S). Thus every slope (z_S) is support-wise MCA-bad.

A deterministic enumeration gives

[
#{z_S:S\in\binom{H}{9}}=288=289-1,
]

with the only missing field element (13\alpha=\alpha^9). Hence

[
\emca(C_F,7/16)\ge \frac{288}{289}.
]

The base-code premise holds with the valid scalar numerator

[
N_{\rm mca}=17:
\qquad
\emca(C_B,7/16)\le1=\frac{17}{17}.
]

The numerator-preserving lift would imply

[
\emca(C_F,7/16)\le\frac{17}{289},
]

but the witness gives

[
\frac{288}{289}>\frac{17}{289}.
]

So the scalar numerator-preserving lift fails even in a smooth half-rate instance.

Verifier: [f1_extension_counterexample_verify.py](sandbox:/mnt/data/f1_extension_counterexample_verify.py)

---

# 3. Verification pseudocode

```python
p = 17
D = 3                       # alpha^2 = 3
F = {(a,b): a,b in F_17}     # a + b alpha
H = F_17^*
k = 8
a = k + 1                   # 9

def mul((a,b),(c,e)):
    return (a*c + D*b*e, a*e + b*c) mod p

alpha = (0,1)

Z = set()
for S in combinations(H, 9):
    L = product(alpha - x for x in S)
    z = alpha^9 - L
    Z.add(z)

assert len(Z) == 288
assert Z == F - {13*alpha}
assert len(Z) > 17
```

For each enumerated (S), the proof above constructs the explicit explaining codeword (P_S) and proves noncontainment by the degree-(8) vanishing contradiction.

---

# 4. What is still true: exact coordinate transfer theorem

Although the scalar numerator lift is false, there is an exact extension-line to base-affine-subspace identity.

Let (e=[F:B]) and fix a (B)-basis (\omega_1,\dots,\omega_e) of (F). Write

[
\Phi:F^H\to (B^H)^e
]

for coordinate expansion. For (z\in F), let (M_z\in\operatorname{Mat}_{e\times e}(B)) be the matrix of multiplication by (z) in this basis.

Then

[
\Phi(C_F)=C_B^{\equiv e}.
]

For every (f,g\in F^H), every (z\in F), and every support (S\subseteq H),

[
(f+zg)|_S\in C_F|_S
]

if and only if

[
\Phi(f)|_S+M_z\Phi(g)|_S\in (C_B|_S)^{\equiv e}.
]

Also, ((f,g)) is simultaneously explained over (F) on (S) if and only if ((\Phi(f),\Phi(g))) is simultaneously explained coordinatewise over (B) on (S).

Therefore

[
\emca_{z\in F}(C_F,\delta)
==========================

\operatorname{mMCA}^{\rm mult}_{z\in F}
\bigl(C_B^{\equiv e},\delta\bigr),
]

where the right-hand side is the base-field (e)-interleaved MCA problem for the structured multiplication-slice affine family

[
\Phi(f)+M_z\Phi(g),\qquad z\in F.
]

This is the protocol-compatible transfer theorem: extension-line MCA is exactly a structured affine-subspace MCA problem over the base field. It is not bounded by scalar base-field MCA unless an additional theorem controls this multiplication-slice affine object.

Source dependencies by label:

[
\texttt{def:mca}
]

for support-wise MCA; the coordinate identity is the MCA-side analogue of

[
\texttt{eq:extension-list}.
]

It is consistent with, but does not use as a black box,

[
\texttt{thm:subfield}
\quad\text{and}\quad
\texttt{lem:confine},
]

which cover only (B)-valued lines. The counterexample uses (E=X-\alpha\notin B[X]), so it deliberately evades subfield confinement.

---

# 5. Separate ledger claims

## List decoding

No list-decoding upper or lower bound is proved by this counterexample. The clean list identity

[
\texttt{eq:extension-list}
]

remains separate. The failure is MCA/CA through extension-valued line data, not a generated-field locator entropy claim.

## CA

The same slopes are CA-bad in both the infinite (k=1) family and the finite (p=17,k=8) packet, because (g=-1/(X-\alpha)) has no degree-(<k) agreement on any (k+1)-point support. Thus the pair ((f,g)) is not jointly close on any support of size (a=k+1), while (f+zg) is explained on such a support.

## MCA

The scalar numerator-preserving lift

[
N_{\rm mca}/q_{\rm line}^{B}
\mapsto
N_{\rm mca}/q_{\rm line}^{F}
]

is false. In the finite packet,

[
q_{\rm line}^{B}=17,\qquad
q_{\rm line}^{F}=q_{\rm chal}=289,
]

and

[
17/17\quad\not\Rightarrow\quad17/289.
]

The actual extension MCA lower bound from one line is

[
288/289.
]

## Support-wise line-MCA

This is the strongest explicit part of the witness. For each bad slope (z_S), the same support (S) explains (u_{z_S}=f+z_Sg), while (g) cannot be explained on (S). Hence the witness satisfies the support-wise definition directly.

## Line-decoding

The construction gives a noncontained residue-line packing lower bound. In the finite packet,

[
\Lambda^{\rm NC}_{1,7/16}(H,8)\ge 288.
]

Therefore any line-decoding theorem implying

[
\emca(C_F,7/16)\le a_{\rm LD}/289
]

must have

[
a_{\rm LD}\ge 288
]

for this code and line family.

## Curve-MCA

No degree-(>1) curve-MCA claim is made. The counterexample is affine-line only, i.e. curve arity (1).

## Protocol ledger

A certificate cannot use

[
q_{\rm gen}=17
]

for entropy and then silently divide a scalar base-field MCA numerator by

[
q_{\rm chal}=289.
]

For extension challenges, the MCA ledger must use one of:

[
q_{\rm line}=|F|
]

together with a theorem for the actual (F)-line family, or the exact coordinate transfer above plus a theorem for the corresponding multiplication-slice affine-subspace MCA over the (e)-interleaved base code.

For the finite witness:

[
\mu=1,\qquad
\nu=1\text{ over }F,\qquad
e=2,
]

and in the base-coordinate view the relevant object is not scalar MCA of (C_B), but a structured (2)-coordinate affine-subspace MCA problem.
