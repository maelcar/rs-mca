# A4 successor: join-closed quotient-band disjointization

**Status:** the finite join identity, exact effective-character
stratification, Möbius formulas, and anchored pairwise compiler below are
PROVED. The required stratum or projected collision energies remain analytic
inputs. This packet changes no TeX and claims no deployed threshold.

**Stack and lineage:** this is a successor to PR #667, commit
\(bc51155206842c2944340ad9b1da429491383dec\), which is stacked on PR #664,
commit \(0aee8592065efacedc9f71679e6eda4f704f2469\). PR #664 supplies the
common effective trace-character bands. PR #667 supplies the exact
nonuniform full-slice factorization and pairwise-\(L^2\) compiler for one
band. The new delta canonically disjointizes a finite join-closed family of
those bands and permits each exact stratum to use its best eligible
factorization.

**Replay:**

    python3 experimental/scripts/verify_a4_quotient_band_join_compiler.py --write
    python3 experimental/scripts/verify_a4_quotient_band_join_compiler.py --check
    python3 experimental/scripts/verify_a4_quotient_band_join_compiler.py --tamper-selftest

The verifier is standard-library-only, imposes a 1 GiB address-space cap,
enumerates partitions and elementary \(p\)-group characters, and writes
experimental/data/certificates/a4-quotient-band-join-compiler/
a4_quotient_band_join_compiler.json.

## 1. Result map

Fix one coordinate-live set \(T\), one translated effective
\(\mathbb F_p\)-space \(V\), and a finite family of kernel partitions of
that same \(T\). A character that is constant on the fibers of two
partitions is constant on the fibers of their least common coarsening.
Equivalently, the two effective factor-through character bands intersect
in exactly the band of the join partition.

If the family is finite and join-closed, every character in the union of
its bands has a unique maximal, or coarsest, partition through which it
factors. This gives a canonical disjoint partition of the union. Exact
stratum cardinalities follow by Möbius inversion in the chosen family.
Exact projected collision energies for one fixed anchor also invert to the
nonnegative \(L^2\) masses of the same strata. PR #667's pairwise compiler
then conditionally bounds each stratum once.

This removes quotient-versus-quotient effective-character overlap for the
selected join-closed family. It does not create the family on a generic
leaf, show that it exhausts the effective major set, supply its energies,
or assign quotient characters against tangent, saturation, planted,
field-descent, split-pencil, or other first-match cells. In particular,
dual-character disjointization is not primal support or slope
first-match disjointization.

## 2. Common effective dual and actual-live joins

Let \(T\ne\varnothing\), let \(p\) be prime, and let
\[
 b:T\longrightarrow V
 \tag{JB1}
\]
take values in one finite-dimensional \(\mathbb F_p\)-space \(V\). For the
frontiers consumer, fix \(t_0\in T\) and take
\[
 V=\operatorname{span}_{\mathbb F_p}
   \{g(t)-g(t_0):t\in T\},
 \qquad b(t)=g(t)-g(t_0).
 \tag{JB2}
\]
The ambient affine coefficient differs from the translated coefficient by
the modulus-one factor already recorded in PR #667.

All partitions below are partitions of this actual live set \(T\). Order
them by refinement:
\[
 \alpha\preceq\pi
 \quad\Longleftrightarrow\quad
 \text{every \(\alpha\)-block lies in a \(\pi\)-block}.
 \tag{JB3}
\]
Thus larger partitions are coarser. Write \(\pi\vee\sigma\) for the least
common coarsening, obtained by taking the equivalence closure of the two
block relations.

For a partition \(\pi\), put
\[
 W_\pi=
 \operatorname{span}_{\mathbb F_p}
 \{b(t)-b(u):t,u\text{ lie in one \(\pi\)-block}\},
 \qquad
 A_\pi=V/W_\pi.
 \tag{JB4}
\]
Place every factor-through band inside the one common effective dual:
\[
 H_\pi
 =
 W_\pi^\perp
 =
 \{\chi\in\widehat V:\chi(w)=1\text{ for every }w\in W_\pi\}
 \cong\widehat{A_\pi}.
 \tag{JB5}
\]
If ambient trace parameters are used, (JB5) is the image
\(W_\pi^\perp/V^\perp\) inside
\(\widehat V\). Treating the abstract groups \(\widehat{A_\pi}\) as
unrelated character sets would make intersections meaningless.

