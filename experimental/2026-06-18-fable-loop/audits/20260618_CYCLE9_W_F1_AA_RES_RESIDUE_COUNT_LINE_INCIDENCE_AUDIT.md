# Cycle 9 Audit: Residue Count Becomes Line Incidence

Status: EXACT_NEW_WALL / BANKABLE_LEMMA / AUDIT.

Run:

- Run id: `2026-06-18T00-25-32-427Z-cycle9-w-f1-aa-res-residue-count-20260618-47412c08`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T00-25-32-427Z-cycle9-w-f1-aa-res-residue-count-20260618-47412c08`
- Lane: VS Code credited terminal ads lane.
- Harness result: `complete`, `EXACT_NEW_WALL`,
  `captureWarning=TUI_VISIBLE_TERMINAL_MALFORMED_RECOVERED_FROM_CLAUDE_JSONL`,
  `answerSource=claude_structured_jsonl`.
- Clean receipt copied to
  `../raw/20260618_CYCLE9_W_F1_AA_RES_RESIDUE_COUNT_RECOVERED_CLAUDE_JSONL.md`.

## Verdict

Cycle 9 is significant. It does not prove the positive MCA/proximity claim, but
it corrects the target after Cycle 8.

Bank:

1. A locator-quotient decomposition for arbitrary anchors.
2. The distinction between raw residue value count and the source-relevant
   slope/bad-line incidence count.
3. A sharper wall:

```text
W-F1-AA-RES-LINE-INCIDENCE
```

Do not bank any `n^{1+o(1)}` incidence bound, any `q_gen` collapse, or any
protocol/MCA/list-decoding consequence.

## Bankable Structural Lemma

Let:

- `B=F_p`, `F=F_{p^2}`.
- `D subset B`, `n=|D|`.
- `w=w0+alpha*w1 : D -> F`, with `w0,w1:D->B`.
- `W=interp_D(w) in F[X]`, `deg W<=n-1`.
- `S subset D`, `|S|=a=k+t`.
- `L_S=prod_{d in S}(X-d)`.
- `I_S=interp_S(w)`, `deg I_S<a`.
- Divide `W` by `L_S`:

```text
W = L_S Q_S + I_S.
```

Then:

```text
deg Q_S <= n-a-1,
R_E(S) := [I_S]_E = [W]_E - [L_S Q_S]_E in F[X]/E.
```

Equivalently, writing the co-support size as

```text
j = n-a = r-t,
```

one has `deg Q_S<=j-1`.

This is elementary Euclidean division: the remainder has degree `<a` and agrees
with `W` on all points of `S`, so it is the support interpolant `I_S`.

## Source Compatibility

This fits the source normal form:

- `slackMCA_v3.tex:1189`, `def:residue`: active objects are slopes `z` with
  witnesses satisfying `Q_z equiv zB mod E`.
- `slackMCA_v3.tex:1197`, `thm:normalform`: `emca` is `1/q` times a maximum
  over noncontained slope counts `Lambda^{NC}`.
- `slackMCA_v3.tex:1227`, `prob:perfiber`, and `slackMCA_v3.tex:1231`,
  `conj:B`: the conjectural positive target is a packing/slope count after
  quotient-periodic separation, not a raw count of all residues.
- `slackMCA_v3.tex:1255`, `rem:aper`: quotient-periodic lines must stay
  separated.
- `slackMCA_v3.tex:1148`, `thm:exactcount`, and `slackMCA_v3.tex:737`,
  `thm:rigidcyclo`: these remain monomial/cyclotomic strata and are not
  imported to arbitrary anchors.

Cycle 8 supplies the reduction from the twisted readout to the original
extension residue `[interp_S(w)]_E`; Cycle 9 starts from that reduced object.

## Corrected Wall

Raw residues:

```text
C1 = #{ [I_S]_E : |S|=a }.
```

Source-relevant slopes:

```text
C2 = #{ z in F : exists S, [I_S]_E = z [Bnum]_E }.
```

The source object is `C2`, not `C1`. For `deg E=t`, the residue space
`F[X]/E` has `F`-dimension `t`, while the bad slope line

```text
F [Bnum]_E
```

has dimension `1` when `Bnum` is nonzero. Thus the bad line has codimension
`t-1`. The sub-reserve `sigma=1` counterpacket sits at the endpoint `t=1`,
where this codimension is zero and raw residue count equals slope count. For
`t>=2`, a raw residue-value count is not the right MCA object; the required
bound is an incidence/landing count into a codimension-`(t-1)` line.

The live target becomes:

```text
W-F1-AA-RES-LINE-INCIDENCE:
For B=F_p, F=F_{p^2}, D subset B, separated aperiodic E with deg E=t=sigma
and E nonzero on D, nonzero numerator Bnum with deg Bnum<t, arbitrary base
anchors w0,w1:D->B, and balanced support size a=k+t=s_delta, bound the number
of slopes z in F for which some a-subset S satisfies

  [interp_S(w0)+alpha interp_S(w1)]_E = z [Bnum]_E.

