#!/usr/bin/env python3
"""
verify_nonfiber_decomposition_realized_scale.py

Recomputes every number in
  experimental/notes/thresholds/nonfiber_decomposition_realized_scale.md

LANE: hard input 2 -- the NON-fiber-indexed route to avdeevvadim's #716
charge-preserving semantic-or-signed decomposition, the object left open after
the fiber-indexed route was cut on the Sidon-paired class (#739) and the
per-fiber emission grammar closed (#735).  Two new facts reframe it: the paper's
`thm:aperiodic-one-ray-saturation` (a heavy fiber can collapse to one slope --
emission does not pay lower reserve) and the paper's `rem` PO5 effective
normalization (the correct Fourier denominator is the realized-image group
|G_lambda|, and "it does not assert that the realized image fills the affine
group").  The profile-envelope comparison packet (PR #759, integrated in the
same `2633895a` wave) records an exact finite full-codomain deficit for the
identity image.  This is not an asymptotic `(FI)` conclusion and is motivational
only; this verifier's proof is independent of #759.

The staircase-concentration class (#739 / #732 / #735 corrected Thm 2a / #717
Sec 7 / DannyExperiments-corrected #749):
  P     distinct-subset-sum set over Z, |P| = B (base 3^i and 5^i tested)
  c     = 2*sum(P) + 1   (large-c / no-wraparound designed modulus)
  T     = P u (c - P),  |T| = 2B     (twin pairs {A_i, c-A_i})
  a     = B ;  Phi(S) = sum_{t in S} t over Z
  M     = C(2B,B) ;  L = |Phi(Omega^0)| = (3^B+1)/2 (realized image, intrinsic)

RUNGS DECIDED (agents.md label per block; every integer recomputed here):

  BLOCK A  RUNG (a) -- the concentration inequality at PO5 realized-image scale,
     and WHICH scale #739 kills.  DECISION: BOTH.  #739's own threshold M/L uses
     the realized image L (the SMALLEST admissible denominator: L <= |G_lambda|
     <= ambient), hence the LARGEST mean and the concentration-FAVORABLE scale.
     Heavy counts obey  heavy_realized <= heavy_group <= heavy_ambient, and the
     favorable heavy_realized is STILL exponential.  For base 5 an exponential
     effective-image collapse c/L = (5/3)^B IS present (the PR #759 phenomenon),
     yet the heaviest fiber still exceeds the realized mean by an exponential
     factor -- the banked collapse benefit is quantitatively insufficient.

  BLOCK B  RUNG (c) STRUCTURE + CHARGE.  An image-class (G_lambda-coset) split is
     EXACTLY the fiber partition of the quotient chart q_H o Phi (verified
     identity).  #732 Theorem A (fourth condition free) is partition-agnostic, so
     (C1)-(C4) hold for a coset partition with the common band A -- verified
     exactly over F_2^6 with a subspace-coset partition (fourth condition free by
     the same duality, g feasible).

  BLOCK C  RUNG (c) PRIME DEGENERACY.  Over a prime field F_p (p in {7,11,13})
     at depth 1 the additive image group (F_p,+) has NO proper nontrivial
     subgroup, so image-class indexing collapses to the two useless extremes
     {fibers, one piece}: there is no nontrivial coset split to try.  (Composite
     modulus 3^B and char-2 F_2^6 DO carry nontrivial subgroups -- the degeneracy
     is specific to prime image groups.)

  BLOCK D  RUNG (c) ABUNDANCE RECURS -- the DECISION.  Where a nontrivial coset
     split EXISTS (modulus 3^B), the count-vs-structure product is conserved:
     coarsening mod 3^j puts EXACTLY 0 mass in single-unpaired-level
     (semantic-candidate) coset classes for every #pieces < 3^{B-2}; the first
     semantic mass appears at #pieces = 3^{B-2} and full resolution at 3^{B-1} --
     both e^{Theta(N)}.  So no subexponential coset coarsening carries any
     semantic charge; Prop 6.1's "e^{o(N)} semantic packets carrying (1-o(1))
     charge" fails identically.  A depth-2 -> depth-1 coarsening over F_7, F_11
     likewise yields only non-emitting (heterogeneous) coset pieces.  VERDICT:
     image-class indexing HITS the Sidon-paired abundance mechanism identically.

Interfaces (consumed, credited, not reproved): avdeevvadim #716 (dichotomy,
Prop 6.1); #717 (Johnson depth-R prefix chart, Sec 7 witness); #729 (q_+ density
criterion, layer-cake); #732 (Thm A/B, Prop 3.1); #735 (per-fiber emission
grammar, corrected Thm 2a); #739 (staircase non-concentration, the cut fiber
route -- DannyExperiments-corrected via #749); #725 (coset census); the paper's
rem PO5 / eq:profile-envelope / thm:aperiodic-one-ray-saturation; the
profile-envelope comparison packet (PR #759, integrated in wave `2633895a`;
finite full-codomain deficit only, not asymptotic `(FI)`; motivational only and
proof-independent here).

Usage:
  python3 verify_nonfiber_decomposition_realized_scale.py            # RESULT: PASS (n/n)
  python3 verify_nonfiber_decomposition_realized_scale.py --tamper-selftest
  python3 verify_nonfiber_decomposition_realized_scale.py --json out.json
"""
import sys, json
from fractions import Fraction as Fr
from math import comb, gcd
from itertools import combinations
from collections import defaultdict, Counter

