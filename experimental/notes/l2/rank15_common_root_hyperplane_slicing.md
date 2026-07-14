# Rank-15 common-root hyperplane slicing

**Status:** `PROVED` for the narrow theorem `R15-HYP14-ROOT-SLICE` below.
The application to the unpublished R13 residual-state ledger is
`CONDITIONAL`. This note proves no rank-15 list bound and eliminates no
complete `(u,c)` state.

## Claim boundary and provenance

This packet was built from

```text
origin/main@9262f63cf093a7510a2df435f220390f59e2bcd5.
```

The load-bearing integrated import is the stateful affine-section theorem in
`experimental/notes/l2/affine_section_one_row_rank_reduction.md`, SHA-256
`3d2c7c3687d2fa4b6202e8de87f64f4e619d427183e23d91a2f1cde9b6451c31`.
Its source verifier has SHA-256
`b17b9c74cd849bd2c2cbbd367c9bfe26ffd3657d099559f9fb431406715196c1`.
The base one-row target is imported through
`experimental/notes/l2/affine_interleaved_shell_compression.md`, SHA-256
`739fc8bc75839086deb3561aa07104f7a427a1aecb225d2cf43ff5654861efdb`.

The R13 rank-15 hybrid recurrence at
`0e776db208da795930d343dca4343f815f258c28` is not in `origin/main` and is not
promoted here. It is used only in the explicitly conditional section
"Residual-ledger consumer" to say where the standalone theorem would apply
if that recurrence packet is accepted. The slicing theorem itself does not
use the R13 hybrid recurrence.

The R14 Role 03 worker return has SHA-256
`d9f28077534f9d9aab30f9a7b69b9df57c40cbf3bb45843b72a10e97b2c213a7`.
Its broad route-cut language is not authority. This packet retains only the
hostile-audit-cleared slicing theorem and exact supporting diagnostics.

## Object and field ledger

The object is a base-field one-row Reed--Solomon agreement list, not MCA, CA,
line decoding, or an extension-field list. The deployed constants are

```text
p = 2,130,706,433 = 2^31-2^24+1,
n = 2,097,152,
K = 1,048,576,
m = 1,116,047,
T = 274,854,110,496,187,592.
```

The target ledger keeps the sextic denominator separate:

```text
q_list = p^6
       = 93,571,093,019,388,561,295,270,373,781,649,880,353,786,165,192,103,559,169,
B       = floor(q_list/2^128)
        = 274,980,728,111,395,087,
D       = p-n+m = 2,129,725,328,
T       = floor(((B+1)D-1)/p).
```

The factor `p` in the theorem below counts the `p` cosets of a base-field
direction hyperplane. It is not an extension-field transfer and does not
produce an extension-field factor-`p` statement.

## Normalized rank-15 state

Let the residual evaluation domain contain `N=n-u` distinct points of
`F_p`, let the residual agreement threshold be `a=m-u`, and put

```text
k_A = K-u-c,             0 <= c <= 152.
```

Let

```text
calA = Q_0 + W subset F_p[X]_{<k_A}
```

be an exact affine `15`-flat, where `dim W=15` and `W` is primitive: its
polynomial gcd is one. In particular, every residual evaluation functional

```text
v_x: W -> F_p,           v_x(w)=w(x),
```

is nonzero. Let `M` be the number of points of `calA` agreeing with the
residual received word on at least `a` coordinates.

For `J in Gr(14,W)`, define

```text
R_J = {x : w(x)=0 for every w in J},
r_J = |R_J|.
```

## Theorem R15-HYP14-ROOT-SLICE

For every normalized state above and every `J in Gr(14,W)`,

```text
r_J >= k_A-4,985
```

implies

```text
M <= p * 20,008,483
  = 42,632,203,442,671,139
  < T.
```

The exact target slack is

```text
T-42,632,203,442,671,139
  = 232,221,907,053,516,453.
```

Consequently every target violator satisfies, simultaneously for every
`J in Gr(14,W)`,

```text
r_J <= k_A-4,986 = 1,043,590-u-c.                         (1)
```

### Proof

Fix `J` and choose `h in W\J`. The affine `15`-flat is the disjoint union of
the `p` affine `14`-flat fibers

```text
calA_alpha = Q_0 + alpha h + J,          alpha in F_p.
```

For every `x in R_J`, primitivity gives `h(x) != 0`; otherwise all of `W`
would vanish at `x`. Hence exactly one `alpha` has

```text
Q_0(x)+alpha h(x)=U(x).
```

