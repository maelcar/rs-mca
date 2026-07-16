# Rank-15 `M=212` conditional arrangement exclusions at `D=66,67,68,146`

## Status

```text
PROVED / EXACT CERTIFICATE / CONDITIONAL ARRANGEMENT PAYMENT
```

## Claim

Work over the deployed prime field

```text
p = 2,130,706,433.
```

Assume a rank-15 source reduction produces an arrangement of 42
distinct, individually `F_p`-rational projective lines with:

- exactly 211 reduced arrangement intersections;
- exactly 15 distinct intersections on every line; and
- intersection multiplicity at most 15.

Let `n_k` be the number of multiplicity-`k` intersections and put `D=n_2`.
Then

```text
D not in {66,67,68,146}.
```

The already integrated note owns `D=39` and `D=44..61`. Pending PR #804 owns
`D=62..65`. If #804 lands, the exact conservative remainder inside this
conditional arrangement model becomes

```text
69 <= D <= 145.
```

No recurrence parent is removed.

## Exact certificate layer

The global incidence identities are

```text
sum_k n_k          = 211,
sum_k k n_k        = 42*15,
sum_k C(k,2) n_k   = C(42,2).
```

The verifier reconstructs every bounded moment profile, the exact disjoint
group packing gate, all 2,025 admissible line types, and all 78 pair-capacity
rows. The JSON contains 4,387 exact sparse integer Farkas certificates:

```text
D=66:  373
D=67: 1168
D=68: 2846
```

For each certificate, equality multipliers are unrestricted, pair-capacity
multipliers are positive, every admissible line-type coefficient is
nonnegative, and the combined right-hand side is strictly negative. The
remaining finite profiles are handled by the geometric arguments below.

## Distinguished-prefix inequality

Let `X` be a selected set of `s` high-multiplicity points and put

```text
J = sum_{P in X} k_P.
```

At most

```text
z = 42 + C(s,2) - J
```

arrangement lines avoid `X`. An unselected multiplicity-`k` point lies on at
least `max(0,k-s)` avoiding lines. Distinct unselected points consume disjoint
unordered pairs of avoiding lines, so

```text
sum_{P notin X} C(max(0,k_P-s),2) <= C(z,2).
```

Descending prefixes reject two residual profiles at `D=66`, four at `D=67`,
and seven at `D=68`.

## Two multiplicity-15 points

A multiplicity-15 point is modular: a line not through it meets its 15 lines
in 15 distinct support points, exhausting that line's support.

Suppose two multiplicity-15 points `P,Q` exist. Their line belongs to the
arrangement. The other 14 lines through each point form a `14 x 14` affine
grid, and the remaining 13 arrangement lines are complete grid transversals.
After sending `PQ` to infinity, those transversals give 13 distinct affine
maps carrying one 14-set onto the other.

The affine stabilizer of a 14-set therefore has order at least 13. It has no
nontrivial translation because a translation orbit has length `p`. After
centering its fixed point, it is a multiplicative subgroup of `F_p^*`. A
14-point invariant set forces subgroup order 13 or 14, but

```text
(p-1) mod 13 = 10,
(p-1) mod 14 = 8.
```

This removes the remaining two-15-point profiles at `D=66,67,68`.

## Final `D=68` profiles

The only remaining profiles are

```text
4^26,5^3,13,14,15,
4^29,6,13,14,15.
```

Call the multiplicity-13, 14, and 15 points `A,B,C`. No line contains all
three. If `x_i` counts lines containing exactly `i` of them, then heavy
incidence gives `x_2=x_0<=3`. The small high points force `x_0>=3`, hence

```text
x_0=x_2=3.
```

Thus all three heavy sides occur, there are exactly three no-heavy lines, and
the remaining lines form low pencils of sizes 11, 12, and 13 at `A,B,C`.

### No-heavy-pair concurrency lemma

