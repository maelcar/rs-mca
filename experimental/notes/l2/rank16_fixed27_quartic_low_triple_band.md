# Fixed-27 quartic low-triple band exclusion

## Status and exact dependencies

This note proves a finite local theorem for one literal normalized fixed-27,
fixed-generator, fixed-syndrome-projective-ray, first-match,
affine-rank-two primitive-quartic source cell. It is conditional on the exact
source theorem in PR #894 at head

```text
3c048a9637a02525ef41d1c340252200e4b0f41a
```

and the exact high-triple theorem in PR #902 at head

```text
f2be578d5b17d546c0cd4437e4927e74c9e47f7c
```

over the frozen public baseline

```text
origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e.
```

The theorem removes one more finite band inside that local source cell. It
does not establish that the cell exists, aggregate cells, pay a ledger row, or
change the official score.

## Literal source cell

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

Fix a literal source cell satisfying every hypothesis of PR #894: seven
distinct labels \(y_0,\ldots,y_6\in\Lambda\setminus C\), nonzero source
scalars \(q_i\), monic squarefree \(H\)-split residuals \(R_i\), and
quotients \(W_i\) such that

\[
 (X^B-y_i)R_i=q_i h+gW_i,
 \qquad \deg R_i=d,
 \qquad \deg W_i\le w.
\]

The cell retains the inherited core-fibre avoidance, selected-fibre
avoidance, no-additional-complete-fibre, same-word, same-ray, same-generator,
and first-match restrictions. In the exact primitive-quartic normalization,
put

\[
 \operatorname{Base}=Z_H(E_1)\cap Z_H(E_2),\qquad
 c=|\operatorname{Base}|\le12,997,
\]

\[
 r=d-c,\qquad \lambda=w-c.
\]

Outside the base, each root has occupancy at most three among the seven
residual root sets. Let \(n_3\) denote the number of outside-base roots with
occupancy exactly three, and let

\[
 U=\bigcup_{i=0}^6 Z_H(R_i).
\]

## Theorem

Under the literal source hypotheses above:

1. There are no six nonempty maximal three-label triple lines.
2. The occupancy-three count satisfies

   \[
   n_3\le5\lambda-7,320.
   \]

3. The seven-residual support satisfies

   \[
   |U|\ge154,021.
   \]

Equivalently, relative to PR #902, the entire integer band

\[
 5\lambda-7,319\le n_3\le5\lambda
\]

is eliminated. The local union floor rises from \(150,361\) to \(154,021\),
an improvement of \(3,660\).

## Proof

### Base and direction-gcd cancellation

Write \(\rho_i=q_i^{-1}R_i\). After cancelling the common base polynomial,
the PR #894 source identities give

\[
 s\bar\rho_i=b_i(X^B)\mathbin{\cdot}(\bar E_1,\bar E_2),
 \qquad \deg\bar\rho_i=r,
 \qquad \deg\bar E_j\le\lambda.
\]

Let \(J=\gcd(\bar E_1,\bar E_2)\). The polynomial \(J\) has no root in
\(H\): such a root would make the original direction pair vanish to order at
least two, while \(s\rho_i\) has valuation one because \(s\) is root-free on
\(H\) and \(\rho_i\) is squarefree.

Factor \(J=QJ_0\) and \(s=QS\) with \(\gcd(J_0,S)=1\). Euclid's lemma gives
\(J_0\mid\bar\rho_i\). Since \(\bar\rho_i\) splits over \(H\), every
nonconstant divisor of it has an \(H\)-root. Since \(J_0\mid J\), this is
impossible unless \(J_0\) is constant. Thus \(J\mid s\), and cancellation
gives

\[
 S\bar\rho_i=b_i(X^B)\mathbin{\cdot}(F,G),
 \qquad \gcd(F,G)=1,
 \qquad L:=\max(\deg F,\deg G)\le\lambda,
\]

with \(S\) root-free on \(H\). Exact affine rank two prevents the reduced
direction pair from collapsing to one dimension.

### Triple lines and the six-line exclusion

An occupancy-three root \(x\), with \(z=x^B\), makes the three corresponding
rows \(b_i(z)\) annihilate the same nonzero vector \((F(x),G(x))\). The
source formula

\[
 b_i(z)=\frac{z-y_i}{a_0(z)}\bigl(c_i-c(z)\bigr)
\]

has no zero denominator under the source hypotheses. Hence the three label
points lie on a unique maximal affine line. Every such line \(\ell\) has an
assigned-root set \(A_\ell\), and a nonzero constant combination of \(F,G\)
vanishes there. Therefore

\[
 |A_\ell|\le L\le\lambda.
\]

