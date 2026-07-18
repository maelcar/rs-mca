# C3 same-line common-factor explosion

**Status: COUNTEREXAMPLE**

This packet cuts one tempting but false route to the C3 planted-block
payment.  Actual witness supports on one received line can carry
positive-density common locator factors in exponentially many distinct
ways, with exponentially many distinct slopes per factor.  Actualness,
same-line incidence, and a genuine common divisor therefore do not create
the subexponential candidate census required by C3.

The result does not contradict the repaired planted-payment criterion in
experimental/asymptotic_rs_mca_frontiers.tex.  That criterion explicitly
assumes small description entropy, a bound at the natural residual profile
scale, and a distinct-slope projection estimate.  The construction below
shows why those hypotheses cannot be inferred from the words common factor.

| item | result |
| --- | --- |
| broad common-factor-to-census implication | false |
| growing-depth obstruction | \(w=\Theta(n/\log n)\), exponentially many factors and slopes per factor |
| exact-symmetry obstruction | after exact stabilizer and scaled-inversion deletion, exponentially many large cells survive |
| exact finite control | one line over \(\mathbb F_{17^5}\), 472 exact bad slopes |
| finite post-symmetry slice | 52 noncoset common-divisor cells and 194 slopes; 48 repeated-factor cells carry 190 slopes |
| printed repaired C3 criterion | not refuted |

Credit: the arithmetic coset census in
experimental/notes/thresholds/c3_planted_divisor_census.md was developed
by Holm Buar.  This packet retains that census theorem and narrows only its
payment interpretation.

**Scope correction to the older census note.**  The older note's full-PAID
and triangular-shift payment interpretation is superseded and withdrawn
here.  Its \(\sigma(N)\) arithmetic proves a candidate census only.  The
triangular shift \(Q_S=Q_PQ_R\) identifies the residual prefix fiber but
does not bound that fiber at its natural profile scale or supply the
distinct-slope projection.  Full C3 payment therefore remains open.

## 1. Source contract

The relevant manuscript interfaces are:

- the C3 catalogue paragraph in sec:cell-catalogue, which requires a
  subexponential census of allowed planted divisors, the residual prefix
  estimate, and a slope projection;
- def:algebraically-planted, which permits support locators, common
  factors, ramification polynomials, quotient fibers, and received-line
  resultants, but separately requires a subexponential family;
- prop:planted-payment-repaired, which requires description entropy,
  natural profile scales, and distinct-slope projection;
- thm:exact-list-line-bijection and
  cor:exact-prefix-ray-realization, which turn a complete locator-prefix
  fiber into exact witnesses on one received line at a separating pole.

These interfaces distinguish three questions that must not be collapsed:

1. Is a polynomial a genuine factor of actual witness locators?
2. Is the family of possible factors subexponential?
3. Is the slope image of each residual factor cell bounded at its natural
   profile scale?

The coset census answers question 2 for quotient, ramification, and
twin-coset generators.  It does not answer question 3, and it does not
classify all factors arising from actual witnesses.

## 2. A two-stage prefix theorem

Let \(\mathbb B\) be a finite field of size \(q\), let
\(D=A\sqcup E\), with \(|A|=a\) and \(|E|=e\), and fix integers
\(b\le a\), \(r\le e\).  Put
\[
 m=b+r,\qquad 0\le w\le m-2,\qquad k=m-w-1.
\]
For an \(m\)-set \(S\), let \(\Phi_w(S)\in\mathbb B^w\) be the first
\(w\) coefficients below the leading term of its monic locator
\[
 Q_S(X)=\prod_{x\in S}(X-x).
\]

**Theorem 2.1 (two-stage prefix amplification).**  There is a prefix
\(z\in\mathbb B^w\), a family
\(\mathcal I\subseteq\binom Ab\), and pairwise disjoint subfamilies
\[
 \mathcal G_T
   =\{T\cup R:R\in\tbinom Er,\ \Phi_w(T\cup R)=z\}
   \subseteq\Phi_w^{-1}(z)
       \qquad (T\in\mathcal I)
\]
such that
\[
 |\mathcal I|
   \ge \left\lceil\frac{\binom ab}{q^w}\right\rceil,
 \qquad
 |\mathcal G_T|
   \ge \left\lceil\frac{\binom er}{q^w}\right\rceil
       \quad\text{for every }T\in\mathcal I.
 \tag{2.1}
\]
Every locator in \(\mathcal G_T\) is divisible by the distinct monic
polynomial \(Q_T\).

