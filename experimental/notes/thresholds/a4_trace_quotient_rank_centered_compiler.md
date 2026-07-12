# A4 successor: trace quotient rank and the centered uniform-fold compiler

**Status:** two finite theorems are PROVED. The first counts the complete
character-value factor-through band, including extension-field trace-only
modes. The second removes the trivial character before the all-degree
Hölder compiler. The displayed KoalaBear and M31 constants are stable
finite computations of a CONDITIONAL energy target; the required centered
energy theorem is OPEN. This packet changes no TeX and claims no deployed
threshold.

**Base and lineage:** this is a successor to the now-integrated PR #656
packet, originally commit
\(6a1e520871dd23ab8a536f4dcd423820990feef1\), on integrated base
\(36de5bfcc7d6e0ca44806112acec2f4a1b4a7532\). It preserves the parent
theorems and fills two deliberately exposed interfaces in
experimental/notes/thresholds/a4_quotient_major_compiler.md.

**Replay:**

    python3 experimental/scripts/verify_a4_trace_quotient_rank_centered_compiler.py --write
    python3 experimental/scripts/verify_a4_trace_quotient_rank_centered_compiler.py --check
    python3 experimental/scripts/verify_a4_trace_quotient_rank_centered_compiler.py --tamper-selftest

The verifier is standard-library-only, imposes a 1 GiB address-space cap,
checks exact finite-field ranks and exact elementary-two-group coefficient
identities, and writes
experimental/data/certificates/a4-trace-quotient-rank-centered/
a4_trace_quotient_rank_centered_compiler.json.

## 1. Result map

This packet adds two compatible but logically separate tools.

1. **Full trace quotient count.** If a boundary map is projected through
   one partition with \(q\) nonempty fibers, all effective characters whose
   character values are constant on every fiber form a group of exact order
   \(p^{v-w_\phi}\), and
   \[
      p^{v-w_\phi}\le p^{q-1}.
   \]
   For an exact \(d\)-fold partition this is at most
   \(p^{N/d-1}\). Unlike PR #656 Theorem A, this counts trace-only modes and
   needs no algebraic lift. It pays certified growing-fold tails when their
   exact characteristic/map entropy is sublinear.
2. **Centered effective compiler.** In the common target \(A_\phi\), put
   \(\eta_j=\kappa_j-1\). Centered Parseval over the nontrivial effective
   characters replaces PR #656's \(K_d-1\) by
   \[
      K_d^\circ(m)
      =\sum_{\mathbf j}w_{\mathbf j}
        \prod_{s=1}^d\eta_{j_s}^{1/d}.
   \]
   This is never larger than \(K_d-1\), and can be smaller. It still
   requires actual centered collision-energy information.

The first tool removes a high-degree extension trace tail under a checkable
entropy condition. The second makes the fixed-degree energy interface
quantitatively sharper. Neither proves the fixed-degree energies.

## 2. Effective trace constraints

Let \(\mathbb B=\mathbb F_{p^s}\), let \(T\ne\varnothing\), and let
\(g:T\to\mathbb B^R\). Fix \(t_0\in T\), and define the manuscript's
effective fixed-weight difference span
\[
 V=\operatorname{span}_{\mathbb F_p}
   \{g(t)-g(t_0):t\in T\}\subseteq\mathbb B^R.
 \tag{TR1}
\]
Let \(\phi:T\twoheadrightarrow Q\) be any surjection, not necessarily
uniform, and put
\[
 W_\phi=\operatorname{span}_{\mathbb F_p}
 \{g(t)-g(u):\phi(t)=\phi(u)\},
 \qquad A_\phi=V/W_\phi.
 \tag{TR2}
\]
Write
\[
 v=\dim_{\mathbb F_p}V,\qquad
 w_\phi=\dim_{\mathbb F_p}W_\phi,\qquad q=|Q|.
\]
The inclusion \(W_\phi\subseteq V\) follows by subtracting both points from
\(t_0\).

Choose a nontrivial additive character
\(\psi:\mathbb F_p\to\mathbb C^\times\). Every ambient additive character
has a unique parameter \(\alpha\in\mathbb B^R\):
\[
 \chi_\alpha(x)
 =\psi\!\left(
   \operatorname{Tr}_{\mathbb B/\mathbb F_p}(\alpha\cdot x)
 \right).
 \tag{TR3}
\]
The trace pairing is nondegenerate for every finite-field extension,
including characteristic two and the case \(p\mid s\).

