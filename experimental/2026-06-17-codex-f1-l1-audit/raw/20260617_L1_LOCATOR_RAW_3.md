## Result

**COUNTEREXAMPLE — COUNTEREXAMPLE.**
The L1 arbitrary locator-fiber statement in `slackMCA_v3.tex` is false as written. The failure is not a quotient-core phenomenon and not a generated-field entropy failure: it occurs with empty quotient profile and with the entropy inequality cleared. The monomial-prefix subproblem is not refuted; the false step is the upgrade from monomial-prefix/exact-support fibers to arbitrary (\Fib_U(s)).

---

## 1. Exact Paper B labels L1 depends on

Direct L1/list-local-limit labels in `tex/slackMCA_v3.tex`:

* `def:locator-fiber` — defines (\Fib_U(s)) and (\Phi_\sigma).
* `prop:arb-fiber` — list size injects into (\Fib_U(s)).
* `prop:monomial-fiber` — monomial-prefix words are exactly prefix fibers.
* `def:taustar` — entropy gap.
* `thm:pigeonhole`, `cor:genfield-pigeonhole`, `cor:entropy-lower` — generated-field entropy lower bound.
* `thm:qcore`, `def:qprofile`, `conj:listprofile` — quotient-core lower bound and quotient-profile reserve.
* `thm:upstairs`, `cor:upstairs-poly` — characteristic-zero quotient rigidity.
* `lem:galois-amp`, `thm:no-collision`, `cor:quasipoly-upper`, `rem:galois-limit` — Galois/norm route and its current range.
* `conj:prefix-local` — monomial-prefix local limit with quotient exceptions.
* `conj:arbitrary-local` — arbitrary locator-fiber local limit.
* `thm:conditional-list` — conditional list theorem from `conj:arbitrary-local`.
* `lem:pairwise` — pairwise distance shadow; explicitly insufficient.
* `conj:final-locator` — final arbitrary locator local limit.

Blueprint label:

* `prob:L1` in `tex/proximity_blueprint_v3.tex`.

MCA labels such as `conj:B`, `conj:final-mca`, `prop:qfloor`, and `thm:qnecessity` are comparison/calibration labels, not direct L1 list-local-limit inputs.

---

## 2. Restated L1 target with the required ledger

Let

[
B=\mathbb F_{q_{\rm gen}}\subseteq F,\qquad H\le B^\times,\qquad |H|=n=2^m,
]

where (B) is the generated field of the evaluation domain and its locator coefficients. Let

[
C_F=\RS[F,H,k],\qquad k=\rho n+O(1).
]

For a target radius

[
\delta=1-\rho-\eta,
]

the agreement size is

[
a=\lceil (1-\delta)n\rceil,\qquad \sigma=a-k,\qquad s=a=k+\sigma,
]

so, up to the (O(1/n)) rounding from (k=\rho n+O(1)),

[
\eta=\sigma/n.
]

The L1 target as written asks for

[
|\Fib_U(k+\sigma)|\le n^{B_{\rm exp}}
]

for every interpolant (U\in F[X]), (\deg U<n), whenever

[
\sigma\ge C_{\rho,B_{\rm exp},\varepsilon}\frac n{\log_2 n},
]

and

[
\sigma\log_2 q_{\rm gen}\ge(1+\varepsilon)\log_2\binom n{k+\sigma}.
]

Quotient notation:

* (K\le H) is a subgroup of order (M).
* (N=n/M) is the quotient size.
* A quotient-core obstruction is active, in Paper B’s list sense, when

[
M\mid \gcd(n,k),\qquad M>\sigma,\qquad k/M\le n/M-1.
]

The quotient-profile budget is

[
\mathcal Q_H(\eta)
==================

\max_{\substack{M\mid\gcd(n,k),\ \lceil\eta n\rceil<M\ k/M\le n/M-1}}
\log_2\binom{n/M-1}{k/M}.
]

For L1 itself, the arities are

[
\mu=1,\qquad \nu=1.
]

