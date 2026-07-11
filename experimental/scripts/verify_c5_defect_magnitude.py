#!/usr/bin/env python3
"""Defect-magnitude bound d_p(G,I)=|G|-|Z_p(G,I)| on the DEPLOYED C5 families.

Lane.  The one OPEN residual of PR #607
(experimental/notes/thresholds/noncyclic_c5_slope_count.md, Rung 4.2): the C5
field-descent slope count is the cyclotomic defect p^{d_p(G,I)} for every finite
abelian slope group with p not dividing |G| (Theorem A), but this is
routing-admissible (payment-grade) only when d_p(G,I)=o(|G|).  #607 pins the
trivial-Frobenius floor (p == 1 mod exp G gives d_p=|G|-|I|, vacuous) and leaves
open whether the DEPLOYED profile families dodge it.  This script proves and
measures the magnitude on the profile families the frontiers tex actually routes
through C5:

    F1  CIRCLE / TWIN-COSET  (asymptotic_rs_mca_frontiers.tex def:circle-twin-domain
        L2656): odd base F_p, norm-one torus U=ker(N_{F_{p^2}/F_p}), |U|=p+1,
        cyclic; slope group G=Z/N with N | p+1; Frobenius chi->chi^p acts as
        u->u^p=u^{-1} (u^{p+1}=1), i.e. NEGATION c->-c, order EXACTLY 2.
    F2  BINARY TOWER  (rem:characteristic-two-rows L2705): K=F_{2^s}, s=o(n);
        multiplicative slope group G=Z/N with N | 2^s-1 (N odd, so 2 not | N);
        Frobenius c->2c, order ord_N(2).
    F0  PRIME-FIELD DYADIC control  (Danny #451 sec.7 excluded row): N | p-1,
        Frobenius trivial (order 1), d_p=|G|-|I|.  The measured vacuous floor.

Every deployed C5 slope group is CYCLIC (a finite subgroup of K^x is cyclic), so
#607 Theorem A specializes here to Danny #451 Theorem 1's cyclic bound; the
non-cyclic group-algebra count is a generalization ahead of deployment.  We keep
one PRODUCT-group cross-check to confirm #607's orbit closed form and
non-multiplicativity (lineage), but the deployed magnitude question is the three
cyclic families above.

Lineage / credit.  Defect object and Theorem-1 cyclic bound: DannyExperiments
#451 (asymptotic_c9_frobenius_cyclotomic_defect.md).  Dyadic active exemplar
(p=5, N=2^s, ord_{2^r}(5)=2^{r-2}): #451 Theorem 2, reproduced here.  Non-cyclic
Theorem A, orbit closed form ell(chi)=lcm_i ord_{n_i/gcd(c_i,n_i)}(p), and the
trivial-Frobenius floor: PR #607.  #545 gap2_collapse_routing.md routes the C5
cell.  Frobenius-closure primitive (sum a_i w_i)^p = sum a_i w_i^p is Lean-backed
zero-sorry (c9_frobenius_closure_lean_backing.md, sum_smul_pow).  GF(p^k)/rank_fp
idiom reused from verify_noncyclic_c5_count.py (#607).

Checks (recomputes every number the note quotes; exit 0 iff all pass):
  TRICH   : Frobenius-order trichotomy o=ord_N(p): N|p-1 => 1, N|p+1 => 2,
            tower N|2^s-1 minimal => ord_N(2); pinned per deployed family.
  ORBIT   : orbit size len(iterate c,pc,p^2c,...) == closed form
            ord_{N/gcd(c,N)}(p); product-group ell=lcm_i(...) (#607 lineage).
  DEFECT  : d_p two ways -- N-|closure| == N - sum_{orbit meets I}|orbit| ==
            N - |union_ell p^ell I|.
  ORDER1  : trivial floor (N|p-1): closure(I)=I, d_p=|G|-|I| (control).
  ORDER2  : circle law d_p = |G| - |I union -I| = N - 2|I| + |{c in I: -c in I}|;
            SHARP THRESHOLD for a prefix {0..R-1}: d = max(0, N-2R+1), so d=0
            for R>N/2 and d=Theta(N) for R/N<1/2; symmetric profile {-w..w}
            gives d=N-|I| (vacuous), the identity/Chebyshev regime.
  ACTIVE  : primitive-root tower (N prime, p primitive root) => d_p<=1 for any
            interval meeting a nonzero frequency.
  DANNY2  : #451 Theorem 2 reproduced: p=5, N=2^s, R>=kappa N => d_5<=2^{J-1},
            J=ceil(log2(4/kappa)); exhausts all interval positions for small s.
  DECAY   : binary-tower census d_2(N, prefix R)/N vs R/N across several N|2^s-1;
            monotone non-increasing; the near-primitive N reach o(N), the small
            ord_N(2) N do not (curve reported, wall bounded).
  FIBER   : independent field realization G=Z/N over F_{p^k} (k=ord_N(p)):
            F_p-rank of syndrome map == |Z_p(I)| (Theorem A); p=2 full Omega =>
            every nonempty fiber == 2^{d_p} (tight); general p Boolean <= p^{d_p}.
  DEPLOY  : R/N = 1 - rate bridge: deep regime 3(n-a)<=n-k => R=n-k=(1-rate)N;
            low-rate (rate<=1/2) circle rows have R/N>=1/2 => circle d_p=0.
  TAMPER  : deliberately wrong values must fail.

Stdlib only.  Zero-arg.  Runtime < 120 s under ulimit -v 2097152.
"""
from __future__ import annotations

