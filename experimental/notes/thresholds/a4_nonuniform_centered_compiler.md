# A4 successor: centered compilation for nonuniform live fibers

**Status:** the finite multiplicity-class factorization and centered compiler
below are PROVED. The classwise centered collision energies remain OPEN.
This packet changes no TeX and claims no deployed threshold.

**Stack and lineage:** this is a successor to PR #664, commit
\(0aee8592065efacedc9f71679e6eda4f704f2469\), itself based on integrated
commit \(36de5bfcc7d6e0ca44806112acec2f4a1b4a7532\). It preserves PR #664's
trace-rank theorem and centered uniform-fold compiler. Its exact delta is to
replace the uniform-live-fiber hypothesis by the actual multiplicity profile.

**Replay:**

    python3 experimental/scripts/verify_a4_nonuniform_centered_compiler.py --write
    python3 experimental/scripts/verify_a4_nonuniform_centered_compiler.py --check
    python3 experimental/scripts/verify_a4_nonuniform_centered_compiler.py --tamper-selftest

The verifier is standard-library-only, imposes a 1 GiB address-space cap,
enumerates exact elementary-two-group characters and subset sums, and writes
experimental/data/certificates/a4-nonuniform-centered-compiler/
a4_nonuniform_centered_compiler.json.

## 1. Result map

Let a quotient map be restricted to an arbitrary nonempty coordinate-live
set, while the object remains the full slice \(\binom Tm\). The surviving
fibers need not have a common size. If the projected phase is still constant
on each surviving fiber, group quotient points by their actual fiber
multiplicities. The full fixed-weight generating polynomial then factors as
one elementary polynomial, raised to its multiplicity, for each class.

If
\[
 D_*=\sum_{s:\,n_s>0}s\ge2,
\]
centered Parseval, Cauchy--Schwarz on the best pair of factor slots, and
\(L^\infty\) on the other slots give the primary convex compiler. The
symmetric \(D_*\)-fold Hölder expression remains a valid corollary. At
\(D_*=2\) it agrees with the primary bound; for \(D_*>2\) the primary bound
can be strictly sharper. The multiplicity-\((1,3)\) example that falsifies a
fake uniform power is handled by its true product.

The theorem removes the complete-uniform-fiber guard for a coordinate-level
full fixed-weight slice. It does not apply after a support-level first-match
deletion, supply the classwise energies, handle an all-singleton restriction
with folding gain, encode fixed PO3 occupancy statistics without markers,
assign overlap with other cells, or close A4.

## 2. Exact multiplicity-class factorization

Let \(T\ne\varnothing\), let \(\phi:T\twoheadrightarrow Q\), let \(A\)
be one finite abelian group, and let \(a:T\to A\) be the translated
effective phase. Assume this group-valued phase factors through the live map:
\[
 a(t)=h(\phi(t)),\qquad h:Q\to A.
 \tag{NC1}
\]
This implies that every character of \(A\), not merely a possibly
nonseparating selected subset, has one common value on each surviving fiber.

For the manuscript consumer, take \(A=A_\phi=V/W_\phi\), fix \(t_0\), and
use
\[
 a(t)=[g(t)-g(t_0)]\in A_\phi.
 \tag{NC1a}
\]
If \(\widetilde\chi\) is any ambient extension of the pulled-back effective
character, the original affine phase contributes
\(\widetilde\chi(g(t_0))^m\) to the weight-\(m\) coefficient. Its absolute
value is one, so every \(L^1\) statement below is translation invariant. Put
\[
 c_y=|\phi^{-1}(y)|,\qquad
 Q_s=\{y\in Q:c_y=s\},\qquad n_s=|Q_s|,
 \tag{NC2}
\]
and let
\[
 \mathcal S=\{s\ge1:n_s>0\},\qquad
 N=|T|=\sum_{s\in\mathcal S}s n_s,\qquad
 D_*=\sum_{s\in\mathcal S}s.
 \tag{NC3}
\]
The definition of \(D_*\) is load-bearing: it counts the repeated polynomial
factors, once for every copy \(1\le\ell\le s\) of each nonempty
multiplicity class. It is neither \(\max\mathcal S\) nor \(|Q|\).

