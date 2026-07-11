# A4 quotient-major bridge: weighted MDS count and uniform-fold energy compiler

**Status:** two finite theorems are PROVED. Their application to the full A4
major aggregate is CONDITIONAL on the consumer hypotheses isolated below.
This packet changes no TeX file and claims no deployed threshold.

**Base:** integrated commit 5c9aab794e6575d815541e0a5dd8534d03d400aa.
The packet was designed consumer-backward from (A4), (A5), def:major-arc,
(MA), (EF7), and (PO3) in
experimental/asymptotic_rs_mca_frontiers.tex.

**Replay:**

    python3 experimental/scripts/verify_a4_quotient_major_compiler.py --write
    python3 experimental/scripts/verify_a4_quotient_major_compiler.py --check
    python3 experimental/scripts/verify_a4_quotient_major_compiler.py --tamper-selftest

The verifier is standard-library-only, imposes a 1 GiB address-space cap,
checks exact prime-field examples and finite group-ring identities, and
writes experimental/data/certificates/a4-quotient-major-compiler/
a4_quotient_major_compiler.json.

## 1. Result map

This packet separates two objects which must not be conflated.

1. **Algebraic quotient-phase count.** Weighted Vandermonde phase words which
   are literally constant in the base field on exact degree-\(d\) fibers form
   a code of dimension at most \(\lceil k/d\rceil\). This pays a
   growing-degree algebraic-major tail when its exact entropy condition holds.
2. **Effective quotient-character compiler.** All effective characters whose
   character values are constant on the same fibers are the dual of a finite
   quotient \(A_\phi\). On an exact uniform fold of every degree \(d\ge2\),
   their fixed-weight Fourier aggregate is bounded by a convex hypergeometric
   average of quotient-slice collision energies.

Over a prime base field the two notions of constancy coincide. Over a proper
extension they need not: literal equality of phase values is stronger than
equality after applying a trace character. The first theorem therefore does
not silently count the whole effective factor-through group in extension
fields. The second theorem is formulated directly on that effective group and
does cover it, but requires intermediate collision-energy inputs not supplied
by (A4) or (A5).

## 2. Weighted quotient-phase count

Let \(\mathbb B\) be a finite field, let \(T\subseteq\mathbb B\) contain
\(N\) distinct points, and let \(\rho:T\to\mathbb B^\times\). For
\(R\ge1\), put

\[
 C_R=\left\{
   \bigl(\rho(t)P(t)\bigr)_{t\in T}:\deg P<R
 \right\}\subseteq\mathbb B^T,\qquad k=\min(R,N).
 \tag{QM1}
\]

This is a generalized Reed--Solomon code of parameters
\([N,k,N-k+1]\). Let \(\phi:T\twoheadrightarrow Q\) be exactly
\(d\)-to-one, so \(\lvert Q\rvert=N/d\), and define

\[
 C_R^\phi=
 \{c\in C_R:c_t=c_u\text{ whenever }\phi(t)=\phi(u)\}.
 \tag{QM2}
\]

### Theorem A (weighted quotient-phase dimension)

\[
 \boxed{\dim_{\mathbb B} C_R^\phi
 \le \left\lfloor\frac{k-1}{d}\right\rfloor+1
 =\left\lceil\frac{k}{d}\right\rceil.}
 \tag{QM3}
\]

Consequently there are at most
\(\lvert\mathbb B\rvert^{\lceil k/d\rceil}\) distinct
\(\mathbb B\)-valued weighted phases in this quotient-factor locus.

### Proof

Every word in \(C_R^\phi\) descends uniquely to a word of length \(N/d\)
on \(Q\). If a nonzero descended word has \(z\) zero coordinates, its lift
has \(dz\) zero coordinates on \(T\). The MDS distance of \(C_R\) says that
a nonzero lifted word has at most \(k-1\) zeros. Hence

\[
 z\le\left\lfloor\frac{k-1}{d}\right\rfloor.
\]

The descended code therefore has minimum distance at least

