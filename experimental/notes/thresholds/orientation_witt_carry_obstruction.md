# Orientation locator carries are exact Witt subset sums

- **Status:** PROVED-SPECIAL / EXACT COORDINATE DICTIONARY / ROUTE CUT.
- **Track:** antipodal orientation prefixes in characteristic three.
- **Parent:** PR #644, stacked on PR #634.
- **Verifier:** experimental/scripts/verify_orientation_witt_carry_obstruction.py.
- **Promotion gate:** experimental only. This note does not promote a
  statement to the frontiers TeX.

## Executive verdict

The characteristic-three locator coordinates omitted by ordinary Newton
moments are genuine cuts. A fixed number of carry coordinates cannot alter
a positive critical-scale exponent; a fixed precision across all components
has rate-scale capacity and may alter it, but has the explicit residual
barrier below. An actual collective contraction remains open.

More exactly, orientation prefixes are binary subset sums in a product of
truncated $3$-typical Witt groups. Reduction modulo $3$ is precisely the
ordinary-moment/Frobenius container used by PR #644; the higher Witt digits
are the missing locator carries. This gives three complementary results.

1. The subset-sum model is an exact fiber equivalence, not merely an upper
   container.
2. Any fixed number of $B$-valued carries costs only
   $q^{O(1)}=\exp(o(a))$. More generally, every fixed Witt precision has an
   explicit critical-scale pigeonhole obstruction.
3. The first carry is nevertheless quantitatively real: at fixed depth
   $u=3$, full prefix fibers are asymptotically flat at the $q^2$ target
   scale. Thus $c_3$ pays its full possible factor $q$, but that factor is
   only polynomial in the orientation length.

The remaining maximum-fiber problem is collective. At the average-wall
endpoint it requires precision growing with $r$ (or a different mechanism);
at a fixed $c$ strictly above that endpoint, the cardinality argument does
not exclude a sufficiently large finite precision. The dictionary alone
does not decide either case.

## 1. Setup

For $r\ge2$, put

\[
q=3^r,\qquad B=\mathbb F_q,\qquad N=q-1=2a.
\]

Fix a generator $g\in B^\times$, and use
$g^0,\ldots,g^{a-1}$ as one representative from every antipodal pair. For
$\epsilon\in\{1,-1\}^a$, write

\[
C_\epsilon(T)=\prod_{i=0}^{a-1}(1-\epsilon_i g^iT),
\qquad
\Phi_u(\epsilon)=(c_1(\epsilon),\ldots,c_u(\epsilon)).
\]

Define the maximum orientation-prefix fiber by

\[
M_r(u)=\max_{z\in B^u}
\#\{\epsilon\in\{\pm1\}^a:\Phi_u(\epsilon)=z\}.
\]

The legal range inherited from the separating-pole packets is
$0\le u\le a-2$. The algebraic statements below make sense at every
truncation, but every comparison with PRs #634/#644 stays in this range.

Let $C_+(T)=\prod_i(1-g^iT)$, and put

\[
b_i=\frac{1-\epsilon_i}{2}\in\{0,1\},
\qquad
F_x(T)=\frac{1+xT}{1-xT}.
\]

We work modulo $T^{u+1}$. Since $2\in B^\times$, the binary
parametrization is unambiguous.

## 2. Exact odd-principal-unit subset sums

Define the truncated odd principal-unit group

\[
U_u^-(B)=
\left\{F\in(1+TB[T]/(T^{u+1}))^\times:
F(T)F(-T)=1\right\}.
\]

Then

\[
\frac{C_\epsilon(T)}{C_+(T)}
=\prod_{i=0}^{a-1}F_{g^i}(T)^{b_i}.
\tag{2.1}
\]

Multiplication by the fixed unit $C_+$ is invertible modulo $T^{u+1}$.
For a second orientation $\eta$, set
$b'_i=(1-\eta_i)/2$. Consequently

