# Rank-16 global `c=0` first-match ledger

Claim: For one arbitrary received word in the deployed base-field row, three
global first-match owners are disjoint: the canonical agreement-fiber owner,
the exact 110-profile nested-pattern owner, and the canonical-complement
mixed-shadow owner. Their total cap is `96603406772691000`; the residual
allowance is `178250703723496592`, split among exactly `1682` remaining
nested dyadic profiles.
Status: PROVED finite ledger theorem and quantifier repair; the first unpaid
cell and two conditional fixed-core transitions are certified, but no local
cap, parent closure, Grand List theorem, or official score change is claimed.
Verifier: `experimental/scripts/verify_rank16_global_c0_ledger.py` reconstructs
the denominator target, all three owners, both the full and remaining profile
censuses, the first unpaid cell, the sharp zero-lower-cell threshold, and the
uniform-core transitions using only the Python standard library.
Consumers: The rank-16 degree-saturated `c=0` compiler may charge the three
owners once, before any generator, syndrome, or projective-ray partition, and
then attack the exact residual-profile or first-unpaid-cell walls below.
Risk-limits: The fixed-27-core cap `6` and fixed-26-core cap `116` are
conditional hypotheses quantified over every core. Local pencil results such
as open PRs `#826`, `#828`, `#831`, `#833`, and `#834` do not supply either
uniform hypothesis.

## Deployed row and target

All received words, list polynomials, evaluation points, selected agreement
sets, complements, and dyadic fibers in this note live over the base field
`F_p`, where

```text
p = 2130706433,  n = 2097152 = 2^21,
K = 1048576 = 2^20,  m = 1116047,
t = n-m = 981105,  u = 1043459.
```

Let `H <= F_p^x` be the order-`n` evaluation subgroup. The verifier checks
that `p` is prime and `p-1=1016n`, so this subgroup exists. The challenge
denominator is `2^128`; `p^6` is used only in that denominator compiler. It
gives

```text
Bstar = floor(p^6/2^128) = 274980728111395087,
T = floor((((Bstar+1)(p-t))-1)/p) = 274854110496187592.
```

No list theorem over `F_(p^6)` is used or asserted.

For an arbitrary received word `U : H -> F_p`, define

```text
L(U) = {P in F_p[X] : deg(P)<K and |{x in H : P(x)=U(x)}|>=m}.
```

Fix a total order on `H`. For each `P in L(U)`, let `S_P` be the first
exactly `m` agreement points and put `E_P=H\S_P`. Thus every `E_P` has the
same size `t`. This canonical selection is load-bearing for the disjoint
owner ledger.

## Three global first-match owners

For `j=15,...,20`, let `e_j(P)` count complete `2^j`-point fibers contained
in `S_P`. Define the agreement-side owner

```text
D = {e_15=33}
    disjoint-union {e_15=34}
    disjoint-union {e_15<=32 and e_16=16}.
```

The arbitrary-received-word complete-fiber theorem proves

```text
|{e_15=33}|                    <= 55534064877048198,
|{e_15=34}|                    <=  1586961812468508,
|{e_15<=32 and e_16=16}|       <=          601080390,
|D|                            <= 57121027290597096.       (1)
```

Distinct list polynomials satisfy `|S_P intersect S_Q|<=K-1`. Hence they
share at most 31 complete q64 agreement fibers and at most 15 complete q32
agreement fibers. Unique 32-subsets pay `e_15=33`; disjoint radius-one balls
in `J(64,34)` pay `e_15=34`; and unique 16-subsets pay the `e_16=16`
category. Nested fibers give `e_15>=2e_16`, proving that the categories in
(1) are exhaustive in their stated first-match order and disjoint.

Every object outside `D` has a nested profile

```text
(e_15,e_16,e_17,e_18,e_19,e_20) <= (32,15,7,3,1,0),
e_j >= 2e_(j+1).
```

There are exactly 1792 such profiles. The integrated nested-pattern theorem
injects each fixed `e_15=32` profile into its exact 32-of-64 leaf pattern.
Exactly 110 of the 166 `e_15=32` profiles have exact pattern count at most
`121502836610262`; call the corresponding first-match owner `Q110`. The
standard-library replay reconstructs the full binary-tree census and proves

```text
|Q110| <= 904093061906432.                              (2)
```

This is an exact cell sum, not `110` times a uniform cap. Removing the 110
profile cells leaves exactly `1792-110=1682` profiles.

At q64, let `f(P)` count complete 32768-point fibers contained in `E_P`.
Call an `f=28` label set paired when it is the union of 14 natural q32
pairs. On the complement of the first two owners define

```text
M = (L(U)\(D union Q110))
    intersect ({f=29} disjoint-union {f=28 and paired}).
```

Distinct canonical complements satisfy

```text
|E_P intersect E_Q| <= n-2m+K-1 = 913633.
```

Because `27*32768<=913633<28*32768`, their 28-shadows are disjoint. The
mixed-shadow theorem therefore gives

```text
|M| <= binom(32,14)
       + floor((binom(64,28)-binom(32,14))/29)
     = 38578286420187472.                               (3)
```

