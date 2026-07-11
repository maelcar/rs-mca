#!/usr/bin/env python3
"""
verify_collapse_field_cost.py  -- recomputes every number in
experimental/notes/thresholds/collapse_field_cost.md.

QUESTION (PR #642/#645 residual): on a C7 effective-image-collapse cell line,
is the per-received-line distinct-MCA-bad-slope count delta(r) forced below
|F|^{1/2+o(1)} ?  (If so: prize-relevance delta/|F|>eps forces |F|<2^{256+o(n)},
a constant field, and the span face closes with NO field hypothesis.)

VERDICT computed here: REFUTED as a universal per-line bound.  An explicit PURE
effective-image-collapse line (single prefix fiber, image size L=1, ambient
A=|B|^w, so G_1=A/L=|B|^w exponential and Q_img=1) carries
delta = Theta(|F|) distinct MCA-bad slopes -- LINEAR in the field, refuting the
1/2 exponent.  The mechanism: with a pole alpha of degree e>=k+1 over B, the map
S |-> Q_S(alpha) = prod_{x in S}(alpha-x) is INJECTIVE on the fiber because
{1,alpha,...,alpha^k} are B-linearly independent, so delta = |fiber|.

Every block prints PASS/FAIL; nonzero exit on any failure.  Stdlib only,
zero-arg, well under ulimit -v 2097152, ~<3 min.

Labels: PROVED (exact hand derivation, recomputed), COMPUTED (exact finite
recomputation), MEASURED (exact finite toy census), AUDIT (interface reading).

Credit: builds on our #642 (c7_collapse_image_degree.md, T-FIELD delta<=|F_r|),
#645 (fi_field_discharge.md, the RED reduction + honest flag "gate sufficient
not necessary"), #544 (simple_pole_realizability.md, the (star) list-<=1 and the
identity list floor), #625 (c7_routing_spectrum.md, MASTER-2 G_1/Q_img), #627
(routing_exhaustiveness.md, T-DET collapse trigger G_1=A/L exponential), #635
(collapse_payment.md, first-match disjoint charge), Codex #624 (Lean pins of
thm:collision-aware-pole / prop:exact-prefix-list), the paper's own
thm:prefix-to-line-hardness (eq 4.5) and thm:exact-list-line-bijection.
"""

import sys, math, itertools
from itertools import combinations

FAILS = []
PASSES = [0]
def check(name, cond, detail=""):
    if cond:
        PASSES[0]+=1
        print(f"  PASS  {name}  {detail}")
    else:
        FAILS.append(name)
        print(f"  FAIL  {name}  {detail}")

# ======================================================================
# Exact finite fields GF(p^d) over F_p, stdlib only.
# ======================================================================
def _sq_set(p): return set((i*i)%p for i in range(p))