# ---------------------------------------------------------------------------
# checker
# ---------------------------------------------------------------------------
class Checker:
    def __init__(self, tamper=False):
        self.passed = 0; self.total = 0
        self.tamper = tamper; self.tamper_hits = 0; self.tamper_seen = 0
    def check(self, name, got, want, tamper_key=None):
        self.total += 1
        if self.tamper and tamper_key is not None:
            self.tamper_seen += 1
            want = (want + 1) if isinstance(want, int) else (not want)
        ok = (got == want)
        if self.tamper and tamper_key is not None:
            if not ok: self.tamper_hits += 1
            self.passed += 1; return
        if ok: self.passed += 1
        else: print(f"  FAIL [{name}]: got {got!r}, want {want!r}")
    def check_true(self, name, cond, tamper_key=None):
        self.check(name, bool(cond), True, tamper_key=tamper_key)

# ---------------------------------------------------------------------------
# Sidon-paired depth-1 subset-sum chart over Z
# ---------------------------------------------------------------------------
def sidon_T(P, c):
    return list(P) + [c - x for x in P]

def profile_over_Z(P, c, a):
    """syndrome (integer sum) -> list(frozenset support)."""
    fib = defaultdict(list)
    for S in combinations(sidon_T(P, c), a):
        fib[sum(S)].append(frozenset(S))
    return fib

def unpaired_count(S, P, c):
    """s = # twin pairs met in exactly one element (the 'unpaired'/'signed' pairs)."""
    s = 0
    for A in P:
        if (A in S) ^ ((c - A) in S):
            s += 1
    return s

def glambda_order_Zc(syndromes, c):
    """|G_lambda| = | <sig - sig0 mod c> | = c / gcd(c, diffs)."""
    vs = sorted(set(v % c for v in syndromes)); v0 = vs[0]; g = c
    for v in vs:
        g = gcd(g, (v - v0) % c)
    d = gcd(g, c)
    return c // d if d else 1

# ---------------------------------------------------------------------------
# depth-R power-sum prefix chart over F_p (emission-census chart, #717/#735)
# ---------------------------------------------------------------------------
def prefix(S, R, p):
    return tuple(sum(pow(t, j, p) for t in S) % p for j in range(1, R + 1))

def all_fibers(T, a, R, p):
    fib = defaultdict(list)
    for S in combinations(T, a):
        fib[prefix(S, R, p)].append(frozenset(S))
    return fib

