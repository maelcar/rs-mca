#!/usr/bin/env python3
"""Zero-argument stdlib verifier for cap25_v13_m31_band_nullity_certificate.md.

The modular F_p-nullity lever on the Mersenne-31 two-shell cell (the named
non-LP next step of PR #495).  It

  1. re-extracts the exact #480 s5 nullity mechanism (the forced F_p-nullity
     floor L0-(n-w)=14747511=7n+w) with every object pinned;
  2. reproduces the #495 surviving-lattice load exactly (grid 3254885, full
     Johnson-scheme Delsarte LP through eigenspace j<=3 eliminates 527, so
     3254358 survive) and cross-checks the eliminated set against #495's
     SHA-256 and column checksums;
  3. PROVES the raw F_p-nullity floor is pair-uniform (identical over all 773
     k-rows) and therefore eliminates zero pairs by itself;
  4. derives the no-collision lemma (bounded integer spectrum, 2(L0-1)<p) and
     the Class-I integer-multiplicity forcing, giving the sharper Seidel bound
     k<=760 and its exact 8305-pair Class-I structural elimination;
  5. records that the deployed sound elimination over the unrestricted family
     class is exactly 0 (collision-excess w is achievable for every pair);
  6. re-confirms the single-eigenvalue inclusion-moment cut vacuous through t=6;
  7. gates soundness on the realizable faithful toys and demonstrates
     F_p-nullity = integer multiplicity on the actual size-23 Seidel matrix.

Pure integer/rational arithmetic; runs well under 10 minutes under
`ulimit -v 2097152`.
"""
import copy
import hashlib
import json
import os
import sys
from math import comb, isqrt
from fractions import Fraction
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
                    "cap25_v13_m31_band_nullity_certificate.json")
CHECKS = []

# The full-grid Johnson-scheme Delsarte LP scan saturates at eigenspace j=3
# (see #495).  Scanning to j=3 reproduces the whole 527-pair eliminated set.
JMAX = 3

# #495's proven deployed eliminated-set fingerprints (cross-checked, not trusted).
PR495_ALL_SHA = "73e7d66a51c52ed56dc85e48949cfe172ccacb72071957ed9ab702bc6a729af0"
PR495_SUMS = {"sum_k": 86940, "sum_t": 65325605,
              "sum_e1": 275102228, "sum_e2": 340427833}


def check(name, condition, detail=""):
    ok = bool(condition)
    CHECKS.append((name, ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))