Write `z_alpha` for the number of such roots assigned to the fiber. Then
`sum_alpha z_alpha=r_J`. On `R_J`, every point of a fixed fiber either agrees
or disagrees together, because every direction in `J` vanishes there. A
listed point in that fiber therefore has at least

```text
a-z_alpha >= a-r_J
```

agreements outside `R_J`.

Every polynomial in `J` is divisible by the locator `L_{R_J}`. Puncturing
`R_J` and dividing the direction space by this locator injects the listed
part of the fiber into a rank-14 affine-section row

```text
(N-r_J, k_A-r_J, a-r_J).                                  (2)
```

Put `k'=k_A-r_J`. Under the theorem hypothesis, `k'<=4,985`.
For fixed `c`, the row (2) is a shifted state of the boundary row

```text
(n-(K-c-4,985), 4,985, m-(K-c-4,985)).                    (3)
```

Indeed, shifting (3) by `4,985-k'` produces exactly (2). The integrated
stateful rank-14 recurrence is a suffix maximum over every such additional
universal shift, so its value at the boundary row bounds every `k'<=4,985`
row with the same `c`.

The exact scan of (3) over `0<=c<=152` gives

```text
max F_14 = 20,008,483,
argmax   = c=0, shifted state 1,043,591.
```

Thus each of the `p` disjoint fibers contains at most `20,008,483` listed
points. Summing the fibers proves the theorem. Negating the integer trigger
gives (1).

### Exact 4,985/4,986 boundary

The same recurrence scan with boundary ceiling `4,986` gives

```text
max F_14 = 290,933,620,
argmax   = c=0, shifted state 1,043,590,
p * max F_14
  = 619,894,135,709,977,460
  = T+345,040,025,213,789,868.
```

Therefore `4,985` is the exact ceiling paid by this rank-14 slicing compiler.
This is not a claim that the threshold is globally optimal under stronger
RS or projective information.

## Exact annihilator identities

These identities explain the overcounting issue but are not a rank-15 bound.
For a 15-coordinate set `X`, put

```text
K_X = {w in W : w(x)=0 for every x in X},
s(X) = dim K_X.
```

Primitivity gives `0<=s(X)<=14`. The normal set is dependent exactly when
`s(X)>0`. If

```text
A_s = (p^s-1)/(p-1),
```

then the exact positive fractional identity is

```text
1_{s(X)>0} = sum_{ell<=K_X, dim ell=1} 1/A_{s(X)}.         (4)
```

An integral first-owner rule exists after choosing a total order on the
projective lines and assigning `X` to the least annihilating line. The choice
is arbitrary: this does not construct a canonical order-independent integral
owner.

For any selected agreement support `E`, exact subspace-lattice inversion gives

```text
dep_15(E)
 = sum_{j=1}^{14} (-1)^(j+1) p^(j(j-1)/2)
     sum_{J in Gr(j,W)} C(|E intersect Z(J)|,15).          (5)
```

For nullity `s`, the coefficient of one set `X` is one because

```text
sum_{j=0}^s (-1)^j p^(j(j-1)/2) [s choose j]_p = 0,
1 <= s <= 14.                                             (6)
```

The verifier evaluates all 14 identities with exact integers. Formula (5) is
an alternating equality. Discarding its negative terms does not give a valid
upper bound.

## Residual-ledger consumer

This section is conditional on the unpublished R13 recurrence packet. It is
not an `origin/main` theorem.

Under that packet, a target violator in the `c<=151` sector must satisfy

```text
1,042,375 <= u <= 1,043,582,
0 <= c <= 151,
u+c <= 1,043,588,
e_14 >= 4,986,
e_15 >= 4,987,
Delta(W) >= 9,946.
```

The `u+c` restriction is the exact feasibility consequence of
`e_15=k_A-1>=4,987`. There are exactly `173,031` admissible `(u,c)` pairs,
not the full rectangle. Combining this restriction with (1) gives

```text
r_J <= 1,043,590-u-c.                                     (7)
```

In particular,

```text
u+c >= 1,043,576  =>  r_J <= 14.
```

A nullity-14 dependent 15-set would have its 15 coordinates inside the
common-root set of its 14-dimensional kernel. Thus the nullity-14 stratum is
empty on this diagonal tail. Nullities `1,...,13` remain unpaid, and outside
the diagonal tail nullity 14 also remains possible under the cap. No state is
eliminated.

For the four conditional `c=152` states, (1) gives

```text
u = 1,043,403, 1,043,404, 1,043,405, 1,043,406,
max r_J = 35, 34, 33, 32,
```

respectively. This does not close any of those states.

## Scalar first-owner/pair-owner route cut

