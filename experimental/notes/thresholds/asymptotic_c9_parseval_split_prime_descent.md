# Parseval-sharp split-prime dyadic resultant descent

Status: `PROVED / STRICT_SUBREGIME`.

Paper B already proves a Galois-amplified split-prime norm descent in
`tex/slackMCA_v4.tex`, `thm:no-collision`.  This note does not claim a new
descent route.  It sharpens one dyadic step by using the exact odd-root
Parseval identity, producing explicit polynomial-prime thresholds.  At the
half-window endpoint the clean consequence is

```text
R=N/2, p>2N: every pure-weight fixed-weight fiber has size at most 2.
```

The theorem is pointwise and accepts every Boolean mask satisfying the stated
cyclic map hypotheses.  It does not prove that every primitive residual has
that form.

## 1. Finite descent theorem

Let

```text
N=2^s, N | p-1, p prime,
t_i=alpha zeta^i, 0<=i<N,
```

where `zeta in F_p^x` has order `N`.  Fix `alpha,c in F_p^x`,
`a in Z/NZ`, and `1<=R<=N/2`.  Let

```text
rho_i = c u_i zeta^(a i),
v_i   = rho_i (1,t_i,...,t_i^(R-1)),
Phi(x)= sum_i x_i v_i.
```

Assume each `u_i in F_p^x` has an integer lift `tilde u_i` with
`|tilde u_i|<=B`.  Put `n_j=N/2^j`.

### Theorem 1 (Parseval-sharp dyadic descent)

Fix `0<=J<=s-1`.  Suppose that for every `0<=j<J`,

```text
p^floor(R/2^(j+1)) > (2 B^2 n_j)^(n_j/4).               (1)
```

Let `Omega subseteq {0,1}^N`.  If `x,x^(0)` lie in one fiber of
`Phi|_Omega`, then the integer collision word

```text
b_i = tilde u_i (x_i-x_i^(0))
```

is constant on every residue class modulo `n_J`:

```text
b_(i+n_J)=b_i.                                           (2)
```

Consequently,

```text
max_y |Omega intersect Phi^(-1)(y)| <= 2^n_J.            (3)
```

If `u_i=1` and `Omega` lies in one Hamming-weight slice, then

```text
max_y |Omega intersect Phi^(-1)(y)|
    <= binom(n_J,floor(n_J/2)).                           (4)
```

In that pure-weight case, the positive and negative parts of every collision
are unions of equal numbers of residue classes modulo `n_J`.  Thus their
split locator polynomials are quotient-periodic.

## 2. The resultant estimate

Let `n=2^r>=2`, put

```text
C_n(X)=X^(n/2)+1=Phi_n(X),
```

and let `f(X)=sum_{i=0}^{n-1} b_iX^i in Z[X]` with `|b_i|<=B`.
Because `p` is congruent to `1` modulo `n`, `C_n` splits into distinct linear
factors over `F_p`.

### Lemma 2 (split resultant dichotomy)

If the reduction of `f` vanishes at `q` distinct primitive `n`th roots in
`F_p`, then either `C_n` divides `f` in `Z[X]`, or

```text
p^q <= |Res(C_n,f)| <= (2 B^2 n)^(n/4).                  (5)
```

### Proof

Every primitive root modulo `p` lifts uniquely to a root of `C_n` in
`Z_p`.  A prescribed modular zero makes the corresponding factor in

```text
Res(C_n,f)=product_{C_n(xi)=0} f(xi)
```

divisible by `p`.  A nonzero resultant therefore has `p`-adic valuation at
least `q`, proving the lower bound.

Let `omega=exp(2 pi i/n)`.  Odd-frequency orthogonality gives the exact
identity

```text
sum_{k odd} |f(omega^k)|^2
  = (n/2) sum_{i=0}^{n/2-1} (b_i-b_(i+n/2))^2.           (6)
```

The mean square over the `n/2` odd roots is at most `2B^2n`.  Applying
AM--GM to the squared absolute values proves the upper bound in (5).

Finally, `C_n` is irreducible over `Q`.  An elementary check is to translate
by `1`: modulo `2`, `C_n(X+1)=X^(n/2)`, while its integer constant term is
`2`.  A nontrivial monic factorization would make both factor constant terms
even, a contradiction.  Thus a zero resultant forces `C_n|f` over `Q`, and
monicity gives divisibility in `Z[X]`.

## 3. Proof of Theorem 1

Fix a fiber base point `x^(0)` and form

```text
f_0(X)=sum_i tilde u_i(x_i-x_i^(0))X^i.
```

Equality of the `R` syndrome coordinates says that the reduction of `f_0`
vanishes at the consecutive cyclic frequencies

```text
I_0={a,a+1,...,a+R-1} mod N.                             (7)
```

At scale `n_j`, let `I_j` contain those `k mod n_j` for which
`2^j k in I_0 mod N`.  The number `q_j` of odd members of `I_j` satisfies

```text
q_j >= floor(R/2^(j+1)).                                 (8)
```

Inductively let `f_j` have degree below `n_j`, coefficient height at most
`B`, and vanish on `I_j`.  By (1), (8), and Lemma 2, the nonzero-resultant
alternative is impossible.  Hence

