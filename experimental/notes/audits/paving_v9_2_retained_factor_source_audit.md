# Paving v9.2 retained-factor source audit

Status: AUDIT

## Scope and bottom line

Claude proposed the line-by-line retained-factor source verification.

This note audits **ass:retained-factor-lift** in
**experimental/RS_MCA_Paving_v9.2.tex** against every load-bearing primary
source step: BCIKS Claims 5.6--5.11, Lemma A.1, Claim A.2, BCHKS Section
3.2, and BCHKS Section 4.2/Theorem 4.3.

The original v9.2 assumption is **not discharged**, because its RF3 antecedent
is too weak.  The standalone conservative RF3'' bridge isolated by this audit
is now proved in
**experimental/notes/audits/paving_v9_2_rf3_global_degree_bridge.md**.

There are two independent obstructions.

1. Universal RF3 omits the coefficient guard needed to absorb scalar-content
   roots.  The existing exact counterexample in
   **experimental/notes/audits/paving_v8_retained_factor_content_guard.md**
   applies unchanged to v9.2.  Its RF3' repair is necessary:
   \[
     |S|>\max(1,2UD_Y^2)D_Z+(r+1)D_Y.             \tag{RF3'}
   \]
2. RF3' is not sufficient to validate the cited proof.  BCHKS Section 3.2
   replaces the global $Y,Z$ degree of $R_i(X,Y,Z)$ by the content-free
   degree of $R_i(x_0,Y,Z)$ and says that the Hensel weights are unaffected.
   The exact witness
   \[
     R(X,Y,Z)=Z^2Y+X(Z^3+1),\qquad x_0=0          \tag{W}
   \]
   disproves that reduction.  Here $R(0,Y,Z)=Z^2Y$, so the content-free
   factor is $H=Y$ of degree one, but the unique Hensel root is
   \[
     \gamma(X)=-X\frac{Z^3+1}{Z^2},
     \qquad
     \alpha_1=-\frac{Z^3+1}{Z^2},
   \]
   whose numerator has degree three.

If the original **global** $Y,Z$ degrees of the factors are retained, the
the corrected BCIKS-style local bounds give the conservative universal envelope
\[
  |S|>(1+2UD_Y^2)D_Z+(r+1)D_Y.                   \tag{RF3''}
\]
RF3'' leaves all four printed KoalaBear rows below the 128-bit budget.
Future-version promotion can therefore use:

- the now-proved standalone global-degree factor lift using RF3''; or
- a new valid sharper local lemma that controls the $X$-dependent
  coefficients missed by the BCHKS content-free specialization and recovers
  RF3'.

Neither source prints the v9.2 arbitrary-parameter synthesis as a theorem.

## Primary sources

- E. Ben-Sasson, D. Carmon, Y. Ishai, S. Kopparty, and S. Saraf,
  *Proximity Gaps for Reed--Solomon Codes*, ECCC TR20-083, revision 3,
  July 3, 2021; IACR ePrint 2020/654.  Pinned PDF SHA-256:
  `84264f52e16dc40108321c8d5b33ac3a03392fc0a9326fd49a229f7e30b804b1`.
  The claim numbering below is the extended revision-3 numbering.
- E. Ben-Sasson, D. Carmon, U. Haböck, S. Kopparty, and S. Saraf,
  *On Proximity Gaps for Reed--Solomon Codes*, ECCC TR25-169; IACR ePrint
  2025/2055.  Pinned PDF SHA-256:
  `f1be50e43e26809f868c7d042104063a4f7353a7923f68b98ba8a6912e500206`.

The audited locations are BCIKS Sections 5.2.3--5.2.8 and Appendix A, and
BCHKS Sections 3.2 and 4.2.

## Notation and integer crosswalk

| Role | Paving v9.2 | BCIKS/BCHKS | Translation |
|---|---:|---:|---|
| Code dimension | $K$ | $k+1$ | $k=K-1$ |
| Code-polynomial degree | $<K$ | $\le k$ | identical |
| Domain size | $n$ | $n$ | identical |
| Chosen agreement | $A$ | $n-e$ | $e=r=n-A$ |
| Multiplicity | $m$ | $m$ | identical |
| Weighted $X,Y$ cap | $D_X$ | $D_X$ | v9.2 uses stronger weight $i+Kj$ |
| $Y$-degree cap | $D_Y$ | actual integral $D_Y$ | use $d=\deg_YQ<D_Y$ |
| $Y,Z$ total-degree cap | $D_Z$ | $D_{YZ}$ or $D_Z$ | v9.2's $(0,1,1)$ weight |
| Ceiling variables | $U,V,W$ | usually suppressed | $\lceil D_X\rceil,\lceil D_Y\rceil,\lceil D_Z\rceil$ |
| Slope | $\gamma$ | $z$ | identical role |
| Explainer | $P_\gamma$ | $P_z$ | $\deg P_\gamma<K$ means $\deg P_z\le k$ |

The exact integral consequences are
\[
\begin{aligned}
 \operatorname{wdeg}_{1,K}Q<D_X
  &\Longrightarrow \operatorname{wdeg}_{1,K}Q\le U-1,\\
 \deg_YQ<D_Y&\Longrightarrow \deg_YQ\le V-1,\\
 \operatorname{wdeg}_{Y,Z}Q<D_Z
  &\Longrightarrow \operatorname{wdeg}_{Y,Z}Q\le W-1.
\end{aligned}
\]

The first line, not the real value $D_X$, controls the final Hensel index.

## RF1 and RF2, clause by clause

### $V\ge m$, $W\ge V$, and $U>K(V-1)$

These are interpolation-box conditions, not hypotheses of a numbered local
BCIKS factor theorem.  They make the RF4 monomial counts
$U-Kj$ and $W-j$ positive for $0\le j<V$.

For the factor argument, $U>K(V-1)$ also gives $U>K$ whenever a
positive-$Y$ factor exists.  If $\deg_YQ=0$, no Hensel pair exists and all
possible slope roots are content roots.

### $D_X<mA$

BCIKS Section 5.2.2 uses the same root count.  Multiplicity $m$ on a chosen
$A$-set gives at least $mA$ roots of
$Q(X,P_\gamma(X),\gamma)$, whose degree is $<D_X$; hence it vanishes
identically.

Inside **ass:retained-factor-lift** that identity is already an antecedent,
so $D_X<mA$ is logically redundant there.  It is needed in the preceding
interpolation-to-root step of **thm:retained-degree-mca**.

### $\operatorname{char}(\mathbb F)>V-1$

Put $d=\deg_YQ$.  Since $d<D_Y$, $d\le V-1$.  An irreducible factor
inseparable in $Y$ has $Y$-degree at least the characteristic.  Therefore
$\operatorname{char}(\mathbb F)>V-1$ excludes the inseparable branch.

This is a valid strengthening of the discussion after BCIKS Claim 5.6.
BCIKS Appendix C is not needed under this guard.  BCHKS Section 3.2 also
works first in the separable case and points to that appendix otherwise.

### $q>2UD_Y$ and the common regular point

BCIKS Claim 5.6 chooses $x_0\in\mathbb F_q$ at which all relevant
irreducible factors remain separable in $Y$.  For the arbitrary-parameter
version, the regularity polynomial must include the $Y$-leading
coefficients as well as the discriminants.  This is necessary for linear
factors, whose usual discriminant is $1$ even if their $Y$-degree drops
after specialization.

If $R_i$ has $Y$-degree $a_i$ and $(1,K)$ weighted degree $\Delta_i$,
the product of its leading coefficient and discriminant has $X$-degree
strictly less than
\[
 (2a_i-1)\Delta_i-Ka_i^2<2a_i\Delta_i.
\]
After squarefree normalization,
$\sum_i\Delta_i<D_X$ and $\sum_i a_i\le d<D_Y$.  The common
leading-coefficient--discriminant product therefore has degree
$<2D_Xd<2UD_Y<q$.  It is nonzero, so a common regular $x_0$ exists.

Thus the field-size clause is adequate, but the v9.2 prose should name the
leading coefficients explicitly.

### Integer top-degree comparison

V9.2 assumes
\[
 (A-K-1)(2U-1)>(n-K-1)(2K+1).                    \tag{T-v9}
\]

The source degree bound is $k=K-1$.  Suppose a local pair charge is
$c$ and the post-deletion slope set satisfies $|T|>(2U-1)c$.
Choosing the $K$ coordinates with largest slope incidence, the exact
Claim 5.11 double count gives
\[
 |T_x|\ge\frac{A-K}{n-K}|T|.
\]
Claim 5.10 requires only $|T_x|>(2K-1)c$.  Hence the natural sufficient
condition is
\[
 (A-K)(2U-1)>(n-K)(2K-1).                         \tag{T-exact}
\]
Because $A\le n$,
\[
 \frac{A-K}{n-K}\ge\frac{A-K-1}{n-K-1},
\]
and $2K+1>2K-1$, so (T-v9) safely implies (T-exact).  The v9.2 condition
is conservative, not the literal source translation.

### Real $D_X$ and the truncation $2U-1$

BCIKS Claim 5.8 writes $2D_X-1$.  For nonintegral $D_X$, the inference
\[
 t<D_X\Longrightarrow2t+1\le2D_X-1
\]
is false.  Since $t$ is integral, the correct statement is
\[
 t<D_X\Longrightarrow t\le U-1
 \Longrightarrow2t+1\le2U-1.
\]
V9.2's use of $2U-1$ is therefore the correct rounding repair.

## BCIKS Claims 5.6--5.11

### Claim 5.6

Role: choose one regular $x_0$ for all irreducible factors.

Mapping: valid under $q>2UD_Y$ after the regularity product is enlarged to
include $Y$-leading coefficients.  The v9.2 proof-tier remark should cite
Claim 5.6 explicitly.

### Claim 5.7

Role: specialize
\[
 R_i(x_0,Y,Z)=C_i(Z)\prod_jH_{ij}(Y,Z)
\]
and pigeonhole slopes into factor pairs $(R_i,H_{ij})$.

BCIKS Claim 5.7 overlooks slopes at which the global $Y$-content or some
$C_i(Z)$ vanishes.  BCHKS Section 3.2, footnote 5, explicitly records this
omission and pays those slopes separately.  Any v9.2 proof must use the
corrected BCHKS partition, not Claim 5.7 literally.

### Claim 5.8

Role: prove that the Hensel series
$\gamma=\sum_{t\ge0}\alpha_t(X-x_0)^t$ has $X$-degree at most the
code-polynomial degree.

For $k=K-1$, Lemma A.1 and Claim A.2 kill the coefficients
$\alpha_t$ for $K\le t\le U-1$ once more than the corresponding
$(2U-1)$ pair charge survives.  Substitution of the truncated
degree-$<K$ series into a factor of the $(1,K)$-weighted interpolant has
$X$-degree at most $U-1$ and vanishes modulo $(X-x_0)^U$, hence
vanishes identically.  Hensel uniqueness kills all later coefficients.

The v9.2 proof-tier remark should cite Claim 5.8 explicitly.

### Claim 5.9

Role: interpolate $\gamma(x)$ at $k+1$ suitable domain points after Claims
5.10 and 5.11 show
$\gamma(x)=u_0(x)+Zu_1(x)$.  This gives
$\gamma=v_0+Zv_1$ with $\deg v_i\le k$.

Mapping: $k=K-1$, so exactly $K$ domain points are needed and the output
degree is $<K$.

### Claim 5.10

Role: after clearing the Claim A.2 denominators, more than
$(2k+1)d_HdD$ rational substitutions force a regular numerator to vanish
by Lemma A.1.

For a factor pair, the mapping is
\[
 d=a_i,\qquad d_H=b_{ij},\qquad D=g_i,\qquad
 2k+1=2K-1,
\]
where $g_i$ must be an upper bound on the **global** $Y,Z$ degree of
$R_i$, not merely the content-free degree after specialization.

### Claim 5.11

Role: double count bad coordinate--slope pairs and choose the $k+1$
highest-incidence coordinates.

The source finishes with a specialized Johnson-radius inequality.  V9.2
replaces it by (T-v9), which implies the exact sufficient inequality
(T-exact).  This adaptation is valid but is not a verbatim instance of the
source claim.

The actual dependency is Claims 5.6--5.11.  The v9.2 proof-tier remark's
short list “Claims 5.7, 5.9--5.10” omits Claims 5.6, 5.8, and 5.11.

## Lemma A.1 and Claim A.2

### Lemma A.1

For irreducible $H$ of $Y$-degree $b_{ij}$, BCIKS constructs
\[
 \mathcal O=\mathbb F_q[Z,T]/(\widetilde H)
\]
with a weight $\Lambda$.  Lemma A.1 bounds the number of rational
substitutions at which a nonzero regular element $\beta$ vanishes by
$b_{ij}\Lambda(\beta)$.  The proof is a resultant-degree bound in $T$.

Its use requires:

- $H$ irreducible and nonconstant in $Y$;
- a numerator in $\mathcal O$;
- prior removal of all denominator roots; and
- distinct base-field slopes.

Those conditions hold after the separability, regular-point, and pole
deletions.  Lemma A.1 supplies a local root count, not the global
$D_Y^2D_Z$ sum.

### Corrected global-degree replacement for Claim A.2

Let
\[
 a_i=\deg_YR_i,\qquad b_{ij}=\deg_YH_{ij},
\]
and let $g_i$ bound the global total $Y,Z$ degree of $R_i(X,Y,Z)$.
The intended Claim A.2 form is
\[
 \alpha_t=\frac{\beta_t}{W^{t+1}\xi^{e_t}},
 \qquad e_t=\max(0,2t-1),
\]
with the final coarse target
\[
 \Lambda(\beta_t)<(2t+1)a_i g_i.
\]
However, Claim A.2 cannot be cited verbatim.  Its printed linear case uses
$W^{a_i-2}$ with a negative exponent, its base-case equality
$\Lambda(T)=\Lambda(W)+1$ is false in general, and its derivative-numerator
bound fails for the explicit cubic witness recorded in the bridge note.

The corrected nonlinear induction in that note retains
$y=\Lambda(T)-\deg W\ge1$ and proves the same coarse global-degree target.
Together with Lemma A.1 it yields the local charge
\[
 (2t+1)a_i b_{ij}g_i
 \le(2U-1)a_i b_{ij}g_i.
\]
The denominator-root deletion costs at most
$a_i b_{ij}g_i$.  Thus more than
$2U a_i b_{ij}g_i$ starting slopes leave more than the required
$(2U-1)$ charge.

For $a_i=1$, the bridge note instead solves $A(X,Z)Y+B(X,Z)=0$ directly,
proves
$\deg N_t\le(t+1)g_i-t$, and clears all coordinate comparisons over the
fixed denominator $A(x_0,Z)^K$.  This handles even coordinates where
$A(x,Z)$ vanishes identically.

## Exact obstruction to the BCHKS content-free replacement

Work over any field and take witness (W).  It has the following properties:

- $R$ is primitive and linear in $Y$, hence irreducible in
  $\mathbb F[X,Y,Z]$;
- $R$ and $R(0,Y,Z)$ are separable in $Y$ over $\mathbb F(X,Z)$ and
  $\mathbb F(Z)$;
- $R(0,Y,Z)=Z^2Y=C_i(Z)H(Y,Z)$ with
  $C_i=Z^2$, $H=Y$, and content-free $Y,Z$ degree $1$;
- the global $Y,Z$ degree of $R$ is $3$; and
- the root $0$ of $H$ lifts uniquely to
  $-X(Z^3+1)/Z^2$.

Using content-free degree $D=1$, Claim A.2 would need, already at $t=1$,
\[
 \Lambda(\beta_1)<(2t+1)dD=3.
\]
In the natural denominator form,
$\beta_1=-(Z^3+1)$ has degree $3$, so the strict inequality fails.
Equivalently, the derivative denominator contains the discarded
$C_i=Z^2$.

Using the global degree $D=3$ instead gives the corrected recurrence enough
coarse allowance to charge this numerator below $9$.  The witness therefore
does not refute the corrected global-degree Hensel method; it refutes exactly
the BCHKS sentence that
specialization content can be removed without affecting the Hensel weights.

The reason is structural.  Dividing $R(0,Y,Z)$ by $C_i(Z)$ says nothing
about $X$-dependent coefficients such as $X(Z^3+1)$.  Dividing the whole
equation by $C_i$ over $\mathbb F(Z)$ turns those coefficients into rational
functions with poles at the content roots and does not reduce their
numerator degrees to the content-free specialization degree.

This blocks the v9.2 source discharge even after RF3'.

## BCHKS Section 3.2 and the conservative global sum

BCHKS equation (13) states, for its own parameter family,
\[
 |S|>2D_XD_Y^2D_Z+(\gamma n+1)D_Y.
\]
Its proof summary has the right overall architecture:

1. separable irreducible factorization;
2. one regular $x_0$;
3. scalar-content exclusions;
4. one local Hensel charge per pair $(R_i,H_{ij})$;
5. a sum over pairs; and
6. one collinearity allowance per pair.

The unsupported step is the replacement of the global factor degree by the
content-free degree of the specialization.

Retain instead
\[
 g_i=\operatorname{wdeg}_{Y,Z}R_i(X,Y,Z).
\]
If $d=\deg_YQ$ and
$\Delta=\operatorname{wdeg}_{Y,Z}Q$, squarefree factorization gives
\[
 \sum_j b_{ij}=a_i,\qquad
 \sum_i a_i\le d<D_Y,\qquad
 \sum_i g_i\le\Delta<D_Z.
\]
Therefore the global factor-pair charge satisfies
\[
\begin{aligned}
 \sum_{i,j}a_i b_{ij}g_i
  &=\sum_i a_i^2g_i\\
  &\le d^2\sum_i g_i\\
  &<D_Y^2D_Z.
\end{aligned}
\]

The number of factor pairs is at most
$\sum_i a_i<D_Y$, so the chosen-support allowance sums to less than
$(r+1)D_Y$.

Let $d_C$ count all slopes lost to the global $Y$-content and to the
specialization contents $C_i(Z)$.  Their degrees are bounded by the global
$Y,Z$ degree ledger, hence
\[
 d_C< D_Z.
\]
If no pair gives the desired chosen-support conclusion, summing the local
global-degree bounds gives
\[
\begin{aligned}
 |S|
 &\le d_C+
      2U\sum_{i,j}a_i b_{ij}g_i+
      (r+1)\#\{(i,j)\}\\
 &<(1+2UD_Y^2)D_Z+(r+1)D_Y.
\end{aligned}
\]
The standalone bridge note proves precisely the corrected global-degree local
claim, including the nonlinear recurrence, direct linear branch, all content
charges, and leading-coefficient guard.  Thus this conservative RF3'' envelope
is now discharged; it does not use the false content-free replacement.

The extra $D_Z$ is genuine in this conservative ledger: specialization
content is paid separately while its degree may also be needed inside the
global Hensel weight.

## Exact RF3'' replay for the four v9.2 rows

For the printed rows,
\[
 D_Y=V-1+2^{-64},\qquad D_Z=W-1+2^{-64}.
\]
Adding $D_Z$ to the old real threshold gives these exact ceilings:

| Rate | RF3 ceiling in v9.2 | RF3'' ceiling | Increase | Budget minus RF3'' |
|---:|---:|---:|---:|---:|
| $1/2$ | 274589064742726105 | 274589064742753629 | 27524 | 391663368641458 |
| $1/4$ | 274721012201264929 | 274721012201293956 | 29027 | 259715910101131 |
| $1/8$ | 274578888391530706 | 274578888391562205 | 31499 | 401839719832882 |
| $1/16$ | 274861787390229386 | 274861787390263486 | 34100 | 118940721131601 |

The common 128-bit numerator budget is
\[
 274980728111395087.
\]
Thus every row still clears the budget, with large exact margin.  The
global-degree arbitrary-parameter bridge is now supplied and mechanically
audited.  The immutable v9.2 rows remain conditional until a future release
states RF3'' and uses these ceilings.

## Constrained-support step

BCHKS Section 4.2, Theorem 4.3, states the correct constrained notion: for
any preselected agreement sets $A_z$, sufficiently many proximate curve
points give one selected $A_{z_0}$ on which all coordinate words are
jointly explained.  Its premise is “as large as in Theorem 4.2,” and its
proof is described as an insertion into another cited proof.  It is not the
arbitrary-parameter theorem needed here.

After one local factor produces
\[
 P_\gamma=v_0+\gamma v_1\qquad(\gamma\in T),
\]
the v9.2 chosen-support argument is nevertheless self-contained.
Put
\[
 B=\{x:(u_0(x),u_1(x))\ne(v_0(x),v_1(x))\}.
\]
At a fixed $x\in B$, the two affine combinations agree for at most one
slope.  Each $\gamma\in T$ has at most $r$ disagreements because its
chosen support has size $A=n-r$.  Hence
\[
 |B|(|T|-1)\le r|T|.
\]
If $|T|>r+1$, integrality gives $|B|\le r$.

If no chosen $A_\gamma$ explains both coordinates, every $A_\gamma$ meets
$B$.  At a point of $A_\gamma\cap B$, the affine combinations agree at
slope $\gamma$, and one point of $B$ cannot serve two distinct slopes.
Thus $|T|\le|B|\le r$, contradicting $|T|>r+1$.

This step is valid and preserves the chosen support.  For RF3' the obstruction
still lies earlier, in obtaining $T$ with the claimed content-free degree
charge; RF3'' avoids that replacement.

## Real-to-integer and endpoint ledger

- $t<D_X$ with integral $t$ means $t\le U-1$ and gives $2U-1$.
- $\deg_YQ<D_Y$ means at most $V-1$ actual $Y$ degree and fewer than
  $D_Y$ factor pairs.
- Every scalar-content charge is integral and is bounded by the global
  $Y,Z$ degree.
- The strict pair inequalities remain strict after deleting at most one
  global-degree pole charge.
- If a real exceptional-set bound is $B$, integrality gives at most
  $\lfloor B\rfloor$.  RF5's $\lceil B\rceil$ is conservative by at most
  one.

## Final classification and next proof target

Established:

- the intended source dependency is Claims 5.6--5.11, Lemma A.1, and Claim
  A.2, not the shorter list printed in v9.2, and Claim A.2 needs the corrected
  replacement above;
- the dimension translation is $k=K-1$;
- $2U-1$ is the correct integer truncation;
- the characteristic and common-regular-point guards are adequate after
  leading coefficients are included;
- the top-incidence and chosen-support double counts are valid;
- universal RF3 has the known content-absorption counterexample;
- the BCHKS content-free Hensel-degree reduction has witness (W);
- RF3'' preserves all four printed numerical budget crossings; and
- the standalone corrected global-degree bridge proves RF3'', including the
  nonlinear, linear, content, leading-coefficient, incidence, and
  chosen-support cases.

Not established:

- RF3 or RF3' as a source-supported arbitrary-parameter factor lift;
- a valid content-free local Hensel bound that controls coefficients away
  from $x_0$;
- unconditional promotion of the four retained KoalaBear rows.

The next mathematical target, if the sharper threshold is still wanted, is an
RF3' invariant that measures the $X$-dependent rational coefficients exposed
by witness (W), not only the content-free specialization.  The other natural
next step is a full Lean formalization of the now-proved RF3'' bridge.

The Lean companion formalizes:

- the ceiling and $2U-1$ truncation;
- (T-v9) implies (T-exact);
- the Claim 5.11 incidence count;
- the global factor-pair sum;
- the RF3'' arithmetic; and
- the chosen-support injection.

The Lean companion keeps the algebraic function-field/Hensel statement as an
explicit unasserted target until the corrected paper proof is formalized.
