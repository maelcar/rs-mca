# Cycle 12 Alternative Lens: Base-Component Complete Intersection

Status: AUDIT / EXPERIMENTAL / EXACT_NEW_WALL.

This note records a route refinement after the Cycle 12 `t=2,j=3` audit. It is
not a proof of the slope bound, but it identifies a better first attack than
the current slope-fiber-collapse phrasing.

## Setup

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `D=F_p` in the finite scanner.
- `q_chal` unused.
- `t=sigma=2`.
- `j=n-a=3`, so `a=n-3`, `k=n-5`.
- `E in F[X]`, `deg E=2`, separated and nonzero on `D`.
- `Bnum`, `deg Bnum<2`, `[Bnum]_E != 0`.

Cycle 12 records the bad-line landing equation as

```text
Delta(tau_1,tau_2,tau_3)=0,
```

where `Delta` is an `F`-valued quadric and `tau_i=e_i(T)` lie in `B`.

## Crack

The phrase "one quadric in three variables" is potentially misleading over the
source ledger. Since the variables are in `B` but the value is in `F=B+alpha B`,
the single displayed equation is generally the pair

```text
Delta_0(tau_1,tau_2,tau_3)=0,
Delta_1(tau_1,tau_2,tau_3)=0
```

of two `B`-valued quadrics.

Thus the generic landing locus is not a surface of size about `p^2`; it is a
complete-intersection curve of size about `p`. In that case

```text
C2 <= #landings = O(p)=O(n)
```

before any fixed-slope fiber-collapse theorem is needed.

The right wall may therefore be:

```text
W-F1-AA-RES-T2J3-BASE-COMPONENT-COMPLETE-INTERSECTION
```

rather than fixed-slope fiber collapse.

## Finite Evidence

Added scanner:

```text
../local_checks/20260618_cycle12_base_component_rank_scan.py
```

It evaluates `Delta` on all of `B^3`, interpolates the two base components as
quadrics, checks whether their coefficient vectors span dimension `2` over
`B`, and counts both all base zeros and split-cubic zeros.

Run:

```text
python3 local_checks/20260618_cycle12_base_component_rank_scan.py
```

Observed summary:

```text
p=7:  zeros_all_B3 in [6,11],  coeff_component_rank=2 in all 8 trials
p=11: zeros_all_B3 in [9,12],  coeff_component_rank=2 in all 8 trials
p=17: zeros_all_B3 in [15,22], coeff_component_rank=2 in all 5 trials
```

For every printed trial, `zeros_all_B3` was about `p`, not `p^2`, and the split
landings had `max_slope_fiber<=1`. The latter fiber observation is only random
evidence and should not be promoted to a theorem.

## What This Suggests

The next proof target should be:

1. Write `Delta=Delta_0+alpha Delta_1` with `Delta_i in B[tau_1,tau_2,tau_3]`.
2. Prove that `Delta_0` and `Delta_1` have no common surface component outside
   classified global/tangent/low-degree resonance strata.
3. Use a degree bound for the complete intersection to get
   `# {tau in B^3 : Delta(tau)=0}=O(p)` when `D=F_p`.
4. Conclude `C2<=O(p)=O(n)` for the `D=F_p`, `t=2,j=3` finite regime.

This route bypasses the need to prove small fixed-slope fibers. In fact, small
fixed-slope fibers may be the wrong generic expectation for arbitrary affine
lines in cubic-coefficient space: a line of monic cubics over `F_p` can contain
`Theta(p)` split cubics. The useful bound is on total landings, not on every
fiber.

## Failure Modes To Classify

The complete-intersection route can fail if:

- all coefficients of `Delta` lie in a one-dimensional `B`-subspace of `F`,
  so the `F`-valued equation is really only one base equation;
- `Delta_0` and `Delta_1` share a common linear or quadratic factor;
- the shared component supports many split cubics and the slope map is not
  collapsed on that component.

These cases should be treated as either resonance lemmas or counterpacket
targets. A shared component alone is not automatically a counterpacket, because
the slope map may be constant or low-valued there.

## What Not To Claim

Do not claim:

- a proof of `W-F1-AA-RES-T2J3`;
- a proof of `conj:B`;
- any result for arbitrary `D subset B` with `|D|<<p`;
- any result above corrected reserve;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK consequence.

This is a source-valid attack refinement plus finite evidence.