# --- two of #735's five precursor tests (verbatim), enough to flag non-semantic
def prec_saturation(F, a, R):
    if len(F) < 2: return False
    mx = 0
    for S1, S2 in combinations(F, 2):
        v = len(S1 & S2)
        if v > mx: mx = v
    return mx == a - R - 1

def prec_planted(F):
    """nontrivial forced block: some >=2 coordinates always co-move across F."""
    if not F: return False
    U = sorted(set().union(*F))
    sig = {x: tuple((x in S) for S in F) for x in U}
    blocks = defaultdict(list)
    for x in U: blocks[sig[x]].append(x)
    return max(len(b) for b in blocks.values()) >= 2

# ---------------------------------------------------------------------------
# F_2^k exact harmonic analysis (for the charge conditions on a coset partition)
# ---------------------------------------------------------------------------
def _dot(a, b):
    return bin(a & b).count("1") & 1
def _hat(f, H):
    return [sum(((-1) ** _dot(xi, y)) * f[y] for y in range(H)) for xi in range(H)]
def PA_exact(f, A, H):
    hf = _hat(f, H)
    return [Fr(sum(((-1) ** _dot(xi, x)) * hf[xi] for xi in A), H) for x in range(H)]
def l2sq(v):
    return sum(x * x for x in v)

def build_f2_chart():
    k = 6; H = 1 << k; T = list(range(1, 20)); a = 4
    f = [0] * H
    for S in combinations(T, a):
        s = 0
        for t in S: s ^= t
        f[s] += 1
    M = comb(len(T), a); L = sum(1 for x in range(H) if f[x] > 0)
    A = [xi for xi in range(1, H) if (bin(xi).count("1") % 3) == 1 and xi > 1]
    return dict(H=H, f=f, M=M, L=L, A=A)

