#!/usr/bin/env python3
"""Finite sanity checks for the Cycle 9 locator-quotient wall.

This is not a proof of the RS-MCA prize problem.  It checks two elementary
claims banked in the Cycle 9 audit over a tiny quadratic field:

  B = F_7, F = F_7[a]/(a^2-3), D = B.

For all a-subsets S in two balanced regimes it verifies

  W = L_S Q_S + interp_S(w),        deg Q_S <= n-a-1,
  R_E(S) = [W]_E - [L_S Q_S]_E.

It also tabulates the distinction between raw residue values C1 and slope-line
landing values C2:

  t=1:  F[X]/E is one-dimensional, so the bad line is the whole space.
  t=2:  F[X]/E is two-dimensional, so the bad line is codimension one.
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
    q = [zero] * max(1, deg(a) - deg(mod) + 1)
    r = a[:]
    inv_lc = finv(mod[-1])
    while deg(r) >= deg(mod) and r != [zero]:
        shift = deg(r) - deg(mod)
        coeff = fmul(r[-1], inv_lc)
        q[shift] = coeff
        r = psub(r, [zero] * shift + pscale(mod, coeff))
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


def random_separated_quadratic():
    while True:
        c0 = (random.randrange(p), random.randrange(p))
        c1 = (random.randrange(p), random.randrange(p))
        if c0[1] == 0 and c1[1] == 0:
            continue
        E = [c0, c1, one]
        if pgcd(E, ptau(E)) != [one]:
            continue
        if any(peval(E, b(x)) == zero for x in range(p)):
            continue
        return E


def residue_key(poly):
    return tuple(trim(poly))


def line_scalar(residue, bnum):
    residue = trim(residue)
    bnum = trim(bnum)
    m = max(len(residue), len(bnum))
    residue = residue + [zero] * (m - len(residue))
    bnum = bnum + [zero] * (m - len(bnum))
    pivot = None
    for coeff in bnum:
        if coeff != zero:
            pivot = coeff
            break
    if pivot is None:
        raise AssertionError("zero numerator")
    z = None
    for ri, bi in zip(residue, bnum):
        if bi == zero:
            if ri != zero:
                return None
            continue
        candidate = fdiv(ri, bi)
        if z is None:
            z = candidate
        elif candidate != z:
            return None
    return z


def run_regime(seed, t, k):
    random.seed(seed)
    D = [b(x) for x in range(p)]
    n = len(D)
    a_support = k + t
    j = n - a_support

    if t == 1:
        E = [fneg(alpha), one]  # X-alpha
        bnum = [one]
    elif t == 2:
        E = random_separated_quadratic()
        bnum = [one, (2, 1)]
    else:
        raise ValueError("only t=1 or t=2 in this checker")

    w0 = [b(random.randrange(p)) for _ in D]
    w1 = [b(random.randrange(p)) for _ in D]
    w = [fadd(w0[i], fmul(alpha, w1[i])) for i in range(n)]
    W = interp(D, w)

    raw_residues = []
    slopes = []

    for idxs in combinations(range(n), a_support):
        pts = [D[i] for i in idxs]
        vals = [w[i] for i in idxs]
        Ls = locator(pts)
        qs, rem = pdivmod(W, Ls)
        Is = interp(pts, vals)

        if rem != Is:
            raise AssertionError("division remainder is not support interpolant")
        if deg(qs) > n - a_support - 1:
            raise AssertionError("quotient degree bound failed")

        direct = pmod(Is, E)
        decomposed = pmod(psub(W, pmul(Ls, qs)), E)
        if direct != decomposed:
            raise AssertionError("locator-quotient residue identity failed")

        raw_residues.append(residue_key(direct))
        z = line_scalar(direct, bnum)
        if z is not None:
            slopes.append(z)

    c1 = len(set(raw_residues))
    c2 = len(set(slopes))
    return {
        "seed": seed,
        "t": t,
        "k": k,
        "n": n,
        "a": a_support,
        "j": j,
        "supports": len(raw_residues),
        "raw_residue_values_C1": c1,
        "slope_line_values_C2": c2,
    }


def main():
    for seed in range(8):
        r1 = run_regime(seed, t=1, k=4)
        r2 = run_regime(seed, t=2, k=3)
        if r1["raw_residue_values_C1"] != r1["slope_line_values_C2"]:
            raise AssertionError("t=1 bad line should equal whole residue space")
        if r2["slope_line_values_C2"] > r2["raw_residue_values_C1"]:
            raise AssertionError("line landing count cannot exceed raw residue count")
        print(
            "seed={seed} t=1 C1={c1a} C2={c2a}; "
            "t=2 C1={c1b} C2={c2b} supports={sup}".format(
                seed=seed,
                c1a=r1["raw_residue_values_C1"],
                c2a=r1["slope_line_values_C2"],
                c1b=r2["raw_residue_values_C1"],
                c2b=r2["slope_line_values_C2"],
                sup=r2["supports"],
            )
        )
    print("cycle9_locator_quotient_incidence_check: PASS")


if __name__ == "__main__":
    main()
