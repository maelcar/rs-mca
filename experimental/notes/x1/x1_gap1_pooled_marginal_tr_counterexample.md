# GAP-1 pooled-marginal terminal reserve counterexample

- **Author:** Manuel E. Rey-Álvarez Zafiria
- **Status:** COUNTEREXAMPLE
- **Source alignment:** repository commit `c35a6da31ed0905afcbaaefe4eb0f242572ebb35`
- **Target:** literal Conjecture TR in
  `experimental/notes/roadmaps/gap1_terminal_reserve.md`
- **Verifier:**
  `experimental/scripts/verify_gap1_tr_pooled_marginal_counterexample.py`
- **Certificate:**
  `experimental/data/certificates/gap1-tr-pooled-marginal-counterexample/gap1_tr_pooled_marginal_counterexample.json`

## Claim

The literal pooled-marginal form of Conjecture TR is false.  There is no
absolute exponent `B_TR` for which

```text
product_{r in R} |A_r(w,A,M,alpha)|
  <= n^B_TR * max(1, C(n,n-A) q^(1-(A-k)))
```

holds uniformly under the quantifiers printed in the terminal-reserve note.
The obstruction is not a large genuine joint image.  It is the Cartesian
product created after per-character values from different codewords have been
pooled independently.

More precisely, for arbitrarily large odd primes `M` there is an admissible
row with

```text
q = 3^(M-1),  n = 2M,  k = M-5,  A = M,
```

a received word `w`, and an active set `R` of size `k` such that

```text
product_{r in R} |A_r(w,A,M,1)| >= 2^(M-5),
FM(A) < 1,
n^3 FM(A) < 1,
```

while `A` lies at least two agreement steps beyond the relevant crossing under
either convention used in the source notes.  Consequently the left-hand side
eventually exceeds `n^B` for every fixed `B`.

## Construction

Fix a sufficiently large odd prime `M` and put

```text
q = 3^(M-1),  n = 2M,  k = M-5,  A = M.
```

Fermat's theorem gives `M | q-1`.  Since `M` is odd and `q-1` is even,
`2M | q-1`.  Hence `F_q^*` contains a cyclic subgroup

```text
H_n = <omega>,  |H_n|=2M.
```

Let `K_M=<omega^2>`.  The domain is the disjoint union of its two
`K_M`-cosets

```text
H_n = S_0 disjoint_union S_1.
```

For `a in F_q^*`, define

```text
h_a(X) = 1 + X + ... + X^(k-2) + a X^(k-1).
```

For each `x in H_n`, the equation `h_a(x)=0` excludes at most one value of
`a`, because `x^(k-1)` is nonzero.  Thus at most `2M` values are excluded.
For all sufficiently large `M`, `q-1>2M`, so one may choose `a!=0` for which
`h_a` has no zero on `H_n`.  Every coefficient of `h_a` is then nonzero.

Set

```text
c_0 = h_a,  c_1 = 2 h_a,
w(x) = c_0(x) for x in S_0,
w(x) = c_1(x) for x in S_1.
```

The field has characteristic three, so `c_0!=c_1`.  Since `h_a` is nonzero
at every domain point,

```text
Agr(c_0,w)=S_0,  Agr(c_1,w)=S_1
```

exactly.  Both supports are `K_M`-stable and have size `A=M`.

## Pooled marginals

Use the admissible tower `B=K=F_q`, take `alpha=1`, and let

```text
R={0,...,k-1}.
```

Because `k<M`, each `r`-isotypic part of `c_0` is the single monomial
`b_r X^r`, where `b_r!=0`; for `c_1` it is `2b_r X^r`.  Therefore every
pooled marginal contains two distinct values:

```text
A_r(w,A,M,1) contains {b_r,2b_r}.
```

It follows that

```text
product_{r in R}|A_r(w,A,M,1)| >= 2^k = 2^(M-5).
```

The genuine joint tuple set contributed by the two displayed codewords has
only two points.  In fact these are the only qualifying codewords.  A
`K_M`-stable subset of `H_n` of size at least `M` is `S_0`, `S_1`, or `H_n`.
Agreement on either `S_i` determines a degree-`<k` polynomial uniquely because
`M>k`, while agreement on all of `H_n` would force the same polynomial to be
both `c_0` and `c_1`.

## Corridor check

Write

```text
FM(A') = C(2M,2M-A') q^(1-(A'-k)).
```

At `A_2=k+2=M-3`,

```text
FM(A_2)=C(2M,M+3)/q.
```

The estimates

```text
C(2M,M) >= 4^M/(2M+1),
C(2M,M+3) >= C(2M,M)/8
```

show that `FM(A_2)>1` for all sufficiently large `M`.  At
`A_3=k+3=M-2`,

```text
FM(A_3)=C(2M,M+2)/q^2 <= 9(4/9)^M < 1.
```

Thus the first agreement with `FM<1` is `M-2`.  If that first-below level is
called `A*`, then `A=M=A*+2`.  Under the offset convention used by the pinned
terminal row, `A*=M-3` and `A=A*+3`.  The literal condition `A>=A*+2` holds in
either convention.

At the chosen agreement `A=M`, one has `A-k=5` and

```text
FM(A)=C(2M,M)/q^4 <= 81(4/81)^M.
```

Hence `FM(A)<1` and `(2M)^3 FM(A)<1` for all sufficiently large `M`.

## Failure of every polynomial reserve

For every fixed real `B`,

```text
2^(M-5)/(2M)^B -> infinity.
```

The pooled-marginal product is therefore larger than
`n^B max(1,FM(A))=n^B` for all sufficiently large prime `M`.  No absolute
`B_TR` can satisfy the displayed pooled-marginal conjecture.

## Corrected object

This counterexample does not refute a reserve theorem for the genuine joint
image

```text
J_R(w) = {
  (alpha^r G_r(beta))_{r in R} :
  one qualifying codeword c
}.
```

For the construction above, `|J_R(w)|=2` while the pooled product is `2^k`.
A viable terminal statement must preserve codeword/support identity, for
example by bounding `|J_R(w)|` or by summing support-stratified joint images.

## Exact finite replay

The verifier includes an exhaustive instance over `F_337` with

```text
M=7, n=14, k=2, A=7.
```

It enumerates all `337^2=113569` degree-`<2` codewords and finds exactly the
two planted qualifying stable codewords.  It independently checks the domain
orders, exact agreement supports, Fourier/isotypic values, both crossing
conventions, and the exact `FM` fractions.  The result is

```text
joint tuple count              2
pooled marginal product        4
n^3 FM(A)                      9417408/12897917761 < 1
```

Run from the repository root:

```bash
python experimental/scripts/verify_gap1_tr_pooled_marginal_counterexample.py
```

The script regenerates the canonical JSON certificate and exits nonzero if
any source-alignment, arithmetic, enumeration, or status check fails.

## Scope

This result refutes only the literal product of independently pooled
per-character marginals.  It does not refute the tower product theorem, a
joint-tuple terminal reserve, a support-stratified reserve, the base
`PrimitiveExactList` target, or any promoted Paper A--D theorem.