\[
 \frac Nd-\left\lfloor\frac{k-1}{d}\right\rfloor.
\]

Singleton on the descended length-\(N/d\) code gives (QM3).

The proof uses exactly three inputs: distinct evaluation points, nonzero
common weights, and exact uniform fibers. It does **not** require the common
weight to factor through \(\phi\), nor \(R<\operatorname{char}\mathbb B\).
The latter restriction in (A5) belongs to the Newton/power-sum coordinate
change, not to this MDS argument.

### The floor count is false for general (A5) weights

Take \(T=\mathbb F_{17}^{\times}\),
\(\phi(t)=t^2\), \(R=3\), and \(\rho(t)=t^2\). The phase space is

\[
 a_0t^2+a_1t^3+a_2t^4.
\]

It is constant on every pair \(\{t,-t\}\) exactly when \(a_1=0\).
The functions \(t^2\) and \(t^4\) are distinct on this domain, so the factor
subspace has dimension two, while
\(\lfloor R/2\rfloor=1\). The ceiling bound is tight. The familiar floor
is correct in the special power-sum convention
\((t,t^2,\ldots,t^R)\) on a cyclic coset with \(R\le|T|\), where no
evaluation aliasing occurs and only indices divisible by \(d\) survive.
It is not the general weighted-Vandermonde theorem.

### Growing-degree sparse-major corollary

Let \(\mathcal I_N\) be a certified family of exact quotient maps with
degrees \(d_\phi\ge D_N\). Suppose every effective character in the
designated **algebraic quotient-major band** has an ambient lift whose
\(\mathbb B\)-valued weighted phase lies in one of the corresponding
\(C_R^\phi\); all remaining designated majors must be paid separately.
Then

\[
 \left|\bigcup_{\phi\in\mathcal I_N}
 \mathfrak M_{\phi}^{\rm alg}\right|
 \le |\mathcal I_N|\,|\mathbb B|^{\lceil k/D_N\rceil}.
 \tag{QM4}
\]

Therefore the sparse-major lemma proves (MA) for this band provided the
following estimate holds uniformly over the designated live leaves, maps, and
received-line data:

\[
 \log|\mathcal I_N|
 +\left\lceil\frac{k}{D_N}\right\rceil\log|\mathbb B|
 =o(N).
 \tag{QM5}
\]

A convenient sufficient package is

\[
 \log|\mathcal I_N|=o(N),\quad
 k\log|\mathbb B|=O(N),\quad
 \log|\mathbb B|=o(N),\quad D_N\to\infty.
 \tag{QM6}
\]

For a cyclic divisor tower, \(|\mathcal I_N|\le\tau(N)\); a dyadic
Chebyshev tower has only logarithmically many scales. Fixed \(d\) is not
paid by counting: PR #465 correctly finds an exponentially large
fixed-degree family.

## 3. Trace-field and effective-lift audit

The TeX first defines the ambient \(\mathbb B\)-valued phase
\(R_\alpha(t)=\alpha\cdot g(t)\), then uses algebraic phase factorization
only to construct a certified effective major/minor partition.
def:major-arc calls such a weighted phase exceptional when it is constant
on a routed quotient fiber or factors through a quotient, and the next
proposition explicitly says this classification does not prove (MA).
Theorem A treats only the global factor-through sublocus: the phase must be
constant on **every** fiber of one exact map. It does not pay the entire
exceptional locus merely because a phase is constant on one routed fiber.

Theorem A counts this literal algebraic locus. It transfers to distinct
effective restrictions without cost: restriction can merge ambient lifts,
not create more characters. One must not instead count all ambient lifts
with their annihilator multiplicity; (EF2) cancels that multiplicity against
the ambient Fourier denominator.

If \(\mathbb B=\mathbb F_p\), a nontrivial additive character is faithful,
so

\[
 \chi(g(t))=\chi(g(u))
 \quad\Longleftrightarrow\quad
 \alpha\cdot(g(t)-g(u))=0.
\]

For a proper extension \(\mathbb B/\mathbb F_p\), the left side gives only

