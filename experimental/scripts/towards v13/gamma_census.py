#!/usr/bin/env python3
# EXPERIMENTAL -- calibration evidence only; enters no proof.
# Exact collision-gap values Gamma_r from the group-algebra fiber censuses.
import numpy as np
from math import comb
from fractions import Fraction

def census(p, N, m, w):
    g = 2
    while len({pow(g, i, p) for i in range(1, p)}) != p-1: g += 1
    H = sorted({pow(g, (p-1)//N*i, p) for i in range(N)})
    cnt = np.zeros((m+1,) + (p,)*w, dtype=np.int64)
    cnt[(0,)+(0,)*w] = 1
    for a in H:
        sh = [pow(a, i, p) for i in range(1, w+1)]
        for j in range(m, 0, -1):
            t = cnt[j-1]
            for ax, s in enumerate(sh): t = np.roll(t, s, axis=ax)
            cnt[j] += t
    return cnt[m].ravel()

print("exact Gamma_r = p^{w(r-1)} * sum mu^r  (uniform => 1); max/mean = lim Gamma_r^{1/r}")
for (p, N, m, wmax) in [(17, 16, 8, 3), (41, 20, 10, 3), (257, 64, 34, 2)]:
    C = comb(N, m)
    print(f"\np={p}, N={N}, m={m}:")
    for w in range(1, wmax+1):
        F = census(p, N, m, w)
        out = []
        for r in (2, 3, 4):
            # Gamma_r = p^{w(r-1)} * sum (F/C)^r  -- exact rational
            s = sum(Fraction(int(x))**r for x in F if x)
            G = Fraction(p)**(w*(r-1)) * s / Fraction(C)**r
            out.append(f"G{r}={float(G):.6f}")
        mx = Fraction(int(F.max())) * Fraction(p)**w / Fraction(C)
        print(f"  w={w}: " + "  ".join(out) + f"  max/mean={float(mx):.4f}")
