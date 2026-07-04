import itertools, cmath, math
from math import comb, sqrt, lgamma, pi
from collections import Counter

p = 257
g = 3
d = (p-1)//16
H = sorted({pow(g, d*i, p) for i in range(16)})
N = 16

def ep(x): return cmath.exp(2j*pi*(x%p)/p)
def em_of(eps, m):
    e = [1+0j]+[0j]*m
    for x in eps:
        for j in range(m,0,-1): e[j] = e[j] + x*e[j-1]
    return e[m]

# w=1 exhaustive
m = 8
fib = Counter()
for A in itertools.combinations(H, m): fib[sum(A)%p] += 1
main = comb(N,m)/p
maxdev = max(abs(fib.get(z,0)-main) for z in range(p))
B = sqrt(p)
bound = math.exp(sum(math.log(B+i) for i in range(m)) - lgamma(m+1))
print(f"[w=1] max fiber dev={maxdev:.2f} vs bound C(sqrt p+m-1,m)={bound:.1f}: ok={maxdev<=bound}")
# also direct: max_t |e_m(eps(t))| <= bound
mx = max(abs(em_of([ep(t*a) for a in H], m)) for t in range(1,p))
print(f"[w=1] max_t|E_m(t)|={mx:.2f} <= {bound:.1f}: {mx<=bound}")

# Gauss bound
w1max = max(abs(sum(ep(u*a) for a in H)) for u in range(1,p))
print(f"[Gauss] max={w1max:.4f} <= sqrt p={sqrt(p):.4f}: {w1max<=sqrt(p)+1e-9}")

# Weil deg-2 over subgroup, exhaustive
worst = max(abs(sum(ep(s1*a+s2*a*a) for a in H)) for s1 in range(p) for s2 in range(p) if (s1,s2)!=(0,0))
print(f"[Weil deg<=2] max over ALL s!=0: {worst:.4f} <= 2 sqrt p={2*sqrt(p):.4f}: {worst<=2*sqrt(p)}")

# w=2 identity with Qhat support on the line s2 = -t2/2
m2 = 6
inv2 = pow(2,p-2,p)
for (t1,t2) in [(5,9),(0,3),(11,250)]:
    E = sum(ep(t1*(sum(A)%p) + t2*(sum(a*b for a,b in itertools.combinations(A,2))%p))
            for A in itertools.combinations(H,m2))
    s2star = (-t2*inv2) % p
    tot = 0
    for s1 in range(p):
        if s1==0 and s2star==0: continue
        Qhat = p*sum(ep(t1*v1 + t2*inv2*v1*v1 - s1*v1) for v1 in range(p))
        if abs(Qhat) < 1e-9: continue
        G = em_of([ep(s1*a + s2star*a*a) for a in H], m2)
        tot += Qhat*G
    tot /= p*p
    Q0 = p*sum(ep(t1*v1 + t2*inv2*v1*v1) for v1 in range(p)) if s2star==0 else 0.0
    print(f"[w=2 identity] t=({t1},{t2}): |E-decomp|={abs(E-tot):.2e}  (E={E:.4f}); Qhat(0)={abs(Q0) if t2 else 'n/a'}")
# joint (e1,e2) fibers exhaustively, compare to C(N,m)/p^2 + p*C(2sqrt p+m-1,m) (weak here, but verify)
fib2 = Counter()
for A in itertools.combinations(H,m2):
    e1 = sum(A)%p; e2 = sum(a*b for a,b in itertools.combinations(A,2))%p
    fib2[(e1,e2)] += 1
main2 = comb(N,m2)/p**2
maxdev2 = max(abs(fib2.get((z1,z2),0)-main2) for z1 in range(p) for z2 in range(p))
B2 = 2*sqrt(p)
bound2 = p * math.exp(sum(math.log(B2+i) for i in range(m2)) - lgamma(m2+1))
print(f"[w=2 fibers] max dev={maxdev2:.3f} vs p^(w/2)*C(2 sqrt p+m-1,m)={bound2:.1f}: ok={maxdev2<=bound2}")
