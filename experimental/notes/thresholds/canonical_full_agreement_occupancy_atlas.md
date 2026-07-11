# Canonical full-agreement occupancy atlas

- **Status:** PROVED exact compiler and saturated-stratum payment.
- **Track:** asymptotic hard input A / profile-envelope refinement.
- **Verifier:**
  `python3 experimental/scripts/verify_canonical_full_agreement_occupancy_atlas.py`.

## Occupancy data

Let `F` be a finite field, let `C=RS_F(D,k)`, and let

```text
D = D_0 disjoint_union X,
|X|=b,
phi : D_0 -> Q,
|Q|=N,
```

where every `phi`-fiber has one common size `c>=2`.  Thus
`n=|D|=b+cN`.

For `T subset D`, define its occupancy profile

```text
lambda_phi(T) = (t,m,p,rho),
```

where `t=|T intersect X|`, `m` is the number of complete fibers in `T`,
`p` is the number of nonempty proper fibers in `T`, and `rho` is the
total number of selected points in those proper fibers.  The exact number
of sets with profile `lambda=(t,m,p,rho)` is

```text
H_phi(lambda)
 = binom(b,t) binom(N,p) binom(N-p,m)
   [z^rho] ((1+z)^c-1-z^c)^p.                             (1)
```

This is the integrated partial-occupancy count, now applied separately to
the witness support and to its full agreement set.

## Joint full-agreement atlas

Fix a received line `r=(r_0,r_1)` and exact support size
`a>=k+1`.  A witness is a triple

```text
w=(gamma,S,h),
|S|=a,
deg h<k,
h(x)=r_0(x)+gamma r_1(x) for x in S,
```

whose support is noncommon: no pair of degree-less-than-`k` polynomials
simultaneously explains `r_0,r_1` on `S`.  Define its full agreement set

```text
A(w)={x in D : h(x)=r_0(x)+gamma r_1(x)}.                 (2)
```

Then `S subset A(w)` and `|A(w)|>=a`.  For support profile `sigma` and
agreement profile `alpha`, put

```text
C_(sigma,alpha)(r)
 = {w : lambda_phi(S)=sigma and lambda_phi(A(w))=alpha}.   (3)
```

Order the nonempty cells by

```text
(1_(p(alpha)+rho(alpha)>0), alpha, -p(sigma), sigma).      (4)
```

The joint cells partition the exact witness incidence and hence form a
witness-exhaustive first-match atlas.  There are at most `(n+1)^8`
profile labels.  The cell predicates have polynomial-size finite-field
descriptions using zero indicators, inverse witnesses for nonzeros, fiber
gates, and binary counters; projecting the auxiliary variables gives
constructible cells.

## Full-agreement-set slope injection

For any witness cell, distinct retained slopes have distinct full
agreement sets.  Indeed, suppose witnesses `(gamma,S,h)` and
`(gamma',S',h')`, with `gamma!=gamma'`, have the same full agreement set
`A`.  Define

```text
f_1 = (h-h')/(gamma-gamma'),
f_0 = h-gamma f_1.
```

Both polynomials have degree less than `k`.  On `A`, they equal `r_1`
and `r_0`, respectively.  Since `S subset A`, they simultaneously
explain the received pair on the noncommon support `S`, a contradiction.
Therefore, for every cell `C`,

```text
|pi_gamma(C)| <= |{A(w):w in C}|.                         (5)
```

The proof uses only retained witnesses, so arbitrary first-match deletion
preserves the injection.

## Exact weighted-cover compiler

Let `Z_(sigma,alpha)^o` be the actual first-match slope set of the joint
cell, restricted to a challenge set `Gamma`.  The fixed-support injection
and (5) give

```text
|Z_(sigma,alpha)^o|
 <= min(|Gamma|,H_phi(sigma),H_phi(alpha)).                (6)
```

Form a bipartite graph whose support vertices are the realized `sigma`,
whose agreement vertices are the realized `alpha`, and whose edges are
the nonempty first-match cells.  Give each vertex its exact occupancy
weight `H_phi`.  If

```text
tau_phi(r,Gamma)
 = min_(K a vertex cover) sum_(v in K) H_phi(v),           (7)
```

