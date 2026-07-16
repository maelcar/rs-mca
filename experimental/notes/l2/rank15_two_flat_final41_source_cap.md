# Rank-15 exact two-flat final-41 source cap

## Status and claim boundary

`PROVED` for the exact source-child interface below.  This note packages the
repaired R26 Role 05 theorem and nothing stronger.

For the deployed parameters

```text
p = 2,130,706,433
n = 2,097,152
K = 1,048,576
m = 1,116,047
```

every exact affine two-flat child whose actual universal agreement count is

```text
1,043,917 <= u <= 1,043,957
```

and whose listed polynomials each have at least `m` agreements contains at
most 211 listed polynomials.  In the rank-15 child ledger this is exactly

```text
D_2(u) <= 211,        1,043,917 <= u <= 1,043,957.       (T)
```

Consequently, only these 41 `D_2` child entries may be replaced by 211.  No
parent recurrence is evaluated or changed in this packet.

The argument is field-uniform: it works over every field `F` containing the
stated `n` distinct evaluation points.  The displayed prime is the deployed
specialization, not an algebraic input to the incidence proof.

## Exact two-flat interface

Let `H subset F` have `n` distinct elements and let `U:H -> F`.  Write

```text
L_m(U) = {P in F[X]_<K : |{x in H : P(x)=U(x)}| >= m}.
```

Let

```text
calA = P_0 + span_F{V_1,V_2}
```

be an exact affine two-flat, so `V_1,V_2` are linearly independent.  Its
actual universal agreement set and its listed points are

```text
Z = {x in H : P(x)=U(x) for every P in calA},   |Z|=u,
S = calA intersect L_m(U),                      |S|=M.
```

For the proof, set

```text
N      = n-u,
a      = m-u,
lambda = K-1-u.
```

The word *actual* is load-bearing.  It ensures that every coordinate outside
`Z` cuts `calA` in either the empty set or a proper affine line, never in all
of `calA`.

## Derivation of the proper-section cap 15

The cap 15 is not left as an unexplained imported number.  Fix `x in H\Z`.
If

```text
calA_x = {P in calA : P(x)=U(x)}
```

is nonempty, it is an affine one-flat.  Its actual universal set contains
`Z union {x}`, and therefore has size at least `u+1`.

The integrated stateful affine-section recurrence gives, for an affine
one-flat with universal count at least `z`,

```text
F_{m,1}(z)
 = max_{z <= v <= K-1}
     min(
       floor((n-v)/(m-v)),
       floor((n-v)(m-K+1) /
             ((m-v)^2-(n-v)(K-1-v)))
     ),                                                   (1)
```

where the second term is read as infinity when its denominator is not
positive.  Exact integer evaluation gives

```text
F_{m,1}(1,043,918) = 15.                                  (2)
```

The function is nonincreasing in its lower endpoint.  Since every state in
(T) has `u+1 >= 1,043,918`, every proper nonuniversal coordinate section has
at most 15 listed points.  The verifier scans the complete range in (1) for
all 41 states; it does not use a floating-point approximation.  Passing from
`S` to any 212-point subset can only decrease these section occupancies.

## Source pencil and incidence demand

Assume for contradiction that `M >= 212`, and select 212 points from `S`.
Use their affine parameters `(s,t)` in the displayed basis of `calA`.

Let `L_Z` be the monic locator of `Z`.  Factoring the two directions and then
their monic gcd gives

```text
V_1 = L_Z G A,       V_2 = L_Z G B,       gcd(A,B)=1.
```

Let

```text
d = max(deg A,deg B),
r = |{x in H\Z : G(x)=0}|.
```

The source degree ledger gives

```text
d <= lambda-r.                                           (3)
```

The `r` coordinates are inactive: if the base polynomial agreed there, the
coordinate would belong to the actual universal set.  At every active
coordinate `x`, division by `L_Z(x)G(x)` gives the literal affine parameter
line

```text
ell_x = {(s,t) in F^2 : sA(x)+tB(x)=omega_x}.             (4)
```

For each represented projective normal direction `nu`, let `c_nu` be its
number of active coordinates, and choose among its parallel lines one with
maximum selected-point occupancy `h_nu`.  Coprimality makes each nonzero
direction polynomial have degree at most `d`, so

```text
1 <= h_nu <= 15,
0 <= c_nu <= d,
sum_nu c_nu <= N-r.                                      (5)
```

Each selected polynomial has at least `a` residual agreements.  Hence

```text
212a <= sum_active_x |S intersect ell_x|
     <= sum_nu c_nu h_nu.                                (6)
```

Increasing the per-direction weight ceiling from `d` to `lambda` and the
total weight from `N-r` to `N` is a relaxation in the upper-bound direction.
It is therefore enough to upper-bound (6) subject to

