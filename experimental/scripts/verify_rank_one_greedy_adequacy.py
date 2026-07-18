#!/usr/bin/env python3
"""Verifier: the local scalar adequacy depth law and greedy completion.

Claims checked (see experimental/notes/thresholds/rank_one_greedy_adequacy.md):

  T1  (B-independence)   per class, best-pattern payment / omega-cap is a
                         pure function of (k, top set, r, sign G): the
                         2^{s_low+1}|G| factor cancels.  Brute Fourier data
                         at B = 6 matches the abstract trig instance.
  T2  (depth <= 3 law)   single-pattern adequacy best >= cap holds for ALL
                         3-adic instances at k <= 3 (exhaustive; worst
                         ratio exactly 1 attained) -- hence for EVERY B,
                         one pattern reaches each hierarchy piece's local
                         scalar cap (upgrades #820 S5 to an all-B scalar
                         theorem at these depths).
  T3  (depth >= 4 fails) the first violating instance is EXACTLY
                         (k, r, top, sG) = (4, 4, {0,1,2}, -1), ratio
                         0.99100917...; worst ratios decay with k
                         (0.7229 / 0.5978 / 0.4482 at k = 4/5/6); the
                         violation is REALIZED by an actual (piece, class)
                         pair at B = 6, k = 4 (brute Fourier witness).
                         #820's open question "best >= cap at general B"
                         resolves NEGATIVELY at depth >= 4, positively at
                         depth <= 3.
  T4  (greedy completion) paying patterns in decreasing |hcube| until the
                         local scalar omega-cap sum h_+ is sound (#820 S4)
                         and scalar-adequate at EVERY depth:
                             sum_eps |h| <= 2^m sum_D |hcube(D)|
                         (triangle inequality), so the cumulative payments
                         always reach the cap.  Exhaustive at k <= 5, spot
                         k in {6,7} at the worst instances; pattern counts
                         pinned.

stdlib only, deterministic; floats under exact Parseval + Lemma-N guards.

Usage:
  python3 verify_rank_one_greedy_adequacy.py
  python3 verify_rank_one_greedy_adequacy.py --tamper-selftest
  python3 verify_rank_one_greedy_adequacy.py --emit-certificate PATH
"""
import json
import sys
from cmath import exp as cexp
from itertools import combinations
from math import comb, cos, pi, sin

FAILED = []
PASSED = [0]


def check(name, ok):
    if ok:
        PASSED[0] += 1
    else:
        FAILED.append(name)
    print(f"  [{'ok' if ok else 'FAIL'}] {name}")


TAMPER = {"triangle": False, "onset": False, "greedy_order": False,
          "ratio_table": False, "realization": False}


# ------------------------------------------------- abstract trig instances

def instance(betas, sG):
    """Return (best, cap, l1, coeff_sum, greedy_used) in 2|G|-units."""
    m = len(betas)
    pays = []
    for mask in range(2 ** m):
        if bin(mask).count("1") % 2:
            continue
        p = 1.0
        for i in range(m):
            p *= abs(sin(betas[i])) if (mask >> i) & 1 else abs(cos(betas[i]))
        pays.append(2 ** m * p)
    hvals = [sG * cos(sum((1 if not (e >> i) & 1 else -1) * betas[i]
                          for i in range(m))) for e in range(2 ** m)]
    cap = sum(v for v in hvals if v > 0)
    l1 = sum(abs(v) for v in hvals)
    pays.sort(reverse=not TAMPER["greedy_order"])
    acc = 0.0
    used = 0
    stop = cap
    for p in pays:
        if acc >= stop - 1e-12:
            break
        acc = min(acc + p, stop)
        used += 1
    return (pays[0] if pays else 0.0), cap, l1, sum(pays), acc, used


def adic_betas(k, topmask, r):
    return [2 * pi * r * 3 ** j / 3 ** k for j in range(k)
            if (topmask >> j) & 1]


def sweep(kmax):
    """Yield (k, topmask, r, sG, instance data) exhaustively."""
    for k in range(1, kmax + 1):
        ck = 3 ** k
        for topmask in range(1, 2 ** k):
            betas = None
            for r in range(1, ck):
                for sG in (1, -1):
                    yield k, topmask, r, sG, instance(
                        adic_betas(k, topmask, r), sG)


