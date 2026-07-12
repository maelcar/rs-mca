# Completed-Cramer payment for strict A6 strata

## Status

`PROVED`, as a successor to PR #659.  The theorem pays every strict
`W1-/W2-` exact-weight stratum whose explicit completed-Cramer count is
subexponential, including all `e=o(n/log n)`.  It does not pay the remaining
linear-weight strict interior.

## Setup

Use the completed weighted-RS chart notation of
`a6_full_support_zero_boundary.md`.  Thus `N=R+kappa`, `t<R`,
`K=ker H_U` is an `[N,kappa,R+1]` MDS code, and `v` is a minimum lift of
`y_1` with

```text
d=wt(v), J=supp(v), M=N-d, Delta=R+1-d=M-kappa+1.
```

For an exact punctured weight `e`, put

```text
h_e=max(1,d+e-t),
q_e=d+2e-2t,
J_e=e^2-2Me+Mq_e.
```

The strict shells left after PR #659 are

```text
W1-: q_e<=Delta and J_e<0,
W2-: Delta<q_e<M and e^2<M(2t-d).
```

Let `Z^circ_{lambda,e}` be the actual retained first-match slope set with one
selected completed witness at exact punctured weight `e`.

## Theorem 1: terminal full-zero-mask rigidity

Choose a kernel generator `G`, a lift `u_*` of `y_0`, and write

```text
c(alpha,gamma)=u_*+G alpha+gamma v.
```

For an actual transverse witness `c_gamma`, let `T_gamma` be its complete zero
mask.  Then the affine incidence

```text
{(alpha,eta): c(alpha,eta)|_{T_gamma}=0}
```

is the singleton `(alpha_gamma,gamma)`.  Equivalently,
`[G_{T_gamma}|v_{T_gamma}]` has rank `kappa+1`.  Hence some
`I subseteq T_gamma`, `|I|=kappa+1`, has nonzero completed determinant and

```text
gamma = det[G_I|-u_{*,I}] / det[G_I|v_I].               (1)
```

### Proof

If the incidence had a nonzero direction `(eta,beta)`, then
`z=G eta+beta v` would vanish on `T_gamma` and be supported inside the witness
support, of size at most `t`.  If `beta=0`, this is a nonzero kernel word of
weight below the MDS distance `R+1`.  If `beta!=0`, then
`b=beta^{-1}z` is a lift of `y_1` supported inside the witness support, while
`c_gamma-gamma b` is such a lift of `y_0`; this contradicts transversality.
Thus the translation space is zero, and (1) follows from Cramer's rule.

## Theorem 2: split completed-Cramer count

Adopt `binom(a,b)=0` outside `0<=b<=a`.  Then

```text
|Z^circ_{lambda,e}| <= B^Cr_e,

B^Cr_e =
  floor(d binom(M,kappa) /
        (h_e binom(M-e,kappa)))          if e<=Delta-1,

  binom(M,e) binom(d,e-Delta+2)          if e>=Delta.     (2)
```

The bound applies directly after arbitrary first-match deletion and on both
strict shells.

### Proof

For a selected witness, split its zero mask into
`X subseteq U\J` and `Y subseteq J`.  Exact punctured weight gives
`|X|=M-e`; the weight and transversality argument gives `|Y|>=h_e`.
Puncturing the kernel to `U\J` yields an `[M,kappa,Delta]` MDS code.

If `M-e>=kappa`, every pair consisting of a `kappa`-subset of `X` and one
point of `Y` is an invertible completed-Cramer pivot.  Each slope owns at least
`h_e binom(M-e,kappa)` labels, the label universe has size
`d binom(M,kappa)`, and each label determines at most one slope.  This proves
the first line of (2).

If `M-e<kappa`, terminal rigidity lets the rows indexed by `X` be completed to
a basis with `r=kappa+1-(M-e)=e-Delta+2` rows of `Y`.  Choose the first such
completion in a fixed order.  The label `(X,B_gamma)` determines the slope by
Cramer's rule, so the labeling is injective.  There are
`binom(M,e)binom(d,e-Delta+2)` labels, proving the second line.

## Subexponential payment and remaining wall

For `e<=Delta-1`, `B^Cr_e<=N^(e+1)`, and for `e>=Delta`,
`B^Cr_e<=N^(2e+2)`.  Therefore every family of exact weights with
`sum_e B^Cr_e=exp(o(n))` is directly paid.  In particular, all
`e=o(n/log n)` strict strata are paid, including genuine `W1-` and `W2-`
families with `kappa=Theta(n)`.

For `e=Theta(n)`, the displayed count can be exponential.  Terminal-mask
rigidity and Cramer reconstruction alone therefore do not close the strict
interior.  The exact remaining input must use the literal first-match
predecessors, realized boundary image, or boundary-equal support-pair/RC
incidence.  No full A6, A7, deployed row, Grand MCA, or Grand List result is
claimed.