No line contains five labels: its affine equation would give a nonzero
polynomial of degree at most four vanishing at five label values, contradicting
the linear independence inherited from exact affine rank two. Distinct
maximal lines use disjoint label pairs. If one maximal line contains four
labels, at most four triple-carrying lines exist, so \(n_3\le4\lambda\).

If all maximal lines contain three labels, their label triples form a linear
3-uniform hypergraph on seven vertices. Seven lines would be the Fano matroid,
which is not representable in the odd characteristic of \(F\). Six lines are
necessarily Fano-minus-one.

For a three-label line \(\ell=\{i,j,k\}\), PR #894 gives

\[
 \det(b_i,b_j)=a_0\delta_{ij},
 \qquad 0\ne\delta_{ij},
 \qquad \deg\delta_{ij}\le2.
\]

Label collinearity provides the root \(y_k\) of \(\delta_{ij}\). Every root
assigned to \(\ell\) supplies another root \(z=x^B\ne y_k\), so all of
\(A_\ell\) lies in one fixed fourth fibre \(z_\ell\). In a six-line
Fano-minus-one family, the six fourth fibres are distinct and avoid all seven
labels. The six corresponding projective split quartics therefore form a
complete quadrilateral, or Pasch configuration, with root-multiplicity
profile

\[
 (n_1,n_2,n_3,n_{\ge4})=(6,3,4,0).
\]

The independent finite census over \(\mu_{64}\) enumerates all \(41,664\)
split cubics, \(23,296\) actual pairwise-root-disjoint collinear cubic
triples, \(635,376\) split quartics, and \(1,281,280\) concurrent quartic
triples. It finds \(11,328\) unique Pasch configurations, represented by
\(67,968\) oriented completion paths. Their complete profile partition is

\[
 (8,2,4,0)\quad\text{for }10,880\text{ configurations},
\]

\[
 (12,0,4,0)\quad\text{for }448\text{ configurations}.
\]

There is no configuration with profile \((6,3,4,0)\). A separate synthetic
positive control produces six oriented paths and one unique target
configuration. Hence six nonempty maximal three-label lines are impossible.

### The deployed bound \(n_3\le2r\)

The inequality used below is not a generic weighted-hypergraph fact. It uses
the exact line cap and the deployed range

\[
 r-2\lambda=d-2w+c=5,807+c>0.
\]

For at most four lines, \(n_3\le4\lambda<2r\). A five-line linear triple
family on seven labels has one of two degree sequences:

\[
 (3,2,2,2,2,2,2),\qquad (3,3,2,2,2,2,1).
\]

In the first case, the unique degree-three label controls three line weights
of total at most \(r\), and the two remaining lines contribute at most
\(2\lambda\). In the second case, the two degree-three labels share exactly
one line and their incident-line sets cover all five lines; summing their
vertex-capacity bounds gives \(n_3+w_{\rm shared}\le2r\). Thus in every
deployed case

\[
 n_3\le2r.
\]

### Divisibility-aware five-cell descent

Assume for contradiction that

\[
 n_3\ge5\lambda-7,319. \tag{1}
\]

Since \(\lambda\ge15,900\), (1) is strictly larger than \(4\lambda\). Thus
no four-label maximal line occurs. The six-line case has already been
excluded, so there are at most five three-label lines.

At a dyadic composition stage write

\[
 F(X)=f(X^M),\qquad G(X)=h(X^M),\qquad M\mid B,
\]

with \(\gcd(f,h)=1\), and put

\[
 b=B/M,\qquad L_M=\max(\deg f,\deg h),
 \qquad L_0=\lfloor\lambda/M\rfloor.
\]

The reduced residual root sets and every assigned-root set are invariant under
the free \(\mu_M\)-action. Hence

\[
 M\mid r,\qquad M\mid n_3.
\]

For the at most five line sets, define

\[
 \Sigma_\ell=\{x^M:x\in A_\ell\},\qquad
 \tau_\ell=|\Sigma_\ell|=|A_\ell|/M\le L_0.
\]

For \(u\in\mu_b\), put

\[
 \Psi_u(Z)=f(uZ)h(Z)-f(Z)h(uZ).
\]

If \(\Psi_u\ne0\), its top term cancels when the two degrees agree, and
\(\Psi_u(0)=0\). Thus it has at most \(2L_M-2\) relevant nonzero roots.
If every nonidentity comparison polynomial were nonzero, ordered-pair counting
within the five quotient sets would give

\[
 \sum_{\ell=1}^5\tau_\ell(\tau_\ell-1)
 \le(b-1)(2L_0-2). \tag{2}
\]

The least multiple of \(M\) allowed by (1) is

