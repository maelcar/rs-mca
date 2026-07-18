# Paving v9.2 retained-factor content-root guard

Status: COUNTEREXAMPLE

Claude proposed re-cutting the retained-factor content-root audit against the
immutable Paving v9.2 package; this note carries out that recut.  It gives an
exact counterexample to the universal form of RF3 in the
`Parameter-retained factor lift` assumption and identifies the missing
coefficient needed to absorb roots of the `Y`-content.  Conditional on a
content-stable degree-subtraction bridge, the corrected envelope is

```text
|S| > max(1, 2 U D_Y^2) D_Z + (r+1) D_Y.          (RF3')
```

When that subtraction bridge is unavailable, the conservative arithmetic
envelope is

```text
|S| > (1 + 2 U D_Y^2) D_Z + (r+1) D_Y.            (RF3'')
```

RF3' repairs the content coefficient only conditional on the content-stable
subtraction bridge.  RF3'' avoids that subtraction arithmetically.  The
standalone proof in
`experimental/notes/audits/paving_v9_2_rf3_global_degree_bridge.md` now
supplies the required global-degree factor lift, including its linear and
content/leading-coefficient cases.  Immutable v9.2 still states the weaker RF3
assumption, so its downstream result remains conditional.

## Immutable v9.2 source binding

The checker binds both release copies

```text
experimental/RS_MCA_Paving_v9.2.tex
experimental/RS_MCA_Paving_v9.2_source/RS_MCA_Paving_v9.2.tex
```

to the identical SHA-256 digest

```text
8e89be94dd6291dc5563897e72ae34b49880512cd37f72287b4288ff030cbbc0
```

and checks the RF3 statement, the RF4 count, and every RF6/RF7 row.  Neither
TeX copy, the PDF, nor any release hash is edited by this audit.

## Exact counterexample

Work over `F_7`, with

```text
D = {1,2,4},  n=A=3,  r=0,  K=1,  m=1,
D_X=21/10,    D_Y=1/100,    D_Z=11/10,
U=3,          V=1,          W=2.
```

Take

```text
Q(X,Y,Z)=Z,
S={0},
P_0(X)=0,
A_0=D,
u_0(x)=0,
u_1(x)=x.
```

All antecedents of the displayed assumption hold:

- The preamble has `A=K+2`.
- RF1's conditions become `1>=1`, `2>=1`, `3>0`, `21/10<3`, and
  `char(F_7)=7>0`.
- RF2's top-degree comparison is `5>3`, and its field-size comparison is
  `7>2*3/100=3/50`.
- For `Q=Z`, the `(1,K,0)`-weighted degree is `0<D_X`, the `Y`-degree is
  `0<D_Y`, and the `(0,1,1)`-weighted degree is `1<D_Z`.
- `Q(X,P_0(X),0)=0`, `deg(P_0)<K`, and
  `P_0=u_0+0*u_1` on the chosen support of size `A`.
- The old RF3 right side is

```text
2*3*(1/100)^2*(11/10) + 1/100 = 533/50000 < 1 = |S|.
```

The conclusion nevertheless fails.  Since `K=1`, both `v_0` and `v_1`
would have to be constant.  No constant over `F_7` agrees with
`u_1(x)=x` at all three distinct points `{1,2,4}`.  The verifier enumerates
all seven constants.

## Root cause and corrected envelope

Let `d_C` be the degree of the `Y`-content and put

```text
alpha = 2 U D_Y^2.
```

The claimed content-stable degree-subtraction bridge would leave `D_Z-d_C`
for the content-free factor part.  Conditional on that bridge, the
content-plus-factor charge before the final absorption step has the form

```text
d_C + alpha (D_Z-d_C) + (r+1)D_Y.               (1)
```

The earlier parametric audit records the analogous expression with `D_X`
and explicitly states that its final simplification uses
`2 D_X D_Y^2 >= 1`.  V9.2 conservatively replaces the real truncation by
the integer `U`, but universal RF1--RF3 does not impose the corresponding
guard `2 U D_Y^2 >= 1`.

Relax the integral degree `d_C` to `0<=d_C<=D_Z`.  If `alpha>=1`, (1)
decreases with `d_C`, so its content/factor part is at most
`alpha D_Z`.  If `alpha<=1`, it increases with `d_C`, so that part is at
most `D_Z`.  Hence, conditional on the content-stable degree-subtraction
bridge, the uniform arithmetic envelope is

```text
max(1, alpha) D_Z + (r+1)D_Y,
```

which is sharp for the continuous relaxation.  The integer-degree maximum
can be slightly smaller for nonintegral `D_Z`; RF3' deliberately uses the
clean continuous envelope.

