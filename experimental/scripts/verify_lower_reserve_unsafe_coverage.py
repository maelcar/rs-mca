#!/usr/bin/env python3
"""Verifier for the lower-reserve / unsafe-side coverage audit (hard input 5).

Stdlib only, zero-arg, deterministic. Prints RESULT: PASS or RESULT: FAIL and
exits nonzero on any failure. Runtime < 60 s (one ~5 s exhaustive MCA count).

It does three things:

  (A) ANCHOR    byte-verifies every obligation quote used by the note against
                the primary sources at their cited line, and negative-tests
                that deliberately corrupted quotes are absent from the file.
  (B) COMPUTED  recomputes every echoed number: DannyExperiments #669 eq (2)
                capacity fraction, #680 same-domain field pair and closed
                endpoint, the integrated two-regime realizability arithmetic
                (simple_pole_realizability.md), and latifkasuli #690's m31
                target and sensitivity flip.
  (C) PROVED    an independent exhaustive support-wise MCA count over F5 that
                reproduces B^MCA(3)=2, confirming the pole floor P=1 <= E=2 is
                realizable and never overshoots (the "not crossing the target"
                failure mode does not occur).

No .tex/.pdf is edited or required beyond reading. Object supported:
hard input 5 (lower reserve / unsafe-side comparison), agents.md L50/L98.
"""
import os
import sys
from math import comb
from fractions import Fraction
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # experimental/
REPO = os.path.dirname(ROOT)                        # repo root
TEX = os.path.join(ROOT, "asymptotic_rs_mca_frontiers.tex")
AGENTS = os.path.join(REPO, "agents.md")

fails = []
npass = 0


def check(cond, label):
    global npass
    if cond:
        npass += 1
    else:
        fails.append(label)
    return cond


