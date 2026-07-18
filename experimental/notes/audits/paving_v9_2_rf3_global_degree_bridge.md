# Paving v9.2 RF3'' global-degree retained-factor bridge

Status: PROVED

## Result

This note proves the standalone global-degree retained-factor bridge requested
by the source audit of `experimental/RS_MCA_Paving_v9.2.tex`.  It keeps the
original global \((Y,Z)\)-degree of every irreducible factor, pays all global
and specialization contents separately, guards both discriminants and
\(Y\)-leading coefficients at the common specialization point, and treats a
factor linear in \(Y\) by a direct recurrence.

The proof gives the conservative v9.2-compatible threshold

\[
 |S|>(1+2UD_Y^2)D_Z+(r+1)D_Y.                 \tag{RF3''}
\]

It does **not** justify the sharper RF3 or RF3' thresholds: those require the
content-free degree subtraction disproved in the predecessor audit.  It also
does not edit the immutable v9.2 release.  RF3'' can replace the retained-lift
assumption in a future version; the four exact RF3'' row ceilings were already
checked in the predecessor packet.

Two repairs to the printed source chain are load-bearing.

1. For a linear global factor \(R=A(X,Z)Y+B(X,Z)\), the expression
   \(W^{a-2}\partial_YR\) used in BCIKS Claim A.2 has a negative exponent.
   The lift is instead computed directly as \(-B/A\).
2. Even when \(a\ge2\), the Claim A.2 base-case sentence
   \(\Lambda(T)=\Lambda(W)+1\) need not hold.  For example, for
   \(H=Y^2+Z^3\), with global bound \(g=3\), one has
   \(\Lambda(T)=2\), \(W=1\), and \(\Lambda(W)+1=1\).  The corrected
   induction below retains the slack
   \(y=\Lambda(T)-\deg W\ge1\).  Its final coarse charge is the same
   global-degree charge needed for RF3''.

The same slack also affects the printed derivative-numerator estimate, not
only its base case.  Over \(\mathbb F_5\), take

\[
 R=X+(Y+Z^2)(Y+1)(Y+2),\qquad x_0=0,\qquad H=Y+Z^2.
\]

Here \(R\) is irreducible (it is monic linear in \(X\)), \(a=3\), \(g=4\),
\(b=1\), and \(W=1\).  At the root \(\alpha_0=-Z^2\),
\(\partial_YR=(1-Z^2)(2-Z^2)\) has degree four, while the printed bound
\((g-1)+(a-2)\deg W\) is only three.  Thus the whole weight induction, not
just the line for \(\beta_0\), must be replaced.  Equations (13)--(21) do so.

## Primary-source boundary

The provenance is:

- E. Ben-Sasson, D. Carmon, Y. Ishai, S. Kopparty, and S. Saraf,
  *Proximity Gaps for Reed--Solomon Codes*, ECCC TR20-083, revision 3,
  Sections 5.2.3--5.2.8 and Appendix A.  Pinned PDF SHA-256:
  `84264f52e16dc40108321c8d5b33ac3a03392fc0a9326fd49a229f7e30b804b1`.
- E. Ben-Sasson, D. Carmon, U. Haböck, S. Kopparty, and S. Saraf,
  *On Proximity Gaps for Reed--Solomon Codes*, ECCC TR25-169, Section 3.2.
  Pinned PDF SHA-256:
  `f1be50e43e26809f868c7d042104063a4f7353a7923f68b98ba8a6912e500206`.

BCIKS Lemma A.1, the resultant zero-count lemma, is used as printed.  The
Claim A.2 coefficient induction is reproduced and corrected below.  BCHKS
Section 3.2 supplies the factor-pair summation architecture and its footnote 5
supplies the content warning, but its replacement of a global factor degree by
the content-free degree after specialization is not used.

## Integer core theorem

Let \(\mathbb F=\mathbb F_q\), let \(D\subseteq\mathbb F\) have size \(n\),
and let \(K,U,A,r\in\mathbb Z_{\ge0}\) satisfy
\(K,U\ge1\), \(r\ge0\), and \(A=n-r\ge K+2\).  Fix received words
\(u_0,u_1:D\to\mathbb F\).

Let \(0\ne Q\in\mathbb F[X,Y,Z]\), and write its actual integral degrees as

