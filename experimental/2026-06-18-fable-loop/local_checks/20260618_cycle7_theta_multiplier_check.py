#!/usr/bin/env python3
"""Cycle 7 sanity check for the nonconstant CRT-multiplier transfer.

This checks the algebraic step rejected in the Cycle 7 audit:

    [P0]_Ehat + theta [P1]_Ehat  ==  [interp_S(w0 + theta*w1)]_Ehat

for theta a nonconstant class in B[X]/Ehat.

The example uses B=F_5 and Ehat=X^2+1, so theta=X is the base CRT class for a
quadratic extension root.  On S={0,1}, take w0=0 and w1(0)=0, w1(1)=1.  Then
interp_S(w1)=X, so theta*interp_S(w1)=X^2=-1 mod Ehat, while
interp_S(theta*w1)=X.  Thus the quotient equation is a twisted readout, not an
ordinary residue-line datum for the pointwise word theta*w1.
"""

p = 5


def trim(poly):
    poly = [c % p for c in poly]
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out)


def mod_ehat(poly):
    """Reduce modulo Ehat=X^2+1 over F_5, i.e. X^2=-1=4."""
    poly = [c % p for c in poly]
    while len(poly) > 2:
        coeff = poly.pop()
        deg = len(poly)
        poly[deg - 2] = (poly[deg - 2] - coeff) % p
    while len(poly) < 2:
        poly.append(0)
    return poly[:2]


theta = [0, 1]  # X
interp_w1 = [0, 1]  # X on S={0,1}

twisted_readout = mod_ehat(mul(theta, interp_w1))
ordinary_word_readout = mod_ehat([0, 1])  # interp_S(x*w1(x)) has values 0,1

print("twisted theta*interp_S(w1) mod X^2+1:", twisted_readout)
print("ordinary interp_S(theta*w1) mod X^2+1:", ordinary_word_readout)
print("equal:", twisted_readout == ordinary_word_readout)

if twisted_readout == ordinary_word_readout:
    raise SystemExit("unexpected equality")
