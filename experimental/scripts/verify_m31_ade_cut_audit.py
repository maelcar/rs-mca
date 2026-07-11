#!/usr/bin/env python3
"""Independent audit recomputation for DannyExperiments' PR #637 M31 ADE cut.

This script is a FRESH, from-the-mathematical-definitions reimplementation used
to audit

    experimental/notes/thresholds/cap25_v13_m31_k2_common_height_ade_cut.md
    experimental/data/cap25_v13_m31_k2_common_height_ade_cut.json
    experimental/scripts/verify_m31_k2_common_height_ade_cut.py   (author's)

It does NOT import any of the author's verifier modules. Every predicate below
is transcribed independently from the two source notes:

  * the base grid bounds and the rank-inertia / centroid cut come from
    cap25_v13_m31_rank_inertia_anchor_cut.md, eqs (1)-(4) and Section 4;
  * the classifier (kappa=2, t>=t0) and the ADE boundary arithmetic come from
    cap25_v13_m31_k2_common_height_ade_cut.md, eqs (1),(2),(7),(8),(10),(11).

The 3,254,885-row grid is never materialised; both large residual layers are
hashed by streaming the grid in generation order (which is exactly sorted
order, asserted row-by-row) so that peak memory stays well under 2 GB.

Every number this audit REPORTS is recomputed here; the run then re-parses the
author's JSON certificate and the base-layer hash pinned by the predecessor
note and asserts byte-identical agreement. Nonzero exit on any failure.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

# --------------------------------------------------------------------------
# Deployed M31 constants (both source notes, Section 1).
# --------------------------------------------------------------------------
P = 2**31 - 1                 # = 2147483647
N = 2**21                     # = 2097152
M = 981_129
W = 67_447
BSTAR = 2**24 - 1
L = BSTAR + 1                 # = 2**24 = 8N = 16777216
R = M * (N - M)               # = 1094962529967
D0 = N - W                    # = 2029705
T0 = 277_868                  # classifier activation threshold t0
Q = 7 * N                     # q = 7n, used by the anchor threshold

# The four rows excluded by PR #628 (star-determinant rank gap), (kappa,t,e1,e2).
PR628_ROWS = {
    (2, 391_732, 391_732, 783_464),
    (2, 391_733, 391_733, 783_466),
    (2, 391_734, 391_734, 783_468),
    (2, 391_735, 391_735, 783_470),
}

# Hash pinned by the predecessor note for the integrated (RI|centroid) union;
# we reproduce it independently to confirm the base layer #637 differences off.
BASE_INTEGRATED_HASH_PIN = (
    "49576339b6755e90f6f1997b294bad5d178aa9bc5c25c44aab345d9ccefd99da"
)

PASS = 0


def check(label, cond):
    global PASS
    if not cond:
        print(f"FAIL: {label}")
        sys.exit(1)
    PASS += 1


# --------------------------------------------------------------------------
# Small exact helpers.
# --------------------------------------------------------------------------
def ceil_div(a, b):
    return -((-a) // b)


def canonical_hash(rows):
    """Author's canonical encoding: sorted rows, 'k,t,e1,e2' joined by ';'."""
    payload = ";".join(",".join(map(str, row)) for row in sorted(rows))
    return sha256(payload.encode("ascii")).hexdigest()


# --------------------------------------------------------------------------
# Anchor threshold H_kappa  (rank_inertia note, eqs P_kappa, T_kappa, (2)).
#   P_kappa(x) = x^2 + (14L-8(n-1))x + 7L^2(8n-1),  L=kappa-1
#   T_kappa(x) = (n-1)^2(q L^3 + x^3) - (q L + x)^3
#   h2 = least x in [0, vertex] with P<=0 ; vertex = 4(n-1)-7L
#   h3 = least x >= ceil(qL/(n-2)) with T>=0
#   H  = max(h2, h3)
# --------------------------------------------------------------------------
def p_poly(kappa, x):
    lam = kappa - 1
    return x * x + (14 * lam - 8 * (N - 1)) * x + 7 * lam * lam * (8 * N - 1)


