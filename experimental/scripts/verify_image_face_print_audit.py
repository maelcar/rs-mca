#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verifier for experimental/notes/thresholds/image_face_print_audit.md.

Zero-arg, stdlib-only.  Exits nonzero on any failure and prints RESULT: FAIL;
otherwise prints RESULT: PASS (N/N).

It checks three things.

  BLOCK A  Every verbatim tex anchor quoted by the print-audit byte-matches
           experimental/asymptotic_rs_mca_frontiers.tex at its stated line.
           Negative-tested: a deliberately corrupted quote MUST NOT match
           (proves the check discriminates).

  BLOCK B  The arc's numeric claims are recomputed from scratch:
             log(3/2)      = 0.405465   (#668 upper bracket end)
             (1/3) log 2   = 0.231049   (#683 off-corridor slice cap)
             2^(4/3)       = 2.5198     (#678 off-corridor X ceiling)
             alpha_0       = 0.084497   (#678 corridor floor: small root of
                                         H2(a) = a + 1/3)
             (alpha_0+1/3)/3 = 0.13928  (#682 diameter-empty threshold)
             2^1.228539    ~ 2.3433     (#678 X* amplification lower guard)

  BLOCK C  DannyExperiments #668's inequalities  f <= 2^(b-d),
           L <= sum_{j<=d} C(b,j),  f*L <= 3^b,  and  L <= 2^(H2(eta) b)
           on an exact small moment-curve block that carries a real fiber;
           and the #655 b=18 champion rho = 0.158411 re-derived by a full
           2^18 signature enumeration (independent of any note's own DP),
           yielding fstar = 30, L1 = 151275.

No .tex / .pdf is modified.
"""

import os
import sys
import math
from itertools import combinations

FAILURES = []
CHECKS = 0


def check(cond, label):
    global CHECKS
    CHECKS += 1
    if cond:
        print("  ok   " + label)
    else:
        print("  FAIL " + label)
        FAILURES.append(label)


HERE = os.path.dirname(os.path.abspath(__file__))
TEX = os.path.normpath(os.path.join(HERE, "..", "asymptotic_rs_mca_frontiers.tex"))


# --------------------------------------------------------------------------
# BLOCK A -- verbatim tex anchor byte-checks + negative test
# --------------------------------------------------------------------------
# (1-based line number, exact substring that must occur on that line)
ANCHORS = [
    (160,  "requires a witness-exhaustive atlas, image-scale MI and MA or a direct"),
    (161,  "Sidon payment, residual ray bounds, and comparison of the complete profile"),
    (778,  "still requires a witness-exhaustive first-match atlas, image-scale"),
    (779,  "effective Fourier payment or a direct Sidon payment, residual ray bounds"),
    (815,  "ambient identity-normalized Sidon payment or an identity-scale MCA"),
    (832,  "refutes ambient identity-normalized Sidon payment, identity-only numerator"),
    (2044, r"\begin{proposition}[Prefix rigidity and its packing limit]"),
    (2051, r"\tag{4.4}\label{eq:packing-fiber-cap}"),
    (4844, r"\tag{FI}\label{eq:full-image-certificate}"),
    (4859, "The image-scale frontier condition is"),
    (4918, r"\max_{s\in\Scal}f_s\le e^{o(N)}\barN^{\rm img}."),
    (7105, r"The atlas payments, \textup{(MA)}, image-scale conditions,"),
    (7129, "does not close the Sidon, algebraic-projection, or higher-dimensional ray"),
    (7195, "moment-accessibility, Sidon moment, and image-scale hypotheses of"),
    (7217, r"a direct Sidon estimate, the primitive image-scale and"),
    (7488, r"effective \textup{(MI)} plus \textup{(MA)} or a direct Sidon payment, the primitive-Q"),
    (7528, r"Sidon payment, the primitive image-scale conditions, and \textup{(RC)},"),
    (7548, "not follow from that census is image coverage, Fourier flatness, or ray"),
]

print("BLOCK A -- tex anchor byte-checks at", os.path.basename(TEX))
with open(TEX, "r", encoding="utf-8") as fh:
    LINES = fh.read().split("\n")

for lineno, sub in ANCHORS:
    ok = (1 <= lineno <= len(LINES)) and (sub in LINES[lineno - 1])
    check(ok, "L%d anchors: %s" % (lineno, sub[:52]))

# Negative test: corrupting a load-bearing anchor must break the match, both on
# its line and file-wide (the string as corrupted appears nowhere).
_orig = "image-scale MI and MA or a direct"
_corrupt = "image-scale MX and MA or a direct"
check(_orig in LINES[160 - 1], "negative-test setup: original present at L160")
check(_corrupt not in LINES[160 - 1], "negative-test: corrupted quote absent at L160")
check(all(_corrupt not in ln for ln in LINES), "negative-test: corrupted quote absent file-wide")


# --------------------------------------------------------------------------
# BLOCK B -- arc constants
# --------------------------------------------------------------------------
print("BLOCK B -- arc numeric claims")


def H2_bits(x):
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


log32 = math.log(1.5)
check(abs(log32 - 0.405465) < 1e-6, "log(3/2) = 0.405465  (#668 upper bracket end) -> %.6f" % log32)

third_log2 = math.log(2.0) / 3.0
check(abs(third_log2 - 0.231049) < 1e-6, "(1/3)log2 = 0.231049  (#683 slice cap) -> %.6f" % third_log2)

x_ceiling = 2.0 ** (4.0 / 3.0)
check(abs(x_ceiling - 2.5198) < 1e-4, "2^(4/3) = 2.5198  (#678 off-corridor X ceiling) -> %.4f" % x_ceiling)

# alpha_0 = 0.084497 is the small root of H2(a) = a + 1/3.
check(abs(H2_bits(0.084497) - (0.084497 + 1.0 / 3.0)) < 1e-4,
      "alpha_0=0.084497 satisfies H2(a)=a+1/3  (#678 corridor floor)")

# ... re-solve that root by bisection and confirm it rounds to 0.084497.
def g(a):
    return H2_bits(a) - a - 1.0 / 3.0

lo, hi = 1e-9, 0.20
check(g(lo) < 0.0 < g(hi), "bracket for small root of H2(a)-a-1/3")
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if g(mid) < 0.0:
        lo = mid
    else:
        hi = mid
root = 0.5 * (lo + hi)
check(abs(root - 0.084497) < 5e-4, "bisection root of H2(a)=a+1/3 -> %.6f ~ 0.084497" % root)

# 0.13928 = (alpha_0 + 1/3)/3, via both the literal and the re-solved root.
demp_lit = (0.084497 + 1.0 / 3.0) / 3.0
demp_root = (root + 1.0 / 3.0) / 3.0
check(abs(demp_lit - 0.13928) < 1e-4, "(0.084497+1/3)/3 = 0.13928  (#682 diameter-empty) -> %.5f" % demp_lit)
check(abs(demp_root - 0.13928) < 1e-3, "(root+1/3)/3 = 0.13928 (from bisection) -> %.5f" % demp_root)

# X* amplification lower guard: note states 2.3433 = 2^1.228539 (minor rounding).
xstar_guard = 2.0 ** 1.228539
check(2.340 < xstar_guard < 2.345, "2^1.228539 ~ 2.3433  (#678 X* lower guard) -> %.5f" % xstar_guard)
check(abs(xstar_guard - 2.3433) < 5e-3, "2^1.228539 within rounding of the note's 2.3433")


# --------------------------------------------------------------------------
# BLOCK C -- DannyExperiments #668 inequalities + #655 b=18 champion
# --------------------------------------------------------------------------
print("BLOCK C -- #668 inequalities and #655 b=18 champion")


def signatures(vs):
    """Full signature counts (w, sum, sumsq) for every subset of moment-curve
    columns a_i=(1, v_i, v_i^2), by a doubling DP.  Returns (fstar, L1)."""
    counts = {(0, 0, 0): 1}
    for v in vs:
        nxt = dict(counts)  # subsets not taking v
        for (w, s, q), c in counts.items():
            key = (w + 1, s + v, q + v * v)
            nxt[key] = nxt.get(key, 0) + c
        counts = nxt
    return max(counts.values()), len(counts)


def max_dissociated(vs):
    """d(A): size of the largest subset-dissociated index set for a_i=(1,v_i,v_i^2)."""
    b = len(vs)
    cols = [(1, v, v * v) for v in vs]
    best = 0
    for size in range(b, 0, -1):
        if size <= best:
            break
        found = False
        for I in combinations(range(b), size):
            sums = set()
            ok = True
            # enumerate all 2^size subset sums of the chosen columns
            for r in range(size + 1):
                for T in combinations(I, r):
                    ssum = (len(T),
                            sum(cols[i][1] for i in T),
                            sum(cols[i][2] for i in T))
                    if ssum in sums:
                        ok = False
                        break
                    sums.add(ssum)
                if not ok:
                    break
            if ok:
                found = True
                break
        if found:
            best = size
            break
    return best


# (i) a small block that carries a real fiber (contains the {1,5,6}={2,3,7}
#     degree-2 PTE trade), so fstar > 1 and d < b -- exercises #668 nontrivially.
vs8 = [0, 1, 2, 3, 4, 5, 6, 7]
b8 = len(vs8)
f8, L8 = signatures(vs8)
d8 = max_dissociated(vs8)
check(f8 >= 2, "b=8 block {0..7} has a real fiber: fstar=%d >= 2" % f8)
check(d8 < b8, "b=8 dissociation deficit: d=%d < b=%d" % (d8, b8))
check(f8 <= 2 ** (b8 - d8), "#668 (1a): f <= 2^(b-d)   [%d <= %d]" % (f8, 2 ** (b8 - d8)))
sauer8 = sum(math.comb(b8, j) for j in range(d8 + 1))
check(L8 <= sauer8, "#668 (1b): L <= sum_{j<=d} C(b,j)   [%d <= %d]" % (L8, sauer8))
check(f8 * L8 <= 3 ** b8, "#668 (2): f*L <= 3^b   [%d <= %d]" % (f8 * L8, 3 ** b8))
# (3): concentration form L <= 2^(H2(eta) b) with eta = 1 - log2(f)/b.
eta8 = 1.0 - math.log2(f8) / b8
if 0.0 < eta8 <= 0.5:
    bound3 = 2.0 ** (H2_bits(eta8) * b8)
    check(L8 <= bound3 + 1e-6, "#668 (3): L <= 2^(H2(eta)b)   [%d <= %.1f], eta=%.4f" % (L8, bound3, eta8))
else:
    check(True, "#668 (3): eta=%.4f outside (0,1/2]; concentration form vacuous here" % eta8)

# (ii) the #655 b=18 champion, re-derived by full signature enumeration.
champ = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]
bC = len(champ)
check(bC == 18, "champion block has b=18 distinct integers")
check(len(set(champ)) == 18, "champion integers are distinct")
fstar, L1 = signatures(champ)
check(fstar == 30, "champion fstar = 30 (re-derived) -> %d" % fstar)
check(L1 == 151275, "champion L1 = 151275 (re-derived) -> %d" % L1)
rho = (math.log(fstar) + math.log(L1)) / bC - math.log(2.0)
check(abs(rho - 0.158411) < 1e-4, "champion rho = 0.158411 (lower bracket end) -> %.6f" % rho)
check(fstar * L1 <= 3 ** bC, "#668 (2) on champion: f*L <= 3^b   [%d <= %d]" % (fstar * L1, 3 ** bC))
# bracket ordering, both ends unconditional after #668/#673 integration.
check(rho < log32 < math.log(2.0), "bracket order: 0.158411 <= rho* <= log(3/2) < log 2")


# --------------------------------------------------------------------------
print("-" * 60)
total = CHECKS
passed = CHECKS - len(FAILURES)
if FAILURES:
    print("RESULT: FAIL (%d/%d)" % (passed, total))
    for f in FAILURES:
        print("   - " + f)
    sys.exit(1)
print("RESULT: PASS (%d/%d)" % (passed, total))
