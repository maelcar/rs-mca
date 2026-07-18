#!/usr/bin/env python3
"""
Self-contained stdlib audit verifier for PR #905 (avdeevvadim):
"Uniform dense-shell transfer shape"
(experimental/notes/thresholds/dense_shell_transfer_shape.md, head 0000964).

Independent re-derivation, from the NOTE'S OWN definitions, of the scalar
gates an auditor checked by hand, plus the two master-composition
inequalities.  A small outward-rounded interval type carries a certified
radius through every transcendental, so single-point gates below are
rigorous.  Gates taken over a parameter interval are fine-grid
corroborations of the packet's continuum Arb gate and are labelled GRID;
the continuum / complex-domain rigor lives in the packet's 448-bit Arb
certificate (python-flint), which was NOT replayed here (python-flint
absent).

This script imports nothing outside the standard library and reads no
repository file, so it runs green on a tree that does NOT have pr-905
checked out.  The SHA256SUMS mismatch (finding S1) and the observed PASS of
pr-905's stdlib consumer verifier are recorded below as embedded data, not
re-executed.

Symbols (note sec.2, sec.6): B_n = tilde G_n; lambda = 241/500;
C = 1289/500; mu = sqrt(C); H(t) = mu*tan(mu*t); d(t) = -1/2 cos(2 pi t);
a'(t) = pi sin(2 pi t); a''(t) = 2 pi^2 cos(2 pi t).
"""
import math
import sys
from fractions import Fraction as Fr


def _p(x):
    return (abs(x) + 1.0) * 4e-16


class Iv:
    """Outward-rounded real interval [lo, hi]."""
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = lo
        self.hi = lo if hi is None else hi

    @staticmethod
    def frac(f):
        x = float(f)
        e = abs(x) * 2.4e-16 + 1e-300
        return Iv(x - e, x + e)

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __add__(self, o):
        o = _iv(o)
        lo = self.lo + o.lo
        hi = self.hi + o.hi
        return Iv(lo - _p(lo), hi + _p(hi))

    def __sub__(self, o):
        o = _iv(o)
        lo = self.lo - o.hi
        hi = self.hi - o.lo
        return Iv(lo - _p(lo), hi + _p(hi))

    def __mul__(self, o):
        o = _iv(o)
        c = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        lo, hi = min(c), max(c)
        return Iv(lo - _p(lo), hi + _p(hi))

    def recip(self):
        if self.lo <= 0.0 <= self.hi:
            raise ZeroDivisionError("interval spans 0")
        lo, hi = 1.0 / self.hi, 1.0 / self.lo
        return Iv(lo - _p(lo), hi + _p(hi))

    def __truediv__(self, o):
        return self * _iv(o).recip()

    def sqrt(self):
        return Iv(math.sqrt(self.lo) - 1e-15, math.sqrt(self.hi) + 1e-15)

    def _mono1(self, f):            # for sin/cos: |f'| <= 1
        mid = 0.5 * (self.lo + self.hi)
        w = 0.5 * (self.hi - self.lo)
        v = f(mid)
        r = w + _p(v) + 1e-15
        return Iv(v - r, v + r)

    def sin(self):
        return self._mono1(math.sin)

    def cos(self):
        return self._mono1(math.cos)

    def tan(self):                  # arguments here are < pi/2, cos > 0
        return self.sin() / self.cos()

    def exp(self):                  # monotone increasing
        lo, hi = math.exp(self.lo), math.exp(self.hi)
        return Iv(lo - _p(lo), hi + _p(hi))

    def __radd__(self, o):
        return _iv(o).__add__(self)

    def __rsub__(self, o):
        return _iv(o).__sub__(self)

    def __rmul__(self, o):
        return _iv(o).__mul__(self)

    def __rtruediv__(self, o):
        return _iv(o).__truediv__(self)


def _iv(x):
    if isinstance(x, Iv):
        return x
    if isinstance(x, Fr):
        return Iv.frac(x)
    return Iv.frac(Fr(x))


# ---- exact/rational constants and the note's functions (sec.2, sec.6) ----
PI = Iv(math.pi - 1e-15, math.pi + 1e-15)
ONE, TWO, THREE = Iv.frac(Fr(1)), Iv.frac(Fr(2)), Iv.frac(Fr(3))
HALF = Iv.frac(Fr(1, 2))
LAM = Iv.frac(Fr(241, 500))         # lambda = 241/500
CC = Iv.frac(Fr(1289, 500))         # C = 1289/500
MU = CC.sqrt()                       # mu = sqrt(C)