Let `M_*=T+1`. Select exactly `a` agreement coordinates for each listed point,
and for a coordinate `t`-set `X` let `m_X` be the number of selected supports
containing it. First-copy ownership and pair counting give

```text
M_* C(a,t)
 <= C(N,t) + C(M_*,2) C(e_15,t).                           (8)
```

The right side is monotone in the scalar degree cap `e_15`. For the conditional
`c<=151` ledger, its smallest numerical envelope is therefore obtained at the
floor `e_15=4,987`. Across the actual `173,031` states, the exact slacks in
(8) are positive for every `1<=t<=15`. Anchors are

```text
t=1 minimum slack
  = 188,370,914,058,257,997,774,318,657,802,052,693,917,

t=15 minimum slack
  = 386,242,437,123,153,995,744,635,441,380,151,300,823,492,215,375,917,507,473,244,365,317,144,618,847,448.
```

The canonical digest of all 15 minima is
`cbf513b131ec9c5d4801fe6cf40e645e7bc2e76149ac346a4acd0b2fd1686655`.
For `t>=16`, the pair-free baseline already has minimum `t=16` slack

```text
102,299,617,521,666,695,635,180,302,935,214,543,229,533,401,125,480,618,311,404,559,696,608,496,083,337,903,981 > 0.
```

The ratio `C(N,t)/C(a,t)` increases with `t` because `N>a`, so the baseline
persists for every larger `t`. The same lower-envelope scan is positive on
the four `c=152` states; its digest is
`2018e9fe37731696572a2a94a1506a8e7fd48b77ed0713d78215ca075ad283ab`.

This cuts only the scalar degree-cap version of (8), and every nonnegative
linear combination of those same failed scalar inequalities. It does not cut
a refinement using actual pair intersections, kernel rank, or simultaneous
polynomial geometry.

## Literal 15-point construction

The construction certifies that raw normal-by-normal charging can overcount
one dependent coordinate set by every projective line in a 14-dimensional
kernel. It is not a target-sized counterexample.

Let

```text
omega = 3^1016 mod p = 1,213,133,211.
```

The verifier checks that `omega` has exact order `n=2^21`. Write
`H={omega^i:0<=i<n}`. At

```text
u=1,043,576, c=0, N=1,053,576, a=72,471, k_A=5,000,
```

take exponent intervals

```text
Z = [0,1,043,576),
R = [1,043,576,1,048,562),             |R|=4,986,
A_i, i=1,...,15: consecutive disjoint blocks of size 67,485
                 beginning at exponent 1,048,562.
```

The last block ends at exponent `2,060,837`, leaving `36,315` unused domain
points. Let `L_Z,L_R` be the corresponding monic locators and set

```text
W = span{1,L_R,XL_R,...,X^13 L_R},
V = L_Z W.
```

The pivot degrees of `W` are

```text
0,4,986,4,987,...,4,999.
```

Thus `dim W=15`, `gcd(W)=1`, `e_14=4,998`, `e_15=4,999`, and
`Delta(W)=69,790`. Multiplication by `L_Z` gives maximum direction degree
`u+4,999=K-1`.

For `i=1,...,15`, put

```text
P_i = i L_Z L_R.
```

Define the received word to be zero on `Z`, `R`, and the unused coordinates,
and to equal `i L_Z L_R` on `A_i`. Since the locators are nonzero off
`Z union R` and `1,...,15` are distinct nonzero field elements, the exact
agreement set of `P_i` is

```text
Z union R union A_i,
```

of size

```text
1,043,576+4,986+67,485 = 1,116,047 = m.
```

At each `x in R`, the evaluation normal relative to the displayed basis of
`W` is `(1,0,...,0)`. Every 15-subset of `R` therefore has normal rank one
and kernel dimension 14. The exact counts are

```text
C(4,986,15)
  = 21,909,367,009,365,612,697,041,153,239,017,239,432,249,840,

A_14
  = 18,655,505,543,855,076,173,051,281,507,835,148,948,133,897,313,976,697,647,355,004,502,028,942,208,827,858,988,228,827,455,801,108,637,563,665,580,574,155,735,054.
```

An unweighted sum over annihilating projective directions counts each such
coordinate set `A_14` times. Across the 15 displayed points, the true
dependent incidence and first-copy excess are

```text
15 C(4,986,15)
  = 328,640,505,140,484,190,455,617,298,585,258,591,483,747,600,

14 C(4,986,15)
  = 306,731,138,131,118,577,758,576,145,346,241,352,051,497,760.
```

Only 15 listed points are certified. Nothing here approaches `T+1`.

## Novelty and live overlap

