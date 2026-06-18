# Cycle 13 Audit: Base-Component Complete Intersection

Status: BANKABLE_LEMMA / EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-18T04-00-53-446Z-cycle13-base-component-complete-intersection-845b6a0d`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T04-00-53-446Z-cycle13-base-component-complete-intersection-845b6a0d`
- Lane: isolated RS-MCA VS Code credited terminal ads lane.
- Launcher: `/Users/danielcabezas/packy-fable-ui/.codex-vscode-launchers/rs-mca-current`
- Initial harness result: `HARNESS_MALFORMED_VISIBLE_TERMINAL`; no
  `response.md` was emitted.
- Harness correction: the terminal scrape was malformed, but the clean
  structured Claude recovery `response_recovered_claude_jsonl.md` was present
  and contained no ad strings, terminal chrome, ANSI escapes, prompt echo, or
  sentinel line. Codex promoted it to `response.md` and marked the run metadata
  with `TUI_VISIBLE_TERMINAL_MALFORMED_RECOVERED_FROM_CLAUDE_JSONL_POSTHOC`.
- Audited math artifact: clean `response.md`, copied to
  `../raw/20260618_CYCLE13_BASE_COMPONENT_COMPLETE_INTERSECTION_RESPONSE.md`.
- Terminal transcript is revenue/debug evidence only.

## Verdict

Cycle 13 is significant. It does not prove the full RS-MCA prize problem, and
it does not settle all `t=2,j=3` cases. It banks a conditional/generic
complete-intersection lemma and sharpens the exact wall to a resonance locus.

The previous Cycle 12 wall described the landing condition as one `F`-valued
quadric

```text
Delta(tau_1,tau_2,tau_3)=0
```

in base variables `tau_i in B`. Cycle 13 correctly attacks this through the
field ledger:

```text
Delta=Delta_0+alpha Delta_1,
Delta_i in B[tau_1,tau_2,tau_3].
```

Thus, generically, landing is two base-field quadratic equations in three base
variables, so the landing locus is curve-sized `O(p)`, not surface-sized
`Theta(p^2)`.

## Banked Lemma

Keep ledgers separate:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`.
- `t=sigma=2`.
- `j=n-a=3`, so `a=n-3`, `k=n-5`.
- `T=D\S`, `|T|=3`, `tau_i=e_i(T) in B`.

Let `A=F[X]/E`, `L_T=X^3-tau_1 X^2+tau_2 X-tau_3`, and
`W=L_S Q_S+I_S`, `L_D=L_S L_T`.

The Cycle 12 landing determinant

```text
Delta=( [W]_E[L_T]_E-[L_D]_E[Q_S]_E )
       wedge( [Bnum]_E[L_T]_E )
```

satisfies the faithful identity

```text
Delta = det(M_[L_T]_E) * ( [I_S]_E wedge [Bnum]_E )
      = Res(L_T,E) * ( [I_S]_E wedge [Bnum]_E ).
```

Because `E` is nonzero on `D` and `T subset D`, `Res(L_T,E) != 0` for every
valid co-support. Therefore `Delta=0` is equivalent to the source landing
condition `[I_S]_E in F [Bnum]_E`; the resultant factor does not create
spurious landings or a forced common component.

Cycle 13 also banks the form

```text
Delta = kappa tau_3^2 + L(tau_1,tau_2) tau_3 + Q(tau_1,tau_2),
kappa = [W]_E wedge [Bnum]_E,
```

with `L` affine-linear and `Q` quadratic over `F`. Splitting over
`F=B+alpha B` gives two base quadrics:

```text
Delta_0, Delta_1 in B[tau_1,tau_2,tau_3].
```

Outside the following resonance strata:

- `R0`: `kappa=0`, the already-known global/tangent endpoint;
- `Ra`: all coefficients of `Delta` are aligned into a one-dimensional
  `B`-subspace, equivalently `Delta in F^* \bar B[tau]`;
- `Rb`: `Delta` has a `\bar B`-linear factor, equivalently the base components
  share a surface component through reducibility/descent;

the two base quadrics `Delta_0,Delta_1` have no common surface component.
Consequently `V(Delta_0,Delta_1) subset A^3_B` is a curve of bounded degree
at most `4`, and standard finite-field degree bounds give

```text
# { tau in B^3 : Delta(tau)=0 } = O(p).
```

Since each valid landing co-support gives one such `tau`, and the slope `z` is
unique when `[Bnum]_E != 0`, this yields

```text
C2 <= #landings = O(p)=O(n)
```

for `D=F_p`, `t=sigma=2`, `j=3`, off `R0 union Ra union Rb`.

## Exact New Wall

The new residual wall is:

```text
W-F1-AA-RES-T2J3-BASE-COMPONENT-RESONANCE.
```

Question:

On the resonance strata

```text
Ra = { Delta in F^* \bar B[tau] },
Rb = { Delta has a \bar B-linear factor },
```

do many `D`-split cubics land with many distinct slopes, or does the slope map
collapse there?

This is the precise place where the older fixed-slope fiber-collapse wall may
still be needed.

## Audit Notes

The following should be verified before promoting this beyond AUDIT:

- Symbolically recompute all coefficients of `Delta`, not only the already
  banked `tau_3^2` coefficient and the representative `tau_2 tau_3`
  coefficient.
- Make the coprimality/resonance proof fully algebraic over `B` and
  `\bar B`, including edge cases where one component has zero leading
  `tau_3^2` coefficient.
- Replace the informal `4p+O(1)` language in the raw answer with a standard
  finite-field curve bound sufficient for `O(p)`.
- Determine whether `Ra` or `Rb` are only thin generic failures or can occur in
  source-valid adversarial families with many distinct slopes.

## What To Bank

Bank:

- the faithful identity
  `Delta=Res(L_T,E)*([I_S]_E wedge [Bnum]_E)`, with nonzero resultant on valid
  supports;
- the two-base-quadrics lens `Delta=Delta_0+alpha Delta_1`;
- the generic/off-resonance complete-intersection bound
  `C2<=O(p)=O(n)` for `D=F_p`, `t=sigma=2`, `j=3`;
- the resonance wall `W-F1-AA-RES-T2J3-BASE-COMPONENT-RESONANCE`.

## What Not To Bank

Do not bank:

- an unconditional `t=2,j=3` bound;
- a proof of `conj:B`;
- any claim above corrected reserve;
- any counterpacket;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK ledger
  consequence.