def d(t):
    return -(HALF * (TWO * PI * t).cos())


def ap(t):                          # a'(t) = pi sin(2 pi t)
    return PI * (TWO * PI * t).sin()


def app(t):                         # a''(t) = 2 pi^2 cos(2 pi t)
    return TWO * PI * PI * (TWO * PI * t).cos()


def H(t, mu=MU):                    # H(t) = mu tan(mu t)
    return mu * (mu * t).tan()


def fr(a, b=1):
    return Iv.frac(Fr(a, b))


FAILED = []


def gate(name, ok, detail):
    print(("PASS" if ok else "FAIL") + " | " + name + " | " + detail)
    if not ok:
        FAILED.append(name)


def eps_points(n):
    pts = [Fr(k, 4 * n) for k in range(0, n + 1)]          # [0, 1/4]
    pts += [Fr(24, 100), Fr(249, 1000), Fr(2499, 10000)]
    return sorted(set(p for p in pts if 0 <= p <= Fr(1, 4)))


def t_points(n):                                            # [1/4, 1/2]
    return [Fr(1, 4) + Fr(k, 4 * n) for k in range(0, n + 1)]


# ---------------------------------------------------------------- gates
def g_eq25():
    """note eq (25): H(5/18) < 1.086 and H(1/2) < 1.663 (rigorous points)."""
    h1 = H(fr(5, 18))
    gate("eq25 H(5/18) < 1.086 [pair-1 envelope]", h1.hi < 1.086,
         "H(5/18) in [%.12f, %.12f]  slack=%.6f" %
         (h1.lo, h1.hi, 1.086 - h1.hi))
    h2 = H(fr(1, 2))
    m2 = 1.663 - h2.hi
    gate("eq25 H(1/2)  < 1.663 [pair-2 envelope, TIGHT]", h2.hi < 1.663,
         "H(1/2) in [%.12f, %.12f]  slack=%.3e" % (h2.lo, h2.hi, m2))
    # (30) parameter box: C at upper corner 2.57801 must not break it.
    mubox = fr(257801, 100000).sqrt()
    h2b = H(fr(1, 2), mubox)
    gate("eq25 H(1/2) < 1.663 at (30)-box C=2.57801", h2b.hi < 1.663,
         "H_box(1/2) in [%.12f, %.12f]  slack=%.3e" %
         (h2b.lo, h2b.hi, 1.663 - h2b.hi))


def g_eq20(n=2000):
    """note eq (20): -a''(p) + (C d(m) - a''(m)) R > 5.14 on [1/4,1/2],
    R = cos(mu m)/cos(mu p), p = t_+, m = t_-.  GRID corroboration."""
    worst = None
    for t in t_points(n):
        ti = fr(t.numerator, t.denominator)
        p = (ONE + ti) / THREE
        m = (ONE - ti) / THREE
        R = (MU * m).cos() / (MU * p).cos()
        val = -app(p) + (CC * d(m) - app(m)) * R
        worst = val.lo if worst is None else min(worst, val.lo)
    gate("eq20 lower-curvature min > 5.14 [GRID n=%d]" % n, worst > 5.14,
         "min over [1/4,1/2] >= %.6f (only >0 is needed for F_n>=0)" % worst)


def g_eq24(n=2000):
    """note eq (24): D_m > 0 and D_p + D_m > 0 on [1/4,1/2] (upper
    curvature).  Stated floors 0.0224 / 0.0282 are correct but very loose;
    actual minima ~5.66 / ~3.45.  GRID corroboration."""
    wdm = wsum = None
    for t in t_points(n):
        ti = fr(t.numerator, t.denominator)
        p = (ONE + ti) / THREE
        m = (ONE - ti) / THREE
        cp = LAM + d(p)
        cm = LAM + d(m)
        chi = LAM / cm
        Ps = TWO * ap(p) * H(p) - app(p)
        Ms = TWO * ap(m) * H(m) - app(m)
        Dp = fr(8) * CC * cp - Ps
        Dm = (fr(9) * CC - CC * chi) * cm - Ms
        s = Dp + Dm
        wdm = Dm.lo if wdm is None else min(wdm, Dm.lo)
        wsum = s.lo if wsum is None else min(wsum, s.lo)
    gate("eq24 D_m > 0 [stated floor 0.0224] [GRID n=%d]" % n, wdm > 0.0,
         "min D_m >= %.4f  (stated 0.0224 is loose)" % wdm)
    gate("eq24 D_p+D_m > 0 [stated floor 0.0282] [GRID n=%d]" % n, wsum > 0.0,
         "min D_p+D_m >= %.4f  (stated 0.0282 is loose)" % wsum)