### Theorem F (live partition join equals band intersection)

For any two partitions of the same actual live set,
\[
 \boxed{
 W_{\pi\vee\sigma}=W_\pi+W_\sigma,
 \qquad
 H_{\pi\vee\sigma}=H_\pi\cap H_\sigma.}
 \tag{JB6}
\]

### Proof

Every \(\pi\)-block and every \(\sigma\)-block lies in a
\(\pi\vee\sigma\)-block, so
\(W_\pi+W_\sigma\subseteq W_{\pi\vee\sigma}\).
Conversely, two points in one join block are connected by a path whose
successive pairs lie alternately in a \(\pi\)-block or a \(\sigma\)-block.
Their \(b\)-difference is the telescoping sum of the corresponding edge
differences, each in \(W_\pi\) or \(W_\sigma\). This proves the first
identity. Taking annihilators in the common dual gives the second.

### Actual-live guard

The join in (JB6) is formed after restriction to \(T\). Restriction need
not commute with a full-domain join. For example, on
\(\{1,2,3\}\), let one partition join \(1\) to \(2\) and another join
\(2\) to \(3\). After deleting \(2\), both restricted partitions on
\(\{1,3\}\) are discrete, while the restriction of their original join is
indiscrete. A full-domain algebraic join therefore cannot be substituted
without proving that the live restriction preserves its paths. Nested
towers may supply that compatibility; nonnested maps require the actual
live join to be recomputed.

## 3. Canonical nontrivial-character strata

Let \(\mathcal P\) be a nonempty finite set of distinct partitions of
\(T\), closed under \(\vee\). Relabelings of the same kernel partition are
deduplicated. Let
\[
 \Omega=\bigvee_{\pi\in\mathcal P}\pi,
 \qquad
 \mathcal H=\bigcup_{\pi\in\mathcal P}H_\pi,
 \tag{JB7}
\]
and let \(\mu_{\mathcal P}\) be the incidence Möbius function of the chosen
poset \((\mathcal P,\preceq)\).

For \(\chi\in\mathcal H\), the nonempty set
\[
 \mathcal P(\chi)=\{\pi\in\mathcal P:\chi\in H_\pi\}
 \tag{JB8}
\]
is closed under joins by (JB6). Hence it has the unique maximum
\[
 m(\chi)=\bigvee_{\pi\in\mathcal P(\chi)}\pi.
 \tag{JB9}
\]
Define the exact nontrivial stratum
\[
 S_\pi^\circ
 =
 \{\chi\in\mathcal H\setminus\{1\}:m(\chi)=\pi\}
 =
 (H_\pi\setminus\{1\})
 \setminus\bigcup_{\rho\succ\pi}H_\rho.
 \tag{JB10}
\]
Then
\[
 \mathcal H\setminus\{1\}
 =\bigsqcup_{\pi\in\mathcal P}S_\pi^\circ,
 \qquad
 H_\pi\setminus\{1\}
 =\bigsqcup_{\rho\succeq\pi}S_\rho^\circ.
 \tag{JB11}
\]
Only the raw top stratum contains the trivial character; (JB10) removes it
before every centered calculation.

Write
\[
 s_\pi=|S_\pi^\circ|.
 \tag{JB12}
\]
Möbius inversion of (JB11), using PR #664's
\(|H_\rho|=|A_\rho|=p^{\dim V-\dim W_\rho}\), gives
\[
 \boxed{
 s_\pi
 =
 \sum_{\rho\succeq\pi}
 \mu_{\mathcal P}(\pi,\rho)(|A_\rho|-1)
 \ge0.}
 \tag{JB13}
\]
The subtraction by one is load-bearing. It is equivalent to applying raw
inversion and removing the trivial character from the unique top stratum.

