#!/usr/bin/env python3
"""Attack the NON-CYCLIC C5 field-descent slope-count wall of PR #545.

WALL (asymptotic_rs_mca_frontiers.tex, C5 extension/field-descent cell,
L2422-2427, verbatim): "...Frobenius invariance is constructible.  Its natural
subfield profile can be larger than the identity profile, so a DIRECT
FIELD-SENSITIVE SLOPE COUNT is required."  #545 (gap2_collapse_routing.md,
Rung 5 / L-G2-4) narrows the residual to this slope count "in the general
(non-cyclic) field-descent case", noting PR #451 supplies only the CYCLIC
instance p^{d_p}.

DANNY #451 (asymptotic_c9_frobenius_cyclotomic_defect.md, Theorem 1) proves,
for a CYCLIC frequency group Z/NZ (the char group of a cyclic multiplicative
subgroup <zeta> of K^x, p prime, p | N false):
    |Omega cap Phi^{-1}(y)| <= p^{d_p(N,I)},  d_p(N,I) = N - |Z_p(N,I)|,
    Z_p(N,I) = union_{ell>=0} p^ell * I  (Frobenius closure of I under x->p x).
His proof forms f_x(X)=sum_i e_i X^i in F_p[X], uses G_Z=prod_{k in Z_p}(X-zeta^k)
| f_x, and counts deg h < d_p giving p^{d_p} polynomials -- PRINCIPAL-IDEAL /
degree bookkeeping in F_p[X]/(X^N-1), a PID *because Z/NZ is cyclic*.

THIS SCRIPT proves + measures the NON-CYCLIC extension.  For a general finite
abelian group G (the non-cyclic slope group of a product / multivariate
field-descent profile) with p not dividing |G|, and a slope profile I in the
dual Ghat, define Z_p(G,I) = union_ell p^ell . I under Frobenius chi->chi^p on
Ghat, d_p(G,I) = |G| - |Z_p(G,I)|.  Then (Theorem A here)
    |Omega cap Phi^{-1}(y)| <= p^{d_p(G,I)}  ................................ (A)
by a SEMISIMPLE GROUP-ALGEBRA count that replaces Danny's PID bookkeeping:
F_p[G] is semisimple (Maschke, p not | |G|), the Fourier transform identifies
Kbar[G]=Kbar^{Ghat}, the syndrome forces ahat|_I=0, the Frobenius primitive
(sum a_i omega_i)^p = sum a_i omega_i^p (Lean sum_smul_pow, field-agnostic)
forces ahat|_{Z_p(G,I)}=0, and the vanishing subspace {a: ahat|_Z=0} for a
Frobenius-closed Z has F_p-dimension exactly |G|-|Z| (each killed Frobenius
orbit of size m removes m; one F_{p^m} simple component).

VERIFIER CHECKS (recomputes every number the note quotes; exit 0 iff all pass):
  ORBIT   : orbit-size closed form ell(chi)=lcm_i ord_{n_i/gcd(c_i,n_i)}(p)
            matches the directly-iterated orbit, on every non-cyclic G.
  DEFECT  : |Z_p(G,I)| = sum over Frobenius orbits meeting I of |orbit|;
            d_p = |G|-|Z_p|, recomputed two ways.
  FIBER=  : (p=2, |G| odd, Omega=all): every nonempty fiber of x->Phi(x) over
            the field realization has size EXACTLY p^{d_p} (bound (A) TIGHT).
  FIBER<= : (general p, Boolean Omega): max measured fiber <= p^{d_p}.
  RANK    : F_p-rank of the syndrome map == |Z_p(G,I)| (the semisimple count),
            cross-checked against enumeration.
  CYCLIC  : the r=1 specialization reproduces Danny #451 |Z_p(N,I)| exactly
            (lineage: (A) specializes to #451 Theorem 1).
  NONMULT : the defect does NOT factor over a product decomposition -- a box
            I=I_1 x I_2 has |Z_p(G,I)| != |Z_p|*|Z_p| in general (Frobenius
            couples the factors); the slope-count functional is NOT
            multiplicative.  (Structure-reduction obstruction, Rung 2.)
  DEGEN   : NEW-FLOOR falsifier -- for p == 1 mod exp(G) (Frobenius trivial,
            Danny's "N|p-1" row in the product) d_p(G,I)=|G|-|I| is MAXIMAL, so
            (A)'s payment p^{d_p} is vacuous; the routing does NOT close
            uniformly on non-cyclic C5 leaves, only on the Frobenius-active
            sub-class.
  MODULAR : scope falsifier -- dropping p not | |G| BREAKS (A): a measured
            fiber exceeds p^{d_p} when p | |G| (characters degenerate,
            non-semisimple).  Confirms the hypothesis is load-bearing.
  TAMPER  : deliberately wrong values must fail.

Stdlib only.  Zero-arg.  Runtime < 120 s under ulimit -v 2097152.
GF/rank idiom reused from verify_gap2_routing.py (#545) and
verify_entropy_inverse_fp_span_cell.py (credited).
"""
from __future__ import annotations

