# Cycle 14 Prompt: Base-Component Resonance Wall

You are a skeptical mathematical research agent for the RS-MCA / Proximity
Prize repository. Work only from the provided source/context files. Do not edit
the main papers. Keep field ledgers separate:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.

Target:

```text
W-F1-AA-RES-T2J3-BASE-COMPONENT-RESONANCE
```

Setup:

- `D=F_p` for the first finite target.
- `w=w0+alpha w1`, arbitrary base anchors `w0,w1:D->B`.
- `E in F[X]` separated, aperiodic, `deg E=t=2`, nonzero on `D`.
- `Bnum` has `deg Bnum<2`, `[Bnum]_E != 0`.
- balanced support ledger: `a=k+t`, `sigma=t=2`.
- finite regime: `j=n-a=r-t=3`, so `a=n-3`, `k=n-5`.
- `T=D\\S`, `|T|=3`, `tau_i=e_i(T) in B`.

Banked Cycle 13 facts:

```text
Delta = Res(L_T,E) * ( [I_S]_E wedge [Bnum]_E ),
Res(L_T,E) != 0 on valid supports.
```

Writing

```text
Delta=Delta_0+alpha Delta_1,
Delta_i in B[tau_1,tau_2,tau_3],
```

the two base quadrics are coprime off

```text
R0 = { [W]_E wedge [Bnum]_E = 0 },
Ra = { Delta in F^* \\bar B[tau] },
Rb = { Delta has a \\bar B-linear factor }.
```

Off `R0 union Ra union Rb`, `C2=O(p)=O(n)`.

Task:

1. Analyze `Ra` and `Rb` directly.
2. Determine whether source hypotheses already exclude either resonance.
3. If a resonance can occur, decide whether the slope image still has `O(p)`
   size or can be `Theta(p^2)` on `D`-split cubics.
4. Produce one of:
   - BANKABLE_LEMMA: slope collapse or `O(p)` bound on `Ra`/`Rb`;
   - COUNTERPACKET: source-valid family on `Ra`/`Rb` with many distinct slopes;
   - ROUTE_CUT: source assumptions exclude the resonance;
   - EXACT_NEW_WALL: a sharper invariant replacing `Ra`/`Rb`.

Do not spend the run reproving the generic complete-intersection lemma. Work
only where `Delta_0,Delta_1` share a surface component.

Do not claim:

- a full proof of `conj:B`;
- any result above corrected reserve unless explicitly verified;
- any `q_gen` collapse;
- any protocol/MCA/CA/list-decoding/line-decoding/SNARK consequence.

Expected final classification:

`PROOF`, `BANKABLE_LEMMA`, `COUNTERPACKET`, `ROUTE_CUT`, or `EXACT_NEW_WALL`.
