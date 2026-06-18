#!/usr/bin/env python3
"""Finite sanity checks for the Cycle 11 t=2, j=2 incidence lemma.

This is not a proof of the prize problem.  It independently checks, over
small quadratic fields, the algebraic claims that make Cycle 11 bankable:

  * for t=2 and j=n-a=2, Q_S = C(X-s_T)+C_1;
  * bad-line landing is equivalent to one determinant equation det(s_T,p_T)=0;
  * the p_T^2 coefficient of det is wedge([W]_E,[Bnum]_E);
  * sampled D=F_p cases satisfy the claimed C2 <= 6n incidence bound.
"""

from itertools import combinations
import random


P = 7
NR = 3
zero = (0, 0)
one = (1, 0)
alpha = (0, 1)


def set_field(p, nr):
    global P, NR
    P, NR = p, nr


def fadd(x, y):
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def fneg(x):
    return ((-x[0]) % P, (-x[1]) % P)


def fsub(x, y):
    return fadd(x, fneg(y))


def fmul(x, y):
    return ((x[0] * y[0] + NR * x[1] * y[1]) % P,
            (x[0] * y[1] + x[1] * y[0]) % P)


def fpow(x, n):
    out = one
    base = x
    while n:
        if n & 1:
            out = fmul(out, base)
        base = fmul(base, base)
        n >>= 1
    return out


def finv(x):
    if x == zero:
        raise ZeroDivisionError
    return fpow(x, P * P - 2)


def fdiv(x, y):
    return fmul(x, finv(y))


def ftau(x):
    return (x[0] % P, (-x[1]) % P)


def b(c):
    return (c % P, 0)


def trim(poly):
    poly = [c for c in poly]
    while len(poly) > 1 and poly[-1] == zero:
        poly.pop()
    return poly


def deg(poly):
    poly = trim(poly)
    return -1 if poly == [zero] else len(poly) - 1


def coeff(poly, i):
    return poly[i] if i < len(poly) else zero


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
        c = fmul(r[-1], inv_lc)
        q[shift] = c
        r = psub(r, [zero] * shift + pscale(mod, c))
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
    for c in reversed(poly):
        out = fadd(fmul(out, x), c)
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


def residue2(poly, E):
    r = pmod(poly, E)
    return (coeff(r, 0), coeff(r, 1))


def rmul(u, v, E):
    return residue2(pmul([u[0], u[1]], [v[0], v[1]]), E)


def rsub(u, v):
    return (fsub(u[0], v[0]), fsub(u[1], v[1]))


def wedge(u, v):
    return fsub(fmul(u[0], v[1]), fmul(u[1], v[0]))


def line_scalar(residue, bnum_residue):
    z = None
    for ri, bi in zip(residue, bnum_residue):
        if bi == zero:
            if ri != zero:
                return None
            continue
        candidate = fdiv(ri, bi)
        if z is None:
            z = candidate
        elif candidate != z:
            return None
    return z if z is not None else zero


def bic_clean(poly):
    return {k: v for k, v in poly.items() if v != zero}


def bic(c):
    return {} if c == zero else {(0, 0): c}


def bi_add(a, b_):
    out = dict(a)
    for k, v in b_.items():
        out[k] = fadd(out.get(k, zero), v)
    return bic_clean(out)


def bi_neg(a):
    return {k: fneg(v) for k, v in a.items()}


def bi_sub(a, b_):
    return bi_add(a, bi_neg(b_))


def bi_mul(a, b_):
    out = {}
    for (is_, ip), av in a.items():
        for (js, jp), bv in b_.items():
            k = (is_ + js, ip + jp)
            out[k] = fadd(out.get(k, zero), fmul(av, bv))
    return bic_clean(out)


def bi_scale(a, c):
    return bic_clean({k: fmul(v, c) for k, v in a.items()})


S_VAR = {(1, 0): one}
P_VAR = {(0, 1): one}


def bi_eval(a, s, p):
    out = zero
    for (is_, ip), v in a.items():
        out = fadd(out, fmul(v, fmul(fpow(s, is_), fpow(p, ip))))
    return out


def rb_const(residue):
    return [bic(residue[0]), bic(residue[1])]


def rb_add(u, v):
    return [bi_add(u[0], v[0]), bi_add(u[1], v[1])]


def rb_sub(u, v):
    return [bi_sub(u[0], v[0]), bi_sub(u[1], v[1])]


def rb_mul(u, v, E):
    e0, e1 = E[0], E[1]
    a0b0 = bi_mul(u[0], v[0])
    a1b1 = bi_mul(u[1], v[1])
    c0 = bi_sub(a0b0, bi_scale(a1b1, e0))
    c1 = bi_sub(bi_add(bi_mul(u[0], v[1]), bi_mul(u[1], v[0])),
                bi_scale(a1b1, e1))
    return [c0, c1]


def rb_wedge(u, v):
    return bi_sub(bi_mul(u[0], v[1]), bi_mul(u[1], v[0]))


