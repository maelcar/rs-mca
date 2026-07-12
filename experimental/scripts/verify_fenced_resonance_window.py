#!/usr/bin/env python3
"""
Verifier for experimental/notes/thresholds/fenced_resonance_window.md

The image-face Bohr->GAP wall (#661 exp_ilo_fourier, #663 bohr_gap_volume) asks
whether the dominant resonance denominator q of the quadratic Bohr set trapping a
high-fiber block can be controlled.  Today's fencing (#682 corridor_diameter_map,
#685 corridor_interior_hunt) narrowed the wall's habitat: any wall-carrying block
(X=(fL)^{1/b} > 2^{4/3}) has diameter exponent delta = log2(D)/b > alpha/3 + 1/9
(so delta >= 1/3 near the fence), large detG, and is not a dilation.  This packet
re-runs the denominator question ON the fenced class and recomputes every number:

  BLOCK 0  setup: alpha_0 root, the #682 residual line delta_res=(alpha+1/3)/3,
           and the two invariances the argument rests on -- affine (v->av+c) and
           single-residue reduction (v=r+q v'') leave (f,L) EXACTLY fixed
           (#643 Lemma A / #685); a non-affine map does not.
  BLOCK 1  fiber-trapping DECOUPLING (COMPUTED): a generic b-subset of ANY
           quadratic Bohr set -- rational a/q OR the #663 golden-ratio
           Diophantine set -- is Sidon (f=1).  Bohr trapping is metric; the
           fiber is additive.  So #663's counterexample is a non-GAP SET, not a
           high-fiber wall-BLOCK: route (B) needs more than the golden family.
  BLOCK 2  the resolution ceiling (PROVED): the width-w trap resolves a
           denominator q only if q <= Q_res = 1/(2w); w = sqrt((ln2/2)(eta+1/b)/eps)
           is minimized at eps=1, eta->0, giving Q_res_max = sqrt(b/(2 ln2)) =
           0.84932 sqrt(b) -- POLYNOMIAL in b.  Residue-count transition at
           q ~ 1/(2w) reproduced exactly.
  BLOCK 3  host-smallness threshold (PROVED): dividing out q reduces delta by
           exactly log2(q)/b (dilation); the residue host stays diameter-scaled,
           so the corridor bound lambda<=alpha+1/3 needs log2(q)/b >= beta :=
           delta - alpha/3 - 1/9 > 0.  In the fenced region 3 delta > alpha+1/3:
           the trivial box bound is already useless, the horn must CUT delta.
  BLOCK 4  MAIN RESULT -- the denominator window is EMPTY (PROVED): the horn
           needs q >= q_cross = 2^{beta b} (exponential) but can only resolve
           q <= Q_res_max = 0.849 sqrt(b) (polynomial); q_cross > Q_res for all
           b > b_0(beta) (tabulated).  The delta at which the window closes
           (beta=0) is EXACTLY #682's residual line -- Bohr face = box face.
  BLOCK 5  the TENSION (COMPUTED, evidence for closure): high-fiber blocks
           concentrate INT|Xhat| at SMALL denominators (monotone in f) and have
           SMALL nontrivial secondary peaks; a Diophantine (large-q) resonance
           carries little fiber.  Every computed block obeys X < 2^{4/3}.
  BLOCK 6  reduction descent & #663 R3 sharpening (PROVED/AUDIT): the productive
           single-class reduction is a dilation (excluded by #685); a two-class
           block does NOT factor (cross-class collisions), so the reduction
           stalls at multi-class -- the open recursion.  #663 R3's bounded-q host
           recomputed ~ D (diameter-scaled), confirming it cannot close the fence.

stdlib only; zero-arg; deterministic (all witnesses hardcoded or fixed-seed);
target < 60 s under `ulimit -v 2097152`.  Nonzero exit on any FAIL.

Credit (consumed read-only, by PR number): DannyExperiments #668 (f<=2^{b-d},
fL<=3^b, the fiber bound the fence rests on); #661 exp_ilo_fourier (Theorem A/B,
T_kappa, the wall statement); #663 bohr_gap_volume (R3 rational horn, the golden
counterexample, the detG dichotomy); #682 corridor_diameter_map (delta coordinate,
residual line, Cor 2 inflation); #685 corridor_interior_hunt (dilation invariance,
the non-dilation fence); #657/#655/#646/#643/#673/#678/#683 (moment-map chain,
champion, affine invariance, rank-r GAP box bound, corridor); hughes #564 (PTE
support 6).  No signed mu_n / max-fiber reduction object is entered (that is
hughes's #564 lane); this stays on the image face (f, L, Phi).
"""
import sys, math, random
from fractions import Fraction

