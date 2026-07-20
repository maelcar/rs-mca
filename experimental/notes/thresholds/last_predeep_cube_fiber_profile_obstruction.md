# Last-predeep cube-fiber profile obstruction

## Status

**PROVED / COUNTEREXAMPLE / AUDIT / ZERO PAYMENT.** This note records the
independently audited R34 Role 06 theorem layer. It gives an explicit family
of last-predeep Reed--Solomon rows that is target-unsafe, and hence survives
any exclusion that removes exactly the target-safe rows, while every
source-consumed dimension-`(k+1)` O5c profile list is empty or singleton and
its maximum challenge-intersection floor is only one.

This falsifies only the conjunction of a precise target-safe exclusion with a
universal strict profile crossing on every survivor. It is not a replacement
exclusion, a semantic owner theorem, a closed ledger, or a Grand theorem. It
makes no ledger payment and leaves the official score at `0/2`.

The publication base is
`origin/main@9908454995f3f195cfe748f35a1135211609d066`. This note augments PR
`#990`, whose square-field family occupies the exact locus of the one-sided
safe cut below. Live overlap was refreshed through open PR `#993`; no other
open head states the cube-fiber syndrome pencil or this obstruction.

## Source interfaces

The source-consumed objects are:

- the support-wise MCA numerator `B_C,Gamma^MCA(a)`, which counts distinct
  challenge slopes rather than supports or witnesses;
- the weighted Vandermonde parity columns, syndrome-line normal form, and
  exact syndrome--secant compiler;
- the universal tangent floor and overlap--packing upper bound;
- actual lists in `C^+=RS_F(D,k+1)` produced by the identity, quotient,
  Chebyshev, or remainder profiles, followed by collision-aware pole
  conversion and challenge averaging.

The source calls `3r<=R` exact-deep. Here "last-predeep" means the compiled
equality `3r=R+1`, not a separately named source definition. Safe means the
actual numerator is at most `B*`; equality remains safe.

## Cube-fiber theorem

For every integer `s>=65`, put

```text
q = 2^(2s),            F = GF(q),          D = F^*,
n = q-1,               R = 8,              k = q-9,
r = n-a = 3,           a = q-4,            Gamma = F.
```

Then

```text
B_C,Gamma^MCA(a) = (q-1)/3.                              (1)
```

At the frozen target `epsilon*=2^-128`,

```text
B* = 2^(2s-128),
(q-1)/3 > B*.                                             (2)
```

Every source-consumed identity, quotient, Chebyshev, or remainder-profile
list in `C^+=RS_F(D,k+1)` at agreement `a` is empty or singleton. The maximum
list size is exactly one, so collision-aware pole conversion and full-field
challenge averaging give

```text
P_prof = 1.                                                (3)
```

The tangent floor is four. Hence

```text
max(P_prof,4) <= B*
```

for every `s>=65`, with equality at `s=65`.

## Proof of the exact numerator

Because `q=4^s`, one has `3 | q-1`. Let

```text
H = (F^*)^3,
T_c = {x in F^* : x^3=c}       for c in H.
```

The fibers `T_c` are disjoint triples partitioning `D`, and
`|H|=(q-1)/3`. Write the source parity columns as

```text
h_x = lambda_x (1,x,...,x^7)^T,
```

where `lambda_x` is nonzero. In characteristic two the field element `3` is
`1`, in particular nonzero. For each `c in H`, define

```text
w_c = sum_(x in T_c) [1/(3 lambda_x x^2)] h_x.
```

The cube-fiber power sums on the exponent range `-2,-1,0,1,2,3,4,5` vanish
except in exponents zero and three. Therefore

```text
w_c = e_2 + c e_5.                                        (4)
```

Set `y_0=e_2` and `y_1=e_5`. Equation (4) puts the point
`y_0+c y_1` in the syndrome span `V_(T_c)`. Every vector `z in V_(T_c)`
satisfies `z_(j+3)=c z_j` for `0<=j<=4`, whereas `y_1` violates this at
`j=2`. Thus the intersection is transverse. Syndrome surjectivity lifts this
single syndrome line to one received pair, and every `c in H` is an actual
bad challenge slope with agreement support `D\T_c`. This proves the lower
bound `(q-1)/3`.

For the upper bound, `j=3r-R=1`. The source overlap--packing theorem gives

```text
B_C,F^MCA(n-r) <= max(r+1,A(n,r,1)),
A(n,r,1) = floor(n/r) = (q-1)/3.
```

