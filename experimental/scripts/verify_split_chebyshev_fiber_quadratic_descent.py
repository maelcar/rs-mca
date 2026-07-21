#!/usr/bin/env python3
"""Exact checks for split-Chebyshev-fibre quadratic descent."""

import json
import itertools


P = 2_147_483_647


def trim(a):
    while len(a) > 1 and a[-1] % P == 0:
        a.pop()
    return [x % P for x in a]


def add(a, b, scale=1):
    out = [0] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = (out[i] + x) % P
    for i, x in enumerate(b):
        out[i] = (out[i] + scale * x) % P
    return trim(out)


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % P
    return trim(out)


def deriv(a):
    return trim([(i * a[i]) % P for i in range(1, len(a))] or [0])


def chebyshev(n):
    t0 = [1]
    if n == 0:
        return t0
    t1 = [0, 1]
    for _ in range(1, n):
        two_x_t1 = [0] + [(2 * x) % P for x in t1]
        t0, t1 = t1, add(two_x_t1, t0, -1)
    return t1


def check_chebyshev_identity(m):
    t = chebyshev(m)
    dt2 = mul(deriv(t), deriv(t))
    lhs = mul([1, 0, -1], dt2)
    rhs = [(m * m) % P]
    rhs = add(rhs, mul(t, t), -(m * m))
    return trim(lhs) == trim(rhs)


def descent_rows(d):
    rows = []
    j = 0
    e = d
    r = 22
    m = 32 * d
    while e >= 2:
        n = m // e
        relation = "equality" if 3 * r == 2 * (n + 1) else "strict"
        outer_degree = r if j == 0 else 2 * (n - r + 1)
        rows.append(
            {
                "j": j,
                "degree": e,
                "values": r,
                "ratio": n,
                "selected_degree": r * e,
                "complement_degree": m - r * e,
                "degree_relation": relation,
                "outer_W_degree": outer_degree,
            }
        )
        if e == 2:
            break
        e //= 2
        r *= 2
        j += 1
    return rows


def verify_uniform_two_thirds_cap():
    cases = 0
    for n in range(2, 129):
        cap = (2 * n + 1) // 3
        threshold = cap + 1
        assert 3 * threshold >= 2 * (n + 1)
        assert 3 * cap < 2 * (n + 1)
        for degree in (4, 8, 16, 32):
            r = threshold
            e = degree
            n_stage = n
            while e >= 4:
                assert 3 * r >= 2 * (n_stage + 1)
                e //= 2
                r *= 2
                n_stage *= 2
            cases += 1
    return {
        "ratios_checked": [2, 128],
        "degrees_checked": [4, 8, 16, 32],
        "total_descent_chains": cases,
        "active_ratio_32_cap": (2 * 32 + 1) // 3,
    }