If a protocol later consumes an interleaved list with arity (\mu>1), that is L2/Paper C work, not part of the base L1 theorem. Likewise (q_{\rm line}) and (q_{\rm chal}) do not replace (q_{\rm gen}) in the locator entropy ledger.

---

## 3. Narrow monomial-prefix / generated-field route cut

For monomial-prefix words,

[
U_c(X)=X^s+\sum_{j=1}^{\sigma}(-1)^j c_jX^{s-j},
]

`prop:monomial-fiber` gives the exact identity

[
|\List(U_c,1-s/n)|=
#{S\in\binom Hs:\Phi_\sigma(S)=c}.
]

Since (H\subseteq B), every locator coefficient (e_j(S)) lies in (B). Therefore:

**BANKABLE_LEMMA — PROVED.**
Let (B\subseteq F), (H\subseteq B), and (c\in F^\sigma). Then the monomial-prefix fiber over (F) is empty unless (c\in B^\sigma). If (c\in B^\sigma), the fiber over (F) is exactly the same set as the fiber over (B):

[
{S:\Phi_\sigma(S)=c\text{ in }F^\sigma}
=======================================

{S:\Phi_\sigma(S)=c\text{ in }B^\sigma}.
]

So the ambient field (F) cannot pay the monomial-prefix entropy bill. The relevant field is exactly

[
q_{\rm gen}=|B|.
]

A slightly stronger arbitrary-(U) field-coordinate version also holds: if (F/B) has basis (\alpha_1,\ldots,\alpha_r) and

[
U=\sum_{i=1}^r \alpha_i U_i,\qquad U_i\in B[X],
]

then, because every (L_S\in B[X]),

[
\Fib_U^F(s)=\bigcap_{i=1}^r \Fib_{U_i}^B(s).
]

This proves the generated-field route cut: extension-valued received words do not enlarge the locator-fiber problem beyond base-field coordinate fibers. It does **not** prove the local limit over (B).

---

## 4. Counterexample to the arbitrary (\Fib_U) local-limit statement

The arbitrary locator-fiber statement fails for the simplest possible reason: if (U) is already a codeword, then every (s)-subset is a locator fiber.

Take any (U=P) with (\deg P<k), for example (U=0). For every (S\subseteq H) with (|S|=s>k),

[
U\bmod L_S=U,
]

because (\deg U<k<s=\deg L_S). Hence

[
\deg(U\bmod L_S)<k,
]

so

[
S\in \Fib_U(s).
]

Therefore

[
|\Fib_U(s)|=\binom ns.
]

At (s=k+\sigma) with (k\sim \rho n) and (\sigma=O(n/\log n)),

[
\binom n{k+\sigma}=2^{\HH(\rho)n-o(n)},
]

which is exponential in (n), not (n^{B_{\rm exp}}).

This survives quotient removal: choose (k=n/2-1) for (n=2^m). Then

[
\gcd(n,k)=\gcd(2^m,2^{m-1}-1)=1,
]

so the Paper B quotient-core profile is empty. The failure is not an active quotient-core contribution.

---

## 5. Concrete finite counterexample

Use:

[
p=97,\qquad B=F=\mathbb F_{97},\qquad n=16.
]

Let (g=5), a primitive element of (\mathbb F_{97}^\times), and

[
\omega=g^{6}=8.
]

Then (\omega) has order (16), and

[
H=\langle 8\rangle\subseteq\mathbb F_{97}^\times.
]

Choose

[
k=7,\qquad \rho=7/16,\qquad \sigma=4,\qquad s=k+\sigma=11.
]

Then

[
\delta=1-s/n=1-11/16=5/16,
]

and

[
\eta=\sigma/n=1/4,
\qquad
1-\rho-\eta=1-7/16-4/16=5/16.
]

The quotient profile is empty because

[
\gcd(n,k)=\gcd(16,7)=1.
]

Take the received word/interpolant

[
U(X)=0.
]

Then

