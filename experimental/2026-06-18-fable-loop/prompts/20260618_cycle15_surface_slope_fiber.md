# Cycle 15 Prompt: Surface Slope-Fiber Wall

You are a skeptical mathematical research agent for the RS-MCA / Proximity
Prize repository. Work only from the mounted source/context files. Do not edit
the main papers. Keep the field ledgers separate:

- `B=F_p`, generated/entropy/base field, `q_gen=p`.
- `F=F_{p^2}`, extension/line field, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, so `n=p`.

Target:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER
```

This is the current residual wall after Cycle 14. Do not re-attack the generic
complete-intersection case; Cycle 13 already handles it off resonance.

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
A = F[X]/E,
b = [Bnum]_E,
m = [L_T]_E.
```

Cycle 13 banked:

```text
Delta = Res(L_T,E) * ( [I_S]_E wedge [Bnum]_E ),
Res(L_T,E) != 0
```

on every valid co-support. Off the resonance strata

```text
Ra = { Delta in F^* \bar B[tau] },
Rb = { Delta has a \bar B-linear factor },
```

the split equations `Delta_0=Delta_1=0` form a bounded-degree curve in
`B^3`, hence `C2=O(p)`.

Cycle 14 reduced the remaining resonance problem to an explicit slope map.
Define

```text
iota(tau)=m[I_S]_E=[W]_E m-[L_D]_E[Q_S]_E,
mu(tau)=m b.
```

Both are `A`-valued affine-linear forms:

```text
iota(tau)=A0(tau_1,tau_2)-tau_3[W]_E,
mu(tau)=B0(tau_1,tau_2)-tau_3 b.
```

Off `R0`, expand in the `F`-basis `{[W]_E,b}`:

```text
A0=p1[W]_E+p2 b,
B0=q1[W]_E+q2 b,
```

where `p_i,q_i in F` are affine-linear in `(tau_1,tau_2)`. Landing
`[I_S]_E=z b` is equivalent to

```text
q1 z^2-(p1-q2)z-p2=0,
tau_3=p1-z q1 in B.
```

The resonance surface `Sigma subset B^3` is either:

- `Ra`: a base quadric surface coming from `Delta in F^* \bar B[tau]`; or
- `Rb`: a base plane or surface component coming from a `\bar B`-linear factor.

The split condition is still:

```text
X^3-tau_1 X^2+tau_2 X-tau_3
```

splits into three distinct roots in `D=F_p`.

## Task

Attack the wall through one of these lenses. Prefer the first one that works:

1. BANKABLE_LEMMA: prove that on every source-valid `Ra` or `Rb` resonance
   surface, the slope image

```text
{ z in F : tau in Sigma, tau is a distinct D-split cubic, [I_S]_E=z b }
```

   has size `O(p)=O(n)`.

2. COUNTERPACKET: construct source-valid data with a resonance surface and
   `Theta(p^2)=Theta(q_line)` distinct slopes on distinct `D`-split cubics.
   Give an explicit infinite family or a finite family plus a clear scaling
   argument. Keep it sub-reserve unless reserve hypotheses are changed.

3. ROUTE_CUT: prove that the currently banked source hypotheses exclude the
   bad resonance subcase you analyze. This must be a theorem, not a genericity
   guess.

4. EXACT_NEW_WALL: reduce the question to a sharper invariant. If you cannot
   decide the slope image, isolate the smallest missing object, for example:
   a base-rationality fiber theorem for `tau_3=p1-zq1 in B`; a classification
   of `q1=0` or `B0 wedge b=0`; or a concrete finite scanner spec with exact
   equations and pass/fail thresholds.

## Forbidden Overclaims

Do not claim:

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
