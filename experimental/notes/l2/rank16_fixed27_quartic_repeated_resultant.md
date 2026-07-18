# Fixed-27 quartic repeated-root resultant and support dichotomy

**Claim layer:** finite local theorem for one actual normalized fixed-27,
fixed-generator, fixed-syndrome-projective-ray, affine-rank-two primitive
quartic source cell. The theorem is repeated-root safe and field specific. It
does not prove that such a source cell exists, exclude seven labels, or pay a
ledger row.

**Status:** the proof below passed an independent hostile audit after the
original formal cancellation was replaced by a prime-valuation argument. The
claimant's archive and verifier hashes were inconsistent with the attached
packet, so no claimant replay claim is consumed. The accompanying verifier
checks the deployed arithmetic, finite minima, density descent, source pins,
and semantic mutations; it is not a mechanical proof of the universal
algebraic theorem.

## Literal source cell

Work over `F=F_p`, where

```text
p = 2,130,706,433 = 127*2^24+1,
H = mu_(2^21) in F^x,
B = 32,768,
Lambda = mu_64,
a = 67,472,
D = 96,369,
d = 63,601,
w = 28,897.
```

Fix a 27-label core `C`, a monic degree-`a` polynomial `g` that is
root-free on `H`, one syndrome projective ray, and one actual normalized
source cell. Assume seven distinct labels `y_0,...,y_6 in Lambda\C`,
nonzero scalars `q_i`, and monic residuals `R_i` satisfying

```text
(X^B-y_i)R_i = q_i h + g W_i,
deg R_i = d,
deg W_i <= w.
```

Each `R_i` is squarefree and split over `H`, avoids the core and its own
selected fibre, and has no additional complete `B`-fibre.

After scalar normalization write

```text
P_i=(X^B-y_i)rho_i=H_0+g c_i dot E,
c_i=(a_1(y_i)/a_0(y_i),a_2(y_i)/a_0(y_i)),
```

where the affine rank is exactly two and `c_0=(0,0)`. The primitive quartic
branch supplies

```text
a_0(X^B)H_0+g(a_1(X^B)E_1+a_2(X^B)E_2)=0,
deg a_0=4,
deg a_1,deg a_2<=4,
a_0(X^B)=g s,
deg s=63,600,
gcd(a_0,a_1,a_2)=1,
a_0(z)!=0 for z in Lambda.
```

Define

```text
N(X,Y)=a_0(Y)H_0+g(a_1(Y)E_1+a_2(Y)E_2)
      =(X^B-Y) mathcal_R(X,Y),
Delta=Res_Y(a_0,mathcal_R).
```

Then `deg_X mathcal_R<=d`, `deg_Y mathcal_R<=3`, and

```text
mathcal_R(X,y_i)=a_0(y_i)rho_i.
```

Put

```text
Base={x in H: mathcal_R(x,Y) is identically zero},
c=|Base|,
C_Base=product_(x in Base)(X-x).
```

## Theorem

Under the fixed-cell hypotheses above:

1. The quartic resultant is repeated-root safe:

   ```text
   g^3 divides Delta,
   Q_res=Delta/g^3 != 0,
   deg Q_res<=51,988.
   ```

2. If the roots `beta_1,...,beta_4` of `a_0` are counted with
   multiplicity and

   ```text
   E_beta=a_1(beta)E_1+a_2(beta)E_2,
   ```

   then for a nonzero field scalar `eta`,

   ```text
   s Q_res=eta product_(nu=1)^4 E_(beta_nu).
   ```

   Consequently

   ```text
   C_Base^4 divides Q_res,
   |Base|<=12,997.
   ```

3. The anchor and every pair secant satisfy

   ```text
   gcd(a_1,a_2) is associated to T-y_0,
   det(b_i,b_j)=a_0 delta_ij,
   0!=delta_ij in F[T],
   deg delta_ij<=2,
   ```

   where

   ```text
   b_i(T)=(c_i a_0(T)-(a_1(T),a_2(T)))/(T-y_i).
   ```

   Hence a pair of residuals has common nonbase roots in at most two complete
   `B`-fibres.

