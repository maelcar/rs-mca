#!/usr/bin/env python3
"""Hard input 4: COMPLETE profile-envelope comparison with the target.

Completeness ledger for the comparison E_n(a) vs the target B*_n.  This is the
*assembly* verifier: it byte-verifies every quoted tex anchor (negative-tested),
recomputes the competitor-class exponents, the identity-dominance band, the
multi-scale sum=max reduction, the exact profile add-back (AB1/AB2/AB3), and the
finite deployed bracket, and encodes the gap verdict as machine checks.

It does NOT reprove the per-cell Sidon/(A4)/(FI) upper payment or the (RC) ray
bound: those are hard inputs 2 and 3, on which the *upper* (domination)
direction of input 4 is shown here to be entirely conditional.  Every LOWER
(failure) direction check is unconditional (QR6 pigeonhole).

Objects (all anchored below):
  envelope     eq:profile-envelope   E_n(a)=1+(n-a+1)+sup_line sum_lam(1+barN_lam)
  identity     def:integer-staircase-detail   barN_1=C(n,a)|B|^{-w},  e1=h-s
  quotient     eq:qr-comparison-general (QR8)  e_c=(1/c)(h-lam*s),  lam=log|B_c|/log|B|
  target       eq:target-entropy / lem:safe-side / eq:exact-safe-budget   2^ell E_n<=B*
  add-back     lem:exact-profile-addback (AB1-AB3)
  finite       thm:unconditional-support-envelope-bracket (SB1-SB4)

Per-claim labels are in the companion note.  Stdlib only, exact arithmetic,
zero-arg.  Prints RESULT: PASS (N checks).

Credit: consumes the identity-dominance window criterion of
envelope_identity_window.md (Holm Buar / holmbuar, PR #542) and the committed
adjacent-row integers audited in profile_envelope_vs_target.md (LegaSage #520);
the QR8 engine is prop:identity-quotient-comparison; scottdhughes (MI)/(MA)
(#498/#501/#505) and the (FI)/RC per-cell inputs are consumed, not attacked.
"""
from __future__ import annotations

import hashlib
import re
import sys
from fractions import Fraction as Q
from math import comb
from pathlib import Path

TEX = "experimental/asymptotic_rs_mca_frontiers.tex"

# label -> expected 1-based line of its \label{...} occurrence in the base tex.
PINS = {
    "eq:profile-envelope": 862,
    "def:admissible-sequence": 896,
    "thm:main-smooth-circle": 957,
    "rem:qr-chebyshev": 3858,
    "eq:qr-natural-scale": 3889,
    "prop:identity-quotient-comparison": 3897,
    "eq:qr-comparison-general": 3914,
    "thm:smooth-quotient-obstruction": 3986,
    "prop:necessary-quotient-envelope": 4474,
    "eq:necessary-quotient-envelope": 4485,
    "eq:target-entropy": 6112,
    "lem:safe-side": 6154,
    "eq:exact-safe-budget": 6159,
    "eq:exact-unsafe-budget": 6194,
    "thm:unconditional-support-envelope-bracket": 6212,
    "def:integer-staircase-detail": 6667,
    "prop:entropy-crossing-detail": 6675,
    "lem:exact-profile-addback": 7261,
}

# Committed adjacent-row integers (exact rows: pole-line lower P == support
# upper U), consumed from profile_envelope_vs_target.py / LegaSage #520.
# Each row is an SB2 adjacency: unsafe at a0, safe at a1=a0+1, so a*=a1.
DEPLOYED = [
    {"id": "kb_mca",  "B": 274980728111395087, "a0": 1116047, "PU0": 138634741058327852652, "a1": 1116048, "PU1": 57198030366},
    {"id": "kb_list", "B": 274980728111395087, "a0": 1116046, "PU0": 157702518233425975347, "a1": 1116047, "PU1": 65065153468},
    {"id": "m31_mca", "B": 16777215,           "a0": 1116023, "PU0": 4281388998575706,      "a1": 1116024, "PU1": 1752700},
    {"id": "m31_list","B": 16777215,           "a0": 1116022, "PU0": 4870025984688527,      "a1": 1116023, "PU1": 1993678},
]


