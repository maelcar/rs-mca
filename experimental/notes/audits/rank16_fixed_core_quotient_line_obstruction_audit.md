# Audit: rank-16 fixed-core quotient-line obstruction

## Verdict

`ACCEPT` as a narrow local theorem and route cut. It makes zero finite-ledger
payment and leaves the official score at `0/2`.

The frozen theorem packet is:

```text
theorem note  19325c602ae14082f6ef36db312d815552e0f0eefc0787f3a71fd4254af650f7
verifier      0e7e25a2e696941f42d7eaf24c4b441e769592c3ffff040883bb9b076765d7dd
expected      8dbe50b5911bfcdbc10fcc3ee578398d0d068f43f57b672c4e84eb42b64dc109
Lean target   f276f5ea54aa736d4c3476e0e1d21d9a8e58ff294c0841605a1f4853f6ad8213
```

## Hostile proof audit

The first independent audit rejected the draft for two exact reasons.

1. Its Lean predicate only said that visible base-field roots belong to `H`;
   an irreducible factor could pass vacuously. The repaired predicate requires
   `roots.card = natDegree` and support in `H`, which is genuine complete
   splitting.
2. An arbitrary affine-line presentation need not give a degree-controlled
   direction. The repaired proof first handles the constant family, then uses
   `V_k-V_j` for two actual distinct quotients. This gives the required
   `deg(V_k-V_j) <= 28897` and makes `H_0=P_j` nonzero.

The same auditor then re-read the corrected object and returned `ACCEPT` with
high confidence. It explicitly rechecked the cross-polynomial root count, gcd
reduction, common semi-character, `r=0` step, root-free cancellation, final
block-degree contradiction, modular-inverse source compiler, and all seven
surviving source conditions.

## Consumer and novelty audit

A second independent native audit of the corrected worktree returned
`ACCEPT`. Live comparison was against `origin/main@02728b208` and open PRs
through `#822`. No integrated or pending packet owns the theorem that one
normalized fixed-core quotient line contains at most five extra labels.

The consumer is exact but conditional: a nine-label counterexample to the
pending cap eight must have normalized quotient affine dimension from two
through eight. No affine-line owner, cap eight, parent saving, or score change
is imported.

## Executable audit

Using the bundled Codex Python runtime:

```text
normal replay:              PASS
optimized (-O) replay:      PASS, byte-identical
expected-output comparison: PASS
tamper self-test:           PASS, 3/3 rejected
py_compile:                 PASS
git diff --check:           PASS
```

The replay proves the deployed modulus prime, checks
`p-1=127*2^24`, and reproduces

```text
6B-2D = 3870,
[D-w,D] = [67472,96369],
2B = 65536 < D-w <= D < 98304 = 3B,
cap-eight target margin = 2720795531085176,
cap-nine target excess  = 26473583037029192.
```

The script is deliberately labeled an arithmetic replay. It does not claim to
machine-check the polynomial proof, splitting condition, modular inverse, or
gcd argument.

## Formalization status

The Lean module is an unproved statement target, not a Lean proof artifact.
It was statically audited against the Markdown theorem. A local Lean executable
was unavailable, so no local `lake build` claim is made.

## Use rule

This packet may be cited only to exclude affine quotient dimensions zero and
one in the literal fixed-27-core source cell. Charge no cap-eight ledger term
until the dimension-two-through-eight simultaneous-Pade wall is paid.
