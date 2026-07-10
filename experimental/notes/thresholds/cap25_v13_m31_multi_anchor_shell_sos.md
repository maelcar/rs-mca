Continues the finite M31 prefix-fiber program beyond exact two-shell families.

# M31 multi-anchor shell-pair SOS and arbitrary-shell first-two-distance wall

**Status:** `PROVED` for the shell-pair PSD identities, global tail
inequalities, and the stated first-two-distance cells; `OPEN` for the remaining
cells, aggregation to a max-fiber bound, and the deployed M31 row.

**Verifier:**
`experimental/scripts/verify_m31_multi_anchor_shell_sos.py` (zero argument,
stdlib only, exact integer arithmetic).

## 1. Shell-pair sum of squares

Let `F` be a family of `m`-subsets of an `n`-set and write

```text
d(A,B)=m-|A intersect B|,  R=m(n-m).
```

Fix an anchor `A`.  For arbitrary real coefficients `c_B`, define

```text
S_A(c) = sum_(B != A) c_B(1_B-1_A),
q_A(c) = sum_(B != A) c_B d(A,B).
```

For `i in A`, let `Q_i` be the weighted deletion load, and for `i not in A`,
let `P_i` be the weighted addition load.  Then

```text
R |S_A(c)|^2-n q_A(c)^2
 = (n-m) sum_{i<j in A}(Q_i-Q_j)^2
   + m sum_{i<j outside A}(P_i-P_j)^2 >= 0.               (1)
```

For each realized anchor distance `e`, put

```text
H_e(A) = {B: d(A,B)=e},
h_e(A) = |H_e(A)|,
z_e(A) = sum_(B in H_e(A))(1_B-1_A).
```

Equation (1) says that the complete shell-pair matrix

```text
K_A(e,f)=R z_e(A).z_f(A)-n e f h_e(A)h_f(A)              (2)
```

is positive semidefinite.  If

```text
t_A(e,f,g)=|{(B,C) in H_e(A) x H_f(A): d(B,C)=g}|,
```

then its exact triple-intersection form is

```text
K_A(e,f)=sum_g (R(e+f-g)-n e f)t_A(e,f,g).                (3)
```

Thus both the direct sum over anchors and the summed global matrix are PSD.
Unlike the scalar anchored cut integrated from PR #529, (2)-(3) retain all
off-diagonal interactions between distinct shells.

## 2. Shell-union and global tail inequalities

Suppose the two smallest positive distances are `e1<e2`, and every
one-distance subfamily at `e1` has size at most `r`.  For any anchor-neighbor
set `U`, put

```text
h=|U|,  q=sum_(B in U)d(A,B).
```

Write `h=ur+s`, `0<=s<r`, and

```text
tau_r(h)=s*C(u+1,2)+(r-s)*C(u,2).
```

Turán's theorem inside `U`, followed by (1), gives

```text
nq^2 <= R(2hq-e1 h(h-1)-2(e2-e1)tau_r(h)).                (4)
```

This applies to every union of anchor shells.  Summing (4) over anchors and
using weighted Cauchy-Schwarz gives, for a set `I` of shell distances,

```text
n Q_I^2
 <= R H_I(2Q_I-e1(H_I-M_I)-2(e2-e1)Xi_I),                (5)
```

where `H_I` and `Q_I` are the global incidence and distance sums, `M_I` is
the number of active anchors, and

```text
Xi_I=sum_A tau_r(h_I(A))/h_I(A).
```

The distribution-only relaxation is

```text
n Q_I^2 <= R H_I(2Q_I-e1 max(H_I-|F|,0)).                 (6)
```

For a distance threshold `c>e1`, let

```text
H_c=sum_(e>=c)N_e,  a_c=ceil(H_c/|F|).
```

Whenever `H_c>0`, some anchor has at least `a_c` such neighbors and

```text
a_c n c^2 <= R(2a_c c-(a_c-1)e1).                         (7)
```

No single higher shell is required to contain those neighbors.

## 3. Many-anchor degree control