\[
\boxed{
\Phi_u(\epsilon)=\Phi_u(\eta)
\iff
\prod_iF_{g^i}^{b_i}=\prod_iF_{g^i}^{b'_i}
\quad\text{in }U_u^-(B).}
\tag{2.2}
\]

Thus locator-prefix fibers are exact fibers of a structured binary
subset-sum map into an abelian $3$-group.

If $F=1+A_1T+\cdots+A_uT^u$, the coefficient of $T^{2j}$ in
$F(T)F(-T)=1$ determines $A_{2j}$ from the preceding coefficients, because
its leading term is $2A_{2j}$. Conversely, arbitrary odd coefficients extend
uniquely by this recursion. Hence

\[
|U_u^-(B)|=q^{\lceil u/2\rceil}.
\tag{2.3}
\]

This is a target cardinality, not an assertion that the orientation map is
onto or that its fibers are uniform.

## 3. Canonical $3$-typical coordinates

Let

\[
K_u=\{k\le u:k\text{ odd and }3\nmid k\},
\qquad
s_k=1+\left\lfloor\log_3\frac uk\right\rfloor.
\]

The canonical decomposition of truncated big Witt units over the
$\mathbb Z_{(3)}$-algebra $B$, restricted to the odd part, gives

\[
U_u^-(B)\simeq\prod_{k\in K_u}W_{s_k}(B).
\tag{3.1}
\]

Normalize the $k$-component so that its $j$-th ghost is the big ghost at
$k3^j$, divided by $k$. With this convention,

\[
\pi_k(F_x)=\frac2k[x^k]\in W_{s_k}(B),
\tag{3.2}
\]

where brackets denote the Teichmüller vector and $2/k$ is a unit in
$\mathbb Z/3^{s_k}\mathbb Z$. Therefore (2.2) is equivalent to

\[
\boxed{
\sum_i b_i[g^{ik}]=\sum_i b'_i[g^{ik}]
\quad\text{in }W_{s_k}(B)
\quad\text{for every }k\in K_u.}
\tag{3.3}
\]

The unit $2/k$ has been cancelled. This is the exact Witt subset-sum
dictionary.

### Audit of the imported decomposition

The factor calculation is performed before reducing to characteristic
three. In the torsion-free ring $\mathbb Z_{(3)}[X]$, the big ghosts of

\[
F_X(T)=\frac{1+XT}{1-XT}
\]

are $2X^m$ for odd $m$ and zero for even $m$. Ghost injectivity in that
universal ring gives (3.2) and kills every even-$k$ component there.
Naturality then reduces the identity to $B$; no injectivity of ghosts in
characteristic three is assumed.

This also prevents a common error: the $3$-typical factors are supplied by
the canonical idempotent decomposition, not by naively grouping raw factors
$(1-x_nT^n)^{-1}$, whose groups are not multiplicatively closed.

Standard references for this decomposition and normalization are Hazewinkel,
*Witt vectors, Part 1*, Sections 9 and 14, and Hesselholt, *Lecture notes on
Witt vectors*, Proposition 10, Example 11, and Proposition 13:

- <https://people.math.rochester.edu/faculty/doug/otherpapers/Hazewinkel-Witt.pdf>
- <https://math.uchicago.edu/~drinfeld/Seminar-2019/Witt_vectors/Hesselholt%20on%20Witt%20vectors.pdf>

The fiber equivalence (2.2) itself is elementary and does not depend on
these references; (3.1)--(3.3) identify its canonical carry coordinates.

### Reduction modulo three and the missing-digit count

Reduction of the $k$-component in (3.3) gives
$\sum_i b_i g^{ik}\in B$. Since
$P_k(\epsilon)=\sum_i\epsilon_i g^{ik}$ differs from this by a fixed affine
unit change, these first digits are precisely the primitive ordinary
moments. The relations $P_{3m}=P_m^3$ supply their Frobenius descendants.

Every odd integer $n\le u$ has a unique form $n=k3^j$ with $k\in K_u$.
Consequently

\[
\sum_{k\in K_u}s_k=\left\lceil\frac u2\right\rceil,
\qquad
\sum_{k\in K_u}(s_k-1)
=\#\{n\le u:n\text{ odd},\ 3\mid n\}
=\left\lfloor\frac{u+3}{6}\right\rfloor.
\tag{3.4}
\]

The first quantity matches (2.3). The second is the exact number of
$B$-valued higher carry slots.

There is also an elementary triangular version. The data

\[
\bigl(P_k(\epsilon)\bigr)_{k\in K_u},
\qquad
\bigl(c_n(\epsilon)\bigr)_{
n\le u,\ n\text{ odd},\ 3\mid n}
\tag{3.5}
\]

determine and are determined by the locator prefix. Even moments are
independent of $\epsilon$. Frobenius supplies every odd nonprimitive moment.
The spectral identity

\[
C_\epsilon(T)C_\epsilon(-T)=1-T^{2a}
\]

recovers even locator coefficients in the legal prefix range. Newton's
identity solves each odd $c_n$ when $3\nmid n$; when $3\mid n$, the second
list in (3.5) supplies exactly the coordinate that division by $n$ cannot
recover. This does not assert statistical independence.

## 4. A bounded-precision obstruction

For $v\ge0$, put

\[
b(v)=\#\{k\le v:k\text{ odd},\ 3\nmid k\}
=\left\lceil\frac v2\right\rceil
-\left\lfloor\frac{v+3}{6}\right\rfloor.
\]

Fix $L\ge1$, truncate every factor in (3.1) to length
$\ell_k=\min(s_k,L)$, and let $\Psi_{u,\le L}$ be the resulting subset-sum
map. Its target has cardinality $q^{D_L(u)}$, where

\[
\begin{aligned}
D_L(u)
&=\sum_{k\in K_u}\min(s_k,L)\\
&=\sum_{j=0}^{L-1}b\!\left(
\left\lfloor\frac{u}{3^j}\right\rfloor\right)\\
&=\frac u2(1-3^{-L})+O(L).
\end{aligned}
\tag{4.1}
\]

No independence hypothesis is needed for pigeonholing. Some truncated fiber
therefore has size at least

\[
\boxed{
\max_z|\Psi_{u,\le L}^{-1}(z)|
\ge\left\lceil\frac{2^a}{q^{D_L(u)}}\right\rceil.}
\tag{4.2}
\]

For fixed $c>0$, put $u_r=\lfloor ca/r\rfloor$. If $L$ is fixed,

\[
\liminf_{r\to\infty}\frac1a
\log\max_z|\Psi_{u_r,\le L}^{-1}(z)|
\ge
\max\left\{0,
\log2-\frac c2(1-3^{-L})\log3\right\}.
\tag{4.3}
\]

Two cases locate the barrier.

- $L=1$ is the complete ordinary-moment/Frobenius signature. Its lower rate
  bound displayed in (4.3) is $\max\{0,\log2-(c/3)\log3\}$, positive for
  $c<3\log2/\log3\approx1.89279$.
- $L=2$ adjoins the first carry in every component, not just $c_3$. Its
  lower bound displayed in (4.3) is
  $\max\{0,\log2-(4c/9)\log3\}$, positive for
  $c<9\log2/(4\log3)\approx1.41959$.

Letting $L\to\infty$ in the target count recovers the full
$q^{\lceil u/2\rceil}$ average wall from PR #634. Formula (4.3) is only a
lower bound for truncated fibers; it does not determine the full-prefix
maximum-fiber rate.

Put

\[
c_L=\frac{2\log2}{(1-3^{-L})\log3},
\qquad
c_\infty=\frac{2\log2}{\log3}.
\tag{4.4}
\]

For every fixed $L$, (4.3) leaves a positive-rate partial fiber whenever
$c<c_L$. In particular, at the average-wall endpoint $c=c_\infty$, its
displayed lower bound equals $3^{-L}\log2>0$; no finite precision can prove
subexponentiality there from these coordinates alone. On the other hand,
$c_L\downarrow c_\infty$. For a fixed $c>c_\infty$, sufficiently large
finite $L$ makes the pigeonhole lower bound zero, so (4.3) does **not** rule
out a finite-precision contraction at that particular $c$.

A simpler form is useful. If an ordinary-moment container $F$ is cut by
$t$ arbitrary $B$-valued functions, one joint subfiber has size at least
$\lceil|F|/q^t\rceil$. Hence any fixed $t$, or more generally
$t=o(a/r)$, changes a normalized exponent by $o(1)$. In particular, the
single $c_3$ carry cannot change any positive critical-scale exponent.

## 5. The first carry pays its full polynomial factor

The obstruction above does not mean $c_3$ is redundant. The following
fixed-depth calibration shows the opposite.

Let $s\ge1$, let $H\subset B^\times$ be any antipodal transversal, let
$R_s=W_s(B)\simeq\operatorname{GR}(3^s,r)$, and fix
$\lambda\in R_s^\times$. For independent binary variables
$\xi_x\in\{0,1\}$, put

\[
Z_s=\sum_{x\in H}\xi_x\lambda[x]\in R_s.
\]

For $1\le t\le s$, define $\theta_t=\cos(\pi/3^t)$ and

\[
\Delta_s(q)=
\sum_{t=1}^s(q^t-q^{t-1})\theta_t^{q/3}.
\]

Then, for every $z\in R_s$,

\[
\left|\Pr(Z_s=z)-q^{-s}\right|
\le q^{-s}\Delta_s(q).
\tag{5.1}
\]

In particular,

\[
\max_z\#\left\{A\subseteq H:
\sum_{x\in A}\lambda[x]=z\right\}
\le\frac{2^a}{q^s}\bigl(1+\Delta_s(q)\bigr).
\tag{5.2}
\]