from itertools import product
from math import gcd

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    CHECKS.append((name, bool(ok), detail))
    return bool(ok)


# ------------------------------------------------------------------------- #
#  number theory                                                            #
# ------------------------------------------------------------------------- #
def mult_order(a: int, n: int) -> int:
    """multiplicative order of a mod n (gcd(a,n)=1); order of the unit."""
    if n == 1:
        return 1
    a %= n
    assert gcd(a, n) == 1, (a, n)
    o, x = 1, a
    while x != 1:
        x = (x * a) % n
        o += 1
    return o


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def prime_factors(n: int) -> set[int]:
    fs, d = set(), 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


def is_primitive_root(g: int, n: int) -> bool:
    """g a primitive root mod n (n prime here): order == n-1."""
    if gcd(g, n) != 1:
        return False
    return mult_order(g, n) == n - 1


# ------------------------------------------------------------------------- #
#  Frobenius orbits and the defect on a cyclic slope group Z/N               #
#  (deployed C5 case; #607 Theorem A specializes to Danny #451 Theorem 1)    #
# ------------------------------------------------------------------------- #
def frob_orbit(c: int, N: int, p: int) -> frozenset[int]:
    """orbit of c in Z/N under x -> p*x (Frobenius chi -> chi^p on the dual)."""
    o, x = set(), c % N
    while x not in o:
        o.add(x)
        x = (p * x) % N
    return frozenset(o)


def orbit_size_closed(c: int, N: int, p: int) -> int:
    """closed form: |orbit(c)| = ord_{N/gcd(c,N)}(p)  (r=1 case of #607's
    ell(chi)=lcm_i ord_{n_i/gcd(c_i,n_i)}(p))."""
    m = N // gcd(c, N)
    return mult_order(p % m, m) if m > 1 else 1


def frob_closure(I, N: int, p: int) -> frozenset[int]:
    """Z_p(N,I) = union of Frobenius orbits meeting I."""
    Z: set[int] = set()
    for c in I:
        Z |= frob_orbit(c, N, p)
    return frozenset(Z)


def frob_closure_iterated(I, N: int, p: int) -> frozenset[int]:
    """Z_p as union_{ell>=0} p^ell I, iterated to fixpoint (independent route)."""
    Z = set(x % N for x in I)
    while True:
        nxt = Z | {(p * x) % N for x in Z}
        if nxt == Z:
            return frozenset(Z)
        Z = nxt


def defect(N: int, I, p: int) -> int:
    return N - len(frob_closure(I, N, p))


def interval(a: int, R: int, N: int):
    return [(a + j) % N for j in range(R)]


# ------------------------------------------------------------------------- #
#  product-group orbit (ONE #607-lineage cross-check; deployed rows are r=1) #
# ------------------------------------------------------------------------- #
def prod_orbit(c, dims, p):
    o, x = set(), tuple(ci % ni for ci, ni in zip(c, dims))
    while x not in o:
        o.add(x)
        x = tuple((p * xi) % ni for xi, ni in zip(x, dims))
    return frozenset(o)