PASS = 0
FAIL = 0
def check(cond, msg):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        print("  FAIL:", msg)
    return cond

LN2 = math.log(2.0)
TARGET = 2 ** (4/3)          # 2.5198420997897464
CHAMP18 = [2,3,4,6,13,14,15,16,17,19,20,21,22,23,30,32,33,34]

# ------------------------------------------------------------------ primitives
def f_and_L(V):
    """Exact max fiber f and image size L of the degree-2 signature map."""
    state = {(0,0,0):1}
    for v in V:
        vv = v*v; ns = dict(state)
        for (a,s,q),c in state.items():
            k = (a+1, s+v, q+vv); ns[k] = ns.get(k,0)+c
        state = ns
    return max(state.values()), len(state)

def rates(V):
    b = len(V); f,L = f_and_L(V)
    D = max(V)-min(V)
    return dict(b=b, f=f, L=L, D=D,
                phi=math.log2(f)/b, lam=math.log2(L)/b,
                delta=(math.log2(D)/b if D>0 else 0.0),
                X=(f*L)**(1.0/b))

def H2(x):
    if x <= 0 or x >= 1: return 0.0
    return -x*math.log2(x) - (1-x)*math.log2(1-x)

def h(alpha):                # #678 envelope exponent
    return (1-alpha) + H2(min(alpha, 0.5))

def frac(x):
    return abs(x - round(x))

def absXhat(V, th0, th1, th2):
    p = 1.0
    for v in V:
        p *= abs(math.cos(math.pi*(th0 + th1*v + th2*v*v)))
        if p < 1e-12: return p
    return p

def best_th0th1(V, th2, N0=16, N1=24):
    m = 0.0
    for i1 in range(N1):
        th1 = i1/N1
        for i0 in range(N0):
            val = absXhat(V, i0/N0, th1, th2)
            if val > m: m = val
    return m

print("="*74)
print("BLOCK 0 -- setup, alpha_0, residual line, and the two invariances")
print("="*74)
# alpha_0 = root of h(alpha) = 4/3 on (0, 1/2), by bisection
lo, hi = 1e-6, 0.5
for _ in range(200):
    mid = 0.5*(lo+hi)
    if h(mid) > 4/3: hi = mid
    else: lo = mid
alpha_0 = 0.5*(lo+hi)
print(f"  alpha_0 (root h=4/3)          = {alpha_0:.6f}   (target 0.084497)")
check(abs(alpha_0 - 0.084497) < 1e-5, "alpha_0 ~ 0.084497")
check(abs(h(2/3) - 4/3) < 1e-9, "h(2/3) = 4/3")
# residual line identity delta_res(alpha) = (alpha+1/3)/3 = alpha/3 + 1/9
for al in [alpha_0, 1/3, 0.5, 2/3]:
    check(abs((al+1/3)/3 - (al/3 + 1/9)) < 1e-12, f"residual line identity at alpha={al:.3f}")
check(abs((alpha_0+1/3)/3 - 0.139277) < 1e-5, "delta_res(alpha_0) = 0.13928")
check(abs((2/3+1/3)/3 - 1/3) < 1e-12, "delta_res(2/3) = 1/3")
print(f"  delta_res(alpha_0)={ (alpha_0+1/3)/3:.5f}  delta_res(2/3)={(2/3+1/3)/3:.5f}  (full corridor at delta>=1/3)")

# affine invariance v -> a v + c leaves (f,L) fixed; non-affine does not
random.seed(11)
Vbase = sorted(random.sample(range(0, 200), 12))
f0, L0 = f_and_L(Vbase)
for a in [1, 7, -3, 13]:
    for c in [0, 5, -101]:
        f1, L1 = f_and_L([a*v + c for v in Vbase])
        check((f1, L1) == (f0, L0), f"affine (a={a},c={c}) preserves (f,L)")
# single-residue reduction v = r + q v'' : f,L(V) == f,L(V'')
for q in [3, 50, 1000]:
    for r in [0, 7]:
        Vq = [r + q*v for v in Vbase]
        check(f_and_L(Vq) == (f0, L0), f"single-residue reduction q={q},r={r} preserves (f,L)")