from itertools import product
from math import gcd

CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    CHECKS.append((name, bool(ok), detail))
    return bool(ok)


# =========================================================================== #
#  number theory helpers                                                       #
# =========================================================================== #
def mult_order(a: int, n: int) -> int:
    """multiplicative order of a mod n (requires gcd(a,n)=1); n>=1, order of unit."""
    if n == 1:
        return 1
    a %= n
    assert gcd(a, n) == 1, (a, n)
    o = 1
    x = a
    while x != 1:
        x = (x * a) % n
        o += 1
    return o


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def _prime_factors(n):
    fs = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            fs.add(d)
            n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs


# =========================================================================== #
#  F_p[x] + GF(p^m) arithmetic  (idiom reused from verify_gap2_routing.py)     #
# =========================================================================== #
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
    a = list(a)
    m = _ptrim(list(m))
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
    for r in _prime_factors(k):
        h = _ppowmod(x, p ** (k // r), f, p)
        g = _pgcd(_psub(h, x, p), f, p)
        if not (len(g) == 1 and g[0] != 0):
            return False
    return True


def _smallest_irred(p, k):
    for code in range(p ** k):
        low = []
        c = code
        for _ in range(k):
            low.append(c % p)
            c //= p
        f = low + [1]
        if _is_irred(f, p):
            return f
    raise RuntimeError("no irreducible")


class GF:
    """F_{p^k}; elements are base-p digit ints; smallest monic irreducible modulus."""

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

    def add(self, a, b):
        return self._enc([(x + y) % self.p for x, y in zip(self._vec(a), self._vec(b))])

    def powr(self, a, e):
        if e == 0:
            return 1
        if a == 0:
            return 0
        return self.antilog[(self.logt[a] * (e % (self.q - 1))) % (self.q - 1)]

    def _find_gen(self):
        q = self.q
        need = q - 1
        fs = _prime_factors(need)
        for cand in range(2, q):
            ok = True
            for r in fs:
                e = need // r
                x, base, ee = 1, cand, e
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
        """a primitive e-th root of unity in F_{p^k}^x (requires e | q-1)."""
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
        if piv == len(rows):
            break
    return piv


# =========================================================================== #
#  finite abelian group G = prod_i Z/n_i and its Frobenius (mult-by-p) action  #
# =========================================================================== #
class AbGroup:
    """G = Z/n_1 x ... x Z/n_r; elements are tuples; Ghat identified with G."""

    def __init__(self, moduli):
        self.n = tuple(moduli)
        self.r = len(moduli)
        self.order = 1
        for ni in moduli:
            self.order *= ni
        self.exp = 1
        for ni in moduli:
            self.exp = lcm(self.exp, ni)
        self.elems = [tuple(e) for e in product(*[range(ni) for ni in moduli])]

    def frob(self, c, p):
        return tuple((p * ci) % ni for ci, ni in zip(c, self.n))

    def orbit(self, c, p):
        orb = []
        seen = set()
        x = c
        while x not in seen:
            seen.add(x)
            orb.append(x)
            x = self.frob(x, p)
        return orb

    def orbit_size_formula(self, c, p):
        """ell(chi) = lcm_i ord_{n_i/gcd(c_i,n_i)}(p)."""
        L = 1
        for ci, ni in zip(c, self.n):
            m = ni // gcd(ci, ni)          # order of c_i in Z/n_i
            if m == 1:
                continue
            L = lcm(L, mult_order(p, m))
        return L

    def frob_closure(self, I, p):
        """Z_p(G,I) = union of full Frobenius orbits of every chi in I."""
        Z = set()
        for c in I:
            if c in Z:
                continue
            for x in self.orbit(c, p):
                Z.add(x)
        return Z

    def closure_by_orbit_sum(self, I, p):
        """|Z_p(G,I)| via sum over distinct orbits meeting I of orbit-size formula."""
        reps = {}
        for c in I:
            orb = tuple(sorted(self.orbit(c, p)))
            reps[orb] = orb[0]
        total = 0
        for orb in reps:
            total += self.orbit_size_formula(reps[orb], p)
        return total, len(reps)

    def pairing(self, c, g):
        """<c,g> mod exp for character value zeta_exp^{<c,g>}; use per-factor exps."""
        s = 0
        for ci, gi, ni in zip(c, g, self.n):
            # contribution ci*gi/ni of a full turn -> exponent on a common e=exp root
            s += (ci * gi) * (self.exp // ni)
        return s % self.exp


# =========================================================================== #
#  field realization of the fiber census                                       #
# =========================================================================== #
def realize_and_census(G: AbGroup, I, p, enumerate_cap=18):
    """Build Phi over K=F_{p^m}, m=ord_exp(p); return (dp, max_fiber, tight_ok,
    rank, all_equal_dp) with Boolean Omega.  For p||G| use e=exp still but the
    characters degenerate (that is the point of the modular falsifier)."""
    e = G.exp
    # smallest m with e | p^m - 1  (order of p mod e/(p-part)); if p|e no such m
    e_coprime = e
    while e_coprime % p == 0:
        e_coprime //= p
    m = mult_order(p, e_coprime) if e_coprime > 1 else 1
    F = GF(p, m)
    zeta = F.root_of_unity(e_coprime) if e_coprime > 1 else 1
    # value zeta^{<c,g>}: reduce exponent mod e_coprime (p-part of e collapses in char p)
    def chval(c, g):
        expo = G.pairing(c, g) % e_coprime if e_coprime > 1 else 0
        return F.powr(zeta, expo)

    # v_g = ( chval(c,g) )_{c in I}  in K^{|I|}
    vg = {g: tuple(chval(c, g) for c in I) for g in G.elems}

    Z = G.frob_closure(I, p)
    dp = G.order - len(Z)

    # --- syndrome-map F_p-rank (semisimple count) ---
    # map x in F_p^{|G|} -> (Phi(x)_c)_{c in I} in K^{|I|} = F_p^{m|I|}, F_p-linear.
    rows = []
    for g in G.elems:
        row = []
        for c in I:
            row.extend(F._vec(vg[g][I.index(c)]))
        rows.append(row)
    # rank of the |G| x (m|I|) matrix = dim image = |G| - dim ker
    rk = rank_fp([list(r) for r in rows], p)

    # --- Boolean-Omega fiber census (enumerate if feasible) ---
    max_fiber = None
    all_equal_dp = None
    if G.order <= enumerate_cap:
        buckets = {}
        nI = len(I)
        # precompute per-g contribution tuple in F_p^{m*nI} coordinates for fast add
        gvecs = [rows[i] for i in range(len(G.elems))]
        width = m * nI
        for mask in range(1 << G.order):
            acc = [0] * width
            mm = mask
            idx = 0
            while mm:
                if mm & 1:
                    gv = gvecs[idx]
                    for j in range(width):
                        acc[j] = (acc[j] + gv[j]) % p
                mm >>= 1
                idx += 1
            key = tuple(acc)
            buckets[key] = buckets.get(key, 0) + 1
        max_fiber = max(buckets.values())
        if p == 2 and G.order % 2 == 1:
            # Omega = all F_2^{|G|}, linear map: every nonempty fiber == |ker| == 2^{|G|-rk}
            all_equal_dp = all(v == (1 << (G.order - rk)) for v in buckets.values())
    return dp, max_fiber, rk, len(Z), all_equal_dp, m, F.q


# =========================================================================== #
#  main                                                                        #
# =========================================================================== #
def main():
    print("=" * 74)
    print("verify_noncyclic_c5_count.py -- non-cyclic C5 field-descent slope count")
    print("Theorem A: |Omega cap Phi^{-1}(y)| <= p^{d_p(G,I)},  p not | |G|")
    print("=" * 74)

    # ---------------------------------------------------------------- #
    #  block 1: ORBIT + DEFECT closed forms on non-cyclic groups        #
    # ---------------------------------------------------------------- #
    # (name, moduli, p) with p not dividing |G|
    ORBIT_CASES = [
        ("(Z3)^2", (3, 3), 2), ("(Z3)^2", (3, 3), 5), ("(Z3)^2", (3, 3), 7),
        ("(Z2)^2", (2, 2), 3), ("(Z2)^2", (2, 2), 5),
        ("Z2xZ4", (2, 4), 3), ("Z2xZ4", (2, 4), 5),
        ("(Z2)^3", (2, 2, 2), 3), ("Z3xZ9", (3, 9), 2),
        ("(Z4)^2", (4, 4), 3), ("(Z5)^2", (5, 5), 2),
        ("Z2xZ6", (2, 6), 5), ("(Z7)^2", (7, 7), 2),
    ]
    print("\n[ORBIT] orbit-size closed form ell(chi)=lcm_i ord_{n_i/gcd}(p):")
    for name, mod, p in ORBIT_CASES:
        G = AbGroup(mod)
        assert G.order % p != 0
        ok = all(len(G.orbit(c, p)) == G.orbit_size_formula(c, p) for c in G.elems)
        check(f"ORBIT.{name}.p{p}.formula", ok,
              f"orbit-size formula vs iterated, all {G.order} elems")
    # defect two ways on a batch of profiles
    print("[DEFECT] |Z_p(G,I)| = sum over orbits meeting I of |orbit|:")
    DEFECT_CASES = []
    for name, mod, p in ORBIT_CASES:
        G = AbGroup(mod)
        # profiles: a single generator, a box, an L-shape
        gens = [tuple(1 if i == 0 else 0 for i in range(G.r))]
        box = [e for e in G.elems if all(1 <= ci <= min(2, ni - 1) for ci, ni in zip(e, G.n))]
        Ls = [tuple(1 if i == 0 else 0 for i in range(G.r)),
              tuple(1 if i == 1 else 0 for i in range(G.r))] if G.r >= 2 else gens
        for tag, I in [("gen", gens), ("box", box or gens), ("L", Ls)]:
            I = sorted(set(I))
            Z = G.frob_closure(I, p)
            tot, norb = G.closure_by_orbit_sum(I, p)
            dp = G.order - len(Z)
            check(f"DEFECT.{name}.p{p}.{tag}.two_ways", tot == len(Z),
                  f"orbit-sum={tot} iterated={len(Z)} dp={dp} |G|={G.order}")
            DEFECT_CASES.append((name, mod, p, tag, I, dp, len(Z)))

    # ---------------------------------------------------------------- #
    #  block 2: FIBER census -- Theorem A bound + tightness             #
    # ---------------------------------------------------------------- #
    print("\n[FIBER] Boolean-Omega fiber census vs p^{d_p}  (bound (A)):")
    fiber_rows = []
    FIBER_CASES = [
        ("(Z3)^2", (3, 3), 2, "box"), ("(Z3)^2", (3, 3), 2, "gen"),
        ("(Z3)^2", (3, 3), 2, "L"),  ("(Z3)^2", (3, 3), 5, "box"),
        ("(Z2)^2", (2, 2), 3, "box"), ("Z2xZ4", (2, 4), 3, "box"),
        ("Z2xZ4", (2, 4), 5, "box"), ("(Z2)^3", (2, 2, 2), 3, "box"),
        ("Z3xZ9", (3, 9), 2, "gen"), ("(Z5)^2", (5, 5), 2, "gen"),
    ]
    for name, mod, p, tag in FIBER_CASES:
        G = AbGroup(mod)
        if tag == "gen":
            I = [tuple(1 if i == 0 else 0 for i in range(G.r))]
        elif tag == "L":
            I = [tuple(1 if i == 0 else 0 for i in range(G.r)),
                 tuple(1 if i == 1 else 0 for i in range(G.r))]
        else:  # box
            I = sorted(e for e in G.elems
                       if all(1 <= ci <= min(2, ni - 1) for ci, ni in zip(e, G.n)))
        I = sorted(set(I))
        dp, mx, rk, zsz, alleq, mm, qq = realize_and_census(G, I, p)
        bound = p ** dp
        # RANK: semisimple count -- image rank == |Z_p(G,I)|
        check(f"RANK.{name}.p{p}.{tag}", rk == zsz,
              f"F_p-rank={rk} |Z_p|={zsz} (semisimple dim count)")
        # FIBER<=: bound (A) holds
        if mx is not None:
            check(f"FIBER<=.{name}.p{p}.{tag}", mx <= bound,
                  f"max_fiber={mx} <= p^dp={bound} (dp={dp})")
            # FIBER=: for p=2,|G| odd,Omega=all the bound is TIGHT (equality)
            if alleq is not None:
                check(f"FIBER=.{name}.p{p}.{tag}", alleq and mx == bound,
                      f"every nonempty fiber == 2^dp={bound} (tight)")
            fiber_rows.append((name, p, tag, dp, mx, bound, rk, zsz, mm, qq))

    print(f"{'group':8} {'p':>2} {'prof':>4} {'dp':>3} {'maxfib':>7} "
          f"{'p^dp':>7} {'rk':>3} {'|Zp|':>4} {'K':>5}")
    for name, p, tag, dp, mx, bd, rk, zsz, mm, qq in fiber_rows:
        print(f"{name:8} {p:>2} {tag:>4} {dp:>3} {mx:>7} {bd:>7} {rk:>3} "
              f"{zsz:>4} F{qq:>4}")

    # ---------------------------------------------------------------- #
    #  block 3: CYCLIC specialization -> reproduces Danny #451          #
    # ---------------------------------------------------------------- #
    print("\n[CYCLIC] r=1 specialization reproduces PR #451 |Z_p(N,I)|:")
    # #545 tamper anchor: |Z_2(7,{1,2})| = 3
    G7 = AbGroup((7,))
    Z = G7.frob_closure([(1,), (2,)], 2)
    check("CYCLIC.Z7.I12.p2", len(Z) == 3, f"|Z_2(7,{{1,2}})|={len(Z)} (==#545 anchor 3)")
    # a few more cyclic (N, I=consecutive interval, p) vs a direct Z/N closure
    for N, a, R, p in [(15, 1, 3, 2), (31, 1, 5, 2), (9, 1, 2, 5), (63, 1, 6, 2)]:
        if N % p == 0:
            continue
        Gc = AbGroup((N,))
        I = [((a + j) % N,) for j in range(R)]
        Z = Gc.frob_closure(I, p)
        # direct scalar closure
        Sset = set((a + j) % N for j in range(R))
        fr = list(Sset)
        while fr:
            x = fr.pop()
            y = (p * x) % N
            if y not in Sset:
                Sset.add(y)
                fr.append(y)
        check(f"CYCLIC.N{N}.a{a}.R{R}.p{p}", len(Z) == len(Sset),
              f"group-alg |Z|={len(Z)} scalar |Z|={len(Sset)} dp={N-len(Z)}")

    # ---------------------------------------------------------------- #
    #  block 4: NONMULT -- defect does NOT factor over the product      #
    # ---------------------------------------------------------------- #
    print("\n[NONMULT] slope-count functional is NOT multiplicative over factors:")
    # G=(Z3)^2, p=2, box I = {1} x {0,1} -> |Z_2(G,I)| != |Z_2(Z3,{1})|*|Z_2(Z3,{0,1})|
    G = AbGroup((3, 3))
    I = [(1, 0), (1, 1)]
    Zbox = G.frob_closure(I, 2)
    # per-factor closures
    F0 = AbGroup((3,))
    Za = F0.frob_closure([(1,)], 2)          # {1,2}
    Zb = F0.frob_closure([(0,), (1,)], 2)    # {0,1,2}
    prod = len(Za) * len(Zb)
    check("NONMULT.Z3sq.box.nonfactoring", len(Zbox) != prod,
          f"|Z_2(G,{{1}}x{{0,1}})|={len(Zbox)} != |Za|*|Zb|={len(Za)}*{len(Zb)}={prod}")
    check("NONMULT.Z3sq.box.value", len(Zbox) == 4,
          f"|Z_2(G,I)|={len(Zbox)} (Frobenius couples the two coordinates)")

    # ---------------------------------------------------------------- #
    #  block 5: DEGEN -- NEW-FLOOR falsifier, Frobenius-trivial => max defect
    # ---------------------------------------------------------------- #
    print("\n[DEGEN] Frobenius-trivial (p==1 mod exp G) => d_p = |G|-|I| MAXIMAL (payment vacuous):")

    def first_prime(pred, start=2):
        n = start
        while True:
            if all(n % d for d in range(2, int(n ** 0.5) + 1)) and n > 1 and pred(n):
                return n
            n += 1

    # Law: p == 1 mod exp(G)  =>  Z_p(G,I) = I exactly (Frobenius trivial), d_p = |G|-|I|.
    # This is Danny #451 sec.7's excluded "N | p-1" row, now in the non-cyclic product.
    DEGEN_GROUPS = [
        ("(Z3)^2", (3, 3), [(1, 0)]),
        ("(Z3)^2", (3, 3), [(1, 1), (1, 2)]),
        ("Z2xZ4", (2, 4), [(1, 1)]),
        ("(Z7)^2", (7, 7), sorted((a, b) for a in (1, 2, 3) for b in (1, 2, 3))),
        ("(Z5)^2", (5, 5), [(1, 2)]),
    ]
    strict_seen = False
    for name, mod, I in DEGEN_GROUPS:
        G = AbGroup(mod)
        I = sorted(set(I))
        p_triv = first_prime(lambda q: q % G.exp == 1 and G.order % q != 0)
        p_act = first_prime(lambda q: q % G.exp != 1 and G.order % q != 0)
        Zt = G.frob_closure(I, p_triv)
        Za = G.frob_closure(I, p_act)
        dt, da = G.order - len(Zt), G.order - len(Za)
        # trivial-Frobenius law: closure is I itself, defect maximal = |G|-|I|
        check(f"DEGEN.{name}.trivial_law_p{p_triv}",
              Zt == set(I) and dt == G.order - len(I),
              f"p={p_triv}==1 mod {G.exp}: Z_p=I, d_p={dt}==|G|-|I|={G.order-len(I)}")
        # active Frobenius never worse; strict somewhere (Frobenius-sensitive floor)
        check(f"DEGEN.{name}.active_le_trivial_p{p_act}", da <= dt,
              f"d_active(p{p_act})={da} <= d_trivial(p{p_triv})={dt}")
        if da < dt:
            strict_seen = True
        print(f"  {name:8} |I|={len(I):<2} d_active(p{p_act})={da:<3} "
              f"d_trivial(p{p_triv})={dt:<3}  (|G|={G.order})")
    check("DEGEN.floor_is_frobenius_sensitive", strict_seen,
          "some non-cyclic profile has d_active < d_trivial (payment non-uniform)")

    # ---------------------------------------------------------------- #
    #  block 6: MODULAR -- dropping p not | |G| BREAKS the bound         #
    # ---------------------------------------------------------------- #
    print("\n[MODULAR] scope falsifier: p | |G| breaks (A) (measured fiber > p^{d_p}):")
    # G=(Z2)^2, p=2: characters degenerate in char 2; measured fiber exceeds p^{d_p}.
    G = AbGroup((2, 2))
    I = [(1, 0)]
    # direct construction: in char 2, mu_2 = {1}, all characters trivial -> Phi(x)=|supp| mod 2
    # d_2: Z_2(G,I): 2*(1,0)=(0,0); orbit {(1,0),(0,0)} size 2 -> |Z|=2, d=4-2=2, bound 2^2=4
    Z = G.frob_closure(I, 2)
    dp = G.order - len(Z)
    bound = 2 ** dp
    # measured: all chars trivial, Phi(x) = sum_g x_g (in F_2) constant over I -> fiber = 2^{|G|-1}
    buckets = {}
    for mask in range(1 << G.order):
        s = bin(mask).count("1") % 2
        buckets[s] = buckets.get(s, 0) + 1
    mx = max(buckets.values())
    check("MODULAR.Z2sq.p2.bound_broken", mx > bound,
          f"measured fiber={mx} > p^dp={bound}: (A) FAILS without p not | |G|")
    print(f"  G=(Z2)^2 p=2: measured max fiber={mx}, p^dp={bound} "
          f"-> hypothesis p not | |G| is load-bearing")

    # ---------------------------------------------------------------- #
    #  tamper self-tests                                                #
    # ---------------------------------------------------------------- #
    t0 = len(CHECKS)
    check("TAMPER.wrong_closure_must_fail",
          not (len(AbGroup((3, 3)).frob_closure([(1, 0)], 2)) == 3),
          "|Z_2((Z3)^2,{(1,0)})|=2 not 3")
    check("TAMPER.wrong_orbit_must_fail",
          not (AbGroup((3, 3)).orbit_size_formula((1, 0), 2) == 1),
          "orbit size of (1,0) under x2 in (Z3)^2 is 2 not 1")
    assert len(CHECKS) == t0 + 2

    # ---------------------------------------------------------------- #
    #  report                                                           #
    # ---------------------------------------------------------------- #
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = len(CHECKS) - npass
    print("\n" + "=" * 74)
    if nfail:
        for nm, ok, det in CHECKS:
            if not ok:
                print(f"  FAIL  {nm}   {det}")
        print(f"RESULT: FAIL ({nfail} of {len(CHECKS)} checks failed)")
        raise SystemExit(1)
    print(f"RESULT: PASS ({npass} checks)")


if __name__ == "__main__":
    main()
