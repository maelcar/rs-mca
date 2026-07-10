#!/usr/bin/env python3
"""Zero-argument stdlib verifier for cap25_v13_m31_integral_ratio_degree4.md.

Escalates PR #481's degree-two spherical-LP cut to the full constant-weight
(Johnson-scheme J(n,m)) Delsarte linear-programming bound.  Eigenspace j=2
reproduces #481's exact 187 eliminated integral-ratio pairs; eigenspaces j>=3
strictly escalate.  Every eliminated pair is a sound exact-integer certificate;
the Eberlein eigenvalue formula is machine-checked against brute-force spectra,
and the cut is gated on realizable faithful-toy two-shell families (it must
never eliminate one).
"""
import copy
import hashlib
import json
import os
import sys
from math import comb
from collections import defaultdict
from itertools import combinations


def apply_memory_cap():
    try:
        import resource
        cap = 2 * 1024 ** 3
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        hard2 = cap if hard == resource.RLIM_INFINITY else min(cap, hard)
        if soft == resource.RLIM_INFINITY or soft > cap:
            resource.setrlimit(resource.RLIMIT_AS, (cap, hard2))
    except Exception:
        pass


apply_memory_cap()

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.join(ROOT, "experimental", "data",
                    "cap25_v13_m31_integral_ratio_degree4.json")
CHECKS = []

