# Exact R=2 C9 razor audit and two-moment Prouhet counterexample

## Status

**COUNTEREXAMPLE_NEW_FLOOR** for the unrestricted R=2 question printed in
PR #585.  **FIXED** for R=2 leaves with subexponential realized image.
**OPEN GAP** for the intended smooth/circle primitive first-match residual over
an exponentially large profile field.

No statement from this packet is promoted into
experimental/asymptotic_rs_mca_frontiers.tex.

## Consumer-backward hypothesis audit

The active consumer is the frontiers-paper interface, not the older compact
normalization.  For a full fixed-weight slice \(\Omega_N^0\), it uses

\[
 M_N=|\Omega_N^0|,\qquad
 L_N=|\Phi_N(\Omega_N^0)|,\qquad
 \bar N_N=M_N/L_N,
\]

but its counted fibers are residual:

\[
 F_{N,s}=\Omega_N^\circ\cap\Phi_N^{-1}(s),\qquad
 f_{N,s}=|F_{N,s}|.
\]

Here \(\Omega_N^\circ\) must be the exact primitive first-match residual after
the printed algebraic cells have been routed.  The active-coordinate density
is bounded away from zero and one, the boundary columns and characteristic
hypotheses must be stated, and a logarithmic order \(q_N\to\infty\) must satisfy
\(\log L_N/q_N=o(N)\).  The Sidon cut is

\[
 \Gamma^{\rm sid}_{q_N,\sigma}
 =\frac1{L_N}\sum_{\Delta(F_{N,s})\le e^{-\sigma N}}
   \left(\frac{f_{N,s}}{\bar N_N}\right)^{q_N}
\]

for every fixed \(\sigma>0\), uniformly over consumed profiles.  The desired
conclusion is primitive Q,
\(\max_s f_{N,s}\le e^{o(N)}\bar N_N\).  A distinct-ray or MCA conclusion still
requires RC or a direct ray bound.

These requirements are pinned by
def:admissible-sequence, eq:exact-power-sum-map, eq:image-ambient-scales,
eq:full-image-certificate, def:primitive-first-match-residual, def:sidon-heavy,
def:sidon-paid-cell, thm:intro-sidon-heavy-repair, def:primitive-q,
thm:primitive-q, prop:high-energy-impossible, and hyp:ray-compiler.  The compact
predecessor uses residual mass and residual image instead.  PR #585 follows
that older convention in places, so its statements cannot be moved into the
frontiers draft without restatement.

## Cut 1: small realized image pays R=2 without energy

For every residual fiber,

\[
 \frac{f_s}{\bar N}\le \frac{M}{M/L}=L.
\]

More precisely, since \(\sum_s f_s\le M\),

\[
 \Gamma^{\rm sid}_{q,\sigma}
 \le \frac1L(\max_s f_s/\bar N)^{q-1}
               \sum_s f_s/\bar N
 \le L^{q-1}.
\]

Therefore \(\log L=o(N)\) proves both primitive Q and the Sidon moment payment
directly.  If \(\Phi\) has two coordinates over \(\mathbb B\), then
\(L\le|\mathbb B|^2\).  Thus

\[
 R=2,\quad \log|\mathbb B|=o(N)
 \quad\Longrightarrow\quad
 \max_s f_s/\bar N=e^{o(N)}
\]

for every residual, with no energy, field geometry, or first-match assumption.

This closes every polynomial-field R=2 toy in PR #581 before its energy is
computed.  A nontrivial R=2 frontier requires \(\log L=\Omega(N)\), hence
\(\log|\mathbb B|=\Omega(N)\).

## Cut 2: positive-rate size already forces TeX-low energy

Use the published Boolean-cube energy consequence

\[
                 E(F)^3\le |F|^8.
\]

For \(f=|F|>0\) and \(\Delta=E(F)/f^3\),

\[
                 \Delta^3\le \frac1f.
\]

If \(f_s/\bar N\ge e^{\eta N-o(N)}\), then \(\bar N\ge1\) gives
\(f_s\ge e^{\eta N-o(N)}\), and hence

\[
                 \Delta(F_s)\le e^{-\eta N/3+o(N)}.
\]

For any fixed \(\sigma<\eta/3\), this Q-bad fiber lies in the TeX Sidon-heavy
sum.  Its single contribution satisfies

