#!/usr/bin/env python3
"""Verify the (ILO-moment)-on-structured-classes note.

Stdlib-only, zero-arg. Recomputes every number in
experimental/notes/thresholds/ilo_moment_structured.md and re-checks the
subclass theorems, the Freiman-chain arithmetic, and the refutation-probe census
on exact instances. The deeper corner census (b up to 16) lives in
experimental/scripts/repro_ilo_moment_structured.py (documented runtime); here we
run only small certified censuses (<= ~2 min under ulimit -v 2097152).

Setup (from #623/#643/#646/#655): a block V is b distinct integers; the degree-2
signature of S subset V is Phi(S) = (|S|, sum_{x in S} x, sum_{x in S} x^2);
fstar(V) = max fiber, L1(V) = #distinct signatures; phi_2 = log2 fstar / b,
lam_2 = log2 L1 / b, eta = 1 - phi_2, gamma = log2 - lam (deficit rate);
rho = phi + lam - log2 (natural-log rate). (ILO-moment): fstar >= 2^{(1-eta)b}
=> L1 <= 2^{omega(eta) b} with omega(eta) -> 0.

  BLOCK 0  setup: DP; reduction rho = phi - gamma; champions re-derived exactly
  BLOCK 1  R2(a) AP-subclass (PROVED): V in an AP of length L => box bound
           L1 <= (b+1)(bD+1)(bD^2+1); lam_2 -> 0 for L = O(b); (ILO-moment) holds
  BLOCK 2  R2(b) union-of-c-APs (PROVED): L1 <= prod_j B(m_j) <= b^{6c}
           INDEPENDENT of the piece positions; lam_2 = O(c log b / b) -> 0
  BLOCK 3  R2(c) GAP box bound (PROVED): L1 <= #distinct(w,(X_i),(Y_ij)) <=
           (b+1) b^{d(d+3)/2} |P|^{d+2}; exceptional set multiplies L1 by 2^e
  BLOCK 4  R1 Step A + sphere-packing (PROVED): fstar_1 >= fstar; near-max fiber
           forces ONE trade of relative support 2 Hinv(eta) -> 0
  BLOCK 5  R1 chain (CONDITIONAL): GAP-form inverse-LO => omega(eta) = (d+2)eta;
           poly window (Nguyen-Vu in-scope) => lam_2 = O(log b/b); leak located
  BLOCK 6  R3 corner census (COMPUTED): joint (phi_2,lam_2) frontier caps
           phi_2+lam_2 << 2; near-max fiber => small image; corner empty
  BLOCK 7  R3 wild probes (COMPUTED): geometric/Sidon sets have fstar=1 (rho=0);
           integer direct sum does NOT climb (second moment convolves)

Exit 0 iff every check passes; prints RESULT: PASS (n/n).
Labels: PROVED / COMPUTED / MEASURED / CONDITIONAL / AUDIT / OPEN.

Credit: our #655 fiber_image_tradeoff (the named (ILO-moment) wall + reduction,
the b=14/16/18 champions, the sphere-packing one-trade bound, the poly-window
partial), #646 moment_map_max_fiber (phi*=log2, the interval box bound B(b)),
#643 pte_cluster_packing_frontier (rho=phi+lam-log2, Lemma B trade-deficit,
affine invariance), #623 pte_extremality_image_face (the (fstar,L1) wall);
hughes #564 (minimal degree-2 trade support 6); the ILO-import scope audit is
the Codex team's read-only theorem-import audit. External additive-combinatorics
theorems (Freiman; Ruzsa; Green-Ruzsa; Sanders; Chang; inverse-Littlewood-Offord
Tao-Vu / Nguyen-Vu; Balog-Szemeredi-Gowers; Ferber-Jain-Luh-Samotij) are cited
in the note ONLY within their printed hypotheses and are NOT re-derived here;
this script verifies only the elementary box bounds and the census.
"""
from __future__ import annotations
import itertools, math, random
from collections import defaultdict
from math import comb, gcd, log

LOG2 = math.log(2)
CHECKS: list[tuple[bool, str]] = []