def g_eq27(n=2000):
    """note eq (27): lam + d(r) + rho(eps)(lam + d(r2)) > 7/6 + 0.095,
    rho = cos(mu r2)/cos(mu r), r = 1/4 + eps/9, r2 = 5/12 - eps/9.
    Binding endpoint eps=0 is rigorous; rest GRID.  TS3 itself is
    share >= 7/6."""
    wshare = wstated = None
    for e in eps_points(n):
        ei = fr(e.numerator, e.denominator)
        r = fr(1, 4) + ei / 9
        r2 = fr(5, 12) - ei / 9
        rho = (MU * r2).cos() / (MU * r).cos()
        lhs = LAM + d(r) + rho * (LAM + d(r2))
        share = lhs - fr(7, 6)
        stated = lhs - fr(7, 6) - fr(95, 1000)
        wshare = share.lo if wshare is None else min(wshare, share.lo)
        wstated = stated.lo if wstated is None else min(wstated, stated.lo)
    gate("eq27/TS3 child-share >= 7/6 [GRID n=%d]" % n, wshare > 0.0,
         "min (share - 7/6) >= %.6f  (substantial slack)" % wshare)
    gate("eq27 as written > 7/6 + 0.095 [binding eps=0, TIGHT]", wstated > 0.0,
         "min (LHS - 7/6 - 0.095) >= %.3e" % wstated)


def need_eps(e):                    # note/consumer: need(eps)
    return ((TWO * PI * e / 3).sin()
            / (TWO * PI * (fr(1, 6) + e / 3)).sin())


def g_eq31(n=2000):
    """note eq (31) / master (KEY):
    (e^{-1.663 g} - need)(7/6) e^{-1.086 g} - sin(4pi/9) sin(pi g) > 0.00574,
    g = 1/18 + 2 eps/9, eps in (0,1/4).  Contract loose caps
    (1.086, 1.663, 7/6).  GRID corroboration; cert value 0.005748519865.."""
    L1, L2, gamma = fr(543, 500), fr(1663, 1000), fr(7, 6)   # 1.086,1.663,7/6
    s49 = (fr(4, 9) * PI).sin()
    worst = None
    for e in eps_points(n):
        if e <= 0 or e >= Fr(1, 4):
            continue
        ei = fr(e.numerator, e.denominator)
        g = fr(1, 18) + TWO * ei / 9
        rho1 = (-(L1 * g)).exp()
        rho2 = (-(L2 * g)).exp()
        D1 = s49 * (PI * g).sin()
        Fv = (rho2 - need_eps(ei)) * gamma * rho1 - D1
        worst = Fv.lo if worst is None else min(worst, Fv.lo)
    gate("eq31 master (KEY) margin > 0.00574 [GRID n=%d]" % n, worst > 0.00574,
         "min F_loose >= %.6f  (cert loose_min_margin=0.005748519865)" % worst)


