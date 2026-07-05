#!/usr/bin/env python3
# EXPERIMENTAL -- verification of the lattice census dictionary and the
# near-rational dichotomy on a small field (the in-paper proofs are self-contained).
import itertools, random
from math import comb

p = 13
F = range(p)
n, K = 8, 3
D = [1,2,3,4,5,6,7,8]           # 0 not in D
def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%p
    return r
def polymod_deg(a):
    d=len(a)-1
    while d>=0 and a[d]==0: d-=1
    return d
def ev(a,x):
    r=0
    for c in reversed(a): r=(r*x+c)%p
    return r
def interp_deg(pts):            # degree of interpolant through pts [(x,y)]
    xs=[x for x,_ in pts]
    # Lagrange
    m=len(pts)
    coef=[0]*m
    for i,(xi,yi) in enumerate(pts):
        num=[1]
        den=1
        for j,(xj,_) in enumerate(pts):
            if i==j: continue
            num=polymul(num,[(-xj)%p,1]); den=den*(xi-xj)%p
        inv=pow(den,p-2,p)
        for t in range(len(num)): coef[t]=(coef[t]+yi*num[t]*inv)%p
    return polymod_deg(coef)

random.seed(5)
for trial in range(200):
    m = random.choice([4,5])
    w = m-K; omega = n-m
    U = [random.randrange(p) for _ in D]
    # census by brute force: m-subsets T with interpolant degree < K
    census = 0
    for T in itertools.combinations(range(n), m):
        if interp_deg([(D[i],U[i]) for i in T]) < K: census += 1
    # minimal weighted degree d1 of M_U: search all (W,N) with small wdeg
    # wdeg(W,N)=max(deg W, deg N-(K-1)); search d from 0..w for a nonzero element
    d1 = None
    for d in range(0, n):
        # W deg<=d, N deg<=d+K-1, W(x)U(x)=N(x) for all x: linear system
        # unknowns: W coeffs (d+1) + N coeffs (d+K)
        import numpy as np
        rows=[]
        for i,x in enumerate(D):
            row=[]
            for j in range(d+1): row.append(pow(x,j,p)*U[i]%p)
            for j in range(d+K): row.append((-pow(x,j,p))%p)
            rows.append(row)
        A=np.array(rows,dtype=int)%p
        # rank over F_p by Gaussian elimination
        M=A.copy(); r=0; cols=M.shape[1]
        for c in range(cols):
            piv=None
            for rr in range(r,M.shape[0]):
                if M[rr,c]%p: piv=rr; break
            if piv is None: continue
            M[[r,piv]]=M[[piv,r]]
            inv=pow(int(M[r,c]),p-2,p)
            M[r]=M[r]*inv%p
            for rr in range(M.shape[0]):
                if rr!=r and M[rr,c]%p: M[rr]=(M[rr]-M[rr,c]*M[r])%p
            r+=1
            if r==M.shape[0]: break
        if cols>r:  # nontrivial kernel => element of wdeg <= d exists
            d1=d; break
    balanced = d1 >= w+1
    if not balanced:
        # dichotomy: census should be 0 or C(n-wt,m) for a codeword within distance d1
        best=None
        for cw in itertools.product(F,repeat=K):
            wt=sum(1 for i,x in enumerate(D) if ev(list(cw),x)!=U[i])
            if wt<=w: best=wt if best is None else min(best,wt)
        pred = comb(n-best,m) if best is not None else 0
        assert census==pred, (trial,m,d1,census,pred,best)
print("dichotomy verified on 200 random small-field instances (unbalanced branch exact; balanced branch unconstrained)")