# NEGATIVE: (f,L) is only AFFINE-invariant; a non-affine relabel changes it.
# interval[0,12) (structured, f>1) vs its non-affine dissociated image {2^v} (f=1).
fI, LI = f_and_L(list(range(12)))
fN, LN = f_and_L([2**v for v in range(12)])
check(fI > 1 and fN == 1 and (fN, LN) != (fI, LI),
      "NEGATIVE: non-affine relabel v->2^v changes (f,L) (invariance is affine-only)")
print(f"  affine/dilation/shift preserve (f,L)={f0,L0}; but non-affine v->2^v maps "
      f"interval (f={fI}) to a dissociated set (f={fN}) -- invariance is AFFINE-only")

print("="*74)
print("BLOCK 1 -- fiber-trapping DECOUPLING: Bohr trap is metric, fiber is additive")
print("="*74)
# rational Bohr trap theta2=a/q
def trap_rational(a, q, th1, w, Dmax):
    return [v for v in range(Dmax+1) if frac(a*v*v/q + th1*v) <= w]
# Diophantine golden Bohr trap (#663)
def trap_golden(th1, w, Dmax):
    g = (math.sqrt(5)-1)/2
    return [v for v in range(Dmax+1) if frac(g*v*v + th1*v) <= w]

trapR = trap_rational(1, 97, 0.11, 0.10, 6000)      # large q -> equidistributing
trapG = trap_golden(0.30, 0.06, 4000)               # the #663 golden set
print(f"  rational q=97 trap: |B|={len(trapR)}   golden trap: |B|={len(trapG)}")
# generic b-subsets of each trap are Sidon (f=1)
for name, trap, bb in [("rational-q97", trapR, 14), ("golden", trapG, 14)]:
    sidon_count = 0; ntest = 8
    for seed in range(ntest):
        random.seed(1000+seed)
        V = sorted(random.sample(trap, bb))
        if f_and_L(V)[0] == 1: sidon_count += 1
    print(f"  {name}: {sidon_count}/{ntest} random b={bb} subsets are Sidon (f=1)")
    check(sidon_count == ntest, f"{name}: all sampled Bohr-trapped subsets Sidon")
# NEGATIVE: an interval (additive structure) has f>1 -- fiber is additive, not metric
check(f_and_L(list(range(14)))[0] > 1, "NEGATIVE: interval (additive) has f>1")
print(f"  contrast: interval[0,14) has f={f_and_L(list(range(14)))[0]} (additive structure => fiber)")

print("="*74)
print("BLOCK 2 -- the resolution ceiling Q_res = 1/(2w) <= 0.84932 sqrt(b)")
print("="*74)
def width(eta, eps, b):
    return math.sqrt((LN2/2)*(eta + 1.0/b)/eps)
const = 1.0/math.sqrt(2*LN2)
print(f"  1/sqrt(2 ln2) = {const:.6f}")
check(abs(const - 0.849322) < 1e-5, "resolution constant 0.84932")
for b in [50, 100, 200, 500, 1000]:
    wmin = width(1e-12, 1.0, b)          # eps=1 (all-exception limit), eta->0
    Qres = 1/(2*wmin)
    approx = const*math.sqrt(b)
    check(abs(Qres - approx) < 1e-6*approx + 1e-6, f"Q_res_max = 0.84932 sqrt(b) at b={b}")
    # any smaller eps or larger eta only shrinks w further? no: eps<1 or eta>0 makes w LARGER -> Qres SMALLER
    check(width(0.05, 0.5, b) >= wmin, f"w(eta=.05,eps=.5) >= w_min at b={b}")
    print(f"  b={b:5d}: Q_res_max={Qres:.3f}  (a width-w trap NEVER resolves q>{Qres:.1f})")
# residue-count transition at q ~ 1/(2w)
print("  residue-count transition (theta2=a/q, count r in [0,q) with ||a r^2/q||<=w):")
for q in [7, 20, 100, 600]:
    w = 0.10
    cnt = sum(1 for r in range(q) if frac(1*r*r/q) <= w)
    print(f"    q={q:3d} w={w}: #residues={cnt:3d}  (2wq={2*w*q:.0f}, 1/(2w)={1/(2*w):.0f})")
    if q <= 1/(2*w):
        check(cnt <= 4, f"q={q}<=1/(2w): few residues (congruence regime)")
    else:
        check(cnt >= 0.5*2*w*q, f"q={q}>1/(2w): ~2wq residues (equidistributed regime)")

