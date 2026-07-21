# Quadratic-direction quartic lines on D128

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** PROVED (computer-assisted exact finite theorem).

Let `F=F_2147483647` and let `D_128` be the full root set of normalized
`T_128`.  Partition it into the 32 complete `T_4` fibres.  For every
four-subset `A` that is not one complete `T_4` fibre, define

```text
R_A(Y)=product_(a in A)(Y-a)
      =Y^4-e1(A)Y^3+e2(A)Y^2-e3(A)Y+e4(A).
```

Such subsets are called canonical quartets.

## Theorem

Every affine coefficient line with fixed `e1` contains at most two
canonical quartics unless there are `s,p in F` for which the whole line has
the form

```text
R_q(Y)=(Y^2-sY+p)(Y^2+q).                         (1)
```

Thus every line containing at least three canonical members is an
opposite-pair carrier.

A fixed-`e1` line is exactly a family

```text
R_t(Y)=R_0(Y)+tQ(Y),  deg Q<=2.
```

Multiplying (1) gives the coefficient equations

```text
e1=s,
e3=s e2-s p,
e4=p e2-p^2.
```

Whenever the variable factor splits on `D_128`, it contributes an opposite
root pair.

## Exact census

The primary implementation enumerates

```text
binom(128,4)-32 = 10667968
```

canonical quartets and all `17244778` unordered pairs with common `e1`.
After exact line normalization it obtains

```text
maximum points on a line:                    62
lines with at least 22 points:             8128
heavy lines that are carriers:             8128
maximum points on a noncarrier line:           2.
```

The independent implementation rebuilds `D_128`, uses two independent
saturating filters to retain every line with at least three pair hits, and
then recounts retained keys exactly.  It finds

```text
exact candidate lines:                      8196
maximum pair multiplicity:                  1891
noncarrier lines with at least 3 points:        0.
```

Hash collisions can add candidates to the exact second pass but cannot
remove a true line, so the filtering has no false-negative route.  Since the
classification is on the full domain, deleting an active puncture cannot
create a new collinearity.

## Reproduction

Compile the two implementations with C++20:

```text
g++ -O3 -std=c++20 experimental/scripts/verify_d128_quartic_line_dichotomy.cpp -o quartic_lines
./quartic_lines --full

g++ -O3 -std=c++20 experimental/scripts/audit_d128_quartic_line_dichotomy.cpp -o quartic_lines_audit
./quartic_lines_audit experimental/data/certificates/d128-quartic-line-dichotomy/independent_output.json
```

The recorded outputs and source hashes are in
`experimental/data/certificates/d128-quartic-line-dichotomy`.

## Scope

The theorem controls quartic families already known to lie on one
degree-at-most-two affine line.  It does not prove such collinearity for
arbitrary same-prefix varying owners, and carrier classification alone is
not a first-match payment.
