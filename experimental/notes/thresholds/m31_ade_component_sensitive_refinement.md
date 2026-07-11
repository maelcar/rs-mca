# M31 common-height ADE cut: component-sensitive rho-below-nine refinement

**Status:** PROVED for the M31-specific common-height ADE proposition and the
exact finite-classifier delta below. This packet is stacked on PR #653 commit
8788a24. All four non-log parent payload files remain byte-identical; the
shared agents log gains only this successor entry, with the parent entry
preserved byte-for-byte. No statement is promoted into the frontiers TeX.

**Lineage:** DannyExperiments PR #637 supplied the common-height ADE model and
original census. Claude/holmbuar PR #648 audited it and isolated the integral
D_s gap. PR #653 repaired that gap. The present packet combines the repaired
D_s branch with the exact A_s dual-norm spectrum and a global allocation
argument. It neither replaces nor rewrites those packets.

**Replay:**

    python3 experimental/scripts/verify_m31_ade_component_sensitive_refinement.py --write
    python3 experimental/scripts/verify_m31_ade_component_sensitive_refinement.py --check
    python3 experimental/scripts/verify_m31_ade_component_sensitive_refinement.py --tamper-selftest

The verifier is standard-library-only, streams the 3,254,885-row source grid
in constant extra memory, imposes a 1 GiB address-space cap, and writes
experimental/data/certificates/m31-ade-component-sensitive/
m31_ade_component_sensitive_refinement.json.

## 1. Exact M31-specific proposition

Use

    N=2^21,        L=8N,        d0=N-67447,
    t_*=276416,    rho_*=rho(t_*)=579686367232/64410204497<9.

Let S consist of L distinct roots in an ADE root lattice of total rank r<=N.
Assume distinct selected roots have pairwise inner products in {0,1} and a
dual vector zeta has height one on every selected root. If

    ||zeta||^2 <= rho_*,

then

    |S| <= 8r+36rho_* < 8r+324,
    r >= N-40 = d0+67407.                                  (CS-ADE-9)

Together with the M31 modular rank bound rank_Fp(Q)<=d0, this rank floor and
the ADE determinant bound are contradictory. Thus the common-height M31
family cannot exist whenever its construction supplies the displayed
hypotheses.

This is deliberately M31-specific: excluding a large A_s component uses both
the fixed family size L and the real-rank upper bound r<=N. The local
component estimates alone do not assert a rank-free theorem for every
rho<9.

## 2. Hypothesis audit

| Printed input | Exact use | Supplied by the M31 consumer? |
|---|---|---|
| exactly L=8N distinct selected roots | contradict the maximum contribution of one heavy A_s component plus all light components | Yes, #637 Sections 1 and 3 |
| total real rank r<=N | bound every A_s rank and the determinant above by the ambient M31 dimension | Yes, #637 equations (5)-(6) |
| orthogonal ADE decomposition and zeta in its dual | decompose rank and norm and use the exact component dual spectra | Yes, #637 Section 3 |
| common height one | invoke Coxeter root counts, the repaired integral-D_s support count, and Bessel bounds | Yes, #637 equation (7) |
| pairwise inner products in {0,1} | used in the two D_s support branches inherited from #637/#653 | Yes, #637 equation (6) |
| total squared norm at most the fixed rho_*<9 | make a heavy A_s component unique, bound its rank, and cap matching/component counts | Yes, monotonicity gives rho(t)<=rho_* for t>=t_* |
| roots have squared norm two | fixes the standard A_s,D_s,E_s normalizations, Coxeter identity, and c/2 Bessel cost | Yes, #637 equation (6) |
| 2Nt-R>0 and t,m nonzero modulo p on the classified grid | define the real common-height embedding and transfer equation (3) to the modular rank bound below #637's old threshold | Yes, at t_* the first quantity is 64410204497>0; every classified source-grid t is at most 490564<p, and 0<m<p |
| modular rank at most d0 over F_p | supply the Smith lower bound p^(r-d0) | Yes, #637 equations (3)-(4) |

No lower bound on rho(t), integrality of A_s coordinates, large-rank
asymptotic, modular-to-real rank identification, or stronger determinant
estimate is used. No additional field hypothesis beyond the pinned M31 prime
and modular-rank input is introduced. The proof always applies the **fixed
boundary parameter** rho_*; it never silently assumes that the decreasing
quantity rho(t) remains above eight.

## 3. Exact A_s dual-norm spectrum

Put n=s+1 and realize

    A_s={x in Z^n: sum_i x_i=0},       roots e_i-e_j.

For z in A_s^*, all differences z_i-z_j are integers and sum_i z_i=0.
Choose integers a_i and, after a common integer shift, a residue
m=sum_i a_i in {0,...,n-1} such that

    z_i=a_i-m/n.

Since every a_i(a_i-1) is an even nonnegative integer,

    Z=||z||^2
     =sum_i a_i^2-m^2/n
     =m(n-m)/n+2j
     =Q-m^2/n,                                           (A-spectrum)
    Q=m+2j,       j=(1/2)sum_i a_i(a_i-1)>=0.

Replacing z and all selected roots by their negatives if necessary preserves
heights and inner products, so take 0<=m<=n/2.

