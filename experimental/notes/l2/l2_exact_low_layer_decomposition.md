# L2 Exact Low-Layer Decomposition

- **Status:** PROVED exact decomposition / COUNTEREXAMPLE to omitting the
  low one-row layer.
- **Date:** 2026-07-12.
- **Scope:** Two-row Reed--Solomon lists. This note is self-contained and does
  not edit or promote Papers A--D.
- **Verifier:**
  `experimental/scripts/verify_l2_exact_low_layer_decomposition.py`.

## Novelty boundary

PR #675 proves the baseline-plus-excess recursion and identifies the high
anchor excess-codegree sum as the remaining two-row object. PR #658 defines an
explicit all-remainder quotient-packet budget; PRs #666 and #679 separate
completed rays from raw support multiplicity. Those results are inputs and are
not claimed here.

This note adds exactly two statements:

1. an exact decomposition which pays every completion whose opposite-row
   codeword has fewer than `tau(s)=2s-k+1` agreements by one global one-row
   layer `L_s(V)-L_tau(s)(V)`; and
2. a quotient-rank-two prime-field family showing that this low layer can be
   exponentially large even after retaining the complement shell, removing
   raw-support multiplicity, and granting deletion at the full explicit #658
   packet-budget capacity.

The remaining object is the post-packet **doubly-high** completed-pair
residual. No bound for that object is proved here.

## Definitions

Let

```text
C = RS[F_q,H,k],       |H|=n,
A_V(d) = {x in H : V(x)=d(x)},
L_t(V) = #{d in C : |A_V(d)|>=t},
tau(s) = 2s-k+1.
```

Set `L_t(V)=0` when `t>n`. For a row `W`, define its high anchors

```text
H_s(W) = {c in C : |A_W(c)|>=tau(s)}.
```

For `c in H_s(W)`, put

```text
B_c = A_W(c),             r_c = n-|B_c|,
Delta_c(V;s)
  = #{d in C : |A_V(d) intersect B_c|>=s,
                 s<=|A_V(d)|<=s+r_c-1}.
```

The doubly-high part is

```text
R_hh(V,W;s)
  = #{(d,c) in C x H_s(W) :
        |A_V(d) intersect B_c|>=s,
        tau(s)<=|A_V(d)|<=s+r_c-1}.
```

All counts are counts of actual codewords or completed codeword pairs, not
raw support witnesses.

## Exact low-layer theorem

**Theorem.** For every `k<=s<=n`,

```text
sum_{c in H_s(W)} Delta_c(V;s)
  <= L_s(V)-L_tau(s)(V) + R_hh(V,W;s).                 (1)
```

**Proof.** Partition the pairs counted on the left according to
`t=|A_V(d)|`. The pairs with `t>=tau(s)` are exactly those counted by
`R_hh`.

Now fix a codeword `d` with

```text
s <= t <= tau(s)-1 = 2s-k.
```

If two distinct high anchors `c,c'` both complete `d`, then each of
`A_V(d) intersect B_c` and `A_V(d) intersect B_c'` has size at least `s`.
Their intersection therefore has size at least

```text
2s-t >= k.
```

On these points both `c` and `c'` equal `W`. Two degree-`<k` polynomials
agreeing at `k` evaluation points are equal, a contradiction. Thus each such
`d` is completed by at most one high anchor. The number of possible `d` is
exactly `L_s(V)-L_tau(s)(V)`, proving (1). QED.

## Four-term two-row compiler

For a fixed `B subseteq H` with `r=n-|B|`, define

```text
Gamma_B(V;s) = #{d in C : |A_V(d) intersect B|>=s}.
```

Removing at most `r` coordinates gives the exact split

```text
Gamma_B(V;s) = L_{s+r}(V) + Delta_B(V;s).              (2)
```

Indeed, every codeword with at least `s+r` total agreements belongs to
`Gamma_B`, while the remaining members of `Gamma_B` are precisely the
displayed `Delta_B` interval.

Combining (1), (2), and the baseline/high-anchor inequality of PR #675 gives

```text
Lambda_2(V,W;s)
 <= L_s(W)
    + sum_{c in H_s(W)} max(L_{s+r_c}(V)-1,0)
    + (L_s(V)-L_tau(s)(V))
    + R_hh(V,W;s).                                    (3)
```

The four terms have distinct roles:

1. the free baseline completion;
2. the complement-size one-row shell;
3. the global low exact one-row layer; and
4. the genuinely doubly-high completed-pair residual.

Only the fourth term is eligible for a quotient-packet / completed-ray
first-match theorem after the first three literal one-row terms are retained.

## Rank-two exact-layer obstruction

Let `q` tend to infinity through odd primes and put

```text
h = log_2 q,      n=q-1,      H=F_q^*,      k=n/2,
sigma = ceil(3n/(4h)),
a = k+sigma,      tau(a)=k+2sigma+1.
```

For all sufficiently large `q`, there exist rows `V,W` of quotient rank two
in `F_q^H/C` with a unique high anchor and

```text
Delta_{H\{x}}(V;a) >= ((n-a-1)/(n-1))
  binom(n,a) q^(-sigma) (1-q^(-1))^(n-a)               (4)

and hence

Delta_{H\{x}}(V;a) >= 2^(n/4-O(n/h^2)-O(h)).           (5)
```

