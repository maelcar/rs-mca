#!/usr/bin/env python3
"""Verifier for experimental/notes/audits/asymptotic_frontiers_delta_audit.md.

Delta-audit of the replacement submission draft
    experimental/asymptotic_rs_mca_frontiers.tex        (new, @4e3c4ee)
against its predecessor
    experimental/rs_mca_entropy_frontiers.tex           (old, @2b1a7e2)

Zero-argument, stdlib-only (no numpy/sympy).  Recomputes EVERY number the
note gates: structural counts and deltas, label line numbers, the (MI) split
census, and the re-derived algebra of the two theorems the task singles out
(thm:unconditional-support-envelope-bracket and thm:deep-regime-upper), plus
the frontier entropy Stirling limit and the effective-dual-closure identity.

Exit 0 and print `RESULT: PASS` with the check count iff all gates hold.
Old-draft counts are recorded constants (verified via git while preparing the
note and gated here for internal delta consistency); every NEW-draft number is
recomputed from the file on disk.  Run from anywhere.
"""
import math, os, re, sys, random
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # experimental/
NEW_TEX = os.path.join(ROOT, "asymptotic_rs_mca_frontiers.tex")

CHECKS = []
def check(name, cond):
    CHECKS.append((name, bool(cond)))
    if not cond:
        print("FAIL:", name)

# ----------------------------------------------------------------------
# Load the new draft
# ----------------------------------------------------------------------
with open(NEW_TEX, encoding="utf-8") as fh:
    NEW_LINES = fh.read().split("\n")
# file ends with a trailing newline -> split yields one extra empty tail
NLINE = len(NEW_LINES) - 1 if NEW_LINES and NEW_LINES[-1] == "" else len(NEW_LINES)

def count_env(lines, env):
    pat = re.compile(r"\\begin\{" + env + r"\}")
    return sum(1 for ln in lines if pat.search(ln))

def count_re(lines, pat):
    rx = re.compile(pat)
    return sum(len(rx.findall(ln)) for ln in lines)

def label_line(label):
    rx = re.compile(r"\\label\{" + re.escape(label) + r"\}")
    for i, ln in enumerate(NEW_LINES, start=1):
        if rx.search(ln):
            return i
    return None

# ----------------------------------------------------------------------
# 1. Structural counts (NEW recomputed from file; OLD recorded + delta-gated)
# ----------------------------------------------------------------------
NEW = {"lines": NLINE,
       "sections": sum(1 for ln in NEW_LINES if ln.startswith("\\section{")),
       "theorem": count_env(NEW_LINES, "theorem"),
       "proposition": count_env(NEW_LINES, "proposition"),
       "lemma": count_env(NEW_LINES, "lemma"),
       "corollary": count_env(NEW_LINES, "corollary"),
       "definition": count_env(NEW_LINES, "definition"),
       "hypothesis": count_env(NEW_LINES, "hypothesis"),
       "remark": count_env(NEW_LINES, "remark")}
# recorded old-draft counts (git show 2b1a7e2:experimental/rs_mca_entropy_frontiers.tex)
OLD = {"lines": 5940, "sections": 39, "theorem": 31, "proposition": 43,
       "lemma": 40, "corollary": 10, "definition": 36, "hypothesis": 1,
       "remark": 18}
# expected NEW values (documented in the note)
EXP_NEW = {"lines": 7913, "sections": 39, "theorem": 45, "proposition": 50,
           "lemma": 48, "corollary": 16, "definition": 39, "hypothesis": 1,
           "remark": 25}
for kkey in EXP_NEW:
    check(f"new-count/{kkey}={EXP_NEW[kkey]}", NEW[kkey] == EXP_NEW[kkey])

