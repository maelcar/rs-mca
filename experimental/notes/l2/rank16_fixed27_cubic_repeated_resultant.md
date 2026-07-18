# Fixed-27 cubic repeated-root resultant and base cancellation

**Claim layer:** finite local theorem in one normalized fixed-27 affine-rank-two
cubic source cell. The theorem extends the integrated squarefree-cubic
resultant to every cubic factor type, including repeated and zero roots. It
forces

```text
|Base| <= 18,619
```

and raises the seven-residual root-union floor from `150,361` to `176,056`.
It does not eliminate seven labels or make a ledger payment.

**Status:** proved after an independent hostile audit corrected the pairwise
chord statement from "one third fibre" to "zero or one admissible third
fibre" and made the splitting-field descent explicit. The author-reported
replacement verifier was not present in the audit packet and is not claimed
here. The official score remains `0/2`.

## Literal source cell

Work over `F=F_p` with

```text
p = 2,130,706,433 = 127*2^24+1,
H = mu_(2^21) in F^x,
B = 32,768,
T = X^B,
a = 67,472,
D = 96,369,
d = 63,601,
w = 28,897.
```

Fix one 27-label core `C` in `mu_64`, one monic degree-`a` polynomial
`g` that is root-free on `H`, one syndrome projective ray, and one normalized
source cell. Assume seven distinct labels `y_i` outside `C`, nonzero scalars
`q_i`, and monic residuals `R_i` satisfying

```text
(T-y_i)R_i = q_i h + g W_i,
deg R_i = d,
deg W_i <= w.
```

Each `R_i` is squarefree and completely split over `H`. All inherited source
filters remain in force: selected/core-fibre avoidance, no additional complete
`q64` fibre, residual footprint at least four, and the `q32` full-pair
restriction.

Assume the inherited affine-rank-two cubic syzygy with an actual anchor `H_0`,
independent directions `E_1,E_2`, and polynomials `a_0,a_1,a_2`:

```text
a_0(T)H_0 + g(a_1(T)E_1+a_2(T)E_2) = 0,
a_0(Y) = Y^3+c_2 Y^2+c_1 Y+c_0,
deg a_1, deg a_2 <= 3,
gcd(a_0,a_1,a_2) = 1,
a_0(y) != 0 for every y in mu_64,
c_ij = a_j(y_i)/a_0(y_i).
```

The source equations and every displayed denominator live over `F`. A finite
splitting field is used only to name the roots of `a_0` and their canonical
divisor layers.

Define

```text
N(X,Y) = a_0(Y)H_0
       + g(a_1(Y)E_1+a_2(Y)E_2)
       = (T-Y) mathcal_R(X,Y).
```

Then

```text
deg_X mathcal_R <= d,
deg_Y mathcal_R <= 2,
mathcal_R(X,y_i) = a_0(y_i)q_i^(-1)R_i(X).
```

Put

```text
Base = {x in H : mathcal_R(x,Y) is identically zero},
c = |Base|,
Gamma(X) = product_(x in Base) (X-x).
```

## Theorem

Under the fixed-cell hypotheses above, all of the following hold.

### 1. Oriented remainder and quadratic content

The exact divided difference is

```text
Q(T,Y) = (a_0(T)-a_0(Y))/(T-Y)
       = Y^2+(T+c_2)Y+(T^2+c_2 T+c_1),
mathcal_R(X,Y) = -rem_g(h(X)Q(T,Y)).                    (1)
```

For every finite extension `K/F` and every nonzero `b in K[T]` of degree at
most two, define

```text
Phi_b = -rem_g(h(X)b(T)),
D_b = gcd(g(X),b(T)).
```

Then

```text
Phi_b != 0,
Gamma D_b divides Phi_b,
c+deg D_b <= d.                                         (2)
```

### 2. Deepest-layer specialization

Over a finite splitting field write

```text
a_0(Y) = product_alpha (Y-alpha)^(m_alpha),
sum_alpha m_alpha = 3.
```

For a nonzero root, put `F_alpha=X^B-alpha` and use the inherited nested
layers