\[
 E=\operatorname{wdeg}_{1,K,0}Q,\qquad
 d=\deg_YQ,\qquad
 G=\operatorname{wdeg}_{0,1,1}Q.
\]

Assume

\[
 E\le U-1,\qquad \operatorname{char}(\mathbb F)>d,
 \qquad q>2Ud,                                      \tag{I1}
\]

and the exact top-incidence comparison

\[
 (A-K)(2U-1)>(n-K)(2K-1).                         \tag{I2}
\]

For each distinct \(\gamma\) in a set \(S\subseteq\mathbb F\), suppose
there is a polynomial \(P_\gamma\in\mathbb F[X]\),
\(\deg P_\gamma<K\), such that

\[
 Q(X,P_\gamma(X),\gamma)=0,
\]

and a chosen set \(A_\gamma\subseteq D\), \(|A_\gamma|=A\), on which

\[
 P_\gamma=u_0+\gamma u_1.
\]

Then

\[
 |S|>(1+2Ud^2)G+(r+1)d                           \tag{I3}
\]

implies that for some \(\gamma_0\in S\) there are
\(v_0,v_1\in\mathbb F[X]\), \(\deg v_i<K\), satisfying

\[
 u_i=v_i\quad\hbox{on the chosen set }A_{\gamma_0},\qquad i=0,1. \tag{I4}
\]

The rest of the note proves this theorem.

## 1. Factorization and a genuinely regular common point

If \(d=0\), then \(Q\in\mathbb F[X,Z]\).  A slope for which
\(Q(X,\gamma)=0\) identically in \(X\) is a root of any fixed nonzero
\(X\)-coefficient of \(Q\), so there are at most \(\deg_ZQ\le G\) such
slopes.  This contradicts (I3).  Hence assume \(d\ge1\).

Factor in \(\mathbb F[X,Z][Y]\):

\[
 Q=C(X,Z)\prod_i R_i(X,Y,Z)^{e_i},                \tag{1}
\]

where \(C\ne0\) is the \(Y\)-content, the \(R_i\) are distinct primitive
irreducibles of positive \(Y\)-degree, and \(e_i\ge1\).  Put

\[
 a_i=\deg_YR_i,\quad
 \Delta_i=\operatorname{wdeg}_{1,K,0}R_i,\quad
 g_i=\operatorname{wdeg}_{0,1,1}R_i,
\]

and \(\Delta_C=\deg_XC\).  Weighted-degree additivity over the integral
coefficient rings gives

\[
 d=\sum_i e_i a_i,\qquad
 E=\Delta_C+\sum_i e_i\Delta_i,\qquad
 G=\deg_ZC+\sum_i e_i g_i.                       \tag{2}
\]

The characteristic guard makes every \(R_i\) separable in \(Y\): an
irreducible with zero \(Y\)-derivative has positive \(Y\)-degree at least
\(\operatorname{char}(\mathbb F)>d\), whereas \(a_i\le d\).

Write \(R_i=\sum_{j=0}^{a_i}r_{ij}(X,Z)Y^j\).  Every monomial in its
discriminant is homogeneous of coefficient degree \(2a_i-2\) and isobaric
of \(Y\)-index \(a_i(a_i-1)\).  Since
\(\deg_Xr_{ij}\le\Delta_i-Kj\),

\[
 \deg_X\!\left(\operatorname{lc}_Y(R_i)
                  \operatorname{disc}_Y(R_i)\right)
 \le (2a_i-1)\Delta_i-Ka_i^2.                   \tag{3}
\]

Choose a nonzero coefficient \(c_*(X)\) of \(C(X,Z)\) as a polynomial in
\(Z\), and form

\[
 \Omega(X,Z)=c_*(X)\prod_i
   \operatorname{lc}_Y(R_i)\operatorname{disc}_Y(R_i).
\]

It is nonzero.  If \(a_*:=\sum_i a_i\le d\), then a nonzero
\(Z\)-coefficient \(\omega(X)\) of \(\Omega\) has

\[
\begin{aligned}
 \deg\omega
 &\le \Delta_C+\sum_i(2a_i-1)\Delta_i\\
 &\le 2d\left(\Delta_C+\sum_i\Delta_i\right)\\
 &\le 2dE\le2d(U-1)<2Ud<q.                      \tag{4}
\end{aligned}
\]

