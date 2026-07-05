# EXPERIMENTAL -- calibration/cross-check only; the in-paper proof is the entropy sandwich.

from math import lgamma, log, log2, isqrt

p = 2**31 - 2**24 + 1
lp = log2(p); B = isqrt(p) + 1      # 46160 >= sqrt(p)
n = 2**21; k = 2**20
def l2c(N, m): return (lgamma(N+1)-lgamma(m+1)-lgamma(N-m+1))/log(2)

def margins(N, m, label, wmax=26):
    print(f"\n{label}: N={N}, m={m}, log2 C(N,m)={l2c(N,m):.1f}")
    w0 = 0
    for w in range(1, wmax+1):
        main = l2c(N,m) - w*lp
        err = (0 if w==1 else w/2*lp) + l2c(w*B + m - 1 + 0, m)  # C(wB+m-1, m)
        # entropy-sandwich certified versions (proof-grade):
        lam = m/N
        H = lambda x: -x*log2(x)-(1-x)*log2(1-x)
        main_cert = N*H(lam) - log2(N+1) - w*lp
        M2 = w*B + m
        err_cert = (0 if w==1 else w/2*lp) + M2*H(m/M2)
        if main - err > 0: w0 = w
        print(f"  w={w:>2}: margin(exact)={main-err:>+12.0f}   margin(sandwich-certified)={main_cert-err_cert:>+12.0f}")
    print(f"  ==> w0 = {w0}")
    return w0

# KoalaBear MCA row (K=k+1): frontier m and head m at each w (head m = K+w)
margins(n, 1116043, "KB MCA, frontier m (=1116043)")
margins(n, 1116046, "KB list, frontier m (=1116046)")
# head rungs: m depends on w; do a joint scan
print("\nhead rungs (m = K + w):")
for (K, label) in [(k+1, "KB MCA head"), (k, "KB list head")]:
    w0 = 0
    for w in range(1, 27):
        m = K + w
        main = l2c(n, m) - w*lp
        err = (0 if w==1 else w/2*lp) + l2c(w*B + m - 1, m)
        if main - err > 0: w0 = w
        if w in (1, 21, 22, 23, 24):
            print(f"  {label} w={w:>2} (m={m}): margin={main-err:>+12.0f}")
    print(f"  ==> {label}: w0 = {w0}")

# --- circle rows (Mersenne-31 line round): doubled Weil constant 2*w*B ---
pc = 2**31 - 1
lpc = log2(pc); Bc = isqrt(pc) + 1     # 46341
print(f"\n\ncircle p'={pc}, B'={Bc}, domain M=2^21 (chi of a twin coset), per-slot cost 2wB'")
def margins_circle(m, label, wmax=14):
    w0 = 0
    for w in range(1, wmax+1):
        main = l2c(n, m) - w*lpc
        err = (0 if w==1 else w/2*lpc) + l2c(2*w*Bc + m - 1, m)
        if main - err > 0: w0 = w
        print(f"  {label} w={w:>2}: margin={main-err:>+12.0f}")
    print(f"  ==> {label}: w0 = {w0}")
margins_circle(1116021, "M31 MCA frontier", 12)
margins_circle(1116022, "M31 list frontier", 12)
print("\ncircle head rungs (m = K + w):")
for (K, label) in [(k+1, "M31 MCA head"), (k, "M31 list head")]:
    w0 = 0
    for w in range(1, 15):
        m = K + w
        main = l2c(n, m) - w*lpc
        err = (0 if w==1 else w/2*lpc) + l2c(2*w*Bc + m - 1, m)
        if main - err > 0: w0 = w
    print(f"  ==> {label}: w0 = {w0} (margin at w0: {l2c(n,K+w0)-w0*lpc-((0 if w0==1 else w0/2*lpc)+l2c(2*w0*Bc+K+w0-1,K+w0)):+.0f})")

# --- KoalaBear quotient scales for the bounded quotient census ---
print("\nKoalaBear quotient scales (N_c = 2^21/c, certificate m_c):")
for c, m in [(2,558019),(4,279007),(8,139501),(16,69748),(32,34871)]:
    N = 2**21//c
    w0 = 0; mg1 = None
    for w in range(1, 14):
        main = l2c(N, m) - w*lp
        err = (0 if w==1 else w/2*lp) + l2c(w*B + m - 1, m)
        if w == 1: mg1 = main - err
        if main - err > 0: w0 = w
    print(f"  c={c:>3} (N=2^{N.bit_length()-1}): w0={w0}, w=1 margin {mg1:+.0f}")