Every pair counted in (4) has exactly `a` common agreement points. It has one
exact-`a` support and gives a distinct completed codeword pair. Thus neither
support deduplication nor completed-ray deduplication removes the family.

### Construction and proof

For a uniformly random word `V`, let

```text
N_a(V) = #{d in C : |A_V(d)|=a}.
```

For each fixed codeword, the agreement count is `Bin(n,1/q)`, so

```text
E N_a(V) = binom(n,a) q^(-sigma) (1-q^(-1))^(n-a).     (6)
```

Choose `V` with `N_a(V)>=E N_a(V)`. Such a `V` is not a codeword: a
codeword has agreement `n` with itself and at most `k-1<a` with every other
codeword, so its exact-`a` layer is empty.

For `x in H`, let `D_x(V)` count the exact-`a` codewords missing coordinate
`x`. Then

```text
sum_x D_x(V) = (n-a)N_a(V).                            (7)
```

The projective quotient classes `[e_x]` are nonzero and pairwise distinct.
Otherwise a nonzero word of weight at most two would lie in the RS code,
contradicting its minimum distance `n-k+1>2`. Hence at most one `[e_x]` lies
on the quotient line spanned by `[V]`. Excluding that coordinate and averaging
(7), choose `x` with

```text
[e_x] notin <[V]>,
D_x(V) >= ((n-a-1)/(n-1))N_a(V).                       (8)
```

Set `W=e_x`. Then `[V],[W]` have quotient rank two. The zero codeword agrees
with `W` on `B=H\{x}`. Every nonzero codeword agrees with `W` at at most
`k` points, while `a>k`; for large `q`, `tau(a)<=n-1`. Thus zero is the
unique threshold-`a` and threshold-`tau(a)` anchor.

Since `r=1`, the residual interval `[a,a+r-1]` is the singleton `{a}` and

```text
Delta_B(V;a) = D_x(V),                                 (9)
Lambda_2(V,W;a) = Gamma_B(V;a)
                  = L_{a+1}(V)+Delta_B(V;a).            (10)
```

Equations (6), (8), and (9) prove (4). Also

```text
a/n = 1/2 + 3/(4h) + O(1/n),
log_2 binom(n,a) = n-O(n/h^2)-O(log n),
3n/4 <= h sigma <= 3n/4+h,
```

and `(1-q^(-1))^(n-a)` is bounded below by a positive constant. This proves
(5).

## Survival under the explicit quotient budget

For the all-remainder `mu=2` packet budget of PR #658, the aligned endpoint
at an active divisor `M` is at most `2^Q`, where `Q=n/M-1`.

At threshold `a`, every active `M` satisfies `M>sigma`, so

```text
Quot_rem,2(n,k,a) <= n 2^(n/sigma) = O(n^(7/3)).       (11)
```

At threshold `tau(a)`, the slack is `2sigma+1`, giving

```text
Quot_rem,2(n,k,tau(a))
  <= n 2^(n/(2sigma+1)) = O(n^(5/3)).                  (12)
```

The simultaneous random term satisfies

```text
binom(n,a) q^(-2sigma)
  <= 2^(n-2h sigma) <= 2^(-n/2).                       (13)
```

Consequently the family in (5) survives deletion of the two explicit packet
budgets even if every packet is granted an arbitrary `exp(o(n))` completed-
pair fiber. The obstruction is the third term of (3), not the complement
shell or `R_hh`.

This is an adversarial capacity grant, stronger than literal budget
subtraction. It does not construct a canonical #658 owner map and does not
claim that the displayed pairs are quotient-free.

## Ledger impact

The theorem is an exact finite decomposition for every RS instance. The
counterexample is an explicit parameter family with an existence-chosen row
`V`; it does not instantiate the deployed Grand List row.

Asymptotically, the missing low layer has exponent at least `1/4-o(1)`, while
the displayed quotient budgets are polynomial. It therefore cannot be hidden
inside `exp(o(n))` loss.

The remaining Grand List wall is now the post-packet doubly-high residual:

```text
R_hh after actual completed-pair first-match deletion.
```

A closing theorem must bound that object by the literal random term plus an
explicit finite remainder, while the three one-row terms in (3) are evaluated
at every active threshold-ladder node.

## Nonclaims

This note does not claim:

- a flaw in PR #658, #666, #675, or #679;
- a counterexample after the low layer `L_s(V)-L_tau(s)(V)` is retained;
- a bound for the post-packet doubly-high residual;
- a uniform one-row list theorem;
- an official Grand List or Grand MCA threshold;
- a deployed certificate `U(a0+1)<=B*<L(a0)`;
- either official Proximity Prize question.

## Verification

The standard-library verifier exhausts every pair of received words for
`RS[F_5,F_5^*,2]`, checks (1)--(3) at every active threshold, checks the exact
shell split (2), exercises the unit-anchor agreement facts, and verifies
the asymptotic arithmetic on increasing prime rows.

```bash
python3 experimental/scripts/verify_l2_exact_low_layer_decomposition.py --check
python3 experimental/scripts/verify_l2_exact_low_layer_decomposition.py --tamper-selftest
```