For \(0\le j\le n_s\), define
\[
 M_{s,j}=\binom{n_s}{j},
 \tag{NC4}
\]
\[
 r_{s,j}(a)=
 \left|
 \left\{J\in\binom{Q_s}{j}:
       \sum_{y\in J}h(y)=a\right\}
 \right|,
 \qquad
 \mathrm{SP}_{s,j}=\sum_{a\in A}r_{s,j}(a)^2,
 \tag{NC5}
\]
and, for \(\chi\in\widehat A\),
\[
 e_{s,j}(\chi)
 =\sum_{J\in\binom{Q_s}{j}}
  \chi\!\left(\sum_{y\in J}h(y)\right).
 \tag{NC6}
\]
The class polynomial is
\[
 E_{s,\chi}(Y)
 =\prod_{y\in Q_s}(1+\chi(h(y))Y)
 =\sum_{j=0}^{n_s}e_{s,j}(\chi)Y^j.
 \tag{NC7}
\]

Each \(y\in Q_s\) has exactly \(s\) live preimages, so the full live
generating polynomial is exactly
\[
 \prod_{t\in T}(1+\chi(a(t))Y)
 =\prod_{s\in\mathcal S}E_{s,\chi}(Y)^s.
 \tag{NC8}
\]
No uniformity approximation occurs.

Index the coefficient expansion by
\[
 \mathcal J_{\mathbf c,m}
 =
 \left\{
 (j_{s,\ell})_{\substack{s\in\mathcal S\\1\le\ell\le s}}:
 0\le j_{s,\ell}\le n_s,\quad
 \sum_{s,\ell}j_{s,\ell}=m
 \right\}.
 \tag{NC9}
\]
Then
\[
 [Y^m]\prod_{t\in T}(1+\chi(a(t))Y)
 =
 \sum_{\mathbf j\in\mathcal J_{\mathbf c,m}}
 \prod_{s\in\mathcal S}\prod_{\ell=1}^{s}
 e_{s,j_{s,\ell}}(\chi).
 \tag{NC10}
\]

Define
\[
 w_{\mathbf j}
 =\frac{
 \prod_{s\in\mathcal S}\prod_{\ell=1}^{s}M_{s,j_{s,\ell}}
 }{\binom Nm}.
 \tag{NC11}
\]
These are probability weights:
\[
 \sum_{\mathbf j\in\mathcal J_{\mathbf c,m}}w_{\mathbf j}=1.
 \tag{NC12}
\]
Indeed, their numerator sum is the coefficient of \(Y^m\) in
\[
 \prod_{s\in\mathcal S}(1+Y)^{s n_s}=(1+Y)^N.
 \]

## 3. Centered class energies

Every class must use the same target \(A\). Put
\[
 \kappa_{s,j}
 =\frac{|A|\mathrm{SP}_{s,j}}{M_{s,j}^2},
 \qquad
 \eta_{s,j}=\kappa_{s,j}-1.
 \tag{NC13}
\]
As in PR #664,
\[
 \eta_{s,j}
 =\frac{|A|}{M_{s,j}^2}
 \sum_{a\in A}
 \left(r_{s,j}(a)-\frac{M_{s,j}}{|A|}\right)^2,
 \tag{NC14}
\]
so
\[
 0\le\eta_{s,j}\le |A|-1,
 \qquad
 \eta_{s,0}=\eta_{s,n_s}=|A|-1.
 \tag{NC15}
\]
Centered Parseval over the one common dual group is
\[
 \sum_{\chi\ne1}|e_{s,j}(\chi)|^2
 =|A|\mathrm{SP}_{s,j}-M_{s,j}^2
 =\eta_{s,j}M_{s,j}^2.
 \tag{NC16}
\]