If a finite extension \(\mathbb F/\mathbb B\) contains a pole separating
the complete fiber \(\Phi_w^{-1}(z)\), then all supports in all
\(\mathcal G_T\) are exact agreement supports of distinct MCA-bad slopes
on one received line for \(\operatorname{RS}_{\mathbb F}(D,k)\).

**Proof.**  Fix \(T\in\binom Ab\).  The map
\[
 R\longmapsto\Phi_w(T\cup R),\qquad R\in\binom Er,
\]
has at most \(q^w\) values.  Choose a largest fiber, using a fixed
tie-breaking order, and call its value \(z_T\).  Its size is at least the
second lower bound in (2.1).  The values \(z_T\), as \(T\) varies, again
occupy at most \(q^w\) bins.  A largest bin supplies one \(z\) and at least
the first number in (2.1) choices of \(T\).

The cells are disjoint because \(S\cap A=T\), and
\(Q_{T\cup R}=Q_TQ_R\).  Distinct \(T\)'s have distinct monic locators.
Finally apply cor:exact-prefix-ray-realization to the complete prefix
fiber.  Its support-to-slope map is injective at a separating pole, and
every agreement set is exactly its support. \(\square\)

The last step can always be arranged after a scalar extension.  If the
complete fiber has size \(L\), it suffices that
\[
 |\mathbb F|>n+k\binom L2.
 \tag{2.2}
\]

### Growing-depth consequence

Take \(\mathbb B_t=\mathbb F_{2^t}\),
\(D_t=\mathbb B_t^\times\), and \(n_t=2^t-1\).  Split \(D_t\) into two
parts of asymptotic size \(n_t/2\), take \(b_t\) and \(r_t\) to be the
nearest half-sizes of those parts, and set
\[
 w_t=
 \left\lfloor\frac{(\log 2)n_t}{4\log|\mathbb B_t|}\right\rfloor.
\]
Then
\[
 \binom{|A_t|}{b_t}
   =\exp\!\left((\tfrac12\log2+o(1))n_t\right),
 \qquad
 |\mathbb B_t|^{w_t}
   \le\exp\!\left(\tfrac14(\log2)n_t\right),
\]
and the same estimate holds on \(E_t\).  Theorem 2.1 therefore gives, in
one depth-\(w_t\) prefix fiber,
\[
 \exp\!\left((\tfrac14\log2+o(1))n_t\right)
\]
distinct common-factor candidates, each carrying that many supports and,
after separation, distinct bad slopes.  Here
\[
 w_t=\Theta(n_t/\log n_t),\qquad
 m_t/n_t\to\tfrac12,\qquad k_t/n_t\to\tfrac12.
\]
Since \(L\le\binom{n_t}{m_t}=\exp(O(n_t))\), an extension of degree
\(O(n_t/\log n_t)\) satisfies (2.2), so
\(\log|\mathbb F_t|=O(n_t)\).

This is a growing-depth obstruction, not merely the identity-prefix case.
It proves that same-line actualness and locator divisibility do not imply a
subexponential factor atlas.

## 3. An antipodal construction that survives exact symmetry deletion

The preceding theorem does not classify which of its supports an arbitrary
first-match atlas assigns to earlier quotient cells.  A depth-one
antipodal family gives a separate route cut that survives deletion by the
two exact support-symmetry predicates below.  This does not cover quotient
cells with marked remainders or other row-specific first-match data.

Let \(p\) be odd, \(D=\mathbb F_p^\times\), \(n=p-1\), and choose a
transversal
\[
 D=A\sqcup(-A),\qquad |A|=M=n/2.
\]
Fix \(b\), put \(m=2b\), \(w=1\), and \(k=m-2\).  For
\(s\in\mathbb F_p\), define
\[
 f_s=\#\{T\in\tbinom Ab:\sum_{x\in T}x=s\}.
\]
For each \(T\in\binom Ab\), define
\[
 \mathcal C_T
  =\{T\cup(-U):U\in\tbinom Ab,\ \sum U=\sum T\}.
 \tag{3.1}
\]

Every support in (3.1) has sum zero and hence lies in
\(\Phi_1^{-1}(0)\).  The cells are disjoint,
\[
 |\mathcal C_T|=f_{\sum T},\qquad
 Q_{T\cup(-U)}=Q_TQ_{-U},
 \]
and
\[
 \sum_T|\mathcal C_T|=\sum_s f_s^2
    \ge\frac{\binom Mb^2}{p}.
 \tag{3.2}
\]
For a maximizing \(s_*\),
\[
 f_{s_*}\ge\binom Mb/p.
 \tag{3.3}
\]
Thus the one band \(\sum T=s_*\) has \(f_{s_*}\) distinct common-factor
cells, each with \(f_{s_*}\) supports.

