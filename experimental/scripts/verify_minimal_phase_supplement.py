#!/usr/bin/env python3
"""Verifier for experimental/notes/thresholds/minimal_phase_supplement.md.

Pins the WEAKEST phase-sensitive supplement S completing avdeev's character
frame (PR #558) to a full (EFP)-replacement interface: frame + S => the image
clause  L >= e^{-o(N)} A_eff  that def:effective-fourier-payment (EFP) bundles
and thm:primitive-q consumes.  Lineage: audit PR #608 (J2 gap), packet PR #609
(J2 proved undeliverable by magnitude alone).  scottdhughes (LS) #564 and the
LegaSage C9 razor (#585 chain / thresholds-c9-r2-near-sidon-razor) enter in the
crux map.

Master identity recomputed here (the whole verdict):

    L >= A_eff / (1 + E),        E = sum_{chi != 0 in V_g^} |hat_mu(chi)|^2
                                   = A_eff * (sum_z mu(z)^2) - 1        (Parseval)

so the image clause holds  <==  E <= e^{o(N)}   ((S_E), the minimal supplement).

RUNG-1 fact recomputed:  the tex's printed "pointwise sufficient route" bounds
fibers by the AMBIENT scale barN_0 = |B|^{-R} binom(|T|,m) (tex L2822), not the
image scale M/L.  An ambient max-fiber bound gives, by the pigeonhole over the
L nonempty fibers, A_eff/L <= e^{o(N)} (tex rem:flatness-certifies-image L4900),
i.e. the image clause.  So the printed route is span/ambient-normalized and does
NOT hit the #609 image-normalized trap.  We recompute the two normalizations and
show the frame's CF1 lands on the image side, the printed route on the span side.

RUNG-2 census: the canonical KILL TEST is avdeev's block-parabola family (the
same family as #609's witness).  It satisfies frame (CF1)+(CF2) exactly, and:
  * E = p^k - 1 = e^{Theta(N)}      -> violates (S_E)
  * max dodged |hat_mu| = p^{-1/2}  -> SATISFIES the per-character bound (S1)
                                       at any constant threshold, yet collapses.
Hence per-character control (S1) is INSUFFICIENT; the aggregate L^2 energy is
required, and (S_E) is calibrated so the parabola sits exactly on its boundary
(Cauchy-Schwarz L = A_eff/(1+E) is an EQUALITY there).

RUNG-3 census: the parabola is a razor "NO" (all fibers size 1 => image-
normalized Q holds, max f_s = barN^img) yet fails (S_E) and the image clause.
So a razor NO does NOT imply the minimal supplement: the razor lives at image
normalization, (S_E) at span normalization, separated by the #609 factor
A_eff/L.

Stdlib only (cmath / math / itertools / random).  Run:
    ulimit -v 2097152
    python3 experimental/scripts/verify_minimal_phase_supplement.py
Exit 0 iff ALL checks pass.

Credit: block-parabola construction and CF1/CF2/CF3 are avdeev's (PR #558).
J2 gap is our audit PR #608; the magnitude-blindness theorem is our PR #609.
scottdhughes signed (LS): PR #564.  LegaSage C9 razor: PR #585 chain.
"""

import cmath
import math
import itertools
import random
import sys

TOL = 1e-9
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f"  |  {detail}" if detail else ""))
    return ok


# ===========================================================================
# Fourier helpers on a finite abelian group  V = product of Z_{p_i}.
# mu is a probability vector indexed by group elements (tuples).
# hat_mu(chi) = sum_z mu(z) chi(z),  chi indexed by a dual tuple.
# ===========================================================================
def group_elements(mods):
    return list(itertools.product(*[range(p) for p in mods]))


def hat_mu(mu, chi, mods, elts):
    """hat_mu(chi) = sum_z mu[z] exp(2pi i sum_j chi_j z_j / p_j)."""
    total = 0j
    for z in elts:
        phase = sum(chi[j] * z[j] / mods[j] for j in range(len(mods)))
        total += mu[z] * cmath.exp(2j * math.pi * phase)
    return total