Since `(q-1)/3>4` at the claimed endpoint, the upper equals the constructed
lower, proving (1). The construction counts distinct slopes on one line; it
does not charge repeated supports or witnesses.

## Profile collapse

Two distinct words in `C^+` listed around one received word at agreement
`a` would agree with each other on at least

```text
2a-n = q-7 = k+2
```

coordinates. Their representing polynomials have degree at most `k`, a
contradiction. Thus every ordinary `C^+` list, and therefore every
source-consumed profile sublist, has size at most one.

The maximum is not zero. In the exact-prefix construction take coefficient
field `B=F`, `K=k+1=q-8`, `m=a=q-4`, and `w=m-K=4`. Its positive list floor
has ceiling one. At `L=1`, the pole formula has `q-n=1` and gives `M(1)=1`;
with `Gamma=F`, challenge averaging gives (3).

## Target comparison and impossibility

The endpoint arithmetic is exact:

```text
(q-1)/3 - 2^(2s-128)
  = [2^(2s-128)(2^128-3)-1]/3 > 0
```

for `s>=65`. Every cube row is target-unsafe, while `P_prof=1<=B*`.

Suppose a predicate `Exc` excludes exactly the target-safe rows:

```text
Exc(row) iff B(row) <= B*(row).
```

Every cube row must survive, but a universal surviving requirement
`P_prof>B*` fails there. This contradiction persists even if `Exc` has oracle
access to the exact MCA numerator. It does not apply to future architectures
that source-define additional inadmissible target-unsafe cells or use a
different direct incidence owner.

## One-sided safe cut

On any last-predeep row `R=3r-1` in the source domain, put `G=|Gamma|` and

```text
E = min(G,r+1),
U = min(G,max(r+1,floor(n/r))).
```

The source gives `E<=B<=U`. Therefore

```text
B* >= U                                                   (5)
```

is a sufficient one-sided safe cut. It is exact only where `E=U`, for
example when `G<=r+1` or `floor(n/r)<=r+1`; it is not a complete exact
exclusion in the middle band `E<=B*<U`.

For the PR `#990` square family, `q=2^(2s)`, `r=2^s`, `n=q-1`, and
`R=3r-1`. Then `floor(n/r)=r-1`, so

```text
E=U=B=2^s+1 < 2^(2s-128)=B*       for s>=129.
```

Cut (5) safely removes the square family. The cube family lies in the genuine
middle band and survives, while still defeating the strict profile crossing.

## Replay and audit

Run

```bash
python3 experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --check
python3 -O experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --check
python3 experimental/scripts/verify_last_predeep_cube_fiber_profile_obstruction.py --tamper-selftest
```

Normal and optimized check output must match the checked-in transcript. The
standard-library verifier pins six source files, replays three cube rows and
two square rows through `78` exact gates, and rejects `15` semantic mutations.

Independent hostile-proof audit accepted the theorem above. Its packet and
frozen public-contract SHA-256 values are respectively
`46727f2d7c0f955939f4ee18dafe83456c6f7857bd8a705c420fd6d7b7f7454f`
and `856814fb236ef02e25df41f97dcdf7d69745bf1c79c85cd80426272a25f54700`.
The distinct source/compiler audit returned `ACCEPT_NARROWED`; its packet and
frozen public-contract SHA-256 values are respectively
`01ab70f2be552468fc436db852085f8548c15a16c360aad806e799b7fd9dc158`
and `6666cc0b1043ccfb6544c1d20d611b19ac2b8316a6d00d9d646fbf2fdda5594d`.

The source audit verified the outer packet, original archive, all `82/82`
nested manifest entries, and all `72/72` source hashes. The source corpus has
`43,486` logical lines (`43,484` newline characters), not the worker's
non-load-bearing `43,556` count. No claimant-generated source, output, or
manifest attachment existed; none is certified here.

## Nonclaims and remaining wall

This result proves no semantic C1--C9 owner, first-match assignment,
earlier-owner survival, disjoint global add-back, closed Grand MCA ledger,
Grand MCA theorem, Grand List theorem, deployed scalar upper, recurrence,
finite or asymptotic ledger payment, or official-score movement. It does not
classify the middle band, prove that power fibers are unique, contradict the
safe-side profile envelope, or certify global literature priority.

The exact remaining wall is to replace the false architecture: source-define
which target-unsafe middle-band cells are admissible, give them a direct
incidence owner or prove a residual upper theorem, and compile a
chronology-correct first-match aggregation. The official score remains `0/2`.
