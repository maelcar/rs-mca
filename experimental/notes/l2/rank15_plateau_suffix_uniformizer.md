# Rank-15 plateau-suffix uniformizer

**Status:** PROVED under the imported rank-15 locator-saturation normal form,
the imported proper-section cap `q = 15`, and the pending PR #746 weighted
graph certificate. The proof is field-uniform once those source hypotheses
hold.

Frozen authority:

```text
role ZIP SHA-256:
28b0cf80a46e4116f42a854e3c3495333a191b9016e0e9bd66297ba9b1722614

worker return SHA-256:
6e8b8cb15e6bf4895982cd96319435baae16cf13dea79e34537a0a6401cef2cb
```

## Exact result

Let `F` be a field, let `H subset F` contain

```text
n = 2,097,152
```

distinct points, and let

```text
calA = P_0 + span_F{V_1,V_2} subset F[X]_<K,
K = 1,048,576,
```

be an exact affine two-flat. For a received word `U : H -> F`, put

```text
Z = {x in H : P(x)=U(x) for every P in calA},
u = |Z|,
m = 1,116,047.
```

Assume the source locator-saturation normal form and assume that every proper
coordinate section outside `Z` contains at most `q=15` listed points. Then,
for every

```text
1,043,771 <= u <= 1,043,948,
```

one has

```text
|calA intersect L_m(U)| <= 217.                         (T)
```

Equivalently, no source-realizable 218-point profile exists at any of these
178 exact recurrence states. The proof does not inspect a divisor, Jacobian
syzygy, quotient vector field, or divisorial-status invariant. It therefore
applies separately to both branches used in the targeting ledger:

```text
divisorial-zero branch:       empty on the 178-state interval;
nonzero-divisor branch:       empty on the 178-state interval.
```

The unresolved interval is exactly

```text
1,043,552 <= u <= 1,043,770,                         (219 states)
```

and neither divisorial branch is eliminated there by this theorem.

## Imported source layer

The proof consumes, rather than reclaims, the following source facts.

1. The locator-saturation normal form writes

   ```text
   V_1 = L_Z G A,       V_2 = L_Z G B,       gcd(A,B)=1.
   ```

   If `r` is the number of inactive residual evaluation points and
   `d=max(deg A,deg B)`, then `d <= lambda-r`, where
   `lambda=K-1-u`.

2. For each projective pencil direction `nu`, the number `c_nu` of active
   coordinates with that normal direction satisfies

   ```text
   c_nu <= deg(F_nu) <= d.
   ```

   Select in each represented direction a coordinate line with maximum
   listed-point occupancy `h_nu`. A direction is rich when `h_nu=15`.
   If `t` is the number of rich directions and `b` the number of all rich
   affine lines, then

   ```text
   t <= b <= 218,
   td >= W + 14r.                                      (S1)
   ```

3. Pending PR #746 supplies the weighted graph theorem at `t=b=218`: its
   graph cost `chi` is even and at least eight, and its ten surviving
   `chi=8` skeletons are exactly

   ```text
   (v,c8,k7,k6,k5,u0)
   (18,25,0,2,1,1)  (18,25,1,0,2,1)  (18,25,1,1,0,5)
   (26,24,1,3,0,1)  (26,24,2,1,1,1)  (26,24,3,0,0,5)
   (34,23,3,2,0,1)  (34,23,4,0,1,1)
   (42,22,5,1,0,1)  (50,21,7,0,0,1).
   ```

   Here the assigned point weights are `1/7` on a designated `K7`, `1/3`
   on a designated `K6`, `3/5` on a designated `K5`, one on an unassigned
   residual vertex, and zero on a removed `K8` component. Every non-rich
   coordinate occurrence of occupancy `h` has total point weight at most
   `8-h`.

The proof below uses no conclusion from pending PRs #747--#750. In particular,
the PR #746 fixed state `u=1,043,596,d=4,828` is not being restated.