The Möbius function in (JB13) is that of \(\mathcal P\), not of the full
partition lattice. A join-closed subposet may omit intermediate
partitions, changing its incidence inverse.

## 4. Anchored projected energies

Fix \(\alpha,\pi\in\mathcal P\) with
\(\alpha\preceq\pi\). Use the partition \(\alpha\) as a factorization
anchor. Its blocks form \(Q_\alpha\); their sizes give the multiplicity
classes
\[
 Q_{\alpha,s}=\{y\in Q_\alpha:|y|=s\},
 \qquad n_{\alpha,s}=|Q_{\alpha,s}|,
 \qquad
 D_{\alpha,*}=\sum_{s:n_{\alpha,s}>0}s.
 \tag{JB14}
\]
For a block \(y\), let
\[
 h_\alpha(y)=[b(t)]\in A_\alpha
 \quad(t\in y).
 \tag{JB15}
\]
This is well-defined by (JB4). Adopt PR #667's class counts,
coefficients, slots, allocations, and convex weights:
\[
 M_{\alpha,s,j}=\binom{n_{\alpha,s}}j,
 \tag{JB16}
\]
\[
 r_{\alpha,s,j}(a)
 =
 \left|
 \left\{
 J\in\binom{Q_{\alpha,s}}j:
 \sum_{y\in J}h_\alpha(y)=a
 \right\}
 \right|,
 \tag{JB17}
\]
\[
 e_{\alpha,s,j}(\chi)
 =
 \sum_{J\in\binom{Q_{\alpha,s}}j}
 \chi\!\left(\sum_{y\in J}h_\alpha(y)\right).
 \tag{JB18}
\]
Let
\[
 \mathcal I_\alpha=
 \{(s,\ell):n_{\alpha,s}>0,\ 1\le\ell\le s\},
 \qquad |\mathcal I_\alpha|=D_{\alpha,*},
 \tag{JB19}
\]
and let \(\mathcal J_{\alpha,m}\) and \(w_{\alpha,\mathbf j}\) be the
allocation set and probability weights from (NC9)--(NC12).

For \(\rho\succeq\pi\), there is a canonical quotient
\[
 q_{\alpha\rho}:A_\alpha\twoheadrightarrow A_\rho.
 \tag{JB20}
\]
Push the fixed \(\alpha\)-slot count through this quotient:
\[
 r_{\rho\mid\alpha,s,j}(c)
 =
 \sum_{\substack{a\in A_\alpha\\q_{\alpha\rho}(a)=c}}
 r_{\alpha,s,j}(a).
 \tag{JB21}
\]
Projected Parseval gives
\[
 F_{\rho\mid\alpha,s,j}
 :=
 \sum_{\chi\in H_\rho}
 |e_{\alpha,s,j}(\chi)|^2
 =
 |A_\rho|
 \sum_{c\in A_\rho}
 r_{\rho\mid\alpha,s,j}(c)^2.
 \tag{JB22}
\]
Center before inversion:
\[
 F^\circ_{\rho\mid\alpha,s,j}
 =
 F_{\rho\mid\alpha,s,j}
 -M_{\alpha,s,j}^2
 =
 \sum_{\chi\in H_\rho\setminus\{1\}}
 |e_{\alpha,s,j}(\chi)|^2.
 \tag{JB23}
\]

Define the normalized stratum energy
\[
 z_{\pi\mid\alpha,s,j}
 =
 \frac1{M_{\alpha,s,j}^2}
 \sum_{\rho\succeq\pi}
 \mu_{\mathcal P}(\pi,\rho)
 F^\circ_{\rho\mid\alpha,s,j}.
 \tag{JB24}
\]
Möbius inversion of (JB11) for this one fixed slot function gives the exact
identity
\[
 \boxed{
 z_{\pi\mid\alpha,s,j}
 =
 \frac1{M_{\alpha,s,j}^2}
 \sum_{\chi\in S_\pi^\circ}
 |e_{\alpha,s,j}(\chi)|^2.}
 \tag{JB25}
\]
Consequently
\[
 0\le z_{\pi\mid\alpha,s,j}\le s_\pi,
 \qquad
 z_{\pi\mid\alpha,s,0}
 =z_{\pi\mid\alpha,s,n_{\alpha,s}}
 =s_\pi.
 \tag{JB26}
\]

