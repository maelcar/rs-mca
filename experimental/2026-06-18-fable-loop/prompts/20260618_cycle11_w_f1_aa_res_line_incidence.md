# Cycle 11 Prompt: W-F1-AA-RES-LINE-INCIDENCE / ONLINE-SLOPE-COUNT

You are working on the RS-MCA / Proximity Prize repository as a skeptical
mathematical co-director. Your task is not to summarize the project. Attack the
current exact wall.

Use only the provided repository/project source. Do not browse. Do not edit main
papers. Treat `.tex` files as source of truth. Treat route-board and audit files
as current working context.

## Read First

- `input_project/ACTIVE_WALLS.md`
- `input_project/BANKED_LEMMAS.md`
- `input_project/CUTS_AND_FALSE_ROUTES.md`
- `input_project/NEXT_PROMPT_QUEUE.md`
- `input_project/ROUTE_BOARD_CURRENT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE9_W_F1_AA_RES_RESIDUE_COUNT_LINE_INCIDENCE_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE10_MANUAL_RESIDUE_COUNT_ROUTE_CUT_AUDIT.md`
- `input_project/current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle9_locator_quotient_incidence_check.py`
- `input_project/upstream_main_20260618/tex/slackMCA_v3.tex`

In `slackMCA_v3.tex`, respect:

- `def:residue`
- `thm:normalform`
- `prob:perfiber`
- `conj:B`
- `rem:aper`
- `thm:rigidcyclo`
- `thm:exactcount`

## Current Wall

The live target is:

```text
W-F1-AA-RES-LINE-INCIDENCE / ONLINE-SLOPE-COUNT
```

Setup:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `D subset B`.
- `q_chal` is unused.
- Balanced ledger: `a=ceil((1-delta)n)`, `sigma=a-k`, `t=sigma`, hence
  `a=k+t=s_delta`.
- `w=w0+alpha*w1`, with `w0,w1:D->B`.
- `E in F[X]`, `deg E=t`, `gcd(E,E^tau)=1`, `E` nonzero on `D`.
- `Bnum` is nonzero with `deg Bnum<t`.
- Quotient-periodic denominators are separated as in `rem:aper`.

Cycle 9 banked:

```text
W = L_S Q_S + interp_S(w),
deg Q_S <= n-a-1 = j-1,  j=n-a=r-t,
[interp_S(w)]_E = [W]_E - [L_S Q_S]_E.
```

The source-relevant object is not the raw residue count
`#{[interp_S(w)]_E}`. It is the online slope / bad-line incidence count:

```text
#{ z in F : exists noncontained a-subset S with
   [interp_S(w0)+alpha interp_S(w1)]_E = z[Bnum]_E }.
```

Equivalently:

```text
[L_S Q_S]_E lands in [W]_E - F[Bnum]_E inside F[X]/E.
```

The bad line has codimension `t-1` over `F`. The `sigma=1` counterpacket is the
codimension-zero endpoint and must not be used as an above-reserve refutation.

## Exact Task

Produce exactly one of:

```text
PROOF
COUNTERPACKET
BANKABLE_LEMMA
ROUTE_CUT
EXACT_NEW_WALL
```

Preferred hard target:

Decide the first nontrivial finite incidence regime:

```text
t=sigma=2, j=n-a=r-t=2
```

Either:

1. prove a source-valid line-incidence lemma in this regime;
2. produce a finite balanced counterpacket with explicit `p,D,k,a,t,E,Bnum,w0,w1`
   and enough data for Codex to verify locally;
3. prove that even this finite regime reduces to a sharper named obstruction.

If you cannot decide `t=2,j=2`, state the exact obstruction and make it sharper
than the current wall.

## Forbidden Repeats

Do not:

- attack raw residue cardinality as the MCA object;
- reopen the twist;
- absorb nonconstant `theta` into `w0+theta*w1`;
- import `thm:exactcount` / `thm:rigidcyclo` beyond their proved
  canonical/monomial strata;
- prove only the same-slope kernel `E*F_{<k}[X]`;
- use unrestricted `ass:extension-mca-lift`;
- use raw arbitrary locator fibers;
- claim `q_gen` collapse unless proved;
- claim protocol, MCA, CA, list-decoding, or line-decoding consequences.

## Output Format

Start with:

```text
Final classification: <PROOF | COUNTERPACKET | BANKABLE_LEMMA | ROUTE_CUT | EXACT_NEW_WALL>
```

Then give:

- precise statement or counterpacket;
- source dependencies;
- field ledger (`q_gen`, `q_line`, `q_chal`, `B`, `F`);
- parameter ledger (`n`, `k`, `rho`, `delta`, `eta`, `sigma/t`, `j=n-a`, quotient order if used);
- proof/audit notes;
- if computational, exact finite data and a verifier outline;
- what Codex should bank or test next.

END_OF_FABLE_RESPONSE