Let
\[
 \mathcal I=\{(s,\ell):s\in\mathcal S,\ 1\le\ell\le s\},
 \qquad |\mathcal I|=D_*.
\]
For \(D_*\ge2\) and one fixed allocation \(\mathbf j\), define
\[
 \theta_{\mathbf j}
 =
 \min_{\substack{u,v\in\mathcal I\\u\ne v}}
 \sqrt{\eta_{u,j_u}\eta_{v,j_v}}.
 \tag{NC17}
\]
The pair consists of distinct factor slots. The two slots may carry the same
class, weight, and therefore the same function. The minimizing pair is
chosen once for the fixed allocation, never separately for each character.

Define the primary pairwise compiler
\[
 P_{\mathbf c}^{\circ}(m)
 =
 \sum_{\mathbf j\in\mathcal J_{\mathbf c,m}}
 w_{\mathbf j}\theta_{\mathbf j}.
 \tag{NC18}
\]
For comparison, retain the symmetric and uncentered quantities
\[
 K_{\mathbf c}^{\circ}(m)
 =
 \sum_{\mathbf j\in\mathcal J_{\mathbf c,m}}
 w_{\mathbf j}
 \prod_{u\in\mathcal I}\eta_{u,j_u}^{1/D_*},
 \tag{NC19}
\]
\[
 K_{\mathbf c}(m)
 =
 \sum_{\mathbf j\in\mathcal J_{\mathbf c,m}}
 w_{\mathbf j}
 \prod_{u\in\mathcal I}\kappa_{u,j_u}^{1/D_*}.
 \tag{NC20}
\]
Use \(0^{1/D_*}=0\).

### Theorem E (pairwise centered multiplicity-class compiler)

Assume (NC1), one common target \(A\), and \(D_*\ge2\). For every
\(\mathfrak M\subseteq\widehat A\setminus\{1\}\) and
\(0\le m\le N\),
\[
 \boxed{
 \frac1{\binom Nm}
 \sum_{\chi\in\mathfrak M}
 \left|
 [Y^m]\prod_{t\in T}(1+\chi(a(t))Y)
 \right|
 \le P_{\mathbf c}^{\circ}(m).}
 \tag{NC21}
\]
Moreover,
\[
 P_{\mathbf c}^{\circ}(m)
 \le K_{\mathbf c}^{\circ}(m)
 \le K_{\mathbf c}(m)-1.
 \tag{NC22}
\]

### Proof

Fix one allocation and two distinct slots \(u,v\). Bound every other factor
in \(L^\infty\), enlarge the selected major set to all nontrivial
characters, and apply Cauchy--Schwarz only to \(u,v\):
\[
\begin{aligned}
 \sum_{\chi\in\mathfrak M}\prod_{r\in\mathcal I}|e_{r,j_r}(\chi)|
 &\le
 \left(\prod_{r\ne u,v}M_{r,j_r}\right)
 \left(\sum_{\chi\ne1}|e_{u,j_u}(\chi)|^2\right)^{1/2}
 \left(\sum_{\chi\ne1}|e_{v,j_v}(\chi)|^2\right)^{1/2}\\
 &=\left(\prod_{r\in\mathcal I}M_{r,j_r}\right)
 \sqrt{\eta_{u,j_u}\eta_{v,j_v}}.
\end{aligned}
 \tag{NC23}
\]
Repeated identical factors are valid Cauchy slots: then the middle product
is simply the same \(L^2\) norm twice. If one selected \(\eta\) is zero,
centered Parseval makes that factor identically zero on every nontrivial
character, so the zero right side is exact.

Minimize (NC23) over pairs, sum over allocations using (NC10), divide by
\(\binom Nm\), and use (NC11). This proves (NC21).