## Plateau arithmetic

Assume for contradiction that 218 listed points exist. Write

```text
N      = n-u,
a      = m-u,
lambda = K-1-u.
```

For the 397 states `1,043,552 <= u <= 1,043,948`, set

```text
e = 1,045,969-u.
```

Direct substitution gives

```text
N      = e + 1,051,183,
a      = e +    70,078,
lambda = e +     2,606,
W      = 218a-14N = 204e+560,442,
Delta  = 15N-218a = 490,741-203e.                       (1)
```

The rich-direction threshold is therefore

```text
t >= ceil(W/lambda).                                    (2)
```

Indeed, `d+r <= lambda` and (S1) imply

```text
t lambda >= t(d+r) >= W+(t+14)r >= W.
```

## Pair and deficient-point inequalities

The selected lines in distinct projective directions are distinct affine
lines. Every pair of listed parameter points lies on a unique affine line,
so

```text
sum_nu C(h_nu,2) <= C(218,2) = 23,653.                  (3)
```

The `t` selected rich lines spend `105t` pairs. Hence the selected non-rich
lines obey

```text
sum_nonrich C(h_L,2) <= 23,653-105t.                    (4)
```

Now include all rich affine lines, not merely the selected ones. For a listed
point `p`, let `k_p` be the number of rich lines through `p` and put

```text
z_p = 15-k_p.
```

Since every rich line has 15 listed points,

```text
sum_p z_p = 15(218-b) <= 15(218-t).                     (5)
```

Distinct rich lines through `p` cover disjoint sets of 14 other points.
Thus the uncovered-pair graph has degree

```text
217-14k_p = 7+14z_p                                    (6)
```

at `p`. Every selected non-rich line is a clique in this graph. A selected
non-rich line of occupancy at least nine contains only points with `z_p>=1`.
Consequently

```text
sum_{L nonrich, h_L>=9} h_L(h_L-1)
 = sum_p sum_{L contains p, h_L>=9} (h_L-1)
 <= sum_{such p} (7+14z_p)
 <= 21 sum_p z_p
 <= 315(218-t).                                         (7)
```

This is the required `315(218-t)` inequality.

## Six threshold inequalities

Fix `H in {9,...,14}`. Let `k_H` be the number of selected non-rich lines
with occupancy at least `H`, let `I_H` be their total point incidence, and
let `r_p` be the number of those lines through `p`. Equation (6) gives

```text
(H-1)r_p <= 7+14z_p,
z_p >= z_H(r_p) := ceil(max((H-1)r_p-7,0)/14).           (8)
```

For

```text
(c_9,c_10,c_11,c_12,c_13,c_14) = (1,1,1,3,6,21),        (9)
```

the exact inequalities

```text
c_H(r-z_H(r)) <= C(r,2),       0 <= r <= 218,            (10)
```

hold. The verifier derives each `c_H` as the largest integer valid for every
`r`; increasing any one by one fails at a printed witness. It checks all
`6*219=1,314` cases.

Summing (10), using (5), and using the fact that two selected affine lines
meet in at most one point gives

```text
c_H I_H - C(k_H,2) <= 15c_H(218-t),       H=9,...,14.    (11)
```

To see the sign precisely, (8)--(10) imply

```text
c_H r_p-C(r_p,2) <= c_H z_p.
```

After summing over `p`, use
`sum_p C(r_p,2) <= C(k_H,2)` and then (5).

## Exact finite optimizer

The actual incidence is at most

```text
sum_nu c_nu h_nu.
```

For an upper bound, enlarge every direction capacity from `d` to `lambda`,
add the `r` inactive weight units so that the total weight is `N`, and allow
a zero-occupancy direction to have occupancy one. These are relaxations in
the upper-bound direction.

For fixed occupancies, the greedy weight assignment is exact: fill the rich
directions first, then fill the remaining non-rich directions in decreasing
occupancy order. If `t lambda >= N`, this gives the capacity `15N`. Otherwise
write

