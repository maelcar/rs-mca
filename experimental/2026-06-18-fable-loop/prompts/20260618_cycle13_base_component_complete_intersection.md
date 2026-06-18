# Cycle 13 Prompt: Base-Component Complete Intersection Attack

You are a skeptical mathematical research agent for the RS-MCA / Proximity
Prize repository. Work only from the provided source/context files. Do not edit
the main papers. Keep the field ledgers separate:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.

Target:

```text
W-F1-AA-RES-T2J3-BASE-COMPONENT-COMPLETE-INTERSECTION
```

Context:

Cycle 12 established the `t=sigma=2`, `j=n-a=3` quotient formula. For
`D=F_p`, `T=D\\S`, `|T|=3`, and `tau_i=e_i(T)`,

```text
Q_S=W_{n-1}(X^2-tau_1 X+tau_2)+W_{n-2}(X-tau_1)+W_{n-3}.
```

The bad-line landing condition is

```text
Delta(tau_1,tau_2,tau_3)=0
```

where

```text
Delta=( [W]_E[L_T]_E-[L_D]_E[Q_S]_E )
       wedge( [Bnum]_E[L_T]_E )
```

is an `F`-valued quadric in the base variables `tau_i in B`.

Crack to investigate:

Since `Delta` is `F`-valued but `tau_i in B`, write

```text
Delta=Delta_0+alpha Delta_1,
Delta_i in B[tau_1,tau_2,tau_3].
```

So the landing condition is generally two base-field quadrics, not one. If
`Delta_0` and `Delta_1` have no common surface component, then for `D=F_p`
the landing set is curve-sized, `O(p)`, and

```text
C2 <= #landings = O(p)=O(n).
```

Task:

1. Derive explicit expressions, or enough coefficient diagnostics, for
   `Delta_0,Delta_1`.
2. Prove or refute that `Delta_0,Delta_1` have no common linear or quadratic
   factor outside classified global/tangent/low-degree resonance strata.
3. If coprimality is true, give a clean finite-field point-count argument
   proving `# {tau in B^3 : Delta(tau)=0}=O(p)` for `D=F_p`.
4. If coprimality fails, determine whether the shared component gives:
   - a harmless low-slope resonance,
   - a route cut already covered by tangent/global cases, or
   - a genuine counterpacket with many distinct slopes.

Do not spend the run:

- rederiving the Cycle 12 quotient formula except as needed;
- proving fixed-slope fibers are `O(1)`;
- bounding raw residue cardinality `C1`;
- using the `sigma=1` endpoint;
- claiming any `q_gen` collapse;
- claiming protocol/MCA/CA/list-decoding/line-decoding/SNARK consequences.

Expected final classification:

`PROOF`, `BANKABLE_LEMMA`, `COUNTERPACKET`, `ROUTE_CUT`, or `EXACT_NEW_WALL`.
