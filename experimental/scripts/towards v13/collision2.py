from math import lgamma, log, log2, comb, isqrt

p = 2**31 - 2**24 + 1
lp = log2(p)
B1 = isqrt(p) + 1          # 46341 >= sqrt(p)
def l2c(N,m): return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)
def l2c_rf(B,m):           # log2 C(B+m-1, m) with integer B via lgamma
    return (lgamma(B+m)-lgamma(B)-lgamma(m+1))/log(2)

print(f"sqrt(p)={p**0.5:.3f}, B1={B1}, d=(p-1)/2^20={(p-1)//2**20}")
rows = [("KB MCA c=2", 2**20, 558019), ("KB list c=2", 2**20, 558022)]
for name,N,m in rows:
    main0 = l2c(N,m)
    print(f"\n{name}: N={N}, m={m}, log2 C(N,m) = {main0:.1f}")
    print("  w   main=log2[C/p^w]   err=log2[p^(w/2) C(wB1+m-1,m)]   margin(bits)")
    for w in range(1,14):
        main = main0 - w*lp
        err = (0 if w==1 else w/2*lp) + l2c_rf(w*B1, m)
        print(f"  {w:>2}  {main:>12.0f}        {err:>12.0f}                {main-err:>+12.0f}")

# per-scale w=1 nonvacuity across scales c=2..64 at the per-scale optimal m
print("\nw=1 margin per scale (at per-scale certificate m from prop:v13f-terminal, KB MCA):")
for c,m in [(2,558019),(4,279007),(8,139501),(16,69748),(32,34871),(64,17433)]:
    N = 2**21//c
    print(f"  c={c:>3} N=2^{N.bit_length()-1}: margin = {l2c(N,m)-lp - l2c_rf(B1,m):+.0f} bits")

# exact relative error at w=1, c=2 (the two-sided stratum statement)
m=558019; N=2**20
rel = l2c_rf(B1,m) - (l2c(N,m)-lp)
print(f"\nw=1, c=2: fiber = C(N,m)/p * (1 + eps), |eps| <= 2^{rel:.0f}")