then

```text
|Z_a(r) intersect Gamma| <= min(|Gamma|,tau_phi(r,Gamma)). (8)
```

To prove this, assign every edge to one endpoint in a chosen cover.  The
union of slope sets assigned to one support vertex injects into its
supports; the union assigned to one agreement vertex injects into its
full agreement sets.  First-match edge slope sets are disjoint, so summing
the endpoint capacities proves (8).

Taking all support vertices is always a cover.  Exact support add-back
therefore gives

```text
tau_phi(r,Gamma) <= sum_sigma H_phi(sigma)=binom(n,a).      (9)
```

The weighted cover is pointwise never weaker than the integrated support
atlas.

## Complete payment of the agreement-saturated stratum

Call an agreement profile saturated when `p=rho=0`; its full agreement
set consists only of exceptional points and complete `phi`-fibers.  All
slopes first-matched to saturated agreement profiles satisfy

```text
|Z_sat^o(r) intersect Gamma| <= min(|Gamma|,M_phi(a)),      (10)

M_phi(a)
 = sum_(t=0)^b binom(b,t)
   sum_(m=max(0,ceil((a-t)/c)))^N binom(N,m).              (11)
```

This counts the possible full agreement sets directly.  It is independent
of how many fibers the witness support occupies partially.  If every bad
slope has at least one witness with saturated full agreement and these
cells are ordered first, (10) conditionally pays the full line; that
extra hypothesis is not asserted here.

For fixed `c`, `b=o(n)`, and `a/n->beta in (0,1)`,

```text
(1/n) log M_phi(a)
 = (1/c) sup_(theta in [beta,1]) h(theta) + o(1).          (12)
```

Thus the exponent is `log(2)/c` for `beta<=1/2` and
`h(beta)/c` for `beta>=1/2`.

## Growing partial-support example

Let `D=theta H` be an even-order multiplicative coset in odd
characteristic with `-1 in H`, and take `phi(x)=x^2`.  Then `c=2`,
`b=0`, and `N=n/2`.  Choose `k+1<=a<N`, an `a`-set `E subset Q`, and
put

```text
A = phi^(-1)(E).
```

Choose one point from each fiber above `E`, obtaining an `a`-support
`S`.  Define received words

```text
r_0(x)=0 on A and 1 off A,
r_1(x)=x^k,
gamma=0,
h=0.
```

The support is noncommon: if a degree-less-than-`k` polynomial agreed
with `x^k` on `S`, their difference would be a nonzero degree-`k`
polynomial with at least `a>=k+1` roots.  The full agreement set is
exactly `A`.  Hence

```text
lambda_phi(S)=(0,0,a,a),
lambda_phi(A)=(0,a,0,0),

H_phi(lambda_phi(S))=binom(N,a) 2^a,
H_phi(lambda_phi(A))=binom(N,a).                           (13)
```

The full-agreement capacity removes the factor `2^a` from this profile's
certified bound, despite positive-density partial occupancy in the witness
support.  This is a capacity refinement; the example itself has one
displayed slope and is not claimed to reduce the global numerator by a
positive rate.

## Ledger effect and remaining wall

This is strictly beyond open PR #589's set-theoretic full-secant
exhaustiveness and the integrated support-only occupancy atlas.  It adds:

- the full-agreement-set slope injection;
- a polynomial-size joint support/agreement atlas;
- the exact weighted vertex-cover compiler;
- unconditional payment of the complete agreement-saturated stratum.

Hard input A remains open globally.  For an unsaturated full agreement
profile `(t,m,p,rho)`, the exact weight (1) still contains the local
proper-fiber orientation factor.  The next target is an actual-slope
projection theorem removing or paying that factor when `p=Theta(n)`.

## Nonclaims

- No global hard-input-A or profile-envelope closure is claimed.
- The conditional all-slope saturated corollary is not assumed.
- No full-image, minor-arc, major-arc, Sidon, or ray theorem is proved.
- No quotient field-drop is inferred from the direct occupancy count.
- No finite M31 or KoalaBear survivor count changes.
- No deployed adjacent inequality is proved.
- No paper TeX is changed.
