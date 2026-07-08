# CAP25 v13 signed-e_m masked residual audit

Status: audit / route repair / counterpacket to an overstrong formulation.

This note records a narrow hostile-audit outcome for the row-sharp Q route
around PR #412.  It does not prove a deployed adjacent safe row, does not prove
row-sharp Q, and does not refute the p^(w/2) concentration-floor route cut in
PR #412.  Its purpose is to repair the named next target.

## 1. Board position

The current finite deployed goal is still the adjacent staircase certificate

```text
U(a0 + 1) <= B* < L(a0).
```

The exact unsafe side is already part of the v13 frontier.  The safe side still
requires the row-sharp Q atom bound and the residual finite BC chart audit.
PR #412 records that routes factoring through ordinary second moments,
Cauchy-Schwarz, or Fourier-Plancherel meet a p^(w/2) concentration floor and
are not row-sharp enough for the deployed finite budgets.

That floor survives this audit.  The repair is only to the phrase
"the crux is signed-e_m inverse".

## 2. Exact false promotion

The following promotion is too strong:

```text
A primitive signed-e_m L1 theorem for the full unpruned elementary-symmetric
coefficient is equivalent to the row-sharp Q atom, or is the theorem-facing
form of the row-sharp Q atom after first-match deletion.
```

There are two failures.

First, row-sharp Q is an L-infinity max-fiber target.  A global Fourier L1
bound is a sufficient certificate, not an equivalent reformulation.

Second, first-match deletion is a support-side deletion.  After paid cells are
removed, the relevant Fourier coefficient is not the full elementary-symmetric
coefficient e_m(v_t).  It is the masked residual coefficient

```text
E_Q(t) = sum_{M in P_Q} psi(t . Phi_w(M)),
```

where P_Q is the first-match-pruned primitive Q residual family.  In general
E_Q(t) is not e_m(v_t), nor is it obtained by simply deleting quotient or
composite frequency directions.

## 3. Correct Fourier identity

Let G be the prefix target group, with |G| = p^w, and let

```text
N_Q(z) = |{M in P_Q : Phi_w(M) = z}|,
T_Q    = |P_Q|,
E_Q(t) = sum_{M in P_Q} psi(t . Phi_w(M)).
```

Fourier inversion gives

```text
p^w N_Q(z) = T_Q + sum_{t != 0} psi(-t . z) E_Q(t).
```

Thus a row budget B_Q is equivalent to the family of phase inequalities

```text
Re sum_{t != 0} psi(-t . z) E_Q(t) <= p^w B_Q - T_Q
for every z.
```

The global L1 condition

```text
sum_{t != 0} |E_Q(t)| <= p^w B_Q - T_Q
```

is sufficient, but stronger than necessary.  It should not be stated as the
same theorem as row-sharp Q.

## 4. Toy counterpackets to raw L1 equivalence

The audit returns found small exact examples where the actual max-fiber Q
constant fits the deployed-style budget multiplier, while a primitive signed
L1 triangle route already exceeds it.

### F_17 example

Take p = 17, D = F_17^*, n = 16, m = 8, and w = 3.  Then

```text
binom(16, 8) = 12870,
p^w = 4913,
max_z N(z) = 7,
max_z N(z) / (binom(16,8)/17^3) = 2.672183...
```

One audit return computed a primitive signed-L1 triangle constant

```text
1 + L1_primitive/binom(16,8) = 10.472846...
```

The Mersenne-31 list row budget ratio recorded in the v13 board is

```text
16777215 / 1993678 = 8.4152079724...
```

So the actual max-fiber ratio can be below the M31 list multiplier while the
raw primitive L1 triangle certificate is above it.  This cuts the equivalence
between row-sharp Q and raw signed-e_m L1.

### F_23 example

For p = 23, n = 22, m = 11, and w = 4, one audit return reported

```text
max_z N(z) / avg = 3.173556...,
```

while the corresponding raw primitive L1 certificate was about

```text
69.89535...
```

Again the max-fiber target and the raw L1 route separate.

These examples are not deployed-row counterexamples.  They are counterpackets
only to the overstrong route equivalence.

## 5. Mersenne-31 list calibration

For the binding Mersenne-31 list row, the board uses

```text
p = 2^31 - 1,
a+ = 1116023,
w = 67447,
B* = 16777215,
ceil(avg) = 1993678,
B* / ceil(avg) = 8.4152079724...
```

The residual theorem is therefore constant-factor, not entropy-scale.  A
heavy residual fiber is only required to exceed a large random baseline by a
small constant factor.  Ordinary statements that require entropy-scale excess,
or that count many trades without subtracting the random baseline and common
core multiplicities, do not automatically give the finite deployed certificate.

## 6. Repaired next target

The theorem-facing target after this audit is:

```text
CAP25-V13-CHARACTER-PHASE-MASKED-SIGNED-EM-INVERSE.
```

One useful formulation is:

```text
Given the first-match-pruned primitive Q family P_Q and its masked residual
coefficients E_Q(t), prove max_z N_Q(z) <= B_Q.  Equivalently, prove the
phase inequalities

Re sum_{t != 0} psi(-t . z) E_Q(t) <= p^w B_Q - T_Q

for every z, or show that any violation forces a paid cell: quotient,
boundary-BC/SP, tangent, extension, common-GCD, rank-drop, or another named
finite residual.
```

If an L1 route is used, it must be stated as a sufficient route for the masked
residual coefficients E_Q(t), not as a full-equivalence theorem for the raw
unpruned signed e_m coefficient.

## 7. Nonclaims

This note does not claim any of the following:

- row-sharp Q is proved;
- an adjacent deployed safe row is proved;
- PR #412's p^(w/2) route cut is false;
- the raw full-population e_m coefficient controls the first-match residual;
- primitive frequency restriction is the same as first-match support deletion;
- the residual BC/SP chart decomposition is closed.

## 8. Next checks

The next useful checks are:

1. Independently replay the F_17 and F_23 toy counterpackets with a small
   script if this note is promoted beyond audit status.
2. Formulate P_Q and E_Q(t) explicitly for the Mersenne-31 list row with the
   same first-match order used by the v13 ledger.
3. Search for a finite support-side theorem saying that any constant-factor
   residual heavy fiber produces enough structured signed trades, after
   common-core multiplicity is divided out, to hit a paid cell or an explicit
   new residual.
4. Keep the saturated BC chart audit as the parallel finite wall.
