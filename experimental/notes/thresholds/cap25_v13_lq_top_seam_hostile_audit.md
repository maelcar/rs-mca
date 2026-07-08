# CAP25 v13 LQ top-seam hostile audit

Status: REPAIR / EXACT_NEW_WALL / AUDIT.

This note records the hostile-audit outcome for the proposed CAP25 v13
`L_Q` top-seam payment.  It does not prove an adjacent deployed safe row and
does not prove

```text
U(a0 + 1) <= B*.
```

The point is narrower.  The top-seam algebra gives useful theorem-facing
normal forms and small local caps, but the audited packet does not justify the
global conclusion that the top seam is already paid by quotient rungs or by
the current finite ledger constants.

## Context

The leakage compiler note separates

```text
Q = Q_paid dotcup L_Q dotcup Q_new,
```

where `L_Q` is the target-label leakage left when a Q witness has the same
prefix target as an earlier support but is not itself an earlier-paid support.
For two equal-prefix supports, write

```text
Lambda_M = G A,
Lambda_E = G B,
deg A = deg B = e = |M \ E| = |E \ M|.
```

Equal first `w` prefix data forces

```text
deg(A - B) <= e - w - 1.
```

The top seam is the boundary case `e = w + 1`.  In this case the locator
difference must be constant:

```text
A - B = c.
```

The Fable referee packet proposed to turn this into a complete deployed-row
payment.  The hostile audits repair that proposal into the narrower facts
below.

## Fixed-mark top-seam normal form

After fixing the earlier marked support and the common core convention, the
top-seam leakage neighbors inject into ordered split-translate data

```text
(B,c),  c in K^*,
```

where `K` is the coefficient field, `B` is monic of degree `e`, and the two
split sides satisfy the appropriate divisor conditions

```text
B | Lambda_E,
B + c | Lambda_{D \ E}
```

up to the chosen orientation of the marked pair.

This is a per-target or fixed-mark numerator bound.  It is not, without the
first-match selector and support-multiplicity bookkeeping, a raw support
cardinality bound.  In particular, a theorem stated for all unmarked supports
is too broad; the safe statement fixes the marked earlier witness or includes
the selector map in the hypotheses.

## Split-translate local cap

Let `D` have size `n`, and let `B` be monic of degree `e`.  The number of
constants `c` for which `B + c` splits over `D` is at most

```text
floor(n/e).
```

If `B` itself is already one split side, then the number of nontrivial
translated mates is at most

```text
floor(n/e) - 1.
```

For the deployed CAP25 v13 top seam, `e = w + 1`, and in the KoalaBear and
Mersenne-31 adjacent rows this gives the local cap

```text
floor(2^21/e) - 1 = 30.
```

This is a useful local cap on multiplicity.  It is not by itself a row-sharp
global payment of `L_Q`.

## Characteristic-zero rigidity

For dyadic multiplicative rows, the constant-translate split-pair equation is
rigid in characteristic zero: at the deployed top seam, the odd part of `e` is
larger than one, so the characteristic-zero multiplicative top seam is empty.
For the KoalaBear MCA row,

```text
e = 67472 = 16 * 4217.
```

For the Mersenne-31 row,

```text
e = 67448 = 8 * 8431.
```

The Mersenne-31 line-round model requires the corresponding Chebyshev or
circle-row version of the rigidity argument; it should not be imported from
the multiplicative proof without stating that extra convention.

The finite-field top seam can still have characteristic-specific accidents.
Thus the characteristic-zero rigidity is an obstruction filter, not a
deployed finite census.

## Pullback descent is structural only

If a split pair has all relevant nonzero coefficients in degrees divisible by a
common divisor `d`, then the pair-level object descends to the quotient rung.
This is a valid structural descent statement.

The audited false promotion is the stronger sentence

```text
pair-level pullback descent => already charged to quotient rungs.
```

That implication is not proved.  A pair can descend while the common core or
the full support is not quotient-closed in the way required by the first-match
ledger.  Therefore quotient descent should be recorded as a structural
classification of split pairs, not as an automatic ledger payment.

## KoalaBear budget audit

For the deployed KoalaBear MCA adjacent row, the raw multiplier appearing in
the Q-fin primitive-wall notes is

```text
K_raw = 4,807,520.
```

The top-seam packet subtracts the audited rung charge

```text
charge = 35,624,
```

giving

```text
K_raw - charge = 4,771,896.
```

However, the first-match ledger also imports the smaller remaining multiplier

```text
K_rem = 4,805,007.
```

If the same charge is deducted from this remaining multiplier, the conservative
post-charge number is

```text
K_rem - charge = 4,769,383.
```

Thus a bound of the form

```text
T_top <= 4,771,896
```

cannot be cited as sufficient for a `K_rem`-based row certificate without an
additional ledger reconciliation.  This is one of the exact first false lines
in the broad Fable packet.

## Mersenne-31 census wall

For the Mersenne-31 adjacent row, the integer multiplier

```text
K_raw = 9
```

is only the ambient full-budget cap.  It is not a post-rung residual payment.
After side charges, the available residual can be smaller or even negative
under a pessimistic charge convention.

Moreover, the top-seam count is naturally an ordered-pair count, hence even
under the usual orientation convention.  Consequently a raw statement

```text
T_top <= 9
```

behaves like the sharper ordered statement `T_top <= 8`.  An exact certificate
finding ten valid ordered Mersenne-31 top-seam pairs would falsify the raw
ambient census, though it would still have to be checked against the precise
first-match selector before becoming a deployed-row counterpacket.

The exact Mersenne-31 live task is therefore a finite census or falsifier for
the ordered top-seam pairs, not a solved ledger inequality.

## Structured-prime warning

Small dyadic rows show that random-model and multiplicity-one intuitions can
fail sharply in characteristic-specific top-seam arithmetic.

The audited structured-prime examples are:

```text
(n,e,p) = (32,3,3137):
  unordered top-seam pairs = 32,
  ordered top-seam pairs   = 64,
  random-model unordered expectation ~= 0.92085.

(n,e,p) = (64,3,65537):
  unordered top-seam pairs = 352,
  ordered top-seam pairs   = 704,
  random-model unordered expectation ~= 0.17456.
```

In the `(64,3,65537)` case, the audit reports six twist orbits.  Of the 352
unordered pairs, 224 have the second difference already zero in characteristic
zero, while the remaining 128 have nonzero characteristic-zero second
difference whose resultant is divisible by `65537^2`.

These examples are not deployed-row counterexamples.  Their role is to block
the unsafe inference that finite top-seam multiplicity should behave like a
generic random-model count or a multiplicity-one census.

## Corrected status

The audited top-seam package supports the following narrow theorem-facing
material:

1. fixed-mark top-seam split-translate normal form;
2. local split-translate cap `floor(n/e)-1 = 30` at the deployed top seam;
3. dyadic multiplicative characteristic-zero rigidity, with a separate
   Chebyshev/circle-row convention required for Mersenne-31;
4. pair-level quotient pullback descent as a structural classification;
5. finite structured-prime warnings against random-model or multiplicity-one
   assumptions.

It does not prove:

```text
U(a0 + 1) <= B*,
CAP25-V13-LQ-MARKED-TOP-SP-EXTREMALITY,
top-seam payment by quotient rungs,
the Mersenne-31 ordered top-seam census,
or a deployed-row first-match upper ledger.
```

The remaining exact wall is a finite row-sharp census or payment theorem for
the `L_Q` top seam under the precise first-match selector, especially the
Mersenne-31 ordered-pair wall and the KoalaBear `K_rem` reconciliation.