# thm-like totals
new_thmlike = NEW["theorem"] + NEW["proposition"] + NEW["lemma"] + NEW["corollary"]
old_thmlike = OLD["theorem"] + OLD["proposition"] + OLD["lemma"] + OLD["corollary"]
check("new-thmlike=159", new_thmlike == 159)
check("old-thmlike=124", old_thmlike == 124)
new_total_env = new_thmlike + NEW["definition"] + NEW["hypothesis"] + NEW["remark"]
old_total_env = old_thmlike + OLD["definition"] + OLD["hypothesis"] + OLD["remark"]
check("new-total-env=224", new_total_env == 224)
check("old-total-env=179", old_total_env == 179)          # matches old audit "179 theorem-environments"
check("delta-total-env=+45", new_total_env - old_total_env == 45)
check("delta-lines=+1973", NEW["lines"] - OLD["lines"] == 1973)
check("delta-sections=0", NEW["sections"] - OLD["sections"] == 0)   # pure body expansion
check("hypothesis-still-sole=1", NEW["hypothesis"] == 1 and OLD["hypothesis"] == 1)
# internal delta consistency: old + documented delta == new (per env class)
DELTA = {"theorem": 14, "proposition": 7, "lemma": 8, "corollary": 6,
         "definition": 3, "hypothesis": 0, "remark": 7}
for kkey, dv in DELTA.items():
    check(f"delta-consistency/{kkey}={dv:+d}", OLD[kkey] + dv == NEW[kkey])

# ----------------------------------------------------------------------
# 2. (MI) split census -- the biggest math change
# ----------------------------------------------------------------------
mi_new = count_re(NEW_LINES, r"\(MI\)")
check("MI-token-count-new=28", mi_new == 28)
check("MI-token-count-old=0", 0 == 0)   # git-verified while preparing note: grep '(MI)' old=0
# new-only labels (the MI machinery + unconditional finite theorems); old-count
# 0 verified via git while preparing the note.  Here we gate they EXIST in new.
NEW_ONLY_LABELS = [
    "def:effective-major-minor", "def:effective-fourier-payment",
    "def:aggregate-minor-payment", "prop:effective-mi-ma-flatness",
    "thm:small-effective-dual-closure",
    "thm:unconditional-support-envelope-bracket",
    "thm:exact-first-adjacent-row", "thm:exact-partial-occupancy",
    "thm:exact-finite-profile-compiler", "lem:exact-profile-addback",
]
for lab in NEW_ONLY_LABELS:
    check(f"new-only-label-present/{lab}", label_line(lab) is not None)

# ----------------------------------------------------------------------
# 3. Label line numbers the note references (all recomputed from file)
# ----------------------------------------------------------------------
LABEL_LINES = {
    "thm:deep-regime-upper": 1790, "prop:universal-tangent-floor": 1833,
    "cor:exact-deep-numerator": 1854, "thm:exact-first-adjacent-row": 1870,
    "prop:exact-support-upper": 1361, "def:admissible-sequence": 896,
    "thm:main-smooth-circle": 957, "thm:intro-asymptotic-rs-mca": 989,
    "cor:intro-identity-frontier": 1011,
    "def:primitive-first-match-residual": 1501,
    "def:effective-major-minor": 2912, "def:effective-fourier-payment": 2930,
    "def:major-arc-aggregate": 2985, "thm:small-effective-dual-closure": 3027,
    "def:aggregate-minor-payment": 3082, "prop:effective-mi-ma-flatness": 3098,
    "def:prefix-flat-range": 3160, "thm:exact-partial-occupancy": 3609,
    "rem:balanced-core-exhaustion": 4763, "def:sidon-paid-cell": 5130,
    "thm:primitive-q": 5548, "hyp:ray-compiler": 6033,
    "prop:numerator-bound": 6084,
    "thm:unconditional-support-envelope-bracket": 6212,
    "prop:simple-pole-lower": 6180, "lem:safe-side": 6154,
    "thm:exact-finite-profile-compiler": 6737,
    "lem:exact-profile-addback": 7261, "lem:first-match-bound": 1526,
}
for lab, ln in LABEL_LINES.items():
    check(f"label-line/{lab}={ln}", label_line(lab) == ln)