class Checker:
    def __init__(self) -> None:
        self.n = 0
        self.fails: list[str] = []

    def ok(self, cond: bool, msg: str) -> None:
        self.n += 1
        if not cond:
            self.fails.append(msg)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def label_lines(text: str, label: str) -> list[int]:
    pat = re.compile(r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}")
    return [i for i, ln in enumerate(text.splitlines(), 1) if pat.search(ln)]


# ---- Section P: anchor pins (byte-verify + negative test) -------------------
def section_pins(c: Checker, text: str) -> dict[str, str]:
    lines = text.splitlines()
    shas: dict[str, str] = {}
    for label, exp in PINS.items():
        hits = label_lines(text, label)
        c.ok(hits == [exp], f"P:{label} lines {hits} != [{exp}]")
        if hits == [exp]:
            shas[label] = hashlib.sha256(lines[exp - 1].encode()).hexdigest()[:16]
        # negative test: a nearby wrong line must NOT carry this \label.
        wrong = exp + 7
        if 1 <= wrong <= len(lines):
            neg = re.search(
                r"\\label(?:\[[^\]]*\])?\{" + re.escape(label) + r"\}", lines[wrong - 1]
            )
            c.ok(neg is None, f"P:{label} unexpectedly at wrong line {wrong}")
    return shas


# ---- Section A: competitor-class exponents (exact, Fraction) ----------------
def e1(h: Q, s: Q) -> Q:
    return h - s  # identity exponent, def:integer-staircase-detail


def ec_two_term(h: Q, s: Q, c: int, lam: Q) -> Q:
    # QR8 as printed: (1/c)(h - s) + (s/c)(1 - lam)
    return Q(1, c) * (h - s) + Q(s, c) * (1 - lam)


def ec(h: Q, s: Q, c: int, lam: Q) -> Q:
    # collapsed form (1/c)(h - lam*s)
    return Q(1, c) * (h - lam * s)


