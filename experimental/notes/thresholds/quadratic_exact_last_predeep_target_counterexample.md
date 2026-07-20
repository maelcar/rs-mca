# Quadratic-exact last-predeep counterexample to exact-deep-only O5c repair

## Status

This note records the independently audited, zero-payment theorem layer of
R33 Role 12. It gives an occurring-length Reed--Solomon family one redundancy
unit outside the exact-deep range whose exact MCA numerator is already below
the frozen `2^-128` target.

It is a necessary route cut for repairing the false universal O5c strict-
crossing assertion. It does not supply a replacement exclusion, a closed
profile theorem, a Grand parent, a recurrence, a ledger payment, or official-
score movement. The official score remains `0/2`.

The publication base is
`origin/main@9908454995f3f195cfe748f35a1135211609d066`. The two source files
consumed by the proof are byte-identical to their source-floor copies at
`6f4e918f27a11995d3951f4ebe7546d4add0f345`. At publication review, the
live open PR heads were #986 at `0b0fddc7d421b2469c58031b206711934a5bad93`,
#987 at `335b9634074fe3a1650749be5985b15e7c8b36ed`, #988 at
`1e7dae5a1b778ec7f2026616e8a2d1203f6b23aa`, and #989 at
`c1cfe797098ca6c14e2c6b60d2854503cb65dbfc`. None changes the pinned source
files or contains this parameter family.

## Theorem

Freeze `epsilon*=2^-128`. For every integer `s>=129`, put

```text
r = 2^s,              q = r^2 = 2^(2s),
F = GF(q),            D = F^*,          Gamma = F,
n = q-1,              R = 3r-1,         k = n-R,
a = n-r,              B* = floor(epsilon*|Gamma|)=2^(2s-128).
```

For the ordinary Reed--Solomon code `C=RS_F(D,k)`, the exact challenge-
restricted MCA numerator at agreement `a` is

```text
B_C,Gamma^MCA(a) = r+1 = 2^s+1.
```

Consequently

```text
2^s+1 < 2^(2s-128) = B*
```

for every `s>=129`. These are occurring lengths `n=2^(2s)-1`; no statement
at every integer length is made.

## Exact arithmetic

The row is exactly one redundancy unit outside the source's exact-deep range:

```text
3(n-a)-R = 3r-(3r-1) = 1.
```

Nevertheless the quadratic mean-overlap theorem applies with strict margin
one:

```text
a^2 - n(k+r) = 1,
r^2 - n(3r-R) = 1.
```

Its upper bound is `r+1`. The universal tangent construction gives the same
lower bound because `Gamma=F`, so the numerator is exactly `r+1`.

Every list in the adjacent dimension-`k+1` code at agreement `a` is empty or
a singleton. Indeed, two distinct listed words would agree with each other on
at least

```text
2a-n = q-1-2r > q-3r = k
```

coordinates, impossible for two distinct degree-at-most-`k` polynomials.
Thus the profile list cap is one. The collision-aware source formula

```text
M(L)=ceil(L(q-n)/(q-n+k(L-1)))
```

is consumed only at `L=1`, where `q-n=1` and `M(1)=1`. With the full
challenge field this gives profile floor one. The source-valid reserve is the
maximum of the profile and tangent floors, not their sum.

## Endpoint field and admissibility

At `s=129`, one concrete presentation is

```text
GF(2^129) = F_2[T]/(T^129+T^5+1),
GF(2^258) = GF(2^129)[Y]/(Y^2+Y+1).
```

Rabin's criterion proves `T^129+T^5+1` irreducible. Since `129` is odd,
`3` does not divide `2^129-1`, so `Y^2+Y+1` has no root over the base field.
For later `s`, only the abstract finite field `GF(2^(2s))` is used.

The domain is the full multiplicative group, the challenge is the full field,
and the target is frozen before the family. The deterministic exact-support
atlas has at most `binom(n,r)` cells and

```text
log binom(n,r) <= r log(e n/r) = o(n).
```

The source's first-match support routing is therefore subexponential. The
complete profile envelope is retained; the singleton bound applies to every
eligible adjacent-code list. No scalar extension, subfield postselection,
postselected challenge, or reciprocal `L>1` shortcut is used.

## Replay

Run

```bash
python3 experimental/scripts/verify_quadratic_exact_last_predeep_target_counterexample.py
python3 -O experimental/scripts/verify_quadratic_exact_last_predeep_target_counterexample.py
```

Both outputs must equal the checked-in transcript. The standard-library-only
verifier pins the current source files, checks the exact symbolic identities,
replays `s=129..160`, proves the endpoint field presentation, and rejects
seventeen semantic mutations. Independent director replay also matched normal
and optimized output and the expected transcript.

## Audit scope

The same-author repair was followed by two distinct external Pro audits. The
hostile proof audit and source/compiler audit each returned `ACCEPT_NARROWED`
only for the theorem above and its necessary-exclusion interpretation. The
source audit required corrected formula serialization, the valid quadratic-
theorem domain, current source rebinding, narrow novelty, and exclusion of
stale contextual scripts; those repairs are enforced here.

## Nonclaims and remaining wall

This note does not prove:

- a replacement sufficient exclusion for O5c;
- strict crossing on all non-exact-deep or all target-closed rows;
- a general profile-envelope upper theorem beyond this family;
- a finite or asymptotic ledger payment;
- Grand MCA, Grand List, a recurrence, or an official theorem;
- any official-score movement.

The exact remaining wall is to formulate and prove a target-viable exclusion
that removes every quadratic-exact target-closed row covered by the source
hypotheses, then establish the full profile comparison on the surviving
regime. This counterexample changes no deployed row and pays zero ledger
units.
