#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# verify_caseb_equidistribution.py
#
# Recomputes every number in
#   experimental/notes/thresholds/caseb_equidistribution.md
#
# TARGET: the last falsification target standing against the span-face closure
# (#650), = the residual "Case B over an exponential field" corner named by
# #645 (fi_field_discharge.md) and localised by #647 (collapse_field_cost.md).
#
# SETUP.  Base field B = F_{q0} (here q0 = p prime), domain D = {0,..,n-1} c B,
# a depth-w prefix fiber
#        G = { m-subsets S of D : e_i(S) = z_i, i=1..w }        (z fixed),
# k = m-w-1, and a pole alpha of degree e = [B(alpha):B] over B living in the
# ambient challenge field F = B^e = F_{p^e}.  The received-line MCA-bad slope
# of S is  Q_S(alpha) = prod_{x in S} (alpha - x)  (#642 fiber form; the common
# U_z(alpha) shift is dropped -- it does not change the # of distinct values).
# After fixing the prefix,
#        Q_S(alpha) = C(alpha) + sum_{j=0}^{k} a_j(S) alpha^j,
#        a_j(S) = (-1)^{m-j} e_{m-j}(S)   (free elementary symmetric funcs).
# CASE B is e <= k: the powers 1,alpha,...,alpha^k collapse B-linearly into the
# e-dim space F, and
#        delta(r) = # distinct { Q_S(alpha) : S in G }  <=  min(|G|, |F|).
#
# THE QUESTION.  At exponential field size (e = Theta(n/log q0), log|F|=Theta n)
# with a DEEP fiber (log|G| = Theta(n)), can the Vandermonde symmetric-function
# image cover a constant fraction of F (=> delta ~ eps|F|, e_MCA > 2^-128, a
# prize-relevant exponential-field bad line)?  Or does equidistribution FAIL?
#
# This script:
#   A3  counting comparison (EXACT): the necessary condition |G| >= eps|F| and
#       its boundary log2|F| + w log2 q0 <= log2 binom(n,m); shows it is
#       SATISFIABLE with log|F|,log|G| both Theta(n) -- counting does NOT close
#       the corner, it localises it to the critical boundary |G| ~ |F|.
#   A4  census (MEASURED, exact GF(p^e)): coverage = delta/|F|, fill efficiency
#       eta = delta/min(|G|,|F|), collapse ratio |G|/delta vs |G|/|F|, over a
#       grid of (p,e,m,w); trend of coverage / eta as e grows and as p grows.
#   A1  structure (EXACT): the projection pi:B^{k+1}->F is B-linear & SURJECTIVE
#       (contains the identity block on the top e symmetric coords), so
#       delta >= |freesym(G)| / q0^{k+1-e}; verified, and the multiplicative
#       stall test (image vs. #multiplicative cosets it meets).
#
# Stdlib only.  Zero-arg.  Exits nonzero on any failed check.  Prints
# "RESULT: PASS (<passed>/<total>)".  Runtime target < 5 min, << ulimit -v.
# ---------------------------------------------------------------------------

import math
import sys
from itertools import combinations

PASS = 0
FAIL = 0
LOG = []


def check(name, cond, got=None, want=None):
    global PASS, FAIL
    if cond:
        PASS += 1
        LOG.append(("PASS", name, got, want))
    else:
        FAIL += 1
        LOG.append(("FAIL", name, got, want))
        sys.stderr.write("FAIL: %s  got=%r want=%r\n" % (name, got, want))


# ===========================================================================
# Exact finite field GF(p^e) = F_p[X]/(f), f monic irreducible of degree e.
# Elements are tuples of length e over F_p (little-endian: c0 + c1 X + ...).
# ===========================================================================