Thus some \(x_0\in\mathbb F\) satisfies \(\omega(x_0)\ne0\).  At this
single point, \(C(x_0,Z)\ne0\), and for every \(i\), both
\(\operatorname{lc}_Y(R_i)(x_0,Z)\) and
\(\operatorname{disc}_Y(R_i)(x_0,Z)\) are nonzero polynomials.  Therefore
\(R_i(x_0,Y,Z)\) retains \(Y\)-degree \(a_i\) and is separable in \(Y\).
The leading-coefficient factor in \(\Omega\) is indispensable when
\(a_i=1\), because the usual linear discriminant is \(1\).

## 2. Global and specialization contents

Factor each regular specialization in \(\mathbb F[Z][Y]\):

\[
 R_i(x_0,Y,Z)=C_i(Z)\prod_j H_{ij}(Y,Z),          \tag{5}
\]

where every \(H_{ij}\) is primitive, irreducible, separable, and of positive
\(Y\)-degree

\[
 b_{ij}:=\deg_YH_{ij},\qquad \sum_jb_{ij}=a_i.   \tag{6}
\]

Let

\[
 C_{\rm sp}(Z)=C(x_0,Z)\prod_i C_i(Z).
\]

The roots of this polynomial contain every slope lost either to the global
content or to a specialization content.  Indeed,
\(C(X,\gamma)=0\) identically implies \(C(x_0,\gamma)=0\).  The product with
multiplicities
\(C(x_0,Z)\prod_i C_i(Z)^{e_i}\) divides the \(Y\)-content of
\(Q(x_0,Y,Z)\).  By Gauss's lemma, the remaining product of primitive
\(H_{ij}\)'s is primitive.  The \(Z\)-degree of that \(Y\)-content is
therefore at most the global \((Y,Z)\)-degree \(G\).  Consequently

\[
 \#\{\gamma:C_{\rm sp}(\gamma)=0\}
 \le\deg C_{\rm sp}\le G.                       \tag{7}
\]

For any remaining slope, (1) and the identity for \(Q\) show that some
\(R_i(X,P_\gamma(X),\gamma)\) vanishes identically.  Substitution of
\(x_0\), followed by (5) and the nonvanishing of \(C_i(\gamma)\), gives
some \(H_{ij}(P_\gamma(x_0),\gamma)=0\).  Assign the slope to one such pair
\((i,j)\).  These assigned sets are disjoint and cover all noncontent
slopes.

## 3. Corrected nonlinear local lift

Fix one pair and abbreviate

\[
 R=R_i,\quad H=H_{ij},\quad
 a=a_i,\quad b=b_{ij},\quad g=g_i,
 \quad c=abg.                                    \tag{8}
\]

First suppose \(a\ge2\).  Write

\[
 H(Y,Z)=h_0(Z)Y^b+\cdots+h_b(Z),\qquad W=h_0,
 \qquad w=\deg W.
\]

Because the global degree \(g\) bounds both \(R\) and \(H\),

\[
 0\le w\le g-b.
\]

Put

\[
 \ell=g-b+1,\qquad y=\ell-w\ge1.                \tag{9}
\]

As in BCIKS Appendix A, monicize

\[
 \widetilde H(T,Z)=W^{b-1}H(T/W,Z)
\]

and use the ring
\(\mathcal O=\mathbb F[Z,T]/(\widetilde H)\) with
\(\Lambda(Z)=1\) and \(\Lambda(T)=\ell\).  Monicity and irreducibility of
\(\widetilde H\) make \(\mathcal O\) a domain; write
\(L=\operatorname{Frac}(\mathcal O)\).  Every nonleading term of
\(\widetilde H\) has weight at most \(b\ell\): for its index \(s\),

\[
 \deg h_s+(s-1)w+(b-s)\ell
 \le b\ell+(s-1)(1+w-\ell)\le b\ell.            \tag{10}
\]

Hence reduction modulo \(\widetilde H\) does not increase weight, and the
resultant proof of BCIKS Lemma A.1 applies unchanged:

