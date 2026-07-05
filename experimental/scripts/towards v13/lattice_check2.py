#!/usr/bin/env python3
# EXPERIMENTAL -- verification of: (i) auto-divisibility (W|Lambda_D => W|N),
# (ii) gcd(W1,W2)=1, (iii) the determinant identity W1 N2 - W2 N1 = gamma*Lambda_D,
# (iv) the ray decomposition census = sum_c C(agr_c, m).
import itertools, random
from math import comb
import numpy as np

p = 13
n, K = 8, 3
D = [1,2,3,4,5,6,7,8]

def polymul(a,b):
    r=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%p
    return r
def pdeg(a):
    d=len(a)-1
    while d>=0 and a[d]==0: d-=1
    return d
def ptrim(a): return a[:pdeg(a)+1] if pdeg(a)>=0 else [0]
def ev(a,x):
    r=0
    for c in reversed(a): r=(r*x+c)%p
    return r
def pgcd(a,b):
    a,b=ptrim(a),ptrim(b)
    while pdeg(b)>=0:
        # a mod b
        a=list(a)
        while pdeg(a)>=pdeg(b) and pdeg(a)>=0:
            sh=pdeg(a)-pdeg(b); c=int(a[pdeg(a)])*pow(int(b[pdeg(b)]),p-2,p)%p
            for i,x in enumerate(b): a[i+sh]=(int(a[i+sh])-c*int(x))%p
        a,b=b,ptrim(a)
    return ptrim(a)
def pdivides(a,b):   # a | b ?
    b=list(ptrim(b)); a=ptrim(a)
    while pdeg(b)>=pdeg(a) and pdeg(b)>=0:
        sh=pdeg(b)-pdeg(a); c=int(b[pdeg(b)])*pow(int(a[pdeg(a)]),p-2,p)%p
        for i,x in enumerate(a): b[i+sh]=(int(b[i+sh])-c*int(x))%p
        b=b[:pdeg(b)+1] if pdeg(b)>=0 else [0]
    return pdeg(ptrim(b))<0

LamD=[1]
for x in D: LamD=polymul(LamD,[(-x)%p,1])

def min_vectors(U, count=2):
    """find shifted-degree-minimal independent elements of M_U by increasing wdeg"""
    found=[]
    for d in range(0, n+2):
        # solve W(x)U(x)=N(x), deg W<=d, deg N<=d+K-1
        rows=[]
        for i,x in enumerate(D):
            row=[pow(x,j,p)*U[i]%p for j in range(d+1)]+[(-pow(x,j,p))%p for j in range(d+K)]
            rows.append(row)
        M=np.array(rows,dtype=np.int64)%p
        # kernel basis by elimination
        Mm=M.copy(); piv=[]; r=0
        for c in range(Mm.shape[1]):
            pr=None
            for rr in range(r,Mm.shape[0]):
                if Mm[rr,c]%p: pr=rr; break
            if pr is None: continue
            Mm[[r,pr]]=Mm[[pr,r]]
            Mm[r]=Mm[r]*pow(int(Mm[r,c]),p-2,p)%p
            for rr in range(Mm.shape[0]):
                if rr!=r and Mm[rr,c]%p: Mm[rr]=(Mm[rr]-Mm[rr,c]*Mm[r])%p
            piv.append(c); r+=1
        free=[c for c in range(Mm.shape[1]) if c not in piv]
        for fc in free:
            v=np.zeros(Mm.shape[1],dtype=np.int64); v[fc]=1
            for ri,c in enumerate(piv): v[c]=(-Mm[ri,fc])%p
            W=[int(t) for t in v[:d+1]]; N=[int(t) for t in v[d+1:]]
            if pdeg(W)<0 and pdeg(N)<0: continue
            # check independence from found (as F[X]-module elements): crude, use later
            found.append((d,ptrim(W),ptrim(N)))
        if len(found)>=count and len({f[0] for f in found})>=1:
            # take two with W-parts not proportional-by-polynomial: just return first two distinct wdeg reps
            uniq=[]
            for f in found:
                ok=True
                for g in uniq:
                    # skip if f = poly*g (check divisibility of both coords)
                    if pdeg(g[1])>=0 and pdeg(f[1])>=0 and pdivides(g[1],f[1]) and (pdeg(g[2])<0 or pdivides(g[2],f[2]) or pdeg(f[2])<0):
                        ok=False; break
                if ok: uniq.append(f)
                if len(uniq)==2: return uniq
    return found[:2]

