# Canonical-error mixed complete-fiber shadow packing

**Status:** PROVED arbitrary-received-word theorem.  The result counts one
literal list globally across all generators, syndromes, and projective residue
rays that arise from that received word.  Its deployed cap is not yet small
enough to close the current disjoint residual ledger.

## Theorem

Let `F` be a field, let `H` be an `n`-point evaluation set, and fix integers
`1 <= K <= m <= n`.  For an arbitrary received word `U : H -> F`, let

```text
L(U) = {P in F[X] : deg(P)<K and P agrees with U at least m times}.
```

Fix a total order on `H`.  For each `P in L(U)`, let `S_P` be its first
exactly `m` agreement points and put

```text
E_P = H \ S_P,                 |E_P| = t := n-m.
```

Then distinct `P,Q in L(U)` satisfy

```text
|E_P intersect E_Q| <= Delta := n-2m+K-1.             (1)
```

Partition `H` into `N` disjoint blocks of size `B`.  Let `f(P)` be the number
of complete blocks contained in `E_P`, put `s=floor(Delta/B)`, and let `M_f`
count list polynomials with `f(P)=f`.  Then

```text
sum_{f>=s+1} M_f binom(f,s+1) <= binom(N,s+1).          (2)
```

Unlike the fixed-weight packing already used in the dyadic complete-fiber
ledger, (2) is mixed-weight: its shadows are disjoint across different values
of `f` as well as within each fixed layer.

## Proof

For distinct `P,Q`, every point of `S_P intersect S_Q` is a root of the
nonzero polynomial `P-Q`, whose degree is at most `K-1`.  Hence

```text
|S_P intersect S_Q| <= K-1.
```

Taking complements inside `H` gives

```text
|E_P intersect E_Q|
  = n-|S_P union S_Q|
  = n-2m+|S_P intersect S_Q|
  <= n-2m+K-1,
```

which proves (1).

For (2), attach to `P` every `(s+1)`-subset of the complete-block labels in
`E_P`.  If one such shadow belonged to two distinct list polynomials, their
canonical error complements would share at least `(s+1)B>Delta` deployed
points, contradicting (1).  Counting the pairwise disjoint shadows proves
(2).

The canonical first-`m` rule is load-bearing only for disjoint ownership: it
makes every `E_P` a size-`t` object even when `P` has more than `m`
agreements.  No fixed generator or projective-ray hypothesis is used.

## Deployed q64 and q32 consequences

For the deployed Grand List row,

```text
p       = 2,130,706,433
n       = 2,097,152
K       = 1,048,576
m       = 1,116,047
t       =   981,105
Delta   =   913,633
T       = 274,854,110,496,187,592.
```

At q64, `B=32,768`, `N=64`, and `s=27`.  Since `t` permits at most 29
complete blocks, (2) becomes

```text
M_28 + 29 M_29 <= binom(64,28)
                  = 1,118,770,292,985,239,888.         (3)
```

In particular, uniformly for every received word,

```text
M_29 <= 38,578,285,965,008,272 < T.                    (4)
```

At q32, `B=65,536`, `N=32`, and `s=13`, so the top-cell shadow count is

```text
P_32 = binom(32,14) = 471,435,600.
```

Let `Z` count q64 `f=28` error complements whose 28 labels are fourteen
natural q32 pairs.  Disjointness of these paired 28-shadows from every q64
`f=29` 28-shadow gives

```text
M_29 + Z <= P_32 + floor((binom(64,28)-P_32)/29)
             = 38,578,286,420,187,472 < T.             (5)
```

The first surviving cell under this shadow theorem is nonpaired q64 `f=28`,
whose direct ceiling is

```text
binom(64,28)-binom(32,14)
  = 1,118,770,292,513,804,288.                         (6)
```

## Consumer status and nonclaims

The integrated dyadic complete-fiber theorem already proves the underlying
agreement-support overlap bound and fixed-weight packings.  The delta here is
the complement conversion and the single mixed-weight shadow ledger (2)--(5).
The integrated monomial `g=X^67,472` packet remains much sharper on its
special periodic cells.

- Equations (4)--(5) are global for one arbitrary received word, not per ray.
- Being below the full target `T` does not by itself close a first-match
  branch after other disjoint populations have consumed part of `T`.  The
  present q64 complete-fiber caps still exceed the current residual allowance.
- No owner theorem placing every remaining `c=0` error in these two cells is
  asserted.  Nonpaired q64 `f=28`, lower q64 weights, generic q128 cells, and
  the complete affine-rank-at-least-16 parent remain open.
- No `F_p`/`F_(p^6)` shell compiler, Grand List, Grand MCA, finite deployed
  adjacent row, or official score claim follows.  The score remains `0/2`.

The next local target is a source-valid refinement of the nonpaired q64
`f=28` layer, or an owner/compiler that combines the mixed-shadow cap with the
current disjoint ledger without double counting.

## Replay

```bash
python3 experimental/scripts/verify_canonical_error_mixed_shadow_packing.py
python3 -O experimental/scripts/verify_canonical_error_mixed_shadow_packing.py
python3 experimental/scripts/verify_canonical_error_mixed_shadow_packing.py --tamper-selftest
```
