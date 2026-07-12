# L2 Sharp Excess-Codegree Recursion

- **Status:** PROVED exact reduction / script-verified.
- **Date:** 2026-07-12.
- **Scope:** Finite fixed-arity interleaved Reed--Solomon lists. This note does
  not edit or promote Papers A--D.
- **Verifier:**
  `experimental/scripts/verify_l2_sharp_excess_codegree_recursion.py`.

## Novelty boundary

The following inputs are already proved in
`l2_sharp_target_conjecture.md` and are not new here:

1. arbitrary invertible row operations and codeword translations preserve the
   literal common-column interleaved list;
2. the list depends only on the received-row span in `F_q^H/C`;
3. quotient rank `r` reduces an arity-`mu` list exactly to an `r`-row list;
4. repeated, proportional, and codeword-translated rows are rank-one cases.

The existing `l2_codegree_reduction_theorem.md` also proves a valid but looser
peel with tail threshold `2s-k` and coefficient `L_s`.

This note claims only the following new refinement and its consequences:

- the first possible nonunique tail is `2s-k+1`;
- the tail coefficient is the excess `L_s-1` above the baseline completion;
- the two-row remainder is a literal high-anchor excess-codegree sum;
- minimizing the sharp peel over quotient flags gives a basis-free dynamic
  `P_s(S)`;
- replacing row profiles by their maximum gives the exact recurrence `B_r` and
  threshold ladder `s_t=k-1+2^t(s-k+1)`.

## Setup

Let `C=RS[F_q,H,k]`, where `H` consists of `n` distinct evaluation points,
`1<=k<=n`, and let `k<=s<=n`. For a received row `V in F_q^H` and `c in C`, put

```text
A_V(c) = {x in H : c(x)=V(x)},
L_s(V) = #{c in C : |A_V(c)|>=s}.
```

For a `j`-row received word `U=(U_1,...,U_j)`, put

```text
Lambda_j(U;s)
  = #{(c_1,...,c_j) in C^j :
      |intersection_i A_{U_i}(c_i)|>=s}.
```

Write `W=F_q^H/C`. The already-proved row-affine invariance makes

```text
ell_s(v) = L_s(V),       v=[V] in W,
```

well-defined; for nonzero `alpha`, `ell_s(alpha v)=ell_s(v)`.

Define

```text
tau(s)  = 2s-k+1,
eta_s(v)  = 1 if ell_s(v)>0, and 0 otherwise,
beta_s(v) = ell_s(v)-eta_s(v) = max(ell_s(v)-1,0).
```

## Sharp baseline-plus-excess theorem

**Theorem.** Let `j>=2` and write `U=(V,U_2,...,U_j)`. Then

```text
Lambda_j(U;s)
 <= eta_s([V]) Lambda_{j-1}(U_2,...,U_j;s)
    + beta_s([V]) Lambda_{j-1}(U_2,...,U_j;tau(s)).       (1)
```

If `L_s(V)>0`, this is

```text
Lambda_j(U;s)
 <= Lambda_{j-1}(U_2,...,U_j;s)
    + (L_s(V)-1) Lambda_{j-1}(U_2,...,U_j;2s-k+1).        (2)
```

**Proof.** Fix a tail tuple `c_tail=(c_2,...,c_j)` and let

```text
S_tail = intersection_{i=2}^j A_{U_i}(c_i),
N       = |S_tail|,
d       = #{c_1 in C : |A_V(c_1) intersection S_tail|>=s}.
```

Suppose `s<=N<=2s-k`. If `c_1` and `c_1'` are two completions, their two
agreement subsets inside `S_tail` overlap in at least

```text
2s-N >= k
```

points. Both codewords equal `V` there, so two degree-`<k` polynomials agree at
at least `k` distinct evaluation points and are equal. Thus `d<=1` throughout
this range. The first integer support size at which nonuniqueness is not ruled
out is therefore `N>=2s-k+1`.

Summing over tail tuples gives

```text
Lambda_j(U;s)
 <= Lambda_{j-1}(U_2,...,U_j;s)
    + sum_{c_tail:N>=tau(s)} max(d-1,0).                  (3)
```

The first term pays one baseline completion for every tail tuple, including an
overpayment when no completion exists. Every completion belongs to the one-row
list of `V`, so `d<=L_s(V)`. If that list is empty, the left side is zero. If it
is nonempty, `max(d-1,0)<=L_s(V)-1`, and the number of high-tail tuples is
`Lambda_{j-1}(U_2,...,U_j;tau(s))`. This proves (1) and (2). The decomposition
is an upper bound, not an exact partition when the baseline overpays a
zero-completion tuple. QED.

## Two-row excess codegree

For a row `W`, a codeword `c`, and its full agreement support `A_W(c)`, define

```text
Gamma_{A_W(c)}(V;s)
  = #{d in C : |A_V(d) intersection A_W(c)|>=s}.
```

The proof above gives the source-facing bound

```text
Lambda_2(V,W;s)
 <= L_s(W)
    + sum_{c:|A_W(c)|>=2s-k+1}
        max(Gamma_{A_W(c)}(V;s)-1,0).                    (4)
```

Consequently, if `L_s(V)>0`,

```text
Lambda_2(V,W;s)
 <= L_s(W)+(L_s(V)-1)L_{2s-k+1}(W).                     (5)
```

Equation (4) identifies the unresolved object exactly: the payment is the
excess above one free completion on high anchors, not the entire punctured
list and not the full Cartesian product.

