# CAP25 v13 LQ top-seam marked-incidence audit

Status: BANKABLE_LEMMA / COUNTERPACKET / EXACT_NEW_WALL.

This note records a narrow correction to the CAP25 v13 finite safe-side
program.  It does not prove the adjacent upper ledger and does not prove

```text
U(1116048) <= B*.
```

The useful point is local: once the first-match Q/LQ leakage branch is reduced
to a locator-prefix collision, the top seam has an exact constant-shift normal
form, but the object that must be counted is a marked incidence with its common
core.  Counting only unmarked side pairs is not a sound deployed-row
certificate.

## Algebraic top seam

Let `D` be the deployed evaluation set, and let `M,E subset D` be two
`m`-supports that collide in the coefficient-prefix data through depth `w`.
Write

```text
Lambda_M = G A,
Lambda_E = G B,
deg A = deg B = e = |M \ E| = |E \ M|,
deg G = m - e.
```

Here `G` is the common-core locator and `A,B` are the two side locators.  The
coefficient-prefix collision gives

```text
deg(Lambda_M - Lambda_E) <= m - w - 1.
```

Since `Lambda_M - Lambda_E = G(A-B)`, one obtains

```text
deg(A - B) <= e - w - 1.
```

Thus nontrivial collisions have `e >= w+1`.  At the top seam `e=w+1`, the
residual difference is forced to be constant:

```text
A - B = c,    c in base_field^*.
```

This is the bankable normal form.  It is only an algebraic reduction; by
itself it does not pay the row.

## Correct counted object

For first-match leakage, the verifier must count ordered marked triples, not
unmarked side pairs.  In support notation the top-seam object has the form

```text
(C,U,V)
```

with

```text
C, U, V pairwise disjoint subsets of D,
|U| = |V| = w+1,
|C| = m - w - 1,
M = C union U,
E = C union V,
Lambda_U - Lambda_V = c in base_field^*,
```

plus whatever first-match, quotient-pruning, support-cell, and row-specific
residual predicates are active in the certificate being audited.

Equivalently, in locator notation the object is

```text
(G,A,B),
```

where `G,A,B` are split, pairwise coprime locators over `D`,
`deg A = deg B = w+1`, `deg G = m-w-1`, and `A-B` is a nonzero constant.

The first false line in several tempting shortcuts is

```text
constant-shift side-pair count controls top-seam leakage mass.
```

It does not.  The common core `C` is part of the incidence.  Projecting away
`C` can hide a factor as large as a binomial-scale choice of common core unless
the residual predicates determine or sharply bound it.

## Row conventions

Under the current CAP25 v13 adjacent-row convention, the top seam has the
following parameters.

| row | safe agreement `m` | prefix depth `w` | side size `e=w+1` | common core `m-e` |
| --- | ---: | ---: | ---: | ---: |
| KoalaBear MCA | 1116048 | 67471 | 67472 | 1048576 |
| KoalaBear list | 1116047 | 67471 | 67472 | 1048575 |
| Mersenne-31 MCA | 1116024 | 67447 | 67448 | 1048576 |
| Mersenne-31 list | 1116023 | 67447 | 67448 | 1048575 |

These numbers should be derived from the row record by any checker.  A note or
script should not hard-code a mismatched `w` from an older table.

## Small-field counterpacket to unmarked/all-mates shortcuts

Work over `F_17^*`, let `m=4`, and use the two-coordinate target

```text
tau(M) = (p1(M), p2(M)),
p_i(M) = sum_{x in M} x^i.
```

The quotient-looking support

```text
E = {4, 6, 11, 13}
```

has

```text
tau(E) = (0,2).
```

The following primitive supports have the same target:

```text
M1 = {1, 2, 4, 10},
M2 = {3, 8, 10, 13},
M3 = {4, 7, 9, 14},
M4 = {7, 13, 15, 16}.
```

For each pair `(Mi,E)`, the common core has size one, so `e=3=w+1` when
`w=2`.  The side locators satisfy

```text
A_i - B_i in {5, 7, 10, 12} subset F_17^*.
```

Thus a single earlier target/support can have multiple primitive top-seam
mates.  This kills any certificate step that uses a canonical first-match
selector as though it also bounded the number of top-seam mates per selected
earlier support.

The example is not a deployed-row counterexample.  It is a local
counterpacket to a proof shortcut: target-level or side-pair-level uniqueness
does not replace a marked-incidence count.

## Checker rule

A CAP25 v13 finite safe-side checker should reject a top-seam certificate
unless it supplies one of the following:

1. an exact count of the marked incidence set `(C,U,V)` with all row-specific
   residual predicates;
2. a proof that the residual predicates determine the common core `C` from the
   side data `(U,V)` with row-compatible multiplicity;
3. a separate row-sharp theorem proving the common-core multiplicity is paid
   by the remaining upper ledger budget.

It is not enough to count only constant-shift side pairs `(U,V)`.

## Remaining wall

The exact remaining theorem is a row-sharp top-seam payment theorem:

```text
CAP25-V13-LQ-TOP-SEAM-NO-FREE-CORE-OR-ROW-SHARP-COUNT.
```

Equivalently, prove that after quotient-pullback, split-pencil, BC/SP, and
first-match pruning predicates are imposed, the marked incidence count is small
enough for the row budget.  A single residual constant-shift atom with a free
common core would be too large, so the next proof must either kill free cores
or replace the side-pair heuristic by an exact finite count.

## Nonclaims

This note does not:

* close the Q/LQ safe-side input;
* prove the KoalaBear or Mersenne adjacent safe rows;
* prove that constant-shift side pairs are rare enough;
* assert that the top seam is paid by existing SP/BC notes;
* modify Papers A-D.

It only banks the top-seam normal form, the correct marked object, a local
counterpacket to unmarked/all-mates shortcuts, and the next exact checker
obligation.