Take \(b/M\to1/2\).  Then \(b/n\to1/4\), \(m/n\to1/2\),
\(k/n\to1/2\), and
\[
 f_{s_*}=\exp\!\left((\tfrac12\log2+o(1))n\right).
 \tag{3.4}
\]

Now delete every support invariant under a nontrivial multiplicative
subgroup and every support invariant under any scaled inversion
\(x\mapsto c/x\).  These are the exact stabilizer and scaled-inversion
support tests; no claim is made here about the broader quotient-remainder
atlas.  The total number deleted is at most
\[
 \tau(n)2^{n/2}+n\,2^{n/2+1}
   =\exp\!\left((\tfrac12\log2+o(1))n\right).
 \tag{3.5}
\]
Indeed a nontrivial subgroup has orbits of size at least two, and a scaled
involution has at most two fixed points and otherwise two-cycles.

The selected band in (3.2) has \(f_{s_*}^2
=\exp((\log2+o(1))n)\) incidences.  By (3.5), all but
\(\exp(o(n))\) of its \(f_{s_*}\) cells retain at least
\(f_{s_*}/2\) supports.  Removing the subexponential quotient,
ramification, and twin-coset factor census still leaves exponentially many
noncoset factors.  Choose a pole separating the complete fiber
\(\Phi_1^{-1}(0)\).  Then cor:exact-prefix-ray-realization gives a
bijection from that complete fiber to the exact-agreement witness incidence,
so the surviving supports yield distinct slopes and none shares its slope
with a deleted support.

Therefore removal by these exact support-symmetry predicates does not repair
the broad common-factor-to-census implication.  Full C1/C2 first-match
survival, including canonical quotient remainders, is not asserted.

## 4. Exact \(\mathbb F_{17}\) control

The certificate fixes
\[
 D=\mathbb F_{17}^\times,\quad
 A=\{1,\ldots,8\},\quad E=-A=\{9,\ldots,16\},
\]
with
\[
 b=r=3,\quad m=6,\quad w=1,\quad k=4,\quad z=0.
\]
The triple-sum multiplicities on \(A\), for residues \(0,\ldots,16\),
are
\[
 (4,3,2,1,1,0,1,1,2,3,4,5,6,6,6,6,5).
\]
Consequently the 56 cells have size distribution
\[
 1^4,\ 2^4,\ 3^6,\ 4^8,\ 5^{10},\ 6^{24}.
\]
They are disjoint and contain 256 supports.  All 56 polynomials \(Q_T\)
are common divisors.  Fifty-two occur in at least two locators, accounting
for 252 slopes.  The whole-cell gcd is exactly \(Q_T\) for 48 cells
carrying 244 slopes; the distinction matters because four two-support
cells share one additional residual root.

The complete prefix-zero fiber contains 472 of the
\(\binom{16}{6}=8008\) supports.  Its occupancy by \(|S\cap A|\) is
\[
 1:41,\quad 2:67,\quad 3:256,\quad 4:67,\quad 5:41.
\]

Inside the balanced 256-support slice, first delete every support with an
exact nontrivial multiplicative stabilizer.  Exactly 56 supports are
deleted, leaving 52 cells and 200 slopes.  Then delete every remaining
support fixed by some \(x\mapsto c/x\).  Six more supports are deleted,
leaving 52 cells and 194 slopes with distribution
\[
 1^4,\ 2^6,\ 3^{10},\ 4^{12},\ 5^{20}.
\]
Every surviving cell still has common divisor \(Q_T\).  Four are singleton
cells; the other 48 genuinely repeat their common factor and carry 190
slopes.  Forty cells carrying 172 slopes have whole-cell gcd exactly
\(Q_T\).  No three-point \(T\) is a subgroup coset, multiplier-fixed root
set, or twin-coset root set; already \(3\nmid16\) is the cardinality
obstruction.

### Exact pole line

Let
\[
 \mathbb F=\mathbb F_{17}[\theta]/(\theta^5+\theta+3),
 \qquad \alpha=\theta.
\]
The verifier checks Rabin's criterion
\[
 \gcd(X^5+X+3,X^{17}-X)=1,\qquad
 X^{17^5}\equiv X\pmod{X^5+X+3}.
\]
Thus \(\theta\) has degree five.  Locator differences inside the
prefix-zero fiber have degree at most four, so their values at \(\theta\)
are pairwise distinct.  The generic numerical condition also has ample
room:
\[
 17^5=1{,}419{,}857
   >16+4\binom{472}{2}=444{,}640.
\]

