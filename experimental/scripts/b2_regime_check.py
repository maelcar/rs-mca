#!/usr/bin/env python3
"""
b2 regime check: 'count of size-b t-null blocks <= n^3' is REGIME-RESTRICTED.
count_b ~ C(n,b)/q^t, so the bound holds iff log2 C(n,b) <= t*log2 q + 3 log2 n.
At PRIZE scale it holds for b<~n/4 but FAILS at b~n/2 -> the prize-relevant regime
is b~t (first moment <<1), NOT b~n/2 (where a small-n toy misleadingly 'passes').
"""
import math
def log2binom(n,b):
    if b<0 or b>n: return float('-inf')
    return (math.lgamma(n+1)-math.lgamma(b+1)-math.lgamma(n-b+1))/math.log(2)

print("PRIZE  n=2^41, t*log2 q ~ 2.15e12, n^3=2^123")
n=2**41; thr=2.15e12 + 3*41
for lbl,b in [("b=t~2^33",2**33),("b=2t~2^34",2**34),("b=2^36",2**36),
              ("b=n/4",n//4),("b=n/2",n//2)]:
    lc=log2binom(n,b)
    print(f"  {lbl:>10}: log2 C={lc:.3e}  count<=n^3? {lc<=thr}  (count~2^{lc-2.15e12:.3e})")

print("\nTOY (32,4,97): threshold=%.2f, n^3=2^15 -- note ALL b 'pass' (small n hides the regime split)"
      % (4*math.log2(97)+3*math.log2(32)))
for b in (5,6,7,13,16):
    lc=log2binom(32,b); fm=lc-4*math.log2(97)
    print(f"  b={b:>2}: log2 C={lc:5.2f}  first_moment~2^{fm:+.2f}  {'(rare-event b~t regime)' if b<8 else '(b~n/2 -- wrong-regime at prize)'}")