random.seed(9)
ok_div=ok_gcd=ok_det=ok_ray=0; trials=120
for t in range(trials):
    m=random.choice([4,5]); w=m-K; om=n-m
    U=[random.randrange(p) for _ in D]
    g=min_vectors(U)
    if len(g)<2: continue
    (d1,W1,N1),(d2,W2,N2)=g
    # (ii) gcd(W1,W2)=1
    if pdeg(pgcd(W1,W2))==0: ok_gcd+=1
    # (iii) determinant = gamma * LamD (mod checking proportionality)
    det=[(a-b)%p for a,b in zip(polymul(W1,N2)+[0]*40,polymul(W2,N1)+[0]*40)]
    det=ptrim(det)
    if pdeg(det)<0 or (pdeg(det)==n and pdivides(LamD,det)): ok_det+=1
    # (i)+(iv): brute-force census and ray identity
    cen=0
    for T in itertools.combinations(range(n), m):
        # valid iff interpolant deg < K -- reuse: exists c matching; check via all codewords (K small)
        pass
    # ray identity: census = sum_c C(agr_c, m); auto-divisibility: check on random split W
    tot=0
    for cw in itertools.product(range(p),repeat=K):
        agr=sum(1 for i,x in enumerate(D) if ev(list(cw),x)==U[i])
        if agr>=m: tot+=comb(agr,m)
    # brute census
    cen=0
    for T in itertools.combinations(range(n), m):
        pts=[(D[i],U[i]) for i in T]
        # interpolate and check degree < K via checking existence of codeword: small K, reuse tot? do direct:
        # Lagrange degree check
        xs=[a for a,_ in pts]; coef=[0]*m
        for i,(xi,yi) in enumerate(pts):
            num=[1]; den=1
            for j,(xj,_) in enumerate(pts):
                if i==j: continue
                num=polymul(num,[(-xj)%p,1]); den=den*(xi-xj)%p
            inv=pow(den,p-2,p)
            for r_ in range(len(num)): coef[r_]=(coef[r_]+yi*num[r_]*inv)%p
        if pdeg(coef)<K: cen+=1
    if cen==tot: ok_ray+=1
    # (i) auto-divisibility on actual valid supports
    good=True
    for T in itertools.combinations(range(n), m):
        W=[1]
        for i in range(n):
            if i not in T: W=polymul(W,[(-D[i])%p,1])
        # N := W*U interpolated on D, reduced mod LamD to degree <= n-1
        # construct N by interpolation of values W(x)U(x)
        vals=[ev(W,D[i])*U[i]%p for i in range(n)]
        Ncoef=[0]*n
        for i,x in enumerate(D):
            num=[1]; den=1
            for j,y in enumerate(D):
                if i==j: continue
                num=polymul(num,[(-y)%p,1]); den=den*(x-y)%p
            inv=pow(den,p-2,p)
            for r_ in range(len(num)): Ncoef[r_]=(Ncoef[r_]+vals[i]*num[r_]*inv)%p
        if not pdivides(W,Ncoef): good=False; break
    if good: ok_div+=1
print(f"gcd(W1,W2)=1: {ok_gcd}/{trials};  det = gamma*Lambda_D: {ok_det}/{trials};")
print(f"auto-divisibility W|Lambda_D => W|N: {ok_div}/{trials};  ray identity census=sum C(agr,m): {ok_ray}/{trials}")