Let `h_A` be the number of neighbors of `A` at distance greater than `e1`.
The complement of the `e1`-distance graph has independence number at most
`r`.  The Caro-Wei random-order argument gives

```text
sum_A 1/(h_A+1) <= r.                                     (8)
```

For `A_t={A:h_A>=t}`, define

```text
H_t=sum_(A in A_t)h_A,  Q_t=sum_(A in A_t)q_A.
```

Then

```text
|A_t| >= |F|-tr,
H_t >= sum_A h_A-t(t-1)r,
tn Q_t^2 <= R H_t(2tQ_t-(t-1)e1 H_t).                     (9)
```

The last inequality follows by applying (4) at each high-degree anchor and
using convexity after weighting by `h_A/H_t`.

## 4. Deployed M31 consequence

Use

```text
n=2097152, m=981129, w=67447,
B*=16777215, L0=B*+1=8n,
r=n-w=2029705, R=1094962529967.
```

Every one-distance subfamily of a depth-`w` deployed M31 prefix fiber has
size at most `r`: the fixed-weight and prefix equations place the incidence
vectors in an affine space of dimension at most `n-w-1`, and the usual
evaluation-function argument gives the affine-function cap `n-w`.

Any `L0`-member family therefore has at least two distances, and its first
two satisfy

```text
67448 <= e1 <= floor(R/n)=522118,
e1 < e2 <= m=981129.                                      (10)
```

Turán gives at least `61148348` unordered non-`e1` pairs.  Equation (8)
strengthens this to

```text
at least 539576 anchors with h_A>=8,
carrying at least 8633216 ordered non-e1 incidences.       (11)
```

Apply (9) with `t=8`.  Every counted incidence has distance at least `e2`,
so convexity between `e1`, `e2`, and `Q_8/H_8` yields the necessary condition

```text
8n e2^2 <= R(16e2-7e1).                                   (12)
```

Crucially, all distances above `e1` may be split among arbitrarily many
shells.  Thus every first-two-distance cell satisfying the strict reverse of
(12) has size at most `B*`, regardless of how many further distances occur.

The complete universe in (10) has the exact ledger

```text
first-two-distance cells             312061622166
excluded by (12)                      45504039302
not excluded                         266557582864
terminal e2 intervals                     386588
```

The first nonempty cut interval is `(135531,981129)`; the last is

```text
e1=522118, 706717 <= e2 <= 981129.
```

The canonical interval rows `(e1,first_bad_e2,981129,count)` have SHA-256

```text
d130fa35b9c5b8d473e3929d53d2627f598439b26e67fb689ec9936c11ee465f
```

On the exact integral-ratio two-shell grid, (12) intersects exactly the
`97162` rows already cut by PR #529.  The new theorem's gain is its
arbitrary-shell scope, not a change to the official two-shell survivor count.

The off-diagonal block is strictly stronger than applying #529 shell by
shell.  At `e1=522118`, take eight one-member shells
`981122,...,981129`: each diagonal singleton test passes, while their union
violates (9) by the exact margin

```text
23704293362569658480.
```

This local population vector is not claimed to be globally realizable.

## 5. Validation and nonclaims

Run

```text
python3 experimental/scripts/verify_m31_multi_anchor_shell_sos.py
```

The verifier checks (1) on all 2,500 shell-weight choices in `J(6,3)`,
recomputes the Turán/many-anchor constants, enumerates every terminal interval,
replays the integral-ratio overlap, and checks all counts, endpoints, hashes,
and the strict off-diagonal example.

This packet does not prove every deployed M31 prefix fiber has size at most
`B*`; pay the remaining `266557582864` first-two-distance cells; add cell
sizes; prove surviving cells realizable; use the modular-nullity floor; supply
an exhaustive first-match upper ledger; prove `U(a0+1)<=B*`; or solve the
deployed M31 row.  It has no asymptotic effect.

The next target is a global tail-distribution dual: either show every
`L0`-member prefix family violates (7) or (9) at some threshold, or construct
an exact ordered-distance and local triple-distribution countercertificate
satisfying all these inequalities and the coordinate-labeled prefix equations.