### Theorem C (exact trace quotient rank)

The ambient parameters whose character values are constant on every
\(\phi\)-fiber are exactly
\[
 Z_\phi=W_\phi^\perp,
 \qquad
 \dim_{\mathbb F_p}Z_\phi=sR-w_\phi.
 \tag{TR4}
\]
Restriction to the effective group fits into the exact sequence
\[
 0\longrightarrow V^\perp
 \longrightarrow W_\phi^\perp
 \longrightarrow \widehat{A_\phi}
 \longrightarrow0.
 \tag{TR5}
\]
Consequently the exact number of distinct effective factor-through
characters is
\[
 \boxed{
 |\widehat{A_\phi}|=|A_\phi|=p^{v-w_\phi}\le p^{q-1}.}
 \tag{TR6}
\]

### Proof

For points in one fiber,
\[
 \chi_\alpha(g(t))=\chi_\alpha(g(u))
 \iff
 \operatorname{Tr}_{\mathbb B/\mathbb F_p}
 \bigl(\alpha\cdot(g(t)-g(u))\bigr)=0,
\]
because a nontrivial character of the additive group \(\mathbb F_p\) is
faithful. Thus the ambient solution space is \(W_\phi^\perp\), proving
(TR4).

Since \(W_\phi\subseteq V\), the kernel of restriction from
\(W_\phi^\perp\) to \(\widehat V\) is \(V^\perp\). Its image is precisely
the characters of \(V\) annihilating \(W_\phi\), namely
\(\widehat{V/W_\phi}=\widehat{A_\phi}\). Nondegeneracy of the trace pairing
gives surjectivity and the displayed dimensions, so the image dimension is
\[
 (sR-w_\phi)-(sR-v)=v-w_\phi.
\]

For the universal upper bound, choose one representative \(t_y\) in every
fiber and choose \(y_0=\phi(t_0)\). Modulo \(W_\phi\), every generator
\(g(t)-g(t_0)\) equals
\[
 g(t_{\phi(t)})-g(t_{y_0}).
\]
Only the \(q-1\) representatives with \(y\ne y_0\) are needed. Therefore
\(\dim_{\mathbb F_p}A_\phi\le q-1\), proving (TR6).

The cancellation in (TR5) is load-bearing. The ambient parameter count is
\(p^{sR-w_\phi}\), but every effective character has
\(p^{sR-v}\) ambient lifts. Counting the ambient parameters as distinct
effective characters would reintroduce exactly the annihilator multiplicity
removed by (EF2) in the TeX.

### Exact folds and nonuniform live sets

If \(\phi\) is exactly \(d\)-to-one on the live active set and
\(|T|=N\), then \(q=N/d\) and
\[
 |\widehat{A_\phi}|\le p^{N/d-1}.
 \tag{TR7}
\]
Uniformity is not needed for Theorem C itself. On a nonuniform live
restriction one must use the actual number \(q\) of nonempty fibers. If only
one \(r\)-point block is collapsed and all other points are singletons, then
\(q=N-r+1\), so (TR6) gives only \(p^{N-r}\). A deletion that breaks most
fibers can therefore erase the useful degree gain.

The theorem concerns global constancy on every block of the named
partition. Constancy on one routed fiber corresponds to a partition with
many singleton blocks and is not the same band.

### Sharpness

The exponent \(q-1\) is universally sharp even for legal
large-characteristic weighted Vandermonde columns. Choose a prime
\(p>N\), take \(R=N<p\), choose \(N\) distinct points, and let
\[
 g(t)=\rho(t)(1,t,\ldots,t^{R-1}),
 \qquad \rho(t)\ne0.
 \tag{TR8}
\]
The \(N\) columns are linearly independent over \(\mathbb F_p\). Hence the
\(N-1\) differences from \(t_0\) are independent, so \(v=N-1\).
For any partition into \(q\) nonempty blocks, the differences from each
nonrepresentative point to its block representative are \(N-q\) independent
vectors. Thus \(w_\phi=N-q\) and
\[
 \dim_{\mathbb F_p}A_\phi=q-1.
 \tag{TR9}
\]
In particular fixed \(d\) can leave \(p^{N/d-1}\) effective factor modes.
The fixed-degree energy compiler remains necessary.