print("="*74)
print("BLOCK 3 -- host-smallness threshold beta and box-bound uselessness")
print("="*74)
# dividing out q reduces delta by exactly log2(q)/b (dilation), (f,L) fixed
Vint = list(range(16)); r16 = rates(Vint)
for q in [8, 256, 65536]:
    rq = rates([q*v for v in Vint])
    check(rq['f']==r16['f'] and rq['L']==r16['L'], f"q={q}: (f,L) fixed under dilation")
    check(abs(rq['delta'] - (r16['delta'] + math.log2(q)/16)) < 1e-9,
          f"q={q}: delta increases by exactly log2(q)/b")
print(f"  interval[0,16): delta={r16['delta']:.3f}; x{65536} -> delta={rates([65536*v for v in Vint])['delta']:.3f}"
      f"  (lam,f unchanged: dividing by q would cut delta by log2(q)/b)")
# corridor needs log2(q)/b >= beta; and fenced => 3 delta > alpha+1/3 (box useless)
for al, dfen in [(alpha_0, alpha_0/3+1/9+0.01), (0.4, 0.4/3+1/9+0.02), (2/3, 2/3/3+1/9+0.01)]:
    beta = dfen - al/3 - 1/9
    check(beta > 0, f"fenced beta>0 at alpha={al:.3f}")
    check(3*dfen > al + 1/3, f"box bound 3 delta > corridor alpha+1/3 at alpha={al:.3f}")
    print(f"  alpha={al:.3f} fenced delta={dfen:.3f}: beta={beta:.4f}>0, "
          f"3delta={3*dfen:.3f} > alpha+1/3={al+1/3:.3f} (box useless, must CUT delta)")

print("="*74)
print("BLOCK 4 -- MAIN RESULT: the denominator window is EMPTY on the fenced class")
print("="*74)
def b0(beta):
    b = 2
    while not (2**(beta*b) > const*math.sqrt(b)):
        b += 1
        if b > 10**6: return None
    return b
print("   beta     q_cross=2^{beta b}   vs   Q_res_max=0.849 sqrt b :  window empties at b_0")
for beta in [0.0100, 0.0500, 0.1000, 0.1928, 0.2222, 0.3000]:
    bb0 = b0(beta)
    # at b_0, q_cross exceeds Q_res; for all b>=b_0 the gap only widens (q_cross grows exp, Q_res sqrt)
    check(bb0 is not None and 2**(beta*bb0) > const*math.sqrt(bb0), f"window empty for b>=b_0 at beta={beta}")
    check(2**(beta*(bb0*4)) > const*math.sqrt(bb0*4), f"gap widens at 4 b_0, beta={beta}")
    print(f"  {beta:.4f}    2^{{{beta:.3f} b}}            {const:.3f} sqrt(b)            b_0 = {bb0}")
# the delta-crossover (beta=0) is EXACTLY #682's residual line
for al in [alpha_0, 0.4, 2/3]:
    delta_star = al/3 + 1/9          # beta=0
    check(abs(delta_star - (al+1/3)/3) < 1e-12, f"crossover delta*(beta=0) == #682 residual line at alpha={al:.3f}")
print(f"  crossover in delta (beta=0) == #682 residual line delta_res=(alpha+1/3)/3  [Bohr face = box face]")
# NEGATIVE control: emptiness HINGES on Q_res being polynomial. If Q_res were 2^{b/4}
# (exponential), a window WOULD open for beta<1/4.
def window_open_if_Qres_exp(beta, expo, b):
    return 2**(expo*b) > 2**(beta*b)      # 2^{expo b} (fake exp Q_res) exceeds q_cross
check(window_open_if_Qres_exp(0.10, 0.25, 100), "NEGATIVE: if Q_res~2^{b/4}, window opens for beta=0.10")
check(not window_open_if_Qres_exp(0.30, 0.25, 100), "control: even fake-exp Q_res~2^{b/4} shut for beta=0.30")
print("  NEGATIVE control: emptiness requires Q_res polynomial -- a hypothetical exp Q_res~2^{b/4} would open it for beta<1/4")

