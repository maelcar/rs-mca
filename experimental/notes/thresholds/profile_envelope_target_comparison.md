# Selected power-profile envelope census and target-direction boundaries

**STATUS:** `COUNTEREXAMPLE`

This status applies to the former universal prime-field, complete-envelope,
exact-`(FI)` and unsafe-target claims in PR #759 head `8cd4f4b6`, integrated
in `2633895a`.  The finite support enumerations and cross-multiplied
identity/square inequalities remain useful after the scope repair below.

The deterministic producer is
`experimental/scripts/verify_profile_envelope_target_comparison.py`; its
source-bound certificate is
`experimental/data/certificates/profile-envelope-target-comparison/cert.json`.
The Lean package is a fixed-natural-number arithmetic shadow only.  No
submission-facing TeX/PDF is changed.

## Verdict

The executable enumerates:

- the identity slice;
- complete power-fiber quotient slices `x -> x^c` and their admissible
  remainders at the listed rows; and
- exact locator-prefix images for those selected support families.

It does **not** enumerate received lines, first-match admission, Chebyshev,
planted, arbitrary partial-occupancy, balanced-core, or general residual
profiles.  Consequently it is not a complete census of the source envelope
`eq:profile-envelope` (1.6).

The previous exact prime-field decision is false.  There are no-field-drop
prime rows with exact full-codomain identity image for which a power slice has
larger realized average fiber than the identity.  The previous target verdict
also reversed a one-way implication: failure of the sufficient safe test does
not prove an unsafe row.

What survives is narrower:

1. exact selected-slice arithmetic at the printed finite rows;
2. the known tower square obstruction against the **formal ambient identity
   proxy**, not against the realized identity term;
3. exact finite full-codomain deficits, which do not by themselves decide the
   asymptotic `(FI)` condition; and
4. counterexamples that prevent promoting the selected census to a universal
   exact identity-dominance theorem.

## Source interface and ownership

The source envelope in
`experimental/asymptotic_rs_mca_frontiers.tex` is

```text
E_n(a) = 1 + (n-a+1)
       + sup_line sum_{lambda in Lambda(line,a)} (1 + barN_lambda),
barN_lambda = |Omega^0_lambda| / |Phi_lambda(Omega^0_lambda)|.
```

Each source profile has its own full support slice, boundary map, coefficient
field, effective dimension, received-line admission, and first-match cell.
The present verifier instead applies one locator-prefix map to selected raw
support families.  Those raw families can overlap and are not an owned
first-match partition.

The pointwise condition

```text
(ID)  barN_lambda <= barN_id  for every realized profile lambda
```

is a useful sufficient comparison of individual terms.  It is not an exact
finite “iff” for the complete sum: even dominated terms contribute additive
mass, and exact target work must retain the received-line sum and ledger
overhead.  At exponent scale, a subexponential profile count lets a maximum
replace a sum, but the nontrivial upper directions still consume the open
`(PEU)`/`(FI)` payments and `(RC)` recorded in
`profile_envelope_completeness.md`.  The general no-drop/field-drop decision
uses the per-folding window, not the former scalar “no field drop iff” headline.

The formal identity quantity

```text
barN_id^formal = C(n,a) |B|^{-w}
```

is an ambient pigeonhole proxy.  The realized identity quantity is
`C(n,a)/L_id`, where `L_id` is the actual locator-prefix image.  They are
equal only under exact full-codomain saturation.  The source asymptotic
condition `(FI)` is weaker:

```text
L_id >= exp(-o(n)) |B|^w.
```

A one-row factor-`p` deficit proves exact non-surjectivity, not failure of
that asymptotic condition.

## Exact prime counterexamples

### The packet's own GF(13) row

For `D=F_13^x`, `n=12,a=6,k=3,w=2`,

```text
identity: |Omega|=924, L=169, barN=924/169;
c=2,r=0: |Omega|=20,  L=13,  barN=20/13;
c=3,r=0: |Omega|=6,   L=1,   barN=6;
c=4,r=2: |Omega|=84,  L=66,  barN=14/11;
c=6,r=0: |Omega|=2,   L=1,   barN=2.
```

Thus the square is identity-dominated, but the `c=3,r=0` cell violates
literal `(ID)`:

```text
6 > 924/169                  (1014 > 924).
```

It is shallow and bounded by the separate deep term `n-a+1=7`.  That makes it
compatible with the structural exponent wrapper; it does not make the former
exact “identity dominates every scale/remainder” sentence true.

### A deep GF(19) no-drop boundary

For `D=F_19^x`, `n=18,a=8,k=4,w=3`, the identity image fills the exact
codomain:

```text
identity: |Omega|=43758, L=6859=19^3, barN=43758/6859;
c=2,r=0: |Omega|=126, L=19,             barN=126/19.
```

There is no subfield drop, yet

```text
126 * 6859 = 864234 > 831402 = 43758 * 19.
```

Hence prime base + no field drop + exact identity saturation does not imply
literal finite `(ID)`.

There is also a simple shallow family.  For
`D=F_p^x,n=p-1,a=p-3,k=p-5,w=1`,