Over a prime field, literal phase constancy and character-value constancy
coincide, so PR #656 Theorem A and (TR6) may both be used:
\[
 |\widehat{A_\phi}|
 \le
 \min\left(
   p^{\lceil k/d\rceil},
   p^{N/d-1}
 \right)
 \tag{TR10}
\]
for an exact \(d\)-fold weighted-GRS row. Over a proper extension,
Theorem A still counts its literal algebraic-lift band, while Theorem C
counts the whole effective character-value factor group. No containment of
the latter in the former is asserted.

## 3. Growing-fold trace-tail payment

Let \(\mathcal I_N\) be a certified family of exact maps on the live active
set, with degrees \(d_\phi\ge D_N\). Theorem C and a union bound give
\[
 \left|
 \bigcup_{\phi\in\mathcal I_N}
 \bigl(\widehat{A_\phi}\setminus\{1\}\bigr)
 \right|
 \le
 \sum_{\phi\in\mathcal I_N}
 \left(p_N^{N/d_\phi-1}-1\right)
 \le
 |\mathcal I_N|p_N^{N/D_N-1}.
 \tag{TR11}
\]
Overlap between maps only reduces the union, so no first-match assignment is
needed for this cardinality upper bound. An overlap assignment is still
needed if the same characters are charged again by other ledger cells.

The sparse-major lemma pays this complete character-value factor band when
\[
 \boxed{
 \log|\mathcal I_N|
 +\frac{N}{D_N}\log p_N=o(N)}
 \tag{TR12}
\]
uniformly over the designated live leaves, maps, and received lines. A
convenient sufficient package is
\[
 \log|\mathcal I_N|=o(N),
 \qquad \log p_N=o(D_N).
 \tag{TR13}
\]
Thus every growing-degree tail is paid in fixed characteristic, and for
polynomial characteristic it suffices that \(D_N/\log N\to\infty\).
The extension degree \(s=[\mathbb B:\mathbb F_p]\) does not enter.

Generic (A1)--(A7) does not assert (TR12). It also does not assert that a
post-deletion active set retains exact folds. Cyclic divisor towers and
dyadic Chebyshev towers have subexponential map-family entropy on their full
domains, but their named square/cubic folds have fixed degree and are not
paid by (TR12).

## 4. Centering the uniform-fold compiler

Return to PR #656's common finite target \(A=A_\phi\). Let
\(h:Q\to A\), \(|Q|=n\), and, for \(0\le j\le n\), put
\[
 M_j=\binom nj,\qquad
 r_j(a)=
 \left|
 \left\{J\in\binom Qj:
       \sum_{y\in J}h(y)=a\right\}
 \right|,
 \qquad
 \mathrm{SP}_j=\sum_{a\in A}r_j(a)^2.
 \tag{CE1}
\]
Use the same target \(A\) at every weight and define
\[
 \kappa_j=\frac{|A|\mathrm{SP}_j}{M_j^2},
 \qquad
 \eta_j=\kappa_j-1.
 \tag{CE2}
\]
The centered form is
\[
 \eta_j
 =\frac{|A|}{M_j^2}
 \sum_{a\in A}
 \left(r_j(a)-\frac{M_j}{|A|}\right)^2.
 \tag{CE3}
\]
Therefore
\[
 0\le\eta_j\le |A|-1,
 \qquad
 \eta_0=\eta_n=|A|-1.
 \tag{CE4}
\]
The endpoint value is not zero: each endpoint has one subset and one image
point in the common target.

For \(\chi\in\widehat A\), write
\[
 e_j(\chi)=
 \sum_{J\in\binom Qj}
 \chi\!\left(\sum_{y\in J}h(y)\right).
\]
Parseval with the trivial character removed is exactly
\[
 \sum_{\chi\ne1}|e_j(\chi)|^2
 =|A|\mathrm{SP}_j-M_j^2
 =\eta_jM_j^2.
 \tag{CE5}
\]