```text
G_(alpha,m_alpha) | ... | G_(alpha,1) | F_alpha.
```

For a zero root use the canonical monomial layers. Write

```text
S_(alpha,nu) = B-deg G_(alpha,nu),
sum_(alpha,nu) S_(alpha,nu) = 3B-a = 30,832.
```

Let

```text
Q_alpha = a_0(T)/(T-alpha),
D_alpha = gcd(g,Q_alpha).
```

Then repeated nonzero roots and zero roots obey the same deepest-layer
formula

```text
D_alpha = g/G_(alpha,m_alpha),
mathcal_R(X,alpha) = D_alpha U_alpha,
Gamma divides U_alpha,
deg U_alpha <= w-S_(alpha,m_alpha).                     (3)
```

Every `mathcal_R(X,alpha)` is nonzero.

### 3. Repeated-root resultant

For each root block let `g_alpha` denote the corresponding factor of `g`, and
define

```text
J = product_alpha g_alpha/G_(alpha,m_alpha)^(m_alpha),
Delta = deg J
      = sum_alpha (
          m_alpha S_(alpha,m_alpha)
          - sum_(nu=1)^(m_alpha) S_(alpha,nu)
        ).
```

Nestedness makes `J` a polynomial. Galois invariance gives `J in F[X]`, and
`Delta>=0`. There is an `M in F[X]` such that

```text
Res_Y(a_0,mathcal_R) = g^2 M,
M = J product_alpha U_alpha^(m_alpha),
deg M <= 3w-(3B-a) = 55,859,
Gamma^3 J divides M.                                   (4)
```

Consequently

```text
3c+Delta <= 55,859,
c <= 18,619.                                            (5)
```

### 4. Root-union floor and exact Base cancellation

Let `U` be the union of the seven `H`-root sets of the residuals. Base roots
have occupancy seven. Outside `Base`, the nonzero polynomial
`mathcal_R(x,Y)` has degree at most two, so occupancy is at most two. Hence

```text
7d <= 7c+2(|U|-c),
|U| >= c+ceil(7(d-c)/2) >= 176,056.                    (6)
```

This improves the inherited floor by

```text
176,056-150,361 = 25,695.
```

Moreover `Gamma` divides `h`, every `R_i`, and every `W_i`. Dividing the
source equations by `Gamma` preserves monicity, squarefreeness, complete
`H`-splitting, selected/core avoidance, and the no-extra-complete-fibre
condition. The seven cancelled residuals have no common `H`-root. Persistence
of residual footprint at least four is not asserted.

### 5. Corrected pairwise chord localization

Put

```text
a(Z) = (a_0(Z),a_1(Z),a_2(Z)),
Delta_ij(Z) = det[a(Z);a(y_i);a(y_j)],
chi_ij(Z) = Delta_ij(Z)/((Z-y_i)(Z-y_j)).
```

Affine rank two and distinct source coordinates imply that `chi_ij` is
nonzero of degree at most one. It can have zero or one admissible root in
`mu_64` outside the core and the selected labels.

After Base cancellation, if there is no admissible root then the two
residuals are coprime. If one admissible root exists, their common roots are
confined to, and match inside, that one `B`-fibre. In all cases

```text
deg gcd(bar_R_i,bar_R_j) <= w-c.                        (7)
```

## Proof

Substitution `Y=T` in `N` gives `N(X,T)=0`, so `T-Y` divides `N`. Modulo `g`,
the primitive syzygy gives `a_0(T)h=0` and

```text
a_0(Y)-a_0(T)=-(T-Y)Q(T,Y).
```

Since `T-Y` and `g(X)` are coprime in `F(Y)[X]`, cancellation is valid. The
bound `deg_X mathcal_R<deg g` selects the unique remainder and proves (1).

Write `mathcal_R=r_0+r_1Y+r_2Y^2`. Every Base point annihilates all three
coefficients, so `Gamma` divides them. Formula (1) gives `r_2=-h`, hence
`Gamma|h`. The three multipliers