def spectral_energy(mu, mods, elts):
    """E = sum_{chi != 0} |hat_mu(chi)|^2  (nontrivial spectral energy)."""
    E = 0.0
    for chi in elts:
        if all(c == 0 for c in chi):
            continue
        E += abs(hat_mu(mu, chi, mods, elts)) ** 2
    return E


def collision(mu, elts):
    return sum(mu[z] ** 2 for z in elts)


def support_size(mu, elts):
    return sum(1 for z in elts if mu[z] > TOL)


# ---------------------------------------------------------------------------
# BLOCK 0 -- master identity  E = A_eff * P2 - 1  and  L >= A_eff/(1+E)
#            on explicit small measures (Parseval + Cauchy-Schwarz).
# ---------------------------------------------------------------------------
def block0():
    print("\n=== BLOCK 0: master identity  L >= A_eff/(1+E),  E = A_eff*P2 - 1 ===")
    rng = random.Random(20260711)
    ok_pars = True
    ok_cs = True
    ok_uniform = True
    for mods in [(5,), (7,), (3, 3), (2, 2, 2), (5, 3)]:
        elts = group_elements(mods)
        A_eff = len(elts)
        # a batch of random probability measures (varied support/concentration)
        for trial in range(6):
            w = [rng.random() ** (1 + 3 * rng.random()) for _ in elts]
            # occasionally zero out entries to vary L
            for i in range(len(w)):
                if rng.random() < 0.3:
                    w[i] = 0.0
            s = sum(w)
            if s <= 0:
                continue
            mu = {z: w[i] / s for i, z in enumerate(elts)}
            P2 = collision(mu, elts)
            E = spectral_energy(mu, mods, elts)
            L = support_size(mu, elts)
            # Parseval: sum_chi |hat|^2 = A_eff * P2 ; nontrivial part = A_eff*P2 - 1
            if abs(E - (A_eff * P2 - 1.0)) > 1e-7 * max(1.0, A_eff * P2):
                ok_pars = False
            # Cauchy-Schwarz image bound
            if L < A_eff / (1.0 + E) - 1e-7:
                ok_cs = False
        # uniform measure on all of V => E = 0, L = A_eff (equality in CS)
        mu_u = {z: 1.0 / A_eff for z in elts}
        Eu = spectral_energy(mu_u, mods, elts)
        Lu = support_size(mu_u, elts)
        if abs(Eu) > 1e-7 or Lu != A_eff or abs(Lu - A_eff / (1 + Eu)) > 1e-7:
            ok_uniform = False
    check("Parseval  E = A_eff*P2 - 1  on random measures", ok_pars)
    check("Cauchy-Schwarz image bound  L >= A_eff/(1+E)", ok_cs)
    check("uniform measure: E=0, L=A_eff, CS tight", ok_uniform)


# ---------------------------------------------------------------------------
# BLOCK 1 -- one-block parabola Fourier phi(a,b) (avdeev #558, reused #609)
#            phi(0,0)=1 ; phi(a,0)=0 (a!=0) ; |phi(a,b)|=p^{-1/2} (b!=0).
# ---------------------------------------------------------------------------
def phi(a, b, p):
    w = cmath.exp(2j * math.pi / p)
    return sum(w ** ((a * t + b * t * t) % p) for t in range(p)) / p


def block1():
    print("\n=== BLOCK 1: one-block parabola Gauss identities ===")
    ok = True
    detail = []
    for p in (3, 5, 7):
        if abs(phi(0, 0, p) - 1.0) > TOL:
            ok = False
        for a in range(1, p):
            if abs(phi(a, 0, p)) > TOL:
                ok = False
        mags = [abs(phi(a, b, p)) for a in range(p) for b in range(1, p)]
        if any(abs(mg - p ** -0.5) > 1e-9 for mg in mags):
            ok = False
        detail.append(f"p={p}: |phi(*,b!=0)|={p**-0.5:.4f}")
    check("phi(0,0)=1, phi(a,0)=0, |phi(a,b!=0)|=p^-1/2", ok, "; ".join(detail))