```text
N-t lambda = f lambda+s,       0 <= s < lambda.          (12)
```

The deployed state range and (2) give `f<=17`. For the full-weight non-rich
directions, let `n_h` count occupancy `h`, `9<=h<=14`. Every high profile is
one of

```text
(n_9,...,n_14),       sum_h n_h <= 17,
```

so the complete profile universe has

```text
C(17+6,6) = 100,947                                  (13)
```

members. If `s>0`, the residual direction has an independently enumerated
occupancy `h_* in {1,...,14}`.

For every profile, residual occupancy, and feasible `t`, the optimizer checks
all of the following exactly:

```text
sum_h n_h C(h,2) + C(h_*,2) <= 23,653-105t,             (14)

sum_h n_h h(h-1)
  + 1_{h_*>=9} h_*(h_*-1) <= 315(218-t),                 (15)

c_H I_H-C(k_H,2) <= 15c_H(218-t),       H=9,...,14.     (16)
```

The residual terms are omitted when `s=0`. For each remaining full-weight
direction of occupancy at most eight, occupancy starts at one and the
successive upgrades cost exactly

```text
1,2,...,7
```

pairs. Spending the remaining pair budget layer by layer is therefore the
exact integer optimum, not a heuristic. A separate literal dynamic program
checks this exchange formula in 2,530 cases.

This produces an exact relaxed capacity `C(u,t)` and

```text
C(u) = max_t C(u,t).                                    (17)
```

Every source-realizable 218-point profile has incidence at least `218a`, so
`C(u)<218a` is a contradiction.

## The `t=218` PR #746 refinement

When `t=218`, (S1) forces `b=t=218`. Equality in the rich point-line
incidence count forces every listed point to lie on exactly 15 rich lines;
the uncovered graph is simple and 7-regular.

For a rich line `ell`, let `e_ell` be its coordinate multiplicity and put

```text
delta_ell = d-e_ell,
epsilon_p = sum_{ell contains p} delta_ell,
delta     = sum_ell delta_ell,
c         = a-15d.                                      (18)
```

Each listed point needs at least

```text
n_p >= c+epsilon_p                                      (19)
```

non-rich coordinate incidences. Let

```text
eta = sum_{L nonrich} (8-h_L),                           (20)
```

with repeated coordinate sections counted with multiplicity.

The imported PR #746 weights have total weight `chi` and satisfy the
per-occurrence inequality `sum_{p in L} w_p <= 8-h_L`. Double counting (19)
therefore gives `eta>=chi*c` before using any extra local slack. If `chi>=10`,

```text
eta >= 10c.                                             (21)
```

For the ten `chi=8` skeletons, `u0` is one or five.

- If `u0=1`, the unique unassigned point lies on no non-rich support of
  occupancy at least five. At occupancy four, the other point weights total
  at most `3*(3/5)`, so every occurrence through it has slack at least

  ```text
  4-(1+9/5)=6/5.
  ```

- If `u0=5`, at most one line contains four unassigned points: two such
  four-subsets of a five-set would share at least three points, while two
  distinct affine lines share at most one. Choose an unassigned point outside
  that possible line. Every non-rich occurrence through the chosen point has
  occupancy at most four and at most two other unassigned points. Its weight
  is at most `1+2+3/5=18/5`, leaving slack at least `2/5`.

The chosen point has at least `c` occurrences by (19), and repeated
occurrences retain their slack. Since `eta` is integral,

```text
eta >= 8c+ceil(2c/5).                                   (22)
```

Equation (21) is stronger than (22), so (22) holds uniformly whenever
`c>0`.

The exact incidence identity is

```text
I = 8(N-r)+1526d-7delta-eta.                            (23)
```

Indeed, the rich coordinates contribute `15(218d-delta)`, while the
non-rich coordinates contribute
`8((N-r)-(218d-delta))-eta`.

