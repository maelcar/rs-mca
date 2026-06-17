#!/usr/bin/env python3
"""Finite check for the sigma=2 degree-one extension-residue family.

This is experimental evidence for the Opus residual-slack audit.  It checks
the natural E=X-alpha, w=X^(k+2) datum over F_p^2 and counts supports with
e_1(S)=0, the degree-drop condition for sigma=2.
"""

from itertools import combinations


class Fp2:
    p = None
    d = None

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

    def __mul__(self, other):
        other = self.coerce(other)
        return type(self)(
            self.a * other.a + self.d * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def __pow__(self, exponent):
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
        return hash((self.a, self.b, self.p, self.d))


def make_field(p, d):
    class F(Fp2):
        pass

    F.p = p
    F.d = d
    return F


def first_nonsquare(p):
    for d in range(2, p):
        if pow(d, (p - 1) // 2, p) == p - 1:
            return d
    raise ValueError("no nonsquare found")


def count_sigma2(p, k):
    d = first_nonsquare(p)
    F = make_field(p, d)
    alpha = F(0, 1)
    a = k + 2
    slopes = set()
    valid_supports = 0

    for support in combinations(range(1, p), a):
        if sum(support) % p != 0:
            continue
        valid_supports += 1
        product = F(1)
        for s in support:
            product = product * (alpha - F(s))
        slopes.add(alpha**a - product)

    return d, valid_supports, len(slopes)


def main():
    for p, k in [(17, 8), (19, 9)]:
        d, valid_supports, slope_count = count_sigma2(p, k)
        print(
            f"p={p}, k={k}, sigma=2, d={d}: "
            f"valid supports={valid_supports}, distinct slopes={slope_count}/{p*p}"
        )
        assert slope_count > p
    print("sigma=2 degree-one finite check passed")


if __name__ == "__main__":
    main()
