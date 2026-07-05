#!/usr/bin/env python3
# EXPERIMENTAL cross-check of the packing-bound corollary (the proof is the
# entropy sandwich + the two-line Johnson-type counting argument).
from math import lgamma, log, log2
def l2c(N, m): return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)
n, k = 2**21, 2**20
rows = [("KB MCA", 1116043, 67466, log2(2**31-2**24+1)),
        ("KB list", 1116046, 67470, log2(2**31-2**24+1)),
        ("M31 MCA", 1116021, 67444, log2(2**31-1)),
        ("M31 list", 1116022, 67446, log2(2**31-1))]
for name, m, w, lp in rows:
    d = (w+2)//2                     # delta = ceil((w+1)/2)
    pack = l2c(n, m-d+1) - l2c(m, d-1)
    triv = l2c(n, m)
    conj = triv - w*lp               # conjectured log2 of C(n,m)/p^w
    print(f"{name}: m={m}, w={w}, delta={d}")
    print(f"   log2 trivial C(n,m)      = {triv:>12.0f}")
    print(f"   log2 packing bound       = {pack:>12.0f}   (gain {triv-pack:+.0f} bits)")
    print(f"   log2 conjectured average = {conj:>12.0f}   (packing excess {pack-conj:+.0f} bits)")