Dropping `-7delta` and applying (22) gives

```text
I <= 8(N-r)+1526d-8(a-15d)-ceil(2(a-15d)/5).             (24)
```

Increasing `d` by one lowers `a-15d` by 15 and increases the right side of
(24) by exactly

```text
1526+8*15+6 = 1652.
```

Since `d<=lambda-r`, the maximum is uniquely at `r=0,d=lambda`; one unit of
`r` loses `1652+8=1660`. With

```text
c_0 = a-15lambda,
```

the uniform `t=218` capacity is

```text
I <= 8N+1526lambda-8c_0-ceil(2c_0/5).                   (25)
```

At the first proved state `u=1,043,771`,

```text
N=1,053,381,  a=72,276,  lambda=4,804,  c_0=216,
eta >= 8*216+ceil(432/5)=1,815,
I <= 15,756,137 < 218a=15,756,168.                       (26)
```

The deficit is 31. The complete optimizer remains strict through the right
endpoint:

```text
C(1,043,948)=15,569,720,
218a           =15,717,582,
deficit        =   147,862.                              (27)
```

Thus (T) holds on all 178 states.

## Exact left boundary

At `u=1,043,770`,

```text
N=1,053,382,  a=72,277,  lambda=4,805,  c_0=202.
```

The exact capacity-minus-`218a` margins are

```text
t=210  -8,054    t=211  -8,054    t=212  -3,249
t=213  -3,249    t=214  -1,705    t=215  -6,510
t=216  -6,510    t=217  -1,705    t=218  +1,403.
```

Hence only `t=218` survives the relaxation. Its maximum is attained only at

```text
r=0,       d=lambda=4,805.
```

Losing one degree costs 1,652 and one inactive point costs at least 1,660,
both larger than the residual margin 1,403. From (23), any remaining source
state must satisfy

```text
7delta+eta <= 3,100.                                    (28)
```

This note does not eliminate that branch. In particular, it does not import
a separate projective `218_15` obstruction to move the endpoint left.

## Literal recurrence replay

Let `F_0(z)=1`. The source affine-section recurrence has local candidate

```text
G_d(u) = min(
  floor((n-u)F_{d-1}(u+1)/(m-u)),
  floor((n-u)(m-K+1)/((m-u)^2-(n-u)(K-1-u)))
),
```

where the second term is omitted when its denominator is nonpositive, and

```text
F_d(z) = max_{z<=u<=K-d} G_d(u).                         (29)
```

The raw dimension-two local candidates on the 397-state plateau are

```text
G_2(u)=218 on u=1,043,552..1,043,906 and u=1,043,948;
G_2(u)=219 on u=1,043,907..1,043,947.
```

Apply the theorem by replacing `G_2(u)` with `min(G_2(u),217)` only for
`1,043,771<=u<=1,043,948`, then replay (29) literally. The exact values at
zero are

```text
d   baseline F_d(0)            cut F_d(0)                 drop
2                 219                    218                    1
3               3,185                  3,170                   15
4              46,313                 46,095                  218
5             673,432                670,262                3,170
6           9,792,173              9,746,079               46,094
7         142,383,225            141,712,995              670,230
8       2,070,298,623          2,060,553,260            9,745,363
9      30,102,431,698         29,960,732,756          141,698,942
10    437,687,944,409        435,627,648,441        2,060,295,968
11  6,363,880,388,611      6,333,924,166,895       29,956,221,716
12 92,528,143,984,263     92,092,593,121,126      435,550,863,137
13 1,345,303,004,308,571  1,338,970,359,348,060  6,332,644,960,511
14 19,559,637,074,221,362 19,467,565,446,676,642 92,071,627,544,720
15 284,377,931,860,724,492 283,039,300,733,528,044
                                                1,338,631,127,196,448
```

The deployed target remains

```text
T = 274,854,110,496,187,592.
```

Therefore the dimension-15 gap changes from

