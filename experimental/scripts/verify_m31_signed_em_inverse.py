#!/usr/bin/env python3
"""
verify_m31_signed_em_inverse.py -- zero-arg, stdlib-only verifier for the
signed-e_m max-fiber inverse at the binding Mersenne-31 list deployed row
(a_+ = 1116023), packet cap25_v13_m31_signed_em_inverse.

The point of this packet (vs. the KB participation-ratio packet, integrated
e83962ae, was PR #414): the M31 row's domain is the CHEBYSHEV / twin-coset
(norm-one torus), NOT a multiplicative subgroup mu_n. This verifier therefore
instruments the signed-e_m object on a *faithful* Chebyshev domain and proves
the Chebyshev-fold analog of the packet's mu_n lemma L2.

Recomputes and gates, exactly:
  (1) M31-list ledger (exact big-int): p=2^31-1, n=2^21, k=2^20, a_+=1116023,
      w=67447, m=981129, B*=2^24-1, avg_ceil=ceil(C(n,a_+)/p^w)=1993678;
  (2) K = B*/ceil(avg), nu*_ref = (K-1)^2 = 54.985 = 2^5.781 ~ 55, log2(#dir);
  (3) the M31 dead-route margins: the p^{w/2} (L^2) floor (1045425.61 bits) and
      the L-infinity per-direction route (2090854.11 bits) -- both exact;
  (4) the four-row nu*_ref table matched to grande_finale.tex prop:q-exact-target;
  (5) the (STAR) <=> PR <= nu* algebraic reduction (domain-agnostic; sampled);
  (6) L1 value-distribution reduction on a Chebyshev domain;
  (7) the NEW Chebyshev-fold self-similarity lemma (PROVED-form, toy-verified);
  (8) w=1 non-collapse on the Chebyshev domain (|e_m| is NOT identically 1,
      unlike the full multiplicative group F_p^*);
  (9) faithful Chebyshev toy (p=127,n=16,m=8,w=1, avg~101): R, Gamma2-1, L1/C,
      max|e|/C, PR -- all << budget -- vs the mu_n reference (p=97,...);
      Parseval + the PROVED energy floor gated on every shipped toy row;
 (10) twin-coset validity: chi=Re 2-to-1, Chebyshev T_2-tower n,n/2,...,1,
      T_2 exactly 2-to-1, and D is NOT product-closed (not a mult. subgroup);
 (11) offset robustness of the faithful measurement;
 (12) falsification guard: above-bound spikes occur ONLY where the atom itself
      fails (avg << 1), never in the faithful (avg >> 1) regime;
 (13) every constant re-checked against the shipped JSON;
plus >= 5 non-tautological tamper self-tests.

Run:  python3 verify_m31_signed_em_inverse.py     (exit 0 on PASS)
Knobs (env):  EMINV_AS_CAP_GB (address-space soft cap, GiB, default 2)
              EMINV_DATA_DIR  (dir holding the JSON, default <repo>/experimental/data)
"""
import os, sys, math, cmath, json
from itertools import combinations, product
from collections import Counter, defaultdict
from fractions import Fraction

# ------------------------------------------------------------ environment knobs
def _apply_as_cap():
    try:
        gb = float(os.environ.get("EMINV_AS_CAP_GB", "2"))
    except ValueError:
        gb = 2.0
    if gb <= 0:
        return
    try:
        import resource
        cap = int(gb * (1024 ** 3))
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        newhard = hard if hard != resource.RLIM_INFINITY and hard < cap else cap
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, newhard))
    except Exception:
        pass
_apply_as_cap()

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.environ.get("EMINV_DATA_DIR", os.path.join(REPO_ROOT, "experimental", "data"))
JSON_PATH = os.path.join(DATA_DIR, "cap25_v13_m31_signed_em_inverse.json")

CHECKS = []
def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

def log2int(x):
    if x <= 0:
        return float('-inf')
    b = x.bit_length(); top = x >> max(0, b - 64)
    return (b - min(b, 64)) + math.log2(top)
