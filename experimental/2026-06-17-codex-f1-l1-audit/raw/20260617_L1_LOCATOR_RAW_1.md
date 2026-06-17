## COUNTEREXAMPLE — formal status tag: COUNTEREXAMPLE

The arbitrary-word L1 locator-fiber statement in `slackMCA_v3.tex` is false as written. The obstruction is not a dimension count, not an MCA conversion, and not a quotient-core family: every low-degree received word has every (s)-subset as a feasible locator fiber.

This does **not** refute the monomial-prefix local-limit problem. It refutes the stronger arbitrary-(U) support-fiber formulation used by `conj:arbitrary-local`, `conj:final-locator`, and the Paper C-style `ass:locator` bridge unless the fiber object is repaired.

---

## 1. Exact `slackMCA_v3.tex` labels L1 depends on

Core definitions and bridges:

* `def:locator-fiber`: defines
  [
  \Fib_U(s)={S\subseteq H:\ |S|=s,\ \deg(U\bmod L_S)<k}.
  ]
* `prop:arb-fiber`: list size injects into feasible locator fibers.
* `prop:monomial-fiber`: for monomial-prefix words (U_c), lists are exactly prefix fibers (\Phi_\sigma^{-1}(c)).
* `def:taustar`: entropy threshold (\tau_\star(\rho,q)).

Necessary lower-bound ledger:

* `thm:pigeonhole`: coefficient pigeonhole lower bound.
* `cor:genfield-pigeonhole`: generated-field version; denominator is (q_{\rm gen}), not ambient (F).
* `cor:entropy-lower`: failure below entropy margin.
* `thm:qcore`: quotient-core list obstruction.
* `rem:corrected-reserve`: fixed exponent (B) needs (\sigma \gtrsim H(\rho)n/(B\log n)).
* `def:qprofile`: quotient-core profile (\mathcal Q_H(\eta)).
* `conj:listprofile`: quotient-profile corrected list entropy gap.

Known positive / partial lanes:

* `thm:upstairs`: characteristic-zero prefix fibers are quotient-periodic.
* `cor:upstairs-poly`: characteristic-zero prefix fibers are polynomial at (\sigma\ge Cn/\log n).
* `lem:galois-amp`: conjugate-prime amplification.
* `thm:no-collision`: finite-field no-collision above
  [
  p>\exp!\left(C n\log n/\sigma\right).
  ]
* `cor:quasipoly-upper`: monomial-prefix upper bound in quasi-polynomial split-prime fields.
* `rem:galois-limit`: explains why the norm route misses polynomial (q_{\rm gen}).

Conjectural L1 target labels:

* `conj:prefix-local`: monomial-prefix local limit with quotient exceptions.
* `conj:arbitrary-local`: arbitrary locator-fiber local limit.
* `thm:conditional-list`: conditional corrected list theorem, depending on the locator conjectures.
* `rem:subfield`: generated-field correction.
* `lem:pairwise`: pairwise/BCH information is insufficient.
* `conj:final-locator`: final locator local limit.

The exact L1 problem statement in the blueprint is `prob:L1`.

---

## 2. Restated L1 local-limit target with full ledger

Let
[
\mathbb F_p\subseteq B=\mathbb F_{q_{\rm gen}}\subseteq F,
]
where (B) is the generated field: the smallest field containing the evaluation domain (H) and hence all locator coefficients (e_j(S)). The ambient or protocol line/challenge field is (F), with (q_{\rm line}=q_{\rm chal}=|F|), but L1’s entropy denominator is (q_{\rm gen}=|B|).

Let

[
H\le B^\times,\qquad |H|=n=2^m,\qquad C_B=\mathrm{RS}[B,H,k],
]
[
k=\rho n+O(1),\qquad a=k+\sigma,\qquad \eta=\sigma/n,\qquad \delta=1-\rho-\eta.
]

The arbitrary locator target is:

[
|\Fib_U(a)|\le n^{B_L}
]
for every received word (U:H\to B), whenever

[
\sigma\ge C_{\rho,B_L,\varepsilon}\frac{n}{\log_2 n},
]
[
\sigma\log_2 q_{\rm gen}\ge (1+\varepsilon)\log_2\binom n{k+\sigma},
]
and the active quotient-core profile is absent, removed, or paid:

[
\mathcal Q_H(\eta)
==================

\max_{\substack{M\mid\gcd(n,k),\ \lceil \eta n\rceil<M\ k/M\le n/M-1}}
\log_2\binom{n/M-1}{k/M}
\le B_L\log_2 n+O(\log\log n).
]