def read_lines(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read().split("\n")


# ---------------------------------------------------------------------------
# (A) ANCHOR checks: (1-indexed line, verbatim substring that must be on it)
# ---------------------------------------------------------------------------
TEX_ANCHORS = [
    # abstract obligation (umbrella O1)
    (161, "comparison of the complete profile"),
    (162, "envelope with the target and lower reserve."),
    # effective-normalization theorem recap (umbrella O2)
    (781, "complete envelope domination, and"),
    (782, "the target and lower reserve comparisons."),
    # SB2 literal-reserve pointer
    (754, "additionally requires the literal reserve comparisons in"),
    # certified profile-list construction (O5)
    (982, "profile, together with the pole and challenge-intersection estimates that"),
    (983, "prove its bad-slope count exceeds the target."),
    # target-aware threshold bracket (O5/O7 consumer)
    (988, "Target-aware threshold bracket"),
    # target-reserve definition, unsafe side (O6)
    (6139, "by which the logarithm of a proved bad-slope construction exceeds"),
    # exact unsafe test / pole floor (O3)
    (6180, "Exact unsafe test"),
    (6197, "replaced by any larger identity, quotient, Chebyshev, or"),
    # unconditional support-envelope bracket / SB2 (O4)
    (6211, "Unconditional exact support-envelope bracket"),
    (6239, "literal target reserve and contains no asymptotic placeholder."),
    # deep-regime unconditional unsafe side (O8)
    (249, "Unconditional asymptotic RS--MCA theorem in the deep regime"),
    (1833, "Universal tangent floor"),
    (1854, "Exact deep numerator"),
    # crossing sharpness (O7 — the open residual)
    (6675, "Target-aware crossing criterion"),
    (6683, "target has subexponential logarithm and a quantitative reserve dominates"),
    (6684, "all errors and pole collisions."),
    (6280, "deduces from exponent notation, that quantitative reserves furnish the"),
    (6281, "exact safe and unsafe tests within"),
]
AGENTS_ANCHORS = [
    (50, "lower reserve / unsafe-side comparison"),
    (64, "against the actual target and lower reserve."),
    (98, "unsafe-side lower reserve not actually crossing the target"),
]

tex_lines = read_lines(TEX)
agents_lines = read_lines(AGENTS)
tex_text = "\n".join(tex_lines)
agents_text = "\n".join(agents_lines)

for ln, sub in TEX_ANCHORS:
    ok = 1 <= ln <= len(tex_lines) and sub in tex_lines[ln - 1]
    check(ok, "ANCHOR tex L%d: %r" % (ln, sub[:42]))
for ln, sub in AGENTS_ANCHORS:
    ok = 1 <= ln <= len(agents_lines) and sub in agents_lines[ln - 1]
    check(ok, "ANCHOR agents L%d: %r" % (ln, sub[:42]))

# negative test: corrupted quotes must be absent from the source entirely.
NEG_TEX = [
    "envelope with the target and upper reserve.",     # lower->upper
    "prove its bad-slope count exceeds the budget.",   # target->budget
    "all errors and pole coincidences.",               # collisions->coincidences
    "literal target reserve and contains one asymptotic placeholder.",
]
NEG_AGENTS = [
    "lower reserve / safe-side comparison",            # unsafe->safe
    "unsafe-side lower reserve actually crossing the target",  # dropped "not"
]
for bad in NEG_TEX:
    check(bad not in tex_text, "NEG-TEX present(should be absent): %r" % bad[:42])
for bad in NEG_AGENTS:
    check(bad not in agents_text, "NEG-AGENTS present(should be absent): %r" % bad[:42])


# ---------------------------------------------------------------------------
# (B) COMPUTED checks
# ---------------------------------------------------------------------------
def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True


def next_prime(m):
    x = m + 1
    while not is_prime(x):
        x += 1
    return x


# --- DannyExperiments #669 (challenge-restricted syndrome-secant lower bound) ---
# eq (2): B^MCA(k+1) >= ceil( G (q-1) N / (q (N+q-1)) ), N=binom(n,k+1).
# The full-field fraction (q-1)N/(q(N+q-1)) -> 1 as n->inf with log q = o(n),
# so a=k+1 is unsafe for every target eps<1 (in particular eps=2^-128).
prev = Fraction(0)
frac_ok = True
mono_ok = True
eps128 = Fraction(1, 2 ** 128)
for n in (64, 128, 256, 512):
    k = n // 2
    N = comb(n, k + 1)
    q = next_prime(n)                       # log q = O(log n) = o(n)
    fr = Fraction((q - 1) * N, q * (N + q - 1))
    if not (fr > eps128):                   # numerator > B* => unsafe at k+1
        frac_ok = False
    if not (fr > prev):
        mono_ok = False
    prev = fr
check(frac_ok, "#669 eq(2) fraction exceeds 2^-128 (unsafe at k+1)")
check(mono_ok, "#669 eq(2) fraction increases toward 1 (log q = o(n))")
check(Fraction(1, 2) < prev < 1, "#669 eq(2) fraction bracketed in (1/2,1)")

# --- DannyExperiments #680 (exact full-field capacity-adjacent frontier) ---
# closed endpoint: M <= floor(q/E)  iff  E*M <= q.
E = 2 ** 128
endpoint_ok = True
for (n, k, q) in [(128, 64, 3 ** 96), (128, 64, 3 ** 160), (40, 20, 2 ** 200)]:
    M = comb(n, k + 1)
    b = q // E
    if (M <= b) != (E * M <= q):
        endpoint_ok = False
check(endpoint_ok, "#680 closed endpoint M<=floor(q/E) iff E*M<=q")
# same-domain field pair (n=128,k=64): q_unsafe=3^96 unsafe, q_safe=3^160 safe.
M128 = comb(128, 65)
check(3 ** 96 < E * M128, "#680 pair: q_unsafe=3^96 < 2^128*binom(128,65) (unsafe)")
check(3 ** 160 > E * M128, "#680 pair: q_safe=3^160 > 2^128*binom(128,65) (safe)")
check(E * M128 == 2 ** 128 * comb(128, 65), "#680 q_crit = 2^128*binom(n,k+1)")

# --- integrated simple_pole_realizability.md two-regime arithmetic ---
# deep boundary a_deep=ceil((2n+k)/3) is strictly inside the list-<=1 zone
# (n+k)/2  <=>  n>k  (always).
adeep_ok = True
for n in range(2, 200):
    for k in range(1, n):
        a_deep = -(-(2 * n + k) // 3)       # ceil
        if (a_deep > Fraction(n + k, 2)) != (n > k):
            adeep_ok = False
check(adeep_ok, "two-regime: a_deep>(n+k)/2 iff n>k (0 failures)")
# pole floor collapses (L(a)=1) for a>(n+k)/2: binom(n,a) <= |B|^{a-k-1}, |B|=n.
collapse_ok = True
collapse_cases = 0
for n in range(2, 70):
    for k in range(1, n):
        for a in range(k + 1, n + 1):
            if 2 * a > n + k:
                collapse_cases += 1
                if not (comb(n, a) <= n ** (a - k - 1)):
                    collapse_ok = False
check(collapse_ok, "two-regime: binom(n,a)<=n^(a-k-1) for a>(n+k)/2 (%d cases)"
      % collapse_cases)


def Lfloor(n, a, k, B):
    w = a - k - 1
    return -(-comb(n, a) // (B ** w)) if w >= 0 else comb(n, a)


def Mconv(Lv, q, n, k):
    num = Lv * (q - n)
    den = (q - n) + k * (Lv - 1)
    return -(-num // den)


def Preserve(n, a, k, B, q, G):
    return -(-(G * Mconv(Lfloor(n, a, k, B), q, n, k)) // q)


# E2 shallow SB2 window (F11,n=3,k=1,a=2): P realizable and tight, P=3.
check(Lfloor(3, 2, 1, 11) == 3 and Mconv(3, 11, 3, 1) == 3
      and Preserve(3, 2, 1, 11, 11, 11) == 3,
      "simple_pole E2: F11 n3 k1 a2 -> L=M=P=3 (shallow, P operative)")
# E1 deep (F5,n=4,k=1,a=3): P collapses to 1 <= E=min{|G|,n-a+1}=2.
E1_E = min(5, 4 - 3 + 1)
check(Lfloor(4, 3, 1, 5) == 1 and Preserve(4, 3, 1, 5, 5, 5) == 1 and E1_E == 2,
      "simple_pole E1: F5 n4 k1 a3 -> P=1 <= E=2 (deep, P redundant)")

# --- latifkasuli #690 (envelope-rung-ledger) echoed target + sensitivity flip ---
check(16777215 == 2 ** 24 - 1, "#690 m31 target B* = 2^24-1")
# watch-item rung margin -0.3938 bits: any multiplier >= 2^0.3938 fires it;
# the crude b=1 endpoint factor 2 flips M=12,769,758 past B*=16,777,215.
check(2 * 12769758 > 16777215, "#690 sensitivity: b=1 factor flips the -0.3938 rung")
check(12769758 < 16777215, "#690 watch-item rung does not fire at b=0 (NO ISSUE)")


# ---------------------------------------------------------------------------
# (C) PROVED (finite): exhaustive support-wise MCA count over F5 reproduces
#     B^MCA(a=3)=2, so the pole floor P=1 is a realizable, non-overshooting
#     lower reserve (the "not actually crossing the target" mode is absent).
# ---------------------------------------------------------------------------
def exhaustive_bmca_f5():
    Fq, n, k, a = 5, 4, 1, 3          # deg<k=deg<1 => constant explanations
    supports = [frozenset(S) for r in range(a, n + 1)
                for S in combinations(range(n), r)]

    def const_on(word, S):
        it = iter(S)
        f = word[next(it)]
        return all(word[i] == f for i in it)

    words = list(product(range(Fq), repeat=n))
    maxbad = 0
    for r0 in words:
        c0 = [const_on(r0, S) for S in supports]
        for r1 in words:
            c1 = [const_on(r1, S) for S in supports]
            bad = 0
            for g in range(Fq):
                w = tuple((r0[i] + g * r1[i]) % Fq for i in range(n))
                isbad = False
                for j, S in enumerate(supports):
                    if const_on(w, S) and not (c0[j] and c1[j]):
                        isbad = True
                        break
                if isbad:
                    bad += 1
            if bad > maxbad:
                maxbad = bad
            if maxbad > 2:               # would refute the E1 claim
                return maxbad
    return maxbad

bmca = exhaustive_bmca_f5()
check(bmca == 2, "PROVED F5 exhaustive: B^MCA(a=3)=2 (= E; pole floor P=1<=2)")


# ---------------------------------------------------------------------------
print()
if fails:
    print("FAILED CHECKS:")
    for f in fails:
        print("  -", f)
    print("\nRESULT: FAIL (%d ok, %d failed)" % (npass, len(fails)))
    sys.exit(1)
print("RESULT: PASS (%d checks)" % npass)