To compare with symmetric Hölder, sort the \(D_*\) values in one allocation:
\[
 0\le z_1\le z_2\le\cdots\le z_{D_*}.
\]
Then
\[
 \sqrt{z_1z_2}\le\left(\prod_{r=1}^{D_*}z_r\right)^{1/D_*}.
 \tag{NC24}
\]
Thus \(P_{\mathbf c}^{\circ}\le K_{\mathbf c}^{\circ}\). The symmetric
quantity is also valid directly: \(D_*\)-fold Hölder and (NC16) give
\[
 \sum_{\chi\ne1}|e_{s,j}(\chi)|^{D_*}
 \le\eta_{s,j}M_{s,j}^{D_*}.
 \tag{NC25}
\]
Finally, for nonnegative \(a_1,\ldots,a_{D_*}\),
\[
 \left(\prod_{r=1}^{D_*}(1+a_r)\right)^{1/D_*}
 \ge
 1+\left(\prod_{r=1}^{D_*}a_r\right)^{1/D_*}.
 \tag{NC26}
\]
Average (NC26) using (NC12) and \(\kappa=1+\eta\) to obtain the second
inequality in (NC22). Equality may occur. At \(D_*=2\), pairwise and
symmetric bounds coincide; for \(D_*>2\), the primary bound can be strict.

### Actual major-arc payment and class tails

The finite theorem is a compiler, not payment by itself. For a designated
family of quotient maps \(\mathcal I_N\), actual MA consumption requires
\[
 \sum_{\phi\in\mathcal I_N}
 P_{\mathbf c(\phi)}^{\circ}(m)=e^{o(N)}
 \tag{NC27}
\]
uniformly over the live lines and leaves after a disjoint assignment of the
relevant character bands.

