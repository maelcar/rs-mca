# L1 Locator-Fiber Counterexample Audit

Route verdict: `COUNTEREXAMPLE`

Formal status tags: `COUNTEREXAMPLE`, `AUDIT`

Raw inputs:

- `raw/20260617_L1_LOCATOR_RAW_1.md`
- `raw/20260617_L1_LOCATOR_RAW_2.md`
- `raw/20260617_L1_LOCATOR_RAW_3.md`

Verifier:

- `../verify_l1_arbitrary_fiber_overcount.py`

## Codex Audit

This is significant, but it must be stated exactly. Pro found a genuine formulation bug in the raw arbitrary feasible-fiber local limit, not a counterexample to the monomial-prefix local-limit problem.

The literal arbitrary-fiber statements are:

- `tex/slackMCA_v3.tex:569` (`conj:arbitrary-local`)
- `tex/slackMCA_v3.tex:1702` (`conj:final-locator`)
- `tex/snarks_v4.tex:353` (`ass:locator`)

The issue is simple and decisive. If `U` is itself a degree-`<k` codeword, then for every `s`-subset `S`,

```text
deg(U mod L_S) < k.
```

Therefore every `s`-subset lies in the raw feasible fiber `Fib_U(s)`, even though the actual list contains only one codeword. The one-way bridge

```text
list size <= |Fib_U(s)|
```

is true, but the raw support count is too coarse to be the final local-limit object.

The verifier checks the finite packet:

```text
p = 97
n = 16
k = 7
sigma = 4
s = 11
U = 0
|Fib_0(11)| = binom(16,11) = 4368 > 16^2 = 256
gcd(n,k) = 1
entropy inequality clears
```

This refutes a literal polynomial bound on raw `Fib_U(s)`.

## Banked Result

Banked as:

```text
COUNTEREXAMPLE to raw arbitrary-Fib_U local limit.
```

Not banked as a refutation of:

- `conj:prefix-local`,
- the monomial-prefix L1 target,
- generated-field entropy lower bounds,
- quotient-core lower bounds,
- or actual list-size smallness.

## Required Repair

Replace the raw arbitrary support fiber by a pruned object, for example:

- codeword-indexed selected supports,
- maximal agreement supports,
- exact-agreement supports,
- or another canonical support selection that preserves list injection without counting all contained subsets of one codeword's agreement set.

The surviving L1 target is the aperiodic monomial-prefix / repaired-arbitrary local limit after quotient-periodic families are removed or budgeted.