```text
0 <= c_nu <= lambda,       sum_nu c_nu = N.               (7)
```

## Partial-linear-space budgets

Let `n_h` be the number of selected maximum lines having occupancy `h`.
Lines from distinct projective directions are distinct affine lines, and a
pair of selected points lies on at most one selected line.  Therefore

```text
sum_{h=1}^{15} C(h,2)n_h <= C(212,2) = 22,366.            (8)
```

For a selected point `p`, let `r_h(p)` count the selected `h`-point lines
through `p`.  Distinct lines through `p` use disjoint sets of other points,
so

```text
sum_{h=2}^{15} (h-1)r_h(p) <= 211.                        (9)
```

Put

```text
delta_p = 211-sum_{h=2}^{15}(h-1)r_h(p),
x_p     = r_15(p).
```

The exact congruence consequence of (9) is

```text
x_p <= 3+12delta_p+sum_{h=2}^{13}(14-h)r_h(p).           (10)
```

Indeed, the right side is at least 3, is congruent to `x_p` modulo 13, and
`x_p <= floor(211/14)=15`; it cannot be 13 below `x_p`.  If `U_0` is the
number of uncovered pairs, then `sum_p delta_p=2U_0`.  Summing (10) and using
(8) yields

```text
195n_15 + 168n_14
  + sum_{h=3}^{13} h(h-2)n_h <= 41,340.                  (11)
```

Three further pointwise inequalities are used:

```text
C(r_15,2)+1080-79r_15-65r_14
  -sum_{h=4}^{13} C(h-2,2)r_h >= 0,                     (12)

C(r_14,2)+1170-78r_15-78r_14
  -sum_{h=4}^{13} C(h-2,2)r_h >= 0,                     (13)

C(r_15,2)+870-sum_{h=4}^{15} gamma_h r_h >= 0,          (14)
```

where

```text
(gamma_4,...,gamma_15)
  = (1,3,6,10,15,21,27,33,39,45,51,65).
```

These are finite integer-knapsack lemmas, not sampled inequalities.  For a
distinguished count `j` of the target occupancy `t`, the remaining point
capacity is `211-(t-1)j`.  If `Q_t(c)` denotes the maximum remaining charge,
the recurrence

```text
Q_t(c) = max(Q_t(c-1),
             max_{h != t, h-1 <= c}(Q_t(c-h+1)+charge_h))
```

checks every capacity from 0 through 211.  The verifier checks all 16 target-15
counts for (12), all 17 target-14 counts for (13), and all 16 target-15
counts for (14).

Two lines in one occupancy class meet in at most one selected point.  Thus

```text
sum_p C(r_15(p),2) <= C(n_15,2),
sum_p C(r_14(p),2) <= C(n_14,2).
```

Summing (12)--(14) gives the global budgets

```text
C(n_15,2)+228,960-1185n_15-910n_14
  -sum_{h=4}^{13} hC(h-2,2)n_h >= 0,                    (15)

C(n_14,2)+248,040-1170n_15-1092n_14
  -sum_{h=4}^{13} hC(h-2,2)n_h >= 0,                    (16)

C(n_15,2)+184,440-975n_15-714n_14
  -sum_{h=4}^{13} h gamma_h n_h >= 0.                   (17)
```

## Exact directional-weight optimizer

Write

```text
N = f lambda+s,       0 < s < lambda.
```

For fixed occupancies, the exact maximum in (7) gives weight `lambda` to the
`f` largest occupancies and weight `s` to one residual occupancy `h_*`.
The optimizer enumerates `h_* in {1,...,15}` and the numbers of full-weight
occupancies 15 and 14.  Every remaining full-weight occupancy lies in
`[h_*,13]`.  Budgets (8), (11), and (15)--(17) then determine its exact
maximum total occupancy.

The balancing step is justified by the following formal lemma.

### Discrete-convex exchange lemma

Let `Phi_1,...,Phi_b` be integer functions on `{q,...,H}` whose forward
differences

```text
Delta_j(h) = Phi_j(h+1)-Phi_j(h)
```

are nondecreasing in `h` for every `j`.  Among all `k`-tuples
`(x_1,...,x_k)` in `{q,...,H}^k` with a fixed sum, the tuple whose entries
differ by at most one weakly minimizes every resource sum
`sum_i Phi_j(x_i)` simultaneously.

*Proof.*  If `x_i >= x_l+2`, replace `(x_i,x_l)` by
`(x_i-1,x_l+1)`.  The total occupancy is unchanged, while resource `j`
changes by

```text
-Delta_j(x_i-1)+Delta_j(x_l) <= 0.
```