4. For the union `U` of the seven `H`-root sets,

   ```text
   |U|>=141,686.
   ```

   More precisely, after setting

   ```text
   r=d-c,
   lambda=w-c,
   n_3=# outside-base roots of occupancy three,
   ```

   one has the dichotomy

   ```text
   n_3<=5 lambda  ==> |U|>=150,361,
   ```

   while `n_3>5 lambda` forces six Fano-minus-one triple lines and a reduced
   direction pencil with coprime generators in `F[X^m]` for some nontrivial
   even divisor `m` of `B`.

## Proof

The exact division by the monic polynomial `X^B-Y` gives the stated degree
bounds and specializations. The coefficient polynomials
`a_0,a_1,a_2` are linearly independent: a constant relation evaluated at
the seven labels would put all affine coordinates on one line, contradicting
affine rank two.

For `x in H`, `mathcal_R(x,Y)` vanishes identically exactly when
`H_0(x)=E_1(x)=E_2(x)=0`. The converse uses
`s(x)=a_0(x^B)/g(x)!=0`. Therefore

```text
Base=Z_H(E_1) intersect Z_H(E_2).
```

Outside `Base`, the specialization in `Y` is nonzero of degree at most
three, so outside-base occupancy is at most three.

### Repeated-root-safe resultant

Work over an algebraic closure and fix a linear prime `pi=X-alpha` dividing
`g`. Put

```text
k=v_pi(g)>0,
beta=alpha^B,
m=mult_beta(a_0) in {1,2,3,4},
f=v_pi(X^B-beta)>0,
r_pi=v_pi(s)=m f-k>=0.
```

Let

```text
C=a_1(X^B)E_1+a_2(X^B)E_2=-sH_0,
E_beta=a_1(beta)E_1+a_2(beta)E_2,
e_beta=v_pi(E_beta).
```

Since `gcd(g,H_0)=1`, `v_pi(C)=r_pi`. Also
`C-E_beta` is divisible by `X^B-beta`. Thus

```text
e_beta>=min(r_pi,f),
e_beta=r_pi when r_pi<f.
```

Primitivity gives `E_beta!=0`. At a root `gamma` of `a_0`,

```text
(X^B-gamma)mathcal_R(X,gamma)=g E_gamma.
```

For the `m` copies of `beta`,

```text
v_pi(mathcal_R(X,beta))=k+e_beta-f.
```

For each other root, `X^B-gamma` is a `pi`-unit and the valuation is at
least `k`. The root-product formula therefore gives

```text
v_pi(Delta)>=4k+m(e_beta-f).
```

After subtracting `3k`, it remains to show
`k+m e_beta-m f>=0`. If `r_pi<f`, then `e_beta=r_pi` and
`k=mf-r_pi`, so the expression is `(m-1)r_pi`. If `r_pi>=f`, then
`e_beta>=f`, so the expression is at least `k`. This proves
`g^3|Delta` for repeated roots of `a_0`, nonsquarefree `g`, shared
primes of `g,s`, and the zero-root block.

Every `E_beta` is nonzero, hence `Delta!=0`. Since
`deg Delta<=4d`,

```text
deg Q_res<=4d-3a=51,988.
```

Multiplying the four specialization identities gives

```text
s Q_res=eta product_beta E_beta.
```

Each `E_beta` vanishes on `Base`, while `s` has no `H`-root. Euclid's
lemma gives `C_Base^4|Q_res`, and degree comparison gives
`c<=floor(51,988/4)=12,997`.

### Anchor and pair secants

Let `q=gcd(a_1,a_2)`. Since `c_0=(0,0)`, `T-y_0|q`. Primitivity gives
`gcd(q,a_0)=1`. The cancelled syzygy gives `q(X^B)|sH_0`, hence
`q(X^B)|H_0`. Because