def build_det_poly(E, W, LD, bnum, C, C1):
    Wb = rb_const(residue2(W, E))
    LDb = rb_const(residue2(LD, E))
    Bb = rb_const(residue2(bnum, E))

    # [L_T]_E = (p-e0) + (-(s+e1)) X for L_T=X^2-sX+p.
    LT = [
        bi_sub(P_VAR, bic(E[0])),
        bi_sub(bi_neg(S_VAR), bic(E[1])),
    ]
    # Q_S = C(X-s)+C1.
    Q = [
        bi_sub(bic(C1), bi_scale(S_VAR, C)),
        bic(C),
    ]
    P_res = rb_sub(rb_mul(Wb, LT, E), rb_mul(LDb, Q, E))
    Bpp = rb_mul(Bb, LT, E)
    return rb_wedge(P_res, Bpp)


def random_separated_quadratic(rng):
    while True:
        c0 = (rng.randrange(P), rng.randrange(P))
        c1 = (rng.randrange(P), rng.randrange(P))
        if c0[1] == 0 and c1[1] == 0:
            continue
        E = [c0, c1, one]
        if pgcd(E, ptau(E)) != [one]:
            continue
        if any(peval(E, b(x)) == zero for x in range(P)):
            continue
        return E


def random_bnum(rng):
    while True:
        bnum = [(rng.randrange(P), rng.randrange(P)), (rng.randrange(P), rng.randrange(P))]
        if bnum != [zero, zero]:
            return trim(bnum)


def run_trial(p, nr, seed):
    set_field(p, nr)
    rng = random.Random(seed)
    D = [b(x) for x in range(P)]
    n = len(D)
    t = 2
    k = n - 4
    a = n - 2
    j = n - a
    assert j == 2 and a == k + t

    E = random_separated_quadratic(rng)
    bnum = random_bnum(rng)
    bnum_res = residue2(bnum, E)

    w0 = [b(rng.randrange(P)) for _ in D]
    w1 = [b(rng.randrange(P)) for _ in D]
    w = [fadd(w0[i], fmul(alpha, w1[i])) for i in range(n)]
    W = interp(D, w)
    LD = locator(D)

    C = coeff(W, n - 1)
    sigma1_D = zero
    for x in D:
        sigma1_D = fadd(sigma1_D, x)
    C1 = fadd(coeff(W, n - 2), fmul(C, sigma1_D))

    det_poly = build_det_poly(E, W, LD, bnum, C, C1)
    kappa = wedge(residue2(W, E), bnum_res)
    if det_poly.get((0, 2), zero) != kappa:
        raise AssertionError("p^2 coefficient of det is not kappa")

    if not det_poly and kappa != zero:
        raise AssertionError("det is identically zero but kappa is nonzero")
    if C != zero and not det_poly:
        raise AssertionError("det identically zero despite C != 0 over D=F_p")

    slopes = set()
    landings = 0
    supports = 0
    for i, j_ in combinations(range(n), 2):
        T = [D[i], D[j_]]
        LT = locator(T)
        Ls, rem_l = pdivmod(LD, LT)
        if rem_l != [zero]:
            raise AssertionError("L_T did not divide L_D")
        qs, Is = pdivmod(W, Ls)
        supports += 1

        sT = fadd(T[0], T[1])
        pT = fmul(T[0], T[1])
        q_form = [fsub(C1, fmul(C, sT)), C]
        if trim(qs) != trim(q_form):
            raise AssertionError("closed-form Q_S failed")

        direct = residue2(Is, E)
        z = line_scalar(direct, bnum_res)

        Wres = residue2(W, E)
        LTres = residue2(LT, E)
        LDres = residue2(LD, E)
        Qres = residue2(qs, E)
        Pres = rsub(rmul(Wres, LTres, E), rmul(LDres, Qres, E))
        Bpp = rmul(bnum_res, LTres, E)
        det_direct = wedge(Pres, Bpp)
        det_eval = bi_eval(det_poly, sT, pT)
        if det_direct != det_eval:
            raise AssertionError("symbolic det evaluation mismatch")
        if (det_direct == zero) != (z is not None):
            raise AssertionError("det landing predicate disagrees with direct slope test")

        if z is not None:
            slopes.add(z)
            landings += 1

    c2 = len(slopes)
    if c2 > 6 * n:
        raise AssertionError(f"C2={c2} exceeded 6n={6*n}")
    return {
        "p": p,
        "q_gen": p,
        "q_line": p * p,
        "seed": seed,
        "n": n,
        "k": k,
        "a": a,
        "t": t,
        "sigma": 2,
        "j": 2,
        "C_nonzero": C != zero,
        "det_zero": not bool(det_poly),
        "landings": landings,
        "C2": c2,
        "supports": supports,
    }


def main():
    cases = [(7, 3, 12), (11, 2, 10), (17, 3, 8)]
    max_c2 = 0
    for p, nr, trials in cases:
        for seed in range(trials):
            r = run_trial(p, nr, seed)
            max_c2 = max(max_c2, r["C2"])
            print(
                "p={p} seed={seed} q_gen={q_gen} q_line={q_line} "
                "n={n} t={t} sigma={sigma} j={j} C2={C2} "
                "landings={landings}/{supports} C_nonzero={C_nonzero} det_zero={det_zero}".format(**r)
            )
    print(f"cycle11_t2_j2_line_incidence_verify: PASS max_C2={max_c2}")


if __name__ == "__main__":
    main()