That subtraction is not automatic from the degree of the specialized
content-free factor.  For example,
`R(X,Y,Z)=Z^2Y+X(Z^3+1)` is primitive and linear-separable, while at `X=0`
its content-free factor is `H=Y` of `(Y,Z)`-degree one.  Its unique lift has
coefficient `alpha_1=-(Z^3+1)/Z^2`, whose reduced numerator has degree three.
Thus a content-stable degree-subtraction bridge is needed before RF3' can be used.

Without a content-stable degree-subtraction lemma, charge the content by at
most `D_Z` and the factor part by at most `alpha D_Z` separately.  This gives
the conservative arithmetic envelope RF3'',

```text
(1+alpha)D_Z + (r+1)D_Y.
```

The companion global-degree bridge note supplies the factor-lift theorem needed
to turn this RF3'' envelope into a future-version hypothesis.  In the
counterexample, RF3' has right side

```text
11/10 + 1/100 = 111/100,
```

so the singleton `S` no longer triggers the conclusion.  At `d_C=1`, the
unabsorbed expression (1) is `50503/50000`, also already larger than `|S|`.
Adding `2 U D_Y^2 >= 1` to RF1 is a narrower content-coefficient repair only
after the content-stable degree-subtraction bridge has been proved; it does
not by itself justify replacing a global degree by a specialized
content-free degree.

## Why RF4 forces `V>=2`

Suppose instead that `V=1`.  RF1 and positive integral `m` force `m=1`.
Because `W>=V`, one has `W>0`, and RF4 reduces exactly to

```text
U W > n W,
```

so `U>n`.  On the other hand, `D_X<mA=A<=n`, and `n` is an integer, hence
`U=ceil(D_X)<=n`, a contradiction.  Thus every application through RF4 has
`V>=2`.  Since `V=ceil(D_Y)`, this gives `D_Y>1`; with positive integral
`U`, it follows that `2 U D_Y^2>1`.  Therefore, conditional on the
content-stable degree-subtraction bridge, RF3' and RF3 coincide on the entire
RF4 regime, not only on the four printed examples.

The exact checker also evaluates RF4 and the corrected threshold for all
four KoalaBear rows.  Their printed RF4 margins remain

```text
4889934
13182624
11133440
4204064
```

and their RF5 ceilings remain

```text
274589064742726105
274721012201264929
274578888391530706
274861787390229386
```

This is a nonimpact statement about the content correction only.  It does
not upgrade any conditional row to an unconditional theorem.

If the content-stable subtraction bridge is unavailable and a standalone
global-degree factor-lift bridge is proved, RF3'' gives the four exact ceilings

```text
274589064742753629
274721012201293956
274578888391562205
274861787390263486
```

All four remain below the KoalaBear 128-bit budget
`274980728111395087`.  Thus the conservative arithmetic envelope remains
in budget, although it changes the four printed numerators.  It does not by
itself establish the retained-factor lift.

## Reproduction

From the repository root:

```bash
python3 experimental/scripts/verify_paving_v9_2_retained_factor_content_guard.py --check
python3 experimental/scripts/verify_paving_v9_2_retained_factor_content_guard.py --tamper-selftest
python3 experimental/scripts/verify_paving_v9_2_retained_factor_source_audit.py --check
python3 experimental/scripts/verify_paving_v9_2_retained_factor_source_audit.py --tamper-selftest
python3 experimental/RS_MCA_Paving_v9.2_source/verify_retained_bchks_v9_2.py
python3 experimental/RS_MCA_Paving_v9.2_source/verify_paving_mca_v9_2.py
```

The checkers use only the Python standard library.  Besides checking the
exact `F_7` data, they verify the local global-degree obstruction, both v9.2
source bindings, the RF3'' ceilings, and semantic tamper rejection.

## Integration recommendation and nonclaims

Keep v9.2 immutable.  A future release repair should:

1. prove a content-stable degree-subtraction bridge and then apply RF3', or
   prove a standalone global-degree factor-lift bridge and pair it with RF3''
   when no sharper subtraction lemma is available;
2. state the proved degree ledger, rather than inferring it from the
   specialized content-free factor;
3. rebuild the PDF and rerun both bundled verifiers; and
4. refresh that new release's hashes together.

This audit does not claim that the cited Hensel steps support the full
arbitrary-parameter synthesis, does not supply either bridge, and does not
discharge the retained-factor lift.  RF3' leaves the deployed ceilings
unchanged only if a content-stable degree-subtraction bridge is proved.  RF3''
is the conservative in-budget arithmetic envelope and becomes usable only
with a standalone global-degree factor-lift bridge.
