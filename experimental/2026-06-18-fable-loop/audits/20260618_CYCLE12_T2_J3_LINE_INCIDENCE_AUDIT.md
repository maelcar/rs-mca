# Cycle 12 Audit: t=2, j=3 Line-Incidence Wall

Status: EXACT_NEW_WALL / BANKABLE_LEMMA / AUDIT.

Run:

- Run id: `2026-06-18T01-29-59-199Z-cycle12-w-f1-aa-res-t2j3-37d71845`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T01-29-59-199Z-cycle12-w-f1-aa-res-t2j3-37d71845`
- Lane: VS Code credited terminal ads lane.
- Initial harness result: `ok=true`, `classification=EXACT_NEW_WALL`, but
  `answerSource=terminal_tui`.
- Harness correction: the terminal scrape was visibly malformed
  (`Ihave he fullledger`, missing spaces/letters). The clean structured Claude
  JSONL answer was present. Codex preserved the damaged scrape as
  `response_malformed_visible_terminal.md`, replaced `response.md` with the
  structured answer, and marked `run_result.json` with
  `TUI_RESPONSE_REPLACED_BY_CLAUDE_STRUCTURED_JSONL_POSTHOC`.
- Audited math artifact: clean `response.md`, copied to
  `../raw/20260618_CYCLE12_W_F1_AA_RES_T2J3_RESPONSE.md`.
- Terminal transcript is revenue/debug evidence only.
- Prompt copied to `../prompts/20260618_cycle12_w_f1_aa_res_t2j3.md`.

## Verdict

Cycle 12 is significant, but it does not prove the `t=2,j=3` slope bound.

Bank the structural algebra:

- the closed form for `Q_S` at `t=2,j=3`;
- the fact that `Q_S` depends on `e1(T),e2(T)` but not `e3(T)`;
- the bad-line landing condition is an `F`-valued quadric in
  `(e1,e2,e3)`;
- the coefficient of `e3(T)^2` is
  `wedge([W]_E,[Bnum]_E)`, so the identically-zero quadric is again a
  global/tangent resonance.

Do not bank a `C2` upper bound. At `j=3`, the Cycle 11 solution-counting
argument becomes vacuous: a quadric in three co-support parameters can have
about `n^2` split triples when `D=F_p`, `n=p`. The missing invariant is now
fiber collapse of the slope map on that quadric, not existence of a low-degree
incidence equation.

## Banked Lemma

Let `B=F_p`, `F=F_{p^2}`, `D subset B`, `|D|=n`, and write
`w=w0+alpha w1` with `w0,w1:D->B`. Let `W=interp_D(w)`. Let
`E in F[X]` be separated of degree `2`, nonzero on `D`, and let
`Bnum` have `deg Bnum<2` with `[Bnum]_E != 0`.

Use the balanced ledger

```text
t=sigma=2,     j=n-a=r-t=3,     a=n-3,     k=n-5.
```

For a support `S` of size `a`, let the co-support be `T=D\S` with
`|T|=3`, and put

```text
tau_i=e_i(T),       E_i=e_i(D),
W_m=[X^m]W.
```

Euclidean division

```text
W=L_S Q_S+I_S,      deg I_S<a
```

gives `deg Q_S<=2`, and coefficient comparison gives

```text
Q_S =
  W_{n-1} X^2
  + (W_{n-2}+W_{n-1}E_1) X
  + (W_{n-3}+W_{n-2}E_1+W_{n-1}(E_1^2-E_2))
  - tau_1 (W_{n-1}X+W_{n-2}+W_{n-1}E_1)
  + tau_2 W_{n-1}.
```

For `D=F_p`, `E_1=E_2=0`, so

```text
Q_S=W_{n-1}(X^2-tau_1 X+tau_2)+W_{n-2}(X-tau_1)+W_{n-3}.
```

Thus `Q_S` is affine in `(tau_1,tau_2)` and independent of `tau_3`.

## Bad-Line Quadric

Let `A=F[X]/E`, `xi=[X]_E`, `W_E=[W]_E`, `B_E=[Bnum]_E`, and
`L_{D,E}=[L_D]_E`. Let

```text
lambda=[L_T]_E,      mu=[Q_S]_E.
```

Since `E` is nonzero on `D`, `lambda` is a unit. The bad-line landing condition

```text
[I_S]_E=z[Bnum]_E for some z in F
```

is equivalent to

```text
Delta(T) := (W_E lambda - L_{D,E} mu) wedge (B_E lambda)=0.
```

Writing `lambda=lambda_0-tau_3` with
`lambda_0=xi^3-tau_1 xi^2+tau_2 xi`, the clean answer derives

```text
Delta =
  (W_E wedge B_E)(tau_3^2-Tr(lambda_0)tau_3+N(lambda_0))
  - <mu,lambda_0> + tau_3 <mu,1>,