def v_depth_law(cert):
    n = 0
    worst_by_k = {}
    first_viol = None
    greedy_fail = 0
    tri_fail = 0
    max_used = {}
    for k, topmask, r, sG, (best, cap, l1, tot, acc, used) in sweep(5):
        n += 1
        if cap <= 1e-12:
            continue
        q = best / cap
        worst_by_k[k] = min(worst_by_k.get(k, 9e9), q)
        if q < 1 - 1e-12 and first_viol is None:
            first_viol = (k, topmask, r, sG)
        if tot < l1 - 1e-9:
            tri_fail += 1
        if acc < cap - 1e-9:
            greedy_fail += 1
        max_used[k] = max(max_used.get(k, 0), used)
    onset = (4, 0b0111, 4, -1)
    if TAMPER["onset"]:
        onset = (3, 0b0111, 4, -1)
    check(f"T2: single-pattern adequacy EXHAUSTIVE at k <= 3 (worst ratios {worst_by_k[1]:.4f}/{worst_by_k[2]:.4f}/{worst_by_k[3]:.4f}, all == 1)",
          all(abs(worst_by_k[k] - 1.0) <= 1e-12 for k in (1, 2, 3)))
    # margin structure: equality exactly on single-sign-nonnegative
    # instances (provable case), strict margin >= 0.0229 elsewhere
    eq = strict_min = None
    eq_ss = eq_n = 0
    strict_min = 9e9
    for k, topmask, r, sG, (best, cap, l1, tot, acc, used) in sweep(3):
        if cap <= 1e-12:
            continue
        rel = (best - cap) / cap
        if abs(rel) <= 1e-11:
            eq_n += 1
            hv = [sG * cos(sum((1 if not (e >> i) & 1 else -1) * b
                               for i, b in enumerate(adic_betas(k, topmask, r))))
                  for e in range(2 ** bin(topmask).count("1"))]
            if all(v >= -1e-12 for v in hv):
                eq_ss += 1
        else:
            strict_min = min(strict_min, rel)
    check(f"T2: equality set == single-sign-nonneg instances ({eq_ss}/{eq_n} == 148/148); min strict margin {strict_min:.4f} >= 0.0229 (float-safe)",
          eq_n == 148 and eq_ss == 148 and strict_min >= 0.0229)
    # exactness closure: no |h| value is ever near zero at 3-adic angles
    # (cos(2 pi x) = 0 needs denominator 4; impossible at 3-power
    # denominators), so the single-sign classification cannot be
    # float-fooled and the h >= 0 one-line equality proof is exact.
    minh = 9e9
    for k, topmask, r, sG, _ in sweep(3):
        for e in range(2 ** bin(topmask).count("1")):
            hv = abs(cos(sum((1 if not (e >> i) & 1 else -1) * b
                             for i, b in enumerate(adic_betas(k, topmask, r)))))
            minh = min(minh, hv)
    check(f"T2: |h| floor over ALL k <= 3 instance values == |cos(2 pi 7/27)| = 0.0581 (got {minh:.4f}; single-sign classification float-safe, cos zeros impossible at 3-power denominators)",
          abs(minh - abs(cos(2 * pi * 7 / 27))) <= 1e-12 and minh > 0.05)
    check(f"T3: FIRST violating instance == (k,r,top,sG) = (4,4,{{0,1,2}},-1) (got {first_viol})",
          first_viol == onset)
    r4 = 0.75 if TAMPER["ratio_table"] else 0.7229
    check(f"T3: worst ratio at k=4 == 0.7229 (got {worst_by_k[4]:.4f}); k=5 == 0.5978 (got {worst_by_k[5]:.4f})",
          abs(worst_by_k[4] - r4) <= 5e-4 and abs(worst_by_k[5] - 0.5978) <= 5e-4)
    check(f"T4: triangle inequality sum_D pays >= cube l1, ALL {n} instances k <= 5 ({tri_fail} failures)",
          tri_fail == 0)
    check(f"T4: greedy reaches the cap on ALL charged instances k <= 5 ({greedy_fail} failures) using at most 2 patterns (max {max(max_used.values())})",
          greedy_fail == 0 and max(max_used.values()) == 2)
    if cert is not None:
        cert["instances_k_le_5"] = n
        cert["worst_ratio_by_k"] = {str(k): round(v, 6)
                                    for k, v in sorted(worst_by_k.items())}
        cert["greedy_max_patterns_by_k"] = {str(k): v for k, v
                                            in sorted(max_used.items())}