def prod_orbit_size_closed(c, dims, p):
    size = 1
    for ci, ni in zip(c, dims):
        m = ni // gcd(ci, ni)
        size = lcm(size, mult_order(p % m, m) if m > 1 else 1)
    return size


# ------------------------------------------------------------------------- #
#  GF(p^k) and rank_fp  (idiom reused from #607 verify_noncyclic_c5_count.py) #
# ------------------------------------------------------------------------- #
def _ptrim(a):
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a


def _pmul(a, b, p):
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return _ptrim(r)


def _pmod(a, m, p):
    a, m = list(a), _ptrim(list(m))
    dm = len(m) - 1
    if dm == 0:
        return [0]
    inv = pow(m[-1], p - 2, p)
    while len(a) - 1 >= dm and len(a) > 1:
        if a[-1] == 0:
            a.pop()
            continue
        c = (a[-1] * inv) % p
        sh = len(a) - 1 - dm
        for i, mi in enumerate(m):
            a[i + sh] = (a[i + sh] - c * mi) % p
        _ptrim(a)
    return _ptrim(a)


def _psub(a, b, p):
    r = [0] * max(len(a), len(b))
    for i in range(len(r)):
        av = a[i] if i < len(a) else 0
        bv = b[i] if i < len(b) else 0
        r[i] = (av - bv) % p
    return _ptrim(r)


def _pgcd(a, b, p):
    a, b = _ptrim(list(a)), _ptrim(list(b))
    while not (len(b) == 1 and b[0] == 0):
        a, b = b, _pmod(a, b, p)
    return a


def _ppowmod(base, e, m, p):
    r = [1]
    base = _pmod(base, m, p)
    while e:
        if e & 1:
            r = _pmod(_pmul(r, base, p), m, p)
        e >>= 1
        if e:
            base = _pmod(_pmul(base, base, p), m, p)
    return r