```text
f_j(X)=(1+X^(n_j/2))f_(j+1)(X).                          (9)
```

The quotient has degree below `n_j/2` and its coefficients are the first half
of those of `f_j`, so its height remains at most `B`.  If `2k in I_j`, then

```text
0=f_j(zeta_j^(2k))=2f_(j+1)(zeta_(j+1)^k) mod p,
```

where `zeta_j=zeta^(2^j)`.  Since `p` is odd, the required zeros transfer to
the next scale.

Multiplying (9) through level `J-1` gives

```text
f_0(X)=(1+X^n_J+...+X^(N-n_J))f_J(X),                   (10)
```

which is exactly the periodicity in (2).

For each residue class, its common collision coefficient lies in the
intersection of two-point sets of the form `{0,tilde u_i}` or
`{0,-tilde u_i}`.  That intersection contains at most one nonzero integer.
Once the common coefficient is fixed, every bit in the class is fixed.  There
are `n_J` classes, proving (3).

When `u_i=1`, a class can change only if the base point is all zero or all one
on that class.  Fixed weight requires the same number of all-zero classes to
be added as all-one classes are removed.  If their counts are `z,o`, the
number of choices is at most

```text
sum_l binom(z,l)binom(o,l)=binom(z+o,z)
    <= binom(n_J,floor(n_J/2)),
```

which proves (4).

## 4. Explicit large-prime consequences

Fix `0<kappa<=1/2` and `0<tau<1`, and assume `R>=kappa N`.  If

```text
p > (2 B^2 N)^[1/(2 kappa(1-tau))],                     (11)
```

descend until the first dyadic scale `n_*<=2/(kappa tau)`.  While
`n_j>2/(kappa tau)`,

```text
floor(R/2^(j+1))
  >= floor(kappa n_j/2)
  > (1-tau)kappa n_j/2.
```

Raising (11) to this integer exponent proves (1).  Therefore

```text
max_y |F_y| <= 2^n_* <= 2^ceil(2/(kappa tau)),           (12)
```

with the central-binomial replacement for pure fixed-weight fibers.

At the half-window endpoint, `R=N/2` and

```text
floor(R/2^(j+1))=n_j/4.
```

Thus (1) is exactly `p>2B^2n_j`.  The single condition

```text
p>2B^2N                                                     (13)
```

pays every level down to `n_*=2`, giving

```text
max_y |F_y| <= 4                                           (arbitrary mask),
max_y |F_y| <= 2                                           (u_i=1, fixed weight). (14)
```

The pure weights include the unweighted row, every shifted monomial window,
and the exact dual normalization

```text
1/P_T'(t_i)=t_i/(N alpha^N).
```

For any nonempty exact cyclic residual independently certified to have these
hypotheses, an `O(1)` pointwise fiber bound implies image-normalized primitive
Q and C9 because `barN=M/L>=1`.

## 5. Relation to the existing descent

- `tex/slackMCA_v4.tex`, `thm:upstairs`, already proves characteristic-zero
  quotient periodicity and the corresponding fiber count.
- `tex/slackMCA_v4.tex`, `lem:galois-amp` and `thm:no-collision`, already prove
  split-prime norm amplification and recursive quotient extraction under
  `p>exp(C_1 n log(2n)/sigma)`.
- `experimental/notes/roadmaps/x30_finite_p_norm_gate.md` already states the
  exact descent-or-norm-gate dichotomy.  Lemma 2 pays that norm gate by an
  explicit Parseval bound when (1) holds.
- PR #444 supplies distance/Plotkin bounds; this note instead forces exact
  quotient periodicity.
- PR #451 covers the orthogonal Frobenius-expanding coefficient-field regime.
  Frobenius is inert in the present split-prime class.
- PR #448 concerns signed elementary-symmetric moment routes, not this
  pointwise consecutive-zero resultant estimate.

The new content is the quantitative sharpening (5), its recursive use, and
the explicit thresholds (11)--(14).  No claim of external-literature novelty
is made.

## 6. Verification

Run

```sh
python3 experimental/scripts/verify_asymptotic_c9_parseval_split_prime_descent.py --check
```

The standard-library verifier checks the exact resultant by a Bareiss
determinant, the odd-root Parseval bound, the scale inequalities, periodicity
with nonconstant bounded lifts, and endpoint fiber ceilings on small split
prime rows.

## 7. Nonclaims and next wall

- No theorem for all split primes is proved.
- No unrestricted prime-field C9 theorem is proved.
- No C1--C8 residual emission, quotient-cell budget, multi-leaf add-back, or
  target-normalized compiler theorem is proved.
- No circle, twin-coset, Chebyshev, KoalaBear, Mersenne-31, QM31, or other
  deployed finite row is certified.
- The result is a quantitative sharpening of the existing norm descent, not a
  replacement for Paper B's theorem.

The remaining small-split-prime problem is to count nondivisible signed words
whose cyclotomic resultant has large `p`-adic valuation.  A subexponential
uniform count at the first failed dyadic scale would remove condition (11)
without pretending that the norm-gate branch is empty.
