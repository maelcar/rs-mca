# Cycle 12 Prompt: Attack W-F1-AA-RES-T2J3

You are Fable/Opus 4.8 acting as a skeptical mathematical co-director for the
RS-MCA / Proximity Prize project.

Read the project source files first:

- `DIRECTOR_STATE.md`
- `ROUTE_BOARD_CURRENT.md`
- `ACTIVE_WALLS.md`
- `BANKED_LEMMAS.md`
- `CUTS_AND_FALSE_ROUTES.md`
- `NEXT_PROMPT_QUEUE.md`
- `README_FOR_FABLE.md`

Use the `.tex` source context referenced there, especially
`slackMCA_v3.tex:def:residue`, `thm:normalform`, `prob:perfiber`, `conj:B`,
and `rem:aper`, but do not edit main papers.

## Current Banked State

Cycle 11 banked the first finite bad-line incidence regime:

```text
t=sigma=2,      j=n-a=r-t=2,      a=n-2,      k=n-4.
```

For `W=interp_D(w)`, `W=L_S Q_S+I_S`, `I_S=interp_S(w)`, and co-support
`T=D\S={d1,d2}`, Cycle 11 proved

```text
Q_S = C(X-s_T)+C1
```

and bad-line landing

```text
[I_S]_E = z[Bnum]_E
```

is equivalent to one conic `det(s_T,p_T)=0`, giving `C2=O(n)` under the stated
nonresonance hypotheses. This is only `t=2,j=2`; do not reprove it.

## Target

Attack the next finite wall:

```text
W-F1-AA-RES-T2J3
```

Use the same source-corrected bad-line slope count, not raw residue count:

```text
C2 = #{ z in F : exists noncontained a-subset S with
       [interp_S(w)]_E = z[Bnum]_E }.
```

Work in the concrete regime:

- `B=F_p`, `F=F_{p^2}`;
- `D subset B`, and start with `D=F_p` if useful;
- `w=w0+alpha w1`, with arbitrary base anchors `w0,w1:D->B`;
- `E in F[X]` separated/aperiodic, `deg E=t=2`, nonzero on `D`;
- `Bnum` has `deg Bnum<2`, `[Bnum]_E != 0`;
- balanced ledger `a=k+t`, `sigma=t=2`;
- `j=n-a=r-t=3`, hence `a=n-3`, `k=n-5`, `deg Q_S<=2`;
- co-support `T=D\S` has size 3, with elementary parameters
  `e1(T), e2(T), e3(T)`.

## What To Do

1. Derive the exact closed form for the quotient `Q_S` in terms of the
   top coefficients of `W` and the size-3 co-support elementary symmetric
   parameters.
2. Translate bad-line landing into explicit determinant/incidence equations in
   the `t=2` residue algebra `F[X]/E`.
3. Decide whether this gives a source-valid bound on `C2`, or whether it
   permits a counterpacket with too many slopes.
4. If a full proof is out of reach, isolate the exact next missing invariant:
   degree, dimension, common-component condition, resonance stratum, or finite
   scanner target.

## Forbidden Moves

- Do not bank raw residue cardinality `C1` as the MCA object.
- Do not use the `sigma=1` endpoint as an above-reserve refutation.
- Do not claim `q_gen` collapse.
- Do not claim protocol, MCA, CA, list-decoding, line-decoding, or SNARK ledger
  consequences.
- Do not merge `q_gen`, `q_line`, `q_chal`, `B`, and `F`.
- Do not cite Cycle 11 beyond `t=2,j=2`.

## Required Output Format

Return one of:

- `PROOF`
- `BANKABLE_LEMMA`
- `COUNTERPACKET`
- `ROUTE_CUT`
- `EXACT_NEW_WALL`

Then give:

- exact statement;
- proof or counterpacket data;
- field ledger (`q_gen`, `q_line`, `q_chal`, `B`, `F`);
- parameter ledger (`n,k,a,t,sigma,j,E,Bnum`);
- source dependencies by label;
- what Codex should bank;
- what Codex must not bank;
- a suggested verifier/checker if computation is relevant.