For \(d\ge2\) and \(0\le m\le dn\), let
\[
 \mathcal J_{d,n,m}
 =\{(j_1,\ldots,j_d):0\le j_s\le n,\ \sum_sj_s=m\},
\]
\[
 w_{\mathbf j}
 =\frac{\prod_sM_{j_s}}{\binom{dn}{m}},
 \qquad
 K_d^\circ(m)
 =\sum_{\mathbf j\in\mathcal J_{d,n,m}}
 w_{\mathbf j}\prod_{s=1}^d\eta_{j_s}^{1/d}.
 \tag{CE6}
\]
We use \(0^{1/d}=0\). The weights sum to one by multivariate
Vandermonde.

### Theorem D (centered uniform-fold compiler)

Assume the live map \(T\to Q\) is exactly \(d\)-to-one. For every
\(\mathfrak M\subseteq\widehat A\setminus\{1\}\),
\[
 \boxed{
 \frac1{\binom{dn}{m}}
 \sum_{\chi\in\mathfrak M}
 \left|
 e_m\bigl(\chi(g(t)):t\in T\bigr)
 \right|
 \le K_d^\circ(m).}
 \tag{CE7}
\]
Moreover,
\[
 K_d^\circ(m)\le K_d(m)-1,
 \tag{CE8}
\]
where \(K_d\) is PR #656's uncentered quantity.

### Proof

Exact \(d\)-fold fibers give the coefficient identity
\[
 e_m\bigl(\chi(g(t)):t\in T\bigr)
 =
 \sum_{\mathbf j\in\mathcal J_{d,n,m}}
 \prod_{s=1}^d e_{j_s}(\chi).
 \tag{CE9}
\]
For one composition, Hölder over \(\mathfrak M\), followed by enlargement
to all nontrivial characters, gives
\[
 \sum_{\chi\in\mathfrak M}
 \prod_s|e_{j_s}(\chi)|
 \le
 \prod_s
 \left(
   \sum_{\chi\ne1}|e_{j_s}(\chi)|^d
 \right)^{1/d}.
 \]
Since \(|e_j(\chi)|\le M_j\), (CE5) implies
\[
 \sum_{\chi\ne1}|e_j(\chi)|^d
 \le
 M_j^{d-2}\sum_{\chi\ne1}|e_j(\chi)|^2
 =\eta_jM_j^d.
 \tag{CE10}
\]
Sum the component bounds, divide by \(\binom{dn}{m}\), and obtain (CE7).
The trivial character is never inserted and therefore never needs to be
subtracted at the end.

For nonnegative \(a_1,\ldots,a_d\), generalized Hölder gives
\[
 \left(\prod_s(1+a_s)\right)^{1/d}
 \ge
 1+\left(\prod_sa_s\right)^{1/d}.
 \tag{CE11}
\]
Apply this with \(a_s=\eta_{j_s}\), then average with the probability
weights \(w_{\mathbf j}\). Since \(\kappa_j=1+\eta_j\), this gives
\(K_d\ge1+K_d^\circ\), proving (CE8). Equality can occur; centered is
never worse and is not claimed to be strictly better on every instance.

If \(A\) is trivial, every \(\eta_j=0\), the nontrivial major set is empty,
and (CE7) reads \(0\le0\). At \(m=0\) or \(m=dn\), the displayed algebra is
still valid, although the literal fixed-weight effective span is trivial;
retaining a nontrivial common \(A\) there is only an overcount.

The exclusion of the trivial character, the single common target, and exact
uniform fibers are load-bearing. For fiber multiplicities \(1\) and \(3\)
over character values \(1\) and \(-1\), the true polynomial is
\((1+Y)(1-Y)^3\), while pretending a uniform degree two gives
\(((1+Y)(1-Y))^2\); their coefficients differ.

## 5. The centered diagonal-energy input