\[
 \text{a nonzero }\beta\in\mathcal O
 \text{ has at most }b\Lambda(\beta)
 \text{ rational slope zeros}.                  \tag{11}
\]

Let \(\alpha_0=T/W\).  It is a simple root of \(R(x_0,Y,Z)\) in the
algebraic function field.  Put

\[
 \zeta=\partial_YR(x_0,\alpha_0,Z),\qquad
 \xi=W^{a-2}\zeta\in\mathcal O.                 \tag{12}
\]

The regular numerator estimate needed below is

\[
 \Lambda(\xi)\le
 \chi:=g-a+(a-1)y+(a-2)w
       =ag-1-(a-1)b-w.                           \tag{13}
\]

In particular \(\chi\ge a-1>0\).

Here is the full coefficient check.  Expand the Hensel equation around
\(h=X-x_0\).  A term indexed by an \(X\)-Hasse derivative of order \(i\)
and a partition \(\lambda=(\lambda_s)_{s\ge1}\) has
\(s_\lambda=\sum_s\lambda_s\).  After evaluating the corresponding
\(Y\)-Hasse derivative at \(T/W\), write its coefficient as

\[
 A_{i,\lambda}=B_{i,\lambda}/W^{a-s_\lambda-\delta_i},
 \qquad \delta_i=\begin{cases}1&i=0,\\0&i>0.\end{cases}              \tag{14}
\]

The saving when \(i=0\) follows because \(W\) divides the
\(Y\)-leading coefficient of \(R(x_0,Y,Z)\).  When \(i=0\) and
\(s_\lambda=a\), the exponent in (14) is \(-1\); the notation then means
\(A_{i,\lambda}=W B_{i,\lambda}\), which is legitimate by that same
divisibility.

For completeness, consider a nonzero term of post-Hasse \(Y\)-degree
\(j\le a-s_\lambda\).  After the common \(W\)-denominator in (14) is
cleared, its weight is at most

\[
 g-s_\lambda-j+j\ell+
   (a-s_\lambda-\delta_i-j)w.
\]

The coefficient of \(j\) is
\(\ell-w-1=y-1\ge0\), so the maximum occurs at
\(j=a-s_\lambda\).  In the \(i=0\) top term,
\(\operatorname{lc}_Y(R(x_0))/W\) is polynomial and gives the same saved
\(w\).  Therefore

\[
 \Lambda(B_{i,\lambda})
 \le g-a+(a-s_\lambda)y+(a-s_\lambda-\delta_i)w. \tag{15}
\]

Taking \(i=0\), \(s_\lambda=1\) in (15) proves (13).

Let

\[
 e_0=0,\qquad e_t=2t-1\quad(t\ge1),
\]

and define

\[
 L_t=y+(t+1)w+e_t\chi.                           \tag{16}
\]

The unique Hensel lift

\[
 \Gamma=\sum_{t\ge0}\alpha_th^t,qquad R(X,\Gamma,Z)=0,
\]

satisfies

\[
 \alpha_t=\frac{\beta_t}{W^{t+1}\xi^{e_t}},
 \qquad \beta_t\in\mathcal O,qquad
 \Lambda(\beta_t)\le L_t.                       \tag{17}
\]

For \(t=0\), take \(\beta_0=T\); then
\(\Lambda(\beta_0)\le\Lambda(T)=\ell=y+w=L_0\).  This is the corrected base case.
For \(t\ge1\), the coefficient equation for \(h^t\) is linear in
\(\alpha_t\) with coefficient \(\zeta\).  Excluding that one term, an index
\((i,\lambda)\) satisfies

\[
 i+\sum_s s\lambda_s=t.
\]

After inserting (14) and the inductive forms (17), and clearing to the
denominator in (17), its contribution to \(\beta_t\) is

\[
 W^{i+\delta_i-1}\xi^{2i+s_\lambda-2}
 B_{i,\lambda}\prod_s\beta_s^{\lambda_s}.        \tag{18}
\]

Both displayed exponents are nonnegative.  For \(i=0\), the omitted linear
term is the only case with \(s_\lambda=1\); every remaining term has
\(s_\lambda\ge2\).  For \(i=t>0\), the partition may be empty; then the
\(\xi\)-exponent is \(2t-2\ge0\).  Using (15) and the inductive bounds, the
weight of (18) is at most

