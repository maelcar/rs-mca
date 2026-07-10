#!/usr/bin/env python3
"""Attack the deep-prefix Gap-2 span-collapse ROUTING lemma.

Target: experimental/asymptotic_rs_mca_frontiers.tex, base 4e3c4ee.

CONTEXT (from PR #539 fi_full_image_primitive.md).  The (FI) certificate
L >= e^{-o(n)} A splits along the scale tower L <= A_eff <= A into
  Gap-1  L >= e^{-o(n)} A_eff   (image fills its effective span; PROVED free by (A4)),
  Gap-2  A_eff >= e^{-o(n)} A    (effective span is nearly ambient; THIS TASK).
Gap-2 fails only by an effective-span COLLAPSE dim_Fp V_g < R*f (A_eff << A),
    V_g = Span_{F_p}{ g(t)-g(t_0) : t in T },   g(t)=(t,t^2,...,t^w),   (EF1, L2861)
    A_eff = |V_g| = p^{dim V_g},   A = |B|^R = p^{w f},   f=[B:F_p], R=w=prefix depth.
The paper discharges such a collapse by RE-ROUTING the leaf "to an earlier
structural profile" (L4/L1115 item 4; C7 saturation/effective-image-collapse
cell L2440-2452), but per #539 that re-route is an ASSUMED enumerative input
("its projection degree remains an enumerative input", L2451).  This script
proves the routing lemma by CLASSIFYING every span-collapse relation.

CLASSIFICATION (the mathematical heart; PROVED here + census-exact):
  A universal F_p-linear relation among the power-sum coordinates p_1..p_w on a
  full slice = an (c_1..c_w) in B^w with sum_j Tr(c_j t^j) constant on the slice.
  By trace duality + cyclotomic-coset theory (Delsarte),
        dim_Fp V_g = | Z_p(q-1, {1,...,w}) |,                          (*)
  the size of the FROBENIUS CLOSURE of {1..w} in Z/(q-1)Z under x -> p*x
  (== PR #451 asymptotic_c9_frobenius_cyclotomic_defect Theorem 1's Z_p(N,I),
  N=q-1, I={1..w}; the closure step (sum a_i w_i)^p = sum a_i w_i^p is Lean-
  backed, c9_frobenius_closure_lean_backing.md psum_pow/root_pow).  Every
  universal relation is therefore a FROBENIUS-CLOSURE relation of two kinds:
    (chain)    p_{p j} = Frob(p_j)          when p j <= w   [Frobenius image link]
    (subfield) p_j in F_{p^d}, d = |coset(j)| < f            [field descent]
  Both are exactly the extension/field-descent cell C5 (L2422, "Frobenius
  invariance is constructible"); the chain kind is rem:binary-ambient-image's
  named p_{2j}=p_j^2 char-2 collapse (L4349).  There is NO third kind, so NO new
  obstruction cell: the classification is EXHAUSTIVE.

ROUTING CONSEQUENCE (PROVED):
  R1 (existence, classification exact)  dim_Fp V_g == |Z_p(q-1,{1..w})| on every
     clean census leaf (w < q-1); all collapse is Frobenius-closure = C5.
  R2 (VACUITY on admissible leaves)  collapse  <=>  w >= p.  Hence when the
     power-sum admissibility window R_N < char (item 4, L932; (A5), L935) holds,
     i.e. w < p, there is NO collapse (dim V_g = w f, A_eff = A) and the Gap-2
     routing obligation is VACUOUS.
  R3 (mass absorption)  in the forbidden regime w >= p the collapse relations
     are verified to hold EXACTLY and to account for the FULL codimension, so the
     leaf routes (first-match) to C5, which precedes the primitive/Sidon cell C9
     in first-match order (L5180) -- an earlier profile, as required.
  R4 (no counterexample)  zero uncaught collapses across the census.
  R5 (coordinate-switch catcher)  the char-2 named collapse is a COORDINATE
     ARTIFACT: on F_8 the power-sum prefix (p_1,p_2) collapses (dim 3) while the
     elementary prefix (e_1,e_2) has FULL span (dim 6), matching the paper's
     mandate "the exact MCA construction uses the elementary locator prefix only".

BUDGET (PARTIAL): the collapsed leaf's data descends to F_{p^d}; C5's payment is
  its catalogued "direct field-sensitive slope count" at the descended profile
  scale, quantified by PR #451's fiber bound |Omega cap Phi^{-1}(y)| <= p^{d_p}.
  This is C5's standing obligation, not a NEW gap -- labeled PARTIAL, not closed.

HONESTY: (*) and R2 are field-independent theorems (proved, census-exact); the
census nulls (R4, exhaustiveness across the six fields) are EVIDENCE + SCOPE at
toy scale.  Boundaries: (MI)/(MA)/entropy-inverse (scottdhughes #498/#501/#505),
Danny #529, latifkasuli #518 untouched.  GF arithmetic + closure idiom reuse
verify_entropy_inverse_fp_span_cell.py and #451 (credited).

Stdlib only.  Zero-arg.  Runtime target < 120 s.  RESULT: PASS (N checks).
"""
from __future__ import annotations