Let the three no-heavy lines be `N_1,N_2,N_3`. A small multiplicity-`k` point
off the heavy sides uses at least `k-3` of these lines, because it lies on at
most one low line through each of `A,B,C`. A small point on a heavy side uses
at least `k-2` no-heavy lines. Distinct points cannot use the same pair
`{N_i,N_j}` because two projective lines have only one intersection.

For `4^26,5^3,13,14,15`, each of the three fivefold points consumes at least
one of the three pairs of no-heavy lines. They therefore consume all three
pairs, one per point. Each is off the sides, uses exactly two no-heavy lines,
and has one low line through each of `A,B,C`. Any fourfold point on a side or
missing one low-pencil direction would consume an already used no-heavy pair,
which is impossible.

For `4^29,6,13,14,15`, the sixfold point is off the sides and lies on all
three no-heavy lines, so it consumes all three pairs. Again, every fourfold
point is off the sides and has one low line through each of `A,B,C`.

This lemma supplies the concurrency premise omitted from the initial worker
draft. In both profiles every small high point is a grid point of the `B`-low
and `C`-low pencils and lies on one `A`-low line.

### Kneser contradiction

The 11 `A`-low lines contain at least 131 `B`-low/`C`-low grid correlations.
Every correlation is at most 12, so at least ten of the eleven correlations
are exactly 12; otherwise their sum is at most

```text
9*12 + 2*11 = 130.
```

Let `T` be ten full-correlation parameters and let `W_0` be the 12-set from
one low pencil. Full correlation gives `|T W_0|<=13`. If `H` is the
stabilizer of `T W_0`, Kneser's theorem gives

```text
|T W_0| >= |T H| + |W_0 H| - |H|.
```

Because `|T W_0|<=13` and `|H|` divides `p-1=2^24*127`, the possible orders
are `1,2,4,8`. The corresponding lower bounds are `21,20,20,24`, all greater
than 13. This excludes both final `D=68` profiles.

## Endpoint `D=146`

There are 65 non-double points. Put `x=k-2` at each. The global moments give

```text
sum x   = 208,
sum x^2 = 676,
sum (x-3)(x-4) = 0.
```

Every summand is nonnegative, so each non-double point is fivefold or
sixfold. The forced profile is

```text
n_5=52, n_6=13.
```

On each line, if `a,b,d` count fivefold, sixfold, and double points, the two
line identities give `3a+4b=26`. Its only nonnegative solutions are
`(a,b)=(6,2)` and `(2,5)`. Every line therefore contains at least two
sixfold points, requiring 84 sixfold incidences, while the global profile has
only `6*13=78`. Contradiction.

## Exact route cut at `D=145`

The profile

```text
n_2=145, n_3=2, n_5=50, n_6=14
```

passes the moment, disjoint-group, line-type, distinguished-prefix, and pair-
capacity relaxation. One abstract line-type ledger consists of one row
`(d,t,n5,n6)=(3,6,4,2)` and 41 rows `(7,0,6,2)`. This is not asserted to be a
projective arrangement. It proves that the present generic relaxation cannot
finish the residual interval without another geometric invariant.

## Source and ledger impact

The repository does not yet prove that every relevant child state reaches the
arrangement interface assumed above. This packet proves only the conditional
arrangement theorem. It does not reprove the characteristic-safe extactic
transport, identify a source row, or transport the exclusion across a child
interval.

The exact local delta is

```text
newly excluded D:             66,67,68,146
conditional post-#804 wall:   69..145
recurrence parents removed:   0
```

## Reproduction

From the packet's `work/` directory, run

```text
python3 verify_rank15_uniform_geometric_transport.py
python3 -O verify_rank15_uniform_geometric_transport.py
cmp verify_rank15_uniform_geometric_transport.expected.txt <(
  python3 verify_rank15_uniform_geometric_transport.py
)
```

The verifier is standard-library only and contains no `assert` statements.

## Nonclaims

This result does not prove the assumed arrangement interface from the literal
source, transport any child state, prove `D_2(u)<=211`, remove a recurrence
parent, settle affine rank at least 16, prove Grand List or Grand MCA, move the
official `0/2` score, or establish a deployed adjacent certificate.