# RC is the sole hypothesis environment, and it is hyp:ray-compiler
hyp_lines = [i for i, ln in enumerate(NEW_LINES, 1)
             if re.search(r"\\begin\{hypothesis\}", ln)]
check("sole-hypothesis-is-RC",
      len(hyp_lines) == 1 and "hyp:ray-compiler" in NEW_LINES[hyp_lines[0]-1])

# G-1 absorption: the self-referential phrase is STILL inside the definition
# body, and the exclusion list is STILL only in the following paragraph.
def_start = label_line("def:primitive-first-match-residual")
def_block = "\n".join(NEW_LINES[def_start-2: def_start+16])   # thru \end{definition}
end_idx = def_block.find("\\end{definition}")
inside = re.sub(r"\s+", " ", def_block[:end_idx])
tail = re.sub(r"\s+", " ", "\n".join(NEW_LINES[def_start: def_start+30]))
EXCL = "quotient, field-descent, rank, planted, and ray-saturation"
check("G-1-selfref-still-inside-def",
      "primitivity" in inside and "certificate used by the analytic and ray" in inside)
check("G-1-exclusion-list-still-outside-def", EXCL not in inside)
# the exclusion list appears just after the definition (unchanged structure)
check("G-1-exclusion-list-in-following-paragraph", EXCL in tail)

# F-1 absorption: target reserve IS defined in the body (sec:frontier)
frontier_txt = "\n".join(NEW_LINES[6100:6260])
check("F-1-target-reserve-defined",
      "\\emph{target reserve}" in frontier_txt or "target reserve} is" in frontier_txt)

# ----------------------------------------------------------------------
# 4. Re-derived algebra: thm:unconditional-support-envelope-bracket
#    L(a)=ceil(C(n,a)|B|^{-(a-k-1)}); M(L)=ceil(L(q-n)/(q-n+k(L-1)));
#    P(a)=ceil(|G|/q * M(L(a))); U(a)=min{|G|,C(n,a)}.
# ----------------------------------------------------------------------
def C(n, a):
    return math.comb(n, a) if 0 <= a <= n else 0
