# Completed-zero-mask two-block payment for strict A6 strata

- **Status:** PROVED under the actual completed-witness hypotheses below.
- **Track:** asymptotic hard input C / condition A6.
- **Dependencies:** the completed-witness chart of PR #659; PR #671 is used
  only for the novelty comparison, not for the proof.
- **Verifier:**
  `experimental/scripts/verify_completed_zero_mask_two_block.py`.

## Exact setup

Let `F` be any field and let `H_U : F^U -> F^R` have weighted
Reed--Solomon parity columns

```text
h_x=lambda_x(1,x,...,x^(R-1))^T,  lambda_x!=0,
```

at `N=R+kappa` distinct points, with `kappa>=1`. Fix `0<=t<R`,
syndromes `y_0,y_1` with `y_1!=0`, and an actual retained first-match set
`Z^circ_lambda` of distinct slopes. For every retained slope `gamma`, select
one actual completed witness `c_gamma` satisfying

```text
H_U c_gamma=y_0+gamma y_1,
wt(c_gamma)<=t,
{y_0,y_1} not subset span{h_x:x in supp(c_gamma)}.          (1)
```

Choose a minimum lift `v` of `y_1` and put

```text
d=wt(v),  J=supp(v),  M=N-d.                               (2)
```

For one exact punctured weight `e`, let `Z^circ_(lambda,e)` be the retained
slopes whose selected witnesses satisfy

```text
e=wt(P_J(c_gamma)),  0<=e<=M.                              (3)
```

where `P_J` deletes the coordinates in `J`. Define

```text
h_e=max(1,d+e-t),
Xi_e=d(M-e)^2+M h_e^2-dM^2.                                (4)
```

## Theorem: two-block complete-mask payment

For `0<e<M`, under (1)--(4),

```text
Xi_e>0  =>  |Z^circ_(lambda,e)|<=N-1,                      (5)

Xi_e=0  =>  |Z^circ_(lambda,e)|<=2(N-2).                   (6)
```

Both bounds are field-independent and remain true after arbitrary preceding
first-match deletion. The two endpoint strata obey

```text
e=0                         => |Z^circ_(lambda,0)|<=floor(d/h_0),
e=M and Xi_M>=0             => |Z^circ_(lambda,M)|<=2d-1.  (7)
```

Consequently, all exact weights in one profile for which `Xi_e>=0` contribute
fewer than `2N^2` slopes. If `N<=n`, this is

```text
exp(O(log n))<=exp(o(n))(1+barN_lambda),                   (8)
```

the direct alternative in `(RC)` at the actual realized-image scale.

## Proof

### 1. Split the complete zero mask

For each selected witness, let

```text
T_gamma={x in U:c_gamma(x)=0},
X_gamma=T_gamma intersect (U\J),
Y_gamma=T_gamma intersect J.                              (8)
```

Exact punctured weight gives

```text
|X_gamma|=M-e.                                             (9)
```

The total weight bound forces at least `d+e-t` zeros in `J` whenever that
number is positive. There is at least one zero in `J` even when it is
nonpositive. Otherwise `supp(v)=J` is contained in `supp(c_gamma)`, and
`u_gamma=c_gamma-gamma v` is also supported inside `supp(c_gamma)`. This
would put both `y_0=H_U u_gamma` and `y_1=H_U v` in the forbidden support
span in (1). Therefore

```text
|Y_gamma|>=h_e.                                            (10)
```

This uses the complete zero mask of an actual selected completed witness; no
synthetic mask or ambient set-system hypothesis is substituted.

### 2. Pairwise common-zero cap

For distinct slopes `gamma` and `gamma'`,

```text
(c_gamma-c_gamma')/(gamma-gamma')                          (11)
```

is a lift of `y_1`. Its weight is at least the minimum-lift weight `d`, so it
has at most `N-d=M` zero coordinates. Every common zero of the two complete
masks is a zero of (11). The blocks are disjoint, hence

```text
|X_gamma intersect X_gamma'|
 +|Y_gamma intersect Y_gamma'|<=M.                         (12)
```

### 3. Endpoint strata

If `e=0`, then every `X_gamma` is the whole `M`-coordinate block. The
pairwise cap (12) therefore makes the sets `Y_gamma` pairwise disjoint. Since
each has size at least `h_0`, at most `floor(d/h_0)` can occur.

Now let `e=M` and suppose `Xi_M>=0`. Then `X_gamma` is empty and