\[
 \operatorname{Tr}_{\mathbb B/\mathbb F_p}
 \bigl(\alpha\cdot(g(t)-g(u))\bigr)=0.
 \tag{TR}
\]

Trace-only quotient characters need not have a lift in \(C_R^\phi\).
Theorem A does not count them unless the row supplies the certified-lift
containment in (QM4). This is consistent with the TeX's Artin--Schreier
discussion: a nonconstant \(\mathbb B\)-valued phase can have constant trace.

## 4. The full effective factor-through group

Now forget the weighted-Vandermonde presentation. Let \(V\) be the finite
effective additive target of one full fixed-weight leaf, let \(g:T\to V\)
be its translated boundary map, and let
\(\phi:T\twoheadrightarrow Q\) be exactly \(d\)-to-one. Put

\[
 W_\phi=\left\langle
 g(t)-g(u):\phi(t)=\phi(u)
 \right\rangle,\qquad A_\phi=V/W_\phi.
 \tag{UF1}
\]

The brackets mean additive-group span (in the manuscript, the
\(\mathbb F_p\)-span). The projected map defines \(h_\phi:Q\to A_\phi\),
and

\[
 \widehat{A_\phi}
 =\{\chi\in\widehat V:\chi(g(t))=\chi(g(u))
      \text{ on every }\phi\text{-fiber}\}.
 \tag{UF2}
\]

Thus \(A_\phi\) is the correct common target for the entire effective
factor-through character band, including trace-only modes. No MDS estimate
for \(|A_\phi|\) is asserted.

Write \(n=|Q|\). For \(0\le j\le n\), define

\[
 r_j(a)=
 \left|\left\{J\in\binom Qj:
       \sum_{y\in J}h_\phi(y)=a\right\}\right|,
 \quad M_j=\binom nj,\quad
 \mathrm{SP}_j=\sum_{a\in A_\phi}r_j(a)^2,
 \tag{UF3}
\]

and use the **same target \(A_\phi\) at every weight**:

\[
 \kappa_j=
 \frac{|A_\phi|\mathrm{SP}_j}{M_j^2}.
 \tag{UF4}
\]

Then

\[
 1\le\kappa_j\le|A_\phi|,
 \qquad \kappa_0=\kappa_n=|A_\phi|.
 \tag{UF5}
\]

The endpoint identity is a guard against a tempting normalization error:
the zero- and full-subset maps have trivial individual difference spans,
but their energies in the common target are \(|A_\phi|\), not one.

## 5. Exact all-degree uniform-fold compiler

For \(0\le m\le dn\), let

\[
 \mathcal J_{d,n,m}=
 \{(j_1,\ldots,j_d):0\le j_s\le n,\ \sum_sj_s=m\},
 \tag{UF6}
\]

\[
 w_{\mathbf j}=
 \frac{\prod_{s=1}^dM_{j_s}}{\binom{dn}{m}},
 \qquad
 K_d(m)=
 \sum_{\mathbf j\in\mathcal J_{d,n,m}}
 w_{\mathbf j}\prod_{s=1}^d\kappa_{j_s}^{1/d}.
 \tag{UF7}
\]

The weights are a probability distribution by coefficient extraction from
\((1+Y)^{dn}\):

\[
 \sum_{\mathbf j}w_{\mathbf j}=1.
 \tag{UF8}
\]

### Theorem B (uniform-fold collision-energy compiler)

For every
\(\mathfrak M\subseteq\widehat{A_\phi}\setminus\{1\}\),

\[
 \boxed{
 \frac1{\binom{dn}{m}}
 \sum_{\chi\in\mathfrak M}
 \left|e_m\bigl(\chi(g(t)):t\in T\bigr)\right|
 \le K_d(m)-1.}
 \tag{UF9}
\]

In particular, \(K_d(m)=e^{o(|T|)}\), uniformly over the designated live
leaves, exact maps, and received-line data, pays the effective major aggregate
for this band.

### Proof

For \(\chi\in\widehat{A_\phi}\), put

