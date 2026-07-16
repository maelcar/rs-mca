# Rank-15 conditional arrangement exclusion at `D=69..72`

## Status and exact theorem

```text
PROVED / CONDITIONAL ARRANGEMENT INTERFACE / FIELD-SPECIFIC
```

Let

```text
p = 2,130,706,433.
```

Let `A` be an arrangement of 42 distinct `F_p`-rational projective lines in
`P^2(F_p)`.  Assume:

1. the reduced set of arrangement intersections has exactly 211 points;
2. every arrangement line contains exactly 15 distinct intersection points;
3. every intersection has multiplicity at most 15.

Write `n_k` for the number of points incident with exactly `k` arrangement
lines, and put `D=n_2`.  Then

```text
D not in {69,70,71,72}.
```

If `D=73`, the same proof leaves only the necessary profile

```text
n_2=73,
n_3=122,
n_4=n_5=n_6=n_11=n_15=1,
n_7=11,
n_k=0 for k in {8,9,10,12,13,14}.
```

This is a theorem about the displayed arrangement object.  It is conditional
only in its repository use: no theorem in this packet constructs that object
from a rank-15 Reed--Solomon child.

## Source-interface boundary

The provenance labels `M=212`, `q=14`, `B=42`, `U=E=0`, and `R=211` name the
source lane that motivated the arrangement interface.  They are not a source
compiler proved here.  In particular, this note does not prove, for any of the
366 child states `u=1,043,592..1,043,957`, that a received word and syndrome:

- produce the required two-flat or pencil;
- produce exactly 42 distinct rational lines;
- have exactly 211 reduced intersections and 15 intersections on every line;
- satisfy `U=E=0` with every required denominator nonzero; or
- enter the literal first-match consumer with the required endpoint convention.

Consequently the theorem removes no child or recurrence parent.  The source
transport wall remains separate from the geometry proved below.

## Global moments and the finite terminal list

Every point is incident with at least two lines.  Counting points, line-point
incidences, and unordered pairs of lines gives

```text
sum_{k=2}^{15} n_k          = 211,
sum_{k=2}^{15} k n_k        = 42*15 = 630,
sum_{k=2}^{15} C(k,2) n_k   = C(42,2) = 861.             (1)
```

Put `c_w=n_{w+3}` for `1<=w<=12`.  Eliminating `n_3` from (1) gives

```text
sum_{w=1}^{12} w c_w       = D-3,
sum_{w=1}^{12} w^2 c_w     = 471-D,
sum_{w=1}^{12} C(w+1,2)c_w = 234.                        (2)
```

We also use the following necessary inequality, proved here rather than
imported.  Select `s` high points, and let `J` be the sum of their
multiplicities.  Inclusion-exclusion over the line pencils shows that the
number `z` of arrangement lines avoiding all selected points satisfies

```text
z <= 42 + C(s,2) - J.                                   (3)
```

Indeed, the sum of the selected pencil sizes is `J`.  If one arrangement line
contains `r` selected points, its overcount `r-1` is at most `C(r,2)`, and all
such selected pairs total at most `C(s,2)`.  An unselected multiplicity-`k`
point lies on at least `max(0,k-s)` avoiding lines.  Two avoiding lines have
only one intersection, so different unselected points consume disjoint line
pairs.  Hence

```text
sum_{Q unselected} C(max(0,m(Q)-s),2) <= C(z,2).          (4)
```

The replay applies (4) to every descending prefix of the multiplicities at
least four.

### At most one multiplicity-15 point

This geometric filter is part of the present proof.  A multiplicity-15 point
`P` is modular: its 15 lines contain `15*14=210` distinct points other than
`P`, which are all the other arrangement intersections.  Thus every point
other than `P` lies on a `P`-line.

Suppose that `P` and `Q` both have multiplicity 15.  Modularity forces the
geometric line `PQ` to be an arrangement line.  Send `PQ` to the line at
infinity.  The 14 other `P`-lines and 14 other `Q`-lines become vertical and
horizontal affine lines, parameterized by 14-sets `X,Y subset F_p`.  The 13
remaining arrangement lines are complete grid transversals: each has equation

```text
y = a x + b,  with a nonzero,
```

