#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/frame_image_completion.md.

Decides the J2 interface gap (audit PR #608) for the character-frame certificate
(avdeev, PR #558): can the frame's magnitude-side hypotheses (CF1)+(CF2) deliver
the image half  L >= e^{-o(N)} A_eff  that def:effective-fourier-payment (EFP)
bundles and thm:primitive-q consumes?

Verdict recomputed here:
  R1 (magnitude derivation)  : CIRCULAR.  The pigeonhole from (CF1) yields only
                               L >= |A|/||K_A||_op, and (CF2) supplies only the
                               image-normalized packing |A| >= e^{-o}L, giving
                               the tautology L >= e^{-o}L.  No choice of A lets
                               |A|/||K_A|| exceed L, so the pigeonhole can never
                               reach A_eff.  (CF3) blocks the span-normalized
                               escape: the full dual pays ||K||=|G| max mu.
  R2 (impossibility witness) : avdeev's OWN block-parabola family satisfies
                               (CF1)+(CF2) EXACTLY (K_{A_k}=I, |A_k|=p^k=L) yet
                               L/A_eff = p^{-k} = e^{-Theta(N)}.  So (CF1)+(CF2)
                               do NOT imply the image bound.

Every number in the note is recomputed below.  Stdlib only (cmath/math/
itertools).  Run:
    ulimit -v 2097152
    python3 experimental/scripts/verify_frame_image_completion.py
Exit 0 iff ALL checks pass.

Credit: block-parabola construction and the CF1/CF2/CF3 identities are avdeev's
(PR #558, asymptotic_primitive_profile_character_frame_v1.md).  The J2 gap is
our audit PR #608.  #539's Gap-1 corollary (EF4 => image >= A_eff/kappa) is the
span-normalized pigeonhole this note contrasts against.
"""

import cmath
import math
import itertools
import sys

TOL = 1e-11
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  |  {detail}" if detail else ""))
    return ok


# ---------------------------------------------------------------------------
# One-block normalized parabola Fourier coefficient
#   phi(a,b) = (1/p) sum_{t in F_p} e_p(a t + b t^2)
# Gauss-sum identities (avdeev #558, note L282-307):
#   phi(0,0)=1 ; phi(a,0)=0 for a!=0 ; |phi(a,b)|=p^{-1/2} for b!=0.
# ---------------------------------------------------------------------------
def phi(a, b, p):
    w = cmath.exp(2j * math.pi / p)
    return sum(w ** ((a * t + b * t * t) % p) for t in range(p)) / p


def hat_mu_block(gamma, p):
    """hat_mu at gamma=((a_1,b_1),...,(a_k,b_k)) for the k-block parabola,
    by the product factorization (note L309-313)."""
    val = 1.0 + 0j
    for (a, b) in gamma:
        val *= phi(a, b, p)
    return val


def image_points(p, k):
    """S = {((t_1,t_1^2),...,(t_k,t_k^2)) : t_i in F_p}."""
    one = [(t, (t * t) % p) for t in range(p)]
    return list(itertools.product(one, repeat=k))


def fp_rank(vectors, p):
    """Rank over F_p of a list of row vectors (tuples of ints)."""
    rows = [list(v) for v in vectors]
    ncol = len(rows[0]) if rows else 0
    r = 0
    for c in range(ncol):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] % p != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [(x * inv) % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p != 0:
                f = rows[i][c] % p
                rows[i] = [(rows[i][j] - f * rows[r][j]) % p for j in range(ncol)]
        r += 1
        if r == len(rows):
            break
    return r


def op_norm_herm_psd(K, iters=2000):
    """Top eigenvalue (= operator norm) of a small Hermitian PSD matrix K
    via power iteration.  K is a list of lists of complex."""
    n = len(K)
    v = [1.0 + 0j] * n
    lam = 0.0
    for _ in range(iters):
        w = [sum(K[i][j] * v[j] for j in range(n)) for i in range(n)]
        nrm = math.sqrt(sum((x * x.conjugate()).real for x in w))
        if nrm < 1e-300:
            return 0.0
        v = [x / nrm for x in w]
        lam = nrm
    return lam


def gram(A, p):
    """Gram K_A(g,g') = hat_mu(g' - g) for characters g,g' in A (list of
    k-tuples of (a,b) pairs).  Difference is componentwise mod p."""
    def diff(g2, g1):
        return tuple(((a2 - a1) % p, (b2 - b1) % p)
                     for (a1, b1), (a2, b2) in zip(g1, g2))
    n = len(A)
    return [[hat_mu_block(diff(A[j], A[i]), p) for j in range(n)] for i in range(n)]


def max_offdiag(K):
    n = len(K)
    return max((abs(K[i][j]) for i in range(n) for j in range(n) if i != j),
               default=0.0)


# ===========================================================================
print("=" * 72)
print("BLOCK 0 : Gauss-sum building blocks (frame note L282-307)")
print("=" * 72)
for p in (3, 5, 7):
    ok00 = abs(phi(0, 0, p) - 1) < TOL
    okA0 = all(abs(phi(a, 0, p)) < TOL for a in range(1, p))
    okAB = all(abs(abs(phi(a, b, p)) - 1 / math.sqrt(p)) < TOL
               for a in range(p) for b in range(1, p))
    check(f"phi(0,0)=1                     p={p}", ok00)
    check(f"phi(a,0)=0 for a!=0            p={p}", okA0,
          "vanishing kills K_A off-diagonals => K_{A_k}=I")
    check(f"|phi(a,b)|=1/sqrt(p) for b!=0  p={p}", okAB,
          "b!=0 band carries the image-span mass the packing A_k dodges")


# ===========================================================================
print("=" * 72)
print("BLOCK 1 : R2 witness -- block-parabola family satisfies CF1+CF2 EXACTLY")
print("          yet L/A_eff = p^{-k} = e^{-Theta(N)}   (avdeev #558's own family)")
print("=" * 72)
# enumerated exact cases
CASES = [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1)]
report_rows = []
for (p, k) in CASES:
    S = image_points(p, k)
    L = len(set(S))
    M = L                       # injective parabola product
    assert L == p ** k
    # effective span V_g = Span_Fp{ s - 0 : s in S }; s already = difference from t=0
    flat = [tuple(x for blk in s for x in blk) for s in S]  # F_p^{2k} vectors
    rank = fp_rank(flat, p)
    A_eff = p ** rank
    # packing A_k = { ((a_1,0),...,(a_k,0)) } , |A_k| = p^k = L
    Ak = list(itertools.product([(a, 0) for a in range(p)], repeat=k))
    K = gram(Ak, p)
    off = max_offdiag(K)
    diag_ok = all(abs(K[i][i] - 1) < TOL for i in range(len(K)))
    normK = 1.0 if off < TOL and diag_ok else op_norm_herm_psd(K)
    Fmax = 1                    # injective => every fiber size 1
    kappa_frame = L * normK / len(Ak)          # frame multiplier (image-normalized)
    kappa_star = A_eff * Fmax / M              # #539 Gap-1 multiplier (span-normalized)
    cf1_rhs = M * normK / len(Ak)              # (CF1) upper bound on max fiber

    check(f"(p,k)=({p},{k})  L=p^k={L}, A_eff=p^(2k)={A_eff}, rank(V_g)={rank}=2k",
          rank == 2 * k and A_eff == p ** (2 * k))
    check(f"(p,k)=({p},{k})  K_{{A_k}} = I  (max offdiag={off:.2e})",
          off < TOL and diag_ok, "=> ||K_{A_k}||_op = 1")
    check(f"(p,k)=({p},{k})  CF1 holds: F_max={Fmax} <= M||K||/|A|={cf1_rhs:.6f}",
          Fmax <= cf1_rhs + TOL)
    check(f"(p,k)=({p},{k})  CF2 holds: |A_k|={len(Ak)}>=L={L} and ||K||={normK:.6f}<=1",
          len(Ak) >= L - TOL and normK <= 1 + TOL, "CF2 satisfied EXACTLY")
    check(f"(p,k)=({p},{k})  J2 FAILS: L/A_eff={L/A_eff:.6g}=p^-k (image collapse)",
          L * A_eff and (L / A_eff) <= 1.0 / p + TOL,
          f"target L>=e^-o A_eff violated by factor A_eff/L={A_eff//L}")
    check(f"(p,k)=({p},{k})  kappa_frame={kappa_frame:.4f}=1 but kappa*(#539)={kappa_star:.1f}=p^k",
          abs(kappa_frame - 1) < TOL and abs(kappa_star - p ** k) < 1e-6,
          f"kappa*/kappa_frame = {kappa_star/kappa_frame:.1f} = A_eff/L")
    report_rows.append((p, k, M, L, A_eff, kappa_frame, kappa_star, L / A_eff))

# closed-form scalable rows (product formula, frame note L309-342): PROVED identity
print("-" * 72)
print("scalable rows (product-formula identities, PROVED): L=p^k A_eff=p^2k kappa*=p^k")
for p in (3, 5):
    for k in (1, 2, 3, 4):
        L, A_eff, ks, kf = p ** k, p ** (2 * k), p ** k, 1
        check(f"closed-form p={p} k={k}: L/A_eff=p^-k={L/A_eff:.3e}, kappa*=p^k={ks}, kf=1",
              A_eff == L * L and ks == L and kf == 1)


# ===========================================================================
print("=" * 72)
print("BLOCK 2 : R1 circularity -- NO character family A makes the pigeonhole")
print("          |A|/||K_A|| exceed L, so it can never certify L >= A_eff.")
print("          (CF3) full-dual identity ||K_{G^}||=|G| max mu blocks the escape.")
print("=" * 72)
for p in (3, 5, 7):
    k = 1
    S = image_points(p, k)
    L = len(set(S)); M = L; A_eff = p * p
    mu_max = 1.0 / p                      # injective p-point image, each mass 1/M=1/p
    Gfull = list(itertools.product([(a, b) for a in range(p) for b in range(p)], repeat=1))
    # candidate families A: singleton, the good packing A_k, the full dual
    singleton = [((0, 0),)]
    Ak = [((a, 0),) for a in range(p)]
    families = {"singleton": singleton, "packing A_k": Ak, "full dual G^": Gfull}
    pig = {}
    for tag, A in families.items():
        K = gram(A, p)
        off = max_offdiag(K)
        nrm = 1.0 if (off < TOL and all(abs(K[i][i] - 1) < TOL for i in range(len(K)))) \
            else op_norm_herm_psd(K)
        pig[tag] = len(A) / nrm
        if tag == "full dual G^":
            # (CF3) exact full-dual identity: ||K_{G^}|| = |G| max mu = p^2 * (1/p) = p
            check(f"p={p}  (CF3) ||K_{{G^}}||={nrm:.6f} = |G|max mu = p={p}",
                  abs(nrm - p) < 1e-4, "span-normalized packing costs ||K||=p (exp per block)")
        check(f"p={p}  pigeonhole via {tag:12s}: |A|/||K_A|| = {pig[tag]:.4f} <= L = {L}",
              pig[tag] <= L + 1e-4)
    best = max(pig.values())
    check(f"p={p}  max_A |A|/||K_A|| = {best:.4f} = L = {L}  (NEVER reaches A_eff={A_eff})",
          abs(best - L) < 1e-4,
          "R1 tautology: pigeonhole recovers L, never A_eff")


# ===========================================================================
print("=" * 72)
print("BLOCK 3 : indistinguishability -- parabola (L=p) and full-G (L=p^2)")
print("          share IDENTICAL frame data K_{A_k}=I on the same packing A_k,")
print("          but Gap-1 fails for one and holds for the other.")
print("=" * 72)
for p in (3, 5):
    Ak = [((a, 0),) for a in range(p)]
    # parabola measure: hat via phi (K_{A_k}=I because phi(a,0)=0, a!=0)
    Kpar = gram(Ak, p)
    off_par = max_offdiag(Kpar)
    # full-G measure: hat_mu_full(gamma)=[gamma=0]; K_{A_k}=I for ANY A
    n = len(Ak)
    Kfull = [[1.0 + 0j if i == j else 0j for j in range(n)] for i in range(n)]
    same = all(abs(Kpar[i][j] - Kfull[i][j]) < TOL for i in range(n) for j in range(n))
    L_par, A_eff = p, p * p
    L_full = p * p
    kstar_par = A_eff * 1 / L_par        # = p  -> Gap-1 FAILS
    kstar_full = A_eff * 1 / L_full      # = 1  -> Gap-1 HOLDS
    check(f"p={p}  same packing A_k gives K=I for BOTH measures (offdiag_par={off_par:.1e})",
          off_par < TOL and same, "frame data identical; L differs p vs p^2")
    check(f"p={p}  Gap-1 kappa*: parabola={kstar_par:.0f} (FAIL) vs full-G={kstar_full:.0f} (HOLD)",
          abs(kstar_par - p) < TOL and abs(kstar_full - 1) < TOL,
          "identical frame data, opposite image verdict => frame is A_eff-blind")


# ===========================================================================
print("=" * 72)
print("SUMMARY TABLE (recomputed)")
print("=" * 72)
print(f"{'p':>3} {'k':>3} {'M':>8} {'L':>8} {'A_eff':>10} "
      f"{'kappa_frame':>12} {'kappa*(#539)':>13} {'L/A_eff':>12}")
for (p, k, M, L, A_eff, kf, ks, ratio) in report_rows:
    print(f"{p:>3} {k:>3} {M:>8} {L:>8} {A_eff:>10} {kf:>12.4f} {ks:>13.1f} {ratio:>12.4e}")


# ===========================================================================
n_fail = sum(1 for _, ok, _ in results if not ok)
n_pass = len(results) - n_fail
print("=" * 72)
print(f"RESULT: {'PASS' if n_fail == 0 else 'FAIL'}  ({n_pass}/{len(results)} checks passed)")
print("=" * 72)
sys.exit(0 if n_fail == 0 else 1)