\[
 n_{\min}=M\left\lceil\frac{5\lambda-7,319}{M}\right\rceil,
 \qquad T_0=n_{\min}/M.
\]

States with \(n_{\min}>2r\) are impossible by the deployed bound above.
States with \(T_0>5L_0\) are impossible by the five cell capacities. In every
remaining state, convexity minimizes the left side of (2) by balancing
\(T_0\) among five cells. Writing \(T_0=5q+s\), \(0\le s<5\), the minimum is

\[
 Q_5(T_0)=s(q+1)q+(5-s)q(q-1).
\]

The exact finite replay checks all \(25,996\) pairs

\[
 0\le c\le12,997,\qquad M\le8,192,\qquad M\mid r.
\]

It finds \(19,346\) feasible comparison states, \(6,647\) interval-infeasible
states, and three capacity-infeasible states. Every feasible state satisfies

\[
 Q_5(T_0)>(B/M-1)(2L_0-2).
\]

The unique minimum margin is \(28\), at

\[
 \begin{aligned}
 &(c,\lambda,r,M,b,n_{\min},T_0,L_0)\\
 &\qquad=(12,401,16,496,51,200,2,048,16,75,776,37,8),
 \end{aligned}
\]

where \(Q_5(T_0)=238\) and the right side is \(210\). This contradicts
(2), so some nonidentity \(\Psi_u\) vanishes identically.

From \(\Psi_u=0\) and \(\gcd(f,h)=1\), one obtains

\[
 f(uZ)=\alpha f(Z),\qquad h(uZ)=\alpha h(Z).
\]

The common exponent residue is zero, since a positive residue would make both
polynomials divisible by \(Z\). Therefore \(f,h\in F[Z^m]\) for the
nontrivial power-of-two order \(m\) of \(u\), and the composition depth
strictly increases. Iteration reaches \(M\ge16,384\).

But \(M\mid r\), while

\[
 49,152<50,604\le r\le63,601<65,536.
\]

This interval contains no multiple of \(16,384\). The contradiction proves

\[
 n_3\le5\lambda-7,320.
\]

The replay also tests the next integer. Replacing \(7,319\) by \(7,320\) in
the contradiction assumption gives minimum certificate margin \(-6,766\) at

\[
 (c,\lambda,r,M)=(12,997,15,900,50,604,1).
\]

This is only sharpness of this comparison certificate. It is not a
source-realized witness and does not show that the surviving region is
nonempty.

### Union floor

Let \(N=|U\setminus\operatorname{Base}|\). Since outside-base occupancy is at
most three,

\[
 7r\le2N+n_3.
\]

Using the new bound,

\[
 |U|\ge c+\left\lceil\frac{7r-5\lambda+7,320}{2}\right\rceil
 =\frac{7d-5w+7,320}{2}
 =154,021.
\]

## Replay and provenance

The independent hostile proof audit returned `ACCEPT_NARROWED`. The frozen
audit packet and public response hashes are

```text
packet: ad0e2148a160d54643ecac1ad1a30737b16c982b744a872c3bb096db0affa144
final:  1a3a83de083162a0ab4f9e130c4710695efcfe5dcd4118b3c7ee3d1bc6e93c33
```

The claimant's advertised verifier files and certificate bundle were absent
from its frozen return and are not consumed here. This package instead ships
the independent auditor's captured sources and fresh exact outputs.

Run the ordinary replay, optimized replay, and tamper self-test with

```bash
python3 experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py
python3 -O experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py
python3 experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py --tamper-selftest
```

The full split-quartic census is reproducible from its fully readable C++17
source when a local compiler is available:

```bash
python3 experimental/scripts/verify_rank16_fixed27_quartic_low_triple.py --full-census
```

The default replay verifies the complete certificate manifest, replays the
three Python certificates, checks the exact arithmetic endpoints and
one-integer sharpness test, and validates the frozen full-census transcript.
The full-census mode recompiles the inspected C++17 source and requires exact
transcript equality.

## Nonclaims and exact wall

This theorem does not establish:

* existence of the assumed seven-label primitive-quartic source cell;
* exclusion of every seven-label quartic source cell;
* fixed-27 quartic cap six;
* impossibility of the surviving region \(n_3\le5\lambda-7,320\);
* a source-realized extremizer or counterexample;
* a theorem for the separate cubic branch;
* global first-match ownership, source-cell disjointness, or add-back;
* rank-16 parent closure, recurrence, or asymptotic payment;
* Grand List, Grand MCA, a ledger payment, or score movement.

The official score remains `0/2`. The exact remaining wall is either a source
theorem excluding the surviving low-triple region or a global owner/add-back
theorem that converts local cells into a nonoverlapping paid contribution.