Its 14 intersections with the vertical class, together with its intersection
with `PQ`, exhaust its 15 support points.  Its intersections with all 14
horizontal lines must therefore be those same grid points, so it maps `X`
bijectively to `Y`.  Fixing one transversal and composing its
inverse with the other 12 gives at least 13 distinct affine automorphisms of
`X`.

Let `G` be the affine stabilizer of `X`.  A nonzero translation has order `p`
and cannot preserve a 14-set, so the slope map `G -> F_p^*` is injective.
Thus `|G|` divides `p-1` and is nonzero in `F_p`.  The average

```text
c = |G|^{-1} sum_{g in G} g(0)
```

is therefore defined and fixed by `G`.  After translating `c` to zero, `G`
is a multiplicative subgroup.  Its nonzero orbits have size `|G|`.  Since
`|G|>=13` and `|X|=14`, one must have `|G|=13` or `14`, according as the fixed
point belongs to `X` or not.  But

```text
p-1 = 2^24*127,
(p-1) mod 13 = 10,
(p-1) mod 14 = 8.
```

Neither order divides `p-1`, a contradiction.  Hence `n_15<=1`.

### Exact arithmetic lemma

Enumerating all nonnegative solutions of (2), applying (4) to descending
prefixes, and then applying `n_15<=1` gives exactly the following terminal
profiles.  Unlisted multiplicities are zero.

| `D` | `n_3` | multiplicities at least four |
|---:|---:|---|
| 69 | 109 | `n_4=27,n_5=3,n_14=3` |
| 69 | 108 | `n_4=29,n_5=2,n_13=n_14=n_15=1` |
| 69 | 108 | `n_4=30,n_6=1,n_14=3` |
| 70 | 106 | `n_4=30,n_5=2,n_14=3` |
| 70 | 105 | `n_4=32,n_5=1,n_13=n_14=n_15=1` |
| 71 | 103 | `n_4=33,n_5=1,n_14=3` |
| 71 | 102 | `n_4=35,n_13=n_14=n_15=1` |
| 71 | 123 | `n_6=15,n_14=n_15=1` |
| 72 | 100 | `n_4=36,n_14=3` |
| 72 | 121 | `n_5=2,n_6=14,n_14=n_15=1` |
| 73 | 122 | `n_4=n_5=n_6=n_11=n_15=1,n_7=11` |
| 73 | 118 | `n_4=3,n_5=1,n_6=14,n_14=n_15=1` |
| 73 | 119 | `n_5=4,n_6=13,n_14=n_15=1` |

The recursion is exhaustive by descending induction on `w`: at stage `w`, it
tries every integer from zero through the minimum of the remaining linear,
quadratic, and point-count quotients.  No solution of (2) can lie outside that
range.  The frozen verifier records the moment/prefix/terminal counts

```text
D=69: 5473 /  7 / 3
D=70: 6115 /  5 / 2
D=71: 6998 / 22 / 3
D=72: 7706 / 23 / 2
D=73: 8446 / 25 / 3.
```

It remains to eliminate the first ten rows and two of the three `D=73` rows.

## The multiplicity-14 matching lemma

Let `P` have multiplicity 14.  Its 14 lines contain 14 further intersections
apiece.  Two such lines have no common point other than `P`, so they cover

```text
14*14 = 196
```

distinct points outside `P`.  Exactly `211-1-196=14` points lie outside this
pencil.

There are 28 arrangement lines avoiding `P`.  Each meets the 14 `P`-lines in
14 distinct points and has exactly one additional intersection, necessarily
one of the 14 off-pencil points.  Thus the off-pencil points receive 28
incidences from the 28 avoiding lines.  Every one receives at least two, so
each receives exactly two.  Therefore:

```text
the 28 lines avoiding P are paired by 14 off-pencil double points.    (5)
```

In particular, every non-double point lies on a `P`-line.  The exceptional
pairs in every product or sum grid below are a subset of the matching (5), so
there is at most one exception in any row or column.

## Coordinate conventions, signs, and denominators

All heavy points and all lines joining them are `F_p`-rational.  The
projective transformations below are in `PGL_3(F_p)` and have nonzero
determinant because the normalized points are distinct.

### Collinear normalization

