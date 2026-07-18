# Affine-prefix line compiler and same-row fibre bifurcation

## Status

This note proves an exact finite Reed--Solomon line theorem and a matched
same-row counterexample to any automatic projection from support-fibre data to
the final slope image.

The generic witness/first-match interfaces overlap PR #882, and the separating
pole mechanism overlaps PR #888. The new theorem is the closed-form
affine-prefix specialization, its exact second-projection multiplicities, and
the direct-versus-pole comparison for the identical support fibre in the same
`k = m - 1` row.

The theorem is line-specific. It does not establish a semantic C1--C9 atlas,
Grand MCA hard input 2, a deployed payment, or score movement.

## Exact two-stage projection identity

Let a witness cell `C` consist of triples `(gamma,S,h)`. Define

```text
R(C) = {(gamma,h): (gamma,S,h) in C for some S},
Z(C) = {gamma: (gamma,h) in R(C) for some h},
nu_C(gamma,h) = #{S: (gamma,S,h) in C},
mu_C(gamma) = #{h: (gamma,h) in R(C)}.
```

Then

\[
 |Z(C)|
 =\sum_{(\gamma,h)\in R(C)}\frac1{\mu_C(\gamma)}
 =\sum_{(\gamma,S,h)\in C}
   \frac1{\nu_C(\gamma,h)\mu_C(\gamma)}.
\]

This is an exact identity: the first sum contributes one on every slope fibre,
and the second lifts every explanation state through its support witnesses.

## Affine-prefix line theorem

Let `F` be a finite field, let `D` be a subset of `F` of size `n`, and let

\[
 1\le k<m\le n,\qquad d=m-k.
\]

For an `m`-set \(S\subseteq D\), write its monic locator as

\[
 Q_S(X)=X^m+c_1(S)X^{m-1}+\cdots+c_m(S)
\]

and put

\[
 \Phi_d(S)=(c_1(S),\ldots,c_d(S)),
 \qquad
 \operatorname{Fib}_d(y)=\{S:\Phi_d(S)=y\}.
\]

Choose \(z,b\in F^d\) and \(u,v\in F[X]_{<k}\), and define received
polynomial representatives

\[
 R_0=X^m+\sum_{i=1}^d z_iX^{m-i}+u,
 \qquad
 R_1=\sum_{i=1}^d b_iX^{m-i}+v.
\]

### Theorem 1

If \(b\ne0\), the complete exact-\(m\) noncommon witness incidence of the
received line \((R_0+\gamma R_1)|_D\) is

\[
 \mathcal W_m=
 \{(\gamma,S,R_0+\gamma R_1-Q_S):
   \gamma\in F,\ S\in\operatorname{Fib}_d(z+\gamma b)\}.
\]

Every displayed witness has full agreement set exactly \(S\), and

\[
 Z_m=\{\gamma:\operatorname{Fib}_d(z+\gamma b)\ne\varnothing\}.
\]

For every occupied slope,

\[
 \nu(\gamma,h)=1,
 \qquad
 \mu(\gamma)=|\operatorname{Fib}_d(z+\gamma b)|.
\]

Consequently

\[
 |Z_m|=
 \left|\Phi_d\!\left(\binom Dm\right)\cap(z+Fb)\right|.
\]

Every partition of the affine prefix line \(z+Fb\) induces a
witness-exhaustive partition with pairwise disjoint actual slope images.
Therefore every ordering is a first-match ordering and its slope counts add
exactly.

If \(b=0\), the exact-\(m\) noncommon witness incidence is empty: \(R_1=v\)
is itself a degree-\(<k\) code polynomial, so every explanation is simultaneous
after translation by \(\gamma v\).

### Proof

If \(\Phi_d(S)=z+\gamma b\), then \(R_0+\gamma R_1\) and \(Q_S\)
have identical coefficients in degrees \(m,m-1,\ldots,k\). Hence

\[
 h_{\gamma,S}=R_0+\gamma R_1-Q_S
\]