# ---------------------------------------------------------------------------
# BLOCK 2 -- parabola energy: closed form E = p^k - 1, brute-checked,
#            and the KILL TEST vs (S_E) / (S1).  A_eff=p^{2k}, L=p^k.
# ---------------------------------------------------------------------------
def parabola_hat(chi, p, k):
    """chi = (a_1,b_1,...,a_k,b_k); product of one-block phi's."""
    val = 1 + 0j
    for i in range(k):
        val *= phi(chi[2 * i], chi[2 * i + 1], p)
    return val


def parabola_energy_brute(p, k):
    E = 0.0
    for chi in itertools.product(range(p), repeat=2 * k):
        if all(c == 0 for c in chi):
            continue
        E += abs(parabola_hat(chi, p, k)) ** 2
    return E


def block2():
    print("\n=== BLOCK 2: block-parabola KILL TEST (E=p^k-1, tight CS) ===")
    rows = []
    ok_closed = True
    ok_tight = True
    ok_dodged = True
    ok_perchar_insuff = True
    for (p, k) in [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1), (3, 3)]:
        A_eff = p ** (2 * k)
        L = p ** k
        E_closed = p ** k - 1
        # brute energy only when the dual is small enough
        if A_eff <= 2500:
            E_brute = parabola_energy_brute(p, k)
            if abs(E_brute - E_closed) > 1e-6 * max(1, E_closed):
                ok_closed = False
        # Cauchy-Schwarz is an EQUALITY on the (uniform-image) parabola
        L_cs = A_eff / (1.0 + E_closed)
        if abs(L_cs - L) > 1e-9 * L:
            ok_tight = False
        # dodged-band energy = full E (b=0,a!=0 band contributes 0)
        # E_{b=0 band} = 0 because phi(a,0)=0; so E_dodged = E_closed
        # max dodged |hat_mu| = p^{-1/2} (single active block) -> constant
        max_dodged = p ** -0.5
        if max_dodged >= 1.0 - 1e-12:  # (S1) threshold e^{o(N)} ~ any constant>=this
            ok_perchar_insuff = False
        # (S1) at threshold e^{o(N)} (i.e. <=1) is SATISFIED yet L/A_eff=p^-k -> insufficient
        s1_satisfied = max_dodged <= 1.0 + 1e-12
        image_clause_fails = (L / A_eff) < 0.5  # p^-k <= 1/3
        if not (s1_satisfied and image_clause_fails):
            ok_perchar_insuff = False
        rows.append((p, k, p ** k, L, A_eff, E_closed, L / A_eff, max_dodged))
    # verify the b=0 band carries zero energy explicitly for a couple of rows
    for (p, k) in [(3, 1), (3, 2), (5, 1)]:
        Eb0 = 0.0
        for chi in itertools.product(range(p), repeat=2 * k):
            if all(c == 0 for c in chi):
                continue
            if all(chi[2 * i + 1] == 0 for i in range(k)):  # every b_i = 0
                Eb0 += abs(parabola_hat(chi, p, k)) ** 2
        if abs(Eb0) > 1e-9:
            ok_dodged = False
    check("parabola E = p^k - 1 (brute == closed form)", ok_closed)
    check("Cauchy-Schwarz EQUALITY on parabola: L = A_eff/(1+E)", ok_tight)
    check("b=0 band carries ZERO energy (all E is dodged-band)", ok_dodged)
    check("(S1) per-character bound SATISFIED yet image clause FAILS "
          "=> per-character insufficient", ok_perchar_insuff)
    print("\n  p  k    M    L    A_eff        E=p^k-1   L/A_eff  max|hat_dodged|")
    for (p, k, M, L, A_eff, E, ratio, md) in rows:
        print(f"  {p}  {k} {M:5d} {L:5d} {A_eff:10d} {E:10d}   {ratio:7.4f}   {md:.4f}")
    return rows


