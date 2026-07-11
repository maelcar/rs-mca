# Dense exclusion correction for fixed-weight moment recursions

- **Status:** PROVED exact identity and route cut.
- **Track:** asymptotic hard input B / the `w=2,3` subgroup-VMVT
  recursion in open PR #564.
- **Verifier:**
  `python3 experimental/scripts/verify_b2_dense_exclusion_correction.py`.

## Claim

Let `A` be a finite abelian group of order `Q`, let `X` have size `n`,
and let `Phi : X -> A`.  Write

```text
nu_r(s) = #{S subset X : |S|=r and sum_{x in S} Phi(x)=s}
P(s)    = #{x in X : Phi(x)=s}
C_r     = nu_{r-1} * P.
```

For `r >= 2`, define the repeated-coordinate correction

```text
kappa_r(s) = #{(B,x) : x in X, B subset X\{x}, |B|=r-2,
                         sum_{y in B} Phi(y) + 2 Phi(x)=s}.
```

Then, pointwise on `A`,

```text
C_r = r nu_r + kappa_r.                                      (1)
```

In particular,

```text
||nu_r||_1       = binom(n,r),
||C_r||_1        = n binom(n,r-1),
||kappa_r||_1    = (r-1) binom(n,r-1),
||C_r/r-nu_r||_1 = (r-1)/(n-r+1) binom(n,r).                 (2)
```

Thus the normalized add-one convolution has the exact mass ratios

```text
||C_r/r-nu_r||_1 / ||nu_r||_1 = (r-1)/(n-r+1),
||C_r/r||_1       / ||nu_r||_1 = n/(n-r+1).                  (3)
```

These ratios do not tend to zero or one when `r/n -> delta in (0,1)`.
Moreover, by Cauchy-Schwarz,

```text
||C_r/r||_2^2 >= (n/(n-r+1))^2 binom(n,r)^2 / Q.             (4)
```

## Explicit asymptotic falsifier for the proxy ratio

Fix `w in {2,3}` and `delta in (0,1)`.  Let odd primes `p` tend to
infinity, put `X=F_p^x`, `n=p-1`,

```text
Phi_w(x) = (x,x^2,...,x^w),    r=floor(delta n).
```

The unconditional shallow-prefix flatness theorem
`thm:unconditional-shallow-mi-ma` applies at the two adjacent densities
`r` and `r-1`.  Hence both `nu_r` and `nu_{r-1}` are exponentially close
to their uniform distributions.  It follows that

```text
  ||C_r/r||_2^2
  ----------------  -> 1/(1-delta)^2.                        (5)
    ||nu_r||_2^2
```

At `delta=1/3`, the limit is `9/4`, not `1`.  This is an explicit
subgroup-moment-map sequence inside the stated `w=2,3` lane, not an
arbitrary-set counterexample.

## Disjoint-pair correction

Let `omega_{a,b}(s)` count ordered disjoint pairs `(A_+,A_-)` with
`|A_+|=a`, `|A_-|=b`, and

```text
sum_{x in A_+} Phi(x) - sum_{y in A_-} Phi(y) = s.
```

For `2r <= n`, put `D_r=omega_{r-1,r}*P`.  Define `kappa_r^+(s)` to
count triples `(C,B,x)` with `|C|=r-2`, `|B|=r`, `C,B,{x}` pairwise
disjoint, and

```text
sum_{y in C} Phi(y) + 2 Phi(x) - sum_{z in B} Phi(z) = s.
```

Then the exact pointwise identity is

```text
D_r = r omega_{r,r} + kappa_r^+
      + (n-2r+2) omega_{r-1,r-1}.                            (6)
```

If

```text
T_r = binom(n,r) binom(n-r,r-1),
```

the three terms on the right of (6) have masses

```text
(n-2r+1)T_r,    (r-1)T_r,    r T_r,
```

while `||D_r||_1=nT_r`.  The omitted fraction is therefore
`(2r-1)/n`; at `r/n -> 1/3`, the convolution proxy has three times the
true mass and the omitted mass has twice the true mass.

## Proof

The convolution `C_r` counts pairs `(B,x)` with `|B|=r-1`.  If `x` is
not in `B`, adjoining it gives an `r`-set with one of its `r`
distinguished elements.  If `x` is in `B`, write `B=C union {x}`; this
is exactly `kappa_r`.  This proves (1), and the mass identities follow by
counting choices.

For (6), split the unrestricted added point `x` into three cases.  If it
is outside both selected sets, it produces `r omega_{r,r}`.  If it lies
in the positive set, it produces `kappa_r^+`.  If it lies in the
negative set, it cancels that occurrence; each resulting
`(r-1,r-1)` pair has `n-2r+2` possible cancelled points.  The cases are
disjoint and exhaustive.

On Fourier transforms, Newton's identity gives the exact correction in
another form.  If

```text
tau_j(c) = sum_{x in X} psi(c . Phi(x))^j,
```

then

```text
r nu_hat_r(c)
  = sum_{j=1}^r (-1)^(j-1) tau_j(c) nu_hat_{r-j}(c),

kappa_hat_r(c)
  = tau_1(c) nu_hat_{r-1}(c) - r nu_hat_r(c)
  = sum_{j=2}^r (-1)^j tau_j(c) nu_hat_{r-j}(c).              (7)
```

The omitted correction is the complete higher-dilate Newton tail.  It
is not a lower-order incidence error at linear density.

## Ledger effect

This cuts only the uncorrected first-order convolution proxy used by the
`w=2,3` numerical recursion in open PR #564.  It does **not** refute the
exact second/fourth-moment engine there, and it does not rule out a
corrected recursion using (7).

The next exact target is a mass-matched marked-exclusion covariance
bound.  With `a_r=(r-1)/n`, it must control

```text
||kappa_r-a_r C_r||_2
```

at the source scale, together with the analogous centered combination of
the last two terms in (6).  A positive estimate would repair the
recursion; a counterexample would terminate that route.

## Nonclaims

- No full image-scale MI+MA or direct Sidon payment is proved.
- No max-fiber theorem or `(SV*)` bound is proved.
- No deployed M31 or KoalaBear row is changed.
- No claim is made that every corrected `w=2,3` route fails.
- No paper TeX is changed.
