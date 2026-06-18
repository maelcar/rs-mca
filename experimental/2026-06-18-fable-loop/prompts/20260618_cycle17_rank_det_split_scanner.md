# Cycle 17 Prompt: Q==0 Split-Distinct Scanner

You are a skeptical mathematical research agent for the RS-MCA / Proximity
Prize repository. Work only from the mounted source/context files. Do not edit
the main papers. Keep the field ledgers separate:

- `B=F_p`, generated/entropy/base field, `q_gen=p`.
- `F=F_{p^2}`, extension/line field, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, so `n=p`.

Target:

```text
W-F1-AA-RES-T2J3-RANK-DET-SPLIT
```

Cycle 16 banked the safe side:

```text
Q(z_0,z_1) not identically zero => C2 <= 4p = O(n)
```

in the `D=F_p`, `t=sigma=2`, `j=3`, off-`R0` regime. The live wall is the
`Q==0` branch with the distinct split-cubic condition retained.

## Source Context To Read

Read these first:

- `DIRECTOR_STATE.md`
- `ROUTE_BOARD_CURRENT.md`
- `ACTIVE_WALLS.md`
- `BANKED_LEMMAS.md`
- `CUTS_AND_FALSE_ROUTES.md`
- `NEXT_PROMPT_QUEUE.md`
- `current_loop_20260618/2026-06-18-fable-loop/audits/20260618_CYCLE16_RANK_DETERMINANT_RESONANCE_AUDIT.md`
- `current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle12_base_component_rank_scan.py`
- `current_loop_20260618/2026-06-18-fable-loop/local_checks/20260618_cycle15_forced_ra_slope_scan.py`

## Task

Produce an implementable scanner/certificate for the `Q==0` split-distinct
branch. If output files are allowed, write the scanner as a Python file under
the run's `output_files/` directory, e.g.

```text
output_files/rank_det_split_scanner.py
```

If you cannot write files, provide the full script text in the answer.

The scanner should extend the existing local checks rather than inventing a new
finite-field stack. Reuse the field/model code from the mounted files where
possible.

## Mathematical Object

Parameters:

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, `n=p`.
- `t=sigma=2`, `j=n-a=3`, so `a=n-3`, `k=n-5`.
- `eta=2/n`, sub-reserve.
- Work off `R0={wedge([W]_E,[Bnum]_E)=0}`.

For source-valid `Ra/Rb` resonance data, compute the Cycle 15 determinant
consistency polynomial

```text
Q(z_0,z_1)=det_{4x4}[c1(z)|c2(z)|c3(z)|c0(z)].
```

Cycle 16 says `Q!=0` is already handled. The scanner should focus on the
`Q==0` branch and count distinct slopes coming from distinct split co-supports
`T subset F_p`, `|T|=3`.

## Required Scanner Behaviour

The scanner should:

1. Generate or accept `p`, irreducible/nonresidue parameter for `F_{p^2}`,
   separated quadratic `E`, nonzero numerator `Bnum`, and base anchors
   `w0,w1:F_p->F_p`.
2. Compute the Cycle 12/14 quantities already used by the existing scripts:
   `Delta`, `Q_S`, `A0/B0` or equivalent slope data.
3. Filter or force `Ra`/`Rb` resonance data. At minimum, implement the forced
   `Ra` route from `20260618_cycle15_forced_ra_slope_scan.py`.
4. Compute `Q` or an equivalent identically-zero test. If the trace/Gram
   criterion from Cycle 16 is used, mark it AUDIT unless independently checked
   in the code by direct polynomial interpolation/evaluation of `Q`.
5. On `Q==0` cases, enumerate distinct split co-supports
   `T subset F_p`, `|T|=3`, compute the slope `z`, and output `C2`.
6. Emit deterministic certificates with enough data to reproduce the case.

Required certificate fields:

```text
{
  p,
  q_gen,
  q_line,
  seed,
  E,
  Bnum,
  stratum,
  off_R0,
  Q_identically_zero,
  degQ_or_test,
  split_triples_examined,
  split_landings,
  C2,
  max_slope_fiber,
  fiber_histogram_summary,
  status
}
```

Statuses:

```text
PASS_QNONZERO_OP
OPEN_QZERO_SMALL_SAMPLE
COUNTERPACKET_C2_GROWTH_CANDIDATE
HARNESS_OR_SOURCE_GAP
```

Counterpacket trigger:

```text
Q==0 and C2/p^2 bounded below across a growing-p family.
```

A single-prime example is EXPERIMENTAL only.

## Output Classification

Classify the result exactly:

- `BANKABLE_LEMMA` only for source-checked scanner identities or direct
  verification logic, not for finite samples.
- `COUNTERPACKET` only for a reproducible growing-p family or a convincing
  symbolic family with `C2/p^2` bounded below.
- `EXACT_NEW_WALL` if the scanner exposes a sharper obstruction.
- `AUDIT` if this is only a checker implementation/spec.
- `EXPERIMENTAL` for finite sample outcomes.

Do not claim:

- a proof of `conj:B`;
- a corrected-reserve counterpacket from `eta=2/n`;
- any `q_gen` collapse;
- any protocol/MCA/CA/list-decoding/line-decoding/SNARK consequence;
- any theorem from terminal/ad transcript text.

Expected final primary classification, exactly one:

```text
BANKABLE_LEMMA
COUNTERPACKET
EXACT_NEW_WALL
AUDIT
EXPERIMENTAL
```
