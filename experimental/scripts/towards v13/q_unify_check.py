#!/usr/bin/env python3
# EXPERIMENTAL -- verification of the (Q)-unification:
# (i) witness lattice profile d1 = w+1 (generic z), second generator = (Q, beta - R)
#     with X^n = P_z Q + R;
# (ii) fiber(z) = #{A: deg A <= omega-w-1, Q + A | X^n - beta}  (prescribed-prefix divisors);
# (iii) fiber sizes constant along the twisted mu_n-action z_j -> zeta^j z_j.
import itertools, random
from math import comb

p = 17
# D = full multiplicative subgroup of order n=8 (8 | 16), beta = 1
n = 8
g0 = 3
H = sorted({pow(g0,(p-1)//n*i,p) for i in range(n)})
D = H; beta = 1   # Lambda_D = X^n - 1
K = 3

def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%p
    return r
def pdeg(a):
    d=len(a)-1
    while d>=0 and a[d]==0: d-=1
    return d
def pdivmod(b,a):
    b=list(b)+[0]; q=[0]*(max(len(b)-len(a)+1,1))
    while pdeg(b)>=pdeg(a)>=0:
        sh=pdeg(b)-pdeg(a); c=b[pdeg(b)]*pow(a[pdeg(a)],p-2,p)%p
        q[sh]=c
        for i,x in enumerate(a): b[i+sh]=(b[i+sh]-c*x)%p
    return q, b
def lam(S):
    W=[1]
    for x in S: W=polymul(W,[(-x)%p,1])
    return W

random.seed(3)
for m in (5,6):
    w = m-K; om = n-m
    # brute-force fibers of prefix map: T -> coefficients of Lambda_T at X^{m-1..m-w}
    fib = {}
    for T in itertools.combinations(range(n), m):
        L = lam([D[i] for i in T])
        z = tuple(L[m-j] for j in range(1,w+1))
        fib[z] = fib.get(z,0)+1
    # (ii) prescribed-prefix divisor identity for random z (including empty fibers)
    ok=0; tot=0
    for _ in range(60):
        z = tuple(random.randrange(p) for _ in range(w))
        P = [0]*(m+1); P[m]=1
        for j in range(1,w+1): P[m-j]=z[j-1]
        Xn = [0]*(n+1); Xn[n]=1
        Q,R = pdivmod(Xn, P)
        Q = Q[:om+1]
        # count A with deg A <= om-w-1 and Q+A | X^n - beta
        cnt=0
        rng = om-w  # number of free coeffs = om-w (degrees 0..om-w-1)
        for A in itertools.product(range(p), repeat=max(rng,0)):
            W=list(Q)
            for i,a in enumerate(A): W[i]=(W[i]+a)%p
            # W | X^n - beta ?
            XnB=[( -beta)%p]+[0]*(n-1)+[1]
            _,rem = pdivmod(XnB, W)
            if pdeg(rem)<0: cnt+=1
        tot+=1
        if cnt == fib.get(z,0): ok+=1
    print(f"m={m} w={w}: prescribed-prefix divisor identity: {ok}/{tot}")
    # (iii) orbit constancy under z_j -> zeta^j z_j
    zeta = pow(g0,(p-1)//n,p)
    bad=0
    for z,c in fib.items():
        z2 = tuple(z[j]*pow(zeta,j+1,p)%p for j in range(w))
        if fib.get(z2,0)!=c: bad+=1
    print(f"        orbit constancy violations: {bad}/{len(fib)}")