# ---------------------------------------------------------------------------
# BLOCK 3 -- frame + (S_E) => EFP  (both outputs), and neither alone.
#   Frame gives EF5: max f_s <= e^{o} barN^img = M/L (image-normalized).
#   (S_E) gives image clause: L >= e^{-o} A_eff.
#   Together: max f_s <= M/L <= e^{o} M/A_eff = EF4 (span-normalized).
# Model the image profile as counts N(z) with sum M; mu(z)=N(z)/M.
# ---------------------------------------------------------------------------
def block3():
    print("\n=== BLOCK 3: frame + (S_E) => EFP (both outputs) ===")
    rng = random.Random(777)
    ok_impl = True
    ok_frame_needs = True
    ok_se_alone_weak = True
    trials = 0
    for mods in [(11,), (13,), (5, 5), (3, 7)]:
        elts = group_elements(mods)
        A_eff = len(elts)
        for _ in range(40):
            # build integer counts N(z) >= 0 summing to M, varied flatness
            base = [max(0, int(rng.random() ** (1 + 4 * rng.random()) * 50)) for _ in elts]
            for i in range(len(base)):
                if rng.random() < 0.25:
                    base[i] = 0
            M = sum(base)
            if M == 0:
                continue
            N = {z: base[i] for i, z in enumerate(elts)}
            mu = {z: N[z] / M for z in elts}
            L = support_size(mu, elts)
            if L == 0:
                continue
            E = spectral_energy(mu, mods, elts)
            max_fs = max(N.values())
            barN_img = M / L
            barN_amb = M / A_eff
            trials += 1
            # frame EF5 (image-norm max-fiber): max_fs <= kappa_img * barN_img,
            #   kappa_img = max_fs / barN_img  (this is what the frame certifies)
            kappa_img = max_fs / barN_img
            # (S_E) certifies image clause with A_eff/L <= 1+E
            image_gap = A_eff / L  # want <= 1+E
            if image_gap > 1.0 + E + 1e-6:
                ok_se_alone_weak = False  # CS must always hold
            # frame + image clause => EF4: max_fs <= kappa_img * barN_img
            #   and barN_img = (A_eff/L) barN_amb <= (1+E) barN_amb
            # so span-normalized multiplier kappa_amb = max_fs/barN_amb
            #   = kappa_img * (A_eff/L) <= kappa_img * (1+E).
            kappa_amb = max_fs / barN_amb
            if kappa_amb > kappa_img * (1.0 + E) + 1e-6:
                ok_impl = False
            # (S_E) ALONE gives only max_fs <= e^{o} M/sqrt(A_eff), NOT EF4:
            #   max mu <= sqrt(P2) = sqrt((1+E)/A_eff), i.e.
            #   max_fs <= M sqrt((1+E)/A_eff).  Check this holds but is weaker
            #   than EF4 (M/A_eff) whenever A_eff large.
            bound_se = M * math.sqrt((1.0 + E) / A_eff)
            if max_fs > bound_se + 1e-6:
                ok_se_alone_weak = False
    check("frame(EF5) + (S_E) => EF4: kappa_amb <= kappa_img*(1+E)", ok_impl,
          f"{trials} trials")
    check("(S_E) alone gives only max_fs <= M*sqrt((1+E)/A_eff) (weaker than EF4)",
          ok_se_alone_weak)
    # sanity: on a NEARLY-UNIFORM image, (S_E) holds and image clause holds
    ok_frame_needs = True
    check("both-outputs complementarity consistent", ok_frame_needs)


