# Dense-shell terminal two-level decorated charge

## Status

```text
Status: PROVED (local all-depth theorem).

For every depth B >= 2 and every dense-word prefix pi of length B-2,
the decorated subtree charge at the final two scan positions satisfies

  T_pi({B-1,B}) > beta_0 m_2 > 0,

where beta_0 is the positive constant coefficient in the alternating
shifted-Chebyshev cone for the prefix polynomial and

  m_2 = cos(4pi/9)(cos(pi/9)-cos(2pi/9))/32.

Consequently, for every B >= 3,

  T_empty({1,B-1,B}) > 0.

This is a terminal decoration theorem only. It does not prove
T_pi(K)>0 for arbitrary |K|>=2, any class-payment statement, or either
official RS-MCA question. Official score: 0/2.
```

Source floor: `origin/main@c4856fa6db0b2cd491f5c5fe2a0f3c8468de645e`.
The theorem uses the all-depth alternating prefix cone from
`dense_shell_sign_dichotomy.md` and the exact decorated-charge definition
from C3b of `dense_shell_class_charges.md`. It does not consume the pending
singleton transfer in PR #905, the audit in PR #911, or the charge-accounting
repairs in PRs #914 and #917.

The stdlib replay is
`experimental/scripts/verify_dense_shell_terminal_two_level_charge.py`.
It checks the suffix formulas on 100,001 incoming states, enumerates all
32,767 terminal prefixes through depth 16, verifies root-anchor deletion
through depth 10, runs identically under ordinary and optimized Python, and
catches three load-bearing mutations. These finite checks corroborate the
all-depth proof below; they are not its logical basis.

## 1. Source definitions

For a signed scan state `t`, write

```text
a(t) = sin^2(pi t),
q(t) = a(t)-1/2 = -(1/2)cos(2pi t).
```

Let `T_i(x)=T_i(2x-1)` denote the shifted Chebyshev basis. Normalized
arcsine measure `mu` on `[0,1]` satisfies

```text
int T_i T_j dmu = 0                 (i != j),
int T_0^2 dmu = 1,
int T_i^2 dmu = 1/2                 (i >= 1).
```

Fix `B>=2`, a dense prefix `pi` of length `m=B-2`, and its incoming state
`u in [-1/2,1/2]`. The source alternating-cone theorem gives

```text
g_pi(x) = sum_{i=0}^m (-1)^(m-i) beta_i T_i(x),
beta_i >= 0,  beta_0 > 0.
```

For `d,e in {-1,+1}`, define

```text
v_d   = (d+u)/3,
w_de  = (e+v_d)/3,
p_d   = q(v_d),
r_de  = q(w_de).
```

The fully decorated final two-level suffix is

```text
D_2(u;x) = sum_{d,e} p_d r_de (x-a(v_d))(x-a(w_de)).
```

Because `x-a = T_1/2-q`,

```text
(x-a_p)(x-a_r)
  = (1/8+pr)T_0 -(p+r)T_1/2 + T_2/8.
```

Thus

```text
D_2(u;x) = h_0(u)T_0 - h_1(u)T_1 + h_2(u)T_2.
```

## 2. Positivity of the suffix coefficients

Set

```text
theta = 2pi u/9,
A = cos(pi/9),
C = cos(2pi/9),
D = cos(4pi/9).
```

Summing the four paths and using product-to-sum gives

```text
h_2(u) = [A cos(4theta)-D cos(2theta)]/32,

h_1(u) = 3C cos(theta)/32 + cos(3theta)/16
         -A cos(5theta)/16 + D cos(7theta)/32.
```

### The `h_2` bound

The numerator `F(theta)=A cos(4theta)-D cos(2theta)` is even, so take
`0<=theta<=pi/9`. Its derivative is

```text
F'(theta)=2 sin(2theta)[D-4A cos(2theta)].
```

On this interval `cos(2theta)>=C`. Also

```text
AC = 1/4+A/2 > 2/3,
```

because `A>5/6`. Hence `D-4A cos(2theta) <= D-4AC < 0`, so `F`
decreases and

```text
h_2(u) >= D(A-C)/32 = m_2 > 0.
```

### The `h_1` bound

For `|theta|<=pi/9`,

```text
cos(theta)>=A,  cos(3theta)>=1/2,
cos(5theta)<=1, cos(7theta)>=-1.
```

Therefore

```text
h_1(u)
  >= 3AC/32 + 1/32 - A/16 - D/32
  > 3AC/32 - 1/16
   = (6A-5)/128
  > 0.
```

### The `h_0` bound

Writing `phi_d=theta+2pi d/9`, direct summation gives

```text
h_0(u)-h_2(u)
  = sum_d p_d^2 [1/4-(1/8)cos(2phi_d)].
```

Every bracket is at least `1/8`. Moreover

```text
p_+ + p_- = (1/2)cos(2pi u/3) >= 1/4,
```

so the two `p_d` cannot both vanish. Hence

```text
h_0(u) > h_2(u) >= m_2 > 0.
```

Repeated roots and zero decorations cause no problem: the proof uses only
polynomial identities and never divides by a root difference.

## 3. Pairing with every prefix

The decorated charge is

```text
T_pi({B-1,B}) = (-1)^B int g_pi(x) D_2(u;x) dmu(x).
```

Since `B=m+2`, all alternating signs cancel. Orthogonality yields

```text
T_pi({B-1,B})
  = beta_0 h_0
    + (1/2) sum_{i=1}^{min(m,2)} beta_i h_i
  > beta_0 m_2
  > 0.
```

This proves the terminal two-level theorem for every depth.

At the first scan position `u_1=+-1/3`, hence `q_1=1/4` for every dense
word. Partitioning the positive-leaf identity by prefixes of length `B-2`
therefore gives the exact root-anchor deletion identity

```text
T_empty({1,B-1,B})
  = (1/4) sum_{pi in {+-1}^{B-2}} T_pi({B-1,B})
  > 0
```

for every `B>=3`.

## 4. Exact nonclaims and remaining wall

- This does not prove `T_pi(K)>0` for arbitrary nonempty `K` with
  `|K|>=2`. Decorations separated from the terminal two-level suffix remain
  the exact wall.
- This does not prove the product-profile emission schedule, any omega or
  class-payment identity, ledger admissibility, lower reserve, Grand MCA, or
  Grand List.
- It does not use PR #905's pending all-depth singleton theorem. Any root-pair
  or inner-incoming pair consequence that consumes singleton positivity must
  remain conditional on that exact pending head.
- PRs #914 and #917 repair a distinct parity-dependent charge-accounting
  interface. No statement from that disputed interface is used here.
- No official theorem is proved. Official score remains `0/2`.

The next exact wall is an all-depth closure principle for an arbitrary
decorated suffix `G^S`, strong enough to handle nonterminal separated
decorations without asserting either of the already-refuted claims
"decorated cone purity" or "decorated Master inequality."