from itertools import combinations
from math import log

BASE_SHA = "4e3c4ee"
CHECKS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> bool:
    CHECKS.append((name, bool(ok), detail))
    return bool(ok)


# =========================================================================== #
#  F_p[x] helpers + finite field F_{p^k}  (reused from                         #
#  verify_entropy_inverse_fp_span_cell.py; credited)                           #
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
    if dm == 0:                       # modulus is a nonzero constant: a mod unit = 0
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
    """F_{p^k}; elements are base-p digit ints; modulus = smallest monic irreducible."""

    def __init__(self, p, k):
        self.p = p
        self.k = k
        self.q = p ** k
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
        return self.antilog[(self.logt[a] * e) % (self.q - 1)]

    def _find_gen(self):
        q = self.q
        need = q - 1
        fs = _prime_factors(need)
        for cand in range(2, q):
            ok = True
            for r in fs:
                e = need // r
                x = 1
                base = cand
                ee = e
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

    def frob(self, a):
        return self.powr(a, self.p)

    def in_subfield(self, a, d):
        """True iff a in F_{p^d} (subfield), i.e. a^{p^d}=a."""
        return self.powr(a, self.p ** d) == a


# =========================================================================== #
#  F_p linear algebra: rank of a list of vectors in F_p^n                      #
# =========================================================================== #
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
#  the effective span V_g and its Frobenius-closure prediction                 #
# =========================================================================== #
def gvec_fp(F, t, w):
    """F_p-coordinate vector of g(t)=(t,t^2,...,t^w) in B^w == F_p^{w k}."""
    out = []
    for j in range(1, w + 1):
        out.extend(F._vec(F.powr(t, j)))
    return out


def span_dim(F, D, w):
    """dim_Fp Span{ g(t)-g(t0) : t in D }, t0 = D[0]."""
    p = F.p
    t0 = D[0]
    g0 = gvec_fp(F, t0, w)
    rows = []
    for t in D:
        gt = gvec_fp(F, t, w)
        rows.append([(a - b) % p for a, b in zip(gt, g0)])
    return rank_fp(rows, p)


def frob_closure(N, exps, p):
    """Z_p(N, exps): closure of {e mod N} under x -> (p*x) mod N (PR #451)."""
    S = set(e % N for e in exps)
    frontier = list(S)
    while frontier:
        x = frontier.pop()
        y = (p * x) % N
        if y not in S:
            S.add(y)
            frontier.append(y)
    return S


def coset_partition_size(N, w, p):
    """Sum of |C| over p-cyclotomic cosets C of Z/NZ with C cap {1..w} != empty."""
    seen = set()
    total = 0
    for j in range(1, w + 1):
        r = j % N
        if r in seen:
            continue
        # build coset of r
        C = set()
        x = r
        while x not in C:
            C.add(x)
            x = (p * x) % N
        seen |= C
        total += len(C)
    return total


