#!/usr/bin/env python3
"""Verify the raw arbitrary-locator-fiber overcount.

If U is already a degree-<k codeword, then every s-subset is feasible:
deg(U mod L_S) < k.  Thus raw Fib_U(s) can be huge while the actual list
contains only that codeword.  This refutes the literal arbitrary-Fib_U local
limit, but not the monomial-prefix local-limit problem.
"""

from math import comb, gcd, log2


def main():
    p = 97
    n = 16
    k = 7
    sigma = 4
    s = k + sigma
    target_exp = 2

    fiber_size = comb(n, s)
    target_bound = n**target_exp
    entropy_lhs = sigma * log2(p)
    entropy_rhs = log2(comb(n, s))

    assert gcd(n, k) == 1
    assert fiber_size == 4368
    assert target_bound == 256
    assert fiber_size > target_bound
    assert entropy_lhs > entropy_rhs

    print("L1 arbitrary-fiber overcount verifier passed")
    print(f"p={p}, n={n}, k={k}, sigma={sigma}, s={s}")
    print(f"|Fib_0(s)| = binom({n},{s}) = {fiber_size}")
    print(f"n^{target_exp} = {target_bound}")
    print(f"entropy lhs = {entropy_lhs:.6f} > rhs = {entropy_rhs:.6f}")
    print("actual list size for U=0 is 1, but raw feasible supports are all s-subsets")


if __name__ == "__main__":
    main()
