# Exchange-excess simple-pole separation

**Status:** PROVED finite theorem / LOWER compiler / AUDIT.

The general collision-aware simple-pole conversion charges every pair of
listed polynomials by the degree ceiling \(k\). Locator-prefix
lists carry more information. After their common support core is removed, a
pair can collide only at as many off-domain poles as its exchange distance
exceeds the minimum prefix distance.

This gives a pair-weighted replacement for the uniform \(k\)-loss. On a
minimum-exchange family every off-domain pole separates every listed word, so
the extension-size condition disappears completely on that stratum.

The low-excess factorization is compatible with
`experimental/notes/l1/l1_prefix_low_excess_norm_sieve.md`. The new content
here is its transport to pole collisions, the weighted pole average, the
distinct-slope lower compiler, and the exact source-line replay. No manuscript
file is edited.

Verifier:
`experimental/scripts/verify_exchange_excess_pole_separation.py`
(stdlib only, deterministic, no files written):

    rows=5
    fibers=103
    pairs=2205
    minimum_exchange_pairs=1287
    sharp_positive_excess_pairs=496
    separator_gain_fibers=15
    source_lines=103
    RESULT: PASS (18195 checks)

## 1. Prefix-list setup

Let

\[
 D\subseteq \mathbb B\subseteq\mathbb F,\qquad
 n=|D|,\qquad q_{\rm line}=|\mathbb F|>n.
\]

Fix a target line-code dimension \(k\ge1\), let
\(C=\operatorname{RS}_{\mathbb F}(D,k)\), and fix an agreement \(m\) with

\[
 w=m-k-1\ge0.
\]

For an \(m\)-set \(S\subseteq D\), write

\[
 Q_S(X)=\prod_{x\in S}(X-x)
\]

and let \(\Phi_w(S)\) be its first \(w\) coefficients below the leading
coefficient. Fix one prefix fiber and a subfamily

\[
 \mathcal G\subseteq\Phi_w^{-1}(z),\qquad L=|\mathcal G|.
\]

For distinct \(S,T\in\mathcal G\), put

\[
 t_{S,T}=d_J(S,T)=|S\setminus T|,\qquad
 e_{S,T}=t_{S,T}-(w+1),
\]

and define the total exchange excess

\[
 E(\mathcal G)=\sum_{\{S,T\}\in\binom{\mathcal G}{2}}e_{S,T}.       \tag{1}
\]

Prefix rigidity says \(e_{S,T}\ge0\).

## 2. Pairwise collision theorem

### Theorem 2.1 (exchange-excess pole bound)

For distinct \(S,T\in\mathcal G\), let

\[
 I=S\cap T,\qquad A=S\setminus T,\qquad B=T\setminus S.
\]

Then

\[
 Q_S-Q_T=Q_I(Q_A-Q_B),\qquad
 \deg(Q_A-Q_B)\le e_{S,T}.                                 \tag{2}
\]

Consequently,

\[
 \#\{\alpha\in\mathbb F\setminus D:
       Q_S(\alpha)=Q_T(\alpha)\}\le e_{S,T}.                \tag{3}
\]

#### Proof

The common-core factorization in (2) is immediate. The shared depth-\(w\)
prefix and cancellation of the leading monic term give

\[
 \deg(Q_S-Q_T)\le m-w-1=k.
\]

Since \(\deg Q_I=m-t_{S,T}\), division by the nonzero common-core locator
gives

\[
 \deg(Q_A-Q_B)
 \le k-(m-t_{S,T})
 =t_{S,T}-(w+1)=e_{S,T}.
\]

For \(\alpha\notin D\), \(Q_I(\alpha)\ne0\). Thus a pole collision is exactly
a root of the nonzero reduced gap \(Q_A-Q_B\), proving (3).
\(\square\)

### Corollary 2.2 (minimum exchange is automatically separated)

If \(d_J(S,T)=w+1\), then \(Q_A-Q_B\) is a nonzero constant. Hence
\(Q_S(\alpha)\ne Q_T(\alpha)\) for every \(\alpha\in\mathbb F\setminus D\).

In particular, if every distinct pair in \(\mathcal G\) has minimum exchange,
then every off-domain pole separates all \(L\) members. No lower bound on
\(q_{\rm line}-n\), beyond existence of a pole, is needed.

## 3. Weighted pole average

For \(\alpha\in\mathbb F\setminus D\), let

\[
 C_\alpha=
 \#\{\{S,T\}\in\binom{\mathcal G}{2}:Q_S(\alpha)=Q_T(\alpha)\}.
\]

Summing (3) pair by pair gives

\[
 \sum_{\alpha\in\mathbb F\setminus D}C_\alpha
 \le E(\mathcal G).                                       \tag{4}
\]