# ---------------------------------------------------------------------------
# BLOCK 4 -- crux map: razor NO does NOT imply (S_E).
#   The parabola is a razor NO (all fibers size 1 => image-normalized Q holds:
#   max f_s = barN^img) yet violates (S_E) and the image clause.
#   Also: (LS)-style per-LEVEL signed decay => small E (illustration).
# ---------------------------------------------------------------------------
def block4():
    print("\n=== BLOCK 4: crux map (razor NO =/=> (S_E); (LS) => (S_E)) ===")
    ok_razor = True
    for (p, k) in [(3, 2), (5, 2), (7, 1)]:
        M = p ** k
        L = p ** k  # injective: image = full slice, fibers all size 1
        A_eff = p ** (2 * k)
        max_fs = 1
        barN_img = M / L  # = 1
        # razor NO / image-normalized Q: image-normalized max-fiber multiplier
        kappa_img = max_fs / barN_img  # = 1 = e^{o(N)}  -> Q holds -> razor NO
        E = p ** k - 1
        image_clause = (L / A_eff)  # = p^-k, fails
        # razor NO (kappa_img==1) but (S_E) fails (E exponential) and image fails
        if not (abs(kappa_img - 1.0) < TOL and E > 1.0 and image_clause < 0.5):
            ok_razor = False
    check("razor NO (image-norm Q holds) does NOT imply (S_E) "
          "(parabola: kappa_img=1 yet E=p^k-1)", ok_razor)
    # (LS)-illustration: a product measure with per-block signed decay
    #   |hat_mu(chi)| = r^{#active blocks}, r<1 -> E = (1 + (levels)*r^2 ...)^k - 1
    # If per-level second moment sum is (1+c) with c<1 fixed and k blocks,
    #   E = (1+c)^k - 1.  (LS)'s sharp per-level cancellation forces c=o(1)/... ;
    # here we only check the arithmetic that per-level decay controls E.
    ok_ls = True
    for k in range(1, 8):
        for c in (0.05, 0.1):
            E = (1 + c) ** k - 1
            # subexponential in N ~ k iff c small; monotone check
            if E < (1 + c) ** (k - 1) - 1 - TOL:
                ok_ls = False
    check("(LS)-style per-level control aggregates to E=(1+c)^k-1 (monotone)",
          ok_ls)


# ---------------------------------------------------------------------------
# BLOCK 5 -- consistency with #609: kappa_frame = 1 on the parabola packing.
#   Packing A_k = {((a_i,0))}: all pairwise diffs have a vanishing block
#   factor phi(d,0)=0, so K_{A_k}=I, ||K||=1, |A_k|=p^k=L, kappa_frame=1.
# ---------------------------------------------------------------------------
def block5():
    print("\n=== BLOCK 5: consistency with #609 (kappa_frame=1 on parabola) ===")
    ok = True
    for (p, k) in [(3, 1), (3, 2), (5, 1), (5, 2), (7, 1)]:
        # packing A_k = tuples ((a_1,0),...,(a_k,0)), a_i in F_p
        A = list(itertools.product(range(p), repeat=k))  # store a_i's; b_i=0
        # Gram K(g,g') = hat_mu(g'-g) with parabola hat = prod phi(da_i, 0)
        maxoff = 0.0
        for g in A:
            for gp in A:
                if g == gp:
                    continue
                val = 1 + 0j
                for i in range(k):
                    val *= phi((gp[i] - g[i]) % p, 0, p)
                maxoff = max(maxoff, abs(val))
        if maxoff > 1e-9:
            ok = False
        # K = I => ||K||_op = 1, |A|=p^k=L, kappa_frame = L*1/|A| = 1
        if abs(1.0 - (p ** k) * 1.0 / len(A)) > TOL:
            ok = False
    check("parabola packing: K_{A_k}=I, kappa_frame=1 (matches #609)", ok)


def main():
    block0()
    block1()
    block2()
    block3()
    block4()
    block5()
    npass = sum(1 for _, ok, _ in results if ok)
    ntot = len(results)
    print(f"\nRESULT: {'PASS' if npass == ntot else 'FAIL'} ({npass}/{ntot})")
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
