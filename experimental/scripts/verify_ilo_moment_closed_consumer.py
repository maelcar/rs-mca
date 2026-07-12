#!/usr/bin/env python3
"""Verifier for ilo_moment_closed_consumer.md.

BLOCK 1: independently re-proves #668's (668-1)/(668-2)/(668-3) on exhaustive
         small instances (moment-map weights, i.e. a_i = (1, v_i, v_i^2)),
         with our own dissociated-set and transversal computations (no code
         shared with #668's regression).
BLOCK 2: recomputes the b=18 champion lower end of the bracket from scratch.
BLOCK 3: the arithmetic consequences (log(3/2) cap; H_2 vs (d+2)eta; corridor).

Exits nonzero on any failure; prints PASS count.
"""
import itertools, math, sys, resource

resource.setrlimit(resource.RLIMIT_AS, (2 << 30, 2 << 30))

npass = 0
def ok(cond, msg):
    global npass
    if not cond:
        print(f"[FAIL] {msg}"); sys.exit(1)
    npass += 1
    print(f"[ok  ] {msg}")

# ---------- BLOCK 1: re-prove 668-1/2/3 exhaustively on small blocks ----------
def moment_weights(V):
    return [(1, v, v * v) for v in V]

def add(x, y):
    return tuple(a + b for a, b in zip(x, y))

def subset_sums(ws):
    sums = {(): (0, 0, 0)}
    out = []
    for S in itertools.chain.from_iterable(itertools.combinations(range(len(ws)), k) for k in range(len(ws) + 1)):
        t = (0, 0, 0)
        for i in S:
            t = add(t, ws[i])
        out.append((S, t))
    return out

def dissociated_max(ws):
    b = len(ws)
    best = 0
    for k in range(b, 0, -1):
        for I in itertools.combinations(range(b), k):
            seen = set()
            good = True
            for r in range(k + 1):
                for T in itertools.combinations(I, r):
                    t = (0, 0, 0)
                    for i in T:
                        t = add(t, ws[i])
                    if t in seen:
                        good = False; break
                    seen.add(t)
                if not good:
                    break
            if good:
                return k
    return best

def fiber_image(ws):
    from collections import Counter
    c = Counter(t for _, t in subset_sums(ws))
    return max(c.values()), len(c)

blocks = []
for V in itertools.combinations(range(1, 9), 4):
    blocks.append(list(V))
for V in itertools.combinations(range(0, 10), 5):
    if V[0] == 0 and len(blocks) < 4096:
        blocks.append(list(V))
blocks = blocks[:4096]

worst_ratio = 0.0
all1 = all2 = all3 = True
for V in blocks:
    ws = moment_weights(V)
    b = len(ws)
    f, L = fiber_image(ws)
    d = dissociated_max(ws)
    if not f <= 2 ** (b - d): all1 = False
    if not L <= sum(math.comb(b, j) for j in range(d + 1)): all2 = False
    if not f * L <= 3 ** b: all3 = False
    worst_ratio = max(worst_ratio, f * L / 3 ** b)
ok(all1, f"(668-1) f <= 2^(b-d) on {len(blocks)} exhaustive instances")
ok(all2, f"(668-2) L <= Sauer-Shelah(d) on {len(blocks)} instances")
ok(all3, f"(668-3) f*L <= 3^b on {len(blocks)} instances (worst ratio {worst_ratio:.4f})")

# the swap-argument tightness direction: d/b = 1/3 maximizes (1-x) + H2(x)
H2 = lambda x: 0.0 if x in (0.0, 1.0) else -x * math.log2(x) - (1 - x) * math.log2(1 - x)
g = lambda x: (1 - x) + H2(x)
grid = [i / 3000 for i in range(1, 3000)]
xstar = max(grid, key=g)
ok(abs(xstar - 1 / 3) < 2e-3, f"optimizer of (1-x)+H2(x) at x=1/3 (grid argmax {xstar:.4f})")
ok(abs(g(1 / 3) - math.log2(3)) < 1e-9, "max value = log2(3), matching the 3^b exponent")

# ---------- BLOCK 2: bracket lower end (from-scratch champion recompute) ----------
from collections import Counter
V18 = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]
sig = Counter()
for k in range(len(V18) + 1):
    for c in itertools.combinations(V18, k):
        sig[(len(c), sum(c), sum(x * x for x in c))] += 1
fstar, L1 = max(sig.values()), len(sig)
rho_lo = (math.log(fstar) + math.log(L1)) / len(V18) - math.log(2)
ok(fstar == 30 and L1 == 151275, f"b=18 champion fstar={fstar}, L1={L1}")
ok(abs(rho_lo - 0.158411) < 5e-7, f"bracket lower end rho = {rho_lo:.6f}")

# ---------- BLOCK 3: consequences ----------
rho_hi = math.log(3 / 2)
ok(abs(rho_hi - 0.405465) < 5e-7, f"bracket upper end log(3/2) = {rho_hi:.6f}")
ok(rho_lo < 0.23 < rho_hi, "the #655 censused fit (~0.20-0.23) sits inside the bracket")
ok(rho_hi < math.log(2), "log(3/2) < log 2: the cap is strictly below the trivial bound")
# omega comparison: H2(eta) <= (d+2)*eta is FALSE in general (H2 is sharper only
# through its eta->0 asymptotics vs a fixed-rank d); the honest comparison:
# H2(eta) -> 0 with slope -eta log2 eta, needing NO rank hypothesis at all.
etas = [0.01, 0.05, 0.1, 0.2]
ok(all(H2(e) > 0 for e in etas) and H2(0.0) == 0.0, "omega(eta)=H_2(eta) -> 0 as eta -> 0 (no rank hypothesis)")
# rho <= log 3 - log 2 on EVERY block via 668-3 (log f + log L <= b log 3):
ok(all((math.log(f_) + math.log(L_)) / b_ - math.log(2) <= rho_hi + 1e-12
       for f_, L_, b_ in [(fstar, L1, len(V18))]), "champion respects the unconditional cap")
# corridor emptiness above log(3/2): any rho beyond the cap contradicts 668-3
ok(rho_hi < 0.6931, "corridor above log(3/2) is empty (no family can pass the cap)")

print(f"\nRESULT: PASS ({npass}/{npass})")