\[
 g-a+ay+(a+t-1)w+(2t-2)\chi
 =y+(t+1)w+(2t-1)\chi=L_t,                       \tag{19}
\]

where the equality is precisely the definition (13) of \(\chi\).  This
closes the induction without assuming \(\Lambda(T)=\Lambda(W)+1\).

The coarse bounds needed for slope counting are still the familiar ones:

\[
 L_t<(2t+1)ag.                                    \tag{20}
\]

For \(t=0\), \(L_0=\ell\le g<ag\).  For \(t\ge1\), substitution of (9) and
(13) gives the strictly positive difference

\[
 (2t+1)ag-L_t
 =2ag-g+b-1+(t-1)w+(2t-1)(1+(a-1)b)>0.           \tag{21}
\]

The denominator deletion is also within one pair charge.  Roots of \(W\)
cost at most \(w\); (11) and (13) bound the slope zeros of the nonzero
\(\xi\) by \(b\chi\).  Finally,

\[
 abg-(w+b\chi)=b+b^2(a-1)+(b-1)w>0.              \tag{22}
\]

Thus fewer than \(c=abg\) assigned slopes are deleted.

For a surviving assigned slope \(\gamma\), put
\(t_\gamma=W(\gamma)P_\gamma(x_0)\).  Then
\[
 \widetilde H(t_\gamma,\gamma)
 =W(\gamma)^{b-1}H(P_\gamma(x_0),\gamma)=0,
\]
so the substitution \(\pi_\gamma:\mathcal O\to\mathbb F\) exists.  Since
\(W(\gamma)\ne0\) and \(\pi_\gamma(\xi)\ne0\),
\(\pi_\gamma(\zeta)=W(\gamma)^{2-a}\pi_\gamma(\xi)\ne0\).  Thus
\(\pi_\gamma(\Gamma)\) and \(P_\gamma\) solve \(R(X,Y,\gamma)=0\) with the
same simple constant term.  Hensel uniqueness identifies them.  Hence for
\(K\le t\le U-1\),
\(\beta_t\) vanishes at every surviving slope.  If the pair began with more
than

\[
 2Uc+(r+1)                                           \tag{23}
\]

assigned slopes, then after (22) more than
\((2U-1)c+(r+1)\) survive.  Equations (11) and (20) force
\(\beta_t=0\), hence \(\alpha_t=0\), for every such \(t\).

The truncated series
\(\Gamma_{<K}=\sum_{t<K}\alpha_th^t\) agrees with \(\Gamma\) modulo
\(h^U\).  Substituting it into \(R\) gives an \(X\)-polynomial of degree at
most \(U-1\), because \(R\) has \((1,K)\)-weighted degree at most \(U-1\).
It vanishes modulo \(h^U\), hence identically.  Hensel uniqueness then gives

\[
 \Gamma=\Gamma_{<K}\in L[X],\qquad \deg_X\Gamma<K. \tag{24}
\]

For a coordinate \(x\), put the expression in (24) over the common
denominator \(W^K\xi^{e_{K-1}}\).  Its comparison numerator is

\[
\begin{aligned}
 N_x={}&\sum_{t=0}^{K-1}
   \beta_t(x-x_0)^tW^{K-t-1}\xi^{e_{K-1}-e_t}\\
 &-(u_0(x)+Zu_1(x))W^K\xi^{e_{K-1}}.
\end{aligned}
\]

All exponents are nonnegative, including when \(K=1\).  Each summand in the
sum has weight at most
\(y+Kw+e_{K-1}\chi\); the affine term has weight at most
\(1+Kw+e_{K-1}\chi\), which is no larger because \(y\ge1\).  Therefore

\[
 \Lambda(N_x)\le y+Kw+e_{K-1}\chi
 =L_{K-1}<(2K-1)ag.                              \tag{25}
\]

By (11), more than \((2K-1)abg=(2K-1)c\) incident surviving slopes force
this numerator to be zero, and therefore

\[
 \Gamma(x)=u_0(x)+Zu_1(x).                       \tag{26}
\]

## 4. Direct linear-factor lift

Now suppose \(a=1\).  Then \(b=1\), \(c=g\), and write

\[
 R(X,Y,Z)=A(X,Z)Y+B(X,Z).
\]