has degree less than \(k\). On `D`, the error polynomial is exactly \(Q_S\),
so its complete zero set is exactly \(S\).

Conversely, an exact-\(m\) witness gives a monic degree-\(m\) error polynomial
with the `m` roots in \(S\), and therefore that error polynomial is \(Q_S\).
Comparing its first `d` nonleading coefficients recovers
\(\Phi_d(S)=z+\gamma b\).

For fixed \((\gamma,h)\), equality of two displayed locators forces \(S=T\),
so \(\nu=1\). For fixed \(\gamma\), different supports give different
explanation polynomials, so \(\mu\) is the prefix-fibre size. Finally, when
\(b\ne0\), the map \(\gamma\mapsto z+\gamma b\) is injective, proving the
partition and add-back statement.

## Same-row one-slope versus many-slope bifurcation

Fix a nonempty complete prefix fibre

\[
 \mathcal F_z=\operatorname{Fib}_d(z),
 \qquad |\mathcal F_z|=L.
\]

The direct affine-prefix line has a cell with

\[
 |C_{\rm dir}|=|R_{\rm dir}|=L,
 \qquad |Z_{\rm dir}|=1,
 \qquad \nu=1,
 \qquad \mu=L.
\]

Assume

\[
 |F|>n+(k-1)\binom L2.                                 \tag{1}
\]

For distinct \(S,T\in\mathcal F_z\), the polynomial \(Q_S-Q_T\) has
degree at most \(k-1\). Inequality (1) therefore supplies an
\(\alpha\in F\setminus D\) for which the \(Q_S(\alpha)\) are pairwise
distinct.

Define received words on `D` by

\[
 p_0(x)=\frac{R_0(x)}{x-\alpha},
 \qquad
 p_1(x)=-\frac1{x-\alpha},
\]

and, for \(S\in\mathcal F_z\), put

\[
 \gamma_S=R_0(\alpha)-Q_S(\alpha),
 \qquad
 g_S(X)=\frac{R_0(X)-Q_S(X)-\gamma_S}{X-\alpha}.
\]

The numerator defining \(g_S\) has degree at most \(k-1\) and vanishes at
\(\alpha\), so \(\deg g_S<k\). Moreover,

\[
 p_0+\gamma_Sp_1-g_S=\frac{Q_S}{X-\alpha}
\]

on `D`. Thus the full agreement set is exactly \(S\). The separator makes all
\(\gamma_S\) distinct, and \(p_1\) is noncommon: agreement with a
degree-\(<k\) polynomial on \(k+1\) points would make a nonzero degree-\(k\)
polynomial have at least \(k+1\) roots.

The pole target cell therefore satisfies

\[
 |C_{\rm pole}|=|R_{\rm pole}|=|Z_{\rm pole}|=L,
 \qquad \nu=\mu=1.
\]

The pole target may be placed first and later cells may complete the line; no
claim about the full pole-line slope set is needed.

The direct and pole cells use the identical support fibre. Hence their exact
agreement sets, explanation-state counts, first-projection occupancies, and all
support-derived representation moments agree, while their final slope images
have sizes one and \(L\). Support data alone therefore cannot determine the
second projection.

## Characteristic-five affine-square family

For every \(B\ge2\), choose an \(F_5\)-basis

\[
 a_1,u_1,v_1,\ldots,a_B,u_B,v_B
\]

of \(F_{5^{3B}}\), and define the `4B`-point domain

\[
 D_B=\{a_i+\epsilon u_i+\eta v_i:
       1\le i\le B,\ \epsilon,\eta\in\{0,1\}\}.
\]

Take \(m=2B\) and \(k=2B-1\), so \(d=1\). A block signature records local
cardinality and the two coordinate sums. The only repeated local signature is
the size-two signature of the two diagonals. Therefore

\[
 Q(y)=1+4y+4y^2+4y^3+y^4,
 \qquad
 P(y)=Q(y)+y^2.
\]

A syndrome with exactly `j` ambiguous blocks has prefix-fibre size \(2^j\),
and the number of such syndromes is

