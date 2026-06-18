#!/usr/bin/env python3
"""Finite sanity scan for the Cycle 12 t=2, j=3 incidence wall.

This is not a proof of any MCA theorem. It extends the Cycle 11 finite
checker from co-support size j=2 to j=3 and verifies the closed form for the
quotient Q_S.

Setup:

  B = F_p, F = F_{p^2}, D = F_p
  t = sigma = 2
  j = n-a = 3, so a = n-3 and k = n-5

For W = interp_D(w) and T = D\\S with |T|=3, write

  e1 = sum(T), e2 = sum_{i<j} t_i t_j, e3 = prod(T).

If W_i is the coefficient of X^i and D1=e1(D), D2=e2(D), then

  Q_S = A X^2 + (B + A(D1-e1)) X
        + C + B(D1-e1) + A(D1^2-D2-D1 e1+e2),

where A=W_{n-1}, B=W_{n-2}, C=W_{n-3}.  Thus Q_S itself is independent of
e3, but the bad-line test after multiplying by L_T sees e3 through [L_T]_E.
"""

from itertools import combinations
import importlib.util
from pathlib import Path
import random


ROOT = Path(__file__).resolve().parent
PREV = ROOT / "20260618_cycle11_t2_j2_line_incidence_verify.py"
spec = importlib.util.spec_from_file_location("cycle11", PREV)
c11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c11)


def elem2(points):
    out = c11.zero
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            out = c11.fadd(out, c11.fmul(points[i], points[j]))
    return out


def elem3(points):
    out = c11.zero
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                out = c11.fadd(out, c11.fmul(c11.fmul(points[i], points[j]), points[k]))
    return out


def sum_points(points):
    out = c11.zero
    for x in points:
        out = c11.fadd(out, x)
    return out


def q_formula_j3(W, n, D1, D2, e1, e2):
    A = c11.coeff(W, n - 1)
    B = c11.coeff(W, n - 2)
    C = c11.coeff(W, n - 3)
    D1_minus_e1 = c11.fsub(D1, e1)
    q2 = A
    q1 = c11.fadd(B, c11.fmul(A, D1_minus_e1))
    d1_sq = c11.fmul(D1, D1)
    inner = c11.fadd(c11.fsub(c11.fsub(d1_sq, D2), c11.fmul(D1, e1)), e2)
    q0 = c11.fadd(c11.fadd(C, c11.fmul(B, D1_minus_e1)), c11.fmul(A, inner))
    return c11.trim([q0, q1, q2])


def run_trial(p, nr, seed):
    c11.set_field(p, nr)
    rng = random.Random(seed)
    D = [c11.b(x) for x in range(p)]
    n = len(D)
    t = 2
    a = n - 3
    k = n - 5
    j = n - a
    assert j == 3 and a == k + t

    E = c11.random_separated_quadratic(rng)
    bnum = c11.random_bnum(rng)
    bnum_res = c11.residue2(bnum, E)

    w0 = [c11.b(rng.randrange(p)) for _ in D]
    w1 = [c11.b(rng.randrange(p)) for _ in D]
    w = [c11.fadd(w0[i], c11.fmul(c11.alpha, w1[i])) for i in range(n)]
    W = c11.interp(D, w)
    LD = c11.locator(D)

    D1 = sum_points(D)
    D2 = elem2(D)

    slopes = set()
    landings = 0
    q_depends_on_e3_counterexamples = 0
    max_same_e1e2_q_forms = {}

    for idxs in combinations(range(n), 3):
        T = [D[i] for i in idxs]
        LT = c11.locator(T)
        Ls, rem_l = c11.pdivmod(LD, LT)
        if rem_l != [c11.zero]:
            raise AssertionError("L_T did not divide L_D")
        qs, Is = c11.pdivmod(W, Ls)

        e1 = sum_points(T)
        e2 = elem2(T)
        e3 = elem3(T)
        q_form = q_formula_j3(W, n, D1, D2, e1, e2)
        if c11.trim(qs) != q_form:
            raise AssertionError(
                f"closed-form Q_S failed p={p} seed={seed} T={idxs}: {qs} != {q_form}"
            )

        key = (e1, e2)
        old = max_same_e1e2_q_forms.setdefault(key, q_form)
        if old != q_form:
            q_depends_on_e3_counterexamples += 1

        direct = c11.residue2(Is, E)
        z = c11.line_scalar(direct, bnum_res)

        Wres = c11.residue2(W, E)
        LTres = c11.residue2(LT, E)
        LDres = c11.residue2(LD, E)
        Qres = c11.residue2(qs, E)
        Pres = c11.rsub(c11.rmul(Wres, LTres, E), c11.rmul(LDres, Qres, E))
        Bpp = c11.rmul(bnum_res, LTres, E)
        det_direct = c11.wedge(Pres, Bpp)
        if (det_direct == c11.zero) != (z is not None):
            raise AssertionError("landing predicate disagrees with direct slope test")

        if z is not None:
            slopes.add(z)
            landings += 1

    c2 = len(slopes)
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
        "j": 3,
        "supports": n * (n - 1) * (n - 2) // 6,
        "landings": landings,
        "C2": c2,
        "q_e3_counterexamples": q_depends_on_e3_counterexamples,
    }


def main():
    cases = [(7, 3, 20), (11, 2, 20), (17, 3, 12)]
    max_c2 = 0
    for p, nr, trials in cases:
        for seed in range(trials):
            r = run_trial(p, nr, seed)
            max_c2 = max(max_c2, r["C2"])
            print(
                "p={p} seed={seed} q_gen={q_gen} q_line={q_line} "
                "n={n} t={t} sigma={sigma} j={j} C2={C2} "
                "landings={landings}/{supports} q_depends_on_e3_failures={q_e3_counterexamples}".format(**r)
            )
    print(f"cycle12_t2_j3_line_incidence_scan: PASS max_C2={max_c2}")


if __name__ == "__main__":
    main()
