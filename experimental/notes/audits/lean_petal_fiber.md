# Lean: map-smooth agreement arithmetic and cap anchors

## Status
PROVED agreement-window arithmetic / EXPERIMENTAL finite cap anchor / AUDIT.

## Source correspondence

The package follows the source declarations
`lem:map-smooth-fiber` + `prop:map-smooth-cap`, primarily in
`experimental/rs_mca_thresholds.tex` and identically in
`experimental/asymptotic_rs_mca_frontiers.tex`.

## General arithmetic

For every natural `k,a`, Lean proves

```text
a * (k / a + 2) + k % a = k + 2*a.
```

It derives the full source window `k+a+1 ≤ A ≤ k+2a` under the sole necessary
hypothesis `0<a`, and proves `A=k+2a ↔ a∣k`.  The positive-degree hypothesis is
implicit in the source definition of a map-smooth domain; without it the lower
endpoint is false at `a=k=0`.

## Object
- a=2,k=2,N=4,n=8,ℓ=3,A=6 with k+a+1≤A≤k+2a and A=k+2a (a|k)
- L=⌈C(4,3)/2⌉=2
- Cap ⌈L(q−n)/(q−n+k(L−1))⌉ = 4/4 = 1 exact (q−n=2)

## Dual routes
- general agreement bounds: quotient/remainder theorems, not enumeration
- remaining fixed anchors: `native_decide`
- fixed dual checks: `decide`

## Nonclaims
The general result is only the integer agreement arithmetic.  The map-smooth
fiber/list construction and the collision-aware MCA cap remain unformalized;
the list-size and cap declarations below it are still fixed numerical anchors.
