# Cycle 16 Prompt: Rank/Determinant Resonance Wall

You are a skeptical mathematical research agent for the RS-MCA / Proximity
Prize repository. Work only from the mounted source/context files. Do not edit
the main papers. Keep the field ledgers separate:

- `B=F_p`, generated/entropy/base field, `q_gen=p`.
- `F=F_{p^2}`, extension/line field, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, so `n=p`.

Target:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DETERMINANT
```

This is the current residual wall after Cycle 15. Do not reprove the Cycle 13
generic complete-intersection lemma or the Cycle 14 slope-map setup. Attack the
rank/determinant obstruction directly.

## Source Context To Read

Read these first:

- `DIRECTOR_STATE.md`
- `ROUTE_BOARD_CURRENT.md`
- `ACTIVE_WALLS.md`
- `BANKED_LEMMAS.md`
- `CUTS_AND_FALSE_ROUTES.md`
- `NEXT_PROMPT_QUEUE.md`
- `current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE15_SURFACE_SLOPE_FIBER_AUDIT.md`
- `current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle15_forced_ra_slope_scan_certificate.md`

## Setup

- `w=w0+alpha w1`, arbitrary base anchors `w0,w1:D->B`.
- `E in F[X]` separated, aperiodic, `deg E=t=2`, nonzero on `D`.
- `Bnum` has `deg Bnum<2`, `[Bnum]_E != 0`.
- balanced support ledger: `a=k+t`, `sigma=t=2`.
- finite regime: `j=n-a=r-t=3`, so `a=n-3`, `k=n-5`.
- `T=D\S`, `|T|=3`, `tau_i=e_i(T) in B`.
- Work off `R0={ [W]_E wedge [Bnum]_E=0 }` unless you explicitly analyze it.

Let

```text
A=F[X]/E,
b=[Bnum]_E.
```

Cycle 14 gave affine-linear `A`-valued forms:

```text
iota(tau)=A0(tau_1,tau_2)-tau_3[W]_E,
mu(tau)=B0(tau_1,tau_2)-tau_3 b.
```

Landing `[I_S]_E=z b` is equivalent to

```text
L_z(tau):=iota(tau)-z mu(tau)=0 in A.
```

Off `R0`, `{[W]_E,b}` is an `F`-basis of `A`. Expand

```text
A0=p1[W]_E+p2 b,
B0=q1[W]_E+q2 b,
```

where each `p_i,q_i` is affine-linear in `(tau_1,tau_2)`.

Cycle 15 wrote the `B`-linear part of `L_z:B^3 -> A ~= B^4` as columns

```text
c1(z) = (p1^1 - z q1^1)[W]_E + (p2^1 - z q2^1)b,
c2(z) = (p1^2 - z q1^2)[W]_E + (p2^2 - z q2^2)b,
c3(z) = -[W]_E + z b.
```

Audit warning: verify these columns against the Cycle 15 audit before using
them. If you find an index mismatch in any mounted source/context file, record
it explicitly as AUDIT and then proceed with the corrected formula.

For fixed `z`, rank `3` gives one affine determinant consistency condition

```text
Q(z_0,z_1)=det_{4x4}[c1(z) | c2(z) | c3(z) | c0(z)].
```

The safe dichotomy is:

- `Q!=0`: slope set is a bounded-degree curve over `B`, hence `O(p)`.
- `Q==0` identically: possible large-slope regime, but only if there are enough
  distinct `D`-split cubics and the slope map is not infinitely folded.

## Task

Attack the wall through one of these lenses, in order:

1. BANKABLE_LEMMA: prove that on every source-valid `Ra` or `Rb` resonance
   stratum, either `Q!=0` or another explicit determinant/rank condition forces
   `O(p)=O(n)` slopes.

2. COUNTERPACKET: construct source-valid data with `Q==0` identically and
   `Theta(p^2)=Theta(q_line)` distinct slopes on distinct `D`-split cubics.
   A finite example alone is not enough unless you also give a scaling law.
   Keep it sub-reserve unless reserve hypotheses are actually changed.

3. ROUTE_CUT: prove that the banked source hypotheses exclude the bad
   `Q==0` resonance subcase. This must be a theorem, not a genericity guess.

4. EXACT_NEW_WALL: reduce to the smallest sharper invariant, preferably:
   a symbolic classification of `Q==0`, a determinant-minor scanner with exact
   pass/fail thresholds, or a theorem about split-cubic density on the
   determinant-zero curve.

## Required Output Discipline

- Tag every mathematical assertion as PROOF, BANKABLE_LEMMA, COUNTERPACKET,
  ROUTE_CUT, EXACT_NEW_WALL, AUDIT, or EXPERIMENTAL.
- State all parameters used: `q_gen`, `q_line`, `q_chal`, `B`, `F`, `n`, `k`,
  `rho` if used, `delta` if used, `eta`, `sigma`, `t`, `j`, and dependencies.
- If you use a scanner idea, give exact input/output/certificate format.
- If you find a typo or index mismatch in Cycle 15, record it explicitly as
  AUDIT and then proceed with the corrected formula.

## Forbidden Overclaims

Do not claim:

- rank `3` alone proves either side of the dichotomy;
- a full proof of `conj:B`;
- any result above corrected reserve unless you explicitly verify reserve
  hypotheses;
- any `q_gen` collapse;
- any protocol/MCA/CA/list-decoding/line-decoding/SNARK consequence;
- any theorem from terminal/ad transcript text;
- generic complete-intersection again as if it handled `Ra/Rb`.

Expected final classification, exactly one primary label:

```text
PROOF
BANKABLE_LEMMA
COUNTERPACKET
ROUTE_CUT
EXACT_NEW_WALL
```