Here (M) is the quotient-core subgroup order and (N=n/M) is the quotient order. This is separate from the MCA slack notation (1-\rho-t/N); L1 uses agreement slack (\sigma=a-k), not MCA slope slack (t).

For protocol arity, L1 is only the base-list (\mu=1) object. If a protocol consumes an interleaved list of arity (\mu), Paper C must separately prove or assume

[
|\Lambda(\mathrm{Int}(C_{\rm line},\mu),\delta)|\le \widehat L_\mu(\delta),
]
often via the trivial bound (\widehat L_\mu\le \widehat L_1^\mu). The implementation interleaving factor (\nu) is a separate protocol parameter and does not repair the generated-field entropy ledger.

---

## 3. Narrow monomial-prefix case

For monomial-prefix words,

[
U_c(X)=X^{k+\sigma}+\sum_{j=1}^{\sigma}(-1)^j c_j X^{k+\sigma-j},
\qquad c\in B^\sigma,
]
`prop:monomial-fiber` gives the exact identity

[
|\List(U_c,1-(k+\sigma)/n)|
===========================

|\Phi_\sigma^{-1}(c)|,
]
where

[
\Phi_\sigma(S)=(e_1(S),\dots,e_\sigma(S)).
]

In characteristic zero, `thm:upstairs` proves that equal prefix fibers are quotient-periodic, and `cor:upstairs-poly` gives polynomial size once (\sigma\ge Cn/\log n). In split prime fields, `thm:no-collision` and `cor:quasipoly-upper` transfer this only when

[
p>\exp!\left(C n\log n/\sigma\right).
]

At the corrected reserve (\sigma\asymp n/\log n), this requires

[
p>\exp(O((\log n)^2)),
]
so it does **not** reach (q_{\rm gen}=\mathrm{poly}(n)). The exact remaining monomial-prefix wall is therefore a fixed-prime, high-multiplicity, aperiodic prefix-fiber local limit after quotient classes are removed. Pairwise noncollision is too strong and not the right target.

---

## 4. Concrete finite counterexample to arbitrary L1

Take

[
B=F=\mathbb F_{17},\qquad q_{\rm gen}=q_{\rm line}=q_{\rm chal}=17,
]
[
H=\mathbb F_{17}^{\times},\qquad n=16,\qquad k=8,\qquad \rho=1/2.
]

Let

[
\sigma=4,\qquad a=s=k+\sigma=12,\qquad \eta=\sigma/n=1/4,\qquad \delta=1-\rho-\eta=1/4.
]

Use list exponent

[
B_L=2.
]

Entropy margin holds even with (\varepsilon=1/2):

[
\sigma\log_2 q_{\rm gen}
========================

4\log_2 17
\approx 16.350,
]
while

[
(1+\varepsilon)\log_2\binom{16}{12}
===================================

1.5\log_2(1820)
\approx 16.245.
]

The active quotient-core profile is harmless. Since

[
\gcd(n,k)=8,
]
the only divisor (M\mid \gcd(n,k)) with (\sigma<M) is (M=8). Then (N=n/M=2), (k/M=1), and

[
\binom{n/M-1}{k/M}
==================

# \binom{1}{1}

1,
]
so

[
\mathcal Q_H(\eta)=0\le B_L\log_2 n.
]

Now choose the received word

[
U(X)=0.
]

For every (S\subseteq H) with (|S|=12),

[
U\bmod L_S=0,
]
so

[
\deg(U\bmod L_S)<k.
]

Therefore

[
\Fib_U(12)=\binom{H}{12},
]
and hence

[
|\Fib_U(12)|=\binom{16}{12}=1820.
]

But the claimed L1-style bound with (B_L=2) would require

[
|\Fib_U(12)|\le n^{B_L}=16^2=256.
]

Thus

[
1820>256,
]
contradicting the arbitrary locator-fiber target.

This counterexample clears the generated-field entropy ledger and the quotient-core ledger. It fails solely because the arbitrary feasible-support fiber counts all (12)-subsets of the agreement set of a low-degree codeword.

Verification pseudocode:

```python
from itertools import combinations
from math import comb, log2

p = 17
H = list(range(1, p))          # F_17^*
n = 16
k = 8
sigma = 4
s = k + sigma
B_L = 2
eps = 0.5

assert s == 12
assert sigma * log2(p) > (1 + eps) * log2(comb(n, s))

# Quotient profile:
# divisors of gcd(16, 8) larger than sigma=4: only M=8
M = 8
N = n // M
assert comb(N - 1, k // M) == 1

# U = 0 is degree < k, so U mod L_S = 0 for every S.
fiber_count = sum(1 for S in combinations(H, s))
assert fiber_count == comb(16, 12)
assert fiber_count == 1820
assert fiber_count > n ** B_L
```