def t_poly(kappa, x):
    lam = kappa - 1
    return (N - 1) ** 2 * (Q * lam**3 + x**3) - (Q * lam + x) ** 3


def least_true(lo, hi, pred):
    # smallest v in [lo, hi] with pred(v); pred must be an up-set on [lo,hi].
    assert lo <= hi and pred(hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if pred(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def anchor_H(kappa):
    lam = kappa - 1
    vertex = 4 * (N - 1) - 7 * lam
    h2 = least_true(0, vertex, lambda x: p_poly(kappa, x) <= 0)
    lo3 = ceil_div(Q * lam, N - 2)
    h3 = least_true(lo3, L - 1, lambda x: t_poly(kappa, x) >= 0)
    return max(h2, h3)


# --------------------------------------------------------------------------
# Integrated exclusion predicates (rank_inertia note).
#   Z = (H(kappa+1)+L)R - H n kappa^2 t
#   RI: (H<=n: Z<0) | (n<H, dL<=n: dL^2 R > nZ)
#       | (n<H, dL>n: 2nZ < -bR and nZ^2+bZR+cR^2 > 0),  d=H-n
#       b = 2dL - H(n-1),  c = dL^2(H-1)
# --------------------------------------------------------------------------
def rank_inertia_cut(kappa, t, H):
    lam = kappa - 1
    Z = (H * (kappa + 1) + lam) * R - H * N * kappa * kappa * t
    if H <= N:
        return Z < 0
    d = H - N
    if d * lam <= N:
        return d * lam * lam * R > N * Z
    b = 2 * d * lam - H * (N - 1)
    c = d * lam * lam * (H - 1)
    return (2 * N * Z < -b * R) and (N * Z * Z + b * Z * R + c * R * R > 0)


def centroid_cut(kappa, t):
    # U = LR/(nt) - L*lam + lam = (LR - lam(L-1)nt)/(nt);  un=numer, ud=nt.
    # cut : U left of vertex of P_kappa  AND  P_kappa(U) > 0  (=> left of lower root)
    lam = kappa - 1
    un = L * R - lam * (L - 1) * N * t
    ud = N * t
    return (2 * un < (8 * (N - 1) - 14 * lam) * ud) and (
        un * un
        + (14 * lam - 8 * (N - 1)) * un * ud
        + 7 * lam * lam * (8 * N - 1) * ud * ud
        > 0
    )


# --------------------------------------------------------------------------
# Base grid: (rank_inertia note eq (1))
#   e1=(kappa-1)t, e2=kappa t; 2<=kappa<=774;
#   ceil((W+1)/(kappa-1)) <= t <= min(M//kappa, R//(N(kappa-1)))
# Generated kappa-ascending then t-ascending == globally sorted tuple order.
# --------------------------------------------------------------------------
def grid_rows(anchor):
    for kappa in range(2, 775):
        low = ceil_div(W + 1, kappa - 1)
        high = min(M // kappa, R // (N * (kappa - 1)))
        for t in range(low, high + 1):
            yield kappa, t, (kappa - 1) * t, kappa * t


# --------------------------------------------------------------------------
# ADE boundary arithmetic (k2 note, eqs (7),(8),(10),(11)).
#   rho(t) = Nt/(2Nt-R)
#   rank_floor(t) = ceil( L/rho - 64 + 4 rho )   [from |S|<=rho r+4rho(16-rho)]
# --------------------------------------------------------------------------
def rho(t):
    return Fraction(N * t, 2 * N * t - R)


def rank_floor(t):
    v = Fraction(L, 1) / rho(t) - 64 + 4 * rho(t)
    return -(-v.numerator // v.denominator)  # ceil


def stream_residual_hash(union_set, anchor):
    """SHA-256 of (grid - union_set) in canonical order, O(1) extra memory.

    Relies on grid_rows() emitting strictly increasing tuples; asserted here."""
    h = sha256()
    first = True
    prev = None
    count = 0
    for row in grid_rows(anchor):
        if prev is not None and not (row > prev):
            print("FAIL: grid generation not strictly sorted; streaming hash invalid")
            sys.exit(1)
        prev = row
        if row in union_set:
            continue
        chunk = ("" if first else ";") + ",".join(map(str, row))
        h.update(chunk.encode("ascii"))
        first = False
        count += 1
    return h.hexdigest(), count


def main():
    root = Path(__file__).resolve().parents[1]

    # -- Pass 1: anchor thresholds, integrated set, classifier set, grid count.
    anchor = {kappa: anchor_H(kappa) for kappa in range(2, 775)}
    # Independent reproduction of the published H values (rank_inertia note).
    check("H(2)=890", anchor[2] == 890)
    check("H(3)=1780", anchor[3] == 1_780)
    check("H(128)=113686", anchor[128] == 113_686)
    check("H(400)=1200745", anchor[400] == 1_200_745)
    check("H(600)=3077757", anchor[600] == 3_077_757)
    check("H(774)=8060986", anchor[774] == 8_060_986)

    grid_count = 0
    integrated = set()
    classifier = set()
    ri_count = 0
    centroid_count = 0
    integrated_k2_min = None
    integrated_k2_max = None
    for kappa, t, e1, e2 in grid_rows(anchor):
        grid_count += 1
        row = (kappa, t, e1, e2)
        ri = rank_inertia_cut(kappa, t, anchor[kappa])
        ce = centroid_cut(kappa, t)
        if ri:
            ri_count += 1
        if ce:
            centroid_count += 1
        if ri or ce:
            integrated.add(row)
            if kappa == 2:
                integrated_k2_min = t if integrated_k2_min is None else min(integrated_k2_min, t)
                integrated_k2_max = t if integrated_k2_max is None else max(integrated_k2_max, t)
        if kappa == 2 and t >= T0:
            classifier.add(row)

    check("grid count == 3,254,885", grid_count == 3_254_885)
    check("RI rows == 153,483", ri_count == 153_483)
    check("centroid rows == 187", centroid_count == 187)
    check("integrated union == 153,605", len(integrated) == 153_605)
    check("integrated hash reproduces predecessor pin",
          canonical_hash(integrated) == BASE_INTEGRATED_HASH_PIN)
    # Independent reproduction of the integrated kappa=2 interval [391736,490564].
    check("integrated kappa=2 interval == [391736, 490564]",
          (integrated_k2_min, integrated_k2_max) == (391_736, 490_564))
    integrated_k2 = {r for r in integrated if r[0] == 2}
    check("integrated kappa=2 count == 98,829 and contiguous",
          len(integrated_k2) == 98_829 == (490_564 - 391_736 + 1))

    # -- Base grid presence + disjointness of the three exclusion layers (R4).
    check("PR628 rows are genuine grid rows", all(
        (2 <= r[0] <= 774) and r[2] == (r[0] - 1) * r[1] and r[3] == r[0] * r[1]
        for r in PR628_ROWS))
    check("PR628 disjoint from integrated (no double count)",
          not (PR628_ROWS & integrated))

    # -- Classifier: independent structural facts (k2 note Section 1).
    check("classifier count == 212,697", len(classifier) == 212_697)
    check("classifier min == (2,277868,277868,555736)",
          min(classifier) == (2, 277_868, 277_868, 555_736))
    check("classifier max == (2,490564,490564,981128)",
          max(classifier) == (2, 490_564, 490_564, 981_128))
    check("classifier is exactly {(2,t,t,2t): 277868<=t<=490564}",
          classifier == {(2, t, t, 2 * t) for t in range(T0, 490_565)})
    check("classifier total == interval length", len(classifier) == 490_564 - T0 + 1)

    # -- Overlaps (R4 double-count audit).
    overlap_int = classifier & integrated
    check("classifier & integrated == 98,829", len(overlap_int) == 98_829)
    check("classifier & integrated == integrated's kappa=2 rows",
          overlap_int == integrated_k2)
    check("classifier contains all 4 PR628 rows",
          classifier & PR628_ROWS == PR628_ROWS)

    # -- Ledger set algebra (k2 note Section 6).
    old_union = integrated | PR628_ROWS
    new_exclusions = classifier - old_union
    new_union = old_union | classifier
    check("old_union count == 153,609", len(old_union) == 153_609)
    check("new_exclusions count == 113,864", len(new_exclusions) == 113_864)
    check("new_union count == 267,473", len(new_union) == 267_473)
    check("new residual == 2,987,412 (grid - new_union)",
          grid_count - len(new_union) == 2_987_412)
    check("old residual == 3,101,276 (grid - old_union)",
          grid_count - len(old_union) == 3_101_276)

    # The three layers form a DISJOINT partition of new_union (no double count).
    check("layers disjoint: integrated | PR628 | new_exclusions partition new_union",
          len(integrated) + len(PR628_ROWS) + len(new_exclusions) == len(new_union)
          and not (integrated & PR628_ROWS)
          and not (integrated & new_exclusions)
          and not (PR628_ROWS & new_exclusions))
    # new_exclusions is exactly the contiguous t-band [277868, 391731].
    check("new_exclusions == {(2,t,t,2t): 277868<=t<=391731}",
          new_exclusions == {(2, t, t, 2 * t) for t in range(T0, 391_732)})
    check("new_exclusions min == (2,277868,277868,555736)",
          min(new_exclusions) == (2, 277_868, 277_868, 555_736))
    check("new_exclusions max == (2,391731,391731,783462)",
          max(new_exclusions) == (2, 391_731, 391_731, 783_462))

    # -- Canonical hashes recomputed from MY rows (small sets).
    classifier_hash = canonical_hash(classifier)
    new_excl_hash = canonical_hash(new_exclusions)
    new_union_hash = canonical_hash(new_union)
    old_union_hash = canonical_hash(old_union)

    # -- Streaming residual hashes (large layers, O(1) memory).
    new_residual_hash, new_residual_count = stream_residual_hash(new_union, anchor)
    old_residual_hash, old_residual_count = stream_residual_hash(old_union, anchor)
    check("streamed new residual count == 2,987,412", new_residual_count == 2_987_412)
    check("streamed old residual count == 3,101,276", old_residual_count == 3_101_276)

    # -- Theorem exact-arithmetic core (k2 note Sections 1,3,5,7).
    check("R = m(N-m)", R == M * (N - M) == 1_094_962_529_967)
    check("D0 = N - W = 2,029,705", D0 == 2_029_705)
    check("PSD at t0: 2*N*t0 - R > 0", 2 * N * T0 - R > 0)
    check("h^2 = 2 - R/(N t0) > 0", Fraction(2) - Fraction(R, N * T0) > 0)
    boundary_rho = rho(T0)
    prev_rho = rho(T0 - 1)
    check("rho(t0) == 582731431936/70500333905",
          boundary_rho == Fraction(582_731_431_936, 70_500_333_905))
    check("rho(t0-1) == 582729334784/70496139601",
          prev_rho == Fraction(582_729_334_784, 70_496_139_601))
    check("8 < rho(t0) < 17/2 (Lemma hypothesis)",
          Fraction(8) < boundary_rho < Fraction(17, 2))
    check("rank_floor(t0) == 2,029,720 == D0+15", rank_floor(T0) == 2_029_720 == D0 + 15)
    check("rank_floor(t0-1) == 2,029,606 == D0-99", rank_floor(T0 - 1) == 2_029_606 == D0 - 99)
    check("first route failure row == (2,277867,277867,555734)",
          (2, T0 - 1, T0 - 1, 2 * (T0 - 1)) == (2, 277_867, 277_867, 555_734))
    # Determinant contradiction: p^(r-d0) | det(B), det(B) positive integer, so
    # det(B) >= p^15; but det(B) <= (N+1)^16.  Need p^gap > (N+1)^16.
    gap = rank_floor(T0) - D0
    check("gap == 15", gap == 15)
    check("p^gap divisibility floor beats determinant ceiling: p^15 > (N+1)^16",
          P**gap > (N + 1) ** 16)
    check("note's stated bracket: p^15 > 2^450 > 2^352 > (N+1)^16",
          P**15 > 2**450 and 2**450 > 2**352 and 2**352 > (N + 1) ** 16)
    # minimal gap that would still yield a contradiction (robustness margin)
    min_gap = next(g for g in range(1, 40) if P**g > (N + 1) ** 16)
    check("minimal contradiction gap == 11 (delivered 15, margin 4)", min_gap == 11)
    # c<=16 orthogonal-component Bessel bound uses rho0<17/2
    check("component count bound c<=16 from Bessel (2*rho0<17)",
          2 * boundary_rho < 17)

    # -- Re-parse the author's JSON certificate and assert full agreement.
    cert = json.loads(
        (root / "data" / "cap25_v13_m31_k2_common_height_ade_cut.json").read_text(
            encoding="utf-8"))
    c_const = cert["constants"]
    check("cert constants match", c_const == {
        "p": P, "N": N, "m": M, "w": W, "d0": D0, "L": L, "R": R, "t0": T0})
    sl = cert["source_ledger"]
    check("cert grid_count", sl["grid_count"] == grid_count)
    check("cert base_integrated_count", sl["base_integrated_count"] == len(integrated))
    check("cert base_integrated_sha256", sl["base_integrated_sha256"] == canonical_hash(integrated))
    check("cert old_union_count", sl["old_union_count"] == len(old_union))
    check("cert old_union_sha256", sl["old_union_sha256"] == old_union_hash)
    check("cert old_residual_count", sl["old_residual_count"] == old_residual_count)
    check("cert old_residual_sha256", sl["old_residual_sha256"] == old_residual_hash)
    cc = cert["classifier"]
    check("cert classifier count", cc["count"] == len(classifier))
    check("cert classifier sha256", cc["sha256"] == classifier_hash)
    check("cert integrated_overlap_count", cc["integrated_overlap_count"] == len(overlap_int))
    check("cert pr628_overlap_count", cc["pr628_overlap_count"] == 4)
    check("cert new_exclusions_count", cc["new_exclusions_count"] == len(new_exclusions))
    check("cert new_exclusions_sha256", cc["new_exclusions_sha256"] == new_excl_hash)
    nl = cert["new_ledger"]
    check("cert new_union_count", nl["union_count"] == len(new_union))
    check("cert new_union_sha256", nl["union_sha256"] == new_union_hash)
    check("cert new_residual_count", nl["residual_count"] == new_residual_count)
    check("cert new_residual_sha256", nl["residual_sha256"] == new_residual_hash)
    bnd = cert["boundary"]
    check("cert rho numerator", bnd["rho_numerator"] == boundary_rho.numerator)
    check("cert rho denominator", bnd["rho_denominator"] == boundary_rho.denominator)
    check("cert rank_floor", bnd["rank_floor"] == rank_floor(T0))
    check("cert rank_gap", bnd["rank_gap"] == gap)
    check("cert previous_rank_floor", bnd["previous_rank_floor"] == rank_floor(T0 - 1))

    print("RESULT: PASS")
    print(f"checks_passed={PASS}")
    print(f"grid={grid_count}")
    print(f"integrated={len(integrated)} (RI={ri_count} centroid={centroid_count})")
    print(f"integrated_hash={canonical_hash(integrated)}")
    print(f"old_union={len(old_union)} old_residual={old_residual_count}")
    print(f"classifier={len(classifier)} overlap_integrated={len(overlap_int)} overlap_pr628=4")
    print(f"new_exclusions={len(new_exclusions)} band=(2,t,t,2t) t in [277868,391731]")
    print(f"new_union={len(new_union)} new_residual={new_residual_count}")
    print(f"classifier_sha256={classifier_hash}")
    print(f"new_exclusions_sha256={new_excl_hash}")
    print(f"new_union_sha256={new_union_hash}")
    print(f"new_residual_sha256={new_residual_hash}")
    print(f"old_union_sha256={old_union_hash}")
    print(f"old_residual_sha256={old_residual_hash}")
    print(f"rho(t0)={boundary_rho} approx {float(boundary_rho):.6f}")
    print(f"rank_floor(t0)={rank_floor(T0)}=d0+{gap}  prefix_cap=d0={D0}")
    print(f"minimal_contradiction_gap=11 delivered_gap={gap} margin={gap-11}")
    print("certificate=PASS")


if __name__ == "__main__":
    main()