Suppose, as a separate analytic input, that for all relevant weights
\[
 \mathrm{SP}_j-\frac{M_j^2}{|A|}
 \le C_nM_j.
 \tag{DE1}
\]
Then (CE3) gives
\[
 \eta_j\le C_n\frac{|A|}{M_j}.
 \tag{DE2}
\]
Theorem D therefore yields
\[
 C_{\rm maj}
 \le C_n B_d(n,m,A),
 \tag{DE3}
\]
where
\[
 B_d(n,m,A)
 =
 \frac{|A|}{\binom{dn}{m}}
 \sum_{\mathbf j\in\mathcal J_{d,n,m}}
 \left(\prod_s\binom n{j_s}\right)^{1-1/d}.
 \tag{DE4}
\]
For \(d=2\),
\[
 B_2(n,m,A)
 =
 \frac{|A|}{\binom{2n}{m}}
 \sum_j
 \sqrt{\binom nj\binom n{m-j}}.
 \tag{DE5}
\]

Input (DE1) is not proved here. It is exactly a centered collision-energy
or Poisson-scale variance statement on the quotient row. PR #564's
b2_l1_reduction_ledger.md already identifies
\[
 \Delta_{\rm energy}
 =\mathrm{SP}_j-\frac{M_j^2}{|A|}
 \]
as the subgroup-VMVT/Poisson-energy frontier and records why soft global
\(L^2\) arguments do not prove max-fiber Q. That work is the owner of the
analytic object. The new statement here is only its exact consumption by
the centered major compiler.

PR #564 also records dyadic imprimitive obstructions to some unconditional
local Poisson-variance formulations. Its deployed central regime is not
thereby decided: the dyadic tower accounts for only a small measured share
of its centered energy, while the primitive subgroup-VMVT term remains
open. Accordingly this packet labels (DE1) OPEN, not plausible-by-default
and not refuted at the displayed rows.

## 6. KB and M31 \(d=2\) calibration

The two full identity charts give exact degree-two geometry before arbitrary
primitive-leaf deletions.

| row | \(2n\) | \(m\) | \(p\) | quotient rank \(r\) | \(A\) |
|---|---:|---:|---:|---:|---:|
| KoalaBear MCA safe row | \(2^{21}\) | \(1{,}116{,}048\) | \(2{,}130{,}706{,}433\) | \(33{,}735\) | \(p^r\) |
| M31 MCA safe row | \(2^{21}\) | \(1{,}116{,}024\) | \(2{,}147{,}483{,}647\) | \(33{,}723\) | \(p^r\) |

For KoalaBear, the exact squaring fold retains the even power indices among
\(1,\ldots,67{,}471\). For M31, the exact \(T_2\) identity chart retains
the even Chebyshev indices among \(1,\ldots,67{,}447\); the triangular
Chebyshev/power basis change preserves the rank. Bounded ramification or
branch exceptions belong to their separately named profiles. These
statements concern the full identity charts, not every post-deletion A4
leaf.

An exact-binomial, high-precision-log computation with a scaled saddle
recurrence gives
\[
\begin{array}{c|c|c|c}
\text{row}&\log_2B_2&B_2&nB_2\\ \hline
\text{KB}&-27.950587886403&
  3.855091138975\cdot10^{-9}&0.00404235604614\\
\text{M31}&-20.459194784554&
  6.936951892869\cdot10^{-7}&0.727392126802
\end{array}
\tag{DE6}
\]
Thus the conditional bound \(C_n\le n\) would charge less than one unit on
each isolated degree-two band. On M31, whose raw normalized multiplier is
\(K_{\rm raw}=9\), reserving one unit for the trivial character leaves an
isolated-band allowance of eight. At that idealized allocation, (DE3) fits
whenever
\[
 C_n\le \frac8{B_2}
 =11{,}532{,}442.6687
 =10.9981943786\,n.
 \tag{DE7}
\]
This is a target calibration, not a proved allowance in a completed ledger:
other minor, major, primitive-Q, and ray/profile costs have not been assigned.
KoalaBear has much more raw multiplier room, but the same missing energy
theorem.

The source audits still label the first quotient rows OPEN-REDUCTION. No
value in (DE6)--(DE7) proves (DE1), full MA, Q, a safe row, or a frontier
move.

## 7. Consumer-backward hypothesis audit

