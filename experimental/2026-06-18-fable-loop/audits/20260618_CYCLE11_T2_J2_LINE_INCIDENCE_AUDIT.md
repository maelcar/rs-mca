# Cycle 11 Audit: t=2, j=2 Line-Incidence Lemma

Status: BANKABLE_LEMMA / AUDIT.

Run:

- Run id: `2026-06-18T00-49-00-860Z-cycle11-w-f1-aa-res-line-incidence-87024365`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T00-49-00-860Z-cycle11-w-f1-aa-res-line-incidence-87024365`
- Lane: VS Code credited terminal ads lane.
- Harness result: `ok=true`, `classification=BANKABLE_LEMMA`,
  `answerSource=claude_structured_jsonl`,
  `captureWarning=TUI_VISIBLE_TERMINAL_MALFORMED_RECOVERED_FROM_CLAUDE_JSONL`.
- Audited math artifact: clean recovered `response.md`, copied to
  `../raw/20260618_CYCLE11_W_F1_AA_RES_LINE_INCIDENCE_RESPONSE.md`.
- Terminal transcript is revenue/debug evidence only.
- Prompt copied to `../prompts/20260618_cycle11_w_f1_aa_res_line_incidence.md`.

## Verdict

Cycle 11 is significant. It gives a source-relevant positive lemma for the
first finite bad-line incidence regime:

```text
t = sigma = 2,      j = n-a = r-t = 2,
a = n-2,            k = n-4.
```

The bankable content is not a proof of `conj:B`, not a protocol theorem, and
not a general reserve theorem. It is a narrow low-reserve incidence calculation
showing that the corrected Cycle 9 object can be small once the bad line has
codimension one.

## Banked Lemma

Let `B=F_p`, `F=F_{p^2}`, `D subset B`, `|D|=n`, and write
`w=w0+alpha w1` with `w0,w1:D->B`. Let `W=interp_D(w)`. Let `E in F[X]` be
separated of degree `2`, nonzero on `D`, with `gcd(E,E^tau)=1`, and let
`Bnum` have `deg Bnum<2` and `[Bnum]_E != 0`.

For a support `S` of size `a=n-2`, let the co-support be
`T=D\S={d1,d2}`, and put

```text
s_T=d1+d2,      p_T=d1 d2,
L_S=prod_{d in S}(X-d),     I_S=interp_S(w).
```

Euclidean division gives

```text
W = L_S Q_S + I_S,      deg Q_S <= 1.
```

Writing `C=[W]_{n-1}`, `C1=[W]_{n-2}+C sigma_1(D)`, one has the closed form

```text
Q_S = C (X-s_T) + C1.
```

Thus in the `t=2,j=2` regime the quotient depends on the co-support only
through the sum `s_T`, not through `p_T`.

Let `R=F[X]/E`. The bad-line landing condition

```text
[I_S]_E = z [Bnum]_E  for some z in F
```

is equivalent to one determinant equation. Define

```text
P   = [W]_E [L_T]_E - [L_D]_E [Q_S]_E,
B'' = [Bnum]_E [L_T]_E,
det(s,p) = wedge(P,B'') in F[s,p].
```

Then `S` lands on the bad line iff `det(s_T,p_T)=0`, and the slope `z` is
unique. Moreover `deg det <= 2`, and the coefficient of `p^2` in `det` is

```text
kappa = wedge([W]_E,[Bnum]_E).
```

Consequently `det identically zero => kappa=0`, the global/tangent endpoint
already anticipated by `rem:strata`.

If `det` is not identically zero, the slope count

```text
C2 = #{ z in F : exists S, [I_S]_E = z [Bnum]_E }
```

is `O(n)`, and the response gives the explicit conservative bound `C2<=6n`.
In generic non-resonant cases where the two base components of `det` share no
common factor, Bezout gives `C2<=4`.

For `D=F_p`, `p>=7`, and `deg W=n-1` (`C != 0`), the response argues that the
identically-zero determinant resonance is excluded by repeated-sum co-supports.
Bank this with the stated top-degree/nonresonance hypotheses attached.

## Source Dependencies

- `tex/slackMCA_v3.tex:1189`, `def:residue`: the source object is a
  noncontained residue-line slope packing, not raw residue cardinality.
- `tex/slackMCA_v3.tex:1197`, `thm:normalform`: MCA is controlled by
  `Lambda^{NC}_{t,delta}` after maximizing over residue-line data.
- `tex/slackMCA_v3.tex:1209`, `rem:strata`: tangent/global explanation strata
  must be kept separate; `kappa=0` belongs here.
- `tex/slackMCA_v3.tex:1227`, `prob:perfiber`: the missing object is a
  per-fiber/bad-line packing problem.
- `tex/slackMCA_v3.tex:1231`, `conj:B`: the full conjectural positive theorem
  remains open.
- `tex/slackMCA_v3.tex:1255`, `rem:aper`: quotient-periodic denominator
  families must remain separated in positive statements.

Cycle dependencies:

- Cycle 3 nonzero-numerator noncontainment subset lemma.
- Cycle 8 separated quadratic twist/residue isomorphism.
- Cycle 9 locator-quotient line-incidence reduction.
- Cycle 10 route cut identifying line-incidence / online-slope count as the
  source-corrected live object.

## Local Verification

Codex added and ran:

```text
../local_checks/20260618_cycle11_t2_j2_line_incidence_verify.py
```

The checker samples `B=F_p`, `F=F_{p^2}`, `D=F_p` for `p=7,11,17`, random
separated quadratic denominators, random nonzero numerators, and random base
anchors. It verifies:

- `Q_S = C(X-s_T)+C1` for every co-support;
- the determinant landing predicate agrees with the direct bad-line slope test;
- the symbolic `p^2` coefficient of `det` equals
  `wedge([W]_E,[Bnum]_E)`;
- sampled `D=F_p` cases satisfy `C2<=6n`;
- no sampled `C != 0` case has `det identically zero`.

Run result:

```text
cycle11_t2_j2_line_incidence_verify: PASS max_C2=2
```

This is sanity evidence only; the banked lemma is the algebra above, not the
finite sample.

## What To Bank

Bank:

- `t=2,j=2` quotient rigidity:
  `Q_S=C(X-s_T)+C1`.
- bad-line landing is a single quadratic determinant equation in
  `(s_T,p_T)`;
- `[p^2]det=kappa=wedge([W]_E,[Bnum]_E)`;
- `det identically zero => kappa=0`, matching the tangent/global stratum;
- conditional `C2=O(n)`, explicitly `C2<=6n` when `det` is not identically
  zero;
- generic `C2<=4` under the no-common-component hypothesis;
- for `D=F_p`, `p>=7`, and `C != 0`, the repeated-sum argument as the proposed
  resonance exclusion.

## What Not To Bank

Do not bank:

- a proof of `conj:B`;
- any extension to `j>=3` or `t>=3`;
- any asymptotic corrected-reserve theorem;
- any `q_gen` collapse;
- any line-decoding, list-decoding, CA, MCA, or SNARK/protocol denominator
  consequence;
- any raw residue cardinality bound as the MCA object;
- any statement that removes quotient-periodic or tangent strata without a
  separate theorem.

## Field Ledger

- `q_gen=p`, `B=F_p`: base/generated field for `D`, `w0`, `w1`, locators,
  co-support sums/products `s_T,p_T`.
- `q_line=p^2`, `F=F_{p^2}`: extension field for `E`, `Bnum`, residues in
  `F[X]/E`, determinant values, and slopes `z`.
- `q_chal`: unused.

No field-ledger merger is claimed.

## Parameter Ledger

- `n=|D|`.
- `t=deg E=2`.
- `sigma=a-k=2`.
- balanced ledger: `a=k+t=n-2`, hence `k=n-4`.
- `r=n-k=4`.
- `j=n-a=r-t=2`.
- co-support order: `|T|=2`.
- quotient degree: `deg Q_S<=j-1=1`.
- numerator: `deg Bnum<2`, `[Bnum]_E != 0`.
- bad-line codimension in `F[X]/E`: `t-1=1`.

## Next Target

Cycle 11 closes the first finite test case. The next wall should be:

```text
W-F1-AA-RES-T2J3:
extend or refute the bad-line incidence law for t=2, j=3.
```

Reason: when `j=3`, `deg Q_S<=2`, so `Q_S` should begin depending on both
`s_T` and `p_T`; the special `j=2` sum-only rigidity is expected to fail. A
secondary target is `t=3,j=2`, where the bad line has codimension two inside a
three-dimensional residue algebra.