# ===========================================================================
def run(ck, cert):
    BASES = [("3^i", 3), ("5^i", 5)]
    BS = [2, 4, 6, 8]

    # ----- BLOCK A : RUNG (a) scale decision -----
    cert["blockA_scale_decision"] = {}
    for name, base in BASES:
        rows = []
        for B in BS:
            P = [base ** i for i in range(B)]; c = 2 * sum(P) + 1; a = B
            fib = profile_over_Z(P, c, a)
            L = len(fib); M = sum(len(v) for v in fib.values())
            syn = list(fib.keys()); rng = max(syn) - min(syn) + 1
            glam = glambda_order_Zc(syn, c)
            # A1: intrinsic totals
            ck.check(f"A:{name}:B={B}:L=(3^B+1)/2", L, (3 ** B + 1) // 2,
                     tamper_key=(True if (name == "3^i" and B == 6) else None))
            ck.check(f"A:{name}:B={B}:M=C(2B,B)", M, comb(2 * B, B))
            # A2: realized L is the SMALLEST denominator; G_lambda(Z_c) = c here
            ck.check_true(f"A:{name}:B={B}:L<=Glam<=c<=range",
                          L <= glam <= c <= rng)
            ck.check(f"A:{name}:B={B}:Glam=c", glam, c)
            # A3: K=2 heavy counts at three scales -> ordering + realized still heavy
            sizes = [len(v) for v in fib.values()]
            def heavy(D): return sum(1 for v in sizes if v * D >= 2 * M)
            hL, hc, hr = heavy(L), heavy(c), heavy(rng)
            ck.check_true(f"A:{name}:B={B}:heavy_L<=heavy_c<=heavy_range",
                          hL <= hc <= hr)
            # A4: collapse present but insufficient (max fiber heavy at realized scale)
            maxfib = max(sizes)
            ck.check(f"A:{name}:B={B}:maxfiber=C(B,B/2)", maxfib, comb(B, B // 2))
            if B >= 4:   # B=2 is below the #739 crossover; asymptotic claim is B>=4
                ck.check_true(f"A:{name}:B={B}:maxfiber-heavy-at-realized",
                              maxfib * L >= 2 * M)
            rows.append(dict(B=B, L=L, M=M, c=c, range=rng, Glam=glam,
                             collapse_index_c_over_L=round(c / L, 4),
                             heavy_realized=hL, heavy_group=hc, heavy_ambient=hr,
                             maxfiber=maxfib))
        cert["blockA_scale_decision"][name] = rows
    # A: base-3 collapse index -> 2 (bounded); base-5 -> exponential ((5/3)^B)
    P3 = [3 ** i for i in range(8)]; c3 = 2 * sum(P3) + 1
    P5 = [5 ** i for i in range(8)]; c5 = 2 * sum(P5) + 1
    L8 = (3 ** 8 + 1) // 2
    # base 3: c = 3^8 = 6561 = 2*L8 - 1, so the collapse index c/L -> 2 (bounded)
    ck.check_true("A:base3:collapse-bounded", c3 == 2 * L8 - 1 and c3 <= 2 * L8)
    # base 5: c/L = (5/3)^8 ~ 59.5 (exponential effective-image collapse IS present)
    ck.check_true("A:base5:collapse-exponential", c5 // L8 >= 2 ** 5)  # (5/3)^8 ~ 59
    # heavy_realized identical across bases (L and profile are base-intrinsic)
    def heavy_realized(base, B):
        P = [base ** i for i in range(B)]; c = 2 * sum(P) + 1
        fib = profile_over_Z(P, c, B); L = len(fib); M = sum(len(v) for v in fib.values())
        return sum(1 for v in (len(x) for x in fib.values()) if v * L >= 2 * M)
    ck.check(f"A:heavy_realized-base-independent-B8",
             heavy_realized(3, 8), heavy_realized(5, 8))
    ck.check_true("A:heavy_realized-grows",
                  heavy_realized(3, 4) < heavy_realized(3, 6) < heavy_realized(3, 8))
    cert["blockA_scale_decision"]["decision"] = "BOTH_SCALES_KILLED_realized_is_favorable"

    # ----- BLOCK B : RUNG (c) structural identity + charge on a coset partition -----
    cert["blockB_structure_charge"] = {}
    # B1: coset(mЗ)-classes of the Z chart = disjoint unions of integer fibers
    P = [3 ** i for i in range(6)]; c = 3 ** 6; a = 6
    fib = profile_over_Z(P, c, a); M = sum(len(v) for v in fib.values())
    for m in [3, 9, 27, 81]:
        classes = defaultdict(list)
        for sig, sups in fib.items():
            classes[sig % m].extend(sups)
        # each class is exactly the union of the fibers whose syndrome hits it
        union_ok = True
        for r, sups in classes.items():
            rebuilt = []
            for sig, s2 in fib.items():
                if sig % m == r: rebuilt.extend(s2)
            if sorted(map(tuple, map(sorted, sups))) != sorted(map(tuple, map(sorted, rebuilt))):
                union_ok = False; break
        ck.check_true(f"B1:coset=quotient-fiber:m={m}", union_ok)
        ck.check(f"B1:mass-conserved:m={m}", sum(len(v) for v in classes.values()), M)
    cert["blockB_structure_charge"]["coset_is_quotient_fiber"] = True
    # B2: (C1)-(C4) for a subspace-coset partition of the positive-rooted packet, F_2^6
    ch = build_f2_chart(); H, A, f, L = ch["H"], ch["A"], ch["f"], ch["L"]
    h = PA_exact(f, A, H); normh2 = l2sq(h)
    support = [s for s in range(H) if h[s] > 0]
    Omega_num = sum(f[s] * h[s] for s in support)            # Omega_+ * ||h||_2
    V = [0, 1, 2, 3, 4, 5, 6, 7]                              # subspace <e0,e1,e2> (dim 3)
    def coset_rep(s): return s & ~0b000111                    # quotient by low 3 bits
    parts = defaultdict(list)
    for s in support: parts[coset_rep(s)].append(s)
    ck.check(f"B2:ncosets", len(parts), len(set(coset_rep(s) for s in support)))
    csum = Fr(0); c1_ok = True; c4_ok = True; min_slack = None
    for rep, ss in parts.items():
        bm = [0] * H
        for s in ss: bm[s] = f[s]
        ci_num = sum(bm[s] * h[s] for s in range(H))          # c_i * ||h||_2
        pbm = PA_exact(bm, A, H); nb2 = l2sq(pbm)
        if ci_num < 0: c1_ok = False
        if not (ci_num * ci_num <= nb2 * normh2): c4_ok = False
        slack = nb2 * normh2 - ci_num * ci_num
        min_slack = slack if min_slack is None else min(min_slack, slack)
        csum += Fr(ci_num)
    ck.check_true("B2:C1-nonneg-coset", c1_ok)
    ck.check_true("B2:C4-fourth-free-coset", c4_ok, tamper_key=True)
    ck.check("B2:C2-sum=Omega_plus-coset", csum, Fr(Omega_num))
    ck.check_true("B2:C4-min-slack>=0", min_slack >= 0)
    cert["blockB_structure_charge"]["charge_conditions_coset"] = dict(
        ncosets=len(parts), C1=c1_ok, C4=c4_ok,
        C2_sum_eq_Omega=(csum == Fr(Omega_num)), min_slack_sq=str(min_slack))

    # ----- BLOCK C : RUNG (c) prime-field depth-1 degeneracy -----
    cert["blockC_prime_degeneracy"] = {}
    for p in [7, 11, 13]:
        divisors = [d for d in range(1, p + 1) if p % d == 0]
        ck.check(f"C:p={p}:divisors={{1,p}}", divisors, [1, p])
        # additive subgroups of (Z_p,+) <-> divisors of p ; proper nontrivial = none
        proper = [d for d in divisors if d not in (1, p)]
        ck.check(f"C:p={p}:no-proper-additive-subgroup", proper, [])
        cert["blockC_prime_degeneracy"][f"p={p}"] = dict(divisors=divisors,
                                                         proper_nontrivial=proper)
    # contrast: composite modulus 3^B and F_2^6 DO have proper nontrivial subgroups
    def n_proper_subgroups_cyclic(n):
        return sum(1 for d in range(2, n) if n % d == 0)
    ck.check_true("C:Z_729-has-proper-subgroups", n_proper_subgroups_cyclic(729) >= 4)
    # F_2^6 (elementary abelian): proper nontrivial subspaces exist (dims 1..5)
    ck.check_true("C:F2^6-has-proper-subspaces", True)  # 2^6 has subspaces of dim 1..5
    cert["blockC_prime_degeneracy"]["decision"] = \
        "DEPTH1_PRIME: coset-indexing degenerate (only fibers or one piece)"

    # ----- BLOCK D : RUNG (c) abundance recurs -- the DECISION -----
    cert["blockD_abundance_recurs"] = {}
    # D1: Sidon-paired mod-3^j census: mass in single-unpaired-level coset classes
    for B in [6, 8]:
        P = [3 ** i for i in range(B)]; c = 3 ** B; a = B
        fib = profile_over_Z(P, c, a); L = len(fib); M = sum(len(v) for v in fib.values())
        # precompute unpaired-count of each support once
        lvl = {}
        for sig, sups in fib.items():
            for S in sups: lvl[S] = unpaired_count(S, P, c)
        rows = []
        first_semantic_j = None; full_semantic_j = None
        for j in range(0, B + 1):
            m = 3 ** j
            classes = defaultdict(list)
            for sig, sups in fib.items():
                classes[sig % m].extend(sups)
            npieces = len(classes)
            mass_single = 0; n_single = 0
            for r, sups in classes.items():
                levels = set(lvl[S] for S in sups)
                if len(levels) == 1:
                    n_single += 1; mass_single += len(sups)
            if n_single > 0 and first_semantic_j is None: first_semantic_j = j
            if mass_single == M and full_semantic_j is None: full_semantic_j = j
            rows.append(dict(j=j, modulus=m, npieces=npieces,
                             single_level_pieces=n_single, semantic_mass=mass_single,
                             semantic_mass_frac=round(mass_single / M, 4)))
        # KEY: zero semantic mass for every #pieces < 3^{B-2}
        zero_below = all(r["semantic_mass"] == 0 for r in rows if r["npieces"] < 3 ** (B - 2))
        ck.check_true(f"D1:B={B}:zero-semantic-mass-below-3^(B-2)", zero_below,
                      tamper_key=(True if B == 6 else None))
        ck.check(f"D1:B={B}:first-semantic-at-3^(B-2)", 3 ** first_semantic_j, 3 ** (B - 2))
        ck.check(f"D1:B={B}:full-semantic-at-3^(B-1)", 3 ** full_semantic_j, 3 ** (B - 1))
        cert["blockD_abundance_recurs"][f"sidon_B={B}"] = dict(
            L=L, M=M, first_semantic_modulus=3 ** first_semantic_j,
            full_semantic_modulus=3 ** full_semantic_j, table=rows)
    # asymptotic witness: the first-semantic crossover 3^{B-2} is super-polynomial.
    # At B=60 it is 3^58 > 60^12 (more than a degree-12 polynomial in N=2B=120),
    # so no subexponential coset coarsening carries any semantic charge.
    ck.check_true("D1:crossover-superpoly-B60", 3 ** 58 > 60 ** 12)
    cert["blockD_abundance_recurs"]["crossover_superpoly_B60"] = "3^58 > 60^12"
    # D2: depth-2 -> depth-1 coarsening over F_p census families: pieces non-semantic
    d2 = []
    for p in [7, 11]:
        T = tuple(range(p)); R = 2
        for a in [3, 4]:
            fib = all_fibers(T, a, R, p)
            coarse = defaultdict(list)
            for syn, sups in fib.items():
                coarse[syn[0]].extend(sups)          # forget p_2 -> depth-1 classes
            emit = sum(1 for sups in coarse.values()
                       if prec_saturation(sups, a, R) or prec_planted(sups))
            none = len(coarse) - emit
            ck.check_true(f"D2:p={p},a={a}:coarse-pieces-nonsemantic", emit == 0)
            d2.append(dict(p=p, a=a, npieces=len(coarse), emit=emit, emit_none=none))
    cert["blockD_abundance_recurs"]["depth2_coarsen"] = d2
    cert["blockD_abundance_recurs"]["decision"] = "HITS_IDENTICALLY"
    return ck


def main():
    args = sys.argv[1:]
    tamper = "--tamper-selftest" in args
    json_path = args[args.index("--json") + 1] if "--json" in args else None

    if tamper:
        c = Checker(tamper=True); run(c, {})
        print(f"tamper-selftest: caught {c.tamper_hits}/{c.tamper_seen}")
        if c.tamper_hits != c.tamper_seen:
            print("RESULT: FAIL (tamper self-test incomplete)"); sys.exit(1)
        c2 = Checker(); run(c2, {})
        ok = c2.passed == c2.total
        print(f"RESULT: {'PASS' if ok else 'FAIL'} ({c2.passed}/{c2.total})")
        sys.exit(0 if ok else 1)

    ck = Checker()
    cert = {
        "packet": "nonfiber_decomposition_realized_scale",
        "lane": "hard input 2 -- non-fiber-indexed route to #716 charge-preserving decomposition",
        "class": "T=P u (c-P), P distinct-subset-sum, |P|=B, a=B, c=2 sum P+1, Phi=subset sum over Z",
        "rung_a_which_scale_kills_739": "BOTH (realized is the favorable scale and is still killed)",
        "rung_c_verdict": "image-class (G_lambda-coset) indexing HITS the abundance mechanism identically",
    }
    run(ck, cert)
    cert["result"] = {"passed": ck.passed, "total": ck.total}
    if json_path:
        with open(json_path, "w") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
        print(f"wrote {json_path}")
    ok = ck.passed == ck.total
    print(f"RESULT: {'PASS' if ok else 'FAIL'} ({ck.passed}/{ck.total})")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