Therefore some pole satisfies

\[
 C_\alpha\le
 \left\lfloor\frac{E(\mathcal G)}{q_{\rm line}-n}\right\rfloor. \tag{5}
\]

Let \(M_\alpha\) be the number of distinct values among
\(\{Q_S(\alpha):S\in\mathcal G\}\). If their multiplicities are
\(r_1,\ldots,r_{M_\alpha}\), then

\[
 \sum_i r_i=L,\qquad
 \sum_i r_i^2=L+2C_\alpha.
\]

Cauchy--Schwarz and (5) yield

\[
 \boxed{
 M_\alpha\ge
 \left\lceil
 \frac{L^2}
 {L+2\left\lfloor E(\mathcal G)/(q_{\rm line}-n)\right\rfloor}
 \right\rceil
 }\ .                                                       \tag{6}
\]

The slightly weaker smooth form is

\[
 M_\alpha\ge
 \left\lceil
 \frac{L^2(q_{\rm line}-n)}
 {L(q_{\rm line}-n)+2E(\mathcal G)}
 \right\rceil.                                             \tag{7}
\]

If \(q_{\rm line}-n>E(\mathcal G)\), (5) gives \(C_\alpha=0\), so
\(M_\alpha=L\).

If every pair has \(e_{S,T}\le d\), then
\(E(\mathcal G)\le d\binom L2\), and (7) becomes

\[
 \boxed{
 M_\alpha\ge
 \left\lceil
 \frac{L(q_{\rm line}-n)}
 {q_{\rm line}-n+d(L-1)}
 \right\rceil
 }\ .                                                       \tag{8}
\]

This is the collision-aware simple-pole bound with the target dimension
\(k\) replaced by the maximum exchange excess \(d\). It is never weaker:
\(0\le e_{S,T}\le k\).

There is also an automatic geometry-only choice. Any two \(m\)-sets have
\(t_{S,T}\le\min(m,n-m)\). Taking
\(d=\max_{\{S,T\}}e_{S,T}\), whenever \(L\ge2\),

\[
 d\le d_{\rm geom}
 =\min\{k,n-m-w-1\}
 =\min\{k,n-2m+k\}.                                      \tag{9}
\]

The second entry is nonnegative precisely because a nonsingleton prefix
fiber must satisfy \(m\le(n+k)/2\). At equality, \(d_{\rm geom}=0\):
every off-domain pole separates the entire prefix fiber.

### Coordinate-load identity

Put

\[
 r_x=|\{S\in\mathcal G:x\in S\}|\qquad(x\in D).
\]

Each unordered pair contributes \(2t_{S,T}\) to
\(\sum_xr_x(L-r_x)\). Therefore

\[
 \boxed{
 E(\mathcal G)
 =\frac12\sum_{x\in D}r_x(L-r_x)
  -(w+1)\binom L2
 }\ .                                                       \tag{10}
\]

Thus the weighted separator can be evaluated from coordinate loads without
enumerating all poles or factoring every locator difference.

## 4. MCA lower compiler

Let

\[
 U_z(X)=X^m+\sum_{i=1}^wz_iX^{m-i},\qquad
 P_S=U_z-Q_S.
\]

Then \(\deg P_S\le k\). For a pole \(\alpha\in\mathbb F\setminus D\), set

\[
 f_\alpha(x)=\frac{U_z(x)}{x-\alpha},\qquad
 g_\alpha(x)=-\frac1{x-\alpha}\qquad(x\in D).
\]

The slope attached to \(S\) is

\[
 \gamma_S=P_S(\alpha)=U_z(\alpha)-Q_S(\alpha),
\]

and its explaining polynomial is

\[
 h_S(X)=\frac{P_S(X)-P_S(\alpha)}{X-\alpha},
 \qquad \deg h_S<k.
\]

On \(S\), \(f_\alpha+\gamma_Sg_\alpha=h_S\). The word \(g_\alpha\) cannot
agree with a degree-\(<k\) polynomial on \(k+1\) points: otherwise
\((X-\alpha)h+1\) would be a nonzero degree-\(\le k\) polynomial with too
many roots. Hence every distinct value counted by (6)--(8), with either the
measured, uniform, or geometric excess bound, is an actual
support-wise MCA-bad slope at agreement \(m\).

For a nonempty challenge set \(\Gamma\subseteq\mathbb F\), the standard line
shear translates the bad-slope set. Starting with the integer lower bound
\(M\) from (6), the challenge-restricted conclusion is

\[
 B^{\rm MCA}_{C,\Gamma}(m)
 \ge \left\lceil\frac{|\Gamma|M}{q_{\rm line}}\right\rceil. \tag{11}
\]