The leading-coefficient guard gives \(A_0(Z):=A(x_0,Z)\ne0\).  Expand at
\(h=X-x_0\):

\[
 A=\sum_{s\ge0}A_s(Z)h^s,qquad
 B=\sum_{s\ge0}B_s(Z)h^s.
\]

Global total degree \(g\) gives

\[
 \deg A_s\le g-1,qquad \deg B_s\le g.           \tag{27}
\]

The unique root is

\[
 \Gamma=-B/A=\sum_{t\ge0}\alpha_th^t,qquad
 \alpha_t=N_t/A_0^{t+1},                         \tag{28}
\]

where

\[
\begin{aligned}
 N_0&=-B_0,\\
 N_t&=-B_tA_0^t-
       \sum_{s=1}^t A_sN_{t-s}A_0^{s-1}.          \tag{29}
\end{aligned}
\]

Induction using (27) gives the exact numerator bound

\[
 \deg N_t\le(t+1)g-t.                            \tag{30}
\]

Indeed, the first term of (29) has that degree, and every summand has degree
at most

\[
 (g-1)+((t-s+1)g-(t-s))+(s-1)(g-1)
 =(t+1)g-t.
\]

Delete the roots of \(A_0\); there are at most \(g-1<c\).  On every
surviving assigned slope, (28) specializes to the polynomial
\(P_\gamma\).  Thus \(N_t(\gamma)=0\) for \(t\ge K\).  Under (23), the
survivor count is greater than \((2U-1)g+(r+1)\), so (30) forces
\(N_t=0\) for \(K\le t\le U-1\).  The same weighted-degree truncation
argument as in (24) gives \(\Gamma\in\mathbb F(Z)[X]\) with
\(\deg_X\Gamma<K\).

For any coordinate \(x\), put the truncated expression over the fixed
denominator \(A_0^K\):

\[
 \Gamma(x)=\frac{M_x(Z)}{A_0(Z)^K},\qquad
 M_x=\sum_{t=0}^{K-1}N_t(x-x_0)^tA_0^{K-t-1}.
\]

Equation (30) gives

\[
 \deg M_x\le Kg-K+1.
\]

The numerator after subtracting \(u_0(x)+Zu_1(x)\) obeys the same bound,
and

\[
 Kg-K+1\le(2K-1)g.                               \tag{31}
\]

More than \((2K-1)g\) incident surviving slopes therefore force the
rational-function identity (26).  The use of the fixed denominator
\(A_0^K\), rather than \(A(x,Z)\), also covers coordinates at which the
specialized leading coefficient \(A(x,Z)\) vanishes identically.

## 5. Top incidence, interpolation, and the chosen support

Both local branches have the following common output.  If a pair with charge
\(c=abg\) begins with more than (23) assigned slopes, a set \(T\) of more
than

\[
 (2U-1)c+(r+1)                                   \tag{32}
\]

slopes survives, and \(P_\gamma\) is the specialization of a single
\(\Gamma\in L[X]\), \(\deg_X\Gamma<K\), for every \(\gamma\in T\).

For \(x\in D\), let

\[
 T_x=\{\gamma\in T:x\in A_\gamma\}.
\]

Choose the \(K\) coordinates with largest \(|T_x|\).  If \(t_K\) is the
smallest of those \(K\) incidences, double counting the at least
\(A|T|\) chosen-support incidences gives

\[
 A|T|\le K|T|+(n-K)t_K,
 \qquad
 t_K\ge\frac{A-K}{n-K}|T|.                       \tag{33}
\]

By (I2), (32), and \(c>0\), every selected coordinate satisfies

\[
 |T_x|>(2K-1)c.                                  \tag{34}
\]

Equation (26), proved by the corrected nonlinear numerator or by (31), holds
at all \(K\) selected coordinates.  Interpolate \(u_0,u_1\) on those
coordinates to polynomials \(v_0,v_1\) of degree less than \(K\).  The two
degree-\(<K\) polynomials in \(L[X]\), \(\Gamma\) and \(v_0+Zv_1\), agree
at \(K\) points, so

\[
 \Gamma=v_0+Zv_1.                                \tag{35}
\]

In particular, \(P_\gamma=v_0+\gamma v_1\) for every \(\gamma\in T\).

