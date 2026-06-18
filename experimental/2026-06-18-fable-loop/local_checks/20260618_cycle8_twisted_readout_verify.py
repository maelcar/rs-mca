#!/usr/bin/env python3
"""Finite sanity checks for the Cycle 8 twisted-readout lemma.

This is not a proof of the RS-MCA prize problem.  It checks the algebraic
identities banked in the Cycle 8 audit over a tiny quadratic field:

  B = F_7, F = F_7[a]/(a^2-3), tau(a)=-a,
  t=sigma=2, k=2, a_support=4.

For random separated quadratic denominators E, random base anchors w0,w1, and
all 4-subsets S of D=F_7, it verifies:

  1. pi(T_theta(S)) = [interp_S(w)]_E.
  2. #T_theta values = #residue values.
  3. theta*interp_S(w1)-interp_S(theta*w1) is divisible by L_S with
     quotient degree <= 2t-2.
  4. Equal T_theta values imply the Cycle 6B kernel condition.
"""

from itertools import combinations
import random

p = 7
nr = 3


def fadd(x, y):
    return ((x[0] + y[0]) % p, (x[1] + y[1]) % p)


def fneg(x):
    return ((-x[0]) % p, (-x[1]) % p)


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y):
    return ((x[0] * y[0] + nr * x[1] * y[1]) % p,
            (x[0] * y[1] + x[1] * y[0]) % p)


def fpow(x, n):
    out = (1, 0)
    base = x
    while n:
        if n & 1:
            out = fmul(out, base)
        base = fmul(base, base)
        n >>= 1
    return out


def finv(x):
    if x == (0, 0):
        raise ZeroDivisionError
    return fpow(x, p * p - 2)


def fdiv(x, y):
    return fmul(x, finv(y))


def ftau(x):
    return (x[0] % p, (-x[1]) % p)


def b(c):
    return (c % p, 0)


zero = (0, 0)
one = (1, 0)
alpha = (0, 1)


def trim(poly):
    poly = [c for c in poly]
    while len(poly) > 1 and poly[-1] == zero:
        poly.pop()
    return poly


def deg(poly):
    poly = trim(poly)
    return -1 if poly == [zero] else len(poly) - 1


def padd(a, b_):
    m = max(len(a), len(b_))
    out = [zero] * m
    for i in range(m):
        out[i] = fadd(a[i] if i < len(a) else zero, b_[i] if i < len(b_) else zero)
    return trim(out)


def pneg(a):
    return trim([fneg(c) for c in a])


def psub(a, b_):
    return padd(a, pneg(b_))


def pmul(a, b_):
    out = [zero] * (len(a) + len(b_) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b_):
            out[i + j] = fadd(out[i + j], fmul(x, y))
    return trim(out)


def pscale(a, c):
    return trim([fmul(x, c) for x in a])


def pdivmod(a, mod):
    a = trim(a)
    mod = trim(mod)
    if deg(mod) < 0:
        raise ZeroDivisionError
    q = [zero] * max(1, (deg(a) - deg(mod) + 1))
    r = a[:]
    inv_lc = finv(mod[-1])
    while deg(r) >= deg(mod) and r != [zero]:
        shift = deg(r) - deg(mod)
        coeff = fmul(r[-1], inv_lc)
        q[shift] = coeff
        sub = [zero] * shift + pscale(mod, coeff)
        r = psub(r, sub)
    return trim(q), trim(r)


def pmod(a, mod):
    return pdivmod(a, mod)[1]


def pgcd(a, b_):
    a, b_ = trim(a), trim(b_)
    while b_ != [zero]:
        _, r = pdivmod(a, b_)
        a, b_ = b_, r
    if a == [zero]:
        return a
    return pscale(a, finv(a[-1]))


def pegcd(a, b_):
    old_r, r = trim(a), trim(b_)
    old_s, s = [one], [zero]
    old_t, t_ = [zero], [one]
    while r != [zero]:
        q, rem = pdivmod(old_r, r)
        old_r, r = r, rem
        old_s, s = s, psub(old_s, pmul(q, s))
        old_t, t_ = t_, psub(old_t, pmul(q, t_))
    lc_inv = finv(old_r[-1])
    return pscale(old_r, lc_inv), pscale(old_s, lc_inv), pscale(old_t, lc_inv)


def pinv_mod(a, mod):
    g, s, _ = pegcd(a, mod)
    if g != [one]:
        raise ZeroDivisionError("not invertible")
    return pmod(s, mod)


def ptau(poly):
    return trim([ftau(c) for c in poly])