```text
barN_id = (p-1)(p-2)/(2p),
barN_c=2 = (p-1)/2,
deep = 3.
```

The square exceeds the identity for every odd `p`, and exceeds the deep term
for `p>=11`.  The verifier checks `p in {11,13,17,19,23,29,31,37,41}`.
These are exact finite boundaries; they do not refute an exponent statement
that absorbs polynomial factors.

## Tower rows: formal proxy versus realized scale

At `GF(49),n=12,a=6,k=3,w=2`, the realized identity average is
`924/319`.  The square is `20/7`, so the identity still wins at realized
scale.  Against the much smaller formal proxy `924/2401`, all four selected
power cells exceed it:

```text
(c,r,barN) = (2,0,20/7), (3,0,6), (4,2,14/11), (6,0,2).
```

The `c=3` cell, not the square, is the selected-inventory leader.

At `GF(121),n=20,a=10,k=7,w=2`,

```text
formal identity = 184756/14641;
realized identity = 184756/1331 = 16796/121;
square = 252/11.
```

Therefore

```text
realized identity > square > formal identity.
```

The selected complete-power inventory is

```text
(c,r,|Omega|,L,barN)
(2,0,  252,  11, 252/11)
(4,2,  660, 190, 66/19)
(5,0,    6,   1, 6)
(10,0,   2,   1, 2).
```

This preserves the paper's tower obstruction against the formal ambient proxy.
It supplies no finite counterexample to realized-scale `(ID)`.

## Exact full-codomain controls

On the smooth `GF(121)` coset the identity image has
`L_id=1331=11^3<11^4=14641`: an exact factor-11 deficit.

The former generic-domain control stopped after 60,000 of 184,756 supports and
could only show a larger partial image than 1331.  The repaired verifier
completes the same deterministic generic-domain census:

```text
|Omega|=184756, L_id=9359, max fiber=57, ambient=14641.
```

The generic image is larger than the smooth-coset image but still does not fill
the codomain.  Neither one-row deficit decides asymptotic `(FI)`.

## Target direction

For `B*=26`, the legacy numbers are:

```text
formal identity proxy                         26
formal identity + square proxy                50
formal identity + all selected power cells    65
realized identity selected budget            152
realized identity + square selected budget   176
realized identity + all selected power cells 191
```

The values 65 and 191 sum the verifier's selected raw power families.  They are
not asserted to equal the source envelope because received-line/first-match
co-realization and the other profile classes are not modeled.

The only valid target conclusion is:

> the formal proxy passes at 26, while the selected realized safe-side tests do
> not certify safety at 26.

The source safe implication is one-way: `E<=B*` implies safe.  Its failure
does not imply unsafe.  No lower-reserve or actual bad-slope computation is
performed here, and no actual threshold movement is claimed.

## Certificate and Lean scope

The repaired JSON certificate has:

- a canonical payload hash;
- SHA-256 bindings for this note, the verifier, the Lean source, the structural
  completeness note, the identity-window source, and the frontiers source;
- exact negative-control rows and target-direction labels; and
- fail-closed semantic/source validation in the producer.

The Lean package compiles without `sorry`, `admit`, or custom axiom
declarations. It proves fixed natural-number/binomial inequalities only. In
particular, `tower121_identity_full_codomain_deficit` proves the numeral
statement `1331<11^4`; it does not formalize or refute asymptotic `(FI)`. No
universal prime-field, first-match, complete-envelope, or target theorem is in
Lean.

## Producer and consumer interlocks

- PR #520 head `73525004`: envelope formula and finite brackets only.
- PR #524 head `5fe12fba`: records input 4 as open.
- PR #542 head `dcda4e9f`: identity-window source.
- PR #606 head `96dc5370`: general per-folding window repair.
- PR #688 head `48b6487d`: structural wrapper with `(PEU)` open and nontrivial
  upper directions conditional.
- PR #713 head `d78ea57e` and PR #714 head `1df8a072`: adjacent residual
  ledgers; neither is closed by this packet.
- PR #760 head `dabf6510`: same-wave motivational consumer.  Its independent
  theorem does not use #759, and its stale “#759 open” status is repaired
  separately.

The current v9.2 submission package continues to leave profile exhaustion,
payment, `(RC)`, and add-back open.  This repair does not edit that package.

## Replay

From repository root:

```bash
python3 experimental/scripts/verify_profile_envelope_target_comparison.py
python3 -O experimental/scripts/verify_profile_envelope_target_comparison.py
python3 experimental/scripts/verify_profile_envelope_target_comparison.py --tamper-selftest
python3 -O experimental/scripts/verify_profile_envelope_target_comparison.py --tamper-selftest
```

The normal and optimized runs must agree exactly.  Both tamper modes reject the
arithmetic, certificate-row, and source-hash mutations.  Unknown options fail
closed.

No complete profile envelope, witness-exhaustive first-match atlas, universal
prime-field theorem, asymptotic `(FI)` verdict, actual safe/unsafe row, target
threshold, deployed certificate, or submission theorem is claimed.