\[
 e_j(\chi)=
 \sum_{J\in\binom Qj}
 \chi\left(\sum_{y\in J}h_\phi(y)\right).
\]

Exact \(d\)-fold fibers give

\[
 e_m\bigl(\chi(g(t)):t\in T\bigr)
 =
 [Y^m]\left(\sum_{j=0}^ne_j(\chi)Y^j\right)^d
 =
 \sum_{\mathbf j\in\mathcal J_{d,n,m}}
 \prod_{s=1}^de_{j_s}(\chi).
 \tag{UF10}
\]

Parseval on the one common target gives

\[
 \sum_{\chi\in\widehat{A_\phi}}|e_j(\chi)|^2
 =|A_\phi|\mathrm{SP}_j
 =\kappa_jM_j^2.
 \tag{UF11}
\]

For \(d\ge2\), the trivial bound \(|e_j(\chi)|\le M_j\) implies

\[
 \sum_\chi|e_j(\chi)|^d
 \le M_j^{d-2}\sum_\chi|e_j(\chi)|^2
 =\kappa_jM_j^d.
 \tag{UF12}
\]

Triangle inequality followed by Hölder with \(d\) factors yields

\[
 \sum_\chi
 \left|e_m\bigl(\chi(g(t)):t\in T\bigr)\right|
 \le
 \sum_{\mathbf j}
 \prod_sM_{j_s}\kappa_{j_s}^{1/d}
 =\binom{dn}{m}K_d(m).
 \tag{UF13}
\]

The trivial character contributes exactly \(\binom{dn}{m}\).
Subtract it and use nonnegativity to obtain (UF9). For \(d=2\), this is
the Parseval/Cauchy--Schwarz square-root formula. For \(d>2\), genuine
\(d\)-th moments could sharpen (UF12), but they are not required for this
valid pair-energy fallback.

## 6. What supplies the intermediate energies

Let \(L_j=|\operatorname{supp}r_j|\), and suppose

\[
 \max_a r_j(a)\le Q_j\frac{M_j}{L_j}.
\]

Then

\[
 \kappa_j\le Q_j\frac{|A_\phi|}{L_j}.
 \tag{UF14}
\]

Thus image-normalized Q plus FI pays \(\kappa_j\) only when both factors
are proved in the **same common target**. Image-Q alone does not suffice:
at \(j=0\), Q is perfect but \(\kappa_0=|A_\phi|\).

If the energies are controlled only on a central set
\(C\subseteq\{0,\ldots,n\}\), the hypergeometric tail must be compared
with target entropy. Since every \(\kappa_j\le|A_\phi|\), a sufficient
finite condition is

\[
 |A_\phi|
 \sum_{\mathbf j:\,\exists s,\ j_s\notin C}w_{\mathbf j}
 =e^{o(|T|)}.
 \tag{UF15}
\]

Saying only that the tail is exponentially small is insufficient when
\(|A_\phi|\) is itself exponential.

## 7. Consumer-backward hypothesis audit

| Required input | What the TeX or deployed chart supplies |
|---|---|
| distinct points and nonzero common weights for Theorem A | (A5) supplies this weighted GRS structure |
| exact uniform fibers on the **live active set** | smooth/circle geometry supplies exact maps on the full domain; generic (A4) leaves may have prior deletions |
| algebraic-major certified-lift containment in (QM4) | def:major-arc classifies such lifts but does not prove exhaustion or (MA) |
| \(k\log|\mathbb B|=O(N)\) | absent generically; follows from **ambient** FI \(L\ge e^{-o(N)}|\mathbb B|^R\) plus fixed density (since \(k\le R\)), not from quotient/effective FI alone |
| common effective target \(A_\phi\) | supplied by (UF1), not by re-normalizing each weight separately |
| intermediate \(\kappa_j\), Q+FI, or a tail inequality | absent from (A4)--(A5); this is the remaining analytic input |
| exact complete fibers of the map on the live active set for (UF10) | full KB power-map and M31 Chebyshev identity charts supply them; an incomplete live fiber or a fixed-statistic PO3 subprofile needs separate markers |