def v_deep_spot(cert):
    # k = 6: EXHAUSTIVE (all topmasks, all r, both signs); k = 7: the
    # exact worst instance from the k <= 7 scout.
    worst6 = 9e9
    ok_greedy = True
    used6 = 0
    for topmask in range(1, 2 ** 6):
        for r in range(1, 3 ** 6):
            for sG in (1, -1):
                best, cap, l1, tot, acc, used = instance(
                    adic_betas(6, topmask, r), sG)
                if cap <= 1e-12:
                    continue
                worst6 = min(worst6, best / cap)
                used6 = max(used6, used)
                if acc < cap - 1e-9 or tot < l1 - 1e-9:
                    ok_greedy = False
    b7, c7, l7, t7, a7, u7 = instance(adic_betas(7, 2 ** 7 - 1, 1367), 1)
    check(f"T3: k=6 EXHAUSTIVE worst ratio == 0.4482 (got {worst6:.4f}); k=7 worst instance == 0.3280 (got {b7/c7:.4f})",
          abs(worst6 - 0.4482) <= 5e-4 and abs(b7 / c7 - 0.3280) <= 5e-4)
    check(f"T4: greedy + triangle hold on the ENTIRE k=6 sweep (max patterns {used6} == 3) and the k=7 worst instance (patterns {u7} == 4)",
          ok_greedy and used6 == 3 and u7 == 4
          and a7 >= c7 - 1e-9 and t7 >= l7 - 1e-9)
    if cert is not None:
        cert["k6_exhaustive_worst"] = round(worst6, 6)
        cert["k6_greedy_max_patterns"] = used6
        cert["k7_worst_instance_ratio"] = round(b7 / c7, 6)
        cert["k7_worst_patterns_used"] = u7


# --------------------------------------------- realization at B = 6, k = 4

B = 6
c = 3 ** B
P = [3 ** i for i in range(B)]


def s3(y, ndig):
    y %= 3 ** ndig
    s = 0
    for _ in range(ndig):
        d = y % 3
        if d == 2:
            d = -1
        y = (y - d) // 3
        s += d != 0
    return s


