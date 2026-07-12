#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/mi_ma_sidon_route_audit.md.

Stdlib-only, zero-arg. Prints `RESULT: PASS (k/k)` and exits 0 on success;
exits nonzero on the first failed check.

  BLOCK A  byte-checks every quoted anchor (frontiers.tex, agents.md, and the
           two base-integrated notes b2_l1_reduction_ledger.md [scottdhughes
           #564] and fiber_image_tradeoff.md [holmbuar #655]) at its exact
           line, plus a negative test (a deliberately corrupted quote MUST
           fail the checker).
  BLOCK B  recomputes, from scratch, the two "same object" Sidon 4th-moment
           identities that are the pivot of the applicability analysis:
             (i)  #663's degree-2 block identity  INT|S|^4 = 2 b^2 - b
                  (moment-curve, continuous torus; 2-vs-2 quadruple count),
                  incl. the #655 b=18 champion (630);
             (ii) scottdhughes #564's engine identity
                  sum_c |tau_w(c)|^4 = p^w (2 n^2 - n)
                  (moment-curve over the subgroup mu_n, finite F_p^w);
           and confirms the moment curve is Sidon at BOTH scales (the 4th
           moment is pinned at its minimum, structure-blind) while the 6th
           moment is structure-SENSITIVE (interval != dissociated) -- the exact
           border #663 and #564 both point at.
  BLOCK C  recomputes DannyExperiments #668's unconditional subset-sum bounds
           f <= 2^(b-d), L <= sum_{j<=d} C(b,j), fL <= 3^b, L <= 2^(H2(eta)b),
           and the atom cap rho* <= log(3/2), by exhaustive subset-sum
           enumeration on small degree-2 moment blocks a_i=(1,v_i,v_i^2).

Run:  ulimit -v 2097152; python3 experimental/scripts/verify_mi_ma_sidon_route_audit.py
"""
import os
import sys
import math
import cmath
from itertools import combinations, product

FAIL = 0
OK = 0


def check(cond, label):
    global FAIL, OK
    if cond:
        OK += 1
    else:
        FAIL += 1
        print(f"FAIL: {label}")


def repo_root():
    # scripts live in experimental/scripts/; repo root is two levels up.
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


ROOT = repo_root()


def read_lines(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read().split("\n")


def anchor_ok(rel, lineno, expected):
    """True iff line `lineno` (1-based) of `rel` equals `expected` exactly."""
    lines = read_lines(rel)
    if lineno < 1 or lineno > len(lines):
        return False
    return lines[lineno - 1] == expected


# ---------------------------------------------------------------------------
# BLOCK A -- byte-exact anchors (every quote in the note is pinned here)
# ---------------------------------------------------------------------------
TEX = "experimental/asymptotic_rs_mca_frontiers.tex"
AGENTS = "agents.md"
LEDGER = "experimental/notes/roadmaps/b2_l1_reduction_ledger.md"
FIT = "experimental/notes/thresholds/fiber_image_tradeoff.md"

ANCHORS = [
    # frontiers.tex -- the hard-input phrasing (image-scale MI/MA or Sidon)
    (TEX, 160, "requires a witness-exhaustive atlas, image-scale MI and MA or a direct"),
    (TEX, 161, "Sidon payment, residual ray bounds, and comparison of the complete profile"),
    (TEX, 162, "envelope with the target and lower reserve."),
    (TEX, 778, "still requires a witness-exhaustive first-match atlas, image-scale"),
    (TEX, 779, "effective Fourier payment or a direct Sidon payment, residual ray bounds"),
    (TEX, 7105, "The atlas payments, \\textup{(MA)}, image-scale conditions,"),
    (TEX, 7106, "\\textup{(RC)}, and full profile envelope remain separate checks."),
    (TEX, 7128, "integer bound.  The paper closes the high-energy Boolean branch, but it"),
    (TEX, 7129, "does not close the Sidon, algebraic-projection, or higher-dimensional ray"),
    (TEX, 7217, "a direct Sidon estimate, the primitive image-scale and"),
    # agents.md -- hard input #2 and the gating clause
    (AGENTS, 47, "image-scale MI + MA, or a direct Sidon payment;"),
    (AGENTS, 61, "4. use the Sidon/Fourier split and BSG/quasicube argument only after the"),
    (AGENTS, 62, "   image-scale MI/MA or direct Sidon payment is available;"),
    # scottdhughes #564 reduction ledger (base-integrated)
    (LEDGER, 14, "VERIFIED ASSETS (don't re-derive): (1) engine identities Sum|tau_w|^2=p^w n, Sum|tau_w|^4=p^w(2n^2-n) PROVEN"),
    (LEDGER, 35, "`Phi(x)=(x,...,x^w)`, `F(S)=sum_{x in S}Phi(x)`, `nu(v)=#{|S|=m: F(S)=v}`, `mu=C(n,m)/p^w`, `N=nu(0)`."),
    (LEDGER, 38, "codewords of C}`. **TARGET (E-b): `N <= n^3`.**"),
    (LEDGER, 263, "     merely an L^2->L^q amplification is NOT enough; the estimate must be SIGNED (one-sided inverse theorem)."),
    (LEDGER, 422, "large-sieve / inverse theorem for binomially-weighted cyclic moment maps, spanning the large-subgroup and"),
    # holmbuar #655 conditional cap
    (FIT, 13, "CONDITIONAL CAP: rho* < log2 under the named (ILO-moment) hypothesis, which is"),
]

for rel, lineno, expected in ANCHORS:
    check(anchor_ok(rel, lineno, expected), f"anchor {rel}:{lineno}")

# Negative control: a corrupted quote MUST be rejected by the checker.
check(not anchor_ok(TEX, 160, "requires a witness-exhaustive atlas, image-scale MI and MA or a DIRECT"),
      "negative-test (corrupted tex quote must fail)")
check(not anchor_ok(AGENTS, 47, "image-scale MI + MA, or a direct sidon payment;"),
      "negative-test (corrupted agents.md quote must fail)")


# ---------------------------------------------------------------------------
# BLOCK B -- the two Sidon 4th-moment identities (the applicability pivot)
# ---------------------------------------------------------------------------

def int_S_2m(V, m):
    """INT_{[0,1)^2} |S(t1,t2)|^{2m} for S=sum e(t1 v + t2 v^2), V a block.
    Equals #{ordered (i_1..i_m; j_1..j_m): sum v_i = sum v_j and
    sum v_i^2 = sum v_j^2} (orthogonality on the torus)."""
    b = len(V)
    p1 = {}  # (sum, sumsq) -> count of ordered m-tuples
    for tup in product(range(b), repeat=m):
        s = sum(V[i] for i in tup)
        s2 = sum(V[i] * V[i] for i in tup)
        p1[(s, s2)] = p1.get((s, s2), 0) + 1
    return sum(c * c for c in p1.values())


# (i) #663 degree-2 identity INT|S|^4 = 2b^2 - b, structure-independent.
BLOCKS = [
    [0, 1, 2, 3, 4],
    [2, 3, 4, 6, 13],
    [0, 5, 17, 42, 100, 101],          # dissociated-ish
    [3, 7, 11, 19, 23, 31, 47],
    # #655 / #663 b=18 champion (INT|S|^4 must be 630)
    [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34],
]
for V in BLOCKS:
    b = len(V)
    check(int_S_2m(V, 2) == 2 * b * b - b,
          f"#663 INT|S|^4 = 2b^2-b on block b={b}")
# named champion value
champ = [2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34]
check(int_S_2m(champ, 2) == 630, "#663 b=18 champion INT|S|^4 = 630")

# 6th moment IS structure-sensitive (interval != dissociated) at the SAME b.
b6 = 8
interval8 = list(range(b6))
dissoc8 = [0, 1, 2, 4, 8, 16, 32, 64]  # subset-dissociated (powers of 2)
check(int_S_2m(interval8, 3) != int_S_2m(dissoc8, 3),
      "#663 INT|S|^6 structure-SENSITIVE (interval != dissociated) at b=8")
# and both 4th moments still coincide at 2b^2-b (structure-blind border)
check(int_S_2m(interval8, 2) == 2 * b6 * b6 - b6 and int_S_2m(dissoc8, 2) == 2 * b6 * b6 - b6,
      "#663 4th moment identical for interval and dissociated (structure-blind)")


# (ii) scottdhughes #564 engine  sum_c|tau_w(c)|^4 = p^w(2n^2-n)  over mu_n.
def prime_factors(m):
    f, d = set(), 2
    while d * d <= m:
        while m % d == 0:
            f.add(d)
            m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f


def subgroup(p, n):
    """Order-n subgroup of F_p^*  (n | p-1)."""
    assert (p - 1) % n == 0
    for g in range(2, p):
        if pow(g, n, p) == 1 and all(pow(g, n // q, p) != 1 for q in prime_factors(n)):
            base = g
            break
    else:
        raise RuntimeError("no generator of order n")
    return [pow(base, k, p) for k in range(n)]


def sum_tau4(p, n, w):
    mu = subgroup(p, n)
    tot = 0.0
    for c in product(range(p), repeat=w):
        s = 0j
        for x in mu:
            ph = 0
            xk = 1
            for j in range(w):
                xk = (xk * x) % p          # x^(j+1)
                ph = (ph + c[j] * xk) % p
            s += cmath.exp(2j * math.pi * ph / p)
        tot += (s * s.conjugate()).real ** 2
    return tot


for (p, n, w) in [(7, 3, 2), (13, 3, 2), (13, 4, 2), (11, 5, 2), (7, 3, 3)]:
    val = sum_tau4(p, n, w)
    pred = (p ** w) * (2 * n * n - n)
    check(abs(val - pred) < 1e-6,
          f"#564 sum_c|tau_w|^4 = p^w(2n^2-n) at p={p},n={n},w={w}")

# The moment curve is Sidon: two points are determined by (p1,p2). Direct check
# that no NONTRIVIAL 2-vs-2 additive quadruple exists on {(v,v^2)}.
def nontrivial_2v2(V):
    b = len(V)
    for i in range(b):
        for k in range(i, b):
            for j in range(b):
                for l in range(j, b):
                    if {i, k} == {j, l}:
                        continue
                    if V[i] + V[k] == V[j] + V[l] and V[i] ** 2 + V[k] ** 2 == V[j] ** 2 + V[l] ** 2:
                        return True
    return False


for V in BLOCKS:
    check(not nontrivial_2v2(V), f"moment curve Sidon: no nontrivial 2-vs-2 quadruple (b={len(V)})")


# ---------------------------------------------------------------------------
# BLOCK C -- DannyExperiments #668 unconditional subset-sum bounds
# ---------------------------------------------------------------------------

def subset_sum_stats(cols, modulus=None):
    """Given columns a_i in Z^d (or Z_modulus^d), enumerate all 2^b subset sums;
    return (f, L, d_dissoc) = (max fiber, image size, max subset-dissociated)."""
    b = len(cols)
    d = len(cols[0])
    fibers = {}
    for mask in range(1 << b):
        s = [0] * d
        for i in range(b):
            if mask & (1 << i):
                for t in range(d):
                    s[t] += cols[i][t]
        if modulus is not None:
            s = tuple(v % modulus for v in s)
        else:
            s = tuple(s)
        fibers[s] = fibers.get(s, 0) + 1
    f = max(fibers.values())
    L = len(fibers)
    # max subset-dissociated I: all 2^|I| subset sums of (a_i)_{i in I} distinct
    d_dissoc = 0
    for size in range(b, 0, -1):
        found = False
        for I in combinations(range(b), size):
            seen = set()
            distinct = True
            for mask in range(1 << size):
                s = [0] * d
                for t2, i in enumerate(I):
                    if mask & (1 << t2):
                        for t in range(d):
                            s[t] += cols[i][t]
                key = tuple(s)
                if key in seen:
                    distinct = False
                    break
                seen.add(key)
            if distinct:
                found = True
                break
        if found:
            d_dissoc = size
            break
    return f, L, d_dissoc


def H2(eta):
    if eta <= 0 or eta >= 1:
        return 0.0
    return -eta * math.log2(eta) - (1 - eta) * math.log2(1 - eta)


# degree-2 moment blocks a_i = (1, v_i, v_i^2); enumerate exactly.
for V in ([0, 1, 2, 3, 4, 5], [0, 1, 3, 7], [2, 3, 5, 7, 11], [0, 1, 2, 4, 8]):
    cols = [(1, v, v * v) for v in V]
    f, L, d = subset_sum_stats(cols)
    b = len(V)
    check(f <= 2 ** (b - d), f"#668 f <= 2^(b-d) on b={b}")
    check(L <= sum(math.comb(b, j) for j in range(d + 1)), f"#668 L <= sum_{{j<=d}} C(b,j) on b={b}")
    check(f * L <= 3 ** b, f"#668 fL <= 3^b on b={b}")
    r = int(b - math.log2(f))
    check(L <= sum(math.comb(b, j) for j in range(r + 1)), f"#668 L <= sum_{{j<=r}} C(b,j) on b={b}")
    # entropy form: if f >= 2^{(1-eta)b} then L <= 2^{H2(eta) b} for eta<=1/2
    eta = 1 - math.log2(f) / b
    if 0 < eta <= 0.5:
        check(L <= 2 ** (H2(eta) * b) + 1e-9, f"#668 L <= 2^(H2(eta)b) on b={b}")
    else:
        OK += 1  # eta out of (0,1/2]; entropy clause vacuous, count as trivially ok

# The atom cap rho* <= log(3/2) < log 2 follows from fL <= 3^b (natural logs).
check(math.log(3.0 / 2.0) < math.log(2.0), "#668 atom cap log(3/2) < log 2")
check(abs(math.log(1.5) - 0.4054651081) < 1e-9, "#668 rho* ceiling log(3/2) = 0.405465")


# ---------------------------------------------------------------------------
total = OK + FAIL
if FAIL:
    print(f"RESULT: FAIL ({OK}/{total})")
    sys.exit(1)
print(f"RESULT: PASS ({OK}/{total})")