For three distinct collinear heavy points, send their line to `Z=0` and the
points to

```text
[1:0:0], [0:1:0], [1:-1:0].
```

Their non-common lines can be written, in the affine chart `Z=1`, as

```text
X=x,  Y=y,  X+Y=z.
```

Thus concurrency has the fixed sign convention `z=x+y`.  No parameter is
divided by another in this normalization.

### Triangle normalization

For three noncollinear heavy points, put the two source vertices at
`A=[1:0:0]`, `C=[0:1:0]`, and the target vertex at `T=[0:0:1]`.  A low line
means a line through one vertex and neither of the other two.  The low lines
have unique parameters in `F_p^*`:

```text
A_x: Y=xZ,
C_y: Z=yX,
T_z: Y=zX.
```

Indeed, for an `A`-line `bY+cZ=0`, both `b` and `c` are nonzero and
`x=-c/b`; the analogous ratios are `y=-a/c` and `z=-a/b`.  These are the only
denominators used, and they are nonzero precisely because side lines have been
removed.  The intersection of `A_x` and `C_y` is `[1:xy:y]`, so

```text
A_x, C_y, T_z are concurrent if and only if z=xy.        (6)
```

Side lines correspond to zero or infinite parameters and are kept outside the
sets in (6).  They and all extra arrangement lines are counted explicitly in
the matching cases below.

## Three multiplicity-14 points are impossible

Let `A,B,C` have multiplicity 14.

### Collinear case

If their common geometric line is absent, the three 14-line pencils are
disjoint and exhaust all 42 lines.  In the collinear normalization, apply (5)
at the point represented by the `X+Y=z` class.  For 14-sets `X,Y,Z`, all but
a perfect matching in `X x Y` satisfy `x+y in Z`.  Hence

```text
|(x+Y) intersect Z| >= 13                    for every x in X,
|Y intersect (Y+d)| >= 12                    for every d in X-X.
```

Cauchy--Davenport gives `|X-X|>=27`.  If
`r_Y(d)=|Y intersect (Y+d)|`, then `sum_d r_Y(d)=|Y|^2`, but

```text
196 >= 14 + 26*12 = 326,
```

a contradiction.

If the common line is present, each heavy pencil has 13 low lines and the
union of the pencils has 40 lines; exactly two extra arrangement lines remain.
The 28 lines avoiding the target 14-point are the two 13-line source classes
plus those two extra lines.  The global matching (5) still permits at most one
exception in each `13 x 13` source row.  Thus the same argument gives

```text
|X-X|>=25,
r_Y(d)>=11 for d in X-X,
169 >= 13 + 24*11 = 277,
```

again impossible.  A source-source intersection cannot lie on the common line,
because the two source lines meet it at different heavy points; hence its
target line is one of the 13 target-low lines.  The two extra lines can consume
matching partners, but cannot create a second exceptional source-source pair
in any row.

### Noncollinear case

Use (6), and apply (5) at a chosen target point.  Let `t` be the number of
triangle sides belonging to the arrangement.  When `t=1`, choose an endpoint
of the unique side as target; when `t=2`, choose the common endpoint of the two
sides.  Let `X,Y` be the source low-line parameter sets and `Z` the target
low-line set.  The exact bookkeeping is:

| `t` | `(|Z|,|X|,|Y|)` | target-avoiding lines outside `X union Y` | `L=2(|Y|-1)-|Z|` | upper bound on `|XX^-1|` |
|---:|---:|---:|---:|---:|
| 0 | `(14,14,14)` | 0 | 12 | 16 |
| 1 | `(13,14,13)` | 1 extra line | 11 | 15 |
| 2 | `(12,13,13)` | 2 extra lines | 12 | 14 |
| 3 | `(12,12,12)` | opposite side plus 3 extra lines | 10 | 14 |

If an `X`-line and a `Y`-line are not matched at a double point, (5) puts
their intersection on a target-pencil line.  It cannot lie on either target
side: a source low line meets that side only at its source vertex, and the
other source low line avoids that vertex.  Hence the target line is in `Z`.

For every `x in X`, at most one `y in Y` is its matching exception, so
`|xY intersect Z|>=|Y|-1`.  Therefore, for every `g in XX^-1`,