<x,y>=(L_{D,E}x) wedge (B_E y).
```

Consequently `Delta` is a quadric in `(tau_1,tau_2,tau_3)` and

```text
[tau_3^2] Delta = W_E wedge B_E.
```

This is the `j=3` analogue of Cycle 11's leading-coefficient diagnostic.
`Delta identically zero` is again a tangent/global resonance stratum, not a
generic positive theorem.

## Local Verification

Codex added and ran:

```text
../local_checks/20260618_cycle12_t2_j3_line_incidence_scan.py
```

The checker imports the Cycle 11 finite-field utilities and samples
`B=F_p`, `F=F_{p^2}`, `D=F_p` for `p=7,11,17`. It verifies:

- the closed-form `Q_S` formula for every `3`-point co-support;
- `Q_S` is independent of `e3(T)`;
- the direct slope test agrees with the multiplied wedge landing predicate;
- random corrected slope counts `C2` for the sampled cases.

Run result:

```text
cycle12_t2_j3_line_incidence_scan: PASS max_C2=5
```

This is experimental evidence only. It suggests random instances may have
strong slope collapse, but it does not prove the needed common-component/fiber
law and does not rule out adversarial large-`C2` sub-reserve packets.

## Current Exact Wall

Name:

```text
W-F1-AA-RES-T2J3-FIBER-COLLAPSE
```

Question:

For the `t=2,j=3` quadric `Delta=0`, bound the number of distinct slopes

```text
C2=#{ z in F : exists T, [I_S]_E=z[Bnum]_E }.
```

Equivalently, understand the fibers of the rational slope map on the split
cubic locus:

```text
T={d1,d2,d3} subset D
  -> (tau_1,tau_2,tau_3)
  -> z.
```

The missing invariant is the typical number of `D`-split cubics lying on the
line `ell_z` cut out by a fixed slope. If fibers are `Theta(n)`, then
`C2=Theta(n)` and the `t=2,j=3` law survives. If generic fibers are `O(1)`,
then `C2` can grow like `Theta(n^2)=Theta(q_line)` in this sub-reserve regime.

## What To Bank

Bank:

- `t=2,j=3` quotient closed form above;
- `Q_S` depends on `e1(T),e2(T)` and not `e3(T)`;
- bad-line landing is a quadric condition in `(e1,e2,e3)`;
- `[e3(T)^2]Delta=wedge([W]_E,[Bnum]_E)`;
- Cycle 11's conic solution-counting mechanism dies at `j=3`;
- the exact next wall is slope-fiber collapse on the split-cubic locus.

## What Not To Bank

Do not bank:

- a proof of `conj:B`;
- any upper or lower `C2` bound for `t=2,j=3`;
- a counterpacket to the corrected reserve conjecture;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK ledger
  consequence;
- any extension to `j>=4` or `t>=3`.

## Field Ledger

- `q_gen=p`, `B=F_p`: base/generated field for `D`, `w0`, `w1`, locators,
  and co-support elementary data `tau_i`.
- `q_line=p^2`, `F=F_{p^2}`: extension field for `E`, `Bnum`, residues in
  `F[X]/E`, determinants, and slopes `z`.
- `q_chal`: unused.

No field-ledger merger is claimed.

## Parameter Ledger

- `n=|D|`, sampled with `D=F_p`, so `n=p`.
- `t=deg E=2`.
- `sigma=a-k=2`.
- balanced ledger: `a=k+t=n-3`, hence `k=n-5`.
- `r=n-k=5`.
- `j=n-a=r-t=3`.
- co-support order: `|T|=3`.
- quotient degree: `deg Q_S<=j-1=2`.
- numerator: `deg Bnum<2`, `[Bnum]_E != 0`.
- bad-line codimension in `F[X]/E`: `t-1=1`.
- reserve: `eta=sigma/n=2/n`, sub-reserve.

## Harness Note

This run exposed a wrapper bug. The clean Claude JSONL answer used a Markdown
heading `## Classification: EXACT_NEW_WALL`, while the damaged terminal scrape
contained a bare smashed `Classification:EXACT_NEW_WALL`. The wrapper's
classification regex initially recognized only the terminal scrape. Codex
patched `/Users/danielcabezas/packy-fable-ui/scripts/credit_surface_runner.mjs`
to accept Markdown heading classification lines. Future VS Code credited runs
should prefer structured JSONL in this case.