[
|\Fib_0(11)|=\binom{16}{11}=4368.
]

For target exponent (B_{\rm exp}=2),

[
n^{B_{\rm exp}}=16^2=256,
]

so

[
|\Fib_0(11)|=4368>256.
]

The generated-field entropy inequality clears strongly:

[
\sigma\log_2 q_{\rm gen}
========================

4\log_2 97
\approx 26.40,
]

while

[
\log_2\binom{16}{11}
====================

\log_2 4368
\approx 12.09.
]

Thus even with (\varepsilon=1),

[
\sigma\log_2 q_{\rm gen}

>

(1+\varepsilon)\log_2\binom{16}{11}.
]

Verification pseudocode:

```python
from itertools import combinations
from math import comb, gcd, log2

p = 97
n = 16
omega = 8
H = [pow(omega, i, p) for i in range(n)]

k = 7
sigma = 4
s = k + sigma
B_exp = 2

assert len(set(H)) == n
assert pow(omega, n, p) == 1
assert all(pow(omega, d, p) != 1 for d in range(1, n))
assert gcd(n, k) == 1  # no active quotient-core divisor

count = 0
for S in combinations(H, s):
    # U = 0, so U mod L_S is 0 for every S
    deg_remainder_less_than_k = True
    if deg_remainder_less_than_k:
        count += 1

assert count == comb(n, s)
assert count == 4368
assert count > n**B_exp
assert sigma * log2(p) > 2 * log2(comb(n, s))
```

---

## 6. What exactly is false, and what is not false

False as written:

[
\forall U,\quad |\Fib_U(k+\sigma)|\le n^{B_{\rm exp}}.
]

This refutes:

* `conj:arbitrary-local`, as stated.
* `conj:final-locator`, as stated.
* `prob:L1`, as stated in the blueprint if (\Fib_U) is interpreted literally as in `def:locator-fiber`.

Not refuted:

* `conj:prefix-local`.
* `prop:monomial-fiber`.
* The generated-field entropy lower bound.
* The quotient-core lower bound.
* Any MCA or protocol statement.
* The actual list-size claim, because `prop:arb-fiber` only injects the list into a chosen subcollection of (\Fib_U(s)); it does not say every feasible (s)-subset should be counted as a distinct nearby codeword.

For (U=0), the list size is (1), but the raw locator fiber has size (\binom ns). The gap is pure contained-support overcounting.

---

## 7. EXACT_NEW_WALL and minimal repair

**EXACT_NEW_WALL — PROVED as a route obstruction.**
The arbitrary-word L1 target cannot bound the raw object (\Fib_U(s)). It must first quotient or prune contained supports.

A repairable object is the maximal-support locator fiber:

[
\MaxFib_U(s)
============

\left{
A_P={x\in H:U(x)=P(x)}:
\deg P<k,\ |A_P|\ge s
\right}.
]

Since (s>k), each support (A_P) determines (P) uniquely. Therefore

[
|\MaxFib_U(s)|=|\List(U,1-s/n)|.
]

For monomial-prefix (U_c), the agreement supports are already exact (s)-sets, because

[
U_c-P=L_S
]

has degree exactly (s). Thus the monomial-prefix local-limit problem remains the correct narrow first target.

**Minimal missing lemma after repair.**

A plausible repaired L1 lemma is:

[
|\MaxFib_U(k+\sigma)|\le n^{B_{\rm exp}}
]

for every (U), after generated-field entropy clears and quotient-periodic/maximal-support families are absent, removed, or budgeted.

Equivalently, in the monomial-prefix lane, the missing finite-field statement is still the quotient-separated aperiodic prefix local limit over (B=\mathbb F_{q_{\rm gen}}):

[
\max_{c\in B^\sigma}
#\left{
S\in\binom H{k+\sigma}:
\Phi_\sigma(S)=c,\ S\text{ aperiodic after quotient removal}
\right}
\le n^{B_{\rm exp}}.
]

That repaired local limit remains **CONJECTURAL**.
