# C9 weighted two-channel remainder compiler

## Status

`PROVED / STRICT SUBREGIME / POST-#488 SUPPORT`

This note proves an exact weighted first-failure bound at and below the
`P_o=2h` wall of the near-norm-gate remainder packet.  It counts every
compatible even-channel lift.  The new input is a two-channel separation
inequality for one representative from each nonempty odd-remainder class.

It does not reach the central fixed-linear-deficit scales where `P_o=o(h)`.

## Setup

Let `n=2h>=4` be a power of two.  Let `p=1 mod 2h` be prime, let `zeta` have
order `2h` in `F_p^*`, and put `eta=zeta^2`.  Let `I` be a consecutive cyclic
interval in `Z/(2h)Z` of length at most `h`.  Define

```text
O={u in Z/hZ: 2u+1 in I},   q=|O|,
E={v in Z/hZ: 2v   in I},   e=|E|.
```

Then `q+e=|I|<=h`, both inherited sets are consecutive cyclic intervals, and
`|q-e|<=1`.

For `0<=r<2h`, fix a one-sided list

```text
A_r in {{0},{0,1},{0,-1}},
w_r=max A_r-min A_r in {0,1},
W=sum_r w_r <= 2h.
```

Let `F` be any family of polynomials

```text
f(X)=sum_{r=0}^{2h-1} b_r X^r,   b_r in A_r,
```

such that

```text
f(zeta^k)=0 for k in I,   X^h+1 does not divide f.        (1)
```

Any additional common restriction, including fixed weight, is allowed.  Write

```text
f=A+X^h B,   d_f=A-B,   s_f=A+B.
```

Put

```text
P_o=p^(2q/h),   P_e=p^(2e/h),   A_o=max{P_o,q+1},

Lambda=max{2(q+e+1), min{A_o+e+1,4A_o}}.                 (2)
```

Let `T(h,E)` be the maximum, over all length-`h` one-sided masks, of the
number of polynomials `r` in that mask satisfying

```text
r(eta^v)=0 for every v in E.                             (3)
```

## Exact finite theorem

### Theorem 1 (weighted two-channel compiler)

```text
Lambda>=W  implies
|F| <= max{1,2W} T(h,E).                                 (4)
```

This is a bound on the full sum over odd remainders, not merely on the number
of distinct remainders.

### Proof

Partition `F` by `d_f`.  Fix one class, choose `f*` in it, and write

```text
f-f*=(1+X^h)r.                                           (5)
```

At an even inherited root, (5) gives `2r(eta^v)=0`; since `p` is odd,
`r(eta^v)=0`.  Coordinatewise, `r` lies in a length-`h` one-sided increment
mask.  Hence every entire remainder class has size at most `T(h,E)`.  No even
lift has been discarded.

Now choose one representative from each nonempty class.  For two distinct
representatives `f,g`, put

```text
Delta A=A_f-A_g,      Delta B=B_f-B_g,
delta=Delta A-Delta B,   tau=Delta A+Delta B.             (6)
```

Distinct remainder classes give `delta!=0`.  The inherited equations give

```text
delta(zeta eta^u)=0 for u in O,
tau(eta^v)=0 for v in E.                                 (7)
```

The odd irreducible resultant bound and the odd Vandermonde support bound give

```text
||delta||_2^2 >= A_o.                                    (8)
```

If `tau!=0`, the even Vandermonde support bound gives

```text
||delta||_2^2+||tau||_2^2 >= A_o+e+1.                    (9)
```

If `tau=0`, then `Delta B=-Delta A`, so `delta=2r` for an odd-root
polynomial `r`, and

```text
||delta||_2^2+||tau||_2^2 >= 4A_o.                       (10)
```

Independently, `f-g` vanishes on the full consecutive window.  Its evaluation
matrix is a column-scaled Vandermonde matrix, so

```text
d_H(f,g)>=q+e+1.                                         (11)
```

Because every active list has width one, coordinatewise

```text
||delta||_2^2+||tau||_2^2 = 2d_H(f,g).                   (12)
```

Equations (9)-(12) prove

```text
2d_H(f,g)>=Lambda.                                       (13)
```