print("="*74)
print("BLOCK 5 -- the TENSION: high fiber concentrates Fourier mass at small denominators")
print("="*74)
tension_blocks = [
    ("interval14", list(range(14))),
    ("champ18",    CHAMP18),
    ("holes14",    [0,1,2,3,4,7,8,9,10,11,14,15,16,17]),
]
random.seed(7)
tension_blocks.append(("sidon12", sorted(random.sample(range(0,400),12))))
Nq = 30
prev_mass5 = -1.0
mass_by_f = []
for name, V in tension_blocks:
    f, L = f_and_L(V)
    massle = {1:0.0, 2:0.0, 5:0.0}; tot = 0.0
    for i2 in range(Nq):
        th2 = i2/Nq
        den = Fraction(th2).limit_denominator(Nq).denominator
        s = 0.0
        for i1 in range(Nq):
            for i0 in range(6):
                s += absXhat(V, i0/6, i1/Nq, th2)
        tot += s
        for Dc in massle:
            if den <= Dc: massle[Dc] += s
    frac5 = massle[5]/tot
    mass_by_f.append((f, frac5))
    print(f"  {name:11s} f={f:4d}: mass(den<=1)={massle[1]/tot:.3f} <=2={massle[2]/tot:.3f} <=5={frac5:.3f}")
    check(0 < frac5 < 1, f"{name}: mass fraction in (0,1)")
    check(V[0] >= 0 and rates(V)['X'] < TARGET, f"{name}: X < 2^{{4/3}} (no wall witness)")
# monotone: sort by f, small-denominator mass should be (weakly) increasing with f
ms = sorted(mass_by_f)
sidon_f, sidon_mass = min(mass_by_f)
champ_mass = [m for f_,m in mass_by_f if f_==30][0]
check(champ_mass > sidon_mass, "high-fiber champ has MORE small-denominator mass than Sidon")
check(ms[0][1] < ms[-1][1], "small-denominator mass increases from lowest-f to highest-f block")
print(f"  monotone: lowest-f block mass(den<=5)={ms[0][1]:.3f} < highest-f block mass(den<=5)={ms[-1][1]:.3f}")
# secondary nontrivial peak: high-fiber block's is small (fiber sits at trivial q<=2)
peak_ch = max(best_th0th1(CHAMP18, i/60, 12, 16) for i in range(60)
              if min(abs(i/60), abs(i/60-0.5)) > 0.05)
print(f"  champ18 best NONTRIVIAL secondary peak |Xhat| = {peak_ch:.3f} (fiber carried by trivial q<=2, not a rational a/q)")
check(peak_ch < 0.5, "champ18 secondary (nontrivial-q) peak is small")

print("="*74)
print("BLOCK 6 -- reduction descent (dilation, #685-excluded) & #663 R3 sharpening")
print("="*74)
# a single-class 'tower' with large delta but full reducibility == a dilation
tower = [65536*v for v in range(14)]            # interval dilated: high delta, f of interval
rt = rates(tower); ri = rates(list(range(14)))
check(rt['f']==ri['f'] and rt['L']==ri['L'], "single-AP tower: (f,L)=interval's (it IS a dilation)")
print(f"  single-AP tower delta={rt['delta']:.3f} but (f,L)=({rt['f']},{rt['L']})=interval[0,14) -- a dilation, EXCLUDED by #685")
# multi-class does NOT factor: a two-residue-class block has cross-class collisions
C0 = [3*t for t in range(7)]                    # residue 0 mod 3
C1 = [1+3*t for t in range(7)]                  # residue 1 mod 3
ff0,_ = f_and_L(C0); ff1,_ = f_and_L(C1); ffU,_ = f_and_L(sorted(C0+C1))
check(ffU != ff0*ff1, "two-class block does NOT factor: f(union) != f(C0) f(C1)")
print(f"  two-class union: f(C0)={ff0} f(C1)={ff1} product={ff0*ff1} but f(union)={ffU} -> reduction STALLS at multi-class")
# #663 R3 host recompute: bounded q, host = residue classes over diameter D ~ D
D = 2**20; q = 8
host_len_per_class = D//q
approx_host = host_len_per_class            # ~ D/q, and with O(1) classes ~ D * q^{-1}
delta_host = math.log2(approx_host)/60      # at b=60
check(abs(delta_host - (20 - 3)/60) < 1e-9, "#663 R3 host log-size ~ (log2 D - log2 q)/b (still diameter-scaled)")
print(f"  #663 R3 with q={q}, D=2^20, b=60: host ~ D/q = 2^{{{math.log2(approx_host):.0f}}} -> "
      f"delta_host={delta_host:.3f} ~ delta (bounded q cannot cut the fenced diameter)")

print("="*74)
if FAIL == 0:
    print(f"RESULT: PASS ({PASS}/{PASS})")
    sys.exit(0)
else:
    print(f"RESULT: FAIL ({PASS}/{PASS+FAIL}), {FAIL} failing")
    sys.exit(1)