Repeating this exchange terminates at the unique balanced multiset for the
fixed sum.  Thus, if the balanced multiset with one more unit violates any
resource budget, every tuple with that larger sum violates a budget.  This
also proves that completing one whole occupancy layer before entering the
next is an exact optimizer, not a heuristic.  QED.

Here the four resource functions on occupancies `1,...,13` are

```text
Phi_pair(h) = C(h,2),
Phi_mod(h)  = 0 for h<=2, and h(h-2) for h>=3,
Phi_cut1(h) = 0 for h<=3, and hC(h-2,2) for h>=4,
Phi_cut2(h) = 0 for h<=3, and h gamma_h for h>=4.
```

Their forward differences are componentwise nonnegative and nondecreasing.
The verifier checks every difference and, for every optimizer branch, checks
that the returned balanced tuple is feasible while its one-unit successor is
infeasible unless the occupancy ceiling 13 has been reached.

## Certificate result

Let `C(u)` be the maximum relaxed incidence produced by the exact optimizer.
The contradiction margin is

```text
margin(u) = C(u)-212(m-u).
```

The exact margins on the claimed interval are:

```text
u         margin       u         margin       u         margin
1043917     -842       1043931   -20469       1043945   -42175
1043918    -2562       1043932   -21061       1043946   -43670
1043919    -4282       1043933   -21653       1043947   -45165
1043920    -6002       1043934   -22245       1043948   -46660
1043921    -7722       1043935   -22837       1043949   -48104
1043922    -9442       1043936   -24896       1043950   -48919
1043923   -11162       1043937   -27522       1043951   -49734
1043924   -12882       1043938   -30148       1043952   -50549
1043925   -14598       1043939   -32774       1043953   -51364
1043926   -15867       1043940   -34700       1043954   -52179
1043927   -17136       1043941   -36195       1043955   -52994
1043928   -18405       1043942   -37690       1043956   -54129
1043929   -19285       1043943   -39185       1043957   -56079
1043930   -19877       1043944   -40680
```

Every margin is negative, contradicting (6).  This proves (T).

The immediately preceding state is not closed:

```text
margin(1,043,916) = +878.                                (18)
```

The `+878` is the immediate wall.  It is a feasible margin only in the
relaxation; it is neither a source construction nor a counterexample.

## Verifier and C++ translation boundary

The external Pro return embedded a C++17 verifier.  It uses only standard
library containers and exact signed-integer arithmetic to check the three
local knapsacks, run the layer optimizer, and print the boundary plus all 41
margins.  The source was inspected before translation.  It was not compiled
on this host because the Apple developer tools are unavailable.

The packet verifier

```text
experimental/data/certificates/rank15-two-flat-final41-source-cap/
  verify_rank15_two_flat_final41_source_cap.py
```

is a theorem-relevant transliteration into standard-library Python.  Python
integers replace C++ `long long`; lists replace the knapsack vectors; tuples
and dictionaries replace the finite pattern cache; and explicit exceptions
replace `runtime_error`.  It independently adds the rank-one section-cap
scan, strict certificate parsing, discrete-convexity checks, frozen-output
checks, normal/optimized byte-parity support, and tamper controls.

The Pro return also contained one additional candidate local cut explicitly
marked as unused in the 41-state theorem.  That cut and its proposed next
optimizer are deliberately excluded here.  The Python packet reproduces
exactly the cuts and margins consumed by (T), without promoting the next-wall
route.

## Provenance

```text
authority base:
  origin/main@9c4ca98cf45639407611a3ad5154893fb22e77e2

external theorem worker:
  ChatGPT Pro
  conversation 6a58d6f0-b38c-83ec-bd3b-a5147d11f66d
  captured 2026-07-16T16:17:14.368Z
  full rendered SHA-256
  75b5fbc66360d71520e68fae25bc01f26f1d80c9904b5ef1d689b59f57da4d42
  final response SHA-256
  aba0ebd890ad84cae68b47298b462a2a8e87d39a5b722382d98841249f38ce94

native hostile audit:
  ACCEPT_HOLD_REPAIR, confidence 0.93
  gpt-5.6-sol xhigh
  agent 019f6bd4-2657-7283-be04-cf4b4c7c03cc
```

The overlap baseline supplied for packaging includes PRs `#826`, `#838`,
`#843`, and `#844`.  This source-child theorem is stated independently of
their arrangement, rank-16, or global-ledger claims.

## Nonclaims

This packet does not prove or claim:

- `D_2(u) <= 211` for `1,043,592 <= u <= 1,043,916`;
- closure of all 366 rank-15 children;
- any source counterexample or realizable profile at `u=1,043,916`;
- any parent recurrence saving or the 261-parent target;
- any source-to-arrangement transport or conditional arrangement result;
- any rank-16 result;
- any Grand List or Grand MCA theorem;
- any official-score movement.