### Proof of (5.1)

The trace pairing on the free unramified
$\mathbb Z/3^s\mathbb Z$-algebra $R_s$ is perfect. One can see this by
lifting a trace-dual basis of $B/\mathbb F_3$: its trace Gram determinant
stays a unit modulo $3^s$. Thus every additive character is

\[
\chi_y(z)=\exp\!\left(
\frac{2\pi i}{3^s}
\operatorname{Tr}_{R_s/\mathbb Z/3^s\mathbb Z}(yz)
\right)
\]

for a unique $y\in R_s$.

There are $q^t-q^{t-1}$ characters of exact conductor $3^t$. For such a
character, absorb the fixed unit $\lambda$ and divide out its $3$-adic
valuation. Modulo $3$, the remaining trace is a nonzero
$\mathbb F_3$-linear functional on $B$, so it is nonzero at exactly $2q/3$
elements of $B^\times$. On those elements,

\[
\left|\frac{1+\chi_y(\lambda[x])}{2}\right|\le\theta_t.
\]

Because $[-x]=-[x]$, the absolute factors agree for $x$ and $-x$. The
decomposition $B^\times=H\sqcup(-H)$ therefore gives

\[
\left|\prod_{x\in H}
\frac{1+\chi_y(\lambda[x])}{2}\right|
\le\theta_t^{q/3}.
\]

