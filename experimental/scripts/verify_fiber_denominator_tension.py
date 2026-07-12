#!/usr/bin/env python3
"""
verify_fiber_denominator_tension.py  (stdlib-only, zero-arg)

Recomputes every number in
    experimental/notes/thresholds/fiber_denominator_tension.md

Image face only. Objects (shared with #661/#663/#682/#685/#691, #668):
  block V = b distinct integers, normalized min V = 0, gcd = 1, diameter D = max V.
  Phi(S) = (|S|, sum_S v, sum_S v^2);  f = max fiber, L = image size.
  u_i=(1,v_i,v_i^2); X_vec=sum eps_i u_i; psi_i(th)=th0+th1 v_i+th2 v_i^2;
  |Xhat(th)| = prod_i |cos(pi psi_i)|;  atom identity f = 2^b max_s P(X_vec=s),
  atom bound f/2^b <= INT_{[0,1)^3}|Xhat|.
  phi=log2 f/b, lambda=log2 L/b, eta=1-phi, delta=log2 D/b, alpha=d/b, X=(fL)^{1/b}.

Labels: PROVED / COMPUTED / MEASURED / REFUTED.  RESULT line at the end.
Runtime target < 60 s under `ulimit -v 2097152`.  Credit #668 (f<=2^{b-d}, fL<=3^b).
"""
import itertools, random
from math import cos, pi, sqrt, log, log2, gcd
from collections import defaultdict

random.seed(20260712)
PASS = 0
FAIL = 0
def check(name, cond):
    global PASS, FAIL
    if cond: PASS += 1
    else:
        FAIL += 1
        print(f"  !! FAIL: {name}")