---

## 5. Infinite version, not a small-parameter artifact

For (\rho=1/2), fix any target exponent (B_L>0) and any proposed constant (C_{\rho,B_L,\varepsilon}). Choose a larger constant (C') satisfying

[
C'>C_{\rho,B_L,\varepsilon},\qquad
C'>(1+\varepsilon)H(1/2),\qquad
C'>H(1/2)/B_L.
]

Let

[
n=2^m,\qquad k=n/2,\qquad \sigma=\left\lceil C'\frac{n}{\log_2 n}\right\rceil,\qquad s=k+\sigma.
]

By Linnik’s theorem, there are primes (p\equiv1\pmod n) with (p\le n^{O(1)}). Let (H\le\mathbb F_p^\times) be the subgroup of order (n). Then (q_{\rm gen}=p=\mathrm{poly}(n)), and because (p\ge n+1),

[
\sigma\log_2 p
\ge
(C'+o(1))n

>

(1+\varepsilon)\log_2\binom n{k+\sigma}.
]

The quotient profile is also within the allowed polynomial budget: every active (M>\sigma) has

[
\frac nM \le \frac n\sigma
==========================

\frac{\log_2 n}{C'}(1+o(1)),
]
so

[
\log_2\binom{n/M-1}{k/M}
\le
\left(\frac{H(1/2)}{C'}+o(1)\right)\log_2 n
\le
B_L\log_2 n.
]

But for (U=0),

[
|\Fib_U(k+\sigma)|
==================

# \binom n{k+\sigma}

2^{H(1/2+o(1))n-o(n)},
]
which is exponential in (n), hence larger than (n^{B_L}) for all large (n).

So the arbitrary locator-fiber statement is asymptotically false even when (q_{\rm gen}=\mathrm{poly}(n)), entropy clears, and the quotient profile is paid.

---

## ROUTE_CUT

`prop:arb-fiber` is a valid one-way injection from list codewords to feasible supports, but the converse support count is too large for arbitrary received words. A uniform bound on (|\Fib_U(a)|) cannot be the missing L1 theorem.

The route

[
\text{arbitrary list size}
\le
|\Fib_U(a)|
\stackrel{?}{\le}
n^{B_L}
]
must be cut at the second inequality. It is false for (U\in C), already for (U=0).

A repair must replace arbitrary feasible (s)-subsets by a codeword-indexed or maximal-agreement object, for example

[
{P\in B[X]_{<k}: |{x\in H:U(x)=P(x)}|\ge a},
]
or by canonical/maximal agreement supports. The monomial-prefix case avoids this bug because `prop:monomial-fiber` is exact: (U_c-P=L_S) has degree exactly (s), so the agreement set is exactly (S).

---

## EXACT_NEW_WALL for the surviving monomial-prefix L1

After the arbitrary-fiber repair, the first real wall is still:

[
\textbf{Aperiodic prefix-fiber occupancy over polynomial generated fields.}
]

Minimal missing lemma:

[
\boxed{
\begin{minipage}{0.86\linewidth}
For (H\le B^\times) generated-field smooth of order (n=2^m), (q_{\rm gen}=|B|=\mathrm{poly}(n)), (k=\rho n+O(1)), (s=k+\sigma), and
[
\sigma\ge C_{\rho,B_L,\varepsilon}n/\log_2 n,\qquad
\sigma\log_2 q_{\rm gen}\ge(1+\varepsilon)\log_2\binom ns,
]
prove that every monomial-prefix fiber
[
\Phi_\sigma^{-1}(c)={S\in\binom Hs:(e_1(S),\dots,e_\sigma(S))=c}
]
has at most (n^{B_L}) aperiodic members after all quotient-periodic classes with (M>\sigma) are removed or charged to (\mathcal Q_H(\eta)).
\end{minipage}
}
]

The existing Galois/norm route cannot supply this at polynomial (q_{\rm gen}): after quotient removal, the proof of `thm:no-collision` still needs

[
q_{\rm gen}>\exp(Cn\log n/\sigma),
]
which becomes

[
q_{\rm gen}>\exp(O((\log n)^2))
]
at (\sigma\asymp n/\log n). That is quasi-polynomial, not polynomial.

So the bankable conclusion is:

[
\boxed{\text{COUNTEREXAMPLE to arbitrary L1 as written; monomial-prefix L1 remains open after quotient removal.}}
]