Fourier inversion, followed by the triangle inequality and summation over
the conductor strata, proves (5.1).

The standard Galois-ring trace facts used above are also recorded in Sison,
*Bases of the Galois Ring GR(p^r,m) over Z/(p^r)*, Sections 2--3:
<https://arxiv.org/abs/1410.0289>.

Since

\[
\Delta_s(q)\le
\exp\!\left(s\log q-\frac{\pi^2q}{6\cdot9^s}\right),
\tag{5.3}
\]

the distribution is asymptotically flat whenever
$\pi^2q/(6\cdot9^s)-s\log q\to+\infty$. This includes every fixed $s$ and,
more generally, $s\le(1/2-\eta)r$ for fixed $\eta>0$. It explicitly does
not include the deepest $k=1$ precision $s_1\sim r$ at critical depth.

At depth three the coordinate law can also be checked without invoking the
general decomposition. Every element of $U_3^-(B)$ has the form

\[
1+AT-A^2T^2+CT^3.
\]

The map

\[
1+AT-A^2T^2+CT^3\longmapsto(A,C+A^3)
\]

identifies multiplication on $U_3^-(B)$ with the standard additive
$W_2(B)$ law. Direct expansion gives

\[
F_x(T)\longmapsto(-x,x^3)=2[x].
\tag{5.4}
\]

At $u=3$, (3.1) has only the component $W_2(B)$, and (3.2) sends each flip
factor to $2[x]$. Therefore, for every legal row $r\ge3$,

\[
\left\lceil\frac{2^a}{q^2}\right\rceil
\le M_r(3)
\le\frac{2^a}{q^2}
\left(1+(q-1)2^{-q/3}
+(q^2-q)\cos(\pi/9)^{q/3}\right).
\tag{5.5}
\]

In particular,

\[
M_r(3)=(1+o(1))\frac{2^a}{q^2}.
\tag{5.6}
\]

Similarly $M_r(1)=M_r(2)=(1+o(1))2^a/q$. Passing from depth two to
depth three pays the full possible $q$-factor asymptotically, while
$\log q/a\to0$. This is the distinction between a genuine finite-depth cut
and a critical-rate contraction.

The proof above is confined to the single $k=1$ component. It extends to a
component $k$ when $x\mapsto x^k$ permutes $B^\times$, but no simultaneous
all-$k$ equidistribution is claimed. When $\gcd(k,q-1)>1$, powers can repeat
in a proper multiplicative subgroup and require a separate character-sum
argument.

## 6. Exact affine-coset witnesses for the carry tower