def wtil(s):
    if s < 0 or s > B:
        return 0
    return comb(B - s, (B - s) // 2) if s % 2 == B % 2 else 0


def factors_poly(angles):
    poly = [1.0]
    for th in angles:
        t = 2 * cos(th)
        new = [0.0] * (len(poly) + 2)
        for i, a in enumerate(poly):
            new[i] += a
            new[i + 1] += a * t
            new[i + 2] += a
        poly = new
    return poly


def v_guards_and_realization(cert):
    HF = [factors_poly([2 * pi * ((j * 3 ** i) % c) / c
                        for i in range(B)])[B] for j in range(c)]
    m2 = sum(comb(B, s) * 2 ** s * wtil(s) ** 2 for s in range(B + 1))
    check("guard: Parseval sum hatf^2 == c * M2 (1e-6 rel)",
          abs(sum(x * x for x in HF) - c * m2) <= 1e-6 * c * m2)
    T = P + [c - p for p in P]
    N = [0] * c
    for S in combinations(T, B):
        N[sum(S) % c] += 1
    check("guard: Lemma N exact (B=6 brute)",
          all(N[y] == wtil(s3(y, B)) for y in range(c)))
    # realization: k = 4, piece {xi == +-4 mod 81}, class with top at
    # positions {2,3,4} (j = 0,1,2) and one low coordinate chosen so that
    # sign G(s_low) = -1.  G(s_low) sign: need G_4(s_low) < 0.
    k, r = 4, 4
    ck = 3 ** k
    Gr = [sum(cexp(-2j * pi * a * r / ck) * wtil(s3(a, k) + l)
              for a in range(ck)).real / ck for l in range(B + 1)]
    # find s_low in {0,1,2} (B-k = 2 low positions) with G < 0
    slow = next(l for l in range(B - k + 1) if Gr[l] < -1e-12)
    v = [0] * B
    lowpos = list(range(B - k))[:slow]
    for i in lowpos:
        v[i] = 1
    for j in (0, 1, 2):
        v[B - k + j] = 1
    if TAMPER["realization"]:
        v[B - k + 3] = 1 - v[B - k + 3]
    s = sum(v)
    if s % 2 != B % 2:  # parity fix with a second low coordinate
        for i in range(B - k):
            if not v[i]:
                v[i] = 1
                break
        s = sum(v)
    U = [i for i in range(B) if v[i]]
    EXP = [cexp(-2j * pi * t / c) for t in range(c)]
    Ab = sorted(set((r + ck * m) % c for m in range(3 ** (B - k)))
                | set((ck - r + ck * m) % c for m in range(3 ** (B - k))))
    hv = []
    for bits in range(2 ** s):
        sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                  for t in range(s)) % c
        hv.append(sum(HF[xi] * EXP[(xi * sig) % c] for xi in Ab).real / c)
    pos = sum(x for x in hv if x > 0)
    best = max(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                       for bits, x in enumerate(hv)) / 2 ** s) * 2 ** s
               for dbits in range(2 ** s))
    tot_pays = sum(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                           for bits, x in enumerate(hv)) / 2 ** s) * 2 ** s
                   for dbits in range(2 ** s))
    check(f"T3: REALIZED at B=6, k=4, piece {{+-4 mod 81}}, class {''.join(map(str, v))}: best {best:.4f} < cap {pos:.4f} (ratio {best/pos:.4f})",
          pos > 1e-9 and best < pos - 1e-6)
    check(f"T4: total coefficient capacity reaches the same class's scalar cap ({tot_pays:.4f} >= cap)",
          tot_pays >= pos - 1e-9)
    # T1: brute ratio == abstract instance ratio (B-independence anchor)
    worst_t1 = 0.0
    for kk, rr in ((2, 1), (3, 5)):
        cck = 3 ** kk
        Gr2 = [sum(cexp(-2j * pi * a * rr / cck) * wtil(s3(a, kk) + l)
                   for a in range(cck)).real / cck for l in range(B + 1)]
        Ab2 = sorted(set((rr + cck * m) % c for m in range(3 ** (B - kk)))
                     | set((cck - rr + cck * m) % c
                           for m in range(3 ** (B - kk))))
        for vv in ((0, 1, 0, 0, 1, 1), (1, 1, 0, 1, 1, 0)):
            ss = sum(vv)
            UU = [i for i in range(B) if vv[i]]
            top = [t for t in range(ss) if UU[t] >= B - kk]
            if not top:
                continue
            sl = ss - len(top)
            if abs(Gr2[sl]) < 1e-12:
                continue
            hh = []
            for bits in range(2 ** ss):
                sig = sum((1 if not (bits >> t) & 1 else -1) * P[UU[t]]
                          for t in range(ss)) % c
                hh.append(sum(HF[xi] * EXP[(xi * sig) % c]
                              for xi in Ab2).real / c)
            bb = max(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                             for bits, x in enumerate(hh)) / 2 ** ss)
                     * 2 ** ss for dbits in range(2 ** ss))
            pp = sum(x for x in hh if x > 0)
            topmask2 = sum(1 << (UU[t] - (B - kk)) for t in top)
            ab, ac_, _, _, _, _ = instance(
                adic_betas(kk, topmask2, rr),
                1 if Gr2[sl] > 0 else -1)
            if pp > 1e-9 and ac_ > 1e-12:
                worst_t1 = max(worst_t1, abs(bb / pp - ab / ac_))
    check(f"T1: brute best/cap == abstract instance best/cap (B-independence anchor; worst {worst_t1:.1e})",
          worst_t1 <= 1e-9)
    if cert is not None:
        cert["realized_witness"] = {"k": k, "r": r,
                                    "class": "".join(map(str, v)),
                                    "ratio": round(best / pos, 6)}