The cyclic power maps are exact on multiplicative cosets. Chebyshev maps are
exact under the twin-coset separation hypothesis, with bounded branch
exceptions placed in a separate profile. The deployed KB full identity chart
has exact \(2^j\)-fold power maps; the deployed M31 full identity chart has
exact Chebyshev \(T_{2^j}\) maps. Neither currently supplies (UF14) at every
intermediate weight, so Theorem B is a genuine reduction, not closure.

An arbitrary planted deletion can break uniform fibers. A consumer must
either prove the active set is a union of complete fibers or split incomplete
fibers into a separately paid exceptional/partial-occupancy profile.
Within a complete live \(d\)-fiber, the full-slice factor
\((1+Y\chi(h_\phi(y)))^d\) already includes selections of every occupancy
\(0,\ldots,d\) with their binomial multiplicities. What UF10 does not encode
is a canonical PO3 sub-slice with fixed partial-occupancy statistics; those
extra statistics require the PO3 marker variables.

## 8. Prior work and the exact new delta

- The TeX's (PO3) gives the exact partial-occupancy generating function, and
  commit 75e5e32 records the binomially weighted multilevel quotient alphabet.
  Thus repeated-column powers and coefficient convolution are prior work, not
  claimed here. Neither source supplies the aggregate \(L^1\) inequality
  (UF9).
- PR #465 identifies pure \(\mu_d\)-invariant major phases and the
  \(p^{w/d}\) fixed-degree count. Theorem A adds the arbitrary-common-weight
  ceiling count, its tight floor falsifier, and the growing-tail condition.
- (EF7) records actual finite Fourier losses but does not compile them across
  a uniform quotient. Theorem B supplies that payment inequality.
- The minimal-phase-supplement packet already records the collision/Parseval
  identity. The new delta is its common-target, all-\(d\), fixed-weight
  convex-allocation consequence, not Parseval itself.
- PR #643's PTE tensor champion is a no-carry direct product of independent
  block-signature systems on an arbitrary integer/prime-field domain. It does
  not exhibit a
  smooth/circle live active set with one exact uniform fold and supplies none
  of the compiler hypotheses. It is a negative applicability stress test only;
  #646's later \(\phi^*=\log 2\) result also supersedes #643's conjectural
  asymptotic constant.
- PR #651 names the image-normalized low-energy/Sidon (A4) payment as the
  remaining wall. This packet attacks its quotient-major side only.

## 9. Promotion-safe conclusion and nonclaims

A maintainer may safely use the following two ledger entries after reviewing
this packet:

1. growing-degree **algebraic** quotient majors are sparse under
   (QM4)--(QM5), uniformly over the designated live leaves and received lines;
2. an exact uniform-fold effective quotient band is MA-paid whenever the
   common-target quantity \(K_d(m)\) in (UF7) is uniformly subexponential over
   the designated live leaves, maps, and received lines.

The packet does **not** prove that every generic primitive active set is
fiber-saturated, that the algebraic locus exhausts extension-field trace
majors, that the intermediate energies or FI/Q inputs hold, that different
quotient scales have been assigned without overlap, that incomplete live
fibers or fixed-statistic PO3 subprofiles obey the unmarked power identity,
or that full A4, primitive Q, RC, a deployed safe
row, or the Grand MCA theorem is closed. It imports no inverse
Littlewood--Offord theorem and changes no paper TeX.

## 10. Verification scope

The verifier checks exact modular ranks of weighted-GRS fiber constraints,
the tight floor counterexample, descended distances and Singleton ceilings,
group-ring convolution for \(d=2,3,4\), Parseval collision identities,
endpoint energies, Hölder component bounds, multivariate Vandermonde weights,
the common-target Q+FI inequality, pinned sources, and semantic tampers for
the global-every-fiber, certified-lift, ambient-entropy, uniformity, exact sparse-tail,
trace, common-target, complete-live-fiber, PO3-subprofile, overlap, and
nonclosure hypotheses. The mathematical proofs are the derivations in
Sections 2 and 5.