The missing $3$-power layers are also witnessed algebraically. Let
$1\le s<r$, let $V\le B$ be an $s$-dimensional
$\mathbb F_3$-subspace, put $h=3^s$, and choose $\alpha\notin V$. Then
$H=\alpha+V$ is disjoint from $-H$, so its elements occupy $h$ distinct
antipodal pairs and can be extended to an orientation.

The subspace locator

\[
L_V(X)=\prod_{v\in V}(X-v)
\]

is a monic linearized polynomial whose nonzero degrees lie among
$1,3,\ldots,3^s$, and

\[
L_H(X)=\prod_{y\in H}(X-y)=L_V(X)-L_V(\alpha).
\]

After reversal,

\[
B_H(T)=\prod_{y\in H}(1-yT)=T^hL_H(T^{-1})
\]

has only even nonconstant degrees below $h$, because each $h-3^j$ is even,
and has a nonzero odd coefficient at degree $h$. Replacing $H$ by $-H$
therefore preserves every locator coefficient through $h-1$ and changes
$c_h$. All ordinary odd moments through $h$ still agree: the lower ones
follow from the common prefix, while at $h=3^s$ one has
$P_h=P_1^h$ and the two full orientations have the same $P_1$.
Equivalently, the flipped coset block itself has sum zero.

Thus the $c_{3^s}$ cuts are genuinely new, and the two orientations have
Hamming distance exactly $h$. At prefix depth $h-1$, this attains PR #644's
general Hamming lower bound. To regard $c_h$ itself as a legal prefix cut,
assume in addition that $h\le a-2$. The verifier checks this condition and
constructs exact legal witnesses at $h=3,9$ over $\mathbb F_{27}$ and at
$h=3,9,27$ over $\mathbb F_{81}$. It does not infer that a locator fiber,
or any higher Witt fiber, is affine.

## 7. Bounded exact census

The verifier exhausts all $2^4$ orientations over $\mathbb F_9$ and all
$2^{13}=8192$ orientations over $\mathbb F_{27}$ at every legal depth. It
checks the exact partition equivalence (3.5), not just one direction of
Newton's identities.

Selected $\mathbb F_{27}$ rows are:

| depth $u$ | ordinary-moment max | locator-prefix max |
| ---: | ---: | ---: |
| 1, 2 | 304 | 304 |
| 3, 4 | 304 | 28 |
| 5, 6 | 28 | 3 |
| 7, 8 | 3 | 2 |
| 9, 10, 11 | 3 | 2 |

At $u=3$, the ordinary signature has $27$ realized values, while the
locator prefix has $729=q^2$; the maximum fiber drops from $304$ to $28$.
This is finite evidence for the exact $c_3$ cut, not an asymptotic proof.
The asymptotic statement is (5.5)--(5.6).

## 8. Consumer-backward hypothesis audit

| Item | Required here | Supplied |
| --- | --- | --- |
| field | $B=\mathbb F_{3^r}$, $r\ge2$ | printed in Section 1 |
| antipodal coordinates | one representative from every $\{x,-x\}$ | $g^0,\ldots,g^{a-1}$ |
| legal prefix comparison | $0\le u\le a-2$ | printed; no algebra outside it is fed to a pole consumer |
| division by two | odd characteristic | $2\in B^\times$ |
| ordinary signature | even moments fixed; odd moments Frobenius-closed | follows from $\epsilon_i\in\{\pm1\}\subset\mathbb F_3$ |
| Witt decomposition | canonical truncated decomposition over a $\mathbb Z_{(3)}$-algebra | lift/descent and normalization audited in Section 3 |
| ghost calculation | injective ghost map | used only in the universal torsion-free lift |
| trace pairing | $W_s(B)$ finite unramified over $\mathbb Z/3^s\mathbb Z$ | dual-basis determinant proof in Section 5 |
| Fourier half-system | $H\sqcup(-H)=B^\times$, $\lambda$ a unit | both stated; no parity condition on $r$ |
| flatness range | $\Delta_s(q)\to0$ | exact sufficient condition (5.3) |
| critical obstruction | fixed $L$, or $t=o(a/r)$ | quantifiers printed in Section 4 |
| affine common prefix | $1\le s<r$ and $\alpha\notin V$ | stated; then $h-1\le a-2$ |
| affine $c_h$ cut inside legal range | $3^s\le a-2$ | imposed separately and checked on the listed rows |