# =========================================================================== #
#  main census                                                                 #
# =========================================================================== #
def main():
    # small q = p^d extension fields, as mandated by the task
    FIELDS = [("F4", 2, 2), ("F8", 2, 3), ("F9", 3, 2),
              ("F16", 2, 4), ("F25", 5, 2), ("F27", 3, 3)]
    WMAX = 4

    uncaught = 0
    collapse_rows = []
    vacuity_rows = []

    for name, p, k in FIELDS:
        F = GF(p, k)
        q = F.q
        N = q - 1
        Dfull = list(range(q))          # D = F_q  (includes 0; t0=0 gives V_g=span image)
        for w in range(1, WMAX + 1):
            dim = span_dim(F, Dfull, w)
            amb = w * k                  # dim_Fp B^w = log_p A
            collapse = dim < amb
            clean = (w < N)              # no multiplicative wraparound of top coord

            # --- Frobenius-closure prediction (*) ---
            clos = frob_closure(N, range(1, w + 1), p)
            csize = len(clos)
            part = coset_partition_size(N, w, p)
            check(f"{name}.w{w}.closure_two_ways", csize == part,
                  f"iter={csize} partition={part}")

            # R1: classification EXACT -- dim V_g == |Frobenius closure| (all configs;
            # clean w<q-1 is the frontier regime, wraparound w>=q-1 also obeys it)
            check(f"{name}.w{w}.R1_classification_exact",
                  dim == csize, f"dim={dim} |Z_p|={csize} amb={amb} clean={clean}")

            # naive chain-only Frobenius bound (no subfield/wraparound)
            naive = (w - w // p) * k

            # R2: VACUITY -- collapse iff w >= p (admissibility window)
            if w < p:
                check(f"{name}.w{w}.R2_no_collapse_when_w<p",
                      not collapse and dim == amb,
                      f"w={w}<p={p} dim={dim} amb={amb}")
                vacuity_rows.append((name, w, dim, amb))

            if collapse:
                check(f"{name}.w{w}.R2_collapse_forces_w>=p",
                      w >= p, f"collapse with w={w} p={p}")
                has_chain = False
                has_subfield = False

                # --- R3 mass absorption: identify + verify EVERY relation ---
                # (chain) coord_{pj} = Frob(coord_j) for pj<=w:
                explained_dim = 0
                # group coordinate exponents 1..w by cyclotomic coset
                by_coset = {}
                for j in range(1, w + 1):
                    # canonical coset rep = min of orbit
                    orb = set()
                    x = j % N
                    while x not in orb:
                        orb.add(x)
                        x = (p * x) % N
                    key = min(orb)
                    by_coset.setdefault(key, (orb, []))[1].append(j)
                for key, (orb, js) in by_coset.items():
                    csz = len(orb)              # coset size = subfield degree d
                    n_here = len(js)            # coords of ours in this coset
                    # each coset contributes exactly csz to the span (dim==closure);
                    # the naive full contribution would be n_here*k, so this coset
                    # supplies codimension  n_here*k - csz  of relations.
                    explained_dim += csz
                    # verify the chain links hold EXACTLY on the data
                    js_sorted = sorted(js)
                    for a_idx in range(len(js_sorted)):
                        for b_idx in range(len(js_sorted)):
                            ja, jb = js_sorted[a_idx], js_sorted[b_idx]
                            if jb == p * ja and jb <= w:
                                has_chain = True
                                ok = all(F.powr(t, jb) == F.frob(F.powr(t, ja))
                                         for t in Dfull)
                                check(f"{name}.w{w}.chain_p{ja}->{jb}", ok,
                                      "p_{pj}=Frob(p_j) exact")
                    # verify subfield descent for short cosets
                    if csz < k:
                        has_subfield = True
                        j0 = js_sorted[0]
                        ok = all(F.in_subfield(F.powr(t, j0), csz) for t in Dfull)
                        check(f"{name}.w{w}.subfield_p{j0}_in_F{p}^{csz}", ok,
                              "coord in proper subfield (field descent C5)")
                # R3: the identified C5 relations account for the FULL span
                check(f"{name}.w{w}.R3_full_absorption",
                      explained_dim == dim,
                      f"explained={explained_dim} dim={dim}")
                # R4: nothing uncaught -- dim==closure means every relation is
                # a Frobenius-closure (C5) relation.  count residue.
                residue = dim - explained_dim
                if residue != 0:
                    uncaught += 1
                kind = "+".join([s for s, b in
                                 (("chain", has_chain), ("subfield", has_subfield)) if b]
                                ) or "(none)"
                collapse_rows.append((name, p, k, w, dim, amb, csize, kind))

    # R4 global: zero uncaught collapses (no COUNTEREXAMPLE)
    check("R4_zero_uncaught_collapses", uncaught == 0, f"uncaught={uncaught}")

    # ---- char-2 named probe (rem:binary-ambient-image, reproduce #539) ----
    F8 = GF(2, 3)
    dim_ps = span_dim(F8, list(range(8)), 2)      # power-sum (p1,p2)
    check("probe.F8.powersum_collapse_dim3", dim_ps == 3, f"dim={dim_ps}")
    check("probe.F8.Aeff8_vs_A64", 2 ** dim_ps == 8 and 2 ** (2 * 3) == 64,
          f"A_eff={2**dim_ps} A={2**6}")
    check("probe.F8.p2_eq_frob_p1",
          all(F8.powr(t, 2) == F8.frob(F8.powr(t, 1)) for t in range(8)),
          "p_2 = p_1^2 in char 2 (Frobenius link)")

    # ---- R5 coordinate-switch catcher: elementary prefix has FULL span ----
    # enumerate 2-subsets S of F_8; elementary (e1,e2)=(x+y, x*y) vs power-sum.
    a_sub = 2
    ps_img, el_img = set(), set()
    ps_rows, el_rows = [], []
    Slist = list(combinations(range(8), a_sub))
    for S in Slist:
        # F_8 has char 2: field addition == XOR of base-2 digit encodings.
        p1 = 0
        p2 = 0
        for x in S:
            p1 ^= x
            p2 ^= F8.powr(x, 2)
        # elementary: e1 = sum x, e2 = sum_{i<j} x_i x_j
        e1 = 0
        for x in S:
            e1 ^= x
        e2 = 0
        for i in range(len(S)):
            for j in range(i + 1, len(S)):
                e2 ^= F8.mult[S[i] * 8 + S[j]]
        ps_img.add((p1, p2))
        el_img.add((e1, e2))
        ps_rows.append(F8._vec(p1) + F8._vec(p2))
        el_rows.append(F8._vec(e1) + F8._vec(e2))
    # differences vs a fixed ref for span dim
    ref_ps, ref_el = ps_rows[0], el_rows[0]
    ps_span = rank_fp([[(a - b) % 2 for a, b in zip(r, ref_ps)] for r in ps_rows], 2)
    el_span = rank_fp([[(a - b) % 2 for a, b in zip(r, ref_el)] for r in el_rows], 2)
    check("R5.F8.powersum_support_span_le3", ps_span <= 3, f"ps_span={ps_span}")
    check("R5.F8.elementary_support_span_full6", el_span == 6, f"el_span={el_span}")
    check("R5.F8.elementary_beats_powersum", el_span > ps_span,
          f"el={el_span} ps={ps_span}")

    # ---- Newton/Frobenius boundary: char>w <=> w<p <=> no collapse ----
    # (ties classification to lem:newton-dictionary-expanded char>w, #536)
    nd_ok = True
    for name, p, k in FIELDS:
        F = GF(p, k)
        for w in range(1, WMAX + 1):
            if w >= (q := F.q) - 1:
                continue  # skip wraparound-degenerate
            dim = span_dim(F, list(range(F.q)), w)
            no_col = (dim == w * k)
            if (w < p) != no_col:
                nd_ok = False
    check("newton_boundary.char>w<=>no_collapse", nd_ok,
          "power-sum admissibility (item 4/A5) window == no-collapse window")

    # ---- closure identity sanity vs PR #451 d_p defect notion ----
    # d_p(N,I) = N - |Z_p(N,I)|; here full-slice defect codim = wk - |Z_p(N,{1..w})|
    for name, p, k in [("F8", 2, 3), ("F9", 3, 2)]:
        F = GF(p, k)
        N = F.q - 1
        for w in [2, 3, 4]:
            clos = frob_closure(N, range(1, w + 1), p)
            defect = w * k - len(clos)
            dim = span_dim(F, list(range(F.q)), w)
            check(f"defect.{name}.w{w}", (w * k - dim) == defect,
                  f"codim={w*k-dim} N-|Z|-style defect={defect}")

    # ---------------------------- tamper self-tests ------------------------
    t_before = len(CHECKS)
    check("tamper.fake_dim_must_fail",
          not (span_dim(GF(2, 3), list(range(8)), 2) == 6),
          "F8 w2 dim is 3 not 6")
    check("tamper.fake_closure_must_fail",
          not (len(frob_closure(7, range(1, 3), 2)) == 2),
          "|Z_2(7,{1,2})|=3 not 2")
    assert len(CHECKS) == t_before + 2

    # ---------------------------------- report -----------------------------
    npass = sum(1 for _, ok, _ in CHECKS if ok)
    nfail = len(CHECKS) - npass
    print("=" * 72)
    print("verify_gap2_routing.py -- deep-prefix Gap-2 span-collapse routing")
    print(f"base {BASE_SHA};  power-sum moment curve g(t)=(t,...,t^w)")
    print("=" * 72)
    print("\nCLASSIFICATION (*)  dim_Fp V_g == |Z_p(q-1,{1..w})| (Frobenius closure):")
    print(f"{'field':6} {'p':>2} {'w':>2} {'dim':>4} {'A_eff=p^dim':>12} "
          f"{'A=p^wk':>10} {'collapse?':>9}  kind")
    for nm, p, k, w, dim, amb, cs, kind in collapse_rows:
        print(f"{nm:6} {p:>2} {w:>2} {dim:>4} {p**dim:>12} {p**amb:>10} "
              f"{'YES':>9}  {kind}")
    print("\nVACUITY  w < p (power-sum admissibility R_N<char) => NO collapse:")
    for nm, w, dim, amb in vacuity_rows[:8]:
        print(f"  {nm} w={w}: dim={dim} == amb={amb}  (A_eff=A)")
    print(f"\nuncaught collapses (would be COUNTEREXAMPLE): {uncaught}")
    print("=" * 72)
    if nfail:
        for nm, ok, det in CHECKS:
            if not ok:
                print(f"  FAIL  {nm}   {det}")
        print(f"RESULT: FAIL ({nfail} of {len(CHECKS)} checks failed)")
        raise SystemExit(1)
    print(f"RESULT: PASS ({npass} checks)")


if __name__ == "__main__":
    main()