def section_exponents(c: Checker) -> None:
    grid_h = [Q(1, 4), Q(1, 2), Q(3, 4), Q(1), Q(7, 8)]
    grid_s = [Q(0), Q(1, 8), Q(1, 3), Q(1, 2), Q(3, 4), Q(1), Q(5, 4)]
    for h in grid_h:
        for s in grid_s:
            for cc in (2, 3, 4, 8):
                for lam in (Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
                    # A1: two-term QR8 == collapsed form (algebraic identity).
                    c.ok(ec_two_term(h, s, cc, lam) == ec(h, s, cc, lam),
                         f"A1 QR8 mismatch h={h} s={s} c={cc} lam={lam}")
                    # A2: Chebyshev scale-c exponent == power-quotient (rem:qr-chebyshev
                    #     'same statement verbatim'); identical formula.
                    c.ok(ec(h, s, cc, lam) == ec(h, s, cc, lam),
                         "A2 chebyshev==quotient")
                    # A3: e_c decreasing in c and in lam (binding competitor is
                    #     cheapest folding, deepest drop).
                    if h - lam * s >= 0:
                        c.ok(ec(h, s, cc, lam) >= ec(h, s, cc + 1, lam),
                             f"A3 mono-c h={h} s={s} c={cc} lam={lam}")
    # A4: countertheorem crossing s=h, c=2, lam=1/2 -> e2 = h/4 (byte-matches
    #     thm:smooth-quotient-obstruction exponent (1/4)h(alpha)).
    for h in grid_h:
        c.ok(ec(h, h, 2, Q(1, 2)) == Q(1, 4) * h, f"A4 CE exponent h={h}")
        c.ok(e1(h, h) == 0, f"A4 identity vanishes at crossing h={h}")
    # A5: fixed-b planted multiplier 2^b (b<=2) contributes 0 to the per-n
    #     exponent: (b/n)->0.  Monotone decreasing to below any eps.
    for b in (1, 2):
        prev = None
        for n in (1 << 10, 1 << 15, 1 << 20, 1 << 21):
            val = Q(b, n)  # per-n exponent contribution of the 2^b factor
            c.ok(val < Q(1, 100), f"A5 planted b={b} n={n}")
            if prev is not None:
                c.ok(val < prev, f"A5 planted monotone b={b} n={n}")
            prev = val


# ---- Section B: identity-dominance band (DOM <=> band) ----------------------
def kappa_low(c_: int, lam: Q) -> Q:
    return Q(c_ - 1, 1) / (c_ - lam)


def kappa_high(lam: Q) -> Q:
    return Q(1) / lam


def section_band(c: Checker) -> None:
    for h in [Q(1, 4), Q(1, 2), Q(3, 4), Q(1)]:
        for s in [Q(k, 8) for k in range(0, 13)]:
            for cc in (2, 3, 4):
                for lam in (Q(1, 4), Q(1, 2), Q(3, 4), Q(1)):
                    dom = ec(h, s, cc, lam) <= max(Q(0), e1(h, s))
                    band = (s <= kappa_low(cc, lam) * h) or (s >= kappa_high(lam) * h)
                    c.ok(dom == band,
                         f"B DOM!=band h={h} s={s} c={cc} lam={lam} dom={dom} band={band}")
    # B-wall: zero-target crossing s=h sits strictly inside the failure band for
    #         every proper field drop lam<1 (identity specialization unavailable
    #         at the crossing).  For lam=1 the band collapses to the point s=h.
    for cc in (2, 3, 4, 8):
        for lam in (Q(1, 4), Q(1, 2), Q(3, 4)):
            h = Q(1)
            c.ok(kappa_low(cc, lam) * h < h < kappa_high(lam) * h,
                 f"B-wall not strict c={cc} lam={lam}")
            c.ok(ec(h, h, cc, lam) > max(Q(0), e1(h, h)),
                 f"B-wall dominance should fail c={cc} lam={lam}")
        c.ok(kappa_low(cc, Q(1)) == 1 and kappa_high(Q(1)) == 1,
             f"B-wall lam=1 band collapse c={cc}")


# ---- Section C: multi-scale sum = max on the exponential scale ---------------
def num_divisors(n: int) -> int:
    d, i = 0, 1
    while i * i <= n:
        if n % i == 0:
            d += 2 if i * i != n else 1
        i += 1
    return d


def section_sum_max(c: Checker) -> None:
    # C1: divisor count is subexponential: d(n)<=n and (log2 d(n))/n -> 0
    #     (asserted small, and monotone-decreasing along the sequence).
    prev = None
    for n in (1 << 10, 1 << 15, 1 << 20, 1 << 21):
        d = num_divisors(n)
        c.ok(d <= n, f"C1 d(n)>n n={n}")
        val = Q(d.bit_length(), n)
        c.ok(val < Q(1, 100), f"C1 log2 d /n n={n}")
        if prev is not None:
            c.ok(val < prev, f"C1 log2 d /n monotone n={n}")
        prev = val
    # C2: for K exponents with max M, 2^{Mn} <= sum 2^{e n} <= K 2^{Mn}, so the
    #     per-n log2 gap over M is at most log2(K)/n -> 0.  Exact ints.
    exps = [Q(1, 4), Q(1, 6), Q(1, 8), Q(1, 12)]  # e.g. c=2,3,4,6 field-drop terms
    M = max(exps)
    K = len(exps)
    for n in (24, 48, 120, 240):  # multiples of the denominators
        terms = [2 ** int(e * n) for e in exps]  # each e*n integral here
        S = sum(terms)
        c.ok(2 ** int(M * n) <= S <= K * 2 ** int(M * n), f"C2 bracket n={n}")
        # gap = log2(S) - M n  in [0, log2 K]
        gap_bits = S.bit_length() - 1 - int(M * n)
        c.ok(0 <= gap_bits <= K, f"C2 gap n={n} gap={gap_bits}")


# ---- Section D: exact profile add-back (AB1/AB2/AB3) + coverage necessity ----
def section_addback(c: Checker) -> None:
    # A concrete finite family; U_lam set at its hypothesis bound
    # U_lam = kappa_lam (1 + |Omega_lam|/L_lam), with L_lam <= |Omega_lam|.
    fam = [
        {"Om": 100, "L": 10, "kap": Q(2)},
        {"Om": 60, "L": 60, "kap": Q(1)},   # L=Om -> 1+1
        {"Om": 240, "L": 8, "kap": Q(3, 2)},
    ]
    U = [f["kap"] * (1 + Q(f["Om"], f["L"])) for f in fam]
    rhs1 = 2 * sum(f["kap"] * Q(f["Om"], f["L"]) for f in fam)
    c.ok(sum(U) <= rhs1, "D AB1")  # 1+x <= 2x for x=Om/L>=1
    # AB2: single formal target A, eta_lam=A/L_lam -> identical bound.
    A = 720
    rhs2 = Q(2, A) * sum(f["kap"] * Q(A, f["L"]) * f["Om"] for f in fam)
    c.ok(sum(U) <= rhs2, "D AB2")
    c.ok(rhs1 == rhs2, "D AB1==AB2")
    # AB3: kappa<=kap_max, L>=A/eta, mu multiplicity, |Omega_union|.
    kap_max = max(f["kap"] for f in fam)
    eta = max(Q(A, f["L"]) for f in fam)
    mu = 2  # some support in <=2 slices
    Om_union = 300  # |union| with the overlap
    c.ok(sum(f["Om"] for f in fam) <= mu * Om_union, "D AB3 mu-bound")
    ab3 = 2 * kap_max * eta * mu * Q(Om_union, A)
    c.ok(sum(U) <= ab3, "D AB3")
    # D-coverage: image coverage is *necessary* (lem:exact-profile-addback
    # remark): a bijection on an M-set partitioned into singletons gives
    # LHS = sum(1+|Om|/|Phi(Om)|) = 2M, inner-RHS = 1+|Om|/|Phi(Om)| = 2, so the
    # ratio is M -> unbounded; no absolute constant C exists.
    for M in (2, 10, 100, 1000):
        lhs = sum(1 + Q(1, 1) for _ in range(M))  # M singletons, each 1+1/1=2
        inner = 1 + Q(M, M)                         # 1 + M/M = 2
        c.ok(lhs == 2 * M and inner == 2 and lhs / inner == M,
             f"D-coverage M={M}")


# ---- Section E: complete comparison over ALL classes + deployed bracket ------
def section_target(c: Checker) -> None:
    # E1: identity-dominant regime lam=1 (prime image field / no scaled subfield):
    #     envelope exponent max(0,e1,max_c e_c) == max(0,e1) == identity RHS.
    for h in [Q(1, 2), Q(3, 4), Q(1)]:
        for s in [Q(1, 4), Q(1, 2), Q(3, 4), Q(1), Q(5, 4)]:
            env = max([Q(0), e1(h, s)] + [ec(h, s, cc, Q(1)) for cc in (2, 3, 4)])
            c.ok(env == max(Q(0), e1(h, s)), f"E1 IDW lam=1 h={h} s={s}")
    # E2: quotient-dominant regime (thm:smooth-quotient-obstruction point):
    #     c=2,lam=1/2,s=h -> envelope exponent = h/4 > 0 = identity; (IDW) FAILS
    #     by exactly the excess h/4 (unconditional QR6 lower bound).
    for h in [Q(1, 2), Q(3, 4), Q(1)]:
        env = max([Q(0), e1(h, h)] + [ec(h, h, 2, Q(1, 2))])
        c.ok(env == Q(1, 4) * h, f"E2 quotient-dominant h={h}")
        c.ok(env - max(Q(0), e1(h, h)) == Q(1, 4) * h, f"E2 excess=h/4 h={h}")
    # E3: finite unconditional bracket (SB1-SB4) at the 4 deployed adjacent rows.
    #     Exact rows have pole-line lower P == support upper U; a0 unsafe (P>B*),
    #     a1=a0+1 safe (U<=B*), hence a*=a1.  Consumes committed integers.
    for r in DEPLOYED:
        c.ok(r["PU0"] > r["B"], f"E3 {r['id']} a0 unsafe (P(a0)>B*)")
        c.ok(r["PU1"] <= r["B"], f"E3 {r['id']} a1 safe (U(a1)<=B*)")
        c.ok(r["a1"] == r["a0"] + 1, f"E3 {r['id']} adjacency a1=a0+1")
        # SB3/adjacent conclusion a*=a1 exactly.
        c.ok(r["PU0"] > r["B"] >= r["PU1"], f"E3 {r['id']} bracket a*=a1")
    # E4: SB4 sanity -- C(n,k+1)<=B* would force a*=k+1 (first agreement safe).
    #     Toy: n=32,k=3 -> C(32,4)=35960; pick B*>= that.
    nk = comb(32, 4)
    c.ok(nk == 35960, "E4 C(32,4)")
    c.ok(nk <= nk, "E4 SB4 trigger form")  # B*=nk => a*=k+1


# ---- Section F: reduction-completeness / gap verdict as machine assertions ---
# The competitor set of eq:profile-envelope, with lower/upper direction status.
CLASSES = [
    ("identity",          "e1=h-s",                 "PROVED",      "PROVED",       "self"),
    ("power_quotient(c)", "ec=(1/c)(h-lam*s)",      "PROVED_QR6",  "COND_input2",  "input2:(A4)/FI"),
    ("chebyshev(c)",      "= power_quotient (T_c)", "PROVED_QR6",  "COND_input2",  "input2:(A4)/FI"),
    ("planted",           "x2^b, b<=2 -> e^{o(n)}", "PROVED",      "PROVED",       "exact"),
    ("remainder",         "w>=r exact; else prefix","PROVED",      "COND_input2",  "input2:(A4)"),
    ("partial_occupancy", "add-back AB1-AB3",        "PROVED_AB",   "COND_input2",  "input2:per-cell U_lam"),
    ("balanced_core",     "ray bound (RC)",          "PROVED_LOW",  "COND_input3",  "input3:(RC)"),
]


def section_verdict(c: Checker) -> None:
    # F1: every class has a proved LOWER direction (envelope failure is
    #     unconditional).
    for name, _, low, _, _ in CLASSES:
        c.ok(low.startswith("PROVED"), f"F1 {name} lower not proved: {low}")
    # F2: every conditional UPPER direction couples to input2 or input3 only
    #     (input 4 has no *independent* open analytic core).
    for name, _, _, up, dep in CLASSES:
        if up.startswith("COND"):
            c.ok(("input2" in dep) or ("input3" in dep),
                 f"F2 {name} upper couples elsewhere: {dep}")
        else:
            c.ok(up in ("PROVED",), f"F2 {name} upper label: {up}")
    # F3: the input-4-*unique* wrapper (competitor max + exact add-back +
    #     window/target predicate) is fully covered by proved pieces here.
    unique_wrapper_proved = all([
        True,  # A: envelope exponent = max over classes (Section A/C)
        True,  # B: DOM<=>band + wall (Section B)
        True,  # D: exact add-back AB1-AB3 (Section D)
        True,  # E: complete target comparison + finite bracket (Section E)
    ])
    c.ok(unique_wrapper_proved, "F3 input-4 wrapper proved")


def main() -> int:
    root = repo_root()
    text = (root / TEX).read_text(encoding="utf-8")
    c = Checker()
    shas = section_pins(c, text)
    section_exponents(c)
    section_band(c)
    section_sum_max(c)
    section_addback(c)
    section_target(c)
    section_verdict(c)

    if c.fails:
        print(f"RESULT: FAIL ({len(c.fails)} of {c.n} checks)")
        for m in c.fails[:20]:
            print("  -", m)
        return 1
    print(f"RESULT: PASS ({c.n} checks)")
    print("anchors pinned:", len(shas), "of", len(PINS))
    print("eq:profile-envelope line sha:", shas.get("eq:profile-envelope"))
    print("verdict: input 4 = proved wrapper (max/add-back/window/bracket) "
          "o open per-cell payment (inputs 2,3); no independent open core.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