```text
r_Y(g):=|Y intersect gY| >= L.                           (7)
```

Since `sum_g r_Y(g)=|Y|^2` and `r_Y(1)=|Y|`, (7) gives the last column.

Now apply Kneser's theorem in `F_p^*`.  If `H` stabilizes `XX^-1`, then

```text
|XX^-1| >= 2|XH|-|H|
         >= |H| (2 ceil(|X|/|H|)-1).                    (8)
```

Every possible `|H|` divides `p-1=2^24*127`.  Direct evaluation of (8) for
`11<=|X|<=14` gives a minimum of 16, attained only at `|H|=16`.  This
contradicts the rows `t=1,2,3`.

For `t=0`, equality throughout forces `|XX^-1|=16`, `|H|=16`, `X` to lie in
one `H`-coset, and `XX^-1=H`.  Equation (7) then gives

```text
sum_{h in H} |Y intersect hY| >= 14+15*12 = 194.         (9)
```

If the intersections of `Y` with the `H`-cosets have sizes `y_i`, the left
side of (9) is `sum_i y_i^2`.  A 14-set meeting at least two 16-cosets has
sum of squares at most `13^2+1=170`, so `Y` also lies in one `H`-coset.

Each element of the product coset has at least

```text
|X|+|Y|-|H| = 12
```

representations as `xy`.  The target `Z` contains **at most fourteen** of the
sixteen elements of that product coset.  Thus at least two values are absent
from `Z`, accounting for at least `2*12=24` exceptional pairs.  The matching
allows at most 14.  This contradiction proves

```text
n_14 <= 2.                                                (10)
```

The phrase "at most fourteen" is essential: `Z` need not be contained in the
product coset.  Only the upper bound on how many coset values it can contain is
used.

## Multiplicities 13, 14, and 15 cannot coexist

Let `m(A)=13`, `m(B)=14`, and `m(C)=15`, and apply (5) at `B`.

### Collinear case

If the common line through `A,B,C` is absent, the three pencils are disjoint
and exhaust all 42 lines.  The 28 lines avoiding `B` are the 13 `A`-lines and 15
`C`-lines.  Lines in the same class meet at `A` or `C`, not at a double point,
so a perfect matching between classes of sizes 13 and 15 is impossible.

If the common line is present, there are 12 `A`-low lines, 13 `B`-low lines,
14 `C`-low lines, and two extra lines.  The lines avoiding `B` are the 12
`A`-low lines, 14 `C`-low lines, and the two extras.  In additive coordinates,
all but at most one point in each 14-entry row lies on one of the 13
`B`-low lines.  Thus `|(x+Y) intersect Z|>=13` for
`(|X|,|Y|,|Z|)=(12,14,13)`, and in particular

```text
r_Y(d)>=12 for d in X-X.
```

Cauchy--Davenport gives `|X-X|>=23`, contradicting

```text
196 >= 14+22*12 = 278.
```

### Noncollinear case

Let `a,b,c` indicate whether `AB,AC,BC` is an arrangement side.  In the
triangle normalization, take `X` from the `A`-low lines, `Y` from the
`C`-low lines, and `Z` from the target `B`-low lines.  Their exact sizes are

```text
|X|=13-a-b,  |Y|=15-b-c,  |Z|=14-a-c.                  (11)
```

The union of the three heavy pencils has `42-(a+b+c)` lines, so exactly
`a+b+c` additional arrangement lines occur.  Among the 28 lines avoiding
`B`, the lines outside `X union Y` consist of the opposite side `AC` when
`b=1`, together with those additional lines.  Matching (5) again gives
`XY subset Z` outside a partial matching: a nonmatched source-source
intersection cannot lie on a target side for the same low-line reason used
above.  The eight cases are:

| `(a,b,c)` | `(|X|,|Y|,|Z|)` | outside `X union Y` | contradiction |
|---:|---:|---:|---|
| 000 | `(13,15,14)` | 0 | unequal cross-class perfect matching |
| 001 | `(13,14,13)` | 1 | `|XX^-1|<=15<16` |
| 010 | `(12,14,14)` | side `AC` plus 1 extra | 14 `Y`-lines have only 13 eligible partners |
| 011 | `(12,13,13)` | side `AC` plus 2 extras | `|XX^-1|<=15<16` |
| 100 | `(12,15,13)` | 1 | one row needs 14 target values, but `|Z|=13` |
| 101 | `(12,14,12)` | 2 | one row needs 13 target values, but `|Z|=12` |
| 110 | `(11,14,13)` | side `AC` plus 2 extras | `|XX^-1|<=15<16` |
| 111 | `(11,13,12)` | side `AC` plus 3 extras | `|XX^-1|<=14<16` |

