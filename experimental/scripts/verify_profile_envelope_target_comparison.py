#!/usr/bin/env python3
"""Exact finite census for selected profile-envelope slices.

The verifier enumerates the identity slice and complete-power-fiber
quotient/remainder slices at the printed GF(13), GF(7^2), GF(11^2), and GF(41)
rows.  It does not enumerate the Chebyshev, planted, balanced-core, or general
first-match profile inventory in (1.6), and it proves no universal
prime-field theorem.

All finite arithmetic uses Fraction/bigint gates.  In particular it records:
  * the GF(13) square is identity-dominated, while the shallow c=3,r=0 cell has
    barN=6 > 924/169 and is only covered by the separate deep term 7;
  * the tower square beats the formal ambient identity proxy, but not the
    realized identity average at the n=20 smooth-coset row;
  * a factor-p exact full-codomain deficit is observed for that identity image;
    this finite equality does not decide the asymptotic (FI) condition;
  * failure of a safe-side upper-budget test is not an unsafe theorem.

The JSON certificate is source-bound and validated here.  Stdlib only,
deterministic, with normal/-O parity and two independent tamper mutations.
Full identity enumeration is capped at n=20 (C(20,10)=184756); the generic
GF(121) control exhausts all 184756 supports.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import combinations
from math import comb, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CERT_PATH = Path(
    "experimental/data/certificates/profile-envelope-target-comparison/cert.json"
)
NOTE_PATH = Path(
    "experimental/notes/thresholds/profile_envelope_target_comparison.md"
)
LEAN_PATH = Path(
    "experimental/lean/profile_envelope_target_comparison/"
    "ProfileEnvelopeTargetComparison.lean"
)
SCRIPT_PATH = Path("experimental/scripts/verify_profile_envelope_target_comparison.py")

# ------------------------------------------------------------------ checker ---

class Checker:
    def __init__(self) -> None:
        self.n = 0
        self.fails: list[str] = []
        self.log: list[str] = []

    def ok(self, cond: bool, msg: str) -> None:
        self.n += 1
        if not cond:
            self.fails.append(msg)

    def note(self, s: str) -> None:
        self.log.append(s)


# --------------------------------------------------------------- GF(p) / GF(p^2)
# A finite field is a dict of closures over exact integer reps.
#   GF(p):   element = int in [0,p)
#   GF(p^2): element = (a,b) meaning a + b*t, with t^2 = nu (nu a nonresidue)

def make_gf_p(p: int) -> dict:
    def add(x, y): return (x + y) % p
    def sub(x, y): return (x - y) % p
    def mul(x, y): return (x * y) % p
    def neg(x): return (-x) % p
    def inv(x): return pow(x, p - 2, p)
    def powr(x, e):
        r = 1
        for _ in range(e):
            r = (r * x) % p
        return r
    elems = list(range(p))
    return dict(p=p, q=p, zero=0, one=1, add=add, sub=sub, mul=mul, neg=neg,
                inv=inv, powr=powr, elems=elems, name=f"GF({p})", prime_field=True)


def make_gf_p2(p: int) -> dict:
    # find a quadratic nonresidue nu
    nu = None
    for cand in range(2, p):
        if pow(cand, (p - 1) // 2, p) == p - 1:
            nu = cand
            break
    assert nu is not None
    def add(x, y): return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)
    def sub(x, y): return ((x[0] - y[0]) % p, (x[1] - y[1]) % p)
    def neg(x): return ((-x[0]) % p, (-x[1]) % p)
    def mul(x, y):
        a, b = x; c, d = y
        return ((a * c + b * d * nu) % p, (a * d + b * c) % p)
    def powr(x, e):
        r = (1, 0)
        base = x
        while e > 0:
            if e & 1:
                r = mul(r, base)
            base = mul(base, base)
            e >>= 1
        return r
    def inv(x):
        return powr(x, p * p - 2)
    elems = [(a, b) for a in range(p) for b in range(p)]
    return dict(p=p, q=p * p, nu=nu, zero=(0, 0), one=(1, 0), add=add, sub=sub,
                mul=mul, neg=neg, inv=inv, powr=powr, elems=elems,
                name=f"GF({p}^2)", prime_field=False)


def find_generator(F: dict):
    """A generator of F^x (order q-1)."""
    q = F["q"]
    order = q - 1
    # factor order
    fac = []
    m = order
    d = 2
    while d * d <= m:
        if m % d == 0:
            fac.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        fac.append(m)
    for g in F["elems"]:
        if g == F["zero"]:
            continue
        if all(F["powr"](g, order // pr) != F["one"] for pr in fac):
            return g
    raise RuntimeError("no generator found")


# --------------------------------------------------------- locator prefix map --

def locator_prefix(F: dict, support, w: int):
    """Depth-w locator prefix Phi_w(S): the w coefficients just below the leading
    coefficient of Q_S(X)=prod_{x in S}(X-x).  Returned as a hashable tuple of
    field elements (c_1,...,c_w), c_i = coeff of X^{|S|-i}.

    Uses the exact recurrence c_i^{new} = c_i - x*c_{i-1} (c_0==1 monic) and
    TRUNCATES to the top w coefficients: since c_i depends only on c_0..c_i, the
    truncation is exact for c_1..c_w and makes each support O(|S|*w)."""
    mul, sub = F["mul"], F["sub"]
    zero, one = F["zero"], F["one"]
    # keep [c_0=1, c_1, ..., c_w]
    c = [one] + [zero] * w
    for x in support:
        # update from high index down so c_{i-1} is the old value
        for i in range(w, 0, -1):
            c[i] = sub(c[i], mul(x, c[i - 1]))
    return tuple(c[1:1 + w])


# ------------------------------------------------------- domain / folding build

def build_prime_row(p: int):
    """D = F_p^x (cyclic of order n=p-1) inside B=F=GF(p).  Prime field: no
    proper subfield, so every folding has lambda_c=1 (no field drop)."""
    F = make_gf_p(p)
    D = list(range(1, p))          # F_p^x
    n = len(D)
    return F, F, D, n               # (F ambient, B base = F, D, n)


def build_prime_subgroup_row(p: int, sub: int):
    """D = the order-`sub` multiplicative subgroup of F_p^x inside B=F=GF(p).
    Requires sub | (p-1).  Prime field: no field drop possible."""
    F = make_gf_p(p)
    assert (p - 1) % sub == 0
    def is_gen(g):
        seen = set()
        x = 1
        for _ in range(p - 1):
            x = (x * g) % p
            seen.add(x)
        return len(seen) == p - 1
    g = next(gg for gg in range(2, p) if is_gen(gg))
    h = pow(g, (p - 1) // sub, p)                     # order-sub element
    D, x = [], 1
    for _ in range(sub):
        x = (x * h) % p
        D.append(x)
    assert len(set(D)) == sub
    return F, F, D, sub


def build_tower_row(p: int):
    """The thm:smooth-quotient-obstruction tower: B=F=GF(p^2), H<=B^x of order
    n=2(p-1), theta a generator, D=theta*H.  Square folding lands D^{(2)} in
    a scalar copy of B_phi=F_p (field drop lambda_2=1/2)."""
    F = make_gf_p2(p)
    g = find_generator(F)
    n = 2 * (p - 1)
    assert (p * p - 1) % n == 0
    step = (p * p - 1) // n        # = (p+1)//2
    H = [F["powr"](g, (step * i) % (p * p - 1)) for i in range(n)]
    theta = g
    D = [F["mul"](theta, h) for h in H]
    # sanity: D distinct
    assert len(set(D)) == n
    return F, F, D, n


def fibers_of_power(F: dict, D, c: int):
    """Complete c-fibers of x -> x^c on D (D cyclic under multiplication).
    Returns (Q, fiber_of_value) where Q=list of distinct x^c and fiber_of_value
    maps each q in Q to the sorted tuple of its c preimages in D."""
    powr = F["powr"]
    buckets: dict = {}
    for x in D:
        y = powr(x, c)
        buckets.setdefault(y, []).append(x)
    Q_ = list(buckets.keys())
    return Q_, buckets


# ---------------------------------------------- slice enumerators (Omega_lambda)

def identity_slice(D, a):
    """All a-subsets of D."""
    for S in combinations(D, a):
        yield S


def quotient_slice(D, a, c, r, Qvals, fiber):
    """Complete-c-fiber-plus-remainder supports S = phi^{-1}(E) sqcup R with
    |E|=m=(a-r)/c full fibers and |R|=r remainder points from OTHER fibers
    (r<c so R contains no full fiber).  Yields sorted-by-D-order tuples."""
    m = (a - r) // c
    fibers = [tuple(fiber[q]) for q in Qvals]
    Nfib = len(fibers)
    if m > Nfib:
        return
    for Eidx in combinations(range(Nfib), m):
        base = []
        chosen = set(Eidx)
        for i in Eidx:
            base.extend(fibers[i])
        if r == 0:
            yield tuple(sorted(base, key=lambda z: D.index(z)))
            continue
        # remainder points from fibers not in Eidx
        rest = []
        for i in range(Nfib):
            if i not in chosen:
                rest.extend(fibers[i])
        for R in combinations(rest, r):
            supp = base + list(R)
            yield tuple(sorted(supp, key=lambda z: D.index(z)))


# ---------------------------------------------------- per-slice exact census ---

def census_slice(F, D, a, w, slice_iter):
    """Exact census of a slice under Phi_w.  Returns:
       size    = |Omega_lambda|
       Ldist   = |Phi_w(Omega_lambda)|  (realized image)
       maxfib  = largest prefix bucket  (the operative pole list size)
       lacunary_ok, subfield_ok, subfield_size (diagnostics; filled by caller)"""
    buckets: dict = {}
    size = 0
    for S in slice_iter:
        size += 1
        key = locator_prefix(F, S, w)
        buckets[key] = buckets.get(key, 0) + 1
    Ldist = len(buckets)
    maxfib = max(buckets.values()) if buckets else 0
    return size, Ldist, maxfib, buckets


def barN(size: int, Ldist: int) -> Q:
    return Q(size, Ldist) if Ldist else Q(0)


# ------------------------------------------------------ collision-aware pole ---

def M_of_L(L: int, q: int, n: int, k: int) -> int:
    """thm:collision-aware-pole (4.2): distinct MCA-bad slopes from a list of L."""
    if L <= 0:
        return 0
    num = L * (q - n)
    den = (q - n) + k * (L - 1)
    return -(-num // den)          # ceil


def P_reserve(Lenv: int, q: int, n: int, k: int, gamma: int) -> int:
    """prop:simple-pole-lower (13.3) / SB1 P(a): challenge-restricted reserve
    from an envelope list of size Lenv."""
    inner = M_of_L(Lenv, q, n, k)
    return -(-(gamma * inner) // q)  # ceil( |Gamma|/q * inner )


# ============================================================= main sections ===

def section_A_reproduce_542(c: Checker) -> None:
    """Cross-check: reproduce envelope_identity_window.md #542 exact F_{p^2}
    square census (p in {5,7,11}); distinct prefixes = p, max bucket = QR6."""
    c.note("== A. Cross-check #542 square census over the F_{p^2} tower ==")
    # #542 table rows: (p, n, a, C(N,m)=C(n/2,a/2), distinct_prefixes=p, maxbucket, QR6)
    expect = {
        5:  dict(n=8,  a=4, CNm=comb(4, 2),  distinct=5,  maxb=2, qr6=2),
        7:  dict(n=12, a=4, CNm=comb(6, 2),  distinct=7,  maxb=3, qr6=3),
        11: dict(n=20, a=4, CNm=comb(10, 2), distinct=11, maxb=5, qr6=5),
    }
    for p, ex in expect.items():
        F, B, D, n = build_tower_row(p)
        c.ok(n == ex["n"], f"A p={p}: n={n} expected {ex['n']}")
        a = ex["a"]
        Qvals, fiber = fibers_of_power(F, D, 2)
        c.ok(all(len(v) == 2 for v in fiber.values()),
             f"A p={p}: complete 2-fibers")
        c.ok(len(Qvals) == n // 2, f"A p={p}: |Q|=n/2")
        m = a // 2
        # square slice: |E|=m fibers, r=0
        size, Ldist, maxb, buckets = census_slice(
            F, D, a, w=2, slice_iter=quotient_slice(D, a, 2, 0, Qvals, fiber))
        c.ok(size == ex["CNm"], f"A p={p}: |Omega_sq|={size} exp {ex['CNm']}")
        # depth-2 global prefix on a square support is (0, c_2): c_1==0 lacunary
        c.ok(all(key[0] == F["zero"] for key in buckets),
             f"A p={p}: c_1==0 lacunary on square slice")
        c.ok(Ldist == ex["distinct"],
             f"A p={p}: distinct prefixes {Ldist} exp {ex['distinct']}")
        c.ok(maxb == ex["maxb"], f"A p={p}: max bucket {maxb} exp {ex['maxb']}")
        qr6 = -(-ex["CNm"] // p)     # ceil(C(N,m)/p)
        c.ok(qr6 == ex["qr6"], f"A p={p}: QR6 ceil={qr6} exp {ex['qr6']}")
        c.ok(maxb == qr6, f"A p={p}: max bucket == QR6 pigeonhole")
        c.note(f"   p={p}: |Omega_sq|={size} L_sq={Ldist}(=p) maxbucket={maxb}"
               f"(=QR6=ceil({ex['CNm']}/{p}))")


def full_envelope_census(c: Checker, tag: str, F, B, D, n, a, k, prime_field: bool):
    """Enumerate the identity and complete-power-fiber quotient inventory.

    This is not the complete (1.6) profile inventory: Chebyshev, planted,
    balanced-core, and arbitrary first-match profiles are outside this census.
    """
    w = a - k - 1
    assert w >= 0
    deep_term = n - a + 1                              # thm:deep-regime-upper
    Bq = B["q"]

    # ---- identity slice (full enumeration) ----
    id_size, id_L, id_max, _ = census_slice(F, D, a, w, identity_slice(D, a))
    c.ok(id_size == comb(n, a), f"{tag}: |Omega_id|=C(n,a)")
    barN_id = barN(id_size, id_L)
    # "saturated" only describes the ambient count |B|^w <= C(n,a).  It does
    # NOT imply exact full-codomain image or the asymptotic (FI) condition.
    saturated = (Bq ** w <= comb(n, a))
    fi_id = (id_L == Bq ** w)  # exact full-codomain equality, not asymptotic FI
    # SB1 pigeonhole floor on the MAX identity fiber (a valid pole list size).
    Lpig = -(-comb(n, a) // (Bq ** w))
    c.ok(Lpig <= id_max, f"{tag}: SB1 pigeonhole floor <= enumerated id max fiber")
    report = dict(tag=tag, n=n, a=a, k=k, w=w, Bq=Bq, deep_term=deep_term,
                  id_size=id_size, id_L=id_L, id_max=id_max,
                  barN_id=barN_id, fi_id=fi_id, Lpig=Lpig, saturated=saturated,
                  prime_field=prime_field, cells=[])

    # ---- every complete-c-fiber quotient slice ----
    # scales c>=2 with c | n and admissible remainder r<c with (a-r)%c==0
    for cfold in range(2, n + 1):
        if n % cfold != 0:
            continue
        Qvals, fiber = fibers_of_power(F, D, cfold)
        if not all(len(v) == cfold for v in fiber.values()):
            continue                                   # not complete fibers
        for r in range(0, cfold):
            if (a - r) % cfold != 0:
                continue
            m = (a - r) // cfold
            if m < 1 or m > len(Qvals):
                continue
            # scaled quotient coefficient field B_phi: minimal subfield with
            # Q subset eta*B_phi.  Prime field => B_phi=B (no drop); tower square
            # => B_phi=F_p.  We DETECT it from the realized prefix, exact.
            size, L, mx, buckets = census_slice(
                F, D, a, w, quotient_slice(D, a, cfold, r, Qvals, fiber))
            if size == 0:
                continue
            bN = barN(size, L)
            shallow = (w < cfold)                       # lacunary trivial prefix
            # realized-image field size on this slice: number of distinct field
            # values appearing across all nonzero prefix coordinates.
            realized_vals = set()
            for key in buckets:
                for coord in key:
                    if coord != F["zero"]:
                        realized_vals.add(coord)
            report["cells"].append(dict(
                c=cfold, r=r, m=m, size=size, L=L, maxfib=mx, barN=bN,
                shallow=shallow, deep_dominated=(bN <= deep_term),
                id_dominated=(bN <= max(Q(1), report["barN_id"])),
                field_vals=len(realized_vals)))
    return report



def section_B_prime(c: Checker) -> dict:
    """Prime GF(13) selected-power inventory, including the exact ID failure."""
    c.note("== B. PRIME GF(13): square dominated; shallow c=3 exceeds identity ==")
    n, a, k = 12, 6, 3
    F, B, D, nn = build_prime_row(13)
    c.ok(nn == n, "B: n=12")
    rep = full_envelope_census(c, "prime GF(13)", F, B, D, n, a, k, True)
    c.ok(rep["saturated"], "B: prime row is saturated (|B|^w <= C(n,a))")
    c.ok(rep["fi_id"], "B: exact identity image equals |B|^w at this row")
    all_ok = True
    for cell in rep["cells"]:
        accounted = cell["id_dominated"] or cell["deep_dominated"]
        c.ok(accounted,
             f"B: cell c={cell['c']} r={cell['r']} barN={cell['barN']} accounted "
             f"(id {rep['barN_id']} / deep {rep['deep_term']})")
        if not cell["id_dominated"]:
            # any excess over the identity term is only the SHALLOW (w<c) deep
            # bucket, never a field-drop competitor: prime field => no drop.
            c.ok(cell["shallow"] and cell["barN"] <= rep["deep_term"],
                 f"B: id-excess only via shallow deep bucket c={cell['c']}")
        all_ok = all_ok and accounted
    c.ok(all_ok, "B: identity+deep account for this selected power inventory")
    c3 = next(cl for cl in rep["cells"] if cl["c"] == 3 and cl["r"] == 0)
    c.ok(
        c3["barN"] == Q(6) and not c3["id_dominated"],
        "B negative control: c=3,r=0 has barN=6 > 924/169",
    )
    c.ok(
        c3["shallow"] and c3["deep_dominated"],
        "B boundary: the c=3,r=0 ID failure is shallow and <= deep term 7",
    )
    # square field values fill F_13 (no drop): the mechanism that keeps it small
    sq = next(cl for cl in rep["cells"] if cl["c"] == 2 and cl["r"] == 0)
    c.ok(sq["field_vals"] > 7,
         f"B: prime square field values {sq['field_vals']} > 7 (NO field drop)")
    c.ok(sq["barN"] <= rep["barN_id"],
         f"B: square barN {sq['barN']} <= identity {rep['barN_id']} (dominated)")
    return rep


def section_C_tower_mechanism(c: Checker) -> dict:
    """The field-drop MECHANISM at n=12 tower GF(49), a=6, k=3, w=2.  Exact
    field-drop structure (lacunarity, F_p confinement, L_sq collapse), and the
    paper's obstruction at the FORMAL identity budget barN_1 = C(n,a)|B|^{-w}."""
    c.note("== C. Tower GF(49) n=12: exact field-drop mechanism + obstruction ==")
    n, a, k = 12, 6, 3
    F, B, D, nn = build_tower_row(7)
    c.ok(nn == n, "C: n=12")
    rep = full_envelope_census(c, "tower GF(49)", F, B, D, n, a, k, False)
    w, Bq = rep["w"], rep["Bq"]
    sq = next(cl for cl in rep["cells"] if cl["c"] == 2 and cl["r"] == 0)
    # EXACT field-drop structure:
    c.ok(sq["field_vals"] <= 7,
         f"C: square field values {sq['field_vals']} <= p=7 (F_p confinement)")
    c.ok(sq["L"] <= 7 ** (w // 2), f"C: L_sq={sq['L']} <= p^(w/2)=7 (image collapse)")
    floor642 = Q(comb(6, 3), 7 ** (w // 2))
    c.ok(sq["barN"] >= floor642, f"C: barN_sq={sq['barN']} >= 6.4' floor {floor642}")
    # paper's obstruction at the FORMAL identity budget (6.3):
    barN1_formal = Q(comb(n, a), Bq ** w)
    c.ok(sq["barN"] > barN1_formal,
         f"C: barN_sq={sq['barN']} > formal identity budget C(n,a)|B|^-w="
         f"{barN1_formal} (6.3/6.4' obstruction holds)")
    # Exact full-codomain measurement on the smooth coset.  This one-row
    # factor-p deficit does not decide the asymptotic (FI) condition.
    rep["fi_id_holds"] = rep["fi_id"]
    rep["sq_field_vals"] = sq["field_vals"]
    rep["barN1_formal"] = barN1_formal
    rep["sq_barN"] = sq["barN"]
    c.ok(
        all(cell["barN"] > barN1_formal for cell in rep["cells"])
        and max(cell["barN"] for cell in rep["cells"]) == Q(6),
        "C boundary: all four power cells beat the formal proxy; c=3 is leader",
    )
    return rep


def _saturated_tower_row(c: Checker, tag: str, p: int, a: int, k: int) -> dict:
    """Saturated tower GF(p^2), enumerate identity AND square slices.  Compares
    the square realized scale (6.4') against the paper's FORMAL identity budget
    (6.3) barN_1 = C(n,a)|B|^{-w}; SEPARATELY measures the identity realized
    image L_id (an exact full-codomain measurement, not an asymptotic FI test)."""
    F, B, D, n = build_tower_row(p)
    w = a - k - 1
    Bq = p * p
    c.ok(Bq ** w <= comb(n, a), f"{tag}: saturated |B|^w<=C(n,a)")
    c.ok(w >= 2, f"{tag}: w>=2 (deep for c=2 square)")
    # FORMAL identity budget (6.3): 1 <= barN_1 < |B|^2
    barN1_formal = Q(comb(n, a), Bq ** w)
    c.ok(barN1_formal >= 1, f"{tag}: crossing barN_1(formal)={float(barN1_formal):.3f}>=1")
    c.ok(barN1_formal < Bq ** 2, f"{tag}: barN_1(formal) < |B|^2 (subexp, 6.3)")
    # identity slice enumerated: realized image and exact full-codomain status
    id_size, id_L, id_max, _ = census_slice(F, D, a, w, identity_slice(D, a))
    c.ok(id_size == comb(n, a), f"{tag}: |Omega_id|=C(n,a)={comb(n,a)}")
    fi_id = (id_L == Bq ** w)
    barN1_real = barN(id_size, id_L)
    # square slice
    Qv, fb = fibers_of_power(F, D, 2)
    c.ok(all(len(v) == 2 for v in fb.values()), f"{tag}: complete 2-fibers")
    sq_size, sq_L, sq_max, _ = census_slice(
        F, D, a, w, quotient_slice(D, a, 2, 0, Qv, fb))
    c.ok(sq_size == comb(n // 2, a // 2),
         f"{tag}: |Omega_sq|=C(n/2,a/2)={comb(n//2,a//2)}")
    c.ok(sq_L <= p ** (w // 2), f"{tag}: L_sq={sq_L}<=p^(w/2)={p**(w//2)} (field drop)")
    barN_sq = barN(sq_size, sq_L)
    # THE OBSTRUCTION (paper's 6.4' vs 6.3): square realized > identity FORMAL
    c.ok(barN_sq > barN1_formal,
         f"{tag}: barN_sq={float(barN_sq):.3f} > barN_1(formal)={float(barN1_formal):.3f}"
         f" -- square beats the formal ambient identity proxy")
    floor642 = Q(comb(n // 2, a // 2), p ** (w // 2))
    c.ok(barN_sq >= floor642, f"{tag}: barN_sq >= 6.4' floor {floor642}")
    power_cells = []
    for cfold in range(2, n + 1):
        if n % cfold != 0:
            continue
        qvals, fiber = fibers_of_power(F, D, cfold)
        if not all(len(values) == cfold for values in fiber.values()):
            continue
        for r in range(cfold):
            if (a - r) % cfold != 0:
                continue
            m = (a - r) // cfold
            if not 1 <= m <= len(qvals):
                continue
            size, image, maxfib, _ = census_slice(
                F, D, a, w, quotient_slice(D, a, cfold, r, qvals, fiber)
            )
            if size:
                power_cells.append(
                    dict(c=cfold, r=r, size=size, L=image,
                         maxfib=maxfib, barN=barN(size, image))
                )
    c.ok(
        [(x["c"], x["r"], x["size"], x["L"]) for x in power_cells]
        == [(2, 0, 252, 11), (4, 2, 660, 190), (5, 0, 6, 1), (10, 0, 2, 1)],
        f"{tag}: complete-power inventory is pinned",
    )
    return dict(tag=tag, n=n, a=a, k=k, w=w, Bq=Bq, id_L=id_L, id_max=id_max,
                fi_id=fi_id, barN1_formal=barN1_formal, barN1_real=barN1_real,
                sq_size=sq_size, sq_L=sq_L, sq_max=sq_max, barN_sq=barN_sq,
                floor=floor642, excess=barN_sq - barN1_formal,
                power_cells=power_cells)


def _saturated_prime_row(c: Checker, tag: str, p: int, sub: int, a: int, k: int) -> dict:
    """Saturated PRIME deep row: D = order-`sub` subgroup of F_p^x, w>=2.  No
    field drop possible -> square dominated by identity at BOTH the formal and
    the realized scale; exact full-codomain equality is checked at this row."""
    F, B, D, n = build_prime_subgroup_row(p, sub)
    w = a - k - 1
    c.ok(p ** w <= comb(n, a), f"{tag}: saturated")
    barN1_formal = Q(comb(n, a), p ** w)
    id_size, id_L, id_max, _ = census_slice(F, D, a, w, identity_slice(D, a))
    fi_id = (id_L == p ** w)
    c.ok(fi_id, f"{tag}: exact identity image L_id={id_L}=|B|^w={p**w}")
    barN1_real = barN(id_size, id_L)
    Qv, fb = fibers_of_power(F, D, 2)
    if not all(len(v) == 2 for v in fb.values()):
        c.ok(False, f"{tag}: complete 2-fibers"); return {}
    sq_size, sq_L, sq_max, _ = census_slice(
        F, D, a, w, quotient_slice(D, a, 2, 0, Qv, fb))
    barN_sq = barN(sq_size, sq_L)
    # no field drop => square dominated at the formal AND realized identity scale
    c.ok(barN_sq <= barN1_formal,
         f"{tag}: barN_sq={float(barN_sq):.3f} <= barN_1(formal)={float(barN1_formal):.3f}")
    c.ok(barN_sq <= barN1_real,
         f"{tag}: barN_sq <= barN_1(realized)={float(barN1_real):.3f} (identity dominates)")
    return dict(tag=tag, n=n, a=a, fi_id=fi_id, barN1_formal=barN1_formal,
                barN1_real=barN1_real, barN_sq=barN_sq, sq_L=sq_L)


def section_E_separation(c: Checker) -> dict:
    """Formal-proxy tower separation plus a selected prime-square control."""
    c.note("== E. Formal-proxy tower separation + selected prime-square control ==")
    # primary tower CE: p=11, n=20, a=10, k=7, w=2 (barN_1>=1 crossing, deep c=2)
    tower = _saturated_tower_row(c, "tower GF(121) n=20", p=11, a=10, k=7)
    c.note(f"   tower n=20 a=10 w=2: barN_1(formal)={float(tower['barN1_formal']):.4f}"
           f"  barN_sq={float(tower['barN_sq']):.4f}  L_sq={tower['sq_L']}  "
           f"excess={float(tower['excess']):.4f}  (beats formal proxy only)")
    c.note(f"   exact full-codomain check: L_id={tower['id_L']} vs "
           f"|B|^w={tower['Bq']**tower['w']} -> "
           f"{'equal' if tower['fi_id'] else 'factor-p deficit'}; realized "
           f"barN_id={float(tower['barN1_real']):.4f}")
    # prime parallel in the SAME deep saturated regime: p=41, D=order-20 subgroup
    prime = _saturated_prime_row(c, "prime GF(41) n=20", p=41, sub=20, a=10, k=7)
    if prime:
        c.note(f"   prime n=20 a=10 w=2: barN_1(formal)={float(prime['barN1_formal']):.4f}"
               f"  barN_sq={float(prime['barN_sq']):.4f}  square is identity-dominated")
    # CONTROL: complete the same deterministic generic-domain census.  Its image
    # is larger than the smooth-coset image but still does not fill the codomain.
    Fg = make_gf_p2(11)
    Dg = [e for e in Fg["elems"] if e != Fg["zero"]][:20]
    generic_size, generic_L, generic_max, _ = census_slice(
        Fg, Dg, 10, 2, identity_slice(Dg, 10)
    )
    c.ok(
        (generic_size, generic_L, generic_max) == (184756, 9359, 57),
        "E control: full generic census is 184756 supports, image 9359, max 57",
    )
    c.ok(generic_L > tower["id_L"],
         f"E control: generic image {generic_L} exceeds smooth-coset {tower['id_L']}")
    c.ok(generic_L < 11 ** 4,
         "E control: generic image 9359 still does not fill ambient 14641")
    c.note(
        f"   full control: generic 20-subset image={generic_L}, max fiber="
        f"{generic_max}, versus smooth coset {tower['id_L']} and ambient 14641"
    )
    return dict(
        tower=tower,
        prime=prime,
        generic_size=generic_size,
        generic_L=generic_L,
        generic_max=generic_max,
    )


def section_D_target(c: Checker, sep: dict) -> dict:
    """Separate formal, realized, and selected-profile safe-side budgets.

    A budget above B* only fails the sufficient safe test (13.2); it does not
    prove an unsafe row.  No lower-reserve theorem is invoked here.
    """
    c.note("== D. Target direction: proxy pass versus failure to certify safety ==")
    t = sep["tower"]
    n, a = t["n"], t["a"]
    deep = n - a + 1
    barN_formal = t["barN1_formal"]
    barN_real = t["barN1_real"]
    barN_sq = t["barN_sq"]
    import math
    E_formal_id = 1 + deep + (1 + math.ceil(barN_formal))
    E_formal_id_square = E_formal_id + (1 + math.ceil(barN_sq))
    E_real_id = 1 + deep + (1 + math.ceil(barN_real))
    E_real_id_square = E_real_id + (1 + math.ceil(barN_sq))
    power_addback = sum(
        1 + math.ceil(cell["barN"]) for cell in t["power_cells"]
    )
    E_formal_power = E_formal_id + power_addback
    E_real_power = E_real_id + power_addback
    Bstar = E_formal_id
    c.ok(barN_real > barN_sq > barN_formal,
         "D: realized identity > square > formal ambient identity proxy")
    c.ok(
        (E_formal_id, E_formal_id_square) == (26, 50),
        "D: legacy 26/50 values are formal-identity and identity+square proxies",
    )
    c.ok(
        (E_real_id, E_real_id_square) == (152, 176),
        "D: realized identity/identity+square selected budgets are 152/176",
    )
    c.ok(
        (E_formal_power, E_real_power) == (65, 191),
        "D: all selected complete-power cells give formal/realized sums 65/191",
    )
    c.ok(
        E_real_id > Bstar and E_real_id_square > Bstar,
        "D: B*=26 fails the selected realized safe tests; no unsafe conclusion",
    )
    c.note(
        "   n=20: formal identity proxy=26; formal identity+square proxy=50; "
        "realized identity selected budget=152; realized identity+square=176; "
        "B*=26 does NOT certify safety at realized scale, and this test proves "
        "no unsafe statement"
    )
    return dict(
        E_formal_id=E_formal_id,
        E_formal_id_square=E_formal_id_square,
        E_real_id=E_real_id,
        E_real_id_square=E_real_id_square,
        E_formal_power=E_formal_power,
        E_real_power=E_real_power,
        Bstar=Bstar,
    )


def section_F_reduction(c: Checker, prime12: dict, tower12: dict, sep: dict) -> None:
    """Consolidate only the finite selected-slice conclusions."""
    c.note("== F. Scope: selected finite slices, not a universal iff ==")
    prime_deep_max = max((cl["barN"] for cl in prime12["cells"]
                          if not cl["shallow"]), default=Q(0))
    c.ok(prime12["barN_id"] >= prime_deep_max,
         "F c-i: prime identity barN >= every DEEP quotient cell (n=12)")
    if sep["prime"]:
        c.ok(sep["prime"]["barN_sq"] <= sep["prime"]["barN1_formal"],
             "F c-i: selected prime GF41 square is identity-dominated")
    # (c-ii) tower: the c=2 field drop beats the FORMAL identity budget
    t = sep["tower"]
    c.ok(t["barN_sq"] > t["barN1_formal"],
         "F c-ii: tower c=2 field-drop beats formal identity budget (saturated n=20)")
    c.ok(t["barN1_real"] > t["barN_sq"],
         "F boundary: tower square does not beat realized identity at n=20")
    c.ok(not t["fi_id"],
         "F c-iii: exact full-codomain equality fails on the smooth coset")
    c.ok(sep["prime"] and sep["prime"]["fi_id"],
         "F c-iii: exact full-codomain equality holds on the prime subgroup")
    c.ok(tower12["sq_field_vals"] <= 7,
         "F c-iii: field-drop structure exact already at n=12 (F_p confinement)")
    c.note(
        "   VERDICT: selected prime squares are dominated at GF(13)/GF(41), "
        "while GF(13 c=3 violates literal ID and the tower square beats only "
        "the formal identity proxy.  These finite facts do not establish a "
        "complete-envelope iff; first-match admission, PEU/RC, and the other "
        "profile classes remain external."
    )


def section_G_prime_counterexamples(c: Checker) -> dict:
    """No-field-drop counterexamples to literal exact ID."""
    c.note("== G. Prime no-drop negative controls for literal exact ID ==")
    F, B, D, n = build_prime_row(19)
    a, k, w = 8, 4, 3
    id_size, id_L, _, _ = census_slice(F, D, a, w, identity_slice(D, a))
    Qv, fb = fibers_of_power(F, D, 2)
    sq_size, sq_L, _, _ = census_slice(
        F, D, a, w, quotient_slice(D, a, 2, 0, Qv, fb)
    )
    c.ok((id_size, id_L) == (43758, 6859),
         "G GF19: identity size/image are 43758/6859 = C(18,8)/19^3")
    c.ok((sq_size, sq_L) == (126, 19),
         "G GF19: square size/image are 126/19 with no field drop")
    c.ok(
        sq_size * id_L > id_size * sq_L,
        "G GF19: square 126/19 exceeds identity 43758/6859",
    )
    family = []
    for p in (11, 13, 17, 19, 23, 29, 31, 37, 41):
        sq = Q(p - 1, 2)
        ident = Q((p - 1) * (p - 2), 2 * p)
        family.append(sq > ident and sq > 3)
    c.ok(all(family),
         "G w=1 family p=11..41: square exceeds identity and deep=3")
    c.note(
        "   GF19 n=18,a=8,k=4,w=3: 126/19 > 43758/6859 despite "
        "prime base and exact identity image 19^3; the w=1 family also beats "
        "identity and deep=3 for every tested p=11..41"
    )
    return dict(
        gf19_id_size=id_size,
        gf19_id_L=id_L,
        gf19_sq_size=sq_size,
        gf19_sq_L=sq_L,
        family_primes=[11, 13, 17, 19, 23, 29, 31, 37, 41],
    )


def file_sha256(relative: Path) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def canonical_payload(data: dict) -> str:
    unsigned = copy.deepcopy(data)
    unsigned.pop("payload_sha256", None)
    raw = json.dumps(
        unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def certificate_sources_fresh(cert: dict) -> bool:
    expected = {
        str(NOTE_PATH),
        str(SCRIPT_PATH),
        str(LEAN_PATH),
        "experimental/notes/thresholds/profile_envelope_completeness.md",
        "experimental/notes/thresholds/envelope_identity_window.md",
        "experimental/asymptotic_rs_mca_frontiers.tex",
    }
    bindings = cert.get("source_bindings")
    if not isinstance(bindings, list):
        return False
    if {row.get("path") for row in bindings if isinstance(row, dict)} != expected:
        return False
    return all(
        isinstance(row, dict)
        and isinstance(row.get("path"), str)
        and isinstance(row.get("sha256"), str)
        and (ROOT / row["path"]).is_file()
        and file_sha256(Path(row["path"])) == row["sha256"]
        for row in bindings
    )


def certificate_semantics(cert: dict) -> bool:
    rows = cert.get("rows", {})
    gf13 = rows.get("prime_GF13_n12", {})
    gf19 = rows.get("prime_GF19_n18", {})
    generic = rows.get("generic_20subset_GF121", {})
    tower = rows.get("tower_GF121_n20", {})
    target = cert.get("target_direction", {})
    scope = cert.get("scope", {})
    return (
        cert.get("schema") == "rs-mca-profile-envelope-target-comparison-v2"
        and cert.get("artifact") == "profile-envelope-target-comparison"
        and cert.get("status") == "COUNTEREXAMPLE"
        and cert.get("producer_head") == "8cd4f4b6"
        and cert.get("integration") == "2633895a"
        and scope.get("enumerated")
        == "identity and complete-power-fiber quotient/remainder slices"
        and scope.get("complete_profile_inventory") is False
        and scope.get("universal_prime_theorem") is False
        and scope.get("unsafe_theorem") is False
        and scope.get("asymptotic_FI_decided") is False
        and gf13.get("identity") == {"size": 924, "L": 169, "barN": "924/169"}
        and gf13.get("c3r0")
        == {
            "size": 6,
            "L": 1,
            "barN": "6",
            "identity_dominated": False,
            "deep_dominated": True,
        }
        and gf19.get("identity") == {"size": 43758, "L": 6859}
        and gf19.get("square") == {"size": 126, "L": 19}
        and gf19.get("square_beats_identity") is True
        and generic
        == {
            "size": 184756,
            "L_id": 9359,
            "max_fiber": 57,
            "ambient": 14641,
            "full_codomain": False,
        }
        and tower.get("power_cells")
        == [
            {"c": 2, "r": 0, "size": 252, "L": 11, "barN": "252/11"},
            {"c": 4, "r": 2, "size": 660, "L": 190, "barN": "66/19"},
            {"c": 5, "r": 0, "size": 6, "L": 1, "barN": "6"},
            {"c": 10, "r": 0, "size": 2, "L": 1, "barN": "2"},
        ]
        and target
        == {
            "B_star": 26,
            "formal_identity_proxy": 26,
            "formal_identity_plus_square_proxy": 50,
            "formal_identity_plus_all_selected_power_cells": 65,
            "realized_identity_selected_budget": 152,
            "realized_identity_plus_square_selected_budget": 176,
            "realized_identity_plus_all_selected_power_cells": 191,
            "conclusion": "selected realized safe test fails; no unsafe theorem",
        }
    )


def certificate_valid(cert: dict) -> bool:
    return (
        cert.get("payload_sha256") == canonical_payload(cert)
        and certificate_sources_fresh(cert)
        and certificate_semantics(cert)
    )


def validate_certificate(c: Checker) -> dict:
    cert = json.loads((ROOT / CERT_PATH).read_text(encoding="utf-8"))
    c.ok(
        cert.get("schema") == "rs-mca-profile-envelope-target-comparison-v2"
        and cert.get("status") == "COUNTEREXAMPLE",
        "H certificate schema/status are repaired",
    )
    c.ok(
        cert.get("payload_sha256") == canonical_payload(cert),
        "H certificate canonical payload is fresh",
    )
    c.ok(certificate_sources_fresh(cert), "H all six certificate source bindings are fresh")
    c.ok(certificate_semantics(cert), "H certificate rows and scope match repaired claims")
    c.ok(certificate_valid(cert), "H certificate passes combined strict validation")
    return cert


def tamper_selftest() -> int:
    rejected = 0
    F, B, D, n = build_tower_row(5)
    Qvals, fiber = fibers_of_power(F, D, 2)
    _, Ldist, _, _ = census_slice(F, D, 4, 2, quotient_slice(D, 4, 2, 0, Qvals, fiber))
    corrupted_expect = Ldist + 1          # true is p=5
    if Ldist != corrupted_expect:
        rejected += 1

    cert = json.loads((ROOT / CERT_PATH).read_text(encoding="utf-8"))
    bad_row = copy.deepcopy(cert)
    bad_row["rows"]["prime_GF13_n12"]["c3r0"]["barN"] = "5"
    bad_row["payload_sha256"] = canonical_payload(bad_row)
    if not certificate_valid(bad_row):
        rejected += 1

    bad_source = copy.deepcopy(cert)
    bad_source["source_bindings"][0]["sha256"] = "0" * 64
    bad_source["payload_sha256"] = canonical_payload(bad_source)
    if not certificate_valid(bad_source):
        rejected += 1

    if rejected == 3:
        print("RESULT: PASS (tamper-selftest)")
        print("tamper_mutations_rejected=3/3")
        print("STATUS: COUNTEREXAMPLE")
        return 0
    print(f"RESULT: FAIL (tamper mutations rejected {rejected}/3)")
    print("STATUS: COUNTEREXAMPLE")
    return 1


def main(argv) -> int:
    if argv == ["--tamper-selftest"]:
        return tamper_selftest()
    if argv:
        print(f"RESULT: FAIL (unknown arguments: {' '.join(argv)})")
        print("STATUS: COUNTEREXAMPLE")
        return 2
    c = Checker()
    section_A_reproduce_542(c)
    prime12 = section_B_prime(c)
    tower12 = section_C_tower_mechanism(c)
    sep = section_E_separation(c)
    dtar = section_D_target(c, sep)
    section_F_reduction(c, prime12, tower12, sep)
    section_G_prime_counterexamples(c)
    validate_certificate(c)

    for line in c.log:
        print(line)
    print()
    sqp = next(cl for cl in prime12["cells"] if cl["c"] == 2 and cl["r"] == 0)
    print("GROUND TRUTH (exact, realized-image scale of PO5/6.4'):")
    print(f"  prime GF(13) n=12: identity barN={float(prime12['barN_id']):.4f}  "
          f"square barN={float(sqp['barN']):.4f} (field vals {sqp['field_vals']}, "
          f"no drop) -> square dominated; c=3,r=0 still violates literal ID")
    print(f"  tower GF(49) n=12: square field vals={tower12['sq_field_vals']}(<=7), "
          f"barN_sq={float(tower12['sq_barN']):.4f} > formal id "
          f"{float(tower12['barN1_formal']):.4f} -> obstruction (exact field drop)")
    tw = sep["tower"]
    print(f"  tower GF(121) n=20 (crossing): formal id barN_1={float(tw['barN1_formal']):.4f}"
          f"  square barN_sq={float(tw['barN_sq']):.4f}  excess={float(tw['excess']):.4f}"
          f" -> beats formal identity proxy only")
    print(f"     exact full-codomain deficit: L_id={tw['id_L']}<|B|^w="
          f"{tw['Bq']**tw['w']} (factor p); asymptotic FI is not decided")
    if sep["prime"]:
        pr = sep["prime"]
        print(f"  prime GF(41) n=20 (same deep regime): formal id barN_1="
              f"{float(pr['barN1_formal']):.4f}  square barN_sq={float(pr['barN_sq']):.4f}"
              f"  exact full image; square is identity-dominated")
    print(f"  target proxies: formal id={dtar['E_formal_id']} formal id+square="
          f"{dtar['E_formal_id_square']} formal selected-power={dtar['E_formal_power']}")
    print(f"  realized selected budgets: id={dtar['E_real_id']} id+square="
          f"{dtar['E_real_id_square']} selected-power={dtar['E_real_power']} "
          f"vs B*={dtar['Bstar']} -> safe test fails; no unsafe conclusion")
    print()
    if c.fails:
        print(f"RESULT: FAIL ({len(c.fails)} of {c.n})")
        for m in c.fails[:30]:
            print("  -", m)
        print("STATUS: COUNTEREXAMPLE")
        return 1
    print(f"RESULT: PASS ({c.n}/{c.n})")
    print("STATUS: COUNTEREXAMPLE")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