| Required input | Supplied status |
|---|---|
| nondegenerate trace pairing and effective span \(V\) | unconditional finite-field linear algebra; (EF0)--(EF2) define the consumer object |
| one named global partition for Theorem C | must be chart data; constancy on only one routed fiber is not enough |
| exact \(d\)-fold live fibers for \(q=N/d\) and (CE9) | full power/Chebyshev identity charts supply this; arbitrary deletions may not |
| actual \(q\) for a nonuniform live restriction | always usable in (TR6), but may give no degree gain |
| subexponential map-family entropy | cyclic divisor and dyadic towers supply it on full domains; generic atlas entropy must still be checked |
| \(\log p_N=o(D_N)\) | absent from generic (A1)--(A7); A5's \(R_N<p_N\) is a lower bound on \(p_N\), not this upper relation |
| same effective target \(A_\phi\) at every intermediate weight | supplied by (TR2), not by weightwise renormalization |
| exclusion of the trivial character in (CE5)--(CE7) | load-bearing and explicit |
| centered diagonal energy (DE1) | OPEN; PR #564's subgroup-VMVT/Poisson frontier |
| exact KB/M31 quotient ranks | supplied only on the named full identity charts; not generic active-set saturation |
| other major bands, MI/Sidon, primitive Q, RC, profile add-back | not supplied by this packet |

The trace count does not need algebraic-major lift containment. The
algebraic count in PR #656 still does. Conversely, Theorem C counts only the
global factor-through character band for the named partitions; it does not
classify every algebraic exceptional phase.

## 8. Prior work and exact new delta

- (EF0)--(EF2) already remove ambient annihilator multiplicity, and PR #656
  already defines \(W_\phi\), \(A_\phi\), the exact factor-character dual,
  and the valid \(K_d-1\) compiler. Theorem C adds the exact ambient/effective
  rank sequence, the universal sharp \(p^{q-1}\) count, and its growing-tail
  entropy consequence. Theorem D adds the nontrivial-character centering.
- PR #656 Theorem A remains the arbitrary-common-weight MDS theorem for
  literal \(\mathbb B\)-valued algebraic phases. Theorem C is neither a
  replacement nor a corollary count on the same locus: it bounds the full
  effective trace-character locus by quotient rank.
- PR #564 owns the centered collision-energy/subgroup-VMVT frontier.
  This packet neither reproves nor solves it. The new contribution is the
  exact \(K_d^\circ\) compiler and the finite target obtained if that input
  is later proved.
- The KB/M31 rung audits own the row parameters, quotient ranks, and
  OPEN-REDUCTION statuses. The displayed calibration consumes those facts
  without changing their verdicts.
- PRs #655--#657 and the active exponential inverse-LO lane concern the
  primal degree-two PTE fiber/image frontier. They do not count this
  effective trace quotient group or prove (DE1).

## 9. Promotion-safe conclusion and nonclaims

A maintainer may safely record these two proved implications:

1. a certified family of global character-value quotient bands is
   sparse-major paid under (TR12), including extension trace-only modes;
2. every complete exact uniform fold obeys the centered effective major
   bound (CE7), and a future diagonal energy theorem (DE1) would be consumed
   with the explicit constant (DE4).

This packet does **not** prove that generic active sets remain fiber
saturated, that (TR12) holds for every sequence, that fixed-degree
factor-through groups are sparse, that (DE1) holds, that any intermediate
energy, Q/FI, minor/Sidon payment, overlap assignment with other cells, RC,
or full A4 holds, or that a deployed row or the Grand MCA theorem closes.
It does not modify paper TeX. Any later promotion remains separately gated
on a fresh audit that the TeX consumer supplies every displayed hypothesis.

## 10. Verification scope

The verifier checks exact ranks of \(V\), \(W_\phi\), their annihilators,
the restriction kernel and image, nonuniform partitions, the \(q=1\)
endpoint, and sharp weighted-Vandermonde examples. It enumerates ambient
characters on small cases to confirm that annihilator multiplicity cancels.
It checks centered collision identities, endpoint \(\eta\), coefficient
convolution and powered Hölder component inequalities for exact folds of
degrees \(2,3,4\) on elementary two-groups, plus a nonuniform-fiber
falsifier. It independently recomputes the two finite \(B_2\) calibrations,
pins the parent and consumer sources, and rejects semantic mutations of the
global-partition, actual-\(q\), map-entropy, characteristic-growth,
trace-multiplicity, common-target, trivial-character, uniform-fiber,
OPEN-energy, nonclosure, and no-TeX guards. The general proofs are the
derivations in Sections 2 and 4.