In case 010, the opposite side `AC` meets every `C`-low line at the
multiplicity-15 point `C`, so it cannot be a double-point matching partner.
Only the 12 `X`-lines and the one extra line are eligible.  In the four Kneser
rows, the upper bounds follow from (7); (8) supplies the lower bound 16.  Thus

```text
n_13 n_14 n_15 = 0.                                     (12)
```

## The PBD forced by a 14-point and a 15-point

Let `m(B)=14` and `m(C)=15`.  First, `S=BC` is an arrangement line.  Otherwise
the 15 `C`-lines all avoid `B`; none can be paired with another `C`-line, but
only 13 other lines avoid `B`, contradicting (5).

With `S` present, the arrangement consists of:

```text
S,
13 B-low lines,
14 C-low lines,
14 lines N_1,...,N_14 avoiding both B and C.             (13)
```

The 28 lines avoiding `B` are the 14 `C`-low lines and the 14 `N_i`.  No two
`C`-low lines form a double point, so (5) pairs every `C`-low line with a
different `N_i`.  In particular, no pair `N_i,N_j` meets in a double point.

Modularity of the multiplicity-15 point says that every point other than `C`
lies on a `C`-line.  The matching lemma at `B` says that every non-double
point lies on a `B`-line.  If `t_Q` of the `N_i` pass through a point `Q`
where at least two `N_i` meet, then

```text
m(Q)=t_Q+1 if Q is on S,
m(Q)=t_Q+2 if Q is off S.                               (14)
```

The line `S` has 13 intersections other than `B,C`.  They receive 14
incidences from the `N_i`; each receives at least one because no other kind of
line can create such an intersection on `S`.  Hence exactly one is incident
with two `N_i`, and the other twelve with one.  The unique side point is a
triple point and supplies one distinguished 2-block.

For every remaining pair `{N_i,N_j}`, take the set of all `N`-indices through
their intersection.  Equations (13)--(14) give a pairwise-balanced design on
14 vertices: every unordered pair occurs in exactly one block, and

```text
sum_blocks C(|block|,2) = C(14,2) = 91.                 (15)
```

An off-side multiplicity-`k` point supplies a block of size `k-2`.  This
translation is exact, not merely a pair-capacity relaxation.

### The `D=71` PBD

For `n_6=15,n_14=n_15=1`, (15) consists of fifteen 4-blocks and the
distinguished 2-block:

```text
15*C(4,2)+C(2,2)=90+1=91.
```

For a vertex, let `r` count incident 4-blocks and `e in {0,1}` membership in
the 2-block.  Its 13 pairs give `3r+e=13`.  A vertex with `e=0` is impossible
modulo 3, but only two vertices have `e=1`.  Contradiction.

### The `D=72` PBD

For `n_5=2,n_6=14,n_14=n_15=1`, the blocks are two 3-blocks, fourteen
4-blocks, and one 2-block.  If `u` counts the incident 3-blocks, `v` the
4-blocks, and `e` the 2-block, then

```text
2u+3v+e=13.
```

Modulo 3, `u=0` forces `e=1`, `u=1` is impossible, and `u=2` forces `e=0`.
No vertex lies in exactly one of the two 3-blocks, so the two blocks have the
same three vertices, repeating three pairs in a PBD.  Contradiction.

### Two `D=73` PBDs

For `n_5=4,n_6=13,n_14=n_15=1`, the blocks are four 3-blocks, thirteen
4-blocks, and one 2-block.  The equation `2u+3v+e=13` permits

```text
(u,e) in {(0,1),(2,0),(3,1)}.
```

Only two vertices have `e=1`, so at least twelve vertices have `u=2`.  This
requires at least 24 incidences in four 3-blocks, which have only 12.