def toy_equality_case():
    # Over F_17, T_4=8*A(H), H=X^2-1/2, A=Y^2+2.
    p = 17
    inv2 = pow(2, -1, p)
    # V=2 is the inverse of A'(Y)^2=4Y^2 modulo Y^2+2.
    inverse_ok = (2 * 4 * (-2)) % p == 1
    # F=(1-X^2)H'^2*8^2-4^2*V(H)=-A(H).
    # Coefficients are low-to-high.
    h = [(-inv2) % p, 0, 1]

    def pmul(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % p
        while len(out) > 1 and out[-1] == 0:
            out.pop()
        return out

    def padd(a, b, scale=1):
        out = [0] * max(len(a), len(b))
        for i, x in enumerate(a):
            out[i] = (out[i] + x) % p
        for i, x in enumerate(b):
            out[i] = (out[i] + scale * x) % p
        while len(out) > 1 and out[-1] == 0:
            out.pop()
        return out

    ah = padd(pmul(h, h), [2])
    hp_b = [0, 16]  # H'=2X and B=8.
    lhs = pmul([1, 0, -1], pmul(hp_b, hp_b))
    f = padd(lhs, [32 % p], -1)
    minus_ah = [(-x) % p for x in ah]
    return {
        "inverse_mod_A": inverse_ok,
        "differential_divisibility_identity": f == minus_ah,
        "square_descent": h == [8, 0, 1],
    }


def exhaustive_ramification_lemma_toy():
    """Exhaust monic deg-4 h and monic deg-2 W over F_5."""
    p = 5

    def norm(a):
        a = [x % p for x in a]
        while len(a) > 1 and a[-1] == 0:
            a.pop()
        return a

    def padd(a, b):
        out = [0] * max(len(a), len(b))
        for i, x in enumerate(a):
            out[i] = (out[i] + x) % p
        for i, x in enumerate(b):
            out[i] = (out[i] + x) % p
        return norm(out)

    def pmul(a, b):
        out = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                out[i + j] = (out[i + j] + x * y) % p
        return norm(out)

    def compose(w, h):
        out = [0]
        for x in reversed(w):
            out = padd(pmul(out, h), [x])
        return out

    def divide(a, b):
        a = norm(a[:])
        b = norm(b[:])
        q = [0] * max(1, len(a) - len(b) + 1)
        inv = pow(b[-1], -1, p)
        while len(a) >= len(b) and a != [0]:
            shift = len(a) - len(b)
            coeff = a[-1] * inv % p
            q[shift] = coeff
            for i, x in enumerate(b):
                a[i + shift] = (a[i + shift] - coeff * x) % p
            a = norm(a)
        return norm(q), norm(a)

    def square_root(f):
        f = norm(f)
        if (len(f) - 1) % 2:
            return None
        m = (len(f) - 1) // 2
        for lead in range(p):
            if lead * lead % p != f[-1]:
                continue
            for lower in itertools.product(range(p), repeat=m):
                q = list(lower) + [lead]
                if pmul(q, q) == f:
                    return q
        return None

    hits = 0
    counterexamples = 0
    for h_coeffs in itertools.product(range(p), repeat=4):
        h = list(h_coeffs) + [1]
        square_plus_constant = False
        for q1, q0 in itertools.product(range(p), repeat=2):
            q = [q0, q1, 1]
            difference = padd(h, [(-x) % p for x in pmul(q, q)])
            if len(difference) == 1:
                square_plus_constant = True
                break
        for w_coeffs in itertools.product(range(p), repeat=2):
            w = list(w_coeffs) + [1]
            quotient, remainder = divide(compose(w, h), [1, 0, -1])
            if remainder == [0] and square_root(quotient) is not None:
                hits += 1
                if not square_plus_constant:
                    counterexamples += 1
    return {
        "field": 5,
        "monic_h_degree": 4,
        "monic_W_degree": 2,
        "solutions": hits,
        "counterexamples": counterexamples,
    }


def main():
    identities = {str(m): check_chebyshev_identity(m) for m in (256, 512, 1024)}
    rows = {str(d): descent_rows(d) for d in (8, 16, 32)}
    for d, stages in rows.items():
        assert stages[0]["degree_relation"] == "equality"
        assert all(s["degree_relation"] == "strict" for s in stages[1:])
        assert all(s["selected_degree"] == 22 * int(d) for s in stages)
        assert all(s["complement_degree"] == 10 * int(d) for s in stages)
        assert all(s["outer_W_degree"] > 0 and s["outer_W_degree"] % 2 == 0 for s in stages)
        assert stages[-1]["degree"] == 2
    toy = toy_equality_case()
    parity_toy = exhaustive_ramification_lemma_toy()
    uniform = verify_uniform_two_thirds_cap()
    assert all(identities.values())
    assert all(toy.values())
    assert parity_toy["counterexamples"] == 0
    print(json.dumps({"status": "PASS", "chebyshev_identities": identities,
                      "descent_rows": rows, "toy_equality_case": toy,
                      "ramification_lemma_exhaustive_toy": parity_toy,
                      "uniform_two_thirds_cap": uniform},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