PR #644 supplies the coarse fixed-$c$ bracket and names the locator-cut wall.
PR #634 supplies only the full-prefix target-cardinality lower floor used for
comparison. Amended PR #636 supplies qualitative effective-image-collapse
geography only. No exact image, uniformity, $Q_{\rm img}=1$, exact $G_1$, or
C7 payment claim is imported.

The following paragraph is consumer context and is not used in any proof
above. Integrated PR #645 materially narrows the prize-facing
interpretation. It classifies
the known separating-extension orientation floors in PRs #631/#634 as
admissible but not prize-relevant under the full-field denominator: their
sufficient pair-separation construction has
$e_{\rm MCA}=e^{-\Theta(a)}$. PR #645 labels necessity of that field cost
open. Live PR #647 (open head e5c2baa) subsequently refutes a universal
$|F|^{1/2+o(1)}$ cap, while leaving #645's exponential-field Case-B
residual open; its witness is poly-field and does not supply a prize-facing
orientation line. This packet does not change either classification. A
prize-facing consumer still needs a challenge-legal confined line or a
separate Case-B theorem. Neither is supplied here.

## 9. Ledger effect and next wall

Paste-ready experimental ledger entry:

> On the antipodal orientation class over $\mathbb F_{3^r}$, depth-$u$
> locator prefixes are exact binary subset sums in
> $\prod_{k\text{ odd},\,3\nmid k}
> W_{1+\lfloor\log_3(u/k)\rfloor}(\mathbb F_{3^r})$.
> Reduction modulo $3$ is the ordinary Fourier/Frobenius container; the
> remaining $\lfloor(u+3)/6\rfloor$ Witt digits are the
> characteristic-three locator carries. Every fixed precision $L$ retains a
> critical-scale fiber of normalized rate at least
> $\max\{0,\log2-(c/2)(1-3^{-L})\log3\}$. Thus it leaves a positive-rate
> obstruction for $c<c_L$ and for every finite $L$ at the endpoint
> $c_\infty=2\log2/\log3$; it does not exclude sufficiently large finite
> $L$ at a fixed $c>c_\infty$. At the shallow calibration $u=3$, the first
> carry is asymptotically fully mixing and
> $M_r(3)\sim2^a/q^2$. The result is pre-atlas and supplies no
> prize-relevant received line or C7/FI-field payment.

The highest-value residual in this lane is now precise:

1. control the joint subset-sum distribution when Witt precision grows,
   especially the $k=1$ component with $s_1\sim r$ at critical depth;
2. prove a collective higher-digit max-fiber contraction, or construct an
   exponential concentration witness;
3. separately, for a prize consequence, realize the prefix control on a
   challenge-legal confined line after PR #645.

Already at the collective $W_2$ layer, Fourier inversion identifies the
next exact object. Primitive characters give trace-evaluation words

\[
w_y(x)=\operatorname{Tr}_{B/\mathbb F_3}
\left(\sum_{\substack{k\text{ odd},\ 3\nmid k\\3k\le u}}y_kx^k\right)
\quad (x\in H).
\]

After quotienting coefficient tuples that define the zero trace function,
the needed estimate is a weighted enumerator of the form

\[
\sum_y\cos(\pi/9)^{\operatorname{wt}_H(w_y)}.
\]

The single $k=1$ code has exact nonzero weight $q/3$ on $H$, which is why
Section 5 closes. Multiple powers require a genuine weighted-enumerator
bound, especially when $\gcd(k,q-1)>1$; a minimum-distance statement alone
does not control the sum.

## Nonclaims

- No improved fixed-$c$ upper bound for the full locator-prefix maximum fiber
  is claimed.
- Exact Witt coordinates do not imply surjectivity, independence, or
  uniformity of the full orientation map.
- The shallow $W_s$ mixing theorem is not applied simultaneously to all
  $k$-components and does not cover $s\sim r$.
- The finite $\mathbb F_{27}$ census is exhaustive only for that row; the
  $\mathbb F_{81}$ entries are exact affine-coset witnesses, not a full
  census.
- No locator or Witt fiber is claimed to be an affine subspace.
- No arbitrary-support, augmented-atlas, primitive-residual, C7 payment,
  FI-field discharge, or profile-envelope theorem is claimed.
- No exact orientation image size is asserted outside the explicitly
  exhaustively checked finite row.
- No received line, pole, extension reserve, slope count, target reserve, or
  prize-value improvement is constructed.
- No statement is moved into the frontiers TeX.