```text
1, T+c_2, T^2+c_2T+c_1
```

form a triangular basis for the polynomials of `T`-degree at most two. Thus
`Gamma|Phi_b`. Also `D_b|Phi_b`, and `g` is root-free on `H`, so
`gcd(Gamma,D_b)=1`. If `Phi_b=0`, coprimality of `g,h` would imply
`g|b(T)`, impossible because `deg b(T)<=2B<a`. This proves (2).

For a nonzero root block, an atomic factor occurring to exponent `e` in `g`
occurs to exponent `m_alpha-1` in `Q_alpha`. Its gcd exponent is
`min(e,m_alpha-1)`. Removing the deepest layer from `g` subtracts one exactly
when `e=m_alpha`, giving the same exponent. For a zero root with
`v_X(g)=k`, the deepest monomial layer has exponent

```text
max(k-(m_alpha-1)B,0),
```

so its removal leaves `min(k,(m_alpha-1)B)`, again the gcd valuation. This
proves the first identity in (3). Nonvanishing follows from
`deg_X Q_alpha=2B<a` and `gcd(g,h)=1`. Dividing by `D_alpha`, using the degree
bound on `mathcal_R`, and cancelling the coprime `Gamma` give the rest of (3).

Because `a_0` is monic, repeated-root multiplicity gives

```text
Res_Y(a_0,mathcal_R)
  = product_alpha mathcal_R(X,alpha)^(m_alpha).
```

The deepest-layer identity shows that the product of the `D_alpha` powers is
`g^2J`. Formula (3), the definition of `Delta`, and the full deficit sum give

```text
deg M
 <= Delta+sum_alpha m_alpha(w-S_(alpha,m_alpha))
 = 3w-sum_(alpha,nu) S_(alpha,nu)
 = 55,859.
```

Galois automorphisms permute the root blocks and canonical layers, so `J` and
`M` descend to `F[X]`. Since `Gamma|U_alpha` for every root block,
`Gamma^3J|M`; (5) follows. The incidence count proves (6).

Squarefreeness makes every Base root occur exactly once in every `R_i`.
The source equation, `Gamma|h`, and `gcd(Gamma,g)=1` imply `Gamma|W_i`, so
exact cancellation is source-valid. A common root after cancellation would
give seven roots of a nonzero polynomial of label degree at most two, which
is impossible.

Finally, `a_0,a_1,a_2` are linearly independent by affine rank two. The
vectors `a(y_i),a(y_j)` are independent because equal affine coordinates
would identify two normalized locators and create a forbidden additional
complete fibre. Therefore `Delta_ij` is nonzero, has the two displayed roots,
and its quotient is nonzero of degree at most one. Evaluating the source
functional at a common residual root proves the localization in (7). The
direction-difference polynomial gives the stated gcd-degree bound.

## Audit and replay scope

The independent hostile audit accepted precisely the theorem above. Its
frozen packet and final-answer hashes are

```text
packet: f49f07999907e4a27559e0de4fbd385d38e6c840b681bf6db8dd1c9a132aa71e
final:  d7439240a34fc24eeab61c5c4582307e4e551e5b6a944b64b0a0e9dc0499a07a
```

The accompanying verifier checks current source pins, deployed arithmetic,
the exact endpoint, repeated/zero valuation identities, expected output, and
semantic mutations. It does not mechanically prove the universal algebraic
theorem. No claim is made for the absent author-reported replacement verifier.

## Exact remaining wall and nonclaims

The endpoint `c=18,619` is arithmetically compatible with the theorem: only
two degrees may remain after `Gamma^3` is charged. A new near-equality or
source-incidence theorem is still required to eliminate the seven-label cubic
cell.

This note does not claim:

* nonexistence of seven labels or a fixed-27 cap of six;
* a literal source witness;
* persistence of residual footprint after Base cancellation;
* a mandatory third pairwise fibre;
* first-match ownership, add-back, or cross-cell aggregation;
* finite, asymptotic, recurrence-parent, Grand List, or Grand MCA payment;
* any official score change.
