#!/usr/bin/env python3
"""Heavy census + fit for the fiber-image tradeoff note (documented runtime).

Finds the best-rho(b) sequence by a symmetric interval-with-holes hill-climb
(exhaustive is infeasible past b~14), then fits three models to distinguish a
genuine sub-log2 cap from a slow poly-loss climb toward log2 (the #646 lesson).
Also scans structured non-interval families. Prints everything; nonzero exit
only on an internal inconsistency.  Runtime: a few minutes under
`ulimit -v 2097152`.  Reproduces the numbers quoted in
experimental/notes/thresholds/fiber_image_tradeoff.md (R3 fit).

  rho(V) = phi + lambda - log2,  phi = log fstar/b,  lambda = log L1/b.
  Models fit to best_rho(b):
    (M1) genuine cap:      rho = R - C/b           (asymptote R)
    (M2) log-poly climb:   rho = log2 - C*log(b)/b (forced to log2)
    (M3) cap + poly loss:  rho = R - C*log(b)/b    (asymptote R)
  Verdict rests on whether M1/M3 asymptote R sits well below log2 = 0.6931 and
  whether M2 (forced-to-log2) fits far worse.
"""
from __future__ import annotations
import itertools, math, random, sys
from collections import defaultdict
from math import comb, gcd, log

LOG2 = math.log(2)
random.seed(20260711)


def sig_dp(V):
    dp = defaultdict(int); dp[(0, 0, 0)] = 1
    for v in V:
        vv = v * v; nd = defaultdict(int)
        for (w, s, q), c in dp.items():
            nd[(w, s, q)] += c
            nd[(w + 1, s + v, q + vv)] += c
        dp = nd
    return dp


def stat(V):
    dp = sig_dp(V); b = len(V)
    f = max(dp.values()); L = len(dp)
    return f, L, (log(f) + log(L)) / b - LOG2, log(f) / b, log(L) / b


def sym_block(n, holes):
    """symmetric block on {0..n} minus a symmetric hole set (holes given as <= n/2 reps)."""
    H = set()
    for h in holes:
        H.add(h); H.add(n - h)
    return tuple(x for x in range(n + 1) if x not in H)


def best_rho_symmetric(b, tries=60, iters=400):
    """hill-climb over symmetric interval-with-holes blocks of size b."""
    best = (-1.0, None, 0, 0)
    for _ in range(tries):
        # pick a diameter n in [b-1, ~2.3b]; need (n+1) - (#hole slots) = b, symmetric
        n = random.randint(b, int(2.3 * b) + 2)
        half = n // 2
        need_removed = (n + 1) - b
        if need_removed < 0:
            continue
        # symmetric holes: each interior hole h != n-h removes 2; center (if n even) removes 1
        # choose a random symmetric hole set of the right total size
        cand_pairs = [h for h in range(0, half + 1) if h != n - h]  # each removes 2
        center = [n // 2] if n % 2 == 0 else []                     # removes 1
        # solve need_removed = 2*p (+1 if center used)
        holes = None
        for use_c in ((1, 0) if center else (0,)):
            rem = need_removed - use_c
            if rem >= 0 and rem % 2 == 0 and rem // 2 <= len(cand_pairs):
                p = rem // 2
                chosen = random.sample(cand_pairs, p)
                if use_c:
                    chosen = chosen + center
                holes = chosen
                break
        if holes is None:
            continue
        V = sym_block(n, holes)
        if len(V) != b or len(set(V)) != b:
            continue
        f, L, rho, phi, lam = stat(V)
        cur = (rho, V, f, L)
        # local search: toggle one hole pair (move a deletion) keeping size & symmetry
        for _ in range(iters):
            present_pairs = [h for h in range(0, half + 1) if h in V and (n - h) in V and h != n - h]
            absent_pairs = [h for h in range(0, half + 1) if h not in V and h != n - h]
            if not present_pairs or not absent_pairs:
                break
            a = random.choice(present_pairs); d = random.choice(absent_pairs)
            Vs = set(V); Vs.discard(a); Vs.discard(n - a); Vs.add(d); Vs.add(n - d)
            W = tuple(sorted(Vs))
            if len(W) != b:
                continue
            f2, L2, rho2, phi2, lam2 = stat(W)
            if rho2 >= cur[0]:
                V = W; cur = (rho2, W, f2, L2)
        if cur[0] > best[0]:
            best = cur
    return best


def lstsq2(xs, ys):
    """least squares y = a + b*x ; return (a, b, rms)."""
    n = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    det = n * sxx - sx * sx
    b = (n * sxy - sx * sy) / det
    a = (sy - b * sx) / n
    rms = math.sqrt(sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys)) / n)
    return a, b, rms