Nonnegativity in (JB26) comes from the exact stratum identity, not from
termwise positivity of the Möbius sum. The coefficients in (JB24) may have
both signs. One-sided upper bounds on the cumulative energies cannot in
general be substituted into (JB24). An upper bound on the Möbius sum
requires exact values, a direct stratum estimate, or upper and lower
estimates matched to the coefficient signs.

The functions in (JB22) are the same \(\alpha\)-slot functions restricted
to deeper bands. They are not the native multiplicity-class functions of
\(\rho\). Native energies from different quotient targets cannot be mixed
or Möbius-inverted.

## 5. Quotient-band-disjoint anchored compiler

For an eligible anchor
\[
 \alpha\preceq\pi,\qquad D_{\alpha,*}\ge2,
 \tag{JB27}
\]
use the slot shorthand
\[
 z_{\pi\mid\alpha,u,j}=z_{\pi\mid\alpha,s,j},
 \qquad
 M_{\alpha,u,j}=M_{\alpha,s,j}
 \quad\text{for }u=(s,\ell).
\]
Then define
\[
 P_{\pi\mid\alpha}(m)
 =
 \sum_{\mathbf j\in\mathcal J_{\alpha,m}}
 w_{\alpha,\mathbf j}
 \min_{\substack{u,v\in\mathcal I_\alpha\\u\ne v}}
 \sqrt{
 z_{\pi\mid\alpha,u,j_u}
 z_{\pi\mid\alpha,v,j_v}}.
 \tag{JB28}
\]
The pair is chosen once for the fixed allocation. Repeated identical
factor functions remain distinct slots, as in PR #667.

Let the intrinsic full-slice coefficient be
\[
 \mathcal E_m(\chi)
 =
 [Y^m]\prod_{t\in T}(1+\chi(b(t))Y).
 \tag{JB29}
\]
For any designated
\(\mathfrak M\subseteq\mathcal H\setminus\{1\}\), put
\[
 C_{\mathfrak M}(m)
 =
 \frac1{\binom{|T|}m}
 \sum_{\chi\in\mathfrak M}|\mathcal E_m(\chi)|.
 \tag{JB30}
\]

### Theorem G (join-closed quotient-band compiler)

Under (JB1)--(JB27), for every integer \(0\le m\le |T|\),
\[
 \boxed{
 C_{\mathfrak M}(m)
 \le
 \sum_{\pi\in\mathcal P}
 \min\!\left\{
 s_\pi,\
 \min_{\substack{\alpha\in\mathcal P\\
                  \alpha\preceq\pi,\ D_{\alpha,*}\ge2}}
 P_{\pi\mid\alpha}(m)
 \right\}.}
 \tag{JB31}
\]
If a stratum has no eligible anchor, its inner minimum is \(+\infty\), so
the exact cardinality \(s_\pi\) is used.

### Proof

By (JB11), split \(\mathfrak M\) across the disjoint
\(S_\pi^\circ\). If \(\alpha\preceq\pi\), then
\(S_\pi^\circ\subseteq H_\pi\subseteq H_\alpha\), so every character in
the stratum factors through \(A_\alpha\). PR #667's exact
multiplicity-class expansion therefore applies at anchor \(\alpha\).

For one allocation, put every factor except two in \(L^\infty\), enlarge
\(\mathfrak M\cap S_\pi^\circ\) to \(S_\pi^\circ\), and apply
Cauchy--Schwarz to the two selected slots. Equation (JB25) gives
\[
 \sum_{\chi\in\mathfrak M\cap S_\pi^\circ}
 \prod_{r\in\mathcal I_\alpha}
 |e_{\alpha,r,j_r}(\chi)|
 \le
 \left(\prod_{r\in\mathcal I_\alpha}
 M_{\alpha,r,j_r}\right)
 \sqrt{
 z_{\pi\mid\alpha,u,j_u}
 z_{\pi\mid\alpha,v,j_v}}.
 \tag{JB32}
\]
Minimize over the two slots, sum the anchor's allocations, and use its
convex weights. This gives the \(P_{\pi\mid\alpha}\) bound.

