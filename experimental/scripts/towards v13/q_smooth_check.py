#!/usr/bin/env python3
# EXPERIMENTAL -- verification of the twisted-smooth identity
#   1{W | X^n - beta} = 1{W splits squarefree over F_p} * prod_{roots} Phi(xi),
# Phi = (n/(p-1)) sum over the (p-1)/n characters of the quotient, evaluated
# via the coset indicator; plus the exact loss arithmetic at deployed scale.
import itertools, random
from math import log2

p = 41; n = 8                      # 8 | 40, quotient size (p-1)/n = 5
g0 = 6                              # primitive root mod 41
assert len({pow(g0,i,p) for i in range(p-1)})==p-1
H = sorted({pow(g0,(p-1)//n*i,p) for i in range(n)})
alpha = g0                          # coset D = alpha*H, beta = alpha^n
D = sorted({alpha*h % p for h in H}); beta = pow(alpha,n,p)

def Phi(x):                         # exact coset indicator = the 5-character sum
    return 1 if pow(x, n, p) == beta else 0

random.seed(2); ok = tot = 0
for _ in range(4000):
    deg = random.choice([2,3,4])
    W = [random.randrange(p) for _ in range(deg)] + [1]
    roots = [x for x in range(1,p) if sum(c*pow(x,i,p) for i,c in enumerate(W))%p==0]
    # squarefree split over F_p: deg distinct roots
    split = (len(set(roots)) == deg) and all(
        sum(c*pow(x,i,p)*i for i,c in enumerate(W))%p != 0 for x in roots)  # simple roots
    lhs_val = split and all(Phi(x) for x in roots)
    # direct divisibility
    XnB = [(-beta) % p] + [0]*(n-1) + [1]
    b = list(XnB)
    while len(b) >= len(W):
        d = len(b)-1
        while d >= 0 and b[d] == 0: d -= 1
        if d < deg: break
        c = b[d]*pow(W[deg], p-2, p) % p; sh = d - deg
        for i, x in enumerate(W): b[i+sh] = (b[i+sh] - c*x) % p
    rem_zero = all(v == 0 for v in b[:deg]) and all(v==0 for v in b[deg:])
    ok += (bool(lhs_val) == rem_zero); tot += 1
print(f"twisted-smooth identity: {ok}/{tot}")

# exact loss arithmetic at the KoalaBear adjacent pair
w = 67467; om = 981108; h = om - w - 1   # 913640
nc = 1016                                 # quotient characters
freq_bits = om * log2(nc)                 # character-tuple count
sqrt_bits = (h+1)/2 * log2(2**31 - 2**24 + 1)
print(f"frequency layer:  log2(#tuples)  = {freq_bits:,.0f} bits")
print(f"per-term maximum: log2(interval^(1/2)) = {sqrt_bits:,.0f} bits")
print(f"target: 192 bits;  triangle-inequality shortfall ~ {freq_bits+sqrt_bits-192:,.0f} bits")