\[
 \Gamma^{\rm sid}_{q,\sigma}
 \ge L^{-1}(f_s/\bar N)^q,
\]

which has positive rate because \(\log L/q=o(N)\).  Conversely primitive Q
bounds every Sidon submoment.  Under the full-slice normalization, the
Boolean energy input above, logarithmic-moment accessibility, and the printed
uniform quantifiers, at positive exponential scale,

\[
                 \boxed{\text{Sidon payment}\iff\text{primitive Q}}.
\]

The current frontiers BSG/quasicube theorem is a sound conditional treatment
of the complementary TeX-high-energy branch.  The rational-power input above
makes its size cutoff explicit.  This aligns with scottdhughes's measured
correction in PR #564 at the method level: BSG/Freiman is not an attack on a
positive-rate bad fiber, because such a fiber is forced into the low-energy
branch.  PR #564's structured moment-curve evidence uses a large-doubling
notion of near-Sidon; the exact ratio to the Sidon floor and PR #585's printed
absolute threshold are different predicates.

Consequently the proposed PR #582/#585 target
\(\Delta(F)\ge f^{-c}\) for some fixed \(c<1\) is insufficient.  For
\(f=e^{\Theta(N)}\), it is still an exponentially small lower bound.  The
nonvacuous high-energy target is \(\Delta\ge f^{-o(1)}=e^{-o(N)}\).
Combined with \(\Delta\le f^{-1/3}\), a fixed lower exponent contradicts
unbounded \(f\) only when \(c<1/3\), not merely when \(c<1\).

The full cube makes the logical failure exact:
\(f=2^N\), \(E=6^N\), and
\(\Delta=(3/4)^N=f^{-\log_2(4/3)}\).  It satisfies, for example,
\(\Delta\ge f^{-1/2}\) with \(1/2<1\), while remaining exponentially
TeX-low-energy.

## Exact two-moment counterexample to the unrestricted R=2 razor

This construction extends avdeevvadim's PR #444 one-nontrivial-moment
interface counterexample to the exact two nontrivial power sums used by
PRs #579, #581, #582, and #585.

### Local Prouhet block

Let

\[
 V=\{0,1,2,4,5,6\},\qquad
 A=\{0,4,5\},\qquad B=\{1,2,6\}.
\]

Both \(A\) and \(B\) have cardinality \(3\), sum \(9\), and square-sum \(41\).
Exhausting all \(64\) subsets of \(V\) shows that this is the only collision
of

\[
             S\longmapsto (|S|,\sum_{u\in S}u,\sum_{u\in S}u^2).
\]

The numbers of distinct local signatures by weight are

\[
                 (1,6,15,19,15,6,1),
\]

so their weight enumerator is

\[
                 P(x)=(1+x)^6-x^3.
\]

### Separated blocks and a no-wrap prime field

Fix \(C=20\) and \(Q=1000\).  For \(0\le i<k\), put

\[
 T_i=\{(C+u)Q^i:u\in V\},\qquad T=\coprod_iT_i.
\]

Write \(S_{2,k}=\sum_{t\in T}t^2\).  By Bertrand's postulate, choose a
prime

\[
                  S_{2,k}<p_k<2S_{2,k},
\]

and regard \(T\) as a subset of \(\mathbb F_{p_k}\).  Then
\(\log p_k=\Theta(k)=\Theta(N)\).

The first-moment digit is
\(d_i=|S_i|C+\sum_{u\in S_i}u\le6\cdot20+18=138<Q\).
Since \(0\le\sum_{u\in S_i}u\le18<C\), it uniquely recovers
\(|S_i|\) and the local sum.  The second-moment digit is
\(e_i=|S_i|C^2+2C\sum_{u\in S_i}u+\sum_{u\in S_i}u^2
\le6\cdot400+40\cdot18+82=3202<Q^2\),
and then uniquely recovers the local square-sum.  Thus no carries occur, and
joint equality of the two global moments is equivalent to equality of the
local cardinality, sum, and square-sum in every block.  The choice of \(p_k\)
makes field equality identical to integer equality.

Take the full slice \(\Omega^0=\binom{T}{3k}\) and