The definitions of `Q110` and `M` use literal first-match complements rather
than informal subtraction. Equations (1)-(3) are therefore disjoint global
charges for one received word:

```text
|D|+|Q110|+|M| <= 96603406772691000,
A := T-(|D| cap + |Q110| cap + |M| cap)
   = 178250703723496592.                                (4)
```

They are charged once before subdividing the residual list by generators,
syndromes, residue rays, or other local owners.

## Remaining profiles and the first unpaid cell

The 1682 remaining profiles have canonical CSV stream length 22590 bytes and
SHA-256

```text
7dfa0fba111addf8ef4568821e2ce451de094c1ccef5de3468e80bd7e0373cfe.
```

Euclidean division gives

```text
A   = 1682*105975448111472 + 688,
A+1 = 1682*105975448111472 + 689.
```

Thus a list of size at least `T+1` forces one remaining profile to contain at
least `105975448111473` elements. Conversely, a uniform cap
`105975448111472` on every remaining profile leaves total `T-688`.

Within the degree-saturated rank-16 `c=0` branch, descending q64-complement
weight leaves the first unpaid cell

```text
f64=28, non-q32-paired, q64 footprint>=32,
at least 4 extra touched q64 blocks, at most 13 complete q32 blocks.
```

After removing 28 full q64 fibers, its non-full-block residue has size
`981105-28*32768=63601`. Its direct shadow ceiling is
`binom(64,28)-binom(32,14)=1118770292513804288`, far above the residual
allowance.

Let `C=binom(64,28)`, `P0=binom(32,14)`, and let `x` be the first-cell
population. If every later unpaid cell is empty, the current exact
mixed-shadow relaxation after `D` and `Q110` is

```text
Phi(x) = 57121027290597096 + 904093061906432
         + P0 + x + floor((C-P0-x)/29).
```

The sharp threshold is

```text
Phi(184616800285050042) = T,
Phi(184616800285050043) = T+1.                          (5)
```

Equation (5) is a zero-lower-cell threshold, not a standalone cap when later
cells are populated. In general the exact obligation is
`R_later <= T-Phi(x)`.

## Uniform fixed-core transitions

The following statements certify arithmetic implications, not their local
hypotheses. The exact 110-profile owner is charged before the joint top-layer
owner in both computations.

If every fixed 27-label core lies in at most `r` surviving nonpaired `f=28`
label sets, double counting core-set incidences gives

```text
M_28^np <= floor(r*binom(64,27)/28).
```

The joint ledger has the exact transition

```text
r=6: total 271769678181377208, margin  3084432314810384,
r=7: total 300964056749491576, excess 26109946253303984. (6)
```

If every fixed 26-label core lies in at most `r` valid `f=28` two-label
extensions, each 28-set contains `binom(28,26)=378` such cores, so

```text
M_28 <= floor(r*binom(64,26)/378).
```

The exact transition is

```text
r=116: total 274842770207052152, margin   11340289135440,
r=117: total 276379316447479224, excess 1525205951291632. (7)
```

For comparison, the local active-pencil cap `130` gives total
`296354417573031160`, exceeding `T` by `21500307076843568`.

The word `every` in (6) and (7) is essential. A theorem about one selected
core, one generator, or one projective ray cannot be summed over all cores.
Open PR `#826` concerns a fixed root-free generator, one syndrome/projective
residue ray, and one fixed 27-core; it does not prove either uniform cap. The
same global-owner warning applies to the local objects in open PRs `#828`,
`#831`, `#833`, and `#834`; the last retains its canonical classification,
fixed-cell Hahn certificate, and complete cover as explicit inputs.

## Source and novelty audit

For a weighted GRS code with nonzero column multipliers, coordinatewise
division by the multiplier vector preserves all agreements, so the theorem
applies to the normalized arbitrary word `U`. Canonical first-`m` selection
makes the owner order source-realized, disjoint, and exhaustive on the
charged cells. No abstract support family is substituted for a list.

The three producer theorems are already present on `origin/main`:

* `experimental/notes/l2/dyadic_complete_fiber_slicing_route_cut.md`;
* `experimental/notes/l2/profile1792_e15_pattern_payment.md`;
* `experimental/notes/l2/canonical_error_mixed_shadow_packing.md`.

This note does not reclaim any producer. Its new theorem layer is their exact
three-owner first-match composition, the 1682-profile residual census, the
first-unpaid-cell reserve, and the correction from a selected-core statement
to the uniform all-core quantifier required by (6) and (7). The original
two-owner Role 04 arithmetic is superseded by this composition because the
110-profile theorem was already live on `origin/main`.

## Nonclaims and exact remaining wall

This theorem does not prove the fixed-27-core cap `6`, the fixed-26-core cap
`116`, a cap on any remaining profile, a rank-16 parent closure, the all-rank
Grand List theorem, Grand MCA, or an official score change. The score remains
`0/2`.

The exact remaining global wall is a source-valid bound on the first unpaid
nonpaired `f=28` cell and then the later lower cells, or a uniform all-core
theorem strong enough to instantiate (6) or (7). Local results must first be
compiled into that global quantifier before they can be charged.
