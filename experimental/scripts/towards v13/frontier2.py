from math import comb, lgamma, log2, log
from fractions import Fraction

p_kb = 2**31 - 2**24 + 1
p_m  = 2**31 - 1
n = 2**21; k = 2**20

def log2comb(N, m):
    return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)

def exact_opt(pbase, Kc_num, thr_num, thr_den, scales, label):
    """largest m per scale with comb(N,m)*thr_den > pbase^(m-ceil(Kc/c))*thr_num; maximize mc"""
    logp = log2(pbase); best = (0, None); rows = []
    for c in scales:
        if n % c: continue
        N = n//c; ceilKc = -(-Kc_num//c)
        if ceilKc > N: continue
        thr_bits = log2(thr_num) - log2(thr_den)
        def f(m): return log2comb(N,m) - (m-ceilKc)*logp - thr_bits
        if f(ceilKc) <= 0 and f(min(N, ceilKc+1)) <= 0 and f((ceilKc+N)//2) <= 0:
            # maybe still passes somewhere? entropy is unimodal; check peak
            if f(min(N, N//2 if N//2>=ceilKc else ceilKc)) <= 0: continue
        lo, hi = ceilKc, N
        while hi - lo > 1:
            mid = (lo+hi)//2
            if f(mid) > 0: lo = mid
            else: hi = mid
        # exact walk from m0 = lo (float boundary), using ratio updates
        m0 = lo
        L = comb(N, m0)
        R = pbase**(m0-ceilKc) * thr_num
        passes = lambda L, R: L*thr_den > R
        m = m0
        if passes(L, R):
            while m+1 <= N:
                L2 = L*(N-m)//(m+1); R2 = R*pbase
                if passes(L2, R2): m += 1; L, R = L2, R2
                else: break
            mstar = m
        else:
            while m-1 >= ceilKc:
                L = L*m//(N-m+1); R = R//pbase if R%pbase==0 else None
                if R is None:
                    R = pbase**(m-1-ceilKc)*thr_num
                m -= 1
                if passes(L, R): break
            mstar = m if passes(L, R) else None
        if mstar is None: continue
        w = mstar - ceilKc
        rows.append((c, mstar, w, mstar*c))
        if mstar*c > best[0]: best = (mstar*c, (c, mstar, w))
    print(f"--- {label} ---")
    for c, m, w, mc in sorted(rows):
        d = Fraction(n-mc, n)
        print(f"  c={c:>5}  m={m:>7}  w={w:>6}  Delta={mc-k:>6}  delta = {d} = {float(d):.8f}")
    mc,(c,m,w) = best
    print(f"  BEST edge: c={c}, m={m}, w={w}, delta = {Fraction(n-mc,n)} = {float(Fraction(n-mc,n)):.8f}\n")
    return best

sc = [2**i for i in range(1,14)]
q_kb = p_kb**6; q_c = p_m**4
b1=exact_opt(p_kb, k+1, q_kb+k, k,     sc, "KoalaBear MCA  (thresh q/k+1)")
b2=exact_opt(p_kb, k,   q_kb,   2**128,sc, "KoalaBear list (thresh 2^-128 q)")
b3=exact_opt(p_m,  k+1, q_c+k,  k,     sc, "circle MCA     (thresh q/k+1)")
b4=exact_opt(p_m,  k,   q_c,    2**100,sc, "circle list    (thresh 2^-100 q)")
