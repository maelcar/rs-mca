# Cycle 8 Audit: Twisted Readout Isomorphism

Status: BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-18T00-10-26-558Z-cycle8-w-f1-aa-res-twisted-readout-20260618-7ff35e06`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T00-10-26-558Z-cycle8-w-f1-aa-res-twisted-readout-20260618-7ff35e06`
- Lane: VS Code credited terminal ads lane.
- Harness result: `complete`, `BANKABLE_LEMMA`,
  `captureWarning=TUI_RESPONSE_REPLACED_BY_CLAUDE_STRUCTURED_JSONL`,
  `answerSource=claude_structured_jsonl`.
- Clean receipt copied to
  `../raw/20260618_CYCLE8_W_F1_AA_RES_TWISTED_READOUT_RECOVERED_CLAUDE_JSONL.md`.

## Verdict

Cycle 8 is bankable as an algebraic reduction, not as a proof of the final
proximity/MCA claim.

The twisted readout wall is resolved: in the separated quadratic case, the
twisted quotient readout is exactly the Weil-restricted form of the original
extension residue. Thus the twist itself is not a new obstruction and not a
source of field-size saving.

The residual wall is:

```text
W-F1-AA-RES-RESIDUE-COUNT:
above corrected reserve eta=sigma/n, bound the F-residue value count
S -> [interp_S(w0)+alpha*interp_S(w1)]_E in F[X]/E
by n^{1+o(1)}, for arbitrary base anchors w0,w1 and aperiodic separated E.
```

## Bankable Lemma

Assume:

- `B=F_p`, `F=F_{p^2}`.
- `tau` is the nontrivial Galois automorphism.
- `D subset B`.
- `w=w0+alpha*w1` with `w0,w1:D->B`.
- `E in F[X]`, `deg E=t`, `E` nonzero on `D`.
- Separated case: `gcd(E,E^tau)=1`, so `Ehat=E E^tau in B[X]`,
  `deg Ehat=2t`.
- Balanced support size: `a=k+t=s_delta`.
- `theta in B[X]/Ehat` is the CRT class with
  `theta == alpha mod E` and `theta == alpha^tau mod E^tau`.
- For an `a`-subset `S`, write `P_i=interp_S(w_i)`.

Then:

1. The map

```text
pi: B[X]/Ehat -> F[X]/E,  [g] -> [g]_E
```

is a ring isomorphism, and `pi(theta)=alpha`.

2. The twisted readout

```text
T_theta(S) = [P0]_Ehat + theta [P1]_Ehat
```

satisfies

```text
pi(T_theta(S)) = [interp_S(w)]_E.
```

Therefore

```text
#{T_theta(S)} = #{[interp_S(w)]_E}
```

for any support family.

3. The Cycle 7 non-absorption failure has an exact commutator:

```text
theta interp_S(w1) - interp_S(theta w1) = L_S R_S,
deg R_S <= 2t-2,
```

where `L_S=prod_{d in S}(X-d)`.

4. On `a=k+t` supports,

```text
T_theta(S)=T_theta(S')
iff [interp_S(w)]_E=[interp_S'(w)]_E
iff interp_S(w)-interp_S'(w) in E*F_{<k}[X].
```

## Proof Audit

The proof is source-valid.

- `pi` is injective: if `g in B[X]`, `deg g<2t`, and `E|g` in `F[X]`, applying
  `tau` gives `E^tau|g`; coprimality gives `Ehat|g`, so `g=0`. Cardinalities
  on both sides are `p^{2t}`, so `pi` is an isomorphism.
- The CRT definition gives `pi(theta)=alpha`.
- Since `D subset B`, support interpolation has base-field Lagrange
  coefficients, so `interp_S(w)=P0+alpha P1`.
- The commutator is divisible by `L_S` because both terms agree on every
  point of `S`; the degree bound follows from
  `deg(theta)<=2t-1`, `deg P1<k+t`, and `deg L_S=k+t`.
- The collision equivalence is the Cycle 6B kernel after applying the
  isomorphism.

## Local Verification

The finite checker:

- `../local_checks/20260618_cycle8_twisted_readout_verify.py`

checks the identities over `B=F_7`, `F=F_49`, `t=sigma=2`, `k=2`,
`a=4`, for random separated denominators and base anchors. It verifies:

- `pi(T_theta(S))=[interp_S(w)]_E`;
- distinct twisted values equal distinct residue values;
- the commutator is locator-divisible with quotient degree `<=2t-2`;
- equal twisted values imply the `E*F_{<k}` kernel condition.

Result:

```text
cycle8_twisted_readout_verify: PASS
```

## Field Ledger

- `q_gen=p`, `B=F_p`: base field for `D`, `w0`, `w1`, `Ehat`, `theta`, and
  `B[X]/Ehat`.
- `q_line=p^2`, `F=F_{p^2}`: extension field for `E`, `Bnum`, slopes, and the
  residue `[interp_S(w)]_E`.
- `q_chal`: unused; no protocol denominator or verifier challenge claim.

The key correction is that the count remains a `q_line` residue-count problem.
There is no automatic collapse to `q_gen`.

## Parameter Ledger

- `n=|D|`.
- `k=rho n`.
- `a=ceil((1-delta)n)`.
- `sigma=a-k`.
- Balanced case: `t=sigma`, so `a=k+t=s_delta`.
- `deg E=t`, `deg Ehat=2t`.
- Commutator quotient degree: `<=2t-2`.
- No quotient order, interleaving/list arity, or protocol challenge parameter
  is used.

## What To Bank

Bank:

- the ring isomorphism `B[X]/Ehat ~= F[X]/E`;
- the identity `T_theta(S)=pi^{-1}([interp_S(w)]_E)`;
- the locator-divisible commutator formula;
- the collision equivalence with the Cycle 6B kernel;
- the sharpened residual wall `W-F1-AA-RES-RESIDUE-COUNT`.

Do not bank:

- a proof of `prob:perfiber` or `conj:B`;
- any `n^{1+o(1)}` value-count bound;
- any `q_gen` field-size saving;
- `thm:exactcount` transfer to arbitrary anchors;
- `ass:extension-mca-lift`;
- protocol, line-decoding, list-decoding, CA, or MCA ledger claims.

## Next Target

Attack `W-F1-AA-RES-RESIDUE-COUNT` directly. The twist has been eliminated.
The next worker should either prove a residue-count lemma, produce a finite
balanced counterpacket, or isolate a sharper invariant inside the arbitrary
extension residue map

```text
S -> [interp_S(w0)+alpha interp_S(w1)]_E.
```
