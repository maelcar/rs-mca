# Split-locator star-configuration flat intersection

**Status:** PROVED.

**Base:** `origin/main@9262f63cf093a7510a2df435f220390f59e2bcd5`.

## Claim

Let `K` be a field, let `Q subset K` consist of `N` distinct points, and let
`0 <= k <= N`.  Put

```text
V_k = K[X]_{<= k}.
```

For a `k`-subset `R subset Q`, write

```text
L_R(X) = product_{r in R} (X-r).
```

The squarefree degree-`k` split-locator star configuration is

```text
S_k(Q) = { [L_R] in P(V_k) : R subset Q and |R| = k }.
```

The locator points are distinct because their monic representatives have
distinct root sets.  Equivalently, if

```text
H_a = { [f] in P(V_k) : f(a) = 0 },
```

then `S_k(Q)` is the set of `k`-fold intersections of the evaluation
hyperplanes `H_a`, `a in Q`.  Distinctness of the points of `Q` makes every
set of at most `k+1` evaluation conditions independent.

### Theorem (sharp flat-intersection bound)

For every integer `d` with `0 <= d <= k` and every projective `d`-flat
`Pi subset P(V_k)`,

```text
|Pi intersect S_k(Q)| <= binom(N-k+d, d).                (1)
```

The bound is sharp for every admissible triple `(N,k,d)`: equality is attained
by a `d`-flat obtained by fixing `k-d` roots.

## Deletion and restriction

Fix `a in Q`.  Two elementary identities drive the proof.

1. A locator contains `a` exactly when its projective point lies in `H_a`:

   ```text
   S_k(Q) intersect H_a
     = { [(X-a)L_T] : T subset Q\{a}, |T|=k-1 }.         (2)
   ```

   Indeed, `L_R(a)=0` if and only if `a in R`, since all points of `Q` are
   distinct.

2. Multiplication by `X-a` is a linear isomorphism

   ```text
   V_{k-1} -> { f in V_k : f(a)=0 }.
   ```

   Its projectivization identifies the right side of (2) with
   `S_{k-1}(Q\{a})` in `P(V_{k-1})`.

The complementary locator set is exactly the deletion

```text
S_k(Q) \ H_a = S_k(Q\{a}).                              (3)
```

Here the configuration on the right remains in `P(V_k)`.

## Proof of the theorem

Define

```text
B(N,k,d) = binom(N-k+d, d).
```

We use strong induction on `N`, with the exact boundary cases below.  It
therefore remains to consider

```text
k >= 2,  1 <= d <= k-1,  N >= k+1.
```

Choose any `a in Q`.

### Case 1: `Pi subset H_a`

Since `H_a` is a hyperplane in `P(V_k)`, this case forces `d <= k-1`.
Division by `X-a` maps `Pi` projectively and linearly to a `d`-flat in
`P(V_{k-1})`.  Since `Pi subset H_a`, identity (2) shows that every locator in
`Pi` contains `a`; hence induction for `(N-1,k-1,d)` gives

```text
|Pi intersect S_k(Q)|
  <= B(N-1,k-1,d)
   = binom((N-1)-(k-1)+d, d)
   = B(N,k,d).                                           (4)
```

### Case 2: `Pi` is not contained in `H_a`

Now `Pi intersect H_a` is a projective `(d-1)`-flat.  Partition the locator
points in `Pi` according to whether their root set contains `a`.

The containing part is carried by division by `X-a` to a subset of a
`(d-1)`-flat meeting `S_{k-1}(Q\{a})`.  Induction gives

```text
|Pi intersect H_a intersect S_k(Q)|
  <= B(N-1,k-1,d-1)
   = binom(N-k+d-1, d-1).                                (5)
```

The avoiding part lies in `Pi intersect S_k(Q\{a})`.  Since `N-1 >= k`,
induction for `(N-1,k,d)` gives

```text
|Pi intersect S_k(Q\{a})|
  <= B(N-1,k,d)
   = binom(N-k+d-1, d).                                  (6)
```

The two parts are disjoint.  Adding (5) and (6), then applying Pascal's
identity, yields