Equivalently, using W=L_S Q_S+I_S, bound the incidence count of the structured
locator-quotient family [L_S Q_S]_E with the affine line

  [W]_E - F[Bnum]_E

inside F[X]/E.
```

## Local Verification

The finite checker:

- `../local_checks/20260618_cycle9_locator_quotient_incidence_check.py`

checks over `B=F_7`, `F=F_49`:

- the identity `W=L_S Q_S+interp_S(w)`;
- the degree bound `deg Q_S<=n-a-1`;
- the residue identity
  `[interp_S(w)]_E=[W]_E-[L_S Q_S]_E`;
- the endpoint distinction that `t=1` has `C1=C2`;
- the `t=2` distinction that line incidence `C2` can be much smaller than
  raw residue count `C1`.

Result:

```text
cycle9_locator_quotient_incidence_check: PASS
```

Representative output includes:

```text
seed=0 t=1 C1=16 C2=16; t=2 C1=21 C2=0 supports=21
seed=1 t=1 C1=20 C2=20; t=2 C1=21 C2=2 supports=21
```

This is finite sanity evidence only. It is not an asymptotic proof.

## Field Ledger

- `q_gen=p`, `B=F_p`: base/generated field for `D`, `w0`, `w1`, and base
  locators `L_S`.
- `q_line=p^2`, `F=F_{p^2}`: extension field for `E`, `Bnum`, residues, and
  slopes `z`.
- `q_chal`: unused; no protocol challenge or denominator saving claim.

## Parameter Ledger

- `n=|D|`.
- `k=rho n`.
- `a=ceil((1-delta)n)=s_delta`.
- `sigma=a-k`.
- Balanced ledger: `t=sigma`, so `a=k+t`.
- `r=n-k`.
- Co-support size: `j=n-a=r-t`.
- `deg E=t`.
- `deg Bnum<t`.
- `deg Q_S<=j-1`.
- Bad line codimension in `F[X]/E`: `t-1`.
- No quotient order, interleaving/list arity, or protocol parameter is used.

## What To Bank

Bank:

- the locator-quotient decomposition;
- the raw residue versus bad-line incidence distinction;
- the codimension-`(t-1)` explanation of why `sigma=1` is a degenerate
  endpoint;
- the replacement wall `W-F1-AA-RES-LINE-INCIDENCE`.

## What Not To Bank

Do not bank:

- a proof of `prob:perfiber`, `conj:B`, or `conj:final-mca`;
- any `n^{1+o(1)}` incidence bound;
- any claim that raw residue values are bounded by `n^{1+o(1)}`;
- any generic/asymptotic statement about random anchors beyond finite sanity
  evidence;
- any `q_gen` collapse;
- any protocol denominator saving;
- any line-decoding, list-decoding, CA, MCA, or SNARK ledger statement.

## Next Target

Attack `W-F1-AA-RES-LINE-INCIDENCE` directly.

Highest-value next prompt: prove or refute an incidence bound for

```text
[L_S Q_S]_E in [W]_E - F[Bnum]_E
```

with `deg Q_S<=j-1`, `j=n-a=r-t`, under separated aperiodic `E` and balanced
`t=sigma`. The first finite test should enumerate `t=2`, `j=2` cases and output
either a reproducible excess-slope counterpacket or evidence that line landings
stay much smaller than raw residues.