Suppose one A_s component is heavy, meaning 8<Z<=rho_*<9. Then
m/2<=m(n-m)/n<=Z and 2j<=Z, so m<=17, j<=4, and Q>=9. If Q>=10,

    n < m^2/(Q-9) <= 100,                                  (A-Q>=10)

where the finite maximum is attained at (m,j,Q)=(10,0,10). Hence for n>=111
one must have Q=9; then m is odd and at most nine. The fixed boundary gives

    n <= floor(m^2/(9-rho_*))
      <= floor(81/(9-rho_*))
      = 953224.                                             (A-heavy-rank)

For n<111 the same final cap is automatic. Thus every heavy A_s component
has n<=953224.

There can be at most one heavy component because the total norm is below
nine. Its Coxeter count is strictly less than 9*953224. All remaining
components have total norm below one. Their A roots number less than N+1; an
integral D projection then has norm zero and no height-one root; a
half-integral irreducible D_s projection costs at least s/4>=1; and all
remaining E roots number less than 30. Therefore a heavy A_s component would
force

    |S| < 9*953224 + (N+1) + 30
        = 10676199
        < L=16777216,

a contradiction. Consequently every A_s component actually has Z<=8.

## 4. Light-component bounds and global summation

Write Z_C for the component squared norm.

- **A_s:** Section 3 gives Z_C<=8. The Coxeter identity gives
  |S_C|<=nZ_C=sZ_C+Z_C<=8s+Z_C.
- **Integral D_s:** because Z_C is an integer below nine, Z_C<=8.
  PR #653 proves |S_C|<=8(s-k)+binom(k,2)<8s for 1<=k<=8, while k=0
  has no height-one root.
- **Half-integral D_s:** s<=4Z_C. There is at most one selected root per
  support. A support-graph matching of size nu gives nu orthogonal height-one
  roots, hence nu/2<=Z_C<9 and nu<=17. The Erdos-Gallai matching edge bound
  gives |S_C|<=17s<=8s+36Z_C.
- **Exceptional E:** the Coxeter number is at most 30, hence
  |S_C|<=30Z_C<=8s+30Z_C.

Thus every component satisfies

    |S_C| <= 8 rank(C)+c_C Z_C,       c_C<=36.

Orthogonality gives sum_C Z_C=||zeta||^2<=rho_*; summing proves
|S|<=8r+36rho_*<8r+324. Since L=8N and r is integral,

    r >= N-40 = 2097112 = d0+67407.                         (rank-CS-9)

## 5. Exact M31 boundary and determinant contradiction

Use the deployed function

    rho(t)=Nt/(2Nt-R).

It decreases, and the exact first integer with rho(t)<9 is

    t_*=276416,
    rho_*=579686367232/64410204497=8.999915025...,
    rho(276415)>9.

The old #637 statement started at t=277868, so its construction hypotheses
must be rechecked rather than inherited from that conclusion. At the new
boundary,

    2Nt_*-R=64410204497>0,

so h^2=2-R/(Nt)>0 for every t>=t_*. On the finite source grid,
t<=floor(m/2)=490564<p=2^31-1, while 0<m=981129<p; hence both t and m remain
nonzero modulo p. Therefore #637 equations (3)-(7) algebraically remain valid
for every source-grid t>=t_*, independently of its old classifier threshold.
In particular they supply ||zeta||^2<=rho(t)<=rho_*, so Sections 3-4 apply
with the fixed parameter.

Choose r independent selected roots. Their Gram determinant is divisible by
p^(r-d0). If their generated ADE lattice has c irreducible components, one
selected height-one root from each component is orthogonal to the others;
Bessel gives c/2<=rho_*<9, hence c<=17. The irreducible ADE determinant
formulas then give

    p^67407 <= p^(r-d0) <= det(B) <= (N+1)^17,

which is false (indeed exponent 12 already suffices on the left). This
contradiction proves the classifier throughout the enlarged band.

## 6. Exact finite-census consequence

The sound classifier is now

    kappa=2, (e1,e2)=(t,2t), t>=276416.

Relative to the audited #637/#653 ledger, the threshold and residual move
exactly as follows:

    threshold       277868 -> 276416
    residual       2987412 -> 2985960

On the finite source grid:

    classifier total                 214149
    new exclusions beyond PR #628    115316
    new exclusion union              268925
    new residual                    2985960
    increment beyond #637/#653          1452

The added rows are exactly (2,t,t,2t) for 276416<=t<=277867. The first row
not certified by this component-sensitive route is

    (2,276415,276415,552830).

This is a certificate boundary, not a counterexample.

## 7. Verification scope and nonclaims

The verifier checks the encoded consequences of the written exact A_s^*
spectrum derivation, the finite Q>=10 optimization, the heavy-component
allocation arithmetic, every light-component coefficient, semantic weakening
controls, the fixed boundary rational and determinant margin, the parent PR
#653 replay, and every old/new count and SHA-256 digest by streaming the
canonical source-grid order.

This packet deliberately stops at rho<9. It does not optimize any rho>=9
regime, claim that t=276415 survives, modify a parent certificate, exclude
another kappa or shell pattern, close the remaining 2,985,960 two-shell rows,
prove a complete M31 upper ledger, or solve a deployed CAP25 row. It changes
no TeX file.
