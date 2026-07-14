# Counterexamples to Global Prefix/Staircase Extremality

**Author:** Manuel E. Rey-Álvarez Zafiria

**Status:** COUNTEREXAMPLE / REPAIRED THEOREM

## Main conclusion

The following global principle is false:

> For every received word and every agreement threshold, the complete RS
> list, or the complete set of MCA-bad slopes, is bounded by one canonical
> prefix/staircase ledger.

It fails both because different prefix fibers can glue into a larger list
and because a single prefix fiber can exceed the average prefix arithmetic.
Two exact finite-field certificates establish both mechanisms.

A universal replacement does hold:

```text
|List_a(y)| <= floor(C(n,K)/C(a,K)),                 (L)

B_MCA(a) <= min(q, floor(C(n,k+1)/(a-k))).           (M)
```

These incidence envelopes allow arbitrary prefix nonflatness and arbitrary
cross-prefix gluing. They are nevertheless too large for the active adjacent
rows, so they do not replace the structural `Q`, `BC`, or shift-pair inputs.

## Definitions

Let `F` be a finite field of size `q`, let `D subset F` have size `n`, and
let

```text
RS_K(D) = { (f(x))_{x in D} : deg(f)<K }.
```

For a received word `y:D->F` and a codeword `c`, write

```text
A_c(y) = {x in D : c(x)=y(x)}.
```

Then

```text
List_a(y) = {c in RS_K(D) : |A_c(y)|>=a}.
```

For a size-`a` support `S`, its first locator prefix at depth `a-K` is the
corresponding tuple of leading nontrivial coefficients of

```text
Lambda_S(X)=product_{x in S}(X-x).
```

At depth one this prefix is `-sum(S)`. A one-prefix extremality law asserts
that the full list can be compressed to, or bounded by, one such fiber.

For MCA, fix a received line `(f_1,f_2)` and define

```text
h_gamma = f_1+gamma f_2,    gamma in F.
```

A finite slope is MCA-bad at agreement `a` when `h_gamma` has an RS
codeword agreeing on at least `a` positions, but the received pair is not
simultaneously explained there by two degree-`<k` codewords. Let `B_MCA(a)`
be the number of distinct bad slopes.

## Counterexample 1: cross-prefix gluing over `F_7`

Take

```text
F=F_7,
D=(0,1,2,3,4,5),
K=2,
a=3,
y=(0,0,0,1,5,4).
```

Exactly four affine codewords `A+BX` agree with `y` in at least three
positions:

| `(A,B)` | agreement support |
|---|---|
| `(0,0)` | `{0,1,2}` |
| `(3,4)` | `{1,3,4}` |
| `(0,5)` | `{0,3,5}` |
| `(2,6)` | `{2,4,5}` |

An exhaustive enumeration of all `7^6` received words and all 49 affine
codewords proves that four is the global maximum; 2,352 received words
attain it.

At depth one, the exact prefix-fiber sizes of three-subsets are

```text
(3,3,3,2,3,3,3),
```

so every individual prefix fiber has size at most three. The canonical
average arithmetic also gives

```text
L_pref = ceil(C(6,3)/7^(3-2)) = 3.
```

Therefore

```text
|List_3(y)| = 4 > 3 = max_z |Fib_1(z)| = L_pref.
```

No compression into one prefix can preserve the extremal list size.

For the pole line at `alpha=6`, take the constant code `k=1` and

```text
f=(0,0,0,2,1,3),
g=(6,3,2,5,4,1).
```

The exact MCA-bad slopes are

```text
{0,2,3,6}.
```

The one-prefix pole conversion predicts `M_pref=1`, while the actual count
is four. Thus the same example refutes the proposed MCA extremality law.

## Counterexample 2: a nonflat prefix over `F_23`

Let `D` be the quadratic-residue subgroup of `F_23^*`:

```text
D=(1,2,3,4,6,8,9,12,13,16,18),    n=11.
```

Take `K=7`, `a=8`, and the received word

```text
y(x)=x^8.
```

There are exactly eleven zero-sum triples `T subset D`. For every such
triple, let `M=D\T`; then `|M|=8` and `sum(M)=0`. Define

```text
c_M(X)=X^8-Lambda_M(X).
```

Because the `X^7` coefficient of `Lambda_M` is `-sum(M)=0`, the degree of
`c_M` is less than seven. Hence `c_M in RS_7(D)`, and it agrees with `x^8`
on all points of `M`.

The eleven complements are distinct, so

```text
|List_8(y)| >= 11.
```

They all lie in the depth-one prefix fiber `sum(M)=0`. However the canonical
average value is

```text
L_pref = ceil(C(11,8)/23) = 8.
```

Thus a single realizable prefix fiber already has size eleven, refuting the
flat-prefix arithmetic.

At the pole `alpha=0`, with MCA dimension `k=6`, the eleven codewords yield
eleven distinct bad slopes

```text
gamma_M = -product(M) = -product(T)^(-1).
```

They are exactly `-D`. Therefore