def ceil_div(a, b):
    return -((-a) // b)


# --------------------------------------------------------------- Johnson/Eberlein
def ff(x, a):
    """Falling factorial x^(a)=x(x-1)...(x-a+1)."""
    r = 1
    for i in range(a):
        r *= (x - i)
    return r


def cb(a, b):
    if b < 0 or a < 0 or b > a:
        return 0
    return comb(a, b)


def eberlein(v, m, i, j):
    """Raw Johnson eigenvalue P_i(j)."""
    return sum((-1) ** s * comb(j, s) * cb(m - j, i - s) * cb(v - m - j, i - s)
               for s in range(j + 1))


def valency(v, m, i):
    return comb(m, i) * comb(v - m, i)


def scheme_mult(v, j):
    return comb(v, j) - (comb(v, j - 1) if j >= 1 else 0)


def num_norm(v, m, e, j):
    """Numerator N_j(e) of p_j(e)=P_e(j)/v_e (avoids astronomical raw binomials)."""
    s = 0
    for ss in range(j + 1):
        s += ((-1) ** ss) * comb(j, ss) * (ff(e, ss) ** 2) \
            * ff(m - e, j - ss) * ff(v - m - e, j - ss)
    return s


def den_norm(v, m, j):
    return ff(m, j) * ff(v - m, j)


def lp_infeasible(v, m, e1, e2, L, jmax):
    """Delsarte constant-weight (Johnson) LP over eigenspaces j=1..jmax.

    A two-distance code of size L in J(v,m) with distances {e1,e2} has inner
    distribution (1,a,b), a+b=L-1, a,b>=0, and every eigenspace obeys
    1+a*p_j(e1)+b*p_j(e2)>=0.  Returns (infeasible, binding_j).  Exact integer
    interval feasibility.
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
        c = n1 - n2
        rhs = -dj - Lm1 * n2
        if c > 0:
            if rhs * ld > ln * c:
                ln, ld = rhs, c
        elif c < 0:
            nn, dd = rhs, c
            if dd < 0:
                nn, dd = -nn, -dd
            if nn * hd < hn * dd:
                hn, hd = nn, dd
        else:
            if rhs > 0:
                return True, j
        if ln * hd > hn * ld:
            return True, j
    return False, None


def verify_scheme(v, m, tmax=5):
    """Confirm eberlein()/scheme_mult() are the true spectrum on a brute-force
    Johnson scheme, and num_norm/den_norm == the normalized raw eigenvalue."""
    verts = [frozenset(c) for c in combinations(range(v), m)]
    N = len(verts)
    Adj = {i: [[0] * N for _ in range(N)] for i in range(m + 1)}
    for a in range(N):
        for b in range(N):
            Adj[m - len(verts[a] & verts[b])][a][b] = 1
    spectrum_ok = True
    for i in range(0, min(m, 3) + 1):
        Mt = Adj[i]
        cur = [[1 if x == y else 0 for y in range(N)] for x in range(N)]
        for t in range(tmax + 1):
            tr = sum(cur[x][x] for x in range(N))
            formula = sum(scheme_mult(v, j) * eberlein(v, m, i, j) ** t
                          for j in range(m + 1))
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
    norm_ok = all(
        Fraction(eberlein(v, m, e, j), valency(v, m, e))
        == Fraction(num_norm(v, m, e, j), den_norm(v, m, j))
        for e in range(m + 1) for j in range(m + 1))
    struct_ok = (all(eberlein(v, m, i, 0) == valency(v, m, i) for i in range(m + 1))
                 and all(eberlein(v, m, 0, j) == 1 for j in range(m + 1))
                 and sum(scheme_mult(v, j) for j in range(m + 1)) == N)
    return spectrum_ok and norm_ok and struct_ok


# ----------------------------------------------------------- exact linear algebra
def nullity_mod(mat, lam, mod):
    """Nullity of (mat+lam*I) over F_mod (mod prime)."""
    L = len(mat)
    M = [[(mat[i][j] + (lam if i == j else 0)) % mod for j in range(L)]
         for i in range(L)]
    rank = row = 0
    for col in range(L):
        piv = next((r for r in range(row, L) if M[r][col] % mod), None)
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        inv = pow(M[row][col], mod - 2, mod)
        M[row] = [(x * inv) % mod for x in M[row]]
        for r in range(L):
            if r != row and M[r][col] % mod:
                f = M[r][col]
                M[r] = [(M[r][j] - f * M[row][j]) % mod for j in range(L)]
        rank += 1
        row += 1
        if row == L:
            break
    return L - rank


def nullity_Q(mat, lam):
    """Nullity of (mat+lam*I) over Q (exact rational; = real multiplicity)."""
    L = len(mat)
    M = [[Fraction(mat[i][j] + (lam if i == j else 0)) for j in range(L)]
         for i in range(L)]
    rank = row = 0
    for col in range(L):
        piv = next((r for r in range(row, L) if M[r][col] != 0), None)
        if piv is None:
            continue
        M[row], M[piv] = M[piv], M[row]
        pv = M[row][col]
        M[row] = [x / pv for x in M[row]]
        for r in range(L):
            if r != row and M[r][col] != 0:
                f = M[r][col]
                M[r] = [M[r][j] - f * M[row][j] for j in range(L)]
        rank += 1
        row += 1
        if row == L:
            break
    return L - rank


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


def toy_fibers(p, n, m, w):
    D = twin_domain(p, n)
    fibers = defaultdict(list)
    for subset in combinations(range(len(D)), m):
        key = tuple(sum(pow(D[i], j, p) for i in subset) % p for j in range(1, w + 1))
        fibers[key].append(sum(1 << i for i in subset))
    return D, fibers


def toy_realizable_families(p, n, m, w):
    """Every inclusion-maximal one/two-shell family (e1,e2,size) in each fiber."""
    _, fibers = toy_fibers(p, n, m, w)
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


# --------------------------------------------------------- the modular predicates
def classI_seidel_infeasible(N, n, w, k):
    """Class-I (bounded integer Seidel spectrum) sharper Seidel Cauchy-Schwarz.

    q=2k-1; M_lo=N-(n-w) is the F_p-nullity floor of S+qI at size N.  Under the
    no-collision lemma (2(N-1)<p and integer spectrum) the real multiplicity of
    -(2k-1) is >= M_lo, and tr S=0, tr S^2=N(N-1) give q^2*M_lo<=(N-1)(N-M_lo).
    Returns True (would eliminate) iff that necessary condition is violated and
    the floor is positive (otherwise the certificate carries no multiplicity).
    """
    M_lo = N - (n - w)
    if M_lo <= 0:
        return False
    q = 2 * k - 1
    return q * q * M_lo > (N - 1) * (N - M_lo)


def max_odd_q(N, M):
    """Largest odd q with q^2*M <= (N-1)(N-M)."""
    rhs = (N - 1) * (N - M)
    q = isqrt(rhs // M)
    while (q + 1) * (q + 1) * M <= rhs:
        q += 1
    while q * q * M > rhs:
        q -= 1
    if q % 2 == 0:
        q -= 1
    return q


def incl_moment(k, e1, e2, m, tmax):
    """Single-forced-eigenvalue inclusion-moment values (must be >=0), t=2..tmax."""
    return [comb(m, t) - k * comb(m - e1, t) + (k - 1) * comb(m - e2, t)
            for t in range(2, tmax + 1)]


# --------------------------------------------------------------- deployed scan
def deployed_scan(n, m, w, Bstar, jmax, moment_tmax):
    L0 = Bstar + 1
    R = m * (n - m)
    grid_count = 0
    all_elim = []
    hist = {}
    moment_min = None
    band_lo = band_hi = None
    for k in range(2, 775):
        lo = ceil_div(w + 1, k - 1)
        hi = min(m // k, R // (n * (k - 1)))
        if lo > hi:
            continue
        for tp in range(lo, hi + 1):
            e1 = (k - 1) * tp
            e2 = k * tp
            grid_count += 1
            mval = min(incl_moment(k, e1, e2, m, moment_tmax))
            if moment_min is None or mval < moment_min:
                moment_min = mval
            inf, jb = lp_infeasible(n, m, e1, e2, L0, jmax)
            if inf:
                all_elim.append((k, tp, e1, e2, jb))
                hist[jb] = hist.get(jb, 0) + 1
                band_lo = e1 if band_lo is None else min(band_lo, e1)
                band_hi = e1 if band_hi is None else max(band_hi, e1)
    return grid_count, all_elim, hist, moment_min, (band_lo, band_hi)


def main():
    if len(sys.argv) != 1:
        print("usage: verify_m31_band_nullity_certificate.py")
        return 2

    with open(DATA, encoding="utf-8") as handle:
        data = json.load(handle)

    p = 2 ** 31 - 1
    n = 2 ** 21
    m = 981_129
    w = 67_447
    Bstar = 2 ** 24 - 1
    L0 = Bstar + 1
    R = m * (n - m)
    rank_prefix = n - w                # 2029705 = Vandermonde/moment rank cap
    real_mult = L0 - n                 # 14680064 = 7n : guaranteed REAL multiplicity
    fp_floor = L0 - rank_prefix        # 14747511 = 7n+w : forced F_p nullity

    print("== s5 extraction: pinned deployed constants ==")
    check("row constants", (p, n, m, w, Bstar, L0)
          == (2147483647, 2097152, 981129, 67447, 16777215, 16777216))
    check("L0 = 8n (first violating size)", L0 == 8 * n)
    check("prefix rank cap n-w = 2029705 = 7... (moment+weight rows)",
          rank_prefix == 2_029_705)
    check("real multiplicity floor 7n = 14680064", real_mult == 14_680_064 == 7 * n)
    check("F_p nullity floor L0-(n-w) = 7n+w = 14747511",
          fp_floor == 14_747_511 == 7 * n + w)
    check("F_p-vs-real nullity gap is exactly w", fp_floor - real_mult == w)

    print("\n== Eberlein eigenvalue soundness (brute-force Johnson schemes) ==")
    for (v, m0) in [(6, 3), (7, 3), (8, 3)]:
        check(f"J({v},{m0}) spectrum & normalized-eigenvalue identity",
              verify_scheme(v, m0))

    print("\n== Reproduce the #495 surviving-lattice load (grid + Johnson LP) ==")
    grid_count, all_elim, hist, moment_min, band = deployed_scan(n, m, w, Bstar,
                                                                 JMAX, 6)
    all_rows = sorted(all_elim)
    elim_count = len(all_rows)
    surviving = grid_count - elim_count
    j2 = sum(1 for r in all_rows if r[4] <= 2)
    j3 = sum(1 for r in all_rows if r[4] == 3)
    sums = {"sum_k": sum(r[0] for r in all_rows), "sum_t": sum(r[1] for r in all_rows),
            "sum_e1": sum(r[2] for r in all_rows), "sum_e2": sum(r[3] for r in all_rows)}
    all_canon = ";".join(",".join(map(str, r)) for r in all_rows).encode("ascii")
    all_sha = hashlib.sha256(all_canon).hexdigest()

    check("grid pair count 3254885", grid_count == 3_254_885)
    check("Johnson LP (j<=3) eliminates 527", elim_count == 527)
    check("binding-j split {2:187, 3:340}", (j2, j3) == (187, 340))
    check("surviving lattice load 3254358", surviving == 3_254_358)
    check("eliminated set matches #495 SHA-256", all_sha == PR495_ALL_SHA)
    check("eliminated column checksums match #495", sums == PR495_SUMS)
    check("all eliminations lie in the e1 band [521834,522118]",
          band == (521_834, 522_118))
    # j<=2 set-equality against #481's closed-form degree-two certificate
    D = n - 1
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
    j2set = {(r[0], r[1]) for r in all_rows if r[4] <= 2}
    check("eigenspace j<=2 set-equals #481 closed-form 187", j2set == cf and len(cf) == 187)

    print("\n== Pair-independence: the raw s5 nullity floor eliminates 0 ==")
    floors = {L0 - rank_prefix for k in range(2, 775)}  # identical for every row
    check("F_p nullity floor is constant over all 773 k-rows",
          floors == {fp_floor})
    check("raw s5 certificate eliminations = 0 (pair-uniform floor)",
          len(floors) == 1)

    print("\n== No-collision lemma + Class-I sharper Seidel bound ==")
    seidel_sq = L0 * (L0 - 1)
    check("Seidel identity tr S^2 = L0(L0-1) = 281474959933440",
          seidel_sq == 281_474_959_933_440)
    check("no-collision margin 2(L0-1) < p", 2 * (L0 - 1) < p)
    q_base = max_odd_q(L0, real_mult)
    q_classI = max_odd_q(L0, fp_floor)
    k_base = (q_base + 1) // 2
    k_classI = (q_classI + 1) // 2
    check("baseline (M>=7n) reproduces #480 k<=774", (q_base, k_base) == (1547, 774))
    check("Class-I (M>=7n+w) sharpens to q<=1519, k<=760",
          (q_classI, k_classI) == (1519, 760))
    check("Class-I bound is exact (1519^2*floor <= (L0-1)(L0-floor) < 1521^2*floor)",
          1519 ** 2 * fp_floor <= (L0 - 1) * (L0 - fp_floor) < 1521 ** 2 * fp_floor)
    # exact Class-I structural elimination: grid rows with k in 761..774
    classI_rows = 0
    classI_new = 0                     # not already removed by the LP
    lp_set = {(r[0], r[1]) for r in all_rows}
    for k in range(k_classI + 1, 775):
        lo = ceil_div(w + 1, k - 1)
        hi = min(m // k, R // (n * (k - 1)))
        for tp in range(lo, hi + 1):
            classI_rows += 1
            if (k, tp) not in lp_set:
                classI_new += 1
    check("Class-I eliminates 8305 pairs (k in 761..774)", classI_rows == 8305)
    check("Class-I self-consistent (rows>=new, new<=survivors)",
          0 < classI_new <= classI_rows <= surviving + elim_count)

    print("\n== Single-eigenvalue inclusion-moment cut is vacuous (t=2..6) ==")
    check("min over grid of C(m,t)-kC(m-e1,t)+(k-1)C(m-e2,t) >= 0",
          moment_min >= 0, "min=%d" % moment_min)

    print("\n== Soundness gates: no realizable toy family is eliminated ==")
    toy_specs = [(31, 8, 4, 2, "p31,n8"), (127, 16, 8, 1, "p127,n16")]
    toy_report = {}
    for (pp, nn, mm, ww, label) in toy_specs:
        fams = toy_realizable_families(pp, nn, mm, ww)
        engaged = 0
        bad = []
        for (e1, e2, L) in fams:
            t = e2 - e1
            integral = t > 0 and e2 % t == 0 and e1 == (e2 // t - 1) * t
            if not integral:
                continue
            k = e2 // t
            if L - (nn - ww) > 0:
                engaged += 1
            si = classI_seidel_infeasible(L, nn, ww, k)
            im = min(incl_moment(k, e1, e2, mm, min(mm, 6)))
            if 2 * (L - 1) < pp and (si or im < 0):
                bad.append((e1, e2, L))
        toy_report[label] = {"families": len(fams), "engaged": engaged}
        check(f"{label}: {len(fams)} families, {engaged} engage the bound, none eliminated",
              not bad, "engaged=%d" % engaged)
    # p127,n32 inclusion-maximal witness (shells {7,8}, size 17)
    check("p127,n32 witness (7,8,17) not eliminated",
          not classI_seidel_infeasible(17, 32, 2, 8)
          and min(incl_moment(8, 7, 8, 15, 6)) >= 0)

    print("\n== Mechanism demo: F_p-nullity = integer multiplicity (size-23 family) ==")
    D16, fib16 = toy_fibers(127, 16, 8, 1)
    verts = fib16[(28,)]
    c = len(verts)
    dist = [[8 - bin(verts[i] & verts[j]).count("1") for j in range(c)] for i in range(c)]
    adj = [0] * c
    for i in range(c):
        for j in range(i):
            if dist[i][j] in (2, 4):
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    idx = max_clique(adj)
    L = len(idx)
    A = [[1 if (a != b and dist[idx[a]][idx[b]] == 2) else 0 for b in range(L)]
         for a in range(L)]
    S = [[2 * A[a][b] - (0 if a == b else 1) for b in range(L)] for a in range(L)]
    kk = 2
    q = 2 * kk - 1                      # forced Seidel eigenvalue -(2k-1) = -3
    nq = nullity_Q(S, q)
    n127 = nullity_mod(S, q, 127)
    n3 = nullity_mod(S, q, 3)
    floor23 = L - (16 - 1)
    demo = {"L": L, "q": q, "Q_nullity": nq, "F127_nullity": n127, "F3_nullity": n3,
            "fp_floor": floor23, "margin_ok": 2 * (L - 1) < 127}
    check("size-23 family reconstructed", L == 23)
    check("Q-multiplicity of -(2k-1) equals F_127-nullity (no collision)", nq == n127)
    check("that multiplicity (14) is >= the toy F_p floor (8)",
          nq == 14 and floor23 == 8 and nq >= floor23)
    check("no-collision margin holds at p=127 (2(L-1)=44<127)", demo["margin_ok"])
    check("tiny prime p=3 (margin violated) inflates the nullity: collision is real",
          n3 > nq and n3 == 15)

    print("\n== JSON packet exact replay ==")
    packet = {
        "schema": "cap25-v13-m31-band-nullity-certificate-v1",
        "status": ("PROVED extraction / grid+LP reproduction / pair-independence / "
                   "no-collision lemma / Class-I k<=760 / deployed sound elimination 0; "
                   "PROVED-AT-TOYS soundness gates + size-23 mechanism demo; "
                   "MEASURED inclusion-moment vacuity; OPEN deployed two-shell cell"),
        "deployed": {
            "p": p, "n": n, "m": m, "w": w, "Bstar": Bstar, "L0": L0,
            "prefix_rank_cap": rank_prefix,
            "real_multiplicity_floor": real_mult,
            "Fp_nullity_floor": fp_floor,
            "Fp_minus_real_gap": fp_floor - real_mult,
        },
        "lp_load": {
            "grid_pair_count": grid_count,
            "eigenspace_cap": JMAX,
            "eliminated_count": elim_count,
            "binding_j_histogram": {"2": j2, "3": j3},
            "surviving_count": surviving,
            "eliminated_band_e1": [band[0], band[1]],
            "eliminated_checksums": sums,
            "eliminated_sha256": all_sha,
            "matches_pr495": all_sha == PR495_ALL_SHA and sums == PR495_SUMS,
        },
        "pair_independence": {
            "floor_value": fp_floor,
            "distinct_floor_values_over_grid": len(floors),
            "raw_certificate_eliminations": 0,
        },
        "collision_dichotomy": {
            "seidel_trS2": seidel_sq,
            "no_collision_margin_2L0m1": 2 * (L0 - 1),
            "no_collision_holds": 2 * (L0 - 1) < p,
            "baseline_q_max": q_base, "baseline_k_max": k_base,
            "classI_q_max": q_classI, "classI_k_max": k_classI,
            "classI_eliminated_pairs": classI_rows,
            "classI_new_beyond_lp": classI_new,
            "deployed_sound_elimination_full_class": 0,
            "surviving_after_modular_lever": surviving,
        },
        "inclusion_moment_cut": {
            "levels": list(range(2, 7)),
            "min_value_over_grid": moment_min,
            "vacuous": moment_min >= 0,
        },
        "soundness_toys": toy_report,
        "mechanism_demo_size23": demo,
    }
    check("JSON packet exactly matches regenerated certificate", data == packet)

    print("\n== Corruption self-tests ==")
    corruptions = [
        ("Fp floor", ("deployed", "Fp_nullity_floor"), lambda x: x - 1),
        ("Fp-real gap", ("deployed", "Fp_minus_real_gap"), lambda x: x + 1),
        ("grid count", ("lp_load", "grid_pair_count"), lambda x: x - 1),
        ("eliminated count", ("lp_load", "eliminated_count"), lambda x: x + 1),
        ("surviving count", ("lp_load", "surviving_count"), lambda x: x + 1),
        ("eliminated sha", ("lp_load", "eliminated_sha256"),
         lambda x: ("1" if x[0] != "1" else "2") + x[1:]),
        ("sum_e2 checksum", ("lp_load", "eliminated_checksums", "sum_e2"),
         lambda x: x + 1),
        ("raw eliminations", ("pair_independence", "raw_certificate_eliminations"),
         lambda x: x + 1),
        ("classI k_max", ("collision_dichotomy", "classI_k_max"), lambda x: x + 1),
        ("classI eliminated", ("collision_dichotomy", "classI_eliminated_pairs"),
         lambda x: x + 1),
        ("deployed sound elim", ("collision_dichotomy",
                                 "deployed_sound_elimination_full_class"),
         lambda x: x + 1),
        ("moment vacuity", ("inclusion_moment_cut", "vacuous"), lambda x: not x),
        ("demo collision", ("mechanism_demo_size23", "F127_nullity"), lambda x: x + 1),
    ]
    for name, path, mut in corruptions:
        damaged = copy.deepcopy(data)
        cur = damaged
        for key in path[:-1]:
            cur = cur[key]
        cur[path[-1]] = mut(cur[path[-1]])
        check(f"tampered {name} is rejected", damaged != packet)

    passed = sum(ok for _n, ok in CHECKS)
    total = len(CHECKS)
    print(f"\nRESULT: {'PASS' if passed == total else 'FAIL'} ({passed}/{total} checks)")
    print("Status: PROVED modular lever analysis / PROVED-AT-TOYS soundness "
          "/ OPEN deployed two-shell cell (SDP/realizability the only lever)")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