def main():
    print("=" * 70)
    print("repro: best-rho(b) symmetric census + three-model fit")
    print("=" * 70)
    # exact anchors for small b (from the verifier's exhaustive moderate-diam search)
    seq = {}
    print("\n b   best_rho    fstar  L1     phi     lambda   V", flush=True)
    for b in list(range(6, 15)):
        tries = 150 if b <= 11 else (80 if b <= 13 else 50)
        iters = 300 if b <= 11 else (150 if b <= 13 else 100)
        rho, V, f, L = best_rho_symmetric(b, tries=tries, iters=iters)
        if V is None:
            continue
        _, _, _, phi, lam = stat(V)
        seq[b] = rho
        vs = str(V) if b <= 16 else f"(diam {max(V)}, |V|={len(V)})"
        print(f"{b:3d}  {rho:.6f}   {f:4d} {L:6d}  {phi:.4f}  {lam:.4f}  {vs}")

    # fit the running-max envelope rho_max(b)=max_{b'<=b} rho(b') over b>=9
    # (monotone; = best rate achievable with up to b coordinates; removes the
    # small-b/parity transient from the 6-coordinate minimal trade).
    run = -1.0; env = {}
    for b in sorted(seq):
        run = max(run, seq[b]); env[b] = run
    bs = [b for b in sorted(env) if b >= 9]
    ys = [env[b] for b in bs]
    print(f"\nfitting running-max rho_max(b) over b in {bs}")
    print("  rho_max:", [f"{y:.4f}" for y in ys])
    # M1: rho = R - C/b  -> y = R + (-C)*(1/b)
    a1, s1, r1 = lstsq2([1.0 / b for b in bs], ys); R1, C1 = a1, -s1
    # M2: rho = log2 - C*log(b)/b  (one param C = (log2 - y)*b/log b, least squares slope through this)
    xs2 = [log(b) / b for b in bs]
    # y = log2 - C*x  -> (log2 - y) = C*x ; C = sum(x*(log2-y))/sum(x^2)
    num = sum(x * (LOG2 - y) for x, y in zip(xs2, ys)); den = sum(x * x for x in xs2)
    C2 = num / den
    r2 = math.sqrt(sum((y - (LOG2 - C2 * x)) ** 2 for x, y in zip(xs2, ys)) / len(ys))
    # M3: rho = R - C*log(b)/b -> y = R + (-C)*x
    a3, s3, r3 = lstsq2(xs2, ys); R3, C3 = a3, -s3

    print(f"\n(M1) cap        rho = R - C/b          : R = {R1:.4f}  C = {C1:.3f}   RMS = {r1:.5f}")
    print(f"(M2) climb->log2 rho = log2 - C*log(b)/b : C = {C2:.3f}              RMS = {r2:.5f}")
    print(f"(M3) cap+poly   rho = R - C*log(b)/b     : R = {R3:.4f}  C = {C3:.3f}   RMS = {r3:.5f}")
    print(f"\nlog2 = {LOG2:.4f}. M1/M3 asymptote R vs log2, and M2 RMS vs M1/M3 RMS, decide cap-vs-climb.")
    best_model = min([("M1-cap", r1), ("M2-climb", r2), ("M3-cap+poly", r3)], key=lambda t: t[1])
    print(f"lowest-RMS model: {best_model[0]} (RMS {best_model[1]:.5f})")
    verdict = "CAP (R well below log2)" if max(R1, R3) < 0.5 else "inconclusive/climb"
    print(f"VERDICT: asymptote max(R1,R3) = {max(R1,R3):.4f}  ->  {verdict}")

    # structured non-interval families
    print("\n" + "=" * 70)
    print("structured non-interval families (best rho over parameter grid)")
    print("=" * 70)
    # (block sizes capped at 14 to keep the DP cheap)
    CAP = 14
    bestfam = defaultdict(float)
    # two-scale union A + M*B
    for M in (5, 7, 11, 20, 50):
        for a in range(2, 5):
            for bb in range(2, 5):
                V = tuple(sorted(set(x + M * y for x in range(a) for y in range(bb))))
                if not (4 <= len(V) <= CAP):
                    continue
                _, _, rho, _, _ = stat(V)
                bestfam[("two-scale", len(V))] = max(bestfam[("two-scale", len(V))], rho)
    # GAP {i + j*M}
    for M in (5, 7, 11, 20):
        for p in range(2, 5):
            for q in range(2, 5):
                V = tuple(sorted(i + j * M for i in range(p) for j in range(q)))
                if len(set(V)) != p * q or not (4 <= len(V) <= CAP):
                    continue
                _, _, rho, _, _ = stat(V)
                bestfam[("GAP", len(V))] = max(bestfam[("GAP", len(V))], rho)
    # geometric floor(r^i)
    for r in (1.3, 1.5, 1.7, 2.0):
        for b in range(6, CAP + 1):
            V = sorted(set(int(r ** i) for i in range(b)))
            if not (5 <= len(V) <= CAP):
                continue
            _, _, rho, _, _ = stat(tuple(V))
            bestfam[("geometric", len(V))] = max(bestfam[("geometric", len(V))], rho)
    for key in sorted(bestfam):
        print(f"  {key[0]:12s} b={key[1]:3d}:  best rho = {bestfam[key]:.5f}")
    fam_max = max(bestfam.values()) if bestfam else 0.0
    print(f"\nbest structured-family rho = {fam_max:.5f}  (champion interval-with-holes = 0.156659)")

    # internal consistency: champion recompute
    champ = tuple(sorted(set(range(23)) - {1, 6, 7, 10, 11, 12, 15, 16, 21}))
    _, _, rc, _, _ = stat(champ)
    ok = abs(rc - 0.156659) < 1e-5
    print(f"\nchampion recompute rho = {rc:.6f}  [{'ok' if ok else 'FAIL'}]")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