```text
B_MCA(8)=11 > 2=M_pref.
```

This multiplicative family is structural, not an isolated numerical search.

## Repaired list incidence theorem

For every `y:D->F` and every `a>=K`,

```text
|List_a(y)| <= floor(C(n,K)/C(a,K)).                 (7)
```

More precisely, if `L_m(y)` is the number of codewords with exact agreement
`m`, then

```text
sum_{m=a}^n C(m,K)L_m(y) <= C(n,K).                  (8)
```

### Proof

Attach to each codeword `c` every `K`-subset of `A_c(y)`. Two distinct
codewords cannot receive the same token: if they agree with `y` on the same
`K` positions, their difference has degree less than `K` and has `K`
distinct roots, so it is zero. A codeword of exact agreement `m` consumes
exactly `C(m,K)` tokens, and only `C(n,K)` tokens exist. This proves (8).
Every codeword in `List_a(y)` consumes at least `C(a,K)` tokens, proving
(7).

The argument is compatible with any exact-agreement and first-match profile
partition, because such a partition neither omits nor duplicates codewords.

## Repaired MCA incidence theorem

Let `1<=k<n` and `k+1<=a<=n`. For every received line,

```text
B_MCA(a)
 <= min(q, floor(C(n,k+1)/(a-k))).                   (9)
```

### Proof

For each bad slope, choose a certifying codeword of maximum agreement and
let `A_gamma` be its exact support, of size `m_gamma>=a`. This support is
not common for `(f_1,f_2)`.

At least one of the restrictions `f_1|A_gamma`, `f_2|A_gamma` is not
representable by a degree-`<k` polynomial. For any nonrepresentable function
on an `m`-set, at least `m-k` of its `(k+1)`-subsets remain
nonrepresentable. To see this, choose a closest degree-`<k` polynomial with
`d` errors. For every error and every `k`-subset of its agreement set, the
resulting `(k+1)`-subset is nonrepresentable. The number produced is

```text
d C(m-d,k) >= d(m-k-d+1) >= m-k.
```

Call these noncommon `(k+1)`-subsets the tokens of `gamma`.

One noncommon token supports at most one finite slope. Indeed, if distinct
`gamma,gamma'` were explained on the same token by `c,c'`, then

```text
(c-c')/(gamma-gamma')
```

would explain `f_2` there, and subtraction would also explain `f_1`, making
the token common. This is a contradiction.

Distinct bad slopes therefore consume disjoint token sets, each of size at
least `a-k`, among `C(n,k+1)` available tokens. This proves the incidence
term in (9); the other term follows because only `q` finite slopes exist.

## Checks against the counterexamples

| case | list count | list envelope | MCA count | MCA envelope |
|---|---:|---:|---:|---:|
| `F_7` | 4 | 5 | 4 | 7 |
| `F_23` | 11 | 41 | 11 | 23 |

The repaired bounds allow both counterexamples. In the `F_7` list case, the
four supports consume twelve distinct two-subsets from a capacity of
fifteen. In the `F_23` list case, they consume 88 distinct seven-subsets
from a capacity of 330.

## Active-row obstruction

The universal theorem is not quantitatively sufficient at the adjacent
challenge rows. With `n=2^21` and `k=2^20`, exact integer lower bounds for
the list envelope give

| row | agreement | certified envelope lower bound | budget |
|---|---:|---:|---:|
| KoalaBear list | 1,116,047 | 340,906,412,957,980,610 | 274,980,728,111,395,087 |
| Mersenne-31 list | 1,116,023 | 24,936,335 | 16,777,215 |

Both universal list envelopes already exceed the target budget.

For MCA, the incidence term exceeds `q` in both rows, so (9) reduces to the
trivial all-slopes bound:

```text
q_KoalaBear = (2^31-2^24+1)^6,
q_Mersenne31 = (2^31-1)^4.
```

Both field sizes exceed their corresponding budgets by many orders of
magnitude.

## Implications

The lower prefix/staircase witnesses are not global extremizers. Any theorem
asserting that every extremal RS-MCA witness compresses to one canonical
prefix is false without additional hypotheses.

The counterexamples do not refute prefix fibers as lower witnesses, a
max-fiber `Q` theorem, quotient descent, split-pencil reductions, or the
same-prefix shift-pair ledger. They show that those objects cannot be turned
into a global upper theorem without an explicit cross-prefix owner or
routing argument.

The incidence theorem is the strongest immediate hypothesis-free repair in
this direction, but its active arithmetic proves that structural input is
still necessary. A useful replacement for global extremality must control
either the number of occupied unpaid prefixes, a bounded-component
cross-prefix transition graph, or a bounded-to-one routing of every bad
slope to a canonical structural cell.

## Reproduction

From the repository root run

```text
python experimental/scripts/verify_prefix_staircase_extremality_counterexamples.py
python experimental/scripts/verify_rs_incidence_envelopes.py
```

Both scripts use only the Python standard library and regenerate the JSON
certificates under
`experimental/data/certificates/prefix-staircase-extremality/`.
