#!/usr/bin/env python3
"""Verify Pro's F1 extension-line MCA counterexamples.

No external dependencies.  The finite field is represented as F_p[t]/(t^2-3).
The script checks:

* p=7, n=6, k=3: 15 distinct extension bad slopes, versus base numerator 7.
* p=17, n=16, k=8: 288 distinct extension bad slopes, versus base numerator 17.
"""

from itertools import combinations


class Fp2:
    p = None
    d = 3

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = int(a) % self.p
        self.b = int(b) % self.p

    @classmethod
    def coerce(cls, other):
        return other if isinstance(other, cls) else cls(other, 0)

    def __add__(self, other):
        other = self.coerce(other)
        return type(self)(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        other = self.coerce(other)
        return type(self)(self.a - other.a, self.b - other.b)

    def __neg__(self):
        return type(self)(-self.a, -self.b)

    def __mul__(self, other):
        other = self.coerce(other)
        return type(self)(
            self.a * other.a + self.d * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def inv(self):
        den = (self.a * self.a - self.d * self.b * self.b) % self.p
        if den == 0:
            raise ZeroDivisionError("nonzero element expected")
        inv_den = pow(den, -1, self.p)
        return type(self)(self.a * inv_den, -self.b * inv_den)

    def __truediv__(self, other):
        return self * self.coerce(other).inv()

    def __pow__(self, exponent):
        if exponent < 0:
            return (self.inv()) ** (-exponent)
        result = type(self)(1)
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def __eq__(self, other):
        other = self.coerce(other)
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b, self.p))

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        return f"{self.a}+{self.b}t"


def make_field(p):
    class F(Fp2):
        pass

    F.p = p
    return F


def poly_mul(a, b, F):
    out = [F(0) for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = out[i + j] + ai * bj
    return out


def poly_eval(poly, x, F):
    value = F(0)
    for coeff in reversed(poly):
        value = value * x + coeff
    return value


def poly_degree(poly, F):
    i = len(poly) - 1
    while i >= 0 and poly[i] == F(0):
        i -= 1
    return i


def divide_by_x_minus_alpha(poly, alpha, F):
    work = poly[:]
    deg = poly_degree(work, F)
    quotient = [F(0) for _ in range(max(deg, 0))]
    while poly_degree(work, F) >= 1:
        d = poly_degree(work, F)
        lead = work[d]
        quotient[d - 1] = lead
        work[d] = work[d] - lead
        work[d - 1] = work[d - 1] + lead * alpha
    assert all(c == F(0) for c in work)
    return quotient


def extension_slopes(p, k, agreement):
    F = make_field(p)
    alpha = F(0, 1)
    domain = [F(i) for i in range(1, p)]
    slopes = set()

    for support in combinations(domain, agreement):
        locator = [F(1)]
        for x in support:
            locator = poly_mul(locator, [-x, F(1)], F)

        monomial = [F(0)] * agreement + [F(1)]
        q_poly = []
        for i in range(max(len(monomial), len(locator))):
            q_poly.append(
                (monomial[i] if i < len(monomial) else F(0))
                - (locator[i] if i < len(locator) else F(0))
            )
        assert poly_degree(q_poly, F) <= agreement - 1

        z = poly_eval(q_poly, alpha, F)
        q_minus_z = q_poly[:]
        q_minus_z[0] = q_minus_z[0] - z
        p_poly = divide_by_x_minus_alpha(q_minus_z, alpha, F)
        assert poly_degree(p_poly, F) < k

        for x in support:
            f_x = (x ** agreement) / (x - alpha)
            g_x = -F(1) / (x - alpha)
            assert poly_eval(p_poly, x, F) == f_x + z * g_x

        slopes.add(z)

    return slopes


def base_bad_slopes(p, agreement):
    values = set()
    for support in combinations(range(1, p), agreement):
        values.add((-sum(support)) % p)
    return values


def main():
    slopes_7 = extension_slopes(p=7, k=3, agreement=4)
    assert len(slopes_7) == 15
    assert len(base_bad_slopes(p=7, agreement=4)) == 7

    slopes_17 = extension_slopes(p=17, k=8, agreement=9)
    assert len(slopes_17) == 288
    assert len(base_bad_slopes(p=17, agreement=9)) == 17

    print("F1 verifier passed")
    print("p=7: extension bad slopes = 15/49; base numerator = 7")
    print("p=17: extension bad slopes = 288/289; base numerator = 17")


if __name__ == "__main__":
    main()