Independently,
\[
 |\mathcal E_m(\chi)|\le\binom{|T|}m,
 \tag{JB33}
\]
so the normalized contribution of the stratum is at most \(s_\pi\).
Choose the better whole-anchor compiler or cardinality fallback for each
stratum and sum the disjoint strata, proving (JB31).

The minimization over anchors in (JB31) is over complete compiler values.
Allocations or terms from different anchor factorizations cannot be mixed
compositionwise.

### Chain specialization

If
\[
 \pi_0\prec\pi_1\prec\cdots\prec\pi_L,
 \tag{JB34}
\]
then the chosen-poset Möbius function is \(1\) on the diagonal, \(-1\) on
adjacent pairs, and zero farther above. Thus for \(i<L\),
\[
 s_{\pi_i}=|A_{\pi_i}|-|A_{\pi_{i+1}}|,
 \qquad
 z_{\pi_i\mid\alpha}
 =
 \frac{
 F^\circ_{\pi_i\mid\alpha}
 -F^\circ_{\pi_{i+1}\mid\alpha}}{M^2},
 \tag{JB35}
\]
while the top has
\[
 s_{\pi_L}=|A_{\pi_L}|-1,
 \qquad
 z_{\pi_L\mid\alpha}
 =F^\circ_{\pi_L\mid\alpha}/M^2.
 \tag{JB36}
\]
This is exactly the nested dual-shell theorem. The join formulation is
structurally stronger because it also disjointizes incomparable bands.

Nested towers have one additional consumer advantage: refinement survives
arbitrary coordinate restriction. If full-domain partitions satisfy
\(\pi_i\preceq\pi_j\), then their restrictions to the same live \(T\)
still satisfy that order, and their actual-live join is the restricted
\(\pi_j\). Thus, after deduplicating coincident restricted kernel
partitions, a certified chain needs no extra nonnested path compatibility
theorem. Its live block sizes, quotient ranks, energies, and compiler sum
still must be recomputed or bounded on the actual leaf.

## 6. Exact stress cases and invalid shortcuts

The verifier computes each of the following controls.

### A nonnested diamond with pairwise equality

Take \(T=\{1,2,3,4\}\),
\(V=(\mathbb Z/2\mathbb Z)^2\), and
\[
 b=(0,1,2,3).
 \tag{JB37}
\]
Let \(0\) be the discrete partition, let
\[
 \pi=12|34,\qquad \sigma=13|24,
 \qquad 1=1234.
 \tag{JB38}
\]
These four partitions form a join-closed diamond. Their within-block
spans have dimensions \(0,1,1,2\). The nontrivial stratum cardinalities
are
\[
 (s_0,s_\pi,s_\sigma,s_1)=(1,1,1,0).
 \tag{JB39}
\]
At total weight \(m=2\), every nontrivial intrinsic coefficient has
normalized absolute value \(1/3\). At anchor \(\pi\), the three
degree allocations have numerator weights \(1,4,1\), their pair factors
are \(1,0,1\), and
\[
 P_{\pi\mid\pi}(2)=\frac13.
 \tag{JB40}
\]
The same holds for \(\sigma\). This checks the common-dual intersection,
centered top, projected shell energy, repeated degree-two factors, and an
exact pairwise Cauchy equality.

### Missing join closure

For two incomparable partitions whose join is omitted, a character in the
band intersection has two incomparable maximal factor partitions. The
putative strata overlap. Adding the actual join restores the unique
maximum in (JB9).

### The wrong Möbius function