def v_structure_essential(cert):
    """T5: m <= 2 holds for all angles (m = 2 an exact identity); m = 3
    fails at general angles (deterministic witness)."""
    import random
    random.seed(20260716)
    worst12 = 9e9
    wid = 0.0
    for _ in range(20000):
        m = random.choice([1, 2])
        bb = [random.uniform(0, 2 * pi) for _ in range(m)]
        sG = random.choice([1, -1])
        best, cap, l1, tot, acc, used = instance(bb, sG)
        if cap > 1e-12:
            worst12 = min(worst12, best / cap)
        if m == 2:
            b1, b2 = bb
            wid = max(wid, abs(abs(cos(b1 + b2)) + abs(cos(b1 - b2))
                               - 2 * max(abs(cos(b1) * cos(b2)),
                                         abs(sin(b1) * sin(b2)))))
    wit = (5.524, 5.474, 2.378)
    if TAMPER["realization"]:
        wit = (0.5, 0.5, 0.5)
    bw, cw, _, _, _, _ = instance(list(wit), -1)
    check(f"T5: m <= 2 holds for ALL angles (20k random, worst ratio {worst12:.6f}); m=2 identity exact (worst {wid:.1e})",
          worst12 >= 1 - 1e-9 and wid <= 1e-12)
    check(f"T5: m = 3 general-angle witness (5.524, 5.474, 2.378, sG=-1) VIOLATES (LHS {bw:.3f} < RHS {cw:.3f})",
          bw < cw - 0.5)
    if cert is not None:
        cert["t5_witness_lhs_rhs"] = [round(bw, 4), round(cw, 4)]


def v_realized_census(cert):
    """T3: the B = 6 depth-4 realized census and the B = 8 second-point
    brute confirmation of the deep witness."""
    HF = [factors_poly([2 * pi * ((j * 3 ** i) % c) / c
                        for i in range(B)])[B] for j in range(c)]
    EXP = [cexp(-2j * pi * t / c) for t in range(c)]
    cls = [tuple((n >> i) & 1 for i in range(B)) for n in range(2 ** B)
           if bin(n).count("1") % 2 == B % 2 and bin(n).count("1") >= 2]
    k, ck = 4, 81
    charged = viol = 0
    worst = (9e9, None)
    configs = set()
    for r in range(1, 41):
        Ab = sorted(set((r + ck * m) % c for m in range(3 ** (B - k)))
                    | set((ck - r + ck * m) % c for m in range(3 ** (B - k))))
        for v in cls:
            s = sum(v)
            U = [i for i in range(B) if v[i]]
            hv = []
            for bits in range(2 ** s):
                sig = sum((1 if not (bits >> t) & 1 else -1) * P[U[t]]
                          for t in range(s)) % c
                hv.append(sum(HF[xi] * EXP[(xi * sig) % c]
                              for xi in Ab).real / c)
            pos = sum(x for x in hv if x > 0)
            if pos <= 1e-9:
                continue
            charged += 1
            best = max(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                               for bits, x in enumerate(hv)) / 2 ** s)
                       * 2 ** s for dbits in range(2 ** s))
            if best < pos - 1e-9:
                viol += 1
                configs.add((tuple(i for i in U if i >= B - k), r % 3))
                if best / pos < worst[0]:
                    worst = (best / pos, (r, "".join(map(str, v))))
    check(f"T3: B=6 depth-4 realized census -- {charged} charged, {viol} violations (expect 958/10), worst REALIZED {worst[0]:.5f} == 0.86405 at {worst[1]}",
          charged == 958 and viol == 10
          and abs(worst[0] - 0.86405) <= 5e-5)
    # abstract worst (top {0,1,2}, r=71, sG=-1) unrealized at B=6:
    G71 = [sum(cexp(-2j * pi * a * 71 / ck) * wtil(s3(a, k) + l)
               for a in range(ck)).real / ck for l in range(B + 1)]
    check("T3: abstract worst (top {0,1,2}, r=71, sG=-1) UNREALIZED at B=6 (G_4 > 0 at every parity-admissible s_low)",
          all(G71[l] > 1e-12 for l in range(B - k + 1)))
    # B = 8 second point: all-ones class on {+-10 mod 81}
    B8 = 8
    c8 = 3 ** B8
    HF8 = [factors_poly([2 * pi * ((j * 3 ** i) % c8) / c8
                         for i in range(B8)])[B8] for j in range(c8)]
    E8 = [cexp(-2j * pi * t / c8) for t in range(c8)]
    P8 = [3 ** i for i in range(B8)]
    Ab8 = sorted(set((10 + 81 * m) % c8 for m in range(3 ** (B8 - 4)))
                 | set((71 + 81 * m) % c8 for m in range(3 ** (B8 - 4))))
    hv8 = []
    for bits in range(2 ** B8):
        sig = sum((1 if not (bits >> t) & 1 else -1) * P8[t]
                  for t in range(B8)) % c8
        hv8.append(sum(HF8[xi] * E8[(xi * sig) % c8] for xi in Ab8).real / c8)
    pos8 = sum(x for x in hv8 if x > 0)
    best8 = max(abs(sum(((-1) ** bin(bits & dbits).count("1")) * x
                        for bits, x in enumerate(hv8)) / 2 ** B8) * 2 ** B8
                for dbits in range(2 ** B8))
    check(f"T3: B=8 brute second point -- all-ones class on {{+-10 mod 81}}: best {best8:.5f} < cap {pos8:.5f}, ratio {best8/pos8:.5f} == 0.86405 (B-independent, matches B=6)",
          best8 < pos8 and abs(best8 / pos8 - 0.86405) <= 5e-5)
    if cert is not None:
        cert["b6_k4_census"] = {"charged": charged, "violations": viol,
                                "distinct_top_configs": len(configs),
                                "worst_realized": round(worst[0], 6)}
        cert["b8_witness"] = {"best": round(best8, 6),
                              "cap": round(pos8, 6)}


