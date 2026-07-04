from math import log2, comb, sqrt
from fractions import Fraction

def Hb(x): return -x*log2(x) - (1-x)*log2(1-x)
p_kb = 2**31-2**24+1; p_m = 2**31-1
b_kb = log2(p_kb); b_m = log2(p_m)
print(f"beta_KB = {b_kb:.6f}, beta_M31 = {b_m:.6f}")

def gstar(rho, beta):
    lo, hi = 1e-9, 1-rho-1e-12
    for _ in range(200):
        mid = (lo+hi)/2
        if Hb(rho+mid) >= beta*mid: lo = mid
        else: hi = mid
    return lo

print("\nAsymptotic frontier g*(rho,beta) and conjectured threshold delta = 1-rho-g*:")
for rho in [1/2,1/4,1/8,1/16]:
    gk = gstar(rho,b_kb); gm = gstar(rho,b_m)
    print(f"  rho=1/{int(1/rho):<2}  KB: g*={gk:.7f} delta*={1-rho-gk:.7f}   M31: g*={gm:.7f} delta*={1-rho-gm:.7f}")

n=2**21; k=2**20
print("\nDeployed (n=2^21) route optima vs frontier:")
for name, D in [("KB MCA",67462),("KB list",67468),("circle MCA",67442),("circle list (2^-100)",67444)]:
    g = D/n
    print(f"  {name:22s} g={g:.7f}  edge={1/2-g:.8f}  frontier deficit ~ {gstar(0.5,b_kb)-g:+.2e}")

# exact certificate margins at c=2 optima (bits)
from math import lgamma, log
def l2c(N,m): return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)
q_kb = p_kb**6; q_c = p_m**4
rows = [
 ("KB MCA",  p_kb, 2**20, 558019, -(-(k+1)//2), log2(q_kb/k+1)),
 ("KB list", p_kb, 2**20, 558022, k//2,          log2(q_kb)-128),
 ("cir MCA", p_m,  2**20, 558009, -(-(k+1)//2), log2(q_c/k+1)),
 ("cir list",p_m,  2**20, 558010, k//2,          log2(q_c)-100),
]
print("\nMargins (bits) at c=2 optima: LHS=log2 C(N,m), RHS=w*log2 p + thresh")
for nm,p,N,m,ck,th in rows:
    w = m-ck
    print(f"  {nm}: m={m} w={w}  LHS-RHS = {l2c(N,m) - w*log2(p) - th:8.1f} bits;  next m fails by {-(l2c(N,m+1)-(w+1)*log2(p)-th):.1f} bits")

print("\nJohnson floors 1-sqrt(rho) (absolute list-witness barrier) per rate:")
for rho in [1/2,1/4,1/8,1/16]:
    print(f"  rho=1/{int(1/rho):<2}: 1-sqrt(rho) = {1-sqrt(rho):.6f}")

print("\nNew open bands (deployed rows, with BCIKS import safe edge 1/4):")
print(f"  KB MCA:  (0.25, {Fraction(n-2*558019,n)}) width {float(Fraction(n-2*558019,n))-0.25:.6f}  (was {15331/32768-0.25:.6f})")
print(f"  KB list: (Johnson {1-sqrt(0.5):.6f}, {Fraction(n-2*558022,n)}) width {float(Fraction(n-2*558022,n))-(1-sqrt(0.5)):.6f}")

# headroom at larger blocklengths: route optimum at n=2^24, c=2 (KB MCA test), envelope q<=2^256 worst case?
# quick: same threshold, N=2^23
for np_ in [2**22, 2**24]:
    N = np_//2; kk = np_//2  # rate 1/2: k=np_/2, ceil((k+1)/2)
    ck = -(-(kk+1)//2)
    lo, hi = ck, N
    th = log2(q_kb/kk+1)
    f = lambda m: l2c(N,m)-(m-ck)*log2(p_kb)-th
    while hi-lo>1:
        mid=(lo+hi)//2
        if f(mid)>0: lo=mid
        else: hi=mid
    g = (2*lo-kk)/np_
    print(f"  route at n=2^{int(log2(np_))}: g ~ {g:.7f} (float-located; deficit to g* {gstar(0.5,b_kb)-g:+.2e})")
