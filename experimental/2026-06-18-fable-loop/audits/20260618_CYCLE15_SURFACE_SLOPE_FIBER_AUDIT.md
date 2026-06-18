# Cycle 15 Audit: Surface Slope-Fiber Rank Wall

Status: EXACT_NEW_WALL / AUDIT.

Run:

- Run id: `2026-06-18T05-12-23-339Z-cycle15-surface-slope-fiber-340f8f67`
- Run dir: `/Users/danielcabezas/packy-fable-ui/projects/rs-mca-proximity-prize-research/runs/2026-06-18T05-12-23-339Z-cycle15-surface-slope-fiber-340f8f67`
- Lane: isolated RS-MCA VS Code credited terminal ads lane.
- Launcher: `/Users/danielcabezas/packy-fable-ui/.codex-vscode-launchers/rs-mca-current`
- App workaround: private no-xattr VS Code copy at
  `/Users/danielcabezas/packy-fable-ui/.vscode-app-sandbox/Visual Studio Code.app`
  because `/Applications/Visual Studio Code.app` stalled during macOS
  code-signing validation.
- Harness result: `ok=true`, `classification=EXACT_NEW_WALL`,
  `answerSource=claude_structured_jsonl`,
  `captureWarning=TUI_RESPONSE_REPLACED_BY_CLAUDE_STRUCTURED_JSONL`.
- Audited math artifact: clean `response.md`, copied to
  `../raw/20260618_CYCLE15_SURFACE_SLOPE_FIBER_RESPONSE.md`.
- Terminal transcript is revenue/debug evidence only.

## Verdict

Cycle 15 does not prove slope collapse and does not construct a
`Theta(q_line)` counterpacket. It sharpens the Cycle 14 slope-fiber wall to an
explicit rank/determinant invariant for the affine equation

```text
L_z(tau) := iota(tau) - z mu(tau) = 0 in A=F[X]/E.
```

Bank the column construction, the determinant-consistency formulation, and the
scanner target. Do not bank the answer's strongest "rank alone decides
`O(p)` versus `Theta(q_line)`" language without the determinant identity check
below.

## Field And Parameter Ledger

- `B=F_p`, `q_gen=p`.
- `F=F_{p^2}`, `q_line=p^2`.
- `q_chal` unused.
- `D=F_p`, so `n=p`.
- `t=sigma=2`.
- `j=n-a=3`, so `a=n-3`, `k=n-5`.
- Work is off `R0={ [W]_E wedge [Bnum]_E = 0 }` unless stated otherwise.

## Banked Structural Reduction

Cycle 14 gives, off `R0`, an `F`-basis `{[W]_E,b}` of
`A=F[X]/E` and affine-linear forms in `tau_1,tau_2`:

```text
iota(tau) = A0(tau_1,tau_2) - tau_3 [W]_E,
mu(tau)   = B0(tau_1,tau_2) - tau_3 b,
A0 = p1[W]_E + p2 b,
B0 = q1[W]_E + q2 b.
```

Landing `[I_S]_E=z b` is equivalent to

```text
L_z(tau)=iota(tau)-z mu(tau)=0.
```

Writing

```text
p_i = p_i^c + p_i^1 tau_1 + p_i^2 tau_2,
q_i = q_i^c + q_i^1 tau_1 + q_i^2 tau_2,
```

the `B`-linear part of `L_z:B^3 -> A ~= B^4` has columns

```text
c1(z) = (p1^1 - z q1^1)[W]_E + (p2^1 - z q2^1)b,
c2(z) = (p1^2 - z q1^2)[W]_E + (p2^2 - z q2^2)b,
c3(z) = -[W]_E + z b.
```

These columns are explicit degree-`<=1` functions of the two `B`-coordinates
of `z in F`.

## Audit Correction

The raw Cycle 15 answer states a clean rank dichotomy. The column construction
is useful, but the stated dimension count is too fast:

- For fixed `z`, if the column rank is `3`, then
  `L_z(tau)=0` is an affine consistency problem for a `3`-plane in
  `A ~= B^4`.
- Consistency imposes one determinant condition in the two `B`-coordinates of
  `z`:

```text
Q(z_0,z_1)=det_{4x4}[c1(z) | c2(z) | c3(z) | c0(z)],
```

  where `c0(z)` is the constant column of `L_z`.
- Therefore rank `3` plus `Q != 0` gives an `O(p)` slope set, not
  `Theta(p^2)`.
- Rank `3` plus `Q == 0` identically is the possible `Theta(p^2)` slope
  regime.

Thus the safe wall is not "rank alone"; it is the rank/determinant pair.

## Exact New Wall

The sharpened wall is:

```text
W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DETERMINANT.
```

On source-valid `Ra/Rb` resonance data, off `R0`, compute the three columns
`c1,c2,c3` and determinant consistency polynomial `Q(z_0,z_1)`.

Target dichotomy:

- `Q != 0`, or rank drops so that the image is at most a curve:
  bank `C2=O(p)=O(n)`.
- `Q == 0` identically with enough split-distinct co-supports and generically
  finite slope map:
  construct a sub-reserve `Theta(q_line)` counterpacket to this finite wall.

This remains below corrected reserve because `eta=sigma/n=2/n`.

## Local Forced-Ra Scan

Codex added a local finite scanner:

- `../local_checks/20260618_cycle15_forced_ra_slope_scan.py`

The scanner forces the `Ra` condition by linear algebra. For each projective
`B`-line direction in `F`, it requires all ten quadratic coefficients of
`Delta` to lie on that line, samples the resulting `W`-kernel, and enumerates
distinct split-cubic slopes.

Smoke result over `B=F_7`, `F=F_49`, `D=F_7`:

```text
forced_ra_slope_scan: BEST p=7 q_gen=7 q_line=49 seed=3
C2=6 split_landings=6 off_R0=True direction=(1, 0) kernel_dim=7
```

All 12 smoke seeds had forced `coeff_rank=1`, `off_R0=True`, and
`C2 <= 6`. This is experimental evidence only. It does not prove collapse and
does not refute the possibility of a larger `Ra/Rb` counterpacket.

## What To Bank

Bank:

- The affine fiber equation `L_z(tau)=iota-z mu=0`.
- The explicit `B`-columns `c1(z),c2(z),c3(z)` in `A ~= B^4`.
- The determinant-consistency invariant `Q(z_0,z_1)`.
- The sharpened wall
  `W-F1-AA-RES-T2J3-SURFACE-SLOPE-FIBER-RANK-DETERMINANT`.
- The forced-`Ra` finite scanner as EXPERIMENTAL / AUDIT evidence.

## What Not To Bank

Do not bank:

- a proof of `C2=O(p)` on all `Ra/Rb`;
- a `Theta(q_line)` counterpacket;
- the raw statement that rank `3` alone implies `Theta(q_line)`;
- a proof of `conj:B`;
- any result at or above corrected reserve;
- any `q_gen` collapse;
- any protocol, MCA, CA, list-decoding, line-decoding, or SNARK consequence.