```text
Xi_M=M(h_M^2-dM)>=0.                                      (12a)
```

For every `Y_gamma` other than the whole block `J`, center its indicator in
`1_d^perp`. Distinct centered vectors have inner product at most

```text
M-|Y_gamma||Y_gamma'|/d <= M-h_M^2/d <= 0.                (12b)
```

The right-angle bound gives at most `2(d-1)` nonzero centered vectors. The
zero centered vector corresponds to `Y_gamma=J` and occurs for at most one
slope: two such witnesses would have support in `U\J`; their normalized
difference would put `y_1` in the span of those support columns, and either
witness would then put `y_0` there as well, contradicting (1). Thus the
endpoint costs at most `2d-1`.

Both endpoint arguments begin with the actual retained witnesses and hence
survive arbitrary earlier first-match deletion.

### 4. Centered two-block vectors

Embed the masks in

```text
V=1_M^perp direct-sum 1_d^perp,  dim(V)=N-2,
```

and define

```text
z_gamma=(
  1_(X_gamma)-(M-e)/M 1_M,
  1_(Y_gamma)-|Y_gamma|/d 1_d
).                                                         (13)
```

Because `0<e<M`, the first component is nonzero. Using (9), (10), and (12),

```text
<z_gamma,z_gamma'>
 <=M-(M-e)^2/M-h_e^2/d
  =-Xi_e/(Md).                                             (14)
```

If `Xi_e>0`, the vectors have strictly negative pairwise inner products. A
nonzero family with that property in an `s`-dimensional real space has size
at most `s+1`: if at least `s+2` vectors occurred, a nonzero linear relation
whose coefficients sum to zero would split into two positive combinations,
and their cross inner product would make the squared norm of the common sum
negative. Taking `s=N-2` proves (5).

If `Xi_e=0`, the pairwise inner products are nonpositive. The standard
right-angle bound gives at most `2s` nonzero vectors in dimension `s`.
Taking `s=N-2` proves (6).

### 5. First-match and profile compilation

The proof begins with the actual retained set `Z^circ_(lambda,e)`. Earlier
first-match cells remove slopes, so every later set is a subset and preserves
all pairwise inequalities. There are at most `M-1<=N-2` interior exact
weights. Their contribution is at most `2(N-2)^2`; the two endpoint bounds
sum to at most `3d-1<=3N-4`. Hence the complete `Xi_e>=0` contribution is at
most

```text
2(N-2)^2+3N-4=2N^2-5N+4<2N^2.                            (14a)
```

For a nonempty realized support slice,

```text
barN_lambda
=|Omega^0_lambda|/|Phi_lambda(Omega^0_lambda)|>=1.
```

Thus (8) is the literal direct profile payment. The proof does not use the
formal codomain size, a full-image hypothesis, primitive Q, or an unproved
support-pair incidence.

## Correct asymptotic statement

Suppose along a sequence that

```text
N/n -> nu,
d/n -> delta>0,
M/n -> mu>0,
t/n -> tau,
e/n -> epsilon,
eta=max(0,delta+epsilon-tau).
```

Then

```text
Xi_e/(Mdn) -> Psi_2blk(delta,mu,tau,epsilon),

Psi_2blk
=(mu-epsilon)^2/mu+eta^2/delta-mu.                         (15)
```

The valid consequences are exactly:

```text
Psi_2blk>0
  => Xi_e>0 eventually and the exact stratum is directly paid;

Psi_2blk=0 and Xi_e>=0 eventually
  => the exact stratum is directly paid.                   (16)
```

The weak limiting condition `Psi_2blk>=0` alone is not sufficient on the
equality surface. Lower-order integer terms can keep `Xi_e<0`. The verifier
contains explicit equality-limit falsifiers.

## Explicit strict linear family

For every integer `r>=1`, take

```text
(N,R,kappa,t,d)=(500r,275r,225r,150r,250r),
M=250r,  Delta=R+1-d=25r+1.                               (17)
```

The older high-direction, punctured-Johnson, deep, and bounded-kernel routes
all fail:

```text
(N-t)^2=122500r^2<NM=125000r^2,

Delta M-2tM+t^2=-46250r^2+250r<0,

3t=450r>R=275r,

kappa=225r=Theta(N).                                      (18)
```

Here

```text
q_e=d+2e-2t=2e-50r,
h_e=100r+e,

Xi_e=500r(e-50r)(e-100r).                                 (19)
```

Every exact weight in

```text
15r<=e<=50r    or    100r<=e<=111r                        (20)
```