Delete fixed coordinates and encode the representatives as binary words of
length `W`.  If `Lambda>=W`, their pairwise distance is at least `W/2`.
Mapping them to normalized sign vectors gives a positive semidefinite Gram
matrix of rank at most `W`, diagonal one, and nonpositive off-diagonal
entries.  The equality-line calculation yields at most `2W` representatives
when `W>0`; for `W=0` there is at most one.  Multiplying by the complete
same-remainder ceiling proves (4).

The even channel in (9) uses only its unconditional MDS support.  No false
irreducible-resultant estimate is assigned to the reducible polynomial
`X^h-1`.

## Polynomial strip below `P_o=2h`

Fix `kappa_0,epsilon>0`.  If

```text
kappa_0 h <= e <= h/2,   P_e >= (1+epsilon)h,             (14)
```

the pure-window theorem from the integrated near-norm-gate packet gives

```text
T(h,E) <= B_{kappa_0,epsilon}(h),                         (15)
```

where, with

```text
r_epsilon=(1+epsilon)/(1+epsilon/2),
H_0=ceil(2 log((1+epsilon)h)/(kappa_0 log r_epsilon))+2,
```

one may take

```text
B_{kappa_0,epsilon}(h)
 = 2+max{1,2/epsilon} ceil(log_2 h) 2^(2H_0).             (16)
```

Thus (4) is polynomial whenever (14) and `Lambda>=W` hold.

In particular, fix `kappa>0` and suppose

```text
q,e>=kappa h-1,   |q-e|<=1,   q+e<=h,
2h-e-1 <= P_o <= 2h.                                     (17)
```

For all sufficiently large `h`, (17) implies `Lambda>=2h>=W` and (14) with
`kappa_0=kappa/2`, `epsilon=1/4`.  Therefore `|F|=h^O_kappa(1)` uniformly over
all masks, windows, and additional common restrictions.  In worst width this
moves the local polynomial threshold from `P_o>2h` to

```text
P_o>=2h-e-1.                                              (18)
```

If `e/h -> theta`, the threshold is `(2-theta)h+O(1)`, reaching
`(3/2+o(1))h` at the balanced edge.

More generally, fix a nonnegative defect sequence `s_h=o(h)`.  Under the same
fixed-density assumptions `q,e>=kappa h-1`, `|q-e|<=1`, and `q+e<=h`, if
`P_o<=2h` and

```text
P_o+e+1 >= 2h-s_h,                                       (19)
```

then `|F|=exp(o(h))`.  If `Lambda<W`, split representatives by their active
weight.  Their fixed-profile deficit is at most
`(W-Lambda)/4+O(1)=o(h)`, so the integrated block-profile theorem pays each
of the `W+1` strata subexponentially.

## Remaining wall

For fixed `0<rho<1/2` in the central split-prime regime,

```text
q/h,e/h=rho+o(1),   P_o=o(h),
Lambda=4rho h+o(h),   W=2h                               (20)
```

in the worst mask.  The remaining gap is the fixed-linear quantity

```text
W-Lambda=2(1-2rho)h+o(h).                                (21)
```

Pairwise distance cannot pay it: ordinary binary packing already allows
exponentially many words at the numerical distance supplied by (13).  The
next exact target is a genuinely higher-order transversal theorem:

```text
log A(h;O,E)=o(h),                                       (22)
```

where `A(h;O,E)` is the largest number of nonempty odd-remainder classes in a
one-sided common-window fiber.  Together with the same-remainder compiler,
this would give the recursive full-fiber bound

```text
T(2h,I) <= (A(h;O,E)+1) T(h,E).                          (23)
```

## Nonclaims

- This does not prove (22), the central fixed-linear transversal theorem, or
  a full one-sided fiber theorem.
- It proves no C1-C8 emission, profile-atlas exhaustion, residual-to-full
  compiler, ray compiler, Sidon or major-arc payment, add-back theorem, full
  C9 theorem, deployed finite row, or prize theorem.
- Counting only distinct odd remainders is invalid; the factor `T(h,E)` is
  essential.
- A termwise even-channel resultant bound is not used and would be false
  without recursive first-failure analysis.

## Verification

`experimental/scripts/verify_asymptotic_c9_weighted_two_channel_remainder.py`
exhausts every one-sided mask and every inherited half-window at length four,
then checks representative masks at length eight.  It verifies complete
remainder-class counts, every cross-remainder word pair in those families,
the two-channel energy identities and separation, the full-window support
floor, and the final weighted inequality.  All threshold comparisons use
integer power inequalities; the verifier contains no floating tolerance.