The live pull-ref audit on 2026-07-13 reached `#741`. Those threshold-wave
heads are now integrated in `origin/main@9262f63cf093a7510a2df435f220390f59e2bcd5`.

- PR `#733` at `db323972ea22dca0fecda4d2da6ebcb4c664b574` is cross-credited.
  It raises the adjacent deployed `M=218` locator-pencil degree floor to
  `d>=4,828`. It neither states nor proves a codimension-one common-root
  slicing theorem, and this packet does not reclaim its degree-floor result.
- PR `#734` at `fbcb0b53e010e7dcbb53d07ef3dbf9127217da5a` is a one-deeper
  prefix-to-anti-host MCA compiler and does not overlap this base one-row
  theorem.
- PR `#735` at `f94d8706ae95e99462038e6d462a34332865be02` concerns heavy prefix
  planted/saturation precursors and does not overlap this theorem.
- PR `#736` at `97e2713f880c856ed4dace2440567cc11740ac57` is a pay-per-bit ledger
  audit and board classification. It mentions the integrated rank-15 normal
  form and classifies PR `#733`, but contains no common-root slicing theorem.
- PR `#737` at `8fcd4152709889da768ec1453d05ec09bccfb41a` proves global and
  nested affine-core set-pair charges for retained LineRay pairs. It is a
  different threshold route and does not overlap this common-root slicing
  theorem.
- PR `#738` at `72f559a5822ef00508a6fc7f8f772dfb14a31ed0` audits the printed
  conditional 86-bit pay-per-bit branch across deployed rows. It is an exact
  hypothesis audit and does not overlap this common-root slicing theorem.
- PR `#739` at `1e8b9871de0f89c87c0d7339218e619fb6d57ae5` gives an exact
  staircase-concentration route cut on the Sidon-paired class. It concerns
  asymptotic prefix fibers and does not overlap this finite common-root theorem.
- PR `#740` at `0c7e2bec70bc1aef1c49e20f4341a43a6d85e991` certifies the deployed
  C9 full-slice odd-monomial Fourier budget. It is an analytic prefix-flatness
  certificate and does not overlap this common-root slicing theorem.
- PR `#741` at `299e8160b51d8b45d205ae6978b3b97696dcb83f` extends
  direction-distance bounds to all retained LineRay pairs. It advances the
  balanced-core residual-ray track and does not overlap this finite list-side
  common-root theorem.

The novelty decision is `NARROW_PR_CANDIDATE_ONLY`: the theorem object
`R15-HYP14-ROOT-SLICE` and its replayable boundary certificate are new against
the checked base and live heads. Any title or body claiming rank-15 closure,
state payment, or official movement must be refused.

## First missing wall

For selected 15-sets define `m_X` as above. A target contradiction at
`M_*=T+1` would follow from the positive, non-overcounting bound

```text
sum_{X:s(X)>0} (m_X-1)
  < M_* C(a,15)-C(N,15).                                  (9)
```

The first unpaid task is to prove (9) after stratifying by the full kernel
`K_X`, especially nullities `1,...,13`, using simultaneous RS/projective
realizability. Formula (5) may recover exact nullity strata, but its negative
terms cannot be discarded. The circuit stratum `s(X)=1` is already uniquely
owned and is the first sharp aggregate wall. The slicing theorem pays only a
large-common-root codimension-one branch; it does not supply (9).

Rank at least 16 is a separate unpaid wall.

## Required nonclaims and publication gate

This packet makes all of the following nonclaims:

- no rank-15 bound;
- no paid `(u,c)` state;
- no `c=152` closure;
- no canonical order-independent owner;
- no extension-field factor-`p` claim;
- no unsigned-Mobius upper bound;
- no target-sized counterexample;
- no score movement.

The official score remains `0/2`. No stable paper TeX is changed. No push or
pull request is part of this packet.

## Reproducibility

The certificate is

```text
experimental/data/certificates/rank15-common-root-hyperplane-slicing/
  rank15_common_root_hyperplane_slicing.json
```

Replay with

```text
python3 experimental/scripts/verify_rank15_common_root_hyperplane_slicing.py --check
python3 -O experimental/scripts/verify_rank15_common_root_hyperplane_slicing.py --check
python3 experimental/scripts/verify_rank15_common_root_hyperplane_slicing.py --tamper-selftest
python3 -m py_compile experimental/scripts/verify_rank15_common_root_hyperplane_slicing.py
python3 experimental/scripts/verify_affine_section_one_row_rank.py
```

The new verifier is standard-library only and uses always-active explicit
checks. Normal and optimized check output must be byte-identical. The saved
normal output is `verifier_output.txt` beside the JSON certificate.