```text
H_0=q_0^(-1)(X^B-y_0)R_0
```

is squarefree and split over `H`, any other root of `q` would create an
additional complete fibre in `R_0`, and multiplicity at `y_0` would
contradict squarefreeness. Thus `q` is associated to `T-y_0`.

Direct expansion of the two rows `b_i,b_j` gives
`det(b_i,b_j)=a_0 delta_ij` with `deg delta_ij<=2`. If
`delta_ij=0`, the two normalized residual root sets coincide fibre by
fibre, forcing a gcd of degree `d>w`. Hence `delta_ij!=0`. At a common
nonbase root `x`, both rows annihilate the same nonzero vector
`(E_1(x),E_2(x))`, so `delta_ij(x^B)=0`. This proves the two-fibre
pairwise localization.

### Support floors

Remove the `c` base roots. For outside-base occupancies
`m_x in {1,2,3}`, set

```text
N=|U\Base|,
P=sum_x binom(m_x,2).
```

Then

```text
sum_x m_x=7r,
P<=21 lambda.
```

The elementary pointwise inequalities for occupancies one, two, and three
give

```text
N>=ceil(7r/3),
N>=ceil((14r-21lambda)/3).
```

Minimizing over `0<=c<=12,997` gives the preliminary floor `133,009`.

Every occupancy-three root determines a unique maximal line among the seven
label coordinates. A line's direction polynomial has at most `lambda`
assigned roots. A triple-carrying line cannot contain five labels. Distinct
maximal lines use disjoint label pairs, and seven triple lines would be the
Fano matroid, which is not representable in odd characteristic. A direct
four-label/five-line/six-line case split yields

```text
n_3<=min(2r,6lambda).
```

Since `7r<=2N+n_3`,

```text
|U|>=c+ceil((7r-min(2r,6lambda))/2).
```

The unique arithmetic minimum is `141,685` at

```text
c=11,545,
r=52,056,
lambda=17,352.
```

Equality would force six Fano-minus-one lines, each carrying exactly
`lambda` roots in a single `B`-fibre. For a coprime direction-pencil
basis `F,G`, define

```text
Psi_u(X)=F(uX)G(X)-F(X)G(uX).
```

The fibre-intersection identity and

```text
3(lambda-1)>B-1
```

force `Psi_u=0` for a nonidentity `u in mu_B`. Coprimality makes
`F,G` common-character polynomials. Their nonzero constant terms force
the trivial character, hence `F,G in F[X^2]`. Descending through

```text
(17,352,32,768),
(8,676,16,384),
(4,338,8,192),
(2,169,4,096)
```

preserves the strict density inequality. The final degree `2,169` is odd,
contradicting membership in `F[X^2]`. Equality is impossible, proving
`|U|>=141,686`.

Finally, if `n_3<=5lambda`, then

```text
7r<=2N+5lambda
```

and `|U|>=ceil((7d-5w)/2)=150,361`. If `n_3>5lambda`, the line case split
forces exactly six Fano-minus-one lines. After dividing two independent
direction quotients by their gcd, the same multiplicative-intersection
argument gives coprime generators in `F[X^m]` for a nontrivial even
`m|B`.

## Audit scope and exact wall

The independent hostile audit accepted the theorem above. Its frozen hashes
are

```text
packet: b61fbad8df450f0d4c2d6c24d147391a9dac759d2ed4194ef1a4ad98a3ee0372
final:  a20ab3c82674fa286a7f65140090bb2b15e2b67e7cdbcb0f7bf51f922d4d1d6c
```

The next exact wall is a source-incidence classification of the high-triple
six-line pencil. The theorem does not claim:

* existence of the assumed source cell;
* fixed-27 cap six or seven-label exclusion;
* owner aggregation, add-back, or any ledger payment;
* recurrence, Grand List, Grand MCA, or score movement;
* the claimant's inconsistent archive hash or absent verifier artifacts.
