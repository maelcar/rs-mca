#!/usr/bin/env python3
# EXPERIMENTAL cross-check of the rank-one census model margins (rem in the
# prize insert); the in-paper numbers are certified by the entropy sandwich.
from math import lgamma, log, log2
def l2c(N, m): return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)
n, k = 2**21, 2**20
lpKB = log2(2**31 - 2**24 + 1); lpM = log2(2**31 - 1)
rows = [("KB MCA   ", 1116044, k+1, 6*lpKB), ("KB list  ", 1116047, k, 6*lpKB),
        ("M31 MCA  ", 1116022, k+1, 4*lpM), ("M31 list ", 1116023, k, 4*lpM)]
print("rank-one census model at the conjectured first safe agreement a0+1:")
for name, m, K, lq in rows:
    w = m - K
    model = l2c(n, m) - (w-1)*lq
    budget = lq - 128          # log2 of per-line budget 2^-128 q
    print(f"  {name} m={m} w={w}: log2 model #R1 = {model:>12.0f}; "
          f"log2 budget = {budget:+.0f}; exclusion window = {budget-model:,.0f} bits")