lies strictly in `W1-` or `W2-` and satisfies `Xi_e>=0`. With `n=N`, the
two paid intervals are

```text
e/n in [3/100,1/10] union [1/5,111/500].                   (21)
```

The exact equality faces are `e=50r` and `e=100r`. There are `46r+2` exact
weights in (20), and their complete contribution is at most

```text
46r(500r-1)+2(1000r-4)
=23000r^2+1954r-8.                                        (22)
```

These intervals are not paid by #659: `q_e<M` and the old `W1/W2`
denominator is strictly negative. They are not paid by the explicit #671
certificate either. For `e<=25r`, its Cramer bound is at least `2*10^e`; for
`e>=25r+1`, it is greater than `2^e`. Thus the previous displayed certificate
has uniformly positive exponential rate while (5)--(6) give a polynomial
bound.

For (17), (15) becomes

```text
Psi_2blk(epsilon)=4(epsilon-0.1)(epsilon-0.2).              (23)
```

The sequences `e=50r+1` and `e=100r-1` converge to the two zeros in (23) but
have `Xi_e<0`. They are the required regression against replacing (16) by a
weak limiting inequality.

### Actual weighted-RS nonvacuity

Let `F` contain at least `500r` elements, choose `U subset F` of that size,
and choose arbitrary nonzero parity weights. Put

```text
G_U(X)=product_(x in U)(X-x),
omega_x=(lambda_x G_U'(x))^(-1).
```

Then

```text
ker H_U={(omega_x p(x))_(x in U):deg p<225r}.              (24)
```

Choose a `250r`-set `T_0 subset U`, let
`f(X)=product_(x in T_0)(X-x)`, and set `v_x=omega_x f(x)`. The vector `v`
has weight `250r`. Every other lift of `H_U v` is obtained by adding a word
from (24); its defining polynomial still has exact degree `250r` and therefore
at most `250r` roots in `U`. Hence `v` is a minimum lift and `d=250r`.

For each `e` in (20), choose `S subset T_0` with `|S|=e`, choose
`B subset U\T_0` with `|B|=t-e`, and choose a vector `c` supported exactly on
`S union B`. Set `y_1=H_U v`, `y_0=H_U c`, and `gamma=0`. Then `c` is an
actual weight-`t` witness of punctured weight `e`. If `y_1` lay in the parity
span of its support, it would have a lift of weight at most `t<d`, a
contradiction. Thus the witness is transverse.

This construction proves source-valid nonvacuity separately for every exact
weight. The chosen `y_0` may vary with `e`; it does not claim that one fixed
received line simultaneously realizes all weights in (20), nor that it gives
an exponential actual slope family.

## Remaining linear-weight wall

After the #659 equality/full-separation branches, the #671 subexponential
Cramer branches, and the theorem above, the unresolved part of this A6 route
contains actual strict `W1-/W2-` completed-witness strata with

```text
Xi_e<0.                                                    (25)
```

For the stress family (17), the canonical central band is

```text
50r<e<100r.                                                (26)
```

Pairwise selected-mask geometry alone permits positive-rate abstract families
there. A further proof must use higher completed-mask/Cramer consistency,
literal predecessor routing, all-witness multiplicity, or an actual
boundary-equal `(RC)` incidence. An abstract constant-composition mask family
is not an RS counterexample.

## Nonclaims

This note does not prove:

- the entire linear-weight strict `W1- union W2-` interior;
- payment when `Xi_e<0`;
- simultaneous realization of (20) on one fixed received line;
- a witness-exhaustive A2 atlas or a bound on the number of profiles;
- primitive Q, MI, MA, a full-image theorem, or an `(RC)` incidence in (25);
- the A7 profile-envelope comparison or unsafe/lower reserve;
- any finite deployed-row improvement;
- Grand MCA, Grand List, or either prize threshold.

The official score remains `0/2`. No stable TeX statement is changed.

## Verification

Run:

```text
python3 experimental/scripts/verify_completed_zero_mask_two_block.py --check
python3 experimental/scripts/verify_completed_zero_mask_two_block.py --tamper-selftest
```

The checker uses only the Python standard library. It exhausts all `43`
two-block cases with `2<=M,d<=5` and `Xi_e>=0`, checks every exact weight in
(20) for `1<=r<=500`, exercises actual weighted-RS completed-witness lines over
small prime fields, tests arbitrary slope deletion, and rejects the weakened
common-zero threshold and the two false asymptotic equality inferences.