The inner ceiling in (6) is retained before applying (11).

### Corollary 4.1 (exchange-sensitive identity-prefix pole floor)

Pigeonholing the \(\binom nm\) supports over their \(|\mathbb B|^w\)
prefixes gives

\[
 L_0(m)=\left\lceil\binom nm|\mathbb B|^{-w}\right\rceil.
\]

Put

\[
 d_m=\max\{0,\min(k,n-2m+k)\}.
\]

If \(L_0(m)=1\), the one-slope conclusion below is immediate. Otherwise,
applying (8) with the geometry cap (9) to any \(L_0(m)\) members of a
largest prefix fiber gives

\[
 M_{\rm ex}(m)=
 \left\lceil
 \frac{L_0(m)(q_{\rm line}-n)}
 {q_{\rm line}-n+d_m(L_0(m)-1)}
 \right\rceil                                             \tag{12}
\]

actual MCA-bad slopes. For a challenge set \(\Gamma\), this gives the nested
integer floor

\[
 B^{\rm MCA}_{C,\Gamma}(m)
 \ge
 \left\lceil\frac{|\Gamma|M_{\rm ex}(m)}{q_{\rm line}}\right\rceil.
 \tag{13}
\]

The existing identity-prefix floor is (12) with \(d_m\) replaced by \(k\).
Thus (12) is never weaker and is strictly stronger whenever the geometry cap
changes the resulting integer quotient.

## 5. Relation to existing bounds

The general collision-aware pole theorem knows only that two listed
degree-\(\le k\) polynomials have at most \(k\) common evaluation poles. It
therefore pays \(k\binom L2\). For a locator-prefix list, (2) removes the
common support core first and replaces that uniform cost by
\(E(\mathcal G)\).

The improvement is strict whenever the family has average exchange below
the disjoint-support extreme. It is especially sharp on the first few
exchange shells:

    minimum shell:       e=0, every pole separates;
    first excess shell:  e=1, at most one bad pole per pair;
    d excess shells:     old k is replaced by d.

This does not assert that a large low-excess subfamily exists in every large
prefix fiber. It gives the exact lower compiler to use when such shell
information has been proved or certified.

This direct pole compiler is also distinct from the collision-free
identity-prefix list floor followed by a deep-point conversion. That route
avoids evaluating the prefix list at a pole; (6)--(13) instead sharpen the
actual pole-collision and direct MCA-slope count.

## 6. Independent exact replay

The verifier enumerates five prime-field rows:

    (p,n,m,k)=(11,6,3,2), (13,8,4,2), (13,11,7,3),
                (17,10,5,2), (19,10,5,3).

For every nonsingleton prefix fiber it independently:

1. expands the two full locators and the common-core factor route;
2. compares the reduced-gap degree with the exchange excess;
3. enumerates every off-domain root and every direct pole collision;
4. checks the weighted sum (4), the integer and smooth Cauchy bounds, the
   uniform-\(d\) corollary, and the load identity (10); and
5. constructs a simple-pole received line, verifies every displayed
   explanation and support-wise nontriviality condition, and replays the
   nested challenge-shear ceiling.

For each row it also replays the identity-prefix pigeonhole floor, the
geometry-capped bound (12), and the nested challenge conclusion (13). The
first row has prefix depth zero, while the third has \(L_0(m)=1\).

The 496 positive-excess pairs attaining the root ceiling show that (3) cannot
be uniformly lowered. Fifteen fibers satisfy the new collision-free criterion
while the old \(k\binom L2\) union bound cannot certify a separator.

## 7. Claim ledger

| Claim | Status |
|---|---|
| Common-core reduction has degree at most exchange excess | **PROVED** |
| A pair has at most \(e_{S,T}\) off-domain colliding poles | **PROVED** |
| Total pole-collision mass is at most \(E(\mathcal G)\) | **PROVED** |
| Integer Cauchy bound (6) and uniform-\(d\) bound (8) | **PROVED** |
| Automatic geometry cap (9) and coordinate-load identity (10) | **PROVED** |
| The resulting values are actual MCA-bad slopes | **PROVED** |
| Every large prefix fiber has a large low-excess subfamily | **NOT CLAIMED** |
| Primitive Q, SP, BCI, A4, or dense-band restriction | **NOT CLAIMED** |
| A new safe upper bound, deployed threshold, or prize theorem | **NOT CLAIMED** |

## 8. Reproduction

From the repository root:

    python3 -W error -m py_compile \
      experimental/scripts/verify_exchange_excess_pole_separation.py
    python3 -W error \
      experimental/scripts/verify_exchange_excess_pole_separation.py