\[
                 \Phi(S)=(\sum_{t\in S}t,\sum_{t\in S}t^2).
\]

Put

\[
 A_i=\{(C+u)Q^i:u\in A\},\qquad
 B_i=\{(C+u)Q^i:u\in B\}.
\]

The target fiber is exactly

\[
 F_k=\{\coprod_i U_i:U_i\in\{A_i,B_i\}\}.
\]
Therefore

\[
                 f_k=2^k.
\]

This is a genuine full-slice fiber, not a sampled or hand-selected residual.

### Exact image normalization

Blockwise factorization gives

\[
 M_k=\binom{6k}{3k},\qquad
 L_k=[x^{3k}]P(x)^k,\qquad
 \bar N_k=M_k/L_k.
\]

The coefficient sequence of \(P\) is symmetric and log-concave; convolution
preserves log-concavity, so the central coefficient of \(P^k\) is maximal.
Since \(P(1)=63\),

\[
 L_k\ge\frac{63^k}{6k+1},\qquad M_k\le64^k,
\]

and hence

\[
 \frac{f_k}{\bar N_k}
 =\frac{2^kL_k}{M_k}
 \ge\frac{(63/32)^k}{6k+1}
 =e^{(\log(63/32)/6)N-o(N)}.
\]

There is also a completely finite subsequence proof that avoids the convolution
lemma.  Inclusion-exclusion gives

\[
 [x^9]P(x)^3
 =\binom{18}{9}-3\binom{12}{6}+3\binom{6}{3}-1=45907.
\]

For \(k=3r\), restrict the image count to sequences
whose consecutive triples of blocks each have weight \(9\).  Then

\[
 L_{3r}\ge45907^r,\qquad M_{3r}\le64^{3r},
\]

so

\[
 \frac{f_{3r}}{\bar N_{3r}}
 \ge\left(\frac{45907}{32768}\right)^r.
\]

The excess is positive at a fixed exponential rate.

### Exact energy and C9 failure

The fiber is an affine copy of \(\{0,1\}^k\) in disjoint coordinate blocks.
Difference equality factorizes blockwise, so

\[
 E(F_k)=6^k,\qquad
 \Delta(F_k)=\frac{6^k}{(2^k)^3}
            =\left(\frac34\right)^k
            =e^{-(\log(4/3)/6)N}.
\]

For every fixed \(\sigma<\log(4/3)/6\), the target lies in the TeX low-energy
cut.

In PR #585's printed absolute sense, this is near-Sidon: it passes every
fixed-threshold test eventually, and
\(\Delta(F_k)-(2f_k-1)/f_k^2\to0\).  The construction is not multiplicatively
near the literal Sidon floor, since

\[
 \frac{E(F_k)}{2f_k^2-f_k}
 =\frac{(3/2)^k}{2-2^{-k}}\sim\frac12(3/2)^k.
\]

Also \(L_k\le M_k\le2^N\), so every logarithmic \(q_N\to\infty\)
satisfies \(\log L_k/q_N=o(N)\).  The one target fiber gives

\[
 \liminf\frac{\log\Gamma^{\rm sid}_{q_N,\sigma}}{Nq_N}>0.
\]

Thus the unrestricted PR #585 YES/NO table has answer **YES** under the
fixed-threshold/absolute-\(o(1)\) criterion it actually prints.  This does not
answer a strengthened ratio-to-floor question, which is neither stated there
nor the TeX C9 predicate.

## Scope boundary: what remains open

The construction matches all of the following literal data:

- a full fixed-weight slice with \(m/N=1/2\);
- distinct nonzero points in a prime field with characteristic greater than \(2\);
- the exact map \((\sum t,\sum t^2)\), equivalently weighted Vandermonde
  columns \(t(1,t)\);
- full-slice realized-image normalization;
- additive energy in \(\mathbb Z^T\);
- logarithmic-moment accessibility.

It is not a smooth multiplicative/circle domain and has a visible bounded-block
Prouhet product.  It is not proved to survive an exact first-match atlas that
routes such block, folding, quotient, or planted profiles.  Therefore it does
**not** refute the intended structured primitive theorem.

Holmbuar's PR #614 proves that this image-normalized razor is orthogonal to
the span-normalized image clause \((S_E)\).  Neither this construction nor a
hypothetical razor-NO conclusion supplies \((S_E)\), \((EFP)\), or any span-side
consequence.