# --------------------------------------------------- recorded audit data
MANIFEST = [
    ("experimental/notes/thresholds/dense_shell_transfer_shape.md",
     "0cf65b76e6a788310ced83c9400aa0ef17b07747c8c509054d3149b7115a0509",
     "5fc9f180b69fe87f5d2b055355577511672aff8ef222beb42ab9d2e628354368"),
    ("experimental/scripts/verify_dense_shell_transfer_shape_arb.py",
     "1fd9d8bbacc79905842837c910e22c8f5cf4079c620fff23eb970150378e4b77",
     "9eac9446b74b50641ee9f7c661de0da656701b5902aba521ba2936f6b50e0c1c"),
    ("experimental/scripts/replay_dense_shell_transfer_shape.py",
     "47e818c40caa974b31bdfc6a2d963d8d9cf4e32d3caab8e62a375ecf46adccef",
     "32b45f42bc694d0daa9271e6223e43060bab8327d5437882616c35732e0a09fa"),
    ("experimental/scripts/README.md",
     "fb457506a1facbf3f8a45c840338079d4a0a67d8739a51c69f5380c2b68f3917",
     "f85c7cff4fc647e8be00c35c8d62588ecb753605235d35befb9dfa0757cfe54f"),
    ("experimental/data/certificates/dense-shell-transfer-shape/"
     "dense_shell_transfer_shape.json",
     "5a731c8839e613d36f767596429ea83867940eb6230eeb142a1a684038792512",
     "80c8dfc072977d4ea6359086f7dedf4eaa67a5a56b6064634299a933f02d4e09"),
    ("experimental/data/certificates/dense-shell-transfer-shape/"
     "consumer_contract.json",
     "3a3f1558e21418cec6bdab4e3c9ad370648bee9e8d7477b38aad1d861e40d702",
     "a0cfa97b006f316812ea4e8c9f7384e745a980691cdc91c14b35fe68a200dacb"),
    ("experimental/data/certificates/dense-shell-transfer-shape/README.md",
     "1408d25ae535aa1a6295b6af46b4f06c65cd083a1d70ff92d7264f3cf3e55efd",
     "042a8045e09c9f56de4431edcd1e5a9bb800a791c0cfad7d3a721fe36c8096d3"),
    ("experimental/notes/thresholds/dense_shell_class_charges.md",
     "6ebb6f6eaf23665cb3ae23d82c6e6e9ba4057869561fcaf0d8066b36ba9f2879",
     "e92c61aaffb3ab382789bee8b8ba00db809fb9b7cfc969dff7918a7904951c4f"),
    ("experimental/scripts/verify_dense_shell_class_charges.py",
     "5fbe9ef774420324b7e22cdf512ee394c0df584c5101bc948acc19103fe2cdeb",
     "561bcf5d536a853296c1ddf9def9067d0ec7616fd63e458c52b7d2f68420b7fc"),
    ("experimental/data/certificates/dense-shell-class-charges/"
     "dense_shell_class_charges.json",
     "613ca0f25ccd22eb9f86feedbb4b337d46a0571c332f239aecd4726f0cc27586",
     "719879447b4ff15d01703b713c493879f40adff63e894a1aa2ffa9bc59a612e3"),
]


def g_sha256sums():
    """S1: SHA256SUMS.txt is stale vs the committed blobs (measured
    2026-07-18).  All 10 entries mismatch; the packet's own replay hash gate
    would abort before python-flint is reached.  Recorded data, not a live
    check.  Reproduce (NOT executed here):
        git show pr-905:PATH | sha256sum"""
    n_mm = 0
    print("  --- SHA256SUMS.txt manifest vs committed blob (pr-905) ---")
    for path, mani, actual in MANIFEST:
        mm = mani != actual
        n_mm += mm
        print("  %-8s %s" % ("MISMATCH" if mm else "match", path))
        print("           manifest=%s.. blob=%s.." % (mani[:16], actual[:16]))
    print("  reproduce (not executed): git show pr-905:<PATH> | sha256sum")
    gate("S1 SHA256SUMS.txt stale for all 10 artifacts", n_mm == 10,
         "%d/10 manifest entries mismatch the committed blob" % n_mm)


def record_consumer():
    print("  RECORD (not re-executed): pr-905 "
          "verify_dense_shell_class_charges.py --deep -> RESULT: PASS (19/19) "
          "on 2026-07-18;")
    print("         P8 KEY (1.086,1.663,7/6): minF=0.0303 Fend=0.0303 "
          "minF_loose=0.0057.")


def main():
    print("== PR #905 dense-shell transfer-shape: independent audit "
          "verifier (symbolic half) ==")
    print("== python-flint absent: 448-bit Arb continuum cert NOT replayed "
          "==")
    g_eq25()
    g_eq20()
    g_eq24()
    g_eq27()
    g_eq31()
    g_sha256sums()
    record_consumer()
    print("== RESULT: %s (%d gate(s) failed) ==" %
          ("PASS" if not FAILED else "FAIL", len(FAILED)))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