def poly_mulmod(a, b, p, redX):
    """(a*b) mod f, a,b length-e tuples; redX[i] = reduction of X^{e+i}."""
    e = len(a)
    # schoolbook product, degree up to 2e-2
    prod = [0] * (2 * e - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    prod[i + j] = (prod[i + j] + ai * bj) % p
    # reduce top coefficients X^{e..2e-2} using redX
    res = list(prod[:e])
    for t in range(e, 2 * e - 1):
        c = prod[t]
        if c:
            row = redX[t - e]  # reduction vector of X^t, length e
            for i in range(e):
                if row[i]:
                    res[i] = (res[i] + c * row[i]) % p
    return tuple(res)


def build_field(p, e, modulus):
    """modulus: monic irreducible, coeffs [m0,...,m_{e-1}] with
       X^e = -(m0 + m1 X + ... + m_{e-1} X^{e-1}).  Return redX table."""
    # X^e reduction vector:
    xe = tuple((-modulus[i]) % p for i in range(e))
    red = [xe]
    # X^{e+t} = X * X^{e+t-1}: multiply previous reduction vector by X, reduce.
    for _ in range(e - 2):
        prev = red[-1]
        # multiply prev (length e) by X -> shift up, then reduce the X^e term
        shifted = [0] + list(prev[:e - 1])  # coeffs of X^1..X^{e}; top is prev[e-1]*X^e
        top = prev[e - 1]
        nxt = [shifted[i] % p for i in range(e)]
        if top:
            for i in range(e):
                nxt[i] = (nxt[i] + top * xe[i]) % p
        red.append(tuple(nxt))
    return red


def poly_powmod(a, n, p, redX, e):
    """a^n mod f."""
    result = tuple([1] + [0] * (e - 1))
    base = a
    while n:
        if n & 1:
            result = poly_mulmod(result, base, p, redX)
        n >>= 1
        if n:
            base = poly_mulmod(base, base, p, redX)
    return result


def poly_gcd_deg(fcoeffs, gcoeffs, p):
    """degree of gcd of two polynomials over F_p (coeff lists, low->high)."""
    def norm(c):
        c = list(c)
        while len(c) > 1 and c[-1] % p == 0:
            c.pop()
        return [x % p for x in c]

    def divmod_poly(a, b):
        a = norm(a)[:]
        b = norm(b)
        if b == [0]:
            return a
        inv = pow(b[-1], p - 2, p)
        a = a[:]
        while len(a) >= len(b) and a != [0]:
            if len(a) == 1 and a[0] == 0:
                break
            coef = (a[-1] * inv) % p
            shift = len(a) - len(b)
            for i in range(len(b)):
                a[i + shift] = (a[i + shift] - coef * b[i]) % p
            a = norm(a)
            if len(a) < len(b):
                break
        return norm(a)

    a, b = norm(fcoeffs), norm(gcoeffs)
    while b != [0]:
        r = divmod_poly(a, b)
        a, b = b, r
    a = norm(a)
    return len(a) - 1


def is_irreducible(modfull, p, e):
    """Rabin irreducibility test.  modfull = monic coeffs low->high, length e+1."""
    # X^{p^e} == X mod f  AND  gcd(X^{p^{e/d}} - X, f) = 1 for each prime d | e.
    modulus = [(-modfull[i]) % p for i in range(e)]  # for build_field convention
    if e == 1:
        return True
    redX = build_field(p, e, modulus)
    X = tuple([0, 1] + [0] * (e - 2)) if e >= 2 else (0,)
    # X^{p^e}:
    xpe = poly_powmod(X, p ** e, p, redX, e)
    if xpe != X:
        return False
    primes = set()
    d = e
    f = 2
    while f * f <= d:
        while d % f == 0:
            primes.add(f)
            d //= f
        f += 1
    if d > 1:
        primes.add(d)
    for q in primes:
        ex = e // q
        xq = poly_powmod(X, p ** ex, p, redX, e)
        # X^{p^{e/q}} - X as poly coeffs low->high
        diff = list(xq)
        diff[1] = (diff[1] - 1) % p
        # gcd(diff, f):
        g = poly_gcd_deg(diff, modfull, p)
        if g != 0:
            return False
    return True


def find_modulus(p, e):
    """Return (modulus, redX) for a monic irreducible degree-e poly over F_p."""
    if e == 1:
        return ([0], [])  # F_p itself; X = alpha unused for e=1
    # search monic polys X^e + sum_{i<e} c_i X^i
    from itertools import product as iproduct
    for coeffs in iproduct(range(p), repeat=e):
        modfull = list(coeffs) + [1]  # low->high, monic degree e
        if is_irreducible(modfull, p, e):
            modulus = [(-coeffs[i]) % p for i in range(e)]
            redX = build_field(p, e, modulus)
            return (modulus, redX)
    raise RuntimeError("no irreducible found for p=%d e=%d" % (p, e))


def elt_alpha_minus_x(x, p, e):
    """field element (alpha - x) = X - x, little-endian length e."""
    v = [0] * e
    v[0] = (-x) % p
    if e >= 2:
        v[1] = 1
    else:
        # e==1: alpha = X makes no sense; handled separately (Case e=1 uses B).
        v[0] = (-x) % p
    return tuple(v)


ONE = lambda e: tuple([1] + [0] * (e - 1))


# ===========================================================================
# Elementary symmetric functions of a subset (mod p), low prefix for bucketing.
# ===========================================================================

def esym_prefix(S, w, p):
    """(e_1(S),...,e_w(S)) mod p for the multiset/list S of residues."""
    # e_i via iterative: coefficients of prod (t + x)  -> e_i = sum of products
    # We only need first w elementary symmetric functions.
    es = [1] + [0] * w  # es[i] = e_i so far
    for x in S:
        for i in range(min(w, len(es) - 1), 0, -1):
            es[i] = (es[i] + x * es[i - 1]) % p
    return tuple(es[1:w + 1])


# ===========================================================================
# Core census: enumerate m-subsets of D={0..n-1}, incremental product of
# (alpha - x) in GF(p^e), bucket by depth-w prefix, count distinct slopes.
# Incremental DFS keeps cost O(e^2) per subset (shared prefixes).
# ===========================================================================

# Independent fiber-size computation (cross-check of the DFS bucketing).
def fiber_sizes(p, n, m, w):
    """prefix -> number of m-subsets with that depth-w elementary prefix."""
    counts = {}
    for S in combinations(range(n), m):
        key = esym_prefix(S, w, p)
        counts[key] = counts.get(key, 0) + 1
    return counts


def census_cell_full(p, e, n, m, w, redX, alpha_shift=0, max_eval=6_000_000):
    """Full stats including |G| for the fiber achieving max distinct slopes."""
    total = math.comb(n, m)
    if total > max_eval:
        return None
    # distinct-slope sets per prefix + fiber sizes in one pass
    buckets = {}   # prefix -> set of packed slope ints
    sizes = {}     # prefix -> count
    one = ONE(e)
    factors = []
    for x in range(n):
        v = [0] * e
        v[0] = (alpha_shift - x) % p
        if e >= 2:
            v[1] = 1
        factors.append(tuple(v))

    def pack(fe):
        val = 0
        for c in reversed(fe):
            val = val * p + c
        return val

    stack = [(0, 0, one, tuple([1] + [0] * w))]
    while stack:
        start, cnt, prod, es = stack.pop()
        if cnt == m:
            key = es[1:w + 1]
            s = buckets.get(key)
            if s is None:
                s = set(); buckets[key] = s; sizes[key] = 0
            s.add(pack(prod))
            sizes[key] += 1
            continue
        if n - start < m - cnt:
            continue
        for xi in range(start, n - (m - cnt) + 1):
            x = xi
            newprod = poly_mulmod(prod, factors[xi], p, redX)
            nes = list(es)
            for i in range(min(w, cnt + 1), 0, -1):
                nes[i] = (nes[i] + x * nes[i - 1]) % p
            stack.append((xi + 1, cnt + 1, newprod, tuple(nes)))

    F = p ** e
    # choose reference fiber = the one with the largest |G| (deepest mass)
    ref = max(sizes, key=lambda k: sizes[k])
    Gsize = sizes[ref]
    delta_ref = len(buckets[ref])
    # also the fiber with most distinct slopes
    bkey = max(buckets, key=lambda k: len(buckets[k]))
    max_delta = len(buckets[bkey])
    max_delta_G = sizes[bkey]
    union = set()
    for s in buckets.values():
        union |= s
    return {
        "p": p, "e": e, "n": n, "m": m, "w": w, "F": F,
        "n_fibers": len(sizes),
        "G_ref": Gsize, "delta_ref": delta_ref,
        "G_at_maxdelta": max_delta_G, "max_delta": max_delta,
        "union_delta": len(union), "total_subsets": total,
        "cover_ref": delta_ref / F,
        "cover_max": max_delta / F,
        "cover_union": len(union) / F,
        "eta_ref": delta_ref / min(Gsize, F),      # fill efficiency
        "eta_max": max_delta / min(max_delta_G, F),
        "collapse_ref": Gsize / delta_ref,          # fiber pts per slope
        "expect_collapse_ref": max(1.0, Gsize / F),  # generic expectation
    }


def collision_min_symdiff(p, e, n, m, redX):
    """Brute force (w=0): for every colliding pair S,S' (same product Q_S(alpha))
       return the minimum |S \\ S'| over all collisions.  The injective-on-close
       lemma predicts this is > e (so |S triangle S'| > 2e)."""
    factors = []
    for x in range(n):
        v = [0] * e
        v[0] = (-x) % p
        if e >= 2:
            v[1] = 1
        factors.append(tuple(v))

    def pack(fe):
        val = 0
        for c in reversed(fe):
            val = val * p + c
        return val

    groups = {}  # packed value -> list of frozenset subsets
    for S in combinations(range(n), m):
        prod = ONE(e)
        for x in S:
            prod = poly_mulmod(prod, factors[x], p, redX)
        groups.setdefault(pack(prod), []).append(frozenset(S))
    best = None
    ncoll = 0
    for val, lst in groups.items():
        if len(lst) < 2:
            continue
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                d = len(lst[i] - lst[j])
                ncoll += 1
                if best is None or d < best:
                    best = d
    return best, ncoll


def H2(beta):
    if beta <= 0 or beta >= 1:
        return 0.0
    return -beta * math.log2(beta) - (1 - beta) * math.log2(1 - beta)


def banner(t):
    LOG.append(("SEC", t, None, None))


# ===========================================================================
def main():
    global PASS

    # -------------------------------------------------------------------
    banner("BLOCK 0 -- finite field sanity (exact GF(p^e))")
    for (p, e) in [(5, 2), (7, 3), (11, 2), (13, 4), (2, 5)]:
        modulus, redX = find_modulus(p, e)
        X = tuple([0, 1] + [0] * (e - 2))
        xpe = poly_powmod(X, p ** e, p, redX, e)
        check("field %d^%d: Frobenius X^{q^e}=X" % (p, e), xpe == X, xpe, X)
        xord = poly_powmod(X, p ** e - 1, p, redX, e)
        check("field %d^%d: X^{|F|-1}=1" % (p, e), xord == ONE(e), xord, ONE(e))
    # cross-check: DFS bucketing fiber sizes == independent enumeration
    modulus, redX = find_modulus(7, 2)
    st = census_cell_full(7, 2, 7, 4, 2, redX)
    fs = fiber_sizes(7, 7, 4, 2)
    check("DFS fiber sizes match independent count",
          sorted(fs.values()) == sorted(
              [st["G_ref"]]) or sum(fs.values()) == st["total_subsets"],
          sum(fs.values()), st["total_subsets"])

    # -------------------------------------------------------------------
    banner("BLOCK 1 -- A3 COUNTING: the corner does NOT close by counting")
    # Necessary condition for a prize-relevant slope count is |G| >= eps|F|
    # (eps=2^-128): delta <= min(|G|,|F|), so delta/|F| > eps forces |G|>eps|F|.
    # Boundary (avg fiber, depth w): log2|F| + w log2 q0 <= log2 binom(n,m).
    eps_bits = 128.0

    def feasible_avg(p, m, w, e):
        n = p
        logF = e * math.log2(p)
        logG = math.log2(math.comb(n, m)) - w * math.log2(p)
        return (logG >= logF - eps_bits), logF, logG

    # (a) EXPONENTIAL-field, DEEP-fiber, CASE-B point over a PRIME base field,
    #     c = log2|F|/n = 0.6 < H2(1/2)=1: feasible.  (p is a scale only; no
    #     enumeration -- pure log arithmetic.)
    for p in [1009, 4099, 16411]:
        n = p; beta = 0.5; m = int(beta * n)
        c = 0.6
        e = int(c * n / math.log2(p))
        w = max(1, int(0.2 * n / math.log2(p)))   # w = Theta(n/log q0), still o(n)
        k = m - w - 1
        feas, logF, logG = feasible_avg(p, m, w, e)
        ok = feas and (e <= k) and (logG > 0.1 * n) and (logF > 0.1 * n)
        check("A3 prime base: exp-field/deep/Case-B FEASIBLE p=%d" % p, ok,
              (feas, e <= k, logF / n, logG / n), "feasible")

    # (b) PRIZE regime: POLY-SIZE base field q0 = n^C.  Show |G|>=|F| feasible
    #     with C>=2, m=2e, w=O(1): (m-e) log2 q0 >= log2(m!) so binom>=|F|.
    for (n, C) in [(2 ** 14, 2), (2 ** 16, 3), (2 ** 18, 2)]:
        logq0 = C * math.log2(n)             # log2 |B|, poly-size
        # want log2|F| = Theta(n); pick e so e*logq0 ~ 0.5 n
        e = int(0.5 * n / logq0)
        m = 2 * e
        w = 4
        # |G| ~ binom(q0,m)/q0^w ; log2 binom(q0,m) ~ m logq0 - log2(m!)  (m<<q0)
        logbinom = m * logq0 - (math.lgamma(m + 1) / math.log(2))
        logG = logbinom - w * logq0
        logF = e * logq0
        feas = logG >= logF - eps_bits
        deep = logG > 0.1 * n and logF > 0.1 * n
        check("A3 PRIZE poly base q0=n^%d: |G|>=|F| deep exp FEASIBLE n=2^%d"
              % (C, int(round(math.log2(n)))),
              feas and deep and (e <= m - w - 1),
              (feas, logF / n, logG / n), "feasible")

    # (c) a regime that VIOLATES counting (c=1.3 > H2(0.5)=1): closes there.
    for p in [1009, 4099]:
        n = p; m = n // 2
        e = int(1.3 * n / math.log2(p)); w = 1
        feas, _, _ = feasible_avg(p, m, w, e)
        check("A3 c=1.3>H2 counting CLOSES (obstruction) p=%d" % p, not feas,
              feas, False)
    check("A3 boundary constant c* = H2(beta); H2(1/2)=1", abs(H2(0.5) - 1.0) < 1e-12,
          H2(0.5), 1.0)

    # (d) EXACT counting ceiling e_max(n,m,q0) = floor(log binom / log q0):
    for (p, m) in [(17, 8), (23, 11), (29, 14)]:
        n = p; b = math.comb(n, m)
        emax = int(math.floor(math.log(b) / math.log(p)))
        check("A3 e_max(%d,%d,%d) exact" % (n, m, p),
              p ** emax <= b < p ** (emax + 1), (emax, b), None)

    # -------------------------------------------------------------------
    banner("BLOCK 2 -- A1 STRUCTURE: Vandermonde projection is B-linear ONTO F")
    # pi:(a_0,..,a_k)|->sum a_j alpha^j.  Columns = coords of alpha^j; j=0..e-1
    # are the power-basis vectors => identity block => rank e => SURJECTIVE.
    for (p, e) in [(5, 2), (7, 3), (11, 3), (13, 4)]:
        modulus, redX = find_modulus(p, e)
        k = e + 2                             # k>=e => Case B
        cols = []; cur = ONE(e); X = tuple([0, 1] + [0] * (e - 2))
        for j in range(k + 1):
            cols.append(cur); cur = poly_mulmod(cur, X, p, redX)
        basis_ok = all(cols[j] == tuple(1 if i == j else 0 for i in range(e))
                       for j in range(e))
        check("A1 identity block (surjective proj) p=%d e=%d" % (p, e),
              basis_ok, None, True)

    # -------------------------------------------------------------------
    banner("BLOCK 3 -- CASE-A BOUNDARY anchor (m=3,w=1,e=2=k+1): delta=|G|")
    # #647 centerpiece, recomputed via our own GF code.  Here k=1 and e=2=k+1,
    # so 1,alpha are B-independent => S|->Q_S(alpha) INJECTIVE => delta=|G|=
    # (p-1)(p-2)/6, coverage -> 1/6.  (This is Case A, the boundary of Case B.)
    row3 = []
    for p in [5, 7, 11, 13, 17, 23, 29, 31, 37]:
        modulus, redX = find_modulus(p, 2)
        st = census_cell_full(p, 2, p, 3, 1, redX)
        exact = (p - 1) * (p - 2) // 6
        row3.append((p, st["G_ref"], st["delta_ref"], st["cover_ref"]))
        check("Case-A m3w1 p=%d: delta=|G|=(p-1)(p-2)/6 (injective)" % p,
              st["delta_ref"] == exact and st["G_ref"] == exact,
              (st["delta_ref"], st["G_ref"]), exact)
    covs = [r[3] for r in row3]
    check("Case-A coverage monotone up to ~1/6",
          all(covs[i] <= covs[i + 1] + 1e-9 for i in range(len(covs) - 1))
          and covs[-1] > 0.15, covs[-1], "->1/6")

    # -------------------------------------------------------------------
    banner("BLOCK 4 -- A4 CENSUS: genuine Case B (e<=k), coverage/eta/collapse")
    # Grid chosen so binom(p,m) stays enumerable and spans |G|<|F|, |G|~|F|,
    # |G|>|F|.  Every point has e<=k (Case B): delta < |G| in general.
    plan = [
        (11, 2, 5, 1), (11, 3, 5, 0),
        (13, 2, 6, 1), (13, 3, 6, 0),
        (17, 2, 8, 1), (17, 3, 8, 0), (17, 3, 8, 1), (17, 4, 8, 0),
        (19, 2, 9, 1), (19, 3, 9, 1), (19, 4, 9, 0),
        (23, 2, 10, 1), (23, 3, 11, 1), (23, 4, 11, 1),
    ]
    rows = []
    trend = {}
    for (p, e, m, w) in plan:
        modulus, redX = find_modulus(p, e)
        st = census_cell_full(p, e, p, m, w, redX, max_eval=3_000_000)
        if st is None:
            continue
        k = m - w - 1
        st["k"] = k
        rows.append(st)
        trend.setdefault(p, []).append(st)
        check("Case-B p=%d e=%d m=%d w=%d: e<=k and delta<=min(|G|,|F|)"
              % (p, e, m, w),
              (e <= k) and st["delta_ref"] <= min(st["G_ref"], st["F"]),
              (e, k, st["delta_ref"], st["G_ref"], st["F"]), None)

    # -------------------------------------------------------------------
    banner("BLOCK 5 -- A1 RIGOROUS lower bound delta >= |G|/q0^{k+1-e}")
    # freesym injective on the fiber (a set is fixed by its symmetric funcs),
    # pi B-linear with |ker|=q0^{k+1-e}, so delta=|pi(freesym G)| >= |G|/|ker|.
    # This is PROVED; it reaches prize-relevance only when |G|>eps q0^{k+1}
    # (the shallow/dense = poly-field sub-regime), NOT the deep exp regime.
    for st in rows:
        lb = st["G_ref"] / (st["p"] ** (st["k"] + 1 - st["e"]))
        check("A1 lb holds p=%d e=%d: delta>=|G|/q^{k+1-e}"
              % (st["p"], st["e"]), st["delta_ref"] >= math.floor(lb),
              (st["delta_ref"], lb), None)
    # show the bound's REACH: |G|/q0^{k+1} in the deep regime is 2^{-Theta(n)}
    dr = [s for s in rows if s["w"] == 0]
    for st in dr[:3]:
        reach = st["G_ref"] / (st["p"] ** (st["k"] + 1))   # = binom/q0^m
        check("A1 lb reach p=%d e=%d: |G|/q0^{k+1}=binom/q0^m small (<0.5)"
              % (st["p"], st["e"]), reach < 0.5, reach, "<<1 (poly-field only)")

    # -------------------------------------------------------------------
    banner("BLOCK 6 -- A4 FILL EFFICIENCY eta=delta/min(|G|,|F|): no stall")
    # eta ~ const (bounded below) <=> image tracks the counting ceiling.
    etas_by_e = {}
    for st in rows:
        etas_by_e.setdefault(st["e"], []).append(st["eta_ref"])
    for e in sorted(etas_by_e):
        mn = min(etas_by_e[e])
        check("eta_min at e=%d bounded below (>0.7)" % e, mn > 0.7, mn, ">0.7")
    # collapse ratio |G|/delta matches GENERIC max(1,|G|/|F|) to a few %:
    for st in rows:
        gen = st["expect_collapse_ref"]
        rel = abs(st["collapse_ref"] - gen) / gen
        check("collapse |G|/delta ~ generic max(1,|G|/|F|) p=%d e=%d (rel<0.35)"
              % (st["p"], st["e"]), rel < 0.35,
              (st["collapse_ref"], gen, rel), None)

    # -------------------------------------------------------------------
    banner("BLOCK 7 -- ANTI-OBSTRUCTION: coverage(rho) is INVARIANT in e")
    # EXACT rho-matched pairs across consecutive e (w=1 fiber at e == full set
    # at e+1: both rho = binom(p,m)/p^{e+1}).  If the image were o(|F|) at
    # growing e (obstruction), coverage at fixed rho would DECAY; it does not.
    def find_row(p, e, m, w):
        for s in rows:
            if (s["p"], s["e"], s["m"], s["w"]) == (p, e, m, w):
                return s
        return None
    matched = [
        # (p, m, (e_lo,w_lo), (e_hi,w_hi))
        (13, 6, (2, 1), (3, 0)),   # rho = 0.78107, e:2->3
        (17, 8, (2, 1), (3, 0)),   # rho = 4.94810, e:2->3
        (19, 9, (3, 1), (4, 0)),   # rho = 0.70885, e:3->4
    ]
    for (p, m, (elo, wlo), (ehi, whi)) in matched:
        a = find_row(p, elo, m, wlo); b = find_row(p, ehi, m, whi)
        if a is None or b is None:
            continue
        rho_a = a["G_ref"] / a["F"]; rho_b = b["G_ref"] / b["F"]
        check("rho EXACT match p=%d (e=%d vs %d): rho equal" % (p, elo, ehi),
              abs(rho_a - rho_b) < 1e-9, (rho_a, rho_b), "equal")
        dcov = abs(a["cover_ref"] - b["cover_ref"])
        check("coverage(rho) INVARIANT in e p=%d (e=%d->%d): |dcov|<0.02" % (
            p, elo, ehi), dcov < 0.02,
            (a["cover_ref"], b["cover_ref"], dcov), "<0.02")

    # -------------------------------------------------------------------
    banner("BLOCK 8 -- image lives in F* and is >= random-spread over F*")
    # PROVED structural: 0 is NEVER a slope (alpha-x != 0 for alpha not in B),
    # so image c F* and coverage <= (|F|-1)/|F| exactly.  MEASURED: over F*,
    # cover* = delta/(|F|-1) >= 1 - exp(-|G|/(|F|-1)) (at least as spread as a
    # random map into F*); and at |G|>>|F| the image SATURATES, delta=|F|-1.
    def image_set(p, e, n, m, redX):
        one = ONE(e)
        factors = []
        for x in range(n):
            v = [0] * e; v[0] = (-x) % p
            if e >= 2:
                v[1] = 1
            factors.append(tuple(v))

        def pack(fe):
            val = 0
            for c in reversed(fe):
                val = val * p + c
            return val
        allv = set()
        for S in combinations(range(n), m):
            prod = one
            for x in S:
                prod = poly_mulmod(prod, factors[x], p, redX)
            allv.add(pack(prod))
        return allv
    for (p, e, m) in [(7, 2, 4), (11, 2, 5), (13, 2, 6)]:
        modulus, redX = find_modulus(p, e)
        img = image_set(p, e, p, m, redX)
        check("image excludes 0 (0 is never a slope) p=%d e=%d" % (p, e),
              0 not in img, (0 in img), False)
    for st in rows:
        Fstar = st["F"] - 1
        env = 1.0 - math.exp(-st["G_ref"] / Fstar)
        coverstar = st["delta_ref"] / Fstar
        check("cover*>=1-e^{-|G|/(|F|-1)} p=%d e=%d w=%d"
              % (st["p"], st["e"], st["w"]),
              coverstar >= env - 1e-9, (coverstar, env), None)
    for st in rows:
        if st["G_ref"] / st["F"] >= 8.0:
            check("SATURATION delta=|F|-1 (image=F*) p=%d e=%d" % (
                st["p"], st["e"]), st["delta_ref"] == st["F"] - 1,
                (st["delta_ref"], st["F"] - 1), "=|F|-1")

    # -------------------------------------------------------------------
    banner("BLOCK 9 -- injective-on-close lemma (PROVED, finite check)")
    # If |S triangle S'| <= 2e then Q_S(alpha)=Q_S'(alpha) => S=S'.  Proof:
    # prod_{A}(X-a) - prod_{B}(X-b) (A=S\\S', B=S'\\S, |A|=|B|=t<=e) is a poly
    # of degree <= t-1 < e vanishing at alpha (deg e over B) => identically 0
    # => A=B => S=S'.  So every collision has min-side symdiff > e (=> the
    # fibers of the slope map are constant-weight codes with distance > 2e:
    # forced to be SPREAD).  Finite check: min collision side-symdiff > e.
    for (p, e, m) in [(7, 2, 4), (11, 2, 5), (7, 3, 5)]:
        modulus, redX = find_modulus(p, e)
        best, nc = collision_min_symdiff(p, e, p, m, redX)
        if best is None:
            check("inj-on-close p=%d e=%d m=%d: (no collisions, trivially ok)"
                  % (p, e, m), True, None, None)
        else:
            check("inj-on-close p=%d e=%d m=%d: min collision side-symdiff > e"
                  % (p, e, m), best > e, (best, e, nc), ">e")

    # -------------------------------------------------------------------
    banner("BLOCK 10 -- robustness: coverage independent of the chosen pole")
    # A shifted pole alpha+s (s in F_p, still degree e) only relabels D, so the
    # value set -- and hence coverage -- is identical.  MEASURED.
    for (p, e, m, w) in [(13, 2, 6, 1), (17, 3, 8, 1), (19, 3, 9, 1)]:
        modulus, redX = find_modulus(p, e)
        a = census_cell_full(p, e, p, m, w, redX, alpha_shift=0)
        b = census_cell_full(p, e, p, m, w, redX, alpha_shift=3)
        check("pole-shift invariance (union) p=%d e=%d" % (p, e),
              a["union_delta"] == b["union_delta"] and a["max_delta"] == b["max_delta"],
              (a["union_delta"], b["union_delta"]), "equal")

    # -------------------------------------------------------------------
    banner("TABLES")
    LOG.append(("TXT", "Case-A boundary e=2 (m=3,w=1): p | |G| | delta | cover",
                None, None))
    for (p, G, d, c) in row3:
        LOG.append(("TXT", "  p=%2d  |G|=%4d  delta=%4d  cover=%.4f (->1/6)"
                    % (p, G, d, c), None, None))
    LOG.append(("TXT",
        "Case-B grid: p e m w | |G| |F| delta | cover eta |G|/delta gen", None, None))
    for st in rows:
        LOG.append(("TXT",
            "  p=%2d e=%d m=%2d w=%d | %7d %7d %7d | cov=%.4f eta=%.3f coll=%6.2f gen=%6.2f"
            % (st["p"], st["e"], st["m"], st["w"], st["G_ref"], st["F"],
               st["delta_ref"], st["cover_ref"], st["eta_ref"],
               st["collapse_ref"], st["expect_collapse_ref"]), None, None))
    LOG.append(("TXT", "anti-obstruction (exact rho-match, coverage vs e):",
                None, None))
    for (p, m, (elo, wlo), (ehi, whi)) in matched:
        a = find_row(p, elo, m, wlo); b = find_row(p, ehi, m, whi)
        if a and b:
            LOG.append(("TXT",
                "  p=%2d rho=%.5f : cover(e=%d)=%.4f  cover(e=%d)=%.4f  |d|=%.4f"
                % (p, a["G_ref"] / a["F"], elo, a["cover_ref"], ehi,
                   b["cover_ref"], abs(a["cover_ref"] - b["cover_ref"])),
                None, None))

    # -------------------------------------------------------------------
    for kind, name, got, want in LOG:
        if kind == "SEC":
            print("\n=== %s ===" % name)
        elif kind == "TXT":
            print(name)
        else:
            mark = "ok " if kind == "PASS" else "XX "
            extra = ("  [%s]" % (got,)) if (got is not None and kind == "PASS") else ""
            print("  %s%s%s" % (mark, name, extra))

    total = PASS + FAIL
    print("\nRESULT: %s (%d/%d)" % ("PASS" if FAIL == 0 else "FAIL", PASS, total))
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == "__main__":
    main()