# Eigenspaces used by the deployed Johnson-scheme LP scan.  The cascade
# saturates at j=3 (see the binding-j histogram in the note); scanning to j=6
# exhibits three empty eigenspaces j=4,5,6, and a thin-band probe (documented in
# the note) confirms no eliminations through j=20.
JMAX = 6


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def ceil_div(a, b):
    return -((-a) // b)


# --------------------------------------------------------------- Johnson/Eberlein
def ff(x, a):
    """Falling factorial x^(a) = x(x-1)...(x-a+1)."""
    r = 1
    for i in range(a):
        r *= (x - i)
    return r


def cb(a, b):
    if b < 0 or a < 0 or b > a:
        return 0
    return comb(a, b)


def eberlein(v, m, i, j):
    """Raw Johnson-scheme eigenvalue P_i(j): eigenvalue of the distance-i
    adjacency matrix of J(v,m) on the j-th eigenspace."""
    return sum((-1) ** s * comb(j, s) * cb(m - j, i - s) * cb(v - m - j, i - s)
               for s in range(j + 1))


def valency(v, m, i):
    return comb(m, i) * comb(v - m, i)


def mult(v, j):
    return comb(v, j) - (comb(v, j - 1) if j >= 1 else 0)


def num_norm(v, m, e, j):
    """Numerator N_j(e) of the normalized eigenvalue p_j(e) = P_e(j)/v_e,
    written to avoid the astronomically large raw binomials.  Denominator is
    den_norm(v,m,j) > 0."""
    s = 0
    for ss in range(j + 1):
        s += ((-1) ** ss) * comb(j, ss) * (ff(e, ss) ** 2) \
            * ff(m - e, j - ss) * ff(v - m - e, j - ss)
    return s


def den_norm(v, m, j):
    return ff(m, j) * ff(v - m, j)


def lp_infeasible(v, m, e1, e2, L, jmax):
    """Delsarte constant-weight LP over eigenspaces j=1..jmax.

    A two-distance code of size L in J(v,m) with distances {e1,e2} has inner
    distribution (1, a, b), a+b=L-1, a,b>=0, and every eigenspace j obeys
        1 + a*p_j(e1) + b*p_j(e2) >= 0.
    Returns (infeasible, binding_j).  Pure integer cross-multiplication; the
    feasible a-interval is tracked as [ln/ld, hn/hd] with positive denominators.
    """
    ln, ld = 0, 1
    hn, hd = L - 1, 1
    Lm1 = L - 1
    for j in range(1, jmax + 1):
        dj = den_norm(v, m, j)
        if dj == 0:
            continue
        n1 = num_norm(v, m, e1, j)
        n2 = num_norm(v, m, e2, j)
        # constraint a*(N1-N2) >= -dj - (L-1)*N2   (multiplied through by dj>0)
        c = n1 - n2
        rhs = -dj - Lm1 * n2
        if c > 0:
            if rhs * ld > ln * c:              # a >= rhs/c tightens lower bound
                ln, ld = rhs, c
        elif c < 0:
            nn, dd = rhs, c                     # a <= rhs/c ; normalise denom>0
            if dd < 0:
                nn, dd = -nn, -dd
            if nn * hd < hn * dd:
                hn, hd = nn, dd
        else:
            if rhs > 0:                         # constraint 0 >= rhs is violated
                return True, j
        if ln * hd > hn * ld:                   # empty interval
            return True, j
    return False, None


# ------------------------------------------------ brute-force spectrum soundness
def verify_scheme(v, m, tmax=6):
    """Confirm eberlein()/mult() are the true spectrum: tr(A_i^t)=sum_j mu_j P_i(j)^t,
    and that num_norm/den_norm equals the normalized raw eigenvalue."""
    verts = [frozenset(c) for c in combinations(range(v), m)]
    N = len(verts)
    A = {i: [[0] * N for _ in range(N)] for i in range(m + 1)}
    for a in range(N):
        for b in range(N):
            i = m - len(verts[a] & verts[b])
            A[i][a][b] = 1
    spectrum_ok = True
    for i in range(0, min(m, 3) + 1):
        Mt = A[i]
        cur = [[1 if x == y else 0 for y in range(N)] for x in range(N)]
        for t in range(tmax + 1):
            tr = sum(cur[x][x] for x in range(N))
            formula = sum(mult(v, j) * eberlein(v, m, i, j) ** t for j in range(m + 1))
            if tr != formula:
                spectrum_ok = False
            nxt = [[0] * N for _ in range(N)]
            for x in range(N):
                cx = cur[x]
                for z in range(N):
                    if cx[z]:
                        Mz = Mt[z]
                        czx = cx[z]
                        nr = nxt[x]
                        for y in range(N):
                            if Mz[y]:
                                nr[y] += czx
            cur = nxt
    from fractions import Fraction as Fr
    norm_ok = True
    for e in range(m + 1):
        for j in range(m + 1):
            if Fr(eberlein(v, m, e, j), valency(v, m, e)) != \
               Fr(num_norm(v, m, e, j), den_norm(v, m, j)):
                norm_ok = False
    struct_ok = (all(eberlein(v, m, i, 0) == valency(v, m, i) for i in range(m + 1))
                 and all(eberlein(v, m, 0, j) == 1 for j in range(m + 1))
                 and sum(mult(v, j) for j in range(m + 1)) == N)
    return spectrum_ok and norm_ok and struct_ok


# ------------------------------------------------------- faithful twin-coset toys
def cmul(u, v, p):
    a, b = u
    c, d = v
    return ((a * c - b * d) % p, (a * d + b * c) % p)


def cpow(u, e, p):
    out = (1, 0)
    while e:
        if e & 1:
            out = cmul(out, u, p)
        u = cmul(u, u, p)
        e >>= 1
    return out


def eorder(u, p):
    val = (1, 0)
    for o in range(1, p + 2):
        val = cmul(val, u, p)
        if val == (1, 0):
            return o
    raise AssertionError


def circle_gen(p):
    for a in range(p):
        for b in range(p):
            if (a * a + b * b) % p == 1 and eorder((a, b), p) == p + 1:
                return (a, b)
    raise AssertionError


def twin_domain(p, n):
    om = circle_gen(p)
    q = (p + 1) // n
    H = [cpow(om, q * j, p) for j in range(n)]
    lifted = {cmul(om, h, p) for h in H} | {cmul(cpow(om, p, p), h, p) for h in H}
    by = defaultdict(list)
    for u in lifted:
        by[u[0]].append(u)
    assert len(lifted) == 2 * n
    return sorted(by)


def max_clique(adj):
    best = []

    def expand(stack, cand):
        nonlocal best
        if not cand:
            if len(stack) > len(best):
                best = stack.copy()
            return
        if len(stack) + bin(cand).count("1") <= len(best):
            return
        c = cand
        while c:
            b = c & -c
            vtx = b.bit_length() - 1
            c ^= b
            stack.append(vtx)
            expand(stack, cand & adj[vtx])
            stack.pop()
            cand ^= b
            if len(stack) + bin(cand).count("1") <= len(best):
                return
    expand([], (1 << len(adj)) - 1)
    return best


def toy_realizable_families(p, n, m, w):
    """Every inclusion-maximal one/two-shell family in every prefix fiber."""
    D = twin_domain(p, n)
    fibers = defaultdict(list)
    for subset in combinations(range(len(D)), m):
        key = tuple(sum(pow(D[i], j, p) for i in subset) % p for j in range(1, w + 1))
        fibers[key].append(sum(1 << i for i in subset))
    fams = set()
    for verts in fibers.values():
        c = len(verts)
        if c < 2:
            continue
        dist = [[0] * c for _ in range(c)]
        vals = set()
        for i in range(c):
            for j in range(i):
                e = m - bin(verts[i] & verts[j]).count("1")
                dist[i][j] = dist[j][i] = e
                vals.add(e)
        pairs = [(e,) for e in sorted(vals)] + list(combinations(sorted(vals), 2))
        for allowed in pairs:
            aset = set(allowed)
            adj = [0] * c
            for i in range(c):
                for j in range(i):
                    if dist[i][j] in aset:
                        adj[i] |= 1 << j
                        adj[j] |= 1 << i
            clique = max_clique(adj)
            if len(clique) >= 2:
                masks = [verts[i] for i in clique]
                sh = sorted({m - bin(masks[i] & masks[j]).count("1")
                             for i in range(len(masks)) for j in range(i)})
                if 1 <= len(sh) <= 2:
                    fams.add((sh[0], sh[-1], len(clique)))
    return sorted(fams)


# --------------------------------------------------------------- deployed scan
def deployed_scan(n, m, w, Bstar, jmax):
    """Regenerate the PR #480/#481 grid and run the Johnson-scheme LP + the
    single-eigenvalue inclusion-moment consistency check on every pair."""
    L0 = Bstar + 1
    R = m * (n - m)
    cm = {t: comb(m, t) for t in (2, 3, 4)}   # pair-independent constants
    grid_count = 0
    j2_elim = []           # eliminated already at eigenspace j<=2 (matches #481)
    all_elim = []          # eliminated by the full LP (j<=jmax)
    hist = {}
    moment_min = None      # min over grid of the t=2,3,4 inclusion-moment values
    for k in range(2, 775):
        lo = ceil_div(w + 1, k - 1)
        hi = min(m // k, R // (n * (k - 1)))
        if lo > hi:
            continue
        for tp in range(lo, hi + 1):
            e1 = (k - 1) * tp
            e2 = k * tp
            grid_count += 1
            # inclusion-matrix single-eigenvalue moment consistency (must be >=0)
            for t in (2, 3, 4):
                g = cm[t] - k * comb(m - e1, t) + (k - 1) * comb(m - e2, t)
                if moment_min is None or g < moment_min:
                    moment_min = g
            inf, jb = lp_infeasible(n, m, e1, e2, L0, jmax)
            if inf:
                all_elim.append((k, tp, e1, e2, jb))
                hist[jb] = hist.get(jb, 0) + 1
                if jb <= 2:                    # incremental LP => j<=2 prefix
                    j2_elim.append((k, tp))
    return {
        "grid_count": grid_count,
        "j2_elim": j2_elim,
        "all_elim": all_elim,
        "hist": hist,
        "moment_min": moment_min,
    }


def build_expected(scan):
    n = 2 ** 21
    m = 981_129
    w = 67_447
    Bstar = 2 ** 24 - 1
    L0 = Bstar + 1
    all_elim = scan["all_elim"]
    hist = scan["hist"]
    surviving = scan["grid_count"] - len(all_elim)
    # canonical certificate of the newly-escalated eliminations (j>=3)
    new_rows = sorted((k, tp, e1, e2, jb) for (k, tp, e1, e2, jb) in all_elim if jb >= 3)
    canonical = ";".join(",".join(map(str, r)) for r in new_rows).encode("ascii")
    all_rows = sorted((k, tp, e1, e2, jb) for (k, tp, e1, e2, jb) in all_elim)
    all_canon = ";".join(",".join(map(str, r)) for r in all_rows).encode("ascii")
    packet = {
        "schema": "cap25-v13-m31-integral-ratio-degree4-v1",
        "status": ("PROVED Johnson-scheme Delsarte LP escalation of the #481 "
                   "degree-two cut / OPEN residual integral-ratio grid"),
        "deployed": {
            "p": 2 ** 31 - 1, "n": n, "m": m, "w": w,
            "Bstar": Bstar, "L0": L0,
        },
        "grid": {"pair_count": scan["grid_count"]},
        "johnson_lp": {
            "eigenspace_cap": JMAX,
            "j2_eliminated_count": len(scan["j2_elim"]),
            "pr481_degree2_count": 187,
            "total_eliminated_count": len(all_elim),
            "escalation_new_count": len(new_rows),
            "surviving_count": surviving,
            "binding_j_histogram": {str(j): hist[j] for j in sorted(hist)},
            "max_binding_j": max(hist) if hist else 0,
            "checksums": {
                "sum_k": sum(r[0] for r in all_rows),
                "sum_t": sum(r[1] for r in all_rows),
                "sum_e1": sum(r[2] for r in all_rows),
                "sum_e2": sum(r[3] for r in all_rows),
            },
            "escalation_canonical_bytes": len(canonical),
            "escalation_canonical_sha256": hashlib.sha256(canonical).hexdigest(),
            "all_eliminated_canonical_sha256": hashlib.sha256(all_canon).hexdigest(),
            "first_five_escalated": [list(r) for r in new_rows[:5]],
            "last_five_escalated": [list(r) for r in new_rows[-5:]],
        },
        "inclusion_moment_cut": {
            "levels": [2, 3, 4],
            "min_value_over_grid": scan["moment_min"],
            "vacuous": scan["moment_min"] >= 0,
        },
    }
    return packet


def main():
    if len(sys.argv) != 1:
        print("usage: verify_m31_integral_ratio_degree4.py")
        return 2

    with open(DATA, encoding="utf-8") as handle:
        data = json.load(handle)

    print("== Eberlein eigenvalue soundness (brute-force small Johnson schemes) ==")
    for (v, m0) in [(6, 3), (7, 3), (8, 3), (9, 4)]:
        check(f"J({v},{m0}) spectrum & normalized-eigenvalue identity",
              verify_scheme(v, m0))

    print("\n== Deployed grid: Johnson-scheme Delsarte LP escalation ==")
    n = 2 ** 21
    m = 981_129
    w = 67_447
    Bstar = 2 ** 24 - 1
    scan = deployed_scan(n, m, w, Bstar, JMAX)
    expected = build_expected(scan)
    jlp = expected["johnson_lp"]
    check("grid pair count 3254885", scan["grid_count"] == 3_254_885)
    check("eigenspace j<=2 reproduces #481 count 187",
          jlp["j2_eliminated_count"] == 187)
    # set-equality against #481's closed-form degree-two cut
    R = m * (n - m)
    D = n - 1
    L0 = Bstar + 1
    cf = set()
    for k in range(2, 775):
        lo = ceil_div(w + 1, k - 1)
        hi = min(m // k, R // (n * (k - 1)))
        for tp in range(lo, hi + 1):
            e1 = (k - 1) * tp
            e2 = k * tp
            den = D * (R - e1 * n) * (R - e2 * n) + R * R
            if (e1 + e2) * n >= 2 * R and den > 0 and e1 * e2 * n * n * D < L0 * den:
                cf.add((k, tp))
    check("eigenspace j<=2 set-equals #481 closed-form cut",
          set(scan["j2_elim"]) == cf and len(cf) == 187)
    check("Johnson LP strictly escalates beyond 187",
          jlp["total_eliminated_count"] > 187)
    check("escalation counts consistent",
          jlp["j2_eliminated_count"] + jlp["escalation_new_count"]
          == jlp["total_eliminated_count"])
    check("surviving = grid - eliminated",
          jlp["surviving_count"] == scan["grid_count"] - jlp["total_eliminated_count"])
    check("cascade saturates below the eigenspace cap",
          jlp["max_binding_j"] < JMAX)
    check("every eliminated pair is integral-ratio",
          all(e1 == (k - 1) * tp and e2 == k * tp
              for (k, tp, e1, e2, _jb) in scan["all_elim"]))

    print("\n== Single-eigenvalue inclusion-moment cut is vacuous ==")
    check("C(m,t)-k C(m-e1,t)+(k-1) C(m-e2,t) >= 0 for all grid pairs (t=2,3,4)",
          scan["moment_min"] >= 0,
          "min=%d" % scan["moment_min"])

    print("\n== Soundness gates: LP must not eliminate a realizable toy family ==")
    for (p, nn, mm, ww, label) in [(31, 8, 4, 2, "p31,n8"),
                                    (127, 16, 8, 1, "p127,n16")]:
        fams = toy_realizable_families(p, nn, mm, ww)
        bad = [(e1, e2, sz) for (e1, e2, sz) in fams
               if lp_infeasible(nn, mm, e1, e2, sz, mm)[0]]
        check(f"{label}: {len(fams)} realizable two-shell families, none eliminated",
              not bad, "families=%d" % len(fams))
    # p127,n32 explicit inclusion-maximal witness (shells {7,8}, size 17)
    check("p127,n32 witness (shells 7,8 size 17) not eliminated",
          not lp_infeasible(32, 15, 7, 8, 17, 15)[0])

    print("\n== JSON packet exact replay ==")
    validator = lambda cand: cand == expected
    check("JSON packet exactly matches regenerated certificate", validator(data))

    print("\n== Corruption self-tests ==")
    corruptions = [
        ("grid count", ("grid", "pair_count"), lambda x: x - 1),
        ("j2 count", ("johnson_lp", "j2_eliminated_count"), lambda x: x + 1),
        ("total eliminated", ("johnson_lp", "total_eliminated_count"), lambda x: x - 1),
        ("escalation count", ("johnson_lp", "escalation_new_count"), lambda x: x + 1),
        ("surviving count", ("johnson_lp", "surviving_count"), lambda x: x + 1),
        ("sum_e2 checksum", ("johnson_lp", "checksums", "sum_e2"), lambda x: x + 1),
        ("escalation hash", ("johnson_lp", "escalation_canonical_sha256"),
         lambda x: ("1" if x[0] != "1" else "2") + x[1:]),
        ("moment vacuity flag", ("inclusion_moment_cut", "vacuous"), lambda x: not x),
    ]
    for name, path, mut in corruptions:
        damaged = copy.deepcopy(data)
        cur = damaged
        for key in path[:-1]:
            cur = cur[key]
        cur[path[-1]] = mut(cur[path[-1]])
        check(f"tampered {name} is rejected", not validator(damaged))

    passed = sum(ok for _n, ok in CHECKS)
    total = len(CHECKS)
    print(f"\nRESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total} checks)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