Take \(T=\{1,2,3,4\}\),
\(V=(\mathbb Z/2\mathbb Z)^2\),
\(b=(0,1,0,2)\), a discrete partition \(0\), and
\(\tau=123|4\). In the chosen two-element join chain,
\[
 \mu_{\mathcal P}(0,\tau)=-1.
 \tag{JB41}
\]
For a verified \(V=(\mathbb Z/2\mathbb Z)^2\) phase, the centered band
sizes are \(3\) and \(1\), so the true stratum sizes are \(2\) and \(1\).
The full partition-lattice interval has Möbius value \(+2\); substituting
it would print \(3+2\cdot1=5\) instead of \(2\).

### One-sided energy bounds do not invert

In the diamond, exact cumulative endpoint masses
\[
 (3,1,1,0)
 \tag{JB42}
\]
give bottom stratum mass \(3-1-1+0=1\). Valid separate upper bounds
\((3,2,2,0)\) would give \(-1\) if naively substituted. This is not an
upper bound and is not an energy. Signed Möbius inversion requires exact
cross-energies or two-sided information.

### Trivial character, duplicate bands, and invalid anchors

If (JB23) is not centered, the raw top stratum contains the trivial
character. If distinct partitions induce the same \(W_\pi\), their lower
strata may be empty and the unique maximal partition receives the band;
empty strata must remain exactly zero. A stratum may use only an anchor
\(\alpha\preceq\pi\). For an incomparable anchor, its block phase need not
be well-defined for characters of \(S_\pi^\circ\).

### All singletons and closure entropy

The discrete partition covers the entire effective dual but has
\(D_*=1\). PR #667's one-slot falsifier still applies, so that stratum
needs the cardinality fallback, a sparse count, a minor estimate, or
another theorem.

Join closure is also not automatically cheap. On \(2k\) points, \(k\)
partitions that independently merge \(k\) disjoint pairs generate
\(2^k-1\) nonempty joins; including the discrete empty join gives
\(2^k\) partitions. The finite theorem remains true, but asymptotic use
must bound the size or description entropy of the actual closure.

### Full-slice and marker guards survive

The theorem changes only the character assignment. It does not authorize
support-level first-match deletion. Nor does it erase PO3 occupancy
markers. PR #667's uniform degree-three example still has unmarked
pairwise compiler \(1/7\) but one-full-fiber component \(1/3\).

## 7. Consumer-backward hypothesis audit

| Required input | Supplied status |
|---|---|
| one coordinate-live \(T\), fixed \(m\), and full pre-first-match slice | supplied by the designated A3 leaf only before support-level deletion |
| translated effective span \(V\) and one common dual \(\widehat V\) | supplied by the manuscript's EF0--EF2 normalization |
| a finite list of distinct actual-live kernel partitions | not supplied generically; must be certified by the row or leaf |
| live join closure | not inherited from full-domain maps; every join must be recomputed or proved compatible after restriction |
| exact trace bands \(H_\pi\) and ranks \(|A_\pi|\) | supplied by PR #664 for a certified partition |
| actual multiplicity profiles and full-slice factorization at each eligible anchor | supplied conditionally by PR #667 |
| \(D_{\alpha,*}\ge2\) | checkable anchor by anchor; the discrete partition fails |
| exact projected cross-energies or direct stratum energies | OPEN analytic input; native energies of different partitions do not substitute |
| join-closure size and sum of (JB31) are \(e^{o(|T|)}\) uniformly | not supplied by finite validity |
| selected band union exhausts the effective major set | not supplied; characters outside the union retain their existing payment |
| assignment against non-quotient major cells | not supplied |
| primal first-match, support add-back, PO3, MI, Q/FI, RC, and target comparison | not supplied |

The actual TeX consumers are the definitions
def:effective-major-minor and def:major-arc-aggregate, together with the
exact finite loss statement (EF7): they need a disjoint subset of the
effective dual and its normalized coefficient sum. Theorem G supplies that
disjointization inside a selected quotient-band union. It resolves PR #656's
different-quotient-scale overlap nonclaim and PR #667's quotient-band
assignment clause in (NC27), for this exact scope.