def peval(poly, x):
    out = zero
    for coeff in reversed(poly):
        out = fadd(fmul(out, x), coeff)
    return out


def interp(points, values):
    out = [zero]
    for i, xi in enumerate(points):
        basis = [one]
        denom = one
        for j, xj in enumerate(points):
            if i == j:
                continue
            basis = pmul(basis, [fneg(xj), one])
            denom = fmul(denom, fsub(xi, xj))
        out = padd(out, pscale(basis, fdiv(values[i], denom)))
    return trim(out)


def locator(points):
    out = [one]
    for x in points:
        out = pmul(out, [fneg(x), one])
    return out


def crt_theta(E, Etau, Ehat):
    # theta = alpha mod E, -alpha mod Etau.
    delta = fsub(fneg(alpha), alpha)
    h = pmul([delta], pinv_mod(pmod(E, Etau), Etau))
    theta = padd([alpha], pmul(E, h))
    theta = pmod(theta, Ehat)
    # The unique fixed representative should have base coefficients.
    if any(c[1] % p for c in theta):
        raise AssertionError(f"theta not in B[X]/Ehat: {theta}")
    return theta


def random_E():
    while True:
        c0 = (random.randrange(p), random.randrange(p))
        c1 = (random.randrange(p), random.randrange(p))
        if c0[1] == 0 and c1[1] == 0:
            continue
        E = [c0, c1, one]
        Etau = ptau(E)
        if pgcd(E, Etau) != [one]:
            continue
        if any(peval(E, b(x)) == zero for x in range(p)):
            continue
        return E, Etau, pmul(E, Etau)


def residue_key(poly):
    return tuple(trim(poly))


def run_trial(seed):
    random.seed(seed)
    E, Etau, Ehat = random_E()
    theta = crt_theta(E, Etau, Ehat)
    if pmod(theta, E) != [alpha]:
        raise AssertionError("theta mod E mismatch")

    D = [b(x) for x in range(p)]
    k = 2
    t = 2
    support_size = k + t
    w0 = [b(random.randrange(p)) for _ in D]
    w1 = [b(random.randrange(p)) for _ in D]

    tvals = []
    rvals = []
    full_interps = []

    for idxs in combinations(range(p), support_size):
        pts = [D[i] for i in idxs]
        vals0 = [w0[i] for i in idxs]
        vals1 = [w1[i] for i in idxs]
        P0 = interp(pts, vals0)
        P1 = interp(pts, vals1)
        Tval = pmod(padd(P0, pmul(theta, P1)), Ehat)
        Rres = pmod(padd(P0, pscale(P1, alpha)), E)
        if pmod(Tval, E) != Rres:
            raise AssertionError("pi(Ttheta) != residue")

        theta_vals = [peval(theta, x) for x in pts]
        interp_theta_w1 = interp(pts, [fmul(theta_vals[i], vals1[i]) for i in range(len(pts))])
        comm = psub(pmul(theta, P1), interp_theta_w1)
        L = locator(pts)
        Q, rem = pdivmod(comm, L)
        if rem != [zero] or deg(Q) > 2 * t - 2:
            raise AssertionError("commutator divisibility failed")
        if pmod(padd(interp_theta_w1, pmul(L, Q)), Ehat) != pmod(pmul(theta, P1), Ehat):
            raise AssertionError("commutator reconstruction failed")

        tvals.append(residue_key(Tval))
        rvals.append(residue_key(Rres))
        full_interps.append(padd(P0, pscale(P1, alpha)))

    if len(set(tvals)) != len(set(rvals)):
        raise AssertionError("distinct T count != distinct residue count")

    for i in range(len(tvals)):
        for j in range(i + 1, len(tvals)):
            if tvals[i] != tvals[j]:
                continue
            diff = psub(full_interps[i], full_interps[j])
            q, rem = pdivmod(diff, E)
            if rem != [zero] or deg(q) >= k:
                raise AssertionError("kernel condition failed")

    return {
        "seed": seed,
        "E": E,
        "Ehat": Ehat,
        "theta": theta,
        "distinct_tvals": len(set(tvals)),
        "distinct_residues": len(set(rvals)),
        "total_supports": len(tvals),
    }


def main():
    for seed in range(20):
        result = run_trial(seed)
        print(
            f"seed={seed} supports={result['total_supports']} "
            f"distinct_T={result['distinct_tvals']} "
            f"distinct_residue={result['distinct_residues']}"
        )
    print("cycle8_twisted_readout_verify: PASS")


if __name__ == "__main__":
    main()