\[
 L_{B,j}=\binom Bj[y^{2(B-j)}]Q(y)^{B-j}.               \tag{2}
\]

The identities

\[
 \sum_jL_{B,j}=[y^{2B}]P(y)^B,
 \qquad
 \sum_j2^jL_{B,j}=\binom{4B}{2B}
\]

follow by distinguishing syndrome fibres and then their supports.

The affine-prefix theorem gives an explicit `B+1`-cell line atlas with

\[
 |Z_{B,j}|=L_{B,j},
 \qquad
 |C_{B,j}|=|R_{B,j}|=2^jL_{B,j},
 \qquad
 \nu=1,
 \qquad
 \mu=2^j.
\]

The top direct cell has one slope and \(2^B\) witnesses. The separator
inequality

\[
 5^{3B}>4B+(2B-2)\binom{2^B}{2}
\]

holds for every \(B\ge2\), so the matched pole cell has \(2^B\) distinct
slopes in the same \(k=2B-1\) row.

Each ambiguous block has three representation outputs with multiplicities
`1,2,1`. Thus, for `j` ambiguous blocks,

\[
 |\operatorname{supp}r|=3^j,
 \qquad \max r=2^j,
 \qquad
 \sum_w r(w)^\tau=(2+2^\tau)^j\quad(\tau\ge0),
\]

where \(\tau=0\) is the zeroth moment over occupied outputs. These quantities
are identical in the direct and pole cells.

Finally, \(Q(1)=14\), so

\[
 L_{B,j}\le\binom Bj14^{B-j}.
\]

For \(\theta=j/B\ge9/10\), the natural-log exponent

\[
 H_e(\theta)+(1-\theta)\ln14-\theta\ln2
\]

is decreasing. At \(\theta=9/10\), its negative is

\[
 \eta_*=\frac{1}{10}\ln\!\left(
 \frac{9^9 2^9}{14\cdot10^{10}}
 \right)
 =0.0348437561509767\ldots>0.
\]

Hence

\[
 10j\ge9B
 \quad\Longrightarrow\quad
 L_{B,j}\le2^j e^{-\eta_*B}.                           \tag{3}
\]

This is a line-local, image-normalized high-switch payment for the constructed
cells. It is not uniform over arbitrary received lines or semantic residual
cells.

For the full direct line the slope denominator is exactly \(5^{3B}\). The top
direct cell contributes \(5^{-3B}\); the matched pole target contributes
\(2^B5^{-3B}\). The agreement fraction is \(m/n=1/2\), while
\(1-k/n=1/2+1/(4B)\).

## Replay

Run

```bash
python3 experimental/scripts/verify_affine_prefix_line_fibre_bifurcation.py
python3 -O experimental/scripts/verify_affine_prefix_line_fibre_bifurcation.py
```

Both modes must match the checked-in expected output. The replay independently
enumerates the `B=2` syndrome histogram, checks (2) for `B=1,...,10`, checks
the representation moments, separator inequality, and high-switch envelope,
and rejects three semantic mutations.

The independent hostile-audit response has SHA-256
`5348a7b6b836d984c88988d611c1ef9291b1d0c0ebc7e718e8030d298780e447`
and returned `ACCEPT` with no fatal gap.

## Nonclaims and next wall

This note does not prove:

- a witness-exhaustive semantic C1--C9 atlas;
- survival of these cells after earlier semantic owners;
- Grand MCA hard input 2 or any other official hard input;
- a deployed-row, complete profile-envelope, or lower-reserve payment;
- a uniform theorem over arbitrary received lines;
- a universal affine-prefix normal form;
- a general C3, C7, C8, or C9 payment;
- the full bad-slope count of the pole line;
- Grand MCA, Grand List, or official score movement.

The next wall is a semantic primitive second-projection/source-incidence
theorem. For every actual primitive first-match cell one must derive an
image-scale bound from the received-line algebra itself, then add those budgets
disjointly across a complete semantic first-match atlas. Support emissions or
representation moments may be used only after that source-incidence map is
proved.