PR #664's union-cardinality bound (TR11) was already overlap-safe and needs
no repair for validity. Exact strata may sharpen its numerical union bound
when the join ranks are known, but Theorem G's main new role is the
stratumwise energy compiler. The manuscript's def:first-match partitions
actual slope projections, not Fourier characters. Its overlap among
quotient, tangent, saturation, planted, and split-pencil witness loci is
unchanged. Likewise, the support-slice overlap multiplicity in
lem:exact-profile-addback is not forced to one by (JB11).

## 8. Prior work and exact new delta

- PR #656 owns the original effective quotient target and uniform
  uncentered compiler. It explicitly leaves different quotient scales
  unassigned.
- PR #664 owns the exact extension trace-character band
  \(|H_\pi|=|A_\pi|\), its growing-fold union count, and the centered
  uniform compiler.
- PR #667 owns the arbitrary actual-multiplicity factorization and
  pairwise centered compiler for one full-slice band. Theorem G uses that
  theorem without changing its class-energy, all-singleton, PO3, or
  support-deletion guards.
- The manuscript's stabilizer tower and quotient examples motivate nested
  bands. They do not print the common-dual join identity, canonical
  incomparable-band strata, or projected-energy Möbius compiler proved
  here.
- PR #564 retains ownership of the subgroup-VMVT/Poisson centered-energy
  frontier. No classwise or stratum energy estimate is reclaimed.
- PR #666 owns the split-pencil ray-collapse lane on the primal slope side.
  PR #662 owns the Hankel/CHG lane; PRs #661/#663 and #665 own the
  inverse-LO and fixed-\(e\) Case-B lanes. The present theorem uses none of
  their claims.

## 9. Promotion-safe conclusion and nonclaims

A maintainer may safely record:

> On one full coordinate-live fixed-weight leaf, a selected finite
> join-closed family of effective trace quotient bands has a canonical
> disjoint nontrivial-character stratification. Its exact stratum
> cardinalities are (JB13), and exact projected stratum energies at any
> eligible finer anchor feed the collision-free compiler (JB31).

This becomes an MA payment only after the selected family and its actual
live joins are certified, its union is matched to the desired effective
major subset, the exact/direct stratum energies and closure entropy are
controlled, and the sum in (JB31) is uniformly subexponential.

This packet does **not** prove that quotient maps exist on a generic A4
leaf, that arbitrary nonnested full-domain joins survive live restriction,
that the selected union exhausts the effective majors, or that its
complement is minor. It does not infer energy bounds from cardinalities,
pass one-sided energy bounds through signed Möbius coefficients, mix
native energies from different targets, or prove PR #564's analytic input.

The strata resolve quotient-versus-quotient dual-character overlap only.
They do not give a witness-exhaustive primal first-match atlas; assign
quotient bands against tangent, saturation, planted, extension,
split-pencil, or other cells; control support-slice overlap; apply after
support-level deletion; or encode a fixed PO3 component. No MI, Q/FI, RC,
full MA/A4, deployed threshold, Grand MCA closure, or TeX promotion is
claimed. Any later TeX promotion remains gated on a fresh audit matching
every displayed hypothesis to its actual consumer.

## 10. Verification scope

The verifier checks partition refinement and joins, alternating-chain
closure, \(W_{\pi\vee\sigma}=W_\pi+W_\sigma\), common-dual band
intersections, exact ranks, join-closed unique maxima, chosen-poset Möbius
inversion, centered cardinalities, projected Parseval, exact stratum
energies, pairwise anchored compilation, whole-anchor minimization,
cardinality fallback, chain-shell specialization, nonnested diamond and
degree-two equality cases, and elementary \(p=2,3\) examples.

It also rejects or falsifies missing join closure, meet-for-join reversal,
ambient-partition Möbius substitution, uncentered top leakage,
one-sided-energy inversion, native-energy mixing, duplicate map labels,
incomparable anchors, all-singleton pairwise use, compositionwise mixing of
anchors, unbounded join-closure inference, support deletion, erased PO3
markers, generic exhaustion, other-cell overlap, and TeX promotion.
