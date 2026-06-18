# Cycle 12 Local Note: t=2, j=3 Quotient Formula And Incidence Wall

Status: BANKABLE_LEMMA / EXACT_NEW_WALL / EXPERIMENTAL.

This note is Codex-local work performed while the Cycle 12 Fable run was still
active. It should be audited against the clean Fable `response.md` before being
promoted into the route board.

## Setup

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D subset B`, scanner uses `D=F_p`.
- `t=sigma=2`.
- `j=n-a=3`, hence `a=n-3`, `k=n-5`.
- `E in F[X]`, `deg E=2`, separated, nonzero on `D`.
- `Bnum`, `deg Bnum<2`, `[Bnum]_E != 0`.

Let `W=interp_D(w)`, `T=D\S` with `|T|=3`, and write

```text
e1=e1(T),     e2=e2(T),     e3=e3(T),
D1=e1(D),     D2=e2(D).
```

Let

```text
A=[W]_{n-1},     B=[W]_{n-2},     C=[W]_{n-3}.
```

## Local Derivation

Since `I_S=interp_S(w)` has degree `<a=n-3`, the top three coefficients of

```text
W = L_S Q_S + I_S
```

determine the degree-`<=2` quotient. The resulting closed form is

```text
Q_S =
  A X^2
  + (B + A(D1-e1)) X
  + C + B(D1-e1) + A(D1^2-D2-D1 e1+e2).
```

So `Q_S` depends on `e1(T)` and `e2(T)`, but not on `e3(T)`.

This is the precise way the Cycle 11 rigidity breaks:

- at `j=2`, `Q_S` depends only on `e1(T)`;
- at `j=3`, `Q_S` depends on `e1(T),e2(T)`;
- the multiplied landing condition still sees `e3(T)` through `[L_T]_E`.

Bad-line landing remains

```text
[I_S]_E in F [Bnum]_E
```

equivalently, after multiplying by `[L_T]_E`,

```text
wedge([W]_E [L_T]_E - [L_D]_E [Q_S]_E,
      [Bnum]_E [L_T]_E) = 0.
```

For `t=2`, this is an `F`-valued quadratic condition in
`(e1,e2,e3)`. Over `B=F_p`, it is two quadratic equations in three base
variables. Generic intersection should be curve-like and give small `C2`, but
a shared-component/common-factor resonance could permit much larger families.

## Scanner

Added:

```text
local_checks/20260618_cycle12_t2_j3_line_incidence_scan.py
```

It imports the Cycle 11 finite-field utilities and checks:

- the closed-form `Q_S` formula for every `3`-point co-support;
- that `Q_S` is independent of `e3`;
- the direct bad-line slope predicate agrees with the multiplied wedge
  predicate;
- random corrected slope counts `C2` for `p=7,11,17`.

Run result:

```text
cycle12_t2_j3_line_incidence_scan: PASS max_C2=5
```

Observed random counts were tiny (`C2<=5`) across the sampled cases. This is
only experimental evidence and does not prove the corrected reserve statement.

## What To Bank

Bank after audit:

- the explicit `t=2,j=3` quotient formula above;
- `Q_S` is independent of `e3(T)`;
- the landing equation is a quadratic `F`-valued incidence condition in
  `(e1,e2,e3)`;
- the next exact wall is common-component/resonance control for the two
  `F_p`-components of that condition on the elementary-symmetric image of
  `3`-subsets.

## What Not To Bank

Do not bank:

- a proof of `conj:B`;
- a proof of the full `W-F1-AA-RES-T2J3` slope bound;
- a `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK ledger
  consequence;
- random finite scan output as proof.