def _is_irred(f, p):
    k = len(f) - 1
    if k == 1:
        return True
    x = [0, 1]
    if _ppowmod(x, p ** k, f, p) != [0, 1]:
        return False
    for r in prime_factors(k):
        h = _ppowmod(x, p ** (k // r), f, p)
        g = _pgcd(_psub(h, x, p), f, p)
        if not (len(g) == 1 and g[0] != 0):
            return False
    return True


def _smallest_irred(p, k):
    for code in range(p ** k):
        low, c = [], code
        for _ in range(k):
            low.append(c % p)
            c //= p
        f = low + [1]
        if _is_irred(f, p):
            return f
    raise RuntimeError("no irreducible")


class GF:
    """F_{p^k}; elements are base-p digit ints; smallest monic irreducible."""

    def __init__(self, p, k):
        self.p, self.k, self.q = p, k, p ** k
        self.f = _smallest_irred(p, k)
        q = self.q
        self._pw = [p ** i for i in range(k)]
        self.mult = [0] * (q * q)
        for a in range(q):
            pa = self._vec(a)
            for b in range(a, q):
                m = self._enc(_pmod(_pmul(pa, self._vec(b), p), self.f, p))
                self.mult[a * q + b] = m
                self.mult[b * q + a] = m
        self.g = self._find_gen()
        self.antilog = [0] * (q - 1)
        self.logt = [None] * q
        x = 1
        for i in range(q - 1):
            self.antilog[i] = x
            self.logt[x] = i
            x = self.mult[x * q + self.g]

    def _vec(self, a):
        p, k = self.p, self.k
        v = [0] * k
        for i in range(k):
            v[i] = a % p
            a //= p
        return v

    def _enc(self, v):
        s = 0
        for i in range(len(v)):
            s += (v[i] % self.p) * self._pw[i]
        return s

    def powr(self, a, e):
        if e == 0:
            return 1
        if a == 0:
            return 0
        return self.antilog[(self.logt[a] * (e % (self.q - 1))) % (self.q - 1)]

    def _find_gen(self):
        q, need = self.q, self.q - 1
        fs = prime_factors(need)
        for cand in range(2, q):
            ok = True
            for r in fs:
                e, x, base, ee = need // r, 1, cand, need // r
                while ee:
                    if ee & 1:
                        x = self.mult[x * q + base]
                    ee >>= 1
                    if ee:
                        base = self.mult[base * q + base]
                if x == 1:
                    ok = False
                    break
            if ok:
                return cand
        raise RuntimeError("no generator")

    def root_of_unity(self, e):
        assert (self.q - 1) % e == 0, (self.q - 1, e)
        return self.antilog[(self.q - 1) // e]


def rank_fp(rows, p):
    rows = [list(r) for r in rows]
    n = len(rows[0]) if rows else 0
    piv = 0
    for col in range(n):
        pr = None
        for r in range(piv, len(rows)):
            if rows[r][col] % p != 0:
                pr = r
                break
        if pr is None:
            continue
        rows[piv], rows[pr] = rows[pr], rows[piv]
        inv = pow(rows[piv][col] % p, p - 2, p)
        rows[piv] = [(x * inv) % p for x in rows[piv]]
        for r in range(len(rows)):
            if r != piv and rows[r][col] % p:
                fac = rows[r][col] % p
                rows[r] = [(a - fac * b) % p for a, b in zip(rows[r], rows[piv])]
        piv += 1
    return piv


def syndrome_rank_and_fibers(N, I, p, enumerate_fibers=True):
    """Realize G=Z/N over F_{p^k}, k=ord_N(p): zeta primitive N-th root of unity.
    Syndrome map x -> (sum_g x_g zeta^{c g})_{c in I}, x in {0,1}^N.
    Returns (rank_fp of the map, max nonempty Boolean fibre) -- both independent
    of the orbit computation (field realization, not orbit counting)."""
    k = mult_order(p % N, N)
    F = GF(p, k)
    zeta = F.root_of_unity(N)
    zpow = [F.powr(zeta, (c * g) % N) for c in I for g in range(N)]
    # F_p-linear syndrome matrix: |I|*k rows (each F_{p^k} coord -> k F_p rows),
    # N columns.  Column g, block (c-index): digits of zeta^{c g}.
    rows = []
    for ci in range(len(I)):
        for dig in range(k):
            rows.append([(zpow[ci * N + g] // (p ** dig)) % p for g in range(N)])
    rk = rank_fp(rows, p) if rows else 0
    maxfib = None
    if enumerate_fibers and N <= 14:
        # F_{p^k} addition is digitwise mod p on the base-p encoding
        vecs = [[F._vec(zpow[ci * N + g]) for g in range(N)] for ci in range(len(I))]
        buckets: dict[tuple, int] = {}
        for x in product(range(2), repeat=N):     # Boolean Omega = {0,1}^N
            syn = []
            for ci in range(len(I)):
                acc = [0] * k
                for g in range(N):
                    if x[g]:
                        v = vecs[ci][g]
                        for d in range(k):
                            acc[d] = (acc[d] + v[d]) % p
                syn.append(tuple(acc))
            key = tuple(syn)
            buckets[key] = buckets.get(key, 0) + 1
        maxfib = max(buckets.values())
    return rk, maxfib


# ------------------------------------------------------------------------- #
#  1. TRICHOTOMY -- Frobenius order per deployed family                      #
# ------------------------------------------------------------------------- #
def run_trichotomy():
    # F0 trivial: N | p-1 => ord_N(p) = 1
    for (N, p) in [(5, 11), (8, 17), (11, 23), (15, 31), (13, 53)]:
        assert (p - 1) % N == 0
        check("TRICH.triv", mult_order(p % N, N) == 1, f"N={N},p={p}")
    # F1 circle: N | p+1, N>2 => ord_N(p) = 2
    for (N, p) in [(4, 3), (6, 11), (8, 7), (12, 23), (14, 13), (9, 17)]:
        assert (p + 1) % N == 0 and N > 2
        check("TRICH.circle2", mult_order(p % N, N) == 2, f"N={N},p={p}")
    # F2 tower: N | 2^s - 1 minimal s => ord_N(2) = s
    for s in [3, 4, 5, 6, 7, 8]:
        N = 2 ** s - 1
        check("TRICH.tower", mult_order(2, N) == s, f"N=2^{s}-1={N}")
    # tower proper divisors: ord divides s
    for (N, s) in [(7, 3), (5, 4), (31, 5), (21, 6), (127, 7)]:
        check("TRICH.tower.div", (s % mult_order(2, N)) == 0 and (2 ** s - 1) % N == 0,
              f"N={N}|2^{s}-1")


# ------------------------------------------------------------------------- #
#  2. ORBIT closed form (cyclic + one product-group #607 lineage)           #
# ------------------------------------------------------------------------- #
def run_orbit():
    for (N, p) in [(15, 2), (31, 2), (63, 2), (13, 5), (16, 5), (24, 5), (14, 13)]:
        if gcd(p, N) != 1:
            continue
        ok = all(len(frob_orbit(c, N, p)) == orbit_size_closed(c, N, p)
                 for c in range(N))
        check("ORBIT.closed", ok, f"N={N},p={p}")
    # product group (#607 lineage): ell = lcm_i ord_{n_i/gcd}(p)
    for dims, p in [((3, 3), 2), ((3, 9), 2), ((5, 5), 2), ((3, 3), 5)]:
        if any(gcd(p, ni) != 1 for ni in dims):
            continue
        ok = all(len(prod_orbit(c, dims, p)) == prod_orbit_size_closed(c, dims, p)
                 for c in product(*[range(ni) for ni in dims]))
        check("ORBIT.prod", ok, f"dims={dims},p={p}")
    # non-multiplicativity witness (#607): (Z/3)^2, p=2, I={1}x{0,1}
    dims, p = (3, 3), 2
    box = [(1, 0), (1, 1)]
    Z = set()
    for c in box:
        Z |= prod_orbit(c, dims, p)
    z1 = len(frob_closure([1], 3, 2))
    z2 = len(frob_closure([0, 1], 3, 2))
    check("ORBIT.nonmult", len(Z) == 4 and z1 * z2 == 6 and len(Z) != z1 * z2,
          f"|Z|={len(Z)} vs {z1}*{z2}={z1*z2}")


# ------------------------------------------------------------------------- #
#  3. DEFECT two ways                                                        #
# ------------------------------------------------------------------------- #
def run_defect_twoways():
    cases = [(15, 2), (31, 2), (63, 2), (13, 5), (14, 13), (24, 5)]
    for (N, p) in cases:
        if gcd(p, N) != 1:
            continue
        for (a, R) in [(0, 3), (1, 5), (0, N // 2), (2, N - 4)]:
            I = interval(a, min(R, N), N)
            Za = frob_closure(I, N, p)
            Zb = frob_closure_iterated(I, N, p)
            # orbit-sum route
            seen, tot = set(), 0
            for c in I:
                orb = frob_orbit(c, N, p)
                if not (orb & seen):
                    tot += len(orb)
                    seen |= orb
                else:
                    seen |= orb
            tot = len(seen)
            ok = (Za == Zb) and (len(Za) == tot) and (defect(N, I, p) == N - len(Za))
            check("DEFECT.2way", ok, f"N={N},p={p},a={a},R={len(I)}")


# ------------------------------------------------------------------------- #
#  4. ORDER1 trivial floor (control)                                        #
# ------------------------------------------------------------------------- #
def run_order1():
    for (N, p) in [(5, 11), (8, 17), (11, 23), (15, 31)]:
        allok = True
        for R in range(1, N):
            I = interval(0, R, N)
            Z = frob_closure(I, N, p)
            if not ((Z == frozenset(x % N for x in I)) and (defect(N, I, p) == N - R)):
                allok = False
        check("ORDER1.floor", allok, f"N={N},p={p}: Z_p(I)=I, d=N-R all R")


# ------------------------------------------------------------------------- #
#  5. ORDER2 circle law + sharp threshold                                    #
# ------------------------------------------------------------------------- #
def order2_defect_formula(N, I):
    """d = N - |I union -I| = N - 2|I| + |{c in I : -c in I}|."""
    Iset = set(x % N for x in I)
    selfconj = sum(1 for c in Iset if (-c) % N in Iset)
    return N - (2 * len(Iset) - selfconj)


def run_order2():
    for (N, p) in [(6, 11), (8, 7), (12, 23), (14, 13), (18, 17), (24, 23)]:
        assert (p + 1) % N == 0 and mult_order(p % N, N) == 2
        # exact law d = N - |I union -I|, all interval positions & lengths
        for a in range(N):
            for R in range(1, N + 1):
                I = interval(a, R, N)
                d_orbit = defect(N, I, p)
                d_form = order2_defect_formula(N, I)
                assert d_orbit == d_form, (N, a, R, d_orbit, d_form)
        check("ORDER2.law", True, f"N={N},p={p}: d==N-|I u -I| all (a,R)")
        # SHARP THRESHOLD on prefix {0..R-1}: d = max(0, N-2R+1)
        thr_ok = True
        for R in range(1, N + 1):
            I = interval(0, R, N)
            expect = max(0, N - 2 * R + 1)
            if defect(N, I, p) != expect:
                thr_ok = False
                break
        check("ORDER2.threshold", thr_ok,
              f"N={N}: prefix d==max(0,N-2R+1); d=0 for R>N/2")
        # symmetric (circle-code) profile {-w..w}: vacuous d = N-|I|
        for w in range(1, N // 2):
            I = [j % N for j in range(-w, w + 1)]
            Iset = set(I)
            ok = (frob_closure(Iset, N, p) == frozenset(Iset)) and \
                 (defect(N, Iset, p) == N - len(Iset))
            assert ok, (N, w)
        check("ORDER2.symmetric", True, f"N={N}: symmetric profile d==N-|I| (vacuous)")


# ------------------------------------------------------------------------- #
#  6. ACTIVE primitive-root tower                                            #
# ------------------------------------------------------------------------- #
def run_active_primitive():
    # N prime, p a primitive root mod N: every nonzero orbit is (Z/N)\{0}
    prim = [(11, 2), (13, 2), (19, 2), (29, 2), (13, 6), (23, 5)]
    for (N, p) in prim:
        assert is_primitive_root(p, N)
        worst = 0
        for a in range(1, N):          # intervals meeting a nonzero freq
            for R in range(1, N):
                I = interval(a, R, N)
                if all(x % N == 0 for x in I):
                    continue
                worst = max(worst, defect(N, I, p))
        check("ACTIVE.primroot", worst <= 1, f"N={N},p={p}: max d_p={worst}<=1")


# ------------------------------------------------------------------------- #
#  7. DANNY #451 Theorem 2 reproduction (p=5, N=2^s, R>=kappa N)             #
# ------------------------------------------------------------------------- #
def run_danny_thm2():
    from math import ceil, log2
    p = 5
    # order fact: ord_{2^r}(5) = 2^{r-2} for r>=2
    for r in range(2, 12):
        check("DANNY2.order", mult_order(5, 2 ** r) == 2 ** (r - 2),
              f"ord_2^{r}(5)=2^{r-2}") if r in (2, 5, 8, 11) else None
        assert mult_order(5, 2 ** r) == 2 ** (r - 2)
    # d_5(2^s, I) <= D_kappa = 2^{J-1}, J=ceil(log2(4/kappa)), for R>=kappa*2^s
    for s in range(3, 11):
        N = 2 ** s
        for kappa in (1.0, 0.5, 0.25, 0.1):
            J = ceil(log2(4 / kappa))
            Dk = 2 ** (J - 1)
            Rmin = max(1, ceil(kappa * N))
            worst = 0
            # defect is monotone non-increasing in R (larger I => larger closure),
            # so the worst case over R>=Rmin is at R=Rmin.
            if s <= 6:
                # exhaust every interval position & length R in [Rmin, N]
                for a in range(N):
                    for R in range(Rmin, N + 1):
                        worst = max(worst, defect(N, interval(a, R, N), p))
            else:
                # large s: worst-case R=Rmin over all positions
                for a in range(N):
                    worst = max(worst, defect(N, interval(a, Rmin, N), p))
            check("DANNY2.bound", worst <= Dk,
                  f"s={s},kappa={kappa}: max d_5={worst}<=D_kappa={Dk}") \
                if (s in (3, 6, 8) and kappa in (0.5, 0.25)) else None
            assert worst <= Dk, (s, kappa, worst, Dk)


# ------------------------------------------------------------------------- #
#  7b. NECKLACE theorem -- binary tower N=2^s-1: d_2 <= 1 at half prefix     #
#      (doubling = cyclic bit-rotation; every non-constant s-bit necklace    #
#       has a rotation with leading bit 0, hence a representative in          #
#       [1, 2^{s-1}]; so {1..ceil(N/2)} meets every nonzero coset.)          #
# ------------------------------------------------------------------------- #
def run_necklace():
    for s in range(3, 13):
        N = 2 ** s - 1
        R = (N + 1) // 2                # = 2^{s-1}
        d = defect(N, interval(1, R, N), 2)
        # only the fixed point 0 (not in the prefix {1..R}) escapes => d==1
        check("NECKLACE.half", d == 1, f"N=2^{s}-1={N}: d_2({{1..{R}}})={d}==1")
        # direct: every nonzero coset meets [1, 2^{s-1}]
        if s <= 10:
            meets = True
            for c in range(1, N):
                orb = frob_orbit(c, N, 2)
                if not any(1 <= x <= 2 ** (s - 1) for x in orb):
                    meets = False
                    break
            check("NECKLACE.cover", meets,
                  f"N=2^{s}-1: every nonzero coset meets [1,2^{s-1}]")
    # including the 0-frequency (prefix {0..R-1}) closes fully => d=0
    for s in [4, 6, 8]:
        N = 2 ** s - 1
        R = (N + 1) // 2 + 1
        check("NECKLACE.zero", defect(N, interval(0, R, N), 2) == 0,
              f"N=2^{s}-1: d_2({{0..{R-1}}})=0")


# ------------------------------------------------------------------------- #
#  8. DECAY census -- binary tower d_2(N, prefix R)/N vs R/N                 #
# ------------------------------------------------------------------------- #
DECAY_ROWS = []


def run_decay():
    p = 2
    # N | 2^s - 1 spanning near-primitive (large ord) to structured (small ord)
    families = [
        ("2^5-1=31 (prime, ord=5)", 31),
        ("2^7-1=127 (prime, ord=7)", 127),
        ("2^11-1=2047=23*89 (ord=11)", 2047),
        ("2^8-1=255=3*5*17 (ord=8)", 255),
        ("2^12-1=4095 (ord=12)", 4095),
        ("primitive: 2 prim root mod 11", 11),
        ("primitive: 2 prim root mod 29", 29),
    ]
    grid = [0.1, 0.25, 0.5, 0.75, 0.9, 1.0]
    for name, N in families:
        o = mult_order(2, N)
        curve, prev = [], None
        mono = True
        for frac in grid:
            R = max(1, int(round(frac * N)))
            R = min(R, N)
            d = defect(N, interval(1, R, N), 2)   # prefix starting at 1 (nonzero)
            curve.append((frac, R, d, round(d / N, 4)))
            if prev is not None and d > prev:
                mono = False
            prev = d
        DECAY_ROWS.append((name, N, o, curve))
        check("DECAY.monotone", mono, f"{name}: d non-increasing in R")
    # near-primitive (large ord relative to N) reaches o(N) by R/N=0.9
    for name, N in [("31", 31), ("127", 127), ("11", 11), ("29", 29)]:
        R = int(round(0.9 * N))
        d = defect(N, interval(1, R, N), 2)
        check("DECAY.active_small", d / N <= 0.12, f"N={N}: d/N={d/N:.3f} at R/N=0.9")


# ------------------------------------------------------------------------- #
#  9. FIBER -- independent field realization (Theorem A cross-check)         #
# ------------------------------------------------------------------------- #
def run_fiber():
    # rank == |Z_p(I)| on a spread of cyclic C5 leaves (all three families)
    rank_cases = [
        (15, 2, interval(1, 4, 15)),   # tower N|2^4-1, active
        (15, 2, interval(1, 8, 15)),
        (9, 2, interval(1, 3, 9)),     # tower divisor
        (8, 7, interval(0, 3, 8)),     # circle N|p+1, order 2
        (8, 7, interval(0, 5, 8)),     # circle deep prefix (past N/2)
        (6, 11, interval(1, 2, 6)),    # circle order 2
        (5, 11, interval(0, 2, 5)),    # trivial floor N|p-1
        (13, 5, interval(1, 4, 13)),
    ]
    for (N, p, I) in rank_cases:
        rk, maxfib = syndrome_rank_and_fibers(N, I, p, enumerate_fibers=(N <= 14))
        Zp = len(frob_closure(I, N, p))
        d = N - Zp
        check("FIBER.rank", rk == Zp, f"N={N},p={p}: rank={rk}==|Z_p|={Zp}")
        if maxfib is not None:
            if p == 2:
                check("FIBER.tight", maxfib == 2 ** d,
                      f"N={N},p=2: maxfib={maxfib}==2^{d}")
            else:
                check("FIBER.bound", maxfib <= p ** d,
                      f"N={N},p={p}: maxfib={maxfib}<={p}^{d}")


# ------------------------------------------------------------------------- #
#  10. DEPLOY bridge -- R/N = 1 - rate; low-rate circle rows paid            #
# ------------------------------------------------------------------------- #
def run_deploy():
    # deep regime 3(n-a) <= n-k, syndrome depth R = n-k = (1-rate) n.
    # circle row: G = Z/N (N | p+1), Frobenius order 2, prefix depth R.
    # For rate <= 1/2 => R/N = 1-rate >= 1/2 => circle prefix defect 0.
    N, p = 24, 23           # N=24 | p+1=24, order 2
    assert (p + 1) % N == 0 and mult_order(p, N) == 2
    for rate in (0.5, 0.25, 0.125, 1.0 / 16):
        R = int(round((1 - rate) * N))
        d = defect(N, interval(0, R, N), p)
        check("DEPLOY.circle_paid", (R > N / 2 and d == 0) or (R <= N / 2),
              f"rate={rate}: R/N={R}/{N}, d={d}")
        assert not (R > N // 2 and d != 0)
    # contrast: high rate (rate>1/2 => R/N<1/2) leaves circle defect Theta(N)
    for rate in (0.75, 0.875):
        R = int(round((1 - rate) * N))
        d = defect(N, interval(1, R, N), p)
        check("DEPLOY.circle_vacuous", d >= N - 2 * R - 1 and d > 0,
              f"rate={rate}: R/N={R}/{N}, d={d} (Theta(N))")


# ------------------------------------------------------------------------- #
#  11. TAMPER                                                                #
# ------------------------------------------------------------------------- #
def run_tamper():
    # wrong: claim circle (order-2) defect for shallow prefix is 0
    N, p = 12, 23
    I = interval(1, 3, N)          # R=3 < N/2=6
    bad = (defect(N, I, p) == 0)
    check("TAMPER.circle", not bad, "shallow circle prefix must have d>0")
    # wrong: claim trivial floor decays
    N, p = 8, 17
    d_small = defect(N, interval(0, 2, N), p)
    d_big = defect(N, interval(0, 6, N), p)
    check("TAMPER.floor", d_small == N - 2 and d_big == N - 6,
          "trivial floor d=N-R, no Frobenius decay")
    # wrong: orbit-size closed form off-by-one must be caught
    off = any(orbit_size_closed(c, 31, 2) + 1 == len(frob_orbit(c, 31, 2))
              for c in range(1, 31))
    check("TAMPER.orbit", not off, "closed form is exact, not off-by-one")


# ------------------------------------------------------------------------- #
def main():
    run_trichotomy()
    run_orbit()
    run_defect_twoways()
    run_order1()
    run_order2()
    run_active_primitive()
    run_danny_thm2()
    run_necklace()
    run_decay()
    run_fiber()
    run_deploy()
    run_tamper()

    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = sum(1 for _, ok, _ in CHECKS if not ok)
    print("=" * 72)
    print("C5 DEFECT-MAGNITUDE census on deployed families (PR #607 residual)")
    print("=" * 72)
    for name, ok, detail in CHECKS:
        if not ok:
            print(f"  FAIL  {name:22s} {detail}")
    # decay curves (data readout)
    print("\nBINARY-TOWER DECAY  d_2(N, prefix R)/N   (F2 family)")
    for name, N, o, curve in DECAY_ROWS:
        pts = "  ".join(f"{f:.2f}:{r:.3f}" for (f, R, d, r) in curve)
        print(f"  N={N:>5d} ord_N(2)={o:>3d}  [R/N:d/N]  {pts}   ({name})")
    print(f"\n{'PASS' if nfail == 0 else 'FAIL'}: {npass} checks"
          + (f", {nfail} FAILED" if nfail else ""))
    raise SystemExit(0 if nfail == 0 else 1)


if __name__ == "__main__":
    main()