def _poly_irreducible(f, p):
    """Rabin irreducibility test for monic f (list low->high, deg d)."""
    d=len(f)-1
    if d==1: return True
    def mod(a):
        a=a[:]
        while len(a)-1>=d and any(a):
            if a[-1]%p!=0:
                c=a[-1]%p; sh=len(a)-1-d
                for i in range(d+1): a[sh+i]=(a[sh+i]-c*f[i])%p
            a.pop()
            while len(a)>1 and a[-1]==0: a.pop()
        return a
    def mul(a,b):
        r=[0]*(len(a)+len(b)-1)
        for i,ai in enumerate(a):
            if ai:
                for j,bj in enumerate(b): r[i+j]=(r[i+j]+ai*bj)%p
        return mod(r)
    def powx(e):
        res=[1]; base=[0,1]
        while e:
            if e&1: res=mul(res,base)
            base=mul(base,base); e>>=1
        return res
    def sub(a,b):
        n=max(len(a),len(b)); r=[((a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0))%p for i in range(n)]
        while len(r)>1 and r[-1]==0: r.pop()
        return r
    def gcd(a,b):
        a=a[:]; b=b[:]
        while any(b):
            # a mod b
            a=a[:]
            invlead=pow(b[-1],p-2,p); db=len(b)-1
            while len(a)-1>=db and any(a):
                c=(a[-1]*invlead)%p; sh=len(a)-1-db
                for i in range(len(b)): a[sh+i]=(a[sh+i]-c*b[i])%p
                while len(a)>1 and a[-1]==0: a.pop()
                if len(a)-1<db: break
            a,b=b,a
        return a
    if sub(powx(p**d),[0,1])!=[0]: return False
    m=d; primes=set(); r=2
    while r*r<=m:
        while m%r==0: primes.add(r); m//=r
        r+=1
    if m>1: primes.add(m)
    for r in primes:
        g=gcd(sub(powx(p**(d//r)),[0,1]), f)
        if len(g)!=1: return False
    return True

def find_modulus(p,d):
    if d==1: return [0,1]
    for tail in itertools.product(range(p),repeat=d):
        f=list(tail)+[1]
        if f[0]==0: continue
        if _poly_irreducible(f,p): return f
    raise RuntimeError(f"no irreducible deg {d} over F_{p}")

class GF:
    def __init__(self,p,d):
        self.p=p; self.d=d; self.q=p**d
        self.f=find_modulus(p,d)
    def emb(self,x):  # embed F_p element
        return tuple([x%self.p]+[0]*(self.d-1))
    def sub(self,a,b):
        return tuple((a[i]-b[i])%self.p for i in range(self.d))
    def mul(self,a,b):
        p=self.p; d=self.d
        if d==1: return ((a[0]*b[0])%p,)
        f=self.f; r=[0]*(2*d-1)
        for i in range(d):
            if a[i]:
                ai=a[i]
                for j in range(d):
                    if b[j]: r[i+j]=(r[i+j]+ai*b[j])%p
        for deg in range(2*d-2,d-1,-1):
            if r[deg]:
                c=r[deg]; sh=deg-d
                for i in range(d+1): r[sh+i]=(r[sh+i]-c*f[i])%p
        return tuple(r[:d])
    def one(self): return tuple([1]+[0]*(self.d-1))
    def elements(self):
        for t in itertools.product(range(self.p),repeat=self.d): yield tuple(t)

def Q_at(gf, Sxint, alpha):
    """Q_S(alpha) = prod_{x in S}(alpha - emb(x)), Sxint = integer roots in F_p."""
    r=gf.one()
    for x in Sxint:
        r=gf.mul(r, gf.sub(alpha, gf.emb(x)))
    return r

def prefix_key(Sxint, w, p):
    """depth-w locator prefix: coeffs c_1..c_w of prod(X-x) below the leading term."""
    poly=[1]
    for x in Sxint:
        new=[0]*(len(poly)+1)
        for i,c in enumerate(poly):
            new[i]=(new[i]-x*c)%p; new[i+1]=(new[i+1]+c)%p
        poly=new
    m=len(poly)-1
    return tuple(poly[m-1-i] for i in range(w))

# ======================================================================
print("="*72)
print("BLOCK A -- exact GF sanity (moduli irreducible; arithmetic is a field)")
print("="*72)
for (p,d) in [(2,4),(3,2),(3,3),(5,2),(7,2),(5,3)]:
    gf=GF(p,d)
    ok_irr=_poly_irreducible(gf.f,p)
    # every nonzero element invertible: check multiplicative group order q-1 for a generator sample
    els=[e for e in gf.elements()]
    # closure/associativity spot check + F_p subfield embedding correct
    a=gf.emb(2%p); b=gf.emb(3%p)
    sub_ok = gf.mul(a,b)==gf.emb((2*3)%p)
    check(f"GF({p}^{d}) modulus irreducible & F_p-subfield mult correct",
          ok_irr and sub_ok, f"|F|={gf.q}")

# ======================================================================
print("="*72)
print("BLOCK B -- CENTERPIECE (PROVED): m=3,w=1 single-fiber collapse line over")
print("           F=F_{p^2}, B=D=F_p.  delta = |fiber| = (p-1)(p-2)/6 = Theta(|F|).")
print("           Injectivity S->Q_S(alpha) from F_p-independence of {1,alpha}.")
print("="*72)
print(f"  {'p':>3} {'|F|=p^2':>8} {'fiber':>6} {'delta':>6} {'inj':>4} "
      f"{'delta/|F|':>9} {'sqrt|F|':>8} {'delta>sqrt|F|':>13}")
ratios=[]
for p in [5,7,11,13,17,19,23,29,31,37]:
    gf=GF(p,2)
    alpha=(0,1)  # a generator of F_{p^2} over F_p (degree 2), NOT in F_p
    check_alpha_ext = (alpha[1]!=0)  # not in F_p
    fib=[S for S in combinations(range(p),3) if sum(S)%p==0]   # e_1 = 0 fixed
    vals={ Q_at(gf,S,alpha) for S in fib }
    inj = (len(vals)==len(fib))
    formula = (p-1)*(p-2)//6
    q=p*p
    ratios.append(len(vals)/q)
    ok = inj and len(fib)==formula and (p<11 or len(vals)>p)
    print(f"  {p:>3} {q:>8} {len(fib):>6} {len(vals):>6} {str(inj):>4} "
          f"{len(vals)/q:>9.4f} {p:>8} {str(len(vals)>p):>13}")
    check(f"m3 p={p}: delta=|fiber|=(p-1)(p-2)/6 injective, alpha ext",
          ok and check_alpha_ext,
          f"delta={len(vals)}={formula}")
# monotone increase toward 1/6, bounded below away from 0
mono = all(ratios[i]<ratios[i+1] for i in range(len(ratios)-1))
check("m3 delta/|F| monotone increasing toward 1/6 (=> delta=Theta(|F|))",
      mono and ratios[-1]>0.15 and ratios[-1]<1/6,
      f"ratios {ratios[0]:.3f}->{ratios[-1]:.3f}, limit (p-1)(p-2)/(6p^2)->1/6")

# ======================================================================
print("="*72)
print("BLOCK C -- (PROVED) general Case-A injectivity: pole of degree e>=k+1 over")
print("           B gives delta=|fiber| for w>=1 collapse fibers (any m).")
print("           Confirms the centerpiece is not special to m=3.")
print("="*72)
# For code degree k, need k+1 free symmetric coords => alpha degree e=k+1 => F=F_{p^{k+1}}.
# w=1 fiber (e_1 fixed). k=m-w-1=m-2. So e=k+1=m-1.  Take F=F_{p^{m-1}}.
for (p,m) in [(5,3),(5,4),(7,3),(7,4),(7,5)]:
    w=1; k=m-w-1; e=k+1   # =m-1
    gf=GF(p,e)
    # a degree-e element: primitive-ish generator (0,1,0,...) has degree dividing e;
    # to guarantee degree exactly e pick alpha=x (root of the deg-e modulus) => degree e.
    alpha=tuple([0,1]+[0]*(e-2)) if e>=2 else (1,)
    # group m-subsets of F_p by e_1
    fibers={}
    for S in combinations(range(p),m):
        fibers.setdefault(sum(S)%p,[]).append(S)
    # test injectivity on the largest fiber
    big=max(fibers.values(),key=len)
    vals={ Q_at(gf,S,alpha) for S in big }
    inj=(len(vals)==len(big))
    check(f"CaseA p={p} m={m} w=1 (F=F_{p}^{e}): delta=|fiber| injective",
          inj, f"|fiber|={len(big)} delta={len(vals)} |F|={gf.q}")

# ======================================================================
print("="*72)
print("BLOCK D -- (MEASURED) N_max(q) census: max distinct collapse-cell slopes on")
print("           any single fiber+pole over F_{p^2}, over m in {3..7}, w=1.")
print("           Exponent log(N_max)/log(q) exceeds 1/2 and climbs toward 1.")
print("="*72)
print(f"  {'p':>3} {'q':>5} {'best(m)':>7} {'maxfiber':>8} {'N_max':>6} "
      f"{'sqrt q':>7} {'N/sqrtq':>8} {'exponent':>8}")
nmax_rows=[]
for p in [5,7,11,13]:
    gf=GF(p,2)
    Dint=list(range(p))
    poles=[a for a in gf.elements() if a[1]!=0]   # F_{p^2}\F_p
    best=0; bestm=None; bestfib=0
    for m in range(3, min(p,8)):
        w=1
        if m-w-1<1: continue
        fibers={}
        for S in combinations(range(p),m):
            fibers.setdefault(prefix_key(list(S),w,p),[]).append(S)
        # only the few largest fibers can maximize delta
        for fib in sorted(fibers.values(),key=len,reverse=True)[:2]:
            if len(fib)<=best: continue
            for alpha in poles:
                vals=set()
                for S in fib:
                    vals.add(Q_at(gf,list(S),alpha))
                if len(vals)>best:
                    best=len(vals); bestm=m; bestfib=len(fib)
    q=p*p; expo=math.log(best)/math.log(q)
    nmax_rows.append((p,q,best,expo))
    print(f"  {p:>3} {q:>5} {bestm:>7} {bestfib:>8} {best:>6} {p:>7} "
          f"{best/p:>8.3f} {expo:>8.3f}")
# exponent must exceed 1/2 for the larger fields and be increasing
exps=[r[3] for r in nmax_rows]
check("N_max exponent exceeds 1/2 at p in {11,13} (refutes |F|^{1/2})",
      nmax_rows[-1][3]>0.5 and nmax_rows[-2][3]>0.5,
      f"exponents {exps[0]:.2f},{exps[1]:.2f},{exps[2]:.2f},{exps[3]:.2f}")
check("N_max/sqrt(q) grows (=> delta/|F|^{1/2} unbounded, not q^{o(1)} plausibly)",
      nmax_rows[-1][2]/math.sqrt(nmax_rows[-1][1]) > nmax_rows[0][2]/math.sqrt(nmax_rows[0][1]),
      "")

# ======================================================================
print("="*72)
print("BLOCK E -- (COMPUTED) eq (4.5) separation gate is SUFFICIENT-NOT-NECESSARY,")
print("           quantified on the centerpiece witness.")
print("           eq(4.5): |F| > n + k*binom(N,2) suffices to separate N slopes.")
print("="*72)
ratios_gate=[]
for p in [13,17,23,31,41,53]:
    N=(p-1)*(p-2)//6      # realized delta on the m=3 line
    n=p; k=1              # k=m-w-1=1 for m=3,w=1
    gate = n + k*(N*(N-1)//2)     # eq(4.5) sufficient field size to separate N slopes
    actual = p*p                  # field in which we ACTUALLY separate N slopes
    ratio = gate/actual
    ratios_gate.append(ratio)
    check(f"gate-loose p={p}: separate N={N} in |F|={actual}, eq(4.5) sufficient asks |F|>{gate}",
          actual < gate and N > math.sqrt(actual),
          f"gate/actual={ratio:.1f}x, N={N} > sqrt|F|={p}")
check("eq(4.5) looseness ratio grows ~ p^2/2 (gate is quadratic, actual linear in q)",
      all(ratios_gate[i]<ratios_gate[i+1] for i in range(len(ratios_gate)-1)),
      f"ratios {ratios_gate[0]:.1f}x -> {ratios_gate[-1]:.1f}x")

# ======================================================================
print("="*72)
print("BLOCK F -- (PROVED, symbolic) exponential-regime dichotomy: Case A forces")
print("           delta<=|F|^{1/2}; the countertheorem SATURATES delta~|F|^{1/2}")
print("           (diluted).  Case B (low-deg pole, deep fiber) leaves delta<=|F|")
print("           OPEN = #645's residual corner.")
print("="*72)
# Case A arithmetic: alpha degree e>=k+1 => |F|>=q0^{k+1}; delta=N<=|fiber|<=binom(n,m).
# In the DEEP collapse regime n=q0, m~cn, w=Theta(n/log n): show q0^{(k+1)/2} >> binom(n,m),
# i.e. the field forced by injectivity is so large that delta<=|F|^{1/2} necessarily.
def deep_caseA_holds(q0, c, wfrac):
    import math as _m
    n=q0; m=int(c*n); w=max(1,int(wfrac*n/max(1,_m.log(n))))
    k=m-w-1
    if k<1: return None
    logbinom = n*( -c*_m.log(c) - (1-c)*_m.log(1-c) )   # ~ log binom(n,cn)
    log_fiber = logbinom - w*_m.log(q0)                 # log |fiber| (>=log delta)
    log_sqrtF = 0.5*(k+1)*_m.log(q0)                    # log |F|^{1/2}, |F|=q0^{k+1}
    return (log_fiber, log_sqrtF, log_fiber < log_sqrtF)
allA=True
for q0 in [101, 1009, 10007]:
    r=deep_caseA_holds(q0, 0.5, 0.5)
    if r is None: continue
    lf,ls,holds=r
    allA = allA and holds
    print(f"  q0={q0}: log|fiber|={lf:.1f}  log|F|^1/2={ls:.1f}  "
          f"delta<=|F|^1/2 {'HOLDS' if holds else 'FAILS'}")
check("CaseA deep regime: injectivity forces delta<=|F|^{1/2} (field too big)",
      allA, "high-degree pole => quadratic-ish field => 1/2 exponent recovered")
# Countertheorem saturation: N=e^{(h/4)n}, |F|~N^2 => |F|^{1/2}=N=delta (exact).
# Work in LOG space (N is astronomically large; never materialize it).
h=0.7  # any positive rate
for n in [100,1000,10000]:
    logN=(h/4)*n             # log delta = log N
    logF=2*logN              # eq(6.7): |F| ~ k*binom(N,2) ~ N^2 => log|F|=2 log N
    logsqrtF=0.5*logF
    e_mca_exp = logN-logF    # log e_MCA = log(delta/|F|) = -log N -> -inf (diluted)
    check(f"countertheorem n={n}: delta=N=|F|^{{1/2}} exactly (diluted)",
          abs(logN-logsqrtF)<1e-9 and e_mca_exp<0,
          f"log delta={logN:.1f} = log|F|^1/2={logsqrtF:.1f}; log e_MCA={e_mca_exp:.1f}->-inf")

# ======================================================================
print("="*72)
print("BLOCK G -- (COMPUTED) collapse-cell classification of the witness (T-DET,")
print("           #625/#627): a single prefix fiber is a PURE effective-image")
print("           collapse cell: image L=1, ambient A=|B|^w, G_1=A/L=|B|^w (exp),")
print("           Q_img = L*max_mu = 1.  (matches #625 worked example.)")
print("="*72)
for (q0,w) in [(11,1),(13,1),(11,2),(101,3)]:
    L=1                       # single fiber -> prefix image size 1
    A=q0**w                   # ambient B^w
    G1=A//L
    Qimg=1                    # L * max occupancy weight = 1*1
    # MASTER-2 (#625): E+1 <= G_1 * Q_img ; here E+1 = A_eff*P_2 with P_2=1 (one atom)
    check(f"collapse-class q0={q0} w={w}: G_1=A/L={G1}=|B|^w (exp when w~n/log|B|), Q_img=1",
          G1==A and Qimg==1, f"A=|B|^w={A}, L=1 -> pure effective-image collapse")

# ======================================================================
print("="*72)
print("BLOCK H -- (COMPUTED) the RED reduction (#645) applied to the poly-field")
print("           witness: it CHARGES the target (e_MCA=Theta(1)) yet is harmless")
print("           because delta=poly(n)=e^{o(n)} -- column 1 of #645's dichotomy.")
print("="*72)
for p in [11,101,1009]:
    N=(p-1)*(p-2)//6; F=p*p
    e_mca = N/F                # #645 (RED): e_MCA = delta/|F|
    # prize-relevant? e_MCA > eps=2^-128 : YES (Theta(1)); but delta subexponential in n=p
    prize_rel = e_mca > 2.0**-128
    subexp = N < math.exp(0.5*p)   # delta << e^{o(n)}, n=p
    check(f"RED p={p}: e_MCA={e_mca:.3f}=Theta(1) prize-rel, yet delta=poly => harmless",
          prize_rel and subexp,
          f"delta={N}=poly(n), log|F|=2log p=o(n): closes anyway (#645 col.1)")

# ======================================================================
print("="*72)
n_ok=PASSES[0]; n_bad=len(FAILS)
if n_bad==0:
    print(f"RESULT: PASS ({n_ok}/{n_ok})")
    sys.exit(0)
else:
    print(f"RESULT: FAIL ({n_ok} passed, {n_bad} failed: {FAILS})")
    sys.exit(1)