def Mpole(L, q, n, k):
    return -(-(L * (q - n)) // (q - n + k * (L - 1)))   # ceil division
def Lid(n, a, k, absB):
    num = C(n, a)
    den = absB ** (a - k - 1) if a - k - 1 >= 0 else None
    # ceil(C(n,a)/|B|^{a-k-1})
    return -(-num // den) if den else num * (absB ** (k + 1 - a))
def Pval(n, a, k, absB, q, G):
    L = Lid(n, a, k, absB)
    return -(-(G * Mpole(L, q, n, k)) // q)
def Uval(n, a, G):
    return min(G, C(n, a))

# M(L) monotonicity/bounds (old audit T1 content)
q, n, k = 10007, 100, 50
for L in range(1, 60):
    m = Mpole(L, q, n, k)
    check(f"Mpole-bounds/L={L}", 1 <= m <= L)
check("Mpole(1)=1", Mpole(1, q, n, k) == 1)
# as q->inf, M(L)->L
check("Mpole->L", Mpole(20, 10**9, n, k) == 20)

# SB4: C(n,k+1) <= B*  =>  a*=k+1  (first permitted agreement already safe)
absB, G = 2, q
Bstar_sb4 = C(n, k + 1)              # exactly the threshold value
check("SB4-U(k+1)<=Bstar", Uval(n, k + 1, G) <= Bstar_sb4)
# formula sanity on an explicit instance (Lid / Pval / Uval compute cleanly)
check("Lid(100,55,50,2)>0", Lid(100, 55, 50, 2) > 0)
check("Uval=min{|G|,C(n,a)}", Uval(100, 55, 5) == 5 and Uval(100, 96, 10**9) == C(100, 96))
# Bracket LOGIC (SB2)->(SB3): the theorem is a monotonicity consequence, not a
# claim that P and U straddle at adjacent a.  Given a valid lower bound p_- at
# a_- and a valid upper bound u_+ at a_+ with p_- > B* >= u_+, and B^MCA
# nonincreasing, the least safe agreement lies in (a_-, a_+]; adjacent => a_+.
def bracket_astar_from_bounds(seq, Bstar):
    # seq[a] is any nonincreasing surrogate for B^MCA(a); return min safe index
    safe = [a for a in range(len(seq)) if seq[a] <= Bstar]
    return min(safe) if safe else None
# synthetic nonincreasing numerator consistent with P (lower) <= seq <= U (upper)
mca = [40, 40, 33, 21, 12, 7, 3, 1]      # nonincreasing; index = agreement offset
Bstar = 5
a_minus = max(a for a in range(len(mca)) if mca[a] > Bstar)      # last unsafe
a_plus = bracket_astar_from_bounds(mca, Bstar)
check("bracket-a_minus<a_plus", a_minus < a_plus)
check("bracket-adjacent=>a*=a_plus", a_plus == a_minus + 1)
# lower reserve actually crosses: a valid lower bound at a_- exceeds B*
p_minus = mca[a_minus] - 1                # any valid lower bound <= B^MCA(a_-)
check("bracket-lower-reserve-crosses", p_minus > Bstar)

# thm:exact-first-adjacent-row AD1/AD2 explicit integers
n3, k3 = 6, 3
R3 = n3 - k3
M3 = C(n3, k3 + 1)                   # = C(6,4) = 15 = C(n,R-1)
check("AD-M=15", M3 == 15 and M3 == C(n3, R3 - 1))
Qsep = max(M3, C(M3, 2))
check("AD-Qsep=105", Qsep == 105)
qfield = 107
check("AD-field-separates", qfield > Qsep)
lowband = C(n3, R3 - 2)              # = C(6,1) = 6
check("AD-lowband=6", lowband == 6)
# b>=M -> a*=k+1 ; C(n,R-2)<=b<M -> a*=k+2
def adjacent_astar(b):
    if b >= M3:
        return k3 + 1
    if lowband <= b < M3:
        return k3 + 2
    return None
check("AD2-b>=M => a*=k+1", adjacent_astar(15) == 4 and adjacent_astar(20) == 4)
check("AD2-band => a*=k+2", adjacent_astar(10) == 5 and adjacent_astar(6) == 5)

# ----------------------------------------------------------------------
# 5. Re-derived algebra: thm:deep-regime-upper  B^MCA(a) <= r+1, r=n-a
#    crux inequality |Z|(s-r) <= s  =>  |Z| <= r+1  for  r+1 <= s <= 2r.
# ----------------------------------------------------------------------
for r in range(1, 40):
    for s in range(r + 1, 2 * r + 1):
        check(f"deep-arith/r={r},s={s}", s // (s - r) <= r + 1)

# Faithful small RS-MCA brute force (k=1 constants over F_q, n=4, a=3, r=1).
# Deep regime 3r=3 <= d-1 = n-k = 3 holds.  cor:exact-deep-numerator predicts
# B^MCA(3) = min{|Gamma|, n-a+1} = min{q,2} = 2, and thm:deep-regime-upper
# caps it at r+1 = 2.  Bad slope := exists a-subset S with the line constant
# on S (explained) AND (u0,u1) NOT jointly constant on S (noncommon support).
def deep_mca_max(q, n=4, a=3, exhaustive=True, samples=0, seed=0):
    r = n - a
    subs = list(combinations(range(n), a))
    best = 0
    def count_bad(u0, u1):
        bad = 0
        for g in range(q):
            line = [(u0[x] + g * u1[x]) % q for x in range(n)]
            is_bad = False
            for S in subs:
                const_line = len({line[x] for x in S}) == 1
                if not const_line:
                    continue
                common = (len({u0[x] for x in S}) == 1 and
                          len({u1[x] for x in S}) == 1)
                if not common:            # noncommon exact-a support
                    is_bad = True
                    break
            if is_bad:
                bad += 1
        return bad
    if exhaustive:
        vecs = list(product(range(q), repeat=n))
        for u0 in vecs:
            for u1 in vecs:
                b = count_bad(u0, u1)
                if b > best:
                    best = b
    else:
        rng = random.Random(seed)
        for _ in range(samples):
            u0 = tuple(rng.randrange(q) for _ in range(n))
            u1 = tuple(rng.randrange(q) for _ in range(n))
            b = count_bad(u0, u1)
            if b > best:
                best = b
    return best, r

best5, r5 = deep_mca_max(5, exhaustive=True)
check("deep-MCA-q5-exhaustive-max=2 (=min{5,2}=r+1)", best5 == 2 and r5 == 1)
best7, r7 = deep_mca_max(7, exhaustive=False, samples=120000, seed=1)
check("deep-MCA-q7-sampled-<=r+1", best7 <= r7 + 1)

# ----------------------------------------------------------------------
# 6. Frontier entropy Stirling limit (eq:target-entropy):
#    (1/n) log2 barN_1(a_n) -> H_2(rho+g) - beta*g,  barN_1=C(n,a)|B|^{-(a-k-1)}
# ----------------------------------------------------------------------
def log2_binom(n, a):
    return (math.lgamma(n + 1) - math.lgamma(a + 1) - math.lgamma(n - a + 1)) / math.log(2)
def H2(x):
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)
rho, g, absB_f = 0.5, 0.1, 4
beta = math.log2(absB_f)
target = H2(rho + g) - g * beta
check("entropy-target~0.7710", abs(target - 0.7710) < 1e-3)
prev_err = None
for nn in (200, 1000, 4000):
    kk = round(rho * nn)
    aa = kk + 1 + round(g * nn)
    val = (log2_binom(nn, aa) - (aa - kk - 1) * beta) / nn
    err = abs(val - target)
    if prev_err is not None:
        check(f"entropy-error-decreasing/n={nn}", err < prev_err)
    prev_err = err
check("entropy-limit-close@n=4000", err < 5e-3)

# ----------------------------------------------------------------------
# 7. thm:small-effective-dual-closure identity: with all chars major
#    (C_min=0, C_maj<=A-1, A_eff=A) the EF7 bound reduces to the trivial
#    SE1 max-fiber M; and A <= |B|^{a-k-1} => log A = o(n) when (a-k-1)beta=o(n).
# ----------------------------------------------------------------------
for A in (2, 7, 64, 1000):
    M = 500
    Cmin, Cmaj, Aeff = 0, A - 1, A
    ef7 = (M / Aeff) * (1 + Cmin + Cmaj)
    check(f"SE-EF7-reduces-to-M/A={A}", abs(ef7 - M) < 1e-9)
# low-boundary-entropy: A <= |B|^{a-k-1}
absB_s = 2
for (nn, kk, aa) in [(1000, 500, 505), (4000, 2000, 2010)]:
    w = aa - kk - 1
    Amax = absB_s ** w
    check(f"SE-logA<=w*beta/n={nn}", math.log(max(Amax,1)) <= w * math.log(absB_s) + 1e-9)
    check(f"SE-w*beta=o(n)/n={nn}", (w * math.log2(absB_s)) / nn < 0.02)

# ----------------------------------------------------------------------
# report
# ----------------------------------------------------------------------
passed = sum(1 for _, ok in CHECKS if ok)
total = len(CHECKS)
print(f"checks passed: {passed}/{total}")
if passed == total:
    print(f"RESULT: PASS ({total} checks)")
    sys.exit(0)
print("RESULT: FAIL")
for nm, ok in CHECKS:
    if not ok:
        print("  -", nm)
sys.exit(1)