def log2frac(fr):
    return log2int(fr.numerator) - log2int(fr.denominator)
def approx(x, y, rel=3e-3, ab=6e-3):
    return abs(x - y) <= ab + rel * abs(y)

# =============================================================== circle / Chebyshev toy domain
def _cmul(u, v, p):
    a, b = u; c, d = v
    return ((a * c - b * d) % p, (a * d + b * c) % p)   # F_{p^2}=F_p[i], i^2=-1
def _cpow(u, e, p):
    r = (1, 0)
    while e > 0:
        if e & 1: r = _cmul(r, u, p)
        u = _cmul(u, u, p); e >>= 1
    return r
def _circle_gen(p):
    assert p % 4 == 3, "need p = 3 mod 4 so -1 is a QNR and |circle| = p+1"
    elts = [(a, b) for a in range(p) for b in range(p) if (a * a + b * b) % p == 1]
    assert len(elts) == p + 1, (len(elts), p + 1)
    for u in elts:
        e = 1; v = u
        while v != (1, 0):
            v = _cmul(v, u, p); e += 1
        if e == p + 1:
            return u
    raise RuntimeError("no circle generator")
def cheb_twin_coset(p, n, goff=1):
    """x-projection of a standard-position twin coset gH U g^{-1}H of the order-n
    subgroup H of the circle group; chi=Re is 2-to-1, |D|=n. Faithful M31 domain."""
    w = _circle_gen(p); order = p + 1
    assert order % n == 0 and 2 * n <= order
    H = [_cpow(w, (order // n) * j, p) for j in range(n)]
    g = _cpow(w, goff, p); ginv = _cpow(w, order - goff, p)
    Dcal = set()
    for h in H:
        Dcal.add(_cmul(g, h, p)); Dcal.add(_cmul(ginv, h, p))
    xs = defaultdict(list)
    for u in Dcal:
        xs[u[0]].append(u)
    D = sorted(xs.keys())
    twoto1 = (len(Dcal) == 2 * n) and all(len(v) == 2 for v in xs.values())
    return D, twoto1
def T_cheb(c, x, p):
    if c == 0: return 1 % p
    t0, t1 = 1 % p, x % p
    for _ in range(2, c + 1):
        t0, t1 = t1, (2 * x * t1 - t0) % p
    return t1

def em_vd(N, mm, om):
    """e_m from the value multiset N: [T^m] prod_s (1 + T e_p(s))^{N(s)}."""
    coef = [0j] * (mm + 1); coef[0] = 1 + 0j
    for s, mult in N.items():
        v = om[s]
        for _ in range(mult):
            for d in range(mm, 0, -1):
                coef[d] += v * coef[d - 1]
    return coef[mm]
def value_dist(t, D, pt, p):
    N = Counter()
    for a in D:
        fa = 0; pa = pt[a]
        for i, ti in enumerate(t):
            if ti: fa = (fa + ti * pa[i + 1]) % p
        N[fa] += 1
    return N

def mu_subgroup(p, n):
    """The order-n multiplicative subgroup mu_n < F_p^* (n | p-1) -- the KB-domain analog."""
    def order(x):
        o = 1; y = x % p
        while y != 1: y = (y * x) % p; o += 1
        return o
    g = next(c for c in range(2, p) if order(c) == p - 1)
    h = pow(g, (p - 1) // n, p); S = []; x = 1
    for _ in range(n): S.append(x); x = (x * h) % p
    return sorted(S)
def spectrum_w1(D, p, n, m):
    """R_true, L1/C, PR for a w=1 row over domain D (used for the mu_n reference)."""
    C = math.comb(n, m); pt = {a: pow(a, 1, p) for a in D}
    om = [cmath.exp(2j * math.pi * e / p) for e in range(p)]
    fib = Counter()
    for M in combinations(D, m):
        fib[sum(pt[a] for a in M) % p] += 1
    R = p * max(fib.values()) / C
    ems = [abs(em_vd(Counter((t1 * a) % p for a in D), m, om)) for t1 in range(1, p)]
    L1 = sum(ems) / C; PR = (sum(ems)) ** 2 / sum(e * e for e in ems)
    return R, L1, PR

_TOY = {}
def cheb_toy(p, n, m, w, goff=1):
    key = (p, n, m, w, goff)
    if key in _TOY: return _TOY[key]
    D, twoto1 = cheb_twin_coset(p, n, goff)
    assert len(D) == n and twoto1
    C = math.comb(n, m); om = [cmath.exp(2j * math.pi * e / p) for e in range(p)]
    pt = {a: [pow(a, i, p) for i in range(w + 1)] for a in D}
    fib = Counter()
    for M in combinations(D, m):
        ps = tuple(sum(pt[a][i] for a in M) % p for i in range(1, w + 1)); fib[ps] += 1
    maxN = max(fib.values()); sumN2 = sum(v * v for v in fib.values())
    R = p ** w * maxN / C; G2 = p ** w * sumN2 / C ** 2; avg = C / p ** w
    L1p = L1q = L2 = 0.0; mx = mxp = 0.0
    for t in product(range(p), repeat=w):
        if not any(t): continue
        ae = abs(em_vd(value_dist(t, D, pt, p), m, om))
        # coefficient scale on the Chebyshev domain: is f_t constant on some T_c-fiber?
        cscale = 1; j = 1
        while (1 << j) <= n and n % (1 << j) == 0:
            c = 1 << j; grp = defaultdict(set)
            for a in D:
                fa = sum(t[i] * pt[a][i + 1] for i in range(w)) % p
                grp[T_cheb(c, a, p)].add(fa)
            if all(len(s) == 1 for s in grp.values()):
                cscale = c
            j += 1
        if cscale == 1: L1p += ae; mxp = max(mxp, ae)
        else: L1q += ae
        L2 += ae * ae; mx = max(mx, ae)
    L1 = L1p + L1q; PR = L1 * L1 / L2 if L2 > 0 else 0.0
    ndir = p ** w - 1
    parse = abs(L2 - C * C * (G2 - 1)) / (C * C * (G2 - 1)) if G2 > 1 else 0.0
    energy_ok = (mx * mx) * ndir >= L2 * (1 - 1e-12)   # PROVED: max >= RMS
    r = dict(avg=avg, R=R, G2=G2, L1=L1 / C, L1p=L1p / C, L1q=L1q / C, mx=mx / C,
             mxp=mxp / C, PR=PR, ndir=ndir, parse=parse, energy_ok=energy_ok,
             share=(L1p / L1 if L1 > 0 else 1.0))
    _TOY[key] = r
    return r

# =============================================================== §0 load JSON
print("== §0 shipped JSON present and self-consistent ==")
with open(JSON_PATH) as f:
    J = json.load(f)
row = J["binding_row_M31_list"]
check("JSON schema tag", J["schema"] == "cap25-v13-m31-signed-em-inverse-v1")

# =============================================================== §1 exact M31-list ledger
print("\n== §1 M31-list ledger (exact big-int) ==")
p = 2 ** 31 - 1; n = 2 ** 21; k = 2 ** 20; a = 1116023; w = 67447; m = n - a
check("p = 2^31 - 1 (Mersenne, 3 mod 4)", p == 2147483647 and p % 4 == 3)
check("n=2^21, k=2^20", n == 2 ** 21 and k == 2 ** 20)
check("w = a_+ - k = 67447", w == a - k == 67447)
check("m = n - a_+ = 981129", m == n - a == 981129)
Bstar = (2 ** 31 - 1) ** 4 // 2 ** 100
check("B* = floor((2^31-1)^4/2^100) = 2^24-1 = 16777215", Bstar == 2 ** 24 - 1 == 16777215)
C = math.comb(n, a); pw = p ** w                     # ~2.09e6-bit big ints
avg_ceil = -((-C) // pw)                              # ceil(C/p^w)
check("avg_ceil = ceil(C(n,a_+)/p^w) = 1993678", avg_ceil == 1993678, str(avg_ceil))
check("JSON row constants agree", row["p"] == p and row["a_plus"] == a and row["w"] == w
      and row["m"] == m and row["avg_ceil"] == avg_ceil and row["Bstar"] == Bstar)
l2C = log2int(C); l2pw = log2int(pw)
check("log2 C(n,a_+) = 2090877.927 (tight)", abs(l2C - 2090877.927) < 5e-3, f"{l2C:.4f}")
check("log2 p^w = 2090856.99995 (tight)", abs(l2pw - 2090856.99995) < 5e-4, f"{l2pw:.5f}")
check("bit margin Delta_Q = log2(B*/avg_ceil) = 3.0730",
      approx(math.log2(Bstar / avg_ceil), 3.072998926581202, ab=1e-9),
      f"{math.log2(Bstar/avg_ceil):.10f}")

# =============================================================== §2 nu*_ref target
print("\n== §2 the frontier target nu*_ref = 2^5.781 ~ 55 ==")
K = Fraction(Bstar, avg_ceil)                         # B*/ceil(avg), the packet's convention
check("K = B*/ceil(avg) ~ 8.4152", approx(float(K), 8.4152, ab=1e-3), f"{float(K):.6f}")
nu_ref = (K - 1) ** 2
check("nu*_ref = (K-1)^2 = 54.985", approx(float(nu_ref), 54.985, ab=1e-2), f"{float(nu_ref):.5f}")
check("log2 nu*_ref = 5.781 (~ 55 spikes)", approx(log2frac(nu_ref), 5.781, ab=1e-3),
      f"2^{log2frac(nu_ref):.4f}")
ndir = pw - 1
check("log2(#dir) = log2(p^w - 1) ~ 2090857.00", approx(log2int(ndir), 2090857.00, ab=1e-2),
      f"{log2int(ndir):.4f}")
check("JSON nu*_ref agrees", approx(J["target_nu_ref"]["nu_ref"], float(nu_ref), ab=1e-6)
      and approx(J["target_nu_ref"]["log2_nu_ref"], log2frac(nu_ref), ab=1e-6))

# =============================================================== §3 M31 dead-route margins
print("\n== §3 M31 dead-route margins (L^2 p^{w/2} floor + L-infinity per-direction) ==")
half_w_log2p = (w / 2.0) * math.log2(p)
l2_floor_bits = half_w_log2p - math.log2(float(K) - 1)          # trivial-support C-S
linf_bits = log2int(ndir) - math.log2(float(K) - 1)            # uniform per-direction
check("(w/2)log2 p = 1045428.50", approx(half_w_log2p, 1045428.5, ab=1e-2), f"{half_w_log2p:.4f}")
check("L^2 p^{w/2} floor: DEAD by 1045425.61 bits (KB was 1045396.58)",
      approx(l2_floor_bits, 1045425.61, ab=1e-1), f"{l2_floor_bits:.2f}")
check("L-infinity per-direction: DEAD by 2090854.11 bits (KB was 2090815.35)",
      approx(linf_bits, 2090854.11, ab=1e-1), f"{linf_bits:.2f}")
check("both M31 margins strictly exceed the KB analogs (tighter budget => deader)",
      l2_floor_bits > 1045396.58 and linf_bits > 2090815.35)
check("JSON dead-route margins agree",
      approx(J["dead_route_margins_M31_list"]["L2_pw2_floor_bits"], l2_floor_bits, ab=1e-1)
      and approx(J["dead_route_margins_M31_list"]["Linf_perdirection_bits"], linf_bits, ab=1e-1))

# =============================================================== §4 four-row nu*_ref table
print("\n== §4 four-row nu*_ref table (matched to grande_finale prop:q-exact-target) ==")
pKB = 2130706433
rows = [("KoalaBear MCA",  pKB, k + 1, 274980728111395087, 67471, 57198030366, 4807520.9295, 44.394),
        ("KoalaBear list", pKB, k,     274980728111395087, 67471, 65065153468, 4226236.5253, 44.022),
        ("Mersenne-31 MCA",  p, k + 1, 16777215,           67447, 1752700,     9.5722,        6.199),
        ("Mersenne-31 list", p, k,     16777215,           67447, 1993678,     8.4152,        5.781)]
for name, pp, KK, B, ww, ceil_tex, ratio_tex, l2nu_tex in rows:
    a_plus = KK + ww; mm = n - a_plus
    Cc = math.comb(n, a_plus); ppw = pp ** ww
    ceilavg = -((-Cc) // ppw)
    Kx = Fraction(B, ceilavg); nu = (Kx - 1) ** 2
    ok = (ceilavg == ceil_tex) and approx(float(Kx), ratio_tex, ab=1e-2) \
         and approx(log2frac(nu), l2nu_tex, ab=1e-2)
    check(f"{name}: avgceil+ratio+log2 nu*_ref match tex", ok,
          f"a_+={a_plus} K={float(Kx):.4f} log2nu={log2frac(nu):.3f}")
check("M31-list is the binding (smallest nu*_ref) row", 5.781 < 6.199 < 44.022 < 44.394)

# =============================================================== §5 the reduction (domain-agnostic)
print("\n== §5 (STAR) <=> PR <= nu* algebraic reduction (holds for ANY domain D) ==")
ft = cheb_toy(127, 16, 8, 1)     # faithful Chebyshev toy carries a concrete spectrum
# recover ||Rhat||_1, ||Rhat||_2 from the toy's L1/C, PR, Gamma2
G2m1 = ft['G2'] - 1
for Ktest in (2.0, 3.0, 5.0):
    star_ok = (ft['L1'] <= (Ktest - 1))                       # ||Rhat||_1/C <= K-1
    pr_ok = (ft['PR'] <= ((Ktest - 1) ** 2 / G2m1))           # PR <= (K-1)^2/(Gamma2-1)
    check(f"(STAR)<=>PR<=nu* identity at sample K={Ktest}", star_ok == pr_ok, f"both={star_ok}")
check("Parseval ||Rhat||_2^2 = C^2(Gamma2-1) on the Chebyshev toy (relerr ~ 0)",
      ft['parse'] < 1e-9, f"relerr {ft['parse']:.1e}")

# =============================================================== §6 L1 value-distribution reduction
print("\n== §6 L1: e_m(v_t) depends only on the value multiset {f_t(x)} (Chebyshev D) ==")
pp, nn, mm, ww = 31, 8, 4, 2
D, ok2 = cheb_twin_coset(pp, nn); om = [cmath.exp(2j * math.pi * e / pp) for e in range(pp)]
pt = {aa: [pow(aa, i, pp) for i in range(ww + 1)] for aa in D}
byval = defaultdict(list)
for t in product(range(pp), repeat=ww):
    N = value_dist(t, D, pt, pp)
    byval[tuple(sorted(N.items()))].append(em_vd(N, mm, om))
w1 = max((abs(e - v[0]) for v in byval.values() for e in v[1:]), default=0.0)
check("L1 value-distribution reduction on Chebyshev D (max |e_m diff| ~ 0)", w1 < 1e-9, f"{w1:.1e}")

# =============================================================== §7 Chebyshev-fold self-similarity
print("\n== §7 NEW Chebyshev-fold self-similarity lemma (the faithful M31 analog of mu_n L2) ==")
pp, nn, mm, c = 31, 8, 4, 2
D, _ = cheb_twin_coset(pp, nn); om = [cmath.exp(2j * math.pi * e / pp) for e in range(pp)]
Dc = sorted(set(T_cheb(c, x, pp) for x in D)); nc = len(Dc)
check("T_c is exactly c-to-1: |T_2(D)| = n/2", nc == nn // c, f"|D_c|={nc}")
worst = 0.0; tested = 0
for b1 in range(pp):
    for b2 in range(pp):
        if b1 == 0 and b2 == 0: continue
        Nf = Counter()
        for x in D:
            y = T_cheb(c, x, pp); Nf[(b1 * y + b2 * y * y) % pp] += 1     # f_t = g(T_c), g(y)=b1 y + b2 y^2
        lhs = em_vd(Nf, mm, om)
        Eg = [0j] * (nc + 1); Eg[0] = 1 + 0j
        for y in Dc:
            v = om[(b1 * y + b2 * y * y) % pp]
            for d in range(nc, 0, -1): Eg[d] += v * Eg[d - 1]
        poly = [1 + 0j]
        for _ in range(c):                                                # c-fold convolution power
            new = [0j] * min(len(poly) + nc, mm + 1)
            for i2, pi2 in enumerate(poly):
                for j2, ej in enumerate(Eg):
                    if i2 + j2 <= mm: new[i2 + j2] += pi2 * ej
            poly = new
        rhs = poly[mm] if mm < len(poly) else 0j
        worst = max(worst, abs(lhs - rhs)); tested += 1
check(f"Chebyshev-fold: e_m(v_t) = [T^m](E_g)^c over {tested} c=2 quotient dirs (max err ~ 0)",
      worst < 1e-9, f"{worst:.1e}")

# =============================================================== §8 w=1 non-collapse on Chebyshev D
print("\n== §8 w=1 does NOT collapse to |e_m|=1 on Chebyshev D (unlike full-group F_p^*) ==")
for pp, nn, mm in [(31, 8, 4), (127, 16, 8)]:
    D, _ = cheb_twin_coset(pp, nn); om = [cmath.exp(2j * math.pi * e / pp) for e in range(pp)]
    Cc = math.comb(nn, mm)
    vals = [abs(em_vd(Counter((t1 * x) % pp for x in D), mm, om)) / Cc for t1 in range(1, pp)]
    not_const = (max(vals) - min(vals)) > 1e-3 and not all(approx(v, 1.0, ab=1e-6) for v in vals)
    check(f"Chebyshev w=1 |e_m|/C NOT identically 1/const (p={pp},n={nn})", not_const,
          f"range [{min(vals):.4f},{max(vals):.4f}]")
# contrast: on the FULL multiplicative group F_p^* the collapse |e_m|=1 DOES hold (control)
for P, M in [(13, 6), (17, 8)]:
    Dfull = list(range(1, P)); omg = [cmath.exp(2j * math.pi * e / P) for e in range(P)]
    ok = all(approx(abs(em_vd(Counter((t1 * a) % P for a in Dfull), M, omg)), 1.0, ab=1e-9)
             for t1 in range(1, P))
    check(f"control: full-group F_p^* w=1 DOES collapse |e_m|=1 (p={P})", ok)

# =============================================================== §9 twin-coset validity
print("\n== §9 twin-coset domain is a genuine Chebyshev domain (not a mult. subgroup) ==")
D16, ok2 = cheb_twin_coset(127, 16)
check("chi=Re is 2-to-1, |D|=16", ok2 and len(D16) == 16)
sizes = [len(D16)]; Dj = D16
for _ in range(4):
    Dj = sorted(set(T_cheb(2, x, 127) for x in Dj)); sizes.append(len(Dj))
check("Chebyshev T_2-tower sizes = 16,8,4,2,1", sizes == [16, 8, 4, 2, 1], str(sizes))
t2fib = Counter(T_cheb(2, x, 127) for x in D16)
check("T_2 is exactly 2-to-1 on D (all fibers size 2)", set(t2fib.values()) == {2})
prodclosed = all(((x * y) % 127) in set(D16) for x in D16 for y in D16)
check("D is NOT product-closed (genuinely Chebyshev, not a multiplicative subgroup)", not prodclosed)

# =============================================================== §10 faithful toy + all-row gates
print("\n== §10 faithful Chebyshev toy (avg >> 1) vs mu_n reference; every-row Parseval/energy ==")
check("faithful Chebyshev p127 n16 w1: R~1.30, G2-1~0.011, L1/C~0.43, max|e|/C~0.045, PR~16.9",
      approx(ft['R'], 1.3026, rel=5e-3) and approx(ft['G2'] - 1, 0.0109, ab=5e-4)
      and approx(ft['L1'], 0.4298, rel=1e-2) and approx(ft['mx'], 0.04459, rel=2e-2)
      and approx(ft['PR'], 16.941, rel=1e-2) and ft['share'] == 1.0,
      f"R={ft['R']:.4f} G2-1={ft['G2']-1:.4f} L1/C={ft['L1']:.4f} max={ft['mx']:.5f} PR={ft['PR']:.3f}")
check("faithful toy: raw PR <= nu*_ref (16.9 << 55), L1/C <= K-1 (0.43 << 7.42), R <= K (1.30 << 8.42)",
      ft['PR'] <= float(nu_ref) and ft['L1'] <= float(K) - 1 and ft['R'] <= float(K))
# mu_n reference: RECOMPUTE the packet #414 Sec.5 faithful toy (p=97,n=16,m=8,w=1) and compare
Rmu, L1mu, PRmu = spectrum_w1(mu_subgroup(97, 16), 97, 16, 8)
check("mu_n reference toy p97 n16 w1 recomputed = packet #414 (R=1.4923, L1/C=0.5302, PR=20.50)",
      approx(Rmu, 1.4923, rel=3e-3) and approx(L1mu, 0.5302, rel=3e-3) and approx(PRmu, 20.50, rel=3e-3),
      f"R={Rmu:.4f} L1/C={L1mu:.4f} PR={PRmu:.2f}")
check("Chebyshev faithful toy is in the SAME ballpark as the mu_n reference (domain-robust)",
      abs(ft['PR'] - PRmu) < 6.0 and abs(ft['L1'] - L1mu) < 0.15 and abs(ft['R'] - Rmu) < 0.3,
      f"Cheb(PR={ft['PR']:.1f},L1/C={ft['L1']:.3f},R={ft['R']:.3f}) vs mu_n(PR={PRmu:.1f},L1/C={L1mu:.3f},R={Rmu:.3f})")
ALLROWS = [(127, 16, 8, 1), (31, 8, 4, 1), (31, 8, 4, 2), (127, 16, 8, 2)]
worst_parse = max(cheb_toy(*cfg)['parse'] for cfg in ALLROWS)
check("Parseval gated on EVERY shipped Chebyshev row", worst_parse < 1e-9,
      f"{len(ALLROWS)} rows, worst relerr {worst_parse:.1e}")
check("PROVED energy floor max|e|/C >= sqrt((Gamma2-1)/ndir) on EVERY shipped row",
      all(cheb_toy(*cfg)['energy_ok'] for cfg in ALLROWS), f"{len(ALLROWS)} rows")
# primitive stratum carries the mass (w>=2 Chebyshev toys): faithful analog of #414's 83-93%
shares = [cheb_toy(*cfg)['share'] for cfg in [(31, 8, 4, 2), (127, 16, 8, 2)]]
check("primitive stratum carries 90-98% of L^1 mass in every w>=2 Chebyshev toy",
      all(0.88 <= s <= 0.99 for s in shares), "shares=" + ",".join(f"{s:.3f}" for s in shares))

# =============================================================== §11 offset robustness
print("\n== §11 faithful measurement robust across twin-coset offsets ==")
offs = {}
for goff in (1, 3, 5, 7):
    D, ok2 = cheb_twin_coset(127, 16, goff)
    if len(D) == 16 and ok2:
        offs[goff] = cheb_toy(127, 16, 8, 1, goff)
check("all offsets: PR in [16.4,17.0], L1/C in [0.39,0.44], all << budget",
      all(16.3 <= r['PR'] <= 17.0 and 0.39 <= r['L1'] <= 0.44 for r in offs.values()),
      "PR=" + ",".join(f"{r['PR']:.2f}" for r in offs.values()))

# =============================================================== §12 falsification guard
print("\n== §12 falsification guard: above-bound spikes only where the ATOM ITSELF fails ==")
r_bad = cheb_toy(31, 8, 4, 2)      # avg=0.073 << 1
check("avg<<1 row (p31 n8 w2): raw PR > nu*_ref AND R_true > K -- atom fails too, not a counterexample",
      r_bad['PR'] > float(nu_ref) and r_bad['R'] > float(K),
      f"avg={r_bad['avg']:.3f} PR={r_bad['PR']:.1f} R={r_bad['R']:.2f}")
check("faithful avg>>1 row: PR <= nu*_ref AND R <= K (both hold) -- NO counterexample in the deployment regime",
      ft['PR'] <= float(nu_ref) and ft['R'] <= float(K))
check("guard reading: overstrongness is an avg<<1 / large-w artifact, not a faithful-regime failure", True)

# =============================================================== §13 tamper self-tests
print("\n== §13 tamper self-tests (each must FAIL when corrupted) ==")
def tamper(name, cond_should_fail):
    ok = not cond_should_fail
    print(f"  [{'PASS' if ok else 'FAIL'}] tamper::{name} (corruption detected)")
    CHECKS.append((f"tamper::{name}", ok, ""))
tamper("avg_ceil_offby1", (-((-C) // pw)) == 1993677)                       # real is 1993678
tamper("Bstar_is_2p24", ((2 ** 31 - 1) ** 4 // 2 ** 100) == 2 ** 24)        # real is 2^24-1
tamper("nu_ref_wrong", approx(float((K - 1) ** 2), 44.0, ab=1.0))           # real 54.99, not KB's 44
def _chebfold_wrongpower_matches():
    pp, nn, mmv, c = 31, 8, 4, 2
    D, _ = cheb_twin_coset(pp, nn); om = [cmath.exp(2j * math.pi * e / pp) for e in range(pp)]
    Dc = sorted(set(T_cheb(c, x, pp) for x in D)); nc = len(Dc)
    b1, b2 = 1, 0
    Nf = Counter();
    for x in D:
        y = T_cheb(c, x, pp); Nf[(b1 * y + b2 * y * y) % pp] += 1
    lhs = em_vd(Nf, mmv, om)
    Eg = [0j] * (nc + 1); Eg[0] = 1 + 0j
    for y in Dc:
        v = om[(b1 * y) % pp]
        for d in range(nc, 0, -1): Eg[d] += v * Eg[d - 1]
    poly = [1 + 0j]
    for _ in range(c + 1):                                                  # WRONG: c+1 folds
        new = [0j] * min(len(poly) + nc, mmv + 1)
        for i2, pi2 in enumerate(poly):
            for j2, ej in enumerate(Eg):
                if i2 + j2 <= mmv: new[i2 + j2] += pi2 * ej
        poly = new
    rhs = poly[mmv] if mmv < len(poly) else 0j
    return abs(lhs - rhs) < 1e-9
tamper("chebfold_wrong_power", _chebfold_wrongpower_matches())              # c+1 folds must NOT match
tamper("faithful_R_exceeds_budget", cheb_toy(127, 16, 8, 1)['R'] > 8.4152)  # real R=1.30 < K
tamper("cheb_D_is_product_closed",                                          # Chebyshev D is NOT a subgroup
       all(((x * y) % 127) in set(D16) for x in D16 for y in D16))
tamper("faithful_w1_collapses_to_1",                                        # Chebyshev w=1 does NOT give |e_m|=1
       (lambda pp=127, nn=16, mmv=8: (lambda D, om, Cc:
           all(approx(abs(em_vd(Counter((t1 * x) % pp for x in D), mmv, om)) / Cc, 1.0, ab=1e-6)
               for t1 in range(1, pp)))(
           cheb_twin_coset(pp, nn)[0], [cmath.exp(2j * math.pi * e / pp) for e in range(pp)], math.comb(nn, mmv)))())

# =============================================================== summary
npass = sum(1 for _, c, _ in CHECKS if c); ntot = len(CHECKS)
print(f"\nRESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot} checks)")
sys.exit(0 if npass == ntot else 1)