With
\[
 U=X^6,\qquad
 f(x)=\frac{x^6}{x-\theta},\qquad
 g(x)=-\frac1{x-\theta},
\]
each support has
\[
 P_S=X^6-Q_S,\quad
 \gamma_S=P_S(\theta),\quad
 h_S=\frac{P_S-P_S(\theta)}{X-\theta}.
\]
The verifier performs arithmetic in \(\mathbb F_{17^5}\), checks all 472
slopes are distinct, and checks for every one of them that the agreement
set of \(f+\gamma_Sg\) with \(h_S\) is exactly \(S\).  It also checks the
standard pole identity showing that \(g\) is noncommon.

## 5. A saturation discriminator

The same complete fiber attains the depth-one Johnson intersection bound:
\[
 \{1,2,3,4,8,16\}\cap\{1,2,3,4,9,15\}
   =\{1,2,3,4\},
\]
and no pair intersects in more than four points.  Nevertheless the pole
line maps all 472 supports to distinct slopes, so its support-to-slope
occupancy is one.

Therefore attainment of the Johnson intersection bound is a
constant-weight proximity event, not by itself the manuscript's C7
saturation datum.  C7 records the actual witness-to-explanation-to-slope
projections and their fiber cardinalities.  This packet makes no general
C7 claim; the finite example is only a regression against identifying
those two notions.

## 6. Consequence for C3

The following implication is false:

> a positive-density locator factor shared by actual supports on one
> received line implies a subgroup-coset or multiplier-fixed census, or
> a subexponential or identity-scale slope charge inferred solely from the
> common-factor property.

The repaired C3 criterion remains sound.  In the counterexample, factor
description entropy and residual natural profile scale are both
exponential.  Such factors cannot be declared paid merely because they
are constructible.  They must either:

1. belong to a predeclared source-rooted family with a proved
   subexponential parameter space, residual prefix estimate, and slope
   projection; or
2. remain in the complete-prefix, balanced-core, or analytic residual with
   their natural profile scale and distinct-ray obligation visible.

The next positive C3 lane is therefore not another unrestricted
common-factor census.  It is a canonical received-line-resultant theorem:
identify a bounded-parameter resultant family from the interpolation
equations, prove that the family is witness-exhaustive for the intended C3
row, and then prove its residual and slope-image budgets.  In the prime-field
multiplicative-coset setting, thm:head-flatness is a possible residual-fiber
input only when its hypotheses \(wd<p\) and its nonvacuous error comparison
hold; the distinct-slope projection and ledger add-back remain separate.

## 7. Nonclaims

- No contradiction to def:algebraically-planted or
  prop:planted-payment-repaired.
- No full C3, C7, or asymptotic RS-MCA payment.
- No assertion that every common factor must be routed to C3; the result
  says the factor property alone cannot justify such routing or payment.
- No full C1/C2 first-match-survival theorem; the antipodal deletion covers
  only exact multiplicative stabilizers and scaled inversions, not marked
  quotient remainders or other row-specific atlas data.
- No claim that the finite \(\mathbb F_{17}\) row is a deployed security
  row.
- The growing-depth theorem and the exact-symmetry-surviving depth-one theorem
  are complementary; neither is substituted for the other.

## 8. Reproducibility

The frozen certificate is
experimental/data/certificates/c3-same-line-common-factor-explosion/c3_same_line_common_factor_explosion.json.
The verifier is standard-library only, deterministic, and normally runs
in under ten seconds:

~~~bash
python3 experimental/scripts/verify_c3_same_line_common_factor_explosion.py --check
python3 experimental/scripts/verify_c3_same_line_common_factor_explosion.py --tamper-selftest
~~~

The packet-local Lean companion is
experimental/lean/c3_same_line_common_factor_explosion/C3SameLineCommonFactorExplosion.lean,
with scope recorded in
experimental/lean/c3_same_line_common_factor_explosion/CORRESPONDENCE.md.
The nested ceiling-pigeonhole kernel
`C3SameLineCommonFactorExplosion.exists_nested_ceiling_fiber` is proved.
The full support-cell, locator-divisibility, and scalar-extension composition
is an honest `sorry` statement target.  The standalone package depends on the
pinned `GrandeFinale.ScalarExtensionListLine` API but does not modify or import
anything into the pinned `GrandeFinale.lean` package root.