It remains to retain a *chosen* support.  Let

\[
 B=\{x\in D:(u_0(x),u_1(x))\ne(v_0(x),v_1(x))\}.
\]

At a fixed point of \(B\), the two affine combinations can agree for at
most one slope.  Each slope has at most \(r=n-A\) disagreements, hence

\[
 |B|(|T|-1)\le r|T|.                             \tag{36}
\]

Since (32) gives \(|T|>r+1\), integrality gives \(|B|\le r\).  If every
chosen \(A_\gamma\) met \(B\), choose a point in each intersection.  Such a
point is an agreement point for that slope and can serve at most one distinct
slope, giving an injection \(T\hookrightarrow B\).  This would imply
\(|T|\le|B|\le r\), a contradiction.  Therefore some chosen
\(A_{\gamma_0}\) is disjoint from \(B\), which is exactly (I4).

## 6. Global pair sum

Suppose no assigned pair has more than its local bound (23).  From (6), (2),
and \(e_i\ge1\),

\[
\begin{aligned}
 \sum_{i,j}a_i b_{ij}g_i
 &=\sum_i a_i^2g_i\\
 &\le d^2\sum_i g_i\\
 &\le d^2G,                                      \tag{37}\\
 \#\{(i,j)\}&\le\sum_{i,j}b_{ij}
              =\sum_i a_i\le d.                 \tag{38}
\end{aligned}
\]

Adding the at most \(G\) content slopes from (7) gives

\[
\begin{aligned}
 |S|
 &\le G+\sum_{i,j}\bigl(2Ua_ib_{ij}g_i+(r+1)\bigr)\\
 &\le(1+2Ud^2)G+(r+1)d,
\end{aligned}
\]

contradicting (I3).  Thus a locally large pair exists, and Sections 3--5
prove the integer core theorem.

## 7. RF3'' corollary for the v9.2 parameter map

For the v9.2 notation, actual integral degrees satisfy

\[
 E\le U-1,\qquad d<D_Y,\qquad G<D_Z.
\]

The RF1 characteristic clause gives
\(\operatorname{char}(\mathbb F)>V-1\ge d\), and RF2 gives
\(q>2UD_Y>2Ud\).

The printed top comparison is stronger than (I2).  Put
\(p=A-K-1\) and \(s=n-K-1\).  Since \(0<p\le s\),

\[
 \frac{A-K}{n-K}=\frac{p+1}{s+1}\ge\frac ps.
\]

Thus

\[
 p(2U-1)>s(2K+1)
\]

implies

\[
 (A-K)(2U-1)>(n-K)(2K-1).
\]

Finally,

\[
 (1+2Ud^2)G+(r+1)d
 <(1+2UD_Y^2)D_Z+(r+1)D_Y.                       \tag{39}
\]

Therefore RF3'' implies the integer hypothesis (I3), and the bridge proves
the retained-factor conclusion with the chosen support.  The interpolation
conditions \(V\ge m\), \(W\ge V\), \(U>K(V-1)\), and \(D_X<mA\) remain
relevant to the preceding construction of \(Q\) and the root identities;
once those identities are hypotheses of the bridge, they are not used again.

## Verification and scope

Run from the repository root:

```bash
python3 experimental/scripts/verify_paving_v9_2_rf3_global_degree_bridge.py --check
python3 experimental/scripts/verify_paving_v9_2_rf3_global_degree_bridge.py --tamper-selftest
cd experimental/lean/paving_retained_factor_lift && lake build
```

The standard-library verifier checks the source bindings, both corrected
local degree recurrences, content and leading-coefficient ledgers, small
exhaustive factor partitions, incidence inequalities, the RF3'' aggregation,
and the four already-pinned row ceilings.  The Lean companion certifies the
elementary arithmetic kernels and records the full algebraic theorem as a
typed, explicitly unformalized target; no axiom or placeholder proof is
introduced.

This is a paper proof of the global-degree bridge.  It is not a formalization
of finite-field factorization, algebraic function fields, Hensel lifting, or
BCIKS Lemma A.1.  It does not recover RF3', alter the immutable v9.2 files, or
by itself relabel the v9.2 rows: a future release must state RF3'' and use the
new exact ceilings.
