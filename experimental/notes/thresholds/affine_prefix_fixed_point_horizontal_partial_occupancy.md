# Affine-prefix fixed-point horizontal partial occupancy

## Status

This note records the independently audited zero-payment layer of R33 Role 10.
It refines the characteristic-five fixed-point family from
`affine_prefix_fixed_point_half_slice.md` by one explicit horizontal two-fold
set map and gives an exact raw support-and-slope partition by the number of
full fibers.

It is not a semantic C1--C9 first-match theorem. It determines neither the
earlier-owner count `e_B` nor the retained C3 set, and it gives no finite or
asymptotic ledger payment, Grand parent, recurrence, or official-score
movement. The official score remains `0/2`.

The publication base is
`origin/main@9908454995f3f195cfe748f35a1135211609d066`. Every pinned
dependency file is byte-identical to the source interface at
`6f4e918f27a11995d3951f4ebe7546d4add0f345`. At publication review, the
only live open PR heads were #986 at
`0b0fddc7d421b2469c58031b206711934a5bad93` and #987 at
`335b9634074fe3a1650749be5985b15e7c8b36ed`; neither touches this source
family or specialization.

## Source family

For every integer `B >= 2`, let

```text
F_B = GF(5^(3B)), n = 4B, k = 2B-1, a = 2B = k+1.
```

Choose an `F_5`-basis

```text
a_1,u_1,v_1,...,a_B,u_B,v_B
```

of `F_B`, put `p=a_1`, and use the domain

```text
D_B = {a_i + eps*u_i + eta*v_i :
       1 <= i <= B and eps,eta in {0,1}}.
```

Let `P_B` be the `2B`-subsets containing `p` and containing neither local
diagonal when a four-point block has local size two. With

```text
Q(y) = 1 + 4y + 4y^2 + 4y^3 + y^4,
c_B = [y^(2B)] Q(y)^B,
```

the inherited fixed-point theorem gives `|P_B|=c_B/2`. The locator coefficient

```text
c_1(S) = -sum_(x in S) x
```

is injective on `P_B`, and each support supplies an exact nontrivial RS witness
at its distinct slope.

## Horizontal refinement

Define the set map

```text
pi_B(a_i + eps*u_i + eta*v_i) = a_i + eta*v_i.
```

It has `2B` fibers, each of size two. For `S in P_B`, let `f(S)` be the
number of full fibers. Then the canonical partial-occupancy parameters are

```text
t = 0, m = f, p_partial = r = 2B - 2f.
```

The symbol `p_partial` is distinct from the planted point `p=a_1`.

In local order `00,10,01,11`, the unrestricted allowed-block and planted
first-block enumerators are

```text
G(y,x) = 1 + 4y + 2(1+x)y^2 + 4xy^3 + x^2y^4,
H(y,x) = y + (1+x)y^2 + 3xy^3 + x^2y^4.
```

Writing

```text
P_B,f = {S in P_B : f(S)=f},
N_B,f = |P_B,f|,
```

independent local multiplication gives

```text
N_B,f = [y^(2B)x^f] H(y,x) G(y,x)^(B-1).          (1)
```

The profile values for the two brute-force cases are

```text
B=2: (N_B,0,N_B,1,N_B,2) = (2,20,3),
B=3: (N_B,0,N_B,1,N_B,2,N_B,3) = (4,108,162,10).
```

## Exact raw add-back and slope images

The profile families partition `P_B`, so

```text
sum_(f=0)^B N_B,f = c_B/2.                         (2)
```

Because the inherited map `S -> c_1(S)` is injective, its restrictions remain
injective and the profile slope images are pairwise disjoint. Thus, with

```text
Z_B,f = c_1(P_B,f),
```

one has

```text
|Z_B,f| = N_B,f,
disjoint_union_f Z_B,f = c_1(P_B),
realized-image mean = N_B,f/|Z_B,f| = 1            (3)
```

for every nonempty profile. Equations (1)--(3) are raw structural identities.
They do not place any profile in an actual semantic owner class.

## Raw exponent and denominator

Let `M_B=max_f N_B,f`. The polynomial `Q` is symmetric unimodal, convolution
preserves this property, and `c_B` is the largest coefficient of `Q^B`.
Therefore

```text
14^B/(4B+1) <= c_B <= 14^B,
c_B/(2(B+1)) <= M_B <= c_B/2,
```

and hence

```text
lim_(B->infinity) (1/(4B)) log M_B = (1/4) log 14. (4)
```

This is a raw count exponent. The challenge denominator is
`|F_B|=5^(3B)`, so the corresponding full-challenge mass exponent is instead

```text
(1/4) log(14/125) < 0.
```

These exponents must not be conflated.

The map `pi_B` is source-valid as a polynomial set map by interpolation on the
finite domain, with a representative of degree at most `4B-1`. Neither this
note nor its verifier asserts a degree-two representative or a locator
composition through `pi_B`.

## Replay

Run

```bash
python3 experimental/scripts/verify_affine_prefix_fixed_point_horizontal_partial_occupancy.py
python3 -O experimental/scripts/verify_affine_prefix_fixed_point_horizontal_partial_occupancy.py
```

Both outputs must equal the checked-in expected transcript. The verifier pins
the inherited fixed-point theorem and the generic partial-occupancy interface,
checks the claim's semantic nonclaims, reconstructs every local enumerator,
checks exact profile rows for `2 <= B <= 10`, brute-forces `B=2,3`, verifies
the add-back and image-size identities, and rejects seventeen semantic
mutations. A separate tamper replay also rejected source-hash, semantic-owner,
and expected-output changes.

## Nonclaims and remaining wall

This note does not prove:

- an actual C1, C2, C3, or C1--C9 semantic owner for any `P_B,f`;
- a value of `e_B`, survival, or extinction of the planted family;
- an empty retained C3 set or a semantic C3 exponent;
- a degree-two folding polynomial or locator composition;
- a finite or asymptotic ledger payment;
- Grand MCA hard input 2, a Grand List theorem, or recurrence;
- a theorem in another characteristic, field family, or projective challenge
  set containing an infinite slope;
- any official-score movement.

The exact remaining wall is a literal source-valid semantic classifier and
first-match order for the raw profile images. It must determine the earlier
owner count and the retained set without charging repeated support labels as
new MCA slopes. Until that wall is crossed, this refinement has zero payment.