## Basis-free quotient-subspace dynamic

For a quotient subspace `S<=W`, define `P_s(S)` recursively. If `s>n`, set
`P_s(S)=0`. For `k<=s<=n`, set

```text
P_s(0) = 1.
```

If `dim S=1`, set `P_s(S)=ell_s(v)` for any nonzero `v in S`. If `dim S=r>=2`,
set

```text
P_s(S)
 = min_{T<S, dim T=r-1; v in S\T}
     [eta_s(v) P_s(T)+beta_s(v) P_{tau(s)}(T)].          (6)
```

**Corollary.** If the received rows span `S(U)<=W`, then

```text
Lambda_mu(U;s) <= P_s(S(U)).                            (7)
```

**Proof.** The cases `dim S=0,1` are the already-known exact quotient-rank
reduction. For `dim S>=2`, choose any quotient hyperplane `T` and complement
vector `v`, lift a basis of `T` together with `v`, apply (1), and use induction
at thresholds `s` and `tau(s)`. The result holds for every such choice, so the
minimum in (6) is valid. Because (6) uses only the quotient subspace and its
one-row profiles, `P_s(S)` is independent of the printed row basis. QED.

For a fixed ordered quotient basis, repeatedly applying (1) gives at most
`2^(r-1)` branch terms. Every high-tail branch replaces the current threshold
by `tau`, while every baseline branch leaves it unchanged. Starting from
`s_0=s`, the thresholds are

```text
s_{t+1}=2s_t-k+1,
s_t=k-1+2^t(s-k+1).                                    (8)
```

For `s=a=k+sigma`, this is `s_t=k-1+2^t(sigma+1)`; in particular the rank-two
tail begins at `k+2sigma+1`.

## Parameter-only envelope

For `k<=s<=n`, put

```text
L(s)=max_{V in F_q^H} L_s(V),
```

and put `L(s)=0` for `s>n`. Set `B_r(s)=0` for every `r` when `s>n`. For
`k<=s<=n`, define

```text
B_1(s)=L(s),
B_r(s)=B_{r-1}(s)+(L(s)-1)B_{r-1}(2s-k+1)   (r>=2).     (9)
```

Then every received word of quotient rank `r>=1` satisfies

```text
Lambda_mu(U;s) <= B_r(s) <= B_mu(s).                    (10)
```

Rank zero has list size one for `s<=n`, while `B_mu(s)>=1`, so the uniform
fixed-arity bound is

```text
max_U Lambda_mu(U;s) <= B_mu(s).                        (11)
```

**Proof.** For `s<=n`, every quotient-vector profile satisfies
`eta_s(v)<=1` and `beta_s(v)<=L(s)-1`. Apply (1), use induction on quotient
rank at thresholds `s` and `2s-k+1`, and obtain (9). Also `L(s)>=1`, since a
codeword received word has a one-row list of size one. Therefore

```text
B_r(s)-B_{r-1}(s)
  = (L(s)-1)B_{r-1}(2s-k+1) >= 0,
```

which proves `B_r(s)<=B_mu(s)` for `r<=mu`. The rank-zero assertion then gives
(11). QED.

This is an exact finite recurrence. It becomes an asymptotic theorem only after
uniform estimates for the one-row profiles `L(s_t)` are supplied.

## Literal denominator

Let `D_list` denote the actual field cardinality or other denominator printed
by the list/protocol ledger. Keep it distinct from the generated field unless a
separate theorem identifies them. Since list sizes are integers,

```text
N <= 2^-128 D_list
  iff
N <= floor(D_list/2^128).                               (12)
```

Thus (7), (10), or (11) gives a sufficient list certificate only after the
corresponding integer bound is compared with `floor(D_list/2^128)`. This note
does not instantiate `D_list` or prove that it equals a challenge, line, or
generated field.

## Source compiler and remaining wall

The compiler is direct:

```text
literal common-column list
 -> already-known quotient row span S(U)
 -> baseline/high-tail split
 -> one-row profiles and excess punctured codegrees
 -> P_s(S) or B_r(s)
 -> floor(D_list/2^128).
```

No first-match atlas is needed for the raw inequality. Any future subtraction
of quotient packets must introduce a canonical first-match order and prove
disjoint charging before inserting a quotient-removed excess term into (4).
The next load-bearing inputs are therefore:

1. a uniform rank-one bound for `L_a(V)` at every active ladder threshold; and
2. a quotient-removed bound for the high-anchor excess sum in (4), or a
   counterexample to such a bound.

## Nonclaims

This note does not claim:

- row-span invariance or effective-rank collapse as new;
- that quotient rank alone controls list size;
- a uniform one-row list theorem;
- decay of quotient-periodic or common-support tails;
- a quotient-packet first-match compiler or excess-codegree payment;
- a numerical value or field identification for `D_list`;
- a growing-arity theorem;
- an asymptotic Grand List threshold;
- a Grand MCA theorem;
- a finite deployed safe/unsafe crossing;
- either official prize question.

## Verification

The standalone standard-library verifier checks exhaustive small RS instances,
the new constants, the basis-free rank-two dynamic, repeated/proportional and
codeword-translated rows, random invertible row operations, a realized RS
`K_{2,2}` equality case, and negative controls:

```bash
python3 experimental/scripts/verify_l2_sharp_excess_codegree_recursion.py --check
python3 experimental/scripts/verify_l2_sharp_excess_codegree_recursion.py --tamper-selftest
```