The pairwise form needs only two controlled slots in an allocation. If a
slot is called controlled when its class and weight have a certified centered
energy bound, a sufficient decomposition is
\[
\begin{aligned}
 P_{\mathbf c}^{\circ}(m)
 &\le
 \sum_{\#\mathrm{controlled}\ge2}w_{\mathbf j}
 \min_{\substack{u<v\\u,v\ \mathrm{controlled}}}
 \sqrt{\overline\eta_{u,j_u}\overline\eta_{v,j_v}}\\
 &\quad+
 (|A|-1)
 \Pr_w\{\#\mathrm{controlled\ slots}\le1\}.
\end{aligned}
 \tag{NC28}
\]
Both terms, and then the sum in (NC27), must be subexponential. The older
condition that every slot be controlled is sufficient but unnecessarily
strong. Generic A3 density does not imply (NC28): coordinate restriction can
split a flat full quotient into tiny multiplicity classes whose endpoint
energies equal \(|A|-1\).

## 4. Boundary cases and falsifiers

### Uniform recovery

If \(\mathcal S=\{d\}\), then \(D_*=d\), \(n_d=|Q|\), (NC8) is
\[
 E_{d,\chi}(Y)^d,
\]
and the symmetric quantity (NC19) is exactly PR #664 Theorem D. At \(d=2\),
the primary pairwise quantity is the same bound. At \(d>2\), (NC18) can be
strictly sharper, while PR #664 remains an immediate corollary of (NC22).

For example, take \(d=3\), \(A=\mathbb Z/2\mathbb Z\),
\(h(Q)=(0,0,1)\), and \(m=3\). Then
\[
 P_{\mathbf c}^{\circ}(3)=\frac17,
 \qquad
 K_{\mathbf c}^{\circ}(3)
 =\frac{6+54/3^{4/3}}{84}\approx0.220006.
\]

### The multiplicity-\((1,3)\) correction

For two quotient values with character values \(1\) and \(-1\), and live
fiber sizes \(1\) and \(3\), (NC8) gives
\[
 (1+Y)(1-Y)^3.
\]
The fake uniform-degree-two expression
\[
 ((1+Y)(1-Y))^2
\]
has different coefficients. The old example falsifies only the fake power;
it is an exact positive test of the multiplicity-class identity.

### All singletons

If \(\mathcal S=\{1\}\), then \(D_*=1\). The exact factorization (NC8)
still holds, but the pairwise theorem is false. Take
\(A=(\mathbb Z/2\mathbb Z)^2\), \(h(Q)=(0,1,2)\), and \(m=1\). Then
\(\eta_{1,1}=1/3\), whereas the three nontrivial character coefficients all
have absolute value one, so their normalized \(L^1\) sum is \(1\), not
\(1/3\). Cauchy gives only the separate fallback
\[
 \frac1{M_{1,m}}\sum_{\chi\in\mathfrak M}|e_{1,m}(\chi)|
 \le\sqrt{|\mathfrak M|\eta_{1,m}}.
\]
Theorem E deliberately excludes \(D_*=1\). A consumer may route an
all-singleton restriction elsewhere; it may not advertise folding leverage
from this compiler.

### Trivial target and endpoint weights

If \(A\) is trivial, the nontrivial character set is empty and both sides
of (NC21) vanish. At \(m=0\) or \(m=N\), the bound remains algebraically
valid and is an equality when all nontrivial characters are included:
every factor uses its endpoint energy \(|A|-1\).

### Phase constancy is load-bearing

The multiplicities in (NC2) describe fibers of a phase-factor map, not only
fibers of a geometric map. If two live points in one purported fiber have
character values \(1\) and \(-1\), their true local factor is
\[
 (1+Y)(1-Y)=1-Y^2,
\]
not \((1+Y)^2\). Such a fiber must be refined until (NC1) holds or routed
outside this theorem.

### Class separation and the common target are load-bearing

Energies cannot be pooled across multiplicity classes. In
\(A=(\mathbb Z/2\mathbb Z)^2\), take
\[
 Q_1=\{0,1\},\qquad Q_2=\{2,3\}.
\]
The pooled weight-one image is perfectly flat and has centered energy zero,
but the actual profile-\((1,2)\), weight-one normalized nontrivial loss is
\(1/3\). The separate class energies are therefore necessary.

Nor may each class be normalized in its own smaller target. With one
size-one fiber at \(1\) and one size-two fiber at \(2\) in the same group
\((\mathbb Z/2\mathbb Z)^2\), local order-two endpoint energies would print
a bound of one, while the true common-target normalized loss is \(5/3\).
The common-\(A\) endpoint energies are three and give the honest bound.

### PO3 markers remain load-bearing

The strict-improvement example above is also a finite marker falsifier. For
uniform \(d=3\), \(A=\mathbb Z/2\mathbb Z\), \(h(Q)=(0,0,1)\), and total
weight three, the unmarked pairwise compiler is \(1/7\). The PO3 component
that selects exactly one full fiber has three supports and normalized
nontrivial loss \(1/3\). Applying the unmarked theorem after erasing the
occupancy markers would therefore be false.

## 5. Consumer-backward hypothesis audit

| Required input | Supplied status |
|---|---|
| one live map and the translated projected phase (NC1a) constant on each actual surviving fiber | must be supplied by the designated quotient-major chart; geometric fibers alone do not suffice |
| actual nonempty multiplicities \(c_y\) after coordinate-level restriction | finite live-set data; no original uniform degree is substituted |
| \(D_*=\sum_{s:n_s>0}s\ge2\) | checkable from the actual profile; all singletons have no folding leverage |
| one common effective target \(A\) for every class and weight | supplied only by a fixed quotient target such as \(A_\phi\); classwise renormalization is forbidden |
| exclusion of the trivial character | load-bearing in centered Parseval and explicit in (NC21) |
| full coordinate-live fixed-weight slice \(\binom Tm\) | (NC8) includes every fiber occupancy with its binomial multiplicity |
| support-level first-match deletion inside \(\binom Tm\) | not supplied; Fourier \(L^1\) is not monotone under removing supports |
| a fixed-statistic PO3 subprofile | not supplied; occupancy markers remain necessary |
| classwise centered energies \(\eta_{s,j}\) | OPEN; this packet compiles them but proves no analytic bound |
| subexponential assigned sum (NC27) and pairwise tail (NC28) | absent from generic A3/A4 density; must be proved uniformly |
| assignment against other quotient scales and non-quotient cells | not supplied |

Theorem E handles coordinate-level restriction of original fibers by using
their actual surviving sizes, provided the object is still the full
\(\binom Tm\) slice. It does not handle a branch point or exceptional live
point on which the phase fails to factor. Nor can it be inserted after a
support-level first-match deletion: cancellations in a Fourier coefficient
can disappear when supports are removed, so the isolated \(L^1\) payment is
not monotone. Such a residual needs its own marked bound, or a completed
full-slice max-fiber statement transferred through a separately proved
residual monotonicity principle.

A fixed total weight \(m\) is already selected by \([Y^m]\). In contrast,
a PO3 subprofile that fixes how many fibers have particular partial
occupancies requires the manuscript's additional marker variables. Erasing
those markers before taking the subprofile is not justified by (NC8), and
the explicit \(1/3>1/7\) example above shows that it can be false.

Finally, a flat full quotient does not make its multiplicity classes flat.
Coordinate restriction can partition \(Q=A\) into tiny classes: full
weight-one energy is then perfect while each singleton class has endpoint
energy \(|A|-1\). Thus PR #564's full-row energy, even if proved, would not
silently supply the classwise inputs here.

## 6. Prior work and exact new delta

- The manuscript's PO3 generating function and commit 75e5e32 already
  contain binomially weighted repeated-column occupancies. The algebraic
  product shape is prior work. The new result is the common-target centered
  \(L^1\) compiler for the actual multiplicity profile.
- PR #656 proves the valid uncentered compiler for one exact uniform class.
  PR #664 centers it and prints the multiplicity-\((1,3)\) falsifier. This
  packet converts that falsifier into the corrected general theorem,
  recovers the symmetric predecessor as a corollary, and adds the strictly
  sharper pairwise compiler.
- PR #564 owns the subgroup-VMVT/Poisson centered-energy frontier. Theorem E
  neither proves nor reclaims any classwise energy estimate.
- PR #662 concerns the B2 Hankel/CHG rank-window route. PRs #661 and #663
  concern the exponential inverse-LO/Bohr-to-GAP route. The current theorem
  uses none of those inputs and changes none of their claims.

## 7. Promotion-safe conclusion and nonclaims

A maintainer may safely record this implication:

> A full coordinate-live fixed-weight quotient-major band with arbitrary
> nonempty fiber sizes obeys (NC21), provided the translated projected phase
> is constant on each actual fiber, all multiplicity-class energies use one
> common target, and \(D_*\ge2\).

It is actually MA-paid only after the assigned sum (NC27), including the
pairwise class-tail requirement (NC28), is proved subexponential.

This packet does **not** prove phase factorization for a generic A4 leaf,
classwise collision energies, Q/FI, sparse-major counting, support-deleted
first-match residuals, a primitive-Q or minor/Sidon payment, a
fixed-statistic PO3 profile, cross-scale or first-match overlap assignment,
RC, full A4, a deployed row, or the Grand MCA theorem. It changes no paper
TeX. Any later promotion remains separately gated on a fresh audit that the
TeX consumer supplies (NC1)--(NC3), (NC27)--(NC28), the common-target and
full-slice hypotheses, and every other displayed input.

## 8. Verification scope

The verifier checks exact classwise subset-sum counts, centered Parseval,
endpoint energies, the full coefficient identity, probability weights,
pairwise Cauchy and powered \(D_*\)-Hölder component inequalities, the
aggregate comparison chain, uniform recovery and strict improvement, the
multiplicity-\((1,3)\) repair, phase-constancy, class-pooling, local-target,
PO3-marker, all-singleton, trivial-target, and endpoint falsifiers or
boundaries, pinned parent sources, and semantic mutations of the common
target, trivial-character exclusion, translation, coordinate/full-slice,
support-deletion, PO3-marker, payment/tail, OPEN-energy, overlap, nonclosure,
and no-TeX guards. The general proof is the derivation in Sections 2 and 3.