For `n_4=3,n_5=1,n_6=14,n_14=n_15=1`, the design has four 2-blocks, one
3-block, and fourteen 4-blocks.  Let `e` count incident 2-blocks and let
`u in {0,1}` record membership in the 3-block.  The equation

```text
e+2u+3v=13
```

forces each of the three vertices in the 3-block to have `e>=2`, and every
other vertex to have `e>=1`.  The required `3*2+11=17` incidences exceed the
eight incidences supplied by four 2-blocks.  Contradiction.

## Completion of the theorem

The five terminal profiles with `n_14=3` fail (10).  The three profiles with
positive `n_13,n_14,n_15` fail (12).  The remaining `D=71,72` profiles fail
their PBD equations.  Thus `D=69,70,71,72` are impossible.  The two PBD
arguments at `D=73` leave only

```text
n_3=122,
n_4=n_5=n_6=n_11=n_15=1,
n_7=11.
```

## Exact remaining geometry wall

At the surviving `D=73` profile, dualize the 42 arrangement lines to 42
points and send the dual line corresponding to the multiplicity-15 point to
infinity.  The other 27 dual points form a set `U subset AG(2,F_p)`.  The 15
points at infinity are exactly the determined directions of `U`.  Each
original line through the multiplicity-15 point has 14 other intersections,
so `U` occupies exactly 14 affine lines in each determined direction.

An original multiplicity-`k` point away from the 15-point becomes an affine
line containing `k-1` points of `U`.  Therefore the aggregate block spectrum
is

```text
10^1, 6^11, 5^1, 4^1, 3^1, 2^122, 1^73.                (16)
```

The checks

```text
number of occupied lines: 210 = 15*14,
point-line incidences:     405 = 15*27,
determined pairs:          351 = C(27,2)
```

show that (16) is exactly compatible with the necessary direction ledger.
The next geometric theorem must exclude or construct this 27-point set.  A
generic direction lower bound is insufficient; the equality case and block
spectrum are load-bearing.

After this packet, the conditional arrangement wall is:

```text
D=73: one exact profile, equivalently (16);
D=74..145: still open to the new high-point/PBD invariants.
```

Independently, a literal source compiler is still required across all 366
children before any arrangement exclusion can be charged to a finite ledger.

## Arithmetic verifier and its boundary

Run from the repository root:

```text
python3 experimental/scripts/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.py
python3 experimental/scripts/verify_rank15_m212_q14_b42_d69_d73_arrangement_profiles.py --tamper-selftest
```

The verifier is standard-library only and uses explicit exceptions rather than
`assert`, so optimized mode follows the same checks.  It reconstructs the
moment census, descending-prefix filter, terminal profiles, `p-1` divisor
table, numerical Kneser minima, PBD pair/vertex equations, and direction
spectrum.  It does **not** machine-prove matching (5), the coordinate
normalizations, Cauchy--Davenport, Kneser's theorem or its applicability, the
PBD construction, or projective duality.  Those are the mathematical steps in
this note.

## Novelty and overlap boundary

At `origin/main@9c4ca98cf45639407611a3ad5154893fb22e77e2`, the integrated
conditional arrangement packets own

```text
D in {39} union {44,45,...,68} union {146}.
```

The new theorem layer is exactly:

- the multiplicity-14 off-pencil perfect matching;
- exclusion of three multiplicity-14 points over this field;
- exclusion of a simultaneous `13,14,15` multiplicity triple;
- the exact 14-vertex PBD induced by a `14,15` pair;
- exclusion of `D=69..72` and reduction of `D=73` to (16).

Open overlap baseline `#826`, `#838`, `#843`, and `#844` is not consumed or
reclaimed.  Those packets concern the rank-16 fixed-core, block-wedge,
source-compiler, or global-ledger layers; this note claims only the separate
rank-15 conditional arrangement theorem above.

## Nonclaims

This packet does not claim:

- source transport or first-match ownership for any child;
- child or parent payment;
- `D_2(u)<=211` for the 366-child interval;
- exclusion of the remaining `D=73` profile or any `D=74..145` profile;
- an all-prime or asymptotic theorem;
- a Grand List or Grand MCA theorem;
- a deployed adjacent certificate or official score movement.

The official score is unchanged.
