# Fixed-27 quartic high-triple exclusion

## Status and dependency

This note proves a local theorem in the literal fixed-27, affine-rank-two,
primitive-quartic source cell. It depends on the source setup and repeated-root
safe quartic reduction in PR #894 at exact head
`3c048a9637a02525ef41d1c340252200e4b0f41a`.

The theorem closes the high-triple alternative isolated by that PR. It does not
exclude the low-triple alternative, prove a cap of six, charge a global ledger,
or change the official score.

The frozen public baseline used for the audit was
`origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.

## Source setup

Work over

\[
 F=\mathbb F_{2,130,706,433},\qquad
 H=\mu_{2^{21}}\subset F^\times,\qquad
 B=32,768,\qquad \Lambda=\mu_{64}.
\]

Set

\[
 d=63,601,\qquad w=28,897.
\]

Fix a literal normalized fixed-27 source cell satisfying the hypotheses of PR
#894. Thus seven distinct labels \(y_0,\ldots,y_6\in\Lambda\setminus C\)
have residuals \(R_i\), nonzero source scalars \(q_i\), and Pad\'e quotients
\(W_i\) with

\[
 (X^B-y_i)R_i=q_i h+gW_i,
 \qquad \deg R_i=d,
 \qquad \deg W_i\le w.
\]

Every \(R_i\) is squarefree, splits completely over \(H\), avoids the core
fibres and its selected fibre, and contains no additional complete \(B\)-fibre.
The generator \(g\) is root-free on \(H\).

In the affine-rank-two primitive-quartic branch, normalize

\[
 \rho_i=q_i^{-1}R_i,
 \qquad
 P_i=(X^B-y_i)\rho_i
     =H_0+g\,c_i\mathbin{\cdot}(E_1,E_2).
\]

The inherited quartic syzygy and pair-secant identities are

\[
 a_0(X^B)H_0+g\bigl(a_1(X^B)E_1+a_2(X^B)E_2\bigr)=0,
\]

\[
 a_0(X^B)=g s,
 \qquad \deg a_0=4,
 \qquad \deg s=63,600,
 \qquad a_0(z)\ne0\quad(z\in\Lambda),
\]

and

\[
 s\rho_i=b_i(X^B)\mathbin{\cdot}(E_1,E_2),
 \qquad
 \det(b_i,b_j)=a_0\delta_{ij},
 \qquad
 0\ne\delta_{ij},\quad \deg\delta_{ij}\le2.
\]

Let

\[
 \mathrm{Base}=Z_H(E_1)\cap Z_H(E_2),
 \qquad c=|\mathrm{Base}|\le12,997,
\]

\[
 r=d-c,
 \qquad \lambda=w-c.
\]

Outside the base, every root has occupancy at most three. Let \(n_3\) be the
number of roots with occupancy exactly three among the seven residual root
sets. PR #894 proves that \(n_3>5\lambda\) forces six nonempty
Fano-minus-one triple lines and one nontrivial even composition of the reduced
direction pair.

## Theorem

Under the source hypotheses above,

\[
 n_3\le5\lambda.
\]

Consequently the high-triple six-line alternative is empty. If

\[
 U=\bigcup_{i=0}^6 Z_H(R_i),
\]

then

\[
 |U|\ge150,361.
\]

This is a uniform local theorem over the stated source cell. It does not assert
that a seven-label source cell exists.

## Proof

Assume for contradiction that \(n_3>5\lambda\).

### 1. Exact base cancellation

Every point of `Base` is a simple root of each \(\rho_i\) and of both direction
polynomials. Cancel the common base polynomial to obtain

\[
 s\bar\rho_i=b_i(X^B)\mathbin{\cdot}(\bar E_1,\bar E_2),
 \qquad
 \deg\bar\rho_i=r,
 \qquad
 \deg\bar E_j\le\lambda.
\]

Write \(J=\gcd(\bar E_1,\bar E_2)\). The polynomial \(J\) has no root in
\(H\): otherwise the original direction pair would vanish to order at least
two at that point, while \(s\rho_i\) has valuation exactly one because \(s\)
is root-free on \(H\) and \(\rho_i\) is squarefree.

Factor \(J=QJ_0\), \(s=QS\), with \(\gcd(J_0,S)=1\). Euclid's lemma gives
\(J_0\mid\bar\rho_i\). Since \(\bar\rho_i\) splits over \(H\), every
nonconstant divisor has an \(H\)-root, whereas \(J_0\mid J\) has none. Hence
\(J_0\) is constant and \(J\mid s\). After cancellation,

\[
 S\bar\rho_i=b_i(X^B)\mathbin{\cdot}(F,G),
 \qquad
 \gcd(F,G)=1,
 \qquad
 \max(\deg F,\deg G)\le\lambda,
\]

where \(S\) is root-free on \(H\).

### 2. Six distinct fourth fibres

For each of the six nonempty triple lines \(\ell=\{i,j,k\}\), let
\(A_\ell\) be its occupancy-three roots. If \(x\in A_\ell\) and \(z=x^B\),
then the rows \(b_i(z)\) and \(b_j(z)\) annihilate the same nonzero vector
\((F(x),G(x))\). Thus

\[
 0=\det(b_i(z),b_j(z))=a_0(z)\delta_{ij}(z).
\]

Since \(a_0(z)\ne0\), one has \(\delta_{ij}(z)=0\). The inherited label
collinearity also gives \(\delta_{ij}(y_k)=0\), and selected-fibre avoidance
gives \(z\ne y_k\). Because \(\delta_{ij}\) is nonzero of degree at most two,
all of \(A_\ell\) lies in one fixed fourth fibre \(x^B=z_\ell\).

The six fibres \(z_\ell\) are pairwise distinct. If two Fano-minus-one lines
shared the same fourth fibre, their distinct affine lines would meet at their
shared label point. The all-\(z\) source identity would then force the complete
factor \(X^B-z_\ell\) into that label's residual, contradicting the
no-additional-complete-fibre condition.

For each line there is a nonzero pair \((\alpha_\ell,\beta_\ell)\) such that

\[
 \alpha_\ell F(x)+\beta_\ell G(x)=0\qquad(x\in A_\ell).
\]

In particular \(|A_\ell|\le L:=\max(\deg F,\deg G)\le\lambda\).

### 3. Uniform dyadic descent

At a descent stage suppose

\[
 F(X)=f(X^M),\qquad G(X)=h(X^M),\qquad M\mid B,
\]

with \(\gcd(f,h)=1\), and put \(b=B/M\). The reduced source identity is
invariant under \(X\mapsto\zeta X\) for \(\zeta\in\mu_M\). Since \(S\) is
root-free on \(H\), each reduced residual root set, and hence every
\(A_\ell\), is \(\mu_M\)-invariant.

Define

\[
 \Sigma_\ell=\{x^M:x\in A_\ell\},
 \qquad
 \tau_\ell=|\Sigma_\ell|=|A_\ell|/M.
\]

The six sets are disjoint, every element of \(\Sigma_\ell\) has
\(b\)-th power \(z_\ell\), and

\[
 0\le\tau_\ell\le L_M:=\max(\deg f,\deg h)\le\lfloor\lambda/M\rfloor,
\]

\[
 \sum_{\ell=1}^6\tau_\ell>5\lambda/M.
\]

For \(u\in\mu_b\), set

\[
 \Psi_u(Z)=f(uZ)h(Z)-f(Z)h(uZ).
\]

If every nonidentity \(\Psi_u\) were nonzero, counting ordered pairs in the
six quotient sets and using the separate root at zero would give

\[
 \sum_{\ell=1}^6\tau_\ell(\tau_\ell-1)
 \le(b-1)(2L_M-1).                                      \tag{1}
\]

Put

\[
 L_0=\lfloor\lambda/M\rfloor,
 \qquad
 T_0=\lfloor5\lambda/M\rfloor+1.
\]

Among six integers in \([0,L_0]\) with sum at least \(T_0\), convexity
minimizes the left side of (1) at the balanced distribution. Writing
\(T_0=6q+s\), \(0\le s<6\), that minimum is

\[
 Q_{\min}=s(q+1)q+(6-s)q(q-1).
\]

The exact standard-library replay exhausts every
\(\lambda\in[15,900,28,897]\) and every dyadic stage with \(b\ge4\), and
verifies

\[
 Q_{\min}>(b-1)(2L_0-1).                                \tag{2}
\]

The unique worst margin is one, at

\[
 (b,M,\lambda,L_0,T_0)=(4,8192,16384,2,11).
\]

Thus some nonidentity comparison polynomial vanishes identically. Coprimality
then implies that all exponents of \(f\) and \(h\) are divisible by the
nontrivial power-of-two order of \(u\). Hence the composition strictly deepens.
Iterating while \(b\ge4\) reaches \(M\ge B/2=16,384\).

### 4. Terminal contradiction and union floor

At the terminal stage, the squarefree split root set of each
\(\bar\rho_i\) is invariant under the free \(\mu_M\)-action. Therefore
\(M\mid r\), and in particular \(16,384\mid r\). But

\[
 50,604=63,601-12,997\le r\le63,601,
\]

while

\[
 49,152<50,604\le r\le63,601<65,536.
\]

There is no multiple of \(16,384\) in this interval. This contradiction proves
\(n_3\le5\lambda\).

Let \(N=|U\setminus\mathrm{Base}|\). Outside the base, occupancy is at most
three, so

\[
 7r\le2N+n_3\le2N+5\lambda.
\]

Consequently

\[
 |U|\ge c+\left\lceil\frac{7r-5\lambda}{2}\right\rceil
      =\left\lceil\frac{7d-5w}{2}\right\rceil
      =150,361.
\]

## Replay

Run

```bash
python3 experimental/scripts/verify_rank16_fixed27_quartic_high_triple.py
python3 -O experimental/scripts/verify_rank16_fixed27_quartic_high_triple.py
```

Both modes must match
`experimental/data/certificates/rank16-fixed27-quartic-high-triple/verify_rank16_fixed27_quartic_high_triple.expected.txt`.
The replay checks all 181,972 stage/parameter pairs, the exact worst margin,
the terminal interval, the union arithmetic, and three mutation cases.

## Audit provenance

The frozen independent hostile audit returned `ACCEPT` with no fatal gap.
Its public response has SHA-256
`189427052020d3552ddc692d62d93bf01b1dc0d290f9be6919dbbbc3b6dcdd3e`.
The audit did not rely on the claimant's unavailable verifier attachment; the
published replay was reconstructed independently and then checked in ordinary
and optimized Python.

## Exact impact

The inherited local floor is \(141,686\). This theorem raises it to
\(150,361\), an increase of \(8,675\), inside the literal fixed-27
primitive-quartic source cell.

No amount is charged to a global ledger. The official score remains `0/2`.

## Nonclaims and next wall

This note does not prove:

- exclusion of the low-triple branch \(n_3\le5\lambda\);
- a fixed-27 quartic cap of six;
- unconditional exclusion or existence of seven labels;
- a global first-match owner or source-cell aggregation theorem;
- the same-word rank-16 deficit/add-back inequality;
- rank-16 closure, Grand MCA, Grand List, or an asymptotic theorem;
- any official score movement.

The next exact local wall is the low-triple branch. A bridge theorem showing
that every literal seven-label primitive-quartic cell forces
\(n_3>5\lambda\) would combine with this note to prove the local quartic cap
of six. Even then, a witness-exhaustive global owner and same-word add-back
argument would still be required before any score-facing payment.