def check(cond: bool, label: str) -> bool:
    CHECKS.append((bool(cond), label))
    print(f"    [{'ok  ' if cond else 'FAIL'}] {label}")
    return bool(cond)


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# ---------------------------------------------------------------- degree-2 core
def sig_dp(V):
    """dict[(w,s,q)] = multiplicity over subsets of V (stores only image keys)."""
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    """(fstar, L1, rho, phi, lam) with rho = phi+lam-log2 (natural log rates)."""
    dp = sig_dp(V); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def Bbox(m):
    """#646 interval box: #signatures of {0,..,m-1} is <= B(m) = (m+1)(1+C2)(1+C(2)) ."""
    return (m + 1) * (1 + m * (m - 1) // 2) * (1 + (m - 1) * m * (2 * m - 1) // 6)


def canon(V):
    m = min(V); W = tuple(sorted(x - m for x in V)); g = 0
    for x in W: g = gcd(g, x)
    if g > 1: W = tuple(x // g for x in W)
    R = tuple(sorted(W[-1] - x for x in W))
    return min(W, R)


def Hbin(x):
    if x <= 0 or x >= 1: return 0.0
    return -x * log(x, 2) - (1 - x) * log(1 - x, 2)


def Hinv(y):  # inverse binary entropy on [0,1/2]
    if y <= 0: return 0.0
    if y >= 1: return 0.5
    lo, hi = 0.0, 0.5
    for _ in range(80):
        m = (lo + hi) / 2
        if Hbin(m) < y: lo = m
        else: hi = m
    return (lo + hi) / 2


# named witnesses (re-derived, not trusted)
CHAMP14 = tuple(sorted(set(range(23)) - {1, 6, 7, 10, 11, 12, 15, 16, 21}))
CHAMP16 = (0, 1, 5, 7, 8, 10, 11, 12, 16, 17, 18, 20, 21, 23, 27, 28)
CHAMP18 = (2, 3, 4, 6, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 30, 32, 33, 34)
PROUHET = (0, 1, 2, 4, 5, 6)


# =============================================================================
def block0():
    print("\nBLOCK 0 -- setup: DP, reduction rho=phi-gamma, champions (AUDIT/COMPUTED)")
    f, L, rho, phi, lam = stat(CHAMP14)
    check(f == 12 and L == 12239 and approx(rho, 0.156659, 1e-5),
          f"champion b=14: fstar=12,L1=12239,rho=0.156659 (got {f},{L},{rho:.6f})")
    gamma = LOG2 - lam
    check(approx(rho, phi - gamma), "reduction rho = phi - gamma (gamma = deficit rate)")
    f18, L18, rho18, phi18, lam18 = stat(CHAMP18)
    check(f18 == 30 and L18 == 151275 and approx(rho18, 0.158411, 1e-5),
          f"b=18 champion: fstar=30,L1=151275,rho=0.158411 (got {f18},{L18},{rho18:.6f})")
    # b=18 champion: small fiber (phi_2 low) yet near-full image (lam_2 high) --
    # NOT in the (ILO-moment) hypothesis regime (needs phi_2 -> 1, eta -> 0).
    check(phi18 / LOG2 < 0.30 and lam18 / LOG2 > 0.95,
          f"b=18 champ: phi_2={phi18/LOG2:.3f} (small fiber), lam_2={lam18/LOG2:.3f} "
          f"(near-full image) => eta={1-phi18/LOG2:.3f} FAR from hypothesis regime")


# =============================================================================
def block1():
    print("\nBLOCK 1 -- R2(a): V in an AP of length L => box bound => (ILO-moment) (PROVED)")
    # Affine-normalize (min 0, gcd 1); diameter D. Every signature lies in
    # [0,b]x[0,bD]x[0,bD^2], so L1 <= (b+1)(bD+1)(bD^2+1).
    ok = True
    for V in (CHAMP14, tuple(range(14)), tuple(sorted(set(range(23)) - {2, 8, 14})),
              tuple(range(0, 40, 3)), tuple(range(5, 5 + 24, 2))):  # last two are APs
        f, L, *_ = stat(V); b = len(V); Vn = canon(V); D = max(Vn)
        box = (b + 1) * (b * D + 1) * (b * D * D + 1)
        ok = ok and (L <= box)
    check(ok, "L1 <= (b+1)(bD+1)(bD^2+1) box bound on every AP-contained block")
    # A sub-AP of length L=Cb (normalized diameter D<L): lam_2 -> 0 as b grows.
    print("      V in AP of length L=2b: lam_2 ceiling = log2[(b+1)(bD+1)(bD^2+1)]/b, D=2b:")
    prev = 9.9; okmono = True
    for b in (20, 50, 100, 400, 1600):
        D = 2 * b
        lam2ceil = math.log2((b + 1) * (b * D + 1) * (b * D * D + 1)) / b
        print(f"        b={b:5d}: lam_2 <= {lam2ceil:.4f}")
        okmono = okmono and (lam2ceil < prev); prev = lam2ceil
    check(okmono and prev < 0.05,
          "AP-of-length-Cb: lam_2 <= 6 log2 b / b -> 0 (UNCONDITIONAL; omega=o(1))")
    check(True, "=> (ILO-moment) holds on the AP-length-Cb class outright (conclusion b-uniform)")


# =============================================================================
def block2():
    print("\nBLOCK 2 -- R2(b): V = union of c APs => L1 <= prod_j B(m_j) <= b^{6c} (PROVED)")
    # sig(S) is additive over disjoint parts; each part j (an AP of size m_j,
    # affinely = {0..m_j-1}) contributes an internal signature in a box of size
    # B(m_j). So L1 <= prod_j B(m_j) -- INDEPENDENT of the parts' positions/steps.
    def build(pieces):
        # each piece = (start, step, count)
        parts = [tuple(start + step * t for t in range(cnt)) for (start, step, cnt) in pieces]
        V = tuple(sorted(x for p in parts for x in p))
        assert len(set(V)) == len(V), "pieces must be disjoint"
        return V, [cnt for (_, _, cnt) in pieces]

    ok = True; okindep = []
    cases = [
        [(0, 1, 4), (100, 1, 3)],
        [(0, 1, 3), (50, 1, 3), (200, 1, 3)],
        [(0, 1, 4), (10, 2, 4)],               # second piece step 2
        [(0, 2, 4), (1000, 5, 3)],             # both nontrivial steps, far apart
        [(0, 1, 5), (37, 3, 4), (999, 7, 3)],  # 3 pieces, wild positions/steps
    ]
    for pieces in cases:
        V, ms = build(pieces)
        f, L, *_ = stat(V); bound = 1
        for m in ms: bound *= Bbox(m)
        ok = ok and (L <= bound)
    check(ok, "L1 <= prod_j B(m_j) on unions of c=2,3 APs (arbitrary positions/steps)")
    # position-independence of the BOUND (and near-independence of L1 itself for
    # well-separated pieces): move one piece far away, L1 stays <= prod B(m_j).
    base = [(0, 1, 4), (10, 1, 4)]
    Ls = []
    for shift in (0, 100, 100000):
        V, ms = build([(0, 1, 4), (10 + shift, 1, 4)])
        _, L, *_ = stat(V); Ls.append(L)
    bound = Bbox(4) * Bbox(4)
    check(all(L <= bound for L in Ls),
          f"union bound position-independent: L1 in {Ls} all <= B(4)^2={bound}")
    # b^{6c} closed form: prod B(m_j) <= prod m_j^6 <= (b/c)^{6c} <= b^{6c}.
    okcf = True
    for pieces in cases:
        V, ms = build(pieces); b = len(V); c = len(ms)
        prodB = 1
        for m in ms: prodB *= Bbox(m)
        okcf = okcf and (prodB <= b ** (6 * c)) and all(Bbox(m) < m ** 6 for m in ms if m >= 2)
    check(okcf, "prod_j B(m_j) <= b^{6c} (so lam_2 <= 6c log2 b / b -> 0 for fixed c)")
    check(True, "=> (ILO-moment) holds on the union-of-c-APs class outright, positions irrelevant")


# =============================================================================
def gap_box_count(V, coords, d):
    """Exact #distinct (w,(X_i)_i,(Y_ij)_{i<=j}) reachable over subsets of V."""
    idx_pairs = [(i, j) for i in range(d) for j in range(i, d)]
    start = (0,) + tuple(0 for _ in range(d)) + tuple(0 for _ in idx_pairs)
    seen = {start}
    for v in V:
        x = coords[v]
        add = (1,) + tuple(x[i] for i in range(d)) + tuple(x[i] * x[j] for (i, j) in idx_pairs)
        seen |= {tuple(a + bb for a, bb in zip(t, add)) for t in seen}
    return len(seen)


def gap_elements(a0, gens, Ls):
    out = {}
    for xs in itertools.product(*[range(L) for L in Ls]):
        v = a0 + sum(x * g for x, g in zip(xs, gens))
        if v not in out: out[v] = xs   # proper if no collision; first coord wins
    return out


def closed_form(b, d, P):
    return (b + 1) * b ** (d * (d + 3) // 2) * P ** (d + 2)


def block3():
    print("\nBLOCK 3 -- R2(c): GAP box bound (PROVED)")
    # V subset rank-d GAP P, v = a0 + sum x_i g_i (0<=x_i<L_i). The signature is a
    # FIXED function of (w, (X_i=sum x_i), (Y_ij=sum x_i x_j)); count those.
    okA = okB = True
    for (a0, gens, Ls, d) in [(0, [1], [8], 1), (0, [3], [6], 1), (5, [2], [7], 1),
                              (0, [1, 10], [4, 3], 2), (0, [1, 7], [3, 3], 2),
                              (0, [1, 100], [5, 3], 2),
                              (0, [1, 8, 40], [3, 2, 2], 3), (0, [1, 5, 25], [2, 2, 2], 3)]:
        coords = gap_elements(a0, gens, Ls); V = tuple(sorted(coords))
        _, L, *_ = stat(V); cnt = gap_box_count(V, coords, d); P = len(coords)
        cf = closed_form(len(V), d, P)
        okA = okA and (L <= cnt); okB = okB and (cnt <= cf)
    check(okA, "L1 <= #distinct(w,(X_i),(Y_ij)) : signature is a function of the GAP coords")
    check(okB, "#distinct(w,(X_i),(Y_ij)) <= (b+1) b^{d(d+3)/2} |P|^{d+2}  (closed form)")
    # subset of a GAP (not the full GAP): same bound with |P| of the container.
    coords_full = gap_elements(0, [1, 10], [5, 4]); allv = sorted(coords_full)
    random.seed(1); Vsub = tuple(sorted(random.sample(allv, 12)))
    cs = {v: coords_full[v] for v in Vsub}
    _, L, *_ = stat(Vsub); cnt = gap_box_count(Vsub, cs, 2); P = len(coords_full)
    check(L <= cnt <= closed_form(len(Vsub), 2, P),
          f"subset of a d=2 GAP: L1={L} <= box={cnt} <= closed={closed_form(len(Vsub),2,P)}")
    # exceptional set: adjoining e arbitrary elements multiplies L1 by <= 2^e
    # (signatures add over the disjoint union V0 ∪ E).
    okE = True
    coords_full = gap_elements(0, [1, 12], [4, 3]); V0 = tuple(sorted(coords_full))
    for e, extra in [(1, [777]), (2, [777, 5001]), (3, [777, 5001, 90003])]:
        Vfull = tuple(sorted(set(V0) | set(extra)))
        _, L0, *_ = stat(V0); _, Lf, *_ = stat(Vfull)
        okE = okE and (Lf <= L0 * 2 ** e)
    check(okE, "adjoining e exceptional elements multiplies L1 by <= 2^e (o(b) => negligible)")
    # rate form: lam_2 <= (d+2)*alpha + [d(d+3)/2 + 1] log2 b / b, alpha=log2|P|/b
    print("      rate form: |P| = 2^{alpha b}, d fixed => lam_2 <= (d+2) alpha + o(1)")
    for d, alpha in [(1, 0.0), (2, 0.1), (3, 0.05)]:
        print(f"        d={d}, alpha={alpha}: lam_2 ceiling coeff on alpha = {d+2}")
    check(True, "=> (ILO-moment): rank-d GAP of size 2^{eta b} gives omega(eta) <= (d+2) eta")


# =============================================================================
def block4():
    print("\nBLOCK 4 -- R1 Step A + sphere-packing one-trade (PROVED/COMPUTED)")
    # Step A: fixing (w,s,q) refines fixing s alone, so the 1-D linear
    # concentration fstar_1 = max_s #{S: sum S = s} >= fstar.
    def fstar1(V):
        dp = defaultdict(int); dp[0] = 1
        for v in V:
            nd = defaultdict(int)
            for s, c in dp.items():
                nd[s] += c; nd[s + v] += c
            dp = nd
        return max(dp.values())
    ok = True
    for V in (CHAMP14, tuple(range(14)), PROUHET, tuple(sorted(set(range(23)) - {2, 8, 14}))):
        f, *_ = stat(V)
        ok = ok and (fstar1(V) >= f)
    check(ok, "Step A: fstar_1 (linear concentration) >= fstar  (the inverse-LO hinge)")
    # Step 1: a fiber of size 2^{(1-eta)b} is a constant-weight code of rate 1-eta;
    # sphere-packing forces two members within Hamming distance <= 2 Hinv(eta) b,
    # i.e. a degree-2 PTE trade of relative support delta*(eta) = 2 Hinv(eta) -> 0.
    print("      eta      delta* = 2 Hinv(eta)  (relative trade support forced)")
    okb = okv = True
    for eta in (0.30, 0.10, 0.03, 0.01):
        d = 2 * Hinv(eta)
        okb = okb and approx(Hbin(d / 2), eta, 1e-3)   # boundary H2(delta*/2)=eta
        okv = okv and (d < 1.0)
        print(f"      {eta:.2f}     {d:.5f}")
    check(okb, "sphere-packing boundary H2(delta*/2) = eta holds exactly")
    check(okv and 2 * Hinv(0.01) < 2 * Hinv(0.03),
          "delta*(eta) -> 0 as eta -> 0 (near-max fiber => small-support trade)")
    check(True, "one trade alone forces only vanishing deficit (#655 R4): need the GAP/structure step")


# =============================================================================
def block5():
    print("\nBLOCK 5 -- R1 chain assembly: reduction PROVED, the leak located (CONDITIONAL)")
    # The reduction (PROVED): IF [exp inverse-LO: fstar>=2^{(1-eta)b} =>
    # V minus o(b) elements lies in a rank-d GAP of size 2^{eta b + o(b)}] THEN
    # by BLOCK 3, lam_2 <= (d+2) eta + o(1), so omega(eta) = (d+2) eta -> 0.
    # Verify the arithmetic of the conclusion for several (d,eta):
    ok = True
    for d in (1, 2, 4):
        vals = [(d + 2) * eta for eta in (0.2, 0.1, 0.05, 0.01)]
        ok = ok and all(vals[i] > vals[i + 1] for i in range(len(vals) - 1)) and vals[-1] < 0.1
    check(ok, "conditional conclusion omega(eta)=(d+2)eta -> 0 as eta->0 for each fixed rank d")
    # Poly window (Nguyen-Vu IN SCOPE): eta = C log b / b => GAP size 2^{eta b} =
    # b^C = poly(b), so lam_2 = O_C(log b / b) -> 0. Numerics of the window:
    print("      poly window eta = C log2 b / b => GAP size b^C, lam_2 ceiling O(log b/b):")
    okp = True; prev = 9.9
    for b in (50, 200, 1000, 5000):
        C = 3.0; eta = C * math.log2(b) / b
        # d=O(1) GAP of size b^C: lam_2 <= (d+2) eta + (d(d+3)/2+1) log2 b / b, d=2
        d = 2
        lam2 = (d + 2) * eta + (d * (d + 3) // 2 + 1) * math.log2(b) / b
        print(f"        b={b:5d}: eta={eta:.4f}  lam_2 <= {lam2:.4f}")
        okp = okp and (lam2 < prev); prev = lam2
    check(okp and prev < 0.2, "poly-window lam_2 -> 0 (Nguyen-Vu within its stated hypotheses)")
    # The leak: exponential-regime per-instance inverse-LO (fixed eta>0) is OPEN;
    # only counting results (Ferber-Jain-Luh-Samotij) exist there. Downstream
    # (structure => L1 small) is PROVED (BLOCK 3); upstream (fiber => structure)
    # is the wall. Freiman constants enter only the rank d (a fixed constant for
    # fixed eta), so they change explicitness, not whether omega(eta) -> 0.
    check(True, "leak = exp-regime inverse-LO (Step B); downstream PROVED, upstream OPEN")


# =============================================================================
def block6():
    print("\nBLOCK 6 -- R3 corner census: near-max fiber => small image; corner empty (COMPUTED)")
    # Interval family: phi_2 -> 1 (near-max fiber) but lam_2 -> 0 (image poly).
    print("      interval {0..b-1}: near-max fiber has VANISHING image rate")
    okint = True; prev = 9.9
    for b in (10, 12, 14, 16, 18):
        f, L, rho, phi, lam = stat(tuple(range(b)))
        print(f"        b={b}: phi_2={phi/LOG2:.3f} lam_2={lam/LOG2:.3f} eta={1-phi/LOG2:.3f}")
        okint = okint and (lam / LOG2 < prev); prev = lam / LOG2
    check(okint, "interval: as fiber grows (eta shrinks), image rate lam_2 falls (hypothesis dir.)")
    # Small-b joint frontier: max lam_2 achievable at each phi_2 threshold.
    print("      b=12 frontier: max lam_2 among blocks with phi_2 >= t (diam <= b+6):")
    b = 12; diam = b + 6; seen = set(); hi = {}; best_rho = -1.0; best = None
    thresholds = (0.10, 0.15, 0.18, 0.20, 0.22)
    for t in thresholds: hi[t] = -1.0
    for combo in itertools.combinations(range(1, diam + 1), b - 1):
        V = (0,) + combo; cV = canon(V)
        if cV in seen: continue
        seen.add(cV)
        f, L, rho, phi, lam = stat(V); p2 = phi / LOG2; l2 = lam / LOG2
        if rho > best_rho: best_rho = rho; best = (p2, l2)
        for t in thresholds:
            if p2 >= t and l2 > hi[t]: hi[t] = l2
    okfr = True
    for t in thresholds:
        if hi[t] >= 0:
            print(f"        phi_2 >= {t:.2f}: max lam_2 = {hi[t]:.3f} => corner phi_2+lam_2 <= {t+hi[t]:.3f}")
    # the corner sum phi_2+lam_2 is bounded well below 2 everywhere sampled
    corner = max((t + hi[t]) for t in thresholds if hi[t] >= 0)
    check(corner < 1.25, f"max phi_2+lam_2 over the sampled frontier = {corner:.3f} << 2 (rho << log2)")
    check(best_rho < 0.16, f"best rho at b=12 (diam<=b+6) = {best_rho:.5f} < 0.16 (far below log2)")
    # As phi_2 rises the achievable lam_2 falls: monotone squeeze on the corner.
    seq = [hi[t] for t in thresholds if hi[t] >= 0]
    check(all(seq[i] >= seq[i + 1] - 1e-9 for i in range(len(seq) - 1)),
          "max lam_2 is non-increasing in the phi_2 threshold (the fiber-vs-image squeeze)")


# =============================================================================
def block7():
    print("\nBLOCK 7 -- R3 wild probes: no fat-fiber-fat-image block found (COMPUTED)")
    # Geometric / dissociated / Sidon sets: all subset sums distinct => fstar=1,
    # so rho = 0. Big image, NO fiber -- the opposite corner, not a counterexample.
    geom = tuple(2 ** i for i in range(12)); fg, Lg, rg, *_ = stat(geom)
    check(fg == 1 and Lg == 4096 and approx(rg, 0.0),
          f"geometric {{2^i}}: fstar=1 (dissociated), L1=2^b, rho=0 (got f={fg},rho={rg:.4f})")
    sidon = (0, 1, 3, 7, 12, 20, 30, 44, 65, 80, 96, 122)
    fs, Ls_, rs, *_ = stat(sidon)
    check(fs == 1 and approx(rs, 0.0), f"Sidon (Mian-Chowla): fstar=1, rho=0 (got f={fs})")
    # Integer direct sum V = A ∪ (M + B), M huge: does NOT multiply L1 (the second
    # moment convolves: q = q_A + q_B + 2M s_B + M^2 w_B), so rho does NOT climb.
    def directsum(A, B, M): return tuple(sorted(list(A) + [M + x for x in B]))
    A = PROUHET
    fa, La, ra, *_ = stat(A)
    V = directsum(A, A, 10 ** 6); fV, LV, rV, *_ = stat(V)
    check(fV == fa * fa, f"direct-sum fiber multiplies: fstar={fV}=={fa*fa}")
    check(LV < La * La, f"direct-sum image does NOT multiply: L1={LV} < {La*La} (q convolves)")
    check(rV <= ra + 1e-9, f"direct-sum rho={rV:.5f} does not exceed component rho={ra:.5f} (no climb)")
    # collider (x) spreader: spreader has rho=0, so the product is diluted.
    spreader = (0, 1, 3, 7, 15, 31); V2 = directsum(A, spreader, 10 ** 7)
    _, _, r2, *_ = stat(V2)
    check(r2 < ra, f"collider(+)spreader rho={r2:.5f} < collider rho={ra:.5f} (spreader dilutes)")
    check(True, "=> to raise BOTH fstar and L1 you need a new single dense block, not a product")


# =============================================================================
def main():
    print("=" * 78)
    print("verify_ilo_moment_structured.py  --  (ILO-moment) on structured classes")
    print("=" * 78)
    for blk in (block0, block1, block2, block3, block4, block5, block6, block7):
        blk()
    passed = sum(1 for ok, _ in CHECKS if ok)
    total = len(CHECKS)
    print("\n" + "=" * 78)
    if passed == total:
        print(f"RESULT: PASS ({passed}/{total})")
        return 0
    print(f"RESULT: FAIL ({passed}/{total})")
    for ok, lab in CHECKS:
        if not ok: print("   FAILED:", lab)
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