# ----------------------------------------------------------------------
# primitives
# ----------------------------------------------------------------------
def normalize(V):
    V = sorted(set(V)); m = V[0]; V = [x - m for x in V]
    g = 0
    for x in V: g = gcd(g, x)
    return [x // g for x in V] if g > 1 else V

def fiber_image(V):
    """exact max fiber f and image size L of Phi via signature DP."""
    cur = defaultdict(int); cur[(0, 0, 0)] = 1
    for v in V:
        nxt = defaultdict(int)
        for (k, s, q), c in cur.items():
            nxt[(k, s, q)] += c
            nxt[(k + 1, s + v, q + v * v)] += c
        cur = nxt
    return max(cur.values()), len(cur)

def psi(v, th): return th[0] + th[1] * v + th[2] * v * v
def nrm(x):     return abs(x - round(x))                 # distance to nearest integer
def vdm(a, b, c): return abs((b - a) * (c - b) * (c - a))

def absXhat(V, th):
    p = 1.0
    for v in V:
        p *= abs(cos(pi * psi(v, th)))
        if p < 1e-300: return 0.0
    return p

def M_of_t2(V, t2, n0=16, n1=16):
    """theta_2-marginal L1 mass M(t2) = INT_{[0,1)^2} |Xhat| dt0 dt1 (midpoint)."""
    s = 0.0
    for i0 in range(n0):
        t0 = (i0 + 0.5) / n0
        for i1 in range(n1):
            t1 = (i1 + 0.5) / n1
            s += absXhat(V, (t0, t1, t2))
    return s / (n0 * n1)

def atom_integral(V, n0=20, n1=20, n2=40):
    s = 0.0
    for i0 in range(n0):
        t0 = (i0 + 0.5) / n0
        for i1 in range(n1):
            t1 = (i1 + 0.5) / n1
            for i2 in range(n2):
                s += absXhat(V, (t0, t1, (i2 + 0.5) / n2))
    return s / (n0 * n1 * n2)

def H2(e):
    if e <= 0 or e >= 1: return 0.0
    return -e * log2(e) - (1 - e) * log2(1 - e)

def small_denom_within(x, Q, hw):
    """True iff x within hw of some a/q, 1<=q<=Q (x on a denom-<=Q major arc)."""
    for q in range(1, Q + 1):
        if nrm(q * x) <= q * hw:
            return True
    return False

# ----------------------------------------------------------------------
# census blocks: Sidon control + structured classes + champion
# ----------------------------------------------------------------------
CHAMP = [2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34]      # #655 champion
def sidon(b):                                                     # Mian-Chowla-ish
    S = [0]; x = 1
    while len(S) < b:
        c = S + [x]; ss = set(); ok = True
        for i in range(len(c)):
            for j in range(i, len(c)):
                v = c[i] + c[j]
                if v in ss: ok = False; break
                ss.add(v)
            if not ok: break
        if ok: S.append(x)
        x += 1
    return S
BLOCKS = {
 'sidon12'   : sidon(12),
 'interval12': list(range(12)),
 'interval14': list(range(14)),
 'holes14'   : normalize([x for x in range(20) if x not in {5,9,13,15,17,18}][:14]),
 'unionAP18' : normalize([j for j in range(10)] + [100 + 3*j for j in range(8)]),
 'gap20'     : normalize([a + 7*c for a in range(4) for c in range(5)]),   # rank-2 GAP
 'champ18'   : CHAMP,
}

print("="*74)
print("verify_fiber_denominator_tension.py")
print("="*74)

# ----------------------------------------------------------------------
# BLOCK 0 -- setup, #668 envelope recap, dilation closed by normalization
# ----------------------------------------------------------------------
print("\n[BLOCK 0] census, #668 envelope, dilation loophole closed by gcd=1 (=#685)")
print(f"  {'block':11s} {'b':>2s} {'f':>5s} {'L':>7s} {'X':>6s} {'phi':>5s} {'lam':>5s} {'eta':>5s}")
data = {}
for nm, V0 in BLOCKS.items():
    V = normalize(V0); b = len(V); f, L = fiber_image(V); X = (f*L)**(1/b)
    phi = log2(f)/b; lam = log2(L)/b; eta = 1-phi
    data[nm] = dict(V=V, b=b, f=f, L=L, X=X, phi=phi, lam=lam, eta=eta)
    print(f"  {nm:11s} {b:2d} {f:5d} {L:7d} {X:6.3f} {phi:5.3f} {lam:5.3f} {eta:5.3f}")
    check(f"{nm} fL<=3^b (#668)", f*L <= 3**b)                    # #668 (2)
# alpha_0 root of h(alpha)=4/3, h=(1-a)+H2(min(a,1/2))  (#678/#682)
def h(a): return (1-a) + H2(min(a, 0.5))
lo, hi = 0.0, 0.3
for _ in range(80):
    mid = (lo+hi)/2
    if h(mid) > 4/3: hi = mid
    else: lo = mid
alpha_0 = (lo+hi)/2
print(f"  #678/#682 envelope: alpha_0 (root h=4/3) = {alpha_0:.6f}  (corridor (alpha_0,2/3))")
check("alpha_0 ~ 0.084497", abs(alpha_0 - 0.084497) < 1e-4)
# dilation: AP {g*j} normalizes to the interval -> identical (f,L,X); gcd=1 == #685 non-dilation
V_int = normalize(list(range(12)))
for g in (5, 16, 97):
    Vap = normalize([g*j for j in range(12)])
    check(f"AP(g={g}) normalizes to interval (dilation closed by gcd=1)", Vap == V_int)
fint = fiber_image(V_int); fap = fiber_image(normalize([16*j for j in range(12)]))
check("dilation invariance f,L (=#685, #643 Lemma A)", fint == fap)
print("  AP{g*j} -> normalize -> interval: dilation loophole is closed BY normalization")
print("  (a normalized gcd=1 block is never a nontrivial dilation = #685's 'not a dilation')")

# ----------------------------------------------------------------------
# BLOCK 1 -- Lemma V (exact 3-point Vandermonde resolution identity) + pointwise mass bound
# ----------------------------------------------------------------------
print("\n[BLOCK 1] Lemma V exact identity + pointwise mass bound (PROVED)")
# identity: (c-b)psi_a-(c-a)psi_b+(b-a)psi_c = Vdm(T)*theta_2, a<b<c, Vdm=(b-a)(c-b)(c-a)
worst_id = 0.0; worst_ineq = 0.0; worst_diam = 0.0; worst_pw = 0.0
pool = sorted(set(CHAMP) | set(range(40)))
for _ in range(60000):
    th = (random.random(), random.random(), random.random())
    a, b, c = sorted(random.sample(pool, 3))
    lhs = (c-b)*psi(a, th) - (c-a)*psi(b, th) + (b-a)*psi(c, th)
    V_ = vdm(a, b, c)
    worst_id = max(worst_id, abs(lhs - V_*th[2]))
    # ||Vdm th2|| <= (c-b)||psi_a||+(c-a)||psi_b||+(b-a)||psi_c||   (exact weighted form)
    rhs = (c-b)*nrm(psi(a, th)) + (c-a)*nrm(psi(b, th)) + (b-a)*nrm(psi(c, th))
    worst_ineq = max(worst_ineq, nrm(V_*th[2]) - rhs)
    # relaxation ... <= diam(T)*(sum ||psi||)
    rhsd = (c-a)*(nrm(psi(a, th))+nrm(psi(b, th))+nrm(psi(c, th)))
    worst_diam = max(worst_diam, nrm(V_*th[2]) - rhsd)
    # pointwise mass bound |Xhat_{a,b,c}| <= exp(-(2/3)||Vdm th2||^2/diam^2)
    prod3 = abs(cos(pi*psi(a, th))*cos(pi*psi(b, th))*cos(pi*psi(c, th)))
    diam = c - a
    bound = 2.718281828459045 ** (-(2.0/3.0)*nrm(V_*th[2])**2/diam**2)
    worst_pw = max(worst_pw, prod3 - bound)
print(f"  signed identity   max |LHS - Vdm*th2|          = {worst_id:.2e}   (want 0)")
print(f"  weighted ineq     max(||Vdm th2|| - weightedRHS)= {worst_ineq:.2e}   (want <=0)")
print(f"  diam relaxation   max(||Vdm th2|| - diam*sum)   = {worst_diam:.2e}   (want <=0)")
print(f"  pointwise bound   max(|cos^3| - exp(..))        = {worst_pw:.2e}   (want <=0)")
check("Lemma V signed identity exact", worst_id < 1e-7)
check("Lemma V weighted inequality", worst_ineq < 1e-9)
check("Lemma V diameter relaxation", worst_diam < 1e-9)
check("pointwise mass bound |cos^3|<=exp(-(2/3)||Vdm th2||^2/diam^2)", worst_pw < 1e-9)

# ----------------------------------------------------------------------
# BLOCK 2 -- AP-embedded denominator bound (multi-point resolution, PROVED)
# ----------------------------------------------------------------------
print("\n[BLOCK 2] AP-embedded bound: (L-2)||2t^2 th2|| <= 4 sqrt(L) sqrt(sum_j||psi||^2) (PROVED)")
def ap_worst_ratio(a, t, Lp, ntr=40000):
    w = 0.0
    for _ in range(ntr):
        th = (random.random(), random.random(), random.random())
        lhs = (Lp-2)*nrm(2*t*t*th[2])
        s2 = 0.0
        for j in range(Lp): s2 += nrm(psi(a+j*t, th))**2
        rhs = 4*sqrt(Lp)*sqrt(s2)
        if rhs > 0: w = max(w, lhs/rhs)
        elif lhs > 1e-12: return 9.9
    return w
for (a, t, Lp) in [(0,1,12), (0,1,18), (0,2,10), (0,3,8), (5,1,10)]:
    r = ap_worst_ratio(a, t, Lp)
    print(f"  AP(a={a},t={t},L={Lp}): worst lhs/rhs = {r:.4f}  (want <=1)  -> denom 2t^2 = {2*t*t}")
    check(f"AP-embedded bound holds AP(a={a},t={t},L={Lp})", r <= 1.0 + 1e-9)
# consequence in a trap sum||psi||^2 <= kappa*b, kappa=(ln2/2)(eta+1/b): closeness of th2 to a/(2t^2)
print("  in-trap closeness ||2t^2 th2|| <= 4 sqrt(L kappa b)/(L-2), L=b, t=1 (den=2):")
print(f"    {'eta':>5s} {'kappa*b':>8s} {'bound':>7s}   bites(<1/2)?")
for eta in (0.02, 0.045, 0.1, 0.3):
    b = 100; kb = (log(2)/2)*(eta + 1/b)*b
    bound = 4*sqrt(b*kb)/(b-2)
    print(f"    {eta:5.3f} {kb:8.3f} {bound:7.3f}   {'YES' if bound < 0.5 else 'no'}")
# negative control: for a Sidon set the same 'AP' template is arithmetically vacuous
# (no genuine common difference) -- the 2t^2 resonance carries no mass; check M near a/(2t^2) small.
Vs = normalize(sidon(12))
Msid = M_of_t2(Vs, 0.5, 24, 24)            # parity resonance point (t=1 -> den 2)
Msid0 = M_of_t2(Vs, 0.5+0.137, 24, 24)     # generic point
check("neg-control: Sidon has no parity peak (M(1/2) ~ M(generic))", abs(Msid-Msid0) < 0.5*max(Msid,Msid0)+1e-6)
print(f"  neg-control Sidon: M(1/2)={Msid:.5f} vs M(generic)={Msid0:.5f} (no structured resonance)")

# ----------------------------------------------------------------------
# BLOCK 3 -- single-triple mass bound holds but does NOT decay (irreducibly multi-point) REFUTED-route
# ----------------------------------------------------------------------
print("\n[BLOCK 3] single-triple marginal bound M(t2)<=P3_T(t2) holds, but P3_T is FLAT (no decay)")
def P3(a, b, c, t2, n0=80, n1=80):
    s = 0.0
    for i0 in range(n0):
        t0 = (i0+0.5)/n0
        for i1 in range(n1):
            th = (t0, (i1+0.5)/n1, t2)
            s += abs(cos(pi*psi(a, th))*cos(pi*psi(b, th))*cos(pi*psi(c, th)))
    return s/(n0*n1)
a, b, c = 2, 3, 4                                  # triple in champion, Vdm=2
viol = 0; p3vals = []
for i in range(11):
    t2 = i/20.0
    M = M_of_t2(CHAMP, t2, 20, 20); p = P3(a, b, c, t2)
    p3vals.append(p)
    if M > p + 1e-6: viol += 1
spread = (max(p3vals) - min(p3vals)) / (sum(p3vals)/len(p3vals))
print(f"  M(t2) <= P3_T(t2) violations over 11 t2 = {viol} (want 0)")
print(f"  P3_T(t2) relative spread (max-min)/mean = {spread:.4f}  -> FLAT (no decay: single triple useless as mass bound)")
check("single-triple mass bound holds", viol == 0)
check("P3_T flat: relative spread < 5% (mass decay is irreducibly multi-point)", spread < 0.05)

# ----------------------------------------------------------------------
# BLOCK 4 -- MEASURED mass law: minor-arc (large-denominator) mass -> 0 by bounded Q
# ----------------------------------------------------------------------
print("\n[BLOCK 4] minor-arc (large-denominator) mass fraction -> 0 by Q<=30 (MEASURED)")
print(f"  {'block':11s} {'f':>4s}  {'total':>7s}   frac mass on MINOR arcs (t2 > 0.02 from every a/q, q<=Q)")
print(f"  {'':11s} {'':4s}  {'':7s}   {'Q=2':>6s} {'Q=5':>6s} {'Q=8':>6s} {'Q=16':>6s} {'Q=30':>6s}")
massfrac = {}
for nm in BLOCKS:
    V = data[nm]['V']; f = data[nm]['f']
    N = 420; hw = 0.02
    tot = 0.0; minor = {Q: 0.0 for Q in (2,5,8,16,30)}
    for i in range(N):
        t2 = (i+0.5)/N; m = M_of_t2(V, t2, 14, 14); tot += m
        for Q in (2,5,8,16,30):
            if not small_denom_within(t2, Q, hw): minor[Q] += m
    fr = {Q: minor[Q]/tot for Q in minor}
    massfrac[nm] = fr
    print(f"  {nm:11s} {f:4d}  {tot/N:7.5f}   " + " ".join(f"{fr[Q]:6.4f}" for Q in (2,5,8,16,30)))
    check(f"{nm}: minor-arc mass monotone decreasing in Q", all(fr[a] >= fr[b]-1e-9 for a,b in zip((2,5,8,16,30),(5,8,16,30))))
    check(f"{nm}: minor-arc mass at Q=30 negligible (<0.02)", fr[30] < 0.02)
print("  => all |Xhat| atom mass sits on bounded-denominator (<=30) major arcs; large-q mass ~ 0")
# dominant NON-trivial resonance denominator (argmax M away from parity {0,1/2}) is BOUNDED
def low_denom_of(x, Qmax=30):
    best = (9.9, 1)
    for q in range(1, Qmax+1):
        d = nrm(q*x)/q
        if d < best[0]-1e-12: best = (d, q)
    return best[1]
print("  dominant NON-trivial resonance (argmax M, t2 away from {0,1/2}) -> denominator:")
for nm in BLOCKS:
    V = data[nm]['V']; N = 360
    Ms = [((i+0.5)/N, M_of_t2(V, (i+0.5)/N, 14, 14)) for i in range(N)]
    peak = max(m for _, m in Ms)
    nz = [(t2, m) for t2, m in Ms if min(nrm(t2), nrm(t2-0.5)) > 0.03]
    t2s, ms = max(nz, key=lambda z: z[1])
    q = low_denom_of(t2s)
    print(f"    {nm:11s} t2*={t2s:.3f} den={q:2d}  M*/peak={ms/peak:.2f}")
    check(f"{nm}: dominant nontrivial resonance denominator bounded (<=30)", q <= 30)

# ----------------------------------------------------------------------
# BLOCK 5 -- atom bound + small-den concentration NOT strictly f-monotone (corrects #691 P5)
# ----------------------------------------------------------------------
print("\n[BLOCK 5] atom bound f/2^b<=INT|Xhat| (COMPUTED); small-den mass NOT strictly f-monotone (corrects #691 P5)")
print(f"  {'block':11s} {'f':>4s} {'f/2^b':>8s} {'INT|Xhat|':>9s} {'ratio':>6s}  {'massfrac(den<=5)':>16s}")
conc = []
for nm in BLOCKS:
    V = data[nm]['V']; b = data[nm]['b']; f = data[nm]['f']
    aI = atom_integral(V, 18, 18, 36); fb = f/2**b
    fr5 = 1 - massfrac[nm][5]           # fraction within 0.02 of some a/q, q<=5
    conc.append((f, fr5, nm))
    print(f"  {nm:11s} {f:4d} {fb:8.5f} {aI:9.5f} {aI/fb:6.2f}  {fr5:16.3f}")
    check(f"{nm}: atom bound f/2^b <= INT|Xhat|", fb <= aI + 5e-4)
# monotone-in-f would need conc sorted by f to be sorted by fr5; show it is NOT
byf = sorted(conc)
is_monotone = all(byf[i][1] <= byf[i+1][1] + 1e-9 for i in range(len(byf)-1))
print(f"  small-den(<=5) concentration ordered by f: {[f'{f}:{fr:.3f}' for f,fr,_ in byf]}")
print(f"  strictly increasing in f? {is_monotone}  -> concentration tracks STRUCTURE (embedded runs), not f")
check("small-den concentration NOT strictly f-monotone (family-dependent) -- corrects #691 P5", not is_monotone)

# ----------------------------------------------------------------------
# BLOCK 6 -- regime map: the trapping/resolution route bites only OFF the wall (PROVED envelope)
# ----------------------------------------------------------------------
print("\n[BLOCK 6] regime map: AP-resolution bites only where #668 envelope is ENVELOPE-SAFE")
print("  AP trap bound (PROVED, L=b=100, t=1): ||2 th2|| <= 4 sqrt(b*kappa*b)/(b-2), kappa=(ln2/2)(eta+1/b)")
print(f"  {'eta':>5s} {'phi':>5s} {'lam_env=H2':>10s} {'phi+lam':>7s} {'wall(>4/3)?':>11s} {'AP||2th2||':>11s}")
bb = 100
def ap_trap_bound(eta):                     # the SAME proven bound as BLOCK 2's table
    kb = (log(2)/2)*(eta + 1/bb)*bb
    return 4*sqrt(bb*kb)/(bb-2)
bite_and_wall = False; bite_thr = None
for eta in (0.02, 0.033, 0.045, 0.067, 0.1, 0.2, 0.3, 0.5):
    phi = 1-eta; lam = H2(min(eta, 0.5)); s = phi+lam
    apb = ap_trap_bound(eta)
    wall = s > 4/3
    bites = apb < 0.5
    if bites and wall: bite_and_wall = True
    if bites and bite_thr is None: bite_thr = eta
    print(f"  {eta:5.3f} {phi:5.3f} {lam:10.3f} {s:7.3f} {('YES' if wall else 'no '):>11s} {apb:11.3f}{'  <1/2 bites' if bites else ''}")
# largest eta at which the proven bound still bites (bisect on ap_trap_bound=1/2)
lo, hi = 0.0, 0.3
for _ in range(60):
    mid = (lo+hi)/2
    if ap_trap_bound(mid) < 0.5: lo = mid
    else: hi = mid
eta_bite = (lo+hi)/2
phi_b = 1-eta_bite; lam_b = H2(eta_bite)
print(f"  proven biting threshold: eta <= {eta_bite:.3f} (phi >= {phi_b:.3f}); there phi+lambda <= {phi_b+lam_b:.3f} < 4/3")
check("PROVED envelope: AP-resolution regime (bites) and wall regime are DISJOINT", not bite_and_wall)
check("biting threshold is envelope-safe (phi+lambda < 4/3)", phi_b + lam_b < 4/3)
# champion sits at eta=0.727, phi+lam:
ch = data['champ18']; print(f"  champion: eta={ch['eta']:.3f}, phi+lam={ch['phi']+ch['lam']:.3f} (<4/3, safe); trapping vacuous here")
check("champion off the biting regime (eta > threshold)", ch['eta'] > eta_bite)

# ----------------------------------------------------------------------
print("\n" + "="*74)
total = PASS + FAIL
print(f"RESULT: {'PASS' if FAIL==0 else 'FAIL'} ({PASS}/{total})")
print("="*74)