```text
9,523,821,364,536,900
```

to

```text
8,185,190,237,340,452.                                  (30)
```

This is a nonzero parent improvement, but it does not close the row.

## Scope against the `c=130..152` Grand Slam family

This theorem uses the original fixed

```text
K=1,048,576,
```

so it is the effective recurrence slice `c=0`. The separate Grand Slam
family uses

```text
K_c=1,048,576-c,       130<=c<=152,
```

with its own `c`-dependent child intervals. The recurrence coordinates are
disjoint, but the theorem classes are nested through

```text
F_p[X]_{<K-c} subset F_p[X]_{<K}.
```

Thus this is a genuinely new 178-state theorem on the original-`K`, `c=0`
slice and a regression certificate on 384 already accepted lower-degree
`(c,u)` rows, since

```text
sum_{c=130}^{152} max(0,U_1(c)-1,043,771+1) = 384.
```

It does not reprove the Grand Slam projective theorem, replace its
`c`-dependent child-plateau proof, or cover its lower interval
`1,043,552..1,043,770`. Conversely, that family is not a premise here and is
not used to extend the boundary (28).

The local demand `c_0=a-15lambda` in (25) is unrelated to the Grand Slam
recurrence-deficit parameter `c`.

## Verification artifacts

The standard-library verifier is

```text
experimental/scripts/verify_rank15_plateau_suffix_uniformizer.py
```

It derives the six threshold coefficients, enumerates all 100,947 high
profiles, checks all 397 capacity states, independently checks the low
optimizer by literal dynamic programming, validates the ten imported
`chi=8` skeleton rows and the `2/5` slack, and replays (29) through `d=15`.
It uses explicit exceptions rather than optimization-sensitive assertions.

Frozen artifacts are

```text
experimental/data/certificates/rank15-plateau-suffix-uniformizer/verifier_output.txt
experimental/data/certificates/rank15-plateau-suffix-uniformizer/capacity_ledger.txt
experimental/data/certificates/rank15-plateau-suffix-uniformizer/recurrence_changes.txt
experimental/data/certificates/rank15-plateau-suffix-uniformizer/fixture.json
```

The capacity ledger prints every `t=210,...,218` capacity and margin at all
397 states. The recurrence ledger is a lossless run-length encoding of every
baseline/cut pair on every row `d=2,...,15`; it is compact but reconstructs
the complete integer rows exactly.

Run

```text
python3 experimental/scripts/verify_rank15_plateau_suffix_uniformizer.py
python3 -O experimental/scripts/verify_rank15_plateau_suffix_uniformizer.py
python3 -m py_compile experimental/scripts/verify_rank15_plateau_suffix_uniformizer.py
```

The first two outputs must be byte-identical to each other and to the frozen
`verifier_output.txt`.

Frozen SHA-256 values:

```text
verifier:
5d048a7327176b12f8cb1f27f51a9d1c0c13a47aff23080e462d460bb0109fe5

verifier output:
969f794e85c676cc80f0f27e81560a6484a9c47533e446fd1322ec6c1ce885f3

capacity ledger:
5091510210060595022fcd04a622319d7da054176369ade0ead0e936d40e20a4

recurrence ledger:
0c4bd290a03e508ec9b73e2d4f223fadf0b4bcf21040512ff7f686742337ab3c

JSON fixture:
fb9966ad9b61c981d9c24e7b09b3609550bba2d0cafbd5dc3461d2741f2bc51c
```

## Nonclaims

This theorem does not:

- solve the 219 residual `M=218` states;
- prove `M<=211`, the eventual rank-15 requirement;
- prove or use the reported syzygy or quotient-vector-field mechanism;
- define a new divisorial invariant or eliminate either branch on the
  residual interval;
- address affine rank at least 16;
- prove the one-row Grand List target;
- supply any of the five missing Grand MCA inputs;
- change the official score from `0/2`.

There is no stable-paper TeX promotion in this packet.