def run_all(cert=None):
    v_guards_and_realization(cert)
    v_depth_law(cert)
    v_deep_spot(cert)
    v_structure_essential(cert)
    v_realized_census(cert)
    if TAMPER["triangle"]:
        # meta-tamper: assert the triangle inequality FAILS somewhere
        found = False
        for k, topmask, r, sG, (b, cp, l1, tot, a, u) in sweep(3):
            if tot < l1 - 1e-9:
                found = True
        check("meta: tampered triangle claim finds a violation", found)
    print(f"RESULT: {'PASS' if not FAILED else 'FAIL'} "
          f"({PASSED[0]}/{PASSED[0] + len(FAILED)})")
    return not FAILED


def tamper_selftest():
    import subprocess
    caught = 0
    keys = list(TAMPER)
    for key in keys:
        rr = subprocess.run([sys.executable, __file__, f"--tamper={key}"],
                            capture_output=True, text=True)
        ok = "RESULT: FAIL" in rr.stdout
        caught += ok
        print(f"tamper {key}: {'caught' if ok else 'MISSED'}")
    print(f"tamper-selftest: caught {caught}/{len(keys)}")
    return caught == len(keys)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--tamper-selftest":
        sys.exit(0 if tamper_selftest() else 1)
    for a in args:
        if a.startswith("--tamper="):
            TAMPER[a.split("=", 1)[1]] = True
    cert = None
    path = None
    if args and args[0] == "--emit-certificate":
        path = args[1]
        cert = {"packet": "rank-one-greedy-adequacy", "chart": "base-3",
                "claims": ["T1", "T2", "T3", "T4"],
                "scope": {
                    "certifies": "local scalar capped-Walsh accounting",
                    "does_not_certify": [
                        "same-owner first-match profile cell",
                        "A4 analytic/Sidon payment",
                        "A6/RC distinct-slope bound",
                        "uniform subexponential aggregate census",
                    ],
                }}
    ok = run_all(cert)
    if cert is not None and ok:
        with open(path, "w") as fh:
            json.dump(cert, fh, indent=1, sort_keys=True)
        print(f"certificate -> {path}")
    sys.exit(0 if ok else 1)