It does prove that adding a second nontrivial power sum does not repair the
literal quantitative interface.  The word primitive must be an evaluable
hypothesis, not an informal exclusion.

## PR audit ledger

| Source | Verdict | Consumer-backward audit |
| --- | --- | --- |
| PR #575, LegaSage | NO ISSUE after restatement | The max-low-fiber moment bound is correct, but promotion must use full-slice \(\bar N\), residual fibers, fixed-\(\sigma\) cuts, and uniform logarithmic orders. |
| PR #577, LegaSage | FIXED | Newton injectivity is valid for the unweighted map with distinct points, \(R\ge m\), and characteristic \(>m\).  Its image-size majorant closes R=2 whenever \(\log|\mathbb B|=o(N)\). |
| PR #579, LegaSage | NO ISSUE in its printed special range | The fixed-\(m\) induction needs characteristic different from two and does not reach fixed density. |
| PR #581, LegaSage | OPEN GAP measurement only | The sweep uses constant cutoff \(0.75\), polynomial CE bars, sampled slices, interval domains, and some composite moduli.  Its \(p=O(N)\) rows are already paid by \(L\le p^2\). |
| PR #582, LegaSage | COUNTEREXAMPLE_NEW_FLOOR | The fixed \(c<1\) energy target does not imply TeX-high energy.  Its correct endpoint is direct Q or \(\Delta\ge f^{-o(1)}\). |
| PR #585, LegaSage | COUNTEREXAMPLE_NEW_FLOOR / OPEN GAP | The unrestricted R=2 razor is false by \(F_k\).  The exact smooth/circle primitive-residual version remains open. |
| PR #564, scottdhughes | NO ISSUE; COMPLEMENTARY MEASUREMENT | Its structured moment-curve toys support a large-doubling sense of near-Sidon and correct BSG/Freiman as the wrong tool.  This is measured, not an asymptotic theorem, and differs from both literal-floor proximity and PR #585's absolute cutoff. |
| PR #614, holmbuar | NO ISSUE; ORTHOGONAL FACE | It proves that the image-normalized razor does not control the span-normalized \((S_E)\) image clause.  This packet makes no span-side claim. |

PR #581's executable phrase near-Sidon is also not the TeX predicate.  Its
absolute test
\(\Delta-(2f-1)/f^2<0.05\) is not scale-free and can label tiny fibers.
Literal Sidon extremality is measured by \(E/(2f^2-f)\), while TeX-low energy
only asks \(\Delta\le e^{-\sigma N}\).  These three notions must not be
interchanged.

## Corrected research target

The subexponential-image R=2 regime is closed.  The unrestricted
exponential-field regime is false.  The remaining target is:

> On an exact admissible smooth/circle sequence with an exponentially large
> realized R=2 image, prove primitive Q directly on the formally defined
> post-first-match residual, or construct a counterexample that survives every
> named algebraic routing cell.

Energy is diagnostic but does not narrow this target: any positive-rate
counterexample is automatically TeX-low-energy.  Weighted charts, \(R=1\),
\(3\le R<m\), window uniformity, span-side \((S_E)\), FI, RC, profile add-back,
and target/reserve comparisons remain separate.

## Lineage and verification

- avdeevvadim PR #444: literal-interface specification guard and the original
  one-nontrivial-moment block counterexample;
- LegaSage PRs #575, #577, #579, #581, #582, and #585: the max-fiber chain,
  finite measurements, and terminal question audited here;
- scottdhughes PR #564: the measured structured-moment-curve large-doubling
  correction and the BSG/Freiman method warning;
- holmbuar PR #614: orthogonality of the razor to the span-side \((S_E)\) clause;
- de Dios Pont--Greenfeld--Ivanisvili--Madrid, Additive Energies on Discrete
  Cubes: the published Boolean energy bound used in Cut 2.

The replay script is
experimental/scripts/verify_c9_r2_near_sidon_razor.py.  It exhausts the local
signature table, checks exact image and energy rows, verifies both rate bounds
and the image-cap/energy cuts, pins the frontiers labels, and rejects scope
overclaims.  The packet makes no TeX edit.