```text
|Pi intersect S_k(Q)|
  <= binom(N-k+d-1,d-1) + binom(N-k+d-1,d)
   = binom(N-k+d,d).
```

This proves (1).

## Exact boundary cases

The induction bases are literal, including all overlaps among them.

| Boundary | Configuration and bound |
| --- | --- |
| `d=0` | A projective point meets a set of projective points in at most one point, and `binom(N-k,0)=1`. |
| `k=0` | Necessarily `d=0`; `S_0(Q)={[1]}` in `P(V_0)=P^0`, and `binom(N,0)=1`. |
| `N=k` | There is only `L_Q`, while `binom(d,d)=1` for every `0 <= d <= k`. |
| `d=k` | The only projective `k`-flat in `P(V_k)` is the whole space; it contains all `binom(N,k)=binom(N-k+k,k)` locators. |

Thus the claimed number is exact, not merely an induction convention, at
`d=0`, `k=0`, and `N=k`.

## Sharpness by a fixed root star

Fix any subset `C subset Q` of size `k-d`, and put

```text
G_C(X) = product_{c in C} (X-c),
W_C    = G_C * K[X]_{<= d} subset V_k.
```

Multiplication by the nonzero polynomial `G_C` is injective, so `W_C` has
vector-space dimension `d+1` and `P(W_C)` is a projective `d`-flat.  A monic
locator `L_R` lies projectively in `W_C` if and only if `G_C` divides `L_R`.
Because both polynomials split into distinct linear factors from `Q`, this is
equivalent to `C subset R`.  Consequently,

```text
|P(W_C) intersect S_k(Q)|
  = #{R subset Q : |R|=k and C subset R}
  = binom(N-(k-d), d)
  = binom(N-k+d, d).                                     (7)
```

This proves sharpness simultaneously in the interior and in all boundary
cases.  In particular, the extremizer is the common star obtained by fixing
`k-d` roots; no uniqueness or classification of all extremizers is asserted.

## Relation to `thm:capf-fixeddim`

The existing theorem `thm:capf-fixeddim` in
`experimental/cap25_cap_v13_raw.tex` bounds a gcd-trivial `d`-flat by
`binom(N,d)`, and bounds a flat with a known common root set `C_0` by
`binom(N-|C_0|,d)`.  The theorem above uses the full star-configuration
deletion/restriction structure to give the sharper uniform value
`binom(N-k+d,d)` for every `d`-flat, without assuming a common root in
advance.  Formula (7) shows that this stronger uniform bound cannot be
improved over the class of all projective `d`-flats.  It does not supersede
stronger bounds already proved on narrower families such as gcd-trivial
lines/planes or prefix-coordinate flats.

This remains a locator-configuration theorem.  When `d` grows with the RS
parameters, the binomial bound itself may still be too large for a target
ledger; the theorem does not supply a conversion from a source fiber to a
specific flat.

## Reproducibility

Run

```text
python3 experimental/scripts/verify_split_locator_star_flat_intersection.py
python3 -O experimental/scripts/verify_split_locator_star_flat_intersection.py
```

The stdlib-only verifier checks:

- both induction recurrences and their parameter ranges;
- the `d=0`, `k=0`, `N=k`, and `d=k` boundary identities;
- the fixed-`k-d`-root sharp count for all parameters in a bounded grid;
- direct prime-field locator coordinates, every projective `d`-flat in each
  recorded small instance, the global maximum, and the explicit sharp flat.

The finite-field census is an audit of the proof, not a substitute for the
field-uniform argument above.  Its deterministic output is recorded at
`experimental/data/certificates/split-locator-star-flat-intersection/verifier_output.txt`.

## Scope and explicit nonclaims

This note proves only the abstract projective flat-intersection theorem above.
It does **not** claim any of the following:

- an RS source-to-flat bridge or any other unproved source bridge;
- common-star attainment `28` in a separate deployed or source-derived model;
- average Johnson degree `<= 60`;
- a deployed-row threshold, prize result, leaderboard movement, or full
  RS-MCA conclusion;
- a classification of extremal flats;
- an abstract linear-map projective-fiber corollary.
